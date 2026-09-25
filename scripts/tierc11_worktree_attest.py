"""TIER-C11 · WORKTREE ATTESTATION [LEANS L-F.3] — a review ran read-only, at the commit it names.

Creates a detached git worktree at COMMIT, stages the gitignored data artifacts beside it (the parquet
files git does not carry, copied read-only from the main tree so the reviewed code can run on the reviewed
outputs), records HEAD and `git status --porcelain` BEFORE, runs the review command inside the worktree,
records HEAD and porcelain AFTER, and files an attestation JSON in the MAIN tree.

    ~/venvs/naiad/bin/python scripts/tierc11_worktree_attest.py --commit <sha> --lens <name> -- <cmd ...>
    ~/venvs/naiad/bin/python scripts/tierc11_worktree_attest.py --commit <sha> --lens <name> --open
        (--open: create + stage the worktree and print its path; the reviewer works there, then runs
         --close --lens <name> to record the AFTER state and remove it)

FAILS IF (exit 1, attestation verdict RED): HEAD inside the worktree != COMMIT before or after, or the
porcelain status is non-empty before or after (a review that wrote a tracked or untracked-unignored file is
not read-only). Ignored files (the staged parquet, _det_ dirs, scratch) do not appear in porcelain.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WT_BASE = ROOT / ".claude" / "worktrees"
OUT = ROOT / "research_outputs" / "tierc11" / "review" / "attest"
STAGE_GLOBS = ("research_outputs/tierc11/**/*.parquet",)


def git(args: list[str], cwd: Path) -> str:
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True).stdout


def state(wt: Path) -> dict:
    return {"head": git(["rev-parse", "HEAD"], wt).strip(),
            "porcelain": git(["status", "--porcelain"], wt)}


def stage_artifacts(wt: Path) -> dict:
    """Copy the gitignored parquet artifacts from the main tree; return {rel: sha256}."""
    staged = {}
    for pat in STAGE_GLOBS:
        for src in sorted(ROOT.glob(pat)):
            rel = src.relative_to(ROOT)
            if any(part.startswith("_det_") for part in rel.parts):
                continue
            dst = wt / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            staged[str(rel)] = hashlib.sha256(dst.read_bytes()).hexdigest()
    return staged


def wt_path(lens: str) -> Path:
    return WT_BASE / f"tc11-review-{lens}"


def open_wt(commit: str, lens: str) -> dict:
    wt = wt_path(lens)
    if wt.exists():
        raise SystemExit(f"HALT: {wt} exists — close it first")
    git(["worktree", "add", "--detach", str(wt), commit], ROOT)
    staged = stage_artifacts(wt)
    before = state(wt)
    rec = {"lens": lens, "commit": commit, "worktree": str(wt), "before": before,
           "staged_artifacts": len(staged), "staged_sha256": hashlib.sha256(
               json.dumps(staged, sort_keys=True).encode()).hexdigest()}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{lens}.open.json").write_text(json.dumps(rec, indent=2) + "\n")
    return rec


def close_wt(lens: str) -> dict:
    wt = wt_path(lens)
    rec = json.loads((OUT / f"{lens}.open.json").read_text())
    after = state(wt)
    findings = []
    for tag, st in (("before", rec["before"]), ("after", after)):
        if st["head"] != rec["commit"]:
            findings.append(f"HEAD {tag} {st['head'][:12]} != reviewed commit {rec['commit'][:12]}")
        if st["porcelain"].strip():
            findings.append(f"porcelain {tag} not empty: {st['porcelain'].strip()[:400]}")
    rec.update(after=after, findings=findings, verdict="GREEN" if not findings else "RED",
               fails_if="HEAD != the reviewed commit, or porcelain non-empty, before or after")
    (OUT / f"{lens}.json").write_text(json.dumps(rec, indent=2) + "\n")
    (OUT / f"{lens}.open.json").unlink()
    git(["worktree", "remove", "--force", str(wt)], ROOT)
    return rec


def main(argv: list[str]) -> int:
    lens = argv[argv.index("--lens") + 1]
    if "--close" in argv:
        rec = close_wt(lens)
        print(json.dumps({k: rec[k] for k in ("lens", "commit", "verdict", "findings")}, indent=2))
        return 0 if rec["verdict"] == "GREEN" else 1
    commit = git(["rev-parse", argv[argv.index("--commit") + 1]], ROOT).strip()
    rec = open_wt(commit, lens)
    if "--open" in argv:
        print(rec["worktree"])
        return 0
    cmd = argv[argv.index("--") + 1:]
    rc = subprocess.run(cmd, cwd=rec["worktree"]).returncode
    rec = close_wt(lens)
    rec_rc = 0 if rec["verdict"] == "GREEN" else 1
    print(json.dumps({"lens": lens, "command_exit": rc, "verdict": rec["verdict"],
                      "findings": rec["findings"]}, indent=2))
    return rc or rec_rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
