# BUILDERS REPORT — HEPHAESTUS — 2026-08-12 — QUEUE 004 FILED, D-0a BUILT

**Lane:** HEPHAESTUS · **Date:** 2026-08-12 · **Branch:** `v12-v1-census` · **HEAD at start:** `8d9eddf`
**Commissioning lane:** ATHENA · **Scope:** file queue 004, build D-0a **only**.

**Delivered:** `exchange/queue/004_move-clone-out-of-onedrive.md` (filed, ratified) and
`scripts/drive_wait.py` (new, committed `e16de8b`). **No existing script was modified. Nothing was
moved. Nothing was deleted.** D-0b, D-0d and D-0e were not begun.

**Headline finding, and it inverts one line of the contract:** the redraft says the operator "has
since disabled USB selective suspend and disk-sleep on AC, which likely removes the common case."
**Measured, both are still on** — `DISKIDLE` is **30 seconds** on AC *and* battery, and USB
selective suspend is **Enabled** on both. Phase 0 is more necessary than the contract now claims,
not less. §5.

---

## 1 · Part 1 — the contract, filed

Gates, as printed. The third is inverted from the previous session: it now halts if 004 **exists**,
so a re-run cannot clobber a filed contract.

```
pwd=/c/Users/luisf/OneDrive/Desktop/Midas-Claude Code Resources/naiad
branch=v12-v1-census  head=8d9eddf
clone-check=OK
branch-check=OK
no-clobber-check=OK (004 absent, safe to create)
```

Written at **7,725 bytes, 121 lines, LF, UTF-8 clean**.

### 1.1 · The paste's field check reported a false MISSING — the check was wrong, not the file

```
  *** MISSING: RATIFIED: **operator, 2026-08-12** ***     <- from the paste's own loop
  3 RATIFIED stamp line ........ OK                        <- from the README-convention loop
```

Two checks on the same line disagreed, so neither was trusted until the contradiction was resolved.
Cause: `grep` without `-F` reads the argument as a **basic regular expression**, where `**` is a
quantifier, not two literal asterisks. Proof, both forms against the same file:

```
  grep -F : PRESENT
  grep BRE: MISSING  <- the paste's form; ** is a quantifier, not literal asterisks

  line 3 as it landed:
  RATIFIED: **operator, 2026-08-12** — "ratify 004". Drafted ATHENA 2026-08-12; **redrafted the same
```

Re-run with `-F`, **all seven fields present:**

```
  present: RATIFIED: **operator, 2026-08-12**      present: PHASE B
  present: CHANGED AFTER THE OPERATOR              present: Verdict criteria
  present: PHASE 0                                 present: What this phase is NOT
  present: PHASE A
```

**This is the third session running in which a guard misreported a healthy artifact** — the
2026-08-11 line-spanning `.replace()`, yesterday's ledger marker-balance assertion, and now a
markdown stamp checked with an unescaped regex. The pattern is consistent: **every one of these
guards was checking a string containing markdown emphasis.** `**bold**` is regex metacharacters. Any
future paste that greps this project's own prose must use `grep -F`.

### 1.2 · Queue README conventions, all six

```
  1 numbered NNN_slug.md ....... OK        3 RATIFIED stamp line ........ OK
  2 full contract fields ....... OK        5 executor named ............. OK
                                           6 BUILT stamp absent .......... OK (correctly absent)
```

Rule 6 is deliberate: `RATIFIED` says the work may start, `BUILT` says it finished. 004 is ratified
and now partially built; the `BUILT` stamp belongs on the session that completes Phase 0, not this
one. `MANIFEST.json` will count it as `queue_ratified_unbuilt`, which is the truthful state.

### 1.3 · Two contract claims verified against the record

Both hold, and they are the load-bearing ones in "Why this exists":

- **2026-07-27 quota outage** — `LEDGER.md:746`: *"OneDrive outage ROOT-CAUSED: quota exhaustion.
  Registry: ItemCantFitInQuotaLastShown = 2026-07-27T01:05:08Z … against a local tree of 21.78 GB in
  22,731 files."*
- **164 dehydrated files, 2026-08-12** — the census report: *"files walked: 839 DEHYDRATED
  (cloud-only): 164 (299.4 MB no longer on disk)."*

---

## 2 · Part 2 — `scripts/drive_wait.py`, in full

**250 lines, 9,817 bytes**, **ASCII-only** (deliberate: the 2026-08-11 session died on a UTF-8 arrow
printed to a cp1252 console, and this module prints), LF endings, no side effects on import.

Quoted **verbatim from the committed file** — the embedded block and `scripts/drive_wait.py` were
compared by sha256 after the last edit and are byte-identical at 9,817 B. This is the state after
the defect in §2.2, not the state first committed.

```python
#!/usr/bin/env python
"""drive_wait.py -- let an external disk wake up before calling it absent.

D-0a of queue 004.  Ships first, alone, and MEASURES.

THE PROBLEM
  Every D: gate in this project is a single existence check:

      [ -d "D:/Naiad" ] || HALT

  A spun-down external disk returns false in milliseconds, so a single call
  cannot tell "the drive is gone" from "the drive has not spun up yet".  We
  have been treating ASLEEP as ABSENT.  That is the same conflation as the
  2026-08-04 retraction, applied to hardware instead of a task list:

      a single failed lookup measures that lookup, not absence --
      of a file, a task, or a disk.

THE THREE STATES
  PRESENT      reachable on the first attempt.  The common case; costs one
               stat call and logs nothing.
  WOKE         not reachable at first, reachable before the budget ran out.
               THIS is the state that did not exist before, and the only one
               that is logged -- see MEASUREMENT below.
  UNREACHABLE  never reachable within the budget.  The caller halts.

  The states are distinguishable BY DESIGN.  A caller that only wants a
  boolean uses `.ok`; a caller that wants to know whether the disk was asleep
  reads `.state`.

MEASUREMENT
  The attempts/delay defaults below are PROVISIONAL.  Nobody has measured this
  machine's real wake latency -- guessing it is exactly the error this helper
  exists to stop.  So every WOKE appends one line to
  exchange/status/DRIVE_WAKE_LOG.md, and the constants are pinned by a later
  ONE-LINE AMENDMENT to queue 004 once that log holds real observations.
  PRESENT and UNREACHABLE log nothing: a log that grows on the common path is
  noise, and noise is not evidence.

INVARIANTS
  * NEVER raises.  Every filesystem call, the spin-up poke and the log write
    are individually wrapped.  A gate helper that can throw is a new failure
    mode, not a fix for one.
  * A failed poke is NOT an error -- it is the normal cold case.  Poking a
    sleeping disk is how you wake it; the poke is expected to fail while it
    spins up.
  * REACHABLE IS NOT WRITABLE.  This helper answers one question.  Callers
    that need to write still write-probe afterwards, exactly as they do today.
  * No side effects on import.  The log is touched only by a WOKE result.
  * The repo root is resolved from __file__, never hardcoded, so this survives
    queue 004 Phase A moving the clone to C:/Naiad.
  * The result is a frozen dataclass and NOT a NamedTuple.  It was a NamedTuple
    for exactly one build, until F-0-1's own cold probe hit this:

        print("RESULT: %s" % result)
        TypeError: not all arguments converted during string formatting

    A NamedTuple IS a tuple, so %-formatting spreads its six fields across one
    placeholder.  A helper whose headline invariant is NEVER RAISES must not
    hand callers a value that makes THEM raise on an ordinary idiom -- and
    D-0b is about to add nine call sites.  Unpacking is not worth that.

USAGE
    from drive_wait import wait_for_drive

    r = wait_for_drive("D:/Naiad")
    if not r.ok:
        raise SystemExit(f"HALT: {r.root} unreachable after {r.elapsed:.1f}s")
    if r.state == "WOKE":
        print(f"note: drive woke after {r.elapsed:.1f}s")

    $ python scripts/drive_wait.py D:/Naiad
"""

from __future__ import annotations

import dataclasses
import datetime as _dt
import os
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

# --------------------------------------------------------------------------
# PROVISIONAL CONSTANTS -- pinned by a one-line amendment to queue 004 once
# exchange/status/DRIVE_WAKE_LOG.md holds real observations.  Do NOT treat
# these as measured: 6 x 3.0s = 18s worst case is a guess carried over from
# the contract draft, and the whole point of the log below is to replace it.
# --------------------------------------------------------------------------
DEFAULT_ATTEMPTS = 6
DEFAULT_DELAY = 3.0

STATE_PRESENT = "PRESENT"
STATE_WOKE = "WOKE"
STATE_UNREACHABLE = "UNREACHABLE"

REPO = Path(__file__).resolve().parent.parent

# Module-level so a fixture can redirect it without touching the signature.
WAKE_LOG = REPO / "exchange" / "status" / "DRIVE_WAKE_LOG.md"

_LOG_HEADER = """# DRIVE_WAKE_LOG -- measured wake latency for external drives

Written by `scripts/drive_wait.py` (D-0a of queue 004).  ONE line per **WOKE**
result: a drive that was not reachable on the first attempt and became reachable
before the attempt budget ran out.

`PRESENT` and `UNREACHABLE` are deliberately NOT logged -- a log that grows on
the common path is noise, and noise is not evidence.

**Why this file exists:** the `attempts` / `delay` defaults in `drive_wait.py`
are PROVISIONAL.  They are pinned by a one-line amendment to queue 004 once this
log holds real observations.  Until then, an empty log means one of two things,
and they are different: either no drive has ever been found asleep, or the
budget was never long enough to catch one waking.

| date (UTC) | root | attempts used | elapsed s | budget |
|---|---|---:|---:|---|
"""


@dataclass(frozen=True)
class DriveWaitResult:
    """The answer, plus the measurement that produced it.

    Frozen dataclass, deliberately NOT a NamedTuple -- see INVARIANTS above.
    """

    state: str          # PRESENT | WOKE | UNREACHABLE
    root: str           # what was probed, as given
    attempts: int       # attempts actually used (the one that succeeded, or all)
    elapsed: float      # wall-clock seconds spent inside wait_for_drive
    budget: float       # attempts_allowed * delay, for context in the log
    logged: bool        # whether this result appended a DRIVE_WAKE_LOG line

    @property
    def ok(self) -> bool:
        """True for PRESENT and WOKE.  The one thing most callers want."""
        return self.state in (STATE_PRESENT, STATE_WOKE)

    def __str__(self) -> str:
        return (f"{self.state} root={self.root} attempts={self.attempts} "
                f"elapsed={self.elapsed:.2f}s budget={self.budget:.1f}s")


def _reachable(root) -> bool:
    """Does the path resolve right now?  Never raises; any error is False."""
    try:
        return os.path.exists(str(root))
    except Exception:
        return False


def _poke(root) -> None:
    """Nudge the volume so a sleeping disk starts spinning up.

    Listing the drive anchor forces the OS to touch the device.  This is
    EXPECTED TO FAIL while the disk is still spinning up -- that is the normal
    cold case, not an error, so every failure mode is swallowed.
    """
    try:
        anchor = Path(str(root)).anchor or str(root)
        os.listdir(anchor)
    except Exception:
        pass


def _append_wake_log(result: DriveWaitResult) -> bool:
    """Append one line for a WOKE result.  Never raises; returns success."""
    try:
        path = Path(WAKE_LOG)
        path.parent.mkdir(parents=True, exist_ok=True)
        new = not path.exists() or path.stat().st_size == 0
        stamp = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")
        row = (f"| {stamp} | `{result.root}` | {result.attempts} | "
               f"{result.elapsed:.2f} | {result.budget:.1f}s |\n")
        with open(path, "a", encoding="utf-8", newline="\n") as fh:
            if new:
                fh.write(_LOG_HEADER)
            fh.write(row)
        return True
    except Exception:
        # A helper whose job is to prevent false halts must not create one by
        # failing to write its own diary.
        return False


def wait_for_drive(root, attempts: Optional[int] = None,
                   delay: Optional[float] = None) -> DriveWaitResult:
    """Wait for `root` to become reachable.  Never raises.

    Tries `attempts` times.  After each failed try it pokes the volume to
    trigger spin-up and sleeps `delay` seconds -- INCLUDING after the last try,
    so an UNREACHABLE result always spends the full budget and its elapsed time
    is a truthful statement about how long we actually waited.

    Returns a DriveWaitResult.  Check `.ok` for a boolean, `.state` to tell a
    sleeping disk from a missing one.
    """
    try:
        n = DEFAULT_ATTEMPTS if attempts is None else int(attempts)
    except Exception:
        n = DEFAULT_ATTEMPTS
    try:
        d = DEFAULT_DELAY if delay is None else float(delay)
    except Exception:
        d = DEFAULT_DELAY
    n = max(1, n)
    d = max(0.0, d)

    root_s = str(root) if root is not None else ""
    budget = n * d
    start = time.monotonic()

    for i in range(1, n + 1):
        if _reachable(root_s):
            elapsed = time.monotonic() - start
            state = STATE_PRESENT if i == 1 else STATE_WOKE
            result = DriveWaitResult(state=state, root=root_s, attempts=i,
                                     elapsed=elapsed, budget=budget,
                                     logged=False)
            if state == STATE_WOKE:
                result = dataclasses.replace(result,
                                             logged=_append_wake_log(result))
            return result
        _poke(root_s)
        try:
            time.sleep(d)
        except Exception:
            pass

    return DriveWaitResult(state=STATE_UNREACHABLE, root=root_s, attempts=n,
                           elapsed=time.monotonic() - start, budget=budget,
                           logged=False)


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    root = argv[0] if argv else "D:/Naiad"
    result = wait_for_drive(root)
    print(result)
    if result.state == STATE_WOKE:
        print(f"  wake logged to {WAKE_LOG}: {result.logged}")
    return 0 if result.ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
```

### 2.1 · Three design decisions worth stating, because they are not obvious

**UNREACHABLE spends the full budget on purpose.** The loop sleeps after the *last* failed attempt
too. Skipping that sleep would return after `(attempts-1) × delay` and report an elapsed time
shorter than the budget it claims to have spent. The contract's fixture demands
`elapsed >= attempts*delay`, which only holds with the trailing sleep — and it makes the number
honest: **elapsed is a truthful statement of how long we actually waited.** The cost is real and is
raised as an objection in §6.

**The result carries its own measurement.** `DriveWaitResult` is a `NamedTuple` with `state`, `root`,
`attempts`, `elapsed`, `budget`, `logged`. A caller wanting a boolean uses `.ok`; a caller wanting to
distinguish a sleeping disk from a missing one reads `.state`. Returning a bare bool would have
rebuilt the exact conflation this deliverable exists to remove.

**`REPO` is resolved from `__file__`.** `Path(__file__).resolve().parent.parent` — the pattern
already used correctly at `backup_estate.py:148`, and the one the QUEUE-004-HALT report identified as
the model. **Six existing scripts hardcode the absolute OneDrive path and will break at Phase A;
this one will not.**

### 2.2 · A defect shipped and was fixed inside the session — `9f3747d`

The first commit (`e16de8b`) made `DriveWaitResult` a `NamedTuple`. **A `NamedTuple` is a tuple**, so
the ordinary idiom

```python
print("RESULT: %s" % result)
```

spreads its six fields across one placeholder and raises:

```
TypeError: not all arguments converted during string formatting
```

**Found by this session's own cold probe, which does exactly that and died on it.** The helper was
fine; the caller was not — and that is the point. `drive_wait.py`'s headline invariant is **NEVER
RAISES**: it exists so a sleeping disk cannot produce a false halt. Handing callers a return value
that makes *them* raise on a common idiom **reintroduces the failure mode one layer up** — and D-0b
is about to add nine call sites written by whoever takes that session. A crash in a D: gate is
exactly the outcome this deliverable was commissioned to prevent.

Fixed to a `@dataclass(frozen=True)`: same fields, same `.ok`, same `__str__`, still immutable, no
longer a tuple. Tuple unpacking is the only capability lost and nothing used it. F-0-1 gained six
checks that pin the regression directly (§3, section 4b). The reasoning is recorded in the module's
own INVARIANTS block so the next editor does not "simplify" it back.

**Why this is in the report rather than quietly amended:** the paste said Part 2 creates one new
file, and it did — but it took two commits to get right, and the first one is on `origin`. The
honest record is that D-0a shipped with a defect that its own testing caught within the session.

---

## 3 · F-0-1 — the fixture transcript, all three states, measured

**43 checks, 0 failed.** Run standalone, not from `fixtures/` — see §6 objection 3 for why that is a
gap rather than a preference. Transcript below is the final run, after the §2.2 fix; the first run
was 37 checks and also 0 failed, which is precisely why the six new ones in section 4b matter.

```
==============================================================================
F-0-1  drive_wait.py -- three states, measured
==============================================================================
  module   : ...\naiad\scripts\drive_wait.py
  REPO     : C:\Users\luisf\OneDrive\Desktop\Midas-Claude Code Resources\naiad
  WAKE_LOG : ...\naiad\exchange\status\DRIVE_WAKE_LOG.md
  defaults : attempts=6 delay=3.0  (PROVISIONAL)

-- 0 · import has no side effects --
   importing drive_wait did not create WAKE_LOG         PASS   (log absent before any WOKE)

-- 1 · PRESENT (reachable on attempt 1) --
   state == PRESENT                                     PASS   state=PRESENT
   attempts == 1                                        PASS   attempts=1
   ok is True                                           PASS
   logged is False (PRESENT must not log)               PASS
   elapsed is near zero                                 PASS   elapsed=0.0000s
   no sleep incurred                                    PASS   wall=0.0000s

-- 1b · PRESENT against the LIVE external drive D:/Naiad --
   D:/Naiad reachable at test time: True
   D:/Naiad -> PRESENT                                  PASS   state=PRESENT
   D:/Naiad elapsed measured                            PASS   elapsed=0.0000s  attempts=1
   D:/Naiad logged nothing                              PASS

-- 2 · UNREACHABLE (nonexistent drive letter, no exception) --
   probing unused drive letter: Q:/
   no exception raised                                  PASS   raised=None
   state == UNREACHABLE                                 PASS   state=UNREACHABLE
   ok is False                                          PASS
   attempts == budgeted attempts                        PASS   attempts=3 of 3
   elapsed >= attempts*delay                            PASS   elapsed=0.6090s  budget=0.60s
   logged is False (UNREACHABLE must not log)           PASS
   budget reported                                      PASS   budget=0.60s

-- 3 · WOKE (root appears between attempts; log written once) --
   state == WOKE                                        PASS   state=WOKE
   ok is True                                           PASS
   attempts > 1 (was absent at first)                   PASS   attempts=4
   attempts < budget (found before giving up)           PASS   attempts=4 of 6
   elapsed >= appearance delay                          PASS   elapsed=0.5940s  appeared at 0.5s
   logged is True                                       PASS
   log file created                                     PASS
   log line written EXACTLY once                        PASS   rows=1
   log carries a header                                 PASS
   log row carries elapsed                              PASS
   LOG ROW: | 2026-08-12 08:43:24Z | `...\f01_wake_dhnymici\late_volume` | 4 | 0.59 | 1.2s |

-- 3b · a second WOKE appends, and does not re-write the header --
   second WOKE logged                                   PASS   state=WOKE
   header appears exactly once                          PASS
   two data rows now                                    PASS

-- 4 · NEVER RAISES on hostile input --
   no raise: None root                                  PASS   -> UNREACHABLE
   no raise: empty string                               PASS   -> UNREACHABLE
   no raise: illegal chars                              PASS   -> UNREACHABLE
   no raise: negative attempts                          PASS   -> UNREACHABLE
   no raise: garbage attempts                           PASS   -> UNREACHABLE
   no raise: zero delay                                 PASS   -> UNREACHABLE

-- 4b · the result formats without raising --
   regression: DriveWaitResult was a NamedTuple, so '%s' % result spread
   its six fields across one placeholder and raised TypeError. Found by
   the cold probe in section 5 of the report, fixed to a frozen dataclass.
   percent-format does not raise                        PASS   PRESENT root=C:\Users\luisf\OneDrive\Deskt
   percent-format of fields does not raise              PASS   state=PRESENT elapsed=0.0
   str() carries the state                              PASS   PRESENT root=C:\Users\luisf\OneDrive\Deskt
   f-string carries the state                           PASS
   result is NOT a tuple subclass                       PASS   type=DriveWaitResult
   result is frozen (immutable)                         PASS   assignment rejected

-- 5 · the REAL DRIVE_WAKE_LOG was never touched --
   real log still absent                                PASS

==============================================================================
F-0-1: 43 checks, 0 failed
VERDICT: PASS
==============================================================================
```

Beyond the contract's three required states, F-0-1 also asserts **import purity**, **hostile input**
(six forms, including `None`, a NUL byte, and non-numeric `attempts`/`delay` — all return
UNREACHABLE rather than raising), **header-written-once across two WOKEs**, and that **the real
`DRIVE_WAKE_LOG.md` was never touched by a test.** The log was redirected to a temp file before any
WOKE case ran.

### 3.1 · F-0-4 — the full suite, unchanged

```
.........................s.............................................. [ 25%]
........................................................................ [ 50%]
........................................................................ [ 75%]
........................................................................ [100%]
287 passed, 1 skipped in 55.89s
```

**287/1, exactly as before.** A new file under `scripts/` adds no collected items.

---

## 4 · Part 3 — commit

Staged set verified to be exactly one file before committing, as instructed:

```
=== STAGED SET (must be EXACTLY scripts/drive_wait.py) ===
  scripts/drive_wait.py
  staged file count = 1  OK
  identity confirmed OK
```

```
e16de8b ops: queue 004 D-0a - drive_wait helper with three states and self-measurement
  pushed OK
HEAD   : e16de8b     origin : e16de8b
   scripts/drive_wait.py | 233 +++++++++++++++++++++++++++++++++++++++++++++++++
   1 file changed, 233 insertions(+)
```

**Two commits, not one**, because of the §2.2 defect. The staged set was re-verified as exactly one
file before each:

```
9f3747d fix: drive_wait result must not be a tuple - %-formatting raised in the caller
  pushed OK
HEAD=9f3747d  origin=9f3747d
```

The paste's "Part 2 creates ONE new file" was honoured — one file, `scripts/drive_wait.py`, and no
existing script modified. It simply took two commits to make that file correct.

`exchange/queue/004_…md` was deliberately **not** in either commit — it travels via `publish()`, per
the paste's routing.

### 4.1 · The CLI, exercised on both outcomes

```
$ python scripts/drive_wait.py "D:/Naiad"
PRESENT root=D:/Naiad attempts=1 elapsed=0.00s budget=18.0s      exit=0

$ python scripts/drive_wait.py "Q:/"
UNREACHABLE root=Q:/ attempts=6 elapsed=18.00s budget=18.0s      exit=2
```

`elapsed=18.00s` against `budget=18.0s` is the trailing-sleep design of §2.1, confirmed live, and is
the measured basis for §6 objection 2.

---

## 5 · Do the provisional defaults look right? — asked directly, answered honestly

**Short answer: I do not know, and this session could not find out. The defaults remain
unvalidated guesses, and `DRIVE_WAKE_LOG.md` does not exist because nothing has legitimately
written to it.** What follows is what was actually tried.

### 5.1 · F-0-1's `PRESENT` measurement is self-confounded — stated because it looks like evidence

F-0-1 reports `D:/Naiad -> PRESENT, elapsed=0.0000s`. **That number proves nothing about wake
latency.** The fixture calls `os.path.exists("D:/Naiad")` on the line before, to decide whether to
run the case at all — and that call is itself a disk access. The fixture measured a drive it had
just woken. So did the preflight `ls -d D:/Naiad` at the top of the session.

This is the same error the whole deliverable exists to prevent, committed by its own fixture: **a
measurement taken through the thing being measured.** It is not a bug in `drive_wait.py` and F-0-1's
assertions are still valid — PRESENT genuinely means "reachable on attempt 1" — but the *elapsed*
figure must not be read as a wake time.

### 5.2 · The machine settings, measured — and the contract is wrong about them

The contract hedges Phase 0's urgency on this sentence: *"The operator has since disabled USB
selective suspend and disk-sleep on AC, which likely removes the common case."* Probed directly:

```
Power Setting GUID: 6738e2c4-...  (Turn off hard disk after)   GUID Alias: DISKIDLE
      Possible Settings units: Seconds
    Current AC Power Setting Index: 0x0000001e      <- 30 seconds
    Current DC Power Setting Index: 0x0000001e      <- 30 seconds

Power Setting GUID: 48e6b7a6-...  (USB selective suspend setting)
      Possible Setting Index: 000 = Disabled / 001 = Enabled
    Current AC Power Setting Index: 0x00000001      <- ENABLED
    Current DC Power Setting Index: 0x00000001      <- ENABLED

Power Scheme GUID: 381b4222-f694-41f0-9685-ff5bb260df2e  (Balanced)
```

**Neither is disabled, on either power source.** "Turn off hard disk after" is **30 seconds** —
units confirmed from powercfg's own `Possible Settings units: Seconds` line, not assumed. That is an
aggressive setting: on paper the LaCie should be spinning down between essentially every scheduled
job.

### 5.3 · The cold probe — idle past the timeout, then measure once

F-0-1 could not produce a wake because it kept touching the drive. So: idle **150 s** (5× the stated
timeout) with no D: access at all, then one probe with the real defaults.

```
COLD PROBE of D:/Naiad
  disk idle timeout : 30s (powercfg DISKIDLE, AC and DC, units=Seconds)
  idling for        : 150s without touching D:
  defaults          : attempts=6 delay=3.0 (budget 18.0s)
  log exists before : False

  idled 150.0s. probing now (first D: access since).

  RESULT : PRESENT root=D:/Naiad attempts=1 elapsed=0.00s budget=18.0s
  ok     : True
  logged : False
  wall   : 0.0000s
  log exists after : False
```

**PRESENT, on attempt 1, in ~0 s, after 150 seconds of deliberate idleness.** The disk did not spin
down, despite a 30-second timeout that says it should have.

### 5.4 · What that does and does not license

**It does not validate the defaults.** Two probes, both PRESENT, zero WOKE observations. `6 × 3.0 s`
is exactly as unmeasured as it was before this session, and the source says so in a comment naming
the amendment that will replace it. **Anyone reading "F-0-1 PASS" as "the timings are right" is
reading it wrong**, which is why this section exists.

**It does not refute the operator's report either.** The operator reports the LaCie failing to wake
in time; that is a real observation from real use. A 150-second idle on AC mains, with the Google
Drive client running and mirroring `D:/naiad-backups`, is a mild test — far milder than an overnight
gap before a 07:00 scheduled run. The most likely explanation for PRESENT is simply that **something
keeps resetting the idle timer**: the Drive client polls that volume, and any access by any process
restarts the 30-second countdown. A drive that is never idle for 30 seconds never spins down.

**What it does establish, and this is worth having:**

- **The healthy path is free.** PRESENT costs one `os.path.exists` and no sleep — measured at 0.00 s
  in both fixture and cold probe. Wiring `wait_for_drive` into nine call sites adds no measurable
  cost when the drive is awake, which is the overwhelmingly common case. That was the main risk of
  D-0b and it is now retired.
- **The unhealthy path costs the full budget, confirmed live.** `python scripts/drive_wait.py Q:/`
  returned `UNREACHABLE ... elapsed=18.00s`, exit 2. Eighteen seconds, per call site. See §6
  objection 2.
- **The 30-second setting is not producing spin-downs in practice**, which is a genuinely useful
  fact for whoever tunes this: the setting is not the lever it appears to be.

**How the defaults actually get pinned — and it is not by another session like this one.** Contrived
idling on a machine in active use cannot reliably reproduce a cold disk. The observations that
matter come from the **scheduled runs**: the 07:00 daily job after an overnight gap, and the Sunday
weekly jobs. Those are exactly the paths D-0b wires. So the honest sequence is: **wire it (D-0b),
let `DRIVE_WAKE_LOG.md` fill from real unattended runs, then pin the constants by the one-line
amendment the contract already provides for.** That is the design working as intended, and it means
an empty log today is the expected state, not a failure.

**One caveat on that plan, raised as objection 4 in §6:** the log only records WOKE. If the budget is
too short, the run halts UNREACHABLE and writes nothing — so an empty log will still look identical
to "no problem." That gap should be closed when the call sites are wired.

**A cheaper option than any of this, for the operator to weigh:** set `DISKIDLE` to `0` (never) on
AC. One command, no code, and it removes the common case for real rather than by assertion —
which is what the contract currently claims has already been done.

```
powercfg /setacvalueindex SCHEME_CURRENT SUB_DISK DISKIDLE 0
powercfg /setactive SCHEME_CURRENT
```

**Not run.** It changes machine state outside the repo and no such authorization was given.

---

## 6 · Objections

**Nothing in the CHANGED-AFTER-STAMP block was resolved in a way I disagree with.** All seven
objections from the HALT report were adopted, and adopted in the stronger form each time — objection
5 in particular (O-5 removed from Phase 0, so a retention-policy disagreement cannot block a
data-safety move) is exactly right. The objections below are about what the redraft **added**, and
about this session's own gaps.

**1 — D-0e reintroduces the defect that removing O-5 just fixed. [design]**
The redraft removed O-5 from Phase 0 on the principle that an unrelated item must not gate a
data-safety move. **D-0e — the missed-run detector — is new, and lands in Phase 0.** It reads
`HEARTBEAT.md`, enumerates missing `DAILY_*` dates and prints them. It shares no code, no fixture and
no failure mode with waking a disk; its only connection is that both are "things that go wrong
unattended." Phase 0 gates Phase A. **A disagreement about routine reporting can now block the
move — which is precisely the coupling objection 5 was raised to break.** It is a good deliverable.
It should be its own queue item, or Phase 0's D-0b should ship without waiting for it.

**2 — UNREACHABLE costs the full budget at every call site, and D-0b has nine of them. [cost]**
With the current defaults an unreachable drive costs **18 s per call**. That is correct and
deliberate for one gate (§2.1), but D-0b wires nine. A daily routine that hits several D: gates with
the drive genuinely disconnected would spend **minutes** re-establishing the same fact, and the
`--phase` path funnels through `assert_environment()` as well. **D-0b should carry a per-process
memo:** once a root returns UNREACHABLE in a given run, later calls for that same root return the
cached verdict instead of re-paying the budget. Cheap to add, and it belongs in the wiring session
rather than here — but if it is not written into D-0b, the helper will make cold-drive runs slower
in a way that reads as a hang.

**3 — F-0-1 is not committed, so `drive_wait.py` has no regression guard. [coverage]**
The paste required the staged set to be exactly `scripts/drive_wait.py`, and adding a fixture under
`fixtures/` would change the suite count that F-0-4 pins at 287/1. Both constraints are reasonable
and I followed them. The consequence is that **the helper ships with 37 passing checks and zero
permanent protection** — nothing will catch a future edit that breaks the three-state distinction.
The fixture is written and passing; committing it is a one-file change that moves the expected count
to 287+N/1. **Recommend it lands with D-0b**, whose own fixtures will move that count anyway.

**4 — the wake log can only ever record successes, so it cannot prove the budget is long enough.
[measurement]**
By design PRESENT and PRESENT-adjacent results log nothing and UNREACHABLE logs nothing. That keeps
the log clean, and I implemented it as specified. But it means an **empty log is ambiguous in a way
that matters**: either no drive was ever found asleep, or the budget was never long enough to catch
one waking. The state that would prove the budget too short — an UNREACHABLE on a disk that was
merely slow — is the one state that writes nothing. I put that ambiguity in the log's own header so
a future reader meets it, but the honest fix is for **D-0b's call sites to record UNREACHABLE where
they halt**, so the two cases can be told apart later.

**5b — F-0-1 as specified can pass without measuring anything. [drafting]**
The contract asks for "PRESENT on a live root." Any fixture satisfying that literally will have
touched the drive to know it is live — so **the specified fixture cannot distinguish a drive that
was already awake from one it woke itself**, and its elapsed figure is meaningless as a wake time
(§5.1). Mine had this flaw until the cold probe exposed it, and I am reporting it rather than
quietly reporting `elapsed=0.0000s` as if it were evidence. The fixture spec should say what it
actually wants: **a probe taken after a measured idle period with no intervening access.** As
written, F-0-1 passes on a helper that never waits for anything.

**5 — the contract states a machine fact that is false, and it is load-bearing. [correctness]**
§5 above. The claim that USB selective suspend and disk sleep were disabled is the reason Phase 0's
urgency is hedged to "covers battery use, unplug events and USB dropouts." **Measured, neither is
disabled, and disk sleep is 30 seconds on both AC and battery.** The sentence should be struck or
rewritten to match the measurement. This is the same failure class the HALT report flagged in the
first draft — a machine fact asserted rather than probed — and it survived the redraft.

---

## 7 · What remains open, with owners

| # | item | owner |
|---|---|---|
| 1 | **Rule on objection 1** — move D-0e out of Phase 0, or accept that it gates Phase A | ATHENA |
| 2 | **Strike or rewrite the power-settings sentence** in Phase 0; optionally set `DISKIDLE` to 0 on AC, which would remove the common case for real | ATHENA drafts · operator decides |
| 3 | Per-process UNREACHABLE memo, written into D-0b before the nine sites are wired | HEPHAESTUS, D-0b session |
| 4 | Commit F-0-1 into `fixtures/`, accepting the new suite count | HEPHAESTUS, D-0b session |
| 5 | Pin `DEFAULT_ATTEMPTS` / `DEFAULT_DELAY` by one-line amendment once `DRIVE_WAKE_LOG.md` holds observations | ATHENA |
| 6 | D-0b (9 wiring points), D-0d (one line into the residency notes), D-0e — all unbuilt | HEPHAESTUS, on the operator's go |
| 7 | Carried unchanged from the HALT report: O-5 widening, the two stale `_archive` paths, O-6's `G:` destinations | ATHENA / operator |

---

## 8 · Publish and rollback

**Rollback.** `git checkout -- exchange/queue/` removes the filed contract. `git revert 9f3747d
e16de8b` removes `drive_wait.py` — **both commits, newest first**, since the second corrects the
first. The contract and the script are independent and either can be reversed alone. No existing
file was modified by Part 2, so there is nothing else to undo.

### 8.1 · The ledger append, and a second false-failing assertion

The append ran under the usual discipline — whole-file read, context printed, assertions after.
**Eleven assertions, ten PASS, one FAIL:**

```
   ATHENA blocks +1                   PASS      both commits named               PASS
   closers == blocks + template       PASS      report filename referenced       PASS
   file ends on a terminated block    PASS      exactly one NEXT added   *** FAIL ***
   new NEXT present                   PASS      file grew                        PASS
   contract-refuted fact present      PASS      line endings preserved           PASS
   in-session defect recorded         PASS

   bytes 36710 -> 41368  (+4658)   CRLF=0  ATHENA blocks=15  template=1
```

**Again the check was wrong, not the file.** `count("NEXT: Rule on item 1") == 1` is a *whole-file*
count, and a lane ledger is an append-only diary of near-identical entries. That phrase already
appeared twice from earlier sessions:

```
  line  250| NEXT: Rule on item 1; the rescue is the only option that removes risk...
  line  288| NEXT: Rule on item 1; it is the only remaining file with no copy anywhere...
  line  354| NEXT: Rule on item 1, then give the go for D-0b. Owner: ATHENA.   <- mine
```

Re-asserted against the appended block alone (lines 334–357), everything passes:

```
   exactly one NEXT in MY block     PASS      my block terminated       PASS
   my NEXT is the D-0b one          PASS      7 PENDING items           PASS
   my block has one METRICS         PASS      prior entry untouched     PASS
```

**Nothing was corrected in the file, because nothing in the file was wrong.** Yesterday's session hit
the same class on the same file (the blank `STATUS_<LANE>` template making closers outnumber
openers). The standing lesson, now twice paid for: **assertions on an append-only ledger must be
scoped to the appended block, never counted across the whole file.**

**Publish output, as printed:**

<<PUBLISH>>

---

## 9 · File-disposition table (§3.2)

| PATH | EXISTS | TRACKED | COMMITTED | PUSHED | PROTECTED BY | BOX COST |
|---|---|---|---|---|---|---|
| `exchange/queue/004_move-clone-out-of-onedrive.md` | yes | tracked (new) | this session's publish | yes — `origin/v12-v1-census` | GitHub + estate zip | **7,725 B — 0.121%** of the 6.39 MB box |
| `scripts/drive_wait.py` | yes | tracked (new) | **`e16de8b`**, corrected by **`9f3747d`** | yes — `origin/v12-v1-census` | GitHub + `--workflow` archive (`scripts/` is a WORKFLOW_SOURCE) | **n/a — outside `exchange/`**, does not enter the box. 250 lines, 9,817 B |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-12_QUEUE-004-FILED-AND-D0A.md` | yes | tracked (new) | this session's publish | yes | GitHub + estate zip | ~24 KB — ~0.37% (stated rounded: a file cannot carry its own exact size or sha256) |
| `exchange/status/LEDGER_ATHENA.md` | yes | tracked | this session's publish | yes | GitHub + estate zip | append, see §10 |
| `exchange/status/DRIVE_WAKE_LOG.md` | see §5 | — | — | — | — | created only by a real WOKE; F-0-1 redirected its log and never touched this path |
| `scripts/backup_estate.py`, `daily_routine.py`, `archive_dependencies.py`, `reviewer_manifest.py` | yes | tracked, **unchanged** | unchanged | unchanged | GitHub + `--workflow` archive | **0 — D-0b is its own session** |
| `exchange/status/CONVENTIONS.md` | yes | tracked, **unchanged** | unchanged | unchanged | GitHub + estate zip | 0 — D-0d targets the residency notes, not this file |
| `C:/Naiad` | **no** | n/a | — | — | — | n/a — Phase A not begun; nothing moved |

No other file was created, modified, moved or deleted.

---

## 10 · Status

**Queue 004 is filed and ratified. D-0a is built, committed `e16de8b`, and passing 37/37 with the
suite unchanged at 287/1.** Phase 0 is not complete: D-0b, D-0d and D-0e remain, and each is its own
session on the operator's go. Phase A and Phase B were not begun and must not be until Phase 0 is
accepted.
