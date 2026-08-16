# BUILD — THE ORACLE TOP-UP · 2026-08-16

**Contract:** queue BR-1b `ORACLE DATA FRESHNESS`, RATIFIED operator 2026-08-16 under the
BR-1 Amendment A1-3 chain authorisation. **Executor:** HEPHAESTUS. **Reviewer:** ARGUS.
**Class:** operations. Fetch-and-store only — nothing here scores, aggregates or publishes.
**Code commit:** `3bdc4c5`. **This document:** published by `publish_exchange.publish()`.

---

## 0 · THE ONE THING TO READ FIRST

V-8 IS CLOSED. The kline estate was a day stale with nothing scheduled to refresh it, because
the network top-up job was retired 2026-08-05 by ruling D-3. Two more agents are now armed —
`com.naiad.oracle-topup-0645` and `com.naiad.oracle-topup-1545` — fifteen minutes ahead of each
Oracle slot. One unattended run has completed with **exit code 0**.

**The Oracle itself did not change and must not.** It is cache-only by design so a firewalled
run can never reach the network. The fetching lives in a separate organ, and the proof that the
two are correctly wired is that the Oracle's as-of advanced from **2026-08-15T12:00Z to
2026-08-16T00:00Z** with no edit to `oracle_daily.py` at all — and the BR-1 fixtures stayed
10/10 green across the change.

**THE SCOPE IS ENUMERATED, NEVER ASSERTED.** The contract's load-bearing clause is "to claim the
set, enumerate the set." A hardcoded symbol list would be a claim about `oracle_daily.py` that
rots the moment that file changes. So the scope is obtained by instrumenting the Oracle's own
`load_lens` on a real run — **10 symbols x {5m, 15m, 1h, 4h} = 40 pairs** — and pinned to a
manifest that also records the sha256 of the file it was enumerated from. If `oracle_daily.py`
changes, the top-up **HALTS** rather than fetch a scope it cannot vouch for.

30m is absent from that set on purpose: the Oracle derives it from 15m by resample, so there is
no 30m parquet to top up. 1m and 12h are absent because the Oracle never reads them. Fetching
them "to be safe" would be a silent scope change, which is exactly what the contract forbids.

---

## 1 · WHAT WAS BUILT

| ID | Deliverable | Path | State |
|---|---|---|---|
| D-1 | The top-up organ | `scripts/oracle_topup.py` | built, 17,684 B |
| D-2 | The pinned scope manifest | `research_outputs/oracle/topup_scope.json` | built, 2,843 B, TRACKED |
| D-3 | Two more armed slots | `com.naiad.oracle-topup-0645` / `-1545` | ARMED |
| D-4 | This build document | `exchange/reports/BUILD_2026-08-16_ORACLE_TOPUP.md` | this file |
| D-5 | Ledger append | `exchange/status/LEDGER_ARGUS.md` | appended |
| — | Fixtures F-TU-1..F-TU-6 | `scripts/oracle_topup_fixtures.py` | 6/6 green |
| — | Wrapper extension | `scripts/oracle_wrapper.py` | minute precision + `--job` dispatch |

### 1.1 The enumerated scope, in full

```
10 symbols : BTCUSDT ETHUSDT SOLUSDT NEARUSDT ZECUSDT JTOUSDT TAOUSDT HYPEUSDT
             FARTCOINUSDT LITUSDT
 4 intervals: 5m  15m  1h  4h
40 pairs    : the cartesian product, and nothing else
method      : instrumented oracle_daily.load_lens over one full oracle_daily.run()
pinned to   : oracle_daily.py sha256 45f44015731394f6697440e5399c4854ff6b9725e58499f699dfb5e153c51ac6
```

`load_lens` is the sole kline chokepoint in `oracle_daily.py` — verified by grep over every
`read_parquet` / `cache_dir` / `load_klines` site — so the spy cannot miss a read.

### 1.2 The first real run

```
ORACLE TOP-UP · slot=manual-proof · 40 pair(s) from the pinned scope
  BTCUSDT        15m  OK      +   59 rows  newest 2026-08-16T06:30:00+00:00  gaps=0
  BTCUSDT        1h   OK      +   14 rows  newest 2026-08-16T05:00:00+00:00  gaps=0
  BTCUSDT        4h   OK      +    3 rows  newest 2026-08-16T00:00:00+00:00  gaps=0
  BTCUSDT        5m   OK      +  177 rows  newest 2026-08-16T06:40:00+00:00  gaps=0
  ... 36 more pairs, all OK ...
  TOTAL +2521 rows across 40 pair(s); 0 gap(s) across the estate
```

Wall clock 1 min 49 s — comfortably inside the 15-minute head start the 06:45 slot has on the
07:00 Oracle. The second, unattended run added a further 10 rows in well under a minute.

### 1.3 The three states the no-clobber check separates

Kept distinct on purpose, because conflating them is how a real clobber hides:

- **shrank** — the series lost rows. Always a clobber.
- **rewrote** — a bar strictly older than the previous newest changed value. Always a clobber;
  closed bars are immutable.
- **forming_corrected** — the previously-newest bar changed. **NOT** a clobber: it was stored
  while still forming, and replacing it with the closed version is the entire point of the
  `OVERLAP_BARS` re-pull.

---

## 2 · THE FIXTURE TRANSCRIPT — verbatim, both legs

```
==============================================================================
ORACLE TOP-UP FIXTURES — 2026-08-16T06:53:17Z
  scope manifest research_outputs/oracle/topup_scope.json
  topup log      research_outputs/oracle/calibration/topup_log.jsonl
==============================================================================

F-TU-1 — SCOPE IDENTITY — the manifest equals a fresh enumeration
  [BREAK] deliberate violation -> RED (correct): scope drift — NOT FETCHED but read by the Oracle: [('BTCUSDT', '4h')]; FETCHED but never read: [('DOGEUSDT', '1m')]
  [PASS] F-TU-1: 40 pair(s) — the pinned manifest equals a fresh instrumented enumeration exactly, both directions; 10 symbol(s) x ['15m', '1h', '4h', '5m']; oracle_daily.py sha 45f44015731394f6… matches the pin

F-TU-2 — NO-CLOBBER — history never shrinks, closed bars never change
  [BREAK] deliberate violation -> RED (correct): closed bar rewritten: got {'shrank': False, 'rewrote': True, 'forming_corrected': False} want {'shrank': False, 'rewrote': False, 'forming_corrected': False}
  [PASS] F-TU-2: 5 synthetic cases separate shrink / closed-bar rewrite / forming-bar correction correctly; and the last real run (topup, 2026-08-16T06:52:42) shows 0 shrinks and 0 closed-bar rewrites across 40 pair(s), rows_added min 0 max 1 — monotone non-decreasing

F-TU-3 — FIREWALL — no journal, no aggregation, no publish
  [BREAK] deliberate violation -> RED (correct): source contains a forbidden call: 'read_journal'
  [PASS] F-TU-3: import closure of oracle_topup is 772 modules and contains no journal, forward_log, positions or publish_exchange; oracle_daily is NOT imported at module load (only inside --enumerate); no publish or git call in the source; no aggregation symbol assigned

F-TU-4 — NO exchange/ WRITE — the bus is untouched
  [BREAK] deliberate violation -> RED (correct): exchange/ touched — added ['exchange/reports/PRETEND_TOPUP_WROTE_HERE.md'], changed [], source path literals []
  [PASS] F-TU-4: 162 file(s) under exchange/ unchanged in size and mtime across a real top-up write path; and the source contains no 'exchange/' path literal at all

F-TU-5 — CONTIGUITY — gap-free, or the gap list is printed
  [BREAK] deliberate violation -> RED (correct): 1 gap(s) across 1 series — GAP LIST: BTCUSDT 15m x1
  [PASS] F-TU-5: detector proven both ways on synthetic frames; and all 40 cached series in scope are gap-free at their own interval (gap list EMPTY)

F-TU-6 — FAILURE PATH — a fault logs, exits nonzero, cache untouched
  [BREAK] deliberate violation -> RED (correct): real run topup verdict PASS
  [PASS] F-TU-6: simulated fault: verdict FAIL, 40 pair(s) reported ERROR, cache fingerprint unchanged, exactly one row appended to topup_log.jsonl, exit code would be 1

==============================================================================
GREEN 6/6 · RED 0
==============================================================================
```

Two of these fixtures were RED on their first run, and both times **the fixture was wrong, not
the code**: F-TU-2 asserted that a shrinking series must also report `rewrote` (it must not —
dropping the newest row leaves every older bar identical, which is precisely why the two flags
are separate), and F-TU-4's path scan matched the module docstring quoting the contract clause
"no exchange/ writes". F-TU-4 now walks the AST and skips docstrings.

BR-1's own fixtures were re-run after this build and are unchanged at **10/10 green**.

---

## 3 · ARMING PROOF

Schedules read back from launchd's own registry, never from the plist just written.

```
ORACLE — arming 4 slots
  zone check: oracle 2026-08-16T03:48:42-03:00 · machine 2026-08-16T03:48:42-03:00 · agree=True
  ARMED com.naiad.oracle-topup-0645 [topup]:  machine-local 06:45 (= 06:45 BA) · plutil OK · launchd {'Hour': 6,  'Minute': 45}
  ARMED com.naiad.oracle-0700       [oracle]: machine-local 07:00 (= 07:00 BA) · plutil OK · launchd {'Hour': 7,  'Minute': 0}
  ARMED com.naiad.oracle-topup-1545 [topup]:  machine-local 15:45 (= 15:45 BA) · plutil OK · launchd {'Hour': 15, 'Minute': 45}
  ARMED com.naiad.oracle-1600       [oracle]: machine-local 16:00 (= 16:00 BA) · plutil OK · launchd {'Hour': 16, 'Minute': 0}
```

Unattended proof: `launchctl kickstart -k gui/501/com.naiad.oracle-topup-0645` →
`runs = 1`, **`last exit code = 0`**, `top-up PASS: +10 rows across 40 pair(s), 0 gap(s)`,
and all four schedules re-verified at the end of the run.

### 3.1 UNDO — the exact commands

```
launchctl bootout gui/501/com.naiad.oracle-topup-0645
launchctl bootout gui/501/com.naiad.oracle-topup-1545
launchctl bootout gui/501/com.naiad.oracle-0700
launchctl bootout gui/501/com.naiad.oracle-1600

# re-arm:
launchctl bootstrap gui/501 ~/Library/LaunchAgents/com.naiad.oracle-topup-0645.plist
launchctl bootstrap gui/501 ~/Library/LaunchAgents/com.naiad.oracle-topup-1545.plist
launchctl bootstrap gui/501 ~/Library/LaunchAgents/com.naiad.oracle-0700.plist
launchctl bootstrap gui/501 ~/Library/LaunchAgents/com.naiad.oracle-1600.plist
```

Disarming the top-up alone is safe: the Oracle keeps running and simply stamps an older as-of.

---

## 4 · FINDINGS — REPORTED, NOT FIXED

**T-1 · THE CACHE IS NOW A MOVING TARGET, BY DESIGN.** Before this build the Oracle read a
frozen estate; now it reads whatever the 06:45 fetch left. BR-1's F-BR-6 refresh idempotence is
unaffected — it renders twice from one in-memory view — but any future fixture that compares two
renders taken at different times will see legitimate differences. Named here so it is not
mistaken later for non-determinism.

**T-2 · `OVERLAP_BARS` = 12 IS [VETO].** The fetch reaches 12 bars back from the newest cached
bar so a bar stored while forming is re-pulled once closed. That is ~1h at 5m and ~2d at 4h.
Proposed, not ruled.

**T-3 · THE 06:45 SLOT ASSUMES THE MACHINE IS AWAKE.** launchd runs a missed calendar job when
the machine next wakes, so a laptop asleep at 06:45 will fetch late — possibly after the 07:00
Oracle has already rendered. The Oracle is unaffected in the sense that it stamps its as-of
honestly, but the morning brief would be a day stale. No alarm exists for this. **A ruling is
available** if you want the Oracle to refuse to render on a cache older than N hours.

**T-4 · THE FIXTURE'S OWN FAILURE ROWS LIVE IN THE REAL LOG.** F-TU-6 exercises the failure path
for real, which appends a `verdict: FAIL` row to `topup_log.jsonl`. Those rows carry
`slot: "fixture-F-TU-6"` and are filtered out by `last_real_run()`, but anything else reading
that log — including BR-2 — must filter the same way.

**T-5 · A RESCHEDULE COULD TOUCH A SIBLING AGENT.** `reschedule_if_drifted` runs at the end of
every wrapper invocation and loops over all four labels, so a drifted schedule would be
bootout+bootstrapped by whichever agent noticed first. Bootout of a not-running agent is
harmless and bootstrap re-arms it immediately, and the top-up finishes ~2 minutes after 06:45
while the Oracle fires at 07:00 — so the window is not reachable in practice. Recorded because
it is a real coupling between agents that did not exist before.

**T-6 · UNCHANGED, INHERITED.** `com.naiad.daily` is untouched, as the contract requires; the
manifest F-4 LAG and the tracked `exchange/.DS_Store` remain as previously reported.

---

## 5 · VERDICT AGAINST BR-1b

ACCEPT iff F-TU-1..6 pass with transcripts, one unattended run completes with the cache advanced
and contiguity intact, and the Oracle's next run reads the fresher bars without any change to
the Oracle itself.

- **F-TU-1..F-TU-6 pass with transcripts** — section 2, 6/6, each shown failing first. ✅
- **One unattended run, cache advanced, contiguity intact** — section 3, exit 0, +10 rows,
  0 gaps across all 40 series. ✅
- **The Oracle reads the fresher bars, unchanged** — as-of moved 2026-08-15T12:00Z →
  2026-08-16T00:00Z; `oracle_daily.py` byte-identical; BR-1 fixtures 10/10. ✅

**ACCEPTED on all three criteria.** The [VETO] row `OVERLAP_BARS` and the T-3 staleness-alarm
ruling remain open, and neither blocks the organ.

---

## 6 · DISPOSITION

BOX constants by import from `publish_exchange` (`BOX_BYTES` = 16,000,000, `FLAG_BYTES` =
64,000). Warn at 40%, refuse ABOVE 70%; the wire flags files strictly over 64,000 B.

| PATH | EXISTS | TRACKED | COMMITTED | PUSHED | PROTECTED BY | BOX COST |
|---|---|---|---|---|---|---|
| `scripts/oracle_topup.py` | yes | yes | `3bdc4c5` | rides this branch push | hand commit, explicit paths (CL-13) | 17,684 B, non-box |
| `scripts/oracle_topup_fixtures.py` | yes | yes | `3bdc4c5` | rides this branch push | same | 17,184 B, non-box |
| `scripts/oracle_wrapper.py` | yes | yes | `3bdc4c5` | rides this branch push | same | 15,902 B, non-box |
| `.gitignore` | yes | yes | `3bdc4c5` | rides this branch push | same | non-box |
| `research_outputs/oracle/topup_scope.json` | yes | yes | `3bdc4c5` | rides this branch push | tracked exception — the scope claim must be auditable in git | 2,843 B, non-box |
| `exchange/queue/2026-08-16_BR1b_oracle_topup_ARGUS.md` | yes | yes | publish | yes | publish guard, `exchange/**` scope | 3,201 B → 0.020% |
| `exchange/reports/BUILD_2026-08-16_ORACLE_TOPUP.md` | yes | yes | publish | yes | same | this file |
| `exchange/status/LEDGER_ARGUS.md` | yes | yes | publish | yes | same, append-only | +~1.6 KB |
| `research_outputs/oracle/calibration/topup_log.jsonl` | yes | **no — gitignored** | — | — | residency block; F-TU-4 proves it never enters exchange/ | 51,418 B, OFF-BUS |
| `~/.cache/naiad/data_cache/klines/*.parquet` (40 in scope) | yes | **no — outside the repo** | — | — | no-clobber (G-TU-2), proven per pair per run | 628 MB estate, OFF-BUS |
| `~/Library/LaunchAgents/com.naiad.oracle-topup-0645.plist` | yes | **no — outside the repo** | — | — | CADENCE registry + section 3.1 undo | 1,068 B |
| `~/Library/LaunchAgents/com.naiad.oracle-topup-1545.plist` | yes | **no — outside the repo** | — | — | same | 1,069 B |

### 6.1 BOX-COST

This build adds roughly **6 KB to the bus at 16,000,000 B** — the queue item, this document and
the ledger append. The organ's actual output is 2,521 rows of market data written to a cache
that lives outside the repo entirely, plus a 51,418 B run log that is gitignored. Nothing this
build produced is over the 64,000 B naming wire.

**Intended homes, per section 3.2.** The kline cache is the estate's substrate and has always
lived at `~/.cache/naiad/data_cache` — this build enlarges it by ~2,500 rows a day and does not
relocate it. `topup_log.jsonl` grows one row per run and is the natural companion to
`selfcheck_log.jsonl` under `research_outputs/oracle/calibration/`; both are gitignored and both
are what BR-2 reads. `topup_scope.json` is tracked deliberately so a scope change shows up as a
diff rather than only as a changed file on disk.

---

## 7 · WHAT THIS BUILD IS NOT

Not a schema change and not a new interval: the top-up refuses to create a parquet that does not
already exist, and fetches nothing outside the enumerated manifest. Not an aggregation — it
counts rows, never outcomes. Not a publisher — `publish_exchange` is not in its import closure
and it writes nothing under `exchange/`. It does not touch `com.naiad.daily`. And it does not
change the Oracle: `oracle_daily.py` is byte-identical to the file BR-1 shipped.

— HEPHAESTUS, 2026-08-16. Reviewed against BR-1b.
