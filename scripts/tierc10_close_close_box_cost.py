#!/usr/bin/env python
"""TIER-C10 · CLOSE · BOX-COST — THE SEVEN-COLUMN DISPOSITION TABLE, PRE-CLOSE.

The RESUME contract's CLOSE list ends "· findings-not-fixed · BOX-COST"
(exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md:136).  CONVENTIONS §3.2
(exchange/status/CONVENTIONS.md:341) says what that is: the table that covers
every file the build created, modified or moved, in SEVEN columns —

    PATH · EXISTS · TRACKED · COMMITTED · PUSHED · PROTECTED BY · BOX COST

— with BOX COST in bytes and % of the box for box-bound paths, FLAGGED over the
naming trip-wire, and "n/a — say which" for anything unsynced.  Both constants
come from `publish_exchange`, never a copy.

REPORT-ONLY · TIER-E BOOKKEEPING.  This file reads paths, byte counts and git
METADATA.  It reads no bar (so it has no reason to touch tierc10_data.load_asof
and does not import it), scores nothing, never calls TP.score / finish_family /
register, never OPENS a registration, score or scored file (it stats them), and
never consults a verdict.  PROGRESS.json is read for its artifact PATHS and its
stage names only.

WHAT IS IN THE TABLE (the auditor's four path sets, nothing typed)
  (a) every path in every commit whose SUBJECT starts `tierc10`
      (`git log --grep=^tierc10 --name-only`, then the subject re-checked,
      because --grep also matches a body line).  OR-1 paths (scripts/oracle_*,
      engine/rangefinder.py, scripts/rangefinder_*.py) appear ONLY because a
      tierc10 commit touched them, and are marked "OR-1 — listed read-only".
  (b) every artifact path in PROGRESS.json.  A path under a `cells` directory
      of census/ or null/ collapses into ONE row per cells directory (count +
      bytes, the covered cell directories listed in the JSON).  The rule is the
      spec's "census/cells and null/*/cells"; it also catches census/smoke/cells
      by the same shape, and the MD says so.
  (c) PLANNED exchange/reports/BUILD_2026-09-21_TIERC10_UNSEEN_RANGES.md, sized
      as the assembled draft: research_outputs/tierc10/BUILD_DRAFT.md plus every
      research_outputs/tierc10/close/*.md section present at run time (top level
      only) EXCEPT this item's own (a file does not measure itself).  Once the document
      exists on disk it is sized from disk instead.
  (d) the frozen snapshot /Users/luis/.cache/naiad/snapshots/tc10_20260921 —
      "n/a — outside repo; NOT PROTECTED until the LaCie mirror".

HOW EACH COLUMN IS READ (git verbs: log · ls-files · check-ignore ·
branch -r --contains · rev-parse — and nothing else, F-BC-GIT)
  EXISTS        os.stat, now.
  TRACKED       `git ls-files`; if untracked, `git check-ignore -v` names the
                .gitignore line; a tracked file that a pattern would ignore is
                named "force-added past" that line (`--no-index`).
  COMMITTED     `git log -1 --format=%h -- <path>`.
  PUSHED        `git branch -r --contains <COMMITTED>` against the
                remote-tracking refs AS LAST FETCHED.  No fetch is made.
  PROTECTED BY  GitHub only if PUSHED and the worktree is unmodified; otherwise
                NOT PROTECTED.  `--workflow` SCOPE is read from
                scripts/backup_estate.py WORKFLOW_SOURCES by AST (never
                imported) and printed as scope only: this file does not read the
                LaCie, so no archive is claimed.
  BOX COST      box-bound = under publish_exchange.SCOPE or in TICK_EXTRA:
                bytes · % of BOX_BYTES · FLAGGED when STRICTLY over FLAG_BYTES
                (publish_exchange.over_flag's own reading).  Else "n/a —
                unsynced", naming the root.
  Constants: BOX_BYTES, FLAG_BYTES, SCOPE, TICK_EXTRA and SUBJECT are
  ast.literal_eval'd from their assignments in scripts/publish_exchange.py.
  THAT MODULE IS NEVER IMPORTED OR EXECUTED (F-BC-CONST proves it).

THE LEGS — every leg states FAILS IF and carries sabotages that must go RED
  F-BC-CONST  FAILS IF the constants the table used differ from a FRESH AST read
              of publish_exchange.py / backup_estate.py, if either module was
              imported, or if an assignment is duplicated or non-literal.
              SABOTAGE: BOX_BYTES typed 16_000_001; a copy of publish_exchange
              carrying 16_000_001; a duplicated FLAG_BYTES; a non-literal
              FLAG_BYTES; a planted `import publish_exchange`.
  F-BC-COVER  FAILS IF any tierc10-commit path, any PROGRESS artifact outside a
              cells root, or any PROGRESS artifact DIRECTORY is missing, if a
              collapsed row's count disagrees with PROGRESS, or if (c)/(d) is
              missing.  SABOTAGE: drop one (a) row; drop one (b) row; drop the
              census/cells row; bend a collapsed count; drop the PLANNED row.
  F-BC-FLAG   FAILS IF a box-bound path over FLAG_BYTES is unflagged (bytes
              re-measured from disk, not trusted from the row), a flag fires at
              or under the wire, or an exchange/ path is classed unsynced.
              Controls: temp files at exactly FLAG_BYTES (unflagged) and
              FLAG_BYTES+1 (flagged) through the real builder.  SABOTAGE: a
              FLAG_BYTES+1 = 64,001 B temp file listed unflagged; the same file
              recorded stale at 64,000 B; the same file classed unsynced.
  F-BC-GIT    FAILS IF any git invocation this run made — recorded at the single
              choke point `_git` BEFORE it executes — uses a verb outside
              {log, ls-files, check-ignore, branch -r --contains, rev-parse}, if
              `git log --output` appears, if a `_git(...)` call in this source
              is not a literal allowed verb, or if a process is spawned anywhere
              but `_git`.  SABOTAGE: plant 'add' in the call record; plant
              `branch -a`, `push`, `log --output`; plant `_git(["add", "-A"])`
              and a raw `subprocess.run(["git", "add", "."])` in a source copy.
              (No planted verb is ever EXECUTED: the record is a list, the
              source copy is parsed, never run.)
  F-DET       FAILS IF two whole builds in one process differ by a byte, or a
              git-sourced column / top-level git field is not NAMED volatile.
              The pair is taken inside a QUIET WINDOW: an input fingerprint
              (HEAD, upstream tip, size+mtime of every input path, the
              snapshot's walk) is taken before, between and after the two
              builds, and a pair is kept only when all three agree — other
              sessions write close/ sections and commit while this runs, and a
              moved input is a named-volatile field moving, not a defect here.
              Never quiet in QUIET_TRIES attempts is RED.  SABOTAGE: a wall
              clock injected into the second render; PUSHED dropped from the
              named-volatile list.
  Cross-process determinism is the operator-visible proof: run the script whole
  twice (the second with --out-dir outside the repo) and compare the three
  files' sha256 — the transcript carries no clock, no temp path and no out-dir.

Run:
  export NAIAD_CACHE_DIR=/Users/luis/.cache/naiad/snapshots/tc10_20260921 \\
         PYTHONDONTWRITEBYTECODE=1
  ~/venvs/naiad/bin/python scripts/tierc10_close_close_box_cost.py
  ~/venvs/naiad/bin/python scripts/tierc10_close_close_box_cost.py --out-dir <scratch>
Writes ONLY research_outputs/tierc10/close/{S8_DISPOSITION_BOX_COST.md,
S8_DISPOSITION_BOX_COST.json, FIXTURES_CLOSE_box_cost.txt} (or the same three
names under an --out-dir OUTSIDE the repo).
Exit: 0 every leg GREEN · 1 a leg RED or a HALT.
"""
from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import json
import os
import stat as _stat
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = Path.home() / ".cache" / "naiad" / "snapshots" / "tc10_20260921"
LIVE_CACHE = Path.home() / ".cache" / "naiad" / "data_cache"


# ──────────────────────────────────────────────────────────── RUN / HALT preamble
def assert_substrate() -> Path:
    """THE FROZEN-SUBSTRATE GUARD [HARD LAW 3], restated so this module halts on
    its own word.  This file reads no bar; the guard stands anyway, so a run
    under the wrong substrate cannot be mistaken for a TC10 run.

    HALTS IF: NAIAD_CACHE_DIR is unset, is the live cache, or is anything but
    the TC10 snapshot; or bytecode writing is on (PYTHONDONTWRITEBYTECODE=1).
    """
    env = os.environ.get("NAIAD_CACHE_DIR", "")
    if not env:
        raise SystemExit("HALT: NAIAD_CACHE_DIR is unset — TC10 reads ONLY the "
                         f"snapshot {SNAPSHOT}")
    got = Path(env).expanduser().resolve()
    if got == LIVE_CACHE.resolve():
        raise SystemExit("HALT: NAIAD_CACHE_DIR is the LIVE cache — READ-NEVER, "
                         "WRITE-NEVER for TC10")
    if got != SNAPSHOT.resolve():
        raise SystemExit(f"HALT: NAIAD_CACHE_DIR={got} is not the TC10 snapshot "
                         f"{SNAPSHOT}")
    if not sys.dont_write_bytecode:
        raise SystemExit("HALT: PYTHONDONTWRITEBYTECODE=1 is not in force")
    return got


assert_substrate()

import subprocess                                                    # noqa: E402

# ──────────────────────────────────────────────────────────── paths of record
REL_PUBLISH = "scripts/publish_exchange.py"
REL_BACKUP = "scripts/backup_estate.py"
REL_PROGRESS = "research_outputs/tierc10/PROGRESS.json"
REL_DRAFT = "research_outputs/tierc10/BUILD_DRAFT.md"
REL_CLOSE = "research_outputs/tierc10/close"
REL_PLANNED = "exchange/reports/BUILD_2026-09-21_TIERC10_UNSEEN_RANGES.md"
REL_LEDGER_APOLLO = "exchange/status/LEDGER_APOLLO.md"
REL_SELF = "scripts/tierc10_close_close_box_cost.py"
MD_NAME = "S8_DISPOSITION_BOX_COST.md"
JSON_NAME = "S8_DISPOSITION_BOX_COST.json"
FIX_NAME = "FIXTURES_CLOSE_box_cost.txt"
TIER_ROOT = "research_outputs/tierc10/"
HEADER = "PRE-CLOSE SNAPSHOT — regenerate after the CLOSE commit/push"
LABEL = ("REPORT-ONLY · Tier-E bookkeeping — paths, bytes and git metadata; "
         "no bar read, nothing scored, no verdict consulted")
SNAPSHOT_TEXT = "n/a — outside repo; NOT PROTECTED until the LaCie mirror"

PUBLISH_NAMES = ("BOX_BYTES", "FLAG_BYTES", "SCOPE", "TICK_EXTRA", "SUBJECT")
BACKUP_NAMES = ("WORKFLOW_SOURCES", "WORKFLOW_ROOT_GLOBS")
NEVER_IMPORTED = ("publish_exchange", "backup_estate")

COLUMNS = ("PATH", "EXISTS", "TRACKED", "COMMITTED", "PUSHED", "PROTECTED BY",
           "BOX COST")
COLUMN_SOURCE = {
    "PATH": "git (the tierc10 commit set) + PROGRESS.json + fixed (c)/(d)",
    "EXISTS": "disk",
    "TRACKED": "git",
    "COMMITTED": "git",
    "PUSHED": "git",
    "PROTECTED BY": "git",
    "BOX COST": "disk",
}
TOP_GIT_FIELDS = ("git.head", "git.branch", "git.upstream", "git.upstream_tip",
                  "git.ahead", "rows[].in_tierc10_commits",
                  "summary.tierc10_commits_pushed")
TOP_DISK_FIELDS = ("rows[].bytes", "planned.components",
                   "not_in_table.ledger_apollo_bytes")


def _is_or1(rel: str) -> bool:
    return (rel.startswith("scripts/oracle_") or rel == "engine/rangefinder.py"
            or (rel.startswith("scripts/rangefinder_") and rel.endswith(".py")))


# ──────────────────────────────────────────────────────────── the one git door
class GitRefused(Exception):
    pass


GIT_CALLS: list = []          # every argv, recorded BEFORE it runs
ALLOWED_VERBS = ("log", "ls-files", "check-ignore", "rev-parse")
BRANCH_FORM = ("branch", "-r", "--contains")
_GIT_ENV = dict(os.environ, GIT_OPTIONAL_LOCKS="0", LC_ALL="C",
                GIT_PAGER="cat", GIT_TERMINAL_PROMPT="0")


def git_verb_ok(argv) -> tuple:
    """(ok, why) for one git argv.  The ONLY gate `_git` consults."""
    argv = tuple(argv)
    if not argv:
        return False, "empty argv"
    v = argv[0]
    if v == "log" and any(str(a).startswith("--output") for a in argv):
        return False, "`git log --output` writes a file"
    if v in ALLOWED_VERBS:
        return True, v
    if v == "branch":
        if argv[:3] == BRANCH_FORM and len(argv) == 4:
            return True, "branch -r --contains"
        return False, f"branch form {' '.join(argv[:3])!r} is not `branch -r --contains <sha>`"
    return False, f"verb {v!r} is outside {{log, ls-files, check-ignore, branch -r --contains, rev-parse}}"


def _git(argv, ok=(0,)) -> tuple:
    gate, why = git_verb_ok(argv)
    if not gate:
        raise GitRefused(why)
    GIT_CALLS.append(tuple(argv))
    proc = subprocess.run(["git", *argv], cwd=str(ROOT), stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, env=_GIT_ENV, timeout=300)
    if proc.returncode not in ok:
        raise SystemExit(f"HALT: git {' '.join(argv[:3])} … rc={proc.returncode}: "
                         f"{proc.stderr.decode('utf-8', 'replace').strip()[:300]}")
    return proc.returncode, proc.stdout.decode("utf-8", "replace")


def git_call_violations(calls) -> list:
    return [(c, git_verb_ok(c)[1]) for c in calls if not git_verb_ok(c)[0]]


def git_verb_census(calls) -> dict:
    out: dict = {}
    for c in calls:
        k = "branch -r --contains" if c[0] == "branch" else c[0]
        out[k] = out.get(k, 0) + 1
    return dict(sorted(out.items()))


# ──────────────────────────────────────────────────────────── constants by AST
class ConstRefused(Exception):
    pass


def read_literals(path: Path, names) -> dict:
    """{name: (value, lineno)} — each NAME must be assigned exactly once, at
    module level, to a literal.  The module is parsed, never imported."""
    tree = ast.parse(path.read_bytes().decode("utf-8"), filename=str(path))
    stores: dict = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and node.id in names and isinstance(node.ctx, ast.Store):
            stores.setdefault(node.id, []).append(node.lineno)
        if isinstance(node, ast.Global):
            for n in node.names:
                if n in names:
                    raise ConstRefused(f"{path.name}: `global {n}` rebinds a constant")
    found: dict = {}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            targets, value = node.targets, node.value
        elif isinstance(node, ast.AnnAssign) and node.value is not None:
            targets, value = [node.target], node.value
        else:
            continue
        for t in targets:
            if isinstance(t, ast.Name) and t.id in names:
                try:
                    found[t.id] = (ast.literal_eval(value), node.lineno)
                except ValueError:
                    raise ConstRefused(f"{path.name}:{node.lineno}: {t.id} is not a literal")
    for n in names:
        if n not in found:
            raise ConstRefused(f"{path.name}: no module-level literal assignment of {n}")
        if len(stores.get(n, [])) != 1:
            raise ConstRefused(f"{path.name}: {n} is bound {len(stores.get(n, []))} times "
                               f"(lines {stores.get(n)})")
    return found


def _fresh_const_read(path: Path, names) -> dict:
    """The F-BC-CONST re-read — a SECOND parse of the bytes on disk NOW, by a
    different walk (every Assign anywhere, not tree.body), so one reader's bug
    cannot vouch for itself.  {name: value}; duplicates → ConstRefused."""
    tree = ast.parse(path.read_bytes().decode("utf-8"))
    out: dict = {}
    for node in ast.walk(tree):
        tgts = (node.targets if isinstance(node, ast.Assign)
                else [node.target] if isinstance(node, (ast.AnnAssign, ast.AugAssign))
                else [])
        for t in tgts:
            if isinstance(t, ast.Name) and t.id in names:
                if t.id in out or isinstance(node, ast.AugAssign):
                    raise ConstRefused(f"{t.id} bound more than once")
                try:
                    out[t.id] = ast.literal_eval(node.value)
                except ValueError:
                    raise ConstRefused(f"{t.id} is not a literal")
    missing = [n for n in names if n not in out]
    if missing:
        raise ConstRefused(f"missing {missing}")
    return out


def load_constants(root: Path = ROOT) -> dict:
    pub = read_literals(root / REL_PUBLISH, PUBLISH_NAMES)
    bak = read_literals(root / REL_BACKUP, BACKUP_NAMES)
    c = {n: {"value": v, "source": f"{REL_PUBLISH}:{ln}"} for n, (v, ln) in pub.items()}
    c.update({n: {"value": v, "source": f"{REL_BACKUP}:{ln}"} for n, (v, ln) in bak.items()})
    for n in ("TICK_EXTRA", "WORKFLOW_SOURCES", "WORKFLOW_ROOT_GLOBS"):
        c[n]["value"] = list(c[n]["value"])
    return c


def _cv(consts, name):
    return consts[name]["value"]


# ──────────────────────────────────────────────────────────── citations, checked
def cite(rel: str, line: int, needle: str) -> str:
    """`rel:line` — HALTS unless `needle` is on that line NOW."""
    lines = (ROOT / rel).read_text(encoding="utf-8").splitlines()
    if line < 1 or line > len(lines) or needle not in lines[line - 1]:
        raise SystemExit(f"HALT: citation {rel}:{line} no longer carries {needle!r}")
    return f"{rel}:{line}"


# ──────────────────────────────────────────────────────────── path sets
def tierc10_commits() -> tuple:
    """(commits [(h, subject)], path -> [h newest first], grep-only [h])."""
    _, out = _git(["log", "--grep=^tierc10", "--name-only", "--format=%x00%h%x09%s"])
    commits, paths, grep_only = [], {}, []
    for chunk in out.split("\x00")[1:]:
        lines = chunk.split("\n")
        h, _, subj = lines[0].partition("\t")
        if not subj.startswith("tierc10"):
            grep_only.append(h)
            continue
        commits.append((h, subj))
        for p in (ln for ln in lines[1:] if ln.strip()):
            if p.startswith('"'):
                raise SystemExit(f"HALT: git quoted a path in commit {h}: {p}")
            paths.setdefault(p, []).append(h)
    return commits, paths, grep_only


def progress_artifacts() -> dict:
    """path -> [stage, …] in ledger order.  Paths and stage names ONLY."""
    d = json.loads((ROOT / REL_PROGRESS).read_text(encoding="utf-8"))
    out: dict = {}
    for s in d["stages"]:
        for p in (s.get("artifact_shas") or {}):
            out.setdefault(p, []).append(s["stage"])
    return out


def collapse_root(rel: str):
    """The cells root a PROGRESS path collapses into, or None."""
    parts = rel.split("/")
    if not rel.startswith(TIER_ROOT) or len(parts) < 5 or parts[2] not in ("census", "null"):
        return None
    dparts = parts[:-1]
    for i in range(3, len(dparts)):
        if dparts[i] == "cells":
            return "/".join(dparts[: i + 1])
    return None


def workflow_scope(rel: str, consts):
    for s in _cv(consts, "WORKFLOW_SOURCES"):
        if rel == s or rel.startswith(s + "/"):
            return s
    if "/" not in rel:
        import fnmatch
        for g in _cv(consts, "WORKFLOW_ROOT_GLOBS"):
            if fnmatch.fnmatchcase(rel, g):
                return f"repo root {g}"
    return None


# ──────────────────────────────────────────────────────────── per-row facts
def disk_size(root: Path, rel: str):
    p = root / rel
    try:
        st = os.lstat(p)
    except FileNotFoundError:
        return None
    return st.st_size if _stat.S_ISREG(st.st_mode) else None


def box_fields(rel: str, nbytes, consts, *, flag_limit=None) -> dict:
    """The BOX COST cell.  `flag_limit` exists ONLY so a sabotage can build a
    wrong flagger; every real row is built with FLAG_BYTES."""
    scope, tick = _cv(consts, "SCOPE"), _cv(consts, "TICK_EXTRA")
    box, flag = _cv(consts, "BOX_BYTES"), _cv(consts, "FLAG_BYTES")
    limit = flag if flag_limit is None else flag_limit
    bound = rel.startswith(scope) or rel in tick
    if not bound:
        root = rel.split("/")[0] + ("/" if "/" in rel else "")
        return {"box_bound": False, "flagged": False,
                "box_cost": f"n/a — unsynced (`{root}`)"}
    if nbytes is None:
        return {"box_bound": True, "flagged": False,
                "box_cost": "box-bound · NO SIZE — the path is absent"}
    flagged = nbytes > limit
    txt = f"{nbytes:,} B · {100.0 * nbytes / box:.3f}% of {box:,} B"
    txt += (f" · **FLAGGED** — over the {flag:,} B trip-wire; name it to the operator"
            if flagged else f" · under the {flag:,} B wire")
    return {"box_bound": True, "flagged": flagged, "box_cost": txt}


def _parse_check_ignore(out: str):
    line = out.splitlines()[0] if out.strip() else ""
    left = line.partition("\t")[0]
    bits = left.split(":", 2)
    if len(bits) != 3:
        return None
    src, ln, pat = bits
    if pat.startswith("!"):
        return None
    return f"{src}:{ln}", pat


class Ctx:
    """Per-build git caches (never shared across builds, so F-DET's second
    build re-asks git every question the first asked)."""

    def __init__(self):
        self.refs: dict = {}
        self.ignore_lines: dict = {}          # "src:line" -> pattern (the legend)

    def ign(self, hit):
        if not hit:
            return None
        self.ignore_lines[hit[0]] = hit[1]
        return f"`{hit[0]}`"

    def remote_refs(self, h: str) -> list:
        if h not in self.refs:
            _, out = _git(["branch", "-r", "--contains", h])
            self.refs[h] = sorted(ln.strip().split(" -> ")[0]
                                  for ln in out.splitlines() if ln.strip())
        return self.refs[h]


def git_fields(ctx: Ctx, rel: str, *, is_dir=False, n_files=0) -> dict:
    _, out = _git(["ls-files", "-z", "--", rel])
    listed = [x for x in out.split("\0") if x]
    f: dict = {}
    if is_dir:
        _, ci = _git(["check-ignore", "-v", "--", rel + "/"], ok=(0, 1))
        ign = ctx.ign(_parse_check_ignore(ci))
        f["tracked_state"] = "ignored" if (ign and not listed) else (
            "partly-tracked" if listed else "untracked")
        f["modified"] = False
        f["tracked"] = (f"ignored — {ign} · {len(listed)} of {n_files} tracked" if ign
                        else f"{len(listed)} of {n_files} tracked")
    elif rel in listed:
        _, m = _git(["ls-files", "-z", "-m", "--", rel])
        _, d = _git(["ls-files", "-z", "-d", "--", rel])
        rc, ci = _git(["check-ignore", "-v", "--no-index", "--", rel], ok=(0, 1))
        force = ctx.ign(_parse_check_ignore(ci)) if rc == 0 else None
        f["modified"] = bool(m.strip("\0")) or bool(d.strip("\0"))
        f["tracked_state"] = "tracked"
        t = "tracked"
        if d.strip("\0"):
            t += " · DELETED in worktree"
        elif m.strip("\0"):
            t += " · MODIFIED in worktree"
        if force:
            t += f" · force-added past {force}"
        f["tracked"] = t
    else:
        rc, ci = _git(["check-ignore", "-v", "--", rel], ok=(0, 1))
        ign = ctx.ign(_parse_check_ignore(ci)) if rc == 0 else None
        f["modified"] = False
        f["tracked_state"] = "ignored" if ign else "untracked"
        f["tracked"] = f"ignored — {ign}" if ign else "untracked"
    _, lo = _git(["log", "-1", "--format=%h%x09%s", "--", rel])
    h, _, subj = lo.strip().partition("\t")
    f["committed_sha"] = h or None
    f["committed_subject"] = subj or None
    f["committed"] = f"`{h}`" if h else "not committed"
    refs = ctx.remote_refs(h) if h else []
    f["pushed_refs"] = refs
    f["pushed"] = ("yes — " + ", ".join(f"`{r}`" for r in refs)) if refs else (
        "no" if h else "no — nothing committed")
    return f


def protected_text(rel: str, g: dict, consts) -> str:
    scope = workflow_scope(rel, consts)
    s = f"`--workflow` scope `{scope}`" if scope else "outside `--workflow`"
    if g["pushed_refs"] and not g["modified"]:
        base = f"GitHub only (`{g['pushed_refs'][0]}`)"
    elif g["pushed_refs"]:
        base = "NOT PROTECTED — worktree differs from the pushed sha"
    elif g["committed_sha"]:
        base = "NOT PROTECTED — committed, not pushed"
    else:
        base = "NOT PROTECTED — local disk only"
    return f"{base} · {s}"


# ──────────────────────────────────────────────────────────── the build
def planned_components(own_md: str = MD_NAME) -> tuple:
    """(mode, [(rel, bytes)]) for the PLANNED build document."""
    on_disk = disk_size(ROOT, REL_PLANNED)
    if on_disk is not None:
        return "filed", [(REL_PLANNED, on_disk)]
    comps = [(REL_DRAFT, disk_size(ROOT, REL_DRAFT))]
    close_dir = ROOT / REL_CLOSE
    if close_dir.is_dir():
        for p in sorted(close_dir.glob("*.md")):
            if p.name != own_md and p.is_file():
                comps.append((f"{REL_CLOSE}/{p.name}", disk_size(ROOT, f"{REL_CLOSE}/{p.name}")))
    return "assembled-draft", comps


def snapshot_walk(root: Path = SNAPSHOT) -> tuple:
    n = b = 0
    for dp, dns, fns in os.walk(root):
        dns.sort()
        for fn in sorted(fns):
            st = os.lstat(os.path.join(dp, fn))
            if _stat.S_ISREG(st.st_mode):
                n += 1
                b += st.st_size
    return n, b


def build(consts) -> dict:
    ctx = Ctx()
    commits, cpaths, grep_only = tierc10_commits()
    prog = progress_artifacts()
    rows = []

    def file_row(group, rel):
        nb = disk_size(ROOT, rel)
        g = git_fields(ctx, rel)
        r = {"group": group, "kind": "file", "path": rel, "or1": _is_or1(rel),
             "exists": nb is not None, "bytes": nb,
             "in_tierc10_commits": cpaths.get(rel, []),
             "progress_stages": prog.get(rel, [])}
        r.update({k: g[k] for k in ("tracked", "tracked_state", "modified", "committed",
                                    "committed_sha", "committed_subject", "pushed",
                                    "pushed_refs")})
        r["protected_by"] = protected_text(rel, g, consts)
        r.update(box_fields(rel, nb, consts))
        r["exists_text"] = f"yes · {nb:,} B" if nb is not None else "no"
        return r

    # (a) — every path a tierc10 commit touched (OR-1 included, marked)
    for rel in sorted(cpaths):
        rows.append(file_row("a", rel))
    # (b) — PROGRESS artifacts; cells collapse per cells root
    groups: dict = {}
    for rel in sorted(prog):
        cr = collapse_root(rel)
        if cr:
            groups.setdefault(cr, []).append(rel)
        elif rel not in cpaths and not _is_or1(rel):
            rows.append(file_row("b", rel))
    for cr in sorted(groups):
        recs = groups[cr]
        leaf_dirs = sorted({r.rsplit("/", 1)[0] for r in recs})
        sizes = [disk_size(ROOT, r) for r in recs]
        present = [s for s in sizes if s is not None]
        disk_n = sum(1 for dp, _, fns in os.walk(ROOT / cr) for fn in fns
                     if _stat.S_ISREG(os.lstat(os.path.join(dp, fn)).st_mode)) \
            if (ROOT / cr).is_dir() else 0
        g = git_fields(ctx, cr, is_dir=True, n_files=len(recs))
        r = {"group": "b-cells", "kind": "cells-dir", "path": cr, "or1": False,
             "exists": bool(present), "bytes": sum(present),
             "n_recorded": len(recs), "n_present": len(present), "n_on_disk": disk_n,
             "n_dirs": len(leaf_dirs), "covered_dirs": leaf_dirs,
             "in_tierc10_commits": [],
             "progress_stages": sorted({s for x in recs for s in prog[x]})}
        r.update({k: g[k] for k in ("tracked", "tracked_state", "modified", "committed",
                                    "committed_sha", "committed_subject", "pushed",
                                    "pushed_refs")})
        r["protected_by"] = protected_text(cr, g, consts)
        r.update(box_fields(cr, None if not present else sum(present), consts))
        et = (f"yes · {len(leaf_dirs)} dirs · {len(present):,} files · {sum(present):,} B"
              if present else "no")
        if len(present) != len(recs):
            et += f" · {len(recs) - len(present)} recorded files ABSENT"
        if disk_n != len(present):
            et += f" · {disk_n:,} files on disk (+{disk_n - len(present):,} not in PROGRESS)"
        r["exists_text"] = et
        rows.append(r)
    # (c) — the PLANNED build document
    mode, comps = planned_components()
    total = sum(b for _, b in comps if b is not None)
    gp = git_fields(ctx, REL_PLANNED)
    rp = {"group": "c", "kind": "planned", "path": REL_PLANNED, "or1": False,
          "exists": mode == "filed", "bytes": total, "sizing": mode,
          "components": [{"path": p, "bytes": b} for p, b in comps],
          "in_tierc10_commits": cpaths.get(REL_PLANNED, []), "progress_stages": []}
    rp.update({k: gp[k] for k in ("tracked_state", "modified", "committed", "committed_sha",
                                  "committed_subject", "pushed", "pushed_refs")})
    if mode == "filed":
        rp["tracked"] = gp["tracked"]
        rp["exists_text"] = f"yes · {total:,} B"
        rp["protected_by"] = protected_text(REL_PLANNED, gp, consts)
    else:
        rp["tracked"] = "untracked — PLANNED, not yet on disk" + (
            f" · would be {gp['tracked']}" if gp["tracked_state"] == "ignored" else "")
        rp["exists_text"] = (f"no — PLANNED · sized as the assembled draft: {total:,} B "
                             f"({len(comps)} part{'s' if len(comps) != 1 else ''})")
        sc = workflow_scope(REL_PLANNED, consts)
        rp["protected_by"] = ("NOT PROTECTED — PLANNED; `publish_exchange.publish()` commits "
                              "and pushes `exchange/**` at CLOSE (CONVENTIONS §3.4) · "
                              + (f"`--workflow` scope `{sc}`" if sc else "outside `--workflow`"))
    rp.update(box_fields(REL_PLANNED, total, consts))
    rows.append(rp)
    # (d) — the snapshot
    sn, sb = snapshot_walk()
    rows.append({"group": "d", "kind": "snapshot", "path": str(SNAPSHOT), "or1": False,
                 "exists": SNAPSHOT.is_dir(), "bytes": sb, "n_files": sn,
                 "exists_text": f"yes · {sn:,} files · {sb:,} B" if SNAPSHOT.is_dir() else "no",
                 "tracked": "n/a — outside repo", "tracked_state": "outside-repo",
                 "modified": False, "committed": "n/a — outside repo", "committed_sha": None,
                 "committed_subject": None, "pushed": "n/a — outside repo",
                 "pushed_refs": [], "protected_by": "NOT PROTECTED until the LaCie mirror",
                 "box_bound": False, "flagged": False, "box_cost": "n/a — outside repo",
                 "in_tierc10_commits": [], "progress_stages": []})

    # git context
    _, head = _git(["rev-parse", "--short", "HEAD"])
    _, br = _git(["rev-parse", "--abbrev-ref", "HEAD"])
    rc, up = _git(["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"], ok=(0, 128))
    up = up.strip() if rc == 0 else None
    tip = ahead = None
    if up:
        _, tip = _git(["rev-parse", "--short", "@{u}"])
        tip = tip.strip()
        _, al = _git(["log", "--format=%h", "@{u}..HEAD"])
        ahead = len([x for x in al.splitlines() if x.strip()])
    pushed_commits = [h for h, _ in commits if ctx.remote_refs(h)]

    # what the CLOSE also touches but this table does not row
    la = disk_size(ROOT, REL_LEDGER_APOLLO)
    model = {
        "header": HEADER, "label": LABEL, "built_by": REL_SELF,
        "contract_item": cite("exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md", 136,
                              "findings-not-fixed · BOX-COST"),
        "standard": cite("exchange/status/CONVENTIONS.md", 341, "3.2 The file-disposition table"),
        "constants": consts,
        "git": {"head": head.strip(), "branch": br.strip(), "upstream": up,
                "upstream_tip": tip, "ahead": ahead, "fetch_made": False},
        "ignore_lines": dict(sorted(ctx.ignore_lines.items())),
        "tierc10_commits": [{"sha": h, "subject": s} for h, s in commits],
        "grep_only_commits": grep_only,
        "columns": list(COLUMNS), "column_source": COLUMN_SOURCE,
        "volatile": {
            "git": sorted([c for c, s in COLUMN_SOURCE.items() if "git" in s]
                          + list(TOP_GIT_FIELDS)),
            "disk": sorted([c for c, s in COLUMN_SOURCE.items() if "disk" in s]
                           + list(TOP_DISK_FIELDS)),
        },
        "rows": rows,
        "summary": {
            "rows": {g: sum(1 for r in rows if r["group"] == g)
                     for g in ("a", "b", "b-cells", "c", "d")},
            "tierc10_commits": len(commits),
            "tierc10_commits_pushed": len(pushed_commits),
            "or1_rows": [r["path"] for r in rows if r["or1"]],
            "tracked_state": {k: sum(1 for r in rows if r["tracked_state"] == k)
                              for k in sorted({r["tracked_state"] for r in rows})},
            "committed_rows": sum(1 for r in rows if r["committed_sha"]),
            "pushed_rows": sum(1 for r in rows if r["pushed_refs"]),
            "box_bound_rows": [r["path"] for r in rows if r["box_bound"]],
            "box_bound_bytes": sum(r["bytes"] or 0 for r in rows if r["box_bound"]),
            "flagged_rows": [r["path"] for r in rows if r["flagged"]],
            "ignored_file_rows": sum(1 for r in rows
                                     if r["kind"] == "file" and r["tracked_state"] == "ignored"),
            "ignored_cells_files": sum(r["n_present"] for r in rows
                                       if r["kind"] == "cells-dir"
                                       and r["tracked_state"] == "ignored"),
        },
        "not_in_table": {
            "ledger_apollo": REL_LEDGER_APOLLO,
            "ledger_apollo_bytes": la,
            "ledger_apollo_over_wire": (la or 0) > _cv(consts, "FLAG_BYTES"),
        },
        "citations": {
            "push_permission": cite("research_outputs/tierc10/OPERATOR_RULINGS.md", 37,
                                    "Permission to push granted"),
            "lacie_vault": cite("research_outputs/tierc10/OPERATOR_RULINGS.md", 65,
                                "/Volumes/LaCie/Repo Clone/naiad-backups"),
            "no_hand_commit": cite("exchange/status/CONVENTIONS.md", 415,
                                   "Do NOT `git add` or `git commit` exchange files separately"),
            "flag_strict": cite(REL_PUBLISH, 363, "STRICTLY over"),
        },
    }
    return model


# ──────────────────────────────────────────────────────────── render
def _cell(s) -> str:
    return str(s).replace("|", "\\|").replace("\n", " ")


def _row_md(r) -> str:
    path = f"`{r['path']}`"
    if r["or1"]:
        path += " · OR-1, listed read-only"
    if r["group"] == "a" and r["progress_stages"]:
        path += " · +PROGRESS"
    return "| " + " | ".join(_cell(x) for x in (
        path, r["exists_text"], r["tracked"], r["committed"], r["pushed"],
        r["protected_by"], r["box_cost"])) + " |"


def render_md(m: dict) -> str:
    c = m["constants"]
    S = m["summary"]
    g = m["git"]
    rows = m["rows"]
    L = []
    A = L.append
    th = "| " + " | ".join(COLUMNS) + " |"
    tb = "|" + "---|" * len(COLUMNS)
    A("## 8 · DISPOSITION · BOX-COST")
    A("")
    A(f"> **{m['header']}.** Every git column below is true of HEAD `{g['head']}` and of the "
      f"remote-tracking refs as last fetched; the CLOSE commit and push change TRACKED, "
      f"COMMITTED, PUSHED and PROTECTED BY for most rows. Re-run "
      f"`{m['built_by']}` after them and file THAT table.")
    A(">")
    A(f"> **{m['label']}.** Every table in this section is REPORT-ONLY.")
    A("")
    A(f"The CLOSE item `{m['contract_item']}` (· findings-not-fixed · BOX-COST), built to the "
      f"seven-column standard at `{m['standard']}`. Built by `{m['built_by']}` — "
      f"transcript `{REL_CLOSE}/{FIX_NAME}`.")
    A("")
    A("**Constants — read by `ast.literal_eval` of their assignments; the modules are never "
      "imported or executed (F-BC-CONST):**")
    A("")
    for n in ("BOX_BYTES", "FLAG_BYTES"):
        A(f"- `{n}` = {c[n]['value']:,} B — `{c[n]['source']}`")
    A(f"- `SCOPE` = `{c['SCOPE']['value']}` — `{c['SCOPE']['source']}` · `TICK_EXTRA` = "
      f"{', '.join('`' + x + '`' for x in c['TICK_EXTRA']['value'])} — "
      f"`{c['TICK_EXTRA']['source']}` (box-bound = either)")
    A(f"- `WORKFLOW_SOURCES` — {len(c['WORKFLOW_SOURCES']['value'])} roots — "
      f"`{c['WORKFLOW_SOURCES']['source']}`; `WORKFLOW_ROOT_GLOBS` "
      f"{', '.join('`' + x + '`' for x in c['WORKFLOW_ROOT_GLOBS']['value'])} — "
      f"`{c['WORKFLOW_ROOT_GLOBS']['source']}` (PROTECTED BY prints `--workflow` SCOPE only)")
    A("")
    A(f"**Git state (git-volatile):** HEAD `{g['head']}` on `{g['branch']}` · upstream "
      f"`{g['upstream']}` at `{g['upstream_tip']}` · HEAD is **{g['ahead']} commits ahead** of it · "
      f"**{S['tierc10_commits_pushed']} of {S['tierc10_commits']}** `tierc10` commits are "
      f"contained in any remote-tracking ref · no fetch was made.")
    A("")
    A("**How each column is read.** PATH — the four sets below. EXISTS — `os.stat` now. "
      "TRACKED — `git ls-files`; if untracked, `git check-ignore -v` names the `.gitignore` "
      "line; a tracked file a pattern would ignore is named *force-added past* that line. "
      "COMMITTED — `git log -1 --format=%h -- <path>`. PUSHED — `git branch -r --contains "
      "<COMMITTED>` (refs as last fetched). PROTECTED BY — *GitHub only* when pushed and "
      "unmodified, else **NOT PROTECTED**; `--workflow` *scope* is printed, never an archive "
      "(this table does not read the LaCie). BOX COST — bytes and % of `BOX_BYTES` for "
      "box-bound paths, **FLAGGED** when strictly over `FLAG_BYTES` "
      f"(`{m['citations']['flag_strict']}`), else *n/a — unsynced*, naming the root. "
      "Git verbs used: `log` · `ls-files` · `check-ignore` · `branch -r --contains` · "
      "`rev-parse` — nothing else (F-BC-GIT).")
    A("")
    if m["ignore_lines"]:
        A("**`.gitignore` lines cited in TRACKED:** "
          + " · ".join(f"`{k}` = `{v}`" for k, v in m["ignore_lines"].items()))
        A("")
    A("### 8.0 · At a glance — REPORT-ONLY")
    A("")
    A("| | count |")
    A("|---|---:|")
    A(f"| (a) paths in `tierc10` commits ({S['tierc10_commits']} commits) | {S['rows']['a']} |")
    A(f"| (b) PROGRESS.json artifacts not already in (a) | {S['rows']['b']} |")
    A(f"| (b) cells directories, collapsed | {S['rows']['b-cells']} |")
    A(f"| (c) PLANNED build document | {S['rows']['c']} |")
    A(f"| (d) the frozen snapshot | {S['rows']['d']} |")
    for k, v in S["tracked_state"].items():
        A(f"| rows · TRACKED state `{k}` | {v} |")
    A(f"| rows with a COMMITTED sha | {S['committed_rows']} |")
    A(f"| rows PUSHED (a remote-tracking ref contains the sha) | {S['pushed_rows']} |")
    A(f"| OR-1 rows (listed read-only) | {len(S['or1_rows'])} |")
    A(f"| box-bound rows | {len(S['box_bound_rows'])} |")
    A(f"| box-bound bytes (these rows) | {S['box_bound_bytes']:,} B · "
      f"{100.0 * S['box_bound_bytes'] / c['BOX_BYTES']['value']:.3f}% of the box |")
    A(f"| **FLAGGED** rows (> {c['FLAG_BYTES']['value']:,} B) | {len(S['flagged_rows'])} |")
    A("")
    sections = (
        ("a", f"### 8.1 · (a) every path in a `tierc10` commit — {S['rows']['a']} paths, "
              f"{S['tierc10_commits']} commits — REPORT-ONLY",
         "Subject re-checked to start `tierc10` (`--grep` also matches body lines; "
         f"{len(m['grep_only_commits'])} grep-only commit(s) dropped). `+PROGRESS` = also a "
         "PROGRESS.json artifact."),
        ("b", f"### 8.2 · (b) PROGRESS.json artifacts not already in (a) — {S['rows']['b']} "
              f"paths — REPORT-ONLY", None),
        ("b-cells", f"### 8.3 · (b) the cells directories, collapsed per directory — "
                    f"{S['rows']['b-cells']} rows — REPORT-ONLY",
         "The spec's `census/cells` and `null/*/cells`, by the rule *the path up to its "
         "`cells` segment under census/ or null/*; the same shape also collapses "
         "`census/smoke/cells` — stated here, not hidden. Count + bytes are the PROGRESS-"
         "recorded files; the covered cell directories are listed in the JSON."),
        ("c", "### 8.4 · (c) the PLANNED build document — REPORT-ONLY", None),
        ("d", "### 8.5 · (d) the frozen snapshot — REPORT-ONLY",
         "Stat only — no bar is opened. Marked "
         f"*{SNAPSHOT_TEXT}* (the vault named in "
         f"`{m['citations']['lacie_vault']}`)."),
    )
    for grp, title, note in sections:
        A(title)
        A("")
        if note:
            A(note)
            A("")
        A(th)
        A(tb)
        for r in rows:
            if r["group"] == grp:
                A(_row_md(r))
        A("")
        if grp == "c":
            rp = next(r for r in rows if r["group"] == "c")
            A(f"Sized as the {'filed document' if rp['sizing'] == 'filed' else 'assembled draft'}"
              f" — {rp['bytes']:,} B from:")
            A("")
            for comp in rp["components"]:
                A(f"- `{comp['path']}` — "
                  + (f"{comp['bytes']:,} B" if comp["bytes"] is not None else "ABSENT"))
            if rp["sizing"] != "filed":
                A(f"- this section (`{REL_CLOSE}/{MD_NAME}`) — **not counted**: a file does not "
                  f"measure itself; the post-CLOSE regeneration sizes the filed document from disk.")
                A("")
                A("An ESTIMATE, not a measurement: the parts are summed as they stand at run time; "
                  "a part that replaces a draft placeholder is not netted out, and no fixture "
                  "transcript is counted. The flag decision is what the operator needs from it.")
            A("")
    A("### 8.6 · BOX COST — REPORT-ONLY")
    A("")
    A("| box-bound path | bytes | % of box | trip-wire |")
    A("|---|---:|---:|---|")
    for r in rows:
        if r["box_bound"]:
            A(f"| `{r['path']}`{' (PLANNED)' if r['kind'] == 'planned' and not r['exists'] else ''}"
              f" | {r['bytes']:,} | {100.0 * r['bytes'] / c['BOX_BYTES']['value']:.3f}% | "
              f"{'**FLAGGED**' if r['flagged'] else 'under'} |")
    A(f"| **these rows, together** | {S['box_bound_bytes']:,} | "
      f"{100.0 * S['box_bound_bytes'] / c['BOX_BYTES']['value']:.3f}% | — |")
    A("")
    nt = m["not_in_table"]
    A(f"Not a row, named because the CLOSE touches it: `{nt['ledger_apollo']}` receives the "
      f"LEDGER_APOLLO append. It is **{nt['ledger_apollo_bytes']:,} B now**, "
      + ("already over the trip-wire — an append-only file that grew across it, which §3.2's "
         "named cost says the duty-at-creation never binds; `publish()` names it on every "
         "publish (advisory, never a refusal)."
         if nt["ledger_apollo_over_wire"] else "under the trip-wire.")
      + " The append is not drafted, so it is not sized.")
    A("")
    A("The whole-bus figure (`exchange/**` and the tick set, against warn/refuse) is **not "
      "computed here**: computing it the way the guard does would mean importing "
      "`publish_exchange`, which this table never does. `publish()` prints it at CLOSE.")
    A("")
    A("### 8.7 · Findings — reported, not fixed — REPORT-ONLY")
    A("")
    n_a = S["rows"]["a"]
    A(f"- **BC-1 · NOTHING OF TC10 IS ON GITHUB.** {S['tierc10_commits_pushed']} of "
      f"{S['tierc10_commits']} `tierc10` commits are in any remote-tracking ref; HEAD is "
      f"{g['ahead']} ahead of `{g['upstream']}`. Every (a) row reads NOT PROTECTED. Push "
      f"permission is on file (`{m['citations']['push_permission']}`); the push is a CLOSE "
      f"act, not this table's.")
    ign_rows = S["ignored_file_rows"]
    A(f"- **BC-2 · THE EVIDENCE TREE IS GIT-IGNORED.** {ign_rows} file rows and "
      f"{S['ignored_cells_files']:,} collapsed cell files sit under an ignore pattern — "
      f"local disk only, outside `--workflow` scope. No `--phase tierc10` archive is verified "
      f"by this table.")
    hand = [r for r in rows if r["box_bound"] and r["committed_sha"]
            and not (r["committed_subject"] or "").startswith(
                c["SUBJECT"]["value"].split("{")[0])]
    if hand:
        A("- **BC-3 · A BOX-BOUND FILE WAS COMMITTED BY HAND.** "
          + "; ".join(f"`{r['path']}` last committed in `{r['committed_sha']}` "
                      f"(\"{r['committed_subject'][:60]}…\")" for r in hand)
          + f" — not by `publish()` (`SUBJECT` = \"{c['SUBJECT']['value']}\", "
          f"`{c['SUBJECT']['source']}`). `{m['citations']['no_hand_commit']}` asks that "
          f"exchange files ride only the guard. It will ride the next branch push.")
    outside = sorted(r["path"] for r in rows if r["group"] == "a" and r["kind"] == "file"
                     and r["tracked_state"] == "tracked"
                     and workflow_scope(r["path"], c) is None)
    roots: dict = {}
    for p in outside:
        parts = p.split("/")
        k = ("/".join(parts[:2]) + "/" if p.startswith("research_outputs/")
             else parts[0] + "/" if len(parts) > 1 else p)
        roots[k] = roots.get(k, 0) + 1
    A(f"- **BC-4 · TRACKED, BUT OUTSIDE `--workflow` SCOPE:** {len(outside)} (a) paths — "
      + ", ".join(f"`{k}` {n}" for k, n in sorted(roots.items()))
      + ". Once pushed, GitHub is their only copy.")
    A(f"- **BC-5 · THE SNAPSHOT IS NOT PROTECTED** ({next(r for r in rows if r['group'] == 'd')['exists_text']}): "
      f"every TC10 number was computed on it; the vault is named at "
      f"`{m['citations']['lacie_vault']}` and the mirror awaits the operator's destination word.")
    if S["flagged_rows"]:
        A("- **BC-6 · FLAGGED FOR NAMING:** " + ", ".join(f"`{p}`" for p in S["flagged_rows"])
          + " — over the trip-wire; §3.2 asks it be named to the operator with its home.")
    else:
        A(f"- **BC-6 · NO ROW IS FLAGGED** at this snapshot; the PLANNED document's size is an "
          f"estimate that grows as the CLOSE sections land — the regeneration re-judges it.")
    A("")
    A("### 8.8 · Volatile fields — named (F-DET) — REPORT-ONLY")
    A("")
    A("Two whole runs on an unchanged tree are byte-identical (F-DET compares two builds "
      "inside a window where every input held still). These fields move without any change "
      "to this script — a commit, a push, a fetch, or another CLOSE section landing:")
    A("")
    A("- **git-volatile:** " + ", ".join(f"`{x}`" for x in m["volatile"]["git"]))
    A("- **disk-volatile:** " + ", ".join(f"`{x}`" for x in m["volatile"]["disk"]))
    A("")
    return "\n".join(L)


def render_json(m: dict) -> str:
    return json.dumps(m, indent=1, sort_keys=True, ensure_ascii=False) + "\n"


def render(m: dict) -> tuple:
    return render_md(m).encode("utf-8"), render_json(m).encode("utf-8")


# ──────────────────────────────────────────────────────────── quiescent double build
QUIET_TRIES = 6
QUIET_WAIT_S = 5.0
ONE_BUILD_CALLS: list = []


def input_fingerprint() -> tuple:
    """Everything a build reads that another writer could move: HEAD, the
    upstream tip, and (size, mtime_ns) of every input path — the tierc10-commit
    paths, every PROGRESS artifact, the draft, the close/ sections, the planned
    document, the ledger, the two constant sources — plus the snapshot's walk."""
    _, head = _git(["rev-parse", "HEAD"])
    rc, up = _git(["rev-parse", "@{u}"], ok=(0, 128))
    paths = set(_expected_commit_paths())
    paths |= set(progress_artifacts())
    paths |= {REL_DRAFT, REL_PLANNED, REL_PROGRESS, REL_LEDGER_APOLLO, REL_PUBLISH, REL_BACKUP}
    cd = ROOT / REL_CLOSE
    if cd.is_dir():
        paths |= {f"{REL_CLOSE}/{q.name}" for q in cd.glob("*.md")}
    st = []
    for rel in sorted(paths):
        try:
            x = os.lstat(ROOT / rel)
            st.append((rel, x.st_size, x.st_mtime_ns))
        except FileNotFoundError:
            st.append((rel, None, None))
    return head.strip(), (up.strip() if rc == 0 else None), tuple(st), snapshot_walk()


def stable_build(consts) -> tuple:
    """(m1, m2, quiet) — two whole builds bracketed by three fingerprints.
    A pair is kept only when all three agree; otherwise wait and retry.  The
    retries are reported on stderr only: the transcript must not depend on how
    busy the other writers were."""
    import time
    m1 = m2 = None
    for attempt in range(QUIET_TRIES):
        f0 = input_fingerprint()
        i0 = len(GIT_CALLS)
        m1 = build(consts)
        i1 = len(GIT_CALLS)
        f1 = input_fingerprint()
        m2 = build(consts)
        f2 = input_fingerprint()
        if f0 == f1 == f2:
            ONE_BUILD_CALLS[:] = GIT_CALLS[i0:i1]
            return m1, m2, True
        print(f"[stderr] F-DET: inputs moved during attempt {attempt + 1}; waiting "
              f"{QUIET_WAIT_S:.0f} s", file=sys.stderr)
        time.sleep(QUIET_WAIT_S)
    ONE_BUILD_CALLS[:] = GIT_CALLS[i0:i1]
    return m1, m2, False


# ──────────────────────────────────────────────────────────── fixture legs
class Leg:
    def __init__(self, fid: str, fails_if: str, out):
        self.fid, self.out = fid, out
        self.control_ok = True
        self.sab_total = self.sab_red = 0
        out(f"── {fid}")
        out(f"   FAILS IF: {fails_if}")

    def control(self, name: str, ok: bool, detail: str = ""):
        self.control_ok &= bool(ok)
        self.out(f"   control · {name}: {'GREEN' if ok else 'RED'}"
                 + (f" — {detail}" if detail else ""))

    def sabotage(self, name: str, went_red: bool, detail: str = ""):
        self.sab_total += 1
        self.sab_red += bool(went_red)
        self.out(f"   SABOTAGE · {name}: {'RED (as required)' if went_red else 'GREEN — THE GUARD DID NOT FIRE'}"
                 + (f" — {detail}" if detail else ""))

    def verdict(self) -> bool:
        ok = self.control_ok and self.sab_red == self.sab_total and self.sab_total > 0
        self.out(f"   {self.fid}: {'GREEN' if ok else 'RED'} (controls "
                 f"{'ok' if self.control_ok else 'FAILED'}; sabotages RED "
                 f"{self.sab_red}/{self.sab_total})")
        return ok


def const_violations(model_consts: dict, fresh: dict) -> list:
    return [n for n in fresh if model_consts.get(n, {}).get("value") != (
        list(fresh[n]) if isinstance(fresh[n], tuple) else fresh[n])]


def import_violations(src: str) -> list:
    bad = []
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, ast.Import):
            bad += [a.name for a in node.names if a.name.split(".")[0] in NEVER_IMPORTED]
        elif isinstance(node, ast.ImportFrom):
            if (node.module or "").split(".")[0] in NEVER_IMPORTED:
                bad.append(node.module)
            bad += [a.name for a in node.names if a.name in NEVER_IMPORTED]
        elif isinstance(node, ast.Call) and isinstance(node.func, (ast.Name, ast.Attribute)):
            fn = node.func.id if isinstance(node.func, ast.Name) else node.func.attr
            if fn in ("__import__", "import_module", "run_path", "exec_module"):
                if any(isinstance(a, ast.Constant) and isinstance(a.value, str)
                       and any(n in a.value for n in NEVER_IMPORTED) for a in node.args):
                    bad.append(fn)
    return bad


def leg_const(model, out) -> bool:
    L = Leg("F-BC-CONST", "the table's BOX_BYTES / FLAG_BYTES (and SCOPE, TICK_EXTRA, SUBJECT, "
            "WORKFLOW_*) differ from a FRESH AST read of the files NOW; or publish_exchange / "
            "backup_estate was imported; or an assignment is duplicated or non-literal", out)
    mc = model["constants"]
    fresh = _fresh_const_read(ROOT / REL_PUBLISH, PUBLISH_NAMES)
    fresh.update(_fresh_const_read(ROOT / REL_BACKUP, BACKUP_NAMES))
    v = const_violations(mc, fresh)
    L.control("fresh AST read == the table's constants", not v,
              f"BOX_BYTES {fresh['BOX_BYTES']:,} · FLAG_BYTES {fresh['FLAG_BYTES']:,} · "
              f"SCOPE {fresh['SCOPE']!r} · TICK_EXTRA {list(fresh['TICK_EXTRA'])} · "
              f"{len(fresh['WORKFLOW_SOURCES'])} workflow roots"
              + (f" · MISMATCH {v}" if v else ""))
    loaded = [n for n in NEVER_IMPORTED if n in sys.modules]
    src_bad = import_violations(Path(__file__).read_text(encoding="utf-8"))
    L.control("never imported (sys.modules + this source)", not loaded and not src_bad,
              f"in sys.modules {loaded} · import statements {src_bad}")
    # the % in a real box-bound row recomputes from the fresh BOX_BYTES
    rp = next(r for r in model["rows"] if r["box_bound"])
    L.control("a row's % recomputes from the fresh BOX_BYTES",
              f"{100.0 * rp['bytes'] / fresh['BOX_BYTES']:.3f}%" in rp["box_cost"],
              f"`{rp['path']}`")
    # sabotages
    bent = copy.deepcopy(mc)
    bent["BOX_BYTES"]["value"] = 16_000_001
    L.sabotage("BOX_BYTES typed 16_000_001 into the table", bool(const_violations(bent, fresh)))
    src = (ROOT / REL_PUBLISH).read_text(encoding="utf-8")

    def bend(name, text):
        """the source with the line that assigns `name` (its AST line) replaced."""
        lines = src.splitlines(True)
        ln = int(mc[name]["source"].rsplit(":", 1)[1])
        lines[ln - 1] = text + "\n"
        return "".join(lines)

    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "publish_exchange.py"
        p.write_text(bend("BOX_BYTES", "BOX_BYTES = 16_000_001"), encoding="utf-8")
        f2 = _fresh_const_read(p, PUBLISH_NAMES)
        L.sabotage("a copy of publish_exchange carrying BOX_BYTES = 16_000_001",
                   "BOX_BYTES" in const_violations(mc, f2))
        p.write_text(src + f"\nFLAG_BYTES = {mc['FLAG_BYTES']['value']}\n", encoding="utf-8")
        red1 = red2 = False
        try:
            read_literals(p, PUBLISH_NAMES)
        except ConstRefused:
            red1 = True
        try:
            _fresh_const_read(p, PUBLISH_NAMES)
        except ConstRefused:
            red2 = True
        L.sabotage("a duplicated FLAG_BYTES assignment", red1 and red2,
                   "both readers refuse")
        p.write_text(bend("FLAG_BYTES", "FLAG_BYTES = int('64000')"), encoding="utf-8")
        red = False
        try:
            read_literals(p, PUBLISH_NAMES)
        except ConstRefused:
            red = True
        L.sabotage("a non-literal FLAG_BYTES", red)
    planted = Path(__file__).read_text(encoding="utf-8") + "\nimport publish_exchange\n"
    L.sabotage("a planted `import publish_exchange` in a source copy",
               bool(import_violations(planted)))
    return L.verdict()


def coverage_violations(model, exp_paths: set, prog: dict) -> list:
    rows = model["rows"]
    bad = []
    a_paths = {r["path"] for r in rows if r["group"] == "a"}
    for p in sorted(exp_paths - a_paths):
        bad.append(f"tierc10-commit path missing: {p}")
    file_rows = {r["path"] for r in rows if r["kind"] == "file"}
    cells = [r for r in rows if r["kind"] == "cells-dir"]
    file_dirs = {p.rsplit("/", 1)[0] for p in file_rows}
    for d in sorted({p.rsplit("/", 1)[0] for p in prog}):
        if d in file_dirs:
            continue
        if not any(d == c["path"] or d.startswith(c["path"] + "/") for c in cells):
            bad.append(f"PROGRESS artifact directory missing: {d}")
    for p in sorted(prog):
        if collapse_root(p) is None and not _is_or1(p) and p not in file_rows:
            bad.append(f"PROGRESS artifact missing: {p}")
    for c in cells:
        n = sum(1 for p in prog if p.startswith(c["path"] + "/"))
        if n != c.get("n_recorded"):
            bad.append(f"collapsed count {c['path']}: row {c.get('n_recorded')} != PROGRESS {n}")
    for g in ("c", "d"):
        if not any(r["group"] == g for r in rows):
            bad.append(f"row ({g}) missing")
    return bad


def _expected_commit_paths() -> set:
    """Independent of tierc10_commits(): its own git log, its own parse."""
    _, out = _git(["log", "--grep=^tierc10", "--name-only", "--format=%x01%s"])
    exp, keep = set(), False
    for ln in out.split("\n"):
        if ln.startswith("\x01"):
            keep = ln[1:].startswith("tierc10")
        elif ln.strip() and keep:
            exp.add(ln)
    return exp


def leg_cover(model, out) -> bool:
    L = Leg("F-BC-COVER", "any tierc10-commit path, any PROGRESS artifact outside a cells root, "
            "or any PROGRESS artifact DIRECTORY has no row; a collapsed row's count disagrees "
            "with PROGRESS; or the PLANNED (c) or snapshot (d) row is missing", out)
    exp = _expected_commit_paths()
    prog = json.loads((ROOT / REL_PROGRESS).read_text(encoding="utf-8"))
    prog = {p for s in prog["stages"] for p in (s.get("artifact_shas") or {})}
    ndirs = len({p.rsplit("/", 1)[0] for p in prog})
    v = coverage_violations(model, exp, prog)
    L.control("every commit path, artifact, artifact directory and (c)/(d) has its row", not v,
              f"{len(exp)} commit paths · {len(prog)} PROGRESS artifacts in {ndirs} directories"
              + (f" · {v[:3]}" if v else ""))

    def drop(pred):
        m2 = copy.deepcopy(model)
        i = next(i for i, r in enumerate(m2["rows"]) if pred(r))
        gone = m2["rows"].pop(i)["path"]
        return m2, gone

    m2, gone = drop(lambda r: r["group"] == "a")
    L.sabotage("drop one (a) row", bool(coverage_violations(m2, exp, prog)), f"`{gone}`")
    m2, gone = drop(lambda r: r["group"] == "b")
    L.sabotage("drop one (b) row", bool(coverage_violations(m2, exp, prog)), f"`{gone}`")
    m2, gone = drop(lambda r: r["kind"] == "cells-dir" and r["path"].endswith("census/cells"))
    vv = coverage_violations(m2, exp, prog)
    L.sabotage("drop the census/cells row (whole artifact directories vanish)",
               any("directory missing" in x for x in vv),
               f"{sum('directory missing' in x for x in vv)} directories uncovered")
    m2 = copy.deepcopy(model)
    cr = next(r for r in m2["rows"] if r["kind"] == "cells-dir")
    cr["n_recorded"] -= 1
    L.sabotage("bend a collapsed row's count by one", bool(coverage_violations(m2, exp, prog)))
    m2, gone = drop(lambda r: r["group"] == "c")
    L.sabotage("drop the PLANNED (c) row", bool(coverage_violations(m2, exp, prog)))
    return L.verdict()


def flag_violations(rows, consts, root: Path = ROOT) -> list:
    """Bytes RE-MEASURED here, never trusted from the row."""
    flag = _cv(consts, "FLAG_BYTES")
    scope, tick = _cv(consts, "SCOPE"), _cv(consts, "TICK_EXTRA")
    bad = []
    for r in rows:
        if r["kind"] == "snapshot":
            continue
        p = r["path"]
        should_bound = p.startswith(scope) or p in tick
        if should_bound and not r["box_bound"]:
            bad.append(f"{p}: box-bound path classed unsynced")
            continue
        if not r["box_bound"]:
            continue
        if r["kind"] == "planned" and r.get("sizing") != "filed":
            nb = sum(disk_size(root, c["path"]) or 0 for c in r["components"])
        else:
            nb = disk_size(root, p)
        if nb is None:
            bad.append(f"{p}: box-bound and absent")
            continue
        must = nb > flag
        said = (r["bytes"] or 0) > flag
        if r["flagged"] != said or ("FLAGGED" in r["box_cost"]) != r["flagged"]:
            bad.append(f"{p}: the row's own {r['bytes']:,} B and its flag disagree")
        if r["flagged"] != must:
            bad.append(f"{p}: {nb:,} B on disk, row {'unflagged' if must else 'flagged'}"
                       + (f" (row recorded {r['bytes']:,} B)" if r["bytes"] != nb else ""))
    return bad


def leg_flag(model, out) -> bool:
    c = model["constants"]
    flag = _cv(c, "FLAG_BYTES")
    L = Leg("F-BC-FLAG", f"a box-bound path over FLAG_BYTES ({flag:,} B, read by AST) is "
            "unflagged — bytes re-measured from disk, not trusted from the row — or a flag "
            "fires at/under the wire, or an exchange/ path is classed unsynced", out)
    v = flag_violations(model["rows"], c)
    nb = sum(1 for r in model["rows"] if r["box_bound"])
    L.control("every box-bound row flagged iff strictly over the wire", not v,
              f"{nb} box-bound rows re-measured" + (f" · {v}" if v else ""))
    with tempfile.TemporaryDirectory() as td:
        troot = Path(td)
        (troot / "exchange" / "reports").mkdir(parents=True)
        at, over = "exchange/reports/_WIRE_AT.md", "exchange/reports/_WIRE_OVER.md"
        (troot / at).write_bytes(b"x" * flag)
        (troot / over).write_bytes(b"x" * (flag + 1))

        def trow(rel, **kw):
            nbytes = disk_size(troot, rel)
            r = {"kind": "file", "path": rel, "bytes": nbytes}
            r.update(box_fields(rel, nbytes, c, **kw))
            return r

        ra, ro = trow(at), trow(over)
        L.control(f"boundary: a {flag:,} B temp file is NOT flagged, a {flag + 1:,} B one IS",
                  (not ra["flagged"]) and ro["flagged"]
                  and not flag_violations([ra, ro], c, troot))
        s1 = trow(over)
        s1["flagged"] = False
        s1["box_cost"] = s1["box_cost"].replace("**FLAGGED**", "under")
        L.sabotage(f"a {flag + 1:,} B temp file listed unflagged",
                   bool(flag_violations([s1], c, troot)))
        s2 = trow(over, flag_limit=flag + 1_000)
        L.sabotage(f"the same file through a flagger bent to {flag + 1_000:,} B",
                   bool(flag_violations([s2], c, troot)))
        s3 = trow(over)
        s3["bytes"] = flag
        s3.update(box_fields(over, flag, c))
        L.sabotage(f"the same file recorded stale at {flag:,} B (disk holds {flag + 1:,})",
                   bool(flag_violations([s3], c, troot)))
        s4 = trow(over)
        s4.update({"box_bound": False, "flagged": False, "box_cost": "n/a — unsynced"})
        L.sabotage("the same exchange/ file classed unsynced",
                   bool(flag_violations([s4], c, troot)))
    return L.verdict()


_SPAWN_ATTRS = {("os", "system"), ("os", "popen"), ("os", "execv"), ("os", "execvp"),
                ("os", "execl"), ("os", "execlp"), ("os", "spawnv"), ("os", "spawnl"),
                ("os", "posix_spawn"), ("os", "posix_spawnp"), ("pty", "spawn")}


def static_git_violations(src: str) -> list:
    tree = ast.parse(src)
    bad = []
    gate_fn = None
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "_git":
            gate_fn = node
    inside = set()
    if gate_fn is not None:
        inside = {id(n) for n in ast.walk(gate_fn)}
        # the gate must be consulted BEFORE the process is spawned
        order = []
        for i, st in enumerate(gate_fn.body):
            names = {getattr(n.func, "id", getattr(n.func, "attr", None))
                     for n in ast.walk(st) if isinstance(n, ast.Call)}
            if "git_verb_ok" in names:
                order.append(("gate", i))
            if "run" in names:
                order.append(("spawn", i))
        gi = [i for k, i in order if k == "gate"]
        si = [i for k, i in order if k == "spawn"]
        if not gi or not si or min(gi) > min(si):
            bad.append("_git does not consult git_verb_ok before spawning")
    else:
        bad.append("no _git choke point")
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and node.id == "subprocess" and id(node) not in inside:
            bad.append(f"line {node.lineno}: `subprocess` referenced outside _git")
        if isinstance(node, ast.Call):
            f = node.func
            if isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name) \
                    and (f.value.id, f.attr) in _SPAWN_ATTRS:
                bad.append(f"line {node.lineno}: {f.value.id}.{f.attr} spawns a process")
            if isinstance(f, ast.Name) and f.id == "_git":
                a0 = node.args[0] if node.args else None
                if not isinstance(a0, (ast.List, ast.Tuple)) or not a0.elts \
                        or not isinstance(a0.elts[0], ast.Constant):
                    bad.append(f"line {node.lineno}: _git called with a non-literal verb")
                    continue
                lit = [e.value if isinstance(e, ast.Constant) else "<expr>" for e in a0.elts]
                if lit[0] == "branch":
                    ok = tuple(lit[:3]) == BRANCH_FORM and len(lit) == 4
                else:
                    ok = git_verb_ok(lit)[0]
                if not ok:
                    bad.append(f"line {node.lineno}: _git({lit[:3]}…) outside the allowed verbs")
    return bad


def leg_git(out) -> bool:
    L = Leg("F-BC-GIT", "any git invocation this run made (recorded at `_git` BEFORE it runs) "
            "uses a verb outside {log, ls-files, check-ignore, branch -r --contains, rev-parse}, "
            "or `log --output`; or this source calls `_git` with a non-literal / disallowed "
            "verb, spawns a process outside `_git`, or spawns before the gate", out)
    calls = list(GIT_CALLS)
    v = git_call_violations(calls)
    L.control("every recorded git call is an allowed verb (all builds, all legs)", not v,
              "one build = " + " · ".join(f"{k} {n}" for k, n in
                                          git_verb_census(ONE_BUILD_CALLS).items())
              + (f" · VIOLATIONS {v[:3]}" if v else ""))
    src = Path(__file__).read_text(encoding="utf-8")
    sv = static_git_violations(src)
    L.control("static: this source's `_git` calls and process spawns", not sv,
              "; ".join(sv[:3]))
    plant = "a" + "dd"
    L.sabotage(f"plant '{plant}' in the call record",
               bool(git_call_violations(calls + [(plant, "--", REL_CLOSE)])))
    L.sabotage("plant `branch -a` in the call record",
               bool(git_call_violations(calls + [("branch", "-a")])))
    L.sabotage("plant `push` in the call record",
               bool(git_call_violations(calls + [("push", "origin", "HEAD")])))
    L.sabotage("plant `log --output=x` in the call record",
               bool(git_call_violations(calls + [("log", "--output=x")])))
    L.sabotage(f"plant `_git([\"{plant}\", \"-A\"])` in a source copy",
               bool(static_git_violations(
                   src + f"\n\ndef _planted():\n    return _git([\"{plant}\", \"-A\"])\n")))
    L.sabotage("plant a raw `subprocess.run([\"git\", \"" + plant + "\", \".\"])` in a source copy",
               bool(static_git_violations(
                   src + "\n\ndef _planted():\n    return subprocess.run([\"git\", \""
                   + plant + "\", \".\"])\n")))
    return L.verdict()


def volatile_violations(model) -> list:
    named = set(model["volatile"]["git"])
    need = {c for c, s in model["column_source"].items() if "git" in s} | set(TOP_GIT_FIELDS)
    namedd = set(model["volatile"]["disk"])
    needd = {c for c, s in model["column_source"].items() if "disk" in s}
    return sorted((need - named) | (needd - namedd))


def leg_det(model, md: bytes, js: bytes, m2, quiet: bool, out) -> bool:
    L = Leg("F-DET", "two whole builds in one process, taken while every input held still "
            "(HEAD, upstream, and the stat of every input path — the named-volatile inputs), "
            "differ by a byte (MD or JSON); or the inputs never held still; or the outputs "
            "carry a temp path; or a git/disk-sourced field is not NAMED volatile", out)
    L.control("the input fingerprint held still across both builds", quiet,
              "" if quiet else f"moved on every one of {QUIET_TRIES} attempts — the table "
              "cannot be proven deterministic while other writers are active")
    md2, js2 = render(m2)
    L.control("second whole build: MD byte-identical", md == md2,
              f"sha256 {hashlib.sha256(md).hexdigest()[:16]}…")
    L.control("second whole build: JSON byte-identical", js == js2,
              f"sha256 {hashlib.sha256(js).hexdigest()[:16]}…")
    tmp = tempfile.gettempdir()
    L.control("no temp path in the outputs", tmp.encode() not in md + js)
    vv = volatile_violations(model)
    L.control("every git/disk-sourced field is named volatile", not vv,
              f"git {len(model['volatile']['git'])} · disk {len(model['volatile']['disk'])}")
    import datetime as _dt
    m3 = copy.deepcopy(m2)
    m3["header"] = m3["header"] + " · " + _dt.datetime.now(_dt.timezone.utc).isoformat()
    L.sabotage("a wall clock injected into the second render", render(m3)[0] != md)
    m4 = copy.deepcopy(model)
    m4["volatile"]["git"] = [x for x in m4["volatile"]["git"] if x != "PUSHED"]
    L.sabotage("PUSHED dropped from the named-volatile list", bool(volatile_violations(m4)))
    return L.verdict()


# ──────────────────────────────────────────────────────────── main
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out-dir", default=str(ROOT / REL_CLOSE))
    args = ap.parse_args(argv)
    out_dir = Path(args.out_dir).expanduser().resolve()
    canonical = (ROOT / REL_CLOSE).resolve()
    if out_dir != canonical and (out_dir == ROOT.resolve() or ROOT.resolve() in out_dir.parents):
        raise SystemExit(f"HALT: --out-dir {out_dir} is inside the repo but is not {REL_CLOSE}")

    T: list = []

    def out(s=""):
        T.append(s)
        print(s)

    try:
        consts = load_constants()
    except ConstRefused as e:
        raise SystemExit(f"HALT: constants — {e}")
    model, twin, quiet = stable_build(consts)
    md, js = render(model)
    S = model["summary"]
    out(f"TIER-C10 · CLOSE · BOX-COST — FIXTURES ({REL_SELF})")
    out(f"{HEADER}")
    out(f"{LABEL}")
    out(f"substrate NAIAD_CACHE_DIR={SNAPSHOT} (guarded) · bytecode off · no bar read · "
        f"no randomness")
    out(f"constants (AST, never imported): BOX_BYTES {_cv(consts, 'BOX_BYTES'):,} "
        f"[{consts['BOX_BYTES']['source']}] · FLAG_BYTES {_cv(consts, 'FLAG_BYTES'):,} "
        f"[{consts['FLAG_BYTES']['source']}] · SCOPE {_cv(consts, 'SCOPE')!r} · TICK_EXTRA "
        f"{_cv(consts, 'TICK_EXTRA')}")
    g = model["git"]
    out(f"git (volatile): HEAD {g['head']} · {g['branch']} · upstream {g['upstream']} "
        f"{g['upstream_tip']} · ahead {g['ahead']} · tierc10 commits "
        f"{S['tierc10_commits_pushed']}/{S['tierc10_commits']} pushed · no fetch")
    out("table: " + " · ".join(f"({k}) {v}" for k, v in S["rows"].items())
        + f" · box-bound {len(S['box_bound_rows'])} ({S['box_bound_bytes']:,} B) · "
        f"FLAGGED {len(S['flagged_rows'])}")
    out("")
    verdicts = {}
    verdicts["F-BC-CONST"] = leg_const(model, out)
    out("")
    verdicts["F-BC-COVER"] = leg_cover(model, out)
    out("")
    verdicts["F-BC-FLAG"] = leg_flag(model, out)
    out("")
    verdicts["F-DET"] = leg_det(model, md, js, twin, quiet, out)
    out("")
    verdicts["F-BC-GIT"] = leg_git(out)       # last: judges every call the run made
    out("")
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / MD_NAME).write_bytes(md)
    (out_dir / JSON_NAME).write_bytes(js)
    for name, b in ((MD_NAME, md), (JSON_NAME, js)):
        out(f"OUTPUT {name} · {len(b):,} B · sha256 {hashlib.sha256(b).hexdigest()}")
    n_ok = sum(verdicts.values())
    out(f"SUMMARY {n_ok}/{len(verdicts)} GREEN · "
        + " · ".join(f"{k} {'GREEN' if v else 'RED'}" for k, v in verdicts.items()))
    rc = 0 if n_ok == len(verdicts) else 1
    out(f"EXIT {rc}")
    (out_dir / FIX_NAME).write_bytes(("\n".join(T) + "\n").encode("utf-8"))
    return rc


if __name__ == "__main__":
    sys.exit(main())
