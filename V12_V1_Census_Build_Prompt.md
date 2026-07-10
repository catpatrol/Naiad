# BUILD PROMPT — v12 Study · Phase V1 "Data Census & Integrity Gate"
### Feed this file to Claude Code. It is a self-contained contract. · 2026-07-10
### Builder: Claude Code · Reviewer: Claude (Project, Fable-mode) · Operator: Ludwig

---

## 0. Mission

Produce a **complete, verified, partition-tagged candle-and-funding estate** for
the v12 Study, plus the census documents that prove it. Where the existing
backfill is shallower than available Binance history, extend it. Where it has
holes, repair them or classify them as exchange-side. Install the loader guards
(LIT floor, study right edge, lockbox seal). Append the ledger. **Run no
analysis of any kind** — this phase touches metadata and bytes, never meaning.

Definition of done: `DATA_CENSUS.md` and `census.json` exist, committed, and
every claim in them is reproducible by re-running the census on the same estate;
fixtures F1–F9 pass; the operator spot check passes; the ledger append (D6) is
committed; a session packet is delivered.

## 1. Read these before writing any code

1. `V12_Study_Charter_Addendum_v1.0.md` — the ratified partition, classes, and
   rules this phase enforces. **On any conflict, the addendum wins.**
2. `LEDGER.md` in the repo root — reconcile the addendum's stated anchors
   against it; if they disagree, STOP and report the diff before proceeding.
3. The Phase 1 data-loader code and storage layout already in this repo.
   **Reuse its conventions** (paths, file format, naming). Do not introduce a
   second storage format. If a convention is genuinely absent, choose one,
   record it in the `census.json` header, and flag it in the packet manifest.

## 2. Context and prior findings the builder must honor

- **LIT two-token trap (hard-coded law):** Binance symbol LITUSDT belonged to
  Litentry until its delisting; the same symbol now trades the Lighter token.
  LIT's first valid candle is floored at **2025-12-23 00:00:00 UTC** on all six
  intervals (verified in Phase 1). Earlier LITUSDT history is a different asset
  and must never enter the estate.
- **Ledger corruption lesson:** a prior manual paste escaped markdown characters
  into LEDGER.md. That is why D6 is a builder task: append the block
  byte-for-byte as given in addendum §8, via file write, and show the diff.
- **Phase 1 anchors of record:** engine 1.0.1 @ commit da31062, 26 fixtures
  green. This phase adds data tooling and fixtures; it does not modify engine
  signal logic.
- **Idempotent-writer lesson:** journal/manifest writers must be safe to re-run;
  re-execution on an unchanged estate must reproduce identical outputs.

## 3. Frozen invariants (violating any of these is a failed phase)

- **I1 — LIT floor.** Loading LITUSDT on any interval yields no candle with
  open time < 2025-12-23 00:00:00 UTC. The loader hard-floors; requests for
  earlier ranges return empty and log a guard event.
- **I2 — Study right edge.** No candle with open time > 2026-07-07 23:59:59 UTC
  enters the study estate or the census. (Forward data is Naiad's; if it exists
  on disk it is simply outside this manifest.)
- **I3 — Lockbox seal.** For candles with open time in
  [2024-07-01 00:00:00, 2025-10-05 23:59:59] UTC, the study loader permits only
  integrity operations: row count, timestamp continuity, duplicate check, hash.
  Any code path requesting OHLCV **values** from lockbox rows without the
  explicit `integrity_only` mode raises `LockboxViolation`. No statistic
  derived from lockbox prices is computed, printed, logged, or plotted in this
  phase or any phase before V8.
- **I4 — Timestamp discipline.** All timestamps UTC, open-time convention,
  strictly increasing within a file, spacing consistent with the interval.
- **I5 — No mutation of verified artifacts.** Existing journals and their
  hashes are untouched. New files only. Every estate file is hashed (SHA256).
- **I6 — Source of truth.** Binance public data (Vision dumps and/or REST
  klines), USDT-M perpetuals. The source channel and retrieval date are
  recorded per file in `census.json`.
- **I7 — Determinism.** Re-running the census on an unchanged estate produces a
  byte-identical `census.json` (stable ordering, no wall-clock timestamps in
  the body; retrieval dates live in per-file metadata written once).
- **I8 — One storage convention.** Phase 1's format and layout, extended — not
  replaced.

## 4. Inputs

- **Assets (10):** BTCUSDT, ETHUSDT, SOLUSDT, NEARUSDT, ZECUSDT, JTOUSDT,
  TAOUSDT, HYPEUSDT, FARTCOINUSDT, LITUSDT — Binance USDT-M perpetuals.
- **Intervals (6):** 1m, 5m, 15m, 1h, 4h, 12h.
- **Coverage target per series:** from the earliest candle Binance provides for
  the perpetual contract (or the LIT floor) through the study right edge.
- **Funding-rate history** per asset, full available depth to the right edge
  (8-hour records; used by later phases' cost model — collected now, analyzed
  never in this phase).
- **Partition boundaries (from addendum VR-1):** exploration-classic
  ≤ 2024-06-30 23:59:59 · lockbox 2024-07-01 → 2025-10-05 23:59:59 · spent
  (BTC) / regime-contaminated (non-BTC) 2025-10-06 → 2026-07-07 23:59:59.

## 5. Deliverables

- **D1 — Estate completion.** Resumable, rate-limit-polite backfill that brings
  all 60 asset×interval candle series and 10 funding series to the coverage
  target. Safe to interrupt and re-run (I7 applies to the census; downloads may
  append, then the census re-verifies).
- **D2 — `DATA_CENSUS.md`.** Human-readable table, one row per asset×interval:
  first candle (UTC), last candle (UTC), row count, gap count, largest gap,
  rows per partition class (exploration-classic / lockbox / spent-or-
  contaminated), source channel, file SHA256 (first 12 hex). Plus a funding
  table (per asset: first record, last record, count, gaps) and a one-paragraph
  plain-language summary of which assets contribute exploration-classic history
  and which are contaminated-only.
- **D3 — `census.json`.** Machine manifest: per file — path, symbol, interval,
  first/last open time, row count, gap list (start, end, bars missing,
  classification), partition row counts, source, retrieval date, SHA256. This
  file is the loader guards' source of truth from this phase forward.
- **D4 — Gap policy report.** Every gap > 1 interval listed and classified:
  `download_hole` (re-fetch; a hole surviving two independent re-fetch attempts
  escalates to) `exchange_side` (documented, accepted). Listing-edge gaps at a
  contract's birth are `listing_edge`, expected and accepted. Zero unresolved
  `download_hole` entries at phase end.
- **D5 — `SPOT_CHECK.md`.** For the operator: 3 candles per asset (30 rows),
  drawn from different intervals and eras (include at least one exploration-era
  and one contaminated-era candle per asset where history allows; **never a
  lockbox candle** — printing its OHLCV would violate I3). Each row: symbol,
  interval, exact UTC open time, expected O/H/L/C/V, and a plain-language
  TradingView navigation line ("open BINANCE:SOLUSDT.P, 4h, scroll to
  2023-03-14 08:00 UTC"). Escalation rule printed at the top: one mismatch on
  an asset → builder regenerates a 10-row sheet for that asset and
  investigates before the phase can pass.
- **D6 — Ledger append.** Addendum §8 block, byte-for-byte, appended to
  `LEDGER.md`; commit shows the diff and nothing else in that file changed.
- **D7 — Session packet.** One zip: `DATA_CENSUS.md`, `census.json`, gap
  report, `SPOT_CHECK.md`, fixture results, ledger diff, one-page manifest
  (what ran, what changed, open items).

## 6. Fixtures (all must pass; add to the existing suite, do not modify old ones)

- **F1 — LIT floor.** Loading LITUSDT (each interval) returns first open
  ≥ 2025-12-23; a request for 2025-01-01→2025-12-22 returns empty + guard log.
- **F2 — Right edge.** A request spanning past 2026-07-07 23:59:59 returns
  nothing later; guard log written.
- **F3 — Lockbox seal.** Value-mode read of a lockbox range raises
  `LockboxViolation`; `integrity_only` mode on the same range succeeds and
  returns counts/hashes only.
- **F4 — Timestamp discipline.** A synthetic file containing a duplicate row, a
  backward timestamp, and an off-grid timestamp → census flags all three,
  individually identified.
- **F5 — Gap detection.** A synthetic file with a known 3-candle hole → gap
  report names the exact missing range and bar count.
- **F6 — Census determinism.** Census run twice on an unchanged estate →
  `census.json` byte-identical (hash-equal).
- **F7 — Partition tagging.** Boundary candles land correctly:
  2024-06-30 23:59 → exploration-classic; 2024-07-01 00:00 → lockbox;
  2025-10-05 23:59 → lockbox; 2025-10-06 00:00 → spent for BTCUSDT and
  regime-contaminated for any non-BTC symbol.
- **F8 — Hash integrity.** Flipping one byte in a copy of an estate file →
  census reports a manifest hash mismatch for that file.
- **F9 — Funding continuity.** Funding series spacing verified at the 8-hour
  grid; a synthetic missing record is flagged.

## 7. Verdict criteria (pre-registered)

V1 **passes** if and only if: all 60 candle series and 10 funding series reach
the coverage target with only `exchange_side` and `listing_edge` gaps
remaining; F1–F9 green; operator spot check returns zero unresolved
mismatches; D2/D3/D4/D5 committed; D6 diff clean; D7 delivered.
V1 **fails pending investigation** if any `download_hole` survives two
re-fetch attempts, any fixture is red, or the LEDGER reconciliation in §1
found a divergence. A failed phase produces the packet anyway, with the
failure named on page one of the manifest.

## 8. What this phase is not

No indicator mathematics. No signals, no backtests, no cell cards. No plots or
statistics of price anywhere — not even on exploration data. No engine
signal-logic changes. No Naiad paper-line changes. No parameter discussion.
No variant work. No reading of any candle past 2026-07-07. Anything not listed
in §5 is out of scope; if it looks necessary, stop and report instead of
building it.

---

## 9. Operator runbook (for Ludwig — the builder skips this section)

Plain language, one step at a time. Rough time: 15 minutes of your attention,
then a long unattended download, then ~45–60 minutes for the spot check.

**Before you start:** make sure you have at least **10 GB free disk space**
(the full 1-minute history for ten assets is large). The download can take
from tens of minutes to a few hours depending on your connection. It is safe
to close the laptop or stop the process — the contract requires downloads to
be resumable, so restarting continues where it left off.

**Step 1 — Put the two files where the builder can see them.**
Download `V12_Study_Charter_Addendum_v1.0.md` and
`V12_V1_Census_Build_Prompt.md` from our chat, then move both into your Naiad
project folder (the folder that contains `LEDGER.md`). *What this does: the
builder can only read files inside the project folder.* *What you should see:
both files listed when you open that folder in File Explorer.*

**Step 2 — Open PowerShell.**
Press the Windows key, type `powershell`, press Enter. *What this does: opens
the command window you type instructions into.* *What you should see: a
blue/black window with a line ending in `>`.*

**Step 3 — Go to the project folder.**
Type `cd ` (with a space), then drag the Naiad folder from File Explorer into
the PowerShell window (this pastes its full path), press Enter. *What this
does: points the command window at your project.* *What you should see: the
prompt now ends with your folder name, e.g. `...\Naiad>`.*

**Step 4 — Get the latest project state.**
Type `git pull` and press Enter. *What this does: downloads any changes made
since your last session.* *What you should see: either `Already up to date.`
or a short list of updated files.* **If instead you see "repository not
found":** this is the known leftover from the repo rename. Type
`git remote set-url origin <the new GitHub address of your Naiad repo>` —
the address is on your repo's GitHub page under the green "Code" button —
then run `git pull` again.

**Step 5 — Start the builder.**
Type `claude` and press Enter. *What you should see: the Claude Code welcome
screen inside the same window.*

**Step 6 — Hand over the contract.**
Type exactly: `Read V12_V1_Census_Build_Prompt.md and
V12_Study_Charter_Addendum_v1.0.md in the project root and execute the build
prompt as this session's contract.` *What this does: the builder reads both
documents and starts Phase V1.* *What you should see: the builder summarizes
the mission and begins asking permission to run commands — approve them; long
quiet stretches during downloads are normal.*

**Step 7 — The spot check (your only hands-on task).**
When the builder announces `SPOT_CHECK.md` is ready, open it (it will be in
the project folder). For each of the 30 rows: open TradingView, load the
symbol and interval named in the row, scroll to the exact date and time, hover
the candle, and compare the open/high/low/close/volume numbers against the
row. Mark each row pass or fail as the file instructs. *What this does: it is
the one check the machine cannot do alone — an independent pair of eyes
confirming the downloaded data matches the charts you actually trade.* *What
you should see: matching numbers. Tiny volume differences can occur; price
values should match. Any price mismatch → tell the builder, which must then
produce the 10-row escalation sheet for that asset.*

**Step 8 — Ferry the packet.**
The builder ends by producing one zip (the session packet). Attach that zip in
our Project chat, and paste the fixture summary lines and the LEDGER diff as
text. *What this does: hands the evidence to the reviewer — me — so I can
recompute the headline claims from the raw artifacts before V1 is declared
passed.* Phase V1 is not done when the builder says done; it is done when the
review of that packet says done.
