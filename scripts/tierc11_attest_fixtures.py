#!/usr/bin/env python
"""TIER-C11 · TC11-FIX — F-ATTEST · F-DET · F-GUARD.  The fixtures of
scripts/tierc11_worktree_attest.py, the L-F.3 worktree attestation [final review 2026-09-25: fidelity
MINOR-2, reproducibility MINOR-5; TC11-FIX verify MAJOR-2, MINOR-6, MINOR-10].

L-F.3: the attestation "FAILS on a mismatch or any modification".  Before the hardening it compared
HEAD and `git status --porcelain` only — porcelain cannot see the staged parquet (gitignored), the
per-file shas recorded at open were never re-checked, and the staged files were never held to the
reviewed commit's own record.  This suite proves every RED the hardened attestation claims, on real
worktrees at the reviewed commit, and that an untouched open/close is GREEN (exit 0).

THE RECORD A CYCLE IS HELD TO.  The attestation reads the reviewed commit's record with ONE call,
`git show <commit>:research_outputs/tierc11/PROGRESS.json`.  Two sources feed that call here:
  REAL  the commit's own PROGRESS.json, unchanged (the reviewer's path).  The three record plants
        run on it, each judged on the findings BEYOND an untouched REAL cycle's own (the drift
        between the staged files and HEAD's record, if the record has not caught up with a
        re-file: printed on STDOUT ONLY, never in the transcript).
  VIEW  HEAD's own PROGRESS.json with every staged-class entry removed from every stage's
        artifact_shas and ONE final stage, FIXTURE-VIEW, recording THIS file's own scan of the
        stage source's staged files.  It is substituted for that one `git show` read by THIS file,
        in THIS file's processes only (an in-process swap of the module's git helper; for the CLI,
        a child process that runs the attestation script as __main__ with only that one read
        answered from the view) — the attestation module has no such seam.  Every other plant, the
        REAL leg and F-DET run on the VIEW, so the untouched attestation MUST be GREEN whether or
        not HEAD's record has caught up with the main tree, and the transcript is the same before
        and after the commit that re-records the staged files [verify MINOR-10].

  F-ATTEST  REAL: `--open` then `--close` through the attestation script's own __main__ (a child
            process; the VIEW of the main tree's staged files), staging from the main tree as a
            reviewer does: exit 0 at open with the worktree printed; between open and close the
            worktree holds EXACTLY the two TC10 records, read-only, byte-equal to the main tree's;
            at close exit 0 and verdict GREEN with NO finding; HEAD before/after == HEAD, porcelain
            empty before/after; the per-file map == THIS file's own recursive scan of the main
            tree's staged files, its count and set sha printed; the TC10 map == THIS file's own
            hash of the main tree's two records; the record provenance == the view's own sha and
            staged-class count; A.scan_staged == THIS file's own recursive scan (main tree and
            frozen stage) [MINOR-6]; an untouched in-process cycle on the frozen stage and its view
            is GREEN; the worktree gone, the open record gone, no tc11-review-fixture-* worktree
            left, the main tree's HEAD and branch unmoved; the removed one-shot `-- <cmd>` mode
            HALTs without creating a worktree.
            SABOTAGE (each on a real worktree at HEAD, staged from a FROZEN scratch copy of the
            main tree's staged files and two TC10 records): a tracked-file edit inside the
            worktree; a byte change to a staged parquet; a staged parquet that differs from HEAD's
            REAL record; HEAD moved inside the worktree (update-ref --no-deref to the commit's
            parent — the scratch worktree's own HEAD, no branch); an untracked file written; a
            staged parquet deleted; a new parquet written TWO levels down (regbooks/P-BRK-4H/)
            [MINOR-6]; a staged parquet HEAD's REAL record lacks (also two levels down); a parquet
            HEAD's REAL record holds, not staged; a legacy (pre-hardening) open record with a staged
            byte changed; the stage source's TC10 STAGE_D_MANIFEST.json bent by one byte; the
            worktree's staged TC10 TUNING_RESULT.json bent after open [MAJOR-2]; an open record
            filed before the TC10 staging with no TC10 record in the worktree; and the CLI's exit
            code on a RED (a tracked edit through __main__).  Each must turn the attestation RED by
            its own named finding.
  F-DET     FAILS IF two subprocess emissions of ATTEST_PROBE.txt (the commit-independent
            projection of the attestation record of an untouched open/close on the frozen stage and
            its view; PYTHONHASHSEED 1, 20260924) differ from each other or from this run's bytes,
            or either exits nonzero.  SABOTAGE: a one-byte-bent copy; a hash-order-dependent
            emission.
  F-GUARD   THIS FILE'S OWN GUARD.  The attestation now reads TC10's STAGE_D_MANIFEST.json, which
            tierc11_env's hook refuses once armed (an AMENDMENT CANDIDATE, not on TC10_ALLOW), so
            this file does NOT import tierc11_env: it types its own substrate guard and installs
            its own audit hook, which refuses any write under the main tree's
            research_outputs/tierc10[_run2], scripts/tierc10_*, exchange/, LEDGER.md, .gitignore,
            research_outputs/tierc11/PROGRESS.json, research_outputs/tierc11/review/, the TC10 and
            TC11 snapshots and the live cache, and any read under research_outputs/tierc10, the
            TC10 snapshot or the live cache other than the two staged TC10 records.  FAILS IF a
            subprocess probe's planted write under research_outputs/tierc10, removal there, write
            under review/attest or read of an unlisted TC10 path is not refused by the guard (every
            plant aims at a directory that does not exist, so nothing can be written even if the
            guard is broken); the two staged TC10 records cannot be read through it; or the guard
            refused anything during this run.

TWO LEGS PER FIXTURE, the BREAK leg first, and it must go RED or the fixture is VOID [the prove()
law of scripts/tierc10_rf_fixtures.py / tierc11_ride_fixtures.py].  A plant counts as CAUGHT only if
a finding NAMES THE INTENDED DETECTOR (its expected substring, the planted file's path included
where there is one); a crash is a FIXTURE DEFECT.  HYGIENE: every worktree is a scratch one named
tc11-review-fixture-<tag> under .claude/worktrees/, removed in `finally` whatever happens; the
attestation records go to RUN_ROOT/_det_attest/att/<tag>/, never to review/attest/; the frozen
stage copy (RUN_ROOT/_det_attest/stage_root) is removed at exit; no artifact of record, no ref and
no other worktree is touched.  The fixture's own reads (the staged scan, the TC10 hashes, the
PROGRESS record, the view, the drift) are THIS file's code — a second object.  FROZEN SUBSTRATE:
HALTs unless NAIAD_CACHE_DIR is the TC11 snapshot (this file's typed guard).  Seed 20260924.  The
transcript carries no clock, no temp path, no commit sha (HEAD prints as HEAD) and nothing that
depends on how far HEAD's PROGRESS record has caught up with the main tree.

Run:  export NAIAD_CACHE_DIR=$HOME/.cache/naiad/snapshots/tc11_20260925 PYTHONDONTWRITEBYTECODE=1
      ~/venvs/naiad/bin/python -B scripts/tierc11_attest_fixtures.py \\
          [leg-substring ...] [--refile-transcript] [--root=DIR]
Exit 0 = every leg GREEN, every break RED · 1 = a RED or VOID fixture, a transcript finding, a
worktree left behind, or a HALT.
"""
from __future__ import annotations

import contextlib
import hashlib
import json
import os
import re
import runpy
import shutil
import subprocess
import sys
import time
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# ── FIXTURE-TYPED LITERALS: the commission, a second object, never A's own ──
PIN = 1_790_294_400_000                  # 2026-09-25T00:00:00Z [L-0.1]
SEED = 20260924
DET_SEEDS = (1, SEED)
AS_OF_LINE = "as_of_last_closed_4h: 2026-09-25T00:00:00Z"
HOME = Path.home()
SNAP = HOME / ".cache" / "naiad" / "snapshots" / "tc11_20260925"
TC10_SNAP = HOME / ".cache" / "naiad" / "snapshots" / "tc10_20260921"
LIVE = HOME / ".cache" / "naiad" / "data_cache"
PROGRESS_REL = "research_outputs/tierc11/PROGRESS.json"
STAGED_DIR = "research_outputs/tierc11"
TC10_RECORDS_T = ("research_outputs/tierc10/census/TUNING_RESULT.json",
                  "research_outputs/tierc10/data/STAGE_D_MANIFEST.json")
TC10_MODE_T = 0o444
WT_BASE = ROOT / ".claude" / "worktrees"
WT_PREFIX = "tc11-review-fixture-"
ATTEST_SCRIPT = ROOT / "scripts" / "tierc11_worktree_attest.py"
TRACKED_PLANT = "research_outputs/tierc11/LEANS.md"
DEEP_DIR = "research_outputs/tierc11/regbooks/P-BRK-4H"      # two levels under tierc11 [MINOR-6]
RECORD_KINDS = ("STAGED != RECORD: ", "STAGED NOT IN RECORD: ", "RECORDED NOT STAGED: ")
VIEW_STAGE = "FIXTURE-VIEW"
HASHORDER_T = ("BTCUSDT", "ETHUSDT", "SOLUSDT", "NEARUSDT", "ZECUSDT", "PUMPUSDT", "HYPEUSDT",
               "SUIUSDT", "MNTUSDT", "XRPUSDT", "DOGEUSDT", "LINKUSDT")
OUT = ROOT / "research_outputs" / "tierc11" / "closure"
RUN_ROOT = OUT
TRANSCRIPT = "FIXTURES_ATTEST.txt"
ARTIFACT = "ATTEST_PROBE.txt"
PY = sys.executable
LINES: list[str] = []
PASSED: list[str] = []
FAILED: list[str] = []
_C: dict = {}
_TMP_RX = re.compile(r"(/private)?/(var/folders|tmp)/[^\s'\"]+")


# ═════════════════════════════════════════════════════════ THIS FILE'S GUARDS (before A)
def guard_substrate(env: str | None) -> Path:
    """HALTs unless NAIAD_CACHE_DIR is the TC11 snapshot (never the live cache, never the TC10
    snapshot) and holds klines/ — typed here (this file does not import tierc11_env)."""
    if not env:
        raise SystemExit(f"HALT: NAIAD_CACHE_DIR is unset — TC11 reads ONLY {SNAP}")
    got = Path(os.path.normpath(os.path.expanduser(env))).resolve()
    for bad, why in ((LIVE, "the LIVE cache"), (TC10_SNAP, "the TC10 snapshot")):
        if got == bad.resolve() or bad.resolve() in got.parents:
            raise SystemExit(f"HALT: NAIAD_CACHE_DIR={got} names {why}")
    if got != SNAP.resolve() or not (got / "klines").is_dir():
        raise SystemExit(f"HALT: NAIAD_CACHE_DIR={got} is not the TC11 snapshot {SNAP} with klines/")
    return got


guard_substrate(os.environ.get("NAIAD_CACHE_DIR"))


class GuardHalt(SystemExit):
    """Raised by THIS file's audit hook (a SystemExit: `except Exception` cannot swallow it)."""


def _canon(p) -> str:
    s = os.path.realpath(os.path.abspath(os.fsdecode(os.fspath(p))))
    s = unicodedata.normalize("NFC", s).casefold()
    for pre in ("/system/volumes/data", "/.nofollow"):
        if s.startswith(pre + "/"):
            s = s[len(pre):]
    return s


def _under(c: str, root: str) -> bool:
    return c == root or c.startswith(root.rstrip("/") + "/")


_G_NO_WRITE = tuple(_canon(p) for p in (
    ROOT / "research_outputs" / "tierc10", ROOT / "research_outputs" / "tierc10_run2",
    ROOT / "exchange", ROOT / "LEDGER.md", ROOT / ".gitignore", ROOT / PROGRESS_REL,
    ROOT / "research_outputs" / "tierc11" / "review", SNAP, TC10_SNAP, LIVE))
_G_NO_WRITE_PREFIX = (_canon(ROOT / "scripts") + "/tierc10_",)
_G_NO_READ = tuple(_canon(p) for p in (ROOT / "research_outputs" / "tierc10", TC10_SNAP, LIVE))
_G_READ_OK = frozenset(_canon(ROOT / r) for r in TC10_RECORDS_T)
_G_LOG: list[str] = []
_WFLAGS = (os.O_WRONLY | os.O_RDWR | os.O_APPEND | os.O_CREAT | os.O_TRUNC
           | getattr(os, "O_EXCL", 0))
_G_MUT1 = frozenset({"os.remove", "os.rmdir", "os.mkdir", "os.chmod", "os.chown", "os.truncate",
                     "os.utime", "os.chflags", "os.lchflags", "shutil.rmtree", "os.removexattr",
                     "os.setxattr"})
_G_MUT2 = frozenset({"os.rename", "shutil.move"})          # both ends
_G_DST = frozenset({"os.symlink", "os.link", "shutil.copyfile", "shutil.copytree"})
_G_LIST = frozenset({"os.listdir", "os.scandir"})


def _refuse(kind: str, path) -> None:
    shown = os.fsdecode(os.fspath(path))
    for base, tok in ((str(ROOT), "<repo>"), (str(HOME), "~")):
        if shown.startswith(base + "/"):
            shown = tok + shown[len(base):]
            break
    msg = f"HALT: GUARD {kind} refused: {shown}"
    _G_LOG.append(msg)
    raise GuardHalt(msg)


def _judge_write(p) -> None:
    if p is None or isinstance(p, int):
        return
    c = _canon(p)
    if any(_under(c, r) for r in _G_NO_WRITE) or any(c.startswith(x) for x in _G_NO_WRITE_PREFIX):
        _refuse("write", p)


def _judge_read(p) -> None:
    if p is None or isinstance(p, int):
        return
    c = _canon(p)
    if c not in _G_READ_OK and any(_under(c, r) for r in _G_NO_READ):
        _refuse("read", p)


def _guard_hook(event, args):
    try:
        if event == "open":
            path, mode, flags = (list(args) + [None, None, None])[:3]
            w = (isinstance(mode, str) and any(ch in mode for ch in "wax+")) or \
                (isinstance(flags, int) and bool(flags & _WFLAGS))
            (_judge_write if w else _judge_read)(path)
        elif event in _G_MUT1 and args:
            _judge_write(args[0])
        elif event in _G_MUT2 and len(args) >= 2:
            _judge_write(args[0])
            _judge_write(args[1])
        elif event in _G_DST and len(args) >= 2:
            _judge_read(args[0])
            _judge_write(args[1])
        elif event in _G_LIST and args:
            _judge_read(args[0])
    except GuardHalt:
        raise
    except (TypeError, ValueError):
        return


sys.addaudithook(_guard_hook)

sys.path.insert(0, str(ROOT / "scripts"))
import tierc11_worktree_attest as A                                  # noqa: E402

if A.WT_BASE != WT_BASE or A.PROGRESS_REL != PROGRESS_REL or A.TC10_STAGED != TC10_RECORDS_T:
    raise SystemExit("HALT: the attestation's worktree base / record path / TC10 staged records "
                     "are not the typed ones")


def say(line: str = "") -> None:            # deterministic -> transcript
    line = _TMP_RX.sub("<tmp>", line)
    for key, label in (("head", "<HEAD>"), ("parent", "<HEAD^>")):
        sha = _C.get(key)
        if sha:                             # the commit prints as HEAD, whole or as a prefix
            line = line.replace(sha, label).replace(sha[:12], label)
    print(line)
    LINES.append(line)


def clock(line: str) -> None:               # wall clock, shas of the moment, drift -> stdout ONLY
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
        except GuardHalt:
            raise                           # the guard is never a plant's finding
        except SystemExit as e:
            found = [str(e) if str(e).startswith("HALT") else f"HALT: {e}"]
        except Exception as e:
            crashed.append(f"{name} -> RAISED {type(e).__name__}: {e}")
            continue
        if not found:
            passed.append(name)
        elif not any(want in str(f) for f in found):
            wrong.append(f"{name} -> {str(found[0])[:200]} (wanted {want!r})")
        else:
            hit = next(str(f) for f in found if want in str(f))
            caught.append(f"{name} [{len(found)} new finding(s)] -> {hit[:230]}")
    if crashed:
        return True, (f"{len(crashed)} plant(s) CRASHED — a FIXTURE DEFECT, not a "
                      f"finding: " + " · ".join(crashed))
    if passed or wrong:
        return True, (f"{len(passed)} plant(s) PASSED {passed}; {len(wrong)} caught by the "
                      f"WRONG detector {wrong}")
    return False, (f"all {len(caught)} plants caught by their named detector, one at a "
                   f"time: " + " · ".join(caught))


# ═════════════════════════════════════════════════════════ THIS FILE'S OWN READS
def git(args: list[str], cwd: Path = ROOT, check: bool = True) -> str:
    return subprocess.run(["git", *args], cwd=cwd, check=check, capture_output=True,
                          text=True).stdout


def sha_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def own_staged(rel: str) -> bool:
    parts = rel.split("/")
    return (rel.startswith(STAGED_DIR + "/") and rel.endswith(".parquet")
            and not any(x.startswith("_det_") for x in parts))


def own_scan(tree: Path) -> dict:
    """{rel: sha256} of every staged-class file under tree/research_outputs/tierc11 (os.walk,
    recursive to any depth, _det_* dirs pruned), in path order."""
    out = {}
    base = tree / STAGED_DIR
    for dp, dns, fns in os.walk(base):
        dns[:] = sorted(d for d in dns if not d.startswith("_det_"))
        for fn in fns:
            p = Path(dp) / fn
            rel = p.relative_to(tree).as_posix()
            if own_staged(rel) and p.is_file():
                out[rel] = sha_file(p)
    return dict(sorted(out.items()))


def own_tc10(tree: Path) -> dict:
    """{rel: sha256} of the two typed TC10 records present under `tree`."""
    return {r: sha_file(tree / r) for r in TC10_RECORDS_T if (tree / r).is_file()}


def progress_text(commit: str) -> str:
    return git(["show", f"{commit}:{PROGRESS_REL}"])


def own_record(commit: str) -> dict:
    """THIS file's read of the commit's REAL PROGRESS record: {staged-class path: sha}."""
    rec = {}
    for st in json.loads(progress_text(commit))["stages"]:
        for p, v in (st.get("artifact_shas") or {}).items():
            rec[p] = v["sha256"] if isinstance(v, dict) else v
    return {p: s for p, s in sorted(rec.items()) if own_staged(p)}


def view_text(commit: str, scan: dict) -> str:
    """THE VIEW: the commit's own PROGRESS.json, every staged-class entry removed from every
    stage's artifact_shas, plus ONE final stage recording `scan` (THIS file's own scan)."""
    doc = json.loads(progress_text(commit))
    for st in doc["stages"]:
        a = st.get("artifact_shas")
        if isinstance(a, dict):
            st["artifact_shas"] = {p: v for p, v in a.items() if not own_staged(p)}
    doc["stages"].append({"stage": VIEW_STAGE, "status": "fixture view (not a record)",
                          "artifact_shas": {p: {"sha256": s} for p, s in sorted(scan.items())}})
    return json.dumps(doc, indent=1, sort_keys=True) + "\n"


def drift(staged: dict, record: dict) -> list[tuple[str, str]]:
    """The (kind, rel) pairs by which a staged map is not the commit's record."""
    out = [("STAGED NOT IN RECORD", r) for r in staged if r not in record]
    out += [("STAGED != RECORD", r) for r in staged if r in record and record[r] != staged[r]]
    out += [("RECORDED NOT STAGED", r) for r in record if r not in staged]
    return sorted(out)


def finding_kind(f: str) -> tuple[str, str] | None:
    for k in RECORD_KINDS:
        if f.startswith(k):
            return (k[:-2], f[len(k):].split(" ")[0])
    return None


def head() -> str:
    if "head" not in _C:
        _C["head"] = git(["rev-parse", "HEAD"]).strip()
    return _C["head"]


def fixture_worktrees() -> list[str]:
    return sorted(ln.split(" ", 1)[1] for ln in git(["worktree", "list", "--porcelain"]).splitlines()
                  if ln.startswith("worktree ") and Path(ln.split(" ", 1)[1]).name.startswith(WT_PREFIX))


def force_remove(wt: Path) -> None:
    if wt.exists():
        git(["worktree", "remove", "--force", str(wt)], check=False)
    if wt.exists():
        raise RuntimeError(f"HYGIENE: {wt} could not be removed")


# ═════════════════════════════════════════════════════════ THE FROZEN STAGE
def frozen() -> tuple[Path, dict]:
    """A scratch COPY of the main tree's staged files AND its two TC10 records, taken once, so that
    every break cycle stages the same bytes whatever a parallel build does to the main tree."""
    if "frozen" in _C:
        return _C["frozen"]
    d = RUN_ROOT / "_det_attest" / "stage_root"
    if d.exists():
        shutil.rmtree(d)
    src, tc = own_scan(ROOT), own_tc10(ROOT)
    for rel in [*src, *tc]:
        (d / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / rel, d / rel)
    got = own_scan(d)
    if got != src or own_tc10(d) != tc or sorted(tc) != sorted(TC10_RECORDS_T):
        raise RuntimeError("the frozen stage copy is not the main tree's bytes (a file moved while "
                           "it was copied, or a TC10 record is absent) — re-run")
    _C["frozen"] = (d, got)
    return _C["frozen"]


def variant(tag: str) -> Path:
    """A symlink tree onto the frozen copies (so a variant costs no bytes), for one plant."""
    d0, fz = frozen()
    v = RUN_ROOT / "_det_attest" / f"variant_{tag}"
    if v.exists():
        shutil.rmtree(v)
    for rel in [*fz, *TC10_RECORDS_T]:
        (v / rel).parent.mkdir(parents=True, exist_ok=True)
        os.symlink(d0 / rel, v / rel)
    return v


def rewrite(p: Path, data: bytes) -> None:
    """Replace a file by a NEW inode (never write through a link or a clone)."""
    p.unlink()
    p.write_bytes(data)


def bent(b: bytes) -> bytes:
    x = bytearray(b)
    x[len(x) // 2] ^= 0x01
    return bytes(x)


def bend(p: Path) -> None:
    rewrite(p, bent(p.read_bytes()))


# ═════════════════════════════════════════════════════════ ONE OPEN / CLOSE CYCLE
def att_dir(tag: str) -> Path:
    return RUN_ROOT / "_det_attest" / "att" / tag


def frozen_view() -> str:
    if "fview" not in _C:
        _C["fview"] = view_text(head(), frozen()[1])
    return _C["fview"]


@contextlib.contextmanager
def record_view(text: str | None):
    """In-process: the attestation's ONE `git show <commit>:PROGRESS.json` read answered from
    `text` (None = the REAL record, nothing swapped); every other git call passes through.
    Counts the reads it answered."""
    if text is None:
        yield
        return
    real = A.git

    def g(args, cwd):
        if len(args) == 2 and args[0] == "show" and args[1].endswith(":" + PROGRESS_REL):
            _C["view_reads"] = _C.get("view_reads", 0) + 1
            return text
        return real(args, cwd)

    A.git = g
    try:
        yield
    finally:
        A.git = real


def cycle(tag: str, mutate=None, stage_root: Path | None = None, legacy: str | None = None,
          view: bool = True) -> dict:
    """In-process A.open_wt -> mutate(worktree) -> A.close_wt, the worktree always removed.
    view=True: the record is the VIEW of the frozen stage; False: HEAD's REAL record.
    legacy: 'hardening' (the pre-hardening open record shape) or 'tc10' (the shape filed before
    the TC10 staging: no staged_tc10 map)."""
    lens = f"fixture-{tag}"
    out = att_dir(tag)
    if out.exists():
        shutil.rmtree(out)
    wt = A.wt_path(lens)
    force_remove(wt)
    try:
        with record_view(frozen_view() if view else None):
            A.open_wt(head(), lens, out=out, stage_root=stage_root or frozen()[0])
            op = out / f"{lens}.open.json"
            r = json.loads(op.read_text())
            if legacy == "hardening":
                r = {k: r[k] for k in ("lens", "commit", "worktree", "before", "staged_artifacts",
                                       "staged_sha256")}
            elif legacy == "tc10":
                r = {k: v for k, v in r.items() if k != "staged_tc10"}
            if legacy:
                op.write_text(json.dumps(r, indent=2) + "\n")
            if mutate:
                mutate(wt)
            rec = A.close_wt(lens, out=out)
    finally:
        force_remove(wt)
    return rec


def baseline(view: bool) -> list[str]:
    """The findings of an UNTOUCHED cycle on the frozen stage: on the VIEW (must be none), or on
    HEAD's REAL record (the drift, if HEAD's record has not caught up: stdout only)."""
    key = "base_view" if view else "base_real"
    if key not in _C:
        _C[key] = cycle("baseline-view" if view else "baseline-real", view=view)
        if not view:
            clock(f"untouched REAL-record cycle on the frozen stage: {len(_C[key]['findings'])} "
                  f"finding(s) (the plants' baseline): {_C[key]['findings']}")
    return _C[key]["findings"]


def new_findings(rec: dict, view: bool = True) -> list[str]:
    if rec["verdict"] != "RED":
        return []
    b = set(baseline(view))
    return [f for f in rec["findings"] if f not in b]


def cli(args: list[str], view: Path | None = None) -> subprocess.CompletedProcess:
    """The attestation script through its own __main__: directly, or (view) in a child of this
    file that answers only the `git show <commit>:PROGRESS.json` read from the view file."""
    env = dict(os.environ, NAIAD_CACHE_DIR=str(SNAP), PYTHONDONTWRITEBYTECODE="1")
    cmd = ([PY, "-B", str(ATTEST_SCRIPT), *args] if view is None else
           [PY, "-B", str(Path(__file__).resolve()), f"--view={view}",
            f"--attest-cli={json.dumps(args)}"])
    return subprocess.run(cmd, capture_output=True, text=True, env=env, cwd=str(ROOT), timeout=900)


def attest_cli_child(view: Path, argv: list[str]) -> None:
    """The CLI child: the attestation script run as __main__ (its own argv parsing and its own
    `sys.exit(main(...))`), with the ONE PROGRESS read answered from the view."""
    text = view.read_text(encoding="utf-8")
    real_run = subprocess.run

    def run(cmd, *a, **k):
        if isinstance(cmd, list) and len(cmd) == 3 and cmd[:2] == ["git", "show"] \
                and str(cmd[2]).endswith(":" + PROGRESS_REL):
            return subprocess.CompletedProcess(cmd, 0, stdout=text, stderr="")
        return real_run(cmd, *a, **k)

    subprocess.run = run
    sys.argv = [str(ATTEST_SCRIPT), *argv]
    runpy.run_path(str(ATTEST_SCRIPT), run_name="__main__")


def cli_cycle(tag: str, mutate=None, view: Path | None = None, inspect=None
              ) -> tuple[dict | None, int, int, str, object]:
    """--open / --close through __main__, staging from the MAIN TREE (the reviewer's path)."""
    lens = f"fixture-{tag}"
    out = att_dir(tag)
    if out.exists():
        shutil.rmtree(out)
    wt = A.wt_path(lens)
    force_remove(wt)
    seen = None
    try:
        o = cli(["--commit", "HEAD", "--lens", lens, "--open", f"--out-dir={out}"], view)
        printed = o.stdout.strip().splitlines()[-1] if o.stdout.strip() else ""
        if o.returncode == 0 and inspect:
            seen = inspect(wt)
        if o.returncode == 0 and mutate:
            mutate(wt)
        c = cli(["--lens", lens, "--close", f"--out-dir={out}"], view)
        p = out / f"{lens}.json"
        rec = json.loads(p.read_text()) if p.exists() else None
    finally:
        force_remove(wt)
    return rec, o.returncode, c.returncode, printed, seen


def main_view() -> Path:
    """The VIEW of the MAIN tree's staged files (the REAL leg's and the CLI plants' record)."""
    if "mview" not in _C:
        p = RUN_ROOT / "_det_attest" / "view_main.json"
        p.parent.mkdir(parents=True, exist_ok=True)
        _C["mscan"] = own_scan(ROOT)
        p.write_text(view_text(head(), _C["mscan"]), encoding="utf-8")
        _C["mview"] = p
    return _C["mview"]


# ═════════════════════════════════════════════════════════ F-ATTEST
def pick_rels(k: int) -> list[str]:
    """The first k frozen staged files that carry NO REAL-record baseline finding (clean
    attribution for the plants on HEAD's REAL record)."""
    b = " ".join(baseline(view=False))
    return [r for r in frozen()[1] if r not in b][:k]


def attest_break():
    r0, rc_, ri = pick_rels(3)
    parent = _C["parent"] = git(["rev-parse", f"{head()}^"]).strip()
    extra = f"{DEEP_DIR}/PLANTED_EXTRA.parquet"
    appeared = f"{DEEP_DIR}/PLANTED_NEW.parquet"
    tc_man, tc_tun = TC10_RECORDS_T[1], TC10_RECORDS_T[0]

    def tracked(wt):
        p = wt / TRACKED_PLANT
        rewrite(p, p.read_bytes() + b"\n<!-- PLANT: a reviewer's edit -->\n")

    def untracked(wt):
        (wt / "research_outputs" / "tierc11" / "review" / "PLANTED_NOTE.md").write_text("plant\n")

    def moved(wt):
        gd = Path(git(["rev-parse", "--absolute-git-dir"], cwd=wt).strip())
        if gd.parent.name != "worktrees" or not gd.name.startswith(WT_PREFIX):
            raise RuntimeError(f"HALT: {wt} is not a scratch fixture worktree (git dir {gd}) — "
                               f"HEAD not moved")
        git(["update-ref", "--no-deref", "HEAD", parent], cwd=wt)   # that worktree's own HEAD

    def stage_bent(rel: str, tag: str):
        v = variant(tag)
        data = (frozen()[0] / rel).read_bytes()
        (v / rel).unlink()
        (v / rel).write_bytes(bent(data))
        return v

    def stage_extra():
        v = variant("extra")
        (v / extra).write_bytes(b"PAR1 planted, not in any record PAR1")
        return v

    def stage_missing():
        v = variant("missing")
        (v / ri).unlink()
        return v

    def tc10_gone(wt):
        for rel in TC10_RECORDS_T:
            (wt / rel).unlink()

    def cli_red():
        rec, rc_o, rc_c, _, _ = cli_cycle("cli-red", mutate=tracked, view=main_view())
        if rec is None or rc_o != 0 or rc_c != 1:
            return []
        return [f"CLI --close exit {rc_c}: {f}" for f in rec["findings"]]

    return plants([
        ("a tracked file edited inside the worktree (LEANS.md, one line appended)",
         "porcelain after not empty", lambda: new_findings(cycle("tracked", tracked))),
        ("one byte of a staged parquet changed inside the worktree",
         f"STAGED CHANGED: {r0}", lambda: new_findings(cycle("byte", lambda wt: bend(wt / r0)))),
        ("a staged parquet that differs from HEAD's REAL PROGRESS record (its stage source bent "
         "by one byte)",
         f"STAGED != RECORD: {rc_}",
         lambda: new_findings(cycle("record", stage_root=stage_bent(rc_, "bent"), view=False),
                              view=False)),
        ("HEAD moved inside the worktree (update-ref --no-deref HEAD to the commit's parent)",
         "HEAD after", lambda: new_findings(cycle("head", moved))),
        ("an untracked, unignored file written inside the worktree",
         "porcelain after not empty", lambda: new_findings(cycle("untracked", untracked))),
        ("a staged parquet deleted inside the worktree",
         f"STAGED VANISHED: {r0}", lambda: new_findings(cycle("vanish",
                                                              lambda wt: (wt / r0).unlink()))),
        ("a new parquet written TWO levels down the worktree's research_outputs/tierc11 "
         "(regbooks/P-BRK-4H/; ignored: porcelain cannot see it)",
         f"STAGED-CLASS APPEARED: {appeared}",
         lambda: new_findings(cycle("appear", lambda wt: (wt / appeared).write_bytes(b"PAR1x")))),
        ("a staged parquet HEAD's REAL record lacks (an extra file two levels down in the stage "
         "source)",
         f"STAGED NOT IN RECORD: {extra}",
         lambda: new_findings(cycle("extra", stage_root=stage_extra(), view=False), view=False)),
        ("a parquet HEAD's REAL record holds, missing from the stage source",
         f"RECORDED NOT STAGED: {ri}",
         lambda: new_findings(cycle("missing", stage_root=stage_missing(), view=False),
                              view=False)),
        ("a LEGACY open record (the pre-hardening shape: no per-file map) with a staged byte "
         "changed",
         "STAGED SET CHANGED (legacy open record",
         lambda: new_findings(cycle("legacy", lambda wt: bend(wt / r0), legacy="hardening"))),
        ("the stage source's TC10 STAGE_D_MANIFEST.json bent by one byte (a staged TC10 record "
         "that is not the main tree's; judged on the OPEN-time findings only)",
         f"TC10 RECORD != MAIN TREE: {tc_man}",
         lambda: [f for f in new_findings(cycle("tc10-source", stage_root=stage_bent(tc_man, "tc10")))
                  if not f.endswith("(at close)")]),
        ("the worktree's staged TC10 TUNING_RESULT.json bent by one byte after open",
         f"STAGED CHANGED: {tc_tun}",
         lambda: new_findings(cycle("tc10-bent", lambda wt: bend(wt / tc_tun)))),
        ("an open record filed before the TC10 staging (no staged_tc10 map) and no TC10 record in "
         "the worktree",
         f"TC10 RECORD NOT STAGED: {tc_tun}",
         lambda: new_findings(cycle("tc10-legacy", tc10_gone, legacy="tc10"))),
        ("the CLI on a RED: a tracked edit between `--open` and `--close` through __main__",
         "CLI --close exit 1: porcelain after not empty", cli_red),
    ])


def attest_real():
    h0 = head()
    br0 = git(["symbolic-ref", "-q", "HEAD"], check=False).strip()
    view = main_view()
    main0, tc0 = _C["mscan"], own_tc10(ROOT)
    vsha = sha_bytes(view.read_bytes())
    rec_real = own_record(h0)
    dr = drift(main0, rec_real)                           # stdout only [MINOR-10]
    clock(f"drift between the main tree's staged files and HEAD's REAL PROGRESS record (this "
          f"file's own read): {len(dr)}" + (": " + "; ".join(f"{k} {r}" for k, r in dr) if dr else
                                            " — HEAD's record vouches for every staged file"))

    def inspect(wt: Path) -> dict:
        return {r: (sha_file(wt / r), (wt / r).stat().st_mode & 0o777)
                for r in TC10_RECORDS_T if (wt / r).is_file()}

    rec, rc_o, rc_c, printed, seen = cli_cycle("real", view=view, inspect=inspect)
    main1 = own_scan(ROOT)
    bad = []
    if main1 != main0 or own_tc10(ROOT) != tc0:
        bad.append("the main tree's staged files or TC10 records moved DURING the leg — a parallel "
                   "build; re-run")
    if rec is None:
        return False, f"no attestation filed (open exit {rc_o}, close exit {rc_c})"
    lens, wt = "fixture-real", A.wt_path("fixture-real")
    if rc_o != 0 or printed != str(wt):
        bad.append(f"--open exit {rc_o}, printed {printed!r} (want 0 and {wt})")
    if rec.get("verdict") != "GREEN" or rc_c != 0 or rec.get("findings"):
        bad.append(f"verdict {rec.get('verdict')} exit {rc_c} with {len(rec.get('findings') or [])} "
                   f"finding(s) (want GREEN, exit 0, none): {(rec.get('findings') or [])[:3]}")
    for tag in ("before", "after"):
        st = rec.get(tag) or {}
        if st.get("head") != h0:
            bad.append(f"HEAD {tag} {st.get('head')} != HEAD")
        if (st.get("porcelain") or "").strip():
            bad.append(f"porcelain {tag}: {st.get('porcelain')[:200]}")
    if rec.get("commit") != h0:
        bad.append("the attested commit is not HEAD")
    sf = rec.get("staged_files") or {}
    if sf != main0:
        bad.append(f"the per-file map != this file's own scan of the main tree's staged files "
                   f"({len(sf)} vs {len(main0)})")
    if rec.get("staged_artifacts") != len(sf) or rec.get("staged_sha256") != hashlib.sha256(
            json.dumps(sf, sort_keys=True).encode()).hexdigest():
        bad.append("staged_artifacts / staged_sha256 are not the map's")
    if rec.get("staged_tc10") != tc0 or sorted(tc0) != sorted(TC10_RECORDS_T):
        bad.append(f"the TC10 map {rec.get('staged_tc10')} != this file's own hash of the main "
                   f"tree's two records")
    want_seen = {r: (s, TC10_MODE_T) for r, s in tc0.items()}
    if seen != want_seen:
        bad.append(f"the open worktree's TC10 records {seen} != the main tree's bytes, mode 0444")
    pr = rec.get("progress_record") or {}
    if pr.get("blob_sha256") != vsha or pr.get("recorded_staged_class") != len(main0):
        bad.append(f"the record provenance {pr} is not the view's (sha, {len(main0)} staged-class "
                   f"paths)")
    if A.scan_staged(ROOT) != own_scan(ROOT):
        bad.append("A.scan_staged(main tree) != this file's own recursive scan")
    d0, fz = frozen()
    if A.scan_staged(d0) != fz:
        bad.append("A.scan_staged(frozen stage) != this file's own recursive scan")
    deep = sum(1 for r in main0 if r.count("/") >= 4)
    bv = baseline(view=True)
    if bv:
        bad.append(f"an untouched in-process cycle on the frozen stage and its view raised "
                   f"{len(bv)} finding(s): {bv[:3]}")
    if wt.exists() or (att_dir("real") / f"{lens}.open.json").exists():
        bad.append("the worktree or the open record survived --close")
    left = fixture_worktrees()
    if left:
        bad.append(f"HYGIENE: fixture worktrees left behind {left}")
    if git(["rev-parse", "HEAD"]).strip() != h0 or \
            git(["symbolic-ref", "-q", "HEAD"], check=False).strip() != br0:
        bad.append("the main tree's HEAD or branch moved")
    one = cli(["--commit", "HEAD", "--lens", "fixture-oneshot", "--", "true"])
    if one.returncode == 0 or "one-shot" not in (one.stderr + one.stdout) \
            or A.wt_path("fixture-oneshot").exists():
        bad.append(f"the removed one-shot mode did not HALT cleanly (exit {one.returncode})")
        force_remove(A.wt_path("fixture-oneshot"))
    ok = not bad
    return ok, (f"--open/--close through the attestation script's own __main__ at HEAD, staged from "
                f"the main tree, the record the VIEW of its staged files: open exit {rc_o} with the "
                f"worktree printed; {len(sf)} parquet staged ({deep} of them two or more levels "
                f"under research_outputs/tierc11), the per-file map == this file's own recursive "
                f"scan of the main tree's staged files; {len(tc0)} TC10 records staged, read-only "
                f"(0444) and byte-equal to the main tree's while the worktree was open, the TC10 "
                f"map == this file's own hash of them; the record provenance == the view's sha and "
                f"staged-class count; close exit {rc_c}, verdict {rec.get('verdict')}, "
                f"{len(rec.get('findings') or [])} finding(s); HEAD before/after == HEAD; porcelain "
                f"empty before/after; A.scan_staged == this file's own recursive scan on the main "
                f"tree and on the frozen stage; an untouched in-process cycle on the frozen stage "
                f"and its view: {'GREEN, no finding' if not bv else 'RED'}; the worktree and the "
                f"open record gone, no tc11-review-fixture-* worktree left, the main tree's HEAD "
                f"and branch unmoved; the one-shot `--` mode HALTs with no worktree"
                + (f"; {len(bad)} finding(s): {' · '.join(bad[:4])}" if bad else ""))


# ═════════════════════════════════════════════════════════ F-DET
def probe_bytes(out: Path) -> bytes:
    """The COMMIT-INDEPENDENT projection of the attestation record of an untouched cycle on the
    frozen stage and its view (lens fixture-det): the verdict, the findings, the per-file and TC10
    maps, the set sha, the staged-class count of the record, before/after (HEAD == the commit,
    porcelain) and the FAILS-IF text — no commit sha, no path, no record blob sha."""
    lens = "fixture-det"
    wt = A.wt_path(lens)
    force_remove(wt)
    if out.exists():
        shutil.rmtree(out)
    try:
        with record_view(frozen_view()):
            A.open_wt(head(), lens, out=out, stage_root=frozen()[0])
            A.close_wt(lens, out=out)
    finally:
        force_remove(wt)
    r = json.loads((out / f"{lens}.json").read_text())
    proj = {"lens": r["lens"], "verdict": r["verdict"], "findings": r["findings"],
            "staged_artifacts": r["staged_artifacts"], "staged_sha256": r["staged_sha256"],
            "staged_files": r["staged_files"], "staged_tc10": r["staged_tc10"],
            "recorded_staged_class": r["progress_record"].get("recorded_staged_class"),
            "before": {"head_is_commit": r["before"]["head"] == r["commit"],
                       "porcelain": r["before"]["porcelain"]},
            "after": {"head_is_commit": (r.get("after") or {}).get("head") == r["commit"],
                      "porcelain": (r.get("after") or {}).get("porcelain")},
            "fails_if": r["fails_if"]}
    return (AS_OF_LINE + "\n").encode() + (json.dumps(proj, indent=2) + "\n").encode()


def emit() -> bytes:
    if "emit" not in _C:
        _C["emit"] = probe_bytes(RUN_ROOT / "_det_attest" / "att" / "det_this")
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
    d0 = frozen()[0]
    for s in DET_SEEDS:
        d = RUN_ROOT / "_det_attest" / (f"seed_{s}" if flag == "--emit-to" else f"hashorder_{s}")
        env = dict(os.environ, NAIAD_CACHE_DIR=str(SNAP), PYTHONDONTWRITEBYTECODE="1",
                   PYTHONHASHSEED=str(s))
        r = subprocess.run([PY, "-B", str(Path(__file__).resolve()), f"{flag}={d}",
                            f"--stage-root={d0}", f"--root={RUN_ROOT}"],
                           env=env, capture_output=True, text=True, cwd=str(ROOT), timeout=1800)
        p = d / ARTIFACT
        outs[s] = (r.returncode, p.read_bytes() if p.exists() else b"")
    return outs


def det_break():
    this = emit()
    return plants([
        ("one byte bent in a copy of this run's emission", "bytes differ at byte",
         lambda: det_findings((0, this), (0, bent(this)), this)),
        ("a hash-order-dependent emission (set iteration) under the two seeds",
         "seed 1 vs seed 20260924: bytes differ",
         lambda: (lambda o: det_findings(o[DET_SEEDS[0]], o[DET_SEEDS[1]],
                                         o[DET_SEEDS[0]][1]))(det_runs("--emit-hashorder-to"))),
    ])


def det_real():
    this = emit()
    o = det_runs()
    bad = det_findings(o[DET_SEEDS[0]], o[DET_SEEDS[1]], this)
    v = json.loads(this.decode("utf-8").split("\n", 1)[1]).get("verdict")
    if v != "GREEN":
        bad.append(f"the probe's attestation verdict is {v}, not GREEN")
    return (not bad), (f"exit {o[1][0]}/{o[SEED][0]}; {len(this)} bytes (the commit-independent "
                       f"projection of the attestation record of an untouched open/close at HEAD on "
                       f"the frozen stage and its view: the per-file and TC10 maps, the record's "
                       f"staged-class count, before/after, the verdict {v}); sha "
                       f"{sha_bytes(o[1][1])[:16]}… == {sha_bytes(o[SEED][1])[:16]}… == this run "
                       f"{sha_bytes(this)[:16]}…: {not bad}" + ("" if not bad else f"; {bad}"))


# ═════════════════════════════════════════════════════════ F-GUARD
GUARD_PLANT_DIR = "research_outputs/tierc10/__attest_guard_plant__"     # never exists
GUARD_PROBES = {
    "write-tc10": ("write", lambda: open(ROOT / GUARD_PLANT_DIR / "plant.txt", "w")),
    "remove-tc10": ("write", lambda: os.remove(ROOT / GUARD_PLANT_DIR / "plant.txt")),
    "write-attest": ("write", lambda: open(ROOT / "research_outputs" / "tierc11" / "review" / "attest"
                                           / "__attest_guard_plant__" / "x.json", "w")),
    "read-tc10": ("read", lambda: open(ROOT / GUARD_PLANT_DIR / "other.json", "rb")),
}


def guard_probe_child(kind: str) -> int:
    """A probe process (this file, guard installed at import): exit 3 printing the refusal, or 0
    printing NOT REFUSED with whatever the OS said (the plant dirs do not exist)."""
    if kind == "read-staged":
        print("GUARD-PROBE " + json.dumps({r: sha_file(ROOT / r) for r in TC10_RECORDS_T}))
        return 0
    try:
        GUARD_PROBES[kind][1]()
    except GuardHalt as e:
        print(f"GUARD-PROBE {e}")
        return 3
    except OSError as e:
        print(f"GUARD-PROBE NOT REFUSED ({type(e).__name__})")
        return 0
    print("GUARD-PROBE NOT REFUSED (the operation succeeded)")
    return 0


def probe(kind: str) -> tuple[int, str]:
    env = dict(os.environ, NAIAD_CACHE_DIR=str(SNAP), PYTHONDONTWRITEBYTECODE="1")
    r = subprocess.run([PY, "-B", str(Path(__file__).resolve()), f"--guard-probe={kind}"],
                       capture_output=True, text=True, env=env, cwd=str(ROOT), timeout=300)
    line = next((ln for ln in r.stdout.splitlines() if ln.startswith("GUARD-PROBE ")), "")
    return r.returncode, line[len("GUARD-PROBE "):]


def guard_break():
    def thunk(kind):
        def f():
            if (ROOT / GUARD_PLANT_DIR).exists():
                raise RuntimeError(f"{GUARD_PLANT_DIR} exists — refusing to plant")
            rc, line = probe(kind)
            return [line] if rc == 3 else []
        return f

    return plants([
        ("a write-mode open under the main tree's research_outputs/tierc10 (subprocess probe)",
         "GUARD write refused", thunk("write-tc10")),
        ("an os.remove under the main tree's research_outputs/tierc10 (subprocess probe)",
         "GUARD write refused", thunk("remove-tc10")),
        ("a write-mode open under research_outputs/tierc11/review/attest, the records of record "
         "(subprocess probe)", "GUARD write refused", thunk("write-attest")),
        ("a read of an unlisted path under research_outputs/tierc10 (subprocess probe)",
         "GUARD read refused", thunk("read-tc10")),
    ])


def guard_real():
    rc, line = probe("read-staged")
    bad = []
    try:
        got = json.loads(line) if rc == 0 else None
    except ValueError:
        got = None
    if got != own_tc10(ROOT):
        bad.append(f"the two staged TC10 records could not be read through the guard (exit {rc})")
    if _G_LOG:
        bad.append(f"the guard refused {len(_G_LOG)} operation(s) during this run: {_G_LOG[:3]}")
    if (ROOT / GUARD_PLANT_DIR).exists():
        bad.append(f"{GUARD_PLANT_DIR} exists after the probes")
    return (not bad), (f"the {len(TC10_RECORDS_T)} staged TC10 records read through the guard in a "
                       f"probe process, byte-equal to this process's own read; the guard refused "
                       f"{len(_G_LOG)} operation(s) during this run (every fixture above ran under "
                       f"it); the plant directory does not exist"
                       + (f"; {len(bad)} finding(s): {' · '.join(bad)}" if bad else ""))


# ═════════════════════════════════════════════════════════ THE TABLE
FIXTURES = (
    ("F-ATTEST", "L-F.3 is a real check: the attestation FAILS on a mismatch or any "
     "modification, and an untouched review is GREEN",
     "any of the fourteen plants (a tracked edit; a staged byte changed; a staged parquet off "
     "HEAD's REAL record; HEAD moved; an untracked file; a staged parquet deleted; a new parquet "
     "two levels down; a staged parquet HEAD's REAL record lacks; a recorded parquet not staged; "
     "a legacy open record with a staged byte changed; the stage source's TC10 manifest bent; the "
     "worktree's staged TC10 TUNING_RESULT bent; an open record filed before the TC10 staging "
     "with no TC10 record staged; the CLI's exit on a RED) does not turn the attestation RED by its "
     "own named finding beyond an untouched cycle's",
     "--open does not exit 0 printing the worktree; the open worktree does not hold exactly the "
     "two TC10 records, read-only and byte-equal to the main tree's; --close does not exit 0 with "
     "verdict GREEN and no finding; the filed attestation's HEAD before/after is not HEAD, "
     "porcelain is not empty before/after, the per-file map is not this file's own recursive scan "
     "of the main tree's staged files (count and set sha included), the TC10 map is not this "
     "file's own hash of the main tree's two records, the record provenance is not the view's; "
     "A.scan_staged differs from this file's own recursive scan; an untouched in-process cycle on "
     "the frozen stage and its view raises a finding; the worktree or the open record survives "
     "--close, a tc11-review-fixture-* worktree is left, the main tree's HEAD or branch moves, or "
     "the removed one-shot mode does not HALT without a worktree",
     attest_break, attest_real),
    ("F-DET", "two subprocess emissions under different hash seeds, one set of bytes",
     "a one-byte-bent copy or a hash-order-dependent emission is not found",
     "the PYTHONHASHSEED 1 and 20260924 emissions of ATTEST_PROBE.txt (the commit-independent "
     "projection of the attestation record of an untouched open/close on the frozen stage and its "
     "view) differ from each other or from this run's bytes, either exits nonzero, or its verdict "
     "is not GREEN",
     det_break, det_real),
    ("F-GUARD", "this file's own guard (it does not import tierc11_env, whose armed hook refuses "
     "TC10's STAGE_D_MANIFEST.json) refuses what it must and nothing else",
     "any of the four subprocess probes (a write-mode open and an os.remove under the main tree's "
     "research_outputs/tierc10; a write under review/attest; a read of an unlisted TC10 path — "
     "every one aimed at a directory that does not exist) is not refused by the guard",
     "the two staged TC10 records cannot be read through the guard, or the guard refused any "
     "operation during this run",
     guard_break, guard_real),
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
    gp = next((a.split("=", 1)[1] for a in args if a.startswith("--guard-probe=")), None)
    if gp:                                   # F-GUARD's probe process
        return guard_probe_child(gp)
    vw = next((a.split("=", 1)[1] for a in args if a.startswith("--view=")), None)
    if vw:                                   # the CLI child: __main__ with the view
        argv = json.loads(next(a.split("=", 1)[1] for a in args if a.startswith("--attest-cli=")))
        attest_cli_child(Path(vw), argv)
        return 0
    root = RUN_ROOT = Path(next((a.split("=", 1)[1] for a in args if a.startswith("--root=")),
                                OUT))
    sr = next((a.split("=", 1)[1] for a in args if a.startswith("--stage-root=")), None)
    emit_to = next((a.split("=", 1)[1] for a in args if a.startswith("--emit-to=")), None)
    ho = next((a.split("=", 1)[1] for a in args if a.startswith("--emit-hashorder-to=")), None)
    if emit_to or ho:                        # F-DET's twins: emission only, on the parent's stage
        if sr is None:
            raise SystemExit("HALT: an emission needs --stage-root (the parent's frozen stage)")
        _C["frozen"] = (Path(sr), own_scan(Path(sr)))
        d = Path(emit_to or ho)
        d.mkdir(parents=True, exist_ok=True)
        body = probe_bytes(d / "att")
        if ho:
            body += ("set order: " + ",".join(set(HASHORDER_T)) + "\n").encode()
        (d / ARTIFACT).write_bytes(body)
        return 0
    pick = [a.lower() for a in args if not a.startswith("--")]
    t0 = time.time()
    head()
    say(AS_OF_LINE)
    say("=" * 78)
    say("TIER-C11 TC11-FIX ATTESTATION FIXTURES — scripts/tierc11_worktree_attest.py (L-F.3) — "
        "break leg first, RED or void")
    say("=" * 78)
    say(f"seed {SEED} · substrate {SNAP.name} · pin {PIN} · reviewed commit: HEAD · worktrees "
        f"{WT_PREFIX}<tag> under .claude/worktrees/ · records under <RUN_ROOT>/_det_attest/att/ · "
        f"the record: HEAD's REAL PROGRESS.json for the three record plants, else the VIEW (HEAD's "
        f"PROGRESS.json, staged-class entries replaced by this file's own scan of the stage "
        f"source) · TC10 records staged {list(TC10_RECORDS_T)}")
    try:
        for fid, title, b_if, r_if, b, r in FIXTURES:
            if not pick or any(q in fid.lower() for q in pick):
                prove(fid, title, b_if, r_if, b, r)
    finally:
        left = fixture_worktrees()
        for w in left:
            force_remove(Path(w))
        shutil.rmtree(RUN_ROOT / "_det_attest" / "stage_root", ignore_errors=True)
        for v in (RUN_ROOT / "_det_attest").glob("variant_*"):
            shutil.rmtree(v, ignore_errors=True)
    if left:
        FAILED.append(f"HYGIENE: fixture worktrees were left behind and removed at exit: {left}")
    say(f"\n  {len(PASSED)} GREEN, {len(FAILED)} RED")
    for f in FAILED:
        say(f"    RED: {f}")
    root.mkdir(parents=True, exist_ok=True)
    body = ("\n".join(LINES) + "\n").encode("utf-8")
    name = TRANSCRIPT if not pick else TRANSCRIPT.replace(".txt", "_partial.txt")
    bad = file_transcript(root / name, body, "--refile-transcript" in args or bool(pick))
    for x in bad:
        clock(x)
    clock(f"wall {time.time() - t0:.1f}s · reviewed commit {head()} · view reads answered "
          f"in-process {_C.get('view_reads', 0)} · transcript sha {sha_bytes(body)}")
    if FAILED:
        print("*** HALT: fixture mismatch. Nothing downstream is trustworthy. ***")
    return 1 if (FAILED or bad) else 0


if __name__ == "__main__":
    raise SystemExit(main())
