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

NO DELETION, EVER (CADENCE §4). Re-arming is bootout + bootstrap; the plist
stays on disk. This wrapper never removes a file.
"""
from __future__ import annotations

import json
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

def plist_body(label: str, slot: str, hour: int, minute: int,
               job: str = "oracle") -> dict:
    return {
        "Label": label,
        "ProgramArguments": [PY, str(ROOT / "scripts" / "oracle_wrapper.py"),
                             "--job", job, "--slot", slot],
        "WorkingDirectory": str(ROOT),
        # PATH pinned exactly as the three existing agents pin it: the house
        # reason is that scripts shell out to bare `git`, and pinning makes the
        # tested environment identical to the scheduled one.
        "EnvironmentVariables": {"PATH": "/usr/bin:/bin:/usr/sbin:/sbin"},
        "StartCalendarInterval": {"Hour": int(hour), "Minute": int(minute)},
        "StandardOutPath": str(LOGDIR / f"{label.split('.')[-1]}.log"),
        "StandardErrorPath": str(LOGDIR / f"{label.split('.')[-1]}.log"),
        # false ON PURPOSE, the same reason the other three say so: RunAtLoad
        # true would fire a full run the instant the agent is bootstrapped and
        # again at every login, which is not what "07:00 daily" means.
        "RunAtLoad": False,
    }


def write_plist(label: str) -> tuple[Path, int, int]:
    cfg = SLOTS[label]
    h, m = machine_local_time_for(cfg["hour"], cfg["minute"])
    p = AGENTS / f"{label}.plist"
    p.parent.mkdir(parents=True, exist_ok=True)
    LOGDIR.mkdir(parents=True, exist_ok=True)
    p.write_bytes(plistlib.dumps(plist_body(label, cfg["slot"], h, m, cfg["job"])))
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
    log(f"  ARMED {label} [{cfg['job']}]: machine-local {h:02d}:{m:02d} "
        f"(= {cfg['hour']:02d}:{cfg['minute']:02d} {ZONE}) · plist {p}")
    log(f"    plutil: {lint.stdout.strip() or lint.stderr.strip()}")
    log(f"    launchd reports: {sched}")
    if r.returncode != 0:
        log(f"    bootstrap stderr: {r.stderr.strip()}")
    return {"label": label, "plist": str(p), "hour": h, "minute": m,
            "bootstrap_rc": r.returncode, "schedule_from_launchd": sched}


def reschedule_if_drifted(label: str, log=print) -> dict:
    """The self-reschedule. Compares the plist's hour against the zone's truth."""
    cfg = SLOTS[label]
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
    rc = 0
    result = {}

    if job == "topup":
        # BR-1b. Fetch-and-store only: no render, no self-checks, no publish.
        # A failure here logs to topup_log.jsonl and exits nonzero; the Oracle
        # 15 minutes later is unaffected and stamps whatever as-of it finds.
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
    else:
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
                              "seconds": round((datetime.now(timezone.utc) - started)
                                               .total_seconds(), 1)})
        log(f"  selfcheck log -> {p}")

    # The self-reschedule runs LAST, so a bootout can never kill the run that
    # is producing today's Oracle.
    for label in SLOTS:
        try:
            d = reschedule_if_drifted(label, log=log)
            if not d["drift"]:
                log(f"  schedule OK on {label}: {d['want']}")
        except Exception as e:
            log(f"  reschedule check failed on {label}: {e}")

    log(f"=== exit {rc} ===")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
