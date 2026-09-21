"""THE ORACLE WRAPPER — D-3 of queue BR-1. Slot-anchored, self-rescheduling.

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

It also runs the daily self-checks and appends PASS/FAIL to
research_outputs/oracle/calibration/selfcheck_log.jsonl — the log BR-2 gate
G-BR2-2 reads.

FIVE AGENTS, NOT FOUR (A2-8, 2026-08-21). The four above are clock agents. The
fifth, com.naiad.oracle-catchup, has no clock at all: it carries RunAtLoad and
fires once per login/boot, asks whether the most recent slot boundary actually
produced a brief, and runs the missed slot if it did not. It exists because
launchd replays a missed calendar job on WAKE but not on BOOT — measured on this
host, see THE CATCH-UP below — so a laptop that was shut down over a slot lost
that slot silently, twice in the six days to 2026-08-21.

THE ALARM (T-7, ruled 2026-08-22). A wrapper that exits nonzero into a log
nobody opens is the 2026-08-20 silence. Any run that ends rc != 0 now writes
ORACLE_DOWN.flag at the top of the repo — timestamp, job, slot, exit code, the
last 15 traceback lines — and any run that actually did work and ended rc == 0
removes it again. The flag is gitignored: it is for the operator standing at
the machine, never for the bus.

THE ON-DEMAND EDITION (OR-1 STEP A, 2026-09-21). The operator suspended the five
agents above — booted out AND disabled, plists retained unedited — and ruled that
the /oracle skill replaces the clock. `--job ondemand` is what that skill runs:
identity gate, the standing flag printed FIRST, the movers fetch in its own
process, the in-scope top-up, the cache-only Oracle, a Front Page summary — one
lock, one exit code, one flag decision, and NO schedule-drift check (on drift
that check rewrites a plist and bootstraps it, which the suspension forbids).
ONDEMAND_STEPS is the chain; `--job ondemand --dry-run` prints it and touches
nothing. See THE ON-DEMAND EDITION below. The four legacy paths (oracle, topup,
catchup, --install) are unchanged.

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

# label -> {slot, hour, minute, job}. Times are in the ORACLE's zone, never the
# machine's; `machine_local_time_for` resolves them through the zone each run.
# job "oracle" renders the organ; job "topup" is BR-1b's fetch-and-store, armed
# 15 minutes ahead of each Oracle slot so the cache is fresh before it is read.
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
    # carries RunAtLoad instead and fires once at every login/boot. See THE
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
    out = subprocess.run(["launchctl", "print", f"gui/{UID}/{label}"],
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


def arm(label: str, log=print) -> dict:
    p, h, m = write_plist(label)
    subprocess.run(["launchctl", "bootout", f"gui/{UID}/{label}"],
                   capture_output=True, text=True)
    r = subprocess.run(["launchctl", "bootstrap", f"gui/{UID}", str(p)],
                       capture_output=True, text=True)
    lint = subprocess.run(["plutil", "-lint", str(p)], capture_output=True, text=True)
    sched = loaded_schedule(label)
    cfg = SLOTS[label]
    when = (f"machine-local {h:02d}:{m:02d} "
            f"(= {cfg['hour']:02d}:{cfg['minute']:02d} {ZONE})"
            if h is not None else "no clock · RunAtLoad, once per login/boot")
    log(f"  ARMED {label} [{cfg['job']}]: {when} · plist {p}")
    log(f"    plutil: {lint.stdout.strip() or lint.stderr.strip()}")
    log(f"    launchd reports: {sched}")
    if r.returncode != 0:
        log(f"    bootstrap stderr: {r.stderr.strip()}")
    return {"label": label, "plist": str(p), "hour": h, "minute": m,
            "bootstrap_rc": r.returncode, "schedule_from_launchd": sched}


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
                f"NOT armed. Re-arm with: oracle_wrapper.py --install")
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
    if drift:
        log(f"  SCHEDULE DRIFT on {label}: plist says {have}, the zone says "
            f"{{'Hour': {want_h}, 'Minute': {want_m}}} — rewriting and reloading")
        arm(label, log=log)
    return {"label": label, "drift": drift, "want": {"Hour": want_h, "Minute": want_m},
            "had": have}


# ══════════════════════════════════════════════════════════════ SINGLE FLIGHT
# D4 of the 2026-08-22 incident audit. Before the catch-up existed, every Oracle
# job was a distinct calendar slot and two could not overlap. The catch-up can
# fire at a login that lands while a clock slot is still running — a top-up takes
# ~130 s wall-clock (measured: 09:45:04 -> 09:47:14) — and both paths append to
# the SAME dated tape parquet and the same selfcheck log. One writer at a time.
#
# A plain O_EXCL file, not flock: the holder must survive being inspected by an
# operator, and a stale lock from a killed run must be recoverable without a
# reboot. STALE_MIN is generous — the longest observed run is well under it.
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
    """Three daily checks, per D-3: refresh idempotence, thumbnail provenance,
    tape append integrity. Results append to selfcheck_log.jsonl for BR-2 G-BR2-2."""
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

    try:
        import pandas as pd
        t = sorted(OD.TAPE_DIR.glob("oracle_tape_*.parquet"))
        df = pd.read_parquet(t[-1])
        missing = [c for c in OD.TAPE_COLS if c not in df.columns]
        # the same stemmed, component-wise matcher the fixture uses — the first
        # version split on "_" only and let plurals through
        import oracle_fixtures as _OF
        banned = [c for c in df.columns
                  if _OF._calibration({c: 0})[0] is False]
        ok = (not missing) and (not banned) and len(df) > 0
        detail = (f"{len(t)} tape file(s), newest {t[-1].name} with {len(df)} rows, "
                  f"{len(df.columns)} columns; missing={missing}; outcome_columns={banned}")
    except Exception as e:
        ok, detail = False, f"{e.__class__.__name__}: {e}"
    res["tape_append_integrity"] = {"pass": bool(ok), "detail": detail[:400]}

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
    out.append("# re-arm:")
    for label in SLOTS:
        out.append(f"launchctl bootstrap gui/{UID} ~/Library/LaunchAgents/{label}.plist")
    return out


def run_topup(slot: str, log=print) -> int:
    """BR-1b. Fetch-and-store only: no render, no self-checks, no publish. A
    failure here logs to topup_log.jsonl and exits nonzero; the Oracle 15 minutes
    later is unaffected and stamps whatever as-of it finds."""
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
    "BANNER_MARKERS": {
        "value": ("LATE EDITION", "STALE DATA"), "ruled": True,
        "source": "OR-1 STEP F: 'Staleness banner => red band under the masthead "
                  "\"LATE EDITION — wire stale since <as-of>\"'; and BR-1 A2-7's "
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
     "path / bytes / sha256 and the banner state"),
    ("alarm", "wrapper",
     "one rc (top-up or Oracle), one ORACLE_DOWN.flag decision; the schedule-drift "
     "check is SKIPPED (clock suspended by operator ruling 2026-09-21)"),
    ("open-render", "skill",
     "open the render (macOS: open <path>)"),
    ("report-back", "skill",
     "print back to the operator: Front Page top rows + self-check verdict + "
     "banner state"),
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


# The Oracle's own per-asset log line (oracle_daily.build_view):
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
        return
    p = Path(hit.group("path"))
    size = f"{p.stat().st_size:,} B" if p.exists() else "MISSING ON DISK"
    log(f"  RENDER {p} · {size} · sha256 {hit.group('sha')}")
    try:
        log(f"  BANNER {banner_state(p)}")
    except Exception as e:
        log(f"  BANNER unknown — {e.__class__.__name__}: {e}")


def ondemand_flag_action(rc: int, no_fetch: bool) -> str:
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
            WIRE DOWN for itself."""
    if rc != 0:
        return "raise"
    if no_fetch:
        return "stand"
    return "clear"


def run_ondemand(argv: list[str], log=print) -> int:
    """--job ondemand. The chain in ONDEMAND_STEPS, steps 1-7, in that order."""
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

    if not acquire_lock(f"ondemand/{slot}", log=log):
        log("=== exit 0 (no-op: another Oracle run holds the lock — NO EDITION "
            "WAS PRINTED by this run) ===")
        return 0

    skips = ondemand_skips(slot, no_fetch)
    rc_t = rc_o = 0
    lines: list[str] = []

    def tee(msg="") -> None:
        lines.append(str(msg))
        log(msg)

    try:
        if "movers-fetch" in skips:
            log(f"{_step('movers-fetch')}: SKIPPED — {skips['movers-fetch']}")
        else:
            run_movers(log=log)

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

        log(f"{_step('oracle-render')}: slot={slot}")
        rc_o = run_oracle(slot, zr, started, log=tee)

        try:
            front_page(lines, slot, started, log=log)
        except Exception as e:
            # The summary is a courtesy printed AFTER the edition and its row are
            # on disk. It may fail to print; it may not fail the edition.
            log(f"  front page summary unavailable: {e.__class__.__name__}: {e}")
        rc = rc_t or rc_o
    except Exception:
        rc = 1
        log("  WRAPPER FAILED:\n" + note_failure())
    finally:
        release_lock(log=log)

    log(f"{_step('alarm')}: rc_topup={rc_t} rc_oracle={rc_o} -> exit {rc}")
    log(f"  schedule: SUSPENDED by operator ruling 2026-09-21 — the drift check is "
        f"SKIPPED for job=ondemand (on drift it would rewrite a retained plist and "
        f"bootstrap it); rollback card {SUSPENDED_CARD}")
    action = ondemand_flag_action(rc, no_fetch)
    if action == "raise":
        raise_flag("ondemand", slot, rc, log=log)
    elif action == "clear":
        if FLAG.exists():
            clear_flag(log=log)          # says CLEARED, or says why it could not
        else:
            log(f"  no {FLAG.name} standing — nothing to clear")
    elif FLAG.exists():
        log(f"  alarm left standing: {FLAG.name} — a --no-fetch run reads the cache "
            f"only and proves nothing about the wire, so it has no all-clear to give")
    else:
        log(f"  no {FLAG.name} standing (a --no-fetch run could not have cleared one)")

    log(f"=== exit {rc} ===")
    return rc


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    log = print
    if "--install" in argv:
        log(f"ORACLE — arming {len(SLOTS)} slots")
        zr = zone_report()
        log(f"  zone check: oracle {zr['oracle_now']} · machine {zr['machine_now']} · "
            f"agree={zr['zones_agree']}")
        armed = [arm(label, log=log) for label in SLOTS]
        log("")
        for line in undo_lines():
            log(line)
        print(json.dumps({"armed": armed, "zone": zr}, indent=1))
        return 0

    job, slot = _argv_job_slot(argv)
    if job == "ondemand":
        # OR-1 STEP A. Its own chain, its own flag rule, and NO schedule loop —
        # it returns here so nothing below (the legacy path, byte-for-byte as
        # it was) can run on its behalf. See THE ON-DEMAND EDITION.
        return run_ondemand(argv, log=log)

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
                             f"--install")
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
