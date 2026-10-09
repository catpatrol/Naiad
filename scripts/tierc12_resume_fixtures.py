#!/usr/bin/env python
"""TIER-C12 · THE RESUME SUITE [LEANS L-0.1, L-0.3 … L-0.10; the resume paste's F-SEAM] — run at every record gate.

    ~/venvs/naiad/bin/python -B /Users/luis/Naiad/scripts/tierc12_resume_fixtures.py \\
        --stage=<record id> --at=<the last tierc12( commit before the one being made> [--root=DIR]
        [--refile-transcript]

One transcript per record gate: <root>/resume/FIXTURES_RESUME_<record id>.txt (root = research_outputs/tierc12
unless --root=DIR).  Ten blocks, each one `prove` call — a BREAK leg of named plants that must each turn RED on a
scratch estate (a scratch tree and a scratch repository under the temp dir, never the tree of record), then the
REAL leg on the tree of record, read-only (git: read-only verbs under --no-optional-locks):

  F-CONTRACT      L-0.1   the contract by its STEP Q PREFIX; the tail is whole `BUILT: ` lines; no slice leaves it
  F-RESUME        L-0.3/4 every record before the gate COMPLETE-VERIFIED under the LAST-RECORD LAW; certified();
                          RESUME_ORDER data == the typed copy; the seed label; THE RESUME POINT, derived
  F-FROZEN-TEXT   L-0.5   byte-frozen texts at their pins; append-only files grow by byte-prefix; write-once
                          files; the `## AM-` heading law; the LEANS sha one value
  F-FROZEN        L-0.6   the frozen estate against its census (scripts/tierc12_frozen.py); the tierc11x ref
  F-ONE-CORRIDOR  L-0.7   one pin: records, transcripts, manifests, tables; the pre-substrate pair before TC12-D
  F-OFFBUS        L-0.8   nothing of TC12 under exchange/ but the two STEP Q texts
  F-COMMIT        L-0.9   the commit-subject grammar, the path allow-list, the trailer, an empty index
  F-PROGRESS      L-0.9   PROGRESS.json == the merger re-derived; record ids, parents, key sets; the prefix form
  F-ORDER         L-0.10  text before result (T1..T7), the records' commit order, ORDER / SUBSTAGES data
  F-SEAM          paste   SEAM_PASS.json: exactly 70 settlements keyed 1..70; LEANS.md holds exactly 251 readings

THE GATE FORM.  The suite is run at --stage=S before S's own commit exists and — at the filing run — before S's own
progress record exists; its transcript must be byte-identical at the gate's re-run (record on file) and at every
later sweep (later records and commits on file).  So every git fact is read at --at; the records walked are those
at or before S in RESUME_ORDER_T; what S's own commit will add is verified WHEN ON FILE and is mandatory from the
next gate on; no line of the transcript counts or names a thing that S's own record, a later record or a later
commit moves.  The live RECORD LEDGER and resume point (every record on disk) are printed to stdout only.

Exit 0 = every block GREEN and the transcript byte-identical · 1 = a RED / VOID block or a transcript finding ·
2 = a usage error.  Stdlib + the process tools tierc12_fx / tierc12_progress / tierc12_frozen / tierc12_pins
(pandas is imported lazily, only by the one leg that reads a table's stamp column).  No network.
"""
from __future__ import annotations

import ast
import contextlib
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.dont_write_bytecode = True

import tierc12_frozen as FZ  # noqa: E402
import tierc12_fx as FX  # noqa: E402
import tierc12_pins as PINS  # noqa: E402
import tierc12_progress as P  # noqa: E402

ROOT = FX.ROOT

# ═══════════════════════════════════════════════════════════ THE FIXTURE-TYPED COMMISSION (second objects)
T12 = "research_outputs/tierc12"
T11 = "research_outputs/tierc11"
CONTRACT_T = "exchange/queue/2026-10-08_TC12_APOLLO.md"
PASTE_T = "exchange/queue/2026-10-09_TC12_RESUME_APOLLO.md"
STEP_Q_T = "STEP Q"
R0_T = "TC12-R0"
LEANS_REC_T = "TC12-LEANS"
FIRST_GATE_T = "TC12-REG"                 # "every record from TC12-REG" (the suites table)
FIRST_SUBSTRATE_T = "TC12-D"              # L-0.10 point 11: before it, the pre-substrate pair
ORDER_T = ("STEP Q", "TC12-R0", "TC12-LEANS", "TC12-REG", "TC12-D", "TC12-ENV", "TC12-V", "TC12-C", "TC12-G",
           "TC12-R", "TC12-S", "TC12-L", "TC12-SCORE", "TC12-FIX", "TC12-REVIEW", "TC12-CLOSE")
RESUME_ORDER_T = (
    "STEP Q", "TC12-R0", "TC12-LEANS", "TC12-REG", "TC12-REG.ledger-spec", "TC12-D", "TC12-ENV.vendor",
    "TC12-ENV", "TC12-ENV.score-build", "TC12-V", "TC12-V.trades", "TC12-C.tide", "TC12-C", "TC12-V.stamps.c",
    "TC12-G", "TC12-R.dir", "TC12-R.sfp", "TC12-R.tables", "TC12-R", "TC12-V.stamps.r", "TC12-S",
    "TC12-V.stamps.s", "TC12-L", "TC12-SCORE", "TC12-FIX", "TC12-REVIEW", "TC12-CLOSE")
SUBSTAGES_T = {       # child id: (parent, blocking, depends_on)
    "TC12-REG.ledger-spec": ("TC12-REG", True, ("TC12-REG",)),
    "TC12-D.mirror": ("TC12-D", False, ("TC12-D",)),
    "TC12-ENV.vendor": ("TC12-ENV", True, ("TC12-D",)),
    "TC12-ENV.score-build": ("TC12-ENV", True, ("TC12-ENV",)),
    "TC12-V.trades": ("TC12-V", True, ("TC12-V",)),
    "TC12-C.tide": ("TC12-C", True, ("TC12-ENV",)),
    "TC12-V.stamps.c": ("TC12-V", True, ("TC12-V", "TC12-C")),
    "TC12-R.dir": ("TC12-R", True, ("TC12-V", "TC12-C", "TC12-V.stamps.c", "TC12-ENV.score-build")),
    "TC12-R.sfp": ("TC12-R", True, ("TC12-V", "TC12-ENV.score-build")),
    "TC12-R.tables": ("TC12-R", True, ("TC12-V", "TC12-C", "TC12-ENV.score-build")),
    "TC12-V.stamps.r": ("TC12-V", True, ("TC12-R.sfp", "TC12-R.tables")),
    "TC12-V.stamps.s": ("TC12-V", True, ("TC12-S",)),
}
PARALLEL_T = ("TC12-G", "TC12-R.dir", "TC12-R.sfp", "TC12-R.tables", "TC12-R", "TC12-V.stamps.r", "TC12-S",
              "TC12-V.stamps.s")
PARALLEL_AFTER_T = "TC12-V.stamps.c"
PARALLEL_DEPENDS_T = {"TC12-G": ("TC12-C", "TC12-C.tide", "TC12-V.stamps.c", "TC12-ENV.score-build"),
                      "TC12-S": ("TC12-V", "TC12-C.tide", "TC12-R.sfp", "TC12-ENV.score-build")}
NO_POSITION_T = ("TC12-D.mirror",)
WALK_T = RESUME_ORDER_T + NO_POSITION_T
FIXTURELESS_T = ("STEP Q", "TC12-R0", "TC12-LEANS")
STATUSES_T = ("COMPLETE-VERIFIED", "PARTIAL", "ABSENT")
CV, PARTIAL, ABSENT = STATUSES_T
RECORD_KEYS_T = ("stage", "parent", "status", "as_of", "blockers", "depends_on", "artifact_shas", "supersedes",
                 "fixtures", "one_line", "notes")
FIXTURE_KEYS_T = ("suite", "transcript", "provenance", "exit_code", "legs_red", "legs_not_run", "legs_total",
                  "transcript_drift", "transcript_sha_before", "transcript_sha_after", "wall_seconds")
PRELAW_KEYS_T = {
    "STEP Q": ("stage", "status", "as_of", "blockers", "commit", "artifact_shas", "one_line"),
    "TC12-R0": ("stage", "status", "as_of", "blockers", "artifact_shas", "fixtures", "one_line", "notes",
                "r0_census_utc", "head_at_r0", "r0_census", "pre_existing_dirty_paths_not_tc12",
                "operator_ruling_in_session", "x_tip", "x_rec", "frozen_estate_shas_at_r0"),
}
R0_DIRTY_KEY_T = "pre_existing_dirty_paths_not_tc12"
X_TIP_KEY_T = "x_tip"
X_REF_T = "refs/heads/tierc11x"
RULINGS_T = T12 + "/ORCHESTRATOR_RULINGS.md"
DISCLOSURES_T = T12 + "/DISCLOSURES.md"
AMENDMENTS_T = T12 + "/LEANS_AMENDMENTS.md"
PROPOSED_T = T12 + "/AMENDMENTS_PROPOSED.md"
LEANS_T = T12 + "/LEANS.md"
ATTEST_T = T12 + "/review/WORKTREE_ATTEST_LEANS.jsonl"
REGISTRY_T = T12 + "/registrations/REGISTRATIONS.json"
REGISTRY_PIN_T = T12 + "/registrations/REGISTRY_PIN.json"
PROGRESS_T = T12 + "/PROGRESS.json"
PIN_FILE_T = T12 + "/data/AS_OF_PIN.json"
STAGE_D_MANIFEST_T = T12 + "/data/STAGE_D_MANIFEST.json"
EDGE_FILE_T = T11 + "/data/AS_OF_PIN.json"
PIN_ISO_KEY_T = "as_of_last_closed_4h"
PIN_MS_KEY_T = "as_of_last_closed_4h_close_ms"
SNAPSHOT_KEY_T = "snapshot_root"
AS_OF_COL_T = "as_of_last_closed_4h"
MANIFEST_NAME_T = "build_manifest.json"
READ_SET_CLASS_T = "tc12-record"
UNTIL_REG_T = (RULINGS_T, DISCLOSURES_T)       # append-only until the TC12-REG commit, then byte-frozen
APPEND_ONLY_T = UNTIL_REG_T + (AMENDMENTS_T, PROPOSED_T, T12 + "/DISCLOSURES_BUILD.md",
                               T12 + "/forward/FORWARD_LEDGER.jsonl", T12 + "/scores/SUPERSEDED.jsonl",
                               T12 + "/scores/REFILE_LOG.jsonl")
WRITE_ONCE_T = (REGISTRY_T, PIN_FILE_T, T12 + "/forward/BOOK4_FREEZE.json")
BYTE_FROZEN_T = (LEANS_T, REGISTRY_T, REGISTRY_PIN_T, T12 + "/pins/CONTRACT_PIN_MAP.json",
                 T12 + "/pins/CONTRACT_PINS.json", T12 + "/pins/PIN_REGISTER.json",
                 T12 + "/pins/CONTRACT_TOKENS_UNPINNED.json", T12 + "/frozen/FROZEN_ESTATE.json",
                 T12 + "/forward/BOOK_SPEC_COMBINED.json", PIN_FILE_T, T12 + "/va/TRAVERSE.json",
                 T12 + "/forward/BOOK4_FREEZE.json")
RERECORDED_T = {      # L-0.4 (1): the tracked paths the readings re-record, and by which records, in order
    "scripts/tierc12_progress.py": ("TC12-R0", "TC12-REG"),
    T12 + "/ferry/FERRY_MANIFEST.json": ("TC12-L", "TC12-CLOSE"),
    T12 + "/va/stamps/build_manifest.json": ("TC12-V.stamps.c", "TC12-V.stamps.r", "TC12-V.stamps.s"),
}
QUARANTINE_T = T12 + "/_det_partial_"
STEP_Q_PATHS_T = (CONTRACT_T, PASTE_T)          # the two queue texts a `tierc12(STEP Q)` commit may file
TC12_SCRIPT_RX_T = re.compile(r"scripts/tierc12_[A-Za-z0-9_]+\.py")
VALUE_AREA_T = "analytics/value_area.py"
SUBJECT_RX_T = re.compile(r"tierc12\((?P<inner>[^)]*)\): \S")
TIER_PREFIX_T = "tierc12("
TRAILER_RX_T = re.compile(r"Co-Authored-By: .+ <[^<>]+>")
BUS_T = "exchange"
REPORT_T = "exchange/reports/BUILD_2026-10-08_TIERC12_VALUE_AREA.md"
ROWS_T = "exchange/rows/tierc12"
WRITE_RECV_T = ("write_text", "write_bytes", "touch")                    # the path is the RECEIVER
WRITE_PATH_T = ("to_csv", "to_parquet", "to_json")                       # the path is the FIRST ARGUMENT
WRITE_EITHER_T = ("mkdir", "makedirs", "unlink")                         # p.mkdir() or os.mkdir(p)
DEST_ATTRS_T = ("replace", "rename", "copy", "copy2", "copyfile", "copytree", "move", "symlink_to")   # LAST argument
WRITE_MODE_RX_T = re.compile(r"[rwaxbt+]*[wax+][rwaxbt+]*")
BOOK_DIRS_T = ("va/trades", "books", "tide", "regbooks", "stage_g", "stage_r", "stage_s", "forward", "era",
               "ferry", "scores")                # T1: where a book, or a table read off one, is filed
RANGE_DIRS_T = ("stage_r", "stage_s", "regbooks/P-DIR-1", "regbooks/P-SFP-VA-1", "regbooks/P-SCALP-3")   # T2
TRAVERSE_T = "va/TRAVERSE.json"
BOOK4_SPEC_T = "forward/BOOK_SPEC_COMBINED.json"
BOOK4_SPEC_PATH = T12 + "/" + BOOK4_SPEC_T
BOOK4_RIDE_T = "forward/" + MANIFEST_NAME_T
SCORES_DIR_T = "scores"
REG_IDS_T = ("P-ADM-1", "P-BRD-1", "P-DIR-1", "P-SFP-VA-1", "P-SCALP-3")
STAMPS_CHILDREN_T = ("TC12-V.stamps.c", "TC12-V.stamps.r", "TC12-V.stamps.s")
REGBOOK_MANIFEST_RX_T = re.compile(re.escape(T12) + r"/regbooks/[^/]+/" + re.escape(MANIFEST_NAME_T))
AP_ID_RX_T = re.compile(r"\bAP-\d+\b")
AM_ID_RX_T = re.compile(r"\bAM-\d+\b")
AM_HEAD_RX_T = re.compile(
    r"## AM-(?P<id>\d+) · \d{4}-\d{2}-\d{2} \(~\d{2}:\d{2}Z\) · (?P<readings>.+?) · "
    r"(?P<basis>ruling on AP-(?P<ap>\d+)|contract :32-33 \(no AP\)|operator veto \"[^\"]+\")(?: · .+)?")
AM_LINE_T = "## AM"
AP_HEAD_RX_T = re.compile(r"(?m)^## AP-(\d+) · ")
TALLY_RX_T = re.compile(r"(?m)^  (\d+) GREEN, (\d+) RED, (\d+) NOT RUN$")
SEED_RX_T = re.compile(r"\bSeed (\d+)\.")
SEAM_PASS_T = T12 + "/review/SEAM_PASS.json"
SEAM_RETURNS_T = T12 + "/review/FIX_PASS_1_RETURNS.json"
SEAM_KEY_T = "residual_conflicts"
N_SEAMS_T = 70
N_READINGS_T = 251
SETTLED_BY_T = ("contract", "ruling", "disposition", "pessimistic", "AMENDMENTS_PROPOSED")
READING_HEAD_RX_T = re.compile(r"(?m)^\*\*(L-[0A-Z]+\.\d+) ")
READING_ID_RX_T = re.compile(r"L-[0A-Z]+\.\d+")
N_READINGS_RX_T = re.compile(r"(?m)^n_readings = (\d+)$")
GIT_RO_T = ("rev-parse", "log", "cat-file", "merge-base", "diff")       # the read-only verbs this suite uses
SCRATCH_STAGE_T = "TC12-ENV.vendor"             # the gate the scratch estate is evaluated at (after TC12-D)
SCRATCH_PIN_ISO_T = "2026-10-08T20:00:00Z"
SCRATCH_EDGE_ISO_T = "2026-09-25T00:00:00Z"
SCRATCH_SNAP_T = "tc12_scratch"
SCRATCH_DATE_T = "2026-10-08T00:00:00+0000"
SCRATCH_TRAILER_T = "Co-Authored-By: Scratch Fixture <fixture@scratch.invalid>"
FOUR_H_T = timedelta(hours=4)
SHOW_T = 6                                       # findings printed in a FAIL line before "… and n more"


# ═══════════════════════════════════════════════════════════ small tools
def sha_b(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def entry_of(p: Path):
    if not p.is_file():
        return None
    raw = p.read_bytes()
    return {"bytes": len(raw), "sha256": sha_b(raw)}


def prefix_ok(p: Path, e: dict) -> bool:
    """The entry's bytes are a byte-prefix of the working file."""
    if not p.is_file():
        return False
    raw = p.read_bytes()
    return len(raw) >= e["bytes"] and sha_b(raw[:e["bytes"]]) == e["sha256"]


def name_of(rid: str) -> str:
    return rid.replace(" ", "_") + ".json"


def rid_of(stem: str) -> str:
    return STEP_Q_T if stem == STEP_Q_T.replace(" ", "_") else stem


EPOCH_T = datetime.fromtimestamp(0, timezone.utc)


def iso_ms(text) -> int:
    d = datetime.fromisoformat(str(text).replace("Z", "+00:00"))
    return ((d if d.tzinfo else d.replace(tzinfo=timezone.utc)) - EPOCH_T) // timedelta(milliseconds=1)


def halts(thunk) -> list:
    """A detector that HALTs has found something: its text is the finding."""
    try:
        return thunk()
    except SystemExit as e:
        return [str(e)]


def show(found: list) -> str:
    more = f" … and {len(found) - SHOW_T} more" if len(found) > SHOW_T else ""
    return f"{len(found)} finding(s): " + " · ".join(str(f) for f in found[:SHOW_T]) + more


def subject_id(subject: str):
    """The record id a `tierc12(<ID>[ <words>]): …` subject names: the LONGEST id of RESUME_ORDER_T ∪ the
    no-position children — written with or without its `TC12-` prefix — that is a prefix of the text inside the
    parentheses and is followed by `)` or a space [L-0.9]."""
    m = SUBJECT_RX_T.match(subject)
    if not m:
        return None
    inner = m.group("inner")
    best = None
    for rid in WALK_T:
        for form in {rid, rid[len("TC12-"):] if rid.startswith("TC12-") else rid}:
            if (inner == form or inner.startswith(form + " ")) and (best is None or len(form) > len(best[0])):
                best = (form, rid)
    return best[1] if best else None


def git(root, *args, ro=True, env=None):
    """(exit code, stdout bytes) of one git call on `root`.  The tree of record sees read-only verbs only."""
    if ro and args[0] not in GIT_RO_T:
        raise RuntimeError(f"git {args[0]} is not a read-only verb of this suite")
    e = dict(os.environ, GIT_OPTIONAL_LOCKS="0")
    e.update(env or {})
    r = subprocess.run(["git", "--no-optional-locks", "-c", "core.quotepath=false", "-C", str(root), *args],
                       capture_output=True, env=e)
    return r.returncode, r.stdout


@contextlib.contextmanager
def patched(obj, name: str, value):
    """A sabotage planted INSIDE production: one attribute replaced for the duration of a plant."""
    saved = getattr(obj, name)
    setattr(obj, name, value)
    try:
        yield
    finally:
        setattr(obj, name, saved)


# ═══════════════════════════════════════════════════════════ THE ESTATE under test (the tree of record, or a scratch)
class Estate:
    def __init__(self, root, stage: str, at: str, snapshots=None):
        self.root = Path(root)
        self.t12 = self.root / T12
        self.stage = stage
        self.snapshots = snapshots
        prog = self.t12 / "progress"
        self.recs = {}
        for rid in WALK_T:
            p = prog / name_of(rid)
            if p.is_file():
                self.recs[rid] = json.loads(p.read_text(encoding="utf-8"))
        self.stray = sorted(p.name for p in prog.glob("*.json") if rid_of(p.stem) not in WALK_T)
        self.at = self.rev(at)
        self.first = self.rev(str(self.recs.get(STEP_Q_T, {}).get("commit")))
        self._commits = None

    def rev(self, name: str) -> str:
        rc, out = git(self.root, "rev-parse", "--verify", "--quiet", f"{name}^{{commit}}")
        if rc:
            raise SystemExit(f"HALT: {name!r} is not a commit of the repository under test")
        return out.decode("utf-8").strip()

    def before(self) -> list:
        """The entries of RESUME_ORDER_T that must be COMPLETE-VERIFIED for this gate to be open."""
        if self.stage in NO_POSITION_T:
            parent = SUBSTAGES_T[self.stage][0]
            return list(RESUME_ORDER_T[:RESUME_ORDER_T.index(parent) + 1])
        return list(RESUME_ORDER_T[:RESUME_ORDER_T.index(self.stage)])

    def scope(self) -> list:
        """The records this gate walks: those before it, its own, and a no-position child whose parent is."""
        ids = self.before() + [self.stage]
        return ids + [c for c in NO_POSITION_T if c not in ids and SUBSTAGES_T[c][0] in self.before()]

    def commits(self) -> list:
        """The commits of <STEP Q commit>^..<at>, oldest first: {sha, subject, body, paths [(status, path)]}."""
        if self._commits is None:
            rc, out = git(self.root, "log", "--reverse", "--first-parent", "-m", "--no-renames", "--name-status",
                          "--format=%x01%H%x02%s%x02%B%x03", f"{self.first}^..{self.at}")
            if rc:
                raise SystemExit("HALT: git log failed on the range of the repository under test")
            self._commits = []
            for chunk in out.decode("utf-8").split("\x01")[1:]:
                head, _, rest = chunk.partition("\x03")
                sha, subject, body = head.split("\x02", 2)
                paths = [tuple(x.split("\t", 1)) for x in rest.split("\n") if "\t" in x]
                self._commits.append({"sha": sha, "subject": subject, "body": body, "paths": paths,
                                      "i": len(self._commits)})
        return self._commits

    def closing(self, rid: str):
        """The commit that closed a record: the last one in range that touched progress/<record>.json."""
        path = f"{T12}/progress/{name_of(rid)}"
        hits = [c for c in self.commits() if any(p == path for _, p in c["paths"])]
        return hits[-1] if hits else None

    def first_add(self, rel: str):
        """The first commit in range that ADDS `rel` or a file under it."""
        return next((c for c in self.commits()
                     if any(s == "A" and (p == rel or p.startswith(rel + "/")) for s, p in c["paths"])), None)

    def blob(self, commit: str, path: str):
        rc, out = git(self.root, "cat-file", "blob", f"{commit}:{path}")
        return None if rc else out

    def ancestor(self, a: dict, b: dict) -> bool:
        """`a` is a PROPER ancestor of `b`."""
        return a["sha"] != b["sha"] and git(self.root, "merge-base", "--is-ancestor", a["sha"], b["sha"])[0] == 0


def last_naming(E: Estate) -> dict:
    """path -> the LAST record, in the fixture's own walk of every record on disk, whose artifact_shas names it."""
    last = {}
    for rid in WALK_T:
        for path in E.recs.get(rid, {}).get("artifact_shas") or {}:
            last[path] = rid
    return last


def tier_commits(E: Estate) -> list:
    return [c for c in E.commits() if c["subject"].startswith(TIER_PREFIX_T)]


# ═══════════════════════════════════════════════════════════ F-CONTRACT [L-0.1]
def contract_findings(root) -> list:
    """The ONE prefix function (the pin door's) on the contract of `root`; a slice cut to the prefix's last line
    re-reads the prefix; a slice one line past it HALTs."""
    root = Path(root)
    prefix = PINS.contract_prefix(root / CONTRACT_T, root / T12 / "progress" / name_of(STEP_Q_T))
    out = []
    raw = (root / CONTRACT_T).read_bytes()[:prefix["prefix_bytes"]]
    if (PINS.cut(prefix["lines"], 1, prefix["n_lines"]) + "\n").encode("utf-8") != raw:
        out.append("CONTRACT-SLICE: the slice 1..n_lines does not re-read the prefix bytes")
    past = halts(lambda: [] if PINS.cut(prefix["lines"], prefix["n_lines"], prefix["n_lines"] + 1) else [])
    if not past:
        out.append("CONTRACT-SLICE: a slice one line past the prefix was cut, not refused")
    return out


def contract_seed(root) -> int:
    root = Path(root)
    prefix = PINS.contract_prefix(root / CONTRACT_T, root / T12 / "progress" / name_of(STEP_Q_T))
    seeds = SEED_RX_T.findall("\n".join(prefix["lines"]))
    if len(seeds) != 1:
        raise SystemExit(f"HALT: the contract prefix names {len(seeds)} seeds, not one")
    return int(seeds[0])


# ═══════════════════════════════════════════════════════════ F-RESUME [L-0.3, L-0.4]
def awaited(path: str, rid: str, recs: dict):
    row = RERECORDED_T.get(path, ())
    later = row[row.index(rid) + 1:] if rid in row else ()
    return later[0] if later and later[0] not in recs else None


def fixture_record_findings(E: Estate, rid: str, rec: dict) -> list:
    out = []
    fixtures = rec.get("fixtures") or []
    if rid not in FIXTURELESS_T and not fixtures:
        out.append(f"FIXTURE-RECORD {rid}: COMPLETE-VERIFIED outside the fixtureless list with no fixture record")
    for f in fixtures:
        name = f.get("transcript")
        lack = [k for k in FIXTURE_KEYS_T if k not in f]
        if lack:
            out.append(f"RECORD-KEYS {rid}: a fixture record lacks {lack}")
            continue
        t = E.root / name
        if f["exit_code"] != 0 or f["legs_red"] != 0:
            out.append(f"FIXTURE-RECORD {rid}: {name} carries exit_code {f['exit_code']}, legs_red {f['legs_red']}")
        if f["transcript_drift"] is not False:
            out.append(f"FIXTURE-RECORD {rid}: {name} carries transcript_drift {f['transcript_drift']!r}")
        if not t.is_file():
            out.append(f"FIXTURE-RECORD {rid}: the transcript {name} is not on file")
            continue
        raw = t.read_bytes()
        if not f["transcript_sha_before"] == f["transcript_sha_after"] == sha_b(raw):
            out.append(f"FIXTURE-RECORD {rid}: {name} does not re-hash to the record's before / after shas")
        tallies = TALLY_RX_T.findall(raw.decode("utf-8"))
        g, r, k = (int(x) for x in tallies[-1]) if tallies else (None, None, None)
        if not tallies or r != 0 or g + k != f["legs_total"] or k != f["legs_not_run"]:
            out.append(f"FIXTURE-RECORD {rid}: the tally of {name} ({g} GREEN, {r} RED, {k} NOT RUN) disagrees "
                       f"with legs_total {f['legs_total']} / legs_not_run {f['legs_not_run']}")
        for suffix in ("_rerun.txt", "_partial.txt"):
            if t.with_name(t.stem + suffix).exists():
                out.append(f"RERUN-FILE {rid}: {t.stem + suffix} stands beside the transcript of record {name}")
    return out


def floor_findings(E: Estate, rid: str, rec: dict) -> list:
    """The depends_on FLOOR [L-0.9, seam 4]: the SUBSTAGES_T row, the PARALLEL_T list, and the last earlier
    record naming each tc12-record path of a READ_SET.json the record files."""
    floor = set(SUBSTAGES_T[rid][2] if rid in SUBSTAGES_T else ()) | set(PARALLEL_DEPENDS_T.get(rid, ()))
    for path in rec.get("artifact_shas") or {}:
        if Path(path).name in ("READ_SET.json", f"READ_SET_{rid}.json") and (E.root / path).is_file():
            for read in json.loads((E.root / path).read_text(encoding="utf-8")).get(READ_SET_CLASS_T, []):
                earlier = [r for r in WALK_T[:WALK_T.index(rid)]
                           if read in (E.recs.get(r, {}).get("artifact_shas") or {})]
                floor |= set(earlier[-1:])
    lack = sorted(floor - set(rec.get("depends_on") or []))
    return [f"DEPENDS-FLOOR {rid}: depends_on lacks {lack} of its typed floor"] if lack else []


def walk(E: Estate) -> tuple:
    """The fixture's OWN walk of the records in scope under L-0.4 (1)-(3): (findings, {record id: status})."""
    per = {rid: [] for rid in WALK_T}
    last = last_naming(E)
    scope = E.scope()
    for rid in scope:
        rec = E.recs.get(rid)
        if rec is None:
            continue
        out = per[rid]
        if rec.get("status") not in STATUSES_T:
            out.append(f"RECORD-STATUS {rid}: status {rec.get('status')!r} is not one of {list(STATUSES_T)}")
        if rid not in PRELAW_KEYS_T:
            lack = [k for k in RECORD_KEYS_T if k not in rec]
            if lack:
                out.append(f"RECORD-KEYS {rid}: lacks {lack} of the typed key set")
        if rec.get("status") == CV and rec.get("blockers"):
            out.append(f"BLOCKERS {rid}: COMPLETE-VERIFIED with {len(rec['blockers'])} blocker(s)")
        for path, e in (rec.get("artifact_shas") or {}).items():
            f = E.root / path
            if path.startswith(QUARANTINE_T):
                out.append(f"QUARANTINE-PATH {rid}: names the quarantine path {path}")
                continue
            if last[path] == rid:
                now = entry_of(f)
                if path == CONTRACT_T:
                    if not prefix_ok(f, e):
                        out.append(f"ARTIFACT-MOVED {rid}: {path} moved inside its STEP Q prefix")
                    continue
                if now is None:
                    out.append(f"ARTIFACT-MISSING {rid}: {path} is not on file")
                    continue
                if now == e or (path in APPEND_ONLY_T and prefix_ok(f, e)):
                    continue                       # grown append-only bytes are the open gate's to re-record
                if not awaited(path, rid, E.recs):
                    out.append(f"ARTIFACT-MOVED {rid}: {path} does not re-hash to the entry of the last record "
                               f"that names it")
                    continue
            # an EARLIER entry (or one whose typed re-record is awaited): held to the blob at its closing commit
            if path in APPEND_ONLY_T and not prefix_ok(f, e):
                out.append(f"APPEND-PREFIX {rid}: the bytes this record names for {path} (append-only) are not a "
                           f"byte-prefix of the working file")
            c = E.closing(rid)
            if c is None:
                if rid != E.stage:
                    out.append(f"EARLIER-BLOB {rid}: no commit in range closed this record, so {path} cannot be "
                               f"held to its blob")
                continue
            b = E.blob(c["sha"], path)
            if b is None:                          # untracked at the closing commit: only `supersedes` waives it
                final = E.recs[last[path]]["artifact_shas"][path]
                waived = any(s.get("path") == path and s.get("old_sha256") == e["sha256"] and s.get("reason")
                             for r in WALK_T[WALK_T.index(rid) + 1:]
                             for s in (E.recs.get(r, {}).get("supersedes") or []))
                if final["sha256"] != e["sha256"] and not waived:
                    per[last[path]].append(
                        f"SUPERSEDES {last[path]}: re-records the untracked path {path} (earlier entry in {rid}) "
                        f"with no supersedes entry {{path, old_sha256, reason}}")
            elif (len(b), sha_b(b)) != (e["bytes"], e["sha256"]):
                out.append(f"EARLIER-BLOB {rid}: the blob of {path} at the commit that closed this record does "
                           f"not re-hash to its entry")
        if rec.get("status") == CV:
            out += fixture_record_findings(E, rid, rec)
        if rid not in PRELAW_KEYS_T:
            out += floor_findings(E, rid, rec)
    for child in NO_POSITION_T:                   # no other record may name a path of the non-blocking child
        for path in E.recs.get(child, {}).get("artifact_shas") or {}:
            for rid in scope:
                if rid != child and path in (E.recs.get(rid, {}).get("artifact_shas") or {}):
                    per[rid].append(f"MIRROR-PATH {rid}: names {path}, a path of {child}")
    word = {}
    for rid in WALK_T:                             # quarantine follows depends_on, transitively
        rec = E.recs.get(rid)
        if rec is None:
            word[rid] = ABSENT
            continue
        low = sorted(d for d in (rec.get("depends_on") or []) if word.get(d, ABSENT) != CV)
        if low and rec.get("status") == CV and rid in scope:
            per[rid].append(f"DEPENDS-CLOSURE {rid}: reads COMPLETE-VERIFIED over {low}, not COMPLETE-VERIFIED")
        word[rid] = CV if rec.get("status") == CV and not per[rid] else PARTIAL
    return [x for rid in WALK_T for x in per[rid]], word


def resume_findings(E: Estate) -> list:
    out, word = walk(E)
    low = [f"{rid} ({word[rid]})" for rid in E.before() if word[rid] != CV]
    if low:
        out.append(f"GATE-ORDER {E.stage}: the gate is not open — {low} before it in RESUME_ORDER_T")
    for path, rid in sorted(last_naming(E).items()):
        want = dict(E.recs[rid]["artifact_shas"][path], record=rid)
        got = halts(lambda: P.certified(path, E.root))
        if got != want:
            out.append(f"CERTIFIED {path}: certified() returns {got if isinstance(got, list) else got.get('record')}"
                       f", the fixture's walk of RESUME_ORDER_T finds {rid} last")
    if tuple(P.RESUME_ORDER) != RESUME_ORDER_T:
        out.append("RESUME-ORDER: scripts/tierc12_progress.py RESUME_ORDER differs from the fixture's typed copy")
    seed = contract_seed(E.root)
    if P.SEED != seed:
        out.append(f"SEED-LABEL: the merger's seed label {P.SEED} is not the contract's seed {seed}")
    rows = {r["record"]: r["status"] for r in P.ledger(E.root)}
    out += [f"LEDGER-DISAGREE {rid}: the printed ledger says {rows.get(rid)}, the fixture's walk {word[rid]}"
            for rid in E.before() if rows.get(rid) != word[rid]]
    return out


def resume_point(E: Estate, word: dict):
    """The first entry of RESUME_ORDER_T, the gate's own record set aside, that is absent or not verified."""
    return next((rid for rid in RESUME_ORDER_T if rid == E.stage or word[rid] != CV), None)


# ═══════════════════════════════════════════════════════════ F-FROZEN-TEXT [L-0.5]
def registry_pins(E: Estate):
    """(REGISTRATIONS.json, REGISTRY_PIN.json) as documents, None where not on file."""
    docs = []
    for rel in (REGISTRY_T, REGISTRY_PIN_T):
        p = E.root / rel
        docs.append(json.loads(p.read_text(encoding="utf-8")) if p.is_file() else None)
    return tuple(docs)


def leans_pin_of(pin_doc: dict):
    v = pin_doc.get("leans_sha256", pin_doc.get("leans"))
    return v.get("sha256") if isinstance(v, dict) else v


def am_findings(E: Estate) -> list:
    out = []
    p = E.root / AMENDMENTS_T
    if not p.is_file():
        return out
    proposed = (E.root / PROPOSED_T).read_text(encoding="utf-8") if (E.root / PROPOSED_T).is_file() else ""
    on_file = set(AP_HEAD_RX_T.findall(proposed))
    ids = []
    for line in p.read_text(encoding="utf-8").split("\n"):
        if not line.startswith(AM_LINE_T):
            continue
        m = AM_HEAD_RX_T.fullmatch(line)
        if not m:
            out.append(f"AM-FORM: the heading {line[:60]!r} is not `## AM-<integer> · <date> (~HH:MMZ) · <reading "
                       f"ids> · <basis>[ · <nickname>]`")
            continue
        ids.append(int(m.group("id")))
        if m.group("ap") is not None and m.group("ap") not in on_file:
            out.append(f"AM-FORM: AM-{m.group('id')} is ruled on AP-{m.group('ap')}, which is not on file")
    if ids != list(range(1, len(ids) + 1)):
        out.append(f"AM-FORM: the amendment ids {ids} do not ascend from 1")
    return out


def frozen_text_findings(E: Estate) -> list:
    out = []
    after_reg = RESUME_ORDER_T.index(E.stage) > RESUME_ORDER_T.index(FIRST_GATE_T) if E.stage in RESUME_ORDER_T \
        else True
    for rel in BYTE_FROZEN_T:                       # (a) a byte-frozen file at the sha of EVERY record naming it
        named = [(rid, E.recs[rid]["artifact_shas"][rel]) for rid in WALK_T
                 if rel in (E.recs.get(rid, {}).get("artifact_shas") or {})]
        if not named:
            continue
        if len({e["sha256"] for _, e in named}) != 1:
            out.append(f"FROZEN-BYTES {rel}: byte-frozen, yet the records {[r for r, _ in named]} name more than "
                       f"one sha")
        if entry_of(E.root / rel) != named[-1][1]:
            out.append(f"FROZEN-BYTES {rel}: does not re-hash to its pin in {named[-1][0]}")
    registry, pin = registry_pins(E)
    if registry is None or pin is None:
        if after_reg:
            out.append("FROZEN-BYTES: the registry (REGISTRATIONS.json, REGISTRY_PIN.json) is not on file after "
                       "the TC12-REG gate")
    else:
        for rel, key in ((RULINGS_T, "rulings"), (DISCLOSURES_T, "disclosures")):
            now = entry_of(E.root / rel)
            if now is None or now["sha256"] != (registry.get(key) or {}).get("sha256"):
                out.append(f"FROZEN-BYTES {rel}: byte-frozen at the registry's `{key}.sha256`, and it no longer "
                           f"re-hashes to it")
    commits = tier_commits(E)
    reg_commit = E.first_add(REGISTRY_T)
    for c in commits:                              # (b) append-only: the parent blob is a byte-prefix
        for status, path in c["paths"]:
            if path not in APPEND_ONLY_T or status == "A":
                continue
            if path in UNTIL_REG_T and reg_commit is not None and c["i"] > reg_commit["i"]:
                out.append(f"FROZEN-BYTES {path}: changed by `{c['subject'][:48]}` after the registry commit")
            new, old = E.blob(c["sha"], path), E.blob(c["sha"] + "^", path)
            if new is None or old is None or new[:len(old)] != old:
                out.append(f"APPEND-ONLY {path}: `{c['subject'][:48]}` did not append — its parent's bytes are "
                           f"not a byte-prefix of its own")
    for rel in WRITE_ONCE_T:                       # (c) write-once: one blob in the range
        touches = [c for c in commits if any(p == rel for _, p in c["paths"])]
        if len(touches) > 1:
            out.append(f"WRITE-ONCE {rel}: {len(touches)} commits in range touch it: "
                       f"{[c['subject'][:32] for c in touches]}")
        elif touches and E.blob(touches[0]["sha"], rel) != ((E.root / rel).read_bytes()
                                                             if (E.root / rel).is_file() else None):
            out.append(f"WRITE-ONCE {rel}: the working file is not the blob that filed it")
    out += am_findings(E)                           # (d) the amendments' heading law
    values = {}                                     # (e) the LEANS sha is ONE value
    now = entry_of(E.root / LEANS_T)
    values["the working file"] = now["sha256"] if now else None
    values["its record"] = ((E.recs.get(LEANS_REC_T, {}).get("artifact_shas") or {}).get(LEANS_T) or {}).get(
        "sha256")
    attest = E.root / ATTEST_T
    head = json.loads(attest.read_text(encoding="utf-8").split("\n")[0]) if attest.is_file() else {}
    values["the hash-bound attestation"] = (head.get("frozen") or {}).get("sha256")
    if registry is not None and pin is not None:
        values["REGISTRATIONS.json leans"] = (registry.get("leans") or {}).get("sha256")
        values["REGISTRY_PIN.json leans"] = leans_pin_of(pin)
    if len(set(values.values())) != 1 or None in values.values():
        out.append(f"FROZEN-LEANS: the LEANS sha is not one value — "
                   f"{ {k: (v or 'absent')[:12] for k, v in values.items()} }")
    return out


# ═══════════════════════════════════════════════════════════ F-FROZEN [L-0.6]
def frozen_findings(E: Estate) -> list:
    """The estate is the MAIN tree's: from a linked worktree the untracked estate and x_rec exist only there."""
    out = halts(lambda: FZ.findings(PINS.main_tree(E.root), snapshots=E.snapshots))
    rc, ref = git(E.root, "rev-parse", "--verify", "--quiet", X_REF_T)
    tip = E.recs.get(R0_T, {}).get(X_TIP_KEY_T)
    if rc or ref.decode("utf-8").strip() != tip:
        out.append(f"X-TIP {X_REF_T}: the ref is not the x_tip {R0_T} recorded")
    return out


# ═══════════════════════════════════════════════════════════ F-ONE-CORRIDOR [L-0.7]
def table_instants(path: Path) -> list:
    import pandas as pd                             # lazy: only a directory that holds a table reaches this
    return sorted(set(pd.read_parquet(path, columns=[AS_OF_COL_T])[AS_OF_COL_T].astype(str)))


def corridor_findings(E: Estate) -> list:
    out = []
    pin_iso = edge_iso = snap = None
    if (E.root / PIN_FILE_T).is_file():
        pin_iso = json.loads((E.root / PIN_FILE_T).read_text(encoding="utf-8"))[PIN_ISO_KEY_T]
    if (E.root / EDGE_FILE_T).is_file():
        edge_iso = json.loads((E.root / EDGE_FILE_T).read_text(encoding="utf-8"))[PIN_ISO_KEY_T]
    if (E.root / STAGE_D_MANIFEST_T).is_file():
        snap = Path(json.loads((E.root / STAGE_D_MANIFEST_T).read_text(encoding="utf-8"))[SNAPSHOT_KEY_T]).name
    first = RESUME_ORDER_T.index(FIRST_SUBSTRATE_T)
    for rid in E.scope():
        rec = E.recs.get(rid)
        if rec is None:
            continue
        heads = []
        for f in rec.get("fixtures") or []:
            t = E.root / str(f.get("transcript"))
            heads.append((f.get("transcript"), t.read_text(encoding="utf-8").split("\n")[:2] if t.is_file() else []))
        if rid in RESUME_ORDER_T and RESUME_ORDER_T.index(rid) < first:
            if rec.get("as_of") is not None:
                out.append(f"ONE-CORRIDOR-ASOF {rid}: a record before {FIRST_SUBSTRATE_T} carries as_of "
                           f"{rec.get('as_of')!r}, not null")
            out += [f"ONE-CORRIDOR-HEADER {rid}: {name} does not open with the fixed pre-substrate pair"
                    for name, two in heads if two != [FX.PRE_SUBSTRATE_AS_OF, FX.PRE_SUBSTRATE_LINE]]
            continue
        if pin_iso is None:
            out.append(f"ONE-CORRIDOR-ASOF {rid}: {PIN_FILE_T} is not on file — no pin to hold the record to")
            continue
        instants = {iso_ms(x) for x in (pin_iso, edge_iso) if x is not None}
        if rec.get("as_of") != pin_iso:
            out.append(f"ONE-CORRIDOR-ASOF {rid}: as_of {rec.get('as_of')!r} is not the pin {pin_iso}")
        out += [f"ONE-CORRIDOR-HEADER {rid}: {name} does not open `as_of_last_closed_4h: {pin_iso}`"
                for name, two in heads if two[:1] != [f"as_of_last_closed_4h: {pin_iso}"]]
        for path in rec.get("artifact_shas") or {}:
            if Path(path).name != MANIFEST_NAME_T or not (E.root / path).is_file():
                continue
            m = json.loads((E.root / path).read_text(encoding="utf-8"))
            if m.get("as_of") is None or iso_ms(m["as_of"]) not in instants:
                out.append(f"ONE-CORRIDOR-MANIFEST {path}: as_of {m.get('as_of')!r} is neither the pin nor the "
                           f"score edge")
            if m.get("substrate") != snap:
                out.append(f"ONE-CORRIDOR-SUBSTRATE {path}: substrate {m.get('substrate')!r} is not the snapshot "
                           f"of Stage D's manifest ({snap})")
            for stem in sorted(m.get("sha") or {}):
                table = (E.root / path).with_name(f"{stem}.parquet")
                third = [x for x in (table_instants(table) if table.is_file() else []) if iso_ms(x) not in instants]
                if third:
                    out.append(f"ONE-CORRIDOR-TABLE {Path(path).parent.as_posix()}/{stem}.parquet: holds a third "
                               f"instant {third[:2]}")
    return out


# ═══════════════════════════════════════════════════════════ F-OFFBUS [L-0.8]
def offbus_ast_findings(name: str, src: str) -> list:
    """A non-fixture TC12 source that writes under exchange/: a write call whose PATH — the receiver of
    write_text / write_bytes / touch, the first argument of to_csv / to_parquet / to_json, either of mkdir /
    makedirs / unlink / a write-mode open, the destination of replace / rename / copy* / move — is built from the
    literal `exchange`, directly or through a NAME assigned from it at module level or inside the same function
    (attribute and subscript targets carry nothing).  Data read FROM the bus and written elsewhere is no finding."""
    tree = ast.parse(src)

    def bus(node, tainted) -> bool:
        return any((isinstance(n, ast.Constant) and isinstance(n.value, str)
                    and (n.value == BUS_T or n.value.startswith(BUS_T + "/")))
                   or (isinstance(n, ast.Name) and n.id in tainted) for n in ast.walk(node))

    def names(target) -> list:
        if isinstance(target, ast.Name):
            return [target.id]
        return [x for t in target.elts for x in names(t)] if isinstance(target, (ast.Tuple, ast.List)) else []

    def taint(nodes, known: frozenset) -> frozenset:
        tainted, grew = set(known), True
        while grew:
            grew = False
            for n in nodes:
                if isinstance(n, (ast.Assign, ast.AnnAssign)) and n.value is not None and bus(n.value, tainted):
                    for t in (n.targets if isinstance(n, ast.Assign) else [n.target]):
                        new = set(names(t)) - tainted
                        tainted |= new
                        grew = grew or bool(new)
        return frozenset(tainted)

    functions = [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda))]
    module = taint([n for n in tree.body], frozenset())
    scope = {}                                      # call node -> the names tainted where it stands
    for n in ast.walk(tree):
        if isinstance(n, ast.Call):
            scope[n] = module
    for f in functions:
        local = taint(list(ast.walk(f)), module)
        for n in ast.walk(f):
            if isinstance(n, ast.Call):
                scope[n] = scope[n] | local
    out = []
    for n, tainted in scope.items():
        attr = n.func.attr if isinstance(n.func, ast.Attribute) else getattr(n.func, "id", None)
        recv = [n.func.value] if isinstance(n.func, ast.Attribute) else []
        modes = [a.value for a in list(n.args) + [k.value for k in n.keywords]
                 if isinstance(a, ast.Constant) and isinstance(a.value, str)]
        if attr in WRITE_RECV_T:
            path = recv
        elif attr in WRITE_PATH_T:
            path = list(n.args[:1])
        elif attr in WRITE_EITHER_T or (attr == "open" and any(WRITE_MODE_RX_T.fullmatch(m) for m in modes)):
            path = recv + list(n.args[:1])
        elif attr in DEST_ATTRS_T:
            path = list(n.args[-1:])
        else:
            path = []
        hit = any(bus(x, tainted) for x in path)
        if hit:
            out.append(f"OFFBUS-WRITE {name}: a `{attr}` call writes under {BUS_T}/")
    return out


def tc12_sources(root: Path) -> list:
    out = sorted(p for p in (root / "scripts").glob("tierc12_*.py") if not p.name.endswith("_fixtures.py"))
    return out + ([root / VALUE_AREA_T] if (root / VALUE_AREA_T).is_file() else [])


def offbus_findings(E: Estate) -> list:
    out = []
    for c in tier_commits(E):
        rid = subject_id(c["subject"])
        for _, path in c["paths"]:
            if path.startswith(BUS_T + "/") and not (rid == STEP_Q_T and path in STEP_Q_PATHS_T):
                out.append(f"OFFBUS-COMMIT {path}: `{c['subject'][:48]}` put a path under {BUS_T}/")
    for rel in (ROWS_T, REPORT_T):
        if (E.root / rel).exists():
            out.append(f"OFFBUS-FILE {rel}: exists before the operator's close act")
    shas = {e["sha256"]: path for rec in E.recs.values() for path, e in (rec.get("artifact_shas") or {}).items()
            if not path.startswith(BUS_T + "/") and e.get("bytes")}
    bus = E.root / BUS_T
    for p in sorted(x for x in bus.rglob("*") if x.is_file()) if bus.is_dir() else []:
        hit = shas.get(sha_b(p.read_bytes()))
        if hit:
            out.append(f"OFFBUS-COPY {p.relative_to(E.root).as_posix()}: carries the bytes of the stage artifact "
                       f"{hit}")
    for p in tc12_sources(E.root):
        out += offbus_ast_findings(p.relative_to(E.root).as_posix(), p.read_text(encoding="utf-8"))
    return out


# ═══════════════════════════════════════════════════════════ F-COMMIT [L-0.9]
def is_tc12_path(path: str) -> bool:
    return path.startswith(T12 + "/") or bool(TC12_SCRIPT_RX_T.fullmatch(path)) or path == VALUE_AREA_T


def commit_findings(E: Estate) -> list:
    out = []
    dirty = E.recs.get(R0_T, {}).get(R0_DIRTY_KEY_T) or []
    for c in E.commits():
        tag = f"`{c['subject'][:48]}`"
        if not c["subject"].startswith(TIER_PREFIX_T):
            out += [f"COMMIT-FOREIGN {path}: touched by {tag}, a commit with another subject"
                    for _, path in c["paths"] if is_tc12_path(path)]
            continue
        rid = subject_id(c["subject"])
        if rid is None:
            out.append(f"COMMIT-ID {tag}: the subject names no record id of RESUME_ORDER_T")
        for _, path in c["paths"]:
            if path in dirty:
                out.append(f"COMMIT-DIRTY {path}: an R0-dirty path, touched by {tag}")
            elif not (is_tc12_path(path) or (rid == STEP_Q_T and path in STEP_Q_PATHS_T)):
                out.append(f"COMMIT-PATH {path}: outside the allow-list, touched by {tag}")
            stem = Path(path).stem
            if path == f"{T12}/progress/{stem}.json" and rid_of(stem) in SUBSTAGES_T and rid_of(stem) != rid:
                out.append(f"COMMIT-CHILD {path}: the record of {rid_of(stem)}, touched by a commit labelled {rid}")
        lines = [x for x in c["body"].split("\n") if x.strip()]
        if not lines or not TRAILER_RX_T.fullmatch(lines[-1]):
            out.append(f"COMMIT-TRAILER {tag}: the body does not end with the attribution trailer")
    if git(E.root, "diff", "--cached", "--quiet")[0] != 0:
        out.append("COMMIT-INDEX: the index is not empty while the suite runs")
    return out


# ═══════════════════════════════════════════════════════════ F-PROGRESS [L-0.9]
def progress_findings(E: Estate) -> list:
    out = []
    for rid, rec in E.recs.items():
        if rec.get("stage") != rid:
            out.append(f"RECORD-STAGE {name_of(rid)}: `stage` reads {rec.get('stage')!r}, not the record's id")
        if rid in PRELAW_KEYS_T:
            if sorted(rec) != sorted(PRELAW_KEYS_T[rid]):
                out.append(f"PRELAW-KEYS {rid}: its keys differ from PRELAW_KEYS_T — "
                           f"{sorted(set(rec) ^ set(PRELAW_KEYS_T[rid]))}")
            continue
        lack = [k for k in RECORD_KEYS_T if k not in rec]
        if lack:
            out.append(f"RECORD-KEYS {rid}: lacks {lack} of the typed key set")
        want = SUBSTAGES_T[rid][0] if rid in SUBSTAGES_T else None
        if "parent" in rec and rec["parent"] != want:
            out.append(f"RECORD-PARENT {rid}: `parent` reads {rec['parent']!r}, not {want!r}")
    out += [f"RECORD-STAGE {name}: a record id in neither ORDER nor SUBSTAGES_T" for name in E.stray]
    merged = halts(lambda: P.render(P.merge(E.root)))
    if isinstance(merged, list):
        return out + merged
    filed = (E.root / PROGRESS_T).read_bytes() if (E.root / PROGRESS_T).is_file() else None
    if filed != merged.encode("utf-8"):
        out.append(f"PROGRESS-BYTES {PROGRESS_T}: not byte-equal to the merger's output re-derived now")
    doc = json.loads(merged)
    pin = (E.recs.get(STEP_Q_T, {}).get("artifact_shas") or {}).get(CONTRACT_T) or {}
    if doc.get("contract_of_record") != {"path": CONTRACT_T, "prefix_bytes": pin.get("bytes"),
                                         "prefix_sha256": pin.get("sha256")}:
        out.append("PROGRESS-CONTRACT: contract_of_record is not exactly {path, prefix_bytes, prefix_sha256} of "
                   "the STEP Q record")
    paste = (E.recs.get(last_naming(E).get(PASTE_T), {}).get("artifact_shas") or {}).get(PASTE_T) or {}
    if doc.get("resume_paste_of_record") != {"path": PASTE_T, "sha256": paste.get("sha256")}:
        out.append("PROGRESS-CONTRACT: resume_paste_of_record is not {path, sha256} of the paste's last record")
    return out


# ═══════════════════════════════════════════════════════════ F-ORDER [L-0.10]
def order_findings(E: Estate) -> list:
    out = []
    data = (tuple(P.ORDER) == ORDER_T, tuple(P.RESUME_ORDER) == RESUME_ORDER_T,
            {k: (v["parent"], v["blocking"], tuple(v["depends_on"])) for k, v in P.SUBSTAGES.items()} == SUBSTAGES_T
            and tuple(P.SUBSTAGES) == tuple(SUBSTAGES_T),
            tuple(P.PARALLEL) == PARALLEL_T and P.PARALLEL_AFTER == PARALLEL_AFTER_T
            and {k: tuple(v) for k, v in P.PARALLEL_DEPENDS.items()} == PARALLEL_DEPENDS_T,
            tuple(P.FIXTURELESS) == FIXTURELESS_T)
    names = ("ORDER", "RESUME_ORDER", "SUBSTAGES", "PARALLEL", "FIXTURELESS")
    out += [f"ORDER-DATA: scripts/tierc12_progress.py {n} differs from the fixture's typed second object"
            for n, ok in zip(names, data) if not ok]
    out += [f"ORDER-ID {name}: a record file whose id is in neither ORDER nor SUBSTAGES_T" for name in E.stray]
    reg = E.first_add(REGISTRY_T)
    for d in BOOK_DIRS_T:                           # T1: the registry before every book
        book = E.first_add(f"{T12}/{d}")
        if book is not None and (reg is None or not E.ancestor(reg, book)):
            out.append(f"ORDER-T1 {T12}/{d}: first filed by `{book['subject'][:48]}`, which is not a proper "
                       f"descendant of the commit that adds REGISTRATIONS.json")
    registry, pin = registry_pins(E)
    leans = entry_of(E.root / LEANS_T)
    want = {"registry_head": (pin or {}).get("head"),
            "registrations_sha256": (entry_of(E.root / REGISTRY_T) or {}).get("sha256"),
            "leans_sha256": (leans or {}).get("sha256")}
    for d in BOOK_DIRS_T:                           # T1: every book manifest carries the three stamps
        base = E.t12 / d
        for m in sorted(base.rglob(MANIFEST_NAME_T)) if base.is_dir() else []:
            rel = m.relative_to(E.root).as_posix()
            if "/_det_" in rel:
                continue
            doc = json.loads(m.read_text(encoding="utf-8"))
            bad = sorted(k for k, v in want.items() if v is None or doc.get(k) != v)
            if bad:
                out.append(f"ORDER-T1-STAMP {rel}: lacks or mis-states {bad}")
    trav = E.first_add(f"{T12}/{TRAVERSE_T}")       # T2: the fitted pin before the books that read it
    for d in RANGE_DIRS_T:
        book = E.first_add(f"{T12}/{d}")
        if book is not None and (trav is None or not E.ancestor(trav, book)):
            out.append(f"ORDER-T2 {T12}/{d}: first filed by `{book['subject'][:48]}`, not after the commit that "
                       f"adds the traverse pin")
    spec, ride = E.first_add(f"{T12}/{BOOK4_SPEC_T}"), E.first_add(f"{T12}/{BOOK4_RIDE_T}")
    if ride is not None and (spec is None or not E.ancestor(spec, ride)):       # T3
        out.append(f"ORDER-T3 {T12}/{BOOK4_RIDE_T}: the fourth book rode before its spec was committed")
    score = E.first_add(f"{T12}/{SCORES_DIR_T}")    # T5: no score before the five books and the three stamps
    if score is not None:
        need = [f"{T12}/regbooks/{r}/STATUS.json" for r in REG_IDS_T] + \
               [f"{T12}/progress/{name_of(c)}" for c in STAMPS_CHILDREN_T]
        late = [n for n in need if E.first_add(n) is None or not E.ancestor(E.first_add(n), score)]
        if late:
            out.append(f"ORDER-T5 {T12}/{SCORES_DIR_T}: first filed by `{score['subject'][:48]}`, not a "
                       f"descendant of the commits adding {late}")
    last = last_naming(E)
    amendments = (E.root / AMENDMENTS_T).read_text(encoding="utf-8") if (E.root / AMENDMENTS_T).is_file() else ""
    for c in tier_commits(E):                       # T6, T7: a rebuilt regbook names its AP; its AM came first
        for status, path in c["paths"]:
            if status != "M" or not REGBOOK_MANIFEST_RX_T.fullmatch(path):
                continue
            new, old = E.blob(c["sha"], path), E.blob(c["sha"] + "^", path)
            if json.loads(new).get("sha") == json.loads(old).get("sha"):
                continue
            notes = json.dumps(E.recs.get(last.get(path), {}).get("notes") or [], ensure_ascii=False)
            if not AP_ID_RX_T.search(notes):
                out.append(f"ORDER-T7 {path}: its content shas changed in `{c['subject'][:48]}` with no AP-n id in "
                           f"its record's notes")
            for am in sorted(set(AM_ID_RX_T.findall(notes))):
                filed = next((x for x in tier_commits(E)
                              if f"## {am} · " in (E.blob(x["sha"], AMENDMENTS_T) or b"").decode("utf-8")), None)
                if f"## {am} · " not in amendments or filed is None or not E.ancestor(filed, c):
                    out.append(f"ORDER-T6 {path}: rebuilt under {am} in `{c['subject'][:48]}`, which is not after "
                               f"the commit that filed {am}")
    seq = [(rid, E.first_add(f"{T12}/progress/{name_of(rid)}")) for rid in RESUME_ORDER_T]
    seq = [(rid, c["i"]) for rid, c in seq if c is not None]
    out += [f"ORDER-RECORDS {b}: its record is first committed before {a}'s, against RESUME_ORDER_T"
            for (a, i), (b, j) in zip(seq, seq[1:]) if j < i]
    for child in NO_POSITION_T:
        c, parent = E.first_add(f"{T12}/progress/{name_of(child)}"), E.first_add(
            f"{T12}/progress/{name_of(SUBSTAGES_T[child][0])}")
        if c is not None and (parent is None or c["i"] < parent["i"]):
            out.append(f"ORDER-RECORDS {child}: its record is committed before its parent's")
    return out


# ═══════════════════════════════════════════════════════════ F-SEAM [the resume paste, RC-1 / RC-2]
def seam_findings(seam_pass: Path, returns: Path, leans: Path) -> list:
    out = []
    doc = json.loads(Path(seam_pass).read_text(encoding="utf-8"))
    conflicts = json.loads(Path(returns).read_text(encoding="utf-8")).get(SEAM_KEY_T)
    text = Path(leans).read_text(encoding="utf-8")
    seams = doc.get("seams") or []
    if len(seams) != N_SEAMS_T or not isinstance(conflicts, list) or len(conflicts) != N_SEAMS_T:
        out.append(f"SEAM-COUNT: SEAM_PASS.json holds {len(seams)} entries and `{SEAM_KEY_T}` "
                   f"{len(conflicts) if isinstance(conflicts, list) else 'no list'}; both must be {N_SEAMS_T}")
    if [s.get("seam_no") for s in seams] != list(range(1, len(seams) + 1)):
        out.append(f"SEAM-KEY: the entries are not keyed 1..{len(seams)} in the order of `{SEAM_KEY_T}`")
    source = doc.get("source") or {}
    if source.get("key") != SEAM_KEY_T or source.get("n") != N_SEAMS_T or \
            source.get("sha256") != sha_b(Path(returns).read_bytes()):
        out.append("SEAM-SOURCE: SEAM_PASS.json `source` does not bind the fix-pass returns on file by sha, key "
                   "and count")
    heads = READING_HEAD_RX_T.findall(text)
    for s in seams:
        if s.get("settled_by") not in SETTLED_BY_T:
            out.append(f"SEAM-SETTLED seam {s.get('seam_no')}: settled_by {s.get('settled_by')!r} is not one of "
                       f"{list(SETTLED_BY_T)}")
        new = sorted(set(READING_ID_RX_T.findall(json.dumps(s, ensure_ascii=False))) - set(heads))
        if new:
            out.append(f"SEAM-READING seam {s.get('seam_no')}: names {new}, not a reading of LEANS.md")
    declared = N_READINGS_RX_T.findall(text)
    if declared != [str(N_READINGS_T)] or doc.get("n_readings_after") != N_READINGS_T:
        out.append(f"SEAM-NREADINGS: the LEANS header reads n_readings {declared} and SEAM_PASS.json "
                   f"n_readings_after {doc.get('n_readings_after')!r}; both must be {N_READINGS_T}")
    if len(heads) != N_READINGS_T or len(set(heads)) != len(heads):
        out.append(f"SEAM-NREADINGS: LEANS.md holds {len(heads)} reading headers ({len(set(heads))} distinct), "
                   f"not {N_READINGS_T}")
    return out


# ═══════════════════════════════════════════════════════════ THE SCRATCH ESTATE (plants only; never the tree of record)
def put(root, rel: str, data) -> str:
    p = Path(root) / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(data if isinstance(data, bytes) else data.encode("utf-8"))
    return rel


def put_json(root, rel: str, doc) -> str:
    return put(root, rel, json.dumps(doc, indent=1, sort_keys=True, ensure_ascii=False) + "\n")


def edit_json(root, rel: str, change) -> None:
    p = Path(root) / rel
    doc = json.loads(p.read_text(encoding="utf-8"))
    change(doc)
    put_json(root, rel, doc)


def flip(root, rel: str, at: int = 0) -> None:
    p = Path(root) / rel
    raw = bytearray(p.read_bytes())
    raw[at] ^= 1
    p.write_bytes(bytes(raw))


def transcript_text(head: list, green: int, not_run: int) -> str:
    return "\n".join(head + ["", f"  {green} GREEN, 0 RED, {not_run} NOT RUN"]) + "\n"


class Scratch:
    """A miniature, lawful TC12 tree with its own repository, built once per run under the temp dir; every plant
    mutates a fresh COPY of it.  No byte of it comes from a book, a tape or a predecessor's record."""

    def __init__(self, tmp: Path):
        self.tmp = Path(tmp).resolve()
        if ROOT in self.tmp.parents or self.tmp == ROOT:
            raise SystemExit("HALT: the scratch estate may not stand inside the tree of record")
        self.snapshots = self.tmp / "snapshots"
        self.n = 0
        self.c = {}
        self._base = None
        self._ctl = {}

    def sgit(self, repo, *args) -> str:
        repo = Path(repo).resolve()
        if self.tmp not in repo.parents:
            raise SystemExit("HALT: a write verb of git may run in the scratch estate only")
        env = {"GIT_AUTHOR_NAME": "Scratch Fixture", "GIT_AUTHOR_EMAIL": "fixture@scratch.invalid",
               "GIT_COMMITTER_NAME": "Scratch Fixture", "GIT_COMMITTER_EMAIL": "fixture@scratch.invalid",
               "GIT_AUTHOR_DATE": SCRATCH_DATE_T, "GIT_COMMITTER_DATE": SCRATCH_DATE_T,
               "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1",
               "GIT_CEILING_DIRECTORIES": str(self.tmp)}
        rc, out = git(repo, *args, ro=False, env=env)
        if rc:
            raise RuntimeError(f"scratch git {args[0]} failed")
        return out.decode("utf-8").strip()

    def commit(self, repo, subject: str, paths: list, body: str = SCRATCH_TRAILER_T) -> str:
        self.sgit(repo, "add", "-A", "--", *paths)
        self.sgit(repo, "commit", "-q", "--no-verify", "-m", f"{subject}\n\n{body}")
        return self.sgit(repo, "rev-parse", "HEAD")

    def estate(self, root, stage: str = SCRATCH_STAGE_T) -> Estate:
        return Estate(root, stage, "HEAD", snapshots=self.snapshots)

    def fresh(self) -> Path:
        self.n += 1
        dst = self.tmp / f"plant_{self.n}"
        shutil.copytree(self.base(), dst, symlinks=True)
        return dst

    def fixture(self, root, transcript: str, total: int, not_run: int) -> dict:
        s = entry_of(Path(root) / transcript)["sha256"]
        return {"suite": "scratch_fixtures.py", "transcript": transcript, "provenance": False, "exit_code": 0,
                "legs_red": 0, "legs_not_run": not_run, "legs_total": total, "transcript_drift": False,
                "transcript_sha_before": s, "transcript_sha_after": s, "wall_seconds": 0.0}

    def record(self, root, rid: str, paths: list, **more) -> str:
        rec = {"stage": rid, "parent": SUBSTAGES_T[rid][0] if rid in SUBSTAGES_T else None, "status": CV,
               "as_of": None, "blockers": [], "depends_on": [],
               "artifact_shas": {p: entry_of(Path(root) / p) for p in paths}, "supersedes": [], "fixtures": [],
               "one_line": "scratch", "notes": []}
        rec.update(more)
        return put_json(root, f"{T12}/progress/{name_of(rid)}", rec)

    def base(self) -> Path:
        if self._base is not None:
            return self._base
        R = self.tmp / "base"
        R.mkdir(parents=True)
        for name in FZ.SNAPSHOTS_T:
            put(self.snapshots, f"{name}/klines/a.bin", "scratch snapshot file\n")
        # the frozen estate in miniature (untracked in the scratch repository, like most of the real one)
        for rel in FZ.FILES_T + FZ.ANALYTICS_PLUS_T:
            put(R, rel, f"scratch estate file {rel}\n")
        put(R, "analytics/profile.py", "ROWS = 0\n")
        put(R, T11 + "/scores/SCORES.json", '{"leaves": 0}\n')
        put_json(R, EDGE_FILE_T, {PIN_ISO_KEY_T: SCRATCH_EDGE_ISO_T, PIN_MS_KEY_T: iso_ms(SCRATCH_EDGE_ISO_T)})
        put(R, "research_outputs/tierc10/close/FIXTURES_X.txt", "scratch\n")
        put(R, "scripts/tierc10_panel.py", "N = 0\n")
        put(R, "scripts/tierc11_score.py", "PIN = 'old'\n")
        dirty = ["exchange/status/daily/DAILY.md", "research_outputs/tierc10/close/FIXTURES_X.txt"]
        put(R, dirty[0], "scratch daily\n")
        self.sgit(R, "init", "-q")
        put(R, "README", "scratch\n")
        self.c["root"] = self.commit(R, "scratch: root", ["README"])
        # STEP Q — the contract (the real prefix bytes and the real STEP Q pin: the one real text in the scratch)
        pin = json.loads((ROOT / T12 / "progress" / name_of(STEP_Q_T)).read_text(encoding="utf-8"))[
            "artifact_shas"][CONTRACT_T]
        put(R, CONTRACT_T, (ROOT / CONTRACT_T).read_bytes()[:pin["bytes"]])
        self.c["step_q"] = self.commit(R, "tierc12(STEP Q): contract filed verbatim", [CONTRACT_T])
        self.sgit(R, "branch", X_REF_T.split("/")[-1], self.c["step_q"])
        # TC12-R0 — the two pre-law records, the rulings, the X manifest, the merger v0
        put(R, T12 + "/.gitignore", "**/*.parquet\n**/_det_*/\nx_rec/**\n!x_rec/\n!x_rec/X_REC_MANIFEST.json\n")
        put(R, RULINGS_T, "# rulings\nO-1\n")
        xa = put(R, FZ.XR + "/tierc11x/a.json", "{}\n")
        xq = FZ.XR + "/queue/2026-09-25_TC11X_APOLLO.md"

        def manifest(paths):
            rows = [dict(entry_of(R / p), copy=p) for p in paths]
            return put_json(R, FZ.X_MANIFEST, {"files": rows, "n_files": len(rows),
                                               "bytes": sum(r["bytes"] for r in rows)})

        manifest([xa])
        put(R, "scripts/tierc12_progress.py", "# the merger, v0\n")
        put_json(R, f"{T12}/progress/{name_of(STEP_Q_T)}",
                 {"stage": STEP_Q_T, "status": CV, "as_of": None, "blockers": [], "commit": self.c["step_q"],
                  "artifact_shas": {CONTRACT_T: pin}, "one_line": "scratch"})
        r0_paths = [RULINGS_T, FZ.X_MANIFEST, T12 + "/.gitignore", "scripts/tierc12_progress.py"]
        put_json(R, f"{T12}/progress/{name_of(R0_T)}",
                 {"stage": R0_T, "status": CV, "as_of": None, "blockers": [],
                  "artifact_shas": {p: entry_of(R / p) for p in r0_paths}, "fixtures": [], "one_line": "scratch",
                  "notes": [], "r0_census_utc": "scratch", "head_at_r0": self.c["step_q"], "r0_census": "scratch",
                  R0_DIRTY_KEY_T: dirty, "operator_ruling_in_session": "scratch", X_TIP_KEY_T: self.c["step_q"],
                  "x_rec": {"n_files": 1, "bytes": entry_of(R / xa)["bytes"]},
                  FZ.R0_KEY: {p: entry_of(R / p) for p in (T11 + "/scores/SCORES.json", "LEDGER.md")}})
        self.c["r0"] = self.commit(R, "tierc12(R0): census", r0_paths + [
            f"{T12}/progress/{name_of(STEP_Q_T)}", f"{T12}/progress/{name_of(R0_T)}"])
        put(R, DISCLOSURES_T, "# disclosures\nD-1\n")
        self.c["r0b"] = self.commit(R, "tierc12(R0): disclosures D-1", [DISCLOSURES_T])
        put(R, PASTE_T, "the resume paste (scratch)\n")
        self.c["paste"] = self.commit(R, "tierc12(STEP Q): resume paste filed verbatim", [PASTE_T])
        # TC12-LEANS — the frozen texts; the rulings, the disclosures and the X manifest re-recorded
        put(R, LEANS_T, "# LEANS (scratch)\n\nn_readings = 2\n\n**L-0.1 A** — a\n\n**L-0.2 B** — b\n")
        put(R, RULINGS_T, "# rulings\nO-1\nO-2\n")
        put(R, DISCLOSURES_T, "# disclosures\nD-1\nD-2\n")
        put(R, AMENDMENTS_T, "# amendments\n\n## AM-1 · 2026-10-09 (~18:10Z) · L-V.9..L-V.15 · contract :32-33 "
                             "(no AP) · AM-V2\n\nbody\n")
        put(R, PROPOSED_T, "# proposed\n\n## AP-1 · 2026-10-09 (~18:10Z) · L-X.36 · filed at the freeze\n\nbody\n")
        put(R, ATTEST_T, json.dumps({"record": "header", "frozen": dict(entry_of(R / LEANS_T), path=LEANS_T)},
                                    sort_keys=True) + "\n")
        manifest([xa, xq])
        leans_paths = [LEANS_T, AMENDMENTS_T, PROPOSED_T, DISCLOSURES_T, RULINGS_T, FZ.X_MANIFEST, ATTEST_T]
        self.record(R, LEANS_REC_T, leans_paths + [PASTE_T], depends_on=[R0_T],
                    x_rec={"n_files": 2, "bytes": sum(entry_of(R / p)["bytes"] for p in (xa, xq))})
        self.c["leans"] = self.commit(R, "tierc12(TC12-LEANS): the readings frozen",
                                      leans_paths + [f"{T12}/progress/{name_of(LEANS_REC_T)}"])
        # TC12-REG — the registry, the census, the merger v1, a transcript
        put_json(R, REGISTRY_T, {"leans": dict(entry_of(R / LEANS_T), path=LEANS_T),
                                 "rulings": dict(entry_of(R / RULINGS_T), path=RULINGS_T),
                                 "disclosures": dict(entry_of(R / DISCLOSURES_T), path=DISCLOSURES_T)})
        put_json(R, REGISTRY_PIN_T, {"head": sha_b(b"scratch head"),
                                     "leans": dict(entry_of(R / LEANS_T), path=LEANS_T)})
        put(R, "scripts/tierc12_progress.py", "# the merger, v1\n")
        census = FZ.write(R, snapshots=self.snapshots).relative_to(R).as_posix()
        pre = [FX.PRE_SUBSTRATE_AS_OF, FX.PRE_SUBSTRATE_LINE]
        t_reg = put(R, f"{T12}/resume/FIXTURES_RESUME_{FIRST_GATE_T}.txt", transcript_text(pre, 3, 0))
        reg_paths = [REGISTRY_T, REGISTRY_PIN_T, census, t_reg, "scripts/tierc12_progress.py"]
        self.record(R, FIRST_GATE_T, reg_paths, depends_on=[LEANS_REC_T], fixtures=[self.fixture(R, t_reg, 3, 0)])
        self.c["reg"] = self.commit(R, "tierc12(TC12-REG): the registry filed",
                                    reg_paths + [f"{T12}/progress/{name_of(FIRST_GATE_T)}"])
        # TC12-REG.ledger-spec — the child; it also names an UNTRACKED path that TC12-D re-records
        spec = put(R, f"{T12}/{BOOK4_SPEC_T}", '{"book": 4}\n')
        ledger = put(R, T12 + "/forward/FORWARD_LEDGER.jsonl", "{}\n{}\n")
        t_spec = put(R, T12 + "/forward/FIXTURES_LEDGER_SPEC.txt", transcript_text(pre, 3, 0))
        demo = put(R, T12 + "/data/untracked_demo.parquet", b"scratch bytes v0, not a table\n")
        child = "TC12-REG.ledger-spec"
        self.record(R, child, [spec, ledger, t_spec, demo], depends_on=[FIRST_GATE_T],
                    fixtures=[self.fixture(R, t_spec, 3, 0)])
        old = entry_of(R / demo)["sha256"]
        self.c["spec"] = self.commit(R, "tierc12(TC12-REG.ledger-spec): the fourth book's spec",
                                     [spec, ledger, t_spec, f"{T12}/progress/{name_of(child)}"])
        # TC12-D — the pin, a manifest, a read set, a post-substrate transcript, the merged ledger
        put_json(R, PIN_FILE_T, {PIN_ISO_KEY_T: SCRATCH_PIN_ISO_T, PIN_MS_KEY_T: iso_ms(SCRATCH_PIN_ISO_T)})
        put_json(R, STAGE_D_MANIFEST_T, {SNAPSHOT_KEY_T: f"/scratch/snapshots/{SCRATCH_SNAP_T}"})
        bm = put_json(R, f"{T12}/data/{MANIFEST_NAME_T}", {"as_of": SCRATCH_PIN_ISO_T, "substrate": SCRATCH_SNAP_T,
                                                           "sha": {}})
        rs = put_json(R, T12 + "/data/READ_SET.json", {READ_SET_CLASS_T: [REGISTRY_T]})
        t_d = put(R, T12 + "/data/FIXTURES_DATA.txt",
                  transcript_text([f"as_of_last_closed_4h: {SCRATCH_PIN_ISO_T}"], 3, 1))
        put(R, demo, b"scratch bytes v1, not a table\n")
        d_paths = [PIN_FILE_T, STAGE_D_MANIFEST_T, bm, rs, t_d]
        self.record(R, FIRST_SUBSTRATE_T, d_paths + [demo], as_of=SCRATCH_PIN_ISO_T, depends_on=[FIRST_GATE_T],
                    supersedes=[{"path": demo, "old_sha256": old, "reason": "scratch: rebuilt under AP-0"}],
                    fixtures=[self.fixture(R, t_d, 4, 1)])
        put(R, PROGRESS_T, P.render(P.merge(R)))
        self.c["d"] = self.commit(R, "tierc12(TC12-D): the substrate",
                                  d_paths + [f"{T12}/progress/{name_of(FIRST_SUBSTRATE_T)}", PROGRESS_T])
        self._base = R
        return R

    def control(self, name: str, detector) -> None:
        """The unmutated scratch estate must be GREEN under a detector, or its plants prove nothing."""
        if name not in self._ctl:
            self._ctl[name] = detector(self.estate(self.base()))
        if self._ctl[name]:
            raise RuntimeError(f"the unmutated scratch estate is not clean under {name}: {self._ctl[name][:2]}")

    def plant(self, detector, mutate, commit=None, stage: str = SCRATCH_STAGE_T):
        """A thunk: a fresh copy, one mutation (and, where given, one more commit), the detector."""
        def thunk():
            R = self.fresh()
            paths = mutate(R)
            if commit is not None:
                self.commit(R, commit[0], paths, *commit[1:])
            return detector(self.estate(R, stage))
        return thunk


def break_leg(S: Scratch, name: str, detector, rows, control_note: str = ""):
    def leg():
        if detector is not None:
            S.control(name, detector)
        ok, why = FX.plants(rows)
        return ok, why + (f" · CONTROL (must stay GREEN): {control_note}" if control_note and not ok else "")
    return leg


def real_leg(thunk, passed):
    def leg():
        found = halts(thunk)
        return (False, show(found)) if found else (True, passed() if callable(passed) else passed)
    return leg


# ═══════════════════════════════════════════════════════════ THE TEN BLOCKS
def leg_contract(E: Estate, S: Scratch):
    def scratch_contract(change):
        def thunk():
            R = S.fresh()
            p = R / CONTRACT_T
            p.write_bytes(change(p.read_bytes()))
            return contract_findings(R)
        return thunk

    def insert_line(raw):
        lines = raw.split(b"\n")
        return b"\n".join(lines[:2] + [b"BUILT: x"] + lines[2:])

    def past_slice():
        R = S.base()
        prefix = PINS.contract_prefix(R / CONTRACT_T, R / T12 / "progress" / name_of(STEP_Q_T))
        return [PINS.cut(prefix["lines"], prefix["n_lines"], prefix["n_lines"] + 1)]

    def control():
        clean = contract_findings(S.base())
        stamped = scratch_contract(lambda raw: raw + b"BUILT: x\n")()
        if clean or stamped:
            raise RuntimeError(f"the control is not GREEN: {clean + stamped}")
        return []

    rows = [
        ("one byte flipped inside the prefix", "CONTRACT-PREFIX",
         scratch_contract(lambda raw: bytes([raw[0] ^ 1]) + raw[1:])),
        ("a line inserted at line 3", "CONTRACT-PREFIX", scratch_contract(insert_line)),
        ("the file cut one byte short of the prefix", "CONTRACT-PREFIX", scratch_contract(lambda raw: raw[:-1])),
        ("a tail line that is not a `BUILT: ` line", "CONTRACT-TAIL",
         scratch_contract(lambda raw: raw + b"NOTE: x\n")),
        ("a reader's slice one line past the prefix", "PIN-SLICE", past_slice),
    ]

    def passed():
        pin = E.recs[STEP_Q_T]["artifact_shas"][CONTRACT_T]
        prefix = PINS.contract_prefix(E.root / CONTRACT_T, E.root / T12 / "progress" / name_of(STEP_Q_T))
        return (f"the first {pin['bytes']} bytes of {CONTRACT_T} hash to the STEP Q sha {pin['sha256']} "
                f"({prefix['n_lines']} lines, read through the pin door's one prefix function); the bytes after "
                f"them are empty or whole `BUILT: ` lines; the slice 1..{prefix['n_lines']} re-reads the prefix "
                f"and a slice one line past it is refused")

    def brk():
        control()
        ok, why = FX.plants(rows)
        return ok, why + ("" if ok else " · CONTROL (stays GREEN): a `BUILT: x` line appended after the prefix "
                                        "leaves every slice and the prefix sha unmoved")

    return ("F-CONTRACT", "the contract of record is its STEP Q PREFIX; a later BUILT line moves nothing [L-0.1]",
            "the file is shorter than N, sha256(first N bytes) differs from the STEP Q sha, the tail holds "
            "anything but whole `BUILT: ` lines, or a slice extends past byte N — planted in scratch copies",
            "the contract on file fails the prefix pin, carries an unlawful tail, or a slice leaves the prefix",
            brk, real_leg(lambda: contract_findings(E.root), passed))


def leg_resume(E: Estate, S: Scratch):
    D, REG, CHILD = FIRST_SUBSTRATE_T, FIRST_GATE_T, "TC12-REG.ledger-spec"
    rec = lambda rid: f"{T12}/progress/{name_of(rid)}"  # noqa: E731

    def rec_edit(rid, change):
        return lambda R: edit_json(R, rec(rid), change)

    def earlier_blob(R):
        edit_json(R, rec(R0_T), lambda d: d["artifact_shas"][RULINGS_T].update(sha256=sha_b(b"another blob")))

    def quarantine(R):
        q = R / f"{QUARANTINE_T}20261009T0000Z" / "registrations"
        q.mkdir(parents=True)
        shutil.move(str(R / REGISTRY_T), str(q / Path(REGISTRY_T).name))
        edit_json(R, rec(REG), lambda d: d.update(status=PARTIAL, blockers=["quarantined (scratch)"]))

    def mirror(R):
        S.record(R, NO_POSITION_T[0], [PIN_FILE_T], status=PARTIAL, depends_on=[D])

    def first_record(path, root=ROOT):
        for rid, r in P.records(root).items():
            if path in (r.get("artifact_shas") or {}):
                return dict(r["artifact_shas"][path], record=rid)
        raise SystemExit("HALT: no record names the path")

    def with_patch(name, value):
        def thunk():
            with patched(P, name, value):
                return resume_findings(S.estate(S.base()))
        return thunk

    swapped = list(RESUME_ORDER_T)
    swapped[-2:] = swapped[:-3:-1]
    plant = lambda mutate: S.plant(resume_findings, mutate)  # noqa: E731
    rows = [
        ("a TAMPERED PARTIAL: one byte flipped in a recorded artifact", "ARTIFACT-MOVED",
         plant(lambda R: flip(R, LEANS_T))),
        ("a recorded artifact deleted", "ARTIFACT-MISSING", plant(lambda R: (R / BOOK4_SPEC_PATH).unlink())),
        ("an earlier record's entry that its blob at its closing commit does not re-hash to", "EARLIER-BLOB",
         plant(earlier_blob)),
        ("an untracked path re-recorded with no supersedes entry", "SUPERSEDES",
         plant(rec_edit(D, lambda d: d.update(supersedes=[])))),
        ("an append-only path whose later version rewrites an earlier byte", "APPEND-PREFIX",
         plant(lambda R: flip(R, RULINGS_T))),
        ("certified() patched to return the FIRST record naming a path", "CERTIFIED",
         with_patch("certified", first_record)),
        ("legs_red set to 1", "FIXTURE-RECORD", plant(rec_edit(D, lambda d: d["fixtures"][0].update(legs_red=1)))),
        ("legs_not_run one less than the transcript's NOT RUN count", "FIXTURE-RECORD",
         plant(rec_edit(D, lambda d: d["fixtures"][0].update(legs_not_run=0)))),
        ("`fixtures` emptied on TC12-D", "FIXTURE-RECORD", plant(rec_edit(D, lambda d: d.update(fixtures=[])))),
        ("a record whose status reads \"COMPLETE\"", "RECORD-STATUS",
         plant(rec_edit(D, lambda d: d.update(status="COMPLETE")))),
        ("a _rerun.txt planted beside a transcript of record", "RERUN-FILE",
         plant(lambda R: put(R, T12 + "/data/FIXTURES_DATA_rerun.txt", "x\n"))),
        ("a dependent record left COMPLETE-VERIFIED over a quarantined depends_on member", "DEPENDS-CLOSURE",
         plant(quarantine)),
        ("a record whose depends_on omits the record certifying a path of its directory's READ_SET.json",
         "DEPENDS-FLOOR", plant(rec_edit(D, lambda d: d.update(depends_on=[])))),
        ("a child whose depends_on omits its SUBSTAGES_T row", "DEPENDS-FLOOR",
         plant(rec_edit(CHILD, lambda d: d.update(depends_on=[])))),
        ("a post-law record lacking a key of the typed set", "RECORD-KEYS",
         plant(rec_edit(D, lambda d: d.pop("supersedes")))),
        ("a COMPLETE-VERIFIED record with a blocker", "BLOCKERS",
         plant(rec_edit(D, lambda d: d.update(blockers=["x"])))),
        ("a quarantine path in a record's artifact_shas", "QUARANTINE-PATH",
         plant(rec_edit(D, lambda d: d["artifact_shas"].update(
             {f"{QUARANTINE_T}20261009T0000Z/data/x.json": {"bytes": 1, "sha256": sha_b(b"x")}})))),
        ("a path of TC12-D.mirror named by another record", "MIRROR-PATH", plant(mirror)),
        ("the record before the gate absent", "GATE-ORDER", plant(lambda R: (R / rec(D)).unlink())),
        ("RESUME_ORDER data with two entries swapped", "RESUME-ORDER", with_patch("RESUME_ORDER", swapped)),
        ("the merger's seed label moved by one", "SEED-LABEL", with_patch("SEED", P.SEED + 1)),
    ]

    def passed():
        _, word = walk(E)
        held = " · ".join(f"{rid} ({len(E.recs[rid].get('artifact_shas') or {})} path(s))" for rid in E.before())
        return (f"{len(E.before())} record(s) stand before {E.stage} in RESUME_ORDER_T, each COMPLETE-VERIFIED "
                f"under the last-record law with git read at --at: {held}; certified() returns, for every "
                f"recorded path, the entry the fixture's own walk finds last; RESUME_ORDER data == the typed copy "
                f"({len(RESUME_ORDER_T)} ids); the merger's seed label == the contract's seed; THE RESUME POINT "
                f"at this gate, derived and never stored: {resume_point(E, word)}")

    return ("F-RESUME", "every record before the gate re-hashes under the last-record law; the resume point is "
            "derived [L-0.3, L-0.4]",
            "a recorded artifact is missing or moved; an earlier entry differs from the blob at its closing "
            "commit or (append-only) is no byte-prefix; an untracked path is re-recorded with no supersedes; "
            "certified() is not the last record; a fixture record, a key set, a status, depends_on or the typed "
            "order is unlawful — each planted in a scratch tree and repository",
            "a record before the gate is absent or not COMPLETE-VERIFIED under L-0.4 (1)-(3), certified() "
            "disagrees with the fixture's walk, RESUME_ORDER data differs from the typed copy, or the seed "
            "label is not the contract's",
            break_leg(S, "F-RESUME", resume_findings, rows), real_leg(lambda: resume_findings(E), passed))


def leg_frozen_text(E: Estate, S: Scratch):
    am = lambda text: (lambda R: put(R, AMENDMENTS_T, (R / AMENDMENTS_T).read_text(encoding="utf-8") + text))  # noqa: E731

    def edit_disclosure(R):
        put(R, DISCLOSURES_T, "# disclosures\nD-1 (edited)\nD-2\n")
        return [DISCLOSURES_T]

    def second_blob(R):
        edit_json(R, REGISTRY_T, lambda d: d.update(note="rewritten"))
        return [REGISTRY_T]

    plant = lambda mutate, commit=None: S.plant(frozen_text_findings, mutate, commit)  # noqa: E731
    rows = [
        ("a one-character edit in a scratch copy of LEANS.md", "FROZEN-BYTES", plant(lambda R: flip(R, LEANS_T))),
        ("an earlier DISCLOSURES entry edited, not appended, in a scratch repository", "APPEND-ONLY",
         plant(edit_disclosure, ("tierc12(TC12-ENV.vendor): a disclosure edited",))),
        ("a line appended to ORCHESTRATOR_RULINGS.md after the scratch registry commit", "FROZEN-BYTES",
         plant(lambda R: put(R, RULINGS_T, (R / RULINGS_T).read_text(encoding="utf-8") + "O-3\n"))),
        ("a heading `## AM-V2 · …` (a nickname in the id's place)", "AM-FORM",
         plant(am("\n## AM-V2 · 2026-10-09 (~18:10Z) · L-V.9 · contract :32-33 (no AP)\n"))),
        ("amendment ids that do not ascend from 1", "AM-FORM",
         plant(am("\n## AM-3 · 2026-10-09 (~18:20Z) · L-0.4 · ruling on AP-1\n"))),
        ("a basis naming an AP that is not on file", "AM-FORM",
         plant(am("\n## AM-2 · 2026-10-09 (~18:20Z) · L-0.4 · ruling on AP-9\n"))),
        ("a write-once file given a second blob in a scratch repository", "WRITE-ONCE",
         plant(second_blob, ("tierc12(TC12-ENV.vendor): the registry rewritten",))),
        ("a registry whose leans pin names another sha", "FROZEN-LEANS",
         plant(lambda R: edit_json(R, REGISTRY_PIN_T, lambda d: d["leans"].update(sha256=sha_b(b"other"))))),
    ]

    def passed():
        grown = sum(1 for c in tier_commits(E) for s, p in c["paths"] if p in APPEND_ONLY_T and s != "A")
        leans = entry_of(E.root / LEANS_T)["sha256"]
        return (f"LEANS.md re-hashes to {leans} — one value with its record and the hash-bound attestation, and "
                f"with the registry's two leans pins from the TC12-REG commit on; every byte-frozen file on "
                f"record re-hashes to the one sha every record names for it; {grown} modification(s) of an "
                f"append-only file by tierc12( commits in range, each a byte-prefix append; no write-once file "
                f"has a second blob; every `## AM-` heading of LEANS_AMENDMENTS.md has the form, the ids ascend "
                f"from 1 and every AP basis is on file")

    return ("F-FROZEN-TEXT", "frozen texts stay frozen; append-only files only grow; amendments are dated and "
            "numbered [L-0.5]",
            "a byte-frozen file differs from its pin; a tierc12( commit's parent blob of an append-only file is "
            "not a byte-prefix of its own; a write-once file has more than one blob in range; an `## AM-` "
            "heading breaks the form, the ids do not ascend from 1 or a basis names an AP not on file; the "
            "LEANS sha is not one value — planted in scratch copies and repositories (the registry filer's own "
            "write-once HALT is F-REG [WRITE-ONCE]'s plant, in the registry suite)",
            "any of those holds on the tree of record at --at",
            break_leg(S, "F-FROZEN-TEXT", frozen_text_findings, rows),
            real_leg(lambda: frozen_text_findings(E), passed))


def leg_frozen(E: Estate, S: Scratch):
    script = "scripts/tierc11_score.py"

    def stamp(applied):
        def mutate(R):
            before = entry_of(R / script)["sha256"]
            put(R, script, "PIN = 'new'\n")
            put_json(R, FZ.STAMP_MAP, {"applied": applied, FZ.STAMP_MAP_ROWS: [
                {"path": script, "sha256_before": before, "sha256_after": entry_of(R / script)["sha256"]}]})
        return mutate

    def control():
        found = S.plant(frozen_findings, stamp(True))()
        if found:
            raise RuntimeError(f"the control is not GREEN: {found[:2]}")

    plant = lambda mutate: S.plant(frozen_findings, mutate)  # noqa: E731
    rows = [
        ("one byte flipped in scores/SCORES.json", f"FROZEN-CHANGED {T11}/scores/SCORES.json",
         plant(lambda R: flip(R, T11 + "/scores/SCORES.json"))),
        ("a _det_x/a.parquet added", f"FROZEN-NEW {T11}/stage_g/_det_x/a.parquet",
         plant(lambda R: put(R, T11 + "/stage_g/_det_x/a.parquet", "x"))),
        ("a __pycache__/a.pyc added", f"FROZEN-NEW {T11}/__pycache__/",
         plant(lambda R: put(R, T11 + "/__pycache__/a.pyc", "x"))),
        ("a SCORES_rerun.json added", f"FROZEN-NEW {T11}/scores/SCORES_rerun.json",
         plant(lambda R: put(R, T11 + "/scores/SCORES_rerun.json", "{}\n"))),
        ("a set-(c) script at its mapped value while the map reads applied: false", f"FROZEN-CHANGED {script}",
         plant(stamp(False))),
        ("a file added to x_rec with no manifest row", f"FROZEN-XREC {FZ.XR}/tierc11x/b.json",
         plant(lambda R: put(R, FZ.XR + "/tierc11x/b.json", "{}\n"))),
        ("a census path deleted", "FROZEN-MISSING LEDGER.md", plant(lambda R: (R / "LEDGER.md").unlink())),
        ("a snapshot gone from its place (its listing moves)", f"FROZEN-SNAPSHOT {FZ.SNAPSHOTS_T[0]}",
         lambda: frozen_findings(Estate(S.base(), SCRATCH_STAGE_T, "HEAD", snapshots=S.tmp / "no_snapshots"))),
        ("the tierc11x ref moved", f"X-TIP {X_REF_T}",
         plant(lambda R: S.sgit(R, "branch", "-f", X_REF_T.split("/")[-1], S.c["r0"]))),
    ]

    def passed():
        first = json.loads(FZ.census_file(E.root).read_text(encoding="utf-8"))
        return (f"the frozen estate is unmoved against its census of record ({FZ.CENSUS_DIR}/{FZ.CENSUS_STEM}.json, "
                f"or the latest census re-pinned beside it): no path missing, none changed outside the one typed "
                f"acceptance, none joined by a sibling; both snapshot listings and x_rec (against its manifest at "
                f"the certified sha) unmoved; {X_REF_T} is the x_tip {R0_T} recorded. The first census holds "
                f"{first['n_files']} files ({first['bytes']} B) under the typed roots, "
                f"{len(first['pycache_dirs'])} __pycache__ directories by name and x_rec's "
                f"{first['x_rec']['n_files']} files")

    def brk():
        S.control("F-FROZEN", frozen_findings)
        control()
        ok, why = FX.plants(rows)
        return ok, why + ("" if ok else " · CONTROL (stays GREEN): the same script at its mapped value while the "
                                        "map reads applied: true")

    return ("F-FROZEN", "TC12 moves no byte of the frozen estate [L-0.6]",
            "a census path is missing, changed outside the one typed acceptance (L-0.24) or joined by a new "
            "sibling under a census root; x_rec or its manifest's certified sha / n_files moved; the tierc11x "
            "ref moved — planted in a scratch copy of the estate, each RED naming the path",
            "the working tree differs from the census of record on any path, sha, snapshot listing or x_rec "
            "row, or refs/heads/tierc11x is not the x_tip recorded at R0",
            brk, real_leg(lambda: frozen_findings(E), passed))


def leg_corridor(E: Estate, S: Scratch):
    bm = f"{T12}/data/{MANIFEST_NAME_T}"
    later = (datetime.fromisoformat(SCRATCH_PIN_ISO_T.replace("Z", "+00:00")) + FOUR_H_T).strftime(
        "%Y-%m-%dT%H:%M:%SZ")

    def third_instant(R):
        import pandas as pd
        pd.DataFrame({AS_OF_COL_T: [SCRATCH_PIN_ISO_T, later]}).to_parquet(R / T12 / "data" / "demo_table.parquet")
        edit_json(R, bm, lambda d: d.update(sha={"demo_table": sha_b(b"scratch")}))

    def pre_pair(R):
        put(R, T12 + "/data/FIXTURES_DATA.txt",
            transcript_text([FX.PRE_SUBSTRATE_AS_OF, FX.PRE_SUBSTRATE_LINE], 3, 1))

    plant = lambda mutate: S.plant(corridor_findings, mutate)  # noqa: E731
    rows = [
        ("a manifest copy with as_of one 4h step later", "ONE-CORRIDOR-MANIFEST",
         plant(lambda R: edit_json(R, bm, lambda d: d.update(as_of=later)))),
        ("a table copy stamped with a third instant", "ONE-CORRIDOR-TABLE", plant(third_instant)),
        ("a manifest copy naming tc11_20260925 as substrate", "ONE-CORRIDOR-SUBSTRATE",
         plant(lambda R: edit_json(R, bm, lambda d: d.update(substrate=FZ.SNAPSHOTS_T[-1])))),
        ("a post-substrate transcript copy headed (pre-substrate stage)", "ONE-CORRIDOR-HEADER", plant(pre_pair)),
        ("a record at TC12-D whose as_of is another instant", "ONE-CORRIDOR-ASOF",
         plant(lambda R: edit_json(R, f"{T12}/progress/{name_of(FIRST_SUBSTRATE_T)}",
                                   lambda d: d.update(as_of=later)))),
        ("a record before TC12-D that carries an as_of", "ONE-CORRIDOR-ASOF",
         plant(lambda R: edit_json(R, f"{T12}/progress/{name_of(FIRST_GATE_T)}",
                                   lambda d: d.update(as_of=SCRATCH_PIN_ISO_T)))),
    ]

    def passed():
        first = RESUME_ORDER_T.index(FIRST_SUBSTRATE_T)
        if RESUME_ORDER_T.index(E.stage) < first:
            return (f"pre-substrate form: every record in scope stands before {FIRST_SUBSTRATE_T} in "
                    f"RESUME_ORDER_T — each carries as_of null and every transcript it records opens with the "
                    f"fixed pair `{FX.PRE_SUBSTRATE_AS_OF}` / `{FX.PRE_SUBSTRATE_LINE}`; no pin record, manifest "
                    f"or table is in scope at this gate")
        pin = json.loads((E.root / PIN_FILE_T).read_text(encoding="utf-8"))[PIN_ISO_KEY_T]
        return (f"one corridor: every record from {FIRST_SUBSTRATE_T} in scope carries as_of {pin}, its "
                f"transcripts open on that line, its manifests name the pin or the score edge and Stage D's "
                f"snapshot, and its tables hold no third instant; the records before {FIRST_SUBSTRATE_T} keep "
                f"the pre-substrate pair")

    return ("F-ONE-CORRIDOR", "one pin, one substrate; the pre-substrate pair before TC12-D and never after "
            "[L-0.7, L-0.10 point 11]",
            "a record's as_of, a transcript's first line or a manifest's as_of names an instant other than the "
            "pin or the score edge; a table holds a third instant; a manifest's substrate is not Stage D's "
            "snapshot; the pre-substrate pair heads a transcript of TC12-D or later — planted in scratch copies",
            "any of those holds for a record in scope; or a record before TC12-D carries an as_of or a "
            "transcript without the fixed pre-substrate pair",
            break_leg(S, "F-ONE-CORRIDOR", corridor_findings, rows), real_leg(lambda: corridor_findings(E), passed))


def leg_offbus(E: Estate, S: Scratch):
    def rows_commit(R):
        return [put(R, ROWS_T + "/a.csv", "a,b\n")]

    def stager(R):
        src = (ROOT / "scripts" / "tierc12_frozen.py").read_text(encoding="utf-8")
        put(R, "scripts/tierc12_ferry.py", src + '\n(ROOT / "exchange" / "rows").mkdir()\n')

    benign = ('ROOT = Path(".")\nCONTRACT = "exchange/queue/c.md"\nOUT = ROOT / "research_outputs" / "tierc12"\n\n\n'
              'def file():\n    text = (ROOT / CONTRACT).read_text()\n    with open(ROOT / CONTRACT, "rb") as f:\n'
              '        raw = f.read()\n    (OUT / "pins").mkdir(exist_ok=True)\n'
              '    (OUT / "pins" / "P.json").write_text(text.replace("exchange/", ""))\n'
              '    (OUT / "pins" / "P.bin").write_bytes(raw)\n')

    def control():
        found = offbus_ast_findings("scripts/tierc12_reader.py", benign)
        if found:
            raise RuntimeError(f"the control is not GREEN: {found[:2]}")

    def brk():
        S.control("F-OFFBUS", offbus_findings)
        control()
        ok, why = FX.plants(rows)
        return ok, why + ("" if ok else " · CONTROL (stays GREEN): a source that READS the contract under "
                                        "exchange/ and writes what it read under research_outputs/tierc12/")

    plant = lambda mutate, commit=None: S.plant(offbus_findings, mutate, commit)  # noqa: E731
    rows = [
        ("a `tierc12(TC12-L)` commit adding exchange/rows/tierc12/a.csv", "OFFBUS-COMMIT",
         plant(rows_commit, ("tierc12(TC12-L): the ferry of record",))),
        ("the draft copied to the report's destination", "OFFBUS-FILE", plant(lambda R: put(R, REPORT_T, "x\n"))),
        ("a stage artifact's bytes copied under exchange/", "OFFBUS-COPY",
         plant(lambda R: put(R, BUS_T + "/drops/LEANS.md", (R / LEANS_T).read_bytes()))),
        ("`(ROOT / \"exchange\" / \"rows\").mkdir()` planted in a copy of a non-fixture TC12 source",
         "OFFBUS-WRITE", plant(stager)),
    ]
    passed = (f"no tierc12( commit in range puts a path under {BUS_T}/ but the two queue texts a STEP Q commit "
              f"files ({CONTRACT_T}; {PASTE_T}, by the resume paste's own STEP Q); neither {ROWS_T} nor the "
              f"report's destination exists; no file under {BUS_T}/ carries a stage artifact's bytes; no "
              f"non-fixture TC12 source on file writes under {BUS_T}/")
    return ("F-OFFBUS", "nothing TC12 writes lands under exchange/ before CLOSE [L-0.8]",
            "a tierc12( commit holds a path under exchange/ other than the queue texts of STEP Q; "
            "exchange/rows/tierc12 or the report's destination exists; a file under exchange/ has the sha of a "
            "stage artifact; a non-fixture TC12 source writes under exchange/ — planted in scratch repositories "
            "and trees",
            "any of those holds on the tree of record at --at",
            brk, real_leg(lambda: offbus_findings(E), passed))


def leg_commit(E: Estate, S: Scratch):
    child = f"{T12}/progress/{name_of('TC12-REG.ledger-spec')}"

    def touch(rel, text="x\n"):
        return lambda R: [put(R, rel, text)]

    def child_record(R):
        edit_json(R, child, lambda d: d.update(one_line="scratch, touched"))
        return [child]

    def staged(R):
        put(R, T12 + "/data/staged.json", "{}\n")
        S.sgit(R, "add", "--", T12 + "/data/staged.json")

    plant = lambda mutate, *commit: S.plant(commit_findings, mutate, commit or None)  # noqa: E731
    rows = [
        ("a `tierc12(TC12-D)` commit touching research_outputs/tierc11/a.txt", "COMMIT-PATH",
         plant(touch(T11 + "/a.txt"), "tierc12(TC12-D): a predecessor's file")),
        ("a subject `tierc11(BUILT-STAMP)` on a TC12 path", "COMMIT-FOREIGN",
         plant(touch(T12 + "/data/a.json"), "tierc11(BUILT-STAMP): a TC12 path")),
        ("a subject whose first token is not a record id", "COMMIT-ID",
         plant(touch(T12 + "/data/a.json"), "tierc12(VENDOR): the referee")),
        ("a child commit labelled with its parent's id while it touches the child's record", "COMMIT-CHILD",
         plant(child_record, "tierc12(TC12-REG): the child's record")),
        ("a body without the attribution trailer", "COMMIT-TRAILER",
         plant(touch(T12 + "/data/a.json"), "tierc12(TC12-D): no trailer", "a body, and nothing else")),
        ("a tierc12( commit touching an R0-dirty path", "COMMIT-DIRTY",
         plant(touch("exchange/status/daily/DAILY.md", "scratch daily, touched\n"),
               "tierc12(TC12-D): the daily file")),
        ("a path left staged while the suite runs", "COMMIT-INDEX", plant(staged)),
    ]

    def passed():
        tier = tier_commits(E)
        ids = " · ".join(subject_id(c["subject"]) for c in tier)
        return (f"{len(tier)} tierc12( commit(s) in range, each naming a record id ({ids}), each inside the "
                f"allow-list ({T12}/**, scripts/tierc12_*.py, {VALUE_AREA_T}; the two queue texts in STEP Q "
                f"commits only), none on an R0-dirty path, each body ending with the trailer; "
                f"{len(E.commits()) - len(tier)} commit(s) with another subject touch no TC12 path; the index "
                f"is empty")

    return ("F-COMMIT", "one writer of history: the subject grammar, the allow-list, the trailer [L-0.9]",
            "a tierc12( commit touches a path outside the allow-list or an R0-dirty path; a commit with another "
            "subject touches a TC12 path; a subject's <ID> is not a record id; a commit touching a child's "
            "record carries another id; a body lacks the trailer; the index is not empty — planted in scratch "
            "repositories",
            "any of those holds on <STEP Q commit>^..<--at>, or the index of the tree of record is not empty",
            break_leg(S, "F-COMMIT", commit_findings, rows), real_leg(lambda: commit_findings(E), passed))


def leg_progress(E: Estate, S: Scratch):
    D = f"{T12}/progress/{name_of(FIRST_SUBSTRATE_T)}"

    def trades(R):
        S.record(R, "TC12-V.trades", [], parent="TC12-R", depends_on=["TC12-V"])

    def full_keys(R):
        edit_json(R, f"{T12}/progress/{name_of(STEP_Q_T)}",
                  lambda d: d.update(parent=None, depends_on=[], supersedes=[], fixtures=[], notes=[]))

    def control():
        R = S.fresh()
        before = P.render(P.merge(R))
        with (R / CONTRACT_T).open("ab") as f:
            f.write(b"BUILT: x\n")
        if P.render(P.merge(R)) != before or progress_findings(S.estate(R)):
            raise RuntimeError("the control is not GREEN: a BUILT line moved the re-derived PROGRESS.json")

    plant = lambda mutate: S.plant(progress_findings, mutate)  # noqa: E731
    rows = [
        ("one key of PROGRESS.json hand-edited", "PROGRESS-BYTES",
         plant(lambda R: put(R, PROGRESS_T, (R / PROGRESS_T).read_text(encoding="utf-8").replace(
             '"tier": "TIER-C12"', '"tier": "TIER-C13"')))),
        ("a record of TC12-V.trades whose parent names another stage", "RECORD-PARENT", plant(trades)),
        ("a post-law record lacking depends_on", "RECORD-KEYS",
         plant(lambda R: edit_json(R, D, lambda d: d.pop("depends_on")))),
        ("STEP_Q.json rewritten to the full key set", "PRELAW-KEYS", plant(full_keys)),
        ("a record whose `stage` is another id", "RECORD-STAGE",
         plant(lambda R: edit_json(R, D, lambda d: d.update(stage="TC12-DATA")))),
        ("a record file TC12-VENDOR.json", "RECORD-STAGE",
         plant(lambda R: put_json(R, f"{T12}/progress/TC12-VENDOR.json", {"stage": "TC12-VENDOR", "status": CV}))),
        ("a record whose status reads \"COMPLETE\" (the merger's HALT is the catch)", "carries status",
         plant(lambda R: edit_json(R, D, lambda d: d.update(status="COMPLETE")))),
    ]

    def passed():
        doc = json.loads((E.root / PROGRESS_T).read_text(encoding="utf-8"))
        c = doc["contract_of_record"]
        return (f"{PROGRESS_T} is byte-equal to the merger's output re-derived now; contract_of_record names "
                f"the prefix ({c['prefix_bytes']} B, {c['prefix_sha256']}) and carries no whole-file sha; "
                f"resume_paste_of_record names {PASTE_T} at the sha its last record certifies; every record's "
                f"`stage` is its id and an ORDER entry or a SUBSTAGES_T child, every `parent` the ORDER entry "
                f"its id extends, every post-law record carries the typed key set, and the two pre-law records "
                f"carry exactly PRELAW_KEYS_T")

    def brk():
        S.control("F-PROGRESS", progress_findings)
        control()
        ok, why = FX.plants(rows)
        return ok, why + ("" if ok else " · CONTROL (stays GREEN): a `BUILT: x` line appended to a scratch "
                                        "contract leaves the re-derived PROGRESS.json byte-equal")

    return ("F-PROGRESS", "PROGRESS.json is the merger's output and nothing else; records carry lawful ids and "
            "keys [L-0.9]",
            "PROGRESS.json is not byte-equal to the merger re-derived; a record's stage is neither an ORDER "
            "entry nor a SUBSTAGES_T id, or its parent is not the ORDER entry its id extends; a post-law record "
            "lacks a typed key; a pre-law record's keys differ from PRELAW_KEYS_T; contract_of_record carries "
            "a whole-file sha — planted in scratch copies; a status \"COMPLETE\" must HALT the merger",
            "any of those holds for PROGRESS.json or a record on file",
            brk, real_leg(lambda: progress_findings(E), passed))


def leg_order(E: Estate, S: Scratch):
    def stamps(R):
        return {"registry_head": json.loads((R / REGISTRY_PIN_T).read_text(encoding="utf-8"))["head"],
                "registrations_sha256": entry_of(R / REGISTRY_T)["sha256"],
                "leans_sha256": entry_of(R / LEANS_T)["sha256"], "sha": {"scored": sha_b(b"v0")}}

    def before_registry():
        R = S.fresh()
        S.sgit(R, "checkout", "-q", "--detach", S.c["leans"])
        bm = put_json(R, f"{T12}/books/{MANIFEST_NAME_T}", {"sha": {}})
        S.commit(R, "tierc12(TC12-C): a book before the registry", [bm])
        return order_findings(S.estate(R))

    def wrong_head(R):
        put_json(R, f"{T12}/books/{MANIFEST_NAME_T}", dict(stamps(R), registry_head=sha_b(b"another head")))

    def two_commits(first, second, subjects):
        def thunk():
            R = S.fresh()
            S.commit(R, subjects[0], first(R))
            S.commit(R, subjects[1], second(R))
            return order_findings(S.estate(R))
        return thunk

    regbook = f"{T12}/regbooks/P-ADM-1/{MANIFEST_NAME_T}"

    def regbook_filed(R):
        bm = put_json(R, regbook, stamps(R))
        return [bm, S.record(R, "TC12-G", [bm], depends_on=list(PARALLEL_DEPENDS_T["TC12-G"]))]

    def regbook_rebuilt(R):
        edit_json(R, regbook, lambda d: d.update(sha={"scored": sha_b(b"v1")}))
        return [regbook]

    def rec_only(rid):
        return lambda R: [S.record(R, rid, [])]

    plant = lambda mutate, commit=None: S.plant(order_findings, mutate, commit)  # noqa: E731
    rows = [
        ("a book manifest committed before the registry", "ORDER-T1 ", before_registry),
        ("a manifest whose registry_head is another hex", "ORDER-T1-STAMP", plant(wrong_head)),
        ("the traverse pin committed after a range-book manifest", "ORDER-T2",
         two_commits(lambda R: [put_json(R, f"{T12}/stage_r/sfp/{MANIFEST_NAME_T}", stamps(R))],
                     lambda R: [put_json(R, f"{T12}/{TRAVERSE_T}", {"by_lens": {}})],
                     ("tierc12(TC12-R.sfp): the range walk", "tierc12(TC12-V): the traverse pins"))),
        ("a regbook manifest changed in a second commit with no AP id", "ORDER-T7",
         two_commits(regbook_filed, regbook_rebuilt,
                     ("tierc12(TC12-G): the regbook", "tierc12(TC12-G): the regbook, rebuilt"))),
        ("progress/TC12-G.json first added before progress/TC12-V.stamps.c.json", "ORDER-RECORDS",
         two_commits(rec_only("TC12-G"), rec_only("TC12-V.stamps.c"),
                     ("tierc12(TC12-G): the record", "tierc12(TC12-V.stamps.c): the record"))),
        ("a record file TC12-VENDOR.json planted", "ORDER-ID",
         plant(lambda R: put_json(R, f"{T12}/progress/TC12-VENDOR.json", {"stage": "TC12-VENDOR", "status": CV}))),
        ("a file under scores/ added before the record of TC12-V.stamps.s", "ORDER-T5",
         plant(lambda R: [put_json(R, f"{T12}/{SCORES_DIR_T}/SCORES.json", {})],
               ("tierc12(TC12-SCORE): the five rows",))),
        ("the fourth book ridden before its spec is committed", "ORDER-T3", lambda: _ride_before_spec(S)),
        ("SUBSTAGES data with one depends_on row changed", "ORDER-DATA",
         lambda: _patched_order(S, "SUBSTAGES", dict(P.SUBSTAGES, **{"TC12-V.trades": {
             "parent": "TC12-V", "blocking": True, "depends_on": ["TC12-C"]}}))),
        ("PARALLEL data with one member dropped", "ORDER-DATA",
         lambda: _patched_order(S, "PARALLEL", list(PARALLEL_T[:-1]))),
    ]

    def passed():
        seq = [(rid, E.first_add(f"{T12}/progress/{name_of(rid)}")) for rid in RESUME_ORDER_T]
        named = " · ".join(rid for rid, c in seq if c is not None)
        reg = E.first_add(REGISTRY_T)
        books = [d for d in BOOK_DIRS_T if E.first_add(f"{T12}/{d}") is not None]
        form = ("pre-registry form: no commit in range adds REGISTRATIONS.json and none files a book directory "
                "(T1, T2, T3, T5, T6 and T7 have no commit to order yet)" if reg is None and not books else
                f"the registry commit `{(reg or {}).get('subject', '')[:40]}` is a proper ancestor of the first "
                f"commit of every book directory in range ({len(books)}); T2, T3, T5, T6 and T7 hold on the "
                f"commits in range")
        return (f"{form}; every book manifest on file carries the registry head, the registry sha and the frozen "
                f"LEANS sha; the records' files are first committed in RESUME_ORDER_T order ({named}); no record "
                f"id on disk is outside ORDER and SUBSTAGES_T; the merger's ORDER, RESUME_ORDER, SUBSTAGES, "
                f"PARALLEL and FIXTURELESS data equal the fixture-typed second objects")

    return ("F-ORDER", "text before result: the registry, the fitted pins and the specs are committed before "
            "what reads them [L-0.10]",
            "an ancestry of T1, T2, T3 or T6 fails; a book manifest lacks or mis-states the registry head, the "
            "registry sha or the LEANS sha; a score is filed before the five books and the three stamps "
            "records (T5); a regbook's content sha changes with no AP id (T7); the records' first commits are "
            "out of RESUME_ORDER_T; a record id is outside ORDER and SUBSTAGES_T; the merger's order data "
            "differs from the typed second object — planted in scratch repositories",
            "any of those holds on the tree of record at --at",
            break_leg(S, "F-ORDER", order_findings, rows), real_leg(lambda: order_findings(E), passed))


def _ride_before_spec(S: Scratch) -> list:
    R = S.fresh()
    S.sgit(R, "checkout", "-q", "--detach", S.c["reg"])
    ride = put_json(R, f"{T12}/{BOOK4_RIDE_T}", {"sha": {}})
    S.commit(R, "tierc12(TC12-L): the fourth book's ride", [ride])
    return order_findings(S.estate(R))


def _patched_order(S: Scratch, name: str, value) -> list:
    with patched(P, name, value):
        return order_findings(S.estate(S.base()))


def leg_seam(E: Estate, S: Scratch):
    real = (E.root / SEAM_PASS_T, E.root / SEAM_RETURNS_T, E.root / LEANS_T)

    def seam_plant(change):
        def thunk():
            S.n += 1
            d = S.tmp / f"seam_{S.n}"
            d.mkdir()
            doc = json.loads(real[0].read_text(encoding="utf-8"))
            change(doc)
            return seam_findings(Path(d / put_json(d, "SEAM_PASS.json", doc)), real[1], real[2])
        return thunk

    def header_plant():
        S.n += 1
        d = S.tmp / f"seam_{S.n}"
        d.mkdir()
        text = real[2].read_text(encoding="utf-8") + "\n**L-0.31 A 252ND READING** — planted\n"
        return seam_findings(real[0], real[1], Path(d / put(d, "LEANS.md", text)))

    def count_plant():
        S.n += 1
        d = S.tmp / f"seam_{S.n}"
        d.mkdir()
        text = real[2].read_text(encoding="utf-8").replace(f"\nn_readings = {N_READINGS_T}\n", "\nn_readings = 252\n")
        return seam_findings(real[0], real[1], Path(d / put(d, "LEANS.md", text)))

    extra = {"seam_no": N_SEAMS_T + 1, "settled_by": SETTLED_BY_T[0], "sections_edited": [], "one_line": "planted"}
    rows = [
        ("a 71st entry", "SEAM-COUNT", seam_plant(lambda d: d["seams"].append(extra))),
        ("a missing entry", "SEAM-COUNT", seam_plant(lambda d: d["seams"].pop(len(d["seams"]) // 2))),
        ("the entries in another order (the key leaves the order of the conflicts)", "SEAM-KEY",
         seam_plant(lambda d: d["seams"].reverse())),
        ("an illegal settled_by", "SEAM-SETTLED", seam_plant(lambda d: d["seams"][0].update(settled_by="operator"))),
        ("an entry naming a reading id that LEANS.md does not hold", "SEAM-READING",
         seam_plant(lambda d: d["seams"][0].update(one_line="settled by the new reading L-0.31"))),
        ("a 252nd reading header", "SEAM-NREADINGS", header_plant),
        ("a header that reads another reading count", "SEAM-NREADINGS", count_plant),
    ]
    passed = (f"review/SEAM_PASS.json holds exactly {N_SEAMS_T} entries keyed 1..{N_SEAMS_T} to the "
              f"`{SEAM_KEY_T}` list of review/FIX_PASS_1_RETURNS.json in order (bound by sha, key and count), "
              f"each settled_by one of {list(SETTLED_BY_T)}, none naming a reading id outside LEANS.md; the LEANS "
              f"header reads `n_readings = {N_READINGS_T}` and the file holds exactly {N_READINGS_T} distinct "
              f"reading headers")
    return ("F-SEAM", "the ONE seam pass: 70 settlements, no new reading [the resume paste, RC-1 / RC-2]",
            "SEAM_PASS.json holds a 71st or a missing entry, an entry out of key order, an illegal settled_by "
            "or a reading id that is not one of LEANS.md's; or LEANS.md's header or header count is any other "
            "reading count — planted in scratch copies",
            f"SEAM_PASS.json is not exactly {N_SEAMS_T} lawful settlements keyed to the residual conflicts in "
            f"order, or LEANS.md does not hold exactly {N_READINGS_T} readings",
            break_leg(S, "F-SEAM", None, rows), real_leg(lambda: seam_findings(*real), passed))


LEGS = (leg_contract, leg_resume, leg_frozen_text, leg_frozen, leg_corridor, leg_offbus, leg_commit, leg_progress,
        leg_order, leg_seam)


# ═══════════════════════════════════════════════════════════ main
def usage(msg: str) -> int:
    print(f"usage error: {msg}")
    print("  tierc12_resume_fixtures.py --stage=<record id> --at=<sha> [--root=DIR] [--refile-transcript]")
    return 2


def main(argv=None) -> int:
    args = sys.argv[1:] if argv is None else list(argv)
    stage, at = FX.opt(args, "--stage="), FX.opt(args, "--at=")
    out_root = Path(FX.opt(args, "--root=", str(ROOT / T12)))
    gated = WALK_T[WALK_T.index(FIRST_GATE_T):]
    if stage not in gated:
        return usage(f"--stage must be a record id from {FIRST_GATE_T} on: {list(gated)}")
    if not at:
        return usage("--at=<the last tierc12( commit before the one being made> is required")
    E = Estate(ROOT, stage, at)
    seed = contract_seed(ROOT)
    substrate = {}
    if stage in NO_POSITION_T or RESUME_ORDER_T.index(stage) >= RESUME_ORDER_T.index(FIRST_SUBSTRATE_T):
        if not ((ROOT / PIN_FILE_T).is_file() and (ROOT / STAGE_D_MANIFEST_T).is_file()):
            raise SystemExit(f"HALT: a gate from {FIRST_SUBSTRATE_T} on needs {PIN_FILE_T} and {STAGE_D_MANIFEST_T} "
                             f"for its header (L-0.7)")
        pin = json.loads((ROOT / PIN_FILE_T).read_text(encoding="utf-8"))
        snap = json.loads((ROOT / STAGE_D_MANIFEST_T).read_text(encoding="utf-8"))[SNAPSHOT_KEY_T]
        substrate = {"substrate": Path(snap).name, "as_of_iso": pin[PIN_ISO_KEY_T], "pin": pin[PIN_MS_KEY_T]}
    typed = [
        f"stage {stage} · at {E.at} · range {E.first}^..{E.at} (the STEP Q commit is read from STEP_Q.json)",
        f"RESUME_ORDER_T ({len(RESUME_ORDER_T)}) {' · '.join(RESUME_ORDER_T)} — no position: {list(NO_POSITION_T)}",
        "SUBSTAGES_T " + " · ".join(f"{c} <- {list(d)}{'' if b else ' NON-BLOCKING'}"
                                    for c, (_, b, d) in SUBSTAGES_T.items()),
        f"PARALLEL_T {list(PARALLEL_T)} after {PARALLEL_AFTER_T}; lists "
        f"{ {k: list(v) for k, v in PARALLEL_DEPENDS_T.items()} }",
        f"FIXTURELESS_T {list(FIXTURELESS_T)} · STATUSES_T {list(STATUSES_T)} · RECORD_KEYS_T {list(RECORD_KEYS_T)}",
        f"FIXTURE_KEYS_T {list(FIXTURE_KEYS_T)}",
        "PRELAW_KEYS_T " + " · ".join(f"{k} {list(v)}" for k, v in PRELAW_KEYS_T.items()),
        f"STEP_Q_PATHS_T {list(STEP_Q_PATHS_T)} · APPEND_ONLY_T {[x[len(T12) + 1:] for x in APPEND_ONLY_T]} · "
        f"WRITE_ONCE_T {[x[len(T12) + 1:] for x in WRITE_ONCE_T]}",
        f"BYTE_FROZEN_T {[x[len(T12) + 1:] for x in BYTE_FROZEN_T]}",
        f"RERECORDED_T { {k: list(v) for k, v in RERECORDED_T.items()} }",
        f"BOOK_DIRS_T {list(BOOK_DIRS_T)} · RANGE_DIRS_T {list(RANGE_DIRS_T)} · REG_IDS_T {list(REG_IDS_T)}",
        f"N_SEAMS_T {N_SEAMS_T} · N_READINGS_T {N_READINGS_T} · SETTLED_BY_T {list(SETTLED_BY_T)}",
    ]
    print(f"  [stdout only] branch {git(ROOT, 'rev-parse', '--abbrev-ref', 'HEAD')[1].decode().strip()} · live "
          f"HEAD {git(ROOT, 'rev-parse', 'HEAD')[1].decode().strip()}")
    for line in P.ledger_lines(P.ledger(ROOT)):     # the LIVE ledger: every record on disk, stdout only
        print(f"  [stdout only] {line}")
    with tempfile.TemporaryDirectory(prefix="tc12_resume_") as tmp:
        S = Scratch(Path(tmp))
        return FX.run_suite(
            args=args, root=out_root / "resume", transcript=f"FIXTURES_RESUME_{stage}.txt",
            banner=f"TIER-C12 RESUME FIXTURES · --stage={stage} — the resume law (L-0.1, L-0.3 … L-0.10) and the "
                   f"resume paste's F-SEAM — break leg first, RED or void",
            seed=seed, fixtures=[leg(E, S) for leg in LEGS], typed=typed, **substrate)


if __name__ == "__main__":
    sys.exit(main())
