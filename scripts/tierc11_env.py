#!/usr/bin/env python
"""TIER-C11 · THE RANGE-FREE SHIM [LEANS L-0.3].  TC10's code, re-rooted onto TC11.

Contract of record: exchange/queue/2026-09-24_TC11_APOLLO.md (sha256 bb38e016…,
STEP Q b9ed953).  Executor HEPHAESTUS; seed 20260924.  Executor readings:
research_outputs/tierc11/LEANS.md (frozen at 4ed4e67) — L-0.3 CODE REUSE is the
reading this module builds; L-1.3 (era by CLOSE), L-1.1/L-1.2 (tolls) and the
seeds of L-1.4 are exposed as constants.

WHAT IT DOES, IN ORDER
  1. GUARDS the substrate before any engine import: NAIAD_CACHE_DIR must be
     ~/.cache/naiad/snapshots/tc11_20260925 (never the live cache, never the
     TC10 snapshot) and must hold klines/.
  2. IMPORTS tierc2_baseline FIRST, under the TC11 env: it binds TB.KLINES /
     TB.FUNDING at import, and every lineage copy (T3/T4/T5.KLINES) is taken
     from it.
  3. IMPORTS tierc10_data, tierc10_panel, tierc10_brk, tierc10_lanes and the
     tierc2..9 lineage, EACH inside an env WINDOW: NAIAD_CACHE_DIR points at the
     TC10 snapshot for the duration of that one import statement only (TC10's
     assert_substrate demands it), restored in `finally`.  A recording audit
     hook logs every path touched inside each window; a module that opens
     anything under the TC10 snapshot (or the live cache) at import, or reads a
     TC10 record that is neither on `TC10_ALLOW` nor declared for that window in
     `IMPORT_TC10_READS`, HALTs the shim — such a module cannot be re-used this
     way.
     It NEVER imports tierc10_census, tierc10_stamps, tierc10_null,
     analytics.rangefinder_census or engine.rangefinder (that is
     scripts/tierc11_nest.py's business, through `tc10_import`, whose range
     door opens ONLY for a caller that is tierc11_nest [verifier MINOR-6]).
     The two L-0.3 post-shim clauses about the census module (C.as_of_close_ms
     == pin for every asset; C.RETEST_PINS) are HANDED OFF to tierc11_nest,
     named in the lean block [verifier MINOR-5].
  4. RE-ROOTS the CLOSED LIST of L-0.3 that belongs to these modules (D.*, TP.*,
     BK.*, LN.*), each verified to exist before it is assigned, plus the TC10
     bindings the list missed (named, with the reason, in `REROOT_PLAN`).
     Every re-root is printed as a lean by `lean_block()`.
  5. ASSERTS (post-shim, HALT on any clause): D.load_pin() == TP.stage_d_pin()
     == 1790294400000; D.kline_path('BTCUSDT','4h') under tc11_20260925; every
     KLINES/FUNDING binding under tc11; TP.substrate() is tc11; no module global
     of the estate still names the TC10 snapshot or the live cache, and every
     global naming research_outputs/tierc10 is DECLARED (`NOT_REROOTED`); the
     panels re-resolved from TC11's Stage D manifest; the fee schedule's taker
     equals tierc2_rules.FEE_BPS_SIDE; and the process holds no range module.
  6. INSTALLS THE PROCESS-WIDE AUDIT HOOK LAST (sys.addaudithook).  It raises
     `AuditHalt` (a SystemExit: `except Exception` cannot swallow it) on:
       · any open (or listing / mutation) of a path under the TC10 snapshot or
         the live cache;
       · any WRITE-mode open (or rename / remove / mkdir / …) under
         research_outputs/tierc10/, research_outputs/tierc10_run2/,
         scripts/tierc10_*, exchange/status/LEDGER*, LEDGER.md or .gitignore —
         in this tree and in the main tree;
       · any open / listing under research_outputs/tierc10 that is NOT one of
         the six records L-0.3 names plus the two AM-1 ruled in (`TC10_ALLOW`, eight) — the allow-list is
         ENFORCED, not merely logged [verifier MAJOR-1];
       · a dir_fd-relative open [MINOR-3].  The "open" audit event carries no
         dir_fd, so a RELATIVE path is judged against the working directory AND
         against every directory fd the process holds open at that instant (a
         sound over-approximation: `..` and symlinks included); a DIRECTORY
         open of a protected root, of an ancestor of one, or inside
         write-protected space is refused outright when its anchor is
         unambiguous (absolute, or relative with no directory fd open).  Every
         other dir_fd-taking event (remove, rename, mkdir, …; scandir(fd)) is
         resolved exactly through the fd's own path (F_GETPATH).
     Paths are judged CANONICALLY: realpath, then the deepest existing ancestor
     matched by (st_dev, st_ino) against the protected roots, then NFC +
     casefold, then the /System/Volumes/Data firmlink and the /.nofollow and
     /.resolve/N prefixes stripped — so a case variant or a volume alias of a
     protected path is that path [MAJOR-2].  ALLOW reads and BLOCKED attempts
     are LOGGED (`audit_log()`) and REPORTED at exit on stderr; a process that
     saw any BLOCKED attempt (even one swallowed in a thread) is forced to exit
     AUDIT_EXIT_CODE [MINOR-7].  Audit hooks cannot be removed, so the fixtures
     prove the hook in SUBPROCESSES.

LIMIT OF THE HOOK, SAID OUT LOUD (the AMENDMENT CANDIDATE text of L-0.3): the
hook sees only Python-level opens (builtins.open, io.open_code, os.open;
pandas.read_parquet on a path string, np.fromfile / np.memmap go through one).
It does NOT see: pyarrow's native readers and writers (pq.read_table,
pq.ParquetFile, pq.write_table, pa.memory_map, pyarrow.dataset, pyarrow.fs
LocalFileSystem opens); pd.read_parquet(..., filesystem=...) and
DataFrame.to_parquet(partition_cols=...) (both route to pyarrow's C++ I/O);
out-of-process reads and writes (subprocess, os.system, ctypes).  A write-never
violation through those goes unrefused.  `hook_escapes(src)` is the AST scan
that bans them in a module's source; TC11 code reads parquet through pandas on
path strings (TB / D loaders) and never through those.

WHAT WOULD MAKE THIS WRONG: importing tierc2_baseline after a TC10 module (the
loaders would bind the TC10 snapshot); leaving the env pointed at TC10 after a
window; re-rooting D.SNAPSHOT without D.OUT (every lens frame silently clipped at
TC10's pin — the post-shim assertion refuses it); re-rooting a name that does not
exist (a typo would create a dead attribute and re-root nothing — `_reroot`
refuses it); relying on a default seed bound at def time (never re-rooted: every
TC11 call passes seed=20260924, n_boot=4000 explicitly).

Run:  export NAIAD_CACHE_DIR=$HOME/.cache/naiad/snapshots/tc11_20260925 PYTHONDONTWRITEBYTECODE=1
      ~/venvs/naiad/bin/python -B scripts/tierc11_env.py        # prints the lean block
Import:  import tierc11_env as E   (E.TP, E.D, E.BK, E.LN, E.T9 … ; see __all__)
"""
from __future__ import annotations

import ast
import atexit
import contextlib
import copy
import fcntl
import importlib
import json
import os
import re
import stat
import sys
import unicodedata
from pathlib import Path

# ══════════════════════════════════════════════════════ 0 · CONSTANTS OF RECORD
ROOT = Path(__file__).resolve().parents[1]
HOME = Path.home()
SNAPSHOT = HOME / ".cache" / "naiad" / "snapshots" / "tc11_20260925"
TC10_SNAPSHOT = HOME / ".cache" / "naiad" / "snapshots" / "tc10_20260921"
LIVE_CACHE = HOME / ".cache" / "naiad" / "data_cache"
OUT = ROOT / "research_outputs" / "tierc11"

PIN_MS = 1_790_294_400_000          # 2026-09-25T00:00:00Z [L-0.1]
PIN_ISO = "2026-09-25T00:00:00Z"
TC10_PIN_MS = 1_790_006_400_000     # 2026-09-21T16:00:00Z — the pin that must NOT leak
SEED = 20260924
SEED_SENS = 20260816                # the lineage's bootstrap seed, printed beside [L-1.4]
N_BOOT = 4000
ERA_CUT_MS = 1_719_791_999_000      # 2024-06-30T23:59:59Z, the LAST tuning instant [L-1.3]
ERA_CUT_ISO = "2024-06-30T23:59:59Z"
LENS_MS = {"5m": 300_000, "15m": 900_000, "1h": 3_600_000, "4h": 14_400_000,
           "12h": 43_200_000, "1d": 86_400_000, "1w": 604_800_000}
LEAN_TAG = "[LEAN-HEPHAESTUS]"
FORBIDDEN_MODULE_SUBSTRINGS = ("rangefinder", "tierc10_census", "tierc10_stamps",
                               "tierc10_null")
# The explicit allow-list of TC10 RECORDS a TC11 stage may READ — the six (+2 by AM-1)
# L-0.3 names ("control journal, P-TRG-2 scored json, TUNING_RESULT, STEP0_RECORD,
# the five-row table, the P_AGE_1 table"), nothing added.  Read by ABSOLUTE
# MAIN-TREE path (`tc10_record`), so a review worktree sees them.  Any other read
# under research_outputs/tierc10 HALTs once the hook is armed.
TC10_ALLOW = {
    "research_outputs/tierc10/panel/control_journal.parquet":
        "the control journal — L-1.7 F-CTRL(b) referee (200 rows, sha fcbf5db0…)",
    "research_outputs/tierc10/registrations/P-TRG-2.scored.json":
        "the P-TRG-2 scored json — L-1.6 9/12 anchor, full-arm book_sha256 b2276fa4…",
    "research_outputs/tierc10/census/TUNING_RESULT.json":
        "TUNING_RESULT — C.RETEST_PINS at census import (tierc11_nest) [L-R.3/L-R.6]",
    "research_outputs/tierc10/STEP0_RECORD.json":
        "STEP0_RECORD — L-R.3 port shas + pins_of_record",
    "research_outputs/tierc10/stamps/control_entry_by_state.parquet":
        "the five-row table — L-R.7 anchor of R5",
    "research_outputs/tierc10/close/P_AGE_1_TIDE_YOUTH.parquet":
        "the P_AGE_1 table — L-G.1 pre_seen anchor",
    # AM-1 (research_outputs/tierc11/LEANS_AMENDMENTS.md, 2026-09-25): two disclosure references ruled in
    "research_outputs/tierc10/census/height_toll_verdict.parquet":
        "AM-1 · L-R.4 disclosure: TC10's per-era [Q-R3] verdicts (continuity column beside TC11's R2)",
    "research_outputs/tierc10/census/outcome_grid.parquet":
        "AM-1 · L-T.1 selection_hazard + R4 continuity anchor: TC10's 7,920-cell census grid",
}
# Records a later stage may want that L-0.3 does NOT name.  FILED AS AN AMENDMENT
# CANDIDATE, NOT ALLOWED: a read of any of them HALTs like any unlisted record
# until the operator rules the amendment in (then it moves into TC10_ALLOW with a
# dated AMENDMENT line in LEANS.md).  TC10's data/AS_OF_PIN.json is deliberately
# absent from both lists: L-T.6's opening instant is a literal (2026-09-21T16:00Z)
# and the leak detector's referee is the literal TC10_PIN_MS.
TC10_AMENDMENT_CANDIDATES = {
    "research_outputs/tierc10/close/P_AGE_1_TIDE_YOUTH.md":
        "L-G.1 pre_seen: the P_AGE_1 narrative that prints B4 OLD n 59 / −22.6566 R",
    "research_outputs/tierc10/PROGRESS.json":
        "L-1.7 the sha of record of the filed control journal (stage PANEL/gate)",
    "research_outputs/tierc10/data/STAGE_D_MANIFEST.json":
        "L-0.2 clone provenance; read BEFORE ARMING by tierc10_panel's import "
        "(IMPORT_TC10_READS); refused after arming",
}
# TC10 records a TC10 module reads AT IMPORT, inside its env window, BEFORE the
# hook is armed (L-0.3: the hook is installed last).  Unavoidable without editing
# TC10 code; declared per window, and any OTHER unlisted TC10 read during a
# window HALTs the shim.  {record: (window label, reason)}
IMPORT_TC10_READS = {
    "research_outputs/tierc10/data/STAGE_D_MANIFEST.json":
        ("tierc10_panel", "TP.resolve_unseen12() runs at import on TC10's record; "
                          "TP._U12 is re-resolved from TC11's manifest after the windows"),
}
AUDIT_EXIT_CODE = 70                # the forced exit of a process that saw a BLOCKED attempt


class AuditHalt(SystemExit):
    """Raised by the audit hook.  A SystemExit, so `except Exception` (pandas,
    TP.resolve_unseen12, …) cannot swallow a substrate violation."""


# ══════════════════════════════════════════════════════ 1 · THE SUBSTRATE GUARD
def guard_substrate(env: str | None) -> Path:
    """HALTS IF NAIAD_CACHE_DIR is unset; names the live cache or the TC10
    snapshot (tested on the path STRING first, then resolved); is anything but
    the TC11 snapshot; or the TC11 snapshot has no klines/.  Runs BEFORE any
    engine import: tierc2_baseline binds its paths at import."""
    if not env:
        raise SystemExit(f"HALT: NAIAD_CACHE_DIR is unset — TC11 reads ONLY {SNAPSHOT}; "
                         f"export it BEFORE python starts")
    norm = Path(os.path.normpath(os.path.expanduser(env)))
    for bad, why in ((LIVE_CACHE, "the LIVE cache — READ-NEVER, WRITE-NEVER"),
                     (TC10_SNAPSHOT, "the TC10 snapshot — TC11 binds tc11_20260925")):
        if (norm == bad or bad in norm.parents or norm.resolve() == bad.resolve()
                or bad.resolve() in norm.resolve().parents):
            raise SystemExit(f"HALT: NAIAD_CACHE_DIR={norm} names {why}")
    got = norm.resolve()
    if got != SNAPSHOT.resolve():
        raise SystemExit(f"HALT: NAIAD_CACHE_DIR={got} is not the TC11 snapshot {SNAPSHOT}")
    if not (got / "klines").is_dir():
        raise SystemExit(f"HALT: the TC11 snapshot has no klines/ directory: {got}")
    return got


_ENV_OF_RECORD = os.environ.get("NAIAD_CACHE_DIR")
guard_substrate(_ENV_OF_RECORD)


def _main_tree(root: Path) -> Path:
    """The main working tree: `root` itself, or — in a linked worktree whose
    .git is a `gitdir:` file — the tree that owns .git/worktrees/<name>.
    TC10 records are read there by absolute path [L-0.3, L-F.3]."""
    g = root / ".git"
    if g.is_file():
        txt = g.read_text(encoding="utf-8").strip()
        if txt.startswith("gitdir:"):
            gd = Path(txt.split(":", 1)[1].strip())
            gd = gd if gd.is_absolute() else (root / gd).resolve()
            if gd.parent.name == "worktrees" and gd.parent.parent.name == ".git":
                return gd.parent.parent.parent
    return root


MAIN_TREE = _main_tree(ROOT)


# ══════════════════════════════════════════════════ 2 · PATH CLASSIFICATION
# A path is judged by its CANONICAL form [verifier MAJOR-2]: realpath (symlinks),
# then the deepest EXISTING ancestor matched by (st_dev, st_ino) against the
# registered roots (catches a case variant, the /System/Volumes/Data firmlink,
# the /.nofollow and /.resolve/N prefixes and any other volume alias of an
# existing directory), then NFC + casefold (APFS here is case-insensitive;
# casefolding can only over-protect on a case-sensitive volume), then the known
# alias prefixes stripped as strings (a path none of whose ancestors exists).
def _real(p) -> str:
    return os.path.realpath(os.path.abspath(str(p)))


def _under(s: str, root: str) -> bool:
    """s is `root` or inside it (the filesystem root "/" contains everything)."""
    return s == root or s.startswith(root.rstrip(os.sep) + os.sep)


def _ino(p: str):
    try:
        st = os.stat(p)
    except (OSError, ValueError):
        return None
    return (st.st_dev, st.st_ino)


_FIRMLINK = "/system/volumes/data"
_NOFOLLOW = "/.nofollow"
_RESOLVE_RX = re.compile(r"^/\.resolve/\d+(?=/|$)")


def _strip_aliases(cf: str) -> str:
    """Casefolded path -> the same path with the macOS volume-alias prefixes
    removed (repeatedly: they nest)."""
    while True:
        if cf == _FIRMLINK or cf.startswith(_FIRMLINK + "/"):
            cf = cf[len(_FIRMLINK):] or "/"
        elif cf == _NOFOLLOW or cf.startswith(_NOFOLLOW + "/"):
            cf = cf[len(_NOFOLLOW):] or "/"
        elif (m := _RESOLVE_RX.match(cf)) is not None:
            cf = cf[m.end():] or "/"
        else:
            return cf


def _cf(s: str) -> str:
    return _strip_aliases(unicodedata.normalize("NFC", s).casefold())


_R_TC10_SNAP = _real(TC10_SNAPSHOT)
_R_LIVE = _real(LIVE_CACHE)
_R_TC11_SNAP = _real(SNAPSHOT)
_R_HOME = _real(HOME)
_TREES = tuple(dict.fromkeys((_real(ROOT), _real(MAIN_TREE))))
_R_INTERP = tuple(dict.fromkeys(os.path.realpath(p) for p in (
    sys.prefix, sys.base_prefix, sys.exec_prefix, sys.base_exec_prefix) if p))
# (st_dev, st_ino) -> the root's real path, for every root a path is judged
# against.  The home directory is registered last so a deeper root wins (the walk
# goes deepest-first anyway).  A root that does not exist is simply absent.
_ALIAS_ROOTS: dict = {}
for _p in (_R_TC10_SNAP, _R_LIVE, _R_TC11_SNAP, *_TREES, *_R_INTERP, _R_HOME):
    _k = _ino(_p)
    if _k is not None and _k not in _ALIAS_ROOTS:
        _ALIAS_ROOTS[_k] = _p


def _inode_rewrite(real: str) -> str:
    """`real` re-anchored on the deepest existing ancestor that IS a registered
    root (same device + inode), keeping the tail as given; `real` itself when no
    ancestor is a registered root."""
    p, tail = real, []
    while True:
        k = _ino(p)
        if k is not None:
            root = _ALIAS_ROOTS.get(k)
            if root is not None:
                return os.path.join(root, *reversed(tail)) if tail else root
        head, name = os.path.split(p)
        if head == p or not name:
            return real
        tail.append(name)
        p = head


def _canon(real: str) -> str:
    """The canonical (casefolded) form every protection compares."""
    if not os.path.isabs(real):
        real = os.path.abspath(real)
    return _cf(_inode_rewrite(real))


_C_TC10_SNAP = _canon(_R_TC10_SNAP)
_C_LIVE = _canon(_R_LIVE)
_C_TC11_SNAP = _canon(_R_TC11_SNAP)
_C_TREES = tuple(dict.fromkeys(_canon(t) for t in _TREES))
_C_INTERP = tuple(dict.fromkeys(_canon(p) for p in _R_INTERP))
_C_TC10_OUT = tuple(os.path.join(t, "research_outputs", "tierc10") for t in _C_TREES)
_C_PROTECT_DIRS = tuple((os.path.join(t, "research_outputs", d), lab) for t in _C_TREES
                        for d, lab in (("tierc10", "tierc10-write"),
                                       ("tierc10_run2", "tierc10_run2-write")))
_C_PROTECT_PREFIX = tuple((os.path.join(t, *rel), lab) for t in _C_TREES
                          for rel, lab in ((("scripts", "tierc10_"), "tierc10-script-write"),
                                           (("exchange", "status", "ledger"), "ledger-write")))
_C_PROTECT_FILES = tuple((os.path.join(t, f), lab) for t in _C_TREES
                         for f, lab in (("ledger.md", "ledger-write"),
                                        (".gitignore", "gitignore-write")))
_C_ALLOW = {os.path.join(t, *_cf(rel).split("/")): rel for t in _C_TREES for rel in TC10_ALLOW}
_C_CANDIDATE = {os.path.join(t, *_cf(rel).split("/")): rel for t in _C_TREES
                for rel in TC10_AMENDMENT_CANDIDATES}
_C_IMPORT_READS = {os.path.join(t, *_cf(rel).split("/")): rel for t in _C_TREES
                   for rel in IMPORT_TC10_READS}
# the roots a DIRECTORY open may not be an ancestor of (or equal to): a dir_fd on
# any of them turns a relative path into an unjudgeable one [MINOR-3]
_C_DIR_GUARD = tuple(dict.fromkeys(
    [_C_TC10_SNAP, _C_LIVE] + [d for d, _ in _C_PROTECT_DIRS]
    + [os.path.dirname(p) for p, _ in _C_PROTECT_PREFIX] + list(_C_TREES)))
# the OS roots a data open may come from — specific system subdirectories, never
# the whole of /System (its Volumes/Data firmlink aliases every user path)
_R_OS = ("/System/Library", "/System/Cryptexes", "/System/iOSSupport",
         "/usr/lib", "/usr/share", "/dev", "/private/etc", "/etc",
         "/Library/Preferences", "/private/var/db/timezone")
_C_OS = tuple(r.casefold() for r in _R_OS)


def _norm_arg(p, anchor: str | None = None, fd_ok: bool = False) -> str | None:
    """An audit-event path argument -> its real absolute path.  A relative path
    is anchored on `anchor` (a dir_fd's path / a glob root_dir) when given, else
    on the working directory.  An int is an fd: resolved only when `fd_ok`
    (listing through an fd), else None."""
    if p is None:
        return None
    if isinstance(p, int):
        return _fd_path(p) if fd_ok else None
    try:
        s = os.fsdecode(os.fspath(p))
    except TypeError:
        return None
    if not s:
        return None
    if anchor and not os.path.isabs(s):
        s = os.path.join(anchor, s)
    try:
        return os.path.realpath(os.path.abspath(s))
    except (OSError, ValueError):
        return os.path.abspath(s)


def _fd_path(fd) -> str | None:
    """The path an open fd names (F_GETPATH on darwin, /proc elsewhere)."""
    if not isinstance(fd, int) or fd < 0:
        return None
    try:
        if hasattr(fcntl, "F_GETPATH"):
            b = fcntl.fcntl(fd, fcntl.F_GETPATH, bytes(1024))
            return os.path.realpath(os.fsdecode(b.split(b"\0", 1)[0])) or None
        return os.path.realpath(os.readlink(f"/proc/self/fd/{fd}"))
    except (OSError, ValueError):
        return None


def classify(real: str) -> str:
    """One word per path, judged on its CANONICAL form: tc10-snapshot ·
    live-cache · tc11-snapshot · tc10-allow · tc10-unlisted · repo ·
    interpreter · os · other."""
    c = _canon(real)
    if _under(c, _C_TC10_SNAP):
        return "tc10-snapshot"
    if _under(c, _C_LIVE):
        return "live-cache"
    if _under(c, _C_TC11_SNAP):
        return "tc11-snapshot"
    if c in _C_ALLOW:
        return "tc10-allow"
    if any(_under(c, d) for d in _C_TC10_OUT):
        return "tc10-unlisted"
    if any(_under(c, t) for t in _C_TREES):
        return "repo"
    if any(_under(c, t) for t in _C_INTERP):
        return "interpreter"
    if any(_under(c, t) for t in _C_OS):
        return "os"
    return "other"


def _protected_write(real: str) -> str | None:
    """The protected class a WRITE to `real` would violate, or None (canonical)."""
    c = _canon(real)
    for d, lab in _C_PROTECT_DIRS:
        if _under(c, d):
            return lab
    for p, lab in _C_PROTECT_PREFIX:
        if c.startswith(p):
            return lab
    for f, lab in _C_PROTECT_FILES:
        if c == f:
            return lab
    return None


def _dir_guarded(real: str) -> bool:
    """A directory that may not be opened (as a future dir_fd): an ancestor of,
    or equal to, a guarded root, or a directory inside write-protected space."""
    c = _canon(real)
    return any(_under(r, c) for r in _C_DIR_GUARD) or _protected_write(real) is not None


def rel_of(real: str) -> str:
    """A deterministic rendering (re-anchored on a registered root when the path
    is an alias): tree-relative, else ~-relative, else as is."""
    s = _inode_rewrite(real) if os.path.isabs(real) else real
    for t in _TREES:
        if _under(s, t):
            return os.path.relpath(s, t)
    if s == _R_HOME:
        return "~"
    if _under(s, _R_HOME):
        return "~/" + os.path.relpath(s, _R_HOME)
    return s


def _show_path(real: str) -> str:
    """rel_of, plus the spelling actually used when it was an alias."""
    shown = rel_of(real)
    if os.path.isabs(real) and _inode_rewrite(real) != real:
        raw = ("~/" + os.path.relpath(real, _R_HOME)) if _under(real, _R_HOME) else real
        shown += f" (opened as {raw})"
    elif os.path.isabs(real) and _cf(real) != unicodedata.normalize("NFC", real).casefold():
        shown += f" (opened as {real})"
    return shown


_WFLAGS = (os.O_WRONLY | os.O_RDWR | os.O_APPEND | os.O_CREAT | os.O_TRUNC
           | getattr(os, "O_EXCL", 0))


def _is_write(mode, flags) -> bool:
    if isinstance(flags, int) and flags & _WFLAGS:
        return True
    return isinstance(mode, str) and any(ch in mode for ch in "wax+")


# event -> how its arguments are read: (path arg index, dir_fd arg index or
# None, is_write).  The dir_fd positions are CPython 3.12's audit signatures:
# os.remove/rmdir (path, dir_fd) · os.mkdir/chmod (path, mode, dir_fd) ·
# os.chown (path, uid, gid, dir_fd) · os.utime (path, times, ns, dir_fd) ·
# os.rename/link (src, dst, src_dir_fd, dst_dir_fd) · os.symlink (src, dst,
# dir_fd) · shutil.rmtree (path, dir_fd) · glob.glob/2 (path, recursive,
# root_dir, dir_fd).  A listing through an fd (os.scandir(fd)) is resolved.
_READ_EVENTS = {"os.listdir": ((0, None, False),), "os.scandir": ((0, None, False),),
                "glob.glob": ((0, None, False),), "glob.glob/2": ((0, 3, False),)}
_MUTATE_EVENTS = {
    "os.mkdir": ((0, 2, True),), "os.remove": ((0, 1, True),), "os.rmdir": ((0, 1, True),),
    "os.truncate": ((0, None, True),), "os.chmod": ((0, 2, True),),
    "os.chown": ((0, 3, True),), "os.utime": ((0, 3, True),),
    "os.chflags": ((0, None, True),), "os.lchflags": ((0, None, True),),
    "os.setxattr": ((0, None, True),), "os.removexattr": ((0, None, True),),
    "shutil.rmtree": ((0, 1, True),),
    "os.rename": ((0, 2, True), (1, 3, True)), "os.link": ((0, 2, False), (1, 3, True)),
    "os.symlink": ((0, None, False), (1, 2, True)),
    "shutil.copyfile": ((0, None, False), (1, None, True)),
    "shutil.copytree": ((0, None, False), (1, None, True)),
    "shutil.move": ((0, None, True), (1, None, True)),
    "shutil.copymode": ((0, None, False), (1, None, True)),
    "shutil.copystat": ((0, None, False), (1, None, True)),
}
_PATH_EVENTS = frozenset({"open"} | set(_READ_EVENTS) | set(_MUTATE_EVENTS))


def _open_dir_fds() -> list[str]:
    """The paths of every DIRECTORY fd this process holds open right now
    (enumerated through /dev/fd; each fstat'ed, then F_GETPATH)."""
    try:
        names = os.listdir("/dev/fd")
    except OSError:
        return []
    out = []
    for x in names:
        try:
            fd = int(x)
            if not stat.S_ISDIR(os.fstat(fd).st_mode):
                continue
        except (ValueError, OSError):
            continue
        p = _fd_path(fd)
        if p and p not in out:
            out.append(p)
    return out


def _relative_open(args) -> str | None:
    """The raw path of an "open" event when it is a RELATIVE path string."""
    if not args or args[0] is None or isinstance(args[0], int):
        return None
    try:
        raw = os.fsdecode(os.fspath(args[0]))
    except TypeError:
        return None
    return raw if raw and not os.path.isabs(raw) else None


def _alt_open_paths(args, raw: str, dir_fds: list[str]) -> list[tuple[str, bool]]:
    """A RELATIVE "open" may be dir_fd-relative — the audit event does not carry
    the dir_fd [MINOR-3].  The real anchor is the working directory or one of the
    directory fds open right now, so the path is ALSO resolved against every one
    of them (a sound over-approximation: `..` and symlinks included), and each
    candidate is judged like the path itself."""
    mode = args[1] if len(args) > 1 else None
    flags = args[2] if len(args) > 2 else None
    w = _is_write(mode, flags)
    first = _norm_arg(raw)
    out = []
    for d in dir_fds:
        r = _norm_arg(raw, anchor=d)
        if r and r != first and (r, w) not in out:
            out.append((r, w))
    return out


def _event_paths(event: str, args) -> list[tuple[str, bool]]:
    if event == "open":
        mode = args[1] if len(args) > 1 else None
        flags = args[2] if len(args) > 2 else None
        r = _norm_arg(args[0]) if args else None
        return [(r, _is_write(mode, flags))] if r else []
    spec = _READ_EVENTS.get(event) or _MUTATE_EVENTS.get(event) or ()
    out = []
    for i, j, w in spec:
        if len(args) <= i:
            continue
        anchor = None
        if j is not None and len(args) > j and isinstance(args[j], int) and args[j] >= 0:
            anchor = _fd_path(args[j])
        elif event == "glob.glob/2" and len(args) > 2 and args[2]:
            try:
                anchor = os.fsdecode(os.fspath(args[2]))
            except TypeError:
                anchor = None
        r = _norm_arg(args[i], anchor=anchor, fd_ok=event in _READ_EVENTS)
        if r:
            out.append((r, w))
    return out


# ═════════════════════════════════════ 3 · THE IMPORT WINDOW + RECORDING HOOK
_WIN: dict = {"label": None, "events": None}
IMPORT_AUDIT: list[dict] = []           # one record per import statement


def _record_hook(event, args):          # inert outside a window
    if _WIN["label"] is None or event not in _PATH_EVENTS:
        return
    for real, w in _event_paths(event, args):
        _WIN["events"].append((event, real, w))


sys.addaudithook(_record_hook)


def _code_file(real: str) -> bool:
    return real.endswith((".py", ".pyc", ".so", ".pth", ".dylib", ".pyd"))


@contextlib.contextmanager
def _window(label: str, env_to: Path | None):
    """NAIAD_CACHE_DIR -> `env_to` for the duration of ONE import statement
    (None = leave the TC11 env as is), restored in `finally`.  Every path the
    import touches is recorded; a touch of the TC10 snapshot or the live cache, a
    write under a protected root, or a read under research_outputs/tierc10 that
    is neither on TC10_ALLOW nor declared for THIS window in IMPORT_TC10_READS,
    HALTs."""
    before = set(sys.modules)
    prev = os.environ.get("NAIAD_CACHE_DIR")
    if env_to is not None:
        os.environ["NAIAD_CACHE_DIR"] = str(env_to)
    _WIN["label"], _WIN["events"] = label, []
    try:
        yield
    finally:
        events, _WIN["label"], _WIN["events"] = _WIN["events"], None, None
        if prev is None:
            os.environ.pop("NAIAD_CACHE_DIR", None)
        else:
            os.environ["NAIAD_CACHE_DIR"] = prev
    new_mods = sorted(set(sys.modules) - before)
    cls_of: dict[str, str] = {}
    for _, r, _ in events:
        if r not in cls_of:
            cls_of[r] = classify(r)

    def shown_class(r: str) -> str:
        c = cls_of[r]
        if c == "tc10-unlisted" and _declared_import_read(r, label):
            return "tc10-import-read"
        return c

    bad = [(e, r) for e, r, w in events if cls_of[r] in ("tc10-snapshot", "live-cache")]
    badw = [(e, r, _protected_write(r)) for e, r, w in events if w and _protected_write(r)]
    unl = sorted({rel_of(r) for e, r, w in events if shown_class(r) == "tc10-unlisted"})
    data_opens = sorted({(shown_class(r), rel_of(r)) for e, r, w in events
                         if e == "open" and not _code_file(r)
                         and cls_of[r] not in ("interpreter", "os")})
    src_reads = sorted({rel_of(r) for e, r, w in events
                        if e == "open" and r.endswith(".py") and cls_of[r] == "repo"
                        and _dotted(r) is not None and _dotted(r) not in sys.modules})
    IMPORT_AUDIT.append({"label": label,
                         "env": "tc10_20260921" if env_to is not None else "tc11_20260925",
                         "new_modules": new_mods, "data_opens": data_opens,
                         "source_reads_not_imports": src_reads,
                         "tc10_snapshot_or_live_touches": [rel_of(r) for _, r in bad],
                         "protected_writes": [rel_of(r) for _, r, _ in badw],
                         "tc10_unlisted_reads": unl})
    if bad:
        raise SystemExit(
            f"HALT: IMPORT WINDOW {label}: touched {len(bad)} path(s) under the TC10 "
            f"snapshot / live cache AT IMPORT (e.g. {bad[0][0]} {_show_path(bad[0][1])}) — "
            f"a module that reads TC10 DATA at import cannot be re-used by the shim [L-0.3]")
    if badw:
        raise SystemExit(f"HALT: IMPORT WINDOW {label}: a protected write at import "
                         f"({badw[0][2]}: {_show_path(badw[0][1])})")
    if unl:
        raise SystemExit(f"HALT: IMPORT WINDOW {label}: read {len(unl)} TC10 record(s) "
                         f"neither on the L-0.3 allow-list nor declared for this window "
                         f"in IMPORT_TC10_READS (e.g. {unl[0]}) [L-0.3]")


def _declared_import_read(real: str, label: str) -> bool:
    c = _canon(real)
    rel = _C_IMPORT_READS.get(c)
    return rel is not None and IMPORT_TC10_READS[rel][0] == label


def _dotted(real: str) -> str | None:
    """repo .py path -> the dotted module name it would import as (scripts/ on
    the path: scripts/x.py -> 'x'; engine/x.py -> 'engine.x')."""
    for t in _TREES:
        if _under(real, t):
            rel = Path(os.path.relpath(real, t))
            parts = rel.with_suffix("").parts
            if parts and parts[0] == "scripts":
                parts = parts[1:]
            if parts and parts[-1] == "__init__":
                parts = parts[:-1]
            return ".".join(parts) if parts else None
    return None


def _forbidden(name: str) -> bool:
    return any(f in name for f in FORBIDDEN_MODULE_SUBSTRINGS)


NEST_MODULE = "tierc11_nest"            # the ONLY module the range door opens for


def _caller_is_nest(depth: int = 2) -> tuple[bool, str]:
    """(True, name) iff the frame `depth` levels up belongs to tierc11_nest —
    imported as `tierc11_nest`, or run as a script whose file is
    tierc11_nest.py."""
    g = sys._getframe(depth).f_globals
    name = str(g.get("__name__"))
    f = os.path.basename(str(g.get("__file__") or ""))
    return (name == NEST_MODULE or (name == "__main__" and f == NEST_MODULE + ".py")), name


def tc10_import(name: str, allow_range: bool = False):
    """Import ONE TC10-guarded module inside an env window (for tierc11_nest's
    second window).  A range module needs `allow_range=True` AND a caller that
    IS tierc11_nest [verifier MINOR-6]: any other module — tierc11_env itself
    included — HALTs, so a decision module cannot reach the range machine
    through this door even with the name held in a variable [L-0.3]."""
    if _forbidden(name):
        is_nest, caller = _caller_is_nest()
        if not (allow_range and is_nest):
            raise SystemExit(f"HALT: tc10_import({name!r}) from {caller!r} — a range "
                             f"module; only {NEST_MODULE} may import it "
                             f"(allow_range=True) [L-0.3]")
    with _window(name, TC10_SNAPSHOT):
        return importlib.import_module(name)


# ══════════════════════════════════════ 4 · THE IMPORTS — TB FIRST, THEN WINDOWS
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

with _window("tierc2_baseline", None):          # FIRST, under the TC11 env
    import tierc2_baseline as TB                                     # noqa: E402

with _window("tierc10_data", TC10_SNAPSHOT):
    import tierc10_data as D                                         # noqa: E402
with _window("tierc10_panel", TC10_SNAPSHOT):
    import tierc10_panel as TP                                       # noqa: E402
with _window("tierc10_brk", TC10_SNAPSHOT):
    import tierc10_brk as BK                                         # noqa: E402
with _window("tierc10_lanes", TC10_SNAPSHOT):
    import tierc10_lanes as LN                                       # noqa: E402
with _window("tierc9", TC10_SNAPSHOT):
    import tierc9 as T9                                              # noqa: E402
with _window("tierc8", TC10_SNAPSHOT):
    import tierc8 as T8                                              # noqa: E402
with _window("tierc7", TC10_SNAPSHOT):
    import tierc7 as T7                                              # noqa: E402
with _window("tierc7_rules", TC10_SNAPSHOT):
    import tierc7_rules as R7                                        # noqa: E402
with _window("tierc7_lab_regime", TC10_SNAPSHOT):
    import tierc7_lab_regime as LAB                                  # noqa: E402
with _window("tierc6", TC10_SNAPSHOT):
    import tierc6 as T6                                              # noqa: E402
with _window("tierc6_rules", TC10_SNAPSHOT):
    import tierc6_rules as R6                                        # noqa: E402
with _window("tierc5", TC10_SNAPSHOT):
    import tierc5 as T5                                              # noqa: E402
with _window("tierc5_rules", TC10_SNAPSHOT):
    import tierc5_rules as R5                                        # noqa: E402
with _window("tierc4_rules", TC10_SNAPSHOT):
    import tierc4_rules as R4                                        # noqa: E402
with _window("tierc3_rules", TC10_SNAPSHOT):
    import tierc3_rules as R3                                        # noqa: E402
with _window("tierc2_rules", TC10_SNAPSHOT):
    import tierc2_rules as R2                                        # noqa: E402

if os.environ.get("NAIAD_CACHE_DIR") != _ENV_OF_RECORD:
    raise SystemExit("HALT: the import windows did not restore NAIAD_CACHE_DIR "
                     f"(now {os.environ.get('NAIAD_CACHE_DIR')!r})")
_SUB_BEFORE_REROOT = dict(TP._SUB)
_TP_OPEN_MEMO_BEFORE = len(TP._OPEN)
_LN_FIVE_BEFORE = len(LN._FIVE)
_BK_FRAMES_BEFORE = len(BK._FRAMES)

# ══════════════════════════════════════════════ 5 · THE CLOSED RE-ROOT LIST
_MODS = {"D": D, "TP": TP, "BK": BK, "LN": LN}
_NEW_RERUN = OUT / "_det_rerun"
# (module, attribute, key-or-None, new value, provenance).  key != None = in
# place on that dict.  "L-0.3" = the lean's closed list; "L-0.3+" = a binding
# the list missed, found by grep (tierc10 / tc10_20260921 / AS_OF_PIN / STAGE_D
# / SEED / OUT) and re-rooted under the same law.
REROOT_PLAN = (
    ("D", "SNAPSHOT", None, SNAPSHOT, "L-0.3"),
    ("D", "OUT", None, OUT / "data", "L-0.3"),
    ("D", "STEP_MS", "15m", LENS_MS["15m"], "L-0.3"),
    ("D", "SEED", None, SEED, "L-0.3+ missed: Stage D's seed, bound at import"),
    ("TP", "OUT", None, OUT, "L-0.3"),
    ("TP", "OUT_RERUN", None, _NEW_RERUN, "L-0.3 (rerun twin under tierc11/_det_rerun)"),
    ("TP", "AS_OF_PIN", None, OUT / "data" / "AS_OF_PIN.json", "L-0.3"),
    ("TP", "STAGE_D_MANIFEST", None, OUT / "data" / "STAGE_D_MANIFEST.json", "L-0.3"),
    ("TP", "SEED", None, SEED, "L-0.3"),
    ("TP", "SEEDS", None, (SEED, SEED_SENS), "L-0.3+ missed: (SEED, SEED_LINEAGE) copied at import"),
    ("BK", "SEED", None, SEED, "L-0.3"),
    ("BK", "OUT", None, OUT / "brk", "L-0.3"),
    ("BK", "OUT_RERUN", None, _NEW_RERUN / "brk", "L-0.3"),
    ("BK", "LENS_MS", "15m", LENS_MS["15m"], "L-0.3 (dict(D.STEP_MS) copied at import)"),
    ("BK", "TUNING_RESULT_FOR", "5m", OUT / "census" / "TUNING_RESULT.json", "L-0.3"),
    ("BK", "TUNING_RESULT_FOR", "1d", OUT / "census" / "TUNING_RESULT_1d.json", "L-0.3"),
    ("BK", "TUNING_RESULT", None, OUT / "census" / "TUNING_RESULT.json",
     "L-0.3+ missed: TUNING_RESULT_FOR['5m'] copied at import"),
    ("BK", "HEIGHT_VS_TOLL_PATH", None, OUT / "census" / "height_toll.parquet", "L-0.3"),
    ("BK", "HEIGHT_VS_TOLL_VERDICT_PATH", None,
     OUT / "census" / "height_toll_verdict.parquet", "L-0.3"),
    ("BK", "REGISTRY_PIN_PATH", None, OUT / "REGISTRY_PIN.json", "L-0.3"),
    ("BK", "REGISTRATION_TEXTS_PATH", None, OUT / "REGISTRATION_TEXTS.json", "L-0.3"),
    ("LN", "SEED", None, SEED, "L-0.3"),
    ("LN", "OUT", None, OUT / "lanes", "L-0.3"),
    ("LN", "REGISTRY_PIN_PATH", None, OUT / "REGISTRY_PIN.json", "L-0.3"),
    ("LN", "REGISTRATION_TEXTS_PATH", None, OUT / "REGISTRATION_TEXTS.json", "L-0.3"),
)
# TC10 bindings deliberately LEFT, each with its reason.  Anything else still
# naming research_outputs/tierc10 HALTs the post-shim assertion.
NOT_REROOTED = {
    "TP.REG_DIR": "L-1.4: TP.REG_DIR is left untouched — TC11 never routes through "
                  "a TP registry door; the audit hook refuses any write there",
    "D.LIVE_CACHE": "a GUARD constant: the path assert_substrate refuses, never read",
    "TP.LIVE_CACHE": "a GUARD constant: the path TP.substrate() refuses, never read",
    "D.SPEND_EXCLUDED_DIRS": "TC10's data-spend audit EXCLUSION filter (directories its "
                             "grep skips); not an output root, never written; TC11 never "
                             "runs TC10's data-spend audit",
}
REROOTS: list[dict] = []


def _show(v) -> str:
    if isinstance(v, Path):
        return rel_of(_real(v))
    if isinstance(v, dict):
        return "{" + ", ".join(f"{k}: {_show(v[k])}" for k in sorted(v, key=str)) + "}"
    if isinstance(v, tuple):
        return "(" + ", ".join(_show(x) for x in v) + ")"
    return repr(v)


def _reroot(alias: str, attr: str, key, new, why: str) -> None:
    mod = _MODS[alias]
    if not hasattr(mod, attr):
        raise SystemExit(f"HALT: RE-ROOT {alias}.{attr}: no such name in "
                         f"{mod.__name__} — the closed list names a binding that "
                         f"does not exist [L-0.3]")
    cur = getattr(mod, attr)
    if key is None:
        old = cur
        setattr(mod, attr, new)
        name = f"{alias}.{attr}"
    else:
        if not isinstance(cur, dict):
            raise SystemExit(f"HALT: RE-ROOT {alias}.{attr}[{key!r}]: not a dict")
        old = cur.get(key, "(absent)")
        cur[key] = new                      # IN PLACE: every holder of the dict sees it
        name = f"{alias}.{attr}[{key!r}]"
    REROOTS.append({"name": name, "old": _show(old), "new": _show(new), "why": why})


for _alias, _attr, _key, _new, _why in REROOT_PLAN:
    _reroot(_alias, _attr, _key, _new, _why)

# The twelve re-resolved from TC11's OWN Stage D manifest (TP resolved them at
# import from TC10's record — a TC10 binding the list missed) [L-0.3+].
_U12_TC10 = copy.deepcopy(TP._U12)
_U12_TC11 = TP.resolve_unseen12(TP.STAGE_D_MANIFEST)
TP._U12.clear()
TP._U12.update(_U12_TC11)                   # in place: admission() reads TP._U12
TP.UNSEEN12_SOURCE = _U12_TC11["source"]
TP.UNSEEN12_NAME_OF = {s: n for n, s in _U12_TC11["symbol_of"].items() if s}
TP.UNSEEN12_UNRESOLVED = tuple(n for n in TP.UNSEEN12_CONTRACT if not _U12_TC11["symbol_of"][n])
_UNSEEN12_TC10 = TP.UNSEEN12
_PANEL17_TC10 = TP.PANEL17
TP.UNSEEN12 = tuple(_U12_TC11["symbol_of"][n] for n in TP.UNSEEN12_CONTRACT
                    if _U12_TC11["symbol_of"][n])
TP.PANEL17 = TP.CLASSIC5 + tuple(
    _U12_TC11["symbol_of"][n] for n in TP.UNSEEN12_CONTRACT
    if _U12_TC11["symbol_of"][n]
    and (_U12_TC11["manifest_admitted"] is None
         or _U12_TC11["manifest_admitted"][n] is not False))
REROOTS.append({"name": "TP._U12 (+UNSEEN12_SOURCE/NAME_OF/UNRESOLVED, UNSEEN12, PANEL17)",
                "old": "resolved at import from research_outputs/tierc10/data/STAGE_D_MANIFEST.json",
                "new": "re-resolved from research_outputs/tierc11/data/STAGE_D_MANIFEST.json",
                "why": "L-0.3+ missed: resolve_unseen12() runs at import on TC10's record"})

CLASSIC5 = tuple(TP.CLASSIC5)
UNSEEN12 = tuple(TP.UNSEEN12)
PANEL17 = tuple(TP.PANEL17)


# ═══════════════════════════════════════════════ 6 · THE POST-SHIM ASSERTION
def _leaves(name: str, v):
    if isinstance(v, (str, Path)):
        yield name, v
    elif isinstance(v, dict):
        for k in sorted(v, key=str):
            if isinstance(v[k], (str, Path)):
                yield f"{name}[{k!r}]", v[k]
    elif isinstance(v, (tuple, list)):
        for i, x in enumerate(v):
            if isinstance(x, (str, Path)):
                yield f"{name}[{i}]", x
    elif isinstance(v, (set, frozenset)):
        for x in sorted((x for x in v if isinstance(x, (str, Path))), key=str):
            yield f"{name}{{{x!s}}}", x


def _pathish(v) -> str | None:
    if isinstance(v, Path):
        return str(v)
    if isinstance(v, str) and "/" in v and not any(ch.isspace() for ch in v):
        return v
    return None


def _estate_modules() -> list:
    """Every loaded module whose file lives in this tree (scripts/, engine/,
    analytics/), in name order — except __main__ and TC11's own modules
    (tierc11_*), which hold the guard constants that NAME the TC10 snapshot in
    order to refuse it."""
    out = []
    for name in sorted(sys.modules):
        m = sys.modules[name]
        f = getattr(m, "__file__", None)
        if (not f or name == "__main__" or name.startswith("tierc11_")
                or m is sys.modules.get(__name__)):
            continue
        if any(_under(os.path.realpath(f), t) for t in _TREES):
            out.append((name, m))
    return out


_ALIAS_OF = {"tierc10_data": "D", "tierc10_panel": "TP", "tierc10_brk": "BK",
             "tierc10_lanes": "LN"}


def tc10_bindings() -> list[dict]:
    """Every module-level str/Path (one container level deep) in the estate's
    loaded modules that names the TC10 snapshot, the live cache or
    research_outputs/tierc10[_run2].  Prose (a string with whitespace) is not a
    binding.  Returns rows with the verdict: declared / guard / UNDECLARED."""
    rows = []
    tc10_snap = str(TC10_SNAPSHOT)
    live = str(LIVE_CACHE)
    for mname, m in _estate_modules():
        alias = _ALIAS_OF.get(mname, mname)
        for k, v in sorted(vars(m).items()):
            if k.startswith("__"):
                continue
            for sub, val in _leaves(k, v):
                s = _pathish(val)
                if s is None:
                    continue
                hit = ("tc10-snapshot" if ("tc10_20260921" in s or tc10_snap in s) else
                       "live-cache" if (live in s or ".cache/naiad/data_cache" in s) else
                       "tierc10-out" if ("research_outputs/tierc10" in s) else None)
                if hit is None:
                    continue
                full = f"{alias}.{sub}"
                decl = NOT_REROOTED.get(full) or NOT_REROOTED.get(f"{alias}.{k}")
                rows.append({"name": full, "kind": hit, "value": rel_of(_real(Path(s)))
                             if os.path.isabs(s) else s,
                             "declared": decl})
    return rows


POST_SHIM: list[str] = []


def _post_shim() -> None:
    bad: list[str] = []

    def chk(ok: bool, clause: str, detail: str) -> None:
        POST_SHIM.append(f"{'ok ' if ok else 'BAD'} {clause}: {detail}")
        if not ok:
            bad.append(f"{clause}: {detail}")

    kl = _real(TB.KLINES)
    chk(kl == _real(SNAPSHOT / "klines") and _real(TB.FUNDING) == _real(SNAPSHOT / "funding"),
        "TB.KLINES/FUNDING", f"{rel_of(kl)} · {rel_of(_real(TB.FUNDING))}")
    stray = [f"{n}.{g}" for n, m in _estate_modules() for g in ("KLINES", "FUNDING")
             if isinstance(getattr(m, g, None), Path)
             and not _under(_real(getattr(m, g)), _R_TC11_SNAP)]
    chk(not stray, "every KLINES/FUNDING binding under tc11_20260925",
        f"{len(stray)} stray {stray[:4]}")
    chk(not _SUB_BEFORE_REROOT, "TP._SUB empty after the windows",
        f"{_SUB_BEFORE_REROOT or '{}'}")
    chk(_TP_OPEN_MEMO_BEFORE == 0 and _LN_FIVE_BEFORE == 0 and _BK_FRAMES_BEFORE == 0,
        "no bar memo filled during the windows",
        f"TP._OPEN {_TP_OPEN_MEMO_BEFORE} · LN._FIVE {_LN_FIVE_BEFORE} · BK._FRAMES {_BK_FRAMES_BEFORE}")
    sub = TP.substrate()["substrate"]
    chk(sub == SNAPSHOT.name, "TP.substrate()", sub)
    try:
        dpin = int(D.load_pin()["as_of_last_closed_4h_close_ms"])
    except SystemExit as e:
        dpin = f"HALT {e}"
    chk(dpin == PIN_MS, "D.load_pin()", f"{dpin}"
        + (" (the TC10 pin LEAKED)" if dpin == TC10_PIN_MS else "") + f" vs {PIN_MS}")
    tpin = TP.stage_d_pin()
    chk(tpin == PIN_MS, "TP.stage_d_pin()", f"{tpin}"
        + (" (the TC10 pin LEAKED)" if tpin == TC10_PIN_MS else "") + f" vs {PIN_MS}")
    kp = _real(D.kline_path("BTCUSDT", "4h"))
    chk(_under(kp, _R_TC11_SNAP), "D.kline_path('BTCUSDT','4h')", rel_of(kp))
    fp = _real(D.funding_path("BTCUSDT"))
    chk(_under(fp, _R_TC11_SNAP), "D.funding_path('BTCUSDT')", rel_of(fp))
    chk(dict(D.STEP_MS) == LENS_MS and dict(BK.LENS_MS) == LENS_MS,
        "D.STEP_MS == BK.LENS_MS == E.LENS_MS (15m in place)",
        f"{sorted(D.STEP_MS)} / {sorted(BK.LENS_MS)}")
    chk(TP.ERA_CUT_MS == ERA_CUT_MS and TP.ERA_CUT_ISO == ERA_CUT_ISO, "TP.ERA_CUT_MS",
        f"{TP.ERA_CUT_MS}")
    chk(T5.SEED == SEED_SENS == TP.SEED_LINEAGE and TP.N_BOOT == N_BOOT,
        "sensitivity seed / n_boot", f"T5.SEED {T5.SEED} TP.SEED_LINEAGE {TP.SEED_LINEAGE} "
        f"TP.N_BOOT {TP.N_BOOT}")
    rows = tc10_bindings()
    und = [r for r in rows if r["declared"] is None]
    chk(not und, "no undeclared TC10 binding in the estate's module globals",
        f"{len(rows)} TC10 binding(s), {len(und)} undeclared"
        + (": " + "; ".join(f"{r['name']}={r['value']}" for r in und[:6]) if und else ""))
    man_panels = D.panel()
    chk(list(man_panels["PANEL17"]) == list(PANEL17)
        and list(man_panels["UNSEEN"]) == list(UNSEEN12)
        and tuple(man_panels["CLASSIC5"]) == CLASSIC5,
        "panels == TC11 Stage D manifest (D.panel())",
        f"CLASSIC5 {len(CLASSIC5)} · UNSEEN12 {len(UNSEEN12)} · PANEL17 {len(PANEL17)}")
    chk(UNSEEN12 == _UNSEEN12_TC10 and PANEL17 == _PANEL17_TC10,
        "the TC11 stems equal TC10's (copies taken at import stay valid)",
        f"UNSEEN12 same={UNSEEN12 == _UNSEEN12_TC10} PANEL17 same={PANEL17 == _PANEL17_TC10}")
    fz = fees()
    tk = sorted({f["taker_bps_side"] for f in fz.values()})
    chk(tk == [float(R2.FEE_BPS_SIDE)] and set(fz) == set(PANEL17),
        "fee_schedule taker == tierc2_rules.FEE_BPS_SIDE, one row per PANEL17 stem",
        f"taker {tk} vs {R2.FEE_BPS_SIDE}; {len(fz)} stems")
    rng = sorted(n for n in sys.modules if _forbidden(n))
    chk(not rng, "RANGE-FREE: no range module in the process",
        f"{len(rng)} {rng[:4]}")
    if bad:
        raise SystemExit("HALT: POST-SHIM [L-0.3] — " + " | ".join(bad))


_FEES: dict = {}


def fees() -> dict:
    """{stem: tolls} from research_outputs/tierc11/data/fee_schedule.json (the
    TC11 record): taker 5.0 bps/side (10.0 round trip) = the toll of record
    [L-1.1]; maker 2.0 bps/side, an ASSUMPTION [L-1.2]; the charter slippage
    tier per stem (A 2 · B 5 · C 10 bps/side), the haircut twin.  A copy."""
    if not _FEES:
        raw = json.loads((OUT / "data" / "fee_schedule.json").read_text(encoding="utf-8"))
        for a in raw["assets"]:
            _FEES[a["stem"]] = {
                "asset": a["asset"], "venue": a["venue"],
                "taker_bps_side": float(a["taker_bps_side_used"]),
                "taker_round_trip_bps": float(a["round_trip_bps_used"]),
                "maker_bps_side": float(a["maker_bps_per_side"]),
                "maker_round_trip_bps": float(a["maker_round_trip_bps"]),
                "maker_kind": a["maker_kind"],
                "maker_slippage_bps_side": float(a["maker_slippage_bps_side"]),
                "slippage_bps_side": float(a["charter_slippage_bps_per_side"]),
                "slippage_tier": a["charter_slippage_tier"],
            }
    return copy.deepcopy(_FEES)


def era_of(close_ms):
    """L-1.3: era = the entry (or event-anchor) bar's CLOSE.  'tuning' iff
    close <= 2024-06-30T23:59:59Z, else 'holdout'.  Scalar or array-like."""
    if isinstance(close_ms, (int,)) or (hasattr(close_ms, "__int__")
                                        and not hasattr(close_ms, "__len__")):
        return "tuning" if int(close_ms) <= ERA_CUT_MS else "holdout"
    import numpy as np
    a = np.asarray(close_ms, dtype=np.int64)
    return np.where(a <= ERA_CUT_MS, "tuning", "holdout")


_post_shim()


# ═══════════════════════════════════════ 7 · THE AUDIT HOOK — INSTALLED LAST
_AUDIT: list[dict] = []
_OPENED: dict[str, str] = {}


def _block(event: str, real: str, w: bool, cls: str, why: str) -> None:
    _AUDIT.append({"event": event, "path": rel_of(real), "write": bool(w),
                   "class": f"BLOCKED:{cls}"})
    raise AuditHalt(f"TC11-AUDIT[{cls}]: {event} {_show_path(real)} — {why} [L-0.3]")


def _enforce_hook(event, args):
    if event not in _PATH_EVENTS:
        return
    judged = [(r, w, "") for r, w in _event_paths(event, args)]
    raw = _relative_open(args) if event == "open" else None
    dir_fds = _open_dir_fds() if raw is not None else []
    if dir_fds:
        judged += [(r, w, " (a relative path, resolved against an open directory fd)")
                   for r, w in _alt_open_paths(args, raw, dir_fds)]
    for real, w, via in judged:
        cls = classify(real)
        if event == "open" and not via:
            _OPENED.setdefault(real, cls)
        if cls in ("tc10-snapshot", "live-cache"):
            _block(event, real, w, cls,
                   "the TC10 snapshot and the live cache are READ-NEVER for TC11" + via)
        if w:
            pw = _protected_write(real)
            if pw:
                _block(event, real, True, pw, "WRITE-NEVER for TC11" + via)
        if cls == "tc10-unlisted":
            cand = _C_CANDIDATE.get(_canon(real))
            _block(event, real, w, cls,
                   f"not one of the {len(TC10_ALLOW)} TC10 records L-0.3 allows"
                   + (" (an AMENDMENT CANDIDATE, not ruled in)" if cand else "") + via)
        # the dir-guard judges only an UNAMBIGUOUS anchor (an absolute path, or a
        # relative one while no directory fd is open): a relative directory open
        # made through a dir fd (shutil.rmtree's walk) is judged by the candidates
        # above, and so is every dir_fd-relative open made through the new fd
        if (event == "open" and not via and not (raw is not None and dir_fds)
                and os.path.isdir(real) and _dir_guarded(real)):
            _block(event, real, w, "dir-guard",
                   "a directory open of a protected root or its ancestor: a dir_fd-relative "
                   "open through it could not be judged" + via)
        if cls == "tc10-allow" and not via:
            _AUDIT.append({"event": event, "path": rel_of(real), "write": bool(w),
                           "class": "ALLOW"})


def exit_report_lines() -> list[str]:
    """The audit log as the exit report prints it (empty when nothing was logged)."""
    if not _AUDIT:
        return []
    n_allow = sum(1 for r in _AUDIT if r["class"] == "ALLOW")
    blocked = [r for r in _AUDIT if r["class"].startswith("BLOCKED:")]
    kinds = sorted({r["class"].split(":", 1)[1] for r in blocked})
    out = [f"TC11-AUDIT exit report: ALLOW {n_allow} · BLOCKED {len(blocked)}"
           + (f" {kinds}" if kinds else "")]
    out += [f"  ALLOW {p}" for p in sorted({r["path"] for r in _AUDIT if r["class"] == "ALLOW"})]
    out += [f"  BLOCKED[{r['class'].split(':', 1)[1]}] {r['event']} {r['path']}"
            for r in blocked]
    if blocked:
        out.append(f"TC11-AUDIT: {len(blocked)} BLOCKED attempt(s) in this process — exit "
                   f"forced to {AUDIT_EXIT_CODE} [L-0.3]")
    return out


def _exit_report() -> None:
    """atexit [verifier MINOR-7]: print the ALLOW / BLOCKED log on stderr; a
    process that saw ANY BLOCKED attempt — caught by an `except BaseException`,
    or raised in a thread whose traceback is merely printed — exits
    AUDIT_EXIT_CODE, never 0."""
    lines = exit_report_lines()
    if not lines:
        return
    try:
        sys.stderr.write("\n".join(lines) + "\n")
        sys.stderr.flush()
    except Exception:                       # noqa: BLE001 — a closed stream reports nothing
        pass
    if any(r["class"].startswith("BLOCKED:") for r in _AUDIT):
        try:
            sys.stdout.flush()
        except Exception:                   # noqa: BLE001
            pass
        os._exit(AUDIT_EXIT_CODE)


sys.addaudithook(_enforce_hook)
atexit.register(_exit_report)


# ═══════════════════════════════════════════════════════════ 8 · THE API
def audit_log() -> list[dict]:
    """Every read of an allow-listed TC10 record since the hook was armed
    (class ALLOW) and every refused attempt (class BLOCKED:<detector>)."""
    return [dict(r) for r in _AUDIT]


def opened_paths() -> dict[str, str]:
    """{real path: class} of every 'open' since the hook was armed."""
    return dict(_OPENED)


def import_audit() -> list[dict]:
    return copy.deepcopy(IMPORT_AUDIT)


def tc10_record(rel: str) -> Path:
    """The ABSOLUTE MAIN-TREE path of an allow-listed TC10 record [L-0.3]."""
    if rel not in TC10_ALLOW:
        raise SystemExit(f"HALT: {rel} is not on the TC10 record allow-list"
                         + (" (an AMENDMENT CANDIDATE, not ruled in)"
                            if rel in TC10_AMENDMENT_CANDIDATES else ""))
    return MAIN_TREE / rel


def static_imports(src: str) -> list[str]:
    """Every module name this source can import: Import / ImportFrom nodes
    ANYWHERE (function bodies included — a lazy import is invisible to a
    closure), plus a constant first argument of importlib.import_module /
    __import__ / tc10_import / _tc10_import."""
    names = []
    for n in ast.walk(ast.parse(src)):
        if isinstance(n, ast.Import):
            names += [a.name for a in n.names]
        elif isinstance(n, ast.ImportFrom) and n.module:
            names.append(n.module)
            names += [f"{n.module}.{a.name}" for a in n.names]
        elif isinstance(n, ast.Call) and n.args and isinstance(n.args[0], ast.Constant) \
                and isinstance(n.args[0].value, str):
            f = n.func
            fn = f.attr if isinstance(f, ast.Attribute) else getattr(f, "id", "")
            if fn in ("import_module", "__import__", "tc10_import", "_tc10_import"):
                names.append(n.args[0].value)
    return names


# The I/O the audit hook cannot see (the LIMIT in the module docstring): the AST
# scan that bans it in a module's source.
_ESC_MODULES = ("subprocess", "ctypes", "cffi", "pyarrow.dataset", "pyarrow.fs")
_ESC_PA_CALLS = frozenset({"read_table", "ParquetFile", "write_table", "write_to_dataset",
                           "memory_map", "OSFile", "open_input_file", "open_input_stream",
                           "open_output_stream", "open_append_stream", "LocalFileSystem"})
_ESC_OS_CALLS = frozenset({"system", "popen", "fork", "forkpty", "posix_spawn",
                           "posix_spawnp"})
_ESC_KWARGS = frozenset({"filesystem", "dir_fd", "src_dir_fd", "dst_dir_fd",
                         "partition_cols"})


def hook_escapes(src: str) -> list[str]:
    """Every use in `src` of I/O the audit hook cannot see: an import of
    subprocess / ctypes / cffi / pyarrow.dataset / pyarrow.fs; a call to
    pyarrow's native readers or writers (read_table, ParquetFile, write_table,
    write_to_dataset, memory_map, OSFile, LocalFileSystem, open_*_stream/file);
    os.system / popen / fork / posix_spawn / exec* / spawn*; a filesystem=,
    dir_fd=, src_dir_fd=, dst_dir_fd= or partition_cols= keyword.  Function
    bodies included.  Each finding starts 'HOOK-ESCAPE line N:'."""
    out = []

    def esc_mod(m: str) -> bool:
        return any(m == e or m.startswith(e + ".") for e in _ESC_MODULES)

    for n in ast.walk(ast.parse(src)):
        if isinstance(n, ast.Import):
            out += [f"HOOK-ESCAPE line {n.lineno}: import {a.name}" for a in n.names
                    if esc_mod(a.name)]
        elif isinstance(n, ast.ImportFrom) and n.module:
            names = [a.name for a in n.names]
            if esc_mod(n.module):
                out.append(f"HOOK-ESCAPE line {n.lineno}: from {n.module} import {names}")
            elif n.module == "pyarrow" and {"dataset", "fs"} & set(names):
                out.append(f"HOOK-ESCAPE line {n.lineno}: from pyarrow import {names}")
            elif n.module.startswith("pyarrow") and _ESC_PA_CALLS & set(names):
                out.append(f"HOOK-ESCAPE line {n.lineno}: from {n.module} import {names}")
            elif n.module == "os" and (_ESC_OS_CALLS & set(names) or any(
                    x.startswith(("exec", "spawn")) for x in names)):
                out.append(f"HOOK-ESCAPE line {n.lineno}: from os import {names}")
        elif isinstance(n, ast.Call):
            f = n.func
            name = f.attr if isinstance(f, ast.Attribute) else getattr(f, "id", "")
            base = f.value.id if (isinstance(f, ast.Attribute)
                                  and isinstance(f.value, ast.Name)) else None
            if name in _ESC_PA_CALLS:
                out.append(f"HOOK-ESCAPE line {n.lineno}: {name}(…) — pyarrow native I/O")
            if base == "os" and (name in _ESC_OS_CALLS
                                 or name.startswith(("exec", "spawn"))):
                out.append(f"HOOK-ESCAPE line {n.lineno}: os.{name}(…) — out of process")
            out += [f"HOOK-ESCAPE line {n.lineno}: {name}(…, {kw.arg}=…)"
                    for kw in n.keywords if kw.arg in _ESC_KWARGS]
    return out


_REGISTRY_TARGETS = ("BK.REGISTRY_PIN_PATH", "BK.REGISTRATION_TEXTS_PATH",
                     "LN.REGISTRY_PIN_PATH", "LN.REGISTRATION_TEXTS_PATH")


def _lean_block_text() -> str:
    """The shim's executor readings, printed: every re-root, every binding
    deliberately left, the import audit (data opens per window), the post-shim
    assertion, the handoff to tierc11_nest and the hook's allow-list.
    Deterministic: no clock, no temp path."""
    L = [f"{LEAN_TAG} L-0.3 TC11 RANGE-FREE SHIM · substrate {SNAPSHOT.name} · pin {PIN_ISO} "
         f"({PIN_MS}) · seed {SEED} (sensitivity {SEED_SENS}) · n_boot {N_BOOT}"]
    L.append(f"{LEAN_TAG} L-0.3 IMPORTS — tierc2_baseline FIRST under the TC11 env; every "
             f"other module inside a TC10 env window restored in finally "
             f"({len(IMPORT_AUDIT)} windows):")
    for w in IMPORT_AUDIT:
        L.append(f"  window {w['label']:<18} env {w['env']:<14} "
                 f"tc10-snapshot/live touches {len(w['tc10_snapshot_or_live_touches'])} · "
                 f"protected writes {len(w['protected_writes'])} · "
                 f"undeclared tc10 reads {len(w['tc10_unlisted_reads'])}")
        for c, p in w["data_opens"]:
            L.append(f"      data open  [{c}] {p}")
        for p in w["source_reads_not_imports"]:
            L.append(f"      source read (AST, never imported) {p}")
    L.append(f"{LEAN_TAG} L-0.3 RE-ROOTS ({len(REROOTS)}; each verified to exist before "
             f"assignment):")
    for r in REROOTS:
        L.append(f"  RE-ROOT {r['name']}")
        L.append(f"      {r['old']}")
        L.append(f"   -> {r['new']}   [{r['why']}]")
    L.append(f"{LEAN_TAG} L-0.3 RE-ROOTED TARGETS THAT DO NOT EXIST — they FAIL CLOSED:")
    for nm in _REGISTRY_TARGETS:
        a, t = nm.split(".")
        p = Path(getattr(_MODS[a], t))
        L.append(f"  {nm} = {rel_of(_real(p))} · exists {p.exists()}")
    L.append("      TC11's registry pin is research_outputs/tierc11/registrations/"
             "REGISTRY_PIN.json (another format), read only by tierc11_score [L-1.4]; a BK/LN "
             "door that reads these paths raises FileNotFoundError — it can never fall back "
             "on a TC10 record.")
    L.append(f"{LEAN_TAG} L-0.3 LEFT AS IS (declared; not re-rooted):")
    rows = tc10_bindings()
    for r in rows:
        L.append(f"  {r['name']} = {r['value']}  [{r['kind']}] — {r['declared']}")
    L.append(f"{LEAN_TAG} L-0.3 DEFAULTS BOUND AT DEF TIME ARE NOT RE-ROOTED: every TC11 "
             f"call passes seed={SEED}, n_boot={N_BOOT}; no family_m default; no TP "
             f"registry door [L-1.4].")
    L.append(f"{LEAN_TAG} L-0.3 POST-SHIM ASSERTION ({len(POST_SHIM)} clauses):")
    L += [f"  {x}" for x in POST_SHIM]
    L.append(f"{LEAN_TAG} L-0.3 HANDOFF TO {NEST_MODULE} — two post-shim clauses of L-0.3 are "
             f"about the census module, which this range-free shim never imports. "
             f"{NEST_MODULE} MUST assert both right after its C.* / stamps.* re-roots, and "
             f"its fixture MUST plant a skipped C.STAGE_D re-root that turns (1) RED:")
    L.append(f"  (1) C.as_of_close_ms(s)[0] == {PIN_MS} for every s in PANEL17 — at census "
             f"import C.STAGE_D names research_outputs/tierc10/data, whose AS_OF_PIN.json is "
             f"NOT on the allow-list: with the hook armed a skipped re-root HALTs "
             f"[tc10-unlisted] instead of returning TC10's pin {TC10_PIN_MS};")
    L.append("  (2) C.RETEST_PINS == {margin_atr 1.0, hold_bars 3, ttl_bars 400, "
             "grid_sha 2135ca66…} (resolved at census import from the allow-listed "
             "census/TUNING_RESULT.json).")
    L.append(f"  The range door tc10_import(name, allow_range=True) opens ONLY for a caller "
             f"that is {NEST_MODULE}; any other caller HALTs.")
    L.append(f"{LEAN_TAG} L-0.3 AUDIT HOOK armed LAST. Paths judged CANONICALLY (realpath; the "
             f"deepest existing ancestor matched by device+inode against the protected roots; "
             f"NFC + casefold; the /System/Volumes/Data firmlink, /.nofollow and /.resolve/N "
             f"prefixes stripped). AuditHalt on:")
    L.append("  · any open / listing / mutation under the TC10 snapshot or the live cache;")
    L.append("  · any write under research_outputs/tierc10[_run2]/, scripts/tierc10_*, "
             "exchange/status/LEDGER*, LEDGER.md, .gitignore (this tree and the main tree);")
    L.append(f"  · any open / listing under research_outputs/tierc10 that is not one of the "
             f"{len(TC10_ALLOW)} records below;")
    L.append("  · a relative open judged against the cwd AND every open directory fd (the "
             "event carries no dir_fd); a directory open of a protected root, of an ancestor "
             "of one, or inside write-protected space, when its anchor is unambiguous;")
    L.append(f"  · at exit: ALLOW/BLOCKED printed on stderr; any BLOCKED attempt forces exit "
             f"{AUDIT_EXIT_CODE}.")
    L.append(f"  TC10 record allow-list ({len(TC10_ALLOW)} — the six L-0.3 names + two by AM-1; read "
             f"by absolute main-tree path, logged ALLOW):")
    for k in sorted(TC10_ALLOW):
        L.append(f"  ALLOW {k} · exists {(MAIN_TREE / k).exists()} — {TC10_ALLOW[k]}")
    L.append(f"  AMENDMENT CANDIDATES ({len(TC10_AMENDMENT_CANDIDATES)}; NOT allowed — "
             f"refused until ruled in):")
    for k in sorted(TC10_AMENDMENT_CANDIDATES):
        L.append(f"  REFUSED {k} — {TC10_AMENDMENT_CANDIDATES[k]}")
    L.append(f"  Declared import-window reads (before arming; any other TC10 read in a window "
             f"HALTs):")
    for k in sorted(IMPORT_TC10_READS):
        L.append(f"  IMPORT-READ {k} by window {IMPORT_TC10_READS[k][0]} — "
                 f"{IMPORT_TC10_READS[k][1]}")
    L.append(f"{LEAN_TAG} L-0.3 LIMIT OF THE HOOK (AMENDMENT CANDIDATE text): Python-level "
             f"opens only. Unseen: pyarrow native readers/writers (pq.read_table, "
             f"pq.ParquetFile, pq.write_table, pa.memory_map, pyarrow.dataset, pyarrow.fs); "
             f"pd.read_parquet(filesystem=…) and to_parquet(partition_cols=…); out-of-process "
             f"I/O (subprocess, os.system, ctypes). hook_escapes(src) is the AST ban.")
    L.append(f"{LEAN_TAG} L-1.3 ERA = the entry/anchor bar's CLOSE: tuning <= {ERA_CUT_ISO} "
             f"({ERA_CUT_MS}), holdout after; TP.in_era / BK.require_era (bar OPEN) are "
             f"not used for TC11 era gating.")
    fz = fees()
    L.append(f"{LEAN_TAG} L-1.1/L-1.2 TOLLS (research_outputs/tierc11/data/fee_schedule.json): "
             f"taker {sorted({f['taker_bps_side'] for f in fz.values()})} bps/side of record; "
             f"maker {sorted({f['maker_bps_side'] for f in fz.values()})} bps/side ASSUMPTION; "
             f"slippage twin by tier "
             + ", ".join(f"{t} {b}" for t, b in sorted({(f['slippage_tier'],
                                                           f['slippage_bps_side'])
                                                          for f in fz.values()})))
    return "\n".join(L) + "\n"


_LEAN = _lean_block_text()      # taken ONCE, at arming: later process history cannot move it


def lean_block() -> str:
    """The lean block as it stood when the shim finished importing."""
    return _LEAN


__all__ = ["TP", "T9", "T8", "T7", "T6", "T5", "TB", "D", "BK", "LN", "R2", "R3", "LAB",
           "PIN_MS", "SEED", "SEED_SENS", "N_BOOT", "CLASSIC5", "UNSEEN12", "PANEL17",
           "ERA_CUT_MS", "era_of", "LENS_MS", "fees", "OUT", "audit_log", "opened_paths",
           "import_audit", "lean_block", "tc10_import", "tc10_record", "classify",
           "REROOTS", "NOT_REROOTED", "TC10_ALLOW", "TC10_AMENDMENT_CANDIDATES",
           "IMPORT_TC10_READS", "AUDIT_EXIT_CODE", "SNAPSHOT", "TC10_SNAPSHOT",
           "LIVE_CACHE", "MAIN_TREE", "ROOT", "AuditHalt", "static_imports", "hook_escapes",
           "exit_report_lines", "NEST_MODULE", "tc10_bindings",
           "FORBIDDEN_MODULE_SUBSTRINGS"]


if __name__ == "__main__":
    sys.stdout.write(lean_block())
