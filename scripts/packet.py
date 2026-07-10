"""D8: the session packet — one zip the operator ferries to the reviewer.

Bundles journals, research outputs, configs, state, and a one-page manifest.

  python scripts/packet.py [--journal-root journal] [--state-root state]
"""

import argparse
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from engine.version import ENGINE_VERSION

ROOT = Path(__file__).resolve().parent.parent


def git_rev() -> str:
    try:
        return subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                              capture_output=True, text=True, cwd=ROOT,
                              check=True).stdout.strip()
    except Exception:
        return "unknown"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--journal-root", default="journal")
    ap.add_argument("--state-root", default="state")
    args = ap.parse_args()

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M")
    out_dir = ROOT / "research_outputs" / "packets"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"naiad_packet_{stamp}.zip"

    include: list[tuple[Path, str]] = []
    for base, arc in [(Path(args.journal_root), "journal"),
                      (Path(args.state_root), "state"),
                      (ROOT / "research_outputs", "research_outputs"),
                      (ROOT / "configs", "configs"),
                      (ROOT / "fixtures" / "autopsy_questions.md", "autopsy_questions.md"),
                      (ROOT / "data_starts.csv", "data_starts.csv"),
                      (ROOT / "CHANGELOG.md", "CHANGELOG.md")]:
        base = base if base.is_absolute() else ROOT / base
        if base.is_file():
            include.append((base, arc))
        elif base.is_dir():
            for p in sorted(base.rglob("*")):
                if p.is_file() and "packets" not in p.parts:
                    include.append((p, f"{arc}/{p.relative_to(base)}"))

    manifest = [
        "NAIAD SESSION PACKET",
        f"created_utc: {datetime.now(timezone.utc).isoformat()}",
        f"engine_version: {ENGINE_VERSION}",
        f"git_rev: {git_rev()}",
        f"files: {len(include)}",
        "",
        "contents:",
    ] + [f"  {arc}" for _, arc in include]

    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("MANIFEST.txt", "\n".join(manifest) + "\n")
        for path, arc in include:
            z.write(path, arc)

    print(f"packet -> {out}  ({len(include)} files)")
    print("Attach this zip to the reviewer session.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
