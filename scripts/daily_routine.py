#!/usr/bin/env python
"""daily_routine.py -- run the day's jobs, stage their outputs, write one report.

Composable by design: the job list lives in scripts/routine_jobs.json, so a new
job is added by editing that file, never by editing this code.

Contract:
  * repo root is resolved from this file's own location -- never hardcoded
  * a SWEEP step runs FIRST, relocating anything left in the legacy
    _reviewer_box drop points into exchange/ (gate A-3a transition support)
  * jobs run in registry order, via the interpreter named in the registry
  * a REQUIRED job that fails stops the run; an optional one is recorded and
    the run continues
  * each job's declared `stage` outputs are COPIED into output_dir with {date}
    filled in; each `reference` output is recorded as a POINTER instead
    (path + size + sha256) and its bytes are left where they are
  * a ROLLING WINDOW keeps the newest `keep_daily` DAILY_*.md and
    MANIFEST_*.json in output_dir and MOVES older ones to daily_archive_dir --
    moved, never deleted
  * the report is written to <output_dir>/DAILY_<yyyy-mm-dd>.md
  * git operations are the final PUBLISH step's, plus two READ-ONLY queries in
    the bus-health section -- see both AMENDMENTS below
  * exit code is non-zero if any required job failed, or if the publish guard
    tripped

AMENDMENT 2026-08-02 (gate A-6a, ruling Q-2 A).  This script's original
contract read "NO git operations of any kind, ever".  That line was written
when the routine's outputs landed in a git-ignored directory and there was
nothing to publish.  Ruling Q-2 A makes exchange/** auto-publishing coordination
state, so the routine now ends with a PUBLISH step: stage exchange/** only,
verify the whole index is inside that scope, then commit and push.  Sections 3
and 4 of the report still read repo state from the MANIFEST rather than from
git -- that part of the original contract is untouched, and deliberately so.
The publish step is the single, bounded exception, and it fails CLOSED: on any
doubt it resets the index and pushes nothing.

AMENDMENT 2026-08-15 (ruling 007).  Section 8, BUS HEALTH, reads live git: one
`rev-parse HEAD` and, only when the manifest disagrees with it, one `rev-list
--count`.  Both are READ-ONLY and neither stages, commits, moves or deletes
anything.  This is recorded as an amendment rather than done quietly because
the paragraph above asserts sections 3 and 4 read repo state from the MANIFEST
and not from git, and that assertion is still true and still deliberate --
section 8 exists precisely to state the DIFFERENCE between the two, which is
finding F-4, the manifest trailing live HEAD.  A section whose whole subject is
manifest-versus-git cannot answer the question from the manifest alone.  Ruling
007 retired DIGEST.md and made HERMES dormant; this section is where the
measurements that lane produced by hand are now taken.
"""

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = Path(__file__).resolve().parent / "routine_jobs.json"

sys.path.insert(0, str(Path(__file__).resolve().parent))
import publish_exchange                                  # noqa: E402
from backup_estate import drive_ready, phase_archive_root_path   # noqa: E402  (D-0b)

# Legacy drop points kept alive for the exchange transition (gate A-3a).  An
# in-flight APOLLO or ARGUS paste that still writes to _reviewer_box must not
# lose its output, so those folders stay working and this routine relocates
# whatever lands in them.  Order is (source, destination), both repo-relative.
SWEEP_MAP = (
    ("_reviewer_box/reports", "exchange/reports"),
    ("_reviewer_box/daily", "exchange/status/daily"),
)


# --------------------------------------------------------------- registry


def load_registry():
    with REGISTRY.open(encoding="utf-8") as fh:
        reg = json.load(fh)
    for key in ("python", "output_dir", "jobs"):
        if key not in reg:
            raise SystemExit(f"routine_jobs.json: missing required key {key!r}")
    return reg


def subst(text, today):
    return text.replace("{date}", today)


# --------------------------------------------------------------- sweep


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def sweep_legacy_box():
    """Relocate anything left in the legacy reviewer box into exchange/.

    Runs BEFORE the jobs, so a swept file is inventoried by the manifest and
    published by the same run rather than waiting a day.

    Collisions are never resolved by overwriting.  If the destination name is
    taken:
      * identical bytes  -> the source is a duplicate of something already
                            swept; the source is removed and the event logged
                            as 'deduped'.  Nothing is lost, because the bytes
                            are provably already there.
      * different bytes  -> the incoming file is kept under a suffixed name
                            (<stem>__swept-N<ext>) and logged as 'renamed'.
                            Two different files with one name is a real
                            collision and the operator must see both.

    EVERY filesystem call here is guarded, and a failure is recorded as an
    'error' row rather than raised.  That is not defensive habit -- the sweep
    runs FIRST, so an unguarded OSError would take down the manifest, the
    ~4-minute brief, the report and the publish, for the sake of one file in a
    transitional folder.  These drop points exist precisely so that in-flight
    pastes can be writing to them, which is the same thing as saying a source
    file may be locked at the moment the 07:00 task fires.  A stuck file must
    cost its own row in the report and nothing else.

    A subdirectory is not swept (the drop points are flat by convention) but is
    RECORDED as 'skipped-dir', because a silently ignored folder looks exactly
    like an empty one.

    Returns a list of {action, src, dst} dicts, oldest-first per folder.
    """
    moved = []
    for src_rel, dst_rel in SWEEP_MAP:
        src_dir, dst_dir = ROOT / src_rel, ROOT / dst_rel
        if not src_dir.is_dir():
            continue
        try:
            dst_dir.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            moved.append({"action": "error", "src": src_rel,
                          "dst": f"cannot create {dst_rel}: {exc}"})
            continue
        try:
            entries = sorted(src_dir.iterdir())
        except OSError as exc:
            moved.append({"action": "error", "src": src_rel,
                          "dst": f"cannot list: {exc}"})
            continue
        for item in entries:
            try:
                if item.is_dir():
                    moved.append({"action": "skipped-dir", "src": f"{src_rel}/{item.name}",
                                  "dst": "not swept — drop points are flat"})
                    continue
                if not item.is_file():
                    continue
                target = dst_dir / item.name
                if not target.exists():
                    shutil.move(str(item), str(target))
                    moved.append({"action": "moved", "src": f"{src_rel}/{item.name}",
                                  "dst": f"{dst_rel}/{item.name}"})
                    continue
                if _sha256(item) == _sha256(target):
                    item.unlink()
                    moved.append({"action": "deduped", "src": f"{src_rel}/{item.name}",
                                  "dst": f"{dst_rel}/{item.name}"})
                    continue
                n = 1
                while (dst_dir / f"{item.stem}__swept-{n}{item.suffix}").exists():
                    n += 1
                alt = dst_dir / f"{item.stem}__swept-{n}{item.suffix}"
                shutil.move(str(item), str(alt))
                moved.append({"action": "renamed", "src": f"{src_rel}/{item.name}",
                              "dst": f"{dst_rel}/{alt.name}"})
            except OSError as exc:
                # Includes the shutil.move copy-then-unlink fallback leaving the
                # source behind on Windows: the file may now exist in BOTH
                # places.  Say so, rather than crashing and leaving no report.
                moved.append({"action": "error", "src": f"{src_rel}/{item.name}",
                              "dst": f"{exc} — check for a copy left in both places"})
    return moved


def sweep_lines(swept):
    """Render the sweep result as report lines."""
    if not swept:
        return ["- nothing in the legacy drop points; nothing to sweep",
                "- `_reviewer_box/reports/` and `_reviewer_box/daily/` remain live "
                "for in-flight pastes"]
    lines = [f"- **{len(swept)} file(s) swept out of the legacy reviewer box.**", ""]
    lines.append("| action | from | to |")
    lines.append("|---|---|---|")
    for row in swept:
        lines.append(f"| {row['action']} | `{row['src']}` | `{row['dst']}` |")
    renamed = [r for r in swept if r["action"] == "renamed"]
    if renamed:
        lines.append("")
        lines.append(f"**{len(renamed)} name collision(s) kept under a suffixed name** — two "
                     "different files wanted one name. Both are present; neither was overwritten.")
    errors = [r for r in swept if r["action"] == "error"]
    if errors:
        lines.append("")
        lines.append(f"**{len(errors)} file(s) could not be swept.** The run continued; they stay "
                     "in the legacy folder and will be retried next run. A locked source can leave "
                     "a copy in both places — check before assuming the move completed.")
    return lines


# --------------------------------------------------------------- job runner


def run_job(job, python, today, out_dir, slot=None):
    """Run one job. Returns a result dict; never raises on job failure.

    Amendment 2 §2.3: when a slot is active, a job declaring `"slot_aware": true`
    receives `--slot <slot>`. Jobs that are not slot-aware run unchanged, which
    is what lets the three session tasks drive THIS routine rather than a second
    scheduler being built beside it.
    """
    jid = job.get("id", "<unnamed>")
    script = ROOT / job["script"]
    res = {
        "id": jid,
        "script": job["script"],
        "required": bool(job.get("required", False)),
        "exit": None,
        "elapsed": 0.0,
        "staged": [],
        "referenced": [],
        "missing": [],
        "error": None,
    }

    # RULING 4a (operator, 2026-08-15): the registry's retirement flags are
    # HONOURED. Until today they were DECORATIVE -- this function never read
    # them and the caller's loop is unconditional, so `daily_brief.py`, retired
    # 2026-08-05 by ruling D-3 and carrying "scheduled": false, ran on every
    # single execution. Measured on the 2026-08-15 launchd proof run: it took
    # 622.0s of the routine's 623.2s, making live network fetches for an output
    # nothing had read in ten days, while its two replacements finished in 0.2s.
    #
    # Checked BEFORE script.exists() on purpose: a retired job is not required
    # to still be on disk, and reporting "script not found" for a job we have
    # decided not to run would be a misleading error rather than a clean skip.
    # The script is NOT deleted -- daily_brief.py is still imported by
    # brief_capture.py for the Part I layers.
    if job.get("scheduled") is False or job.get("retired"):
        res["exit"] = 0
        why = job.get("retired")
        res["skipped"] = f"retired {why}" if why else "scheduled: false"
        return res

    if not script.exists():
        res["exit"] = 127
        res["error"] = f"script not found: {job['script']}"
        return res

    argv = [python, str(script)]
    if job.get("slot_aware"):
        if not slot:
            # A slot-aware job cannot run without one -- brief_capture.py makes
            # --slot required, so calling it slotless would fail on argparse and
            # report as a broken job rather than an inapplicable one. SKIPPED is
            # the honest state, and it keeps a no-slot routine run clean.
            res["exit"] = 0
            res["skipped"] = "slot-aware job, no --slot given"
            return res
        argv += ["--slot", slot]
        res["slot"] = slot

    t0 = time.monotonic()
    try:
        proc = subprocess.run(
            argv,
            cwd=str(ROOT),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        res["exit"] = proc.returncode
        if proc.returncode != 0:
            tail = (proc.stdout or b"").decode("utf-8", "replace").strip().splitlines()
            res["error"] = tail[-1] if tail else "no output"
    except OSError as exc:
        res["exit"] = 126
        res["error"] = f"could not launch: {exc}"
    res["elapsed"] = round(time.monotonic() - t0, 1)

    if res["exit"] != 0:
        return res

    for item in job.get("stage", []):
        src = ROOT / subst(item["from"], today)
        dst = out_dir / subst(item["to"], today)
        if src.exists():
            shutil.copy2(src, dst)
            res["staged"].append(dst.name)
        else:
            res["missing"].append(subst(item["from"], today))

    # REFERENCED, not copied.  A pointer -- path, size, sha256 -- instead of the
    # bytes.  The brief's html+json run ~400 KB a day; copying them into
    # exchange/ meant every day permanently refilled a capacity-constrained
    # project box with output that is regenerable and already on disk.  The
    # pointer is enough to find the file and prove it is the right one.
    for rel_tmpl in job.get("reference", []):
        rel = subst(rel_tmpl, today)
        src = ROOT / rel
        if src.exists():
            res["referenced"].append({
                "path": rel,
                "size": src.stat().st_size,
                "sha256": _sha256(src),
            })
        else:
            res["missing"].append(rel)
    return res


# --------------------------------------------------------- reminder engine

DATED_ARCHIVE = re.compile(r"_(\d{4}-\d{2}-\d{2})\.zip$")
PREF_BLOCKS = ("User preferences", "Project instructions", "Custom style")


def _archive_date(path):
    """The generation date from a dated archive name; mtime as a fallback."""
    m = DATED_ARCHIVE.search(path.name)
    if m:
        try:
            return date.fromisoformat(m.group(1))
        except ValueError:
            pass
    try:
        return date.fromtimestamp(path.stat().st_mtime)
    except OSError:
        return None


def _newest(dest, pattern):
    """(path, date) of the newest dated archive matching pattern, or (None, None)."""
    best = (None, None)
    try:
        for p in dest.glob(pattern):
            if not p.is_file():
                continue
            d = _archive_date(p)
            if d and (best[1] is None or d > best[1]):
                best = (p, d)
    except OSError:
        return (None, None)
    return best


def _unfilled_pref_blocks():
    """Which of the three PART 1 blocks are still empty. None if the file is absent.

    A block is a fenced ```text region under a `### <label>` heading.  Empty
    means whitespace-only between the fences -- which the file itself defines as
    "not yet captured", never "not set".
    """
    path = ROOT / "docs" / "primers" / "OPERATOR_PREFERENCES.md"
    if not path.is_file():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    unfilled = []
    for label in PREF_BLOCKS:
        head = text.find(f"### {label}")
        if head == -1:
            unfilled.append(f"{label} (heading missing)")
            continue
        open_fence = text.find("```", head)
        if open_fence == -1:
            unfilled.append(f"{label} (no block)")
            continue
        body_start = text.find("\n", open_fence)
        close_fence = text.find("```", body_start)
        body = text[body_start:close_fence] if close_fence != -1 else ""
        if not body.strip():
            unfilled.append(label)
    return unfilled


def _unratified_queue_items():
    """Queue item numbers with no ratification stamp.  See reviewer_manifest."""
    qdir = ROOT / "exchange" / "queue"
    if not qdir.is_dir():
        return []
    open_items = []
    for p in sorted(qdir.glob("*.md")):
        name = p.name
        if not (len(name) > 4 and name[:3].isdigit() and name[3] == "_"):
            continue
        try:
            raw = p.read_bytes()
        except OSError:
            continue
        ratified = False
        for line in raw.split(b"\n"):
            line = line.strip()
            if line.upper().startswith(b"RATIFIED:"):
                rest = line[len(b"RATIFIED:"):].strip()
                if rest and rest.upper() != b"PENDING":
                    ratified = True
        if not ratified:
            open_items.append(name[:3])
    return open_items


def _onedrive_running():
    if os.name != "nt":
        return None
    try:
        proc = subprocess.run(["tasklist", "/FI", "IMAGENAME eq OneDrive.exe", "/NH"],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except OSError:
        return None
    if proc.returncode != 0:
        return None
    return b"onedrive.exe" in proc.stdout.lower()


def _retention_violations(dest, cfg):
    """Generations outside 'newest N estate + K workflow'. LIST only.

    CORRECTED 2026-08-03, in step with scripts/backup_estate.py.  This helper
    ALSO carried the phase-set rule, so the alarm was independently reporting
    unique study evidence as "outside the rule" every single run -- the same
    defect in a second place, which is exactly how a wrong rule becomes received
    wisdom.

    PHASE ARCHIVES ARE NEVER A VIOLATION.  Each holds a different phase's
    evidence; an older one is the only copy, not a superseded generation.  There
    is no keep-count for them here and no `keep_phase_sets` key is read.
    """
    out = []
    for pattern, keep, label in (
        ("naiad_estate_*.zip", cfg.get("keep_estate", 4), "estate"),
        ("naiad_workflow_*.zip", cfg.get("keep_workflow", 4), "workflow"),
    ):
        try:
            gens = sorted((p for p in dest.glob(pattern) if p.is_file()),
                          key=lambda p: p.name, reverse=True)
        except OSError:
            continue
        for p in gens[keep:]:
            out.append(f"{label}: {p.name}")
    return out


SECOND_ACCOUNT_PATH = ROOT / "exchange" / "status" / "SECOND_ACCOUNT.md"
_SECOND_ACCOUNT_DATE = re.compile(r"^last_manual_upload:\s*(\d{4}-\d{2}-\d{2})\s*$",
                                  re.M)


def _second_account_due(dest, facts):
    """Is a manual upload to the second Google Drive account outstanding?

    That account is NOT machine-verifiable -- there is no API, no mounted drive,
    nothing this script can read.  The only honest mechanism is a date the
    operator writes down after each manual upload, compared against the newest
    archive we CAN see.  If an archive is newer than that date, an upload is
    outstanding.

    Returns an alert string, or None.
    """
    newest_name, newest_d = None, None
    for key in ("estate", "workflow"):
        iso = facts.get(key)
        if not iso:
            continue
        d = date.fromisoformat(iso)
        if newest_d is None or d > newest_d:
            newest_d, newest_name = d, key
    if newest_d is None:
        return None

    if not SECOND_ACCOUNT_PATH.is_file():
        return (f"**second-account upload state unknown** — "
                f"`exchange/status/SECOND_ACCOUNT.md` is missing, so there is no "
                f"record of when the second Google Drive account was last "
                f"updated by hand. Newest archive is the {newest_name} of "
                f"{newest_d.isoformat()}.")
    m = _SECOND_ACCOUNT_DATE.search(
        SECOND_ACCOUNT_PATH.read_text(encoding="utf-8", errors="replace"))
    if not m:
        return ("**second-account date line unreadable** — "
                "`exchange/status/SECOND_ACCOUNT.md` has no "
                "`last_manual_upload: YYYY-MM-DD` line.")
    last = date.fromisoformat(m.group(1))
    if newest_d > last:
        return (f"**manual upload to the second Google Drive account is "
                f"outstanding** — the newest {newest_name} archive is "
                f"{newest_d.isoformat()}, but the last recorded manual upload "
                f"was {last.isoformat()}. That account cannot be checked by "
                f"machine; upload in the browser, then update the date line in "
                f"`exchange/status/SECOND_ACCOUNT.md`.")
    return None


def check_reminders(reg, today):
    """Every check computed from real state.  Returns (alerts, facts).

    Nothing here is assumed.  If the backup destination cannot be read, that is
    reported as its own ALERT rather than silently becoming "0 days since
    backup" -- an unreachable drive must never read as a healthy one.
    """
    cfg = reg.get("reminders", {})
    alerts, facts = [], {}
    today_d = date.fromisoformat(today)

    dest_raw = reg.get("backup_dest")
    dest = Path(dest_raw) if dest_raw else None
    # D-0b.  This is the gate that runs unattended most often -- the 07:00 daily
    # job, after the machine has been idle all night.  A bare is_dir() on a
    # spun-down external disk returned False in milliseconds and raised
    # "backup destination unreachable" on a drive that was merely asleep.
    dest_detail = "(not configured)"
    if dest is not None:
        ready, dest_detail = drive_ready(dest)
        dest_ok = bool(ready and dest.is_dir())
    else:
        dest_ok = False
    facts["dest"] = str(dest) if dest else "(not configured)"
    facts["dest_probe"] = dest_detail

    if not dest_ok:
        alerts.append(f"**backup destination unreachable** — `{facts['dest']}` is not readable "
                      f"({dest_detail}). "
                      "Estate, workflow, operator-export and retention checks could NOT run; "
                      "their state is UNKNOWN, not healthy.")
        facts.update({"estate": None, "workflow": None, "phase": None})
    else:
        for pattern, key, limit, label in (
            ("naiad_estate_*.zip", "estate", cfg.get("estate_max_days", 8), "estate"),
            ("naiad_workflow_*.zip", "workflow", cfg.get("workflow_max_days", 8), "workflow"),
        ):
            p, d = _newest(dest, pattern)
            facts[key] = d.isoformat() if d else None
            if d is None:
                alerts.append(f"**no {label} archive found** in `{dest}` — the {label} backup has "
                              "never run, or its output is missing.")
            else:
                age = (today_d - d).days
                if age > limit:
                    alerts.append(f"**{label} backup is {age} days old** "
                                  f"(`{p.name}`, limit {limit}).")

        exports = dest / "operator-exports"
        limit = cfg.get("operator_export_max_days", 35)
        if not exports.is_dir():
            alerts.append(f"**operator-exports folder missing** at `{exports}`.")
        else:
            files = [f for f in exports.rglob("*") if f.is_file()]
            if not files:
                alerts.append(f"**no operator data export yet** — `{exports}` is empty. "
                              "Project memory, preferences, instructions and custom style are "
                              "not in any export, so this folder is the only route for the rest.")
            else:
                newest = max(files, key=lambda f: f.stat().st_mtime)
                age = (today_d - date.fromtimestamp(newest.stat().st_mtime)).days
                if age > limit:
                    alerts.append(f"**operator export is {age} days old** "
                                  f"(`{newest.name}`, limit {limit}).")

        violations = _retention_violations(dest, cfg)
        if violations:
            alerts.append("**retention — generations outside the rule** (listed, never pruned): "
                          + "; ".join(violations))

    # phase set date, for the heartbeat.
    #
    # STALE PATH, fixed 2026-08-12 (D-0b).  This read REPO/research_outputs/
    # _archive, which stopped holding archives on 2026-08-06 when ruling B moved
    # them off-machine -- only the sidecars stayed in the repo.  So the heartbeat
    # has been reporting `phase: NONE` while nine archives sat on the drive.
    # This is the same defect O-4 fixed inside backup_estate.py, surviving in a
    # second file; it now resolves the SAME root --phase writes to, through the
    # same waiting gate.
    arch = phase_archive_root_path()
    arch_ready, _arch_detail = drive_ready(arch, note=lambda *_a, **_k: None)
    _, phase_d = _newest(arch, "*.zip") if (arch_ready and arch.is_dir()) else (None, None)
    facts["phase"] = phase_d.isoformat() if phase_d else None

    unfilled = _unfilled_pref_blocks()
    if unfilled is None:
        alerts.append("**docs/primers/OPERATOR_PREFERENCES.md is missing.**")
    elif unfilled:
        alerts.append(f"**operator preferences not captured** — {len(unfilled)} of 3 PART 1 blocks "
                      f"still empty: {', '.join(unfilled)}. These exist only in Claude's cloud "
                      "settings, are excluded from data exports, and can only be pasted by hand.")

    od = _onedrive_running()
    facts["onedrive"] = od
    if od is False:
        alerts.append("**OneDrive.exe is not running.** Since 2026-08-12 (queue 004 Phase A) the "
                      "repo lives at `C:/Naiad`, OUTSIDE the OneDrive tree, so this no longer "
                      "affects the repo — it is reported only because other folders on this "
                      "machine may still rely on it.")

    second = _second_account_due(dest if dest_ok else None, facts)
    if second:
        alerts.append(second)

    unratified = _unratified_queue_items()
    if unratified:
        alerts.append(f"**{len(unratified)} queue item(s) awaiting your ratification stamp**: "
                      + ", ".join(unratified) + ". They are requests, not work, until stamped.")

    # (h) published status older than the newest estate snapshot.  Top-level
    # files of exchange/status/ only: daily/ is an append-only archive whose
    # older entries are expected to be old, and flagging them every run would
    # bury the signal this check exists to raise.
    if facts.get("estate"):
        cutoff = date.fromisoformat(facts["estate"])
        status_dir = ROOT / "exchange" / "status"
        stale = []
        if status_dir.is_dir():
            for p in sorted(status_dir.glob("*")):
                if not p.is_file():
                    continue
                try:
                    if date.fromtimestamp(p.stat().st_mtime) < cutoff:
                        stale.append(p.name)
                except OSError:
                    continue
        if stale:
            alerts.append(f"**{len(stale)} published status file(s) predate the newest estate "
                          f"snapshot ({facts['estate']})** — lane state may be stale: "
                          + ", ".join(stale[:12])
                          + (f" … +{len(stale) - 12} more" if len(stale) > 12 else ""))

    return alerts, facts


def action_required_lines(alerts):
    if not alerts:
        return ["nothing overdue — all cadences current"]
    lines = [f"**{len(alerts)} item(s) need attention.**", ""]
    lines += [f"{i}. {a}" for i, a in enumerate(alerts, 1)]
    return lines


def _heartbeat_last_run(hb_path):
    """The date of the last completed routine run, from HEARTBEAT.md.

    Returns (date, reason).  `date` is None when it cannot be established, and
    `reason` then says why -- which is NOT the same as "no runs were missed".
    """
    try:
        text = hb_path.read_text(encoding="utf-8")
    except OSError:
        return None, f"`{_rel(hb_path)}` is absent — no run has ever recorded a heartbeat here"
    for line in text.splitlines():
        if line.startswith("run:"):
            stamp = line.split(":", 1)[1].strip()
            try:
                return date.fromisoformat(stamp[:10]), None
            except ValueError:
                return None, f"the heartbeat's run line is unreadable: `{line.strip()}`"
    return None, "the heartbeat has no `run:` line"


def missed_runs(out_dir, archive_dir, hb_path, today):
    """D-0e.  Which daily runs never happened, BY NAME.  Report-only.

    The cadence is daily, so every date strictly between the last recorded run
    and today should have produced a DAILY_<date>.md.  A date counts as run if
    its report is either still in the window or has aged into the archive --
    checking only `out_dir` would report the rolling window's own housekeeping
    as missed runs.

    Returns (missing_dates, reason).  This NEVER backfills and never launches a
    catch-up: a missed run is a fact to report, and re-running yesterday's jobs
    today would produce a report dated yesterday from today's data.
    """
    last, reason = _heartbeat_last_run(hb_path)
    if last is None:
        return [], reason

    today_d = date.fromisoformat(today)
    have = set()
    for d in (out_dir, archive_dir):
        try:
            have |= {p.name for p in d.glob("DAILY_*.md")}
        except OSError:
            pass

    missing, cursor = [], last + timedelta(days=1)
    while cursor < today_d:
        if f"DAILY_{cursor.isoformat()}.md" not in have:
            missing.append(cursor.isoformat())
        cursor += timedelta(days=1)
    return missing, None


def missed_run_lines(missing, reason, today):
    """The banner. Empty list when there is nothing to say -- no gap, no noise."""
    if reason:
        return ["## MISSED RUNS — UNKNOWN", "",
                f"**Cannot tell whether any run was missed:** {reason}.",
                "",
                "An unanswerable question is not a clean bill of health. This says "
                "UNKNOWN rather than nothing, for the same reason the retention "
                "report says NOT ENUMERABLE rather than \"none found\".", ""]
    if not missing:
        return []
    n = len(missing)
    out = [f"## MISSED RUNS — {n} DAY(S) WITH NO REPORT", "",
           f"The routine is daily. These {n} date(s) between the last recorded run "
           f"and today ({today}) produced no `DAILY_<date>.md`:", ""]
    out += [f"- **{d}** — no `DAILY_{d}.md`" for d in missing]
    out += ["",
            "Report-only: nothing was backfilled and no catch-up was run. A missed "
            "day's data cannot be reconstructed by running today's jobs.", ""]
    return out


def write_heartbeat(facts, alerts, exit_code, out_path):
    """Six lines max. Its absence or a stale timestamp IS the alert."""
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines = [
        "# HEARTBEAT",
        f"run: {stamp}",
        f"exit: {exit_code} (jobs + window; publish outcome in the day's DAILY report)",
        f"overdue: {len(alerts)}",
        f"archives — estate: {facts.get('estate') or 'NONE'} · "
        f"workflow: {facts.get('workflow') or 'NONE'} · phase: {facts.get('phase') or 'NONE'}",
    ]
    try:
        out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    except OSError as exc:
        print(f"  heartbeat could not be written: {exc}")


# ------------------------------------------------------- rolling window


def _rel(path):
    """Repo-relative POSIX path, or the absolute path if it is outside the repo.

    `daily_archive_dir` is operator-configurable, so it can legitimately point
    anywhere -- another drive, a network share.  A bare relative_to() raises
    ValueError in that case, and it would raise at the very END of the run,
    after the jobs, the brief and the report had all succeeded.  Fall back
    instead of throwing away the day's work over a display string.
    """
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def apply_rolling_window(out_dir, archive_dir, keep):
    """Keep the newest `keep` DAILY_*.md and MANIFEST_*.json; MOVE the rest out.

    MOVED, never deleted.  The point is to stop exchange/ growing without bound
    -- it is tracked, auto-pushed and synced into a capacity-constrained project
    box -- not to lose the history.  Older reports land in archive_dir, still on
    disk, still readable.

    Names carry an ISO date (DAILY_2026-08-02.md), so a lexical sort is a
    chronological sort; no filesystem timestamps are trusted.

    Every move is guarded: a failure is recorded and the run continues, because
    this happens after the day's real work and must never cost it.
    """
    moved = []
    if keep is None or keep < 0:
        return moved
    try:
        archive_dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        return [{"action": "error", "name": str(archive_dir), "detail": str(exc)}]

    for pattern in ("DAILY_*.md", "MANIFEST_*.json"):
        try:
            files = sorted(out_dir.glob(pattern), key=lambda p: p.name, reverse=True)
        except OSError as exc:
            moved.append({"action": "error", "name": pattern, "detail": str(exc)})
            continue
        for old in files[keep:]:
            target = archive_dir / old.name
            try:
                if target.exists():
                    if _sha256(old) == _sha256(target):
                        old.unlink()
                        moved.append({"action": "deduped", "name": old.name,
                                      "detail": "identical copy already archived"})
                        continue
                    n = 1
                    while (archive_dir / f"{old.stem}__{n}{old.suffix}").exists():
                        n += 1
                    target = archive_dir / f"{old.stem}__{n}{old.suffix}"
                shutil.move(str(old), str(target))
                moved.append({"action": "moved", "name": old.name,
                              "detail": _rel(target)})
            except OSError as exc:
                moved.append({"action": "error", "name": old.name, "detail": str(exc)})
    return moved


def window_lines(moved, out_dir, keep, archive_dir):
    kept = {p.name for p in out_dir.glob("DAILY_*.md")} | \
           {p.name for p in out_dir.glob("MANIFEST_*.json")}
    lines = [f"- window: newest **{keep}** of each of `DAILY_*.md` and `MANIFEST_*.json` stay in "
             f"`{_rel(out_dir)}`",
             f"- anything older is **moved** (never deleted) to `{_rel(archive_dir)}`",
             f"- {len(kept)} file(s) currently inside the window"]
    if not moved:
        lines.append("- nothing aged out this run")
        return lines
    lines += ["", "| action | file | destination |", "|---|---|---|"]
    for row in moved:
        lines.append(f"| {row['action']} | `{row['name']}` | `{row['detail']}` |")
    errs = [r for r in moved if r["action"] == "error"]
    if errs:
        lines.append("")
        lines.append(f"**{len(errs)} file(s) could not be moved.** They stay in the window folder "
                     "and will be retried next run.")
    return lines


# --------------------------------------------------------------- bus health
# RULING 007, 2026-08-15.  DIGEST.md is retired and HERMES is dormant, so the
# measurements that lane produced by hand each cycle are taken here, by the run
# that already happens every day.  publish_exchange carries the two cheap
# components and the renderer; the two expensive ones live here -- see the
# note above publish_exchange.folder_rows for the measured cost split.

LEDGER_LANES = ("APOLLO", "ARGUS", "ATHENA", "DIONYSUS", "HEPHAESTUS", "HERMES")

# A parked lane's ledger age is not a finding, and saying so is the difference
# between a report and a nag.  Without this, the block that ABSORBED HERMES's
# staleness duty would report HERMES as the stalest lane in the project, by a
# margin growing one day per day forever -- while CONVENTIONS §5 tells the
# reader "nothing waits on HERMES".  The successor surface would contradict
# the dormancy ruling it was created by.  The row stays (dropping it would
# hide the ledger entirely); only the interpretation changes.
DORMANT_LANES = {"HERMES": "DORMANT (ruling 007) — not expected to move"}

# Entry headers, and why each piece is here.  THREE header shapes are live in
# the ledgers today and a reader that knows only one publishes a false
# staleness reading -- which is finding F-5, committed for real on 2026-08-12
# and reported as another lane's neglect:
#   `=== STATUS_ARGUS — 2026-08-11 ===`   the naiad-eod template
#   `=== STATUS ATHENA — 2026-08-15 ===`  a SPACE, not an underscore; five of
#                                         ATHENA's most recent entries use it
#   `## 2026-08-11 — ARGUS acknowledges…` ARGUS's newest entry is this shape,
#                                         and ONLY this shape
# Both patterns anchor on a real ISO date, which is what keeps the fenced
# template line `=== STATUS_<LANE> — <date> ===` -- present in all six files --
# from matching, and what keeps the trailing sequence letter in APOLLO's
# `2026-08-15b` from being read as part of the date.
#
# Anchoring on the HEADER rather than on any date is the other half.  Grepping
# for any date returns 2026-08-28 for APOLLO and 2026-09-05 for ARGUS -- both
# forward-looking rotation due-dates sitting in prose.  Too loose fails exactly
# as badly as too strict, and in the more embarrassing direction.
_ISO = r"(\d{4}-\d{2}-\d{2})"
_DASH = r"(?:—|--)"
ENTRY_HEADER_RES = (
    re.compile(r"^===\s*STATUS[_ ][A-Za-z]+.*?" + _DASH + r"\s*" + _ISO),
    re.compile(r"^##\s+" + _ISO + r"\s*" + _DASH),
)


def _valid_past_dates(found, today):
    """Keep only real calendar dates at or before `today`; report the rest.

    max() over raw matches is not safe, and the failure is finding F-5 in the
    direction the obvious fixture does not test.  A single typo'd header --
    `2027-08-15` for `2026-08-15` -- or a planning heading like
    `## 2026-09-05 — INTERFACE rotation` pins that lane at "fresh" forever and
    HIDES a genuinely stale ledger underneath it.  `\\d{4}-\\d{2}-\\d{2}` also
    accepts 2026-13-45, which then renders an age of "--" that looks exactly
    like the NOT ENUMERABLE row meaning something else entirely.

    So: parse, drop the impossible and the future, and SAY how many were
    dropped -- a discarded header must become visible, not become the answer.
    """
    good, bad, future = [], 0, 0
    for s in found:
        try:
            d = datetime.strptime(s, "%Y-%m-%d").date()
        except ValueError:
            bad += 1
            continue
        if d > today:
            future += 1
            continue
        good.append(s)
    notes = []
    if future:
        notes.append(f"{future} future-dated header(s) ignored")
    if bad:
        notes.append(f"{bad} unparseable date(s) ignored")
    return good, notes


def ledger_recency(status_dir=None, today=None):
    """[(lane, newest entry-header date or None, note)] for the six lanes.

    RECENCY IS PER FILE, not per lane token, and that is a deliberate choice
    worth stating: LEDGER_ATHENA.md holds one STATUS_HEPHAESTUS entry filed by
    the lane that commissioned it, so "the newest entry in ATHENA's ledger" and
    "ATHENA's newest entry" can differ.  The question this table answers is
    whether a ledger is being kept current, so the file is the right unit --
    but a reader comparing it against a lane-scoped count deserves to know why
    the two can disagree, and that is what this docstring is for.
    """
    status_dir = Path(status_dir) if status_dir else ROOT / "exchange" / "status"
    today = today or date.today()
    rows = []
    for lane in LEDGER_LANES:
        path = status_dir / f"LEDGER_{lane}.md"
        if not path.is_file():
            rows.append((lane, None, "no ledger file at %s" % _rel(path)))
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            rows.append((lane, None, "unreadable: %s" % exc))
            continue
        found = []
        for line in text.splitlines():
            for rx in ENTRY_HEADER_RES:
                m = rx.match(line)
                if m:
                    found.append(m.group(1))
                    break
        good, notes = _valid_past_dates(found, today)
        if not good:
            why = "no entry header matched" if not found else \
                  "no usable date; " + " · ".join(notes)
            rows.append((lane, None, why))
        else:
            note = "%d entry header(s)" % len(good)
            if notes:
                note += " · " + " · ".join(notes)
            if lane in DORMANT_LANES:
                note += " · %s" % DORMANT_LANES[lane]
            rows.append((lane, max(good), note))
    return rows


def ledger_recency_lines(rows, today):
    """The recency table, as markdown."""
    out = ["| lane | newest entry | age (days) | entries |", "|---|---|---:|---:|"]
    for lane, when, note in rows:
        if when is None:
            out.append(f"| **{lane}** | NOT ENUMERABLE | -- | {note} |")
            continue
        try:
            age = (datetime.strptime(today, "%Y-%m-%d").date()
                   - datetime.strptime(when, "%Y-%m-%d").date()).days
            age_s = str(age)
        except ValueError:
            age_s = "--"
        out.append(f"| **{lane}** | {when} | {age_s} | {note} |")
    return out


def rotation_candidate_lines(today):
    """The queue-003 rotation-candidate count, or a stated reason there is none.

    Wrapped in its own try/except and never allowed to propagate: this is a
    reporting line inside an unattended 07:00 run, and no report line is worth
    failing a launchd task over.  InboxSourceUnavailable is expected, not
    exceptional, while the unacted-inbox surface has no home (ruling 007).
    """
    try:
        import rotate_reports
    except ImportError as exc:
        return ["- rotation candidates: NOT ENUMERABLE -- "
                f"`scripts/rotate_reports.py` did not import ({exc})."]
    caveat = []
    try:
        when = datetime.strptime(today, "%Y-%m-%d").date()
        parts = rotate_reports.classify(when)
    except rotate_reports.InboxSourceUnavailable as exc:
        # Report the count anyway, as an UPPER BOUND with the exemption switched
        # off and said out loud.  Ruling 007 asked for this number; refusing to
        # print it because one input is missing would hide the very cadence
        # figure queue 003 D-2 exists to publish.  The SWEEP still halts -- only
        # this reporting line proceeds, and it cannot move anything.
        caveat = ["- **exemption NOT APPLIED.** " + str(exc),
                  "  The count above is therefore an UPPER BOUND: it includes "
                  "any unacted inbox note that would otherwise be exempt."]
        try:
            parts = rotate_reports.classify(when, inbox=set())
        except Exception as exc2:                       # noqa: BLE001
            return [f"- rotation candidates: NOT ENUMERABLE -- "
                    f"{type(exc2).__name__}: {exc2}"]
    except Exception as exc:                            # noqa: BLE001
        return [f"- rotation candidates: NOT ENUMERABLE -- {type(exc).__name__}: {exc}"]
    candidates, exempt, young, undated, cutoff, _inbox = parts
    cand_bytes = sum(s for _, s, _, _ in candidates)
    box = publish_exchange.BOX_BYTES
    return [
        f"- rotation candidates (queue 003, {rotate_reports.AGE_DAYS}-day window, "
        f"cutoff {cutoff.isoformat()}): **{len(candidates)}** file(s), "
        f"{cand_bytes:,} B, {100.0 * cand_bytes / box:.2f}% of the box",
        f"- exempt {len(exempt)} · inside the window {len(young)} · undated "
        f"{len(undated)} (undated files are never selected — an unknown age is "
        "not an old age)",
    ] + caveat


def _walk_scope(scope_dir):
    """[(bytes, repo-relative posix path)] for every file under scope_dir."""
    out = []
    for p in scope_dir.rglob("*"):
        if p.is_file() and not p.is_symlink():
            try:
                out.append((p.stat().st_size, _rel(p)))
            except OSError:
                continue
    return out


def bus_health_lines(today):
    """Section 8 -- the bus-health block, all four components, as markdown.

    The folder breakdown is measured from the WORKTREE here, not from the git
    index as in publish().  Deliberate, and the block says which: bus health is
    about what the bus is CARRYING, so a file dropped in and not yet committed
    has loaded the bus whether or not git has noticed it.  The two figures
    agree whenever exchange/ is clean and diverge exactly when it is not, which
    is the moment the difference is worth seeing.
    """
    scope = ROOT / "exchange"
    sized = _walk_scope(scope)
    total_bytes = sum(s for s, _ in sized)
    rows = publish_exchange.folder_rows(sized)
    recorded, live, delta = publish_exchange.measure_head_pair(ROOT)

    out = [f"Bus carrying **{total_bytes:,} B** in **{len(sized)}** file(s) "
           "(worktree, including anything not yet committed).", ""]
    out.append("| folder | bytes | files | % of box |")
    out.append("|---|---:|---:|---:|")
    box = publish_exchange.BOX_BYTES
    for folder, b, n in rows:
        out.append(f"| `{folder}` | {b:,} | {n} | {100.0 * b / box:.2f}% |")
    out.append(f"| **total** | **{total_bytes:,}** | **{len(sized)}** | "
               f"**{100.0 * total_bytes / box:.2f}%** |")
    out.append("")
    out.append("**Manifest freshness (F-4).** Stated side by side on every run, "
               "including the runs where they agree — a line that appears only "
               "on disagreement teaches nothing on the days it is silent, and "
               "F-4 has been re-found in five separate cycles for want of it.")
    out.append("")
    out.append("| | sha |")
    out.append("|---|---|")
    out.append(f"| manifest records | `{recorded[:7] if recorded else 'unknown'}` |")
    out.append(f"| live HEAD | `{live[:7] if live else 'unknown'}` |")
    # ONE verdict function, shared with the publish line.  This was a second
    # hand-rolled copy of the same three-way branch, and it was the copy that
    # lands in the published report while the fixture pinned only the other --
    # so the ruling's headline clause ("the two heads print even when equal")
    # was asserted against the renderer lanes do not read.
    verdict, detail = publish_exchange.head_verdict(recorded, live, delta)
    out.append(f"| verdict | **{verdict}**{' — ' + detail if detail else ''} |")
    out.append("")
    out.append("**Ledger recency.** Newest entry header per ledger file.")
    out.append("")
    out += ledger_recency_lines(
        ledger_recency(today=datetime.strptime(today, "%Y-%m-%d").date()), today)
    out.append("")
    out.append("**Rotation.**")
    out += rotation_candidate_lines(today)
    return out


def reference_lines(results):
    """Section 6 -- artifacts recorded as pointers rather than copied in."""
    refs = [r for res in results for r in res.get("referenced", [])]
    if not refs:
        return ["- no referenced artifacts this run"]
    lines = [
        "These files are **referenced, not copied.** They are regenerable output that would "
        "otherwise add ~400 KB per day to a tracked, auto-pushed, box-synced directory. The path "
        "and hash below are enough to locate each one and prove it is the right file.",
        "",
        "| path | size (B) | sha256 |",
        "|---|---:|---|",
    ]
    for r in refs:
        lines.append(f"| `{r['path']}` | {r['size']:,} | `{r['sha256']}` |")
    lines.append("")
    lines.append("_Their directory is git-ignored by design (charter A1.5), so they live on this "
                 "machine and in the weekly estate backup, not in the repository._")
    return lines


# --------------------------------------------------------------- report parts


def repo_state(manifest):
    """Section 3 -- repo state, read from the manifest, never from git."""
    if not manifest:
        return ["Repo state unavailable -- no manifest was staged this run."]

    ab = manifest.get("ahead_behind") or {}
    porcelain = manifest.get("status_porcelain") or []
    tracked_dirty = [p for p in porcelain if not p.lstrip().startswith("??")]
    drifted = [s["path"] for s in manifest.get("sources", []) if not s.get("match_head", True)]
    untracked = manifest.get("untracked_root") or []

    lines = [
        f"- HEAD: `{manifest.get('head', '?')}`",
        f"- branch: `{manifest.get('branch', '?')}`",
        f"- ahead / behind: {ab.get('ahead', '?')} / {ab.get('behind', '?')}",
        f"- worktree clean (tracked files): {'yes' if not tracked_dirty else 'NO'}"
        + (f" -- {len(tracked_dirty)} tracked entr{'y' if len(tracked_dirty) == 1 else 'ies'} dirty" if tracked_dirty else ""),
    ]
    if drifted:
        lines.append(f"- sources with `match_head: false` ({len(drifted)}):")
        lines += [f"    - `{p}`" for p in drifted]
    else:
        lines.append("- sources with `match_head: false`: none")

    if untracked:
        lines.append(f"- untracked files at repo root ({len(untracked)}):")
        lines += [f"    - `{u.get('name', u) if isinstance(u, dict) else u}`" for u in untracked]
    else:
        lines.append("- untracked files at repo root: none")
    return lines


def _untracked_names(manifest):
    out = set()
    for u in manifest.get("untracked_root") or []:
        out.add(u.get("name") if isinstance(u, dict) else str(u))
    return out


def _source_shas(manifest):
    return {
        s["path"]: s.get("sha256_worktree")
        for s in manifest.get("sources", []) + manifest.get("reviewer_box", [])
        if "path" in s
    }


def change_since_last(manifest, out_dir, today):
    """Section 4 -- diff today's manifest against the most recent earlier one."""
    if not manifest:
        return ["Not computed -- no manifest this run."]

    prior = sorted(
        p for p in out_dir.glob("MANIFEST_*.json")
        if p.stem.replace("MANIFEST_", "") < today
    )
    if not prior:
        return ["No earlier manifest in the archive -- this is the first recorded run."]

    prev_path = prior[-1]
    prev_date = prev_path.stem.replace("MANIFEST_", "")
    try:
        with prev_path.open(encoding="utf-8") as fh:
            prev = json.load(fh)
    except (OSError, ValueError) as exc:
        return [f"Could not read {prev_path.name}: {exc}"]

    lines, changed = [], False

    old_head, new_head = prev.get("head"), manifest.get("head")
    if old_head != new_head:
        changed = True
        lines.append(f"- HEAD moved: `{old_head}` -> `{new_head}`")
        lines.append(
            "    - commits added: not enumerable -- this routine performs no git "
            "operations by contract, and the manifest records only the HEAD sha."
        )
    else:
        lines.append(f"- HEAD unchanged: `{new_head}`")

    old_shas, new_shas = _source_shas(prev), _source_shas(manifest)
    moved = sorted(p for p in old_shas.keys() & new_shas.keys() if old_shas[p] != new_shas[p])
    added = sorted(new_shas.keys() - old_shas.keys())
    dropped = sorted(old_shas.keys() - new_shas.keys())
    if moved:
        changed = True
        lines.append(f"- files whose sha256 changed ({len(moved)}):")
        lines += [f"    - `{p}`" for p in moved]
    if added:
        changed = True
        lines.append(f"- files newly tracked by the manifest ({len(added)}):")
        lines += [f"    - `{p}`" for p in added]
    if dropped:
        changed = True
        lines.append(f"- files no longer tracked by the manifest ({len(dropped)}):")
        lines += [f"    - `{p}`" for p in dropped]
    if not (moved or added or dropped):
        lines.append("- no sha256 changes among manifest sources")

    u_old, u_new = _untracked_names(prev), _untracked_names(manifest)
    u_add, u_del = sorted(u_new - u_old), sorted(u_old - u_new)
    if u_add:
        changed = True
        lines.append(f"- untracked added ({len(u_add)}):")
        lines += [f"    - `{n}`" for n in u_add]
    if u_del:
        changed = True
        lines.append(f"- untracked removed ({len(u_del)}):")
        lines += [f"    - `{n}`" for n in u_del]
    if not (u_add or u_del):
        lines.append("- untracked set unchanged")

    if not changed:
        return [f"no change since {prev_date}"]
    return [f"Compared against `{prev_path.name}` ({prev_date}).", ""] + lines


def _brief_json_path(results, out_dir, today):
    """Where the brief JSON is -- referenced source first, staged copy second.

    The brief is no longer copied into exchange/, so this reads it where it
    actually lives.  The staged fallback keeps older archived runs readable.
    """
    for res in results:
        for ref in res.get("referenced", []):
            if ref["path"].endswith(".json"):
                return ROOT / ref["path"]
    legacy = out_dir / f"brief_{today}.json"
    return legacy if legacy.exists() else None


def brief_biases(results, out_dir, today):
    """Section 5 -- headline daily/weekly bias per asset, if the brief ran."""
    source = _brief_json_path(results, out_dir, today)
    if source is None or not source.exists():
        return None
    try:
        with source.open(encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError) as exc:
        return [f"Brief JSON staged but unreadable: {exc}"]

    assets = data.get("assets") or {}
    if not assets:
        return ["Brief JSON found but carried no assets block."]

    rows = ["| asset | daily bias | weekly bias |", "|---|---|---|"]
    for sym in sorted(assets):
        bias = (assets[sym] or {}).get("bias") or {}
        d = (bias.get("daily") or {}).get("verdict", "?")
        w = (bias.get("weekly") or {}).get("verdict", "?")
        rows.append(f"| {sym} | {d} | {w} |")
    return rows


# --------------------------------------------------------------- main


def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(
        description="Naiad daily routine. --slot runs the session-anchored "
                    "BRIEF-2 capture (Amendment 2 §2.3); without it the "
                    "routine behaves exactly as before.")
    ap.add_argument("--slot", default=None,
                    help="london | ny_am | post_ny")
    args = ap.parse_args(argv)

    reg = load_registry()
    slot = args.slot
    if slot is not None:
        allowed = reg.get("slots") or []
        if allowed and slot not in allowed:
            raise SystemExit(f"unknown slot {slot!r}; routine_jobs.json "
                             f"declares {allowed}")
        print(f"  slot: {slot}")
    today = date.today().strftime("%Y-%m-%d")
    out_dir = ROOT / reg["output_dir"]
    out_dir.mkdir(parents=True, exist_ok=True)

    python = reg["python"]
    if not Path(python).exists():
        raise SystemExit(f"configured interpreter does not exist: {python}")

    # Sweep FIRST: a file relocated now is inventoried by the manifest job and
    # published by this same run.
    swept = sweep_legacy_box()
    if swept:
        print(f"  sweep: {len(swept)} file(s) relocated out of _reviewer_box")

    results, halted = [], None
    for job in reg["jobs"]:
        res = run_job(job, python, today, out_dir, slot=slot)
        results.append(res)
        if res.get("skipped"):
            # Ruling 4a: a skip is REPORTED, never silent. A job that vanishes
            # from the output looks identical to a job that was forgotten.
            print(f"  {res['id']}: SKIPPED({res['skipped']})")
        else:
            print(f"  {res['id']}: exit={res['exit']} elapsed={res['elapsed']}s")
        if res["exit"] != 0 and res["required"]:
            halted = res["id"]
            break

    manifest = None
    staged_manifest = out_dir / f"MANIFEST_{today}.json"
    if staged_manifest.exists():
        try:
            with staged_manifest.open(encoding="utf-8") as fh:
                manifest = json.load(fh)
        except (OSError, ValueError):
            manifest = None

    failures = [r for r in results if r["exit"] != 0]
    skipped = [j["id"] for j in reg["jobs"] if j["id"] not in {r["id"] for r in results}]

    alerts, facts = check_reminders(reg, today)
    if alerts:
        print(f"  ACTION REQUIRED: {len(alerts)} item(s) overdue")

    out = [f"# DAILY -- {today}", ""]
    out.append(f"Generated {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')} "
               f"by `scripts/daily_routine.py` (registry version {reg.get('version')}).")
    out.append("")

    # D-0e.  ABOVE section 0, because a run that never happened outranks a
    # request inside a run that did.  Unnumbered on purpose: it is a banner that
    # appears only when there is something to say, not a standing section, so
    # numbering it would renumber every section below it on gap days only.
    _missed, _missed_reason = missed_runs(
        out_dir,
        ROOT / reg.get("daily_archive_dir", "research_outputs/_daily_archive"),
        ROOT / "exchange" / "status" / "HEARTBEAT.md",
        today)
    _missed_lines = missed_run_lines(_missed, _missed_reason, today)
    if _missed_lines:
        print(f"  MISSED RUNS: {len(_missed)} day(s) with no report"
              if not _missed_reason else f"  MISSED RUNS: UNKNOWN ({_missed_reason})")
    out += _missed_lines

    # 0. ACTION REQUIRED -- first, because it is the only section that asks the
    # operator to do something. Everything below is a record; this is a request.
    out.append("## 0. ACTION REQUIRED")
    out.append("")
    out += action_required_lines(alerts)
    out.append("")

    # 1. failures first, in plain language
    out.append("## 1. Failures")
    out.append("")
    # Ruling 4a (2026-08-15): skipped jobs are named here, above the failures.
    # "all jobs OK" alongside a job that never ran is technically true and
    # practically a lie -- a reader must be able to see what did NOT run.
    _skipped = [r for r in results if r.get("skipped")]
    if _skipped:
        for r in _skipped:
            out.append(f"- **{r['id']}** SKIPPED — {r['skipped']}. Not a failure; it was not run.")
        out.append("")

    if not failures:
        out.append("all jobs OK")
    else:
        for r in failures:
            kind = "required" if r["required"] else "optional"
            out.append(f"- **{r['id']}** ({kind}) failed with exit code {r['exit']}.")
            if r["error"]:
                out.append(f"  Last thing it said: {r['error']}")
            if r["required"]:
                out.append("  This job is required, so the run stopped here.")
            else:
                out.append("  This job is optional, so the run continued without it.")
        if skipped:
            out.append(f"- Not attempted because the run stopped: {', '.join(skipped)}.")
    out.append("")

    # 2. per-job detail
    out.append("## 2. Jobs")
    out.append("")
    out.append("| job | exit code | elapsed (s) | staged | referenced |")
    out.append("|---|---:|---:|---|---:|")
    for r in results:
        staged = ", ".join(f"`{s}`" for s in r["staged"]) if r["staged"] else "--"
        nref = len(r.get("referenced", [])) or "--"
        out.append(f"| {r['id']} | {r['exit']} | {r['elapsed']} | {staged} | {nref} |")
    for r in results:
        if r["missing"]:
            out.append("")
            out.append(f"Declared outputs missing for **{r['id']}**: "
                       + ", ".join(f"`{m}`" for m in r["missing"]))
    out.append("")

    # 3. repo state
    out.append("## 3. Repo state")
    out.append("")
    out += repo_state(manifest)
    out.append("")

    # 4. change since last run
    out.append("## 4. Change since last run")
    out.append("")
    out += change_since_last(manifest, out_dir, today)
    out.append("")

    # 5. brief biases
    out.append("## 5. Headline bias")
    out.append("")
    biases = brief_biases(results, out_dir, today)
    out += biases if biases else ["The brief did not run, so there is no bias table today."]
    out.append("")

    # 6. referenced artifacts -- pointers, not copies
    out.append("## 6. Brief artifacts — referenced, not copied")
    out.append("")
    out += reference_lines(results)
    out.append("")

    # 7. legacy box sweep
    out.append("## 7. Legacy box sweep")
    out.append("")
    out += sweep_lines(swept)
    out.append("")

    # 8. bus health -- ruling 007.  The residue of the retired DIGEST and the
    # dormant HERMES lane, measured rather than maintained.
    out.append("## 8. Bus health")
    out.append("")
    try:
        out += bus_health_lines(today)
    except Exception as exc:                            # noqa: BLE001
        # This section is a REPORT LINE.  It is assembled before the report is
        # written, before the heartbeat, and before the publish, so an escape
        # here would cost all three and leave a bare traceback in the launchd
        # log -- the routine dying of the section that exists to say the
        # routine is healthy.  It degrades to a stated reason instead.
        out.append(f"NOT ENUMERABLE — the bus-health block raised "
                   f"{type(exc).__name__}: {exc}")
        out.append("")
        out.append("_The rest of this report is unaffected; the block is "
                   "reporting only._")
        print(f"  bus-health: NOT ENUMERABLE ({type(exc).__name__}: {exc})")
    out.append("")

    report = out_dir / f"DAILY_{today}.md"
    report.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"wrote {report.relative_to(ROOT).as_posix()}")

    # 9. ROLLING WINDOW -- runs after the report is written so that today's own
    # DAILY_<date>.md is on disk and counts as the newest member of the window.
    archive_dir = ROOT / reg.get("daily_archive_dir", "research_outputs/_daily_archive")
    keep = reg.get("keep_daily", 7)
    windowed = apply_rolling_window(out_dir, archive_dir, keep)
    if windowed:
        print(f"  window: {len(windowed)} file(s) aged out of {reg['output_dir']}")
    with report.open("a", encoding="utf-8") as fh:
        fh.write("\n## 9. Rolling window\n\n")
        fh.write("\n".join(window_lines(windowed, out_dir, keep, archive_dir)) + "\n")

    # HEARTBEAT -- written BEFORE publish on purpose.  It has to be inside the
    # commit, because the whole point is that a stale timestamp on GitHub is
    # itself the alert; a heartbeat that always lags one run cannot do that job.
    # The cost is that the exit code it carries is the pre-publish one, which
    # the file says plainly rather than implying otherwise.
    pre_publish_rc = 1 if [r for r in results if r["exit"] != 0 and r["required"]] else 0
    write_heartbeat(facts, alerts, pre_publish_rc, ROOT / "exchange" / "status" / "HEARTBEAT.md")

    # 10. PUBLISH -- gate A-6a.  Runs AFTER the report is written so that the
    # report itself is inside the commit.  The publish outcome is then appended
    # to the report; those appended bytes ride along in the NEXT publish, which
    # is the price of having the report be part of what it describes.
    pub = None
    if reg.get("publish", True):
        pub = publish_exchange.publish(ROOT, today)
        with report.open("a", encoding="utf-8") as fh:
            fh.write("\n## 10. Publish\n\n")
            fh.write("_Appended after the publish step ran; these bytes are "
                     "published by the next run, not this one._\n\n")
            fh.write("\n".join(publish_exchange.report_lines(pub)) + "\n")
    else:
        with report.open("a", encoding="utf-8") as fh:
            fh.write("\n## 10. Publish\n\n")
            fh.write("- disabled in the registry (`\"publish\": false`)\n")

    required_failed = [r["id"] for r in results if r["exit"] != 0 and r["required"]]
    if required_failed:
        print(f"FAILED (required): {', '.join(required_failed)}")
        return 1
    if pub is not None and pub["status"] in ("FLAGGED", "ERROR"):
        # Non-zero on purpose: an unattended 07:00 run must surface a publish
        # that did not happen as a FAILED task, not as a line nobody reads.
        # ERROR counts as well as FLAGGED -- learned the hard way on the first
        # real run, where a stale index.lock stopped the publish dead and the
        # routine still exited 0.  A bus that did not update is a failure
        # whether the cause was the guard or the plumbing.
        print(f"FAILED (publish {pub['status']}) -- see the report")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
