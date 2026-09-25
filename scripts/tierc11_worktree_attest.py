"""TIER-C11 · WORKTREE ATTESTATION [LEANS L-F.3] — a review ran read-only, at the commit it names,
on the artifacts that commit records.

--open creates a detached git worktree at COMMIT and stages the gitignored data artifacts beside it
(research_outputs/tierc11/**/*.parquet, never a _det_ scratch dir: git does not carry them, so they
are copied from the main tree so the reviewed code can run on the reviewed outputs).  It records a
PER-FILE sha256 map of every staged file, checks that map against the REVIEWED COMMIT's own record
(`git show COMMIT:research_outputs/tierc11/PROGRESS.json`, every stage's artifact_shas, the last
stage that records a path governs), and records HEAD and `git status --porcelain` BEFORE.  The
reviewer works inside the worktree, then --close records HEAD and porcelain AFTER, RE-HASHES every
staged file, files the attestation JSON in the MAIN tree and removes the worktree.

--open ALSO stages READ-ONLY copies (mode 0444) of EXACTLY the two TC10 records that TC10's own
modules read AT IMPORT from their own tree — research_outputs/tierc10/data/STAGE_D_MANIFEST.json
(tierc10_panel: resolve_unseen12() at import) and research_outputs/tierc10/census/TUNING_RESULT.json
(tierc10_census: RETEST_PINS at import) [TC11-FIX verify MAJOR-2: without them the env suite reads
"TC10 records read []" in a review worktree].  They are TC10 records, never in TC11's PROGRESS
record: each staged copy is held to the MAIN tree's own bytes at open, re-hashed at close like every
other staged file, and the main tree's bytes are re-read at close.  Nothing else under
research_outputs/tierc10 is staged.

    ~/venvs/naiad/bin/python scripts/tierc11_worktree_attest.py --commit <sha> --lens <name> --open
        (prints the worktree path; the reviewer works there)
    ~/venvs/naiad/bin/python scripts/tierc11_worktree_attest.py --lens <name> --close
    [--out-dir=DIR]  files the open record and the attestation under DIR instead of
                     research_outputs/tierc11/review/attest (the fixtures' scratch)

FAILS IF (exit 1 at --close, attestation verdict RED) — any one finding:
  · HEAD inside the worktree != COMMIT, before or after;
  · `git status --porcelain` non-empty, before or after (a review that wrote a tracked or an
    untracked-unignored file is not read-only);
  · at --open: a staged file whose sha256 differs from the reviewed commit's PROGRESS record
    (STAGED != RECORD), a staged file the record lacks (STAGED NOT IN RECORD), a recorded file of
    the staged class that was not staged (RECORDED NOT STAGED), or no readable record at COMMIT;
    a staged TC10 record whose bytes are not the main tree's (TC10 RECORD != MAIN TREE), or one
    of the two that could not be staged (TC10 RECORD NOT STAGED);
  · at --close: a staged file (parquet or TC10 record) whose bytes changed since --open (STAGED
    CHANGED), a staged file gone (STAGED VANISHED), a file of the staged class that was not
    staged at --open (STAGED-CLASS APPEARED), or a TC10 record whose main-tree bytes moved since
    --open (TC10 RECORD != MAIN TREE … at close) — porcelain cannot see any of these, the staged
    files are ignored;
  · the worktree could not be read or removed at --close.
Findings found at --open are printed on stderr at once and carried into the --close verdict;
--open still exits 0 so that --close always runs and removes the worktree.

AM-8 (LEANS_AMENDMENTS.md): the only subprocess use in this module is `git` (worktree, rev-parse,
status, show) for L-F.3.  The one-shot `-- <cmd ...>` mode, which ran the review command in a
subprocess, is REMOVED — the reviewer runs its own commands between --open and --close (as all five
lenses of the 2026-09-25 final review did).  scripts/tierc11_closure_fixtures.py F-HOOK-ESCAPE-ALL
enforces it; scripts/tierc11_attest_fixtures.py plants every RED above.
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WT_BASE = ROOT / ".claude" / "worktrees"
OUT = ROOT / "research_outputs" / "tierc11" / "review" / "attest"
STAGE_GLOBS = ("research_outputs/tierc11/**/*.parquet",)
STAGE_PREFIX, STAGE_SUFFIX = "research_outputs/tierc11/", ".parquet"
PROGRESS_REL = "research_outputs/tierc11/PROGRESS.json"
# The two TC10 records TC10's own modules read at import from their own tree [MAJOR-2]: staged
# read-only, held to the MAIN tree's bytes (they are TC10's, not in TC11's PROGRESS record).
TC10_STAGED = ("research_outputs/tierc10/census/TUNING_RESULT.json",
               "research_outputs/tierc10/data/STAGE_D_MANIFEST.json")
TC10_MODE = 0o444
LENS_RX = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,63}")
FAILS_IF = ("HEAD != the reviewed commit, or porcelain non-empty, before or after; at open a staged "
            "file whose sha differs from, or is absent from, the reviewed commit's PROGRESS.json "
            "record, or a recorded file of the staged class not staged, or a staged TC10 record "
            "not the main tree's bytes or not staged; at close a staged file (parquet or TC10 "
            "record) changed, vanished or appeared since open, or a TC10 record's main-tree bytes "
            "moved; the worktree unreadable or not removed")


def git(args: list[str], cwd: Path) -> str:
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True).stdout


def sha_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def state(wt: Path) -> dict:
    return {"head": git(["rev-parse", "HEAD"], wt).strip(),
            "porcelain": git(["status", "--porcelain"], wt)}


def staged_class(rel: str) -> bool:
    """A path of the staged class: a parquet under research_outputs/tierc11/, no _det_ part."""
    parts = rel.split("/")
    return (rel.startswith(STAGE_PREFIX) and rel.endswith(STAGE_SUFFIX)
            and not any(p.startswith("_det_") for p in parts))


def scan_staged(tree: Path) -> dict:
    """{rel: sha256} of every staged-class file under `tree`, in path order."""
    out = {}
    for pat in STAGE_GLOBS:
        for p in sorted(tree.glob(pat)):
            rel = p.relative_to(tree).as_posix()
            if staged_class(rel) and p.is_file():
                out[rel] = sha_file(p)
    return dict(sorted(out.items()))


def stage_artifacts(wt: Path, stage_root: Path = ROOT) -> dict:
    """Copy the staged-class files from `stage_root` (the main tree) into the worktree; return
    {rel: sha256 of the COPY}, in path order."""
    staged = {}
    for pat in STAGE_GLOBS:
        for src in sorted(stage_root.glob(pat)):
            rel = src.relative_to(stage_root).as_posix()
            if not staged_class(rel) or not src.is_file():
                continue
            dst = wt / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            staged[rel] = sha_file(dst)
    return dict(sorted(staged.items()))


def stage_tc10(wt: Path, stage_root: Path = ROOT) -> dict:
    """Copy EXACTLY the TC10_STAGED records from `stage_root` (the main tree) into the worktree at
    the same relative paths, each made read-only (TC10_MODE); return {rel: sha256 of the COPY}.
    A record the stage source lacks is not staged (tc10_findings names it)."""
    staged = {}
    for rel in TC10_STAGED:
        src = stage_root / rel
        if not src.is_file():
            continue
        dst = wt / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
        dst.chmod(TC10_MODE)
        staged[rel] = sha_file(dst)
    return dict(sorted(staged.items()))


def tc10_findings(staged_tc10: dict, main: Path = ROOT, tail: str = "") -> list[str]:
    """Each staged TC10 record against the MAIN tree's own bytes (not against PROGRESS: they are
    TC10's records)."""
    out = []
    for rel in TC10_STAGED:
        m = main / rel
        msha = sha_file(m) if m.is_file() else None
        if rel not in staged_tc10:
            out.append(f"TC10 RECORD NOT STAGED: {rel} (no staged copy){tail}")
        elif msha is None:
            out.append(f"TC10 RECORD != MAIN TREE: {rel} staged sha {staged_tc10[rel][:12]}… but "
                       f"the main tree has no such file{tail}")
        elif staged_tc10[rel] != msha:
            out.append(f"TC10 RECORD != MAIN TREE: {rel} staged sha {staged_tc10[rel][:12]}… vs "
                       f"the main tree's {msha[:12]}…{tail}")
    return out


def rehash_tc10(wt: Path, staged_tc10: dict) -> list[str]:
    out = []
    for rel, sha in staged_tc10.items():
        p = wt / rel
        if not p.is_file():
            out.append(f"STAGED VANISHED: {rel} (sha at open {sha[:12]}…)")
        elif (got := sha_file(p)) != sha:
            out.append(f"STAGED CHANGED: {rel} sha at open {sha[:12]}… vs at close {got[:12]}…")
    return out


def commit_record(commit: str) -> tuple[dict, dict, list[str]]:
    """The reviewed commit's PROGRESS.json record: ({path: sha256}, provenance, findings).  Every
    stage's artifact_shas; a path recorded by several stages takes the LAST stage's sha (a later
    re-file supersedes), and the superseded count is printed."""
    try:
        raw = git(["show", f"{commit}:{PROGRESS_REL}"], ROOT)
    except subprocess.CalledProcessError as e:
        return {}, {"path": PROGRESS_REL}, [f"NO RECORD: git show {commit[:12]}:{PROGRESS_REL} "
                                             f"failed ({(e.stderr or '').strip()[:160]})"]
    prov = {"path": PROGRESS_REL, "blob_sha256": hashlib.sha256(raw.encode("utf-8")).hexdigest()}
    try:
        stages = json.loads(raw)["stages"]
        rec, superseded = {}, 0
        for st in stages:
            for path, v in (st.get("artifact_shas") or {}).items():
                sha = v["sha256"] if isinstance(v, dict) else v
                if path in rec and rec[path] != sha:
                    superseded += 1
                rec[path] = str(sha)
    except (ValueError, KeyError, TypeError) as e:
        return {}, prov, [f"NO RECORD: {PROGRESS_REL} at {commit[:12]} is not a readable "
                          f"record ({type(e).__name__}: {e})"]
    prov.update(recorded_paths=len(rec), recorded_staged_class=sum(map(staged_class, rec)),
                superseded_records=superseded)
    return rec, prov, []


def record_findings(staged: dict, record: dict) -> list[str]:
    out = []
    for rel, sha in staged.items():
        if rel not in record:
            out.append(f"STAGED NOT IN RECORD: {rel} (sha {sha[:12]}…) — the reviewed commit's "
                       f"PROGRESS.json lacks it")
        elif record[rel] != sha:
            out.append(f"STAGED != RECORD: {rel} staged sha {sha[:12]}… vs the reviewed commit's "
                       f"record {record[rel][:12]}…")
    for rel in sorted(record):
        if staged_class(rel) and rel not in staged:
            out.append(f"RECORDED NOT STAGED: {rel} (the reviewed commit records "
                       f"{record[rel][:12]}…; the main tree has no such file)")
    return out


def rehash_findings(wt: Path, staged: dict) -> list[str]:
    now = scan_staged(wt)
    out = []
    for rel, sha in staged.items():
        p = wt / rel
        if not p.is_file():
            out.append(f"STAGED VANISHED: {rel} (sha at open {sha[:12]}…)")
        elif (got := sha_file(p)) != sha:
            out.append(f"STAGED CHANGED: {rel} sha at open {sha[:12]}… vs at close {got[:12]}…")
    for rel in now:
        if rel not in staged:
            out.append(f"STAGED-CLASS APPEARED: {rel} (sha {now[rel][:12]}…) — not staged at open")
    return out


def check_lens(lens: str) -> str:
    if not LENS_RX.fullmatch(lens or ""):
        raise SystemExit(f"HALT: lens {lens!r} is not a plain name ([A-Za-z0-9._-], ≤ 64)")
    return lens


def wt_path(lens: str) -> Path:
    return WT_BASE / f"tc11-review-{check_lens(lens)}"


def remove_wt(wt: Path) -> None:
    git(["worktree", "remove", "--force", str(wt)], ROOT)


def open_wt(commit: str, lens: str, out: Path = OUT, stage_root: Path = ROOT) -> dict:
    wt = wt_path(lens)
    if wt.exists():
        raise SystemExit(f"HALT: {wt} exists — close it first")
    if (out / f"{lens}.open.json").exists():
        raise SystemExit(f"HALT: {out / f'{lens}.open.json'} exists — close that review first")
    commit = git(["rev-parse", "--verify", f"{commit}^{{commit}}"], ROOT).strip()
    git(["worktree", "add", "--detach", str(wt), commit], ROOT)
    try:
        staged = stage_artifacts(wt, stage_root)
        staged_tc10 = stage_tc10(wt, stage_root)
        record, prov, rec_find = commit_record(commit)
        open_findings = (rec_find + record_findings(staged, record)
                         + tc10_findings(staged_tc10, ROOT))
        before = state(wt)
        rec = {"lens": lens, "commit": commit, "worktree": str(wt), "before": before,
               "staged_artifacts": len(staged),
               "staged_sha256": hashlib.sha256(
                   json.dumps(staged, sort_keys=True).encode()).hexdigest(),
               "staged_files": staged, "staged_tc10": staged_tc10,
               "progress_record": prov, "open_findings": open_findings}
        out.mkdir(parents=True, exist_ok=True)
        (out / f"{lens}.open.json").write_text(json.dumps(rec, indent=2) + "\n")
    except BaseException:
        if wt.exists():
            remove_wt(wt)
        raise
    return rec


def close_wt(lens: str, out: Path = OUT) -> dict:
    wt = wt_path(lens)
    op = out / f"{lens}.open.json"
    if not op.exists():
        raise SystemExit(f"HALT: no open record {op} — nothing to close"
                         + (f" (the worktree {wt} exists: remove it by hand)" if wt.exists() else ""))
    rec = json.loads(op.read_text())
    findings = list(rec.get("open_findings", []))
    after = None
    try:
        after = state(wt)
        for tag, st in (("before", rec["before"]), ("after", after)):
            if st["head"] != rec["commit"]:
                findings.append(f"HEAD {tag} {st['head'][:12]} != reviewed commit "
                                f"{rec['commit'][:12]}")
            if st["porcelain"].strip():
                findings.append(f"porcelain {tag} not empty: {st['porcelain'].strip()[:400]}")
        if "staged_files" in rec:
            findings += rehash_findings(wt, rec["staged_files"])
        else:
            # An open record filed by the pre-hardening script: no per-file map, no record
            # check.  Re-hash the staged set against its set-level sha, and check it against
            # the reviewed commit's record now — a legacy open cannot close unchecked.
            now = scan_staged(wt)
            if hashlib.sha256(json.dumps(now, sort_keys=True).encode()).hexdigest() \
                    != rec.get("staged_sha256"):
                findings.append(f"STAGED SET CHANGED (legacy open record: set-level sha only): "
                                f"{len(now)} staged-class files now vs "
                                f"{rec.get('staged_artifacts')} at open")
            record, prov, rec_find = commit_record(rec["commit"])
            findings += [f"{f} (checked at close: legacy open record)"
                         for f in rec_find + record_findings(now, record)]
            rec.update(staged_files=now, progress_record=prov, legacy_open_record=True)
        if "staged_tc10" in rec:
            findings += rehash_tc10(wt, rec["staged_tc10"])
            findings += tc10_findings(rec["staged_tc10"], ROOT, " (at close)")
        else:
            # An open record filed before the TC10 staging: no TC10 map was taken at open.  The
            # copies now in the worktree (if any) are held to the main tree at close; a record
            # never staged is a finding — such an open cannot close unchecked either.
            now_tc10 = {rel: sha_file(wt / rel) for rel in TC10_STAGED if (wt / rel).is_file()}
            findings += tc10_findings(now_tc10, ROOT,
                                      " (checked at close: open record predates the TC10 staging)")
            rec.update(staged_tc10=now_tc10, tc10_checked_at_close=True)
    except (subprocess.CalledProcessError, OSError) as e:
        findings.append(f"WORKTREE UNREADABLE at close: {type(e).__name__}: "
                        f"{str(getattr(e, 'stderr', '') or e).strip()[:200]}")
    finally:
        if wt.exists():
            try:
                remove_wt(wt)
            except subprocess.CalledProcessError as e:
                findings.append(f"WORKTREE NOT REMOVED: {(e.stderr or '').strip()[:200]}")
    rec.update(after=after, findings=findings, verdict="GREEN" if not findings else "RED",
               fails_if=FAILS_IF)
    (out / f"{lens}.json").write_text(json.dumps(rec, indent=2) + "\n")
    op.unlink()
    return rec


def _flag(argv: list[str], name: str) -> str | None:
    if name in argv:
        i = argv.index(name)
        if i + 1 >= len(argv):
            raise SystemExit(f"HALT: {name} needs a value")
        return argv[i + 1]
    return None


def main(argv: list[str]) -> int:
    if "--" in argv:
        raise SystemExit("HALT: the one-shot `-- <cmd ...>` mode is removed (AM-8: this module's "
                         "only subprocess use is git). Run --open, review inside the printed "
                         "worktree, then --close.")
    lens = _flag(argv, "--lens")
    if lens is None:
        raise SystemExit("HALT: --lens <name> is required")
    check_lens(lens)
    out = next((Path(a.split("=", 1)[1]) for a in argv if a.startswith("--out-dir=")), OUT)
    if "--close" in argv:
        rec = close_wt(lens, out)
        print(json.dumps({k: rec[k] for k in ("lens", "commit", "verdict", "findings")}, indent=2))
        return 0 if rec["verdict"] == "GREEN" else 1
    if "--open" not in argv:
        raise SystemExit("HALT: give --open (with --commit) or --close")
    commit = _flag(argv, "--commit")
    if commit is None:
        raise SystemExit("HALT: --open needs --commit <sha>")
    rec = open_wt(commit, lens, out)
    print(rec["worktree"])
    if rec["open_findings"]:
        print(f"OPEN FINDINGS ({len(rec['open_findings'])}; the --close verdict will be RED):",
              file=sys.stderr)
        for f in rec["open_findings"]:
            print(f"  {f}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
