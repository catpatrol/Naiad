"""S-2 — instrumented pass 2 of the 20-cell grid, run TWICE (contract §12.5).

Engine 1.0.9, config v12_anchor_g8 (UNCHANGED), TC-4 windows verbatim.
Roots:
    research_outputs/s1/journal_s2/scored/<cell>/       + s2_events/
    research_outputs/s1/journal_s2_run2/scored/<cell>/  + s2_events_run2/

journal_pass1/journal_pass2 are read-only history; existing S-1 roots abort
(the idempotent merge must never mask non-determinism).

    .venv/Scripts/python.exe scripts/s2_runner.py [--workers N]
"""
import argparse
import hashlib
import json
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

CONFIG = "v12_anchor_g8"
END = "2024-06-30T23:59"
OUT = ROOT / "research_outputs" / "s2"
RESAMPLED = ROOT / "research_outputs" / "s1" / "resampled"

CELLS = {
    "BTCUSDT_intraday": "2019-10-01", "BTCUSDT_position": "2020-01-01",
    "BTCUSDT_swing": "2019-11-01", "ETHUSDT_intraday": "2020-01-01",
    "ETHUSDT_position": "2020-04-01", "ETHUSDT_swing": "2020-01-01",
    "JTOUSDT_intraday": "2024-01-01", "JTOUSDT_position": "2024-04-01",
    "JTOUSDT_swing": "2024-02-01", "NEARUSDT_intraday": "2020-11-01",
    "NEARUSDT_position": "2021-02-01", "NEARUSDT_swing": "2020-12-01",
    "SOLUSDT_intraday": "2020-10-01", "SOLUSDT_position": "2021-01-01",
    "SOLUSDT_swing": "2020-11-01", "TAOUSDT_intraday": "2024-05-01",
    "TAOUSDT_swing": "2024-06-01", "ZECUSDT_intraday": "2020-03-01",
    "ZECUSDT_position": "2020-06-01", "ZECUSDT_swing": "2020-04-01",
}
ORDER = sorted(CELLS, key=lambda c: ({"intraday": 0, "position": 1,
                                      "swing": 2}[c.rsplit("_", 1)[1]],
                                     CELLS[c]))


def one_cell(journal_root: str, sidecar_root: str, cell_id: str) -> dict:
    from engine.replay import run_replay
    t0 = time.time()
    s = run_replay(CONFIG, cell_id, CELLS[cell_id], END, Path(journal_root),
                   backfill=False, log=lambda *a, **k: None,
                   s2_sidecar_root=Path(sidecar_root),
                   s2_resampled_dir=RESAMPLED)
    s["cell_id"] = cell_id
    s["elapsed_s"] = round(time.time() - t0, 1)
    return s


def run_pass(jname: str, ename: str, workers: int) -> dict:
    jroot = OUT / jname / "scored"
    eroot = OUT / ename
    for r in (jroot, eroot):
        if r.exists():
            raise SystemExit(f"{r} exists — refusing (determinism guard).")
    results = {}
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(one_cell, str(jroot), str(eroot), c): c
                for c in ORDER}
        for fut in as_completed(futs):
            s = fut.result()
            results[s["cell_id"]] = s
            print(f"[{jname}] {s['cell_id']:<18} rows={s['rows']:>6} "
                  f"side={s['sidecar_rows']:>6} "
                  f"jsha={s['journal_sha256'][:10]} "
                  f"ssha={s['sidecar_sha256'][:10]} {s['elapsed_s']}s "
                  f"({len(results)}/20, t+{time.time()-t0:.0f}s)", flush=True)
    return results


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=2)
    args = ap.parse_args()
    p1 = run_pass("journal_s2", "s2_events", args.workers)
    p2 = run_pass("journal_s2_run2", "s2_events_run2", args.workers)

    from engine.version import ENGINE_VERSION
    all_match = True
    table = {}
    for c in sorted(CELLS):
        m = (p1[c]["journal_sha256"] == p2[c]["journal_sha256"]
             and p1[c]["sidecar_sha256"] == p2[c]["sidecar_sha256"]
             and p1[c]["rows"] == p2[c]["rows"])
        all_match &= m
        table[c] = {
            "start": CELLS[c], "end": END, "run_id": p1[c]["run_id"],
            "rows": p1[c]["rows"], "sidecar_rows": p1[c]["sidecar_rows"],
            "journal_sha256": p1[c]["journal_sha256"],
            "sidecar_sha256": p1[c]["sidecar_sha256"],
            "rerun_journal_sha256": p2[c]["journal_sha256"],
            "rerun_sidecar_sha256": p2[c]["sidecar_sha256"],
            "match": m,
        }
        print(f"{c:<18} {'MATCH' if m else '*** MISMATCH ***'}", flush=True)
    manifest = {
        "phase": "S-2 instrumented pass 2 (corrected simulator + new families)",
        "contract": "S2_Instrumented_Pass_Builder_Contract.md",
        "engine_version": ENGINE_VERSION,
        "config_id": CONFIG,
        "config_sha256": hashlib.sha256(
            (ROOT / "configs" / f"{CONFIG}.yaml").read_bytes()).hexdigest(),
        "baseline": "research_outputs/tc4/journal_pass2 (engine 1.0.8); s1 joined from journal_s1, not re-emitted",
        "s1_flag": "runner parameter (s1_sidecar_root + s1_resampled_dir); "
                   "config unchanged",
        "data_source": "census estate + research_outputs/s1/resampled, "
                       "offline, backfill=False both passes",
        "determinism_all_identical": all_match,
        "cells": table,
    }
    (OUT / "manifest.json").write_text(
        json.dumps(manifest, indent=1, sort_keys=True) + "\n",
        encoding="utf-8", newline="\n")
    print(f"\nDETERMINISM: {'ALL IDENTICAL' if all_match else 'MISMATCH'}")
    return 0 if all_match else 1


if __name__ == "__main__":
    raise SystemExit(main())
