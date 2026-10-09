#!/usr/bin/env python
"""TIER-C12 · THE FROZEN ESTATE — its census and its verdict [LEANS L-0.6; ORCHESTRATOR_RULINGS O-3, O-4, O-25].

TC12 moves no byte of the estate O-3 lists.  Prevention is the env hook's (L-D); DETECTION is here.  At TC12-REG
this tool writes research_outputs/tierc12/frozen/FROZEN_ESTATE.json ONCE — a census of the WORKING-TREE bytes of
  · research_outputs/tierc10/** and research_outputs/tierc11/**            every file as {bytes, sha256}
  · scripts/tierc10_* and scripts/tierc11_*
  · the two earlier TC contracts in exchange/queue/ (TC10 RESUME, TC11), X's contract as the manifest-pinned copy
    under x_rec/queue/, exchange/queue/008_sail-skeleton.md, LEDGER.md, exchange/status/LEDGER_APOLLO.md,
    exchange/status/CONVENTIONS.md, scripts/publish_exchange.py
  · every analytics/*.py and analytics/INTERFACE.md, except analytics/value_area.py (TC12's own module)
  · every __pycache__ directory under those roots, BY NAME
  · the two earlier snapshots as the sha of a (path, bytes, mtime_ns) LISTING — stat only, no file opened
  · x_rec/** held against x_rec/X_REC_MANIFEST.json (path set, n_files, every sha); the manifest's own sha is the
    one `tierc12_progress.certified` returns and n_files the `x_rec` block of the record it names
and asserts that the entries of progress/TC12-R0.json `frozen_estate_shas_at_r0` equal the census on their paths.
A file is HASHED as bytes and never parsed: no bar, tape or book is read.  Stdlib only; no git; no network; the
tool writes exactly one file, under research_outputs/tierc12/frozen/.

THE VERDICT (`findings`, run by F-FROZEN at every record gate and at CLOSE): the path set and every sha equal the
census, with ONE typed acceptance (L-0.24): a census path of L-0.24's sets (a)-(f), or the stamped TC11 contract,
is accepted at its census sha OR at the value research_outputs/tierc12/close/TC11_STAMP_MAP.json names for it when
that map reads `applied: true`.  The detectors, each naming the path:
  FROZEN-MISSING   a census path is not on file          FROZEN-CHANGED   a census path re-hashes to other bytes
  FROZEN-NEW       a path under a census root that the census does not hold (a _det_* file, a *_rerun.*, a
                   __pycache__, anything)                FROZEN-SNAPSHOT  a snapshot's listing sha moved
  FROZEN-XREC      x_rec differs from its manifest, or the manifest from its certified sha / n_files
  FROZEN-R0        an R0 entry differs from the census   FROZEN-CENSUS    no census on file
IF A PREDECESSOR'S CLOSE ACT LANDS MID-BUILD the estate moves by design: the orchestrator files the amendment and
`--write --k=<n>` writes FROZEN_ESTATE_<n>.json BESIDE the first, which is never rewritten; the verdict reads the
census with the highest <n>.

Run:  ~/venvs/naiad/bin/python -B /Users/luis/Naiad/scripts/tierc12_frozen.py            (the verdict; exit 1 on a finding)
      ~/venvs/naiad/bin/python -B /Users/luis/Naiad/scripts/tierc12_frozen.py --write    (the census; write-once)
      … --write --k=<n>   (a re-pinned census beside the first)   ·   … --root=DIR   (another tree, for fixtures)
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path

import tierc12_progress as P

ROOT = P.ROOT
T12 = P.T12
T11 = "research_outputs/tierc11"
XR = T12 + "/x_rec"
X_MANIFEST = XR + "/X_REC_MANIFEST.json"
CENSUS_DIR = T12 + "/frozen"
CENSUS_STEM = "FROZEN_ESTATE"
R0_RECORD = "TC12-R0"
R0_KEY = "frozen_estate_shas_at_r0"

# ── the estate, as typed roots (L-0.6) ──
TREES_T = ("research_outputs/tierc10", T11)
SCRIPT_DIR = "scripts"
SCRIPT_PREFIXES_T = ("tierc10_", "tierc11_")
TC11_CONTRACT = "exchange/queue/2026-09-24_TC11_APOLLO.md"
FILES_T = ("exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md", TC11_CONTRACT,
           XR + "/queue/2026-09-25_TC11X_APOLLO.md", "exchange/queue/008_sail-skeleton.md", "LEDGER.md",
           "exchange/status/LEDGER_APOLLO.md", "exchange/status/CONVENTIONS.md", "scripts/publish_exchange.py")
ANALYTICS_DIR = "analytics"
ANALYTICS_SUFFIX = ".py"
ANALYTICS_PLUS_T = ("analytics/INTERFACE.md",)
ANALYTICS_EXCEPT_T = ("analytics/value_area.py",)
PYCACHE = "__pycache__"
SNAPSHOTS_T = ("tc10_20260921", "tc11_20260925")
SNAPSHOT_HOME = ("~", ".cache", "naiad", "snapshots")

# ── the ONE typed acceptance (L-0.24): the paths TC12's own close act may move, and the map that says so ──
STAMP_MAP = T12 + "/close/TC11_STAMP_MAP.json"
STAMP_SETS_T = {
    "contract": (TC11_CONTRACT,),
    "a": (T11 + "/registrations/REGISTRATIONS.json",),
    "b": (T11 + "/registrations/REGISTRY_PIN.json",),
    "c": ("scripts/tierc11_registrations.py", "scripts/tierc11_score.py", "scripts/tierc11_score_fixtures.py",
          "scripts/tierc11_stage_g.py", "scripts/tierc11_stage_t_brk.py"),
    "f": (T11 + "/PROGRESS.json",),
}
STAMP_OPEN_PREFIX = T11 + "/"          # sets (d) and (e): TC11's own regenerated records, as the map lists them
NEVER_MOVED_T = (T11 + "/scores/SCORES.json", T11 + "/scores/FAMILY.json", T11 + "/scores/BASE_IDENT.json")
STAMP_MAP_ROWS = "moved"               # the map's rows: [{path, sha256_before, sha256_after}] (L-X.34)


def halt(msg: str):
    raise SystemExit(f"HALT: {msg}")


def file_entry(p: Path) -> dict:
    with p.open("rb") as f:
        return {"bytes": p.stat().st_size, "sha256": hashlib.file_digest(f, "sha256").hexdigest()}


def _walk(root: Path, rel: str):
    """(sorted file paths, sorted __pycache__ directory paths) under root/rel, repo-relative."""
    files, caches = [], []
    for d, dirs, names in os.walk(root / rel):
        dirs.sort()
        here = Path(d).relative_to(root).as_posix()
        caches += [f"{here}/{x}" for x in dirs if x == PYCACHE]
        files += [f"{here}/{x}" for x in sorted(names)]
    return sorted(files), sorted(caches)


def estate(root=ROOT) -> tuple:
    """(the estate's file paths on disk, the __pycache__ directories under its roots) — sorted, repo-relative."""
    root = Path(root)
    files, caches = [], []
    for tree in TREES_T:
        f, c = _walk(root, tree)
        files += f
        caches += c
    for d in (SCRIPT_DIR, ANALYTICS_DIR):
        if (root / d / PYCACHE).is_dir():
            caches.append(f"{d}/{PYCACHE}")
    if (root / SCRIPT_DIR).is_dir():
        files += [f"{SCRIPT_DIR}/{p.name}" for p in (root / SCRIPT_DIR).iterdir()
                  if p.is_file() and p.name.startswith(SCRIPT_PREFIXES_T)]
    if (root / ANALYTICS_DIR).is_dir():
        files += [f"{ANALYTICS_DIR}/{p.name}" for p in (root / ANALYTICS_DIR).iterdir()
                  if p.is_file() and p.name.endswith(ANALYTICS_SUFFIX)]
    files += [x for x in FILES_T + ANALYTICS_PLUS_T if (root / x).is_file()]
    return sorted(set(files) - set(ANALYTICS_EXCEPT_T)), sorted(set(caches))


def snapshot_listing(name: str, snapshots=None) -> dict:
    """The sha of a snapshot's (path, bytes, mtime_ns) listing — stat only; its bytes are Stage D's to hash."""
    base = Path(snapshots) if snapshots is not None else Path(*SNAPSHOT_HOME).expanduser()
    d = base / name
    if not d.is_dir():
        return {"path": "/".join(SNAPSHOT_HOME + (name,)), "on_file": False}
    rows, total = [], 0
    for here, dirs, names in os.walk(d):
        dirs.sort()
        for x in sorted(names):
            st = (Path(here) / x).stat()
            rows.append(f"{(Path(here) / x).relative_to(d).as_posix()}\t{st.st_size}\t{st.st_mtime_ns}\n")
            total += st.st_size
    return {"path": "/".join(SNAPSHOT_HOME + (name,)), "on_file": True, "n_files": len(rows), "bytes": total,
            "listing_sha256": hashlib.sha256("".join(sorted(rows)).encode("utf-8")).hexdigest()}


def x_rec_findings(root=ROOT) -> tuple:
    """(findings, block): x_rec/** against its manifest; the manifest against `certified()` and its record."""
    root = Path(root)
    out = []
    cert = P.certified(X_MANIFEST, root)
    n_record = P.records(root)[cert["record"]].get("x_rec", {}).get("n_files")
    mpath = root / X_MANIFEST
    if not mpath.is_file():
        return [f"FROZEN-XREC {X_MANIFEST}: the manifest is not on file"], {}
    entry = file_entry(mpath)
    if entry != {"bytes": cert["bytes"], "sha256": cert["sha256"]}:
        out.append(f"FROZEN-XREC {X_MANIFEST}: the manifest does not re-hash to the entry {cert['record']} certifies")
    manifest = json.loads(mpath.read_text(encoding="utf-8"))
    rows = {r["copy"]: r for r in manifest["files"]}
    on_disk = [p for p in _walk(root, XR)[0] if p != X_MANIFEST]
    if not len(rows) == len(manifest["files"]) == manifest["n_files"] == n_record:
        out.append(f"FROZEN-XREC {X_MANIFEST}: n_files — the manifest says {manifest['n_files']}, holds "
                   f"{len(manifest['files'])} rows ({len(rows)} distinct), the record {cert['record']} says {n_record}")
    out += [f"FROZEN-XREC {p}: a file under x_rec with no manifest row" for p in on_disk if p not in rows]
    out += [f"FROZEN-XREC {p}: a manifest row with no file under x_rec" for p in sorted(rows) if p not in on_disk]
    total = 0
    for p in on_disk:
        if p in rows:
            e = file_entry(root / p)
            total += e["bytes"]
            if (e["bytes"], e["sha256"]) != (rows[p]["bytes"], rows[p]["sha256"]):
                out.append(f"FROZEN-XREC {p}: does not re-hash to its manifest row")
    block = {"manifest": {"path": X_MANIFEST, "record": cert["record"], **entry}, "n_files": len(on_disk),
             "bytes": total}
    return out, block


def r0_entries(root=ROOT) -> dict:
    return P.records(root).get(R0_RECORD, {}).get(R0_KEY, {})


def census(root=ROOT, snapshots=None) -> dict:
    """The census document of the working tree (deterministic: no clock, sorted paths)."""
    root = Path(root)
    missing = [x for x in FILES_T + ANALYTICS_PLUS_T if not (root / x).is_file()]
    if missing:
        halt(f"FROZEN-MISSING: the estate's listed file(s) {missing} are not on file — no census is written")
    paths, caches = estate(root)
    files = {p: file_entry(root / p) for p in paths}
    x_findings, x_block = x_rec_findings(root)
    if x_findings:
        halt(f"{len(x_findings)} x_rec finding(s), first: {x_findings[0]} — no census is written")
    r0 = r0_entries(root)
    return {
        "what": "TIER-C12 · the census of the frozen estate (LEANS L-0.6): working-tree bytes at TC12-REG",
        "law": "the path set and every sha equal this census at every record gate and at CLOSE; one typed "
               "acceptance (L-0.24) — see stamp_acceptance",
        "roots": {"trees": list(TREES_T), "scripts": [f"{SCRIPT_DIR}/{x}*" for x in SCRIPT_PREFIXES_T],
                  "files": list(FILES_T), "analytics": [f"{ANALYTICS_DIR}/*{ANALYTICS_SUFFIX}"] + list(ANALYTICS_PLUS_T),
                  "analytics_except": list(ANALYTICS_EXCEPT_T)},
        "n_files": len(files),
        "bytes": sum(e["bytes"] for e in files.values()),
        "files": files,
        "pycache_dirs": caches,
        "snapshots": {name: snapshot_listing(name, snapshots) for name in SNAPSHOTS_T},
        "x_rec": x_block,
        "r0": {"record": f"{T12}/progress/{P.record_name(R0_RECORD)}", "key": R0_KEY, "n_paths": len(r0),
               "moved_since_r0": sorted(p for p, e in r0.items() if files.get(p) != e)},
        "stamp_acceptance": {"map": STAMP_MAP, "sets": {k: list(v) for k, v in STAMP_SETS_T.items()},
                             "sets_d_e": f"paths under {STAMP_OPEN_PREFIX} as the map lists them",
                             "never_moved": list(NEVER_MOVED_T),
                             "rule": "accepted at the census sha, or at the map's sha256_after when the map reads "
                                     "applied: true"},
    }


def render(doc: dict) -> str:
    return json.dumps(doc, indent=1, ensure_ascii=False, sort_keys=True) + "\n"


def census_file(root=ROOT, k=None) -> Path:
    return Path(root) / CENSUS_DIR / (f"{CENSUS_STEM}.json" if k is None else f"{CENSUS_STEM}_{k}.json")


def latest_census(root=ROOT):
    """The census the verdict reads: FROZEN_ESTATE_<n>.json with the highest n, else FROZEN_ESTATE.json."""
    d = Path(root) / CENSUS_DIR
    numbered = {}
    for p in (d.glob(f"{CENSUS_STEM}_*.json") if d.is_dir() else ()):
        tag = p.stem[len(CENSUS_STEM) + len("_"):]
        if tag.isdigit():
            numbered[int(tag)] = p
    if numbered:
        return numbered[max(numbered)]
    return census_file(root) if census_file(root).is_file() else None


def write(root=ROOT, k=None, snapshots=None) -> Path:
    """Write the census ONCE.  HALT if the target exists; the first census is never rewritten."""
    out = census_file(root, k)
    if out.exists():
        halt(f"{out.name} is on file — the census is write-once [L-0.5, L-0.6]")
    if k is not None and not census_file(root).is_file():
        halt(f"{CENSUS_STEM}.json is not on file — a re-pinned census is written BESIDE the first")
    doc = census(root, snapshots)
    if k is None and doc["r0"]["moved_since_r0"]:
        halt(f"FROZEN-R0: {doc['r0']['moved_since_r0']} differ from {R0_RECORD}'s {R0_KEY} — no census is written")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(doc), encoding="utf-8")
    return out


def stamp_accepts(root, path: str, sha_now: str) -> bool:
    """The ONE typed acceptance (L-0.24): `path` is the stamped contract or of sets (a)-(f), the map reads
    `applied: true`, and the map's row for the path names the bytes on file."""
    typed = {x for v in STAMP_SETS_T.values() for x in v}
    if path in NEVER_MOVED_T or not (path in typed or path.startswith(STAMP_OPEN_PREFIX)):
        return False
    m = Path(root) / STAMP_MAP
    if not m.is_file():
        return False
    doc = json.loads(m.read_text(encoding="utf-8"))
    if doc.get("applied") is not True:
        return False
    return any(r.get("path") == path and r.get("sha256_after") == sha_now for r in doc.get(STAMP_MAP_ROWS, []))


def findings(root=ROOT, snapshots=None) -> list:
    """THE VERDICT: the working tree against the census of record.  [] is GREEN."""
    root = Path(root)
    cpath = latest_census(root)
    if cpath is None:
        return [f"FROZEN-CENSUS {CENSUS_DIR}/{CENSUS_STEM}.json: no census is on file"]
    doc = json.loads(cpath.read_text(encoding="utf-8"))
    out = []
    paths, caches = estate(root)
    held = doc["files"]
    out += [f"FROZEN-MISSING {p}: a census path is not on file" for p in sorted(held) if p not in paths]
    out += [f"FROZEN-NEW {p}: under a census root and not in the census" for p in paths if p not in held]
    out += [f"FROZEN-NEW {c}/: a {PYCACHE} directory under a census root and not in the census"
            for c in caches if c not in doc["pycache_dirs"]]
    for p in paths:
        if p in held:
            e = file_entry(root / p)
            if e != held[p] and not stamp_accepts(root, p, e["sha256"]):
                out.append(f"FROZEN-CHANGED {p}: re-hashes to {e['sha256']} ({e['bytes']} B), the census holds "
                           f"{held[p]['sha256']} ({held[p]['bytes']} B)")
    for name in SNAPSHOTS_T:
        if snapshot_listing(name, snapshots) != doc["snapshots"].get(name):
            out.append(f"FROZEN-SNAPSHOT {name}: the (path, bytes, mtime_ns) listing differs from the census")
    x_findings, x_block = x_rec_findings(root)
    out += x_findings
    if not x_findings and x_block != doc["x_rec"]:
        out.append(f"FROZEN-XREC {X_MANIFEST}: the x_rec block differs from the census")
    if cpath == census_file(root):
        r0 = r0_entries(root)
        out += [f"FROZEN-R0 {p}: {R0_RECORD}'s {R0_KEY} entry differs from the census" for p in sorted(r0)
                if held.get(p) != r0[p]]
    return out


def main(argv=None) -> int:
    args = sys.argv[1:] if argv is None else list(argv)
    root = Path(next((a.split("=", 1)[1] for a in args if a.startswith("--root=")), ROOT)).resolve()
    k = next((a.split("=", 1)[1] for a in args if a.startswith("--k=")), None)
    if "--write" in args:
        if k is not None and not k.isdigit():
            halt(f"--k={k}: not a census number")
        out = write(root, None if k is None else int(k))
        doc = json.loads(out.read_text(encoding="utf-8"))
        print(f"{out.relative_to(root).as_posix()} written: {doc['n_files']} files, {doc['bytes']} B, "
              f"{len(doc['pycache_dirs'])} {PYCACHE} directories, x_rec {doc['x_rec']['n_files']} files; sha256 "
              f"{P.sha(out)}")
        return 0
    found = findings(root)
    for f in found:
        print(f)
    print(f"FROZEN ESTATE: {'UNMOVED' if not found else str(len(found)) + ' finding(s)'}")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
