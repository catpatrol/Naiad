#!/usr/bin/env python
"""publish_exchange.py -- the auto-publish step and the guard that bounds it.

Standing rule (ruling Q-2 A, FUNNEL_DIONYSUS_W1, 2026-08-02):

    Coordination state under exchange/** auto-publishes.
    Evidence NEVER publishes without the operator.

This module is the single implementation of that rule.  Both
scripts/daily_routine.py and scripts/backup_estate.py call publish() as their
final step, so there is one guard to audit rather than two copies to drift.

THE GUARD, in one sentence: after staging, every single staged path must begin
with "exchange/" -- and if even one does not, NOTHING is pushed.

Why it is written as "verify after staging" rather than "stage carefully":
`git add -- exchange` stages what we asked for, but it cannot tell us what was
ALREADY in the index when we arrived.  A half-finished `git add` from an
earlier session, a merge in progress, a hook -- any of these can leave study
code staged, and a commit would then publish evidence under an "auto-publish"
subject line.  So the guard reads the index back and judges the whole of it.

On a violation the index is reset (`git reset`, mixed, no paths), a FLAG line
is emitted, and the push is skipped.  That discards staging state the operator
may have set up by hand -- deliberately.  It touches no working-tree file and
loses no work; the alternative is publishing evidence by accident, which is the
one outcome the rule exists to prevent.

Nothing here is destructive to the worktree.  No file is written, moved or
deleted by this module.
"""

import datetime as _dt
import os
import re
import subprocess
from pathlib import Path

SCOPE = "exchange/"
SUBJECT = "exchange: auto-publish {date}"

# ------------------------------------------------------- F-P6: routine freshness
#
# The unmasking line, 2026-08-12.  Queue 002 made PUBLISH refresh MANIFEST.json.
# That closed one defect and opened a worse one: `MANIFEST.json` is the file every
# lane reads to check the repo is alive, and after 002 its freshness only proves
# that SOMEONE PUBLISHED -- not that the daily routine ran.  On 2026-08-09 the
# routine halted; eleven publishes on 08-11 kept the manifest looking six hours
# old, and the outage went unseen for three days.
#
# So publish now states, every time, when the ROUTINE last completed -- a fact it
# reads from HEARTBEAT.md and does not itself write.  The signal and the thing it
# signals are separated again.
#
# PRINT-ONLY, NEVER BLOCKS.  A stale heartbeat is information, not a reason to
# refuse a publish: the publishes are usually how a human is repairing the very
# outage being reported.  A guard that blocked here would fight the repair.
HEARTBEAT_PATH = "exchange/status/HEARTBEAT.md"
STALE_AFTER_HOURS = 36.0
_HEARTBEAT_RUN = re.compile(r"^\s*run:\s*(\S+)", re.M)

# --------------------------------------------------------------- size budget
#
# D3, queue 002 (ratified 2026-08-04, ruling G5-a).  The scope guard above
# answers "is this the right KIND of file"; it has never answered "is there too
# much of it".  Those are different questions and only the first was ever asked:
# `offenders= []` on every run means "nothing outside exchange/", never anything
# about size.
#
# Why a TOTAL and not a per-file cap: exchange/ reached 51.4% of the project box
# while NINE OF ITS TEN largest data files were each under the 1 MB per-file cap
# in CONVENTIONS §4.2.  A per-file limit cannot catch an aggregate; only the sum
# can.  The box held ~6.39 MB and had overflowed twice (raised to 16 MB on
# 2026-08-15, below), and the three web lanes reach repo content ONLY through it
# -- so an overflow is not an inconvenience, it is those lanes going blind.
#
# WARN, then REFUSE, then an override that is always available: a guard with no
# escape hatch becomes something people route around, and the routing-around is
# what actually loses the safety.  The override prints what it let through.
# RAISED by operator ruling 2026-08-15 ["box", VETO]: 6.39 MB -> 16 MB, warn
# 25% -> 50%, refuse 40% -> 80%.  The ceiling rises; the housekeeping stays --
# the 30-day rotation (queue 003, next ~2026-08-28) remains scheduled and
# AGE_DAYS is untouched.  The ruling was taken after the VIZ-2 paste was
# REFUSED at 40.16% with all four payloads already built and local: the guard
# worked, and the number it was defending had simply gone stale.
BOX_BYTES = 16_000_000

# RECALIBRATED 2026-08-15 by ATHENA on the box-governance transfer (APOLLO ->
# ATHENA handoff note, operator go "edit these limits to proportions reasonable
# to new capabilities"): warn 0.50 -> 0.40, refuse 0.80 -> 0.70.  The raise
# moved the ceiling but left the thresholds where a 6.39 MB box had put them,
# proportionally; at 0.50/0.80 the first warning would not arrive until 8 MB, by
# which point the bus would have tripled with nothing said.  0.40/0.70 restores
# a margin that warns while there is still room to act: warn 6.4 MB, refuse
# 11.2 MB, against a current footprint near 2.6 MB.
#
# BOUNDARY SEMANTICS ARE UNCHANGED and are the comparators below, not these
# numbers: `> REFUSE` and `>= WARN`, so exactly 70.0% warns and does not refuse,
# exactly as exactly 80.0% did.  F-BOX-1 proves it at both edges.
WARN_FRACTION = 0.40
REFUSE_FRACTION = 0.70
OVERRIDE_ENV = "NAIAD_ALLOW_OVERSIZE_PUBLISH"

# D3 METERING GAP -- CLOSED 2026-08-15.  The box holds `LEDGER.md` AND
# `exchange/` (DIGEST §1).  The guard metered `exchange/` alone and so
# under-reported true occupancy by the size of the ledger -- ~4 points on the
# old 6.39 MB box, ~1.6 on this one.  Open since ATHENA's queue-003 report of
# 2026-08-11 and transferred with the governance.  Closed here: the THRESHOLDS
# NOW GOVERN ON THE TICK SET.  The exchange-only figure keeps being printed
# beside it, because every prior report quotes that number and a reader
# comparing across cycles must not be handed a silent redefinition.
TICK_EXTRA = ("LEDGER.md",)

# Quoted verbatim on refusal.  A refusal that does not say what to do instead is
# just an obstacle; this names the remedy CONVENTIONS already ratified.
POINTER_RULE = (
    "CONVENTIONS §4.2: text only, 1 MB per file. Larger artifacts are referenced "
    "by path + sha256 pointer, never copied in. Captures and renders go to "
    "briefs/; study artifacts to research_outputs/; local working files to "
    "_reviewer_box/."
)


def _git(repo, args, timeout=300, stdin=None):
    """Run one git command.  Returns (returncode, stdout, stderr) as text."""
    proc = subprocess.run(
        ["git"] + args,
        cwd=str(repo),
        input=None if stdin is None else stdin.encode("utf-8"),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
    )
    return (proc.returncode,
            proc.stdout.decode("utf-8", "replace"),
            proc.stderr.decode("utf-8", "replace"))


def guard(staged):
    """The scope guard, as a pure function so it can be tested without a repo.

    staged -- list of repo-relative paths, as `git diff --cached --name-only`
              reports them (forward slashes).

    Returns (ok, offenders).  ok is True only when EVERY path is inside the
    published scope.  An empty list is ok: nothing staged is not a violation,
    it just means there is nothing to publish.
    """
    offenders = [p for p in staged if p and not p.startswith(SCOPE)]
    return (not offenders), offenders


def budget(total_bytes, box=BOX_BYTES):
    """The size budget, as a pure function so it can be tested without a repo.

    Returns (level, fraction) where level is "OK", "WARN" or "REFUSE".

    `total_bytes` is the TICK SET -- `exchange/` plus TICK_EXTRA -- since the
    D3 gap was closed on 2026-08-15.  Callers that pass exchange-only bytes get
    an under-reading, which is the defect that closure exists to remove.

    Thresholds are read as: WARN at or above WARN_FRACTION, REFUSE strictly
    above REFUSE_FRACTION -- 40% and 70% since the 2026-08-15 recalibration.
    "REFUSE above 70%" is taken literally -- exactly 70.0% warns, it does not
    refuse -- because a boundary that refuses its own stated limit surprises the
    one reader who checked the number first.  The comparators below are the
    definition; the constants only move where the edges sit.
    """
    frac = (total_bytes / box) if box else 0.0
    if frac > REFUSE_FRACTION:
        return "REFUSE", frac
    if frac >= WARN_FRACTION:
        return "WARN", frac
    return "OK", frac


def heartbeat_line(text, now=None):
    """F-P6.  Render the routine-freshness line from HEARTBEAT.md's contents.

    A pure function of (text, now) -- like budget() above -- so the STALE and
    MISSING branches can be demonstrated on doctored input without touching the
    real heartbeat or waiting two days for one to go stale.

    `text` is the file's contents, or None if it could not be read.  Returns the
    single line publish should print.  Never raises: an unreadable, truncated or
    garbled heartbeat reports itself as MISSING rather than taking down the
    publish that is probably trying to fix it.
    """
    if now is None:
        now = _dt.datetime.now(_dt.timezone.utc)
    if not text:
        return "publish: *** HEARTBEAT MISSING *** (%s unreadable)" % HEARTBEAT_PATH
    match = _HEARTBEAT_RUN.search(text)
    if not match:
        return ("publish: *** HEARTBEAT MISSING *** (no `run:` line in %s)"
                % HEARTBEAT_PATH)
    stamp = match.group(1).strip()
    try:
        parsed = _dt.datetime.fromisoformat(stamp.replace("Z", "+00:00"))
    except ValueError:
        return ("publish: *** HEARTBEAT MISSING *** (unparseable run stamp %r in %s)"
                % (stamp, HEARTBEAT_PATH))
    if parsed.tzinfo is None:                    # naive stamp: read it as UTC
        parsed = parsed.replace(tzinfo=_dt.timezone.utc)
    hours = (now - parsed).total_seconds() / 3600.0
    line = ("publish: routine last completed %s (%.0fh ago)"
            % (parsed.date().isoformat(), hours))
    if hours > STALE_AFTER_HOURS:
        line += " *** STALE >%dh ***" % STALE_AFTER_HOURS
    return line


def heartbeat_text(repo):
    """HEARTBEAT.md's contents, or None if it cannot be read for any reason."""
    try:
        return Path(repo, *HEARTBEAT_PATH.split("/")).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def tick_extra_bytes(repo):
    """Bytes of the tracked box members that sit OUTSIDE `exchange/`.

    Measured at HEAD, not in the index, and deliberately: publish only ever
    commits `exchange/` -- the scope guard forbids anything else -- so a
    TICK_EXTRA file's contribution to the box is whatever is already committed.
    Reading the index here would report 0 and silently re-open the gap.

    Returns (total_bytes, [(size, path)]).
    """
    rows = []
    for path in TICK_EXTRA:
        rc, out, _err = _git(repo, ["ls-tree", "-l", "HEAD", "--", path])
        if rc != 0 or not out.strip():
            continue
        for line in out.splitlines():
            parts = line.split()
            # <mode> <type> <sha> <size>\t<path>
            if len(parts) >= 4 and parts[3].isdigit():
                rows.append((int(parts[3]), line.split("\t", 1)[-1]))
    return sum(sz for sz, _ in rows), rows


def budget_lines(scope_total, tick_total, level):
    """The dual-figure budget report -- printed on EVERY publish, not only on
    warn/refuse.  A ceiling that only speaks when it is angry teaches the bus
    nothing on the way up.

    Percentages against a ceiling that has just moved are exactly the figure a
    reader mis-reads, so the absolute MB is printed beside every one of them.
    """
    def mb(b):
        return f"{b / 1e6:.2f} MB"
    return [
        "publish: box %s -- TICK SET %s B (%s) = %.2f%% of %s B (%s)  [governs]"
        % (level, f"{tick_total:,}", mb(tick_total),
           100.0 * tick_total / BOX_BYTES, f"{BOX_BYTES:,}", mb(BOX_BYTES)),
        "publish:     exchange-only %s B (%s) = %.2f%%   [continuity with prior reports]"
        % (f"{scope_total:,}", mb(scope_total), 100.0 * scope_total / BOX_BYTES),
        "publish:     warn %.0f%% = %s · refuse %.0f%% = %s"
        % (100 * WARN_FRACTION, mb(BOX_BYTES * WARN_FRACTION),
           100 * REFUSE_FRACTION, mb(BOX_BYTES * REFUSE_FRACTION)),
    ]


def _index_sizes(repo):
    """[(size, path)] for every SCOPE path in the index, largest first.

    Reads the INDEX, not the worktree: the question D3 asks is "how big is what
    we are about to publish", and after `git add` that is the index.  Sizes come
    from the staged blobs via cat-file, so a file staged and then edited in the
    worktree is measured as the bytes that would actually be committed.
    """
    rc, out, err = _git(repo, ["ls-files", "-s", "-z", "--", SCOPE.rstrip("/")])
    if rc != 0:
        raise RuntimeError("git ls-files failed: %s" % err.strip())
    entries = []
    for rec in out.split("\0"):
        if not rec:
            continue
        meta, _, path = rec.partition("\t")
        parts = meta.split()
        if len(parts) >= 2 and path:
            entries.append((parts[1], path))
    if not entries:
        return []
    rc, out, err = _git(repo, ["cat-file", "--batch-check"],
                        stdin="".join(sha + "\n" for sha, _ in entries))
    if rc != 0:
        raise RuntimeError("git cat-file failed: %s" % err.strip())
    lines = out.split("\n")
    sized = []
    for (sha, path), line in zip(entries, lines):
        parts = line.split()
        if len(parts) >= 3 and parts[2].isdigit():
            sized.append((int(parts[2]), path))
    sized.sort(reverse=True)
    return sized


def _staged_paths(repo):
    rc, out, err = _git(repo, ["diff", "--cached", "--name-only", "-z"])
    if rc != 0:
        raise RuntimeError("git diff --cached failed: %s" % err.strip())
    return [p for p in out.split("\0") if p]


def publish(repo, date_str, remote="origin", log=print, allow_oversize=None):
    """Stage exchange/** only, guard the index, then commit and push.

    Returns a result dict with a "status" of:
      PUBLISHED  -- committed and pushed; "commit" holds the short sha
      NOTHING    -- exchange/ had no changes; nothing staged, nothing pushed
      FLAGGED    -- the scope guard tripped; index reset, push skipped, see "offenders"
      REFUSED    -- the D3 size budget tripped; index reset, push skipped
      ERROR      -- a git command failed; see "error"
    Never raises.  A publish failure must not fail the job that called it.

    allow_oversize -- override the D3 refusal.  None (default) consults
    $NAIAD_ALLOW_OVERSIZE_PUBLISH so a caller that cannot pass the argument
    still has an escape hatch; True/False decide it outright.  An override is
    always announced on screen -- a silent override is the same defect as a
    silent no-op.
    """
    repo = Path(repo)
    if allow_oversize is None:
        allow_oversize = os.environ.get(OVERRIDE_ENV, "").strip().lower() in (
            "1", "true", "yes", "on")
    result = {"status": "ERROR", "offenders": [], "staged": [],
              "commit": None, "branch": None, "error": None, "pushed": False,
              "bytes": None, "fraction": None, "budget": None, "heartbeat": None,
              "largest": [], "oversize_override": bool(allow_oversize)}

    try:
        rc, branch, err = _git(repo, ["rev-parse", "--abbrev-ref", "HEAD"])
        if rc != 0:
            result["error"] = "cannot resolve branch: %s" % err.strip()
            return result
        branch = branch.strip()
        result["branch"] = branch
        if branch == "HEAD":
            result["error"] = "detached HEAD -- refusing to auto-publish"
            return result

        rc, _, err = _git(repo, ["add", "--", "exchange"])
        if rc != 0:
            result["error"] = "git add failed: %s" % err.strip()
            if "index.lock" in err:
                # Seen for real on 2026-08-02: a zero-byte .git/index.lock left
                # behind by an interrupted git run the previous day silently
                # blocked every staging attempt.  Say so precisely, because the
                # generic message sends people looking for a running process
                # that is not there.
                result["error"] = (
                    "git add blocked by .git/index.lock. If no git process is "
                    "running, the lock is stale and must be removed BY HAND. "
                    "This script will not delete it: a lock that is not stale "
                    "is protecting a real operation. Original: %s" % err.strip())
            log("publish: %s" % result["error"])
            return result

        staged = _staged_paths(repo)
        result["staged"] = staged

        ok, offenders = guard(staged)
        if not ok:
            result["status"] = "FLAGGED"
            result["offenders"] = offenders
            _git(repo, ["reset"])          # unstage everything, worktree untouched
            log("FLAG: publish aborted -- %d staged path(s) outside %s: %s"
                % (len(offenders), SCOPE, ", ".join(offenders[:10])))
            log("FLAG: index reset; nothing was committed and nothing was pushed.")
            return result

        if not staged:
            result["status"] = "NOTHING"
            log("publish: exchange/ unchanged -- nothing to commit.")
            return result

        # --- D3: total-size budget.  Runs AFTER the scope guard, never instead
        # of it: size is an ADDITIONAL check and a small file in the wrong place
        # is still a violation.
        sized = _index_sizes(repo)
        scope_total = sum(sz for sz, _ in sized)
        extra_total, extra_rows = tick_extra_bytes(repo)
        total = scope_total + extra_total          # the TICK SET; it governs
        level, frac = budget(total)
        # `bytes` / `fraction` keep their historical meaning -- exchange-only --
        # so no prior consumer is handed a silent redefinition.  The governing
        # figures are the tick_* keys, and `budget` is derived from them.
        result["bytes"] = scope_total
        result["fraction"] = scope_total / BOX_BYTES if BOX_BYTES else 0.0
        result["tick_bytes"] = total
        result["tick_fraction"] = frac
        result["tick_extra"] = extra_rows
        result["budget"] = level
        result["largest"] = sized[:10]

        for line in budget_lines(scope_total, total, level):
            log(line)

        if level == "WARN":
            log("publish: WARNING -- the box holds %s B (tick set), %.1f%% of "
                "the %s B box (warn at %d%%, refuse above %d%%)."
                % (f"{total:,}", 100 * frac, f"{BOX_BYTES:,}",
                   100 * WARN_FRACTION, 100 * REFUSE_FRACTION))
        elif level == "REFUSE":
            for line in _oversize_lines(total, frac, sized):
                log(line)
            if not allow_oversize:
                result["status"] = "REFUSED"
                _git(repo, ["reset"])
                log("REFUSE: publish aborted by the size budget; index reset, "
                    "nothing committed, nothing pushed.")
                log("REFUSE: override with allow_oversize=True or %s=1 if this "
                    "publish is legitimate." % OVERRIDE_ENV)
                # printed here too: this path returns early, and a dead routine
                # is worth knowing about even on a publish that was refused.
                log(heartbeat_line(heartbeat_text(repo)))
                return result
            log("publish: size budget OVERRIDDEN (%s) -- publishing %s B anyway."
                % ("allow_oversize=True" if os.environ.get(OVERRIDE_ENV, "") == ""
                   else OVERRIDE_ENV, f"{total:,}"))

        # F-P6: the routine-freshness line, immediately after the budget report.
        # Read, never written, by this module -- publish reports the heartbeat,
        # it does not produce one, which is the whole point of the separation.
        result["heartbeat"] = heartbeat_line(heartbeat_text(repo))
        log(result["heartbeat"])

        rc, out, err = _git(repo, ["commit", "-m", SUBJECT.format(date=date_str)])
        if rc != 0:
            result["error"] = "git commit failed: %s" % (err.strip() or out.strip())
            return result

        rc, sha, _ = _git(repo, ["rev-parse", "--short", "HEAD"])
        result["commit"] = sha.strip() if rc == 0 else None

        rc, out, err = _git(repo, ["push", remote, branch], timeout=600)
        if rc != 0:
            result["status"] = "ERROR"
            result["error"] = "committed %s but push failed: %s" % (
                result["commit"], err.strip() or out.strip())
            log("publish: committed %s but PUSH FAILED -- %s"
                % (result["commit"], result["error"]))
            return result

        result["pushed"] = True
        result["status"] = "PUBLISHED"
        log("publish: committed %s (%d path(s)) and pushed to %s/%s"
            % (result["commit"], len(staged), remote, branch))
        return result

    except (OSError, RuntimeError, subprocess.SubprocessError) as exc:
        result["error"] = str(exc)
        log("publish: ERROR -- %s" % exc)
        return result


def _oversize_lines(total, frac, sized):
    """The refusal message: the number, the ten largest, and the remedy."""
    out = [
        "REFUSE: the box holds %s B (%.2f MB) across the tick set (%s + %s), "
        "%.1f%% of the %s B project box -- above the %d%% ceiling (%.1f MB)."
        % (f"{total:,}", total / 1e6, SCOPE, " + ".join(TICK_EXTRA),
           100 * frac, f"{BOX_BYTES:,}", 100 * REFUSE_FRACTION,
           BOX_BYTES * REFUSE_FRACTION / 1e6),
        "REFUSE: the ten largest staged paths:",
    ]
    for sz, path in sized[:10]:
        out.append("    %10s B  %5.2f%%  %s" % (f"{sz:,}", 100.0 * sz / BOX_BYTES, path))
    out.append("REFUSE: " + POINTER_RULE)
    return out


def report_lines(result):
    """Render a publish result as markdown lines for a report section."""
    status = result.get("status")
    if status == "PUBLISHED":
        lines = [
            f"- committed `{result['commit']}` on `{result['branch']}` and pushed to origin",
            f"- {len(result['staged'])} path(s) published, all inside `{SCOPE}`",
        ]
        if result.get("bytes") is not None:
            tb = result.get("tick_bytes", result["bytes"])
            tf = result.get("tick_fraction", result["fraction"])
            lines.append(
                f"- box budget **{result.get('budget')}** — tick set "
                f"({SCOPE} + {' + '.join(TICK_EXTRA)}): {tb:,} B / {tb / 1e6:.2f} MB "
                f"= {100 * tf:.1f}% of {BOX_BYTES:,} B ({BOX_BYTES / 1e6:.0f} MB) "
                f"— **governs**")
            lines.append(
                f"- `{SCOPE}` only: {result['bytes']:,} B / "
                f"{result['bytes'] / 1e6:.2f} MB = {100 * result['fraction']:.1f}% "
                f"— continuity with prior reports")
            lines.append(
                f"- warn {100 * WARN_FRACTION:.0f}% = "
                f"{BOX_BYTES * WARN_FRACTION / 1e6:.1f} MB · refuse "
                f"{100 * REFUSE_FRACTION:.0f}% = "
                f"{BOX_BYTES * REFUSE_FRACTION / 1e6:.1f} MB")
        if result.get("budget") == "REFUSE" and result.get("oversize_override"):
            lines.append("- **the size ceiling was OVERRIDDEN for this publish**")
        if result.get("heartbeat"):
            lines.append("- %s" % result["heartbeat"].replace("publish: ", "", 1))
        return lines
    if status == "REFUSED":
        lines = [
            "- **REFUSED — publish aborted by the D3 size budget.** The tick set "
            f"(`{SCOPE}` + {' + '.join(TICK_EXTRA)}) holds "
            f"{result.get('tick_bytes', result['bytes']):,} B / "
            f"{result.get('tick_bytes', result['bytes']) / 1e6:.2f} MB, "
            f"{100 * result.get('tick_fraction', result['fraction']):.1f}% of the "
            f"{BOX_BYTES:,} B box, above the {100 * REFUSE_FRACTION:.0f}% ceiling "
            f"({BOX_BYTES * REFUSE_FRACTION / 1e6:.1f} MB):",
        ]
        lines += [f"    - `{p}` — {sz:,} B ({100.0 * sz / BOX_BYTES:.2f}%)"
                  for sz, p in result.get("largest", [])]
        lines.append(f"- {POINTER_RULE}")
        lines.append("- the index was reset; nothing was committed and nothing was pushed")
        lines.append(f"- override with `allow_oversize=True` or `{OVERRIDE_ENV}=1`")
        return lines
    if status == "NOTHING":
        return ["- `exchange/` was unchanged; nothing committed, nothing pushed"]
    if status == "FLAGGED":
        lines = [
            "- **FLAG — publish aborted by the scope guard.** "
            f"{len(result['offenders'])} staged path(s) fell outside `{SCOPE}`:",
        ]
        lines += [f"    - `{p}`" for p in result["offenders"][:20]]
        if len(result["offenders"]) > 20:
            lines.append(f"    - … and {len(result['offenders']) - 20} more")
        lines.append("- the index was reset; nothing was committed and nothing was pushed")
        lines.append("- this is the evidence-never-auto-publishes rule doing its job; "
                     "resolve the staged paths by hand, then re-run")
        return lines
    return [f"- publish did not complete: {result.get('error') or 'unknown error'}"]
