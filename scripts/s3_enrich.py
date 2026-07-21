"""S-3 — Cell-B Enrichment & Cross-Run Excursion Substrate (contract
S3_Enrichment_Builder_Contract.md). Tier B: instrumentation only, engine
1.0.11 UNCHANGED — the TC-1 runner's run_replay is called WITH the s2 capture
params (s2_sidecar_root set) over the tc1_B config. signals.py + trading.py
byte-untouched (F-BYTE enforces it behaviorally). J-1 stays out a fifth time
(byte-identity requires it), disclosed.

    .venv/Scripts/python.exe scripts/s3_enrich.py run [--workers N]
    .venv/Scripts/python.exe scripts/s3_enrich.py analyze

`run`     — the winning cell-B book over the 20-cell grid, TWICE for
            determinism, capture on, into research_outputs/s3/.
`analyze` — fixtures (F-BYTE first) then deliverables D1–D6, the scorecard,
            s3_results.json, s3_excursion_substrate.jsonl, S3_ENRICHMENT.md.

The runner spawns worker processes (Windows spawn re-imports this module), so
`one_cell` imports only from engine — never edit this file while `run` is in
flight.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

CONFIG = "tc1_B"
END = "2024-06-30T23:59"
OUT = ROOT / "research_outputs" / "s3"
RESAMPLED = ROOT / "research_outputs" / "s1" / "resampled"
REF = ROOT / "research_outputs" / "tc1" / "B_run1" / "scored"   # F-BYTE baseline
CONFIG_SHA = "3e99401d427fedd96842cc4df15c329220b8ec43e93bd6543c62de7acb3f636b"

# TC-1 grid windows, verbatim (tc1_runner.py / s2_runner.py).
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
    "ZECUSDT_position": "2020-06-01", "ZECUSDT_swing": "2020-04-01"}
ORDER = sorted(CELLS, key=lambda c: ({"intraday": 0, "position": 1,
                                      "swing": 2}[c.rsplit("_", 1)[1]],
                                     CELLS[c]))


# ══════════════════════════════════════════════════════════ runner
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


def _complete(jname: str) -> bool:
    root = OUT / jname / "scored"
    if not root.exists():
        return False
    return sum(1 for c in ORDER if (root / c).exists()
               and any((root / c).glob("*.jsonl"))) == 20


def run_pass(jname: str, ename: str, workers: int) -> dict:
    jroot = OUT / jname / "scored"
    eroot = OUT / ename
    if _complete(jname):
        print(f"[{jname}] already complete — re-reading summaries from disk",
              flush=True)
        return {c: _cell_summary(jroot, eroot, c) for c in ORDER}
    for r in (OUT / jname, eroot):
        if r.exists():
            import shutil
            shutil.rmtree(r)
            print(f"[{jname}] partial — cleared, re-running", flush=True)
    results = {}
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(one_cell, str(jroot), str(eroot), c): c
                for c in ORDER}
        for fut in as_completed(futs):
            s = fut.result()
            results[s["cell_id"]] = s
            print(f"[{jname}] {s['cell_id']:<18} rows={s['rows']:>6} "
                  f"side={s['sidecar_rows']:>6} tr={s['tranches']:>5} "
                  f"jsha={s['journal_sha256'][:10]} "
                  f"ssha={s['sidecar_sha256'][:10]} {s['elapsed_s']}s "
                  f"({len(results)}/20, t+{time.time()-t0:.0f}s)", flush=True)
    return results


def _cell_summary(jroot: Path, eroot: Path, cell: str) -> dict:
    """rows / sha for an already-persisted pass (resume path)."""
    from engine.journal import files_sha256, count_lines
    jf = sorted((jroot / cell).glob("*.jsonl"))
    ef = eroot / f"{cell}.jsonl"
    tr = sum(1 for p in jf for l in open(p, encoding="utf-8")
             if l.strip() and json.loads(l)["evt"] in ("ENTRY_FILL", "ADD_FILL"))
    return {"cell_id": cell, "rows": count_lines(jf),
            "sidecar_rows": (count_lines([ef]) if ef.exists() else 0),
            "tranches": tr, "journal_sha256": files_sha256(jf),
            "sidecar_sha256": (files_sha256([ef]) if ef.exists() else "-"),
            "run_id": "-", "final_equity": None, "elapsed_s": 0.0}


def cmd_run(workers: int) -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    p1 = run_pass("journal_s3", "s3_events", workers)
    p2 = run_pass("journal_s3_run2", "s3_events_run2", workers)

    from engine.version import ENGINE_VERSION
    all_match = True
    table = {}
    for c in ORDER:
        m = (p1[c]["journal_sha256"] == p2[c]["journal_sha256"]
             and p1[c]["sidecar_sha256"] == p2[c]["sidecar_sha256"]
             and p1[c]["rows"] == p2[c]["rows"])
        all_match &= m
        table[c] = {
            "start": CELLS[c], "end": END, "rows": p1[c]["rows"],
            "sidecar_rows": p1[c]["sidecar_rows"], "tranches": p1[c]["tranches"],
            "journal_sha256": p1[c]["journal_sha256"],
            "sidecar_sha256": p1[c]["sidecar_sha256"],
            "rerun_journal_sha256": p2[c]["journal_sha256"],
            "rerun_sidecar_sha256": p2[c]["sidecar_sha256"], "match": m}
        print(f"{c:<18} {'MATCH' if m else '*** MISMATCH ***'}", flush=True)
    manifest = {
        "phase": "S-3 cell-B enrichment & cross-run excursion substrate",
        "contract": "S3_Enrichment_Builder_Contract.md",
        "engine_version": ENGINE_VERSION, "config_id": CONFIG,
        "config_sha256": CONFIG_SHA,
        "capture": "s2 family ON via runner param (s2_sidecar_root); "
                   "signals.py + trading.py byte-untouched",
        "baseline_for_F_BYTE": "research_outputs/tc1/B_run1 (engine 1.0.11, "
                               "capture off)",
        "j1_status": "OUT (fifth carry, disclosed) — byte-identity requires it",
        "determinism_all_identical": all_match, "cells": table}
    (OUT / "manifest.json").write_text(
        json.dumps(manifest, indent=1, sort_keys=True) + "\n",
        encoding="utf-8", newline="\n")
    print(f"\nDETERMINISM: {'ALL IDENTICAL' if all_match else 'MISMATCH'}")
    return 0 if all_match else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    pr = sub.add_parser("run")
    pr.add_argument("--workers", type=int, default=4)
    sub.add_parser("analyze")
    args = ap.parse_args()
    if args.cmd == "run":
        return cmd_run(args.workers)
    if args.cmd == "analyze":
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from s3_analyze import run_analysis
        return run_analysis()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
