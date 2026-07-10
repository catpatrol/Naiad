"""D6: the (dormant) forward-collector tick — Phase 1.5's engine.

One tick = for each active cell: top up the kline/funding cache, then re-run
the SAME deterministic replay (one engine, one code path — charter §10) from
the cell's paper epoch to the last closed exec bar, merging rows into the
journal idempotently. Overlapping or missed runs cannot duplicate or corrupt
rows (invariant 11); the practical effect is a rolling re-scan in which only
recent months' files change.

The paper epoch is set once per cell, on the cell's first-ever tick, to the
UTC month start of that first run — and then read from state forever after
(state/{cell_id}.json). Frozen rules + fixed epoch = every tick recomputes
the same journal prefix byte-for-byte and extends it.

  python scripts/tick.py --config naiad_v0 [--cells BTCUSDT_swing,...]
      [--journal-root journal] [--state-root state]

Exit code 0 even when single cells fail (their error lands in state), so one
sick symbol cannot silence the rest of the grid.
"""

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from engine.cells import INTERVAL_MS, all_cells, cell_by_id
from engine.replay import WarmupError, run_replay
from engine.version import ENGINE_VERSION


def month_start_iso(ms: int) -> str:
    d = datetime.fromtimestamp(ms / 1000, timezone.utc)
    return d.strftime("%Y-%m-01")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="naiad_v0")
    ap.add_argument("--cells", default=None,
                    help="comma-separated cell ids (default: whole grid)")
    ap.add_argument("--journal-root", default="journal")
    ap.add_argument("--state-root", default="state")
    args = ap.parse_args()

    cells = ([cell_by_id(c) for c in args.cells.split(",")] if args.cells
             else all_cells())
    state_root = Path(args.state_root)
    state_root.mkdir(parents=True, exist_ok=True)
    now_ms = int(time.time() * 1000)

    failures = 0
    for cell in cells:
        state_path = state_root / f"{cell.cell_id}.json"
        state = json.loads(state_path.read_text()) if state_path.exists() else {}
        epoch = state.get("paper_epoch") or month_start_iso(now_ms)
        step = INTERVAL_MS[cell.tf_exec]
        last_closed_ms = (now_ms // step) * step - step
        end = datetime.fromtimestamp(last_closed_ms / 1000, timezone.utc) \
            .strftime("%Y-%m-%dT%H:%M")
        try:
            summary = run_replay(args.config, cell.cell_id, epoch, end,
                                 Path(args.journal_root), backfill=True,
                                 log=lambda *_: None)
            state = {"cell_id": cell.cell_id, "paper_epoch": epoch,
                     "last_end": end, "engine_version": ENGINE_VERSION,
                     "config_id": args.config, "run_id": summary["run_id"],
                     "journal_sha256": summary["journal_sha256"],
                     "rows": summary["rows"], "halts": summary["halts"],
                     "final_equity": summary["final_equity"], "error": None}
            print(f"{cell.cell_id}: ok — {summary['rows']} rows, "
                  f"equity {summary['final_equity']}")
        except WarmupError as e:
            state = {"cell_id": cell.cell_id, "paper_epoch": epoch,
                     "engine_version": ENGINE_VERSION, "error": f"warmup: {e}"}
            print(f"{cell.cell_id}: warm-up floor not met — skipped (normal "
                  f"for young listings)")
        except Exception as e:  # one sick cell must not silence the grid
            failures += 1
            state = {"cell_id": cell.cell_id, "paper_epoch": epoch,
                     "engine_version": ENGINE_VERSION, "error": repr(e)}
            print(f"{cell.cell_id}: FAILED — {e!r}")
        state_path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n",
                              encoding="utf-8", newline="\n")

    print(f"tick complete: {len(cells)} cell(s), {failures} failure(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
