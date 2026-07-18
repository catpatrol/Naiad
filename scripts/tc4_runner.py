"""TC-4 — engine 1.0.8 re-anchor: the 20-cell scored grid, run TWICE.

Contract: TC4_Engine_1_0_8_Builder_Contract.md (§4/§5). Windows are the
anchor run's exactly (month-aligned starts per the v3_anchor manifest, end
2024-06-30T23:59 — no lockbox contact). Config v12_anchor_g8, offline census
estate (backfill=False), fresh journal roots:

    research_outputs/tc4/journal_pass2/scored/<cell>/        (deliverable)
    research_outputs/tc4/journal_pass2_run2/scored/<cell>/   (determinism twin)

journal_pass1 (research_outputs/v3_anchor/) is READ-ONLY history and is
never opened for writing by this script. Existing tc4 journal roots abort
the run — the idempotent journal merge must never mask non-determinism.

    .venv/Scripts/python.exe scripts/tc4_runner.py [--workers N]
"""

import argparse
import json
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

CONFIG = "v12_anchor_g8"
END = "2024-06-30T23:59"
OUT = ROOT / "research_outputs" / "tc4"

# Month-aligned starts, verbatim from the v3_anchor manifest (scored cells).
CELLS = {
    "BTCUSDT_intraday": "2019-10-01",
    "BTCUSDT_position": "2020-01-01",
    "BTCUSDT_swing": "2019-11-01",
    "ETHUSDT_intraday": "2020-01-01",
    "ETHUSDT_position": "2020-04-01",
    "ETHUSDT_swing": "2020-01-01",
    "JTOUSDT_intraday": "2024-01-01",
    "JTOUSDT_position": "2024-04-01",
    "JTOUSDT_swing": "2024-02-01",
    "NEARUSDT_intraday": "2020-11-01",
    "NEARUSDT_position": "2021-02-01",
    "NEARUSDT_swing": "2020-12-01",
    "SOLUSDT_intraday": "2020-10-01",
    "SOLUSDT_position": "2021-01-01",
    "SOLUSDT_swing": "2020-11-01",
    "TAOUSDT_intraday": "2024-05-01",
    "TAOUSDT_swing": "2024-06-01",
    "ZECUSDT_intraday": "2020-03-01",
    "ZECUSDT_position": "2020-06-01",
    "ZECUSDT_swing": "2020-04-01",
}

# Longest tapes first so the pool packs well (intraday = 1m exec dominates).
ORDER = sorted(CELLS, key=lambda c: ({"intraday": 0, "position": 1,
                                      "swing": 2}[c.rsplit("_", 1)[1]],
                                     CELLS[c]))


def one_cell(pass_root: str, cell_id: str) -> dict:
    from engine.replay import run_replay          # import inside the worker
    t0 = time.time()
    s = run_replay(CONFIG, cell_id, CELLS[cell_id], END,
                   Path(pass_root), backfill=False, log=lambda *a, **k: None)
    s["cell_id"] = cell_id
    s["elapsed_s"] = round(time.time() - t0, 1)
    return s


def run_pass(name: str, workers: int) -> dict:
    root = OUT / name / "scored"
    if root.exists():
        raise SystemExit(f"{root} already exists — refusing to merge into "
                         "an existing journal root (determinism guard).")
    results = {}
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(one_cell, str(root), c): c for c in ORDER}
        for fut in as_completed(futs):
            s = fut.result()      # a worker exception (GateViolation) halts everything
            results[s["cell_id"]] = s
            print(f"[{name}] {s['cell_id']:<18} rows={s['rows']:>6} "
                  f"eq={s['final_equity']:>10} halts={s['halts']} "
                  f"sha={s['journal_sha256'][:12]} {s['elapsed_s']}s "
                  f"({len(results)}/20, t+{time.time()-t0:.0f}s)", flush=True)
    return results


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=4)
    args = ap.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)
    p1 = run_pass("journal_pass2", args.workers)
    p2 = run_pass("journal_pass2_run2", args.workers)

    from engine.version import ENGINE_VERSION
    all_match = True
    table = {}
    for c in sorted(CELLS):
        m = p1[c]["journal_sha256"] == p2[c]["journal_sha256"] and \
            p1[c]["rows"] == p2[c]["rows"]
        all_match &= m
        table[c] = {
            "start": CELLS[c], "end": END, "run_id": p1[c]["run_id"],
            "rows": p1[c]["rows"], "sha256": p1[c]["journal_sha256"],
            "rerun_sha256": p2[c]["journal_sha256"], "match": m,
            "final_equity": p1[c]["final_equity"], "halts": p1[c]["halts"],
            "signal_events": p1[c]["signal_events"],
            "tranches": p1[c]["tranches"],
        }
        print(f"{c:<18} {'MATCH' if m else '*** MISMATCH ***'} "
              f"{p1[c]['journal_sha256'][:16]}", flush=True)

    import hashlib
    grid_hash = hashlib.sha256("".join(
        table[c]["sha256"] for c in sorted(CELLS)).encode()).hexdigest()
    manifest = {
        "phase": "TC-4 engine 1.0.8 re-anchor",
        "contract": "TC4_Engine_1_0_8_Builder_Contract.md",
        "engine_version": ENGINE_VERSION,
        "config_id": CONFIG,
        "config_sha256": hashlib.sha256(
            (ROOT / "configs" / f"{CONFIG}.yaml").read_bytes()).hexdigest(),
        "window_end": END,
        "data_source": "census-verified local estate, offline, "
                       "backfill=False both passes",
        "determinism_all_identical": all_match,
        "grid_evidence_hash": grid_hash,
        "grid_evidence_hash_formula": "sha256 over concatenation of per-cell "
                                      "journal sha256 hex digests, cells "
                                      "sorted by cell_id",
        "cells": table,
    }
    (OUT / "manifest.json").write_text(
        json.dumps(manifest, indent=1, sort_keys=True) + "\n",
        encoding="utf-8", newline="\n")
    print(f"\nDETERMINISM: {'ALL IDENTICAL' if all_match else 'MISMATCH'}")
    print(f"grid evidence hash: {grid_hash}")
    return 0 if all_match else 1


if __name__ == "__main__":
    raise SystemExit(main())
