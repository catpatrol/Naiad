#!/usr/bin/env python
"""TIER-C12 · the PROGRESS ledger merge and the progress law (orchestrator bookkeeping; stdlib only, pure).

Builds research_outputs/tierc12/PROGRESS.json from the per-stage records under research_outputs/tierc12/progress/.
The stage builders write those records and never PROGRESS.json itself (ORCHESTRATOR_RULINGS O-6); every record is
carried verbatim, in plan order.  It computes no number of any book.  The law it holds as data and functions
(added at the TC12-REG commit, LEANS L-0.9 / L-0.10 / L-0.4 / L-0.1) is documented below the stage list.
Run:  ~/venvs/naiad/bin/python -B /Users/luis/Naiad/scripts/tierc12_progress.py [--ledger] [--root=DIR]
"""
from __future__ import annotations

import hashlib
import json
import sys
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


# ═════════════════════════════════════════════════════ THE PROGRESS LAW, AS DATA [LEANS L-0.10, L-0.4, L-0.5]
# `ORDER` above stays the stage list of record.  A sub-stage is a dotted child `<ORDER entry>.<tag>`; no record id
# exists outside ORDER and SUBSTAGES without a dated amendment.  The resume fixture types a second copy of
# RESUME_ORDER, SUBSTAGES and PARALLEL and holds this data equal to it (F-RESUME, F-ORDER).
T12 = "research_outputs/tierc12"
RESUME_PASTE = "exchange/queue/2026-10-09_TC12_RESUME_APOLLO.md"      # binds beside the contract (O-36, RC-5)
SEED = 20261008                    # the header's seed label; F-RESUME holds it equal to the contract's (:4)
COMPLETE, PARTIAL, ABSENT = STATUSES

# L-0.10 point 3 — the order in which records are gated and committed.
RESUME_ORDER = ["STEP Q", "TC12-R0", "TC12-LEANS", "TC12-REG", "TC12-REG.ledger-spec", "TC12-D",
                "TC12-ENV.vendor", "TC12-ENV", "TC12-ENV.score-build", "TC12-V", "TC12-V.trades", "TC12-C.tide",
                "TC12-C", "TC12-V.stamps.c", "TC12-G", "TC12-R.dir", "TC12-R.sfp", "TC12-R.tables", "TC12-R",
                "TC12-V.stamps.r", "TC12-S", "TC12-V.stamps.s", "TC12-L", "TC12-SCORE", "TC12-FIX", "TC12-REVIEW",
                "TC12-CLOSE"]

# L-0.10 point 2 — SUBSTAGES_T: child id -> its ORDER parent, whether it blocks its stage, its depends_on row.
SUBSTAGES = {
    "TC12-REG.ledger-spec": {"parent": "TC12-REG", "blocking": True, "depends_on": ["TC12-REG"]},
    "TC12-D.mirror": {"parent": "TC12-D", "blocking": False, "depends_on": ["TC12-D"]},
    "TC12-ENV.vendor": {"parent": "TC12-ENV", "blocking": True, "depends_on": ["TC12-D"]},
    "TC12-ENV.score-build": {"parent": "TC12-ENV", "blocking": True, "depends_on": ["TC12-ENV"]},
    "TC12-V.trades": {"parent": "TC12-V", "blocking": True, "depends_on": ["TC12-V"]},
    "TC12-C.tide": {"parent": "TC12-C", "blocking": True, "depends_on": ["TC12-ENV"]},
    "TC12-V.stamps.c": {"parent": "TC12-V", "blocking": True, "depends_on": ["TC12-V", "TC12-C"]},
    "TC12-R.dir": {"parent": "TC12-R", "blocking": True,
                   "depends_on": ["TC12-V", "TC12-C", "TC12-V.stamps.c", "TC12-ENV.score-build"]},
    "TC12-R.sfp": {"parent": "TC12-R", "blocking": True, "depends_on": ["TC12-V", "TC12-ENV.score-build"]},
    "TC12-R.tables": {"parent": "TC12-R", "blocking": True,
                      "depends_on": ["TC12-V", "TC12-C", "TC12-ENV.score-build"]},
    "TC12-V.stamps.r": {"parent": "TC12-V", "blocking": True, "depends_on": ["TC12-R.sfp", "TC12-R.tables"]},
    "TC12-V.stamps.s": {"parent": "TC12-V", "blocking": True, "depends_on": ["TC12-S"]},
}

# L-0.10 point 5 — PARALLEL_T: each may START once every entry through PARALLEL_AFTER and every record of its own
# depends_on are COMPLETE-VERIFIED; commits still land in RESUME_ORDER.  PARALLEL_DEPENDS = the two parents' lists.
PARALLEL = ["TC12-G", "TC12-R.dir", "TC12-R.sfp", "TC12-R.tables", "TC12-R", "TC12-V.stamps.r", "TC12-S",
            "TC12-V.stamps.s"]
PARALLEL_AFTER = "TC12-V.stamps.c"
PARALLEL_DEPENDS = {
    "TC12-G": ["TC12-C", "TC12-C.tide", "TC12-V.stamps.c", "TC12-ENV.score-build"],
    "TC12-S": ["TC12-V", "TC12-C.tide", "TC12-R.sfp", "TC12-ENV.score-build"],
}

# L-0.4 — the closed list of records that are COMPLETE-VERIFIED on clauses (1) and (2) alone (documents only).
FIXTURELESS = ("STEP Q", "TC12-R0", "TC12-LEANS")

# L-0.5 — append-only files: every later version carries the earlier bytes as a byte-prefix.
APPEND_ONLY = (T12 + "/ORCHESTRATOR_RULINGS.md", T12 + "/DISCLOSURES.md", T12 + "/LEANS_AMENDMENTS.md",
               T12 + "/AMENDMENTS_PROPOSED.md", T12 + "/DISCLOSURES_BUILD.md", T12 + "/forward/FORWARD_LEDGER.jsonl",
               T12 + "/scores/SUPERSEDED.jsonl", T12 + "/scores/REFILE_LOG.jsonl")

# L-0.4 (1) — the tracked paths the readings themselves re-record, with the records that do so, in order.  While
# the NEXT record of a row is not on file yet, a working file that differs from the last entry is the next record's
# to pin (its gate is open); the earlier entry is held to git by F-RESUME.  Anything else is a moved artifact.
RERECORDED = {
    "scripts/tierc12_progress.py": ["TC12-R0", "TC12-REG"],
    T12 + "/ferry/FERRY_MANIFEST.json": ["TC12-L", "TC12-CLOSE"],
    T12 + "/va/stamps/build_manifest.json": ["TC12-V.stamps.c", "TC12-V.stamps.r", "TC12-V.stamps.s"],
}
QUARANTINE_PREFIX = T12 + "/_det_partial_"        # L-0.4: research_outputs/tierc12/_det_partial_<YYYYMMDD>T<HHMM>Z/
TALLY_WORDS = (" GREEN, ", " RED, ", " NOT RUN")  # L-0.14 C: `  N GREEN, M RED, K NOT RUN`


def halt(msg: str):
    raise SystemExit(f"HALT: {msg}")


def record_name(record_id: str) -> str:
    """The file of a record under progress/ (`STEP Q` is STEP_Q.json)."""
    return record_id.replace(" ", "_") + ".json"


def walk_order() -> list:
    """RESUME_ORDER, then the children that hold no position in it (`TC12-D.mirror`) [L-0.4]."""
    return RESUME_ORDER + [c for c in SUBSTAGES if c not in RESUME_ORDER]


def records(root=ROOT) -> dict:
    """{record id: record} for the records on file, in walk order."""
    d = Path(root) / T12 / "progress"
    out = {}
    for rid in walk_order():
        p = d / record_name(rid)
        if p.exists():
            out[rid] = json.loads(p.read_text(encoding="utf-8"))
    return out


def certified(rel_path, root=ROOT) -> dict:
    """THE ONE HELPER OF EVERY SHA-FIRST READER [L-0.4]: the LAST record, in walk order, whose `artifact_shas`
    names `rel_path` (repo-relative) -> {record, bytes, sha256}.  HALT if no record names it."""
    rel = Path(rel_path)
    rel = rel.relative_to(root).as_posix() if rel.is_absolute() else rel.as_posix()
    hit = None
    for rid, rec in records(root).items():
        e = rec.get("artifact_shas", {}).get(rel)
        if e is not None:
            hit = {"record": rid, "bytes": e["bytes"], "sha256": e["sha256"]}
    if hit is None:
        halt(f"certified({rel!r}): no record under {T12}/progress names that path [L-0.4]")
    return hit


def read_certified(rel_path, root=ROOT) -> bytes:
    """The bytes of a certified path; HALT unless they re-hash to the last record naming it."""
    c = certified(rel_path, root)
    rel = Path(rel_path)
    raw = (rel if rel.is_absolute() else Path(root) / rel).read_bytes()
    if len(raw) != c["bytes"] or hashlib.sha256(raw).hexdigest() != c["sha256"]:
        halt(f"read_certified({str(rel_path)!r}): the file does not re-hash to its entry in {c['record']} [L-0.4 (1)]")
    return raw


# ═════════════════════════════════════════════════════ THE CONTRACT BY ITS PREFIX [LEANS L-0.1, L-0.9]
def contract_of_record(root=ROOT) -> dict:
    """{path, prefix_bytes, prefix_sha256} READ FROM progress/STEP_Q.json — the contract is named by the bytes
    filed at STEP Q, never by a whole-file sha, so a later `BUILT: ` line moves no byte of PROGRESS.json.  (The
    one function that READS the contract through this pin is the pin door's, `tierc12_pins.contract_prefix`.)"""
    step_q = Path(root) / T12 / "progress" / record_name(ORDER[0])
    if not step_q.exists():
        halt(f"{T12}/progress/{record_name(ORDER[0])} is not on file: the contract of record has no pin")
    pin = json.loads(step_q.read_text(encoding="utf-8")).get("artifact_shas", {}).get(CONTRACT)
    if pin is None:
        halt(f"{record_name(ORDER[0])} does not name {CONTRACT}")
    return {"path": CONTRACT, "prefix_bytes": pin["bytes"], "prefix_sha256": pin["sha256"]}


# ═════════════════════════════════════════════════════ THE RECORD LEDGER AND THE RESUME POINT [L-0.3, L-0.4]
def _hashes(p: Path, n: int):
    """(sha256 of the file, sha256 of its first n bytes, its length) — or None when it is not on file."""
    if not p.is_file():
        return None
    raw = p.read_bytes()
    return hashlib.sha256(raw).hexdigest(), hashlib.sha256(raw[:n]).hexdigest(), len(raw)


def _tally(transcript: Path):
    """(GREEN, RED, NOT RUN) of a transcript's tally line, or None when it has none."""
    for line in reversed(transcript.read_text(encoding="utf-8").split("\n")):
        g, mid_g, rest = line.partition(TALLY_WORDS[0])
        r, mid_r, k = rest.partition(TALLY_WORDS[1])
        if mid_g and mid_r and k.endswith(TALLY_WORDS[2]):
            parts = (g.strip(), r.strip(), k[:-len(TALLY_WORDS[2])].strip())
            if all(x.isdigit() for x in parts):
                return tuple(int(x) for x in parts)
    return None


def _awaited(path: str, rid: str, recs: dict):
    """The record that is next to re-record `path` after `rid` and is not on file yet, or None [RERECORDED]."""
    row = RERECORDED.get(path, [])
    later = row[row.index(rid) + 1:] if rid in row else []
    return later[0] if later and later[0] not in recs else None


def record_problems(rid: str, recs: dict, root=ROOT) -> tuple:
    """What keeps one record on file from COMPLETE-VERIFIED, FROM FILES ONLY — L-0.4 clauses (1) for the working
    tree, (2) and (3).  Returns (problems, notes).  The earlier-entry-against-git half of (1) and the typed key
    sets are F-RESUME's; the re-run (4) is the sweep's."""
    root = Path(root)
    rec = recs[rid]
    problems, notes = [], []
    if rec.get("status") != COMPLETE:
        problems.append(f"the record says {rec.get('status')!r}")
    if rec.get("blockers"):
        problems.append(f"{len(rec['blockers'])} blocker(s)")
    for path, e in rec.get("artifact_shas", {}).items():
        if path.startswith(QUARANTINE_PREFIX):
            problems.append(f"names a quarantine path {path}")
            continue
        last = certified(path, root)["record"] == rid
        got = _hashes(root / path, e["bytes"])
        if got is None:
            problems.append(f"{path} is not on file")
        elif path == CONTRACT:                       # the contract is held by its PREFIX [L-0.1]
            if got[1] != e["sha256"] or got[2] < e["bytes"]:
                problems.append(f"{path} moved inside its STEP Q prefix")
        elif (got[0], got[2]) == (e["sha256"], e["bytes"]):
            pass
        elif path in APPEND_ONLY and got[1] == e["sha256"] and got[2] > e["bytes"]:
            if last:
                notes.append(f"{path} grew past this record's bytes (append-only): the next gate re-records it")
        elif not last:
            if path in APPEND_ONLY:
                problems.append(f"{path} (append-only) no longer carries this record's bytes as a prefix")
        elif _awaited(path, rid, recs):
            notes.append(f"{path} is {_awaited(path, rid, recs)}'s to re-record (its gate is open)")
        else:
            problems.append(f"{path} does not re-hash to this record's entry (a moved artifact)")
    fixtures = rec.get("fixtures", [])
    if rid not in FIXTURELESS and not fixtures:
        problems.append("no fixture record")
    for f in fixtures:
        name = f.get("transcript", "?")
        t = root / name
        if f.get("exit_code") != 0 or f.get("legs_red") != 0 or f.get("transcript_drift") is not False:
            problems.append(f"fixture {name}: exit_code / legs_red / transcript_drift not clean")
        elif not t.is_file():
            problems.append(f"fixture {name}: the transcript is not on file")
        elif not f.get("transcript_sha_before") == f.get("transcript_sha_after") == sha(t):
            problems.append(f"fixture {name}: the transcript does not re-hash to the record's two shas")
        else:
            tally = _tally(t)
            if tally is None or tally[1] or tally[0] + tally[2] != f.get("legs_total") or \
                    tally[2] != f.get("legs_not_run"):
                problems.append(f"fixture {name}: the tally disagrees with legs_total / legs_not_run")
    return problems, notes


def ledger(root=ROOT) -> list:
    """THE RECORD LEDGER: one row {record, status, why, notes} per id of walk_order(), derived from files — never
    typed, never stored.  A record over a `depends_on` member that is not COMPLETE-VERIFIED is PARTIAL with it."""
    recs = records(root)
    rows, word = [], {}
    for rid in walk_order():
        if rid not in recs:
            word[rid] = ABSENT
            rows.append({"record": rid, "status": ABSENT, "why": [], "notes": []})
            continue
        problems, notes = record_problems(rid, recs, root)
        for dep in recs[rid].get("depends_on", []):
            if word.get(dep) != COMPLETE:
                problems.append(f"depends on {dep} ({word.get(dep, 'not yet walked')})")
        word[rid] = PARTIAL if problems else COMPLETE
        rows.append({"record": rid, "status": word[rid], "why": problems, "notes": notes})
    return rows


def resume_point(rows: list):
    """THE RESUME POINT [L-0.10 point 4]: the first entry of RESUME_ORDER whose record is absent or not
    COMPLETE-VERIFIED; None when every entry is.  A child outside RESUME_ORDER never moves it."""
    word = {r["record"]: r["status"] for r in rows}
    return next((rid for rid in RESUME_ORDER if word.get(rid) != COMPLETE), None)


def stage_complete(stage: str, rows: list) -> bool:
    """An ORDER stage is COMPLETE-VERIFIED iff its parent record and every BLOCKING child are [L-0.10 point 6]."""
    word = {r["record"]: r["status"] for r in rows}
    need = [stage] + [c for c, row in SUBSTAGES.items() if row["parent"] == stage and row["blocking"]]
    return all(word.get(rid) == COMPLETE for rid in need)


def ledger_lines(rows: list) -> list:
    """The printed RECORD LEDGER and the resume point, as lines."""
    width = max(len(rid) for rid in walk_order())
    out = ["RECORD LEDGER (derived from files; every id of RESUME_ORDER, then the children in no position)"]
    for r in rows:
        tail = " · ".join(r["why"] + r["notes"])
        if r["record"] not in RESUME_ORDER:
            tail = " · ".join(x for x in ("non-blocking, in no position", tail) if x)
        out.append(f"  {r['record']:<{width}}  {r['status']}" + (f"  [{tail}]" if tail else ""))
    point = resume_point(rows)
    out.append(f"RESUME POINT: {point if point is not None else '(none: every record is COMPLETE-VERIFIED)'}")
    return out


# ═════════════════════════════════════════════════════ THE MERGE [L-0.9] — the only writer of PROGRESS.json
def pointer(rel: str, root=ROOT) -> dict | None:
    p = Path(root) / T12 / rel
    return {"path": p.relative_to(root).as_posix(), "sha256": sha(p)} if p.exists() else None


def merge(root=ROOT) -> dict:
    """The merged ledger as a document: the header, then every progress/*.json verbatim in plan order."""
    root = Path(root)
    out = root / T12
    recs = []
    for p in sorted((out / "progress").glob("*.json")):
        rec = json.loads(p.read_text())
        if rec.get("status") not in STATUSES:
            raise SystemExit(f"HALT: {p.name} carries status {rec.get('status')!r}; legal: {STATUSES}")
        rec["_record"] = {"path": p.relative_to(root).as_posix(), "sha256": sha(p)}
        recs.append((stage_key(rec, p.stem), rec))
    stages = [r for _, r in sorted(recs, key=lambda t: t[0])]
    pin = out / "data" / "AS_OF_PIN.json"
    return {
        "tier": "TIER-C12",
        "branch": "v12-v1-census",
        "seed": SEED,
        "contract_of_record": contract_of_record(root),
        "resume_paste_of_record": {"path": RESUME_PASTE, "sha256": certified(RESUME_PASTE, root)["sha256"]},
        "rulings_of_record": pointer("ORCHESTRATOR_RULINGS.md", root),
        "leans_of_record": pointer("LEANS.md", root),
        "amendments_of_record": pointer("LEANS_AMENDMENTS.md", root),
        "registrations_of_record": pointer("registrations/REGISTRY_PIN.json", root),
        "as_of_pin": json.loads(pin.read_text()) if pin.exists() else None,
        "law_1_note": "a stage is COMPLETE only if its artifacts exist, manifest shas verify, and its fixtures RE-PASS now.",
        "merge_law": "stage records are written by the builders under progress/ and merged here verbatim, in plan order",
        "stages": stages,
    }


def render(doc: dict) -> str:
    return json.dumps(doc, indent=2, ensure_ascii=False, sort_keys=False) + "\n"


def main(argv=None) -> None:
    args = sys.argv[1:] if argv is None else list(argv)
    root = Path(next((a.split("=", 1)[1] for a in args if a.startswith("--root=")), ROOT)).resolve()
    if "--ledger" not in args:                    # --ledger prints the ledger and writes nothing
        doc = merge(root)
        (root / T12 / "PROGRESS.json").write_text(render(doc), encoding="utf-8")
        for s in doc["stages"]:
            print(f"{s.get('stage')!s:<16} {s.get('status')}")
    for line in ledger_lines(ledger(root)):
        print(line)


if __name__ == "__main__":
    main()
