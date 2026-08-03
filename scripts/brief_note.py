#!/usr/bin/env python
"""brief_note.py -- timestamp an operator observation into a capture (§8.3).

    C:\\venvs\\naiad\\Scripts\\python.exe scripts/brief_note.py \\
        --date 2026-08-03 --slot post_ny --text "watching the 90d VAL"

WHY THIS EXISTS AND WHY IT IS NARROW.  The operator's read is the one input the
machine cannot produce, and it is worth having in the record beside the numbers
it was formed from.  But a capture that can be edited freely stops being a
record, so this tool APPENDS to a notes list and touches nothing else.

A NOTE IS AN OBSERVATION, NEVER AN OUTCOME.  "the 30d VAL held" is a note.
"that trade worked" is an outcome statistic and belongs nowhere near an ops
artifact -- it is census work under G-7.  The forbidden-word guard below is not
decoration; it is the firewall at the one place a human types free text into the
record.

The capture's own sha256 changes when a note is appended, so `briefs/index.jsonl`
gains a corrected line rather than being rewritten -- the index is append-only
for the same reason the capture is.
"""

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

BRIEFS = ROOT / "briefs"

# Outcome and sizing language. A note describing what was SEEN is welcome; a note
# describing what a trade DID is an outcome statistic, and one describing size is
# sizing advice. Both are refused at the point of entry rather than filtered later.
FORBIDDEN = re.compile(
    r"\b(pnl|p&l|profit|loss(es)?|won|lost|win(s|ning)?|r[- ]?multiple|"
    r"expectancy|hit[- ]rate|win[- ]rate|size|sizing|qty|quantity|notional|"
    r"leverage|contracts?|risk\s*%)\b", re.I)


def _now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def capture_path(date, slot, briefs_dir=BRIEFS):
    return Path(briefs_dir) / f"brief_{date}_{slot}.json"


def check_note(text):
    """Refuse outcome or sizing language. Returns the offending words."""
    return sorted({m.group(0).lower() for m in FORBIDDEN.finditer(text or "")})


def append_note(date, slot, text, briefs_dir=BRIEFS, author="operator",
                force=False):
    bad = check_note(text)
    if bad and not force:
        raise SystemExit(
            f"REFUSED: the note contains outcome or sizing language {bad}. "
            f"A note records what was SEEN. What a trade DID is an outcome "
            f"statistic and is census work under G-7; size is never printed by "
            f"this instrument. Rephrase, or pass --force if the match is "
            f"spurious (it is recorded either way).")

    p = capture_path(date, slot, briefs_dir)
    if not p.exists():
        raise SystemExit(f"no capture at {p}")
    doc = json.loads(p.read_text(encoding="utf-8"))

    note = {"ts_utc": _now(), "author": author, "text": text,
            "observation_only": True}
    if bad:
        note["forced_past_guard"] = bad
    doc.setdefault("operator_notes", []).append(note)

    import brief_capture as BC
    p.write_text(BC.serialize(doc), encoding="utf-8", newline="\n")
    sha = hashlib.sha256(p.read_bytes()).hexdigest()

    idx = Path(briefs_dir) / "index.jsonl"
    with idx.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps({"date": date, "slot": slot,
                             "amended_utc": note["ts_utc"],
                             "reason": "operator note appended",
                             "notes": len(doc["operator_notes"]),
                             "json_path": str(p.relative_to(ROOT)).replace("\\", "/")
                             if str(p).startswith(str(ROOT)) else str(p),
                             "json_sha256": sha}, sort_keys=True) + "\n")
    return note, sha


def main():
    ap = argparse.ArgumentParser(description="Append an operator note")
    ap.add_argument("--date", required=True)
    ap.add_argument("--slot", required=True)
    ap.add_argument("--text", required=True)
    ap.add_argument("--author", default="operator")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    note, sha = append_note(args.date, args.slot, args.text,
                            author=args.author, force=args.force)
    print(f"appended note at {note['ts_utc']}")
    print(f"  capture sha256 now {sha}")
    print("  index.jsonl gained a corrected line (append-only, never rewritten)")


if __name__ == "__main__":
    main()
