#!/usr/bin/env python
"""orchestrator_state.py -- emit one machine-readable coordination file.

WHY THIS EXISTS
---------------
Three chats (OPS, STUDY, BRIEF) run against one repo, one ledger, one operator.
They cannot read each other's conversations -- ever. The failure mode is not
collision, it is STALE STATE: a lane asserting repo facts from memory that were
true two sessions ago. The measured cost of relaying that state by hand was
~150 operator actions for 9 real decisions (6%).

This script replaces the relay. Every lane opens its session by reading
_reviewer_box/STATE.json instead of asking the operator to paste anything.

DESIGN DECISIONS -- each is an a-priori choice the operator may veto
--------------------------------------------------------------------
D-OR1  This is a SEPARATE script, not an extension of reviewer_manifest.py,
       which orchestration decision D-O2 called for. Reasons: (a) that tool is
       accepted, fixtured (F-M1..M4), sha-pinned in MANIFEST.json's own sources
       list and cited in the ledger -- editing it invalidates an accepted
       artifact and forces re-acceptance; (b) its concern is INTEGRITY (do the
       bytes on disk match HEAD), which is study-critical, while this concern is
       COORDINATION, which is ops. Ops iteration must not share a blast radius
       with study-critical code. The "two beacons that can disagree" risk that
       D-O2 was protecting against is answered by DEPENDENCE, not merger: this
       script does not recompute repo state, it READS MANIFEST.json and halts if
       the manifest is stale against HEAD. There remains exactly one source of
       repo truth. REVERSIBLE: fold into reviewer_manifest.py on request.

D-OR2  Lane keys are `ops`, `study`, `brief` (operator ruling, 2026-07-28,
       replacing the inverted SYSTEM/ENGINE conventions that were both live).

D-OR3  Commit -> lane mapping extends D-O3 under the rename:
         ops:   / chore:            -> ops
         brief:                     -> brief
         census / tc / s1-3 / rc /
         phase names                -> study
         docs:                      -> unassigned (any lane may write docs)

D-OR4  STATE.json is written to _reviewer_box/, which is gitignored. It is
       DERIVED and regenerated, never authored, so it must not be tracked --
       a tracked derived file produces merge noise and invites hand-editing.

D-OR5  `git log` is read for commit classification only. daily_routine.py's
       contract forbids the RUNNER from touching git; a job reading history is
       non-mutating and cannot corrupt state. It degrades gracefully: with
       --no-git, lanes are derived from LEDGER.md alone and STATE.json records
       lane_source="ledger" so the reader knows which basis produced it.

INVARIANTS
----------
  * repo root resolved from this file's own location -- never hardcoded
  * READ-ONLY on everything except its single declared output
  * no commit, no add, no checkout, no push, no fetch -- ever
  * every number carries its basis; nothing is asserted without a source
  * if the manifest is stale against HEAD, STATE.json still writes but sets
    manifest_fresh=false and stale_reason -- a loud false, never a silent guess
"""

import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_VERSION = 1

MANIFEST = ROOT / "_reviewer_box" / "MANIFEST.json"
LEDGER = ROOT / "LEDGER.md"
REGISTER = ROOT / "Naiad_Orchestration_and_Open_Questions.md"
OUT = ROOT / "_reviewer_box" / "STATE.json"

STATUS_DOCS = {
    "ops": ROOT / "claude" / "STATUS_OPS.md",
    "study": ROOT / "claude" / "STATUS_STUDY.md",
    "brief": ROOT / "claude" / "STATUS_BRIEF.md",
}

# D-OR3 commit -> lane
LANE_PATTERNS = [
    ("ops", re.compile(r"^(ops|chore)\s*[:(]", re.I)),
    ("brief", re.compile(r"^brief\s*[:(]", re.I)),
    ("study", re.compile(r"^(census|tc\d|s[123]\b|rc\d|s2b)", re.I)),
]
STALE_DAYS = 2.0

# The register was written under the retired lane names. Operator ruling
# 2026-07-28 renames them; this normalises historic tags without editing the
# register, which stays canonical and is rewritten by a human, not by this tool.
LANE_ALIASES = {"system": "ops", "engine": "study", "brief": "brief", "all": "all"}


def now_utc():
    return datetime.now(timezone.utc)


def sha256_file(path):
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def git(*args):
    """Read-only git. Returns stdout or None. Never raises."""
    try:
        r = subprocess.run(
            ["git", *args], cwd=str(ROOT), capture_output=True, text=True, timeout=30
        )
        return r.stdout.strip() if r.returncode == 0 else None
    except Exception:
        return None


# ------------------------------------------------------------------ manifest


def read_manifest():
    if not MANIFEST.exists():
        return None, "MANIFEST.json absent -- run scripts/reviewer_manifest.py"
    try:
        with MANIFEST.open(encoding="utf-8") as fh:
            return json.load(fh), None
    except Exception as exc:
        return None, f"MANIFEST.json unreadable: {exc}"


def manifest_block(man, err, use_git):
    if man is None:
        return {"available": False, "stale_reason": err, "manifest_fresh": False}

    head = man.get("head")
    live_head = git("rev-parse", "HEAD") if use_git else None
    if live_head is None:
        fresh, reason = None, "HEAD not read (--no-git); freshness undetermined"
    elif live_head == head:
        fresh, reason = True, None
    else:
        fresh = False
        reason = f"manifest head {head[:8]} != live HEAD {live_head[:8]} -- rerun reviewer_manifest.py"

    srcs = man.get("sources", [])
    mism = [s["path"] for s in srcs if not s.get("match_head", True)]
    box = man.get("reviewer_box", [])
    box_mism = [b["path"] for b in box if not b.get("match_head", True)]

    return {
        "available": True,
        "manifest_fresh": fresh,
        "stale_reason": reason,
        "generated_utc": man.get("generated_utc"),
        "head": head,
        "origin_head": man.get("origin_head"),
        "branch": man.get("branch"),
        "ahead_behind": man.get("ahead_behind"),
        "in_sync_with_origin": man.get("head") == man.get("origin_head"),
        "porcelain_count": len(man.get("status_porcelain", [])),
        "porcelain": man.get("status_porcelain", []),
        "untracked_root_count": len(man.get("untracked_root", [])),
        "sources_total": len(srcs),
        "sources_matching_head": len(srcs) - len(mism),
        "sources_mismatched": mism,
        "box_files_total": len(box),
        "box_mismatched": box_mism,
    }


# -------------------------------------------------------------------- ledger


def ledger_block():
    if not LEDGER.exists():
        return {"available": False}
    raw = LEDGER.read_bytes()
    text = raw.decode("utf-8", errors="replace")
    lines = text.splitlines()

    heads = [(i + 1, ln) for i, ln in enumerate(lines) if ln.startswith("## ")]
    last_no, last_line = heads[-1] if heads else (None, None)

    date = None
    if last_line:
        m = re.match(r"##\s*(\d{4}-\d{2}-\d{2})", last_line)
        if m:
            date = m.group(1)

    return {
        "available": True,
        "bytes": len(raw),
        "lines": len(lines),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "entry_count": len(heads),
        "head_entry_line": last_no,
        "head_entry_date": date,
        "head_entry_title": (last_line or "").lstrip("# ").strip(),
        "recent_entry_titles": [ln.lstrip("# ").strip() for _, ln in heads[-5:]],
    }


# --------------------------------------------------------------------- lanes


def lane_of(subject):
    for lane, pat in LANE_PATTERNS:
        if pat.search(subject):
            return lane
    if re.match(r"^docs\s*[:(]", subject, re.I):
        return "unassigned"
    return "unassigned"


def lanes_block(use_git):
    lanes = {k: {"last_commit": None, "commits_seen": 0} for k in ("ops", "study", "brief")}
    lanes["unassigned"] = {"last_commit": None, "commits_seen": 0}

    if not use_git:
        return lanes, "ledger"

    log = git("log", "-80", "--date=short", "--pretty=%H%x1f%ad%x1f%s")
    if not log:
        return lanes, "ledger"

    for row in log.splitlines():
        parts = row.split("\x1f")
        if len(parts) != 3:
            continue
        sha, date, subject = parts
        lane = lane_of(subject)
        blk = lanes[lane]
        blk["commits_seen"] += 1
        if blk["last_commit"] is None:
            blk["last_commit"] = {"sha": sha[:8], "date": date, "subject": subject}
    return lanes, "git+ledger"


# ----------------------------------------------------------------- decisions


def decisions_block():
    """Parse the open-questions register. Counts only; the register stays canonical."""
    if not REGISTER.exists():
        return {"available": False, "register": str(REGISTER.relative_to(ROOT))}

    text = REGISTER.read_text(encoding="utf-8", errors="replace")
    buckets = {"blocking": [], "live": [], "parked": []}
    current = None
    for ln in text.splitlines():
        if ln.startswith("###"):
            # Match on the section's FIRST word only. Substring matching is wrong
            # here: the Live header reads "not blocking, but degrading", so a
            # naive `"blocking" in line` test swallows the whole Live section
            # into blocking. (Found by verification, 2026-07-28.)
            head = re.sub(r"^#+\s*", "", ln)
            head = re.sub(r"[^\w\s]", " ", head).strip().lower()
            first = head.split()[0] if head.split() else ""
            current = first if first in buckets else None
            continue
        m = re.match(r"\*\*(Q-\d+)\s*(?:·|\.)?\s*(.*?)\*\*", ln)
        if m and current:
            title = m.group(2).strip().rstrip("*").strip()
            lane = None
            lm = re.search(r"\*\(([A-Z]+)\)\*", ln)
            if lm:
                lane = LANE_ALIASES.get(lm.group(1).lower(), lm.group(1).lower())
            buckets[current].append({"id": m.group(1), "title": title, "lane_tag": lane})

    return {
        "available": True,
        "register": str(REGISTER.relative_to(ROOT)),
        "blocking_count": len(buckets["blocking"]),
        "live_count": len(buckets["live"]),
        "parked_count": len(buckets["parked"]),
        "open_total": len(buckets["blocking"]) + len(buckets["live"]),
        "blocking": buckets["blocking"],
        "live": buckets["live"],
        "parked": buckets["parked"],
    }


# --------------------------------------------------------------- status docs


def status_docs_block(now):
    out = {}
    for lane, path in STATUS_DOCS.items():
        if not path.exists():
            out[lane] = {"exists": False, "path": str(path.relative_to(ROOT)), "stale": True,
                         "note": "absent -- lane has no current handoff"}
            continue
        mt = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
        age = (now - mt).total_seconds() / 86400.0
        out[lane] = {
            "exists": True,
            "path": str(path.relative_to(ROOT)),
            "mtime_utc": mt.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "age_days": round(age, 2),
            "stale": age > STALE_DAYS,
            "sha256": sha256_file(path),
            "bytes": path.stat().st_size,
        }
    return out


# -------------------------------------------------------------------- render


def summarise(state):
    L = []
    m = state["repo"]
    L.append("ORCHESTRATOR STATE  " + state["generated_utc"])
    if not m.get("available"):
        L.append(f"  repo      : UNAVAILABLE -- {m.get('stale_reason')}")
    else:
        fresh = {True: "fresh", False: "STALE", None: "undetermined"}[m["manifest_fresh"]]
        L.append(f"  repo      : {m['branch']} @ {(m['head'] or '')[:8]}  "
                 f"origin {'in sync' if m['in_sync_with_origin'] else 'DIVERGED'}  "
                 f"manifest {fresh}")
        L.append(f"  integrity : {m['sources_matching_head']}/{m['sources_total']} sources match HEAD  "
                 f"· {m['porcelain_count']} uncommitted · {m['untracked_root_count']} untracked at root")
        if m["sources_mismatched"]:
            L.append(f"              MISMATCH: {', '.join(m['sources_mismatched'][:5])}")
        if m.get("stale_reason"):
            L.append(f"              ! {m['stale_reason']}")
    lg = state["ledger"]
    if lg.get("available"):
        L.append(f"  ledger    : {lg['entry_count']} entries · head {lg['head_entry_date']} "
                 f"(line {lg['head_entry_line']}) · {lg['bytes']:,} B")
    d = state["decisions"]
    if d.get("available"):
        L.append(f"  decisions : {d['blocking_count']} blocking · {d['live_count']} live · "
                 f"{d['parked_count']} parked")
        for q in d["blocking"]:
            L.append(f"              BLOCKING {q['id']} [{q['lane_tag'] or '?'}] {q['title'][:60]}")
    L.append(f"  lanes     : (basis {state['lane_source']})")
    for lane in ("ops", "study", "brief"):
        c = state["lanes"][lane]["last_commit"]
        sd = state["status_docs"][lane]
        doc = "absent" if not sd["exists"] else (
            f"{sd['age_days']}d{' STALE' if sd['stale'] else ''}")
        if c:
            L.append(f"    {lane:<6} last {c['sha']} {c['date']} {c['subject'][:44]:<44} status {doc}")
        else:
            L.append(f"    {lane:<6} no classified commit in window{'':<28} status {doc}")
    return "\n".join(L)


# ---------------------------------------------------------------------- main


def main():
    ap = argparse.ArgumentParser(description="Emit _reviewer_box/STATE.json")
    ap.add_argument("--no-git", action="store_true",
                    help="skip all git reads; lanes derived from ledger only")
    ap.add_argument("--print", dest="do_print", action="store_true",
                    help="print the human summary to stdout")
    args = ap.parse_args()
    use_git = not args.no_git

    now = now_utc()
    man, err = read_manifest()
    lanes, lane_source = lanes_block(use_git)

    state = {
        "schema_version": SCHEMA_VERSION,
        "generated_utc": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "generator": "scripts/orchestrator_state.py",
        "lane_source": lane_source,
        "lane_names": {
            "ops": "reliability, integrity, tooling, how the collaboration works",
            "study": "the v12 study and the trading engine itself",
            "brief": "market observation, measurement, the daily brief",
        },
        "repo": manifest_block(man, err, use_git),
        "ledger": ledger_block(),
        "lanes": lanes,
        "decisions": decisions_block(),
        "status_docs": status_docs_block(now),
        "reads_only": True,
        "caveats": [
            "Conversations are NOT readable across chats. This file carries repo "
            "artifacts only; anything a lane discussed but did not write down is absent.",
            "Repo state is inherited from MANIFEST.json, not recomputed. If "
            "manifest_fresh is false or null, treat every repo number as suspect.",
            "The data estate (klines, journals) is outside the repo and is not "
            "described here at all.",
        ],
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(state, indent=2, sort_keys=True) + "\n"
    OUT.write_text(payload, encoding="utf-8")

    summary = summarise(state)
    if args.do_print:
        print(summary)
    print(f"wrote {OUT.relative_to(ROOT)} ({len(payload):,} B)")

    repo = state["repo"]
    if repo.get("available") and repo.get("manifest_fresh") is False:
        print("WARNING: manifest is stale against HEAD -- rerun reviewer_manifest.py", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
