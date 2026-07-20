"""TC-5 — intraday re-spec 1H/5m, five cells run TWICE (config-only).

Amendment 1: triple (gov 1h, exec 5m, align 1h). The v2 cells are injected
via a cell_by_id monkeypatch that constructs the Cell dataclass from the
committed configs/tc5_*.json specs — engine/ source is byte-untouched
(F-ENG proves it). Config v12_anchor_g8 (baseline architecture + G-8),
UNCHANGED. Windows = the v1 start dates (single variable = the TF triple).

Roots research_outputs/tc5/{journal_tc5, journal_tc5_run2}; prior roots
read-only. No network, no resampling (5m/1h/4h/12h native).

    .venv/Scripts/python.exe scripts/tc5_runner.py [--workers N]
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

CFG_FILES = ["tc5_btc.json", "tc5_eth.json", "tc5_sol.json",
             "tc5_near.json", "tc5_zec.json"]


def _specs():
    out = {}
    for fn in CFG_FILES:
        s = json.loads((ROOT / "configs" / fn).read_text(encoding="utf-8"))
        out[s["cell_id"]] = s
    return out


def one_cell(journal_root: str, cell_id: str) -> dict:
    # applied INSIDE the worker (Windows spawn) so the patch is live there
    import engine.replay as R
    from engine.cells import Cell
    specs = _specs()
    _orig = R.cell_by_id

    def _patched(cid):
        if cid in specs:
            s = specs[cid]
            return Cell(cell_id=cid, symbol=s["symbol"],
                        mandate=s["mandate"], tf_gov=s["tf_gov"],
                        tf_exec=s["tf_exec"], tf_align=s["tf_align"],
                        slippage_bps=s["slippage_bps"])
        return _orig(cid)
    R.cell_by_id = _patched

    s = specs[cell_id]
    t0 = time.time()
    res = R.run_replay(s["base_config"], cell_id, s["start"], s["end"],
                       Path(journal_root), backfill=False,
                       log=lambda *a, **k: None)
    res["cell_id"] = cell_id
    res["elapsed_s"] = round(time.time() - t0, 1)
    return res


def run_pass(name: str, workers: int) -> dict:
    root = ROOT / "research_outputs" / "tc5" / name / "scored"
    if root.exists():
        raise SystemExit(f"{root} exists — refusing (determinism guard).")
    specs = _specs()
    results = {}
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(one_cell, str(root), c): c for c in specs}
        for fut in as_completed(futs):
            r = fut.result()
            results[r["cell_id"]] = r
            print(f"[{name}] {r['cell_id']:<20} rows={r['rows']:>6} "
                  f"eq={r['final_equity']:>9} halts={r['halts']} "
                  f"sha={r['journal_sha256'][:12]} {r['elapsed_s']}s "
                  f"({len(results)}/5, t+{time.time()-t0:.0f}s)", flush=True)
    return results


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=3)
    args = ap.parse_args()
    out = ROOT / "research_outputs" / "tc5"
    out.mkdir(parents=True, exist_ok=True)
    p1 = run_pass("journal_tc5", args.workers)
    p2 = run_pass("journal_tc5_run2", args.workers)

    from engine.version import ENGINE_VERSION
    specs = _specs()
    all_match = True
    table = {}
    for c in sorted(specs):
        m = (p1[c]["journal_sha256"] == p2[c]["journal_sha256"]
             and p1[c]["rows"] == p2[c]["rows"])
        all_match &= m
        table[c] = {"run_id": p1[c]["run_id"], "rows": p1[c]["rows"],
                    "sha256": p1[c]["journal_sha256"],
                    "rerun_sha256": p2[c]["journal_sha256"], "match": m,
                    "final_equity": p1[c]["final_equity"],
                    "halts": p1[c]["halts"],
                    "signal_events": p1[c]["signal_events"],
                    "tranches": p1[c]["tranches"],
                    "config_sha256": hashlib.sha256(
                        (ROOT / "configs" /
                         f"tc5_{c.split('USDT')[0].lower()}.json")
                        .read_bytes()).hexdigest()}
        print(f"{c:<20} {'MATCH' if m else '*** MISMATCH ***'}", flush=True)
    manifest = {
        "phase": "TC-5 intraday re-spec 1H/5m (config-only)",
        "contract": "TC5_Intraday_Respec_Builder_Contract.md + Amendment 1",
        "engine_version": ENGINE_VERSION,
        "base_config": "v12_anchor_g8",
        "align_ruling": "tf_align=1h (governor) per Amendment 1",
        "determinism_all_identical": all_match,
        "cells": table,
    }
    (out / "manifest.json").write_text(
        json.dumps(manifest, indent=1, sort_keys=True) + "\n",
        encoding="utf-8", newline="\n")
    print(f"\nDETERMINISM: {'ALL IDENTICAL' if all_match else 'MISMATCH'}")
    return 0 if all_match else 1


if __name__ == "__main__":
    raise SystemExit(main())
