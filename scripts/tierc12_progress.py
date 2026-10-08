#!/usr/bin/env python
"""TIER-C12 · the PROGRESS ledger merge (orchestrator bookkeeping).

Builds research_outputs/tierc12/PROGRESS.json from the per-stage records under research_outputs/tierc12/progress/.
The stage builders write those records and never PROGRESS.json itself (ORCHESTRATOR_RULINGS O-6). The merge is
pure: stages are ordered by the plan's stage order, every record is carried verbatim, and the header names the
records of record by sha. It computes no number of any book. The pattern is TC11-X's (tc11x_progress.py).

Run:  ~/venvs/naiad/bin/python -B /Users/luis/Naiad/scripts/tierc12_progress.py
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "research_outputs" / "tierc12"
CONTRACT = "exchange/queue/2026-10-08_TC12_APOLLO.md"
ORDER = ["STEP Q", "TC12-R0", "TC12-LEANS", "TC12-REG", "TC12-D", "TC12-ENV", "TC12-V", "TC12-C", "TC12-G",
         "TC12-R", "TC12-S", "TC12-L", "TC12-SCORE", "TC12-FIX", "TC12-REVIEW", "TC12-CLOSE"]
STATUSES = ("COMPLETE-VERIFIED", "PARTIAL", "ABSENT")


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def stage_key(rec: dict, name: str) -> tuple:
    st = str(rec.get("stage", name))
    base = next((o for o in sorted(ORDER, key=len, reverse=True) if st.startswith(o)), st)
    return (ORDER.index(base) if base in ORDER else len(ORDER), name)


def pointer(rel: str) -> dict | None:
    p = OUT / rel
    return {"path": str(p.relative_to(ROOT)), "sha256": sha(p)} if p.exists() else None


def main() -> None:
    recs = []
    for p in sorted((OUT / "progress").glob("*.json")):
        rec = json.loads(p.read_text())
        if rec.get("status") not in STATUSES:
            raise SystemExit(f"HALT: {p.name} carries status {rec.get('status')!r}; legal: {STATUSES}")
        rec["_record"] = {"path": str(p.relative_to(ROOT)), "sha256": sha(p)}
        recs.append((stage_key(rec, p.stem), rec))
    stages = [r for _, r in sorted(recs, key=lambda t: t[0])]
    pin = OUT / "data" / "AS_OF_PIN.json"
    doc = {
        "tier": "TIER-C12",
        "branch": "v12-v1-census",
        "seed": 20261008,
        "contract_of_record": {"path": CONTRACT, "sha256": sha(ROOT / CONTRACT)},
        "rulings_of_record": pointer("ORCHESTRATOR_RULINGS.md"),
        "leans_of_record": pointer("LEANS.md"),
        "amendments_of_record": pointer("LEANS_AMENDMENTS.md"),
        "registrations_of_record": pointer("registrations/REGISTRY_PIN.json"),
        "as_of_pin": json.loads(pin.read_text()) if pin.exists() else None,
        "law_1_note": "a stage is COMPLETE only if its artifacts exist, manifest shas verify, and its fixtures RE-PASS now.",
        "merge_law": "stage records are written by the builders under progress/ and merged here verbatim, in plan order",
        "stages": stages,
    }
    (OUT / "PROGRESS.json").write_text(json.dumps(doc, indent=2, ensure_ascii=False, sort_keys=False) + "\n")
    for s in stages:
        print(f"{s.get('stage')!s:<16} {s.get('status')}")


if __name__ == "__main__":
    main()
