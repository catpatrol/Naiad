#!/usr/bin/env python
"""TIER-C11 · TC11-R — F-PINS · F-REROOT-NEST · F-CAL · F-NEST-ASOF · F-EQ-SCAN ·
F-COIN · F-DET.  The fixtures of THE RANGE LAYER, scripts/tierc11_nest.py
[LEANS L-0.3, L-R.2, L-R.3, L-R.5, L-R.6, L-F.1, L-F.2].

TWO LEGS PER FIXTURE, the BREAK leg first, and it must go RED or the fixture is
VOID — a guard nobody has seen fail is a guard nobody has seen [the prove() law
of scripts/tierc10_rf_fixtures.py / tierc11_env_fixtures.py].  Each leg prints
its own FAILS IF.  A break leg is a set of PLANTS judged one at a time; a plant
counts as CAUGHT only if the finding NAMES THE INTENDED DETECTOR (its expected
substring).  A plant that crashes is a FIXTURE DEFECT, never a catch.  Every
plant is made on a COPY (a dict, a frame, an array, a mutated module attribute
restored in `finally`, or a mutated copy of tierc11_nest.py in a temp dir run in
a SUBPROCESS); no filed artifact moves.

  F-PINS        FAILS IF the port / engine sha, the 12 pins (values, types, key
                order) or the retest grid pins differ from STEP0_RECORD / the
                literals typed HERE.  SABOTAGE: ten plants through
                N.pins_findings and a mutated tierc11_nest that must HALT.
  F-REROOT-NEST FAILS IF a C.* / stamps.* / null.* re-root misses its typed
                target, a post-shim clause is not ok, a TC10 binding is
                undeclared, or a fresh import does not exit 0 with BLOCKED 0 and
                ALLOW ⊆ {STEP0, TUNING_RESULT}.  SABOTAGE: mutated copies (the
                C.STAGE_D re-root skipped — the ROOTS clause, checked first, in
                EVERY tree; a second census root; C.LENS_MS['1h']; stamps.OUT;
                the toll label; C.SEED; the provisional retest pins).
  F-CAL         FAILS IF any filed pick, grid row, label or input sha does not
                reproduce from an INDEPENDENT path typed HERE: tapes read from
                the snapshot files (tuning = bars with CLOSE <= the era cut —
                never a holdout bar), fresh ATR, a density loop over
                RC.run_machine at the 11 typed scales, the tie-break typed here.
                SABOTAGE: six plants (TUNING-HEAD, IN-SAMPLE-LABEL, COVERAGE,
                GRID-ROWS, SOURCES, LABEL).
  F-NEST-ASOF   FAILS IF, at >= 40 cuts per nest lens per CLASSIC5 asset, the
                prefix nest vector != the full-run vector, a lens's as-of arrays
                / event frames known by the cut differ, OR the full-run vector
                at the cut != THE END-OF-PREFIX MACHINE ORACLE (the prefix run's
                live range top / bottom, final_state, harden counts, flips known
                by touch + 6, untouched memory lines -> coincidence).  SABOTAGE:
                the leaked redraw and a flip read at its stamp (prefix check);
                top / bot swapped and the pre-repair deviation reset (causal but
                WRONG readers — only the oracle can see them), each on EVERY
                asset.
  F-EQ-SCAN     FAILS IF, on CLASSIC5 x 7 lenses x {calibrated, frozen3.0}, ANY
                scan row (every seq, taps and memory line) differs from a PLAIN-
                LOOP scan typed HERE (own EMA, own loops), the first row per DIE
                differs from C.retest_holds / BK.band_hold_candidates, the scan
                breaks its own law, the memory-line first row differs from the
                engine's one-shot flip, or no DIE is rescued (taps, memory line).
                SABOTAGE: skip-first-touch, ONE-SHOT, skip-SECOND-touch, on the
                taps and on the memory line.
  F-COIN        FAILS IF planted configurations differ from hand-computed flags,
                a real nest row differs from a plain-Python recomputation, or the
                NA structure is wrong.  SABOTAGE: COIN_FRAC 0.5; memory lines
                ignored.
  F-DET         [L-F.1 variant (i)] FAILS IF two SUBPROCESS BUILDS (PYTHONHASHSEED
                1, 20260924) — the lean block + range probe AND a full rebuild of
                the four pick files into their own _det_ roots — differ in the
                file set, the bytes, or the parquet content sha, from each other,
                from this run's probe, or from the FILED pick files.  SABOTAGE:
                a bent byte, a hash-order emission, an extra file, a moved
                parquet, a rebuilt SCALE_PICKS.json != the filed one.
BANNED: self-comparison; one example where cardinality was possible; a tuned
magnitude bound standing in for an identity; a check whose claim is not the
design's claim.  FROZEN SUBSTRATE: HALTs unless NAIAD_CACHE_DIR is the TC11
snapshot (tierc11_env's guard).  Seed 20260924.  The transcript carries no clock,
no temp path and no tree-dependent byte: it is byte-identical in the main tree
and in a review worktree (gitignored parquet absent, research_outputs/tierc10
absent) [L-F.3].

Run:  export NAIAD_CACHE_DIR=$HOME/.cache/naiad/snapshots/tc11_20260925 PYTHONDONTWRITEBYTECODE=1
      ~/venvs/naiad/bin/python -B scripts/tierc11_nest_fixtures.py \\
          [leg-substring ...] [--refile-transcript] [--root=DIR]
Exit 0 = every leg GREEN, every break RED · 1 = a RED or VOID fixture, a
transcript finding, or a HALT.
"""
from __future__ import annotations

import contextlib
import copy
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
import tierc11_nest as N                                             # noqa: E402  (guards first)

import numpy as np                                                   # noqa: E402
import pandas as pd                                                  # noqa: E402

E, C, RC = N.E, N.C, N.RC

# ── FIXTURE-TYPED LITERALS: the commission, a second object, never N's own ──
HOME = Path.home()
TC11_SNAP = HOME / ".cache" / "naiad" / "snapshots" / "tc11_20260925"
TC11_OUT = ROOT / "research_outputs" / "tierc11"
PIN = 1790294400000                      # 2026-09-25T00:00:00Z [L-0.1]
ERA_CUT = 1719791999000                  # 2024-06-30T23:59:59Z [L-1.3]
SEED = 20260924
DET_SEEDS = (1, SEED)
AS_OF_LINE = "as_of_last_closed_4h: 2026-09-25T00:00:00Z"
PINS12 = (("LEG_MIN", 0.5), ("REV_MIN", 1.75), ("TOUCH_EPS", 0.60), ("DEV_RETURN_BARS", 7),
          ("BREAK_CONFIRM_N", 8), ("BREAK_MARGIN", 1.5), ("BOUNDARY_MODE", "body"),
          ("SCALE_MULT", 3.0), ("FLIP_HOLD_MARGIN", 1.0), ("FLIP_HOLD_BARS", 6),
          ("MEM_TTL_BARS", 400), ("ATR_LEN", 14))
PORT_SHA = "19c5507ff2d39b68aa119ff701aef58a2d219fa287c34cdf7302ebf2bbb7b37d"
ENGINE_SHA = "bbae464fdc8e0e01fc90b286aa79e726fcff4422e6118dee1173f2460dab84d4"
GRID_SHA = "2135ca663a7c407ca1a2a99165692bd3a9a9cd90de458e03dabdc2e32855e7b3"
LENS_MS = {"5m": 300_000, "15m": 900_000, "1h": 3_600_000, "4h": 14_400_000,
           "12h": 43_200_000, "1d": 86_400_000, "1w": 604_800_000}
CLASSIC5 = ("BTCUSDT", "ETHUSDT", "SOLUSDT", "NEARUSDT", "ZECUSDT")
UNSEEN12 = ("ENAUSDT", "PUMPUSDT", "HYPEUSDT", "MNTUSDT_BYBIT", "SUIUSDT", "LTCUSDT",
            "XMRUSDT", "BNBUSDT", "UNIUSDT", "1000PEPEUSDT", "DOGEUSDT", "1000BONKUSDT")
LENSES7 = ("5m", "15m", "1h", "4h", "12h", "1d", "1w")
NEST5 = ("1h", "4h", "12h", "1d", "1w")
UNSEEN_LENSES = ("1h", "4h", "1d")
# the commission [L-R.1]: CLASSIC5 x 7 lenses + the twelve x {1h, 4h, 1d} = 5 x 7 + 12 x 3
COMMISSION = (tuple((s, l) for s in CLASSIC5 for l in LENSES7)
              + tuple((s, l) for s in UNSEEN12 for l in UNSEEN_LENSES))
N_COMMISSION = 71
LADDER = {"1h": "4h", "4h": "12h", "12h": "1d", "1d": "1w", "1w": None}      # [L-R.5]
BANDS = (("tap89", 89), ("tap127", 127), ("tap200", 200))                   # [L-R.6(a)]
RETEST_MARGIN, RETEST_HOLD, RETEST_TTL = 1.0, 3, 400                       # C.RETEST_PINS of record
MEM_MARGIN, MEM_HOLD, MEM_TTL = 1.0, 6, 400                                # FLIP_HOLD_* / MEM_TTL_BARS
SCALES = (1.5, 1.75, 2.0, 2.25, 2.5, 2.75, 3.0, 3.25, 3.5, 3.75, 4.0)       # [L-R.2] 1.5..4.0
DENSITY_TARGET = 0.75                                                       # confirmed / 100 bars
FROZEN = 3.0
MIN_TUNING_BARS = 400
COIN = 0.25                                                                 # x ATR_L [L-R.5]
FALLBACK_WINDOW = "whole-tape (fallback)"
IN_SAMPLE_TEXT = {"tuning": "IN-SAMPLE for tuning · OUT-OF-SAMPLE for holdout",
                  "first_half": "IN-SAMPLE for the first half of tuning · OUT-OF-SAMPLE after it",
                  "whole": "IN-SAMPLE for tuning AND holdout (fit on the whole tape)"}
PICK_FILES = ("SCALE_GRID.parquet", "SCALE_PICKS.json", "SCALE_PICKS.md",
              "SCALE_PICKS_SOURCES.json")
T11 = TC11_OUT
RANGES = T11 / "ranges"
# the C.* / stamps.* / null.* re-roots of L-0.3 (and the ones the list missed),
# EACH WITH ITS INTENDED TARGET — (module, attr, key, target)
DECL_REROOT = (
    (C, "SNAPSHOT", None, TC11_SNAP), (C, "OUT", None, T11 / "census"),
    (C, "STAGE_D", None, T11 / "data"), (C, "NULL_ROOT", None, RANGES / "null"),
    (C, "SEED", None, SEED),
    (C, "LENS_MS", "15m", 900_000), (C, "LENS_MS", "1h", 3_600_000),
    (C, "LENS_MS", "12h", 43_200_000), (C, "LENS_MS", "1w", 604_800_000),
    (C, "LENS_SOURCE", "15m", "15m"), (C, "LENS_SOURCE", "1h", "1h"),
    (C, "LENS_SOURCE", "12h", "12h"), (C, "LENS_SOURCE", "1w", "1w"),
    (C, "LENS_SOURCE", "1d", "4h"),
    (N.ST, "SNAPSHOT", None, TC11_SNAP), (N.ST, "OUT", None, RANGES / "stamps"),
    (N.ST, "OUT_RERUN", None, T11 / "_det_rerun" / "stamps"), (N.ST, "SEED", None, SEED),
    (N.ST, "LENS_MS", "15m", 900_000), (N.ST, "LENS_MS", "1h", 3_600_000),
    (N.ST, "LENS_MS", "12h", 43_200_000), (N.ST, "LENS_MS", "1w", 604_800_000),
    (N.NL, "SEED", None, SEED), (N.NL, "OUT", None, RANGES / "null"),
)
ALLOWED_NEST_READS = {"research_outputs/tierc10/STEP0_RECORD.json",
                      "research_outputs/tierc10/census/TUNING_RESULT.json"}

OUT = RANGES
RUN_ROOT = OUT
TRANSCRIPT = "FIXTURES_NEST.txt"
ARTIFACT = "NEST_PROBE.txt"
PY = sys.executable
NEST_SRC = ROOT / "scripts" / "tierc11_nest.py"
POOL = 8                                 # EXEC'd worker interpreters for the corpus fixtures
DET_PROCS = 1                            # N.build_picks inside each F-DET subprocess: sequential
                                         # (its fork pool is slow on this host; see _exec_map)
NAN = float("nan")
LINES: list[str] = []
PASSED: list[str] = []
FAILED: list[str] = []
_TMP_RX = re.compile(r"(/private)?/(var/folders|tmp)/[^\s'\"]+")


def say(line: str = "") -> None:            # deterministic -> transcript
    line = _TMP_RX.sub("<tmp>", line)
    print(line, flush=True)
    LINES.append(line)


def clock(line: str) -> None:               # wall clock, temp paths, tree facts -> stdout ONLY
    print(f"  [clock · stdout only] {line}", flush=True)


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def frame_sha(df: pd.DataFrame) -> str:
    return sha_bytes(df.to_csv(index=False).encode("utf-8"))


def prove(fid: str, title: str, break_if: str, real_if: str, break_leg, real_leg) -> None:
    """Break first; it must go RED (ok False) or the fixture is VOID.  Each leg
    prints its own FAILS IF."""
    say(f"\n{fid} — {title}")
    t0 = time.time()
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
    clock(f"{fid} wall {time.time() - t0:.1f}s")
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


@contextlib.contextmanager
def mutated(obj, name: str, value):
    """obj.name = value for the duration; restored in finally."""
    old = getattr(obj, name)
    setattr(obj, name, value)
    try:
        yield
    finally:
        setattr(obj, name, old)


def _exec_map(kind: str, jobs: list, procs: int = POOL) -> list:
    """A parallel map over FRESH INTERPRETERS (this file, `--worker=<kind>`), each
    importing tierc11_nest under its own name (the range door opens) — exec, not
    fork: forked children on this host spent ~10x their user time in the kernel
    (measured: 10 scan cells, fork pool 50 s wall / 433 s sys; exec'd 5 s).  Jobs
    are dealt round-robin; results come back as JSON in JOB ORDER, so nothing
    depends on the pool.  A worker that exits nonzero RAISES (never a silent gap)."""
    procs = max(1, min(procs, len(jobs)))
    deal = [list(range(i, len(jobs), procs)) for i in range(procs)]
    out: list = [None] * len(jobs)
    with tempfile.TemporaryDirectory(prefix="tc11nestw_") as d:
        run = []
        for w, idx in enumerate(deal):
            jp, op = Path(d) / f"jobs_{w}.json", Path(d) / f"out_{w}.json"
            jp.write_text(json.dumps([jobs[i] for i in idx]), encoding="utf-8")
            run.append((idx, op, subprocess.Popen(
                [PY, "-B", str(Path(__file__).resolve()), f"--worker={kind}", f"--jobs={jp}",
                 f"--out={op}"], env=_env(), cwd=str(ROOT), stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE, text=True)))
        for idx, op, pr in run:
            _, err = pr.communicate(timeout=7200)
            if pr.returncode != 0 or not op.exists():
                raise RuntimeError(f"worker {kind} exit {pr.returncode}: {err[-600:]}")
            for i, r in zip(idx, json.loads(op.read_text(encoding="utf-8"))):
                out[i] = r
    return out


def _worker_main(kind: str, jobs_path: str, out_path: str) -> int:
    jobs = json.loads(Path(jobs_path).read_text(encoding="utf-8"))
    fn = {"eq": lambda j: eq_cell(*j), "cal": lambda j: _cal_cell(tuple(j)),
          "asof": lambda j: asof_asset(*j)}[kind]
    Path(out_path).write_text(json.dumps([fn(j) for j in jobs]), encoding="utf-8")
    return 0


def _env() -> dict:
    return dict(os.environ, NAIAD_CACHE_DIR=str(TC11_SNAP), PYTHONDONTWRITEBYTECODE="1")


def run_py(code: str, pre_path: str | None = None, timeout: int = 900
           ) -> subprocess.CompletedProcess:
    head = (f"import sys\nsys.dont_write_bytecode = True\n"
            f"sys.path.insert(0, {str(ROOT)!r})\nsys.path.insert(0, {str(ROOT / 'scripts')!r})\n")
    if pre_path:
        head += f"sys.path.insert(0, {pre_path!r})\n"
    return subprocess.run([PY, "-B", "-c", head + code], capture_output=True, text=True,
                          env=_env(), cwd=str(ROOT), timeout=timeout)


def _last_json(out: str):
    for ln in reversed(out.strip().splitlines()):
        if ln.startswith("{") or ln.startswith("["):
            return json.loads(ln)
    raise RuntimeError(f"no JSON line in the subprocess output: {out[-300:]!r}")


_IMPORT_TAIL = """
import json
try:
    import tierc11_nest as N
    print(json.dumps({"raised": False, "post_shim": N.POST_SHIM}))
except BaseException as e:
    print(json.dumps({"raised": True, "type": type(e).__name__, "msg": str(e)}))
"""


def shadow_import(src: str) -> list[str]:
    """Import a MUTATED copy of tierc11_nest (a temp dir first on sys.path, the
    file named tierc11_nest.py so the range door opens) in a fresh interpreter.
    The finding is the refusal: a HALT (SystemExit) or an AuditHalt, with the
    process exit code."""
    with tempfile.TemporaryDirectory(prefix="tc11nest_") as d:
        (Path(d) / "tierc11_nest.py").write_text(src, encoding="utf-8")
        r = run_py(_IMPORT_TAIL, pre_path=d)
    j = _last_json(r.stdout)
    if not j["raised"]:
        return []
    return [f"{j['type']}: {j['msg']} ‖ exit {r.returncode}"]


def _mutate(src: str, old: str, new: str) -> str:
    if src.count(old) != 1:
        raise RuntimeError(f"mutation anchor not unique ({src.count(old)}x): {old[:60]!r}")
    return src.replace(old, new)


def _nest_src() -> str:
    return NEST_SRC.read_text(encoding="utf-8")


def _same(a, b) -> bool:
    """Exact equality, NA / NaN / None equal to each other only."""
    na = a is None or a is pd.NA or (isinstance(a, float) and a != a)
    nb = b is None or b is pd.NA or (isinstance(b, float) and b != b)
    if na or nb:
        return na and nb
    return a == b


def _py(v):
    """A frame cell -> a plain Python value (NA -> None)."""
    if v is None or v is pd.NA:
        return None
    if isinstance(v, (np.floating, float)):
        return float(v)
    if isinstance(v, (np.bool_, bool)):
        return bool(v)
    if isinstance(v, (np.integer, int)):
        return int(v)
    return v


def _first_diff(x: bytes, y: bytes) -> int:
    return next((i for i in range(min(len(x), len(y))) if x[i] != y[i]), min(len(x), len(y)))


# ═════════════════════════════════════════════════════════════════ F-PINS
def pins_break():
    base = N.pins_inputs()

    def bent(**kw):
        d = copy.deepcopy(base)
        d.update(kw)
        return lambda: N.pins_findings(**d)

    def bend_pin(k, v):
        return [(kk, (v if kk == k else vv)) for kk, vv in base["pins"]]

    swapped = list(base["pins"])
    swapped[2], swapped[3] = swapped[3], swapped[2]
    rec_bad = copy.deepcopy(base["record"])
    rec_bad["pins_of_record"]["DEV_RETURN_BARS"] = 8
    flip = lambda h: h[:-1] + ("0" if h[-1] != "0" else "1")      # noqa: E731
    src = _nest_src()
    return plants([
        ("TOUCH_EPS perturbed 0.60 -> 0.61 (live)", "PINS-12",
         bent(pins=bend_pin("TOUCH_EPS", 0.61))),
        ("ATR_LEN 14 handed as the float 14.0", "PINS-12", bent(pins=bend_pin("ATR_LEN", 14.0))),
        ("the record's DEV_RETURN_BARS 7 -> 8", "PINS-12", bent(record=rec_bad)),
        ("TOUCH_EPS and DEV_RETURN_BARS swapped in key order", "PINS-ORDER", bent(pins=swapped)),
        ("the port sha bent by one hex digit", "PORT-SHA", bent(port_sha=flip(base["port_sha"]))),
        ("the engine sha bent by one hex digit", "ENGINE-SHA",
         bent(engine_sha=flip(base["engine_sha"]))),
        ("the PROVISIONAL retest hold 6 (a worktree's fallback)", "RETEST-PINS",
         bent(retest=dict(base["retest"], hold_bars=6))),
        ("the retest grid sha bent", "RETEST-PINS",
         bent(retest=dict(base["retest"], grid_sha=flip(base["retest"]["grid_sha"])))),
        ("a port imported from another file", "PORT-FILE",
         bent(port_file=str(ROOT / "scripts" / "rangefinder_core.py"))),
        ("a mutated tierc11_nest whose port literal is bent (import must HALT)",
         "PINS [L-R.3]",
         lambda: shadow_import(_mutate(src, f'PORT_SHA = "{PORT_SHA}"',
                                       f'PORT_SHA = "{flip(PORT_SHA)}"'))),
    ])


def pins_real():
    P = N.pins_inputs()
    bad = N.pins_findings(**P)
    rec = P["record"]
    typed = list(PINS12)
    ok_typed = (P["pins"] == typed and list(rec["pins_of_record"].items()) == typed
                and all(type(a[1]) is type(b[1]) for a, b in zip(P["pins"], typed)))
    ok_sha = P["port_sha"] == PORT_SHA and P["engine_sha"] == ENGINE_SHA
    R = P["retest"]
    ok_rt = (R["margin_atr"], R["hold_bars"], R["ttl_bars"], R["grid_sha"]) == (1.0, 3, 400, GRID_SHA)
    for ln in N.pins_block().rstrip("\n").splitlines():
        say(f"      {ln}")
    return (not bad and ok_typed and ok_sha and ok_rt), (
        f"N.pins_findings: {len(bad)} findings {bad[:2]}; the 12 live pins == STEP0_RECORD "
        f"pins_of_record == the 12 typed here, values + types + key order: {ok_typed}; port "
        f"{P['port_sha'][:16]}… / engine {P['engine_sha'][:16]}… == the typed literals: "
        f"{ok_sha}; C.RETEST_PINS (1.0, 3, 400, {R['grid_sha'][:16]}…) == typed: {ok_rt}")


# ═══════════════════════════════════════════════════════════ F-REROOT-NEST
def reroot_break():
    src = _nest_src()
    return plants([
        ("C.STAGE_D re-root skipped (every later read would go through TC10's data dir)",
         "C.STAGE_D / C.SNAPSHOT are TC11's",
         lambda: shadow_import(_mutate(
             src, '    ("C", "STAGE_D", None, E.OUT / "data", "L-0.3"),\n', ""))),
        ("C.OUT re-rooted to a SECOND census root (tierc11/ranges/census)", "one census root",
         lambda: shadow_import(_mutate(src, '    ("C", "OUT", None, E.OUT / "census",\n',
                                       '    ("C", "OUT", None, OUT / "census",\n'))),
        ("C.LENS_MS['1h'] extension skipped", "LENS_MS",
         lambda: shadow_import(_mutate(
             src, '    ("C", "LENS_MS", "1h", _NEW_LENS_MS["1h"], "L-0.3"),\n', ""))),
        ("stamps.OUT re-root skipped", "undeclared TC10 binding",
         lambda: shadow_import(_mutate(src, '    ("ST", "OUT", None, OUT / "stamps", "L-0.3"),\n', ""))),
        ("the toll label override skipped (the census.py:520 leak)", "toll_bps_for",
         lambda: shadow_import(_mutate(src, '    ("C", "toll_bps_for", None, toll_bps_for11,\n',
                                       '    ("C", "LENS_MS", "12h", _NEW_LENS_MS["12h"],\n'))),
        ("C.SEED re-root skipped (TC10's 20260921 survives)", "seeds re-rooted",
         lambda: shadow_import(_mutate(src, '    ("C", "SEED", None, SEED, "L-0.3"),\n', ""))),
        ("the PROVISIONAL retest pins resolved (a worktree without TUNING_RESULT)", "RETEST-PINS",
         lambda: shadow_import(_mutate(
             src, "C.RETEST_PINS = C.resolve_retest_pins(E.tc10_record(_TUNING_REL).parent)",
             "C.RETEST_PINS = dict(C.RETEST_DEFAULT)"))),
    ])


def reroot_real():
    bad = []
    for mod, attr, key, target in DECL_REROOT:
        got = getattr(mod, attr) if key is None else getattr(mod, attr).get(key)
        same = (E._real(got) == E._real(target)) if isinstance(target, Path) else (got == target)
        if not same:
            bad.append(f"{mod.__name__}.{attr}{'' if key is None else f'[{key!r}]'} = {got!r} "
                       f"!= typed {target!r}")
    if set(C.LENSES) != set(LENSES7) or dict(C.LENS_MS) != LENS_MS:
        bad.append(f"C.LENSES / LENS_MS {list(C.LENSES)} {dict(C.LENS_MS)}")
    if C.toll_bps_for.__name__ != "toll_bps_for11":
        bad.append("C.toll_bps_for is not the label-true override")
    lab = C.toll_bps_for("BTCUSDT")[1]
    if "tierc10" in lab:
        bad.append(f"toll label still names TC10: {lab}")
    census = {E._real(p.parent) for p in [E.BK.HEIGHT_VS_TOLL_PATH, E.BK.HEIGHT_VS_TOLL_VERDICT_PATH,
                                          E.BK.TUNING_RESULT, *E.BK.TUNING_RESULT_FOR.values()]}
    if census != {E._real(T11 / "census")} or E._real(C.OUT) != E._real(T11 / "census"):
        bad.append(f"census roots {sorted(census)} / C.OUT {C.OUT} are not the ONE typed root")
    post_bad = [x for x in N.POST_SHIM if not x.startswith("ok ")]
    rows = [r for r in E.tc10_bindings()
            if r["name"].split(".")[0] in ("tierc10_census", "tierc10_stamps", "tierc10_null")]
    und = [r["name"] for r in rows if r["name"] not in N.NOT_REROOTED]
    r = run_py("import tierc11_nest as N\nprint('{\"ok\": true}')\n")
    rep = [ln for ln in r.stderr.splitlines() if ln.startswith("TC11-AUDIT") or ln.startswith("  ALLOW")]
    allows = {ln.split("ALLOW", 1)[1].strip() for ln in rep if ln.startswith("  ALLOW")}
    blocked = next((m.group(1) for ln in rep for m in [re.search(r"BLOCKED (\d+)", ln)] if m), None)
    fresh_ok = r.returncode == 0 and blocked == "0" and allows <= ALLOWED_NEST_READS
    ok = not bad and not post_bad and not und and fresh_ok
    # the ALLOW COUNT is tree-dependent (the census import reads TUNING_RESULT through the
    # ROOT-relative dir only in the main tree): printed to stdout, never to the transcript
    clock(f"fresh import audit report: {rep[:1]}")
    return ok, (f"{len(DECL_REROOT)} typed re-roots land on their targets ({len(bad)} misses "
                f"{bad[:2]}); one census root research_outputs/tierc11/census; post-shim "
                f"{len(N.POST_SHIM)} clauses, {len(post_bad)} not ok; {len(rows)} TC10 bindings "
                f"left in census/stamps/null, all declared ({len(und)} undeclared {und}); toll "
                f"label {lab!r}; a fresh interpreter importing tierc11_nest: exit {r.returncode}, "
                f"BLOCKED {blocked}, TC10 reads {sorted(allows)} ⊆ the two the nest needs: "
                f"{allows <= ALLOWED_NEST_READS}")


# ═════════════════════════════════════════════════════════════════ F-CAL
def _file_frame(stem: str, lens: str, cut_ms: int) -> pd.DataFrame:
    """The snapshot file read DIRECTLY (1d: Stage D's derived 1d file, which the
    loader HALT-checks equal to the 4h derivation), bars with CLOSE <= cut_ms."""
    p = TC11_SNAP / "klines" / f"{stem}_{lens}.parquet"
    f = pd.read_parquet(p, columns=["open_time", "open", "high", "low", "close"])
    f = f.sort_values("open_time", kind="mergesort").reset_index(drop=True)
    return f[f["open_time"] + LENS_MS[lens] <= cut_ms].reset_index(drop=True)


def _window_grid(f: pd.DataFrame, lens: str) -> dict:
    """ONE window, fresh arrays, fresh engine ATR on THESE bars only, the machine at
    each of the 11 typed scales; the pick by the tie-break typed here."""
    t0 = f["open_time"].to_numpy(np.int64)
    o, h, l, c = (f[k].to_numpy(float).copy() for k in ("open", "high", "low", "close"))
    ts = pd.to_datetime(t0, unit="ms", utc=True).strftime(C.TS_FMT[lens]).tolist()
    atr = N.IND.atr(h, l, c, 14)
    rows = {}
    for s in SCALES:
        m = RC.run_machine((o, h, l, c, ts), atr, RC.macro_pins(s))
        nb, nc = int(m["n_bars"]), int(m["n_confirmed"])
        rows[s] = {"n_bars": nb, "n_confirmed": nc, "density_per_100": 100.0 * nc / nb,
                   "coverage_pct": float(m["coverage_pct"]),
                   "mean_confirmed_lifetime": (NAN if m["mean_confirmed_lifetime"] is None
                                               else float(m["mean_confirmed_lifetime"]))}
    dens = {s: r["density_per_100"] for s, r in rows.items()}
    pick = min(sorted(dens), key=lambda s: (round(abs(dens[s] - DENSITY_TARGET), 9),
                                            abs(s - FROZEN), s))
    return {"bars": int(len(f)), "first_open_ms": int(t0[0]),
            "last_close_ms": int(t0[-1]) + LENS_MS[lens], "rows": rows, "pick": float(pick)}


def _cal_cell(job) -> dict:
    """A fork worker: ONE commission cell recomputed on the independent path."""
    stem, lens = job
    whole = _file_frame(stem, lens, PIN)
    tun = whole[whole["open_time"] + LENS_MS[lens] <= ERA_CUT].reset_index(drop=True)
    tb = int(len(tun))
    win = {"whole": _window_grid(whole, lens)}
    if tb >= MIN_TUNING_BARS:
        win["tuning"] = _window_grid(tun, lens)
        win["first_half"] = _window_grid(tun.head(tb // 2).reset_index(drop=True), lens)
    return {"tuning_bars": tb, "whole_bars": int(len(whole)), "windows": win,
            "tuning_pick": win["tuning"]["pick"] if "tuning" in win else None,
            "whole_tape_pick": win["whole"]["pick"],
            "first_half_pick": win["first_half"]["pick"] if "first_half" in win else None,
            "first_half_bars": tb // 2 if "tuning" in win else None}


_CAL: dict = {}


def cal_indep() -> dict:
    """Every commission cell on the independent path, memoised (exec'd workers; the
    5m cells dealt first so the workers balance).  JSON turns the scale keys into
    text: they are turned back into the typed floats here."""
    if not _CAL:
        order = sorted(COMMISSION, key=lambda x: LENSES7.index(x[1]))
        res = _exec_map("cal", [list(x) for x in order])
        for r in res:
            for w in r["windows"].values():
                w["rows"] = {float(k): v for k, v in w["rows"].items()}
                if sorted(w["rows"]) != list(SCALES):
                    raise RuntimeError("a worker returned a grid off the typed scales")
        _CAL.update(dict(zip(order, res)))
    return _CAL


_GRID: dict = {}


def filed_grid() -> pd.DataFrame:
    """The FILED grid rows.  SCALE_GRID.parquet is gitignored [L-0.5]: in a review
    worktree it is absent, and the rows are REBUILT by the module (N.compute_picks)
    and must hash to the record's content sha before anything is compared with
    them.  Which source was used is a TREE fact: stdout only."""
    if not _GRID:
        if N.GRID_PATH.exists():
            g, how = pd.read_parquet(N.GRID_PATH), "the filed SCALE_GRID.parquet"
        else:
            g, how = N.compute_picks(N.PICK_CELLS, procs=1)["grid"], \
                "REBUILT by N.compute_picks (the parquet is gitignored and absent in this tree)"
        clock(f"F-CAL grid rows: {how}")
        _GRID["g"] = g
    return _GRID["g"]


def _window_of_record(r: dict) -> str:
    return "tuning" if r["tuning_bars"] >= MIN_TUNING_BARS else "whole"


def grid_row_findings(grid: pd.DataFrame, indep: dict) -> list[str]:
    """GRID-ROWS: every filed grid row == the independent machine, cell x window x
    scale: n_bars, n_confirmed, density (filed at 8 dp), coverage, lifetime, the
    window's bars / first open / last close, the window's pick, chosen, the frozen
    flag, the TRUE in-sample text and flags, the window of record."""
    bad = []
    nd = C.ROUND_ND
    rnd = lambda x: float(np.round(np.float64(x), nd))          # noqa: E731  (canon's rounding)
    by = {k: g for k, g in grid.groupby(["asset", "lens", "window"], sort=False)}
    for (s, l), r in indep.items():
        want_w = set(r["windows"])
        got_w = {w for (a, ll, w) in by if a == s and ll == l}
        if got_w != want_w:
            bad.append(f"GRID-ROWS: {s} {l} filed windows {sorted(got_w)} != {sorted(want_w)}")
            continue
        for w, iw in r["windows"].items():
            g = by[(s, l, w)].set_index("scale_mult")
            if sorted(g.index.tolist()) != list(SCALES):
                bad.append(f"GRID-ROWS: {s} {l} {w} scales {sorted(g.index.tolist())}")
                continue
            for sc in SCALES:
                x, y = g.loc[sc], iw["rows"][sc]
                want = {"n_bars": y["n_bars"], "n_confirmed": y["n_confirmed"],
                        "density_per_100": rnd(y["density_per_100"]),
                        "coverage_pct": rnd(y["coverage_pct"]),
                        "mean_confirmed_lifetime": (NAN if y["mean_confirmed_lifetime"] != y["mean_confirmed_lifetime"]
                                                    else rnd(y["mean_confirmed_lifetime"])),
                        "window_bars": iw["bars"], "window_first_open_ms": iw["first_open_ms"],
                        "window_last_close_ms": iw["last_close_ms"], "pick_of_window": iw["pick"],
                        "chosen": sc == iw["pick"], "is_frozen_pin": sc == FROZEN,
                        "calibrated_in_sample": IN_SAMPLE_TEXT[w],
                        "in_sample_tuning": True, "in_sample_holdout": w == "whole",
                        "is_window_of_record": w == _window_of_record(r)}
                diff = [k for k, v in want.items() if not _same(_py(x[k]), v)]
                if diff:
                    bad.append(f"GRID-ROWS: {s} {l} {w} scale {sc}: {diff[:4]} filed "
                               f"{[_py(x[k]) for k in diff[:2]]} vs independent "
                               f"{[want[k] for k in diff[:2]]}")
    return bad


def record_findings(filed: dict, grid: pd.DataFrame, indep: dict) -> list[str]:
    """The record vs the independent path: N.pick_findings (the module's guard,
    fed the INDEPENDENT picks and the commission typed HERE) + the fields it does
    not read (window text, stability, first-half bars, fallback list)."""
    rec_pf = {}
    for (s, l), r in indep.items():
        sub = grid[(grid["asset"] == s) & (grid["lens"] == l)].reset_index(drop=True)
        rec_pf[(s, l)] = {"tuning_bars": r["tuning_bars"], "tuning_pick": r["tuning_pick"],
                          "whole_tape_pick": r["whole_tape_pick"],
                          "first_half_pick": r["first_half_pick"],
                          # the record's per-cell sha vs the FILED rows (record-internal)
                          "grid_sha": C.content_sha(C.canon(sub, N.GRID_KEY))}
    bad = N.pick_findings(filed, rec_pf, commission=COMMISSION)
    by = {(c["asset"], c["lens"]): c for c in filed.get("cells", [])}
    for key, r in indep.items():
        c = by.get(key)
        if c is None:
            continue
        tag = f"{key[0]} {key[1]}"
        fb = r["tuning_bars"] < MIN_TUNING_BARS
        want = {"pick_window": FALLBACK_WINDOW if fb else "tuning",
                "pick_of_record": r["whole_tape_pick"] if fb else r["tuning_pick"],
                "first_half_bars": r["first_half_bars"], "n_bars": r["whole_bars"],
                "in_sample_holdout": fb,
                "stable_first_half_vs_tuning": (None if fb else
                                                r["first_half_pick"] == r["tuning_pick"])}
        diff = [k for k, v in want.items() if not _same(c.get(k), v)]
        if diff:
            bad.append(f"RECORD: {tag} {diff} filed {[c.get(k) for k in diff]} vs independent "
                       f"{[want[k] for k in diff]}")
    fb_list = [f"{s} {l}" for (s, l) in COMMISSION if indep[(s, l)]["tuning_bars"] < MIN_TUNING_BARS]
    if filed.get("fallback_cells") != fb_list or filed.get("n_cells") != N_COMMISSION:
        bad.append(f"RECORD: fallback_cells / n_cells {filed.get('n_cells')} vs typed {N_COMMISSION}")
    if len(grid) != filed.get("grid_rows"):
        bad.append(f"GRID: {len(grid)} rows vs the record's {filed.get('grid_rows')}")
    return bad


_SHA: dict = {}


def _snap_sha(rel: str) -> str:
    if rel not in _SHA:
        _SHA[rel] = N.sha_file(TC11_SNAP / rel)
    return _SHA[rel]


def sources_findings(picks_bytes: bytes, src: dict, manifest: dict, indep: dict) -> list[str]:
    """SOURCES [verifier finding 11]: the sidecar annotates the FILED SCALE_PICKS.json
    bytes; per commission cell (in commission order) the input file named by the
    law typed here, its sha == the snapshot file's sha == STAGE_D_MANIFEST's; the
    HALT-check file likewise; n_bars == the independent whole-tape count."""
    bad = []
    if src.get("annotates_sha256") != sha_bytes(picks_bytes):
        bad.append(f"SOURCES: annotates_sha256 {str(src.get('annotates_sha256'))[:12]}… != "
                   f"sha256(SCALE_PICKS.json) {sha_bytes(picks_bytes)[:12]}…")
    man = {f["path"]: f["sha256"] for f in manifest["files"]}
    cells = src.get("cells", [])
    if [(c["asset"], c["lens"]) for c in cells] != list(COMMISSION):
        bad.append(f"SOURCES: {len(cells)} cells, not the typed commission in its order")
    for c in cells:
        s, l = c["asset"], c["lens"]
        tag = f"{s} {l}"
        want_file = f"klines/{s}_{'4h' if l == '1d' else l}.parquet"
        want_chk = ({f"klines/{s}_1d.parquet"} if l == "1d" else
                    {f"klines/{s}_4h.parquet"} if l == "1w" else set())
        if c["source_file"] != want_file or set(c["checked_against"]) != want_chk:
            bad.append(f"SOURCES: {tag} files {c['source_file']} {sorted(c['checked_against'])}")
            continue
        for rel, sha in [(c["source_file"], c["source_sha256"]), *c["checked_against"].items()]:
            if not (sha == _snap_sha(rel) == man.get(rel)):
                bad.append(f"SOURCES: {tag} {rel} sha {sha} vs snapshot {_snap_sha(rel)} vs "
                           f"STAGE_D_MANIFEST {man.get(rel)}")
        if (s, l) in indep and c["n_bars"] != indep[(s, l)]["whole_bars"]:
            bad.append(f"SOURCES: {tag} n_bars {c['n_bars']} != {indep[(s, l)]['whole_bars']}")
    return bad


LABEL_STEMS = CLASSIC5 + ("ENAUSDT", "DOGEUSDT")
LABEL_INSTANTS = (ERA_CUT - 3_600_000, ERA_CUT, ERA_CUT + 1, PIN)


def _typed_label(indep: dict, s: str, l: str, kind: str) -> dict:
    if kind == "frozen3.0":
        return {"pick_window": "frozen3.0", "fallback": False, "in_sample_holdout": False,
                "stability_changed": None}
    r = indep[(s, l)]
    fb = r["tuning_bars"] < MIN_TUNING_BARS
    return {"pick_window": FALLBACK_WINDOW if fb else "tuning", "fallback": fb,
            "in_sample_holdout": fb,
            "stability_changed": None if fb else r["first_half_pick"] != r["tuning_pick"]}


def _typed_in_sample(lab: dict, t: int) -> bool:
    return lab["pick_window"] != "frozen3.0" and (lab["fallback"] or t <= ERA_CUT)


def label_findings(indep: dict) -> list[str]:
    """LABEL [L-R.2; verifier finding 5]: N.scale_label on every commission cell x
    both kinds == the law typed here from the INDEPENDENT picks; the nest rows of 7
    stems x 2 kinds at 4 instants around the era cut carry, per lens, the typed
    pick_window / scale_in_sample / stability_changed (NA outside the commission);
    every event frame of CLASSIC5 x {4h, 1w} carries scale_in_sample by the typed
    rule at its known instant."""
    bad = []
    for s, l in COMMISSION:
        for kind in ("calibrated", "frozen3.0"):
            got, want = N.scale_label(s, l, kind), _typed_label(indep, s, l, kind)
            if got != want:
                bad.append(f"LABEL: scale_label({s}, {l}, {kind}) {got} != typed {want}")
    inst = np.array(LABEL_INSTANTS, dtype=np.int64)
    n_rows = 0
    for s in LABEL_STEMS:
        for kind in ("calibrated", "frozen3.0"):
            nv = N.nest_at(s, inst, kind)
            for L in NEST5:
                for i, t in enumerate(LABEL_INSTANTS):
                    n_rows += 1
                    got = (_py(nv[f"{L}_pick_window"].iloc[i]), _py(nv[f"{L}_scale_in_sample"].iloc[i]),
                           _py(nv[f"{L}_stability_changed"].iloc[i]))
                    if (s, L) not in COMMISSION:
                        want = (None, None, None)
                    else:
                        lab = _typed_label(indep, s, L, kind)
                        want = (lab["pick_window"], _typed_in_sample(lab, t), lab["stability_changed"])
                    if got != want:
                        bad.append(f"LABEL: nest {s} {kind} {L} at {t}: {got} != typed {want}")
    n_ev = 0
    for s in CLASSIC5:
        for L in ("4h", "1w"):
            lab = _typed_label(indep, s, L, "calibrated")
            tape = N.bundle11(s, L, "calibrated")["tape"]
            for k, f in N.events(s, L, "calibrated").items():
                at = (tape.t0[f["born"].to_numpy(np.int64)] + tape.step if k == "mem"
                      else f["known_close_ms"].to_numpy(np.int64))
                want = np.array([_typed_in_sample(lab, int(t)) for t in at], dtype=bool)
                n_ev += len(f)
                if (not np.array_equal(f["scale_in_sample"].to_numpy(bool), want)
                        or set(f["pick_window"]) - {lab["pick_window"]}):
                    bad.append(f"LABEL: events {s} {L} {k}: scale_in_sample / pick_window")
    _LABEL_N.update({"rows": n_rows, "events": n_ev})
    return bad


_LABEL_N: dict = {}


def cal_break():
    filed = json.loads(N.PICKS_PATH.read_text(encoding="utf-8"))
    indep = cal_indep()
    grid = filed_grid()
    R = {k: {"tuning_bars": r["tuning_bars"], "tuning_pick": r["tuning_pick"],
             "whole_tape_pick": r["whole_tape_pick"], "first_half_pick": r["first_half_pick"],
             "grid_sha": ""} for k, r in indep.items()}

    def whole_as_oos():
        f = copy.deepcopy(filed)
        k = 0
        for c in f["cells"]:
            if c["pick_window"] == "tuning" and c["whole_tape_pick"] != c["tuning_pick"]:
                c["pick_of_record"] = c["tuning_pick"] = c["whole_tape_pick"]
                k += 1
        return [f"({k} cells planted) " + x for x in N.pick_findings(f, R, commission=COMMISSION)
                if "GRID" not in x] if k else []

    def fallback_as_oos():
        f = copy.deepcopy(filed)
        k = 0
        for c in f["cells"]:
            if c["pick_window"] != "tuning":
                c["pick_window"], c["in_sample_holdout"] = "tuning", False
                c["label"] = "OUT-OF-SAMPLE for holdout (tuning-era pick; IN-SAMPLE for tuning)"
                k += 1
        return [f"({k} cells planted) " + x for x in N.pick_findings(f, R, commission=COMMISSION)
                if "GRID" not in x] if k else []

    def dropped():
        f = copy.deepcopy(filed)
        f["cells"] = f["cells"][1:]
        return [x for x in N.pick_findings(f, R, commission=COMMISSION) if "GRID" not in x]

    def grid_bent():
        g = grid.copy()
        i = g.index[(g["asset"] == "BTCUSDT") & (g["lens"] == "4h") & (g["window"] == "tuning")
                    & (g["scale_mult"] == FROZEN)][0]
        g.loc[i, "n_confirmed"] = int(g.loc[i, "n_confirmed"]) + 1
        return grid_row_findings(g, indep)

    def source_bent():
        src = json.loads(N.SOURCES_PATH.read_text(encoding="utf-8"))
        c = src["cells"][3]
        c["source_sha256"] = c["source_sha256"][:-1] + ("0" if c["source_sha256"][-1] != "0" else "1")
        return sources_findings(N.PICKS_PATH.read_bytes(), src, _manifest(), indep)

    def labels_dropped():
        fake = lambda s, l, k: {"pick_window": "tuning", "fallback": False,          # noqa: E731
                                "in_sample_holdout": False, "stability_changed": False}
        for s in CLASSIC5:                  # the event memo is filled with the REAL labels
            for L in ("4h", "1w"):          # first, so the plant cannot leak into it
                N.events(s, L, "calibrated")
        with mutated(N, "scale_label", fake):
            return label_findings(indep)
    return plants([
        ("the WHOLE-TAPE pick filed as the pick of record, labelled out-of-sample",
         "TUNING-HEAD", whole_as_oos),
        ("every in-sample fallback relabelled out-of-sample", "IN-SAMPLE-LABEL", fallback_as_oos),
        ("one cell dropped from the record", "COVERAGE", dropped),
        ("one filed grid row's n_confirmed bent by 1 (BTC 4h tuning, scale 3.0)", "GRID-ROWS",
         grid_bent),
        ("one input sha bent in a copy of the provenance sidecar", "SOURCES", source_bent),
        ("the honesty labels dropped (every lens read as a tuning pick, stable)", "LABEL",
         labels_dropped),
    ])


def _manifest() -> dict:
    return json.loads((T11 / "data" / "STAGE_D_MANIFEST.json").read_text(encoding="utf-8"))


def cal_real():
    pb = N.PICKS_PATH.read_bytes()
    filed = json.loads(pb)
    indep = cal_indep()
    grid = filed_grid()
    bad = []
    if tuple(N.PICK_CELLS) != COMMISSION or len(COMMISSION) != N_COMMISSION:
        bad.append(f"COMMISSION: N.PICK_CELLS ({len(N.PICK_CELLS)}) != the typed commission "
                   f"CLASSIC5 x 7 + UNSEEN12 x 3 = {N_COMMISSION}")
    if tuple(N.UNSEEN12) != UNSEEN12:
        bad.append(f"COMMISSION: N.UNSEEN12 {list(N.UNSEEN12)} != typed")
    gsha = C.content_sha(grid)
    if gsha != filed["grid_content_sha256"]:
        bad.append(f"GRID: SCALE_GRID content sha {gsha[:12]}… != the record's")
    bad += record_findings(filed, grid, indep)
    bad += grid_row_findings(grid, indep)
    src = json.loads(N.SOURCES_PATH.read_text(encoding="utf-8"))
    bad += sources_findings(pb, src, _manifest(), indep)
    bad += label_findings(indep)
    # write-once: a second build is refused (aimed at a temp copy, so a broken
    # guard could never touch the filed artifacts)
    with tempfile.TemporaryDirectory(prefix="tc11cal_") as d:
        (Path(d) / "SCALE_PICKS.json").write_bytes(pb)
        try:
            N.build_picks(out=Path(d))
            refused = "NOT refused"
        except SystemExit as e:
            refused = "refused" if "write-once" in str(e) else f"HALT without write-once: {e}"
    if refused != "refused":
        bad.append(f"WRITE-ONCE: a second build was {refused}")
    cells = filed["cells"]
    fb = [f"{c['asset']} {c['lens']}" for c in cells if c["pick_window"] != "tuning"]
    diff = [f"{c['asset']} {c['lens']} {c['tuning_pick']:g}/{c['whole_tape_pick']:g}"
            for c in cells if c["pick_window"] == "tuning"
            and c["tuning_pick"] != c["whole_tape_pick"]]
    n_grid = sum(len(r["windows"]) * len(SCALES) for r in indep.values())
    n_tun = sum(1 for r in indep.values() if r["tuning_pick"] is not None)
    say(f"      picks filed: {len(cells)} cells ({len(cells) - len(fb)} tuning-era picks, "
        f"{len(fb)} IN-SAMPLE fallbacks: {', '.join(fb)})")
    say(f"      tuning pick != whole-tape pick on {len(diff)} cells: {', '.join(diff)}")
    say(f"      stability (CLASSIC5 x 1h/4h/12h, first half vs tuning) changed on "
        f"{len(filed['stability_changes_classic5_1h_4h_12h'])}: "
        + "; ".join(filed["stability_changes_classic5_1h_4h_12h"]))
    edge = [f"{c['asset']} {c['lens']} {c['pick_of_record']:g}" for c in cells
            if c["pick_at_grid_edge"]]
    say(f"      picks of record at the grid edge (a clamp, not a fit): {', '.join(edge) or 'none'}")
    say(f"      provenance sidecar {N.SOURCES_NAME}: {len(src['cells'])} cells, annotates "
        f"SCALE_PICKS.json sha256 {src['annotates_sha256'][:16]}…; {len(_SHA)} distinct input "
        f"files hashed here == STAGE_D_MANIFEST")
    return (not bad), (
        f"{len(indep)} cells ({N_COMMISSION} typed = 5 x 7 + 12 x 3) recomputed on the "
        f"INDEPENDENT path (snapshot files, tuning = bars with close <= {ERA_CUT}, fresh ATR, "
        f"RC.run_machine at the 11 typed scales, the typed tie-break): {n_tun} tuning picks and "
        f"{len(indep) - n_tun} whole-tape fallbacks labelled IN-SAMPLE reproduce, every "
        f"whole-tape / first-half pick and stability flag reproduces, {n_grid} filed grid rows == "
        f"the independent machine (n_confirmed, density, coverage, lifetime, window facts, true "
        f"in-sample text); SCALE_GRID content sha {gsha[:16]}… == the record's; the sidecar's "
        f"input shas == the snapshot == STAGE_D_MANIFEST; honesty labels on {_LABEL_N.get('rows')} "
        f"nest lens-rows and {_LABEL_N.get('events')} event rows == the typed law; a second build "
        f"{refused} (write-once) — {len(bad)} findings {bad[:3]}")


# ═════════════════════════════════════════════════════════════ F-NEST-ASOF
ASOF_RANDOM = 16
ASOF_AIM_EACH = 6                      # x 4 classes: hardens, confirms, deaths, flip holds
ASOF_MIN_CUTS = 40
ASOF_MIN_BARS = 30                     # every lens prefix holds at least this many bars
# (law, the VIEW the law reads, whether the READER is the pre-repair deviation reset)
ASOF_LAWS = ("honest", "leaked-redraw", "flip-at-stamp", "top-bot-swapped", "dev-reset")
VIEW_OF_LAW = {"honest": "honest", "leaked-redraw": "leaked-redraw",
               "flip-at-stamp": "flip-at-stamp", "top-bot-swapped": "top-bot-swapped",
               "dev-reset": "honest"}
EVENT_KEYS = ("deaths", "hardens", "scan", "scan_mem")
ORACLE_FIELDS = ("state", "in_range", "top", "bot", "pct", "dist_signed_atr", "near_side",
                 "bnd_age", "dev_top", "dev_bot", "flip_pol", "flip_age", "atr_L",
                 "coin_top", "coin_bot", "coin_top_mem", "coin_bot_mem")


def _rederive(tape, v: dict) -> dict:
    with np.errstate(invalid="ignore", divide="ignore"):
        v["pct"] = 100.0 * (tape.c - v["bot"]) / (v["top"] - v["bot"])
        d_top, d_bot = np.abs(v["top"] - tape.c), np.abs(tape.c - v["bot"])
        v["dist_atr"] = np.minimum(d_top, d_bot) / tape.atr
        v["near_side"] = np.where(v["in_range"], np.where(d_top <= d_bot, 1, -1), 0).astype(np.int8)
    return v


def law_view(tape, v2: dict, view: dict, law: str) -> dict:
    """The honest view, or a LEAKY / WRONG READER of the same run (a copy)."""
    law = VIEW_OF_LAW[law]
    if law == "honest":
        return view
    v = dict(view)
    n = tape.n
    if law == "leaked-redraw":              # the as-of bounds read off Range.top/.bottom
        v["top"], v["bot"] = view["top"].copy(), view["bot"].copy()
        for r in v2["macro"]["ranges"]:
            if r.confirm_i >= 0:
                b = r.die_i if r.die_i >= 0 else n
                v["top"][r.confirm_i:b], v["bot"][r.confirm_i:b] = r.top, r.bottom
        return _rederive(tape, v)
    if law == "flip-at-stamp":              # a flip read at its touch bar, not touch + 6
        lf = C.leash_frame(v2["leash"], MEM_HOLD)
        fl = lf[lf["event"] == "flip"].sort_values(["i", "pos"], kind="mergesort")
        pol = [1 if s == "top" else -1 for s in fl["side"]]
        v["flip_pol"] = C._step_fill(n, list(zip(fl["i"].tolist(), pol)), 0, np.int8)
        known = C._step_fill(n, list(zip(fl["i"].tolist(), fl["i"].tolist())), -1, np.int64)
        v["flip_age"] = np.where(known >= 0, np.arange(n) - known, -1)
        return v
    if law == "top-bot-swapped":            # CAUSAL but WRONG: top and bottom read crossed
        v["top"], v["bot"] = view["bot"].copy(), view["top"].copy()
        return _rederive(tape, v)
    raise ValueError(law)


def _dev_reset(view: dict):
    """The PRE-REPAIR reader: out of range, deviations read the view's reset 0."""
    return (np.asarray(view["dev_top"], dtype=np.int64), np.asarray(view["dev_bot"], dtype=np.int64))


@contextlib.contextmanager
def reader_of(law: str):
    if law == "dev-reset":
        with mutated(N, "_dev_carry", _dev_reset):
            yield
    else:
        yield


def machine_oracle(p, pv2: dict) -> dict:
    """THE END-OF-PREFIX MACHINE ANSWER of one lens (the prefix run's own objects,
    which at the end of the prefix ARE as-of): the live range (state CONFIRMED)
    top / bottom; final_state; harden counts of the live range, or out of range of
    the last DEAD confirmed range (the carry); the last flip KNOWN (touch + 6 <=
    the last bar); the untouched memory lines (dead confirmed ranges' lines with no
    leash event yet).  Typed from the machine's objects, not from the as-of view."""
    macro = pv2["macro"]
    k = p.n - 1
    live = [r for r in macro["ranges"] if r.confirm_i >= 0 and r.state == "CONFIRMED"]
    dead = [r for r in macro["ranges"] if r.confirm_i >= 0 and r.state == "DEAD"]
    hard: dict = {}
    for e in macro["events"]:
        if e["event"] == "harden":
            hard.setdefault((int(e["rid"]), str(e["side"])), []).append(int(e["i"]))
    r = live[0] if len(live) == 1 else None
    src = r if r is not None else (max(dead, key=lambda x: x.die_i) if dead else None)
    o = {"n_live": len(live), "atr_L": float(p.atr[k]),
         "dev_top": len(hard.get((src.rid, "top"), ())) if src is not None else 0,
         "dev_bot": len(hard.get((src.rid, "bottom"), ())) if src is not None else 0}
    c = float(p.c[k])
    if r is not None:
        top, bot = float(r.top), float(r.bottom)
        dt, db = abs(top - c), abs(c - bot)
        near = 1 if dt <= db else -1
        since = max([int(r.confirm_i)] + hard.get((r.rid, "top" if near == 1 else "bottom"), []))
        o.update({"state": "IN_RANGE", "in_range": True, "top": top, "bot": bot,
                  "pct": 100.0 * (c - bot) / (top - bot),
                  "dist_signed_atr": (1.0 if bot <= c <= top else -1.0) * (min(dt, db) / o["atr_L"]),
                  "near_side": near, "bnd_age": k - since})
    else:
        o.update({"state": {"NEUTRAL": "NONE", "BULL_EXP": "BULL_EXP",
                            "BEAR_EXP": "BEAR_EXP"}[macro["final_state"]],
                  "in_range": False, "top": NAN, "bot": NAN, "pct": NAN, "dist_signed_atr": NAN,
                  "near_side": 0, "bnd_age": None})
    flips = [(int(e["i"]) + MEM_HOLD, pos, str(e["side"])) for pos, e in enumerate(pv2["leash"])
             if e["event"] == "flip" and int(e["i"]) + MEM_HOLD <= k]
    if flips:
        kn, _, sd = max(flips)
        o["flip_pol"], o["flip_age"] = (1 if sd == "top" else -1), k - kn
    else:
        o["flip_pol"], o["flip_age"] = 0, -1
    touched = {(int(e["rid"]), str(e["side"])) for e in pv2["leash"]}
    o["mem"] = ([float(x.top) for x in dead if x.confirm_i <= x.die_i - 1
                 and (x.rid, "top") not in touched]
                + [float(x.bottom) for x in dead if x.confirm_i <= x.die_i - 1
                   and (x.rid, "bottom") not in touched])
    return o


def oracle_coin(oL: dict, oU: dict | None) -> dict:
    """Coincidence typed HERE from two end-of-prefix machine answers (0.25 x ATR_L,
    inclusive, all four pairings; the twin admits U's untouched memory lines)."""
    if oU is None:
        return {k: None for k in ("coin_top", "coin_bot", "coin_top_mem", "coin_bot_mem")}
    thr = COIN * oL["atr_L"]
    inL, inU = oL["in_range"], oU["in_range"]
    near = lambda x, ys: any(x == x and y == y and abs(x - y) <= thr for y in ys)   # noqa: E731
    ct = inL and inU and near(oL["top"], (oU["top"], oU["bot"]))
    cb = inL and inU and near(oL["bot"], (oU["top"], oU["bot"]))
    return {"coin_top": ct, "coin_bot": cb,
            "coin_top_mem": ct or (inL and near(oL["top"], oU["mem"])),
            "coin_bot_mem": cb or (inL and near(oL["bot"], oU["mem"]))}


def _mem_known(m: pd.DataFrame, t: int) -> pd.DataFrame:
    """The memory lines known by bar t - 1: born by then; an end (and its reason)
    that falls at or after t is not yet known — end_live clipped to t, reason
    'open'."""
    m = m[m["born"] <= t - 1].copy()
    later = m["end_live"].to_numpy(np.int64) >= t
    m["end_live"] = np.minimum(m["end_live"].to_numpy(np.int64), t)
    m.loc[later, "end_reason"] = "open"
    return m.reset_index(drop=True)


def _events_known(b: dict, t: int) -> dict:
    """The event frames of a bundle restricted to what is known by bar t - 1."""
    out = {"deaths": N.deaths_of(b), "hardens": N.hardens_of(b), "scan": N.scan_bands_of(b),
           "scan_mem": N.scan_memory_of(b)}
    out = {k: v[v["known_at"] <= t - 1].reset_index(drop=True) for k, v in out.items()}
    out["mem"] = _mem_known(b["mem"], t)
    return out


def _frame_diff(a: pd.DataFrame, b: pd.DataFrame) -> list[str]:
    """Columns that differ (NA-aware, EXACT — floats included)."""
    if list(a.columns) != list(b.columns) or len(a) != len(b):
        return [f"shape {a.shape} vs {b.shape}"]
    out = []
    for col in a.columns:
        x, y = a[col], b[col]
        xn, yn = x.isna().to_numpy(), y.isna().to_numpy()
        if not np.array_equal(xn, yn):
            out.append(col)
            continue
        xv = x[~xn].to_numpy(dtype=object)
        yv = y[~yn].to_numpy(dtype=object)
        if not all(p == q for p, q in zip(xv, yv)):
            out.append(col)
    return out


def _cut_instants(stem: str, lens: str, full: dict, t_min: int, rng) -> list[tuple[int, str]]:
    b = full[lens]
    tape, v2 = b["tape"], b["v2"]
    close = lambda i: int(tape.t0[i]) + tape.step                  # noqa: E731
    conf = [r.confirm_i for r in v2["macro"]["ranges"] if r.confirm_i >= 1]
    flips = [int(e["i"]) for e in v2["leash"] if e["event"] == "flip"]
    classes = {
        "harden": [close(i + dx) for i, _, _ in b["hardens"] for dx in (-1, 0) if i + dx >= 0],
        "confirm": [close(i + dx) for i in conf for dx in (-1, 0)],
        "death": [close(i + dx) for i, _, _ in b["dies"] for dx in (-1, 0) if i + dx >= 0],
        "flip-hold": [close(i + dx) for i in flips for dx in range(0, MEM_HOLD)
                      if i + dx < tape.n],
    }
    cuts: dict = {}
    for tag, xs in classes.items():
        xs = sorted({x for x in xs if t_min <= x <= PIN})
        if xs:
            for j in sorted(rng.choice(len(xs), size=min(ASOF_AIM_EACH, len(xs)), replace=False)):
                cuts.setdefault(int(xs[j]), tag)
    k = 0
    while k < ASOF_RANDOM or len(cuts) < ASOF_MIN_CUTS:
        cuts.setdefault(int(rng.integers(t_min, PIN + 1)), "random")
        k += 1
    return sorted(cuts.items())


def _nest(bundles: dict, inst, law: str) -> pd.DataFrame:
    with reader_of(law):
        return N.nest_from_bundles(bundles, inst)


def asof_asset(ai: int, stem: str) -> dict:
    """One CLASSIC5 asset: every nest lens's cuts; per law the prefix-vs-full
    comparison AND the full-run vector at the cut vs the machine oracle."""
    scale = {L: N.scale_of(stem, L, "calibrated") for L in NEST5}
    full_honest = {L: N.bundle11(stem, L, "calibrated") for L in NEST5}
    full = {law: {L: (full_honest[L] if VIEW_OF_LAW[law] == "honest" else
                      N.bundle_of(full_honest[L]["tape"], full_honest[L]["v2"],
                                  law_view(full_honest[L]["tape"], full_honest[L]["v2"],
                                           full_honest[L]["view"], law)))
                  for L in NEST5} for law in ASOF_LAWS}
    t_min = max(int(full_honest[L]["tape"].t0[ASOF_MIN_BARS - 1]) + LENS_MS[L] for L in NEST5)
    ev_full = {L: _events_known(full_honest[L], full_honest[L]["tape"].n) for L in NEST5}
    stat = {"cuts": {}, "aims": {}, "bad": {law: [] for law in ASOF_LAWS},
            "oracle_bad": {law: [] for law in ASOF_LAWS},
            "caught_lens": {law: {} for law in ASOF_LAWS}, "arrays": 0, "events": 0,
            "instants": 0, "oracle": 0, "oracle_out_of_range_carried": 0}
    for li, lens in enumerate(NEST5):
        rng = np.random.default_rng([SEED, ai, li])
        cuts = _cut_instants(stem, lens, full_honest, t_min, rng)
        stat["cuts"][lens] = len(cuts)
        for T, tag in cuts:
            stat["aims"][tag] = stat["aims"].get(tag, 0) + 1
            pre = {law: {} for law in ASOF_LAWS}
            ts, orc = {}, {}
            for L in NEST5:
                tape = full_honest[L]["tape"]
                t = int(C.asof_index(tape, T)) + 1
                ts[L] = t
                p = tape.head(t)
                pv2 = C.run_scale(p, scale[L])
                pview = C.asof_view(p, pv2["macro"], pv2["leash"])
                honest_pre = N.bundle_of(p, pv2, pview)
                for law in ASOF_LAWS:
                    pre[law][L] = (honest_pre if VIEW_OF_LAW[law] == "honest" else
                                   N.bundle_of(p, pv2, law_view(p, pv2, pview, law)))
                orc[L] = machine_oracle(p, pv2)
                fv = full_honest[L]["view"]
                for name in C.ASOF_ARRAYS:          # TC10's F-RNG-ASOF law, per lens
                    stat["arrays"] += 1
                    if not np.array_equal(fv[name][:t], pview[name], equal_nan=True):
                        stat["bad"]["honest"].append(f"{stem} {lens} cut {T} ({tag}): {L} "
                                                     f"as-of array `{name}`")
                pe = _events_known(honest_pre, t)
                fe = {k: (v[v["known_at"] <= t - 1].reset_index(drop=True) if k != "mem" else
                          _mem_known(full_honest[L]["mem"], t))
                      for k, v in ev_full[L].items()}
                for k in (*EVENT_KEYS, "mem"):
                    stat["events"] += len(pe[k])
                    dcols = _frame_diff(pe[k], fe[k])
                    if dcols:
                        stat["bad"]["honest"].append(f"{stem} {lens} cut {T} ({tag}): {L} "
                                                     f"events `{k}` {dcols[:3]}")
            for L in NEST5:
                if orc[L]["n_live"] > 1:
                    stat["oracle_bad"]["honest"].append(f"machine oracle: {stem} cut {T}: {L} "
                                                        f"{orc[L]['n_live']} live ranges")
                orc[L].update(oracle_coin(orc[L], orc[LADDER[L]] if LADDER[L] else None))
                if not orc[L]["in_range"] and (orc[L]["dev_top"] or orc[L]["dev_bot"]):
                    stat["oracle_out_of_range_carried"] += 1
            inst = {T}
            for L in NEST5:
                tape = full_honest[L]["tape"]
                for q in range(max(0, ts[L] - 3), ts[L]):
                    inst.add(int(tape.t0[q]) + tape.step)
            inst = sorted(inst)
            iT = inst.index(T)
            stat["instants"] += len(inst)
            for law in ASOF_LAWS:
                nf = _nest(full[law], inst, law)
                d = _frame_diff(nf, _nest(pre[law], inst, law))
                if d:
                    stat["bad"][law].append(f"{stem} {lens} cut {T} ({tag}): nest vector "
                                            f"columns {d[:4]}")
                    stat["caught_lens"][law][lens] = stat["caught_lens"][law].get(lens, 0) + 1
                row = nf.iloc[iT]
                for L in NEST5:
                    if law == "honest":
                        stat["oracle"] += 1
                    wrong = [f for f in ORACLE_FIELDS if not _same(_py(row[f"{L}_{f}"]), orc[L][f])]
                    if wrong:
                        stat["oracle_bad"][law].append(
                            f"machine oracle: {stem} {lens} cut {T} ({tag}): {L} {wrong[:4]} "
                            f"nest {[_py(row[f'{L}_{f}']) for f in wrong[:2]]} vs end-of-prefix "
                            f"machine {[orc[L][f] for f in wrong[:2]]}")
    return stat


_ASOF: dict = {}


def asof_corpus() -> dict:
    """ONE pass, memoised: every asset's cuts, one exec'd worker per asset.  Each
    asset's cuts are seeded by (SEED, asset index, lens index), so the result does
    not depend on the pool."""
    if not _ASOF:
        res = _exec_map("asof", [[ai, s] for ai, s in enumerate(CLASSIC5)], procs=len(CLASSIC5))
        _ASOF.update(dict(zip(CLASSIC5, res)))
    return _ASOF


def asof_break():
    A = asof_corpus()

    def plant(law, kind):
        key, other = ("bad", "oracle_bad") if kind == "prefix" else ("oracle_bad", "bad")
        miss = [s for s in CLASSIC5 if not A[s][key][law]]
        if miss:                        # a leak one asset lets through is a leak
            return []                   # the fixture cannot see
        n = sum(len(A[s][key][law]) for s in CLASSIC5)
        n_o = sum(len(A[s][other][law]) for s in CLASSIC5)
        head = "nest vector" if kind == "prefix" else "machine oracle"
        return [f"{head} RED on all {len(CLASSIC5)} assets ({n} cut-lens readings; the "
                f"{'oracle' if kind == 'prefix' else 'prefix check'} saw {n_o}), e.g. "
                f"{A[CLASSIC5[0]][key][law][0]}"]
    return plants([
        ("LEAKED REDRAW (top / bot read off Range.top / .bottom — end-of-run values)",
         "nest vector", lambda: plant("leaked-redraw", "prefix")),
        ("FLIP AT ITS STAMP BAR (flip polarity / age from the touch bar, not touch + 6)",
         "nest vector", lambda: plant("flip-at-stamp", "prefix")),
        ("TOP / BOTTOM SWAPPED (a CAUSAL but wrong reader: prefix-invariant by construction)",
         "machine oracle", lambda: plant("top-bot-swapped", "oracle")),
        ("DEVIATIONS RESET out of range (the PRE-REPAIR reader; causal, so prefix-invariant)",
         "machine oracle", lambda: plant("dev-reset", "oracle")),
    ])


def asof_real():
    A = asof_corpus()
    bad = [x for s in CLASSIC5 for x in A[s]["bad"]["honest"]]
    obad = [x for s in CLASSIC5 for x in A[s]["oracle_bad"]["honest"]]
    n_cuts = sum(sum(A[s]["cuts"].values()) for s in CLASSIC5)
    n_or = sum(A[s]["oracle"] for s in CLASSIC5)
    n_carry = sum(A[s]["oracle_out_of_range_carried"] for s in CLASSIC5)
    for s in CLASSIC5:
        st = A[s]
        say(f"      {s}: cuts per lens {st['cuts']} · aimed {dict(sorted(st['aims'].items()))} · "
            f"{st['instants']} instants compared · {st['arrays']} as-of arrays · "
            f"{st['events']} events known by the cut · {st['oracle']} oracle lens-readings "
            f"({st['oracle_out_of_range_carried']} out of range with carried deviations) · "
            f"honest mismatches {len(st['bad']['honest'])} / oracle {len(st['oracle_bad']['honest'])}")
    mn = min(min(A[s]["cuts"].values()) for s in CLASSIC5)
    say("      scale HELD at the filed pick (SCALE_PICKS.json) on every prefix: this fixture "
        "does NOT test the pick — the pick is a pin, fitted once [L-R.5].")
    return (not bad and not obad and mn >= ASOF_MIN_CUTS and n_carry > 0), (
        f"{n_cuts} cuts over {len(CLASSIC5)} CLASSIC5 assets x {len(NEST5)} nest lenses (min "
        f"{mn} per lens; seeded random mid-bar instants + aimed at hardens, confirms, deaths and "
        f"flip hold windows), every lens cut at the one instant: the prefix nest vector == the "
        f"full-run nest vector at the cut and at each lens's last three closes, every lens's "
        f"{len(C.ASOF_ARRAYS)} as-of arrays == full[:t], the death / harden / memory-line / "
        f"scan frames known by the cut == the full run's; and at every cut every lens's "
        f"{len(ORACLE_FIELDS)} fields == the END-OF-PREFIX MACHINE ORACLE ({n_or} lens-readings, "
        f"{n_carry} of them out of range with carried deviations) — "
        + ("0 mismatches" if not (bad or obad) else
           f"{len(bad)} prefix / {len(obad)} oracle mismatches: " + "; ".join((bad + obad)[:3])))


# ═══════════════════════════════════════════════════════════════ F-EQ-SCAN
def _typed_ema(c: list, p: int) -> list:
    """EMA of close typed HERE: seeded at the first close, alpha 2 / (p + 1); NaN
    over the first p bars (the warm-up law)."""
    a = 2.0 / (p + 1.0)
    out, prev = [], None
    for v in c:
        prev = v if prev is None else prev + a * (v - prev)
        out.append(prev)
    for i in range(min(p, len(out))):
        out[i] = NAN
    return out


def _typed_dies(macro: dict) -> list:
    return sorted(((int(e["i"]), int(e["rid"]), str(e["side"])) for e in macro["events"]
                   if e["event"] == "breakout-die"), key=lambda x: x[0])


def plain_band_scan(band: str, h: list, l: list, c: list, atr: list, dies: list,
                    line: list, n: int) -> list:
    """THE FIRST RETEST THAT HOLDS, plain loops [L-R.6(a)], typed HERE: per DIE, bars
    in (d, min(d + 400, next - 1, n - 1)] in order; a touch meets the line and its
    PRIOR close sat beyond it on the die side; hold = no close through by 1.0 ATR
    over touch..touch + 3 (an unreadable line fails); truncated when touch + 3 >= n;
    stop at the first non-failed verdict."""
    rows = []
    for q, (d, rid, side) in enumerate(dies):
        nxt = dies[q + 1][0] if q + 1 < len(dies) else n
        end = min(d + RETEST_TTL, nxt - 1, n - 1)
        seq = 0
        for j in range(d + 1, end + 1):
            b = line[j]
            if not (l[j] <= b and h[j] >= b):
                continue
            if not ((c[j - 1] > line[j - 1]) if side == "top" else (c[j - 1] < line[j - 1])):
                continue
            if j + RETEST_HOLD >= n:
                v = "truncated"
            else:
                v = "hold"
                for k in range(j, j + RETEST_HOLD + 1):
                    bk = line[k]
                    if bk != bk or ((c[k] < bk - RETEST_MARGIN * atr[k]) if side == "top"
                                    else (c[k] > bk + RETEST_MARGIN * atr[k])):
                        v = "failed"
                        break
            rows.append((band, d, rid, side, 1 if side == "top" else -1, seq, j,
                         j + RETEST_HOLD, v, v == "hold"))
            seq += 1
            if v != "failed":
                break
    return rows


def plain_mem_scan(h: list, l: list, c: list, atr: list, dies: list, macro: dict,
                   leash: list, n: int) -> list:
    """THE MEMORY LINE, plain loops [R-SCAN-2], typed HERE: the dead range's broken-
    side line (the machine's own Range boundary of a DEAD range — its end-of-life
    line; none if the range was not confirmed by die - 1); bars in (d, min(d + 400,
    next - 1, n - 1)], before the line's first expiry; the bar CONTAINS the line and
    the prior close sat strictly beyond it; hold = no close through by 1.0 ATR over
    touch..touch + 6; truncated when touch + 6 >= n."""
    by = {r.rid: r for r in macro["ranges"]}
    exp: dict = {}
    for e in leash:
        if e["event"] == "line-expired":
            exp.setdefault((int(e["rid"]), str(e["side"])), int(e["i"]))
    rows = []
    for q, (d, rid, side) in enumerate(dies):
        nxt = dies[q + 1][0] if q + 1 < len(dies) else n
        end = min(d + MEM_TTL, nxt - 1, n - 1)
        r = by[rid]
        if end <= d or not (0 <= r.confirm_i <= d - 1):
            continue
        px = float(r.top) if side == "top" else float(r.bottom)
        e_i = exp.get((rid, side), n + 10**9)
        seq = 0
        for j in range(d + 1, end + 1):
            if j >= e_i:
                break
            if not (l[j] <= px <= h[j]):
                continue
            if not ((c[j - 1] > px) if side == "top" else (c[j - 1] < px)):
                continue
            if j + MEM_HOLD >= n:
                v = "truncated"
            else:
                v = "hold"
                for k in range(j, j + MEM_HOLD + 1):
                    thr = MEM_MARGIN * atr[k]
                    if (c[k] < px - thr) if side == "top" else (c[k] > px + thr):
                        v = "failed"
                        break
            rows.append(("memory-line", d, rid, side, 1 if side == "top" else -1, seq, j,
                         j + MEM_HOLD, v, v == "hold", px))
            seq += 1
            if v != "failed":
                break
    return rows


_SCAN_TUP = ["band", "die_i", "rid", "side", "dir", "seq", "touch_i", "known_at", "verdict",
             "is_first_hold"]


def _rows_of(f: pd.DataFrame, with_px: bool = False) -> list:
    cols = _SCAN_TUP + (["px"] if with_px else [])
    return [tuple(_py(x) for x in t) for t in f[cols].itertuples(index=False, name=None)]


def _rows_diff(tag: str, mod: list, plain: list) -> list[str]:
    if mod == plain:
        return []
    k = next((i for i in range(min(len(mod), len(plain))) if mod[i] != plain[i]),
             min(len(mod), len(plain)))
    return [f"SCAN-ROWS: {tag}: {len(mod)} module rows vs {len(plain)} plain-loop rows; first "
            f"difference at row {k}: {mod[k] if k < len(mod) else None} vs "
            f"{plain[k] if k < len(plain) else None}"]


def _scan_law_bad(sc: pd.DataFrame) -> list[str]:
    """The scan's own law, per (band, DIE): seq 0..k-1 contiguous, touches strictly
    rising, every row but the last 'failed', at most one hold and only last."""
    out = []
    for (band, d), g in sc.groupby(["band", "die_i"], sort=False):
        v = g["verdict"].tolist()
        if g["seq"].tolist() != list(range(len(g))) or not np.all(np.diff(g["touch_i"]) > 0):
            out.append(f"{band} die {d}: seq/touch order")
        if any(x != "failed" for x in v[:-1]):
            out.append(f"{band} die {d}: a non-failed row before the last {v}")
        if g["is_first_hold"].sum() != (v[-1] == "hold"):
            out.append(f"{band} die {d}: first-hold flag")
    return out


def eq_cell(stem: str, lens: str, kind: str) -> dict:
    b = N.bundle11(stem, lens, kind)
    tape, v2 = b["tape"], b["v2"]
    rp = C.RETEST_PINS
    sc = N.scan_bands_of(b)
    st = {"dies": len(b["dies"]), "evaluated": 0, "oneshot_hold": 0, "scan_hold": 0,
          "rescued": 0, "rows": len(sc), "mem_agree": 0, "mem_outside": 0, "plain_rows": 0,
          "mem_rows": 0, "mem_hold": 0, "mem_rescued": 0}
    bad = [f"{stem} {lens} {kind}: LAW {x}" for x in _scan_law_bad(sc)]
    h, l, c, atr, n = tape.h.tolist(), tape.l.tolist(), tape.c.tolist(), tape.atr.tolist(), tape.n
    dies = _typed_dies(v2["macro"])
    if dies != list(b["dies"]):
        bad.append(f"{stem} {lens} {kind}: the machine's breakout-die events != the bundle's DIEs")
    for band, period in BANDS:
        lo, hi = C.band_of(band)(tape.c)
        one = C.retest_holds(tape, b["dies"], lo, hi, float(rp["margin_atr"]),
                             int(rp["hold_bars"]), int(rp["ttl_bars"]))
        _, tally = E.BK.band_hold_candidates(tape.h, tape.l, tape.c, tape.atr, b["dies"], lo, hi,
                                             float(rp["margin_atr"]), int(rp["hold_bars"]),
                                             int(rp["ttl_bars"]))
        g = sc[(sc["band"] == band) & (sc["seq"] == 0)]
        first = [{"rid": int(r.rid), "side": r.side, "die_i": int(r.die_i), "touch_i": int(r.touch_i),
                  "known_at": int(r.known_at), "verdict": r.verdict} for r in g.itertuples()]
        if first != one:
            k = next((i for i in range(min(len(first), len(one))) if first[i] != one[i]),
                     min(len(first), len(one)))
            bad.append(f"{stem} {lens} {kind} {band}: first evaluated row per DIE != "
                       f"C.retest_holds ({len(first)} vs {len(one)} rows; first difference at "
                       f"{k}: {first[k] if k < len(first) else None} vs "
                       f"{one[k] if k < len(one) else None})")
        if first != tally["rows"]:
            bad.append(f"{stem} {lens} {kind} {band}: first evaluated row per DIE != "
                       f"BK.band_hold_candidates ({len(first)} vs {len(tally['rows'])})")
        plain = plain_band_scan(band, h, l, c, atr, dies, _typed_ema(c, period), n)
        bad += _rows_diff(f"{stem} {lens} {kind} {band}", _rows_of(sc[sc["band"] == band]), plain)
        st["plain_rows"] += len(plain)
        st["evaluated"] += len(one)
        st["oneshot_hold"] += sum(1 for r in one if r["verdict"] == "hold")
        st["scan_hold"] += sum(1 for r in plain if r[8] == "hold")
        st["rescued"] += sum(1 for r in plain if r[8] == "hold" and r[5] > 0)
    sm = N.scan_memory_of(b)
    bad += [f"{stem} {lens} {kind}: LAW {x}" for x in _scan_law_bad(sm)]
    pm = plain_mem_scan(h, l, c, atr, dies, v2["macro"], v2["leash"], n)
    bad += _rows_diff(f"{stem} {lens} {kind} memory-line", _rows_of(sm, with_px=True), pm)
    st["mem_rows"] += len(pm)
    st["mem_hold"] += sum(1 for r in pm if r[8] == "hold")
    st["mem_rescued"] += sum(1 for r in pm if r[8] == "hold" and r[5] > 0)
    om = N.oneshot_memory_of(b).set_index("die_i")
    f0 = sm[sm["seq"] == 0].set_index("die_i")
    for q, (d, rid, side) in enumerate(dies):
        nxt = dies[q + 1][0] if q + 1 < len(dies) else n
        end = min(d + MEM_TTL, nxt - 1, n - 1)
        e = om.loc[d] if d in om.index else None
        f = f0.loc[d] if d in f0.index else None
        if e is not None and int(e["touch_i"]) <= end:
            if f is None or int(f["touch_i"]) != int(e["touch_i"]) or f["verdict"] != e["verdict"]:
                bad.append(f"{stem} {lens} {kind} memory-line die {d}: scan first row "
                           f"{None if f is None else (int(f['touch_i']), f['verdict'])} != the "
                           f"engine's one-shot flip ({int(e['touch_i'])}, {e['verdict']})")
            else:
                st["mem_agree"] += 1
        else:
            st["mem_outside"] += 1
            if f is not None:
                bad.append(f"{stem} {lens} {kind} memory-line die {d}: a scan row with no "
                           f"in-window engine evaluation")
    return {"bad": bad, "stat": st}


EQ_CELLS = tuple((stem, lens, kind) for lens in LENSES7 for stem in CLASSIC5
                 for kind in ("calibrated", "frozen3.0"))


def eq_all(first_finding: bool = False) -> tuple[list[str], dict]:
    """Every CLASSIC5 asset x 7 lenses x 2 kinds.  first_finding=True (a break
    leg, IN-PROCESS so the plant is live) walks the coarse lenses first and stops
    at the first cell with a finding; otherwise a fork pool, the 5m cells first."""
    bad, tot = [], {}
    if first_finding:
        for stem, lens, kind in sorted(EQ_CELLS, key=lambda x: -LENSES7.index(x[1])):
            r = eq_cell(stem, lens, kind)
            if r["bad"]:
                return r["bad"], tot
        return bad, tot
    jobs = sorted(EQ_CELLS, key=lambda x: LENSES7.index(x[1]))
    for (stem, lens, kind), r in zip(jobs, _exec_map("eq", [list(j) for j in jobs])):
        bad += r["bad"]
        for k, v in r["stat"].items():
            tot[(lens, kind, k)] = tot.get((lens, kind, k), 0) + v
    return bad, tot


def eq_break():
    orig_t, orig_m = N._qualifying_touches, N._mem_touches

    def tap(fn):
        def run():
            with mutated(N, "_qualifying_touches", fn):
                return eq_all(first_finding=True)[0]
        return run

    def mem(fn):
        def run():
            with mutated(N, "_mem_touches", fn):
                return eq_all(first_finding=True)[0]
        return run
    skip2 = lambda w: np.concatenate([w[:1], w[2:]])                     # noqa: E731
    return plants([
        ("taps: a scan that SKIPS the first qualifying touch",
         "first evaluated row per DIE != C.retest_holds",
         tap(lambda *a: orig_t(*a)[1:])),
        ("taps: the ONE-SHOT rule (the scan stops after the first touch, whatever its verdict)",
         "SCAN-ROWS", tap(lambda *a: orig_t(*a)[:1])),
        ("taps: the SECOND qualifying touch skipped", "SCAN-ROWS",
         tap(lambda *a: skip2(orig_t(*a)))),
        ("memory line: the ONE-SHOT rule", "SCAN-ROWS", mem(lambda *a: orig_m(*a)[:1])),
        ("memory line: the SECOND qualifying touch skipped", "SCAN-ROWS",
         mem(lambda *a: skip2(orig_m(*a)))),
    ])


def eq_real():
    bad, tot = eq_all()
    if tuple(N.SCAN_BANDS) != tuple(b for b, _ in BANDS):
        bad.append(f"BANDS: N.SCAN_BANDS {list(N.SCAN_BANDS)} != typed {[b for b, _ in BANDS]}")
    g = lambda lens, kind, k: tot[(lens, kind, k)]                          # noqa: E731
    for kind in ("calibrated", "frozen3.0"):
        for lens in LENSES7:
            say(f"      {kind:>10} {lens:>3}: {g(lens, kind, 'dies')} DIEs · taps 89/127/200: "
                f"{g(lens, kind, 'rows')} scan rows == the plain loop's {g(lens, kind, 'plain_rows')} · "
                f"{g(lens, kind, 'evaluated')} one-shot rows == the scan's first rows · one-shot holds "
                f"{g(lens, kind, 'oneshot_hold')} · first-that-holds {g(lens, kind, 'scan_hold')} "
                f"(rescued after a failed touch {g(lens, kind, 'rescued')}) · memory line: "
                f"{g(lens, kind, 'mem_rows')} rows == the plain loop, holds "
                f"{g(lens, kind, 'mem_hold')} (rescued {g(lens, kind, 'mem_rescued')}); "
                f"{g(lens, kind, 'mem_agree')} first rows == the engine flip, "
                f"{g(lens, kind, 'mem_outside')} DIEs with no in-window engine evaluation")
    res = sum(v for (lens, kind, k), v in tot.items() if k == "rescued")
    mres = sum(v for (lens, kind, k), v in tot.items() if k == "mem_rescued")
    rows = sum(v for (lens, kind, k), v in tot.items() if k in ("plain_rows", "mem_rows"))
    if res == 0 or mres == 0:
        bad.append(f"RESCUE: {res} tap / {mres} memory-line DIEs rescued after a failed touch — "
                   f"the scan cannot be told from the one-shot rule")
    return (not bad), (f"{len(CLASSIC5)} assets x {len(LENSES7)} lenses x 2 scale kinds: EVERY "
                       f"scan row ({rows}, every seq, taps 89/127/200 and the memory line) == "
                       f"the plain-loop scan typed here (own EMA, own loops, the machine's own "
                       f"line); the first evaluated row per DIE == C.retest_holds == "
                       f"BK.band_hold_candidates; the scan's own law holds on every (band, DIE); "
                       f"the memory-line first row == the engine's one-shot flip wherever that "
                       f"evaluation lies in the window; {res} tap and {mres} memory-line DIEs "
                       f"rescued after a failed touch (the rule the one-shot twin cannot see) — "
                       + ("0 findings" if not bad else f"{len(bad)} findings: " + "; ".join(bad[:3])))


# ═════════════════════════════════════════════════════════════════ F-COIN
# PLANTED CONFIGURATIONS, HAND-COMPUTED HERE.  Each row: the L box (top, bot,
# atr, in range), the L+1 box (top, bot, in range), L+1's memory lines as (px,
# born, end_live) with L+1's as-of bar kU, and the expected (coin_top, coin_bot,
# coin_top_mem, coin_bot_mem).  The rule under test: |L boundary - L+1 level| <=
# 0.25 x ATR_L, inclusive; L+1 levels = its LIVE boundaries (twin: + its LIVE
# memory lines, born <= kU < end_live).
COIN_CASES = (
    # 1 · same-side top: |100.0 - 100.4| = 0.4 <= 0.25 x 2.0 = 0.5 -> top True;
    #     bottom |90.0 - 89.2| = 0.8 > 0.5 -> False (it would be True at 0.5 x 2.0 = 1.0)
    ("same-side top 0.4 of 0.5; bottom 0.8 (inside 1.0)",
     (100.0, 90.0, 2.0, True), (100.4, 89.2, True), (), 7, (True, False, True, False)),
    # 2 · CROSS pairing: L top 50.0 vs L+1 BOTTOM 50.25 -> |0.25| <= 0.25 x 1.0
    #     (inclusive) -> top True; L bottom 45.0 vs 57.0 / 50.25 -> False
    ("cross pairing at the threshold exactly (inclusive)",
     (50.0, 45.0, 1.0, True), (57.0, 50.25, True), (), 7, (True, False, True, False)),
    # 3 · L+1 NOT in range: its boundaries never coincide; the twin admits a live
    #     memory line at 45.2 (|45.0 - 45.2| = 0.2 <= 0.25) -> bot_mem True; a live
    #     line at 50.3 is 0.3 from the top (> 0.25, <= 0.5) -> top_mem False
    ("L+1 out of range; live memory lines 0.2 and 0.3 ATR away",
     (50.0, 45.0, 1.0, True), (float("nan"), float("nan"), False),
     ((45.2, 10, 100), (50.3, 10, 100)), 50, (False, False, False, True)),
    # 4 · L NOT in range: nothing of L is live -> all False, whatever L+1 holds
    ("L out of range (its boundaries are not live)",
     (float("nan"), float("nan"), 1.0, False), (50.0, 45.0, True), ((50.0, 0, 100),), 7,
     (False, False, False, False)),
    # 5 · memory lines AT the L boundaries but NOT live at kU 30: one frozen at bar 20
    #     (end_live 20 <= 30), one born at 40 (> 30) -> every flag False
    ("memory lines at the boundaries but not live (frozen before kU; born after kU)",
     (60.0, 55.0, 1.0, True), (float("nan"), float("nan"), False),
     ((60.0, 0, 20), (55.0, 40, 10**9)), 30, (False, False, False, False)),
)


def coin_case_findings() -> list[str]:
    out = []
    for name, (tL, bL, aL, iL), (tU, bU, iU), mem, kU, want in COIN_CASES:
        m = pd.DataFrame({"px": [x[0] for x in mem], "born": [x[1] for x in mem],
                          "end_live": [x[2] for x in mem]}).astype(
            {"px": float, "born": np.int64, "end_live": np.int64})
        live = N.mem_live_at(m, np.array([kU], dtype=np.int64))
        got = N.coin_flags([tL], [bL], [aL], [iL], [tU], [bU], [iU],
                           m["px"].to_numpy(float), live)
        g = tuple(bool(got[k][0]) for k in ("coin_top", "coin_bot", "coin_top_mem", "coin_bot_mem"))
        if g != want:
            out.append(f"hand-computed config '{name}': got {g}, hand-computed {want}")
    return out


def _coin_independent(nv: pd.DataFrame, bundles: dict, L: str) -> list[str]:
    """Plain-Python recomputation of the four flags from the nest row's own
    columns and L+1's memory-line table, row by row (0.25 and the ladder typed
    HERE)."""
    U = LADDER[L]
    mem = bundles[U]["mem"]
    lines = list(zip(mem["px"].tolist(), mem["born"].tolist(), mem["end_live"].tolist()))
    cols = [f"{L}_in_range", f"{U}_in_range", f"{L}_top", f"{L}_bot", f"{L}_atr_L", f"{U}_top",
            f"{U}_bot", f"{U}_k", f"{L}_coin_top", f"{L}_coin_bot", f"{L}_coin_top_mem",
            f"{L}_coin_bot_mem"]
    live_of: dict = {}
    bad = 0
    for inL, inU, tL, bL, aL, tU, bU, kU, g1, g2, g3, g4 in zip(*(nv[c].tolist() for c in cols)):
        inL, inU = bool(inL), bool(inU)
        thr = COIN * aL

        def near(x, ys):
            return any(x == x and y == y and abs(x - y) <= thr for y in ys)
        if kU not in live_of:
            live_of[kU] = [px for px, born, end in lines
                           if kU is not pd.NA and kU >= 0 and born <= kU < end]
        live = live_of[kU]
        ct = inL and inU and near(tL, (tU, bU))
        cb = inL and inU and near(bL, (tU, bU))
        ctm = ct or (inL and near(tL, live))
        cbm = cb or (inL and near(bL, live))
        if (bool(g1), bool(g2), bool(g3), bool(g4)) != (ct, cb, ctm, cbm):
            bad += 1
    return [f"{L}: {bad} rows differ from the independent recomputation"] if bad else []


def coin_break():
    def with_frac():
        with mutated(N, "COIN_FRAC", 0.5):
            return coin_case_findings()

    def no_mem():
        with mutated(N, "mem_live_at", lambda mem, k: np.zeros((len(k), len(mem)), dtype=bool)):
            return coin_case_findings()
    return plants([("COIN_FRAC 0.25 -> 0.5", "hand-computed", with_frac),
                   ("L+1 memory lines ignored (none live)", "hand-computed", no_mem)])


def coin_real():
    bad = coin_case_findings()
    if dict(N.LADDER) != LADDER or tuple(N.NEST_LENSES) != NEST5:
        bad.append(f"LADDER: N.LADDER {dict(N.LADDER)} / N.NEST_LENSES != typed")
    n_rows, counts = 0, {}
    for stem in CLASSIC5:
        bundles = {L: N.bundle11(stem, L, "calibrated") for L in NEST5}
        for L in ("1h", "4h", "12h", "1d"):
            tape = bundles[L]["tape"]
            inst = tape.t0 + tape.step
            nv = N.nest_at(stem, inst, "calibrated")
            bad += [f"{stem} {x}" for x in _coin_independent(nv, bundles, L)]
            n_rows += len(nv)
            for k in ("coin_top", "coin_bot", "coin_top_mem", "coin_bot_mem"):
                counts[(L, k)] = counts.get((L, k), 0) + int(nv[f"{L}_{k}"].sum())
        nv1w = N.nest_at(stem, bundles["1w"]["tape"].t0 + LENS_MS["1w"], "calibrated")
        if not all(nv1w[f"1w_{k}"].isna().all() for k in ("coin_top", "coin_bot", "coin_top_mem",
                                                          "coin_bot_mem")):
            bad.append(f"{stem}: a 1w coincidence is not NA ('no lens above')")
    for stem in UNSEEN12:
        t4 = N.bundle11(stem, "4h", "calibrated")["tape"]
        nv = N.nest_at(stem, t4.t0[-50:] + t4.step, "calibrated")
        na_ok = (all(nv[c].isna().all() for c in nv.columns if c.startswith(("12h_", "1w_")))
                 and nv["4h_coin_top"].isna().all() and nv["1d_coin_bot"].isna().all()
                 and not nv["1h_coin_top"].isna().any())
        if not na_ok:
            bad.append(f"{stem}: NA structure (12h / 1w NA; 4h / 1d coincidence NA; 1h not)")
    for L in ("1h", "4h", "12h", "1d"):
        say(f"      {L} vs {LADDER[L]}: over every closed {L} bar of CLASSIC5 — coin_top "
            f"{counts[(L, 'coin_top')]} · coin_bot {counts[(L, 'coin_bot')]} · with memory lines "
            f"{counts[(L, 'coin_top_mem')]} / {counts[(L, 'coin_bot_mem')]}")
    return (not bad), (f"{len(COIN_CASES)} planted configurations == hand-computed; {n_rows} real "
                       f"nest rows (every closed 1h/4h/12h/1d bar of CLASSIC5) == an independent "
                       f"plain-Python recomputation of all four flags; 1w coincidence NA; the "
                       f"twelve: 12h/1w NA, 4h/1d coincidence NA, 1h live; the ladder == typed — "
                       + ("0 findings" if not bad else f"{len(bad)} findings: " + "; ".join(bad[:3])))


# ═════════════════════════════════════════════════════════════════ F-DET
def _facts_sha(f: dict) -> str:
    h = hashlib.sha256()
    for k in sorted(f):
        a = np.asarray(f[k])
        h.update(k.encode())
        h.update(str(a.dtype).encode())
        h.update(a.tobytes() if a.dtype.kind != "U" else str(a).encode())
    return h.hexdigest()


def probe_text() -> str:
    L = ["PROBE · TIER-C11 RANGE LAYER (deterministic)"]
    L.append(f"SCALE_PICKS.json sha256 {sha_bytes(N.PICKS_PATH.read_bytes())}")
    L.append(f"{N.SOURCES_NAME} sha256 {sha_bytes(N.SOURCES_PATH.read_bytes())}")
    rng = np.random.default_rng(SEED)
    inst = np.sort(rng.integers(1_600_000_000_000, PIN, 60))
    for stem in CLASSIC5 + ("ENAUSDT", "DOGEUSDT"):
        for kind in ("calibrated", "frozen3.0"):
            nv = N.nest_at(stem, inst, kind)
            L.append(f"nest {stem} {kind}: {len(nv)} instants x {nv.shape[1]} columns · sha "
                     f"{frame_sha(nv)}")
            r = nv.iloc[-1]
            L.append("  last: " + " · ".join(
                f"{Lz} {r[f'{Lz}_state']} pct {float(r[f'{Lz}_pct'])!r} d "
                f"{float(r[f'{Lz}_dist_signed_atr'])!r} dev {r[f'{Lz}_dev_top']}/{r[f'{Lz}_dev_bot']} "
                f"{r[f'{Lz}_pick_window']}"
                for Lz in NEST5 if r[f"{Lz}_state"] is not None))
    for stem in CLASSIC5:
        for lens in NEST5:
            ev = N.events(stem, lens, "calibrated")
            L.append(f"events {stem} {lens}: " + " · ".join(
                f"{k} {len(v)} {frame_sha(v)[:16]}" for k, v in ev.items()))
            f = N.range_facts(stem, lens, "calibrated")
            L.append(f"facts {stem} {lens}: {len(f)} arrays · n {len(f['close_ms'])} · sha "
                     f"{_facts_sha(f)}")
        D = N.events(stem, "4h", "calibrated")["deaths"]
        cells = N.l1_cell(stem, "4h", "calibrated", D["dir"].to_numpy(), D["boundary"].to_numpy(),
                          D["known_close_ms"].to_numpy())
        L.append(f"l1 cells {stem} 4h deaths: " + " · ".join(
            f"{c} {int((cells['cell'] == c).sum())}" for c in N.CELLS))
    return "\n".join(L) + "\n"


_EMIT: dict = {}


def emit() -> bytes:
    """The probe emission (memoised in-process: deterministic by the fixture's own claim,
    and each F-DET subprocess computes its own)."""
    if "b" not in _EMIT:
        _EMIT["b"] = (N.lean_block() + probe_text()).encode("utf-8")
    return _EMIT["b"]


def _collect(d: Path) -> dict:
    """{posix path relative to d: bytes} for every file under d, sorted."""
    if not d.exists():
        return {}
    return {p.relative_to(d).as_posix(): p.read_bytes()
            for p in sorted(d.rglob("*")) if p.is_file()}


def _parquet_sha(b: bytes) -> str:
    return C.content_sha(pd.read_parquet(io.BytesIO(b)))


DET_SET = tuple(sorted({ARTIFACT} | {f"picks/{f}" for f in PICK_FILES}))


def det_findings(a: tuple, b: tuple, this: bytes, filed: dict) -> list[str]:
    """a, b = (exit code, {rel: bytes}) of the two hash-seed builds; this = this
    run's probe; filed = the FILED pick files {name: bytes} (the parquet by the
    record's content sha: it is gitignored and absent in a review worktree)."""
    out = []
    for lab, (rc, _) in (("seed 1", a), (f"seed {SEED}", b)):
        if rc != 0:
            out.append(f"{lab} exit {rc}")
    fa, fb = a[1], b[1]
    if not fa or not fb:
        out.append("an emission is EMPTY")
    if set(fa) != set(fb):
        out.append(f"file set: seed 1 {sorted(fa)} vs seed {SEED} {sorted(fb)}")
    for lab, fs in (("seed 1", fa), (f"seed {SEED}", fb)):
        if set(fs) != set(DET_SET):
            out.append(f"file set: {lab} holds {sorted(fs)} != the typed {list(DET_SET)}")
    for rel in sorted(set(fa) & set(fb)):
        if rel.endswith(".parquet"):
            sa, sb = _parquet_sha(fa[rel]), _parquet_sha(fb[rel])
            if sa != sb:
                out.append(f"parquet content sha: {rel} seed 1 {sa[:12]}… vs seed {SEED} {sb[:12]}…")
        elif fa[rel] != fb[rel]:
            out.append(f"seed 1 vs seed {SEED}: {rel}: bytes differ at byte "
                       f"{_first_diff(fa[rel], fb[rel])} (sha {sha_bytes(fa[rel])[:12]}… vs "
                       f"{sha_bytes(fb[rel])[:12]}…)")
    if ARTIFACT in fa and fa[ARTIFACT] != this:
        out.append(f"seed 1 vs this run: {ARTIFACT}: bytes differ at byte "
                   f"{_first_diff(fa[ARTIFACT], this)}")
    for name in PICK_FILES:
        rel = f"picks/{name}"
        if rel not in fa:
            continue
        if name.endswith(".parquet"):
            s = _parquet_sha(fa[rel])
            if s != filed["grid_content_sha256"]:
                out.append(f"{rel}: parquet content sha {s[:12]}… != the FILED record's "
                           f"{filed['grid_content_sha256'][:12]}…")
        elif fa[rel] != filed[name]:
            out.append(f"{rel}: bytes != the FILED {name} (differ at byte "
                       f"{_first_diff(fa[rel], filed[name])})")
    return out


def _filed_picks() -> dict:
    d = {n: (OUT / n).read_bytes() for n in PICK_FILES if not n.endswith(".parquet")}
    d["grid_content_sha256"] = json.loads(d["SCALE_PICKS.json"])["grid_content_sha256"]
    return d


def det_runs(flag: str = "--emit-to") -> dict:
    """The two hash-seed subprocesses, CONCURRENTLY, each into its own fresh
    _det_ root (gitignored [L-0.5])."""
    procs = {}
    for s in DET_SEEDS:
        d = RUN_ROOT / "_det_nest" / (f"seed_{s}" if flag == "--emit-to" else f"hashorder_{s}")
        if d.exists():
            shutil.rmtree(d)
        env = dict(_env(), PYTHONHASHSEED=str(s))
        procs[s] = (d, subprocess.Popen([PY, "-B", str(Path(__file__).resolve()), f"{flag}={d}"],
                                        env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                        text=True, cwd=str(ROOT)))
    outs = {}
    for s, (d, pr) in procs.items():
        _, err = pr.communicate(timeout=3600)
        if pr.returncode != 0:
            clock(f"F-DET seed {s} exit {pr.returncode}: {err[-400:]}")
        outs[s] = (pr.returncode, _collect(d))
    return outs


def det_break():
    this = emit()
    filed = _filed_picks()
    bent = bytearray(this)
    bent[len(bent) // 2] ^= 0x01
    good = {ARTIFACT: this, **{f"picks/{n}": filed[n] for n in PICK_FILES if n in filed}}

    def with_(**kw):
        d = dict(good)
        d.update(kw)
        return d
    g1 = pd.DataFrame({"asset": ["BTCUSDT", "ETHUSDT"], "density_per_100": [0.75, 0.8]})
    g2 = g1.copy()
    g2.loc[1, "density_per_100"] = 0.81
    pq1, pq2 = g1.to_parquet(index=False), g2.to_parquet(index=False)
    js = bytearray(filed["SCALE_PICKS.json"])
    js[len(js) // 3] ^= 0x01
    return plants([
        ("one byte bent in a copy of the seed-20260924 emission", "bytes differ at byte",
         lambda: det_findings((0, good), (0, with_(**{ARTIFACT: bytes(bent)})), this, filed)),
        ("a hash-order-dependent emission (set iteration) under the two seeds",
         f"seed 1 vs seed {SEED}: {ARTIFACT}: bytes differ",
         lambda: (lambda o: det_findings(o[DET_SEEDS[0]], o[DET_SEEDS[1]], o[DET_SEEDS[0]][1]
                                         .get(ARTIFACT, b""), filed))(
             det_runs("--emit-hashorder-to"))),
        ("an extra file in one build's set", "file set",
         lambda: det_findings((0, good), (0, with_(**{"picks/EXTRA.json": b"{}\n"})), this, filed)),
        ("a parquet whose content moved between the builds (one density bent)",
         "parquet content sha",
         lambda: det_findings((0, with_(**{"picks/SCALE_GRID.parquet": pq1})),
                              (0, with_(**{"picks/SCALE_GRID.parquet": pq2})), this, filed)),
        ("a rebuilt SCALE_PICKS.json one byte off the FILED record (both builds agree)",
         "bytes != the FILED SCALE_PICKS.json",
         lambda: det_findings((0, with_(**{"picks/SCALE_PICKS.json": bytes(js)})),
                              (0, with_(**{"picks/SCALE_PICKS.json": bytes(js)})), this, filed)),
    ])


def det_real():
    this = emit()
    filed = _filed_picks()
    o = det_runs()
    bad = det_findings(o[DET_SEEDS[0]], o[DET_SEEDS[1]], this, filed)
    fa = o[DET_SEEDS[0]][1]
    shas = {rel: (_parquet_sha(b) if rel.endswith(".parquet") else sha_bytes(b))[:16]
            for rel, b in fa.items()}
    return (not bad), (f"exit {o[1][0]}/{o[SEED][0]}; the two hash-seed subprocess builds hold "
                       f"the typed file set {list(DET_SET)}; bytes (parquet: content sha) equal "
                       f"under both seeds: " + " · ".join(f"{k} {v}…" for k, v in sorted(shas.items()))
                       + f"; {ARTIFACT} == this run ({len(this)} bytes); the rebuilt "
                       f"SCALE_PICKS.json / .md / {N.SOURCES_NAME} == the FILED bytes and the "
                       f"rebuilt grid's content sha == the record's: {not bad}"
                       + ("" if not bad else f"; findings {bad[:4]}"))


FIXTURES = (
    ("F-PINS", "pins = TC10 sha: the port, the engine, the 12 pins in key order and the retest "
     "grid pins equal STEP0_RECORD and the literals of record; HALT at import otherwise",
     "a perturbed input to N.pins_findings (pin value, pin type, key order, port / engine sha, "
     "provisional hold 6, grid sha, foreign port file) is not refused by its named detector, or "
     "a tierc11_nest with a bent port literal imports without the PINS HALT",
     "the port / engine sha, a pin's value, type or key order, or the retest pins differ from "
     "STEP0_RECORD or the literals typed here",
     pins_break, pins_real),
    ("F-REROOT-NEST", "the census / stamps / null re-roots land on their typed tierc11 targets; "
     "the post-shim handoff holds; one census root; a fresh interpreter reads only the two "
     "allowed TC10 records",
     "a mutated copy skipping the C.STAGE_D re-root (-> the ROOTS clause, checked first, the "
     "same detector in every tree), re-rooting C.OUT to a second census root, skipping the "
     "C.LENS_MS['1h'] extension, the stamps.OUT re-root, the toll label override or the C.SEED "
     "re-root, or resolving the provisional retest pins, imports without its own HALT",
     "a typed C.* / stamps.* / null.* re-root misses, the census roots are not the one typed "
     "root, a post-shim clause is not ok, a TC10 binding of the three modules is undeclared, or "
     "the fresh import does not exit 0 with BLOCKED 0 and ALLOW ⊆ {STEP0_RECORD, TUNING_RESULT}",
     reroot_break, reroot_real),
    ("F-CAL", "every filed pick, grid row, honesty label and input sha reproduces from an "
     "INDEPENDENT path (snapshot files, tuning bars by close, fresh ATR, the typed density loop "
     "and tie-break); write-once holds",
     "N.pick_findings lets through a whole-tape pick labelled out-of-sample, a fallback "
     "relabelled out-of-sample or a dropped cell; the grid-row check lets through one bent "
     "n_confirmed; the sources check lets through one bent input sha; or the label check lets "
     "through labels dropped from every row",
     "the typed commission (71) != N.PICK_CELLS; any pick of record / tuning / whole-tape / "
     "first-half pick, stability flag, window text, fallback label or first-half bar count "
     "differs from the independent path; any of the filed grid rows differs from the "
     "independent machine; the grid's content sha is not the record's; the sidecar's input shas "
     "differ from the snapshot or STAGE_D_MANIFEST or it does not annotate the filed json; a "
     "nest / event label differs from the typed law; or a second build is not refused",
     cal_break, cal_real),
    ("F-NEST-ASOF", "the nest vector is AS-OF (prefix == full at every cut, every lens cut at one "
     "instant, the scale held at the filed pick) AND RIGHT (== the end-of-prefix machine "
     "oracle)",
     "the leaked-redraw reader or the flip-at-stamp reader is not caught by the prefix check on "
     "EVERY asset, or the top/bottom-swapped reader or the pre-repair deviation reset (causal, "
     "wrong) is not caught by the machine oracle on EVERY asset",
     "on any CLASSIC5 asset, any of >= 40 cuts per nest lens gives a prefix nest vector != the "
     "full-run vector (at the cut or at a lens's last three closes), a lens's as-of arrays or "
     "event frames known by the cut != the full run's, any lens's field at the cut != the "
     "end-of-prefix machine oracle, or no out-of-range reading carries deviations",
     asof_break, asof_real),
    ("F-EQ-SCAN", "the first-retest-that-holds scan: EVERY row == a plain-loop scan; its first "
     "row per DIE IS the one-shot detector; the memory-line scan's first row IS the engine's "
     "flip evaluation",
     "a scan that skips the first touch is not caught by the one-shot comparison, or the ONE-SHOT "
     "rule / a skipped SECOND touch, on the taps or on the memory line, is not caught by the "
     "plain-loop row comparison",
     "on any CLASSIC5 asset x 7 lenses x {calibrated, frozen3.0}, any scan row (taps 89/127/200, "
     "memory line, every seq) differs from the plain loop typed here, the first evaluated row "
     "per DIE differs from C.retest_holds or BK.band_hold_candidates, the scan breaks its own "
     "law, the memory-line first row differs from the engine's one-shot flip in the window, "
     "N.SCAN_BANDS != typed, or no DIE is rescued (taps, memory line)",
     eq_break, eq_real),
    ("F-COIN", "boundary coincidence (0.25 x ATR_L, live boxes, all four pairings; the memory-"
     "line twin) on planted configurations and on every real closed bar",
     "COIN_FRAC 0.5, or memory lines ignored, leaves every hand-computed configuration GREEN",
     "a planted configuration differs from its hand-computed flags, a real nest row's flags "
     "differ from an independent plain-Python recomputation, the NA structure (1w; the twelve's "
     "12h / 1w and 4h / 1d coincidence) is wrong, or N.LADDER != typed",
     coin_break, coin_real),
    ("F-DET", "[L-F.1 variant (i)] two subprocess BUILDS under different hash seeds: one file "
     "set, one set of bytes, one parquet content sha — and the filed pick files",
     "a bent byte, a hash-order-dependent emission, an extra file, a parquet whose content "
     "moved, or a rebuilt SCALE_PICKS.json one byte off the filed one is not caught by its "
     "named detector",
     "the PYTHONHASHSEED 1 and 20260924 builds (lean block + range probe + the four pick files "
     "rebuilt into their own _det_ roots) differ in file set, bytes or parquet content sha from "
     "each other, the probe differs from this run's, a rebuilt pick file differs from the FILED "
     "one (the parquet by the record's content sha), or either exits nonzero",
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
    wk = next((a.split("=", 1)[1] for a in args if a.startswith("--worker=")), None)
    if wk:                                   # an exec'd corpus worker (_exec_map)
        return _worker_main(wk, next(a.split("=", 1)[1] for a in args if a.startswith("--jobs=")),
                            next(a.split("=", 1)[1] for a in args if a.startswith("--out=")))
    emit_to = next((a.split("=", 1)[1] for a in args if a.startswith("--emit-to=")), None)
    if emit_to:                              # F-DET's twin: the probe + a full pick build
        Path(emit_to).mkdir(parents=True, exist_ok=True)
        (Path(emit_to) / ARTIFACT).write_bytes(emit())
        N.build_picks(procs=DET_PROCS, out=Path(emit_to) / "picks")
        return 0
    ho = next((a.split("=", 1)[1] for a in args if a.startswith("--emit-hashorder-to=")), None)
    if ho:                                   # F-DET's SABOTAGE twin: a set-order line
        Path(ho).mkdir(parents=True, exist_ok=True)
        (Path(ho) / ARTIFACT).write_bytes(
            N.lean_block().encode() + ("set order: " + ",".join(set(E.PANEL17)) + "\n").encode())
        return 0
    global RUN_ROOT
    root = RUN_ROOT = Path(next((a.split("=", 1)[1] for a in args if a.startswith("--root=")),
                                OUT))
    pick = [a.lower() for a in args if not a.startswith("--")]
    t0 = time.time()
    say(AS_OF_LINE)
    say("=" * 78)
    say("TIER-C11 TC11-R FIXTURES — scripts/tierc11_nest.py (THE RANGE LAYER; L-0.3, L-R.2, "
        "L-R.3, L-R.5, L-R.6, L-F.1, L-F.2) — break leg first, RED or void")
    say("=" * 78)
    say(f"seed {SEED} · substrate {TC11_SNAP.name} · pin {PIN}")
    for ln in N.lean_block().rstrip("\n").splitlines():
        say(ln)
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
