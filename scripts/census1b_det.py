"""CENSUS-1b — F1b-DET determinism check + build_manifest emission.

Compares the pass-1 artifacts against the pass-2 (--run2) artifacts.

NORMALIZATION DISCLOSURE: `census1b_results.json` carries two wall-clock timing
fields that cannot be byte-stable across runs — top-level `elapsed_s` and
`D6b_adverse_zone.elapsed_s`. F1b-DET normalizes exactly those two fields and
requires byte-identity everywhere else. `census1b_termini_enriched.jsonl` is
compared RAW (no normalization) and must be byte-identical outright.
Precedent: CENSUS-1's F-BYTE normalized three run-identity stamps.

Usage:
  .venv/Scripts/python.exe scripts/census1b_det.py
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
R1 = ROOT
R2 = ROOT / "research_outputs" / "census1b_run2"
OUT = ROOT / "research_outputs" / "census1b"

NORMALIZED = ["elapsed_s", "D6b_adverse_zone.elapsed_s",
              "D5b_enriched_dataset.path"]


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def normalize(d: dict) -> dict:
    d = json.loads(json.dumps(d, sort_keys=True))
    d.pop("elapsed_s", None)
    if "D6b_adverse_zone" in d:
        d["D6b_adverse_zone"].pop("elapsed_s", None)
    if "D5b_enriched_dataset" in d:
        d["D5b_enriched_dataset"].pop("path", None)
    return d


def main() -> int:
    j1 = R1 / "census1b_results.json"
    j2 = R2 / "census1b_results.json"
    e1 = R1 / "census1b_termini_enriched.jsonl"
    e2 = R2 / "census1b_termini_enriched.jsonl"
    for p in (j1, j2, e1, e2):
        if not p.exists():
            print(f"MISSING: {p}")
            return 2

    n1 = normalize(json.loads(j1.read_text(encoding="utf-8")))
    n2 = normalize(json.loads(j2.read_text(encoding="utf-8")))
    b1 = json.dumps(n1, sort_keys=True).encode()
    b2 = json.dumps(n2, sort_keys=True).encode()
    json_ok = (b1 == b2)

    s1 = sha256_file(e1); s2 = sha256_file(e2)
    enr_ok = (s1 == s2)

    diffs = []
    if not json_ok:
        def walk(a, b, path=""):
            if isinstance(a, dict) and isinstance(b, dict):
                for k in sorted(set(a) | set(b)):
                    walk(a.get(k), b.get(k), f"{path}.{k}" if path else k)
            elif isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
                for i, (x, y) in enumerate(zip(a, b)):
                    walk(x, y, f"{path}[{i}]")
            elif a != b:
                diffs.append(f"{path}: {a!r} != {b!r}")
        walk(n1, n2)

    status = "MATCH" if (json_ok and enr_ok) else "MISMATCH"
    res = {
        "fixture": "F1b-DET",
        "status": status,
        "results_json_identical_after_normalization": json_ok,
        "enriched_jsonl_byte_identical": enr_ok,
        "normalized_fields": NORMALIZED,
        "normalization_disclosure":
            "Three RUN-IDENTITY fields are normalized — two wall-clock timings "
            "and the enriched-dataset output path (pass 2 writes to a different "
            "directory by design). NO computed value is normalized: every "
            "statistic, CI, count, hash and verdict is compared byte-for-byte. "
            "The enriched jsonl itself is compared RAW and is byte-identical. "
            "Precedent: CENSUS-1 F-BYTE normalized three run-identity stamps.",
        "sha256": {
            "census1b_results.json_pass1": sha256_file(j1),
            "census1b_results.json_pass2": sha256_file(j2),
            "census1b_termini_enriched.jsonl_pass1": s1,
            "census1b_termini_enriched.jsonl_pass2": s2,
        },
        "first_diffs": diffs[:20],
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "determinism.json").write_text(
        json.dumps(res, indent=1, sort_keys=True), encoding="utf-8", newline="\n")

    # build manifest (the committed surface for the uncommitted large jsonl)
    man = {
        "phase": "CENSUS-1b analysis (Tier A, measure-only)",
        "engine_version_note": "engine 1.0.11 byte-untouched; no engine file opened",
        "pre_registration": "LEDGER 2026-07-22 CENSUS-1b G-7 (commit a70a49c)",
        "reads_substrate": json.loads(
            (ROOT / "research_outputs" / "census" / "build_manifest.json")
            .read_text())["sha256"],
        "emits": {
            "census1b_results.json": sha256_file(j1),
            "census1b_termini_enriched.jsonl": s1,
            "census1b_termini_enriched.jsonl_rows": sum(1 for _ in open(e1, "rb")),
        },
        "determinism": {"F1b-DET": status, "normalized_fields": NORMALIZED},
    }
    (OUT / "build_manifest.json").write_text(
        json.dumps(man, indent=1, sort_keys=True), encoding="utf-8", newline="\n")

    print(f"F1b-DET: {status}")
    print(f"  results.json identical after normalization: {json_ok}")
    print(f"  enriched jsonl byte-identical: {enr_ok}")
    print(f"    pass1 {s1[:32]}…")
    print(f"    pass2 {s2[:32]}…")
    for d in diffs[:20]:
        print("  DIFF", d)
    return 0 if status == "MATCH" else 1


if __name__ == "__main__":
    raise SystemExit(main())
