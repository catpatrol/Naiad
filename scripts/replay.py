"""D3: deterministic replay of one cell over one window.

  python scripts/replay.py --config naiad_v0 --cell BTCUSDT_swing \
      --start 2026-05-01 --end 2026-07-07 [--backfill] [--journal-root journal]

Prints a run summary including the journal SHA-256 (two identical runs must
print the same hash — F1).
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from engine.replay import run_replay


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True, choices=["naiad_v0", "v11_faithful"])
    ap.add_argument("--cell", required=True, help="e.g. BTCUSDT_swing")
    ap.add_argument("--start", required=True, help="UTC, e.g. 2026-05-01")
    ap.add_argument("--end", required=True, help="UTC, e.g. 2026-07-07")
    ap.add_argument("--backfill", action="store_true",
                    help="top up the local cache from Binance first")
    ap.add_argument("--journal-root", default="journal")
    args = ap.parse_args()

    summary = run_replay(args.config, args.cell, args.start, args.end,
                         Path(args.journal_root), backfill=args.backfill)
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
