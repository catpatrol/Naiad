"""v12 Study V1 operator spot check (deliverable D5).

  python scripts/spot_check.py                    # SPOT_CHECK.md, 30 rows
  python scripts/spot_check.py --escalate SOLUSDT # 10-row sheet, one asset

Selection is deterministic (fixed seed) and NEVER touches the lockbox: rows
come from the exploration-classic era (window floored at 2022-01-01, keeping
clear of the Naiad pre-2022 sealed retro holdout) and the spent/regime-
contaminated era. Values are read through the guarded study loader, so a
lockbox read here would raise, not print.
"""

import argparse
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from study import loader
from study.loader import load_study_klines, partition_class, utc_str

ROOT = Path(__file__).resolve().parent.parent
SEED = 20260710

EXPL_START_MS = 1_640_995_200_000     # 2022-01-01T00:00Z (retro-holdout guard)
EXPL_END_MS = loader.LOCKBOX_START_MS - 1
CONTAM_START_MS = loader.LOCKBOX_END_EXCL_MS
CONTAM_END_MS = loader.EDGE_EXCL_MS - 1

# (era, interval) plan per asset: >=1 exploration + >=1 recent era where
# history allows; HYPE/FARTCOIN list inside the lockbox and LIT floors at
# 2025-12-23, so their sheets are contaminated-era only. All six intervals
# appear across the 30 rows; deep-history LTF rows stay in the recent era so
# TradingView can actually reach them.
PLAN = {
    "BTCUSDT": [("expl", "12h"), ("recent", "5m"), ("expl", "4h")],
    "ETHUSDT": [("expl", "4h"), ("recent", "15m"), ("expl", "1h")],
    "SOLUSDT": [("expl", "12h"), ("recent", "1m"), ("expl", "1h")],
    "NEARUSDT": [("expl", "4h"), ("recent", "5m"), ("expl", "12h")],
    "ZECUSDT": [("expl", "1h"), ("recent", "15m"), ("expl", "12h")],
    "JTOUSDT": [("expl", "4h"), ("recent", "5m"), ("expl", "1h")],
    "TAOUSDT": [("expl", "4h"), ("recent", "15m"), ("expl", "12h")],
    "HYPEUSDT": [("recent", "4h"), ("recent", "1h"), ("recent", "15m")],
    "FARTCOINUSDT": [("recent", "4h"), ("recent", "1h"), ("recent", "5m")],
    "LITUSDT": [("recent", "4h"), ("recent", "1h"), ("recent", "15m")],
}

ESCALATE_INTERVALS = ["12h", "4h", "1h", "15m", "5m", "1m"]

HEADER = """# SPOT_CHECK — v12 Study, Phase V1 (deliverable D5)

**Escalation rule (read first):** compare every row against TradingView. If
ANY price value (O/H/L/C) mismatches on an asset, that asset fails: tell the
builder, which must regenerate a 10-row escalation sheet for that asset
(`python scripts/spot_check.py --escalate SYMBOL`) and investigate before the
phase can pass. Tiny volume differences can occur; prices must match.

How to check a row: open the TradingView symbol given in the row (Binance
USDT-M perpetual, the `.P` symbol), set the row's timeframe, scroll/jump to
the exact UTC open time, hover the candle, compare open/high/low/close/volume.
Make sure your TradingView chart timezone is set to UTC.

No row in this sheet is a lockbox candle (2024-07-01 → 2025-10-05): printing
lockbox OHLCV would violate the seal. Exploration rows are drawn from
2022-01-01 onward, keeping clear of the pre-2022 sealed retro holdout.

| # | Symbol | TF | Open (UTC) | Open | High | Low | Close | Volume | Era | Pass? |
|--:|---|---|---|---|---|---|---|---|---|---|"""


def fmt(x: float) -> str:
    """Shortest round-trip decimal — exchange precision, no float64 noise."""
    return repr(x)


def pick_row(rng, symbol: str, interval: str, era: str) -> dict | None:
    if era == "expl":
        lo, hi = EXPL_START_MS, EXPL_END_MS
    else:
        lo, hi = CONTAM_START_MS, CONTAM_END_MS
    df = load_study_klines(symbol, interval, lo, hi)
    if not len(df):
        return None
    r = df.iloc[int(rng.integers(0, len(df)))]
    open_ms = int(r["open_time"])
    return {
        "symbol": symbol, "interval": interval, "open_ms": open_ms,
        "open": float(r["open"]), "high": float(r["high"]),
        "low": float(r["low"]), "close": float(r["close"]),
        "volume": float(r["volume"]),
        "class": partition_class(symbol, open_ms),
    }


def render(rows: list[dict], title_note: str) -> str:
    lines = [HEADER]
    for i, r in enumerate(rows, 1):
        lines.append(
            f"| {i} | {r['symbol']} | {r['interval']} | "
            f"{utc_str(r['open_ms'])} | {fmt(r['open'])} | {fmt(r['high'])} | "
            f"{fmt(r['low'])} | {fmt(r['close'])} | {fmt(r['volume'])} | "
            f"{r['class']} |  |")
    lines += ["", "## Navigation lines", ""]
    for i, r in enumerate(rows, 1):
        lines.append(
            f"{i}. open BINANCE:{r['symbol']}.P, {r['interval']}, scroll to "
            f"{utc_str(r['open_ms'])[:-3]} UTC")
    lines += ["", title_note, ""]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--escalate", default=None, metavar="SYMBOL")
    args = ap.parse_args()

    if args.escalate:
        sym = args.escalate
        if sym not in PLAN:
            print(f"unknown study symbol {sym}"); return 1
        rng = np.random.default_rng(SEED + 1)
        eras = {e for e, _ in PLAN[sym]}
        rows = []
        k = 0
        while len(rows) < 10 and k < 40:
            iv = ESCALATE_INTERVALS[k % len(ESCALATE_INTERVALS)]
            era = ("expl" if "expl" in eras and (k % 2 == 0) else "recent")
            r = pick_row(rng, sym, iv, era)
            k += 1
            if r and r["open_ms"] not in {x["open_ms"] for x in rows
                                          if x["interval"] == iv}:
                rows.append(r)
        out = ROOT / f"SPOT_CHECK_ESCALATION_{sym}.md"
        out.write_text(render(rows, f"Escalation sheet for {sym}: 10 rows."),
                       encoding="utf-8", newline="\n")
        print(f"escalation sheet -> {out}")
        return 0

    rng = np.random.default_rng(SEED)
    rows = []
    for sym, plan in PLAN.items():
        for era, iv in plan:
            r = pick_row(rng, sym, iv, era)
            if r is None:
                print(f"WARNING: no candles for {sym} {iv} {era}")
                continue
            rows.append(r)
    out = ROOT / "SPOT_CHECK.md"
    out.write_text(
        render(rows, f"{len(rows)} rows, 3 per asset; no lockbox candles."),
        encoding="utf-8", newline="\n")
    print(f"spot check -> {out}  ({len(rows)} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
