"""S-2 instrumentation (engine 1.0.10) — corrected simulator + new families.

Measure-only. The candidate-path construction is UNCHANGED from S-1
(engine.s1.candidate_path, pinned semantics); what 1.0.10 corrects is the
EXIT WALK: `sim_corrected` re-derives exits under the engine's own wake
order — (1) queued open-flatten at camp_end+1, (2) gap at the open,
(3) intra-bar touch — with coverage from fill_i (the fill bar included,
no gap leg there: the fill IS the open). The legacy walk (engine.s1
.simulate_exit) is retained solely for the F-DELTA semantics-delta fixture.

Two-line = one corrected walk on the pointwise-tighter of the native line
and the candidate line (for a long, the higher stop is struck first; both
lines flatten together at campaign death) — no derivation shortcut, and on
zero-advance tranches the combined line equals the candidate line
identically, which is F-IDENT2's structural content.

All grids and mechanizations pinned in the S-2 ledger pre-registration
(2026-07-19, commit 6af174b). Emission neutrality as S-1: replay attaches
these outputs to rows it was already emitting.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from engine import indicators as ind
from engine.cells import Cell
from engine.journal import iso
from engine.s1 import (S1Context, S1_INTERVAL_MS, _map_htf, _pivots,
                       candidate_path, r6, simulate_exit as legacy_exit)

TL_CANDS = ["ema200_gov_b0.5", "ema200_gov_b0.0", "ema89_gov_b0.0"]
LEVEL_TFS = ["4h", "12h", "1d"]
DET_TFS = ["30m", "1h"]
REPL_TF = "4h"
ALL_DET_TFS = DET_TFS + [REPL_TF]
D1_GRID = [(20, 2.0), (20, 3.0), (40, 2.0), (40, 3.0), (80, 2.0), (80, 3.0)]
D2_GRID = [(0.15, 10), (0.15, 20), (0.25, 10), (0.25, 20)]
D3_GRID = [(3, 0.5), (3, 1.0), (4, 0.5), (4, 1.0)]
D4_GRID = [(0.25, 3), (0.25, 5), (0.5, 3), (0.5, 5)]
F4_TFS = ["exec", "30m", "1h"]
F4_VOID_BARS = 200
F8_STEPS = {"intraday": ["30m", "15m", "5m"],
            "swing": ["1h", "30m", "15m"],
            "position": ["4h", "1h", "30m"]}
F8_B = [3, 5]
HORIZONS = [5, 20, 100]
CAP_R = 10.0
HEADWIND_ATR = 0.5
GATE_TOL = 1e-9


def _fwd_bps(sig, j, ks):
    """Signed forward returns (up-positive) from next exec open."""
    out = {}
    if j + 1 >= len(sig.c):
        return {f"fwd_{k}_bps": None for k in ks}
    e = sig.o[j + 1]
    for k in ks:
        out[f"fwd_{k}_bps"] = (r6((sig.c[j + k] - e) / e * 1e4)
                               if j + k < len(sig.c) else None)
    return out


# ══════════════════════════════════════════ corrected simulator (1.0.10)
def working(series, f, j, entry_stop):
    return entry_stop if j == f else series[j - 1 - f] \
        if 0 <= j - 1 - f < len(series) else series[-1]


def sim_corrected(sig, d, f, camp_end, entry_stop, series):
    """Engine-wake-order exit walk. series[j-f] = value confirmed at bar j.
    Returns (exit_px, exit_bar, kind) — kind in {flatten, gap, stop}."""
    n = len(sig.c)
    for j in range(f, camp_end + 2):
        if j >= n:
            return None
        if j == camp_end + 1:
            return float(sig.o[j]), j, "flatten"
        w = working(series, f, j, entry_stop)
        if w != w:
            continue
        if j > f and (sig.o[j] - w) * d <= 0:
            return float(sig.o[j]), j, "gap"
        if (sig.l[j] <= w) if d == 1 else (sig.h[j] >= w):
            return float(w), j, "stop"
    return None


def two_line_walk(sig, d, f, camp_end, entry_stop, native, cand):
    """Corrected walk on both lines; exits at the first touch of either.
    Returns (exit_px, exit_bar, kind, source in {cand, base, both})."""
    n = len(sig.c)
    for j in range(f, camp_end + 2):
        if j >= n:
            return None
        if j == camp_end + 1:
            return float(sig.o[j]), j, "flatten", "both"
        wn = working(native, f, j, entry_stop)
        wc = working(cand, f, j, entry_stop)
        if wn != wn and wc != wc:
            continue
        if wn != wn:
            tight, src = wc, "cand"
        elif wc != wc:
            tight, src = wn, "base"
        elif (wc - wn) * d > GATE_TOL:
            tight, src = wc, "cand"
        elif (wn - wc) * d > GATE_TOL:
            tight, src = wn, "base"
        else:
            tight, src = wn, "both"
        if j > f and (sig.o[j] - tight) * d <= 0:
            return float(sig.o[j]), j, "gap", src
        if (sig.l[j] <= tight) if d == 1 else (sig.h[j] >= tight):
            return float(tight), j, "stop", src
    return None


# ══════════════════════════════════════════════════════ S2 context
class S2Context:
    def __init__(self, cell: Cell, cfg: dict, sig, trades, data: dict,
                 resampled_dir: Path):
        self.base = S1Context(cell, cfg, sig, trades, data, resampled_dir)
        self.sig = sig
        self.cell = cell
        self.n = len(sig.c)
        self.step = self.base.step
        # native TF frames for levels + detectors (+ exec alias)
        self.native = {}
        lo = int(sig.exec_open_ms[0])
        hi = int(sig.exec_open_ms[-1]) + self.step
        for tf in sorted(set(LEVEL_TFS + ALL_DET_TFS)):
            step_tf = S1_INTERVAL_MS[tf]
            if tf in data:
                df = data[tf]
            elif tf in ("30m", "1d"):
                df = pd.read_parquet(resampled_dir /
                                     f"{cell.symbol}_{tf}.parquet")
                df = df[(df["open_time"] >= lo - step_tf * 300)
                        & (df["open_time"] <= hi)].reset_index(drop=True)
            else:
                from engine import data as dl
                df = dl.load_klines(cell.symbol, tf, lo - step_tf * 300, hi)
            o = df["open"].to_numpy(float)
            h = df["high"].to_numpy(float)
            l = df["low"].to_numpy(float)
            c = df["close"].to_numpy(float)
            fr = {"ms": df["open_time"].to_numpy(np.int64),
                  "o": o, "h": h, "l": l, "c": c,
                  "atr": ind.atr(h, l, c, cfg["signal"]["atr_len"]),
                  "e9": ind.ema(c, cfg["signal"]["len_fast"]),
                  "e89": ind.ema(c, cfg["signal"]["len_slow"])}
            fr["idx"] = _map_htf(sig.exec_open_ms, fr["ms"], step_tf)
            # first exec bar at which each TF bar is visible (confirmed)
            vis = np.full(len(fr["ms"]), -1, dtype=np.int64)
            prev = -1
            for j, ix in enumerate(fr["idx"]):
                if ix > prev:
                    for t in range(prev + 1, ix + 1):
                        vis[t] = j
                    prev = ix
            fr["vis"] = vis
            self.native[tf] = fr
        # confirmed (5,5) pivots per level TF, native coordinates
        self.lv_piv = {}
        for tf in LEVEL_TFS:
            fr = self.native[tf]
            ch, vh = _pivots(fr["h"], 5, 5, low=False)
            cl, vl = _pivots(fr["l"], 5, 5, low=True)
            self.lv_piv[tf] = {"hi": (ch, vh), "lo": (cl, vl)}
        # exec-frame (5,5) pivots come from S1Context.pivots
        # prior-day / prior-week levels from the 1d frame
        d1 = self.native["1d"]
        day = d1["ms"] // 86_400_000
        wk = (day - (day + 3) % 7)
        self.pd_hi = np.concatenate(([np.nan], d1["h"][:-1]))
        self.pd_lo = np.concatenate(([np.nan], d1["l"][:-1]))
        pw_hi = np.full(len(day), np.nan)
        pw_lo = np.full(len(day), np.nan)
        prev_w, cur_w = None, None
        hi_prev = lo_prev = np.nan
        hi_cur = lo_cur = np.nan
        for j in range(len(day)):
            if wk[j] != cur_w:
                prev_w, cur_w = cur_w, wk[j]
                hi_prev, lo_prev = hi_cur, lo_cur
                hi_cur, lo_cur = d1["h"][j], d1["l"][j]
            else:
                hi_cur = max(hi_cur, d1["h"][j])
                lo_cur = min(lo_cur, d1["l"][j])
            pw_hi[j], pw_lo[j] = hi_prev, lo_prev
        self.pw_hi, self.pw_lo = pw_hi, pw_lo
        # F8 step packs (mapped e89/e200/atr) — includes 5m for intraday,
        # which the S-1 capture set does not carry
        from engine.htf import take
        from engine.signals import _prep_tf
        self.f8_packs = {}
        for tf in F8_STEPS[cell.mandate]:
            if tf in self.base.capture:
                self.f8_packs[tf] = self.base.capture[tf]
            else:
                t = _prep_tf(data[tf], cfg["signal"])
                idx = _map_htf(sig.exec_open_ms, t["open_ms"],
                               S1_INTERVAL_MS[tf])
                self.f8_packs[tf] = {"e89": take(t["e89"], idx),
                                     "e200": take(t["e200"], idx),
                                     "atr": take(t["atr"], idx)}


# ═══════════════════════════════════════════════ F2 levels per row bar
def levels_block(ctx: S2Context, j: int, px: float, d: int) -> dict:
    out = {}
    any_headwind = False
    for tf in LEVEL_TFS:
        fr = ctx.native[tf]
        ix = fr["idx"][j]
        atr = fr["atr"][ix] if ix >= 0 else np.nan
        rec = {}
        for side in ("hi", "lo"):
            conf, vals = ctx.lv_piv[tf][side]
            sel = conf <= ix          # confirmed by this exec bar
            vs = vals[sel]
            cs = conf[sel]
            if side == "hi":
                mask = vs > px
            else:
                mask = vs < px
            if not mask.any() or atr != atr or atr <= 0 or ix < 0:
                rec[f"{side}_dist_atr"] = None
                rec[f"{side}_dist_bps"] = None
                rec[f"{side}_age"] = None
                rec[f"{side}_retests"] = None
                rec[f"{side}_fresh"] = None
                continue
            vsm, csm = vs[mask], cs[mask]
            k = int(np.argmin(np.abs(vsm - px)))
            lv, cb = float(vsm[k]), int(csm[k])
            touch = int(((fr["l"][cb + 1:ix + 1] <= lv)
                         & (fr["h"][cb + 1:ix + 1] >= lv)).sum()) \
                if ix > cb else 0
            rec[f"{side}_dist_atr"] = r6(abs(lv - px) / atr)
            rec[f"{side}_dist_bps"] = r6(abs(lv - px) / px * 1e4)
            rec[f"{side}_age"] = ix - cb
            rec[f"{side}_retests"] = touch
            rec[f"{side}_fresh"] = touch == 0
            adverse = (side == "hi") if d == 1 else (side == "lo")
            if adverse and touch == 0 and abs(lv - px) / atr <= HEADWIND_ATR:
                any_headwind = True
        out[tf] = rec
    d1 = ctx.native["1d"]
    ix = d1["idx"][j]
    for name, arr in (("pdh", ctx.pd_hi), ("pdl", ctx.pd_lo),
                      ("pwh", ctx.pw_hi), ("pwl", ctx.pw_lo)):
        v = arr[ix] if ix >= 0 else np.nan
        out[f"{name}_dist_bps"] = r6((v - px) / px * 1e4) if v == v else None
    out["headwind"] = any_headwind
    return out


# ═══════════════════════════════════════════ detectors on native frames
def detect_tf(ctx: S2Context, tf: str) -> dict:
    """Per sweep cell: active masks + event lists in native bars."""
    fr = ctx.native[tf]
    h, l, c, atr = fr["h"], fr["l"], fr["c"], fr["atr"]
    e9, e89 = fr["e9"], fr["e89"]
    nb = len(c)
    out = {"d1": {}, "d2": {}, "d3": {}, "d4": [], "events": []}
    piv_h = _pivots(h, 5, 5, low=False)
    piv_l = _pivots(l, 5, 5, low=True)
    with np.errstate(invalid="ignore"):
        for N, k in D1_GRID:
            hi = pd.Series(h).rolling(N, min_periods=N).max().to_numpy()
            lo = pd.Series(l).rolling(N, min_periods=N).min().to_numpy()
            act = (hi - lo) < k * atr
            act &= ~np.isnan(atr)
            key = f"{N}_{k}"
            out["d1"][key] = {"act": act, "hi": hi, "lo": lo}
            prev = np.concatenate(([False], act[:-1]))
            brk_up = prev & (c > np.concatenate(([np.nan], hi[:-1])))
            brk_dn = prev & (c < np.concatenate(([np.nan], lo[:-1])))
            out["d1"][key]["brk_up"] = brk_up
            out["d1"][key]["brk_dn"] = brk_dn
            for t in np.flatnonzero(brk_up | brk_dn):
                t = int(t)
                up = bool(brk_up[t])
                edge = float(hi[t - 1] if up else lo[t - 1])
                retest = None
                for u in range(t + 1, min(t + 21, nb)):
                    if l[u] <= edge <= h[u]:
                        retest = u
                        break
                out["events"].append({
                    "det": "d1", "cell_key": key, "t": t,
                    "kind": "break_up" if up else "break_down",
                    "edge": r6(edge), "retest_t": retest})
        for x, M in D2_GRID:
            cond = np.abs(e9 - e89) < x * atr
            run = np.zeros(nb, dtype=np.int32)
            for t in range(nb):
                run[t] = run[t - 1] + 1 if cond[t] and t > 0 else \
                    (1 if cond[t] else 0)
            act = run >= M
            key = f"{x}_{M}"
            out["d2"][key] = {"act": act}
            starts = np.flatnonzero(act & ~np.concatenate(([False],
                                                           act[:-1])))
            for t in starts:
                out["events"].append({"det": "d2", "cell_key": key,
                                      "t": int(t), "kind": "start"})
        allc = np.sort(np.concatenate([piv_h[0], piv_l[0]]))
        allv = np.concatenate([piv_h[1], piv_l[1]])[
            np.argsort(np.concatenate([piv_h[0], piv_l[0]]),
                       kind="stable")]
        for P, w in D3_GRID:
            key = f"{P}_{w}"
            act = np.zeros(nb, dtype=bool)
            zt = np.full(nb, np.nan)
            zb = np.full(nb, np.nan)
            k0 = 0
            for t in range(nb):
                if atr[t] != atr[t]:
                    continue
                while k0 < len(allc) and allc[k0] <= t - F4_VOID_BARS:
                    k0 += 1
                kk = np.searchsorted(allc, t, side="right")
                vals = np.sort(allv[k0:kk])
                if len(vals) < P:
                    continue
                width = w * atr[t]
                best = None
                a = 0
                for b2 in range(len(vals)):
                    while vals[b2] - vals[a] > width:
                        a += 1
                    if b2 - a + 1 >= P:
                        span = vals[b2] - vals[a]
                        if best is None or span < best[0]:
                            best = (span, vals[a], vals[b2])
                if best is not None:
                    act[t] = True
                    zb[t], zt[t] = best[1], best[2]
            out["d3"][key] = {"act": act, "top": zt, "bot": zb}
            starts = np.flatnonzero(act & ~np.concatenate(([False],
                                                           act[:-1])))
            for t in starts:
                out["events"].append({"det": "d3", "cell_key": key,
                                      "t": int(t), "kind": "zone_start",
                                      "top": r6(zt[t]), "bot": r6(zb[t])})
        # D4 sweep-reclaim over active D1/D3 edges
        for y, b in D4_GRID:
            key = f"{y}_{b}"
            for src, cells in (("d1", out["d1"]), ("d3", out["d3"])):
                for ck, cd in cells.items():
                    act = cd["act"]
                    top = cd.get("hi", cd.get("top"))
                    bot = cd.get("lo", cd.get("bot"))
                    t = 0
                    while t < nb - 1:
                        if not act[t] or top[t] != top[t]:
                            t += 1
                            continue
                        for edge, up in ((float(top[t]), True),
                                         (float(bot[t]), False)):
                            ext = h[t] - edge if up else edge - l[t]
                            if not (0 < ext <= y * atr[t]):
                                continue
                            for u in range(t + 1, min(t + 1 + b, nb)):
                                inside = c[u] < edge if up else c[u] > edge
                                if inside:
                                    depth = ext / atr[t]
                                    pw = abs(top[t] - bot[t])
                                    out["d4"].append({
                                        "det": "d4", "cell_key": key,
                                        "src": f"{src}_{ck}", "t": int(u),
                                        "sweep_t": int(t),
                                        "kind": "sweep_reclaim",
                                        "dir": -1 if up else 1,
                                        "edge": r6(edge),
                                        "extreme": r6(h[t] if up else l[t]),
                                        "depth_atr": r6(depth),
                                        "pocket_width_atr":
                                            r6(pw / atr[t]) if pw > 0
                                            else None,
                                        "depth_frac":
                                            r6(ext / pw) if pw > 0
                                            else None,
                                        "reclaim_bars": int(u - t)})
                                    break
                        t += 1
    return out


# ═══════════════════════════════════════════════════════ F8 reclaims
def f8_events(ctx: S2Context, in_window) -> list[dict]:
    sig = ctx.sig
    base = ctx.base
    mand = ctx.cell.mandate
    open_by_bar = {}
    for t in base.trades.tranches:
        if not t.exited:
            continue
        for j in range(t.fill_i, t.exit_i):
            open_by_bar.setdefault(j, []).append(t)
    rows = []
    for si, tf in enumerate(F8_STEPS[mand], start=1):
        pack = ctx.f8_packs[tf]
        for ema_name in ("e89", "e200"):
            line = pack[ema_name]
            state = 0     # 1 = penetrated (adverse side), per open campaign
            pen_bar = None
            pen_depth = 0.0
            for j in sorted(open_by_bar):
                trs = open_by_bar[j]
                d = trs[0].dir
                v = line[j]
                if v != v:
                    continue
                atr_tf = pack["atr"][j]
                adverse = (sig.l[j] - v) * d < 0 if d == 1 else \
                    (sig.h[j] - v) * d < 0
                beyond_close = (sig.c[j] - v) * d > 0
                if state == 0 and adverse:
                    state, pen_bar = 1, j
                    pen_depth = abs((sig.l[j] if d == 1 else sig.h[j]) - v)
                elif state == 1:
                    pen_depth = max(pen_depth, abs(
                        (sig.l[j] if d == 1 else sig.h[j]) - v))
                    if beyond_close:
                        rec = {"family": "f8_reclaim", "step": -si,
                               "tf": tf, "ema": ema_name,
                               "i": pen_bar,
                               "ts_open": iso(int(sig.exec_open_ms[pen_bar])),
                               "reclaim_bars": j - pen_bar,
                               "reclaimed_b3": j - pen_bar <= 3,
                               "reclaimed_b5": j - pen_bar <= 5,
                               "depth_tf_atr": r6(pen_depth / atr_tf)
                               if atr_tf == atr_tf and atr_tf > 0 else None,
                               "dir": d,
                               "rem_r_mean": r6(float(np.mean(
                                   [(t.exit_px - sig.c[j]) * d /
                                    ((t.fill_px - t.stop_at_entry) * d)
                                    for t in trs]))),
                               }
                        if in_window(pen_bar):
                            rows.append(rec)
                        state, pen_bar, pen_depth = 0, None, 0.0
                # unreclaimed: position closed or campaign ends with state=1
            if state == 1 and pen_bar is not None and in_window(pen_bar):
                trs = open_by_bar[max(k for k in open_by_bar
                                      if k >= pen_bar)]
                d = trs[0].dir
                rows.append({"family": "f8_reclaim", "step": -si, "tf": tf,
                             "ema": ema_name, "i": pen_bar,
                             "ts_open": iso(int(sig.exec_open_ms[pen_bar])),
                             "reclaim_bars": None, "reclaimed_b3": False,
                             "reclaimed_b5": False,
                             "depth_tf_atr": None, "dir": d,
                             "rem_r_mean": r6(float(np.mean(
                                 [(t.exit_px - sig.c[pen_bar]) * d /
                                  ((t.fill_px - t.stop_at_entry) * d)
                                  for t in trs])))})
    return rows


# ═══════════════════════════════════════════════ F1 reject counterfactuals
def f1_rows(ctx: S2Context, in_window) -> list[dict]:
    sig = ctx.sig
    n = ctx.n
    rows = []
    for ev in sig.events:
        if ev.evt != "REJECT" or ev.subkey != "prime" or \
                ev.reject_reason != "no_zone":
            continue
        j = ev.i
        if not in_window(j) or j + 1 >= n:
            continue
        d = ev.dir
        atr = sig.atr_x[j]
        rec = {"family": "f1_reject", "i": j,
               "ts_open": iso(int(sig.exec_open_ms[j])), "dir": d}
        if atr != atr or atr <= 0:
            rows.append(rec | {"stop": None, "outcome_r": None,
                               "terminal": "no_atr",
                               **{f"fwd_{k}_r": None for k in HORIZONS}})
            continue
        stop = (sig.l[j] - 0.5 * atr) if d == 1 else (sig.h[j] + 0.5 * atr)
        entry = float(sig.o[j + 1])
        unit = (entry - stop) * d
        if unit <= 0:
            rows.append(rec | {"stop": r6(stop), "outcome_r": None,
                               "terminal": "bad_unit",
                               **{f"fwd_{k}_r": None for k in HORIZONS}})
            continue
        outcome, terminal = None, None
        end = min(j + 1 + 100, n)
        for u in range(j + 1, end):
            if u > j + 1 and (sig.o[u] - stop) * d <= 0:
                outcome, terminal = (sig.o[u] - entry) * d / unit, "gap"
                break
            if (sig.l[u] <= stop) if d == 1 else (sig.h[u] >= stop):
                outcome, terminal = -1.0, "stop"
                break
            if (((sig.h[u] if d == 1 else sig.l[u]) - entry) * d / unit
                    >= CAP_R):
                outcome, terminal = CAP_R, "cap10"
                break
        else:
            if end == n:
                terminal = "data_end"
            else:
                outcome, terminal = \
                    (sig.c[end - 1] - entry) * d / unit, "horizon"
        fwd = {}
        for k in HORIZONS:
            fwd[f"fwd_{k}_r"] = (r6((sig.c[j + k] - entry) * d / unit)
                                 if j + k < n else None)
        rows.append(rec | {"stop": r6(stop),
                           "stop_dist_bps": r6(unit / entry * 1e4),
                           "outcome_r": r6(outcome), "terminal": terminal,
                           **fwd})
    return rows


# ═══════════════════════════════════════════════ F3 level-event sidecar
def f3_rows(ctx: S2Context, in_window) -> list[dict]:
    sig = ctx.sig
    rows = []
    for tf in LEVEL_TFS:
        fr = ctx.native[tf]
        nb = len(fr["ms"])
        for side in ("hi", "lo"):
            conf, vals = ctx.lv_piv[tf][side]
            for cb, lv in zip(conf, vals):
                cb = int(cb)
                lv = float(lv)
                for t in range(cb + 1, min(cb + 1 + 400, nb)):
                    touched = fr["l"][t] <= lv <= fr["h"][t]
                    through = (fr["c"][t] > lv) if side == "hi" else \
                        (fr["c"][t] < lv)
                    if not touched:
                        continue
                    vb = int(fr["vis"][t]) if t < len(fr["vis"]) else -1
                    if vb < 0 or not in_window(vb):
                        if through:
                            break
                        continue
                    rows.append({"family": "f3_level", "tf": tf,
                                 "side": side, "level": r6(lv),
                                 "kind": "close_through" if through
                                 else "retest",
                                 "ts_open": iso(int(fr["ms"][t])),
                                 **_fwd_bps(sig, vb, HORIZONS)})
                    if through:
                        break
    return rows


# ══════════════════════════════════════ F4 structure-anchored stop
def f4_block(ctx: S2Context, tr, camp_end) -> dict:
    sig = ctx.sig
    d = tr.dir
    out = {}
    unit0 = (tr.fill_px - tr.stop_at_entry) * d
    for tfv in F4_TFS:
        if tfv == "exec":
            conf, vals = ctx.base.pivots[(5, 5, d)]
            cutoff = tr.fill_i - F4_VOID_BARS
            sel = (conf <= tr.fill_i) & (conf > cutoff)
            vsel = vals[sel]
        else:
            fr = ctx.native[tfv]
            ixf = fr["idx"][tr.fill_i]
            if d == 1:
                cN, vN = _pivots(fr["l"], 5, 5, low=True)
            else:
                cN, vN = _pivots(fr["h"], 5, 5, low=False)
            sel = (cN <= ixf) & (cN > ixf - F4_VOID_BARS)
            vsel = vN[sel]
        beyond = vsel[(vsel - tr.fill_px) * d < 0] if len(vsel) else vsel
        if len(beyond) == 0:
            out[tfv] = {"void": True}
            continue
        pv = float(beyond[(np.abs(beyond - tr.fill_px)).argmin()])
        atr_sig = sig.atr_x[tr.signal_i]
        stop = pv - d * 0.5 * atr_sig
        unit = (tr.fill_px - stop) * d
        if unit <= 0 or atr_sig != atr_sig:
            out[tfv] = {"void": True}
            continue
        const = np.full(camp_end - tr.fill_i + 1, stop)
        sim = sim_corrected(sig, d, tr.fill_i, camp_end, stop, const)
        if sim is None:
            out[tfv] = {"void": True}
            continue
        px, bar, kind = sim
        fav = sig.h if d == 1 else sig.l
        seg = fav[tr.fill_i:bar + 1]
        peak = (max(float(seg.max()), tr.fill_px) if d == 1
                else min(float(seg.min()), tr.fill_px))
        mfe_struct = (peak - tr.fill_px) * d / unit
        out[tfv] = {
            "void": False, "stop": r6(stop),
            "stop_dist_bps": r6(unit / tr.fill_px * 1e4),
            "exit_r_struct": r6((px - tr.fill_px) * d / unit),
            "exit_bps": r6((px - tr.fill_px) * d / tr.fill_px * 1e4),
            "exit_kind": kind, "exit_i_offset": bar - tr.fill_i,
            "mfe_struct_r": r6(mfe_struct),
            "reach_1r_struct": bool(mfe_struct >= 1.0),
            "reach_1r_orig": bool((peak - tr.fill_px) * d / unit0 >= 1.0),
        }
    return out


# ═══════════════════════════════════════════════════════ top level
def compute_s2(cell, cfg, sig, trades, data, resampled_dir,
               in_window) -> dict:
    ctx = S2Context(cell, cfg, sig, trades, data, resampled_dir)
    base = ctx.base
    p = cfg["signal"]

    det = {tf: detect_tf(ctx, tf) for tf in ALL_DET_TFS}

    def entry_det_flags(j):
        out = {}
        for tf in DET_TFS:
            fr = ctx.native[tf]
            ix = fr["idx"][j]
            if ix < 0:
                out[tf] = None
                continue
            dd = det[tf]
            d1 = {k: bool(v["act"][ix]) for k, v in dd["d1"].items()}
            tight = None
            for k, v in dd["d1"].items():
                if v["act"][ix] and v["hi"][ix] == v["hi"][ix]:
                    wdt = v["hi"][ix] - v["lo"][ix]
                    if tight is None or wdt < tight[0]:
                        atr = fr["atr"][ix]
                        tight = (wdt,
                                 r6((v["hi"][ix] - sig.c[j]) / atr),
                                 r6((sig.c[j] - v["lo"][ix]) / atr))
            br = False
            for e in dd["events"]:
                if e["det"] == "d1" and e.get("retest_t") is not None \
                        and e["retest_t"] <= ix <= e["retest_t"] + 20:
                    br = True
                    break
            out[tf] = {"d1": d1, "in_range": any(d1.values()),
                       "dist_hi_atr": tight[1] if tight else None,
                       "dist_lo_atr": tight[2] if tight else None,
                       "d2": {k: bool(v["act"][ix])
                              for k, v in dd["d2"].items()},
                       "d3": {k: bool(v["act"][ix])
                              for k, v in dd["d3"].items()},
                       "break_retest": br}
        return out

    fill_s2, exit_s2, sig_s2 = {}, {}, {}
    for camp, trs in sorted(base.camp_tranches.items()):
        camp_end = base.camp_end[camp]
        for tr in trs:
            fill_s2[tr.tranche_id] = {
                "levels": levels_block(ctx, tr.fill_i, tr.fill_px, tr.dir),
                "det": entry_det_flags(tr.fill_i),
            }
            if not tr.exited or camp_end is None:
                continue
            d = tr.dir
            entry_stop = tr.stop_at_entry
            real = base.real_stop(d)
            native = real[tr.fill_i:camp_end + 1].copy()
            unit0 = (tr.fill_px - entry_stop) * d
            tl = {}
            for cid in TL_CANDS:
                path, eng = candidate_path(base, tr, cid, camp_end)
                leg = legacy_exit(base, tr, path, camp_end)
                fold = sim_corrected(sig, d, tr.fill_i, camp_end,
                                     entry_stop, path)
                two = two_line_walk(sig, d, tr.fill_i, camp_end,
                                    entry_stop, native, path)
                rec = {}
                for tag, sm in (("legacy", leg), ("fold", fold)):
                    if sm is None:
                        rec[f"{tag}_exit_r"] = None
                        rec[f"{tag}_off"] = None
                        rec[f"{tag}_kind"] = None
                    else:
                        px, bar, kind = sm[0], sm[1], sm[2]
                        rec[f"{tag}_exit_r"] = r6((px - tr.fill_px) * d
                                                  / unit0)
                        rec[f"{tag}_off"] = bar - tr.fill_i
                        rec[f"{tag}_kind"] = kind
                if two is None:
                    rec.update({"two_exit_r": None, "two_off": None,
                                "two_kind": None, "two_src": None})
                else:
                    px, bar, kind, src = two
                    rec.update({"two_exit_r": r6((px - tr.fill_px) * d
                                                 / unit0),
                                "two_off": bar - tr.fill_i,
                                "two_kind": kind, "two_src": src})
                rec["engaged_off"] = (eng - tr.fill_i) if eng is not None \
                    else None
                tl[cid] = rec
            # baseline shakeout (S-1 noise def applied to the real exit)
            shake = False
            if tr.exit_reason in ("stop", "stop_gap"):
                end = tr.exit_i + 20
                if end < ctx.n:
                    fav = sig.h if d == 1 else sig.l
                    seg = fav[tr.exit_i + 1:end + 1]
                    best = seg.max() if d == 1 else seg.min()
                    shake = bool((best - tr.exit_px) * d / unit0 >= 1.0)
            exit_s2[tr.tranche_id] = {
                "tl": tl,
                "f4": f4_block(ctx, tr, camp_end),
                "baseline_shakeout": shake,
                "zero_advance": None,   # filled by reader from s1 join
            }

    # signal-row s2: levels + FH-1 true depth
    z1p, z2p, z3p = p["z1_prox"], p["z2_prox"], p["z3_prox"]
    for ev in sig.events:
        if ev.evt not in ("PRIME", "CONFIRM", "V", "TAG"):
            continue
        j = ev.i
        key = (j, ev.evt, ev.dir, ev.subkey)
        blk = {"levels": levels_block(ctx, j, float(sig.c[j]), ev.dir)}
        zone = ev.zone if ev.evt != "TAG" else ev.subkey
        if zone in ("Z1", "Z2", "Z3"):
            ga = base.gATR[j]
            if ga == ga and ga > 0:
                if zone == "Z1":
                    top, bot = base.gE9[j] + z1p * ga, base.gE9[j] - z1p * ga
                elif zone == "Z2":
                    top = base.gE89[j] + z2p * ga
                    bot = base.gE89[j] - z2p * ga
                else:
                    top = base.gBandTop[j] + z3p * ga
                    bot = base.gBandBot[j] - z3p * ga
                ext = sig.l[j] if ev.dir == 1 else sig.h[j]
                near = top if ev.dir == 1 else bot
                blk["fh1"] = {"band_top": r6(top), "band_bot": r6(bot),
                              "depth_gov_atr": r6((near - ext) * ev.dir
                                                  / ga)}
        sig_s2[key] = blk

    sidecar = f1_rows(ctx, in_window)
    sidecar += f3_rows(ctx, in_window)
    for tf in ALL_DET_TFS:
        fr = ctx.native[tf]
        for e in det[tf]["events"] + det[tf]["d4"]:
            t = e["t"]
            vb = int(fr["vis"][t]) if t < len(fr["vis"]) else -1
            if vb < 0 or not in_window(vb):
                continue
            row = {"family": f"det_{e['det']}", "tf": tf,
                   "ts_open": iso(int(fr["ms"][t])),
                   **{k: v for k, v in e.items() if k not in ("det", "t")},
                   **_fwd_bps(sig, vb, HORIZONS)}
            sidecar.append(row)
    sidecar += f8_events(ctx, in_window)
    sidecar.sort(key=lambda r: (r["ts_open"], r["family"],
                                json.dumps({k: r.get(k) for k in
                                            ("tf", "side", "kind",
                                             "cell_key", "src", "step",
                                             "ema", "dir")},
                                           sort_keys=True, default=str)))
    def clean(x):
        if isinstance(x, dict):
            return {k: clean(v) for k, v in x.items()}
        if isinstance(x, (list, tuple)):
            return [clean(v) for v in x]
        if isinstance(x, np.integer):
            return int(x)
        if isinstance(x, np.floating):
            return None if x != x else float(x)
        if isinstance(x, np.bool_):
            return bool(x)
        return x

    return {"fill_s2": clean(fill_s2), "exit_s2": clean(exit_s2),
            "sig_s2": clean(sig_s2), "sidecar": clean(sidecar)}
