---
name: oracle
description: "Print an edition of The Daily Oracle on demand"
---
Print an edition of The Daily Oracle for the operator, now. The five
`com.naiad.oracle-*` launchd agents were SUSPENDED by operator ruling on 2026-09-21;
this skill is what replaced the clock. It runs the chain the clock ran, as ONE
command, under ONE lock, with ONE exit code (queue OR-1, STEP A).

Pick the verb from what the operator typed (`$ARGUMENTS`):

- `/oracle` — the FULL edition: movers fetch, in-scope top-up, full render.
- `/oracle refresh` — the Watch/Board refresh: SKIPS the movers fetch, still tops up.
- `/oracle --no-fetch` — cache-only: nothing is fetched, and the LATE EDITION band
  under the masthead tells the truth about how old the wire is. Combines with
  either of the other two (`/oracle refresh --no-fetch`).

Run from the repo root, `~/Naiad`. Full edition:

```
~/venvs/naiad/bin/python scripts/oracle_wrapper.py --job ondemand --slot on-demand-full
```

Refresh:

```
~/venvs/naiad/bin/python scripts/oracle_wrapper.py --job ondemand --slot on-demand-refresh
```

Cache-only (append `--no-fetch` to either command):

```
~/venvs/naiad/bin/python scripts/oracle_wrapper.py --job ondemand --slot on-demand-full --no-fetch
```

To see the chain without touching anything — no lock, no flag, no fetch, no render:

```
~/venvs/naiad/bin/python scripts/oracle_wrapper.py --job ondemand --dry-run
```

With the wire down a full edition is SLOW, not stuck: every top-up pair retries
before it gives up (measured 2026-09-21: a fully failing 40-pair top-up took about
10 minutes, and the roster has grown since), and the movers organ is allowed 600 s.
Give the command a long timeout and let it finish; the render is attempted whatever
the fetches did.

## The chain, step by step

Steps 1-7 are performed by the wrapper and logged with the tag `STEP n <id>`.
Steps 8-9 are yours. The ids and their order are `ONDEMAND_STEPS` in
`scripts/oracle_wrapper.py`; fixture F-SK-1 fails if this list and that one differ.
Read the log as it comes and check each step against the lines below.

### STEP 1 · identity-gate

CONVENTIONS §0, both sides: ROOT must be `$HOME/Naiad` AND neither ROOT nor the
working directory may sit in a cloud-synced tree. Expect:

```
  STEP 1 identity-gate: PASS — ROOT /Users/luis/Naiad is $HOME/Naiad; no cloud-tree marker in ROOT or cwd (/Users/luis/Naiad)
```

On `STEP 1 identity-gate: HALT: …` the run exits 2 having touched NOTHING (no
lock, no flag, no fetch, no render). Stop and show the operator the HALT line. Do
not work around it.

### STEP 2 · flag-first

If `ORACLE_DOWN.flag` is standing, its body is printed verbatim BEFORE any work.
Expect one of:

```
  STEP 2 flag-first: no ORACLE_DOWN.flag standing
```

```
  STEP 2 flag-first: ORACLE_DOWN.flag IS STANDING — its body, verbatim, before any work:
  -------- /Users/luis/Naiad/ORACLE_DOWN.flag --------
UTC   <iso>
JOB   <job>
SLOT  <slot>
EXIT  <rc>

LAST <n> TRACEBACK LINE(S), NEWEST FAILURE LAST:
<the traceback tail>

The Oracle is down. Read logs/launchd/oracle-*.log. This file self-clears on the next clean run.
  -------- end of ORACLE_DOWN.flag --------
```

A standing flag does not stop the run. Tell the operator it was standing, and
quote its JOB, SLOT, UTC and last traceback line in your report.

If the next line is `LOCK HELD by … — standing down`, another Oracle run holds the
lock: NO EDITION WAS PRINTED by this run and the exit code is still 0. Say so, wait,
and run again; a lock older than 30 minutes is reclaimed automatically.

### STEP 3 · movers-fetch

The Market Page's fetch: `scripts/oracle_movers.py`, in its OWN process. Expect
one of:

```
  STEP 3 movers-fetch: running oracle_movers.py in its own process (timeout 600 s)
    movers| …the last 12 lines of the movers organ's own output, ending:
    movers|   status OK · universe <n> · 0 error(s) · runtime <s> s · peak used weight <w> per min
    movers|   movers json -> research_outputs/oracle/movers/movers_<date>.json
    movers|   <bytes> B  sha256 <sha>
  STEP 3 movers-fetch: OK (exit 0, <s> s) — /Users/luis/Naiad/research_outputs/oracle/movers/movers_<date>.json <bytes> B
```

```
  STEP 3 movers-fetch: WIRE DOWN for movers — oracle_movers.py exited 1 after <s> s; the Market Page will say so; the edition goes on (a movers failure never fails the edition and never raises the flag)
```

```
  STEP 3 movers-fetch: SKIPPED — refresh edition: Watch/Board only — the Market Page keeps whatever movers json the day already has
  STEP 3 movers-fetch: SKIPPED — --no-fetch: a cache-only edition fetches nothing
```

WIRE DOWN for movers also covers a missing script and a timeout. It is NOT a failed
edition: the page prints "WIRE DOWN — no movers this edition" and the exit code is
untouched. Report it; do not retry it in a loop.

### STEP 4 · scope-topup

The in-scope kline top-up (`oracle_topup`, pinned scope, slot string `on-demand`).
Expect:

```
  STEP 4 scope-topup: slot=on-demand
ORACLE TOP-UP · slot=on-demand · <n> pair(s) from the pinned scope
  BTCUSDT        4h   OK      +    2 rows  newest <iso>  gaps=0
  …one line per pair…
  TOTAL +<n> rows across <n> pair(s); <n> gap(s) across the estate
  top-up PASS: +<n> rows across <n> pair(s), <n> gap(s)
```

With `--no-fetch`:

```
  STEP 4 scope-topup: SKIPPED — --no-fetch: a cache-only edition fetches nothing
```

If the top-up does not PASS — `top-up FAIL: …`, or `TOP-UP HALTED: …` when
`oracle_daily.py` changed since the scope was pinned — the chain says so and GOES ON:

```
  STEP 4 scope-topup: NOT CLEAN (rc 1) — the edition renders anyway, on the cache as it stands (ruling T-3); the banner tells the truth and this run will exit nonzero
```

### STEP 5 · oracle-render

`oracle_daily`, CACHE-ONLY — it never fetches. Render, then the three self-checks,
then ONE row appended to `research_outputs/oracle/calibration/selfcheck_log.jsonl`
tagged `slot="on-demand-full"` or `slot="on-demand-refresh"`. Expect:

```
  STEP 5 oracle-render: slot=on-demand-full
ORACLE on-demand-full · <date> · lens 4h
  posture_canon.json <bytes> B sha256 <sha>
  BTCUSDT        ARMED      heat= 6.248 levels= 35 clusters= 14 atr_d=2376.77
  …one line per roster symbol…
  fired events in the last 24h: <n> across <m> (lens, class) cells
  /Users/luis/Naiad/briefs/oracle/oracle_<date>.html <bytes> B sha256 <sha>
  /Users/luis/Naiad/research_outputs/oracle/tape/oracle_tape_<date>.parquet <bytes> B sha256 <sha>
  /Users/luis/Naiad/research_outputs/oracle/calibration/oracle_calibration_<date>_on-demand-full.json <bytes> B sha256 <sha>
  render /Users/luis/Naiad/briefs/oracle/oracle_<date>.html sha256 <sha>
  selfcheck refresh_idempotence: PASS
  selfcheck thumbnail_provenance: PASS
  selfcheck tape_append_integrity: PASS
  selfcheck log -> /Users/luis/Naiad/research_outputs/oracle/calibration/selfcheck_log.jsonl
```

`RUN FAILED:` followed by a traceback means there is no new render; the row is
still written, with verdict FAIL.

### STEP 6 · front-page

The wrapper's summary of what it just printed. Expect:

```
  STEP 6 front-page:
  FRONT PAGE — top 5 of <n> Board rows by heat
     1  BTCUSDT        ARMED      heat= 6.248
     2  …
  SELF-CHECK VERDICT: PASS — refresh_idempotence PASS · tape_append_integrity PASS · thumbnail_provenance PASS (row slot=on-demand-full)
  RENDER /Users/luis/Naiad/briefs/oracle/oracle_<date>.html · <bytes> B · sha256 <sha>
  BANNER none — no staleness band in this render
```

or, when the cache is stale:

```
  BANNER UP — LATE EDITION — wire stale since <as-of>
```

### STEP 7 · alarm

One exit code (`rc_topup or rc_oracle`), one flag decision, and NO schedule check.
Expect the `STEP 7` line and the `schedule:` line always, then exactly one of the
five that follow:

```
  STEP 7 alarm: rc_topup=0 rc_oracle=0 -> exit 0
  schedule: SUSPENDED by operator ruling 2026-09-21 — the drift check is SKIPPED for job=ondemand (on drift it would rewrite a retained plist and bootstrap it); rollback card research_outputs/oracle/SUSPENDED_2026-09-21.txt
  ALARM CLEARED — ORACLE_DOWN.flag removed by a clean run
  no ORACLE_DOWN.flag standing — nothing to clear
  ALARM RAISED — /Users/luis/Naiad/ORACLE_DOWN.flag
  alarm left standing: ORACLE_DOWN.flag — a --no-fetch run reads the cache only and proves nothing about the wire, so it has no all-clear to give
  no ORACLE_DOWN.flag standing (a --no-fetch run could not have cleared one)
=== exit 0 ===
```

A failed top-up under a clean render exits 1 WITH THE FLAG RAISED: the edition is
on disk and readable, and the alarm about the wire is standing. Both are true;
report both. That run ends:

```
  STEP 7 alarm: rc_topup=1 rc_oracle=0 -> exit 1
  ALARM RAISED — /Users/luis/Naiad/ORACLE_DOWN.flag
=== exit 1 ===
```

### STEP 8 · open-render

Take the path from the `RENDER` line of step 6 and open it (macOS):

```
open /Users/luis/Naiad/briefs/oracle/oracle_<date>.html
```

Skip this only when step 6 printed `RENDER none`. Open the render even when the
exit code is nonzero because of the top-up — ruling T-3: the edition is printed and
its banner tells the truth.

### STEP 9 · report-back

Print back to the operator, from the step 6 block and nothing else: the FRONT PAGE
top rows exactly as logged (symbol, station, heat), the SELF-CHECK VERDICT line, and
the BANNER state.

Notes for the run:
- NEVER run `oracle_wrapper.py --install`, and NEVER `launchctl bootstrap`, `enable`
  or `kickstart` any `com.naiad.oracle-*` label. The clock is SUSPENDED by operator
  ruling; the five plists stay on disk UNEDITED. The rollback card is
  `research_outputs/oracle/SUSPENDED_2026-09-21.txt` and rolling back is the
  OPERATOR's action, never this skill's.
- The Oracle is DISPLAY-ONLY and CACHE-ONLY. It never fetches; the top-up and the
  movers organ fetch, each in its own lane. No gate, filter or sizing reads a range
  or a mover. Do not present a number from the edition as a signal or as advice.
- The exit code is `rc_topup or rc_oracle`. A movers failure NEVER changes it and
  NEVER raises the flag.
- `ORACLE_DOWN.flag` is RAISED by any run ending nonzero, CLEARED only by a run that
  fetched and came back clean, and NEVER cleared by `--no-fetch` — a cache-only run
  proves nothing about the wire.
- The job REFUSES what it does not know: any other `--slot`, or a mistyped flag
  such as `--nofetch`, HALTs with exit 2 and touches nothing. Fix the command;
  do not fall back to `--job oracle` or `--job topup` (those are the clock's jobs
  and they still run the schedule check).
- A same-day re-run OVERWRITES `briefs/oracle/oracle_<date>.html`. That is correct
  behaviour: the edition is a view of the cache, the tape and the selfcheck log are
  the record.
- Do NOT run `scripts/oracle_daily.py` or `scripts/oracle_topup.py` directly to
  "save time": they take no lock, write no selfcheck row and know nothing of the flag.
- The renders, the tape, the movers json and the flag are OFF-BUS (gitignored).
  Nothing this skill produces is committed or pushed.

Report: verb run and exit code; whether a flag was standing at the start (JOB, SLOT,
UTC, last traceback line) and its state at the end (CLEARED, RAISED, left standing,
none); movers OK / WIRE DOWN / SKIPPED; top-up verdict with rows added and gaps, or
SKIPPED; render path, bytes, sha256; the Front Page top rows; the self-check verdict
with the slot tag on its row; the banner state.
