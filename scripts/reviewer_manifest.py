#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""One-paste integrity manifest for the reviewer loop.  Version 1.1.

Contract: prompts/Reviewer_Manifest_Builder_Contract.md (OPS tier, Tier-0,
drafted and ratified 2026-07-26).  This is an ops artifact: not study evidence,
no G-7, no journal reads, no engine imports, no ledger scorecard.

v1.1 (2026-08-02, gate A-3 / A-3a -- the exchange migration).  Four changes,
each forced by the move of the published surface out of the git-ignored
_reviewer_box/ and into the auto-published exchange/:
  * BOX_DIR is now exchange/status.  The manifest is written to, and the box
    inventory taken over, exchange/status/ -- which is TRACKED, not ignored.
  * F-M1 is now a round-trip test (see fixture_m1); the self-hash it used to
    be is retained as a secondary assertion inside the same fixture.
  * F-M4's comparison normalises away the manifest's own output path.  The
    old fixture relied on the output being git-ignored, so writing it could
    not move porcelain.  That is no longer true and the fixture would fail on
    every run for a reason that is not a defect.  Everything else must still
    be byte-identical before and after; a touch anywhere else still fails.
  * The box is no longer a flattened COPY box, so the bare-name fallback in
    guess_source() is narrowed -- see that function.

Invariants (contract section 1):
  1. Read-only on the repo, with exactly one exception: the manifest itself,
     written to exchange/status/MANIFEST.json.  That path is git-TRACKED as of
     v1.1, so this run can and normally does move `git status` for that one
     path -- F-M4 accounts for it explicitly and for nothing else.  Fixture
     F-M2's test double writes a mutated copy into a SYSTEM temp directory --
     never the repo -- and removes it again; that is the only write outside
     the manifest, and the contract mandates it.
  2. All byte questions answered with hashlib.sha256 over binary reads.  No
     grep/sed/text pipelines for byte questions: msys tools strip CR (known
     hazard, recorded 2026-07-26).
  3. Git is queried with READ-ONLY commands, including but not limited to:
     rev-parse, status, cat-file, ls-files, log, and `git config --get`.  The
     enumeration is illustrative rather than exhaustive -- the binding property
     is that no command mutates repository state.  `git config --get` reads;
     `git log` reads.  Neither writes.  (This wording supersedes v1.0's closed
     four-command list, which `git config --get` already had to be excused
     from by a footnote; the footnote is now the rule.)
  4. Standard library only.  Engine modules are never imported.

Field semantics, so a record cannot be misread:

  manifest_version  "1.1" -- bump when field semantics change

  sources[]
    path              repo-relative, POSIX separators
    tracked           path appears in `git ls-files`
    size              worktree byte count
    sha256_worktree   sha256 of the worktree bytes
    sha256_head_blob  sha256 of the raw bytes of `git cat-file blob HEAD:<path>`
                      (null when the path is absent from HEAD)
    match_head        worktree bytes == HEAD blob bytes
    a missing file collapses to {path, present: false} and nothing else

  reviewer_box[]      KEY NAME RETAINED DELIBERATELY.  It now inventories
                      exchange/status/, not _reviewer_box/.  The name is kept
                      because daily_routine.py compares today's manifest to
                      archived ones by this key; renaming it would make every
                      historical comparison read as a mass add/drop.
    path/size/sha256_worktree   describe the file as it sits in the box
    tracked           refers to the box path itself.  Under v1.1 this is
                      normally TRUE once the exchange is committed -- the
                      opposite of v1.0, where it was false by design
    source_guess      repo path a FLATTENED name resolves to, else null.  Most
                      exchange/status files are native artifacts (lane ledgers,
                      CADENCE.md) that are copies of nothing, so null here is
                      the normal case and not a failure to resolve
    sha256_head_blob  HEAD blob of source_guess, not of the box path
    match_head        box copy == source_guess's HEAD blob, i.e. "is this
                      flattened copy still current?"  null source_guess yields
                      false, meaning "unanswerable", per hashes_match()

  onedrive_running    true/false -- is OneDrive.exe running right now?  null on
                      a non-Windows host or if the query itself failed.  The
                      repo lives inside the OneDrive tree, so a false here
                      means the working tree has no live cloud copy
  ledger_head         {present, title, size} for LEDGER.md -- the first line and
                      the byte count, enough to catch a truncation or a swap
  lane_last_commit    per message-prefix, the most recent commit carrying it:
                      {sha, subject, committed_utc} or null.  Answers "when did
                      this lane last land anything?" without reading a ledger
  queue_total         every non-README work order in exchange/queue/
  queue_unratified    of those, the ones with no usable RATIFIED stamp --
                      they may not be executed yet
  queue_ratified_unbuilt
                      ratified but not yet stamped BUILT -- the real backlog
  queue_open          KEPT as an alias of queue_ratified_unbuilt so older
                      readers do not break; see queue_counts() for why its
                      meaning changed on 2026-08-12

Run:  python scripts/reviewer_manifest.py
"""

import glob
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

# ------------------------------------------------------------------ EDIT HERE
# Contract section 2: "Initial SOURCES (edit in-script, comment says so)".
# Add or remove glob patterns and literal paths below; everything else adapts.
# A glob that matches nothing is reported as a present:false record naming the
# pattern, so a silent coverage hole is impossible.
# Keep scripts/reviewer_manifest.py: fixture F-M1 (self-hash) requires it.
SOURCE_PATTERNS = [
    "engine/*.py",
    "configs/*.yaml",
    "configs/tc5_*.json",
    "scripts/census_build.py",
    "scripts/census_analyze.py",
    "scripts/census1b_*.py",
    "scripts/s2b_decompose.py",
    "scripts/s3_*.py",
    "scripts/tc1_*.py",
    "scripts/tc5_*.py",
    "scripts/reviewer_manifest.py",          # F-M1 self-hash target
    "scripts/daily_brief.py",
    "scripts/brief_lookup.py",
    "LEDGER.md",
    "DATA_CENSUS.md",
    "census.json",
    "research_outputs/census/build_manifest.json",
]
# ----------------------------------------------------------------------------

SELF_REL = "scripts/reviewer_manifest.py"
BOX_DIR = "exchange/status"          # v1.1: was _reviewer_box (gate A-3a)
MANIFEST_NAME = "MANIFEST.json"
OUT_REL = BOX_DIR + "/" + MANIFEST_NAME
QUEUE_DIR = "exchange/queue"
MANIFEST_VERSION = "1.1"

# Commit-message prefixes that identify a lane's work.  Order is the report
# order; a prefix that never appears records null rather than being omitted, so
# a lane that has never landed anything is visible as such.
LANE_PREFIXES = ("ops:", "brief:", "docs:", "exchange:", "study-phase")

# Contract section 2's three named flattening rules, applied first and literally.
FLATTEN_RULES = (
    ("engine_", "engine/"),
    ("configs_", "configs/"),
    ("scripts_", "scripts/"),
)


# --------------------------------------------------------------- git plumbing

def git(args, check=True):
    """Read-only git query.  Returns (returncode, stdout_bytes).

    stdout is kept as BYTES: blob content must never round-trip through a text
    decoder (invariant 2).
    """
    proc = subprocess.run(
        ["git"] + args,
        cwd=REPO_ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if check and proc.returncode != 0:
        raise RuntimeError("git %s failed: %s" % (
            " ".join(args), proc.stderr.decode("utf-8", "replace").strip()))
    return proc.returncode, proc.stdout


def git_text(args, check=True):
    rc, out = git(args, check=check)
    return rc, out.decode("utf-8", "replace")


def repo_root():
    proc = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        sys.stderr.write("not inside a git work tree\n")
        raise SystemExit(2)
    return os.path.realpath(proc.stdout.decode("utf-8", "replace").strip())


# -------------------------------------------------------------------- hashing

def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha256_path(abs_path):
    """sha256 over a binary read -- never a text read (invariant 2)."""
    digest = hashlib.sha256()
    with open(abs_path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def hashes_match(left, right):
    """The single comparison helper; F-M2 proves it can return False.

    A None on either side means "cannot compare" and yields False -- an
    unanswerable question is never reported as agreement.
    """
    if left is None or right is None:
        return False
    return left == right


def head_blob_sha256(rel):
    """sha256 of the raw bytes of HEAD:<rel>, or None if absent from HEAD."""
    if not rel:
        return None
    rc, blob = git(["cat-file", "blob", "HEAD:" + rel], check=False)
    if rc != 0:
        return None
    return sha256_bytes(blob)


# ---------------------------------------------------------------- inventories

def tracked_paths():
    rc, out = git(["ls-files", "-z"])
    return sorted(p for p in out.decode("utf-8", "replace").split("\0") if p)


def expand_sources():
    """SOURCE_PATTERNS -> ordered, de-duplicated repo-relative paths."""
    out = []
    for pattern in SOURCE_PATTERNS:
        if any(ch in pattern for ch in "*?["):
            hits = glob.glob(os.path.join(REPO_ROOT, pattern))
            matches = sorted(
                os.path.relpath(h, REPO_ROOT).replace(os.sep, "/")
                for h in hits if os.path.isfile(h))
            out.extend(matches if matches else [pattern])
        else:
            out.append(pattern)
    seen, unique = set(), []
    for path in out:
        if path not in seen:
            seen.add(path)
            unique.append(path)
    return unique


def source_record(rel, tracked_set):
    abs_path = os.path.join(REPO_ROOT, rel)
    if not os.path.isfile(abs_path):
        return {"path": rel, "present": False}
    worktree = sha256_path(abs_path)
    head_blob = head_blob_sha256(rel)
    return {
        "path": rel,
        "tracked": rel in tracked_set,
        "size": os.path.getsize(abs_path),
        "sha256_worktree": worktree,
        "sha256_head_blob": head_blob,
        "match_head": hashes_match(worktree, head_blob),
    }


def flatten_index(tracked):
    """tracked path with '/' -> '_' mapped back to the tracked path."""
    index = {}
    for rel in tracked:
        index.setdefault(rel.replace("/", "_"), []).append(rel)
    return index


def guess_source(name, tracked_set, index):
    """Resolve a flattened box filename to its repo path.

    The three named rules run first and literally.  The fallback is a
    documented generalisation of them: a box name that is exactly some tracked
    path with '/' replaced by '_' resolves to that path.  It resolves nested
    copies (research_outputs_census_build_manifest.json) that the three rules
    alone leave unmatched.  An ambiguous name resolves to None -- never a coin
    flip.

    v1.1 NARROWING (gate A-3a).  The fallback now requires the resolved target
    to contain a '/', i.e. to be a genuinely FLATTENED nested path.  In v1.0 it
    also resolved bare root filenames, because _reviewer_box/ held flat COPIES
    of root files (census.json, DATA_CENSUS.md) and that was the right answer.
    exchange/status/ holds no copies -- it holds native artifacts -- and under
    the old rule its README.md resolved to the repo's own root README.md and
    reported match_head false: a copy-is-stale alarm about a file that is not a
    copy of anything.  Requiring a '/' in the target keeps every real flattened
    resolution and drops exactly that class of false positive.
    """
    for prefix, replacement in FLATTEN_RULES:
        if name.startswith(prefix):
            candidate = replacement + name[len(prefix):]
            if candidate in tracked_set:
                return candidate
    hits = [h for h in index.get(name, []) if "/" in h]
    return hits[0] if len(hits) == 1 else None


def box_records(tracked_set, index):
    box_abs = os.path.join(REPO_ROOT, BOX_DIR)
    if not os.path.isdir(box_abs):
        return []
    records = []
    for dirpath, dirnames, filenames in os.walk(box_abs):
        dirnames.sort()
        for name in sorted(filenames):
            if name == MANIFEST_NAME:
                continue
            abs_path = os.path.join(dirpath, name)
            rel = os.path.relpath(abs_path, REPO_ROOT).replace(os.sep, "/")
            worktree = sha256_path(abs_path)
            guess = guess_source(name, tracked_set, index)
            head_blob = head_blob_sha256(guess)
            records.append({
                "path": rel,
                "tracked": rel in tracked_set,
                "size": os.path.getsize(abs_path),
                "sha256_worktree": worktree,
                "source_guess": guess,
                "sha256_head_blob": head_blob,
                "match_head": hashes_match(worktree, head_blob),
            })
    return sorted(records, key=lambda r: r["path"])


def untracked_root():
    """Untracked files at repo root -- the `git clean` exposure inventory."""
    rc, out = git(["ls-files", "--others", "--exclude-standard", "-z"])
    names = sorted(
        p for p in out.decode("utf-8", "replace").split("\0")
        if p and "/" not in p)
    records = []
    for name in names:
        abs_path = os.path.join(REPO_ROOT, name)
        if os.path.isfile(abs_path):
            records.append({
                "name": name,
                "size": os.path.getsize(abs_path),
                "sha256": sha256_path(abs_path),
            })
    return records


def branch_state():
    """(branch, upstream, {ahead, behind}) from `git status --porcelain=v2`.

    porcelain=v2 --branch is used instead of rev-list so that every git call
    stays inside the read-only set named by invariant 3.
    """
    rc, text = git_text(["status", "--porcelain=v2", "--branch"])
    branch = upstream = ahead_behind = None
    for line in text.splitlines():
        if line.startswith("# branch.head "):
            branch = line.split(" ", 2)[2].strip()
        elif line.startswith("# branch.upstream "):
            upstream = line.split(" ", 2)[2].strip()
        elif line.startswith("# branch.ab "):
            parts = line.split()
            ahead_behind = {"ahead": int(parts[2]), "behind": abs(int(parts[3]))}
    if branch == "(detached)":
        branch = None
    return branch, upstream, ahead_behind


def eol_config():
    """Make byte-comparison validity self-documenting (contract section 2).

    NOTE_CONFIG: core.autocrlf is reachable only through `git config --get`.
    Under v1.0 that sat outside invariant 3's closed four-command list and was
    excused here by footnote.  v1.1 rewrote the invariant to say what it always
    meant -- read-only commands, "including but not limited to" -- so this is
    now ordinary compliance rather than a disclosed exception.  The note stays
    because the reasoning is worth keeping: parsing system/global/local config
    files by hand would be both fragile and less faithful to what git resolves.
    """
    rc, text = git_text(["config", "--get", "core.autocrlf"], check=False)
    autocrlf = text.strip() if rc == 0 and text.strip() else None

    attrs_abs = os.path.join(REPO_ROOT, ".gitattributes")
    present = os.path.isfile(attrs_abs)
    star_minus_text = False
    if present:
        with open(attrs_abs, "rb") as handle:        # bytes, not a text pipeline
            for raw in handle.read().split(b"\n"):
                tokens = raw.strip().split()
                if not tokens or tokens[0].startswith(b"#"):
                    continue
                if tokens[0] == b"*" and b"-text" in tokens[1:]:
                    star_minus_text = True
    return {
        "core_autocrlf": autocrlf,
        "gitattributes_present": present,
        "gitattributes_star_minus_text": star_minus_text,
        # worktree bytes are comparable to blob bytes when conversion is off
        "byte_comparison_valid": bool(
            star_minus_text or autocrlf in (None, "false", "input")),
    }


# ------------------------------------------------------------- v1.1 fields

def onedrive_running():
    """Is OneDrive.exe running right now?  None when unanswerable.

    The repo lives inside the OneDrive tree, so this is not trivia: a false
    means the working tree currently has no live cloud copy.  Process listing
    only -- no sync state, no error queue, and nothing is started or stopped.
    """
    if os.name != "nt":
        return None
    try:
        proc = subprocess.run(
            ["tasklist", "/FI", "IMAGENAME eq OneDrive.exe", "/NH"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except OSError:
        return None
    if proc.returncode != 0:
        return None
    return b"onedrive.exe" in proc.stdout.lower()


def ledger_head():
    """First line and byte size of LEDGER.md -- enough to catch a swap.

    A truncation or a wrong-file substitution changes one or both.  The full
    ledger is hashed as a SOURCE already; this is the cheap human-readable
    cross-check that sits next to it in the record.
    """
    abs_path = os.path.join(REPO_ROOT, "LEDGER.md")
    if not os.path.isfile(abs_path):
        return {"present": False, "title": None, "size": None}
    with open(abs_path, "rb") as handle:        # bytes, not a text pipeline
        first = handle.readline()
    return {
        "present": True,
        "title": first.decode("utf-8", "replace").rstrip("\r\n"),
        "size": os.path.getsize(abs_path),
    }


def lane_last_commit():
    """Most recent commit per message prefix -- "when did this lane last land?"

    Read-only `git log` (invariant 3).  A prefix that has never appeared records
    null rather than being dropped, so a silent lane is visible as a silent
    lane instead of as a missing key.
    """
    out = {p.rstrip(":"): None for p in LANE_PREFIXES}
    rc, text = git_text(["log", "--format=%H%x1f%cI%x1f%s"], check=False)
    if rc != 0:
        return out
    for line in text.splitlines():
        parts = line.split("\x1f", 2)
        if len(parts) != 3:
            continue
        sha, when, subject = parts
        for prefix in LANE_PREFIXES:
            key = prefix.rstrip(":")
            if out[key] is None and subject.startswith(prefix):
                out[key] = {"sha": sha, "subject": subject, "committed_iso": when}
    return out


def _stamp_value(line, keyword):
    """The value of a `KEYWORD:` stamp on one line, or None if it is not one.

    Tolerant of the markdown the queue actually contains.  The old parser
    required the line to START with the bare keyword, so it silently missed
    `**RATIFIED: operator, 2026-08-06** -- "stamp seq8"` -- a real, valid,
    operator-issued stamp that reads as UNSTAMPED to a `startswith` test.  A
    counter that calls a ratified item unratified because of two asterisks is
    not measuring the queue, it is measuring its own formatting assumptions.

    Leading `>`, `#`, `*`, `_` and whitespace are stripped before matching, and
    trailing emphasis is stripped from the value.
    """
    text = line.strip().lstrip(b">#*_ \t")
    if not text.upper().startswith(keyword + b":"):
        return None
    return text[len(keyword) + 1:].strip().strip(b"*_ \t")


def _is_stamped(blob, keyword):
    """True when `blob` carries a KEYWORD stamp that is real and not PENDING.

    Both a missing stamp and an explicit `KEYWORD: PENDING` read as NOT
    stamped -- the operator-facing meaning is the same in each case.
    """
    for raw in blob.split(b"\n"):
        value = _stamp_value(raw, keyword)
        if value and value.upper() != b"PENDING":
            return True
    return False


def queue_items():
    """[(name, ratified, built)] for every work order in exchange/queue/.

    A work order is ANY `.md` directly under exchange/queue/ except README.md,
    which is the convention document.

    The old rule counted only `NNN_*.md` -- three digits then an underscore.
    That silently excluded the three date-named contracts (WF1, SEQ8, MC1),
    which is how `MANIFEST.json` came to report `queue_open: 0` against a queue
    holding SIX items (HERMES finding F-3, 2026-08-12).  The filter was not
    wrong about the files it looked at; it was wrong about which files were
    work orders at all.

    Returns None when the queue directory does not exist.
    """
    qdir = os.path.join(REPO_ROOT, *QUEUE_DIR.split("/"))
    if not os.path.isdir(qdir):
        return None
    items = []
    for name in sorted(os.listdir(qdir)):
        if not name.lower().endswith(".md") or name.lower() == "readme.md":
            continue
        abs_path = os.path.join(qdir, name)
        if not os.path.isfile(abs_path):
            continue
        with open(abs_path, "rb") as handle:     # bytes, not a text pipeline
            blob = handle.read()
        items.append((name, _is_stamped(blob, b"RATIFIED"),
                      _is_stamped(blob, b"BUILT")))
    return items


def queue_counts():
    """The three truthful counters, plus the `queue_open` alias.

    queue_total              every non-README work order
    queue_unratified         no usable RATIFIED stamp -- may not be executed
    queue_ratified_unbuilt   ratified but not yet stamped BUILT -- the real
                             backlog, and the number `queue_open` now carries

    `queue_open` is KEPT as an alias of queue_ratified_unbuilt so nothing that
    reads the old key breaks.  Its meaning has changed, which is the point: the
    old number answered "what may not be executed yet" and was read by everyone
    as "what still has to be done".  Those differ, and on 2026-08-12 they
    differed by the entire queue.

    Returns a dict of Nones when the queue directory does not exist.
    """
    items = queue_items()
    if items is None:
        return {"queue_total": None, "queue_unratified": None,
                "queue_ratified_unbuilt": None, "queue_open": None}
    unratified = sum(1 for _, ratified, _ in items if not ratified)
    unbuilt = sum(1 for _, ratified, built in items if ratified and not built)
    return {"queue_total": len(items),
            "queue_unratified": unratified,
            "queue_ratified_unbuilt": unbuilt,
            "queue_open": unbuilt}


def queue_open():
    """Backward-compatible alias -- now `queue_ratified_unbuilt`.  See above."""
    return queue_counts()["queue_open"]


# --------------------------------------------------------------- the manifest

def build_manifest():
    tracked = tracked_paths()
    tracked_set = set(tracked)
    index = flatten_index(tracked)

    rc, head = git_text(["rev-parse", "HEAD"])
    branch, upstream, ahead_behind = branch_state()

    ref = upstream or ("origin/" + branch if branch else None)
    origin_head = None
    if ref:
        rc, text = git_text(["rev-parse", ref], check=False)
        if rc == 0:
            origin_head = text.strip()

    rc, status = git_text(["status", "--porcelain"])

    return {
        "manifest_version": MANIFEST_VERSION,
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "head": head.strip(),
        "branch": branch,
        "ahead_behind": ahead_behind,
        "origin_head": origin_head,
        "status_porcelain": status.splitlines(),
        "sources": [source_record(p, tracked_set) for p in expand_sources()],
        "reviewer_box": box_records(tracked_set, index),
        "untracked_root": untracked_root(),
        "eol_config": eol_config(),
        "onedrive_running": onedrive_running(),
        "ledger_head": ledger_head(),
        "lane_last_commit": lane_last_commit(),
        **queue_counts(),
    }


def serialize(manifest):
    return json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=True) + "\n"


def without_timestamp(text):
    return "\n".join(
        line for line in text.splitlines() if '"generated_utc"' not in line)


# -------------------------------------------------------------------- fixtures

def fixture_m1(manifest, out_abs, written_text):
    """F-M1 ROUND-TRIP (v1.1): the manifest survives a full write/read cycle.

    Three assertions in order, any of which fails the fixture:
      1. the bytes on disk are exactly the bytes we intended to write;
      2. those bytes re-parse as JSON;
      3. re-serialising the re-parsed object reproduces them byte for byte.

    (3) is the one that earns its keep.  A manifest that serialises but does not
    round-trip is a manifest whose consumers -- daily_routine.py compares
    archived manifests field by field -- can silently disagree with its author
    about what it says.  Byte-equality after a full cycle is the only cheap
    proof that the written record and the in-memory record are the same record.

    The v1.0 self-hash is retained as a fourth, secondary assertion: the
    recorded sha256 of this very script must still equal a fresh re-read.
    """
    if not os.path.isfile(out_abs):
        return False, "manifest was not written"

    with open(out_abs, "rb") as handle:          # bytes, not a text read
        on_disk = handle.read()
    intended = written_text.encode("utf-8")
    if on_disk != intended:
        return False, "on-disk %d bytes != %d bytes written" % (
            len(on_disk), len(intended))

    try:
        reparsed = json.loads(on_disk.decode("utf-8"))
    except ValueError as exc:
        return False, "written manifest does not re-parse: %s" % exc

    reserialized = serialize(reparsed).encode("utf-8")
    if reserialized != on_disk:
        return False, "re-serialised %d bytes differ from the written %d" % (
            len(reserialized), len(on_disk))

    # secondary -- the assertion F-M1 used to be, kept rather than replaced
    record = next(
        (r for r in manifest["sources"] if r.get("path") == SELF_REL), None)
    if record is None:
        return False, "%s absent from sources" % SELF_REL
    if record.get("present") is False:
        return False, "%s recorded as missing" % SELF_REL
    fresh = sha256_path(os.path.join(REPO_ROOT, SELF_REL))
    if not hashes_match(record["sha256_worktree"], fresh):
        return False, "recorded %s != re-read %s" % (
            record["sha256_worktree"][:12], fresh[:12])

    return True, "round-trip byte-identical over %d bytes; self sha256 %s" % (
        len(on_disk), fresh[:16])


def fixture_m2(manifest):
    """F-M2 blob-comparison correctness, both directions."""
    target = "engine/cells.py"
    record = next(
        (r for r in manifest["sources"] if r.get("path") == target), None)
    if record is None or record.get("present") is False:
        return False, "%s absent" % target
    if not record.get("tracked"):
        return False, "%s not tracked" % target
    if not record.get("match_head"):
        return False, "%s does not match its HEAD blob" % target

    tmpdir = tempfile.mkdtemp(prefix="naiad_fm2_")   # system temp, never the repo
    try:
        if os.path.realpath(tmpdir).startswith(REPO_ROOT + os.sep):
            return False, "refusing to run: temp dir landed inside the repo"
        with open(os.path.join(REPO_ROOT, target), "rb") as handle:
            data = bytearray(handle.read())
        if not data:
            return False, "%s is empty; nothing to mutate" % target
        data[-1] ^= 0x01                 # same length, exactly one byte differs
        mutant = os.path.join(tmpdir, "cells_mutated.py")
        with open(mutant, "wb") as handle:
            handle.write(bytes(data))
        mutated = sha256_path(mutant)
        if hashes_match(mutated, record["sha256_head_blob"]):
            return False, "comparator accepted a one-byte-different copy"
        if not hashes_match(record["sha256_worktree"], record["sha256_head_blob"]):
            return False, "comparator rejected the true copy"
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)
    return True, "true copy accepted, one-byte mutant rejected (%s)" % mutated[:12]


def fixture_m3(text_a, text_b):
    """F-M3 determinism: two back-to-back builds, timestamp line removed."""
    stripped_a = without_timestamp(text_a)
    stripped_b = without_timestamp(text_b)
    if stripped_a != stripped_b:
        return False, "second build differs from the first"
    return True, "two builds byte-identical over %d chars" % len(stripped_a)


def _porcelain_minus_output(text):
    """Porcelain lines with the manifest's OWN output path removed.

    v1.1.  Until the exchange migration the output lived in a git-ignored
    directory, so writing it could not move `git status` and F-M4 could compare
    raw.  exchange/status/MANIFEST.json is tracked, so the write now shows up as
    a modification of that one path -- expected, authorised by invariant 1, and
    not evidence of a side effect.

    Exactly one path is normalised out, matched literally.  Anything else the
    run touched still lands in the comparison and still fails the fixture.
    """
    kept = []
    for line in text.splitlines():
        if len(line) > 3 and line[3:].strip() == OUT_REL:
            continue
        kept.append(line)
    return kept


def fixture_m4(before, after):
    """F-M4 read-only audit: porcelain unchanged apart from the manifest."""
    norm_before = _porcelain_minus_output(before)
    norm_after = _porcelain_minus_output(after)
    if norm_before != norm_after:
        return False, "git status changed during the run"
    count = len([l for l in norm_before if l.strip()])
    raw_before = len([l for l in before.splitlines() if l.strip()])
    raw_after = len([l for l in after.splitlines() if l.strip()])
    note = ""
    if raw_before != count or raw_after != count:
        note = " (manifest's own path normalised out: %d/%d raw)" % (
            raw_before, raw_after)
    return True, "porcelain unchanged (%d entries before and after)%s" % (
        count, note)


# ------------------------------------------------------------------------ main

def main():
    rc, status_before = git_text(["status", "--porcelain"])

    first = build_manifest()
    text_a = serialize(first)
    second = build_manifest()
    text_b = serialize(second)

    out_abs = os.path.join(REPO_ROOT, OUT_REL)
    out_dir = os.path.dirname(out_abs)
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    with open(out_abs, "wb") as handle:
        handle.write(text_b.encode("utf-8"))

    rc, status_after = git_text(["status", "--porcelain"])

    results = [
        ("F-M1",) + fixture_m1(second, out_abs, text_b),
        ("F-M2",) + fixture_m2(second),
        ("F-M3",) + fixture_m3(text_a, text_b),
        ("F-M4",) + fixture_m4(status_before, status_after),
    ]

    # ASCII-only output: this runs in consoles that are not UTF-8.
    for name, ok, detail in results:
        print("%s %s - %s" % ("PASS" if ok else "FAIL", name, detail))

    print("wrote %s (%d sources, %d box files, %d untracked root)" % (
        OUT_REL, len(second["sources"]), len(second["reviewer_box"]),
        len(second["untracked_root"])))
    od = second["onedrive_running"]
    print("v1.1 fields: onedrive_running=%s, ledger %d B" % (
        "unknown" if od is None else ("yes" if od else "NO"),
        second["ledger_head"]["size"] or 0))
    print("queue: %s total · %s unratified · %s ratified-unbuilt "
          "(queue_open aliases the last)" % (
              "n/a" if second["queue_total"] is None else second["queue_total"],
              "n/a" if second["queue_unratified"] is None
              else second["queue_unratified"],
              "n/a" if second["queue_ratified_unbuilt"] is None
              else second["queue_ratified_unbuilt"]))

    failed = [name for name, ok, _ in results if not ok]
    if failed:
        print("HALT: %s failed; no partial adoption (contract section 5)"
              % ", ".join(failed))
        return 1
    return 0


REPO_ROOT = repo_root()

if __name__ == "__main__":
    raise SystemExit(main())
