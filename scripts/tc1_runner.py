"""TC-1 — Stop × Exit factorial runner. Cell A first (byte-identity gate),
then B/C/D each twice (determinism). Engine 1.0.11, standard 20-cell grid.

Roots research_outputs/tc1/{A, B_run1, B_run2, C_run1, C_run2, D_run1,
D_run2}/scored/<grid_cell>/. Prior roots read-only. F-A-BYTE aborts B/C/D
if cell A is not byte-identical to journal_pass2.

    .venv/Scripts/python.exe scripts/tc1_runner.py [--workers N]
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

END = "2024-06-30T23:59"
PASS2 = ROOT / "research_outputs" / "tc4" / "journal_pass2" / "scored"
OUT = ROOT / "research_outputs" / "tc1"
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


def one(config_id: str, journal_root: str, cell: str) -> dict:
    from engine.replay import run_replay
    t0 = time.time()
    s = run_replay(config_id, cell, CELLS[cell], END, Path(journal_root),
                   backfill=False, log=lambda *a, **k: None)
    s["cell"] = cell
    s["elapsed_s"] = round(time.time() - t0, 1)
    return s


def complete(name: str) -> bool:
    root = OUT / name / "scored"
    if not root.exists():
        return False
    return sum(1 for d in root.iterdir() if d.is_dir()
               and any(d.glob("*.jsonl"))) == 20


def cell_meta(name: str, cell: str) -> dict:
    """rows/final_equity/halts/tranches/sha from a persisted journal (resume:
    an arm completed in a prior job is read, not re-run)."""
    root = OUT / name / "scored"
    rows = tr = halts = 0
    last_eq = None
    for p in sorted((root / cell).glob("*.jsonl")):
        for line in open(p, encoding="utf-8"):
            if not line.strip():
                continue
            rows += 1
            r = json.loads(line)
            if r["evt"] in ("ENTRY_FILL", "ADD_FILL"):
                tr += 1
            elif r["evt"] == "EXIT" and r["equity_after"] is not None:
                last_eq = r["equity_after"]
            elif r["evt"] == "HALT":
                halts += 1
    return {"rows": rows, "final_equity": last_eq, "halts": halts,
            "tranches": tr, "journal_sha256": sha_root(root, cell),
            "cell": cell}


def run_grid(config_id: str, name: str, workers: int) -> dict:
    root = OUT / name / "scored"
    if complete(name):
        print(f"[{name}] already complete — reading from disk", flush=True)
        return {c: cell_meta(name, c) for c in ORDER}
    if root.exists():
        import shutil
        shutil.rmtree(OUT / name)
        print(f"[{name}] partial — cleared, re-running", flush=True)
    res = {}
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(one, config_id, str(root), c): c for c in ORDER}
        for fut in as_completed(futs):
            s = fut.result()
            res[s["cell"]] = s
            print(f"[{name}] {s['cell']:<18} rows={s['rows']:>6} "
                  f"eq={s['final_equity']:>10} halts={s['halts']} "
                  f"sha={s['journal_sha256'][:10]} {s['elapsed_s']}s "
                  f"({len(res)}/20, t+{time.time()-t0:.0f}s)", flush=True)
    return res


def _norm(line):
    r = json.loads(line)
    r.pop("s1", None); r.pop("s2", None)
    r["run_id"] = r["engine_version"] = r["config_id"] = "-"
    return json.dumps(r, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False)


def f_a_byte(a_root: Path) -> tuple[bool, list]:
    mism = []
    for cell in ORDER:
        a = [_norm(l) for p in sorted((a_root / cell).glob("*.jsonl"))
             for l in open(p, encoding="utf-8") if l.strip()]
        b = [_norm(l) for p in sorted((PASS2 / cell).glob("*.jsonl"))
             for l in open(p, encoding="utf-8") if l.strip()]
        if a != b:
            mism.append((cell, len(a), len(b)))
    return not mism, mism


def sha_root(root: Path, cell: str) -> str:
    h = hashlib.sha256()
    for p in sorted((root / cell).glob("*.jsonl"), key=lambda p: p.name):
        h.update(p.read_bytes())
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=2)
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)

    # ── Cell A first — byte-identity gate ──
    a = run_grid("tc1_A", "A", args.workers)
    ok, mism = f_a_byte(OUT / "A" / "scored")
    print(f"\nF-A-BYTE: {'PASS' if ok else 'FAIL'} {mism[:5]}", flush=True)
    if not ok:
        print("*** HALT: cell A not byte-identical — config gating broken. "
              "B/C/D not run. ***")
        (OUT / "manifest.json").write_text(json.dumps(
            {"f_a_byte": False, "mismatches": mism}, indent=1) + "\n",
            encoding="utf-8")
        return 1

    from engine.version import ENGINE_VERSION
    manifest = {"phase": "TC-1 stop x exit factorial", "f_a_byte": True,
                "engine_version": ENGINE_VERSION, "window_end": END,
                "cells": {}}
    manifest["cells"]["A"] = {c: {"sha256": a[c]["journal_sha256"],
                                  "rows": a[c]["rows"],
                                  "final_equity": a[c]["final_equity"],
                                  "halts": a[c]["halts"]} for c in ORDER}

    det_ok = True
    for cfg, name in (("tc1_B", "B"), ("tc1_C", "C"), ("tc1_D", "D")):
        r1 = run_grid(cfg, f"{name}_run1", args.workers)
        r2 = run_grid(cfg, f"{name}_run2", args.workers)
        cellrec = {}
        for c in ORDER:
            m = (r1[c]["journal_sha256"] == r2[c]["journal_sha256"]
                 and r1[c]["rows"] == r2[c]["rows"])
            det_ok &= m
            cellrec[c] = {"sha256": r1[c]["journal_sha256"],
                          "rerun_sha256": r2[c]["journal_sha256"],
                          "match": m, "rows": r1[c]["rows"],
                          "final_equity": r1[c]["final_equity"],
                          "halts": r1[c]["halts"],
                          "tranches": r1[c]["tranches"]}
            print(f"{name} {c:<18} {'MATCH' if m else '*** MISMATCH ***'}",
                  flush=True)
        manifest["cells"][name] = cellrec
    manifest["determinism_all_identical"] = det_ok
    manifest["config_shas"] = {
        f"tc1_{k}": hashlib.sha256(
            (ROOT / "configs" / f"tc1_{k}.yaml").read_bytes()).hexdigest()
        for k in ("A", "B", "C", "D")}
    (OUT / "manifest.json").write_text(
        json.dumps(manifest, indent=1, sort_keys=True) + "\n",
        encoding="utf-8", newline="\n")
    print(f"\nF-A-BYTE PASS · DETERMINISM "
          f"{'ALL IDENTICAL' if det_ok else 'MISMATCH'}")
    return 0 if det_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
