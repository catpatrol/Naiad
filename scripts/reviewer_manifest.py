#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""One-paste integrity manifest for the reviewer loop.

Contract: prompts/Reviewer_Manifest_Builder_Contract.md (OPS tier, Tier-0,
drafted and ratified 2026-07-26).  This is an ops artifact: not study evidence,
no G-7, no journal reads, no engine imports, no ledger scorecard.

Invariants (contract section 1):
  1. Read-only on the repo.  The only file written inside the repo is
     _reviewer_box/MANIFEST.json (git-ignored).  Fixture F-M2's test double
     writes a mutated copy into a SYSTEM temp directory -- never the repo --
     and removes it again; that is the only write outside the manifest, and
     the contract mandates it.
  2. All byte questions answered with hashlib.sha256 over binary reads.  No
     grep/sed/text pipelines for byte questions: msys tools strip CR (known
     hazard, recorded 2026-07-26).
  3. Git is queried read-only via subprocess: rev-parse, status, cat-file,
     ls-files.  See NOTE_CONFIG for the one addition, `git config --get`.
  4. Standard library only.  Engine modules are never imported.

Field semantics, so a record cannot be misread:

  sources[]
    path              repo-relative, POSIX separators
    tracked           path appears in `git ls-files`
    size              worktree byte count
    sha256_worktree   sha256 of the worktree bytes
    sha256_head_blob  sha256 of the raw bytes of `git cat-file blob HEAD:<path>`
                      (null when the path is absent from HEAD)
    match_head        worktree bytes == HEAD blob bytes
    a missing file collapses to {path, present: false} and nothing else

  reviewer_box[]      path/size/sha256_worktree describe the BOX copy
    tracked           refers to the box path itself; the box is git-ignored,
                      so this is false by design, not a defect
    source_guess      repo path the flattened name resolves to (null if none)
    sha256_head_blob  HEAD blob of source_guess, not of the box path
    match_head        box copy == source_guess's HEAD blob, i.e. the question
                      "is this box copy still current?"

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
    "LEDGER.md",
    "DATA_CENSUS.md",
    "census.json",
    "research_outputs/census/build_manifest.json",
]
# ----------------------------------------------------------------------------

SELF_REL = "scripts/reviewer_manifest.py"
BOX_DIR = "_reviewer_box"
MANIFEST_NAME = "MANIFEST.json"
OUT_REL = BOX_DIR + "/" + MANIFEST_NAME

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
    path with '/' replaced by '_' resolves to that path.  It subsumes the named
    rules and additionally resolves nested copies (research_outputs_census_
    build_manifest.json) and bare root copies (census.json, DATA_CENSUS.md),
    which the three rules alone leave unmatched.  An ambiguous name resolves to
    None -- never a coin flip.
    """
    for prefix, replacement in FLATTEN_RULES:
        if name.startswith(prefix):
            candidate = replacement + name[len(prefix):]
            if candidate in tracked_set:
                return candidate
    hits = index.get(name, [])
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

    NOTE_CONFIG: core.autocrlf is reachable only through `git config --get`,
    which invariant 3's enumeration omits.  The enumeration is read as
    illustrative of READ-ONLY queries -- `--get` mutates nothing -- and the
    alternative (parsing system/global/local config files by hand) would be
    both fragile and less faithful to what git actually resolves.  Recorded
    here as a disclosed reading rather than a silent one.
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
    }


def serialize(manifest):
    return json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=True) + "\n"


def without_timestamp(text):
    return "\n".join(
        line for line in text.splitlines() if '"generated_utc"' not in line)


# -------------------------------------------------------------------- fixtures

def fixture_m1(manifest, out_abs):
    """F-M1 self-hash: recorded value == a fresh re-read after writing."""
    record = next(
        (r for r in manifest["sources"] if r.get("path") == SELF_REL), None)
    if record is None:
        return False, "%s absent from sources" % SELF_REL
    if record.get("present") is False:
        return False, "%s recorded as missing" % SELF_REL
    if not os.path.isfile(out_abs):
        return False, "manifest was not written"
    fresh = sha256_path(os.path.join(REPO_ROOT, SELF_REL))
    if not hashes_match(record["sha256_worktree"], fresh):
        return False, "recorded %s != re-read %s" % (
            record["sha256_worktree"][:12], fresh[:12])
    return True, "self sha256 %s re-read and equal" % fresh[:16]


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


def fixture_m4(before, after):
    """F-M4 read-only audit: porcelain status unchanged across the run."""
    if before != after:
        return False, "git status changed during the run"
    count = len([l for l in before.splitlines() if l.strip()])
    return True, "porcelain unchanged (%d entries before and after)" % count


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
        ("F-M1",) + fixture_m1(second, out_abs),
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

    failed = [name for name, ok, _ in results if not ok]
    if failed:
        print("HALT: %s failed; no partial adoption (contract section 5)"
              % ", ".join(failed))
        return 1
    return 0


REPO_ROOT = repo_root()

if __name__ == "__main__":
    raise SystemExit(main())
