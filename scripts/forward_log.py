#!/usr/bin/env python
"""forward_log.py -- FORWARD-0, the hash-chained trade diary (v4 Phase III).

    python scripts/forward_log.py --verify
    python scripts/forward_log.py --log --kind mechanical ...

A DIARY, NOT A SCOREBOARD.  It records what was intended, when, and on what
basis, so that when a forward-validation hypothesis is eventually registered
under G-10 the record already has integrity instead of being reconstructed from
memory.

PROHIBITED UNTIL G-10 IS SEPARATELY RATIFIED: any aggregate, win rate,
expectancy, P&L summary, "how did the flagged setups do", or any statistic
whatsoever computed over this log.  F-F3 scans this file to prove none exists.

    Recording an exit is diary-keeping.  Aggregating exits is a statistic.
    The line sits exactly there.

RENUMBER NOTE.  The Forward Validation Protocol was drafted as G-9; G-9 is
already the ratified standing rule on relative fixture tolerances, so it is
renumbered G-10 throughout.  This rests on a cross-lane [agent]-tagged claim
rather than a first-hand read of the G-register; it is cheap and reversible and
the basis is recorded here so the choice stays explicable.

APPEND-ONLY AND EXITS.  §III.2 says exits are "status transitions on the same
entry", and the log is append-only.  Those are reconciled the only way they can
be: a transition is a NEW LINE carrying the same `id` and a new `status`, never
an edit to an existing line.  The current state of an entry is its most recent
line.  Editing a stored line breaks the chain from that point forward, which is
exactly what makes "I recorded this before I knew the outcome" credible --
including to yourself, which is the harder audience.
"""

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

LOG_PATH = ROOT / "ops" / "forward_log.jsonl"
BRIEFS_DIR = ROOT / "briefs"

# Strictly separated, never mixed in any later sample (§III.2).
KINDS = ("mechanical", "hypothetical", "actual")

STATUSES = ("open", "closed", "invalidated", "cancelled")

GENESIS = "0" * 64

# The record schema, in order.  Declared as data so F-F5 and the CLI cannot
# drift from each other.
FIELDS = ("id", "ts_utc", "kind", "symbol", "lens", "direction", "trigger",
          "entry_level", "stop_level", "targets", "brief_date", "brief_slot",
          "brief_json_sha256", "rules_version", "analytics_version", "note",
          "status", "exit_ts_utc", "exit_level", "exit_reason",
          "prev_sha256", "entry_sha256")


def _now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def canonical(entry):
    """Canonical JSON of an entry EXCLUDING its own sha.

    A digest cannot cover itself, so `entry_sha256` is removed before hashing.
    Sorted keys and compact separators make the bytes independent of field
    order, so re-reading and re-hashing a stored line reproduces the digest.
    """
    body = {k: v for k, v in entry.items() if k != "entry_sha256"}
    return json.dumps(body, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False)


def chain_hash(entry, prev_sha256):
    """entry_sha256 = sha256(canonical_json(entry_without_own_sha) + prev_sha256)."""
    blob = (canonical(entry) + str(prev_sha256)).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def read_lines(path=LOG_PATH):
    """Raw entries in file order.  For APPEND and VERIFY only.

    Deliberately not a sampling surface: nothing here selects, filters or
    combines entries for analysis.  `entries_of_kind` is the only selector and
    it requires an explicit kind (F-F4).
    """
    p = Path(path)
    if not p.exists():
        return []
    out = []
    for i, line in enumerate(p.read_text(encoding="utf-8").splitlines()):
        if not line.strip():
            continue
        try:
            out.append(json.loads(line))
        except ValueError as exc:
            raise ValueError(f"{p.name}:{i + 1} is not valid JSON: {exc}") from exc
    return out


def last_sha(path=LOG_PATH):
    lines = read_lines(path)
    return lines[-1]["entry_sha256"] if lines else GENESIS


def make_entry(kind, symbol, lens, direction, trigger, entry_level, stop_level,
               targets, brief_date, brief_slot, brief_json_sha256,
               rules_version, analytics_version, note="", status="open",
               entry_id=None, ts_utc=None, exit_ts_utc=None, exit_level=None,
               exit_reason=None, prev_sha256=GENESIS):
    """Build one fully-populated entry, chained onto `prev_sha256`."""
    if kind not in KINDS:
        raise ValueError(f"kind must be one of {KINDS}, got {kind!r}")
    if status not in STATUSES:
        raise ValueError(f"status must be one of {STATUSES}, got {status!r}")
    if direction not in ("long", "short"):
        raise ValueError(f"direction must be long|short, got {direction!r}")

    entry = {
        "id": entry_id or hashlib.sha256(
            f"{symbol}{lens}{ts_utc or _now()}{trigger}".encode()).hexdigest()[:16],
        "ts_utc": ts_utc or _now(),
        "kind": kind,
        "symbol": symbol,
        "lens": lens,
        "direction": direction,
        "trigger": trigger,
        "entry_level": entry_level,
        "stop_level": stop_level,
        "targets": list(targets or []),
        "brief_date": brief_date,
        "brief_slot": brief_slot,
        "brief_json_sha256": brief_json_sha256,
        "rules_version": rules_version,
        "analytics_version": analytics_version,
        "note": note,
        "status": status,
        "exit_ts_utc": exit_ts_utc,
        "exit_level": exit_level,
        "exit_reason": exit_reason,
        "prev_sha256": prev_sha256,
    }
    entry["entry_sha256"] = chain_hash(entry, prev_sha256)
    return entry


def append_entry(entry, path=LOG_PATH):
    """Append one entry.  NEVER rewrites, NEVER reorders (F-F2)."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    expected_prev = last_sha(p)
    if entry["prev_sha256"] != expected_prev:
        raise ValueError(
            f"refusing to append: prev_sha256 {entry['prev_sha256'][:12]}... "
            f"does not match the log head {expected_prev[:12]}.... Rewriting "
            f"history is refused; append a new line instead.")
    if entry["entry_sha256"] != chain_hash(entry, entry["prev_sha256"]):
        raise ValueError("entry_sha256 does not match the entry's own content")
    with p.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(entry, sort_keys=True, ensure_ascii=False) + "\n")
    return entry


def log_intent(kind, symbol, lens, direction, trigger, entry_level, stop_level,
               targets, brief_date, brief_slot, brief_json_sha256,
               rules_version, analytics_version, note="", path=LOG_PATH):
    """Record an intent, chained onto the current head."""
    entry = make_entry(kind, symbol, lens, direction, trigger, entry_level,
                       stop_level, targets, brief_date, brief_slot,
                       brief_json_sha256, rules_version, analytics_version,
                       note=note, status="open", prev_sha256=last_sha(path))
    return append_entry(entry, path)


def log_transition(entry_id, status, exit_level=None, exit_reason=None,
                   exit_ts_utc=None, note="", path=LOG_PATH):
    """Record a status transition as a NEW appended line on the same id.

    This is diary-keeping.  It records THAT an entry ended and at what level; it
    computes nothing over the ending, and nothing in this module reads
    `exit_level` back for any purpose other than writing it down.
    """
    if status not in STATUSES:
        raise ValueError(f"status must be one of {STATUSES}, got {status!r}")
    prior = None
    for e in read_lines(path):
        if e["id"] == entry_id:
            prior = e
    if prior is None:
        raise ValueError(f"no entry with id {entry_id!r} to transition")

    prev = last_sha(path)
    entry = dict(prior)
    entry.update({"ts_utc": _now(), "status": status,
                  "exit_ts_utc": exit_ts_utc or _now(),
                  "exit_level": exit_level, "exit_reason": exit_reason,
                  "note": note or prior.get("note", ""),
                  "prev_sha256": prev})
    entry.pop("entry_sha256", None)
    entry["entry_sha256"] = chain_hash(entry, prev)
    return append_entry(entry, path)


def verify_chain(path=LOG_PATH):
    """F-F1/F-F2 -- walk the chain and report the first break.

    Returns integrity metadata only.  `checked` counts LINES for the integrity
    report; it is not a statistic about trading, and nothing here touches
    outcome fields.
    """
    lines = read_lines(path)
    prev = GENESIS
    for i, e in enumerate(lines):
        if e.get("prev_sha256") != prev:
            return {"ok": False, "checked": i, "first_bad_line": i + 1,
                    "reason": "prev_sha256 does not match the previous entry's "
                              "digest -- a line was inserted, removed or reordered",
                    "id": e.get("id")}
        recomputed = chain_hash(e, prev)
        if recomputed != e.get("entry_sha256"):
            return {"ok": False, "checked": i, "first_bad_line": i + 1,
                    "reason": "entry_sha256 does not match the line's own "
                              "content -- the line was edited after it was written",
                    "id": e.get("id")}
        prev = e["entry_sha256"]
    return {"ok": True, "checked": len(lines), "head": prev,
            "first_bad_line": None, "reason": None}


def verify_capture_linkage(path=LOG_PATH, briefs_dir=BRIEFS_DIR):
    """F-F5 -- every entry's brief_json_sha256 matches a stored capture."""
    known = set()
    idx = Path(briefs_dir) / "index.jsonl"
    if idx.exists():
        for line in idx.read_text(encoding="utf-8").splitlines():
            if line.strip():
                known.add(json.loads(line)["json_sha256"])
    for p in Path(briefs_dir).glob("brief_*_*.json"):
        known.add(hashlib.sha256(p.read_bytes()).hexdigest())

    orphans = []
    for e in read_lines(path):
        sha = e.get("brief_json_sha256")
        if sha and sha not in known:
            orphans.append({"id": e.get("id"), "brief_json_sha256": sha})
    return {"ok": not orphans, "orphans": orphans, "captures_known": len(known)}


def entries_of_kind(kind, path=LOG_PATH):
    """The ONLY selector, and it requires an explicit kind (F-F4).

    There is deliberately no "give me everything" sampling surface: mechanical,
    hypothetical and actual entries are different species of claim, and a
    function that returned them together would make mixing them the easy path.
    """
    if kind not in KINDS:
        raise ValueError(f"kind must be one of {KINDS}, got {kind!r}")
    return [e for e in read_lines(path) if e.get("kind") == kind]


def main():
    ap = argparse.ArgumentParser(description="FORWARD-0 trade diary")
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--log", action="store_true")
    ap.add_argument("--transition", metavar="ID")
    ap.add_argument("--kind", choices=KINDS)
    ap.add_argument("--symbol"); ap.add_argument("--lens")
    ap.add_argument("--direction", choices=("long", "short"))
    ap.add_argument("--trigger"); ap.add_argument("--entry", type=float)
    ap.add_argument("--stop", type=float)
    ap.add_argument("--targets", default="")
    ap.add_argument("--brief-date"); ap.add_argument("--brief-slot")
    ap.add_argument("--note", default="")
    ap.add_argument("--status", choices=STATUSES)
    ap.add_argument("--exit-level", type=float)
    ap.add_argument("--exit-reason")
    args = ap.parse_args()

    if args.verify:
        chain = verify_chain()
        link = verify_capture_linkage()
        print(f"chain     : {'OK' if chain['ok'] else 'BROKEN'} "
              f"({chain['checked']} line(s) checked)")
        if not chain["ok"]:
            print(f"  first bad line {chain['first_bad_line']}: {chain['reason']}")
        print(f"linkage   : {'OK' if link['ok'] else 'ORPHANS'} "
              f"({link['captures_known']} capture sha(s) known)")
        for o in link["orphans"]:
            print(f"  orphan {o['id']}: {o['brief_json_sha256'][:16]}...")
        print("\nNO AGGREGATION: this log is a diary. Any statistic over it "
              "waits on G-10 being separately ratified.")
        return 0 if (chain["ok"] and link["ok"]) else 1

    if args.transition:
        e = log_transition(args.transition, args.status or "closed",
                           exit_level=args.exit_level,
                           exit_reason=args.exit_reason, note=args.note)
        print(f"appended transition {e['id']} -> {e['status']}  "
              f"sha {e['entry_sha256'][:16]}...")
        return 0

    if args.log:
        import analytics
        import brief2 as B2
        sha = ""
        cap = BRIEFS_DIR / f"brief_{args.brief_date}_{args.brief_slot}.json"
        if cap.exists():
            sha = hashlib.sha256(cap.read_bytes()).hexdigest()
        targets = [float(x) for x in args.targets.split(",") if x.strip()]
        e = log_intent(args.kind, args.symbol, args.lens, args.direction,
                       args.trigger, args.entry, args.stop, targets,
                       args.brief_date, args.brief_slot, sha,
                       B2.RULES_VERSION, analytics.ANALYTICS_VERSION,
                       note=args.note)
        print(f"appended {e['kind']} {e['symbol']} {e['direction']}  "
              f"id {e['id']}  sha {e['entry_sha256'][:16]}...")
        return 0

    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
