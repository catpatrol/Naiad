#!/usr/bin/env python
"""TIER-C10 · STAGE 0b — F-RNG-ASOF · F-RF-4 · F-GRID · F-C10-TOLL (groundwork) ·
F-CEN-TAPE · F-CEN-OUTCOME · F-CEN-HOLD · F-DET.  The fixtures of CENSUS-R.
TWO LEGS PER FIXTURE, the BREAK leg first and it must go RED, or the fixture
proves nothing [the prove() law, carried from the RF suites through
scripts/tierc10_rf_fixtures.py, whose harness this file imports].  Every plant
is made on a COPY — an array, a frame, a text, a throwaway directory; no real
artifact is touched.

WHAT IS ON TRIAL.  scripts/tierc10_census.py turns the port's event logs into
per-bar AS-OF arrays, six classes of events, and outcome tables net of a
measured toll.  Four ways it could lie, one fixture each, and the rest:
  F-RNG-ASOF    PREFIX-STABILITY: on seeded random cuts AND on cuts aimed at the
                structure (one bar before a redraw, inside a flip's hold window,
                at a confirm, at a pivot's seal) the as-of arrays, the class
                events and the known_at-filtered logs computed on tape[:t] equal
                the full run's view restricted to <= t - 1; and the view at
                t - 1 equals the MACHINE's own end-of-prefix state (the engine's
                on the 1d tapes).  SABOTAGE: a leaked redraw, a flip read at its
                stamp bar, a back-dated left edge, a naive known_at — each RED.
  F-RNG-ASOF-SEAL  the engine's knowable_at = -1 quirk (engine/rangefinder.py:497-502:
                a numpy-rounded key read with a Python-rounded price): on NEARUSDT
                4h, UNIUSDT 4h and a SOLUSDT 5m slice, 30 seeded cuts per tape x
                SCALE aimed first at the -1 pivots — the census hands each its SEAL,
                and the ENGINE's own prefix runs of the raw tape show the pivot
                absent on tape[:seal] and present on tape[:seal + 1].  SABOTAGE: the
                field read as it stands (-1 = known before the tape), and -1
                "repaired" to the wick bar — each RED, through the pivot log alone.
  F-RF-4       spring kinship, parametrised off the BTC-1D globals and mirrored
                (bottom springs, top upthrusts), both overlap directions PRINTED;
                the bottom side must reproduce the v1 suite's own record numbers
                and the top side must be the bottom's exact mirror.
  F-GRID        every grid whole: declared literal vs filed, NaN cells explicit
                with their reason, collar + as-of columns on every table, no
                verdict column anywhere, grid rows recomputed from the FILED
                ledgers, the SCALE grid whole with one pick under the printed
                tie-break.
  F-C10-TOLL    (groundwork) get_toll reads ONLY the grid; the quoted number is
                re-derived from raw bars + the estate fee object; a perturbed
                COPY moves the quote; an AST scan finds no numeric literal in a
                toll position.
  F-CEN-TAPE    the loader: closed bars <= AS_OF, 1d = six native-4h bars [L1],
                the engine's ATR, a prefix's ATR is the full tape's (a tail's
                is not — chunking is illegal).
  F-CEN-OUTCOME term / MFE / MAE / toll per event re-walked with plain loops on
                the raw parquet; CENSORED, never shortened.
  F-CEN-HOLD    the parameterised retest-hold detector re-walked with plain
                loops for EVERY macro DIE; every flip-hold re-verified on raw
                bars at touch + HOLD; a failed hold must FAIL.
  F-DET         two subprocess builds under DIFFERENT hash seeds: same shas,
                same bytes; a resumed run reuses every cell; a moved table is
                not reused.

BANNED HERE, as in every tier suite: self-comparison; one example where
cardinality was possible; a tuned magnitude bound standing in for an identity;
a check whose claim is not the design's claim.

FROZEN SUBSTRATE [TIER-C10 law 3]: HALTs unless NAIAD_CACHE_DIR is the TC10
snapshot.  Seed 20260921.  TIER-E: nothing here scores, registers or gates.
The transcript filed beside the grid carries no wall clock.

Run: NAIAD_CACHE_DIR=~/.cache/naiad/snapshots/tc10_20260921 \\
     ~/venvs/naiad/bin/python scripts/tierc10_census_fixtures.py [--root=DIR] [leg ...]
     (any other argument is matched as a substring of the leg id, case-blind;
     --root defaults to the filed census, else the smoke root)
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
import time
from pathlib import Path

sys.dont_write_bytecode = True

import numpy as np                                                   # noqa: E402
import pandas as pd                                                  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import tierc10_census as C                                           # noqa: E402
import tierc10_rf_fixtures as RFX                                    # noqa: E402
from analytics import rangefinder_census as RC                       # noqa: E402
from engine import rangefinder as E                                  # noqa: E402
from engine.data import cache_dir                                    # noqa: E402
import tierc2_rules as R2                                            # noqa: E402

SEED = 20260921
# --slow: F-C10-ACC re-walks EVERY cell of the per-cell replay ledger instead of
# the seeded sample.  Stated in the transcript either way, never silent.
ACC_SLOW = any(a == "--slow" for a in sys.argv[1:])
PY = str(Path.home() / "venvs" / "naiad" / "bin" / "python")
say, clock, prove, plants = RFX.say, RFX.clock, RFX.prove, RFX.plants

# THE COMMISSION'S LITERALS, typed HERE — a second object beside the engine's
# own, so "declared vs written" is never one tuple counted twice.
DECL_RETEST = ("retest-hold-ribbon89_127", "retest-hold-ribbon127_200",
               "retest-hold-tap89", "retest-hold-tap127", "retest-hold-tap200")
DECL_CLASSES = ("breach", "harden", "DIE", "memory-touch-v1", "memory-touch-2s",
                "flip-hold") + DECL_RETEST
DECL_KINDS = ("frozen3.0", "calibrated")
DECL_HORIZONS = {"H20": 20, "H100": 100}
DECL_ERAS = ("ALL", "tuning", "holdout")
DECL_ERA_BOUNDARY_MS = 1719791999000         # 2024-06-30T23:59:59Z [R1], typed HERE
DECL_SCALES = (1.5, 1.75, 2.0, 2.25, 2.5, 2.75, 3.0, 3.25, 3.5, 3.75, 4.0)
DECL_TUNED = DECL_RETEST                     # the R1-tuned pin pair rules all five
DECL_SIDES = ("bottom", "top")
DECL_ANCHORS = ("memory-line",) + tuple(c[len("retest-hold-"):] for c in DECL_RETEST)
DECL_MARGINS = (0.25, 0.5, 1.0)              # R1, verbatim
DECL_HOLDS = (3, 6, 12)                      # R1, verbatim
VERDICT_COLUMNS = ("verdict", "clears_bh_bar", "promotable", "scored_in_family",
                   "p_one_sided", "is_the_registered_cell")


def census_root() -> Path:
    for a in sys.argv[1:]:
        if a.startswith("--root="):
            return Path(a.split("=", 1)[1]).expanduser().resolve()
    full = C.OUT / "build_manifest.json"
    return C.OUT if full.exists() else C.OUT / "smoke"


CROOT = census_root()


def rel(p: Path) -> str:
    """Repo-relative when the path is in the repo (a transcript names no home
    directory); the path itself for a --root outside it."""
    try:
        return Path(p).resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return str(p)


def manifest() -> dict:
    p = CROOT / "build_manifest.json"
    if not p.exists():
        raise SystemExit(f"HALT: no census build under {CROOT} — run "
                         "scripts/tierc10_census.py first (the smoke: --assets BTCUSDT "
                         "--lenses 4h,1d --out research_outputs/tierc10/census/smoke)")
    return json.loads(p.read_text())


def tol(x: float, roundings: int = 1) -> float:
    """DERIVED, not tuned: a filed float is rounded to ROUND_ND places, so it
    sits within half a unit of the last place of the truth — once per rounding
    between the truth and the filed figure (a median is 1-Lipschitz, so a
    median of rounded values, rounded again, is two) — plus float noise
    between two orders of the same arithmetic."""
    return roundings * 0.5 * 10.0 ** -C.ROUND_ND + 1e-11 * max(1.0, abs(x))


def same(a, b, roundings: int = 1) -> bool:
    a, b = float(a), float(b)
    return (np.isnan(a) and np.isnan(b)) or (np.isfinite(a) and np.isfinite(b)
                                             and abs(a - b) <= tol(b, roundings))


_TAPE: dict = {}


def tape_of(sym: str, lens: str) -> C.Tape:
    if (sym, lens) not in _TAPE:
        _TAPE[(sym, lens)] = C.load_tape(sym, lens)
    return _TAPE[(sym, lens)]


def own_atr(h, l, c, length: int) -> np.ndarray:
    """Wilder's ATR seeded at TR[0], written HERE with a plain loop — it shares
    nothing with engine.indicators (a poisoned shared builder passes every leg
    that reads it)."""
    n = len(c)
    out = np.empty(n)
    prev = h[0] - l[0]
    out[0] = prev
    for i in range(1, n):
        tr = max(h[i] - l[i], abs(h[i] - c[i - 1]), abs(l[i] - c[i - 1]))
        prev = prev + (tr - prev) / length
        out[i] = prev
    return out


def own_ema(c, period: int) -> np.ndarray:
    out = np.empty(len(c))
    prev = c[0]
    out[0] = prev
    a = 2.0 / (period + 1.0)
    for i in range(1, len(c)):
        prev = prev + a * (c[i] - prev)
        out[i] = prev
    return out


def raw_tape(sym: str, lens: str) -> dict:
    """The fixture's OWN read of the snapshot — pandas on the parquet, the
    AS_OF cut and the six-bar day written again here."""
    src = "4h" if lens == "1d" else lens
    f = pd.read_parquet(cache_dir() / "klines" / f"{sym}_{src}.parquet")
    f = f.sort_values("open_time").reset_index(drop=True)
    close_ms = int(json.loads((C.STAGE_D / "AS_OF_PIN.json").read_text())
                   ["as_of_last_closed_4h_close_ms"])
    f = f[f["open_time"] + C.LENS_MS[src] <= close_ms].reset_index(drop=True)
    if lens == "1d":
        d = RFX.tape_1d(f)
        return {"t0": d["t0"].to_numpy(np.int64), "o": d["o"].to_numpy(float),
                "h": d["h"].to_numpy(float), "l": d["l"].to_numpy(float),
                "c": d["c"].to_numpy(float), "close_ms": close_ms}
    return {"t0": f["open_time"].to_numpy(np.int64), "o": f["open"].to_numpy(float),
            "h": f["high"].to_numpy(float), "l": f["low"].to_numpy(float),
            "c": f["close"].to_numpy(float), "close_ms": close_ms}


# ═════════════════════════════════════════════════════════ F-RNG-ASOF
ASOF_TAPES = (("BTCUSDT", "4h", None), ("BTCUSDT", "1d", None), ("ETHUSDT", "4h", None),
              ("ETHUSDT", "1d", None), ("SOLUSDT", "5m", 60_000))
ASOF_SCALES = (3.0, 2.0)         # the frozen pin, and one more so the law is not
                                 # a property of one SCALE
ASOF_RANDOM_CUTS = 14
ASOF_STRUCT_EACH = 5
ASOF_EVENT_COLS = ["cls", "i", "known_at", "rid", "side", "sgn"]
LAWS = ("honest", "leaked-redraw", "flip-at-stamp", "backdated-edge", "naive-known-at")


def _bounds_derived(tape, v):
    with np.errstate(invalid="ignore", divide="ignore"):
        v["pct"] = 100.0 * (tape.c - v["bot"]) / (v["top"] - v["bot"])
        v["dist_atr"] = np.minimum(np.abs(v["top"] - tape.c),
                                   np.abs(tape.c - v["bot"])) / tape.atr
    return v


def _law_views(tape, macro, leash, view, evf):
    """The honest view + FOUR LEAKY READERS of ONE run, each built on a COPY:
    what a census that broke one as-of rule would have computed on this tape.
    The SAME reader is applied to the full tape and to every prefix — so a
    plant goes RED only through what the fixture really tests (the prefix is
    not stable under the leak, or the machine's own end-state disagrees), never
    because an honest prefix was compared with a dishonest full run."""
    n, hold = tape.n, int(RC.PINS_V2["FLIP_HOLD_BARS"])
    kf, lf = C.known_frame(macro), C.leash_frame(leash, hold)
    out = {"honest": (view, evf, kf["known_at"].to_numpy(), lf["known_at"].to_numpy())}
    # 1 · a LEAKED REDRAW: bounds read off Range.top / .bottom (end-of-run)
    v = dict(view)
    v["top"], v["bot"] = view["top"].copy(), view["bot"].copy()
    for r in macro["ranges"]:
        if r.confirm_i >= 0:
            b = r.die_i if r.die_i >= 0 else n
            v["top"][r.confirm_i:b], v["bot"][r.confirm_i:b] = r.top, r.bottom
    out["leaked-redraw"] = (_bounds_derived(tape, v),) + out["honest"][1:]
    # 2 · a FLIP READ AT ITS OWN STAMP BAR
    e2 = evf.copy()
    m = e2["cls"] == "flip-hold"
    e2.loc[m, "known_at"] = e2.loc[m, "i"]
    v = dict(view)
    fl = lf[lf["event"] == "flip"].sort_values(["i", "pos"], kind="mergesort")
    pol = [1 if s == "top" else -1 for s in fl["side"]]
    v["flip_pol"] = C._step_fill(n, list(zip(fl["i"].tolist(), pol)), 0, np.int8)
    known = C._step_fill(n, list(zip(fl["i"].tolist(), fl["i"].tolist())), -1, np.int64)
    v["flip_age"] = np.where(known >= 0, np.arange(n) - known, -1)
    v["flip_rid"] = C._step_fill(n, list(zip(fl["i"].tolist(), fl["rid"].tolist())),
                                 -1, np.int64)
    out["flip-at-stamp"] = (v, e2) + out["honest"][2:]
    # 3 · the BACK-DATED LEFT EDGE read as life
    v = dict(view)
    for k in ("top", "bot", "rid", "in_range"):
        v[k] = view[k].copy()
    for r in macro["ranges"]:
        if r.confirm_i >= 0 and 0 <= r.backdated_from < r.confirm_i:
            s = slice(r.backdated_from, r.confirm_i)
            v["top"][s], v["bot"][s], v["rid"][s], v["in_range"][s] = (
                r.top0, r.bottom0, r.rid, True)
    out["backdated-edge"] = (_bounds_derived(tape, v),) + out["honest"][1:]
    # 4 · NAIVE known_at: every event read at its own stamp bar
    out["naive-known-at"] = (view, evf, kf["i"].to_numpy(), lf["i"].to_numpy())
    return out


def _cuts(tape, macro, leash, evf, rng) -> list[int]:
    n, hold = tape.n, int(RC.PINS_V2["FLIP_HOLD_BARS"])
    cuts = set(rng.integers(200, n + 1, size=ASOF_RANDOM_CUTS).tolist())

    def pick(xs):
        xs = sorted(set(int(x) for x in xs if 200 <= x <= n))
        return [xs[k] for k in sorted(rng.choice(len(xs), size=min(ASOF_STRUCT_EACH, len(xs)),
                                                 replace=False).tolist())] if xs else []
    hard = [e["i"] for e in macro["events"] if e["event"] == "harden"]
    conf = [r.confirm_i for r in macro["ranges"] if r.confirm_i >= 0]
    flips = evf[evf["cls"] == "flip-hold"]["i"].tolist()
    cuts |= set(pick(hard)) | set(pick([x + 1 for x in hard]))   # one bar before the
    cuts |= set(pick(conf)) | set(pick([x + 1 for x in conf]))   # redraw; and with it
    cuts |= set(pick([i + 1 + int(rng.integers(0, hold)) for i in flips]))
    cuts |= set(pick(macro["seals"]))                             # tape[:seal] must not see it
    return sorted(cuts)


def _oracle(tape, t, pins, engine: bool) -> dict:
    """The MACHINE's own end-of-prefix state — never the census's as-of code.
    On the 1d tapes the machine is the ENGINE's; elsewhere the port's (held
    byte-equal to the engine by F-RF-EQ; the engine is O(n^2))."""
    p = tape.head(t)
    if engine:
        d = pd.DataFrame({"o": p.o, "h": p.h, "l": p.l, "c": p.c, "ts": p.ts})
        m = E.run_machine(d, pins)
    else:
        m = RC.run_machine(p.d, p.atr, pins)
    alive = [r for r in m["ranges"] if r.state == "CONFIRMED"]
    return {"state": {"NEUTRAL": 0, "BULL_EXP": 1, "BEAR_EXP": -1}[m["final_state"]],
            "rid": alive[0].rid if alive else -1,
            "top": alive[0].top if alive else np.nan,
            "bot": alive[0].bottom if alive else np.nan,
            "ndev": alive[0].n_deviations if alive else 0,
            "coverage_pct": m["coverage_pct"]}


_ASOF: dict = {}


def asof_corpus() -> dict:
    """ONE pass, memoised: per tape x SCALE, the full run, its five readers, and
    every prefix — compared as it is built, so no prefix array is kept."""
    if _ASOF:
        return _ASOF
    rng = np.random.default_rng(SEED)
    bad = {law: [] for law in LAWS}
    caught = {law: {} for law in LAWS}
    stat = {"cuts": 0, "arrays": 0, "events": 0, "oracle": 0, "late_known": 0, "tapes": [],
            "tags": []}
    for sym, lens, head in ASOF_TAPES:
        tape = tape_of(sym, lens)
        tape = tape if head is None else tape.head(head)
        for scale in ASOF_SCALES:
            tag = f"{sym} {lens}{'' if head is None else f'[:{head}]'} @{scale:g}"
            v2 = C.run_scale(tape, scale)
            macro, leash = v2["macro"], v2["leash"]
            view = C.asof_view(tape, macro, leash)
            evf, _ = C.census_events(tape, macro, leash, view)
            readers = _law_views(tape, macro, leash, view, evf)
            stat["late_known"] += int((evf["known_at"] != evf["i"]).sum())
            cuts = _cuts(tape, macro, leash, evf, rng)
            stat["tags"].append(tag)
            stat["tapes"].append(f"{tag}: n={tape.n:,}, {len(cuts)} cuts, "
                                 f"{len(evf):,} class events")
            pins = RC.macro_pins(scale)
            for t in cuts:
                p = tape.head(t)
                pv2 = C.run_scale(p, scale)
                pview = C.asof_view(p, pv2["macro"], pv2["leash"])
                pev, _ = C.census_events(p, pv2["macro"], pv2["leash"], pview)
                preaders = _law_views(p, pv2["macro"], pv2["leash"], pview, pev)
                orc = _oracle(tape, t, pins, engine=(lens == "1d"))
                stat["cuts"] += 1
                for law, (fv, fev, fk, flk) in readers.items():
                    pv, pe, pk, plk = preaders[law]
                    want_ev = pe[pe["known_at"] <= t - 1][ASOF_EVENT_COLS].to_records(index=False).tolist()
                    want_m = RFX.sha([e for e, k in zip(pv2["macro"]["events"], pk) if k <= t - 1])
                    want_l = RFX.sha([e for e, k in zip(pv2["leash"], plk) if k <= t - 1])
                    found = []
                    for name in C.ASOF_ARRAYS:
                        if not np.array_equal(fv[name][:t], pv[name], equal_nan=True):
                            found.append(f"array `{name}`")
                    got_ev = fev[fev["known_at"] <= t - 1][ASOF_EVENT_COLS].to_records(index=False).tolist()
                    if sorted(got_ev) != sorted(want_ev):
                        found.append(f"class events ({len(got_ev)} vs prefix {len(want_ev)})")
                    if RFX.sha([e for e, k in zip(macro["events"], fk) if k <= t - 1]) != want_m:
                        found.append("macro log")
                    if RFX.sha([e for e, k in zip(leash, flk) if k <= t - 1]) != want_l:
                        found.append("leash log")
                    k = t - 1
                    if int(fv["state"][k]) != orc["state"]:
                        found.append("state vs the machine's final_state")
                    if int(fv["rid"][k]) != orc["rid"] or not (
                            same(fv["top"][k], orc["top"]) and same(fv["bot"][k], orc["bot"])):
                        found.append("bounds vs the machine's alive Range")
                    if int(fv["dev_top"][k] + fv["dev_bot"][k]) != orc["ndev"]:
                        found.append("deviations vs Range.n_deviations")
                    if round(100.0 * int(fv["covered"][:t].sum()) / t, 2) != orc["coverage_pct"]:
                        found.append("coverage vs the machine's coverage_pct")
                    if found:
                        bad[law].append(f"{tag} cut {t}: " + ", ".join(found))
                        caught[law][tag] = caught[law].get(tag, 0) + 1
                stat["arrays"] += len(C.ASOF_ARRAYS)
                stat["events"] += int((pev["known_at"] <= t - 1).sum())
                stat["oracle"] += 4
    _ASOF.update({"bad": bad, "caught": caught, "stat": stat})
    return _ASOF


def asof_break():
    A = asof_corpus()
    tags = A["stat"]["tags"]

    def plant(law):
        miss = [t for t in tags if t not in A["caught"][law]]
        if miss:                       # a leak that one tape x SCALE lets through
            return []                  # is a leak the fixture cannot see
        return [f"RED on all {len(tags)} tape x SCALE runs "
                f"({sum(A['caught'][law].values())} cuts), e.g. {A['bad'][law][0]}"]
    return plants([
        ("LEAKED REDRAW (as-of bounds read off Range.top / .bottom — end-of-run values)",
         lambda: plant("leaked-redraw")),
        ("FLIP AT ITS STAMP BAR (flip-hold anchored at the touch bar i, not i + HOLD)",
         lambda: plant("flip-at-stamp")),
        ("BACK-DATED LEFT EDGE (a range read as alive from backdated_from)",
         lambda: plant("backdated-edge")),
        ("NAIVE known_at (every event read at its own stamp bar — a pivot at its wick)",
         lambda: plant("naive-known-at")),
    ])


def asof_real():
    A = asof_corpus()
    st, bad = A["stat"], A["bad"]["honest"]
    for line in st["tapes"]:
        say(f"        {line}")
    return not bad, (
        f"{st['cuts']} cuts (seeded random + aimed at hardens, confirms, flip hold windows "
        f"and pivot seals) over {len(st['tapes'])} tape x SCALE runs on "
        f"{len({x[0] for x in ASOF_TAPES})} assets x {len({x[1] for x in ASOF_TAPES})} lenses: "
        f"all {len(C.ASOF_ARRAYS)} as-of arrays, the class events and both known_at-filtered "
        f"logs of tape[:t] equal the full view restricted to <= t - 1; state / bounds / "
        f"deviations / coverage at t - 1 equal the MACHINE's own end-of-prefix state (the "
        f"ENGINE's on 1d) — 0 mismatches; {st['late_known']} class events are anchored LATER "
        f"than they are stamped" if not bad else f"{len(bad)} mismatches: " + "; ".join(bad[:3]))


# ═════════════════════════════════════════════════ F-RNG-ASOF-SEAL (the -1 quirk)
# THE QUESTION THIS LEG CLOSES.  The engine (engine/rangefinder.py:497-502), and
# therefore the byte-identical port, ships knowable_at = -1 on some pivots: the
# seal lookup is keyed on a numpy-rounded price and read with a Python-rounded
# one.  A reader that took that field as the known bar would see such a pivot
# from BEFORE THE TAPE — look-ahead, on exactly the assets that carry them.  The
# census reads the port's recorded SEAL (macro["seals"], the bar the zigzag
# reversal fired) and never that field; this leg proves it on the tapes where
# the quirk lives, against the ENGINE's own prefix runs of the raw tape.
SEAL_TAPES = (("NEARUSDT", "4h", None), ("UNIUSDT", "4h", None), ("SOLUSDT", "5m", 60_000))
SEAL_SCALES = (3.0, 2.0)
SEAL_CUTS = 30                   # per tape x SCALE, seeded
SEAL_AIMED_MAX = 21              # of which at most this many are aimed at -1 pivots
SEAL_LAWS = ("honest", "engine-knowable-at", "repaired-to-stamp-bar")


def _engine_run(tape, t, pins) -> dict:
    p = tape.head(t)
    return E.run_machine(pd.DataFrame({"o": p.o, "h": p.h, "l": p.l, "c": p.c, "ts": p.ts}),
                         pins)


def _seal_readers(macro) -> dict:
    """known_at per macro event under the honest law and under TWO leaky
    readers of the engine's knowable_at field, each a fresh list (a COPY — the
    run is never edited).  The same reader is applied to the full tape and to
    every prefix."""
    ev = macro["events"]
    honest = C.known_frame(macro)["known_at"].tolist()
    field = [e["knowable_at"] if e["event"] == "pivot" else e["i"] for e in ev]
    return {"honest": honest,
            # -1 read as it stands: "known since before the tape"
            "engine-knowable-at": field,
            # -1 "repaired" to the pivot's own STAMP (wick) bar — the cheap fix
            "repaired-to-stamp-bar": [max(k, e["i"]) for k, e in zip(field, ev)]}


_SEAL: dict = {}


def seal_corpus() -> dict:
    if _SEAL:
        return _SEAL
    rng = np.random.default_rng([SEED, 1])          # its own stream: F-RNG-ASOF's cuts stay put
    bad = {law: [] for law in SEAL_LAWS}
    caught = {law: {} for law in SEAL_LAWS}
    other = {law: [] for law in SEAL_LAWS}          # findings NOT about the pivot log
    stat = {"cuts": 0, "neg": 0, "pivots": 0, "proved": 0, "tags": [], "lines": [],
            "vacuous": [], "early": 0}
    for sym, lens, head in SEAL_TAPES:
        tape = tape_of(sym, lens)
        tape = tape if head is None else tape.head(head)
        for scale in SEAL_SCALES:
            tag = f"{sym} {lens}{'' if head is None else f'[:{head}]'} @{scale:g}"
            pins = RC.macro_pins(scale)
            v2 = C.run_scale(tape, scale)
            macro, leash = v2["macro"], v2["leash"]
            view = C.asof_view(tape, macro, leash)
            evf, _ = C.census_events(tape, macro, leash, view)
            kf = C.known_frame(macro)
            readers = _seal_readers(macro)
            seal_at = {(p[0], "high" if p[2] == 1 else "low"): int(s)
                       for p, s in zip(macro["pivots"], macro["seals"])}
            neg = [(e["i"], e["side"], seal_at[(e["i"], e["side"])]) for e in macro["events"]
                   if e["event"] == "pivot" and e["knowable_at"] == -1]
            stat["tags"].append(tag)
            stat["neg"] += len(neg)
            stat["pivots"] += len(macro["pivots"])
            if not neg:
                stat["vacuous"].append(tag)
            # the census's own known_at: never before the stamp, never -1
            stat["early"] += int((kf["known_at"] < kf["i"]).sum())
            # (a) THE HONEST KNOWN BAR, RECOMPUTED FROM THE RAW TAPE by the ENGINE:
            # the pivot is absent on tape[:seal] and present on tape[:seal + 1]
            for w, side, s in neg:
                def has(t):
                    return any(e["event"] == "pivot" and e["i"] == w and e["side"] == side
                               for e in _engine_run(tape, t, pins)["events"])
                got = int(kf[(kf["event"] == "pivot") & (kf["i"] == w)
                             & (kf["side"] == side)]["known_at"].iloc[0])
                if got != s or s <= w or has(s) or not has(s + 1) or has(w + 1):
                    bad["honest"].append(f"{tag} pivot@{w} {side}: census known_at {got}, "
                                         f"seal {s}, engine sees it on tape[:{s}]={has(s)} "
                                         f"tape[:{s + 1}]={has(s + 1)}")
                else:
                    stat["proved"] += 1
            # (b) PREFIX-RECOMPUTE on SEAL_CUTS seeded cuts, aimed first at the -1 pivots
            aimed = []
            for w, side, s in neg:
                aimed += [s, s + 1, int(rng.integers(w + 1, s + 1))]
            aimed = sorted({x for x in aimed if 200 <= x <= tape.n})
            if len(aimed) > SEAL_AIMED_MAX:
                aimed = [aimed[k] for k in sorted(rng.choice(len(aimed), size=SEAL_AIMED_MAX,
                                                             replace=False).tolist())]
            cuts = set(aimed)
            while len(cuts) < SEAL_CUTS:
                cuts.add(int(rng.integers(200, tape.n + 1)))
            stat["lines"].append(
                f"{tag}: n={tape.n:,}, {len(neg)} of {len(macro['pivots'])} pivots ship "
                f"knowable_at = -1 (wick -> seal: "
                + ", ".join(f"{w}->{s}" for w, _, s in neg[:4])
                + (", …" if len(neg) > 4 else "") + f"); {len(cuts)} cuts, {len(aimed)} aimed")
            for t in sorted(cuts):
                p = tape.head(t)
                pv2 = C.run_scale(p, scale)
                pview = C.asof_view(p, pv2["macro"], pv2["leash"])
                pev, _ = C.census_events(p, pv2["macro"], pv2["leash"], pview)
                preaders = _seal_readers(pv2["macro"])
                em = _engine_run(tape, t, pins)
                alive = [r for r in em["ranges"] if r.state == "CONFIRMED"]
                stat["cuts"] += 1
                k = t - 1
                base = []
                for name in C.ASOF_ARRAYS:
                    if not np.array_equal(view[name][:t], pview[name], equal_nan=True):
                        base.append(f"array `{name}`")
                got_ev = evf[evf["known_at"] <= k][ASOF_EVENT_COLS].to_records(index=False).tolist()
                want_ev = pev[pev["known_at"] <= k][ASOF_EVENT_COLS].to_records(index=False).tolist()
                if sorted(got_ev) != sorted(want_ev):
                    base.append("class events")
                if int(view["state"][k]) != {"NEUTRAL": 0, "BULL_EXP": 1,
                                             "BEAR_EXP": -1}[em["final_state"]]:
                    base.append("state vs the ENGINE's final_state")
                if int(view["rid"][k]) != (alive[0].rid if alive else -1) or not (
                        same(view["top"][k], alive[0].top if alive else np.nan)
                        and same(view["bot"][k], alive[0].bottom if alive else np.nan)):
                    base.append("bounds vs the ENGINE's alive Range")
                for law in SEAL_LAWS:
                    fk, pk = readers[law], preaders[law]
                    found = list(base)
                    if (RFX.sha([e for e, q in zip(macro["events"], fk) if q <= k])
                            != RFX.sha([e for e, q in zip(pv2["macro"]["events"], pk) if q <= k])):
                        found.append("macro log (the pivots)")
                    # the ENGINE's prefix log is the WHOLE truth at t: nothing to filter
                    if (law == "honest" and RFX.sha([e for e, q in zip(macro["events"], fk)
                                                     if q <= k and e["event"] == "pivot"])
                            != RFX.sha([e for e in em["events"] if e["event"] == "pivot"])):
                        found.append("pivot log vs the ENGINE's own run of tape[:t]")
                    if found:
                        bad[law].append(f"{tag} cut {t}: " + ", ".join(found))
                        caught[law][tag] = caught[law].get(tag, 0) + 1
                    other[law] += [f for f in found if f != "macro log (the pivots)"]
    _SEAL.update({"bad": bad, "caught": caught, "other": other, "stat": stat})
    return _SEAL


def seal_break():
    A = seal_corpus()
    tags = A["stat"]["tags"]

    def plant(law):
        # judged on the planted item ALONE: RED on every tape x SCALE, and RED
        # through the pivot log only — anything else would be another defect
        if [t for t in tags if t not in A["caught"][law]] or A["other"][law]:
            return []
        return [f"RED on all {len(tags)} tape x SCALE runs "
                f"({sum(A['caught'][law].values())} cuts, pivot log only), e.g. "
                f"{A['bad'][law][0]}"]
    return plants([
        ("ENGINE knowable_at READ AS THE KNOWN BAR (-1 = known since before the tape)",
         lambda: plant("engine-knowable-at")),
        ("-1 REPAIRED TO THE STAMP BAR (known at the pivot's own wick, not at its seal)",
         lambda: plant("repaired-to-stamp-bar")),
    ])


def seal_real():
    A = seal_corpus()
    st, bad = A["stat"], A["bad"]["honest"]
    for line in st["lines"]:
        say(f"        {line}")
    if st["vacuous"]:
        return False, f"VACUOUS: no knowable_at = -1 pivot on {st['vacuous']} — the leg tests nothing there"
    if st["early"]:
        return False, f"{st['early']} macro event(s) carry a census known_at BEFORE their own stamp bar"
    return not bad, (
        f"{st['neg']} of {st['pivots']} pivots on {len(st['tags'])} tape x SCALE runs "
        f"(NEARUSDT 4h, UNIUSDT 4h, SOLUSDT 5m[:60000]) ship the engine's knowable_at = -1; "
        f"the census reads NONE of them from that field: known_frame hands each its SEAL, and "
        f"all {st['proved']} were shown by ENGINE prefix runs of the raw tape to be ABSENT on "
        f"tape[:wick + 1] and tape[:seal] and PRESENT on tape[:seal + 1]; {st['cuts']} seeded "
        f"cuts ({SEAL_CUTS} per run, aimed first at those seals): all {len(C.ASOF_ARRAYS)} as-of "
        f"arrays, the class events and the known_at-filtered macro log of tape[:t] equal the "
        f"full view restricted to <= t - 1, the pivot log equals the ENGINE's own run of "
        f"tape[:t], and state / bounds at t - 1 equal the ENGINE's end-of-prefix — 0 mismatches; "
        f"no census known_at precedes its stamp bar"
        if not bad else f"{len(bad)} mismatches: " + "; ".join(bad[:3]))


# ═══════════════════════════════════════════════════════════ F-RF-4
def _record_tape():
    """The v1 suite's own tape and machine (BTC 1D, 420 days at the record
    anchor) — imported, so its numbers are ITS numbers."""
    import rangefinder_fixtures as V1
    D = V1.D
    t0 = D["t0"].to_numpy(np.int64)
    tape = C.Tape("BTCUSDT", "1d", D["o"].to_numpy(float), D["h"].to_numpy(float),
                  D["l"].to_numpy(float), D["c"].to_numpy(float), t0, D["ts"].tolist(),
                  RFX.atr_of(D), {})
    return V1, tape


def _mirror(tape, macro, view):
    """Price negation: highs <-> lows, top <-> bottom.  Applied to the INPUTS
    of spring_overlap only (the machine's warm-up is not mirror-symmetric, so
    the machine is NOT re-run)."""
    t2 = C.Tape(tape.sym, tape.lens, -tape.o, -tape.l, -tape.h, -tape.c, tape.t0, tape.ts,
                tape.atr, {})
    flip = {"top": "bottom", "bottom": "top"}
    ev = [dict(e, side=flip[e["side"]]) if e.get("side") in flip else e
          for e in macro["events"]]
    return t2, {"events": ev}, {"top": -view["bot"], "bot": -view["top"]}


def _rf4_findings(corrupt: bool) -> tuple[list[str], dict]:
    V1, tape = _record_tape()
    _, law, s20, n_dev, n_spr, n_in = V1._kinship()
    m = RC.run_machine(tape.d, tape.atr, RC.PINS)       # the v1 (single-scale) machine
    view = C.asof_view(tape, m, [])
    if corrupt:            # every bottom harden's reclaim close pushed back to its
        c = tape.c.copy()  # episode's extreme, BELOW the boundary — on a COPY; the
        opens = {}         # law must stop matching
        for e in m["events"]:
            if e["event"] == "breach-open":
                opens[(e["rid"], e["side"])] = e["i"]
            elif e["event"] == "harden" and e["side"] == "bottom":
                c[e["i"]] = tape.l[opens[(e["rid"], "bottom")]:e["i"] + 1].min()
        tape = C.Tape(tape.sym, tape.lens, tape.o, tape.h, tape.l, c, tape.t0, tape.ts,
                      tape.atr, {})
    rows = {r["side"]: r for r in C.spring_overlap(tape, m, view)}
    b = rows["bottom"]
    bad = []
    if (b["n_hardens"], b["n_law_reclaim"]) != (n_dev, law):
        bad.append(f"bottom law {b['n_law_reclaim']}/{b['n_hardens']} != the v1 suite's "
                   f"{law}/{n_dev}")
    if not corrupt:
        if (b["n_hardens_also_sweep_look"], b["n_house_shapes"],
                b["n_house_shapes_inside_episode"]) != (s20, n_spr, n_in):
            bad.append(f"bottom statistic {b['n_hardens_also_sweep_look']}/{b['n_hardens']}, "
                       f"{b['n_house_shapes_inside_episode']}/{b['n_house_shapes']} != the v1 "
                       f"suite's {s20}/{n_dev}, {n_in}/{n_spr}")
        t2, m2, v2 = _mirror(tape, m, view)
        mir = {r["side"]: r for r in C.spring_overlap(t2, m2, v2)}
        keys = ("n_hardens", "n_law_reclaim", "n_hardens_also_sweep_look",
                "n_house_shapes", "n_house_shapes_inside_episode")
        for a_, b_ in (("top", "bottom"), ("bottom", "top")):
            if any(rows[a_][k] != mir[b_][k] for k in keys):
                bad.append(f"the {a_} side is not the mirror of the {b_} side on the negated tape")
        for side in DECL_SIDES:
            if rows[side]["n_law_reclaim"] != rows[side]["n_hardens"]:
                bad.append(f"{side}: {rows[side]['n_law_reclaim']}/{rows[side]['n_hardens']} "
                           "hardens reclaim their boundary")
    return bad, {"rows": rows, "v1": (law, n_dev, s20, n_spr, n_in)}


def rf4_break():
    bad, st = _rf4_findings(corrupt=True)
    b = st["rows"]["bottom"]
    return not bad, (f"with every reclaim close pushed back below its boundary (a COPY) the "
                     f"law still matches {b['n_law_reclaim']}/{b['n_hardens']} — it does not "
                     "read the close" if not bad else
                     f"corrupted reclaim closes match {b['n_law_reclaim']}/{b['n_hardens']} — "
                     "the shape test reads the close for real")


def rf4_real():
    bad, st = _rf4_findings(corrupt=False)
    law, n_dev, s20, n_spr, n_in = st["v1"]
    sp = pd.read_parquet(CROOT / "spring_overlap.parquet")
    say("        SPRING OVERLAP, BOTH SIDES x BOTH DIRECTIONS — macro machine, as filed under "
        f"{rel(CROOT)} (look = {C.SPRING_LOOK} bars):")
    say(f"        {'asset':>14} {'lens':>4} {'kind':>10} {'SCALE':>5} {'side':>6} {'shape':>8} "
        f"{'law':>7} {'(a) also sweep look':>20} {'(b) house shapes inside an episode':>36}")
    for r in sp.itertuples():
        say(f"        {r.asset:>14} {r.lens:>4} {r.scale_kind:>10} {r.scale_mult:>5.2f} "
            f"{r.side:>6} {r.shape:>8} {r.n_law_reclaim:>3}/{r.n_hardens:<3} "
            f"{r.n_hardens_also_sweep_look:>16}/{r.n_hardens:<3} "
            f"{r.n_house_shapes_inside_episode:>30}/{r.n_house_shapes:<5}")
    whole = sorted(zip(sp["asset"], sp["lens"], sp["scale_kind"], sp["side"]))
    if any(sp[sp["side"] == s].empty for s in DECL_SIDES):
        bad.append("a side is missing from the filed table")
    if any(int(r.n_law_reclaim) != int(r.n_hardens) for r in sp.itertuples()):
        bad.append("a filed row's law count is not its harden count")
    return not bad, (
        f"on the v1 suite's OWN tape and machine the parametrised bottom side reproduces its "
        f"numbers ({law}/{n_dev} law, {s20}/{n_dev} also sweep the {C.SPRING_LOOK}-bar extreme, "
        f"{n_in}/{n_spr} house springs inside an episode) with the boundary read AS-OF at full "
        f"precision, never from the 2-dp event; the TOP side (upthrusts) is the bottom's exact "
        f"mirror on the negated tape; {len(whole)} filed rows, both sides, every harden reclaims "
        f"(definitional — the content is the close)" if not bad else "; ".join(bad[:4]))


# ═══════════════════════════════════════════════════════════ F-GRID
def _grid_findings(tables: dict, man: dict, cells_ok: bool = True) -> list[str]:
    import tierc10_panel as P
    bad = []
    com = man["commission"]
    g = tables["outcome_grid"]
    pool_names = list(com.get("pooled") or ["POOLED:ALL"])
    declared = ["|".join((a, l, c, k, e, h)) for a in list(com["assets"]) + pool_names
                for l in com["lenses"] for c in DECL_CLASSES
                for k in com["scale_kinds"] for e in DECL_ERAS for h in DECL_HORIZONS]
    w = g.assign(cell=g["asset"] + "|" + g["lens"] + "|" + g["cls"] + "|"
                 + g["scale_kind"] + "|" + g["era"] + "|" + g["horizon"])
    ok, lines = P.grid_whole(declared, w, cell_col="cell",
                             require_cols=("n", "n_events", "pins_status", "provisional",
                                           "nan_reason", "toll_bps_source", "sign_law",
                                           "anchor_law"), label="outcome_grid")
    bad += [x for x in lines if x.startswith("[BAD]")]
    if not set(com["scale_kinds"]) <= set(DECL_KINDS):
        bad.append(f"undeclared scale kind in the commission: {com['scale_kinds']}")
    stats = list(C.STAT_COLS)
    floor_n = R2_PROVISIONAL()
    for r in g.itertuples():
        vals = [getattr(r, s) for s in stats]
        key = f"{r.asset}|{r.lens}|{r.cls}|{r.scale_kind}|{r.era}|{r.horizon}"
        if r.n == 0 and (any(np.isfinite(v) for v in vals) or not r.nan_reason):
            bad.append(f"{key}: n = 0 but a statistic is finite or nan_reason is empty")
        if r.n > 0 and (not all(np.isfinite(v) for v in vals) or r.nan_reason):
            bad.append(f"{key}: n = {r.n} but a statistic is NaN or a nan_reason is given")
        if bool(r.provisional) != bool(r.n < floor_n):
            bad.append(f"{key}: provisional flag != (n < {floor_n})")
        if (r.pins_status == C.TUNED_PINS) != (r.cls in DECL_TUNED):
            bad.append(f"{key}: pins_status {r.pins_status!r}")
        if r.horizon_bars != DECL_HORIZONS.get(r.horizon):
            bad.append(f"{key}: horizon_bars {r.horizon_bars}")
        if r.era not in DECL_ERAS:
            bad.append(f"{key}: undeclared era {r.era!r}")
        if bool(r.printable) != (not (r.lens == "5m" and r.cls in DECL_RETEST
                                      and r.era != "tuning")):
            bad.append(f"{key}: the printable collar disagrees with the declared law")
        if r.n > 0 and not same(r.net, r.median_term - r.toll_atr):
            bad.append(f"{key}: NET != median - toll_atr")
        if not r.pooled and np.isfinite(r.toll_atr_all) != (r.n_events - r.n_bad_atr > 0):
            bad.append(f"{key}: toll_atr_all finite != (the class has an anchor)")
    # THE ERA SPLIT IS A PARTITION: every anchor sits in exactly one era, so the
    # COUNTS are additive (the medians are not, and are never added)
    piv = g.set_index(C.GRID_KEY).sort_index()
    for k4, S in g[g["era"] == "ALL"].groupby(
            ["asset", "lens", "cls", "scale_kind", "horizon"], sort=True):
        a, l, c, kk, h = k4
        try:
            tu = piv.loc[(a, l, c, kk, "tuning", h)]
            ho = piv.loc[(a, l, c, kk, "holdout", h)]
        except KeyError:
            bad.append(f"{a}|{l}|{c}|{kk}|{h}: an era row is missing")
            continue
        al = S.iloc[0]
        for col in ("n_events", "n", "n_censored", "n_bad_atr"):
            if int(al[col]) != int(tu[col]) + int(ho[col]):
                bad.append(f"{a}|{l}|{c}|{kk}|{h}: ALL {col} {int(al[col])} != tuning "
                           f"{int(tu[col])} + holdout {int(ho[col])}")
    # the SCALE grid, whole; one pick; the pick re-derived from the FILED densities
    sg = tables["scale_grid"]
    for (a, l), S in sg.groupby(["asset", "lens"], sort=True):
        if tuple(S["scale_mult"].round(6)) != DECL_SCALES:
            bad.append(f"scale_grid {a} {l}: cells {tuple(S['scale_mult'])} != the declared 11")
            continue
        if int(S["chosen"].sum()) != 1 or int(S["is_frozen_pin"].sum()) != 1:
            bad.append(f"scale_grid {a} {l}: {int(S['chosen'].sum())} chosen, "
                       f"{int(S['is_frozen_pin'].sum())} frozen")
            continue
        err = (S["density_per_100"] - 0.75).abs().round(9).to_numpy()
        sc = S["scale_mult"].to_numpy()
        best = min(range(len(sc)), key=lambda k: (err[k], abs(sc[k] - 3.0), sc[k]))
        if float(S[S["chosen"]]["scale_mult"].iloc[0]) != float(sc[best]):
            bad.append(f"scale_grid {a} {l}: chosen is not the nearest-density cell")
        cv = tables["coverage"]
        cal = cv[(cv["asset"] == a) & (cv["lens"] == l) & (cv["scale_kind"] == "calibrated")]
        if len(cal) and float(cal["scale_mult"].iloc[0]) != float(sc[best]):
            bad.append(f"coverage {a} {l}: the calibrated row does not ride the chosen SCALE")
    for name, decl in (
            ("coverage", [(a, l, k) for a in com["assets"] for l in com["lenses"]
                          for k in com["scale_kinds"]]),
            ("spring_overlap", [(a, l, k, s) for a in com["assets"] for l in com["lenses"]
                                for k in com["scale_kinds"] for s in DECL_SIDES]),
            ("hold_tally", [(a, l, k, s) for a in com["assets"] for l in com["lenses"]
                            for k in com["scale_kinds"] for s in DECL_ANCHORS])):
        t = tables[name]
        got = sorted(map(tuple, t[man["keys"][name]].to_records(index=False).tolist()))
        if got != sorted(decl):
            bad.append(f"{name}: filed keys != the declared {len(decl)} cells")
    for name, t in tables.items():
        lack = [c for c in C.COLLAR_COLUMNS + C.AS_OF_COLUMNS if c not in t.columns
                or t[c].isna().any()]
        if lack:
            bad.append(f"{name}: collar / as-of column missing or null: {lack}")
        vc = [c for c in t.columns if c in VERDICT_COLUMNS]
        if vc:
            bad.append(f"{name}: a VERDICT column on a Tier-E table: {vc}")
    if not cells_ok:
        bad.append("a per-cell table fails its key or its stamps")
    return bad


def R2_PROVISIONAL() -> int:
    import tierc5_rules as V5
    return int(V5.PROVISIONAL_MIN_N)


def _root_tables(root: Path | None = None) -> dict:
    return {n: pd.read_parquet((CROOT if root is None else root) / f"{n}.parquet")
            for n in ("outcome_grid", "coverage", "scale_grid", "spring_overlap", "hold_tally")}


def grid_break():
    man, T0 = manifest(), _root_tables()

    def with_(name, fn):
        t = {k: v.copy() for k, v in T0.items()}
        t[name] = fn(t[name])
        return _grid_findings(t, man)

    def blank_reason(g):
        k = g.index[0]
        g.loc[k, list(C.STAT_COLS)] = np.nan
        g.loc[k, "n"] = 0
        g.loc[k, "nan_reason"] = ""
        return g

    def nan_with_n(g):
        g.loc[g.index[g["n"] > 0][0], "median_term"] = np.nan
        return g

    def two_chosen(s):
        s.loc[s.index[~s["chosen"]][0], "chosen"] = True
        return s

    def wrong_pick(s):
        a, l = s["asset"].iloc[0], s["lens"].iloc[0]
        m = (s["asset"] == a) & (s["lens"] == l)
        s.loc[m, "chosen"] = (s.loc[m, "scale_mult"] == s.loc[m, "scale_mult"].max())
        return s
    return plants([
        ("MISSING CELL (one outcome row dropped)",
         lambda: with_("outcome_grid", lambda g: g.iloc[1:])),
        ("UNDECLARED CELL (a ninth class)", lambda: with_(
            "outcome_grid", lambda g: pd.concat([g, g.iloc[:1].assign(cls="retest-hold-ema55")]))),
        ("SILENT NaN (n = 0, no nan_reason)", lambda: with_("outcome_grid", blank_reason)),
        ("NaN UNDER n > 0", lambda: with_("outcome_grid", nan_with_n)),
        ("VERDICT COLUMN on a Tier-E table",
         lambda: with_("outcome_grid", lambda g: g.assign(verdict="SUPPORTED"))),
        ("COLLAR REMOVED (`gates` dropped)",
         lambda: with_("coverage", lambda t: t.drop(columns=["gates"]))),
        ("AS-OF STAMP REMOVED (`as_of_last_closed_bar` dropped)",
         lambda: with_("hold_tally", lambda t: t.drop(columns=["as_of_last_closed_bar"]))),
        ("SCALE GRID NOT WHOLE (one SCALE dropped)",
         lambda: with_("scale_grid", lambda s: s.iloc[1:])),
        ("TWO PICKS", lambda: with_("scale_grid", two_chosen)),
        ("PICK NOT THE NEAREST DENSITY", lambda: with_("scale_grid", wrong_pick)),
        ("PROVISIONAL PINS PASSED OFF AS FROZEN", lambda: with_(
            "outcome_grid", lambda g: g.assign(pins_status=C.FROZEN_PINS))),
    ])


def _recompute_grid(man: dict, root: Path | None = None) -> list[str]:
    """grid == f(FILED ledgers), re-derived with plain numpy for EVERY row —
    per asset, and pooled (pooled median over the pooled events; pooled toll =
    the max of the assets' own)."""
    bad = []
    root = CROOT if root is None else root
    g = pd.read_parquet(root / "outcome_grid.parquet").set_index(C.GRID_KEY).sort_index()
    com = man["commission"]
    pools = com.get("pools") or {"POOLED:ALL": list(com["assets"])}
    cols = ["asset", "lens", "cls", "scale_kind", "era", "bad_atr", "toll_atr_evt"] + [
        f"{x}_{h}" for h in DECL_HORIZONS for x in ("cens", "term")]
    led = pd.concat([pd.read_parquet(C.cell_dir(root, a, l) / "events.parquet", columns=cols)
                     for a in com["assets"] for l in com["lenses"]], ignore_index=True)
    # the ERA of a filed ledger row is re-derived HERE from the anchor's close,
    # not trusted: a row whose era column lies would move a median
    for name, members in [(None, list(com["assets"]))] + list(pools.items()):
        L0 = led if name is None else led[led["asset"].isin(members)]
        for era in DECL_ERAS:
            L = L0 if era == "ALL" else L0[L0["era"] == era]
            by = (["lens", "cls", "scale_kind"] if name
                  else ["asset", "lens", "cls", "scale_kind"])
            n_ev = L.groupby(by).size()
            for hn in DECL_HORIZONS:
                S = L[~L["bad_atr"] & ~L[f"cens_{hn}"]]
                G = S.groupby(by)
                n, med, tl = G.size(), G[f"term_{hn}"].median(), G["toll_atr_evt"].median()
                rows = (g.xs((era, hn), level=("era", "horizon"))
                        if name is None else None)
                keys = ([k for k in rows.index if k[0] in members] if name is None
                        else [(name,) + k for k in
                              sorted({(l, c, kk) for l in com["lenses"]
                                      for c in DECL_CLASSES for kk in com["scale_kinds"]})])
                for key in keys:
                    r = g.loc[key[:4] + (era, hn)]
                    gk = key[1:] if name else key
                    want_n = int(n.get(gk, 0))
                    want_med = float(med.get(gk, np.nan))
                    if name:
                        own = [float(g.loc[(s,) + key[1:4] + (era, hn), "toll_atr"])
                               for s in members
                               if g.loc[(s,) + key[1:4] + (era, hn), "n"] > 0]
                        want_toll = max(own) if own else np.nan
                    else:
                        want_toll = float(tl.get(gk, np.nan))
                    if int(r["n"]) != want_n or int(r["n_events"]) != int(n_ev.get(gk, 0)) \
                            or not same(r["median_term"], want_med) \
                            or not same(r["toll_atr"], want_toll):
                        bad.append(f"{'|'.join(map(str, key[:4]))}|{era}|{hn}: filed "
                                   f"n={r['n']} med={r['median_term']} toll={r['toll_atr']} "
                                   f"vs ledger n={want_n} med={want_med} toll={want_toll}")
    return bad


def grid_real():
    import tierc10_panel as P
    import rangefinder_twin as RF
    man, T0 = manifest(), _root_tables()
    cells_bad = []
    for a in man["commission"]["assets"]:
        for l in man["commission"]["lenses"]:
            cd = C.cell_dir(CROOT, a, l)
            for name, key in C.CELL_TABLES.items():
                d = pd.read_parquet(cd / f"{name}.parquet")
                if d.duplicated(subset=key).any() or any(c not in d.columns for c in C.AS_OF_COLUMNS):
                    cells_bad.append(f"{cd.name}/{name}")
    bad = _grid_findings(T0, man, cells_ok=not cells_bad) + cells_bad
    ok_k, lines = P.check_keys(CROOT, man)
    for x in lines:
        say(f"        F-KEY over the census root: {x}")
    if not ok_k:
        bad.append("F-KEY totality fails on the census root")
    bad += _recompute_grid(man)
    # the constants are the estate's OBJECTS, and the tie-break is the printed one
    pine = (ROOT / "pine" / "SS12_RangeFinder_v2.pine").read_text(encoding="utf-8")
    mm = re.search(r"scaleMult\s*=\s*input\.float\(\s*([\d.]+).*?minval\s*=\s*([\d.]+)\s*,"
                   r"\s*step\s*=\s*([\d.]+)", pine)
    if not mm or (float(mm.group(1)), float(mm.group(2)), float(mm.group(3))) != (
            C.FROZEN_SCALE, C.SCALE_GRID[0], C.SCALE_GRID[1] - C.SCALE_GRID[0]):
        bad.append("SCALE_GRID's start / step / the frozen pin are not the Pine input's")
    if tuple(C.SCALE_GRID) != DECL_SCALES or tuple(C.CLASSES) != DECL_CLASSES:
        bad.append("the engine's grid / classes are not the fixture's declared literals")
    if tuple(C.ERAS) != DECL_ERAS or C.ERA_BOUNDARY_MS != DECL_ERA_BOUNDARY_MS:
        bad.append(f"the engine's eras / boundary {C.ERA_BOUNDARY_MS} are not the "
                   f"declared {DECL_ERAS} / {DECL_ERA_BOUNDARY_MS} [R1]")
    if tuple(C.TUNE_MARGINS) != DECL_MARGINS or tuple(C.TUNE_HOLDS) != DECL_HOLDS:
        bad.append("the R1 tuning grid's margins / holds are not the ruling's")
    if C.DENSITY_TARGET_PER_100 != RF.TARGETS_Q["Q3_conf_per_100"][0]:
        bad.append("DENSITY_TARGET_PER_100 is not the twin's Q3 centre")
    if C.PROVISIONAL_MIN_N != R2_PROVISIONAL():
        bad.append("PROVISIONAL_MIN_N is not tierc5_rules'")
    far = {s: 9.0 for s in DECL_SCALES}
    for dens, want, why in (({**far, 2.5: 0.70, 3.5: 0.80}, 2.5, "equal error, equal "
                             "distance to 3.0 -> the LOWER"),
                            ({**far, 2.0: 0.70, 3.25: 0.80}, 3.25, "equal error -> "
                             "TOWARD 3.0"),
                            ({**far, 2.0: 0.74, 3.0: 0.70}, 2.0, "nearest density wins "
                             "over the frozen pin")):
        if C.pick_scale(dens) != want:
            bad.append(f"tie-break: {why}: picked {C.pick_scale(dens)}, want {want}")
    # a YOUNG tape files WHOLE: a 40-bar and a 250-bar PREFIX (no EMA300 yet, few or
    # no ranges) must still give every class its rows — NaN, each with its reason
    young = []
    for head in (40, 250):
        fr = C.compute_cell(tape_of("BTCUSDT", "1d").head(head))["frames"]
        gy = C.canon(fr["grid"], C.GRID_KEY)
        dead = gy[gy["cls"] == "retest-hold-tap200"]
        if len(gy) != (len(DECL_CLASSES) * len(DECL_KINDS) * len(DECL_ERAS)
                       * len(DECL_HORIZONS)) \
                or not (dead["n"] == 0).all() \
                or not (gy[gy["n"] == 0]["nan_reason"].str.len() > 0).all() \
                or gy[gy["n"] == 0][list(C.STAT_COLS)].notna().any().any():
            bad.append(f"a {head}-bar prefix cell does not file whole, NaN with reasons")
        for name, key in C.CELL_TABLES.items():
            C.canon(fr[name], key)                       # HALTs on a broken key
        young.append(f"{head} bars: {int((gy['n'] == 0).sum())}/{len(gy)} NaN rows")
    com = man["commission"]
    n_nan = int((T0["outcome_grid"]["n"] == 0).sum())
    return not bad, (
        f"{len(T0['outcome_grid'])} outcome rows == the declared {len(com['assets'])} asset(s) + "
        f"{com.get('pooled')} x {com['lenses']} x {len(DECL_CLASSES)} classes x "
        f"{com['scale_kinds']} x {list(DECL_ERAS)} eras x "
        f"{list(DECL_HORIZONS)} — none missing, none undeclared; the era split is a "
        f"partition on every count; {n_nan} NaN row(s), each with "
        f"its reason; every row re-derived from the FILED ledgers (n, median, toll; pooled toll "
        f"= the binding max); SCALE grid whole (11 x {len(com['assets']) * len(com['lenses'])}), "
        f"one pick each, re-derived; collar + as-of on every table, no verdict column; young "
        f"prefix cells file whole ({'; '.join(young)}); "
        f"is_the_contract_grid = {com['is_the_contract_grid']}"
        + ("" if com["is_the_contract_grid"] else
           " — THIS ROOT IS A SMOKE / PARTIAL COMMISSION, not the contract's 17 x 3")
        if not bad else f"{len(bad)} finding(s): " + "; ".join(bad[:4]))


# ═══════════════════════════════════════════════════ F-C10-TOLL (groundwork)
TOLL_NAME = re.compile(r"toll|fee", re.I)


def _nums(node, floats_only=False) -> list:
    return [c.value for c in ast.walk(node) if isinstance(c, ast.Constant)
            and isinstance(c.value, (float,) if floats_only else (int, float))
            and not isinstance(c.value, bool)]


def _tnames(t) -> list[str]:
    if isinstance(t, ast.Name):
        return [t.id]
    if isinstance(t, ast.Attribute):
        return [t.attr]
    if isinstance(t, ast.Subscript) and isinstance(t.slice, ast.Constant) \
            and isinstance(t.slice.value, str):
        return [t.slice.value]
    if isinstance(t, (ast.Tuple, ast.List)):
        return [x for e in t.elts for x in _tnames(e)]
    return []


def toll_literals(src: str) -> list[str]:
    """THE AST SCAN.  A numeric literal in a TOLL POSITION is: the value of an
    assignment, a dict entry or a keyword argument whose name says toll / fee;
    a default of such a parameter; or a float in a `return` of a function whose
    name says so.  A toll is READ (the grid, the fee object) — never typed."""
    out = []
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
            tg = node.targets if isinstance(node, ast.Assign) else [node.target]
            names = [x for t in tg for x in _tnames(t)]
            if node.value is not None and any(TOLL_NAME.search(x) for x in names) \
                    and _nums(node.value):
                out.append(f"line {node.lineno}: {names} = ... {_nums(node.value)}")
        elif isinstance(node, ast.Dict):
            for k, v in zip(node.keys, node.values):
                if isinstance(k, ast.Constant) and isinstance(k.value, str) \
                        and TOLL_NAME.search(k.value) and _nums(v):
                    out.append(f"line {v.lineno}: dict[{k.value!r}] = {_nums(v)}")
        elif isinstance(node, ast.keyword):
            if node.arg and TOLL_NAME.search(node.arg) and _nums(node.value):
                out.append(f"line {node.value.lineno}: keyword {node.arg}={_nums(node.value)}")
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            a = node.args
            pos = a.posonlyargs + a.args
            for arg, d in list(zip(pos[len(pos) - len(a.defaults):], a.defaults)) + [
                    (x, y) for x, y in zip(a.kwonlyargs, a.kw_defaults) if y is not None]:
                if TOLL_NAME.search(arg.arg) and _nums(d):
                    out.append(f"line {node.lineno}: default {arg.arg}={_nums(d)}")
            if TOLL_NAME.search(node.name):
                for sub in ast.walk(node):
                    if isinstance(sub, ast.Return) and sub.value is not None \
                            and _nums(sub.value, floats_only=True):
                        out.append(f"line {sub.lineno}: {node.name}() returns a typed "
                                   f"{_nums(sub.value, floats_only=True)}")
    return out


def _toll_rederive(asset: str, raw: dict, atr: np.ndarray, led: pd.DataFrame, cls: str,
                   kind: str, hn: str | None) -> float:
    """The quoted toll from NOTHING but raw bars, the filed anchors and the
    estate fee OBJECT: median((bps / 10 000) * close / atr) with an ATR written
    in this file."""
    L = led[(led["cls"] == cls) & (led["scale_kind"] == kind) & ~led["bad_atr"]]
    if hn is not None:
        L = L[~L[f"cens_{hn}"]]
    k = L["known_at"].to_numpy(np.int64)
    fee = json.loads((C.STAGE_D / "fee_schedule.json").read_text())
    bps = [a["round_trip_bps_used"] for a in fee["assets"] if a["stem"] == asset]
    if len(bps) != 1 or float(bps[0]) != float(R2.FEE_BPS_ROUND_TRIP) \
            or float(R2.FEE_BPS_ROUND_TRIP) != 2.0 * float(R2.FEE_BPS_SIDE):
        raise AssertionError(f"the fee objects disagree for {asset}: {bps} vs "
                             f"{R2.FEE_BPS_ROUND_TRIP}")
    if not len(k):
        return float("nan")                # no anchor: there is no toll to quote
    return float(np.median((float(bps[0]) / 10_000) * raw["c"][k] / atr[k]))


_QUOTES = {"n": 0, "halts": 0}


def _toll_findings(grid_path: Path, man: dict, only: tuple | None = None) -> list[str]:
    bad = []
    _QUOTES.update(n=0, halts=0)
    com = man["commission"]
    for a in com["assets"]:
        for l in com["lenses"]:
            if only is not None and (a, l) != only:
                continue
            raw = raw_tape(a, l)
            atr = own_atr(raw["h"], raw["l"], raw["c"], RC.ATR_LEN)
            led = pd.read_parquet(C.cell_dir(CROOT, a, l) / "events.parquet",
                                  columns=["cls", "scale_kind", "bad_atr", "known_at",
                                           "cens_H20", "cens_H100"])
            for cls in DECL_CLASSES:
                for hn in (None, "H20", "H100"):
                    want = _toll_rederive(a, raw, atr, led, cls, "frozen3.0", hn)
                    try:
                        q = C.get_toll(a, l, cls, "frozen3.0", hn, grid_path=grid_path)
                    except SystemExit as e:
                        q = None
                        why = str(e)[:80]
                    if np.isnan(want):         # no anchor -> the reader must HALT
                        _QUOTES["halts"] += 1
                        if q is not None:
                            bad.append(f"{a} {l} {cls} {hn}: a quote ({q}) with no filed anchor")
                    elif q is None:
                        bad.append(f"{a} {l} {cls} {hn}: {why}")
                    else:
                        _QUOTES["n"] += 1
                        if not same(q, want, roundings=2):   # events rounded, then the median
                            bad.append(f"{a} {l} {cls} {hn}: quoted {q} != re-derived {want:.8f}")
    return bad


def toll_break():
    man = manifest()
    src = Path(C.__file__).read_text(encoding="utf-8")
    grid = CROOT / "outcome_grid.parquet"
    a0, l0 = man["commission"]["assets"][0], man["commission"]["lenses"][0]

    def perturbed():
        with tempfile.TemporaryDirectory(prefix="tc10_census_toll_") as td:
            g = pd.read_parquet(grid)
            m = (g["asset"] == a0) & (g["lens"] == l0) & (g["cls"] == "DIE") \
                & (g["scale_kind"] == "frozen3.0")
            g.loc[m, ["toll_atr", "toll_atr_all"]] *= 2.0
            p = Path(td) / "outcome_grid.parquet"
            g.to_parquet(p, index=False)
            before = C.get_toll(a0, l0, "DIE", grid_path=grid)
            after = C.get_toll(a0, l0, "DIE", grid_path=p)
            typed = (lambda: before)()      # what a typed literal would still say
            say(f"        perturbed COPY: get_toll {before:.8f} -> {after:.8f} (the quote "
                f"MOVES with the grid; a typed {typed:.8f} would not)")
            return _toll_findings(p, man, only=(a0, l0))

    def nan_toll():
        with tempfile.TemporaryDirectory(prefix="tc10_census_toll_") as td:
            g = pd.read_parquet(grid)
            g.loc[(g["asset"] == a0) & (g["cls"] == "DIE"), ["toll_atr", "toll_atr_all"]] = np.nan
            p = Path(td) / "outcome_grid.parquet"
            g.to_parquet(p, index=False)
            try:
                v = C.get_toll(a0, l0, "DIE", grid_path=p)
            except SystemExit as e:
                return [f"HALT, no default handed back: {str(e)[:70]}"]
            return [] if np.isfinite(v) else [f"returned {v}"]

    def planted(text, anchor="\ndef get_toll("):
        assert anchor in src
        return toll_literals(src.replace(anchor, text + anchor, 1))
    return plants([
        ("PERTURBED GRID (a COPY's toll doubled: the quote must leave the re-derived truth)",
         perturbed),
        ("NaN TOLL (a class with no event must HALT the reader, not default)", nan_toll),
        ("TYPED ASSIGNMENT", lambda: planted("\ntoll_atr_5m = 0.27\n")),
        ("TYPED DICT ENTRY", lambda: planted("\n_ROW = {'toll_atr': 0.27, 'n': 3}\n")),
        ("TYPED KEYWORD", lambda: planted("\n_X = dict(toll_bps=10.0)\n")),
        ("TYPED DEFAULT", lambda: planted("\ndef _score(book, fee_bps=10.0):\n    return book\n")),
        ("TYPED RETURN", lambda: planted("\ndef measured_toll():\n    return 0.2670\n")),
    ])


def toll_real():
    man = manifest()
    grid = CROOT / "outcome_grid.parquet"
    bad = _toll_findings(grid, man)
    lit = toll_literals(Path(C.__file__).read_text(encoding="utf-8"))
    bad += [f"numeric literal in a toll position: {x}" for x in lit]
    a0 = man["commission"]["assets"][0]
    for l in man["commission"]["lenses"]:
        say(f"        get_toll({a0}, {l}, 'DIE') = {C.get_toll(a0, l, 'DIE', grid_path=grid):.8f} "
            f"ATR · 'flip-hold' = {C.get_toll(a0, l, 'flip-hold', grid_path=grid):.8f} ATR "
            f"[frozen3.0, era ALL, all anchors] — READ from {rel(grid)}")
    # THE MEASURED 5m TOLL, PER ASSET, FOR THE DIE CLASS — READ, never typed.
    # P-BRK-S1 is struck NET OF THIS NUMBER and it is quoted from here alone.
    if "5m" in man["commission"]["lenses"]:
        say("        THE MEASURED 5m TOLL [F-C10-TOLL] — per asset, DIE class, frozen3.0, "
            "era ALL, ALL anchors, READ from the filed grid (never typed):")
        for a in man["commission"]["assets"]:
            try:
                t_all = C.get_toll(a, "5m", "DIE", grid_path=grid)
                t20 = C.get_toll(a, "5m", "DIE", horizon="H20", grid_path=grid)
                t100 = C.get_toll(a, "5m", "DIE", horizon="H100", grid_path=grid)
                say(f"          {a:>16} 5m DIE toll = {t_all:.8f} ATR  "
                    f"(H20 row {t20:.8f} · H100 row {t100:.8f})")
            except SystemExit as e:
                say(f"          {a:>16} 5m DIE toll: HALT — {str(e)[:110]}")
    n, halts = _QUOTES["n"], _QUOTES["halts"]
    return not bad, (
        f"all {n} quotes (asset x lens x class x {{all anchors, H20, H100}}; {halts} more have "
        f"no anchor and HALT the reader) returned by "
        f"get_toll equal the toll re-derived from raw bars + the filed anchors + the fee OBJECT "
        f"(fee_schedule.json == tierc2_rules.FEE_BPS_ROUND_TRIP == 2 x FEE_BPS_SIDE) with an ATR "
        f"written in this file; the AST scan finds no numeric literal in a toll position in "
        f"scripts/tierc10_census.py. GROUNDWORK: the P-BRK-S1 lane does not exist yet — its "
        f"module joins this scan when it does" if not bad else
        f"{len(bad)} finding(s): " + "; ".join(bad[:4]))


# ═════════════════════════════════════════════════════════ F-CEN-TAPE
def _tape_findings(tape: C.Tape, raw: dict) -> list[str]:
    bad = []
    if int(tape.t0[-1]) + tape.step > raw["close_ms"]:
        bad.append(f"last bar closes {C.iso(int(tape.t0[-1]) + tape.step)} AFTER the AS_OF "
                   f"{C.iso(raw['close_ms'])}")
    if len(tape.t0) != len(raw["t0"]) or not all(
            np.array_equal(getattr(tape, k), raw[k]) for k in ("t0", "o", "h", "l", "c")):
        bad.append("the tape is not the fixture's own read of the snapshot")
    else:
        a = own_atr(raw["h"], raw["l"], raw["c"], RC.ATR_LEN)
        if not np.allclose(tape.atr, a, rtol=1e-12, atol=0.0):
            bad.append("the ATR handed to the port is not Wilder's seeded at TR[0]")
    return bad


def tape_break():
    def uncut():
        f = pd.read_parquet(cache_dir() / "klines" / "BTCUSDT_5m.parquet").sort_values("open_time")
        f = f.tail(5_000)
        t = C.Tape("BTCUSDT", "5m", f["open"].to_numpy(float), f["high"].to_numpy(float),
                   f["low"].to_numpy(float), f["close"].to_numpy(float),
                   f["open_time"].to_numpy(np.int64), [], np.ones(len(f)), {})
        raw = raw_tape("BTCUSDT", "5m")
        return _tape_findings(t, {k: (v[-5000:] if k != "close_ms" else v)
                                  for k, v in raw.items()})

    def sma_atr():
        from analytics import volatility as AV
        t = tape_of("BTCUSDT", "1d")
        try:
            RC.run_machine(t.d, AV.atr(t.h, t.l, t.c, RC.ATR_LEN), RC.PINS)
        except ValueError as e:
            return [f"the port REFUSES it: {str(e)[:60]}"]
        return []

    def tail_atr():
        t = tape_of("BTCUSDT", "4h")
        tail = C.ind.atr(t.h[-1700:], t.l[-1700:], t.c[-1700:], RC.ATR_LEN)
        return ([] if np.array_equal(tail, t.atr[-1700:]) else
                [f"a tail's ATR differs from the full tape's on {int((tail != t.atr[-1700:]).sum())} "
                 "of 1700 bars — a chunk is a different machine"])
    return plants([
        ("UNCUT FILE (the snapshot's 5m rows past the AS_OF read as closed bars)", uncut),
        ("SMA-SEEDED ATR (analytics.volatility.atr, NaN warm-up) handed to the port", sma_atr),
        ("CHUNKED TAPE (a tail's re-warmed ATR passed off as the full tape's)", tail_atr),
    ])


def tape_real():
    bad = []
    for sym, lens in (("BTCUSDT", "4h"), ("BTCUSDT", "1d"), ("ETHUSDT", "1d"), ("BTCUSDT", "5m")):
        t, raw = tape_of(sym, lens), raw_tape(sym, lens)
        bad += [f"{sym} {lens}: {x}" for x in _tape_findings(t, raw)]
        say(f"        {sym} {lens}: {t.n:,} closed bars {t.meta['first_bar_open']} -> "
            f"{t.meta['last_bar_close']} · gaps {t.meta['gap_count']} · source "
            f"{t.meta['source_file']} sha256 {t.meta['source_sha256'][:16]}… · as_of_lens {lens}")
        cut = t.n // 2
        p = t.head(cut)
        if not np.array_equal(p.atr, C.ind.atr(t.h[:cut], t.l[:cut], t.c[:cut], RC.ATR_LEN)):
            bad.append(f"{sym} {lens}: a PREFIX's ATR is not the full tape's — head() is not as-of")
    # asof_index / stamps_at: a Stage-A instant reads the last bar CLOSED at or before it
    rng = np.random.default_rng(SEED)
    n_inst = 0
    for sym, lens in (("BTCUSDT", "4h"), ("BTCUSDT", "1d")):
        t = tape_of(sym, lens)
        v2 = C.run_scale(t, C.FROZEN_SCALE)
        view = C.asof_view(t, v2["macro"], v2["leash"])
        inst = np.concatenate([rng.integers(int(t.t0[0]) - t.step, int(t.t0[-1]) + 3 * t.step,
                                            size=400), t.t0[:50] + t.step, t.t0[:50] + t.step - 1])
        idx = C.asof_index(t, inst)
        n_inst += len(inst)
        for q, j in zip(inst.tolist(), idx.tolist()):
            want = max([b for b in range(max(0, j - 2), min(t.n, j + 3))
                        if int(t.t0[b]) + t.step <= q], default=-1)
            rec = C.stamps_at(t, view, j)
            if j != want or (j >= 0 and rec["rf_bar_close_ms"] > q) or (
                    j >= 0 and not rec["rf_in_range"] and rec["rf_pct_of_range"] is not None):
                bad.append(f"{sym} {lens}: instant {q} reads bar {j}, want {want}")
                break
    f4 = pd.read_parquet(cache_dir() / "klines" / "BTCUSDT_4h.parquet").sort_values("open_time")
    f4 = f4[f4["open_time"] + C.LENS_MS["4h"] <= raw_tape("BTCUSDT", "4h")["close_ms"]]
    e = E.tape_from_klines(f4, len(f4))
    t = tape_of("BTCUSDT", "4h")
    if e["ts"].tolist() != t.ts or not all(
            np.array_equal(e[k].to_numpy(float), getattr(t, k)) for k in ("o", "h", "l", "c")):
        bad.append("BTCUSDT 4h: not the engine's tape_from_klines")
    sd = pd.read_parquet(cache_dir() / "klines" / "BTCUSDT_1d.parquet").sort_values("open_time")
    d1 = tape_of("BTCUSDT", "1d")
    if not np.array_equal(sd["open_time"].to_numpy(np.int64)[:d1.n], d1.t0) or len(sd) != d1.n:
        bad.append("BTCUSDT 1d: not Stage D's derived file")
    return not bad, (
        "every tape equals the fixture's own read of the snapshot cut at the Stage D AS_OF "
        "(1d = six native-4h bars per UTC day, equal to the RF suite's tape_1d AND to Stage "
        "D's derived file); the 4h tape is the engine's tape_from_klines; the ATR equals "
        "Wilder's seeded at TR[0] written here; a prefix's ATR is bit-equal to the full tape's; "
        f"asof_index hands a Stage-A instant the last bar CLOSED at or before it ({n_inst} "
        "instants, bar closes and the ms before them included), never a forming bar"
        if not bad else "; ".join(bad[:4]))


# ══════════════════════════════════════════════════════ F-CEN-OUTCOME
def _outcome_findings(led: pd.DataFrame, raw: dict, atr: np.ndarray, rng, shorten=False):
    bad, n_chk, n_cens = [], 0, 0
    n = len(raw["c"])
    cens_any = led[[f"cens_{h}" for h in DECL_HORIZONS]].any(axis=1)
    take = sorted(set(led.index[cens_any].tolist())
                  | set(rng.choice(led.index.to_numpy(), size=min(60, len(led)),
                                   replace=False).tolist()))
    fee = float(R2.FEE_BPS_ROUND_TRIP)
    for ix in take:
        r = led.loc[ix]
        k, sg = int(r["known_at"]), float(r["sgn"])
        if not same(r["toll_atr_evt"], (fee / 10_000) * raw["c"][k] / atr[k]):
            bad.append(f"{r['cls']} k={k}: toll_atr_evt")
        if int(r["known_close_ms"]) != int(raw["t0"][k]) + C.LENS_MS[r["lens"]]:
            bad.append(f"{r['cls']} k={k}: known_close_ms is not the CLOSE of the known_at bar")
        for hn, H in DECL_HORIZONS.items():
            n_chk += 1
            if k + H > n - 1 and not shorten:
                n_cens += 1
                if not (bool(r[f"cens_{hn}"]) and np.isnan(r[f"term_{hn}"])):
                    bad.append(f"{r['cls']} k={k} {hn}: k + H > n - 1 but NOT censored")
                continue
            end = min(k + H, n - 1)
            if end <= k:                               # nothing after the anchor to walk
                continue
            hi = lo = None
            for j in range(k + 1, end + 1):            # a plain walk, bar by bar
                hi = raw["h"][j] if hi is None else max(hi, raw["h"][j])
                lo = raw["l"][j] if lo is None else min(lo, raw["l"][j])
            term = sg * (raw["c"][end] - raw["c"][k]) / atr[k]
            mfe = ((hi - raw["c"][k]) if sg > 0 else (raw["c"][k] - lo)) / atr[k]
            mae = ((raw["c"][k] - lo) if sg > 0 else (hi - raw["c"][k])) / atr[k]
            if not (same(r[f"term_{hn}"], term) and same(r[f"mfe_{hn}"], mfe)
                    and same(r[f"mae_{hn}"], mae)):
                bad.append(f"{r['cls']} k={k} {hn}: filed ({r[f'term_{hn}']}, {r[f'mfe_{hn}']}, "
                           f"{r[f'mae_{hn}']}) vs walked ({term:.8f}, {mfe:.8f}, {mae:.8f})")
    return bad, n_chk, n_cens


def _outcome_run(shorten: bool):
    man = manifest()
    rng = np.random.default_rng(SEED)
    bad, n_chk, n_cens, n_rows = [], 0, 0, 0
    for a in man["commission"]["assets"][:2]:
        for l in man["commission"]["lenses"]:
            raw = raw_tape(a, l)
            atr = own_atr(raw["h"], raw["l"], raw["c"], RC.ATR_LEN)
            led = pd.read_parquet(C.cell_dir(CROOT, a, l) / "events.parquet")
            b, c1, c2 = _outcome_findings(led, raw, atr, rng, shorten)
            bad += [f"{a} {l}: {x}" for x in b]
            n_chk, n_cens, n_rows = n_chk + c1, n_cens + c2, n_rows + len(led)
            k = led["known_at"].to_numpy()
            for hn, H in DECL_HORIZONS.items():            # the censor law, EVERY row
                if not np.array_equal(led[f"cens_{hn}"].to_numpy(bool) & ~led["bad_atr"].to_numpy(bool),
                                      (k + H > len(raw["c"]) - 1) & ~led["bad_atr"].to_numpy(bool)):
                    bad.append(f"{a} {l} {hn}: cens flag != (known_at + H > n - 1) on some row")
    return bad, n_chk, n_cens, n_rows


def outcome_break():
    bad, n_chk, n_cens, _ = _outcome_run(shorten=True)
    return not bad, (
        "a walker that SHORTENS the horizon at the tape end agrees with the ledger — the "
        "censor law is not being checked" if not bad else
        f"the SHORTEN law (end = min(k + H, n - 1), census-2A's) disagrees with the filed "
        f"ledger on {len(bad)} horizon(s) — it would have printed a number where the ledger "
        f"says CENSORED")


def outcome_real():
    bad, n_chk, n_cens, n_rows = _outcome_run(shorten=False)
    # an all-censored class and an empty class get their rows, NaN, with the reason
    t = tape_of("BTCUSDT", "1d")
    v2 = C.run_scale(t, 3.0)
    view = C.asof_view(t, v2["macro"], v2["leash"])
    ev = pd.DataFrame({"cls": ["DIE"], "i": [t.n - 5], "known_at": [t.n - 5], "rid": [1],
                       "side": ["top"], "sgn": [1]})
    led = C.outcome_ledger(t, ev, view, float(R2.FEE_BPS_ROUND_TRIP))
    rows = pd.DataFrame(C.grid_rows(led, "X", "1d", "frozen3.0", 3.0, 0, "fixture"))
    # the ERA of that one event, re-derived here from its anchor's close: the
    # all-censored story belongs to ITS era and to ALL; the other era is EMPTY
    want_era = ("tuning" if 0 <= int(led["known_close_ms"].iloc[0]) <= DECL_ERA_BOUNDARY_MS
                else "holdout")
    other = "holdout" if want_era == "tuning" else "tuning"
    if str(led["era"].iloc[0]) != want_era:
        bad.append(f"the ledger's era {led['era'].iloc[0]!r} != the re-derived {want_era!r}")
    die = rows[(rows["cls"] == "DIE") & (rows["era"].isin(("ALL", want_era)))]
    empty = rows[(rows["cls"] == "DIE") & (rows["era"] == other)]
    brk = rows[rows["cls"] == "breach"]
    if not ((die["n"] == 0).all() and die["nan_reason"].str.contains("censored").all()
            and die["median_term"].isna().all()):
        bad.append("an all-censored class does not file NaN + 'censored'")
    if not ((brk["n"] == 0).all() and brk["nan_reason"].str.contains("no event").all()):
        bad.append("an empty class does not file NaN + 'no event'")
    if not (int(empty["n_events"].sum()) == 0
            and empty["nan_reason"].str.contains("no event").all()):
        bad.append(f"an event stamped {want_era} shows under {other}, or that era's rows "
                   "do not file NaN + 'no event'")
    if len(rows) != len(DECL_CLASSES) * len(DECL_ERAS) * len(DECL_HORIZONS):
        bad.append("grid_rows is not whole on a one-event ledger")
    return not bad, (
        f"{n_chk} event-horizons re-walked bar by bar on the raw parquet with an ATR written "
        f"here (every censored row + a seeded sample of {n_rows:,} ledger rows): term, MFE, MAE, "
        f"toll and the known_at bar's CLOSE stamp all equal; {n_cens} horizons with k + H > "
        f"n - 1 are CENSORED, none shortened; the censor flag equals (known_at + H > n - 1) on "
        f"EVERY row; an all-censored and an empty class file whole, NaN, with their reason, "
        f"in the anchor's OWN era and in ALL, while the other era files 'no event'"
        if not bad else f"{len(bad)} finding(s): " + "; ".join(bad[:3]))


# ═════════════════════════════════════════════════════════ F-CEN-HOLD
def _own_retest(raw, atr, dies, lo, hi, margin, H, ttl):
    """The detector's law, walked bar by bar with plain Python."""
    n, out = len(raw["c"]), []
    for q, (d_i, rid, side) in enumerate(dies):
        nxt = dies[q + 1][0] if q + 1 < len(dies) else n
        j, hit = d_i + 1, None
        while j <= d_i + ttl and j <= nxt - 1 and j <= n - 1:
            if all(np.isfinite(x) for x in (lo[j], hi[j], lo[j - 1], hi[j - 1])):
                touch = raw["l"][j] <= hi[j] and raw["h"][j] >= lo[j]
                came = (raw["c"][j - 1] > hi[j - 1]) if side == "top" else (raw["c"][j - 1] < lo[j - 1])
                if touch and came:
                    hit = j
                    break
            j += 1
        if hit is None:
            continue
        if hit + H >= n:
            verdict = "truncated"
        else:
            verdict = "hold"
            for k in range(hit, hit + H + 1):
                if (side == "top" and raw["c"][k] < lo[k] - margin * atr[k]) or (
                        side == "bottom" and raw["c"][k] > hi[k] + margin * atr[k]):
                    verdict = "failed"
                    break
        out.append((int(rid), side, int(d_i), hit, hit + H, verdict))
    return out


def _own_bands(c):
    """THE FIVE R1 BANDS, written out HERE from this file's own EMA — the
    ribbons by name, the taps by name, the warm-up NaN and never imputed."""
    e = {p: own_ema(c, p) for p in (89, 127, 200)}
    for p, v in e.items():
        v[:p] = np.nan
    out = {f"tap{p}": (e[p], e[p].copy()) for p in (89, 127, 200)}
    for a, b in ((89, 127), (127, 200)):
        lo, hi = np.minimum(e[a], e[b]), np.maximum(e[a], e[b])
        lo[:max(a, b)], hi[:max(a, b)] = np.nan, np.nan
        out[f"ribbon{a}_{b}"] = (lo, hi)
    return out


HOLD_CELLS = (("BTCUSDT", "4h"), ("BTCUSDT", "1d"), ("ETHUSDT", "4h"))


def _hold_findings() -> tuple[list[str], dict]:
    bad = []
    st = {"dies": 0, "evaluated": 0, "holds": 0, "failed": 0, "flips": 0, "flip_fail": 0,
          "lines": []}
    # the MEMORY LINE keeps the frozen flip-hold pins; the RETEST bands ride the
    # R1-TUNED pins the census resolved (read from the module, checked against the
    # filed TUNING_RESULT.json in F-C10-TUNE)
    margin, H, ttl = (RC.PINS_V2["FLIP_HOLD_MARGIN"], RC.PINS_V2["FLIP_HOLD_BARS"],
                      RC.PINS_V2["MEM_TTL_BARS"])
    r_margin = float(C.RETEST_PINS["margin_atr"])
    r_H = int(C.RETEST_PINS["hold_bars"])
    r_ttl = int(C.RETEST_PINS["ttl_bars"])
    st["retest_pins"] = f"margin {r_margin:g} ATR / {r_H} bars / ttl {r_ttl}"
    for sym, lens in HOLD_CELLS:
        t, raw = tape_of(sym, lens), raw_tape(sym, lens)
        atr = own_atr(raw["h"], raw["l"], raw["c"], RC.ATR_LEN)
        own_b = _own_bands(raw["c"])
        for scale in ASOF_SCALES:
            v2 = C.run_scale(t, scale)
            macro, leash = v2["macro"], v2["leash"]
            dies = [(e["i"], e["rid"], e["side"]) for e in macro["events"]
                    if e["event"] == "breakout-die"]
            st["dies"] += len(dies)
            for name, band in C.RETEST_BANDS:
                lo, hi = band(t.c)
                got = [(g["rid"], g["side"], g["die_i"], g["touch_i"], g["known_at"], g["verdict"])
                       for g in C.retest_holds(t, dies, lo, hi, r_margin, r_H, r_ttl)]
                want = _own_retest(raw, atr, dies, *own_b[name], r_margin, r_H, r_ttl)
                st["evaluated"] += len(want)
                st["holds"] += sum(1 for w in want if w[5] == "hold")
                st["failed"] += sum(1 for w in want if w[5] == "failed")
                if got != want:
                    bad.append(f"{sym} {lens} @{scale:g} {name}: detector {len(got)} rows != "
                               f"plain walk {len(want)} rows")
                if scale == 3.0:
                    for w in [x for x in want if x[5] == "hold"][:3]:
                        worst = min(((raw["c"][k] - own_b[name][0][k]) if w[1] == "top"
                                     else (own_b[name][1][k] - raw["c"][k])) / atr[k]
                                    for k in range(w[3], w[4] + 1))
                        st["lines"].append(
                            f"{sym} {lens} {name}: {w[1]}-DIE {C.iso(raw['t0'][w[2]])} -> touch "
                            f"{C.iso(raw['t0'][w[3]])} -> HOLD known at the close of "
                            f"{C.iso(raw['t0'][w[4]])} (worst close {worst:+.2f} ATR vs the far "
                            f"edge; fails below {-r_margin:+.2f})")
            # the memory line: every flip re-verified on raw bars, at touch + HOLD
            px = {(r.rid, s): (r.top if s == "top" else r.bottom) for r in macro["ranges"]
                  for s in ("top", "bottom")}
            for e in leash:
                verdict = e.get("verdict", "")
                if e["event"] != "flip" and not verdict.startswith("failed through"):
                    continue
                i, p, side = e["i"], px[(e["rid"], e["side"])], e["side"]
                through = any((raw["c"][k] < p - margin * atr[k]) if side == "top"
                              else (raw["c"][k] > p + margin * atr[k]) for k in range(i, i + H + 1))
                st["flips" if e["event"] == "flip" else "flip_fail"] += 1
                if through == (e["event"] == "flip"):
                    bad.append(f"{sym} {lens} @{scale:g}: leash {e['event']} at {i} disagrees "
                               "with the raw-bar hold walk")
    for a in manifest()["commission"]["assets"]:
        for l in manifest()["commission"]["lenses"]:
            led = pd.read_parquet(C.cell_dir(CROOT, a, l) / "events.parquet",
                                  columns=["cls", "i", "known_at"])
            fh = led[led["cls"] == "flip-hold"]
            if not ((fh["known_at"] - fh["i"]) == H).all():
                bad.append(f"{a} {l}: a filed flip-hold is not anchored at touch + {H}")
            rh = led[led["cls"].isin(DECL_RETEST)]
            if not ((rh["known_at"] - rh["i"]) == r_H).all():
                bad.append(f"{a} {l}: a filed retest-hold is not anchored at touch + {r_H}")
    return bad, st


def hold_break():
    """A FAILED HOLD MUST FAIL.  On a COPY of the tape, one close inside a real
    hold window is driven three ATR through the far edge: the detector (band
    anchor) and the leash (memory-line anchor) must both withdraw the hold."""
    t = tape_of("BTCUSDT", "4h")
    margin, H, ttl = (RC.PINS_V2["FLIP_HOLD_MARGIN"], RC.PINS_V2["FLIP_HOLD_BARS"],
                      RC.PINS_V2["MEM_TTL_BARS"])
    v2 = C.run_scale(t, 3.0)
    macro = v2["macro"]
    dies = [(e["i"], e["rid"], e["side"]) for e in macro["events"] if e["event"] == "breakout-die"]

    def corrupt(k, level, side):
        c, l, h = t.c.copy(), t.l.copy(), t.h.copy()
        c[k] = level - 3.0 * t.atr[k] if side == "top" else level + 3.0 * t.atr[k]
        l[k], h[k] = min(l[k], c[k]), max(h[k], c[k])
        return C.Tape(t.sym, t.lens, t.o, h, l, c, t.t0, t.ts, C.ind.atr(h, l, c, RC.ATR_LEN), {})

    def band_plant(name, band):
        rm, rh, rt = (float(C.RETEST_PINS["margin_atr"]), int(C.RETEST_PINS["hold_bars"]),
                      int(C.RETEST_PINS["ttl_bars"]))
        lo, hi = band(t.c)
        rows = [g for g in C.retest_holds(t, dies, lo, hi, rm, rh, rt) if g["verdict"] == "hold"]
        g = rows[0]
        k = g["touch_i"] + min(3, rh)
        t2 = corrupt(k, lo[k] if g["side"] == "top" else hi[k], g["side"])
        lo2, hi2 = band(t2.c)
        after = [x for x in C.retest_holds(t2, dies, lo2, hi2, rm, rh, rt)
                 if x["rid"] == g["rid"]]
        return ([f"rid {g['rid']} touch {g['touch_i']}: hold -> {after[0]['verdict']}"]
                if after and after[0]["verdict"] != "hold" else [])

    def line_plant():
        f = [e for e in v2["leash"] if e["event"] == "flip"][0]
        r = [x for x in macro["ranges"] if x.rid == f["rid"]][0]
        k = f["i"] + 3
        t2 = corrupt(k, r.top if f["side"] == "top" else r.bottom, f["side"])
        le = RC.flips_and_leash(macro, t2.d, t2.atr, RC.PINS_V2, retests=False)
        still = [e for e in le if e["event"] == "flip" and (e["rid"], e["side"]) == (f["rid"], f["side"])]
        return [] if still else [f"rid {f['rid']} {f['side']} line: the flip at {f['i']} is withdrawn"]
    return plants([(f"FAILED HOLD on the {b.label} (a close 3 ATR through the far edge, bar "
                    f"inside the hold window)", (lambda n_=n_, b=b: band_plant(n_, b)))
                   for n_, b in C.RETEST_BANDS]
                  + [("FAILED HOLD on the memory line (same plant, the leash's flip)", line_plant)])


def hold_real():
    bad, st = _hold_findings()
    for x in st["lines"]:
        say(f"        [{C.TUNED_PINS}] {x}")
    return not bad, (
        f"[memory line: the FROZEN flip-hold pins {RC.PINS_V2['FLIP_HOLD_MARGIN']} ATR / "
        f"{RC.PINS_V2['FLIP_HOLD_BARS']} bars / ttl {RC.PINS_V2['MEM_TTL_BARS']}; the five R1 "
        f"bands: the R1-TUNED {st['retest_pins']}] the detector equals a plain bar-by-bar walk "
        f"(own EMA, own ATR) for EVERY one of {st['dies']} macro DIEs x "
        f"{len(C.RETEST_BANDS)} R1 bands ({', '.join(n for n, _ in C.RETEST_BANDS)}) over "
        f"{list(HOLD_CELLS)} x SCALE {list(ASOF_SCALES)}: {st['evaluated']} evaluations, "
        f"{st['holds']} holds, {st['failed']} failed; all {st['flips']} leash flips hold and "
        f"all {st['flip_fail']} 'failed through' fail on the raw bars at touch..touch + HOLD; "
        f"every FILED flip-hold is anchored at touch + {RC.PINS_V2['FLIP_HOLD_BARS']} and every "
        f"FILED retest-hold at touch + {int(C.RETEST_PINS['hold_bars'])}. GROUNDWORK for "
        f"F-C10-HOLD (per-lens hand-walks ride the registered lanes)" if not bad else
        f"{len(bad)} finding(s): " + "; ".join(bad[:3]))


# ══════════════════════════════════════════════════════════════ F-DET
DET_CELL = ("BTCUSDT", "1d")
DET_ASSETS = ("BTCUSDT", "ETHUSDT")     # two, so the POOLED rows pool something
_DET: dict = {}


def _build(root: Path, hash_seed: str) -> str:
    env = dict(os.environ, PYTHONHASHSEED=hash_seed, PYTHONDONTWRITEBYTECODE="1")
    r = subprocess.run([PY, str(ROOT / "scripts" / "tierc10_census.py"), "--assets",
                        ",".join(DET_ASSETS), "--lenses", DET_CELL[1], "--out", str(root)],
                       capture_output=True, text=True, env=env, timeout=3600, cwd=str(ROOT))
    if r.returncode != 0:
        raise RuntimeError(f"census subprocess failed: {r.stdout[-400:]} {r.stderr[-400:]}")
    return r.stdout


def _det_findings(a: Path, b: Path) -> list[str]:
    bad = []
    fa = sorted(p.relative_to(a).as_posix() for p in a.rglob("*") if p.is_file())
    fb = sorted(p.relative_to(b).as_posix() for p in b.rglob("*") if p.is_file())
    if fa != fb:
        return [f"different file sets: {sorted(set(fa) ^ set(fb))[:4]}"]
    for rel in fa:
        if (a / rel).read_bytes() != (b / rel).read_bytes():
            bad.append(f"bytes differ: {rel}")
        if rel.endswith(".parquet") and C.content_sha(pd.read_parquet(a / rel)) != \
                C.content_sha(pd.read_parquet(b / rel)):
            bad.append(f"content sha differs: {rel}")
    ma = json.loads((a / "build_manifest.json").read_text())
    for name, s in ma["sha"].items():
        if C.content_sha(pd.read_parquet(a / f"{name}.parquet")) != s:
            bad.append(f"the manifest's sha for {name} is not the table's")
    return bad


CLOCK_FIELD = re.compile(r'"[^"]*(elapsed|wall_clock|perf_counter|_at_run|run_started)[^"]*"\s*:')


def _clock_hits(root: Path) -> list[str]:
    return [f"{p.relative_to(root).as_posix()}: {CLOCK_FIELD.search(p.read_text()).group(0)}"
            for p in sorted(root.rglob("*.json")) if CLOCK_FIELD.search(p.read_text())]


def det_runs() -> dict:
    if _DET:
        return _DET
    td = Path(tempfile.mkdtemp(prefix="tc10_census_fdet_"))
    a, b = td / "run1", td / "run2"
    t0 = time.perf_counter()
    _build(a, "1")
    _build(b, "20260921")
    out3 = _build(a, "7")                          # the SAME root again: must resume
    clock(f"three subprocess builds of {DET_ASSETS} x {DET_CELL[1]}: "
          f"{time.perf_counter() - t0:.1f}s")
    _DET.update({"td": td, "a": a, "b": b, "resume_stdout": out3})
    return _DET


def det_break():
    R = det_runs()

    def moved_bytes():
        c = R["td"] / "plant1"
        shutil.copytree(R["b"], c)
        p = c / "cells" / f"{DET_CELL[0]}__{DET_CELL[1]}" / "events.parquet"
        d = pd.read_parquet(p)
        d.loc[d.index[0], "term_H20"] = d["term_H20"].iloc[0] + 1e-6
        d.to_parquet(p, index=False)
        return _det_findings(R["a"], c)

    def stale_cell():
        c = R["td"] / "plant2"
        shutil.copytree(R["b"], c)
        p = c / "cells" / f"{DET_CELL[0]}__{DET_CELL[1]}" / "grid.parquet"
        d = pd.read_parquet(p)
        d.loc[d.index[0], "median_term"] = 9.0
        d.to_parquet(p, index=False)
        ok, why = C.cell_is_current(c, *DET_CELL, C.SCALE_KINDS, C.code_sha())
        return [] if ok else [f"resume REFUSES the cell: {why}"]

    def wall_clock():
        c = R["td"] / "plant3"
        shutil.copytree(R["b"], c)
        p = c / "build_manifest.json"
        p.write_text(json.dumps(dict(json.loads(p.read_text()), elapsed_s=1.23)))
        return _clock_hits(c)
    return plants([
        ("ONE FLOAT MOVED by 1e-6 in a COPY of run 2's ledger", moved_bytes),
        ("A CELL TABLE EDITED behind its receipt (resume must not trust it)", stale_cell),
        ("A WALL-CLOCK FIELD (the artifact scan must be able to see one)", wall_clock),
    ])


def det_real():
    R = det_runs()
    try:
        bad = _det_findings(R["a"], R["b"])
        if R["resume_stdout"].count("REUSED") != len(DET_ASSETS):
            bad.append("a third build into the same root did not REUSE its current cells")
        ma = json.loads((R["a"] / "build_manifest.json").read_text())
        pooled = [f"(2-asset root) {x}" for x in
                  _grid_findings(_root_tables(R["a"]), ma) + _recompute_grid(ma, R["a"])]
        bad += pooled
        bad += [f"a wall-clock field: {x}" for x in _clock_hits(R["a"])]
        n_files = len([p for p in R["a"].rglob("*") if p.is_file()])
        filed = CROOT / "cells" / f"{DET_CELL[0]}__{DET_CELL[1]}" / "cell.json"
        if filed.exists():
            fa = json.loads(filed.read_text())["tables"]
            fb = json.loads((R["a"] / "cells" / filed.parent.name / "cell.json").read_text())["tables"]
            if {k: v["sha"] for k, v in fa.items()} != {k: v["sha"] for k, v in fb.items()}:
                bad.append(f"the FILED {filed.parent.name} cell is not what a fresh build makes")
        return not bad, (
            f"two subprocess builds of {list(DET_ASSETS)} x {DET_CELL[1]} under PYTHONHASHSEED 1 "
            f"and 20260921: the same {n_files} files, BYTE-identical (parquets, receipts, "
            f"manifest), every content sha equal and equal to the manifest's; a third build into "
            f"run 1's root REUSES both cells; its grid is WHOLE and its POOLED:ALL rows re-derive "
            f"from the two filed ledgers (pooled median, BINDING max toll); no wall-clock field "
            f"in any artifact; the {DET_CELL} cell FILED under "
            f"{rel(CROOT)} carries the same table shas as the fresh build "
            f"(grid sha {ma['sha']['outcome_grid'][:16]}…)"
            if not bad else f"{len(bad)} finding(s): " + "; ".join(bad[:4]))
    finally:
        shutil.rmtree(R["td"], ignore_errors=True)


# ═════════════════════════════════════════════════ F-C10-TUNE (the R1 protocol)
# The tuning chooses the hold pins EVERY retest-hold row in the grid is built
# with, so two things must be true of it: it cannot see a holdout-era bar, and
# its choice is the printed rule applied to the printed grid.  Both are proved
# on a CHEAP stand-in commission (three assets, the 1d lens, a low floor) that
# exercises the SAME tune() the 5m run used — never on a second implementation.
TUNE_CELLS = ("BTCUSDT", "ETHUSDT", "SOLUSDT")
TUNE_TEST_FLOOR = 5
_TUNE: dict = {}


def _cut_set(assets=TUNE_CELLS, lens="1d") -> dict:
    return {s: (lambda t: t.head(C.era_cut(t)))(tape_of(s, lens)) for s in assets}


def _blast_holdout(t: C.Tape) -> C.Tape:
    """A COPY of the tape with a HUGE planted edge in every HOLDOUT-era bar: a
    5x level shift and a monotone ramp.  A tuner that reads one holdout bar
    cannot miss this; an as-of-clean one cannot see it."""
    k = C.era_cut(t)
    o, h, l, c = t.o.copy(), t.h.copy(), t.l.copy(), t.c.copy()
    ramp = 1.0 + 0.01 * np.arange(len(c) - k)
    for arr in (o, h, l, c):
        arr[k:] = arr[k:] * 5.0 * ramp
    return C.Tape(t.sym, t.lens, o, h, l, c, t.t0, t.ts,
                  C.ind.atr(h, l, c, RC.ATR_LEN), dict(t.meta))


def _own_pick(grid: pd.DataFrame, floor_n: int) -> tuple:
    """R1's rule, written AGAIN here: the eligible cell with the highest
    objective; ties to the on-disk pins (margin 1.0, hold 6) first, then the
    simpler band (tap before ribbon, 89 before 127 before 200)."""
    order = ("tap89", "tap127", "tap200", "ribbon89_127", "ribbon127_200")
    best = None
    for r in grid.itertuples():
        if int(r.n) < int(floor_n):
            continue
        key = (-round(float(r.objective_net_h20), C.ROUND_ND),
               0 if (float(r.margin_atr) == 1.0 and int(r.hold_bars) == 6) else 1,
               order.index(str(r.band)), float(r.margin_atr), int(r.hold_bars))
        if best is None or key < best[0]:
            best = (key, (str(r.band), float(r.margin_atr), int(r.hold_bars), int(r.n)))
    return best[1] if best else (None, None, None, 0)


def tune_runs() -> dict:
    if not _TUNE:
        cut = _cut_set()
        t0 = time.perf_counter()
        g0, r0 = C.tune(cut, "1d", TUNE_TEST_FLOOR)
        blasted = {s: _blast_holdout(tape_of(s, "1d")) for s in TUNE_CELLS}
        cut2 = {s: t.head(C.era_cut(t)) for s, t in blasted.items()}
        g1, r1 = C.tune(cut2, "1d", TUNE_TEST_FLOOR)
        clock(f"two tune() runs on {list(TUNE_CELLS)} x 1d (honest + holdout-blasted): "
              f"{time.perf_counter() - t0:.1f}s")
        _TUNE.update(cut=cut, grid=g0, res=r0, blast_grid=g1, blast_res=r1,
                     blasted=blasted)
    return _TUNE


def tune_break():
    """THE GUARD MUST BITE.  (1) tune() handed an UNCUT tape must HALT — the
    door is the only door.  (2) one bar past the boundary must HALT.  (3) a
    LEAKY tuner (the same grid computed on the uncut tapes) must be MOVED by
    the holdout plant — otherwise the immunity in the real leg proves nothing.
    (4) a selector that ignores the floor must disagree with the filed pick."""
    R = tune_runs()

    def uncut():
        try:
            C.tune({s: tape_of(s, "1d") for s in TUNE_CELLS}, "1d", TUNE_TEST_FLOOR)
        except SystemExit as e:
            return [f"HALT on an uncut tape: {str(e)[:90]}"]
        return []

    def one_bar_late():
        cut = {s: tape_of(s, "1d").head(C.era_cut(tape_of(s, "1d")) + 1) for s in TUNE_CELLS}
        try:
            C.tune(cut, "1d", TUNE_TEST_FLOOR)
        except SystemExit as e:
            return [f"HALT one bar past the boundary: {str(e)[:70]}"]
        return []

    def leaky_tuner_moves():
        # what a LEAKY tuner would see: the same ledger road, run on the WHOLE
        # tape (holdout included), honest tape vs blasted copy.  Built here —
        # tune() itself cannot be asked to do this, which is the point.
        vecs = []
        for tapes in ({s_: tape_of(s_, "1d") for s_ in TUNE_CELLS}, R["blasted"]):
            row = []
            for sym, t in tapes.items():
                v2 = C.run_scale(t, 3.0)
                view = C.asof_view(t, v2["macro"], v2["leash"])
                dies = [(e["i"], e["rid"], e["side"]) for e in v2["macro"]["events"]
                        if e["event"] == "breakout-die"]
                bps, _src = C.toll_bps_for(sym)
                for bn, band in C.RETEST_BANDS:
                    led = C._tune_ledgers(t, band, 1.0, 6, 400, f"retest-hold-{bn}",
                                          dies, view, bps)
                    S = led[~led["bad_atr"] & ~led["cens_H20"]]
                    row.append((bn, len(S), round(float(S["term_H20"].median()), 6)
                                if len(S) else None))
            vecs.append(row)
        moved = [(a, b) for a, b in zip(*vecs) if a != b]
        return ([f"a whole-tape (leaky) tuner moves on {len(moved)} of {len(vecs[0])} "
                 f"(asset, band) cells, e.g. {moved[0][0]} -> {moved[0][1]}"]
                if moved else [])

    def floor_ignored():
        # a COPY of the grid carrying a BELOW-FLOOR cell with a monster objective:
        # the floor must refuse it, so the pick must not move
        g = R["grid"].copy().reset_index(drop=True)
        g.loc[0, "n"] = TUNE_TEST_FLOOR - 1
        g.loc[0, "objective_net_h20"] = 99.0
        honest = _own_pick(R["grid"], TUNE_TEST_FLOOR)
        with_floor = _own_pick(g, TUNE_TEST_FLOOR)
        no_floor = _own_pick(g, 0)
        out = []
        if with_floor[:3] != honest[:3]:
            out.append(f"the floor let the planted below-floor cell through: {with_floor[:3]}")
        elif no_floor[:3] == honest[:3]:
            out.append("VACUOUS: dropping the floor does not reach the planted cell")
        else:
            out.append(f"the floor REFUSED a below-floor cell with objective +99.0 "
                       f"({g.loc[0, 'band']}|{g.loc[0, 'margin_atr']:g}|"
                       f"{int(g.loc[0, 'hold_bars'])}, n {int(g.loc[0, 'n'])}); a selector "
                       f"without the floor takes it")
        return out
    return plants([
        ("TUNE ON AN UNCUT TAPE (the whole history handed to tune())", uncut),
        ("TUNE ONE BAR PAST THE ERA BOUNDARY", one_bar_late),
        ("A LEAKY (whole-tape) TUNER IS MOVED BY THE HOLDOUT PLANT — so the plant has "
         "teeth", leaky_tuner_moves),
        ("A BELOW-FLOOR CELL WITH A MONSTER OBJECTIVE (the floor must refuse it)",
         floor_ignored),
    ])


def tune_real():
    R = tune_runs()
    bad = []
    g, res, gb, rb = R["grid"], R["res"], R["blast_grid"], R["blast_res"]
    # 1 · the whole grid, once each
    want = {(b, m, h) for b, _ in C.RETEST_BANDS for m in DECL_MARGINS for h in DECL_HOLDS}
    got = [(str(r.band), float(r.margin_atr), int(r.hold_bars)) for r in g.itertuples()]
    if sorted(got) != sorted(want) or len(got) != len(want):
        bad.append(f"the tuning grid is not the whole {len(want)} cells, once each")
    if not (g["eligible"] == (g["n"] >= TUNE_TEST_FLOOR)).all():
        bad.append("eligible != (n >= floor)")
    if not (g[~g["eligible"]]["ineligible_reason"].str.len() > 0).all():
        bad.append("an ineligible cell carries no reason")
    if not all(same(r.objective_net_h20, r.median_term - r.toll_atr) for r in g.itertuples()):
        bad.append("the objective is not median term - toll on some cell")
    # 2 · HOLDOUT IMMUNITY: the blast moved nothing
    if C.content_sha(g) != C.content_sha(gb):
        d = g.compare(gb)
        bad.append(f"the holdout plant MOVED the tuning grid ({len(d)} differing row(s)) — "
                   "the tuning path read a holdout-era bar")
    for k in ("band", "margin_atr", "hold_bars", "n", "objective", "grid_sha"):
        if res.get(k) != rb.get(k):
            bad.append(f"the holdout plant moved the result's {k}: {res.get(k)} -> {rb.get(k)}")
    if not any(C.era_cut(t) < t.n for t in R["blasted"].values()):
        bad.append("VACUOUS: no tape has a holdout era to blast")
    # 3 · the pick is the printed rule on the printed grid
    own = _own_pick(g, TUNE_TEST_FLOOR)
    if (res["band"], res["margin_atr"], res["hold_bars"], res["n"]) != own:
        bad.append(f"the selected cell {res['band']}|{res['margin_atr']}|{res['hold_bars']} "
                   f"is not this file's own application of the tie-break ({own})")
    # 4 · the FILED 5m result is the census's pins of record
    filed = C.tuning_result("5m", CROOT if (CROOT / "TUNING_RESULT.json").exists() else C.OUT)
    if filed is None:
        bad.append("no TUNING_RESULT.json is filed — the census is riding pre-R1 pins")
    else:
        fg = pd.read_parquet((CROOT if (CROOT / "TUNING_GRID.parquet").exists() else C.OUT)
                             / "TUNING_GRID.parquet")
        if C.content_sha(fg) != filed["grid_sha"]:
            bad.append("the filed TUNING_RESULT's grid_sha is not the filed TUNING_GRID's")
        fown = _own_pick(fg, int(filed["floor_n"]))
        if (filed["band"], filed["margin_atr"], filed["hold_bars"], filed["n"]) != fown:
            bad.append(f"the FILED 5m pick is not the tie-break applied to the FILED grid "
                       f"({fown})")
        if (float(C.RETEST_PINS["margin_atr"]), int(C.RETEST_PINS["hold_bars"])) != \
                (float(filed["margin_atr"]), int(filed["hold_bars"])):
            bad.append("the census's RETEST_PINS are not the filed 5m tuning result's")
        if not all(int(t.t0[-1] + t.step) <= DECL_ERA_BOUNDARY_MS
                   for t in R["cut"].values()):
            bad.append("a cut tape reaches past the declared era boundary")
    say(f"        R1 5m pins of record: margin {C.RETEST_PINS['margin_atr']:g} ATR / "
        f"hold {C.RETEST_PINS['hold_bars']} bars / ttl {C.RETEST_PINS['ttl_bars']} "
        f"[{C.RETEST_PINS['status']}]"
        + (f" · scored band {filed['band']} · n {filed['n']:,}" if filed else ""))
    say(f"        stand-in commission {list(TUNE_CELLS)} x 1d, floor {TUNE_TEST_FLOOR}: "
        f"pick {res['band']}|{res['margin_atr']:g}|{res['hold_bars']} n {res['n']} — "
        f"IDENTICAL on the holdout-blasted copy (grid sha {res['grid_sha'][:16]})")
    return not bad, (
        f"the R1 tuning grid is whole ({len(g)} cells = {len(C.RETEST_BANDS)} bands x "
        f"{list(DECL_MARGINS)} x {list(DECL_HOLDS)}), every ineligible cell filed with its "
        f"reason, the objective = median term - toll on every cell; tune() HALTS on any tape "
        f"that reaches past {C.ERA_BOUNDARY_ISO}, and a COPY whose every HOLDOUT bar is blown "
        f"up 5x with a ramp leaves the grid content sha and the whole result BIT-IDENTICAL "
        f"while a whole-tape tuner moves; the pick is this file's own application of the "
        f"printed tie-break, on the stand-in grid AND on the FILED 5m grid, and the census's "
        f"RETEST_PINS are the filed result's"
        if not bad else f"{len(bad)} finding(s): " + "; ".join(bad[:4]))


# ═════════════════ F-C10-ACC (Q-R4) · F-C10-HT (Q-R3) — the two absent clauses
R34_CELL = ("BTCUSDT", "4h")          # a REAL cell, re-walked live by both legs


def _r34(name: str) -> pd.DataFrame:
    p = CROOT / f"{name}.parquet"
    if not p.exists():
        raise SystemExit(f"HALT: {p} is not filed — run `tierc10_census.py --r34`")
    return pd.read_parquet(p)


def _law_sha(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True).encode("utf-8")).hexdigest()


def _walk_cell(sym: str = R34_CELL[0], lens: str = R34_CELL[1], kind: str = "frozen3.0"):
    """The live machine + the live episode walk on one real cell."""
    tape = C.load_tape(sym, lens)
    rc = C._cell_receipt(CROOT, sym, lens)
    scale = (float(C.FROZEN_SCALE) if kind == "frozen3.0"
             else float(rc["calibrated_scale"]))
    m = RC.run_v2(tape.d, tape.atr, dict(RC.PINS_V2, SCALE_MULT=scale),
                  with_micro=False, retests=False)["macro"]
    w = C._r34_walk(tape, m, RC.macro_pins(scale))
    return tape, m, w, float(rc["toll_bps"])


def _replay_gap(w, m) -> list:
    truth = [(e["i"], e["rid"], e["side"], e["by"], e["closes"])
             for e in m["events"] if e["event"] == "breakout-die"]
    mine = [(e["die_i"], e["rid"], e["side"], e["die_by"], e["max_closes"])
            for e in w["episodes"] if e["end_kind"] == "die"]
    return [] if truth == mine else [f"{len(mine)} replayed vs {len(truth)} machine"]



# ── THE MARGIN / FLOOR HELPERS [review 2026-09-22, findings 1 and 2] ─────────
def _bitsame(a, b) -> bool:
    """Two filed floats are the SAME number — and two ABSENCES are the same
    absence. An empty era files NaN on both sides; a NaN facing a number is a
    disagreement, not a match [LEAN R3-f]."""
    x, y = float(a), float(b)
    return (np.isnan(x) and np.isnan(y)) or x == y


def _live_edge(sym: str, lens: str, kind: str = "frozen3.0"):
    """The RAW edge arrays of ONE real cell, re-walked live — the independent
    object every margin assertion below is judged against."""
    tape, m, w, bps = _walk_cell(sym, lens, kind)
    return C.edge_arrays(tape, w, bps, 0), tape, w


def _cellmean(e, lens, asset, kind, era, hz, *, near_only, by):
    """THE DEFECT, RECONSTRUCTED: the weighted mean of per-cell `net`s that the
    prior digest published. Kept HERE, in the fixture, as the thing the real
    leg must prove the filed margins are NOT."""
    z = e[(e["asset"] == asset) & (e["lens"] == lens) & (e["scale_kind"] == kind)
          & (e["era"] == era) & (e["horizon"] == hz)
          & (e["margin"] == C.MARGIN_CELL)]
    if near_only:
        z = z[z["is_near_boundary"]]
    g = z.groupby(by).apply(
        lambda x: float(np.average(x["net"], weights=x["n"].clip(lower=1))),
        include_groups=False)
    return g


ACC_SAMPLE_N = 6          # cells re-walked LIVE by F-C10-ACC; --slow does all of them


def _replay_sample(man: dict, n: int | None = None) -> list[str]:
    """THE SEEDED SAMPLE of (asset|lens|kind) cells F-C10-ACC re-walks live.
    Seeded from SEED so the sample is the same on every run and the leg is
    deterministic; the WHOLE list under --slow."""
    keys = sorted(man["replay_by_cell"])
    if n is None or n >= len(keys):
        return keys
    rng = np.random.default_rng(SEED)
    return [keys[i] for i in sorted(rng.choice(len(keys), size=n, replace=False))]


def _replay_live(key: str) -> dict:
    """Re-walk ONE cell and return the same five fields the build filed for it
    — computed here from the machine + the walk, never read from a manifest."""
    sym, lens, kind = key.split("|")
    tape, m, w, _ = _walk_cell(sym, lens, kind)
    truth = [(e["i"], e["rid"], e["side"], e["by"], e["closes"])
             for e in m["events"] if e["event"] == "breakout-die"]
    mine = [(e["die_i"], e["rid"], e["side"], e["die_by"], e["max_closes"])
            for e in w["episodes"] if e["end_kind"] == "die"]
    return {"die": len(truth), "episodes": len(w["episodes"]),
            "ranges": len(w["ranges"]), "in_range_bars": int(len(w["ir_t"])),
            "die_i_sha": hashlib.sha256(
                json.dumps([[int(x[0]), int(x[1]), str(x[2]), str(x[3]), int(x[4])]
                            for x in truth]).encode()).hexdigest(),
            "_gap": [] if truth == mine else
                    [f"{len(mine)} replayed vs {len(truth)} machine"]}


def acc_break():
    """SIX deliberate sabotages of the acceptance head-to-head, ONE AT A TIME."""
    a = _r34("acceptance_head_to_head")

    def definition_edited():
        keep = dict(C.ACCEPTANCE_LAW)
        try:
            C.ACCEPTANCE_LAW[C.ACC_2C] = keep[C.ACC_2C] + " (edited)"
            live = _law_sha(C.ACCEPTANCE_LAW)
            bad = sorted(set(a["acceptance_law_sha"]) - {live})
            txt = set(a[a["variant"] == C.ACC_2C]["definition"])
            return ([f"filed law sha {bad[0][:16]} is not the live {live[:16]}"] if bad
                    else []) + ([f"filed definition is not the live one"]
                                if txt != {C.ACCEPTANCE_LAW[C.ACC_2C]} else [])
        finally:
            C.ACCEPTANCE_LAW.clear()
            C.ACCEPTANCE_LAW.update(keep)

    def variant_N_edited():
        keep = dict(C.ACC_N)
        try:
            C.ACC_N[C.ACC_2C] = 4                      # "2-close" silently becomes 4
            tape, m, w, bps = _walk_cell()
            led = C.acceptance_rows(tape, w, R34_CELL[0], R34_CELL[1], "frozen3.0", bps)
            got = int(led[(led["variant"] == C.ACC_2C) & led["declared"]].shape[0])
            f = a[(a["asset"] == R34_CELL[0]) & (a["lens"] == R34_CELL[1])
                  & (a["scale_kind"] == "frozen3.0") & (a["era"] == C.ERA_ALL)
                  & (a["horizon"] == "H20") & (a["variant"] == C.ACC_2C)]
            want = int(f["n_declared"].iloc[0])
            return [f"2-close re-declares {got}, filed says {want}"] if got != want else []
        finally:
            C.ACC_N.clear()
            C.ACC_N.update(keep)

    def variant_promoted():
        keep = RC.PINS["BREAK_CONFIRM_N"]
        try:
            RC.PINS["BREAK_CONFIRM_N"] = 3             # the pins MOVE = a promotion
            live = (f"BREAK_CONFIRM_N={RC.PINS['BREAK_CONFIRM_N']} · "
                    f"BREAK_MARGIN={RC.PINS['BREAK_MARGIN']} — UNCHANGED")
            bad = sorted(set(a["engine_default_after"]) - {live})
            return [f"the engine default MOVED: filed {bad[0][:60]!r}"] if bad else []
        finally:
            RC.PINS["BREAK_CONFIRM_N"] = keep

    def replay_sabotaged():
        tape, m, w, _ = _walk_cell()
        w2 = dict(w, episodes=[e for e in w["episodes"]
                               if not (e["end_kind"] == "die" and e is w["episodes"][-1])])
        w2["episodes"] = [e for e in w["episodes"] if e["end_kind"] != "die"][:1] + \
                         [e for e in w["episodes"] if e["end_kind"] == "die"][:-1]
        return _replay_gap(w2, m) or []

    def per_cell_log_corrupted():
        """ONE CELL'S FILED REPLAY LEDGER IS CORRUPTED and the leg must find it
        by RE-WALKING, not by reading the manifest back to itself
        [review 2026-09-22, finding 3]. The plant edits a COPY of the manifest
        dict; nothing on disk is touched."""
        man = json.loads((CROOT / "R34_MANIFEST.json").read_text())
        if "replay_by_cell" not in man:
            return ["VACUOUS: the manifest files no per-cell replay ledger"]
        sample = _replay_sample(man, ACC_SAMPLE_N)
        k = sample[0]
        bad_man = json.loads(json.dumps(man))
        bad_man["replay_by_cell"][k] = dict(
            bad_man["replay_by_cell"][k],
            die=int(bad_man["replay_by_cell"][k]["die"]) + 1,
            die_i_sha="0" * 64)
        live = _replay_live(k)
        f = bad_man["replay_by_cell"][k]
        found = [f"{fld}: filed {f[fld]!r} != re-walked {live[fld]!r}"
                 for fld in ("die", "episodes", "ranges", "in_range_bars",
                             "die_i_sha")
                 if f[fld] != live[fld]]
        return found

    def grand_totals_cannot_go_red():
        """THE TAUTOLOGY, NAMED. `die_machine` and `die_matched` are
        incremented in lockstep one line after the build's own HALT has
        already forced truth == mine, so no arrangement of the data can make
        them differ. The plant tries: it drives the build's own accumulation
        with a DELIBERATELY UNEQUAL pair and shows the HALT fires first, which
        is why the equality assertion is worthless as evidence and why this
        leg no longer rests on it."""
        truth = [(1, 0, "top", "margin", 3)]
        mine = [(1, 0, "top", "margin", 4)]           # DIFFERENT, on purpose
        rep = {"die_machine": 0, "die_matched": 0}
        halted = False
        try:
            if truth != mine:
                raise SystemExit("HALT (F-C10-ACC-REPLAY): 1 vs 1 events")
            rep["die_machine"] += len(truth)
            rep["die_matched"] += len(mine)
        except SystemExit:
            halted = True
        if not halted:
            return ["the build's HALT did NOT fire on an unequal replay"]
        if rep["die_machine"] != rep["die_matched"]:
            return ["the counters diverged — they are not lockstep after all"]
        return ["`die_machine == die_matched` is TRUE BY CONSTRUCTION (the HALT "
                "fires first and the two += lines are unreachable when they "
                "would differ) — it is not evidence and is no longer asserted"]

    return plants([("an acceptance DEFINITION is edited", definition_edited),
                   ("a variant's N is edited (2-close -> 4-close)", variant_N_edited),
                   ("a variant is PROMOTED (BREAK_CONFIRM_N moved 8 -> 3)", variant_promoted),
                   ("the episode replay is sabotaged", replay_sabotaged),
                   ("ONE CELL'S FILED REPLAY LEDGER IS CORRUPTED (the sampled "
                    "re-walk must catch it)", per_cell_log_corrupted),
                   ("the manifest's GRAND TOTAL equality is asserted as evidence",
                    grand_totals_cannot_go_red)])


def acc_real():
    a = _r34("acceptance_head_to_head")
    man = json.loads((CROOT / "R34_MANIFEST.json").read_text())
    bad: list[str] = []
    com = man["commission"]
    pools = list(C.pools_for(com["assets"]))
    want = (len(com["assets"]) + len(pools)) * len(com["lenses"]) \
        * len(com["scale_kinds"]) * len(C.ACCEPTANCE_VARIANTS) * len(C.ERAS) \
        * len(C.HORIZONS)
    if len(a) != want:
        bad.append(f"grid is {len(a)} rows, the whole declared grid is {want}")
    if int(a.duplicated(subset=C.ACC_GRID_KEY).sum()):
        bad.append("the acceptance key is not unique")
    live = _law_sha(C.ACCEPTANCE_LAW)
    if set(a["acceptance_law_sha"]) != {live}:
        bad.append("a row's acceptance_law_sha is not the live law's")
    # NOTHING WAS PROMOTED: the engine's own pins are where R0 left them
    if (RC.PINS["BREAK_CONFIRM_N"], RC.PINS["BREAK_MARGIN"]) != (8, 1.5):
        bad.append(f"the engine default MOVED to {RC.PINS['BREAK_CONFIRM_N']} / "
                   f"{RC.PINS['BREAK_MARGIN']} — Q-R4 promotes NOTHING")
    if set(a["engine_default_after"]) != {
            f"BREAK_CONFIRM_N={RC.PINS['BREAK_CONFIRM_N']} · "
            f"BREAK_MARGIN={RC.PINS['BREAK_MARGIN']} — UNCHANGED"}:
        bad.append("a row does not carry the UNCHANGED engine default")
    # the time-beyond threshold is READ from the frozen pin, never typed
    if C.TIME_BEYOND_T != RC.PINS["DEV_RETURN_BARS"] or set(a["time_beyond_T"]) != {
            RC.PINS["DEV_RETURN_BARS"]}:
        bad.append("time_beyond_T is not RC.PINS['DEV_RETURN_BARS']")
    src = Path(C.__file__).read_text()
    if "TIME_BEYOND_T = RC.PINS[\"DEV_RETURN_BARS\"]" not in src:
        bad.append("TIME_BEYOND_T is no longer READ from the pin")
    # the five rules share ONE denominator, so their declare-rates compare
    g = a.groupby(["asset", "lens", "scale_kind", "era", "horizon"])["n_episodes"].nunique()
    if int((g != 1).sum()):
        bad.append(f"{int((g != 1).sum())} cell(s) give the five variants different "
                   "n_episodes — the head-to-head is not like-for-like")
    # the DIE rule declares exactly the machine's deaths, and is never 'survived'
    d = a[a["variant"] == C.ACC_DIE]
    if int((d["n_declared_survived"] != 0).sum()):
        bad.append("the DIE rule declared on an episode that did not die")
    if not (d["precision_died"].dropna() == 1.0).all():
        bad.append("the DIE rule's precision is not 1.0 by construction")
    # and the live walk still IS the machine, bar for bar
    tape, m, w, _ = _walk_cell()
    gap = _replay_gap(w, m)
    if gap:
        bad.append(f"the episode replay is not the machine's die log: {gap[0]}")
    n_die = len([e for e in w["episodes"] if e["end_kind"] == "die"])
    # THE REPLAY EVIDENCE IS RE-WALKED, NEVER READ BACK OUT OF THE ARTIFACT
    # UNDER TEST [review 2026-09-22, finding 3].  The manifest's GRAND TOTALS
    # are equal BY CONSTRUCTION (the build HALTs before the two counters can
    # diverge), so asserting their equality asserts nothing and this leg does
    # not.  What it asserts is the FILED PER-CELL LEDGER, against a live
    # re-walk of a SEEDED SAMPLE of those cells — the whole 102 under --slow.
    if "replay_by_cell" not in man:
        bad.append("the manifest files no per-cell replay ledger to verify")
        sample, walked = [], {}
    else:
        allk = sorted(man["replay_by_cell"])
        if len(allk) != int(man["replay"]["cells"]):
            bad.append(f"the per-cell ledger has {len(allk)} cells, the build "
                       f"counted {man['replay']['cells']}")
        tot_die = sum(int(x["die"]) for x in man["replay_by_cell"].values())
        tot_eps = sum(int(x["episodes"]) for x in man["replay_by_cell"].values())
        if tot_die != int(man["replay"]["die_machine"]):
            bad.append(f"the per-cell die counts sum to {tot_die:,}, the grand "
                       f"total says {int(man['replay']['die_machine']):,}")
        if tot_eps != int(man["replay"]["episodes"]):
            bad.append(f"the per-cell episode counts sum to {tot_eps:,}, the "
                       f"grand total says {int(man['replay']['episodes']):,}")
        sample = _replay_sample(man, None if ACC_SLOW else ACC_SAMPLE_N)
        walked = {}
        for k in sample:
            liv = _replay_live(k)
            walked[k] = liv
            if liv["_gap"]:
                bad.append(f"{k}: the replay is not the machine's die log "
                           f"({liv['_gap'][0]})")
            f_ = man["replay_by_cell"][k]
            for fld in ("die", "episodes", "ranges", "in_range_bars", "die_i_sha"):
                if f_[fld] != liv[fld]:
                    bad.append(f"{k}: filed {fld} {f_[fld]!r} != re-walked "
                               f"{liv[fld]!r}")
    return (not bad, "; ".join(bad) if bad else
            f"{len(a):,} rows = the whole declared grid · law sha {live[:16]} · "
            f"{len(C.ACCEPTANCE_VARIANTS)} rules, ONE denominator per cell · engine default "
            f"BREAK_CONFIRM_N={RC.PINS['BREAK_CONFIRM_N']}/BREAK_MARGIN="
            f"{RC.PINS['BREAK_MARGIN']} UNCHANGED (nothing promoted) · T="
            f"{C.TIME_BEYOND_T} READ from DEV_RETURN_BARS · RE-WALKED LIVE HERE: "
            f"{len(sample)} of {int(man['replay']['cells'])} cells "
            f"({'ALL — --slow' if ACC_SLOW else f'seeded sample, seed {SEED}'}) — "
            + "; ".join(f"{k} die {walked[k]['die']:,} eps "
                        f"{walked[k]['episodes']:,} ranges {walked[k]['ranges']:,}"
                        for k in sample)
            + f" — every one bar-for-bar the machine's own breakout-die log, and "
            f"every field equal to the FILED per-cell ledger including a sha over "
            f"the (bar, rid, side, cause, closes) tuples. THE BUILD'S GRAND TOTALS "
            f"({man['replay']['die_matched']:,}/{man['replay']['die_machine']:,} over "
            f"{man['replay']['cells']} cells, {man['replay']['episodes']:,} episodes) "
            f"ARE NOT EVIDENCE AND ARE NOT ASSERTED HERE: they are incremented after "
            f"the build's own HALT has already forced equality. What IS asserted is "
            f"that the per-cell ledger SUMS to them ({int(man['replay']['cells'])} "
            f"cells checked) and that the sampled cells re-walk true; "
            f"{R34_CELL[0]} {R34_CELL[1]} re-walked live: {n_die} deaths, bar for bar")


def ht_break():
    """FOUR deliberate sabotages of the height-vs-toll GATE, ONE AT A TIME."""
    v = _r34("height_toll_verdict")
    h = _r34("height_toll")

    def threshold_moved():
        keep = C.HEIGHT_RATIO_MIN
        try:
            C.HEIGHT_RATIO_MIN = 500.0             # the bar moves, silently
            re = ((h["ratio_median"] >= C.HEIGHT_RATIO_MIN)
                  & (h["share_ratio_lt_1"] <= C.INFEASIBLE_MAX_SHARE))
            n = int((re != h["gate_height_pass"]).sum())
            return [f"{n} filed gate verdict(s) disagree with the live threshold"] if n else []
        finally:
            C.HEIGHT_RATIO_MIN = keep

    def gate_law_sha_moved():
        keep = dict(C.HEIGHT_GATE_LAW)
        try:
            C.HEIGHT_GATE_LAW["gate_height"] = "PASS iff someone says so"
            C.HEIGHT_GATE_LAW_SHA_LIVE = _law_sha(C.HEIGHT_GATE_LAW)
            k = C.HEIGHT_GATE_LAW_SHA
            C.HEIGHT_GATE_LAW_SHA = C.HEIGHT_GATE_LAW_SHA_LIVE
            try:
                C.height_vs_toll_verdict("4h", root=CROOT)
                return []
            except SystemExit as e:
                return [f"the read HALTED: {str(e)[:90]}"]
            finally:
                C.HEIGHT_GATE_LAW_SHA = k
        finally:
            C.HEIGHT_GATE_LAW.clear()
            C.HEIGHT_GATE_LAW.update(keep)

    def read_before_filed():
        with tempfile.TemporaryDirectory() as td:
            try:
                C.height_vs_toll_verdict("4h", root=Path(td))
                return []
            except SystemExit as e:
                return [f"the read HALTED instead of defaulting: {str(e)[:90]}"]

    def conjunction_broken():
        q = v.copy()
        q.loc[q.index[0], "verdict_pass"] = True       # a verdict without its gates
        q.loc[q.index[0], "gate_edge_fade_pass"] = False
        q.loc[q.index[0], "gate_height_pass"] = False
        n = int((q["verdict_pass"] != (q["gate_height_pass"] & q["gate_edge_fade_pass"])).sum())
        return [f"{n} verdict(s) are not the conjunction LEDGER.md:834 orders"] if n else []

    def margin_is_a_mean_of_cells():
        """THE DEFECT ITSELF, PLANTED: the margin rows are replaced by the
        weighted mean of the per-cell nets that the prior digest published.
        The leg must find it — on a real lens, with real numbers, and without
        being told where to look [review 2026-09-22, finding 1]."""
        e = _r34("edge_fade")
        found = []
        for lens in sorted(set(e["lens"])):
            filed = [float(C.edge_margin(e, lens, dec=i, age=C.EDGE_AGE_ALL)["net"])
                     for i in range(10)]
            mean = _cellmean(e, lens, C.POOL_ALL, "frozen3.0", C.ERA_ALL, "H20",
                             near_only=False, by="entry_decile")
            bad = [i for i in range(10)
                   if not np.isclose(filed[i], float(mean.get(i, np.nan)),
                                     rtol=0, atol=1e-9)]
            if bad:
                i = bad[0]
                found.append(f"{lens} d{i}: RAW margin {filed[i]:+.4f} vs the "
                             f"mean-of-cells {float(mean[i]):+.4f} "
                             f"({len(bad)}/10 deciles differ)")
        filedm, meanm = {}, {}
        for lens in sorted(set(e["lens"])):
            filedm[lens] = [float(C.edge_margin(e, lens, dec=C.EDGE_DEC_ALL,
                                                age=k)["net"]) for k in C.AGE_LABELS]
            g = _cellmean(e, lens, C.POOL_ALL, "frozen3.0", C.ERA_ALL, "H20",
                          near_only=True, by="age_bucket")
            meanm[lens] = [float(g[k]) for k in C.AGE_LABELS]
        mono = {k: all(v[i + 1] <= v[i] for i in range(len(v) - 1))
                for k, v in filedm.items()}
        mono_mean = {k: all(v[i + 1] <= v[i] for i in range(len(v) - 1))
                     for k, v in meanm.items()}
        flip = [k for k in mono if mono[k] != mono_mean[k]]
        if flip:
            found.append(f"the monotonicity VERDICT itself flips on {flip}: RAW "
                         f"{mono[flip[0]]}, mean-of-cells {mono_mean[flip[0]]}")
        return found

    def floor_moved():
        """The declared sample floor is moved on the MODULE; the filed
        verdicts must then disagree with the live law [as F-C10-HT does for
        the 3.0x threshold]."""
        keep = (C.HEIGHT_MIN_N_RANGES, C.EDGE_MIN_N_RANGES, C.EDGE_MIN_N_BARS)
        try:
            C.HEIGHT_MIN_N_RANGES = 1
            C.EDGE_MIN_N_RANGES = 1
            C.EDGE_MIN_N_BARS = 1
            hp = ((v["n_ranges"] >= C.HEIGHT_MIN_N_RANGES)
                  & (v["ratio_median"] >= C.HEIGHT_RATIO_MIN)
                  & (v["share_ratio_lt_1"] <= C.INFEASIBLE_MAX_SHARE))
            ep = ((v["edge_n_ranges"] >= C.EDGE_MIN_N_RANGES)
                  & (v["edge_n"] >= C.EDGE_MIN_N_BARS) & (v["edge_net_h20"] > 0))
            n = int(((hp & ep) != v["verdict_pass"]).sum())
            return [f"{n} filed verdict(s) disagree with the live floor"] if n else []
        finally:
            (C.HEIGHT_MIN_N_RANGES, C.EDGE_MIN_N_RANGES,
             C.EDGE_MIN_N_BARS) = keep

    def provisional_served():
        """The read interface must REFUSE a provisional row by default. The
        plant asks for one by name and proves the default path HALTs."""
        pr = v[v["provisional"]]
        if not len(pr):
            return ["VACUOUS: no provisional row is filed to refuse"]
        r0 = pr.iloc[0]
        try:
            C.height_vs_toll_verdict(r0["lens"], root=CROOT, asset=r0["asset"],
                                     scale_kind=r0["scale_kind"],
                                     era=r0["era"])
            return []
        except SystemExit as ex:
            got = C.height_vs_toll_verdict(r0["lens"], root=CROOT,
                                           asset=r0["asset"],
                                           scale_kind=r0["scale_kind"],
                                           era=r0["era"],
                                           allow_provisional=True)
            if not bool(got.get("provisional")):
                return ["the row served under allow_provisional does not say so"]
            return [f"the read REFUSED a provisional row: {str(ex)[:90]}"]

    def floor_counted_in_bars():
        """THE FLOOR COUNTED IN IN-RANGE BARS ON **BOTH** LEGS instead of in
        CONFIRMED RANGES — the reading LEAN R3-e rejects, since the bars inside
        one range are one observation seen many times. Filed verdicts must
        move, and the rows that move must be the thin ones; otherwise counting
        in ranges buys nothing and the lean is decoration."""
        alt = ((v["edge_n"] >= C.EDGE_MIN_N_BARS)
               & (v["ratio_median"] >= C.HEIGHT_RATIO_MIN)
               & (v["share_ratio_lt_1"] <= C.INFEASIBLE_MAX_SHARE)
               & (v["edge_net_h20"] > 0))
        d = v[alt != v["verdict_pass"]]
        if not len(d):
            return []                       # VOID: the break leg goes GREEN
        thin = d[d["n_ranges"] < C.PROVISIONAL_MIN_N]
        w = d.sort_values("n_ranges").iloc[0]
        return [f"{len(d)} filed verdict(s) move when the floor is counted in "
                f"BARS ({len(thin)} of them below {C.PROVISIONAL_MIN_N} ranges) "
                f"— e.g. {w['asset']} {w['lens']} {w['scale_kind']} would PASS on "
                f"{int(w['n_ranges'])} confirmed range(s) / {int(w['edge_n']):,} "
                f"in-range bars"]

    return plants([("the gate THRESHOLD is silently changed", threshold_moved),
                   ("the filed gate law sha no longer matches the code", gate_law_sha_moved),
                   ("the verdict is READ BEFORE IT IS FILED", read_before_filed),
                   ("a verdict is not its two gates' conjunction", conjunction_broken),
                   ("A MARGIN IS A WEIGHTED MEAN OF THE CELLS (the prior digest's "
                    "own arithmetic)", margin_is_a_mean_of_cells),
                   ("the declared SAMPLE FLOOR is moved", floor_moved),
                   ("the SAMPLE FLOOR is counted in BARS, not CONFIRMED RANGES",
                    floor_counted_in_bars),
                   ("a PROVISIONAL verdict is asked for on the default path",
                    provisional_served)])


def ht_real():
    h = _r34("height_toll")
    v = _r34("height_toll_verdict")
    e = _r34("edge_fade")
    man = json.loads((CROOT / "R34_MANIFEST.json").read_text())
    com = man["commission"]
    npan = len(com["assets"]) + len(C.pools_for(com["assets"]))
    bad: list[str] = []
    for nm, df, want in (
            ("height_toll", h, npan * len(com["lenses"]) * len(com["scale_kinds"])
             * len(C.ERAS)),
            # THE VERDICT IS KEYED ON THE ERA TOO [LEAN R3-f; review round 3]:
            # three rows per panel per lens per scale kind, never one.
            ("height_toll_verdict", v, npan * len(com["lenses"])
             * len(com["scale_kinds"]) * len(C.ERAS)),
            # 10 x 6 CELLS + 10 by-decile margins + 6 near-edge-by-age margins
            # + 1 near-edge/all-ages margin, per era per horizon [LEAN R3-d]
            ("edge_fade", e, npan * len(com["lenses"]) * len(com["scale_kinds"])
             * len(C.ERAS) * len(C.HORIZONS)
             * (10 * len(C.AGE_BUCKETS) + 10 + len(C.AGE_BUCKETS) + 1))):
        if len(df) != want:
            bad.append(f"{nm} is {len(df)} rows, the whole declared grid is {want}")
    # the gate is the DECLARED arithmetic on every row — no hand-set verdicts
    re = ((h["ratio_median"] >= C.HEIGHT_RATIO_MIN)
          & (h["share_ratio_lt_1"] <= C.INFEASIBLE_MAX_SHARE)
          & (h["n_ranges"] >= C.HEIGHT_MIN_N_RANGES))
    if int((re != h["gate_height_pass"]).sum()):
        bad.append("a filed gate_height_pass is not the declared arithmetic")
    # THE SAMPLE FLOOR IS REAL ON EVERY ROW [review 2026-09-22, finding 2]
    if int((h["n_ranges"] < C.HEIGHT_MIN_N_RANGES).sum() and
           (h[h["n_ranges"] < C.HEIGHT_MIN_N_RANGES]["gate_height_pass"]).sum()):
        bad.append("a height gate PASSES below the declared floor")
    ev = ((v["edge_n_ranges"] >= C.EDGE_MIN_N_RANGES)
          & (v["edge_n"] >= C.EDGE_MIN_N_BARS) & (v["edge_net_h20"] > 0))
    if int((ev != v["gate_edge_fade_pass"]).sum()):
        bad.append("a filed gate_edge_fade_pass is not the declared arithmetic")
    pl = ((v["n_ranges"] < C.PROVISIONAL_MIN_N)
          | (v["edge_n_ranges"] < C.PROVISIONAL_MIN_N))
    if int((pl != v["provisional"]).sum()):
        bad.append("a filed `provisional` is not lean C-g's declared law")
    if int((v["provisional"] & v["verdict_pass"]).sum()):
        bad.append("a PROVISIONAL row carries verdict_pass = True")
    for col in ("provisional", "provisional_reason", "edge_n_ranges",
                "min_n_ranges_pinned", "gates_what"):
        if col not in v.columns:
            bad.append(f"height_toll_verdict has no `{col}` column")
    if "toll_basis" not in h.columns or "toll_atr_binding" not in h.columns:
        bad.append("height_toll does not declare its toll convention")
    # THE MARGINS ARE RAW, NOT A COLLAPSE OF THE CELLS [LEAN R3-d, finding 1].
    # Judged against a LIVE re-walk of a real cell, not against the table.
    A_live, _tp, _w = _live_edge(R34_CELL[0], R34_CELL[1], "frozen3.0")
    near_live = C._near_mask(A_live["dec"])
    for dec in range(10):
        want = C._edge_stats(A_live, A_live["dec"] == dec, "H20", False)
        got = C.edge_margin(e, R34_CELL[1], asset=R34_CELL[0], dec=dec,
                            age=C.EDGE_AGE_ALL)
        if not (np.isclose(float(got["net"]), want["net"], rtol=0, atol=1e-12)
                and int(got["n"]) == want["n"]
                and int(got["n_ranges"]) == want["n_ranges"]):
            bad.append(f"the filed by-decile margin d{dec} on {R34_CELL[0]} "
                       f"{R34_CELL[1]} is not the live raw statistic "
                       f"({float(got['net']):+.6f} vs {want['net']:+.6f})")
    for ab, lab in enumerate(C.AGE_LABELS):
        want = C._edge_stats(A_live, near_live & (A_live["age"] == ab), "H20", False)
        got = C.edge_margin(e, R34_CELL[1], asset=R34_CELL[0],
                            dec=C.EDGE_DEC_ALL, age=lab)
        if not (np.isclose(float(got["net"]), want["net"], rtol=0, atol=1e-12)
                and int(got["n"]) == want["n"]):
            bad.append(f"the filed near-edge age margin {lab} on {R34_CELL[0]} "
                       f"{R34_CELL[1]} is not the live raw statistic")
    # and the near-edge / ALL-ages margin IS the gate's own statistic, bit for bit
    n_gate = 0
    for lens in com["lenses"]:
        for kind in com["scale_kinds"]:
            for asset in sorted(set(v["asset"])):
                for era in C.ERAS:
                    m = C.edge_margin(e, lens, asset=asset, kind=kind, era=era,
                                      dec=C.EDGE_DEC_ALL, age=C.EDGE_AGE_ALL)
                    q = v[(v["lens"] == lens) & (v["scale_kind"] == kind)
                          & (v["asset"] == asset) & (v["era"] == era)]
                    if len(q) != 1:
                        bad.append(f"{len(q)} verdict row(s) for {asset} {lens} "
                                   f"{kind} era {era}")
                        continue
                    r = q.iloc[0]
                    n_gate += 1
                    # NaN faces NaN on an EMPTY era (HYPEUSDT / PUMPUSDT have no
                    # tuning-era bars): absent together is equal; absent facing a
                    # number is NOT [LEAN R3-f].
                    if not (_bitsame(m["net"], r["edge_net_h20"])
                            and int(m["n"]) == int(r["edge_n"])
                            and int(m["n_ranges"]) == int(r["edge_n_ranges"])
                            and _bitsame(m["toll_atr"], r["edge_toll_atr"])):
                        bad.append(f"the near-edge margin for {asset} {lens} {kind} "
                                   f"era {era} is not the verdict row's own edge "
                                   "statistic")
    # A MARGIN IS NOT THE MEAN OF ITS CELLS, and the difference is not cosmetic
    worst = 0.0
    for lens in com["lenses"]:
        g = _cellmean(e, lens, C.POOL_ALL, "frozen3.0", C.ERA_ALL, "H20",
                      near_only=False, by="entry_decile")
        for i in range(10):
            f_ = float(C.edge_margin(e, lens, dec=i, age=C.EDGE_AGE_ALL)["net"])
            worst = max(worst, abs(f_ - float(g.get(i, np.nan))))
    if not worst > 1e-6:
        bad.append("the filed margins are indistinguishable from a mean of the "
                   "cells — the leg that caught finding 1 has gone vacuous")
    if set(h["ratio_min_pinned"]) != {C.HEIGHT_RATIO_MIN}:
        bad.append("a row's pinned ratio floor is not the code's")
    if set(h["gate_law_sha"]) != {_law_sha(C.HEIGHT_GATE_LAW)}:
        bad.append("a row's gate_law_sha is not the live law's")
    # LEDGER.md:834's conjunction, on every row
    if int((v["verdict_pass"] != (v["gate_height_pass"] & v["gate_edge_fade_pass"])).sum()):
        bad.append("a verdict is not height AND edge-fade")
    # the ratio is ATR-FREE: re-derived from price and the fee object alone
    tape, m, w, bps = _walk_cell()
    hl = C.height_rows(w, tape, R34_CELL[0], R34_CELL[1], "frozen3.0", bps)
    alt = (hl["height_px"] / ((bps / C.BPS_PER_UNIT) * hl["close_at_confirm"]))
    if not np.allclose(hl["ratio"], alt, rtol=1e-12, atol=0):
        bad.append("the ratio is NOT ATR-free — the ATR does not cancel")
    f = h[(h["asset"] == R34_CELL[0]) & (h["lens"] == R34_CELL[1])
          & (h["scale_kind"] == "frozen3.0") & (h["era"] == C.ERA_ALL)]
    if int(f["n_ranges"].iloc[0]) != int(len(hl)):
        bad.append(f"filed n_ranges {int(f['n_ranges'].iloc[0])} != re-walked {len(hl)}")
    # the READ INTERFACE hands back the filed row, for every lens
    got = {}
    for lens in com["lenses"]:
        for era in C.ERAS:
            r = C.height_vs_toll_verdict(lens, root=CROOT, era=era)
            if era == C.ERA_ALL:
                got[lens] = bool(r["verdict_pass"])
            row = v[(v["lens"] == lens) & (v["scale_kind"] == "frozen3.0")
                    & (v["asset"] == C.POOL_ALL) & (v["era"] == era)]
            if bool(row["verdict_pass"].iloc[0]) != bool(r["verdict_pass"]):
                bad.append("the read interface disagrees with the filed row on "
                           f"{lens} era {era}")
            if str(r.get("era")) != era or str(r.get("era_judged")) != era:
                bad.append(f"the served row does not state its era on {lens} {era}")
    nm = int((e["margin"] != C.MARGIN_CELL).sum())
    return (not bad, "; ".join(bad) if bad else
            f"{len(h)} height rows + {len(v)} verdicts + {len(e):,} edge-fade rows "
            f"({len(e) - nm:,} cells + {nm:,} MARGIN rows) = the whole declared grid · "
            f"gate = n_ranges >= {C.HEIGHT_MIN_N_RANGES} AND median(ratio) >= "
            f"{C.HEIGHT_RATIO_MIN} AND share(ratio<1) <= {C.INFEASIBLE_MAX_SHARE} (sha "
            f"{_law_sha(C.HEIGHT_GATE_LAW)[:16]}) · edge leg floor edge_n_ranges >= "
            f"{C.EDGE_MIN_N_RANGES} confirmed ranges · the ratio is ATR-free to 1e-12 on "
            f"{R34_CELL[0]} {R34_CELL[1]} ({len(hl)} ranges) · verdict = height AND "
            f"edge-fade on every row · {int(v['verdict_pass'].sum())}/{len(v)} rows PASS "
            f"and {int(v['provisional'].sum())}/{len(v)} are PROVISIONAL, all filed and "
            f"all printed in the digest · every one of the {n_gate} near-edge/ALL-ages "
            f"MARGIN rows is bit-identical to its verdict row's edge statistic, and the "
            f"{len(com['lenses']) * 10} by-decile margins differ from a mean of their "
            f"cells by up to {worst:.4f} ATR · the by-decile and near-edge-age margins on "
            f"{R34_CELL[0]} {R34_CELL[1]} equal a LIVE raw re-walk to 1e-12 · read "
            f"interface POOLED:ALL frozen3.0: "
            + ", ".join(f"{k} {'PASS' if x else 'FAIL'}" for k, x in got.items()))


# ═════════════ F-C10-HT-ERA (Q-R3) — THE VERDICT GRID IS KEYED ON THE ERA
# [review round 3, blocking finding].  The verdict used to be filed 120 rows
# deep on (lens, scale_kind, asset), silently judged on full history, while
# BOTH of its inputs were filed three ways per era.  The split is not cosmetic:
# it reverses this digest's own headline, and the ONE pooled row that passes on
# full history FAILS on the holdout era — the era P-BRK-S1 is scored in.
DIGEST_NAME = "CENSUS_R_DIGEST.md"
NEAR_KW = dict(dec=C.EDGE_DEC_ALL, age=C.EDGE_AGE_ALL)


def _era_counts(v) -> dict:
    """PASS per era, computed HERE from the filed table and from nothing else."""
    return {era: int(v[v["era"] == era]["verdict_pass"].sum()) for era in C.ERAS}


def _era_grid_findings(q, want_rows: int) -> list[str]:
    """EVERY GRID WHOLE, on the era axis: the era is a column, it is never
    null, it names only declared eras, the key is unique WITH it, and every
    (lens, scale_kind, asset) carries all three eras."""
    f = []
    if "era" not in q.columns:
        return ["the verdict table has NO `era` column — a whole declared "
                "dimension is missing and no row can say what it was judged on"]
    if int(q["era"].isna().sum()) or int((q["era"].astype(str) == "").sum()):
        f.append("a verdict row carries no era")
    unk = sorted(set(q["era"].astype(str)) - set(C.ERAS))
    if unk:
        f.append(f"a verdict row names an undeclared era: {unk}")
    if len(q) != want_rows:
        f.append(f"the verdict table is {len(q)} rows; the whole declared grid "
                 f"is {want_rows} ({want_rows // len(C.ERAS)} panels x "
                 f"{len(C.ERAS)} eras)")
    key = ["lens", "scale_kind", "asset", "era"]
    dup = int(q.duplicated(subset=key).sum())
    if dup:
        f.append(f"{dup} duplicate row(s) under the declared key {key}")
    g = q.groupby(["lens", "scale_kind", "asset"], sort=True)["era"].nunique()
    short = g[g != len(C.ERAS)]
    if len(short):
        f.append(f"{len(short)} panel(s) do not carry all {len(C.ERAS)} eras, "
                 f"e.g. {short.index[0]} carries {int(short.iloc[0])}")
    return f


def _digest_era_findings(text: str, v) -> list[str]:
    """WHAT §B.3 MUST SAY ABOUT THE ERA, judged against the FILED table —
    every number below is recomputed here, never read out of the prose and
    compared to itself."""
    f = []
    for era, n in _era_counts(v).items():
        m = re.search(rf"era {re.escape(era)} = (\d+) PASS", text)
        if not m:
            f.append(f"the digest prints no PASS count for era {era}")
        elif int(m.group(1)) != n:
            f.append(f"the digest says {m.group(1)} PASS on era {era}; the filed "
                     f"table says {n}")
    if re.search(r"\*\*THE CONJUNCTION FAILS ON EVERY POOLED:ALL ROW", text):
        f.append("the digest still carries the UNQUALIFIED bold headline 'THE "
                 "CONJUNCTION FAILS ON EVERY POOLED:ALL ROW' — a sentence true "
                 "of era ALL alone and false of the grid")
    if "ON FULL HISTORY (era = ALL)" not in text:
        f.append("the full-history headline does not name the era it is true of")
    by = {}
    for r in v.itertuples():
        by.setdefault((r.lens, r.scale_kind, r.asset), {})[r.era] = r
    moves = [k for k, g in by.items()
             if len({bool(g[e].verdict_pass) for e in C.ERAS if e in g}) > 1]
    m = re.search(r"CHANGES WITH THE ERA — ALL (\d+) OF THEM", text)
    if not m:
        f.append("the digest does not name the rows whose verdict changes with era")
    elif int(m.group(1)) != len(moves):
        f.append(f"the digest names {m.group(1)} era-dependent rows; the filed "
                 f"table has {len(moves)}")
    for lens, kind, asset in (("1d", "frozen3.0", C.POOL_CLASSIC5),
                              ("1d", "frozen3.0", C.POOL_ALL),
                              ("1d", "calibrated", C.POOL_ALL),
                              ("4h", "frozen3.0", C.POOL_CLASSIC5),
                              ("1d", "frozen3.0", C.POOL_UNSEEN12)):
        z = v[(v["lens"] == lens) & (v["scale_kind"] == kind)
              & (v["asset"] == asset)]
        if not len(z):
            continue
        head = f"- **{lens} | {kind} | {asset}**"
        line = next((ln for ln in text.splitlines() if ln.startswith(head)), None)
        if line is None:
            f.append(f"the digest does not name {lens} | {kind} | {asset} among "
                     "the panels the era split moves")
            continue
        for r in z.itertuples():
            if f"net {float(r.edge_net_h20):+.6f}" not in line:
                f.append(f"the digest's line for {lens} | {kind} | {asset} does "
                         f"not carry its filed era-{r.era} net "
                         f"{float(r.edge_net_h20):+.6f}")
        np_ = int(z["verdict_pass"].sum())
        if line.count("**PASS**") != np_:
            f.append(f"the digest's line for {lens} | {kind} | {asset} shows "
                     f"{line.count('**PASS**')} PASS verdicts; the filed table "
                     f"has {np_}")
    return f


def ht_era_break():
    """FOUR deliberate sabotages of the ERA KEYING, one at a time."""
    v = _r34("height_toll_verdict")
    man = json.loads((CROOT / "R34_MANIFEST.json").read_text())
    com = man["commission"]
    npan = len(com["assets"]) + len(C.pools_for(com["assets"]))
    want = npan * len(com["lenses"]) * len(com["scale_kinds"]) * len(C.ERAS)
    txt = (CROOT / DIGEST_NAME).read_text() if (CROOT / DIGEST_NAME).exists() else ""

    def collapsed_to_all():
        """THE DEFECT ITSELF: the era rows are dropped and the table collapses
        to the 120 full-history rows the prior build filed."""
        return _era_grid_findings(v[v["era"] == C.ERA_ALL].copy(), want)

    def era_column_gone():
        """A verdict row with no era at all — in the table AND at the read."""
        q = v.drop(columns=["era"])
        found = _era_grid_findings(q, want)
        with tempfile.TemporaryDirectory() as td:
            q.to_parquet(Path(td) / "height_toll_verdict.parquet", index=False)
            try:
                C.height_vs_toll_verdict(com["lenses"][0], root=Path(td))
                found.append("BUT the read interface SERVED the era-less table")
            except SystemExit as ex:
                found.append(f"and the read HALTED: {str(ex)[:80]}")
        return found

    def one_era_from_anothers_inputs():
        """A verdict recomputed for the HOLDOUT from the ALL era's inputs —
        live, on a real cell, both as the HALT the builder owes and as the
        number it would otherwise have filed."""
        tape, m, w, bps = _walk_cell()
        sym, lens = R34_CELL
        hl = C.height_rows(w, tape, sym, lens, "frozen3.0", bps)
        hg = C.height_grid(hl, sym, lens)
        A_ = C.edge_arrays(tape, w, bps, 0)
        honest = {(sym, "frozen3.0", e): C.edge_gate(A_, False, e) for e in C.ERAS}
        wrong = dict(honest)
        wrong[(sym, "frozen3.0", C.ERA_HOLDOUT)] = honest[(sym, "frozen3.0", C.ERA_ALL)]
        found = []
        try:
            C.verdict_rows(hg, wrong, lens)
            found.append("BUT verdict_rows FILED a holdout verdict built from the "
                         "ALL era's edge gate")
        except SystemExit as ex:
            found.append(f"verdict_rows HALTED: {str(ex)[:90]}")
        a, h = (honest[(sym, "frozen3.0", C.ERA_ALL)],
                honest[(sym, "frozen3.0", C.ERA_HOLDOUT)])
        if (int(a["n"]) == int(h["n"]) and int(a["n_ranges"]) == int(h["n_ranges"])
                and float(a["net"]) == float(h["net"])):
            found.append("VACUOUS: the ALL and holdout edge gates are the same "
                         f"statistic on {sym} {lens}")
        else:
            found.append(f"and the two are different statistics on {sym} {lens}: "
                         f"ALL n {int(a['n']):,} / ranges {int(a['n_ranges'])} / net "
                         f"{float(a['net']):+.6f} vs holdout n {int(h['n']):,} / "
                         f"ranges {int(h['n_ranges'])} / net {float(h['net']):+.6f}")
        return found

    def digest_headline_wrong():
        """The digest's own sentences, mutated one at a time against the filed
        table: a PASS count bumped by one, the era-dependent row count bumped,
        and the old unqualified headline restored."""
        if not txt:
            return ["VACUOUS: no digest is filed to check"]
        found = []
        for era, n in _era_counts(v).items():
            bad = txt.replace(f"era {era} = {n} PASS", f"era {era} = {n + 1} PASS", 1)
            got = _digest_era_findings(bad, v)
            found += [f"[{era} count bumped] {got[0]}"] if got else []
            if not got:
                return []                       # a mutation nothing caught: VOID
        m = re.search(r"CHANGES WITH THE ERA — ALL (\d+) OF THEM", txt)
        if m:
            bad = txt.replace(m.group(0), f"CHANGES WITH THE ERA — ALL "
                              f"{int(m.group(1)) + 1} OF THEM", 1)
            got = _digest_era_findings(bad, v)
            if not got:
                return []
            found.append(f"[era-dependent row count bumped] {got[0]}")
        bad = txt.replace("ON FULL HISTORY (era = ALL) THE CONJUNCTION FAILS",
                          "THE CONJUNCTION FAILS", 1)
        got = _digest_era_findings(bad, v)
        if not got:
            return []
        found.append(f"[the old unqualified headline restored] {got[0]}")
        return found

    return plants([
        ("THE DEFECT ITSELF: the verdict grid collapsed to era = ALL", collapsed_to_all),
        ("a verdict row carries no era (table AND read interface)", era_column_gone),
        ("a verdict recomputed for one era from ANOTHER era's inputs",
         one_era_from_anothers_inputs),
        ("the digest's headline does not match the filed per-era counts",
         digest_headline_wrong)])


def ht_era_real():
    v = _r34("height_toll_verdict")
    h = _r34("height_toll")
    e = _r34("edge_fade")
    man = json.loads((CROOT / "R34_MANIFEST.json").read_text())
    com = man["commission"]
    npan = len(com["assets"]) + len(C.pools_for(com["assets"]))
    want = npan * len(com["lenses"]) * len(com["scale_kinds"]) * len(C.ERAS)
    bad = _era_grid_findings(v, want)
    if bad:
        return False, "; ".join(bad)
    if man["keys"]["height_toll_verdict"] != ["lens", "scale_kind", "asset", "era"]:
        bad.append(f"the manifest declares the verdict key as "
                   f"{man['keys']['height_toll_verdict']}, not the era-keyed one")
    # ── EVERY ROW IS ITS OWN ERA'S CONJUNCTION, recomputed from the two INPUT
    # ── tables — the reviewer's own independent recompute, on all 360 rows ──
    near = e[(e["margin"] == C.MARGIN_NEAR) & (e["horizon"] == "H20")]
    j = h.merge(near[["asset", "lens", "scale_kind", "era", "n", "n_ranges", "net",
                      "median_term", "toll_atr", "hit_rate_net"]],
                on=["asset", "lens", "scale_kind", "era"], how="left",
                suffixes=("", "_e"))
    ep = ((j["n_ranges_e"] >= C.EDGE_MIN_N_RANGES) & (j["n"] >= C.EDGE_MIN_N_BARS)
          & (j["net"] > 0))
    j["want_pass"] = j["gate_height_pass"].astype(bool) & ep
    j["want_edge"] = ep
    k = ["lens", "scale_kind", "asset", "era"]
    z = v.merge(j[k + ["want_pass", "want_edge", "n", "n_ranges_e", "net",
                       "n_ranges", "gate_height_pass"]], on=k, how="left",
                suffixes=("", "_w"))
    if len(z) != len(v):
        bad.append(f"the recompute joined {len(z)} rows onto {len(v)} verdicts")
    for col, wcol, nm in (("verdict_pass", "want_pass", "verdict"),
                          ("gate_edge_fade_pass", "want_edge", "edge leg"),
                          ("gate_height_pass", "gate_height_pass_w", "height leg")):
        n = int((z[col].astype(bool) != z[wcol].astype(bool)).sum())
        if n:
            bad.append(f"{n} filed {nm}(s) are not the per-era conjunction of the "
                       "filed height row and the filed near-edge margin of the SAME era")
    for a, b_, nm in (("edge_n", "n", "edge_n"), ("edge_n_ranges", "n_ranges_e",
                                                  "edge_n_ranges"),
                      ("n_ranges", "n_ranges_w", "n_ranges")):
        n = int((z[a].astype("int64") != z[b_].astype("int64")).sum())
        if n:
            bad.append(f"{n} verdict row(s) carry a {nm} that is not their own era's")
    # NaN faces NaN on an EMPTY era (HYPEUSDT / PUMPUSDT have no tuning-era
    # bars at all): the two must be absent TOGETHER, and finite where both are.
    a_ = z["edge_net_h20"].to_numpy(float)
    b_ = z["net"].to_numpy(float)
    n = int(((np.isnan(a_) != np.isnan(b_))
             | (~np.isnan(a_) & ~np.isnan(b_)
                & ~np.isclose(a_, b_, rtol=0, atol=1e-9))).sum())
    if n:
        bad.append(f"{n} verdict row(s) carry an edge NET that is not their own era's")
    # ── THE FLOORS ARE APPLIED WITHIN THE ERA, not inherited from ALL ──────
    pl = ((v["n_ranges"] < C.PROVISIONAL_MIN_N)
          | (v["edge_n_ranges"] < C.PROVISIONAL_MIN_N))
    if int((pl != v["provisional"]).sum()):
        bad.append("a filed `provisional` is not lean C-g's law ON ITS OWN ERA's n")
    # ── A LIVE RE-WALK OF ONE REAL CELL, PER ERA ──────────────────────────
    tape, m, w, bps = _walk_cell()
    sym, lens = R34_CELL
    A_ = C.edge_arrays(tape, w, bps, 0)
    hl = C.height_rows(w, tape, sym, lens, "frozen3.0", bps)
    hgl = {r["era"]: r for r in C.height_grid(hl, sym, lens)
           if r["scale_kind"] == "frozen3.0"}
    live = {}
    for era in C.ERAS:
        g = C.edge_gate(A_, False, era)
        live[era] = g
        r = v[(v["lens"] == lens) & (v["scale_kind"] == "frozen3.0")
              & (v["asset"] == sym) & (v["era"] == era)].iloc[0]
        if not (int(g["n"]) == int(r["edge_n"])
                and int(g["n_ranges"]) == int(r["edge_n_ranges"])
                and np.isclose(float(g["net"]), float(r["edge_net_h20"]),
                               rtol=0, atol=1e-8)):
            bad.append(f"the filed {sym} {lens} era-{era} edge leg is not the LIVE "
                       f"re-walk ({float(r['edge_net_h20']):+.6f} vs "
                       f"{float(g['net']):+.6f})")
        if bool(hgl[era]["gate_height_pass"]) != bool(r["gate_height_pass"]):
            bad.append(f"the filed {sym} {lens} era-{era} height leg is not the LIVE "
                       "re-walk")
        if int(hgl[era]["n_ranges"]) != int(r["n_ranges"]):
            bad.append(f"the filed {sym} {lens} era-{era} n_ranges is not the LIVE "
                       "re-walk")
    if (int(live[C.ERA_ALL]["n"]) == int(live[C.ERA_HOLDOUT]["n"])
            and int(live[C.ERA_ALL]["n"]) == int(live[C.ERA_TUNING]["n"])):
        bad.append("VACUOUS: the three eras are the same sample on the live cell")
    if int(live[C.ERA_TUNING]["n"]) + int(live[C.ERA_HOLDOUT]["n"]) != int(
            live[C.ERA_ALL]["n"]):
        bad.append("the two eras do not partition the ALL sample on the live cell")
    # ── THE THREE ERAS ARE THREE DIFFERENT ROW SETS, or the split is décor ──
    sets = {era: set(map(tuple, v[(v["era"] == era) & v["verdict_pass"]]
                         [["lens", "scale_kind", "asset"]].to_numpy().tolist()))
            for era in C.ERAS}
    if sets[C.ERA_ALL] == sets[C.ERA_TUNING] == sets[C.ERA_HOLDOUT]:
        bad.append("VACUOUS: the three eras PASS on exactly the same rows")
    # ── THE READ INTERFACE TAKES THE ERA AND SAYS WHICH ERA IT SERVED ─────
    for lens_ in com["lenses"]:
        for era in C.ERAS:
            r = C.height_vs_toll_verdict(lens_, root=CROOT, era=era,
                                         allow_provisional=True)
            row = v[(v["lens"] == lens_) & (v["scale_kind"] == "frozen3.0")
                    & (v["asset"] == C.POOL_ALL) & (v["era"] == era)].iloc[0]
            if str(r.get("era")) != era or str(r.get("era_judged")) != era:
                bad.append(f"the served {lens_} row does not state era {era}")
            if bool(r["verdict_pass"]) != bool(row["verdict_pass"]):
                bad.append(f"the read interface disagrees with the filed "
                           f"{lens_} era-{era} row")
    try:
        C.height_vs_toll_verdict(com["lenses"][0], root=CROOT, era="full")
        bad.append("the read interface served an era the census never filed")
    except SystemExit:
        pass
    d = C.height_vs_toll_verdict(com["lenses"][0], root=CROOT,
                                 allow_provisional=True)
    if str(d.get("era_judged")) != C.ERA_ALL:
        bad.append("the DEFAULT read does not state that it judged on era ALL")
    # ── THE FLOOR BITES WITHIN THE ERA: a row clean on ALL, provisional on an
    # ── era, is REFUSED for that era and served for ALL ───────────────────
    split = None
    for key, g in v.groupby(["lens", "scale_kind", "asset"], sort=True):
        s = g.set_index("era")
        if (not bool(s.loc[C.ERA_ALL, "provisional"])
                and any(bool(s.loc[x, "provisional"]) for x in
                        (C.ERA_TUNING, C.ERA_HOLDOUT) if x in s.index)):
            split = (key, s)
            break
    if split is None:
        bad.append("VACUOUS: no panel is clean on ALL and provisional on an era")
    else:
        (ln_, kd_, as_), s = split
        era_ = next(x for x in (C.ERA_TUNING, C.ERA_HOLDOUT)
                    if bool(s.loc[x, "provisional"]))
        C.height_vs_toll_verdict(ln_, root=CROOT, asset=as_, scale_kind=kd_)
        try:
            C.height_vs_toll_verdict(ln_, root=CROOT, asset=as_, scale_kind=kd_,
                                     era=era_)
            bad.append(f"the read served the PROVISIONAL era-{era_} row for {as_} "
                       f"{ln_} {kd_} on the default path")
        except SystemExit:
            pass
    # ── AND THE DIGEST SAYS THE SAME NUMBERS ──────────────────────────────
    if not (CROOT / DIGEST_NAME).exists():
        bad.append(f"no {DIGEST_NAME} is filed to check")
    else:
        bad += _digest_era_findings((CROOT / DIGEST_NAME).read_text(), v)
    cnt = _era_counts(v)
    return (not bad, "; ".join(bad[:6]) if bad else (
        f"{len(v)} verdict rows = {npan} panels x {len(com['lenses'])} lenses x "
        f"{len(com['scale_kinds'])} scale kinds x {len(C.ERAS)} ERAS, key "
        f"{man['keys']['height_toll_verdict']}, every row carrying its era · the "
        f"conjunction on ALL {len(v)} rows is its OWN era's filed height row AND "
        f"its OWN era's near-edge MARGIN row, recomputed here from the two input "
        f"tables · PASS per era: "
        + " · ".join(f"{k} {cnt[k]}/{len(v) // len(C.ERAS)}" for k in C.ERAS)
        + f" — {len(sets[C.ERA_ALL] ^ sets[C.ERA_TUNING])} rows differ between ALL "
        f"and tuning, {len(sets[C.ERA_ALL] ^ sets[C.ERA_HOLDOUT])} between ALL and "
        f"holdout · LIVE re-walk of {sym} {lens}: the three era gates are "
        + ", ".join(f"{k} n {int(live[k]['n']):,}/ranges "
                    f"{int(live[k]['n_ranges'])}/net {float(live[k]['net']):+.6f}"
                    for k in C.ERAS)
        + f" and tuning + holdout = ALL exactly · the read takes era= and states it "
        f"back in `era` and `era_judged`, HALTS on an era the census never filed, "
        f"and REFUSES a row provisional in ITS OWN era · §B.3's per-era counts, its "
        f"count of era-dependent rows and the five named panels' nets all equal the "
        f"filed table"))


# ═══════════════════════════════════ F-C10-COLLAR (LAW 4 + R1's print collar)
def _report_lines(root: Path) -> list[str]:
    keep = list(C.LOG_LINES)
    C.LOG_LINES.clear()
    try:
        import io
        import contextlib
        with contextlib.redirect_stdout(io.StringIO()):
            C.print_report(root)
        out = list(C.LOG_LINES)
    finally:
        C.LOG_LINES.clear()
        C.LOG_LINES.extend(keep)
    return out


def _collar_findings(lines: list[str]) -> list[str]:
    """Walk the report the way a reader does: the era is the table's header,
    every data row names asset / lens / kind / class.  A row the collar holds
    must not be on a line."""
    bad, era = [], None
    for ln in lines:
        m = re.search(r"OUTCOME AFTER EVENT — era (\S+) —", ln)
        if m:
            era = m.group(1)
            continue
        tok = ln.split()
        if era is None or len(tok) < 5 or tok[1] not in C.LENSES or tok[3] not in DECL_CLASSES:
            continue
        if tok[1] == "5m" and tok[3] in DECL_RETEST and era != "tuning":
            bad.append(f"a collared row is PRINTED: era {era} · {tok[0]} {tok[1]} {tok[3]}")
    return bad


def _collar_texts(root: Path) -> list[Path]:
    return sorted([p for p in root.glob("*.md")] + [p for p in root.glob("*.txt")]
                  + [p for p in root.glob("*.json")])


def _collared_literals(root: Path) -> list[tuple]:
    g = pd.read_parquet(root / "outcome_grid.parquet")
    q = g[(g["lens"] == "5m") & (g["cls"].isin(DECL_RETEST)) & (g["era"] != "tuning")
          & (g["n"] > 0)]
    out = []
    for r in q.itertuples():
        for col in ("median_term", "net", "median_mfe", "median_mae"):
            v = float(getattr(r, col))
            if np.isfinite(v) and abs(v) >= 5e-4:
                out.append((f"{v:.6f}", f"{r.asset}|{r.era}|{r.cls}|{r.horizon}|{col}"))
    return out


def collar_break():
    """THE COLLAR SWITCHED OFF.  printable() is forced True on the MODULE for
    the length of one report; the scan must find the rows it lets through."""
    def off():
        keep = C.printable
        try:
            C.printable = lambda lens, cls, era: True
            return _collar_findings(_report_lines(CROOT))
        finally:
            C.printable = keep

    def literal_planted():
        # THE PLANTED TEXT IS A LOCAL STRING AND THE FIGURE IS NEVER ECHOED: this
        # transcript is itself one of the files the real leg scans, so a finding
        # that quoted the number would leak it and redden the next run.
        lits = _collared_literals(CROOT)
        if not lits:
            return ["VACUOUS: no collared row carries a number to leak"]
        text = "a digest line quoting " + lits[0][0]
        return [f"the scan finds the collared figure of {lits[0][1]} in a planted text "
                f"(the figure itself is REDACTED here — this transcript is scanned)"] \
            if lits[0][0] in text else []
    return plants([("THE COLLAR SWITCHED OFF (printable forced True for one report)", off),
                   ("A COLLARED FIGURE PLANTED IN A TEXT", literal_planted)])


def collar_real():
    lines = _report_lines(CROOT)
    bad = _collar_findings(lines)
    g = pd.read_parquet(CROOT / "outcome_grid.parquet")
    law = ~((g["lens"] == "5m") & (g["cls"].isin(DECL_RETEST)) & (g["era"] != "tuning"))
    if not (g["printable"].astype(bool) == law).all():
        bad.append("the filed printable column is not the declared law")
    lits = _collared_literals(CROOT)
    texts = _collar_texts(CROOT)
    hits = []
    for p in texts:
        body = p.read_text(errors="ignore")
        hits += [f"{p.name}: {lit} ({why})" for lit, why in lits if lit in body]
    bad += hits
    n_held = int((~g["printable"].astype(bool)).sum())
    return not bad, (
        f"the collar holds: print_report emits {len(lines)} lines and NOT ONE of the "
        f"{n_held} collared rows (5m retest-hold outside the tuning era) is among them; the "
        f"filed `printable` column equals the declared law on all {len(g):,} grid rows; none "
        f"of the {len(lits)} six-decimal figures those rows carry appears in any of the "
        f"{len(texts)} text artifacts under {rel(CROOT)} "
        f"({', '.join(p.name for p in texts[:6])}{'…' if len(texts) > 6 else ''})"
        if not bad else f"{len(bad)} finding(s): " + "; ".join(bad[:4]))


# ════════════════════════════════════════════════════════════ main
LEGS = (
    ("F-CEN-TAPE", "the loader — closed bars <= AS_OF, six-bar days, the engine's ATR, whole",
     "a tape's last bar closes after the Stage D AS_OF; a tape differs from the fixture's own "
     "read of the snapshot (4h: the engine's tape_from_klines; 1d: the RF suite's tape_1d and "
     "Stage D's derived file); the ATR is not Wilder's seeded at TR[0]; a prefix's ATR is not "
     "bit-equal to the full tape's; asof_index reads a bar that closes after the instant, or "
     "skips one that closed before it.",
     tape_break, tape_real),
    ("F-RNG-ASOF", "no feature reads a confirm / redraw / flip stamped after its bar",
     "for any cut t (seeded random, or aimed at a harden, a confirm, a flip's hold window, a "
     "pivot's seal) an as-of array, the class-event set or a known_at-filtered log computed on "
     "tape[:t] differs from the full run's restricted to <= t - 1; or the view at t - 1 differs "
     "from the machine's own end-of-prefix state (final_state, the alive Range's top / bottom / "
     "n_deviations, coverage_pct).",
     asof_break, asof_real),
    ("F-RNG-ASOF-SEAL", "the engine's knowable_at = -1 pivots are read at their SEAL — never "
     "at -1, never at the wick",
     "a pivot the engine stamps knowable_at = -1 carries a census known_at that is not its "
     "seal; the ENGINE's own run of the raw tape sees that pivot on tape[:seal] (or on "
     "tape[:wick + 1]) or does not see it on tape[:seal + 1]; for any of the seeded cuts on "
     "NEARUSDT 4h, UNIUSDT 4h or SOLUSDT 5m[:60000] an as-of array, the class-event set or the "
     "known_at-filtered macro log of tape[:t] differs from the full view restricted to "
     "<= t - 1, the honest pivot log differs from the ENGINE's run of tape[:t], or state / "
     "bounds at t - 1 differ from the ENGINE's end-of-prefix; a census known_at precedes its "
     "stamp bar; or a tape named here carries no -1 pivot (the leg would be vacuous).",
     seal_break, seal_real),
    ("F-RF-4", "spring overlap, BOTH sides x BOTH directions — parametrised, mirrored, PRINTED",
     "the parametrised bottom side does not reproduce the v1 suite's own law / statistic "
     "numbers on the v1 suite's own tape; the top side is not the bottom's mirror on the "
     "negated tape; a harden does not reclaim its as-of boundary; a side is missing from the "
     "filed table.",
     rf4_break, rf4_real),
    ("F-CEN-OUTCOME", "term / MFE / MAE / toll re-walked on raw bars — censored, never shortened",
     "a filed term, MFE, MAE, toll or known-close stamp differs from a plain bar-by-bar walk "
     "of the raw parquet from the CLOSE of the known_at bar; a horizon with k + H > n - 1 "
     "carries a number; an all-censored or empty class does not file NaN with its reason.",
     outcome_break, outcome_real),
    ("F-CEN-HOLD", "the retest-hold detector on the FIVE R1 BANDS at the TUNED pins — a "
     "failed hold must FAIL",
     "the detector's rows differ from a plain walk (own EMA, own ATR) for any macro DIE on any "
     "of the five R1 bands; a leash flip does not hold, or a 'failed through' does not fail, "
     "on the raw bars; a filed flip-hold is anchored anywhere but touch + FLIP_HOLD_BARS, or a "
     "filed retest-hold anywhere but touch + the TUNED hold_bars.",
     hold_break, hold_real),
    ("F-C10-TUNE", "the R1 hold-pin tuning — whole grid, tuning era only, the printed rule",
     "the tuning grid is not the whole 5 bands x 3 margins x 3 holds, once each; an "
     "ineligible cell carries no reason; the objective is not (median term - toll); tune() "
     "accepts a tape that reaches past 2024-06-30T23:59:59Z; a COPY whose HOLDOUT-era bars "
     "carry a planted 5x edge moves the grid sha or any field of the result; the selected "
     "cell is not this file's own application of the printed tie-break to the printed grid "
     "(on the stand-in grid or on the FILED 5m grid); the census's RETEST_PINS are not the "
     "filed TUNING_RESULT.json's.",
     tune_break, tune_real),
    ("F-C10-ACC", "[Q-R4] the four acceptance operationalisations head-to-head beside the "
     "RangeFinder DIE rule — the data's default NAMED, nothing promoted [LEDGER.md:835]",
     "the filed grid is not the whole declared grid, or its key repeats; a row's "
     "acceptance_law_sha is not the live law's, or an acceptance DEFINITION is edited "
     "without the sha moving; a variant's N is edited and the filed declaration count "
     "still stands; the engine default BREAK_CONFIRM_N/BREAK_MARGIN MOVES (a promotion); "
     "time_beyond_T is typed rather than READ from RC.PINS['DEV_RETURN_BARS']; the five "
     "rules are given different n_episodes so the head-to-head is not like-for-like; the "
     "DIE rule declares on an episode that did not die; the episode replay is not the "
     "machine's own breakout-die log, bar for bar ON EVERY CELL THIS LEG RE-WALKS LIVE; "
     "the FILED per-cell replay ledger disagrees with that live re-walk in the die "
     "count, the episode count, the confirmed-range count, the in-range bar count or the "
     "sha over the machine's (bar, rid, side, cause, closes) die tuples; that ledger's "
     "per-cell counts do not sum to the build's own grand totals, or name a different "
     "number of cells. NOT ASSERTED, BECAUSE IT CANNOT GO RED: the manifest's "
     "die_machine == die_matched, which the build increments only after its own HALT has "
     "forced the equality [review 2026-09-22, finding 3].",
     acc_break, acc_real),
    ("F-C10-HT", "[Q-R3] height-vs-toll feasibility + the EDGE-FADE outcome leg — a GATE, "
     "and the BRK track's READ INTERFACE [LEDGER.md:834]",
     "a filed grid is not whole (cells AND both margins); a filed gate_height_pass or "
     "gate_edge_fade_pass is not the declared arithmetic on its own row; either gate "
     "PASSES below its declared sample floor; the filed `provisional` is not lean C-g's "
     "law, or a provisional row carries verdict_pass; the gate THRESHOLD or the SAMPLE "
     "FLOOR is changed without the filed verdicts disagreeing; the edge floor counted in "
     "BARS moves no filed verdict (the range floor would then be decoration); a row's "
     "gate_law_sha is not the live law's; a verdict is not the conjunction of its two "
     "gates; the height/toll ratio is not ATR-free; A FILED MARGIN ROW IS NOT THE RAW "
     "STATISTIC A LIVE RE-WALK COMPUTES, or is indistinguishable from the weighted mean "
     "of its own cells, or the near-edge/ALL-ages margin is not bit-identical to the "
     "verdict row's edge statistic; a verdict is READ BEFORE IT IS FILED and a default is "
     "returned instead of a HALT; a PROVISIONAL verdict is served on the default read "
     "path; the read interface disagrees with the filed row.",
     ht_break, ht_real),
    ("F-C10-HT-ERA", "[Q-R3] THE VERDICT GRID IS KEYED ON THE ERA — 360 rows, three per "
     "panel, each judged WITHIN its own era [LEDGER.md:834 · LEAN R3-f]",
     "the filed verdict table is not the whole declared grid on the era axis (fewer "
     "than panels x lenses x scale kinds x 3 rows, a repeated key, a panel missing an "
     "era); a verdict row carries no era, or an undeclared one, or the table has no "
     "`era` column at all and the read interface serves it instead of HALTing; a filed "
     "verdict, height leg, edge leg, n_ranges, edge_n, edge_n_ranges or edge NET is not "
     "its OWN era's — recomputed on every row from the filed height row and the filed "
     "near-edge MARGIN row of the same era, and re-walked LIVE per era on a real cell; "
     "a verdict is recomputed for one era from ANOTHER era's inputs without a HALT; the "
     "provisional floor is inherited from ALL instead of applied within the era; the "
     "three eras PASS on exactly the same rows (the split would then be decoration); "
     "the read interface does not take an era, does not state the era it judged on, "
     "serves an era the census never filed, or serves a row provisional in the era "
     "asked for; the digest's §B.3 per-era PASS counts, its count of era-dependent "
     "rows or the nets on the panels it names disagree with the filed table, or it "
     "still carries the unqualified bold headline about POOLED:ALL.",
     ht_era_break, ht_era_real),
    ("F-C10-COLLAR", "P-BRK-S1's scoring ground is FILED and never PRINTED [LAW 4 + R1]",
     "print_report emits a 5m retest-hold row outside the tuning era; the filed `printable` "
     "column disagrees with the declared law on any row; a six-decimal figure carried by a "
     "collared row appears in any .md / .txt / .json artifact under the census root.",
     collar_break, collar_real),
    ("F-GRID", "every grid whole — declared vs filed, NaN with reasons, collared, stamped",
     "a declared cell is missing, undeclared or repeated in any filed table; a NaN statistic "
     "has no reason or a finite one has; a row is not what the FILED ledgers re-derive; the "
     "SCALE grid is not the 11 declared cells with exactly one pick = the nearest density "
     "under the printed tie-break; a collar or as-of column is missing or null; a verdict "
     "column exists; a provisional-pins row says frozen; F-KEY totality fails on the root.",
     grid_break, grid_real),
    ("F-C10-TOLL", "(groundwork) the toll is READ from the grid — never typed",
     "get_toll returns anything but the filed grid's number; that number differs from the "
     "toll re-derived from raw bars + filed anchors + the estate fee object; a NaN toll is "
     "handed back instead of a HALT; a numeric literal sits in a toll position in "
     "scripts/tierc10_census.py.",
     toll_break, toll_real),
    ("F-DET", "same input, same bytes — across processes and hash seeds; resume is honest",
     "two subprocess builds under different PYTHONHASHSEED differ in any file's bytes or any "
     "table's content sha; a rebuild into a current root recomputes; resume trusts an edited "
     "table; any artifact carries a wall-clock field.",
     det_break, det_real),
)


def main() -> int:
    want = [a.lower().replace("_", "-") for a in sys.argv[1:]
            if not a.startswith("--root=") and a != "--slow"]
    legs = [x for x in LEGS if not want or any(w in x[0].lower() for w in want)]
    man = manifest()
    say(f"as_of_last_closed_4h: {man['as_of']}")
    say("=" * 78)
    say("TIER-C10 STAGE 0b · CENSUS-R FIXTURES — break leg first, RED or void")
    say("=" * 78)
    say(f"seed {SEED} · substrate NAIAD_CACHE_DIR={os.environ.get('NAIAD_CACHE_DIR')}")
    say(f"census root {rel(CROOT)} · commission {man['commission']['label']}: "
        f"{man['commission']['assets']} x {man['commission']['lenses']} x "
        f"{man['commission']['scale_kinds']} · is_the_contract_grid = "
        f"{man['commission']['is_the_contract_grid']}")
    say(f"  {C.TIER}")
    say(f"  engine scripts/tierc10_census.py + port: code sha {C.code_sha()}")
    for src, s in sorted(man["input_sha"].items()):
        say(f"  input {src:28} sha256 {s[:16]}…")
    for ln in C.LEANS:
        say(ln)
    for fid, title, fails_if, b, r in legs:
        t0 = time.perf_counter()
        prove(fid, title, fails_if, b, r)
        clock(f"{fid}: {time.perf_counter() - t0:.1f}s")
    say(f"\nTIER-C10 CENSUS-R FIXTURES: {len(RFX.PASSED)}/{len(legs)} GREEN"
        + (f" · FAILED: {RFX.FAILED}" if RFX.FAILED else ""))
    say("warranty: these lines are true AS OF the substrate, the census root and the bars named "
        "above and of no other; the corridor advances with the cache [TC6V-a]")
    if not want:                       # a partial run never overwrites the full transcript
        (CROOT / "FIXTURES_CENSUS.txt").write_text("\n".join(RFX.T) + "\n", encoding="utf-8")
        print(f"transcript -> {rel(CROOT / 'FIXTURES_CENSUS.txt')}")
    if RFX.FAILED:
        print("*** HALT: fixture mismatch. Nothing downstream is trustworthy. ***")
    return 1 if RFX.FAILED else 0


if __name__ == "__main__":
    raise SystemExit(main())
