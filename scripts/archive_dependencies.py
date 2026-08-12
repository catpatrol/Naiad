"""Build docs/ARCHIVE_DEPENDENCIES.md -- the grep that should have run before
the 2026-07-27 reclamation."""
import io
import json
import os
import re
import sys
import zipfile
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from backup_estate import drive_ready, phase_archive_root_path   # noqa: E402  (D-0b)
SCAN_DIRS = ["fixtures", "tests", "scripts"]
EXTS = {".py", ".ps1"}

# "research_outputs" / "census" / ...   |   research_outputs/census/...
PAT_PARTS = re.compile(r'"research_outputs"\s*(?:/\s*"([A-Za-z0-9_\-]+)")?')
PAT_SLASH = re.compile(r'research_outputs[/\\]([A-Za-z0-9_\-]+)')

WRITE_HINT = re.compile(r'\b(OUT_DIR|out_dir|OUT\b|mkdir|write|dump|to_parquet|to_csv|savefig|open\([^)]*["\']w)', re.I)
READ_HINT = re.compile(r'\b(read_parquet|read_csv|load|open\(|rglob|glob|iterdir|exists\(\)|is_dir\(\)|Path\()', re.I)

hits = defaultdict(list)          # component -> [(file, line, text, kind)]
for d in SCAN_DIRS:
    base = REPO / d
    if not base.exists():
        continue
    for f in sorted(base.rglob("*")):
        if not f.is_file() or f.suffix.lower() not in EXTS:
            continue
        if "__pycache__" in f.parts:
            continue
        try:
            lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for n, line in enumerate(lines, 1):
            if "research_outputs" not in line:
                continue
            comps = set(c for c in PAT_PARTS.findall(line) if c)
            comps |= set(PAT_SLASH.findall(line))
            if not comps:
                comps = {"(root)"}
            kind = "write" if WRITE_HINT.search(line) and not READ_HINT.search(line) else \
                   ("read" if READ_HINT.search(line) else "ref")
            for c in comps:
                rel = f.relative_to(REPO).as_posix()
                hits[c].append((rel, n, line.strip()[:150], kind))

# archive membership: which top-level component lives in which zip
#
# STALE PATH, fixed 2026-08-12 (D-0b).  This read REPO/research_outputs/_archive,
# which has held no zips since ruling B moved them off-machine on 2026-08-06 --
# so the archive-membership column silently went blank and this report has been
# claiming components live in no archive at all.  Third copy of the same defect
# (backup_estate.py fixed by O-4, daily_routine.py fixed alongside this one).
# Resolves the same root --phase writes to, through the same waiting gate.
arch_dir = phase_archive_root_path()
arch_ready, arch_detail = drive_ready(arch_dir, note=lambda *_a, **_k: None)
archives = {}
ARCHIVE_SCAN_NOTE = (f"archive membership read from `{arch_dir}` ({arch_detail})"
                     if arch_ready else
                     f"**archive membership NOT ENUMERABLE** — `{arch_dir}` is "
                     f"unreachable ({arch_detail}). This is not the same as "
                     f"\"no archives\".")
if arch_ready and arch_dir.exists():
    for z in sorted(arch_dir.glob("*.zip")):
        phase = z.name.split("_2026")[0]
        try:
            with zipfile.ZipFile(z) as zf:
                archives[phase] = (z.name, len(zf.namelist()))
        except zipfile.BadZipFile:
            archives[phase] = (z.name, -1)

rows = []
for comp in sorted(hits):
    if comp == "(root)":
        continue
    p = REPO / "research_outputs" / comp
    if p.is_dir():
        n = sum(1 for _ in p.rglob("*") if _.is_file())
        state = f"resolves ({n} files)" if n else "resolves (EMPTY)"
    elif p.exists():
        state = "resolves (file)"
    elif list((REPO / "research_outputs").glob(comp + ".*")):
        # the name is a FILE stem (e.g. dryrun_autopsy.md), not a directory --
        # a false MISSING row in a governance doc is worse than no row at all
        state = "resolves (file)"
    else:
        state = "MISSING"
    arc = archives.get(comp)
    if arc and p.is_dir():
        # A phase that was archived-and-released still "resolves" -- but only as a
        # thin shell of the git-tracked files preserved in place (LEDGER.md:756).
        # Reporting bare "resolves" here is what cost two retrievals: a reader sees
        # the directory exists and assumes the phase is intact.
        on_disk = sum(1 for _ in p.rglob("*") if _.is_file())
        archived = arc[1] - 1                      # minus the embedded MANIFEST.json
        if on_disk < archived:
            state = (f"THIN SHELL -- {on_disk} of {archived} archived files on disk; "
                     f"the rest are only inside the zip")
    rows.append((comp, state, arc[0] if arc else "-", hits[comp]))

out = io.StringIO()
w = out.write
w("# ARCHIVE DEPENDENCIES\n\n")
w("**THE RULE (standing, adopted 2026-07-28, contract v4 §0.4).** "
  "No phase directory under `research_outputs/` is archived until this document "
  "is regenerated and the archive's manifest records which readers depend on it.\n\n")
w("The 2026-07-27 reclamation cost two retrievals -- the `c141t213` regression "
  "fixture and the S-3 journals the census Phase 0 needs. Both were avoidable "
  "with one grep. This file is that grep, made durable.\n\n")
w("Regenerate with `scripts/archive_dependencies.py`. Scan scope: "
  f"`{'`, `'.join(SCAN_DIRS)}` for `*.py` and `*.ps1`.\n\n")
w("## Summary\n\n")
w("| path under `research_outputs/` | state on disk | archived in | referencing sites |\n")
w("|---|---|---|---:|\n")
for comp, state, arc, hh in rows:
    flag = "**MISSING**" if state == "MISSING" else state
    w(f"| `{comp}/` | {flag} | {arc} | {len(hh)} |\n")
w("\n### Archives present\n\n")
w(ARCHIVE_SCAN_NOTE + "\n\n")
if arch_ready:
    w("| archive | entries |\n|---|---:|\n")
    for phase, (name, n) in sorted(archives.items()):
        w(f"| `{name}` | {n} |\n")
    if not archives:
        w("_The archive root is reachable and holds no `.zip`._\n")

w("\n## Detail -- every referencing site\n\n")
for comp, state, arc, hh in rows:
    w(f"### `research_outputs/{comp}/` — {state}\n\n")
    if arc != "-":
        w(f"Archived in `{arc}`.\n\n")
    w("| reader | line | kind | source |\n|---|---:|---|---|\n")
    for rel, n, text, kind in sorted(hh):
        safe = text.replace("|", "\\|").replace("`", "'")
        w(f"| `{rel}` | {n} | {kind} | `{safe}` |\n")
    w("\n")

(REPO / "docs").mkdir(exist_ok=True)
(REPO / "docs" / "ARCHIVE_DEPENDENCIES.md").write_text(out.getvalue(), encoding="utf-8")

print("wrote docs/ARCHIVE_DEPENDENCIES.md")
print(f"components: {len(rows)}   referencing sites: {sum(len(h) for _,_,_,h in rows)}")
print("\nMISSING (readers depend on a path that no longer resolves):")
for comp, state, arc, hh in rows:
    if state == "MISSING":
        readers = sorted({r for r, _, _, k in hh if k in ("read", "ref")})
        print(f"  research_outputs/{comp}/  archived_in={arc}  readers={readers}")
