"""S-1 instrumentation (engine 1.0.9) — measure-only enrichment + sidecar.

Everything in this module OBSERVES a finished replay (SignalResult +
TradeResult) and computes counterfactuals; nothing here can reach the
trading path. Emission neutrality is structural: replay.py attaches the
returned objects to rows it was already emitting and writes sidecar rows to
a separate stream — this module never sees, filters, or orders main-journal
rows.

All a-priori mechanizations are pinned in the S-1 ledger pre-registration
(2026-07-18): candidate stop semantics (series[j-1] governs bar j; one-way
never-loosen; phase-1 = live baseline series for pivot/EMA/hybrid families,
entry stop for chandelier/R-ladder/giveback; post-engagement no baseline
floor; engagement seeds at the standing phase-1 stop), V-shadow notches,
zone replication validated bar-exactly against sig.active_zone AND sig.dir,
dead-gate conventions, sidecar horizons.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from engine import data as dl
from engine import indicators as ind
from engine.cells import INTERVAL_MS, Cell
from engine.htf import map_htf_to_exec, take, take_bool
from engine.journal import iso
from engine.shadows import _campaign_span
from engine.signals import SignalResult, _prep_tf
from engine.trading import TradeResult

BIG = 100_000

# ── pinned grids (F-GRID audits these) ────────────────────────────────────
CHANDELIER_K = [1.5, 2.0, 3.0]
PIVOT_GRID = [(3, 3, 2), (3, 3, 3), (5, 5, 2), (5, 5, 3)]
EMA_GRID = [("89", "1h"), ("89", "gov"), ("200", "exec"), ("200", "gov")]
EMA_B = [0.0, 0.5]
GIVEBACK_GRID = [(1.0, 0.30), (1.0, 0.40), (1.0, 0.50),
                 (2.0, 0.30), (2.0, 0.40), (2.0, 0.50)]

RATCHET_IDS = (
    [f"chand_k{k}" for k in CHANDELIER_K]
    + [f"pivot_{l}_{r}_n{n}" for l, r, n in PIVOT_GRID]
    + [f"ema{p}_{tf}_b{b}" for p, tf in EMA_GRID for b in EMA_B]
    + ["rladder"]
    + [f"gb_t{int(t)}_g{int(g * 100)}" for t, g in GIVEBACK_GRID]
    + ["hyb_chand_k2", "hyb_pivot_5_5_n2"]
)
assert len(RATCHET_IDS) == 24

DEADGATE_HOURS = [12, 24, 48]
ANCHOR_Y = [0.5, 0.75, 1.0, 1.25]
BPS_M = [0.5, 1.0, 2.0]
Z3P = [0.25, 0.35, 0.50]
ASYM = [(0.25, 0.5), (0.25, 0.75), (0.25, 1.0),
        (0.5, 0.5), (0.5, 0.75), (0.5, 1.0)]
V_VARIANTS = [
    ("clx_3.0", {"climax_mult": 3.0}), ("clx_2.5", {"climax_mult": 2.5}),
    ("ext_0.75", {"cap_ext_atr": 0.75}), ("ext_0.5", {"cap_ext_atr": 0.5}),
    ("win_15", {"cap_window": 15}), ("win_20", {"cap_window": 20}),
    ("vol_1.1", {"cap_vol_conf": 1.1}), ("vol_1.0", {"cap_vol_conf": 1.0}),
    ("all_loose", {"climax_mult": 2.5, "cap_ext_atr": 0.5,
                   "cap_window": 20, "cap_vol_conf": 1.0}),
]
ADD_TRIGGERS = ["brk20", "brk55", "pull_e9", "ext_2atr", "recross"]
CAPTURE_TFS = ["15m", "30m", "1h", "4h", "12h", "1d"]
# capture-set intervals: the frozen grid map (cells.py) plus the two locally
# resampled TFs — kept here so no ratified module changes for S-1
S1_INTERVAL_MS = dict(INTERVAL_MS, **{"30m": 1_800_000, "1d": 86_400_000})


def _map_htf(exec_open_ms: np.ndarray, htf_open_ms: np.ndarray,
             step_ms: int) -> np.ndarray:
    """Confirmed-HTF visibility mapping (htf.map_htf_to_exec semantics) with
    an explicit interval, so 30m/1d work without touching the frozen map."""
    idx = np.searchsorted(htf_open_ms + step_ms, exec_open_ms,
                          side="right") - 1
    return idx
NOISE_HORIZON = 20          # exec bars; resumption >= +1R per-unit
FWD_BARS = [5, 20, 100]     # V-shadow forward returns
V_CAP_R = 10.0
V_CAP_BARS = 1000
F1_CAP_R = 10.0
GATE_TOL = 1e-9


def r6(x):
    if x is None:
        return None
    x = float(x)
    if x != x:
        return None
    return round(x, 6) + 0.0


def _pivots(x: np.ndarray, L: int, R: int, low: bool):
    """Strict (L,R) pivot extremes, vectorized; (confirm_bars, values)."""
    s = pd.Series(x)
    left = (s.rolling(L, min_periods=L).min() if low
            else s.rolling(L, min_periods=L).max()).shift(1).to_numpy()
    right = (s.rolling(R, min_periods=R).min() if low
             else s.rolling(R, min_periods=R).max()).shift(-R).to_numpy()
    with np.errstate(invalid="ignore"):
        piv = (x < left) & (x < right) if low else (x > left) & (x > right)
    p = np.flatnonzero(piv)
    return p + R, x[p]


def _edge(mapped_flag: np.ndarray, idx: np.ndarray) -> np.ndarray:
    """HTF event flag stays visible all period; edge = first exec bar the
    mapped HTF index advanced onto a flagged bar."""
    prev_idx = np.concatenate(([-2], idx[:-1]))
    return mapped_flag & (idx != prev_idx)


# ══════════════════════════════════════════════════════════════ context
class S1Context:
    """Per-cell precomputation shared by every family."""

    def __init__(self, cell: Cell, cfg: dict, sig: SignalResult,
                 trades: TradeResult, data: dict, resampled_dir: Path):
        p = cfg["signal"]
        self.cell = cell
        self.cfg = cfg
        self.sig = sig
        self.trades = trades
        self.n = len(sig.c)
        self.step = INTERVAL_MS[cell.tf_exec]

        gov = _prep_tf(data[cell.tf_gov], p)
        gidx = map_htf_to_exec(sig.exec_open_ms, gov["open_ms"], cell.tf_gov)
        self.gE9 = take(gov["e9"], gidx)
        self.gE89 = take(gov["e89"], gidx)
        self.gE200 = take(gov["e200"], gidx)
        self.gATR = take(gov["atr"], gidx)
        self.gS2B = take_bool(gov["s2bu"], gidx)
        self.gS2S = take_bool(gov["s2be"], gidx)
        self.gBullX = take_bool(gov["bx"], gidx)
        self.gBearX = take_bool(gov["sx"], gidx)
        self.gBandTop = np.maximum(self.gE89, self.gE200)
        self.gBandBot = np.minimum(self.gE89, self.gE200)
        self.vol_ma = ind.sma(sig.v, p["vol_len"])

        # capture set: exec + {15m, 30m, 1h, 4h, 12h, 1d}
        self.capture = {"exec": {
            "e9": sig.e9x, "e89": sig.e89x, "e200": sig.e200x,
            "atr": sig.atr_x,
            "s2bu": sig.e89x > sig.e200x, "s2be": sig.e89x < sig.e200x,
            "bx": ind.crossover(sig.e9x, sig.e89x),
            "sx": ind.crossunder(sig.e9x, sig.e89x),
            "bx2": ind.crossover(sig.e89x, sig.e200x),
            "sx2": ind.crossunder(sig.e89x, sig.e200x),
        }}
        lo = int(sig.exec_open_ms[0])
        hi = int(sig.exec_open_ms[-1]) + self.step
        for tf in CAPTURE_TFS:
            step_tf = S1_INTERVAL_MS[tf]
            if tf in data:
                df = data[tf]
            elif tf in ("30m", "1d"):
                df = pd.read_parquet(resampled_dir /
                                     f"{cell.symbol}_{tf}.parquet")
                df = df[(df["open_time"] >= lo - step_tf * 300)
                        & (df["open_time"] <= hi)].reset_index(drop=True)
            else:                        # 15m for swing/intraday cells
                df = dl.load_klines(cell.symbol, tf, lo - step_tf * 300, hi)
            t = _prep_tf(df, p)
            idx = _map_htf(sig.exec_open_ms, t["open_ms"], step_tf)
            self.capture[tf] = {
                "e9": take(t["e9"], idx), "e89": take(t["e89"], idx),
                "e200": take(t["e200"], idx), "atr": take(t["atr"], idx),
                "s2bu": take_bool(t["s2bu"], idx),
                "s2be": take_bool(t["s2be"], idx),
                "bx": _edge(take_bool(t["bx"], idx), idx),
                "sx": _edge(take_bool(t["sx"], idx), idx),
                "bx2": _edge(take_bool(
                    ind.crossover(t["e89"], t["e200"]), idx), idx),
                "sx2": _edge(take_bool(
                    ind.crossunder(t["e89"], t["e200"]), idx), idx),
            }

        self.ema_lines = {
            ("89", "1h"): self.capture["1h"]["e89"],
            ("89", "gov"): sig.g_e89,
            ("200", "exec"): sig.e200x,
            ("200", "gov"): self.gE200,
        }

        self.pivots = {}
        for L, R in {(l, r) for l, r, _ in PIVOT_GRID}:
            self.pivots[(L, R, 1)] = _pivots(sig.l, L, R, low=True)
            self.pivots[(L, R, -1)] = _pivots(sig.h, L, R, low=False)

        self.brk = {}
        for N in (20, 55):
            hi_roll = ind.rolling_max(sig.h, N)
            lo_roll = ind.rolling_min(sig.l, N)
            self.brk[N] = (np.concatenate(([np.nan], hi_roll[:-1])),
                           np.concatenate(([np.nan], lo_roll[:-1])))

        self.camp_tranches: dict[int, list] = {}
        for tr in trades.tranches:
            self.camp_tranches.setdefault(tr.campaign, []).append(tr)
        for c in self.camp_tranches:
            self.camp_tranches[c].sort(key=lambda t: (t.fill_i, t.tranche_id))
        self.camp_end: dict[int, int | None] = {}
        for c, trs in self.camp_tranches.items():
            self.camp_end[c] = _campaign_span(sig, trs[0].dir,
                                              trs[0].fill_i)[1]

        self.add_signals: dict[int, list[int]] = {1: [], -1: []}
        for ev in sig.events:
            if (ev.evt == "PRIME" and ev.is_add) or \
                    (ev.evt == "CONFIRM" and ev.is_add):
                self.add_signals[ev.dir].append(ev.i)

        openers = sorted(((trs[0].fill_i, c) for c, trs in
                          self.camp_tranches.items()))
        self.attempt: dict[int, int] = {}
        self.first_opener: dict[int, object] = {}
        run_first, prev_dir, att = None, None, 0
        for _, c in openers:
            tr0 = self.camp_tranches[c][0]
            if tr0.dir != prev_dir:
                run_first, att, prev_dir = tr0, 0, tr0.dir
            att += 1
            self.attempt[c] = att
            self.first_opener[c] = run_first

    def real_stop(self, d: int) -> np.ndarray:
        return self.sig.stop_long if d == 1 else self.sig.stop_short


# ══════════════════════════════════════════════════ candidate stop paths
def candidate_path(ctx: S1Context, tr, cand_id: str, last: int):
    """(series over [fill_i, last], engagement bar or None). series[j-fill]
    is the value confirmed at bar j (governs bar j+1)."""
    sig, d = ctx.sig, tr.dir
    f = tr.fill_i
    out = np.empty(last - f + 1)
    real = ctx.real_stop(d)
    atr = sig.atr_x
    fav = sig.h if d == 1 else sig.l
    entry_stop = tr.stop_at_entry
    unit = (tr.fill_px - entry_stop) * d

    def tighten(prev, cand):
        if cand != cand:
            return prev
        if prev != prev:
            return cand
        return max(prev, cand) if d == 1 else min(prev, cand)

    eng = None
    s = entry_stop
    if cand_id.startswith("chand_"):
        k = float(cand_id.split("k")[1])
        peak = tr.fill_px
        for j in range(f, last + 1):
            peak = max(peak, fav[j]) if d == 1 else min(peak, fav[j])
            cand = peak - d * k * atr[j] if atr[j] == atr[j] else np.nan
            s2 = tighten(s, cand)
            if eng is None and (s2 - s) * d > GATE_TOL:
                eng = j
            s = s2
            out[j - f] = s
    elif cand_id == "rladder":
        peak = tr.fill_px
        for j in range(f, last + 1):
            peak = max(peak, fav[j]) if d == 1 else min(peak, fav[j])
            rung = int((peak - tr.fill_px) * d / unit) if unit > 0 else 0
            if rung >= 1:
                if eng is None:
                    eng = j
                s = tighten(s, tr.fill_px + d * (rung - 1) * unit)
            out[j - f] = s
    elif cand_id.startswith("gb_"):
        t_arm = float(cand_id.split("_t")[1].split("_")[0])
        g = int(cand_id.split("_g")[1]) / 100.0
        peak = tr.fill_px
        for j in range(f, last + 1):
            peak = max(peak, fav[j]) if d == 1 else min(peak, fav[j])
            peak_r = (peak - tr.fill_px) * d / unit if unit > 0 else 0.0
            if peak_r >= t_arm:
                if eng is None:
                    eng = j
                s = tighten(s, tr.fill_px + d * (1.0 - g) * peak_r * unit)
            out[j - f] = s
    elif cand_id.startswith("ema"):
        head, tf, btag = cand_id.split("_")
        line = ctx.ema_lines[(head[3:], tf)]
        b = float(btag[1:])
        c = sig.c
        for j in range(f, last + 1):
            if eng is None:
                s = tighten(s, real[j])
                if line[j] == line[j] and (c[j] - line[j]) * d > 0:
                    eng = j
            if eng is not None:
                lv = (line[j] - d * b * atr[j]
                      if line[j] == line[j] and atr[j] == atr[j] else np.nan)
                s = tighten(s, lv)
            out[j - f] = s
    elif cand_id.startswith("pivot_") or cand_id == "hyb_pivot_5_5_n2":
        if cand_id.startswith("pivot_"):
            _, L, R, ntag = cand_id.split("_")
            L, R, N = int(L), int(R), int(ntag[1:])
            need_mfe = None
        else:
            L, R, N = 5, 5, 2
            need_mfe = 1.0
        conf, vals = ctx.pivots[(L, R, d)]
        k0 = int(np.searchsorted(conf, f, side="right"))
        k = k0
        peak = tr.fill_px
        armed = need_mfe is None
        for j in range(f, last + 1):
            peak = max(peak, fav[j]) if d == 1 else min(peak, fav[j])
            if not armed and unit > 0 and \
                    (peak - tr.fill_px) * d / unit >= need_mfe:
                armed = True
            while k < len(conf) and conf[k] <= j:
                k += 1
            if eng is None:
                s = tighten(s, real[j])
                if armed and k > k0:
                    eng = j
            if eng is not None and k > k0:
                pick = max(k0, k - N)     # Nth-most-recent, else earliest
                a = atr[conf[k - 1]]
                lv = vals[pick] - d * 0.5 * a if a == a else np.nan
                s = tighten(s, lv)
            out[j - f] = s
    elif cand_id == "hyb_chand_k2":
        peak = tr.fill_px
        for j in range(f, last + 1):
            peak = max(peak, fav[j]) if d == 1 else min(peak, fav[j])
            if eng is None:
                s = tighten(s, real[j])
                if unit > 0 and (peak - tr.fill_px) * d / unit >= 1.0:
                    eng = j
            if eng is not None:
                s = tighten(s, peak - d * 2.0 * atr[j]
                            if atr[j] == atr[j] else np.nan)
            out[j - f] = s
    else:
        raise KeyError(cand_id)
    return out, eng


def simulate_exit(ctx: S1Context, tr, path: np.ndarray, camp_end: int):
    """(exit_px, exit_bar, kind) under a candidate path; kind 'stop' |
    'flatten'; None if the data ends first (cannot happen on emitted rows)."""
    sig, d, f = ctx.sig, tr.dir, tr.fill_i
    for j in range(f + 1, camp_end + 2):
        if j >= ctx.n:
            return None
        s = path[j - 1 - f]
        if s == s:
            if (sig.o[j] - s) * d <= 0:
                return float(sig.o[j]), j, "stop"
            if (sig.l[j] <= s) if d == 1 else (sig.h[j] >= s):
                return float(s), j, "stop"
        if j == camp_end + 1:
            return float(sig.o[j]), j, "flatten"
    return None


def _noise_stopout(ctx: S1Context, tr, exit_px: float, exit_bar: int,
                   kind: str):
    if kind != "stop":
        return False
    d = tr.dir
    unit = (tr.fill_px - tr.stop_at_entry) * d
    end = exit_bar + NOISE_HORIZON
    if end >= ctx.n:
        return None                      # F-NULL: edge-unresolvable
    fav = ctx.sig.h if d == 1 else ctx.sig.l
    seg = fav[exit_bar + 1:end + 1]
    best = seg.max() if d == 1 else seg.min()
    return bool((best - exit_px) * d / unit >= 1.0)


# ═══════════════════════════════════════════════════════ per-tranche blocks
def advance_block(ctx: S1Context, tr, mfe_bar: int) -> dict:
    d = tr.dir
    real = ctx.real_stop(d)
    unit = (tr.fill_px - tr.stop_at_entry) * d
    lo = max(tr.fill_i - 1, 0)
    hi = tr.exit_i - 1
    n_adv = 0
    adv_before_mfe = 0
    first = None
    prev = None
    last_valid = tr.stop_at_entry
    for m in range(lo, hi + 1):
        v = real[m]
        if v != v:
            continue
        if prev is not None and (v - prev) * d > GATE_TOL:
            n_adv += 1
            if first is None:
                first = m
            if m < mfe_bar:
                adv_before_mfe += 1
        prev = v
        last_valid = v
    return {
        "n_stop_advances": n_adv,
        "advances_before_mfe": adv_before_mfe,
        "bars_to_first_advance": (first - tr.fill_i)
        if first is not None else None,
        "stop_moved_r": r6((last_valid - tr.stop_at_entry) * d / unit),
        "mfe_bar_offset": mfe_bar - tr.fill_i,
    }


def _mfe_bar(ctx: S1Context, tr) -> int:
    sig, d = ctx.sig, tr.dir
    fav = sig.h if d == 1 else sig.l
    peak = tr.fill_px
    for j in range(tr.fill_i, tr.exit_i + 1):
        peak = max(peak, fav[j]) if d == 1 else min(peak, fav[j])
        if peak == tr.peak:
            return j
    return tr.exit_i


def mtf_block(ctx: S1Context, tr, mfe_bar: int) -> dict:
    sig, d = ctx.sig, tr.dir
    marks = {"entry": tr.fill_i, "mfe": mfe_bar, "exit": tr.exit_i}
    life = slice(tr.fill_i, tr.exit_i + 1)
    c_life = sig.c[life]
    out = {}
    for tf, pack in ctx.capture.items():
        rec = {}
        for mk, j in marks.items():
            a = pack["atr"][j]
            for el in ("e9", "e89", "e200"):
                v = pack[el][j]
                rec[f"{mk}_d{el[1:]}"] = (r6((sig.c[j] - v) / a)
                                          if a == a and a > 0 and v == v
                                          else None)
        s2 = pack["s2bu"] if d == 1 else pack["s2be"]
        rec["s2_aligned_entry"] = bool(s2[tr.fill_i])
        seg = s2[life]
        rec["s2_flip_during"] = bool(seg.any() and not seg.all())
        e200 = pack["e200"][life]
        ok = ~np.isnan(e200)
        rec["frac_beyond_e200"] = (r6(float(((c_life[ok] - e200[ok]) * d > 0)
                                            .mean())) if ok.any() else None)
        out[tf] = rec
    return out


def entryflags_block(ctx: S1Context, tr) -> dict:
    atr = ctx.sig.atr_x[tr.signal_i]
    dist = abs(tr.fill_px - tr.stop_at_entry)
    out = {}
    for y in ANCHOR_Y:
        tag = f"{y}".replace(".", "")
        if atr != atr or atr <= 0:
            out[f"rej_struct_{tag}"] = None
            out[f"rej_pure_{tag}"] = None
        else:
            out[f"rej_struct_{tag}"] = bool(dist - 0.5 * atr < y * atr)
            out[f"rej_pure_{tag}"] = bool(dist < y * atr)
    dist_bps = dist / tr.fill_px * 1e4
    cost_bps = 2.0 * (ctx.cfg["trading"]["fee_bps_side"]
                      + ctx.cell.slippage_bps)
    for m in BPS_M:
        out[f"rej_bps_{f'{m}'.replace('.', '')}"] = \
            bool(dist_bps < m * cost_bps)
    out["stop_dist_bps"] = r6(dist_bps)
    out["roundtrip_cost_bps"] = r6(cost_bps)
    return out


def cluster_block(ctx: S1Context, tr) -> dict | None:
    camp = tr.campaign
    if ctx.camp_tranches[camp][0] is not tr:
        return None
    att = ctx.attempt[camp]
    ref = ctx.first_opener[camp]
    if att == 1 or ref is None:
        return {"attempt": att, "dist_gov_atr": None, "in_cluster_025": None,
                "in_cluster_05": None, "in_cluster_10": None}
    a = ctx.sig.g_atr[ref.signal_i]
    if a != a or a <= 0:
        return {"attempt": att, "dist_gov_atr": None, "in_cluster_025": None,
                "in_cluster_05": None, "in_cluster_10": None}
    dist = abs(tr.fill_px - ref.fill_px) / a
    return {"attempt": att, "dist_gov_atr": r6(dist),
            "in_cluster_025": bool(dist <= 0.25),
            "in_cluster_05": bool(dist <= 0.5),
            "in_cluster_10": bool(dist <= 1.0)}


def deadgate_block(ctx: S1Context, camp: int) -> dict:
    trs = ctx.camp_tranches[camp]
    r1 = trs[0]
    d = r1.dir
    real = ctx.real_stop(d)
    unresolved = any(not t.exited for t in trs)
    actual = sum(t.realized_r for t in trs if t.exited)
    out = {"actual_campaign_r": r6(actual) if not unresolved else None}
    for nh in DEADGATE_HOURS:
        nbars = nh * 3_600_000 // ctx.step
        g = r1.fill_i + nbars
        for action in ("kill", "halve"):
            key = f"{action}_{nh}h"
            if unresolved:
                out[key] = None
                continue
            if g >= ctx.n:
                out[key] = {"evaluable": False, "triggered": False,
                            "cf_r": r6(actual)}
                continue
            w = real[max(r1.fill_i - 1, 0):g]
            w = w[~np.isnan(w)]
            be = bool(len(w) and ((w - r1.fill_px) * d >= -GATE_TOL).any())
            done = all(t.exit_i <= g for t in trs)
            if be or done:
                out[key] = {"evaluable": True, "triggered": False,
                            "cf_r": r6(actual)}
                continue
            cf = 0.0
            gate_px = ctx.sig.c[g]
            for t in trs:
                unit = (t.fill_px - t.stop_at_entry) * d
                cost_r = (t.fees + t.funding + t.slippage_usd) / t.one_r_usd
                if t.exit_i <= g:
                    cf += t.realized_r
                elif t.fill_i > g:
                    cf += 0.0 if action == "kill" else 0.5 * t.realized_r
                else:
                    at_gate = (gate_px - t.fill_px) * d / unit * t.size_r \
                        - cost_r
                    cf += at_gate if action == "kill" else \
                        0.5 * t.realized_r + 0.5 * at_gate
            out[key] = {"evaluable": True, "triggered": True, "cf_r": r6(cf)}
    return out


# ═══════════════════════════════════════ zone replica + labels (validated)
def zone_labels(ctx: S1Context) -> dict[int, dict]:
    """Counterfactual active-zone labels (9 variants incl. the live z3_prox)
    at every PRIME/CONFIRM/funnel-REJECT bar; the replica is validated
    bar-exactly against sig.active_zone AND sig.dir on every bar."""
    sig, p = ctx.sig, ctx.cfg["signal"]
    n = ctx.n
    prov_arm = p["provisional_arming"]
    prov_z12 = p["prov_zones"] == "Z1+Z2"
    v_prov = p["v_births_provisional"]
    zmem = ctx.cell.zone_memory
    fail_win = p["fail_win"]
    l, h, c = sig.l, sig.h, sig.c
    with np.errstate(invalid="ignore"):
        hit1_l = l <= ctx.gE9 + p["z1_prox"] * ctx.gATR
        hit1_s = h >= ctx.gE9 - p["z1_prox"] * ctx.gATR
        hit2_l = l <= ctx.gE89 + p["z2_prox"] * ctx.gATR
        hit2_s = h >= ctx.gE89 - p["z2_prox"] * ctx.gATR
        hits3 = {}
        for zp in Z3P:
            hits3[f"z3p_{zp}"] = (l <= ctx.gBandTop + zp * ctx.gATR,
                                  h >= ctx.gBandBot - zp * ctx.gATR)
        for a, b in ASYM:
            hits3[f"asym_{a}_{b}"] = (l <= ctx.gE200 + b * ctx.gATR,
                                      h >= ctx.gE200 - b * ctx.gATR)
        nan3 = {k: np.isnan(ctx.gATR) | np.isnan(
            ctx.gBandTop if k.startswith("z3p_") else ctx.gE200)
            for k in hits3}
        nan12 = np.isnan(ctx.gATR) | np.isnan(ctx.gE9)
        nan2 = np.isnan(ctx.gATR) | np.isnan(ctx.gE89)
    cap_l_live, cap_s_live = v_fire(ctx, dict(p))
    ids = list(hits3.keys())
    live_key = f"z3p_{p['z3_prox']}"
    assert live_key in ids
    want = set()
    for ev in sig.events:
        if ev.evt in ("PRIME", "CONFIRM") or \
                (ev.evt == "REJECT" and ev.subkey in ("prime", "confirm")):
            want.add(ev.i)
    gS2B, gS2S = ctx.gS2B, ctx.gS2S
    gBullX, gBearX = ctx.gBullX, ctx.gBearX
    tag1 = tag2 = None
    tag3 = dict.fromkeys(ids)
    dir_ = 0
    camp_counter = False
    beyond_bot = beyond_top = 0
    out: dict[int, dict] = {}
    for i in range(n):
        arm_bull = gBullX[i] if prov_arm else (gBullX[i] and gS2B[i])
        arm_bear = gBearX[i] if prov_arm else (gBearX[i] and gS2S[i])
        if arm_bull:
            dir_ = 1
            camp_counter = not gS2B[i]
            tag1 = tag2 = None
            tag3 = dict.fromkeys(ids)
        if arm_bear:
            dir_ = -1
            camp_counter = not gS2S[i]
            tag1 = tag2 = None
            tag3 = dict.fromkeys(ids)
        if camp_counter and ((dir_ == 1 and gS2B[i]) or
                             (dir_ == -1 and gS2S[i])):
            camp_counter = False
        stage_aligned = gS2B[i] if dir_ == 1 else \
            (gS2S[i] if dir_ == -1 else False)
        z1_armed = dir_ != 0
        z2_armed = dir_ != 0 and (not camp_counter or prov_z12)
        z3_armed = dir_ != 0 and stage_aligned
        if z1_armed and not nan12[i] and (hit1_l[i] if dir_ == 1
                                          else hit1_s[i]):
            tag1 = i
        if z2_armed and not nan2[i] and (hit2_l[i] if dir_ == 1
                                         else hit2_s[i]):
            tag2 = i
        if z3_armed:
            for k in ids:
                if not nan3[k][i] and (hits3[k][0][i] if dir_ == 1
                                       else hits3[k][1][i]):
                    tag3[k] = i
        rec1 = z1_armed and tag1 is not None and i - tag1 <= zmem
        rec2 = z2_armed and tag2 is not None and i - tag2 <= zmem
        live_zone = None
        rec_row = None
        if i in want:
            rec_row = {}
        for k in ids:
            rec3 = z3_armed and tag3[k] is not None and i - tag3[k] <= zmem
            z = 3 if rec3 else 2 if rec2 else 1 if rec1 else 0
            if k == live_key:
                live_zone = z
            if rec_row is not None:
                rec_row[k] = f"Z{z}" if z else "-"
        if live_zone != sig.active_zone[i]:
            raise AssertionError(
                f"{ctx.cell.cell_id}: zone replica diverged at bar {i}: "
                f"{live_zone} vs {int(sig.active_zone[i])}")
        if rec_row is not None:
            out[i] = rec_row
        if cap_l_live[i] and dir_ != 1:
            dir_ = 1
            camp_counter = (not gS2B[i]) if v_prov else False
            tag1 = tag2 = None
            tag3 = dict.fromkeys(ids)
        if cap_s_live[i] and dir_ != -1:
            dir_ = -1
            camp_counter = (not gS2S[i]) if v_prov else False
            tag1 = tag2 = None
            tag3 = dict.fromkeys(ids)
        beyond_bot = beyond_bot + 1 if (ctx.gBandBot[i] == ctx.gBandBot[i]
                                        and c[i] < ctx.gBandBot[i]) else 0
        beyond_top = beyond_top + 1 if (ctx.gBandTop[i] == ctx.gBandTop[i]
                                        and c[i] > ctx.gBandTop[i]) else 0
        if dir_ == 1 and beyond_bot == fail_win:
            dir_ = 0
        elif dir_ == -1 and beyond_top == fail_win:
            dir_ = 0
        if dir_ != sig.dir[i]:
            raise AssertionError(
                f"{ctx.cell.cell_id}: dir replica diverged at bar {i}: "
                f"{dir_} vs {int(sig.dir[i])}")
    return out


# ═══════════════════════════════════════════════════════════ V pipeline
def v_fire(ctx: S1Context, params: dict):
    """Vectorized cap_l/cap_s under the given thresholds (§4.6 replicated)."""
    sig = ctx.sig
    n = ctx.n
    p = params
    vol, vol_ma = sig.v, ctx.vol_ma
    c, o, l, h = sig.c, sig.o, sig.l, sig.h
    with np.errstate(invalid="ignore"):
        clx_dn = ((vol >= p["climax_mult"] * vol_ma) & (c < o)
                  & (l <= ctx.gE89 - p["cap_ext_atr"] * ctx.gATR))
        clx_up = ((vol >= p["climax_mult"] * vol_ma) & (c > o)
                  & (h >= ctx.gE89 + p["cap_ext_atr"] * ctx.gATR))
        idx = np.arange(n)
        last_dn = np.maximum.accumulate(np.where(clx_dn, idx, -BIG))
        last_up = np.maximum.accumulate(np.where(clx_up, idx, -BIG))
        prev_c = np.concatenate(([np.nan], c[:-1]))
        top, bot = ctx.gBandTop, ctx.gBandBot
        prev_top = np.concatenate(([np.nan], top[:-1]))
        prev_bot = np.concatenate(([np.nan], bot[:-1]))
        x_up = (~np.isnan(top)) & (c > top) & (prev_c <= prev_top)
        x_dn = (~np.isnan(bot)) & (c < bot) & (prev_c >= prev_bot)
        volc = vol >= p["cap_vol_conf"] * vol_ma
        cap_l = x_up & (idx - last_dn <= p["cap_window"]) & volc
        cap_s = x_dn & (idx - last_up <= p["cap_window"]) & volc
    if not ctx.cfg["signal"]["cap_on"]:
        cap_l = np.zeros(n, dtype=bool)
        cap_s = np.zeros(n, dtype=bool)
    return cap_l, cap_s


def v_shadow_rows(ctx: S1Context, in_window) -> list[dict]:
    sig = ctx.sig
    base_l, base_s = v_fire(ctx, dict(ctx.cfg["signal"]))
    base = {(int(i), 1) for i in np.flatnonzero(base_l)} | \
           {(int(i), -1) for i in np.flatnonzero(base_s)}
    rows = []
    for vid, over in V_VARIANTS:
        params = dict(ctx.cfg["signal"])
        params.update(over)
        cl, cs = v_fire(ctx, params)
        fires = sorted([(int(i), 1) for i in np.flatnonzero(cl)]
                       + [(int(i), -1) for i in np.flatnonzero(cs)])
        for i, d in fires:
            if not in_window(i) or i + 1 >= ctx.n:
                continue
            atr = sig.atr_x[i]
            if atr != atr:
                continue
            stop = (sig.l[i] - 0.5 * atr) if d == 1 else (sig.h[i] + 0.5 * atr)
            entry = float(sig.o[i + 1])
            unit = (entry - stop) * d
            fwd = {}
            for k in FWD_BARS:
                if i + k < ctx.n and unit > 0:
                    fwd[f"fwd_{k}_r"] = r6((sig.c[i + k] - entry) * d / unit)
                    fwd[f"fwd_{k}_bps"] = r6((sig.c[i + k] - entry) * d
                                             / entry * 1e4)
                else:
                    fwd[f"fwd_{k}_r"] = None
                    fwd[f"fwd_{k}_bps"] = None
            outcome_r = terminal = None
            if unit > 0:
                end = min(i + 1 + V_CAP_BARS, ctx.n)
                for j in range(i + 1, end):
                    if j > i + 1 and (sig.o[j] - stop) * d <= 0:
                        outcome_r = (sig.o[j] - entry) * d / unit
                        terminal = "stop"
                        break
                    if (sig.l[j] <= stop) if d == 1 else (sig.h[j] >= stop):
                        outcome_r, terminal = -1.0, "stop"
                        break
                    run = ((sig.h[j] if d == 1 else sig.l[j]) - entry) \
                        * d / unit
                    if run >= V_CAP_R:
                        outcome_r, terminal = V_CAP_R, "cap10"
                        break
                else:
                    if end == ctx.n:
                        terminal = "data_end"
                    else:
                        outcome_r = (sig.c[end - 1] - entry) * d / unit
                        terminal = "horizon"
            rows.append({
                "family": "v_shadow", "variant": vid, "i": i,
                "ts_open": iso(int(sig.exec_open_ms[i])), "dir": d,
                "incremental": (i, d) not in base,
                "entry_px": r6(entry), "stop": r6(stop),
                "outcome_r": r6(outcome_r), "terminal": terminal, **fwd,
            })
    return rows


# ══════════════════════════════════════════ sidecar families 1, 2 and 4
def _sim_forward(ctx: S1Context, d: int, start_bar: int, entry: float,
                 stop0: float, cap_r: float | None):
    """Forward outcome from `entry` at open of start_bar on the LIVE stop
    series (never-loosen from stop0), to stop / direction-run death /
    +cap_r. Returns (per-unit gross R, terminal)."""
    sig = ctx.sig
    real = ctx.real_stop(d)
    unit = (entry - stop0) * d
    if unit <= 0:
        return None, "bad_unit"
    _, camp_end = _campaign_span(sig, d, start_bar)
    last = camp_end if camp_end is not None else ctx.n - 1
    stop_prev = stop0
    for j in range(start_bar, last + 2):
        if j >= ctx.n:
            return None, "data_end"
        rv = real[j - 1]
        s = stop_prev if rv != rv else \
            (max(stop_prev, rv) if d == 1 else min(stop_prev, rv))
        if j > start_bar and (sig.o[j] - s) * d <= 0:
            return r6((sig.o[j] - entry) * d / unit), "stop"
        if (sig.l[j] <= s) if d == 1 else (sig.h[j] >= s):
            return r6((s - entry) * d / unit), "stop"
        if cap_r is not None:
            run = ((sig.h[j] if d == 1 else sig.l[j]) - entry) * d / unit
            if run >= cap_r:
                return r6(cap_r), "cap"
        if camp_end is not None and j == camp_end + 1:
            return r6((sig.o[j] - entry) * d / unit), "death"
        stop_prev = s
    return None, "data_end"


def drought_rows_for_camp(ctx: S1Context, camp: int, paths: dict,
                          in_window) -> list[dict]:
    sig = ctx.sig
    trs = ctx.camp_tranches[camp]
    d = trs[0].dir
    open_bars: dict[int, list] = {}
    for t in trs:
        if not t.exited:
            continue
        for j in range(t.fill_i, t.exit_i):
            open_bars.setdefault(j, []).append(t)
    if not open_bars:
        return []
    real = ctx.real_stop(d)
    brk = {N: (ctx.brk[N][0] if d == 1 else ctx.brk[N][1]) for N in (20, 55)}
    rib = ctx.capture["exec"]["bx" if d == 1 else "sx"]
    rows = []
    prev_fire = dict.fromkeys(ADD_TRIGGERS, False)
    for j in sorted(open_bars):
        fires = {}
        for N in (20, 55):
            ref = brk[N][j]
            fires[f"brk{N}"] = bool(ref == ref and (sig.c[j] - ref) * d > 0)
        fires["pull_e9"] = bool((sig.l[j] <= sig.e9x[j]) if d == 1
                                else (sig.h[j] >= sig.e9x[j]))
        fires["ext_2atr"] = bool(sig.atr_x[j] == sig.atr_x[j]
                                 and (sig.c[j] - sig.e9x[j]) * d
                                 >= 2.0 * sig.atr_x[j])
        fires["recross"] = bool(rib[j])
        for trig in ADD_TRIGGERS:
            fire_now = fires[trig] and not prev_fire[trig]
            prev_fire[trig] = fires[trig]
            if not fire_now or not in_window(j) or j + 1 >= ctx.n:
                continue
            stop_now = real[j]
            opens = open_bars[j]
            admissible = {}
            if stop_now == stop_now:
                admissible["baseline"] = bool(all(
                    (t.fill_px - stop_now) * d <= GATE_TOL for t in opens))
            else:
                admissible["baseline"] = None
            for cid in RATCHET_IDS:
                ok = True
                for t in opens:
                    arr = paths.get((t.tranche_id, cid))
                    if arr is None or j - t.fill_i >= len(arr) or \
                            j < t.fill_i:
                        ok = None
                        break
                    s = arr[j - t.fill_i]
                    if s != s or (t.fill_px - s) * d > GATE_TOL:
                        ok = False
                        break
                admissible[cid] = ok
            outcome_r = terminal = None
            if stop_now == stop_now:
                outcome_r, terminal = _sim_forward(
                    ctx, d, j + 1, float(sig.o[j + 1]), float(stop_now),
                    F1_CAP_R)
            rows.append({
                "family": "add_trigger", "trigger": trig, "i": j,
                "ts_open": iso(int(sig.exec_open_ms[j])), "dir": d,
                "campaign": camp, "n_open": len(opens),
                "stop": r6(stop_now) if stop_now == stop_now else None,
                "outcome_r": outcome_r, "terminal": terminal,
                "admissible_under": admissible,
            })
    return rows


def reentry_rows(ctx: S1Context, in_window) -> list[dict]:
    sig = ctx.sig
    rows = []
    seen = set()
    for rj in ctx.trades.rejects:
        if rj.reason != "not_positioned":
            continue
        key = (rj.i, rj.dir)
        if key in seen:
            continue
        seen.add(key)
        d, j = rj.dir, rj.i
        if not in_window(j):
            continue
        stop_now = ctx.real_stop(d)[j]
        outcome_r = terminal = stop_bps = None
        if j + 1 < ctx.n and stop_now == stop_now:
            entry = float(sig.o[j + 1])
            stop_bps = r6(abs(entry - stop_now) / entry * 1e4)
            outcome_r, terminal = _sim_forward(ctx, d, j + 1, entry,
                                               float(stop_now), None)
        rows.append({
            "family": "reentry_ab", "i": j,
            "ts_open": iso(int(sig.exec_open_ms[j])), "dir": d,
            "stop": r6(stop_now) if stop_now == stop_now else None,
            "stop_dist_bps": stop_bps,
            "outcome_r": outcome_r, "terminal": terminal,
        })
    return rows


def mtf_cross_rows(ctx: S1Context, in_window) -> list[dict]:
    sig = ctx.sig
    open_by_bar: dict[int, list] = {}
    for t in ctx.trades.tranches:
        if not t.exited:
            continue
        for j in range(t.fill_i, t.exit_i):
            open_by_bar.setdefault(j, []).append(t)
    rows = []
    for tf, pack in ctx.capture.items():
        for pair, up, dn in (("e9_e89", "bx", "sx"),
                             ("e89_e200", "bx2", "sx2")):
            for flag, xd in ((pack[up], 1), (pack[dn], -1)):
                for j in np.flatnonzero(flag):
                    j = int(j)
                    if j not in open_by_bar or not in_window(j):
                        continue
                    for t in open_by_bar[j]:
                        unit = (t.fill_px - t.stop_at_entry) * t.dir
                        rows.append({
                            "family": "mtf_cross", "tf": tf, "pair": pair,
                            "cross_dir": xd, "i": j,
                            "ts_open": iso(int(sig.exec_open_ms[j])),
                            "dir": t.dir, "tranche_id": t.tranche_id,
                            "with_trend": xd == t.dir,
                            "remaining_life_r":
                                r6((t.exit_px - sig.c[j]) * t.dir / unit),
                            "tranche_realized_unit_r":
                                r6((t.exit_px - t.fill_px) * t.dir / unit),
                        })
    return rows


# ═══════════════════════════════════════════════════════════ top level
def compute_s1(cell: Cell, cfg: dict, sig: SignalResult, trades: TradeResult,
               data: dict, resampled_dir: Path, in_window) -> dict:
    """Returns {fill_s1, exit_s1, zone_s1, sidecar} for replay to attach."""
    ctx = S1Context(cell, cfg, sig, trades, data, resampled_dir)
    zone = zone_labels(ctx)          # includes the bar-exact validation

    fill_s1: dict[str, dict] = {}
    exit_s1: dict[str, dict] = {}
    sidecar: list[dict] = []

    for camp in sorted(ctx.camp_tranches):
        trs = ctx.camp_tranches[camp]
        camp_end = ctx.camp_end[camp]
        opener = trs[0]
        dg = deadgate_block(ctx, camp)
        paths: dict[tuple, np.ndarray] = {}
        engs: dict[tuple, int | None] = {}
        for tr in trs:
            fill_s1[tr.tranche_id] = {
                "entryflags": entryflags_block(ctx, tr),
                "cluster": cluster_block(ctx, tr),
            }
            if tr.exited and camp_end is not None:
                for cid in RATCHET_IDS:
                    paths[(tr.tranche_id, cid)], engs[(tr.tranche_id, cid)] \
                        = candidate_path(ctx, tr, cid, camp_end)
        for tr in trs:
            if not tr.exited or camp_end is None:
                continue
            d = tr.dir
            unit = (tr.fill_px - tr.stop_at_entry) * d
            mfe_bar = _mfe_bar(ctx, tr)
            peak = tr.peak
            if tr.exit_reason == "stop":
                jx = tr.exit_i
                peak = max(peak, sig.h[jx]) if d == 1 else \
                    min(peak, sig.l[jx])
            enr_mfe = (peak - tr.fill_px) * d / unit
            adds = [j for j in ctx.add_signals[d]
                    if tr.fill_i <= j < tr.exit_i]
            blk = {}
            for cid in RATCHET_IDS:
                path = paths[(tr.tranche_id, cid)]
                eng = engs[(tr.tranche_id, cid)]
                sim = simulate_exit(ctx, tr, path, camp_end)
                # engagement counts only if it precedes the candidate's own
                # exit (the path keeps advancing past it for gate tests)
                if sim is not None and eng is not None and eng > sim[1]:
                    eng = None
                rec = {"engaged": eng is not None,
                       "engage_i_offset": (eng - tr.fill_i)
                       if eng is not None else None}
                if sim is None:
                    rec.update({"exit_r": None, "exit_i_offset": None,
                                "noise_stopout": None, "capture_pct": None,
                                "adds_would_be_eligible": None})
                else:
                    px, bar, kind = sim
                    exit_r = (px - tr.fill_px) * d / unit
                    rec.update({
                        "exit_r": r6(exit_r),
                        "exit_i_offset": bar - tr.fill_i,
                        "noise_stopout": _noise_stopout(ctx, tr, px, bar,
                                                        kind),
                        "capture_pct": (r6(exit_r / enr_mfe)
                                        if enr_mfe >= 1.0 else None),
                        "adds_would_be_eligible": sum(
                            1 for j in adds
                            if path[j - tr.fill_i] == path[j - tr.fill_i]
                            and (tr.fill_px - path[j - tr.fill_i]) * d
                            <= GATE_TOL),
                    })
                blk[cid] = rec
            exit_s1[tr.tranche_id] = {
                "ratchet": blk,
                "advance": advance_block(ctx, tr, mfe_bar),
                "mtf": mtf_block(ctx, tr, mfe_bar),
                "deadgate": dg if tr is opener else None,
            }
        sidecar.extend(drought_rows_for_camp(ctx, camp, paths, in_window))

    sidecar.extend(reentry_rows(ctx, in_window))
    sidecar.extend(v_shadow_rows(ctx, in_window))
    sidecar.extend(mtf_cross_rows(ctx, in_window))
    sidecar.sort(key=lambda r: (
        r["ts_open"], r["family"], r.get("variant", ""),
        r.get("trigger", ""), r.get("tf", ""), r.get("pair", ""),
        r.get("tranche_id", ""), r.get("dir", 0), r.get("cross_dir", 0)))
    return {"fill_s1": fill_s1, "exit_s1": exit_s1, "zone_s1": zone,
            "sidecar": sidecar}


def write_sidecar(rows: list[dict], path: Path, cell_id: str,
                  base: dict) -> str:
    """Canonical deterministic sidecar JSONL; returns sha256 hex."""
    import hashlib
    path.parent.mkdir(parents=True, exist_ok=True)
    h = hashlib.sha256()
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        for r in rows:
            row = {"cell_id": cell_id, "run_id": base["run_id"],
                   "engine_version": base["engine_version"], **r}
            row.pop("i", None)
            line = json.dumps(row, sort_keys=True, separators=(",", ":"),
                              ensure_ascii=False, allow_nan=False)
            f.write(line + "\n")
            h.update((line + "\n").encode("utf-8"))
    return h.hexdigest()
