#!/usr/bin/env python
"""TIER-C11 · TC11-R · THE RANGE LAYER [LEANS L-0.3, L-R.1..L-R.6, L-F.2].

Contract of record: exchange/queue/2026-09-24_TC11_APOLLO.md (sha256 bb38e016…,
STEP Q b9ed953).  Executor HEPHAESTUS; seed 20260924.  Executor readings:
research_outputs/tierc11/LEANS.md (frozen at 4ed4e67).  THIS IS THE ONLY TC11
MODULE THAT MAY IMPORT THE RANGE MACHINE (L-0.3): it imports tierc11_env (the
range-free shim) and then tierc10_census, tierc10_stamps and tierc10_null through
the shim's range door (`E.tc10_import(..., allow_range=True)`, which opens for a
caller named tierc11_nest and for no other).  Decision modules never import it:
they receive `range_facts(...)` — a plain dict of numpy arrays (L-F.2).

WHAT IT DOES, IN ORDER
  1. SHIM.  The second import window; the C.* / stamps.* / null.* entries of the
     L-0.3 closed list re-rooted onto TC11 (C.SNAPSHOT, C.OUT, C.STAGE_D,
     C.NULL_ROOT, C.SEED; C.LENSES / LENS_MS / LENS_SOURCE / TS_FMT extended IN
     PLACE for 15m, 1h, 12h, 1w; stamps.SNAPSHOT / OUT / LENS_MS) plus every
     other TC10 binding a grep of the three modules finds (each named, with its
     reason).  The label leak at tierc10_census.py:520 (toll_bps_for names
     TC10's fee file while reading TC11's) is overridden.  C.RETEST_PINS is
     re-resolved from the ABSOLUTE MAIN-TREE TUNING_RESULT.json.  The post-shim
     assertion (the handoff tierc11_env names) HALTs unless C.as_of_close_ms(s)
     == 1790294400000 for every CLASSIC5 and UNSEEN12 stem and C.RETEST_PINS ==
     {margin 1.0, hold 3, ttl 400, grid_sha 2135ca66…}.
  2. PINS [L-R.3].  sha256(analytics/rangefinder_census.py) == STEP0_RECORD's
     port sha 19c5507f…, sha256(engine/rangefinder.py) == bbae464f…, the 12
     live pins == STEP0_RECORD.pins_of_record in key order, the retest grid
     sha == 2135ca66….  HALT on any mismatch; the pins block is printed.
  3. LOADER.  load11(stem, lens) for {5m, 15m, 1h, 4h, 12h, 1d, 1w}: C.load_tape
     through the extended dicts — closed bars <= the pin, full history, ATR =
     engine.indicators.atr(h, l, c, 14) on the WHOLE tape.  1d is derived from
     native 4h and HALTs unless it equals Stage D's derived 1d file (C's own
     law); 1w reads Stage D's derived 1w file and is cross-checked here against
     D.derive_1w(D.derive_1d(native 4h)).
  4. SCALE PICKS [L-R.2].  Per CLASSIC5 x 7 lenses and UNSEEN12 x {1h, 4h, 1d}:
     the tuning pick C.calibrate(tape.head(C.era_cut(tape))) (era by bar CLOSE
     <= 1719791999000, verified); the whole-tape fallback (labelled IN-SAMPLE)
     when the tuning head holds < 400 bars; the whole-tape pick; the first-half-
     of-tuning pick (stability); frozen 3.0.  calibrate()'s hard-coded
     calibrated_in_sample=True is overwritten with the true flag.  FILED ONCE:
     research_outputs/tierc11/ranges/SCALE_PICKS.json (write-once — the picks
     are pins) + SCALE_GRID.parquet + SCALE_PICKS.md + the provenance sidecar
     SCALE_PICKS_SOURCES.json (each cell's input file and sha256).  Every reader
     takes the pick from SCALE_PICKS.json (`scale_of`) and never re-fits; every
     row that reads a lens carries its honesty labels (`scale_label`).
  5. VIEWS.  view11(stem, lens, scale_kind) -> (tape, run_scale output,
     asof_view), memoised in-process.
  6. NEST VECTOR [L-R.5].  nest_at(stem, instants_ms, scale_kind): one row per
     instant; per L in {1h, 4h, 12h, 1d, 1w}, read at the last CLOSED bar of L
     at or before the instant.
  7. EVENTS [L-R.6], all AS-OF: deaths, hardens, memory lines, the FIRST-
     RETEST-THAT-HOLDS scan (tap89 / tap127 / tap200 and the memory line), the
     one-shot twins, and the L+1 cell classifier.
  8. DECISION ADAPTER [L-F.2]: range_facts(stem, lens, scale_kind).

NEVER READ: Range.top / .bottom / .n_deviations (end-of-run values — the
leaked-redraw sabotage), and never a price out of an event (2-dp rounded).
Boundaries come from C.asof_view, rebuilt from raw bars at full precision.

Run:  export NAIAD_CACHE_DIR=$HOME/.cache/naiad/snapshots/tc11_20260925 PYTHONDONTWRITEBYTECODE=1
      ~/venvs/naiad/bin/python -B scripts/tierc11_nest.py                 # lean + pins block
      ~/venvs/naiad/bin/python -B scripts/tierc11_nest.py --build-picks [--procs=N] [--out=DIR]
      ~/venvs/naiad/bin/python -B scripts/tierc11_nest.py --file-sources   # the sidecar, once
Import (runners only):  import tierc11_nest as N
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import tierc11_env as E                                              # noqa: E402  (guards first)

import numpy as np                                                   # noqa: E402
import pandas as pd                                                  # noqa: E402

# ══════════════════════════════════════════ 1 · THE SECOND IMPORT WINDOW
# Each import runs inside the shim's env window (NAIAD_CACHE_DIR -> the TC10
# snapshot for that one statement: TC10's assert_substrate demands it), with the
# armed audit hook watching.  The door opens only because THIS module's name is
# tierc11_nest.
C = E.tc10_import("tierc10_census", allow_range=True)
ST = E.tc10_import("tierc10_stamps", allow_range=True)
NL = E.tc10_import("tierc10_null", allow_range=True)
RC = C.RC                                   # analytics.rangefinder_census (the port)
from engine import indicators as IND                                 # noqa: E402

ROOT = E.ROOT
OUT = E.OUT / "ranges"                      # research_outputs/tierc11/ranges
PIN_MS = E.PIN_MS
PIN_ISO = E.PIN_ISO
SEED = E.SEED
LEAN_TAG = E.LEAN_TAG
LENS_MS = dict(E.LENS_MS)                   # 5m 15m 1h 4h 12h 1d 1w
LENSES11 = ("5m", "15m", "1h", "4h", "12h", "1d", "1w")
NEST_LENSES = ("1h", "4h", "12h", "1d", "1w")                 # [L-R.5]
LADDER = {"1h": "4h", "4h": "12h", "12h": "1d", "1d": "1w", "1w": None}
CLASSIC5 = tuple(E.CLASSIC5)
UNSEEN12 = tuple(E.UNSEEN12)
LENSES_OF = {**{s: LENSES11 for s in CLASSIC5},
             **{s: ("1h", "4h", "1d") for s in UNSEEN12}}      # [L-R.1]
SCALE_KINDS = ("calibrated", "frozen3.0")
TUNE_MIN_BARS = int(C.TUNE_MIN_BARS)        # 400 [L-R.2]
COIN_FRAC = 0.25                            # [L-R.5] boundary coincidence, x ATR_L
MID_BAND = (25.0, 75.0)                     # [L-R.6] "in-range mid"
SCAN_BANDS = ("tap89", "tap127", "tap200")  # [L-R.6(a)]
INF = int(np.iinfo(np.int64).max)

# ══════════════════════════════════════════ 2 · THE CLOSED RE-ROOT LIST (C.* / ST.*)
_NEW_LENS_MS = {k: LENS_MS[k] for k in ("15m", "1h", "12h", "1w")}
_NEW_SOURCE = {"15m": "15m", "1h": "1h", "12h": "12h", "1w": "1w"}
_NEW_TS_FMT = {"15m": "%Y-%m-%dT%H:%M", "1h": "%Y-%m-%dT%H:%M",
               "12h": "%Y-%m-%dT%H:%M", "1w": "%Y-%m-%d"}
_MODS = {"C": C, "ST": ST, "NL": NL}
_C_TOLL_BPS_FOR_TC10 = C.toll_bps_for       # the census's own function, kept
_TC11_FEE_REL = "research_outputs/tierc11/data/fee_schedule.json"


def toll_bps_for11(stem: str) -> tuple[float, str]:
    """C.toll_bps_for with the TRUE source label.  After the C.STAGE_D re-root the
    census reads TC11's fee_schedule.json but still LABELS the row with TC10's
    path (tierc10_census.py:520, a literal) — the known label leak, overridden
    here.  The bps is the census function's own number, never re-typed."""
    bps, src = _C_TOLL_BPS_FOR_TC10(stem)
    if "fee_schedule.json" in src:
        src = f"{_TC11_FEE_REL}[{stem}].round_trip_bps_used"
    return bps, src


# (module, attribute, key-or-None, new value, provenance).  key != None = IN
# PLACE on that dict (every holder of the dict sees it).  "L-0.3" = the lean's
# closed list; "L-0.3+" = a binding the list missed, found by grep of the three
# modules (tierc10 / tc10_20260921 / SEED / OUT / STAGE_D / LENS_MS) and
# re-rooted under the same law.
REROOT_PLAN = (
    ("C", "SNAPSHOT", None, E.SNAPSHOT, "L-0.3"),
    ("C", "OUT", None, E.OUT / "census",
     "L-0.3 — the ONE TC11 census root, shared with the env shim's BK.TUNING_RESULT_FOR / "
     "BK.HEIGHT_VS_TOLL_PATH / _VERDICT_PATH (BK.grid_toll_atr reads through C.get_toll = "
     "C.OUT/outcome_grid.parquet) [verifier finding 10: two roots refused]"),
    ("C", "STAGE_D", None, E.OUT / "data", "L-0.3"),
    ("C", "NULL_ROOT", None, OUT / "null", "L-0.3"),
    ("C", "SEED", None, SEED, "L-0.3"),
    ("C", "LENSES", None, tuple(C.LENSES) + ("15m", "1h", "12h", "1w"),
     "L-0.3 (a TUPLE: rebound, read at call time by load_tape)"),
    ("C", "LENS_MS", "15m", _NEW_LENS_MS["15m"], "L-0.3"),
    ("C", "LENS_MS", "1h", _NEW_LENS_MS["1h"], "L-0.3"),
    ("C", "LENS_MS", "12h", _NEW_LENS_MS["12h"], "L-0.3"),
    ("C", "LENS_MS", "1w", _NEW_LENS_MS["1w"], "L-0.3 (Tape.step / head() keep the lens step)"),
    ("C", "LENS_SOURCE", "15m", "15m", "L-0.3 native"),
    ("C", "LENS_SOURCE", "1h", "1h", "L-0.3 native"),
    ("C", "LENS_SOURCE", "12h", "12h", "L-0.3 native"),
    ("C", "LENS_SOURCE", "1w", "1w", "L-0.3 the Stage-D-derived 1w file"),
    ("C", "TS_FMT", "15m", _NEW_TS_FMT["15m"], "L-0.3"),
    ("C", "TS_FMT", "1h", _NEW_TS_FMT["1h"], "L-0.3"),
    ("C", "TS_FMT", "12h", _NEW_TS_FMT["12h"], "L-0.3"),
    ("C", "TS_FMT", "1w", _NEW_TS_FMT["1w"], "L-0.3"),
    ("C", "toll_bps_for", None, toll_bps_for11,
     "finding: the label leak at tierc10_census.py:520 (TC10's fee-file path typed "
     "into the source label) — overridden; the bps is the census function's own"),
    ("ST", "SNAPSHOT", None, E.SNAPSHOT, "L-0.3"),
    ("ST", "OUT", None, OUT / "stamps", "L-0.3"),
    ("ST", "OUT_RERUN", None, E.OUT / "_det_rerun" / "stamps",
     "L-0.3+ missed: research_outputs/tierc10_run2/stamps (the env's _det_rerun law)"),
    ("ST", "SEED", None, SEED, "L-0.3+ missed: stamps' own seed, bound at import"),
    ("ST", "LENS_MS", "15m", _NEW_LENS_MS["15m"], "L-0.3 (dict(C.LENS_MS) copied at import)"),
    ("ST", "LENS_MS", "1h", _NEW_LENS_MS["1h"], "L-0.3"),
    ("ST", "LENS_MS", "12h", _NEW_LENS_MS["12h"], "L-0.3"),
    ("ST", "LENS_MS", "1w", _NEW_LENS_MS["1w"], "L-0.3"),
    ("NL", "SEED", None, SEED, "L-0.3+ missed: null.SEED = C.SEED copied at import"),
    ("NL", "OUT", None, OUT / "null", "L-0.3+ missed: research_outputs/tierc10/null"),
)
# TC10 bindings of C / ST / NL deliberately LEFT, each with its reason.  Anything
# else still naming TC10 HALTs the post-shim assertion.
NOT_REROOTED = {
    "tierc10_census.LIVE_CACHE": "a GUARD constant: the path assert_substrate refuses, never read",
    "tierc10_stamps.LIVE_CACHE": "a GUARD constant: the path assert_substrate refuses, never read",
}
REROOTS: list[dict] = []


def _reroot(alias: str, attr: str, key, new, why: str) -> None:
    mod = _MODS[alias]
    if not hasattr(mod, attr):
        raise SystemExit(f"HALT: RE-ROOT {alias}.{attr}: no such name in {mod.__name__} — "
                         f"the closed list names a binding that does not exist [L-0.3]")
    cur = getattr(mod, attr)
    if key is None:
        old = cur
        setattr(mod, attr, new)
        name = f"{alias}.{attr}"
    else:
        if not isinstance(cur, dict):
            raise SystemExit(f"HALT: RE-ROOT {alias}.{attr}[{key!r}]: not a dict")
        old = cur.get(key, "(absent)")
        cur[key] = new
        name = f"{alias}.{attr}[{key!r}]"
    REROOTS.append({"name": name, "old": E._show(old) if not callable(old) else
                    f"{old.__module__}.{old.__name__}",
                    "new": E._show(new) if not callable(new) else
                    f"{new.__module__}.{new.__name__}", "why": why})


for _alias, _attr, _key, _new, _why in REROOT_PLAN:
    _reroot(_alias, _attr, _key, _new, _why)

# C.RETEST_PINS re-resolved from the ABSOLUTE MAIN-TREE TUNING_RESULT.json [L-0.3,
# buildability 8]: in a review worktree the ROOT-relative census dir is absent
# (gitignored) and the import-time resolution would silently fall back to the
# PROVISIONAL pins (hold 6, no grid sha).
_TUNING_REL = "research_outputs/tierc10/census/TUNING_RESULT.json"
C.RETEST_PINS = C.resolve_retest_pins(E.tc10_record(_TUNING_REL).parent)
# The import-time value is NOT printed: it is tree-dependent (TUNED in the main
# tree, PROVISIONAL in a review worktree, where the ROOT-relative dir is absent),
# and every transcript byte must be the same in both trees [verifier finding 3].
REROOTS.append({"name": "C.RETEST_PINS",
                "old": ("as resolved at census import from the ROOT-relative census dir "
                        "(tree-dependent — gitignored, absent in a review worktree — so not "
                        "printed)"),
                "new": (f"re-resolved from the absolute main-tree {_TUNING_REL}: margin_atr "
                        f"{C.RETEST_PINS.get('margin_atr')!r} · hold_bars "
                        f"{C.RETEST_PINS.get('hold_bars')!r} · ttl_bars "
                        f"{C.RETEST_PINS.get('ttl_bars')!r} · grid_sha "
                        f"{C.RETEST_PINS.get('grid_sha')!r} · status "
                        f"{C.RETEST_PINS.get('status')!r}"),
                "why": "L-0.3 / buildability 8: TC10 records are read by absolute main-tree path"})

# ══════════════════════════════════════════ 3 · THE PINS [L-R.3]
PORT_REL = "analytics/rangefinder_census.py"
ENGINE_REL = "engine/rangefinder.py"
PORT_SHA = "19c5507ff2d39b68aa119ff701aef58a2d219fa287c34cdf7302ebf2bbb7b37d"
ENGINE_SHA = "bbae464fdc8e0e01fc90b286aa79e726fcff4422e6118dee1173f2460dab84d4"
RETEST_GRID_SHA = "2135ca663a7c407ca1a2a99165692bd3a9a9cd90de458e03dabdc2e32855e7b3"
RETEST_OF_RECORD = {"margin_atr": 1.0, "hold_bars": 3, "ttl_bars": 400,
                    "grid_sha": RETEST_GRID_SHA}
STEP0_REL = "research_outputs/tierc10/STEP0_RECORD.json"
NOT_IN_THE_TWELVE = ("REDRAW_BASIS", "MULTI_ACTIVE")   # the as-of recipe's two
                                                      # preconditions, asserted apart


def sha_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def live_pins() -> list[tuple[str, object]]:
    """The 12 live pins in EXPORT ORDER: RC.PINS | RC.PINS_V2 | ATR_LEN, minus the
    two as-of recipe preconditions STEP0_RECORD does not carry."""
    live = {**RC.PINS, **RC.PINS_V2, "ATR_LEN": RC.ATR_LEN}
    return [(k, v) for k, v in live.items() if k not in NOT_IN_THE_TWELVE]


def step0_record() -> dict:
    return json.loads(E.tc10_record(STEP0_REL).read_text(encoding="utf-8"))


def pins_findings(port_sha: str, engine_sha: str, pins: list, record: dict,
                  retest: dict, port_file: str) -> list[str]:
    """[L-R.3] every way the range machine can have moved from TC10's STEP 0.
    Each finding starts with its detector: PORT-SHA · ENGINE-SHA · PINS-12 ·
    PINS-ORDER · RETEST-PINS · PORT-FILE · RECIPE."""
    bad = []
    src = record.get("sources") or {}
    exp_port = (src.get(PORT_REL) or {}).get("sha256_expected")
    exp_eng = (src.get(ENGINE_REL) or {}).get("sha256_expected")
    if not (port_sha == exp_port == PORT_SHA):
        bad.append(f"PORT-SHA: {PORT_REL} hashes {port_sha}, STEP0_RECORD expects "
                   f"{exp_port}, the literal of record {PORT_SHA}")
    if not (engine_sha == exp_eng == ENGINE_SHA):
        bad.append(f"ENGINE-SHA: {ENGINE_REL} hashes {engine_sha}, STEP0_RECORD expects "
                   f"{exp_eng}, the literal of record {ENGINE_SHA}")
    rec = record.get("pins_of_record") or {}
    order = list(record.get("pins_key_order") or [])
    if [k for k, _ in pins] != list(rec) or list(rec) != order:
        bad.append(f"PINS-ORDER: live key order {[k for k, _ in pins]} vs pins_of_record "
                   f"{list(rec)} vs pins_key_order {order} — export order is bytes")
    for k, v in pins:
        if k in rec and (type(v) is not type(rec[k]) or v != rec[k]):
            bad.append(f"PINS-12: pin {k} live {v!r} ({type(v).__name__}) != record "
                       f"{rec[k]!r} ({type(rec[k]).__name__})")
    if len(pins) != 12 or len(rec) != 12:
        bad.append(f"PINS-12: {len(pins)} live pins / {len(rec)} recorded — the record is 12")
    for k, want in RETEST_OF_RECORD.items():
        if retest.get(k) != want:
            bad.append(f"RETEST-PINS: C.RETEST_PINS[{k!r}] = {retest.get(k)!r} != {want!r}")
    if os.path.realpath(port_file) != os.path.realpath(ROOT / PORT_REL):
        bad.append(f"PORT-FILE: the imported port is {E.rel_of(E._real(port_file))}, not "
                   f"{E.rel_of(E._real(ROOT / PORT_REL))} (tree-relative)")
    if RC.PINS.get("REDRAW_BASIS") != "wick" or RC.PINS.get("MULTI_ACTIVE") != 0:
        bad.append(f"RECIPE: REDRAW_BASIS {RC.PINS.get('REDRAW_BASIS')!r} / MULTI_ACTIVE "
                   f"{RC.PINS.get('MULTI_ACTIVE')!r} — the as-of recipe needs 'wick' / 0")
    return bad


def pins_inputs() -> dict:
    return {"port_sha": sha_file(ROOT / PORT_REL), "engine_sha": sha_file(ROOT / ENGINE_REL),
            "pins": live_pins(), "record": step0_record(), "retest": dict(C.RETEST_PINS),
            "port_file": RC.__file__}


_PINS_IN = pins_inputs()
_PINS_BAD = pins_findings(**_PINS_IN)
if _PINS_BAD:
    raise SystemExit("HALT: PINS [L-R.3] — " + " | ".join(_PINS_BAD))


def pins_block() -> str:
    P = _PINS_IN
    L = [f"{LEAN_TAG} L-R.3 PINS = TC10 sha — verified at import, HALT on any mismatch:"]
    L.append(f"  {PORT_REL} sha256 {P['port_sha']} == STEP0_RECORD sha256_expected == "
             f"literal: {P['port_sha'] == PORT_SHA}")
    L.append(f"  {ENGINE_REL} sha256 {P['engine_sha']} == STEP0_RECORD sha256_expected == "
             f"literal: {P['engine_sha'] == ENGINE_SHA}")
    L.append(f"  the 12 pins, key order of record ({STEP0_REL} pins_of_record; "
             f"{P['record'].get('pins_reconciled')}):")
    for k, v in P["pins"]:
        L.append(f"    {k:<17} {v!r}")
    L.append(f"  recipe preconditions (not in the 12; asof_view asserts them): REDRAW_BASIS "
             f"{RC.PINS['REDRAW_BASIS']!r} · MULTI_ACTIVE {RC.PINS['MULTI_ACTIVE']!r} · "
             f"MEM_CAP_PER_SIDE {RC.MEM_CAP_PER_SIDE}")
    R = P["retest"]
    L.append(f"  C.RETEST_PINS: margin_atr {R['margin_atr']} · hold_bars {R['hold_bars']} · "
             f"ttl_bars {R['ttl_bars']} · grid_sha {R['grid_sha']} · status {R['status']!r} "
             f"(the ONE 5m-tuned pair, applied to every lens)")
    return "\n".join(L) + "\n"


# ══════════════════════════════════════════ 4 · THE POST-SHIM ASSERTION (the handoff)
POST_SHIM: list[str] = []


def _post_shim() -> None:
    bad: list[str] = []

    def chk(ok: bool, clause: str, detail: str) -> None:
        POST_SHIM.append(f"{'ok ' if ok else 'BAD'} {clause}: {detail}")
        if not ok:
            bad.append(f"{clause}: {detail}")

    # THE ROOTS FIRST, and a HALT at once if they are not TC11's: every later
    # clause READS through C.STAGE_D / C.SNAPSHOT, and a read through a TC10 root
    # would be judged by whichever guard the TREE happens to trip (the audit hook
    # in the main tree; nothing in a review worktree, where research_outputs/
    # tierc10 is absent) — one detector in both trees [verifier finding 2].
    roots_ok = (E._real(C.STAGE_D) == E._real(E.OUT / "data")
                and E._real(C.SNAPSHOT) == E._real(E.SNAPSHOT))
    chk(roots_ok, "C.STAGE_D / C.SNAPSHOT are TC11's (checked FIRST; no read goes through a "
        "TC10 root)", f"{E.rel_of(E._real(C.STAGE_D))} · {Path(C.SNAPSHOT).name}")
    if not roots_ok:
        raise SystemExit("HALT: POST-SHIM [L-0.3, tierc11_nest] — " + " | ".join(bad))
    census = {"C.OUT": C.OUT, "BK.TUNING_RESULT": E.BK.TUNING_RESULT.parent,
              "BK.HEIGHT_VS_TOLL_PATH": E.BK.HEIGHT_VS_TOLL_PATH.parent,
              "BK.HEIGHT_VS_TOLL_VERDICT_PATH": E.BK.HEIGHT_VS_TOLL_VERDICT_PATH.parent,
              **{f"BK.TUNING_RESULT_FOR[{k!r}]": Path(v).parent
                 for k, v in sorted(E.BK.TUNING_RESULT_FOR.items())}}
    roots = sorted({E.rel_of(E._real(v)) for v in census.values()})
    chk(roots == [E.rel_of(E._real(E.OUT / "census"))],
        "one census root: C.OUT == the env shim's BK census paths' dir == "
        "research_outputs/tierc11/census", f"{len(census)} bindings -> {roots}")
    pins = {}
    for s in CLASSIC5 + UNSEEN12:
        ms, src = C.as_of_close_ms(s)
        pins[s] = (int(ms), src)
    wrong = {s: v for s, v in pins.items() if v[0] != PIN_MS}
    chk(not wrong, f"C.as_of_close_ms(s)[0] == {PIN_MS} for every CLASSIC5 + UNSEEN12 stem",
        f"{len(pins)} stems, {len(wrong)} wrong" + (f" {wrong}" if wrong else "")
        + f" · source {sorted({v[1] for v in pins.values()})}")
    R = dict(C.RETEST_PINS)
    chk(all(R.get(k) == v for k, v in RETEST_OF_RECORD.items()),
        "C.RETEST_PINS == {margin_atr 1.0, hold_bars 3, ttl_bars 400, grid_sha 2135ca66…}",
        f"margin {R.get('margin_atr')} hold {R.get('hold_bars')} ttl {R.get('ttl_bars')} "
        f"grid {str(R.get('grid_sha'))[:16]}…")
    chk(dict(C.LENS_MS) == LENS_MS and dict(ST.LENS_MS) == LENS_MS,
        "C.LENS_MS == stamps.LENS_MS == E.LENS_MS (extended in place)",
        f"{sorted(C.LENS_MS, key=LENS_MS.get)} / {sorted(ST.LENS_MS, key=LENS_MS.get)}")
    chk(set(C.LENSES) == set(LENSES11) and set(C.LENS_SOURCE) == set(LENSES11)
        and set(C.TS_FMT) == set(LENSES11),
        "C.LENSES / LENS_SOURCE / TS_FMT cover the seven lenses", f"{list(C.LENSES)}")
    probe = C.Tape("PROBE", "1w", *(np.zeros(3),) * 4, np.zeros(3, np.int64), ["", "", ""],
                   np.ones(3))
    chk(probe.head(2).step == LENS_MS["1w"], "C.Tape.head() keeps the lens step",
        f"Tape('1w').head(2).step {probe.head(2).step}")
    chk(int(C.ERA_BOUNDARY_MS) == E.ERA_CUT_MS, "C.ERA_BOUNDARY_MS == E.ERA_CUT_MS",
        f"{C.ERA_BOUNDARY_MS}")
    fz = E.fees()
    tl = {s: C.toll_bps_for(s) for s in CLASSIC5 + UNSEEN12}
    badt = {s: v for s, v in tl.items()
            if v[0] != fz[s]["taker_round_trip_bps"] or "tierc10" in v[1]
            or not v[1].startswith(_TC11_FEE_REL)}
    chk(not badt, "C.toll_bps_for(s) == TC11 fee_schedule taker round trip, labelled TC11",
        f"{len(tl)} stems, {len(badt)} wrong" + (f" {badt}" if badt else "")
        + f" · e.g. {tl['BTCUSDT']}")
    rows = [r for r in E.tc10_bindings()
            if r["name"].split(".")[0] in ("tierc10_census", "tierc10_stamps", "tierc10_null")]
    und = [r for r in rows if r["name"] not in NOT_REROOTED
           and r["name"].rsplit("[", 1)[0] not in NOT_REROOTED]
    chk(not und, "no undeclared TC10 binding in the census / stamps / null globals",
        f"{len(rows)} TC10 binding(s), {len(und)} undeclared"
        + (": " + "; ".join(f"{r['name']}={r['value']}" for r in und[:6]) if und else ""))
    chk(NL.SEED == SEED == C.SEED == ST.SEED, "seeds re-rooted (C / stamps / null)",
        f"C {C.SEED} · ST {ST.SEED} · NL {NL.SEED}")
    if bad:
        raise SystemExit("HALT: POST-SHIM [L-0.3, tierc11_nest] — " + " | ".join(bad))


_post_shim()


# ══════════════════════════════════════════ 5 · THE LOADER
_TAPES: dict = {}
_NO_MEMO = ("5m", "15m")                    # 740k / 250k bars: loaded on demand


def _check_1w(stem: str, tape) -> None:
    """The Stage-D-derived 1w file == D.derive_1w(D.derive_1d(native 4h)), both
    cut at the pin — one law [L1], two answers refused."""
    p = Path(E.D.kline_path(stem, "4h"))
    f4 = pd.read_parquet(p).sort_values("open_time", kind="mergesort")
    f4 = f4[f4["open_time"] + LENS_MS["4h"] <= PIN_MS].reset_index(drop=True)
    d1, _ = E.D.derive_1d(f4)
    w1, _ = E.D.derive_1w(d1)
    w1 = w1[w1["open_time"] + LENS_MS["1w"] <= PIN_MS].reset_index(drop=True)
    same = (len(w1) == tape.n and np.array_equal(w1["open_time"].to_numpy(np.int64), tape.t0)
            and all(np.array_equal(w1[k].to_numpy(float), a) for k, a in
                    (("open", tape.o), ("high", tape.h), ("low", tape.l), ("close", tape.c))))
    if not same:
        raise SystemExit(f"HALT: {stem} 1w: Stage D's derived file ({tape.n} weeks) != "
                         f"derive_1w(derive_1d(native 4h)) ({len(w1)} weeks) [L-R.1]")


def load11(stem: str, lens: str):
    """(stem, lens) -> C.Tape: closed bars <= the TC11 pin, FULL history, ATR =
    engine.indicators.atr(h, l, c, 14) on the WHOLE tape (C.load_tape through the
    extended dicts).  HALTS IF the lens is not one of the seven, the tape's pin is
    not TC11's, a bar closes after the pin, or a derived lens disagrees with its
    derivation law."""
    if lens not in LENSES11:
        raise SystemExit(f"HALT: load11: lens {lens!r} is not one of {list(LENSES11)}")
    key = (stem, lens)
    if key in _TAPES:
        return _TAPES[key]
    tape = C.load_tape(stem, lens)
    if int(tape.meta["as_of_close_ms"]) != PIN_MS:
        raise SystemExit(f"HALT: load11({stem}, {lens}): as_of {tape.meta['as_of_close_ms']} "
                         f"is not the TC11 pin {PIN_MS}")
    if tape.step != LENS_MS[lens] or int(tape.t0[-1]) + tape.step > PIN_MS:
        raise SystemExit(f"HALT: load11({stem}, {lens}): step {tape.step} / last close "
                         f"{int(tape.t0[-1]) + tape.step} vs pin {PIN_MS}")
    if not np.array_equal(tape.atr, IND.atr(tape.h, tape.l, tape.c, RC.ATR_LEN)):
        raise SystemExit(f"HALT: load11({stem}, {lens}): the ATR is not engine.indicators.atr "
                         f"on the whole tape")
    if lens == "1w":
        _check_1w(stem, tape)
    if lens not in _NO_MEMO:
        _TAPES[key] = tape
    return tape


def era_cut11(tape) -> int:
    """C.era_cut, VERIFIED to cut by bar CLOSE <= 1719791999000 [L-1.3]: every
    bar before the cut closes at or before the instant and none after it does."""
    t = int(C.era_cut(tape))
    close = tape.t0 + LENS_MS[tape.lens]
    ok = (t == int((close <= E.ERA_CUT_MS).sum())
          and (t == 0 or int(close[t - 1]) <= E.ERA_CUT_MS)
          and (t == tape.n or int(close[t]) > E.ERA_CUT_MS))
    if not ok:
        raise SystemExit(f"HALT: C.era_cut({tape.sym} {tape.lens}) = {t} does not cut by "
                         f"bar CLOSE <= {E.ERA_CUT_MS}")
    return t


# ══════════════════════════════════════════ 6 · THE SCALE PICKS [L-R.2] — FILED ONCE
PICKS_PATH = OUT / "SCALE_PICKS.json"
PICKS_MD = OUT / "SCALE_PICKS.md"
GRID_NAME = "SCALE_GRID"
GRID_PATH = OUT / f"{GRID_NAME}.parquet"
GRID_KEY = ["asset", "lens", "window", "scale_mult"]
PICK_CELLS = (tuple((s, l) for s in CLASSIC5 for l in LENSES11)
              + tuple((s, l) for s in UNSEEN12 for l in ("1h", "4h", "1d")))
STABILITY_LENSES = ("1h", "4h", "12h")      # [L-R.2] printed per CLASSIC5 asset
WINDOWS = ("tuning", "whole", "first_half")
IN_SAMPLE_TEXT = {
    "tuning": "IN-SAMPLE for tuning · OUT-OF-SAMPLE for holdout",
    "first_half": "IN-SAMPLE for the first half of tuning · OUT-OF-SAMPLE after it",
    "whole": "IN-SAMPLE for tuning AND holdout (fit on the whole tape)",
}
PICK_LAW = ("L-R.2: pick of record = C.calibrate(tape.head(C.era_cut(tape))) — the 11-cell "
            "grid 1.5..4.0, the density nearest 0.75 confirmed ranges / 100 bars, ties toward "
            "3.0 then lower — on the TUNING era (bar CLOSE <= 2024-06-30T23:59:59Z); where the "
            "tuning era holds fewer than 400 bars of the lens the pick falls back to the WHOLE "
            "tape and is labelled IN-SAMPLE everywhere. calibrate()'s hard-coded "
            "calibrated_in_sample=True is overwritten with the true flag. The whole-tape pick, "
            "the first-half-of-tuning pick (stability) and the frozen 3.0 ride beside. The "
            "picks are PINS: every reader takes them from this file and never re-fits.")


def _grid_rows(g: pd.DataFrame, window: str, tape, pick: float, of_record: bool) -> pd.DataFrame:
    g = g.copy()
    g["window"] = window
    g["window_bars"] = int(tape.n)
    g["window_first_open_ms"] = int(tape.t0[0])
    g["window_last_close_ms"] = int(tape.t0[-1]) + LENS_MS[tape.lens]
    g["pick_of_window"] = float(pick)
    g["calibrated_in_sample"] = IN_SAMPLE_TEXT[window]          # the TRUE flag
    g["in_sample_tuning"] = True
    g["in_sample_holdout"] = window == "whole"
    g["is_window_of_record"] = bool(of_record)
    return g


def calibrate_cell(stem: str, lens: str) -> dict:
    """ONE (asset, lens) cell: the whole-tape grid always; the tuning grid and the
    first-half-of-tuning grid when the tuning head holds >= 400 bars.  Returns
    {'cell': the SCALE_PICKS row, 'grid': the grid rows, 'secs': wall}."""
    t_start = time.perf_counter()
    tape = load11(stem, lens)
    t_cut = era_cut11(tape)
    whole_pick, g_whole = C.calibrate(tape)
    fallback = t_cut < TUNE_MIN_BARS
    grids = []
    if fallback:
        tun_pick = half_pick = None
        half = None
        pick, window = float(whole_pick), "whole-tape (fallback)"
        grids.append(_grid_rows(g_whole, "whole", tape, whole_pick, True))
        label = (f"IN-SAMPLE (fallback: the tuning era holds {t_cut} < {TUNE_MIN_BARS} bars "
                 f"of this lens; fit on the whole tape)")
        dens = float(g_whole.loc[g_whole["chosen"], "density_per_100"].iloc[0])
        edge = bool(g_whole["pick_at_grid_edge"].iloc[0])
        brk = bool(g_whole["target_bracketed"].iloc[0])
    else:
        head = tape.head(t_cut)
        tun_pick, g_t = C.calibrate(head)
        half = t_cut // 2
        half_pick, g_h = C.calibrate(tape.head(half))
        pick, window = float(tun_pick), "tuning"
        grids += [_grid_rows(g_t, "tuning", head, tun_pick, True),
                  _grid_rows(g_whole, "whole", tape, whole_pick, False),
                  _grid_rows(g_h, "first_half", tape.head(half), half_pick, False)]
        label = "OUT-OF-SAMPLE for holdout (tuning-era pick; IN-SAMPLE for tuning)"
        dens = float(g_t.loc[g_t["chosen"], "density_per_100"].iloc[0])
        edge = bool(g_t["pick_at_grid_edge"].iloc[0])
        brk = bool(g_t["target_bracketed"].iloc[0])
    grid = C.canon(pd.concat(grids, ignore_index=True), GRID_KEY)
    cell = {
        "asset": stem, "lens": lens, "n_bars": int(tape.n),
        "first_bar_open": C.iso(int(tape.t0[0])),
        "last_bar_close": C.iso(int(tape.t0[-1]) + LENS_MS[lens]),
        "tuning_bars": int(t_cut),
        "tuning_last_close": (C.iso(int(tape.t0[t_cut - 1]) + LENS_MS[lens]) if t_cut else None),
        "pick_of_record": pick, "pick_window": window, "label": label,
        "in_sample_tuning": True, "in_sample_holdout": bool(fallback),
        "tuning_pick": None if tun_pick is None else float(tun_pick),
        "whole_tape_pick": float(whole_pick),
        "first_half_bars": None if half is None else int(half),
        "first_half_pick": None if half_pick is None else float(half_pick),
        "stable_first_half_vs_tuning": (None if half_pick is None
                                        else bool(float(half_pick) == float(tun_pick))),
        "frozen_scale": float(C.FROZEN_SCALE),
        "density_at_pick_per_100": round(dens, 8),
        "pick_at_grid_edge": edge, "target_bracketed": brk,
        "grid_content_sha256": C.content_sha(grid),
    }
    return {"cell": cell, "grid": grid, "source": cell_source(stem, lens, tape),
            "secs": time.perf_counter() - t_start}


# ── THE PROVENANCE SIDECAR [L-R.2; verifier finding 11] ─────────────────────
# SCALE_PICKS.json is write-once and carries no input shas; the sidecar names,
# per pick cell, the snapshot file the tape was read from and its sha256 (the
# loader's own tape.meta), plus the file a derived lens is HALT-checked against.
# It annotates the exact bytes of SCALE_PICKS.json.  F-CAL re-verifies every sha
# against STAGE_D_MANIFEST and the snapshot; F-DET rebuilds it byte for byte.
SOURCES_NAME = "SCALE_PICKS_SOURCES.json"
SOURCES_PATH = OUT / SOURCES_NAME
SOURCES_LAW = ("provenance of SCALE_PICKS.json (write-once, so the input shas ride in this "
               "sidecar): per pick cell, the snapshot file C.load_tape read and its sha256 "
               "(tape.meta.source_sha256), and the file a derived lens is HALT-checked "
               "against (1d: Stage D's 1d file; 1w: the native 4h file it is re-derived "
               "from). The picks reproduce from exactly these bytes (F-CAL, F-DET).")


def cell_source(stem: str, lens: str, tape=None) -> dict:
    tape = load11(stem, lens) if tape is None else tape
    m = tape.meta
    chk = {}
    if lens == "1d":
        chk[f"klines/{stem}_1d.parquet"] = sha_file(Path(C.cache_dir()) / "klines" /
                                                    f"{stem}_1d.parquet")
    if lens == "1w":
        chk[f"klines/{stem}_4h.parquet"] = sha_file(Path(E.D.kline_path(stem, "4h")))
    return {"asset": stem, "lens": lens, "n_bars": int(tape.n),
            "source_file": str(m["source_file"]), "source_sha256": str(m["source_sha256"]),
            "checked_against": chk}


def sources_record(rows: list[dict], picks_bytes: bytes) -> dict:
    return {"tier": "TIER-C11", "stage": "TC11-R", "reading": "L-R.2", "law": SOURCES_LAW,
            "annotates": PICKS_PATH.name,
            "annotates_sha256": hashlib.sha256(picks_bytes).hexdigest(),
            "as_of_close_ms": PIN_MS, "substrate": E.SNAPSHOT.name, "n_cells": len(rows),
            "cells": rows}


def _pool_cell(args):                        # a fork-pool worker (module level)
    return calibrate_cell(*args)


def compute_picks(cells=PICK_CELLS, procs: int = 1) -> dict:
    """Every cell, in PICK_CELLS order.  procs > 1 forks worker processes (the
    fork start method: a spawned child would re-import this module under a name
    the range door refuses).  -> {'cells', 'grid', 'sources', 'secs'}."""
    if procs > 1:
        import multiprocessing as mp
        with mp.get_context("fork").Pool(procs) as pool:
            res = pool.map(_pool_cell, list(cells), chunksize=1)
    else:
        res = [calibrate_cell(s, l) for s, l in cells]
    secs = {(r["cell"]["asset"], r["cell"]["lens"]): r["secs"] for r in res}
    grid = C.canon(pd.concat([r["grid"] for r in res], ignore_index=True), GRID_KEY)
    return {"cells": [r["cell"] for r in res], "grid": grid,
            "sources": [r["source"] for r in res], "secs": secs}


def picks_record(cells: list[dict], grid: pd.DataFrame) -> dict:
    stab = [f"{c['asset']} {c['lens']}: first half {c['first_half_pick']} vs tuning "
            f"{c['tuning_pick']}" for c in cells
            if c["asset"] in CLASSIC5 and c["lens"] in STABILITY_LENSES
            and c["stable_first_half_vs_tuning"] is False]
    return {
        "tier": "TIER-C11", "stage": "TC11-R", "reading": "L-R.2", "law": PICK_LAW,
        "contract_sha256": "bb38e016a8f3e55ca3bcc09fec53ba6b8dc40accb60d054f8163d033a898f835",
        "as_of_last_closed_4h": PIN_ISO, "as_of_close_ms": PIN_MS,
        "substrate": E.SNAPSHOT.name, "seed": SEED,
        "era_cut_ms": E.ERA_CUT_MS, "era_cut_iso": E.ERA_CUT_ISO, "era_law": "bar CLOSE",
        "tune_min_bars": TUNE_MIN_BARS, "scale_grid": [float(s) for s in C.SCALE_GRID],
        "density_target_per_100": float(C.DENSITY_TARGET_PER_100),
        "tie_break": "nearest density; then toward 3.0; then the lower SCALE",
        "frozen_scale": float(C.FROZEN_SCALE),
        "pins_of_record": {k: v for k, v in live_pins()},
        "pins_key_order": [k for k, _ in live_pins()],
        "port_sha256": PORT_SHA, "engine_sha256": ENGINE_SHA,
        "retest_pins": {k: C.RETEST_PINS[k] for k in RETEST_OF_RECORD},
        "grid_file": f"{GRID_NAME}.parquet", "grid_key": GRID_KEY,
        "grid_rows": int(len(grid)), "grid_content_sha256": C.content_sha(grid),
        "n_cells": len(cells),
        "fallback_cells": [f"{c['asset']} {c['lens']}" for c in cells
                           if c["pick_window"] != "tuning"],
        "stability_changes_classic5_1h_4h_12h": stab,
        "cells": cells,
    }


def _picks_md(rec: dict, grid: pd.DataFrame) -> str:
    L = [f"# TIER-C11 · TC11-R · SCALE PICKS (L-R.2) — filed once, the picks are pins", "",
         f"as_of_last_closed_4h: {rec['as_of_last_closed_4h']} · substrate {rec['substrate']} "
         f"· seed {rec['seed']}", "", rec["law"], "",
         f"era cut: bar CLOSE <= {rec['era_cut_iso']} ({rec['era_cut_ms']}); fallback below "
         f"{rec['tune_min_bars']} tuning bars; grid {rec['scale_grid']}; target "
         f"{rec['density_target_per_100']} / 100 bars; tie-break: {rec['tie_break']}.", "",
         "## The 12 pins, key order of record", ""]
    L += [f"- {k} = {v!r}" for k, v in rec["pins_of_record"].items()]
    L += ["", "## Picks per asset x lens", "",
          "| asset | lens | bars | tuning bars | PICK OF RECORD | window | tuning | whole tape | "
          "first half | stable | frozen | density@pick | edge | label |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for c in rec["cells"]:
        L.append(f"| {c['asset']} | {c['lens']} | {c['n_bars']} | {c['tuning_bars']} | "
                 f"**{c['pick_of_record']:g}** | {c['pick_window']} | "
                 f"{'—' if c['tuning_pick'] is None else format(c['tuning_pick'], 'g')} | "
                 f"{c['whole_tape_pick']:g} | "
                 f"{'—' if c['first_half_pick'] is None else format(c['first_half_pick'], 'g')} | "
                 f"{'—' if c['stable_first_half_vs_tuning'] is None else c['stable_first_half_vs_tuning']} | "
                 f"{c['frozen_scale']:g} | {c['density_at_pick_per_100']:.4f} | "
                 f"{c['pick_at_grid_edge']} | {c['label']} |")
    L += ["", "## Stability (CLASSIC5 x {1h, 4h, 12h}): first half of tuning vs the whole "
          "tuning era", ""]
    L += ([f"- CHANGED: {x}" for x in rec["stability_changes_classic5_1h_4h_12h"]]
          or ["- no change on any of the 15 cells"])
    L += ["", "## The whole density grid (confirmed ranges per 100 bars; * = the window's pick)",
          "", "| asset | lens | window | bars | " + " | ".join(f"{s:g}" for s in rec["scale_grid"])
          + " |", "|---|---|---|---|" + "---|" * len(rec["scale_grid"])]
    order = {s: i for i, s in enumerate(CLASSIC5 + UNSEEN12)}
    lo = {l: i for i, l in enumerate(LENSES11)}
    wo = {w: i for i, w in enumerate(WINDOWS)}
    for (a, l, w), g in sorted(grid.groupby(["asset", "lens", "window"]),
                               key=lambda x: (order[x[0][0]], lo[x[0][1]], wo[x[0][2]])):
        g = g.sort_values("scale_mult")
        cells = [f"{d:.4f}{'*' if ch else ''}" for d, ch in zip(g["density_per_100"], g["chosen"])]
        L.append(f"| {a} | {l} | {w} | {int(g['window_bars'].iloc[0])} | " + " | ".join(cells) + " |")
    L += ["", f"grid file: {rec['grid_file']} · {rec['grid_rows']} rows · content sha256 "
          f"{rec['grid_content_sha256']}"]
    return "\n".join(L) + "\n"


def _dump_json(obj, path: Path) -> bytes:
    b = (json.dumps(obj, indent=1, sort_keys=True, default=str) + "\n").encode("utf-8")
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_bytes(b)
    os.replace(tmp, path)
    return b


def _write_grid(grid: pd.DataFrame, out: Path | None = None) -> str:
    """C.canon -> an atomic parquet (pandas on a PATH STRING, a Python-level open the
    audit hook sees) -> the content sha."""
    out = OUT if out is None else Path(out)
    out.mkdir(parents=True, exist_ok=True)
    d = C.canon(grid, GRID_KEY)
    p = out / f"{GRID_NAME}.parquet"
    tmp = p.with_name(p.name + ".tmp")
    d.to_parquet(str(tmp), index=False)
    os.replace(tmp, p)
    return C.content_sha(d)


PICK_FILES = ("SCALE_PICKS.json", "SCALE_PICKS.md", f"{GRID_NAME}.parquet", SOURCES_NAME)


def build_picks(procs: int = 1, out: Path | None = None) -> dict:
    """FILE ONCE into `out` (default research_outputs/tierc11/ranges; F-DET builds
    into its own _det_ roots).  HALTS IF out/SCALE_PICKS.json already exists: the
    picks are pins, and a pin is never re-fitted.  Writes the four PICK_FILES."""
    out = OUT if out is None else Path(out)
    pj = out / "SCALE_PICKS.json"
    if pj.exists():
        raise SystemExit(f"HALT: {E.rel_of(E._real(pj))} is FILED (write-once) — the "
                         f"picks are pins; a re-fit is refused [L-R.2]")
    t0 = time.perf_counter()
    got = compute_picks(PICK_CELLS, procs=procs)
    cells, grid, secs = got["cells"], got["grid"], got["secs"]
    rec = picks_record(cells, grid)
    sha = _write_grid(grid, out)
    if sha != rec["grid_content_sha256"]:
        raise SystemExit("HALT: the filed SCALE_GRID content sha moved on write")
    (out / "SCALE_PICKS.md").write_text(_picks_md(rec, grid), encoding="utf-8")
    b = _dump_json(rec, pj)                     # the json is the seal ...
    _dump_json(sources_record(got["sources"], b), out / SOURCES_NAME)   # ... its sidecar
    C.clock(f"build_picks: {len(cells)} cells, procs {procs}, wall "
            f"{time.perf_counter() - t0:.1f}s; slowest "
            + ", ".join(f"{a} {l} {s:.1f}s" for (a, l), s in
                        sorted(secs.items(), key=lambda x: -x[1])[:5]))
    return rec


def file_sources() -> dict:
    """FILE ONCE the provenance sidecar of the ALREADY-FILED SCALE_PICKS.json
    (filed before the sidecar existed): the same rows build_picks writes, from
    the same loader.  HALTS IF the sidecar exists, the record is absent, or a
    filed cell's bar count is not the tape's (the record was fit on other bytes)."""
    if SOURCES_PATH.exists():
        raise SystemExit(f"HALT: {E.rel_of(E._real(SOURCES_PATH))} is FILED (write-once)")
    if not PICKS_PATH.exists():
        raise SystemExit(f"HALT: {E.rel_of(E._real(PICKS_PATH))} is not filed")
    pb = PICKS_PATH.read_bytes()
    by = {(c["asset"], c["lens"]): c for c in json.loads(pb)["cells"]}
    rows = []
    for s, l in PICK_CELLS:
        r = cell_source(s, l)
        if by[(s, l)]["n_bars"] != r["n_bars"]:
            raise SystemExit(f"HALT: {s} {l}: filed n_bars {by[(s, l)]['n_bars']} != the "
                             f"tape's {r['n_bars']} — the record was not fit on these bytes")
        rows.append(r)
    rec = sources_record(rows, pb)
    _dump_json(rec, SOURCES_PATH)
    return rec


_PICKS: dict = {}


def picks() -> dict:
    """The FILED record (read once per process).  HALTS IF it is absent."""
    if not _PICKS:
        if not PICKS_PATH.exists():
            raise SystemExit(f"HALT: {E.rel_of(E._real(PICKS_PATH))} is not filed — run "
                             f"`tierc11_nest.py --build-picks` once [L-R.2]")
        rec = json.loads(PICKS_PATH.read_text(encoding="utf-8"))
        _PICKS.update(rec)
        _PICKS["_by_cell"] = {(c["asset"], c["lens"]): c for c in rec["cells"]}
    return _PICKS


def scale_of(stem: str, lens: str, scale_kind: str) -> float:
    """THE scale a reader uses: the FILED pick of record ('calibrated') or the
    frozen 3.0 — never a re-fit."""
    if scale_kind == "frozen3.0":
        return float(C.FROZEN_SCALE)
    if scale_kind != "calibrated":
        raise SystemExit(f"HALT: scale_kind {scale_kind!r} is not one of {list(SCALE_KINDS)}")
    c = picks()["_by_cell"].get((stem, lens))
    if c is None:
        raise SystemExit(f"HALT: no filed pick for {stem} {lens} — the commission is CLASSIC5 x "
                         f"{list(LENSES11)} and UNSEEN12 x [1h, 4h, 1d] [L-R.1]")
    return float(c["pick_of_record"])


LABEL_FIELDS = ("pick_window", "scale_in_sample", "stability_changed")


def scale_label(stem: str, lens: str, scale_kind: str) -> dict:
    """THE HONESTY LABELS of one (stem, lens, scale_kind) [L-R.2], carried on every
    row that consumes the lens [verifier finding 5]:
      pick_window        'tuning' · 'whole-tape (fallback)' · 'frozen3.0'
      fallback           the pick was fit on the WHOLE tape (IN-SAMPLE everywhere)
      in_sample_holdout  True for a fallback; False for a tuning pick and frozen 3.0
      stability_changed  the first-half-of-tuning pick != the tuning pick (True /
                         False); None where there is no tuning pick (a fallback,
                         frozen 3.0)."""
    if scale_kind == "frozen3.0":
        return {"pick_window": "frozen3.0", "fallback": False, "in_sample_holdout": False,
                "stability_changed": None}
    scale_of(stem, lens, scale_kind)            # HALTS on an unknown kind / cell
    c = picks()["_by_cell"][(stem, lens)]
    st = c["stable_first_half_vs_tuning"]
    return {"pick_window": str(c["pick_window"]), "fallback": c["pick_window"] != "tuning",
            "in_sample_holdout": bool(c["in_sample_holdout"]),
            "stability_changed": None if st is None else (not bool(st))}


def scale_in_sample(lab: dict, instants_ms) -> np.ndarray:
    """[L-R.2 SCALE-IN-SAMPLE] a calibrated-scale range read at an instant <= the
    era cut is structurally in-sample (the pick saw bars after it); a whole-tape
    fallback is in-sample at EVERY instant; frozen 3.0 never is."""
    t = np.asarray(instants_ms, dtype=np.int64)
    if lab["pick_window"] == "frozen3.0":
        return np.zeros(t.shape, dtype=bool)
    if lab["fallback"]:
        return np.ones(t.shape, dtype=bool)
    return t <= E.ERA_CUT_MS


def _label_frame(f: pd.DataFrame, lab: dict, instants_ms) -> pd.DataFrame:
    f = f.copy()
    f["pick_window"] = lab["pick_window"]
    f["scale_in_sample"] = scale_in_sample(lab, instants_ms)
    f["stability_changed"] = pd.array([lab["stability_changed"]] * len(f), dtype="boolean")
    return f


def pick_findings(rec: dict, recomputed: dict, commission=None) -> list[str]:
    """F-CAL's guard: a FILED record vs cells recomputed from the TUNING HEAD
    ALONE.  recomputed[(asset, lens)] = {'tuning_bars', 'tuning_pick' (None when
    < 400), 'whole_tape_pick', 'first_half_pick', 'grid_sha'}.  Detectors:
    TUNING-HEAD · IN-SAMPLE-LABEL · WHOLE-TAPE · FIRST-HALF · GRID · COVERAGE."""
    bad = []
    want = set(PICK_CELLS if commission is None else commission)
    by = {(c["asset"], c["lens"]): c for c in rec.get("cells", [])}
    if set(by) != want or len(rec.get("cells", [])) != len(want):
        bad.append(f"COVERAGE: {len(by)} filed cells vs the commission's {len(want)}")
    for key, r in recomputed.items():
        c = by.get(key)
        if c is None:
            continue
        tag = f"{key[0]} {key[1]}"
        if c["tuning_bars"] != r["tuning_bars"]:
            bad.append(f"TUNING-HEAD: {tag} filed tuning_bars {c['tuning_bars']} != "
                       f"{r['tuning_bars']} recomputed by bar close")
        if r["tuning_pick"] is not None:
            if not (c["pick_of_record"] == c["tuning_pick"] == r["tuning_pick"]):
                bad.append(f"TUNING-HEAD: {tag} pick of record {c['pick_of_record']} / filed "
                           f"tuning {c['tuning_pick']} != the pick fit on the tuning head alone "
                           f"{r['tuning_pick']}")
            if c["pick_window"] != "tuning" or c["in_sample_holdout"] is not False:
                bad.append(f"IN-SAMPLE-LABEL: {tag} window {c['pick_window']!r} / "
                           f"in_sample_holdout {c['in_sample_holdout']} on a tuning pick")
        else:
            if c["pick_window"] == "tuning" or c["in_sample_holdout"] is not True \
                    or not c["label"].startswith("IN-SAMPLE"):
                bad.append(f"IN-SAMPLE-LABEL: {tag} has {r['tuning_bars']} < {TUNE_MIN_BARS} "
                           f"tuning bars but is labelled {c['pick_window']!r} / "
                           f"in_sample_holdout {c['in_sample_holdout']} / {c['label'][:40]!r}")
            if c["pick_of_record"] != r["whole_tape_pick"]:
                bad.append(f"WHOLE-TAPE: {tag} fallback pick {c['pick_of_record']} != the "
                           f"whole-tape pick {r['whole_tape_pick']}")
        if c["whole_tape_pick"] != r["whole_tape_pick"]:
            bad.append(f"WHOLE-TAPE: {tag} filed {c['whole_tape_pick']} != {r['whole_tape_pick']}")
        if c["first_half_pick"] != r["first_half_pick"]:
            bad.append(f"FIRST-HALF: {tag} filed {c['first_half_pick']} != {r['first_half_pick']}")
        if c["grid_content_sha256"] != r["grid_sha"]:
            bad.append(f"GRID: {tag} filed grid sha {c['grid_content_sha256'][:12]}… != "
                       f"recomputed {r['grid_sha'][:12]}…")
    return bad


# ══════════════════════════════════════════ 7 · VIEWS AND LENS BUNDLES
_VIEWS: dict = {}
_BUNDLES: dict = {}


def view11(stem: str, lens: str, scale_kind: str = "calibrated"):
    """(tape, run_scale output, asof_view) at the FILED scale — memoised in-process
    (5m / 15m are recomputed on demand, never held)."""
    key = (stem, lens, scale_kind)
    if key in _VIEWS:
        return _VIEWS[key]
    tape = load11(stem, lens)
    v2 = C.run_scale(tape, scale_of(stem, lens, scale_kind))
    view = C.asof_view(tape, v2["macro"], v2["leash"])
    out = (tape, v2, view)
    if lens not in _NO_MEMO:
        _VIEWS[key] = out
    return out


def drop_memo() -> None:
    _TAPES.clear()
    _VIEWS.clear()
    _BUNDLES.clear()


STATE4 = {"NONE": 0, "BULL_EXP": 1, "BEAR_EXP": -1, "IN_RANGE": 2}
STATE4_NAMES = np.array(["BEAR_EXP", "NONE", "BULL_EXP", "IN_RANGE"])   # index = code + 1
VERDICT = {"hold": 1, "failed": 0, "truncated": -1}
UP = {"top": 1, "bottom": -1}


def _dies(macro: dict) -> list[tuple[int, int, str]]:
    d = [(int(e["i"]), int(e["rid"]), str(e["side"])) for e in macro["events"]
         if e["event"] == "breakout-die"]
    d.sort(key=lambda x: x[0])
    return d


def _hardens(macro: dict) -> list[tuple[int, int, str]]:
    return [(int(e["i"]), int(e["rid"]), str(e["side"])) for e in macro["events"]
            if e["event"] == "harden"]


def _mem_lines(tape, v2: dict, view: dict) -> pd.DataFrame:
    """The dead macro ranges' memory lines, AS-OF.  px = the boundary as-of bar
    die_i - 1 (the view, full precision — never Range.top/.bottom; equal to the
    leash's own line because no harden of the range falls at or after die_i,
    asserted).  LIVE = the engine's LIVE (unfrozen, unexpired): from die_i until
    the line's FIRST leash event (the first two-sided touch freezes it; a cap or
    ttl expiry ends it) — each known at its own bar.  INF = no such event on
    this tape."""
    macro, leash = v2["macro"], v2["leash"]
    first: dict = {}
    for e in leash:
        k = (int(e["rid"]), str(e["side"]))
        if k not in first:
            first[k] = (int(e["i"]), e["event"], e.get("reason") or e.get("verdict", ""))
    hard_after: dict = {}
    for i, rid, _ in _hardens(macro):
        hard_after.setdefault(rid, []).append(i)
    dead = {r.rid for r in macro["ranges"] if r.state == "DEAD" and r.confirm_i >= 0
            and r.die_i >= 0}
    dies = _dies(macro)
    if dead != {rid for _, rid, _ in dies}:
        raise SystemExit(f"HALT: {tape.sym} {tape.lens}: the DEAD confirmed ranges "
                         f"{len(dead)} != the breakout-die events {len(dies)}")
    rows = []
    for d_i, rid, dside in dies:
        if any(i >= d_i for i in hard_after.get(rid, ())):
            raise SystemExit(f"HALT: {tape.sym} {tape.lens}: rid {rid} hardens at/after its "
                             f"death bar {d_i} — the as-of line would not be the machine's")
        k = d_i - 1
        ok = k >= 0 and bool(view["in_range"][k]) and int(view["rid"][k]) == rid
        for side in ("top", "bottom"):
            px = float(view["top" if side == "top" else "bot"][k]) if ok else float("nan")
            fe = first.get((rid, side))
            if fe is None:
                end, why = INF, "open"
            elif fe[1] == "line-expired":
                end, why = fe[0], f"expired-{fe[2]}"
            else:
                end, why = fe[0], "touched (frozen)"
            rows.append({"rid": rid, "side": side, "dir": UP[side], "die_side": dside,
                         "px": px, "born": d_i, "end_live": end, "end_reason": why})
    cols = ["rid", "side", "dir", "die_side", "px", "born", "end_live", "end_reason"]
    f = pd.DataFrame(rows, columns=cols)
    for k in ("rid", "dir", "born", "end_live"):
        f[k] = f[k].astype(np.int64)
    f["px"] = f["px"].astype(float)
    return f


def bundle_of(tape, v2: dict, view: dict) -> dict:
    """Everything the nest and the events read from ONE (lens, scale) run — a
    pure function of the run, so a PREFIX run gives the prefix bundle."""
    return {"tape": tape, "v2": v2, "view": view, "mem": _mem_lines(tape, v2, view),
            "dies": _dies(v2["macro"]), "hardens": _hardens(v2["macro"])}


def bundle11(stem: str, lens: str, scale_kind: str = "calibrated") -> dict:
    key = (stem, lens, scale_kind)
    if key in _BUNDLES:
        return _BUNDLES[key]
    b = bundle_of(*view11(stem, lens, scale_kind))
    if lens not in _NO_MEMO:
        _BUNDLES[key] = b
    return b


# ══════════════════════════════════════════ 8 · THE NEST VECTOR [L-R.5]
NEST_FIELDS = ("k", "bar_close_ms", "state", "in_range", "pct", "dist_signed_atr", "near_side",
               "bnd_age", "dev_top", "dev_bot", "flip_pol", "flip_age", "top", "bot", "atr_L",
               "coin_top", "coin_bot", "coin_top_mem", "coin_bot_mem")
_NEST_DTYPES = {"k": "Int64", "bar_close_ms": "Int64", "state": object, "in_range": "boolean",
                "pct": float, "dist_signed_atr": float, "near_side": "Int8", "bnd_age": "Int64",
                "dev_top": "Int64", "dev_bot": "Int64", "flip_pol": "Int8", "flip_age": "Int64",
                "top": float, "bot": float, "atr_L": float, "coin_top": "boolean",
                "coin_bot": "boolean", "coin_top_mem": "boolean", "coin_bot_mem": "boolean"}


def within(level, others: list, atr, frac: float | None = None) -> np.ndarray:
    """|level - other| <= frac x ATR_L for ANY of `others` (inclusive; NaN never
    coincides).  frac defaults to the module's COIN_FRAC, read at CALL time."""
    f = COIN_FRAC if frac is None else frac
    level = np.asarray(level, dtype=float)
    thr = f * np.asarray(atr, dtype=float)
    out = np.zeros(np.broadcast(level, thr).shape, dtype=bool)
    with np.errstate(invalid="ignore"):
        for o in others:
            out |= np.abs(level - np.asarray(o, dtype=float)) <= thr
    return out


def coin_flags(top_L, bot_L, atr_L, in_L, top_U, bot_U, in_U, mem_px=None, mem_live=None,
               frac: float | None = None) -> dict:
    """THE COINCIDENCE RULE [L-R.5], the one place it is written.  Per side of L:
    a LIVE boundary of L within frac x ATR_L of EITHER live boundary of L+1 (all
    four pairings, inclusive).  The twin (…_mem) also admits L+1's LIVE memory
    lines: mem_px (m,) with mem_live (n, m) booleans.  Arrays of length n."""
    in_L = np.asarray(in_L, dtype=bool)
    in_U = np.asarray(in_U, dtype=bool)
    both = in_L & in_U
    ct = both & within(top_L, [top_U, bot_U], atr_L, frac)
    cb = both & within(bot_L, [top_U, bot_U], atr_L, frac)
    ctm, cbm = ct.copy(), cb.copy()
    if mem_px is not None and len(mem_px):
        f = COIN_FRAC if frac is None else frac
        px = np.asarray(mem_px, dtype=float)[None, :]
        thr = (f * np.asarray(atr_L, dtype=float))[:, None]
        live = np.asarray(mem_live, dtype=bool)
        with np.errstate(invalid="ignore"):
            mt = (live & (np.abs(np.asarray(top_L, dtype=float)[:, None] - px) <= thr)).any(axis=1)
            mb = (live & (np.abs(np.asarray(bot_L, dtype=float)[:, None] - px) <= thr)).any(axis=1)
        ctm |= in_L & mt
        cbm |= in_L & mb
    return {"coin_top": ct, "coin_bot": cb, "coin_top_mem": ctm, "coin_bot_mem": cbm}


def mem_live_at(mem: pd.DataFrame, k: np.ndarray) -> np.ndarray:
    """(n, m): memory line j is LIVE at bar k[i] (born <= k < end_live; k < 0 = none)."""
    k = np.asarray(k, dtype=np.int64)[:, None]
    born = mem["born"].to_numpy(np.int64)[None, :]
    end = mem["end_live"].to_numpy(np.int64)[None, :]
    return (k >= 0) & (born <= k) & (k < end)


def _dev_carry(view: dict) -> tuple[np.ndarray, np.ndarray]:
    """[L-R.5] "out of range ... deviations CARRY": per bar, the deviation counts
    (hardens per side) of the live range, or — out of range — of the LAST live
    range as of its last in-range bar (die_i - 1: no harden falls at or after
    die_i, asserted in _mem_lines); 0 before the first range.  The as-of view
    resets dev_top / dev_bot to 0 at a death; this carries the dead range's
    final counts forward instead [verifier finding 4].  Causal: bar k reads bar
    j <= k only."""
    inr = np.asarray(view["in_range"], dtype=bool)
    idx = np.arange(len(inr), dtype=np.int64)
    last = np.maximum.accumulate(np.where(inr, idx, -1)) if len(inr) else idx
    safe = np.where(last >= 0, last, 0)
    dt = np.where(last >= 0, np.asarray(view["dev_top"])[safe], 0).astype(np.int64)
    db = np.where(last >= 0, np.asarray(view["dev_bot"])[safe], 0).astype(np.int64)
    return dt, db


def _lens_arrays(b: dict, inst: np.ndarray) -> dict:
    tape, view = b["tape"], b["view"]
    dev_t, dev_b = _dev_carry(view)            # read at CALL time (F-NEST-ASOF plants it)
    k = C.asof_index(tape, inst).astype(np.int64)
    ok = k >= 0
    ks = np.where(ok, k, 0)
    inr = ok & view["in_range"][ks]
    raw = np.where(ok, view["state"][ks].astype(np.int64), 0)
    code = np.where(inr, STATE4["IN_RANGE"], raw)             # latch 0, not in range: NONE
    nan = np.full(len(k), np.nan)
    top = np.where(inr, view["top"][ks], nan)
    bot = np.where(inr, view["bot"][ks], nan)
    c = tape.c[ks]
    with np.errstate(invalid="ignore"):
        inside = (bot <= c) & (c <= top)
    return {
        "k": k, "ok": ok, "ks": ks,
        "bar_close_ms": np.where(ok, tape.t0[ks] + tape.step, -1),
        "state_code": code, "in_range": inr,
        "pct": np.where(inr, view["pct"][ks], nan),
        "dist_signed_atr": np.where(inr, np.where(inside, 1.0, -1.0) * view["dist_atr"][ks], nan),
        "near_side": np.where(inr, view["near_side"][ks], 0).astype(np.int64),
        "bnd_age": np.where(inr, view["bnd_age"][ks], -1),
        "dev_top": np.where(ok, dev_t[ks], 0),
        "dev_bot": np.where(ok, dev_b[ks], 0),
        "flip_pol": np.where(ok, view["flip_pol"][ks], 0).astype(np.int64),
        "flip_age": np.where(ok, view["flip_age"][ks], -1),
        "top": top, "bot": bot, "atr_L": np.where(ok, tape.atr[ks], nan),
    }


def nest_from_bundles(bundles: dict, instants_ms) -> pd.DataFrame:
    """bundles = {lens: bundle or None (NA lens)} over NEST_LENSES.  One row per
    instant; per lens L the fields of NEST_FIELDS, prefixed 'L_'.  Pure: the same
    function reads a full run and a prefix run."""
    inst = np.asarray(instants_ms, dtype=np.int64)
    n = len(inst)
    A = {L: (_lens_arrays(bundles[L], inst) if bundles.get(L) is not None else None)
         for L in NEST_LENSES}
    cols: dict = {"instant_ms": inst}
    for L in NEST_LENSES:
        a, U = A[L], LADDER[L]
        if a is None:                           # NA lens: every field NA
            for fld in NEST_FIELDS:
                dt = _NEST_DTYPES[fld]
                cols[f"{L}_{fld}"] = (np.full(n, np.nan) if dt is float else
                                      np.array([None] * n, dtype=object) if dt is object else
                                      pd.array([pd.NA] * n, dtype=dt))
            continue
        cols[f"{L}_k"] = pd.array(a["k"], dtype="Int64")
        bc = pd.array(a["bar_close_ms"], dtype="Int64")
        bc[~a["ok"]] = pd.NA
        cols[f"{L}_bar_close_ms"] = bc
        cols[f"{L}_state"] = pd.Series(STATE4_NAMES[a["state_code"] + 1], dtype=object).values
        cols[f"{L}_in_range"] = pd.array(a["in_range"], dtype="boolean")
        for fld in ("pct", "dist_signed_atr", "top", "bot", "atr_L"):
            cols[f"{L}_{fld}"] = a[fld].astype(float)
        cols[f"{L}_near_side"] = pd.array(a["near_side"], dtype="Int8")
        ba = pd.array(a["bnd_age"], dtype="Int64")
        ba[~a["in_range"]] = pd.NA
        cols[f"{L}_bnd_age"] = ba
        for fld in ("dev_top", "dev_bot", "flip_age"):
            cols[f"{L}_{fld}"] = pd.array(a[fld], dtype="Int64")
        cols[f"{L}_flip_pol"] = pd.array(a["flip_pol"], dtype="Int8")
        u = A.get(U) if U is not None else None
        if u is None:
            for fld in ("coin_top", "coin_bot", "coin_top_mem", "coin_bot_mem"):
                cols[f"{L}_{fld}"] = pd.array([pd.NA] * n, dtype="boolean")
            continue
        mem = bundles[U]["mem"]
        live = mem_live_at(mem, u["k"])
        cf = coin_flags(a["top"], a["bot"], a["atr_L"], a["in_range"], u["top"], u["bot"],
                        u["in_range"], mem["px"].to_numpy(float), live)
        for fld, v in cf.items():
            cols[f"{L}_{fld}"] = pd.array(v, dtype="boolean")
    order = ["instant_ms"] + [f"{L}_{fld}" for L in NEST_LENSES for fld in NEST_FIELDS]
    return pd.DataFrame({k: cols[k] for k in order})


def nest_at(stem: str, instants_ms, scale_kind: str = "calibrated") -> pd.DataFrame:
    """THE NEST VECTOR [L-R.5]: one row per instant (ms), per L in {1h, 4h, 12h,
    1d, 1w} read at the last CLOSED bar of L with close <= the instant.  For the
    twelve, the 12h and 1w columns (and the 4h / 1d coincidence, whose L+1 is NA)
    are NA."""
    if stem not in LENSES_OF:
        raise SystemExit(f"HALT: nest_at: {stem} is not in CLASSIC5 or UNSEEN12 [L-R.1]")
    bundles = {L: (bundle11(stem, L, scale_kind) if L in LENSES_OF[stem] else None)
               for L in NEST_LENSES}
    nv = nest_from_bundles(bundles, instants_ms)
    # the honesty labels, per lens, on every row [L-R.2; verifier finding 5]
    inst = nv["instant_ms"].to_numpy(np.int64)
    n = len(nv)
    for L in NEST_LENSES:
        if bundles[L] is None:
            nv[f"{L}_pick_window"] = np.array([None] * n, dtype=object)
            nv[f"{L}_scale_in_sample"] = pd.array([pd.NA] * n, dtype="boolean")
            nv[f"{L}_stability_changed"] = pd.array([pd.NA] * n, dtype="boolean")
            continue
        lab = scale_label(stem, L, scale_kind)
        nv[f"{L}_pick_window"] = np.array([lab["pick_window"]] * n, dtype=object)
        nv[f"{L}_scale_in_sample"] = pd.array(scale_in_sample(lab, inst), dtype="boolean")
        nv[f"{L}_stability_changed"] = pd.array([lab["stability_changed"]] * n, dtype="boolean")
    order = ["instant_ms"] + [f"{L}_{fld}" for L in NEST_LENSES
                              for fld in NEST_FIELDS + LABEL_FIELDS]
    return nv[order]


# ══════════════════════════════════════════ 9 · EVENTS [L-R.6], ALL AS-OF
def _close_ms(tape, i: np.ndarray) -> np.ndarray:
    i = np.asarray(i, dtype=np.int64)
    inside = (i >= 0) & (i < tape.n)
    return np.where(inside, tape.t0[np.where(inside, i, 0)] + tape.step, -1)


def deaths_of(b: dict) -> pd.DataFrame:
    """Every macro death: die_i, rid, side, dir (+1 top / -1 bottom), known_at =
    die_i, the BROKEN side's as-of boundary at die_i - 1, ATR_L at known_at."""
    tape, view = b["tape"], b["view"]
    rows = []
    for d_i, rid, side in b["dies"]:
        k = d_i - 1
        ok = k >= 0 and bool(view["in_range"][k]) and int(view["rid"][k]) == rid
        bnd = float(view["top" if side == "top" else "bot"][k]) if ok else float("nan")
        rows.append({"die_i": d_i, "rid": rid, "side": side, "dir": UP[side], "known_at": d_i,
                     "boundary": bnd, "atr_known": float(tape.atr[d_i])})
    f = pd.DataFrame(rows, columns=["die_i", "rid", "side", "dir", "known_at", "boundary",
                                    "atr_known"])
    for k in ("die_i", "rid", "dir", "known_at"):
        f[k] = f[k].astype(np.int64)
    f["known_close_ms"] = _close_ms(tape, f["known_at"].to_numpy())
    return f


def hardens_of(b: dict) -> pd.DataFrame:
    """Every harden (swing failure): harden_i, rid, side, dir (a bottom harden is
    a spring +1, a top harden an upthrust -1), known_at = harden_i, the deviated
    side's as-of boundary at harden_i - 1 (PRE-redraw, of record) and at harden_i
    (POST-redraw, the Tier-E twin), ATR_L at known_at."""
    tape, view = b["tape"], b["view"]
    rows = []
    for i, rid, side in b["hardens"]:
        key = "top" if side == "top" else "bot"
        pre_ok = i - 1 >= 0 and bool(view["in_range"][i - 1]) and int(view["rid"][i - 1]) == rid
        post_ok = bool(view["in_range"][i]) and int(view["rid"][i]) == rid
        rows.append({"harden_i": i, "rid": rid, "side": side, "dir": -UP[side], "known_at": i,
                     "boundary_pre": float(view[key][i - 1]) if pre_ok else float("nan"),
                     "boundary_post": float(view[key][i]) if post_ok else float("nan"),
                     "atr_known": float(tape.atr[i])})
    f = pd.DataFrame(rows, columns=["harden_i", "rid", "side", "dir", "known_at",
                                    "boundary_pre", "boundary_post", "atr_known"])
    for k in ("harden_i", "rid", "dir", "known_at"):
        f[k] = f[k].astype(np.int64)
    f["known_close_ms"] = _close_ms(tape, f["known_at"].to_numpy())
    return f


def _qualifying_touches(h, l, c, lo, hi, d_i: int, end: int, side: str) -> np.ndarray:
    """C.retest_holds' touch law: bars j in (d_i, end] whose [low, high] MEETS the
    band AND whose PRIOR close sat beyond the band on the die side — in bar order."""
    w = np.arange(d_i + 1, end + 1)
    with np.errstate(invalid="ignore"):
        touch = (l[w] <= hi[w]) & (h[w] >= lo[w])
        opp = (c[w - 1] > hi[w - 1]) if side == "top" else (c[w - 1] < lo[w - 1])
    return w[np.nonzero(touch & opp)[0]]


def _hold_verdict(c, atr, lo, hi, j: int, H: int, margin: float, side: str, n: int) -> str:
    """C.retest_holds' test of ONE touch: truncated when j + H >= n; failed when any
    close in j..j+H goes through the band's far edge by margin x ATR[k] (or the
    band is unreadable); else hold."""
    if j + H >= n:
        return "truncated"
    k = np.arange(j, j + H + 1)
    with np.errstate(invalid="ignore"):
        through = ((c[k] < lo[k] - margin * atr[k]) if side == "top"
                   else (c[k] > hi[k] + margin * atr[k]))
        unread = ~np.isfinite(lo[k]) | ~np.isfinite(hi[k])
    return "failed" if (through | unread).any() else "hold"


# (no window-end column: the candidacy window's end — the next death, the ttl —
# is not a fact at a row's known_at, and every column here is)
SCAN_COLS = ["band", "die_i", "rid", "side", "dir", "seq", "touch_i", "known_at", "verdict",
             "is_first_hold"]


def _scan_frame(rows: list[dict], tape, with_px: bool = False) -> pd.DataFrame:
    f = pd.DataFrame(rows, columns=SCAN_COLS + (["px"] if with_px else []))
    if with_px:
        f["px"] = f["px"].astype(float)
    for k in ("die_i", "rid", "dir", "seq", "touch_i", "known_at"):
        f[k] = f[k].astype(np.int64)
    f["is_first_hold"] = f["is_first_hold"].astype(bool)
    f["known_close_ms"] = _close_ms(tape, f["known_at"].to_numpy())
    return f


def scan_band(tape, dies: list, band: str, lo: np.ndarray, hi: np.ndarray,
              margin: float, hold: int, ttl: int) -> list[dict]:
    """THE FIRST RETEST THAT HOLDS [L-R.6(a)] on one band.  Per DIE: the candidacy
    window (die_i, min(die_i + ttl, next_die - 1, n - 1)]; every qualifying touch
    in bar order gets retest_holds' own test — a touch inside another touch's
    pending hold window included; the first 'hold' is the event (known at touch +
    hold) and ends the scan; a 'truncated' verdict ends it; every evaluated touch
    is a row."""
    h, l, c, atr, n, H = tape.h, tape.l, tape.c, tape.atr, tape.n, int(hold)
    rows = []
    for q, (d_i, rid, side) in enumerate(dies):
        nxt = dies[q + 1][0] if q + 1 < len(dies) else n
        end = min(d_i + int(ttl), nxt - 1, n - 1)
        if end <= d_i:
            continue
        for seq, j in enumerate(_qualifying_touches(h, l, c, lo, hi, d_i, end, side)):
            j = int(j)
            v = _hold_verdict(c, atr, lo, hi, j, H, float(margin), side, n)
            rows.append({"band": band, "die_i": d_i, "rid": rid, "side": side, "dir": UP[side],
                         "seq": seq, "touch_i": j, "known_at": j + H,
                         "verdict": v, "is_first_hold": v == "hold"})
            if v != "failed":
                break
    return rows


def scan_bands_of(b: dict, bands=SCAN_BANDS, retest: dict | None = None) -> pd.DataFrame:
    rp = dict(C.RETEST_PINS if retest is None else retest)
    tape = b["tape"]
    rows = []
    for name in bands:
        lo, hi = C.band_of(name)(tape.c)
        rows += scan_band(tape, b["dies"], name, lo, hi, float(rp["margin_atr"]),
                          int(rp["hold_bars"]), int(rp["ttl_bars"]))
    return _scan_frame(rows, tape)


def oneshot_bands_of(b: dict, bands=SCAN_BANDS, retest: dict | None = None) -> pd.DataFrame:
    """THE ONE-SHOT TWIN: C.retest_holds itself (TC10's law — the first touch gets
    the only evaluation), one row per retested DIE per band."""
    rp = dict(C.RETEST_PINS if retest is None else retest)
    tape = b["tape"]
    rows = []
    for name in bands:
        lo, hi = C.band_of(name)(tape.c)
        for g in C.retest_holds(tape, b["dies"], lo, hi, float(rp["margin_atr"]),
                                int(rp["hold_bars"]), int(rp["ttl_bars"])):
            rows.append({"band": name, **g, "dir": UP[g["side"]]})
    f = pd.DataFrame(rows, columns=["band", "rid", "side", "die_i", "touch_i", "known_at",
                                    "verdict", "dir"])
    for k in ("rid", "die_i", "touch_i", "known_at", "dir"):
        f[k] = f[k].astype(np.int64)
    f["known_close_ms"] = _close_ms(tape, f["known_at"].to_numpy())
    return f


def _line_expiry(leash: list) -> dict:
    out: dict = {}
    for e in leash:
        if e["event"] == "line-expired":
            out.setdefault((int(e["rid"]), str(e["side"])), int(e["i"]))
    return out


def _mem_touches(h, l, c, px: float, d_i: int, end: int, side: str, e_i: int) -> np.ndarray:
    """The memory line's touch law [R-SCAN-2]: bars j in (d_i, end] whose [low,
    high] CONTAINS the line, whose PRIOR close sat strictly beyond it on the die
    side, and at which the line is unexpired (j < its expiry bar) — in bar order."""
    w = np.arange(d_i + 1, end + 1)
    opp = (c[w - 1] > px) if side == "top" else (c[w - 1] < px)
    return w[np.nonzero((l[w] <= px) & (px <= h[w]) & opp & (w < e_i))[0]]


def scan_memory_of(b: dict) -> pd.DataFrame:
    """THE MEMORY LINE, SAME LAW [L-R.6(a)]: per DIE, the dead range's memory line
    on the broken side (px = its as-of boundary at die_i - 1).  Qualifying touches
    in the candidacy window (die_i, min(die_i + MEM_TTL_BARS, next_die - 1, n - 1)]:
    the bar's [low, high] contains the line (two-sided), its PRIOR close sat beyond
    it on the die side (strictly), and the line is UNEXPIRED at the bar (no cap /
    ttl expiry at or before it).  Test: no close through the line by
    FLIP_HOLD_MARGIN x ATR[k] over touch..touch + FLIP_HOLD_BARS (1.0 ATR / 6
    bars); truncated when the window passes the tape.  The first hold is the event,
    known at touch + 6; a truncated verdict ends the scan."""
    tape = b["tape"]
    h, l, c, atr, n = tape.h, tape.l, tape.c, tape.atr, tape.n
    H = int(RC.PINS_V2["FLIP_HOLD_BARS"])
    margin = float(RC.PINS_V2["FLIP_HOLD_MARGIN"])
    ttl = int(RC.PINS_V2["MEM_TTL_BARS"])
    exp = _line_expiry(b["v2"]["leash"])
    mem = b["mem"].set_index(["rid", "side"])
    dies = b["dies"]
    rows = []
    for q, (d_i, rid, side) in enumerate(dies):
        nxt = dies[q + 1][0] if q + 1 < len(dies) else n
        end = min(d_i + ttl, nxt - 1, n - 1)
        px = float(mem.loc[(rid, side), "px"])
        if end <= d_i or not np.isfinite(px):
            continue
        e_i = exp.get((rid, side), INF)
        for seq, j in enumerate(_mem_touches(h, l, c, px, d_i, end, side, e_i)):
            j = int(j)
            if j + H >= n:
                v = "truncated"
            else:
                k = np.arange(j, j + H + 1)
                thr = margin * atr[k]
                through = (c[k] < px - thr) if side == "top" else (c[k] > px + thr)
                v = "failed" if through.any() else "hold"
            rows.append({"band": "memory-line", "die_i": d_i, "rid": rid, "side": side,
                         "dir": UP[side], "seq": seq, "touch_i": j,
                         "known_at": j + H, "verdict": v, "is_first_hold": v == "hold",
                         "px": px})
            if v != "failed":
                break
    return _scan_frame(rows, tape, with_px=True)


def oneshot_memory_of(b: dict) -> pd.DataFrame:
    """THE ENGINE'S ONE-SHOT MEMORY FLIP (the twin): per dead range, the leash's ONE
    evaluation of its broken-side line — flip (hold) / failed through / truncated
    — at its touch bar, known at touch + FLIP_HOLD_BARS; not bounded by the next
    death (the engine's law)."""
    tape = b["tape"]
    H = int(RC.PINS_V2["FLIP_HOLD_BARS"])
    side_of = {rid: side for _, rid, side in b["dies"]}
    die_of = {rid: d_i for d_i, rid, _ in b["dies"]}
    rows = []
    for e in b["v2"]["leash"]:
        rid, side = int(e["rid"]), str(e["side"])
        if side_of.get(rid) != side:
            continue
        verdict = e.get("verdict", "")
        v = ("hold" if e["event"] == "flip" else "failed" if verdict.startswith("failed through")
             else "truncated" if verdict.startswith("hold window truncated") else None)
        if v is None:
            continue
        rows.append({"band": "memory-line", "rid": rid, "side": side, "die_i": die_of[rid],
                     "touch_i": int(e["i"]), "known_at": int(e["i"]) + H, "verdict": v,
                     "dir": UP[side]})
    f = pd.DataFrame(rows, columns=["band", "rid", "side", "die_i", "touch_i", "known_at",
                                    "verdict", "dir"])
    for k in ("rid", "die_i", "touch_i", "known_at", "dir"):
        f[k] = f[k].astype(np.int64)
    f["known_close_ms"] = _close_ms(tape, f["known_at"].to_numpy())
    return f


def deaths(stem: str, lens: str, scale_kind: str = "calibrated") -> pd.DataFrame:
    return events(stem, lens, scale_kind)["deaths"]


def hardens(stem: str, lens: str, scale_kind: str = "calibrated") -> pd.DataFrame:
    return events(stem, lens, scale_kind)["hardens"]


def memory_lines(stem: str, lens: str, scale_kind: str = "calibrated") -> pd.DataFrame:
    """The memory-line table (rid, side, px, born, end_live, end_reason); a line
    is LIVE at bar k iff born <= k < end_live (see mem_live_at)."""
    return events(stem, lens, scale_kind)["mem"]


def memory_lines_live_at(stem: str, lens: str, scale_kind: str, bars) -> np.ndarray:
    """(len(bars), n_lines) booleans: which memory lines are LIVE at each bar."""
    return mem_live_at(memory_lines(stem, lens, scale_kind), np.asarray(bars, dtype=np.int64))


def first_retest_scan(stem: str, lens: str, scale_kind: str = "calibrated") -> pd.DataFrame:
    """Every evaluated touch of the first-retest-that-holds scan: the three taps and
    the memory line (band 'memory-line'), first holds flagged."""
    ev = events(stem, lens, scale_kind)
    return pd.concat([ev["scan"], ev["scan_mem"].drop(columns=["px"])], ignore_index=True)


def events(stem: str, lens: str, scale_kind: str = "calibrated") -> dict:
    """All event frames of one (stem, lens, scale_kind), memoised with the bundle."""
    b = bundle11(stem, lens, scale_kind)
    if "_events" not in b:
        lab = scale_label(stem, lens, scale_kind)
        raw = {"deaths": deaths_of(b), "hardens": hardens_of(b), "mem": b["mem"],
               "scan": scan_bands_of(b), "scan_mem": scan_memory_of(b),
               "oneshot": oneshot_bands_of(b), "oneshot_mem": oneshot_memory_of(b)}
        # every frame carries the honesty labels, the in-sample flag read at the
        # row's KNOWN instant (a memory line: its birth close) [verifier finding 5]
        b["_events"] = {k: _label_frame(f, lab, (_close_ms(b["tape"], f["born"].to_numpy())
                                                 if k == "mem" else f["known_close_ms"]))
                        for k, f in raw.items()}
    return b["_events"]


# ══════════════════════════════════════════ 10 · THE L+1 CELL [L-R.6]
CELLS = ("EXP_ALIGNED", "EXP_COUNTER", "IN_RANGE_COINCIDENT", "IN_RANGE_MID", "IN_RANGE_OTHER",
         "NONE", "NA")
STARRED = ("EXP_ALIGNED", "IN_RANGE_COINCIDENT", "IN_RANGE_MID")   # the contract's three ★
CELL_CODE = {c: i for i, c in enumerate(CELLS)}


def _cells(direction, uc: np.ndarray, u_pct: np.ndarray, coin: np.ndarray) -> np.ndarray:
    d = np.broadcast_to(np.asarray(direction, dtype=np.int64), uc.shape)
    with np.errstate(invalid="ignore"):
        mid = (u_pct >= MID_BAND[0]) & (u_pct <= MID_BAND[1])
    out = np.full(uc.shape, "NONE", dtype=object)
    inr = uc == STATE4["IN_RANGE"]
    out[inr & coin] = "IN_RANGE_COINCIDENT"
    out[inr & ~coin & mid] = "IN_RANGE_MID"
    out[inr & ~coin & ~mid] = "IN_RANGE_OTHER"
    exp = (uc == 1) | (uc == -1)
    out[exp & (uc == d)] = "EXP_ALIGNED"
    out[exp & (uc != d)] = "EXP_COUNTER"
    return out


def l1_cell(stem: str, lens: str, scale_kind: str, direction, boundary, known_at_ms
            ) -> pd.DataFrame:
    """THE L+1 PARTITION [L-R.6] of events of lens L: L+1 read AS-OF the event's
    known_at instant (its last closed bar at or before it).  Coincidence = the
    event's boundary of L within COIN_FRAC x ATR_L (ATR of L's as-of bar at the
    instant) of either LIVE L+1 boundary; mid = L+1 pct in [25, 75] and not
    coincident.  'cell_mem' is the twin that also admits L+1's live memory lines.
    'NA' where L has no L+1 (1w) or L+1 is not in the commission (the twelve)."""
    d = np.atleast_1d(np.asarray(direction, dtype=np.int64))
    bnd = np.atleast_1d(np.asarray(boundary, dtype=float))
    inst = np.atleast_1d(np.asarray(known_at_ms, dtype=np.int64))
    U = LADDER[lens]
    n = len(inst)

    def labels(prefix: str, lz) -> dict:            # [L-R.2; verifier finding 5]
        if lz is None:
            return {f"{prefix}_pick_window": [None] * n,
                    f"{prefix}_scale_in_sample": pd.array([pd.NA] * n, dtype="boolean"),
                    f"{prefix}_stability_changed": pd.array([pd.NA] * n, dtype="boolean")}
        lab = scale_label(stem, lz, scale_kind)
        return {f"{prefix}_pick_window": [lab["pick_window"]] * n,
                f"{prefix}_scale_in_sample": pd.array(scale_in_sample(lab, inst), dtype="boolean"),
                f"{prefix}_stability_changed": pd.array([lab["stability_changed"]] * n,
                                                        dtype="boolean")}
    lab_L = labels("l", lens if lens in LENSES_OF[stem] else None)
    if U is None or U not in LENSES_OF[stem] or lens not in LENSES_OF[stem]:
        return pd.DataFrame({"cell": ["NA"] * n, "cell_mem": ["NA"] * n,
                             "u_state": [None] * n, "u_pct": np.full(n, np.nan),
                             "u_k": np.full(n, -1, np.int64), "atr_L": np.full(n, np.nan),
                             **lab_L, **labels("u", None)})
    bL, bU = bundle11(stem, lens, scale_kind), bundle11(stem, U, scale_kind)
    kL = C.asof_index(bL["tape"], inst)
    atr_L = np.where(kL >= 0, bL["tape"].atr[np.where(kL >= 0, kL, 0)], np.nan)
    u = _lens_arrays(bU, inst)
    coin = u["in_range"] & within(bnd, [u["top"], u["bot"]], atr_L)
    live = mem_live_at(bU["mem"], u["k"])
    f = COIN_FRAC
    with np.errstate(invalid="ignore"):
        mcoin = (live & (np.abs(bnd[:, None] - bU["mem"]["px"].to_numpy(float)[None, :])
                         <= (f * atr_L)[:, None])).any(axis=1)
    return pd.DataFrame({"cell": _cells(d, u["state_code"], u["pct"], coin),
                         "cell_mem": _cells(d, u["state_code"], u["pct"], coin | (u["in_range"] & mcoin)),
                         "u_state": STATE4_NAMES[u["state_code"] + 1], "u_pct": u["pct"],
                         "u_k": u["k"], "atr_L": atr_L, **lab_L, **labels("u", U)})


# ══════════════════════════════════════════ 11 · THE DECISION ADAPTER [L-F.2]
def _i8(x) -> np.ndarray:
    """nullable boolean -> int8 (1 True · 0 False · -1 NA)."""
    s = pd.array(x, dtype="boolean")
    return np.where(s.isna(), -1, s.fillna(False).astype(bool)).astype(np.int8)


def range_facts(stem: str, lens: str, scale_kind: str = "calibrated") -> dict:
    """A PLAIN dict of numpy arrays aligned to this lens's bars (and event lists as
    int / float arrays) — what a decision module receives.  It holds no machine
    object, no Range, no event dict: a decision cannot read a field stamped after
    its bar.  Codes: state4 (STATE4: 0 NONE · 1 BULL_EXP · -1 BEAR_EXP · 2
    IN_RANGE), verdict (1 hold · 0 failed · -1 truncated), coin_* (1 · 0 · -1 NA),
    base_cell_* (CELL_CODE), side / dir (+1 top or long · -1 bottom or short).

    AS-OF USE: the per-bar arrays are as-of their own bar.  The event arrays list
    the WHOLE tape's events: a reader at bar k takes only rows with *_known_at <= k
    (a scan row's verdict, a death, a harden), and a memory line is live at k iff
    mem_born <= k < mem_end_live — the VALUE of mem_end_live beyond that test is a
    later fact."""
    b = bundle11(stem, lens, scale_kind)
    tape, view = b["tape"], b["view"]
    close = tape.t0 + tape.step
    lab = scale_label(stem, lens, scale_kind)
    dev_t, dev_b = _dev_carry(view)
    st_ch = lab["stability_changed"]
    out = {"stem": np.array(stem), "lens": np.array(lens), "scale_kind": np.array(scale_kind),
           "scale_mult": np.array(scale_of(stem, lens, scale_kind)),
           "pick_window": np.array(lab["pick_window"]),
           "in_sample_holdout": np.array(lab["in_sample_holdout"]),
           "stability_changed": np.array(-1 if st_ch is None else int(st_ch), dtype=np.int8),
           "scale_in_sample": scale_in_sample(lab, close),
           "open_ms": tape.t0.copy(), "close_ms": close.copy(),
           "in_range": view["in_range"].copy(), "rid": view["rid"].copy(),
           "state": view["state"].astype(np.int8),
           "state4": np.where(view["in_range"], STATE4["IN_RANGE"],
                              view["state"].astype(np.int64)).astype(np.int8),
           "top": view["top"].copy(), "bot": view["bot"].copy(), "atr": tape.atr.copy(),
           "pct": view["pct"].copy(), "near_side": view["near_side"].astype(np.int8),
           "bnd_age": view["bnd_age"].astype(np.int64), "dev_top": dev_t, "dev_bot": dev_b,
           "flip_pol": view["flip_pol"].astype(np.int8),
           "flip_age": view["flip_age"].astype(np.int64)}
    with np.errstate(invalid="ignore"):
        inside = (view["bot"] <= tape.c) & (tape.c <= view["top"])
    out["dist_signed_atr"] = np.where(view["in_range"], np.where(inside, 1.0, -1.0)
                                      * view["dist_atr"], np.nan)
    if lens in NEST_LENSES:                     # the nest flags of L at its own closes
        nv = nest_at(stem, close, scale_kind)
        for fld in ("coin_top", "coin_bot", "coin_top_mem", "coin_bot_mem"):
            out[fld] = _i8(nv[f"{lens}_{fld}"])
        U = LADDER[lens]
        if U is not None and U in LENSES_OF[stem]:
            u_code = np.array([STATE4.get(x, 0) if x is not None else 0
                               for x in nv[f"{U}_state"]], dtype=np.int64)
            u_pct = nv[f"{U}_pct"].to_numpy(float)
            # base-cell coincidence of record = coin_top OR coin_bot (the base rate
            # anchors at every bar and has no event side) — declared in R-FACTS
            # [verifier finding 12]; the per-side twins ride beside so an event row
            # can be set against the base of ITS own side
            out["l1_state4"] = u_code.astype(np.int8)
            out["l1_pct"] = u_pct
            for tag, coin in (("", (out["coin_top"] == 1) | (out["coin_bot"] == 1)),
                              ("_topside", out["coin_top"] == 1),
                              ("_botside", out["coin_bot"] == 1)):
                for nm, d in (("long", 1), ("short", -1)):
                    out[f"base_cell_{nm}{tag}"] = np.array(
                        [CELL_CODE[x] for x in _cells(d, u_code, u_pct, coin)], dtype=np.int8)
    ev = events(stem, lens, scale_kind)
    D, Hd, M = ev["deaths"], ev["hardens"], ev["mem"]
    out.update({"die_i": D["die_i"].to_numpy(np.int64), "die_rid": D["rid"].to_numpy(np.int64),
                "die_dir": D["dir"].to_numpy(np.int64),
                "die_known_at": D["known_at"].to_numpy(np.int64),
                "die_boundary": D["boundary"].to_numpy(float),
                "die_atr": D["atr_known"].to_numpy(float),
                "harden_i": Hd["harden_i"].to_numpy(np.int64),
                "harden_rid": Hd["rid"].to_numpy(np.int64),
                "harden_dir": Hd["dir"].to_numpy(np.int64),
                "harden_known_at": Hd["known_at"].to_numpy(np.int64),
                "harden_pre": Hd["boundary_pre"].to_numpy(float),
                "harden_post": Hd["boundary_post"].to_numpy(float),
                "harden_atr": Hd["atr_known"].to_numpy(float),
                "die_scale_in_sample": D["scale_in_sample"].to_numpy(bool),
                "harden_scale_in_sample": Hd["scale_in_sample"].to_numpy(bool),
                "mem_rid": M["rid"].to_numpy(np.int64), "mem_side": M["dir"].to_numpy(np.int64),
                "mem_px": M["px"].to_numpy(float), "mem_born": M["born"].to_numpy(np.int64),
                "mem_end_live": M["end_live"].to_numpy(np.int64),
                "mem_scale_in_sample": M["scale_in_sample"].to_numpy(bool)})
    for tag, fr in (("scan", ev["scan"]), ("scan_mem", ev["scan_mem"]),
                    ("oneshot", ev["oneshot"]), ("oneshot_mem", ev["oneshot_mem"])):
        for band in (SCAN_BANDS if tag in ("scan", "oneshot") else ("memory-line",)):
            g = fr[fr["band"] == band]
            p = f"{tag}_{band.replace('-', '_')}" if tag in ("scan", "oneshot") else tag
            out[f"{p}_die_i"] = g["die_i"].to_numpy(np.int64)
            out[f"{p}_rid"] = g["rid"].to_numpy(np.int64)
            out[f"{p}_dir"] = g["dir"].to_numpy(np.int64)
            out[f"{p}_touch_i"] = g["touch_i"].to_numpy(np.int64)
            out[f"{p}_known_at"] = g["known_at"].to_numpy(np.int64)
            out[f"{p}_verdict"] = g["verdict"].map(VERDICT).to_numpy(np.int8)
            out[f"{p}_scale_in_sample"] = g["scale_in_sample"].to_numpy(bool)
            if "seq" in g:
                out[f"{p}_seq"] = g["seq"].to_numpy(np.int64)
                out[f"{p}_first_hold"] = g["is_first_hold"].to_numpy(bool)
    return out


# ══════════════════════════════════════════ 12 · THE LEAN BLOCK
READINGS = (
    "R-NEST-1 STATE (four-valued, tierc10_stamps.macro_state_of's collapse): a live confirmed "
    "range -> IN_RANGE; otherwise the machine's latch +1 BULL_EXP / -1 BEAR_EXP; latch 0 "
    "outside a range (no pivot sealed yet) or no closed bar of L yet -> NONE.",
    "R-NEST-2 SIGNED DISTANCE: + when bot <= close <= top (inclusive) at L's as-of bar, - "
    "beyond; |value| = the as-of view's dist_atr (the nearest boundary, ATR of that bar); "
    "near_side beside (+1 top / -1 bottom, tie -> top).",
    "R-NEST-3 COINCIDENCE: per side of L, |L boundary - L+1 top or bottom| <= 0.25 x ATR_L "
    "(INCLUSIVE; ATR_L = ATR of L's as-of bar; all four pairings); both L and L+1 must hold a "
    "LIVE confirmed range at their as-of bars — otherwise False (a fact, not NA); NA only when "
    "L has no L+1 (1w: 'no lens above') or L / L+1 is outside the commission (the twelve's 12h "
    "and 1w, hence their 4h and 1d coincidence).",
    "R-NEST-4 MEMORY-LINE TWIN (coin_*_mem): L+1's LIVE memory lines are admitted beside its "
    "live boundaries. A line = a dead macro range's boundary AS-OF bar die_i - 1 (the view, "
    "full precision; the leash's own line is the machine's end-of-life boundary, equal "
    "because no harden falls at or after die_i — asserted per death). LIVE = the engine's LIVE "
    "(engine/rangefinder.py H3: unfrozen, unexpired): born at die_i, live until its FIRST leash "
    "event — the first two-sided touch freezes it, a cap / ttl expiry ends it — each known at "
    "its own bar; read at L+1's as-of bar.",
    "R-NEST-5 OUT OF RANGE: pct, signed distance, top, bot, bnd_age are NaN / NA; state, "
    "flip (polarity, age) and deviations CARRY — deviations are the live range's hardens per "
    "side, and out of range the LAST live range's final counts as of its last in-range bar "
    "(die_i - 1), 0 before the first range (the as-of view resets them to 0 at a death; the "
    "nest and range_facts carry them instead) [verifier finding 4].",
    "R-SCAN-1 BANDS (tap89 / tap127 / tap200, C.band_of EMAs of close on L's own bars, "
    "C.RETEST_PINS 1.0 ATR / 3 bars / ttl 400): C.retest_holds' touch law and test, applied to "
    "EVERY qualifying touch in bar order in (die_i, min(die_i + 400, next_die - 1, n - 1)]; "
    "the first hold is the event (known at touch + 3) and ends the scan; truncated ends it; "
    "every evaluated touch is a row. Twin: C.retest_holds itself (one-shot).",
    "R-SCAN-2 MEMORY LINE: the dead range's BROKEN-side line (top after a top death, bottom "
    "after a bottom death), same window with MEM_TTL_BARS 400; a qualifying touch contains the "
    "line (l <= px <= h), its prior close sat STRICTLY beyond it on the die side (the band law; "
    "the engine's own flip test reads c[j-1] <= px for a bottom line — equal except on an "
    "exact tie), and the line is unexpired (no cap / ttl expiry at or before the bar); hold = "
    "no close through by 1.0 ATR over touch..touch + 6, known at touch + 6. Twin: the engine's "
    "one-shot flip evaluation (leash flip / failed through / truncated), unbounded by the next "
    "death, as the engine has it.",
    "R-CELL L+1 PARTITION: L+1 read as-of the event's known_at instant; IN_RANGE_COINCIDENT "
    "when the event's boundary of L (BREAKOUT: broken side at die_i - 1; SWING-FAILURE: "
    "deviated side at harden_i - 1, post-redraw at harden_i the Tier-E twin) is within 0.25 x "
    "ATR_L (L's as-of bar at the instant) of either live L+1 boundary; IN_RANGE_MID when L+1 "
    "pct in [25, 75] (inclusive) and not coincident; IN_RANGE_OTHER otherwise; EXP_ALIGNED / "
    "EXP_COUNTER by the L+1 latch vs the event direction; NONE; NA without an L+1. cell_mem = "
    "the twin admitting L+1's live memory lines.",
    "R-CAL-1 calibrated_in_sample is overwritten with the TRUE flag, as text per window: "
    "tuning 'IN-SAMPLE for tuning · OUT-OF-SAMPLE for holdout'; whole 'IN-SAMPLE for tuning AND "
    "holdout'; first half 'IN-SAMPLE for the first half of tuning · OUT-OF-SAMPLE after it' — "
    "with in_sample_tuning / in_sample_holdout booleans beside. First half = tape.head(t_cut "
    "// 2). The 400-bar floor is C.TUNE_MIN_BARS.",
    "R-FACTS range_facts is a plain dict of numpy arrays; per-bar arrays are as-of their "
    "bar, event arrays carry *_known_at (a reader at bar k filters known_at <= k; a memory "
    "line is live at k iff born <= k < end_live). Codes: state4 0 NONE · 1 BULL_EXP · -1 BEAR_EXP · 2 IN_RANGE; verdict "
    "1 hold · 0 failed · -1 truncated; coin_* 1 · 0 · -1 NA; base_cell_long / _short = the L+1 "
    "cell of every closed bar of L, CELL_CODE order "
    + " · ".join(f"{i} {c}" for i, c in enumerate(CELLS)) + ".",
    "R-BASE-COIN (a sub-reading of L-R.6's base rate, declared [verifier finding 12]): the "
    "base rate anchors at EVERY closed bar k of L and has no event side, so its coincidence of "
    "record is L's nest flag coin_top OR coin_bot at k (either boundary of L coincides with "
    "L+1). Rival, printed beside as twins: the per-side base cells base_cell_{long,short}"
    "_topside (coin_top alone) and _botside (coin_bot alone), so an event can be set against "
    "the base of its own side (BREAKOUT: the broken side; SWING-FAILURE: the deviated side).",
    "R-LABEL (L-R.2 'labelled IN-SAMPLE everywhere', 'a change is flagged on every row that "
    "consumes that lens') [verifier finding 5]: every row that reads a lens carries "
    "pick_window ('tuning' · 'whole-tape (fallback)' · 'frozen3.0'), scale_in_sample (a "
    "calibrated read at an instant <= 2024-06-30T23:59:59Z, or ANY read of a fallback pick; "
    "never frozen 3.0; the instant = the nest instant, an event's known close, a bar's close, "
    "a memory line's birth close) and stability_changed (first half of tuning != tuning pick; "
    "NA without a tuning pick). Nest columns L_pick_window / L_scale_in_sample / "
    "L_stability_changed; event frames and l1_cell (l_ / u_ prefixes) and range_facts beside.",
    "R-CENSUS-ROOT one TC11 census root, research_outputs/tierc11/census: C.OUT (the census's "
    "own outputs, C.get_toll) and the env shim's BK.TUNING_RESULT_FOR / HEIGHT_VS_TOLL paths "
    "agree (asserted in the post-shim) [verifier finding 10].",
)


def import_opens_block() -> str:
    """The second import window's data opens — TREE-DEPENDENT, so never part of
    the lean block (the transcript / F-DET bytes)."""
    L = ["[stdout only · tree-dependent] second import window data opens:"]
    for w in E.import_audit():
        if w["label"] in ("tierc10_census", "tierc10_stamps", "tierc10_null"):
            for c_, p_ in w["data_opens"]:
                L.append(f"  {w['label']:<16} data open [{c_}] {p_}")
    return "\n".join(L) + "\n"


def lean_block() -> str:
    L = [f"{LEAN_TAG} L-0.3 TC11 RANGE LAYER (tierc11_nest) · substrate {E.SNAPSHOT.name} · pin "
         f"{PIN_ISO} ({PIN_MS}) · seed {SEED}"]
    L.append(f"{LEAN_TAG} L-0.3 SECOND IMPORT WINDOW (through E.tc10_import, the range door):")
    for w in E.import_audit():
        if w["label"] in ("tierc10_census", "tierc10_stamps", "tierc10_null"):
            L.append(f"  window {w['label']:<16} env {w['env']} · new modules {w['new_modules']} · "
                     f"tc10-snapshot/live touches {len(w['tc10_snapshot_or_live_touches'])} · "
                     f"protected writes {len(w['protected_writes'])} · undeclared tc10 reads "
                     f"{len(w['tc10_unlisted_reads'])}")
    L.append("  (the windows' data opens are TREE-DEPENDENT — the census import reads TC10's "
             "ROOT-relative, gitignored census dir, absent in a review worktree — so they are "
             "printed by `tierc11_nest.py` to stdout, never in this block [verifier finding 3])")
    L.append(f"{LEAN_TAG} L-0.3 RE-ROOTS ({len(REROOTS)}; each verified to exist before assignment):")
    for r in REROOTS:
        L.append(f"  RE-ROOT {r['name']}")
        L.append(f"      {r['old']}")
        L.append(f"   -> {r['new']}   [{r['why']}]")
    L.append(f"{LEAN_TAG} L-0.3 LEFT AS IS (declared; not re-rooted):")
    for r in E.tc10_bindings():
        if r["name"].split(".")[0] in ("tierc10_census", "tierc10_stamps", "tierc10_null"):
            L.append(f"  {r['name']} = {r['value']}  [{r['kind']}] — {NOT_REROOTED.get(r['name'])}")
    L.append(f"{LEAN_TAG} L-0.3 POST-SHIM ASSERTION, tierc11_nest's half ({len(POST_SHIM)} clauses):")
    L += [f"  {x}" for x in POST_SHIM]
    L.append(pins_block().rstrip("\n"))
    L.append(f"{LEAN_TAG} L-R.1 LENSES: {list(LENSES11)} x CLASSIC5; [1h, 4h, 1d] x the twelve. "
             f"Nest lenses {list(NEST_LENSES)}, ladder "
             + " -> ".join(NEST_LENSES) + ". Loader = C.load_tape through the extended dicts: "
             "closed bars <= the pin, full history, ATR = engine.indicators.atr(h, l, c, 14) on "
             "the whole tape (asserted); 1d derived from native 4h == Stage D's 1d file (C's "
             "HALT); 1w = Stage D's derived file == derive_1w(derive_1d(native 4h)) (asserted).")
    L.append(f"{LEAN_TAG} L-R.2 {PICK_LAW}")
    L += [f"{LEAN_TAG} {x}" for x in READINGS]
    L.append(f"{LEAN_TAG} NEVER READ: Range.top / .bottom / .n_deviations, or a price from an "
             f"event. The machine is reached only here; decision modules receive range_facts().")
    return "\n".join(L) + "\n"


__all__ = ["C", "ST", "NL", "RC", "E", "load11", "era_cut11", "calibrate_cell", "build_picks",
           "picks", "scale_of", "view11", "bundle11", "bundle_of", "nest_at", "nest_from_bundles",
           "coin_flags", "within", "mem_live_at", "deaths_of", "hardens_of", "scan_band",
           "deaths", "hardens", "memory_lines", "memory_lines_live_at", "first_retest_scan",
           "scan_bands_of", "scan_memory_of", "oneshot_bands_of", "oneshot_memory_of", "events",
           "l1_cell", "range_facts", "lean_block", "pins_block", "pins_findings", "pick_findings",
           "scale_label", "scale_in_sample", "file_sources", "cell_source", "sources_record",
           "compute_picks", "import_opens_block", "LABEL_FIELDS", "PICK_FILES",
           "COIN_FRAC", "NEST_LENSES", "LADDER", "LENSES11", "LENSES_OF", "STATE4", "CELLS",
           "STARRED", "CELL_CODE", "VERDICT", "PICK_CELLS"]


def main() -> int:
    args = sys.argv[1:]
    if "--build-picks" in args:
        procs = int(next((a.split("=", 1)[1] for a in args if a.startswith("--procs=")), "1"))
        out = next((a.split("=", 1)[1] for a in args if a.startswith("--out=")), None)
        rec = build_picks(procs=procs, out=None if out is None else Path(out))
        sys.stdout.write(f"filed {rec['n_cells']} cells · grid {rec['grid_rows']} rows sha "
                         f"{rec['grid_content_sha256']}\n")
        return 0
    if "--file-sources" in args:
        rec = file_sources()
        sys.stdout.write(f"filed {E.rel_of(E._real(SOURCES_PATH))} · {rec['n_cells']} cells · "
                         f"annotates {rec['annotates']} sha256 {rec['annotates_sha256']}\n")
        return 0
    sys.stdout.write(lean_block())
    sys.stdout.write(import_opens_block())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
