# BUILDERS REPORT — HEPHAESTUS — 2026-08-12 — QUEUE 004 PHASE 0 COMPLETE

**Lane:** HEPHAESTUS · **Date:** 2026-08-12 · **Branch:** `v12-v1-census` · **HEAD at start:** `dea01d4`
**Commissioning lane:** ATHENA · **Operator go:** *"wire it & phase A"*, 2026-08-12.

**Phase 0 is complete and green in the current tree.** D-0b wired 8 gates, D-0e built, D-0d filed,
the two stale `_archive` paths fixed. Code in one commit, **`20ad593`**.

**PHASE A WAS NOT BEGUN.** The operator's go said "& phase A"; the reviewer's methodological split
holds it back to its own session so that a failure after the move has exactly one possible cause.
**Nothing was copied to `C:/Naiad`. Task Scheduler was not touched. Nothing was deleted.**

**The finding that justifies the whole phase, measured live:** `HEARTBEAT.md` read
**`phase: NONE`** before this session and **`phase: 2026-08-02`** after — it had been reporting no
phase archives while **nine, totalling 1,043.6 MB**, sat on the drive. §4.

---

## 1 · What already existed vs what this session created

Step 0 enumerated before assuming, and found both prerequisites already built — so neither was
rewritten.

| thing | state at session start | this session |
|---|---|---|
| `exchange/queue/004_…md` | **PRESENT**, 7,725 B, ratified, committed `cc02307` | **left byte-untouched** |
| `scripts/drive_wait.py` | **PRESENT**, 250 lines, committed `e16de8b` + `9f3747d` | **left byte-untouched** (still 250 lines, still a frozen dataclass — asserted) |
| references to `wait_for_drive` | **only `drive_wait.py` itself** — built but not wired | **8 call sites wired** |
| `drive_ready()` helper | absent | **created** in `backup_estate.py` |
| D-0e missed-run detector | absent | **created** in `daily_routine.py` |
| D-0d rule in residency notes | absent | **filed**, published `89c849f` |
| `exchange/status/DRIVE_WAKE_LOG.md` | absent | **still absent** — see §6 |

Steps 1 and 2 were correctly skipped. Working code was not rewritten.

---

## 2 · D-0b — the D: site enumeration, with a verdict on every site

The paste's grep finds string *literals*; the actual gates are `.exists()` / `.is_dir()` / `.glob()`
calls elsewhere, so the enumeration was rebuilt from a reachability-shaped scan of all four files
and each site classified. **Every site is either WIRED or explicitly out-of-scope with a reason.**

### 2.1 · WIRED — 8 sites

| # | site (post-edit line) | what it gates | why it mattered |
|---|---|---|---|
| 1 | `backup_estate.py:412` `assert_environment()` | the write probe **all three modes** funnel through (`--estate`, `--workflow`, `--phase`) | a sleeping disk was judged unwritable before it could wake. Reachable is still not writable — the probe below it is unchanged and remains the real test |
| 2 | `backup_estate.py:473` `phase_archive_root()` | `--phase` halt gate | the original ruling-B gate |
| 3 | `backup_estate.py:506` `backup_dest_root()` | `--estate` / `--workflow` halt gate | the two irreplaceable archives |
| 4 | `backup_estate.py:1052` `_generations()` | **estate + workflow retention sections** | **was completely UNGATED** — see §2.2 |
| 5 | `backup_estate.py:1123` `retention_report()` phase half | phase archive enumeration | O-4's gate, now waiting instead of single-shot |
| 6 | `daily_routine.py:496` `check_reminders()` | **the 07:00 unattended gate** | the job that runs most often, after the machine has been idle all night. This is the one that alarmed "backup destination unreachable" on a drive that was merely asleep |
| 7 | `daily_routine.py:557` phase set date | heartbeat's phase figure | **stale path** — §4 |
| 8 | `archive_dependencies.py:61` archive membership | `docs/ARCHIVE_DEPENDENCIES.md` | **stale path** — §4 |

My previous census called the minimum correct set **9**. It is **8 call sites**, and the ninth is
accounted for rather than dropped: the old `if not arch.is_dir()` branch (formerly `:1072`) sits
*downstream* of site 5's wait, so by the time it runs the drive is already confirmed present. It
needs no wait of its own and correctly means "mounted, but the directory does not exist yet."
**Subsumed, not omitted.**

### 2.2 · The site that was never gated at all

`_generations()` — the estate and workflow half of the retention report — had **no reachability
check of any kind**:

```python
try:
    gens = sorted((p for p in dest.glob(pattern) if p.is_file()), ...)
except OSError as exc:
    return out + [f"- could not read the destination: {exc}"]
if not gens:
    return out + ["- none found"]
```

**An unmounted drive does not raise `OSError` — `dest.glob()` simply yields nothing.** So the report
printed **"- none found"** for four perfectly good archives sitting on an unplugged disk. Ruling O-4
gave the *phase* section three distinct states and forbade it from ever saying "none found" when it
could not look — and left this half untouched. **Same conflation, same file, one function higher up.**

Now the three states are distinct here too: unreachable prints **NOT ENUMERABLE**, reachable-and-empty
prints "none found — the drive is reachable and holds no matching archive."

**The wait is resolved ONCE, not per section.** Two `_generations()` calls with a per-section wait
would pay the budget twice for the same drive.

### 2.3 · OUT-OF-SCOPE — classified, not skipped

| site | verdict | reason |
|---|---|---|
| `backup_estate.py:250` `PHASE_ARCHIVE_ROOT_DEFAULT`, `:277` `BACKUP_DEST_DEFAULT` | **not a gate** | string constants; they perform no check |
| `backup_estate.py:445` `phase_archive_root_path()`, `:501` `--dest` precedence | **not a gate, deliberately** | pure resolvers. O-4 split them out precisely so `retention_report()` could resolve a path *without* halting. Adding a wait here would make a resolver block |
| `scripts/routine_jobs.json:9` `"backup_dest"` | **data, not code** | consumed at `daily_routine.py:488` and gated at site 6 |
| `backup_estate.py:538` `mirror_phase_outputs()` `mkdir` | **NOT WIRED — flagged** | `--mirror` takes an arbitrary operator-supplied drive and is reachable only via an explicit interactive `--phase --mirror`; no scheduled task uses it. It is the one reachability-shaped D:-capable site left unwaited. **Open item §7.3** |
| every `G:` gate | **excluded by ruling** | see §2.4 |
| `_generations()` `-NN` grouping + same-day sort inversion | **excluded — O-5** | a retention-policy question, not a gate defect. Explicitly asserted untouched |

### 2.4 · The G: exclusion is declared, because it cannot be detected

The instruction was to exclude G: gates — a Drive mount is not a sleeping disk, and waiting cannot
start a client that is not running. I tried to implement that as a *property* rather than a
hardcoded letter, and **measured that it cannot be**:

```
  C:\  -> 3 (FIXED)
  D:\  -> 3 (FIXED)      <- the LaCie, a physical external disk
  G:\  -> 3 (FIXED)      <- the Google Drive virtual mount
  Q:\  -> 1 (NO_ROOT_DIR)
```

`GetDriveTypeW` reports the Drive mount as a fixed local disk, **indistinguishable from the LaCie**.
Worse, an *absent* drive returns `NO_ROOT_DIR` whatever it used to be — and absence is exactly the
case needing classification. So the exclusion is a declared list, overridable via
`NAIAD_NO_WAIT_ANCHORS`, with the measurement recorded in the source so nobody re-attempts detection:

```python
NO_WAIT_ANCHORS_DEFAULT = "G:\\"
NO_WAIT_ANCHORS_ENV = "NAIAD_NO_WAIT_ANCHORS"
```

This matters concretely: **the two Sunday tasks still pass `--dest "G:\My Drive\naiad-backups"`**
(open item O-6, unchanged — Task Scheduler was not modified). Without the exclusion they would wait
18 s on the wrong drive before an inevitable halt.

### 2.5 · The helper

```python
def drive_ready(root: Path, note=print):
    """Is `root`'s drive reachable?  Waits for a sleeping disk.  Never raises.

    D-0b.  Replaces the bare `anchor.exists()` that every D: gate used to run.
    A single existence check returns False in milliseconds on a spun-down
    external disk, so it cannot tell "the drive is gone" from "the drive has
    not spun up yet" -- and we were reading the second as the first.

    Returns (ok, detail) where detail is a human-readable measurement suitable
    for appending to a halt message.  Anchors in NO_WAIT_ANCHORS are probed
    once, exactly as before, and never waited on.
    """
    anchor = Path(root.anchor) if root.anchor else None
    if anchor is None:
        return True, "no drive anchor to check"
    if str(anchor).upper() in _no_wait_anchors():
        ok = anchor.exists()
        return ok, (f"{anchor} probed once (no-wait anchor; a Drive mount is not "
                    f"a sleeping disk)")
    r = wait_for_drive(anchor)
    if r.state == "WOKE":
        note(f"drive {anchor} was asleep and WOKE after {r.elapsed:.2f}s "
             f"(attempt {r.attempts} of {r.attempts})")
    return r.ok, (f"{anchor} {r.state} after {r.elapsed:.2f}s "
                  f"({r.attempts} attempt(s), budget {r.budget:.1f}s)")
```

Two deliberate choices. **It returns a `detail` string** rather than just a boolean, so every halt
message now carries the measurement that produced it — a halt that says *"UNREACHABLE after 18.00s,
6 attempts"* is auditable in a way that *"not mounted"* never was. **`note` is injectable** because
`retention_report()` and the two stale-path sites build report lines; a bare `print` there would
inject a WOKE notice into the middle of another function's output.

---

## 3 · `scripts/drive_wait.py` — unchanged this session, reproduced in full

Committed `e16de8b`, corrected `9f3747d`. **Not modified by this session** (asserted: still 250
lines, still `@dataclass(frozen=True)`). Reproduced because §3.1 requires this document to stand
alone with zero prior context.

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

---

## 4 · The two stale paths — a defect fixed once, surviving in two more files

Ruling O-4 fixed `backup_estate.py`'s retention scan, which had been reading
`REPO/research_outputs/_archive` — a directory that stopped holding archives on **2026-08-06**, when
ruling B moved them off-machine and left only the sidecars behind. **The same line existed in two
other files and was never fixed.**

```python
# daily_routine.py, before
arch = ROOT / "research_outputs" / "_archive"

# archive_dependencies.py, before
arch_dir = REPO / "research_outputs" / "_archive"
```

**Measured consequence, before and after, same machine, same drive:**

```
BEFORE   archives — estate: 2026-08-11 · workflow: 2026-08-12 · phase: NONE
AFTER    archives — estate: 2026-08-11 · workflow: 2026-08-12 · phase: 2026-08-02
```

`phase: NONE` was not a missing archive. **Nine phase archives totalling 1,043,591,544 B (1,043.6 MB)
were on the drive the whole time** — `tc1`, `tc4`, `tc5`, `v3_anchor` and five more, all enumerated
by the `--workflow` run in §5.2. The heartbeat — the file whose entire job is to say whether this
project's protection is healthy — has been reporting the phase estate as absent for six days.

`archive_dependencies.py` had the same defect with a quieter symptom: its "archived in" column
silently went blank, so `docs/ARCHIVE_DEPENDENCIES.md` has been claiming components live in no
archive at all. Both now resolve the same root `--phase` writes to, through the same waiting gate,
and both print **NOT ENUMERABLE** rather than a blank when the drive is unreachable.

---

## 5 · Step 6 — THE BASELINE. Phase A must reproduce these exactly from `C:/Naiad`

**These are the numbers Phase A's acceptance is measured against.**

### 5.1 · (a) Full test suite

```
287 passed, 1 skipped in 84.06s
```

**BASELINE: 287 passed / 1 skipped.** Unchanged by 238 inserted lines across three scripts.

### 5.2 · (c) `backup_estate.py --workflow` through the new gate

First invocation halted on the no-clobber guard — correct behaviour, today's archive already
existed — so it was re-run with `--force-same-day`:

```
destination      : D:\naiad-backups   (no --dest given; from built-in default)
destination      : D:\naiad-backups\naiad_workflow_2026-08-12-02.zip
roots archived   : 12 dir(s) + repo-root *.md
members to archive: 349
  verifying (bidirectional)...
    verified 349/349
  PASS F-K1  - 349/349 members verified both directions; 0 mismatches, 0 strays, 0 omissions
  PASS F-K4  - 10 members restored outside repo; 0 hash mismatches
  PASS F-K5  - re-read from destination: sha256 b286c5d8ae64d3bc... matches=True,
               sidecar matches=True, CRC clean=True, 349 members
  PASS F-K6b - --force-same-day correctly does NOT apply to an older archive
archive   : D:\naiad-backups\naiad_workflow_2026-08-12-02.zip
sha256    : b286c5d8ae64d3bcb7c927c641a96ec2c787d9d0816a5aa60d612bfac1adaf3b
members   : 349
EXIT CODE = 0
```

**BASELINE: 349 members, 0 mismatches, 0 strays, 0 omissions, 4/4 fixtures, exit 0.**

And the phase section, proving site 5's gate resolved the real root:

```
Location: `D:\Naiad\research_outputs\_archive`
9 archive(s), 1,043,591,544 B (1,043.6 MB). **All permanent. None prunable.**
```

### 5.3 · (b) Daily routine end-to-end

```
  manifest:       exit=0  elapsed=3.2s
  brief:          exit=0  elapsed=264.9s
  brief2_capture: exit=0  elapsed=0.0s
  brief2_panel:   exit=0  elapsed=1.2s
  ACTION REQUIRED: 6 item(s) overdue
wrote exchange/status/daily/DAILY_2026-08-12.md
EXIT CODE = 0
```

**BASELINE: exit 0, all 4 jobs exit 0, HEARTBEAT regenerated at 2026-08-12T10:16:17Z with
`phase: 2026-08-02`.**

**The MISSED RUNS banner correctly printed nothing** — a run completed earlier today, so there is no
gap. That is D-0e's common path working: no gap, no noise. The report opens straight into
`## 0. ACTION REQUIRED` exactly as before.

### 5.4 · (d) `DRIVE_WAKE_LOG.md`

**Does not exist. No WOKE has ever occurred.** Every probe in this session — F-0-1, the cold probe,
eight wired gates across a full routine and a full workflow backup — returned **PRESENT on attempt 1
at ~0.00 s.** §6 states what that does and does not license.

---

## 6 · Do the provisional constants survive contact with the real drive?

**Asked directly, answered directly: they have still never been tested, and the honest position is
unchanged from the D-0a session — but the evidence that they are* harmless* is now much stronger.**

**What is now proven:** the healthy path is genuinely free. Eight gates now sit in front of every
D: access in the daily routine and the workflow backup. The routine's non-brief jobs ran in 3.2 s,
1.2 s and 0.0 s; the 264.9 s belongs to `brief`, which does market work and touches no gate. **Adding
eight waits changed no measurable timing anywhere.** That was the main risk of D-0b — that wrapping
every gate would slow the common path — and it is now retired with numbers.

**What is still not proven:** `6 × 3.0 s = 18 s` remains a guess. The drive has never been observed
asleep, so no observation constrains the budget. The previous session established why: `DISKIDLE` is
30 seconds on this machine, yet a deliberate 150-second idle still returned PRESENT — something (most
likely the Google Drive client mirroring `D:\naiad-backups`) keeps resetting the idle timer.

**The one number that is real:** an unreachable drive costs exactly the budget, confirmed live —
`drive_wait.py Q:/` returns `UNREACHABLE, elapsed=18.00s`, exit 2. With eight gates that is the cost
worth watching, and it is why §7.2 matters.

**My view: leave the constants alone and let the scheduled runs decide.** Pinning them now would
substitute a second guess for the first. The runs that will actually catch a cold disk are the 07:00
daily after an overnight gap and the Sunday weeklies — all of which now pass through a gate that
records what it saw. **An empty `DRIVE_WAKE_LOG.md` today is the expected state, not a failure.**
The one caveat, carried from the D-0a session and still open: the log records only WOKE, so it cannot
distinguish "never asleep" from "budget too short" (§7.4).

---

## 7 · Findings reported, NOT fixed — and what remains open

**7.1 · My own proof run made O-5 measurably worse. [disclosure]**
`--force-same-day` wrote `naiad_workflow_2026-08-12-02.zip`, a **third** same-day archive. The
retention report now reads **8 workflow generations, 4 within the rule, 4 outside** — and three of
the four keep-slots are all 2026-08-12. Two genuinely distinct older days sit "outside the rule"
because one calendar day occupies three slots. Nothing was deleted and the report never deletes, but
**the symptom O-5 describes is now three-deep instead of two.** Owner: ATHENA.

**7.2 · No per-process UNREACHABLE memo. [carried, now higher stakes]**
Raised in the D-0a report; unchanged, and eight gates now exist rather than one. With the drive
genuinely disconnected, a single daily routine can pay 18 s at `check_reminders()`, again at the
phase-date lookup, and again per backup mode. Nothing caches the verdict within a run. **This should
land before anyone reports a cold-boot run as "hung".** Owner: HEPHAESTUS, next session.

**7.3 · `mirror_phase_outputs()` is the one D:-capable site left unwaited.**
`backup_estate.py:538`. Deliberate (§2.3) — arbitrary operator-supplied path, interactive-only, no
scheduled task reaches it — but it is an inconsistency and I am naming it rather than leaving it to
be discovered. Owner: HEPHAESTUS.

**7.4 · The wake log still records only successes. [carried]**
An empty log cannot distinguish "never asleep" from "budget too short", because the state that would
prove the budget too short is the one state that writes nothing. Owner: ATHENA.

**7.5 · F-0-1 and F-0-3 are still not committed as regression tests.**
Both pass — 43 and 28 checks — but both run standalone from the scratchpad, so **nothing protects
`drive_wait.py`, `drive_ready()` or the missed-run detector from a future edit.** Adding them to
`fixtures/` moves the suite count off 287/1, which is why it did not happen inside a session whose
job was to prove that number unchanged. **It should happen in the session immediately after Phase A**,
once the baseline has served its purpose. Owner: HEPHAESTUS.

**7.6 · The publish budget WARNING could not be cleared.**
The paste required the publish to show "no budget WARNING". `exchange/` is at **26.0%** against a
25% warn line, and the only mechanism that lowers it — report rotation — is **queue 003, ratified
2026-08-11 and still unbuilt.** I could not satisfy that requirement without building an unrelated
ratified contract inside this session. The warning is shown, not suppressed, per the paste's own
parenthetical that rotation is the answer to WARN rather than silence. Owner: operator, to schedule
003.

**7.7 · Carried unchanged:** O-6 (both Sunday tasks still pass `--dest "G:\…"`; Task Scheduler not
modified this session, by instruction), O-7, O-8.

---

## 8 · Edit discipline — enumerate, context, assert

Ten edits across four files. Every one was a whole-content string replacement against a
context-verified anchor, never a line-index write. **44 post-write assertions, 0 failures after one
correction:**

```
   no bare anchor.exists() gates left                       PASS   old form occurrences=0
   _generations gated (was UNGATED)                         PASS
   _generations resolves the wait ONCE                      PASS
   NOT ENUMERABLE emitted in BOTH halves (comments excluded) PASS   emitted=2, comment lines excluded=1
   stale REPO _archive path gone (daily_routine)            PASS
   stale REPO _archive path gone (archive_dependencies)     PASS
   banner wired above section 0                             PASS
   banner unnumbered (no duplicate '0.')                    PASS
   rule present EXACTLY once                                PASS   count=1
   NOT written into CONVENTIONS 2                           PASS
   drive_wait.py still 250 lines                            PASS
   compiles: all four scripts                               PASS
```

**The one failure was, once again, the assertion and not the file.** `count("NOT ENUMERABLE") == 2`
returned 3 — the third occurrence is inside **O-4's explanatory comment** at `:1109`, not emitted
output. Re-scoped to exclude comment lines, it passes at exactly 2.

**That is three sessions in a row where a guard misreported a healthy artifact** — a line-spanning
`.replace()`, a ledger marker count colliding with history, a `grep` reading `**bold**` as a regex,
and now a string count matching a comment. The through-line is now unmistakable: **every one was a
whole-file count standing in for a placement check.** A count tells you a string exists somewhere.
It never tells you it is in the right place, in the right form, or that it is code rather than prose.

---

## 9 · Publish and rollback

**Rollback.** `git revert 20ad593` removes all D-0b/D-0e wiring in one step; the three scripts return
to their `dea01d4` behaviour and `drive_wait.py` stays (it is used by nothing else). `git checkout --
exchange/queue/` is a no-op — 004 was not touched. **Nothing was deleted and nothing was moved, so
there is nothing else to undo.**

**Commits this session, in order:**

```
89c849f  exchange: auto-publish   (swept in the D-0d residency-note edit)
81fcc5f  exchange: auto-publish   (backup_estate's own publish step, after --workflow)
e923850  exchange: auto-publish   (the daily routine's own publish step)
20ad593  ops: queue 004 Phase 0 - wire drive_wait (D-0b), missed-run detector (D-0e)
```

Three of those four are **not mine** — they are `backup_estate.py` and `daily_routine.py` publishing
their own output, which is exactly what step 6 asked them to do. The code went in **one** commit as
instructed, staged set printed and verified at exactly three files.

<<PUBLISH>>

---

## 10 · File-disposition table (§3.2)

| PATH | EXISTS | TRACKED | COMMITTED | PUSHED | PROTECTED BY | BOX COST |
|---|---|---|---|---|---|---|
| `scripts/backup_estate.py` | yes | tracked | **`20ad593`** (+99 lines) | yes | GitHub + `--workflow` archive | n/a — outside `exchange/` |
| `scripts/daily_routine.py` | yes | tracked | **`20ad593`** (+123 lines) | yes | GitHub + `--workflow` archive | n/a |
| `scripts/archive_dependencies.py` | yes | tracked | **`20ad593`** (+31 lines) | yes | GitHub + `--workflow` archive | n/a |
| `scripts/drive_wait.py` | yes | tracked, **unchanged** | `e16de8b`/`9f3747d` | yes | GitHub + `--workflow` archive | n/a |
| `exchange/reports/NOTE_ATHENA_to_ARGUS_2026-08-11_DATA-RESIDENCY.md` | yes | tracked | **`89c849f`** (D-0d, +10 lines) | yes | GitHub + estate zip | +~0.8 KB — ~0.01% |
| `exchange/queue/004_move-clone-out-of-onedrive.md` | yes | tracked, **byte-untouched** | `cc02307` | yes | GitHub + estate zip | 0 — not modified |
| `exchange/status/HEARTBEAT.md` | yes | tracked | `e923850` | yes | GitHub + estate zip | regenerated; `phase: NONE` → `2026-08-02` |
| `exchange/status/RETENTION.md` | yes | tracked | `81fcc5f` | yes | GitHub + estate zip | regenerated by the `--workflow` run |
| `exchange/status/daily/DAILY_2026-08-12.md` | yes | tracked | `e923850` + this publish | yes | GitHub + estate zip | regenerated |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-12_PHASE-0.md` | yes | tracked (new) | this publish | yes | GitHub + estate zip | ~35 KB — ~0.55% (stated rounded: a file cannot carry its own size or sha256) |
| `exchange/status/LEDGER_ATHENA.md` | yes | tracked | this publish | yes | GitHub + estate zip | append, §11 |
| `exchange/status/DRIVE_WAKE_LOG.md` | **no** | — | — | — | — | 0 — created only by a real WOKE; none has occurred |
| `D:\naiad-backups\naiad_workflow_2026-08-12-02.zip` | yes | n/a — off-machine | — | — | the archive itself + tracked sidecar | n/a — 3,637,063 B on D: |
| `C:/Naiad` | **no** | n/a | — | — | — | n/a — **Phase A not begun; nothing copied** |
| Task Scheduler (3 tasks) | unchanged | n/a | — | — | — | **0 — not modified, by instruction** |

---

## 11 · Status

**Phase 0 is complete and green in the current tree.** D-0a shipped last session; D-0b wired 8 gates
plus 2 stale paths; D-0d filed; D-0e built and passing. Suite 287/1, workflow 349/349 with 0
mismatches, routine exit 0 — **this is the baseline Phase A must reproduce byte-for-byte from
`C:/Naiad`.**

**Phase A was deliberately not begun**, per the reviewer's ruling that it runs as its own session so
a failure after the move has exactly one possible cause. Its blocking pre-work is unchanged and
stated in the contract: **A-2's three identity gates assert the path contains `OneDrive`, and until
they are amended no post-move session can start.**
