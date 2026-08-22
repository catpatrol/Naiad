#!/usr/bin/env python
"""rotate_reports.py -- move aged build documents off the exchange bus.

Queue 003, D-1 (ratified operator 2026-08-11).

WHY THIS EXISTS.  `exchange/` is ticked into the project box and grows with
every session BY DESIGN: CONVENTIONS 3.1 requires one build document per
session, read-only sessions included, and that rule is correct.  The bus is not
growing because anyone is careless; it is growing because the record is being
kept.  Measured against the then-6.39 MB box: 17.9% on 2026-08-05, 26.4% on
2026-08-11, and a REFUSE at 40.2% on 2026-08-15 that stopped a paste dead.

The box was raised that day by operator ruling to 16 MB, and its thresholds were
recalibrated the same day on the APOLLO -> ATHENA governance transfer to warn
40% / refuse 70%.  THIS SCRIPT DID NOT CHANGE THROUGH EITHER: the ceiling rose,
the thresholds moved, the housekeeping stayed.  AGE_DAYS is still 30.  The live
values are read from `publish_exchange.BOX_BYTES` / `WARN_FRACTION` /
`REFUSE_FRACTION` -- never copied here -- so both changes reached this module for
free, which is the whole argument for importing.  Rotation is not a pressure
valve for a full box; it is how the record stays navigable.

Metering note: since 2026-08-15 the guard governs on the TICK SET
(`exchange/` + `publish_exchange.TICK_EXTRA`, i.e. the ledger), not on
`exchange/` alone.  Rotation still only ever moves files inside `exchange/`.

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

# The six lanes, plus the two broadcast tokens a note can be addressed to.
# Used ONLY to parse a note's recipient out of its filename -- see note_pair().
LANES = ("APOLLO", "ARGUS", "ATHENA", "DIONYSUS", "HEPHAESTUS", "HERMES")
BROADCAST = ("ALL-LANES", "ALL", "PANTHEON", "LANES")

# PINNED at ratification 2026-08-11 (queue 003 finding 3.1).  The contract
# shipped this number carrying a [VETO] marker; the operator let the drafted
# default stand.  It is a constant, not a flag: a rotation window that can be
# widened from the command line is a rotation window that will be widened at
# the moment someone wants a file gone, which is the one moment to refuse.
AGE_DAYS = 30

CHUNK = 1024 * 1024
DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")
# Notes.  The exemption keeps the NEWEST note of each lane pair -- see
# newest_note_per_lane_pair().
#
# CORRECTION 2026-08-22 (queue 003 correction, operator-ratified).  This read
# `^NOTE_.+_to_.+`, which only ever matched NOTE_<FROM>_to_<TO>_... .  Broadcasts
# -- NOTE_HERMES_2026-08-12_ALL-LANES_..., NOTE_DIONYSUS_2026-08-12_PANTHEON_...
# -- never matched it, so they were NEVER EXEMPTIBLE AT ALL, even on the days the
# DIGEST read worked.  The widening is deliberate and is named in the contract.
NOTE_RE = re.compile(r"^NOTE_", re.IGNORECASE)


class InboxSourceUnavailable(RuntimeError):
    """The exemption rule's INPUT cannot be obtained.

    RETAINED, NOT RAISED, since the 2026-08-22 correction.  The ratified
    exemption is now computed from exchange/reports/ itself
    (newest_note_per_lane_pair), and a rule with no external input has no
    unavailable state -- so nothing in this module raises this any more.  It
    stays defined because daily_routine.rotation_candidate_lines() names it in
    an `except` clause, and because if a future exemption source is ever ruled
    to live outside the bus, this is the shape it must fail in.

    The original rationale, preserved because it is the reason the halt was
    right at the time:

    Raised -- never swallowed -- when the unacted-inbox list cannot be read.
    Queue 003 exempts "any NOTE_*_to_* file listed as unacted inbox in the
    newest DIGEST".  It does not authorise this script to GUESS when that list
    is unavailable, and an unknown inbox is not an empty inbox.

    Deliberately a RuntimeError and not a SystemExit: main() turns it into a
    loud non-zero exit for the operator, while a library caller (the daily
    routine's bus-health block) catches it and reports NOT ENUMERABLE instead
    of dying.  A SystemExit here would take down an unattended 07:00 run.
    """


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


def note_pair(name: str):
    """(sender, recipient) for a NOTE filename, or None if it is not a note.

    Three shapes exist on the bus and all three are parsed:

        NOTE_<FROM>_to_<TO>_<date>_<topic>.md        ARGUS   -> APOLLO
        NOTE_<FROM>_<date>_TO_<TO>_<topic>.md        APOLLO  -> ATHENA
        NOTE_<FROM>_<date>_<BROADCAST>_<topic>.md    HERMES  -> ALL-LANES

    Anything that starts NOTE_ but names no recipient is treated as a BROADCAST
    rather than dropped: an unparsed note must still land in SOME pair, because a
    note that belongs to no pair is a note the exemption cannot protect.  That is
    the direction to fail in -- a too-wide exemption keeps a file one more cycle,
    a too-narrow one rotates a live message off the bus.
    """
    if not NOTE_RE.match(name):
        return None
    stem = Path(name).stem
    tokens = stem.split("_")[1:]                       # drop the NOTE_ prefix
    if not tokens:
        return None
    sender = tokens[0].upper()
    for i, tok in enumerate(tokens[1:], start=1):
        up = tok.upper()
        if up == "TO" and i + 1 < len(tokens):
            nxt = tokens[i + 1].upper()
            if nxt in LANES:
                return sender, nxt
        if up in BROADCAST:
            return sender, "ALL-LANES"
        if up in LANES and up != sender:
            return sender, up
    return sender, "ALL-LANES"


def newest_note_per_lane_pair(src_dir: Path = None) -> set:
    """Basenames of the notes that are the NEWEST of their lane pair.

    THIS IS D-1's EXEMPTION INPUT since the 2026-08-22 correction.  A note is
    live while it is the most recent thing its sender said to its recipient;
    once a newer note of the same pair exists, the older one has been superseded
    by it and may rotate.

    WHY IT REPLACED THE DIGEST READ.  The ratified rule exempted "any
    NOTE_*_to_* file listed as unacted inbox in the newest DIGEST".  Ruling 007
    retired the DIGEST on 2026-08-15 and the exemption's only input died with it,
    so this script halted -- correctly, since guessing which notes are live is
    exactly the guess that rotates a live message off the bus, but with the
    consequence that NO rotation could run for seven days (finding F-2,
    2026-08-18).  The rule now reads the bus itself.

    THE PROPERTY THAT MATTERS: this function has no external input, so unlike
    the DIGEST read it CANNOT become unavailable.  It never raises
    InboxSourceUnavailable; a missing scope directory yields an empty set, which
    is correct rather than unknown -- no directory means no notes to protect.
    """
    src_dir = (REPO / SCOPE_DIR) if src_dir is None else Path(src_dir)
    if not src_dir.is_dir():
        return set()
    best = {}
    for path in sorted(src_dir.glob("*.md")):
        pair = note_pair(path.name)
        if pair is None:
            continue
        # A note under a FABRICATED tree (the fixtures) has no git history, so
        # only its filename can date it.  Asking resolve_date() for a path
        # outside the repo used to raise ValueError out of relative_to() --
        # caught by F-ROT-3 on the first run of these fixtures, before this
        # function had ever been pointed anywhere but the live bus.
        try:
            rel = path.relative_to(REPO).as_posix()
        except ValueError:
            when = None
            m = DATE_RE.search(path.name)
            if m:
                try:
                    when = datetime.strptime(m.group(1), "%Y-%m-%d").date()
                except ValueError:
                    when = None
        else:
            when, _how = resolve_date(rel)
        # (date, mtime) -- the date decides, mtime breaks the tie when two notes
        # of one pair carry the same date, which has happened (DIONYSUS->APOLLO,
        # both 2026-08-04).
        key = (when or date_min(), path.stat().st_mtime)
        if pair not in best or key > best[pair][0]:
            best[pair] = (key, path.name)
    return {name for _key, name in best.values()}


def date_min():
    """The floor for an undated note, so it never outranks a dated one."""
    return datetime.min.date()


def classify(today, inbox=None):
    """Partition exchange/reports/*.md into candidates, exempt, and too-young.

    `inbox` overrides the exemption set instead of computing it.  Added
    2026-08-15 (ruling 007) for ONE caller: the daily bus-health block, which
    reports a candidate COUNT and had to keep producing one while the DIGEST
    retirement left the old exemption with nothing to read.  Passing an empty
    set means "no exemptions applied", which makes the count an UPPER BOUND --
    and the report says so in those words.

    CORRECTION 2026-08-22: the default no longer raises.  It computes the
    exemption from the bus itself (newest_note_per_lane_pair), which has no
    external input and so cannot become unavailable.  The override survives
    because it is still the honest way for a REPORTING caller to ask for the
    unexempted upper bound, and because deleting a parameter that one caller
    passes by keyword is a break with no benefit.
    """
    src_dir = REPO / SCOPE_DIR
    cutoff = today - timedelta(days=AGE_DAYS)
    inbox = newest_note_per_lane_pair(src_dir) if inbox is None else inbox
    candidates, exempt, young, undated = [], [], [], []
    if not src_dir.is_dir():
        return candidates, exempt, young, undated, cutoff, inbox

    for path in sorted(src_dir.glob("*.md")):
        rel = path.relative_to(REPO).as_posix()
        name = path.name
        size = path.stat().st_size
        when, how = resolve_date(rel)

        if NOTE_RE.match(name) and name in inbox:
            exempt.append((rel, size, when, "newest note of its lane pair"))
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
    print("  exemption    : %d note(s) -- newest of their lane pair, computed from "
          "%s/ (queue 003 correction 2026-08-22)" % (len(inbox), SCOPE_DIR))
    for nm in sorted(inbox):
        pair = note_pair(nm)
        print("      EXEMPT  %-14s -> %-10s %s"
              % (pair[0] if pair else "?", pair[1] if pair else "?", nm))
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
    try:
        return rotate(execute=bool(args.execute))
    except InboxSourceUnavailable as exc:
        # A HALT, not a traceback.  classify() raises before any file is
        # examined and long before any git mv, so nothing is half-done here --
        # the sweep simply reports that it cannot answer and moves nothing.
        print("rotate_reports -- HALT: the unacted-inbox exemption has no source.")
        print("  %s" % exc)
        print("  Nothing was classified. Nothing was moved. Exit 2.")
        return 2


if __name__ == "__main__":
    sys.exit(main())
