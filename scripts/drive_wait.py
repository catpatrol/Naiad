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

import datetime as _dt
import os
import sys
import time
from pathlib import Path
from typing import NamedTuple, Optional

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


class DriveWaitResult(NamedTuple):
    """The answer, plus the measurement that produced it."""

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
                result = result._replace(logged=_append_wake_log(result))
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
