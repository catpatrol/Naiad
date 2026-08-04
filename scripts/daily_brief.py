#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The Naiad Daily Brief generator — Atlas-styled HTML + machine-readable JSON.

Contracts (both govern; the amendment wins on conflict):
  prompts/Daily_Brief_Builder_Contract.md          (ratified 2026-07-26)
  prompts/Daily_Brief_Contract_Amendment_1.md      (ratified 2026-07-26, D1-D6)

OPS artifact, Tier-0. Decision support for discretionary trading.

THE FIREWALL (contract section 1 + amendment A1.1), enforced structurally:
  1. Consumes live/current data. Legitimate for operations, FORBIDDEN as study
     evidence. Nothing here may seed an engine rule or a pre-registration.
  2. Never reads trade journals; never computes signal-outcome or trade-outcome
     statistics on any window. Market state only, never strategy performance.
  3. Engine modules are imported READ-ONLY. signals.py / trading.py / cells.py
     are not modified, and no config is written.
  4. HYPOTHESIS-MINE CLAUSE: the archive (daily JSON + brief_index.jsonl) is an
     operations journal. It MAY be mined for hypotheses; a resulting rule change
     enters the study only through G-7 on exploration-classic data. The archive
     is never a scoring window, and radar-outcome tracking stays prohibited.

TWO DISCLOSED READINGS (builder, 2026-07-26) — see the report and NOTE_* below:
  NOTE_SIGNALS  Contract 1.3 says signals are reached "via the replay path with
                trading disabled". run_replay() unconditionally WRITES a journal
                (engine/replay.py write_journal), and this build's write
                authorization covers only the A1.8 deliverables — writing
                live-data journal rows into the estate is exactly what the
                firewall forbids. So the signal layer is invoked directly:
                compute_signals() on cached klines, with the trading layer
                never imported (F-B5 asserts this). That satisfies section 3.10
                ("trading.enabled=false") more strictly than a disabled flag.
  NOTE_WARMUP   The warm-up anchor and the (5,5) pivot helper are re-implemented
                here, byte-for-byte in formula, rather than imported from
                engine/replay.py and engine/s1.py — importing either pulls in
                engine.trading transitively. Cited at each definition.

Run:  .venv/Scripts/python.exe scripts/daily_brief.py            (real day)
      .venv/Scripts/python.exe scripts/daily_brief.py --fixture  (frozen day)
      .venv/Scripts/python.exe scripts/daily_brief.py --fixtures-only
"""

import argparse
import hashlib
import html as html_mod
import json
import os
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# Read-only engine imports. Deliberately NOT engine.replay / engine.s1 /
# engine.trading / engine.journal (see NOTE_WARMUP; F-B5 audits this list).
from engine import data as dl                                    # noqa: E402
from engine import indicators as ind                             # noqa: E402
from engine.cells import INTERVAL_MS, MTF_SET, SYMBOLS, Cell     # noqa: E402
from engine.config import load_config                            # noqa: E402
from engine.htf import map_htf_to_exec, take, take_bool          # noqa: E402
from engine.signals import compute_signals                       # noqa: E402
from engine.version import ENGINE_VERSION                        # noqa: E402

# D-3 (reviewer ruling 2026-08-03): one resample implementation, one closure
# rule.  See `resample` below for the disclosed value shift.
from analytics import structure as S                             # noqa: E402

SCRIPT_VERSION = "1.1.0"
RULES_VERSION = "1.1.0"
CONFIG_ID = "v11_faithful"        # D2: v11 semantics only, no v12 study content

OUT_DIR = ROOT / "research_outputs" / "brief"
INDEX_PATH = OUT_DIR / "brief_index.jsonl"
FIXTURE_DIR = ROOT / "tests" / "brief_fixture"

DAY_MS = 86_400_000
EXTRA_MS = {"30m": 1_800_000, "2h": 7_200_000, "8h": 28_800_000, "1d": DAY_MS}
ALL_MS = {**INTERVAL_MS, **EXTRA_MS}

# ── Lens definitions (amendment A1.2). The 1h lens is the TC-5-ratified triple
# (gov 1h / exec 5m / align 1h — configs/tc5_btc.json, tc5_runner.py align
# ruling); 4h and 12h are the frozen swing/position mandates, native. Built by
# constructing engine.cells.Cell directly — the tc5_runner.py monkey-patch
# precedent without needing the patch, since Cell is a public frozen dataclass.
LENSES = {
    "1h":  {"framing": "intraday", "gov": "1h",  "exec": "5m",  "align": "1h"},
    "4h":  {"framing": "swing",    "gov": "4h",  "exec": "5m",  "align": "1h"},
    "12h": {"framing": "position", "gov": "12h", "exec": "15m", "align": "4h"},
}
GOV_BARS_REPORT = 400        # contract 3.10: trailing ~400 governor bars

# ── Placeholders, re-ratified after ~1 week of use (A1.2 D3) ──
WATCH_PROXIMITY_GOV_ATR = 1.0
POST_X_WINDOW_GOV_BARS = 10
DEFENSE_WINDOW_EXEC_BARS = 12

VP_BINS = 200                # printed in the rules header
TPO_BINS = 100
VALUE_AREA = 0.70
NAKED_POC_DAYS = 90
POI_CAP = 12

# ── Confluence dictionary — EXACTLY these 18 (A1.4). Changing this list
# requires a contract amendment AND a rules_version bump; archive
# comparability depends on it. ──
CONFLUENCE_FLAGS = [
    "above_M_vwap", "above_Y_vwap", "in_prior_day_value", "above_VAH",
    "below_VAL", "naked_poc_above_1atr", "naked_poc_below_1atr",
    "rsi4h_bull_side", "rsi12h_bull_side", "rsi_div_bear_active",
    "rsi_div_bull_active", "funding_p90_plus", "funding_p10_minus",
    "gov4h_long_regime", "gov12h_long_regime", "stage2_4h",
    "compression_flag", "oi_surge_p90",
]

POI_SEVERITY = {           # fixed ranking table, printed in the JSON
    "POI-3": 1, "POI-1": 2, "POI-7": 3, "POI-2": 4,
    "POI-4": 5, "POI-6": 6, "POI-5": 7, "POI-8": 8,
}
POI_RULES = {
    "POI-1": "funding percentile >=90 or <=10",
    "POI-2": "RSI divergence (regular or hidden) on 4h or above",
    "POI-3": "naked POC within 1.0 daily-ATR of price",
    "POI-4": "price crossed an anchored VWAP (M/Q/Y) within the last 24h",
    "POI-5": "compression flag >=5 consecutive days",
    "POI-6": "session extension >1.5x the 20d median session range",
    "POI-7": "OI 24h-change percentile >=90 (Tier-2; degrades)",
    "POI-8": "radar state changed vs the previous index line",
}

STALENESS_TABLE = {         # A1.6(c): layer -> native reference TF
    "structure": "1d", "volume_profile": "1m", "tpo": "30m", "vwap": "1h",
    "rsi": "1h", "volatility": "1d", "funding": "8h", "sessions": "1h",
    "btc_beta": "1d", "governor": "gov_tf", "radar": "gov_tf",
    "points_of_interest": "1d", "tier2": "1h",
}

VERDICT_BANDS = ["Short", "Lean-short", "Neutral-mixed", "Lean-long", "Long"]
DOCTRINE_CHIP = 'playbook 5.5: "half size, Z1/Z2 only, grade <= B"'

PALETTE = {"ink": "#0E1420", "panel": "#151D2C", "rule": "#26324C",
           "tx": "#C9D4E6", "mute": "#7A8AA5", "warn": "#E8853F",
           "ok": "#54C6A0"}


# ══════════════════════════════════════════════════════════ small utilities

def iso(ms):
    if ms is None:
        return None
    return datetime.fromtimestamp(int(ms) / 1000, timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ")


def day_floor(ms):
    return (int(ms) // DAY_MS) * DAY_MS


def f(x, nd=8):
    """JSON-safe float: NaN/inf/None -> None, else rounded (never -0.0)."""
    if x is None:
        return None
    try:
        v = float(x)
    except (TypeError, ValueError):
        return None
    if not np.isfinite(v):
        return None
    return round(v, nd) + 0.0


def bps(a, b):
    """Signed distance a-b in basis points of b."""
    if a is None or b is None or not np.isfinite(a) or not np.isfinite(b) or b == 0:
        return None
    return (a - b) / abs(b) * 1e4


def pct_rank(series, value):
    """Percentile of `value` within `series` (0-100), NaN-safe."""
    s = np.asarray(series, dtype=float)
    s = s[np.isfinite(s)]
    if not len(s) or value is None or not np.isfinite(value):
        return None
    return float((s <= value).sum()) / len(s) * 100.0


def pivots(x, L, R, low):
    """Strict (L,R) pivot extremes -> (confirm_bars, values).

    NOTE_WARMUP: formula-identical to engine/s1.py:100-110 (_pivots), inlined so
    the brief never imports engine.s1 (which pulls in engine.trading).
    """
    s = pd.Series(x)
    left = (s.rolling(L, min_periods=L).min() if low
            else s.rolling(L, min_periods=L).max()).shift(1).to_numpy()
    right = (s.rolling(R, min_periods=R).min() if low
             else s.rolling(R, min_periods=R).max()).shift(-R).to_numpy()
    with np.errstate(invalid="ignore"):
        piv = (x < left) & (x < right) if low else (x > left) & (x > right)
    p = np.flatnonzero(piv)
    return p + R, x[p]


def warmup_anchor_ms(tf_exec, tf_gov, start_ms):
    """NOTE_WARMUP: formula-identical to engine/replay.py:69-73
    (warmup_anchor_ms + month_floor_ms), inlined to avoid importing
    engine.replay (which imports engine.trading and engine.journal)."""
    need = max(2000 * INTERVAL_MS[tf_exec], 1000 * INTERVAL_MS[tf_gov])
    ms = start_ms - need - 35 * DAY_MS
    d = datetime.fromtimestamp(ms / 1000, timezone.utc)
    return int(d.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
               .timestamp() * 1000)


def resample(df, tf):
    """OHLCV resample onto a UTC-aligned grid of `tf`.  CLOSED BUCKETS ONLY.

    FINDING F-1R-B, fixed 2026-08-03 (reviewer ruling D-3).  This function used
    to be a PRIVATE pandas groupby that kept every bucket including the forming
    one, so it did not inherit Amendment 2 §1.2's closure discipline.  While the
    v1.1 brief stood alone that was merely wrong; once BRIEF-2 reads the same
    layers, two briefs disagreeing about which bar is the last closed one is the
    exact defect class Phase I-R exists to abolish.

    It now delegates to `analytics.structure.resample_ohlcv`, which emits only
    buckets PROVED closed by a bar in a strictly later bucket.  One implementation,
    one closure rule, no drift.

    DISCLOSED VALUE SHIFT.  Every resampled timeframe loses exactly one bucket --
    the forming one -- so published values move from the forming bar to the last
    CLOSED bar.  Measured 2026-08-03 across the basket:

        RSI(14)   4h   -0.61 to +0.89     12h  -6.40 to +1.19     1d  -5.98 to -1.25
        ATR(14)   1d   BTCUSDT 1,638.22 -> 1,699.80

    That is the F-AN-8c diff class and it is the correction, not a regression:
    mid-period, a resampled oscillator was reading a fraction of a period as if
    it were the whole one.
    """
    if not len(df):
        return df.copy()
    try:
        r = S.resample_ohlcv(
            df["open_time"].to_numpy(np.int64),
            df["open"].to_numpy(float), df["high"].to_numpy(float),
            df["low"].to_numpy(float), df["close"].to_numpy(float),
            df["volume"].to_numpy(float), ALL_MS[tf])
    except S.UndecidableStepError:
        # REGRESSION FIX 2026-08-03. Amendment 2 §1.2 rules that analytics
        # REFUSES an undecidable step rather than guessing, and that refusal is
        # correct and stays. What was wrong is that this caller treated it as
        # fatal: routing resample() through analytics (finding F-1R-B, cycle 3)
        # turned a degenerate one-bar slice -- which the frozen fixture day
        # contains -- into a HALT of the whole brief. F-B3 caught it; the pytest
        # suite could not, because F-B1..F-B8 run inside this script.
        #
        # A timeframe that cannot be resampled DEGRADES to empty, exactly as a
        # failed Tier-2 fetch degrades under F-B6. The refusal is preserved
        # (nothing is guessed) and the brief still renders.
        return df.iloc[0:0][["open_time", "open", "high", "low", "close",
                             "volume"]].copy()
    return pd.DataFrame({"open_time": r["open_time"], "open": r["open"],
                         "high": r["high"], "low": r["low"],
                         "close": r["close"], "volume": r["volume"]})


def rsi_wilder(close, length=14):
    """RSI(length) with Wilder smoothing, reusing the engine's RMA."""
    c = np.asarray(close, dtype=float)
    d = np.diff(c, prepend=np.nan)
    gain = np.where(np.isnan(d), np.nan, np.maximum(d, 0.0))
    loss = np.where(np.isnan(d), np.nan, np.maximum(-d, 0.0))
    ag, al = ind.rma(gain, length), ind.rma(loss, length)
    with np.errstate(divide="ignore", invalid="ignore"):
        rs = np.where(al > 0, ag / al, np.inf)
        out = 100.0 - 100.0 / (1.0 + rs)
    out[~np.isfinite(np.asarray(ag, dtype=float))] = np.nan
    return out


# ══════════════════════════════════════════════════ volume profile / TPO

def volume_profile(df, bins=VP_BINS):
    """Uniform-spread kline volume profile (contract 3.2).

    Each bar's volume is spread uniformly across [low, high]; the profile is a
    difference of the exact per-bar CDF evaluated on bin edges, so the result is
    exact for the stated approximation (never a midpoint histogram). Provenance
    chip is `approximation`: kline method, not tick data.
    """
    if not len(df):
        return None
    lo_a = df["low"].to_numpy(float)
    hi_a = df["high"].to_numpy(float)
    v = df["volume"].to_numpy(float)
    ok = np.isfinite(lo_a) & np.isfinite(hi_a) & np.isfinite(v) & (v > 0)
    lo_a, hi_a, v = lo_a[ok], hi_a[ok], v[ok]
    if not len(v):
        return None
    lo, hi = float(lo_a.min()), float(hi_a.max())
    if not np.isfinite(lo) or not np.isfinite(hi) or hi <= lo:
        return None
    edges = np.linspace(lo, hi, bins + 1)
    span = np.where(hi_a > lo_a, hi_a - lo_a, np.nan)
    # CDF of each bar's uniform mass at every edge, summed over bars
    frac = np.clip((edges[None, :] - lo_a[:, None]) / span[:, None], 0.0, 1.0)
    zero_range = ~np.isfinite(span)
    if zero_range.any():                      # doji: all mass at the first edge >= low
        idx = np.clip(np.searchsorted(edges, lo_a[zero_range], side="right") - 1,
                      0, bins - 1)
        frac[zero_range, :] = 0.0
        for row, j in zip(np.flatnonzero(zero_range), idx):
            frac[row, j + 1:] = 1.0
    cdf = (frac * v[:, None]).sum(axis=0)
    prof = np.diff(cdf)
    total = prof.sum()
    if total <= 0:
        return None
    centers = (edges[:-1] + edges[1:]) / 2.0
    poc_i = int(np.argmax(prof))
    # value area: grow from the POC, always taking the richer neighbour
    lo_i = hi_i = poc_i
    acc = prof[poc_i]
    while acc < VALUE_AREA * total and (lo_i > 0 or hi_i < bins - 1):
        down = prof[lo_i - 1] if lo_i > 0 else -1.0
        up = prof[hi_i + 1] if hi_i < bins - 1 else -1.0
        if up >= down:
            hi_i += 1
            acc += prof[hi_i]
        else:
            lo_i -= 1
            acc += prof[lo_i]
    return {"poc": f(centers[poc_i], 8), "vah": f(edges[hi_i + 1], 8),
            "val": f(edges[lo_i], 8), "range_low": f(lo, 8), "range_high": f(hi, 8),
            "bin_width": f((hi - lo) / bins, 10), "bins": bins,
            "value_area_fraction": VALUE_AREA,
            "volume_total": f(total, 4), "bars": int(len(v)),
            "method": "uniform-spread kline CDF", "provenance": "approximation"}


def tpo_profile(df, tf="30m", bins=TPO_BINS):
    """30m-bracket TPO profile with a 70% value area (contract 3.3)."""
    b = resample(df, tf)
    if not len(b):
        return None
    lo_a, hi_a = b["low"].to_numpy(float), b["high"].to_numpy(float)
    lo, hi = float(np.nanmin(lo_a)), float(np.nanmax(hi_a))
    if not np.isfinite(lo) or not np.isfinite(hi) or hi <= lo:
        return None
    edges = np.linspace(lo, hi, bins + 1)
    counts = np.zeros(bins)
    for a, z in zip(lo_a, hi_a):
        if not (np.isfinite(a) and np.isfinite(z)):
            continue
        i0 = np.clip(np.searchsorted(edges, a, side="right") - 1, 0, bins - 1)
        i1 = np.clip(np.searchsorted(edges, z, side="right") - 1, 0, bins - 1)
        counts[i0:i1 + 1] += 1.0
    total = counts.sum()
    if total <= 0:
        return None
    centers = (edges[:-1] + edges[1:]) / 2.0
    poc_i = int(np.argmax(counts))
    lo_i = hi_i = poc_i
    acc = counts[poc_i]
    while acc < VALUE_AREA * total and (lo_i > 0 or hi_i < bins - 1):
        down = counts[lo_i - 1] if lo_i > 0 else -1.0
        up = counts[hi_i + 1] if hi_i < bins - 1 else -1.0
        if up >= down:
            hi_i += 1
            acc += counts[hi_i]
        else:
            lo_i -= 1
            acc += counts[lo_i]
    return {"poc": f(centers[poc_i], 8), "vah": f(edges[hi_i + 1], 8),
            "val": f(edges[lo_i], 8), "brackets": int(len(b)),
            "bracket_tf": tf, "bins": bins, "provenance": "approximation"}


def naked_pocs(df_days, now_ms, days=NAKED_POC_DAYS):
    """Untested daily POCs over the trailing window (contract 3.2).

    A POC is 'naked' while no LATER bar's range has traded through it.
    """
    today = day_floor(now_ms)
    start = today - days * DAY_MS
    d = df_days[df_days["open_time"] >= start]
    if not len(d):
        return []
    # Only COMPLETED days can carry an untested POC: the current day's POC has
    # no later bars to be tested against, so it would be trivially 'naked'.
    day_ids = [x for x in np.unique((d["open_time"].to_numpy(np.int64) // DAY_MS)
                                    * DAY_MS) if x < today]
    out = []
    for day in day_ids:
        sl = d[(d["open_time"] >= day) & (d["open_time"] < day + DAY_MS)]
        vp = volume_profile(sl, bins=VP_BINS)
        if vp is None or vp["poc"] is None:
            continue
        later = d[d["open_time"] >= day + DAY_MS]
        if len(later):
            touched = bool(((later["low"].to_numpy(float) <= vp["poc"]) &
                            (later["high"].to_numpy(float) >= vp["poc"])).any())
        else:
            touched = False
        if not touched:
            out.append({"day": iso(int(day))[:10], "poc": vp["poc"]})
    return out


# ══════════════════════════════════════════════════════════ VWAP complex

def vwap_series(df1h, mask=None):
    """Volume-weighted mean of typical price (H+L+C)/3 with a 1-sigma band.

    A1.6(d): ALL rolling and anchored VWAPs are computed on 1h klines, typical
    price, volume-weighted. Pinned.
    """
    d = df1h if mask is None else df1h[mask]
    if not len(d):
        return None, None
    tp = (d["high"].to_numpy(float) + d["low"].to_numpy(float)
          + d["close"].to_numpy(float)) / 3.0
    v = d["volume"].to_numpy(float)
    ok = np.isfinite(tp) & np.isfinite(v) & (v > 0)
    if not ok.any():
        return None, None
    tp, v = tp[ok], v[ok]
    w = v.sum()
    if w <= 0:
        return None, None
    mean = float((tp * v).sum() / w)
    var = float((v * (tp - mean) ** 2).sum() / w)
    return mean, float(np.sqrt(max(var, 0.0)))


def anchor_starts(now_ms):
    """UTC period-open anchors for W/M/Q/Y (contract 3.4)."""
    d = datetime.fromtimestamp(now_ms / 1000, timezone.utc)
    week = d - timedelta(days=d.weekday())
    week = week.replace(hour=0, minute=0, second=0, microsecond=0)
    month = d.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    quarter = month.replace(month=((d.month - 1) // 3) * 3 + 1)
    year = month.replace(month=1)
    return {k: int(v.timestamp() * 1000) for k, v in
            (("W", week), ("M", month), ("Q", quarter), ("Y", year))}


def vwap_complex(df1h, now_ms, price):
    ot = df1h["open_time"].to_numpy(np.int64)
    out = {"rolling": {}, "anchored": {}, "provenance": "computed",
           "basis": "1h klines, typical price (H+L+C)/3, volume-weighted"}
    for days in (7, 30, 90, 365):
        m = ot >= now_ms - days * DAY_MS
        mean, sd = vwap_series(df1h, m)
        out["rolling"][f"{days}d"] = {
            "vwap": f(mean), "sigma": f(sd),
            "upper_1sigma": f(None if mean is None else mean + sd),
            "lower_1sigma": f(None if mean is None else mean - sd),
            "distance_bps": f(bps(price, mean), 2), "bars": int(m.sum())}
    for name, a in anchor_starts(now_ms).items():
        m = ot >= a
        mean, sd = vwap_series(df1h, m)
        out["anchored"][name] = {
            "anchor_utc": iso(a), "vwap": f(mean), "sigma": f(sd),
            "upper_1sigma": f(None if mean is None else mean + sd),
            "lower_1sigma": f(None if mean is None else mean - sd),
            "distance_bps": f(bps(price, mean), 2), "bars": int(m.sum())}
    return out


def anchored_vwap_cross_24h(df1h, now_ms):
    """POI-4: did price cross an anchored M/Q/Y VWAP in the last 24h?

    The anchored VWAP is re-evaluated at each of the last 24 hourly closes, so
    the crossing test uses the level as it actually stood on that bar.
    """
    ot = df1h["open_time"].to_numpy(np.int64)
    close = df1h["close"].to_numpy(float)
    hits = []
    for name, a in anchor_starts(now_ms).items():
        if name == "W":
            continue
        idx = np.flatnonzero((ot >= now_ms - DAY_MS) & (ot <= now_ms))
        prev_side = None
        for i in idx:
            mean, _ = vwap_series(df1h, (ot >= a) & (ot <= ot[i]))
            if mean is None or not np.isfinite(close[i]):
                continue
            side = 1 if close[i] > mean else -1
            if prev_side is not None and side != prev_side:
                hits.append({"anchor": name, "at_utc": iso(int(ot[i])),
                             "level": f(mean), "direction":
                             "up" if side > 0 else "down"})
            prev_side = side
    return hits


# ══════════════════════════════════════════════════════════ other layers

def structure_layer(df1d, df1h, now_ms, price):
    """Pivots (5,5) + prior D/W/M ranges + W/M/Q/Y opens (contract 3.1)."""
    lo = df1d["low"].to_numpy(float)
    hi = df1d["high"].to_numpy(float)
    pl_c, pl_v = pivots(lo, 5, 5, low=True)
    ph_c, ph_v = pivots(hi, 5, 5, low=False)
    days = df1d["open_time"].to_numpy(np.int64)
    today = day_floor(now_ms)

    def period_range(start, end):
        m = (days >= start) & (days < end)
        if not m.any():
            return None, None
        return f(float(df1d["high"].to_numpy(float)[m].max())), \
            f(float(df1d["low"].to_numpy(float)[m].min()))

    pd_hi, pd_lo = period_range(today - DAY_MS, today)
    a = anchor_starts(now_ms)
    prev_week = a["W"] - 7 * DAY_MS
    pw_hi, pw_lo = period_range(prev_week, a["W"])
    prev_month_end = a["M"]
    pm_start = int((datetime.fromtimestamp(a["M"] / 1000, timezone.utc)
                    - timedelta(days=1)).replace(
                        day=1, hour=0, minute=0, second=0,
                        microsecond=0).timestamp() * 1000)
    pm_hi, pm_lo = period_range(pm_start, prev_month_end)

    opens = {}
    ot1h = df1h["open_time"].to_numpy(np.int64)
    o1h = df1h["open"].to_numpy(float)
    for name, anc in a.items():
        j = np.flatnonzero(ot1h >= anc)
        opens[name] = {"level": f(float(o1h[j[0]])) if len(j) else None,
                       "anchor_utc": iso(anc)}
        if opens[name]["level"] is not None:
            opens[name]["distance_bps"] = f(bps(price, opens[name]["level"]), 2)

    def last_pivots(conf, vals, n=3):
        out = []
        for k in range(1, min(n, len(vals)) + 1):
            out.append({"level": f(float(vals[-k])),
                        "day": iso(int(days[min(len(days) - 1,
                                                int(conf[-k]) - 5)]))[:10],
                        "distance_bps": f(bps(price, float(vals[-k])), 2)})
        return out

    return {"provenance": "computed", "pivot_convention": "pivot(5,5) on 1d",
            "pivot_lows": last_pivots(pl_c, pl_v),
            "pivot_highs": last_pivots(ph_c, ph_v),
            "prior_day": {"high": pd_hi, "low": pd_lo},
            "prior_week": {"high": pw_hi, "low": pw_lo},
            "prior_month": {"high": pm_hi, "low": pm_lo},
            "period_opens": opens}


def rsi_layer(df1h, price):
    """MTF RSI(14, Wilder) + regular/hidden divergences (contract 3.5)."""
    out = {"provenance": "computed", "length": 14, "method": "Wilder",
           "timeframes": {}}
    for tf in ("1h", "2h", "4h", "12h", "1d"):
        b = df1h if tf == "1h" else resample(df1h, tf)
        if len(b) < 40:
            out["timeframes"][tf] = {"value": None, "note": "insufficient history"}
            continue
        r = rsi_wilder(b["close"].to_numpy(float), 14)
        val = r[-1]
        prev = r[-2] if len(r) > 1 else np.nan
        div = divergences(b, r)
        out["timeframes"][tf] = {
            "value": f(val, 4), "side": ("bull" if np.isfinite(val) and val > 50
                                         else "bear" if np.isfinite(val) else None),
            "slope": f(val - prev, 4),
            "bars": int(len(b)),
            "last_bar_utc": iso(int(b["open_time"].iloc[-1])),
            "divergences": div}
    return out


def divergences(b, r):
    """Regular + hidden divergence via price-pivot vs RSI-pivot, pivot(5,5),
    last 2 pivot pairs per TF (contract 3.5)."""
    lo = b["low"].to_numpy(float)
    hi = b["high"].to_numpy(float)
    out = []
    for low_side in (True, False):
        pc, _ = pivots(lo if low_side else hi, 5, 5, low=low_side)
        rc, _ = pivots(r, 5, 5, low=low_side)
        pc = [int(i) - 5 for i in pc if 0 <= int(i) - 5 < len(r)]
        rc = [int(i) - 5 for i in rc if 0 <= int(i) - 5 < len(r)]
        if len(pc) < 2:
            continue
        for k in (1, 2):
            if len(pc) < k + 1:
                break
            i1, i0 = pc[-k], pc[-k - 1]
            px1, px0 = (lo[i1], lo[i0]) if low_side else (hi[i1], hi[i0])
            r1, r0 = r[i1], r[i0]
            if not all(np.isfinite(x) for x in (px1, px0, r1, r0)):
                continue
            kind = None
            if low_side:
                if px1 < px0 and r1 > r0:
                    kind = "regular_bull"
                elif px1 > px0 and r1 < r0:
                    kind = "hidden_bull"
            else:
                if px1 > px0 and r1 < r0:
                    kind = "regular_bear"
                elif px1 < px0 and r1 > r0:
                    kind = "hidden_bear"
            if kind:
                out.append({"kind": kind, "pair": k,
                            "price_from": f(px0), "price_to": f(px1),
                            "rsi_from": f(r0, 4), "rsi_to": f(r1, 4),
                            "at_utc": iso(int(b["open_time"].iloc[i1]))})
    return out


def volatility_layer(data, now_ms):
    """ATR(14) percentile vs 1y per TF + RV 7d/30d ratio (contract 3.6)."""
    out = {"provenance": "computed", "atr_percentile_vs_1y": {}}
    for tf in ("1h", "4h", "12h", "1d"):
        b = data.get(tf)
        if b is None or not len(b):
            continue
        a = ind.atr(b["high"].to_numpy(float), b["low"].to_numpy(float),
                    b["close"].to_numpy(float), 14)
        ot = b["open_time"].to_numpy(np.int64)
        hist = a[ot >= now_ms - 365 * DAY_MS]
        out["atr_percentile_vs_1y"][tf] = {
            "atr": f(a[-1]), "percentile": f(pct_rank(hist, a[-1]), 2),
            "sample_bars": int(np.isfinite(hist).sum())}
    d1 = data["1d"]
    c = d1["close"].to_numpy(float)
    ret = np.diff(np.log(c))
    rv7 = float(np.nanstd(ret[-7:])) if len(ret) >= 7 else np.nan
    rv30 = float(np.nanstd(ret[-30:])) if len(ret) >= 30 else np.nan
    ratio = rv7 / rv30 if np.isfinite(rv7) and np.isfinite(rv30) and rv30 > 0 else np.nan
    flag = ("expansion" if np.isfinite(ratio) and ratio > 1.2 else
            "compression" if np.isfinite(ratio) and ratio < 0.8 else "neutral")
    # consecutive compression days (POI-5): recompute the ratio day by day
    streak = 0
    for k in range(0, 30):
        e = len(ret) - k
        if e < 30:
            break
        a7 = float(np.nanstd(ret[e - 7:e]))
        a30 = float(np.nanstd(ret[e - 30:e]))
        if np.isfinite(a7) and np.isfinite(a30) and a30 > 0 and a7 / a30 < 0.8:
            streak += 1
        else:
            break
    out.update({"rv_7d": f(rv7, 8), "rv_30d": f(rv30, 8),
                "rv_ratio_7_30": f(ratio, 6), "regime_flag": flag,
                "compression_streak_days": streak,
                "expansion_threshold": 1.2, "compression_threshold": 0.8})
    return out


def funding_layer(fund, now_ms):
    """Funding posture off actual timestamped records (contract 2 + 3.7)."""
    if fund is None or not len(fund):
        return {"provenance": "computed", "note": "no funding records"}
    t = fund["funding_time"].to_numpy(np.int64)
    r = fund["funding_rate"].to_numpy(float)
    cur = float(r[-1])
    m7 = t >= now_ms - 7 * DAY_MS
    recent = t[m7]
    gaps = np.diff(np.sort(recent)) if len(recent) > 1 else np.array([])
    grid = sorted({int(round(g / 3_600_000)) for g in gaps}) if len(gaps) else []
    return {"provenance": "computed",
            "current": f(cur, 10), "current_at_utc": iso(int(t[-1])),
            "mean_7d": f(float(np.nanmean(r[m7])) if m7.any() else None, 10),
            "records_7d": int(m7.sum()),
            "observed_grid_hours_7d": grid,
            "percentile_vs_full_history": f(pct_rank(r, cur), 2),
            "history_records": int(len(r)),
            "history_first_utc": iso(int(t[0])),
            "integration": "per-record timestamps; never assumed 8h x 3/day"}


def sessions_layer(df1h, now_ms):
    """Asia/London/NY ranges, conventions printed (contract 3.8)."""
    windows = {"asia": (0, 8), "london": (7, 16), "ny": (13, 22)}
    today = day_floor(now_ms)
    ot = df1h["open_time"].to_numpy(np.int64)
    hi = df1h["high"].to_numpy(float)
    lo = df1h["low"].to_numpy(float)
    hours = (ot % DAY_MS) // 3_600_000      # UTC hour-of-day, vectorized
    out = {"provenance": "computed",
           "convention_utc": {k: f"{a:02d}-{b:02d}" for k, (a, b) in windows.items()},
           "day_utc": iso(today)[:10], "sessions": {}}
    day_m = (ot >= today) & (ot < today + DAY_MS)
    ranges = {}
    for name, (a, b) in windows.items():
        m = day_m & (hours >= a) & (hours < b)
        if not m.any():
            out["sessions"][name] = {"high": None, "low": None, "range": None}
            continue
        h, l = float(hi[m].max()), float(lo[m].min())
        ranges[name] = h - l
        out["sessions"][name] = {"high": f(h), "low": f(l), "range": f(h - l),
                                 "bars": int(m.sum())}
    out["driver"] = max(ranges, key=ranges.get) if ranges else None
    # 20d median of the day's full range, for POI-6
    med = []
    for k in range(1, 21):
        d0 = today - k * DAY_MS
        m = (ot >= d0) & (ot < d0 + DAY_MS)
        if m.any():
            med.append(float(hi[m].max()) - float(lo[m].min()))
    day_m_any = day_m.any()
    day_range = (float(hi[day_m].max()) - float(lo[day_m].min())) if day_m_any else None
    median20 = float(np.median(med)) if med else None
    out.update({"day_range": f(day_range), "median_day_range_20d": f(median20),
                "extension_ratio": f(day_range / median20, 4)
                if day_range and median20 else None,
                "extension_threshold": 1.5})
    return out


def beta_layer(df1d, btc1d):
    """30d correlation + beta vs BTC on daily log returns (contract 3.9)."""
    a = pd.DataFrame({"d": (df1d["open_time"].to_numpy(np.int64) // DAY_MS),
                      "c": df1d["close"].to_numpy(float)})
    b = pd.DataFrame({"d": (btc1d["open_time"].to_numpy(np.int64) // DAY_MS),
                      "c": btc1d["close"].to_numpy(float)})
    j = a.merge(b, on="d", suffixes=("_a", "_b")).tail(31)
    if len(j) < 10:
        return {"provenance": "computed", "note": "insufficient overlap"}
    ra = np.diff(np.log(j["c_a"].to_numpy(float)))
    rb = np.diff(np.log(j["c_b"].to_numpy(float)))
    if np.nanstd(rb) == 0:
        return {"provenance": "computed", "note": "degenerate BTC series"}
    corr = float(np.corrcoef(ra, rb)[0, 1])
    beta = float(np.cov(ra, rb)[0, 1] / np.var(rb))
    return {"provenance": "computed", "window_days": int(len(ra)),
            "correlation_30d": f(corr, 6), "beta_30d": f(beta, 6),
            "basis": "daily log returns vs BTCUSDT"}


# ═════════════════════════════════════ layers 10 + 11 — governor & radar

def run_lens(symbol, lens_key, cfg, klines, now_ms):
    """One signal run (trading layer never invoked — NOTE_SIGNALS).

    Returns the SignalResult plus the governor series the radar needs. Zone and
    band edges are recomputed here from the SAME primitives and parameters the
    signal layer uses (engine/signals.py:128-160): ind.ema on governor closes,
    mapped by the confirmed-HTF rule. SignalResult exposes g_atr/g_e89 but not
    gE9/gE200, and the radar needs all four for the zone and band edges — the
    identical pattern engine/replay.py:_tc1_arch_data uses for gov_e200.
    """
    L = LENSES[lens_key]
    p = cfg["signal"]
    cell = Cell(cell_id=f"{symbol}_brief_{lens_key}", symbol=symbol,
                mandate=L["framing"], tf_gov=L["gov"], tf_exec=L["exec"],
                tf_align=L["align"], slippage_bps=0.0)

    gov_step = INTERVAL_MS[L["gov"]]
    window_start = now_ms - GOV_BARS_REPORT * gov_step
    anchor = warmup_anchor_ms(L["exec"], L["gov"], window_start)

    def slice_tf(tf):
        d = klines[tf]
        return d[(d["open_time"] >= anchor) & (d["open_time"] <= now_ms)] \
            .reset_index(drop=True)

    exec_df = slice_tf(L["exec"])
    gov_df = slice_tf(L["gov"])
    mtf = {tf: slice_tf(tf) for tf in MTF_SET}
    if len(exec_df) < 300 or len(gov_df) < 60:
        return None

    sig = compute_signals(cell, p, exec_df, gov_df, mtf,
                          v_births_provisional=p["v_births_provisional"])

    # governor tuple, recomputed exactly as signals.py does
    gc = gov_df["close"].to_numpy(float)
    gh, gl = gov_df["high"].to_numpy(float), gov_df["low"].to_numpy(float)
    gidx = map_htf_to_exec(sig.exec_open_ms,
                           gov_df["open_time"].to_numpy(np.int64), L["gov"])
    gE9 = take(ind.ema(gc, p["len_fast"]), gidx)
    gE89 = take(ind.ema(gc, p["len_slow"]), gidx)
    gE200 = take(ind.ema(gc, p["len_trend"]), gidx)
    gATR = take(ind.atr(gh, gl, gc, p["atr_len"]), gidx)
    gS2B = take_bool(ind.ema(gc, p["len_slow"]) > ind.ema(gc, p["len_trend"]), gidx)
    gS2S = take_bool(ind.ema(gc, p["len_slow"]) < ind.ema(gc, p["len_trend"]), gidx)

    # internal consistency: our recomputation must match what the engine returned
    for name, mine, theirs in (("g_atr", gATR, sig.g_atr), ("g_e89", gE89, sig.g_e89)):
        m = np.isfinite(mine) & np.isfinite(theirs)
        if m.any() and not np.allclose(mine[m], theirs[m], rtol=0, atol=0):
            raise AssertionError(
                f"{symbol}/{lens_key}: recomputed {name} differs from SignalResult")

    return {"cell": cell, "lens": lens_key, "sig": sig, "params": p,
            "gov_open_ms": gov_df["open_time"].to_numpy(np.int64),
            "gE9": gE9, "gE89": gE89, "gE200": gE200, "gATR": gATR,
            "gS2B": gS2B, "gS2S": gS2S,
            "window_start_ms": int(window_start), "anchor_ms": int(anchor),
            "exec_bars": int(len(exec_df)), "gov_bars": int(len(gov_df)),
            "last_bar_utc": iso(int(sig.exec_open_ms[-1]))}


def zone_bands(run, i):
    """Armed-band geometry at exec bar i, per engine/signals.py:157-160 and the
    v11.0.2 arming rules (Z1/Z2 with every live campaign incl. provisional when
    prov_zones=Z1+Z2; Z3 only when stage-aligned)."""
    p, sig = run["params"], run["sig"]
    gATR, gE9, gE89 = run["gATR"][i], run["gE9"][i], run["gE89"][i]
    band_top = max(run["gE89"][i], run["gE200"][i])
    band_bot = min(run["gE89"][i], run["gE200"][i])
    d = int(sig.dir[i])
    provisional = bool(sig.camp_counter[i])
    stage_aligned = bool(run["gS2B"][i] if d == 1 else
                         run["gS2S"][i] if d == -1 else False)
    prov_z12 = p["prov_zones"] == "Z1+Z2"
    z = {
        "Z1": {"top": gE9 + p["z1_prox"] * gATR, "bot": gE9 - p["z1_prox"] * gATR,
               "armed": d != 0},
        "Z2": {"top": gE89 + p["z2_prox"] * gATR, "bot": gE89 - p["z2_prox"] * gATR,
               "armed": d != 0 and (not provisional or prov_z12)},
        "Z3": {"top": band_top + p["z3_prox"] * gATR,
               "bot": band_bot - p["z3_prox"] * gATR,
               "armed": d != 0 and stage_aligned},
    }
    return z, band_top, band_bot, stage_aligned, provisional


def radar_row(run, poi_prev_state=None):
    """LAYER 11 — the SSv11.0.2 playbook state machine as one table row."""
    sig = run["sig"]
    i = len(sig.c) - 1
    lens = run["lens"]
    gov_step = INTERVAL_MS[LENSES[lens]["gov"]]
    price = float(sig.c[i])
    d = int(sig.dir[i])
    z, band_top, band_bot, stage_aligned, provisional = zone_bands(run, i)
    gATR = float(run["gATR"][i])

    # ── events, aged ──
    evs = [e for e in sig.events]
    last_regime = next((e for e in reversed(evs) if e.evt == "REGIME"), None)
    last_prime = next((e for e in reversed(evs) if e.evt == "PRIME"), None)
    last_any = evs[-1] if evs else None
    last_x = next((e for e in reversed(evs) if e.evt == "X"), None)
    last_tpw = next((e for e in reversed(evs) if e.evt == "TPW"), None)

    def gov_age(ev):
        if ev is None:
            return None
        return int((int(sig.exec_open_ms[i]) // gov_step)
                   - (int(sig.exec_open_ms[ev.i]) // gov_step))

    x_gov_age = gov_age(last_x)
    tpw_exec_age = (i - last_tpw.i) if last_tpw is not None else None
    cold_start = last_regime is None

    # Operator ruling 2026-07-27: an X's authority ends at the NEXT arming.
    # POST_X holds only while no campaign has armed since the X; campaign_id
    # increments on every arming/V-birth (engine/signals.py:75), so a non-zero
    # campaign_id after the X bar is proof that a fresh governor cross re-armed.
    # A live campaign therefore reports its true state, with the recent failure
    # surfaced as a caution chip rather than suppressed to stand-aside.
    armed_since_x = bool(last_x is not None
                         and (sig.campaign_id[last_x.i + 1:] != 0).any())
    x_recent = x_gov_age is not None and x_gov_age <= POST_X_WINDOW_GOV_BARS

    stop = (float(sig.stop_long[i]) if d == 1 else
            float(sig.stop_short[i]) if d == -1 else float("nan"))
    entered = bool(d != 0 and np.isfinite(stop))

    # zone occupancy: price inside an armed band (A1.2's literal ZONE_ACTIVE
    # definition). Distinct from the engine's tag memory, which is reported
    # separately as engine_tag_zone -- the radar never claims a tag occurred.
    inside = [k for k in ("Z3", "Z2", "Z1")
              if z[k]["armed"] and np.isfinite(z[k]["bot"])
              and z[k]["bot"] <= price <= z[k]["top"]]
    active = inside[0] if inside else None

    # ── the state machine (precedence order) ──
    if x_recent and not armed_since_x:
        state = "POST_X"
    elif d == 0:
        state = "DORMANT"
    elif entered and tpw_exec_age is not None and tpw_exec_age <= DEFENSE_WINDOW_EXEC_BARS:
        state = "DEFENSE"
    elif entered:
        state = "ENTERED"
    elif active:
        state = "ZONE_ACTIVE"
    else:
        state = "ARMED"

    # ── nearest armed band + distance ──
    def edge_distance(k):
        if not z[k]["armed"] or not np.isfinite(z[k]["bot"]):
            return None
        if z[k]["bot"] <= price <= z[k]["top"]:
            return 0.0
        return min(abs(price - z[k]["top"]), abs(price - z[k]["bot"]))

    dists = {k: edge_distance(k) for k in ("Z1", "Z2", "Z3")}
    dists = {k: v for k, v in dists.items() if v is not None}
    near = active or (min(dists, key=dists.get) if dists else None)
    near_d = dists.get(near) if near else None

    # ── invalidations (mandatory) ──
    setup_inval = None
    if near:
        setup_inval = z[near]["bot"] if d == 1 else z[near]["top"]
    if d == 1:
        camp_inval = band_bot
        camp_note = "far governor band edge (the X reference level)"
    elif d == -1:
        camp_inval = band_top
        camp_note = "far governor band edge (the X reference level)"
    else:
        # A1.2 makes invalidation MANDATORY on every row, but a flat row has no
        # armed zone and no direction to orient a 'far' edge. Print the nearer
        # governor band edge -- the operative X reference either way -- and
        # expose both edges so the stance is falsifiable in both directions.
        edges = [e for e in (band_top, band_bot) if np.isfinite(e)]
        camp_inval = (min(edges, key=lambda e: abs(price - e)) if edges else None)
        camp_note = ("no live campaign: nearer governor band edge printed as the "
                     "operative X reference level (both edges in "
                     "governor_band_top / governor_band_bot)")

    # ── needs-next hint ──
    if state == "POST_X":
        needs = "needs: fresh governor cross (never negotiate with an X)"
    elif state == "DORMANT":
        needs = "needs: governor cross"
    elif state == "DEFENSE":
        needs = "needs: defend or stand down per 5-7 (TPW live)"
    elif state == "ENTERED":
        needs = "needs: manage per 5-7"
    elif state == "ZONE_ACTIVE":
        needs = ("needs: stage confirm for Z3" if not stage_aligned
                 else "needs: PRIME trigger (9-EMA reclaim)")
    else:
        needs = "needs: zone tag"

    row = {
        "lens": lens, "framing": LENSES[lens]["framing"],
        "state": state, "dir": d,
        "dir_word": "long" if d == 1 else "short" if d == -1 else "flat",
        "stage": int(sig.stage[i]), "stage_aligned": stage_aligned,
        "tier": "provisional" if provisional else "full" if d != 0 else "-",
        "cold_start": cold_start,
        "price": f(price), "gov_atr": f(gATR),
        "active_zone": active, "engine_tag_zone":
            (f"Z{int(sig.active_zone[i])}" if int(sig.active_zone[i]) else None),
        "nearest_armed_zone": near,
        "zone_distance_bps": f(near_d / price * 1e4, 2)
            if near_d is not None and price else None,
        "zone_distance_gov_atr": f(near_d / gATR, 4)
            if near_d is not None and np.isfinite(gATR) and gATR > 0 else None,
        "armed_bands": {k: {"armed": bool(z[k]["armed"]), "top": f(z[k]["top"]),
                            "bot": f(z[k]["bot"])} for k in ("Z1", "Z2", "Z3")},
        "whipsaw_arrow_hidden": bool(last_regime is not None
                                     and last_regime.arrow_visible is False),
        "last_prime": None if last_prime is None else {
            "grade": last_prime.grade, "zone": last_prime.zone,
            "exec_bars_ago": int(i - last_prime.i),
            "at_utc": iso(int(sig.exec_open_ms[last_prime.i]))},
        "last_event": None if last_any is None else {
            "type": last_any.evt, "exec_bars_ago": int(i - last_any.i),
            "at_utc": iso(int(sig.exec_open_ms[last_any.i]))},
        "last_x_gov_bars_ago": x_gov_age,
        "post_x_caution": bool(x_recent and armed_since_x),
        "campaign_armed_since_last_x": armed_since_x,
        "tpw_exec_bars_ago": tpw_exec_age,
        "live_stop": f(stop) if entered else None,
        "setup_invalidation": f(setup_inval),
        "setup_invalidation_note": "active-or-nearest armed zone's far edge",
        "campaign_invalidation": f(camp_inval),
        "campaign_invalidation_note": camp_note,
        "governor_band_top": f(band_top), "governor_band_bot": f(band_bot),
        "needs_next": needs,
        "doctrine_chip": DOCTRINE_CHIP if provisional else None,
        "governor_bars": run["gov_bars"], "exec_bars": run["exec_bars"],
        "window_start_utc": iso(run["window_start_ms"]),
        "last_bar_utc": run["last_bar_utc"],
        "gov_tf": LENSES[lens]["gov"], "exec_tf": LENSES[lens]["exec"],
        "align_tf": LENSES[lens]["align"],
        "provenance": "computed",
    }
    return row


def recompute_state_independently(run):
    """F-B7: second, independent derivation of the radar state from the
    layer-10 arrays. Deliberately written as a flat re-read of SignalResult
    rather than by calling radar_row's helpers."""
    sig = run["sig"]
    i = len(sig.c) - 1
    p = run["params"]
    gov_step = INTERVAL_MS[LENSES[run["lens"]]["gov"]]
    d = int(sig.dir[i])
    price = float(sig.c[i])
    provisional = bool(sig.camp_counter[i])
    stage_ok = bool(run["gS2B"][i] if d == 1 else run["gS2S"][i] if d == -1 else False)
    atr = float(run["gATR"][i])
    bands = []
    if d != 0:
        bands.append((run["gE9"][i] - p["z1_prox"] * atr,
                      run["gE9"][i] + p["z1_prox"] * atr))
        if (not provisional) or p["prov_zones"] == "Z1+Z2":
            bands.append((run["gE89"][i] - p["z2_prox"] * atr,
                          run["gE89"][i] + p["z2_prox"] * atr))
        if stage_ok:
            bt = max(run["gE89"][i], run["gE200"][i]) + p["z3_prox"] * atr
            bb = min(run["gE89"][i], run["gE200"][i]) - p["z3_prox"] * atr
            bands.append((bb, bt))
    in_band = any(b <= price <= t for b, t in bands if np.isfinite(b))
    stop = sig.stop_long[i] if d == 1 else sig.stop_short[i] if d == -1 else np.nan
    entered = bool(d != 0 and np.isfinite(stop))
    xs = [e for e in sig.events if e.evt == "X"]
    tpws = [e for e in sig.events if e.evt == "TPW"]
    x_age = (int(sig.exec_open_ms[i]) // gov_step
             - int(sig.exec_open_ms[xs[-1].i]) // gov_step) if xs else None
    tpw_age = (i - tpws[-1].i) if tpws else None
    rearmed = bool(xs and (sig.campaign_id[xs[-1].i + 1:] != 0).any())
    if x_age is not None and x_age <= POST_X_WINDOW_GOV_BARS and not rearmed:
        return "POST_X"
    if d == 0:
        return "DORMANT"
    if entered and tpw_age is not None and tpw_age <= DEFENSE_WINDOW_EXEC_BARS:
        return "DEFENSE"
    if entered:
        return "ENTERED"
    if in_band:
        return "ZONE_ACTIVE"
    return "ARMED"


def governor_dashboard(runs):
    """LAYER 10 — the spine, one row per governor lens (contract 3.10)."""
    out = {}
    for lens, run in runs.items():
        if run is None:
            out[lens] = {"note": "insufficient history", "provenance": "computed"}
            continue
        sig = run["sig"]
        i = len(sig.c) - 1
        last_prime = next((e for e in reversed(sig.events) if e.evt == "PRIME"), None)
        last_regime = next((e for e in reversed(sig.events) if e.evt == "REGIME"), None)
        out[lens] = {
            "provenance": "computed",
            "gov_tf": LENSES[lens]["gov"], "exec_tf": LENSES[lens]["exec"],
            "align_tf": LENSES[lens]["align"], "framing": LENSES[lens]["framing"],
            "regime_dir": int(sig.dir[i]),
            "regime_word": ("long" if sig.dir[i] == 1 else
                            "short" if sig.dir[i] == -1 else "flat"),
            "stage": int(sig.stage[i]),
            "tier": "provisional" if bool(sig.camp_counter[i]) else
                    "full" if sig.dir[i] != 0 else "-",
            "engine_tag_zone": int(sig.active_zone[i]),
            "campaign_id": int(sig.campaign_id[i]),
            "gov_atr": f(run["gATR"][i]),
            "last_prime_exec_bars_ago": None if last_prime is None else int(i - last_prime.i),
            "last_prime_grade": None if last_prime is None else last_prime.grade,
            "whipsaw_arrow_hidden": bool(last_regime is not None
                                         and last_regime.arrow_visible is False),
            "exec_bars": run["exec_bars"], "governor_bars": run["gov_bars"],
            "window_start_utc": iso(run["window_start_ms"]),
            "last_bar_utc": run["last_bar_utc"],
            "config_id": CONFIG_ID, "engine_version": ENGINE_VERSION,
            "trading": "never invoked (NOTE_SIGNALS)",
        }
    return out


# ══════════════════════════════════════════════════════════════ Tier 2

def fetch_tier2(symbol, canned=None):
    """Layers 13-16, one public fetch each. Failures degrade to a stale chip."""
    if canned is not None:
        return canned
    import requests
    base = "https://fapi.binance.com"
    out = {"provenance": "fetched", "degraded": [], "fetched_utc": None}

    def get(path, params, prefix):
        try:
            r = requests.get(base + path, params=params, timeout=20)
            if r.status_code != 200:
                out["degraded"].append(f"{prefix}:HTTP{r.status_code}")
                return None
            return r.json()
        except Exception as e:                       # network/degradation path
            out["degraded"].append(f"{prefix}:{type(e).__name__}")
            return None

    oi = get("/futures/data/openInterestHist",
             {"symbol": symbol, "period": "1h", "limit": 500}, "open_interest")
    if oi:
        val = np.array([float(x["sumOpenInterest"]) for x in oi])
        out["open_interest"] = {
            "level": f(val[-1], 4), "at_utc": iso(int(oi[-1]["timestamp"])),
            "change_24h_pct": f((val[-1] / val[-25] - 1) * 100, 4) if len(val) > 25 else None,
            "change_7d_pct": f((val[-1] / val[-169] - 1) * 100, 4) if len(val) > 169 else None,
            "percentile": f(pct_rank(val, val[-1]), 2), "samples": int(len(val))}
        if len(val) > 25:
            ch = val[25:] / val[:-25] - 1.0
            out["open_interest"]["change_24h_percentile"] = f(
                pct_rank(ch, val[-1] / val[-25] - 1.0), 2)
    prem = get("/fapi/v1/premiumIndex", {"symbol": symbol}, "basis")
    if prem:
        mark, index = float(prem["markPrice"]), float(prem["indexPrice"])
        out["basis"] = {"mark_price": f(mark), "index_price": f(index),
                        "basis_bps": f(bps(mark, index), 3),
                        "at_utc": iso(int(prem["time"]))}
        out["next_funding"] = {
            "next_funding_utc": iso(int(prem["nextFundingTime"])),
            "last_funding_rate": f(float(prem["lastFundingRate"]), 10),
            "interest_rate": f(float(prem.get("interestRate", "nan")), 10)}
    ls = get("/futures/data/topLongShortAccountRatio",
             {"symbol": symbol, "period": "1h", "limit": 168}, "top_trader_ratio")
    if ls:
        vals = np.array([float(x["longShortRatio"]) for x in ls])
        out["top_trader_ratio"] = {
            "ratio": f(vals[-1], 6), "at_utc": iso(int(ls[-1]["timestamp"])),
            "percentile_7d": f(pct_rank(vals, vals[-1]), 2), "samples": int(len(vals))}
    out["fetched_utc"] = iso(int(time.time() * 1000))
    if out["degraded"]:
        out["provenance"] = "stale"
    return out


# ══════════════════════════════════════════════════════════════ bias engine

BIAS_RULES = {
    "method": "count-based, equal weights, never fitted (D9 discipline)",
    "votes": {
        "location": {
            "daily": "price vs anchored M-VWAP AND prior-day value area "
                     "(+1 above both, -1 below both, else 0)",
            "weekly": "price vs anchored Q-VWAP AND 20d value area "
                      "(+1 above both, -1 below both, else 0)"},
        "momentum": {
            "daily": "4h and 12h RSI agree on side AND slope sign (+1 bull, -1 bear, else 0)",
            "weekly": "12h and 1d RSI agree on side AND slope sign"},
        "crowding": {
            "daily": "funding percentile >= 90 votes -1; <= 10 votes +1; else 0 "
                     "(A1.6b: symmetric)",
            "weekly": "same as daily"},
        "trend": {
            "daily": "sign of the sum of governor regime dirs over lenses {1h, 4h}",
            "weekly": "sign of the sum of governor regime dirs over lenses {4h, 12h}"},
    },
    "volatility_rule": "A1.6(a): volatility casts NO vote; a compression flag "
                       "demotes the final verdict one band toward Neutral-mixed",
    "bands": {"Long": "sum >= +3", "Lean-long": "sum in +1..+2",
              "Neutral-mixed": "sum == 0", "Lean-short": "sum in -2..-1",
              "Short": "sum <= -3"},
    "invalidation_rule": "every bias prints its invalidation; no invalidation, "
                         "no bias printed (contract 4)",
}


def band_for(total):
    if total >= 3:
        return "Long"
    if total >= 1:
        return "Lean-long"
    if total == 0:
        return "Neutral-mixed"
    if total >= -2:
        return "Lean-short"
    return "Short"


def demote(band):
    """One band toward Neutral-mixed (A1.6a)."""
    i = VERDICT_BANDS.index(band)
    mid = VERDICT_BANDS.index("Neutral-mixed")
    if i == mid:
        return band
    return VERDICT_BANDS[i + (1 if i < mid else -1)]


def bias_engine(a, gov, horizon):
    """Count-based bias with per-vote invalidation levels (contract 4 + A1.6)."""
    price = a["price"]
    votes, details = {}, {}

    vw = a["vwap"]["anchored"]["M" if horizon == "daily" else "Q"]["vwap"]
    if horizon == "daily":
        vp = a["volume_profile"].get("prior_day") or {}
    else:
        vp = a["volume_profile"].get("20d") or {}
    vah, val = vp.get("vah"), vp.get("val")
    v = 0
    if vw is not None and vah is not None and val is not None and price is not None:
        above = price > vw and price > vah
        below = price < vw and price < val
        v = 1 if above else -1 if below else 0
    votes["location"] = v
    details["location"] = {"vote": v, "vwap_level": vw, "vah": vah, "val": val,
                           "invalidation": vw,
                           "invalidation_note": "anchored %s-VWAP cross"
                           % ("M" if horizon == "daily" else "Q")}

    tfs = ("4h", "12h") if horizon == "daily" else ("12h", "1d")
    r = a["rsi"]["timeframes"]
    vals = [r.get(t, {}) for t in tfs]
    v = 0
    if all(x.get("value") is not None for x in vals):
        bull = all(x["value"] > 50 and (x["slope"] or 0) >= 0 for x in vals)
        bear = all(x["value"] < 50 and (x["slope"] or 0) <= 0 for x in vals)
        v = 1 if bull else -1 if bear else 0
    votes["momentum"] = v
    details["momentum"] = {"vote": v, "timeframes": list(tfs),
                           "values": [x.get("value") for x in vals],
                           "slopes": [x.get("slope") for x in vals],
                           "invalidation": 50.0,
                           "invalidation_note": "%s RSI crossing 50" % tfs[0]}

    fp = a["funding"].get("percentile_vs_full_history")
    v = 0 if fp is None else (-1 if fp >= 90 else 1 if fp <= 10 else 0)
    votes["crowding"] = v
    details["crowding"] = {"vote": v, "funding_percentile": fp,
                           "invalidation": 90.0 if v == -1 else 10.0 if v == 1 else None,
                           "invalidation_note": "funding percentile re-entering 10-90"}

    lenses = ("1h", "4h") if horizon == "daily" else ("4h", "12h")
    dirs = [gov.get(l, {}).get("regime_dir") for l in lenses]
    dirs = [d for d in dirs if d is not None]
    s = sum(dirs)
    v = 1 if s > 0 else -1 if s < 0 else 0
    votes["trend"] = v
    key = lenses[-1]
    inval = None
    for row in a.get("radar", []):
        if row["lens"] == key:
            inval = row["campaign_invalidation"]
    details["trend"] = {"vote": v, "lenses": list(lenses), "dirs": dirs,
                        "invalidation": inval,
                        "invalidation_note": "%s governor far band edge" % key}

    total = sum(votes.values())
    raw = band_for(total)
    compression = a["volatility"].get("regime_flag") == "compression"
    final = demote(raw) if compression else raw
    invals = [d["invalidation"] for d in details.values() if d["invalidation"] is not None]
    return {"horizon": horizon, "votes": votes, "vote_total": total,
            "verdict_raw": raw, "verdict": final,
            "compression_demotion": bool(compression),
            "details": details,
            "invalidation_levels": invals,
            "provenance": "computed"}


# ══════════════════════════════════════════════════════ flags, POI, summary

def confluence_flags(a, gov):
    price = a["price"]
    vp_pd = a["volume_profile"].get("prior_day") or {}
    r = a["rsi"]["timeframes"]
    fl = {k: False for k in CONFLUENCE_FLAGS}
    mv = a["vwap"]["anchored"]["M"]["vwap"]
    yv = a["vwap"]["anchored"]["Y"]["vwap"]
    fl["above_M_vwap"] = bool(mv is not None and price is not None and price > mv)
    fl["above_Y_vwap"] = bool(yv is not None and price is not None and price > yv)
    vah, val = vp_pd.get("vah"), vp_pd.get("val")
    fl["in_prior_day_value"] = bool(vah is not None and val is not None
                                    and val <= price <= vah)
    fl["above_VAH"] = bool(vah is not None and price > vah)
    fl["below_VAL"] = bool(val is not None and price < val)
    atr1d = (a["volatility"]["atr_percentile_vs_1y"].get("1d") or {}).get("atr")
    npocs = a["volume_profile"].get("naked_pocs") or []
    if atr1d and price is not None:
        fl["naked_poc_above_1atr"] = any(
            p["poc"] > price and (p["poc"] - price) <= atr1d for p in npocs)
        fl["naked_poc_below_1atr"] = any(
            p["poc"] < price and (price - p["poc"]) <= atr1d for p in npocs)
    fl["rsi4h_bull_side"] = bool((r.get("4h", {}).get("value") or 0) > 50)
    fl["rsi12h_bull_side"] = bool((r.get("12h", {}).get("value") or 0) > 50)
    divs = [d["kind"] for tf in ("4h", "12h", "1d")
            for d in (r.get(tf, {}).get("divergences") or [])]
    fl["rsi_div_bear_active"] = any("bear" in k for k in divs)
    fl["rsi_div_bull_active"] = any("bull" in k for k in divs)
    fp = a["funding"].get("percentile_vs_full_history")
    fl["funding_p90_plus"] = bool(fp is not None and fp >= 90)
    fl["funding_p10_minus"] = bool(fp is not None and fp <= 10)
    fl["gov4h_long_regime"] = gov.get("4h", {}).get("regime_dir") == 1
    fl["gov12h_long_regime"] = gov.get("12h", {}).get("regime_dir") == 1
    fl["stage2_4h"] = gov.get("4h", {}).get("stage") == 2
    fl["compression_flag"] = a["volatility"].get("regime_flag") == "compression"
    oi = (a.get("tier2") or {}).get("open_interest") or {}
    p90 = oi.get("change_24h_percentile")
    fl["oi_surge_p90"] = bool(p90 is not None and p90 >= 90)
    return fl


def points_of_interest(symbol, a, gov, prev_states):
    out = []

    def add(rid, detail, numbers):
        out.append({"asset": symbol, "rule_id": rid, "rule": POI_RULES[rid],
                    "severity": POI_SEVERITY[rid], "detail": detail,
                    "numbers": numbers})

    fp = a["funding"].get("percentile_vs_full_history")
    if fp is not None and (fp >= 90 or fp <= 10):
        add("POI-1", "funding %s extreme" % ("crowded-long" if fp >= 90 else "crowded-short"),
            {"percentile": fp, "current": a["funding"].get("current")})
    r = a["rsi"]["timeframes"]
    for tf in ("1d", "12h", "4h"):            # highest TF first: it leads the row
        for d in (r.get(tf, {}).get("divergences") or []):
            add("POI-2", "%s %s divergence" % (tf, d["kind"]),
                {"tf": tf, "kind": d["kind"], "rsi_from": d["rsi_from"],
                 "rsi_to": d["rsi_to"], "at_utc": d["at_utc"]})
            break
    atr1d = (a["volatility"]["atr_percentile_vs_1y"].get("1d") or {}).get("atr")
    price = a["price"]
    if atr1d and price:
        near_first = sorted((a["volume_profile"].get("naked_pocs") or []),
                            key=lambda p: abs(p["poc"] - price))
        for p in near_first:                  # nearest naked POC leads the row
            if abs(p["poc"] - price) <= atr1d:
                add("POI-3", "naked POC from %s within 1.0 daily-ATR" % p["day"],
                    {"poc": p["poc"], "distance_bps": f(bps(p["poc"], price), 2),
                     "daily_atr": atr1d})
    for h in (a["vwap"].get("crossed_24h") or []):
        add("POI-4", "price crossed anchored %s-VWAP %s" % (h["anchor"], h["direction"]),
            {"anchor": h["anchor"], "level": h["level"], "at_utc": h["at_utc"]})
    streak = a["volatility"].get("compression_streak_days") or 0
    if streak >= 5:
        add("POI-5", "compression %d consecutive days" % streak,
            {"days": streak, "rv_ratio_7_30": a["volatility"].get("rv_ratio_7_30")})
    ext = a["sessions"].get("extension_ratio")
    if ext is not None and ext > 1.5:
        add("POI-6", "session extension %.2fx the 20d median" % ext,
            {"extension_ratio": ext, "driver": a["sessions"].get("driver"),
             "median_day_range_20d": a["sessions"].get("median_day_range_20d")})
    oi = (a.get("tier2") or {}).get("open_interest") or {}
    p90 = oi.get("change_24h_percentile")
    if p90 is not None and p90 >= 90:
        add("POI-7", "OI 24h change in the top decile",
            {"change_24h_pct": oi.get("change_24h_pct"), "percentile": p90})
    if prev_states:
        for row in a.get("radar", []):
            prev = prev_states.get(row["lens"])
            if prev and prev != row["state"]:
                add("POI-8", "radar %s lens: %s -> %s" % (row["lens"], prev, row["state"]),
                    {"lens": row["lens"], "from": prev, "to": row["state"]})

    # One row per asset per rule (builder reporting decision, printed in the
    # rules header): without it a single detector with many instances -- e.g.
    # several naked POCs inside 1 ATR -- would consume the whole 12-row cap and
    # crowd out every other asset. The leading instance is the most significant
    # one (nearest POC, highest TF); the rest survive as an occurrence count.
    grouped = {}
    for p in out:
        g = grouped.setdefault(p["rule_id"], {"row": p, "count": 0})
        g["count"] += 1
    final = []
    for rid, g in grouped.items():
        row = g["row"]
        if g["count"] > 1:
            row["numbers"]["occurrences"] = g["count"]
        final.append(row)
    final.sort(key=lambda p: p["severity"])
    return final


def actionable_summary(assets, placeholders):
    now, watch, aside = [], [], []
    for sym, a in assets.items():
        bias = a["bias"]["daily"]["verdict"]
        for row in a.get("radar", []):
            line = {"asset": sym, "lens": row["lens"], "dir": row["dir_word"],
                    "state": row["state"], "zone": row["active_zone"] or row["nearest_armed_zone"],
                    "distance_gov_atr": row["zone_distance_gov_atr"],
                    "setup_invalidation": row["setup_invalidation"],
                    "campaign_invalidation": row["campaign_invalidation"],
                    "tier": row["tier"], "needs_next": row["needs_next"],
                    "daily_verdict": bias,
                    "disagreement": bool(
                        (row["dir"] == 1 and bias in ("Short", "Lean-short")) or
                        (row["dir"] == -1 and bias in ("Long", "Lean-long"))),
                    "doctrine_chip": row["doctrine_chip"],
                    "post_x_caution": row.get("post_x_caution", False),
                    "last_x_gov_bars_ago": row.get("last_x_gov_bars_ago")}
            if row["state"] == "ZONE_ACTIVE":
                line["action"] = "playbook-valid zone occupancy"
                now.append(line)
            elif row["state"] in ("ENTERED", "DEFENSE"):
                line["action"] = "manage per 5-7"
                line["live_stop"] = row["live_stop"]
                now.append(line)
            elif row["state"] == "POST_X":
                aside.append(line)
            elif row["state"] == "ARMED":
                d = row["zone_distance_gov_atr"]
                if d is not None and d <= placeholders["watch_proximity_gov_atr"]:
                    watch.append(line)
    order = {"ZONE_ACTIVE": 0, "ENTERED": 1, "DEFENSE": 1}
    now.sort(key=lambda x: (order.get(x["state"], 2),
                            0 if x["tier"] == "full" else 1, x["asset"], x["lens"]))
    watch.sort(key=lambda x: (x["distance_gov_atr"] if x["distance_gov_atr"] is not None
                              else 9e9, x["asset"]))
    aside.sort(key=lambda x: (x["asset"], x["lens"]))
    return {"now": now, "watch": watch, "stand_aside": aside,
            "empty_line": "No playbook-valid setups today — standing aside is a position."}


# ══════════════════════════════════════════════════════════ assembly

def rules_header(vp_substrate):
    return {
        "rules_version": RULES_VERSION,
        "script_version": SCRIPT_VERSION,
        "engine_version": ENGINE_VERSION,
        "config_id": CONFIG_ID,
        # NB: not "contracts" -- F-B7 forbids any key matching
        # size|qty|notional|leverage|contracts anywhere in this artifact.
        "governed_by": ["prompts/Daily_Brief_Builder_Contract.md",
                        "prompts/Daily_Brief_Contract_Amendment_1.md"],
        "firewall": [
            "1. live data: operations only, forbidden as study evidence",
            "2. no journal reads; no signal-outcome or trade-outcome statistics "
            "on any window",
            "3. engine modules imported read-only; signals/trading/cells "
            "unmodified; trading layer never invoked",
            "4. hypothesis-mine clause: the archive may seed hypotheses but is "
            "never a scoring window; radar-outcome scoring prohibited",
        ],
        "bias": BIAS_RULES,
        "radar": {
            "states": ["DORMANT", "ARMED", "ZONE_ACTIVE", "ENTERED", "DEFENSE", "POST_X"],
            "precedence": "POST_X > DORMANT > DEFENSE > ENTERED > ZONE_ACTIVE > ARMED",
            "post_x_rule": "operator ruling 2026-07-27: an X's authority ends at "
                           "the NEXT arming. POST_X holds only while no campaign "
                           "has armed since the X (campaign_id proves it); a "
                           "campaign armed after a recent X reports its true live "
                           "state and carries post_x_caution=true instead. "
                           "'Never negotiate with an X' forbids re-entering the "
                           "campaign that failed, not the one a fresh governor "
                           "cross created.",
            "semantics": "SSv11.0.2 playbook state machine; v11 semantics only (D2)",
            "zone_occupancy_rule": "ZONE_ACTIVE means price is inside an armed "
                                   "band (two-sided containment). This is NOT the "
                                   "engine's tag memory, reported separately as "
                                   "engine_tag_zone; the radar never claims a tag.",
            "arming": "Z1 armed with every live campaign; Z2 likewise when "
                      "prov_zones=Z1+Z2 (provisional included); Z3 only when "
                      "stage-aligned (stage 2)",
            "placeholders": {"watch_proximity_gov_atr": WATCH_PROXIMITY_GOV_ATR,
                             "post_x_window_gov_bars": POST_X_WINDOW_GOV_BARS,
                             "defense_window_exec_bars": DEFENSE_WINDOW_EXEC_BARS,
                             "re_ratify": "after ~1 week of use (D3)"},
            "zone_parameters_source": "configs/%s.yaml signal block (never "
                                      "hardcoded independently)" % CONFIG_ID,
            "lenses": LENSES,
            "governor_bars_reported": GOV_BARS_REPORT,
            "doctrine_chip": DOCTRINE_CHIP,
            "no_sizing": "no sizing field exists anywhere in this artifact (F-B7)",
        },
        "poi_severity": POI_SEVERITY,
        "poi_rules": POI_RULES,
        "poi_cap": POI_CAP,
        "poi_grouping": "one row per asset per rule; the leading instance is the "
                        "most significant (nearest naked POC, highest divergence "
                        "TF) and further instances survive as numbers.occurrences",
        "staleness_measured_from": "the input bar's CLOSE time (open + interval), "
                                   "not its open; funding records are stamped at "
                                   "settlement and carry no bar interval",
        "naked_poc_scope": "completed days only -- the current day's POC has no "
                           "later bars to be tested against",
        "confluence_dictionary": CONFLUENCE_FLAGS,
        "confluence_note": "changes require a contract amendment and a "
                           "rules_version bump (A1.4)",
        "staleness": STALENESS_TABLE,
        "staleness_rule": "input older than one native interval prints a stale chip",
        "volume_profile": {"bins": VP_BINS, "value_area_fraction": VALUE_AREA,
                           "method": "uniform-spread kline CDF",
                           "naked_poc_days": NAKED_POC_DAYS,
                           "substrate_per_asset": vp_substrate,
                           "fallback_rule": "1m klines where present, else 5m "
                                            "(contract 3.2)"},
        "tpo": {"bracket_tf": "30m", "bins": TPO_BINS,
                "value_area_fraction": VALUE_AREA},
        "vwap": {"basis": "1h klines, typical price (H+L+C)/3, volume-weighted "
                          "(A1.6d, pinned)",
                 "rolling_days": [7, 30, 90, 365],
                 "anchored": ["W", "M", "Q", "Y"]},
        "sessions_utc": {"asia": "00-08", "london": "07-16", "ny": "13-22"},
        "provenance_legend": {"computed": "from the local estate",
                              "fetched": "live public endpoint",
                              "approximation": "kline method, not tick data",
                              "stale": "input older than its native interval, or "
                                       "a degraded fetch"},
    }


def canonical_rules_sha256(rules):
    blob = json.dumps(rules, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def staleness_for(asset, now_ms, runs):
    out = []
    for layer, tf in STALENESS_TABLE.items():
        if layer == "tier2":
            t2 = asset.get("tier2") or {}
            if t2.get("degraded"):
                out.append({"layer": layer, "reason": "degraded fetch",
                            "detail": t2["degraded"]})
            continue
        # Age is measured from the input bar's CLOSE (open + interval), not its
        # open: at 03:37 the freshest CLOSED 1h bar is the one that opened at
        # 02:00, so an open-time test would flag every layer stale forever.
        if tf == "gov_tf":
            for lens, run in runs.items():
                if run is None:
                    continue
                ex_tf = LENSES[lens]["exec"]
                closed = int(run["sig"].exec_open_ms[-1]) + INTERVAL_MS[ex_tf]
                lim = INTERVAL_MS[LENSES[lens]["gov"]]
                if now_ms - closed > lim:
                    out.append({"layer": "%s:%s" % (layer, lens),
                                "native_tf": LENSES[lens]["gov"],
                                "last_input_utc": iso(closed),
                                "age_hours": round((now_ms - closed) / 3.6e6, 2)})
            continue
        src_tf = {"1d": "1h", "30m": "5m", "8h": "funding"}.get(tf, tf)
        last = asset["last_bar_utc"].get(src_tf)
        if last is None:
            continue
        last_ms = int(datetime.strptime(last, "%Y-%m-%dT%H:%M:%SZ")
                      .replace(tzinfo=timezone.utc).timestamp() * 1000)
        # a funding record is stamped at settlement -- it has no bar to close
        closed = last_ms if src_tf == "funding" else last_ms + ALL_MS[src_tf]
        if now_ms - closed > ALL_MS[tf]:
            out.append({"layer": layer, "native_tf": tf,
                        "last_input_utc": iso(closed),
                        "age_hours": round((now_ms - closed) / 3.6e6, 2)})
    return out


def load_all(symbol, now_ms, tfs):
    out = {}
    for tf in tfs:
        d = dl.load_klines(symbol, tf, 0, now_ms)
        out[tf] = d.reset_index(drop=True)
    out["1d"] = resample(out["1h"], "1d")
    return out


def build_brief(symbols, now_ms, tier2_canned=None, prev_index_line=None,
                log=print):
    t0 = time.time()
    cfg = load_config(CONFIG_ID)
    tfs = ["1m", "5m", "15m", "1h", "4h", "12h"]
    vp_substrate, assets, all_runs = {}, {}, {}

    btc = load_all("BTCUSDT", now_ms, ["1h"])
    prev_states_all = {}
    if prev_index_line:
        for sym, blob in (prev_index_line.get("per_asset") or {}).items():
            prev_states_all[sym] = blob.get("radar_states") or {}

    for sym in symbols:
        log(f"  {sym}: layers…")
        k = load_all(sym, now_ms, tfs)
        if not len(k["1h"]):
            log(f"  {sym}: no klines, skipped")
            continue
        fund = dl.load_funding(sym, 0, now_ms)
        price = float(k["1h"]["close"].iloc[-1])
        sub = "1m" if len(k["1m"]) else "5m"
        vp_substrate[sym] = sub
        vsrc = k[sub]

        last_bar = {tf: iso(int(k[tf]["open_time"].iloc[-1])) for tf in tfs if len(k[tf])}
        last_bar["1d"] = iso(int(k["1d"]["open_time"].iloc[-1]))
        last_bar["funding"] = iso(int(fund["funding_time"].iloc[-1])) if len(fund) else None

        today = day_floor(now_ms)
        vp = {
            "substrate": sub, "provenance": "approximation",
            "prior_day": volume_profile(vsrc[(vsrc["open_time"] >= today - DAY_MS)
                                             & (vsrc["open_time"] < today)]),
            "5d": volume_profile(vsrc[vsrc["open_time"] >= now_ms - 5 * DAY_MS]),
            "20d": volume_profile(vsrc[vsrc["open_time"] >= now_ms - 20 * DAY_MS]),
            "naked_pocs": naked_pocs(k["5m"] if len(k["5m"]) else vsrc, now_ms),
            "naked_poc_window_days": NAKED_POC_DAYS,
            "naked_poc_substrate": "5m" if len(k["5m"]) else sub,
        }
        vw = vwap_complex(k["1h"], now_ms, price)
        vw["crossed_24h"] = anchored_vwap_cross_24h(k["1h"], now_ms)

        a = {
            "symbol": sym, "price": f(price),
            "price_at_utc": iso(int(k["1h"]["open_time"].iloc[-1])),
            "last_bar_utc": last_bar,
            "structure": structure_layer(k["1d"], k["1h"], now_ms, price),
            "volume_profile": vp,
            "tpo": {"session": tpo_profile(vsrc[vsrc["open_time"] >= today]),
                    "composite_5d": tpo_profile(
                        vsrc[vsrc["open_time"] >= now_ms - 5 * DAY_MS])},
            "vwap": vw,
            "rsi": rsi_layer(k["1h"], price),
            "volatility": volatility_layer(k, now_ms),
            "funding": funding_layer(fund, now_ms),
            "sessions": sessions_layer(k["1h"], now_ms),
            "btc_beta": beta_layer(k["1d"], resample(btc["1h"], "1d"))
            if sym != "BTCUSDT" else {"provenance": "computed", "note": "reference asset"},
        }

        runs = {}
        for lens in LENSES:
            runs[lens] = run_lens(sym, lens, cfg, k, now_ms)
        all_runs[sym] = runs
        a["governor"] = governor_dashboard(runs)
        a["radar"] = [radar_row(runs[l]) for l in LENSES if runs[l] is not None]
        a["tier2"] = fetch_tier2(sym, (tier2_canned or {}).get(sym))
        a["flags"] = confluence_flags(a, a["governor"])
        a["bias"] = {h: bias_engine(a, a["governor"], h) for h in ("daily", "weekly")}
        a["points_of_interest"] = points_of_interest(
            sym, a, a["governor"], prev_states_all.get(sym))
        a["staleness"] = staleness_for(a, now_ms, runs)
        assets[sym] = a

    poi_all = [p for a in assets.values() for p in a["points_of_interest"]]
    poi_all.sort(key=lambda p: (p["severity"], p["asset"], p["rule_id"]))
    rules = rules_header(vp_substrate)
    doc = {
        "schema": "naiad_daily_brief",
        "date": iso(now_ms)[:10],
        "generated_utc": iso(int(time.time() * 1000)),
        "as_of_utc": iso(now_ms),
        "script_version": SCRIPT_VERSION,
        "rules_version": RULES_VERSION,
        "rules": rules,
        "rules_sha256": canonical_rules_sha256(rules),
        "universe": list(symbols),
        "vp_substrate": vp_substrate,
        "assets": assets,
        "points_of_interest_top": poi_all[:POI_CAP],
        "points_of_interest_total": len(poi_all),
        "points_of_interest_dropped": max(0, len(poi_all) - POI_CAP),
        "actionable": actionable_summary(
            assets, rules["radar"]["placeholders"]),
        "calendar_events": {"note": "Tier 3 — added by the reviewer at review "
                                    "(web search); this script never fetches it",
                            "items": []},
        "runtime_seconds": round(time.time() - t0, 2),
    }
    return doc, all_runs


def index_line_from_json(doc, json_path):
    """A1.5 index schema, rebuildable from the JSON alone (F-B8)."""
    per_asset = {}
    for sym, a in doc["assets"].items():
        states = {r["lens"]: r["state"] for r in a.get("radar", [])}
        best = None
        for pref in ("ZONE_ACTIVE", "DEFENSE", "ENTERED", "ARMED", "POST_X", "DORMANT"):
            if pref in states.values():
                best = pref
                break
        per_asset[sym] = {
            "daily_verdict": a["bias"]["daily"]["verdict"],
            "weekly_verdict": a["bias"]["weekly"]["verdict"],
            "radar_best_state": best,
            "radar_states": states,
            "poi_count": len(a["points_of_interest"]),
            "flags_true": [k for k in CONFLUENCE_FLAGS if a["flags"].get(k)],
        }
    return {
        "date": doc["date"], "generated_utc": doc["generated_utc"],
        "script_version": doc["script_version"],
        "rules_version": doc["rules_version"],
        "rules_sha256": doc["rules_sha256"],
        "json_sha256": sha256_file(json_path),
        "per_asset": per_asset,
        "staleness": [{"asset": s, "items": a["staleness"]}
                      for s, a in doc["assets"].items() if a["staleness"]],
    }


def sha256_file(path):
    """Binary read only — never a shell tool (msys CR hazard, A1.5)."""
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def write_index(line, path=INDEX_PATH):
    """One line per date; a same-date re-run REPLACES that date's line."""
    path.parent.mkdir(parents=True, exist_ok=True)
    keep = []
    if path.exists():
        with open(path, "rb") as fh:
            for raw in fh.read().decode("utf-8").splitlines():
                if not raw.strip():
                    continue
                try:
                    if json.loads(raw).get("date") == line["date"]:
                        continue
                except json.JSONDecodeError:
                    continue
                keep.append(raw)
    keep.append(json.dumps(line, sort_keys=True, ensure_ascii=True))
    keep.sort(key=lambda r: json.loads(r)["date"])
    with open(path, "wb") as fh:
        fh.write(("\n".join(keep) + "\n").encode("utf-8"))
    return path


def read_last_index_line(path=INDEX_PATH, before_date=None):
    if not path.exists():
        return None
    lines = []
    with open(path, "rb") as fh:
        for raw in fh.read().decode("utf-8").splitlines():
            if raw.strip():
                try:
                    lines.append(json.loads(raw))
                except json.JSONDecodeError:
                    pass
    lines = [l for l in lines if before_date is None or l.get("date") < before_date]
    return lines[-1] if lines else None


# ══════════════════════════════════════════════════════════════ HTML

def esc(x):
    return html_mod.escape("" if x is None else str(x))


def num(x, nd=2):
    if x is None:
        return "—"
    try:
        v = float(x)
    except (TypeError, ValueError):
        return esc(x)
    if abs(v) >= 1000:
        return f"{v:,.{max(0, nd - 2)}f}"
    if abs(v) >= 1:
        return f"{v:,.{nd}f}"
    return f"{v:.6g}"


def chip(text, kind="mute"):
    return f'<span class="chip {kind}">{esc(text)}</span>'


VERDICT_KIND = {"Long": "ok", "Lean-long": "ok", "Neutral-mixed": "mute",
                "Lean-short": "warn", "Short": "warn"}
STATE_KIND = {"ZONE_ACTIVE": "ok", "ENTERED": "ok", "DEFENSE": "warn",
              "POST_X": "warn", "ARMED": "mute", "DORMANT": "mute"}


def render_summary(doc, foot=False):
    act = doc["actionable"]
    ph = doc["rules"]["radar"]["placeholders"]
    out = [f'<section class="panel" id="{"actionable-foot" if foot else "actionable"}">']
    out.append('<h2>Actionable summary</h2>')
    out.append('<p class="lede">The radar reports playbook <em>state</em> under '
               'printed rules. It sizes nothing and decides nothing — '
               'every trade decision is the operator\'s.</p>')
    if not act["now"] and not act["watch"] and not act["stand_aside"]:
        out.append(f'<p class="empty">{esc(act["empty_line"])}</p>')
    for title, key, note in (
            ("Actionable now", "now", "ZONE_ACTIVE first (full tier before provisional), then ENTERED/DEFENSE to manage per 5–7"),
            ("Watch", "watch", f"ARMED rows whose nearest armed band is within {ph['watch_proximity_gov_atr']} gov-ATR"),
            ("Stand aside", "stand_aside", "never negotiate with an X")):
        rows = act[key]
        out.append(f'<h3>{esc(title)} <span class="mute">— {esc(note)}</span></h3>')
        if not rows:
            out.append('<p class="empty">— none —</p>')
            continue
        out.append('<table><thead><tr><th>Asset</th><th>Lens</th><th>Dir</th>'
                   '<th>State</th><th>Zone</th><th>Dist (gov-ATR)</th>'
                   '<th>Setup invalidation</th><th>Campaign invalidation</th>'
                   '<th>Bias (daily)</th><th>Needs next</th></tr></thead><tbody>')
        for r in rows:
            flags = ""
            if r.get("tier") == "provisional":
                flags += chip("provisional", "warn")
                if r.get("doctrine_chip"):
                    flags += chip(r["doctrine_chip"], "mute")
            if r.get("disagreement"):
                flags += chip("radar vs bias disagree", "warn")
            if r.get("post_x_caution"):
                flags += chip(f'post-X caution ({r.get("last_x_gov_bars_ago")} gov bars)',
                              "warn")
            out.append(
                f'<tr><td><a href="#{esc(r["asset"])}">{esc(r["asset"])}</a></td>'
                f'<td>{esc(r["lens"])}</td><td>{esc(r["dir"])}</td>'
                f'<td>{chip(r["state"], STATE_KIND.get(r["state"], "mute"))}{flags}</td>'
                f'<td>{esc(r["zone"] or "—")}</td>'
                f'<td class="n">{num(r["distance_gov_atr"], 3)}</td>'
                f'<td class="n">{num(r["setup_invalidation"], 4)}</td>'
                f'<td class="n">{num(r["campaign_invalidation"], 4)}</td>'
                f'<td>{chip(r["daily_verdict"], VERDICT_KIND.get(r["daily_verdict"], "mute"))}</td>'
                f'<td class="mute">{esc(r["needs_next"])}</td></tr>')
        out.append('</tbody></table>')
    out.append('</section>')
    return "\n".join(out)


def render_html(doc):
    """Built from the JSON document ONLY (F-B2). No external requests."""
    p = PALETTE
    css = f"""
:root{{--ink:{p['ink']};--panel:{p['panel']};--rule:{p['rule']};--tx:{p['tx']};
--mute:{p['mute']};--warn:{p['warn']};--ok:{p['ok']}}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--ink);color:var(--tx);
font-family:"IBM Plex Sans","Segoe UI",system-ui,-apple-system,sans-serif;
font-size:14px;line-height:1.5}}
h1,h2,h3{{font-family:"Space Grotesk","IBM Plex Sans",system-ui,sans-serif;
font-weight:600;letter-spacing:-0.01em}}
h1{{font-size:26px;margin:0 0 4px}} h2{{font-size:19px;margin:0 0 10px}}
h3{{font-size:15px;margin:18px 0 8px;font-weight:500}}
a{{color:var(--tx)}} a:hover{{color:var(--ok)}}
.wrap{{max-width:1500px;margin:0 auto;padding:20px 22px 60px}}
.masthead{{border-bottom:1px solid var(--rule);padding-bottom:14px;margin-bottom:18px}}
.masthead .sub{{color:var(--mute);font-size:13px}}
.panel{{background:var(--panel);border:1px solid var(--rule);border-radius:10px;
padding:16px 18px;margin:14px 0}}
.lede{{color:var(--mute);margin:0 0 12px;max-width:110ch}}
.empty{{color:var(--mute);font-style:italic}}
nav.assets{{position:sticky;top:0;z-index:9;background:var(--ink);
border-bottom:1px solid var(--rule);padding:8px 0;margin-bottom:10px;
display:flex;flex-wrap:wrap;gap:6px}}
nav.assets a{{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:12px;
text-decoration:none;border:1px solid var(--rule);border-radius:999px;
padding:3px 9px;color:var(--mute)}}
nav.assets a:hover{{border-color:var(--ok);color:var(--ok)}}
table{{width:100%;border-collapse:collapse;margin:6px 0 2px;font-size:13px}}
th,td{{text-align:left;padding:5px 8px;border-bottom:1px solid var(--rule);
vertical-align:top}}
th{{color:var(--mute);font-weight:500;font-size:11.5px;text-transform:uppercase;
letter-spacing:.06em}}
td.n,th.n{{text-align:right;font-family:"IBM Plex Mono",ui-monospace,monospace}}
.chip{{display:inline-block;font-family:"IBM Plex Mono",ui-monospace,monospace;
font-size:10.5px;padding:1px 6px;border-radius:999px;border:1px solid var(--rule);
color:var(--mute);margin:0 3px 2px 0;white-space:nowrap}}
.chip.ok{{color:var(--ok);border-color:var(--ok)}}
.chip.warn{{color:var(--warn);border-color:var(--warn)}}
.chip.mute{{color:var(--mute)}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:14px}}
.kv{{display:grid;grid-template-columns:auto 1fr;gap:2px 12px;font-size:13px}}
.kv dt{{color:var(--mute)}}
.kv dd{{margin:0;font-family:"IBM Plex Mono",ui-monospace,monospace}}
.asset{{border-top:2px solid var(--rule);margin-top:26px;padding-top:6px}}
.asset h2{{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap}}
.mono{{font-family:"IBM Plex Mono",ui-monospace,monospace}}
.mute{{color:var(--mute)}}
.small{{font-size:12px}}
footer{{color:var(--mute);font-size:12px;border-top:1px solid var(--rule);
margin-top:30px;padding-top:12px}}
"""
    A = doc["assets"]
    out = [f'<style>{css}</style>', '<div class="wrap">']

    # ── masthead ──
    out.append('<header class="masthead">')
    out.append(f'<h1>Naiad Daily Brief — {esc(doc["date"])}</h1>')
    out.append(f'<div class="sub mono">as of {esc(doc["as_of_utc"])} · '
               f'generated {esc(doc["generated_utc"])} · script v{esc(doc["script_version"])} · '
               f'rules v{esc(doc["rules_version"])} · rules sha {esc(doc["rules_sha256"][:12])} · '
               f'engine {esc(doc["rules"]["engine_version"])} · config {esc(doc["rules"]["config_id"])}</div>')
    out.append('<div class="sub">Operations artifact — Tier-0 decision support. '
               '<strong>Not study evidence.</strong> No sizing, no alerts, no outcome statistics.</div>')
    out.append('</header>')

    out.append('<nav class="assets">')
    for s in doc["universe"]:
        if s in A:
            out.append(f'<a href="#{esc(s)}">{esc(s)}</a>')
    out.append('<a href="#poi">POI</a><a href="#calendar">Calendar</a>'
               '<a href="#rules">Rules</a></nav>')

    out.append(render_summary(doc))

    # ── bias board ──
    out.append('<section class="panel"><h2>Bias board</h2>')
    out.append('<p class="lede">Count-based votes, equal weights, never fitted. '
               'Every verdict prints its invalidation; disagreement with the radar '
               'is shown, never reconciled.</p>')
    out.append('<table><thead><tr><th>Asset</th><th class="n">Price</th>'
               '<th>Daily</th><th>Weekly</th><th>Votes (loc/mom/crowd/trend)</th>'
               '<th class="n">Invalidation</th><th>Flags true</th></tr></thead><tbody>')
    for s in doc["universe"]:
        if s not in A:
            continue
        a = A[s]
        d, w = a["bias"]["daily"], a["bias"]["weekly"]
        v = d["votes"]
        ft = [k for k in CONFLUENCE_FLAGS if a["flags"].get(k)]
        dem = chip("compression demotion", "warn") if d["compression_demotion"] else ""
        out.append(
            f'<tr><td><a href="#{esc(s)}">{esc(s)}</a></td>'
            f'<td class="n">{num(a["price"], 4)}</td>'
            f'<td>{chip(d["verdict"], VERDICT_KIND.get(d["verdict"], "mute"))}{dem}</td>'
            f'<td>{chip(w["verdict"], VERDICT_KIND.get(w["verdict"], "mute"))}</td>'
            f'<td class="mono small">{v["location"]:+d} / {v["momentum"]:+d} / '
            f'{v["crowding"]:+d} / {v["trend"]:+d} = {d["vote_total"]:+d}</td>'
            f'<td class="n">{num(d["details"]["location"]["invalidation"], 4)}</td>'
            f'<td class="small mute">{esc(", ".join(ft)) or "—"}</td></tr>')
    out.append('</tbody></table></section>')

    # ── points of interest ──
    out.append('<section class="panel" id="poi"><h2>Points of interest</h2>')
    out.append(f'<p class="lede">Fixed detectors over already-computed layers, '
               f'ranked by the printed severity table; capped at {doc["rules"]["poi_cap"]}. '
               f'{doc["points_of_interest_total"]} fired'
               + (f', {doc["points_of_interest_dropped"]} below the cap not shown'
                  if doc["points_of_interest_dropped"] else '') + '.</p>')
    if not doc["points_of_interest_top"]:
        out.append('<p class="empty">— none fired today —</p>')
    else:
        out.append('<table><thead><tr><th>Rule</th><th>Asset</th><th class="n">Sev</th>'
                   '<th>Detail</th><th>Numbers</th></tr></thead><tbody>')
        for p in doc["points_of_interest_top"]:
            nums = " · ".join(f"{k}={num(v, 4) if isinstance(v, (int, float)) else esc(v)}"
                              for k, v in p["numbers"].items())
            out.append(f'<tr><td class="mono">{esc(p["rule_id"])}</td>'
                       f'<td><a href="#{esc(p["asset"])}">{esc(p["asset"])}</a></td>'
                       f'<td class="n">{p["severity"]}</td>'
                       f'<td>{esc(p["detail"])}</td>'
                       f'<td class="small mute mono">{nums}</td></tr>')
        out.append('</tbody></table>')
    out.append('</section>')

    # ── per asset ──
    for s in doc["universe"]:
        if s not in A:
            continue
        a = A[s]
        out.append(f'<section class="asset" id="{esc(s)}">')
        stale = chip("stale inputs", "warn") if a["staleness"] else ""
        out.append(f'<h2>{esc(s)} <span class="mono mute">{num(a["price"], 4)}</span>'
                   f'{chip(a["bias"]["daily"]["verdict"], VERDICT_KIND.get(a["bias"]["daily"]["verdict"], "mute"))}'
                   f'{chip("VP " + a["volume_profile"]["substrate"], "mute")}{stale}</h2>')

        # radar
        out.append('<div class="panel"><h3>Setup radar — playbook state machine</h3>')
        out.append('<table><thead><tr><th>Lens</th><th>State</th><th>Dir</th>'
                   '<th>Stage</th><th>Tier</th><th>Zone</th><th class="n">Dist bps</th>'
                   '<th class="n">Dist gov-ATR</th><th class="n">Live stop</th>'
                   '<th class="n">Setup inval.</th><th class="n">Campaign inval.</th>'
                   '<th>Last PRIME</th><th>Needs next</th></tr></thead><tbody>')
        for r in a["radar"]:
            extra = ""
            if r["whipsaw_arrow_hidden"]:
                extra += chip("arrows hidden (whipsaw) — arming unaffected", "warn")
            if r["cold_start"]:
                extra += chip("cold_start", "warn")
            if r.get("post_x_caution"):
                extra += chip(f'post-X caution — X {r["last_x_gov_bars_ago"]} gov '
                              f'bars ago, re-armed since', "warn")
            if r["doctrine_chip"]:
                extra += chip(r["doctrine_chip"], "mute")
            lp = r["last_prime"]
            lp_s = ("—" if not lp else
                    f'{esc(lp["grade"])} {esc(lp["zone"])} · {lp["exec_bars_ago"]} bars')
            out.append(
                f'<tr><td class="mono">{esc(r["lens"])}<span class="mute small"> '
                f'{esc(r["framing"])}</span></td>'
                f'<td>{chip(r["state"], STATE_KIND.get(r["state"], "mute"))}{extra}</td>'
                f'<td>{esc(r["dir_word"])}</td><td class="n">{r["stage"]}</td>'
                f'<td>{esc(r["tier"])}</td>'
                f'<td>{esc(r["active_zone"] or r["nearest_armed_zone"] or "—")}</td>'
                f'<td class="n">{num(r["zone_distance_bps"], 1)}</td>'
                f'<td class="n">{num(r["zone_distance_gov_atr"], 3)}</td>'
                f'<td class="n">{num(r["live_stop"], 4)}</td>'
                f'<td class="n">{num(r["setup_invalidation"], 4)}</td>'
                f'<td class="n">{num(r["campaign_invalidation"], 4)}</td>'
                f'<td class="small">{lp_s}</td>'
                f'<td class="small mute">{esc(r["needs_next"])}</td></tr>')
        out.append('</tbody></table>')
        out.append('<p class="small mute">Setup invalidation = the active-or-nearest '
                   'armed zone\'s far edge. Campaign invalidation = the far governor '
                   'band edge, i.e. the X reference level — except on a flat row '
                   '(DORMANT / POST_X), which has no direction to orient "far" and '
                   'therefore prints the <em>nearer</em> band edge; each row\'s JSON '
                   'carries its own campaign_invalidation_note, and both edges are '
                   'in governor_band_top / governor_band_bot.</p></div>')

        out.append('<div class="grid">')

        # governor dashboard
        out.append('<div class="panel"><h3>Governor dashboard</h3><table><thead><tr>'
                   '<th>Lens</th><th>Regime</th><th class="n">Stage</th><th>Tier</th>'
                   '<th class="n">gov-ATR</th><th>Last PRIME</th></tr></thead><tbody>')
        for lens, g in a["governor"].items():
            if "regime_word" not in g:
                out.append(f'<tr><td>{esc(lens)}</td><td colspan="5" class="mute">'
                           f'{esc(g.get("note"))}</td></tr>')
                continue
            out.append(f'<tr><td class="mono">{esc(lens)}</td>'
                       f'<td>{esc(g["regime_word"])}</td><td class="n">{g["stage"]}</td>'
                       f'<td>{esc(g["tier"])}</td><td class="n">{num(g["gov_atr"], 4)}</td>'
                       f'<td class="small">{esc(g["last_prime_grade"] or "—")} '
                       f'{"" if g["last_prime_exec_bars_ago"] is None else str(g["last_prime_exec_bars_ago"]) + " bars"}'
                       f'</td></tr>')
        out.append('</tbody></table></div>')

        # structure
        st = a["structure"]
        out.append('<div class="panel"><h3>Structure</h3><dl class="kv">')
        for lbl, key in (("Prior day", "prior_day"), ("Prior week", "prior_week"),
                         ("Prior month", "prior_month")):
            r = st[key]
            out.append(f'<dt>{esc(lbl)} H/L</dt><dd>{num(r["high"], 4)} / {num(r["low"], 4)}</dd>')
        for k, v in st["period_opens"].items():
            out.append(f'<dt>{esc(k)} open</dt><dd>{num(v["level"], 4)} '
                       f'<span class="mute">({num(v.get("distance_bps"), 1)} bps)</span></dd>')
        for lbl, key in (("Pivot lows", "pivot_lows"), ("Pivot highs", "pivot_highs")):
            lv = " · ".join(f'{num(x["level"], 4)}' for x in st[key]) or "—"
            out.append(f'<dt>{esc(lbl)}</dt><dd>{lv}</dd>')
        out.append(f'</dl><p class="small mute">{chip(st["provenance"], "mute")}'
                   f'{esc(st["pivot_convention"])}</p></div>')

        # volume profile + TPO
        vp = a["volume_profile"]
        out.append('<div class="panel"><h3>Volume profile &amp; TPO</h3>'
                   '<table><thead><tr><th>Composite</th><th class="n">POC</th>'
                   '<th class="n">VAH</th><th class="n">VAL</th></tr></thead><tbody>')
        for lbl, key in (("Prior day", "prior_day"), ("5d", "5d"), ("20d", "20d")):
            r = vp.get(key)
            if not r:
                continue
            out.append(f'<tr><td>{esc(lbl)}</td><td class="n">{num(r["poc"], 4)}</td>'
                       f'<td class="n">{num(r["vah"], 4)}</td>'
                       f'<td class="n">{num(r["val"], 4)}</td></tr>')
        for lbl, key in (("TPO session", "session"), ("TPO 5d", "composite_5d")):
            r = a["tpo"].get(key)
            if not r:
                continue
            out.append(f'<tr><td>{esc(lbl)}</td><td class="n">{num(r["poc"], 4)}</td>'
                       f'<td class="n">{num(r["vah"], 4)}</td>'
                       f'<td class="n">{num(r["val"], 4)}</td></tr>')
        out.append('</tbody></table>')
        np_list = vp.get("naked_pocs") or []
        out.append(f'<p class="small"><span class="mute">Naked POCs '
                   f'({vp["naked_poc_window_days"]}d, {esc(vp["naked_poc_substrate"])}): </span>'
                   + (esc(" · ".join(f'{x["day"]} {num(x["poc"], 4)}' for x in np_list[-8:]))
                      if np_list else '<span class="mute">none</span>') + '</p>')
        out.append(f'<p class="small">{chip("approximation", "warn")}'
                   f'<span class="mute">kline method ({esc(vp["substrate"])}), not tick data · '
                   f'{doc["rules"]["volume_profile"]["bins"]} bins · 70% value area</span></p></div>')

        # VWAP
        out.append('<div class="panel"><h3>VWAP complex</h3><table><thead><tr>'
                   '<th>Window</th><th class="n">VWAP</th><th class="n">±1σ</th>'
                   '<th class="n">Dist bps</th></tr></thead><tbody>')
        for k, r in a["vwap"]["rolling"].items():
            out.append(f'<tr><td>rolling {esc(k)}</td><td class="n">{num(r["vwap"], 4)}</td>'
                       f'<td class="n">{num(r["sigma"], 4)}</td>'
                       f'<td class="n">{num(r["distance_bps"], 1)}</td></tr>')
        for k, r in a["vwap"]["anchored"].items():
            out.append(f'<tr><td>anchored {esc(k)}</td><td class="n">{num(r["vwap"], 4)}</td>'
                       f'<td class="n">{num(r["sigma"], 4)}</td>'
                       f'<td class="n">{num(r["distance_bps"], 1)}</td></tr>')
        out.append('</tbody></table>')
        cr = a["vwap"].get("crossed_24h") or []
        if cr:
            out.append('<p class="small">' + "".join(
                chip(f'crossed {c["anchor"]}-VWAP {c["direction"]}', "warn") for c in cr)
                + '</p>')
        out.append(f'<p class="small mute">{esc(a["vwap"]["basis"])}</p></div>')

        # RSI
        out.append('<div class="panel"><h3>MTF RSI</h3><table><thead><tr><th>TF</th>'
                   '<th class="n">RSI(14)</th><th>Side</th><th class="n">Slope</th>'
                   '<th>Divergence</th></tr></thead><tbody>')
        for tf, r in a["rsi"]["timeframes"].items():
            dv = " ".join(chip(d["kind"], "warn") for d in (r.get("divergences") or []))
            out.append(f'<tr><td class="mono">{esc(tf)}</td>'
                       f'<td class="n">{num(r.get("value"), 2)}</td>'
                       f'<td>{esc(r.get("side") or "—")}</td>'
                       f'<td class="n">{num(r.get("slope"), 3)}</td>'
                       f'<td>{dv or "—"}</td></tr>')
        out.append('</tbody></table><p class="small mute">Wilder, length 14 · '
                   'divergences via price-pivot vs RSI-pivot, pivot(5,5)</p></div>')

        # volatility / funding / sessions / beta
        vol, fu, se, be = a["volatility"], a["funding"], a["sessions"], a["btc_beta"]
        out.append('<div class="panel"><h3>Volatility, funding, sessions, beta</h3>'
                   '<dl class="kv">')
        for tf, r in vol["atr_percentile_vs_1y"].items():
            out.append(f'<dt>ATR14 {esc(tf)} pctile (1y)</dt>'
                       f'<dd>{num(r["percentile"], 1)} <span class="mute">'
                       f'(atr {num(r["atr"], 4)})</span></dd>')
        out.append(f'<dt>RV 7d/30d</dt><dd>{num(vol.get("rv_ratio_7_30"), 3)} '
                   f'{chip(vol.get("regime_flag"), "warn" if vol.get("regime_flag") != "neutral" else "mute")}'
                   f'{("streak " + str(vol.get("compression_streak_days")) + "d") if vol.get("compression_streak_days") else ""}</dd>')
        out.append(f'<dt>Funding now</dt><dd>{num(fu.get("current"), 8)} '
                   f'<span class="mute">pctile {num(fu.get("percentile_vs_full_history"), 1)} · '
                   f'7d mean {num(fu.get("mean_7d"), 8)} · {fu.get("records_7d", 0)} records/7d · '
                   f'grid {esc(fu.get("observed_grid_hours_7d"))}h</span></dd>')
        out.append(f'<dt>Session driver</dt><dd>{esc(se.get("driver") or "—")} '
                   f'<span class="mute">ext {num(se.get("extension_ratio"), 2)}x '
                   f'(day {num(se.get("day_range"), 4)} vs 20d median '
                   f'{num(se.get("median_day_range_20d"), 4)})</span></dd>')
        if "beta_30d" in be:
            out.append(f'<dt>BTC beta 30d</dt><dd>{num(be["beta_30d"], 3)} '
                       f'<span class="mute">corr {num(be["correlation_30d"], 3)}</span></dd>')
        out.append('</dl></div>')

        # tier 2
        t2 = a["tier2"]
        out.append('<div class="panel"><h3>Tier 2 — live public fetch</h3><dl class="kv">')
        oi = t2.get("open_interest") or {}
        if oi:
            out.append(f'<dt>Open interest</dt><dd>{num(oi.get("level"), 2)} '
                       f'<span class="mute">24h {num(oi.get("change_24h_pct"), 2)}% · '
                       f'7d {num(oi.get("change_7d_pct"), 2)}% · pctile '
                       f'{num(oi.get("percentile"), 1)}</span></dd>')
        ba = t2.get("basis") or {}
        if ba:
            out.append(f'<dt>Basis</dt><dd>{num(ba.get("basis_bps"), 2)} bps '
                       f'<span class="mute">mark {num(ba.get("mark_price"), 4)}</span></dd>')
        ls = t2.get("top_trader_ratio") or {}
        if ls:
            out.append(f'<dt>Top-trader L/S</dt><dd>{num(ls.get("ratio"), 3)} '
                       f'<span class="mute">pctile {num(ls.get("percentile_7d"), 1)}</span></dd>')
        nf = t2.get("next_funding") or {}
        if nf:
            out.append(f'<dt>Next funding</dt><dd class="small">{esc(nf.get("next_funding_utc"))} '
                       f'<span class="mute">last {num(nf.get("last_funding_rate"), 8)}</span></dd>')
        out.append('</dl>')
        if t2.get("degraded"):
            out.append('<p class="small">' + chip("degraded: " + ", ".join(t2["degraded"]), "warn")
                       + '</p>')
        else:
            out.append(f'<p class="small">{chip(t2.get("provenance", "fetched"), "mute")}</p>')
        out.append('</div>')

        # flags
        out.append('<div class="panel"><h3>Confluence flags <span class="mute small">'
                   '(fixed 18-flag dictionary — P2 capture)</span></h3><p>')
        for k in CONFLUENCE_FLAGS:
            out.append(chip(k, "ok" if a["flags"].get(k) else "mute"))
        out.append('</p></div>')

        # bias detail
        out.append('<div class="panel"><h3>Bias detail</h3><table><thead><tr>'
                   '<th>Horizon</th><th>Vote</th><th class="n">Value</th>'
                   '<th class="n">Invalidation</th><th>Note</th></tr></thead><tbody>')
        for h in ("daily", "weekly"):
            b = a["bias"][h]
            for name, d in b["details"].items():
                out.append(f'<tr><td>{esc(h)}</td><td>{esc(name)}</td>'
                           f'<td class="n">{d["vote"]:+d}</td>'
                           f'<td class="n">{num(d["invalidation"], 4)}</td>'
                           f'<td class="small mute">{esc(d["invalidation_note"])}</td></tr>')
            out.append(f'<tr><td>{esc(h)}</td><td><strong>verdict</strong></td>'
                       f'<td class="n">{b["vote_total"]:+d}</td><td class="n">—</td>'
                       f'<td>{chip(b["verdict"], VERDICT_KIND.get(b["verdict"], "mute"))}'
                       + (chip("demoted from " + b["verdict_raw"], "warn")
                          if b["compression_demotion"] else "") + '</td></tr>')
        out.append('</tbody></table></div>')

        if a["staleness"]:
            out.append('<div class="panel"><h3>Staleness</h3><p class="small">')
            for s_ in a["staleness"]:
                out.append(chip(f'{s_.get("layer")} · {s_.get("age_hours", s_.get("reason"))}', "warn"))
            out.append('</p></div>')

        out.append('</div></section>')

    # ── calendar (Tier 3, reviewer-added) ──
    out.append('<section class="panel" id="calendar"><h2>Calendar &amp; events</h2>'
               '<p class="lede">Added at review — the reviewer fills this in chat via '
               'web search. This script never fetches it.</p>'
               '<p class="empty">— reserved —</p></section>')

    out.append(render_summary(doc, foot=True))

    # ── rules ──
    out.append('<section class="panel" id="rules"><h2>Rules of record</h2>')
    out.append('<p class="lede">The complete rule set that produced this brief is '
               'embedded in the JSON under <span class="mono">rules</span> '
               f'(sha256 {esc(doc["rules_sha256"][:16])}). Thresholds are v1 '
               'placeholders, expected to be re-ratified after about a week of use.</p>')
    out.append('<dl class="kv">')
    for k, v in doc["rules"]["radar"]["placeholders"].items():
        out.append(f'<dt>{esc(k)}</dt><dd>{esc(v)}</dd>')
    out.append(f'<dt>verdict bands</dt><dd class="small">'
               f'{esc(json.dumps(doc["rules"]["bias"]["bands"], sort_keys=True))}</dd>')
    out.append(f'<dt>POI severity</dt><dd class="small">'
               f'{esc(json.dumps(doc["rules"]["poi_severity"], sort_keys=True))}</dd>')
    out.append('</dl>')
    out.append('<p class="small mute">' + esc(" · ".join(doc["rules"]["firewall"])) + '</p>')
    out.append('</section>')

    out.append('<footer>Naiad Daily Brief · OPS Tier-0 · operations artifact, not '
               'study evidence · no sizing anywhere · the operator owns every '
               f'trade decision · runtime {esc(doc["runtime_seconds"])}s</footer>')
    out.append('</div>')
    return f'<!doctype html><html lang="en"><head><meta charset="utf-8">' \
           f'<meta name="viewport" content="width=device-width,initial-scale=1">' \
           f'<title>Naiad Daily Brief — {esc(doc["date"])}</title></head><body>' \
           + "\n".join(out) + '</body></html>\n'


# ══════════════════════════════════════════════════════════════ output

def serialize_json(doc):
    return json.dumps(doc, indent=1, sort_keys=True, ensure_ascii=True) + "\n"


def write_outputs(doc, out_dir=OUT_DIR):
    out_dir.mkdir(parents=True, exist_ok=True)
    jp = out_dir / f"brief_{doc['date']}.json"
    hp = out_dir / f"brief_{doc['date']}.html"
    with open(jp, "wb") as fh:
        fh.write(serialize_json(doc).encode("utf-8"))
    with open(hp, "wb") as fh:
        fh.write(render_html(doc).encode("utf-8"))
    return jp, hp


# ══════════════════════════════════════════════════════════════ fixture

def fixture_paths():
    return (FIXTURE_DIR / "fixture.json", FIXTURE_DIR / "tier2_canned.json",
            FIXTURE_DIR / "data_cache")


FIXTURE_MANIFEST = FIXTURE_DIR / "fixture_manifest.json"


def fixture_slice_manifest(cache):
    """sha256 + row counts for every frozen slice, for the pinned manifest."""
    out = {}
    for p in sorted(cache.rglob("*.parquet")):
        rel = p.relative_to(cache).as_posix()
        out[rel] = {"sha256": sha256_file(p), "bytes": p.stat().st_size,
                    "rows": int(len(pd.read_parquet(p, columns=[
                        "funding_time" if "funding" in rel else "open_time"])))}
    return out


def verify_fixture_slices(cache, manifest, log=print):
    """Fenced-substrate check: the slices are NOT in git (charter section 10 --
    raw candles are never committed), so they are verified against the pinned
    sha256 manifest instead. Same contract as the CENSUS-1b substrate: absent
    is rebuildable, present-but-different is a hard failure."""
    pinned = manifest.get("slices") or {}
    if not pinned:
        return
    missing, bad = [], []
    for rel, meta in sorted(pinned.items()):
        p = cache / rel
        if not p.exists():
            missing.append(rel)
            continue
        if sha256_file(p) != meta["sha256"]:
            bad.append(rel)
    if missing or bad:
        raise SystemExit(
            "fixture substrate does not match tests/brief_fixture/"
            "fixture_manifest.json\n"
            f"  missing: {missing or 'none'}\n"
            f"  altered: {bad or 'none'}\n"
            "The frozen klines are FENCED, not committed (charter section 10:\n"
            "raw candles are never committed; .gitignore data_cache/). Rebuild\n"
            "them from the local estate with:\n"
            f"    .venv/Scripts/python.exe scripts/daily_brief.py "
            f"--build-fixture {manifest.get('date', 'YYYY-MM-DD')}\n"
            "then re-run. The manifest pins every byte, so a rebuild is\n"
            "verifiable rather than merely plausible.")
    log(f"  fixture substrate verified against {len(pinned)} pinned sha256 slices")


def build_fixture(as_of_ms, symbols=("BTCUSDT", "SOLUSDT"), log=print):
    """Freeze a slice of the live cache as the committed determinism fixture.

    Builder utility, run once. Windows are trimmed to keep the committed bytes
    small; a fixture run therefore has less indicator warm-up than a real run,
    which is fine — F-B3 tests determinism, not agreement with a live day.
    """
    fx, canned_path, cache = fixture_paths()
    spans = {"1m": 25, "5m": 200, "15m": 200, "1h": 400, "4h": 200, "12h": 200}
    (cache / "klines").mkdir(parents=True, exist_ok=True)
    (cache / "funding").mkdir(parents=True, exist_ok=True)
    written = []
    for sym in symbols:
        for tf, days in spans.items():
            d = dl.load_klines(sym, tf, as_of_ms - days * DAY_MS, as_of_ms)
            p = cache / "klines" / f"{sym}_{tf}.parquet"
            d.reset_index(drop=True).to_parquet(p, index=False)
            written.append((p, len(d)))
        fu = dl.load_funding(sym, 0, as_of_ms)
        p = cache / "funding" / f"{sym}.parquet"
        fu.reset_index(drop=True).to_parquet(p, index=False)
        written.append((p, len(fu)))
    # canned Tier-2 (A1.7): determinism must cover the whole artifact
    canned = {}
    for sym in symbols:
        canned[sym] = {
            "provenance": "fetched", "degraded": [],
            "fetched_utc": iso(as_of_ms), "canned": True,
            "open_interest": {"level": 100000.0, "at_utc": iso(as_of_ms),
                              "change_24h_pct": 1.25, "change_7d_pct": -3.5,
                              "percentile": 62.5, "samples": 500,
                              "change_24h_percentile": 91.0},
            "basis": {"mark_price": 100.5, "index_price": 100.0,
                      "basis_bps": 50.0, "at_utc": iso(as_of_ms)},
            "next_funding": {"next_funding_utc": iso(as_of_ms + 4 * 3_600_000),
                             "last_funding_rate": 0.0001, "interest_rate": 0.0001},
            "top_trader_ratio": {"ratio": 1.85, "at_utc": iso(as_of_ms),
                                 "percentile_7d": 44.0, "samples": 168},
        }
    with open(canned_path, "wb") as fh:
        fh.write((json.dumps(canned, indent=1, sort_keys=True) + "\n").encode("utf-8"))
    manifest = {"as_of_ms": int(as_of_ms), "as_of_utc": iso(as_of_ms),
                "date": iso(as_of_ms)[:10], "assets": list(symbols),
                "spans_days": spans, "script_version": SCRIPT_VERSION,
                "purpose": "F-B3 determinism + F-B6/F-B7/F-B8 harness; frozen "
                           "klines/funding + canned Tier-2 (A1.7)"}
    with open(fx, "wb") as fh:
        fh.write((json.dumps(manifest, indent=1, sort_keys=True) + "\n").encode("utf-8"))
    # Pinned manifest for the FENCED substrate (operator ruling 2026-07-27):
    # the slices themselves stay out of git under charter section 10, so this
    # file is what makes a rebuild verifiable instead of merely plausible.
    slices = fixture_slice_manifest(cache)
    pinned = dict(manifest)
    pinned.update({
        "slices": slices,
        "slice_count": len(slices),
        "total_bytes": sum(v["bytes"] for v in slices.values()),
        "fencing": "The frozen klines/funding under data_cache/ are NOT "
                   "committed: charter section 10 / build prompt invariant 9 "
                   "forbid committing raw candles, and .gitignore data_cache/ "
                   "enforces it. This manifest pins every slice by sha256 so a "
                   "rebuild is verifiable. Precedent: the CENSUS-1b substrate is "
                   "fenced the same way.",
        "rebuild": "scripts/daily_brief.py --build-fixture %s" % iso(as_of_ms)[:10],
    })
    with open(FIXTURE_MANIFEST, "wb") as fh:
        fh.write((json.dumps(pinned, indent=1, sort_keys=True) + "\n").encode("utf-8"))
    for p, n in written:
        log(f"  fixture {p.name}: {n} rows, {p.stat().st_size} bytes")
    log(f"  pinned {len(slices)} slices ({pinned['total_bytes']} bytes) in "
        f"{FIXTURE_MANIFEST.name} — substrate fenced, not committed")
    return fx


def load_fixture(log=print):
    fx, canned_path, cache = fixture_paths()
    if not fx.exists():
        raise SystemExit(f"no fixture at {fx} — run --build-fixture first")
    manifest = json.loads(fx.read_text(encoding="utf-8"))
    canned = json.loads(canned_path.read_text(encoding="utf-8"))
    if FIXTURE_MANIFEST.exists():
        verify_fixture_slices(
            cache, json.loads(FIXTURE_MANIFEST.read_text(encoding="utf-8")),
            log=log)
    os.environ["NAIAD_CACHE_DIR"] = str(cache)   # the loaders read the frozen slice
    return manifest, canned


def run_fixture_day(log=print):
    """One frozen-day build: no network, canned Tier-2, frozen 'now'."""
    manifest, canned = load_fixture(log=log)
    doc, runs = build_brief(manifest["assets"], manifest["as_of_ms"],
                            tier2_canned=canned, prev_index_line=None, log=log)
    doc["runtime_seconds"] = "n/a (fixture)"      # keep F-B3 byte-comparable
    doc["fixture"] = manifest
    return doc, runs


# ══════════════════════════════════════════════════════════════ fixtures

FORBIDDEN_KEY_TOKENS = ("size", "qty", "notional", "leverage", "contracts")


def walk_keys(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield k
            yield from walk_keys(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from walk_keys(v)


def fb1_recompute(doc, log):
    """F-B1: independently recompute a VWAP distance, a VAH and an RSI.

    Each is recomputed by a DIFFERENT code path than the one that produced the
    published number — plain arithmetic here, so agreement is evidence rather
    than tautology.
    """
    sym = doc["universe"][0]
    a = doc["assets"][sym]
    now_ms = int(datetime.strptime(doc["as_of_utc"], "%Y-%m-%dT%H:%M:%SZ")
                 .replace(tzinfo=timezone.utc).timestamp() * 1000)
    k1h = dl.load_klines(sym, "1h", 0, now_ms).reset_index(drop=True)
    checks = []

    # (1) rolling 30d VWAP distance, by direct summation
    m = k1h["open_time"].to_numpy(np.int64) >= now_ms - 30 * DAY_MS
    tp = ((k1h["high"].to_numpy(float) + k1h["low"].to_numpy(float)
           + k1h["close"].to_numpy(float)) / 3.0)[m]
    vv = k1h["volume"].to_numpy(float)[m]
    mine = float((tp * vv).sum() / vv.sum())
    price = a["price"]
    mine_bps = (price - mine) / abs(mine) * 1e4
    pub = a["vwap"]["rolling"]["30d"]["distance_bps"]
    checks.append(("vwap30d_distance_bps", pub, round(mine_bps, 2)))

    # (2) prior-day VAH, by an explicit per-bar accumulation loop
    sub = a["volume_profile"]["substrate"]
    src = dl.load_klines(sym, sub, 0, now_ms).reset_index(drop=True)
    today = day_floor(now_ms)
    sl = src[(src["open_time"] >= today - DAY_MS) & (src["open_time"] < today)]
    lo_a, hi_a = sl["low"].to_numpy(float), sl["high"].to_numpy(float)
    v_a = sl["volume"].to_numpy(float)
    keep = np.isfinite(lo_a) & np.isfinite(hi_a) & np.isfinite(v_a) & (v_a > 0)
    lo_a, hi_a, v_a = lo_a[keep], hi_a[keep], v_a[keep]
    lo, hi = float(lo_a.min()), float(hi_a.max())
    edges = np.linspace(lo, hi, VP_BINS + 1)
    prof = np.zeros(VP_BINS)
    for a0, b0, v0 in zip(lo_a, hi_a, v_a):          # different algorithm
        if b0 <= a0:
            j = min(max(int(np.searchsorted(edges, a0, side="right") - 1), 0), VP_BINS - 1)
            prof[j] += v0
            continue
        d = v0 / (b0 - a0)
        for j in range(VP_BINS):
            ov = min(edges[j + 1], b0) - max(edges[j], a0)
            if ov > 0:
                prof[j] += d * ov
    total = prof.sum()
    poc_i = int(np.argmax(prof))
    li = hi_i = poc_i
    acc = prof[poc_i]
    while acc < VALUE_AREA * total and (li > 0 or hi_i < VP_BINS - 1):
        dn = prof[li - 1] if li > 0 else -1.0
        up = prof[hi_i + 1] if hi_i < VP_BINS - 1 else -1.0
        if up >= dn:
            hi_i += 1
            acc += prof[hi_i]
        else:
            li -= 1
            acc += prof[li]
    checks.append(("prior_day_vah", a["volume_profile"]["prior_day"]["vah"],
                   round(float(edges[hi_i + 1]), 8)))

    # (3) 4h RSI(14) Wilder, by an explicit recursive loop
    b4 = resample(k1h, "4h")
    c = b4["close"].to_numpy(float)
    ag = al = None
    gains, losses = [], []
    for i in range(1, len(c)):
        ch = c[i] - c[i - 1]
        gains.append(max(ch, 0.0))
        losses.append(max(-ch, 0.0))
    for i, (g, l) in enumerate(zip(gains, losses)):
        ag = g if ag is None else ag + (g - ag) / 14.0
        al = l if al is None else al + (l - al) / 14.0
    rsi = 100.0 if al == 0 else 100.0 - 100.0 / (1.0 + ag / al)
    checks.append(("rsi_4h", a["rsi"]["timeframes"]["4h"]["value"], round(rsi, 4)))

    ok = True
    for name, pub_v, mine_v in checks:
        if pub_v is None:
            ok = False
            log(f"      {name}: published None")
            continue
        rel = abs(pub_v - mine_v) / max(abs(pub_v), 1e-12)
        good = rel <= 1e-9
        ok &= good
        log(f"      {name}: published {pub_v} vs recomputed {mine_v} "
            f"(rel {rel:.2e}) {'ok' if good else 'MISMATCH'}")
    return ok, f"{len(checks)} numbers recomputed by independent arithmetic on {sym}"


def fb2_json_html(doc, log):
    """F-B2: HTML is built from the JSON only; spot-assert 10 sampled values."""
    h = render_html(doc)
    pool = [("rules_sha256", doc["rules_sha256"][:12]), ("date", doc["date"])]
    for sym in doc["universe"]:
        a = doc["assets"].get(sym)
        if not a:
            continue
        pool += [
            (f"{sym}.price", num(a["price"], 4)),
            (f"{sym}.vwap_M", num(a["vwap"]["anchored"]["M"]["vwap"], 4)),
            (f"{sym}.rsi_4h", num(a["rsi"]["timeframes"].get("4h", {}).get("value"), 2)),
            (f"{sym}.daily_verdict", a["bias"]["daily"]["verdict"]),
            (f"{sym}.radar_state", a["radar"][0]["state"] if a["radar"] else None),
            (f"{sym}.setup_invalidation",
             num(a["radar"][0]["setup_invalidation"], 4) if a["radar"] else None),
        ]
    samples = [(n, v) for n, v in pool if v and v != "—"][:10]
    if len(samples) < 10:
        return False, f"only {len(samples)} renderable values available to sample"
    missing = [n for n, v in samples if esc(v) not in h]
    for n, v in samples:
        log(f"      {n} -> '{v}' {'found' if esc(v) in h else 'MISSING'}")
    return not missing, (f"{len(samples)} JSON values found verbatim in the "
                         f"{len(h)}-char HTML, which is built from the JSON only")


def fb3_determinism(log):
    """F-B3: two frozen-day runs, byte-identical modulo generated_utc.

    The cache override is restored afterwards: run_fixture_day() repoints
    NAIAD_CACHE_DIR at the frozen slice, and leaking that would make every LATER
    fixture read fixture data instead of the estate it is supposed to audit
    (F-B4 would then compare live published numbers against frozen ones).
    """
    prev = os.environ.get("NAIAD_CACHE_DIR")
    try:
        d1, _ = run_fixture_day(log=lambda *a, **k: None)
        d2, _ = run_fixture_day(log=lambda *a, **k: None)
    finally:
        if prev is None:
            os.environ.pop("NAIAD_CACHE_DIR", None)
        else:
            os.environ["NAIAD_CACHE_DIR"] = prev
    s1, s2 = serialize_json(d1), serialize_json(d2)
    strip = lambda s: "\n".join(l for l in s.splitlines()
                                if '"generated_utc"' not in l)
    h1, h2 = render_html(d1), render_html(d2)
    hstrip = lambda s: s.replace(d1["generated_utc"], "").replace(d2["generated_utc"], "")
    json_same = strip(s1) == strip(s2)
    html_same = hstrip(h1) == hstrip(h2)
    log(f"      json {len(strip(s1))} chars identical={json_same} · "
        f"html {len(h1)} chars identical={html_same}")
    return json_same and html_same, "two frozen-day runs byte-identical (json + html)"


def fb4_funding_grids(doc, log):
    """F-B4: SOL cadence switches integrated per record, never 3/day."""
    sym = "SOLUSDT" if "SOLUSDT" in doc["universe"] else doc["universe"][0]
    now_ms = int(datetime.strptime(doc["as_of_utc"], "%Y-%m-%dT%H:%M:%SZ")
                 .replace(tzinfo=timezone.utc).timestamp() * 1000)
    fu = dl.load_funding(sym, 0, now_ms)
    t = fu["funding_time"].to_numpy(np.int64)
    gaps = np.diff(t)
    hours = sorted({int(round(g / 3_600_000)) for g in gaps})
    non_8h = [h for h in hours if h != 8]
    win = t[t >= now_ms - 7 * DAY_MS]
    published = doc["assets"][sym]["funding"]["records_7d"]
    naive = 3 * 7
    ok = (published == len(win)) and bool(non_8h)
    log(f"      cache read: {dl.cache_dir()}")
    log(f"      {sym}: observed gap hours over full history {hours} "
        f"(non-8h present={bool(non_8h)})")
    log(f"      records in trailing 7d: published {published} vs actual "
        f"{len(win)} (a 3/day assumption would say {naive})")
    return ok, (f"{sym} integrated from {len(t)} timestamped records; "
                f"cadences {hours}h observed")


def fb5_firewall(log):
    """F-B5: import audit + source audit. No journals, no outcome joins."""
    import ast
    src_path = Path(__file__).resolve()
    src = src_path.read_text(encoding="utf-8")
    tree = ast.parse(src)
    mods = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for al in node.names:
                mods.add(al.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            mods.add(node.module)
    banned = {"engine.journal", "engine.trading", "engine.replay", "engine.s1",
              "engine.s2", "engine.shadows"}
    hit = sorted(m for m in mods if m in banned or m.endswith(".journal"))
    engine_mods = sorted(m for m in mods if m.startswith("engine"))
    # source audit: no journal path reads, no outcome-join vocabulary
    lowered = src.lower()
    bad_tokens = [t for t in ("journals", "realized_r", "pnl_usd", "equity_after",
                              "win_rate", "expectancy")
                  if t in lowered.replace("no outcome joins", "")
                  and f'"{t}"' not in lowered]
    log(f"      engine imports: {engine_mods}")
    log(f"      banned imports present: {hit or 'none'}")
    log(f"      outcome-join tokens present: {bad_tokens or 'none'}")
    return (not hit) and (not bad_tokens), \
        f"{len(engine_mods)} engine modules imported, all read-only; no journal path"


def fb6_degradation(doc, log):
    """F-B6: mocked-failing fetches still render, with degraded chips."""
    import requests

    class Boom(Exception):
        pass

    orig = requests.get

    def fail(*a, **k):
        raise Boom("network disabled by F-B6")
    requests.get = fail
    try:
        t2 = fetch_tier2("BTCUSDT", None)
    finally:
        requests.get = orig
    degraded = bool(t2.get("degraded")) and t2.get("provenance") == "stale"
    probe = json.loads(serialize_json(doc))
    sym = probe["universe"][0]
    probe["assets"][sym]["tier2"] = t2
    h = render_html(probe)
    chip_shown = "degraded:" in h
    log(f"      degraded flags: {t2.get('degraded')} · provenance="
        f"{t2.get('provenance')} · chip rendered={chip_shown}")
    return degraded and chip_shown, "all Tier-2 fetches failed; brief still renders"


def fb7_radar_nosizing(doc, runs, log):
    """F-B7: independent state recomputation + no sizing keys anywhere."""
    mismatches = []
    n = 0
    for sym, lens_runs in runs.items():
        published = {r["lens"]: r["state"] for r in doc["assets"][sym]["radar"]}
        for lens, run in lens_runs.items():
            if run is None:
                continue
            n += 1
            again = recompute_state_independently(run)
            if published.get(lens) != again:
                mismatches.append((sym, lens, published.get(lens), again))
    keys = set(walk_keys(doc))
    bad = sorted(k for k in keys
                 if any(t in k.lower() for t in FORBIDDEN_KEY_TOKENS))
    # A1.2 makes invalidation mandatory and A1.9 makes it a PASS criterion, so
    # it is asserted here rather than left to an external check.
    no_inval = [(s, r["lens"], r["state"])
                for s, a in doc["assets"].items() for r in a["radar"]
                if r["setup_invalidation"] is None
                and r["campaign_invalidation"] is None]
    total_rows = sum(len(a["radar"]) for a in doc["assets"].values())
    log(f"      radar rows recomputed: {n} · mismatches: {mismatches or 'none'}")
    log(f"      forbidden key tokens {list(FORBIDDEN_KEY_TOKENS)}: {bad or 'none'}")
    log(f"      rows printing an invalidation: {total_rows - len(no_inval)}"
        f"/{total_rows}{'' if not no_inval else '  MISSING ' + str(no_inval)}")
    if mismatches or bad or no_inval:
        return False, (f"{len(mismatches)} state mismatch(es) {mismatches}; "
                       f"forbidden keys {bad}; rows without invalidation {no_inval}")
    return True, (f"{n} radar states independently confirmed; {total_rows}/"
                  f"{total_rows} rows print an invalidation; 0 sizing keys "
                  f"among {len(keys)} distinct keys")


def fb8_index_roundtrip(doc, json_path, index_path, log):
    """F-B8: index line rebuilt from the JSON alone, byte-identical; sha256
    verified by binary re-read; one brief_lookup.py query returns the day."""
    import subprocess
    reread = json.loads(Path(json_path).read_bytes().decode("utf-8"))
    line_a = index_line_from_json(doc, json_path)
    line_b = index_line_from_json(reread, json_path)
    ba = json.dumps(line_a, sort_keys=True, ensure_ascii=True).encode("utf-8")
    bb = json.dumps(line_b, sort_keys=True, ensure_ascii=True).encode("utf-8")
    same = ba == bb
    sha_again = sha256_file(json_path)
    sha_ok = sha_again == line_a["json_sha256"]
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "brief_lookup.py"),
                        "--index", str(index_path), "--date", doc["date"]],
                       capture_output=True, text=True)
    found = doc["date"] in (r.stdout or "")
    log(f"      rebuilt line {len(ba)} bytes, byte-equal={same} · "
        f"json_sha256 re-read ok={sha_ok}")
    log(f"      brief_lookup.py --date {doc['date']}: "
        f"{'returned the day' if found else 'DID NOT return the day'} "
        f"(exit {r.returncode})")
    return same and sha_ok and found, "index line round-trips from JSON alone"


def run_fixtures(doc, runs, json_path, index_path, log=print):
    results = []
    for name, fn in (
            ("F-B1", lambda: fb1_recompute(doc, log)),
            ("F-B2", lambda: fb2_json_html(doc, log)),
            ("F-B3", lambda: fb3_determinism(log)),
            ("F-B4", lambda: fb4_funding_grids(doc, log)),
            ("F-B5", lambda: fb5_firewall(log)),
            ("F-B6", lambda: fb6_degradation(doc, log)),
            ("F-B7", lambda: fb7_radar_nosizing(doc, runs, log)),
            ("F-B8", lambda: fb8_index_roundtrip(doc, json_path, index_path, log))):
        log(f"  {name}…")
        try:
            ok, detail = fn()
        except Exception as e:                      # a fixture error is a FAIL
            ok, detail = False, f"{type(e).__name__}: {e}"
        results.append((name, ok, detail))
        log(f"{'PASS' if ok else 'FAIL'} {name} - {detail}")
    return results


# ══════════════════════════════════════════════════════════════ main

def main():
    ap = argparse.ArgumentParser(description="Naiad Daily Brief")
    ap.add_argument("--fixture", action="store_true",
                    help="build the frozen fixture day (no network)")
    ap.add_argument("--fixtures-only", action="store_true",
                    help="run F-B1..F-B8 against the fixture day and exit")
    ap.add_argument("--build-fixture", metavar="UTC_DATE",
                    help="builder utility: freeze tests/brief_fixture from cache")
    ap.add_argument("--no-topup", action="store_true",
                    help="skip the network top-up (use the cache as-is)")
    ap.add_argument("--assets", help="comma-separated subset of the basket")
    ap.add_argument("--no-fixtures", action="store_true",
                    help="skip the fixture suite (not a contract-valid run)")
    args = ap.parse_args()
    t0 = time.time()

    if args.build_fixture:
        as_of = int(datetime.strptime(args.build_fixture, "%Y-%m-%d")
                    .replace(tzinfo=timezone.utc).timestamp() * 1000)
        build_fixture(as_of)
        print("fixture built")
        return 0

    if args.fixture or args.fixtures_only:
        print("frozen fixture day (no network, canned Tier-2)")
        doc, runs = run_fixture_day()
        out = FIXTURE_DIR / "out"
        jp, hp = write_outputs(doc, out)
        print(f"wrote {jp} ({jp.stat().st_size} bytes) and {hp} "
              f"({hp.stat().st_size} bytes)")
        fx_index = write_index(index_line_from_json(doc, jp),
                               out / "brief_index.jsonl")
        results = run_fixtures(doc, runs, jp, fx_index)
        failed = [n for n, ok, _ in results if not ok]
        print(f"{len(results) - len(failed)}/{len(results)} fixtures pass")
        return 1 if failed else 0

    symbols = ([s.strip() for s in args.assets.split(",")] if args.assets
               else list(SYMBOLS))
    now_ms = int(time.time() * 1000)

    if not args.no_topup:
        print("top-up (contract §2: refresh to the latest closed bar)…")
        for sym in symbols:
            for tf in ("1m", "5m", "15m", "1h", "4h", "12h"):
                try:
                    dl.backfill_klines(sym, tf, now_ms - 10 * DAY_MS, now_ms,
                                       log=lambda *a, **k: None)
                except Exception as e:
                    print(f"  WARN {sym} {tf} top-up: {type(e).__name__}: {e}")
            try:
                dl.backfill_funding(sym, now_ms - 30 * DAY_MS, now_ms,
                                    log=lambda *a, **k: None)
            except Exception as e:
                print(f"  WARN {sym} funding top-up: {type(e).__name__}: {e}")
        print(f"  top-up done in {time.time()-t0:.0f}s")

    prev = read_last_index_line(before_date=iso(now_ms)[:10])
    print("layers…")
    doc, runs = build_brief(symbols, now_ms, prev_index_line=prev)
    jp, hp = write_outputs(doc)
    line = index_line_from_json(doc, jp)
    write_index(line)
    print(f"wrote {jp}")
    print(f"wrote {hp} ({hp.stat().st_size} bytes)")
    print(f"index {INDEX_PATH} (date {line['date']}, json_sha256 "
          f"{line['json_sha256'][:12]})")

    ok = True
    if not args.no_fixtures:
        print("fixtures…")
        results = run_fixtures(doc, runs, jp, INDEX_PATH)
        failed = [n for n, o, _ in results if not o]
        ok = not failed
        print(f"{len(results) - len(failed)}/{len(results)} fixtures pass")
        if failed:
            print("HALT: " + ", ".join(failed) + " failed — no partial adoption "
                  "(A1.9)")

    print("\nheadline biases:")
    for sym in doc["universe"]:
        a = doc["assets"].get(sym)
        if not a:
            continue
        states = "/".join(r["state"] for r in a["radar"])
        print(f"  {sym:<14} daily {a['bias']['daily']['verdict']:<14} "
              f"weekly {a['bias']['weekly']['verdict']:<14} radar {states}")
    print(f"\ntotal runtime {time.time()-t0:.0f}s")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
