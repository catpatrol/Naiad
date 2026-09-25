#!/usr/bin/env python
"""TIER-C11 · TC11-FIX — F-CLOSURE-ALL · F-HOOK-ESCAPE-ALL · F-DET.  L-F.2 over the WHOLE DECISION
set and the lineage, and AM-2 / AM-8 over every non-fixture tierc11 module [final review
2026-09-25: fidelity MINOR-5, reproducibility MINOR-6; TC11-FIX verify MINOR-2, -3, -4].

The earlier closure legs (F-CLOSURE-ENV, F-CLOSURE-RIDE, the scorer's F-CLOSURE, the T-brk decision
functions) each covered ONE module and never AST-scanned the lineage.  This suite covers them all:

  THE DECISION SET [L-F.2] = every non-fixture scripts/tierc11_*.py EXCEPT tierc11_nest and the
  runners that legitimately import it.  The runners are TYPED here (RUNNERS_T: stage_a, stage_h,
  stage_r, stage_r4, stage_t_brk) and each exemption must be EARNED — the runner's source must
  import tierc11_nest, or the exemption is a hole.  A module this file does not name (a new
  tierc11 module) defaults to the DECISION set and is scanned.

  THE LINEAGE [L-F.2 "tierc2_rules … tierc9 stays range-blind"] = the STATIC repo closure of the
  DECISION set: every repo-local module (scripts/, engine/, analytics/, …) named by an import of a
  DECISION module or of a lineage module, anywhere in its source (function bodies included), plus
  every module a lineage module imports by a NAME HELD IN DATA (`__import__(name)` over a literal
  table — tierc6/tierc7's labs), transitively.  tierc11_* modules are the DECISION set's business;
  tierc10_* modules are TC10's layer, which L-0.3 re-uses and whose range paths L-0.3 routes
  through tierc11_nest — they are disclosed, not walked.  The walk must hold the fifteen tierc2..9
  modules tierc11_env's import windows load (LINEAGE_ENV_T, typed), and every repo module a fresh
  interpreter actually loads must be in it (the static walk cannot be narrower than the runtime).

  F-CLOSURE-ALL     FAILS IF a fresh interpreter importing ANY DECISION module (one interpreter
                    per module) holds a module whose name contains rangefinder / tierc10_census /
                    tierc10_stamps / tierc10_null / tierc11_nest, or loads the module from anywhere
                    but scripts/<name>.py; this file's own AST walk of any DECISION or LINEAGE source
                    finds such an import (Import / ImportFrom anywhere, function bodies included; a
                    constant-string import_module / __import__ / tc10_import call; a lineage
                    name-held dynamic import), a sys.modules reach of one, a Range.top/.bottom read
                    (an attribute .top / .bottom anywhere, getattr / hasattr / attrgetter with
                    'top' / 'bottom', or a namespace-dict read x.__dict__['top'] / vars(x)['bottom']
                    / .get('top')), a non-constant import site in a DECISION module other than the
                    declared nest-only door (tierc11_env.tc10_import), an exec / eval / compile
                    call in a DECISION module (code built at run time: an UNDECLARED dynamic site,
                    none is declared), or an unresolved non-constant import site in the lineage;
                    a typed runner does not import
                    tierc11_nest (EXEMPTION UNEARNED); the walk misses one of LINEAGE_ENV_T or a
                    repo module a fresh interpreter loaded.  SABOTAGE: two shadow modules with a
                    top-level range import under a fresh interpreter; lazy / constant-string /
                    sys.modules / name-held-dynamic imports, .top and getattr 'bottom' reads planted
                    in DECISION sources; a new tierc11 module importing tierc11_nest; lazy imports
                    and a .bottom read planted in LINEAGE sources, one of them in a lab reachable
                    only through tierc7's name-held __import__; a runner without its nest import;
                    exec('import tierc10_census') in a DECISION function; r.__dict__['top'] and
                    vars(r)['bottom'] in DECISION sources.
  F-HOOK-ESCAPE-ALL FAILS IF E.hook_escapes finds, in ANY non-fixture tierc11 module (nest and the
                    runners included), pyarrow-native I/O, an os-level out-of-process call or an
                    fd / filesystem / partition_cols keyword; subprocess is imported (or reached by
                    an import call) by any module but the three AM-8 names; or, in an AM-8 module,
                    a subprocess call's argv is not a literal list whose head is that module's named
                    use (tierc11_data: `cp` with `-cpR`; tierc11_data_clock_note: `git` with `show`;
                    tierc11_worktree_attest: `git`), a call passes shell=True, or a subprocess
                    function is referenced outside a checked call; an AM-8 module holds other than
                    its ONE pinned call site (AM8_SITE_T: the enclosing function and the argv as
                    ast.unparse renders it), or a destination argv element (cp's last; every
                    element of a git argv) resolves — through the enclosing function's and the
                    module's assignments — into research_outputs/tierc10[_run2] or the TC10
                    snapshot; the attestation's git([...]) helper passes a subcommand outside the
                    typed {worktree, rev-parse, status, show} (ATTEST_GIT_T, LEANS_AMENDMENTS.md
                    AM-8), a non-literal argv, or is held as a value.  SABOTAGE: a subprocess call
                    in a non-AM-8 module (import, from-import, import_module('subprocess')); a
                    `curl` argv, a non-literal argv (the removed one-shot mode), shell=True and a
                    held `subprocess.run` value in AM-8 modules; pq.read_table, os.system and a
                    filesystem= keyword in three other modules; `git push` through the
                    attestation's helper; a `cp -cpR` into TC10_DATA; a second well-formed `git
                    show` site.
  F-DET             FAILS IF two subprocess emissions of CLOSURE_PROBE.txt (PYTHONHASHSEED 1,
                    20260924) differ from each other or from this run's bytes, or either exits
                    nonzero.  SABOTAGE: a one-byte-bent copy; a hash-order-dependent emission.

TWO LEGS PER FIXTURE, the BREAK leg first, and it must go RED or the fixture is VOID [the prove()
law of scripts/tierc10_rf_fixtures.py / tierc11_ride_fixtures.py].  A break leg is a set of PLANTS
judged one at a time; a plant counts as CAUGHT only if a finding NAMES THE INTENDED DETECTOR (its
expected substring).  A plant that crashes is a FIXTURE DEFECT, never a catch.  Every plant is made
on a COPY of a source held in memory, or on a shadow module written under
RUN_ROOT/_det_closure/shadow and removed; no source of record moves.  The detectors are THIS file's
AST walk (a second object) plus E.hook_escapes (the AM-2 scanner of record, named by AM-8).
BANNED: self-comparison; one example where cardinality was possible; a check whose claim is not
the design's claim.  FROZEN SUBSTRATE: HALTs unless NAIAD_CACHE_DIR is the TC11 snapshot
(tierc11_env's guard).  Seed 20260924.  The transcript carries no clock, no temp path, no line
number (a GREEN scan prints none; a planted finding's prints as `line #` — a benign edit to a
scanned module does not move the record) and no registered number.

Run:  export NAIAD_CACHE_DIR=$HOME/.cache/naiad/snapshots/tc11_20260925 PYTHONDONTWRITEBYTECODE=1
      ~/venvs/naiad/bin/python -B scripts/tierc11_closure_fixtures.py \\
          [leg-substring ...] [--refile-transcript] [--root=DIR]
Exit 0 = every leg GREEN, every break RED · 1 = a RED or VOID fixture, a transcript finding, or
a HALT.
"""
from __future__ import annotations

import ast
import functools
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
import tierc11_env as E                                              # noqa: E402  (guards first)

# ── FIXTURE-TYPED LITERALS: the commission, a second object, never a module's own ──
PIN = 1_790_294_400_000                  # 2026-09-25T00:00:00Z [L-0.1]
SEED = 20260924
DET_SEEDS = (1, SEED)
AS_OF_LINE = "as_of_last_closed_4h: 2026-09-25T00:00:00Z"
SNAP = Path.home() / ".cache" / "naiad" / "snapshots" / "tc11_20260925"
SCRIPTS = ROOT / "scripts"
FORBIDDEN = ("rangefinder", "tierc10_census", "tierc10_stamps", "tierc10_null", "tierc11_nest")
NEST = "tierc11_nest"
RUNNERS_T = ("tierc11_stage_a", "tierc11_stage_h", "tierc11_stage_r", "tierc11_stage_r4",
             "tierc11_stage_t_brk")
LINEAGE_ENV_T = ("tierc2_baseline", "tierc2_rules", "tierc3_baseline", "tierc3_rules",
                 "tierc4_baseline", "tierc4_rules", "tierc5", "tierc5_rules", "tierc6",
                 "tierc6_rules", "tierc7", "tierc7_lab_regime", "tierc7_rules", "tierc8", "tierc9")
# AM-8: the three non-fixture subprocess uses allowed BY NAME — (argv head, constants the argv
# must also hold, what it is).
AM8_T = {"tierc11_data": ("cp", ("-cpR",), "the APFS clone of the TC10 snapshot (TC11-D --clone)"),
         "tierc11_data_clock_note": ("git", ("show",), "git show e97ad73:<path>, a read of the "
                                                       "committed record"),
         "tierc11_worktree_attest": ("git", (), "git worktree / rev-parse / status / show for "
                                                "L-F.3")}
# AM-8, pinned [TC11-FIX verify MINOR-3]: the ONE subprocess call site each AM-8 module may hold —
# (the enclosing function, the argv exactly as ast.unparse renders it, the destination's argv
# index or None when the use writes nothing).
AM8_SITE_T = {"tierc11_data": ("clone_snapshot", "['cp', '-cpR', str(TC10_SNAPSHOT), str(SNAPSHOT)]", -1),
              "tierc11_data_clock_note": ("git_blob", "['git', '-C', str(ROOT), 'show', f'{rev}:{rel}']",
                                          None),
              "tierc11_worktree_attest": ("git", "['git', *args]", None)}
# AM-8, typed [TC11-FIX verify MINOR-2]: the git subcommands tierc11_worktree_attest may pass
# through its git([...]) helper — LEANS_AMENDMENTS.md AM-8 "No other git subcommand is allowed".
ATTEST_GIT_T = frozenset({"worktree", "rev-parse", "status", "show"})
# a path into TC10's space: research_outputs/tierc10[_run2] or the TC10 snapshot
TC10_DEST_RX = re.compile(r"(^|/)tierc10(_run2)?(/|$)|tc10_20260921")
DYN_DECLARED_T = (("tierc11_env", "tc10_import"),)   # the nest-only door (F-CLOSURE-ENV)
DYN_FUNCS = frozenset({"import_module", "__import__", "tc10_import", "_tc10_import"})
# code built at run time [TC11-FIX verify MINOR-4]: exec / eval / compile in a DECISION module
# is an UNDECLARED dynamic site (none is declared)
EXEC_FUNCS = frozenset({"exec", "eval", "compile"})
TOPBOT = ("top", "bottom")
TOPBOT_CALLS = frozenset({"getattr", "hasattr", "setattr", "delattr", "attrgetter"})
SP_CALLS = frozenset({"run", "call", "check_call", "check_output", "Popen", "getoutput",
                      "getstatusoutput"})
SP_SAFE = frozenset({"PIPE", "DEVNULL", "STDOUT", "CalledProcessError", "TimeoutExpired",
                     "CompletedProcess", "SubprocessError"})
MOD_RX = re.compile(r"[A-Za-z_][A-Za-z0-9_]*(\.[A-Za-z_][A-Za-z0-9_]*)*")
OUT = ROOT / "research_outputs" / "tierc11" / "closure"
RUN_ROOT = OUT
TRANSCRIPT = "FIXTURES_CLOSURE.txt"
ARTIFACT = "CLOSURE_PROBE.txt"
PY = sys.executable
LINES: list[str] = []
PASSED: list[str] = []
FAILED: list[str] = []
_C: dict = {}
_TMP_RX = re.compile(r"(/private)?/(var/folders|tmp)/[^\s'\"]+")
_LINE_RX = re.compile(r"\bline \d+")


def say(line: str = "") -> None:            # deterministic -> transcript
    line = _TMP_RX.sub("<tmp>", line)
    print(line)
    LINES.append(line)


def clock(line: str) -> None:               # wall clock, temp paths -> stdout ONLY
    print(f"  [clock · stdout only] {line}")


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def prove(fid: str, title: str, break_if: str, real_if: str, break_leg, real_leg) -> None:
    """Break first; it must go RED (ok False) or the fixture is VOID."""
    say(f"\n{fid} — {title}")
    say(f"  [BREAK] FAILS IF: {break_if}")
    try:
        b_ok, b_why = break_leg()
    except Exception as e:                  # a break leg that errors proved nothing
        b_ok, b_why = True, f"break leg RAISED {type(e).__name__}: {e}"
    say(f"  [BREAK] deliberate violation -> "
        f"{'RED (correct)' if not b_ok else 'GREEN (FIXTURE IS VOID)'}: {b_why}")
    say(f"  [REAL]  FAILS IF: {real_if}")
    try:
        r_ok, r_why = real_leg()
    except Exception as e:                  # a real leg that errors is a FAIL
        r_ok, r_why = False, f"raised {type(e).__name__}: {e}"
    say(f"  [{'PASS' if r_ok else 'FAIL'}] {fid}: {r_why}")
    if b_ok:
        FAILED.append(f"{fid} (break leg did not go RED — fixture proves nothing)")
    elif not r_ok:
        FAILED.append(fid)
    else:
        PASSED.append(fid)


def plants(rows) -> tuple[bool, str]:
    """rows = (name, expected detector substring, thunk -> list of findings).  Judged ONE AT A
    TIME.  CAUGHT only if a finding names the intended detector.  No finding = the plant PASSED
    (VOID); a finding without the substring = the WRONG detector (VOID); a crash = a FIXTURE
    DEFECT (VOID).  A HALT is a finding (it carries its own text)."""
    passed, wrong, caught, crashed = [], [], [], []
    for name, want, thunk in rows:
        try:
            found = thunk()
        except SystemExit as e:
            found = [str(e) if str(e).startswith("HALT") else f"HALT: {e}"]
        except Exception as e:
            crashed.append(f"{name} -> RAISED {type(e).__name__}: {e}")
            continue
        if not found:
            passed.append(name)
        elif not any(want in str(f) for f in found):
            wrong.append(f"{name} -> {str(found[0])[:160]} (wanted {want!r})")
        else:
            hit = next(str(f) for f in found if want in str(f))
            i = hit.index(want)
            shown = hit[:170] if i + len(want) <= 170 else (hit[:60] + " … " + hit[i:i + 150])
            shown = _LINE_RX.sub("line #", shown)   # a planted line's number moves with any edit
            caught.append(f"{name} [{len(found)} finding(s)] -> {shown}")
    if crashed:
        return True, (f"{len(crashed)} plant(s) CRASHED — a FIXTURE DEFECT, not a "
                      f"finding: " + " · ".join(crashed))
    if passed or wrong:
        return True, (f"{len(passed)} plant(s) PASSED {passed}; {len(wrong)} caught by the "
                      f"WRONG detector {wrong}")
    return False, (f"all {len(caught)} plants caught by their named detector, one at a "
                   f"time: " + " · ".join(caught))


def forbidden(name: str) -> bool:
    return any(f in name for f in FORBIDDEN)


# ═════════════════════════════════════════════════════════════ THE SOURCES
def tierc11_names() -> list[str]:
    """Every non-fixture scripts/tierc11_*.py, by module name."""
    return sorted(p.stem for p in SCRIPTS.glob("tierc11_*.py") if not p.stem.endswith("_fixtures"))


def module_file(name: str) -> Path | None:
    """The repo file a module name resolves to (scripts/ first, then the repo root), or None
    (stdlib / third-party / absent)."""
    if not MOD_RX.fullmatch(name or ""):
        return None
    rel = name.replace(".", "/")
    for base in (SCRIPTS, ROOT):
        for p in (base / f"{rel}.py", base / rel / "__init__.py"):
            if p.is_file():
                return p
    return None


def rel_of(p: Path) -> str:
    return p.resolve().relative_to(ROOT.resolve()).as_posix()


def read(name: str, over: dict | None = None) -> str:
    if over and name in over:
        return over[name]
    p = module_file(name)
    if p is None:
        raise RuntimeError(f"no source for {name}")
    return p.read_text(encoding="utf-8")


# ═════════════════════════════════════════════════════════ THIS FILE'S AST WALK
@functools.lru_cache(maxsize=None)
def _tree(src: str) -> ast.Module:
    """One parse per distinct source text (the trees are only read, never mutated)."""
    return ast.parse(src)


def _fn(call: ast.Call) -> str:
    f = call.func
    return f.attr if isinstance(f, ast.Attribute) else getattr(f, "id", "")


def _cstr(node) -> str | None:
    return node.value if isinstance(node, ast.Constant) and isinstance(node.value, str) else None


def walk_imports(tree) -> list[tuple[int, str]]:
    """Every module name the source can import: Import / ImportFrom nodes ANYWHERE (function
    bodies included), each from-import also as module.name, plus a constant first argument of
    import_module / __import__ / tc10_import / _tc10_import."""
    out = []
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            out += [(n.lineno, a.name) for a in n.names]
        elif isinstance(n, ast.ImportFrom):
            mod = "." * n.level + (n.module or "")
            out.append((n.lineno, mod))
            out += [(n.lineno, f"{mod}.{a.name}" if n.module else f"{mod}{a.name}")
                    for a in n.names]
        elif isinstance(n, ast.Call) and _fn(n) in DYN_FUNCS and n.args \
                and _cstr(n.args[0]) is not None:
            out.append((n.lineno, n.args[0].value))
    return out


def dyn_sites(tree) -> list[tuple[int, str, str, list[str]]]:
    """Every import call whose module name is NOT a constant: (line, function called, the
    enclosing function, the repo modules its name can be — the string constants of the
    enclosing function and of the module-level literals it names that resolve to a repo module)."""
    lits = {}
    for n in tree.body:
        if isinstance(n, ast.Assign):
            for t in n.targets:
                if isinstance(t, ast.Name):
                    lits[t.id] = n.value
    funcs = [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
    out = []
    for n in ast.walk(tree):
        if not (isinstance(n, ast.Call) and _fn(n) in DYN_FUNCS):
            continue
        if n.args and _cstr(n.args[0]) is not None:
            continue
        enc = [g for g in funcs if g.lineno <= n.lineno <= (g.end_lineno or g.lineno)]
        scope = min(enc, key=lambda g: (g.end_lineno or g.lineno) - g.lineno) if enc else tree
        strings = {c.value for c in ast.walk(scope) if _cstr(c) is not None}
        for nm in ast.walk(scope):
            if isinstance(nm, ast.Name) and nm.id in lits:
                strings |= {c.value for c in ast.walk(lits[nm.id]) if _cstr(c) is not None}
        targets = sorted(s for s in strings if module_file(s) is not None)
        out.append((n.lineno, _fn(n), getattr(scope, "name", "<module>"), targets))
    return out


def _is_nsdict(node) -> str | None:
    """'__dict__' for an `x.__dict__`, 'vars()' for a `vars(x)` call, else None."""
    if isinstance(node, ast.Attribute) and node.attr == "__dict__":
        return "__dict__"
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "vars":
        return "vars()"
    return None


def topbot_reads(tree) -> list[tuple[int, str]]:
    """.top / .bottom attributes; getattr-family calls naming 'top' / 'bottom'; and a namespace
    dict read of them — `x.__dict__['top']`, `vars(x)['bottom']`, `x.__dict__.get('top')`
    [TC11-FIX verify MINOR-4]."""
    out = []
    for n in ast.walk(tree):
        if isinstance(n, ast.Attribute) and n.attr in TOPBOT:
            out.append((n.lineno, f".{n.attr}"))
        elif isinstance(n, ast.Call) and _fn(n) in TOPBOT_CALLS:
            out += [(n.lineno, f"{_fn(n)}(…, {a.value!r})") for a in n.args if _cstr(a) in TOPBOT]
        elif isinstance(n, ast.Subscript) and (how := _is_nsdict(n.value)) \
                and _cstr(n.slice) in TOPBOT:
            out.append((n.lineno, f"{how}[{n.slice.value!r}]"))
        elif isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) \
                and n.func.attr in ("get", "pop", "setdefault") \
                and (how := _is_nsdict(n.func.value)) and n.args and _cstr(n.args[0]) in TOPBOT:
            out.append((n.lineno, f"{how}.{n.func.attr}({n.args[0].value!r})"))
    return out


def exec_sites(tree) -> list[tuple[int, str, str]]:
    """Every exec / eval / compile call (by name, or builtins.<name>): (line, function called,
    the enclosing function) [TC11-FIX verify MINOR-4]."""
    funcs = [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
    out = []
    for n in ast.walk(tree):
        if not isinstance(n, ast.Call):
            continue
        f = n.func
        name = (f.id if isinstance(f, ast.Name) and f.id in EXEC_FUNCS else
                f.attr if (isinstance(f, ast.Attribute) and f.attr in EXEC_FUNCS
                           and isinstance(f.value, ast.Name) and f.value.id == "builtins")
                else None)
        if name is None:
            continue
        enc = [g for g in funcs if g.lineno <= n.lineno <= (g.end_lineno or g.lineno)]
        scope = min(enc, key=lambda g: (g.end_lineno or g.lineno) - g.lineno) if enc else None
        out.append((n.lineno, name, getattr(scope, "name", "<module>")))
    return out


def _is_sys_modules(node) -> bool:
    return (isinstance(node, ast.Attribute) and node.attr == "modules"
            and isinstance(node.value, ast.Name) and node.value.id == "sys")


def sysmod_reach(tree) -> list[tuple[int, str]]:
    out = []
    for n in ast.walk(tree):
        s = None
        if isinstance(n, ast.Subscript) and _is_sys_modules(n.value):
            s = _cstr(n.slice)
        elif (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
              and n.func.attr in ("get", "pop", "setdefault") and _is_sys_modules(n.func.value)
              and n.args):
            s = _cstr(n.args[0])
        if s and forbidden(s):
            out.append((n.lineno, s))
    return out


def scan_source(name: str, src: str, role: str) -> list[str]:
    """L-F.2 on one source: forbidden imports anywhere, sys.modules reaches, Range.top/.bottom
    reads; DECISION: a non-constant import site other than the declared door; LINEAGE: a
    name-held dynamic import of a forbidden module, or one that resolves to nothing."""
    tree = _tree(src)
    out = [f"AST import [{role}] {name} line {ln}: {x}" for ln, x in walk_imports(tree)
           if forbidden(x)]
    out += [f"AST Range.top/.bottom read [{role}] {name} line {ln}: {how}"
            for ln, how in topbot_reads(tree)]
    out += [f"AST sys.modules reach [{role}] {name} line {ln}: {x}" for ln, x in sysmod_reach(tree)]
    if role == "DECISION":
        out += [f"AST UNDECLARED dynamic site [{role}] {name} line {ln}: {fn}(…) in {fun}() — code "
                f"built at run time" for ln, fn, fun in exec_sites(tree)]
    for ln, fn, fun, tg in dyn_sites(tree):
        if role == "DECISION":
            if (name, fun) not in DYN_DECLARED_T:
                out.append(f"AST UNDECLARED dynamic import [{role}] {name} line {ln}: "
                           f"{fn}(<non-constant>) in {fun}()")
        elif not tg:
            out.append(f"AST UNRESOLVED dynamic import [{role}] {name} line {ln}: "
                       f"{fn}(<non-constant>) in {fun}() names no repo module")
        else:
            out += [f"AST import [{role}] {name} line {ln}: {fn}({t!r}) name-held in {fun}()"
                    for t in tg if forbidden(t)]
    return out


def repo_candidates(x: str) -> list[str]:
    """The repo modules an import of `x` executes: the longest dotted prefix that resolves to a
    repo file, and each parent package of it that does."""
    parts = x.split(".")
    for k in range(len(parts), 0, -1):
        c = ".".join(parts[:k])
        if module_file(c) is not None:
            return [".".join(parts[:j]) for j in range(1, k + 1)
                    if module_file(".".join(parts[:j])) is not None]
    return []


def lineage_walk(decision: dict, over: dict | None = None) -> tuple[dict, dict, dict]:
    """The static repo closure of the DECISION sources: ({lineage module: src}, {tierc10 layer
    module: rel}, {lineage module: its name-held dynamic sites})."""
    queue = [x for src in decision.values() for _, x in walk_imports(_tree(src))]
    lineage, tc10, dyn, seen = {}, {}, {}, set()
    while queue:
        x = queue.pop(0)
        for c in repo_candidates(x):
            if c in seen or c in decision or c.startswith("tierc11_") or forbidden(c):
                continue
            seen.add(c)
            if c.startswith("tierc10_"):
                tc10[c] = rel_of(module_file(c))
                continue
            src = read(c, over)
            lineage[c] = src
            tree = _tree(src)
            queue += [y for _, y in walk_imports(tree)]
            ds = dyn_sites(tree)
            if ds:
                dyn[c] = ds
            queue += [t for _, _, _, tg in ds for t in tg]
    return dict(sorted(lineage.items())), dict(sorted(tc10.items())), dict(sorted(dyn.items()))


def runner_findings(names: list[str], over: dict | None = None) -> list[str]:
    out = []
    for r in RUNNERS_T:
        if r not in names:
            out.append(f"EXEMPTION UNEARNED: typed runner {r} does not exist")
            continue
        imps = [x for _, x in walk_imports(_tree(read(r, over)))]
        if not any(x == NEST or x.startswith(NEST + ".") for x in imps):
            out.append(f"EXEMPTION UNEARNED: runner {r} does not import {NEST} — excluded from "
                       f"the DECISION set without cause")
    return out


def static_scan(over: dict | None = None, extra: tuple = ()) -> dict:
    """The whole static side of L-F.2: the module sets, the runners' exemptions, the DECISION and
    LINEAGE AST findings.  `over` = {module: planted source}; `extra` = planted new modules."""
    names = sorted(set(tierc11_names()) | set(extra))
    decision_names = [n for n in names if n != NEST and n not in RUNNERS_T]
    decision = {n: read(n, over) for n in decision_names}
    lineage, tc10, ldyn = lineage_walk(decision, over)
    F = runner_findings(names, over)
    for n, src in decision.items():
        F += scan_source(n, src, "DECISION")
    for n, src in lineage.items():
        F += scan_source(n, src, "lineage")
    miss = [m for m in LINEAGE_ENV_T if m not in lineage]
    if miss:
        F.append(f"LINEAGE MISSING: the static walk lacks {miss} (tierc11_env loads them)")
    return {"names": names, "decision": decision_names, "lineage": list(lineage), "tc10": tc10,
            "lineage_dyn": ldyn, "decision_src": decision, "findings": F}


# ═════════════════════════════════════════════════════════ THE FRESH INTERPRETERS
_FRESH = """import json, os, sys
sys.dont_write_bytecode = True
sys.path[:0] = {path!r}
import {mod}
root = os.path.realpath({root!r})
repo = {{}}
for m in sorted(sys.modules):
    f = getattr(sys.modules[m], "__file__", None)
    if f:
        r = os.path.realpath(f)
        if r.startswith(root + os.sep):
            repo[m] = os.path.relpath(r, root)
print("FRESH " + json.dumps({{"mods": sorted(sys.modules), "repo": repo,
                             "self": os.path.realpath(sys.modules[{mod!r}].__file__)}}))
"""


def fresh(mod: str, pre_path: Path | None = None) -> dict:
    """ONE fresh interpreter importing `mod` (a shadow dir first on sys.path when planted)."""
    path = ([str(pre_path)] if pre_path else []) + [str(ROOT), str(SCRIPTS)]
    code = _FRESH.format(path=path, mod=mod, root=str(ROOT))
    env = dict(os.environ, NAIAD_CACHE_DIR=str(SNAP), PYTHONDONTWRITEBYTECODE="1")
    r = subprocess.run([PY, "-B", "-c", code], capture_output=True, text=True, env=env,
                       cwd=str(ROOT), timeout=900)
    line = next((ln for ln in reversed(r.stdout.splitlines()) if ln.startswith("FRESH ")), None)
    if r.returncode or line is None:
        return {"error": f"exit {r.returncode}: {r.stderr.strip()[-300:]}"}
    return json.loads(line[len("FRESH "):])


def fresh_findings(mod: str, res: dict, expect_self: Path) -> list[str]:
    if "error" in res:
        return [f"FRESH IMPORT FAILED {mod}: {res['error']}"]
    out = []
    hits = sorted(m for m in res["mods"] if forbidden(m))
    if hits:
        out.append(f"fresh-interpreter closure of {mod} holds {hits}")
    if res["self"] != os.path.realpath(expect_self):
        out.append(f"FRESH SELF {mod} loaded from {res['self']} (expected {expect_self})")
    return out


def shadow(mod: str, tail: str) -> Path:
    """A shadow copy of scripts/<mod>.py with `tail` appended (its ROOT line pinned to the repo),
    under RUN_ROOT/_det_closure/shadow/<mod>/ — the caller removes it."""
    src = (SCRIPTS / f"{mod}.py").read_text(encoding="utf-8")
    old = "ROOT = Path(__file__).resolve().parents[1]"
    if src.count(old) != 1:
        raise RuntimeError(f"{mod}'s ROOT line is not unique")
    d = RUN_ROOT / "_det_closure" / "shadow" / mod
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True)
    (d / f"{mod}.py").write_text(src.replace(old, f"ROOT = Path({str(ROOT)!r})") + tail,
                                 encoding="utf-8")
    return d


def fresh_plant(mod: str, tail: str) -> list[str]:
    d = shadow(mod, tail)
    try:
        return fresh_findings(mod, fresh(mod, d), d / f"{mod}.py")
    finally:
        shutil.rmtree(d, ignore_errors=True)


# ═════════════════════════════════════════════════════════ AM-2 / AM-8
_SP_IMPORT_RX = re.compile(r"^HOOK-ESCAPE line \d+: (import subprocess|from subprocess import)")


def am8_audit(name: str, src: str) -> tuple[list[str], list[str]]:
    """In an AM-8 module: every subprocess call's argv is a literal list headed by the module's
    named use (and holding its required constants), no shell=True, no subprocess function
    referenced outside a checked call.  Returns (findings, the call sites' argv heads)."""
    head, need, _ = AM8_T[name]
    tree = _tree(src)
    alias, funcs = set(), set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            alias |= {a.asname or a.name for a in n.names if a.name == "subprocess"}
        elif isinstance(n, ast.ImportFrom) and n.module == "subprocess":
            funcs |= {a.asname or a.name for a in n.names if a.name in SP_CALLS}
    out, sites, checked, calls = [], [], set(), []
    for n in ast.walk(tree):
        if not isinstance(n, ast.Call):
            continue
        f = n.func
        is_sp = ((isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name)
                  and f.value.id in alias and f.attr in SP_CALLS)
                 or (isinstance(f, ast.Name) and f.id in funcs))
        if not is_sp:
            continue
        checked.add(id(f))
        if isinstance(f, ast.Attribute):
            checked.add(id(f.value))
        argv = n.args[0] if n.args else next((k.value for k in n.keywords if k.arg == "args"), None)
        calls.append((n.lineno, enclosing(tree, n.lineno),
                      ast.unparse(argv) if argv is not None else "<none>", argv))
        consts = ([_cstr(e) for e in argv.elts] if isinstance(argv, (ast.List, ast.Tuple)) else [])
        if not isinstance(argv, (ast.List, ast.Tuple)) or not argv.elts or consts[0] != head:
            shown = ast.unparse(argv)[:80] if argv is not None else "<none>"
            out.append(f"AM-8 ARGV {name} line {n.lineno}: argv {shown} is not a literal list "
                       f"headed {head!r} (AM-8 allows {name} only {AM8_T[name][2]})")
            continue
        lack = [c for c in need if c not in consts]
        if lack:
            out.append(f"AM-8 ARGV {name} line {n.lineno}: argv {ast.unparse(argv)[:80]} lacks "
                       f"{lack} (AM-8 allows {name} only {AM8_T[name][2]})")
            continue
        if any(k.arg == "shell" and not (isinstance(k.value, ast.Constant)
                                         and k.value.value is False) for k in n.keywords):
            out.append(f"AM-8 SHELL {name} line {n.lineno}: shell= on a subprocess call")
            continue
        sites.append(f"{head} {' '.join(c for c in consts[1:] if c in need)}".strip()
                     + (" …" if len(consts) > 1 + len(need) else ""))
    attr_values = {id(p.value) for p in ast.walk(tree) if isinstance(p, ast.Attribute)}
    for n in ast.walk(tree):
        if isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name) \
                and n.value.id in alias and id(n) not in checked and n.attr not in SP_SAFE:
            out.append(f"AM-8 REF {name} line {n.lineno}: subprocess.{n.attr} referenced outside "
                       f"a checked call")
        elif isinstance(n, ast.Name) and (n.id in funcs or n.id in alias) \
                and id(n) not in checked and isinstance(n.ctx, ast.Load) \
                and id(n) not in attr_values:
            out.append(f"AM-8 REF {name} line {n.lineno}: {n.id} referenced outside a checked "
                       f"call")
    # THE ONE SITE [TC11-FIX verify MINOR-3]: exactly one subprocess call, in the pinned function,
    # with the pinned argv; and no argv element that is a destination resolves into TC10's space
    fn_t, shape_t, dest_t = AM8_SITE_T[name]
    if len(calls) != 1:
        out.append(f"AM-8 SITE {name}: {len(calls)} subprocess call sites — AM-8 allows exactly "
                   f"one, {fn_t}() with argv {shape_t}")
    for ln, fun, shape, argv in calls:
        if (fun, shape) != (fn_t, shape_t):
            out.append(f"AM-8 SITE {name} line {ln}: {fun}() argv {shape[:90]} is not the pinned "
                       f"{fn_t}() argv {shape_t}")
        elts = argv.elts if isinstance(argv, (ast.List, ast.Tuple)) else []
        dests = elts[1:] if dest_t is None else elts[dest_t:][:1] if elts else []
        for e in dests:
            hit = tc10_consts(tree, e, ln)
            if hit:
                out.append(f"AM-8 DEST {name} line {ln}: argv element {ast.unparse(e)[:60]} "
                           f"resolves into TC10's space ({hit[0]!r}) — AM-8 never writes there")
    return out, sites


def enclosing(tree, line: int) -> str:
    """The innermost function holding `line` ('<module>' at top level)."""
    enc = [g for g in ast.walk(tree) if isinstance(g, (ast.FunctionDef, ast.AsyncFunctionDef))
           and g.lineno <= line <= (g.end_lineno or g.lineno)]
    return min(enc, key=lambda g: (g.end_lineno or g.lineno) - g.lineno).name if enc else "<module>"


def tc10_consts(tree, node, line: int) -> list[str]:
    """The string constants `node` can carry — its own, and those of every name it uses, followed
    through the enclosing function's and the module's assignments, transitively — that name a
    path in TC10's space (TC10_DEST_RX)."""
    scope = {}
    for n in tree.body:
        if isinstance(n, ast.Assign):
            for t in n.targets:
                if isinstance(t, ast.Name):
                    scope[t.id] = n.value
        elif isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name) and n.value:
            scope[n.target.id] = n.value
    fun = enclosing(tree, line)
    for g in ast.walk(tree):
        if isinstance(g, (ast.FunctionDef, ast.AsyncFunctionDef)) and g.name == fun:
            for n in ast.walk(g):
                if isinstance(n, ast.Assign):
                    for t in n.targets:
                        if isinstance(t, ast.Name):
                            scope[t.id] = n.value
    seen, stack, consts = set(), [node], []
    while stack:
        x = stack.pop()
        for c in ast.walk(x):
            if _cstr(c) is not None:
                consts.append(c.value)
            elif isinstance(c, ast.Name) and c.id in scope and c.id not in seen:
                seen.add(c.id)
                stack.append(scope[c.id])
    return sorted({c for c in consts if TC10_DEST_RX.search(c)})


def git_calls(src: str) -> tuple[list[str], list[str]]:
    """The git subcommands tierc11_worktree_attest passes through its git([...]) helper, and the
    findings: a subcommand beyond ATTEST_GIT_T, a non-literal argv (its subcommand unknowable), a
    held `git` value, or an argv element resolving into TC10's space [TC11-FIX verify MINOR-2]."""
    tree = _tree(src)
    subs, out, called = set(), [], set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "git":
            called.add(id(n.func))
            a0 = n.args[0] if n.args else None
            if not (isinstance(a0, (ast.List, ast.Tuple)) and a0.elts
                    and _cstr(a0.elts[0]) is not None):
                subs.add("<non-constant>")
                out.append(f"AM-8 GIT tierc11_worktree_attest line {n.lineno}: git("
                           f"{ast.unparse(a0)[:60] if a0 is not None else ''}) — the subcommand is "
                           f"not a literal (AM-8 allows only {sorted(ATTEST_GIT_T)})")
                continue
            c = a0.elts[0].value
            subs.add(c)
            if c not in ATTEST_GIT_T:
                out.append(f"AM-8 GIT tierc11_worktree_attest line {n.lineno}: git subcommand "
                           f"{c!r} — AM-8 allows only {sorted(ATTEST_GIT_T)}")
            for e in a0.elts[1:]:
                hit = tc10_consts(tree, e, n.lineno)
                if hit:
                    out.append(f"AM-8 DEST tierc11_worktree_attest line {n.lineno}: git {c} "
                               f"argv element {ast.unparse(e)[:60]} resolves into TC10's space "
                               f"({hit[0]!r})")
    for n in ast.walk(tree):
        if isinstance(n, ast.Name) and n.id == "git" and isinstance(n.ctx, ast.Load) \
                and id(n) not in called:
            out.append(f"AM-8 GIT tierc11_worktree_attest line {n.lineno}: git referenced "
                       f"outside a call (its subcommands unknowable)")
    return sorted(subs), out


def escape_scan(over: dict | None = None) -> dict:
    """AM-2 / AM-8 over every non-fixture tierc11 module (nest and the runners included)."""
    names = tierc11_names()
    F, per, sites = [], {}, {}
    for n in names:
        src = read(n, over)
        esc = E.hook_escapes(src)
        kept = []
        for f in esc:
            if _SP_IMPORT_RX.match(f):
                if n not in AM8_T:
                    kept.append(f"{f} ({n} is not an AM-8 name)")
            else:
                kept.append(f"{f} [{n}]")
        esc_import_lines = {int(m.group(1)) for f in esc
                            if (m := re.match(r"HOOK-ESCAPE line (\d+): ", f))}
        for ln, x in walk_imports(_tree(src)):
            if (x == "subprocess" or x.startswith("subprocess.")) and n not in AM8_T \
                    and ln not in esc_import_lines:
                kept.append(f"SUBPROCESS REACH {n} line {ln}: {x} by an import call "
                            f"({n} is not an AM-8 name)")
        if n in AM8_T:
            a, s = am8_audit(n, src)
            kept += a
            sites[n] = s
        per[n] = (len(esc), len(kept))
        F += kept
    attest_git, gf = git_calls(read("tierc11_worktree_attest", over))
    F += gf
    return {"names": names, "findings": F, "per": per, "sites": sites, "attest_git": attest_git}


# ═════════════════════════════════════════════════════════ THE REAL SCAN (cached)
def real_scan() -> dict:
    if "scan" in _C:
        return _C["scan"]
    st = static_scan()
    fr, F = {}, list(st["findings"])
    for m in st["decision"]:
        fr[m] = fresh(m)
        F += fresh_findings(m, fr[m], SCRIPTS / f"{m}.py")
    known = set(st["lineage"]) | set(st["tc10"]) | set(st["names"])
    miss = {}
    for m, res in fr.items():
        for k, rel in (res.get("repo") or {}).items():
            if k not in known and not k.startswith("tierc11_") and k != "__main__":
                miss.setdefault(k, (rel, m))
    F += [f"STATIC WALK MISSES {k} ({rel}), loaded by a fresh `import {m}`"
          for k, (rel, m) in sorted(miss.items())]
    env_lin = sorted(k for k in (fr.get("tierc11_env", {}).get("repo") or {})
                     if re.match(r"tierc[2-9](_|$)", k))
    if "tierc11_env" in fr and env_lin != sorted(LINEAGE_ENV_T):
        F.append(f"LINEAGE_ENV_T {sorted(LINEAGE_ENV_T)} != the tierc2..9 modules a fresh "
                 f"`import tierc11_env` loads {env_lin}")
    esc = escape_scan()
    _C["scan"] = {"static": st, "fresh": fr, "closure_findings": F, "env_lineage": env_lin,
                  "escape": esc}
    return _C["scan"]


def tc10_layer_lines(st: dict) -> list[str]:
    out = []
    for m, rel in st["tc10"].items():
        imps = sorted({x for _, x in walk_imports(_tree((ROOT / rel).read_text("utf-8")))
                       if forbidden(x)})
        out.append(f"{m} ({rel}): range imports in its source {imps or 'none'}")
    return out


# ═════════════════════════════════════════════════════════ F-CLOSURE-ALL
def _plant_src(mod: str, tail: str) -> dict:
    return {mod: read(mod) + tail}


def static_plant(over: dict, extra: tuple = ()) -> list[str]:
    return static_scan(over=over, extra=extra)["findings"]


def closure_break():
    t_brk = read("tierc11_stage_t_brk")
    t_brk_no_nest = "\n".join(ln for ln in t_brk.splitlines()
                              if not re.match(r"\s*(import|from)\s+tierc11_nest\b", ln)) + "\n"
    lab_tail = "\n\ndef _plant():\n    import engine.rangefinder  # PLANT\n    return 0\n"
    return plants([
        ("a shadow tierc11_books importing engine.rangefinder at top level (fresh interpreter)",
         "fresh-interpreter closure of tierc11_books holds",
         lambda: fresh_plant("tierc11_books", "\nimport engine.rangefinder  # PLANT\n")),
        ("a shadow tierc11_worktree_attest importing analytics.rangefinder_census at top level "
         "(fresh interpreter; a module outside the shim)",
         "fresh-interpreter closure of tierc11_worktree_attest holds",
         lambda: fresh_plant("tierc11_worktree_attest",
                             "\nimport analytics.rangefinder_census  # PLANT\n")),
        ("a LAZY in-function tierc10_stamps import in tierc11_forward_ledger",
         "AST import [DECISION] tierc11_forward_ledger",
         lambda: static_plant(_plant_src("tierc11_forward_ledger",
                                         "\n\ndef _plant():\n    import tierc10_stamps  # PLANT\n"
                                         "    return tierc10_stamps\n"))),
        ("a planted Range.top read in tierc11_registrations",
         "AST Range.top/.bottom read [DECISION] tierc11_registrations",
         lambda: static_plant(_plant_src("tierc11_registrations",
                                         "\n\ndef _plant(r):\n    return r.top  # PLANT\n"))),
        ("getattr(r, 'bottom') in tierc11_stage_w",
         "AST Range.top/.bottom read [DECISION] tierc11_stage_w",
         lambda: static_plant(_plant_src("tierc11_stage_w",
                                         "\n\ndef _plant(r):\n    return getattr(r, 'bottom')\n"))),
        ("importlib.import_module('analytics.rangefinder_census') in tierc11_data_clock_note",
         "AST import [DECISION] tierc11_data_clock_note",
         lambda: static_plant(_plant_src("tierc11_data_clock_note",
                                         "\n\ndef _plant():\n    import importlib\n    return "
                                         "importlib.import_module('analytics.rangefinder_census')"
                                         "\n"))),
        ("a name-held import_module(nm) in tierc11_score (not the declared door)",
         "AST UNDECLARED dynamic import [DECISION] tierc11_score",
         lambda: static_plant(_plant_src("tierc11_score",
                                         "\n\ndef _plant(nm='tierc10_null'):\n    import importlib"
                                         "\n    return importlib.import_module(nm)\n"))),
        ("sys.modules['tierc11_nest'] in tierc11_stage_g",
         "AST sys.modules reach [DECISION] tierc11_stage_g",
         lambda: static_plant(_plant_src("tierc11_stage_g",
                                         "\n\ndef _plant():\n    return sys.modules"
                                         "['tierc11_nest']\n"))),
        ("a NEW tierc11 module (tierc11_close_plant, unnamed here: defaults to DECISION) with a "
         "lazy `from tierc11_nest import …`",
         "AST import [DECISION] tierc11_close_plant",
         lambda: static_plant({"tierc11_close_plant": "def _plant():\n    from tierc11_nest "
                                                      "import lens_frame\n    return lens_frame\n"},
                              extra=("tierc11_close_plant",))),
        ("a LAZY tierc10_census import in LINEAGE tierc9",
         "AST import [lineage] tierc9",
         lambda: static_plant(_plant_src("tierc9", "\n\ndef _plant():\n    import tierc10_census"
                                                   "  # PLANT\n    return 0\n"))),
        ("a .bottom read in LINEAGE tierc7_rules",
         "AST Range.top/.bottom read [lineage] tierc7_rules",
         lambda: static_plant(_plant_src("tierc7_rules",
                                         "\n\ndef _plant(r):\n    return r.bottom  # PLANT\n"))),
        ("a lazy engine.rangefinder import in lab tierc6_lab_limit, reachable ONLY through "
         "tierc6's name-held __import__",
         "AST import [lineage] tierc6_lab_limit",
         lambda: static_plant(_plant_src("tierc6_lab_limit", lab_tail))),
        ("runner tierc11_stage_t_brk with its tierc11_nest import removed",
         "EXEMPTION UNEARNED: runner tierc11_stage_t_brk",
         lambda: static_plant({"tierc11_stage_t_brk": t_brk_no_nest})),
        ("exec('import tierc10_census') inside a function of DECISION tierc11_stage_s (code built "
         "at run time)",
         "AST UNDECLARED dynamic site [DECISION] tierc11_stage_s",
         lambda: static_plant(_plant_src("tierc11_stage_s",
                                         "\n\ndef _plant():\n    exec('import tierc10_census')  "
                                         "# PLANT\n    return 0\n"))),
        ("r.__dict__['top'] in DECISION tierc11_forward_ledger (a namespace-dict read)",
         "AST Range.top/.bottom read [DECISION] tierc11_forward_ledger",
         lambda: static_plant(_plant_src("tierc11_forward_ledger",
                                         "\n\ndef _plant(r):\n    return r.__dict__['top']  "
                                         "# PLANT\n"))),
        ("vars(r)['bottom'] in DECISION tierc11_registrations (a namespace-dict read)",
         "AST Range.top/.bottom read [DECISION] tierc11_registrations",
         lambda: static_plant(_plant_src("tierc11_registrations",
                                         "\n\ndef _plant(r):\n    return vars(r)['bottom']  "
                                         "# PLANT\n"))),
    ])


def closure_real():
    sc = real_scan()
    st, fr, F = sc["static"], sc["fresh"], sc["closure_findings"]
    say(f"  [INFO] non-fixture tierc11 modules ({len(st['names'])}): {', '.join(st['names'])}")
    say(f"  [INFO] runners, each exemption earned by its own `import {NEST}`: "
        f"{', '.join(RUNNERS_T)}; {NEST} itself excluded")
    say(f"  [INFO] DECISION set ({len(st['decision'])}): {', '.join(st['decision'])}")
    for m in st["decision"]:
        res = fr[m]
        if "error" in res:
            say(f"  [INFO]   fresh `import {m}`: FAILED")
            continue
        say(f"  [INFO]   fresh `import {m}`: loaded from {rel_of(Path(res['self']))} · names "
            f"containing a forbidden substring: {sorted(x for x in res['mods'] if forbidden(x))}")
    dd = [(n, fun, tg) for n, src in st["decision_src"].items()
          for _, _, fun, tg in dyn_sites(_tree(src))]
    say(f"  [INFO] DECISION non-constant import sites: "
        + ("; ".join(f"{n}.{fun}() (declared: the nest-only door, runtime-guarded — a non-nest "
                     f"caller HALTs, F-CLOSURE-ENV; its name-held strings {tg})" for n, fun, tg in dd)
           or "none"))
    say(f"  [INFO] LINEAGE, the static repo closure of the DECISION set ({len(st['lineage'])}): "
        f"{', '.join(st['lineage'])}")
    say(f"  [INFO] lineage name-held dynamic imports followed: "
        + ("; ".join(f"{m}.{fun}() -> {tg}" for m, ds in st["lineage_dyn"].items()
                     for _, _, fun, tg in ds) or "none"))
    say(f"  [INFO] the tierc2..9 modules a fresh `import tierc11_env` loads: "
        f"{', '.join(sc['env_lineage'])} (== LINEAGE_ENV_T, typed)")
    say(f"  [INFO] DISCLOSURE — the TC10 layer the DECISION set imports (outside L-F.2's "
        f"DECISION set and lineage; L-0.3 routes its range paths through {NEST}, whose runners "
        f"import it first): " + "; ".join(tc10_layer_lines(st)))
    ok = not F
    n_fr = sum("error" not in r for r in fr.values())
    return ok, (f"{len(st['decision'])} DECISION modules, each in its own fresh interpreter "
                f"({n_fr}/{len(fr)} imported from scripts/<name>.py): no loaded module named "
                f"with {list(FORBIDDEN)}; this file's AST walk of the {len(st['decision'])} "
                f"DECISION and {len(st['lineage'])} LINEAGE sources (imports anywhere incl. "
                f"function bodies, constant-string and name-held import calls, sys.modules "
                f"reaches, .top/.bottom reads incl. getattr/attrgetter): "
                f"{len(F)} finding(s){(': ' + ' · '.join(F[:4])) if F else ''}; the "
                f"{len(RUNNERS_T)} runner exemptions earned; the walk holds LINEAGE_ENV_T and "
                f"every repo module the fresh interpreters loaded")


# ═════════════════════════════════════════════════════════ F-HOOK-ESCAPE-ALL
def esc_plant(mod: str, tail: str) -> list[str]:
    return escape_scan(over=_plant_src(mod, tail))["findings"]


def escape_break():
    return plants([
        ("a subprocess call planted in tierc11_books (not an AM-8 name)",
         "(tierc11_books is not an AM-8 name)",
         lambda: esc_plant("tierc11_books", "\nimport subprocess\n\n\ndef _plant():\n"
                                            "    return subprocess.run(['ls'])\n")),
        ("`from subprocess import run` planted lazily in tierc11_ride",
         "(tierc11_ride is not an AM-8 name)",
         lambda: esc_plant("tierc11_ride", "\n\ndef _plant():\n    from subprocess import run as "
                                           "_r\n    return _r(['git', 'push'])\n")),
        ("subprocess reached by importlib.import_module('subprocess') in tierc11_stage_s",
         "SUBPROCESS REACH tierc11_stage_s",
         lambda: esc_plant("tierc11_stage_s", "\n\ndef _plant():\n    import importlib\n    return "
                                              "importlib.import_module('subprocess')\n")),
        ("a `curl` subprocess in tierc11_data_clock_note (an AM-8 module, not its named use)",
         "AM-8 ARGV tierc11_data_clock_note",
         lambda: esc_plant("tierc11_data_clock_note",
                           "\n\ndef _plant():\n    return subprocess.run(['curl', 'https://x'])\n")),
        ("a non-literal argv in tierc11_worktree_attest (the removed one-shot `-- <cmd>` mode)",
         "AM-8 ARGV tierc11_worktree_attest",
         lambda: esc_plant("tierc11_worktree_attest",
                           "\n\ndef _plant(cmd):\n    return subprocess.run(cmd, cwd='.')\n")),
        ("shell=True on the clone in tierc11_data",
         "AM-8 SHELL tierc11_data",
         lambda: esc_plant("tierc11_data", "\n\ndef _plant():\n    return subprocess.run(['cp', "
                                           "'-cpR', 'a', 'b'], shell=True)\n")),
        ("subprocess.run held as a value in tierc11_data",
         "AM-8 REF tierc11_data",
         lambda: esc_plant("tierc11_data", "\n_RUN = subprocess.run  # PLANT\n")),
        ("pq.read_table in tierc11_score",
         "pyarrow native I/O",
         lambda: esc_plant("tierc11_score", "\n\ndef _plant(p):\n    import pyarrow.parquet as pq"
                                            "\n    return pq.read_table(p)\n")),
        ("os.system in tierc11_nest (the nest is scanned too)",
         "out of process",
         lambda: esc_plant("tierc11_nest", "\n\ndef _plant():\n    return os.system('ls')\n")),
        ("pd.read_parquet(p, filesystem=fs) in tierc11_stage_r",
         "filesystem=",
         lambda: esc_plant("tierc11_stage_r", "\n\ndef _plant(p, fs):\n    return pd.read_parquet("
                                              "p, filesystem=fs)\n")),
        ("git(['push', '--force', 'origin', 'HEAD'], ROOT) in tierc11_worktree_attest (a git "
         "subcommand AM-8 does not allow)",
         "AM-8 GIT tierc11_worktree_attest",
         lambda: esc_plant("tierc11_worktree_attest",
                           "\n\ndef _plant():\n    return git(['push', '--force', 'origin', "
                           "'HEAD'], ROOT)\n")),
        ("a `cp -cpR` of OUT INTO TC10_DATA in tierc11_data (a second call site, its destination "
         "in research_outputs/tierc10)",
         "AM-8 DEST tierc11_data",
         lambda: esc_plant("tierc11_data",
                           "\n\ndef _plant():\n    return subprocess.run(['cp', '-cpR', str(OUT), "
                           "str(TC10_DATA)], check=True)\n")),
        ("a second, well-formed `git show` call in tierc11_data_clock_note (outside git_blob)",
         "AM-8 SITE tierc11_data_clock_note",
         lambda: esc_plant("tierc11_data_clock_note",
                           "\n\ndef _plant(rel):\n    return subprocess.run(['git', '-C', str(ROOT), "
                           "'show', f'HEAD:{rel}'], capture_output=True)\n")),
    ])


def escape_real():
    esc = real_scan()["escape"]
    F = esc["findings"]
    subp = sorted(n for n, (e, _) in esc["per"].items() if e)
    for n in esc["names"]:
        e, _ = esc["per"][n]
        say(f"  [INFO] {n}: E.hook_escapes {e} finding(s)"
            + (f" — `import subprocess` only, an AM-8 name ({AM8_T[n][2]}); call sites: "
               f"{esc['sites'][n]}" if n in AM8_T else ""))
    say(f"  [INFO] tierc11_worktree_attest's git subcommands (through its git([...]) helper): "
        f"{esc['attest_git']}")
    unused = [n for n in AM8_T if not esc["sites"].get(n)]
    ok = not F and set(subp) <= set(AM8_T) and not unused
    return ok, (f"E.hook_escapes over all {len(esc['names'])} non-fixture tierc11 modules (nest "
                f"and the runners included): 0 pyarrow-native / os-level / fd-keyword escapes; "
                f"subprocess imported only by {subp} (the AM-8 names {sorted(AM8_T)}), every call "
                f"a literal argv headed by its named use, no shell=, no subprocess value held; each "
                f"AM-8 module holds exactly its ONE pinned call site (function and argv), no "
                f"destination resolves into TC10's space; the attestation's git subcommands "
                f"{esc['attest_git']} within the typed {sorted(ATTEST_GIT_T)}; no "
                f"other module reaches subprocess by an import call; {len(F)} finding(s)"
                + (f": {' · '.join(F[:4])}" if F else "")
                + (f"; AM-8 allowance with no call site: {unused}" if unused else ""))


# ═════════════════════════════════════════════════════════ F-DET
def probe_text() -> str:
    sc = real_scan()
    st, fr, esc = sc["static"], sc["fresh"], sc["escape"]
    L = ["PROBE · TIER-C11 L-F.2 / AM-2 / AM-8 CLOSURE SCAN (deterministic; module names and "
         "verdicts only — no line number, no registered number)"]
    L.append(f"forbidden substrings {list(FORBIDDEN)}")
    L.append(f"non-fixture tierc11 modules {st['names']}")
    L.append(f"runners {list(RUNNERS_T)} · DECISION {st['decision']}")
    for m in st["decision"]:
        r = fr[m]
        L.append(f"fresh {m}: " + ("FAILED" if "error" in r else
                                   f"self {rel_of(Path(r['self']))} · forbidden "
                                   f"{sorted(x for x in r['mods'] if forbidden(x))}"))
    L.append(f"LINEAGE {st['lineage']}")
    L.append("lineage name-held dynamic imports "
             + json.dumps({m: [[fun, tg] for _, _, fun, tg in ds]
                           for m, ds in st["lineage_dyn"].items()}, sort_keys=True))
    L.append(f"TC10 layer {tc10_layer_lines(st)}")
    L.append(f"env lineage {sc['env_lineage']}")
    L.append(f"closure findings {sc['closure_findings']}")
    L.append("hook escapes " + json.dumps({n: esc["per"][n][0] for n in esc["names"]},
                                          sort_keys=True))
    L.append("AM-8 call sites " + json.dumps(esc["sites"], sort_keys=True))
    L.append(f"attest git subcommands {esc['attest_git']}")
    L.append(f"escape findings {esc['findings']}")
    return "\n".join(L) + "\n"


def emit() -> bytes:
    if "emit" not in _C:
        _C["emit"] = (AS_OF_LINE + "\n" + probe_text()).encode("utf-8")
    return _C["emit"]


def det_findings(a: tuple, b: tuple, this: bytes) -> list[str]:
    out = []
    for lab, (rc, _) in (("seed 1", a), (f"seed {SEED}", b)):
        if rc != 0:
            out.append(f"{lab} exit {rc}")
    if not a[1] or not b[1]:
        out.append("an emission is EMPTY")
    for lab, x, y in (("seed 1 vs seed 20260924", a[1], b[1]), ("seed 1 vs this run", a[1], this)):
        if x != y:
            k = next((i for i in range(min(len(x), len(y))) if x[i] != y[i]), min(len(x), len(y)))
            out.append(f"{lab}: bytes differ at byte {k} (sha {sha_bytes(x)[:12]}… vs "
                       f"{sha_bytes(y)[:12]}…)")
    return out


def det_runs(flag: str = "--emit-to") -> dict:
    outs = {}
    for s in DET_SEEDS:
        d = RUN_ROOT / "_det_closure" / (f"seed_{s}" if flag == "--emit-to" else f"hashorder_{s}")
        env = dict(os.environ, NAIAD_CACHE_DIR=str(SNAP), PYTHONDONTWRITEBYTECODE="1",
                   PYTHONHASHSEED=str(s))
        r = subprocess.run([PY, "-B", str(Path(__file__).resolve()), f"{flag}={d}"],
                           env=env, capture_output=True, text=True, cwd=str(ROOT), timeout=1800)
        p = d / ARTIFACT
        outs[s] = (r.returncode, p.read_bytes() if p.exists() else b"")
    return outs


def det_break():
    this = emit()
    bent = bytearray(this)
    bent[len(bent) // 2] ^= 0x01
    return plants([
        ("one byte bent in a copy of this run's emission", "bytes differ at byte",
         lambda: det_findings((0, this), (0, bytes(bent)), this)),
        ("a hash-order-dependent emission (set iteration) under the two seeds",
         "seed 1 vs seed 20260924: bytes differ",
         lambda: (lambda o: det_findings(o[DET_SEEDS[0]], o[DET_SEEDS[1]],
                                         o[DET_SEEDS[0]][1]))(det_runs("--emit-hashorder-to"))),
    ])


def det_real():
    this = emit()
    o = det_runs()
    bad = det_findings(o[DET_SEEDS[0]], o[DET_SEEDS[1]], this)
    n_lines = len(this.decode("utf-8").splitlines())
    return (not bad), (f"exit {o[1][0]}/{o[SEED][0]}; {len(this)} bytes, {n_lines} lines (the "
                       f"module sets, the fresh-interpreter verdicts, the lineage walk, the "
                       f"escape scan and the AM-8 call sites); sha {sha_bytes(o[1][1])[:16]}… == "
                       f"{sha_bytes(o[SEED][1])[:16]}… == this run {sha_bytes(this)[:16]}…: "
                       f"{not bad}" + ("" if not bad else f"; findings {bad}"))


# ═════════════════════════════════════════════════════════ THE TABLE
FIXTURES = (
    ("F-CLOSURE-ALL", "L-F.2 over the WHOLE DECISION set and the lineage: range-free by fresh "
     "interpreter and by AST",
     "any of the sixteen plants (two shadow modules with a top-level range import under a fresh "
     "interpreter; a lazy tierc10_stamps import, a .top read, a getattr 'bottom' read, a "
     "constant-string import_module, a name-held import_module and a sys.modules reach planted in "
     "six DECISION sources; a new tierc11 module importing tierc11_nest; a lazy tierc10_census "
     "import and a .bottom read in two LINEAGE sources; a lazy range import in a lab reachable "
     "only by name; a runner without its nest import; an exec('import tierc10_census') in a "
     "DECISION function; r.__dict__['top'] and vars(r)['bottom'] in two DECISION sources) is not "
     "caught by its named detector",
     "a fresh interpreter importing any DECISION module (one per module) holds a module named "
     "with rangefinder / tierc10_census / tierc10_stamps / tierc10_null / tierc11_nest or loads "
     "it from anywhere but scripts/<name>.py; the AST walk of any DECISION or LINEAGE source "
     "finds such an import anywhere (function bodies included; constant-string or name-held "
     "import calls), a sys.modules reach of one, or a .top / .bottom read (attribute, getattr, "
     "attrgetter, a __dict__ / vars() subscript or .get); a DECISION module holds a non-constant "
     "import site other than tierc11_env.tc10_import or any exec / eval / compile call, or a "
     "lineage one resolves to no module; a typed runner does not "
     "import tierc11_nest; the lineage walk lacks one of the fifteen tierc2..9 modules "
     "tierc11_env loads, or misses a repo module a fresh interpreter loaded",
     closure_break, closure_real),
    ("F-HOOK-ESCAPE-ALL", "AM-2 over every non-fixture tierc11 module; subprocess only at the "
     "three AM-8 names",
     "any of the thirteen plants (a subprocess call, a from-import and an import_module('subprocess') "
     "in three non-AM-8 modules; a curl argv, a non-literal argv, shell=True and a held "
     "subprocess.run in AM-8 modules; pq.read_table, os.system and a filesystem= keyword in "
     "three more; a `git push` through the attestation's helper; a cp into TC10_DATA; a second "
     "well-formed git show call site) is not caught by its named detector",
     "E.hook_escapes finds, in any of the non-fixture tierc11 modules (tierc11_nest and the "
     "runners included), any escape but `import subprocess` in tierc11_data / "
     "tierc11_data_clock_note / tierc11_worktree_attest; any other module reaches subprocess by "
     "an import call; an AM-8 module's subprocess call has an argv that is not a literal list "
     "headed by its named use (cp with -cpR / git with show / git), passes shell=, or a "
     "subprocess function is referenced outside a checked call; an AM-8 module holds other than "
     "ONE subprocess call site, in its pinned function with its pinned argv (AM8_SITE_T), or a "
     "destination argv element resolves into research_outputs/tierc10 or the TC10 snapshot; the "
     "attestation passes a git subcommand outside {worktree, rev-parse, status, show}, a "
     "non-literal one, or holds its git helper as a value; an AM-8 allowance has no call site",
     escape_break, escape_real),
    ("F-DET", "two subprocess emissions under different hash seeds, one set of bytes",
     "a one-byte-bent copy or a hash-order-dependent emission is not found",
     "the PYTHONHASHSEED 1 and 20260924 emissions of CLOSURE_PROBE.txt (module sets, fresh "
     "verdicts, lineage walk, escape scan, AM-8 call sites) differ from each other or from this "
     "run's bytes, or either exits nonzero",
     det_break, det_real),
)


def file_transcript(out: Path, body: bytes, refile: bool) -> list[str]:
    """NEVER CLOBBER the transcript of record [tierc10_resume_fixtures.file_transcript]."""
    if not out.exists() and not refile:
        return [f"{out.name} ABSENT — nothing written; re-file with --refile-transcript"]
    if out.exists() and out.read_bytes() == body:
        return []
    if out.exists() and not refile:
        (rr := out.with_name(out.stem + "_rerun.txt")).write_bytes(body)
        return [f"{out.name} NOT byte-identical; this run -> {rr.name}; record untouched"]
    out.write_bytes(body)
    return []


def main() -> int:
    global RUN_ROOT
    args = sys.argv[1:]
    root = RUN_ROOT = Path(next((a.split("=", 1)[1] for a in args if a.startswith("--root=")),
                                OUT))
    emit_to = next((a.split("=", 1)[1] for a in args if a.startswith("--emit-to=")), None)
    if emit_to:                              # F-DET's twin: emission only, no legs
        Path(emit_to).mkdir(parents=True, exist_ok=True)
        (Path(emit_to) / ARTIFACT).write_bytes(emit())
        return 0
    ho = next((a.split("=", 1)[1] for a in args if a.startswith("--emit-hashorder-to=")), None)
    if ho:                                   # F-DET's SABOTAGE twin: a set-order line
        Path(ho).mkdir(parents=True, exist_ok=True)
        (Path(ho) / ARTIFACT).write_bytes(
            emit() + ("set order: " + ",".join(set(E.PANEL17)) + "\n").encode())
        return 0
    pick = [a.lower() for a in args if not a.startswith("--")]
    t0 = time.time()
    say(AS_OF_LINE)
    say("=" * 78)
    say("TIER-C11 TC11-FIX CLOSURE FIXTURES — L-F.2 over the whole DECISION set + lineage; AM-2 "
        "/ AM-8 over every non-fixture tierc11 module — break leg first, RED or void")
    say("=" * 78)
    say(f"seed {SEED} · substrate {SNAP.name} · pin {PIN}")
    say(f"  typed: FORBIDDEN {list(FORBIDDEN)} · RUNNERS_T {list(RUNNERS_T)} · DYN_DECLARED_T "
        f"{[f'{a}.{b}' for a, b in DYN_DECLARED_T]}")
    say(f"  typed: LINEAGE_ENV_T {list(LINEAGE_ENV_T)}")
    say("  typed: AM8_T " + "; ".join(f"{k}: {v[0]} {list(v[1])} — {v[2]}" for k, v in AM8_T.items()))
    say("  typed: AM8_SITE_T " + "; ".join(f"{k}: {v[0]}() argv {v[1]} · destination "
                                           f"{'argv[' + str(v[2]) + ']' if v[2] is not None else 'none (every argv element checked)'}"
                                           for k, v in AM8_SITE_T.items()))
    say(f"  typed: ATTEST_GIT_T {sorted(ATTEST_GIT_T)} · TC10 destinations {TC10_DEST_RX.pattern!r} · "
        f"EXEC_FUNCS {sorted(EXEC_FUNCS)}")
    for fid, title, b_if, r_if, b, r in FIXTURES:
        if not pick or any(q in fid.lower() for q in pick):
            prove(fid, title, b_if, r_if, b, r)
    say(f"\n  {len(PASSED)} GREEN, {len(FAILED)} RED")
    for f in FAILED:
        say(f"    RED: {f}")
    root.mkdir(parents=True, exist_ok=True)
    body = ("\n".join(LINES) + "\n").encode("utf-8")
    name = TRANSCRIPT if not pick else TRANSCRIPT.replace(".txt", "_partial.txt")
    bad = file_transcript(root / name, body, "--refile-transcript" in args or bool(pick))
    for x in bad:
        clock(x)
    clock(f"wall {time.time() - t0:.1f}s · transcript sha {sha_bytes(body)}")
    if FAILED:
        print("*** HALT: fixture mismatch. Nothing downstream is trustworthy. ***")
    return 1 if (FAILED or bad) else 0


if __name__ == "__main__":
    raise SystemExit(main())
