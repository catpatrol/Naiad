#!/usr/bin/env python
"""TIER-C11 · TC11-RIDE — F-WALK-IDENT · F-RELAY-RIDE · F-EXIT1H · F-MISMATCH-1H ·
F-WARN-BOOK · F-ORDER · F-ADD-ACCT · F-CLOSURE-RIDE · F-DET.  The fixtures of
scripts/tierc11_ride.py (the ride engine: L-W.0, L-W.3, L-W.5, L-A.1, L-H.1, L-T.2,
L-1.5, L-R.5 stamps).

TWO LEGS PER FIXTURE, the BREAK leg first, and it must go RED or the fixture is
VOID — a guard nobody has seen fail is a guard nobody has seen [the prove() law
of scripts/tierc10_rf_fixtures.py / tierc11_env_fixtures.py].  A break leg is a
set of PLANTS judged one at a time; a plant counts as CAUGHT only if a finding
NAMES THE INTENDED DETECTOR (its expected substring).  A plant that crashes is a
FIXTURE DEFECT, never a catch.  A plant is either a corrupted input handed to a
guard, or a MUTATION of the module — a shadow copy of tierc11_ride.py with ONE
named mis-build (`MUTANTS`), loaded under its own module name, under which the
REAL leg's own checks must go RED.  Every plant is made on a COPY; no real
artifact moves.  Every leg prints its own FAILS IF.

  F-WALK-IDENT   REAL: with every hook off and the 1h walk ON, the whole CLASSIC5
                 v6 book equals the v6 control at 0.000e+00 (12 CTRL_COLS, raw),
                 the identity helper finds nothing; planted MISMATCH / SAME-CHILD
                 / LATCH-FIRST / CHILDREN-BELOW bars behave as hand-walked; a Walk
                 OBJECT passed as transform_book(walk=) HALTs.  SABOTAGE: a walk
                 ignoring the mismatch law (x2); LATCH before STOP; a bent unacted
                 net_r; [mutant] the walk-type guard removed.
  F-RELAY-RIDE   REAL (L-T.2 at cardinality): (a) all 200 v6 campaigns re-entered
                 at their 4h close == _ride_leg9 and the v6 Trade; (b) EVERY v6
                 campaign x J in {ti, ti+1, ti+2} x entry at the close of child 0/1/2
                 through relay_entry -> relay_stop -> relay11, against THIS file's
                 hand walk of J (entry price and as-of J-1, the stop as of J-1, a
                 stop inside J, a bell at J, the state after J incl. the harvest
                 armed per close[J-1] and touched on post-entry children, the trail
                 armed iff the latch), and every carried relay whose state after J
                 equals v6's one-bar state continues EXACTLY as tierc9._ride_leg9
                 (GLUE); (c) every (2,2) pivot confirming at a latched relay's J:
                 the trail at J; (d) every split bar m of every v6 campaign: ride11
                 from the injected state after m == the untruncated _ride_leg9.
                 SABOTAGE: a carry dropping reached_1r; [mutants] M1 as-of J, M2
                 harvest armed on close[J], M3 harvest touch on the whole bar, M4
                 trail armed by the parent's high, M8 mae_to_1r past the latch,
                 M11 continuation from J+2, M12 injected stop ignored, M13 no trail
                 at J.
  F-EXIT1H       REAL: every real stop exit (walk ON) resolves at the first 1h
                 child of the exit bar touching the stop in force (own read); bell
                 exits at the 4h close; the L-R.5 stamps (exit, latch) of every
                 campaign; every v6 stop bar planted as a mismatch bar decided by the
                 parent (stamped at its open).  SABOTAGE: resolving at the 4h close;
                 [mutant] M17 a parent-decided stop stamped at the close.
  F-MISMATCH-1H  REAL (L-W.0, 1h-only events on a mismatch bar): (a) a relay
                 entry inside EVERY real corridor mismatch bar (x child 0-2 x both
                 directions) is moved to the parent's close at the parent's close,
                 its stop as of J, refused when that lands on the trigger close, its
                 ride == _ride_leg9 from J and the bar COUNTED; relay11(moved=True)
                 at a walkable bar's close HALTs; (b) on every eligible
                 latched v6 campaign, an add event inside a planted mismatch bar
                 after the latch is admitted at the parent's close and price, booked
                 to a hand calculation; (c) on every eligible latched campaign, a
                 counter cross on its planted-mismatch LATCH bar does not warn, and
                 one on the bar before does (at the parent's close).  SABOTAGE:
                 [mutants] M5 relay not moved, M6 add not moved, M7 warn ignoring
                 the parent's latch, M15 the moved= guard removed.
  F-WARN-BOOK    REAL (L-W.2, L-W.5): warn_of's 12/89 cross arrays == THIS file's
                 plain-loop EMA crosses on every asset; the whole CLASSIC5 warn book
                 == THIS file's hand walk (exit reason / price / instant / bar /
                 stamp; mfe_r, mae_r under the held law) and the identity law.
                 SABOTAGE: [mutants] the default pair 12/26; a walked warn that
                 ignores the +1R latch.
  F-ORDER        REAL: STOP > TP on every eligible v6 stop bar; TP > BELL on every
                 eligible bell bar; guard / unguarded / far side / post-harvest on
                 EVERY bell bar; gap fills at the open on every gap bar; the TP
                 after the harvest (the 0.5 remainder) and before it (the 1.0) booked
                 to a hand calculation, mfe capped at the fill; re-arming across
                 bars on every eligible bar pair; the TP exit INSTANT under the
                 walk on every bell bar, and on each planted as a mismatch bar (the
                 parent's close, stamped at the open); four planted warn cases.  SABOTAGE: TP
                 before STOP; BELL before TP; WARN before LATCH; [mutants] M9 TP
                 instant = the 4h close, M10 post-harvest twin live before the
                 harvest, M14 near side read on close[j], M16 a mismatch-bar TP
                 stamped at the close.
  F-ADD-ACCT     REAL: PLANT A (the D12 ceiling binds) and PLANT B (harvest, flags,
                 twins) booked to a hand calculation; the Δ = add_r + cap-absorbed
                 funding decomposition (AMENDMENT CANDIDATE on L-1.5); prices come
                 from the tape and a differing caller price HALTs.  SABOTAGE: a
                 3rd add; [mutant] the caller's price taken, unchecked.
  F-CLOSURE-RIDE REAL: range-free closure (fresh interpreter + AST), no
                 hook-escaping I/O in tierc11_ride.py's own source, and the ride's
                 data reads observed as `open` audit events on the TC11 snapshot.
                 SABOTAGE: four planted imports / reads; an observer installed
                 after the reads.
  F-DET          REAL: two subprocess emissions of RIDE_PROBE.txt (PYTHONHASHSEED
                 1, 20260924) byte-identical to each other and to this run; the
                 probe carries the hooks-off, walk, warn, TP (synthetic levels),
                 add and relay outputs.  SABOTAGE: a one-byte-bent copy; a
                 hash-order-dependent emission.
BANNED: self-comparison; one example where cardinality was possible; a tuned
magnitude bound standing in for an identity; a check whose claim is not the
design's claim.  FROZEN SUBSTRATE: HALTs unless NAIAD_CACHE_DIR is the TC11
snapshot (tierc11_env's guard).  Seed 20260924.  No registered rule's aggregate is
computed or printed here.  The transcript carries no clock and no temp path.

Run:  export NAIAD_CACHE_DIR=$HOME/.cache/naiad/snapshots/tc11_20260925 PYTHONDONTWRITEBYTECODE=1
      ~/venvs/naiad/bin/python -B scripts/tierc11_ride_fixtures.py \\
          [leg-substring ...] [--refile-transcript] [--root=DIR]
Exit 0 = every leg GREEN, every break RED · 1 = a RED or VOID fixture, a
transcript finding, or a HALT.
"""
from __future__ import annotations

import ast
import copy
import dataclasses
import hashlib
import importlib.util
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
import tierc11_ride as RD                                            # noqa: E402

import numpy as np                                                   # noqa: E402
import pandas as pd                                                  # noqa: E402

TP, T9, T8, T7, RC = E.TP, E.T9, E.T8, E.T7, RD.RC
CARD, ROLES = TP.CONTROL_CARD, T9.V6_ROLES

# ── FIXTURE-TYPED LITERALS: the commission, a second object, never RD's own ──
PIN = 1_790_294_400_000                  # 2026-09-25T00:00:00Z [L-0.1]
SEED = 20260924
DET_SEEDS = (1, SEED)
AS_OF_LINE = "as_of_last_closed_4h: 2026-09-25T00:00:00Z"
SNAP = Path.home() / ".cache" / "naiad" / "snapshots" / "tc11_20260925"
H1, H4 = 3_600_000, 14_400_000
TOL = 1e-9                               # a REPRESENTATION tolerance (be_sequence's law)
CTRL_COLS = ("entry_ms", "exit_ms", "entry_px", "exit_px", "stop_px", "r_dist", "net_r",
             "gross_r", "fee_r", "funding_r", "mfe_r", "n_advances")
BPS_SIDE = 5.0 / 10_000.0                # taker 5 bps per side [L-1.1]
GUARD = 10.0 / 10_000.0                  # the round-trip taker fee [L-H.1 (ii)]
HARVEST_Q = 0.5                          # v6's harvest fraction
CEILING_R = 1.0                          # D12
# v6's role stack and trail law, typed here (the card is checked against them below)
TIDE_F, TIDE_S, WIN_F, WIN_S = 89, 316, 12, 89
BELL_W, BELL_T = f"bell_{WIN_F}_{WIN_S}", f"bell_{TIDE_F}_{TIDE_S}"
RAIL_ATR = 1.0                           # struct_stop_4h rail [L-T.2]
TRAIL_LR = (2, 2)
ANCHOR_KIND, ANCHOR_OFF, MIN_ADV_ATR = "pivot", 0.5, 0.05
HARVEST_MIN_UNIT_R = float("-inf")
WARN_PAIR = (12, 89)                     # L-W.2 / L-W.5: the 1h 12/89 counter cross
WARN_LBL = "warn_1h_12_89"
LIFT = 1e-6                              # a planted mismatch: 1e-6 relative >> REPR_TOL
FORBIDDEN = ("rangefinder", "tierc10_census", "tierc10_stamps", "tierc10_null", "tierc11_nest")
OUT = ROOT / "research_outputs" / "tierc11" / "ride"
RUN_ROOT = OUT
TRANSCRIPT = "FIXTURES_RIDE.txt"
ARTIFACT = "RIDE_PROBE.txt"
PY = sys.executable
RIDE_SRC = ROOT / "scripts" / "tierc11_ride.py"
LINES: list[str] = []
PASSED: list[str] = []
FAILED: list[str] = []
_TMP_RX = re.compile(r"(/private)?/(var/folders|tmp)/[^\s'\"]+")

if tuple(TP.CTRL_COLS) != CTRL_COLS:
    raise SystemExit(f"HALT: TP.CTRL_COLS {TP.CTRL_COLS} is not the typed twelve")
if ((ROLES.tide_f, ROLES.tide_s, ROLES.win_f, ROLES.win_s) != (TIDE_F, TIDE_S, WIN_F, WIN_S)
        or (CARD.trail_l, CARD.trail_r) != TRAIL_LR or CARD.entry_rail_atr != RAIL_ATR
        or CARD.anchor_kind != ANCHOR_KIND or CARD.anchor_offset != ANCHOR_OFF
        or CARD.trail_min_advance_atr != MIN_ADV_ATR or CARD.harvest_frac != HARVEST_Q
        or CARD.harvest_min_unit_r != HARVEST_MIN_UNIT_R or CARD.trail_arm_after_r != 1.0
        or CARD.funding_ceiling_r != CEILING_R):
    raise SystemExit("HALT: the v6 card / roles are not the ones this file types")


def say(line: str = "") -> None:            # deterministic -> transcript
    line = _TMP_RX.sub("<tmp>", line)
    print(line)
    LINES.append(line)


def clock(line: str) -> None:               # wall clock, temp paths -> stdout ONLY
    print(f"  [clock · stdout only] {line}")


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def iso(ms) -> str:
    return T9.iso(int(ms))


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
    """rows = (name, expected detector substring, thunk -> list of findings).
    Judged ONE AT A TIME.  CAUGHT only if a finding names the intended detector.
    No finding = the plant PASSED (VOID); a finding without the substring = the
    WRONG detector (VOID); a crash = a FIXTURE DEFECT (VOID).  A HALT is a
    finding (it carries its own text)."""
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
            caught.append(f"{name} [{len(found)} finding(s)] -> {shown}")
    if crashed:
        return True, (f"{len(crashed)} plant(s) CRASHED — a FIXTURE DEFECT, not a "
                      f"finding: " + " · ".join(crashed))
    if passed or wrong:
        return True, (f"{len(passed)} plant(s) PASSED {passed}; {len(wrong)} caught by the "
                      f"WRONG detector {wrong}")
    return False, (f"all {len(caught)} plants caught by their named detector, one at a "
                   f"time: " + " · ".join(caught))


def verdict(findings: list[str], ok_text: str) -> tuple[bool, str]:
    if findings:
        return False, f"{len(findings)} finding(s): " + " · ".join(findings[:4])
    return True, ok_text


# ═════════════════════════════════════════ THE MUTANTS (shadow copies of the module)
# tag -> (what the mis-build is, [(anchor in tierc11_ride.py, replacement), ...]).
# Each anchor must occur EXACTLY once, or the plant crashes (a fixture defect).
MUTANTS = {
    "M1": ("relay_entry: a 1h entry's as-of is J (the stop/ATR read at the unclosed bar)",
           [('"asof_i": J - 1, "moved": False, "child_k": k}',
             '"asof_i": J, "moved": False, "child_k": k}')]),
    "M2": ("relay11: the harvest armed on close[J], not close[J-1]",
           [('if not st["h_armed"] and RC.harvest_outside(float(f.c[J - 1]), pe, d):',
             'if not st["h_armed"] and RC.harvest_outside(float(f.c[J]), pe, d):')]),
    "M3": ("relay11: the harvest touch judged on the WHOLE bar J",
           [('hi_post, lo_post = float(W.h1.h[post].max()), float(W.h1.l[post].min())',
             'hi_post, lo_post = float(f.h[J]), float(f.l[J])')]),
    "M4": ("relay11: the trail armed by the parent's high (v6's bar law), not the latch",
           [('    if wk["latch_k"] is not None:\n        st["reached_1r"] = True',
             '    if ((float(f.h[J]) - entry_px) / R >= 1.0 if d == 1\n'
             '            else (entry_px - float(f.l[J])) / R >= 1.0):\n'
             '        st["trail_armed"] = True\n'
             '    if wk["latch_k"] is not None:\n        st["reached_1r"] = True')]),
    "M5": ("relay_entry: a 1h entry inside a MISMATCH bar is not moved to the parent's close",
           [('    elif not W.ok[J]:\n        out = {"J": J, "kind": "parent-close',
             '    elif False:\n        out = {"J": J, "kind": "parent-close')]),
    "M6": ("admit_adds: an add event on a MISMATCH bar is not moved to the parent's close",
           [("        moved = not bool(walk.ok[i])", "        moved = False")]),
    "M7": ("ride11: a mismatch bar's warn ignores the parent's +1R latch",
           [("            if wctr is not None and latch_ms is None:\n"
             "                a, n = int(walk.a[j]), int(walk.n[j])",
             "            if wctr is not None:\n"
             "                a, n = int(walk.a[j]), int(walk.n[j])")]),
    "M8": ("relay11: mae_to_1r counts J's children AFTER the latch",
           [('st["mae_to_1r"] = min(st["mae_to_1r"], wk["min_uadv_pre"])',
             'st["mae_to_1r"] = min(st["mae_to_1r"], wk["min_uadv"])')]),
    "M9": ("ride11: the TP exit instant under the walk is the 4h close",
           [("                    exit_child_ms = walk.h1.close_ms(fk[0])",
             "                    exit_child_ms = int(om[j]) + MS_4H")]),
    "M10": ("ride11: the post-harvest TP twin is also live BEFORE the harvest",
            [('                        and (post_ok or tp.mode != "post_harvest"))',
              "                        and True)")]),
    "M11": ("relay11: the continuation starts at J+2 (skips J+1)",
            [("state=stJ, j0=J + 1, child_order=child_order, ctx=cx)",
              "state=stJ, j0=J + 2, child_order=child_order, ctx=cx)")]),
    "M12": ("ride11: an injected state's stop is ignored (restarts from stop0)",
            [('    stop = float(st["stop"])', "    stop = float(stop0)")]),
    "M13": ("relay11: no TRAIL at J's close",
            [('    if card.trail and st["trail_armed"]:', '    if False and st["trail_armed"]:')]),
    "M14": ("ride11: the TP near-side test reads close[j] (look-ahead), not close[j-1]",
            [("                near = (lvl - float(f.c[j - 1])) * d > 0.0",
              "                near = (lvl - float(f.c[j])) * d > 0.0")]),
    "M15": ("relay11: the moved= guard removed (a walkable bar's close accepted as moved)",
            [("    if moved and (t != int(om[J]) + MS_4H or bool(W.ok[J])):",
              "    if False:")]),
    "M16": ("ride11: a TP filled on a MISMATCH bar is stamped at the parent's close (the "
            "post-event twin), not the bar's open",
            [('                else:\n                    exit_close_ms, exit_by = close_j, "parent"\n'
              '            break\n        if (fav - entry_px) * d > (mfe - entry_px) * d:',
              '                else:\n                    exit_close_ms, exit_by = close_j, "parent"\n'
              '                    exit_stamp = close_j\n'
              '            break\n        if (fav - entry_px) * d > (mfe - entry_px) * d:')]),
    "M17": ("ride11: a stop decided by the parent on a MISMATCH bar is stamped at its close, "
            "not the bar's open",
            [('            elif walk is not None:\n                exit_close_ms, exit_by = close_j, '
              '"parent"\n            break\n        if winner == "warn":',
              '            elif walk is not None:\n                exit_close_ms, exit_by = close_j, '
              '"parent"\n                exit_stamp = close_j\n            break\n'
              '        if winner == "warn":')]),
    "W1": ("warn_of: the default pair is 12/26, not L-W.2's 12/89",
           [("def warn_of(walk: Walk, fast: int = 12, slow: int = 89) -> Warn:",
             "def warn_of(walk: Walk, fast: int = 12, slow: int = 26) -> Warn:")]),
    "W2": ("walk_children: the warn fires after the +1R latch too",
           [("                if wctr is not None and not latched and bool(wctr[k]):",
             "                if wctr is not None and bool(wctr[k]):")]),
    "A1": ("admit_adds: the caller's price is taken, unchecked",
           [("        if px is not None and (px_1h is None or px != px_1h):",
             "        if False:"),
            ("if moved else (ms, px_1h)", "if moved else (ms, px if px is not None else px_1h)")]),
    "T1": ("transform_book: the walk-type guard removed",
           [("    if not (isinstance(walk, bool) or callable(walk)):", "    if False:")]),
}
_SHADOW: dict = {}


def shadow_rd(tag: str):
    """A shadow tierc11_ride with ONE mis-build, loaded as its own module; it
    shares the real module's 1h-tape / walk memos (read-only data)."""
    if tag in _SHADOW:
        return _SHADOW[tag]
    _, pairs = MUTANTS[tag]
    src = RIDE_SRC.read_text(encoding="utf-8")
    for old, new in pairs:
        if src.count(old) != 1:
            raise RuntimeError(f"mutant {tag}: its anchor occurs {src.count(old)} times")
        src = src.replace(old, new)
    root_line = "ROOT = Path(__file__).resolve().parents[1]"
    if src.count(root_line) != 1:
        raise RuntimeError("the ride's ROOT line is not unique")
    src = src.replace(root_line, f"ROOT = Path({str(ROOT)!r})")
    name = f"tierc11_ride_mut_{tag}"
    with tempfile.TemporaryDirectory(prefix="f-ride-mut-") as td:
        p = Path(td) / f"{name}.py"
        p.write_text(src, encoding="utf-8")
        spec = importlib.util.spec_from_file_location(name, p)
        mod = importlib.util.module_from_spec(spec)
        sys.modules[name] = mod
        spec.loader.exec_module(mod)
    mod._H1, mod._WALKS = RD._H1, RD._WALKS
    _SHADOW[tag] = mod
    return mod


def mutant(tag: str, detector: str, thunk):
    """A plant row: the REAL check `thunk(rd)` run on the shadow module `tag`."""
    return (f"[mutant {tag}] {MUTANTS[tag][0]}", detector, lambda: thunk(shadow_rd(tag)))


# ═══════════════════════════════════════════════ THE SHARED BOOK (computed once)
_C: dict = {}


def corridor() -> tuple[int, int]:
    if "lo" not in _C:
        lo, hi, _ = TP.corridor_n(E.CLASSIC5)
        if hi + 1 != PIN:
            raise SystemExit(f"HALT: the corridor ends {iso(hi + 1)}, not the pin {iso(PIN)}")
        _C["lo"], _C["hi"] = lo, hi
    return _C["lo"], _C["hi"]


def base() -> list:
    """The v6 control over the TC11 corridor (the book every fixture judges)."""
    if "base" not in _C:
        lo, hi = corridor()
        _C["base"] = TP.run_cell_n(CARD, ROLES, E.CLASSIC5, lo, hi)
    return _C["base"]


def keyed(book) -> list:
    return sorted(book, key=lambda t: (t.symbol, int(t.entry_ms)))


def hi_i_of(sym: str) -> int:
    lo, hi = corridor()
    return T7._idx_range(T9.frame(sym)["f"].open_ms, lo, hi)[1]


def inputs() -> list:
    if "inp" not in _C:
        lo, hi = corridor()
        _C["inp"] = RD.v6_inputs(base(), CARD, ROLES, lo, hi)
    return _C["inp"]


def inp_of(t):
    return next(i for i in inputs() if i.key == (t.symbol, int(t.entry_ms)))


# ── THIS FILE'S OWN READ of the snapshot (the hand-walk's data path) ──────────
def own_bars(sym: str, lens: str) -> pd.DataFrame:
    k = ("own", sym, lens)
    if k not in _C:
        step = {"1h": H1, "4h": H4}[lens]
        d = pd.read_parquet(SNAP / "klines" / f"{sym}_{lens}.parquet").sort_values("open_time")
        d = d[d["open_time"] + step <= PIN].reset_index(drop=True)
        _C[k] = d
    return _C[k]


def own_funding(sym: str) -> dict:
    k = ("fund", sym)
    if k not in _C:
        d = pd.read_parquet(SNAP / "funding" / f"{sym}.parquet")
        out: dict = {}
        for ft, fr in zip(d["funding_time"].astype(np.int64), d["funding_rate"].astype(float)):
            h = int(ft) // H1 * H1
            out[h] = out.get(h, 0.0) + fr
        _C[k] = out
    return _C[k]


def own_ema(x, n: int) -> np.ndarray:
    """A plain recursive EMA (alpha 2/(n+1), seeded at the first value) — THIS
    file's loop, never the engine's."""
    a = 2.0 / (n + 1.0)
    out = np.empty(len(x))
    prev = None
    for i, v in enumerate(x):
        v = float(v)
        if v != v:
            raise RuntimeError("a NaN close in the own read")
        prev = v if prev is None else prev + a * (v - prev)
        out[i] = prev
    return out


def own_cross(fast: np.ndarray, slow: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    up = np.zeros(len(fast), dtype=bool)
    dn = np.zeros(len(fast), dtype=bool)
    up[1:] = (fast[1:] > slow[1:]) & (fast[:-1] <= slow[:-1])
    dn[1:] = (fast[1:] < slow[1:]) & (fast[:-1] >= slow[:-1])
    return up, dn


def own4(sym: str) -> dict:
    """The own 4h tape with this file's EMAs, bells and band edges.  Its rows must
    BE the frame the module rides (same opens and prices), or indices would not
    align — a fixture defect, never a finding."""
    k = ("own4", sym)
    if k not in _C:
        b = own_bars(sym, "4h")
        om = b["open_time"].to_numpy(np.int64)
        o, h, l, c = (b[x].to_numpy(float) for x in ("open", "high", "low", "close"))
        f = T9.frame(sym)["f"]
        if not (np.array_equal(om, np.asarray(f.open_ms, dtype=np.int64))
                and np.array_equal(h, f.h) and np.array_equal(l, f.l)
                and np.array_equal(c, f.c) and np.array_equal(o, f.o)):
            raise RuntimeError(f"{sym}: the own 4h read is not the module's frame")
        e12, e89, e316 = own_ema(c, WIN_F), own_ema(c, TIDE_F), own_ema(c, TIDE_S)
        w_up, w_dn = own_cross(e12, e89)
        b_up, b_dn = own_cross(e89, e316)
        lo, hi = corridor()
        lo_i, hi_i = T7._idx_range(om, lo, hi)
        _C[k] = dict(om=om, o=o, h=h, l=l, c=c, e89=e89, e316=e316, w_up=w_up, w_dn=w_dn,
                     b_up=b_up, b_dn=b_dn, lo_i=lo_i, hi_i=hi_i)
    return _C[k]


def own1(sym: str) -> dict:
    """The own 1h tape (row order = the module's tape order, checked)."""
    k = ("own1", sym)
    if k not in _C:
        b = own_bars(sym, "1h")
        t = b["open_time"].to_numpy(np.int64)
        if not np.array_equal(t, RD.h1_tape(sym).open_ms):
            raise RuntimeError(f"{sym}: the own 1h read is not row-aligned with the module's")
        _C[k] = dict(t=t, h=b["high"].to_numpy(float), l=b["low"].to_numpy(float),
                     c=b["close"].to_numpy(float), idx={int(x): i for i, x in enumerate(t)})
    return _C[k]


def same(a, b_) -> bool:
    return abs(float(a) - float(b_)) <= TOL * max(1.0, abs(float(a)), abs(float(b_)))


def own_kids(sym: str, J: int):
    """THIS file's walk law: the 4 rows of bar J (4 on the 1h grid, none other in
    the bar) reproducing its high, low and close to the representation
    tolerance; else None (a mismatch bar)."""
    k = ("kids", sym, int(J))
    if k not in _C:
        X, Hh = own4(sym), own1(sym)
        o4 = int(X["om"][J])
        ks = [Hh["idx"].get(o4 + q * H1) for q in range(4)]
        n_in = int(np.searchsorted(Hh["t"], o4 + H4, "left") - np.searchsorted(Hh["t"], o4, "left"))
        ok = all(x is not None for x in ks) and n_in == 4
        if ok:
            ok = (same(max(Hh["h"][x] for x in ks), X["h"][J])
                  and same(min(Hh["l"][x] for x in ks), X["l"][J])
                  and same(Hh["c"][ks[3]], X["c"][J]))
        _C[k] = ks if ok else None
    return _C[k]


def own_bar_index(sym: str, open4: int) -> int:
    return int(np.searchsorted(own4(sym)["om"], int(open4), "left"))


def own_children(sym: str, open4: int) -> pd.DataFrame:
    d = own_bars(sym, "1h")
    return d[(d["open_time"] >= open4) & (d["open_time"] < open4 + H4)]


def own_walkable(sym: str, open4: int) -> bool:
    return own_kids(sym, own_bar_index(sym, open4)) is not None


def own_1h_close(sym: str, close_ms: int) -> float:
    Hh = own1(sym)
    i = Hh["idx"].get(int(close_ms) - H1)
    if i is None:
        raise RuntimeError(f"no own 1h bar closing {iso(close_ms)}")
    return float(Hh["c"][i])


def band_edge(sym: str, j: int, d: int) -> float:
    X = own4(sym)
    return max(X["e89"][j], X["e316"][j]) if d == 1 else min(X["e89"][j], X["e316"][j])


def outside(px: float, edge: float, d: int) -> bool:
    return bool(px > edge) if d == 1 else bool(px < edge)


def bell_at(sym: str, j: int, d: int):
    X = own4(sym)
    if d == 1:
        return BELL_W if X["w_dn"][j] else BELL_T if X["b_dn"][j] else None
    return BELL_W if X["w_up"][j] else BELL_T if X["b_up"][j] else None


def stop_at(t, j: int) -> float:
    """The stop in force at bar j of a v6 campaign (its trail advances, conf < j)."""
    st = float(t.stop_px)
    for a in t.advances:
        if a.conf_i < j:
            st = float(a.new_stop)
    return st


def own_latch_bar(t):
    """The first bar after entry whose PARENT reaches +1R (own read), or None."""
    X, d, e, R = own4(t.symbol), int(t.direction), float(t.entry_px), float(t.r_dist)
    for j in range(int(t.entry_i) + 1, int(t.exit_i) + 1):
        fav = X["h"][j] if d == 1 else X["l"][j]
        if (fav - e) * d / R >= 1.0:
            return j
    return None


def canon(x):
    """A JSON-stable image (floats by repr) for the probe's shas."""
    if x is None or isinstance(x, (bool, str)):
        return x
    if isinstance(x, (np.bool_,)):
        return bool(x)
    if isinstance(x, (int, np.integer)):
        return int(x)
    if isinstance(x, (float, np.floating)):
        return repr(float(x))
    if dataclasses.is_dataclass(x):
        return canon(dataclasses.astuple(x))
    if isinstance(x, dict):
        return {str(k): canon(v) for k, v in sorted(x.items(), key=lambda kv: str(kv[0]))}
    if isinstance(x, (list, tuple)):
        return [canon(v) for v in x]
    return str(x)


def rows_sha(rows) -> str:
    return sha_bytes(json.dumps(canon(rows), separators=(",", ":")).encode("utf-8"))


# ── comparators ───────────────────────────────────────────────────────────────
def val(t, c):
    return len(t.advances) if c == "n_advances" else float(getattr(t, c))


def raw_diff(got, want, label: str) -> tuple[list[str], float]:
    """EXACT on the 12 CTRL_COLS (raw floats, not the journal's 6 dp), exit
    reasons identical, same keys, same count."""
    g, w = keyed(got), keyed(want)
    out = []
    if len(g) != len(w):
        return [f"{label}: campaigns {len(g)} vs {len(w)}"], float("inf")
    worst = 0.0
    for a, b in zip(g, w):
        if (a.symbol, int(a.entry_ms)) != (b.symbol, int(b.entry_ms)):
            out.append(f"{label}: key {a.symbol} {iso(a.entry_ms)} vs {b.symbol} {iso(b.entry_ms)}")
            continue
        for c in CTRL_COLS:
            dv = abs(val(a, c) - val(b, c))
            worst = max(worst, dv)
            if dv != 0.0:
                out.append(f"{label}: {a.symbol} {iso(a.entry_ms)} {c} differs by {dv:.3e}")
        if a.exit_reason != b.exit_reason:
            out.append(f"{label}: {a.symbol} {iso(a.entry_ms)} exit_reason {a.exit_reason!r} "
                       f"vs {b.exit_reason!r}")
    return out, worst


LEG_KEYS = ("exit_i", "exit_px", "exit_reason", "final_stop", "mfe", "mae", "mae_to_1r",
            "reached_1r", "harvest", "blocked", "n_opportunities", "own_r", "entry_i",
            "entry_px", "stop0")
GLUE_KEYS = ("exit_i", "exit_px", "exit_reason", "final_stop", "mfe", "mae", "mae_to_1r",
             "reached_1r", "harvest", "blocked", "n_opportunities")


def adv_rows(advs) -> list:
    return [dataclasses.astuple(a) for a in advs]


def leg_diff(got: dict, want: dict, label: str, keys=LEG_KEYS) -> list[str]:
    out = [f"{label}: {k} {got.get(k)!r} vs {want.get(k)!r}" for k in keys
           if got.get(k) != want.get(k)]
    if adv_rows(got["advances"]) != adv_rows(want["advances"]):
        out.append(f"{label}: advances differ ({len(got['advances'])} vs "
                   f"{len(want['advances'])})")
    return out


# ── planted 1h tapes and walks (COPIES; never memoised by RD) ─────────────────
def planted_tape(sym: str, X: int, children) -> RD.H1Tape:
    """A copy of the real 1h tape with the four children of 4h bar X replaced by
    `children` = [(o, h, l, c)] * 4 (the 1h opens stay the real grid)."""
    real = RD.h1_tape(sym)
    W = RD.walk_of(sym)
    a = int(W.a[X])
    o, h, l, c = (real.o.copy(), real.h.copy(), real.l.copy(), real.c.copy())
    for k, (co, ch, cl, cc) in enumerate(children):
        o[a + k], h[a + k], l[a + k], c[a + k] = co, ch, cl, cc
    return RD.H1Tape(sym, real.open_ms.copy(), o, h, l, c, source=f"PLANT bar {X}")


def mismatch_walk(sym: str, Y: int, d: int):
    """The real walk with bar Y turned into a MISMATCH bar: the child carrying the
    parent's FAVOURABLE extreme is pushed LIFT (1e-6 relative) past it — a long's
    high up, a short's low down — so the children no longer reproduce the parent
    (THIS file's reproduction test must say so) and nothing the parent decides
    moves.  Only bar Y's walk flag changes."""
    real, W = RD.h1_tape(sym), RD.walk_of(sym)
    ks = own_kids(sym, Y)
    if ks is None or int(W.a[Y]) != ks[0]:
        raise RuntimeError(f"{sym} bar {Y}: not an own-walkable bar aligned to the walk")
    X = own4(sym)
    h, l = real.h.copy(), real.l.copy()
    if d == 1:
        k = ks[int(np.argmax([h[x] for x in ks]))]
        h[k] = h[k] * (1 + LIFT)
    else:
        k = ks[int(np.argmin([l[x] for x in ks]))]
        l[k] = l[k] * (1 - LIFT)
    if same(max(h[x] for x in ks), X["h"][Y]) and same(min(l[x] for x in ks), X["l"][Y]):
        raise RuntimeError(f"{sym} bar {Y}: the planted children still reproduce the parent")
    tape = RD.H1Tape(sym, real.open_ms, real.o, h, l, real.c, source=f"PLANT mismatch {Y}")
    ok = W.ok.copy()
    ok[Y] = False
    why = dict(W.why)
    why[Y] = "PLANT: the favourable-extreme child lifted 1e-6 past the parent"
    return dataclasses.replace(W, h1=tape, ok=ok, why=why)


# ═══════════════════════════════════════════════════════════ F-WALK-IDENT
def walk_book(walk_for=True, bend=None):
    lo, hi = corridor()
    book = RD.transform_book(base(), CARD, ROLES, lo, hi, walk=walk_for)
    if bend is not None:
        book = [copy.copy(t) for t in book]
        bend(book)
    return book


def walk_book_real():
    if "wb" not in _C:
        _C["wb"] = walk_book(True)
    return _C["wb"]


def walk_real_findings(bend=None) -> tuple[list[str], str]:
    book = walk_book(True, bend)
    bad, worst = raw_diff(book, base(), "walk-ON vs v6")
    ok_j, worst_j, why_j = TP.ctrl_diff(TP.journal_frame(book), TP.journal_frame(base()))
    if not ok_j:
        bad.append(f"TP.ctrl_diff(journals): {why_j}")
    idf, ist = RD.identity_findings(base(), book)
    bad += idf
    if ist["acted"]:
        bad.append(f"IDENTITY: {ist['acted']} campaign(s) flagged acted with every hook off")
    nm = sum(t.n_walk_mismatch for t in book)
    res = {}
    for t in book:
        res[t.exit_resolved_by] = res.get(t.exit_resolved_by, 0) + 1
    return bad, (f"whole book n {len(book)}: raw CTRL_COLS worst {worst:.3e}, journals "
                 f"{why_j}; identity helper {ist}; mismatch bars ridden (decided by the "
                 f"parent, summed over the book) {nm}; exits resolved "
                 f"{dict(sorted(res.items()))}")


def walk_type_findings(rd=RD) -> list[str]:
    """MINOR-9: transform_book(walk=<a Walk object>) must HALT, never ride the
    real walk silently."""
    lo, hi = corridor()
    b0 = base()[:1]
    try:
        rd.transform_book(b0, CARD, ROLES, lo, hi, walk=rd.walk_of(b0[0].symbol))
    except SystemExit as e:
        if "transform_book(walk=)" in str(e):
            return []
        return [f"WALK-TYPE: a HALT, but not the walk-type guard's: {e}"]
    return ["WALK-TYPE: a Walk object passed as walk= was accepted (it rides the REAL walk)"]


def pick_stop_campaign() -> tuple:
    """The first v6 stop exit, in (asset, entry) order, whose exit bar is walkable."""
    for t in keyed(base()):
        if t.exit_reason == "stop" and RD.walk_of(t.symbol).ok[t.exit_i]:
            return t
    raise RuntimeError("no walkable v6 stop exit")


def mismatch_plant(sabotage: bool = False) -> tuple[list[str], str]:
    """A real stop bar X whose children are lifted clear of the stop (a long's
    four prices max'd with stop*(1+1e-6); mirrored short): they no longer
    reproduce the parent's low (high), so L-W.0 hands X to the parent — v6's
    exit, counted, resolved 'parent', stamped at the bar's OPEN (L-R.5).
    SABOTAGE: every 4-child bar walkable."""
    t = pick_stop_campaign()
    s, X, d, stop = t.symbol, int(t.exit_i), int(t.direction), float(t.exit_px)
    real, W = RD.h1_tape(s), RD.walk_of(s)
    a = int(W.a[X])
    lift = stop * (1 + 1e-6) if d == 1 else stop * (1 - 1e-6)
    f = (max if d == 1 else min)
    ch = [tuple(f(float(x), lift) for x in (real.o[k], real.h[k], real.l[k], real.c[k]))
          for k in range(a, a + 4)]
    Wp = RD.walk_of(s, h1=planted_tape(s, X, ch))
    if Wp.ok[X]:
        raise RuntimeError("the planted bar is still walkable — the plant tests nothing")
    if sabotage:
        Wp = dataclasses.replace(Wp, ok=(Wp.n == 4))
    got = RD.ride_campaign(inp_of(t), CARD, ROLES, walk=Wp)
    bad, _ = raw_diff([got], [t], "PLANT mismatch")
    om = T9.frame(s)["f"].open_ms
    if got.exit_resolved_by != "parent" or got.exit_close_ms != int(om[X]) + H4:
        bad.append(f"PLANT mismatch: resolved {got.exit_resolved_by!r} at "
                   f"{got.exit_close_ms}, want 'parent' at the 4h close")
    if got.exit_stamp_ms != int(om[X]):
        bad.append(f"PLANT mismatch: exit_stamp_ms {got.exit_stamp_ms}, want the bar's OPEN "
                   f"{int(om[X])} (L-R.5, a stop decided by the parent)")
    if int(om[X]) not in got.walk_mismatch_ms:
        bad.append("PLANT mismatch: the planted bar is not counted")
    return bad, (f"{s} {iso(t.entry_ms)} exit bar {iso(om[X])} ({Wp.why.get(X, '')}): v6's "
                 f"stop at {stop:.8g}, resolved {got.exit_resolved_by}, stamped at the bar's "
                 f"open, counted {got.n_walk_mismatch}")


def pick_survived_campaign():
    """The first v6 campaign (key order) that survives its first ride bar Y =
    entry+1, a walkable bar."""
    for t in keyed(base()):
        Y = int(t.entry_i) + 1
        if int(t.exit_i) > Y and RD.walk_of(t.symbol).ok[Y]:
            return t, Y
    raise RuntimeError("no survived first bar")


def mismatch_below_plant(sabotage: bool = False) -> tuple[list[str], str]:
    """A real first ride bar Y the parent SURVIVES; one child's low (high, short)
    pushed 1e-4 past the stop in force (stop0): the children no longer reproduce
    the parent, and they now 'touch' a stop the parent never touched — L-W.0
    hands Y to the parent: no stop, v6's campaign unchanged, the bar counted.
    SABOTAGE: every 4-child bar walkable."""
    t, Y = pick_survived_campaign()
    s, d, stop0 = t.symbol, int(t.direction), float(t.stop_px)
    real, W = RD.h1_tape(s), RD.walk_of(s)
    a = int(W.a[Y])
    ch = [(float(real.o[k]), float(real.h[k]), float(real.l[k]), float(real.c[k]))
          for k in range(a, a + 4)]
    o_, h_, l_, c_ = ch[1]
    ch[1] = ((o_, h_, stop0 * (1 - 1e-4), c_) if d == 1 else (o_, stop0 * (1 + 1e-4), l_, c_))
    Wp = RD.walk_of(s, h1=planted_tape(s, Y, ch))
    if Wp.ok[Y]:
        raise RuntimeError("the planted bar is still walkable — the plant tests nothing")
    if sabotage:
        Wp = dataclasses.replace(Wp, ok=(Wp.n == 4))
    got = RD.ride_campaign(inp_of(t), CARD, ROLES, walk=Wp)
    bad, _ = raw_diff([got], [t], "PLANT mismatch-below")
    om = T9.frame(s)["f"].open_ms
    if int(om[Y]) not in got.walk_mismatch_ms:
        bad.append("PLANT mismatch-below: the planted bar is not counted")
    return bad, (f"{s} {iso(t.entry_ms)} bar {iso(om[Y])} ({Wp.why.get(Y, '')}): the parent "
                 f"survives, v6's campaign unchanged (exit {iso(t.exit_ms)} {t.exit_reason})")


def order_bar() -> tuple:
    """BTCUSDT, the first corridor bar X (from floor + 400) that is walkable and
    admits the geometry below with entry e = close[X-1], R = 0.8 * min(H - e,
    e - L): stop e - R and target e + R both inside (L, H), and the open and the
    close strictly between them."""
    s = "BTCUSDT"
    f, W = T9.frame(s)["f"], RD.walk_of(s)
    lo_i = max(T7._idx_range(f.open_ms, *corridor())[0], ROLES.floor_bars)
    for X in range(lo_i + 400, hi_i_of(s)):
        if not W.ok[X]:
            continue
        e, H, L, O, C = (float(f.c[X - 1]), float(f.h[X]), float(f.l[X]), float(f.o[X]),
                         float(f.c[X]))
        R = 0.8 * min(H - e, e - L)
        if R <= 0:
            continue
        stop, tgt = e - R, e + R
        if stop < O < tgt and stop < C < tgt and stop < min(O, e):
            return s, X, e, R, stop, tgt, (O, H, L, C)
    raise RuntimeError("no order bar")


def order_plant(kind: str, child_order=RD.CHILD_ORDER) -> tuple[list[str], str]:
    """kind 'same': child 1 touches the stop AND prints +1R -> STOP, no latch.
       kind 'first': child 1 prints +1R, child 2 touches the stop -> latch on 1.
    The children reproduce the parent (walkable); the v6 reference is
    tierc9._ride_leg9 on the same (entry, stop, R), from bar X."""
    s, X, e, R, stop, tgt, (O, H, L, C) = order_bar()
    if kind == "same":
        ch = [(O, O, O, O), (O, H, L, e), (e, e, e, e), (e, max(e, C), min(e, C), C)]
        want_latch, want_exit_k, want_plus = None, 1, 1
    else:
        ch = [(O, O, O, O), (O, H, min(O, e), e), (e, e, L, e), (e, max(e, C), min(e, C), C)]
        want_latch, want_exit_k, want_plus = 1, 2, 1
    Wp = RD.walk_of(s, h1=planted_tape(s, X, ch))
    if not Wp.ok[X]:
        raise RuntimeError(f"the planted '{kind}' bar is not walkable: {Wp.why.get(X)}")
    hi_i = hi_i_of(s)
    ref = T9._ride_leg9(s, CARD, ROLES, 1, X - 1, e, stop, R, hi_i)
    got = RD.ride11(s, CARD, ROLES, 1, X - 1, e, stop, R, hi_i, walk=Wp,
                    child_order=child_order)
    a = int(Wp.a[X])
    cm = [Wp.h1.close_ms(a + k) for k in range(4)]
    bad = leg_diff(got, ref, f"PLANT {kind}")
    want = {"latch_1h_ms": None if want_latch is None else cm[want_latch],
            "exit_child_ms": cm[want_exit_k], "exit_resolved_by": "1h",
            "plus1r_1h_ms": cm[want_plus], "latch_on_stop_child": kind == "same",
            "exit_stamp_ms": cm[want_exit_k],
            "latch_stamp_ms": None if want_latch is None else cm[want_latch]}
    bad += [f"PLANT {kind}: {k} got {got[k]!r}, hand-walked {v!r}" for k, v in want.items()
            if got[k] != v]
    return bad, (f"{s} bar {iso(Wp.open4[X])} e {e:.8g} stop {stop:.8g} +1R {tgt:.8g}: "
                 f"exit child {want_exit_k}, latch child {want_latch}")


def bend_one(book):
    """Bend ONE unacted campaign's net_r by 1e-12 (the identity helper's plant)."""
    t = book[len(book) // 2]
    object.__setattr__(t, "net_r", float(t.net_r) + 1e-12)


def walk_break():
    return plants([
        ("a walk ignoring the mismatch law (every 4-child bar walkable) on the planted "
         "mismatch bar", "L-W.3", lambda: mismatch_plant(sabotage=True)[0]),
        ("the same, on the planted children-below-the-parent bar", "L-W.3",
         lambda: mismatch_below_plant(sabotage=True)[0]),
        ("child order LATCH before STOP on the planted same-child bar", "latch_1h_ms",
         lambda: order_plant("same", child_order=("latch", "stop", "warn"))[0]),
        ("the walk-ON book with one unacted campaign's net_r bent by 1e-12", "IDENTITY",
         lambda: walk_real_findings(bend=bend_one)[0]),
        mutant("T1", "WALK-TYPE", walk_type_findings),
    ])


def walk_real():
    b1, t1 = walk_real_findings()
    b2, t2 = mismatch_plant()
    b2b, t2b = mismatch_below_plant()
    b3, t3 = order_plant("same")
    b4, t4 = order_plant("first")
    b5 = walk_type_findings()
    return verdict(b1 + b2 + b2b + b3 + b4 + b5,
                   f"{t1} · PLANT mismatch: {t2} · PLANT mismatch-below: {t2b} · PLANT "
                   f"same-child: {t3} · PLANT latch-first: {t4} · transform_book(walk=<Walk>) "
                   f"HALTs (walk-type guard)")


# ═══════════════════════════════════════════════════════════ F-RELAY-RIDE
def relay_close_findings(rd=RD) -> tuple[list[str], str]:
    """(a) every v6 campaign re-entered through the relay path at its 4h close."""
    bad, n = [], 0
    trades = []
    for inp in inputs():
        s = inp.symbol
        f = T9.frame(s)["f"]
        re_ = rd.relay_entry(s, inp.entry_close_ms)
        if re_["kind"] != "4h-close" or re_["J"] != inp.ti or re_["entry_px"] != inp.entry_px:
            bad.append(f"RELAY-CLOSE {s} {iso(inp.entry_ms)}: entry resolved {re_}")
            continue
        stp, atr = rd.relay_stop(s, re_["asof_i"], re_["entry_px"], inp.direction, CARD)
        if stp is None or stp.stop_px != inp.stop.stop_px or stp.r_dist != inp.stop.r_dist \
                or atr != inp.atr_sig:
            bad.append(f"RELAY-CLOSE {s} {iso(inp.entry_ms)}: relay_stop {stp} vs v6 {inp.stop}")
            continue
        leg = rd.relay11(s, CARD, ROLES, inp.direction, re_["entry_close_ms"], re_["entry_px"],
                         stp.stop_px, stp.r_dist, inp.hi_i)
        ref = T9._ride_leg9(s, CARD, ROLES, inp.direction, inp.ti, inp.entry_px,
                            inp.stop.stop_px, inp.stop.r_dist, inp.hi_i)
        bad += leg_diff(leg, ref, f"RELAY-CLOSE {s} {iso(inp.entry_ms)} vs _ride_leg9",
                        keys=tuple(k for k in ref if k != "advances"))
        trades.append(rd.trade11(s, CARD, ROLES, inp.direction, arm_i=inp.arm_i,
                                 arm_ms=inp.arm_ms, disp=inp.disp, entry_i=re_["J"],
                                 entry_ms=int(f.open_ms[re_["J"]]), entry_px=re_["entry_px"],
                                 stp=stp, atr_sig=atr, leg=leg,
                                 entry_close_ms=re_["entry_close_ms"]))
        n += 1
    if n < 20:
        bad.append(f"RELAY-CLOSE: only {n} campaigns re-entered (< 20)")
    tb, worst = raw_diff(trades, base(), "RELAY-CLOSE trade vs v6")
    return bad + tb, (f"(a) {n} real v6 campaigns re-entered at their 4h close == "
                      f"_ride_leg9 on every key, Trade CTRL_COLS worst {worst:.3e}")


def hand_stop(sym: str, asof_i: int, e: float, d: int):
    """struct_stop_4h (v6's law) as of THIS file's as-of bar, railed RAIL_ATR."""
    F = T9.frame(sym)
    atr = float(F["f"].atr[asof_i])
    if not (np.isfinite(atr) and atr > 0):
        return None, atr
    stp = RC.struct_stop_4h(F["pv4"], int(asof_i), float(e), int(d), atr,
                            min_stop_atr=RAIL_ATR, forbidden=None)
    if stp is None or not (np.isfinite(stp.r_dist) and stp.r_dist > 0):
        return None, atr
    return stp, atr


def hand_trail(sym: str, J: int, d: int, stop: float):
    """v6's trail law (matched_step) at J's close, on the hand-walked stop."""
    X = own4(sym)
    return T8.matched_step(T9.fractals(sym, *TRAIL_LR), int(J), int(d), float(stop),
                           float(X["c"][J]), float(T9.frame(sym)["f"].atr[J]),
                           T8.anchor_series(sym), ANCHOR_KIND, ANCHOR_OFF, X["om"],
                           min_advance_atr=MIN_ADV_ATR)


def hand_relay_J(sym: str, d: int, J: int, ke: int, e: float, stop: float, R: float) -> dict:
    """THIS FILE'S WALK of bar J after a relay entry at the close of own child ke
    [L-T.2]: per post-entry child STOP then the +1R latch (adverse and +1R print
    counted on the stop child; its favourable not); the harvest armed per
    close[J-1] and touched on the post-entry children; the bell at J."""
    X, Hh = own4(sym), own1(sym)
    ks = own_kids(sym, J)
    mae = m1r = 0.0
    mfe, latch, plus, xk = e, None, None, None
    for k in ks[ke + 1:]:
        hi_, lo_ = float(Hh["h"][k]), float(Hh["l"][k])
        fav, adv = (hi_, lo_) if d == 1 else (lo_, hi_)
        cm = int(Hh["t"][k]) + H1
        uf, ua = (fav - e) * d / R, (adv - e) * d / R
        if plus is None and uf >= 1.0:
            plus = cm
        mae = min(mae, ua)
        if latch is None:
            m1r = min(m1r, ua)
        if (d == 1 and lo_ <= stop) or (d == -1 and hi_ >= stop):
            xk = cm
            break
        if latch is None and uf >= 1.0:
            latch = cm
        if (fav - e) * d > (mfe - e) * d:
            mfe = fav
    post = ks[ke + 1:]
    hp, lp = max(float(Hh["h"][k]) for k in post), min(float(Hh["l"][k]) for k in post)
    h_armed = outside(float(X["c"][J - 1]), band_edge(sym, J - 1, d), d)
    edge = band_edge(sym, J, d)
    ufill = (float(X["c"][J]) - e) * d / R
    touch = bool(h_armed and ((lp <= edge) if d == 1 else (hp >= edge))
                 and ufill >= HARVEST_MIN_UNIT_R)
    harv = (J, float(X["c"][J]), (float(X["c"][J]) - e) * d / R) if touch else None
    return dict(mae=mae, m1r=m1r, mfe=mfe, latch=latch, plus=plus, xk=xk, touch=touch,
                harv=harv, h_armed=h_armed, bell=bell_at(sym, J, d),
                close_J=int(X["om"][J]) + H4)


def relay_population() -> list:
    """Every v6 campaign x J in {ti, ti+1, ti+2} (J <= the corridor edge) x the
    entry at the close of child 0, 1, 2 — in book order."""
    out = []
    for t in base():
        hi = own4(t.symbol)["hi_i"]
        for J in (int(t.entry_i), int(t.entry_i) + 1, int(t.entry_i) + 2):
            if J > hi:
                continue
            for ke in (0, 1, 2):
                out.append((t.symbol, int(t.direction), J, ke))
    return out


def relay_card_findings(rd=RD, carry=None) -> tuple[list[str], str]:
    """(b) the relay's 1h path at cardinality, against this file's hand walk,
    plus the GLUE: a carried relay whose state after J equals v6's one-bar
    state continues EXACTLY as tierc9._ride_leg9 from the same entry/stop/R."""
    bad = []
    paths: dict = {}
    n = n_mm = n_none = n_latch = n_touch = n_glue = 0
    for s, d, J, ke in relay_population():
        X = own4(s)
        lab = f"{s} {'L' if d == 1 else 'S'} J {iso(X['om'][J])} child {ke}"
        te = int(X["om"][J]) + (ke + 1) * H1
        ks = own_kids(s, J)
        if ks is None:                       # F-MISMATCH-1H owns these
            n_mm += 1
            continue
        try:
            re_ = rd.relay_entry(s, te)
        except SystemExit as ex:
            bad.append(f"RELAY-ENTRY {lab}: relay_entry HALTed — {ex}")
            continue
        e = float(own1(s)["c"][ks[ke]])
        want_e = {"J": J, "kind": "1h", "entry_close_ms": te, "entry_px": e, "asof_i": J - 1,
                  "moved": False, "refused": None}
        bad += [f"RELAY-ENTRY {lab}: {k} got {re_.get(k)!r}, hand {v!r}"
                for k, v in want_e.items() if re_.get(k) != v]
        close_J = int(X["om"][J]) + H4
        if rd.relay_entry(s, te, trigger_close_ms=close_J).get("refused") is not None \
                or rd.relay_entry(s, te, trigger_close_ms=int(X["om"][J])).get("refused") is None:
            bad.append(f"RELAY-ENTRY {lab}: the trigger refusal is not 'strictly before the "
                       f"trigger close' (J's close: kept; the prior 4h close: refused)")
        stp, atr = hand_stop(s, J - 1, e, d)
        got_stp, got_atr = rd.relay_stop(s, re_["asof_i"], re_["entry_px"], d, CARD)
        if stp is None:
            n_none += 1
            if got_stp is not None:
                bad.append(f"RELAY-STOP {lab}: relay_stop gave {got_stp.stop_px!r}, struct_stop_4h "
                           f"as of J-1 gives none")
            continue
        if got_stp is None or (got_stp.stop_px, got_stp.r_dist) != (stp.stop_px, stp.r_dist) \
                or got_atr != atr:
            bad.append(f"RELAY-STOP {lab}: relay_stop "
                       f"{None if got_stp is None else (got_stp.stop_px, got_stp.r_dist)} "
                       f"ATR {got_atr!r} vs struct_stop_4h as of J-1 {(stp.stop_px, stp.r_dist)} "
                       f"ATR {atr!r}")
        stop, R = float(stp.stop_px), float(stp.r_dist)
        hw = hand_relay_J(s, d, J, ke, e, stop, R)
        n += 1
        n_latch += hw["latch"] is not None
        n_touch += hw["touch"]
        leg = rd.relay11(s, CARD, ROLES, d, te, e, stop, R, X["hi_i"],
                         carry=carry or rd.carry_state)
        common = {"mae": hw["mae"], "mfe": hw["mfe"], "mae_to_1r_raw": hw["m1r"],
                  "latch_1h_ms": hw["latch"], "plus1r_1h_ms": hw["plus"],
                  "reached_1r": hw["latch"] is not None, "latch_stamp_ms": hw["latch"]}
        if hw["xk"] is not None:
            path = "stop-in-J"
            want = dict(common, exit_reason="stop", exit_i=J, exit_px=stop,
                        exit_close_ms=hw["xk"], exit_stamp_ms=hw["xk"], exit_resolved_by="1h",
                        blocked="stop" if hw["touch"] else "", harvest=None)
        elif hw["bell"]:
            path = "bell-at-J"
            want = dict(common, exit_reason=hw["bell"], exit_i=J, exit_px=float(X["c"][J]),
                        exit_close_ms=hw["close_J"], exit_stamp_ms=hw["close_J"],
                        blocked="bell" if hw["touch"] else "", harvest=None)
        else:
            adv = opp = None
            want_stop = stop
            if hw["latch"] is not None:
                adv, opp = hand_trail(s, J, d, stop)
                if adv is not None:
                    want_stop = float(adv.new_stop)
            want_adv = [] if adv is None else [dataclasses.astuple(adv)]
            if J >= X["hi_i"]:
                path = "corridor-end-at-J"
                want = dict(common, exit_reason="corridor_end", exit_i=J,
                            exit_px=float(X["c"][J]), harvest=hw["harv"], final_stop=want_stop)
            else:
                path = "carry"
                want = {}
                snap = leg.get("state_after_J")
                ws = {"stop": want_stop, "reached_1r": hw["latch"] is not None,
                      "trail_armed": hw["latch"] is not None, "h_armed": hw["h_armed"],
                      "mfe": hw["mfe"], "mae": hw["mae"], "mae_to_1r": hw["m1r"],
                      "harv": hw["harv"], "n_opp": int(opp or 0), "blocked": "",
                      "latch_1h_ms": hw["latch"],
                      "latch_1h_by": "1h" if hw["latch"] is not None else None,
                      "plus1r_1h_ms": hw["plus"], "mismatch_ms": []}
                if snap is None:
                    bad.append(f"RELAY-J {lab} [carry]: no state_after_J")
                else:
                    bad += [f"RELAY-J {lab} [carry]: state {k} got {snap.get(k)!r}, hand {v!r}"
                            for k, v in ws.items() if snap.get(k) != v]
                    if adv_rows(snap["advances"]) != want_adv:
                        bad.append(f"RELAY-J {lab} [carry]: state advances "
                                   f"{len(snap['advances'])}, hand {len(want_adv)}")
                # GLUE: v6's one-bar state from the same (entry, stop, R) at J-1
                v1 = T9._ride_leg9(s, CARD, ROLES, d, J - 1, e, stop, R, J)
                if v1["exit_reason"] == "corridor_end":
                    adv_w = float(X["l"][J]) if d == 1 else float(X["h"][J])
                    vs = (v1["final_stop"], adv_rows(v1["advances"]), v1["harvest"], v1["mfe"],
                          v1["mae"], v1["reached_1r"], min(0.0, (adv_w - e) * d / R),
                          v1["n_opportunities"])
                    hs = (want_stop, want_adv, hw["harv"], hw["mfe"], hw["mae"],
                          hw["latch"] is not None, hw["m1r"], int(opp or 0))
                    if vs == hs:
                        n_glue += 1
                        full = T9._ride_leg9(s, CARD, ROLES, d, J - 1, e, stop, R, X["hi_i"])
                        bad += [f"RELAY-GLUE {lab}: {k} got {leg.get(k)!r}, v6 from the same "
                                f"state {full[k]!r}" for k in GLUE_KEYS if leg.get(k) != full[k]]
                        if adv_rows(leg["advances"]) != adv_rows(full["advances"]):
                            bad.append(f"RELAY-GLUE {lab}: advances {len(leg['advances'])} vs v6 "
                                       f"{len(full['advances'])}")
        paths[path] = paths.get(path, 0) + 1
        bad += [f"RELAY-J {lab} [{path}]: {k} got {leg.get(k)!r}, hand {v!r}"
                for k, v in want.items() if leg.get(k) != v]
    for cls, k in (("stop-in-J", paths.get("stop-in-J", 0)), ("bell-at-J", paths.get("bell-at-J", 0)),
                   ("carry", paths.get("carry", 0)), ("latched in J", n_latch),
                   ("harvest touch", n_touch), ("glue", n_glue)):
        if k < 1:
            bad.append(f"RELAY-J: the population holds no '{cls}' relay — the leg is vacuous there")
    return bad, (f"(b) {n} relays (every v6 campaign x J in {{ti, ti+1, ti+2}} x the close of "
                 f"child 0/1/2) hand-walked on this file's own read — relay_entry (1h, the 1h "
                 f"close, as-of J-1) and relay_stop (struct_stop_4h as of J-1) on every one; "
                 f"paths {dict(sorted(paths.items()))}; latched in J {n_latch}; harvest touches "
                 f"{n_touch}; mismatch J {n_mm} (F-MISMATCH-1H); no struct stop {n_none}; GLUE "
                 f"{n_glue} carried relays whose state after J equals v6's one-bar state continue "
                 f"exactly as tierc9._ride_leg9")


def relay_trail_findings(rd=RD) -> tuple[list[str], str]:
    """(c) every (2,2) pivot confirming at a bar J where a relay (child 0/1/2
    close, both directions) latched in J, did not stop, and J does not bell: the
    state after J carries v6's trail step at J on the hand-walked stop."""
    bad = []
    n = n_adv = 0
    for s in E.CLASSIC5:
        X = own4(s)
        fr = T9.fractals(s, *TRAIL_LR)
        lo_i = max(X["lo_i"], ROLES.floor_bars)
        for d in (1, -1):
            src = fr.low_by_conf if d == 1 else fr.high_by_conf
            for J in sorted(k for k in src if lo_i + 1 <= k < X["hi_i"]):
                ks = own_kids(s, J)
                if ks is None:
                    continue
                for ke in (0, 1, 2):
                    e = float(own1(s)["c"][ks[ke]])
                    stp, _ = hand_stop(s, J - 1, e, d)
                    if stp is None:
                        continue
                    stop, R = float(stp.stop_px), float(stp.r_dist)
                    hw = hand_relay_J(s, d, J, ke, e, stop, R)
                    if hw["xk"] is not None or hw["latch"] is None or hw["bell"]:
                        continue
                    adv, opp = hand_trail(s, J, d, stop)
                    leg = rd.relay11(s, CARD, ROLES, d, int(X["om"][J]) + (ke + 1) * H1, e,
                                     stop, R, X["hi_i"])
                    st = leg.get("state_after_J")
                    n += 1
                    n_adv += adv is not None
                    want_stop = float(adv.new_stop) if adv is not None else stop
                    lab = f"{s} {'L' if d == 1 else 'S'} J {iso(X['om'][J])} child {ke}"
                    if st is None or st["stop"] != want_stop or st["n_opp"] != int(opp) \
                            or adv_rows(st["advances"]) != ([] if adv is None
                                                            else [dataclasses.astuple(adv)]) \
                            or st["trail_armed"] is not True:
                        bad.append(f"RELAY-TRAIL {lab}: state after J "
                                   f"{None if st is None else (st['stop'], st['n_opp'], len(st['advances']), st['trail_armed'])}"
                                   f", v6's trail at J {(want_stop, int(opp), int(adv is not None), True)}")
    if n_adv < 1:
        bad.append("RELAY-TRAIL: no relay's trail advances at J — the leg is vacuous")
    return bad, (f"(c) {n} latched relays with a (2,2) pivot confirming at J: the state after J "
                 f"carries v6's trail step on every one ({n_adv} advance the stop at J)")


def split_findings(rd=RD) -> tuple[list[str], str]:
    """(d) every v6 campaign split after every bar m in (ti, exit): the state
    after m (truncated _ride_leg9 + this file's h_armed / mae_to_1r loop)
    injected into ride11 from m+1 == the untruncated _ride_leg9."""
    bad = []
    n = 0
    keys = GLUE_KEYS
    for t in base():
        s, d, e = t.symbol, int(t.direction), float(t.entry_px)
        X = own4(s)
        ti, R, stop0 = int(t.entry_i), float(t.r_dist), float(t.stop_px)
        full = T9._ride_leg9(s, CARD, ROLES, d, ti, e, stop0, R, X["hi_i"])
        h_armed, m1r, reached = False, 0.0, False
        for m in range(ti + 1, int(t.exit_i)):
            if not h_armed and outside(float(X["c"][m - 1]), band_edge(s, m - 1, d), d):
                h_armed = True
            fav = float(X["h"][m]) if d == 1 else float(X["l"][m])
            adv = float(X["l"][m]) if d == 1 else float(X["h"][m])
            if not reached:
                m1r = min(m1r, (adv - e) * d / R)
                if (fav - e) * d / R >= 1.0:
                    reached = True
            tr = T9._ride_leg9(s, CARD, ROLES, d, ti, e, stop0, R, m)
            lab = f"{s} {iso(t.entry_ms)} split after bar +{m - ti}"
            if tr["exit_reason"] != "corridor_end" or tr["reached_1r"] != reached:
                bad.append(f"SPLIT {lab}: the truncated v6 ride is not a state "
                           f"({tr['exit_reason']}, reached {tr['reached_1r']} vs {reached})")
                continue
            st = {"stop": tr["final_stop"], "advances": list(tr["advances"]),
                  "harv": tr["harvest"], "blocked": tr["blocked"], "mfe": tr["mfe"],
                  "mae": tr["mae"], "mae_to_1r": m1r, "reached_1r": reached,
                  "trail_armed": reached, "h_armed": h_armed,
                  "n_opp": tr["n_opportunities"], "latch_1h_ms": None, "latch_1h_by": None,
                  "plus1r_1h_ms": None, "mismatch_ms": []}
            got = rd.ride11(s, CARD, ROLES, d, ti, e, stop0, R, X["hi_i"], state=st, j0=m + 1)
            n += 1
            bad += [f"SPLIT {lab}: {k} got {got[k]!r}, v6 {full[k]!r}" for k in keys
                    if got[k] != full[k]]
            if adv_rows(got["advances"]) != adv_rows(full["advances"]):
                bad.append(f"SPLIT {lab}: advances {len(got['advances'])} vs v6 "
                           f"{len(full['advances'])}")
    return bad, (f"(d) {n} split points (every bar m strictly inside every v6 campaign): "
                 f"ride11 from the injected state after m == the untruncated _ride_leg9 on "
                 f"every key incl. the trail advances")


def relay_all(rd=RD, carry=None) -> tuple[list[str], str]:
    b0, t0 = relay_close_findings(rd)
    b1, t1 = relay_card_findings(rd, carry)
    b2, t2 = relay_trail_findings(rd)
    b3, t3 = split_findings(rd)
    return b0 + b1 + b2 + b3, f"{t0} · {t1} · {t2} · {t3}"


def drop_reached(st: dict) -> dict:
    out = RD.carry_state(st)
    out["reached_1r"] = False
    return out


def relay_break():
    return plants([
        ("a carry that drops reached_1r at J+1 (the carry= seam)", "state reached_1r",
         lambda: relay_all(carry=drop_reached)[0]),
        mutant("M1", "RELAY-STOP", lambda rd: relay_all(rd)[0]),
        mutant("M2", "state h_armed", lambda rd: relay_all(rd)[0]),
        mutant("M3", "state harv", lambda rd: relay_all(rd)[0]),
        mutant("M4", "state trail_armed", lambda rd: relay_all(rd)[0]),
        mutant("M8", "mae_to_1r", lambda rd: relay_all(rd)[0]),
        mutant("M11", "RELAY-GLUE", lambda rd: relay_all(rd)[0]),
        mutant("M12", "SPLIT", lambda rd: relay_all(rd)[0]),
        mutant("M13", "RELAY-TRAIL", lambda rd: relay_all(rd)[0]),
    ])


def relay_real():
    return verdict(*relay_all())


# ═══════════════════════════════════════════════════════════════ F-EXIT1H
def dead_walk(sym: str):
    """SABOTAGE: a walk that walks nothing — every bar to the parent, so every
    stop resolves at the 4h close."""
    W = RD.walk_of(sym)
    return dataclasses.replace(W, ok=np.zeros(len(W.ok), dtype=bool))


def exit1h_findings(walk_for=True) -> tuple[list[str], str, list]:
    book = walk_book(walk_for)
    bad, shown, hist = [], [], {}
    n_stop = n_bell = n_latch = 0
    for t in keyed(book):
        s, d = t.symbol, int(t.direction)
        om = T9.frame(s)["f"].open_ms
        X = int(om[t.exit_i])
        if t.latch_1h_ms is not None:
            n_latch += 1
            want_ls = int(t.latch_1h_ms) - (H4 if t.latch_1h_by == "parent" else 0)
            if t.latch_stamp_ms != want_ls:
                bad.append(f"EXIT1H {s} {iso(t.entry_ms)}: latch_stamp_ms {t.latch_stamp_ms}, "
                           f"want {want_ls} (L-R.5, latch by {t.latch_1h_by})")
        if t.exit_reason != "stop":
            n_bell += 1
            if t.exit_close_ms != X + H4 or t.exit_resolved_by != "close" \
                    or t.exit_stamp_ms != X + H4:
                bad.append(f"EXIT1H {s} {iso(t.entry_ms)} {t.exit_reason}: resolved "
                           f"{t.exit_resolved_by!r} at {t.exit_close_ms} stamp "
                           f"{t.exit_stamp_ms}, want the 4h close")
            continue
        n_stop += 1
        stop = float(t.exit_px)
        if not own_walkable(s, X):
            if t.exit_resolved_by != "parent" or t.exit_close_ms != X + H4 \
                    or t.exit_stamp_ms != X:
                bad.append(f"EXIT1H {s} {iso(t.entry_ms)}: mismatch bar resolved "
                           f"{t.exit_resolved_by!r} stamp {t.exit_stamp_ms}")
            hist["parent"] = hist.get("parent", 0) + 1
            continue
        ch = own_children(s, X)
        lows, highs = ch["low"].to_numpy(float), ch["high"].to_numpy(float)
        touch = [k for k in range(4)
                 if (d == 1 and lows[k] <= stop) or (d == -1 and highs[k] >= stop)]
        if not touch:
            bad.append(f"EXIT1H {s} {iso(t.entry_ms)}: no child touches the stop {stop!r}")
            continue
        k = touch[0]
        want = int(ch["open_time"].iloc[k]) + H1
        hist[k] = hist.get(k, 0) + 1
        if t.exit_close_ms != want or t.exit_resolved_by != "1h" or t.exit_stamp_ms != want:
            bad.append(f"EXIT1H {s} {iso(t.entry_ms)}: resolved {t.exit_resolved_by!r} at "
                       f"{iso(t.exit_close_ms)} (stamp {t.exit_stamp_ms}), hand-walked child {k} "
                       f"closing {iso(want)} (no earlier child touches)")
        if k != 3 and len(shown) < 3 and s not in {x[0] for x in shown}:
            ext = lows if d == 1 else highs
            shown.append((s, f"{s} {'long' if d == 1 else 'short'} {iso(t.entry_ms)} exit "
                             f"bar {iso(X)} stop {stop:.8g}: child "
                             f"{'lows' if d == 1 else 'highs'} "
                             f"{[round(float(x), 8) for x in ext]} -> first touch child {k} "
                             f"(close {iso(want)}) == ride {iso(t.exit_close_ms)}"))
    return bad, (f"{n_stop} stop exits hand-walked on this file's own 1h read (first "
                 f"touching child: {dict(sorted(hist.items(), key=str))}); {n_bell} bell "
                 f"exits at the 4h close; L-R.5 exit stamps on all {len(book)} and latch stamps "
                 f"on all {n_latch} latched"), [x[1] for x in shown]


def stop_parent_findings(rd=RD) -> tuple[list[str], str]:
    """EVERY v6 stop exit whose exit bar is own-walkable, that bar PLANTED as a
    mismatch bar (mismatch_walk): the parent decides — v6's exit exactly,
    resolved 'parent' at the 4h close, STAMPED at the bar's open (L-R.5), the
    bar counted."""
    bad, n = [], 0
    for t in keyed(base()):
        s, d, X = t.symbol, int(t.direction), int(t.exit_i)
        if t.exit_reason != "stop" or own_kids(s, X) is None:
            continue
        got = rd.ride_campaign(inp_of(t), CARD, ROLES, walk=mismatch_walk(s, X, d))
        o4 = int(own4(s)["om"][X])
        n += 1
        g = (got.exit_reason, int(got.exit_ms), float(got.exit_px), float(got.net_r),
             got.exit_close_ms, got.exit_resolved_by, got.exit_stamp_ms, o4 in got.walk_mismatch_ms)
        w = ("stop", int(t.exit_ms), float(t.exit_px), float(t.net_r), o4 + H4, "parent", o4, True)
        if g != w:
            bad.append(f"EXIT-PARENT {s} {iso(t.entry_ms)}: (reason, bar, px, net_r, instant, by, "
                       f"stamp, counted) {g}, want {w}")
    if n < 1:
        bad.append("EXIT-PARENT: vacuous")
    return bad, (f"{n} v6 stop bars planted as mismatch bars: v6's exit exactly, resolved "
                 f"'parent' at the 4h close, stamped at the bar's open, counted")


def exit1h_break():
    return plants([
        ("a walk that resolves every stop at the 4h close (walks nothing)", "hand-walked child",
         lambda: exit1h_findings(walk_for=dead_walk)[0]),
        mutant("M17", "EXIT-PARENT", lambda rd: stop_parent_findings(rd)[0]),
    ])


def exit1h_real():
    bad, txt, shown = exit1h_findings()
    if len(shown) < 3:
        bad.append(f"only {len(shown)} hand-walk examples with the touch before child 3")
    for x in shown:
        say(f"    hand-walked: {x}")
    b2, t2 = stop_parent_findings()
    return verdict(bad + b2, f"{txt} · {t2}")


# ═══════════════════════════════════════════════════════════ F-MISMATCH-1H
def corridor_mismatch_bars() -> list:
    """Every CLASSIC5 corridor 4h bar THIS file's walk law finds mismatched."""
    if "mmbars" not in _C:
        out = []
        for s in E.CLASSIC5:
            X = own4(s)
            for J in range(X["lo_i"], X["hi_i"] + 1):
                if own_kids(s, J) is None:
                    out.append((s, J))
        _C["mmbars"] = out
    return _C["mmbars"]


def relay_mismatch_findings(rd=RD) -> tuple[list[str], str]:
    """(a) a relay entry at the close of child 0/1/2 of every real corridor
    mismatch bar J, both directions: moved to the parent's close at its close
    price, as-of J; refused on the trigger close; its ride == _ride_leg9 from J
    and the bar counted."""
    bad = []
    n = n_ride = 0
    for s, J in corridor_mismatch_bars():
        X = own4(s)
        close_J = int(X["om"][J]) + H4
        for ke in (0, 1, 2):
            te = int(X["om"][J]) + (ke + 1) * H1
            lab = f"{s} J {iso(X['om'][J])} child {ke}"
            try:
                re_ = rd.relay_entry(s, te)
                re_on = rd.relay_entry(s, te, trigger_close_ms=close_J)
                re_after = rd.relay_entry(s, te, trigger_close_ms=close_J + H4)
            except SystemExit as ex:
                bad.append(f"RELAY-MISMATCH {lab}: relay_entry HALTed — {ex}")
                continue
            n += 1
            want = {"J": J, "moved": True, "entry_close_ms": close_J,
                    "entry_px": float(X["c"][J]), "asof_i": J}
            bad += [f"RELAY-MISMATCH {lab}: {k} got {re_.get(k)!r}, want {v!r} (L-W.0: the "
                    f"parent's close)" for k, v in want.items() if re_.get(k) != v]
            if re_on.get("refused") is None:
                bad.append(f"RELAY-MISMATCH {lab}: moved onto the trigger close, not refused")
            if re_after.get("refused") is not None:
                bad.append(f"RELAY-MISMATCH {lab}: refused with the trigger a bar later")
            for d in (1, -1):
                stp, atr = hand_stop(s, J, float(X["c"][J]), d)
                got_stp, got_atr = rd.relay_stop(s, re_["asof_i"], re_["entry_px"], d, CARD)
                if (stp is None) != (got_stp is None) or (
                        stp is not None and (got_stp.stop_px, got_stp.r_dist, got_atr)
                        != (stp.stop_px, stp.r_dist, atr)):
                    bad.append(f"RELAY-MISMATCH {lab} d {d}: relay_stop is not struct_stop_4h "
                               f"as of J")
                if stp is None or J >= X["hi_i"]:
                    continue
                leg = rd.relay11(s, CARD, ROLES, d, close_J, float(X["c"][J]), stp.stop_px,
                                 stp.r_dist, X["hi_i"], moved=True)
                ref = T9._ride_leg9(s, CARD, ROLES, d, J, float(X["c"][J]), stp.stop_px,
                                    stp.r_dist, X["hi_i"])
                n_ride += 1
                bad += [f"RELAY-MISMATCH {x}" for x in
                        leg_diff(leg, ref, f"{lab} d {d} ride vs _ride_leg9 from J",
                                 keys=tuple(k for k in ref if k != "advances"))]
                if leg["walk_mismatch_ms"] != [int(X["om"][J])] or leg["n_walk_mismatch"] != 1:
                    bad.append(f"RELAY-MISMATCH {lab} d {d}: the moved bar is not counted "
                               f"({leg['walk_mismatch_ms']})")
    t0 = next(t for t in base() if own_kids(t.symbol, int(t.entry_i)) is not None)
    X0 = own4(t0.symbol)
    try:                                     # a corrupted input: moved=True on a WALKABLE bar
        rd.relay11(t0.symbol, CARD, ROLES, int(t0.direction),
                   int(X0["om"][int(t0.entry_i)]) + H4, float(t0.entry_px), float(t0.stop_px),
                   float(t0.r_dist), X0["hi_i"], moved=True)
        bad.append("RELAY-MISMATCH moved guard: relay11(moved=True) at a WALKABLE bar's close "
                   "was ridden, not refused")
    except SystemExit as ex:
        if "flagged moved" not in str(ex):
            bad.append(f"RELAY-MISMATCH moved guard: a HALT, but not the guard's: {ex}")
    if n < 1:
        bad.append("RELAY-MISMATCH: no corridor mismatch bar — the leg is vacuous")
    return bad, (f"(a) {len(corridor_mismatch_bars())} real corridor mismatch bars x child 0-2: "
                 f"{n} relay entries moved to the parent's close (price, as-of J, refused on the "
                 f"trigger close); {n_ride} rides (both directions) == _ride_leg9 from J, the bar "
                 f"counted")


def walk_twin(t):
    """The walk-ON (hooks off) twin of a v6 campaign."""
    if "wb_by_key" not in _C:
        _C["wb_by_key"] = {(x.symbol, int(x.entry_ms)): x for x in walk_book_real()}
    return _C["wb_by_key"][(t.symbol, int(t.entry_ms))]


def add_mismatch_cases() -> list:
    """Every latched v6 campaign whose own parent latch bar Lb holds the walk's
    latch, with Y = Lb + 1 an own-walkable bar strictly before the exit bar."""
    wb = {(t.symbol, int(t.entry_ms)): t for t in walk_book_real()}
    out = []
    for t in keyed(base()):
        tw = wb[(t.symbol, int(t.entry_ms))]
        Lb = own_latch_bar(t)
        if tw.latch_1h_ms is None or Lb is None:
            continue
        X = own4(t.symbol)
        if not (int(X["om"][Lb]) < int(tw.latch_1h_ms) <= int(X["om"][Lb]) + H4):
            continue
        Y = Lb + 1
        if Y < int(t.exit_i) and own_kids(t.symbol, Y) is not None:
            out.append((t, Y))
    return out


def add_mismatch_findings(rd=RD) -> tuple[list[str], str]:
    """(b) an add event at child 1's close of a planted mismatch bar Y after the
    latch: admitted AT THE PARENT'S CLOSE and price (Add.i = Y), the v6 leg kept,
    the bar counted, and the campaign booked to the hand calculation."""
    bad = []
    cases = add_mismatch_cases()
    for t, Y in cases:
        s, d = t.symbol, int(t.direction)
        X = own4(s)
        lab = f"{s} {iso(t.entry_ms)} Y {iso(X['om'][Y])}"
        Wp = mismatch_walk(s, Y, d)
        ms = int(X["om"][Y]) + 2 * H1
        got = rd.ride_campaign(inp_of(t), CARD, ROLES, walk=Wp,
                               add_events=[(ms, own_1h_close(s, ms))])
        want_add = (Y, int(X["om"][Y]) + H4, float(X["c"][Y]), 0.5)
        adm = [(int(a.i), int(a.ms), float(a.px), float(a.size)) for a in got.adds]
        if adm != [want_add]:
            bad.append(f"ADD-MISMATCH {lab}: admitted {adm}, want {[want_add]} (L-W.0: the "
                       f"parent's close and price)")
        dd = got.add_dispositions[0] if got.add_dispositions else {}
        if dd.get("disposition") != "admitted" or dd.get("moved_to_parent_close") is not True:
            bad.append(f"ADD-MISMATCH {lab}: disposition {dd.get('disposition')!r} moved "
                       f"{dd.get('moved_to_parent_close')!r}")
        if (int(got.exit_ms), float(got.exit_px), got.exit_reason) != \
                (int(t.exit_ms), float(t.exit_px), t.exit_reason):
            bad.append(f"ADD-MISMATCH {lab}: the v6 leg moved")
        want_mm = sorted(list(walk_twin(t).walk_mismatch_ms) + [int(X["om"][Y])])
        if list(got.walk_mismatch_ms) != want_mm:
            bad.append(f"ADD-MISMATCH {lab}: mismatch bars {got.walk_mismatch_ms}, want the "
                       f"book's own plus Y {want_mm}")
        hand = add_hand(t, [(want_add[1], want_add[2])])
        for k in ("net_r", "add_r", "funding_r", "funding_r_uncapped"):
            if float(getattr(got, k) or 0.0) != float(hand[k]):
                bad.append(f"ADD-MISMATCH {lab}: {k} {getattr(got, k)!r} vs hand {hand[k]!r}")
    if not cases:
        bad.append("ADD-MISMATCH: no eligible campaign — the leg is vacuous")
    return bad, (f"(b) {len(cases)} latched v6 campaigns, an add at child 1 of a planted "
                 f"mismatch bar after the latch: admitted at the parent's close and price, "
                 f"booked == the hand calculation, the v6 leg kept, the bar counted")


def warn_plant(sym: str, Wp, bar: int, d: int):
    """Counter crosses on the four children of `bar` (and nowhere else)."""
    n = len(Wp.h1.open_ms)
    up, dn = np.zeros(n, dtype=bool), np.zeros(n, dtype=bool)
    a = int(Wp.a[bar])
    (dn if d == 1 else up)[a:a + 4] = True
    return RD.Warn(up, dn, WARN_LBL)


def warn_mismatch_findings(rd=RD) -> tuple[list[str], str]:
    """(c) every latched v6 campaign whose own parent latch bar Lb is walkable
    and before the exit bar: Lb planted mismatch + a counter cross on each of its
    children -> NO warn (the parent latched at the top of the bar); the ride is
    v6's, the latch parent-decided (stamped at the bar's open).  And, where Lb-1
    is an in-trade walkable bar, the same plant on Lb-1 -> the warn exit at
    Lb-1's close (the parent's close price)."""
    bad = []
    n1 = n2 = 0
    wb = {(t.symbol, int(t.entry_ms)): t for t in walk_book_real()}
    for t in keyed(base()):
        tw = wb[(t.symbol, int(t.entry_ms))]
        Lb = own_latch_bar(t)
        s, d = t.symbol, int(t.direction)
        if tw.latch_1h_ms is None or Lb is None or Lb >= int(t.exit_i) \
                or own_kids(s, Lb) is None:
            continue
        X = own4(s)
        lab = f"{s} {iso(t.entry_ms)} Lb {iso(X['om'][Lb])}"
        Wp = mismatch_walk(s, Lb, d)
        got = rd.ride_campaign(inp_of(t), CARD, ROLES, walk=Wp, warn=warn_plant(s, Wp, Lb, d))
        n1 += 1
        if (got.exit_reason, int(got.exit_ms), float(got.exit_px), float(got.net_r)) != \
                (t.exit_reason, int(t.exit_ms), float(t.exit_px), float(t.net_r)):
            bad.append(f"WARN-MISMATCH {lab}: a cross on the parent-latched bar moved the exit "
                       f"to {got.exit_reason!r} {iso(got.exit_ms)} (v6 {t.exit_reason!r} "
                       f"{iso(t.exit_ms)})")
        want = {"latch_1h_by": "parent", "latch_1h_ms": int(X["om"][Lb]) + H4,
                "latch_stamp_ms": int(X["om"][Lb]),
                "walk_mismatch_ms": sorted(list(tw.walk_mismatch_ms) + [int(X["om"][Lb])])}
        bad += [f"WARN-MISMATCH {lab}: {k} got {getattr(got, k)!r}, want {v!r}"
                for k, v in want.items() if getattr(got, k) != v]
        P = Lb - 1
        if P > int(t.entry_i) and own_kids(s, P) is not None:
            Wq = mismatch_walk(s, P, d)
            g2 = rd.ride_campaign(inp_of(t), CARD, ROLES, walk=Wq, warn=warn_plant(s, Wq, P, d))
            n2 += 1
            w2 = {"exit_reason": WARN_LBL, "exit_ms": int(X["om"][P]),
                  "exit_px": float(X["c"][P]), "exit_close_ms": int(X["om"][P]) + H4,
                  "exit_stamp_ms": int(X["om"][P]) + H4, "exit_resolved_by": "parent",
                  "latch_1h_ms": None, "acted_by": "warn"}
            bad += [f"WARN-MISMATCH {lab} (bar before): {k} got {getattr(g2, k)!r}, want {v!r}"
                    for k, v in w2.items() if getattr(g2, k) != v]
    if n1 < 1 or n2 < 1:
        bad.append(f"WARN-MISMATCH: vacuous ({n1} latch-bar / {n2} bar-before cases)")
    return bad, (f"(c) {n1} latched v6 campaigns, a counter cross on the planted-mismatch "
                 f"LATCH bar: no warn, v6's exit exactly, the latch parent-decided (stamped at "
                 f"the bar's open); {n2} with the same plant on the bar before: the warn exit "
                 f"at that parent's close")


def mismatch_all(rd=RD) -> tuple[list[str], str]:
    b1, t1 = relay_mismatch_findings(rd)
    b2, t2 = add_mismatch_findings(rd)
    b3, t3 = warn_mismatch_findings(rd)
    return b1 + b2 + b3, f"{t1} · {t2} · {t3}"


def mismatch_break():
    return plants([
        mutant("M5", "RELAY-MISMATCH", lambda rd: mismatch_all(rd)[0]),
        mutant("M6", "ADD-MISMATCH", lambda rd: mismatch_all(rd)[0]),
        mutant("M7", "WARN-MISMATCH", lambda rd: mismatch_all(rd)[0]),
        mutant("M15", "moved guard", lambda rd: mismatch_all(rd)[0]),
    ])


def mismatch_real():
    return verdict(*mismatch_all())


# ═══════════════════════════════════════════════════════════════ F-WARN-BOOK
def own_warn_cross(sym: str):
    k = ("wx", sym)
    if k not in _C:
        c = own1(sym)["c"]
        _C[k] = own_cross(own_ema(c, WARN_PAIR[0]), own_ema(c, WARN_PAIR[1]))
    return _C[k]


def hand_warn(t) -> dict:
    """THIS FILE'S WARN WALK of one v6 campaign [L-W.5]: per walkable bar, per
    child STOP -> the +1R latch -> the counter 12/89 cross while pre-+1R (exit at
    that 1h close, mae / mfe HELD through that child); a completed bar books
    v6's parent law; a mismatch bar: the parent's latch, stop, then the warn at
    its close over every child in the bar."""
    s, d, e, R = t.symbol, int(t.direction), float(t.entry_px), float(t.r_dist)
    X, Hh = own4(s), own1(s)
    up, dn = own_warn_cross(s)
    ctr = dn if d == 1 else up
    latch = None
    mfe, mae = e, 0.0
    for j in range(int(t.entry_i) + 1, int(t.exit_i) + 1):
        stp = stop_at(t, j)
        ks = own_kids(s, j)
        o4 = int(X["om"][j])
        close_j = o4 + H4
        fav_p = float(X["h"][j]) if d == 1 else float(X["l"][j])
        adv_p = float(X["l"][j]) if d == 1 else float(X["h"][j])
        if ks is not None:
            mae_b, mfe_b = mae, mfe
            for k in ks:
                hi_, lo_ = float(Hh["h"][k]), float(Hh["l"][k])
                fav, adv = (hi_, lo_) if d == 1 else (lo_, hi_)
                cm = int(Hh["t"][k]) + H1
                mae_b = min(mae_b, (adv - e) * d / R)
                if (d == 1 and lo_ <= stp) or (d == -1 and hi_ >= stp):
                    return dict(reason="stop", j=j, px=stp, ms=cm, stamp=cm, by="1h")
                if latch is None and (fav - e) * d / R >= 1.0:
                    latch = cm
                if (fav - e) * d > (mfe_b - e) * d:
                    mfe_b = fav
                if latch is None and ctr[k]:
                    return dict(reason=WARN_LBL, j=j, px=float(Hh["c"][k]), ms=cm, stamp=cm,
                                by="1h", mfe=mfe_b, mae=mae_b)
            mae = min(mae, (adv_p - e) * d / R)
            if (fav_p - e) * d > (mfe - e) * d:
                mfe = fav_p
        else:
            mae = min(mae, (adv_p - e) * d / R)
            if latch is None and (fav_p - e) * d / R >= 1.0:
                latch = close_j
            if (d == 1 and float(X["l"][j]) <= stp) or (d == -1 and float(X["h"][j]) >= stp):
                return dict(reason="stop", j=j, px=stp, ms=close_j, stamp=o4, by="parent")
            if (fav_p - e) * d > (mfe - e) * d:
                mfe = fav_p
            lo_k = int(np.searchsorted(Hh["t"], o4, "left"))
            hi_k = int(np.searchsorted(Hh["t"], o4 + H4, "left"))
            if latch is None and bool(ctr[lo_k:hi_k].any()):
                return dict(reason=WARN_LBL, j=j, px=float(X["c"][j]), ms=close_j,
                            stamp=close_j, by="parent", mfe=mfe, mae=mae)
    j = int(t.exit_i)
    return dict(reason=t.exit_reason, j=j, px=float(t.exit_px), ms=int(X["om"][j]) + H4,
                stamp=int(X["om"][j]) + H4, by="close")


def warn_book_findings(rd=RD) -> tuple[list[str], str]:
    bad = []
    for s in E.CLASSIC5:
        Wn = rd.warn_of(rd.walk_of(s))
        up, dn = own_warn_cross(s)
        if Wn.label != WARN_LBL or not (np.array_equal(Wn.up, up) and np.array_equal(Wn.dn, dn)):
            bad.append(f"WARN-BOOK {s}: warn_of's arrays ({Wn.label}, up {int(Wn.up.sum())} dn "
                       f"{int(Wn.dn.sum())}) are not this file's 1h EMA {WARN_PAIR[0]}/"
                       f"{WARN_PAIR[1]} crosses (up {int(up.sum())} dn {int(dn.sum())})")
    lo, hi = corridor()
    book = rd.transform_book(base(), CARD, ROLES, lo, hi, walk=True,
                             warn_of=lambda s: rd.warn_of(rd.walk_of(s)))
    nw = npar = 0
    for t, w in zip(base(), book):
        h = hand_warn(t)
        om = own4(t.symbol)["om"]
        lab = f"{t.symbol} {iso(t.entry_ms)}"
        got = (w.exit_reason, float(w.exit_px), w.exit_close_ms, int(w.exit_ms), w.exit_stamp_ms)
        want = (h["reason"], float(h["px"]), h["ms"], int(om[h["j"]]), h["stamp"])
        if got != want:
            bad.append(f"WARN-BOOK {lab}: (reason, px, instant, bar, stamp) {got}, hand {want}")
        if h["reason"] == WARN_LBL:
            nw += 1
            npar += h["by"] == "parent"
            R, e, d = float(t.r_dist), float(t.entry_px), int(t.direction)
            if w.mfe_r != (h["mfe"] - e) * d / R or w.mae_r != h["mae"] or w.reached_1r:
                bad.append(f"WARN-BOOK {lab}: held law mfe_r/mae_r/reached {w.mfe_r!r}/"
                           f"{w.mae_r!r}/{w.reached_1r!r}, hand {(h['mfe'] - e) * d / R!r}/"
                           f"{h['mae']!r}/False")
    idf, ist = rd.identity_findings(base(), book)
    bad += [f"WARN-BOOK identity: {x}" for x in idf]
    if nw < 1:
        bad.append("WARN-BOOK: no warn exit — the leg is vacuous")
    return bad, (f"warn_of's 1h {WARN_PAIR[0]}/{WARN_PAIR[1]} crosses == this file's plain-loop "
                 f"EMA crosses on {len(E.CLASSIC5)} assets; the whole CLASSIC5 warn book (n "
                 f"{len(book)}) == this file's hand walk on reason, price, instant, bar and "
                 f"L-R.5 stamp; {nw} warn exits ({npar} on a mismatch parent) with mfe_r / "
                 f"mae_r under the held law exactly; identity {ist}")


def warn_break():
    return plants([
        mutant("W1", "WARN-BOOK", lambda rd: warn_book_findings(rd)[0]),
        mutant("W2", "WARN-BOOK", lambda rd: warn_book_findings(rd)[0]),
    ])


def warn_real():
    return verdict(*warn_book_findings())


# ═══════════════════════════════════════════════════════════════ F-ORDER
def nan_levels(sym: str) -> np.ndarray:
    return np.full(len(T9.frame(sym)["f"].c), np.nan)


def tp_of(sym: str, X, lvl: float, d: int, mode: str = "record") -> RD.TPLevels:
    lv = nan_levels(sym)
    for x in ([X] if isinstance(X, (int, np.integer)) else X):
        lv[x] = lvl
    nn = nan_levels(sym)
    return RD.TPLevels(lv if d == 1 else nn, nn if d == 1 else lv, mode=mode)


def same_bar_findings(exit_order=RD.EXIT_ORDER, rd=RD) -> tuple[list[str], str]:
    """Every v6 stop exit whose exit bar admits a live, touched TP level (planted
    midway between max(prior close, entry x (1 + 10 bps)) and the bar's high;
    mirrored short): the STOP must win — v6's exit exactly."""
    bad, n = [], 0
    for inp, t in zip(inputs(), base()):
        if t.exit_reason != "stop":
            continue
        s, d, X = t.symbol, int(t.direction), int(t.exit_i)
        f = T9.frame(s)["f"]
        e, pc = float(t.entry_px), float(f.c[X - 1])
        if d == 1:
            lo_l = max(pc, e * (1 + GUARD))
            if not float(f.h[X]) > lo_l:
                continue
            lvl = (lo_l + float(f.h[X])) / 2
        else:
            hi_l = min(pc, e * (1 - GUARD))
            if not float(f.l[X]) < hi_l:
                continue
            lvl = (hi_l + float(f.l[X])) / 2
        n += 1
        got = rd.ride_campaign(inp, CARD, ROLES, tp=tp_of(s, X, lvl, d), exit_order=exit_order)
        tb, _ = raw_diff([got], [t], "SAME-BAR")
        if got.exit_reason != "stop":
            tb.append(f"SAME-BAR {s} {iso(t.entry_ms)}: got exit {got.exit_reason!r}, "
                      f"want exit 'stop'")
        c = got.tp_counts
        if exit_order == RD.EXIT_ORDER and (c["live"] != 1 or c["fill_blocked_by_stop"] != 1):
            tb.append(f"SAME-BAR {s} {iso(t.entry_ms)}: the planted TP was not live+touched "
                      f"({c}) — the plant tests nothing")
        bad += tb
    if n < 2:
        bad.append(f"SAME-BAR: only {n} eligible stop bars")
    return bad, f"{n} v6 stop bars with a live, touched TP planted: STOP wins on every one"


def bell_bars() -> list:
    """Every real bell bar X (from floor + 1 to the corridor end) of CLASSIC5 where
    a planted TP is live and touched: long w_dn|b_dn with high > close[X-1] x
    (1 + 10 bps); short w_up|b_up with low < close[X-1] x (1 - 10 bps)."""
    if "bells" in _C:
        return _C["bells"]
    out = []
    lo, hi = corridor()
    for s in E.CLASSIC5:
        f = T9.frame(s)["f"]
        ra = T9.role_arrays(s, ROLES)
        lo_i, hi_i = T7._idx_range(f.open_ms, lo, hi)
        for X in range(max(lo_i, ROLES.floor_bars) + 1, hi_i + 1):
            e = float(f.c[X - 1])
            if (ra["w_dn"][X] or ra["b_dn"][X]) and float(f.h[X]) > e * (1 + GUARD):
                out.append((s, X, 1, e, (e * (1 + GUARD) + float(f.h[X])) / 2))
            if (ra["w_up"][X] or ra["b_up"][X]) and float(f.l[X]) < e * (1 - GUARD):
                out.append((s, X, -1, e, (e * (1 - GUARD) + float(f.l[X])) / 2))
    _C["bells"] = out
    return out


def tp_bell_findings(exit_order=RD.EXIT_ORDER, rd=RD) -> tuple[list[str], str]:
    """Entry at close[X-1], stop 50 ATR away (never touched), the TP planted at X:
    the TP fills at max(level, open) (long) before the close's BELL; the v6
    reference (_ride_leg9, same entry/stop/R) must exit on that BELL."""
    bad, n, gaps = [], 0, 0
    for s, X, d, e, lvl in bell_bars():
        f = T9.frame(s)["f"]
        R = 50.0 * float(f.atr[X - 1])
        stop = e - R * d
        hi_i = hi_i_of(s)
        ref = T9._ride_leg9(s, CARD, ROLES, d, X - 1, e, stop, R, hi_i)
        if ref["exit_i"] != X or not ref["exit_reason"].startswith("bell"):
            bad.append(f"TP-BELL {s} {iso(f.open_ms[X])}: the v6 reference exits "
                       f"{ref['exit_reason']} at {ref['exit_i']} — the plant tests nothing")
            continue
        got = rd.ride11(s, CARD, ROLES, d, X - 1, e, stop, R, hi_i, tp=tp_of(s, X, lvl, d),
                        exit_order=exit_order)
        o = float(f.o[X])
        want_px = max(lvl, o) if d == 1 else min(lvl, o)
        gaps += int(want_px != lvl)
        n += 1
        if got["exit_reason"] != "tp" or got["exit_i"] != X or got["exit_px"] != want_px:
            bad.append(f"TP-BELL {s} {iso(f.open_ms[X])} d {d}: got exit "
                       f"{got['exit_reason']!r} at {got['exit_px']!r}, want exit 'tp' at "
                       f"{want_px!r}")
    if n < 2:
        bad.append(f"TP-BELL: only {n} eligible bell bars")
    return bad, (f"{n} real bell bars with a live, touched TP planted: TP fills first at "
                 f"max(level, open) on every one ({gaps} gap fill(s) at the open)")


def tp_mechanics_findings(rd=RD) -> tuple[list[str], str]:
    """On EVERY eligible bell bar: a level inside the guard (5 bps) is WITHHELD in
    'record' and fills 'unguarded'; a level on the far side of the prior close
    rests nowhere; 'post_harvest' withholds before any harvest.  Each withheld
    case must exit on the BELL."""
    bad, n = [], 0
    for s, X, d, e, lvl in bell_bars():
        f = T9.frame(s)["f"]
        R = 50.0 * float(f.atr[X - 1])
        stop = e - R * d
        hi_i = hi_i_of(s)
        inside = e * (1 + 0.5 * GUARD * d)
        far = e * (1 - 0.5 * GUARD * d)
        cases = (("guard/record", inside, "record", "bell", "guard_withheld"),
                 ("guard/unguarded", inside, "unguarded", "tp", None),
                 ("far side/record", far, "record", "bell", "far_side"),
                 ("post_harvest", lvl, "post_harvest", "bell", "preharvest_withheld"))
        for lab, L_, mode, want, cnt in cases:
            got = rd.ride11(s, CARD, ROLES, d, X - 1, e, stop, R, hi_i,
                            tp=tp_of(s, X, L_, d, mode))
            ok = got["exit_reason"].startswith(want) and (cnt is None
                                                           or got["tp_counts"][cnt] == 1)
            if want == "tp":
                o = float(f.o[X])
                ok = ok and got["exit_px"] == (max(L_, o) if d == 1 else min(L_, o))
            if not ok:
                bad.append(f"TP-MECH {lab} {s} {iso(f.open_ms[X])}: exit "
                           f"{got['exit_reason']!r} counts {got['tp_counts']}")
            n += 1
    return bad, (f"{n} guard / unguarded / far-side / post-harvest cases (4 on every one of "
                 f"{len(bell_bars())} bell bars) as the reading reads")


def gap_findings(rd=RD) -> tuple[list[str], str]:
    """EVERY corridor bar X of CLASSIC5 that OPENS beyond the prior close (up for a
    long, down for a short): entry 1% on the far side of close[X-1] (so the guard
    passes), stop 50 ATR away, a TP level planted strictly between close[X-1] and
    open[X] — live (near side) and gapped through: it must fill AT THE OPEN
    (max(level, open) long, min short), never at the level."""
    bad, n = [], 0
    lo, hi = corridor()
    for s in E.CLASSIC5:
        f = T9.frame(s)["f"]
        lo_i, hi_i = T7._idx_range(f.open_ms, lo, hi)
        for X in range(max(lo_i, ROLES.floor_bars) + 1, hi_i + 1):
            pc, o = float(f.c[X - 1]), float(f.o[X])
            if o == pc:
                continue
            d = 1 if o > pc else -1
            lvl = (pc + o) / 2
            if not ((lvl - pc) * d > 0 and (o - lvl) * d > 0):
                continue
            e = pc * (1 - 0.01 * d)
            R = 50.0 * float(f.atr[X - 1])
            got = rd.ride11(s, CARD, ROLES, d, X - 1, e, e - R * d, R, hi_i,
                            tp=tp_of(s, X, lvl, d))
            n += 1
            if got["exit_reason"] != "tp" or got["exit_i"] != X or got["exit_px"] != o:
                bad.append(f"GAP {s} {iso(f.open_ms[X])} d {d}: exit {got['exit_reason']!r} at "
                           f"{got['exit_px']!r}, want exit 'tp' at the open {o!r}")
    if n < 2:
        bad.append(f"GAP: only {n} gap bars")
    return bad, f"{n} real gap bars with a TP planted inside the gap: every one fills at the open"


def tp_live_level(sym: str, Z: int, e: float, d: int):
    """A level live and touched at bar Z: midway between max(close[Z-1], entry x
    (1 + guard)) and high[Z] (mirrored short), or None."""
    X = own4(sym)
    if d == 1:
        lo_l = max(float(X["c"][Z - 1]), e * (1 + GUARD))
        return (lo_l + float(X["h"][Z])) / 2 if float(X["h"][Z]) > lo_l else None
    hi_l = min(float(X["c"][Z - 1]), e * (1 - GUARD))
    return (hi_l + float(X["l"][Z])) / 2 if float(X["l"][Z]) < hi_l else None


def tp_harvest_findings(rd=RD) -> tuple[list[str], str]:
    """THE REMAINDER [L-H.1].  (i) every harvested v6 campaign, the first bar Z
    after the harvest bar (before the exit) admitting a live, touched TP: 'record'
    and 'post_harvest' both fill the 0.5 remainder at max(level, open[Z]); the
    harvest half keeps v6's harvest; net_r == the hand calculation; mfe capped at
    the fill.  (ii) every v6 campaign, the first bar Z before its harvest bar (and
    exit) admitting one: 'record' fills the whole 1.0 (no harvest), net_r == the
    hand calculation; 'post_harvest' withholds it and rides v6 exactly."""
    bad = []
    n_post = n_pre = 0
    for inp, t in zip(inputs(), base()):
        s, d, e, R = t.symbol, int(t.direction), float(t.entry_px), float(t.r_dist)
        X = own4(s)
        ti, xi = int(t.entry_i), int(t.exit_i)
        hi_ = int(t.harvest_i) if t.harvested else None
        lab = f"{s} {iso(t.entry_ms)}"
        # (i) after the harvest
        if hi_ is not None:
            Z = next(((z, lv) for z in range(hi_ + 1, xi)
                      if (lv := tp_live_level(s, z, e, d)) is not None), None)
            if Z is not None:
                z, lv = Z
                fill = max(lv, float(X["o"][z])) if d == 1 else min(lv, float(X["o"][z]))
                hand = hand_book(s, d, R, e, int(t.entry_ms), int(X["om"][z]), fill,
                                 harvest=(int(t.harvest_ms), float(t.harvest_px)))
                mfe = max([e] + [float(X["h"][j]) for j in range(ti + 1, z)] + [fill]) \
                    if d == 1 else min([e] + [float(X["l"][j]) for j in range(ti + 1, z)] + [fill])
                n_post += 1
                for mode in ("record", "post_harvest"):
                    got = rd.ride_campaign(inp, CARD, ROLES, tp=tp_of(s, z, lv, d, mode))
                    w = {"exit_reason": "tp", "exit_ms": int(X["om"][z]), "exit_px": fill,
                         "harvested": True, "harvest_ms": int(t.harvest_ms),
                         "harvest_px": float(t.harvest_px), "net_r": hand["net_r"],
                         "funding_r": hand["funding_r"], "mfe_r": (mfe - e) * d / R}
                    bad += [f"TP-HARVEST {lab} post-harvest [{mode}]: {k} got "
                            f"{getattr(got, k)!r}, hand {v!r}" for k, v in w.items()
                            if getattr(got, k) != v]
        # (ii) before the harvest
        top = min(hi_, xi) if hi_ is not None else xi
        Z = next(((z, lv) for z in range(ti + 1, top)
                  if (lv := tp_live_level(s, z, e, d)) is not None), None)
        if Z is None:
            continue
        z, lv = Z
        fill = max(lv, float(X["o"][z])) if d == 1 else min(lv, float(X["o"][z]))
        hand = hand_book(s, d, R, e, int(t.entry_ms), int(X["om"][z]), fill)
        n_pre += 1
        got = rd.ride_campaign(inp, CARD, ROLES, tp=tp_of(s, z, lv, d, "record"))
        w = {"exit_reason": "tp", "exit_ms": int(X["om"][z]), "exit_px": fill,
             "harvested": False, "net_r": hand["net_r"], "funding_r": hand["funding_r"]}
        bad += [f"TP-HARVEST {lab} pre-harvest [record]: {k} got {getattr(got, k)!r}, hand {v!r}"
                for k, v in w.items() if getattr(got, k) != v]
        g2 = rd.ride_campaign(inp, CARD, ROLES, tp=tp_of(s, z, lv, d, "post_harvest"))
        if (g2.exit_reason, int(g2.exit_ms), float(g2.exit_px), float(g2.net_r)) != \
                (t.exit_reason, int(t.exit_ms), float(t.exit_px), float(t.net_r)) \
                or g2.tp_counts["preharvest_withheld"] != 1:
            bad.append(f"TP-HARVEST {lab} pre-harvest [post_harvest]: exit {g2.exit_reason!r} "
                       f"{iso(g2.exit_ms)} counts {g2.tp_counts} — the twin must withhold and "
                       f"ride v6 ({t.exit_reason!r} {iso(t.exit_ms)})")
    if n_post < 1 or n_pre < 1:
        bad.append(f"TP-HARVEST: vacuous ({n_post} post-harvest / {n_pre} pre-harvest cases)")
    return bad, (f"{n_post} harvested v6 campaigns with a TP after the harvest (record and "
                 f"post_harvest fill the 0.5 remainder; net_r and funding == the hand "
                 f"calculation; mfe capped at the fill) · {n_pre} campaigns with a TP before "
                 f"the harvest (record fills the whole 1.0 == the hand calculation; post_harvest "
                 f"withholds and rides v6 exactly)")


def tp_rearm_findings(rd=RD) -> tuple[list[str], str]:
    """RE-ARMING [L-H.1]: every eligible corridor bar pair (X, X+1), both
    directions, with one level L at both bars where close[X-1] is BEYOND L (no
    order rests at X although the bar trades through L) and close[X] is back on
    the near side (the order rests at X+1 and fills at max(L, open[X+1]))."""
    bad, n = [], 0
    for s in E.CLASSIC5:
        X = own4(s)
        f = T9.frame(s)["f"]
        c, h, l, o = X["c"], X["h"], X["l"], X["o"]
        for x in range(max(X["lo_i"], ROLES.floor_bars) + 1, X["hi_i"]):
            for d in (1, -1):
                if bell_at(s, x, d) or bell_at(s, x + 1, d):
                    continue
                if d == 1:
                    cap = min(float(c[x - 1]), float(h[x]), float(h[x + 1]))
                    if not float(c[x]) < cap:
                        continue
                    L = (float(c[x]) + cap) / 2
                    e = min(float(c[x - 1]), float(c[x])) * 0.99
                else:
                    cap = max(float(c[x - 1]), float(l[x]), float(l[x + 1]))
                    if not float(c[x]) > cap:
                        continue
                    L = (float(c[x]) + cap) / 2
                    e = max(float(c[x - 1]), float(c[x])) * 1.01
                R = 50.0 * float(f.atr[x - 1])
                got = rd.ride11(s, CARD, ROLES, d, x - 1, e, e - R * d, R, X["hi_i"],
                                tp=tp_of(s, [x, x + 1], L, d))
                n += 1
                want_px = max(L, float(o[x + 1])) if d == 1 else min(L, float(o[x + 1]))
                if (got["exit_reason"], got["exit_i"], got["exit_px"]) != ("tp", x + 1, want_px) \
                        or got["tp_counts"]["far_side"] != 1 or got["tp_counts"]["live"] != 1:
                    bad.append(f"TP-REARM {s} {iso(X['om'][x])} d {d}: exit "
                               f"{got['exit_reason']!r} at bar +{got['exit_i'] - x} px "
                               f"{got['exit_px']!r} counts {got['tp_counts']}; want 'tp' at "
                               f"X+1 {want_px!r} (no order at X)")
    if n < 1:
        bad.append("TP-REARM: vacuous")
    return bad, (f"{n} real bar pairs: no order rests while the prior close is beyond the "
                 f"level (the bar trades through it), the order re-arms on the close back "
                 f"inside and fills at the next bar")


def tp_instant_findings(rd=RD) -> tuple[list[str], str]:
    """THE TP EXIT INSTANT under the walk, on every eligible bell bar: the close of
    the first own child reaching the level ('1h', stamped there); on an own
    mismatch bar the parent's close ('parent', stamped at the bar's OPEN)."""
    bad = []
    n = n_par = n_plant = 0
    for s, X, d, e, lvl in bell_bars():
        f = T9.frame(s)["f"]
        R = 50.0 * float(f.atr[X - 1])
        got = rd.ride11(s, CARD, ROLES, d, X - 1, e, e - R * d, R, hi_i_of(s),
                        tp=tp_of(s, X, lvl, d), walk=rd.walk_of(s))
        ks = own_kids(s, X)
        o4 = int(own4(s)["om"][X])
        if ks is not None:
            Hh = own1(s)
            k = next(k for k in ks if (d == 1 and Hh["h"][k] >= lvl)
                     or (d == -1 and Hh["l"][k] <= lvl))
            want = (int(Hh["t"][k]) + H1, "1h", int(Hh["t"][k]) + H1)
        else:
            n_par += 1
            want = (o4 + H4, "parent", o4)
        n += 1
        g = (got["exit_close_ms"], got["exit_resolved_by"], got["exit_stamp_ms"])
        if got["exit_reason"] != "tp" or g != want:
            bad.append(f"TP-INSTANT {s} {iso(o4)} d {d}: exit {got['exit_reason']!r} "
                       f"(instant, by, stamp) {g}, hand {want}")
        if ks is not None:                   # the same bar PLANTED as a mismatch bar
            gp = rd.ride11(s, CARD, ROLES, d, X - 1, e, e - R * d, R, hi_i_of(s),
                           tp=tp_of(s, X, lvl, d), walk=mismatch_walk(s, X, d))
            n_plant += 1
            g2 = (gp["exit_reason"], gp["exit_px"], gp["exit_close_ms"], gp["exit_resolved_by"],
                  gp["exit_stamp_ms"])
            w2 = ("tp", got["exit_px"], o4 + H4, "parent", o4)
            if g2 != w2:
                bad.append(f"TP-INSTANT {s} {iso(o4)} d {d} (planted mismatch): (reason, px, "
                           f"instant, by, stamp) {g2}, want {w2}")
    return bad, (f"{n} bell bars with the walk ON: the TP exit instant is the first child "
                 f"reaching the level ({n_par} on a real mismatch parent); the same {n_plant} "
                 f"bars planted as mismatch bars: the same fill, at the parent's close, stamped "
                 f"at the bar's open")


def warn_findings(child_order=RD.CHILD_ORDER) -> tuple[list[str], str]:
    """THE WARN EXIT on planted children of the order bar X (long, entry e =
    close[X-1], stop e - R, +1R e + R), one counter 12/89 cross planted per case:
      W1  cross on child 1, before any latch; the parent's stop comes on child 2
          -> WARN at child 1's close (= e), the HELD law (reached_1r False, mae
          and mfe through child 1 only);
      W2  child 1 prints +1R, the cross is ON the latch child -> no warn (post-
          +1R); child 2 stops -> STOP at child 2;
      W3  child 1 both stops and prints +1R, the cross on it -> STOP (adverse-
          first), no latch, no warn;
      W4  a MISMATCH bar (the high child lifted 1e-6 past the parent), stop 50
          ATR away, no +1R, cross on child 1 -> WARN at the PARENT's close."""
    s, X, e, R, stop, tgt, (O, H, L, C) = order_bar()
    hi_i = hi_i_of(s)
    f = T9.frame(s)["f"]
    a = int(RD.walk_of(s).a[X])
    bad, lab = [], RD.WARN_LABEL
    lo1, hi1 = min(O, e), max(O, e)
    cases = {
        "W1": ([(O, O, O, O), (O, hi1, lo1, e), (e, H, L, e), (e, max(e, C), min(e, C), C)],
               1, stop, R, {"exit_reason": lab, "exit_px": e, "exit_k": 1, "reached_1r": False,
                            "mae": min(0.0, (O - e) / R, (lo1 - e) / R), "mfe": max(e, O, hi1),
                            "exit_resolved_by": "1h", "latch": None}),
        "W2": ([(O, O, O, O), (O, H, lo1, e), (e, e, L, e), (e, max(e, C), min(e, C), C)],
               1, stop, R, {"exit_reason": "stop", "exit_px": stop, "exit_k": 2, "latch": 1,
                            "exit_resolved_by": "1h"}),
        "W3": ([(O, O, O, O), (O, H, L, e), (e, e, e, e), (e, max(e, C), min(e, C), C)],
               1, stop, R, {"exit_reason": "stop", "exit_px": stop, "exit_k": 1, "latch": None,
                            "exit_resolved_by": "1h"}),
    }
    real = RD.h1_tape(s)
    k_hi = a + int(np.argmax(real.h[a:a + 4]))          # the child carrying the parent's high
    lifted = [(float(real.o[k]), float(real.h[k]) * (1 + (1e-6 if k == k_hi else 0.0)),
               float(real.l[k]), float(real.c[k])) for k in range(a, a + 4)]
    R4 = 50.0 * float(f.atr[X - 1])
    cases["W4"] = (lifted, 1, e - R4, R4, {"exit_reason": lab, "exit_px": float(f.c[X]),
                                           "exit_k": None, "latch": None,
                                           "exit_resolved_by": "parent"})
    for name, (ch, k_x, stp, R_, want) in cases.items():
        Wp = RD.walk_of(s, h1=planted_tape(s, X, ch))
        if bool(Wp.ok[X]) != (name != "W4"):
            raise RuntimeError(f"{name}: the planted bar's walkability is not the case's")
        dn = np.zeros(len(Wp.h1.open_ms), dtype=bool)
        dn[a + k_x] = True
        wr = RD.Warn(np.zeros_like(dn), dn, lab)
        got = RD.ride11(s, CARD, ROLES, 1, X - 1, e, stp, R_, hi_i, walk=Wp, warn=wr,
                        child_order=child_order)
        cm = [Wp.h1.close_ms(a + k) for k in range(4)]
        exp = {"exit_reason": want["exit_reason"], "exit_px": want["exit_px"], "exit_i": X,
               "exit_resolved_by": want["exit_resolved_by"],
               "exit_close_ms": (cm[want["exit_k"]] if want["exit_k"] is not None
                                 else int(Wp.open4[X]) + H4),
               "latch_1h_ms": None if want["latch"] is None else cm[want["latch"]]}
        for k in ("reached_1r", "mae", "mfe"):
            if k in want:
                exp[k] = want[k]
        bad += [f"WARN-ORDER {name}: {k} got {got[k]!r}, hand-walked {v!r}"
                for k, v in exp.items() if got[k] != v]
    return bad, (f"{len(cases)} planted warn cases on {s} bar {iso(f.open_ms[X])}: W1 warn "
                 f"before a later stop (held law), W2 no warn on the latch child, W3 stop "
                 f"before warn, W4 a mismatch bar's warn at the parent's close")


def order_all(rd=RD) -> tuple[list[str], str]:
    parts = [same_bar_findings(rd=rd), tp_bell_findings(rd=rd), tp_mechanics_findings(rd),
             gap_findings(rd), tp_harvest_findings(rd), tp_rearm_findings(rd),
             tp_instant_findings(rd)]
    if rd is RD:
        parts.append(warn_findings())
    return [x for b, _ in parts for x in b], " · ".join(t for _, t in parts)


def order_break():
    return plants([
        ("EXIT_ORDER with TP before STOP, on the planted same-bar STOP+TP bars",
         "want exit 'stop'",
         lambda: same_bar_findings(exit_order=("tp", "stop", "warn", "bell"))[0]),
        ("EXIT_ORDER with BELL before TP, on the planted TP-then-BELL bars", "want exit 'tp'",
         lambda: tp_bell_findings(exit_order=("stop", "warn", "bell", "tp"))[0]),
        ("per-child order WARN before LATCH, on the planted cross on the latch child",
         "WARN-ORDER W2", lambda: warn_findings(child_order=("stop", "warn", "latch"))[0]),
        mutant("M9", "TP-INSTANT", lambda rd: order_all(rd)[0]),
        mutant("M10", "TP-HARVEST", lambda rd: order_all(rd)[0]),
        mutant("M14", "TP-REARM", lambda rd: order_all(rd)[0]),
        mutant("M16", "planted mismatch", lambda rd: order_all(rd)[0]),
    ])


def order_real():
    return verdict(*order_all())


# ═══════════════════════════════════════════════════════════════ F-ADD-ACCT
def add_campaign():
    """The real v6 campaign that reached +1R on the 1h walk with the largest
    uncapped funding (ties by key)."""
    wb = {(t.symbol, int(t.entry_ms)): t for t in walk_book_real()}
    cands = [t for t in keyed(base()) if wb[(t.symbol, int(t.entry_ms))].latch_1h_ms is not None]
    t = max(cands, key=lambda x: (float(x.funding_r_uncapped), x.symbol, -int(x.entry_ms)))
    return t, wb[(t.symbol, int(t.entry_ms))]


def add_events(t, tw) -> tuple[list, dict]:
    s = t.symbol
    ec, lt, xc = int(tw.entry_close_ms), int(tw.latch_1h_ms), int(tw.exit_close_ms)
    named = {"pre-entry": ec, "latch": lt, "latch+1h": lt + H1, "latch+2h": lt + 2 * H1,
             "exit": xc}
    if lt - H1 > ec:
        named["pre-latch"] = lt - H1
    if not (lt + 2 * H1 < xc):
        raise RuntimeError("the add campaign's latch is too close to its exit for 3 adds")
    W = RD.walk_of(s)
    om = T9.frame(s)["f"].open_ms
    for lab, ms in named.items():
        i = int(np.searchsorted(om, ms, "left")) - 1
        if not W.ok[i]:
            raise RuntimeError(f"add event {lab} {iso(ms)} sits on a mismatch bar — the "
                               f"plant would test L-W.0's move, not the booking")
    ev = [(ms, own_1h_close(s, ms)) for ms in named.values()]
    return ev, named


def own_fund(sym: str, lo_open: int, hi_open: int, d: int, qty: float) -> float:
    """sum over own 4h bars with lo_open < open <= hi_open of rate(open) x
    close[prev] x d x qty — funding from the NEXT 4h open."""
    b = own_bars(sym, "4h")
    om, c = b["open_time"].to_numpy(np.int64), b["close"].to_numpy(float)
    fund = own_funding(sym)
    s_ = 0.0
    for j in range(int(np.searchsorted(om, lo_open, "right")),
                   int(np.searchsorted(om, hi_open, "right"))):
        rate = fund.get(int(om[j]))
        if rate:
            s_ += rate * float(c[j - 1]) * d * qty
    return s_


def own_bar_of(sym: str, close_ms: int) -> int:
    """The open ms of the own 4h bar containing a 1h close."""
    b = own_bars(sym, "4h")["open_time"].to_numpy(np.int64)
    return int(b[int(np.searchsorted(b, close_ms, "left")) - 1])


def hand_book(sym: str, d: int, R: float, e: float, entry_open: int, exit_open: int,
              xpx: float, harvest=None, adds=()) -> dict:
    """THE HAND CALCULATION, on this file's own bars and funding: the leg (the
    harvest half at its fill, the rest at the exit), each add 0.5 from its 1h
    close to the exit, fees 5 bps a side, funding from the next 4h open, the D12
    ceiling once on the total."""
    if harvest is not None:
        h_open, hpx = harvest
        g1 = HARVEST_Q * (hpx - e) * d
        fe1 = BPS_SIDE * HARVEST_Q * (e + hpx)
        u1 = own_fund(sym, entry_open, h_open, d, HARVEST_Q)
        g2 = (1 - HARVEST_Q) * (xpx - e) * d
        fe2 = BPS_SIDE * (1 - HARVEST_Q) * (e + xpx)
        u2 = own_fund(sym, entry_open, exit_open, d, 1 - HARVEST_Q)
        g, fe, u = g1 + g2, fe1 + fe2, u1 + u2
    else:
        g = (xpx - e) * d
        fe = BPS_SIDE * (e + xpx)
        u = own_fund(sym, entry_open, exit_open, d, 1.0)
    add_r = 0.0
    for ms, px in adds:
        a_open = own_bar_of(sym, ms)
        g += 0.5 * (xpx - px) * d
        fe += BPS_SIDE * 0.5 * (px + xpx)
        ua = own_fund(sym, a_open, exit_open, d, 0.5)
        u += ua
        add_r += (0.5 * (xpx - px) * d - BPS_SIDE * 0.5 * (px + xpx) - ua) / R
    unc = u / R
    eff = min(unc, CEILING_R) if unc > CEILING_R else unc
    return {"gross_r": g / R, "fee_r": fe / R, "funding_r_uncapped": unc, "funding_r": eff,
            "net_r": g / R - fe / R - eff, "add_r": add_r, "bound": unc > CEILING_R}


def add_hand(t, adds_hand) -> dict:
    return hand_book(t.symbol, int(t.direction), float(t.r_dist), float(t.entry_px),
                     int(t.entry_ms), int(t.exit_ms), float(t.exit_px),
                     harvest=((int(t.harvest_ms), float(t.harvest_px)) if t.harvested
                              else None), adds=adds_hand)


def add_findings(max_adds: int = RD.ADDS_MAX) -> tuple[list[str], str]:
    t, tw = add_campaign()
    ev, named = add_events(t, tw)
    inp = inp_of(t)
    W = RD.walk_of(t.symbol)
    got = RD.ride_campaign(inp, CARD, ROLES, walk=W, add_events=ev, max_adds=max_adds)
    want_adm = [(named["latch"], own_1h_close(t.symbol, named["latch"])),
                (named["latch+1h"], own_1h_close(t.symbol, named["latch+1h"]))]
    bad = []
    adm = [(int(a.ms), float(a.px)) for a in got.adds]
    if adm != want_adm:
        bad.append(f"ADD: admitted {[(iso(m), p) for m, p in adm]}, hand-walked "
                   f"{[(iso(m), p) for m, p in want_adm]}")
    for a in got.adds:
        if a.size != 0.5 or int(T9.frame(t.symbol)["f"].open_ms[a.i]) != own_bar_of(t.symbol,
                                                                                    a.ms):
            bad.append(f"ADD: tranche {iso(a.ms)} size {a.size} bar {a.i} is not 0.5 in the "
                       f"4h bar containing its 1h close")
    want_disp = {named["pre-entry"]: "refused: pre-entry",
                 named["latch"]: "admitted", named["latch+1h"]: "admitted",
                 named["latch+2h"]: f"refused: cap {RD.ADDS_MAX} reached",
                 named["exit"]: "refused: not before the 1h-resolved exit"}
    if "pre-latch" in named:
        want_disp[named["pre-latch"]] = "refused: before the +1R latch"
    gd = {int(r["event_ms"]): r["disposition"] for r in got.add_dispositions}
    bad += [f"ADD: event {iso(m)} disposition {gd.get(m)!r}, want {w!r}"
            for m, w in want_disp.items() if gd.get(m) != w]
    hand = add_hand(t, want_adm)
    if not hand["bound"]:
        bad.append(f"ADD: the planted adds do not bind the D12 ceiling "
                   f"(uncapped {hand['funding_r_uncapped']:.6f}) — the plant tests less than "
                   f"it claims")
    for k in ("net_r", "gross_r", "fee_r", "funding_r", "funding_r_uncapped", "add_r"):
        dv = abs(float(getattr(got, k)) - float(hand[k]))
        if dv != 0.0:
            bad.append(f"ADD: {k} {float(getattr(got, k))!r} vs hand {hand[k]!r} "
                       f"(differs by {dv:.3e})")
    if got.funding_ceiling_bound is not True:
        bad.append("ADD: funding_ceiling_bound is not set")
    # L-1.5 x L-A.1 — the paired delta is NOT add_r when the ceiling binds
    delta = float(got.net_r) - float(t.net_r)
    absorbed = float(got.funding_r_uncapped) - float(got.funding_r)
    if t.funding_ceiling_bound or not same(delta - float(got.add_r), absorbed):
        bad.append(f"ADD-DELTA: net_r - v6 net_r {delta!r} - add_r {float(got.add_r)!r} is not "
                   f"the cap-absorbed funding {absorbed!r} (v6 bound {t.funding_ceiling_bound})")
    hb = t.harvest_i
    want_below = sum(1 for _, px in want_adm if (px - float(t.entry_px)) * t.direction < 0)
    want_post = sum(1 for ms, _ in want_adm
                    if hb is not None and own_bar_of(t.symbol, ms) >= int(t.harvest_ms))
    if (got.n_adds_below_entry, got.n_adds_post_harvest) != (want_below, want_post):
        bad.append(f"ADD: flags below-entry/post-harvest {got.n_adds_below_entry}/"
                   f"{got.n_adds_post_harvest} vs hand {want_below}/{want_post}")
    lo, hi = corridor()
    key = (t.symbol, int(t.entry_ms))
    book = RD.transform_book(base(), CARD, ROLES, lo, hi, walk=True,
                             adds_of=lambda k: ev if k == key else None, max_adds=max_adds)
    idf, ist = RD.identity_findings(base(), book)
    bad += idf
    if ist["acted"] != 1:
        bad.append(f"ADD: the add book has {ist['acted']} acted campaigns, want 1")
    return bad, (f"{t.symbol} {'long' if t.direction == 1 else 'short'} {iso(t.entry_ms)} "
                 f"(v6 funding {float(t.funding_r_uncapped):.6f} R, harvested {t.harvested}): "
                 f"{len(ev)} events -> admitted {[iso(m) for m, _ in adm]}; net_r "
                 f"{float(got.net_r):.6f} == hand {hand['net_r']:.6f} (v6 {float(t.net_r):.6f}); "
                 f"add_r {float(got.add_r):.6f}; funding uncapped "
                 f"{hand['funding_r_uncapped']:.6f} -> capped {float(got.funding_r):.6f}; "
                 f"L-1.5 x L-A.1: delta net_r - v6 = {delta:.6f} = add_r "
                 f"{float(got.add_r):.6f} + the cap-absorbed funding {absorbed:.6f} (AMENDMENT "
                 f"CANDIDATE: delta != add_r when the ceiling binds; the paired delta is scored "
                 f"on net_r); flags below-entry {got.n_adds_below_entry} post-harvest "
                 f"{got.n_adds_post_harvest}; identity over the whole add book {ist}")


def add_harvest_plant() -> tuple:
    """PLANT B: the first harvested v6 campaign (key order) that latched on the
    1h walk, whose harvest bar's first 1h child closes after the latch and
    before the 1h-resolved exit, and that has a 1h close on the losing side of
    entry after the latch and BEFORE the harvest bar (so the two classes are
    distinct events).  Events: that below-entry close, and the harvest bar's
    first child close (inside the harvest's 4h bar)."""
    wb = {(t.symbol, int(t.entry_ms)): t for t in walk_book_real()}
    for t in keyed(base()):
        tw = wb[(t.symbol, int(t.entry_ms))]
        if not (t.harvested and tw.latch_1h_ms is not None):
            continue
        s, d, e = t.symbol, int(t.direction), float(t.entry_px)
        W = RD.walk_of(s)
        om = T9.frame(s)["f"].open_ms
        hk = int(t.harvest_ms) + H1
        lt, xc = int(tw.latch_1h_ms), int(tw.exit_close_ms)
        if not (lt < hk < xc):
            continue
        d1 = own_bars(s, "1h")
        cl = d1["open_time"].to_numpy(np.int64) + H1
        cc = d1["close"].to_numpy(float)
        below = [int(m) for m, c in zip(cl, cc) if lt <= m <= int(t.harvest_ms)
                 and (c - e) * d < 0 and W.ok[int(np.searchsorted(om, m, "left")) - 1]]
        if not below or not W.ok[int(t.harvest_i)]:
            continue
        ev = sorted({below[0], hk})
        if len(ev) != 2:
            continue
        return t, tw, [(m, own_1h_close(s, m)) for m in ev], below[0], hk
    raise RuntimeError("no harvested add campaign")


def add_harvest_findings() -> tuple[list[str], str]:
    t, tw, ev, m_below, m_harv = add_harvest_plant()
    inp = inp_of(t)
    W = RD.walk_of(t.symbol)
    bad = []
    got = RD.ride_campaign(inp, CARD, ROLES, walk=W, add_events=ev)
    if [(int(a.ms), float(a.px)) for a in got.adds] != ev:
        bad.append(f"ADD-B: admitted {[(iso(a.ms), a.px) for a in got.adds]}, want both events")
    hand = add_hand(t, ev)
    for k in ("net_r", "gross_r", "fee_r", "funding_r", "funding_r_uncapped", "add_r"):
        dv = abs(float(getattr(got, k)) - float(hand[k]))
        if dv != 0.0:
            bad.append(f"ADD-B: {k} {float(getattr(got, k))!r} vs hand {hand[k]!r} "
                       f"(differs by {dv:.3e})")
    want_below = sum(1 for m, px in ev if (px - float(t.entry_px)) * t.direction < 0)
    want_post = sum(1 for m, _ in ev if own_bar_of(t.symbol, m) >= int(t.harvest_ms))
    if (got.n_adds_below_entry, got.n_adds_post_harvest) != (want_below, want_post) \
            or want_below < 1 or want_post < 1:
        bad.append(f"ADD-B: flags below-entry/post-harvest {got.n_adds_below_entry}/"
                   f"{got.n_adds_post_harvest} vs hand {want_below}/{want_post} (each >= 1)")
    below_of = {m: (px - float(t.entry_px)) * t.direction < 0 for m, px in ev}
    post_of = {m: own_bar_of(t.symbol, m) >= int(t.harvest_ms) for m, _ in ev}
    if not (below_of[m_below] and post_of[m_harv]):
        raise RuntimeError("PLANT B's events are not of their named classes")
    for opt, cls, lab in (("refuse_below_entry", below_of, "refused: below entry (twin)"),
                          ("refuse_post_harvest", post_of, "refused: post-harvest (twin)")):
        tw_ = RD.ride_campaign(inp, CARD, ROLES, walk=W, add_events=ev, add_opts={opt: True})
        dd = {int(r["event_ms"]): r["disposition"] for r in tw_.add_dispositions}
        want = {m: (lab if cls[m] else "admitted") for m, _ in ev}
        if dd != want or len(tw_.adds) != sum(1 for m in want if not cls[m]):
            bad.append(f"ADD-B twin {opt}: dispositions "
                       f"{ {iso(m): v for m, v in dd.items()} }, hand-walked "
                       f"{ {iso(m): v for m, v in want.items()} }")
    return bad, (f"{t.symbol} {'long' if t.direction == 1 else 'short'} {iso(t.entry_ms)} "
                 f"(harvested {iso(t.harvest_ms)}): adds at {iso(ev[0][0])}, {iso(ev[1][0])} "
                 f"-> net_r {float(got.net_r):.6f} == hand {hand['net_r']:.6f} (v6 "
                 f"{float(t.net_r):.6f}), add_r {float(got.add_r):.6f}; flags below-entry "
                 f"{got.n_adds_below_entry} post-harvest {got.n_adds_post_harvest}; both "
                 f"twins refuse their class")


def add_price_findings(rd=RD) -> tuple[list[str], str]:
    """THE ADD PRICE IS THE TAPE'S [L-A.1]: PLANT A's events with no caller
    price are admitted at the own 1h closes; a caller price that is not the 1h
    close of its event (bent by one part in 1e9) HALTs."""
    t, tw = add_campaign()
    ev, named = add_events(t, tw)
    inp = inp_of(t)
    W = rd.walk_of(t.symbol)
    bad = []
    got = rd.ride_campaign(inp, CARD, ROLES, walk=W, add_events=[(m, None) for m, _ in ev])
    want = [(named["latch"], own_1h_close(t.symbol, named["latch"])),
            (named["latch+1h"], own_1h_close(t.symbol, named["latch+1h"]))]
    if [(int(a.ms), float(a.px)) for a in got.adds] != want:
        bad.append(f"ADD-PRICE: with no caller price the adds are "
                   f"{[(iso(a.ms), a.px) for a in got.adds]}, want the 1h closes {want}")
    m0, p0 = want[0]
    try:
        g2 = rd.ride_campaign(inp, CARD, ROLES, walk=W, add_events=[(m0, p0 * (1 + 1e-9))])
        bad.append(f"ADD-PRICE: a caller price {p0 * (1 + 1e-9)!r} that is not the 1h close "
                   f"{p0!r} was accepted (booked at {[a.px for a in g2.adds]})")
    except SystemExit as ex:
        if "not the 1h close" not in str(ex):
            bad.append(f"ADD-PRICE: a HALT, but not the price law's: {ex}")
    return bad, ("no caller price -> the tape's 1h closes; a bent caller price HALTs "
                 "(L-A.1: the add enters at the 1h close of its event)")


def add_break():
    return plants([
        ("a 3rd add admitted (cap 3) on the planted campaign", "net_r",
         lambda: add_findings(max_adds=3)[0]),
        mutant("A1", "ADD-PRICE", lambda rd: add_price_findings(rd)[0]),
    ])


def add_real():
    b1, t1 = add_findings()
    b2, t2 = add_harvest_findings()
    b3, t3 = add_price_findings()
    return verdict(b1 + b2 + b3, f"PLANT A (the ceiling): {t1} · PLANT B (the harvest branch, "
                                 f"the flags, the twins): {t2} · THE PRICE: {t3}")


# ═══════════════════════════════════════════════════════════ F-CLOSURE-RIDE
def run_py(code: str, pre_path: str | None = None, timeout: int = 900):
    head = (f"import sys\nsys.dont_write_bytecode = True\n"
            f"sys.path.insert(0, {str(ROOT)!r})\nsys.path.insert(0, {str(ROOT / 'scripts')!r})\n")
    if pre_path:
        head += f"sys.path.insert(0, {pre_path!r})\n"
    env = dict(os.environ, NAIAD_CACHE_DIR=str(SNAP), PYTHONDONTWRITEBYTECODE="1")
    return subprocess.run([PY, "-B", "-c", head + code], capture_output=True, text=True,
                          env=env, cwd=str(ROOT), timeout=timeout)


def closure_of(pre_path: str | None = None) -> list[str]:
    r = run_py("import json\nimport tierc11_ride\nprint(json.dumps(sorted(sys.modules)))",
               pre_path=pre_path)
    if r.returncode != 0:
        raise RuntimeError(f"closure subprocess exit {r.returncode}: {r.stderr[-300:]}")
    for ln in reversed(r.stdout.strip().splitlines()):
        if ln.startswith("["):
            return json.loads(ln)
    raise RuntimeError("no module list")


def reach(mods) -> list[str]:
    return sorted(m for m in mods if any(x in m for x in FORBIDDEN))


def ast_findings(src: str) -> list[str]:
    """THIS file's AST walk: every Import / ImportFrom anywhere + constant-string
    import calls, matched on FORBIDDEN by substring; every attribute read named
    top / bottom (L-F.2: Range.top/.bottom is never read)."""
    out = []
    for n in ast.walk(ast.parse(src)):
        names = []
        if isinstance(n, ast.Import):
            names = [a.name for a in n.names]
        elif isinstance(n, ast.ImportFrom):
            names = [n.module or ""] + [a.name for a in n.names]
        elif (isinstance(n, ast.Call) and n.args and isinstance(n.args[0], ast.Constant)
              and isinstance(n.args[0].value, str)):
            fn = n.func.attr if isinstance(n.func, ast.Attribute) else getattr(n.func, "id", "")
            if fn in ("import_module", "__import__", "tc10_import", "_tc10_import"):
                names = [n.args[0].value]
        out += [f"AST import line {n.lineno}: {x}" for x in names
                if any(f in x for f in FORBIDDEN)]
        if isinstance(n, ast.Attribute) and n.attr in ("top", "bottom"):
            out.append(f"AST Range.top/.bottom read line {n.lineno}: .{n.attr}")
    return out


def shadow(td: Path, tail: str) -> Path:
    src = RIDE_SRC.read_text(encoding="utf-8")
    old = "ROOT = Path(__file__).resolve().parents[1]"
    if src.count(old) != 1:
        raise RuntimeError("the ride's ROOT line is not unique")
    (td / "tierc11_ride.py").write_text(src.replace(old, f"ROOT = Path({str(ROOT)!r})") + tail,
                                        encoding="utf-8")
    return td


def audit_observe(hook_first: bool = True) -> list[str]:
    """In a fresh interpreter, an `open` audit-event observer (installed BEFORE
    the ride is imported, or — the plant — after its reads) records every path
    opened while tierc11_ride reads BTCUSDT's 1h tape and builds its walk (which
    reads the 4h frame).  The ride's 1h parquet read must be SEEN on the TC11
    snapshot: its data I/O goes through the `open` event the audit hook sees."""
    hook = ("seen = []\n"
            "def _obs(ev, args):\n"
            "    if ev == 'open' and args and isinstance(args[0], (str, bytes, os.PathLike)):\n"
            "        seen.append(os.fsdecode(args[0]))\n")
    install = "sys.addaudithook(_obs)\n"
    code = ("import json, os\n" + hook + (install if hook_first else "")
            + "import tierc11_ride as RD\nRD.h1_tape('BTCUSDT')\nRD.walk_of('BTCUSDT')\n"
            + ("" if hook_first else install)
            + "print(json.dumps(sorted(set(seen))))\n")
    r = run_py(code)
    if r.returncode != 0:
        raise RuntimeError(f"audit subprocess exit {r.returncode}: {r.stderr[-300:]}")
    seen = json.loads(r.stdout.strip().splitlines()[-1])
    want = str(SNAP / "klines" / "BTCUSDT_1h.parquet")
    out = []
    if not any(os.path.realpath(p) == os.path.realpath(want) for p in seen):
        out.append(f"AUDIT-OBSERVE: the ride's 1h read ({Path(want).name}) raised no `open` "
                   f"audit event the observer saw ({len(seen)} opens seen)")
    bad = [p for p in seen if "tc10_20260921" in p or "/data_cache" in p]
    if bad:
        out.append(f"AUDIT-OBSERVE: opens outside the TC11 snapshot {bad[:3]}")
    return out


def closure_break():
    def fresh_plant():
        with tempfile.TemporaryDirectory() as td:
            d = shadow(Path(td), "\nimport engine.rangefinder  # PLANT\n")
            got = reach(closure_of(str(d)))
        return [f"fresh-interpreter closure holds {got}"] if got else []

    def lazy(tail):
        return lambda: ast_findings(RIDE_SRC.read_text(encoding="utf-8") + tail)

    return plants([
        ("a shadow tierc11_ride importing engine.rangefinder at top level",
         "fresh-interpreter closure holds", fresh_plant),
        ("a lazy in-function tierc10_census import (invisible to a closure)", "AST import",
         lazy("\n\ndef _plant():\n    import tierc10_census  # PLANT\n    return 0\n")),
        ("a lazy in-function tierc11_nest import", "AST import",
         lazy("\n\ndef _plant():\n    import tierc11_nest  # PLANT\n    return 0\n")),
        ("a planted Range.top read", "Range.top/.bottom",
         lazy("\n\ndef _plant(r):\n    return r.top  # PLANT\n")),
        ("an observer installed AFTER the ride's reads (a read it cannot see)",
         "AUDIT-OBSERVE", lambda: audit_observe(hook_first=False)),
    ])


def closure_real():
    mods = closure_of()
    hit = reach(mods)
    src = RIDE_SRC.read_text(encoding="utf-8")
    ah = ast_findings(src)
    esc = E.hook_escapes(src)
    obs = audit_observe(hook_first=True)
    have = "tierc11_env" in mods and "tierc9" in mods
    ok = not hit and not ah and not esc and not obs and have
    return ok, (f"fresh interpreter: after `import tierc11_ride` sys.modules holds {len(mods)} "
                f"modules; names containing {list(FORBIDDEN)}: {hit or 0}; AST scan of "
                f"tierc11_ride.py (function bodies included; imports + .top/.bottom): "
                f"{ah or 0}; E.hook_escapes on tierc11_ride.py's OWN source: {esc or 0}; the "
                f"ride's 1h read seen as an `open` audit event on the TC11 snapshot, none "
                f"outside it: {obs or 'yes'}; tierc11_env and tierc9 loaded: {have}")


# ═══════════════════════════════════════════════════════════════════ F-DET
PROBE_T_COLS = ("symbol", "entry_ms", "exit_ms", "exit_px", "exit_reason", "net_r", "mfe_r",
                "mae_r", "exit_close_ms", "exit_resolved_by", "exit_stamp_ms", "latch_1h_ms",
                "latch_stamp_ms", "n_walk_mismatch", "tp_counts", "acted_by")
PROBE_LEG_KEYS = ("exit_i", "exit_px", "exit_reason", "final_stop", "mfe", "mae",
                  "mae_to_1r_raw", "reached_1r", "harvest", "blocked", "n_opportunities",
                  "latch_1h_ms", "plus1r_1h_ms", "exit_close_ms", "exit_stamp_ms",
                  "state_after_J")


def book_rows(book, extra=()) -> list:
    return [[getattr(t, c, None) for c in PROBE_T_COLS + tuple(extra)] for t in keyed(book)]


def probe_levels(sym: str) -> RD.TPLevels:
    """SYNTHETIC TP levels for the determinism probe only (close[j-1] x (1 +/- 3%)),
    never the reading's range levels."""
    c = T9.frame(sym)["f"].c
    lv_l, lv_s = np.full(len(c), np.nan), np.full(len(c), np.nan)
    lv_l[1:], lv_s[1:] = c[:-1] * 1.03, c[:-1] * 0.97
    return RD.TPLevels(lv_l, lv_s)


def probe_text() -> str:
    L = ["PROBE · TIER-C11 RIDE ENGINE (deterministic; shas and counts only, no aggregate of any "
         "registered book)"]
    L += RD.spec_lines()
    lo, hi = corridor()
    b = base()
    L.append(f"corridor CLASSIC5 {iso(lo)} -> {iso(hi + 1)} · v6 control n {len(b)} · book "
             f"sha {TP._book_sha(b)}")
    b0 = RD.transform_book(b, CARD, ROLES, lo, hi)
    b1 = walk_book_real()
    L.append(f"ride11 hooks off: book sha {TP._book_sha(b0)} · == v6 "
             f"{TP._book_sha(b0) == TP._book_sha(b)}")
    L.append(f"ride11 walk ON:   book sha {TP._book_sha(b1)} · == v6 "
             f"{TP._book_sha(b1) == TP._book_sha(b)} · rows sha {rows_sha(book_rows(b1))}")
    for s in E.CLASSIC5:
        W = RD.walk_of(s)
        f = T9.frame(s)["f"]
        lo_i, hi_i = T7._idx_range(f.open_ms, lo, hi)
        mm = [j for j in sorted(W.why) if lo_i <= j <= hi_i]
        L.append(f"  walk {s}: 4h bars {len(W.ok)} · 1h rows {len(W.h1.open_ms)} · mismatch "
                 f"bars in the corridor {len(mm)}: "
                 + "; ".join(f"{iso(W.open4[j])} ({W.why[j]})" for j in mm))
    res: dict = {}
    for t in b1:
        if t.exit_reason == "stop":
            k = ("parent" if t.exit_resolved_by == "parent"
                 else str((int(t.exit_close_ms) - int(t.exit_ms)) // H1 - 1))
            res[k] = res.get(k, 0) + 1
    L.append(f"walk ON stop exits resolved at child {dict(sorted(res.items()))} · "
             f"latch_on_stop_child {sum(bool(t.latch_on_stop_child) for t in b1)} · campaigns "
             f"crossing a mismatch bar "
             f"{[(t.symbol, iso(t.entry_ms)) for t in b1 if t.n_walk_mismatch]}")
    L.append(f"latch_1h present == v6 reached_1r on every campaign: "
             f"{all((t.latch_1h_ms is not None) == bool(t.reached_1r) for t in b1)}")
    wn = RD.transform_book(b, CARD, ROLES, lo, hi, walk=True,
                           warn_of=lambda s: RD.warn_of(RD.walk_of(s)))
    L.append(f"warn book (walk ON, 1h 12/89 counter cross pre-+1R): n {len(wn)} · rows sha "
             f"{rows_sha(book_rows(wn))}")
    tpb = RD.transform_book(b, CARD, ROLES, lo, hi, walk=True, tp_of=probe_levels)
    L.append(f"TP probe book (walk ON; SYNTHETIC levels, not the reading's): n {len(tpb)} · "
             f"rows sha {rows_sha(book_rows(tpb))}")
    wb = {(t.symbol, int(t.entry_ms)): t for t in b1}

    def probe_adds(k):
        t = wb[k]
        if t.latch_1h_ms is None:
            return None
        return [(int(t.latch_1h_ms) + q * H1, None) for q in range(3)
                if int(t.latch_1h_ms) + q * H1 < int(t.exit_close_ms)]
    ab = RD.transform_book(b, CARD, ROLES, lo, hi, walk=True, adds_of=probe_adds)
    L.append(f"add probe book (walk ON; events at the latch +0/1/2h, tape prices): n {len(ab)} "
             f"· rows sha {rows_sha(book_rows(ab, ('add_r', 'adds', 'add_dispositions')))}")
    legs = []
    for s, d, J, ke in relay_population():
        te = int(own4(s)["om"][J]) + (ke + 1) * H1
        re_ = RD.relay_entry(s, te)
        stp, _ = RD.relay_stop(s, re_["asof_i"], re_["entry_px"], d, CARD)
        if stp is None:
            legs.append([s, d, J, ke, None])
            continue
        leg = RD.relay11(s, CARD, ROLES, d, re_["entry_close_ms"], re_["entry_px"], stp.stop_px,
                         stp.r_dist, own4(s)["hi_i"], moved=re_["moved"], walk_after=True)
        legs.append([s, d, J, ke, [leg.get(k) for k in PROBE_LEG_KEYS]])
    L.append(f"relay probe (every v6 campaign x J in ti..ti+2 x child 0-2, walk_after): n "
             f"{len(legs)} · legs sha {rows_sha(legs)}")
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
        d = RUN_ROOT / "_det_ride" / (f"seed_{s}" if flag == "--emit-to" else f"hashorder_{s}")
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
    key = [ln for ln in this.decode("utf-8").splitlines() if ln.startswith(("ride11 walk ON",
                                                                            "corridor"))]
    n_lines = len(this.decode("utf-8").splitlines())
    return (not bad), (f"exit {o[1][0]}/{o[SEED][0]}; {len(this)} bytes, {n_lines} lines (hooks "
                       f"off, walk, warn, TP, add and relay probes); sha "
                       f"{sha_bytes(o[1][1])[:16]}… == {sha_bytes(o[SEED][1])[:16]}… == this "
                       f"run {sha_bytes(this)[:16]}…: {not bad}"
                       + ("" if not bad else f"; findings {bad}")
                       + f"; the probe's key lines: {key}")


# ═══════════════════════════════════════════════════════════════ THE TABLE
FIXTURES = (
    ("F-WALK-IDENT", "every hook off, the 1h walk ON: v6 exactly; the mismatch law and the "
     "per-child order proven on planted bars",
     "any of the five plants (a walk ignoring the mismatch law, on either planted mismatch "
     "bar; LATCH before STOP; a bent unacted net_r; the walk-type guard removed) is not "
     "caught by its named detector",
     "the walk-ON CLASSIC5 book differs from the v6 control on any of the 12 CTRL_COLS (raw "
     "floats) or an exit reason or the count, TP.ctrl_diff fails, the identity helper finds "
     "anything; the planted mismatch bar is not decided by the parent (v6's exit, counted, "
     "resolved 'parent', stamped at the bar's open); the planted children-below bar stops "
     "the campaign or is not counted; the planted same-child bar latches or exits elsewhere "
     "than that child; the planted latch-first bar does not latch on the earlier child; a "
     "Walk object passed as transform_book(walk=) does not HALT",
     walk_break, walk_real),
    ("F-RELAY-RIDE", "L-T.2 at cardinality: the relay's entry, stop, bar-J walk, carried "
     "state and continuation",
     "any of the nine plants (a carry dropping reached_1r; mutants M1 as-of J, M2 harvest "
     "armed on close[J], M3 whole-bar harvest touch, M4 parent-high trail arming, M8 "
     "mae_to_1r past the latch, M11 continuation from J+2, M12 injected stop ignored, M13 no "
     "trail at J) is not caught by its named detector",
     "any of the 200 4h-close re-entries differs from _ride_leg9 or the v6 Trade; on any "
     "relay of the population (every v6 campaign x J in {ti, ti+1, ti+2} x child 0-2) "
     "relay_entry is not (J, '1h', the 1h close, as-of J-1, not refused; refused against a "
     "trigger at the prior 4h close, kept against J's close), relay_stop is not "
     "struct_stop_4h as of J-1, or relay11's exit (stop inside J / bell at J / corridor end) "
     "or state after J differs from this file's hand walk; any carried relay whose state "
     "after J equals v6's one-bar state does not continue exactly as _ride_leg9; any "
     "latched relay's trail at J differs from v6's matched_step; any split point's injected "
     "continuation differs from the untruncated _ride_leg9; a claimed path class is empty",
     relay_break, relay_real),
    ("F-EXIT1H", "a stop exit resolves at the first 1h child touching the stop in force; "
     "the L-R.5 stamps",
     "either plant (resolving every stop at the 4h close; mutant M17 stamping a parent-"
     "decided stop at its close) is not caught by its named detector",
     "any real stop exit (walk ON) resolves (or is stamped) anywhere but the close of the "
     "first child of its exit bar whose low (high) touches the stop, hand-walked on this "
     "file's own read — or, on a bar this file finds mismatched, anywhere but the parent's "
     "close (stamped at its open); any bell exit resolves or is stamped anywhere but its 4h "
     "close; any latch stamp is not its 1h child's close (the bar's open when parent-"
     "decided); fewer than 3 examples with the touch before the last child are printed; "
     "any v6 stop bar planted as a mismatch bar is not v6's exit, resolved 'parent' at the "
     "4h close, stamped at the bar's open and counted",
     exit1h_break, exit1h_real),
    ("F-MISMATCH-1H", "L-W.0: 1h-only events (relay entry, add, warn) on a mismatch bar are "
     "taken at the parent's close",
     "any of the four mutants (M5 relay entry not moved, M6 add not moved, M7 warn ignoring "
     "the parent's latch, M15 the moved= guard removed) is not caught by its named detector",
     "a relay entry inside any real corridor mismatch bar is not moved to the parent's close "
     "at its close price and as-of J, is not refused on the trigger close, or rides "
     "otherwise than _ride_leg9 from J with the bar counted; relay11(moved=True) at a "
     "walkable bar's close does not HALT; an add at a planted mismatch "
     "bar after the latch is not admitted at the parent's close and price, moves the v6 "
     "leg, is not counted, or is booked off the hand calculation; a counter cross on a "
     "planted-mismatch latch bar warns or moves anything but the latch stamp, or one on the "
     "bar before does not warn at the parent's close; a leg is vacuous",
     mismatch_break, mismatch_real),
    ("F-WARN-BOOK", "the whole warn book (L-W.2 12/89 pair, L-W.5 rule) == this file's hand "
     "walk",
     "either mutant (the default pair 12/26; a walked warn that ignores the +1R latch) is "
     "not caught by its named detector",
     "warn_of's cross arrays differ from this file's plain-loop EMA 12/89 crosses on any "
     "asset; any campaign of the CLASSIC5 warn book differs from the hand walk on exit "
     "reason, price, instant, bar or stamp; any warn exit's mfe_r / mae_r differ from the "
     "held law or it keeps reached_1r; the identity helper finds anything; no warn exit",
     warn_break, warn_real),
    ("F-ORDER", "same-bar order STOP -> TP -> (close) BELL; the TP guard, twins, gap fill, "
     "remainder, re-arming and exit instant; per 1h child STOP -> LATCH -> WARN",
     "any of the seven plants (TP-before-STOP, BELL-before-TP, WARN-before-LATCH orders; "
     "mutants M9 TP instant at the 4h close, M10 post-harvest twin live before the harvest, "
     "M14 near side read on close[j], M16 a mismatch-bar TP stamped at the close) is not "
     "caught by its named detector",
     "on any eligible v6 stop bar with a live, touched TP planted the exit is not v6's stop; "
     "on any eligible bell bar the TP does not fill first at max(level, open) (min short), or "
     "a guard / far-side / post-harvest case does not withhold (and count), or the unguarded "
     "twin does not fill; any gap bar's TP fills anywhere but the open; a TP after the "
     "harvest does not book the 0.5 remainder (or before it the whole 1.0) to the hand "
     "calculation with mfe capped at the fill, or the post-harvest twin does not withhold "
     "before the harvest; any eligible bar pair does not withhold at X and re-arm at X+1; "
     "any bell bar's TP exit instant under the walk is not the first child reaching the "
     "level, or, the bar planted as a mismatch bar, not the same fill at the parent's close "
     "stamped at the bar's open; any of the four planted warn cases "
     "differs from its hand walk",
     order_break, order_real),
    ("F-ADD-ACCT", "adds booked through tierc7._account_chain equal a hand calculation, the "
     "D12 ceiling once on the total; the price is the tape's",
     "either plant (a 3rd add admitted; mutant A1 taking the caller's price unchecked) is "
     "not caught by its named detector",
     "the planted campaign admits anything but the two intended adds (0.5 each, in the 4h "
     "bar containing the 1h close), any event's disposition differs from the hand walk, "
     "net_r / gross_r / fee_r / funding_r / funding_r_uncapped / add_r differ from the hand "
     "calculation, the ceiling does not bind or is not flagged, the paired delta is not "
     "add_r + the cap-absorbed funding, the flags differ, or the whole add book breaks the "
     "identity law; PLANT B's booking, flags or twins differ from the hand walk; adds with "
     "no caller price are not at the tape's 1h closes, or a bent caller price does not HALT",
     add_break, add_real),
    ("F-CLOSURE-RIDE", "tierc11_ride is a range-free decision module whose data I/O the "
     "audit hook sees",
     "any of the five plants (a top-level rangefinder import in a fresh interpreter; lazy "
     "tierc10_census / tierc11_nest imports; a .top read; an observer installed after the "
     "reads) is not caught by its named detector",
     "a fresh interpreter importing tierc11_ride holds a module named with rangefinder / "
     "tierc10_census / tierc10_stamps / tierc10_null / tierc11_nest; tierc11_ride.py's own "
     "source imports one anywhere, reads .top/.bottom, or uses an I/O primitive the audit "
     "hook cannot see (E.hook_escapes — the lineage's sources are not scanned); or the "
     "ride's 1h read is not observed as an `open` audit event on the TC11 snapshot, or any "
     "open lands outside it",
     closure_break, closure_real),
    ("F-DET", "two subprocess emissions under different hash seeds, one set of bytes",
     "a one-byte-bent copy or a hash-order-dependent emission is not found",
     "the PYTHONHASHSEED 1 and 20260924 emissions of RIDE_PROBE.txt (hooks off, walk, warn, "
     "TP, add and relay outputs) differ from each other or from this run's bytes, or either "
     "exits nonzero",
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
    say("TIER-C11 TC11-RIDE FIXTURES — scripts/tierc11_ride.py (the ride engine: L-W.0, "
        "L-W.3, L-W.5, L-A.1, L-H.1, L-T.2, L-1.5) — break leg first, RED or void")
    say("=" * 78)
    say(f"seed {SEED} · substrate {SNAP.name} · pin {PIN} · module sha256 "
        f"{sha_bytes(RIDE_SRC.read_bytes())}")
    for ln in RD.spec_lines():
        say(ln)
    say(f"  mutants (shadow copies, one mis-build each): {len(MUTANTS)} — "
        + "; ".join(f"{k} {v[0]}" for k, v in MUTANTS.items()))
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
