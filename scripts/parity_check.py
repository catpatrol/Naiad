#!/usr/bin/env python
"""parity_check.py -- emit OUR value for exactly the candles the operator read.

    C:\\venvs\\naiad\\Scripts\\python.exe scripts/parity_check.py --demo
    C:\\venvs\\naiad\\Scripts\\python.exe scripts/parity_check.py --spec spec.json
    C:\\venvs\\naiad\\Scripts\\python.exe scripts/parity_check.py \\
        --ask BTCUSDT,1d,2026-08-01T00:00Z,rsi14

PURPOSE.  Adoption is gated on the operator's parity readings matching ours
(Amendment §0).  When his chart captures arrive, the comparison must be ONE SMALL
PASTE, not an afternoon of re-deriving what we computed and when.

THE TWO THINGS THAT MAKE A PARITY COMPARISON MEANINGLESS, both handled here:

1.  COMPARING DIFFERENT BARS.  A chart read mid-period shows the FORMING candle;
    everything here is computed on CLOSED buckets only, via
    analytics.structure.resample_ohlcv.  So the tool takes the candle's
    open time explicitly and prints the exact bar it evaluated, in UTC.  If the
    operator's reading is of a forming bar, that shows up as a named mismatch
    rather than as a mysterious few-percent difference.

2.  COMPARING DIFFERENT RECIPES.  Every measure prints the pinned recipe it
    used, so a disagreement can be attributed to the recipe rather than argued
    about.  RVWAP in particular is TradingView's published algorithm with
    volume-weighted POPULATION variance and no (n-1) correction -- an ordinary
    standard deviation produces plausible numbers that never match his chart.

This tool COMPUTES; it does not judge.  It has no tolerance and no pass/fail,
because what counts as a match is the operator's call, not the builder's.
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import analytics                                                    # noqa: E402
from analytics import momentum as M                                 # noqa: E402
from analytics import profile as P                                  # noqa: E402
from analytics import structure as S                                # noqa: E402
from analytics import volatility as V                               # noqa: E402
from analytics import vwap as W                                     # noqa: E402
from engine.data import cache_dir                                   # noqa: E402

HOUR_MS = 3_600_000
DAY_MS = 86_400_000
STEP_MS = {"1m": 60_000, "5m": 300_000, "15m": 900_000, "1h": HOUR_MS,
           "4h": 4 * HOUR_MS, "12h": 12 * HOUR_MS, "1d": DAY_MS,
           "1w": 7 * DAY_MS}
NATIVE = ("1m", "5m", "15m", "1h")

RECIPES = {
    "close": "last CLOSED candle close",
    "rsi14": "RSI(14), Wilder/RMA smoothing, source close",
    "atr14": "ATR(14), Wilder smoothing of true range",
    "ema": "EMA, alpha=2/(len+1), seeded with SMA(len) at index len-1",
    "sma": "SMA",
    "macd": "MACD(12,26,9) line / signal / histogram, source close",
    "ao": "Awesome Oscillator, SMA(5)-SMA(34) of (H+L)/2",
    "stoch_rsi": "StochRSI: RSI(14) -> stoch(14) -> %K sma3 -> %D sma3",
    "rvwap": ('TradingView "Rolling VWAP": trailing W-millisecond window floored '
              'at 10 bars, src hlc3, volume-weighted POPULATION variance via '
              'max(E[x^2]-E[x]^2, 0), NO (n-1) correction'),
    "avwap": ('Anchored VWAP accumulated from the period open (param W/M/Q/Y), '
              'src hlc3, SAME volume-weighted POPULATION variance as the '
              'rolling form -- VERIFIED (R4), no longer inferred'),
    "poc": "windowed volume profile POC, 120 rows, VA 70%, volume spread "
           "uniformly across each bar's range (APPROXIMATION)",
    "vah": "windowed volume profile VAH (70% value area)",
    "val": "windowed volume profile VAL (70% value area)",
}


def _iso(ms):
    return datetime.fromtimestamp(int(ms) / 1000, timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ")


def _parse_utc(s):
    s = s.strip().replace("Z", "+00:00")
    dt = datetime.fromisoformat(s)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return int(dt.timestamp() * 1000)


def _load(symbol, tf):
    """Bars at `tf`, closed buckets only, resampled from native where needed."""
    kd = cache_dir() / "klines"
    if tf in NATIVE and (kd / f"{symbol}_{tf}.parquet").exists():
        df = pd.read_parquet(kd / f"{symbol}_{tf}.parquet")
        return {c: df[c].to_numpy(np.int64 if c == "open_time" else float)
                for c in ("open_time", "open", "high", "low", "close", "volume")}, tf
    base = None
    for cand in ("1h", "15m", "5m", "1m"):
        if (kd / f"{symbol}_{cand}.parquet").exists():
            base = cand
            break
    if base is None:
        raise SystemExit(f"no klines for {symbol}")
    df = pd.read_parquet(kd / f"{symbol}_{base}.parquet")
    r = S.resample_ohlcv(df["open_time"].to_numpy(np.int64),
                         *[df[c].to_numpy(float) for c in
                           ("open", "high", "low", "close", "volume")],
                         STEP_MS[tf])
    return r, f"{base}->{tf} (closed buckets only)"


def evaluate(symbol, tf, candle_open_utc, measure, param=None):
    """Our value for ONE measure at ONE candle.  Never guesses which bar."""
    want_ms = _parse_utc(candle_open_utc)
    bars, substrate = _load(symbol, tf)
    t = np.asarray(bars["open_time"], dtype="int64")

    idx = int(np.searchsorted(t, want_ms))
    exact = idx < len(t) and int(t[idx]) == want_ms
    if not exact:
        idx = max(0, min(idx - 1, len(t) - 1))

    row = {"symbol": symbol, "timeframe": tf, "measure": measure,
           "param": param,
           "requested_candle_utc": _iso(want_ms),
           "evaluated_candle_utc": _iso(int(t[idx])),
           "exact_candle_match": bool(exact),
           "substrate": substrate,
           "bars_available": int(len(t)),
           "last_closed_candle_utc": _iso(int(t[-1])),
           "recipe": RECIPES.get(measure, "UNKNOWN MEASURE"),
           "closed_bars_only": True,
           "analytics_version": analytics.ANALYTICS_VERSION}
    if not exact:
        row["note"] = ("no candle opens at the requested time; evaluated the "
                       "closest EARLIER closed candle. If your chart showed a "
                       "later bar it was still forming.")

    c = np.asarray(bars["close"], float)[:idx + 1]
    h = np.asarray(bars["high"], float)[:idx + 1]
    l = np.asarray(bars["low"], float)[:idx + 1]
    v = np.asarray(bars["volume"], float)[:idx + 1]
    tt = t[:idx + 1]

    def val(x):
        x = float(x)
        return None if not np.isfinite(x) else x

    if measure == "close":
        row["value"] = val(c[-1])
    elif measure == "rsi14":
        row["value"] = val(M.rsi(c, 14)[-1])
    elif measure == "atr14":
        row["value"] = val(V.atr(h, l, c, 14)[-1])
    elif measure == "ema":
        row["value"] = val(M.ema(c, int(param or 21))[-1])
    elif measure == "sma":
        row["value"] = val(M.sma(c, int(param or 20))[-1])
    elif measure == "macd":
        line, sig, hist = M.macd(c)
        row["value"] = val(line[-1])
        row["extra"] = {"signal": val(sig[-1]), "histogram": val(hist[-1])}
    elif measure == "ao":
        row["value"] = val(M.awesome_oscillator(h, l)[-1])
    elif measure == "stoch_rsi":
        k_, d_ = M.stoch_rsi(c)
        row["value"] = val(k_[-1])
        row["extra"] = {"%K": val(k_[-1]), "%D": val(d_[-1])}
    elif measure == "rvwap":
        wd = float(param or 7)
        rv = W.rolling_vwap(tt, W.hlc3(h, l, c), v, wd, sigmas=(1, 2, 3))
        row["value"] = val(rv["vwap"][-1])
        # ALL THREE triples, not just +/-1s.  The operator reads six band values
        # per VWAP off the chart; emitting one pair meant four of every six
        # numbers he supplied could not be compared at all.
        row["extra"] = {"sigma": val(rv["stdev"][-1]), "window_days": wd,
                        "bars_in_window": int(np.count_nonzero(
                            tt > tt[-1] - wd * DAY_MS)),
                        "substrate_pinned": W.VWAP_SUBSTRATE,
                        "source_pinned": W.VWAP_SOURCE}
        for k in (1, 2, 3):
            row["extra"][f"+{k}s"] = val(rv[f"band_up_{k}"][-1])
            row["extra"][f"-{k}s"] = val(rv[f"band_dn_{k}"][-1])
        row["lockbox_overlap"] = analytics.lockbox_overlap(
            int(tt[-1]) - int(wd * DAY_MS), int(tt[-1]))
    elif measure == "avwap":
        # Anchored to the UTC period open containing the evaluated bar.  The
        # anchor is DERIVED from the bar, never passed in, so a parity row can
        # never silently compare two different anchors.
        period = str(param or "M").upper()
        dt = datetime.fromtimestamp(int(tt[-1]) / 1000, timezone.utc)
        if period == "W":
            a = dt - pd.Timedelta(days=dt.weekday())
            a = a.replace(hour=0, minute=0, second=0, microsecond=0)
        elif period == "M":
            a = dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        elif period == "Q":
            a = dt.replace(month=((dt.month - 1) // 3) * 3 + 1, day=1,
                           hour=0, minute=0, second=0, microsecond=0)
        elif period == "Y":
            a = dt.replace(month=1, day=1, hour=0, minute=0, second=0,
                           microsecond=0)
        else:
            raise SystemExit(f"avwap param must be W/M/Q/Y, got {period!r}")
        a_ms = int(a.timestamp() * 1000)
        sel = np.flatnonzero(tt >= a_ms)
        if not len(sel):
            raise SystemExit(f"no bars at or after the {period} anchor {_iso(a_ms)}")
        a0 = int(sel[0])
        av = W.anchored_vwap(W.hlc3(h, l, c), v, a0, sigmas=(1, 2, 3))
        nbars = len(tt) - a0
        row["value"] = val(av["vwap"][-1])
        row["extra"] = {"sigma": val(av["stdev"][-1]), "period": period,
                        "anchor_utc": _iso(a_ms),
                        "anchor_bar_utc": _iso(int(tt[a0])),
                        "bars_since_anchor": int(nbars),
                        "maturity": W.maturity(nbars),
                        "substrate_pinned": W.VWAP_SUBSTRATE,
                        "source_pinned": W.VWAP_SOURCE}
        for k in (1, 2, 3):
            row["extra"][f"+{k}s"] = val(av[f"band_up_{k}"][-1])
            row["extra"][f"-{k}s"] = val(av[f"band_dn_{k}"][-1])
    elif measure in ("poc", "vah", "val"):
        wd = float(param or 30)
        wp = P.windowed_profile(tt, h, l, v, wd, int(tt[-1]), substrate=str(substrate))
        row["value"] = None if wp.get("warming") else val(wp[measure])
        row["extra"] = {"window_days": wd, "warming": bool(wp.get("warming")),
                        "rows": P.PROFILE_ROWS, "value_area": P.VALUE_AREA,
                        "approximation": P.APPROXIMATION}
        row["lockbox_overlap"] = wp.get("lockbox_overlap")
    else:
        raise SystemExit(f"unknown measure {measure!r}; known: {sorted(RECIPES)}")
    return row


def _print(rows):
    print(f"{'symbol':<13}{'tf':<5}{'measure':<11}{'candle (UTC)':<22}"
          f"{'our value':>16}  exact")
    print("-" * 82)
    for r in rows:
        v = r["value"]
        vs = "n/a (warming)" if v is None else f"{v:,.6f}".rstrip("0").rstrip(".")
        print(f"{r['symbol']:<13}{r['timeframe']:<5}{r['measure']:<11}"
              f"{r['evaluated_candle_utc']:<22}{vs:>16}  "
              f"{'yes' if r['exact_candle_match'] else 'NO'}")
        if r.get("extra"):
            print(f"{'':>31}  {r['extra']}")
        if r.get("note"):
            print(f"{'':>31}  ! {r['note']}")


def demo(symbol="BTCUSDT"):
    """Three most recent CLOSED 1d candles, so the output format is visible."""
    bars, _ = _load(symbol, "1d")
    t = np.asarray(bars["open_time"], dtype="int64")
    rows = []
    for ms in t[-3:]:
        for meas, param in (("close", None), ("rsi14", None), ("atr14", None),
                            ("rvwap", 30), ("poc", 30), ("stoch_rsi", None)):
            rows.append(evaluate(symbol, "1d", _iso(int(ms)), meas, param))
    return rows


def main():
    ap = argparse.ArgumentParser(description="Parity comparison helper")
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--symbol", default="BTCUSDT")
    ap.add_argument("--spec", help="JSON file: [{symbol,timeframe,candle_utc,"
                                   "measure,param}, ...]")
    ap.add_argument("--ask", action="append",
                    help="SYMBOL,TF,CANDLE_UTC,MEASURE[,PARAM]  (repeatable)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    rows = []
    if args.demo:
        rows = demo(args.symbol)
    elif args.spec:
        for s in json.loads(Path(args.spec).read_text(encoding="utf-8")):
            rows.append(evaluate(s["symbol"], s["timeframe"], s["candle_utc"],
                                 s["measure"], s.get("param")))
    elif args.ask:
        for a in args.ask:
            p = [x.strip() for x in a.split(",")]
            rows.append(evaluate(p[0], p[1], p[2], p[3],
                                 p[4] if len(p) > 4 else None))
    else:
        ap.print_help()
        print("\nknown measures:", ", ".join(sorted(RECIPES)))
        return 0

    if args.json:
        print(json.dumps(rows, indent=1, default=str))
    else:
        _print(rows)
        print("\nEvery value above is computed on CLOSED bars only. If a reading "
              "disagrees,\ncheck the candle column FIRST -- a chart read "
              "mid-period shows the forming bar.")
        print("No tolerance is applied here: what counts as a match is the "
              "operator's call.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
