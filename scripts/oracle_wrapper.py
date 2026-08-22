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

NO DELETION, EVER (CADENCE §4). Re-arming is bootout + bootstrap; the plist
stays on disk. This wrapper never removes a file.
"""
from __future__ import annotations

import json
import os
import plistlib
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
        log(f"  TOP-UP HALTED: {e}")
    except Exception:
        rc = 1
        log("  TOP-UP FAILED:\n" + traceback.format_exc())
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
        log("  RUN FAILED:\n" + traceback.format_exc())

    res = {}
    if rc == 0:
        try:
            res = self_checks(log=log)
            if not all(v["pass"] for v in res.values()):
                rc = 1
        except Exception:
            rc = 1
            log("  SELF-CHECKS FAILED:\n" + traceback.format_exc())

    p = append_selfcheck(slot, res or {"run": {"pass": rc == 0,
                                               "detail": "run failed"}},
                         {"zone_agree": zr["zones_agree"],
                          "html_sha": result.get("html_sha"),
                          "catchup": bool(catchup),
                          "seconds": round((datetime.now(timezone.utc) - started)
                                           .total_seconds(), 1)})
    log(f"  selfcheck log -> {p}")
    return rc


def run_catchup(zr: dict, started: datetime, log=print) -> int:
    """A2-8. Fires at every login/boot; runs something only when a slot was missed."""
    d = catchup_due()
    log(f"  catch-up: most recent Oracle boundary {d['boundary']} [{d['slot']}], "
        f"{d['age_min']:.0f} min ago")
    log(f"  evidence: {d['reason']}")
    if not d["due"]:
        log("  NOTHING MISSED — no catch-up run")
        return 0
    log(f"  MISSED SLOT [{d['slot']}] — running the top-up first, then the Oracle")
    rc_t = run_topup("topup", log=log)
    rc_o = run_oracle(d["slot"], zr, started, log=log, catchup=True)
    return rc_t or rc_o


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

    slot = "full"
    if "--slot" in argv:
        slot = argv[argv.index("--slot") + 1]
    job = "oracle"
    if "--job" in argv:
        job = argv[argv.index("--job") + 1]

    started = datetime.now(timezone.utc)
    log(f"=== ORACLE WRAPPER · job={job} slot={slot} · {started.isoformat()} ===")
    zr = zone_report()
    log(f"  zone: {zr}")
    if not acquire_lock(f"{job}/{slot}", log=log):
        log("=== exit 0 (no-op: another Oracle run holds the lock) ===")
        return 0
    try:
        if job == "topup":
            rc = run_topup(slot, log=log)
        elif job == "catchup":
            rc = run_catchup(zr, started, log=log)
        else:
            rc = run_oracle(slot, zr, started, log=log)
    finally:
        release_lock(log=log)

    # The self-reschedule runs LAST, so a bootout can never kill the run that
    # is producing today's Oracle.
    for label in SLOTS:
        try:
            d = reschedule_if_drifted(label, log=log)
            if d.get("missing"):
                rc = rc or 1
            elif not d["drift"]:
                log(f"  schedule OK on {label}: {d['want']}")
        except Exception as e:
            log(f"  reschedule check failed on {label}: {e}")

    log(f"=== exit {rc} ===")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
