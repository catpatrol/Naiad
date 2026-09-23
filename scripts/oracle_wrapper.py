"""THE ORACLE WRAPPER — D-3 of queue BR-1. Slot-anchored, self-rescheduling.
THE CLOCK IT WAS BUILT FOR IS SUSPENDED (operator ruling 2026-09-21): all five
agents are booted out AND `launchctl disable`d, so NOTHING here fires by itself
and no slot boundary is covered automatically. The live path is `--job ondemand`,
what the /oracle skill runs — see THE ON-DEMAND EDITION below. Everything between
here and there describes the clock AS IT WAS ARMED, and is live code again the day
the operator rolls it back (rollback card
research_outputs/oracle/SUSPENDED_2026-09-21.txt).

C-1, verbatim: "CADENCE = 07:00 local America/Argentina/Buenos_Aires full brief
+ 16:00 local Watch/Board refresh ... Delivered via slot-anchored launchd
wrapper (launchd has no timezone field)."

════════════════════════════════════════════════════════════════════════════
WHY A WRAPPER AT ALL, GIVEN WHAT THE MACHINE MEASURES.

launchd's StartCalendarInterval fires on MACHINE LOCAL WALL-CLOCK and has no
timezone field. ops/brief_schedule.yaml states the problem and leaves it open:
"a launchd port cannot express 'America/New_York 10:00' directly -- it needs
either a regenerating installer that rewrites the plists at each DST
transition, or a wrapper that computes the zone itself. Outstanding."

MEASURED ON THIS HOST: /etc/localtime -> America/Argentina/Buenos_Aires, and
`zdump -v` shows the last transition was 2009-03-15 with gmtoff fixed at
-10800 ever since. The Oracle's zone IS the machine's zone and that zone has
no DST, so a bare StartCalendarInterval {Hour 7|16} already lands on target.

The wrapper is built anyway, because the contract names it and because the
measurement is a property of THIS MACHINE TODAY, not of the schedule. What it
does is make the assumption self-checking: every run recomputes the correct
machine-local hour for the Buenos Aires slot, compares it with what the plist
actually says, and REWRITES + RELOADS the plist if they have drifted apart.
The day the laptop travels, or the day Argentina reinstates DST, the schedule
corrects itself on the next run instead of silently firing at the wrong hour.
(That check runs for the legacy jobs only; job=ondemand skips it — on drift it
would rewrite a retained plist and try to bootstrap a disabled label. See the
`schedule: SUSPENDED` line near the end of _ondemand_locked and WHY THE SCHEDULE
CHECK IS NOT RUN HERE.)

It also runs the self-checks once per edition and appends PASS/FAIL to
research_outputs/oracle/calibration/selfcheck_log.jsonl — the log BR-2 gate
G-BR2-2 reads. (Until the 2026-09-21 suspension that was once per clock slot;
now it is once per on-demand edition — see THE ON-DEMAND EDITION below. G-BR2-2
counts the last 7 RUNS, not the last 7 days, and always did.)

FIVE AGENTS, NOT FOUR (A2-8, 2026-08-21). The four above are clock agents. The
fifth, com.naiad.oracle-catchup, has no clock at all: it carried RunAtLoad and
fired once per login/boot WHILE ARMED, asking whether the most recent slot
boundary actually produced a brief and running the missed slot if it did not.
SUSPENDED SINCE 2026-09-21 — the disable override refuses it, RunAtLoad included,
so a missed boundary is now the operator's /oracle to fire. It exists because
launchd replays a missed calendar job on WAKE but not on BOOT — measured on this
host, see THE CATCH-UP below — so a laptop that was shut down over a slot lost
that slot silently, twice in the six days to 2026-08-21.

THE ALARM (T-7, ruled 2026-08-22). A wrapper that exits nonzero into a log
nobody opens is the 2026-08-20 silence. Any run that ends rc != 0 now writes
ORACLE_DOWN.flag at the top of the repo — timestamp, job, slot, exit code, the
last 15 traceback lines — and any run that actually did work and ended rc == 0
removes it again. (ONE EXCEPTION, OR-1 STEP A: a clean `--job ondemand --no-fetch`
run leaves a standing flag STANDING — it read the cache only and has no all-clear
to give about the wire. See ondemand_flag_action.) The flag is gitignored: it is
for the operator standing at the machine, never for the bus.

THE ON-DEMAND EDITION (OR-1 STEP A, 2026-09-21). The operator suspended the five
agents above — booted out AND disabled, plists retained unedited — and ruled that
the /oracle skill replaces the clock. `--job ondemand` is what that skill runs:
identity gate, the standing flag printed FIRST, the movers fetch in its own
process, the in-scope top-up, the cache-only Oracle, a Front Page summary — one
lock, one exit code, one flag decision, and NO schedule-drift check (on drift
that check rewrites a plist and bootstraps it, which the suspension forbids).
ONDEMAND_STEPS is the chain; `--job ondemand --dry-run` prints it and touches
nothing. See THE ON-DEMAND EDITION below. The four legacy paths (oracle, topup,
catchup, --install) are unchanged for every argv the clock ever wrote. The one
thing that changed for --install: an argv that NAMES THE ON-DEMAND EDITION is
dispatched to the on-demand job FIRST, and that job REFUSES --install (exit 2,
nothing touched) — `--job ondemand --dry-run --install` used to reach the arming
branch for all five suspended labels and print no dry run at all (fix round 1,
F-SK-2e). What that branch DID was only ever observed with arm() replaced by a
recorder: against the real, persistently `launchctl disable`d labels each
bootstrap should be refused, so the effect was five REWRITTEN plists (same bytes,
new mtimes — which is what the suspension audit's "five plists present and
unedited" checks) and five `ARMED <label>` lines that were not true, since
bootstrap_rc never reached the exit code (OR-1 finding OR1-b).

THE STRAY ARMING COMMAND IS GUARDED (OR-2 R-4, operator 2026-09-22). While the
sentinel research_outputs/oracle/SCHEDULE_SUSPENDED exists, `--install` alone
REFUSES — exit 2, nothing touched: no plist written, no launchctl call — and names
the explicit path, `--install --rearm`. That path (the operator's, never a
skill's) enables each label, bootstraps it and verifies it with `launchctl list`;
every rc reaches the exit code, and `ARMED <label>` prints only when all of them
answered 0 (arm_ok). The drift re-arm of the legacy post-run loop is held by the
same sentinel. launchctl is called by its bare name through LAUNCHCTL, resolved on
PATH, so F-SK-4 can run the explicit path against a recording shim and never the
real gui domain.

NO DELETION, EVER (CADENCE §4). Re-arming is bootout + bootstrap; the plist
stays on disk. This wrapper never removes a plist. (The flag above is not a
plist; it is the alarm's own body, and clearing it IS the all-clear.)
"""
from __future__ import annotations

import json
import os
import plistlib
import re
import subprocess
import sys
import traceback
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

ZONE = "America/Argentina/Buenos_Aires"
UID = 501
PY = "/Users/luis/venvs/naiad/bin/python"
AGENTS = Path.home() / "Library" / "LaunchAgents"
LOGDIR = ROOT / "logs" / "launchd"
SELFCHECK = ROOT / "research_outputs" / "oracle" / "calibration" / "selfcheck_log.jsonl"

# OR-2 R-4 · THE GUARD ON THE STRAY ARMING COMMAND. Plain module constants, not
# ONDEMAND_REGISTER rows: the ruling fixed them, so there is nothing [VETO] to show.
# The sentinel is a module-level Path so a fixture can point it elsewhere; its
# EXISTENCE is the guard, its text is for the operator (it carries REARM_COMMAND
# byte for byte, which F-SK-4 checks).
SCHEDULE_SENTINEL = ROOT / "research_outputs" / "oracle" / "SCHEDULE_SUSPENDED"
SCHEDULE_SENTINEL_REL = "research_outputs/oracle/SCHEDULE_SUSPENDED"
REARM_FLAG = "--rearm"
REARM_COMMAND = ("cd ~/Naiad && ~/venvs/naiad/bin/python scripts/oracle_wrapper.py "
                 "--install --rearm")
# BARE ON PURPOSE: resolved through PATH at call time, never an absolute path, so
# F-SK-4's recording shim is what answers under the fixture.
LAUNCHCTL = "launchctl"

# label -> {slot, hour, minute, job}. Times are in the ORACLE's zone, never the
# machine's; `machine_local_time_for` resolves them through the zone each run.
# job "oracle" renders the organ; job "topup" is BR-1b's fetch-and-store, which
# WAS armed 15 minutes ahead of each Oracle slot so the cache was fresh before it
# was read. All five labels are SUSPENDED since 2026-09-21; this table is what the
# retained plists say, not what the machine is running.
SLOTS = {
    "com.naiad.oracle-topup-0645": {"slot": "topup", "hour": 6, "minute": 45,
                                    "job": "topup"},
    "com.naiad.oracle-0700": {"slot": "full", "hour": 7, "minute": 0,
                              "job": "oracle"},
    "com.naiad.oracle-topup-1545": {"slot": "topup", "hour": 15, "minute": 45,
                                    "job": "topup"},
    "com.naiad.oracle-1600": {"slot": "refresh", "hour": 16, "minute": 0,
                              "job": "oracle"},
    # A2-8 · THE CATCH-UP. Not a clock slot: hour is None, so no
    # StartCalendarInterval is written and the self-reschedule skips it. It
    # carried RunAtLoad instead and fired once at every login/boot while armed. See THE
    # CATCH-UP below for why the other four are not enough.
    "com.naiad.oracle-catchup": {"slot": "catchup", "hour": None, "minute": None,
                                 "job": "catchup", "run_at_load": True},
}


# ══════════════════════════════════════════════════════ THE ZONE ARITHMETIC

def machine_local_time_for(zone_hour: int, zone_minute: int = 0,
                           when: datetime | None = None) -> tuple[int, int]:
    """The machine-local (hour, minute) at which it is zone_hour:zone_minute in ZONE.

    Computed through the zone, never through a stored UTC offset — the zone is
    the durable quantity and the offset is a rendering of it (the .ps1 the
    Windows era used made the same choice, and said so).
    """
    z = ZoneInfo(ZONE)
    now = (when or datetime.now(timezone.utc)).astimezone(z)
    target = now.replace(hour=zone_hour, minute=zone_minute, second=0, microsecond=0)
    if target <= now:
        target = target + timedelta(days=1)
    local = target.astimezone()          # the machine's own zone
    return local.hour, local.minute


def zone_report() -> dict:
    z = ZoneInfo(ZONE)
    now_utc = datetime.now(timezone.utc)
    a = now_utc.astimezone(z)
    b = now_utc.astimezone()
    return {
        "oracle_zone": ZONE,
        "oracle_now": a.isoformat(),
        "oracle_utcoffset_s": int(a.utcoffset().total_seconds()),
        "machine_now": b.isoformat(),
        "machine_utcoffset_s": int(b.utcoffset().total_seconds()),
        "zones_agree": a.utcoffset() == b.utcoffset(),
    }


# ═════════════════════════════════════════════════════════ THE PLIST ITSELF

def plist_body(label: str, slot: str, hour: int | None, minute: int | None,
               job: str = "oracle", run_at_load: bool = False) -> dict:
    body = {
        "Label": label,
        "ProgramArguments": [PY, str(ROOT / "scripts" / "oracle_wrapper.py"),
                             "--job", job, "--slot", slot],
        "WorkingDirectory": str(ROOT),
        # PATH pinned exactly as the three existing agents pin it: the house
        # reason is that scripts shell out to bare `git`, and pinning makes the
        # tested environment identical to the scheduled one.
        "EnvironmentVariables": {"PATH": "/usr/bin:/bin:/usr/sbin:/sbin"},
        "StandardOutPath": str(LOGDIR / f"{label.split('.')[-1]}.log"),
        "StandardErrorPath": str(LOGDIR / f"{label.split('.')[-1]}.log"),
        # false ON PURPOSE for every CLOCK slot, the same reason the other three
        # say so: RunAtLoad true would fire a full run the instant the agent is
        # bootstrapped and again at every login, which is not what "07:00 daily"
        # means. The catch-up agent is the one deliberate exception — it has no
        # clock, and firing at login is its entire job.
        "RunAtLoad": bool(run_at_load),
    }
    if hour is not None:
        body["StartCalendarInterval"] = {"Hour": int(hour), "Minute": int(minute)}
    return body


def write_plist(label: str) -> tuple[Path, int | None, int | None]:
    cfg = SLOTS[label]
    h, m = ((None, None) if cfg["hour"] is None
            else machine_local_time_for(cfg["hour"], cfg["minute"]))
    p = AGENTS / f"{label}.plist"
    p.parent.mkdir(parents=True, exist_ok=True)
    LOGDIR.mkdir(parents=True, exist_ok=True)
    p.write_bytes(plistlib.dumps(plist_body(label, cfg["slot"], h, m, cfg["job"],
                                            cfg.get("run_at_load", False))))
    return p, h, m


def loaded_schedule(label: str) -> dict | None:
    out = subprocess.run([LAUNCHCTL, "print", f"gui/{UID}/{label}"],
                         capture_output=True, text=True)
    if out.returncode != 0:
        return None
    sched = {}
    for k in ("Hour", "Minute"):
        for line in out.stdout.splitlines():
            if f'"{k}"' in line and "=>" in line:
                try:
                    sched[k] = int(line.split("=>")[1].strip())
                except ValueError:
                    pass
    return sched or {"loaded": True}


def arm_ok(rcs: dict) -> bool:
    """OR-2 R-4 · ARMED IS SAID ONLY ON rc 0. `rcs` holds the return code of every
    launchctl step that decides the question — `enable` (the explicit re-arm path
    only), `bootstrap`, and the `list` that verifies the label is loaded. The
    bootout's rc is NOT among them: a label that is not loaded answers nonzero, and
    unloading it first is housekeeping, not arming. Before R-4 the bootstrap rc went
    into a dict and a stderr line only, and `ARMED <label>` printed whatever it said
    (OR1-b's false-ARMED half). A pure function, so F-SK-4 can replant the old
    rc-blind rule and watch it go red."""
    return bool(rcs) and all(rc == 0 for rc in rcs.values())


def arm(label: str, log=print, enable: bool = False) -> dict:
    """Write the plist, (enable), bootout, bootstrap, verify. `enable=True` is the
    explicit re-arm path (`--install --rearm`): the five labels were persistently
    `launchctl disable`d on 2026-09-21, and bootstrap alone will not re-arm a
    disabled label (the rollback card), so enable goes FIRST."""
    p, h, m = write_plist(label)
    rcs: dict = {}
    if enable:
        rcs["enable"] = subprocess.run([LAUNCHCTL, "enable", f"gui/{UID}/{label}"],
                                       capture_output=True, text=True).returncode
    subprocess.run([LAUNCHCTL, "bootout", f"gui/{UID}/{label}"],
                   capture_output=True, text=True)
    r = subprocess.run([LAUNCHCTL, "bootstrap", f"gui/{UID}", str(p)],
                       capture_output=True, text=True)
    rcs["bootstrap"] = r.returncode
    lint = subprocess.run(["plutil", "-lint", str(p)], capture_output=True, text=True)
    rcs["list"] = subprocess.run([LAUNCHCTL, "list", label],
                                 capture_output=True, text=True).returncode
    sched = loaded_schedule(label)
    ok = arm_ok(rcs)
    cfg = SLOTS[label]
    when = (f"machine-local {h:02d}:{m:02d} "
            f"(= {cfg['hour']:02d}:{cfg['minute']:02d} {ZONE})"
            if h is not None else "no clock · RunAtLoad, once per login/boot")
    rc_txt = " · ".join(f"{k} rc {v}" for k, v in rcs.items())
    if ok:
        log(f"  ARMED {label} [{cfg['job']}]: {when} · plist {p} · {rc_txt}")
    else:
        log(f"  NOT ARMED {label} [{cfg['job']}]: {rc_txt} — every one must be 0 · plist {p}")
    log(f"    plutil: {lint.stdout.strip() or lint.stderr.strip()}")
    log(f"    launchd reports: {sched}")
    if r.returncode != 0:
        log(f"    bootstrap stderr: {r.stderr.strip()}")
    return {"label": label, "plist": str(p), "hour": h, "minute": m,
            "bootstrap_rc": r.returncode, "rcs": rcs, "armed": ok,
            "schedule_from_launchd": sched}


def install_refusal(argv: list[str]) -> str | None:
    """OR-2 R-4 · the one decision on the arming verb; None means "go ahead".
    While SCHEDULE_SENTINEL exists, `--install` alone REFUSES and names the explicit
    path. The explicit path takes EXACTLY `--install --rearm`: a stray token beside
    it (a `--dry-run`, a `--job`) would otherwise arm for real while looking like
    something else. `--rearm` without `--install` would otherwise fall through to
    the legacy job (a full render plus the drift loop), so it refuses too."""
    if REARM_FLAG in argv and "--install" not in argv:
        return (f"HALT: {REARM_FLAG} means nothing without --install; the explicit re-arm "
                f"is `{REARM_COMMAND}`. Nothing was touched.")
    if REARM_FLAG in argv and set(argv) - {"--install", REARM_FLAG}:
        extra = sorted(set(argv) - {"--install", REARM_FLAG})
        return (f"HALT: the explicit re-arm takes exactly `--install --rearm`; this argv "
                f"also carries {extra}. Nothing was touched.")
    if "--install" in argv and REARM_FLAG not in argv and SCHEDULE_SENTINEL.exists():
        return (f"HALT: --install REFUSED — the five com.naiad.oracle-* agents are SUSPENDED "
                f"(sentinel {SCHEDULE_SENTINEL_REL}, OR-2 R-4). Nothing was touched: no plist "
                f"written, no launchctl call. Re-arming is the operator's explicit path, "
                f"`--install --rearm`: `{REARM_COMMAND}` (rollback card {SUSPENDED_CARD}).")
    return None


def reschedule_if_drifted(label: str, log=print) -> dict:
    """The self-reschedule. Compares the plist's hour against the zone's truth."""
    cfg = SLOTS[label]
    if cfg["hour"] is None:
        # A clockless agent has no StartCalendarInterval to drift away from the
        # zone. It is still checked for PRESENCE — an agent that vanished is the
        # failure this whole wrapper exists to notice.
        p = AGENTS / f"{label}.plist"
        gone = not p.exists()
        if gone:
            log(f"  AGENT MISSING: {label} has no plist at {p} — the catch-up is "
                f"NOT armed. Re-arm with: oracle_wrapper.py --install (while "
                f"{SCHEDULE_SENTINEL_REL} exists: --install --rearm)")
        return {"label": label, "drift": False, "missing": gone,
                "want": {"RunAtLoad": True, "installed": not gone}, "had": {}}
    want_h, want_m = machine_local_time_for(cfg["hour"], cfg["minute"])
    p = AGENTS / f"{label}.plist"
    have = {}
    if p.exists():
        try:
            have = plistlib.loads(p.read_bytes()).get("StartCalendarInterval", {})
        except Exception:
            have = {}
    drift = (int(have.get("Hour", -1)) != want_h) or (int(have.get("Minute", -1)) != want_m)
    if drift and SCHEDULE_SENTINEL.exists():
        # OR-2 R-4: the second route into arm(). A hand-run legacy job would
        # otherwise rewrite and bootstrap a suspended label on drift.
        log(f"  SCHEDULE DRIFT on {label}: plist says {have}, the zone says "
            f"{{'Hour': {want_h}, 'Minute': {want_m}}} — NOT re-armed: the schedule "
            f"is SUSPENDED ({SCHEDULE_SENTINEL_REL}); the explicit re-arm is "
            f"`{REARM_COMMAND}`")
    elif drift:
        log(f"  SCHEDULE DRIFT on {label}: plist says {have}, the zone says "
            f"{{'Hour': {want_h}, 'Minute': {want_m}}} — rewriting and reloading")
        arm(label, log=log)
    return {"label": label, "drift": drift, "want": {"Hour": want_h, "Minute": want_m},
            "had": have}


# ══════════════════════════════════════════════════════════════ SINGLE FLIGHT
# D4 of the 2026-08-22 incident audit. Before the catch-up existed, every Oracle
# job was a distinct calendar slot and two could not overlap. The catch-up can
# fire at a login that lands while a clock slot is still running, and both paths
# append to the SAME dated tape parquet and the same selfcheck log. One writer at
# a time.
#
# A plain O_EXCL file, not flock: the holder must survive being inspected by an
# operator, and a stale lock from a killed run must be recoverable without a
# reboot.
#
# LOCK_STALE_MIN IS NO LONGER ABOVE THE WORST CASE (review finding, 2026-09-21).
# The words here read "STALE_MIN is generous — the longest observed run is well
# under it", and "a top-up takes ~130 s wall-clock (measured: 09:45:04 ->
# 09:47:14)". Both were true when the scope was 40 pairs. The pinned scope is now
# 72 (research_outputs/oracle/topup_scope.json) and the roster went 10 -> 18
# symbols on 2026-09-21. MEASURED on this lane's own logs: a FAILING pair costs
# >= 15 s (engine.data._get's 1.5 + 3 + 4.5 + 6 s of backoff; 2026-09-18
# 09:45:03 -> 09:55:21 = 618.7 s for 40 pairs = 15.47 s/pair, and 2026-09-20
# reproduces it), so a wire-down top-up over 72 pairs is >= 18 min on its own;
# MOVERS_TIMEOUT_S = 600 s sits in front of it and the render ~20 s behind it,
# i.e. ~29 min against LOCK_STALE_MIN = 30. acquire_lock's stale rule is AGE
# ONLY — it never asks whether the holder is alive — so past 30 minutes it would
# take the lock from a run that is still working, and two editions would then
# write one oracle_<date>.html and one oracle_tape_<date>.parquet, neither write
# atomic, and two selfcheck rows for one operator request.
# THAT RULE IS LEGACY AND SHARED with the (suspended) clock jobs, and the
# constant is incident-earned (2026-08-22 audit D4) with no REGISTER row, so it
# is NOT changed here: raising it is an operator matter and wants a ruled row
# carrying the arithmetic above. What job=ondemand does instead is stand down on
# a live pid at any age — live_lock_holder(), called from _ondemand_locked.
LOCK = LOGDIR / ".oracle.lock"
LOCK_STALE_MIN = 30


def acquire_lock(who: str, log=print) -> bool:
    LOCK.parent.mkdir(parents=True, exist_ok=True)
    body = json.dumps({"who": who, "pid": os.getpid(),
                       "ts": datetime.now(timezone.utc).isoformat()})
    try:
        fd = os.open(LOCK, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
    except FileExistsError:
        held = {}
        try:
            held = json.loads(LOCK.read_text())
            age_min = (datetime.now(timezone.utc)
                       - datetime.fromisoformat(held["ts"])).total_seconds() / 60.0
        except Exception:
            age_min = LOCK_STALE_MIN + 1          # unreadable lock is a stale lock
        if age_min <= LOCK_STALE_MIN:
            log(f"  LOCK HELD by {held.get('who')} (pid {held.get('pid')}, "
                f"{age_min:.1f} min old) — standing down, this run does nothing")
            return False
        log(f"  STALE LOCK from {held.get('who')} ({age_min:.1f} min > "
            f"{LOCK_STALE_MIN} min) — reclaiming it")
        try:
            LOCK.unlink()
        except FileNotFoundError:
            pass
        try:
            fd = os.open(LOCK, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
        except FileExistsError:
            log("  lock re-taken by another run in the same instant — standing down")
            return False
    os.write(fd, body.encode())
    os.close(fd)
    return True


def release_lock(log=print) -> None:
    try:
        LOCK.unlink()
    except FileNotFoundError:
        pass
    except Exception as e:
        log(f"  could not release {LOCK}: {e}")


# ═════════════════════════════════════════════════════════════════ THE ALARM
# T-7 of the 2026-08-20 incident, RULED "flagfile" by the operator on 2026-08-22.
#
# WHAT THE SILENCE COST. The Oracle died on six consecutive runs from 2026-08-20
# and nothing said so. launchd recorded the nonzero exit and moved on; the brief
# on disk had been written BEFORE the crash line, so it looked current; the only
# honest evidence was a FAIL row inside a jsonl nobody opens at 07:00. Two days
# passed. An alarm that lives inside the machinery the operator does not read is
# not an alarm.
#
# So: ONE FILE, at the top of the repo, where it cannot be walked past. Its
# presence IS the alarm; its absence IS the all-clear. No daemon, no notification
# service, no second process that can itself die quietly.
#
# IT MUST NEVER REACH THE BUS. The flag is gitignored. A published exchange
# carrying ORACLE_DOWN.flag would tell every reader of the bus that a laptop in
# Buenos Aires had a bad morning; the flag is for the operator at the machine.
#
# SELF-CLEARING — BUT NOT BY A RUN THAT DID NOTHING. rc == 0 alone is not an
# all-clear. The lock stand-down exits 0 having done no work; --install exits 0
# without running the Oracle at all; a catch-up that finds nothing missed exits 0
# by design. If any of those cleared the flag, a login could silently cancel a
# real alarm — the same class of mistake as D1/D2, where a file a FAILED run also
# writes was taken as proof the run succeeded. The flag is therefore cleared only
# by a run that PERFORMED A JOB and reached rc == 0, which is exactly what the
# flag's own last sentence promises: the next CLEAN RUN.
#
# THE SENTENCE IS LEFT BYTE-FOR-BYTE (it is in every flag the legacy jobs write, and
# F-BR-12 reads it). What "the next clean run" means for job=ondemand is narrower
# than rc == 0: a clean `--no-fetch` edition is NOT that run — it never touched the
# wire — and it says so in its own log ("alarm left standing … no all-clear to
# give") at the moment the operator is reading. See ondemand_flag_action.
FLAG = ROOT / "ORACLE_DOWN.flag"
FLAG_SENTENCE = ("The Oracle is down. Read logs/launchd/oracle-*.log. "
                 "This file self-clears on the next clean run.")
FLAG_TB_LINES = 15

# Why a module-level list and not a return value: the except blocks that HOLD a
# traceback sit three frames below main(), and by the time the alarm is written
# the stack is gone. Those blocks already format the text for the log; this keeps
# the same text for the flag. APPENDED, never replaced — one run can fail twice
# (the render, then a missing agent) and the operator wants to see both.
FAILURES: list[str] = []


def note_failure(text: str | None = None) -> str:
    """Remember WHY, for the alarm. `None` means: format the live traceback."""
    t = (traceback.format_exc() if text is None else text).rstrip()
    FAILURES.append(t)
    return t


def raise_flag(job: str, slot: str, rc: int, log=print) -> Path:
    """Write the alarm. Overwrites any older flag: the newest failure is the one
    the operator should read first, and the log keeps the rest."""
    joined = ("\n".join(FAILURES) if FAILURES else
              "(no traceback captured — the run returned nonzero without raising)")
    tail = joined.splitlines()[-FLAG_TB_LINES:]
    body = "\n".join([
        f"UTC   {datetime.now(timezone.utc).isoformat()}",
        f"JOB   {job}",
        f"SLOT  {slot}",
        f"EXIT  {rc}",
        "",
        f"LAST {len(tail)} TRACEBACK LINE(S), NEWEST FAILURE LAST:",
        *tail,
        "",
        FLAG_SENTENCE,
        "",
    ])
    try:
        FLAG.parent.mkdir(parents=True, exist_ok=True)
        FLAG.write_text(body, encoding="utf-8")
    except Exception as e:                    # an alarm that raises is no alarm
        log(f"  COULD NOT RAISE THE ALARM at {FLAG}: {e}")
        return FLAG
    log(f"  ALARM RAISED — {FLAG}")
    return FLAG


def clear_flag(log=print) -> bool:
    """The all-clear. True if a flag was actually standing and is now gone."""
    try:
        FLAG.unlink()
    except FileNotFoundError:
        return False
    except Exception as e:
        log(f"  could not clear {FLAG}: {e}")
        return False
    log(f"  ALARM CLEARED — {FLAG.name} removed by a clean run")
    return True


# ═══════════════════════════════════════════════════════════════ THE CATCH-UP
# A2-8 (2026-08-21), the SHUTDOWN half of finding T-3. A2-7 gave the sleep half
# a banner; this gives the shutdown half a run.
#
# MEASURED ON THIS HOST, 2026-08-16 → 2026-08-21, from logs/launchd and
# `last reboot`: launchd DOES replay a missed StartCalendarInterval when the
# machine WAKES — 08-20 16:00 ran at 16:03 and 08-21 16:00 ran at 16:08, each on
# the DarkWake logged the same second — but it does NOT replay one when the
# machine BOOTS. The 08-18 07:00 and 08-19 16:00 slots fell inside power-off
# windows (05:05→15:30 and 14:21→18:40) and were never replayed: the 15:30 boot
# fired neither the 06:45 top-up nor the 07:00 Oracle, and 2026-08-18 has no
# morning brief and no calibration record to this day.
#
# So the four clock agents are complete for a sleeping laptop and silently
# incomplete for one that was off. This agent closes that: no clock, RunAtLoad
# true, one question at every login — has the most recent slot boundary actually
# produced a brief? — and the missed slot runs if it has not.
#
# IT RUNS THE TOP-UP FIRST. That is not the open T-3 ruling (whether the Oracle
# should REFUSE to render on a stale cache); it is only the obvious ordering for
# a catch-up that owns both halves and can therefore choose them in order.
#
# GRACE keeps it out of launchd's way. launchd's own on-wake replay was 3 and 8
# minutes late in the two measured cases, so a boundary younger than GRACE is
# left to launchd rather than raced for it.
CATCHUP_GRACE_MIN = 20


def last_slot_boundary(now: datetime | None = None) -> tuple[datetime, str]:
    """The most recent Oracle slot boundary at or before `now`, and its slot name.

    Computed in the ORACLE's zone for the same reason everything else here is:
    the zone is the durable quantity. Yesterday's boundaries are candidates too,
    so a 03:00 login correctly resolves to yesterday's 16:00 and not to nothing.
    """
    z = ZoneInfo(ZONE)
    now = (now or datetime.now(timezone.utc)).astimezone(z)
    cands = []
    for cfg in SLOTS.values():
        if cfg["job"] != "oracle":
            continue
        for back in (0, 1):
            b = (now - timedelta(days=back)).replace(
                hour=cfg["hour"], minute=cfg["minute"], second=0, microsecond=0)
            if b <= now:
                cands.append((b, cfg["slot"]))
    return max(cands, key=lambda t: t[0])


def selfcheck_rows() -> list[dict]:
    if not SELFCHECK.exists():
        return []
    out = []
    for line in SELFCHECK.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except Exception:
            continue                      # a torn row is not a reason to stop
    return out


def _row_time(row: dict, z: ZoneInfo) -> datetime | None:
    try:
        return datetime.fromisoformat(row["ts"]).astimezone(z)
    except Exception:
        return None


def catchup_due(now: datetime | None = None) -> dict:
    """Did the most recent slot boundary produce a PASSING run?

    THE EVIDENCE IS THE SELFCHECK LOG, NOT THE BRIEF (repaired 2026-08-22, defect
    D2 of the incident audit). The first draft read the brief's mtime, which is
    wrong for the exact failure this agent was built after: oracle_daily.run()
    writes the brief BEFORE it calls write_calibration, so the four crashed runs
    of 2026-08-20/21 each left a freshly stamped brief on disk and no calibration
    record at all. A file that a FAILED run also writes cannot be the evidence
    that the run succeeded — the mtime test would have reported covered=True
    straight through the outage and the catch-up would have sat silent.

    The selfcheck log is the right witness: it is one row per run carrying the
    verdict, it is the same log BR-2 gate G-BR2-2 reads, and it distinguishes
    "no run happened" from "a run happened and failed". Both now count as not
    covered, so this agent recovers a MISSED SLOT and a CRASHED RUN alike.

    A boundary is tried at most ONCE. If a catch-up already ran for it and still
    did not produce a PASS, the fault is not a missed wake-up and re-running on
    every login would only bury the operator's evidence under retries.
    """
    z = ZoneInfo(ZONE)
    now_z = (now or datetime.now(timezone.utc)).astimezone(z)
    boundary, slot = last_slot_boundary(now_z)
    age_min = (now_z - boundary).total_seconds() / 60.0

    rows = selfcheck_rows()
    after = [(r, t) for r in rows for t in [_row_time(r, z)] if t and t >= boundary]
    passed = [(r, t) for r, t in after if r.get("verdict") == "PASS"]
    tried = [(r, t) for r, t in after if r.get("catchup")]

    covered = bool(passed)
    if covered:
        t = max(t for _, t in passed)
        reason = f"selfcheck row {t:%Y-%m-%d %H:%M} verdict PASS, at or after the boundary"
    elif age_min < CATCHUP_GRACE_MIN:
        reason = (f"boundary is only {age_min:.0f} min old, inside the "
                  f"{CATCHUP_GRACE_MIN}-min grace — left to launchd's own wake replay")
    elif tried:
        t = max(t for _, t in tried)
        reason = (f"a catch-up already ran for this boundary at {t:%Y-%m-%d %H:%M} "
                  f"and did not reach PASS — not retried; this needs the operator")
    elif after:
        reason = (f"{len(after)} run(s) since the boundary, none of them PASS — "
                  f"newest verdict {max(after, key=lambda rt: rt[1])[0].get('verdict')}")
    else:
        reason = "no selfcheck row at all at or after the boundary — the slot never ran"

    return {"due": (not covered) and (not tried) and age_min >= CATCHUP_GRACE_MIN,
            "slot": slot, "boundary": boundary.isoformat(),
            "age_min": round(age_min, 1),
            "rows_after_boundary": len(after), "passed_after_boundary": len(passed),
            "already_tried": bool(tried), "covered": covered, "reason": reason}


# ═════════════════════════════════════════════════════════ THE SELF-CHECKS

def self_checks(log=print) -> dict:
    """Three per-edition checks, per D-3 (one run per on-demand edition since the clock
    was suspended 2026-09-21; they were once per clock slot while it was armed): refresh
    idempotence, thumbnail provenance, tape append integrity. Results append to
    selfcheck_log.jsonl for BR-2 G-BR2-2. The three KEY LITERALS below are what those
    rows are keyed on: they are the log's schema and do not move with this wording."""
    import oracle_fixtures as OF
    import oracle_daily as OD
    res: dict[str, object] = {}
    OF.load_artifacts()
    for name, fn in (("refresh_idempotence", lambda: OF._refresh(tamper=False)),
                     ("thumbnail_provenance", lambda: OF._thumbnails(OF.HTML))):
        try:
            ok, detail = fn()
        except Exception as e:
            ok, detail = False, f"{e.__class__.__name__}: {e}"
        res[name] = {"pass": bool(ok), "detail": detail[:400]}

    # TWO TAPES, ONE CHECK (A-OR1-1 v, 2026-09-22). The D-4 tape is TC4's event tape
    # and its schema is untouched: exactly OD.TAPE_COLS, the pre-OR-1 24, so a column
    # beyond them (a range column come back) FAILS the check. The range layer records
    # to its sibling, research_outputs/oracle/tape_ranges/, and that file gets the same
    # existence / columns / banned-vocabulary / row-count check plus one row per roster
    # symbol. Both fold into the ONE key "tape_append_integrity": the key literals are
    # the selfcheck log's schema and do not move (see the docstring).
    try:
        import pandas as pd
        # the same stemmed, component-wise matcher the fixture uses — the first
        # version split on "_" only and let plurals through
        import oracle_fixtures as _OF
        t = sorted(OD.TAPE_DIR.glob("oracle_tape_*.parquet"))
        if not t:
            raise FileNotFoundError(f"no D-4 tape (oracle_tape_*.parquet) under {OD.TAPE_DIR}")
        df = pd.read_parquet(t[-1])
        missing = [c for c in OD.TAPE_COLS if c not in df.columns]
        extra = [c for c in df.columns if c not in OD.TAPE_COLS]
        banned = [c for c in df.columns
                  if _OF._calibration({c: 0})[0] is False]
        rt = sorted(OD.TAPE_RANGES_DIR.glob("oracle_tape_ranges_*.parquet"))
        if not rt:
            raise FileNotFoundError(f"no sibling range tape (oracle_tape_ranges_*.parquet) "
                                    f"under {OD.TAPE_RANGES_DIR} — the D-4 tape "
                                    f"{t[-1].name} has {len(df.columns)} columns, extra={extra}")
        rdf = pd.read_parquet(rt[-1])
        r_missing = [c for c in OD.RANGE_TAPE_COLS if c not in rdf.columns]
        r_extra = [c for c in rdf.columns if c not in OD.RANGE_TAPE_COLS]
        r_banned = [c for c in rdf.columns
                    if _OF._calibration({c: 0})[0] is False]
        roster = list(OD.REGISTER["ROSTER"]["value"])
        r_assets = sorted(rdf["asset"].astype(str)) if "asset" in rdf.columns else []
        per_symbol = r_assets == sorted(roster)
        ok = ((not missing) and (not extra) and (not banned) and len(df) > 0
              and (not r_missing) and (not r_extra) and (not r_banned) and len(rdf) > 0
              and per_symbol)
        detail = (f"{len(t)} tape file(s), newest {t[-1].name} with {len(df)} rows, "
                  f"{len(df.columns)} columns; missing={missing}; extra={extra}; "
                  f"outcome_columns={banned} ‖ {len(rt)} sibling range tape file(s), newest "
                  f"{rt[-1].name} with {len(rdf)} rows for {len(roster)} roster symbols "
                  f"(one per symbol: {per_symbol}), {len(rdf.columns)} columns; "
                  f"missing={r_missing}; extra={r_extra}; outcome_columns={r_banned}")
    except Exception as e:
        ok, detail = False, f"{e.__class__.__name__}: {e}"
    res["tape_append_integrity"] = {"pass": bool(ok), "detail": detail[:600]}

    for k, v in res.items():
        log(f"  selfcheck {k}: {'PASS' if v['pass'] else 'FAIL'}")
    return res


def append_selfcheck(slot: str, res: dict, extra: dict) -> Path:
    SELFCHECK.parent.mkdir(parents=True, exist_ok=True)
    row = {
        "date": datetime.now().astimezone().strftime("%Y-%m-%d"),
        "ts": datetime.now(timezone.utc).isoformat(),
        "slot": slot,
        "verdict": "PASS" if all(v["pass"] for v in res.values()) else "FAIL",
        "checks": res,
        **extra,
    }
    with SELFCHECK.open("a") as fh:
        fh.write(json.dumps(row, sort_keys=True) + "\n")
    return SELFCHECK


# ═════════════════════════════════════════════════════════════════ RUNNING

def undo_lines() -> list[str]:
    out = ["# UNDO — disarm the Oracle. bootout unloads the agent; the plist stays",
           "# on disk and `launchctl bootstrap` re-arms it. Removing a plist is an",
           "# operator action, never a scheduled-lane one (CADENCE §4, no-delete)."]
    for label in SLOTS:
        out.append(f"launchctl bootout gui/{UID}/{label}")
    out.append("# re-arm: enable FIRST (a disabled label refuses a bootstrap), then bootstrap:")
    for label in SLOTS:
        out.append(f"launchctl enable gui/{UID}/{label}")
    for label in SLOTS:
        out.append(f"launchctl bootstrap gui/{UID} ~/Library/LaunchAgents/{label}.plist")
    return out


def run_topup(slot: str, log=print) -> int:
    """BR-1b. Fetch-and-store only: no render, no self-checks, no publish. A
    failure here logs to topup_log.jsonl and exits nonzero; the Oracle is
    unaffected and stamps whatever as-of it finds — 15 minutes later under the
    legacy topup slot, SECONDS later in the on-demand chain, where this is step
    'scope-topup' and the render follows in the same process (ruling T-3: it
    renders on a stale cache with the banner showing)."""
    try:
        import oracle_topup as TU
        doc = TU.run(slot=slot, log=log)
        rc = 0 if doc["verdict"] == "PASS" else 1
        log(f"  top-up {doc['verdict']}: +{doc['rows_added']} rows across "
            f"{doc['pairs']} pair(s), {doc['gaps']} gap(s)")
    except SystemExit as e:
        rc = 1
        log("  TOP-UP HALTED: " + note_failure(f"TOP-UP HALTED: {e}"))
    except Exception:
        rc = 1
        log("  TOP-UP FAILED:\n" + note_failure())
        try:
            import oracle_topup as TU
            TU.append_log({"ts": datetime.now(timezone.utc).isoformat(),
                           "date": datetime.now().astimezone().strftime("%Y-%m-%d"),
                           "slot": slot, "verdict": "FAIL", "pairs": 0,
                           "rows_added": 0, "gaps": 0,
                           "failures": ["wrapper-level exception"],
                           "traceback": traceback.format_exc()[-1200:]})
        except Exception:
            pass
    return rc


def run_oracle(slot: str, zr: dict, started: datetime, log=print,
               catchup: bool = False) -> int:
    """Render the organ, then the three self-checks, then one selfcheck_log row.

    The self-checks are gated on a clean render ON PURPOSE — checking the
    idempotence of a render that did not happen proves nothing. The cost of that
    gate is that a render failure takes the checks dark with it, which is exactly
    what happened for six runs from 2026-08-20, so the row below records
    `checks: {run: ...}` and the reader can tell the two states apart."""
    rc = 0
    result: dict = {}
    try:
        import oracle_daily as OD
        result = OD.run(slot=slot, log=log)
        log(f"  render {result['html']} sha256 {result['html_sha']}")
    except Exception:
        rc = 1
        log("  RUN FAILED:\n" + note_failure())

    res = {}
    if rc == 0:
        try:
            res = self_checks(log=log)
            bad = [k for k, v in res.items() if not v["pass"]]
            if bad:
                rc = 1
                # A red self-check raises no exception, so the alarm would have
                # nothing to show without this line.
                note_failure("SELF-CHECKS FAILED: " + "; ".join(
                    f"{k}: {res[k].get('detail')}" for k in bad))
        except Exception:
            rc = 1
            log("  SELF-CHECKS FAILED:\n" + note_failure())

    p = append_selfcheck(slot, res or {"run": {"pass": rc == 0,
                                               "detail": "run failed"}},
                         {"zone_agree": zr["zones_agree"],
                          "html_sha": result.get("html_sha"),
                          "catchup": bool(catchup),
                          "seconds": round((datetime.now(timezone.utc) - started)
                                           .total_seconds(), 1)})
    log(f"  selfcheck log -> {p}")
    return rc


def run_catchup(zr: dict, started: datetime, log=print) -> tuple[int, bool]:
    """A2-8. Fires at every login/boot; runs something only when a slot was missed.

    Returns (rc, ran). `ran` is False when nothing was missed — a correct, clean,
    entirely idle exit, and therefore NOT the clean run that clears the T-7 flag."""
    d = catchup_due()
    log(f"  catch-up: most recent Oracle boundary {d['boundary']} [{d['slot']}], "
        f"{d['age_min']:.0f} min ago")
    log(f"  evidence: {d['reason']}")
    if not d["due"]:
        log("  NOTHING MISSED — no catch-up run")
        return 0, False
    log(f"  MISSED SLOT [{d['slot']}] — running the top-up first, then the Oracle")
    rc_t = run_topup("topup", log=log)
    rc_o = run_oracle(d["slot"], zr, started, log=log, catchup=True)
    return rc_t or rc_o, True


def _argv_job_slot(argv: list[str]) -> tuple[str, str]:
    """Read --job/--slot defensively, and from one place, because the outermost
    alarm net needs them too. `--slot` as the final argument used to be an
    IndexError: a wrapper that crashes parsing its own arguments cannot raise the
    alarm that says it crashed."""
    job, slot = "oracle", "full"
    if "--slot" in argv:
        i = argv.index("--slot") + 1
        if i < len(argv):
            slot = argv[i]
    if "--job" in argv:
        i = argv.index("--job") + 1
        if i < len(argv):
            job = argv[i]
    return job, slot


# ═══════════════════════════════════════════════════ THE ON-DEMAND EDITION
# OR-1 STEP A (ratified 2026-09-21). The same day the operator SUSPENDED the
# five-agent clock — all five labels booted out AND `launchctl disable`d, the
# plists RETAINED UNEDITED, rollback card at
# research_outputs/oracle/SUSPENDED_2026-09-21.txt — and ruled that the /oracle
# skill replaces it. This job is what the skill runs: "the chain the clock ran",
# as ONE command, under ONE lock, with ONE exit code and ONE flag decision.
#
# WHY A JOB AND NOT TWO HAND-RUN COMMANDS. Until now the only way to print an
# edition by hand was `--job topup` followed by `--job oracle`, and that pair
# carries a hazard MEASURED on 2026-09-21 itself: the 06:45 top-up FAILED (40 of
# 40 pairs, the wire was down) and raised ORACLE_DOWN.flag; the 07:00 Oracle then
# rendered cleanly ON THE STALE CACHE, exited 0, and CLEARED the flag. The alarm
# about the wire was erased fifteen minutes later by a job that never touches the
# wire. Any clean job cleared a flag raised by a different job. Here the top-up
# and the render share one rc (rc_topup or rc_oracle), so a failed top-up followed
# by a clean render ends nonzero WITH THE FLAG STANDING. F-SK-2c holds that shut.
#
# WHY THE SCHEDULE CHECK IS NOT RUN HERE. reschedule_if_drifted() reads the
# retained plists and, ON DRIFT, calls arm() — which REWRITES the plist and runs
# launchctl bootout + bootstrap. While the clock is suspended that is exactly the
# thing the ruling forbids: a laptop that changes timezone, or a plist that fails
# to parse, would have an on-demand run edit a retained plist and try to re-arm a
# disabled label. So job=ondemand never enters that loop; it prints one line
# saying so. The legacy jobs keep the loop, byte-for-byte: they only run if the
# operator rolls the clock back, and then the check is wanted again.
#
# THE FIREWALL IS UNCHANGED. The Oracle stays cache-only (BR-1b: "it may never
# fetch inside a firewalled run"). Fetching is done by two OTHER organs — the
# top-up (klines, in scope) and the movers script (STEP E, its own process) —
# and this wrapper only orders them. Nothing here reads a range or a mover; the
# Front Page summary below is three display strings per Board row, lifted from
# the Oracle's own log lines.

# The rows a ruling has not yet touched are [VETO]: builder defaults, named so
# the operator can overrule one number without reading the chain. --dry-run
# prints every unruled row (this module has no rendered appendix of its own).
ONDEMAND_REGISTER = {
    "ONDEMAND_SLOTS": {
        "value": ("on-demand-full", "on-demand-refresh"), "ruled": True,
        "source": "OR-1 STEP A, verbatim: 'Selfcheck rows tagged slot=\"on-demand-"
                  "full\"|\"on-demand-refresh\" so run-based gates can read them.' "
                  "The FIRST entry is the default when --slot is not given."},
    "TOPUP_SLOT": {
        "value": "on-demand", "ruled": False,
        "source": "[VETO] builder default. The topup_log.jsonl slot string for a "
                  "top-up run by this chain. It does not start with 'fixture-', so "
                  "oracle_topup_fixtures.last_real_run() counts it as a REAL run — "
                  "which it is."},
    "MOVERS_TIMEOUT_S": {
        "value": 600, "ruled": False,
        "source": "[VETO] builder default. Wall-clock ceiling on the movers "
                  "subprocess. Sized against the one measured wire-down figure this "
                  "lane has: a fully failing 40-pair top-up took ~10 min on "
                  "2026-09-21 (06:45 -> 06:55). A movers fetch that outlives this is "
                  "logged WIRE DOWN and the edition goes on."},
    "MOVERS_LOG_TAIL": {
        "value": 12, "ruled": False,
        "source": "[VETO] builder default. How many trailing lines of the movers "
                  "organ's own output are echoed into this log; STEP E enumerates a "
                  "universe of hundreds of symbols and the edition log is not the "
                  "place for them."},
    "FRONT_PAGE_ROWS": {
        "value": 5, "ruled": False,
        "source": "[VETO] builder default. OR-1 STEP A says 'print the Front "
                  "Page's top rows' and names no count."},
    "MOVERS_FAILURE_HOLDS_FLAG": {
        "value": False, "ruled": False,
        "source": "[VETO] builder default, and a DEVIATION the operator should rule "
                  "on. The builder brief said the flag is 'cleared ONLY if every job "
                  "that was supposed to run ran clean'. With False, a movers failure "
                  "is outside the flag's jurisdiction in BOTH directions: it never "
                  "raises the flag (contract: a movers failure does not fail the "
                  "edition) and it never holds one up — a clean top-up + clean render "
                  "CLEARS a standing flag even when the movers organ failed, because "
                  "the flag's sentence is 'The Oracle is down' and the Market Page "
                  "prints WIRE DOWN for itself. With True, a run whose movers fetch "
                  "was SUPPOSED to run and failed leaves a standing flag STANDING (it "
                  "still never raises one). F-SK-2g holds both readings to the "
                  "constant."},
    "CUT_OFF_SIGNALS": {
        "value": ("SIGTERM", "SIGHUP"), "ruled": False,
        "source": "[VETO] builder default (fix round 1, 2026-09-21). The polite ways "
                  "a harness, a shell or a logout ends a process. MEASURED by the "
                  "verifier: SIGTERM 3 s into a chain left `.oracle.lock` behind, no "
                  "flag, no selfcheck row and NOT ONE LINE of output, and every retry "
                  "was then locked out (exit 0, no edition) for LOCK_STALE_MIN. The "
                  "chain now turns these into a CUT OFF exit: lock released, flag "
                  "raised, exit 128+signum. A signal that arrives IGNORED (nohup) is "
                  "left ignored. SIGINT is deliberately absent — the __main__ net's "
                  "own ruling: an operator who stops a manual run has not discovered "
                  "an outage (the lock is still released, by the chain's finally). "
                  "SIGKILL cannot be trapped; reclaim_dead_lock is its answer."},
    "BANNER_MARKERS": {
        "value": ("LATE EDITION", "STALE DATA"), "ruled": True,
        "source": "OR-2 R-1 (2026-09-22): 'LATE EDITION — N of R rows on a stale wire "
                  "(oldest <as-of>)', which superseded OR-1 STEP F's 'Staleness banner => "
                  "red band under the masthead \"LATE EDITION — wire stale since "
                  "<as-of>\"'; and BR-1 A2-7's "
                  "'STALE DATA — ...' div, the wording before the STEP F typesetting. "
                  "Either one found in the render's TEXT (style, script, comments and "
                  "tags stripped) reads as banner UP. Loose on purpose: a false "
                  "'banner up' costs the operator a glance, a false 'none' is the "
                  "A2-7 silence again."},
    "CLOUD_MARKERS": {
        "value": ("OneDrive", "com~apple~CloudDocs", "Mobile Documents"),
        "ruled": True,
        "source": "exchange/status/CONVENTIONS.md §0 THE IDENTITY GATE, the three "
                  "patterns of its case statement, verbatim."},
}
ONDEMAND_SLOTS = ONDEMAND_REGISTER["ONDEMAND_SLOTS"]["value"]
TOPUP_SLOT = ONDEMAND_REGISTER["TOPUP_SLOT"]["value"]
MOVERS_TIMEOUT_S = ONDEMAND_REGISTER["MOVERS_TIMEOUT_S"]["value"]
MOVERS_LOG_TAIL = ONDEMAND_REGISTER["MOVERS_LOG_TAIL"]["value"]
FRONT_PAGE_ROWS = ONDEMAND_REGISTER["FRONT_PAGE_ROWS"]["value"]
MOVERS_FAILURE_HOLDS_FLAG = ONDEMAND_REGISTER["MOVERS_FAILURE_HOLDS_FLAG"]["value"]
CUT_OFF_SIGNALS = ONDEMAND_REGISTER["CUT_OFF_SIGNALS"]["value"]
BANNER_MARKERS = ONDEMAND_REGISTER["BANNER_MARKERS"]["value"]
CLOUD_MARKERS = ONDEMAND_REGISTER["CLOUD_MARKERS"]["value"]

# Module-level PATHS, like FLAG / LOCK / SELFCHECK above, so a fixture can point
# them into a TemporaryDirectory (the F-BR-12 pattern) and drive the real main().
MOVERS_SCRIPT = ROOT / "scripts" / "oracle_movers.py"
MOVERS_DIR = ROOT / "research_outputs" / "oracle" / "movers"
# Printed, never opened: a repo-relative STRING, so the line reads the same from
# any tree and no fixture that redirects ROOT can trip over it.
SUSPENDED_CARD = "research_outputs/oracle/SUSPENDED_2026-09-21.txt"

# THE CHAIN, ONCE. (step id, who performs it, one line). This tuple is the single
# source of truth: --dry-run prints it, every "STEP n <id>" log tag below is
# looked up in it, .claude/skills/oracle/SKILL.md walks it in the same order with
# the same ids, and F-SK-1 fails if any of the three disagree. The contract's own
# seven — identity gate -> flag FIRST -> movers fetch -> top-up -> oracle_daily ->
# open the render -> print the Front Page + verdict — are here in that order;
# `front-page` and `alarm` are the wrapper's half of the last one, made explicit
# because they print lines the skill has to be able to quote. The two `skill`
# rows are NOT performed by this process: a wrapper that opened a browser would
# open one under every fixture run.
ONDEMAND_STEPS = (
    ("identity-gate", "wrapper",
     "CONVENTIONS §0 two-sided gate: ROOT is $HOME/Naiad AND no cloud-tree marker "
     "in ROOT or cwd; HALT nonzero before ANY action"),
    ("flag-first", "wrapper",
     "if ORACLE_DOWN.flag is standing, print its body verbatim FIRST, before any work"),
    ("movers-fetch", "wrapper",
     "scripts/oracle_movers.py in its OWN process (STEP E organ); skipped on refresh "
     "and on --no-fetch; a failure is WIRE DOWN for movers, never a failed edition"),
    ("scope-topup", "wrapper",
     "in-scope kline top-up (oracle_topup, slot 'on-demand'); skipped on --no-fetch; "
     "a failed top-up does NOT block the render (ruling T-3)"),
    ("oracle-render", "wrapper",
     "oracle_daily, cache-only: render + the three self-checks + ONE selfcheck row "
     "tagged slot=on-demand-full|on-demand-refresh"),
    ("front-page", "wrapper",
     "print the Board's top rows by heat, the self-check verdict, the render's "
     "path / bytes / sha256, the banner state and the stale-row count"),
    ("alarm", "wrapper",
     "one rc (top-up or Oracle), one ORACLE_DOWN.flag decision; the schedule-drift "
     "check is SKIPPED (clock suspended by operator ruling 2026-09-21)"),
    ("open-render", "skill",
     "open the render (macOS: open <path>)"),
    ("report-back", "skill",
     "print back to the operator: Front Page top rows + self-check verdict + "
     "banner state + stale-row count"),
)


def _step(step_id: str) -> str:
    """The log tag for a step: '  STEP n <id>'. Looked up, never typed twice."""
    ids = [s[0] for s in ONDEMAND_STEPS]
    return f"  STEP {ids.index(step_id) + 1} {step_id}"


def ondemand_skips(slot: str, no_fetch: bool) -> dict:
    """{step id: why it is skipped on THIS invocation}. One function, read by both
    the dry run and the real chain, so the plan printed is the plan executed."""
    skips: dict[str, str] = {}
    if no_fetch:
        why = "--no-fetch: a cache-only edition fetches nothing"
        skips["movers-fetch"] = why
        skips["scope-topup"] = why
    elif slot == "on-demand-refresh":
        skips["movers-fetch"] = ("refresh edition: Watch/Board only — the Market "
                                 "Page keeps whatever movers json the day already has")
    return skips


def ondemand_plan_lines(slot: str, no_fetch: bool) -> list[str]:
    """What --dry-run prints. Pure: it reads two constants and touches nothing."""
    skips = ondemand_skips(slot, no_fetch)
    out = [f"ORACLE ON-DEMAND · DRY RUN · slot={slot}"
           f"{' · --no-fetch' if no_fetch else ''} · NOTHING IS TOUCHED "
           f"(no lock, no flag, no fetch, no render)"]
    for i, (sid, who, desc) in enumerate(ONDEMAND_STEPS, 1):
        out.append(f"  STEP {i} {sid:14} [{who}] {desc}")
        if sid in skips:
            out.append(f"         SKIPPED on this invocation — {skips[sid]}")
    out.append("  schedule: SUSPENDED by operator ruling 2026-09-21 — no run of this "
               "job checks, rewrites or re-arms a plist")
    out.append("  --install: REFUSED by this job (exit 2, nothing touched) — arming is "
               "the clock's verb, and rolling the clock back is the operator's action")
    for k, v in ONDEMAND_REGISTER.items():
        if not v["ruled"]:
            out.append(f"  [VETO] unruled constant {k} = {v['value']!r}")
    return out


def identity_gate(root: Path | None = None, home: Path | None = None,
                  cwd: Path | None = None) -> tuple[bool, str]:
    """CONVENTIONS §0 THE IDENTITY GATE, for a local run. BOTH sides, because the
    rule's own text says why: checking only the path passes a copy left behind in
    a cloud-synced tree, and checking only for the absence of markers passes any
    directory on the machine. The shell gate tests `pwd`; this process is located
    by ROOT (where the code that is about to run actually lives), and cwd is held
    to the marker side as well — a run started from inside a synced tree is
    misrouted even when the script path is right."""
    root = Path(ROOT if root is None else root).resolve()
    home = Path(Path.home() if home is None else home).resolve()
    cwd = Path(Path.cwd() if cwd is None else cwd).resolve()
    for where, p in (("ROOT", root), ("cwd", cwd)):
        hit = [m for m in CLOUD_MARKERS if m in str(p)]
        if hit:
            return False, f"cloud tree — {where} {p} carries {hit}"
    if root != home / "Naiad":
        return False, f"not $HOME/Naiad — ROOT is {root}, $HOME/Naiad is {home / 'Naiad'}"
    return True, f"ROOT {root} is $HOME/Naiad; no cloud-tree marker in ROOT or cwd ({cwd})"


def show_standing_flag(log=print) -> bool:
    """Step 2. The alarm is read BEFORE the work, not discovered after it: an
    operator asking for an edition while the flag stands must be told, first, that
    the last run failed and why. Verbatim means verbatim — the body is printed
    unindented between two rules, byte for byte as raise_flag() wrote it."""
    tag = _step("flag-first")
    if not FLAG.exists():
        log(f"{tag}: no {FLAG.name} standing")
        return False
    try:
        body = FLAG.read_text(encoding="utf-8")
    except Exception as e:
        log(f"{tag}: {FLAG.name} IS STANDING at {FLAG} but could not be read: {e}")
        return True
    log(f"{tag}: {FLAG.name} IS STANDING — its body, verbatim, before any work:")
    log(f"  -------- {FLAG} --------")
    log(body.rstrip("\n"))
    log(f"  -------- end of {FLAG.name} --------")
    return True


def run_movers(log=print) -> dict:
    """Step 3. The Market Page's fetch — STEP E's organ, in ITS OWN PROCESS, so the
    wrapper never imports a module that talks to the network and the Oracle's
    cache-only property cannot be bent from here. CLI contract (OR-1 STEP E): no
    arguments; exit 0 = movers json written; exit 1 = fetch failed and the organ
    wrote its own status-FAIL json.

    A MOVERS FAILURE IS NOT AN ORACLE FAILURE. The page prints 'WIRE DOWN — no
    movers this edition' and the rest of the paper is whole, so nothing here
    touches rc and nothing here raises the flag. It is logged plainly instead."""
    tag = _step("movers-fetch")
    out = {"ran": False, "ok": False, "rc": None}
    if not MOVERS_SCRIPT.exists():
        log(f"{tag}: WIRE DOWN for movers — {MOVERS_SCRIPT} does not exist; the "
            f"edition goes on without a fresh Market Page")
        return out
    log(f"{tag}: running {MOVERS_SCRIPT.name} in its own process "
        f"(timeout {MOVERS_TIMEOUT_S} s)")
    t0 = datetime.now(timezone.utc)
    try:
        r = subprocess.run([PY, str(MOVERS_SCRIPT)], cwd=str(ROOT),
                           capture_output=True, text=True, timeout=MOVERS_TIMEOUT_S)
    except subprocess.TimeoutExpired:
        log(f"{tag}: WIRE DOWN for movers — no answer inside {MOVERS_TIMEOUT_S} s, "
            f"process killed; the edition goes on")
        return {**out, "ran": True}
    except Exception as e:
        log(f"{tag}: WIRE DOWN for movers — could not start the organ: "
            f"{e.__class__.__name__}: {e}; the edition goes on")
        return out
    secs = (datetime.now(timezone.utc) - t0).total_seconds()
    for line in ((r.stdout or "") + (r.stderr or "")).splitlines()[-MOVERS_LOG_TAIL:]:
        log(f"    movers| {line}")
    if r.returncode != 0:
        log(f"{tag}: WIRE DOWN for movers — {MOVERS_SCRIPT.name} exited "
            f"{r.returncode} after {secs:.1f} s; the Market Page will say so; the "
            f"edition goes on (a movers failure never fails the edition and never "
            f"raises the flag)")
        return {"ran": True, "ok": False, "rc": r.returncode}
    newest = sorted(MOVERS_DIR.glob("movers_*.json")) if MOVERS_DIR.exists() else []
    if not newest:
        # Reported, not judged: the organ said OK, and what the Market Page makes
        # of an empty directory is the Oracle's call (it prints WIRE DOWN).
        log(f"{tag}: exit 0 after {secs:.1f} s, but there is NO movers_*.json under "
            f"{MOVERS_DIR} — the Market Page will have nothing to read")
        return {"ran": True, "ok": False, "rc": 0}
    log(f"{tag}: OK (exit 0, {secs:.1f} s) — {newest[-1]} "
        f"{newest[-1].stat().st_size:,} B")
    return {"ran": True, "ok": True, "rc": 0}


# The Oracle's own per-asset log line (oracle_daily.build_view). F-SK-1 renders this
# very f-string OUT OF oracle_daily.build_view by AST and asserts this regex matches
# it and recovers symbol/station/heat; a format change over there reddens the suite,
# which is the point — front_page() would otherwise report "the Oracle did not get as
# far as the Board" for a run that logged all 18 rows and printed the edition.
#   "  BTCUSDT        ARMED      heat= 6.248 levels= 35 clusters= 14 atr_d=2376.77"
# and this wrapper's own render line (run_oracle):
#   "  render /…/oracle_2026-09-21.html sha256 <64 hex>"
# WHY THE LOG AND NOT THE TAPE: the tape's `station` column is the WINDOW's
# station for any asset that has a window, so the Board word is not recoverable
# from it; the log line carries exactly the three strings the Board row shows.
# Anything after `heat=` is ignored, so a later column on that line costs nothing.
_BOARD_LINE = re.compile(r"^\s+(?P<sym>[A-Z0-9]+)\s+(?P<station>[A-Z][A-Z_-]*)\s+"
                         r"heat=\s*(?P<heat>-?\d+(?:\.\d+)?|nan|inf)\b")
_RENDER_LINE = re.compile(r"^\s+render (?P<path>.+) sha256 (?P<sha>[0-9a-f]{64})\s*$")

# oracle_daily.run()'s OWN line, logged immediately after it writes the html:
#   "  /…/oracle_2026-09-21.html 451,312 B sha256 <64 hex>"
_CUT_HTML_LINE = re.compile(
    r"^\s+(?P<path>.+?oracle_\d{4}-\d\d-\d\d\.html) [\d,]+ B sha256 [0-9a-f]{64}\s*$")


def _cut_render_path(lines: list[str]) -> str | None:
    """The edition oracle_daily.run() had ALREADY WRITTEN when a signal landed.
    Read from the tee — run()'s own `  <path> <n> B sha256 <sha>` line (logged at
    oracle_daily.py:2474, immediately after the write at :2472) or the wrapper's
    later `render` line — because a boolean set after run_oracle RETURNS cannot
    see a cut that happened inside it."""
    for ln in reversed(lines):
        m = _CUT_HTML_LINE.match(ln) or _RENDER_LINE.match(ln)
        if m:
            return m.group("path")
    return None


def banner_state(html_path: Path) -> str:
    """UP or none, read from the render's TEXT. Display-only: it changes nothing,
    it only lets the log say what the operator is about to see under the masthead."""
    text = Path(html_path).read_text(encoding="utf-8", errors="replace")
    text = re.sub(r"(?is)<(style|script)\b.*?</\1\s*>|<!--.*?-->", " ", text)
    text = re.sub(r"\s+", " ", re.sub(r"(?s)<[^>]+>", " ", text))
    for marker in BANNER_MARKERS:
        i = text.find(marker)
        if i >= 0:
            return f"UP — {text[i:i + 200].strip()}"
    return "none — no staleness band in this render"


_STALE_COUNT = re.compile(r"\b(\d+) of (\d+) rows stale\b")


def stale_state(html_path: Path) -> str:
    """OR-2 R-1 · how many Board rows went to press on a stale wire, read off the
    render's DATELINE ('<n> of <R> rows stale'). The page, not oracle_daily's
    constants: this process never judges staleness itself, and a render printed
    before R-1 carries no count and says so."""
    text = Path(html_path).read_text(encoding="utf-8", errors="replace")
    m = re.search(r'(?s)<p class="dateline">(.*?)</p>', text)
    c = _STALE_COUNT.search(re.sub(r"\s+", " ", m.group(1))) if m else None
    if c is None:
        return "unknown — this render prints no stale-row count (printed before OR-2 R-1?)"
    n, r = int(c.group(1)), int(c.group(2))
    return (f"{n} of {r} Board rows on a stale wire"
            + (" — their R1 lines are HELD out of the paste block" if n else ""))


def front_page(lines: list[str], slot: str, started: datetime, log=print) -> None:
    """Step 6. `lines` is everything run_oracle logged for THIS run (a tee)."""
    log(f"{_step('front-page')}:")
    rows = []
    for ln in lines:
        m = _BOARD_LINE.match(ln)
        if m:
            h = float(m.group("heat"))
            rows.append((m.group("sym"), m.group("station"), h))
    rows.sort(key=lambda r: -(r[2] if r[2] == r[2] else float("-inf")))
    if rows:
        top = rows[:FRONT_PAGE_ROWS]
        log(f"  FRONT PAGE — top {len(top)} of {len(rows)} Board rows by heat")
        for i, (sym, station, heat) in enumerate(top, 1):
            log(f"    {i:>2}  {sym:14} {station:10} heat={heat:6.3f}")
    else:
        log("  FRONT PAGE — no Board row was logged by this run (the Oracle did "
            "not get as far as the Board)")

    # parsed, not string-compared: isoformat() drops the fraction on a whole second
    mine = [r for r in selfcheck_rows() if r.get("slot") == slot
            for t in [_row_time(r, timezone.utc)] if t and t >= started]
    if mine:
        row = mine[-1]
        parts = " · ".join(f"{k} {'PASS' if v.get('pass') else 'FAIL'}"
                           for k, v in sorted(row.get("checks", {}).items()))
        log(f"  SELF-CHECK VERDICT: {row.get('verdict')} — {parts} "
            f"(row slot={row.get('slot')})")
    else:
        log(f"  SELF-CHECK VERDICT: NONE — no selfcheck row for slot={slot} was "
            f"written by this run")

    hit = next((m for m in map(_RENDER_LINE.match, reversed(lines)) if m), None)
    if hit is None:
        log("  RENDER none — the Oracle did not render on this run")
        log("  BANNER unknown — there is no render to read")
        log("  STALE unknown — there is no render to read")
        return
    p = Path(hit.group("path"))
    size = f"{p.stat().st_size:,} B" if p.exists() else "MISSING ON DISK"
    log(f"  RENDER {p} · {size} · sha256 {hit.group('sha')}")
    try:
        log(f"  BANNER {banner_state(p)}")
    except Exception as e:
        log(f"  BANNER unknown — {e.__class__.__name__}: {e}")
    try:
        log(f"  STALE {stale_state(p)}")
    except Exception as e:
        log(f"  STALE unknown — {e.__class__.__name__}: {e}")


def ondemand_flag_action(rc: int, no_fetch: bool, movers_failed: bool = False) -> str:
    """'raise' | 'clear' | 'stand'. The whole alarm policy of this job, as a pure
    function so F-SK-2 can replant the old rule and watch it go red.

    raise — rc != 0. rc is (rc_topup or rc_oracle), so a failed top-up under a
            clean render raises: the 2026-09-21 hazard, closed.
    stand — a --no-fetch run. It read the cache only; it PROVES NOTHING ABOUT THE
            WIRE, and the wire is what most standing flags are about. It can raise
            an alarm (a render that crashes is a render that crashes) but it has no
            all-clear to give.
    clear — rc == 0 on a run that fetched: the top-up AND the Oracle both ran and
            both came back clean. The movers organ is outside this on purpose, in
            both directions — it never raises the flag, so it never holds it up;
            the flag's sentence is 'The Oracle is down', and the Market Page says
            WIRE DOWN for itself. THAT HALF IS UNRULED: it is the [VETO] row
            MOVERS_FAILURE_HOLDS_FLAG, and set True it turns this clear into a
            'stand' when the movers fetch was supposed to run and failed. Either
            way a movers failure NEVER returns 'raise' — that half is the contract's."""
    if rc != 0:
        return "raise"
    if no_fetch:
        return "stand"
    if movers_failed and MOVERS_FAILURE_HOLDS_FLAG:
        return "stand"
    return "clear"


# ── THE CUT-OFF RUN (fix round 1, 2026-09-21). The edition is typed by hand and
# usually run by an agent under a harness with a foreground ceiling; with the wire
# down the chain outlives that ceiling (72 pairs at the measured 2026-09-21 rate is
# ~19 min). MEASURED before this block existed: SIGTERM three seconds in left the
# lock on disk, no flag, no selfcheck row and an EMPTY capture — stdout is
# block-buffered on a pipe — and the next run, `--no-fetch` included, stood down on
# that lock with exit 0 and no edition. Silence, then a lock-out, in exactly the
# wire-down case T-3 and T-7 were built for. Three answers, all scoped to this job:
#   1. every line this job logs is FLUSHED as it is logged (run_ondemand's `log`);
#   2. CUT_OFF_SIGNALS become an exception the chain's own try/finally sees, so the
#      lock is released, the flag is raised saying which step was cut, exit 128+n;
#   3. a lock whose holder's pid is NOT RUNNING is reclaimed before acquire_lock is
#      asked — the answer to SIGKILL and power loss, which nothing can trap.
# acquire_lock itself is untouched (age-only, as the legacy jobs have always had it).

class CutOff(BaseException):
    """BaseException ON PURPOSE: run_topup and run_oracle catch Exception (and
    run_topup SystemExit), and a run that is being ended must not be swallowed by
    the nets built for a run that failed."""

    def __init__(self, signum: int):
        super().__init__(signum)
        self.signum = int(signum)


def trap_cut_off() -> dict:
    """Install the CUT_OFF_SIGNALS handlers; return what was there, for untrap.
    ONE CutOff per run: the handler sets every trapped signal to IGNORE before it
    raises, so the clean-up it triggers (release the lock, raise the flag) cannot
    itself be cut by a second, impatient signal."""
    import signal
    prev: dict = {}

    def _cut(signum, frame):
        for s in prev:
            signal.signal(s, signal.SIG_IGN)
        raise CutOff(signum)

    for name in CUT_OFF_SIGNALS:
        s = getattr(signal, name, None)
        if s is None:
            continue
        try:
            if signal.getsignal(s) == signal.SIG_IGN:
                continue                  # nohup said ignore it; it stays ignored
            prev[s] = signal.signal(s, _cut)
        except (ValueError, OSError):     # not the main thread: nothing to trap
            pass
    return prev


def untrap_cut_off(prev: dict) -> None:
    import signal
    for s, handler in prev.items():
        try:
            signal.signal(s, signal.SIG_DFL if handler is None else handler)
        except (ValueError, OSError):
            pass


def _pid_running(pid) -> bool:
    """False ONLY on proof. Anything that is not a positive int, or any answer other
    than 'no such process', reads as running — so a doubt falls back to
    acquire_lock's age rule and never to a reclaim. (pid <= 0 is refused before
    os.kill sees it: kill(0, …) addresses the whole process group.)"""
    if isinstance(pid, bool) or not isinstance(pid, int) or pid <= 0:
        return True
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except Exception:                     # PermissionError: running, someone else's
        return True
    return True


def reclaim_dead_lock(log=print) -> bool:
    """True if a lock was standing whose holder is PROVABLY not running, and it is
    now gone. A lock that cannot be read is left to acquire_lock (unreadable =
    stale, its own rule). The body is re-read immediately before the unlink so a
    lock some other run took in between is not the one removed."""
    try:
        raw = LOCK.read_text()
        held = json.loads(raw)
    except Exception:
        return False
    if not isinstance(held, dict) or _pid_running(held.get("pid")):
        return False
    try:
        if LOCK.read_text() != raw:
            return False
        LOCK.unlink()
    except Exception:
        return False
    log(f"  DEAD LOCK from {held.get('who')} (pid {held.get('pid')} is not running — "
        f"that run was cut off before it could release; stamped {held.get('ts')}) — "
        f"reclaiming it")
    return True


def live_lock_holder(log=print) -> dict | None:
    """The lock's body when a lock is standing whose pid is PROVABLY running.

    SCOPED TO job=ondemand, the same precedent as THE CUT-OFF RUN answer 3.
    acquire_lock's stale rule is AGE ONLY (legacy, shared with the clock jobs):
    past LOCK_STALE_MIN it would take the lock from a holder that is still
    working, and two editions would then write one oracle_<date>.html and one
    oracle_tape_<date>.parquet, neither write atomic, plus two selfcheck rows
    for one operator request — and the FIRST run's `finally: release_lock()`
    would then unlink the SECOND run's lock and let a third in. A wire-down full
    edition is no longer well inside 30 min: 72 pinned pairs x >= 15 s per
    failing engine.data._get (MEASURED floor: 1.5+3+4.5+6 s of backoff) = >= 18
    min, plus MOVERS_TIMEOUT_S = 600 s and the render. So this job never reclaims
    on age from a live pid; a DEAD holder is still reclaimed, by
    reclaim_dead_lock, on the spot."""
    try:
        held = json.loads(LOCK.read_text())
    except Exception:
        return None                  # unreadable: acquire_lock's own rule decides
    return held if isinstance(held, dict) and _pid_running(held.get("pid")) else None


def run_ondemand(argv: list[str], log=print) -> int:
    """--job ondemand. The chain in ONDEMAND_STEPS, steps 1-7, in that order."""
    say = log

    def log(msg="") -> None:              # THE CUT-OFF RUN, answer 1: line by line
        # A reader that went away (a harness that stopped listening, a closed pipe)
        # must not take the edition or the flag decision with it: the log is the
        # least of the three, so a line that cannot be written is dropped.
        try:
            say(msg)
            sys.stdout.flush()
        except OSError:
            pass

    if "--install" in argv:
        # Refused FIRST and by name, not left to the stray-argument net below: this
        # is the one flag whose legacy meaning is "rewrite five plists, bootout,
        # bootstrap". main() sends every argv that names the on-demand edition here
        # BEFORE it looks for --install, so this line is the only thing --install
        # can reach from such an argv — `--dry-run` alongside it included.
        log(f"HALT: --job ondemand REFUSES --install. The five com.naiad.oracle-* "
            f"agents are SUSPENDED by operator ruling 2026-09-21 and this job never "
            f"arms, rewrites or bootstraps one; rolling the clock back is the "
            f"operator's action (rollback card {SUSPENDED_CARD}). Nothing was touched.")
        return 2
    _, slot = _argv_job_slot(argv)
    if "--slot" not in argv:
        slot = ONDEMAND_SLOTS[0]
    no_fetch = "--no-fetch" in argv
    if slot not in ONDEMAND_SLOTS:
        # A free slot string here would write a selfcheck row no run-based gate
        # knows how to read — refuse it before anything is touched.
        log(f"HALT: --job ondemand takes --slot {' | '.join(ONDEMAND_SLOTS)} "
            f"(got {slot!r}). Nothing was touched.")
        return 2
    stray = [a for a in argv if a not in
             ("--job", "ondemand", "--slot", slot, "--no-fetch", "--dry-run")]
    if stray:
        # `--nofetch` must not quietly become a run that fetches. The legacy jobs
        # ignore what they do not know; this one is typed by hand, so it refuses.
        log(f"HALT: --job ondemand does not know {stray}. It takes --slot "
            f"{' | '.join(ONDEMAND_SLOTS)}, --no-fetch, --dry-run. Nothing was touched.")
        return 2
    if "--dry-run" in argv:
        for line in ondemand_plan_lines(slot, no_fetch):
            log(line)
        return 0

    started = datetime.now(timezone.utc)
    log(f"=== ORACLE WRAPPER · job=ondemand slot={slot}"
        f"{' --no-fetch' if no_fetch else ''} · {started.isoformat()} ===")
    zr = zone_report()
    log(f"  zone: {zr}")

    ok, why = identity_gate()
    if not ok:
        # "halts before ANY action" — so no lock, and NO FLAG either: the flag
        # lives at ROOT, and writing into a tree the gate has just refused is the
        # misrouted write the gate exists to stop.
        log(f"{_step('identity-gate')}: HALT: {why}")
        log("=== exit 2 (identity gate — nothing was touched: no lock, no flag, "
            "no fetch, no render) ===")
        return 2
    log(f"{_step('identity-gate')}: PASS — {why}")

    show_standing_flag(log=log)

    prev = trap_cut_off()                 # THE CUT-OFF RUN, answer 2
    try:
        return _ondemand_locked(slot, no_fetch, zr, started, log)
    finally:
        untrap_cut_off(prev)


def _ondemand_locked(slot: str, no_fetch: bool, zr: dict, started: datetime,
                     log=print) -> int:
    """Steps 3-7: everything that happens under the lock, and the alarm after it.
    Split from run_ondemand only so the signal trap can wrap ALL of it — the flag
    decision included — in one try/finally."""
    skips = ondemand_skips(slot, no_fetch)
    rc_t = rc_o = 0
    rc: int | None = None
    locked = rendered = movers_failed = False
    doing: str | None = None              # the step a CutOff lands in, for the flag
    lines: list[str] = []

    def tee(msg="") -> None:
        lines.append(str(msg))
        log(msg)

    try:
        reclaim_dead_lock(log=log)        # THE CUT-OFF RUN, answer 3
        held = live_lock_holder(log=log)  # SINGLE FLIGHT: never reclaim from a LIVE pid
        if held is not None:
            age = "unknown"
            try:
                held_for = datetime.now(timezone.utc) - datetime.fromisoformat(held["ts"])
                age = f"{held_for.total_seconds() / 60.0:.1f}"
            except Exception:
                pass
            log(f"  LOCK HELD by a LIVE pid: {held.get('who')} (pid {held.get('pid')}, "
                f"{age} min old) — standing down. Past {LOCK_STALE_MIN} min this is "
                f"LONGER THAN EXPECTED but NOT reclaimable: with the wire down a full "
                f"edition can outlive that. Wait, or end that run (its pid) and run "
                f"again — the dead lock is then reclaimed on the spot.")
            log("=== exit 0 (no-op: another Oracle run holds the lock — NO EDITION "
                "WAS PRINTED by this run) ===")
            return 0
        locked = acquire_lock(f"ondemand/{slot}", log=log)
        if not locked:
            log("=== exit 0 (no-op: another Oracle run holds the lock — NO EDITION "
                "WAS PRINTED by this run) ===")
            return 0

        doing = "movers-fetch"
        if "movers-fetch" in skips:
            log(f"{_step('movers-fetch')}: SKIPPED — {skips['movers-fetch']}")
        else:
            movers_failed = not run_movers(log=log)["ok"]

        doing = "scope-topup"
        if "scope-topup" in skips:
            log(f"{_step('scope-topup')}: SKIPPED — {skips['scope-topup']}")
        else:
            log(f"{_step('scope-topup')}: slot={TOPUP_SLOT}")
            noted = len(FAILURES)
            rc_t = run_topup(TOPUP_SLOT, log=log)
            if rc_t != 0:
                if len(FAILURES) == noted:
                    # A top-up whose pairs ERROR returns verdict FAIL without
                    # raising, so the alarm would otherwise have nothing to show.
                    note_failure(f"TOP-UP DID NOT PASS (rc {rc_t}, slot {TOPUP_SLOT}) "
                                 f"— per-pair detail is the newest row of "
                                 f"research_outputs/oracle/calibration/topup_log.jsonl")
                log(f"{_step('scope-topup')}: NOT CLEAN (rc {rc_t}) — the edition "
                    f"renders anyway, on the cache as it stands (ruling T-3); the "
                    f"banner tells the truth and this run will exit nonzero")

        doing = "oracle-render"
        log(f"{_step('oracle-render')}: slot={slot}")
        rc_o = run_oracle(slot, zr, started, log=tee)
        rendered = True

        doing = "front-page"
        try:
            front_page(lines, slot, started, log=log)
        except Exception as e:
            # The summary is a courtesy printed AFTER the edition and its row are
            # on disk. It may fail to print; it may not fail the edition.
            log(f"  front page summary unavailable: {e.__class__.__name__}: {e}")
        rc = rc_t or rc_o
    except CutOff as cut:
        import signal
        rc = 128 + cut.signum
        where = (_step(doing).strip() if doing else
                 "the lock acquisition (after STEP 2, before STEP 3)")
        # THREE WAYS, NOT TWO (review finding, 2026-09-21). `rendered` is a boolean
        # set only AFTER run_oracle RETURNS, but oracle_daily.run() writes the whole
        # HTML at :2472 and only then the D-4 tape (:2476), the sibling range tape
        # (:2480, A-OR1-1 v), the calibration (:2482) and — back here — the selfcheck
        # row. A signal landing anywhere in that window (a
        # closed session, a harness stopping the background job, a logout) used to
        # print "NO EDITION WAS PRINTED by this run" one line below the log line
        # naming the edition it had just written — an orphan, current-dated, that
        # G-BR2-1's count of dated editions will pick up and that catchup_due()'s own
        # docstring warns about ("a file a FAILED run also writes cannot be the
        # evidence that the run succeeded"). The sentence matters TWICE: it is also
        # the ORACLE_DOWN.flag body, which the next run's STEP 2 prints verbatim, and
        # SKILL.md:73 quotes it and tells the agent to relay it in these words. So the
        # no-render sentence stays BYTE-IDENTICAL, and the new middle case says only
        # what the log can actually see: an edition exists, it is UNVERIFIED, and
        # whether the two tapes and the calibration record were written is unknown.
        on_disk = _cut_render_path(lines)
        if rendered:
            said = "the edition and its selfcheck row were already on disk"
        elif on_disk is not None:
            said = (f"NO SELFCHECK ROW WAS WRITTEN, so no run-based gate counts this "
                    f"run — but an edition was already written to {on_disk} before "
                    f"the signal landed. It is UNVERIFIED: the self-checks did not "
                    f"run, and the D-4 tape row, the sibling range tape and the "
                    f"calibration record may or may not have been written. It is "
                    f"not the record of a completed run; print the edition again")
        else:
            said = ("NO EDITION WAS PRINTED by this run and no selfcheck row was "
                    "written")
        log("  " + note_failure(
            f"CUT OFF by signal {cut.signum} ({signal.Signals(cut.signum).name}) "
            f"during {where} — " + said
            + f"; the lock is released and the run exits {rc}. Run it again DETACHED "
              f"(.claude/skills/oracle/SKILL.md): with the wire down a full edition "
              f"outlives any foreground timeout"))
    except Exception:
        rc = 1
        log("  WRAPPER FAILED:\n" + note_failure())
    finally:
        if locked:
            release_lock(log=log)

    log(f"{_step('alarm')}: rc_topup={rc_t} rc_oracle={rc_o} -> exit {rc}")
    log(f"  schedule: SUSPENDED by operator ruling 2026-09-21 — the drift check is "
        f"SKIPPED for job=ondemand (on drift it would rewrite a retained plist and "
        f"bootstrap it); rollback card {SUSPENDED_CARD}")
    action = ondemand_flag_action(rc, no_fetch, movers_failed)
    if action == "raise":
        raise_flag("ondemand", slot, rc, log=log)
    elif action == "clear":
        if FLAG.exists():
            clear_flag(log=log)          # says CLEARED, or says why it could not
        else:
            log(f"  no {FLAG.name} standing — nothing to clear")
    elif not no_fetch:
        # 'stand' on a run that fetched: only MOVERS_FAILURE_HOLDS_FLAG gets here.
        head = (f"alarm left standing: {FLAG.name}" if FLAG.exists()
                else f"no {FLAG.name} standing")
        log(f"  {head} — the movers fetch was supposed to run and did not come back "
            f"clean, and MOVERS_FAILURE_HOLDS_FLAG is set: this run has no all-clear "
            f"to give")
    elif FLAG.exists():
        log(f"  alarm left standing: {FLAG.name} — a --no-fetch run reads the cache "
            f"only and proves nothing about the wire, so it has no all-clear to give")
    else:
        log(f"  no {FLAG.name} standing (a --no-fetch run could not have cleared one)")

    log(f"=== exit {rc} ===")
    return rc


def names_ondemand(argv: list[str]) -> bool:
    """Does this argv NAME THE ON-DEMAND EDITION? `--job ondemand` does — and so,
    for the ONE purpose of keeping --install away from it, does any token spelling
    'ondemand' or 'on-demand' (`--job=ondemand`, a bare `--slot on-demand-full`):
    an argv typed for the edition must never be read as the clock's arming verb
    because its --job was mistyped. No argv the clock or its plists ever wrote
    carries either spelling, so every legacy argv is judged exactly as before."""
    if _argv_job_slot(argv)[0] == "ondemand":
        return True
    return "--install" in argv and any(
        "ondemand" in a.lower() or "on-demand" in a.lower() for a in argv)


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    log = print
    if names_ondemand(argv):
        # OR-1 STEP A — and FIRST, ahead of --install (fix round 1, 2026-09-21).
        # Its own chain, its own flag rule, NO schedule loop and NO arming: it
        # returns here so nothing below (the legacy path, byte-for-byte as it
        # was) can run on its behalf. Dispatched after --install, as it first
        # was, `--job ondemand --dry-run --install` reached the arming branch for
        # all five suspended labels and printed no dry run (what that branch does
        # against a DISABLED label is a rewritten plist and an untrue ARMED line,
        # not an armed agent). See THE ON-DEMAND EDITION; F-SK-2e.
        return run_ondemand(argv, log=log)
    if "--install" in argv or REARM_FLAG in argv:
        # OR-2 R-4 — the guard answers BEFORE anything is printed or touched.
        refusal = install_refusal(argv)
        if refusal is not None:
            log(refusal)
            return 2
        rearm = REARM_FLAG in argv
        log(f"ORACLE — arming {len(SLOTS)} slots"
            + (" · EXPLICIT RE-ARM (enable, bootstrap, verify)" if rearm else ""))
        zr = zone_report()
        log(f"  zone check: oracle {zr['oracle_now']} · machine {zr['machine_now']} · "
            f"agree={zr['zones_agree']}")
        armed = [arm(label, log=log, enable=rearm) for label in SLOTS]
        log("")
        for line in undo_lines():
            log(line)
        print(json.dumps({"armed": armed, "zone": zr}, indent=1))
        bad = [a["label"] for a in armed if not a.get("armed")]
        if rearm and SCHEDULE_SENTINEL.exists():
            log(f"  the sentinel {SCHEDULE_SENTINEL_REL} is LEFT IN PLACE: removing it is "
                f"the operator's act, once `launchctl list | grep -c com.naiad.oracle` "
                f"reads {len(SLOTS)}")
        # lower case ON PURPOSE: this line is not an `  ARMED <label>` line
        log(f"  armed {len(armed) - len(bad)} of {len(armed)} · exit {1 if bad else 0}"
            + (f" · not armed: {', '.join(bad)}" if bad else ""))
        return 1 if bad else 0

    job, slot = _argv_job_slot(argv)
    started = datetime.now(timezone.utc)
    log(f"=== ORACLE WRAPPER · job={job} slot={slot} · {started.isoformat()} ===")
    zr = zone_report()
    log(f"  zone: {zr}")
    if not acquire_lock(f"{job}/{slot}", log=log):
        # No work done, so no all-clear to give: a standing alarm stays standing.
        log("=== exit 0 (no-op: another Oracle run holds the lock) ===")
        return 0
    worked = False
    try:
        if job == "topup":
            rc = run_topup(slot, log=log)
            worked = True
        elif job == "catchup":
            rc, worked = run_catchup(zr, started, log=log)
        else:
            rc = run_oracle(slot, zr, started, log=log)
            worked = True
    except Exception:
        # run_topup and run_oracle catch their own, so nothing should reach here.
        # An alarm that only fires on the failures we anticipated is the
        # 2026-08-20 silence wearing a different coat.
        rc = 1
        log("  WRAPPER FAILED:\n" + note_failure())
    finally:
        release_lock(log=log)

    # The self-reschedule runs LAST, so a bootout can never kill the run that
    # is producing today's Oracle.
    for label in SLOTS:
        try:
            d = reschedule_if_drifted(label, log=log)
            if d.get("missing"):
                rc = rc or 1
                note_failure(f"AGENT MISSING — {label} has no plist; the slot it "
                             f"carries will not fire. Re-arm: oracle_wrapper.py "
                             f"--install (while {SCHEDULE_SENTINEL_REL} exists: "
                             f"--install --rearm)")
            elif not d["drift"]:
                log(f"  schedule OK on {label}: {d['want']}")
        except Exception as e:
            log(f"  reschedule check failed on {label}: {e}")

    # ── T-7 · THE ALARM. From here every exit tells the operator one of exactly
    # two things: the flag is up, or the flag is down.
    if rc != 0:
        raise_flag(job, slot, rc, log=log)
    elif worked:
        clear_flag(log=log)
    elif FLAG.exists():
        log(f"  alarm left standing: {FLAG.name} — this run did no work, so it "
            f"has no all-clear to give")

    log(f"=== exit {rc} ===")
    return rc


if __name__ == "__main__":
    # THE OUTERMOST NET (T-7). main() carries no top-level try of its own — argv
    # parsing, zone_report() and acquire_lock() all sit outside one — so a crash
    # in any of them would exit nonzero with the alarm silent, which is precisely
    # the failure T-7 exists to end. KeyboardInterrupt is deliberately NOT caught:
    # an operator who stops a manual run has not discovered an outage.
    try:
        _rc = main()
    except Exception:
        _job, _slot = _argv_job_slot(list(sys.argv[1:]))
        print("  WRAPPER CRASHED BEFORE IT COULD REPORT:\n" + note_failure())
        raise_flag(_job, _slot, 1)
        raise
    raise SystemExit(_rc)
