#!/usr/bin/env python
"""parity_worksheet.py -- emit the operator's chart-parity reading sheet.

Contract v4 SS I.6.  ADOPTION OF `analytics/` IS GATED ON THIS SHEET: the numbers
below are ours, and until a human reads the same numbers off a chart and they
agree, nothing here is adopted.  That is the entire point -- a fixture proves we
compute what we intended, and only a chart proves what we intended is what the
market convention actually is.

WHAT IT EMITS
  _reviewer_box/parity_worksheet_<date>.md
    24 current-bar rows (3 assets x 8 measures) + 4 historical rows ~30 days back
    Canonical chart:  BINANCE:<SYM>USDT.P      Timezone: UTC
    CLOSED CANDLES ONLY -- see the closed-bar note below.
    RVWAP rows target TradingView's official "Rolling VWAP" indicator with a
    FIXED window of 7 / 30 / 90 / 365 days, source hlc3, bands x1.
    An optional column sits beside ours for the operator's own private RVWAP
    script, so a three-way disagreement is legible at a glance.

CLOSED CANDLES ONLY.  Resampled layers drop the forming bucket by construction
(Amendment FAN8).  For NATIVE layers this script drops the final cached bar,
because a cache written at an arbitrary moment may hold a bar still forming and
there is no way to tell from the bar alone.  Every row therefore names the exact
UTC open time it refers to; the operator reads THAT candle, not "the last one".

I/O lives here, in a script, never in analytics/ (invariant I-B).
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import analytics                                                   # noqa: E402
from analytics import momentum as M                                # noqa: E402
from analytics import structure as S                               # noqa: E402
from analytics import volatility as V                              # noqa: E402
from analytics import vwap as W                                    # noqa: E402
from engine import data as dl                                      # noqa: E402

SYMBOLS = ("BTCUSDT", "ETHUSDT", "SOLUSDT")
RVWAP_WINDOWS = (7, 30, 90, 365)
HOUR_MS = 3_600_000
DAY_MS = 86_400_000
HIST_BACK_DAYS = 30


def iso(ms):
    return datetime.fromtimestamp(int(ms) / 1000, timezone.utc).strftime(
        "%Y-%m-%d %H:%M UTC")


def fmt(x, dp=4):
    return "n/a" if x is None or x != x else f"{float(x):,.{dp}f}"


def load_closed_1h(symbol, end_ms):
    """1h klines with the final (possibly forming) bar dropped."""
    k = dl.load_klines(symbol, "1h", 0, end_ms)
    cols = ("open_time", "open", "high", "low", "close", "volume")
    arr = {c: k[c].to_numpy() for c in cols}
    if len(arr["open_time"]) >= 2:
        arr = {c: v[:-1] for c, v in arr.items()}
    return arr


def measures_at(a, idx):
    """The eight measures, evaluated as-of index `idx` of the 1h series.

    Everything is computed on the PREFIX [0..idx] so the row is exactly what a
    reader standing at that bar would have seen -- the same truncation discipline
    F-AN-13 enforces on the package itself.
    """
    t = a["open_time"][:idx + 1]
    o, h, l, c, v = (a[k][:idx + 1] for k in ("open", "high", "low", "close", "volume"))
    src = W.hlc3(h, l, c)
    rows = []

    rows.append(("close (1h)", "last closed 1h candle close", float(c[-1]), 2))
    for wd in RVWAP_WINDOWS:
        rv = W.rolling_vwap(t, src, v, wd)
        rows.append((f"RVWAP {wd}d",
                     f'TradingView "Rolling VWAP", fixed {wd} days, src hlc3',
                     float(rv["vwap"][-1]), 2))
    rows.append(("RSI(14) 1h", "native 1h, Wilder", float(M.rsi(c, 14)[-1]), 4))

    r4 = S.resample_ohlcv(t, o, h, l, c, v, 4 * HOUR_MS)
    rows.append(("RSI(14) 4h", "resampled 1h->4h, CLOSED buckets only",
                 float(M.rsi(r4["close"], 14)[-1]), 4))

    r1d = S.resample_ohlcv(t, o, h, l, c, v, DAY_MS)
    rows.append(("ATR(14) 1d", "resampled 1h->1d, CLOSED buckets only",
                 float(V.atr(r1d["high"], r1d["low"], r1d["close"], 14)[-1]), 2))
    return rows, int(t[-1])


def rvwap_band_note(a, idx):
    """One x1 band pair, so the operator can check band geometry too."""
    t = a["open_time"][:idx + 1]
    h, l, c, v = (a[k][:idx + 1] for k in ("high", "low", "close", "volume"))
    rv = W.rolling_vwap(t, W.hlc3(h, l, c), v, 7)
    return float(rv["band_up_1"][-1]), float(rv["band_dn_1"][-1])


def build(end_ms=None):
    if end_ms is None:
        end_ms = int(datetime.now(timezone.utc).timestamp() * 1000)

    data = {s: load_closed_1h(s, end_ms) for s in SYMBOLS}
    for s, a in data.items():
        if len(a["open_time"]) < 400:
            raise SystemExit(f"{s}: only {len(a['open_time'])} closed 1h bars -- "
                             "not enough history for a 365d RVWAP row")

    out = []
    out.append("# PARITY WORKSHEET — analytics/ vs the chart")
    out.append("")
    out.append(f"**Generated** {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')} "
               f"· `scripts/parity_worksheet.py`")
    out.append(f"**ANALYTICS_VERSION** `{analytics.ANALYTICS_VERSION}` · "
               f"**analytics_sha** `{analytics.analytics_sha()}`")
    out.append("")
    out.append("## What to do with this sheet")
    out.append("")
    out.append("1. Open TradingView. For each row, load the chart named in the **Chart** column — "
               "the canonical form is `BINANCE:<SYM>USDT.P`, the perpetual, **not** the spot pair. "
               "A spot chart will disagree and the disagreement will mean nothing.")
    out.append("2. **Set the chart timezone to UTC.** Everything below is UTC. A chart in local "
               "time reads a different candle and produces a false mismatch.")
    out.append("3. Go to the exact candle named in the **As-of (UTC)** column. Every row is the "
               "value at the CLOSE of that candle. Do not read the candle currently forming.")
    out.append("4. Write what the chart says into **Operator reads**. Leave it blank if you did "
               "not check that row — a blank is honest, a guess is not.")
    out.append("5. If you have your own RVWAP script, put its number in **Your script** so a "
               "three-way disagreement is visible.")
    out.append("6. Send the sheet back with the columns filled. **Nothing in `analytics/` is "
               "adopted until this comes back.** A row that disagrees is a finding, not a "
               "rounding argument — bring it back as it is.")
    out.append("")
    out.append("### Settings that must match, or the comparison is void")
    out.append("")
    out.append("| setting | value |")
    out.append("|---|---|")
    out.append("| Chart | `BINANCE:<SYM>USDT.P` (perpetual) |")
    out.append("| Timezone | UTC |")
    out.append("| Candles | **closed only** — never the forming one |")
    out.append("| RVWAP indicator | TradingView's official **Rolling VWAP** |")
    out.append("| RVWAP window | **Fixed**, set to the days in the row (7 / 30 / 90 / 365) |")
    out.append("| RVWAP source | `hlc3` |")
    out.append("| RVWAP bands | ×1 (one standard deviation) |")
    out.append("| RSI | length 14, Wilder smoothing, source close |")
    out.append("| ATR | length 14, Wilder smoothing |")
    out.append("")
    out.append("> **Anchored-band variance — TO BE CONFIRMED BY READING.** Our anchored VWAP "
               "bands reuse the same volume-weighted *population* variance as the rolling form. "
               "That is a reasoned inference from shared TradingView band machinery, **not read "
               "from source**. It is not pinned and must not be cited as pinned. If you can read "
               "the indicator source, this is the single most valuable thing to confirm.")
    out.append("")
    out.append("> **Closed-bar note (Amendment FAN8).** Resampled rows (4h, 1d) drop the "
               "still-forming bucket, so they show the last FINISHED period. Mid-candle, a chart "
               "shows the forming one — those two SHOULD differ, and that is not a parity failure. "
               "Compare at the named as-of candle.")
    out.append("")

    # ---------------- current-bar block -----------------------------------
    out.append("## A. Current-bar rows (24)")
    out.append("")
    out.append("| # | Asset | Chart | Measure | Convention | As-of (UTC) | Ours | "
               "Operator reads | Your script |")
    out.append("|---:|---|---|---|---|---|---:|---|---|")
    n = 0
    current_rows = []
    for sym in SYMBOLS:
        a = data[sym]
        idx = len(a["open_time"]) - 1
        rows, asof = measures_at(a, idx)
        for name, conv, val, dp in rows:
            n += 1
            out.append(f"| {n} | {sym} | `BINANCE:{sym}.P` | {name} | {conv} | "
                       f"{iso(asof)} | **{fmt(val, dp)}** |  |  |")
            current_rows.append({"n": n, "asset": sym, "measure": name,
                                 "convention": conv, "as_of_utc": iso(asof),
                                 "ours": val})
    out.append("")

    # ---------------- historical block ------------------------------------
    out.append(f"## B. Historical rows (4) — about {HIST_BACK_DAYS} days back")
    out.append("")
    out.append("These exist to catch an error that only shows up away from the right edge. "
               "Same instructions; scroll back to the named candle.")
    out.append("")
    out.append("| # | Asset | Chart | Measure | Convention | As-of (UTC) | Ours | "
               "Operator reads | Your script |")
    out.append("|---:|---|---|---|---|---|---:|---|---|")
    hist_rows = []
    a = data["BTCUSDT"]
    back = int(np.searchsorted(a["open_time"],
                               a["open_time"][-1] - HIST_BACK_DAYS * DAY_MS))
    back = max(back, 400)
    rows, asof = measures_at(a, back)
    wanted = ("close (1h)", "RVWAP 7d", "RSI(14) 1h", "ATR(14) 1d")
    for name, conv, val, dp in rows:
        if name not in wanted:
            continue
        n += 1
        out.append(f"| {n} | BTCUSDT | `BINANCE:BTCUSDT.P` | {name} | {conv} | "
                   f"{iso(asof)} | **{fmt(val, dp)}** |  |  |")
        hist_rows.append({"n": n, "asset": "BTCUSDT", "measure": name,
                          "convention": conv, "as_of_utc": iso(asof), "ours": val})
    out.append("")

    # ---------------- band geometry ---------------------------------------
    out.append("## C. Band geometry spot-check (RVWAP 7d, ×1)")
    out.append("")
    out.append("| Asset | As-of (UTC) | Upper ×1 (ours) | Lower ×1 (ours) | "
               "Operator reads upper | Operator reads lower |")
    out.append("|---|---|---:|---:|---|---|")
    for sym in SYMBOLS:
        a = data[sym]
        idx = len(a["open_time"]) - 1
        up, dn = rvwap_band_note(a, idx)
        out.append(f"| {sym} | {iso(int(a['open_time'][idx]))} | **{fmt(up, 2)}** | "
                   f"**{fmt(dn, 2)}** |  |  |")
    out.append("")
    out.append("---")
    out.append("")
    out.append(f"**Rows to read: {len(current_rows)} current + {len(hist_rows)} historical "
               f"= {len(current_rows) + len(hist_rows)}**, plus {len(SYMBOLS)} band pairs.")
    out.append("")
    out.append("**Adoption remains gated on this sheet coming back.** No partial adoption: "
               "CENSUS-2b, CENSUS-1d and H-RVX all wait behind it.")

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    box = ROOT / "_reviewer_box"
    box.mkdir(exist_ok=True)
    path = box / f"parity_worksheet_{stamp}.md"
    path.write_text("\n".join(out) + "\n", encoding="utf-8")
    return path, current_rows, hist_rows


def main():
    path, cur, hist = build()
    print(f"wrote {path.relative_to(ROOT).as_posix()}")
    print(f"current-bar rows : {len(cur)}")
    print(f"historical rows  : {len(hist)}")
    print(f"total rows       : {len(cur) + len(hist)}")
    print(f"ANALYTICS_VERSION: {analytics.ANALYTICS_VERSION}")
    print(f"analytics_sha    : {analytics.analytics_sha()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
