#!/usr/bin/env python
"""TIER-C11 · TC11-ENV — F-SUBSTRATE · F-REROOT · F-CLOSURE-ENV · F-DET.
The fixtures of the RANGE-FREE SHIM, scripts/tierc11_env.py [LEANS L-0.3].

TWO LEGS PER FIXTURE, the BREAK leg first, and it must go RED or the fixture is
VOID — a guard nobody has seen fail is a guard nobody has seen [the prove() law
of scripts/tierc10_rf_fixtures.py / tierc10_resume_fixtures.py].  A break leg is
a set of PLANTS judged one at a time; a plant counts as CAUGHT only if the
finding NAMES THE INTENDED DETECTOR (its expected substring).  A plant that
crashes is a FIXTURE DEFECT, never a catch.  Audit hooks cannot be removed, so
every plant against the hook, and every mutated copy of the shim, runs in a
SUBPROCESS; mutated copies live in a temp dir placed first on sys.path — no repo
file is touched, and no plant can create or change a file even if its guard is
broken (write plants aim at directories that do not exist; the live-cache plants
are READS of files that do not exist; the protected single files — .gitignore,
LEDGER.md — are judged by the hook's write classifier on the path STRING, never
opened).  A hook plant counts only if the AuditHalt names its detector AND the
process then exits 70 with the shim's exit report (a BLOCKED attempt can never
end in exit 0).

  F-SUBSTRATE    FAILS IF any plant is not refused by the audit hook with its
                 own detector name: a TC10-snapshot read; D.SNAPSHOT reverted to
                 TC10 — as written, as a CASE VARIANT, through the
                 /System/Volumes/Data FIRMLINK; TB.KLINES through /.nofollow;
                 dir_fd-relative reads (a guarded directory open refused; a
                 sibling's '..' judged against every open directory fd); D.OUT
                 reverted to research_outputs/tierc10/data; a read of an
                 AMENDMENT-CANDIDATE TC10 record; writes under
                 research_outputs/tierc10/ (as written and case-varied),
                 scripts/tierc10_* (as written, through the firmlink, and through
                 a dir fd whose anchor is ambiguous), exchange/status/LEDGER*,
                 and through a guarded dir_fd; live-cache opens
                 (as written and case-varied); an AuditHalt swallowed in a thread
                 (the process must still exit 70); .GITIGNORE / LEDGER.MD /
                 firmlinked .gitignore not classed as protected writes.  OR the
                 representative run (BTCUSDT 4h via TB + the v6 control book over
                 the full corridor + one allow-listed TC10 record), watched by
                 THIS file's own recording hook installed BEFORE the shim is
                 imported and classified by THIS file's own roots, opens any path
                 outside {TC11 snapshot, repo minus research_outputs/tierc10, the
                 eight allow-listed records, interpreter, OS subdirectories} — the
                 import phase additionally allowing exactly the one declared
                 import-window read; the TC10 records it saw differ from the
                 shim's ALLOW log; the exit report is absent; E.classify over
                 EVERY file under research_outputs/tierc10 allows anything but the
                 eight named records; or a shutil.rmtree of a temp tree whose
                 subdirectories are named like guarded repo directories (opened
                 relative to the walk's own dir fd) is refused.
  F-REROOT       FAILS IF any constant of L-0.3's closed list (TYPED HERE with
                 its intended target, a second object) resolves anywhere but that
                 target; the extra re-roots miss their typed targets; any module
                 global of D/TP/BK/LN still names TC10 outside the declared set;
                 any pin reads anything but 1790294400000; or TP._U12 is not TC11's
                 manifest (closed_4h_bars per stem, TP.admission agreement 17/17).
                 SABOTAGE: mutated shims that skip D.OUT / TP.AS_OF_PIN /
                 D.SNAPSHOT must HALT at the post-shim assertion; ones that skip
                 D.OUT AND the assertion, point BK.OUT at tierc11 instead of
                 tierc11/brk, or skip the _U12 re-resolve must be caught by THIS
                 fixture's own checks.
  F-CLOSURE-ENV  FAILS IF a fresh interpreter importing tierc11_env holds a
                 module whose name contains rangefinder / tierc10_census /
                 tierc10_stamps / tierc10_null, the shim's source imports one
                 anywhere (AST, function bodies included) or uses I/O the hook
                 cannot see (hook_escapes), a declared shim import is absent, or
                 the range door fails to open for a module named tierc11_nest.
                 SABOTAGE: a shadow shim importing tierc10_census (after arming:
                 the closure scan must catch it; before the self-check: the
                 shim's RANGE-FREE clause must HALT); a lazy in-function
                 tierc10_stamps import (the AST scan must catch it); the range
                 door called from a module that is not tierc11_nest (must HALT);
                 a pq.read_table call planted in the shim (hook_escapes must
                 catch it).
  F-DET          FAILS IF two subprocess emissions of the lean block + probe
                 (PYTHONHASHSEED 1, 20260924) differ by one byte from each other
                 or from this run's bytes, or either exits nonzero.  SABOTAGE:
                 the comparator on a one-byte-bent copy, and a hash-order-
                 dependent emission under the two seeds, must each be found.
BANNED: self-comparison; one example where cardinality was possible; a tuned
magnitude bound standing in for an identity; a check whose claim is not the
design's claim.  FROZEN SUBSTRATE: HALTs unless NAIAD_CACHE_DIR is the TC11
snapshot (tierc11_env's guard).  Seed 20260924.  The transcript carries no clock
and no temp path.

Run:  export NAIAD_CACHE_DIR=$HOME/.cache/naiad/snapshots/tc11_20260925 PYTHONDONTWRITEBYTECODE=1
      ~/venvs/naiad/bin/python -B scripts/tierc11_env_fixtures.py \\
          [leg-substring ...] [--refile-transcript] [--root=DIR]
Exit 0 = every leg GREEN, every break RED · 1 = a RED or VOID fixture, a
transcript finding, or a HALT.
"""
from __future__ import annotations

import ast
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
import tierc11_env as E                                              # noqa: E402  (guards first)

LEAN_TEXT = E.lean_block()

# ── FIXTURE-TYPED LITERALS: the commission, a second object, never E's own ──
HOME = Path.home()
TC11_SNAP = HOME / ".cache" / "naiad" / "snapshots" / "tc11_20260925"
TC10_SNAP = HOME / ".cache" / "naiad" / "snapshots" / "tc10_20260921"
LIVE = HOME / ".cache" / "naiad" / "data_cache"
TC11_OUT = ROOT / "research_outputs" / "tierc11"
PIN = 1790294400000                      # 2026-09-25T00:00:00Z [L-0.1]
TC10_PIN = 1790006400000                 # 2026-09-21T16:00:00Z — must never leak
SEED = 20260924
DET_SEEDS = (1, SEED)
AS_OF_LINE = "as_of_last_closed_4h: 2026-09-25T00:00:00Z"
AUDIT_EXIT = 70                          # the forced exit after a BLOCKED attempt
# L-0.3's closed list, the part that belongs to tierc11_env (C.* / stamps.* are
# tierc11_nest's), typed from LEANS.md, EACH WITH ITS INTENDED TARGET — TC10's
# layout mirrored under research_outputs/tierc11 (tierc10_run2 -> tierc11/_det_rerun,
# the L-0.5 gitignored _det_ tree) — (alias, attr, key, target)
T11 = TC11_OUT
DECL_REROOT = (
    ("D", "SNAPSHOT", None, TC11_SNAP), ("D", "OUT", None, T11 / "data"),
    ("D", "STEP_MS", "15m", 900_000),
    ("TP", "OUT", None, T11), ("TP", "OUT_RERUN", None, T11 / "_det_rerun"),
    ("TP", "AS_OF_PIN", None, T11 / "data" / "AS_OF_PIN.json"),
    ("TP", "STAGE_D_MANIFEST", None, T11 / "data" / "STAGE_D_MANIFEST.json"),
    ("TP", "SEED", None, SEED),
    ("BK", "SEED", None, SEED), ("BK", "OUT", None, T11 / "brk"),
    ("BK", "OUT_RERUN", None, T11 / "_det_rerun" / "brk"),
    ("BK", "LENS_MS", "15m", 900_000),
    ("BK", "TUNING_RESULT_FOR", "5m", T11 / "census" / "TUNING_RESULT.json"),
    ("BK", "TUNING_RESULT_FOR", "1d", T11 / "census" / "TUNING_RESULT_1d.json"),
    ("BK", "HEIGHT_VS_TOLL_PATH", None, T11 / "census" / "height_toll.parquet"),
    ("BK", "HEIGHT_VS_TOLL_VERDICT_PATH", None, T11 / "census" / "height_toll_verdict.parquet"),
    ("BK", "REGISTRY_PIN_PATH", None, T11 / "REGISTRY_PIN.json"),
    ("BK", "REGISTRATION_TEXTS_PATH", None, T11 / "REGISTRATION_TEXTS.json"),
    ("LN", "SEED", None, SEED), ("LN", "OUT", None, T11 / "lanes"),
    ("LN", "REGISTRY_PIN_PATH", None, T11 / "REGISTRY_PIN.json"),
    ("LN", "REGISTRATION_TEXTS_PATH", None, T11 / "REGISTRATION_TEXTS.json"),
)
# the bindings the list missed, re-rooted under the same law — typed targets
EXTRA_REROOT = (
    ("D", "SEED", None, SEED), ("TP", "SEEDS", None, (SEED, 20260816)),
    ("BK", "TUNING_RESULT", None, T11 / "census" / "TUNING_RESULT.json"),
)
# the bindings the shim is allowed to LEAVE naming TC10 (L-1.4 + guard constants)
DECL_LEFT = {"TP.REG_DIR", "D.SPEND_EXCLUDED_DIRS[2]", "D.SPEND_EXCLUDED_DIRS[3]",
             "D.LIVE_CACHE", "TP.LIVE_CACHE"}
FORBIDDEN = ("rangefinder", "tierc10_census", "tierc10_stamps", "tierc10_null")
SHIM_IMPORTS = ("tierc2_baseline", "tierc10_data", "tierc10_panel", "tierc10_brk",
                "tierc10_lanes", "tierc9", "tierc8", "tierc7", "tierc7_rules",
                "tierc7_lab_regime", "tierc6", "tierc6_rules", "tierc5", "tierc5_rules",
                "tierc4_rules", "tierc3_rules", "tierc2_rules")
# EXACTLY the eight records L-0.3 names + the two AM-1 rules in ("control journal, P-TRG-2 scored json,
# TUNING_RESULT, STEP0_RECORD, the five-row table, the P_AGE_1 table")
ALLOW_RECORDS = {
    "research_outputs/tierc10/panel/control_journal.parquet",
    "research_outputs/tierc10/registrations/P-TRG-2.scored.json",
    "research_outputs/tierc10/census/TUNING_RESULT.json",
    "research_outputs/tierc10/STEP0_RECORD.json",
    "research_outputs/tierc10/stamps/control_entry_by_state.parquet",
    "research_outputs/tierc10/close/P_AGE_1_TIDE_YOUTH.parquet",
    # AM-1 (LEANS_AMENDMENTS.md, 2026-09-25): two disclosure references ruled in
    "research_outputs/tierc10/census/height_toll_verdict.parquet",
    "research_outputs/tierc10/census/outcome_grid.parquet",
}
# the one TC10 record a TC10 module reads AT IMPORT (tierc10_panel: resolve_unseen12)
IMPORT_READ = "research_outputs/tierc10/data/STAGE_D_MANIFEST.json"
ALLOW_READ_IN_RUN = "research_outputs/tierc10/panel/control_journal.parquet"

OUT = TC11_OUT / "env"
RUN_ROOT = OUT
TRANSCRIPT = "FIXTURES_ENV.txt"
ARTIFACT = "ENV_PROBE.txt"
PY = sys.executable
SHIM_SRC = ROOT / "scripts" / "tierc11_env.py"
LINES: list[str] = []
PASSED: list[str] = []
FAILED: list[str] = []
_TMP_RX = re.compile(r"(/private)?/(var/folders|tmp)/[^\s'\"]+")


def say(line: str = "") -> None:            # deterministic -> transcript
    line = _TMP_RX.sub("<tmp>", line)
    print(line)
    LINES.append(line)


def clock(line: str) -> None:               # wall clock, temp paths -> stdout ONLY
    print(f"  [clock · stdout only] {line}")


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def prove(fid: str, title: str, fails_if: str, break_leg, real_leg) -> None:
    """Break first; it must go RED (ok False) or the fixture is VOID."""
    say(f"\n{fid} — {title}")
    say(f"  FAILS IF: {fails_if}")
    try:
        b_ok, b_why = break_leg()
    except Exception as e:                  # a break leg that errors proved nothing
        b_ok, b_why = True, f"break leg RAISED {type(e).__name__}: {e}"
    say(f"  [BREAK] deliberate violation -> "
        f"{'RED (correct)' if not b_ok else 'GREEN (FIXTURE IS VOID)'}: {b_why}")
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
    """rows = (name, expected detector substring, thunk -> list of findings).
    Judged ONE AT A TIME.  CAUGHT only if a finding names the intended detector.
    No finding = the plant PASSED (VOID); a finding without the substring = the
    WRONG detector (VOID); a crash = a FIXTURE DEFECT (VOID)."""
    passed, wrong, caught, crashed = [], [], [], []
    for name, want, thunk in rows:
        try:
            found = thunk()
        except SystemExit as e:
            found = [f"HALT: {e}"]
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
            caught.append(f"{name} -> {shown}")
    if crashed:
        return True, (f"{len(crashed)} plant(s) CRASHED — a FIXTURE DEFECT, not a "
                      f"finding: " + " · ".join(crashed))
    if passed or wrong:
        return True, (f"{len(passed)} plant(s) PASSED {passed}; {len(wrong)} caught by the "
                      f"WRONG detector {wrong}")
    return False, (f"all {len(caught)} plants caught by their named detector, one at a "
                   f"time: " + " · ".join(caught))


def _env() -> dict:
    return dict(os.environ, NAIAD_CACHE_DIR=str(TC11_SNAP), PYTHONDONTWRITEBYTECODE="1")


def run_py(code: str, pre_path: str | None = None, env: dict | None = None,
           timeout: int = 900) -> subprocess.CompletedProcess:
    """A fresh interpreter: repo + scripts on sys.path (a shadow dir first when
    given), then `code`."""
    head = (f"import sys\nsys.dont_write_bytecode = True\n"
            f"sys.path.insert(0, {str(ROOT)!r})\nsys.path.insert(0, {str(ROOT / 'scripts')!r})\n")
    if pre_path:
        head += f"sys.path.insert(0, {pre_path!r})\n"
    return subprocess.run([PY, "-B", "-c", head + code], capture_output=True, text=True,
                          env=env or _env(), cwd=str(ROOT), timeout=timeout)


def _last_json(out: str):
    for ln in reversed(out.strip().splitlines()):
        if ln.startswith("{") or ln.startswith("["):
            return json.loads(ln)
    raise RuntimeError(f"no JSON line in the subprocess output: {out[-300:]!r}")


# ═══════════════════════════════ independent path classification (not E's)
# THIS file's own roots and its own canonicalisation: realpath, then the deepest
# existing ancestor that IS one of the typed roots (same device + inode — a case
# variant or a volume alias of a root is that root), then a casefolded tail.
def _r(p) -> str:
    return os.path.realpath(os.path.abspath(str(p)))


def _fx_ino(p: str):
    try:
        st = os.stat(p)
    except (OSError, ValueError):
        return None
    return (st.st_dev, st.st_ino)


INTERP_ROOTS = tuple(sorted({os.path.realpath(p) for p in (sys.prefix, sys.base_prefix,
                                                            sys.exec_prefix) if p}))
# specific OS subdirectories — never the whole of /System, whose Volumes/Data
# firmlink aliases every user path [verifier MINOR-4]
OS_ROOTS = ("/System/Library", "/System/Cryptexes", "/usr/lib", "/usr/share", "/dev",
            "/private/etc", "/etc", "/Library/Preferences", "/private/var/db/timezone")
_FX_ROOTS: dict = {}
for _lab, _p in (("TC10-SNAPSHOT", TC10_SNAP), ("LIVE-CACHE", LIVE), ("tc11", TC11_SNAP),
                 ("tree", ROOT), ("tree", E.MAIN_TREE)):
    _k = _fx_ino(str(_p))
    if _k is not None:
        _FX_ROOTS.setdefault(_k, (_lab, _r(_p)))
_FX_ALLOW = {x.casefold() for x in ALLOW_RECORDS}


def _fx_anchor(real: str):
    """(root label, casefolded tail) of the deepest existing ancestor that is a
    typed root, else (None, casefolded path)."""
    p, tail = real, []
    while True:
        k = _fx_ino(p)
        if k is not None and k in _FX_ROOTS:
            return _FX_ROOTS[k][0], "/".join(reversed(tail)).casefold()
        head = os.path.dirname(p)
        if head == p:
            return None, real.casefold()
        tail.append(os.path.basename(p))
        p = head


def my_class(real: str) -> str:
    lab, tail = _fx_anchor(real)
    if lab in ("TC10-SNAPSHOT", "LIVE-CACHE", "tc11"):
        return lab
    if lab == "tree":
        if tail == "research_outputs/tierc10" or tail.startswith("research_outputs/tierc10/"):
            return "allow" if tail in _FX_ALLOW else "TC10-UNLISTED"
        return "repo"
    if any(real == t or real.startswith(t + os.sep) for t in INTERP_ROOTS):
        return "interpreter"
    if any(real == t or real.startswith(t + os.sep) for t in OS_ROOTS):
        return "os"
    return "OTHER"


def _tree_rel(real: str) -> str:
    for t in dict.fromkeys((_r(ROOT), _r(E.MAIN_TREE))):
        if real == t or real.startswith(t + os.sep):
            return os.path.relpath(real, t)
    return real


# ═══════════════════════════════════════════════════════════ F-SUBSTRATE
_PLANT_TAIL = """
import json
try:
{body}
    print(json.dumps({{"raised": False}}))
except BaseException as e:
    print(json.dumps({{"raised": True, "type": type(e).__name__, "msg": str(e)}}))
"""


def _absent_dir(p: Path) -> Path:
    if p.parent.exists():
        raise RuntimeError(f"plant target directory {p.parent} EXISTS — refusing to plant "
                           f"a write that could create a file")
    return p


def _exit_lines(stderr: str) -> list[str]:
    return [ln for ln in stderr.splitlines() if ln.startswith("TC11-AUDIT")]


def hook_plant(body: str) -> list[str]:
    """Run `body` after `import tierc11_env as E` in a fresh interpreter.  The
    finding is the refusal — an AuditHalt only — AND the forced exit: the
    process must end with exit 70 and the shim's exit report on stderr."""
    code = "import tierc11_env as E\n" + _PLANT_TAIL.format(
        body="\n".join("    " + ln for ln in body.strip().splitlines()))
    r = run_py(code)
    j = _last_json(r.stdout)
    if not j["raised"] or j["type"] != "AuditHalt":
        return []                           # passed, or refused by the OS: not caught
    rep = _exit_lines(r.stderr)
    if r.returncode != AUDIT_EXIT or not any("exit forced to" in x for x in rep):
        return [f"an AuditHalt was raised but the process exited {r.returncode} without "
                f"the forced exit (exit report {rep[:1]})"]
    return [f"{j['type']}: {j['msg']} ‖ exit {r.returncode}"]


def thread_plant(tc10_file: Path) -> list[str]:
    """An AuditHalt raised in a THREAD only prints a traceback; the main thread
    carries on.  The finding is the forced exit 70 with the exit report."""
    code = ("import tierc11_env as E\nimport json, threading\nimport pandas as pd\n"
            f"t = threading.Thread(target=lambda: pd.read_parquet({str(tc10_file)!r}))\n"
            "t.start(); t.join()\nprint(json.dumps({'main_continued': True}))\n")
    r = run_py(code)
    j = _last_json(r.stdout)
    forced = [x for x in _exit_lines(r.stderr) if "exit forced to" in x]
    if r.returncode == AUDIT_EXIT and forced and j.get("main_continued"):
        return [f"the main thread continued, the process exited {r.returncode}: {forced[-1]}"]
    return []


def write_class_plant(p: Path) -> list[str]:
    """The hook's WRITE classifier on a path STRING (never opened)."""
    lab = E._protected_write(os.path.realpath(os.path.abspath(str(p))))
    return [f"E._protected_write -> {lab}"] if lab else []


def substrate_break():
    tc10_file = TC10_SNAP / "klines" / "BTCUSDT_4h.parquet"
    if not tc10_file.is_file():
        raise RuntimeError(f"the TC10 snapshot file {tc10_file} is absent — the plant "
                           f"would read nothing")
    case10 = Path(str(TC10_SNAP).replace("tc10_20260921", "Tc10_20260921"))
    firm10 = Path("/System/Volumes/Data" + str(TC10_SNAP))
    for alias in (case10, firm10):
        if not alias.is_dir():
            raise RuntimeError(f"the alias {alias} does not resolve on this volume — the "
                               f"plant would test nothing")
    snaps = TC10_SNAP.parent
    w10 = _absent_dir(ROOT / "research_outputs" / "tierc10" / "__tc11_env_plant__" / "p.txt")
    w10c = _absent_dir(ROOT / "research_outputs" / "TIERC10" / "__tc11_env_plant__" / "p.txt")
    ws = _absent_dir(ROOT / "scripts" / "tierc10___tc11_env_plant__" / "p.py")
    wsf = _absent_dir(Path("/System/Volumes/Data" + str(ROOT)) / "scripts"
                      / "TIERC10___tc11_env_plant__" / "p.py")
    wl = _absent_dir(ROOT / "exchange" / "status" / "LEDGER___tc11_env_plant__" / "p.md")
    _absent_dir(ROOT / "research_outputs" / "tierc10" / "__tc11_env_plant__" / "q.txt")
    live = LIVE / "__tc11_env_plant__" / "p.parquet"                  # READ of an absent file
    livec = Path(str(LIVE).replace("data_cache", "Data_Cache")) / "__tc11_env_plant__" / "p.parquet"
    cand = ROOT / "research_outputs" / "tierc10" / "PROGRESS.json"
    return plants([
        ("TC10-snapshot read (pd.read_parquet)", "TC11-AUDIT[tc10-snapshot]",
         lambda: hook_plant(f"import pandas as pd\npd.read_parquet({str(tc10_file)!r})")),
        ("D.SNAPSHOT reverted to TC10, then D.load_asof", "TC11-AUDIT[tc10-snapshot]",
         lambda: hook_plant("E.D.SNAPSHOT = E.TC10_SNAPSHOT\nE.D.load_asof('BTCUSDT', '4h')")),
        ("D.SNAPSHOT = a CASE VARIANT of the TC10 snapshot (Tc10_20260921)",
         "TC11-AUDIT[tc10-snapshot]",
         lambda: hook_plant(f"from pathlib import Path\nE.D.SNAPSHOT = Path({str(case10)!r})\n"
                            f"E.D.load_asof('BTCUSDT', '4h')")),
        ("D.SNAPSHOT through the /System/Volumes/Data FIRMLINK", "TC11-AUDIT[tc10-snapshot]",
         lambda: hook_plant(f"from pathlib import Path\nE.D.SNAPSHOT = Path({str(firm10)!r})\n"
                            f"E.D.load_asof('BTCUSDT', '4h')")),
        ("TB.KLINES through the /.nofollow prefix", "TC11-AUDIT[tc10-snapshot]",
         lambda: hook_plant(f"from pathlib import Path\n"
                            f"E.TB.KLINES = Path({'/.nofollow' + str(TC10_SNAP / 'klines')!r})\n"
                            f"E.TB.load_klines('BTCUSDT', '4h')")),
        ("dir_fd-relative read: os.open(the snapshots dir), then tc10_20260921/… on it",
         "TC11-AUDIT[dir-guard]",
         lambda: hook_plant(f"import os\npfd = os.open({str(snaps)!r}, os.O_RDONLY)\n"
                            f"os.open('tc10_20260921/klines/BTCUSDT_4h.parquet', os.O_RDONLY, "
                            f"dir_fd=pfd)")),
        ("dir_fd sibling '..': os.open(the TC11 snapshot dir), then ../tc10_20260921/… on it",
         "TC11-AUDIT[tc10-snapshot]",
         lambda: hook_plant(f"import os\npfd = os.open({str(TC11_SNAP)!r}, os.O_RDONLY)\n"
                            f"os.open('../tc10_20260921/klines/BTCUSDT_4h.parquet', "
                            f"os.O_RDONLY, dir_fd=pfd)")),
        ("dir_fd write: scripts/ opened relative to the cwd while another dir fd is open, "
         "then tierc10_* on it",
         "TC11-AUDIT[tierc10-script-write]",
         lambda: hook_plant(f"import os\nos.chdir({str(ROOT)!r})\n"
                            f"other = os.open({str(TC11_OUT)!r}, os.O_RDONLY)\n"
                            f"pfd = os.open('scripts', os.O_RDONLY)\n"
                            f"os.open('tierc10___tc11_env_plant__/p.py', os.O_WRONLY | "
                            f"os.O_CREAT, dir_fd=pfd)")),
        ("D.OUT reverted to research_outputs/tierc10/data, then D.load_pin",
         "TC11-AUDIT[tc10-unlisted]",
         lambda: hook_plant(f"from pathlib import Path\n"
                            f"E.D.OUT = Path({str(ROOT / 'research_outputs' / 'tierc10' / 'data')!r})\n"
                            f"E.D.load_pin()")),
        ("read of an AMENDMENT-CANDIDATE record (research_outputs/tierc10/PROGRESS.json)",
         "TC11-AUDIT[tc10-unlisted]",
         lambda: hook_plant(f"open({str(cand)!r}).read()")),
        ("write under research_outputs/tierc10/ (open 'w')", "TC11-AUDIT[tierc10-write]",
         lambda: hook_plant(f"open({str(w10)!r}, 'w')")),
        ("write under research_outputs/TIERC10/ (case variant)", "TC11-AUDIT[tierc10-write]",
         lambda: hook_plant(f"open({str(w10c)!r}, 'w')")),
        ("write under scripts/tierc10_* (os.open O_CREAT)", "TC11-AUDIT[tierc10-script-write]",
         lambda: hook_plant(f"import os\nos.open({str(ws)!r}, os.O_WRONLY | os.O_CREAT)")),
        ("write under scripts/TIERC10_* through the firmlink", "TC11-AUDIT[tierc10-script-write]",
         lambda: hook_plant(f"import os\nos.open({str(wsf)!r}, os.O_WRONLY | os.O_CREAT)")),
        ("append under exchange/status/LEDGER* (open 'a')", "TC11-AUDIT[ledger-write]",
         lambda: hook_plant(f"open({str(wl)!r}, 'a')")),
        ("dir_fd-relative write: os.open(research_outputs), then tierc10/… on it",
         "TC11-AUDIT[dir-guard]",
         lambda: hook_plant(f"import os\npfd = os.open({str(ROOT / 'research_outputs')!r}, "
                            f"os.O_RDONLY)\nos.open('tierc10/__tc11_env_plant__/q.txt', "
                            f"os.O_WRONLY | os.O_CREAT, dir_fd=pfd)")),
        ("live-cache open (path string only)", "TC11-AUDIT[live-cache]",
         lambda: hook_plant(f"open({str(live)!r}, 'rb')")),
        ("live-cache open, CASE VARIANT (Data_Cache)", "TC11-AUDIT[live-cache]",
         lambda: hook_plant(f"open({str(livec)!r}, 'rb')")),
        ("an AuditHalt swallowed in a thread (main thread carries on)", "exit forced to 70",
         lambda: thread_plant(tc10_file)),
        ("write-class of .GITIGNORE (case variant; never opened)", "gitignore-write",
         lambda: write_class_plant(ROOT / ".GITIGNORE")),
        ("write-class of LEDGER.MD (case variant; never opened)", "ledger-write",
         lambda: write_class_plant(ROOT / "LEDGER.MD")),
        ("write-class of .gitignore through the firmlink (never opened)", "gitignore-write",
         lambda: write_class_plant(Path("/System/Volumes/Data" + str(ROOT)) / ".gitignore")),
    ])


_REAL_RUN = """
import json, os, sys
_PHASE = ["import"]
_REC = []
def _rec(ev, args):                     # THIS fixture's recorder, armed BEFORE the shim
    if ev not in ("open", "os.listdir", "os.scandir") or not args:
        return
    p = args[0]
    if p is None or isinstance(p, int):
        return
    try:
        s = os.fsdecode(os.fspath(p))
    except TypeError:
        return
    _REC.append([_PHASE[0], ev, os.path.abspath(s)])
sys.addaudithook(_rec)
import tierc11_env as E
_PHASE[0] = "run"
import pandas as pd
TB, TP, T9 = E.TB, E.TP, E.T9
k = TB.load_klines('BTCUSDT', '4h')
lo, hi, meta = TP.corridor_n(('BTCUSDT',))
book = TP.run_cell_n(TP.CONTROL_CARD, T9.V6_ROLES, ('BTCUSDT',), lo, hi)
jr = pd.read_parquet(E.tc10_record(%r))
_PHASE[0] = "report"
print(json.dumps({"rows_4h": int(len(k)), "lo": int(lo), "hi": int(hi), "n": len(book),
                  "max_exit_ms": max(int(t.exit_ms) for t in book) if book else None,
                  "journal_rows": int(len(jr)), "rec": _REC, "audit": E.audit_log()}))
""" % ALLOW_READ_IN_RUN

_RMTREE_RUN = """
import json, os, tempfile
import tierc11_env as E
names = ("scripts", "exchange", "research_outputs", "brk")
with tempfile.TemporaryDirectory() as td:
    for nm in names:
        d = os.path.join(td, nm, "status")
        os.makedirs(d)
        for i in range(3):
            with open(os.path.join(d, "f%d.txt" % i), "w") as f:
                f.write("x")
print(json.dumps({"removed": list(names), "blocked": len(E.audit_log())}))
"""

_LIST_TC10 = """
import json, os, sys
out = []
for t in sys.argv[1:]:
    base = os.path.join(t, "research_outputs", "tierc10")
    for d, _, fs in os.walk(base):
        out += [os.path.join(d, f) for f in fs]
print(json.dumps(sorted(set(out))))
"""


def substrate_real():
    r = run_py(_REAL_RUN)
    if r.returncode != 0:
        return False, f"representative run exit {r.returncode}: {r.stderr[-300:]}"
    j = _last_json(r.stdout)
    rep = _exit_lines(r.stderr)
    want_rep = "TC11-AUDIT exit report: ALLOW 1 · BLOCKED 0"
    code = (".py", ".pyc", ".so", ".pth", ".dylib")
    seen: dict[str, dict[str, str]] = {"import": {}, "run": {}}
    for ph, ev, p in j["rec"]:
        if ph in seen:
            real = _r(p)
            seen[ph].setdefault(real, my_class(real))
    ok_cls = ("tc11", "repo", "allow", "interpreter", "os")
    bad_imp = sorted(f"[{c}] {_tree_rel(p)}" for p, c in seen["import"].items()
                     if c not in ok_cls and not (c == "TC10-UNLISTED" and _tree_rel(p) == IMPORT_READ))
    bad_run = sorted(f"[{c}] {_tree_rel(p)}" for p, c in seen["run"].items() if c not in ok_cls)
    tc10_imp = sorted(_tree_rel(p) for p, c in seen["import"].items()
                      if c in ("allow", "TC10-UNLISTED"))
    tc10_run = sorted(_tree_rel(p) for p, c in seen["run"].items() if c in ("allow", "TC10-UNLISTED"))
    allow_log = sorted({a["path"] for a in j["audit"] if a["class"] == "ALLOW"})
    blocked = [a for a in j["audit"] if a["class"] != "ALLOW"]
    data = sorted(f"[{c}] " + (os.path.relpath(p, _r(TC11_SNAP)) if c == "tc11" else _tree_rel(p))
                  for p, c in seen["run"].items() if not p.endswith(code) and c != "interpreter"
                  and c != "os")
    # E.classify over EVERY file under research_outputs/tierc10 (listed by a
    # process that never imports the shim), and this file's my_class beside it
    lr = subprocess.run([PY, "-B", "-c", _LIST_TC10, *dict.fromkeys((str(ROOT), str(E.MAIN_TREE)))],
                        capture_output=True, text=True, env=_env(), cwd=str(ROOT), timeout=300)
    if lr.returncode != 0:
        return False, f"the TC10 listing exit {lr.returncode}: {lr.stderr[-300:]}"
    files = _last_json(lr.stdout)
    e_cls = {f: E.classify(_r(f)) for f in files}
    e_allow = sorted(_tree_rel(_r(f)) for f, c in e_cls.items() if c == "tc10-allow")
    e_other = sorted({c for c in e_cls.values()} - {"tc10-allow", "tc10-unlisted"})
    disagree = sorted(_tree_rel(_r(f)) for f, c in e_cls.items()
                      if (c == "tc10-allow") != (my_class(_r(f)) == "allow"))
    # the other side of the dir-fd wall: shutil.rmtree walks a temp tree through its
    # own dir fds, opening subdirectories named like the guarded repo directories
    # RELATIVE to them — a legitimate walk that must not be refused
    rt = run_py(_RMTREE_RUN)
    rtj = _last_json(rt.stdout) if rt.returncode == 0 else {"blocked": None}
    ok = (rt.returncode == 0 and rtj["blocked"] == 0
          and not bad_imp and not bad_run and tc10_imp == [IMPORT_READ]
          and tc10_run == [ALLOW_READ_IN_RUN] == allow_log and not blocked
          and want_rep in rep and j["rows_4h"] > 0 and j["hi"] + 1 == PIN and j["n"] > 0
          and j["max_exit_ms"] <= PIN and j["journal_rows"] > 0
          and e_allow == sorted(ALLOW_RECORDS) and set(E.TC10_ALLOW) == ALLOW_RECORDS
          and not e_other and not disagree)
    print(f"  [clock · stdout only] F-SUBSTRATE path counts (environment-dependent, kept out of the "
          f"transcript): import phase {len(seen['import'])}, run phase {len(seen['run'])}, files under "
          f"research_outputs/tierc10 {len(files)} (unlisted "
          f"{sum(c == 'tc10-unlisted' for c in e_cls.values())})")
    return ok, (f"BTCUSDT 4h {j['rows_4h']} rows via TB; v6 control over the full corridor "
                f"(end == pin {j['hi'] + 1 == PIN}) = {j['n']} campaigns, last exit <= pin "
                f"{j['max_exit_ms'] <= PIN}; one allow-listed record read "
                f"({j['journal_rows']} rows). THIS file's recorder (armed before the shim) + "
                f"its own roots: import phase: outside the "
                f"allowed classes {bad_imp or 0}, TC10 records read {tc10_imp} (== the one "
                f"declared import read {tc10_imp == [IMPORT_READ]}); run phase "
                f"outside {bad_run or 0}, TC10 records read "
                f"{tc10_run} == the shim's ALLOW log {allow_log}: "
                f"{tc10_run == allow_log}; BLOCKED {len(blocked)}; the {len(data)} run-phase "
                f"DATA opens {data}; exit report {rep}. E.classify over every file "
                f"under research_outputs/tierc10: tc10-allow {len(e_allow)} == the eight "
                f"typed records {e_allow == sorted(ALLOW_RECORDS)}, other classes "
                f"{e_other or 0}, disagreements with this file's classifier {disagree or 0}; "
                f"E.TC10_ALLOW == the eight {set(E.TC10_ALLOW) == ALLOW_RECORDS}. shutil.rmtree "
                f"of a temp tree with subdirectories named scripts / exchange / "
                f"research_outputs / brk (opened relative to the walk's dir fd): exit "
                f"{rt.returncode}, BLOCKED {rtj['blocked']}")


# ════════════════════════════════════════════════════════════════ F-REROOT
def _live_value(Em, alias: str, attr: str, key):
    mod = {"D": Em.D, "TP": Em.TP, "BK": Em.BK, "LN": Em.LN}[alias]
    if not hasattr(mod, attr) or (key is not None and key not in getattr(mod, attr)):
        raise KeyError(f"{alias}.{attr}" + (f"[{key!r}]" if key else "") + " ABSENT")
    v = getattr(mod, attr)
    return v[key] if key is not None else v


def _shown(v) -> str:
    if isinstance(v, (str, Path)):
        s = _r(v)
        for t, pre in ((_r(ROOT), ""), (_r(HOME), "~/")):
            if s == t or s.startswith(t + os.sep):
                return pre + os.path.relpath(s, t)
        return s
    return repr(v)


def _on_target(v, target) -> bool:
    """The live value IS the typed target: a path resolves to the same real path;
    anything else is equal."""
    if isinstance(target, Path):
        return isinstance(v, (str, Path)) and _r(v) == _r(target)
    return v == target


def reroot_findings(env_mod=None) -> tuple[list[str], int]:
    """THE CLAIM: every constant of the closed list, and every extra re-root,
    resolves to ITS TYPED TARGET (this file's literals); every module global of
    D/TP/BK/LN naming TC10 is in DECL_LEFT; no pin reads anything but 1790294400000;
    and TP._U12 is TC11's Stage D record (closed_4h_bars per stem; admission
    agreement).  Judged on the LIVE objects, with this file's own scan."""
    Em = env_mod or E
    bad, n = [], 0
    for alias, attr, key, target in DECL_REROOT + EXTRA_REROOT:
        n += 1
        name = f"{alias}.{attr}" + (f"[{key!r}]" if key else "")
        try:
            v = _live_value(Em, alias, attr, key)
        except KeyError as e:
            bad.append(str(e))
            continue
        if not _on_target(v, target):
            bad.append(f"{name}: resolves to {_shown(v)}, typed target {_shown(target)}")
    for alias, mod in (("D", Em.D), ("TP", Em.TP), ("BK", Em.BK), ("LN", Em.LN)):
        for k, v in sorted(vars(mod).items()):
            if k.startswith("__"):
                continue
            vals = ([(k, v)] if isinstance(v, (str, Path)) else
                    [(f"{k}[{kk!r}]", vv) for kk, vv in v.items()] if isinstance(v, dict) else
                    [(f"{k}[{i}]", x) for i, x in enumerate(v)] if isinstance(v, (tuple, list))
                    else [])
            for nm, x in vals:
                if not isinstance(x, (str, Path)):
                    continue
                s = str(x)
                if isinstance(x, str) and (" " in s or "/" not in s):
                    continue
                if ("tc10_20260921" in s or "research_outputs/tierc10" in s
                        or ".cache/naiad/data_cache" in s):
                    n += 1
                    if f"{alias}.{nm}" not in DECL_LEFT:
                        bad.append(f"{alias}.{nm} still names TC10: {s}")
    pins = (("D.load_pin()", lambda: int(Em.D.load_pin()["as_of_last_closed_4h_close_ms"])),
            ("TP.stage_d_pin()", lambda: Em.TP.stage_d_pin()),
            ("TP.corridor_n(CLASSIC5) end", lambda: Em.TP.corridor_n(Em.TP.CLASSIC5)[1] + 1),
            ("TP.control_window() end", lambda: Em.TP.control_window()[1] + 1))
    for k, fn in pins:
        n += 1
        try:
            v = fn()
        except SystemExit as e:             # a HALT, or the audit hook's AuditHalt
            bad.append(f"{k}: REFUSED — {e}")
            continue
        if v != PIN:
            bad.append(f"{k} = {v}" + (" — THE TC10 PIN 1790006400000 LEAKED" if v == TC10_PIN
                                        else ""))
    man = json.loads((TC11_OUT / "data" / "STAGE_D_MANIFEST.json").read_text(encoding="utf-8"))
    want4 = {r["stem"]: r.get("closed_4h_bars") for r in man["admission"]["rows"]}
    by = Em.TP._U12.get("manifest_by_stem") or {}
    for s in man["panels"]["PANEL17_stems"]:
        n += 1
        got = (by.get(s) or {}).get("closed_4h_bars")
        if got != want4.get(s):
            bad.append(f"TP._U12[{s}].closed_4h_bars = {got}, TC11 manifest {want4.get(s)}")
    if (list(Em.TP.UNSEEN12) != list(man["panels"]["UNSEEN_admitted_stems"])
            or list(Em.TP.PANEL17) != list(man["panels"]["PANEL17_stems"])):
        bad.append("TP.UNSEEN12 / TP.PANEL17 are not the TC11 manifest's panels")
    n += 1
    adm = Em.TP.admission(Em.TP.PANEL17)
    n_agree = int(adm["agrees_with_stage_d"].eq(True).sum())
    if n_agree != len(Em.TP.PANEL17):
        bad.append(f"TP.admission agrees with the TC11 Stage D record on {n_agree}/"
                   f"{len(Em.TP.PANEL17)} assets")
    return bad, n


def _shadow(tmp: Path, mutate) -> Path:
    """A COPY of the shim in `tmp`, ROOT pinned to this tree, then `mutate`d."""
    src = SHIM_SRC.read_text(encoding="utf-8")
    old = "ROOT = Path(__file__).resolve().parents[1]"
    if src.count(old) != 1:
        raise RuntimeError("the shim's ROOT line is not unique — cannot pin a shadow copy")
    src = src.replace(old, f"ROOT = Path({str(ROOT)!r})")
    src = mutate(src)
    (tmp / "tierc11_env.py").write_text(src, encoding="utf-8")
    return tmp


def _drop_line(needle: str):
    def m(src: str) -> str:
        hits = [ln for ln in src.splitlines() if needle in ln]
        if len(hits) != 1:
            raise RuntimeError(f"mutation needle {needle!r} matches {len(hits)} lines, not 1")
        return src.replace(hits[0] + "\n", "", 1)
    return m


def _swap(old: str, new: str):
    def m(src: str) -> str:
        if src.count(old) != 1:
            raise RuntimeError(f"mutation needle {old!r} matches {src.count(old)} times, not 1")
        return src.replace(old, new, 1)
    return m


def _chain(*ms):
    def m(src: str) -> str:
        for f in ms:
            src = f(src)
        return src
    return m


def _halt_line(stderr: str) -> str | None:
    """The shim's HALT message (a SystemExit prints it bare on stderr)."""
    hits = [ln for ln in stderr.strip().splitlines() if ln.startswith("HALT")]
    return hits[-1] if hits else None


def _shadow_halt(mutate) -> list[str]:
    """Import a mutated shim in a fresh interpreter; the finding is its HALT."""
    with tempfile.TemporaryDirectory() as td:
        d = _shadow(Path(td), mutate)
        r = run_py("import tierc11_env\nprint('IMPORTED')", pre_path=str(d))
    if r.returncode == 0:
        return []
    msg = _halt_line(r.stderr)
    if msg is None:
        raise RuntimeError(f"the mutated shim CRASHED (not a HALT): {r.stderr[-300:]}")
    return [msg]


def _shadow_fixture_check(mutate) -> list[str]:
    """Import a mutated shim, then run THIS file's reroot_findings against it.
    Exit 70 (the hook refused something the check touched) is a finding too."""
    with tempfile.TemporaryDirectory() as td:
        d = _shadow(Path(td), mutate)
        r = run_py("import json, tierc11_env as E\nimport tierc11_env_fixtures as F\n"
                   "bad, n = F.reroot_findings(E)\nprint(json.dumps(bad))", pre_path=str(d))
    if r.returncode not in (0, AUDIT_EXIT):
        raise RuntimeError(f"the mutated shim + fixture check exit {r.returncode}: "
                           f"{r.stderr[-300:]}")
    found = list(_last_json(r.stdout))
    if r.returncode == AUDIT_EXIT:
        found += [f"exit {r.returncode}: {x}" for x in _exit_lines(r.stderr)
                  if "exit forced to" in x]
    return found


_POST_SHIM_CALL = _swap("\n_post_shim()\n", "\n")


def _stray_pin_plant() -> list[str]:
    """D.OUT -> a temp dir whose AS_OF_PIN.json carries TC10's pin VALUE (never a
    TC10 file), with the post-shim assertion removed."""
    with tempfile.TemporaryDirectory() as td:
        (Path(td) / "AS_OF_PIN.json").write_text(json.dumps(
            {"as_of_last_closed_4h": "2026-09-21T16:00:00Z",
             "as_of_last_closed_4h_close_ms": TC10_PIN}), encoding="utf-8")
        return _shadow_fixture_check(_chain(
            _swap('("D", "OUT", None, OUT / "data", "L-0.3"),',
                  f'("D", "OUT", None, Path({td!r}), "L-0.3"),'), _POST_SHIM_CALL))


def reroot_break():
    dout = _drop_line('("D", "OUT", None, OUT / "data", "L-0.3"),')
    return plants([
        ("skip the D.OUT re-root", "D.load_pin(): 1790006400000 (the TC10 pin LEAKED)",
         lambda: _shadow_halt(dout)),
        ("skip the TP.AS_OF_PIN re-root",
         "TP.stage_d_pin(): 1790006400000 (the TC10 pin LEAKED)",
         lambda: _shadow_halt(_drop_line(
             '("TP", "AS_OF_PIN", None, OUT / "data" / "AS_OF_PIN.json", "L-0.3"),'))),
        ("skip the D.SNAPSHOT re-root", "HALT: POST-SHIM [L-0.3]",
         lambda: [f for f in _shadow_halt(_drop_line('("D", "SNAPSHOT", None, SNAPSHOT, "L-0.3"),'))
                  if "D.kline_path('BTCUSDT','4h')" in f]),
        ("skip D.OUT AND the post-shim assertion (D.load_pin reaches TC10's AS_OF_PIN.json: "
         "the armed hook must refuse it inside this fixture's pin check)",
         "D.load_pin(): REFUSED — TC11-AUDIT[tc10-unlisted]",
         lambda: _shadow_fixture_check(_chain(dout, _POST_SHIM_CALL))),
        ("D.OUT re-rooted to a stray pin record carrying TC10's pin value, post-shim "
         "assertion skipped (no TC10 path, so only this fixture's pin check can see it)",
         "D.load_pin() = 1790006400000 — THE TC10 PIN 1790006400000 LEAKED",
         _stray_pin_plant),
        ("BK.OUT re-rooted to research_outputs/tierc11 instead of tierc11/brk (post-shim "
         "blind to it)",
         "BK.OUT: resolves to research_outputs/tierc11, typed target research_outputs/tierc11/brk",
         lambda: _shadow_fixture_check(_swap('("BK", "OUT", None, OUT / "brk", "L-0.3"),',
                                             '("BK", "OUT", None, OUT, "L-0.3"),'))),
        ("skip the TP._U12 re-resolve (TC10's Stage D record stays; post-shim blind: the "
         "stems are equal)",
         "TP._U12[BTCUSDT].closed_4h_bars = ",
         lambda: _shadow_fixture_check(_chain(_drop_line("TP._U12.clear()"),
                                              _drop_line("TP._U12.update(_U12_TC11)"),
                                              _POST_SHIM_CALL))),
    ])


def reroot_real():
    bad, n = reroot_findings()
    printed = {r["name"] for r in E.REROOTS}
    want = {f"{a}.{t}" + (f"[{k!r}]" if k else "") for a, t, k, _ in DECL_REROOT}
    extra_want = {f"{a}.{t}" for a, t, _, _ in EXTRA_REROOT}
    unprinted = sorted((want | extra_want) - printed)
    extra = sorted(printed - want)
    in_block = [nm for nm in sorted(want | extra_want) if f"RE-ROOT {nm}\n" not in LEAN_TEXT]
    ok = not bad and not unprinted and not in_block
    return ok, (f"{n} checks on the live objects: {len(DECL_REROOT)} closed-list constants + "
                f"{len(EXTRA_REROOT)} extra re-roots, each against ITS TYPED TARGET (this "
                f"file's literals) + every D/TP/BK/LN global naming TC10 + 4 pins == {PIN} + "
                f"TP._U12 closed_4h_bars on the 17 TC11 stems + TP.admission agreement; "
                f"findings {bad or 0}; re-roots not performed/printed {unprinted or 0} / not "
                f"in the lean block {in_block or 0}; the shim's re-roots beyond the closed "
                f"list: {extra}")


# ══════════════════════════════════════════════════════════ F-CLOSURE-ENV
def closure_of(pre_path: str | None = None) -> list[str]:
    """The modules a FRESH interpreter holds after `import tierc11_env` — the
    WHOLE of sys.modules (what was there before the import is stdlib start-up,
    and is scanned too)."""
    code = ("import json\nimport tierc11_env\n"
            "print(json.dumps(sorted(sys.modules)))")
    r = run_py(code, pre_path=pre_path)
    if r.returncode != 0:
        msg = _halt_line(r.stderr)
        if msg is not None:
            raise SystemExit(msg)
        raise RuntimeError(f"closure subprocess exit {r.returncode}: {r.stderr[-300:]}")
    return list(_last_json(r.stdout))


def reach(mods) -> list[str]:
    return sorted(m for m in mods if any(f in m for f in FORBIDDEN))


def ast_hits(src: str) -> list[str]:
    """THIS file's AST walk (not the shim's): every Import / ImportFrom node
    anywhere, plus constant-string import calls, matched on FORBIDDEN."""
    out = []
    for n in ast.walk(ast.parse(src)):
        names = []
        if isinstance(n, ast.Import):
            names = [a.name for a in n.names]
        elif isinstance(n, ast.ImportFrom):
            names = [n.module or ""] + [a.name for a in n.names]
        elif (isinstance(n, ast.Call) and n.args and isinstance(n.args[0], ast.Constant)
              and isinstance(n.args[0].value, str)):
            f = n.func
            fn = f.attr if isinstance(f, ast.Attribute) else getattr(f, "id", "")
            if fn in ("import_module", "__import__", "tc10_import", "_tc10_import"):
                names = [n.args[0].value]
        out += [f"line {n.lineno}: {x}" for x in names if any(f in x for f in FORBIDDEN)]
    return out


_NEST_DOOR = ("import tierc11_env as E\n"
              "C = E.tc10_import('tierc10_' + 'census', allow_range=True)\n")


def _nest_door_run() -> subprocess.CompletedProcess:
    """A module NAMED tierc11_nest (a temp stand-in, first on sys.path) opens
    the range door — the other side of the MINOR-6 wall."""
    with tempfile.TemporaryDirectory() as td:
        (Path(td) / "tierc11_nest.py").write_text(_NEST_DOOR, encoding="utf-8")
        return run_py("import json, sys\nimport tierc11_nest as N\n"
                      "rp = N.C.RETEST_PINS\n"
                      "print(json.dumps({'census': 'tierc10_census' in sys.modules, "
                      "'pins': [rp['margin_atr'], rp['hold_bars'], rp['ttl_bars'], "
                      "str(rp.get('grid_sha', ''))[:8]]}))", pre_path=td)


def closure_break():
    def plant_after(src: str) -> str:       # after arming AND the self-check
        return src + ('\nwith _window("tierc10_census", TC10_SNAPSHOT):\n'
                      '    import tierc10_census as _PLANT\n')

    def plant_before(src: str) -> str:      # among the windows, before the self-check
        anchor = "    import tierc2_rules as R2                                        # noqa: E402\n"
        if src.count(anchor) != 1:
            raise RuntimeError("the tierc2_rules window line is not unique")
        return src.replace(anchor, anchor + "with _window(\"tierc10_census\", TC10_SNAPSHOT):\n"
                                            "    import tierc10_census as _PLANT\n", 1)

    def closure_plant():
        with tempfile.TemporaryDirectory() as td:
            d = _shadow(Path(td), plant_after)
            got = reach(closure_of(str(d)))
        return [f"fresh-interpreter closure reaches {got}"] if "tierc10_census" in got else []

    def selfcheck_plant():
        return _shadow_halt(plant_before)

    def lazy_plant():
        src = SHIM_SRC.read_text(encoding="utf-8") + (
            "\n\ndef _lazy_plant():\n    import tierc10_stamps  # PLANT\n    return tierc10_stamps\n")
        hits = ast_hits(src)
        return [f"AST scan: {h}" for h in hits]

    def door_plant():
        # the range door from a module that is NOT tierc11_nest, the name held in
        # a variable (invisible to any AST scan)
        r = run_py("import tierc11_env as E\nnm = 'tierc10_' + 'census'\n"
                   "E.tc10_import(nm, allow_range=True)\nprint('IMPORTED')")
        if r.returncode == 0:
            return []
        msg = _halt_line(r.stderr)
        if msg is None:
            raise RuntimeError(f"the door plant CRASHED (not a HALT): {r.stderr[-300:]}")
        return [msg]

    def escape_plant():
        src = SHIM_SRC.read_text(encoding="utf-8") + (
            "\n\ndef _escape_plant(p):\n    import pyarrow.parquet as pq  # PLANT\n"
            "    return pq.read_table(p)\n")
        return E.hook_escapes(src)

    return plants([
        ("shadow shim importing tierc10_census after arming",
         "fresh-interpreter closure reaches", closure_plant),
        ("shadow shim importing tierc10_census before its self-check",
         "RANGE-FREE: no range module in the process", selfcheck_plant),
        ("a lazy in-function tierc10_stamps import (invisible to a closure)",
         "AST scan: line", lazy_plant),
        ("tc10_import(<a variable naming tierc10_census>, allow_range=True) from __main__",
         "only tierc11_nest may import it", door_plant),
        ("a pq.read_table call planted in the shim (I/O the audit hook cannot see)",
         "read_table(…) — pyarrow native I/O", escape_plant),
    ])


def closure_real():
    mods = closure_of()
    hit = reach(mods)
    shim_src = SHIM_SRC.read_text(encoding="utf-8")
    src_hits = ast_hits(shim_src)
    esc = E.hook_escapes(shim_src)
    missing = [m for m in SHIM_IMPORTS if m not in mods]
    dr = _nest_door_run()
    door = _last_json(dr.stdout) if dr.returncode == 0 else {"census": False, "pins": None}
    ok = not hit and not src_hits and not esc and not missing and door["census"]
    return ok, (f"fresh interpreter: after `import tierc11_env` sys.modules holds {len(mods)} "
                f"modules; "
                f"names containing {list(FORBIDDEN)}: {hit or 0}; AST scan of the shim "
                f"(function bodies included): {src_hits or 0}; hook_escapes(shim): "
                f"{esc or 0}; the other side of the wall — the {len(SHIM_IMPORTS)} modules "
                f"the shim declares are all loaded: "
                f"{not missing}{'' if not missing else ' MISSING ' + str(missing)}; the range "
                f"door opens for a module named tierc11_nest: exit {dr.returncode}, "
                f"tierc10_census loaded {door['census']}, C.RETEST_PINS (margin, hold, ttl, "
                f"grid sha) {door['pins']}")


# ═══════════════════════════════════════════════════════════════════ F-DET
def probe_text() -> str:
    TP, D, T9 = E.TP, E.D, E.T9
    L = ["PROBE · TIER-C11 RANGE-FREE SHIM (deterministic)"]
    pin = D.load_pin()
    L.append(f"D.load_pin: close_ms {pin['as_of_last_closed_4h_close_ms']} "
             f"({pin['as_of_last_closed_4h']}) · TP.stage_d_pin {TP.stage_d_pin()} · "
             f"E.PIN_MS {E.PIN_MS}")
    lo, hi, meta = TP.corridor_n(E.CLASSIC5)
    L.append(f"TP.corridor_n(CLASSIC5): {TP.iso(lo)} -> {TP.iso(hi + 1)} · end == pin "
             f"{hi + 1 == E.PIN_MS} · binding {meta['binding_edge_assets']} · substrate "
             f"{meta['substrate']} · stage_d_as_of_pin {meta['stage_d_as_of_pin']}")
    for s in E.CLASSIC5:
        L.append(f"  {s}: n_4h {meta['per_asset_n_4h'][s]} · first "
                 f"{meta['per_asset_first_4h'][s]} · last open "
                 f"{meta['per_asset_last_4h_open'][s]} · floor {meta['per_asset_floor_4h'][s]}")
    cw = TP.control_window()
    L.append(f"TP.control_window() == corridor_n(CLASSIC5)[:2]: {tuple(cw) == (lo, hi)}")
    for lens in E.LENS_MS:
        d = D.load_asof("BTCUSDT", lens)
        last = int(d["open_time"].iloc[-1])
        L.append(f"D.load_asof(BTCUSDT, {lens:>3}): {len(d)} rows · last open {TP.iso(last)} · "
                 f"last close {TP.iso(last + E.LENS_MS[lens])} <= pin "
                 f"{last + E.LENS_MS[lens] <= E.PIN_MS}")
    blo, bhi, _ = TP.corridor_n(("BTCUSDT",))
    book = TP.run_cell_n(TP.CONTROL_CARD, T9.V6_ROLES, ("BTCUSDT",), blo, bhi)
    L.append(f"v6 control, BTCUSDT, full corridor: n {len(book)} · sum net_r "
             f"{round(sum(float(t.net_r) for t in book), 6)} · first entry "
             f"{TP.iso(int(min(t.entry_ms for t in book)))} · last entry "
             f"{TP.iso(int(max(t.entry_ms for t in book)))} · book sha {TP._book_sha(book)}")
    fz = E.fees()
    for s in E.CLASSIC5:
        f = fz[s]
        L.append(f"  fees {s}: taker {f['taker_bps_side']}/side ({f['taker_round_trip_bps']} rt) "
                 f"· maker {f['maker_bps_side']}/side ({f['maker_round_trip_bps']} rt, "
                 f"ASSUMPTION) · slippage tier {f['slippage_tier']} "
                 f"{f['slippage_bps_side']}/side")
    for ms in (E.ERA_CUT_MS, E.ERA_CUT_MS + 1, 1719777600000, 1719792000000, E.PIN_MS):
        L.append(f"  era_of(close {ms} = {TP.iso(ms)}{f' +{ms % 1000} ms' if ms % 1000 else ''}) = "
                 f"{E.era_of(ms)}")
    L.append(f"E.LENS_MS {E.LENS_MS}")
    L.append(f"E.UNSEEN12 {list(E.UNSEEN12)}")
    L.append(f"E.PANEL17 {list(E.PANEL17)}")
    L.append(f"E.SEED {E.SEED} · E.SEED_SENS {E.SEED_SENS} · E.N_BOOT {E.N_BOOT} · E.OUT "
             f"{os.path.relpath(E.OUT, ROOT)}")
    return "\n".join(L) + "\n"


def emit() -> bytes:
    return (LEAN_TEXT + probe_text()).encode("utf-8")


def det_findings(a: tuple, b: tuple, this: bytes) -> list[str]:
    """(exit, bytes) x 2 vs this run's bytes -> findings."""
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
        d = RUN_ROOT / "_det_env" / (f"seed_{s}" if flag == "--emit-to" else f"hashorder_{s}")
        env = dict(_env(), PYTHONHASHSEED=str(s))
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
        ("one byte bent in a copy of the seed-20260924 emission", "bytes differ at byte",
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
    key = [ln for ln in this.decode("utf-8").splitlines()
           if ln.startswith(("v6 control, BTCUSDT", "TP.corridor_n(CLASSIC5)"))]
    return (not bad), (f"exit {o[1][0]}/{o[SEED][0]}; {len(this)} bytes; sha "
                       f"{sha_bytes(o[1][1])[:16]}… == {sha_bytes(o[SEED][1])[:16]}… == this "
                       f"run {sha_bytes(this)[:16]}…: {not bad}"
                       + ("" if not bad else f"; findings {bad}")
                       + f"; the probe's key lines: {key}")


FIXTURES = (
    ("F-SUBSTRATE", "the audit hook refuses the TC10 snapshot, the live cache, unlisted TC10 "
     "records, guarded directory opens and the protected writes — by any alias; a "
     "representative run, watched independently, stays on TC11 + repo + the eight records",
     "a planted TC10-snapshot read (as written, case-varied, through the firmlink or "
     "/.nofollow, or dir_fd-relative — through a guarded directory or a sibling's '..'), "
     "D.OUT reverted to research_outputs/tierc10/data, an "
     "amendment-candidate TC10 read, a write under research_outputs/tierc10/ or "
     "scripts/tierc10_* or exchange/status/LEDGER* (as written, case-varied, through the "
     "firmlink, or dir_fd-relative), a live-cache open (as written or case-varied), or an "
     "AuditHalt swallowed in a thread is not refused by the hook's own named detector AND a "
     "forced exit 70; a case-varied / firmlinked .gitignore or LEDGER.md is not a protected "
     "write; or the representative run, seen by this file's recorder armed before the shim, "
     "opens a path outside {TC11 snapshot, repo minus research_outputs/tierc10, the eight "
     "allow-listed records, interpreter, OS subdirectories} (import phase: plus exactly the "
     "one declared import read), its TC10 reads differ from the shim's ALLOW log, or "
     "E.classify allows any file under research_outputs/tierc10 but the eight; or a "
     "shutil.rmtree of a temp tree whose subdirectories are named like guarded repo "
     "directories is refused",
     substrate_break, substrate_real),
    ("F-REROOT", "the closed re-root list lands on its typed tierc11 / tc11_20260925 targets; "
     "no TC10 pin or Stage D record leaks",
     "a closed-list constant or extra re-root resolves anywhere but its typed target, a "
     "D/TP/BK/LN global names TC10 outside the declared set, a pin reads anything but "
     "1790294400000, or TP._U12 is not TC11's Stage D record; or a shim skipping D.OUT / "
     "TP.AS_OF_PIN / D.SNAPSHOT imports without a POST-SHIM HALT, or one skipping D.OUT and "
     "the assertion, mis-targeting BK.OUT, or skipping the _U12 re-resolve escapes this "
     "fixture's own checks",
     reroot_break, reroot_real),
    ("F-CLOSURE-ENV", "tierc11_env is range-free (fresh-interpreter closure + AST + no "
     "hook-escaping I/O); the range door opens only for tierc11_nest",
     "a fresh interpreter importing tierc11_env holds a module named with rangefinder / "
     "tierc10_census / tierc10_stamps / tierc10_null, the shim's source imports one "
     "anywhere or uses I/O the hook cannot see, a declared shim import is absent, the range "
     "door opens for a caller that is not tierc11_nest, or fails to open for one that is",
     closure_break, closure_real),
    ("F-DET", "two subprocess emissions under different hash seeds, one set of bytes",
     "the PYTHONHASHSEED 1 and 20260924 emissions of the lean block + probe differ from "
     "each other or from this run's bytes, or either exits nonzero",
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
    args = sys.argv[1:]
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
    global RUN_ROOT
    root = RUN_ROOT = Path(next((a.split("=", 1)[1] for a in args if a.startswith("--root=")),
                                OUT))
    pick = [a.lower() for a in args if not a.startswith("--")]
    t0 = time.time()
    say(AS_OF_LINE)
    say("=" * 78)
    say("TIER-C11 TC11-ENV FIXTURES — scripts/tierc11_env.py (the RANGE-FREE shim, "
        "L-0.3) — break leg first, RED or void")
    say("=" * 78)
    say(f"seed {SEED} · substrate {TC11_SNAP.name} · pin {PIN}")
    for ln in LEAN_TEXT.rstrip("\n").splitlines():
        say(ln)
    for fid, title, fails_if, b, r in FIXTURES:
        if not pick or any(q in fid.lower() for q in pick):
            prove(fid, title, fails_if, b, r)
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
