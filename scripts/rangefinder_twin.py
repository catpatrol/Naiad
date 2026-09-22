#!/usr/bin/env python
"""SS12-RANGEFINDER v1 · the PYTHON TWIN — the operator's grammar.

QUEUE RF-2 (v1) atop RF-1 v2, drafted ARGUS 2026-08-22, ratified by firing
("ok, make it better"). DISPLAY-ONLY:
this module renders and measures; it rules NOTHING and no decision path may
import it. RECONSTRUCTION, NOT CODE ACCESS: the semantics are rebuilt from
the public artifacts of a closed-source system (@sergio_tesla_, 2026-08-10
post + two screenshots). Hypotheses route to APOLLO under G-7.

THE LIFT [OR-1 STEP D, 2026-09-21]: the pure machine — ATR_LEN, PINS,
V2_WINDOW_BARS, MEM_CAP_PER_SIDE, PINS_V2, Range, run_machine, _span,
_span_at, containment, flips_and_leash, run_v2 — now lives in
engine/rangefinder.py, moved VERBATIM with every event log BYTE-IDENTICAL
(gate G-5: the five event shas and both exports of record re-measured equal
on the frozen tape, before and after). THE PINNED READINGS moved with the
machine they govern — read them in that file's header. This file is the THIN
CALLER that remains: the cache loaders, the KEY-A/B/C tables, scoring,
calibration, the exports of record and the CLI. Every name the fixtures and
the pine-sim read (RF.PINS, RF.PINS_V2, RF.run_machine, RF.run_v2,
RF._span_at, RF.flips_and_leash, T.MEM_CAP_PER_SIDE, Range …) is re-exported
here, unchanged in meaning.

ONE SEMANTICS, TWIN AND PINE — the .pine port must implement exactly the
machine in engine/rangefinder.py; F-RF-5 pins its input defaults to the
calibrated pins.

Cache-only, no network. Run: ~/venvs/naiad/bin/python scripts/rangefinder_twin.py
        (--calibrate for the grid; default runs the calibrated pins)
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
from dataclasses import asdict
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from engine import rangefinder as _core                              # noqa: E402
from engine.data import cache_dir                                    # noqa: E402
# THE MACHINE, re-exported [OR-1 lift]. These are the SAME objects the core
# holds (PINS and PINS_V2 are one dict each, not copies), so RF.PINS[...] in
# a fixture and PINS inside run_v2 can never disagree. flips_and_leash and
# run_v2 are NOT in this list on purpose — see their wrappers in the v2
# section below [TRAP 1].
from engine.rangefinder import (                                     # noqa: E402,F401
    ATR_LEN,               # house pin, never swept
    PINS,                  # THE CALIBRATED PINS [VETO] — F-RF-5 pins the pine
    PINS_V2,               # v2 calibration of record (KEY-C)
    V2_WINDOW_BARS,        # 4h bars; the Jan shelf forms inside [C-R3]
    MEM_CAP_PER_SIDE,      # H3, commissioned — THIS module's own global:
                           # F-RF-10's break leg patches it HERE
    Range, run_machine, _span, _span_at, containment, tape_from_klines,
)

OUT = ROOT / "research_outputs" / "rangefinder"
WINDOW_BARS = 420          # covers KEY-B's Jul-2025 opening [C6, disclosed]


# ═══════════════════════════════════════════════════ the tape, cache-only
# THE RECORD ANCHOR [TIER-C10 Stage 0a]. Both loaders read tail(N) of a LIVE
# parquet, and every record the fixtures hold — KEY-A's 71.19 / 7.78 / 1.19 /
# 68.2, KEY-B, KEY-C, the five event shas in engine/rangefinder.py — was
# measured on ONE window: the 4h tape whose last bar OPENS 2026-08-22T04:00Z.
# That is the v2 export's own window.end (1700 bars from 2025-11-12T00:00),
# and cut there the 1D resample ends 2026-08-21 (Aug 22 holds two 4h bars and
# is dropped as incomplete) — the v1 export's window.end, 420 days from
# 2025-06-28, "dropped_incomplete_days": 2. As the tail slid, four fixtures
# went RED on a machine that had not moved; the fixtures lacked an as-of.
# [LEAN-HEPHAESTUS] anchor_ms DEFAULTS TO None = the live tail, so every
# caller that is not a fixture (this CLI, the pine-sim run standalone,
# calibrate / calibrate_v2 by import) behaves exactly as before; the two
# fixture suites pass RECORD_ANCHOR_MS and ride the window of record. The cut
# is applied BEFORE tail(N): the records depend on the window START as much as
# its end (ATR seed, the visible-left shelf).
RECORD_ANCHOR_MS = 1_787_371_200_000       # 2026-08-22T04:00Z, a bar OPEN


def daily_bars(anchor_ms: int | None = None) -> pd.DataFrame:
    """BTCUSDT 4h → 1D UTC, COMPLETE days only (six 4h bars — the AN-2
    head-bucket law applied at birth rather than repaired later); the true
    window is printed, never assumed. anchor_ms keeps only 4h bars whose
    open_time <= anchor_ms (None = live)."""
    f = pd.read_parquet(cache_dir() / "klines" / "BTCUSDT_4h.parquet")
    if anchor_ms is not None:
        f = f[f["open_time"] <= int(anchor_ms)].copy()
    f["day"] = f["open_time"] // 86_400_000
    g = f.groupby("day").agg(n=("open_time", "size"), o=("open", "first"),
                             h=("high", "max"), l=("low", "min"),
                             c=("close", "last"), t0=("open_time", "first"))
    dropped = int((g["n"] != 6).sum())
    d = g[g["n"] == 6].tail(WINDOW_BARS).reset_index(drop=True)
    d["ts"] = pd.to_datetime(d["t0"], unit="ms", utc=True).dt.strftime(
        "%Y-%m-%d")
    d.attrs["dropped_incomplete_days"] = dropped
    return d


# ═════════════════════════ STEP 2c · CALIBRATION — KEY-A · VERIFY — KEY-B
# KEY-A: the reference's published statistics (unchanged from RF-1).
# KEY-B: the operator's chart transcription (BTCUSDT.P 1D; our tape is
# BTCUSDT SPOT resampled 4h→1D — a DISCLOSED feed divergence inside the
# ±1,500 USD transcription tolerance).  Calibrate on A; VERIFY on B; a
# divergence IS the finding, never forced.
TARGETS_Q = {
    "Q1_coverage": (80.6, 8.0, 3.0),          # (center, halfband, weight)
    "Q2_pivot_per_bars": (28.5, 8.55, 2.0),    # 27–30 ±30%
    "Q3_conf_per_100": (0.75, 0.375, 1.0),
    "Q4_lifetime": (102.5, 51.5, 1.0),         # 85–110 ±40% → [51, 154]
}

# KEY-B, transcription-grade: (name, from, to, top, bottom, deviations)
# each deviation carries the transcription's own DATE ANCHOR [review: a
# first-hit matcher credited the Oct ATH spike to a July inception event —
# the verdicts survived but the evidence pointers lied]
KEY_B = [
    ("L-R1", "2025-07-01", "2025-11-20", 124_200.0, 100_300.0,
     [("top", 124_000.0, 128_000.0, "2025-10-07"),
      ("bottom", 100_000.0, 107_000.0, "2025-10-10")]),
    ("L-R2", "2025-11-20", "2026-02-10", 96_200.0, 84_600.0,
     [("top", 96_000.0, 99_300.0, "2026-01-15"),
      ("bottom", 83_000.0, 86_500.0, "2025-12-15")]),
    ("L-R3", "2026-02-10", "2026-05-31", 80_100.0, 60_800.0,
     [("bottom", 57_900.0, 62_000.0, "2026-02-20"),
      ("top", 78_000.0, 81_000.0, "2026-05-15")]),
    ("L-R4", "2026-06-01", "2026-08-22", 67_400.0, 60_100.0,
     [("bottom", 57_600.0, 60_300.0, "2026-07-02")]),
]
KEY_B_TOL_USD = 1_500.0
KEY_B_TOL_BARS = 6

# ONE_ACTIVE is PINNED by the v0 calibration of record (multi lost in the
# RF-1 grid); v1 sweeps the six numeric pins in BODY mode [C6].
GRID_COARSE = {
    "LEG_MIN": [0.25, 0.5, 1.0, 1.5],
    "REV_MIN": [1.5, 2.0, 2.5, 3.0, 3.5],
    "TOUCH_EPS": [0.0, 0.15, 0.30, 0.50],
    "DEV_RETURN_BARS": [3, 5, 8, 13],
    "BREAK_CONFIRM_N": [2, 3, 5, 8],
    "BREAK_MARGIN": [1.0, 1.5, 2.0, 3.0],
}


def score(m: dict, d: pd.DataFrame) -> tuple[float, dict]:
    """KEY-A only — the calibration objective (v1)."""
    res = {}
    vals = {
        "Q1_coverage": m["coverage_pct"],
        "Q2_pivot_per_bars": (m["n_bars"] / m["n_pivots"]
                              if m["n_pivots"] else 1e9),
        "Q3_conf_per_100": 100.0 * m["n_confirmed"] / m["n_bars"],
        "Q4_lifetime": (m["mean_confirmed_lifetime"]
                        if m["mean_confirmed_lifetime"] else 0.0),
    }
    s = 0.0
    for k, (c0, hb, w) in TARGETS_Q.items():
        v = vals[k]
        viol = max(0.0, abs(v - c0) - hb) / hb
        res[k] = {"value": round(float(v), 2),
                  "band": [round(c0 - hb, 2), round(c0 + hb, 2)],
                  "violation": round(float(viol), 4)}
        s += w * viol
    return round(s, 4), res


def _bar_of(d: pd.DataFrame, iso_date: str) -> int:
    ts = d["ts"].tolist()
    for i, t in enumerate(ts):
        if t >= iso_date:
            return i
    return len(d) - 1


def verify_key_b(m: dict, d: pd.DataFrame) -> list[dict]:
    """One row per L-R target: the matched range (largest bar-overlap with
    the target window), boundary residuals against the transcription, and
    each transcribed deviation found-or-not (a harden OR an
    inception-deviation on the given side whose extreme falls inside the
    transcribed band ±1,500, within the window ±6 bars)."""
    n = m["n_bars"]
    rows = []
    conf = [r for r in m["ranges"] if r.confirm_i >= 0]
    for name, a, b, top_t, bot_t, devs in KEY_B:
        ia, ib = _bar_of(d, a), _bar_of(d, b)
        best, best_ov = None, 0
        for r in conf:
            lo_r = r.confirm_i
            hi_r = r.die_i if r.die_i >= 0 else n - 1
            ov = max(0, min(ib, hi_r) - max(ia, lo_r))
            if ov > best_ov:
                best, best_ov = r, ov
        row = {"target": name, "window": f"{a}→{b}",
               "target_top": top_t, "target_bottom": bot_t,
               "matched_rid": best.rid if best else None,
               "overlap_bars": best_ov}
        if best:
            # THE TRANSCRIPTION'S OBJECT IS THE BOX [operator grammar]: the
            # range numbers on his chart are the BODY-cluster boundaries;
            # the zones beyond carry the extremes.  So the box basis
            # (top0/bottom0, pre-redraw) is the comparison of record; the
            # redrawn extent prints beside it — two bases, both shown,
            # neither shopped.
            row.update({
                "box_top": round(float(best.top0), 1),
                "box_bottom": round(float(best.bottom0), 1),
                "redrawn_top": round(float(best.top), 1),
                "redrawn_bottom": round(float(best.bottom), 1),
                "top_residual_usd": round(abs(best.top0 - top_t), 1),
                "bottom_residual_usd": round(abs(best.bottom0 - bot_t), 1),
                "top_within_tol": bool(abs(best.top0 - top_t)
                                       <= KEY_B_TOL_USD),
                "bottom_within_tol": bool(abs(best.bottom0 - bot_t)
                                          <= KEY_B_TOL_USD),
            })
            for side, lo_d, hi_d, anchor in devs:
                anchor_i = _bar_of(d, anchor)
                cands = [e for e in m["events"]
                         if e["event"] in ("harden", "inception-deviation")
                         and e.get("rid") == best.rid
                         and e.get("side") == side
                         and ia - KEY_B_TOL_BARS <= e["i"]
                         <= ib + KEY_B_TOL_BARS
                         and lo_d - KEY_B_TOL_USD <= e["extreme"]
                         <= hi_d + KEY_B_TOL_USD]
                hit = (min(cands, key=lambda e: abs(e["i"] - anchor_i))
                       if cands else None)
                key = f"dev_{side}_{int(lo_d / 1000)}k"
                row[key] = (f"FOUND@{hit['ts']} ext {hit['extreme']:.0f} "
                            f"({hit['event']})" if hit else "NOT FOUND")
                row[key + "_found"] = bool(hit)
        rows.append(row)
    return rows


def calibrate(d: pd.DataFrame, verbose: bool = True):
    """Coarse-then-fine over the six free pins.  If nothing satisfies
    Q-1..Q-5, the best three sets print WITH the resisting target — that
    names the wrong rule; it is not forced."""
    import itertools
    keys = list(GRID_COARSE)
    rows = []
    for combo in itertools.product(*(GRID_COARSE[k] for k in keys)):
        pins = dict(zip(keys, combo))
        m = run_machine(d, pins)
        s, res = score(m, d)
        rows.append((s, pins, res, m["status_line"]))
    # DETERMINISTIC TIE-BREAK, disclosed: equal scores prefer FEWER
    # grid-edge pins (an edge choice is a truncated search wearing a
    # winner's name), then lexicographic pins.
    def _edges(p):
        e = 0
        for k, ax in GRID_COARSE.items():
            if isinstance(ax[0], (int, float)) and len(ax) > 1:
                if p[k] <= min(ax) or p[k] >= max(ax):
                    e += 1
        return e
    rows.sort(key=lambda r: (r[0], _edges(r[1]),
                             tuple(sorted(r[1].items()))))
    best = rows[0]
    # fine pass around the winner: ±one half-step per continuous pin
    fine_axes = {
        "LEG_MIN": [max(0.25, best[1]["LEG_MIN"] - 0.25),
                    best[1]["LEG_MIN"], best[1]["LEG_MIN"] + 0.25],
        "REV_MIN": [max(1.0, best[1]["REV_MIN"] - 0.25),
                    best[1]["REV_MIN"], best[1]["REV_MIN"] + 0.25],
        "TOUCH_EPS": [max(0.0, best[1]["TOUCH_EPS"] - 0.1),
                      best[1]["TOUCH_EPS"], best[1]["TOUCH_EPS"] + 0.1],
        "DEV_RETURN_BARS": sorted({max(1, best[1]["DEV_RETURN_BARS"] - 1),
                                   best[1]["DEV_RETURN_BARS"],
                                   best[1]["DEV_RETURN_BARS"] + 1}),
        "BREAK_CONFIRM_N": sorted({max(2, best[1]["BREAK_CONFIRM_N"] - 1),
                                   best[1]["BREAK_CONFIRM_N"],
                                   best[1]["BREAK_CONFIRM_N"] + 1}),
        "BREAK_MARGIN": [max(0.5, best[1]["BREAK_MARGIN"] - 0.25),
                         best[1]["BREAK_MARGIN"],
                         best[1]["BREAK_MARGIN"] + 0.25],
    }
    for combo in itertools.product(*(fine_axes[k] for k in keys)):
        pins = dict(zip(keys, combo), BOUNDARY_MODE="body", MULTI_ACTIVE=0)
        m = run_machine(d, pins)
        s, res = score(m, d)
        rows.append((s, pins, res, m["status_line"]))
    rows.sort(key=lambda r: (r[0], _edges(r[1]),
                             tuple(sorted(r[1].items()))))
    if verbose:
        print(f"\nCALIBRATION SCOREBOARD (coarse {len(list(__import__('itertools').product(*(GRID_COARSE[k] for k in keys))))} + fine) — top 5 of {len(rows)}:")
        for s, pins, res, sl in rows[:5]:
            print(f"  score {s:7.4f}  {pins}")
            print(f"          {sl}")
        s0, p0, r0, _ = rows[0]
        print("\nCHOSEN SET:", p0)
        print("RESIDUALS:")
        for k, v in r0.items():
            print(f"  {k:32} {v}")
        hardq = [k for k, v in r0.items()
                 if k.startswith("Q") and isinstance(v.get("violation"), float)
                 and v["violation"] > 0]
        if hardq:
            print(f"\nRESISTING TARGET(S): {hardq} — the rule they lean on "
                  f"is the suspect; NOT forced. Best three sets above.")
        else:
            print("\nKEY-A (Q-1..Q-4) all satisfied by the chosen set.")
    return rows


# ═══════════════════════════════════════════════════ STEP 2d · EXPORT
def export(d: pd.DataFrame, pins: dict) -> Path:
    """v1: BOTH modes ridden, BOTH keys scored, one artifact."""
    OUT.mkdir(parents=True, exist_ok=True)
    p = OUT / "BTCUSD_1d_ranges_v1.json"
    modes = {}
    for mode in ("body", "wick"):
        mp = dict(pins, BOUNDARY_MODE=mode)
        m = run_machine(d, mp)
        _, res_a = score(m, d)
        modes[mode] = {
            "status_line": m["status_line"],
            "coverage_pct": m["coverage_pct"],
            "key_a_residuals": res_a,
            "key_b": verify_key_b(m, d),
            "events": m["events"],
            "ranges": [asdict(r) for r in m["ranges"]],
        }
    payload = {
        "source": "SS12-RangeFinder v1 twin — the operator's grammar atop "
                  "the v0 reconstruction (@sergio_tesla_); display-only",
        "window": {"start": d["ts"].iloc[0], "end": d["ts"].iloc[-1],
                   "bars": int(len(d)),
                   "dropped_incomplete_days":
                       int(d.attrs["dropped_incomplete_days"])},
        "pins": pins, "atr_len": ATR_LEN,
        "modes": modes,
    }
    txt = json.dumps(payload, indent=1, default=str)
    txt = txt.replace(": NaN", ": null")     # strict JSON [review]
    p.write_text(txt)
    return p


def main() -> int:
    d = daily_bars()
    print(f"WINDOW: {d['ts'].iloc[0]} → {d['ts'].iloc[-1]}  ({len(d)} bars; "
          f"{d.attrs['dropped_incomplete_days']} incomplete day(s) dropped "
          f"at resample)")
    if "--calibrate" in sys.argv:
        rows = calibrate(d)
        return 0
    for mode in ("body", "wick"):
        m = run_machine(d, dict(PINS, BOUNDARY_MODE=mode))
        _, res = score(m, d)
        print(f"\n═══ MODE {mode.upper()} ═══")
        print(m["status_line"])
        print("KEY-A RESIDUALS:", json.dumps(res, default=str))
        print("RANGE TABLE:")
        for r in m["ranges"]:
            if r.confirm_i >= 0:
                print(f"  #{r.rid} {r.state:10} conf@{r.confirm_i} "
                      f"die@{r.die_i} [{r.bottom:.0f} … {r.top:.0f}] "
                      f"dev n={r.n_deviations} incept={r.n_inception_zones} "
                      f"born@{r.born_at}<-{r.backdated_from}")
        print("KEY-B CONCORDANCE:")
        for row in verify_key_b(m, d):
            print("  " + json.dumps(row, default=str))
        if mode == "body":
            print("\nBODY EVENT LOG (lifecycle only):")
            for e in m["events"]:
                if e["event"] != "pivot":
                    print("  " + json.dumps(e))
    p = export(d, PINS)
    sha = hashlib.sha256(p.read_bytes()).hexdigest()
    print(f"\nEXPORT {p}  {p.stat().st_size:,} B  sha256 {sha[:16]}…")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


# ═══════════════════════════ v2 · HIERARCHY + FLIPS + THE LEASH [RF-3]
# The v2 PINNED READINGS (CONTAINMENT [H1] · FLIP [H2] · LEASH [H3] · TTL
# DEFAULT), the v2 pins and the laws themselves moved to engine/rangefinder.py
# at OR-1, verbatim. What stays here: the 4h loader, the two thin wrappers
# below, KEY-C, calibration and the v2 export of record.


def bars_4h(n_bars: int = V2_WINDOW_BARS,
            anchor_ms: int | None = None) -> pd.DataFrame:
    """The raw 4h tape, no resample — KEY-C is a 4h transcription.
    anchor_ms keeps only bars whose open_time <= anchor_ms, THEN takes the
    last n_bars (None = live) [RECORD_ANCHOR_MS, above]."""
    f = pd.read_parquet(cache_dir() / "klines" / "BTCUSDT_4h.parquet")
    if anchor_ms is not None:
        f = f[f["open_time"] <= int(anchor_ms)]
    # the rename/ts step lives in the core now (the Oracle needs it without
    # the IO); one body, so the twin's tape and the Oracle's cannot drift
    return tape_from_klines(f, n_bars)


# TRAP 1 [OR-1 lift] — WHY THESE TWO ARE WRAPPERS AND NOT RE-EXPORTS.
# F-RF-10's break leg raises the leash cap SILENTLY by monkeypatching
# rangefinder_twin.MEM_CAP_PER_SIDE = 99 and then calls the twin's
# flips_and_leash; the fixture is green only if that patch BITES (ten
# synthetic corpses, > 6 live lines per side). The law now lives in
# engine.rangefinder and reads ITS OWN constant, so a plain re-export would
# leave the patch inert, the break leg green, the fixture void. Each wrapper
# therefore reads THIS module's global AT CALL TIME and hands it to the core
# (whose keyword defaults to its own constant). run_v2 is wrapped for the
# same reason: before the lift a patched cap governed everything the twin
# ran, and export_v2 prints this same global as "mem_cap_per_side" — the
# number exported and the number enforced must stay one number.
def flips_and_leash(macro: dict, d: pd.DataFrame, pins: dict) -> list[dict]:
    """[H2+H3] engine.rangefinder.flips_and_leash under the TWIN's cap."""
    return _core.flips_and_leash(macro, d, pins, mem_cap=MEM_CAP_PER_SIDE)


def run_v2(d: pd.DataFrame, pins_v2: dict) -> dict:
    """engine.rangefinder.run_v2 under the TWIN's cap."""
    return _core.run_v2(d, pins_v2, mem_cap=MEM_CAP_PER_SIDE)


# ═══════════════════════════════════ v2 · KEY-C VERIFY + CALIBRATE
KEY_C_TOL_USD = 1_200.0
KEY_C_TOL_BARS = 8

KEY_C_RANGES = [
    # (name, window_a, window_b, top, bottom, midline, devs)
    ("C-R1", "2026-02-01", "2026-05-31", 75_000.0, 59_900.0, 66_500.0,
     [("bottom", 57_900.0, 62_000.0, "2026-02-20"),
      ("top", 75_000.0, 78_500.0, "2026-04-15")]),
    ("C-R2", "2026-06-01", "2026-08-22", 67_300.0, 59_900.0, None,
     [("bottom", 57_600.0, 60_300.0, "2026-07-02")]),
    ("C-R3", "2025-12-01", "2026-02-05", None, 84_500.0, None,
     [("top", 95_000.0, 97_500.0, "2026-01-05")]),
]
KEY_C_FLIPS = [
    ("C-F1", "resistance", 84_500.0, 1_500.0, "2026-02-01"),
    ("C-F2", "support", 75_000.0, 1_200.0, "2026-05-15"),
]


def verify_key_c(v2: dict, d: pd.DataFrame) -> list[dict]:
    ts = d["ts"].tolist()
    n = len(d)

    def bar_of(s):
        for i, t in enumerate(ts):
            if t >= s:
                return i
        return n - 1
    rows = []
    macro = v2["macro"]
    conf = [r for r in macro["ranges"] if r.confirm_i >= 0]
    for name, a, b, top_t, bot_t, mid_t, devs in KEY_C_RANGES:
        ia, ib = bar_of(a), bar_of(b)
        best, best_ov = None, 0
        for r in conf:
            hi_r = r.die_i if r.die_i >= 0 else n - 1
            ov = max(0, min(ib, hi_r) - max(ia, r.confirm_i))
            if ov > best_ov:
                best, best_ov = r, ov
        row = {"target": name, "matched_rid": best.rid if best else None,
               "overlap_bars": best_ov}
        if best:
            # the RF-2 finding carried: the operator's numbers track the
            # REDRAWN extent — both bases print, redrawn is the comparison
            for label, t_val, got_box, got_rd in (
                    ("top", top_t, best.top0, best.top),
                    ("bottom", bot_t, best.bottom0, best.bottom)):
                if t_val is None:
                    continue
                row[f"{label}_redrawn"] = round(float(got_rd), 1)
                row[f"{label}_box"] = round(float(got_box), 1)
                row[f"{label}_residual"] = round(abs(got_rd - t_val), 1)
                row[f"{label}_within"] = bool(abs(got_rd - t_val)
                                              <= KEY_C_TOL_USD)
            if mid_t is not None:
                mid = (best.top + best.bottom) / 2
                row["mid_residual"] = round(abs(mid - mid_t), 1)
                row["mid_within"] = bool(abs(mid - mid_t) <= KEY_C_TOL_USD)
            for side, lo_d, hi_d, anchor in devs:
                ai = bar_of(anchor)
                cands = [e for e in macro["events"]
                         if e["event"] in ("harden", "inception-deviation")
                         and e.get("rid") == best.rid
                         and e.get("side") == side
                         and lo_d - KEY_C_TOL_USD <= e["extreme"]
                         <= hi_d + KEY_C_TOL_USD]
                hit = (min(cands, key=lambda e: abs(e["i"] - ai))
                       if cands else None)
                key = f"dev_{side}_{int(lo_d / 1000)}k"
                row[key] = (f"FOUND@{hit['ts']} ext {hit['extreme']:.0f} "
                            f"({hit['event']})" if hit else "NOT FOUND")
                row[key + "_found"] = bool(hit)
        rows.append(row)
    for name, pol, px_t, tol, anchor in KEY_C_FLIPS:
        ai = bar_of(anchor)
        cands = [e for e in v2["flips"]
                 if e["polarity"] == pol and abs(e["px"] - px_t) <= tol]
        hit = min(cands, key=lambda e: abs(e["i"] - ai)) if cands else None
        in_time = bool(hit and abs(hit["i"] - ai) <= 180)  # ~30d of 4h
        # bars; computed-not-asserted [disclosed]: the April flip + May
        # flip-retests is the accepted C-F2 reading
        rows.append({"target": name, "polarity": pol, "line": px_t,
                     "found": (f"{hit['glyph']}@{hit['ts']} px {hit['px']}"
                               if hit else "NOT FOUND"),
                     "found_flag": bool(hit),
                     "near_anchor": in_time})
    rows.append({"target": "C-Q1",
                 "macro_confirms_feb_aug": v2["macro_count_feb_aug"],
                 "within_2_4": bool(2 <= v2["macro_count_feb_aug"] <= 4)})
    return rows


def score_key_c(v2: dict, d: pd.DataFrame) -> tuple[float, list]:
    rows = verify_key_c(v2, d)
    s = 0.0
    for row in rows:
        t = row["target"]
        if t.startswith("C-R"):
            if row.get("matched_rid") is None:
                s += 5.0
                continue
            for k, v in row.items():
                if k.endswith("_residual") and v is not None:
                    s += max(0.0, v - KEY_C_TOL_USD) / KEY_C_TOL_USD
                if k.endswith("_found") and not v:
                    s += 1.0
        elif t.startswith("C-F"):
            if not row["found_flag"]:
                s += 3.0
        elif t == "C-Q1" and not row["within_2_4"]:
            s += 3.0
    return round(s, 4), rows


def calibrate_v2(d: pd.DataFrame):
    """Fit ONLY the four v2 pins (TTL adopted at the proposed 400 — no
    KEY-C row constrains it, disclosed); micro pins FROZEN."""
    import itertools
    grid = {"SCALE_MULT": [2.5, 3.0, 3.5, 4.0],
            "FLIP_HOLD_MARGIN": [0.25, 0.5, 1.0],
            "FLIP_HOLD_BARS": [6, 12, 18]}
    rows = []
    for combo in itertools.product(*grid.values()):
        pins = dict(zip(grid, combo), MEM_TTL_BARS=400)
        v2 = run_v2(d, pins)
        s, res = score_key_c(v2, d)
        rows.append((s, pins, v2["status_line"]))
    rows.sort(key=lambda r: (r[0], tuple(sorted(r[1].items()))))
    print(f"\nKEY-C SCOREBOARD ({len(rows)} cells) — top 5:")
    for s, pins, sl in rows[:5]:
        print(f"  score {s:7.4f}  {pins}")
        print(f"          {sl}")
    s0, p0, _ = rows[0]
    print("\nCHOSEN v2 SET:", p0)
    v2 = run_v2(d, p0)
    _, res = score_key_c(v2, d)
    print("KEY-C RESIDUALS:")
    for row in res:
        print("  " + json.dumps(row, default=str))
    return rows


def export_v2(d: pd.DataFrame, pins_v2: dict) -> Path:
    v2 = run_v2(d, pins_v2)
    _, res = score_key_c(v2, d)
    OUT.mkdir(parents=True, exist_ok=True)
    p = OUT / "BTCUSD_4h_ranges_v2.json"
    payload = {
        "source": "SS12-RangeFinder v2 twin — hierarchy + flips + leash "
                  "(RF-3); display-only",
        "window": {"start": d["ts"].iloc[0], "end": d["ts"].iloc[-1],
                   "bars": int(len(d)), "tf": "4h"},
        "pins_v2": pins_v2, "micro_pins_frozen": PINS,
        "mem_cap_per_side": MEM_CAP_PER_SIDE,
        "status_line": v2["status_line"],
        "key_c": res,
        "flips": v2["flips"], "leash_events": v2["leash"],
        "suppressed_micro": v2["suppressed"],
        "kept_micro": v2["kept"],
        "macro_events": v2["macro"]["events"],
        "macro_ranges": [asdict(r) for r in v2["macro"]["ranges"]],
        "micro_ranges": [asdict(r) for r in v2["micro"]["ranges"]],
    }
    txt = json.dumps(payload, indent=1, default=str)
    txt = txt.replace(": NaN", ": null")
    p.write_text(txt)
    return p
