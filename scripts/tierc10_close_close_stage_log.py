#!/usr/bin/env python3
"""TIER-C10 · CLOSE · LAW 6 STAGE LOG — the one line per stage the draft is owed.

The contract of record (exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md:23-24):

    6 · after EVERY stage: commit + update research_outputs/tierc10/PROGRESS.json
        {stage, status, artifact shas, as_of, fixtures} + one line to the draft.

The commits and the ledger were kept; the draft's §1 STAGE LOG stopped at the R0
commit f97cded (five lines).  This script owes nothing new to the record: it
REPRINTS what the ledger and the commit record already say, verbatim, in the shape
§1 uses, so the closer can move the lines into the build doc.  It edits NOTHING
it reads.

REPORT-ONLY.  A ledger reprint, not a result.  No registration is scored, no
registration's verdict is consulted (nothing under registrations/ or scores/ is
opened — F-SL-INPUTS blocks it), no bar is read (so tierc10_data.load_asof is not
needed; no klines file is opened at all).  The stage one_lines of B-CORE / B-5M
quote verdict text because PROGRESS.json does; they are reprinted, never computed.

INPUTS (read-only)
  research_outputs/tierc10/PROGRESS.json   stages[] {stage, status, one_line,
                                           fixtures, blockers, notes}
  research_outputs/tierc10/BUILD_DRAFT.md  §1 STAGE LOG and the §R0.2 table
  git (read-only subcommands only: log, show, rev-list, rev-parse)
      `git log --grep='^tierc10' --format='%h %cI %s'`  (pinned to the HEAD
      resolved once at start, so a commit landing mid-run cannot split the view)
      and the committed history of PROGRESS.json (`git log -- <path>`,
      `git show <sha>:<path>`), which is where "which commit filed this line"
      and "which commit moved this stage" are READ from, never typed.

OUTPUTS (research_outputs/tierc10/close/)
  STAGE_LOG.md                  §A one line per PROGRESS stage, §B one line per
                                tierc10 commit after f97cded not already in §1:
                                - **<stage>** · <commit ISO date> · <one_line verbatim> (`<short sha>`)
  R0_ADDENDUM.md                the R0.2 table VERBATIM as history, beside the
                                ledger AS IT STANDS (same renderer), what moved
                                PARTIAL -> COMPLETE-VERIFIED and at which commit,
                                the remaining PARTIALs' blockers verbatim, and the
                                status of every stage in every committed ledger
  FIXTURES_CLOSE_stage_log.txt  this transcript

RULES READ FROM THE RECORD, NOT CHOSEN HERE
  · a STAGE line's commit = the oldest commit from which the stage's current
    one_line has stood VERBATIM in every committed PROGRESS.json through the
    newest.  A one_line that is in no committed ledger prints `uncommitted`.
  · a COMMIT line = the subject, split at `tierc10(<scope>): ` into label and
    text, verbatim; F-SL-VERBATIM re-joins them and demands the subject back.
  · "moved PARTIAL -> COMPLETE-VERIFIED at" = the first committed ledger that
    records COMPLETE-VERIFIED right after a committed PARTIAL record.  The
    "repair window" = the tierc10 commits in (last PARTIAL record, move] —
    printed as the candidates the git log names, NOT attributed.

FIXTURE LEGS (each states FAILS IF and carries sabotage that must go RED; a leg
is GREEN only when its real check is GREEN AND every sabotage is RED)
  F-SL-COVER     FAILS IF any PROGRESS stage, or any tierc10 commit after
                 f97cded, is absent from STAGE_LOG.md (and not already in §1),
                 or appears twice, or a line names a stage/commit the record
                 does not hold, or a bullet is malformed.
                 SABOTAGE: emit from a COPY of PROGRESS.json with one stage
                 removed -> RED; emit with one commit dropped -> RED.
  F-SL-VERBATIM  FAILS IF any stage line's text differs from its PROGRESS
                 one_line by one byte, or names a commit whose committed ledger
                 does not carry that one_line (or is not where it began to
                 stand), or a commit line does not re-join to its git subject,
                 or any line's date is not the %cI of the sha on it.
                 SABOTAGE: emit from a COPY of PROGRESS.json with one word of
                 one one_line edited -> RED; one word of a commit line edited ->
                 RED; a stage line re-attributed to an earlier ledger -> RED.
  F-SL-HISTORY   FAILS IF R0_ADDENDUM.md's §A HISTORY does not carry the R0.2
                 table text of BUILD_DRAFT.md exactly once, byte-for-byte, as
                 whole contiguous lines.
                 SABOTAGE: one cell altered -> RED; emitted from a COPY of the
                 draft with one row deleted -> RED; the table omitted -> RED.
  F-SL-R0SEAL    FAILS IF the R0.2 table does not re-render byte-identically
                 from PROGRESS.json AS COMMITTED AT f97cded (the ledger it
                 claims to print) — i.e. the history is not the history.
                 SABOTAGE: that ledger with one status flipped -> RED; a COPY of
                 the draft with one blocker count bent -> RED.
  F-SL-INPUTS    FAILS IF, while gathering and emitting, the run opens any file
                 under the repo other than PROGRESS.json and BUILD_DRAFT.md
                 (registrations/, scores/, *.scored.json above all), opens
                 anything under ~/.cache/naiad, opens anything for writing,
                 renames/removes/utimes anything, or starts any subprocess but
                 git with a read-only subcommand — or if the hook did not
                 OBSERVE the two declared reads and at least one git call (a
                 blind hook certifies nothing).  The audit hook BLOCKS a
                 violation before it executes, so a planted one never runs.
                 SABOTAGE: a planted open under scores/ -> RED; a planted
                 `git status` -> RED; a planted write-mode open -> RED; a
                 blind hook (nothing observed) -> RED.
  F-DET          FAILS IF STAGE_LOG.md or R0_ADDENDUM.md differ by one byte
                 between the in-process emission, the files on disk, and two
                 emissions in two fresh processes (fresh hash seeds).
                 SABOTAGE: an emission with a clock stamped in -> RED.
  F-SL-READONLY  FAILS IF the bytes (sha256) — or, stricter, the size or the
                 mtime — of PROGRESS.json, FIXTURES_RESUME.txt or BUILD_DRAFT.md
                 change between the start of the run and the end of the last
                 leg.  SABOTAGE on COPIES: one byte appended -> RED; a literal
                 `touch` (mtime only) -> RED; one byte flipped, size kept -> RED.

Run: export NAIAD_CACHE_DIR=/Users/luis/.cache/naiad/snapshots/tc10_20260921 PYTHONDONTWRITEBYTECODE=1
     ~/venvs/naiad/bin/python scripts/tierc10_close_close_stage_log.py
         [--emit-to DIR]   emission only (no legs, no transcript) — F-DET's
                           second and third processes
Exit: 0 every leg GREEN · 1 a leg RED, or HALT.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = Path.home() / ".cache" / "naiad" / "snapshots" / "tc10_20260921"
LIVE_CACHE = Path.home() / ".cache" / "naiad" / "data_cache"
NAIAD_CACHE_ROOT = Path.home() / ".cache" / "naiad"


def assert_substrate() -> Path:
    """THE FROZEN-SUBSTRATE GUARD [HARD LAW 3], restated from tierc10_census.py.
    This script reads no bar, but it runs under the same preamble as every TC10
    script so that it cannot be the one that ran against the live cache.

    HALTS IF: NAIAD_CACHE_DIR is unset, is the live cache, or is anything but
    the TC10 snapshot; or PYTHONDONTWRITEBYTECODE is unset (the hard rule).
    """
    env = os.environ.get("NAIAD_CACHE_DIR", "")
    if not env:
        raise SystemExit("HALT: NAIAD_CACHE_DIR is unset — TC10 reads ONLY the "
                         f"snapshot {SNAPSHOT}")
    got = Path(env).expanduser().resolve()
    if got == LIVE_CACHE.resolve():
        raise SystemExit("HALT: NAIAD_CACHE_DIR is the LIVE cache — READ-NEVER, "
                         "WRITE-NEVER for TC10")
    if got != SNAPSHOT.resolve():
        raise SystemExit(f"HALT: NAIAD_CACHE_DIR={got} is not the TC10 snapshot "
                         f"{SNAPSHOT}")
    if not (got / "klines").is_dir():
        raise SystemExit(f"HALT: snapshot has no klines/ directory: {got}")
    if os.environ.get("PYTHONDONTWRITEBYTECODE", "") != "1":
        raise SystemExit("HALT: PYTHONDONTWRITEBYTECODE=1 is required (TC10 hard rule)")
    return got


assert_substrate()

T10 = ROOT / "research_outputs" / "tierc10"
PROGRESS = T10 / "PROGRESS.json"
DRAFT = T10 / "BUILD_DRAFT.md"
FIX_RESUME = T10 / "FIXTURES_RESUME.txt"
OUT_DIR = T10 / "close"
OUT_LOG_NAME = "STAGE_LOG.md"
OUT_ADD_NAME = "R0_ADDENDUM.md"
OUT_FIX = OUT_DIR / "FIXTURES_CLOSE_stage_log.txt"
WATCHED = (PROGRESS, FIX_RESUME, DRAFT)
ALLOWED_READ = frozenset(os.path.abspath(p) for p in (PROGRESS, DRAFT))

PROGRESS_REL = "research_outputs/tierc10/PROGRESS.json"
DRAFT_REL = "research_outputs/tierc10/BUILD_DRAFT.md"
ANCHOR = "f97cded"            # the R0 ledger commit — §1's last five lines were written here
GIT_LOG_SPEC = ("log", "--grep=^tierc10", "--format=%h %cI %s")   # the spec's command
GIT_READONLY = frozenset({"log", "show", "rev-list", "rev-parse"})
CV, PARTIAL = "COMPLETE-VERIFIED", "PARTIAL"
SUBJECT_RE = re.compile(r"^tierc10(?:\((?P<scope>[^)]*)\))?: (?P<rest>.*)$")
LINE_RE = re.compile(r"^- \*\*(?P<label>.+?)\*\* · (?P<date>\S+) · (?P<text>.*) "
                     r"\(`(?P<sha>[0-9a-f]{7,40}|uncommitted)`\)$")


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


# ─────────────────────────────── the audit hook (F-SL-INPUTS) ───────────────
_AUDIT = {"on": False, "block": True, "violations": []}
_MUTATING = {"os.remove", "os.rename", "os.replace", "os.rmdir", "os.mkdir",
             "os.truncate", "os.utime", "os.chmod", "os.link", "os.symlink",
             "shutil.rmtree", "shutil.move", "shutil.copyfile"}
_WRITE_FLAGS = os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_APPEND | os.O_TRUNC


def _git_subcommand(argv) -> str | None:
    it = iter(argv[1:])
    for tok in it:
        if tok in ("-C", "-c"):
            next(it, None)
            continue
        if tok.startswith("-"):
            continue
        return tok
    return None


def _violation(event, args):
    root = str(ROOT) + os.sep
    cache = str(NAIAD_CACHE_ROOT) + os.sep
    if event == "open":
        path, mode, flags = args
        if isinstance(path, int):
            return None
        if isinstance(path, bytes):
            path = path.decode("utf-8", "replace")
        ap = os.path.abspath(str(path))
        writing = (isinstance(mode, str) and any(c in mode for c in "wax+")) or \
                  (mode is None and isinstance(flags, int) and flags & _WRITE_FLAGS)
        if writing:
            return f"write-mode open of {os.path.basename(ap)}"
        if ap.startswith(cache):
            return f"opened a ~/.cache/naiad path ({os.path.relpath(ap, str(NAIAD_CACHE_ROOT))})"
        if ap.startswith(root) and ap not in ALLOWED_READ:
            return f"opened {os.path.relpath(ap, str(ROOT))}"
        return None
    if event == "subprocess.Popen":
        _exe, argv, _cwd, _env = args
        argv = [argv] if isinstance(argv, (str, bytes)) else list(argv)
        argv = [a.decode() if isinstance(a, bytes) else str(a) for a in argv]
        if not argv or os.path.basename(argv[0]) != "git":
            return f"non-git subprocess {argv[:1]}"
        sub = _git_subcommand(argv)
        if sub not in GIT_READONLY:
            return f"git {sub} is not on the read-only allowlist {sorted(GIT_READONLY)}"
        return None
    if event in _MUTATING:
        return f"{event} during a read-only window"
    return None


def _observe(event, args):
    """Record the ALLOWED events too, so a GREEN cannot come from a blind hook."""
    if event == "open":
        path = args[0]
        if isinstance(path, bytes):
            path = path.decode("utf-8", "replace")
        if isinstance(path, str) and os.path.abspath(path) in ALLOWED_READ:
            _AUDIT["seen_reads"].add(os.path.relpath(os.path.abspath(path), str(ROOT)))
    elif event == "subprocess.Popen":
        argv = args[1]
        argv = [argv] if isinstance(argv, (str, bytes)) else list(argv)
        argv = [a.decode() if isinstance(a, bytes) else str(a) for a in argv]
        _AUDIT["seen_git"].append(_git_subcommand(argv))


def _hook(event, args):
    if not _AUDIT["on"]:
        return
    v = _violation(event, args)
    if v:
        _AUDIT["violations"].append(v)
        if _AUDIT["block"]:
            raise PermissionError(f"F-SL-INPUTS blocked: {v}")
    else:
        _observe(event, args)


sys.addaudithook(_hook)


def audited(fn, *a, **kw):
    """Run fn under the hook (blocking).  Returns (result, violations, error,
    observed) — observed = {"reads": allowed repo reads seen, "git": [subcommands]}."""
    _AUDIT.update(on=True, block=True, violations=[], seen_reads=set(), seen_git=[])
    res, err = None, None
    try:
        res = fn(*a, **kw)
    except PermissionError as e:
        err = str(e)
    finally:
        _AUDIT["on"] = False
    return (res, list(_AUDIT["violations"]), err,
            {"reads": set(_AUDIT["seen_reads"]), "git": list(_AUDIT["seen_git"])})


def check_inputs(violations, observed):
    F = [f"violation: {x}" for x in violations]
    want = {os.path.relpath(p, str(ROOT)) for p in ALLOWED_READ}
    if observed["reads"] != want:
        F.append(f"the hook observed reads {sorted(observed['reads'])}, not the two declared "
                 f"inputs — a blind hook cannot certify anything")
    if not observed["git"]:
        F.append("the hook observed no git call — a blind hook cannot certify anything")
    counts = {}
    for g in observed["git"]:
        counts[g] = counts.get(g, 0) + 1
    return F, (f"observed reads: {', '.join(sorted(observed['reads']))}; git calls: "
               + ", ".join(f"{k}x{counts[k]}" for k in sorted(counts)) + " — 0 violations")


# ─────────────────────────────── gather (read-only) ─────────────────────────
def git(*args) -> str:
    cmd = ["git", "-C", str(ROOT), "--no-pager", "-c", "color.ui=never",
           "-c", "log.showSignature=false", *args]
    env = dict(os.environ, GIT_OPTIONAL_LOCKS="0")
    r = subprocess.run(cmd, capture_output=True, env=env)
    if r.returncode:
        raise SystemExit(f"HALT: git {args[0]} failed: "
                         f"{r.stderr.decode('utf-8', 'replace').strip()}")
    return r.stdout.decode("utf-8")


def read_git() -> dict:
    head = git("rev-parse", "HEAD").strip()
    anchor_full = git("rev-parse", "--verify", ANCHOR + "^{commit}").strip()
    order = git("rev-list", "--reverse", "--topo-order", head).split()
    pos = {H: i for i, H in enumerate(order)}
    after = set(git("rev-list", f"{anchor_full}..{head}").split())

    tierc10 = []                                   # newest first, as git prints
    for line in git(*GIT_LOG_SPEC, head).splitlines():
        h, ciso, subject = line.split(" ", 2)
        full = [H for H in order if H.startswith(h)]
        if len(full) != 1:
            raise SystemExit(f"HALT: short sha {h} resolves to {len(full)} commits")
        tierc10.append({"h": h, "H": full[0], "ciso": ciso, "subject": subject})
    if not any(c["H"] == anchor_full for c in tierc10):
        raise SystemExit(f"HALT: the anchor {ANCHOR} is not in the tierc10 log")

    hist = []                                      # oldest first
    for line in reversed(git("log", "--format=%h %H %cI", head, "--", PROGRESS_REL).splitlines()):
        h, H, ciso = line.split(" ")
        hist.append({"h": h, "H": H, "ciso": ciso,
                     "ledger": json.loads(git("show", f"{H}:{PROGRESS_REL}"))})
    draft_last = git("log", "-1", "--format=%h %cI", head, "--", DRAFT_REL).strip()
    return {"head": head, "anchor_full": anchor_full, "pos": pos, "after": after,
            "tierc10": tierc10, "hist": hist,
            "head_progress": git("show", f"{head}:{PROGRESS_REL}"),
            "head_draft": git("show", f"{head}:{DRAFT_REL}"),
            "draft_last": draft_last}


# ─────────────────────────────── pure model ─────────────────────────────────
def extract_section1(draft: str) -> str:
    lines = draft.split("\n")
    i = next((k for k, l in enumerate(lines) if l.startswith("## 1 · STAGE LOG")), None)
    if i is None:
        raise SystemExit("HALT: BUILD_DRAFT.md has no '## 1 · STAGE LOG' section")
    j = next((k for k in range(i + 1, len(lines)) if lines[k].startswith("## ")), len(lines))
    return "\n".join(lines[i:j])


def extract_r02_table(draft: str):
    """The first contiguous run of '|' lines under '### R0.2'.  Returns
    (table_text, first_line_no, last_line_no) — line numbers 1-indexed."""
    lines = draft.split("\n")
    i = next((k for k, l in enumerate(lines) if l.startswith("### R0.2")), None)
    if i is None:
        raise SystemExit("HALT: BUILD_DRAFT.md has no '### R0.2' section")
    j = next((k for k in range(i + 1, len(lines))
              if lines[k].startswith("### ") or lines[k].startswith("## ")), len(lines))
    s = next((k for k in range(i + 1, j) if lines[k].startswith("|")), None)
    if s is None:
        raise SystemExit("HALT: §R0.2 carries no table")
    e = s
    while e < j and lines[e].startswith("|"):
        e += 1
    return "\n".join(lines[s:e]), s + 1, e


def render_ledger_table(stages) -> str:
    """The renderer the R0.2 table was printed with (F-SL-R0SEAL proves it
    re-renders that table byte-for-byte from the f97cded ledger)."""
    out = ["| stage | status | artifacts re-hashed | fixtures, re-run NOW | blockers |",
           "|---|---|---|---|---|"]
    for s in stages:
        fx = "; ".join(
            f"`{f.get('suite')}` exit {f.get('exit_code')}, {f.get('legs_red')} red, "
            f"{'drift' if f.get('transcript_drift') else 'no drift'}"
            for f in s.get("fixtures", []))
        out.append(f"| {s['stage']} | **{s['status']}** | {s.get('artifact_count')} | "
                   f"{fx} | {len(s.get('blockers', []))} |")
    return "\n".join(out)


def _stage(ledger, name):
    return next((s for s in ledger.get("stages", []) if s.get("stage") == name), None)


def standing_since(name, one_line, hist):
    since = None
    for rec in reversed(hist):
        st = _stage(rec["ledger"], name)
        if st is not None and st.get("one_line") == one_line:
            since = rec
        else:
            break
    return since


def split_subject(subject: str):
    m = SUBJECT_RE.match(subject)
    if not m:
        return "(subject)", subject
    return (m.group("scope") if m.group("scope") is not None else "tierc10"), m.group("rest")


def join_subject(label: str, text: str) -> str:
    if label == "(subject)":
        return text
    if label == "tierc10":
        return f"tierc10: {text}"
    return f"tierc10({label}): {text}"


def _in_sec1(h: str, sec1: str) -> bool:
    return re.search(r"(?<![0-9a-f])" + re.escape(h) + r"(?![0-9a-f])", sec1) is not None


def _stage_in_sec1(name: str, one_line: str, sec1: str) -> bool:
    for ln in sec1.split("\n"):
        if ln.startswith(f"- **{name}** · ") and one_line in ln:
            return True
    return False


def selection(progress: dict, draft: str, facts: dict) -> dict:
    """What the log must hold: shared by the emitter and the checks (the checks
    then judge the EMITTED TEXT against the raw inputs, not this selection)."""
    sec1 = extract_section1(draft)
    stages = [s for s in progress["stages"] if not _stage_in_sec1(s["stage"], s["one_line"], sec1)]
    after = [c for c in facts["tierc10"] if c["H"] in facts["after"]]
    commits = [c for c in after if not _in_sec1(c["h"], sec1)]
    return {"sec1": sec1, "stages": stages, "after": after, "commits": commits,
            "sec1_stage_skips": [s["stage"] for s in progress["stages"] if s not in stages],
            "sec1_commit_skips": [c["h"] for c in after if c not in commits]}


def status_path(name, hist):
    """[(rec, status|None, one_line)] oldest first."""
    out = []
    for rec in hist:
        st = _stage(rec["ledger"], name)
        out.append((rec, st.get("status") if st else None, st.get("one_line") if st else None))
    return out


def transitions(name, now_status, hist, facts):
    path = status_path(name, hist)
    present = [(r, s) for r, s, _ in path if s is not None]
    born = present[0] if present else None
    moves = []
    prev = None
    for r, s in present:
        if prev is not None and s != prev[1]:
            moves.append((prev[0], prev[1], r, s))
        prev = (r, s)
    flip = None
    for m in moves:
        if m[1] == PARTIAL and m[3] == CV:
            flip = m
    window = []
    if flip:
        lo, hi = facts["pos"][flip[0]["H"]], facts["pos"][flip[2]["H"]]
        window = sorted((c for c in facts["tierc10"] if lo < facts["pos"][c["H"]] <= hi),
                        key=lambda c: facts["pos"][c["H"]])
    newest = present[-1][1] if present else None
    return {"born": born, "moves": moves, "flip": flip, "window": window,
            "committed_now": newest, "uncommitted_change": newest != now_status}


def model(progress_bytes: bytes, draft_bytes: bytes, facts: dict) -> dict:
    progress = json.loads(progress_bytes.decode("utf-8"))
    draft = draft_bytes.decode("utf-8")
    sel = selection(progress, draft, facts)
    stage_lines = []
    for s in sel["stages"]:
        since = standing_since(s["stage"], s["one_line"], facts["hist"])
        if since is None:
            stage_lines.append((s["stage"], "uncommitted", s["one_line"], "uncommitted"))
        else:
            stage_lines.append((s["stage"], since["ciso"], s["one_line"], since["h"]))
    commit_lines = []
    for c in reversed(sel["commits"]):                          # oldest first
        label, text = split_subject(c["subject"])
        commit_lines.append((label, c["ciso"], text, c["h"]))
    r02, r02_a, r02_b = extract_r02_table(draft)
    r02_status = {}
    for ln in r02.split("\n")[2:]:
        cells = [x.strip() for x in ln.strip("|").split("|")]
        r02_status[cells[0]] = cells[1].strip("*")
    return {"progress": progress, "draft": draft, "sel": sel, "facts": facts,
            "progress_sha": sha256(progress_bytes), "draft_sha": sha256(draft_bytes),
            "stage_lines": stage_lines, "commit_lines": commit_lines,
            "r02": r02, "r02_lines": (r02_a, r02_b), "r02_status": r02_status,
            "sec1_bullets": sum(1 for l in sel["sec1"].split("\n") if l.startswith("- **"))}


# ─────────────────────────────── renderers ──────────────────────────────────
def _fmt_line(label, date, text, h):
    return f"- **{label}** · {date} · {text} (`{h}`)"


def render_stage_log(m: dict) -> str:
    f, sel = m["facts"], m["sel"]
    n_tc = len(f["tierc10"])
    L = [
        "# TIER-C10 · §1 STAGE LOG — the lines LAW 6 owed the draft",
        "",
        "> **REPORT-ONLY.** A ledger reprint, not a result: no registration is scored, no",
        "> verdict file is opened, no bar is read. These are append-ready lines for",
        "> `research_outputs/tierc10/BUILD_DRAFT.md` §1 (LAW 6: \"after EVERY stage: commit + update",
        "> … PROGRESS.json … + one line to the draft\"). The script that printed them does not edit",
        "> the draft; they move into §1 at CLOSE.",
        "",
        f"- **Inputs (read-only):** `research_outputs/tierc10/PROGRESS.json` sha256 `{m['progress_sha']}`"
        f" ({len(m['progress']['stages'])} stages) · `research_outputs/tierc10/BUILD_DRAFT.md` sha256"
        f" `{m['draft_sha']}` (§1 holds {m['sec1_bullets']} lines) ·"
        f" `git log --grep='^tierc10' --format='%h %cI %s'` ({n_tc} commits; {len(sel['after'])} after"
        f" `{ANCHOR}`, {len(sel['sec1_commit_skips'])} of them already in §1).",
        "- **A stage line's commit** is the oldest commit from which the stage's `one_line` has"
        " stood VERBATIM in every committed `PROGRESS.json` through the newest (a text filed"
        " earlier, replaced, then restored counts from its restoration; `R0_ADDENDUM.md` §E shows"
        " every committed ledger). `uncommitted` = the line is in no committed ledger.",
        "- **A commit line** is the commit's subject verbatim, split at `tierc10(<scope>): ` into"
        " label and text.",
        "- **Format:** `` - **<stage>** · <commit ISO date> · <one_line verbatim> (`<short sha>`) ``.",
        "",
        f"## A · The ledger — one line per PROGRESS.json stage ({len(m['stage_lines'])}), in ledger order",
        "",
        "*REPORT-ONLY — the ledger's own words.*"
        + (f" Already in §1, not repeated: {', '.join(sel['sec1_stage_skips'])}."
           if sel["sec1_stage_skips"] else ""),
        "",
    ]
    L += [_fmt_line(*x) for x in m["stage_lines"]]
    L += [
        "",
        f"## B · The commit record — one line per tierc10 commit after `{ANCHOR}` not already in"
        f" §1 ({len(m['commit_lines'])}), oldest first",
        "",
        "*REPORT-ONLY — the commit record's own words.*"
        + (f" Already in §1, not repeated: {', '.join('`' + h + '`' for h in sel['sec1_commit_skips'])}."
           if sel["sec1_commit_skips"] else ""),
        "",
    ]
    L += [_fmt_line(*x) for x in m["commit_lines"]]
    return "\n".join(L) + "\n"


def _abbr(status):
    return {CV: "CV", PARTIAL: "P", None: "·"}.get(status, status)


def render_addendum(m: dict) -> str:
    f, prog = m["facts"], m["progress"]
    stages = prog["stages"]
    a, b = m["r02_lines"]
    anchor_rec = next((r for r in f["hist"] if r["H"] == f["anchor_full"]), None)
    now_cv = sum(1 for s in stages if s["status"] == CV)
    now_p = sum(1 for s in stages if s["status"] == PARTIAL)
    r02_cv = sum(1 for v in m["r02_status"].values() if v == CV)
    r02_p = sum(1 for v in m["r02_status"].values() if v == PARTIAL)
    wt_eq_head = m["progress_sha"] == sha256(f["head_progress"].encode("utf-8"))
    L = [
        "# R0 ADDENDUM — the R0.2 ledger as filed, beside the ledger as it stands",
        "",
        "> **REPORT-ONLY.** A ledger, not a result: no registration is scored, no verdict file",
        "> is opened, no bar is read. For `BUILD_DRAFT.md` §R0 at CLOSE; the draft itself is not",
        "> edited. Every status, count, commit and blocker below is read from `PROGRESS.json`, its",
        "> committed history, or the git log — none is typed.",
        "",
        f"- **PROGRESS.json** sha256 `{m['progress_sha']}` — {len(stages)} stages;"
        f" working tree == its newest committed blob: **{wt_eq_head}**.",
        f"- **BUILD_DRAFT.md** sha256 `{m['draft_sha']}` — last changed at"
        f" `{f['draft_last'].split(' ')[0]}`.",
        f"- **Committed ledgers read:** {len(f['hist'])} (`git log -- {PROGRESS_REL}`),"
        f" oldest `{f['hist'][0]['h']}`, newest `{f['hist'][-1]['h']}`.",
        "",
        "## A · HISTORY — the R0.2 table as filed, verbatim",
        "",
        f"*REPORT-ONLY · HISTORY, NOT CURRENT.* Copied byte-for-byte from `BUILD_DRAFT.md`"
        f" §R0.2, lines {a}–{b}. It re-renders byte-identically from `PROGRESS.json` as"
        f" committed at `{anchor_rec['h'] if anchor_rec else ANCHOR}` (F-SL-R0SEAL): at R0.2,"
        f" {r02_cv} COMPLETE-VERIFIED and {r02_p} PARTIAL of {len(m['r02_status'])} stages.",
        "",
        m["r02"],
        "",
        f"## B · AS IT STANDS — the same renderer over PROGRESS.json now ({len(stages)} stages)",
        "",
        f"*REPORT-ONLY · the ledger as it stands.* The five columns of §A, printed by the same"
        f" renderer, so each row reads beside its R0.2 row. The fixtures column lists every"
        f" fixture record the ledger holds for the stage. Now: {now_cv} COMPLETE-VERIFIED,"
        f" {now_p} PARTIAL.",
        "",
        render_ledger_table(stages),
        "",
        "## C · WHAT MOVED — status at R0.2 beside status now",
        "",
        "*REPORT-ONLY.* **moved at** = the first committed ledger that records"
        " COMPLETE-VERIFIED right after a committed PARTIAL record (the ledger commit that moved"
        " the stage). **repair window** = the tierc10 commits in (last PARTIAL record, move] —"
        " the candidates the git log names, NOT an attribution. **born** = the first committed"
        " ledger that holds the stage.",
        "",
        "| stage | at R0.2 | now | born | moved PARTIAL → COMPLETE-VERIFIED at | repair window | blockers now |",
        "|---|---|---|---|---|---|---|",
    ]
    moved = []
    for s in stages:
        t = transitions(s["stage"], s["status"], f["hist"], f)
        at = m["r02_status"].get(s["stage"])
        at_txt = f"**{at}**" if at else "— (not in R0.2)"
        born = (f"{t['born'][1]} at `{t['born'][0]['h']}`" if t["born"] else "uncommitted")
        if t["flip"]:
            fl = t["flip"]
            moved_txt = (f"`{fl[2]['h']}` · {fl[2]['ciso']} (last PARTIAL record"
                         f" `{fl[0]['h']}`)")
            win = f"{len(t['window'])}: " + " ".join(f"`{c['h']}`" for c in t["window"])
            moved.append(s["stage"])
        elif s["status"] == CV:
            moved_txt, win = "— never PARTIAL in a committed ledger", "—"
        else:
            moved_txt, win = f"— still {s['status']}", "—"
        if t["uncommitted_change"]:
            moved_txt += f" · working tree says {s['status']}, newest commit says {t['committed_now']}"
        L.append(f"| {s['stage']} | {at_txt} | **{s['status']}** | {born} | {moved_txt} | {win} |"
                 f" {len(s.get('blockers', []))} |")
    L += [
        "",
        f"Moved PARTIAL → COMPLETE-VERIFIED since R0: {len(moved)}"
        + (f" ({', '.join(moved)})." if moved else "."),
        "",
        "## D · THE REMAINING PARTIALS — blockers verbatim",
        "",
        "*REPORT-ONLY.* Each blocker is `PROGRESS.json`'s string, byte-for-byte, one bullet each,"
        " in the ledger's order; nothing is summarised, merged or dropped.",
        "",
    ]
    partials = [s for s in stages if s["status"] != CV]
    if not partials:
        L += ["No stage is PARTIAL.", ""]
    for s in partials:
        bl = s.get("blockers", [])
        L += [f"### {s['stage']} — {s['status']} · {len(bl)} blocker{'s' if len(bl) != 1 else ''}", ""]
        L += [f"- {x}" for x in bl] or ["- (the ledger records no blocker)"]
        notes = s.get("notes") or []
        L += ["", f"Notes in the ledger: {len(notes)}."]
        L += [f"- {x}" for x in notes]
        L += [""]
    cols = f["hist"]
    L += [
        "## E · STATUS IN EVERY COMMITTED LEDGER",
        "",
        "*REPORT-ONLY.* One column per commit that touched `PROGRESS.json`, oldest first, then"
        " the working tree. CV = COMPLETE-VERIFIED · P = PARTIAL · `·` = the stage is not in that"
        " ledger · ≡ = that ledger carries today's `one_line` verbatim.",
        "",
        "| stage | " + " | ".join(f"`{r['h']}`" for r in cols) + " | now |",
        "|---|" + "---|" * (len(cols) + 1),
    ]
    names = [s["stage"] for s in stages]
    for r in cols:
        for st in r["ledger"].get("stages", []):
            if st["stage"] not in names:
                names.append(st["stage"])
    now = {s["stage"]: s for s in stages}
    for n in names:
        cur = now.get(n)
        cells = []
        for r in cols:
            st = _stage(r["ledger"], n)
            c = _abbr(st.get("status") if st else None)
            if st and cur and st.get("one_line") == cur["one_line"]:
                c += " ≡"
            cells.append(c)
        cells.append(_abbr(cur["status"]) if cur else "·")
        L.append(f"| {n} | " + " | ".join(cells) + " |")
    return "\n".join(L) + "\n"


def emit(progress_bytes: bytes, draft_bytes: bytes, facts: dict) -> dict:
    m = model(progress_bytes, draft_bytes, facts)
    return {OUT_LOG_NAME: render_stage_log(m).encode("utf-8"),
            OUT_ADD_NAME: render_addendum(m).encode("utf-8")}


def gather_and_emit(progress_path=PROGRESS, draft_path=DRAFT, facts=None):
    pb, db = progress_path.read_bytes(), draft_path.read_bytes()
    facts = facts if facts is not None else read_git()
    return pb, db, facts, emit(pb, db, facts)


# ─────────────────────────────── checks (return findings) ───────────────────
def parse_log(text: str) -> dict:
    secs, cur = {"A": [], "B": []}, None
    for ln in text.split("\n"):
        if ln.startswith("## A · "):
            cur = "A"
            continue
        if ln.startswith("## B · "):
            cur = "B"
            continue
        if ln.startswith("## "):
            cur = None
            continue
        if cur and ln.startswith("- "):
            mm = LINE_RE.match(ln)
            secs[cur].append(mm.groupdict() if mm else {"malformed": ln[:80]})
    return secs


def check_cover(log_text: str, ref_progress: dict, ref_draft: str, facts: dict):
    sel = selection(ref_progress, ref_draft, facts)
    secs = parse_log(log_text)
    F = []
    for k in ("A", "B"):
        F += [f"§{k} malformed bullet: {x['malformed']!r}" for x in secs[k] if "malformed" in x]
    labels = [x["label"] for x in secs["A"] if "label" in x]
    want = [s["stage"] for s in sel["stages"]]
    for n in want:
        c = labels.count(n)
        if c == 0:
            F.append(f"stage ABSENT: {n}")
        elif c > 1:
            F.append(f"stage printed {c}x: {n}")
    F += [f"stage line for a stage the ledger does not hold: {n}"
          for n in labels if n not in [s["stage"] for s in ref_progress["stages"]]]
    shas = [x["sha"] for x in secs["B"] if "sha" in x]
    wantc = [c["h"] for c in sel["commits"]]
    for h in wantc:
        c = shas.count(h)
        if c == 0:
            F.append(f"commit ABSENT: {h}")
        elif c > 1:
            F.append(f"commit printed {c}x: {h}")
    F += [f"commit line for a commit not in (after {ANCHOR}, not in §1): {h}"
          for h in shas if h not in wantc]
    return F, f"{len(want)}/{len(want)} stages, {len(wantc)}/{len(wantc)} commits"


def check_verbatim(log_text: str, ref_progress: dict, facts: dict):
    secs = parse_log(log_text)
    by_stage = {s["stage"]: s for s in ref_progress["stages"]}
    by_h = {c["h"]: c for c in facts["tierc10"]}
    hist = facts["hist"]
    hidx = {r["h"]: i for i, r in enumerate(hist)}
    F = []
    for x in secs["A"]:
        if "label" not in x or x["label"] not in by_stage:
            continue
        ol = by_stage[x["label"]]["one_line"]
        if x["text"] != ol:
            k = next((i for i, (p, q) in enumerate(zip(x["text"], ol)) if p != q),
                     min(len(x["text"]), len(ol)))
            F.append(f"one_line differs from PROGRESS: {x['label']} (first difference at char {k})")
        if x["sha"] == "uncommitted":
            F.append(f"LAW 6: {x['label']}'s one_line is in no committed ledger")
            continue
        if x["sha"] not in hidx:
            F.append(f"{x['label']} names {x['sha']}, which is not a commit of PROGRESS.json")
            continue
        i = hidx[x["sha"]]
        for r in hist[i:]:
            st = _stage(r["ledger"], x["label"])
            if st is None or st.get("one_line") != ol:
                F.append(f"{x['label']}: ledger {r['h']} (on/after {x['sha']}) does not carry the one_line")
                break
        if i > 0:
            st = _stage(hist[i - 1]["ledger"], x["label"])
            if st is not None and st.get("one_line") == ol:
                F.append(f"{x['label']}: the one_line already stood at {hist[i - 1]['h']}, before {x['sha']}")
        if x["date"] != hist[i]["ciso"]:
            F.append(f"{x['label']}: date {x['date']} is not {x['sha']}'s %cI {hist[i]['ciso']}")
    for x in secs["B"]:
        if "sha" not in x or x["sha"] not in by_h:
            continue
        c = by_h[x["sha"]]
        if join_subject(x["label"], x["text"]) != c["subject"]:
            F.append(f"commit line {x['sha']} does not re-join to its git subject")
        if x["date"] != c["ciso"]:
            F.append(f"commit line {x['sha']}: date {x['date']} is not its %cI {c['ciso']}")
    return F, f"{len(secs['A'])} stage lines and {len(secs['B'])} commit lines byte-equal to the record"


def _section(text: str, start: str, stop_prefix: str = "## ") -> str | None:
    lines = text.split("\n")
    i = next((k for k, l in enumerate(lines) if l.startswith(start)), None)
    if i is None:
        return None
    j = next((k for k in range(i + 1, len(lines)) if lines[k].startswith(stop_prefix)), len(lines))
    return "\n".join(lines[i:j])


def check_history(add_text: str, ref_draft: str):
    table, a, b = extract_r02_table(ref_draft)
    sec = _section(add_text, "## A · HISTORY")
    if sec is None:
        return ["§A HISTORY section absent"], ""
    n = ("\n" + sec + "\n").count("\n" + table + "\n")
    if n != 1:
        return [f"the R0.2 table (draft lines {a}–{b}) appears {n}x in §A HISTORY, not once verbatim"], ""
    return [], f"R0.2 table (draft lines {a}–{b}, {b - a + 1} lines) verbatim once in §A HISTORY"


def check_r0seal(ref_draft: str, anchor_ledger: dict):
    table, _, _ = extract_r02_table(ref_draft)
    rend = render_ledger_table(anchor_ledger["stages"])
    if rend == table:
        return [], f"{len(anchor_ledger['stages'])}/{len(anchor_ledger['stages'])} rows re-render byte-identically"
    rl, tl = rend.split("\n"), table.split("\n")
    bad = [i + 1 for i in range(max(len(rl), len(tl)))
           if (rl[i] if i < len(rl) else None) != (tl[i] if i < len(tl) else None)]
    return [f"R0.2 table differs from the {ANCHOR} ledger's rendering at table line(s) {bad}"], ""


def fingerprint(paths):
    out = {}
    for p in paths:
        st = os.stat(p)
        out[p.name] = (sha256(p.read_bytes()), st.st_size, st.st_mtime_ns)
    return out


def check_readonly(before: dict, after: dict):
    F = []
    for k in before:
        if k not in after:
            F.append(f"{k} vanished")
            continue
        (h0, s0, t0), (h1, s1, t1) = before[k], after[k]
        if h0 != h1:
            F.append(f"{k} bytes changed")
        if s0 != s1:
            F.append(f"{k} size changed")
        if t0 != t1:
            F.append(f"{k} mtime changed")
    return F, f"{len(before)} files: sha256, size and mtime unchanged"


# ─────────────────────────────── the legs ───────────────────────────────────
LEGS = []


def leg(name, fails_if):
    def deco(fn):
        LEGS.append((name, fails_if, fn))
        return fn
    return deco


def _copy(src: Path, scratch: Path, name: str) -> Path:
    dst = scratch / name
    shutil.copy2(src, dst)
    return dst


@leg("F-SL-COVER", "any PROGRESS stage, or any tierc10 commit after f97cded, is absent from "
     "STAGE_LOG.md (and not already in §1), is printed twice, a line names a stage/commit the "
     "record does not hold, or a bullet is malformed")
def leg_cover(ctx):
    real = check_cover(ctx["out"][OUT_LOG_NAME].decode(), ctx["progress"], ctx["draft"], ctx["facts"])
    sab = []
    stages = ctx["progress"]["stages"]
    drop = stages[len(stages) // 2]["stage"]
    cp = _copy(PROGRESS, ctx["scratch"], "PROGRESS.cover.json")
    j = json.loads(cp.read_text(encoding="utf-8"))
    j["stages"] = [s for s in j["stages"] if s["stage"] != drop]
    cp.write_text(json.dumps(j, ensure_ascii=False, indent=2), encoding="utf-8")
    out = gather_and_emit(cp, DRAFT, ctx["facts"])[3]
    sab.append((f"remove stage '{drop}' from a COPY of PROGRESS.json, emit",
                check_cover(out[OUT_LOG_NAME].decode(), ctx["progress"], ctx["draft"], ctx["facts"])[0]))
    after = [c for c in ctx["facts"]["tierc10"] if c["H"] in ctx["facts"]["after"]]
    dh = after[len(after) // 2]["h"]
    f2 = dict(ctx["facts"], tierc10=[c for c in ctx["facts"]["tierc10"] if c["h"] != dh])
    out = emit(ctx["pb"], ctx["db"], f2)
    sab.append((f"drop commit {dh} from the commit record, emit",
                check_cover(out[OUT_LOG_NAME].decode(), ctx["progress"], ctx["draft"], ctx["facts"])[0]))
    return real, sab


@leg("F-SL-VERBATIM", "any stage line's text differs from its PROGRESS one_line by one byte, or "
     "names a commit whose committed ledger does not carry it (or is not where it began to stand), "
     "or a commit line does not re-join to its git subject, or a date is not the %cI of its sha")
def leg_verbatim(ctx):
    real = check_verbatim(ctx["out"][OUT_LOG_NAME].decode(), ctx["progress"], ctx["facts"])
    sab = []
    tgt = ctx["progress"]["stages"][0]["stage"]
    cp = _copy(PROGRESS, ctx["scratch"], "PROGRESS.verbatim.json")
    j = json.loads(cp.read_text(encoding="utf-8"))
    w = j["stages"][0]["one_line"].split(" ")
    old = w[2]
    w[2] = "SABOTAGED"
    j["stages"][0]["one_line"] = " ".join(w)
    cp.write_text(json.dumps(j, ensure_ascii=False, indent=2), encoding="utf-8")
    out = gather_and_emit(cp, DRAFT, ctx["facts"])[3]
    sab.append((f"edit word 3 ('{old}') of '{tgt}''s one_line in a COPY of PROGRESS.json, emit",
                check_verbatim(out[OUT_LOG_NAME].decode(), ctx["progress"], ctx["facts"])[0]))
    lines = ctx["out"][OUT_LOG_NAME].decode().split("\n")
    bi = next(i for i, l in enumerate(lines) if l.startswith("## B · "))
    ci = next(i for i in range(bi, len(lines)) if lines[i].startswith("- **"))
    mm = LINE_RE.match(lines[ci])
    tw = mm.group("text").split(" ")
    tw[0] = "SABOTAGED"
    bent = list(lines)
    bent[ci] = _fmt_line(mm.group("label"), mm.group("date"), " ".join(tw), mm.group("sha"))
    sab.append((f"edit word 1 of commit line {mm.group('sha')} in the emitted log",
                check_verbatim("\n".join(bent), ctx["progress"], ctx["facts"])[0]))
    hist = ctx["facts"]["hist"]
    hidx = {r["h"]: i for i, r in enumerate(hist)}
    ai = next(i for i, l in enumerate(lines) if l.startswith("## A · "))
    for i in range(ai, bi):
        mm = LINE_RE.match(lines[i]) if lines[i].startswith("- **") else None
        if mm and mm.group("sha") in hidx and hidx[mm.group("sha")] > 0:
            prev = hist[hidx[mm.group("sha")] - 1]
            bent = list(lines)
            bent[i] = _fmt_line(mm.group("label"), prev["ciso"], mm.group("text"), prev["h"])
            sab.append((f"re-attribute '{mm.group('label')}' from {mm.group('sha')} to the earlier ledger {prev['h']}",
                        check_verbatim("\n".join(bent), ctx["progress"], ctx["facts"])[0]))
            break
    return real, sab


@leg("F-SL-HISTORY", "R0_ADDENDUM.md's §A HISTORY does not carry the R0.2 table text of "
     "BUILD_DRAFT.md exactly once, byte-for-byte, as whole contiguous lines (altered or omitted)")
def leg_history(ctx):
    add = ctx["out"][OUT_ADD_NAME].decode()
    real = check_history(add, ctx["draft"])
    sab = []
    sec = _section(add, "## A · HISTORY")
    bent_sec = sec.replace("| **PARTIAL** |", "| **COMPLETE-VERIFIED** |", 1)
    sab.append(("alter one cell of the emitted history (first PARTIAL -> COMPLETE-VERIFIED)",
                check_history(add.replace(sec, bent_sec, 1), ctx["draft"])[0]))
    table, a, b = extract_r02_table(ctx["draft"])
    rows = table.split("\n")
    cd = _copy(DRAFT, ctx["scratch"], "BUILD_DRAFT.history.md")
    cd.write_text(ctx["draft"].replace(table, "\n".join(rows[:3] + rows[4:]), 1), encoding="utf-8")
    out = gather_and_emit(PROGRESS, cd, ctx["facts"])[3]
    sab.append((f"emit from a COPY of the draft with R0.2 row 2 ('{rows[3].split('|')[1].strip()}') deleted",
                check_history(out[OUT_ADD_NAME].decode(), ctx["draft"])[0]))
    sab.append(("omit the table from the emitted history",
                check_history(add.replace(sec, sec.replace(table + "\n", "", 1), 1), ctx["draft"])[0]))
    return real, sab


@leg("F-SL-R0SEAL", f"the R0.2 table does not re-render byte-identically from PROGRESS.json AS "
     f"COMMITTED AT {ANCHOR} — the history printed is not the ledger it claims to be")
def leg_r0seal(ctx):
    rec = next(r for r in ctx["facts"]["hist"] if r["H"] == ctx["facts"]["anchor_full"])
    real = check_r0seal(ctx["draft"], rec["ledger"])
    sab = []
    bent = json.loads(json.dumps(rec["ledger"]))
    tgt = next(s for s in bent["stages"] if s["status"] == PARTIAL)
    tgt["status"] = CV
    sab.append((f"the {ANCHOR} ledger with '{tgt['stage']}' flipped PARTIAL -> COMPLETE-VERIFIED",
                check_r0seal(ctx["draft"], bent)[0]))
    table, _, _ = extract_r02_table(ctx["draft"])
    rows = table.split("\n")
    cells = rows[2].split(" | ")
    cells[-1] = str(int(cells[-1].rstrip(" |")) + 1) + " |"
    bent_draft = ctx["draft"].replace(rows[2], " | ".join(cells), 1)
    cd = _copy(DRAFT, ctx["scratch"], "BUILD_DRAFT.r0seal.md")
    cd.write_text(bent_draft, encoding="utf-8")
    sab.append((f"a COPY of the draft with '{rows[2].split('|')[1].strip()}''s blocker count bent by +1",
                check_r0seal(cd.read_text(encoding="utf-8"), rec["ledger"])[0]))
    return real, sab


@leg("F-SL-INPUTS", "while gathering and emitting, the run opens any repo file but PROGRESS.json "
     "and BUILD_DRAFT.md (registrations/, scores/, *.scored.json above all), anything under "
     "~/.cache/naiad, anything for writing, mutates any path, or starts any subprocess but git "
     "with a read-only subcommand (log, show, rev-list, rev-parse); or the hook did not observe "
     "the two declared reads and a git call (blind)")
def leg_inputs(ctx):
    real = check_inputs(ctx["audit_real"], ctx["audit_seen"])
    sab = []
    plant = T10 / "scores" / "__SABOTAGE_PLANT_NEVER_EXISTS__.json"

    def planted_open():
        gather_and_emit()
        with open(plant, "rb"):
            pass
    _, vv, _err, seen = audited(planted_open)
    sab.append(("a full gather + a planted read of research_outputs/tierc10/scores/<plant>.json "
                "(blocked before the open)", check_inputs(vv, seen)[0]))

    def planted_git():
        gather_and_emit()
        subprocess.run(["git", "-C", str(ROOT), "status", "--porcelain"], capture_output=True,
                       env=dict(os.environ, GIT_OPTIONAL_LOCKS="0"))
    _, vv, _err, seen = audited(planted_git)
    sab.append(("a full gather + a planted `git status` (blocked before exec)", check_inputs(vv, seen)[0]))

    def planted_write():
        gather_and_emit()
        with open(ctx["scratch"] / "planted_write.txt", "w"):
            pass
    _, vv, _err, seen = audited(planted_write)
    sab.append(("a full gather + a planted write-mode open in scratch (blocked before the open)",
                check_inputs(vv, seen)[0]))
    sab.append(("a BLIND hook: the canonical run's violations with nothing observed",
                check_inputs(ctx["audit_real"], {"reads": set(), "git": []})[0]))
    return real, sab


@leg("F-DET", "STAGE_LOG.md or R0_ADDENDUM.md differ by one byte between the in-process emission, "
     "the files on disk, and two emissions in two fresh processes (fresh hash seeds)")
def leg_det(ctx):
    canon = ctx["out"]
    runs = {"on disk": {k: (OUT_DIR / k).read_bytes() for k in canon}}
    for i in (1, 2):
        d = ctx["scratch"] / f"det{i}"
        d.mkdir()
        env = dict(os.environ)
        env.pop("PYTHONHASHSEED", None)
        r = subprocess.run([sys.executable, str(Path(__file__).resolve()), "--emit-to", str(d)],
                           capture_output=True, env=env)
        if r.returncode:
            runs[f"process {i}"] = {k: b"" for k in canon}
            runs[f"process {i}"]["__err__"] = r.stderr[-400:]
        else:
            runs[f"process {i}"] = {k: (d / k).read_bytes() for k in canon}

    def compare(others):
        F = []
        for who, got in others.items():
            if "__err__" in got:
                F.append(f"{who} failed: {got['__err__'].decode('utf-8', 'replace').strip()[-200:]}")
            for k in canon:
                if got.get(k) != canon[k]:
                    F.append(f"{k}: {who} differs from the in-process emission")
        return F
    shas = " · ".join(f"{k} {sha256(canon[k])[:16]}" for k in canon)
    real = (compare(runs), f"4 emissions byte-identical ({shas})")
    g = globals()
    orig = g["render_addendum"]
    g["render_addendum"] = lambda m: orig(m) + f"<!-- {time.perf_counter_ns()} -->\n"
    try:
        stamped = emit(ctx["pb"], ctx["db"], ctx["facts"])
    finally:
        g["render_addendum"] = orig
    return real, [("an emission with a clock stamped into R0_ADDENDUM.md", compare({"stamped run": stamped}))]


@leg("F-SL-READONLY", "the bytes (sha256) — or, stricter, the size or the mtime — of PROGRESS.json, "
     "FIXTURES_RESUME.txt or BUILD_DRAFT.md change between the start of the run and the end of the "
     "last leg")
def leg_readonly(ctx):
    ctx["fp_after"] = fingerprint(WATCHED)
    real = check_readonly(ctx["fp_before"], ctx["fp_after"])
    sab = []
    sd = ctx["scratch"] / "ro"
    sd.mkdir()
    copies = [_copy(p, sd, p.name) for p in WATCHED]
    cp, cf, cd = copies

    def append_byte(p):
        with open(p, "ab") as fh:
            fh.write(b"\n")

    def utime(p):
        st = os.stat(p)
        os.utime(p, ns=(st.st_atime_ns, st.st_mtime_ns + 1_000_000_000))

    def flip_byte(p):
        b = bytearray(p.read_bytes())
        b[len(b) // 2] ^= 0x01
        st = os.stat(p)
        p.write_bytes(bytes(b))
        os.utime(p, ns=(st.st_atime_ns, st.st_mtime_ns))

    for label, tgt, act in (("append one byte to the PROGRESS.json copy", cp, append_byte),
                            ("`touch` the FIXTURES_RESUME.txt copy (mtime only)", cf, utime),
                            ("flip one byte of the BUILD_DRAFT.md copy, size and mtime kept", cd, flip_byte)):
        before = fingerprint(copies)
        gather_and_emit(cp, cd, ctx["facts"])
        act(tgt)
        sab.append((label + " during a watched emission", check_readonly(before, fingerprint(copies))[0]))
    return real, sab


# ─────────────────────────────── main ───────────────────────────────────────
def main(argv) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--emit-to", default=None)
    args = ap.parse_args(argv)

    if args.emit_to:
        d = Path(args.emit_to)
        out = gather_and_emit()[3]
        for k, v in out.items():
            (d / k).write_bytes(v)
        return 0

    fp_before = fingerprint(WATCHED)
    lines = []

    def say(s=""):
        lines.append(s)
        print(s, flush=True)

    # THE CANONICAL GATHER + EMIT RUNS UNDER THE AUDIT HOOK (blocking).
    res, viol, err, seen = audited(gather_and_emit)
    if err or res is None:
        raise SystemExit(f"HALT: the canonical gather/emit tripped F-SL-INPUTS: {err or viol}")
    pb, db, facts, out = res
    progress = json.loads(pb.decode("utf-8"))
    draft = db.decode("utf-8")
    m = model(pb, db, facts)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for k, v in out.items():
        (OUT_DIR / k).write_bytes(v)

    say("=" * 78)
    say("TIER-C10 · CLOSE · LAW 6 STAGE LOG — FIXTURES (F-SL-*, F-DET)")
    say("REPORT-ONLY: a ledger reprint. No registration scored or consulted; no bar read;")
    say("tierc10_data.load_asof not needed (this script opens no klines file).")
    say(f"script   scripts/{Path(__file__).name}  sha256 {sha256(Path(__file__).read_bytes())}")
    say(f"substrate NAIAD_CACHE_DIR = {SNAPSHOT}  (guard passed)")
    say("=" * 78)
    say("INPUTS (read-only)")
    for p in WATCHED:
        h, sz, _ = fp_before[p.name]
        say(f"  {p.relative_to(ROOT)}  sha256 {h}  {sz:,} B")
    say(f"  git log --grep='^tierc10' --format='%h %cI %s' : {len(facts['tierc10'])} commits; "
        f"{len(m['sel']['after'])} after {ANCHOR}; {len(m['sel']['sec1_commit_skips'])} already in §1")
    say(f"  committed ledgers (git log -- PROGRESS.json): {len(facts['hist'])} — "
        + " ".join(r["h"] for r in facts["hist"]))
    say(f"  PROGRESS.json working tree == newest committed blob: "
        f"{m['progress_sha'] == sha256(facts['head_progress'].encode('utf-8'))}")
    say(f"  BUILD_DRAFT.md working tree == HEAD blob: "
        f"{m['draft_sha'] == sha256(facts['head_draft'].encode('utf-8'))}  (last changed "
        f"{facts['draft_last'].split(' ')[0]})")
    say(f"  §1 STAGE LOG holds {m['sec1_bullets']} lines; §R0.2 table = draft lines "
        f"{m['r02_lines'][0]}–{m['r02_lines'][1]}")
    say("OUTPUTS (research_outputs/tierc10/close/)")
    for k, v in out.items():
        say(f"  {k:<16} sha256 {sha256(v)}  {len(v):,} B  {v.count(b'\n')} lines")
    say(f"  STAGE_LOG.md: §A {len(m['stage_lines'])} stage lines · §B {len(m['commit_lines'])} commit lines")
    say(f"  R0.2 history: {sum(1 for v in m['r02_status'].values() if v == CV)} CV / "
        f"{sum(1 for v in m['r02_status'].values() if v == PARTIAL)} PARTIAL of {len(m['r02_status'])}; "
        f"now: {sum(1 for s in progress['stages'] if s['status'] == CV)} CV / "
        f"{sum(1 for s in progress['stages'] if s['status'] == PARTIAL)} PARTIAL of {len(progress['stages'])}")
    for s in progress["stages"]:
        t = transitions(s["stage"], s["status"], facts["hist"], facts)
        if t["flip"]:
            say(f"  moved PARTIAL -> CV: {s['stage']} at {t['flip'][2]['h']} "
                f"(last PARTIAL record {t['flip'][0]['h']}; window {len(t['window'])} tierc10 commits)")
    for s in progress["stages"]:
        if s["status"] != CV:
            say(f"  remains {s['status']}: {s['stage']} ({len(s.get('blockers', []))} blockers, verbatim in §D)")
    say("=" * 78)

    with tempfile.TemporaryDirectory(prefix="tc10_stage_log_") as td:
        ctx = {"pb": pb, "db": db, "facts": facts, "out": out, "progress": progress,
               "draft": draft, "scratch": Path(td), "fp_before": fp_before,
               "audit_real": viol, "audit_seen": seen}
        n_green = n_sab = n_sab_red = 0
        for name, fails_if, fn in LEGS:
            (rf, rsum), sabs = fn(ctx)
            say(name)
            say(f"  FAILS IF   : {fails_if}")
            if rf:
                say(f"  real       : RED — {len(rf)} finding(s)")
                for x in rf:
                    say(f"               · {x}")
            else:
                say(f"  real       : GREEN — {rsum}")
            ok = not rf
            for i, (desc, sf) in enumerate(sabs, 1):
                n_sab += 1
                if sf:
                    n_sab_red += 1
                    say(f"  sabotage {i} : RED as required — {desc}")
                    say(f"               · {sf[0]}" + (f"  (+{len(sf) - 1} more)" if len(sf) > 1 else ""))
                else:
                    ok = False
                    say(f"  sabotage {i} : GREEN — NOT CAUGHT — {desc}")
            if not sabs:
                ok = False
                say("  sabotage   : NONE — a leg without sabotage cannot be GREEN")
            n_green += ok
            say(f"  verdict    : {'GREEN' if ok else 'RED'}")
    say("=" * 78)
    n = len(LEGS)
    say(f"FIXTURE SUMMARY {n_green}/{n} GREEN · {n - n_green} RED · sabotages {n_sab_red}/{n_sab} RED as required")
    say("=" * 78)
    OUT_FIX.write_text("\n".join(lines) + "\n", encoding="utf-8")
    if check_readonly(fp_before, fingerprint(WATCHED))[0]:
        print("F-SL-READONLY (post-transcript): a watched file changed after the last leg", file=sys.stderr)
        return 1
    return 0 if n_green == n else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
