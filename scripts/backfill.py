"""Backfill Binance USDT-M klines + funding into the local cache.

Usage (see README for plain-language steps):
  python scripts/backfill.py --symbols BTCUSDT --intervals 5m,1h,4h,12h \
      --start 2023-01-01 --end 2026-07-08
  python scripts/backfill.py --all           # whole basket, all intervals,
                                             # from each symbol's first candle

Writes a coverage report to research_outputs/coverage/.
Raw candles land in the local cache only — never in the repo (invariant 9).
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from engine import data as dl
from engine.cells import INTERVALS, SYMBOLS
from engine.replay import parse_utc


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbols", default=None, help="comma-separated, e.g. BTCUSDT,ETHUSDT")
    ap.add_argument("--intervals", default=None, help="comma-separated, e.g. 5m,4h")
    ap.add_argument("--start", default=None, help="UTC date (default: first candle)")
    ap.add_argument("--end", required=True, help="UTC date, e.g. 2026-07-08")
    ap.add_argument("--all", action="store_true", help="whole basket, all intervals")
    ap.add_argument("--funding", action="store_true", help="also backfill funding history")
    args = ap.parse_args()

    symbols = list(SYMBOLS) if args.all or not args.symbols else args.symbols.split(",")
    intervals = INTERVALS if args.all or not args.intervals else args.intervals.split(",")
    end_ms = parse_utc(args.end)

    reports = []
    for sym in symbols:
        if args.funding or args.all:
            first = dl.detect_first_candle(sym, "1h") or 0
            dl.backfill_funding(sym, dl.first_valid_ms(sym, "1h", first), end_ms)
        for iv in intervals:
            detected = dl.detect_first_candle(sym, iv)
            if detected is None:
                print(f"  {sym} {iv}: no futures data — skipped")
                continue
            start_ms = parse_utc(args.start) if args.start else dl.first_valid_ms(sym, iv, detected)
            print(f"{sym} {iv}: backfilling from {dl.datetime.fromtimestamp(max(start_ms, dl.first_valid_ms(sym, iv, detected))/1000, dl.timezone.utc):%Y-%m-%d} to {args.end}")
            df = dl.backfill_klines(sym, iv, start_ms, end_ms)
            rep = dl.integrity_report(sym, iv, df)
            reports.append(rep)
            gaps = len(rep["gaps"])
            print(f"  -> {rep['bars']} bars, {rep['duplicates']} duplicates, "
                  f"{gaps} gap(s){' (exchange downtime is normal)' if gaps else ''}")

    out = Path(__file__).resolve().parent.parent / "research_outputs" / "coverage" / "coverage.json"
    dl.write_coverage_report(reports, out)
    print(f"coverage report -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
