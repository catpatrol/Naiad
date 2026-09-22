#!/usr/bin/env python
"""TIER-C10 · STAGE 0a — F-RF-PINS · F-RF-EQ · F-RF-SEAL · F-RF-KNOWN ·
F-RF-DET · F-RF-WALLS · F-RF-ANCHOR.  The RangeFinder module-ized under analytics/, and
the F-RF suites riding.  TWO LEGS PER FIXTURE, the BREAK leg first and it must
go RED, or the fixture proves nothing [the prove() law of the RF suites and
oracle_fixtures, verbatim shape].  Every plant is made on a COPY — a dict, a
text, an array, a throwaway directory; no real artifact is touched.

WHAT IS ON TRIAL.  analytics/rangefinder_census.py is a PORT of the machine in
engine/rangefinder.py: it may not import it (I-B), so nothing but a fixture
that imports BOTH can say the two are one.  This file is that fixture.
  F-RF-PINS    port literals == machine PINS / PINS_V2 == Pine input defaults;
               the three STEP 0 shas re-asserted (a moved file is PRINTED and
               the pins verdict stands on its own); the twin differs from its
               STEP 0 blob in its two loaders and one constant, nowhere else.
  F-RF-EQ      port == machine: the five event shas OF RECORD on the frozen
               tape (three-way: literal, machine, port), then FULL equality
               (every event log, Range field, pivot, summary number) on
               ETHUSDT 4h full history, SOLUSDT 1d, SOLUSDT 5m — so the port is
               neither BTC- nor lens-overfit — and at off-default pins, so the
               branches the shipped pins never reach are not dead weight.
  F-RF-SEAL    out["seals"] is the truth the machine's knowable_at drops to
               -1 on some 3+ decimal tapes; proven by MACHINE prefix runs.
  F-RF-KNOWN   machine_known_at / leash_known_at (additive, the port's): the log
               of tape[:t] == the full log filtered by known_at <= t - 1 on seeded
               cuts; the naive `i` filter and the machine's knowable_at both FAIL.
  F-RF-DET     the port is pure: same input, same bytes; inputs never mutated;
               a DataFrame and a tuple of arrays are one tape.
  F-RF-WALLS   F-AN-3 / F-AN-4 / F-AN-5 (the real tests, run) and F-BR-14's
               regex + closure legs (its constants read as TEXT from
               scripts/oracle_fixtures.py, never imported — another lane's
               file is live in this tree); the port is NOT in
               analytics._MODULES and analytics_sha() stays put.
  F-RF-ANCHOR  the record anchor is DERIVED (both exports of record + the
               machine's own header) and it is what restores F-RF-2 / F-RF-7 /
               F-RF-9 / F-RF-7c: both suites 8/8 at the anchor, the same four
               RED on the un-anchored tail; the loaders' default is still live.

BANNED HERE, as in every tier suite: self-comparison; one example where
cardinality was possible; a tuned magnitude bound standing in for an
identity; a check whose claim is not the design's claim.  Identity is judged
by sha, never by eye.

FROZEN SUBSTRATE [TIER-C10 law 3]: HALTs unless NAIAD_CACHE_DIR is exported
and is not the live cache.  Seed 20260921.  The transcript filed under
research_outputs/tierc10/ carries no wall clock (timings print to stdout only).

Run: NAIAD_CACHE_DIR=~/.cache/naiad/snapshots/tc10_20260921 \\
     ~/venvs/naiad/bin/python scripts/tierc10_rf_fixtures.py [leg ...]
     (any argument is matched as a substring of the leg id, case-blind)
"""
from __future__ import annotations

import ast
import contextlib
import copy
import hashlib
import importlib.util
import inspect
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import tokenize
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict
from pathlib import Path

sys.dont_write_bytecode = True

import numpy as np                                                   # noqa: E402
import pandas as pd                                                  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from analytics import rangefinder_census as RC                       # noqa: E402
from engine import indicators as ind                                 # noqa: E402
from engine import rangefinder as E                                  # noqa: E402
from engine.data import cache_dir                                    # noqa: E402
import rangefinder_twin as RF                                        # noqa: E402

SEED = 20260921
OUT = ROOT / "research_outputs" / "tierc10"
LIVE_CACHE = Path.home() / ".cache" / "naiad" / "data_cache"
STEP0_COMMIT = "d63592f"           # STEP0_RECORD.md: "branch v12-v1-census @ d63592f"
H4_MS = 14_400_000

# THE FIVE EVENT SHAS OF RECORD — typed HERE from engine/rangefinder.py's
# header, a second object beside the port's own EVENT_SHAS_OF_RECORD, so the
# three-way check below is never one literal counted twice.
RECORD_SHAS = {
    "v2_macro": (92, "2145418831a00be710fb401c3a7c16722c0857feda4a29d58d503f3dc2b09ed4"),
    "v2_micro": (573, "73798d744a377d6f2398020b0ae891d2f34efab2e48fda1c0e745243e2b04c72"),
    "v2_leash": (153, "824cdff43675053a54f5c2cbbec9ba8b87c2e3661fca20c00459880bd17ec54e"),
    "v2_suppress": (17, "e7b0de6a072ea9ba0c5bb0b7dc2c0ebba72d68e2730b1e6056f26fa7189dba70"),
    "v1_body": (152, "af2485e664bf822492e8bb86ef4c45afb05844bed5e342f4a9aa30588dba5404"),
}
RECORD_TAPE_SHA8 = "bda85c2e"      # engine.rangefinder.tape_from_klines' docstring

LEANS = (
    "[LEAN-HEPHAESTUS] L1 1d = exactly SIX complete native-4h bars per UTC day (the twin's "
    "law); 1w = seven such complete days, MONDAY-anchored UTC, complete weeks only. Source = "
    "native 4h, never 1h/5m aggregates.",
    "[LEAN-HEPHAESTUS] L2 SCALE_MULT: every registered lane and every Stage-A stamp uses the "
    "FROZEN 3.0 (Pine/twin pin of record). CENSUS-R prints the self-calibrated SCALE tables "
    "WITH the frozen-3.0 tables beside. Calibrator = grid 1.5..4.0 step 0.25 (Pine "
    "minval/step), nearest confirmed-macro-range density to 0.75 per 100 bars, tie-break "
    "toward 3.0 then lower; the whole grid printed (F-GRID: every grid whole).",
    "[LEAN-HEPHAESTUS] L3 analytics module = analytics/rangefinder_census.py: a PURE numpy "
    "port (no engine import, no IO, ATR passed IN as an argument), NOT added to "
    "analytics._MODULES (analytics_sha stays put) — printed as a finding.",
    "[LEAN-HEPHAESTUS] Stage 0a: the twin's loaders take anchor_ms DEFAULTING TO None = the "
    "live tail, so every caller that is not a fixture behaves exactly as before; the two RF "
    "fixture suites pass RF.RECORD_ANCHOR_MS and ride the window of record (`--live` rides "
    "the tail).",
)

FAILED: list[str] = []
PASSED: list[str] = []
T: list[str] = []                  # the transcript: deterministic lines only


def say(line: str = "") -> None:
    print(line)
    T.append(line)


def clock(line: str) -> None:
    """Wall-clock facts: stdout ONLY, never the filed transcript [F-DET law]."""
    print(f"  [clock · stdout only] {line}")


def check(fixture: str, ok: bool, detail: str) -> bool:
    say(f"  [{'PASS' if ok else 'FAIL'}] {fixture}: {detail}")
    return ok


def prove(fixture: str, title: str, fails_if: str, break_leg, real_leg) -> None:
    """Both legs, in order. The break leg must go red or the fixture is void."""
    say(f"\n{fixture} — {title}")
    say(f"  FAILS IF: {fails_if}")
    try:
        b_ok, b_detail = break_leg()
    except Exception as e:                       # a break leg that errors proved nothing
        b_ok, b_detail = True, f"break leg RAISED {e.__class__.__name__}: {e}"
    say(f"  [BREAK] deliberate violation -> "
        f"{'RED (correct)' if not b_ok else 'GREEN (FIXTURE IS VOID)'}: {b_detail}")
    try:
        r_ok, r_detail = real_leg()
    except Exception as e:                       # a fixture that errors is a fail
        r_ok, r_detail = False, f"raised {e.__class__.__name__}: {e}"
    green = check(fixture, r_ok, r_detail)
    if b_ok:
        FAILED.append(f"{fixture} (break leg passed — fixture proves nothing)")
    elif not green:
        FAILED.append(fixture)
    else:
        PASSED.append(fixture)


def plants(rows) -> tuple[bool, str]:
    """One plant per guard, judged ONE AT A TIME [F-BR-13/14 idiom]. `rows` =
    (name, thunk -> list of findings). A plant that yields NO finding passed —
    the break leg is then GREEN and the fixture void."""
    passed, caught = [], []
    for name, thunk in rows:
        found = thunk()
        (caught if found else passed).append(
            f"{name} -> {str(found[0])[:110]}" if found else name)
    if passed:
        return True, f"{len(passed)} plant(s) PASSED: {passed}"
    return False, f"all {len(caught)} plants caught, one at a time: " + " · ".join(caught)


# ═══════════════════════════════════════════════════ tapes, cache-only
def sha(x) -> str:
    return hashlib.sha256(json.dumps(x, sort_keys=True).encode()).hexdigest()


def file_sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def iso(ms: int) -> str:
    return pd.Timestamp(int(ms), unit="ms", tz="UTC").strftime("%Y-%m-%dT%H:%MZ")


def klines(sym: str, tf: str) -> pd.DataFrame:
    return pd.read_parquet(cache_dir() / "klines" / f"{sym}_{tf}.parquet")


def tape_4h(f: pd.DataFrame, n_bars: int | None = None) -> pd.DataFrame:
    return E.tape_from_klines(f, len(f) if n_bars is None else n_bars)


def tape_1d(f4: pd.DataFrame) -> pd.DataFrame:
    """[LEAN-HEPHAESTUS] L1: 1d = exactly SIX complete native-4h bars per UTC
    day. Written here from the raw parquet, sharing no code with the twin's
    daily_bars (F-RF-ANCHOR compares the two)."""
    day = (f4["open_time"] // 86_400_000).to_numpy()
    g = (f4.assign(day=day).groupby("day")
         .agg(n=("open_time", "size"), o=("open", "first"), h=("high", "max"),
              l=("low", "min"), c=("close", "last"), t0=("open_time", "first")))
    d = g[g["n"] == 6].reset_index(drop=True)
    d["ts"] = pd.to_datetime(d["t0"], unit="ms", utc=True).dt.strftime("%Y-%m-%d")
    d.attrs["dropped_incomplete_days"] = int((g["n"] != 6).sum())
    return d


def atr_of(d) -> np.ndarray:
    """The machine's ATR — the engine's Wilder RMA seeded at TR[0] — computed
    HERE, in scripts/, and handed to the port as an argument [L3 / I-D]."""
    return ind.atr(d["h"].to_numpy(float), d["l"].to_numpy(float),
                   d["c"].to_numpy(float), RC.ATR_LEN)


_TAPES: dict = {}


def tapes() -> dict:
    """label -> (frame, lens, note). Built once. The record tapes are cut at
    the anchor BEFORE tail(N); the other three run to the snapshot's edge."""
    if _TAPES:
        return _TAPES
    btc = klines("BTCUSDT", "4h")
    rec = btc[btc["open_time"] <= RC.RECORD_ANCHOR_MS]
    _TAPES["BTCUSDT 4h RECORD"] = (tape_4h(rec, E.V2_WINDOW_BARS), "4h",
                                   "last 1700 bars with open_time <= the anchor")
    _TAPES["BTCUSDT 1d RECORD"] = (tape_1d(rec).tail(RF.WINDOW_BARS).reset_index(drop=True),
                                   "1d", "last 420 complete UTC days at the anchor [L1]")
    _TAPES["ETHUSDT 4h FULL"] = (tape_4h(klines("ETHUSDT", "4h")), "4h", "full history")
    _TAPES["SOLUSDT 1d FULL"] = (tape_1d(klines("SOLUSDT", "4h")), "1d",
                                 "full history, six native-4h bars per day [L1]")
    s5 = klines("SOLUSDT", "5m").tail(60_000)
    _TAPES["SOLUSDT 5m LAST-60000"] = (tape_4h(s5, 60_000), "5m",
                                       "last 60,000 bars (the machine is O(n^2): "
                                       "full 5m history costs it minutes)")
    return _TAPES


# ═══════════════════════════════════════════════ equality, facet by facet
SUMMARY_KEYS = ("coverage_pct", "n_bars", "n_pivots", "n_confirmed",
                "n_potential_unresolved", "mean_confirmed_lifetime",
                "n_lifetime_censored", "n_pending_open", "final_state", "status_line")


def _ranges_json(m) -> str:
    return json.dumps([asdict(r) for r in m["ranges"]], sort_keys=True, default=str)


def machine_diff(e: dict, p: dict) -> list[str]:
    """Every facet on which the port's run differs from the machine's."""
    bad = []
    if sha(e["events"]) != sha(p["events"]):
        bad.append(f"events ({len(e['events'])} vs {len(p['events'])})")
    if _ranges_json(e) != _ranges_json(p):
        bad.append("Range fields")
    if ([(int(a), float(b), int(c)) for a, b, c in e["pivots"]]
            != [(int(a), float(b), int(c)) for a, b, c in p["pivots"]]):
        bad.append("pivots")
    bad += [f"{k} ({e[k]!r} vs {p[k]!r})" for k in SUMMARY_KEYS
            if json.dumps(e[k], default=float) != json.dumps(p[k], default=float)]
    return bad


def v2_diff(e: dict, p: dict) -> list[str]:
    bad = [f"macro.{x}" for x in machine_diff(e["macro"], p["macro"])]
    bad += [f"micro.{x}" for x in machine_diff(e["micro"], p["micro"])]
    for k in ("leash", "suppressed", "micro_kept_events", "flips"):
        if sha(e[k]) != sha(p[k]):
            bad.append(f"{k} ({len(e[k])} vs {len(p[k])})")
    if [list(x) for x in e["kept"]] != [list(x) for x in p["kept"]]:
        bad.append("kept")
    bad += [k for k in ("state", "macro_count_feb_aug", "status_line") if e[k] != p[k]]
    return bad


def _is_spam(x: dict) -> bool:
    return x["event"] == "flip-retest" or (
        x["event"] == "memory-retest" and x["verdict"].startswith("candidacy consumed"))


_RUNS: dict = {}


def runs(label: str) -> tuple:
    """(machine v2, port v2, atr, seconds machine, seconds port) — memoised."""
    if label not in _RUNS:
        d = tapes()[label][0]
        a = atr_of(d)
        t0 = time.perf_counter()
        ev2 = E.run_v2(d, E.PINS_V2)
        t1 = time.perf_counter()
        pv2 = RC.run_v2(d, a, RC.PINS_V2)
        t2 = time.perf_counter()
        _RUNS[label] = (ev2, pv2, a, t1 - t0, t2 - t1)
    return _RUNS[label]


# ═════════════════════════════════════════════════════════ F-RF-PINS
PINE_PATH = ROOT / "pine" / "SS12_RangeFinder_v2.pine"
NUM_MAP = {"LEG_MIN": "legMin", "REV_MIN": "revMin", "TOUCH_EPS": "touchEps",
           "DEV_RETURN_BARS": "devRet", "BREAK_CONFIRM_N": "brkN",
           "BREAK_MARGIN": "brkMargin"}
V2_MAP = {"SCALE_MULT": "scaleMult", "FLIP_HOLD_MARGIN": "flipMargin",
          "FLIP_HOLD_BARS": "flipBars", "MEM_TTL_BARS": "memTtl"}
TWIN_SANCTIONED = {"daily_bars", "bars_4h", "RECORD_ANCHOR_MS"}


def _pine_defaults(text: str) -> dict:
    out = {}
    for pin, var in {**NUM_MAP, **V2_MAP}.items():
        m = re.search(rf"^{var}\s*=\s*input\.(?:float|int)\(\s*([0-9.]+)", text, re.M)
        if m:
            out[pin] = float(m.group(1))
    m = re.search(r'^boundaryMode\s*=\s*input\.string\(\s*"(\w+)"', text, re.M)
    out["BOUNDARY_MODE"] = m.group(1) if m else None
    m = re.search(r"^ATR_LEN\s*=\s*(\d+)", text, re.M)
    out["ATR_LEN"] = int(m.group(1)) if m else None
    return out


def _pins_findings(port_pins: dict, port_v2: dict, pine_text: str) -> list[str]:
    bad = []
    if list(port_pins.items()) != list(E.PINS.items()):
        bad.append(f"port PINS != machine PINS (values or KEY ORDER): "
                   f"{[k for k in E.PINS if port_pins.get(k) != E.PINS[k]]}")
    if list(port_v2.items()) != list(E.PINS_V2.items()):
        bad.append(f"port PINS_V2 != machine PINS_V2: "
                   f"{[k for k in E.PINS_V2 if port_v2.get(k) != E.PINS_V2[k]]}")
    got = _pine_defaults(pine_text)
    for k in NUM_MAP:
        if got.get(k) is None or abs(got[k] - float(port_pins[k])) >= 1e-12:
            bad.append(f"Pine default {k}={got.get(k)} != port {port_pins[k]}")
    for k in V2_MAP:
        if got.get(k) is None or abs(got[k] - float(port_v2[k])) >= 1e-12:
            bad.append(f"Pine default {k}={got.get(k)} != port {port_v2[k]}")
    if got["BOUNDARY_MODE"] != port_pins["BOUNDARY_MODE"]:
        bad.append(f"Pine boundaryMode {got['BOUNDARY_MODE']!r} != port "
                   f"{port_pins['BOUNDARY_MODE']!r}")
    if got["ATR_LEN"] != RC.ATR_LEN:
        bad.append(f"Pine ATR_LEN {got['ATR_LEN']} != port {RC.ATR_LEN}")
    return bad


def _git_blob(rev: str, rel: str) -> bytes | None:
    """READ-ONLY git: the bytes of one file at one commit. None if unreachable."""
    out = subprocess.run(["git", "cat-file", "-p", f"{rev}:{rel}"], cwd=ROOT,
                         capture_output=True)
    return out.stdout if out.returncode == 0 else None


def _top_level(src: str) -> dict:
    """name -> ast.dump of every top-level statement; unnamed ones keyed by order."""
    out: dict = {}
    for k, node in enumerate(ast.parse(src).body):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            name = node.name
        elif isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
            name = node.targets[0].id
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            name = node.target.id
        else:
            name = f"<stmt {sum(1 for n in out if n.startswith('<stmt'))}>"
        out[name] = ast.dump(node)
    return out


def _twin_findings(twin_src: str, step0_src: str) -> list[str]:
    """The twin may differ from its STEP 0 blob ONLY in TWIN_SANCTIONED."""
    now, then = _top_level(twin_src), _top_level(step0_src)
    bad = [f"twin statement `{k}` differs from the STEP 0 blob" for k in then
           if k not in TWIN_SANCTIONED and now.get(k) != then[k]]
    bad += [f"twin grew a top-level `{k}` that STEP 0 did not have"
            for k in now if k not in then and k not in TWIN_SANCTIONED]
    return bad


def pins_break():
    pine = PINE_PATH.read_text(encoding="utf-8")
    twin = (ROOT / "scripts" / "rangefinder_twin.py").read_text(encoding="utf-8")
    blob = _git_blob(STEP0_COMMIT, "scripts/rangefinder_twin.py")
    step0 = blob.decode("utf-8") if blob else ""
    return plants([
        ("PIN PLANT (a COPY of the port's PINS with TOUCH_EPS 0.60 -> 0.67 — the "
         "STEP 0 note's phantom pin)",
         lambda: _pins_findings(dict(RC.PINS, TOUCH_EPS=0.67), dict(RC.PINS_V2), pine)),
         ("KEY-ORDER PLANT (the same pins, REV_MIN moved last — export order is bytes)",
         lambda: _pins_findings({**{k: v for k, v in RC.PINS.items() if k != "REV_MIN"},
                                 "REV_MIN": RC.PINS["REV_MIN"]}, dict(RC.PINS_V2), pine)),
        ("PINE PLANT (scaleMult default 3.0 -> 2.0 in a COPY of the .pine text)",
         lambda: _pins_findings(dict(RC.PINS), dict(RC.PINS_V2), pine.replace(
             "scaleMult = input.float(3.0", "scaleMult = input.float(2.0", 1))),
        ("TWIN PLANT (KEY_C_TOL_USD 1_200.0 -> 9_999.0 in a COPY of the twin text — an "
         "edit OUTSIDE the two loaders)",
         lambda: _twin_findings(twin.replace("KEY_C_TOL_USD = 1_200.0",
                                             "KEY_C_TOL_USD = 9_999.0", 1), step0)),
    ])


def pins_real():
    bad = _pins_findings(RC.PINS, RC.PINS_V2, PINE_PATH.read_text(encoding="utf-8"))
    for name in ("ATR_LEN", "V2_WINDOW_BARS", "MEM_CAP_PER_SIDE"):
        if getattr(RC, name) != getattr(E, name):
            bad.append(f"{name}: port {getattr(RC, name)} != machine {getattr(E, name)}")
    if RC.PINS is E.PINS or RC.PINS_V2 is E.PINS_V2:
        bad.append("the port's pins ARE the machine's objects — not frozen literals")
    if not (RF.PINS is E.PINS and RF.PINS_V2 is E.PINS_V2):
        bad.append("the twin no longer re-exports the machine's OWN pin dicts")
    moved = []
    for rel, want in RC.STEP0_SHA256.items():
        got = file_sha(ROOT / rel)
        blob = _git_blob(STEP0_COMMIT, rel)
        if blob is None:
            bad.append(f"{rel}: STEP 0 blob {STEP0_COMMIT} unreachable — silence is not health")
        elif hashlib.sha256(blob).hexdigest() != want:
            bad.append(f"{rel}: the STEP 0 literal is NOT the sha of the {STEP0_COMMIT} blob")
        say(f"      {rel}")
        say(f"        STEP 0  {want}")
        say(f"        now     {got}  {'== STEP 0' if got == want else 'MOVED since STEP 0'}")
        if got != want:
            moved.append(rel)
    twin_rel = "scripts/rangefinder_twin.py"
    blob = _git_blob(STEP0_COMMIT, twin_rel)
    if blob is not None:
        tw = _twin_findings((ROOT / twin_rel).read_text(encoding="utf-8"),
                            blob.decode("utf-8"))
        bad += tw
        say(f"      twin vs its STEP 0 blob: {'differs ONLY in ' + str(sorted(TWIN_SANCTIONED)) if not tw else tw}")
    unexpected = [m for m in moved if m != twin_rel]
    if unexpected:
        say(f"      MOVED SINCE STEP 0 (another lane is live in this tree): {unexpected} — "
            f"pins {'STILL AGREE' if not bad else 'NO LONGER AGREE'}; F-RF-EQ says whether "
            f"the BYTES still do")
    pine = _pine_defaults(PINE_PATH.read_text(encoding="utf-8"))
    ok = not bad
    return ok, (f"port == machine == Pine on all {len(NUM_MAP)} micro pins + "
                f"{len(V2_MAP)} v2 pins + BOUNDARY_MODE + ATR_LEN, key order included "
                f"(pin of record TOUCH_EPS {pine['TOUCH_EPS']:.2f} / DEV_RETURN_BARS "
                f"{int(pine['DEV_RETURN_BARS'])} / BREAK_CONFIRM_N {int(pine['BREAK_CONFIRM_N'])}; "
                f"SCALE_MULT {pine['SCALE_MULT']}); STEP 0 shas: "
                f"{len(RC.STEP0_SHA256) - len(moved)} unmoved, moved = {moved or 'none'}"
                f"{' (the twin moved by the Stage 0a anchor edit, proven loader-only)' if moved == [twin_rel] else ''}"
                if ok else "; ".join(bad[:4]))


# ═══════════════════════════════════════════════════════════ F-RF-EQ
def _record_findings(pins: dict, pins_v2: dict, tape_edit=None, atr_edit=None) -> list[str]:
    """The port's five shas on the record tapes vs the literals OF RECORD."""
    d4, d1 = tapes()["BTCUSDT 4h RECORD"][0], tapes()["BTCUSDT 1d RECORD"][0]
    if tape_edit is not None:
        d4, d1 = tape_edit(d4.copy()), tape_edit(d1.copy())
    a4, a1 = atr_of(d4), atr_of(d1)
    if atr_edit is not None:
        a4, a1 = atr_edit(a4.copy()), atr_edit(a1.copy())
    try:
        macro = RC.run_machine(d4, a4, RC.macro_pins(pins_v2["SCALE_MULT"], pins))
        micro = RC.run_machine(d4, a4, dict(pins))
        got = {"v2_macro": macro["events"], "v2_micro": micro["events"],
               "v2_leash": RC.flips_and_leash(macro, d4, a4, pins_v2),
               "v2_suppress": RC.containment(micro, macro)[1],
               "v1_body": RC.run_machine(d1, a1, dict(pins))["events"]}
    except ValueError as e:
        return [f"the port REFUSED the input: {e}"]
    return [f"{k}: {len(got[k])} events {sha(got[k])[:12]}… != record {n} {want[:12]}…"
            for k, (n, want) in RECORD_SHAS.items()
            if (len(got[k]), sha(got[k])) != (n, want)]


def _bump(col: str, k: int):
    def edit(d):
        d.loc[d.index[k], col] = d[col].iloc[k] * 1.02
        return d
    return edit


def _nan_warmup(a):
    a[:RC.ATR_LEN - 1] = np.nan        # this package's own SMA-seeded ATR looks like this
    return a


def eq_break():
    return plants([
        ("PIN PLANT (TOUCH_EPS 0.60 -> 0.67 in the port CALL, tape and ATR untouched)",
         lambda: _record_findings(dict(RC.PINS, TOUCH_EPS=0.67), RC.PINS_V2)),
        # FLIP_HOLD_BARS 6 -> 7 is NOT the plant: measured INERT on the record tape
        # (all five flips also hold a seventh bar, and the log never prints the pin)
        # — a plant that cannot bite proves nothing. The margin bites: C-F2 holds by
        # ~101 USD at 1.0 and fails through at 0.5 [the machine's header].
        ("PIN PLANT (FLIP_HOLD_MARGIN 1.0 -> 0.5 in the port CALL)",
         lambda: _record_findings(RC.PINS, dict(RC.PINS_V2, FLIP_HOLD_MARGIN=0.5))),
        ("TAPE PLANT (one high ×1.02 on bar 100 of a COPY of each record tape)",
         lambda: _record_findings(RC.PINS, RC.PINS_V2, tape_edit=_bump("h", 100))),
        ("ATR PLANT (a COPY of the ATR scaled ×1.001 — a different smoother)",
         lambda: _record_findings(RC.PINS, RC.PINS_V2, atr_edit=lambda a: a * 1.001)),
        ("ATR PLANT (NaN warm-up, the SMA-seeded shape — the port must REFUSE it)",
         lambda: _record_findings(RC.PINS, RC.PINS_V2, atr_edit=_nan_warmup)),
    ])


def _offdefault_findings() -> tuple[list[str], list[str]]:
    """Branches the shipped pins never reach. -> (findings, lines)."""
    bad, lines = [], []
    d1 = tapes()["BTCUSDT 1d RECORD"][0]
    de = tapes()["ETHUSDT 4h FULL"][0]
    a1, ae = atr_of(d1), atr_of(de)
    cases = (
        ("BTC 1d RECORD · BOUNDARY_MODE wick", d1, a1, dict(E.PINS, BOUNDARY_MODE="wick")),
        ("BTC 1d RECORD · MULTI_ACTIVE 1", d1, a1, dict(E.PINS, MULTI_ACTIVE=1)),
        ("BTC 1d RECORD · lapse-open DEV 2 / N 20 / M 6.0 · REDRAW_BASIS body", d1, a1,
         dict(E.PINS, DEV_RETURN_BARS=2, BREAK_CONFIRM_N=20, BREAK_MARGIN=6.0,
              REDRAW_BASIS="body")),
        ("ETH 4h FULL · MULTI_ACTIVE 1 (micro)", de, ae, dict(E.PINS, MULTI_ACTIVE=1)),
    )
    for name, d, a, pins in cases:
        em, pm = E.run_machine(d, pins), RC.run_machine(d, a, pins)
        diff = machine_diff(em, pm)
        lapses = sum(1 for x in em["events"] if x["event"] == "breach-lapse")
        lines.append(f"      {name}: {len(em['events'])} events {sha(em['events'])[:12]}… "
                     f"{'IDENTICAL' if not diff else 'DIFFERS ' + str(diff)}"
                     + (f" · {lapses} breach-lapse (the law unreachable at the shipped pins)"
                        if "lapse" in name else ""))
        bad += [f"{name}: {x}" for x in diff]
        if "lapse" in name and not lapses:
            bad.append(f"{name}: no lapse occurred — the case exercises nothing")
    # containment's scan path + the leash under OVERLAPPING macro lives
    mp = dict(RC.macro_pins(3.0), MULTI_ACTIVE=1)
    em, pm = E.run_machine(de, mp), RC.run_machine(de, ae, mp)
    emi, pmi = E.run_machine(de, dict(E.PINS)), RC.run_machine(de, ae, dict(RC.PINS))
    lives = [r for r in em["ranges"] if r.confirm_i >= 0]
    overlap = sum(1 for x, y in zip(lives, lives[1:]) if x.die_i < 0 or x.die_i > y.confirm_i)
    ek, es = E.containment(emi, em)
    pk, ps = RC.containment(pmi, pm)
    el, pl = E.flips_and_leash(em, de, E.PINS_V2), RC.flips_and_leash(pm, de, ae, RC.PINS_V2)
    same = (not machine_diff(em, pm) and [list(x) for x in ek] == [list(x) for x in pk]
            and sha(es) == sha(ps) and sha(el) == sha(pl))
    lines.append(f"      ETH 4h FULL · MACRO MULTI_ACTIVE 1: {overlap} overlapping macro lives "
                 f"(containment's scan path), kept {len(ek)} / suppressed {len(es)} / leash "
                 f"{len(el)} — {'IDENTICAL' if same else 'DIFFERS'}")
    if not same:
        bad.append("MULTI macro: containment / leash differ")
    if not overlap:
        bad.append("MULTI macro produced no overlapping lives — the scan path is untested")
    # the cap: a real tape rarely binds it
    for cap in (1, 2):
        mac_e, mac_p = runs("ETHUSDT 4h FULL")[0]["macro"], runs("ETHUSDT 4h FULL")[1]["macro"]
        el = E.flips_and_leash(mac_e, de, E.PINS_V2, mem_cap=cap)
        pl = RC.flips_and_leash(mac_p, de, ae, RC.PINS_V2, mem_cap=cap)
        caps = sum(1 for x in el if x.get("reason") == "cap")
        lines.append(f"      ETH 4h FULL · mem_cap {cap}: {len(el)} leash events, {caps} "
                     f"cap-expiries — {'IDENTICAL' if sha(el) == sha(pl) else 'DIFFERS'}")
        if sha(el) != sha(pl):
            bad.append(f"mem_cap {cap}: leash differs")
        if not caps:
            bad.append(f"mem_cap {cap}: the cap never bound — the case exercises nothing")
    # ten synthetic never-touched corpses [the F-RF-10 population]: cap 6 decisive
    proto = next(r for r in runs("ETHUSDT 4h FULL")[0]["macro"]["ranges"]
                 if r.state == "DEAD" and r.confirm_i >= 0)
    fake = {"ranges": []}
    for k in range(10):
        r = copy.copy(proto)
        r.rid, r.confirm_i, r.die_i = 900 + k, 20 + k * 5, 40 + k * 5
        r.top, r.bottom = 1.0e9 + k, 1.0e-9 + k * 1.0e-12
        fake["ranges"].append(r)
    el = E.flips_and_leash(fake, de, E.PINS_V2)
    pl = RC.flips_and_leash(fake, de, ae, RC.PINS_V2)
    lines.append(f"      synthetic ten-corpse population, cap 6: {len(el)} events "
                 f"({sum(1 for x in el if x.get('reason') == 'cap')} cap, "
                 f"{sum(1 for x in el if x.get('reason') == 'ttl')} ttl) — "
                 f"{'IDENTICAL' if sha(el) == sha(pl) else 'DIFFERS'}")
    if sha(el) != sha(pl):
        bad.append("synthetic corpses: leash differs")
    return bad, lines


def eq_real():
    bad = []
    # (a) the record, three ways: literal == machine == port
    ev2, pv2, _, _, _ = runs("BTCUSDT 4h RECORD")
    d1 = tapes()["BTCUSDT 1d RECORD"][0]
    mach = {"v2_macro": ev2["macro"]["events"], "v2_micro": ev2["micro"]["events"],
            "v2_leash": ev2["leash"], "v2_suppress": ev2["suppressed"],
            "v1_body": E.run_machine(d1, E.PINS)["events"]}
    port = {"v2_macro": pv2["macro"]["events"], "v2_micro": pv2["micro"]["events"],
            "v2_leash": pv2["leash"], "v2_suppress": pv2["suppressed"],
            "v1_body": RC.run_machine(d1, atr_of(d1), RC.PINS)["events"]}
    header = E.__doc__ or ""
    say("      THE FIVE EVENT SHAS OF RECORD — literal · machine · port")
    for k, (n, want) in RECORD_SHAS.items():
        m_ok = (len(mach[k]), sha(mach[k])) == (n, want)
        p_ok = (len(port[k]), sha(port[k])) == (n, want)
        l_ok = want in header and RC.EVENT_SHAS_OF_RECORD.get(k) == (n, want)
        say(f"        {k:12} {n:4d} events  {want}  machine {'==' if m_ok else '!='} · "
            f"port {'==' if p_ok else '!='} · header+port literal {'==' if l_ok else '!='}")
        if not (m_ok and p_ok and l_ok):
            bad.append(f"{k}: machine={m_ok} port={p_ok} literals={l_ok}")
    # (b) full equality, tape by tape
    say("      FULL EQUALITY — every event log, Range field, pivot, summary number, kept set;")
    say("      and the LEAN leash (retests=False) == the full leash minus its two spam classes")
    for label, (d, lens, note) in tapes().items():
        e, p, a, te, tp = runs(label)
        diff = v2_diff(e, p)
        lean = RC.flips_and_leash(p["macro"], d, a, RC.PINS_V2, retests=False)
        want_lean = [x for x in e["leash"] if not _is_spam(x)]
        if sha(lean) != sha(want_lean):
            diff.append(f"lean leash ({len(lean)} vs {len(want_lean)})")
        nomic = RC.run_v2(d, a, RC.PINS_V2, with_micro=False, retests=False)
        if (sha(nomic["macro"]["events"]) != sha(e["macro"]["events"])
                or nomic["micro"] is not None or nomic["kept"] is not None):
            diff.append("with_micro=False")
        say(f"        {label}: {len(d):,} bars, {lens} lens, as of bar-open {d['ts'].iloc[-1]} "
            f"({note})")
        say(f"          macro {len(e['macro']['events'])} {sha(e['macro']['events'])[:12]}… · "
            f"micro {len(e['micro']['events'])} {sha(e['micro']['events'])[:12]}… · leash "
            f"{len(e['leash'])} {sha(e['leash'])[:12]}… (lean {len(lean)}) · suppress "
            f"{len(e['suppressed'])} · kept {len(e['kept'])} — "
            f"{'IDENTICAL' if not diff else 'DIFFERS: ' + str(diff[:4])}")
        clock(f"{label}: machine run_v2 {te:.3f} s · port run_v2 {tp:.3f} s "
              f"(×{te / max(tp, 1e-9):.0f})")
        bad += [f"{label}: {x}" for x in diff]
    # (c) the branches the shipped pins never reach
    say("      OFF-DEFAULT PINS — the port's fallbacks are not dead weight")
    ob, lines = _offdefault_findings()
    for ln in lines:
        say(ln)
    bad += ob
    ok = not bad
    return ok, (f"literal == machine == port on all five shas of record; FULL equality on "
                f"{len(tapes())} tapes across three lenses (4h, 1d, 5m) and three symbols; "
                f"identical at wick / MULTI / lapse-open / body-redraw pins, under "
                f"overlapping macro lives, at mem_cap 1 and 2 and on the synthetic corpse "
                f"population; lean leash == full minus spam, everywhere"
                if ok else "; ".join(bad[:4]))


# ═════════════════════════════════════════════════════════ F-RF-SEAL
def _seal_findings(label: str, shift: int = 0, n_sample: int = 12) -> tuple[list[str], dict]:
    """The port's seals vs the MACHINE on prefixes: pivot k (bar b, dir) with
    seal s is ABSENT from the machine's pivots on tape[:s] and PRESENT on
    tape[:s+1]. Checked for EVERY pivot the machine stamped knowable_at = -1
    and for a seeded sample of the rest; both scales."""
    d = tapes()[label][0]
    e, p, a, _, _ = runs(label)
    rng = np.random.default_rng(SEED)
    bad, stat = [], {"pivots": 0, "minus1": 0, "prefix_checked": 0}
    for scale, pins in (("macro", RC.macro_pins(3.0)), ("micro", dict(RC.PINS))):
        em, pm = e[scale], p[scale]
        pe = [x for x in em["events"] if x["event"] == "pivot"]
        seals = [s + shift for s in pm["seals"]]
        if len(pe) != len(pm["pivots"]) or [x["i"] for x in pe] != [q[0] for q in pm["pivots"]]:
            bad.append(f"{scale}: pivot events do not align 1:1 with the port's pivots")
            continue
        stat["pivots"] += len(pe)
        minus1 = [k for k, x in enumerate(pe) if x["knowable_at"] < 0]
        stat["minus1"] += len(minus1)
        for k, x in enumerate(pe):
            if x["knowable_at"] >= 0 and x["knowable_at"] != seals[k]:
                bad.append(f"{scale} pivot@{x['i']}: knowable_at {x['knowable_at']} != "
                           f"seal {seals[k]}")
        rest = [k for k in range(len(pe)) if k not in set(minus1)]
        pick = minus1 + sorted(rng.choice(rest, size=min(n_sample, len(rest)),
                                          replace=False).tolist())
        for k in pick:
            b, _, dirn = pm["pivots"][k]
            s = seals[k]
            if not (b < s < len(d)):
                bad.append(f"{scale} pivot@{b}: seal {s} is not a later bar on the tape")
                continue
            have = lambda cut: (b, dirn) in {(q[0], q[2]) for q in E.run_machine(
                d.iloc[:cut].reset_index(drop=True), pins)["pivots"]}
            stat["prefix_checked"] += 1
            if have(s) or not have(s + 1):
                bad.append(f"{scale} pivot@{b}: NOT first knowable at bar {s} on the "
                           f"machine's own prefixes")
    return bad, stat


def seal_break():
    return plants([
        ("SEAL PLANT (every seal read ONE BAR EARLY on SOLUSDT 1d — a one-bar look-ahead)",
         lambda: _seal_findings("SOLUSDT 1d FULL", shift=-1)[0]),
        ("SEAL PLANT (every seal read one bar LATE on the BTC 4h record tape)",
         lambda: _seal_findings("BTCUSDT 4h RECORD", shift=+1)[0]),
    ])


def seal_real():
    bad, total = [], 0
    for label in tapes():
        if "5m" in label:
            continue                       # prefix runs on 60k bars cost the machine minutes
        b, st = _seal_findings(label)
        bad += [f"{label}: {x}" for x in b]
        total += st["minus1"]
        say(f"        {label}: {st['pivots']} pivots (both scales) · the machine ships "
            f"knowable_at = -1 on {st['minus1']} · {st['prefix_checked']} seals proven on "
            f"machine prefixes")
    ok = not bad
    return ok, (f"every knowable_at >= 0 equals the port's seal; all {total} pivots the "
                f"machine stamps -1 (numpy-vs-Python rounding of 3+ dp prices) carry a seal "
                f"PROVEN first-knowable by the machine's own prefix runs — FINDING: a reader "
                f"of knowable_at sees those pivots from bar 0; read out['seals']"
                if ok else "; ".join(bad[:4]))


# ════════════════════════════════════════════════════════ F-RF-KNOWN
KNOWN_TAPES = (("ETHUSDT 4h FULL", 6000), ("SOLUSDT 1d FULL", None))
KNOWN_CUTS = 40


def _known_findings(law: str) -> tuple[list[str], dict]:
    """PREFIX-STABILITY: for seeded random cuts t, the port's logs on tape[:t]
    must equal its full logs filtered by known_at <= t - 1 (both sides
    filtered by their OWN known_at, so a prefix's "truncated by tape end"
    verdict — an artifact of the cut — drops out of both). `law`:
      port        RC.machine_known_at / RC.leash_known_at       (the real leg)
      naive       known_at = the event's own i                  (sabotage)
      knowable_at pivots read from the machine's knowable_at    (sabotage)"""
    hold = RC.PINS_V2["FLIP_HOLD_BARS"]
    rng = np.random.default_rng(SEED)
    bad, stat = [], {"cuts": 0, "events": 0, "late_known": 0}

    def k_machine(m):
        if law == "port":
            return RC.machine_known_at(m)
        if law == "naive":
            return [e["i"] for e in m["events"]]
        return [e["knowable_at"] if e["event"] == "pivot" else e["i"] for e in m["events"]]

    def k_leash(le):
        return RC.leash_known_at(le, hold) if law != "naive" else [e["i"] for e in le]

    for label, head in KNOWN_TAPES:
        d = tapes()[label][0]
        d = d if head is None else d.iloc[:head].reset_index(drop=True)
        a = atr_of(d)                  # Wilder RMA seeded at TR[0]: a[:t] IS the prefix's ATR
        full = RC.run_v2(d, a, RC.PINS_V2, with_micro=False)
        fk, lk = k_machine(full["macro"]), k_leash(full["leash"])
        stat["events"] += len(fk) + len(lk)
        stat["late_known"] += sum(1 for e, k in zip(full["macro"]["events"], fk) if k != e["i"])
        stat["late_known"] += sum(1 for e, k in zip(full["leash"], lk) if k != e["i"])
        for t in sorted(rng.integers(200, len(d), size=KNOWN_CUTS).tolist()):
            dp = d.iloc[:t].reset_index(drop=True)
            pre = RC.run_v2(dp, a[:t], RC.PINS_V2, with_micro=False)
            stat["cuts"] += 1
            for name, f_ev, f_k, p_ev, p_k in (
                    ("macro", full["macro"]["events"], fk, pre["macro"]["events"],
                     k_machine(pre["macro"])),
                    ("leash", full["leash"], lk, pre["leash"], k_leash(pre["leash"]))):
                want = [e for e, k in zip(f_ev, f_k) if k <= t - 1]
                got = [e for e, k in zip(p_ev, p_k) if k <= t - 1]
                if sha(want) != sha(got):
                    bad.append(f"{label} cut {t} {name}: prefix log ({len(got)}) != full log "
                               f"filtered by known_at ({len(want)})")
    return bad, stat


def known_break():
    return plants([
        ("NAIVE PLANT (every event read at its own stamp bar i — a pivot at its wick, a flip "
         "at its touch)", lambda: _known_findings("naive")[0]),
        ("KNOWABLE_AT PLANT (pivots read from the machine's knowable_at, which ships -1 on "
         "SOLUSDT 1d)", lambda: _known_findings("knowable_at")[0]),
    ])


def known_real():
    bad, st = _known_findings("port")
    return not bad, (f"{st['cuts']} seeded cuts over {[x[0] for x in KNOWN_TAPES]} (macro at "
                     f"the frozen SCALE 3.0 + leash): every prefix log equals the full log "
                     f"filtered by known_at — 0 mismatches; {st['late_known']} of "
                     f"{st['events']} events are known LATER than they are stamped"
                     if not bad else f"{len(bad)} mismatches: " + "; ".join(bad[:3]))


# ══════════════════════════════════════════════════════════ F-RF-DET
def det_break():
    d = tapes()["ETHUSDT 4h FULL"][0]
    a = atr_of(d)
    # a 2 % nudge to one low was measured INERT here (no threshold crossed, and
    # the log prints prices, never the ATR) — so the plant is a wick nobody can
    # miss: one high ×1.25, a pivot by construction
    d2 = d.copy()
    d2.loc[d2.index[5000], "h"] = d2["h"].iloc[5000] * 1.25
    same = sha(RC.run_machine(d2, atr_of(d2), RC.PINS)["events"]) == sha(
        RC.run_machine(d, a, RC.PINS)["events"])
    return same, ("a perturbed tape produced the SAME log — the comparison is blind" if same
                  else "one high ×1.25 on bar 5000 changes the port's log — the equality "
                       "has teeth")


def det_real():
    d = tapes()["ETHUSDT 4h FULL"][0]
    a = atr_of(d)
    cols = {k: d[k].to_numpy(float).copy() for k in ("o", "h", "l", "c")}
    a0 = a.copy()
    r1 = RC.run_v2(d, a, RC.PINS_V2)
    r2 = RC.run_v2(d.copy(), a.copy(), RC.PINS_V2)
    bad = [k for k in ("macro", "micro") if sha(r1[k]["events"]) != sha(r2[k]["events"])]
    bad += [k for k in ("leash", "suppressed") if sha(r1[k]) != sha(r2[k])]
    if any(not np.array_equal(cols[k], d[k].to_numpy(float)) for k in cols) or \
            not np.array_equal(a0, a):
        bad.append("the port MUTATED its input")
    as_tuple = (cols["o"], cols["h"], cols["l"], cols["c"], d["ts"].tolist())
    r3 = RC.run_v2(as_tuple, a, RC.PINS_V2)
    if sha(r3["macro"]["events"]) != sha(r1["macro"]["events"]) or sha(r3["leash"]) != sha(r1["leash"]):
        bad.append("tuple-of-arrays tape != DataFrame tape")
    no_ts = RC.run_machine(as_tuple[:4], a, RC.PINS)
    if [x["i"] for x in no_ts["events"]] != [x["i"] for x in r1["micro"]["events"]] or \
            any(x["ts"] is not None for x in no_ts["events"]):
        bad.append("a tape without ts does not run to the same bars with ts None")
    m = r1["macro"]
    if round(100.0 * m["covered"].sum() / m["n_bars"], 2) != m["coverage_pct"] or \
            len(m["covered"]) != m["n_bars"] or len(m["seals"]) != m["n_pivots"]:
        bad.append("additive keys (covered / seals) disagree with the summary")
    ok = not bad
    return ok, ("byte-identical logs on re-run (macro, micro, leash, suppress); inputs "
                "never mutated; DataFrame == tuple of arrays; a ts-less tape runs to the "
                "same bars; covered mask and seals agree with coverage_pct / n_pivots"
                if ok else "; ".join(bad))


# ════════════════════════════════════════════════════════ F-RF-WALLS
PORT_PATH = ROOT / "analytics" / "rangefinder_census.py"
AN3_REGEX = r"^\s*(from|import)\s+engine\b"
AN4_BANNED = ["read_parquet", "requests", "urllib", "os.environ", "socket"]


def _code_only(source: str) -> str:
    out = []
    for tok in tokenize.generate_tokens(io.StringIO(source).readline):
        if tok.type in (tokenize.STRING, tokenize.COMMENT):
            continue
        out.append(tok.string)
    return " ".join(out)


def _an_findings(src: str) -> list[str]:
    """tests/test_analytics.py F-AN-3 + F-AN-4, replicated for PLANTED text
    (the real tests run on the real file in the real leg)."""
    bad = []
    m = re.search(AN3_REGEX, src, re.M)
    if m:
        bad.append(f"F-AN-3: imports the engine package: `{m.group(0).strip()}`")
    body = _code_only(src)
    bad += [f"F-AN-4: IO token `{t}`" for t in AN4_BANNED if t in body]
    if re.search(r"\bopen\s*\(", body):
        bad.append("F-AN-4: open( call")
    return bad


def _br14_constants() -> dict:
    """F-BR-14's constants, read as TEXT from scripts/oracle_fixtures.py —
    never imported (it imports the Oracle, another lane's live file)."""
    tree = ast.parse((ROOT / "scripts" / "oracle_fixtures.py").read_text(encoding="utf-8"))
    want = ("RANGE_DECISION_MODULES", "RANGE_MACHINE", "RANGE_BANNED_IN_DECISION",
            "RANGE_BANNED_IN_MACHINE", "RANGE_IMPORT_LINE")
    out = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) \
                and node.targets[0].id in want:
            v = node.value
            out[node.targets[0].id] = (v.args[0].value if isinstance(v, ast.Call)
                                       else ast.literal_eval(v))
    missing = [k for k in want if k not in out]
    if missing:
        raise RuntimeError(f"F-BR-14 constants not found in oracle_fixtures.py: {missing}")
    return out


def _closure(modname: str, planted: tuple[str, str] | None = None) -> set[str]:
    """sys.modules after importing `modname` in a clean subprocess. `planted`
    = (module name, source): written into a throwaway directory that goes
    FIRST on the subprocess's path [F-BR-14's _closure_src idiom]."""
    with tempfile.TemporaryDirectory(prefix="f-rf-walls-") as td:
        extra = ""
        if planted is not None:
            (Path(td) / f"{planted[0]}.py").write_text(planted[1], encoding="utf-8")
            extra = f"sys.path.insert(0,{td!r}); "
        code = ("import sys, json; sys.dont_write_bytecode = True; "
                "sys.path.insert(0,'.'); sys.path.insert(0,'scripts'); " + extra +
                f"import {modname}; print(json.dumps(sorted(set(sys.modules))))")
        out = subprocess.run([sys.executable, "-c", code], cwd=ROOT,
                             capture_output=True, text=True)
    if out.returncode != 0:
        raise RuntimeError(out.stderr[-400:])
    return set(json.loads(out.stdout.strip().splitlines()[-1]))


def _reach(who: str, closure: set[str], banned) -> list[str]:
    hits = sorted(x for x in closure if set(x.split(".")) & set(banned))
    return [f"{who} reaches {hits[:4]} (component-wise on {sorted(banned)})"] if hits else []


def _static_findings(sources: dict, pattern: str) -> list[str]:
    rx = re.compile(pattern)
    return [f"{name} imports the range machine: `{rx.search(text).group(0).strip()}`"
            for name, text in sources.items() if rx.search(text)]


def _br14_sources() -> dict:
    files = [p for p in sorted((ROOT / "engine").glob("*.py")) if p.name != "rangefinder.py"]
    files += [ROOT / "scripts" / "posture_engine.py"]
    files += sorted((ROOT / "scripts").glob("tierc*_rules.py"))
    return {str(p.relative_to(ROOT)): p.read_text(encoding="utf-8", errors="replace")
            for p in files}


def walls_break():
    src = PORT_PATH.read_text(encoding="utf-8")
    k = _br14_constants()
    rules = ROOT / "scripts" / "tierc2_rules.py"
    dec_ban = (*k["RANGE_BANNED_IN_DECISION"], "rangefinder_census")
    return plants([
        ("F-AN-3 PLANT (`from engine import rangefinder as E` in a COPY of the port)",
         lambda: _an_findings(src + "\nfrom engine import rangefinder as E\n")),
        ("F-AN-3 PLANT (the same import INDENTED inside a function — a lazy import)",
         lambda: _an_findings(src + "\ndef _x():\n    from engine import indicators\n")),
        ("F-AN-4 PLANT (`pd.read_parquet(...)` in a COPY of the port)",
         lambda: _an_findings(src + "\n_f = pd.read_parquet('x.parquet')\n")),
        ("F-BR-14 STATIC PLANT (`from engine.rangefinder import run_v2` appended to the "
         "TEXT of tierc2_rules.py, never executed)",
         lambda: _static_findings({rules.name: rules.read_text(encoding="utf-8")
                                   + "\nfrom engine.rangefinder import run_v2\n"},
                                  k["RANGE_IMPORT_LINE"])),
        ("CLOSURE PLANT (`from analytics import rangefinder_census` planted in a COPY of "
         "tierc2_rules.py — the census CONSULTED by a decision module; F-BR-14's own regex "
         "is blind to this name by design, so the closure must see it)",
         lambda: _reach("tierc2_rules", _closure("tierc2_rules", planted=(
             "tierc2_rules", rules.read_text(encoding="utf-8")
             + "\nfrom analytics import rangefinder_census\n")), dec_ban)),
    ])


def walls_real():
    bad = []
    src = PORT_PATH.read_text(encoding="utf-8")
    # 1 · the replicas are the tests' own words, or they are stale
    tests_src = (ROOT / "tests" / "test_analytics.py").read_text(encoding="utf-8")
    if AN3_REGEX not in tests_src or json.dumps(AN4_BANNED) not in tests_src:
        bad.append("this file's F-AN-3/4 replica no longer matches tests/test_analytics.py")
    bad += _an_findings(src)
    # 2 · the REAL tests, run on the real package (no cache dir, no bytecode)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    out = subprocess.run([sys.executable, "-m", "pytest", "-p", "no:cacheprovider",
                          "tests/test_analytics.py", "-k", "f_an_3 or f_an_4 or f_an_5"],
                         cwd=ROOT, capture_output=True, text=True, env=env)
    tail = (out.stdout.strip().splitlines() or ["<no output>"])[-1]
    tail = re.sub(r" in [0-9.]+s", "", tail)          # pytest prints a wall clock
    if out.returncode != 0:
        bad.append(f"pytest F-AN-3/4/5: {tail}")
    # 3 · not in _MODULES; analytics_sha() stays put (vs the committed package)
    import analytics
    if PORT_PATH.name in analytics._MODULES:
        bad.append("the port IS in analytics._MODULES — L3 says it is not")
    h = hashlib.sha256()
    unreachable = []
    for name in analytics._MODULES:
        blob = _git_blob("HEAD", f"analytics/{name}")
        if blob is None:
            unreachable.append(name)
            continue
        h.update(name.encode("utf-8"))
        h.update(blob)
    if unreachable:
        bad.append(f"HEAD blobs unreachable for {unreachable}")
    elif h.hexdigest() != analytics.analytics_sha():
        bad.append("analytics_sha() differs from the committed package — it did NOT stay put")
    # 4 · F-BR-14, legs (a)-static and (b)-closures, its own constants
    k = _br14_constants()
    dec = tuple(k["RANGE_DECISION_MODULES"])
    mods = (*dec, k["RANGE_MACHINE"], "analytics.rangefinder_census", "tierc10_rf_fixtures")
    with ThreadPoolExecutor(max_workers=len(mods)) as ex:
        clos = dict(zip(mods, ex.map(_closure, mods)))
    for m in dec:
        bad += _reach(m, clos[m], (*k["RANGE_BANNED_IN_DECISION"], "rangefinder_census"))
    bad += _reach(f"the range machine ({k['RANGE_MACHINE']})", clos[k["RANGE_MACHINE"]],
                  k["RANGE_BANNED_IN_MACHINE"])
    port_clo = clos["analytics.rangefinder_census"]
    bad += _reach("the census port", port_clo, ("engine", "scripts", "pandas", "rangefinder",
                                                "oracle_daily", "rangefinder_twin"))
    if "analytics.rangefinder_census" not in port_clo:
        bad.append("the port is absent from its own closure — the probe imported nothing")
    if k["RANGE_MACHINE"] not in clos["tierc10_rf_fixtures"]:
        bad.append("this fixture does not import the machine — F-RF-EQ compares nothing")
    sources = _br14_sources()
    bad += _static_findings(sources, k["RANGE_IMPORT_LINE"])
    rx = re.compile(k["RANGE_IMPORT_LINE"])
    mine = [ln for ln in src.splitlines() if rx.search(ln)]
    if mine:
        bad.append(f"the port spells a range-machine import line: {mine[:1]}")
    ok = not bad
    return ok, (f"F-AN-3/4 replica clean AND the real tests pass ({tail}); the port is NOT in "
                f"analytics._MODULES and analytics_sha() {analytics.analytics_sha()[:16]}… == "
                f"the committed package's [FINDING, L3: unhashed code inside the package, "
                f"disclosed]; F-BR-14 static leg clean over {len(sources)} files; closures: "
                f"{len(dec)} decision modules reach neither `rangefinder` nor "
                f"`rangefinder_census`, the machine reaches no `analytics`, the port reaches "
                f"no engine / pandas ({len(port_clo)} modules). NOT replicated: F-BR-14's "
                f"AST / behaviour / tape legs — they judge oracle_daily.py, which Stage 0a "
                f"does not touch" if ok else "; ".join(bad[:4]))


# ═══════════════════════════════════════════════════════ F-RF-ANCHOR
SUITES = (("v1", "rangefinder_fixtures.py"), ("v2", "rangefinder_fixtures_v2.py"))
RECORD_RED = {"v1": {"F-RF-2", "F-RF-7"}, "v2": {"F-RF-9", "F-RF-7c"}}


def _ride(which: str, fname: str, live: bool) -> tuple[list[str], list[str], str]:
    """Import one RF suite fresh and run its main() IN-PROCESS -> (PASSED,
    FAILED, tape line). The v2 suite's main() writes FIXTURES_v2.txt under
    RF.OUT; that write is pointed at a throwaway directory so a sabotage ride
    can never file '4/8 GREEN' as the suite's status of record."""
    argv, out_dir = sys.argv, RF.OUT
    sys.argv = [fname] + (["--live"] if live else [])
    buf = io.StringIO()
    try:
        spec = importlib.util.spec_from_file_location(
            f"_rf_suite_{which}_{'live' if live else 'rec'}", ROOT / "scripts" / fname)
        mod = importlib.util.module_from_spec(spec)
        with contextlib.redirect_stdout(buf):
            spec.loader.exec_module(mod)
            with tempfile.TemporaryDirectory(prefix="f-rf-anchor-") as td:
                if which == "v2":
                    RF.OUT = Path(td)
                mod.main()
    finally:
        sys.argv, RF.OUT = argv, out_dir
    tape = next((ln for ln in buf.getvalue().splitlines() if ln.startswith("TAPE:")), "TAPE: ?")
    return list(mod.PASSED), list(mod.FAILED), tape


def _tape_sha(d: pd.DataFrame) -> str:
    return hashlib.sha256(d[["t0", "o", "h", "l", "c"]].to_csv(index=False).encode()).hexdigest()


def _anchor_findings(anchor_ms: int) -> list[str]:
    """Is `anchor_ms` the anchor of record? Three independent sources."""
    bad = []
    m = re.search(r"open_time <= (\d+)", E.__doc__ or "")
    if not m or int(m.group(1)) != anchor_ms:
        bad.append(f"the machine's header names open_time <= {m.group(1) if m else '?'}, "
                   f"not {anchor_ms}")
    for fname, key in (("BTCUSD_4h_ranges_v2.json", "v2"), ("BTCUSD_1d_ranges_v1.json", "v1")):
        p = RF.OUT / fname
        if not p.exists():
            bad.append(f"export of record {fname} ABSENT (gitignored) — silence is not health")
            continue
        w = json.loads(p.read_text())["window"]
        if key == "v2":
            d = RF.bars_4h(anchor_ms=anchor_ms)
            end_ms = int(pd.Timestamp(w["end"], tz="UTC").value // 10 ** 6)
            if end_ms != anchor_ms:
                bad.append(f"v2 export window.end {w['end']} = {end_ms} != {anchor_ms}")
            got = {"start": d["ts"].iloc[0], "end": d["ts"].iloc[-1], "bars": int(len(d))}
            if any(w[x] != got[x] for x in got):
                bad.append(f"v2 export window {w} != the anchored tape {got}")
            if not _tape_sha(d).startswith(RECORD_TAPE_SHA8):
                bad.append(f"anchored 4h tape sha {_tape_sha(d)[:16]}… is not the tape of "
                           f"record {RECORD_TAPE_SHA8}…")
        else:
            d = RF.daily_bars(anchor_ms=anchor_ms)
            got = {"start": d["ts"].iloc[0], "end": d["ts"].iloc[-1], "bars": int(len(d)),
                   "dropped_incomplete_days": int(d.attrs["dropped_incomplete_days"])}
            if any(w[x] != got[x] for x in got):
                bad.append(f"v1 export window {w} != the anchored tape {got}")
    return bad


def anchor_break():
    def live_ride():
        found = []
        for which, fname in SUITES:
            passed, failed, tape = _ride(which, fname, live=True)
            red = {f.split(" ")[0] for f in failed}
            say(f"      un-anchored {which}: {len(passed)}/8 GREEN · RED {sorted(red)} · {tape[:70]}")
            if RECORD_RED[which] <= red:
                found.append(f"{which}: {sorted(RECORD_RED[which])} RED on the sliding tail")
        return found if len(found) == len(SUITES) else []
    return plants([
        ("ANCHOR PLANT (the anchor moved ONE 4h bar later)",
         lambda: _anchor_findings(RC.RECORD_ANCHOR_MS + H4_MS)),
        ("UN-ANCHORED RIDE (both suites on the tail of the frozen snapshot — the four "
         "record legs must go RED, or the anchor is not what restores them)", live_ride),
    ])


def anchor_real():
    bad = []
    if RF.RECORD_ANCHOR_MS != RC.RECORD_ANCHOR_MS:
        bad.append(f"twin anchor {RF.RECORD_ANCHOR_MS} != port anchor {RC.RECORD_ANCHOR_MS}")
    bad += _anchor_findings(RF.RECORD_ANCHOR_MS)
    # the twin's 1D law and this file's independent L1 resample are one tape
    mine, twin = tapes()["BTCUSDT 1d RECORD"][0], RF.daily_bars(anchor_ms=RF.RECORD_ANCHOR_MS)
    if _tape_sha(mine) != _tape_sha(twin):
        bad.append("the twin's anchored daily tape != the independent L1 resample")
    # the default is still LIVE: no non-fixture caller changed behaviour
    for fn in (RF.daily_bars, RF.bars_4h):
        if inspect.signature(fn).parameters["anchor_ms"].default is not None:
            bad.append(f"{fn.__name__}: anchor_ms does not default to None (live)")
    live4 = klines("BTCUSDT", "4h")
    if _tape_sha(RF.bars_4h()) != _tape_sha(tape_4h(live4, E.V2_WINDOW_BARS)):
        bad.append("bars_4h() default is no longer the live tail(1700)")
    if _tape_sha(RF.daily_bars()) != _tape_sha(
            tape_1d(live4).tail(RF.WINDOW_BARS).reset_index(drop=True)):
        bad.append("daily_bars() default is no longer the live tail(420 complete days)")
    for which, fname in SUITES:
        passed, failed, tape = _ride(which, fname, live=False)
        say(f"      anchored {which}: {len(passed)}/8 GREEN"
            + (f" · FAILED {failed}" if failed else "") + f" · {tape}")
        if failed or len(passed) != 8:
            bad.append(f"{which} suite at the anchor: {len(passed)}/8, FAILED {failed}")
    ok = not bad
    return ok, (f"anchor {RF.RECORD_ANCHOR_MS} = {iso(RF.RECORD_ANCHOR_MS)} (bar OPEN) is "
                f"DERIVED three ways — the machine's header, the v2 export's window.end "
                f"(1700 bars from 2025-11-12T00:00, tape sha {RECORD_TAPE_SHA8}…), the v1 "
                f"export's window (420 days to 2026-08-21, 2 incomplete days dropped); both "
                f"suites 8/8 GREEN on it; the loaders still default to the live tail"
                if ok else "; ".join(bad[:4]))


# ════════════════════════════════════════════════════════════ main
LEGS = (
    ("F-RF-PINS", "port literals == machine pins == Pine defaults; STEP 0 shas re-asserted",
     "any port pin (value or key order), ATR_LEN, V2_WINDOW_BARS or MEM_CAP_PER_SIDE differs "
     "from the machine's, or from the Pine input defaults; the port's pins are the machine's "
     "own objects; a STEP 0 literal is not the sha of the STEP 0 blob; the twin differs from "
     "its STEP 0 blob anywhere but its two loaders + RECORD_ANCHOR_MS. (A pine/engine file "
     "that MOVED since STEP 0 is printed, not failed: another lane is live.)",
     pins_break, pins_real),
    ("F-RF-EQ", "the port IS the machine — shas of record, three tapes more, off-default pins",
     "any of the five event logs on the frozen record tape does not hash to its sha OF RECORD "
     "from the machine AND from the port; any event log, Range field, pivot, summary number "
     "or kept set differs on any tape or pin set; the lean leash is not the full leash minus "
     "its two spam classes; a case meant to exercise a branch exercises nothing.",
     eq_break, eq_real),
    ("F-RF-SEAL", "out['seals'] is the knowability the machine's knowable_at can lose",
     "a knowable_at >= 0 differs from the port's seal; or a checked pivot is present on the "
     "machine's prefix ending BEFORE its seal, or absent on the prefix ending AT it.",
     seal_break, seal_real),
    ("F-RF-KNOWN", "the as-of law — known_at makes the log prefix-stable, `i` does not",
     "for any seeded cut t the port's macro or leash log on tape[:t] differs from its full "
     "log filtered by known_at <= t - 1.",
     known_break, known_real),
    ("F-RF-DET", "the port is pure — same bytes, inputs untouched, frame == arrays",
     "two runs differ; an input array is mutated; a tuple-of-arrays tape and a DataFrame "
     "tape differ; the additive keys disagree with the summary.",
     det_break, det_real),
    ("F-RF-WALLS", "I-B / I-A / F-BR-14 — the port lives under analytics/ and breaks no wall",
     "the port imports the engine package or spells an IO token; the real F-AN-3/4/5 tests "
     "fail; the port is in analytics._MODULES or analytics_sha() moved; any decision closure "
     "reaches `rangefinder` or `rangefinder_census`; the machine's closure reaches "
     "`analytics`; the port's closure reaches engine or pandas; F-BR-14's import-line regex "
     "fires on any file it scans.",
     walls_break, walls_real),
    ("F-RF-ANCHOR", "the record anchor is derived, and it is what makes the F-RF suites ride",
     "the anchor is not the one the machine's header, the v2 export and the v1 export all "
     "name; the anchored tapes are not the exports' windows / the tape sha of record; either "
     "suite is not 8/8 at the anchor; a loader no longer defaults to the live tail.",
     anchor_break, anchor_real),
)


def main() -> int:
    env = os.environ.get("NAIAD_CACHE_DIR")
    if not env or Path(env).resolve() == LIVE_CACHE.resolve():
        print("*** HALT: NAIAD_CACHE_DIR must be exported to the FROZEN snapshot before python "
              "starts [TIER-C10 law 3]; the live cache is read-never for TC10. ***")
        return 2
    want = [a.lower().replace("_", "-") for a in sys.argv[1:]]
    legs = [x for x in LEGS if not want or any(w in x[0].lower() for w in want)]
    btc = klines("BTCUSDT", "4h")
    say(f"as_of_last_closed_4h: {iso(int(btc['open_time'].iloc[-1]) + H4_MS)}")
    say(f"as_of_record_anchor_bar_open: {iso(RC.RECORD_ANCHOR_MS)}")
    say("=" * 78)
    say("TIER-C10 STAGE 0a · RANGEFINDER CENSUS PORT FIXTURES — break leg first, RED or void")
    say("=" * 78)
    say(f"seed {SEED} · substrate NAIAD_CACHE_DIR={env}")
    for sym, tf in (("BTCUSDT", "4h"), ("ETHUSDT", "4h"), ("SOLUSDT", "4h"), ("SOLUSDT", "5m")):
        p = cache_dir() / "klines" / f"{sym}_{tf}.parquet"
        f = klines(sym, tf)
        say(f"  {p.name:22} sha256 {file_sha(p)[:16]}…  {len(f):>7,} bars  as_of_lens {tf}  "
            f"as_of_last_bar_open {iso(int(f['open_time'].iloc[-1]))}")
    say(f"  port {PORT_PATH.relative_to(ROOT)} sha256 {file_sha(PORT_PATH)}")
    for ln in LEANS:
        say(ln)
    for fid, title, fails_if, b, r in legs:
        prove(fid, title, fails_if, b, r)
    say(f"\nTIER-C10 RF FIXTURES: {len(PASSED)}/{len(legs)} GREEN"
        + (f" · FAILED: {FAILED}" if FAILED else ""))
    say("warranty: these lines are true AS OF the substrate and the bars named above and of "
        "no other; the corridor advances with the cache [TC6V-a]")
    if not want:                       # a partial run never overwrites the full transcript
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / "FIXTURES_RF.txt").write_text("\n".join(T) + "\n", encoding="utf-8")
        print(f"transcript -> {(OUT / 'FIXTURES_RF.txt').relative_to(ROOT)}")
    if FAILED:
        print("*** HALT: fixture mismatch. Nothing downstream is trustworthy. ***")
    return 1 if FAILED else 0


if __name__ == "__main__":
    raise SystemExit(main())
