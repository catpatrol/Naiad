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

import subprocess
from pathlib import Path

SCOPE = "exchange/"
SUBJECT = "exchange: auto-publish {date}"


def _git(repo, args, timeout=300):
    """Run one git command.  Returns (returncode, stdout, stderr) as text."""
    proc = subprocess.run(
        ["git"] + args,
        cwd=str(repo),
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


def _staged_paths(repo):
    rc, out, err = _git(repo, ["diff", "--cached", "--name-only", "-z"])
    if rc != 0:
        raise RuntimeError("git diff --cached failed: %s" % err.strip())
    return [p for p in out.split("\0") if p]


def publish(repo, date_str, remote="origin", log=print):
    """Stage exchange/** only, guard the index, then commit and push.

    Returns a result dict with a "status" of:
      PUBLISHED  -- committed and pushed; "commit" holds the short sha
      NOTHING    -- exchange/ had no changes; nothing staged, nothing pushed
      FLAGGED    -- the guard tripped; index reset, push skipped, see "offenders"
      ERROR      -- a git command failed; see "error"
    Never raises.  A publish failure must not fail the job that called it.
    """
    repo = Path(repo)
    result = {"status": "ERROR", "offenders": [], "staged": [],
              "commit": None, "branch": None, "error": None, "pushed": False}

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


def report_lines(result):
    """Render a publish result as markdown lines for a report section."""
    status = result.get("status")
    if status == "PUBLISHED":
        return [
            f"- committed `{result['commit']}` on `{result['branch']}` and pushed to origin",
            f"- {len(result['staged'])} path(s) published, all inside `{SCOPE}`",
        ]
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
