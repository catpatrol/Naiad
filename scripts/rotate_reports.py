#!/usr/bin/env python
"""rotate_reports.py -- move aged build documents off the exchange bus.

Queue 003, D-1 (ratified operator 2026-08-11).

WHY THIS EXISTS.  `exchange/` is ticked into the ~6.39 MB project box and grows
with every session BY DESIGN: CONVENTIONS 3.1 requires one build document per
session, read-only sessions included, and that rule is correct.  The bus is not
growing because anyone is careless; it is growing because the record is being
kept.  Measured: 17.9% of the box on 2026-08-05, 26.4% on 2026-08-11.  Queue
002's D3 guard warns at 25% and refuses above 40%.  Without rotation, ordinary
reporting reaches the refuse line in roughly ten more days of similar activity.

So: the current month's record stays hot on the bus; everything older moves to
docs/history/reports/YYYY-MM/, where it is still tracked, still on GitHub, and
still reachable by `git log --follow`.  Nothing leaves the repository.

THE CENTRAL INVARIANT: THIS SCRIPT MOVES.  IT NEVER DESTROYS.
No deletion primitive of any kind appears anywhere in this file -- not in the
code, not in a comment, not behind a flag.  Verify it rather than trusting it;
003's verdict criteria require exactly that grep to come back empty.  The only
mutation performed is `git mv`, which relocates a tracked file and preserves the
history that makes the relocation reversible.

WHY `git mv` AND NOT A FILESYSTEM COPY.  A copy plus a removal would lose the
rename record, and `git log --follow` would stop at the move.  A build document
whose history stops is worth less than one that was never rotated -- the whole
point is that the record stays retrievable.  So the move goes through git, and
F-303-3 asserts the history really does follow.

SAFETY POSTURE.  --dry-run is the DEFAULT.  Moving requires --execute, typed on
purpose.  Every file is hashed before the move and re-hashed at its destination,
and a mismatch stops the run.  An occupied destination is refused, never
overwritten.  Nothing rotates unattended: D-2 puts the candidate list in HERMES's
box-budget section each cycle and the operator says when to sweep.
"""

import argparse
import hashlib
import re
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import publish_exchange                                  # noqa: E402

# Scope, destination and log.  All repo-relative, forward slashes.
SCOPE_DIR = "exchange/reports"
DEST_ROOT = "docs/history/reports"
LOG_PATH = "exchange/status/ROTATION_LOG.md"
DIGEST_PATH = "exchange/DIGEST.md"

# PINNED at ratification 2026-08-11 (queue 003 finding 3.1).  The contract
# shipped this number carrying a [VETO] marker; the operator let the drafted
# default stand.  It is a constant, not a flag: a rotation window that can be
# widened from the command line is a rotation window that will be widened at
# the moment someone wants a file gone, which is the one moment to refuse.
AGE_DAYS = 30

CHUNK = 1024 * 1024
DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")
# Inbox notes, exempt while unacted -- see digest_inbox_names().
NOTE_RE = re.compile(r"^NOTE_.+_to_.+", re.IGNORECASE)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(CHUNK), b""):
            h.update(block)
    return h.hexdigest()


def git(*args) -> tuple:
    proc = subprocess.run(["git", "-C", str(REPO), *args],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return (proc.returncode,
            proc.stdout.decode("utf-8", "replace"),
            proc.stderr.decode("utf-8", "replace"))


def resolve_date(rel: str):
    """(date, how) for one repo-relative report path.

    Filename first: these documents are named for the day they describe, and
    that is the date a reader means.  Only when the name carries no date do we
    ask git when the file first appeared -- the contract's stated fallback.
    A file with neither is reported and never selected: an unknown age is not
    an old age, and guessing in the direction of "move it" is the wrong guess.
    """
    m = DATE_RE.search(Path(rel).name)
    if m:
        try:
            return datetime.strptime(m.group(1), "%Y-%m-%d").date(), "filename"
        except ValueError:
            pass
    rc, out, _ = git("log", "--diff-filter=A", "--follow",
                     "--format=%ad", "--date=short", "--", rel)
    dates = [l.strip() for l in out.splitlines() if l.strip()]
    if not dates:
        rc, out, _ = git("log", "--format=%ad", "--date=short", "--", rel)
        dates = [l.strip() for l in out.splitlines() if l.strip()]
    if dates:
        try:
            return datetime.strptime(dates[-1], "%Y-%m-%d").date(), "git log"
        except ValueError:
            pass
    return None, "unknown"


def digest_inbox_names() -> set:
    """Basenames listed in the newest DIGEST's inbox section.

    The contract exempts "any NOTE_*_to_* file listed as unacted inbox in the
    newest DIGEST".  An open note is a message somebody still owes a reply to;
    rotating it off the bus would file the request as history before it was
    answered.  Parsing is deliberately loose -- any report basename appearing
    anywhere in the inbox section counts -- because the failure that matters is
    rotating a live note, and a too-wide exemption merely keeps a file one more
    cycle.
    """
    p = REPO / DIGEST_PATH
    if not p.is_file():
        return set()
    try:
        text = p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return set()
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.startswith("#") and "inbox" in line.lower():
            start = i
            break
    if start is None:
        section = text                      # no section found: search it all
    else:
        end = len(lines)
        for j in range(start + 1, len(lines)):
            if lines[j].startswith("## "):
                end = j
                break
        section = "\n".join(lines[start:end])
    return {m for m in re.findall(r"[A-Za-z0-9_.\-]+\.md", section)}


def classify(today):
    """Partition exchange/reports/*.md into candidates, exempt, and too-young."""
    src_dir = REPO / SCOPE_DIR
    cutoff = today - timedelta(days=AGE_DAYS)
    inbox = digest_inbox_names()
    candidates, exempt, young, undated = [], [], [], []
    if not src_dir.is_dir():
        return candidates, exempt, young, undated, cutoff, inbox

    for path in sorted(src_dir.glob("*.md")):
        rel = path.relative_to(REPO).as_posix()
        name = path.name
        size = path.stat().st_size
        when, how = resolve_date(rel)

        if NOTE_RE.match(name) and name in inbox:
            exempt.append((rel, size, when, "unacted inbox note in DIGEST"))
            continue
        if when is None:
            undated.append((rel, size, None, "no date in name, none in git log"))
            continue
        if when >= cutoff:
            young.append((rel, size, when, how))
            continue
        candidates.append((rel, size, when, how))
    return candidates, exempt, young, undated, cutoff, inbox


def tracked_exchange_bytes() -> int:
    """Bytes of tracked files under exchange/, as they sit in the worktree."""
    rc, out, _ = git("ls-files", "-z", "--", "exchange")
    total = 0
    for rel in out.split("\0"):
        if not rel:
            continue
        p = REPO / rel
        try:
            total += p.stat().st_size
        except OSError:
            pass
    return total


def box_line(prefix: str) -> str:
    b = tracked_exchange_bytes()
    box = publish_exchange.BOX_BYTES
    return "%s %s B, %.1f%% of the %s B box" % (prefix, f"{b:,}", 100.0 * b / box, f"{box:,}")


def append_log(rows) -> Path:
    """Append one line per rotated file.  Creates the log with a header once."""
    p = REPO / LOG_PATH
    p.parent.mkdir(parents=True, exist_ok=True)
    new = not p.exists()
    with open(p, "ab") as fh:
        if new:
            fh.write((
                "# ROTATION LOG\n"
                "\n"
                "Append-only record of build documents moved off the exchange bus by\n"
                "`scripts/rotate_reports.py` (queue 003, D-1). Every entry is a MOVE:\n"
                "the file is still tracked, still on GitHub, and `git log --follow`\n"
                "still returns its full history at the new path.\n"
                "\n"
                "| rotated | file | new path | sha256 |\n"
                "|---|---|---|---|\n").encode("utf-8"))
        for stamp, name, dest, sha in rows:
            fh.write(("| %s | `%s` | `%s` | `%s` |\n"
                      % (stamp, name, dest, sha)).encode("utf-8"))
    return p


def rotate(execute: bool, today=None) -> int:
    today = today or datetime.now().date()
    stamp = today.strftime("%Y-%m-%d")
    candidates, exempt, young, undated, cutoff, inbox = classify(today)

    print("rotate_reports -- %s" % ("EXECUTE" if execute else "DRY RUN (default)"))
    print("  scope        : %s/*.md" % SCOPE_DIR)
    print("  today        : %s   window: %d days   cutoff: files dated before %s"
          % (stamp, AGE_DAYS, cutoff.isoformat()))
    print("  destination  : %s/YYYY-MM/" % DEST_ROOT)
    print("  DIGEST inbox : %d name(s) parsed from %s" % (len(inbox), DIGEST_PATH))
    print("  " + box_line("before       :"))
    print("")

    cand_bytes = sum(s for _, s, _, _ in candidates)
    box = publish_exchange.BOX_BYTES
    print("  CANDIDATES  : %d file(s), %s B, %.2f%% of box"
          % (len(candidates), f"{cand_bytes:,}", 100.0 * cand_bytes / box))
    for rel, size, when, how in candidates:
        print("      %s  %9s B  %s  (date from %s)" % (when.isoformat(), f"{size:,}", rel, how))
    if not candidates:
        print("      (none -- nothing on the bus is older than the window)")

    print("  EXEMPT      : %d file(s)" % len(exempt))
    for rel, size, when, why in exempt:
        print("      %9s B  %s  -- %s" % (f"{size:,}", rel, why))
    print("  TOO YOUNG   : %d file(s) inside the %d-day window" % (len(young), AGE_DAYS))
    if undated:
        print("  UNDATED     : %d file(s) -- NOT selected; an unknown age is not an old age"
              % len(undated))
        for rel, size, _, why in undated:
            print("      %9s B  %s  -- %s" % (f"{size:,}", rel, why))

    if not execute:
        print("")
        print("  DRY RUN: nothing moved. Re-run with --execute to move the candidates.")
        return 0

    if not candidates:
        print("")
        print("  EXECUTE: no candidates; nothing to move.")
        return 0

    print("")
    print("  moving (sha256 -> git mv -> re-hash at destination):")
    rows, failures = [], 0
    for rel, size, when, _how in candidates:
        src = REPO / rel
        dest_rel = "%s/%s/%s" % (DEST_ROOT, when.strftime("%Y-%m"), Path(rel).name)
        dest = REPO / dest_rel
        if dest.exists():
            print("      REFUSED  %s -- destination already occupied: %s" % (rel, dest_rel))
            print("               nothing was moved for this file; resolve by hand.")
            failures += 1
            continue
        before = sha256_file(src)
        dest.parent.mkdir(parents=True, exist_ok=True)
        rc, out, err = git("mv", rel, dest_rel)
        if rc != 0:
            print("      FAILED   %s -- git mv: %s" % (rel, (err or out).strip()))
            failures += 1
            continue
        if not dest.is_file():
            print("      FAILED   %s -- destination missing after git mv" % rel)
            failures += 1
            continue
        after = sha256_file(dest)
        if after != before:
            print("      FAILED   %s -- sha256 changed in transit (%s -> %s)"
                  % (rel, before[:16], after[:16]))
            failures += 1
            continue
        rows.append((stamp, Path(rel).name, dest_rel, before))
        print("      MOVED    %s -> %s  sha256=%s...  (%s B, verified at destination)"
              % (rel, dest_rel, before[:16], f"{size:,}"))

    if rows:
        log = append_log(rows)
        print("")
        print("  wrote %d line(s) to %s" % (len(rows), log.relative_to(REPO).as_posix()))

    print("  " + box_line("after        :"))
    print("")
    print("  %d moved, %d refused/failed" % (len(rows), failures))
    if rows:
        print("  NOTE: `git mv` stages BOTH paths, and the new one is outside exchange/.")
        print("        publish_exchange's scope guard will FLAG that index and reset it.")
        print("        Commit the rotation yourself first, then publish exchange/ -- see")
        print("        the queue 003 build document.")
    return 1 if failures else 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--dry-run", action="store_true",
                   help="report only, move nothing (this is the default)")
    g.add_argument("--execute", action="store_true",
                   help="actually move the candidates; required, never implied")
    args = ap.parse_args()
    return rotate(execute=bool(args.execute))


if __name__ == "__main__":
    sys.exit(main())
