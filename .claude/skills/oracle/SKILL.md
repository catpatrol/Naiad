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

Run from the repo root, `~/Naiad`, and run it DETACHED: start the command with the
Bash tool's `run_in_background: true`, unbuffered (`python -u`), appending to the
edition's own log, and read that log while it grows. NEVER run an edition that
fetches under a foreground timeout. Full edition:

```
~/venvs/naiad/bin/python -u scripts/oracle_wrapper.py --job ondemand --slot on-demand-full >> logs/launchd/oracle-ondemand.log 2>&1
```

Refresh:

```
~/venvs/naiad/bin/python -u scripts/oracle_wrapper.py --job ondemand --slot on-demand-refresh >> logs/launchd/oracle-ondemand.log 2>&1
```

Cache-only (append `--no-fetch` to either command; it renders in well under a
minute, but start it the same way — one habit, one log):

```
~/venvs/naiad/bin/python -u scripts/oracle_wrapper.py --job ondemand --slot on-demand-full --no-fetch >> logs/launchd/oracle-ondemand.log 2>&1
```

Then follow the run. The log is APPENDED to, so read from the LAST
`=== ORACLE WRAPPER · job=ondemand` line down; the run is over when that block ends
in an `=== exit N` line (the harness also tells you when the background command
exits, with the same code):

```
tail -n 120 logs/launchd/oracle-ondemand.log
```

To see the chain without touching anything — no lock, no flag, no fetch, no render
(this one prints a dozen lines and may run in the foreground):

```
~/venvs/naiad/bin/python scripts/oracle_wrapper.py --job ondemand --dry-run
```

WHY DETACHED. With the wire down a full edition is SLOW, not stuck: every top-up
pair retries before it gives up. MEASURED: a fully failing 40-pair top-up took
10 min 19 s on 2026-09-21 (09:45:03Z -> 09:55:22Z) and again on 2026-09-20; the
pinned scope has since grown to 72 pairs, which at that rate is about 19 minutes,
and the movers organ is allowed 600 s before it. A CLEAN 40-pair top-up took
2 min 29 s (2026-09-19), so about 4.5 minutes for 72. The Bash tool's foreground
ceiling is 600000 ms and its default is 120000: a clean full edition already
overruns the default, and a wire-down one CANNOT finish under the ceiling. The
render is attempted whatever the fetches did (ruling T-3) — but only if the run is
still alive to attempt it.

WHAT A CUT-OFF RUN LEAVES BEHIND, and what to tell the operator:

- Cut off POLITELY (SIGTERM or SIGHUP — a timeout, a closed session): the chain says
  so, releases its lock, RAISES THE FLAG and exits 128+signal. Expect:

```
  CUT OFF by signal 15 (SIGTERM) during STEP 4 scope-topup — NO EDITION WAS PRINTED by this run and no selfcheck row was written; the lock is released and the run exits 143. Run it again DETACHED (.claude/skills/oracle/SKILL.md): with the wire down a full edition outlives any foreground timeout
  STEP 7 alarm: rc_topup=0 rc_oracle=0 -> exit 143
  ALARM RAISED — /Users/luis/Naiad/ORACLE_DOWN.flag
=== exit 143 ===
```

- Cut off HARD (SIGKILL, power loss): nothing is said, NO flag is raised, NO selfcheck
  row is written, and `logs/launchd/.oracle.lock` is left on disk. The log block
  simply stops with no `=== exit` line. The NEXT on-demand run reclaims a lock whose
  pid is not running and goes on:

```
  DEAD LOCK from ondemand/on-demand-full (pid <pid> is not running — that run was cut off before it could release; stamped <iso>) — reclaiming it
```

  A lock whose pid IS running is another edition in progress: `LOCK HELD by …`
  (step 2 below), for at most `LOCK_STALE_MIN` = 30 minutes. NEVER delete the lock
  by hand while its pid is alive.
- Tell the operator, in these words: the run was CUT OFF at step <n>, NO EDITION
  was printed (or: the edition was already on disk), whether the flag is standing,
  and that you are running it again detached — or `/oracle --no-fetch` if they
  want a cache-only edition NOW and the wire can wait.

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
lock and its pid is RUNNING: NO EDITION WAS PRINTED by this run and the exit code is
still 0. Say so, wait for that run, and run again; a lock older than 30 minutes is
reclaimed automatically. A lock left by a run that is no longer running never gets
this far — it is reclaimed on the spot with a `DEAD LOCK from …` line (see WHAT A
CUT-OFF RUN LEAVES BEHIND).

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
  edition Vol. I · No. <n> · Morning Edition
  /Users/luis/Naiad/briefs/oracle/oracle_<date>.html <bytes> B sha256 <sha>
  /Users/luis/Naiad/research_outputs/oracle/tape/oracle_tape_<date>.parquet <bytes> B sha256 <sha>
  /Users/luis/Naiad/research_outputs/oracle/calibration/oracle_calibration_<date>_on-demand-full.json <bytes> B sha256 <sha>
  render /Users/luis/Naiad/briefs/oracle/oracle_<date>.html sha256 <sha>
  selfcheck refresh_idempotence: PASS
  selfcheck thumbnail_provenance: PASS
  selfcheck tape_append_integrity: PASS
  selfcheck log -> /Users/luis/Naiad/research_outputs/oracle/calibration/selfcheck_log.jsonl
```

The `edition` line reads `Refresh Edition` on `on-demand-refresh`. `RUN FAILED:`
followed by a traceback means there is no new render; the row is still written,
with verdict FAIL.

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
  OPERATOR's action, never this skill's. Beside the on-demand job the wrapper
  refuses it for you — `HALT: --job ondemand REFUSES --install. …`, exit 2, nothing
  touched — but `--install` typed ALONE is still the clock's arming verb and still
  arms all five. Do not type it.
- ALWAYS DETACHED (`run_in_background: true`, `python -u`, the log at
  `logs/launchd/oracle-ondemand.log`). A foreground timeout that fires mid-chain
  ends the run before the render; see WHAT A CUT-OFF RUN LEAVES BEHIND.
- The Oracle is DISPLAY-ONLY and CACHE-ONLY. It never fetches; the top-up and the
  movers organ fetch, each in its own lane. No gate, filter or sizing reads a range
  or a mover. Do not present a number from the edition as a signal or as advice.
- The exit code is `rc_topup or rc_oracle`. A movers failure NEVER changes it and
  NEVER raises the flag.
- `ORACLE_DOWN.flag` is RAISED by any run ending nonzero (a CUT OFF run included),
  CLEARED only by a run that fetched and came back clean, and NEVER cleared by
  `--no-fetch` — a cache-only run proves nothing about the wire. The flag's own last
  sentence says "self-clears on the next clean run"; a clean `--no-fetch` edition is
  NOT that run, and its log says so (`alarm left standing: …`).
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

Report: verb run and exit code (or CUT OFF at which step, and whether an edition was
printed); whether a flag was standing at the start (JOB, SLOT, UTC, last traceback
line) and its state at the end (CLEARED, RAISED, left standing, none); a DEAD LOCK
reclaimed, if one was; movers OK / WIRE DOWN / SKIPPED; top-up verdict with rows
added and gaps, or SKIPPED; render path, bytes, sha256; the Front Page top rows; the
self-check verdict with the slot tag on its row; the banner state.
