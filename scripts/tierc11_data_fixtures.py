#!/usr/bin/env python
"""TIER-C11 · STAGE TC11-D — the corridor's fixtures (scripts/tierc11_data.py).

TWO LEGS PER FIXTURE, the BREAK leg first, and it must go RED or the fixture
is VOID — a guard nobody has seen fail is a guard nobody has seen [the prove()
law of scripts/tierc10_rf_fixtures.py / tierc10_resume_fixtures.py].  Every
plant is made on a COPY (a dict, a frame, a source text, a temp file); no real
artifact moves.  A plant counts as CAUGHT only when a finding NAMES THE
DETECTOR it was planted for (each plant carries that detector's tag or text);
a plant caught by another detector, a plant that passes, and a plant that
CRASHES each make the fixture VOID (hardened plants()).
  F-D11-GUARD     FAILS IF the substrate guard accepts an unset variable, a '~' or
                  relative spelling, the live cache, a directory inside it, the TC10
                  snapshot, a foreign directory, or a TC11 path without klines/; or
                  IMPORTING the module in a fresh interpreter (NAIAD_CACHE_DIR unset,
                  or a temp directory holding klines/) does not HALT before engine.data
                  or any tier module is loaded.  [round 2: defects 1, 4]
  F-D11-BOUND     FAILS IF _assert_bound() lets engine.data write anywhere but the
                  TC11 snapshot, any call that writes the snapshot does not sit
                  behind _assert_bound() on every path through its function, or a
                  file-writing call sits outside the typed write owners (so the
                  sink list is checked, not assumed).  SABOTAGE: NAIAD_CACHE_DIR
                  moved to a temp directory; a barrier removed, moved after its
                  write, or made conditional in a copy of the module's source; an
                  unguarded writer or a raw to_parquet appended.  [defect 2]
                  The sinks are DERIVED: every engine.data function that reaches a
                  write (engine/data.py's syntax tree) and every ED.<attr> call outside
                  a typed read-only allow-list; ED may not escape (getattr, an alias,
                  a rebinding, a second import).  [round 2: defect 2]
  F-D11-PORT      FAILS IF a port labelled VERBATIM is not AST-identical to its
                  source function (or constant) in scripts/tierc10_data.py, a
                  provenance comment names the wrong lines or sha, a label lies, or
                  the port set read off the provenance COMMENTS is not D.PORTS.
                  [round 2: defect 9]
  F-D11-SCOPE     FAILS IF the module's scope_paths(), PRE_STATE.json's files or the
                  manifest's files[] are not the fixture's own typed 124 paths
                  (17 stems x {5m,1h,4h,12h,1d,1w} + CLASSIC5 x 15m + 17 funding).
  F-D11-CLONE     FAILS IF any cloned pre-existing file's content up to its TC10
                  edge differs from the TC10 snapshot's bytes that re-hash to TC10's
                  manifest, or any untouched file's bytes differ from TC10's
                  manifest.  SABOTAGE: a flipped byte in a temp copy.
  F-D11-PIN       FAILS IF the filed pin is not 2026-09-25T00:00:00Z, not a 4h close,
                  not closed by the venue record in the file, moved since the seal,
                  or write-once lets a rewrite through.  SABOTAGE: one plant per
                  detector, the 4h-modulus plant under a moved contract pin.
  F-D11-CLOCK     FAILS IF FETCH_CLOCK_NOTE.json's fetch-time latest closed 4h, clock
                  row, venue clock or relabel is not what the filed records show, or
                  record_fetch_clock does not file the venue clock and the latest
                  closed 4h, or a fetch can start before it.  [defect 8]  Every
                  field of the note is re-derived (its derivation, pin-run record,
                  record shas, corroboration capture, lean erratum and re-describe
                  diff against git e97ad73), and the filed bytes must be what
                  scripts/tierc11_data_clock_note.py builds.  [round 2: defect 5]
  F-D11-PREFIX    FAILS IF any row that existed in PRE_STATE is not byte-identical
                  after the fetch.  SABOTAGE: a modified historical row in a temp copy.
  F-D11-EDGE      FAILS IF any typed kline file does not end exactly at its lens's
                  last bar closing <= the pin, has a gap, a duplicate, an off-grid
                  stamp or a row past the pin; a typed funding tape stops short of
                  the pin's hour, fails coverage, repeats a print or holds a print
                  past the pin + 60 s; or the manifest mis-describes a file (its
                  sha, flags or parquet content sha).
  F-D11-DERIVE    FAILS IF 1d / 1w recomputed from native 4h by a plain loop differ
                  by one bit from the derived files, or the manifest's content shas of
                  a derived file and of its derivation are not the plain loop's.
                  SABOTAGE: a shifted week anchor; a one-ulp volume.
  F-DET           FAILS IF two subprocess manifest builds (PYTHONHASHSEED 1 and
                  20260924) differ from each other or from the filed bytes, hold a
                  different file set, exit nonzero, carry a clock field, or differ
                  in any parquet content sha (124 files + 34 derivations) [L-F.1;
                  round 2: defect 8].
  F-D11-OUT       FAILS IF --out admits research_outputs/tierc10/data, a symlink to
                  it, a '..' traversal to it, or the stage dir's parent; refuses the
                  stage dir, a directory under it or a temp directory; or a write of
                  write_manifest does not sit behind _out_guard().  [round 2: defect 3]
  F-D11-FETCHPATH FAILS IF, offline on a temp snapshot the module is bound to, the
                  fetch path's HALTs (absent file, not in PRE_STATE, an early start,
                  an off-grid venue stamp, a Bybit 15m, an absent funding tape, a
                  symbol not TRADING, a file moved since the clone) do not fire; or a
                  --fetch resume over the filed snapshot asks or saves anything; or
                  the fetch path, replayed from clone-time bytes, does not reproduce
                  the filed content.  [round 2: defect 10]
  F-D11-UNTOUCHED FAILS IF the TC10 snapshot does not re-hash to TC10's manifest
                  after the build, TC10's own seal faults, or the live cache
                  MANIFEST.json's stat (size, mtime, inode) moved ACROSS THIS FIXTURE
                  RUN ONLY — stat only, never opened.  The stat bounds this run and
                  nothing else: the BUILD's never-touched-the-live-cache claim is BY
                  CONSTRUCTION and rests on F-D11-GUARD + F-D11-BOUND.
BANNED: self-comparison; one example where cardinality was possible; a tuned
magnitude bound standing in for an identity; a check whose claim is not the
design's claim.  FROZEN SUBSTRATE: HALTs unless NAIAD_CACHE_DIR is the TC11
snapshot.  Seed 20260924.  The transcript carries no clock and no temp path.

Run:  export NAIAD_CACHE_DIR=$HOME/.cache/naiad/snapshots/tc11_20260925 PYTHONDONTWRITEBYTECODE=1
      ~/venvs/naiad/bin/python -B scripts/tierc11_data_fixtures.py \\
          [leg-substring ...] [--refile-transcript] [--root=DIR]
Exit 0 = every leg GREEN, every break RED · 1 = a RED or VOID fixture, a transcript
finding, or a HALT (SystemExit carries the reason).
"""
from __future__ import annotations

import ast
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from contextlib import ExitStack, contextmanager
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
import tierc11_data as D            # noqa: E402  its import-time guard HALTs off the TC11 snapshot
import tierc11_data_clock_note as CN  # noqa: E402  the note's generator (no guard: reads records only)
import numpy as np                  # noqa: E402
import pandas as pd                 # noqa: E402

SEED = 20260924
DET_SEEDS = (1, SEED)
OUT = D.OUT
RUN_ROOT = OUT                      # --root=DIR redirects transcript + F-DET twins
TRANSCRIPT = "FIXTURES_DATA.txt"
DET_FILES = ("STAGE_D_MANIFEST.json", "fee_schedule.json", "STAGE_D_MANIFEST.md")
CLOCK_NOTE = "FETCH_CLOCK_NOTE.json"
STDOUT_COPY = "RUN_ALL_STDOUT_20260925.txt"
BUILD_REV = "e97ad73"                # the commit that filed the TC11-D build
AS_OF_LINE = "as_of_last_closed_4h: 2026-09-25T00:00:00Z"
# ── FIXTURE-TYPED second objects (never the module's own constants) ──────────
PIN_MS = 1_790_294_400_000
PIN_ISO = "2026-09-25T00:00:00Z"
STEP = {"5m": 300_000, "15m": 900_000, "1h": 3_600_000, "4h": 14_400_000,
        "12h": 43_200_000, "1d": 86_400_000, "1w": 604_800_000}
HOUR, DAY, WEEK, MONDAY = 3_600_000, 86_400_000, 604_800_000, 4 * 86_400_000   # 1970-01-05: Monday
FUNDING_JITTER = 60_000
TYPED_PANEL17 = ("BTCUSDT", "ETHUSDT", "SOLUSDT", "NEARUSDT", "ZECUSDT", "ENAUSDT", "PUMPUSDT",
                 "HYPEUSDT", "MNTUSDT_BYBIT", "SUIUSDT", "LTCUSDT", "XMRUSDT", "BNBUSDT", "UNIUSDT",
                 "1000PEPEUSDT", "DOGEUSDT", "1000BONKUSDT")
TYPED_CLASSIC5 = ("BTCUSDT", "ETHUSDT", "SOLUSDT", "NEARUSDT", "ZECUSDT")
TYPED_LENS_STEMS = {"5m": TYPED_PANEL17, "15m": TYPED_CLASSIC5, "1h": TYPED_PANEL17,
                    "4h": TYPED_PANEL17, "12h": TYPED_PANEL17, "1d": TYPED_PANEL17,
                    "1w": TYPED_PANEL17}
TYPED_SCOPE = tuple(rel for s in TYPED_PANEL17 for rel in
                    [f"klines/{s}_{iv}.parquet" for iv in STEP if s in TYPED_LENS_STEMS[iv]]
                    + [f"funding/{s}.parquet"])
if len(TYPED_SCOPE) != 124:
    raise SystemExit(f"HALT: the fixture's typed scope holds {len(TYPED_SCOPE)} paths, not 124")
RELABEL = "by construction (guard + _assert_bound)"
LIVE_MANIFEST = D.LIVE_CACHE / "MANIFEST.json"                  # os.stat ONLY — never opened
CLOCK_FIELD = re.compile(r'"[^"]*(elapsed|wall_clock|perf_counter|_at_run|run_started)[^"]*"\s*:')
TMP_RX = re.compile(r"[^\s'\"=]*f-d11-[A-Za-z0-9_]+")
LINES: list[str] = []
PASSED: list[str] = []
FAILED: list[str] = []
TALLY = {"break_red": 0, "break_void": 0, "real_green": 0, "real_red": 0, "plants": 0}


def _norm(s: str) -> str:
    return TMP_RX.sub("<tmp>", s)


def say(line: str = "") -> None:            # deterministic -> transcript
    line = _norm(line)
    print(line)
    LINES.append(line)


def clock(line: str) -> None:               # wall clock, temp paths -> stdout ONLY
    print(f"  [clock · stdout only] {line}")


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
    except SystemExit as e:                 # a HALT inside a real leg is a FAIL
        r_ok, r_why = False, f"HALT: {e}"
    except Exception as e:                  # a real leg that errors is a FAIL
        r_ok, r_why = False, f"raised {type(e).__name__}: {e}"
    say(f"  [{'PASS' if r_ok else 'FAIL'}] {fid}: {r_why}")
    TALLY["break_void" if b_ok else "break_red"] += 1
    TALLY["real_green" if r_ok else "real_red"] += 1
    if b_ok:
        FAILED.append(f"{fid} (break leg did not go RED — fixture proves nothing)")
    elif not r_ok:
        FAILED.append(fid)
    else:
        PASSED.append(fid)


# copied from scripts/tierc10_resume_fixtures.py:946-974 — HARDENED twice: a crash
# is a defect, and a plant is CAUGHT only by the detector it names [TC11-D_VERIFY 5]
def plants(rows) -> tuple[bool, str]:
    """rows: (name, detector, thunk -> list of findings).  One plant at a time.
    CAUGHT iff some finding contains `detector` (a tag like '[gap]' or the named
    guard's own words).  VOID (returns True) if any plant passes, is caught only
    by another detector, or crashes."""
    passed, caught, wrong, crashed = [], [], [], []
    for name, detector, thunk in rows:
        TALLY["plants"] += 1
        try:
            found = [str(x) for x in thunk()]
        except SystemExit as e:             # a HALT is a finding, and the best kind
            found = [f"HALT: {e}"]
        except Exception as e:              # a CRASH proves nothing about the guard
            crashed.append(f"{name} -> RAISED {e.__class__.__name__}: {e}")
            continue
        hit = next((f for f in found if detector in f), None)
        if hit is not None:
            caught.append(f"{name} -> {_norm(hit)[:170]}")
        elif found:
            wrong.append(f"{name} -> caught, but by ANOTHER detector (none names {detector!r}): "
                         f"{_norm(found[0])[:150]}")
        else:
            passed.append(name)
    if crashed:
        return True, (f"{len(crashed)} plant(s) CRASHED instead of being CAUGHT — an "
                      f"unexpected exception is a FIXTURE DEFECT, not a finding: "
                      + " · ".join(crashed))
    if wrong:
        return True, (f"{len(wrong)} plant(s) not caught by their named detector — the detector "
                      f"is unproven: " + " · ".join(wrong))
    if passed:
        return True, f"{len(passed)} plant(s) PASSED: {passed}"
    return False, (f"all {len(caught)} plants caught, one at a time, each by its named "
                   f"detector: " + " · ".join(caught))


@contextmanager
def mutated(obj, name: str, value):
    old = getattr(obj, name)
    setattr(obj, name, value)
    try:
        yield
    finally:
        setattr(obj, name, old)


@contextmanager
def env_moved(value: str):
    """NAIAD_CACHE_DIR set to `value` for the block, restored in finally.  Never
    the live cache: engine/data.py:47 mkdirs whatever the variable names."""
    if Path(value).resolve() == D.LIVE_CACHE.resolve() or D.LIVE_CACHE.resolve() in Path(value).resolve().parents:
        raise AssertionError("env_moved refuses the live cache")
    old = os.environ.get("NAIAD_CACHE_DIR")
    os.environ["NAIAD_CACHE_DIR"] = value
    try:
        yield
    finally:
        if old is None:
            os.environ.pop("NAIAD_CACHE_DIR", None)
        else:
            os.environ["NAIAD_CACHE_DIR"] = old


def tmpdir() -> tempfile.TemporaryDirectory:
    return tempfile.TemporaryDirectory(prefix="f-d11-")


def read_json(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def ms_of(s: str) -> int:
    return int(datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
               .timestamp() * 1000)


def tc10_expected() -> dict[str, str]:
    """rel -> sha256 from TC10's STAGE_D_MANIFEST.json, read here independently."""
    m = read_json(D.TC10_MANIFEST)
    exp = {f["path"]: f["sha256"] for f in m["files"] if f.get("present")}
    exp.update({o["path"]: o["sha256"] for o in m["out_of_scope_snapshot_files"]})
    return exp


def tree(root: Path) -> list[str]:
    return sorted(q.relative_to(root).as_posix() for q in root.rglob("*") if q.is_file())


def colset(rel: str) -> tuple[str, list[str]]:
    return (("open_time", D.KLINE_COLS) if rel.startswith("klines/")
            else ("funding_time", D.FUNDING_COLS))


def flip_byte_copy(src: Path, dst_dir: Path, rel: str) -> Path:
    q = dst_dir / rel
    q.parent.mkdir(parents=True, exist_ok=True)
    b = bytearray(src.read_bytes())
    b[len(b) // 2] ^= 0xFF
    q.write_bytes(bytes(b))
    return q


def frame_copy(df: pd.DataFrame, dst_dir: Path, rel: str) -> Path:
    q = dst_dir / rel
    q.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(q, index=False)
    return q


def src_edit(src: str, old: str, new: str) -> str:
    """A plant on a COPY of a source text.  HALTS (a fixture defect) if the
    anchor is not there exactly once."""
    if src.count(old) != 1:
        raise AssertionError(f"plant anchor found {src.count(old)} times, not once: {old[:50]!r}")
    return src.replace(old, new, 1)


def module_src() -> str:
    return Path(D.__file__).read_text(encoding="utf-8")


def sha_of(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def iso_of(ms: int) -> str:
    return datetime.fromtimestamp(int(ms) / 1000, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def content_hash(df: pd.DataFrame, cols: list[str]) -> str:
    """The manifest's content-sha law, typed HERE: sha256 of f"{rows}|{cols}" and then each
    column's raw little-endian bytes (stamps int64, values float64), in column order."""
    h = hashlib.sha256()
    h.update(f"{len(df)}|{','.join(cols)}".encode())
    for c in cols:
        a = df[c].to_numpy()
        a = a.astype(np.int64) if c.endswith("_time") else a.astype(np.float64)
        h.update(np.ascontiguousarray(a).tobytes())
    return h.hexdigest()


def git_blob(rel: str, rev: str = BUILD_REV) -> bytes:
    """A filed record's bytes at a commit (read-only `git show`)."""
    r = subprocess.run(["git", "-C", str(ROOT), "show", f"{rev}:{rel}"], capture_output=True)
    if r.returncode:
        raise AssertionError(f"git show {rev}:{rel} failed: {r.stderr.decode()[:120]}")
    return r.stdout


# ═══════════════════════════════════════════════ F-D11-GUARD  [round 2: defects 1, 4]
LATE_MODULES = ("engine.data", "engine.cells", "tierc2_rules", "tierc2_baseline", "numpy", "pandas",
                "requests")
GUARD_BLOCK = ('if not _CLONE_ONLY:\n    guard_substrate(os.environ.get("NAIAD_CACHE_DIR"))\n')
MOD_DIR = Path(D.__file__).resolve().parent     # the module the fixture imported (a mutated copy too)
ENGINE_IMPORT = "import tierc2_rules as R2                                            # noqa: E402\n"


def import_probe(mod_dir: Path, env_over: dict, drop: tuple = ("NAIAD_CACHE_DIR",)) -> tuple:
    """IMPORT tierc11_data (the copy in mod_dir) in a FRESH interpreter.  Returns (exit
    code, stdout, stderr); on a HALT the child names every engine / tier / numpy module
    already loaded at that moment (LOADED-AT-HALT)."""
    code = ("import sys\n"
            f"sys.path[:0] = {[str(mod_dir), str(ROOT), str(ROOT / 'scripts')]!r}\n"
            "try:\n"
            "    import tierc11_data\n"
            "except SystemExit as e:\n"
            f"    late = sorted(m for m in {LATE_MODULES!r} if m in sys.modules)\n"
            "    sys.stderr.write(str(e) + '\\nLOADED-AT-HALT ' + repr(late) + '\\n')\n"
            "    raise SystemExit(3)\n"
            "print('IMPORTED', tierc11_data.SNAPSHOT.name)\n")
    env = {k: v for k, v in os.environ.items() if k not in drop}
    env.update(env_over, PYTHONDONTWRITEBYTECODE="1")
    p = subprocess.run([sys.executable, "-B", "-c", code], env=env, cwd=str(ROOT),
                       capture_output=True, text=True, timeout=600)
    return p.returncode, p.stdout, p.stderr


def import_findings(rc: int, out: str, err: str) -> list[str]:
    """The import-time guard CAUGHT it iff the child exited nonzero with 'HALT:
    NAIAD_CACHE_DIR' on stderr and nothing from engine / tier / numpy loaded."""
    if rc == 0:
        return []
    m = re.search(r"LOADED-AT-HALT (\[.*\])", err)
    loaded = ast.literal_eval(m.group(1)) if m else None
    halt = next((x for x in err.splitlines() if x.startswith("HALT: NAIAD_CACHE_DIR")), None)
    if halt and loaded:                     # its message is quoted WITHOUT its 'HALT: ' prefix, so a
        #                                     late guard can never pass for the timely one's detector
        return [f"[guard-late] the import stopped only after {loaded} were loaded (its message: "
                f"{halt[len('HALT: '):]})"]
    if halt and loaded == []:
        return [f"{halt} (exit {rc}; no engine, tier or numpy module loaded at the HALT)"]
    tail = err.strip().splitlines()[-1] if err.strip() else ""
    return [f"[import-error] exit {rc}: {tail[:140]}"]


def guard_break():
    def halt(env):
        def t():
            D.guard_substrate(env)
            return []
        return t
    with tmpdir() as tmp:
        t = Path(tmp)
        foreign = t / "foreign"
        (foreign / "klines").mkdir(parents=True)
        bare = t / "bare"
        bare.mkdir()
        late = t / "late" / "scripts"
        late.mkdir(parents=True)
        src = module_src()
        src = src.replace(GUARD_BLOCK, "", 1) if src.count(GUARD_BLOCK) == 1 else src
        (late / "tierc11_data.py").write_text(src_edit(src, ENGINE_IMPORT, ENGINE_IMPORT + GUARD_BLOCK),
                                              encoding="utf-8")
        home = {"HOME": str(t)}          # a HOME in temp: no default cache path can be the real one

        def no_klines():
            with mutated(D, "SNAPSHOT", bare):
                D.guard_substrate(str(bare))
            return []
        return plants([
            ("unset", "is unset", halt(None)),
            ("empty string", "is unset", halt("")),
            ("a '~' spelling of the snapshot of record (engine.data would bind <cwd>/~/...)",
             "is not an absolute path", halt("~/.cache/naiad/snapshots/tc11_20260925")),
            ("the snapshot of record spelled relative to the repo root", "is not an absolute path",
             halt(os.path.relpath(D.SNAPSHOT, ROOT))),
            ("the live cache (path string)", "names the LIVE cache", halt(str(D.LIVE_CACHE))),
            ("a directory inside the live cache", "names the LIVE cache",
             halt(str(D.LIVE_CACHE / "klines"))),
            ("the TC10 snapshot", "names the TC10 snapshot", halt(str(D.TC10_SNAPSHOT))),
            ("a foreign directory holding klines/", "is not the TC11 snapshot", halt(str(foreign))),
            ("the snapshot of record with no klines/", "has no klines/ directory", no_klines),
            ("IMPORT the module in a fresh interpreter with NAIAD_CACHE_DIR unset (HOME in temp)",
             "HALT: NAIAD_CACHE_DIR", lambda: import_findings(*import_probe(MOD_DIR, home))),
            ("IMPORT the module in a fresh interpreter with NAIAD_CACHE_DIR = a temp dir holding "
             "klines/", "HALT: NAIAD_CACHE_DIR",
             lambda: import_findings(*import_probe(MOD_DIR,
                                                  dict(home, NAIAD_CACHE_DIR=str(foreign))))),
            ("IMPORT a module copy whose guard runs AFTER the engine and tier imports",
             "[guard-late]",
             lambda: import_findings(*import_probe(late, dict(home, NAIAD_CACHE_DIR=str(foreign)))))])


def guard_real():
    env = os.environ.get("NAIAD_CACHE_DIR")
    got = D.guard_substrate(env)
    bound = Path(D.ED.cache_dir()).resolve()
    rc, out, err = import_probe(MOD_DIR, {"NAIAD_CACHE_DIR": str(D.SNAPSHOT)})
    ok = (got == D.SNAPSHOT.resolve() == bound and D.SNAPSHOT.name == "tc11_20260925"
          and os.path.isabs(env) and os.path.expanduser(env) == env
          and rc == 0 and out.split() == ["IMPORTED", "tc11_20260925"])
    return ok, (f"NAIAD_CACHE_DIR (absolute, as given) resolves to {got.name}; engine.data.cache_dir() -> "
                f"{bound.name}; klines/ present: {(got / 'klines').is_dir()}; a fresh interpreter "
                f"IMPORTS the module under it (exit {rc}: {' '.join(out.split())})"
                + ("" if ok else f" — stderr {err.strip()[-200:]!r}"))


# ═══════════════════════════════════════════════ F-D11-BOUND  [TC11-D_VERIFY 2; round 2: defect 2]
# The write-time barrier.  SINKS are DERIVED, never assumed: every engine.data function that
# reaches a file write (read off engine/data.py's syntax tree, to a fixed point), every ED.<attr>
# call of the module outside the typed read-only allow-list, and _write_if_changed (the derived
# lenses).  A function that calls a sink NOT behind _assert_bound() is itself a writer; the
# closure is taken to a fixed point.  ED must not escape the `ED.<attr>(...)` form (getattr, an
# alias, a rebinding, a monkeypatch, a second import of engine.data), or the scan could not see it.
ED_SRC = ROOT / "engine" / "data.py"
ED_READ_ONLY = {                     # FIXTURE-TYPED: the engine.data calls allowed with no barrier
    "_get": "one HTTP GET through requests; no file",
    "_fetch_rest_klines": "REST klines into a frame; no file",
    "cache_dir": ("mkdir(exist_ok) of the directory NAIAD_CACHE_DIR names — _assert_bound's own "
                  "probe; the import guard pins that directory to the TC11 snapshot"),
}
ED_MKDIR_ONLY = ("cache_dir",)       # allow-listed although it writes: its ONLY write must be mkdir
BARRIER = "_assert_bound"
BLOCKS = ("body", "orelse", "finalbody")
# Every file-writing primitive in the module must sit in a function typed here with what it
# writes.  A write primitive in any other function is a finding, so a new writer cannot slip past.
STRONG_WRITES = {"to_parquet", "to_csv", "to_json", "to_feather", "to_pickle", "to_hdf", "to_excel",
                 "to_sql", "to_stata", "to_orc", "write_table", "write_text", "write_bytes", "write",
                 "writelines", "dump", "save", "savez", "savez_compressed", "savetxt", "tofile",
                 "mkdir", "makedirs", "rmtree", "rmdir", "removedirs", "unlink", "copyfile", "copy2",
                 "copytree", "copymode", "copystat", "symlink", "symlink_to", "hardlink_to", "link",
                 "touch", "chmod", "truncate", "ftruncate", "utime", "Popen", "system", "mkfifo",
                 "mknod", "renames"}
RECEIVER_WRITES = {"replace": ("os",), "rename": ("os",), "remove": ("os",), "copy": ("shutil",),
                   "move": ("shutil",), "run": ("subprocess",)}
WRITE_OWNERS = {
    "_write_if_changed": "the snapshot's derived lenses — a SINK, behind the barrier via its callers",
    "clone_snapshot": "creates the snapshot by cp -cpR (--clone only: the guard's one exemption)",
    "_dump": "stage records (research_outputs/tierc11/data, or --out)",
    "_fetch_log": "research_outputs/tierc11/data/FETCH_LOG.jsonl (append)",
    "write_manifest": "--out (the stage dir or a temp dir, _out_guard)",
    "pin_as_of": "mkdir of the stage dir",
    "run_all": "mkdir of the stage dir",
}


def _open_mode(mode) -> str | None:
    if mode is None:
        return None                                         # open's default mode is "r"
    if isinstance(mode, ast.Constant) and isinstance(mode.value, str):
        return f"open({mode.value})" if set(mode.value) & set("wax+") else None
    return "open(<non-literal mode>)"


def write_primitive(n) -> str | None:
    """The file-writing primitive a Call is, or None.  os.replace / os.rename also count as
    Path.replace(target) / Path.rename(target) (one positional argument, no keyword) — not
    str.replace(a, b) or datetime.replace(day=...)."""
    if not isinstance(n, ast.Call):
        return None
    f = n.func
    if isinstance(f, ast.Name):
        name, recv = f.id, None
    elif isinstance(f, ast.Attribute):
        name, recv = f.attr, (f.value.id if isinstance(f.value, ast.Name) else None)
    else:
        return None
    kw_mode = next((k.value for k in n.keywords if k.arg == "mode"), None)
    if name == "open":
        if recv == "os":
            return "os.open"
        if recv in (None, "io", "builtins", "codecs"):
            return _open_mode(n.args[1] if len(n.args) > 1 else kw_mode)
        return _open_mode(n.args[0] if n.args else kw_mode)              # Path.open(mode)
    if name in STRONG_WRITES:
        return name
    if name in RECEIVER_WRITES:
        if recv in RECEIVER_WRITES[name]:
            return f"{recv}.{name}"
        if name in ("replace", "rename") and len(n.args) == 1 and not n.keywords:
            return f"<path>.{name}"
    return None


def write_census(src: str) -> tuple[dict, list[str]]:
    """{owner: [primitive, ...]} for every file-writing call in `src`, and the
    [unclassified-write] findings for owners not typed in WRITE_OWNERS."""
    tree = ast.parse(src)
    par = _parents(tree)
    seen: dict[str, list[str]] = {}
    for n in ast.walk(tree):
        w = write_primitive(n)
        if w:
            seen.setdefault(_owner(n, par), []).append(w)
    bad = [f"[unclassified-write] {fn}: writes by {sorted(set(p))} and is not a typed write owner"
           for fn, p in sorted(seen.items()) if fn not in WRITE_OWNERS]
    return seen, bad


def engine_writers(ed_src: str) -> dict[str, list[str]]:
    """{engine.data function: the write primitives it reaches}, directly or through another
    engine.data function — read off engine/data.py's syntax tree, to a fixed point."""
    tree = ast.parse(ed_src)
    par = _parents(tree)
    defs = {n.name for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}
    reach: dict[str, set] = {}
    calls: dict[str, set] = {}
    for n in ast.walk(tree):
        if isinstance(n, ast.Call):
            fn = _owner(n, par)
            w = write_primitive(n)
            if w:
                reach.setdefault(fn, set()).add(w)
            if isinstance(n.func, ast.Name) and n.func.id in defs:
                calls.setdefault(fn, set()).add(n.func.id)
    changed = True
    while changed:
        changed = False
        for fn, cs in calls.items():
            for c in cs:
                if c in reach and not reach[c] <= reach.get(fn, set()):
                    reach.setdefault(fn, set()).update(reach[c])
                    changed = True
    return {fn: sorted(p) for fn, p in sorted(reach.items()) if fn in defs}


def ed_calls(src: str) -> set[str]:
    return {n.func.attr for n in ast.walk(ast.parse(src)) if isinstance(n, ast.Call)
            and isinstance(n.func, ast.Attribute) and isinstance(n.func.value, ast.Name)
            and n.func.value.id == "ED"}


def sink_set(src: str, ed_src: str) -> tuple[set, list[str], dict]:
    """(sinks, [ed-allow-list] findings, engine writers).  A sink is ED.<every engine.data
    writer> and ED.<every ED call of the module outside the read-only allow-list>."""
    w = engine_writers(ed_src)
    bad = [f"[ed-allow-list] ED.{a} is typed read-only here, but engine.data reaches {w[a]} from it"
           for a in sorted(ED_READ_ONLY) if a in w and not (a in ED_MKDIR_ONLY and w[a] == ["mkdir"])]
    sinks = {f"ED.{a}" for a in (ed_calls(src) | set(w)) if a not in ED_READ_ONLY}
    return sinks | {"_write_if_changed"}, bad, w


def ed_escape_findings(src: str) -> list[str]:
    """[ed-escape] ED used other than as `ED.<attr>` read (getattr, an alias, an argument, a
    monkeypatch); [ed-rebind] ED re-bound; [ed-import] engine.data reached another way."""
    tree = ast.parse(src)
    par = _parents(tree)
    bad, aliases = [], []
    for n in ast.walk(tree):
        if isinstance(n, ast.ImportFrom):
            mod = n.module or ""
            if mod == "engine.data" or mod.startswith("engine.data."):
                bad.append(f"[ed-import] from {mod} import {', '.join(a.name for a in n.names)}")
            if mod == "engine":
                aliases += [a.asname for a in n.names if a.name == "data"]
        elif isinstance(n, ast.Import):
            bad += [f"[ed-import] import {a.name}" for a in n.names
                    if a.name == "engine" or a.name.startswith("engine.data")]
        elif isinstance(n, ast.Call) and _callee(n) in ("importlib.import_module", "__import__",
                                                         "import_module"):
            bad.append(f"[ed-import] {_callee(n)}(...) — a dynamic import")
        elif (isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name)
              and n.value.id == "sys" and n.attr == "modules"):
            bad.append(f"[ed-import] sys.modules read in {_owner(n, par)}")
        elif isinstance(n, (ast.Global, ast.Nonlocal)) and "ED" in n.names:
            bad.append(f"[ed-rebind] {type(n).__name__.lower()} ED in {_owner(n, par)}")
        elif isinstance(n, ast.Name) and n.id == "ED":
            up = par.get(n)
            if isinstance(n.ctx, (ast.Store, ast.Del)):
                bad.append(f"[ed-rebind] ED re-bound in {_owner(n, par)}")
            elif not (isinstance(up, ast.Attribute) and up.value is n):
                bad.append(f"[ed-escape] ED used as a value in {_owner(n, par)} "
                           f"({type(up).__name__}) — getattr, an alias or an argument")
            elif isinstance(up.ctx, (ast.Store, ast.Del)):
                bad.append(f"[ed-escape] ED.{up.attr} assigned in {_owner(n, par)} (a monkeypatch)")
    if aliases != ["ED"]:
        bad.append(f"[ed-import] `from engine import data` appears {len(aliases)} time(s) with "
                   f"alias(es) {aliases}, not exactly once as ED")
    return bad


def _callee(node) -> str | None:
    f = node.func if isinstance(node, ast.Call) else None
    if isinstance(f, ast.Name):
        return f.id
    if isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name):
        return f"{f.value.id}.{f.attr}"
    return None


def _stmt_calls(st, name: str) -> bool:
    """`st` is a statement whose value is a call of `name` (x(), y = x(), y: T = x())."""
    v = st.value if isinstance(st, (ast.Expr, ast.Assign, ast.AnnAssign)) else None
    return isinstance(v, ast.Call) and _callee(v) == name


def _parents(tree) -> dict:
    par = {}
    for n in ast.walk(tree):
        for c in ast.iter_child_nodes(n):
            par[c] = n
    return par


def behind(node, name: str, par: dict) -> bool:
    """True iff a statement calling `name` runs before `node` on EVERY path through
    its function: an EARLIER statement of the node's own block, or of any block
    enclosing it, up to the def (structured dominance — a barrier inside an `if`
    guards only that branch; an except handler is never dominated by its try)."""
    while node in par:
        up = par[node]
        for field in BLOCKS:
            block = getattr(up, field, None)
            if isinstance(block, list):
                i = next((k for k, x in enumerate(block) if x is node), None)
                if i is not None and any(_stmt_calls(s, name) for s in block[:i]):
                    return True
        if isinstance(up, (ast.FunctionDef, ast.AsyncFunctionDef)):
            return False
        node = up
    return False


def _owner(node, par: dict) -> str:
    while node in par:
        node = par[node]
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            return node.name
    return "<module>"


def barrier_map(src: str, sinks: set) -> dict:
    """{'writers': {fn: first unguarded writer it calls}, 'guarded': [(fn, callee, line)],
    'unguarded': [(fn, callee, line)], 'called': {fn: [(caller, guarded)]}, 'entries': set}"""
    tree = ast.parse(src)
    par = _parents(tree)
    calls = sorted(((n.lineno, n.col_offset, _callee(n), _owner(n, par), n)
                    for n in ast.walk(tree) if isinstance(n, ast.Call) and _callee(n)),
                   key=lambda x: (x[0], x[1]))
    writers: dict[str, str | None] = {s: None for s in sorted(sinks)}
    changed = True
    while changed:
        changed = False
        for _, _, callee, fn, n in calls:
            if callee in writers and fn not in writers and not behind(n, BARRIER, par):
                writers[fn] = callee
                changed = True
    guarded = [(fn, callee, ln) for ln, _, callee, fn, n in calls
               if callee in writers and behind(n, BARRIER, par)]
    unguarded = [(fn, callee, ln) for ln, _, callee, fn, n in calls
                 if callee in writers and not behind(n, BARRIER, par)]
    called: dict[str, list] = {}
    for _, _, callee, fn, n in calls:
        called.setdefault(callee, []).append((fn, behind(n, BARRIER, par)))
    module_level = {callee for _, _, callee, fn, _ in calls if fn == "<module>"}
    defs = {n.name for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}
    entries = module_level | {f for f in defs if f not in called} | {"<module>"}
    return {"writers": writers, "guarded": guarded, "unguarded": unguarded,
            "called": called, "entries": entries}


def barrier_findings(src: str, ed_src: str | None = None) -> list[str]:
    """[barrier] one finding per ENTRY (a module-level call, a function nothing in the
    module calls, or module code) that reaches a snapshot write with no
    _assert_bound() on the way — named by its whole chain.  The sinks are derived
    (sink_set); their [ed-allow-list] findings ride along."""
    sinks, bad, _ = sink_set(src, ed_src if ed_src is not None else ED_SRC.read_text(encoding="utf-8"))
    m = barrier_map(src, sinks)
    for w in sorted(set(m["writers"]) - sinks):
        if w in m["entries"]:
            chain, x = [w], w
            while m["writers"].get(x) is not None and len(chain) < 20:
                x = m["writers"][x]
                chain.append(x)
            bad.append(f"[barrier] {' → '.join(chain)}: reaches a snapshot write with no "
                       f"_assert_bound() before it")
    return bad


def bound_break():
    src = module_src()
    ed_src = ED_SRC.read_text(encoding="utf-8")
    ek = ("            _assert_bound()\n            ED._save_cache(stem, iv, df[KLINE_COLS])\n")
    ef = ("    _assert_bound()\n    if venue == \"BINANCE_USDTM\":\n"
          "        _retry(lambda: ED.backfill_funding(")
    rd = "def run_derive(pin: dict) -> dict:\n    _assert_bound()\n"
    no_ek = src_edit(src, ek, "            ED._save_cache(stem, iv, df[KLINE_COLS])\n")
    after = src_edit(src, ek, "            ED._save_cache(stem, iv, df[KLINE_COLS])\n"
                              "            _assert_bound()\n")
    no_ef = src_edit(src, ef, ef.replace("    _assert_bound()\n", "", 1))
    no_rd = src_edit(src, rd, "def run_derive(pin: dict) -> dict:\n")
    cond = src_edit(src, rd, "def run_derive(pin: dict) -> dict:\n    if not pin:\n"
                             "        _assert_bound()\n")

    def plus(body: str) -> str:
        return src + "\n\n" + body
    rogue = plus("def rogue_writer(stem, df):\n    ED._save_funding(stem, df)\n")
    raw = plus("def rogue_parquet(df):\n"
               "    df.to_parquet(SNAPSHOT / 'klines' / 'BTCUSDT_4h.parquet', index=False)\n")
    bk = plus("def rogue_klines(sym):\n    ED.backfill_klines(sym, '4h', 0, 1)\n")
    unknown = plus("def rogue_new(stem, df):\n    return ED.integrity_report(stem, '4h', df)\n")
    gat = plus("def rogue_getattr(stem, df):\n    getattr(ED, '_save_cache')(stem, '4h', df)\n")
    alias = plus("def rogue_alias(stem, df):\n    E = ED\n    E._save_cache(stem, '4h', df)\n")
    patch = plus("def rogue_patch():\n    ED.cache_dir = lambda: SNAPSHOT\n")
    frm = plus("from engine.data import _save_cache as _sc\n")
    imp = plus("import engine.data\n")
    csv = plus("def rogue_csv(df):\n    df.to_csv(SNAPSHOT / 'klines' / 'x.csv')\n")
    fd = plus("def rogue_fd(b):\n    k = os.open(str(SNAPSHOT / 'x'), os.O_WRONLY | os.O_CREAT)\n"
              "    os.write(k, b)\n")
    jd = plus("def rogue_json(obj):\n    json.dump(obj, (SNAPSHOT / 'x.json').open('w'))\n")
    ed_rest = src_edit(ed_src, "        frames.append(df)\n        nxt = int(df[\"open_time\"].iloc[-1]) "
                               "+ INTERVAL_MS[interval]\n",
                       "        frames.append(df)\n        df.to_parquet(_kline_path(symbol, interval))\n"
                       "        nxt = int(df[\"open_time\"].iloc[-1]) + INTERVAL_MS[interval]\n")
    ed_cd = src_edit(ed_src, "    base.mkdir(parents=True, exist_ok=True)\n    return base\n",
                     "    base.mkdir(parents=True, exist_ok=True)\n    (base / 'x').write_text('')\n"
                     "    return base\n")

    def env_to_temp():
        with tmpdir() as tmp, env_moved(tmp):
            D._assert_bound()
        return []

    def snapshot_moved():
        with tmpdir() as tmp, mutated(D, "SNAPSHOT", Path(tmp)):
            D._assert_bound()
        return []
    return plants([
        ("NAIAD_CACHE_DIR moved to a temp directory at write time", "engine.data.cache_dir()",
         env_to_temp),
        ("the module's SNAPSHOT moved off engine.data's binding", "engine.data.cache_dir()",
         snapshot_moved),
        ("extend_klines' barrier removed (source copy)", "extend_klines → ED._save_cache",
         lambda: barrier_findings(no_ek)),
        ("extend_klines' barrier moved AFTER its write (source copy)",
         "extend_klines → ED._save_cache", lambda: barrier_findings(after)),
        ("extend_funding's barrier removed (source copy)", "extend_funding → ED.backfill_funding",
         lambda: barrier_findings(no_ef)),
        ("run_derive's barrier removed (source copy)", "run_derive → derive_lenses → _write_if_changed",
         lambda: barrier_findings(no_rd)),
        ("run_derive's barrier made conditional — earlier by line, not on every path (source copy)",
         "run_derive → derive_lenses", lambda: barrier_findings(cond)),
        ("an unguarded writer appended (source copy)", "rogue_writer → ED._save_funding",
         lambda: barrier_findings(rogue)),
        ("an ED.backfill_klines call appended — an engine.data writer the old typed SINKS lacked "
         "(source copy)", "rogue_klines → ED.backfill_klines", lambda: barrier_findings(bk)),
        ("an ED call outside the read-only allow-list appended (source copy)",
         "rogue_new → ED.integrity_report", lambda: barrier_findings(unknown)),
        ("getattr(ED, '_save_cache') appended (source copy)", "[ed-escape] ED used as a value in "
         "rogue_getattr", lambda: ed_escape_findings(gat)),
        ("an alias E = ED appended (source copy)", "[ed-escape] ED used as a value in rogue_alias",
         lambda: ed_escape_findings(alias)),
        ("ED.cache_dir monkeypatched (source copy)", "[ed-escape] ED.cache_dir assigned",
         lambda: ed_escape_findings(patch)),
        ("from engine.data import _save_cache as _sc appended (source copy)",
         "[ed-import] from engine.data import _save_cache", lambda: ed_escape_findings(frm)),
        ("import engine.data appended (source copy)", "[ed-import] import engine.data",
         lambda: ed_escape_findings(imp)),
        ("a raw to_parquet into the snapshot appended — a writer outside SINKS (source copy)",
         "[unclassified-write] rogue_parquet", lambda: write_census(raw)[1]),
        ("a df.to_csv into the snapshot appended (source copy)", "[unclassified-write] rogue_csv",
         lambda: write_census(csv)[1]),
        ("os.open + os.write into the snapshot appended (source copy)",
         "[unclassified-write] rogue_fd", lambda: write_census(fd)[1]),
        ("json.dump into the snapshot appended (source copy)", "[unclassified-write] rogue_json",
         lambda: write_census(jd)[1]),
        ("engine.data's _fetch_rest_klines gains a to_parquet (engine source copy)",
         "[ed-allow-list] ED._fetch_rest_klines", lambda: barrier_findings(src, ed_rest)),
        ("engine.data's cache_dir gains a write_text (engine source copy)",
         "[ed-allow-list] ED.cache_dir", lambda: barrier_findings(src, ed_cd))])


def bound_real():
    bad = []
    try:
        D._assert_bound()
    except SystemExit as e:
        bad.append(f"_assert_bound() HALTs under the real env: {e}")
    env = Path(os.environ.get("NAIAD_CACHE_DIR", "")).resolve()
    if env != D.SNAPSHOT.resolve():
        bad.append(f"NAIAD_CACHE_DIR not restored ({env})")
    src = module_src()
    ed_src = ED_SRC.read_text(encoding="utf-8")
    bad += barrier_findings(src, ed_src)
    bad += ed_escape_findings(src)
    census, unclassified = write_census(src)
    bad += unclassified
    if "_write_if_changed" not in census or any(o not in census for o in ("_dump", "_fetch_log")):
        bad.append(f"write census lost a typed owner: {sorted(census)}")
    sinks, _, w = sink_set(src, ed_src)
    called = ed_calls(src)
    m = barrier_map(src, sinks)
    g = [f"{fn}→{c}" for fn, c, _ in m["guarded"] if c in sinks]
    trans = sorted(set(m["writers"]) - sinks)
    callers = {x: sorted({f"{f}{'' if ok else ' (UNGUARDED)'}" for f, ok in m["called"].get(x, [])})
               for x in trans}
    if not g or any("UNGUARDED" in c for cs in callers.values() for c in cs):
        bad.append(f"barrier map: guarded {g}, transitive {callers}")
    ro = sorted(called & set(ED_READ_ONLY))
    return (not bad), (f"_assert_bound() passes under the real env (engine.data.cache_dir() -> "
                       f"{Path(D.ED.cache_dir()).resolve().name}); engine/data.py's syntax tree names "
                       f"{len(w)} writer functions; the module calls ED.{{{', '.join(sorted(called))}}}: "
                       f"{', '.join(sorted(called - set(ED_READ_ONLY)))} are sinks, "
                       f"{', '.join(ro)} the typed read-only allow-list (cache_dir mkdir-only, "
                       f"checked); {len(g)} sink call(s) sit behind _assert_bound() on every path of "
                       f"their own function: {', '.join(g)}; writer(s) with no barrier of their own: "
                       + "; ".join(f"{x} → {m['writers'][x]} (in-module callers: "
                                   f"{', '.join(callers[x])}, each behind _assert_bound())"
                                   for x in trans)
                       + f"; ED never escapes its `ED.<attr>` form and engine.data is imported once; "
                         f"write census: {sum(len(v) for v in census.values())} file-writing calls in "
                         f"{len(census)} typed owners ({', '.join(sorted(census))}), none elsewhere — "
                         f"DISCLOSURE: an out-of-module caller of a barrier-less writer, and code "
                         f"built at run time (exec/eval), are not covered; clone_snapshot's cp -cpR "
                         f"(--clone only) is the guard's one exemption"
                       if not bad else f"{len(bad)} fault(s): {bad[:3]}")


# ═══════════════════════════════════════════════ F-D11-PORT  [round 2: defect 9]
PROV_RX = re.compile(r"^# ported from scripts/tierc10_data\.py:(\d+)-(\d+) @ sha256 "
                     r"([0-9a-f]{16}) — (VERBATIM|CHANGED)")


def top_nodes(src: str) -> dict:
    """name -> top-level node: every def, and every plain `NAME = ...` assignment."""
    out = {}
    for n in ast.parse(src).body:
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            out[n.name] = n
        elif isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name):
            out[n.targets[0].id] = n
    return out


def port_targets(src: str) -> tuple[dict, list[str]]:
    """THE PORT SET, READ OFF THE COMMENTS: {name: (a, b, sha16, label)} for every
    provenance comment, bound to the first top-level def or assignment under it (only
    comment lines between)."""
    lines = src.splitlines()
    tops = sorted((n.lineno, name) for name, n in top_nodes(src).items())
    out, bad = {}, []
    for i, line in enumerate(lines, 1):
        m = PROV_RX.match(line)
        if not m:
            continue
        nxt = next(((ln, name) for ln, name in tops if ln > i), None)
        between = lines[i: nxt[0] - 1] if nxt else []
        if nxt is None or any(x.strip() and not x.lstrip().startswith("#") for x in between):
            bad.append(f"[port-orphan] line {i}: a provenance comment with no def or assignment under it")
            continue
        if nxt[1] in out:
            bad.append(f"[port-orphan] {nxt[1]}: two provenance comments")
        out[nxt[1]] = (int(m[1]), int(m[2]), m[3], m[4])
    return out, bad


def port_findings(my_src: str, tc10_src: str, ports: dict | None = None) -> tuple[list[str], dict]:
    ports = D.PORTS if ports is None else ports
    targets, bad = port_targets(my_src)
    mine, theirs = top_nodes(my_src), top_nodes(tc10_src)
    st = {"VERBATIM": 0, "CHANGED": 0, "constants": 0}
    bad += [f"[port-uncommented] {x}: D.PORTS lists it, no provenance comment sits above it"
            for x in sorted(set(ports) - set(targets))]
    bad += [f"[port-unlisted] {x}: a provenance comment names it a port, D.PORTS does not list it"
            for x in sorted(set(targets) - set(ports))]
    for name, (a, b, sha16, label) in sorted(targets.items()):
        m, t = mine.get(name), theirs.get(name)
        if t is None:
            bad.append(f"{name}: no top-level {name} in tierc10_data")
            continue
        same = ast.dump(m) == ast.dump(t)
        if (a, b) != (t.lineno, t.end_lineno):
            bad.append(f"{name}: comment names :{a}-{b}, the source is :{t.lineno}-{t.end_lineno}")
        if sha16 != D.TC10_SRC_SHA256[:16]:
            bad.append(f"{name}: comment sha {sha16} != {D.TC10_SRC_SHA256[:16]}")
        if name in ports:
            want = "VERBATIM" if ports[name] == "" else "CHANGED"
            if label != want:
                bad.append(f"{name}: labelled {label}, PORTS says {want}")
        if label == "VERBATIM" and not same:
            bad.append(f"{name}: labelled VERBATIM but its AST differs from tierc10_data.{name}")
        if label == "CHANGED" and same:
            bad.append(f"{name}: labelled CHANGED but AST-identical to its source")
        st[label] += 1
        st["constants"] += isinstance(m, ast.Assign)
    return bad, st


def _srcs() -> tuple[str, str]:
    return module_src(), D.TC10_SRC.read_text(encoding="utf-8")


def port_break():
    mine, tc10 = _srcs()
    body = src_edit(mine, 'h.update(f"{len(df)}|{\',\'.join(cols)}".encode())',
                    'h.update(f"{len(df)};{\',\'.join(cols)}".encode())')
    rng = src_edit(mine, "scripts/tierc10_data.py:428-437 @", "scripts/tierc10_data.py:428-438 @")
    lab = src_edit(mine, "scripts/tierc10_data.py:472-517 @ sha256 2cbf9bb6bcfea3ec — CHANGED",
                   "scripts/tierc10_data.py:472-517 @ sha256 2cbf9bb6bcfea3ec — VERBATIM")
    const = src_edit(mine, '@ sha256 2cbf9bb6bcfea3ec — CHANGED: gains "15m"',
                     '@ sha256 2cbf9bb6bcfea3ec — VERBATIM: gains "15m"')
    uncom = src_edit(mine, "# ported from scripts/tierc10_data.py:973-986 @ sha256 2cbf9bb6bcfea3ec "
                           "— VERBATIM\n", "")
    dropped = {k: v for k, v in D.PORTS.items() if k != "frame_sha"}
    return plants([
        ("frame_sha's separator changed in a copy of this module",
         "labelled VERBATIM but its AST differs", lambda: port_findings(body, tc10)[0]),
        ("frame_sha's provenance range off by one", "comment names :428-438",
         lambda: port_findings(rng, tc10)[0]),
        ("pin_as_of relabelled VERBATIM", "labelled VERBATIM, PORTS says CHANGED",
         lambda: port_findings(lab, tc10)[0]),
        ("the constant port STEP_MS relabelled VERBATIM", "STEP_MS: labelled VERBATIM but its AST differs",
         lambda: port_findings(const, tc10)[0]),
        ("frame_sha dropped from D.PORTS (its comment stays)", "[port-unlisted] frame_sha",
         lambda: port_findings(mine, tc10, dropped)[0]),
        ("derive_1w's provenance comment removed (it stays in D.PORTS)", "[port-uncommented] derive_1w",
         lambda: port_findings(uncom, tc10)[0])])


def port_real():
    mine, tc10 = _srcs()
    sha_now = hashlib.sha256(tc10.encode("utf-8")).hexdigest()
    bad, st = port_findings(mine, tc10)
    targets, _ = port_targets(mine)
    if sha_now != D.TC10_SRC_SHA256:
        bad.append(f"scripts/tierc10_data.py sha {sha_now[:16]} != the provenance sha")
    return (not bad), (f"{len(targets)} provenance comments (the port set, read off the comments) == "
                       f"the {len(D.PORTS)} D.PORTS entries: {st['VERBATIM']} VERBATIM (AST-identical), "
                       f"{st['CHANGED']} CHANGED (each names its change), {st['constants']} of them a "
                       f"constant (STEP_MS); source sha {sha_now[:16]} == provenance"
                       if not bad else f"{len(bad)} fault(s): {bad[:3]}")


# ═══════════════════════════════════════════════ F-D11-SCOPE  [TC11-D_VERIFY 7]
def scope_findings(module_paths, pre_files, man_paths) -> list[str]:
    """The fixture's typed 124 against the module's scope (in order), PRE_STATE's
    file set and the manifest's files[] (a set, no repeats)."""
    bad = []
    mp, typed = list(module_paths), list(TYPED_SCOPE)
    if mp != typed:
        plus, minus = sorted(set(mp) - set(typed)), sorted(set(typed) - set(mp))
        bad.append(f"[module-scope] D.scope_paths() ({len(mp)}) != the fixture's typed "
                   f"{len(typed)}: +{plus[:3]} -{minus[:3]}"
                   + ("" if plus or minus else " (same set, other order)"))
    if set(pre_files) != set(typed):
        bad.append(f"[pre-state-scope] PRE_STATE.json holds {len(set(pre_files))} files: "
                   f"+{sorted(set(pre_files) - set(typed))[:3]} -{sorted(set(typed) - set(pre_files))[:3]}")
    mn = list(man_paths)
    if set(mn) != set(typed) or len(mn) != len(set(mn)):
        bad.append(f"[manifest-scope] the manifest's files[] ({len(mn)} rows, {len(set(mn))} paths) "
                   f"!= the typed {len(typed)}: +{sorted(set(mn) - set(typed))[:3]} "
                   f"-{sorted(set(typed) - set(mn))[:3]}")
    return bad


def scope_break():
    pre = read_json(OUT / "PRE_STATE.json")
    man = [f["path"] for f in read_json(OUT / "STAGE_D_MANIFEST.json")["files"]]
    swapped = TYPED_PANEL17[:-1] + ("1000SHIBUSDT",)
    pre_bad = {**{k: v for k, v in pre["files"].items() if k != "klines/ZECUSDT_15m.parquet"},
               "klines/ZECUSDT_1m.parquet": {}}

    def module_with(name, value):
        def t():
            with mutated(D, name, value):
                return scope_findings(D.scope_paths(), pre["files"], man)
        return t
    return plants([
        ("the module's PANEL17 with its last stem swapped", "[module-scope]",
         module_with("PANEL17", swapped)),
        ("the module's CLASSIC5 without ZECUSDT (its 15m leaves scope)", "[module-scope]",
         module_with("CLASSIC5", TYPED_CLASSIC5[:4])),
        ("a PRE_STATE copy with ZECUSDT_15m swapped for ZECUSDT_1m", "[pre-state-scope]",
         lambda: scope_findings(D.scope_paths(), pre_bad, man)),
        ("a manifest copy with one files[] row dropped", "[manifest-scope]",
         lambda: scope_findings(D.scope_paths(), pre["files"], man[:-1])),
        ("a manifest copy with one files[] row repeated", "[manifest-scope]",
         lambda: scope_findings(D.scope_paths(), pre["files"], man + man[:1]))])


def scope_real():
    pre = read_json(OUT / "PRE_STATE.json")
    man = [f["path"] for f in read_json(OUT / "STAGE_D_MANIFEST.json")["files"]]
    bad = scope_findings(D.scope_paths(), pre["files"], man)
    nk = sum(1 for r in TYPED_SCOPE if r.startswith("klines/"))
    n15 = sum(1 for r in TYPED_SCOPE if r.endswith("_15m.parquet"))
    return (not bad), (f"the fixture's typed {len(TYPED_SCOPE)} paths ({len(TYPED_PANEL17)} stems x "
                       f"{{5m,1h,4h,12h,1d,1w}} = {nk - n15} + CLASSIC5 x 15m = {n15} + "
                       f"{len(TYPED_SCOPE) - nk} funding) == D.scope_paths() in order == PRE_STATE.json's "
                       f"{len(pre['files'])} == the manifest's files[] {len(man)}"
                       if not bad else f"{len(bad)} fault(s): {bad[:3]}")


# ═══════════════════════════════════════════════ F-D11-CLONE
def clone_findings(root: Path, rels: list[str], exp: dict, scope: set) -> tuple[list[str], dict]:
    """In-scope files: the TC10 snapshot's file must be TC10's manifest bytes, and
    the TC11 file's rows up to that file's last stamp must be those rows, byte for
    byte (raw column bytes).  Every other file: whole-file sha == TC10's record."""
    bad, st = [], {"prefix": 0, "whole": 0, "rows": 0}
    for rel in rels:
        q, src = root / rel, D.TC10_SNAPSHOT / rel
        if rel in scope:
            if D.file_sha256(src) != exp[rel]:
                bad.append(f"{rel}: the TC10 snapshot's own file is not TC10's manifest bytes")
                continue
            col, cols = colset(rel)
            t10 = pd.read_parquet(src).sort_values(col)
            cur = pd.read_parquet(q).sort_values(col)
            pref = cur[cur[col] <= int(t10[col].max())]
            if D.frame_sha(pref, cols) != D.frame_sha(t10, cols):
                bad.append(f"{rel}: rows up to the TC10 edge differ from the TC10 snapshot")
            st["prefix"] += 1
            st["rows"] += len(t10)
        else:
            want = exp.get(rel) or D.file_sha256(src)
            if D.file_sha256(q) != want:
                bad.append(f"{rel}: bytes differ from TC10's record")
            st["whole"] += 1
    return bad, st


def clone_break():
    exp = tc10_expected()
    pre = read_json(OUT / "PRE_STATE.json")
    other = sorted((r for r in exp if r not in pre["files"]),
                   key=lambda r: (D.SNAPSHOT / r).stat().st_size)[0]
    with tmpdir() as tmp:
        t = Path(tmp)
        flip_byte_copy(D.SNAPSHOT / other, t / "flip", other)
        f4 = pd.read_parquet(D.SNAPSHOT / "klines/BTCUSDT_4h.parquet").sort_values("open_time")
        f4 = f4.reset_index(drop=True)
        f4.loc[100, "close"] = f4.loc[100, "close"] + 0.1
        frame_copy(f4, t / "edit", "klines/BTCUSDT_4h.parquet")
        return plants([
            (f"a flipped byte in a temp copy of {other}", "bytes differ from TC10's record",
             lambda: clone_findings(t / "flip", [other], exp, set(pre["files"]))[0]),
            ("a temp copy of klines/BTCUSDT_4h.parquet with one historical close moved",
             "rows up to the TC10 edge differ",
             lambda: clone_findings(t / "edit", ["klines/BTCUSDT_4h.parquet"], exp,
                                    set(pre["files"]))[0])])


def clone_real():
    exp = tc10_expected()
    pre = read_json(OUT / "PRE_STATE.json")
    att = read_json(OUT / D.CLONE_ATTEST)
    have, src = tree(D.SNAPSHOT), tree(D.TC10_SNAPSHOT)
    bad = []
    if have != src:
        bad.append(f"file sets differ: +{sorted(set(have) - set(src))[:3]} "
                   f"-{sorted(set(src) - set(have))[:3]}")
    for rel, v in att["files"].items():
        if rel in exp and v["sha256"] != exp[rel]:
            bad.append(f"CLONE_ATTEST {rel}: clone sha != TC10 manifest")
    if set(att["files"]) != set(src):
        bad.append("CLONE_ATTEST does not list every file of the TC10 snapshot")
    f2, st = clone_findings(D.SNAPSHOT, have, exp, set(pre["files"]))
    bad += f2
    return (not bad), (f"{len(have)} files == the TC10 snapshot's set; CLONE_ATTEST {len(att['files'])} "
                       f"files, {sum(1 for r in att['files'] if r in exp)} pinned by TC10's manifest; "
                       f"{st['prefix']} in-scope files: rows up to the TC10 edge ({st['rows']} rows) "
                       f"byte-identical to the TC10 snapshot; {st['whole']} other files byte-identical"
                       if not bad else f"{len(bad)} fault(s): {bad[:3]}")


# ═══════════════════════════════════════════════ F-D11-PIN  [TC11-D_VERIFY 4]
def pin_record_findings(pin: dict, pin_sha: str, seal: dict) -> list[str]:
    """The fixture's OWN reading of the filed pin, against fixture-typed values."""
    bad = []
    c, k, vs = int(pin["as_of_last_closed_4h_close_ms"]), pin["venue_kline_of_pinned_bar"], \
        int(pin["venue_server_time_ms"])
    if not (c == PIN_MS and pin["as_of_last_closed_4h"] == PIN_ISO and c % STEP["4h"] == 0):
        bad.append(f"[contract-pin] close {c} / {pin['as_of_last_closed_4h']} is not the contract's "
                   f"4h close {PIN_MS} / {PIN_ISO}")
    if not (int(k[0]) + STEP["4h"] - 1 == int(k[6]) == c - 1 < vs):
        bad.append(f"[venue-kline] the filed venue kline (open {k[0]}, closeTime {k[6]}) does not "
                   f"prove the bar closing {c} closed before the venue clock {vs}")
    if seal["files"]["AS_OF_PIN.json"]["sha256"] != pin_sha:
        bad.append("[seal] AS_OF_PIN.json moved since the seal")
    return bad


def write_once_findings(pin: dict, before: bytes) -> list[str]:
    """_dump_once over a temp copy of the filed pin must HALT and leave its bytes."""
    with tmpdir() as tmp:
        cp = Path(tmp) / "AS_OF_PIN.json"
        cp.write_bytes(before)
        refused = False
        try:
            D._dump_once(dict(pin, as_of_last_closed_4h_close_ms=PIN_MS + STEP["4h"]), cp)
        except SystemExit:
            refused = True
        if not refused or cp.read_bytes() != before:
            return [f"[write-once] a rewrite of the filed pin went through (refused: {refused})"]
    return []


def reread_findings(pin: dict, before: bytes | None) -> list[str]:
    """A second pin_as_of over a directory holding the filed pin must re-read it
    and never reach the network (requests.get is a tripwire here)."""
    def no_net(*a, **kw):
        raise AssertionError("pin_as_of reached the network")
    with tmpdir() as tmp:
        cp = Path(tmp) / "AS_OF_PIN.json"
        if before is not None:
            cp.write_bytes(before)
        try:
            with mutated(D.requests, "get", no_net):
                again = D.pin_as_of(Path(tmp))
        except AssertionError as e:
            return [f"[no-network] {e} instead of re-reading a filed pin"]
        except SystemExit as e:
            return [f"[re-read] pin_as_of HALTed on the filed pin: {e}"]
        if again != pin or before is None or cp.read_bytes() != before:
            return ["[re-read] a second pin_as_of did not return the filed pin unchanged"]
    return []


def pin_break():
    pin = read_json(OUT / "AS_OF_PIN.json")
    before = (OUT / "AS_OF_PIN.json").read_bytes()
    seal = read_json(OUT / D.SEAL)
    sha = D.file_sha256(OUT / "AS_OF_PIN.json")
    keys = D.tc10_pin_keys()
    c, o, vc = (pin["as_of_last_closed_4h_close_ms"], pin["as_of_last_closed_4h_open_ms"],
                pin["venue_close_time_of_pinned_bar_ms"])
    k = list(pin["venue_kline_of_pinned_bar"])
    c5 = c + 300_000                                # a close 5 min off the 4h grid, all else consistent
    notclose = dict(pin, as_of_last_closed_4h_close_ms=c5, as_of_last_closed_4h_open_ms=c5 - D.MS_4H,
                    as_of_last_closed_4h=D.iso(c5), as_of_last_closed_4h_open=D.iso(c5 - D.MS_4H),
                    venue_close_time_of_pinned_bar_ms=c5 - 1,
                    venue_kline_of_pinned_bar=[c5 - D.MS_4H] + k[1:6] + [c5 - 1] + k[7:])

    def under_moved_contract():
        with mutated(D, "PIN_CLOSE_MS", c5):
            return D.pin_findings(notclose, keys)

    def dump_is_plain():
        with mutated(D, "_dump_once", D._dump):
            return write_once_findings(pin, before)
    seal_bad = json.loads(json.dumps(seal))
    seal_bad["files"]["AS_OF_PIN.json"]["sha256"] = "0" * 64
    return plants([
        ("a close 5 min off the 4h grid, the contract pin moved with it (only the modulus can see it)",
         "is not a 4h bar close", under_moved_contract),
        ("a bar still forming by the venue clock", "still forming",
         lambda: D.pin_findings(dict(pin, venue_server_time_ms=vc - 1), keys)),
        ("a pin one 4h bar later than the contract's", "!= the contract's pin",
         lambda: D.pin_findings(dict(pin, as_of_last_closed_4h_close_ms=c + D.MS_4H,
                                     as_of_last_closed_4h_open_ms=o + D.MS_4H), keys)),
        ("an open 1 ms off close - 4h", "!= close - 4h",
         lambda: D.pin_findings(dict(pin, as_of_last_closed_4h_open_ms=o - 1), keys)),
        ("an ISO string that disagrees with its ms", "ISO strings disagree",
         lambda: D.pin_findings(dict(pin, as_of_last_closed_4h="2026-09-25T04:00:00Z"), keys)),
        ("a venue closeTime 1 ms early", "!= close - 1 ms",
         lambda: D.pin_findings(dict(pin, venue_close_time_of_pinned_bar_ms=vc - 1), keys)),
        ("a filed venue kline of the previous bar", "the filed venue kline row is not the pinned bar",
         lambda: D.pin_findings(dict(pin, venue_kline_of_pinned_bar=[k[0] - D.MS_4H] + k[1:]), keys)),
        ("a seed that is not TC11's", "seed 1 != 20260924",
         lambda: D.pin_findings(dict(pin, seed=1), keys)),
        ("a TC10 schema key dropped", "TC10 AS_OF_PIN keys missing",
         lambda: D.pin_findings({x: v for x, v in pin.items() if x != "local_clock_skew_ms"}, keys)),
        ("the fixture's reading: an ISO string off the contract", "[contract-pin]",
         lambda: pin_record_findings(dict(pin, as_of_last_closed_4h="2026-09-25T04:00:00Z"), sha, seal)),
        ("the fixture's reading: the filed kline's closeTime (k[6]) off by one", "[venue-kline]",
         lambda: pin_record_findings(dict(pin, venue_kline_of_pinned_bar=k[:6] + [k[6] + 1] + k[7:]),
                                     sha, seal)),
        ("the fixture's reading: a seal copy holding another sha", "[seal]",
         lambda: pin_record_findings(pin, sha, seal_bad)),
        ("the module's _dump_once replaced by the plain _dump", "[write-once]", dump_is_plain),
        ("a directory with no filed pin (pin_as_of must go to the venue: the tripwire fires)",
         "[no-network]", lambda: reread_findings(pin, None))])


def pin_real():
    p = OUT / "AS_OF_PIN.json"
    pin, before = read_json(p), p.read_bytes()
    bad = list(D.pin_findings(pin, D.tc10_pin_keys()))
    bad += pin_record_findings(pin, D.file_sha256(p), read_json(OUT / D.SEAL))
    bad += write_once_findings(pin, before)
    bad += reread_findings(pin, before)
    if p.read_bytes() != before:
        bad.append("the real pin file moved during this leg")
    return (not bad), (f"pin {pin['as_of_last_closed_4h']} (close ms {pin['as_of_last_closed_4h_close_ms']}, "
                       f"a 4h multiple); venue closeTime {pin['venue_close_time_of_pinned_bar_ms']} < venue "
                       f"clock {pin['venue_server_time_ms']}; latest closed at the pin run "
                       f"{pin['latest_closed_4h_at_pin_run']}; TC10's {len(D.tc10_pin_keys())} keys all "
                       f"present; == the seal's sha; a rewrite HALTs and a second pin re-reads, no network"
                       if not bad else f"{len(bad)} fault(s): {bad[:3]}")


# ═══════════════════════════════════════════════ F-D11-CLOCK  [TC11-D_VERIFY 8]
SYNTH_SRV = PIN_MS + 2 * HOUR + 1_234      # 02:00:01.234Z: its 4h floor is the pin, its 1h floor is not


NOTE_RECORDS = ("AS_OF_PIN.json", "WRITE_ONCE_SEAL.json", "FETCH_LOG.jsonl")
REDESCRIBED = ("STAGE_D_MANIFEST.json", "STAGE_D_MANIFEST.md", "fee_schedule.json")
QUOTED = ("18", "19", "20", "135", "155")


def clock_ctx() -> dict:
    """Everything the note is re-derived from, read ONCE: the filed records, the filed
    stdout copy, the re-described files and their bytes at git e97ad73, LEANS.md, and
    the note generator's own bytes."""
    ctx = {"lines": (OUT / D.FETCH_LOG).read_text(encoding="utf-8").splitlines(),
           "seal": read_json(OUT / D.SEAL), "pin": read_json(OUT / "AS_OF_PIN.json"),
           "man": read_json(OUT / "STAGE_D_MANIFEST.json"),
           "bytes": {n: (OUT / n).read_bytes() for n in NOTE_RECORDS + REDESCRIBED + (STDOUT_COPY,)},
           "blobs": {n: git_blob(f"research_outputs/tierc11/data/{n}") for n in REDESCRIBED},
           "leans": (ROOT / D.LEANS_DOC).read_text(encoding="utf-8").splitlines(),
           "gen": CN.note_bytes(CN.build_note())}
    return ctx


def _flat(x, p: str = "") -> dict:
    if isinstance(x, dict):
        out = {}
        for k, v in x.items():
            out.update(_flat(v, f"{p}.{k}" if p else k))
        return out if x else {p: {}}
    if isinstance(x, list):
        out = {}
        for i, v in enumerate(x):
            out.update(_flat(v, f"{p}[{i}]"))
        return out if x else {p: []}
    return {p: x}


def _pat(path: str) -> str:
    path = re.sub(r"^files\[\d+\]", "files[*]", path)
    return re.sub(r"^(out_of_scope_snapshot_files\[\d+\])\..*$", r"\1", path)


def redescribe_diff(old: bytes, new: bytes, md: bool) -> tuple[dict, list[str]]:
    """The fixture's own diff: (changes in the note's shape, [texts-only faults])."""
    if md:
        a, b = old.decode("utf-8").splitlines(), new.decode("utf-8").splitlines()
        ca, cb = {}, {}
        for x in a:
            ca[x] = ca.get(x, 0) + 1
        for x in b:
            cb[x] = cb.get(x, 0) + 1
        gone = sum(max(0, n - cb.get(x, 0)) for x, n in ca.items())
        came = sum(max(0, n - ca.get(x, 0)) for x, n in cb.items())
        return {"lines_before": len(a), "lines_after": len(b), "lines_gone": gone, "lines_new": came}, []
    fa, fb = _flat(json.loads(old)), _flat(json.loads(new))
    out, faults = {}, []
    for kind, keys in (("changed", [k for k in fa if k in fb and fa[k] != fb[k]]),
                       ("added", [k for k in fb if k not in fa]),
                       ("removed", [k for k in fa if k not in fb])):
        cnt: dict[str, int] = {}
        for k in keys:
            cnt[_pat(k)] = cnt.get(_pat(k), 0) + 1
        out[kind] = dict(sorted(cnt.items()))
    for k in (k for k in fa if k in fb and fa[k] != fb[k]):
        if not (isinstance(fa[k], str) and isinstance(fb[k], str)):
            faults.append(f"{k}: {fa[k]!r} -> {fb[k]!r} is not a text change")
    faults += [f"{k}: removed" for k in fa if k not in fb]
    return out, faults


def clock_note_findings(note: dict, ctx: dict) -> list[str]:
    """Every field of FETCH_CLOCK_NOTE.json re-derived from the FILED records, one tag per group."""
    bad = []
    seal, pin, man, fb = ctx["seal"], ctx["pin"], ctx["man"], ctx["bytes"]
    fl = seal["fetch_log"]
    sealed = ctx["lines"][: fl["sealed_lines"]]
    sealed_sha = sha_of(("\n".join(sealed) + "\n").encode("utf-8"))
    if sealed_sha != fl["sha256_of_sealed_lines"]:
        bad.append("[note-log] the fetch log's sealed prefix moved")
    rows = [json.loads(x) for x in sealed]
    # [note-top]
    top = {"tier": "TIER-C11", "stage": "TC11-D", "seed": SEED, "as_of_last_closed_4h": PIN_ISO,
           "as_of_last_closed_4h_close_ms": PIN_MS}
    for k, v in top.items():
        if note.get(k) != v:
            bad.append(f"[note-top] {k}: the note files {note.get(k)!r}, not {v!r}")
    # [note-row] / [note-server-time]
    cc = note["fetch_time_clock_call"]
    n = cc["line"]
    row = rows[n - 1] if isinstance(n, int) and 1 <= n <= len(rows) else None
    clock_lines = [i + 1 for i, r in enumerate(rows) if r.get("phase") == "clock"]
    if (row is None or row != cc["row"] or clock_lines != [n] or row.get("endpoint") != "/fapi/v1/time"
            or row.get("status") != 200 or cc.get("fetch_log") != "research_outputs/tierc11/data/FETCH_LOG.jsonl"):
        bad.append(f"[note-row] the note cites line {n} of {cc.get('fetch_log')}; the sealed log's clock "
                   f"call(s) are at line(s) {clock_lines}")
    srv_filed = (row or {}).get("venue_server_time_ms")
    if (note["venue_server_time_ms_at_fetch_clock_call"] != srv_filed
            or cc["carries_venue_server_time"] != (srv_filed is not None)):
        bad.append(f"[note-server-time] the note's venue clock "
                   f"{note['venue_server_time_ms_at_fetch_clock_call']} is not what the filed row "
                   f"holds ({srv_filed})")
    # [note-latest]
    skew = int(pin["local_clock_skew_ms"])
    floors = set()
    for r in rows:                                  # 1 s wall clocks: the instant lies in [t, t + 999]
        t = ms_of(r["wall_clock_utc"])
        floors.update({(t - skew) // STEP["4h"] * STEP["4h"], (t + 999 - skew) // STEP["4h"] * STEP["4h"]})
    v = note["fetch_time_latest_closed_4h_close_ms"]
    d = note["derivation"]
    if (floors != {v} or note["fetch_time_latest_closed_4h"] != iso_of(v)
            or note["fetch_time_latest_equals_pin"] != (v == PIN_MS)
            or d["local_clock_skew_ms"] != skew
            or d["distinct_4h_floor_close_ms_over_every_sealed_row"] != sorted(floors)):
        bad.append(f"[note-latest] the note's fetch-time latest closed 4h {iso_of(v)} is not the 4h "
                   f"floor of every sealed row {[iso_of(x) for x in sorted(floors)]}")
    # [note-derivation]
    first, last = ms_of(rows[0]["wall_clock_utc"]), ms_of(rows[-1]["wall_clock_utc"])
    want = {"fetch_log_sealed_lines": len(sealed), "fetch_log_sha256_of_sealed_lines": sealed_sha,
            "first_row_utc": rows[0]["wall_clock_utc"], "last_row_utc": rows[-1]["wall_clock_utc"],
            "clock_row_utc": (row or {}).get("wall_clock_utc"),
            "seconds_after_the_pinned_close_at_the_first_row": (first - skew - PIN_MS) // 1000,
            "seconds_before_the_next_4h_close_at_the_last_row":
                (PIN_MS + STEP["4h"] - (last + 999 - skew)) // 1000}
    for k, x in want.items():
        if d.get(k) != x:
            bad.append(f"[note-derivation] {k}: the note files {d.get(k)!r}, the sealed log gives {x!r}")
    if (len(sealed) != fl["sealed_lines"] or fl["first_row_utc"] != want["first_row_utc"]
            or fl["last_row_utc"] != want["last_row_utc"]):
        bad.append("[note-derivation] the seal's line count / first / last row disagree with the log")
    # [note-pin-run]
    pr = note["pin_run_record"]
    vs = int(pin["venue_server_time_ms"])
    for k in ("venue_server_time_ms", "venue_server_time", "latest_closed_4h_at_pin_run",
              "latest_closed_4h_at_pin_run_close_ms", "pin_equals_latest_closed_at_pin_run"):
        if pr.get(k) != pin.get(k):
            bad.append(f"[note-pin-run] {k}: the note files {pr.get(k)!r}, AS_OF_PIN.json holds {pin.get(k)!r}")
    latest_at_pin = vs // STEP["4h"] * STEP["4h"]
    if not (iso_of(vs) == pr.get("venue_server_time")
            and latest_at_pin == pr.get("latest_closed_4h_at_pin_run_close_ms") == PIN_MS
            and pr.get("latest_closed_4h_at_pin_run") == iso_of(latest_at_pin)
            and pr.get("pin_equals_latest_closed_at_pin_run") is (latest_at_pin == PIN_MS)
            and pr.get("source") == "research_outputs/tierc11/data/AS_OF_PIN.json (write-once, sealed)"):
        bad.append(f"[note-pin-run] the venue clock {vs} floors to {iso_of(latest_at_pin)}; the note's "
                   "pin-run record does not say so")
    # [note-records]
    rec = note["records_not_rewritten_sha256"]
    want_rec = {"AS_OF_PIN.json": sha_of(fb["AS_OF_PIN.json"]),
                "WRITE_ONCE_SEAL.json": sha_of(fb["WRITE_ONCE_SEAL.json"]), "FETCH_LOG.jsonl": sealed_sha}
    for k in sorted(set(rec) | set(want_rec)):
        if rec.get(k) != want_rec.get(k):
            bad.append(f"[note-records] {k}: the note files {str(rec.get(k))[:16]}, the record is "
                       f"{str(want_rec.get(k))[:16]}")
    for k in ("AS_OF_PIN.json", "WRITE_ONCE_SEAL.json"):
        if k in seal["files"] and seal["files"][k]["sha256"] != want_rec[k]:
            bad.append(f"[note-records] {k} moved since the seal")
    # [note-corroboration]
    c = note["corroboration_stdout"]
    cap = fb[STDOUT_COPY]
    capl = cap.decode("utf-8").splitlines()
    ql = c.get("lines", {})
    ok = (c.get("filed_copy") == f"research_outputs/tierc11/data/{STDOUT_COPY}" and c.get("sha256") == sha_of(cap)
          and sorted(ql) == sorted(QUOTED)
          and all(capl[int(k) - 1] == ql[k] for k in ql if int(k) <= len(capl))
          and f"serverTime {pin['venue_server_time_ms']}" in ql.get("18", "")
          and f"closeTime of the bar {pin['venue_close_time_of_pinned_bar_ms']}" in ql.get("18", "")
          and "(== pin: True)" in ql.get("19", "") and pin["pin_equals_latest_closed_at_pin_run"] is True
          and f"+ {fl['sealed_lines']} fetch-log lines" in ql.get("155", ""))
    if not ok:
        bad.append(f"[note-corroboration] the quoted capture (sha {str(c.get('sha256'))[:16]}) is not the "
                   f"filed copy {STDOUT_COPY} (sha {sha_of(cap)[:16]}) line for line, or disagrees with "
                   "the filed records")
    # [note-relabel]
    rl = note["live_cache_touched_relabel"]
    if (rl["filed_value"] != man["live_cache_touched"] or rl["reading_of_record"] != RELABEL
            or rl.get("file") != "research_outputs/tierc11/data/STAGE_D_MANIFEST.json"
            or rl.get("key") != "live_cache_touched" or rl.get("basis_key") != "live_cache_touched_basis"
            or rl.get("basis_filed") != man.get("live_cache_touched_basis")
            or not str(man.get("live_cache_touched_basis", "")).startswith(RELABEL)):
        bad.append(f"[note-relabel] the note relabels {rl['filed_value']!r} as "
                   f"{rl['reading_of_record']!r}; the manifest holds {man['live_cache_touched']!r} with "
                   f"basis {str(man.get('live_cache_touched_basis'))[:40]!r}")
    # [note-erratum]
    er = note["l01_lean_erratum"]
    old_man = json.loads(ctx["blobs"]["STAGE_D_MANIFEST.json"])
    l01 = " ".join(x.strip(" -") for x in ctx["leans"][23:25])
    quote = "Every stage reads it, and the latest close at fetch time is printed beside it."
    if not (er.get("filed_at_build") == old_man["leans"][0] and er.get("filed_now") == man["leans"][0]
            and "the latest close at pin time is filed beside it" in old_man["leans"][0]
            and "the latest close at FETCH time is printed beside it" in man["leans"][0]
            and quote in l01 and f"'{quote}'" in er.get("reading", "")):
        bad.append("[note-erratum] the L-0.1 erratum does not quote LEANS.md:24-25, the lean filed at "
                   f"{BUILD_REV} and the lean filed now")
    # [note-redescribe]
    rd = note["manifest_redescribed"]
    for name in REDESCRIBED:
        old, new = ctx["blobs"][name], fb[name]
        f = rd["files"].get(name, {})
        got, faults = redescribe_diff(old, new, name.endswith(".md"))
        if (f.get("old_sha256") != sha_of(old) or f.get("new_sha256") != sha_of(new)
                or f.get("old_source") != f"git {BUILD_REV}:research_outputs/tierc11/data/{name}"):
            bad.append(f"[note-redescribe] {name}: the note's old/new sha is not git {BUILD_REV}'s / the "
                       "filed file's")
        if rd["changes"].get(name) != got:
            bad.append(f"[note-redescribe] {name}: the note's diff is not the diff "
                       f"({json.dumps(got, sort_keys=True)[:120]})")
        if faults:
            bad.append(f"[note-redescribe] {name}: a number moved: {faults[:2]}")
    # [note-provenance]
    if (json.dumps(note, indent=2, sort_keys=True) + "\n").encode("utf-8") != ctx["gen"]:
        bad.append("[note-provenance] the note is not what scripts/tierc11_data_clock_note.py builds "
                   "from the filed records")
    return bad


class _Resp:
    def __init__(self, ms: int):
        self._ms = ms

    def json(self) -> dict:
        return {"serverTime": self._ms}


def clock_row_findings(srv: int = SYNTH_SRV) -> list[str]:
    """record_fetch_clock under a STUBBED venue clock (no network): exactly one
    kind='clock' row carrying that clock and the latest closed 4h it implies."""
    pin = read_json(OUT / "AS_OF_PIN.json")

    def no_net(*a, **kw):
        raise AssertionError("record_fetch_clock reached the network")
    with tmpdir() as tmp, mutated(D.requests, "get", no_net), \
            mutated(D.ED, "_get", lambda url, params=None, retries=4: _Resp(srv)):
        D.record_fetch_clock(Path(tmp), pin)
        p = Path(tmp) / "FETCH_LOG.jsonl"
        rows = [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines()] if p.exists() else []
    clk = [r for r in rows if r.get("kind") == "clock"]
    want = srv // STEP["4h"] * STEP["4h"]
    if len(clk) != 1:
        return [f"[clock-row] {len(clk)} kind='clock' row(s) filed, not 1"]
    r, bad = clk[0], []
    if r.get("venue_server_time_ms") != srv:
        bad.append(f"[clock-row] the row's venue clock {r.get('venue_server_time_ms')} != {srv}")
    if r.get("latest_closed_4h_close_ms") != want or r.get("latest_closed_4h") != D.iso(want):
        bad.append(f"[clock-latest] the row files latest {r.get('latest_closed_4h')}, the venue clock "
                   f"{D.iso(srv)} implies {D.iso(want)}")
    if r.get("pinned_close_ms") != PIN_MS or r.get("latest_equals_pin") != (want == PIN_MS):
        bad.append("[clock-pin] the row does not carry the pin beside it")
    return bad


def fetch_clock_findings(src: str) -> list[str]:
    """Every call of run_fetch — and --all's seal — sits behind record_fetch_clock()."""
    tree = ast.parse(src)
    par = _parents(tree)
    bad, n = [], 0
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        who, fn = _callee(node), _owner(node, par)
        if who == "run_fetch" or (who == "seal_provenance" and fn == "run_all"):
            n += 1
            if not behind(node, "record_fetch_clock", par):
                bad.append(f"[fetch-clock-order] {fn}: {who} is not behind record_fetch_clock() "
                           f"on every path")
    if n == 0:
        bad.append("[fetch-clock-order] no run_fetch call found")
    return bad


def clock_break():
    note = read_json(OUT / CLOCK_NOTE)
    ctx = clock_ctx()
    src = module_src()

    def note_with(path: tuple, value):
        def t():
            x = json.loads(json.dumps(note))
            d = x
            for key in path[:-1]:
                d = d[key]
            d[path[-1]] = value
            return clock_note_findings(x, ctx)
        return t

    def no_log():
        with mutated(D, "_fetch_log", lambda out, row: None):
            return clock_row_findings()

    def one_hour_grid():
        with mutated(D, "MS_4H", STEP["1h"]):
            return clock_row_findings()
    no_all = src_edit(src, "    srv, latest = record_fetch_clock(OUT, pin)          "
                           "# filed BEFORE the fetch and the seal\n", "")
    no_fetch = src_edit(src, "        record_fetch_clock(OUT, pin)                    "
                             "# [L-0.1] the latest close AT FETCH TIME\n", "")
    mc = note["manifest_redescribed"]["changes"]["STAGE_D_MANIFEST.json"]
    fewer = {k: v for k, v in mc["changed"].items() if k != "leans[15]"}
    return plants([
        ("a note claiming 04:00Z as the fetch-time latest closed 4h", "[note-latest]",
         note_with(("fetch_time_latest_closed_4h_close_ms",), PIN_MS + STEP["4h"])),
        ("a note citing line 4 (not a clock row) as the clock call", "[note-row]",
         note_with(("fetch_time_clock_call", "line"), 4)),
        ("a note with an INVENTED venue clock for the fetch-time call", "[note-server-time]",
         note_with(("venue_server_time_ms_at_fetch_clock_call",), 1_790_297_867_000)),
        ("a note filing another seed", "[note-top]", note_with(("seed",), 1)),
        ("a note whose first-row margin is the non-conservative 3466 s", "[note-derivation]",
         note_with(("derivation", "seconds_after_the_pinned_close_at_the_first_row"), 3466)),
        ("a note whose pin-run venue clock is 1 s late", "[note-pin-run]",
         note_with(("pin_run_record", "venue_server_time_ms"), 1_790_297_867_708)),
        ("a note whose FETCH_LOG sha is not the sealed prefix's", "[note-records]",
         note_with(("records_not_rewritten_sha256", "FETCH_LOG.jsonl"), "0" * 64)),
        ("a note whose capture sha is not the filed copy's", "[note-corroboration]",
         note_with(("corroboration_stdout", "sha256"), "0" * 64)),
        ("a note relabelling a filed True", "[note-relabel]",
         note_with(("live_cache_touched_relabel", "filed_value"), True)),
        ("a note claiming the build filed today's L-0.1 lean", "[note-erratum]",
         note_with(("l01_lean_erratum", "filed_at_build"), ctx["man"]["leans"][0])),
        ("a note whose re-describe diff omits leans[15]", "[note-redescribe]",
         note_with(("manifest_redescribed", "changes", "STAGE_D_MANIFEST.json", "changed"), fewer)),
        ("a note whose prose differs from the repo generator's (one word)", "[note-provenance]",
         note_with(("law",), note["law"] + " (edited)")),
        ("the module's _fetch_log silenced: record_fetch_clock files nothing", "[clock-row]", no_log),
        ("the module's 4h step set to 1h: the filed latest is the 1h floor", "[clock-latest]",
         one_hour_grid),
        ("run_all without its record_fetch_clock call (source copy)",
         "[fetch-clock-order] run_all: run_fetch", lambda: fetch_clock_findings(no_all)),
        ("main --fetch without its record_fetch_clock call (source copy)",
         "[fetch-clock-order] main: run_fetch", lambda: fetch_clock_findings(no_fetch))])


def clock_real():
    note = read_json(OUT / CLOCK_NOTE)
    ctx = clock_ctx()
    bad = clock_note_findings(note, ctx)
    if (OUT / CLOCK_NOTE).read_bytes() != ctx["gen"]:
        bad.append("[note-provenance] the filed note's BYTES are not build_note()'s")
    bad += clock_row_findings()
    bad += fetch_clock_findings(module_src())
    seal = ctx["seal"]
    rows = [json.loads(x) for x in ctx["lines"][: seal["fetch_log"]["sealed_lines"]]]
    n_kind_clock = sum(1 for r in rows if r.get("kind") == "clock")
    cc, d = note["fetch_time_clock_call"], note["derivation"]
    ch = note["manifest_redescribed"]["changes"]
    return (not bad), (f"FETCH_CLOCK_NOTE.json re-derived field by field from the filed records: the "
                       f"sealed log's one clock call (line {cc['line']}, GET /fapi/v1/time, "
                       f"{cc['row']['wall_clock_utc']}) carries no serverTime and the note files null for "
                       f"it (never invented); all {len(rows)} sealed rows floor to the 4h close "
                       f"{note['fetch_time_latest_closed_4h']} == the note == the pin, margins "
                       f"{d['seconds_after_the_pinned_close_at_the_first_row']} s / "
                       f"{d['seconds_before_the_next_4h_close_at_the_last_row']} s (conservative); "
                       f"{n_kind_clock} kind='clock' rows in the sealed log (the old code filed none); the "
                       f"pin-run record == AS_OF_PIN.json; the record shas (FETCH_LOG = its sealed "
                       f"prefix) hold; the {len(note['corroboration_stdout']['lines'])} quoted lines are "
                       f"the filed capture's ({STDOUT_COPY}); relabel {RELABEL!r} == the manifest's "
                       f"live_cache_touched_basis over the filed {ctx['man']['live_cache_touched']!r}; the "
                       f"L-0.1 erratum quotes LEANS.md:24-25; the re-describe diff vs git {BUILD_REV} is "
                       f"texts only (manifest changed {sorted(ch['STAGE_D_MANIFEST.json']['changed'])}, "
                       f"fee_schedule {sorted(ch['fee_schedule.json']['changed'])}, the rest ADDED); the "
                       f"filed bytes == scripts/tierc11_data_clock_note.py's build; record_fetch_clock "
                       f"under a stubbed venue clock {iso_of(SYNTH_SRV)} (no network) files one "
                       f"kind='clock' row with the clock and the latest closed 4h "
                       f"{iso_of(SYNTH_SRV // STEP['4h'] * STEP['4h'])}; run_all and main --fetch call it "
                       f"before run_fetch, and run_all before its seal"
                       if not bad else f"{len(bad)} fault(s): {bad[:3]}")


# ═══════════════════════════════════════════════ F-D11-PREFIX
def prefix_break():
    pre = read_json(OUT / "PRE_STATE.json")
    rel = "klines/BTCUSDT_12h.parquet"
    one = {"files": {rel: pre["files"][rel]}}
    f = pd.read_parquet(D.SNAPSHOT / rel).sort_values("open_time").reset_index(drop=True)
    with tmpdir() as tmp:
        t = Path(tmp)
        g = f.copy()
        g.loc[1000, "high"] = g.loc[1000, "high"] + 0.01
        frame_copy(g, t / "edit", rel)
        frame_copy(f.drop(index=2000), t / "drop", rel)
        ins = pd.concat([f, f.iloc[[3000]].assign(open_time=f.loc[3000, "open_time"] + 1)])
        frame_copy(ins.sort_values("open_time"), t / "ins", rel)

        def run(sub):
            return [r["why"] for r in D.verify_prefixes(one, t / sub) if not r["ok"]]
        return plants([
            ("a historical 12h high moved by 0.01 in a temp copy", "old-prefix content sha moved",
             lambda: run("edit")),
            ("a historical 12h row deleted in a temp copy", "old-prefix content sha moved",
             lambda: run("drop")),
            ("a row inserted behind the edge in a temp copy", "old-prefix content sha moved",
             lambda: run("ins"))])


def prefix_real():
    pre = read_json(OUT / "PRE_STATE.json")
    rows = D.verify_prefixes(pre)
    bad = [r["file"] for r in rows if not r["ok"]]
    ext = sum(1 for r in rows if r["extended_by"])
    untouched = sum(1 for r in rows if r["untouched_file"])
    ok = not bad and len(rows) == 124 == len(pre["files"])
    return ok, (f"{len(rows)}/{len(pre['files'])} PRE_STATE files (which files: F-D11-SCOPE): every old "
                f"row byte-identical ({sum(r['old_rows'] for r in rows)} rows); {ext} extended "
                f"(+{sum(r['extended_by'] for r in rows)} rows), {untouched} untouched byte for byte"
                if ok else f"{len(bad)} prefix(es) moved: {bad[:3]}")


# ═══════════════════════════════════════════════ F-D11-EDGE  [TC11-D_VERIFY 6, 7]
def expected_last_open(iv: str) -> int:
    s, a = STEP[iv], (MONDAY if iv == "1w" else 0)
    x = PIN_MS - s
    return x - ((x - a) % s)


def edge_findings(root: Path, rel: str) -> list[str]:
    iv = rel[: -len(".parquet")].rpartition("_")[2]
    step, anchor = STEP[iv], (MONDAY if iv == "1w" else 0)
    t = np.sort(pd.read_parquet(root / rel, columns=["open_time"])["open_time"].to_numpy(np.int64))
    bad, want = [], expected_last_open(iv)
    if t[-1] != want:
        bad.append(f"[last-open] {rel}: last open {D.iso(t[-1])} != the lens's last bar closing <= "
                   f"the pin {D.iso(want)}")
    d = np.diff(t)
    if (d > step).any():
        bad.append(f"[gap] {rel}: {int((d > step).sum())} gap(s)")
    if (d <= 0).any():
        bad.append(f"[dup] {rel}: {int((d <= 0).sum())} duplicate/backward stamp(s)")
    if ((t - anchor) % step != 0).any():
        bad.append(f"[off-grid] {rel}: {int(((t - anchor) % step != 0).sum())} stamp(s) off the {iv} grid")
    if (t + step > PIN_MS).any():
        bad.append(f"[past-pin] {rel}: {int((t + step > PIN_MS).sum())} row(s) past the pin")
    return bad


def funding_edge_findings(root: Path, stem: str) -> list[str]:
    rel = f"funding/{stem}.parquet"
    t = np.sort(pd.read_parquet(root / rel, columns=["funding_time"])["funding_time"].to_numpy(np.int64))
    bad = []
    past = int((t > PIN_MS + FUNDING_JITTER).sum())
    if past:
        bad.append(f"[funding-past-pin] {rel}: {past} print(s) past the pin + 60 s")
    known = t[t <= PIN_MS + FUNDING_JITTER]
    if not len(known) or int(known[-1]) // HOUR * HOUR != PIN_MS:
        bad.append(f"[funding-hour] {rel}: the last print at the pin "
                   f"{D.iso(int(known[-1])) if len(known) else None} is not in the pin's hour {PIN_ISO}")
    if len(np.unique(t)) != len(t):
        bad.append(f"[funding-dup] {rel}: {len(t) - len(np.unique(t))} repeated print(s)")
    cov = D.funding_coverage(stem, PIN_MS, root)
    if not cov["ok"]:
        bad.append(f"[funding-coverage] {rel}: {cov['why']}")
    return bad


def manifest_row_findings(row: dict | None, root: Path, rel: str) -> list[str]:
    if row is None or row.get("sha256") != D.file_sha256(root / rel):
        return [f"[manifest-sha] {rel}: the manifest does not describe this file's bytes"]
    if rel.startswith("klines/") and not (row["gap_count"] == 0 and row["complete_to_as_of"]
                                          and row["last_bar_close_equals_lens_last_closed_at_pin"]):
        return [f"[manifest-flags] {rel}: the manifest row disagrees (gaps/complete/edge)"]
    col, cols = colset(rel)
    if row.get("content_sha") != content_hash(pd.read_parquet(root / rel).sort_values(col), cols):
        return [f"[manifest-content-sha] {rel}: the manifest's content_sha is not this file's rows"]
    return []


def edge_break():
    rel, stem = "klines/BTCUSDT_4h.parquet", "BTCUSDT"
    frel = f"funding/{stem}.parquet"
    f = pd.read_parquet(D.SNAPSHOT / rel).sort_values("open_time").reset_index(drop=True)
    fu = pd.read_parquet(D.SNAPSHOT / frel).sort_values("funding_time").reset_index(drop=True)
    row = {r["path"]: r for r in read_json(OUT / "STAGE_D_MANIFEST.json")["files"]}[rel]
    with tmpdir() as tmp:
        t = Path(tmp)
        mid = len(f) // 2
        frame_copy(f.drop(index=mid), t / "mid", rel)
        frame_copy(f.iloc[:-1], t / "last", rel)
        nxt = f.iloc[[-1]].assign(open_time=int(f["open_time"].iloc[-1]) + STEP["4h"])
        frame_copy(pd.concat([f, nxt]), t / "past", rel)
        frame_copy(pd.concat([f, f.iloc[[mid]]]).sort_values("open_time"), t / "dup", rel)
        half = f.iloc[[mid]].assign(open_time=int(f.loc[mid, "open_time"]) + STEP["4h"] // 2)
        frame_copy(pd.concat([f, half]).sort_values("open_time"), t / "grid", rel)
        ft = fu["funding_time"]
        frame_copy(fu[ft < PIN_MS], t / "fhour", frel)
        frame_copy(fu[ft <= PIN_MS - 3 * DAY], t / "fcov", frel)
        late = fu.iloc[[-1]].assign(funding_time=PIN_MS + 8 * HOUR)
        frame_copy(pd.concat([fu, late]), t / "fpast", frel)
        frame_copy(pd.concat([fu, fu.iloc[[len(fu) // 2]]]).sort_values("funding_time"), t / "fdup", frel)
        return plants([
            ("a dropped middle 4h bar", "[gap]", lambda: edge_findings(t / "mid", rel)),
            ("a dropped last 4h bar", "[last-open]", lambda: edge_findings(t / "last", rel)),
            ("a 4h bar appended past the pin", "[past-pin]", lambda: edge_findings(t / "past", rel)),
            ("a repeated 4h bar", "[dup]", lambda: edge_findings(t / "dup", rel)),
            ("a 4h bar stamped half a step off the grid", "[off-grid]",
             lambda: edge_findings(t / "grid", rel)),
            ("a manifest row copy whose sha is not the file's", "[manifest-sha]",
             lambda: manifest_row_findings(dict(row, sha256="0" * 64), D.SNAPSHOT, rel)),
            ("a manifest row copy that says incomplete", "[manifest-flags]",
             lambda: manifest_row_findings(dict(row, complete_to_as_of=False), D.SNAPSHOT, rel)),
            ("a manifest row copy whose content_sha is not the file's rows", "[manifest-content-sha]",
             lambda: manifest_row_findings(dict(row, content_sha="0" * 64), D.SNAPSHOT, rel)),
            ("a BTCUSDT funding copy without its 00:00Z print", "[funding-hour]",
             lambda: funding_edge_findings(t / "fhour", stem)),
            ("a BTCUSDT funding copy stopped 3 days short", "[funding-coverage]",
             lambda: funding_edge_findings(t / "fcov", stem)),
            ("a BTCUSDT funding copy with a print at the pin + 8h", "[funding-past-pin]",
             lambda: funding_edge_findings(t / "fpast", stem)),
            ("a BTCUSDT funding copy with one print repeated", "[funding-dup]",
             lambda: funding_edge_findings(t / "fdup", stem))])


def edge_real():
    rows = {r["path"]: r for r in read_json(OUT / "STAGE_D_MANIFEST.json")["files"]}
    bad, n_k, n_f = [], 0, 0             # the loop is the fixture's typed scope (F-D11-SCOPE ties it
    #                                      to the module's, PRE_STATE's and the manifest's)
    for rel in TYPED_SCOPE:
        bad += manifest_row_findings(rows.get(rel), D.SNAPSHOT, rel)
        if rel.startswith("klines/"):
            n_k += 1
            bad += edge_findings(D.SNAPSHOT, rel)
        else:
            n_f += 1
            bad += funding_edge_findings(D.SNAPSHOT, rel[len("funding/"):-len(".parquet")])
    lens = [iv for iv in STEP if any(r.endswith(f"_{iv}.parquet") for r in TYPED_SCOPE)]
    return (not bad), (f"{n_k} typed kline files ({', '.join(lens)}) each end exactly at their lens's "
                       f"last bar closing <= {PIN_ISO}: zero gaps, duplicates, off-grid stamps and rows "
                       f"past the pin; {n_f} typed funding tapes carry the {PIN_ISO} print, pass coverage, "
                       f"repeat no print and hold none past the pin + 60 s; the manifest's sha, flags "
                       f"and parquet content sha (re-hashed here) describe every file"
                       if not bad else f"{len(bad)} fault(s): {bad[:3]}")


# ═══════════════════════════════════════════════ F-D11-DERIVE
def kahan(vals) -> float:
    """pandas' groupby sum is COMPENSATED (Kahan); a naive left-to-right sum
    differs from it in the last bit on hundreds of BTC days (F-D11-DERIVE's
    naive plant prints the count) — so the plain loop states the compensated
    sum explicitly."""
    s = c = 0.0
    for v in vals:
        y = v - c
        t = s + y
        c = (t - s) - y
        s = t
    return s


def plain_derive(stem: str, naive: bool = False) -> tuple[np.ndarray, np.ndarray]:
    f = pd.read_parquet(D.SNAPSHOT / "klines" / f"{stem}_4h.parquet").sort_values("open_time")
    t = f["open_time"].to_numpy(np.int64)
    o, h, l, c, v = (f[k].to_numpy(np.float64) for k in ("open", "high", "low", "close", "volume"))
    days: dict[int, list[int]] = {}
    for i in range(len(t)):
        if int(t[i]) + STEP["4h"] <= PIN_MS:
            days.setdefault(int(t[i]) // DAY, []).append(i)
    add = (lambda xs: sum(xs, 0.0)) if naive else kahan
    d1 = []
    for dk in sorted(days):
        ix = days[dk]
        if len(ix) == 6:
            d1.append((dk * DAY, o[ix[0]], max(h[j] for j in ix), min(l[j] for j in ix),
                       c[ix[-1]], add([v[j] for j in ix])))
    weeks: dict[int, list[tuple]] = {}
    for r in d1:
        weeks.setdefault((r[0] - MONDAY) // WEEK, []).append(r)
    w1 = []
    for wk in sorted(weeks):
        rs = weeks[wk]
        if len(rs) == 7:
            w1.append((wk * WEEK + MONDAY, rs[0][1], max(r[2] for r in rs), min(r[3] for r in rs),
                       rs[-1][4], add([r[5] for r in rs])))
    return np.array(d1, dtype=object), np.array(w1, dtype=object)


def same_frame(df: pd.DataFrame, ref: np.ndarray) -> bool:
    if len(df) != len(ref):
        return False
    if not len(df):
        return True
    if not np.array_equal(df["open_time"].to_numpy(np.int64), ref[:, 0].astype(np.int64)):
        return False
    return all(np.array_equal(df[k].to_numpy(np.float64), ref[:, i].astype(np.float64))
               for i, k in enumerate(("open", "high", "low", "close", "volume"), 1))


def first_diff(df: pd.DataFrame, ref: np.ndarray) -> str:
    """Where a frame and the plain loop's rows part: row counts, or the first
    differing column and stamp (and how many rows differ)."""
    if len(df) != len(ref):
        return f"{len(df)} rows vs the plain loop's {len(ref)}"
    cols = ("open_time", "open", "high", "low", "close", "volume")
    rows = np.zeros(len(df), dtype=bool)
    first = None
    for i, k in enumerate(cols):
        a = df[k].to_numpy(np.int64 if i == 0 else np.float64)
        b = ref[:, i].astype(np.int64 if i == 0 else np.float64)
        ne = a != b
        if ne.any() and first is None:
            first = (k, int(ref[int(np.argmax(ne)), 0]))
        rows |= ne
    return (f"{int(rows.sum())} of {len(df)} rows differ, first in {first[0]} at {D.iso(first[1])}"
            if first else "identical")


def derive_findings(stem: str, d1: pd.DataFrame, w1: pd.DataFrame, ref=None) -> list[str]:
    d1_ref, w1_ref = ref if ref is not None else plain_derive(stem)
    bad = []
    if not same_frame(d1, d1_ref):
        bad.append(f"[1d] {stem}: the 1d frame != the plain loop: {first_diff(d1, d1_ref)}")
    if not same_frame(w1, w1_ref):
        bad.append(f"[1w] {stem}: the 1w frame != the plain loop: {first_diff(w1, w1_ref)}")
    return bad


KCOLS = ["open_time", "open", "high", "low", "close", "volume"]


def ref_frame(ref: np.ndarray) -> pd.DataFrame:
    return pd.DataFrame({k: (ref[:, i].astype(np.int64) if i == 0 else ref[:, i].astype(np.float64))
                         for i, k in enumerate(KCOLS)})


def derivation_sha_findings(stem: str, ref, rows: dict) -> list[str]:
    """The manifest's derivation_content_sha AND content_sha of each derived file == the fixture's
    own hash of the plain loop's frame."""
    bad = []
    for iv, r in zip(("1d", "1w"), ref):
        want = content_hash(ref_frame(r), KCOLS)
        row = rows.get(f"klines/{stem}_{iv}.parquet", {})
        if row.get("derivation_content_sha") != want or row.get("content_sha") != want:
            bad.append(f"[derivation-sha] {stem} {iv}: the manifest's derivation/content sha "
                       f"{str(row.get('derivation_content_sha'))[:12]}/{str(row.get('content_sha'))[:12]} "
                       f"!= the plain loop's {want[:12]}")
    return bad


def _derived(stem: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    return tuple(pd.read_parquet(D.SNAPSHOT / "klines" / f"{stem}_{iv}.parquet")
                 .sort_values("open_time").reset_index(drop=True) for iv in ("1d", "1w"))


def derive_break():
    stem = "BTCUSDT"
    d1_file, w1_file = _derived(stem)
    ref = plain_derive(stem)
    naive = plain_derive(stem, naive=True)

    def sunday():
        with mutated(D, "MONDAY_EPOCH_OFFSET_MS", 3 * DAY):           # a SUNDAY anchor
            w_bad, _ = D.derive_1w(d1_file)
        return derive_findings(stem, d1_file, w_bad, ref)

    def one_ulp():
        g = d1_file.copy()
        g.loc[500, "volume"] = np.nextafter(g.loc[500, "volume"], np.inf)
        return derive_findings(stem, g, w1_file, ref)
    rows = {r["path"]: r for r in read_json(OUT / "STAGE_D_MANIFEST.json")["files"]}
    bad_rows = dict(rows)
    bad_rows["klines/BTCUSDT_1w.parquet"] = dict(rows["klines/BTCUSDT_1w.parquet"],
                                                 derivation_content_sha="0" * 64)
    return plants([
        ("the module's derive_1w with the week anchor shifted to Sunday", "[1w]", sunday),
        ("a manifest copy whose BTCUSDT 1w derivation_content_sha is off", "[derivation-sha] BTCUSDT 1w",
         lambda: derivation_sha_findings(stem, ref, bad_rows)),
        ("a copy of the 1d file with one volume moved by one ulp", "[1d]", one_ulp),
        ("the plain loop's volume summed naively (uncompensated): the identity is to the bit",
         "[1d]", lambda: derive_findings(stem, d1_file, w1_file, naive))])


def derive_real():
    bad, n_d, n_w = [], 0, 0
    rows = {r["path"]: r for r in read_json(OUT / "STAGE_D_MANIFEST.json")["files"]}
    for stem in TYPED_PANEL17:
        d1, w1 = _derived(stem)
        ref = plain_derive(stem)
        bad += derive_findings(stem, d1, w1, ref)
        bad += derivation_sha_findings(stem, ref, rows)
        n_d += len(d1)
        n_w += len(w1)
    return (not bad), (f"{len(TYPED_PANEL17)} typed assets: {n_d} days and {n_w} Monday-anchored weeks "
                       f"re-derived by a plain loop from native 4h (bars closed <= {PIN_ISO}) equal "
                       f"the derived files bit for bit on all six columns; the manifest's "
                       f"{2 * len(TYPED_PANEL17)} derivation_content_sha and content_sha of the derived "
                       f"files == the plain loop's frames hashed here"
                       if not bad else f"{len(bad)} mismatch(es): {bad[:4]}")


# ═══════════════════════════════════════════════ F-DET  [TC11-D_VERIFY 1]
def det_runs() -> dict:
    procs = {}
    for s in DET_SEEDS:
        d = RUN_ROOT / "_det_data" / f"seed_{s}"
        if d.exists():
            shutil.rmtree(d)
        env = dict(os.environ, PYTHONHASHSEED=str(s), PYTHONDONTWRITEBYTECODE="1",
                   NAIAD_CACHE_DIR=str(D.SNAPSHOT))
        procs[s] = (d, subprocess.Popen(
            [sys.executable, "-B", str(ROOT / "scripts" / "tierc11_data.py"), "--manifest",
             "--out", str(d)], env=env, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True))
    outs = {}
    for s, (d, p) in procs.items():
        _, err = p.communicate(timeout=3600)
        if p.returncode:
            clock(f"F-DET seed {s} stderr tail: {err[-300:]}")
        outs[s] = (p.returncode, {q.name: q.read_bytes() for q in sorted(d.iterdir()) if q.is_file()}
                   if d.exists() else {})
    return outs


N_CONTENT, N_DERIV = len(TYPED_SCOPE), 2 * len(TYPED_PANEL17)     # 124 files, 34 derivations


def content_shas(files: dict) -> dict:
    """{(path, key): sha} — every parquet content sha a build's manifest carries [L-F.1]."""
    b = files.get("STAGE_D_MANIFEST.json")
    if b is None:
        return {}
    try:
        m = json.loads(b)
    except ValueError:
        return {}
    return {(f["path"], k): f[k] for f in m.get("files", [])
            for k in ("content_sha", "derivation_content_sha") if f.get(k)}


def det_findings(outs: dict, filed: dict) -> list[str]:
    """outs: seed -> (exit code, {file name: bytes}); filed: name -> the filed bytes."""
    a, b = DET_SEEDS
    bad = []
    cs = {s: content_shas(outs[s][1]) for s in DET_SEEDS}
    cf = content_shas(filed)
    for s in DET_SEEDS:
        n1 = sum(1 for k in cs[s] if k[1] == "content_sha")
        n2 = sum(1 for k in cs[s] if k[1] == "derivation_content_sha")
        if (n1, n2) != (N_CONTENT, N_DERIV):
            bad.append(f"[content-sha] the PYTHONHASHSEED={s} build carries {n1} file and {n2} derivation "
                       f"content shas, not {N_CONTENT} and {N_DERIV}")
    dd = sorted(k for k in set(cs[a]) | set(cs[b]) if cs[a].get(k) != cs[b].get(k))
    if dd:
        bad.append(f"[content-sha] {len(dd)} parquet content sha(s) differ between the builds, first "
                   f"{dd[0][0]} {dd[0][1]}")
    df_ = sorted(k for k in set(cs[a]) | set(cf) if cs[a].get(k) != cf.get(k))
    if df_ and not dd:
        bad.append(f"[content-sha] {len(df_)} parquet content sha(s) of the builds differ from the filed "
                   f"manifest's, first {df_[0][0]} {df_[0][1]}")
    for s in DET_SEEDS:
        rc, files = outs[s]
        if rc != 0:
            bad.append(f"[exit] the PYTHONHASHSEED={s} build exited {rc}")
        if set(files) != set(DET_FILES):
            bad.append(f"[file-set] the PYTHONHASHSEED={s} build holds {sorted(files)}, not "
                       f"{sorted(DET_FILES)}")
    for n in DET_FILES:
        x, y = outs[a][1].get(n), outs[b][1].get(n)
        if x is None or y is None:
            bad.append(f"[absent] {n} missing from the build(s) under PYTHONHASHSEED "
                       f"{[s for s, v in ((a, x), (b, y)) if v is None]}")
            continue
        if x != y:
            bad.append(f"[twins-differ] {n}: the PYTHONHASHSEED {a} and {b} builds differ")
        elif x != filed[n]:
            bad.append(f"[not-filed-bytes] {n}: the builds agree but differ from the filed bytes")
        if n.endswith(".json"):
            for who, blob in (("filed", filed[n]), (f"seed {a}", x), (f"seed {b}", y)):
                m = CLOCK_FIELD.findall(blob.decode("utf-8", "replace"))
                if m:
                    bad.append(f"[clock-field] {n} ({who}) carries clock field(s) {sorted(set(m))}")
    return bad


def det_break():
    filed = {n: (OUT / n).read_bytes() for n in DET_FILES}
    man = filed["STAGE_D_MANIFEST.json"]
    anchor = b'"seed": 20260924'
    if man.count(anchor) != 1:
        raise AssertionError("plant anchor '\"seed\": 20260924' not found once in the manifest")
    salted = man.replace(anchor, anchor + b', "salt": 4242', 1)
    clocked = man.replace(anchor, anchor + b', "wall_clock_utc": "x"', 1)
    a, b = DET_SEEDS
    with_clock = dict(filed, **{"STAGE_D_MANIFEST.json": clocked})
    no_fee = {k: v for k, v in filed.items() if k != "fee_schedule.json"}
    mj = json.loads(man)
    mj["files"][0]["content_sha"] = "0" * 64
    one_sha = (json.dumps(mj, indent=2, sort_keys=True, default=str) + "\n").encode("utf-8")
    for f in mj["files"]:
        f.pop("content_sha", None)
        f.pop("derivation_content_sha", None)
    stripped = (json.dumps(mj, indent=2, sort_keys=True, default=str) + "\n").encode("utf-8")
    return plants([
        ("one build with one parquet content sha altered", "[content-sha] 1 parquet content sha(s) "
         "differ between the builds",
         lambda: det_findings({a: (0, dict(filed)), b: (0, dict(filed, **{"STAGE_D_MANIFEST.json": one_sha}))},
                              filed)),
        ("both builds without parquet content shas (the keys stripped alike)", "[content-sha] the "
         "PYTHONHASHSEED=1 build carries 0 file and 0 derivation content shas",
         lambda: det_findings({s: (0, dict(filed, **{"STAGE_D_MANIFEST.json": stripped}))
                               for s in DET_SEEDS}, filed)),
        ("one build salted", "[twins-differ]",
         lambda: det_findings({a: (0, dict(filed)),
                               b: (0, dict(filed, **{"STAGE_D_MANIFEST.json": salted}))}, filed)),
        ("both builds salted alike (equal to each other, not to the filed bytes)", "[not-filed-bytes]",
         lambda: det_findings({s: (0, dict(filed, **{"STAGE_D_MANIFEST.json": salted}))
                               for s in DET_SEEDS}, filed)),
        ("one build exits 1", "[exit]",
         lambda: det_findings({a: (1, dict(filed)), b: (0, dict(filed))}, filed)),
        ("one build missing fee_schedule.json", "[absent]",
         lambda: det_findings({a: (0, dict(filed)), b: (0, no_fee)}, filed)),
        ("one build with an extra file", "[file-set]",
         lambda: det_findings({a: (0, dict(filed, **{"STAGE_D_MANIFEST.json.tmp": b"{}"})),
                               b: (0, dict(filed))}, filed)),
        ("a clock field in the filed manifest and both builds alike", "[clock-field]",
         lambda: det_findings({s: (0, dict(with_clock)) for s in DET_SEEDS}, with_clock))])


def det_real():
    o = det_runs()
    filed = {n: (OUT / n).read_bytes() for n in DET_FILES}
    bad = det_findings(o, filed)
    shas = " · ".join(f"{n} {hashlib.sha256(filed[n]).hexdigest()[:16]}…" for n in DET_FILES)
    a, b = DET_SEEDS
    return (not bad), (f"exit {o[a][0]}/{o[b][0]}; each build holds exactly the {len(DET_FILES)} files; "
                       f"byte-identical under PYTHONHASHSEED {a} and {b} and == the filed bytes ({shas}); "
                       f"no clock field; the {N_CONTENT} file and {N_DERIV} derivation parquet content "
                       f"shas equal across the builds and the filed manifest"
                       if not bad else f"{len(bad)} fault(s): {bad[:3]}")


# ═══════════════════════════════════════════════ F-D11-UNTOUCHED  [TC11-D_VERIFY 3]
def live_stat() -> tuple:
    st = os.stat(LIVE_MANIFEST)                      # metadata only; the file is never opened
    return (st.st_size, st.st_mtime_ns, st.st_ino)


LIVE_STAT_AT_START: tuple | None = None


def untouched_findings(root: Path, rels: list[str], exp: dict, ref: dict) -> list[str]:
    bad = []
    for rel in rels:
        want = exp.get(rel) or ref.get(rel)
        if D.file_sha256(root / rel) != want:
            bad.append(f"[tc10-bytes] {rel}: the TC10 snapshot's bytes moved")
    return bad


def stat_findings(a: tuple, b: tuple) -> list[str]:
    moved = [k for k, x, y in zip(("size", "mtime_ns", "inode"), a, b) if x != y]
    return ([f"[live-stat] the live cache MANIFEST.json stat moved across this fixture run "
             f"({', '.join(moved)}) — by any process; not attributable to TC11"] if moved else [])


def tc10_seal_findings(root: Path | None = None) -> list[str]:
    return [f"[tc10-seal] {x}" for x in D.verify_seal(D.TC10_DATA, root)]


def untouched_break():
    exp = tc10_expected()
    rel = sorted(exp, key=lambda r: (D.TC10_SNAPSHOT / r).stat().st_size)[0]
    s0 = LIVE_STAT_AT_START or live_stat()
    seal = read_json(D.TC10_DATA / D.SEAL)
    with tmpdir() as tmp:
        t = Path(tmp)
        flip_byte_copy(D.TC10_SNAPSHOT / rel, t / "snap", rel)
        rec = t / "rec"
        rec.mkdir()
        for n in list(seal["files"]) + [seal["fetch_log"]["file"]]:
            shutil.copyfile(D.TC10_DATA / n, rec / n)
        victim = sorted(seal["files"])[0]
        flip_byte_copy(D.TC10_DATA / victim, rec, victim)
        return plants([
            (f"a flipped byte in a temp copy of TC10's {rel}", "[tc10-bytes]",
             lambda: untouched_findings(t / "snap", [rel], exp, {})),
            (f"a flipped byte in a temp copy of TC10's sealed {victim}", "bytes moved since the seal",
             lambda: tc10_seal_findings(rec)),
            ("a live-cache stat whose mtime moved by 1 ns", "[live-stat]",
             lambda: stat_findings(s0, (s0[0], s0[1] + 1, s0[2])))])


def untouched_real():
    exp = tc10_expected()
    att = read_json(OUT / D.CLONE_ATTEST)
    ref = {r: v["reference_sha256"] for r, v in att["files"].items() if r not in exp}
    have = tree(D.TC10_SNAPSHOT)
    bad = []
    if set(have) != set(exp) | set(ref):
        bad.append("the TC10 snapshot's file set moved")
    bad += untouched_findings(D.TC10_SNAPSHOT, have, exp, ref)
    bad += tc10_seal_findings()
    s1 = live_stat()
    bad += stat_findings(LIVE_STAT_AT_START, s1)
    return (not bad), (f"{len(have)} TC10 snapshot files re-hash to TC10's manifest "
                       f"({len(exp)}) / the clone-time record ({len(ref)}); TC10's WRITE_ONCE_SEAL "
                       f"verifies; the live cache MANIFEST.json stat (size, mtime_ns, inode) held "
                       f"across THIS FIXTURE RUN ONLY (stat only, never opened) — the build's "
                       f"live-cache claim is by construction (F-D11-GUARD + F-D11-BOUND)"
                       if not bad else f"{len(bad)} fault(s): {bad[:3]}")


# ═══════════════════════════════════════════════ F-D11-OUT  [round 2: defect 3]
def out_guard_order_findings(src: str) -> list[str]:
    """Every write of write_manifest (a write primitive, _dump, _dump_once) sits behind
    _out_guard() on every path of the function."""
    tree = ast.parse(src)
    par = _parents(tree)
    fn = next((n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "write_manifest"), None)
    if fn is None:
        return ["[out-guard-order] no write_manifest"]
    bad, n_w = [], 0
    for n in ast.walk(fn):
        if isinstance(n, ast.Call) and (write_primitive(n) or _callee(n) in ("_dump", "_dump_once")):
            n_w += 1
            if not behind(n, "_out_guard", par):
                bad.append(f"[out-guard-order] write_manifest: {_callee(n) or write_primitive(n)} is not "
                           f"behind _out_guard() on every path")
    if n_w == 0:
        bad.append("[out-guard-order] write_manifest writes nothing the scan can see")
    return bad


def out_break():
    refuse = f"is not {D.OUT}, under it, or under a temp directory"
    src = module_src()
    no_guard = src_edit(src, "    dst = _out_guard(dst)\n", "")

    def g(path: Path):
        def t():
            D._out_guard(path)
            return []
        return t
    with tmpdir() as tmp:
        link = Path(tmp) / "to_tc10_data"
        link.symlink_to(D.TC10_DATA, target_is_directory=True)
        return plants([
            ("--out research_outputs/tierc10/data (TC10's filed manifest, md and fee schedule)", refuse,
             g(D.TC10_DATA)),
            ("--out a temp-dir symlink that resolves to research_outputs/tierc10/data", refuse, g(link)),
            ("--out a '..' traversal from the stage dir to research_outputs/tierc10/data", refuse,
             g(D.OUT / ".." / ".." / "tierc10" / "data")),
            ("--out the stage dir's parent research_outputs/tierc11", refuse, g(D.OUT.parent)),
            ("write_manifest without its _out_guard call (source copy)", "[out-guard-order]",
             lambda: out_guard_order_findings(no_guard))])


def out_real():
    bad = out_guard_order_findings(module_src())
    with tmpdir() as tmp:
        for q in (D.OUT, D.OUT / "_det_data" / "seed_1", Path(tmp), Path(tmp) / "sub"):
            try:
                got = D._out_guard(q)
            except SystemExit as e:
                bad.append(f"_out_guard refused {_norm(str(q))}: {e}")
                continue
            if got != q.resolve():
                bad.append(f"_out_guard({_norm(str(q))}) returned {_norm(str(got))}")
    return (not bad), ("_out_guard admits the stage dir, a directory under it (_det_data/seed_1), a temp "
                       "directory and one under it, each as its resolved path; every write of "
                       "write_manifest (_dump x2, write_text) sits behind it on every path"
                       if not bad else f"{len(bad)} fault(s): {bad[:3]}")


# ═══════════════════════════════════════════════ F-D11-FETCHPATH  [round 2: defect 10]
FETCH_STEM = "PUMPUSDT"                  # a small Binance tape: every leg below copies a few MB


class FakeResp:
    def __init__(self, payload=None, headers=None, content: bytes = b"{}"):
        self._p, self.headers, self.content, self.status_code = payload, headers or {}, content, 200

    def json(self):
        return self._p


def tripwire(what: str):
    def f(*a, **kw):
        raise AssertionError(f"[offline] {what} was reached")
    return f


def offline_doors() -> ExitStack:
    """Every network and engine-save door of the module a tripwire (a leg stubs what it needs)."""
    st = ExitStack()
    for obj, name in ((D.requests, "get"), (D.ED, "_get"), (D.ED, "_fetch_rest_klines"),
                      (D.ED, "_save_cache"), (D.ED, "_save_funding"), (D.ED, "backfill_funding"),
                      (D, "bybit_klines"), (D, "bybit_funding"), (D, "_bybit_get")):
        st.enter_context(mutated(obj, name, tripwire(f"{getattr(obj, '__name__', obj)}.{name}")))
    return st


@contextmanager
def sandbox(files: dict, saves: bool = False):
    """A temp snapshot the module is BOUND to — D.SNAPSHOT and NAIAD_CACHE_DIR both — holding only
    `files` (rel -> a source path to copy, or a frame), with every network door a tripwire; engine
    saves are tripwires too unless `saves` (then they land in the temp snapshot, _assert_bound
    passing).  Yields (snapshot, out)."""
    with tmpdir() as tmp:
        snap, out = Path(tmp) / "snap", Path(tmp) / "out"
        for sub in ("klines", "funding"):
            (snap / sub).mkdir(parents=True)
        out.mkdir()
        for rel, src in files.items():
            if isinstance(src, pd.DataFrame):
                src.to_parquet(snap / rel, index=False)
            else:
                shutil.copyfile(src, snap / rel)
        with mutated(D, "SNAPSHOT", snap), env_moved(str(snap)), offline_doors() as st:
            if saves:
                for name in ("_save_cache", "_save_funding", "backfill_funding"):
                    st.enter_context(mutated(D.ED, name, ENGINE_REAL[name]))
            yield snap, out


ENGINE_REAL = {n: getattr(D.ED, n) for n in ("_save_cache", "_save_funding", "backfill_funding")}


def fetch_prep() -> dict:
    """Read once from the REAL records and snapshot (read-only) before any sandbox."""
    pre, pin = read_json(OUT / "PRE_STATE.json"), read_json(OUT / "AS_OF_PIN.json")
    assets = {a["stem"]: a for a in D.panel_assets()}
    rel4, relf = f"klines/{FETCH_STEM}_4h.parquet", f"funding/{FETCH_STEM}.parquet"
    cur4 = pd.read_parquet(D.SNAPSHOT / rel4).sort_values("open_time").reset_index(drop=True)
    curf = pd.read_parquet(D.SNAPSHOT / relf).sort_values("funding_time").reset_index(drop=True)
    return {"pre": pre, "pin": pin, "a": assets[FETCH_STEM], "mnt": assets["MNTUSDT_BYBIT"],
            "rel4": rel4, "relf": relf, "cur4": cur4, "curf": curf,
            "last4": int(pre["files"][rel4]["last_ms"]), "first4": int(cur4["open_time"].min()),
            "specs": read_json(OUT / D.CONTRACT_SPECS)}


def replay_specs(P: dict, out: Path, not_trading: str | None = None) -> dict:
    """capture_contract_specs with the venue REPLAYED from the filed venue objects (no network)."""
    objs = [dict(x["venue_object"]) for x in P["specs"]["assets"] if x["venue"] == "BINANCE_USDTM"]
    for o in objs:
        if o["symbol"] == not_trading:
            o["status"] = "SETTLING"
    byb = [x["venue_object"] for x in P["specs"]["assets"] if x["venue"] != "BINANCE_USDTM"]
    info = {"symbols": objs}
    with offline_doors(), mutated(D.ED, "_get", lambda url, params=None, retries=4:
                                  FakeResp(info, content=json.dumps(info).encode())), \
            mutated(D, "_bybit_get", lambda path, params: {"list": byb}):
        return D.capture_contract_specs(out, P["pin"])


def fetchpath_break():
    P = fetch_prep()
    a, pin, pre, rel4, cur4, last4 = P["a"], P["pin"], P["pre"], P["rel4"], P["cur4"], P["last4"]
    clone4 = cur4[cur4["open_time"] <= last4]
    pre_wo = {**pre, "files": {k: v for k, v in pre["files"].items() if k != rel4}}
    mrel = "klines/MNTUSDT_BYBIT_15m.parquet"
    pre_m15 = {**pre, "files": {**pre["files"], mrel: {"last_ms": int(clone4["open_time"].max())}}}

    def ext(files: dict, pre_: dict, asset: dict = a, iv: str = "4h", stub=None):
        def t():
            with sandbox(files) as (snap, out), ExitStack() as st:
                if stub is not None:
                    st.enter_context(mutated(D.ED, "_fetch_rest_klines", stub))
                D.extend_klines(asset, iv, pin, out, pre_)
            return []
        return t

    def off_grid(sym, iv, lo, hi):
        rows = cur4[(cur4["open_time"] >= lo) & (cur4["open_time"] <= hi)].reset_index(drop=True)
        rows.loc[0, "open_time"] = int(rows.loc[0, "open_time"]) + 1
        return rows

    def funding_absent():
        with sandbox({}) as (snap, out):
            D.extend_funding(a, pin, P["first4"], out)
        return []

    def not_trading():
        with tmpdir() as tmp:
            replay_specs(P, Path(tmp), not_trading=FETCH_STEM)
        return []

    def pre_state(files: dict):
        def t():
            with sandbox(files) as (snap, out), mutated(D, "PANEL17", (FETCH_STEM,)):
                shutil.copyfile(OUT / D.CLONE_ATTEST, out / D.CLONE_ATTEST)
                D.write_pre_state(pin, out)
            return []
        return t
    rel5 = f"klines/{FETCH_STEM}_5m.parquet"
    return plants([
        (f"extend_klines on a snapshot without {rel4}", "is absent or not in PRE_STATE", ext({}, pre)),
        (f"extend_klines on {rel4} with PRE_STATE not listing it", "is absent or not in PRE_STATE",
         ext({rel4: clone4}, pre_wo)),
        (f"extend_klines on {rel4} truncated one bar below its PRE_STATE edge (an early start)",
         "is not past the PRE_STATE edge", ext({rel4: clone4.iloc[:-1]}, pre)),
        ("extend_klines with the venue serving one stamp 1 ms off the 4h grid",
         "off-grid open_time(s) — refusing to save", ext({rel4: clone4}, pre, stub=off_grid)),
        ("extend_klines asked for MNT (Bybit) 15m", "Bybit serves no 15m",
         ext({mrel: clone4}, pre_m15, asset=P["mnt"], iv="15m")),
        (f"extend_funding on a snapshot without funding/{FETCH_STEM}.parquet", "is absent — TC11 never "
         "fetches a whole tape", funding_absent),
        (f"capture_contract_specs with {FETCH_STEM} served SETTLING (replayed venue)",
         "not TRADING at the TC11 capture", not_trading),
        (f"write_pre_state over {rel5} as extended by TC11 (moved since the clone)",
         "moved between the clone and PRE_STATE", pre_state({rel5: D.SNAPSHOT / rel5})),
        (f"write_pre_state over a snapshot without {rel5}", "is missing from the TC11 clone",
         pre_state({}))])


def fetchpath_real():
    P = fetch_prep()
    a, pin, pre, rel4, relf, cur4, curf = (P["a"], P["pin"], P["pre"], P["rel4"], P["relf"], P["cur4"],
                                           P["curf"])
    bad = []
    # (a) a --fetch resume over the FILED snapshot: nothing asked, nothing saved, no HALT
    kl, fu = [], []
    with tmpdir() as tmp, offline_doors():
        out = Path(tmp)
        for x in D.panel_assets():
            for iv in ("4h", "12h", "1h", "15m", "5m"):
                if iv in D.lenses_of(x["stem"]):
                    kl.append(D.extend_klines(x, iv, pin, out, pre))
            first = int(pd.read_parquet(D.kline_path(x["stem"], "4h"), columns=["open_time"])["open_time"].min())
            fu.append(D.extend_funding(x, pin, first, out))
        logged = (out / "FETCH_LOG.jsonl").exists()
    if logged or any(not r["complete"] or r["fetched"] for r in kl) or any(not r.get("skipped") for r in fu):
        bad.append(f"a resume over the filed snapshot asked or wrote something (log {logged})")
    # (b) offline, from the CLONE-TIME bytes, the fetch path reproduces the filed content
    def rest(sym, iv, lo, hi):
        return cur4[(cur4["open_time"] >= lo) & (cur4["open_time"] <= hi)].reset_index(drop=True)

    def eget(url, params=None, retries=4):
        if url.endswith("/fapi/v1/ping"):
            return FakeResp({}, headers={"x-mbx-used-weight-1m": "1"})
        if url.endswith("/fapi/v1/fundingRate"):
            sel = curf[(curf["funding_time"] >= params["startTime"])
                       & (curf["funding_time"] <= params["endTime"])].head(params.get("limit", 1000))
            return FakeResp([{"fundingTime": int(t), "fundingRate": repr(float(r))}
                             for t, r in zip(sel["funding_time"], sel["funding_rate"])])
        raise AssertionError(f"[offline] unexpected GET {url}")
    with sandbox({rel4: D.TC10_SNAPSHOT / rel4, relf: D.TC10_SNAPSHOT / relf}, saves=True) as (snap, out), \
            mutated(D.ED, "_fetch_rest_klines", rest), mutated(D.ED, "_get", eget):
        r1 = D.extend_klines(a, "4h", pin, out, pre)
        r2 = D.extend_klines(a, "4h", pin, out, pre)                  # a resume: nothing to ask
        rf = D.extend_funding(a, pin, P["first4"], out)
        got4 = content_hash(pd.read_parquet(snap / rel4).sort_values("open_time"), D.KLINE_COLS)
        gotf = content_hash(pd.read_parquet(snap / relf).sort_values("funding_time"), D.FUNDING_COLS)
        log = [json.loads(x) for x in (out / "FETCH_LOG.jsonl").read_text(encoding="utf-8").splitlines()]
    want4, wantf = content_hash(cur4, D.KLINE_COLS), content_hash(curf, D.FUNDING_COLS)
    added_f = len(curf) - int(pre["files"][relf]["rows"])
    if not (r1["complete"] and r1["fetched"] == len(cur4) - int(pre["files"][rel4]["rows"])
            and r2["fetched"] == 0 and r2["complete"] and got4 == want4 and gotf == wantf
            and [x["kind"] for x in log] == ["klines", "funding"]):
        bad.append(f"offline replay: klines {r1['fetched']} bars (resume {r2['fetched']}), content "
                   f"{got4 == want4}, funding content {gotf == wantf}, log kinds {[x['kind'] for x in log]}")
    # (c) the TRADING check admits the capture of record, replayed
    with tmpdir() as tmp:
        doc = replay_specs(P, Path(tmp))
    if doc["assets"] != P["specs"]["assets"] or not doc["all_trading"]:
        bad.append("capture_contract_specs replayed from the filed venue objects does not rebuild its rows")
    # (d) write_pre_state over the clone-time bytes rebuilds the filed rows
    rels = [r for r in D.scope_paths() if f"/{FETCH_STEM}" in r or r.startswith(f"klines/{FETCH_STEM}_")]
    with sandbox({r: D.TC10_SNAPSHOT / r for r in rels}) as (snap, out), mutated(D, "PANEL17", (FETCH_STEM,)):
        shutil.copyfile(OUT / D.CLONE_ATTEST, out / D.CLONE_ATTEST)
        ps = D.write_pre_state(pin, out)
    if ps["files"] != {r: pre["files"][r] for r in rels}:
        bad.append(f"write_pre_state over {FETCH_STEM}'s clone-time files does not rebuild the filed rows")
    return (not bad), (f"a --fetch resume over the filed snapshot: {len(kl)} kline extensions complete with "
                       f"0 bars asked, {len(fu)} funding tapes skipped (edge in the pin's hour) — no "
                       f"request, no save, no log row, no HALT; offline from {FETCH_STEM}'s clone-time "
                       f"bytes, extend_klines (+{r1['fetched']} bars) and extend_funding (+{added_f} prints) "
                       f"through engine.data's own save path rebuild the filed content shas, and a second "
                       f"extend_klines asks nothing; capture_contract_specs replayed from the filed venue "
                       f"objects admits all {len(doc['assets'])} symbols TRADING and rebuilds its rows; "
                       f"write_pre_state over {FETCH_STEM}'s {len(rels)} clone-time files rebuilds the filed "
                       f"PRE_STATE rows" if not bad else f"{len(bad)} fault(s): {bad[:3]}")


FIXTURES = (
    ("F-D11-GUARD", "the substrate guard admits the TC11 snapshot and nothing else",
     "an unset variable, the live cache, a directory inside it, the TC10 snapshot, a foreign "
     "directory, or a snapshot path without klines/ is accepted, or the real env does not "
     "resolve to tc11_20260925 with engine.data bound to it", guard_break, guard_real),
    ("F-D11-BOUND", "the write-time barrier: every snapshot write sits behind _assert_bound()",
     "_assert_bound() passes with NAIAD_CACHE_DIR or the module's SNAPSHOT moved off the TC11 "
     "snapshot, any engine save / _write_if_changed call is reachable from an entry point "
     "without _assert_bound() on every path before it, or a file-writing call sits in a "
     "function the fixture has not typed as a write owner", bound_break, bound_real),
    ("F-D11-OUT", "--out admits the stage dir, a directory under it or a temp dir, and nothing else",
     "_out_guard admits research_outputs/tierc10/data, a symlink to it, a '..' traversal to it or the "
     "stage dir's parent, refuses the stage dir, a directory under it or a temp directory, or a write "
     "of write_manifest does not sit behind _out_guard()", out_break, out_real),
    ("F-D11-PORT", "every port of tierc10_data is what its provenance comment says",
     "a VERBATIM port is not AST-identical to its source, a comment names the wrong lines or "
     "sha, a CHANGED label hides an identical copy, or tierc10_data.py's sha moved",
     port_break, port_real),
    ("F-D11-SCOPE", "the fixture's typed 124 paths are the module's, PRE_STATE's and the manifest's",
     "D.scope_paths() differs from the fixture's typed 124 (in order), or PRE_STATE.json's files "
     "or the manifest's files[] are not that set", scope_break, scope_real),
    ("F-D11-CLONE", "the clone reproduces TC10's bytes up to every TC10 edge",
     "any in-scope file's rows up to its TC10 edge differ from the TC10 snapshot's rows (whose "
     "file re-hashes to TC10's manifest), any other file differs from TC10's record, or the "
     "clone's file set differs from TC10's", clone_break, clone_real),
    ("F-D11-PIN", "one as-of pin, closed by the venue, written once",
     "the pin is not 2026-09-25T00:00:00Z, is not a 4h close, is not closed by the venue "
     "record in the file, lacks a TC10 key, moved since the seal, or write-once lets a "
     "rewrite through, or a re-read reaches the network", pin_break, pin_real),
    ("F-D11-CLOCK", "the fetch-time latest closed 4h, filed beside the pin",
     "FETCH_CLOCK_NOTE.json's clock row, venue clock, latest closed 4h or relabel is not what the "
     "filed FETCH_LOG.jsonl / AS_OF_PIN.json / manifest show, or record_fetch_clock does not file "
     "one kind='clock' row with the venue clock and its latest closed 4h, or run_fetch (or --all's "
     "seal) can run before it", clock_break, clock_real),
    ("F-D11-PREFIX", "no pre-existing row was rewritten by the fetch",
     "any of the 124 PRE_STATE files' old rows (<= its old edge) does not re-hash to its "
     "PRE_STATE content sha", prefix_break, prefix_real),
    ("F-D11-EDGE", "every lens ends exactly at its last bar closing <= the pin, whole",
     "a typed kline file's last open is not its lens's last bar closing <= the pin, or it holds a "
     "gap, a duplicate, an off-grid stamp or a row past the pin; a typed funding tape lacks the "
     "pin-hour print, fails coverage, repeats a print or holds one past the pin + 60 s; or the "
     "manifest mis-describes a file", edge_break, edge_real),
    ("F-D11-FETCHPATH", "the fetch path's HALTs fire offline; a resume over the filed state is a no-op",
     "on a temp snapshot the module is bound to, an absent file, a file PRE_STATE does not list, an "
     "early start, an off-grid venue stamp, a Bybit 15m, an absent funding tape, a symbol not TRADING or "
     "a file moved since the clone does not HALT; or a --fetch resume over the filed snapshot asks or "
     "saves anything; or the fetch path replayed offline from clone-time bytes does not rebuild the "
     "filed content, the capture's rows or PRE_STATE's rows", fetchpath_break, fetchpath_real),
    ("F-D11-DERIVE", "1d / 1w are native 4h re-derived, bit for bit",
     "the plain-loop 1d (six complete 4h bars per UTC day) or 1w (seven complete days, "
     "Monday-anchored) differs from a derived file of a typed asset in any stamp or value",
     derive_break, derive_real),
    ("F-DET", "two subprocess manifest builds under different hash seeds, one set of bytes",
     "the PYTHONHASHSEED 1 and 20260924 builds differ from each other or from the filed "
     "bytes, hold another file set, either exits nonzero, or a JSON carries a clock field",
     det_break, det_real),
    ("F-D11-UNTOUCHED", "the TC10 snapshot is TC10's; the live cache stat held across THIS FIXTURE RUN",
     "a TC10 snapshot file does not re-hash to TC10's manifest (or its clone-time record), "
     "TC10's own seal faults, or the live cache MANIFEST.json's stat moved across this fixture "
     "run only (the build's live-cache claim is by construction: F-D11-GUARD + F-D11-BOUND)",
     untouched_break, untouched_real),
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
    global RUN_ROOT, LIVE_STAT_AT_START
    LIVE_STAT_AT_START = live_stat()
    args = sys.argv[1:]
    root = RUN_ROOT = Path(next((a.split("=", 1)[1] for a in args if a.startswith("--root=")), OUT))
    pick = [a.lower() for a in args if not a.startswith("--")]
    pin = read_json(OUT / "AS_OF_PIN.json")
    first = f"as_of_last_closed_4h: {pin['as_of_last_closed_4h']}"
    if first != AS_OF_LINE:
        raise SystemExit(f"HALT: the filed pin reads {first!r}, not {AS_OF_LINE!r}")
    say(first)
    say("=" * 78)
    say("TIER-C11 STAGE TC11-D FIXTURES — the corridor · break leg first, RED or void")
    say("=" * 78)
    say(f"seed {SEED} · substrate {D.SNAPSHOT.name} · pin close ms {pin['as_of_last_closed_4h_close_ms']}"
        f" · contract sha {D.CONTRACT_SHA256[:16]}… · module scripts/tierc11_data.py")
    say(f"[LEAN-HEPHAESTUS] {len(D.LEANS)} readings filed in STAGE_D_MANIFEST.json leans "
        f"(L-0.1, L-0.2, L-1.1, L-1.2 of research_outputs/tierc11/LEANS.md; D11-a..g)")
    say("hardened per research_outputs/tierc11/review/TC11-D_VERIFY.md defects 1-8 and the round-2 "
        "verification's defects 1-10: a plant counts only when the finding names its detector")
    for fid, title, fails_if, b, r in FIXTURES:
        if not pick or any(q in fid.lower() for q in pick):
            prove(fid, title, fails_if, b, r)
    say(f"\n  {len(PASSED)} GREEN, {len(FAILED)} RED · break legs RED (correct) "
        f"{TALLY['break_red']}/{TALLY['break_red'] + TALLY['break_void']} · real legs GREEN "
        f"{TALLY['real_green']}/{TALLY['real_green'] + TALLY['real_red']} · {TALLY['plants']} plants")
    for f in FAILED:
        say(f"    RED: {f}")
    root.mkdir(parents=True, exist_ok=True)
    body = ("\n".join(LINES) + "\n").encode("utf-8")
    name = TRANSCRIPT if not pick else TRANSCRIPT.replace(".txt", "_partial.txt")
    bad = file_transcript(root / name, body, "--refile-transcript" in args or bool(pick))
    for x in bad:
        clock(x)
    if FAILED:
        print("*** HALT: fixture mismatch. Nothing downstream is trustworthy. ***")
    return 1 if (FAILED or bad) else 0


if __name__ == "__main__":
    raise SystemExit(main())
