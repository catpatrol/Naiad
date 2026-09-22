#!/usr/bin/env python
"""TIER-C10 · STAGE 0c — F-NULL-COV · F-NULL-BOX · F-NULL-ASOF · F-NULL-SANE ·
F-NULL-GRID · F-NULL-DET.  The fixtures of the CENSUS-R null model.
TWO LEGS PER FIXTURE, the BREAK leg first and it must go RED, or the fixture
proves nothing [the prove() law, carried from the RF suites through
scripts/tierc10_rf_fixtures.py, whose harness this file imports].  Every plant
is made on a COPY — an array, a frame, a throwaway directory, a module global
restored in a finally; no real artifact is touched.

WHAT IS ON TRIAL.  scripts/tierc10_null.py redraws the real ranges' boxes at
random and sends their events down the census's own road.  Six ways it could
lie, one fixture each:
  F-NULL-COV   THE ALIVE-BAR IDENTITY: every draw's schedule holds EXACTLY the
               real alive-bar count — rebuilt HERE from the filed boxes and
               from the census's as-of layer, a second road to the same number
               — every box carrying the life AND the ATR height of ONE real
               range (its src_rid; the pairs a permutation, each whole), the
               gaps a permutation of the real gaps, no window overlapping
               another or leaving the tape.  Real vs achieved close-inside-span coverage
               is PRINTED per draw; no tolerance stands in for the identity.
  F-NULL-BOX   THE FROZEN PINS BIND THE STATIC BOX: breach / harden / DIE and
               the one-sided memory touch of every filed box re-walked on the
               RAW parquet with an ATR and literals written here; every filed
               flip-hold holds on the raw bars at touch + HOLD (a failed hold
               must FAIL); the ledger's term / MFE / MAE / toll re-walked bar
               by bar; the per-draw grid re-derived from the filed ledger.
  F-NULL-ASOF  THE NULL IS AS-OF CLEAN: on seeded random cuts AND cuts aimed at
               the structure, the null's events and per-bar arrays on tape[:t]
               equal the full run's restricted to <= t - 1.  SABOTAGE: a DIE
               read one bar early, a flip at its stamp bar, a box centred on
               its window's LAST close — each RED.
  F-NULL-SANE  ON A PURE RANDOM WALK the real machine's outcome medians and
               the null's AGREE within bootstrap noise, and each side's own
               mean term holds zero (a leaked null must FAIL it); ON A PLANTED
               EDGE — a drift after every REAL DIE, planted causally — real
               MUST BEAT null (the plant removed must FAIL it).
  F-NULL-GRID  every table whole: declared vs filed, the REAL rows equal to the
               census's own filed grid, the summary re-derived from the filed
               grid, collared, stamped, no verdict column.
  F-NULL-DET   same seed -> the same bytes, across processes and hash seeds; a
               different draw index or seed -> different boxes; resume honest.

BANNED HERE, as in every tier suite: self-comparison; one example where
cardinality was possible; a tuned magnitude bound standing in for an identity;
a check whose claim is not the design's claim.

FROZEN SUBSTRATE [TIER-C10 law 3]: HALTs unless NAIAD_CACHE_DIR is the TC10
snapshot.  Seed 20260921.  TIER-E: nothing here scores, registers or gates.
The transcript filed beside the null carries no wall clock.

Run: NAIAD_CACHE_DIR=~/.cache/naiad/snapshots/tc10_20260921 \\
     ~/venvs/naiad/bin/python scripts/tierc10_null_fixtures.py [--null-root=DIR] [leg ...]
     (any other argument is matched as a substring of the leg id, case-blind;
     --null-root defaults to the filed null, else the smoke root)
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import asdict
from pathlib import Path

sys.dont_write_bytecode = True

import numpy as np                                                   # noqa: E402
import pandas as pd                                                  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import tierc10_census as C                                           # noqa: E402
import tierc10_null as N                                             # noqa: E402
import tierc10_rf_fixtures as RFX                                    # noqa: E402
import tierc10_census_fixtures as CF                                 # noqa: E402
from analytics import rangefinder_census as RC                       # noqa: E402
from engine import indicators as ind                                 # noqa: E402

SEED = 20260921
PY = str(Path.home() / "venvs" / "naiad" / "bin" / "python")
say, clock, prove, plants = RFX.say, RFX.clock, RFX.prove, RFX.plants
same, rel = CF.same, CF.rel

# THE NULL'S LITERALS, typed HERE — a second object beside the module's own
# and beside the port's pins, so "the frozen pins bind" is never one dict
# counted twice.
DECL_DEV_RETURN_BARS = 7
DECL_BREAK_CONFIRM_N = 8
DECL_BREAK_MARGIN = 1.5
DECL_HOLD_BARS = 6
DECL_HOLD_MARGIN = 1.0
DECL_TTL_BARS = 400
DECL_ATR_LEN = 14
DECL_REAL_DRAW = -1
DECL_STATS = ("median_term", "net", "hit_rate", "hit_rate_net", "median_mfe", "median_mae")
DECL_ROOT_TABLES = ("null_grid", "null_coverage", "null_summary", "leans")
DECL_CELL_TABLES = ("null_grid", "null_events", "null_boxes", "null_coverage",
                    "null_summary")
VERDICT_COLUMNS = CF.VERDICT_COLUMNS + ("p", "p_value", "pvalue", "significant", "reject")


def null_root() -> Path:
    for a in sys.argv[1:]:
        if a.startswith("--null-root="):
            return Path(a.split("=", 1)[1]).expanduser().resolve()
    return N.OUT if (N.OUT / "build_manifest.json").exists() else N.OUT / "smoke"


NROOT = null_root()


def manifest() -> dict:
    p = NROOT / "build_manifest.json"
    if not p.exists():
        raise SystemExit(f"HALT: no null build under {NROOT} — run scripts/tierc10_null.py "
                         "first (the smoke: --assets BTCUSDT --lenses 4h --draws 5 --out "
                         "research_outputs/tierc10/null/smoke)")
    return json.loads(p.read_text())


def cells(man: dict) -> list:
    return [(a, l) for a in man["commission"]["assets"] for l in man["commission"]["lenses"]]


def plant_cells(man: dict) -> list:
    """ONE cell carries the plants that RE-RUN draws (a corrupted pin is judged
    on a fresh ledger): the first that is not 5m, where a re-run costs minutes."""
    cs = cells(man)
    return [next((c for c in cs if c[1] != "5m"), cs[0])]


def receipt(sym: str, lens: str) -> dict:
    return json.loads((C.cell_dir(NROOT, sym, lens) / "cell.json").read_text())


def cell_table(sym: str, lens: str, name: str) -> pd.DataFrame:
    return pd.read_parquet(C.cell_dir(NROOT, sym, lens) / f"{name}.parquet")


_REAL: dict = {}


def real_of(sym: str, lens: str, scale: float) -> dict:
    """The REAL side of one (tape, SCALE), memoised: the census's run, and the
    lives / gaps / heights derived HERE by a road the null module does not
    take — lives and gaps from the run-lengths of the census AS-OF layer's
    per-bar rid array, heights from Range.top0 / bottom0 over an ATR written
    in the fixture suite (own_atr) on the fixture's own read of the parquet."""
    key = (sym, lens, float(scale))
    if key in _REAL:
        return _REAL[key]
    tape = CF.tape_of(sym, lens)
    raw = CF.raw_tape(sym, lens)
    atr = CF.own_atr(raw["h"], raw["l"], raw["c"], DECL_ATR_LEN)
    v2 = C.run_scale(tape, scale)
    view = C.asof_view(tape, v2["macro"], v2["leash"])
    rid = view["rid"]
    n = len(rid)
    edges = np.flatnonzero(np.diff(rid) != 0) + 1
    life_of, start_of, gaps, prev_end = {}, {}, [], 0
    for s, e in zip(np.r_[0, edges].tolist(), np.r_[edges, n].tolist()):
        if rid[s] >= 0:
            gaps.append(s - prev_end)
            life_of[int(rid[s])], start_of[int(rid[s])] = e - s, s
            prev_end = e
    gaps.append(n - prev_end)
    height_of = {int(r.rid): float((r.top0 - r.bottom0) / atr[r.confirm_i])
                 for r in v2["macro"]["ranges"] if r.confirm_i >= 0}
    _REAL[key] = {"tape": tape, "raw": raw, "atr": atr, "macro": v2["macro"], "n": n,
                  "life_of": life_of, "start_of": start_of, "gaps": gaps,
                  "height_of": height_of,
                  "alive": int(view["in_range"].sum()),
                  "coverage_pct": 100.0 * float(np.asarray(v2["macro"]["covered"]).sum()) / n}
    return _REAL[key]


# ═════════════════════════════════════════════════════════ F-NULL-COV
COV_TAPES = (("BTCUSDT", "4h"), ("BTCUSDT", "1d"), ("ETHUSDT", "4h"), ("SOLUSDT", "1d"))
COV_SCALES = (3.0, 2.0)          # the frozen pin, and one more
COV_DRAWS = 12


def _box_findings(bx: pd.DataFrame, own: dict, label: str) -> list[str]:
    """ONE draw's boxes against the real set derived HERE.  The alive-bar count
    is rebuilt as a MASK (an overlap or a window off the tape loses bars in a
    mask; a sum of lives would not notice)."""
    b = bx.sort_values("box", kind="mergesort")
    a = b["confirm_i"].to_numpy(np.int64)
    L = b["life"].to_numpy(np.int64)
    n = own["n"]
    if len(a) != len(own["life_of"]):
        return [f"{label}: {len(a)} boxes for {len(own['life_of'])} real ranges"]
    bad = []
    mask = np.zeros(n, dtype=bool)
    for s, e in zip(a.tolist(), (a + L).tolist()):
        mask[max(s, 0):e] = True
    if int(mask.sum()) != own["alive"]:
        bad.append(f"alive-bar count {int(mask.sum()):,} != the real {own['alive']:,}")
    src = b["src_rid"].astype(int).tolist()
    if sorted(src) != sorted(own["life_of"]):
        bad.append("the boxes' source ranges are not a permutation of the real ranges")
    else:
        if L.tolist() != [own["life_of"][r] for r in src]:
            bad.append("a life is not its source range's")
        if not all(same(x, own["height_of"][r]) for x, r in zip(b["height_atr"].tolist(), src)):
            bad.append("a height (ATR) is not its source range's — a (life, height) pair is "
                       "broken")
    if len(a):
        if (a[1:] < (a + L)[:-1]).any():
            bad.append("two scheduled windows overlap")
        if a[0] < 0 or a[-1] + L[-1] > n:
            bad.append("a window leaves the tape")
        if a[0] < DECL_ATR_LEN:
            bad.append(f"a box is born inside the ATR warm floor ({a[0]} < {DECL_ATR_LEN})")
        got = np.r_[a[0], a[1:] - (a + L)[:-1], n - (a[-1] + L[-1])].tolist()
        if sorted(got) != sorted(own["gaps"]):
            bad.append("the gaps are not a permutation of the real gaps")
    return [f"{label}: {x}" for x in bad]


def _own_coverage(bx: pd.DataFrame, raw: dict, atr: np.ndarray) -> tuple[int, int, int]:
    """(scheduled alive bars, closes inside the box over the schedule, over the
    event-alive bars) — from the FILED box fields and the raw parquet only."""
    n = len(raw["c"])
    sched = np.zeros(n, dtype=bool)
    in_s, in_e = np.zeros(n, dtype=bool), np.zeros(n, dtype=bool)
    for r in bx.itertuples():
        a = int(r.confirm_i)
        height = r.height_atr * atr[a]
        bot = raw["c"][a] - r.u * height
        top = bot + height
        e = min(a + int(r.life), n)
        stop = min(max(int(r.die_i), a), e) if r.die_i >= 0 else e   # clamped: a planted
        inside = (raw["c"][a:e] >= bot) & (raw["c"][a:e] <= top)     # box may be anywhere
        sched[a:e] = True
        in_s[a:e] = inside
        in_e[a:stop] = inside[:stop - a]
    return int(sched.sum()), int(in_s.sum()), int(in_e.sum())


def _filed_cov_findings(boxes: dict | None = None, cov: dict | None = None) -> tuple[list, dict]:
    """The FILED root.  `boxes` / `cov` = {(sym, lens): frame} COPIES standing in
    for the filed tables (the break leg's plants)."""
    man = manifest()
    bad, st = [], {"draws": 0, "boxes": 0, "lines": []}
    for sym, lens in cells(man):
        rc = receipt(sym, lens)
        bx_all = (boxes or {}).get((sym, lens), None)
        bx_all = cell_table(sym, lens, "null_boxes") if bx_all is None else bx_all
        cv_all = (cov or {}).get((sym, lens), None)
        cv_all = cell_table(sym, lens, "null_coverage") if cv_all is None else cv_all
        for kind in man["commission"]["scale_kinds"]:
            own = real_of(sym, lens, rc["scales"][kind]["scale_mult"])
            for draw in range(man["n_draws"]):
                tag = f"{sym} {lens} {kind} draw {draw}"
                bx = bx_all[(bx_all["scale_kind"] == kind) & (bx_all["draw"] == draw)]
                cv = cv_all[(cv_all["scale_kind"] == kind) & (cv_all["draw"] == draw)]
                st["draws"] += 1
                st["boxes"] += len(bx)
                bad += _box_findings(bx, own, tag)
                if len(cv) != 1:
                    bad.append(f"{tag}: {len(cv)} coverage row(s)")
                    continue
                r = cv.iloc[0]
                n_s, in_s, in_e = _own_coverage(bx, own["raw"], own["atr"])
                if not (int(r["null_alive_bars_scheduled"]) == n_s == own["alive"]
                        == int(r["real_alive_bars"]) and bool(r["alive_bars_identity"])):
                    bad.append(f"{tag}: filed alive bars {int(r['null_alive_bars_scheduled']):,}"
                               f" / rebuilt from the boxes {n_s:,} / real {own['alive']:,}")
                if not (same(r["null_coverage_pct_scheduled"], 100.0 * in_s / own["n"])
                        and same(r["null_coverage_pct_event"], 100.0 * in_e / own["n"])
                        and same(r["real_coverage_pct"], own["coverage_pct"])):
                    bad.append(f"{tag}: a filed coverage % is not what the boxes and the raw "
                               "closes give")
                st["lines"].append(
                    f"{tag:>34}: alive {n_s:>7,} == real {own['alive']:>7,} · close-inside-span "
                    f"real {own['coverage_pct']:6.2f}% · null over the schedule "
                    f"{100.0 * in_s / own['n']:6.2f}% · over event-alive bars "
                    f"{100.0 * in_e / own['n']:6.2f}%")
    return bad, st


def _first_cell_copies() -> tuple[tuple, pd.DataFrame, pd.DataFrame]:
    sym, lens = cells(manifest())[0]
    return ((sym, lens), cell_table(sym, lens, "null_boxes").copy(),
            cell_table(sym, lens, "null_coverage").copy())


def cov_break():
    key, bx0, cv0 = _first_cell_copies()
    kind = manifest()["commission"]["scale_kinds"][0]
    pick = (bx0["scale_kind"] == kind) & (bx0["draw"] == 0)
    ix = bx0.index[pick].tolist()                      # draw 0's boxes, in box order

    def longer_life():
        b = bx0.copy()
        b.loc[ix[len(ix) // 2], "life"] += 1
        return _filed_cov_findings(boxes={key: b})[0]

    def overlap():
        b = bx0.copy()
        k = len(ix) // 2
        b.loc[ix[k + 1], "confirm_i"] = (b.loc[ix[k], "confirm_i"] + b.loc[ix[k], "life"] - 1)
        return _filed_cov_findings(boxes={key: b})[0]

    def one_bar_between_gaps():
        # alive bars, lives, heights and disjointness ALL survive this one: a
        # box slid one bar along — only the gap multiset can see it
        b = bx0.copy()
        a, L = b.loc[ix, "confirm_i"].to_numpy(), b.loc[ix, "life"].to_numpy()
        gaps = np.r_[a[0], a[1:] - (a + L)[:-1]]
        for k in range(1, len(ix) - 1):
            g_l, g_r = int(gaps[k]), int(a[k + 1] - (a[k] + L[k]))
            if g_r >= 1 and g_l + 1 != g_r:
                b.loc[ix[k], "confirm_i"] += 1
                break
        return _filed_cov_findings(boxes={key: b})[0]

    def pair_broken():
        # alive bars, gaps, windows ALL survive: two boxes trade heights
        b = bx0.copy()
        h = b.loc[ix, "height_atr"].to_numpy()
        k = next(k for k in range(len(ix) - 1) if not same(h[k], h[k + 1]))
        b.loc[ix[k], "height_atr"], b.loc[ix[k + 1], "height_atr"] = h[k + 1], h[k]
        return _filed_cov_findings(boxes={key: b})[0]

    def filed_count_moved():
        c = cv0.copy()
        c.loc[c.index[0], "null_alive_bars_scheduled"] += 1
        return _filed_cov_findings(cov={key: c})[0]
    return plants([
        ("ONE LIFE ONE BAR LONGER in a COPY of the filed boxes", longer_life),
        ("TWO WINDOWS OVERLAPPING by one bar (a sum of lives would not notice)", overlap),
        ("ONE BAR MOVED BETWEEN TWO GAPS (alive bars, lives, heights all intact)",
         one_bar_between_gaps),
        ("TWO BOXES TRADE HEIGHTS (alive bars, gaps, windows all intact — a pair is broken)",
         pair_broken),
        ("THE FILED ALIVE-BAR COUNT moved by one in a COPY of the coverage table",
         filed_count_moved),
    ])


def cov_real():
    bad, st = _filed_cov_findings()
    for x in st["lines"]:
        say(f"        {x}")
    n_mem = swaps = ident = 0
    own_pct = {False: [], True: []}
    for sym, lens in COV_TAPES:
        for scale in COV_SCALES:
            own = real_of(sym, lens, scale)
            real = N.real_box_set(own["tape"], own["macro"])
            for draw in range(COV_DRAWS):
                for keep in (False, True):          # the schedule, and the design of record
                    boxes, info = N.schedule(real, N.draw_rng(SEED, draw, sym, lens,
                                                              f"@{scale:g}"), keep_order=keep)
                    ov = sum(max(0, min(b.confirm_i + b.life, own["start_of"][b.src_rid] + b.life)
                                 - max(b.confirm_i, own["start_of"][b.src_rid])) for b in boxes)
                    own_pct[keep].append(100.0 * ov / max(1, own["alive"]))
                    if ov != info["own_window_overlap_bars"]:
                        bad.append(f"(in memory) {sym} {lens} draw {draw}: own-window overlap "
                                   f"{info['own_window_overlap_bars']} vs {ov} counted here")
                    if keep:
                        continue
                    bx = pd.DataFrame([asdict(b) for b in boxes],
                                      columns=["box", "src_rid", "confirm_i", "life",
                                               "height_atr", "u", "censored"])
                    tag = f"(in memory) {sym} {lens} @{scale:g} draw {draw}"
                    bad += _box_findings(bx, own, tag)
                    nm = N.static_box_machine(own["tape"], boxes)
                    if int(nm["alive_sched"].sum()) != own["alive"]:
                        bad.append(f"{tag}: the machine's scheduled mask is not the real "
                                   "alive-bar count")
                    if not (nm["alive_evt"] <= nm["alive_sched"]).all():
                        bad.append(f"{tag}: event-alive bars outside the schedule")
                    n_mem += 1
                    swaps += int(info["lead_gap_swapped"])
                    ident += int(info["identity_perm"])
    say(f"        OWN-WINDOW OVERLAP (share of the schedule inside each box's OWN real window — "
        f"the place its life was earned; PRINTED, not asserted) over {n_mem} in-memory draws: "
        f"gaps + order permuted {np.mean(own_pct[False]):.2f}% (max {np.max(own_pct[False]):.2f}%)"
        f" · gaps ALONE, the design of record, {np.mean(own_pct[True]):.2f}% "
        f"(max {np.max(own_pct[True]):.2f}%) [N-c]")
    return not bad, (
        f"ALIVE-BAR IDENTITY on all {st['draws']} FILED draws ({st['boxes']:,} boxes, "
        f"{rel(NROOT)}) and on {n_mem} more drawn in memory over {list(COV_TAPES)} x SCALE "
        f"{list(COV_SCALES)}: the schedule's alive-bar MASK holds exactly the real count — the "
        f"census as-of layer's in_range sum, a road the null module does not take; every box "
        f"carries the life AND the ATR height of ONE real range (heights over an ATR written "
        f"here), the sources a permutation of the real ranges; the gaps are a permutation of "
        f"the real gaps; no window overlaps or leaves the tape or starts inside the warm floor "
        f"({swaps} lead-gap swap(s), {ident} identity permutation(s) among the in-memory "
        f"draws). The filed coverage figures re-derive from the filed boxes + raw closes. "
        f"MATCHED COVERAGE IS PRINTED ABOVE, per draw: the identity is the alive-bar count; "
        f"the close-inside-span figures are reported, never toleranced"
        if not bad else f"{len(bad)} finding(s): " + "; ".join(bad[:4]))


# ═════════════════════════════════════════════════════════ F-NULL-BOX
def _own_walk(c, atr, a: int, end: int, bot: float, top: float) -> list[tuple]:
    """The static-box law, written again with the literals typed above:
    [(i, 'breach' | 'harden' | 'lapse' | 'DIE', side)]."""
    out, side, open_i, closes = [], None, 0, 0
    for i in range(a, end):
        x = c[i]
        if side is None:
            if x > top or x < bot:
                side, open_i, closes = ("top" if x > top else "bottom"), i, 1
                out.append((i, "breach", side))
        else:
            if (x > top) if side == "top" else (x < bot):
                closes += 1
            else:
                out.append((i, "harden" if i - open_i <= DECL_DEV_RETURN_BARS else "lapse", side))
                side = None
        if side is not None:
            far = (x - top) if side == "top" else (bot - x)
            if closes >= DECL_BREAK_CONFIRM_N or far >= DECL_BREAK_MARGIN * atr[i]:
                out.append((i, "DIE", side))
                break
    return out


def _holds(raw, atr, px: float, side: str, i: int) -> bool:
    n = len(raw["c"])
    if i + DECL_HOLD_BARS >= n:
        return False
    return not any((raw["c"][k] < px - DECL_HOLD_MARGIN * atr[k]) if side == "top"
                   else (raw["c"][k] > px + DECL_HOLD_MARGIN * atr[k])
                   for k in range(i, i + DECL_HOLD_BARS + 1))


def _box_law_findings(bx: pd.DataFrame, led: pd.DataFrame, raw: dict, atr: np.ndarray,
                      st: dict) -> list[str]:
    """ONE draw: filed boxes + filed ledger against a plain walk of the raw bars."""
    bad = []
    n = len(raw["c"])
    want = {"breach": set(), "harden": set(), "DIE": set(), "memory-touch-v1": set()}
    px, die = {}, {}
    for r in bx.itertuples():
        a = int(r.confirm_i)
        height = r.height_atr * atr[a]
        bot = raw["c"][a] - r.u * height
        top = bot + height
        px[(r.box, "top")], px[(r.box, "bottom")] = top, bot
        walk = _own_walk(raw["c"], atr, a, min(a + int(r.life), n), bot, top)
        for i, kind, side in walk:
            if kind in want:
                want[kind].add((int(r.box), side, i))
        d = [(i, side) for i, kind, side in walk if kind == "DIE"]
        st["boxes"] += 1
        if (d[0] if d else (-1, "")) != (int(r.die_i), r.die_side):
            bad.append(f"box {r.box}: filed DIE ({r.die_i}, {r.die_side!r}) vs walked {d}")
        if d:
            die[int(r.box)] = d[0]
            hit = np.flatnonzero(raw["h"][d[0][0] + 1:] >= top)
            if len(hit):
                want["memory-touch-v1"].add((int(r.box), "top", d[0][0] + 1 + int(hit[0])))
            hit = np.flatnonzero(raw["l"][d[0][0] + 1:] <= bot)
            if len(hit):
                want["memory-touch-v1"].add((int(r.box), "bottom", d[0][0] + 1 + int(hit[0])))
    for cls, w in want.items():
        L = led[led["cls"] == cls]
        got = set(zip(L["rid"].astype(int), L["side"], L["i"].astype(int)))
        st["events"] += len(w)
        if got != w:
            bad.append(f"{cls}: {len(got)} filed vs {len(w)} walked "
                       f"(e.g. {sorted(got ^ w)[:2]})")
        if not (L["known_at"] == L["i"]).all():
            bad.append(f"{cls}: a row is anchored away from its own bar")
        sg = {"breach": 1, "harden": -1, "DIE": 1}.get(cls)
        if sg is not None and not (L["sgn"] == np.where(L["side"] == "top", sg, -sg)).all():
            bad.append(f"{cls}: a sign is not the census's sign law")
    for r in led[led["cls"] == "flip-hold"].itertuples():
        i, p = int(r.i), px[(int(r.rid), r.side)]
        st["flips"] += 1
        came = raw["c"][i - 1] > p if r.side == "top" else not raw["c"][i - 1] > p
        if not (int(r.rid) in die and i > die[int(r.rid)][0]
                and raw["l"][i] <= p <= raw["h"][i] and came
                and _holds(raw, atr, p, r.side, i)
                and int(r.known_at) == i + DECL_HOLD_BARS
                and int(r.sgn) == (1 if r.side == "top" else -1)):
            bad.append(f"flip-hold rid {r.rid} {r.side} at {i}: not an opposite-side two-sided "
                       f"touch of a corpse line that HOLDS, anchored at touch + {DECL_HOLD_BARS}")
    for r in led[led["cls"] == "memory-touch-2s"].itertuples():
        i, p = int(r.i), px[(int(r.rid), r.side)]
        st["touch2s"] += 1
        d_i = die.get(int(r.rid), (n, ""))[0]
        earlier = np.flatnonzero((raw["l"][d_i + 1:i] <= p) & (p <= raw["h"][d_i + 1:i]))
        if not (d_i < i <= d_i + DECL_TTL_BARS and raw["l"][i] <= p <= raw["h"][i]
                and not len(earlier) and int(r.known_at) == i
                and int(r.sgn) == (1 if die[int(r.rid)][1] == "top" else -1)):
            bad.append(f"memory-touch-2s rid {r.rid} {r.side} at {i}: not the FIRST two-sided "
                       "touch of a live corpse line, signed by the death")
    return bad


def _own_grid_findings(led: pd.DataFrame, grid: pd.DataFrame, tag: str) -> list[str]:
    bad = []
    for (kind, draw, cls, era, hn), G in grid.groupby(["scale_kind", "draw", "cls", "era",
                                                       "horizon"]):
        L = led[(led["scale_kind"] == kind) & (led["draw"] == draw) & (led["cls"] == cls)]
        if era != C.ERA_ALL:
            L = L[L["era"] == era]
        S = L[~L["bad_atr"] & ~L[f"cens_{hn}"]]
        g = G.iloc[0]
        if int(g["n_events"]) != len(L) or int(g["n"]) != len(S):
            bad.append(f"{tag} {kind} draw {draw} {cls} {era} {hn}: n {g['n_events']}/{g['n']} vs "
                       f"the ledger's {len(L)}/{len(S)}")
            continue
        if not len(S):
            if not (np.isnan(g["median_term"]) and g["nan_reason"]):
                bad.append(f"{tag} {kind} draw {draw} {cls} {era} {hn}: n = 0 without NaN + a reason")
            continue
        med, toll = float(S[f"term_{hn}"].median()), float(S["toll_atr_evt"].median())
        if not (same(g["median_term"], med, 2) and same(g["toll_atr"], toll, 2)
                and same(g["net"], float(np.round(med, C.ROUND_ND) - np.round(toll, C.ROUND_ND)), 2)
                and same(g["hit_rate"], float((S[f"term_{hn}"] > 0).mean()), 2)
                and same(g["median_mfe"], float(S[f"mfe_{hn}"].median()), 2)):
            bad.append(f"{tag} {kind} draw {draw} {cls} {era} {hn}: a filed statistic is not the "
                       "filed ledger's")
    return bad


def _box_run(pins: dict | None = None, led_edit=None, grid_edit=None,
             only: list | None = None) -> tuple[list, dict]:
    """The FILED root against the raw bars.  `pins` = a corrupted pin set: the
    draws are then RE-RUN in memory under it and ITS ledger is judged in the
    filed one's place.  `led_edit` / `grid_edit` = edits made on COPIES.
    `only` = the cells a plant is judged on (the real leg walks them all)."""
    man = manifest()
    rng = np.random.default_rng(SEED)
    bad = []
    st = {"boxes": 0, "events": 0, "flips": 0, "touch2s": 0, "walked": 0, "cens": 0,
          "grid": 0, "draws": 0}
    for sym, lens in (cells(man) if only is None else only):
        rc = receipt(sym, lens)
        raw = CF.raw_tape(sym, lens)
        atr = CF.own_atr(raw["h"], raw["l"], raw["c"], DECL_ATR_LEN)
        bx_all = cell_table(sym, lens, "null_boxes")
        led_all = cell_table(sym, lens, "null_events")
        grid = cell_table(sym, lens, "null_grid")
        if led_edit is not None:
            led_all = led_edit(led_all.copy(), sym, lens)
        if grid_edit is not None:
            grid = grid_edit(grid.copy())
        for kind in man["commission"]["scale_kinds"]:
            for draw in range(man["n_draws"]):
                bx = bx_all[(bx_all["scale_kind"] == kind) & (bx_all["draw"] == draw)]
                led = led_all[(led_all["scale_kind"] == kind) & (led_all["draw"] == draw)]
                if pins is not None:
                    led = _rerun_ledger(sym, lens, kind, draw, rc, pins)
                st["draws"] += 1
                bad += [f"{sym} {lens} {kind} draw {draw}: {x}"
                        for x in _box_law_findings(bx, led, raw, atr, st)]
        null_led = led_all[led_all["draw"] >= 0].reset_index(drop=True)
        b, c1, c2 = CF._outcome_findings(null_led, raw, atr, rng)
        bad += [f"{sym} {lens}: {x}" for x in b]
        st["walked"], st["cens"] = st["walked"] + c1, st["cens"] + c2
        bad += _own_grid_findings(led_all, grid, f"{sym} {lens}")
        st["grid"] += len(grid)
    return bad, st


def _rerun_ledger(sym, lens, kind, draw, rc, pins) -> pd.DataFrame:
    tape = CF.tape_of(sym, lens)
    s = rc["scales"][kind]["scale_mult"]
    own = real_of(sym, lens, s)
    boxes, _ = N.schedule(N.real_box_set(tape, own["macro"]),
                          N.draw_rng(rc["seed"], draw, sym, lens, kind))
    nm = N.static_box_machine(tape, boxes, pins)
    leash = RC.flips_and_leash(nm, tape.d, tape.atr, RC.PINS_V2, retests=False)
    view = N.null_view(tape, nm, leash)
    return N.events_of(tape, nm, leash, view, rc["toll_bps"], N.memo_bands(tape))


def _failed_through() -> tuple | None:
    """(sym, lens, kind, draw, rid, side, i) of one 'failed through' touch among
    the filed draws' leashes, recomputed in memory."""
    man = manifest()
    for sym, lens in plant_cells(man):
        rc = receipt(sym, lens)
        tape = CF.tape_of(sym, lens)
        for kind in man["commission"]["scale_kinds"]:
            s = rc["scales"][kind]["scale_mult"]
            real = N.real_box_set(tape, real_of(sym, lens, s)["macro"])
            for draw in range(man["n_draws"]):
                d = N.null_draw(tape, real, draw, rc["seed"], kind, s, rc["toll_bps"],
                                N.memo_bands(tape))
                for e in d["leash"]:
                    if e.get("verdict", "").startswith("failed through"):
                        return sym, lens, kind, draw, int(e["rid"]), e["side"], int(e["i"])
    return None


def box_break():
    ft = _failed_through()

    def failed_hold(led, sym, lens):
        if ft is None or (sym, lens) != ft[:2]:
            return led
        row = led[(led["scale_kind"] == ft[2]) & (led["draw"] == ft[3])].iloc[0].copy()
        row["cls"], row["rid"], row["side"], row["i"] = "flip-hold", ft[4], ft[5], ft[6]
        row["known_at"], row["sgn"] = ft[6] + DECL_HOLD_BARS, (1 if ft[5] == "top" else -1)
        return pd.concat([led, row.to_frame().T], ignore_index=True).infer_objects()

    def flip_at_stamp(led, sym, lens):
        m = led["cls"] == "flip-hold"
        led.loc[m, "known_at"] = led.loc[m, "i"]
        return led

    def touch_moved(led, sym, lens):
        ix = led.index[(led["cls"] == "memory-touch-v1") & (led["draw"] >= 0)][0]
        led.loc[ix, "i"] += 1
        led.loc[ix, "known_at"] += 1
        return led

    def median_moved(g):
        ix = g.index[(g["draw"] >= 0) & (g["n"] > 0)][0]
        g.loc[ix, "median_term"] += 1e-6
        return g
    only = plant_cells(manifest())

    def run(guard: str, **kw):
        """A plant counts only if the guard it was aimed at is the one that fires."""
        return [x for x in _box_run(only=only, **kw)[0] if guard in x]
    return plants([
        ("DEV_RETURN_BARS = 3 (late returns harden under the frozen 7, lapse under 3)",
         lambda: run("harden:", pins=dict(RC.PINS, DEV_RETURN_BARS=3))),
        ("BREAK_CONFIRM_N = 5 (a box dies three closes early)",
         lambda: run("DIE", pins=dict(RC.PINS, BREAK_CONFIRM_N=5))),
        ("BREAK_MARGIN = 1.0 ATR (a box dies on a smaller excursion)",
         lambda: run("DIE", pins=dict(RC.PINS, BREAK_MARGIN=1.0))),
        ("A FAILED HOLD filed as a flip-hold in a COPY of the ledger — a failed hold must FAIL",
         lambda: run("flip-hold", led_edit=failed_hold) if ft is not None else []),
        ("EVERY flip-hold anchored at its STAMP bar in a COPY",
         lambda: run("flip-hold", led_edit=flip_at_stamp)),
        ("ONE v1 memory touch moved one bar in a COPY",
         lambda: run("memory-touch-v1", led_edit=touch_moved)),
        ("ONE null median moved by 1e-6 in a COPY of the grid",
         lambda: run("filed statistic", grid_edit=median_moved)),
    ])


def box_real():
    bad, st = _box_run()
    return not bad, (
        f"all {st['boxes']:,} FILED boxes of {st['draws']} draws re-walked on the RAW parquet "
        f"with an ATR written here and the pins typed here ({DECL_DEV_RETURN_BARS} / "
        f"{DECL_BREAK_CONFIRM_N} / {DECL_BREAK_MARGIN}): the breach, harden, DIE and one-sided "
        f"memory-touch rows of the filed ledger are EXACTLY the walked sets ({st['events']:,} "
        f"events), each anchored at its own bar under the census's sign law, every box's filed "
        f"DIE the walked one; all {st['flips']} filed flip-holds are opposite-side two-sided "
        f"touches of a corpse line that HOLD on the raw bars at touch..touch + "
        f"{DECL_HOLD_BARS}, anchored at touch + {DECL_HOLD_BARS}; all {st['touch2s']} "
        f"memory-touch-2s rows are FIRST two-sided touches inside the TTL; {st['walked']} "
        f"event-horizons of the null ledger re-walked bar by bar (term, MFE, MAE, toll, the "
        f"known_at close stamp; {st['cens']} CENSORED, none shortened) by the CENSUS suite's own "
        f"walker; {st['grid']} filed grid rows re-derive from the filed ledger"
        if not bad else f"{len(bad)} finding(s): " + "; ".join(bad[:4]))


# ═════════════════════════════════════════════════════════ F-NULL-ASOF
ASOF_TAPES = (("BTCUSDT", "4h"), ("BTCUSDT", "1d"), ("ETHUSDT", "4h"))
ASOF_DRAWS = (0, 1)
ASOF_RANDOM_CUTS = 10
ASOF_STRUCT_EACH = 4
ASOF_EVENT_COLS = ["cls", "i", "known_at", "rid", "side", "sgn"]
ASOF_ARRAYS = ("in_range", "state", "top", "bot", "pct", "dist_atr", "flip_pol")
NULL_LAWS = ("honest", "die-one-bar-early", "flip-at-stamp", "box-reads-its-window-end")
_CUR: dict = {}


def _leaky_bounds(b, c_a, atr_a):
    """THE PLANT: a box centred on the LAST close of its own window."""
    cc = _CUR["c"]
    height = b.height_atr * atr_a
    bot = cc[min(b.confirm_i + b.life - 1, len(cc) - 1)] - b.u * height
    return bot, bot + height


def _null_run(tape, boxes, law: str):
    """The null on one tape under ONE reader — the SAME reader for the full
    tape and for every prefix, so a plant goes RED only through what the
    fixture tests (the prefix is not stable under the leak)."""
    keep = N.box_bounds
    try:
        if law == "box-reads-its-window-end":
            _CUR["c"] = tape.c
            N.box_bounds = _leaky_bounds
        nm = N.static_box_machine(tape, boxes)
    finally:
        N.box_bounds = keep
    leash = RC.flips_and_leash(nm, tape.d, tape.atr, RC.PINS_V2, retests=False)
    view = N.null_view(tape, nm, leash)
    evf, _ = C.census_events(tape, nm, leash, view)
    if law == "die-one-bar-early":
        evf.loc[evf["cls"] == "DIE", "known_at"] -= 1
    if law == "flip-at-stamp":
        m = evf["cls"] == "flip-hold"
        evf.loc[m, "known_at"] = evf.loc[m, "i"]
    view = dict(view, alive_sched=nm["alive_sched"])
    return view, evf


def _null_cuts(tape, boxes, evf, rng) -> list[int]:
    n = tape.n
    cuts = set(rng.integers(200, n + 1, size=ASOF_RANDOM_CUTS).tolist())

    def pick(xs):
        xs = sorted(set(int(x) for x in xs if 200 <= x <= n))
        return [xs[k] for k in sorted(rng.choice(len(xs), size=min(ASOF_STRUCT_EACH, len(xs)),
                                                 replace=False).tolist())] if xs else []
    die = evf[evf["cls"] == "DIE"]["i"].tolist()
    held = evf[evf["cls"].isin(("flip-hold",) + CF.DECL_RETEST)]["i"].tolist()
    cuts |= set(pick(die)) | set(pick([x + 1 for x in die]))       # the DIE bar unseen / seen
    cuts |= set(pick([b.confirm_i for b in boxes]))
    cuts |= set(pick([b.confirm_i + max(1, b.life // 2) for b in boxes]))   # mid-window
    cuts |= set(pick([i + 1 + int(rng.integers(0, DECL_HOLD_BARS)) for i in held]))
    return sorted(cuts)


_ASOF: dict = {}


def asof_corpus() -> dict:
    if _ASOF:
        return _ASOF
    rng = np.random.default_rng(SEED)
    bad = {law: [] for law in NULL_LAWS}
    st = {"cuts": 0, "arrays": 0, "events": 0, "late": 0, "tags": []}
    for sym, lens in ASOF_TAPES:
        own = real_of(sym, lens, 3.0)
        tape = own["tape"]
        real = N.real_box_set(tape, own["macro"])
        for draw in ASOF_DRAWS:
            boxes, _ = N.schedule(real, N.draw_rng(SEED, draw, sym, lens, "frozen3.0"))
            tag = f"{sym} {lens} draw {draw}"
            full = {law: _null_run(tape, boxes, law) for law in NULL_LAWS}
            cuts = _null_cuts(tape, boxes, full["honest"][1], rng)
            st["late"] += int((full["honest"][1]["known_at"] != full["honest"][1]["i"]).sum())
            st["tags"].append(f"{tag} ({len(cuts)} cuts)")
            for t in cuts:
                pre_tape = tape.head(t)
                for law in NULL_LAWS:
                    fv, fe = full[law]
                    pv, pe = _null_run(pre_tape, boxes, law)
                    for k in ASOF_ARRAYS + ("alive_sched",):
                        if not np.array_equal(np.asarray(fv[k])[:t], np.asarray(pv[k]),
                                              equal_nan=True):
                            bad[law].append(f"{tag} t={t}: array {k}")
                    a = (fe[fe["known_at"] <= t - 1][ASOF_EVENT_COLS]
                         .sort_values(ASOF_EVENT_COLS).reset_index(drop=True))
                    b = (pe[pe["known_at"] <= t - 1][ASOF_EVENT_COLS]
                         .sort_values(ASOF_EVENT_COLS).reset_index(drop=True))
                    if not a.equals(b):
                        bad[law].append(f"{tag} t={t}: {len(a)} events known by t - 1 in the "
                                        f"full run, {len(b)} on the prefix")
                    if len(pe) and int(pe["known_at"].max()) > t - 1:
                        bad[law].append(f"{tag} t={t}: the prefix files an event known after "
                                        "its own last bar")
                    if law == "honest":
                        st["cuts"] += 1
                        st["arrays"] += len(ASOF_ARRAYS) + 1
                        st["events"] += len(a)
    _ASOF.update({"bad": bad, "st": st})
    return _ASOF


def asof_break():
    R = asof_corpus()
    return plants([(f"THE READER '{law}'", (lambda law=law: R["bad"][law]))
                   for law in NULL_LAWS if law != "honest"])


def asof_real():
    R = asof_corpus()
    bad, st = R["bad"]["honest"], R["st"]
    return not bad, (
        f"PREFIX-STABILITY of the null on {st['cuts']} cuts ({'; '.join(st['tags'])}): seeded "
        f"random cuts and cuts aimed at the structure — a null DIE bar (unseen, then seen), a "
        f"confirm bar, the middle of a scheduled window, inside the hold window of a flip-hold "
        f"or a retest-hold. With the SAME boxes, the null's events on tape[:t] equal the full "
        f"run's with known_at <= t - 1 ({st['events']:,} event rows compared; {st['late']} of "
        f"the full runs' events are known LATER than they are stamped) and all "
        f"{len(ASOF_ARRAYS) + 1} per-bar arrays agree on [0, t) ({st['arrays']:,} array "
        f"comparisons). A box is (schedule, u, c and ATR at its confirm bar); an event reads "
        f"its own bar" if not bad else f"{len(bad)} finding(s): " + "; ".join(bad[:4]))


# ═════════════════════════════════════════════════════════ F-NULL-SANE
SANE_TAPES = 100                # independent synthetic tapes — the bootstrap's clusters
SANE_BARS = 5000
SANE_SUB = 4                    # sub-steps per bar: the walk that makes a bar's wicks
SANE_P0 = 2000.0                # ARITHMETIC walk, unit sub-step, no drift
SANE_DRAWS = 5
SANE_BOOT = 20000
SANE_ALPHA = 0.01               # family-wise; Bonferroni over the scored cells
PLANT_TAPES = 8
PLANT_MU_ATR = 0.25             # drift per bar, in ATR of the DIE bar
PLANT_BARS = 20                 # == H20
PLANT_CELL = ("DIE", "H20")
T0_MS = 1_500_000_000_000 - 1_500_000_000_000 % C.LENS_MS["4h"]
SANE_CELLS = [(c, h) for c in CF.DECL_CLASSES for h in CF.DECL_HORIZONS]
# three families on the random walk, ONE Bonferroni over all of them
SANE_FAMILIES = (
    ("real - null, median term", lambda t: t["real"] - t["null"]),
    ("the REAL machine's own mean term", lambda t: t["real_mean"]),
    ("the NULL's own mean term", lambda t: t["null_mean"]),
)


def _inc(stream: int, r: int) -> np.ndarray:
    return np.random.default_rng([SEED, stream, r]).standard_normal((SANE_BARS, SANE_SUB))


def _tape(inc: np.ndarray, name: str) -> C.Tape:
    x = SANE_P0 + np.cumsum(inc.ravel()).reshape(inc.shape)
    c = x[:, -1].copy()
    o = np.r_[SANE_P0, c[:-1]]
    h, l = np.maximum(o, x.max(axis=1)), np.minimum(o, x.min(axis=1))
    if not l.min() > 0:
        raise ValueError("synthetic tape went non-positive")
    t0 = T0_MS + np.arange(len(c), dtype=np.int64) * C.LENS_MS["4h"]
    ts = pd.to_datetime(t0, unit="ms", utc=True).strftime(C.TS_FMT["4h"]).tolist()
    return C.Tape(name, "4h", o, h, l, c, t0, ts, ind.atr(h, l, c, RC.ATR_LEN), {})


def _planted(r: int) -> tuple[C.Tape, list, list]:
    """A random walk with a drift of PLANT_MU_ATR x ATR[k] per bar for
    PLANT_BARS bars after EVERY real macro DIE at k, in the DIE's direction —
    planted CAUSALLY: the machine is prefix-stable, so a DIE found on the tape
    so far is unmoved by what is planted after it; the next DIE is then read
    off the planted tape.  Returns (tape, planted DIEs, the final run's DIEs)."""
    inc = _inc(11, r)
    planted, last = [], -1
    while True:
        tape = _tape(inc, f"SYNTH-EDGE-{r:02d}")
        m = RC.run_machine(tape.d, tape.atr, RC.macro_pins(C.FROZEN_SCALE))
        dies = [(e["i"], e["side"]) for e in m["events"] if e["event"] == "breakout-die"]
        nxt = [d for d in dies if d[0] > last]
        if not nxt:
            return tape, planted, dies
        k, side = nxt[0]
        inc[k + 1:k + 1 + PLANT_BARS, :] += ((1.0 if side == "top" else -1.0) * PLANT_MU_ATR
                                             * tape.atr[k] / SANE_SUB)
        planted.append((k, side))
        last = k


def _medians(tape: C.Tape, leak: bool = False, keep_order: bool = False) -> dict:
    """{(cls, horizon): {real, null, real_mean, null_mean, ...}} of ONE tape:
    the real machine and SANE_DRAWS null draws POOLED, both down the census's
    road (N.events_of -> the filed ledger form -> C.grid_rows).  leak = THE
    PLANT: every null DIE read one bar before it is known.  keep_order = the
    design of record's schedule (gaps alone), for the printed comparison."""
    bps, src = C.toll_bps_for(tape.sym)
    bands = N.memo_bands(tape)
    s = float(C.FROZEN_SCALE)
    macro, led_r = N.real_side(tape, s, bps, bands)
    real = N.real_box_set(tape, macro)
    leds = []
    for draw in range(SANE_DRAWS):
        if not leak:
            led = N.null_draw(tape, real, draw, SEED, "frozen3.0", s, bps, bands,
                              keep_order=keep_order)["ledger"]
        else:
            boxes, _ = N.schedule(real, N.draw_rng(SEED, draw, tape.sym, tape.lens, "frozen3.0"))
            nm = N.static_box_machine(tape, boxes)
            leash = RC.flips_and_leash(nm, tape.d, tape.atr, RC.PINS_V2, retests=False)
            view = N.null_view(tape, nm, leash)
            evf, _ = C.census_events(tape, nm, leash, view, bands=bands)
            evf.loc[evf["cls"] == "DIE", "known_at"] -= 1
            led = C.outcome_ledger(tape, evf, view, bps)
        leds.append(N._filed_ledger(led, tape.sym, tape.lens, "frozen3.0", draw))
    rows_r = C.grid_rows(N._filed_ledger(led_r, tape.sym, tape.lens, "frozen3.0", -1),
                         tape.sym, tape.lens, "frozen3.0", s, bps, src)
    rows_n = C.grid_rows(pd.concat(leds, ignore_index=True), tape.sym, tape.lens,
                         "frozen3.0", s, bps, src)
    out = {}
    for a, b in zip(rows_r, rows_n):
        if a["era"] != C.ERA_ALL:          # the synthetic walks carry no era question
            continue
        out[(a["cls"], a["horizon"])] = {
            "real": a["median_term"], "null": b["median_term"], "n_real": a["n"],
            "n_null": b["n"], "real_mean": a["mean_term"], "null_mean": b["mean_term"],
            "real_mfe": a["median_mfe"], "null_mfe": b["median_mfe"],
            "real_mae": a["median_mae"], "null_mae": b["median_mae"]}
    return out


def _boot(d: np.ndarray, m_cells: int, rng) -> tuple[float, float, float, int]:
    """CLUSTER bootstrap over independent tapes: the (1 - alpha / m) percentile
    interval of the mean over tapes.  The tape is the cluster — events on one
    tape share bars, horizons and boxes; tapes share nothing."""
    d = d[np.isfinite(d)]
    if len(d) < 2:
        return float("nan"), float("nan"), float("nan"), len(d)
    means = d[rng.integers(0, len(d), size=(SANE_BOOT, len(d)))].mean(axis=1)
    a = SANE_ALPHA / m_cells
    return (float(np.quantile(means, a / 2)), float(np.quantile(means, 1 - a / 2)),
            float(d.mean()), len(d))


_SANE: dict = {}


def sane_corpus() -> dict:
    if _SANE:
        return _SANE
    t0 = time.perf_counter()
    rw = [_tape(_inc(7, r), f"SYNTH-RW-{r:03d}") for r in range(SANE_TAPES)]
    _SANE["rw"] = [_medians(t) for t in rw]
    _SANE["rw_leak"] = [_medians(t, leak=True) for t in rw]
    _SANE["rw_gaps_only"] = [_medians(t, keep_order=True) for t in rw]
    planted = [_planted(r) for r in range(PLANT_TAPES)]
    _SANE["planted_meta"] = [(len(p), p == d) for _, p, d in planted]
    _SANE["planted"] = [_medians(t) for t, _, _ in planted]
    _SANE["unplanted"] = [_medians(_tape(_inc(11, r), f"SYNTH-EDGE-{r:02d}"))
                          for r in range(PLANT_TAPES)]
    clock(f"F-NULL-SANE corpus: 3 x {SANE_TAPES} random-walk measurements and 2 x "
          f"{PLANT_TAPES} edge tapes of {SANE_BARS} bars: {time.perf_counter() - t0:.1f}s")
    return _SANE


def _holds_zero(per_tape: list, families=SANE_FAMILIES, m_cells: int | None = None,
                seed_key: int = 99) -> tuple[list, list]:
    """(findings, printable lines): every family x class x horizon interval of
    the mean over tapes must hold 0 — ONE Bonferroni over all of them."""
    m = len(families) * len(SANE_CELLS) if m_cells is None else m_cells
    rng = np.random.default_rng([SEED, seed_key])
    bad, lines = [], []
    for name, fn in families:
        lines.append(f"{name}:")
        for c, h in SANE_CELLS:
            d = np.array([fn(t[(c, h)]) for t in per_tape], dtype=float)
            lo, hi, mean, r = _boot(d, m, rng)
            ok = np.isfinite(lo) and lo <= 0.0 <= hi
            if r < len(per_tape) // 2:
                bad.append(f"{name} · {c} {h}: scored on {r} of {len(per_tape)} tapes — too "
                           "few to judge")
            elif not ok:
                bad.append(f"{name} · {c} {h}: mean {mean:+.3f} ATR, interval [{lo:+.3f}, "
                           f"{hi:+.3f}] EXCLUDES 0")
            lines.append(f"  {c:>24} {h:>4}: mean {mean:+.3f} ATR  [{lo:+.3f}, {hi:+.3f}]  tapes "
                         f"{r:>3}  events/tape real "
                         f"{int(np.median([t[(c, h)]['n_real'] for t in per_tape])):>3} "
                         f"null(pooled) {int(np.median([t[(c, h)]['n_null'] for t in per_tape])):>4}"
                         f"  {'holds 0' if ok else 'EXCLUDES 0'}")
    return bad, lines


def _beats(per_tape: list) -> tuple[bool, str]:
    rng = np.random.default_rng([SEED, 98])
    d = np.array([t[PLANT_CELL]["real"] - t[PLANT_CELL]["null"] for t in per_tape], dtype=float)
    lo, hi, mean, r = _boot(d, 1, rng)
    real = float(np.nanmean([t[PLANT_CELL]["real"] for t in per_tape]))
    null = float(np.nanmean([t[PLANT_CELL]["null"] for t in per_tape]))
    return bool(np.isfinite(lo) and lo > 0.0), (
        f"{PLANT_CELL[0]} {PLANT_CELL[1]}: real {real:+.3f} ATR vs null {null:+.3f} ATR, "
        f"mean(real - null) {mean:+.3f}, {100 * (1 - SANE_ALPHA):g}% interval [{lo:+.3f}, "
        f"{hi:+.3f}] over {r} tapes")


def _z_line(per_tape: list, key: str) -> tuple[int, float, list]:
    """(cells with a negative mean, the most negative tape-clustered z, all z)."""
    zs = []
    for cell in SANE_CELLS:
        d = np.array([t[cell][key] for t in per_tape], dtype=float)
        d = d[np.isfinite(d)]
        zs.append(float(d.mean() / (d.std(ddof=1) / np.sqrt(len(d)))))
    return int(sum(z < 0 for z in zs)), float(min(zs)), zs


def sane_break():
    R = sane_corpus()

    def leaked_null():
        return _holds_zero(R["rw_leak"])[0]

    def plant_removed():
        ok, detail = _beats(R["unplanted"])
        return [] if ok else [f"real does NOT beat null — {detail}"]
    return plants([
        ("A LEAKED NULL on the random walk: every null DIE read one bar before it is known",
         leaked_null),
        ("THE PLANT REMOVED: the same seeds with no drift after a DIE — real must NOT beat null",
         plant_removed),
    ])


def sane_real():
    R = sane_corpus()
    bad, lines = _holds_zero(R["rw"])
    say(f"        RANDOM WALK — {SANE_TAPES} tapes x {SANE_BARS} bars (arithmetic, driftless), "
        f"SCALE {C.FROZEN_SCALE:g}, {SANE_DRAWS} null draws pooled per tape; cluster bootstrap "
        f"over tapes, B = {SANE_BOOT:,}, family-wise alpha {SANE_ALPHA} (ONE Bonferroni over "
        f"{len(SANE_FAMILIES) * len(SANE_CELLS)} intervals). An as-of-clean event on a driftless "
        f"walk has MEAN term zero — a martingale identity — so each side is also held to 0 on "
        f"its own, not only to the other:")
    for x in lines:
        say(f"        {x}")
    for key, name in (("_mfe", "median MFE"), ("_mae", "median MAE")):
        b2, l2 = _holds_zero(R["rw"], families=(
            (f"{name}, real - null", lambda t, k=key: t["real" + k] - t["null" + k]),),
            m_cells=len(SANE_CELLS))
        say(f"        {name}, real - null — PRINTED, NOT ASSERTED (a pivot-born range and a "
            f"static box meet the ATR ruler differently; on a walk that is a fact about the "
            f"ruler, not an edge): {len(b2)} of {len(SANE_CELLS)} intervals exclude 0")
        for x in l2[1:]:
            say(f"        {x}")
    neg_s, min_s, _ = _z_line(R["rw"], "null_mean")
    neg_g, min_g, _ = _z_line(R["rw_gaps_only"], "null_mean")
    say(f"        [N-c] THE SCHEDULE, PRINTED NOT ASSERTED — the null's mean term over the same "
        f"{SANE_TAPES} tapes, tape-clustered z per cell: gaps + order permuted {neg_s} of "
        f"{len(SANE_CELLS)} cells negative, most negative z {min_s:+.2f} · gaps ALONE (the "
        f"design of record) {neg_g} of {len(SANE_CELLS)} negative, most negative z {min_g:+.2f}. "
        f"The gaps-only leak is small and {SANE_TAPES} tapes do not resolve it at the "
        f"family-wise bar; the argument is the mechanism (a life is a future fact about the "
        f"place it was earned), the z is its trace")
    n_planted = sum(k for k, _ in R["planted_meta"])
    if not all(ok for _, ok in R["planted_meta"]):
        bad.append("the planted tapes' real DIEs are not the DIEs the drift was planted after "
                   "— the plant was not causal")
    ok, detail = _beats(R["planted"])
    if not ok:
        bad.append(f"PLANTED EDGE: real does not beat null — {detail}")
    say(f"        PLANTED EDGE — {PLANT_TAPES} tapes, a drift of {PLANT_MU_ATR} ATR[k] per bar for "
        f"{PLANT_BARS} bars after each of {n_planted} REAL macro DIEs, planted causally: {detail}")
    for c, h in (("DIE", "H100"), ("breach", "H20"), ("memory-touch-2s", "H20")):
        rr = float(np.nanmean([t[(c, h)]["real"] for t in R["planted"]]))
        nn = float(np.nanmean([t[(c, h)]["null"] for t in R["planted"]]))
        say(f"          (printed) {c} {h}: real {rr:+.3f} vs null {nn:+.3f} ATR")
    return not bad, (
        f"RANDOM WALK: on {SANE_TAPES} independent driftless tapes the real machine's median "
        f"term and the null's AGREE, and each side's own mean term holds 0, for all "
        f"{len(SANE_CELLS)} class x horizon cells — every one of the "
        f"{len(SANE_FAMILIES) * len(SANE_CELLS)} Bonferroni intervals holds 0 (MFE / MAE "
        f"printed beside, not asserted). PLANTED EDGE: {detail} — real BEATS null, and every "
        f"planted tape's real DIEs are exactly the {n_planted} the drift was planted after"
        if not bad else f"{len(bad)} finding(s): " + "; ".join(bad[:4]))


# ═════════════════════════════════════════════════════════ F-NULL-GRID
def _root_tables(root: Path | None = None) -> dict:
    root = NROOT if root is None else root
    return {p.stem: pd.read_parquet(p) for p in sorted(root.glob("*.parquet"))}


def _census_rows(man: dict) -> pd.DataFrame | None:
    croot = ROOT / man["census_root"] if not Path(man["census_root"]).is_absolute() \
        else Path(man["census_root"])
    p = croot / "outcome_grid.parquet"
    if not p.exists():
        return None
    g = pd.read_parquet(p)
    cman = json.loads((croot / "build_manifest.json").read_text())
    if cman["commission"]["assets"] != man["commission"]["assets"]:
        g = g[g["asset"] != "POOLED:ALL"]           # a pool of other assets is another number
    return g


def _own_summary(grid: pd.DataFrame) -> dict:
    out = {}
    for key, G in grid.groupby(["asset", "lens", "scale_kind", "cls", "era", "horizon"]):
        for stat in DECL_STATS:
            rv = float(G[G["draw"] == DECL_REAL_DRAW][stat].iloc[0])
            nv = G[G["draw"] >= 0][stat].to_numpy(float)
            ok = np.sort(nv[np.isfinite(nv)])
            if not len(ok):
                out[key + (stat,)] = (rv, np.nan, np.nan, np.nan, np.nan, 0)
                continue
            below, ties = int(np.sum(ok < rv)), int(np.sum(ok == rv))
            out[key + (stat,)] = (rv, float(np.median(ok)), float(np.quantile(ok, 0.25)),
                                  float(np.quantile(ok, 0.75)),
                                  (100.0 * (below + ties / 2.0) / len(ok)
                                   if np.isfinite(rv) else np.nan), len(ok))
    return out


def _grid_findings(tables: dict, man: dict, census: pd.DataFrame | None) -> list[str]:
    bad = []
    com = man["commission"]
    assets = list(com["assets"]) + ["POOLED:ALL"]
    draws = [DECL_REAL_DRAW] + list(range(man["n_draws"]))
    if sorted(tables) != sorted(DECL_ROOT_TABLES):
        bad.append(f"root tables {sorted(tables)} != declared {sorted(DECL_ROOT_TABLES)}")
        return bad
    g, s, cv = tables["null_grid"], tables["null_summary"], tables["null_coverage"]
    decl = {(a, l, k, c, e, d, h) for a in assets for l in com["lenses"]
            for k in com["scale_kinds"] for c in CF.DECL_CLASSES for e in CF.DECL_ERAS
            for d in draws for h in CF.DECL_HORIZONS}
    got = list(zip(g["asset"], g["lens"], g["scale_kind"], g["cls"], g["era"], g["draw"],
                   g["horizon"]))
    grid_whole = set(got) == decl and len(got) == len(decl)
    if not grid_whole:
        bad.append(f"null_grid: {len(got)} rows / {len(set(got))} keys vs {len(decl)} declared "
                   f"(missing {len(decl - set(got))}, undeclared {len(set(got) - decl)})")
    if not ((g["source"] == "REAL") == (g["draw"] == DECL_REAL_DRAW)).all():
        bad.append("null_grid: source REAL is not exactly draw -1")
    nan = g["median_term"].isna()
    if not ((g["n"] == 0) == nan).all() or not (g.loc[nan, "nan_reason"] != "").all() \
            or not (g.loc[~nan, "nan_reason"] == "").all():
        bad.append("null_grid: NaN without n = 0 and a reason, or a reason on a number")
    prov = g["cls"].isin(CF.DECL_TUNED)
    if not (g.loc[prov, "pins_status"] == C.TUNED_PINS).all() \
            or (g.loc[~prov, "pins_status"] == C.TUNED_PINS).any():
        bad.append("null_grid: a tuned-pins row says frozen, or the reverse")
    if set(g["schedule_variant"].unique()) != {man["commission"]["schedule_variant"]}:
        bad.append("null_grid: a row carries a schedule variant the commission does not")
    decl_s = {k[:3] + (k[3], k[4], k[6], st) for k in decl for st in DECL_STATS}
    got_s = list(zip(s["asset"], s["lens"], s["scale_kind"], s["cls"], s["era"],
                     s["horizon"], s["stat"]))
    if set(got_s) != decl_s or len(got_s) != len(decl_s):
        bad.append(f"null_summary: {len(got_s)} rows vs {len(decl_s)} declared")
    elif grid_whole:                    # a summary is re-derived from a WHOLE grid only
        own = _own_summary(g)
        for r in s.itertuples():
            w = own[(r.asset, r.lens, r.scale_kind, r.cls, r.era, r.horizon, r.stat)]
            if not (same(r.real, w[0]) and same(r.null_median, w[1], 2) and same(r.null_q25, w[2], 2)
                    and same(r.null_q75, w[3], 2) and same(r.real_pctile_in_null, w[4], 2)
                    and int(r.n_draws_valid) == w[5] and int(r.n_draws) == man["n_draws"]):
                bad.append(f"null_summary {r.asset} {r.lens} {r.scale_kind} {r.cls} {r.horizon} "
                           f"{r.stat}: not what the FILED grid re-derives")
                break
    decl_c = {(a, l, k, d) for a in com["assets"] for l in com["lenses"]
              for k in com["scale_kinds"] for d in range(man["n_draws"])}
    if set(zip(cv["asset"], cv["lens"], cv["scale_kind"], cv["draw"])) != decl_c \
            or len(cv) != len(decl_c):
        bad.append("null_coverage: not one row per declared (asset, lens, scale kind, draw)")
    if not cv["alive_bars_identity"].all():
        bad.append("null_coverage: a draw's alive-bar identity is False")
    if census is None:
        bad.append("the census grid the null stands beside is not on disk")
    else:
        real = g[g["draw"] == DECL_REAL_DRAW].set_index(C.GRID_KEY).sort_index()
        cen = census.set_index(C.GRID_KEY).sort_index()
        cen = cen[cen.index.isin(real.index)]
        n_missing = len(real.index.difference(cen.index))
        pooled_only = real.index.difference(cen.index).get_level_values("asset").unique().tolist()
        if n_missing and pooled_only != ["POOLED:ALL"]:
            bad.append(f"{n_missing} real rows have no row in the census grid")
        r2 = real.loc[cen.index]
        for col in ("n_events", "n", "median_term", "toll_atr", "net", "hit_rate",
                    "median_mfe", "median_mae", "toll_atr_all"):
            if not np.array_equal(r2[col].to_numpy(float), cen[col].to_numpy(float),
                                  equal_nan=True):
                bad.append(f"the REAL rows' {col} is not the census grid's")
    for name, df in tables.items():
        miss = [c for c in C.COLLAR_COLUMNS + C.AS_OF_COLUMNS if c not in df.columns]
        if miss:
            bad.append(f"{name}: collar / as-of column(s) missing {miss}")
        elif df[list(C.COLLAR_COLUMNS + C.AS_OF_COLUMNS)].isna().any().any():
            bad.append(f"{name}: a collar / as-of cell is null")
        hit = [c for c in df.columns if c.lower() in VERDICT_COLUMNS]
        if hit:
            bad.append(f"{name}: verdict column(s) {hit} — Tier-E files none")
        if name not in man["keys"]:
            bad.append(f"{name}: no declared key in the manifest [F-KEY totality]")
        elif df.duplicated(subset=man["keys"][name]).any():
            bad.append(f"{name}: duplicate on its declared key")
    if "leans" in tables and len(tables["leans"]) != len(N.LEANS):
        bad.append("leans: not every lean is filed")
    return bad


def grid_break():
    man, census = manifest(), _census_rows(manifest())
    T = _root_tables()

    def edit(name, fn):
        t = dict(T)
        t[name] = fn(T[name].copy())
        return _grid_findings(t, man, census)

    def real_moved(g):
        ix = g.index[(g["draw"] == DECL_REAL_DRAW) & (g["n"] > 0)][0]
        g.loc[ix, "median_term"] += 1e-6
        return g

    def pctile_moved(s):
        ix = s.index[s["real_pctile_in_null"].notna()][0]
        s.loc[ix, "real_pctile_in_null"] = (s.loc[ix, "real_pctile_in_null"] + 50.0) % 100.0
        return s

    def collar_nulled(c):
        c["gates"] = c["gates"].astype(object)
        c.loc[c.index[0], "gates"] = None
        return c
    return plants([
        ("ONE DRAW'S ROW DROPPED from a COPY of the grid",
         lambda: edit("null_grid", lambda g: g.iloc[1:])),
        ("A `verdict` COLUMN on a COPY of the summary",
         lambda: edit("null_summary", lambda s: s.assign(verdict="beats the null"))),
        ("A `p_value` COLUMN on a COPY of the summary (the percentile is not one)",
         lambda: edit("null_summary", lambda s: s.assign(p_value=0.04))),
        ("ONE REAL MEDIAN moved by 1e-6 in a COPY (it must be the census grid's)",
         lambda: edit("null_grid", real_moved)),
        ("ONE PERCENTILE moved in a COPY of the summary",
         lambda: edit("null_summary", pctile_moved)),
        ("A COLLAR CELL nulled in a COPY of the coverage table",
         lambda: edit("null_coverage", collar_nulled)),
        ("A TABLE MISSING from the root", lambda: _grid_findings(
            {k: v for k, v in T.items() if k != "null_coverage"}, man, census)),
    ])


def grid_real():
    man = manifest()
    census = _census_rows(man)
    T = _root_tables()
    bad = _grid_findings(T, man, census)
    for sym, lens in cells(man):
        rc = receipt(sym, lens)
        have = sorted(rc["tables"])
        if have != sorted(DECL_CELL_TABLES):
            bad.append(f"cell {sym} {lens}: tables {have}")
        if not rc["census_anchor"].startswith("ANCHORED"):
            bad.append(f"cell {sym} {lens}: {rc['census_anchor']}")
    g = T["null_grid"]
    return not bad, (
        f"{rel(NROOT)}: null_grid holds EXACTLY the {len(g)} declared keys ((assets + POOLED:ALL) "
        f"x lenses x scale kinds x {len(CF.DECL_CLASSES)} classes x draws -1..{man['n_draws'] - 1} "
        f"x {len(CF.DECL_HORIZONS)} horizons), source REAL iff draw -1, NaN exactly where n = 0 "
        f"and with its reason, provisional pins labelled; the REAL rows equal the census's own "
        f"filed grid ({man['census_root']}) column for column, and every cell's receipt says "
        f"ANCHORED; null_summary ({len(T['null_summary'])} rows x {len(DECL_STATS)} stats) "
        f"re-derives from the FILED grid — median, quartiles, mid-rank percentile; one coverage "
        f"row per draw, every identity True; collar + all {len(C.AS_OF_COLUMNS)} as-of columns "
        f"on every table, none null; NO verdict / p-value column; every table keyed and unique "
        f"[F-KEY]" if not bad else f"{len(bad)} finding(s): " + "; ".join(bad[:4]))


# ═════════════════════════════════════════════════════════ F-NULL-DET
DET_ASSETS = ("BTCUSDT", "ETHUSDT")     # two, so the POOLED rows pool something
DET_LENS = "4h"
_DET: dict = {}


def _build(root: Path, hash_seed: str, draws: int, seed: int = SEED) -> str:
    env = dict(os.environ, PYTHONHASHSEED=hash_seed, PYTHONDONTWRITEBYTECODE="1")
    man = manifest()
    # the fresh build must be THIS root's commission, or "the filed cell is what a
    # fresh build makes" would compare two different commissions
    com = man["commission"]
    r = subprocess.run([PY, str(ROOT / "scripts" / "tierc10_null.py"), "--assets",
                        ",".join(DET_ASSETS), "--lenses", DET_LENS, "--draws", str(draws),
                        "--seed", str(seed), "--out", str(root),
                        "--scale-kind", ",".join(com["scale_kinds"]),
                        "--variant", com.get("schedule_variant", N.VARIANT_DEFAULT),
                        "--census-root", str(ROOT / man["census_root"])],
                       capture_output=True, text=True, env=env, timeout=3600, cwd=str(ROOT))
    if r.returncode != 0:
        raise RuntimeError(f"null subprocess failed: {r.stdout[-400:]} {r.stderr[-400:]}")
    return r.stdout


def det_runs() -> dict:
    if _DET:
        return _DET
    td = Path(tempfile.mkdtemp(prefix="tc10_null_fdet_"))
    a, b = td / "run1", td / "run2"
    k = manifest()["n_draws"]
    t0 = time.perf_counter()
    _build(a, "1", k)
    _build(b, "20260921", k)
    out3 = _build(a, "7", k)                        # the SAME root again: must resume
    clock(f"three subprocess builds of {DET_ASSETS} x {DET_LENS} x {k} draws: "
          f"{time.perf_counter() - t0:.1f}s")
    _DET.update({"td": td, "a": a, "b": b, "resume_stdout": out3, "k": k})
    return _DET


def _distinct_findings(sets: dict) -> list[str]:
    """sets = {label: [(confirm_i, u), ...]}: no two labels may hold one box set."""
    bad, labels = [], sorted(sets)
    for x in range(len(labels)):
        for y in range(x + 1, len(labels)):
            if sets[labels[x]] == sets[labels[y]]:
                bad.append(f"{labels[x]} and {labels[y]} drew the SAME boxes")
    return bad


def _box_sets(bx: pd.DataFrame) -> dict:
    return {f"{k[0]} {k[1]} draw {k[2]}": list(zip(G.sort_values("box")["confirm_i"].tolist(),
                                                     G.sort_values("box")["u"].tolist()))
            for k, G in bx.groupby(["asset", "scale_kind", "draw"])}


def det_break():
    R = det_runs()
    cell = R["b"] / "cells" / f"{DET_ASSETS[0]}__{DET_LENS}"

    def moved_bytes():
        c = R["td"] / "plant1"
        shutil.copytree(R["b"], c)
        p = c / "cells" / cell.name / "null_events.parquet"
        d = pd.read_parquet(p)
        ix = d.index[d["term_H20"].notna()][0]
        d.loc[ix, "term_H20"] += 1e-6
        d.to_parquet(p, index=False)
        return CF._det_findings(R["a"], c)

    def stale_cell():
        c = R["td"] / "plant2"
        shutil.copytree(R["b"], c)
        p = c / "cells" / cell.name / "null_grid.parquet"
        d = pd.read_parquet(p)
        d.loc[d.index[0], "n"] += 1
        d.to_parquet(p, index=False)
        com = manifest()["commission"]
        ok, why = N.cell_is_current(c, DET_ASSETS[0], DET_LENS, tuple(com["scale_kinds"]),
                                    R["k"], SEED, N.code_sha(),
                                    com.get("schedule_variant", N.VARIANT_DEFAULT))
        return [] if ok else [f"resume REFUSES the cell: {why}"]

    def wall_clock():
        c = R["td"] / "plant3"
        shutil.copytree(R["b"], c)
        p = c / "build_manifest.json"
        p.write_text(json.dumps(dict(json.loads(p.read_text()), elapsed_s=1.23)))
        return CF._clock_hits(c)

    def draw_index_ignored():
        own = real_of(DET_ASSETS[0], DET_LENS, 3.0)
        real = N.real_box_set(own["tape"], own["macro"])
        sets = {}
        for label in ("draw 0", "draw 1"):          # the plant: BOTH ride draw 0's stream
            boxes, _ = N.schedule(real, N.draw_rng(SEED, 0, DET_ASSETS[0], DET_LENS, "frozen3.0"))
            sets[label] = [(b.confirm_i, b.u) for b in boxes]
        return _distinct_findings(sets)
    return plants([
        ("ONE FLOAT MOVED by 1e-6 in a COPY of run 2's null ledger", moved_bytes),
        ("A CELL TABLE EDITED behind its receipt (resume must not trust it)", stale_cell),
        ("A WALL-CLOCK FIELD (the artifact scan must be able to see one)", wall_clock),
        ("THE DRAW INDEX IGNORED: two draws riding one stream", draw_index_ignored),
    ])


def det_real():
    R = det_runs()
    try:
        bad = CF._det_findings(R["a"], R["b"])
        if R["resume_stdout"].count("REUSED") != len(DET_ASSETS):
            bad.append("a third build into the same root did not REUSE its current cells")
        bad += [f"a wall-clock field: {x}" for x in CF._clock_hits(R["a"])]
        ma = json.loads((R["a"] / "build_manifest.json").read_text())
        T = _root_tables(R["a"])
        # ETHUSDT 4h is not in the smoke census: its real rows have nothing to be
        # held to there — printed by the build as UNANCHORED, not judged here
        bad += [f"(2-asset root) {x}" for x in _grid_findings(T, ma, _census_rows(ma))
                if "no row in the census grid" not in x]
        bx = pd.concat([pd.read_parquet(R["a"] / "cells" / f"{s}__{DET_LENS}" / "null_boxes.parquet")
                        for s in DET_ASSETS], ignore_index=True)
        sets = _box_sets(bx)
        bad += _distinct_findings(sets)
        # a different SEED -> different boxes; the same (seed, draw) -> the same
        own = real_of(DET_ASSETS[0], DET_LENS, 3.0)
        real = N.real_box_set(own["tape"], own["macro"])
        one = [N.schedule(real, N.draw_rng(s, 0, DET_ASSETS[0], DET_LENS, "frozen3.0"))[0]
               for s in (SEED, SEED, 20260816)]
        if one[0] != one[1]:
            bad.append("the same (seed, draw, cell) drew two different box sets in one process")
        if one[0] == one[2]:
            bad.append("seed 20260921 and the lineage seed 20260816 drew the SAME boxes")
        filed = C.cell_dir(NROOT, DET_ASSETS[0], DET_LENS) / "cell.json"
        tied = "no filed cell to compare"
        if filed.exists() and json.loads(filed.read_text())["n_draws"] == R["k"]:
            fa = json.loads(filed.read_text())["tables"]
            fb = json.loads((R["a"] / "cells" / filed.parent.name / "cell.json").read_text())["tables"]
            if {k: v["sha"] for k, v in fa.items()} != {k: v["sha"] for k, v in fb.items()}:
                bad.append(f"the FILED {filed.parent.name} null cell is not what a fresh build makes")
            tied = f"the FILED {filed.parent.name} cell carries the same table shas"
        n_files = len([p for p in R["a"].rglob("*") if p.is_file()])
        return not bad, (
            f"two subprocess builds of {list(DET_ASSETS)} x {DET_LENS} x {R['k']} draws under "
            f"PYTHONHASHSEED 1 and 20260921: the same {n_files} files, BYTE-identical (parquets, "
            f"receipts, manifest), every content sha equal and equal to the manifest's; a third "
            f"build into run 1's root REUSES both cells; its tables are WHOLE and the POOLED:ALL "
            f"rows pool two assets; no wall-clock field in any artifact; all {len(sets)} filed "
            f"(asset, scale kind, draw) box sets are pairwise DIFFERENT; seed 20260816 draws "
            f"different boxes, the same (seed, draw) the same; {tied} "
            f"(null_grid sha {ma['sha']['null_grid'][:16]}…)"
            if not bad else f"{len(bad)} finding(s): " + "; ".join(bad[:4]))
    finally:
        shutil.rmtree(R["td"], ignore_errors=True)


# ════════════════════════════════════════════════════════════ main
LEGS = (
    ("F-NULL-COV", "the alive-bar identity, every draw — matched coverage PRINTED",
     "any draw's scheduled alive-bar MASK (rebuilt here from the filed boxes) differs from the "
     "real alive-bar count (the census as-of layer's in_range sum) by even one bar; the boxes' "
     "sources are not a permutation of the real ranges, or a life or an ATR height is not its "
     "source's; the gaps are not a permutation of the real gaps; two windows overlap, or one "
     "leaves the tape or starts inside the ATR warm floor; a filed coverage figure is not "
     "what the filed boxes and the raw closes give.",
     cov_break, cov_real),
    ("F-NULL-BOX", "the frozen pins bind the static box — re-walked on raw bars; a failed hold FAILS",
     "a filed breach / harden / DIE / v1 memory-touch row set differs from a plain walk of the "
     "raw parquet (own ATR; 7 / 8 / 1.5 typed here) for ANY filed box; a filed flip-hold does "
     "not hold on the raw bars or is anchored anywhere but touch + 6; a filed memory-touch-2s "
     "is not a first two-sided touch inside the TTL; a ledger term / MFE / MAE / toll differs "
     "from a bar-by-bar walk, or a censored horizon carries a number; a filed grid row is not "
     "what the filed ledger re-derives.",
     box_break, box_real),
    ("F-NULL-ASOF", "the static-box machine is as-of clean — known_at discipline, prefix-stable",
     "for any cut t (seeded random, or aimed at a null DIE, a confirm, a window's middle, a "
     "hold window) the null's class events with known_at <= t - 1 or any per-bar array on "
     "[0, t) differ between tape[:t] and the full tape under the SAME boxes; or a prefix files "
     "an event known after its last bar.",
     asof_break, asof_real),
    ("F-NULL-SANE", "random walk: real and null AGREE · planted edge: real BEATS null",
     "on the driftless synthetic tapes the Bonferroni cluster-bootstrap interval of "
     "mean(real median term - null median term), of the real machine's own mean term, or of "
     "the null's own mean term EXCLUDES 0 for any class x horizon, or a cell is scored on "
     "fewer than half the tapes; on the planted-edge tapes the interval for DIE "
     "H20 does not lie strictly above 0, or the planted tapes' real DIEs are not the ones the "
     "drift was planted after.",
     sane_break, sane_real),
    ("F-NULL-GRID", "every null table whole — declared vs filed, real rows = the census's, collared",
     "a declared (asset | pool, lens, scale kind, class, ERA, draw, horizon) key is missing, "
     "undeclared or repeated; a REAL row differs from the census's own filed grid; a summary "
     "row is not what the FILED grid re-derives; a NaN has no reason; a coverage row is "
     "missing or its identity False; a collar or as-of column is missing or null; a verdict or "
     "p-value column exists; a table has no declared key or repeats on it; a cell is UNANCHORED; "
     "a row carries a schedule variant the commission does not name.",
     grid_break, grid_real),
    ("F-NULL-DET", "same seed, same bytes — different draw or seed, different boxes; resume honest",
     "two subprocess builds under different PYTHONHASHSEED differ in any file's bytes or any "
     "table's content sha; a rebuild into a current root recomputes; resume trusts an edited "
     "table; an artifact carries a wall-clock field; two (asset, scale kind, draw) box sets "
     "coincide; seed 20260816 draws the same boxes as 20260921; the filed cell is not what a "
     "fresh build makes.",
     det_break, det_real),
)


def main() -> int:
    want = [a.lower().replace("_", "-") for a in sys.argv[1:] if not a.startswith("--null-root=")]
    legs = [x for x in LEGS if not want or any(w in x[0].lower() for w in want)]
    man = manifest()
    say(f"as_of_last_closed_4h: {man['as_of']}")
    say("=" * 78)
    say("TIER-C10 STAGE 0c · CENSUS-R NULL MODEL FIXTURES — break leg first, RED or void")
    say("=" * 78)
    say(f"seed {SEED} · substrate NAIAD_CACHE_DIR={os.environ.get('NAIAD_CACHE_DIR')}")
    say(f"null root {rel(NROOT)} · commission {man['commission']['label']}: "
        f"{man['commission']['assets']} x {man['commission']['lenses']} x "
        f"{man['commission']['scale_kinds']} x {man['n_draws']} draws (seed {man['seed']}) · "
        f"is_the_contract_null = {man['commission']['is_the_contract_null']}")
    say(f"  {C.TIER}")
    say(f"  null + census + port: code sha {N.code_sha()}")
    say(f"  NULL LAW: {N.NULL_LAW}")
    for src, s in sorted(man["input_sha"].items()):
        say(f"  input {src:28} sha256 {s[:16]}…")
    for ln in N.LEANS:
        say(ln)
    for fid, title, fails_if, b, r in legs:
        t0 = time.perf_counter()
        prove(fid, title, fails_if, b, r)
        clock(f"{fid}: {time.perf_counter() - t0:.1f}s")
    say(f"\nTIER-C10 CENSUS-R NULL FIXTURES: {len(RFX.PASSED)}/{len(legs)} GREEN"
        + (f" · FAILED: {RFX.FAILED}" if RFX.FAILED else ""))
    say("warranty: these lines are true AS OF the substrate, the null root and the bars named "
        "above and of no other; the corridor advances with the cache [TC6V-a]")
    if not want:                       # a partial run never overwrites the full transcript
        (NROOT / "FIXTURES_NULL.txt").write_text("\n".join(RFX.T) + "\n", encoding="utf-8")
        print(f"transcript -> {rel(NROOT / 'FIXTURES_NULL.txt')}")
    if RFX.FAILED:
        print("*** HALT: fixture mismatch. Nothing downstream is trustworthy. ***")
    return 1 if RFX.FAILED else 0


if __name__ == "__main__":
    raise SystemExit(main())
