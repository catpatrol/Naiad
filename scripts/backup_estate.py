#!/usr/bin/env python
"""backup_estate.py -- dated, hashed, bidirectionally-verified archives.

Reference implementation: the manual run recorded in LEDGER.md under
"2026-07-27 -- Estate protection established" (LEDGER.md:743-757).  That run
established the pattern this script reproduces: compress -> verify in BOTH
directions -> only then consider the source releasable, per-phase atomic, with
an embedded MANIFEST.json carrying {rel_path,size,sha256} for every member.

MODES
  --estate            (default) the irreplaceable price estate, resolved by
                      CALLING engine.data.cache_dir() so NAIAD_CACHE_DIR is
                      honoured.  census.json stores RELATIVE paths only
                      (LEDGER.md:762 item 3) and is therefore used to check
                      COMPLETENESS, never to locate anything.
  --workflow          the irreplaceable everything-else: docs/memory,
                      docs/knowledge, skills, prompts, claude, exchange,
                      docs/primers, docs/history, scripts, the repo-root *.md
                      documents, and the operator-exports drop.
                      Dated, hashed and verified exactly like --estate; members
                      keep their repo-relative paths so a restore lands them
                      back where they came from.  Added 2026-08-02.
  --phase <name>      one research_outputs/<name> subtree.
  --verify <zip>      recompute every member's sha256 from inside the archive
                      and compare against the embedded manifest.  Extracts
                      nothing, writes nothing.

INVARIANTS
  * Read-only on every source.  This script does not delete the estate, ever.
  * All hashing is hashlib over binary reads, chunked.  No shell text tools.
  * A hard environment assertion runs before ANY read or write.
  * Archive names are dated and never overwritten -- an existing target halts.
  * Standard library only, except engine.data.cache_dir() in --estate mode.

DELETION -- deliberately opt-in.  The spec for --phase permits deleting
UNTRACKED source files once verification reports zero mismatches, and the
reference run did exactly that.  Because deletion is irreversible and this
project's own record shows the builder halting to ask rather than deleting
unprompted (LEDGER.md:756), it is gated behind an explicit --delete-source
flag.  Without that flag the run archives, verifies, and REPORTS what it would
have released.  Git-tracked files are preserved in place under every setting.

FIXTURES (all must pass; any failure exits non-zero)
  F-K1 member integrity, every member, both directions
  F-K2 completeness vs census.json (60/60 klines, 10/10 funding)
  F-K3 source untouched (sha sample + git status identical before/after)
  F-K4 restore rehearsal into a temp dir asserted OUTSIDE the repo
  F-K5 destination verification -- archive re-read FROM the destination
  F-K6 no-clobber
  F-K7 tracked-file preservation

AMENDMENT 2026-08-02 (gates A-5a, A-6a).  Two additions, neither of which
touches the archive path:

  RETENTION REPORT.  After a successful --estate run, the script reports the
  archive estate against the retention rule and names every GENERATION outside
  it.  It REPORTS ONLY.  It never deletes, and it never will -- the DELETION
  note above governs, and pruning backups unprompted is exactly the class of act
  this project halts to ask about.  The report is written to
  exchange/status/RETENTION.md (overwritten each run, so it is a current-state
  surface, not an accumulating log) and echoed to stdout.

  CORRECTION 2026-08-03.  The rule originally read "keep the newest 4 estate
  generations plus 1 phase set".  The phase clause was WRONG and is removed:
  phase archives are not generations of one thing, so keeping only the newest
  dated set flagged 1,025.2 MB of unique study evidence as prunable.  The rule
  is now "keep the newest 4 estate + 4 workflow generations; phase archives are
  PERMANENT EVIDENCE and are never prunable".

AMENDMENT 2026-08-03.  --force-same-day.  The no-clobber guard is correct and
stays on by default, but it made no distinction between overwriting YESTERDAY's
archive (a real loss) and re-running TODAY's (ordinary).  It had forced four
manual archive deletions -- a safety rail that trains the operator to delete
archives by hand is doing harm.  With the flag, and only when the existing file
was written today, the new archive takes a -NN suffix and BOTH are kept.  An
archive from an earlier day still refuses, flag or no flag.

  PUBLISH.  --estate and --phase runs end by staging exchange/** ONLY, checking
  the whole index against that scope, and pushing if and only if it is clean
  (scripts/publish_exchange.py).  --verify does neither: it is an inspection
  mode and stays read-only.  This is the one place the script writes inside the
  repo; every source remains read-only, as before.

AMENDMENT 2026-08-11 -- queue 002 (ratified 2026-08-04, rulings G1-a / G5-a;
amended 2026-08-06 ruling B).  Three defects fixed, all of them measured:

  D1  --phase now writes its ARCHIVE off-machine, to $NAIAD_PHASE_ARCHIVE_ROOT
      or --phase-archive-root, default D:/Naiad/research_outputs/_archive, and
      HALTS if that drive is not mounted rather than falling back to the laptop.
      Its SIDECAR stays tracked in research_outputs/_archive/, which is what
      makes an archive provable from a clone that has never seen the drive.
      --mirror DIR takes an ADDITIONAL verified copy after F-K5 passes, checked
      by re-reading FROM the mirror and refusing to overwrite anything.

      SUPERSEDED 2026-08-15 (DATA RESIDENCY v2) -- D1's text above is kept as
      the record of why the split exists.  What changed: the archive is now
      BORN LOCAL, at REPO/research_outputs/_archive, and `--mirror` carries the
      verified second copy to /Volumes/LaCie/naiad-backups.  D1's premise was
      that the laptop was a synced OneDrive tree, so "off-machine" and "safe"
      were the same word; ~/Naiad is now unsynced and permanent, so they are
      not.  The invariant D1 actually protects -- the archive exists in two
      places and the second copy is VERIFIED, never assumed -- is unchanged,
      and mirror_phase_outputs() still re-reads FROM the mirror to prove it.
      The SIDECAR still stays tracked in-repo, for exactly the original reason.

  D2  --phase --dest is now an ERROR naming --mirror.  It used to parse cleanly,
      exit 0, print success and write inside the repo -- run_phase never read
      args.dest at all.  --estate and --workflow hard-fail without --dest; this
      was the one mode where the flag lied.

  D3  publish_exchange.py gained a TOTAL-size budget (see that module).  The
      scope guard answers "is this the right kind of file" and never answered
      "is there too much of it".

  CORRECTION to the PUBLISH paragraph above: publish is no longer "the one
  place the script writes inside the repo".  Since ruling B --phase also writes
  its sidecar to research_outputs/_archive/.  The archive itself no longer
  lands in the repo at all.  Every SOURCE remains read-only, as before.

AMENDMENT 2026-08-12 -- the backup destination is configuration again.
(ADDRESS UPDATED 2026-08-15: every `D:/naiad-backups` in this section is the
SAME PHYSICAL DISK now reached at `/Volumes/LaCie/naiad-backups`.  The Windows
paths and the DriveFS measurement below are retained as the record of how the
destination came to be configuration; they are not live paths on this host.)

  --estate and --workflow now DEFAULT to D:/naiad-backups (BACKUP_DEST_DEFAULT),
  overridable by $NAIAD_BACKUP_DEST and, above that, by an explicit --dest,
  which still wins exactly as before.  Both modes previously hard-failed
  without --dest.  That looked strict and was in fact the opposite: it pushed
  the only statement of WHERE the backups go into the argument string of a
  Windows scheduled task, where no clone can read it, no review can see it and
  no commit records a change to it.

  The move that prompted this: the operator relocated the backup folder from
  `G:/My Drive/naiad-backups` -- the Google Drive VIRTUAL mount -- to
  `D:/naiad-backups`, a physical external disk.  The off-site property survives
  the move because Google Drive for desktop mirrors that local folder back to
  the cloud; verified 2026-08-12 by decoding the DriveFS `SyncTargets` registry
  value, which names `D:\\naiad-backups` as a sync target for the signed-in
  account.  This was MEASURED, not inferred from the folder's existence.

  Note what did NOT change and is deliberately left to the operator: the two
  weekly scheduled tasks still pass `--dest "G:\\My Drive\\naiad-backups"`
  explicitly, and an explicit --dest wins.  Until those task arguments are
  edited, the Sunday runs still target the old path.  Changing a default cannot
  fix a hardcoded caller, and pretending otherwise is how a backup silently
  stops being one.
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import publish_exchange                                  # noqa: E402
from drive_wait import wait_for_drive                    # noqa: E402  (D-0b)

CHUNK = 1024 * 1024
REPO_PREFIX = "_repo/"

# Names the ARCHIVE FORMAT owns at the zip root.  build_archive() writes the
# member index as "MANIFEST.json" and verify_archive() both reads it back by
# that name and excludes it from the member set, so any SOURCE file that would
# land on the same arcname must be escaped instead of silently duplicated.
# See estate_members() for the measured failure this prevents.
RESERVED_ROOT_NAMES = frozenset({"MANIFEST.json"})
ESTATE_PREFIX = "_estate/"

# Retention rule -- REPORTING thresholds, never deletion thresholds.
#
# CORRECTED 2026-08-03.  `KEEP_PHASE_SETS = 1` is REMOVED, not retuned.
#
# The old rule grouped phase archives by date and kept only the newest dated
# "set", on the reasoning that they were archived in a batch and therefore aged
# as a batch.  That reasoning is wrong, and it was wrong in a dangerous
# direction: PHASE ARCHIVES ARE NOT GENERATIONS OF ONE THING.  s1, s2, s3, tc1,
# tc4, tc5 and v3_anchor each hold a DIFFERENT phase's evidence.  An older phase
# archive is not a superseded copy of a newer one -- it is the only copy of work
# that will never be produced again.
#
# Measured before the fix: the old rule flagged 8 archives totalling 1,025.2 MB
# as "outside the rule", including every study phase except the most recently
# archived one.  A retention report that names unique evidence as prunable is
# worse than no retention report, because it launders a deletion decision as
# routine housekeeping.
#
# Estate and workflow archives ARE generations -- each is a full snapshot of the
# same thing at a later moment -- so a keep-newest-N rule is correct for them.
KEEP_ESTATE_GENERATIONS = 4
KEEP_WORKFLOW_GENERATIONS = 4
# Phase archives have no keep-count. They are permanent evidence.
DATED_ZIP = re.compile(r"_(\d{4}-\d{2}-\d{2})\.zip$")

# --workflow mode: the project's THINKING, as opposed to its price estate.
# Repo-relative roots, archived under their own path so a restore lands them
# back where they came from.  A root that does not exist is skipped and named
# in the report -- absence is recorded, never silently passed over.
#
# scripts/ added 2026-08-02: the disposition inventory found the ENTIRE
# toolchain -- daily_brief.py, backup_estate.py, every census and recompute
# script -- protected by nothing but GitHub. One copy on one third-party
# service is not a backup.
#
# briefs/, docs/reports/, docs/handoffs/ added 2026-08-12 (ATHENA ruling O-3),
# for exactly the reason scripts/ was added and found the same way: the
# 2026-08-12 filing session measured which destinations this list actually
# covers, and these three held TRACKED content while sitting outside it. They
# had GitHub and nothing else -- the same "one copy on one third-party service"
# that the note above already refuses to call a backup.
#
# Measured before widening, because a backup list that silently grows is how a
# weekly job becomes an hourly one: briefs 3.92 MB / 12 files, docs/reports
# 0.26 MB / 2, docs/handoffs 0.02 MB / 2 -- 4.21 MB total against a 50 MB
# ceiling. If a future addition approaches that ceiling, measure again rather
# than assuming this one stayed cheap.
WORKFLOW_SOURCES = (
    "docs/memory",
    "docs/knowledge",
    "skills",
    "prompts",
    "claude",
    "exchange",
    "docs/primers",
    "docs/history",
    "docs/reports",
    "docs/handoffs",
    "briefs",
    "scripts",
    "drops/operator-exports",
    "exchange/drops/operator-exports",
)

# Repo-ROOT file globs, non-recursive.  Added 2026-08-02 for the same reason as
# scripts/: the charter, every contract, LEDGER.md and README.md sit at the repo
# root, belong to no directory in the list above, and were GitHub-only.
WORKFLOW_ROOT_GLOBS = ("*.md",)

# Never archived, from any root.  Compiled bytecode is regenerable, machine- and
# version-specific, and would add ~200 KB of noise that restores to something a
# different interpreter must discard anyway.
WORKFLOW_EXCLUDE_PARTS = ("__pycache__",)
WORKFLOW_EXCLUDE_SUFFIXES = (".pyc", ".pyo")

# --------------------------------------------------------------- phase archives
#
# AMENDMENT 2026-08-06, RULING B (queue 002).  The local archive root for
# --phase is the EXTERNAL DRIVE, not the repo.
#
# Before this, run_phase hardcoded `REPO / "research_outputs" / "_archive"` and
# never read args.dest at all -- so `--phase X --dest "G:/..."` parsed cleanly,
# exited 0, printed success, and wrote inside the repo anyway.  Every phase
# archive that ever reached off-machine storage got there because a human ran a
# paste, not because this mode put it there.
#
# The split now: the ARCHIVE (large, binary, unpublishable) lands on the drive;
# its SIDECAR (64 hex bytes, tracked, pushed to GitHub) stays in the repo.  That
# is what makes an archive provable from a clone that has never seen the drive.
#
# If the configured root is unreachable this HALTS.  It does not fall back to
# the laptop: a silent fallback is how 5.45 GB accumulated in a synced folder,
# and a backup that quietly lands on the machine it is backing up is not one.
# AMENDED 2026-08-15 (DATA RESIDENCY v2).  The rule above -- "never falls back
# to the laptop" -- was written when the laptop was a synced OneDrive tree and
# the archive had to be born off-machine to be safe.  v2 inverts that premise:
# ~/Naiad is now the permanent home and is not synced anywhere, so an archive
# born HERE is born in the right place.  --phase therefore writes LOCALLY and
# `--mirror` copies it to the backup volume as a SECOND step.  The distinction
# that matters is preserved exactly: the archive still ends up in two places,
# and the mirror still halts rather than pretending.  What changed is which of
# the two is the original.
PHASE_ARCHIVE_ROOT_DEFAULT = str(REPO / "research_outputs" / "_archive")
PHASE_ARCHIVE_ROOT_ENV = "NAIAD_PHASE_ARCHIVE_ROOT"
PHASE_SIDECAR_DIR = "research_outputs/_archive"

# ZIP RESIDENCY RULING, operator 2026-08-15:
#   "older zips live on the LaCie; new zips are born local; backups go to the
#    LaCie only."
#
# So the LOCAL _archive is a CURRENT-CYCLE working set, not the whole archive
# set, and it is EXPECTED to be empty right after an aging pass.  The aged-out
# zips live here.  This is a separate subtree from the estate/workflow backup
# destination -- the LaCie carries both, and they are not the same shelf.
PHASE_ARCHIVE_AGED_DEFAULT = "/Volumes/LaCie/Naiad/research_outputs/_archive"
PHASE_ARCHIVE_AGED_ENV = "NAIAD_PHASE_ARCHIVE_AGED"


def phase_archive_aged_path() -> Path:
    """Where aged-out phase zips live, $NAIAD_PHASE_ARCHIVE_AGED or the default."""
    return Path(os.environ.get(PHASE_ARCHIVE_AGED_ENV) or PHASE_ARCHIVE_AGED_DEFAULT)

# --------------------------------------------------------- estate/workflow dest
#
# AMENDMENT 2026-08-12.  --estate and --workflow gain a DEFAULT destination.
#
# Until now both modes hard-failed without --dest, so the destination lived only
# in the argument string of a Windows scheduled task -- a place no clone can
# read, no review can see, and no `git log` records.  The operator moved the
# backup folder from `G:/My Drive/naiad-backups` (the Google Drive virtual
# mount) to `D:/naiad-backups` (a physical external disk that Google Drive
# MIRRORS back to the cloud, verified 2026-08-12 from the DriveFS SyncTargets
# registry value), and nothing in the repository had to change for that move to
# happen -- which is exactly the problem.  The destination is now configuration,
# in the repo, under version control.
#
# Precedence, deliberately identical to --phase: an explicit --dest wins, then
# $NAIAD_BACKUP_DEST, then this default.  Explicit --dest STILL WINS, so every
# existing caller keeps its current behaviour and this change cannot silently
# redirect a backup somebody else configured.
#
# HALT-if-absent matches phase_archive_root(): the check is on the drive ANCHOR,
# so a first run on a freshly-mounted disk creates the folder, while an unplugged
# disk stops the run dead instead of quietly writing the backup onto the machine
# it is backing up.
# AMENDED 2026-08-15 (v2).  The physical external disk is the same object; only
# its address changed when the estate crossed to macOS.  D:/naiad-backups and
# /Volumes/LaCie/naiad-backups are the SAME FOLDER on the SAME DRIVE.
BACKUP_DEST_DEFAULT = "/Volumes/LaCie/naiad-backups"
BACKUP_DEST_ENV = "NAIAD_BACKUP_DEST"


# ------------------------------------------------------------------ D-0b
# Anchors that are NEVER waited on, and why.
#
# `G:\` is the Google Drive virtual mount.  A Drive mount is not a sleeping
# disk: when it is missing the client is not running, and no amount of waiting
# spins it up.  Waiting there would only delay an inevitable halt -- and the two
# Sunday tasks still pass `--dest "G:\My Drive\naiad-backups"` explicitly
# (open item O-6), so without this exclusion they would wait on the wrong drive.
#
# This is a LIST rather than a drive-type test because a drive-type test does
# not work.  Measured 2026-08-12 with GetDriveTypeW: C:\ = 3 (FIXED),
# D:\ = 3 (FIXED), G:\ = 3 (FIXED).  Windows reports the Drive mount as a fixed
# local disk, indistinguishable from the LaCie; and an ABSENT drive returns
# 1 (NO_ROOT_DIR) whatever it was, which is precisely the case we must classify.
# So the exclusion is declared, not detected.  Override with NAIAD_NO_WAIT_ANCHORS
# (semicolon-separated) if the Drive letter ever changes.
# AMENDED 2026-08-15 (v2).  `G:\` does not exist on this platform, and the
# GetDriveTypeW reasoning above is a Windows measurement that cannot be taken
# here at all.  The MECHANISM is kept -- a declared exclusion list is still the
# right shape, and a Drive/iCloud mount is still not a sleeping disk -- but the
# default is now EMPTY, because on macOS the one volume we wait for (the LaCie)
# is a real spinning disk that genuinely benefits from the wait.  Set
# $NAIAD_NO_WAIT_ANCHORS (semicolon-separated) if a virtual mount ever needs
# excluding again.  The Windows text above is retained as the reason the list
# exists; it is not a live measurement of this machine.
NO_WAIT_ANCHORS_DEFAULT = ""
NO_WAIT_ANCHORS_ENV = "NAIAD_NO_WAIT_ANCHORS"


def _no_wait_anchors() -> set:
    raw = os.environ.get(NO_WAIT_ANCHORS_ENV, NO_WAIT_ANCHORS_DEFAULT)
    return {a.strip().upper() for a in raw.split(";") if a.strip()}


def volume_anchor(root: Path) -> Path | None:
    """The mount point that must be PRESENT for `root` to be writable.

    ADDED 2026-08-15 (v2), and this is a CORRECTNESS FIX, not a port.

    Every caller here used `Path(root.anchor)`.  On Windows that is `D:\\` --
    exactly right.  On POSIX `Path("/Volumes/LaCie/naiad-backups").anchor` is
    `"/"`, the boot volume, which is ALWAYS mounted.  So on macOS the guard
    that exists to stop a backup landing on the machine it is backing up
    returned "reachable" no matter what -- including with the LaCie unplugged.
    The halt could not fire.  A guard that cannot fail is not a guard.

    Returns the mount point, or None when the path is on the boot volume and
    there is genuinely nothing external to wait for.
    """
    p = root if root.is_absolute() else Path(root).resolve()
    parts = p.parts
    # macOS mounts external volumes at /Volumes/<name>.
    if len(parts) >= 3 and parts[1] == "Volumes":
        return Path(parts[0]) / parts[1] / parts[2]
    if os.name == "nt":
        return Path(p.anchor) if p.anchor else None
    return None


def drive_ready(root: Path, note=print):
    """Is `root`'s drive reachable?  Waits for a sleeping disk.  Never raises.

    D-0b.  Replaces the bare `anchor.exists()` that every D: gate used to run.
    A single existence check returns False in milliseconds on a spun-down
    external disk, so it cannot tell "the drive is gone" from "the drive has
    not spun up yet" -- and we were reading the second as the first.

    Returns (ok, detail) where detail is a human-readable measurement suitable
    for appending to a halt message.  Anchors in NO_WAIT_ANCHORS are probed
    once, exactly as before, and never waited on.

    AMENDED 2026-08-15 (v2): the anchor comes from volume_anchor(), not from
    Path.anchor -- see that function for why the old form could not halt here.
    """
    anchor = volume_anchor(root)
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


# --------------------------------------------------------------- hashing

def sha256_file(path: Path) -> str:
    """sha256 of a file, chunked binary read.  Never loads the whole file."""
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(CHUNK), b""):
            h.update(block)
    return h.hexdigest()


def sha256_zip_member(zf: zipfile.ZipFile, name: str) -> tuple:
    """sha256 and byte length of a member, streamed out of the archive."""
    h, n = hashlib.sha256(), 0
    with zf.open(name, "r") as fh:
        for block in iter(lambda: fh.read(CHUNK), b""):
            h.update(block)
            n += len(block)
    return h.hexdigest(), n


# --------------------------------------------------------------- git (read-only)

def git(*args) -> tuple:
    proc = subprocess.run(["git", "-C", str(REPO), *args],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return proc.returncode, proc.stdout.decode("utf-8", "replace")


def git_head() -> str:
    rc, out = git("rev-parse", "HEAD")
    return out.strip() if rc == 0 else "unavailable"


def git_porcelain() -> str:
    rc, out = git("status", "--porcelain")
    return out if rc == 0 else "unavailable"


def git_tracked_under(rel_dir: str) -> set:
    """Tracked paths under rel_dir, NUL-delimited.

    -z is not a style preference.  Without it `git ls-files` C-quotes any path
    containing a non-ASCII byte -- it returns the literal 14 characters
    "docs/history/STATUS \\342\\200\\224 ... .txt" rather than the path -- and
    every consumer then asks whether a file by that literal name exists, is told
    no, and reports a tracked file as missing.  F-K7 failed exactly this way on
    the first --workflow run (2026-08-02): 3 of 64 tracked paths, all of them
    files with an em-dash in the name.  -z suppresses the quoting entirely.
    """
    rc, out = git("ls-files", "-z", "--", rel_dir)
    if rc != 0:
        return set()
    return {p for p in out.split("\0") if p}


# --------------------------------------------------------------- environment

def assert_environment(dest: Path, need_writable: bool) -> dict:
    """Hard precondition gate.  Runs before any source read or any write.

    A misrouted read-only run silently succeeds and returns plausible nonsense,
    which is precisely the failure the standing rule at LEDGER.md:761 exists to
    prevent -- so this asserts even when nothing will be written.
    """
    problems = []

    for marker in ("engine/data.py", "census.json", ".git"):
        if not (REPO / marker).exists():
            problems.append(f"repo marker missing: {marker}")

    if need_writable:
        if dest is None:
            problems.append("no --dest given")
        else:
            # D-0b.  All three modes funnel through this write probe, so a
            # sleeping disk must be given time to wake BEFORE mkdir decides it
            # is unwritable.  Reachable is still not writable -- the probe
            # below remains the actual test, exactly as before.
            ready, detail = drive_ready(dest)
            if not ready:
                problems.append(f"destination drive unreachable: {dest} ({detail})")
            try:
                dest.mkdir(parents=True, exist_ok=True)
                probe = dest / f".naiad_write_probe_{os.getpid()}"
                probe.write_bytes(b"probe")
                if probe.read_bytes() != b"probe":
                    problems.append(f"destination read-back mismatch: {dest}")
                probe.unlink()
            except OSError as exc:
                problems.append(f"destination not writable: {dest} ({exc})")

    if problems:
        sys.stderr.write("ENVIRONMENT ASSERTION FAILED\n")
        for p in problems:
            sys.stderr.write(f"  - {p}\n")
        raise SystemExit(2)

    onedrive = os.environ.get("OneDrive") or os.environ.get("OneDriveConsumer")
    return {"repo": str(REPO), "onedrive_root": onedrive, "head": git_head()}


def inside(child: Path, parent: str | None) -> bool:
    if not parent:
        return False
    try:
        child.resolve().relative_to(Path(parent).resolve())
        return True
    except (ValueError, OSError):
        return False


def phase_archive_root_path(override: str | None = None) -> Path:
    """Resolve the configured --phase archive root WITHOUT checking the mount.

    Split out 2026-08-12 (ruling O-4) so retention_report(), which has no args
    and must never halt, resolves the SAME path --phase writes to.  Before this
    the retention report looked in `REPO/research_outputs/_archive` and reported
    "none found" while nine archives sat on the drive -- a report that answers a
    different question from the one it appears to answer.
    """
    return Path(override
                or os.environ.get(PHASE_ARCHIVE_ROOT_ENV)
                or PHASE_ARCHIVE_ROOT_DEFAULT)


def phase_archive_root(args) -> Path:
    """Where --phase writes its archive.  Ruling B (2026-08-06), amended v2.

    Precedence: --phase-archive-root, then $NAIAD_PHASE_ARCHIVE_ROOT, then the
    repo-local default.  Configurable in all three places, but never silently.

    AMENDED 2026-08-15 (v2).  Ruling B sent the archive off-machine because the
    machine was a synced OneDrive tree.  Under v2 ~/Naiad is the permanent,
    unsynced home, so the archive is BORN LOCAL here and `--mirror` carries a
    copy to the backup volume.  Ruling B's substance -- the archive must exist
    in two places, and the second copy must never be faked -- is unchanged; see
    mirror_phase_outputs() for the half that still halts.

    Still HALTS with SystemExit(2) if the configured root IS on an external
    volume (an operator can still point this at the LaCie) and that volume is
    not mounted.  For a local root there is no volume to wait on, so
    volume_anchor() returns None and drive_ready() passes trivially.
    """
    root = phase_archive_root_path(getattr(args, "phase_archive_root", None))
    anchor = volume_anchor(root)
    ok, detail = drive_ready(root)
    if not ok:
        sys.stderr.write(
            f"PHASE ARCHIVE ROOT UNREACHABLE: {root}\n"
            f"  {detail}\n"
            f"  The volume {anchor} is not mounted.\n"
            f"  You have pointed --phase at an external volume, and it will NOT fall\n"
            f"  back to the laptop silently -- if you meant the local default, drop\n"
            f"  --phase-archive-root / ${PHASE_ARCHIVE_ROOT_ENV} and re-run.\n"
            f"  Otherwise mount the volume and re-run.\n")
        raise SystemExit(2)
    return root


def backup_dest_root(args) -> Path:
    """Where --estate and --workflow write.  Amendment 2026-08-12.

    Precedence: --dest, then $NAIAD_BACKUP_DEST, then BACKUP_DEST_DEFAULT.
    An explicit --dest always wins, so this cannot redirect an existing caller.

    HALTS with SystemExit(2) when the root's drive is not mounted, for the same
    reason phase_archive_root() does: --estate and --workflow protect the two
    irreplaceable things this project owns, and a backup that silently lands on
    the laptop it is backing up is not a backup.  The check is on the VOLUME
    ANCHOR (`/Volumes/LaCie`, or `D:\\` on Windows), not the full path, so a
    first run on a fresh disk creates the directory rather than refusing over a
    folder that does not exist yet.

    AMENDED 2026-08-15 (v2): anchor now comes from volume_anchor().  Under the
    old Path.anchor form this check was INERT on macOS -- see volume_anchor().
    """
    raw = (getattr(args, "dest", None)
           or os.environ.get(BACKUP_DEST_ENV)
           or BACKUP_DEST_DEFAULT)
    root = Path(raw)
    anchor = volume_anchor(root)
    ok, detail = drive_ready(root)
    if not ok:
        sys.stderr.write(
            f"BACKUP DESTINATION UNREACHABLE: {root}\n"
            f"  {detail}\n"
            f"  The volume {anchor} is not mounted.\n"
            f"  --estate and --workflow write off-machine and will NOT fall back to\n"
            f"  the laptop -- a backup that lands on the machine it is backing up is\n"
            f"  not a backup.\n"
            f"  Plug the drive, or point --dest / ${BACKUP_DEST_ENV} at a reachable\n"
            f"  directory.\n")
        raise SystemExit(2)
    if not getattr(args, "dest", None):
        src = (f"${BACKUP_DEST_ENV}" if os.environ.get(BACKUP_DEST_ENV)
               else "built-in default")
        print(f"destination      : {root}   (no --dest given; from {src})")
    return root


def mirror_phase_outputs(fx: "Fixtures", target: Path, sidecar: Path,
                         mirror_dir: Path, expect_sha: str) -> None:
    """D1.  Copy archive AND sidecar to mirror_dir, then verify FROM the mirror.

    Two rules the contract is explicit about, and both matter:

    * Verification re-reads the MIRRORED bytes.  Re-hashing the source would
      prove only that the source is still the source -- it would pass even if
      the copy never landed, which is exactly the failure a mirror exists to
      rule out.
    * No-clobber refuses rather than overwrites, and BOTH destinations are
      checked BEFORE either is written, so a refusal never leaves a half-mirror.
    """
    mirror_dir.mkdir(parents=True, exist_ok=True)
    m_archive = mirror_dir / target.name
    m_sidecar = mirror_dir / sidecar.name

    existing = [p for p in (m_archive, m_sidecar) if p.exists()]
    if existing:
        sys.stderr.write(
            "REFUSING TO CLOBBER THE MIRROR: "
            + ", ".join(str(p) for p in existing) + "\n"
            "  Mirrored archives are non-overwriting by design (D1, queue 002).\n"
            "  Nothing was written to the mirror; the source archive is intact.\n"
            "  Move or rename the existing file, or pass a different --mirror DIR.\n")
        raise SystemExit(3)

    shutil.copy2(target, m_archive)
    shutil.copy2(sidecar, m_sidecar)

    try:
        fresh = sha256_file(m_archive)                      # FROM the mirror
        with zipfile.ZipFile(m_archive, "r") as zf:
            crc_bad = zf.testzip()
        side = m_sidecar.read_text(encoding="utf-8").split()[0]
        ok = (fresh == expect_sha and crc_bad is None and side == expect_sha)
        fx.record("F-M1", ok,
                  f"mirror {mirror_dir}: re-read FROM mirror sha256 {fresh[:16]}... "
                  f"matches source={fresh == expect_sha}, "
                  f"sidecar matches={side == expect_sha}, CRC clean={crc_bad is None}")
    except Exception as exc:                       # noqa: BLE001
        fx.record("F-M1", False, f"mirror re-read raised: {exc}")


def assert_no_clobber(target: Path, force_same_day: bool = False) -> Path:
    """F-K6.  Dated names must accumulate generations, never overwrite one.

    Returns the path to write, which is `target` unless a same-day suffix was
    taken.  Raises SystemExit(3) when it refuses.

    --force-same-day (added 2026-08-03).  The guard is correct and stays on by
    default: a dated archive must never be silently overwritten, because the
    thing overwritten is a backup.  But a SAME-DAY re-run is a different case
    from a clobber -- re-running today's backup after fixing something is
    ordinary, and the guard has now forced FOUR manual archive deletions, which
    is worse than the risk it was defending: it trained the operator to delete
    archives by hand to get past a safety rail.

    So with the flag, and ONLY when the existing file was written TODAY, the new
    archive takes a `-NN` suffix and BOTH are kept. Nothing is deleted, nothing
    is overwritten, and yesterday's archive is still untouchable -- an older file
    refuses exactly as before, flag or no flag, because overwriting THAT would
    be a real loss.
    """
    if not target.exists():
        return target

    same_day = False
    try:
        same_day = (datetime.fromtimestamp(target.stat().st_mtime).date()
                    == datetime.now().date())
    except OSError:
        same_day = False

    if force_same_day and same_day:
        stem, suffix = target.stem, target.suffix
        for n in range(1, 100):
            alt = target.with_name(f"{stem}-{n:02d}{suffix}")
            if not alt.exists():
                print(f"  same-day re-run: {target.name} exists and was written "
                      f"today; writing {alt.name} instead (both are kept)")
                return alt
        sys.stderr.write(
            f"REFUSING TO CLOBBER: {target} and -01..-99 all exist.\n")
        raise SystemExit(3)

    hint = ("  The existing file was written TODAY — pass --force-same-day to "
            "write a -NN suffixed copy instead of halting.\n"
            if same_day else
            "  The existing file is from an EARLIER day; --force-same-day does "
            "NOT apply and will not help.\n")
    sys.stderr.write(
        f"REFUSING TO CLOBBER: {target} already exists.\n"
        f"  Dated archives are non-overwriting by design (ruling R-B).\n"
        + hint
        + f"  Move or rename the existing file, or pass a different --dest.\n")
    raise SystemExit(3)


# --------------------------------------------------------------- member collection

def walk_members(root: Path, prefix: str = "") -> list:
    """[(rel_path, abs_path)] for every file under root, sorted, forward slashes."""
    out = []
    for dirpath, _dirs, files in os.walk(root):
        for name in sorted(files):
            ap = Path(dirpath) / name
            rel = prefix + ap.relative_to(root).as_posix()
            out.append((rel, ap))
    return sorted(out, key=lambda t: t[0])


def estate_members(estate_root: Path) -> list:
    members = walk_members(estate_root)

    # RESERVED-NAME COLLISION, fixed 2026-08-15.  `MANIFEST.json` at the archive
    # ROOT belongs to the archive format: build_archive() writes the member
    # index under exactly that name, and verify_archive() reads it back with
    # `zf.read("MANIFEST.json")` and then EXCLUDES it from the member set with
    # `n != "MANIFEST.json"`.
    #
    # The estate cache has its own MANIFEST.json at its root.  Walking it
    # produced a SECOND zip entry under the reserved name, so every estate
    # archive carried two, and zipfile returns the LAST for a duplicated name.
    # Measured consequences, both of which the fixtures caught honestly:
    # F-K1 reported 1 omission (the cache's copy is in `pinned` but its name is
    # excluded from `in_zip`), and F-K4 restored `MANIFEST.json`, got the
    # generated index instead of the cache's, and reported 1 hash mismatch.
    # This was the SECOND of the two collisions found on 2026-08-15; removing
    # the stray `_repo/` from the cache fixed the other three and left this one.
    #
    # The fix is symmetric with REPO_PREFIX rather than novel: a member whose
    # arcname would collide with a reserved root name is stored under a prefix,
    # and resolve_member() maps it back.  The cache's manifest is PRESERVED --
    # dropping it would have been the smaller change and would have quietly
    # made restores incomplete.
    members = [((ESTATE_PREFIX + rel) if rel in RESERVED_ROOT_NAMES else rel, ap)
               for rel, ap in members]

    extras = ["census.json", "DATA_CENSUS.md",
              "research_outputs/census/build_manifest.json"]
    for rel in extras:
        ap = REPO / rel
        if not ap.exists():
            sys.stderr.write(f"required companion file missing: {rel}\n")
            raise SystemExit(2)
        members.append((REPO_PREFIX + rel, ap))
    return members


def resolve_member(rel: str, estate_root: Path, repo_root: Path) -> Path:
    if rel.startswith(REPO_PREFIX):
        return repo_root / rel[len(REPO_PREFIX):]
    if rel.startswith(ESTATE_PREFIX):          # reserved-name escape, see estate_members
        return estate_root / rel[len(ESTATE_PREFIX):]
    return estate_root / rel


def workflow_roots() -> tuple:
    """(present, missing, skipped_nested) for the --workflow source list.

    Two things this must get right:
      * a root that does not exist is REPORTED, not silently dropped -- an
        empty backup that looks complete is the failure this whole script
        exists to prevent;
      * a root nested inside another included root is skipped, or its files
        would be archived twice under two names.  exchange/drops/operator-
        exports is exactly that case: exchange/ already carries it.
    """
    present, missing = [], []
    for rel in WORKFLOW_SOURCES:
        (present if (REPO / rel).is_dir() else missing).append(rel)

    kept, nested = [], []
    for rel in present:
        parent = next((o for o in present
                       if o != rel and (rel + "/").startswith(o + "/")), None)
        (nested.append((rel, parent)) if parent else kept.append(rel))
    return kept, missing, nested


def _workflow_excluded(rel: str) -> bool:
    parts = rel.split("/")
    if any(p in WORKFLOW_EXCLUDE_PARTS for p in parts):
        return True
    return rel.endswith(WORKFLOW_EXCLUDE_SUFFIXES)


def workflow_root_files() -> list:
    """[(rel_path, abs_path)] for repo-ROOT files matching WORKFLOW_ROOT_GLOBS.

    Non-recursive by design: this covers the loose documents that live at the
    repo root and belong to no archived directory.  Recursing would duplicate
    everything already collected from the directory roots.
    """
    out = []
    for pattern in WORKFLOW_ROOT_GLOBS:
        for ap in sorted(REPO.glob(pattern)):
            if ap.is_file():
                out.append((ap.name, ap))
    return out


def workflow_members(roots) -> list:
    """[(rel_path, abs_path)] for every file under the workflow roots.

    Members keep their repo-relative path, so a restore puts them back exactly
    where they came from.
    """
    members = []
    for rel in roots:
        members.extend(walk_members(REPO / rel, prefix=rel + "/"))
    members.extend(workflow_root_files())
    members = [(rel, ap) for rel, ap in members if not _workflow_excluded(rel)]
    seen, unique = set(), []
    for rel, ap in sorted(members, key=lambda t: t[0]):
        if rel not in seen:          # a root file cannot also come from a dir,
            seen.add(rel)            # but belt-and-braces: never pin twice
            unique.append((rel, ap))
    return unique


# --------------------------------------------------------------- writing

def build_archive(members: list, target: Path, meta: dict) -> dict:
    """Compress, then embed the manifest.  Returns the manifest dict."""
    assert_no_clobber(target)
    files, total = [], 0
    tmp = target.with_suffix(target.suffix + ".partial")
    if tmp.exists():
        tmp.unlink()

    try:
        with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zf:
            for i, (rel, ap) in enumerate(members, 1):
                size = ap.stat().st_size
                digest = sha256_file(ap)
                zf.write(ap, rel)
                files.append({"rel_path": rel, "size": size, "sha256": digest})
                total += size
                if i % 250 == 0 or i == len(members):
                    print(f"    compressed {i}/{len(members)}")
            manifest = dict(meta)
            manifest.update({"file_count": len(files),
                             "total_bytes": total,
                             "files": files})
            zf.writestr("MANIFEST.json",
                        json.dumps(manifest, indent=1, ensure_ascii=False))
        os.replace(tmp, target)
    finally:
        if tmp.exists():
            tmp.unlink()
    return manifest


# --------------------------------------------------------------- verification

def verify_archive(target: Path, estate_root: Path | None,
                   repo_root: Path | None, check_sources: bool,
                   disk_members: list | None = None) -> dict:
    """Bidirectional verification.

    For every member: bytes streamed OUT of the zip must hash equal to the
    embedded pin, and (when check_sources) equal to a fresh re-read of the
    source on disk.  Set membership is cross-checked in all directions.
    """
    res = {"members": 0, "verified": 0, "mismatches": [],
           "strays": [], "omissions": [], "archive_sha256": None}

    res["archive_sha256"] = sha256_file(target)

    with zipfile.ZipFile(target, "r") as zf:
        bad = zf.testzip()
        if bad is not None:
            res["mismatches"].append({"rel_path": bad, "why": "CRC failure"})

        manifest = json.loads(zf.read("MANIFEST.json"))
        pinned = {f["rel_path"]: f for f in manifest["files"]}
        in_zip = {n for n in zf.namelist() if n != "MANIFEST.json"}

        res["members"] = len(pinned)
        res["strays"] = sorted(in_zip - set(pinned))
        res["omissions"] = sorted(set(pinned) - in_zip)

        for i, (rel, pin) in enumerate(sorted(pinned.items()), 1):
            if rel not in in_zip:
                continue
            zsha, zlen = sha256_zip_member(zf, rel)
            row = {"rel_path": rel}
            ok = True
            if zsha != pin["sha256"]:
                row["why"] = "zip content != embedded pin"
                ok = False
            elif zlen != pin["size"]:
                row["why"] = f"zip length {zlen} != pinned size {pin['size']}"
                ok = False
            elif check_sources and estate_root is not None:
                src = resolve_member(rel, estate_root, repo_root)
                if not src.exists():
                    row["why"] = "source missing on disk"
                    ok = False
                elif sha256_file(src) != pin["sha256"]:
                    row["why"] = "source on disk != embedded pin"
                    ok = False
            if ok:
                res["verified"] += 1
            else:
                res["mismatches"].append(row)
            if i % 250 == 0 or i == len(pinned):
                print(f"    verified {i}/{len(pinned)}")

        # disk -> zip direction: nothing on disk may be absent from the archive.
        # disk_members lets a caller that built its own member list (--workflow)
        # supply it, instead of re-deriving an estate-shaped one.
        if check_sources and estate_root is not None:
            if disk_members is not None:
                disk = {rel for rel, _ in disk_members}
            elif repo_root is not None:
                disk = {rel for rel, _ in estate_members(estate_root)}
            else:
                disk = set()
            res["omissions"] += sorted(disk - set(pinned))

    res["manifest"] = manifest
    return res


# --------------------------------------------------------------- fixtures

class Fixtures:
    def __init__(self):
        self.rows = []

    def record(self, fid, passed, detail):
        self.rows.append((fid, bool(passed), detail))
        print(f"  {'PASS' if passed else 'FAIL'} {fid} - {detail}")

    def na(self, fid, why):
        self.rows.append((fid, True, f"n/a - {why}"))
        print(f"  N/A  {fid} - {why}")

    @property
    def ok(self):
        return all(p for _, p, _ in self.rows)


def fk2_completeness(fx: Fixtures, estate_root: Path) -> None:
    census = json.loads((REPO / "census.json").read_text(encoding="utf-8"))
    kl, fu = census.get("klines", []), census.get("funding", [])
    missing = []
    for entry in kl + fu:
        # census paths are RELATIVE -- resolve them through the estate root
        if not (estate_root / entry["path"]).exists():
            missing.append(entry["path"])
    ok = (len(kl) == 60 and len(fu) == 10 and not missing)
    detail = f"census {len(kl)}/60 klines, {len(fu)}/10 funding; {len(missing)} unresolved"
    if missing:
        detail += f" (first: {missing[0]})"
    fx.record("F-K2", ok, detail)


def _porcelain_minus_outputs(text: str, outputs: list) -> list:
    """Porcelain lines with THIS RUN'S OWN outputs removed.

    F-K3 asks "were the sources touched?".  It answered that by comparing raw
    `git status` before and after, which works only while every output lands
    outside the repo -- true for --estate and --workflow, whose destination is
    the Drive.  It is NOT true for --phase, which writes into
    research_outputs/_archive/.  There the .zip is ignored by *.zip but the
    .sha256 sidecar is not, so the run creates a new untracked entry and then
    asserts nothing changed.  F-K3 failed on the first live --phase run
    (2026-08-02, tc5) for exactly that reason -- and because releasing sources
    is gated on fx.ok, --delete-source could never have fired either.

    Two forms are dropped, and only these two: a line naming an output exactly,
    and a collapsed directory entry (git prints `?? dir/` rather than listing a
    wholly-untracked directory's contents) that CONTAINS an output.  Everything
    the run did not write stays in the comparison and still fails the fixture.
    """
    kept = []
    for line in text.splitlines():
        if len(line) <= 3:
            continue
        path = line[3:].strip().strip('"')
        if path in outputs:
            continue
        if path.endswith("/") and any(o.startswith(path) for o in outputs):
            continue
        kept.append(line)
    return kept


def fk3_source_untouched(fx: Fixtures, sample: list, before_status: str,
                         outputs: list | None = None) -> None:
    changed = [rel for rel, ap, pre in sample
               if not ap.exists() or sha256_file(ap) != pre]
    after_status = git_porcelain()
    outputs = outputs or []
    before = _porcelain_minus_outputs(before_status, outputs)
    after = _porcelain_minus_outputs(after_status, outputs)
    same = (before == after)
    detail = (f"{len(sample)}-file sha sample unchanged: {not changed}; "
              f"git porcelain identical: {same}")
    if outputs and after_status != before_status:
        detail += f" (this run's own {len(outputs)} output path(s) normalised out)"
    fx.record("F-K3", (not changed) and same, detail)


def fk4_restore_rehearsal(fx: Fixtures, target: Path, limit: int = 10) -> None:
    tmp = None
    try:
        tmp = Path(tempfile.mkdtemp(prefix="naiad_restore_"))
        # the rehearsal must never land inside the repository
        assert not inside(tmp, str(REPO)), f"temp dir inside repo: {tmp}"
        with zipfile.ZipFile(target, "r") as zf:
            manifest = json.loads(zf.read("MANIFEST.json"))
            pick = manifest["files"][:limit]
            bad = []
            for f in pick:
                zf.extract(f["rel_path"], tmp)
                out = tmp / f["rel_path"]
                if sha256_file(out) != f["sha256"]:
                    bad.append(f["rel_path"])
        fx.record("F-K4", not bad,
                  f"{len(pick)} members restored to {tmp.parent}\\... outside repo; "
                  f"{len(bad)} hash mismatches")
    except Exception as exc:                       # noqa: BLE001
        fx.record("F-K4", False, f"rehearsal raised: {exc}")
    finally:
        if tmp and tmp.exists():
            shutil.rmtree(tmp, ignore_errors=True)


def fk5_destination_verification(fx: Fixtures, target: Path,
                                 expect_sha: str, sidecar: Path) -> None:
    """Re-read the archive FROM the destination after writing."""
    try:
        fresh = sha256_file(target)
        with zipfile.ZipFile(target, "r") as zf:
            crc_bad = zf.testzip()
            n = len([x for x in zf.namelist() if x != "MANIFEST.json"])
        side = sidecar.read_text(encoding="utf-8").split()[0] if sidecar.exists() else ""
        ok = (fresh == expect_sha and crc_bad is None and side == expect_sha)
        fx.record("F-K5", ok,
                  f"re-read from destination: sha256 {fresh[:16]}... "
                  f"matches={fresh == expect_sha}, sidecar matches={side == expect_sha}, "
                  f"CRC clean={crc_bad is None}, {n} members")
    except Exception as exc:                       # noqa: BLE001
        fx.record("F-K5", False, f"destination re-read raised: {exc}")


def fk6_no_clobber(fx: Fixtures, target: Path) -> None:
    """F-K6, both paths (2026-08-03).

    The default path must still REFUSE, and the --force-same-day path must
    SIDESTEP without overwriting. Asserting only the refusal would let the new
    flag silently become a clobber.
    """
    # (a) default: refuses
    try:
        assert_no_clobber(target)
        fx.record("F-K6", False, "no-clobber guard did NOT trip on an existing target")
        return
    except SystemExit:
        pass

    # (b) --force-same-day on a file written TODAY: takes a -NN suffix
    try:
        alt = assert_no_clobber(target, force_same_day=True)
    except SystemExit:
        fx.record("F-K6", False,
                  "--force-same-day refused a same-day target instead of suffixing")
        return

    ok = (alt != target and not alt.exists() and target.exists()
          and alt.name.startswith(target.stem) and alt.suffix == target.suffix)
    fx.record("F-K6", ok,
              f"default refuses; --force-same-day yields {alt.name} while "
              f"{target.name} survives untouched"
              if ok else
              f"--force-same-day produced {alt} — expected a -NN sibling with "
              f"the original still present")

    # (c) an archive from an EARLIER day must refuse even with the flag
    old = target.with_name(f"_fk6_probe_{target.name}")
    try:
        old.write_bytes(b"probe")
        stale = datetime.now().timestamp() - 86_400 * 3
        os.utime(old, (stale, stale))
        try:
            assert_no_clobber(old, force_same_day=True)
            fx.record("F-K6b", False,
                      "--force-same-day overrode an archive from an EARLIER day")
        except SystemExit:
            fx.record("F-K6b", True,
                      "--force-same-day correctly does NOT apply to an older archive")
    except OSError as exc:
        fx.record("F-K6b", False, f"could not stage the older-file probe: {exc}")
    finally:
        try:
            old.unlink()
        except OSError:
            pass


def fk7_tracked_preserved(fx: Fixtures, tracked: set) -> None:
    gone = [t for t in sorted(tracked) if not (REPO / t).exists()]
    detail = (f"{len(tracked) - len(gone)}/{len(tracked)} git-tracked source files "
              f"still present on disk; {len(gone)} missing")
    if gone:
        detail += " -- " + ", ".join(gone[:3])
    fx.record("F-K7", not gone, detail)


# --------------------------------------------------------------- retention

def retention_report(dest: Path) -> list:
    """Report the archive estate against the retention rule.  NEVER deletes.

    Rule, CORRECTED 2026-08-03.  Estate and workflow archives are GENERATIONS --
    successive full snapshots of the same thing -- so the newest
    KEEP_*_GENERATIONS are within the rule and older ones are listed as
    prunable.

    PHASE ARCHIVES ARE NEVER PRUNABLE.  Each holds a different phase's evidence,
    so an older one is not a superseded copy; it is the only copy.  They are
    reported under their own heading with no keep-count at all.

    Anything outside the generation rule is LISTED, with its size, so the
    operator can decide.  Nothing is removed, moved, or renamed.
    """
    lines = ["# RETENTION — archive estate vs the rule", ""]
    lines.append(f"Generated {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')} "
                 f"by `scripts/backup_estate.py`.")
    lines.append("")
    lines.append(f"**Rule:** keep the newest {KEEP_ESTATE_GENERATIONS} estate generations "
                 f"and the newest {KEEP_WORKFLOW_GENERATIONS} workflow generations. "
                 f"**Phase archives are permanent evidence and are never prunable.**")
    lines.append("**This report never deletes anything.** It names what falls outside "
                 "the generation rule; acting on it is the operator's call.")
    lines.append("")

    # D-0b, 2026-08-12.  The estate/workflow half of this report was UNGATED.
    #
    # Ruling O-4 gave the PHASE section three distinct states and forbade it
    # from ever saying "none found" when it could not look.  It left this half
    # alone -- so an unmounted drive made `dest.glob()` return an empty iterator
    # (an empty glob is not an OSError), and the report printed "- none found"
    # for four perfectly good archives sitting on an unplugged disk.  Same
    # conflation, same file, one function higher up.
    #
    # Resolved ONCE, not per section: two calls would pay the wait budget twice
    # for the same drive.  The -NN grouping and the same-day sort inversion are
    # O-5 and are deliberately NOT touched here -- this is a gate fix only.
    dest_mounted, dest_detail = drive_ready(dest, note=lambda *_a, **_k: None)

    def _generations(pattern, keep_n, title):
        """One dated-generation section, shared by estate and workflow."""
        out = [f"## {title}", "", f"Location: `{dest}`", ""]
        if not dest_mounted:
            return out + [
                f"**NOT ENUMERABLE — the destination drive is not reachable.** "
                f"({dest_detail})",
                "",
                "This is NOT the same as \"none found\", and this report will never say "
                "that when it could not look. Plug the drive, or point `--dest` / "
                f"`${BACKUP_DEST_ENV}` at a reachable directory, and re-run.",
            ]
        try:
            gens = sorted((p for p in dest.glob(pattern) if p.is_file()),
                          key=lambda p: p.name, reverse=True)
        except OSError as exc:
            return out + [f"- could not read the destination: {exc}"]
        if not gens:
            return out + ["- none found — the drive is reachable and holds no "
                          "matching archive"]
        keep, over = gens[:keep_n], gens[keep_n:]
        out.append(f"{len(gens)} generation(s) present; "
                   f"{len(keep)} within the rule, {len(over)} outside it.")
        out.append("")
        out.append("| generation | size (B) | within rule |")
        out.append("|---|---:|---|")
        for p in gens:
            out.append(f"| `{p.name}` | {p.stat().st_size:,} | "
                       f"{'yes' if p in keep else '**NO — outside the rule**'} |")
        if not over:
            out.append("")
            out.append(f"Nothing to consider: fewer than {keep_n + 1} generations exist.")
        return out

    lines += _generations("naiad_estate_*.zip", KEEP_ESTATE_GENERATIONS,
                          "Estate generations")
    lines.append("")
    lines += _generations("naiad_workflow_*.zip", KEEP_WORKFLOW_GENERATIONS,
                          "Workflow generations")

    # --- phase archives: PERMANENT ------------------------------------------
    #
    # RULING O-4, 2026-08-12.  Two defects fixed here, and the second is the
    # one that matters.
    #
    # (1) WRONG LOCATION.  This scanned `REPO/research_outputs/_archive`, which
    #     stopped holding archives on 2026-08-06 when ruling B moved them
    #     off-machine.  Only the SIDECARS stayed in the repo.  So the report
    #     printed "none found" while nine archives sat on the drive.  It now
    #     resolves the same root --phase writes to.
    #
    # (2) ABSENCE OF THE DRIVE IS NOT ABSENCE OF THE ARCHIVES.  Three states are
    #     now distinct, and the third must NEVER print "none found":
    #       drive mounted + archives  -> enumerate them
    #       drive mounted + no zips   -> "none found"
    #       drive NOT mounted         -> "NOT ENUMERABLE"
    #     Collapsing the third into the second is the exact conflation that
    #     produced the 2026-08-04 retraction: a single lookup returning nothing
    #     was read as a measurement of absence.  To claim a thing does not
    #     exist, you must have been able to look.
    #
    # When the drive is absent the report falls back to the TRACKED SIDECARS in
    # the repo, which are the standing proof of which archives exist and what
    # they hashed to.  That is precisely why ruling B kept them in-repo.
    # v2, 2026-08-15.  `arch` is now the LOCAL _archive and is ALWAYS present,
    # so the NOT-ENUMERABLE branch below has become the rare case rather than
    # the normal one -- but it is kept in full, because an operator can still
    # point $NAIAD_PHASE_ARCHIVE_ROOT at an external volume, and the reasoning
    # in ruling O-4 (absence of the drive is not absence of the archives) is
    # exactly as true then as it was in 2026-08.
    arch = phase_archive_root_path()
    anchor = volume_anchor(arch)
    # D-0b: waits for a sleeping disk before declaring it absent.  note=lambda
    # discards the WOKE line -- this function returns report lines and must not
    # print into the middle of a caller's output.
    drive_mounted, _ = drive_ready(arch, note=lambda *_a, **_k: None)

    lines.append("")
    lines.append("## PHASE ARCHIVES — PERMANENT EVIDENCE, NEVER PRUNE")
    lines.append("")
    lines.append("Each phase archive holds a DIFFERENT phase's evidence, so an older "
                 "one is not a superseded copy of a newer one — it is the only copy "
                 "of work that will never be produced again.")
    lines.append("")
    lines.append(f"Location: `{arch}`")
    lines.append("")

    if not drive_mounted:
        lines.append(f"**NOT ENUMERABLE — the drive `{anchor}` is not mounted.**")
        lines.append("")
        lines.append("This is NOT the same as \"none found\", and this report will never say "
                     "that when it could not look. The archives are off-machine by ruling B "
                     "(2026-08-06); plug the drive, or set "
                     f"`${PHASE_ARCHIVE_ROOT_ENV}`, and re-run to enumerate them.")
        sidecars = sorted((REPO / PHASE_SIDECAR_DIR).glob("*.sha256"))
        lines.append("")
        if sidecars:
            lines.append(f"**{len(sidecars)} tracked sidecar(s) in `{PHASE_SIDECAR_DIR}/` record "
                         "which archives exist and what they hashed to** — this is the "
                         "standing proof that survives an unplugged drive:")
            lines.append("")
            lines.append("| sidecar | recorded sha256 |")
            lines.append("|---|---|")
            for s in sidecars:
                try:
                    rec = next((t for t in s.read_text(encoding="utf-8").replace("*", " ").split()
                                if len(t) == 64), "unreadable")
                except OSError as exc:
                    rec = f"unreadable: {exc}"
                lines.append(f"| `{s.name}` | `{rec}` |")
        else:
            lines.append(f"No sidecars in `{PHASE_SIDECAR_DIR}/` either — "
                         "the archive set cannot be described from this clone.")
        return lines

    if not arch.is_dir():
        lines.append(f"- none found — the drive is mounted but `{arch}` does not exist, "
                     "so no phase archive has been written there yet")
        return lines

    phases = sorted((p for p in arch.glob("*.zip") if p.is_file()),
                    key=lambda p: p.name)
    # ZIP RESIDENCY, 2026-08-15.  The local _archive is the CURRENT-CYCLE set.
    # An empty one is the NORMAL state immediately after an aging pass, so this
    # branch must not read like a finding.  It used to say "none found", which
    # is the same sentence this report prints when something is wrong, and a
    # scan that cries wolf is a scan an operator learns to ignore.
    if not phases:
        lines.append("**CURRENT CYCLE EMPTY — this is BY DESIGN and is NOT a finding.**")
        lines.append("")
        lines.append("Under the zip-residency ruling (operator, 2026-08-15) *new zips are "
                     "born local and older zips live on the LaCie*. An empty local "
                     "`_archive` means every archive written so far has been aged out to "
                     "the backup volume — which is the intended end state of a cycle, not "
                     "a missing archive. The tracked sidecars below are the standing "
                     "fingerprint set and are always present; the aged-out archives are "
                     "enumerated further down when the volume is reachable.")
    else:
        total = sum(p.stat().st_size for p in phases)
        lines.append(f"**CURRENT CYCLE:** {len(phases)} archive(s) born local, {total:,} B "
                     f"({total / 1e6:,.1f} MB). **All permanent. None prunable.**")
        lines.append("")
        lines.append("| archive | date | size (B) | status |")
        lines.append("|---|---|---:|---|")
        for p in phases:
            m = DATED_ZIP.search(p.name)
            lines.append(f"| `{p.name}` | {m.group(1) if m else 'undated'} | "
                         f"{p.stat().st_size:,} | **PERMANENT — never prune** |")
        lines.append("")
        lines.append("There is no keep-count for phase archives and no circumstance "
                     "under which this report will list one as prunable.")

    # --- the FINGERPRINT SET.  Always printed, in every branch, because it is
    # the one part of this report that does not depend on any volume being
    # mounted or any zip still being local: the sidecars are tracked in git.
    sidecars = sorted((REPO / PHASE_SIDECAR_DIR).glob("*.sha256"))
    lines.append("")
    if sidecars:
        lines.append(f"**FINGERPRINT SET: {len(sidecars)} tracked sidecar(s) in "
                     f"`{PHASE_SIDECAR_DIR}/`.** These are committed, so they describe the "
                     "archive set from any clone, with no volume attached and no zip "
                     "present locally.")
    else:
        lines.append(f"**FINGERPRINT SET: none.** No sidecars in `{PHASE_SIDECAR_DIR}/` — "
                     "the archive set cannot be described from this clone. THIS one *is* "
                     "a finding.")

    # --- the AGED-OUT archives on the LaCie.  Same three-state discipline as
    # ruling O-4: enumerated, reachable-but-empty, or NOT ENUMERABLE.  Never a
    # count this run did not actually take.
    aged = phase_archive_aged_path()
    aged_anchor = volume_anchor(aged)
    aged_reachable, aged_detail = drive_ready(aged, note=lambda *_a, **_k: None)
    lines.append("")
    lines.append(f"Aged-out archives: `{aged}`")
    if not aged_reachable:
        lines.append(f"- **[backup] NOT ENUMERABLE — `{aged_anchor}` is not mounted** "
                     f"({aged_detail}). This is NOT \"no archives exist\"; it is \"this run "
                     "could not look\". The fingerprint set above is what stands.")
    elif not aged.is_dir():
        lines.append(f"- **[backup] volume mounted, `{aged}` does not exist** — nothing has "
                     "been aged out to it yet.")
    else:
        azips = sorted(p for p in aged.glob("*.zip") if p.is_file())
        atotal = sum(p.stat().st_size for p in azips)
        lines.append(f"- **[backup] {len(azips)} archive(s), {atotal:,} B "
                     f"({atotal / 1e6:,.1f} MB)** on `{aged_anchor}`.")
        names = {s.name[:-len(".sha256")] for s in sidecars}
        gap = sorted(names - {p.name for p in azips})
        if gap:
            lines.append(f"- **{len(gap)} fingerprinted archive(s) NOT on the volume: "
                         f"{', '.join(f'`{g}`' for g in gap)}** — a sidecar exists but "
                         "neither a local nor an aged-out copy was found. THIS is a finding.")

    # --- the BACKUP copy on the external volume (v2, 2026-08-15) -------------
    #
    # Under v2 the enumeration above is of the LOCAL working copies, which are
    # always present.  That makes it easy to read this report as "the archives
    # are safe" when what it has actually shown is "the archives are HERE" --
    # one copy, on one machine.  So the backup volume is reported too, and the
    # same three-state discipline from ruling O-4 applies to it: reachable and
    # holding archives, reachable and empty, or NOT ENUMERABLE.  It must never
    # print a count it could not take.
    bdest = Path(os.environ.get(BACKUP_DEST_ENV) or BACKUP_DEST_DEFAULT)
    bphases = bdest / "phases"
    banchor = volume_anchor(bdest)
    breachable, bdetail = drive_ready(bdest, note=lambda *_a, **_k: None)
    lines.append("")
    lines.append(f"Backup copy: `{bphases}`")
    if not breachable:
        lines.append(f"- **[backup] NOT ENUMERABLE — `{banchor}` is not mounted** "
                     f"({bdetail}). This is NOT \"no backup exists\"; it is "
                     "\"this run could not look\". The tracked sidecars in "
                     f"`{PHASE_SIDECAR_DIR}/` remain the standing proof of what "
                     "the archive set is.")
    elif not bphases.is_dir():
        lines.append(f"- **[backup] volume mounted, `{bphases}` does not exist** — "
                     "the phase archives have never been mirrored there.")
    else:
        bzips = sorted(p for p in bphases.glob("*.zip") if p.is_file())
        btotal = sum(p.stat().st_size for p in bzips)
        lines.append(f"- **[backup] {len(bzips)} archive(s), {btotal:,} B** on "
                     f"`{banchor}`.")
        local_names = {p.name for p in phases}
        missing = sorted(local_names - {p.name for p in bzips})
        if missing:
            lines.append(f"- **[backup] {len(missing)} local archive(s) NOT mirrored: "
                         f"{', '.join(missing)}** — run `--phase <name> --mirror`.")
    return lines


def publish_step(args=None) -> dict:
    """Final PUBLISH step (gate A-6a).  Stages exchange/** only; fails closed.

    A tripped guard is printed as a FLAG line and returned to the caller, which
    turns it into a non-zero exit code -- an unattended Sunday-morning run must
    surface this as a failed task, not as a line in a log nobody opens.

    The D3 size budget can refuse for a second, independent reason; REFUSED is
    treated exactly like FLAGGED by every caller.
    """
    date_str = datetime.now().strftime("%Y-%m-%d")
    allow = True if getattr(args, "allow_oversize_publish", False) else None
    print("\nPUBLISH")
    pub = publish_exchange.publish(REPO, date_str, log=lambda m: print(f"  {m}"),
                                   allow_oversize=allow)
    if pub["status"] == "FLAGGED":
        print("  FLAG: nothing pushed. Resolve the staged paths by hand, then re-run.")
    if pub["status"] == "REFUSED":
        print("  REFUSE: nothing pushed. Move data out of exchange/ per §4.2, or "
              "re-run with --allow-oversize-publish if this publish is legitimate.")
    return pub


def emit_retention(dest: Path) -> None:
    """Print the retention report and publish it to exchange/status/."""
    lines = retention_report(dest)
    print("\nRETENTION REPORT (report only -- nothing is ever deleted)")
    for line in lines[4:]:                      # skip the markdown title block
        if line.strip():
            print(f"  {line}")
    try:
        out = REPO / "exchange" / "status" / "RETENTION.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"\nwrote {out.relative_to(REPO).as_posix()}")
    except OSError as exc:
        print(f"\ncould not write the retention report: {exc}")


# --------------------------------------------------------------- modes

def run_estate(dest: Path, args) -> int:
    env = assert_environment(dest, need_writable=True)
    from engine.data import cache_dir            # noqa: PLC0415 - Mode A only
    estate_root = cache_dir()

    override = os.environ.get("NAIAD_CACHE_DIR")
    date = datetime.now().strftime("%Y-%m-%d")
    target = dest / f"naiad_estate_{date}.zip"
    sidecar = target.with_suffix(".zip.sha256")
    force_sd = bool(getattr(args, "force_same_day", False))
    target = assert_no_clobber(target, force_sd)
    sidecar = assert_no_clobber(target.with_suffix(".zip.sha256"), force_sd)

    print(f"estate root      : {estate_root}")
    print(f"NAIAD_CACHE_DIR  : {override or '(unset)'}")
    print(f"inside OneDrive  : {inside(estate_root, env['onedrive_root'])}")
    print(f"destination      : {target}")

    members = estate_members(estate_root)
    print(f"members to archive: {len(members)}")

    before_status = git_porcelain()
    sample = [(rel, ap, sha256_file(ap)) for rel, ap in members[:20]]
    tracked = {"census.json", "DATA_CENSUS.md",
               "research_outputs/census/build_manifest.json"}

    meta = {
        "created_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "mode": "estate",
        "estate_root": str(estate_root),
        "repo_root": str(REPO),
        "naiad_cache_dir_override": override,
        "inside_onedrive": inside(estate_root, env["onedrive_root"]),
        "repo_head": env["head"],
    }

    print("  compressing...")
    manifest = build_archive(members, target, meta)
    archive_sha = sha256_file(target)
    sidecar.write_text(f"{archive_sha}  {target.name}\n", encoding="utf-8")

    print("  verifying (bidirectional)...")
    res = verify_archive(target, estate_root, REPO, check_sources=True)

    print("\nFIXTURES")
    fx = Fixtures()
    fx.record("F-K1",
              not res["mismatches"] and not res["strays"] and not res["omissions"]
              and res["verified"] == res["members"],
              f"{res['verified']}/{res['members']} members verified both directions; "
              f"{len(res['mismatches'])} mismatches, {len(res['strays'])} strays, "
              f"{len(res['omissions'])} omissions")
    fk2_completeness(fx, estate_root)
    fk3_source_untouched(fx, sample, before_status)
    fk4_restore_rehearsal(fx, target)
    fk5_destination_verification(fx, target, archive_sha, sidecar)
    fk6_no_clobber(fx, target)
    fk7_tracked_preserved(fx, tracked)

    print(f"\narchive   : {target}")
    print(f"size      : {target.stat().st_size:,} B "
          f"({target.stat().st_size / 1048576:.1f} MB, "
          f"{100 * target.stat().st_size / max(manifest['total_bytes'], 1):.1f}% of source)")
    print(f"sha256    : {archive_sha}")
    print(f"members   : {manifest['file_count']}")
    print(f"source    : {manifest['total_bytes']:,} B")
    print(f"sidecar   : {sidecar}")
    print(f"\n{sum(1 for _, p, _ in fx.rows if p)}/{len(fx.rows)} fixtures pass")

    emit_retention(dest)
    pub = publish_step(args)
    if pub["status"] in ("FLAGGED", "REFUSED", "ERROR"):
        return 1
    return 0 if fx.ok else 1


def run_workflow(dest: Path, args) -> int:
    """Archive the project's THINKING -- dated and hashed exactly like --estate.

    The estate backup protects irreplaceable PRICE data.  This protects the
    irreplaceable everything-else: memory, knowledge, skills, contracts, lane
    status, the exchange.  Same archive shape, same embedded manifest, same
    bidirectional verification, same no-clobber guard -- because the failure
    modes are identical and the estate mode's answers to them are already
    proven.
    """
    env = assert_environment(dest, need_writable=True)
    roots, missing, nested = workflow_roots()

    date = datetime.now().strftime("%Y-%m-%d")
    target = dest / f"naiad_workflow_{date}.zip"
    sidecar = target.with_suffix(".zip.sha256")
    force_sd = bool(getattr(args, "force_same_day", False))
    target = assert_no_clobber(target, force_sd)
    sidecar = assert_no_clobber(target.with_suffix(".zip.sha256"), force_sd)

    print(f"repo root        : {REPO}")
    print(f"destination      : {target}")
    print(f"roots archived   : {len(roots)} dir(s) + repo-root {', '.join(WORKFLOW_ROOT_GLOBS)}")
    for rel in roots:
        n = sum(1 for r, _ in walk_members(REPO / rel, prefix=rel + "/")
                if not _workflow_excluded(r))
        print(f"    {rel:<34} {n} file(s)")
    print(f"    {'(repo root) ' + ' '.join(WORKFLOW_ROOT_GLOBS):<34} "
          f"{len(workflow_root_files())} file(s)")
    if nested:
        for rel, parent in nested:
            print(f"    SKIPPED (nested) : {rel} -- already inside {parent}")
    if missing:
        for rel in missing:
            print(f"    absent           : {rel}")

    members = workflow_members(roots)
    if not members:
        sys.stderr.write("no workflow sources present -- refusing to write an empty archive\n")
        raise SystemExit(2)
    print(f"members to archive: {len(members)}")

    before_status = git_porcelain()
    sample = [(rel, ap, sha256_file(ap)) for rel, ap in members[:20]]
    tracked = set()
    for rel in roots:
        tracked |= {t for t in git_tracked_under(rel) if not _workflow_excluded(t)}
    root_names = {rel for rel, _ in workflow_root_files()}
    tracked |= {t for t in git_tracked_under(".") if t in root_names}

    meta = {
        "created_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "mode": "workflow",
        "roots": list(roots),
        "root_globs": list(WORKFLOW_ROOT_GLOBS),
        "excluded": list(WORKFLOW_EXCLUDE_PARTS) + list(WORKFLOW_EXCLUDE_SUFFIXES),
        "roots_absent": list(missing),
        "roots_skipped_nested": [r for r, _ in nested],
        "estate_root": str(REPO),
        "repo_root": str(REPO),
        "naiad_cache_dir_override": os.environ.get("NAIAD_CACHE_DIR"),
        "inside_onedrive": inside(REPO, env["onedrive_root"]),
        "repo_head": env["head"],
    }

    print("  compressing...")
    manifest = build_archive(members, target, meta)
    archive_sha = sha256_file(target)
    sidecar.write_text(f"{archive_sha}  {target.name}\n", encoding="utf-8")

    print("  verifying (bidirectional)...")
    res = verify_archive(target, REPO, None, check_sources=True, disk_members=members)

    print("\nFIXTURES")
    fx = Fixtures()
    fx.record("F-K1",
              not res["mismatches"] and not res["strays"] and not res["omissions"]
              and res["verified"] == res["members"],
              f"{res['verified']}/{res['members']} members verified both directions; "
              f"{len(res['mismatches'])} mismatches, {len(res['strays'])} strays, "
              f"{len(res['omissions'])} omissions")
    fx.na("F-K2", "completeness vs census.json applies to --estate only")
    fk3_source_untouched(fx, sample, before_status)
    fk4_restore_rehearsal(fx, target)
    fk5_destination_verification(fx, target, archive_sha, sidecar)
    fk6_no_clobber(fx, target)
    fk7_tracked_preserved(fx, tracked)

    print(f"\narchive   : {target}")
    print(f"size      : {target.stat().st_size:,} B "
          f"({target.stat().st_size / 1048576:.1f} MB, "
          f"{100 * target.stat().st_size / max(manifest['total_bytes'], 1):.1f}% of source)")
    print(f"sha256    : {archive_sha}")
    print(f"members   : {manifest['file_count']}")
    print(f"source    : {manifest['total_bytes']:,} B")
    print(f"sidecar   : {sidecar}")
    print(f"\n{sum(1 for _, p, _ in fx.rows if p)}/{len(fx.rows)} fixtures pass")

    emit_retention(dest)
    pub = publish_step(args)
    if pub["status"] in ("FLAGGED", "REFUSED", "ERROR"):
        return 1
    return 0 if fx.ok else 1


def run_phase(name: str, args) -> int:
    src = REPO / "research_outputs" / name
    if not src.is_dir():
        sys.stderr.write(f"no such phase directory: {src}\n")
        return 2

    # Ruling B: the archive goes off-machine, the sidecar stays tracked in-repo.
    dest = phase_archive_root(args)
    env = assert_environment(dest, need_writable=True)
    sidecar_dir = REPO / PHASE_SIDECAR_DIR
    sidecar_dir.mkdir(parents=True, exist_ok=True)
    date = datetime.now().strftime("%Y-%m-%d")
    target = dest / f"{name}_{date}.zip"
    force_sd = bool(getattr(args, "force_same_day", False))
    target = assert_no_clobber(target, force_sd)
    # the sidecar follows whatever name the archive actually took (-NN and all)
    sidecar = assert_no_clobber(sidecar_dir / f"{target.stem}.zip.sha256", force_sd)

    rel_dir = f"research_outputs/{name}"
    tracked = git_tracked_under(rel_dir)
    members = walk_members(src)
    print(f"phase      : {name}")
    print(f"source     : {src}")
    print(f"archive to : {target}        (off-machine, ruling B)")
    print(f"sidecar to : {sidecar}   (in-repo, tracked)")
    print(f"members    : {len(members)}  (git-tracked among them: {len(tracked)})")

    before_status = git_porcelain()
    sample = [(rel, ap, sha256_file(ap)) for rel, ap in members[:20]]

    meta = {
        "created_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "mode": "phase",
        "phase": name,
        "estate_root": str(src),
        "repo_root": str(REPO),
        "naiad_cache_dir_override": os.environ.get("NAIAD_CACHE_DIR"),
        "inside_onedrive": inside(src, env["onedrive_root"]),
        "repo_head": env["head"],
    }

    print("  compressing...")
    manifest = build_archive(members, target, meta)
    archive_sha = sha256_file(target)
    sidecar.write_text(f"{archive_sha}  {target.name}\n", encoding="utf-8")

    print("  verifying (bidirectional)...")
    res = verify_archive(target, src, None, check_sources=True)

    print("\nFIXTURES")
    fx = Fixtures()
    clean = (not res["mismatches"] and not res["strays"]
             and not res["omissions"] and res["verified"] == res["members"])
    fx.record("F-K1", clean,
              f"{res['verified']}/{res['members']} members verified both directions; "
              f"{len(res['mismatches'])} mismatches, {len(res['strays'])} strays, "
              f"{len(res['omissions'])} omissions")
    fx.na("F-K2", "completeness vs census.json applies to --estate only")
    # F-K3 must be told which paths are this run's own output (see
    # _porcelain_minus_outputs).  Since ruling B the archive lands OUTSIDE the
    # repo and cannot appear in porcelain at all, so only in-repo outputs are
    # normalised out -- and the membership test is `inside`, not an assumption.
    outputs = [p.relative_to(REPO).as_posix()
               for p in (target, sidecar) if inside(p, str(REPO))]
    fk3_source_untouched(fx, sample, before_status, outputs=outputs)
    fk4_restore_rehearsal(fx, target)
    fk5_destination_verification(fx, target, archive_sha, sidecar)
    fk6_no_clobber(fx, target)
    fk7_tracked_preserved(fx, tracked)

    # D1: the mirror runs only AFTER F-K5 has passed -- there is no point
    # copying an archive that has not yet proved it verifies at its source.
    mirror = getattr(args, "mirror", None)
    if mirror:
        fk5_ok = next((p for fid, p, _ in fx.rows if fid == "F-K5"), False)
        if not fk5_ok:
            fx.record("F-M1", False,
                      "F-K5 did not pass -- mirror skipped, nothing copied")
        else:
            mirror_phase_outputs(fx, target, sidecar, Path(mirror), archive_sha)

    releasable = [rel for rel, _ in members if f"{rel_dir}/{rel}" not in tracked]
    if not fx.ok:
        print("\nfixtures failed -- source kept, nothing released")
    elif args.delete_source:
        if not clean:
            print("\nmismatches present -- source kept, run aborted")
            return 1
        freed = 0
        for rel, ap in members:
            if f"{rel_dir}/{rel}" in tracked:
                continue
            freed += ap.stat().st_size
            ap.unlink()
        print(f"\nreleased {len(releasable)} untracked files, {freed:,} B; "
              f"{len(tracked)} tracked files preserved in place")
    else:
        print(f"\n--delete-source not given: source kept intact. "
              f"{len(releasable)} untracked files ({len(members) - len(releasable)} tracked) "
              f"would be releasable.")

    print(f"\narchive   : {target}")
    print(f"size      : {target.stat().st_size:,} B")
    print(f"sha256    : {archive_sha}")
    print(f"members   : {manifest['file_count']}")
    print(f"\n{sum(1 for _, p, _ in fx.rows if p)}/{len(fx.rows)} fixtures pass")

    pub = publish_step(args)
    if pub["status"] in ("FLAGGED", "REFUSED", "ERROR"):
        return 1
    return 0 if fx.ok else 1


def run_verify(path: Path) -> int:
    assert_environment(None, need_writable=False)
    if not path.is_file():
        sys.stderr.write(f"no such archive: {path}\n")
        return 2
    print(f"archive : {path}")
    res = verify_archive(path, None, None, check_sources=False)
    man = res["manifest"]
    print(f"\nmode         : {man.get('mode', '?')}"
          f"{'/' + man['phase'] if man.get('phase') else ''}")
    print(f"created_utc  : {man.get('created_utc', '?')}")
    print(f"members      : {res['members']}")
    print(f"verified     : {res['verified']}")
    print(f"mismatches   : {len(res['mismatches'])}")
    print(f"strays       : {len(res['strays'])}")
    print(f"omissions    : {len(res['omissions'])}")
    print(f"archive sha256: {res['archive_sha256']}")
    for m in res["mismatches"][:10]:
        print(f"    MISMATCH {m['rel_path']}: {m.get('why')}")
    ok = not res["mismatches"] and not res["strays"] and not res["omissions"]
    print(f"\n{'VERIFIED' if ok else 'FAILED'}")
    return 0 if ok else 1


# --------------------------------------------------------------- cli

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--estate", action="store_true",
                   help="archive the price estate (default)")
    g.add_argument("--workflow", action="store_true",
                   help="archive the workflow estate (memory, knowledge, skills, "
                        "prompts, claude, exchange, primers, history, operator exports)")
    g.add_argument("--phase", metavar="NAME",
                   help="archive one research_outputs/<NAME> subtree")
    g.add_argument("--verify", metavar="ZIP",
                   help="verify an existing archive against its embedded manifest")
    ap.add_argument("--dest", metavar="DIR",
                    help=f"destination directory for --estate and --workflow "
                         f"(default ${BACKUP_DEST_ENV}, else {BACKUP_DEST_DEFAULT}; "
                         f"an explicit --dest always wins). An ERROR for --phase "
                         f"-- use --mirror.")
    ap.add_argument("--mirror", metavar="DIR",
                    help="--phase only: after F-K5 passes, copy the archive AND its "
                         "sidecar to DIR and verify by re-reading FROM DIR. Refuses "
                         "an existing destination file rather than overwriting.")
    ap.add_argument("--phase-archive-root", metavar="DIR",
                    help=f"--phase only: where the archive is written "
                         f"(default ${PHASE_ARCHIVE_ROOT_ENV}, else "
                         f"{PHASE_ARCHIVE_ROOT_DEFAULT}). The sidecar always stays "
                         f"tracked in {PHASE_SIDECAR_DIR}/.")
    ap.add_argument("--allow-oversize-publish", action="store_true",
                    help="override the publish size budget for this run (D3). "
                         "The override is announced on screen.")
    ap.add_argument("--delete-source", action="store_true",
                    help="--phase only: release untracked sources after zero mismatches")
    ap.add_argument("--force-same-day", action="store_true",
                    help="if the target exists AND was written TODAY, append -NN "
                         "instead of halting. Both files are kept; nothing is "
                         "overwritten. Does NOT apply to archives from an "
                         "earlier day, which still refuse.")
    args = ap.parse_args()

    # D2, queue 002.  --dest is defined on the top-level parser, so before this
    # `--phase X --dest "G:/..."` parsed cleanly, exited 0, printed success and
    # wrote inside the repo.  --estate and --workflow hard-fail when --dest is
    # missing; --phase was the one mode where the flag LIED.  It is now an error
    # that names the alternative, because a refusal with nothing to offer would
    # be worse than the no-op it replaces.
    if args.phase and args.dest:
        ap.error("--phase does not take --dest. The phase archive root is "
                 "configured with --phase-archive-root or $%s (default %s); "
                 "an additional off-machine copy is made with --mirror DIR."
                 % (PHASE_ARCHIVE_ROOT_ENV, PHASE_ARCHIVE_ROOT_DEFAULT))
    if args.mirror and not args.phase:
        ap.error("--mirror applies to --phase only; --estate and --workflow "
                 "write to --dest.")
    if args.phase_archive_root and not args.phase:
        ap.error("--phase-archive-root applies to --phase only.")

    if args.verify:
        return run_verify(Path(args.verify))
    if args.phase:
        return run_phase(args.phase, args)
    # Amendment 2026-08-12: both modes resolve their destination through
    # backup_dest_root(), which honours an explicit --dest first and HALTS on an
    # unmounted drive rather than falling back to the laptop.  The old
    # `ap.error("... requires --dest")` pair is gone: it did not make the backup
    # safer, it only made the destination invisible to the repository.
    if args.workflow:
        return run_workflow(backup_dest_root(args), args)
    return run_estate(backup_dest_root(args), args)


if __name__ == "__main__":
    sys.exit(main())
