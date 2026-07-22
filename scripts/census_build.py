"""CENSUS-1 — MTF signal-stack census (Tier B, trade-independent) — BUILD.

Contract: Census_1_MTF_Signal_Stack_Builder_Contract.md, under Amendment 1
(Census_1_Amendment_1.md). Engine 1.0.11 byte-UNTOUCHED — this script only
IMPORTS engine.indicators (ema/rma/atr/crossover/crossunder); it edits no
engine file and simulates no trading. It photographs price.

What it emits (the census substrate, consumed by scripts/census_analyze.py):
  research_outputs/census[_run2]/
     census_outcomes.jsonl   every cross event, dual-basis forward MFE/MAE at
                             {20,100,500} exec-bar horizons + (on exec-5m 9/89
                             anchors) the regime-scale horizon per governor lens
     census_ladder.jsonl     D8 cascade chains: each initiating 9/89 cross, its
                             first same-direction 9/89 follow-on on every other
                             TF, the lag, and the remaining forward move per rung
     census_termini.jsonl    D10 pullback termini (confirmed (5,5) pivots in the
                             lens regime) + the matched in-regime null sample
     continuation.jsonl      §3.4 continuation moments (D4/D9 anchor set)
     build_manifest.json     window/estate/params + per-file sha256 + row counts

Determinism (F-DET): every array op is vectorized and order-stable; every JSONL
is sorted by a total key and floats are rounded to 6 dp before emission, so two
builds are byte-identical. No network (offline cache only). No lookahead: HTF
state is gathered as-of the last CLOSED HTF bar (engine.htf convention); a cross
is anchored on the FIRST exec bar whose open >= the cross bar's close.

Usage:
  .venv/Scripts/python.exe scripts/census_build.py            # run1 root
  .venv/Scripts/python.exe scripts/census_build.py --run2     # run2 root
  CENSUS_ASSETS=TAOUSDT .venv/Scripts/python.exe scripts/census_build.py  # smoke
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from engine.indicators import ema, atr, crossover, crossunder  # noqa: E402

# ----------------------------------------------------------------------------
# Pre-registered configuration (contract §3-§5 + Amendment §2-§5). FROZEN.
# ----------------------------------------------------------------------------
ASSET_STARTS = {
    "BTCUSDT": "2019-10-01", "ETHUSDT": "2020-01-01", "JTOUSDT": "2024-01-01",
    "NEARUSDT": "2020-11-01", "SOLUSDT": "2020-10-01", "TAOUSDT": "2024-05-01",
    "ZECUSDT": "2020-03-01",
}
# exploration-classic ceiling: open_time < 2024-07-01T00:00:00Z (DATA_CENSUS.md).
CEIL_MS = int(datetime(2024, 7, 1, tzinfo=timezone.utc).timestamp() * 1000)

TF_MS = {"5m": 300_000, "15m": 900_000, "30m": 1_800_000, "1h": 3_600_000,
         "4h": 14_400_000, "12h": 43_200_000, "1d": 86_400_000}
TFS = ["5m", "15m", "30m", "1h", "4h", "12h", "1d"]
EXEC_TF = "5m"
# native cache TFs; 30m<-15m (ratio 2), 1d<-1h (ratio 24) resampled (s1 algo).
RESAMPLE = {"30m": ("15m", 1_800_000), "1d": ("1h", 86_400_000)}

LEN_FAST, LEN_SLOW, LEN_TREND, ATR_LEN = 9, 89, 200, 14
CROSS_PAIRS = {"9_89": (LEN_FAST, LEN_SLOW), "89_200": (LEN_SLOW, LEN_TREND),
               "9_200": (LEN_FAST, LEN_TREND)}
HORIZONS = [20, 100, 500]
REGIME_CAP = 2000
GOVERNORS = ["1h", "4h", "12h", "1d"]
GOV_NEXT = {"1h": "4h", "4h": "12h", "12h": "1d", "1d": None}  # lens+1

RIBBON_SEP_ATR = 1.0       # §3.4 continuation: exec ribbon separated >= 1.0 ATR
NOPULLBACK_LOOKBACK = 20   # §3.4: no pullback-reclaim in the prior 20 exec bars
PIVOT_L, PIVOT_R = 5, 5    # D10 (5,5) pivot convention (F-CFG pinned)
NULL_SEED = 20260721       # D10 matched-null seed (F-CFG pinned)
NULL_MULT = 10             # D10 null sample multiple (>= 10x termini, F-CFG)
Z2_BAND_ATR = 0.35         # D10 excess-mass reference band (Z2 width)
BOOTSTRAP_SEED = 20260721  # analysis seed (recorded here for provenance)

R6 = 6  # float rounding for byte-stable JSONL


def ms(day: str) -> int:
    return int(datetime.strptime(day, "%Y-%m-%d")
               .replace(tzinfo=timezone.utc).timestamp() * 1000)


# ----------------------------------------------------------------------------
# Data loading + per-TF indicator frame
# ----------------------------------------------------------------------------
def _resample(src: pd.DataFrame, step_ms: int) -> pd.DataFrame:
    """OHLCV aggregation, identical to scripts/s1_resample.aggregate()."""
    key = src["open_time"].to_numpy(np.int64) // step_ms * step_ms
    g = src.groupby(key, sort=True)
    return pd.DataFrame({
        "open_time": np.asarray(sorted(set(key)), dtype=np.int64),
        "open": g["open"].first().to_numpy(float),
        "high": g["high"].max().to_numpy(float),
        "low": g["low"].min().to_numpy(float),
        "close": g["close"].last().to_numpy(float),
        "volume": g["volume"].sum().to_numpy(float),
    })


def load_tf(klines: Path, sym: str, tf: str, start_ms: int) -> pd.DataFrame:
    """Load one TF frame over [start, CEIL), computing EMAs/ATR and crosses.

    Higher TFs read their own closed bars; 30m/1d are resampled from 15m/1h.
    Bars are filtered to open_time < CEIL_MS (exploration-classic)."""
    if tf in RESAMPLE:
        src_tf, step = RESAMPLE[tf]
        raw = pd.read_parquet(klines / f"{sym}_{src_tf}.parquet")
        raw = raw[raw["open_time"] < CEIL_MS].sort_values("open_time")
        df = _resample(raw.reset_index(drop=True), step)
    else:
        df = pd.read_parquet(klines / f"{sym}_{tf}.parquet")
        df = df[df["open_time"] < CEIL_MS].sort_values("open_time").reset_index(drop=True)
    # warm-up: keep bars from start_ms, but compute EMA/ATR on full available
    # history so the recursive seed is warmed (parity with the engine).
    o = df["open_time"].to_numpy(np.int64)
    c = df["close"].to_numpy(float)
    h = df["high"].to_numpy(float)
    lo = df["low"].to_numpy(float)
    e9 = ema(c, LEN_FAST); e89 = ema(c, LEN_SLOW); e200 = ema(c, LEN_TREND)
    a = atr(h, lo, c, ATR_LEN)
    out = pd.DataFrame({"open_time": o, "open": df["open"].to_numpy(float),
                        "high": h, "low": lo, "close": c,
                        "e9": e9, "e89": e89, "e200": e200, "atr": a})
    # restrict to the asset window AFTER warm-up (start_ms floor)
    out = out[out["open_time"] >= start_ms].reset_index(drop=True)
    return out


def detect_crosses(df: pd.DataFrame) -> dict:
    """Return {cross_type: {'up': idx[], 'down': idx[]}} on this TF's bars."""
    ev = {}
    for name, (fa, sl) in CROSS_PAIRS.items():
        a = df[f"e{fa}"].to_numpy(); b = df[f"e{sl}"].to_numpy()
        ev[name] = {"up": np.nonzero(crossover(a, b))[0],
                    "down": np.nonzero(crossunder(a, b))[0]}
    return ev


# ----------------------------------------------------------------------------
# As-of gather + forward rolling excursion
# ----------------------------------------------------------------------------
def asof_idx(exec_open: np.ndarray, htf_open: np.ndarray, tf: str) -> np.ndarray:
    """Per exec bar, index of the last HTF bar with close <= exec open (-1 none)."""
    htf_close = htf_open + TF_MS[tf]
    return np.searchsorted(htf_close, exec_open, side="right") - 1


def pivots_strict(x: np.ndarray, left: int, right: int, want_low: bool) -> np.ndarray:
    """Strict (left,right) pivot: center strictly lower (low) / higher (high)
    than all `left` bars before and `right` bars after. Ties -> not a pivot
    (a proper isolated pivot, matching ta.pivotlow/pivothigh semantics)."""
    n = len(x)
    ok = np.ones(n, dtype=bool)
    for k in range(1, left + 1):
        sh = np.full(n, np.nan); sh[k:] = x[:-k]          # x[i-k]
        with np.errstate(invalid="ignore"):
            ok &= (x < sh) if want_low else (x > sh)
    for k in range(1, right + 1):
        sh = np.full(n, np.nan); sh[:-k] = x[k:]          # x[i+k]
        with np.errstate(invalid="ignore"):
            ok &= (x < sh) if want_low else (x > sh)
    ok[:left] = False
    ok[n - right:] = False
    return ok


def fwd_extents(high: np.ndarray, low: np.ndarray, h: int):
    """Forward window [i .. i+h-1]: (max high, min low, bars available)."""
    n = len(high)
    hi = pd.Series(high[::-1]).rolling(h, min_periods=1).max().to_numpy()[::-1]
    lo = pd.Series(low[::-1]).rolling(h, min_periods=1).min().to_numpy()[::-1]
    avail = np.minimum(h, n - np.arange(n))
    return hi, lo, avail


def excursion(p0: np.ndarray, hi: np.ndarray, lo: np.ndarray,
              is_long: np.ndarray, atr_basis: np.ndarray):
    """Dual-basis MFE/MAE. long: fav up / adv down; short: mirror."""
    fav = np.where(is_long, hi - p0, p0 - lo)
    adv = np.where(is_long, lo - p0, p0 - hi)
    return (fav / p0 * 1e4, adv / p0 * 1e4, fav / atr_basis, adv / atr_basis)


# ----------------------------------------------------------------------------
# Per-asset census
# ----------------------------------------------------------------------------
def census_asset(klines: Path, sym: str, log) -> dict:
    t0 = time.time()
    start_ms = ms(ASSET_STARTS[sym])
    frames = {tf: load_tf(klines, sym, tf, start_ms) for tf in TFS}
    ex = frames[EXEC_TF]
    xo = ex["open_time"].to_numpy(np.int64)
    xopen = ex["open"].to_numpy(float)
    xhigh = ex["high"].to_numpy(float)
    xlow = ex["low"].to_numpy(float)
    xclose = ex["close"].to_numpy(float)
    xatr = ex["atr"].to_numpy(float)
    N = len(ex)

    # forward extents per fixed horizon (exec grid)
    fwd = {h: fwd_extents(xhigh, xlow, h) for h in HORIZONS}

    # as-of gather of every TF onto the exec grid (for state vector + regimes)
    asof = {tf: asof_idx(xo, frames[tf]["open_time"].to_numpy(np.int64), tf)
            for tf in TFS}

    def gather(tf, col):
        idx = asof[tf]; arr = frames[tf][col].to_numpy(float)
        out = arr[np.clip(idx, 0, None)].copy(); out[idx < 0] = np.nan
        return out

    # per-TF as-of EMAs/ATR on the exec grid
    tfE = {tf: {c: gather(tf, c) for c in ("e9", "e89", "e200", "atr")}
           for tf in TFS}

    # governor regimes on the exec grid (long = G e9 > e89, as-of)
    gov_long = {g: (tfE[g]["e9"] > tfE[g]["e89"]) for g in GOVERNORS}

    # governor 9/89 flip anchors (exec idx of first-visible bar per flip)
    def cross_anchor_idx(tf, sub):  # first exec bar with open >= cross close
        oc = frames[tf]["open_time"].to_numpy(np.int64)[sub] + TF_MS[tf]
        return np.searchsorted(xo, oc, side="left")
    crosses = {tf: detect_crosses(frames[tf]) for tf in TFS}
    gov_flip_anchor = {}
    for g in GOVERNORS:
        ups = cross_anchor_idx(g, crosses[g]["9_89"]["up"])
        dns = cross_anchor_idx(g, crosses[g]["9_89"]["down"])
        gov_flip_anchor[g] = np.sort(np.concatenate([ups, dns]))

    # D9 factor prerequisites (state at the arming anchor; no lookahead — HTF
    # values are as-of via tfE, exec ribbon is the current exec bar).
    ex_e9 = ex["e9"].to_numpy(); ex_e89 = ex["e89"].to_numpy()
    ribbon_exec = np.abs(ex_e9 - ex_e89) / np.where(xatr > 0, xatr, np.nan)
    e989_anchor = {tf: {d: np.sort(cross_anchor_idx(tf, crosses[tf]["9_89"][d]))
                        for d in ("up", "down")} for tf in TFS}
    fctx = {"tfE": tfE, "xclose": xclose, "ex_e9": ex_e9, "ex_e89": ex_e89,
            "ribbon_exec": ribbon_exec, "e989_anchor": e989_anchor}

    # ---- cross-event outcomes (census_outcomes.jsonl) ----
    out_rows = []
    for tf in TFS:
        for ctype in CROSS_PAIRS:
            for direction, sub in (("up", crosses[tf][ctype]["up"]),
                                   ("down", crosses[tf][ctype]["down"])):
                if len(sub) == 0:
                    continue
                fr = frames[tf]
                ev_open = fr["open_time"].to_numpy(np.int64)[sub]
                ev_close = ev_open + TF_MS[tf]
                ev_price = fr["close"].to_numpy(float)[sub]
                ev_atr = fr["atr"].to_numpy(float)[sub]
                anch = np.searchsorted(xo, ev_close, side="left")
                keep = (anch < N) & np.isfinite(ev_atr) & (ev_atr > 0)
                if not keep.any():
                    continue
                sub, ev_open, ev_price, ev_atr, anch = (
                    sub[keep], ev_open[keep], ev_price[keep],
                    ev_atr[keep], anch[keep])
                is_long = np.full(len(anch), direction == "up")
                p0 = xopen[anch]
                row_out = {h: excursion(p0, fwd[h][0][anch], fwd[h][1][anch],
                                        is_long, ev_atr) for h in HORIZONS}
                avail = {h: fwd[h][2][anch] for h in HORIZONS}
                is_exec_regime = (tf == EXEC_TF and ctype == "9_89")
                for j in range(len(anch)):
                    r = {"asset": sym, "tf": tf, "cross_type": ctype,
                         "dir": direction, "ts": int(ev_open[j]),
                         "exec_ts": int(xo[anch[j]]),
                         "exec_idx": int(anch[j]),
                         "event_price": round(float(ev_price[j]), R6),
                         "p0": round(float(p0[j]), R6),
                         "atr_basis": round(float(ev_atr[j]), R6)}
                    for h in HORIZONS:
                        mb, ab, ma_, aa = row_out[h]
                        r[f"mfe_bps_h{h}"] = round(float(mb[j]), R6)
                        r[f"mae_bps_h{h}"] = round(float(ab[j]), R6)
                        r[f"mfe_atr_h{h}"] = round(float(ma_[j]), R6)
                        r[f"mae_atr_h{h}"] = round(float(aa[j]), R6)
                        r[f"trunc_h{h}"] = bool(avail[h][j] < h)
                    if is_exec_regime:
                        r["gov"] = _regime_scale(
                            anch[j], is_long[j], xopen, xhigh, xlow, xatr,
                            gov_flip_anchor, gov_long, N)
                        r["fac"] = _factors(int(anch[j]), bool(is_long[j]), fctx)
                    out_rows.append(r)

    # ---- continuation moments (continuation.jsonl) ----
    cont_rows = _continuation(sym, xo, xopen, xhigh, xlow, xclose, xatr,
                              ex, fwd, crosses, frames, N)

    # ---- D8 cascade ladder (census_ladder.jsonl) ----
    ladder_rows = _ladder(sym, xo, xopen, xhigh, xlow, crosses, frames, N)

    # ---- D10 pullback termini + matched null (census_termini.jsonl) ----
    term_rows = _termini(sym, frames)

    log(f"  {sym}: N={N} outcomes={len(out_rows)} cont={len(cont_rows)} "
        f"ladder={len(ladder_rows)} termini={len(term_rows)} "
        f"({time.time()-t0:.1f}s)")
    return {"outcomes": out_rows, "continuation": cont_rows,
            "ladder": ladder_rows, "termini": term_rows, "N": N}


def _regime_scale(k, is_long, xopen, xhigh, xlow, xatr, gov_flip_anchor,
                  gov_long, N) -> dict:
    """Regime-scale horizon per governor lens: window [k .. next G-flip), capped
    at REGIME_CAP; ATR basis = exec ATR at the anchor."""
    p0 = xopen[k]; ab = xatr[k]
    gov = {}
    for g in GOVERNORS:
        fa = gov_flip_anchor[g]
        pos = np.searchsorted(fa, k, side="right")
        nxt = fa[pos] if pos < len(fa) else N
        end = int(min(nxt, k + REGIME_CAP, N))
        end = max(end, k + 1)
        hi = xhigh[k:end].max(); lo = xlow[k:end].min()
        fav = (hi - p0) if is_long else (p0 - lo)
        adv = (lo - p0) if is_long else (p0 - hi)
        gov[g] = {"regime_long": bool(gov_long[g][k]),
                  "mfe_bps": round(float(fav / p0 * 1e4), R6),
                  "mae_bps": round(float(adv / p0 * 1e4), R6),
                  "mfe_atr": round(float(fav / ab), R6) if ab > 0 else None,
                  "mae_atr": round(float(adv / ab), R6) if ab > 0 else None,
                  "end_off": int(end - k),
                  "trunc": bool(end >= N or end == k + REGIME_CAP)}
    return gov


def _factors(k, is_long, fx) -> dict:
    """D9 registered factor list F1..F9, per lens, at an arming anchor (exec-5m
    9/89 cross). FIXED here, never tuned. Higher-TF values are as-of (tfE); the
    exec ribbon is the current exec bar. Returns {lens: {"k": int, "bits": str}}.

      F1 1D structurally aligned (e89>e200), direction-signed
      F2 12H structurally aligned, direction-signed
      F3 lens-governor regime aligned (e9>e89), direction-signed
      F4 price beyond lens e89 (in-dir)
      F5 price beyond lens+1 e200 (in-dir; False if no lens+1)
      F6 a faster-TF 9/89 cross in-direction within the last 20 lens bars
      F7 lens 9/200 state aligned (e9 vs e200), direction-signed
      F8 exec ribbon separated >= 1.0 ATR in-direction
      F9 pullback-terminus-at-EMA: price within 0.35 lens-ATR of the lens
         e89 or e200 at the anchor (D10's zone-landing condition, applied here)
    """
    tfE = fx["tfE"]; xclose = fx["xclose"]
    d = 1.0 if is_long else -1.0
    close = xclose[k]
    out = {}
    f1 = (tfE["1d"]["e89"][k] > tfE["1d"]["e200"][k]) == is_long
    f2 = (tfE["12h"]["e89"][k] > tfE["12h"]["e200"][k]) == is_long
    f8 = bool(fx["ribbon_exec"][k] >= RIBBON_SEP_ATR
              and ((fx["ex_e9"][k] > fx["ex_e89"][k]) == is_long))
    for L in GOVERNORS:
        e9 = tfE[L]["e9"][k]; e89 = tfE[L]["e89"][k]
        e200 = tfE[L]["e200"][k]; la = tfE[L]["atr"][k]
        f3 = (e9 > e89) == is_long
        f4 = (close - e89) * d > 0
        nxt = GOV_NEXT[L]
        if nxt is not None and np.isfinite(tfE[nxt]["e200"][k]):
            f5 = (close - tfE[nxt]["e200"][k]) * d > 0
        else:
            f5 = False
        w = int(round(20 * TF_MS[L] / TF_MS[EXEC_TF]))  # 20 lens bars in exec
        f6 = False
        for tf in TFS:
            if TF_MS[tf] >= TF_MS[L]:
                continue  # faster TFs only
            arr = fx["e989_anchor"][tf]["up" if is_long else "down"]
            pos = np.searchsorted(arr, k, side="right")
            if pos > 0 and (k - arr[pos - 1]) <= w:
                f6 = True
                break
        f7 = (e9 > e200) == is_long
        if np.isfinite(la) and la > 0:
            f9 = min(abs(close - e89), abs(close - e200)) / la <= Z2_BAND_ATR
        else:
            f9 = False
        bits = [f1, f2, f3, f4, f5, f6, f7, f8, f9]
        out[L] = {"k": int(sum(bool(b) for b in bits)),
                  "bits": "".join("1" if b else "0" for b in bits)}
    return out


def _continuation(sym, xo, xopen, xhigh, xlow, xclose, xatr, ex, fwd,
                  crosses, frames, N) -> list:
    e9 = ex["e9"].to_numpy(); e89 = ex["e89"].to_numpy()
    e200 = ex["e200"].to_numpy()
    long_dir = e9 > e89
    ribbon_sep = np.abs(e9 - e89) / np.where(xatr > 0, xatr, np.nan)
    beyond_e9 = np.where(long_dir, xclose > e9, xclose < e9)
    # no pullback-reclaim in prior LOOKBACK bars: every prior close held beyond
    # e9 in-dir (a closing-basis pullback would have re-touched e9). Vectorized
    # rolling-all: min of the 0/1 hold flag over the window == 1.
    held = np.where(long_dir, xclose > e9, xclose < e9).astype(float)
    prior_hold = (pd.Series(held).rolling(NOPULLBACK_LOOKBACK,
                  min_periods=NOPULLBACK_LOOKBACK).min().to_numpy() == 1.0)
    qual = (np.isfinite(ribbon_sep) & (ribbon_sep >= RIBBON_SEP_ATR)
            & beyond_e9 & prior_hold & np.isfinite(e200))
    idxs = np.nonzero(qual)[0]
    idxs = idxs[idxs < N]
    if len(idxs) == 0:
        return []
    # prior-window cross presence per exec bar (any TF), for D4
    def prior_cross(win, ctype, only_faster=None):
        flag = np.zeros(N, dtype=bool)
        for tf in TFS:
            if only_faster is not None and TF_MS[tf] >= only_faster:
                continue
            for d in ("up", "down"):
                sub = crosses[tf][ctype][d]
                if len(sub) == 0:
                    continue
                oc = frames[tf]["open_time"].to_numpy(np.int64)[sub] + TF_MS[tf]
                a = np.searchsorted(xo, oc, side="left")
                a = a[a < N]
                for ai in a:
                    flag[ai:min(ai + win, N)] = True
        return flag
    f989_20 = prior_cross(20, "9_89")
    f9200_20 = prior_cross(20, "9_200")
    f989_5 = prior_cross(5, "9_89")
    rows = []
    p0 = xopen[idxs]; ab = xatr[idxs]; il = long_dir[idxs]
    exc = {h: excursion(p0, fwd[h][0][idxs], fwd[h][1][idxs], il, ab)
           for h in HORIZONS}
    for n, i in enumerate(idxs):
        r = {"asset": sym, "exec_ts": int(xo[i]), "exec_idx": int(i),
             "dir": "long" if long_dir[i] else "short",
             "p0": round(float(xopen[i]), R6),
             "atr_basis": round(float(xatr[i]), R6),
             "ribbon_sep_atr": round(float(ribbon_sep[i]), R6),
             "cross_989_prior20": bool(f989_20[i]),
             "cross_9200_prior20": bool(f9200_20[i]),
             "cross_989_prior5": bool(f989_5[i])}
        for h in HORIZONS:
            mb, abps, ma_, aa = exc[h]
            r[f"mfe_bps_h{h}"] = round(float(mb[n]), R6)
            r[f"mfe_atr_h{h}"] = round(float(ma_[n]), R6)
            r[f"mae_atr_h{h}"] = round(float(aa[n]), R6)
            r[f"trunc_h{h}"] = bool(fwd[h][2][i] < h)
        rows.append(r)
    return rows


def _ladder(sym, xo, xopen, xhigh, xlow, crosses, frames, N) -> list:
    """D8: each initiating 9/89 cross -> first same-dir 9/89 follow-on on every
    other TF within [k, k+REGIME_CAP], the lag, and remaining forward move
    (100-bar) from each follow-on. Full chains, never cherry-picked."""
    # precompute per-TF 9/89 anchor arrays (sorted) by direction
    anch = {tf: {} for tf in TFS}
    for tf in TFS:
        for d in ("up", "down"):
            sub = crosses[tf]["9_89"][d]
            oc = frames[tf]["open_time"].to_numpy(np.int64)[sub] + TF_MS[tf]
            a = np.searchsorted(xo, oc, side="left")
            anch[tf][d] = np.sort(a[a < N])
    hi100 = pd.Series(xhigh[::-1]).rolling(100, min_periods=1).max().to_numpy()[::-1]
    lo100 = pd.Series(xlow[::-1]).rolling(100, min_periods=1).min().to_numpy()[::-1]
    rows = []
    for init_tf in TFS:
        for d in ("up", "down"):
            for k in anch[init_tf][d]:
                is_long = d == "up"
                rungs = []
                for tf in TFS:
                    if tf == init_tf:
                        continue
                    arr = anch[tf][d]
                    pos = np.searchsorted(arr, k, side="right")
                    if pos >= len(arr):
                        continue
                    kf = int(arr[pos])
                    lag = kf - int(k)
                    if lag > REGIME_CAP:
                        continue
                    p0 = xopen[kf]
                    fav = (hi100[kf] - p0) if is_long else (p0 - lo100[kf])
                    adv = (lo100[kf] - p0) if is_long else (p0 - hi100[kf])
                    ab = float(frames[EXEC_TF]["atr"].to_numpy()[kf]) \
                        if EXEC_TF else 0.0
                    rungs.append({"tf": tf, "lag_exec_bars": lag,
                                  "rem_mfe_bps_100": round(float(fav / p0 * 1e4), R6),
                                  "rem_mfe_atr_100": round(float(fav / ab), R6) if ab > 0 else None,
                                  "rem_mae_atr_100": round(float(adv / ab), R6) if ab > 0 else None,
                                  "trunc": bool(fwd_avail(kf, 100, N) < 100)})
                rows.append({"asset": sym, "init_tf": init_tf, "dir": d,
                             "init_ts": int(xo[int(k)]),
                             "init_exec_idx": int(k),
                             "n_rungs": len(rungs), "rungs": rungs})
    return rows


def fwd_avail(i, h, N):
    return min(h, N - i)


def _termini(sym, frames) -> list:
    """D10: confirmed strict (5,5) pivots on each LENS's OWN frame while that
    lens is in regime (long -> pivot low; short -> pivot high), plus the matched
    in-regime null (random same-lens/same-regime lens bars, NULL_MULT x count,
    seed pinned). Distances to the lens e89/e200 and the lens+1 e200 in
    lens-ATR; the terminus row also carries the forward 100-lens-bar MFE from
    the confirmation bar (i+PIVOT_R). The null is mandatory because with 21 EMA
    lines every price point is near some line — only excess clustering counts."""
    rows = []
    rng = np.random.default_rng(NULL_SEED)
    for lens in GOVERNORS:
        lf = frames[lens]
        n = len(lf)
        o = lf["open_time"].to_numpy(np.int64)
        opn = lf["open"].to_numpy(float)
        hi = lf["high"].to_numpy(float); lo = lf["low"].to_numpy(float)
        cl = lf["close"].to_numpy(float)
        e9 = lf["e9"].to_numpy(); e89 = lf["e89"].to_numpy()
        e200 = lf["e200"].to_numpy(); la = lf["atr"].to_numpy()
        long_regime = e9 > e89
        nxt = GOV_NEXT[lens]
        if nxt is not None:
            nf = frames[nxt]
            idxn = asof_idx(o, nf["open_time"].to_numpy(np.int64), nxt)
            e200n = nf["e200"].to_numpy()[np.clip(idxn, 0, None)].copy()
            e200n[idxn < 0] = np.nan
        else:
            e200n = None
        hi100 = pd.Series(hi[::-1]).rolling(100, min_periods=1).max().to_numpy()[::-1]
        lo100 = pd.Series(lo[::-1]).rolling(100, min_periods=1).min().to_numpy()[::-1]
        piv_low = pivots_strict(lo, PIVOT_L, PIVOT_R, want_low=True)
        piv_high = pivots_strict(hi, PIVOT_L, PIVOT_R, want_low=False)
        for regime, is_long, pivmask in (("long", True, piv_low),
                                         ("short", False, piv_high)):
            in_regime = long_regime if is_long else (~long_regime)
            src = np.nonzero(pivmask)[0]
            src = src[src + PIVOT_R < n]
            src = src[in_regime[src]]
            price_all = lo if is_long else hi
            valid = (np.isfinite(la) & (la > 0) & np.isfinite(e89)
                     & np.isfinite(e200))
            src = src[valid[src]]
            if len(src) == 0:
                continue
            for i in src:
                ci = i + PIVOT_R
                p = price_all[i]; a = la[i]
                d89 = abs(p - e89[i]) / a; d200 = abs(p - e200[i]) / a
                dnp = (abs(p - e200n[i]) / a
                       if (e200n is not None and np.isfinite(e200n[i])) else None)
                p0 = opn[ci]
                fav = (hi100[ci] - p0) if is_long else (p0 - lo100[ci])
                rows.append({
                    "asset": sym, "lens": lens, "regime": regime,
                    "kind": "terminus", "ts": int(o[i]),
                    "dist_e89_atr": round(float(d89), R6),
                    "dist_e200_atr": round(float(d200), R6),
                    "dist_lensp1_e200_atr": (round(float(dnp), R6)
                                             if dnp is not None else None),
                    "near_e89": bool(d89 <= Z2_BAND_ATR),
                    "near_e200": bool(d200 <= Z2_BAND_ATR),
                    "near_any": bool(min(d89, d200) <= Z2_BAND_ATR),
                    "fwd_mfe_atr_100": round(float(fav / a), R6),
                    "fwd_mfe_bps_100": round(float(fav / p0 * 1e4), R6),
                    "trunc": bool(fwd_avail(ci, 100, n) < 100)})
            pool = np.nonzero(in_regime & valid)[0]
            n_null = NULL_MULT * len(src)
            if len(pool) == 0 or n_null == 0:
                continue
            sel = pool[rng.integers(0, len(pool), size=n_null)]
            for s_i, i in enumerate(sel):
                p = cl[i]; a = la[i]
                d89 = abs(p - e89[i]) / a; d200 = abs(p - e200[i]) / a
                dnp = (abs(p - e200n[i]) / a
                       if (e200n is not None and np.isfinite(e200n[i])) else None)
                rows.append({
                    "asset": sym, "lens": lens, "regime": regime,
                    "kind": "null", "ts": int(o[i]), "sample_i": int(s_i),
                    "dist_e89_atr": round(float(d89), R6),
                    "dist_e200_atr": round(float(d200), R6),
                    "dist_lensp1_e200_atr": (round(float(dnp), R6)
                                             if dnp is not None else None),
                    "near_e89": bool(d89 <= Z2_BAND_ATR),
                    "near_e200": bool(d200 <= Z2_BAND_ATR),
                    "near_any": bool(min(d89, d200) <= Z2_BAND_ATR)})
    return rows


# ----------------------------------------------------------------------------
# Emission
# ----------------------------------------------------------------------------
def write_jsonl(path: Path, rows: list, keyfn) -> str:
    rows = sorted(rows, key=keyfn)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        for r in rows:
            f.write(json.dumps(r, sort_keys=True, separators=(",", ":")) + "\n")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run2", action="store_true")
    args = ap.parse_args()
    root = ROOT / "research_outputs" / ("census_run2" if args.run2 else "census")
    root.mkdir(parents=True, exist_ok=True)

    from engine.data import cache_dir
    klines = cache_dir() / "klines"
    assets_env = os.environ.get("CENSUS_ASSETS")
    assets = (assets_env.split(",") if assets_env else list(ASSET_STARTS))

    t0 = time.time()
    agg = {"outcomes": [], "continuation": [], "ladder": [], "termini": []}
    per_asset_N = {}
    for sym in assets:
        r = census_asset(klines, sym, print)
        for k in agg:
            agg[k].extend(r[k])
        per_asset_N[sym] = r["N"]

    shas = {}
    shas["census_outcomes.jsonl"] = write_jsonl(
        root / "census_outcomes.jsonl", agg["outcomes"],
        lambda r: (r["asset"], r["tf"], r["cross_type"], r["dir"], r["ts"]))
    shas["continuation.jsonl"] = write_jsonl(
        root / "continuation.jsonl", agg["continuation"],
        lambda r: (r["asset"], r["exec_ts"]))
    shas["census_ladder.jsonl"] = write_jsonl(
        root / "census_ladder.jsonl", agg["ladder"],
        lambda r: (r["asset"], r["init_tf"], r["dir"], r["init_ts"]))
    shas["census_termini.jsonl"] = write_jsonl(
        root / "census_termini.jsonl", agg["termini"],
        lambda r: (r["lens"], r["regime"], r["kind"], r["asset"], r["ts"],
                   r.get("sample_i", -1)))

    manifest = {
        "phase": "CENSUS-1 build (trade-independent, measure-only)",
        "contract": "Census_1_MTF_Signal_Stack_Builder_Contract.md + Amendment 1",
        "engine_version_note": "engine 1.0.11 byte-untouched; imports indicators only",
        "window": {"assets": ASSET_STARTS, "ceiling_ms": CEIL_MS,
                   "ceiling": "2024-07-01T00:00:00Z (exploration-classic)"},
        "params": {"tfs": TFS, "ema": [LEN_FAST, LEN_SLOW, LEN_TREND],
                   "atr_len": ATR_LEN, "horizons": HORIZONS,
                   "regime_cap": REGIME_CAP, "governors": GOVERNORS,
                   "ribbon_sep_atr": RIBBON_SEP_ATR,
                   "nopullback_lookback": NOPULLBACK_LOOKBACK,
                   "pivot": [PIVOT_L, PIVOT_R], "null_seed": NULL_SEED,
                   "null_mult": NULL_MULT, "z2_band_atr": Z2_BAND_ATR,
                   "bootstrap_seed": BOOTSTRAP_SEED},
        "assets_run": assets, "per_asset_exec_bars": per_asset_N,
        "row_counts": {k: len(v) for k, v in agg.items()},
        "sha256": shas,
        "elapsed_s": round(time.time() - t0, 1),
    }
    (root / "build_manifest.json").write_text(
        json.dumps(manifest, indent=1, sort_keys=True) + "\n",
        encoding="utf-8", newline="\n")
    print(f"\nBUILD done -> {root.name} in {time.time()-t0:.1f}s")
    for k, v in shas.items():
        print(f"  {k:26} {v[:16]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
