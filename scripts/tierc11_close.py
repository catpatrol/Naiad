#!/usr/bin/env python
"""TIER-C11 · CLOSE — THE BUILD DOCUMENT, THE FINDINGS, BOX-COST, THE LEDGER APPEND, THE OPERATOR'S ACTS.

A DETERMINISTIC GENERATOR.  Re-running it on an unchanged tree reproduces every output byte for byte
(no clock, no random draw, no absolute home path, sorted iteration everywhere).  It never scores,
never re-words a registration, never consults a verdict to choose anything (verdicts are COPIED from
the record), never writes under exchange/, never commits, never pushes and never calls publish().

WHAT IT READS (read-only)
  the contract of record exchange/queue/2026-09-24_TC11_APOLLO.md; research_outputs/tierc11/** (the
  stage reports, the scorer's records, PROGRESS.json, LEANS, the reviews and attestations); the TC10
  contract, TC10's staged append (the SAIL hold and the tier line; or TC10's block on LEDGER_APOLLO once TC10's
  CLOSE has landed) and TC10's close_acts.sh (its step-6 'git add' finding; its moves, for the projection); the tc11x
  lane's PINNED commit df0b5c4 (git only); stage_r/R5_CHOP.md (R5's direction cells, never the git-ignored parquet);
  scripts/publish_exchange.py
  and scripts/backup_estate.py (constants by ast.literal_eval — never imported, never executed);
  read-only git plumbing (log, rev-list, rev-parse, merge-base, branch -r --contains, ls-files,
  check-ignore, diff --quiet, cat-file, ls-tree); two input records filed for the CLOSE:
    research_outputs/tierc11/close/COMPUTE_LEDGER.json   the orchestrator's compute figures (the ONE
                                                          exception to "no typed number")
    research_outputs/tierc11/close/TC11_FIX_VERIFY.json  the TC11-FIX wave's reports, copied from the
                                                          harness's workflow journal

WHAT IT WRITES (nothing else; an output guard refuses any other path)
  research_outputs/tierc11/BUILD_DRAFT.md                      the build document (LAW 5: drafted off-bus)
  research_outputs/tierc11/LEDGER_APOLLO_APPEND.md             the staged append for exchange/status/LEDGER_APOLLO.md
  research_outputs/tierc11/close/S5_FINDINGS_NOT_FIXED.{json,md}
  research_outputs/tierc11/close/BOX_COST.{md,json}
  research_outputs/tierc11/close/TRACES.json                   every number's file + field, and its uses
  research_outputs/tierc11/close/close_acts.sh                 the operator's acts (bash)

HOW A NUMBER GETS INTO AN OUTPUT
  Only three ways, each checked by scripts/tierc11_close_fixtures.py:
  (1) T(key, spec, fmt): the value is RESOLVED from its record (a JSON field, a parquet cell, a text
      match, a git fact, an ast constant, a file's bytes) and FORMATTED by a named format; the pair is
      filed in TRACES.json with the number of times each region used it (F-NUM re-derives it);
  (2) a VERBATIM block: source lines copied byte for byte behind a marker
      <!-- verbatim: <path>:<line spans> --> (F-NUM / F-S0-NINE re-read the lines);
  (3) a «cite» with its '|' / '+' quote lines in the append (TC10's render_quote; F-LAR11 re-verifies
      it with TC10's verify_quote).
  Harvested findings carry their verbatim text and the locator that re-extracts it (F-FNF).

Run:  export NAIAD_CACHE_DIR=/Users/luis/.cache/naiad/snapshots/tc11_20260925 PYTHONDONTWRITEBYTECODE=1
      ~/venvs/naiad/bin/python scripts/tierc11_close.py [--out-root=DIR]
Exit: 0 written · a HALT (SystemExit with the reason) writes nothing.
"""
from __future__ import annotations

import ast
import datetime as _dt
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = Path.home() / ".cache" / "naiad" / "snapshots" / "tc11_20260925"
LIVE_CACHE = Path.home() / ".cache" / "naiad" / "data_cache"


def halt(msg: str):
    raise SystemExit(f"HALT: {msg}")


def guard_env() -> None:
    env = os.environ.get("NAIAD_CACHE_DIR")
    if not env:
        halt(f"NAIAD_CACHE_DIR is unset — the TC11 CLOSE runs only on {SNAPSHOT}")
    norm = Path(os.path.normpath(os.path.expanduser(env)))
    if norm == LIVE_CACHE or LIVE_CACHE in norm.parents:
        halt("NAIAD_CACHE_DIR names the LIVE cache — READ-NEVER, WRITE-NEVER for TC11")
    if norm.resolve() != SNAPSHOT.resolve():
        halt(f"NAIAD_CACHE_DIR={norm} is not the TC11 snapshot {SNAPSHOT}")
    if os.environ.get("PYTHONDONTWRITEBYTECODE") != "1":
        halt("PYTHONDONTWRITEBYTECODE is not 1 (the TC11 run law)")


guard_env()
sys.path.insert(0, str(ROOT / "scripts"))
import tierc10_close_close_ledger_append as LA   # TC10's quote renderer / parser / verifier  # noqa: E402

# ═══════════════════════════════════════════════════════════════ paths of record
TC11 = "research_outputs/tierc11"
CLOSE = f"{TC11}/close"
CONTRACT = "exchange/queue/2026-09-24_TC11_APOLLO.md"
TC10_CONTRACT = "exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md"
TC10_APPEND = "research_outputs/tierc10/LEDGER_APOLLO_APPEND.md"
TC10_DOC = "exchange/reports/BUILD_2026-09-21_TIERC10_UNSEEN_RANGES.md"
TC10_ACTS = "research_outputs/tierc10/close/close_acts.sh"
LEDGER_APOLLO = "exchange/status/LEDGER_APOLLO.md"
DOC = "exchange/reports/BUILD_2026-09-24_TIERC11_EVENTS.md"
PUBLISH = "scripts/publish_exchange.py"
BACKUP = "scripts/backup_estate.py"
PROGRESS = f"{TC11}/PROGRESS.json"
LEANS = f"{TC11}/LEANS.md"
AMEND = f"{TC11}/LEANS_AMENDMENTS.md"
REGS = f"{TC11}/registrations/REGISTRATIONS.json"
SCORES = f"{TC11}/scores/SCORES.json"
FAMILY = f"{TC11}/scores/FAMILY.json"
S0MD = f"{TC11}/scores/S0_VERDICTS.md"
REGCHECK = f"{TC11}/scores/REGISTRY_CHECK.json"
R2J = f"{TC11}/stage_r/R2_LENS_VERDICTS.json"
R5MD = f"{TC11}/stage_r/R5_CHOP.md"
R1MD = f"{TC11}/stage_r/R1_LENSES.md"
NESTMD = f"{TC11}/stage_r/NEST_GRID.md"
LANESMD = f"{TC11}/stage_r/lanes/NEST_GRID_LANES.md"
STAGE_R = f"{TC11}/stage_r/STAGE_R.md"
R4MD = f"{TC11}/stage_r4/STAGE_R4.md"
WMD = f"{TC11}/stage_w/STAGE_W.md"
GMD = f"{TC11}/stage_g/STAGE_G.md"
TBRK = f"{TC11}/stage_t_brk/STAGE_T_BRK.md"
TREL = f"{TC11}/stage_t_relay/STAGE_T_RELAY.md"
FWDMD = f"{TC11}/forward/FORWARD_LEDGER.md"
FWDJL = f"{TC11}/forward/FORWARD_LEDGER.jsonl"
SMD = f"{TC11}/stage_s/STAGE_S.md"
AMD = f"{TC11}/stage_a/STAGE_A.md"
HMD = f"{TC11}/stage_h/STAGE_H.md"
FINAL = f"{TC11}/review/FINAL_REVIEW_2026-09-25.json"
ATTEST = f"{TC11}/review/attest"
BOOKS_FX = f"{TC11}/books/FIXTURES_BOOKS.txt"
COMPUTE = f"{CLOSE}/COMPUTE_LEDGER.json"
FIXV = f"{CLOSE}/TC11_FIX_VERIFY.json"

OUT_DRAFT = f"{TC11}/BUILD_DRAFT.md"
OUT_APPEND = f"{TC11}/LEDGER_APOLLO_APPEND.md"
OUT_S5J = f"{CLOSE}/S5_FINDINGS_NOT_FIXED.json"
OUT_S5M = f"{CLOSE}/S5_FINDINGS_NOT_FIXED.md"
OUT_BOXM = f"{CLOSE}/BOX_COST.md"
OUT_BOXJ = f"{CLOSE}/BOX_COST.json"
OUT_TRACES = f"{CLOSE}/TRACES.json"
OUT_ACTS = f"{CLOSE}/close_acts.sh"
OUTPUTS = (OUT_DRAFT, OUT_APPEND, OUT_S5J, OUT_S5M, OUT_BOXM, OUT_BOXJ, OUT_TRACES, OUT_ACTS)
FIXTURES_SCRIPT = "scripts/tierc11_close_fixtures.py"
GENERATOR_SCRIPT = "scripts/tierc11_close.py"
TRANSCRIPT = f"{CLOSE}/FIXTURES_CLOSE.txt"
STAMPED_TRANSCRIPT = f"{CLOSE}/FIXTURES_CLOSE_LEDGER_STAMPED.txt"
# the CLOSE's own files, committed by the CLOSE commit before the operator runs close_acts.sh
CLOSE_SOURCES = (OUT_DRAFT, OUT_APPEND, OUT_S5J, OUT_S5M, OUT_BOXM, OUT_BOXJ, OUT_TRACES, OUT_ACTS,
                 COMPUTE, FIXV, TRANSCRIPT, GENERATOR_SCRIPT, FIXTURES_SCRIPT, f"{ATTEST}/fix-head.json")
VOLATILE = (TRANSCRIPT, STAMPED_TRANSCRIPT)       # rewritten by fixture runs: listed, never sized
SELF_UNSIZED = (OUT_BOXM, OUT_BOXJ, OUT_TRACES)    # written with or after the table: listed, never sized
BRANCH = "v12-v1-census"
REMOTE_REF = f"origin/{BRANCH}"
TIER_PREFIX = "tierc11("
STAMP_TEXT = ("⟦STAMP AT CLOSE — replace this bracket with 'N tierc11 commits, M on a remote', read AFTER "
              "the push (close_acts.sh step 3); then re-run scripts/tierc11_close_fixtures.py F-LAR11 --stamped⟧")
STAMP_RE = re.compile(r"⟦STAMP AT CLOSE[^⟧\n]*⟧")
COLLAR = "tier TIER-E · a SELECTION, not a result · gates nothing"
COLLAR_LINE = f"*{COLLAR}.*"          # printed above every non-registered table the draft copies (contract :8)
# the tc11x lane's commit that names its vendored env shim — PINNED (the lane branch moves; this commit does not)
TC11X_PIN = "df0b5c4"
# the TC10 STATUS header on LEDGER_APOLLO (TC11's close_acts.sh step 0 greps the same pattern)
TC10_HDR_RE = re.compile(r"(?m)^=== STATUS_APOLLO — \d{4}-\d{2}-\d{2} — TIER-C10 · ")
VERBATIM_RE = re.compile(r"^<!-- verbatim: ([^:]+):([0-9,\-]+) -->$")
SEP = "\n---\n\n"


# ═══════════════════════════════════════════════════════════════ git (read-only)
GIT_OK = {"log", "rev-list", "rev-parse", "merge-base", "branch", "ls-files", "check-ignore", "diff",
          "cat-file", "ls-tree", "show", "for-each-ref"}


def git(*a: str, check: bool = True, stdin: str | None = None) -> str:
    if a[0] not in GIT_OK:
        halt(f"git {a[0]} is not a read-only subcommand this generator may run")
    if a[0] == "branch" and "-r" not in a:
        halt("git branch is allowed only as 'branch -r --contains'")
    r = subprocess.run(["git", "-C", str(ROOT), *a], capture_output=True, text=True, input=stdin)
    if check and r.returncode != 0:
        halt(f"git {' '.join(a)} failed: {r.stderr.strip()}")
    return r.stdout


def git_rc(*a: str) -> int:
    if a[0] not in GIT_OK:
        halt(f"git {a[0]} is not a read-only subcommand this generator may run")
    return subprocess.run(["git", "-C", str(ROOT), *a], capture_output=True, text=True).returncode


def tier_commits(rev: str) -> list[tuple[str, str, str, str]]:
    """(full, short, iso date, subject) of every commit in rev's history whose subject starts tierc11(,
    oldest first."""
    out = []
    for ln in git("log", "--reverse", "--format=%H%x09%h%x09%cI%x09%s", rev).splitlines():
        h, s, d, subj = ln.split("\t", 3)
        if subj.startswith(TIER_PREFIX):
            out.append((h, s, d, subj))
    return out


def is_ancestor(a: str, b: str) -> bool:
    return git_rc("merge-base", "--is-ancestor", a, b) == 0


# ═══════════════════════════════════════════════════════════════ sources (read-only, sha-recorded)
class Sources:
    def __init__(self):
        self.read: dict[str, tuple[int, str]] = {}
        self._b: dict[str, bytes] = {}
        self._j: dict = {}
        self._pq: dict = {}

    def b(self, rel: str) -> bytes:
        if rel not in self._b:
            p = ROOT / rel
            if not p.is_file():
                halt(f"source {rel} is missing")
            data = p.read_bytes()
            self._b[rel] = data
            self.read[rel] = (len(data), hashlib.sha256(data).hexdigest())
        return self._b[rel]

    def t(self, rel: str) -> str:
        return self.b(rel).decode("utf-8")

    def lines(self, rel: str) -> list[str]:
        return self.t(rel).split("\n")

    def j(self, rel: str):
        if rel not in self._j:
            if rel.endswith(".jsonl"):
                self._j[rel] = [json.loads(x) for x in self.t(rel).splitlines() if x.strip()]
            else:
                self._j[rel] = json.loads(self.b(rel))
        return self._j[rel]

    def pq(self, rel: str):
        if rel not in self._pq:
            import pandas as pd
            self.b(rel)
            self._pq[rel] = pd.read_parquet(ROOT / rel)
        return self._pq[rel]

    def sha(self, rel: str) -> str:
        self.b(rel)
        return self.read[rel][1]

    def size(self, rel: str) -> int:
        self.b(rel)
        return self.read[rel][0]


SRC = Sources()


def ast_const(rel: str, name: str):
    """(value, line) of a module-level NAME = <literal> — ast.literal_eval, never import."""
    tree = ast.parse(SRC.t(rel))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in node.targets):
            return ast.literal_eval(node.value), node.lineno
    halt(f"{rel}: constant {name} not found")


# ═══════════════════════════════════════════════════════════════ resolving a spec
def resolve(spec: dict):
    k = spec["kind"]
    if k == "json":
        v = LA.resolve(SRC.j(spec["path"]), spec["sel"])
    elif k == "jsonl":
        v = LA.resolve(SRC.j(spec["path"])[spec["line"]], spec["sel"])
    elif k == "parquet":
        df = SRC.pq(spec["path"])
        m = df
        for c, val in sorted(spec["where"].items()):
            m = m[m[c].astype(str) == str(val)]
        if len(m) != 1:
            halt(f"parquet spec {spec} matched {len(m)} rows (exactly one is required)")
        v = m.iloc[0][spec["col"]]
        v = v.item() if hasattr(v, "item") else v
    elif k == "text":
        ms = list(re.finditer(spec["re"], SRC.t(spec["path"]), flags=re.M))
        if len(ms) != 1:
            halt(f"text spec {spec} matched {len(ms)} times (exactly one is required)")
        v = ms[0].group(1)
    elif k == "git":
        w = spec["what"]
        if w == "tierc11_count_in":
            v = len(tier_commits(spec["rev"]))
        elif w == "tierc11_count_ancestor_of":
            v = sum(1 for c in tier_commits(spec["rev"]) if is_ancestor(c[0], spec["base"]))
        elif w == "tierc11_not_ancestor_of":
            v = " ".join(c[1] for c in tier_commits(spec["rev"]) if not is_ancestor(c[0], spec["base"]))
        elif w == "subject":
            v = git("log", "-1", "--format=%s", spec["rev"]).strip()
        elif w == "date":
            v = git("log", "-1", "--format=%cI", spec["rev"]).strip()
        elif w == "short":
            v = git("rev-parse", "--short=7", spec["rev"]).strip()
        elif w == "ahead":
            v = int(git("rev-list", "--count", f"{spec['base']}..{spec['rev']}").strip())
        elif w == "json_leaves":
            a = leaves(json.loads(git("show", f"{spec['base']}:{spec['path']}")))
            b = leaves(json.loads(git("show", f"{spec['rev']}:{spec['path']}")))
            st = spec["stat"]
            if st == "added":
                v = len(set(b) - set(a))
            elif st == "removed":
                v = len(set(a) - set(b))
            elif st == "changed":
                v = sum(1 for k in set(a) & set(b) if a[k] != b[k])
            elif st == "changed_non_string":
                v = sum(1 for k in set(a) & set(b) if a[k] != b[k]
                        and not (isinstance(a[k], str) and isinstance(b[k], str)))
            else:
                halt(f"unknown json_leaves stat {st}")
        else:
            halt(f"unknown git spec {w}")
    elif k == "mdcell":
        # a markdown table cell: the first table after the ONE line starting `heading`, the ONE row whose first
        # cell is `row`, the cell under the column `col` (F-NUM re-reads it with its own parser)
        l1, l2 = table_after_line(spec["path"], spec["heading"])
        rows = [r for _, r in md_table_rows(spec["path"], l1, l2)]
        hits = [r for r in rows if next(iter(r.values())) == spec["row"]]
        if len(hits) != 1:
            halt(f"mdcell spec {spec} matched {len(hits)} rows (exactly one is required)")
        if spec["col"] not in hits[0]:
            halt(f"mdcell spec {spec}: no column {spec['col']!r}")
        v = hits[0][spec["col"]]
    elif k == "const":
        v = ast_const(spec["path"], spec["name"])[0]
        if spec.get("index") is not None:
            v = v[spec["index"]]
    elif k == "file":
        if spec["what"] == "bytes":
            v = SRC.size(spec["path"])
        elif spec["what"] == "sha256":
            v = SRC.sha(spec["path"])
        else:
            halt(f"unknown file spec {spec}")
    else:
        halt(f"unknown spec kind {k}")
    if spec.get("agg") == "len":
        v = len(v)
    if spec.get("re_in_value"):
        ms = list(re.finditer(spec["re_in_value"], str(v)))
        if len(ms) != 1:
            halt(f"re_in_value {spec['re_in_value']!r} matched {len(ms)} times in {spec}")
        v = ms[0].group(1)
    return v


def fmtv(fmt: str, v) -> str:
    if fmt == "int":
        if float(v) != int(float(v)):
            halt(f"fmt int on a non-integral value {v!r}")
        return str(int(float(v)))
    if fmt == "intc":
        return f"{int(float(v)):,}"
    if fmt in ("f0", "f1", "f2", "f3", "f4", "f6", "f8"):
        return f"{float(v):.{fmt[1]}f}"
    if fmt in ("f1s", "f2s", "f3s", "f4s", "f6s", "f8s"):
        return f"{float(v):+.{fmt[1]}f}"
    if fmt == "pct3":
        return f"{100.0 * float(v):.3f}%"
    if fmt == "str":
        return str(v)
    if fmt == "date":
        return str(v)[:10]
    if fmt == "iso_ms":
        return _dt.datetime.fromtimestamp(int(v) / 1000, _dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    if fmt == "sha7":
        return str(v)[:7]
    if fmt == "sha12":
        return str(v)[:12]
    if fmt == "sha16":
        return str(v)[:16]
    halt(f"unknown format {fmt}")


# ═══════════════════════════════════════════════════════════════ the trace registry
class Tracer:
    """Every number an output prints goes through here: resolved from its record, formatted by name,
    counted per region.  TRACES.json files the registry; F-NUM re-derives every entry."""

    def __init__(self):
        self.items: dict[str, dict] = {}
        self.uses: dict[str, dict[str, int]] = {}
        self.ex_uses: dict[str, dict[str, int]] = {}
        self.region = "doc"

    def __call__(self, key: str, spec: dict, fmt: str) -> str:
        v = resolve(spec)
        lit = fmtv(fmt, v)
        if key in self.items:
            if self.items[key]["lit"] != lit or self.items[key]["spec"] != spec:
                halt(f"trace key {key} reused with a different spec or literal")
        else:
            self.items[key] = {"key": key, "lit": lit, "fmt": fmt, "spec": spec,
                               "value": v if isinstance(v, (int, float, str, bool)) or v is None else str(v)}
        u = self.uses.setdefault(key, {})
        u[self.region] = u.get(self.region, 0) + 1
        return lit

    def checkpoint(self):
        return json.loads(json.dumps([self.uses, self.ex_uses]))

    def restore(self, cp) -> None:
        self.uses, self.ex_uses = json.loads(json.dumps(cp[0])), json.loads(json.dumps(cp[1]))

    def ex(self, lit: str, why: str) -> str:
        """An EXEMPTION: a digit-bearing literal that is a NAME, not a measured value (e.g. '9/12', the
        frozen trigger pair).  Counted per region like a trace."""
        EXEMPT_WHY.setdefault(lit, why)
        u = self.ex_uses.setdefault(lit, {})
        u[self.region] = u.get(self.region, 0) + 1
        return lit


T = Tracer()
EXEMPT_WHY: dict[str, str] = {}


def JS(path: str, sel: str, **kw) -> dict:
    return {"kind": "json", "path": path, "sel": sel, **kw}


def JL(path: str, line: int, sel: str) -> dict:
    return {"kind": "jsonl", "path": path, "line": line, "sel": sel}


def PQ(path: str, where: dict, col: str) -> dict:
    return {"kind": "parquet", "path": path, "where": where, "col": col}


def TX(path: str, pattern: str) -> dict:
    return {"kind": "text", "path": path, "re": pattern}


def GIT(what: str, rev: str, base: str | None = None, **kw) -> dict:
    d = {"kind": "git", "what": what, "rev": rev, **kw}
    if base:
        d["base"] = base
    return d


def CONST(path: str, name: str, index: int | None = None) -> dict:
    d = {"kind": "const", "path": path, "name": name}
    if index is not None:
        d["index"] = index
    return d


def FILEB(path: str) -> dict:
    return {"kind": "file", "what": "bytes", "path": path}


def FILESHA(path: str) -> dict:
    return {"kind": "file", "what": "sha256", "path": path}


def MDC(path: str, heading: str, row: str, col: str) -> dict:
    return {"kind": "mdcell", "path": path, "heading": heading, "row": row, "col": col}


# ═══════════════════════════════════════════════════════════════ markdown helpers
def heading_level(line: str) -> int:
    m = re.match(r"^(#{1,6}) ", line)
    return len(m.group(1)) if m else 0


def find_heading(rel: str, prefix: str) -> int:
    """1-based line number of the ONE line starting with prefix."""
    hits = [i + 1 for i, ln in enumerate(SRC.lines(rel)) if ln.startswith(prefix)]
    if len(hits) != 1:
        halt(f"{rel}: heading/line prefix {prefix!r} found {len(hits)} times (exactly one is required)")
    return hits[0]


def block(rel: str, heading: str, *, first_table: bool = False, upto: str | None = None) -> tuple[int, int]:
    """(l1, l2), 1-based inclusive: the lines under `heading` up to the next heading of the same or a
    higher level, blank lines trimmed; first_table keeps only the first run of '|' lines; upto stops
    before the first line starting with it."""
    L = SRC.lines(rel)
    h = find_heading(rel, heading)
    lvl = heading_level(L[h - 1]) or 7
    end = len(L)
    for i in range(h, len(L)):
        hl = heading_level(L[i])
        if hl and hl <= lvl:
            end = i
            break
    idx = list(range(h, end))                      # 0-based indices of the body lines
    if upto is not None:
        cut = [i for i in idx if L[i].startswith(upto)]
        if not cut:
            halt(f"{rel}: 'upto' {upto!r} not found under {heading!r}")
        idx = [i for i in idx if i < cut[0]]
    if first_table:
        t = [i for i in idx if L[i].startswith("|")]
        if not t:
            halt(f"{rel}: no table under {heading!r}")
        run = [t[0]]
        for i in t[1:]:
            if i == run[-1] + 1:
                run.append(i)
            else:
                break
        idx = run
    while idx and not L[idx[0]].strip():
        idx = idx[1:]
    while idx and not L[idx[-1]].strip():
        idx = idx[:-1]
    if not idx:
        halt(f"{rel}: empty block under {heading!r}")
    return idx[0] + 1, idx[-1] + 1


def table_after_line(rel: str, prefix: str) -> tuple[int, int]:
    L = SRC.lines(rel)
    h = find_heading(rel, prefix)
    i = h
    while i < len(L) and not L[i].startswith("|"):
        i += 1
    j = i
    while j < len(L) and L[j].startswith("|"):
        j += 1
    if i >= len(L):
        halt(f"{rel}: no table after {prefix!r}")
    return i + 1, j


def spans_str(lines_1b: list[int]) -> str:
    out, s, p = [], None, None
    for n in lines_1b:
        if s is None:
            s = p = n
        elif n == p + 1:
            p = n
        else:
            out.append(f"{s}-{p}" if s != p else f"{s}")
            s = p = n
    if s is not None:
        out.append(f"{s}-{p}" if s != p else f"{s}")
    return ",".join(out)


def verbatim(rel: str, l1: int, l2: int | None = None, *, lines: list[int] | None = None) -> str:
    """The marker line, then the source lines byte for byte.  A block may not carry a level-1 or
    level-2 heading (it would break the document's own structure)."""
    L = SRC.lines(rel)
    nums = lines if lines is not None else list(range(l1, l2 + 1))
    body = [L[n - 1] for n in nums]
    for x in body:
        if heading_level(x) in (1, 2):
            halt(f"{rel}: a verbatim block may not carry an H1/H2 line ({x[:60]!r})")
    return "\n".join([f"<!-- verbatim: {rel}:{spans_str(nums)} -->"] + body)


def md_table_rows(rel: str, l1: int, l2: int) -> list[tuple[int, dict]]:
    """Parse a markdown table (header at l1, separator at l1+1) into (line, {col: cell})."""
    L = SRC.lines(rel)

    def cells(s: str) -> list[str]:
        s = s.strip()
        s = s[1:-1] if s.startswith("|") and s.endswith("|") else s
        parts = re.split(r"(?<!\\)\|", s)
        return [p.strip() for p in parts]
    head = cells(L[l1 - 1])
    out = []
    for n in range(l1 + 2, l2 + 1):
        c = cells(L[n - 1])
        if len(c) != len(head):
            halt(f"{rel}:{n}: {len(c)} cells under a {len(head)}-column header")
        out.append((n, dict(zip(head, c))))
    return out


# ═══════════════════════════════════════════════════════════════ the record, gathered
LENSES = ("5m", "15m", "1h", "4h", "12h", "1d", "1w")      # the contract's seven lenses (R1), in order


def gather() -> dict:
    X: dict = {}
    X["progress"] = SRC.j(PROGRESS)
    X["scores"] = SRC.j(SCORES)
    X["family"] = SRC.j(FAMILY)
    X["regs"] = SRC.j(REGS)
    X["r2"] = SRC.j(R2J)
    if sorted(LENSES) != sorted(X["r2"]["lenses"]):
        halt("R2_LENS_VERDICTS.json lens set is not the contract's seven lenses")
    # THE R2 GUARD. Every sentence this CLOSE writes about range trading ("closed by the R2 law on …", "the maker
    # twin fails too", "1w provisional") presumes every lens word and every maker twin reads FAIL. A PASS
    # anywhere makes those sentences false: HALT rather than print them.
    for k in LENSES:
        v = X["r2"]["lenses"][k]
        for fld in ("word", "verdict", "maker_twin"):
            if not str(v[fld]).startswith("FAIL"):
                halt(f"R2 GUARD: lens {k} {fld} reads {v[fld]!r}, not FAIL — the CLOSE's range-trading sentences "
                     "would be false")
    X["r2_closed"] = [k for k in LENSES if not X["r2"]["lenses"][k]["provisional"]]
    X["r2_prov"] = [k for k in LENSES if X["r2"]["lenses"][k]["provisional"]]
    if not X["r2_closed"] or X["r2_closed"] != list(LENSES[:len(X["r2_closed"])]):
        halt(f"R2 GUARD: the non-provisional FAIL lenses {X['r2_closed']} are not a leading run of the lens order")
    X["final"] = SRC.j(FINAL)
    X["fwd"] = SRC.j(FWDJL)
    X["compute"] = SRC.j(COMPUTE)
    X["fixv"] = SRC.j(FIXV)
    X["head"] = git("rev-parse", "HEAD").strip()
    X["head7"] = X["head"][:7]
    X["origin"] = git("rev-parse", REMOTE_REF).strip()
    X["origin7"] = X["origin"][:7]
    X["branch"] = git("rev-parse", "--abbrev-ref", "HEAD").strip()
    X["tier_commits"] = tier_commits(X["head"])
    X["contract_sha"] = SRC.sha(CONTRACT)
    if X["contract_sha"] != X["progress"]["contract_of_record"]["sha256"]:
        halt("the contract's sha is not PROGRESS.json's contract_of_record")
    if X["contract_sha"] != X["regs"]["contract"]["sha256"]:
        halt("the contract's sha is not REGISTRATIONS.json's contract pin")
    fam = X["family"]
    order = [r["registration"] for r in fam["rows"]]
    if order != [r["registration"] for r in X["scores"]["rows"]]:
        halt("FAMILY.json and SCORES.json disagree on the registration order")
    if order != [r["registration"] for r in X["regs"]["registrations"]]:
        halt("FAMILY.json and REGISTRATIONS.json disagree on the registration order")
    if len(order) != fam["family_m"]:
        halt("FAMILY.json rows != family_m")
    X["order"] = order
    X["reg_by"] = {r["registration"]: r for r in X["regs"]["registrations"]}
    X["score_by"] = {r["registration"]: r for r in X["scores"]["rows"]}
    X["fam_by"] = {r["registration"]: r for r in fam["rows"]}
    X["lenses"] = list(LENSES)
    # TC10's CLOSE state (read-only): its report in exchange/reports AND its STATUS block on LEDGER_APOLLO
    X["tc10_closed"] = (ROOT / TC10_DOC).exists() and bool(TC10_HDR_RE.search(SRC.t(LEDGER_APOLLO)))
    return X


def lens_span(ks: list[str]) -> str:
    """'5m–1d' for a leading run of the lens order (a NAME: letter-bearing tokens, no measured digit)."""
    return ks[0] if len(ks) == 1 else f"{ks[0]}–{ks[-1]}"


# ═══════════════════════════════════════════════════════════════ findings — the harvest
def section_items(text: str, heading: str, style: str, stop: str | None = None) -> list[str]:
    """The items of a list under `heading` in a markdown text.  style: 'bold-bullet' (^- **), 'bullet'
    (^- ), 'numbered' (^N. ), 'fnf' (^**FNF-).  An item runs to the next item start, the stop line
    (a regex matched at a line start) or the section's end.  Items are returned rstripped, verbatim."""
    lines = text.split("\n")
    hs = [i for i, ln in enumerate(lines) if ln.startswith(heading)]
    if len(hs) != 1:
        halt(f"section {heading!r} found {len(hs)} times")
    h = hs[0]
    lvl = heading_level(lines[h]) or 7
    end = len(lines)
    for i in range(h + 1, len(lines)):
        hl = heading_level(lines[i])
        if hl and hl <= lvl:
            end = i
            break
        if stop and re.match(stop, lines[i]):
            end = i
            break
    starts_re = {"bold-bullet": r"^- \*\*", "bullet": r"^- ", "numbered": r"^\d+\. ",
                 "fnf": r"^\*\*FNF-\d+ "}[style]
    starts = [i for i in range(h + 1, end) if re.match(starts_re, lines[i])]
    items = []
    for k, s in enumerate(starts):
        e = starts[k + 1] if k + 1 < len(starts) else end
        items.append("\n".join(lines[s:e]).rstrip())
    return items


def review_report(lens: str) -> str:
    hits = [r for r in SRC.j(FINAL)["result"]["reviews"] if r["lens"] == lens]
    if len(hits) != 1:
        halt(f"FINAL_REVIEW: lens {lens} found {len(hits)} times")
    return hits[0]["report"]


def harvest_text(src: dict) -> str:
    """Re-extract a harvested text from its locator (the same law F-FNF re-runs)."""
    if src.get("field"):
        base = LA.resolve(SRC.j(src["path"]), src["field"])
    else:
        base = SRC.t(src["path"])
    if src["how"] == "item":
        items = section_items(base, src["section"], src["style"], src.get("stop"))
        if not (1 <= src["item"] <= len(items)):
            halt(f"{src['path']} {src['section']!r}: item {src['item']} of {len(items)}")
        return items[src["item"] - 1]
    if src["how"] == "line":
        hits = [ln for ln in base.split("\n") if ln.startswith(src["prefix"])]
        if len(hits) != 1:
            halt(f"{src['path']}: line prefix {src['prefix']!r} found {len(hits)} times")
        return hits[0].rstrip()
    halt(f"unknown harvest locator {src}")


# The harvest spec — curated: (id, owner, owner reading, primary source, [also-reported-by sources]).
# Sources are LOCATORS, never texts: every text is re-extracted from its file on every run.
def _rev(lens, section, style, item, stop=None):
    return {"path": FINAL, "field": f"result.reviews[lens={lens}].report", "how": "item",
            "section": section, "style": style, "item": item, **({"stop": stop} if stop else {})}


def _md(path, section, style, item, stop=None):
    return {"path": path, "how": "item", "section": section, "style": style, "item": item,
            **({"stop": stop} if stop else {})}


def _line(path, prefix, field=None):
    return {"path": path, "how": "line", "prefix": prefix, **({"field": field} if field else {})}


TRD = ("## Findings-not-fixed for the build doc (ranked)", "fnf", r"^My scratch")
STA = ("## Findings-not-fixed candidates for the build doc (facts, not defects)", "numbered")
FID = ("## Findings-not-fixed candidates (facts for the operator, not defects)", "bold-bullet")
CAU = ("### Findings-not-fixed candidates for the build doc (facts, not defects)", "numbered", r"^My scratch")
REP = ("## Findings-not-fixed candidates for the build doc", "bullet")
FXV = ("## 6. Remaining defects", "bold-bullet")


def trd(k):
    return _rev("trading", TRD[0], TRD[1], k, TRD[2])


def sta(k):
    return _rev("statistics", STA[0], STA[1], k)


def fid(k):
    return _rev("fidelity", FID[0], FID[1], k)


def cau(k):
    return _rev("causality", CAU[0], CAU[1], k, CAU[2])


def rep(k):
    return _rev("reproducibility", REP[0], REP[1], k)


def fxv(k):
    return {"path": FIXV, "field": "verify", "how": "item", "section": FXV[0], "style": FXV[1], "item": k,
            "stop": r"^I checked the fixer's other claims"}


SR_F = "## Findings not fixed (for the operator) [L-R.4]"
TB_F = "## 10 · Findings (disclosures, not fixed; no rule was changed after a number was seen)"
A_F = "## 10 · Findings (derived in-build; findings-not-fixed for the build doc)"
H_F = "## 9 · Findings (stage-intrinsic, derived from the tables above)"
S_F = "## 6 · Not built, and why"

OPB_TRD = "the trading reviewer's own owner tag on the item"
OPB_FACT = "a fact for the operator to weigh (the report's own section heading: facts, not defects); no code change is owed"
EXB_FIX = "a fixture / label / code gap the executor can close in a later wave; it moves no registered number"

HARVEST = [
    # ── the trading lens's ranked list first (FNF-1..17), each with the duplicates it absorbs
    ("FN-TRD-01", "operator", OPB_TRD, trd(1), []),
    ("FN-TRD-02", "operator", OPB_TRD, trd(2), [fid(3)]),
    ("FN-TRD-03", "operator", OPB_TRD, trd(3), [sta(1), fid(6)]),
    ("FN-TRD-04", "operator", OPB_TRD, trd(4), [sta(4)]),
    ("FN-TRD-05", "operator", OPB_TRD, trd(5), [sta(5)]),
    ("FN-TRD-06", "operator", OPB_TRD, trd(6), []),
    ("FN-TRD-07", "operator", OPB_TRD, trd(7), []),
    ("FN-TRD-08", "operator", OPB_TRD, trd(8), []),
    ("FN-TRD-09", "operator", OPB_TRD, trd(9), []),
    ("FN-TRD-10", "operator", OPB_TRD, trd(10), [sta(9)]),
    ("FN-TRD-11", "operator", OPB_TRD, trd(11), []),
    ("FN-TRD-12", "operator", OPB_TRD, trd(12), [fid(5), _md(TBRK, TB_F, "bullet", 1)]),
    ("FN-TRD-14", "operator", OPB_TRD, trd(14), []),
    ("FN-TRD-15", "operator", OPB_TRD, trd(15), [sta(3), sta(6)]),
    ("FN-TRD-16", "operator", OPB_TRD, trd(16), [fid(9), cau(7), _line(FWDMD, "LIMIT (finding, not fixed):"),
                                                _line(TREL, "LIMIT (finding, not fixed):")]),
    ("FN-TRD-17", "operator", OPB_TRD, trd(17), [_md(STAGE_R, SR_F, "bullet", 1)]),
    # ── the other four lenses' candidates (statistics, fidelity, causality, reproducibility)
    ("FN-STA-2", "operator", OPB_FACT, sta(2), [fid(4)]),
    ("FN-STA-8", "operator", OPB_FACT, sta(8), [fid(8)]),
    ("FN-FID-1", "operator", OPB_FACT, fid(1), [_md(SMD, S_F, "bold-bullet", 4)]),
    ("FN-FID-7", "operator", OPB_FACT, fid(7), [_md(AMD, A_F, "bullet", 4)]),
    ("FN-FID-10", "operator", OPB_FACT, fid(10), []),
    ("FN-FID-11", "operator", OPB_FACT, fid(11), []),
    ("FN-FID-12", "operator", OPB_FACT, fid(12), []),
    ("FN-CAU-2", "operator", OPB_FACT, cau(2), [_md(TBRK, TB_F, "bullet", 6)]),
    ("FN-CAU-6", "operator", OPB_FACT, cau(6), []),
    ("FN-REP-3", "operator", OPB_FACT, rep(3), []),
    # ── the stage reports' own findings (operator-facing)
    ("FN-STG-R-3", "operator", OPB_FACT, _md(STAGE_R, SR_F, "bullet", 3),
     [_md(TBRK, TB_F, "bullet", 3), _md(AMD, A_F, "bullet", 6), _md(HMD, H_F, "bullet", 5)]),
    ("FN-STG-A-8", "operator", OPB_FACT, _md(AMD, A_F, "bullet", 10), [_md(AMD, A_F, "bullet", 11)]),
    # ── TC10's still-open question and the SAIL hold, harvested
    ("FN-H-TC10-Q2", "operator", "an operator question TC10 left open; the executor may not answer it",
     _line(LEANS, "- TC10's operator question Q2"), []),
    ("FN-H-SAIL", "operator", "SAIL is the operator's act; the contract holds it", _line(CONTRACT, " (m=9; SAIL still HELD"), []),
    # ── executor-owned
    ("FN-TRD-13", "executor", OPB_TRD, trd(13), [fid(2), sta(7)]),
    ("FN-CAU-1", "executor", EXB_FIX, cau(1), []),
    ("FN-CAU-3", "executor", EXB_FIX, cau(3), [_md(AMD, A_F, "bullet", 1), _md(STAGE_R, SR_F, "bullet", 4)]),
    ("FN-CAU-4", "executor", EXB_FIX, cau(4), [_md(AMD, A_F, "bullet", 8), _md(AMD, A_F, "bullet", 9)]),
    ("FN-CAU-5", "executor", EXB_FIX, cau(5), []),
    ("FN-REP-2", "executor", EXB_FIX, rep(2), [_md(HMD, H_F, "bullet", 2)]),
    ("FN-REP-5", "executor", EXB_FIX, rep(5), []),
    ("FN-FIX-A", "executor", EXB_FIX, fxv(1), []),
    ("FN-FIX-B", "executor", EXB_FIX, fxv(2), []),
    ("FN-FIX-C", "executor", EXB_FIX, fxv(3), []),
    ("FN-FIX-D", "executor", EXB_FIX, fxv(4), []),
    ("FN-FIX-E", "executor", EXB_FIX, fxv(5), []),
    ("FN-FIX-F", "executor", EXB_FIX, fxv(6), []),
    ("FN-STG-R-2", "executor", EXB_FIX, _md(STAGE_R, SR_F, "bullet", 2), []),
    ("FN-STG-TB-2", "executor", EXB_FIX, _md(TBRK, TB_F, "bullet", 2), []),
    ("FN-STG-TB-4", "executor", EXB_FIX, _md(TBRK, TB_F, "bullet", 4), []),
    ("FN-STG-TB-5", "executor", EXB_FIX, _md(TBRK, TB_F, "bullet", 5), []),
    ("FN-STG-TB-7", "executor", EXB_FIX, _md(TBRK, TB_F, "bullet", 7), []),
    ("FN-STG-A-2", "executor", EXB_FIX, _md(AMD, A_F, "bullet", 2), [_md(AMD, A_F, "bullet", 3)]),
    ("FN-STG-A-4", "executor", EXB_FIX, _md(AMD, A_F, "bullet", 5), []),
    ("FN-STG-A-6", "executor", EXB_FIX, _md(AMD, A_F, "bullet", 7), [_md(HMD, H_F, "bullet", 6)]),
    ("FN-STG-H-1", "executor", EXB_FIX, _md(HMD, H_F, "bullet", 1), []),
    ("FN-STG-H-3", "executor", EXB_FIX, _md(HMD, H_F, "bullet", 3), []),
    ("FN-STG-H-4", "executor", EXB_FIX, _md(HMD, H_F, "bullet", 4), []),
]
# harvested, then superseded by a later record (listed, not counted as findings-not-fixed)
SUPERSEDED = [
    ("SUP-REP-1", rep(1), "the TC11-FIX wave fixed it: env/data run in a review worktree (MAJOR-2 of that wave)",
     {"path": FIXV, "field": "fix", "needle": "**MAJOR-2** (env suite fails in a review worktree) | Fixed"}),
    ("SUP-REP-4", rep(4), "the uncommitted edits were committed in the TC11-FIX commit and re-attested GREEN at it",
     {"path": f"{ATTEST}/fix-head.json", "field": "verdict", "needle": "GREEN"}),
    ("SUP-FIX-MAJOR-3", {"path": FIXV, "field": "verify", "how": "line",
                         "prefix": "**MAJOR-3 (open, orchestrator's file): PROGRESS.json has not been refreshed.**"},
     "PROGRESS.json was refreshed in the TC11-FIX commit; the fix-head attestation reads it GREEN with no open finding",
     {"path": f"{ATTEST}/fix-head.json", "field": "verdict", "needle": "GREEN"}),
]


def build_findings(X: dict) -> dict:
    T.region = "s5"
    F = []
    seen_locators = set()
    for fid_, owner, basis, src, also in HARVEST:
        text = harvest_text(src)
        key = json.dumps(src, sort_keys=True)
        if key in seen_locators:
            halt(f"{fid_}: a locator harvested twice")
        seen_locators.add(key)
        also_rows = []
        for a in also:
            ak = json.dumps(a, sort_keys=True)
            if ak in seen_locators:
                halt(f"{fid_}: an also-reported locator harvested twice")
            seen_locators.add(ak)
            also_rows.append({"source": a, "text": harvest_text(a)})
        rc = None
        m = re.match(r"^\*\*FNF-\d+ · ([A-Z +]+) · (operator|executor)\.\*\*", text)
        if m:
            rc = m.group(1)
            if m.group(2) != owner:
                halt(f"{fid_}: owner {owner} is not the reviewer's own tag {m.group(2)}")
        F.append({"id": fid_, "class": "HARVESTED", "owner": owner,
                  "owner_basis": {"path": src["path"], "field": src.get("field"),
                                  "quote": (m.group(0) if m else text.split("\n", 1)[0][:160]),
                                  "reading": basis},
                  "source": src, "status": "REPORTED, NOT FIXED", "text": text, "text_form": "verbatim string",
                  **({"reviewer_class": rc} if rc else {}), "also_reported_by": also_rows})
    # ── MEASURED at build time (rendered from values read this run; every number traced)
    F.extend(measured_findings(X))
    # ── LEANS: this CLOSE's own operationalisations
    F.extend(lean_findings())
    ops = [f for f in F if f["owner"] == "operator"]
    exs = [f for f in F if f["owner"] == "executor"]
    F = ops + exs
    for i, f in enumerate(F, 1):
        f["rank"] = i
    ids = [f["id"] for f in F]
    if len(ids) != len(set(ids)):
        halt("finding ids are not unique")
    sup = []
    for sid, src, why, later in SUPERSEDED:
        lv = LA.resolve(SRC.j(later["path"]), later["field"])
        if later["needle"] not in str(lv):
            halt(f"{sid}: the later record does not read {later['needle']!r}")
        sup.append({"id": sid, "source": src, "text": harvest_text(src), "superseded_because": why,
                    "later_record": later})
    counts = {}
    for c in ("HARVESTED", "MEASURED", "LEAN"):
        row = {o: sum(1 for f in F if f["class"] == c and f["owner"] == o) for o in ("operator", "executor")}
        row["total"] = row["operator"] + row["executor"]
        counts[c] = row
    counts["all"] = {o: sum(1 for f in F if f["owner"] == o) for o in ("operator", "executor")}
    counts["all"]["total"] = len(F)
    ln = find_heading(CONTRACT, " (m=9; SAIL still HELD")
    return {
        "schema": "tierc11.close.S5_FINDINGS_NOT_FIXED.v1",
        "label": "REPORT-ONLY · Tier-E — findings harvested verbatim, measured at build time, or leaned by this "
                 "CLOSE; nothing here is scored, no verdict is read to choose anything, and nothing is fixed.",
        "status_law": "every finding's status is 'REPORTED, NOT FIXED': it records what THIS build did (report, "
                      "never fix); it does not claim the item is still open",
        "ranking_law": "operator-owned first, then executor-owned; within each owner the order of harvest: the "
                       "trading lens's FNF list in its own rank, then the statistics, fidelity, causality and "
                       "reproducibility candidates, the TC11-FIX verifier's residuals, the stage reports' own "
                       "findings, TC10's open question and the SAIL hold, then the measured items and this "
                       "CLOSE's leans",
        "dedup_law": "a fact reported by several sources is ONE finding: the first source in ranking order is the "
                     "primary and keeps its verbatim text; every other source is listed under also_reported_by "
                     "with its own verbatim text",
        "tier": X["progress"]["tier"],
        "as_of_of_record": X["progress"]["as_of_of_record"],
        "contract": {"path": CONTRACT, "sha256": X["contract_sha"],
                     "clause": {"line": ln - 1, "text": SRC.lines(CONTRACT)[ln - 2]}},
        "built_by": GENERATOR_SCRIPT,
        "counts": counts,
        "findings": F,
        "superseded": sup,
    }


def measured_findings(X: dict) -> list[dict]:
    out = []
    head = X["head"]
    # M-1 · MINOR-9: SCORES.json leaves between the reviewed commit and the fix commit
    rev_commit = SRC.j(f"{ATTEST}/trading.json")["commit"]
    a = leaves(json.loads(git("show", f"{rev_commit}:{SCORES}")))
    b = leaves(json.loads(git("show", f"{head}:{SCORES}")))
    changed = sorted(k for k in set(a) & set(b) if a[k] != b[k])
    MEAS["scores_leaves"] = {"reviewed_commit": rev_commit, "fix_commit": head, "changed_keys": changed}
    lv = lambda st: T(f"meas.scores.{st}", GIT("json_leaves", head, rev_commit, path=SCORES, stat=st), "int")  # noqa: E731
    t = (f"SCORES.json between the reviewed commit {rev_commit[:7]} (the lens reviews) and HEAD {head[:7]}: "
         f"{lv('added')} leaves added, {lv('removed')} removed, {lv('changed')} changed — each changed leaf a "
         f"string label ({', '.join(changed)}); {lv('changed_non_string')} numeric, bool or null leaf moved. The "
         f"TC11-FIX verifier filed the additions as MINOR-9, awaiting the operator's ruling (TC11_FIX_VERIFY.json "
         f"verify).")
    out.append(_meas("FN-M-SCORES-LEAVES", "operator",
                     "an operator ruling is pending (MINOR-9); the executor may not rule on its own record",
                     {"path": SCORES, "field": None, "how": "git show <reviewed>:SCORES.json vs HEAD:SCORES.json, "
                      "leaf by leaf"}, t, [fxv(7)]))
    # M-2 · the parallel tc11x lane vendors the env shim at the pre-AM-1 sha — read at the PINNED commit (the lane
    # branch moves; a later lane commit naming a shim must not move or break this finding)
    if git_rc("cat-file", "-e", f"{TC11X_PIN}^{{commit}}") != 0:
        halt(f"the tc11x lane commit {TC11X_PIN} is not in this repository's object store (FN-M-TC11X-SHIM reads it; "
             "the lane is local, not on origin)")
    x_short, x_s = git("log", "-1", "--format=%h%x09%s", TC11X_PIN).strip().split("\t", 1)
    vm = re.search(r"tc11x_env vendored from ([0-9a-f]+)", x_s)
    if not vm:
        halt(f"the pinned tc11x commit {TC11X_PIN} does not name a vendored shim")
    env_rec = [st for st in X["progress"]["stages"] if st["stage"] == "TC11-ENV"][0]["artifact_shas"]["scripts/tierc11_env.py"]["sha256"]
    env_now = hashlib.sha256((ROOT / "scripts/tierc11_env.py").read_bytes()).hexdigest()
    MEAS["tc11x"] = {"commit": x_short, "vendored_from": vm.group(1), "shim_of_record": env_rec, "shim_now": env_now}
    t = (f"The parallel tc11x lane (commit {x_short}, pinned — it sits on the local branch tierc11x, not on origin: "
         f"\"{x_s[:120]}…\") vendors the env shim from {vm.group(1)} — the pre-AM-1 shim. TC11's committed shim "
         f"scripts/tierc11_env.py is sha256 {env_rec[:16]}… (PROGRESS.json stage TC11-ENV; on disk {env_now[:16]}…). "
         f"The two lanes do not run one shim; this CLOSE read the lane's pinned commit through git only and changed "
         f"nothing there.")
    out.append(_meas("FN-M-TC11X-SHIM", "operator",
                     "a cross-lane alignment the operator orders; the tc11x lane is not this executor's to touch",
                     {"path": f"git:{TC11X_PIN}", "field": None,
                      "how": f"git log -1 {TC11X_PIN} (the pinned commit whose subject names the vendored shim)"},
                     t, []))
    # M-3 · the queue BUILT stamp would move the pinned contract sha
    t = (f"exchange/queue/2026-09-24_TC11_APOLLO.md carries no BUILT line (other queue files do, e.g. "
         f"exchange/queue/2026-09-22_OR2_oracle_rulings_ARGUS.md). Its sha256 {X['contract_sha'][:16]}… is pinned by "
         f"REGISTRATIONS.json contract.sha256, scores/REGISTRY_CHECK.json contract.sha256 and PROGRESS.json "
         f"contract_of_record — stamping BUILT into the file would change those bytes and break every pin. Whether "
         f"to stamp (and re-pin), stamp a sibling file, or leave the contract byte-frozen is the operator's word.")
    if SRC.j(REGCHECK)["contract"]["sha256"] != X["contract_sha"]:
        halt("REGISTRY_CHECK.json does not pin the contract's current sha")
    if not re.search(r"(?m)^BUILT: ", SRC.t("exchange/queue/2026-09-22_OR2_oracle_rulings_ARGUS.md")):
        halt("the OR2 queue file no longer carries a BUILT line")
    if re.search(r"(?m)^BUILT", SRC.t(CONTRACT)):
        halt("the TC11 contract already carries a BUILT line")
    out.append(_meas("FN-M-QUEUE-STAMP", "operator", "queue hygiene and re-pinning are the operator's call",
                     {"path": CONTRACT, "field": None, "how": "grep ^BUILT; the three pins compared"}, t, []))
    # M-4 · TC11's CLOSE is ordered after TC10's (a dated fact: the state at draft time, and the law that holds)
    tc10_doc = (ROOT / TC10_DOC).exists()
    tc10_hdr = bool(TC10_HDR_RE.search(SRC.t(LEDGER_APOLLO)))
    MEAS["tc10_close"] = {"doc_exists": tc10_doc, "ledger_has_tc10": tc10_hdr}
    if not X["tc10_closed"]:
        t = (f"At draft time (HEAD {head[:7]}) TC10's CLOSE had not run: {TC10_DOC} existed: "
             f"{'yes' if tc10_doc else 'no'}; {LEDGER_APOLLO} carried a TIER-C10 STATUS block: "
             f"{'yes' if tc10_hdr else 'no'}. TC11's close_acts.sh step 0 STOPS until TC10's report is tracked and its "
             f"STATUS block committed (\"run {TC10_ACTS} first (the ledger keeps tier order)\"); F-CLOSE-ORDER proves "
             f"each stop in a sandbox clone.")
        out.append(_meas("FN-M-TC10-FIRST", "operator", "the operator runs both close scripts, TC10's first",
                         {"path": TC10_DOC, "field": None, "how": "path exists; ledger header grep"}, t, []))
    # M-7 · TC10's own close_acts.sh stops at its step 6: `git add` without -f on paths under an ignored directory
    acts = SRC.lines(TC10_ACTS)
    adds = [(n, ln) for n, ln in enumerate(acts, 1) if re.match(r"^git add (?!-f)", ln)]
    if len(adds) != 1:
        halt(f"{TC10_ACTS}: {len(adds)} bare 'git add' lines (exactly one is expected: its step 6)")
    add_n, add_ln = adds[0]
    names = re.findall(r'"\$([A-Z_]+)"', add_ln)
    assign = {m.group(1): m.group(2) for ln in acts for m in [re.match(r"^([A-Z_]+)=(\S+)$", ln)] if m}
    if not names or any(nm not in assign for nm in names):
        halt(f"{TC10_ACTS}:{add_n}: the added variables {names} are not all assigned in the script")
    def step_of(n: int) -> str:
        s = [k for k, ln in enumerate(acts, 1) if k < n and ln.startswith("STEP=")][-1]
        return re.match(r"^STEP=(\d+)", acts[s - 1]).group(1)
    step_word = step_of(add_n)
    app_ln = [n for n, ln in enumerate(acts, 1) if re.match(r'^cat "\$APP" >> "\$LEDGER"', ln)]
    if len(app_ln) != 1 or app_ln[0] > add_n:
        halt(f"{TC10_ACTS}: the ledger append line is not found once before the bare 'git add'")
    app_step = step_of(app_ln[0])
    pipefail = any(ln.strip() == "set -euo pipefail" for ln in acts)
    ign = {}
    for nm in names:
        p = assign[nm]
        r = subprocess.run(["git", "-C", str(ROOT), "check-ignore", "-v", "--no-index", "--", p],
                           capture_output=True, text=True)
        if r.returncode != 0:
            halt(f"{p} is not matched by an ignore rule: FN-M-TC10-ACTS-IGNORED would be false")
        src_, line_, pat_ = r.stdout.split("\t")[0].split(":", 2)
        ign[nm] = (p, f"{src_}:{line_}", pat_, git_rc("ls-files", "--error-unmatch", "--", p) == 0)
    rules = sorted({v[1] for v in ign.values()})
    MEAS["tc10_acts_ignored"] = {"line": add_n, "text": add_ln, "step": step_word, "paths": ign}
    acts_tracked = git_rc("ls-files", "--error-unmatch", "--", TC10_ACTS) == 0
    t = (f"TC10's {TC10_ACTS}:{add_n} (its step {step_word}; the script itself "
         f"{'tracked' if acts_tracked else 'untracked and git-ignored: local disk only'}) runs `{add_ln.strip()}` "
         f"without -f"
         f"{' under `set -euo pipefail`' if pipefail else ''}; "
         + "; ".join(f"{nm} = {v[0]} ({'tracked' if v[3] else 'untracked'}) matches `{v[1]}` (`{v[2]}`)"
                     for nm, v in sorted(ign.items()))
         + f". A `git add` naming a path under an ignored directory stages it but exits 1 ('The following paths are "
         f"ignored by one of your .gitignore files'); F-CLOSE-ORDER reproduces the exit in a sandbox clone. So TC10's "
         f"script stops at its step {step_word} after its step {app_step} has appended TC10's block to {LEDGER_APOLLO}, "
         f"before its own residue commit and before publish(): TC10's report is left untracked in exchange/reports/ and "
         f"the ledger uncommitted. TC11's close_acts.sh step 0 then stops on the TC10 gate (report not tracked / "
         f"ledger not committed), naming this finding. The fix (`git add -f` at {TC10_ACTS}:{add_n}, the rule "
         f"{', '.join(rules)} the reason) is in TC10's script, outside this executor's write scope.")
    out.append(_meas("FN-M-TC10-ACTS-IGNORED", "operator",
                     "TC10's close script is outside this executor's write scope; the operator edits it or adds -f by "
                     "hand at its step 6 before running it",
                     {"path": TC10_ACTS, "field": None,
                      "how": "the bare 'git add' line; git check-ignore -v --no-index on each path it adds"}, t, []))
    # M-5 · the fix-head attestation record is untracked
    fx = f"{ATTEST}/fix-head.json"
    tracked = git_rc("ls-files", "--error-unmatch", "--", fx) == 0
    MEAS["fix_head_tracked"] = tracked
    t = (f"{fx} — the attestation of the fix commit {SRC.j(fx)['commit'][:7]} (verdict "
         f"{SRC.j(fx)['verdict']}) — is {'tracked' if tracked else 'NOT tracked'} at HEAD {head[:7]}; until the "
         f"CLOSE commit adds it, it is local disk only. close_acts.sh step 0 requires it committed.")
    out.append(_meas("FN-M-ATTEST-UNTRACKED", "executor", "the CLOSE commit adds it; a bookkeeping act",
                     {"path": fx, "field": None, "how": "git ls-files --error-unmatch"}, t, []))
    # M-6 · publish() will sweep every uncommitted exchange/ edit
    mod = [p for p in git("diff", "--name-only", "--", "exchange").splitlines() if p]
    MEAS["exchange_uncommitted"] = mod
    t = (f"publish() stages ALL of exchange/** (CONVENTIONS §3.4). Uncommitted exchange/ edits at HEAD {head[:7]}: "
         f"{', '.join(mod) if mod else 'none'} — the daily routine's own appended section, which it says the next "
         f"publish carries. TC10's close_acts.sh publish step or TC11's, whichever runs first, will commit it.")
    out.append(_meas("FN-M-EXCHANGE-SWEEP", "operator", "the publish acts are the operator's",
                     {"path": "exchange/", "field": None, "how": "git diff --name-only -- exchange"}, t, []))
    return out


MEAS: dict = {}


def leaves(o, p=""):
    out = {}
    if isinstance(o, dict):
        for k, v in o.items():
            out.update(leaves(v, f"{p}.{k}"))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            out.update(leaves(v, f"{p}[{i}]"))
    else:
        out[p] = o
    return out


def _meas(i, owner, reading, source, text, also) -> dict:
    return {"id": i, "class": "MEASURED", "owner": owner,
            "owner_basis": {"path": source["path"], "field": None, "quote": "", "reading": reading},
            "source": source, "status": "REPORTED, NOT FIXED", "text": text,
            "text_form": "measured — rendered from values read this run",
            "also_reported_by": [{"source": a, "text": harvest_text(a)} for a in also]}


LEANS_CLOSE = [
    ("LEAN-CLOSE-1", "§0.2 is the §0 table of scores/S0_VERDICTS.md copied byte for byte (a verbatim block), never "
                     "re-rendered: the scorer's cell text, labels included, is the record."),
    ("LEAN-CLOSE-2", "§0.1 opens §0 with R5's plain answer in words, its numbers read from the direction tables of "
                     "stage_r/R5_CHOP.md (the tracked twin of the git-ignored R5_CHOP_DIRECTION.parquet; alignment and "
                     "direction-adjusted cells), because the frozen chop table is direction-blind (the trading review's "
                     "D-2); every calibrated read carries its SCALE-IN-SAMPLE count inline; the words decide nothing."),
    ("LEAN-CLOSE-3", "the append's push fact is stated against the refs at draft time (HEAD and origin named by "
                     "sha, ancestry read through git, time-invariant); the live fact after the operator's push "
                     "goes into the one pending stamp, which close_acts.sh fills and F-LAR11 --stamped certifies."),
    ("LEAN-CLOSE-4", "R4's '★ cells' are the contract's three starred L+1 conditions (EXP_ALIGNED*, "
                     "IN_RANGE_COINCIDENT*, IN_RANGE_MID*) at direction 'both', calibrated scale, cell law record, "
                     "each row pointing at the STAGE_R4.md lines it copies; every other cell stays in STAGE_R4.md / "
                     "R4_GRID.parquet."),
    ("LEAN-CLOSE-5", "the BOX-COST rows are the tierc11 commits' paths (b9ed953 included), every PROGRESS.json "
                     "artifact not among them, the CLOSE's own files, the untracked tierc11 files, the two planned "
                     "exchange destinations and the snapshot; files a fixture run rewrites are listed, never sized."),
    ("LEAN-CLOSE-6", "the TC11-FIX verifier's residual MINORs are harvested from close/TC11_FIX_VERIFY.json, a "
                     "verbatim copy of the harness's workflow journal fields, so the harvest reads a file in the repo."),
    ("LEAN-CLOSE-7", "'the nesting grid whole' (contract CLOSE; LAWS 'every grid reported whole') is printed whole in "
                     "§2.3: every line under stage_r/NEST_GRID.md's R3 heading and every line of "
                     "stage_r/lanes/NEST_GRID_LANES.md below its title, in verbatim blocks; the two H2 lines a verbatim "
                     "block may not carry are re-printed as H4 labels. The document stays under the §4.2 per-file cap "
                     "(the generator HALTs over it)."),
    ("LEAN-CLOSE-8", "every sentence about TC10's CLOSE is time-invariant or dated: the append states the step-0 law "
                     "(TC11 follows TC10) rather than TC10's state, and its tier line cites TC10's block on "
                     "LEDGER_APOLLO when that block is there at generation, else TC10's staged file, in words true "
                     "before and after TC10's CLOSE."),
    ("LEAN-CLOSE-9", "the R2 sentences name the lenses the [Q-R3] law closes (every non-provisional FAIL) apart from "
                     "the provisional ones (a count under its floor), which stay the operator's question; the "
                     "generator HALTs if any lens word or maker twin is not FAIL."),
    ("LEAN-CLOSE-10", "F-NUM's coverage law (every digit traced, masked, verified or exempted) binds §0 and the "
                      "append; every other number of the draft is read by the generator from its record "
                      "(PROGRESS.json, the transcripts, the findings, COMPUTE_LEDGER.json, BOX_COST) and the verbatim "
                      "blocks, the R4 ★ table and BOX_COST.json are re-derived by fixtures, but §1.2, §9, §10, §11 "
                      "and §14.3 carry no digit-by-digit coverage check (the close verifier's m5, left open)."),
    ("LEAN-CLOSE-11", "the collar line stands above every table copied from STAGE_W's W2 sections and STAGE_A's "
                      "head-to-head (the blocks are split before each table); tables that carry the collar in their "
                      "own cells (STAGE_G's tier · selection_not_a_result · gates columns) or under a file-level "
                      "collar line copied in the same block (R5_CHOP.md, NEST_GRID.md, NEST_GRID_LANES.md) are "
                      "copied as they stand; registered books ('book, not a verdict') carry none."),
]


def lean_findings() -> list[dict]:
    return [{"id": i, "class": "LEAN", "owner": "executor",
             "owner_basis": {"path": GENERATOR_SCRIPT, "field": None, "quote": "LEANS_CLOSE",
                             "reading": "a lean is the executor's operationalisation; the operator may overrule it"},
             "source": {"path": GENERATOR_SCRIPT, "field": None, "how": "LEANS_CLOSE"},
             "status": "REPORTED, NOT FIXED", "text": "[LEAN-HEPHAESTUS] " + t, "text_form": "lean",
             "also_reported_by": []} for i, t in LEANS_CLOSE]


def render_findings_md(S5: dict) -> str:
    L = ["# TIER-C11 · CLOSE · FINDINGS — REPORTED, NOT FIXED", "",
         f"> **{S5['label']}**", ">", f"> {S5['status_law'][0].upper() + S5['status_law'][1:]}.", "",
         f"- **Contract of record:** `{S5['contract']['path']}` sha256 `{S5['contract']['sha256']}`",
         f"- **Clause:** line {S5['contract']['clause']['line']} — `{S5['contract']['clause']['text'].strip()}`",
         f"- **AS-OF OF RECORD:** {S5['as_of_of_record']}",
         f"- **Ranking law:** {S5['ranking_law']}.",
         f"- **Dedup law:** {S5['dedup_law']}.",
         f"- **Built by:** `{S5['built_by']}`; certified by `{FIXTURES_SCRIPT}` F-FNF (json == md; class, owner and "
         f"source on every finding; ids unique; every harvested text re-extracted from its locator).", "",
         "## 0 · Inputs, read-only", "", "| input | bytes | sha256 |", "|---|---:|---|"]
    for rel in sorted(S5["inputs"]):
        v = S5["inputs"][rel]
        L.append(f"| `{rel}` | {v['bytes']} | `{v['sha256']}` |")
    L += ["", "## 1 · Counts and index", "", "| class | operator | executor | total |", "|---|---:|---:|---:|"]
    for c in ("HARVESTED", "MEASURED", "LEAN", "all"):
        r = S5["counts"][c]
        L.append(f"| {c} | {r['operator']} | {r['executor']} | {r['total']} |")
    L += ["", "| rank | id | class | owner | source | locator |", "|---:|---|---|---|---|---|"]
    for f in S5["findings"]:
        L.append(f"| {f['rank']} | `{f['id']}` | {f['class']} | {f['owner']} | `{f['source']['path']}` | "
                 f"{locator_str(f['source'])} |")
    L += ["", "## 2 · The findings, ranked — operator-owned first", ""]
    for f in S5["findings"]:
        L += [f"#### {f['id']}", "",
              f"- **{f['class']}** · owner **{f['owner']}** · status **{f['status']}** · rank {f['rank']}"
              + (f" · the reviewer's class {f['reviewer_class']}" if f.get("reviewer_class") else ""),
              f"- source: `{f['source']['path']}` · {locator_str(f['source'])}",
              f"- owner basis: {f['owner_basis']['reading']}", "", "~~~text", f["text"], "~~~", ""]
        for a in f["also_reported_by"]:
            L += [f"- also reported by: `{a['source']['path']}` · {locator_str(a['source'])}", "", "~~~text",
                  a["text"], "~~~", ""]
    L += ["## 3 · Harvested, then superseded by a later record — listed, not counted", ""]
    for s in S5["superseded"]:
        L += [f"#### {s['id']}", "", f"- source: `{s['source']['path']}` · {locator_str(s['source'])}",
              f"- superseded because: {s['superseded_because']} (`{s['later_record']['path']}` "
              f"{s['later_record']['field']} reads {s['later_record']['needle']!r})", "", "~~~text", s["text"], "~~~", ""]
    L += ["## 4 · What this document is not", "",
          "- Not a fix list: nothing here was fixed by the CLOSE, and no registered number moved.",
          "- Not a verdict: no finding changes a row of §0; the verdicts are the scorer's (scores/S0_VERDICTS.md).",
          "- Not a promotion: a candidate for a new registration named here is post hoc and is the operator's to "
          "order or refuse.", ""]
    return "\n".join(L)


def locator_str(s: dict) -> str:
    fld = f"`{s['field']}` · " if s.get("field") else ""
    if s.get("how") == "item":
        return f"{fld}{s['style']} item {s['item']} under `{s['section']}`"
    if s.get("how") == "line":
        return f"{fld}the line starting `{s['prefix'].strip()}`"
    return str(s.get("how", ""))


# ═══════════════════════════════════════════════════════════════ the LEDGER append
def wrapq(indent: int, path: str, l1: int, l2: int, text: str) -> list[str]:
    return LA.render_quote(indent, {"path": path, "l1": l1, "l2": l2, "sel": None, "text": text})


def jq(indent: int, path: str, sel: str, text: str) -> list[str]:
    return LA.render_quote(indent, {"path": path, "l1": None, "l2": None, "sel": sel, "text": text})


def line_quote(indent: int, path: str, prefix: str, sub: str | None = None) -> list[str]:
    n = find_heading(path, prefix)
    ln = SRC.lines(path)[n - 1]
    text = sub if sub is not None else ln
    if text not in ln:
        halt(f"{path}:{n}: quote {text[:40]!r} not on the line")
    return wrapq(indent, path, n, n, text)


def lines_quote(indent: int, path: str, l1: int, l2: int) -> list[str]:
    L = SRC.lines(path)
    return wrapq(indent, path, l1, l2, "\n".join(L[l1 - 1:l2]))


def render_append(X: dict) -> str:
    T.region = "append"
    fam = X["family"]
    Lc = SRC.lines(CONTRACT)
    title = Lc[0].split(" · ", 1)[1]
    main, sub = title.split(" — ", 1)
    header_title = f"{main}: {sub.upper()}"
    date = T("append.date", GIT("date", X["head"]), "date")
    m = T("fam.m", JS(FAMILY, "family_m"), "int")
    q = T("fam.q", JS(FAMILY, "family_q"), "str")
    bar = T("fam.bar", JS(FAMILY, "bar_filed"), "f6")
    barx = T("fam.bar_exact", JS(FAMILY, "bar_exact"), "str")
    spent = T("fam.spent", JS(FAMILY, "tests_spent"), "int")
    seed = T("progress.seed", JS(PROGRESS, "seed"), "int")
    asof = T("progress.asof", JS(PROGRESS, "as_of_of_record"), "str")
    snap = T("progress.substrate", JS(PROGRESS, "substrate"), "str")
    L: list[str] = []
    a = L.append
    a(f"=== STATUS_APOLLO — {date} — {X['progress']['tier']} · {header_title} ===")
    a(f"LANE      APOLLO (drafted) · HEPHAESTUS (executor) · branch {X['branch']} · seed {seed}")
    a("CLASS     NINE REGISTRATIONS, ONE FAMILY, TEXT FROZEN AT STEP Q AND FILED")
    a(f"          BEFORE ANY TC11 BOOK (registry head {X['regs']['head'][:8]}…, REGISTRY_PIN.json).")
    a(f"          m = {m}, one fixed bar q/m = {q}/{T('fam.m', JS(FAMILY, 'family_m'), 'int')} = {bar} ({barx});")
    a(f"          {spent} tests spent — P-SCALP-2 was closed by its own R2 precondition and")
    a("          spent none, and fewer tests never loosen the bar (scores/FAMILY.json).")
    a(f"          As-of {asof}, one corridor (snapshot {snap}).")
    a("          Every «cite» below is re-verified against its source by F-LAR11 and")
    a("          every number is traced to its file and field by F-NUM")
    a("          (scripts/tierc11_close_fixtures.py).")
    a("")
    a("  THE FAMILY — ONE, AS FILED:")
    fl = find_heading(CONTRACT, "ONE family, m = ")
    L.extend(wrapq(4, CONTRACT, fl, fl, "ONE family, m = 9 independently-failable hypotheses (bar 0.10/9)"))
    L.extend(jq(4, FAMILY, "law", "a registration closed by its own precondition or condition spends no test "
                                  "and never loosens the bar"))
    a("")
    a("  SAIL · STILL HELD.")
    L.extend(line_quote(4, CONTRACT, " (m=9; SAIL still HELD", "(m=9; SAIL still HELD; the forward ledger opened)"))
    l2 = find_heading(TC10_CONTRACT, "RATIFIED: operator 2026-09-21")
    L.extend(wrapq(4, TC10_CONTRACT, l2, l2 + 1, "Q6 SAIL spec HELD\nuntil TC10 autopsied"))
    a("    Held. Nothing in this tier is a SAIL act; the one SUPPORTED row below is")
    a("    an in-sample re-score, not confirmation, and no card change is proposed.")
    a("")
    a("  VERDICTS, each under its own text (the contract's lines, sliced by")
    a("  REGISTRATIONS.json text_lines) with its verdict cell and labels")
    a("  (scores/SCORES.json rows[].verdict_cell) and its numbers (rows[].stats):")
    for reg in X["order"]:
        r = X["reg_by"][reg]
        sr = X["score_by"][reg]
        a(f"    {reg}")
        L.extend(lines_quote(6, CONTRACT, r["text_lines"][0], r["text_lines"][1]))
        L.extend(jq(6, SCORES, f"rows[registration={reg}].verdict_cell", sr["verdict_cell"]))
        if sr["stats"] is not None:
            b = f"rows[registration={reg}]"
            n = T(f"{reg}.n", JS(SCORES, f"{b}.stats.main.n"), "int")
            if sr["stats"]["main"].get("n_base") is None:
                nbs = "vs zero"
            else:
                nbs = f"base {T(f'{reg}.n_base', JS(SCORES, f'{b}.stats.main.n_base'), 'int')}, {sr['ruler']}"
            pt = T(f"{reg}.point", JS(SCORES, f"{b}.stats.main.point"), "f4s")
            lo = T(f"{reg}.lo", JS(SCORES, f"{b}.stats.main.lo"), "f4s")
            hi = T(f"{reg}.hi", JS(SCORES, f"{b}.stats.main.hi"), "f4s")
            p = T(f"{reg}.p", JS(SCORES, f"{b}.stats.main.p_one_sided"), "f6")
            cb = "yes" if X["fam_by"][reg]["clears_bar"] else "no"
            a(f"      n {n} ({nbs}) · point {pt} R · CI [{lo}, {hi}] · p {p} · clears bar: {cb}")
        else:
            a("      no number, no slot spent (FAMILY.json spent_test false).")
    a("")
    span, prov = lens_span(X["r2_closed"]), X["r2_prov"]
    a(f"  RANGE TRADING — THE R2 LAW CLOSES IT ON {span}"
      + (f"; {', '.join(prov)} FAIL IS PROVISIONAL (Q4):" if prov else ":"))
    L.extend(lines_quote(4, CONTRACT, find_heading(CONTRACT, " R2 FEASIBILITY GATE PER LENS"),
                         find_heading(CONTRACT, " R2 FEASIBILITY GATE PER LENS") + 2))
    L.extend(line_quote(4, STAGE_R, "- The lens verdicts of record per lens:"))
    makers = sorted({X["r2"]["lenses"][k]["maker_twin"].split(" ")[0] for k in X["lenses"]})
    if makers != ["FAIL"]:
        halt(f"a maker twin reads {makers}: the 'the maker twin fails too' sentence would be false")
    words, protect = r2_prose(X)
    for ln in wrap_prose(words, 4, "", protect=protect):
        a(ln)
    a("")
    a("  THE FORWARD LEDGER — OPENED, STANDING, UNSCORED:")
    L.extend(line_quote(4, FWDMD, "opening ", "opening 2026-09-21T16:00:00Z (entry close must be after it)"))
    L.extend(line_quote(4, FWDMD, "**Standing and UNSCORED",
                        "**Standing and UNSCORED until each book's own n >= 30.** No CI, no p, no verdict."))
    v6c = X["fwd"][1]["books"]["v6"]["continuations_not_admitted"]
    o9 = X["fwd"][1]["books"]["trg912"]["open"]
    if len(v6c) != 1 or len(o9) != 1 or X["fwd"][1]["books"]["v6"]["open"] or X["fwd"][1]["books"]["trg912"]["continuations_not_admitted"]:
        halt("the forward ledger's open / continuation lists are not the one each the append describes")
    nv6 = T("fwd.v6.n", JL(FWDJL, 1, "books.v6.n_appended_total"), "int")
    n912 = T("fwd.912.n", JL(FWDJL, 1, "books.trg912.n_appended_total"), "int")
    nsc = T("fwd.n_score", JL(FWDJL, 0, "n_score"), "int")
    c_sym = T("fwd.v6.cont.sym", JL(FWDJL, 1, "books.v6.continuations_not_admitted[0].key[0]"), "str")
    c_ent = T("fwd.v6.cont.entry", JL(FWDJL, 1, "books.v6.continuations_not_admitted[0].key[1]"), "iso_ms")
    c_net = T("fwd.v6.cont.net", JL(FWDJL, 1, "books.v6.continuations_not_admitted[0].net_r"), "f6s")
    o_sym = T("fwd.912.open.sym", JL(FWDJL, 1, "books.trg912.open[0].key[0]"), "str")
    o_ent = T("fwd.912.open.entry", JL(FWDJL, 1, "books.trg912.open[0].key[1]"), "iso_ms")
    o_mk = T("fwd.912.open.mark", JL(FWDJL, 1, "books.trg912.open[0].net_r_marked_to_pin"), "f6s")
    pin = T("fwd.pin", JL(FWDJL, 1, "pin_iso"), "str")
    a(f"    base v6: n {nv6} appended; the continuation {c_sym} long entered {c_ent}")
    a(f"      (at or before the opening) is listed, not counted: stop {c_net} R.")
    a(f"    frozen {T.ex('9/12', 'the frozen 9/12 book: a trigger-pair NAME (contract :58), not a measured value')}: "
      f"n {n912} appended; OPEN at the pin {pin}: {o_sym} long entered")
    a(f"      {o_ent}, marked {o_mk} R, listed, not counted.")
    a(f"    Each book stays UNSCORED until its own n >= {nsc}. A refresh past the pin needs")
    a("    the foundation re-rooted on a new snapshot + pin record:")
    L.extend(line_quote(6, FWDMD, "LIMIT (finding, not fixed):",
                        "a refresh on bars after 2026-09-25T00:00Z needs the foundation re-rooted"))
    a("")
    a("  THE PUSH FACT (git, read at draft time):")
    h7 = T("git.head7", GIT("short", X["head"]), "str")
    o7 = T("git.origin7", GIT("short", X["origin"]), "str")
    osub = T("git.origin.subject", GIT("subject", X["origin"]), "str")
    odate = T("git.origin.date", GIT("date", X["origin"]), "str")
    ntot = T("git.tier.count", GIT("tierc11_count_in", X["head"]), "int")
    non = T("git.tier.on_origin", GIT("tierc11_count_ancestor_of", X["head"], X["origin"]), "int")
    noff = T("git.tier.not_on_origin", GIT("tierc11_not_ancestor_of", X["head"], X["origin"]), "str")
    a(f"    The operator's daily publish {o7} (\"{osub}\",")
    a(f"    committed {odate}) pushed the branch:")
    a(f"    {REMOTE_REF} = {T('git.origin7', GIT('short', X['origin']), 'str')}.")
    a(f"    At HEAD {h7}: {non} of the {ntot} tierc11 commits are on origin; not on")
    a(f"    origin: {noff}.")
    for ln in wrap_prose(TC10_LAW_APPEND, 4, ""):
        a(ln)
    a(f"    - Commits and remote at CLOSE: {STAMP_TEXT}.")
    a("")
    a("  ALSO FILED")
    c = lambda cell, col, f: T(f"r5d.{cell}.{col}", r5cell(cell, col), f)   # noqa: E731
    ali, fro = "calibrated|4h|alignment|IN_RANGE", "frozen3.0|4h|alignment|IN_RANGE"
    r5 = (f"R5 ({COLLAR}): v6 is not killed in chop at entry — in-range 4h entries net positive, calibrated n "
          f"{c(ali, 'n', 'int')} E {c(ali, 'mean_net_r', 'f4s')} R (SCALE-IN-SAMPLE: {c(ali, 'n_scale_in_sample', 'int')} "
          f"of them read in-sample; holdout slice E {c(ali, 'mean_net_r_holdout', 'f4s')} R), frozen3.0 n "
          f"{c(fro, 'n', 'int')} E {c(fro, 'mean_net_r', 'f4s')} R ({R5MD.split('tierc11/', 1)[1]}).")
    for ln in wrap_prose(r5, 4, "- ", protect=[COLLAR]):
        a(ln)
    wn = T("w.cohort.n", TX(WMD, r"^- cohort \(v6 campaigns with an IN-TRADE counter 12/89 1h cross before the \+1R latch\): n (\d+),"), "int")
    wd = T("w.delta", TX(WMD, r"^- delta = mean\(cohort\) − mean\(book\) = (-?\d+\.\d+);"), "str")
    wlo = T("w.lo", TX(WMD, r"^- delta = .*; cluster-90% \[(-?\d+\.\d+), "), "str")
    whi = T("w.hi", TX(WMD, r"^- delta = .*; cluster-90% \[-?\d+\.\d+, (-?\d+\.\d+)\]"), "str")
    a(f"    - P-WARN-1's condition was MET (cohort n {wn}, delta {wd}, cluster")
    a(f"      interval [{wlo}, {whi}]), so its rule was scored, paired — flat.")
    r4n = T("r4.grid.rows", TX(R4MD, r"^\| R4_GRID\.parquet \| (\d+) \|"), "intc")
    a(f"    - R4, the fractal grid, whole: {r4n} rows (stage_r4/R4_GRID.parquet), Tier-E.")
    a("    - Findings not fixed: research_outputs/tierc11/close/S5_FINDINGS_NOT_FIXED.md")
    a("      (BUILD §10).")
    a(f"    - The build document: {DOC}")
    a(f"      (FLAGGED: over the {T('pub.flag', CONST(PUBLISH, 'FLAG_BYTES'), 'intc')} B wire; close/BOX_COST.md).")
    a("")
    a("  INTEGRITY")
    sweep = T("progress.sweep", JS(PROGRESS, "last_sweep_utc", re_in_value=r"\): (\d+ suites, \d+ fixtures GREEN)"), "str")
    a(f"    - Fixture sweep of record: {sweep} (PROGRESS.json last_sweep_utc).")
    a("    - F-CTRL-a, v6 on the TC11 corridor against tierc6:")
    L.extend(line_quote(6, BOOKS_FX, "  [PASS] F-CTRL-a:", "WORST ABS DIFF 0.000e+00 (bar EXACTLY 0.000e+00)"))
    att = sorted(p.name for p in (ROOT / ATTEST).glob("*.json"))
    greens = [n for n in att if SRC.j(f"{ATTEST}/{n}")["verdict"] == "GREEN"]
    if greens != att:
        halt(f"an attestation record is not GREEN: {sorted(set(att) - set(greens))}")
    a("    - Worktree attestations: every record under review/attest/ reads GREEN")
    a(f"      ({', '.join(n[:-5] for n in att)}); the lens reviews at")
    a(f"      {T('att.review.commit', JS(f'{ATTEST}/trading.json', 'commit'), 'sha7')}, "
      f"fix-head at {T('att.fix.commit', JS(f'{ATTEST}/fix-head.json', 'commit'), 'sha7')}.")
    a("")
    a("  OPEN FOR THE OPERATOR (BUILD §11)")
    for qline in open_questions(X, short=True):
        L.extend(wrap_prose(qline, 4, "- ", protect=[T.items[k]["lit"] for k in ("r2.1w.word",)] + ["`git add`"]))
    a("")
    src, tl, te = tc10_tier_line(X)
    if src == LEDGER_APOLLO:
        a("  THE TIER LINE. TC10's block above on this ledger closes on:")
    else:
        for ln in wrap_prose("THE TIER LINE. TC10's block (staged at research_outputs/tierc10/LEDGER_APOLLO_APPEND.md, "
                             "and required on this ledger before this block by close_acts.sh's preconditions) closes "
                             "on:", 2, ""):
            a(ln)
    TL = SRC.lines(src)
    L.extend(wrapq(4, src, tl, te, "\n".join([TL[tl - 1].lstrip()] + TL[tl:te])))
    n_ns = sum(1 for r in fam["rows"] if r["verdict_of_record"].startswith("NOT SUPPORTED"))
    words = {7: "SEVEN"}
    if n_ns not in words:
        halt(f"{n_ns} NOT SUPPORTED rows: the tier line's word would be false")
    if X["progress"]["tier"] != "TIER-C11":
        halt("the tier line names ELEVEN TIERS")
    prov = X["r2_prov"]
    tier = (f"ELEVEN TIERS. ONE IN-SAMPLE RE-SCORE (P-AGE-1, NO NEW CAMPAIGN SINCE THE TC10 PIN) CLEARS ITS OWN BAR; "
            f"{words[n_ns]} SCORED ROWS DO NOT; P-SCALP-2 IS CLOSED BY R2; THE R2 LAW CLOSES RANGE TRADING ON "
            f"{lens_span(X['r2_closed'])}"
            + (f", {', '.join(prov)} PROVISIONAL (Q4)" if prov else "")
            + ". SAIL stays HELD; no card change is proposed.")
    for ln in wrap_prose(tier, 2, ""):
        a(ln)
    a("=== END ===")
    return SEP + "\n".join(L) + "\n"


TC10_LAW_APPEND = ("This block follows TC10's: TC11's close_acts.sh preconditions stop until TC10's report is tracked "
                   "in exchange/reports/ and TC10's STATUS block is committed on this ledger (the ledger keeps tier "
                   "order).")


def tc10_tier_line(X: dict) -> tuple[str, int, int]:
    """(source, first line, last line) of TC10's tier line: its block on LEDGER_APOLLO when TC10's CLOSE has put it
    there, else TC10's staged append."""
    src = LEDGER_APOLLO if X["tc10_closed"] else TC10_APPEND
    TL = SRC.lines(src)
    start = 0
    if src == LEDGER_APOLLO:
        hdr = [i for i, ln in enumerate(TL) if TC10_HDR_RE.match(ln)]
        if len(hdr) != 1:
            halt(f"{LEDGER_APOLLO}: {len(hdr)} TIER-C10 STATUS headers (exactly one is required)")
        start = hdr[0]
    tls = [i for i in range(start, len(TL)) if TL[i].startswith("  TEN TIERS.")]
    if not tls:
        halt(f"{src}: TC10's tier line is not found")
    tl = tls[0] + 1
    te = tl
    while TL[te].strip() != "=== END ===":
        te += 1
    return src, tl, te


def r5cell(cell: str, col: str) -> dict:
    """R5's direction / chop cells, read from the tracked stage_r/R5_CHOP.md tables (never the git-ignored parquet)."""
    sc, lens, kind, bucket = cell.split("|")
    return MDC(R5MD, f"#### {lens} · {sc} · {kind}", bucket, col)


def r2_parts(X: dict) -> dict:
    """Every literal the R2 sentences print, traced (called once per region that prints them)."""
    P = {"span": lens_span(X["r2_closed"]), "prov": []}
    law = r"^Word law: SR-3 THE WORD \[L-R\.4\]: "
    P["floor"] = T("r2.law.floor", TX(STAGE_R, law + r"PASS iff the height leg \(n_ranges >= (\d+),"), "int")
    P["ratio_bar"] = T("r2.law.ratio_bar", TX(STAGE_R, law + r".*?median\(ratio\) >= (\d+\.\d+),"), "str")
    P["net_bar"] = T("r2.law.net_bar", TX(STAGE_R, law + r".*? - round\(toll, 8\) > (\d+)\)"), "str")
    for k in X["r2_prov"]:
        b = f"lenses.{k}"
        word = T(f"r2.{k}.word", JS(R2J, f"{b}.word"), "str")
        floor_w = fmtv("int", resolve(JS(R2J, f"{b}.word", re_in_value=r"n<(\d+)\)")))   # a check, not printed
        if floor_w != P["floor"]:
            halt(f"R2 {k}: the word's floor {floor_w} is not the word law's {P['floor']}")
        under = [(f, T(f"r2.{k}.{f}", JS(R2J, f"{b}.{f}"), "int")) for f in ("n_ranges", "edge_n_ranges", "edge_n")
                 if X["r2"]["lenses"][k][f] < int(P["floor"])]
        if not under:
            halt(f"R2 {k} is provisional but no count sits under the floor")
        P["prov"].append({"lens": k, "word": word, "under": under,
                          "ratio": T(f"r2.{k}.ratio_median", JS(R2J, f"{b}.ratio_median"), "f0"),
                          "net": T(f"r2.{k}.edge_net_h20.f4", JS(R2J, f"{b}.edge_net_h20"), "f4s")})
        v = X["r2"]["lenses"][k]
        if not (v["ratio_median"] >= float(P["ratio_bar"]) and v["edge_net_h20"] > float(P["net_bar"])):
            halt(f"R2 {k}: the 'measured values clear their bars' sentence would be false")
    P["net1h"] = T("r2.1h.net", JS(R2J, "lenses.1h.edge_net_h20"), "f8s")
    P["med1h"] = T("r2.1h.med", JS(R2J, "lenses.1h.edge_median_term_h20"), "f8s")
    P["toll1h"] = T("r2.1h.toll", JS(R2J, "lenses.1h.edge_toll_atr"), "f8")
    return P


def r2_prov_sentence(p: dict, floor: str, ratio_bar: str, net_bar: str) -> str:
    return (f"{p['lens']} reads {p['word']}: its counts sit under the floor ("
            + ", ".join(f"{f} {n}" for f, n in p["under"]) + f" < {floor}) while its measured values clear their bars "
            f"(median height ÷ toll {p['ratio']} ≥ {ratio_bar}; edge net {p['net']} ATR > {net_bar}), so whether it "
            f"closes {p['lens']} is the operator's question (BUILD §11 Q4)")


def r2_prose(X: dict) -> tuple[str, list[str]]:
    P = r2_parts(X)
    t = (f"Under that law a FAIL closes the lens for range trading in this and every later tier unless the toll "
         f"model changes, and the maker twin (the only reopening path) reads FAIL at every record cell "
         f"(R2_LENS_VERDICTS.json lenses[*].maker_twin): range trading is closed on {P['span']}. "
         + "".join(r2_prov_sentence(p, P["floor"], P["ratio_bar"], P["net_bar"]) + ". " for p in P["prov"])
         + f"At 1h the edge leg nets {P['net1h']} ATR (median H20 {P['med1h']} - taker toll {P['toll1h']}): "
         f"Stage S is CLOSED BY R2 (1h: FAIL) and P-SCALP-2 spent no slot.")
    return t, [p["word"] for p in P["prov"]]


def wrap_prose(text: str, indent: int, bullet: str, protect=(), width: int = 78) -> list[str]:
    """Wrap a prose line for the ledger without ever splitting a protected (multi-word) literal."""
    import textwrap
    t = text
    for p in protect:
        t = t.replace(p, p.replace(" ", "\x00"))
    lines = textwrap.wrap(t, width=width - indent - len(bullet), break_long_words=False, break_on_hyphens=False)
    out = []
    for i, ln in enumerate(lines):
        pre = " " * indent + (bullet if i == 0 else " " * len(bullet))
        out.append((pre + ln).replace("\x00", " "))
    return out


def open_questions(X: dict, short: bool) -> list[str]:
    """The questions the records leave for the operator (the same list in the ledger and in §11)."""
    ms = MEAS["scores_leaves"]
    added = T("meas.scores.added", GIT("json_leaves", ms["fix_commit"], ms["reviewed_commit"], path=SCORES,
                                       stat="added"), "int")
    w1 = T("r2.1w.word", JS(R2J, "lenses.1w.word"), "str")
    return [
        f"Q1 · MINOR-9: rule on the {added} SCORES.json leaves added since the lens reviews (none moved) — keep "
        "them, or re-file the scorer's record?",
        "Q2 · The contract's BUILT stamp: stamp it and re-pin REGISTRATIONS.json, REGISTRY_CHECK.json and "
        "PROGRESS.json, or leave the contract byte-frozen?",
        "Q3 · TC10's Q2 (does slippage join the toll of record?) stays open; every TC11 row carries the haircut "
        "twin beside the toll of record, never instead of it.",
        f"Q4 · R2 1w reads {w1}; its counts sit under the floor while its measured values clear their bars. "
        "Accept it as closing 1w for range trading, or order a re-measure when the lens has the ranges?",
        "Q5 · The forward ledger: order the foundation re-rooted on a new snapshot and pin record so it can refresh.",
        f"Q6 · The push and the publish: run TC10's close_acts.sh (its step-{MEAS['tc10_acts_ignored']['step']} "
        "`git add` needs -f: FN-M-TC10-ACTS-IGNORED), then TC11's — both are the operator's acts.",
        "Q7 · The tierc11x lane vendors the pre-AM-1 env shim: align the two lanes, or keep them apart?",
        "Q8 · The post-hoc candidates the reviews name (the relay in the windows v6 enters late; the memory-line "
        "first-hold twin): order a forward registration, or let them lie?",
        "Q9 · Two reading conflicts the fidelity review names (L-W.4 against L-1.4 on Tier-E intervals; L-W.1 read "
        "as less-or-equal): ratify or overrule each.",
    ]


# ═══════════════════════════════════════════════════════════════ the BUILD DRAFT
def md_block(rel: str, heading: str, **kw) -> str:
    l1, l2 = block(rel, heading, **kw)
    return verbatim(rel, l1, l2)


def md_table_after(rel: str, prefix: str) -> str:
    l1, l2 = table_after_line(rel, prefix)
    return verbatim(rel, l1, l2)


def render_draft(X: dict, append_text: str, S5: dict, s5_md: bytes, flagged: bool) -> str:
    L: list[str] = []
    a = L.append
    pr = X["progress"]
    T.region = "doc"
    title = SRC.lines(CONTRACT)[0]
    a(f"# BUILD — {title}")
    a("")
    a(f"> **DRAFT.** This document lives at `{OUT_DRAFT}` and moves to `{DOC}` **only at CLOSE** (LAW 5: a draft "
      "under `exchange/` is not a draft). The operator's `research_outputs/tierc11/close/close_acts.sh` moves it, "
      "sha-checked across the copy. Generated by `scripts/tierc11_close.py`; certified by "
      "`scripts/tierc11_close_fixtures.py`.")
    a("")
    csha = T("contract.sha", FILESHA(CONTRACT), "str")
    cb = T("contract.bytes", FILEB(CONTRACT), "intc")
    a(f"- **Contract of record:** `{CONTRACT}` (sha256 `{csha}`, {cb} bytes — equal to `PROGRESS.json` "
      "`contract_of_record`).")
    a(f"- **Drafted:** APOLLO. **Executor:** HEPHAESTUS. **Seed:** {T('progress.seed', JS(PROGRESS, 'seed'), 'int')}. "
      f"**Branch:** `{X['branch']}`, HEAD `{T('git.head7', GIT('short', X['head']), 'str')}` at draft time.")
    a(f"- **AS-OF OF RECORD:** {T('progress.asof', JS(PROGRESS, 'as_of_of_record'), 'str')} — the latest closed 4h "
      f"bar; one corridor; substrate `~/.cache/naiad/snapshots/{T('progress.substrate', JS(PROGRESS, 'substrate'), 'str')}` "
      f"(the live cache untouched: `live_cache_touched` {str(pr['live_cache_touched']).lower()}).")
    a("- **Reading rule.** Every number is read by the generator from the file and field named beside it "
      "(`close/TRACES.json` files each one; F-NUM re-derives it). A block behind a `verbatim` marker is copied "
      "byte for byte from the named lines. \"Tier-E\" means report-only: a SELECTION, not a result; it gates "
      "nothing and holds no slot in m.")
    fb = T("pub.flag", CONST(PUBLISH, "FLAG_BYTES"), "intc")
    a(f"- **SIZE — named, as CONVENTIONS §3.2 asks.** This document is "
      f"{'**FLAGGED** — over' if flagged else 'under'} `FLAG_BYTES` = {fb} B (`scripts/publish_exchange.py`, read by "
      "ast, never imported). Its home is `exchange/reports/`. Its exact bytes and sha are in `close/BOX_COST.json` "
      "(a document cannot carry its own size).")
    a("")
    a("---")
    a("")
    # ─────────────────────────────── §0
    T.region = "s0"
    a("## 0 · VERDICTS")
    a("")
    a("*In the contract's order: R5's chop test first (§0.1), the nine rows (§0.2), the feasibility verdict per lens "
      "(§0.3); then the family (§0.4), the forward ledger (§0.5) and the verdicts in words (§0.6).*")
    a("")
    a("### 0.1 · R5's chop table — the \"killed in chop\" test, printed first [contract R5; L-R.7]")
    a("")
    a(f"*v6's outcomes by 4h and 12h state × %-of-range decile at entry, calibrated and frozen3.0, the TC10 "
      f"five-row anchor, and the direction-adjusted Tier-E rows — {COLLAR}. Copied whole from `{R5MD}` "
      f"(sha256 `{T('r5md.sha', FILESHA(R5MD), 'sha16')}…`).*")
    a("")
    L.extend(chop_answer(X))
    a("")
    a(md_block(R5MD, "## R5 · THE CHOP TABLE"))
    a("")
    a("### 0.2 · The nine rows, exactly as `scores/S0_VERDICTS.md` §0 files them")
    a("")
    a(f"*Read, never retyped: the scorer's §0 table, byte for byte (F-S0-NINE). Every row carries its own honesty "
      f"labels in the verdict cell. `{S0MD}` sha256 `{T('s0md.sha', FILESHA(S0MD), 'sha16')}…`.*")
    a("")
    a(md_block(S0MD, "## §0 table"))
    a("")
    a("### 0.3 · The feasibility verdict per lens — R2, all seven lenses")
    a("")
    L.extend(feasibility_table(X))
    a("")
    a("### 0.4 · The family")
    a("")
    L.extend(family_block(X))
    a("")
    a("### 0.5 · The forward ledger, opened — both books side by side")
    a("")
    L.extend(forward_block(X))
    a("")
    a("### 0.6 · The verdicts in words")
    a("")
    L.extend(headline(X))
    a("")
    a("---")
    a("")
    T.region = "doc"
    L.extend(sec1(X))
    L.extend(sec2(X))
    L.extend(sec3(X))
    L.extend(sec4(X))
    L.extend(sec5(X))
    L.extend(sec6(X))
    L.extend(sec7(X))
    L.extend(sec8(X))
    L.extend(sec9(X))
    L.extend(sec10(X, S5, s5_md))
    L.extend(sec11(X))
    L.extend(sec12(X))
    L.extend(sec13_append(X, append_text))
    L.extend(sec14_disposition(X, flagged))      # CONVENTIONS §3.2: the document ENDS with the disposition table
    return "\n".join(L) + "\n"


def headline(X: dict) -> list[str]:
    fam = X["family"]
    ag = "rows[registration=P-AGE-1]"
    pt = T("P-AGE-1.point", JS(SCORES, f"{ag}.stats.main.point"), "f4s")
    lo = T("P-AGE-1.lo", JS(SCORES, f"{ag}.stats.main.lo"), "f4s")
    hi = T("P-AGE-1.hi", JS(SCORES, f"{ag}.stats.main.hi"), "f4s")
    p = T("P-AGE-1.p", JS(SCORES, f"{ag}.stats.main.p_one_sided"), "f6")
    bar = T("fam.bar", JS(FAMILY, "bar_filed"), "f6")
    # the honesty label and the cohort are READ from the scorer's record, never typed (F-CLAIMS holds both)
    label = T("P-AGE-1.honesty", JS(SCORES, f"{ag}.verdict_cell", re_in_value=r"^SUPPORTED — ([A-Z][A-Z ,-]*?) \("),
              "str")
    cohort = T("P-AGE-1.pre_seen.cohort",
               JS(SCORES, f"{ag}.labels.pre_seen", re_in_value=r"^(the scored cohort IS [^(;]*?) \("), "str")
    band = T("P-AGE-1.refused_band", JS(SCORES, f"{ag}.provenance.scored.description", re_in_value=r"\((B4 OLD);"),
             "str")
    n_sc = T("P-AGE-1.n", JS(SCORES, f"{ag}.stats.main.n"), "int")
    n_b = T("P-AGE-1.n_base", JS(SCORES, f"{ag}.stats.main.n_base"), "int")
    r_n = T("P-AGE-1.refused_n", JS(SCORES, f"{ag}.gate.refused_n"), "int")
    r_s = T("P-AGE-1.refused_sum", JS(SCORES, f"{ag}.gate.refused_sum_r"), "f2s")
    since = T("P-AGE-1.since", JS(SCORES, f"{ag}.pre_seen_new_campaigns.since"), "str")
    ns = T("P-AGE-1.new_scored", JS(SCORES, f"{ag}.pre_seen_new_campaigns.scored"), "int")
    nb = T("P-AGE-1.new_base", JS(SCORES, f"{ag}.pre_seen_new_campaigns.base"), "int")
    if fam["supported"] != ["P-AGE-1"]:
        halt(f"FAMILY.json supported is {fam['supported']}: the headline would be false")
    others = [r["registration"] for r in fam["rows"] if r["verdict_of_record"].startswith("NOT SUPPORTED")]
    below = [r["registration"] for r in fam["rows"] if r["verdict_of_record"] == "NOT SUPPORTED — CI wholly below zero"]
    pw = T("P-WIN-1.p", JS(SCORES, "rows[registration=P-WIN-1].stats.main.p_one_sided"), "f6")
    m = T("fam.m", JS(FAMILY, "family_m"), "int")
    q = T("fam.q", JS(FAMILY, "family_q"), "str")
    barx = T("fam.bar_exact", JS(FAMILY, "bar_exact"), "str")
    spent = T("fam.spent", JS(FAMILY, "tests_spent"), "int")
    words = " · ".join(f"{k} {T(f'r2.{k}.word', JS(R2J, f'lenses.{k}.word'), 'str')}" for k in X["lenses"])
    P = r2_parts(X)
    opening = T("fwd.opening", JL(FWDJL, 0, "opening_iso"), "str")
    nv6 = T("fwd.v6.n", JL(FWDJL, 1, "books.v6.n_appended_total"), "int")
    nsc = T("fwd.n_score", JL(FWDJL, 0, "n_score"), "int")
    ntot = T("git.tier.count", GIT("tierc11_count_in", X["head"]), "int")
    non = T("git.tier.on_origin", GIT("tierc11_count_ancestor_of", X["head"], X["origin"]), "int")
    noff = T("git.tier.not_on_origin", GIT("tierc11_not_ancestor_of", X["head"], X["origin"]), "str")
    o7 = T("git.origin7", GIT("short", X["origin"]), "str")
    h7 = T("git.head7", GIT("short", X["head"]), "str")
    prov = "".join(f" **{r2_prov_sentence(x, P['floor'], P['ratio_bar'], P['net_bar'])}.**" for x in P["prov"])
    return [
        f"1. **P-AGE-1 is the only SUPPORTED row — and it is an {label}.** Δ {pt} R per campaign, CI [{lo}, {hi}], "
        f"p {p} against the bar {bar}. Its `pre_seen` label (`SCORES.json` `labels.pre_seen`) reads: {cohort} — v6 "
        f"(n {n_b}) with the {band} band refused (refused n {r_n}, ΣR {r_s} R), n {n_sc} scored. The point was known "
        f"before filing, and the campaigns entered since {since} number scored {ns} / base {nb}.",
        f"2. **Every other scored row is NOT SUPPORTED** — {', '.join(x for x in others)} — with "
        f"{', '.join(below)}'s CI wholly below zero and P-WIN-1 missing the bar at p {pw}. **m = {m}**, bar "
        f"q/m = {q}/{T('fam.m', JS(FAMILY, 'family_m'), 'int')} = {T('fam.bar', JS(FAMILY, 'bar_filed'), 'f6')} "
        f"({barx}), **{spent} tests spent**: P-SCALP-2 was closed by its own R2 precondition and spent none.",
        f"3. **The R2 law closes range trading on {P['span']}.** Under the [Q-R3] law a FAIL closes the lens for "
        f"range trading in this and every later tier unless the toll model changes, and the maker twin — the only "
        f"reopening path — fails on every lens too. R2's lens verdict of record (POOLED:CLASSIC5 · holdout · "
        f"calibrated · taker): {words}.{prov} At 1h the edge leg nets {P['net1h']} ATR (median H20 {P['med1h']} − "
        f"toll {P['toll1h']}), so **P-SCALP-2 is CLOSED BY R2 (1h: FAIL)**.",
        f"4. **v6 is not killed in chop at entry** — §0.1, printed first, in words and numbers ({COLLAR}).",
        f"5. **The forward ledger is open; the push and the publish are the operator's.** The ledger opened at "
        f"{opening}, n {nv6} appended per book, UNSCORED until each book's own n ≥ {nsc}. At draft time the "
        f"operator's daily publish {o7} had pushed the branch: {non} of {ntot} tierc11 commits were on "
        f"{REMOTE_REF}; not on it: {noff}. "
        f"This CLOSE follows TC10's: close_acts.sh's preconditions stop until TC10's report is tracked in "
        f"exchange/reports/ and its STATUS block is committed on LEDGER_APOLLO (at draft time, HEAD {h7}, TC10's "
        f"CLOSE had {'run' if X['tc10_closed'] else 'not yet run'}).",
    ]


def chop_answer(X: dict) -> list[str]:
    c = lambda cell, col, f: T(f"r5d.{cell}.{col}", r5cell(cell, col), f)   # noqa: E731

    def insample(cell: str, inner: bool = False) -> str:
        if not cell.startswith("calibrated|"):
            return ""
        k = c(cell, 'n_scale_in_sample', 'int')
        return f", SCALE-IN-SAMPLE: {k} in-sample" if inner else f" (SCALE-IN-SAMPLE: {k} of them read in-sample)"
    rows = []
    for sc in ("calibrated", "frozen3.0"):
        for lens in ("4h", "12h"):
            cell = f"{sc}|{lens}|alignment|IN_RANGE"
            rows.append(f"{sc} {lens}: n {c(cell, 'n', 'int')}{insample(cell)}, E {c(cell, 'mean_net_r', 'f4s')} R, "
                        f"holdout slice n {c(cell, 'n_holdout', 'int')} E {c(cell, 'mean_net_r_holdout', 'f4s')} R")
    al = "calibrated|4h|alignment|EXP_ALIGNED"
    cx = "calibrated|4h|alignment|EXP_COUNTER"
    mid = "calibrated|4h|pct_dir_adj|[33.33,66.67)"
    far = "calibrated|4h|pct_dir_adj|[66.67,100)"
    allc = "calibrated|4h|alignment|__ALL__"
    return [
        "**The answer, stated plainly from the numbers below** (" + COLLAR + "): **no — v6 is not killed in chop at "
        "entry.** Its IN_RANGE entries net positive at both lenses, on both scales, and in the causal holdout slice:",
        "",
        *[f"- {r}" for r in rows],
        "",
        f"The whole book reads n {c(allc, 'n', 'int')}{insample(allc)}, E {c(allc, 'mean_net_r', 'f4s')} R. What does "
        f"lose is direction, not balance: at 4h calibrated, entries WITH an expansion earn E {c(al, 'mean_net_r', 'f4s')} "
        f"R (n {c(al, 'n', 'int')}{insample(al, True)}), entries AGAINST one E {c(cx, 'mean_net_r', 'f4s')} R "
        f"(n {c(cx, 'n', 'int')}{insample(cx, True)}); inside a range, the middle third earns E "
        f"{c(mid, 'mean_net_r', 'f4s')} R (n {c(mid, 'n', 'int')}{insample(mid, True)}) and the third nearest the "
        f"boundary the trade must break E {c(far, 'mean_net_r', 'f4s')} R (n {c(far, 'n', 'int')}{insample(far, True)}). "
        "The calibrated reads are IN-SAMPLE "
        "on tuning-era entries (SCALE-IN-SAMPLE, their counts inline above and on every row of the tables below); the "
        "frozen3.0 twin and the holdout slices are the causal reads. The direction rows are the trading review's D-2 "
        f"reading, read from `{R5MD}`'s direction tables, printed beside the frozen table and deciding nothing.",
    ]


def feasibility_table(X: dict) -> list[str]:
    rec = X["r2"]["record"]
    L = [f"*The lens verdict of record is the {rec['panel']} row, {rec['era']} era, {rec['scale_kind']} scale, "
         f"{rec['toll']} toll (`{R2J}`, sha256 `{T('r2j.sha', FILESHA(R2J), 'sha16')}…`; F-FEAS-0 holds every word "
         "and number below against it). A FAIL closes the lens for range trading in this and every later tier "
         "unless the toll model changes; the maker twin is the only reopening path (contract R2). The tuning and "
         f"ALL words are Tier-E twins — {COLLAR}.*",
         "",
         "| lens | word of record (taker) | maker twin | charter twin | Tier-E tuning word | Tier-E ALL word | "
         "n_ranges | edge_n_ranges | edge net H20 (ATR) | provisional | scale |",
         "|---|---|---|---|---|---|---:|---:|---:|---|---|"]
    for k in X["lenses"]:
        b = f"lenses.{k}"
        w = lambda f: T(f"r2.{k}.{f}", JS(R2J, f"{b}.{f}"), "str")   # noqa: E731
        L.append(f"| {k} | **{w('word')}** | {w('maker_twin')} | {w('charter_twin')} | {w('tier_e_tuning_word')} | "
                 f"{w('tier_e_all_word')} | {T(f'r2.{k}.n_ranges', JS(R2J, f'{b}.n_ranges'), 'int')} | "
                 f"{T(f'r2.{k}.edge_n_ranges', JS(R2J, f'{b}.edge_n_ranges'), 'int')} | "
                 f"{T(f'r2.{k}.edge_net_h20', JS(R2J, f'{b}.edge_net_h20'), 'f8s')} | "
                 f"{str(X['r2']['lenses'][k]['provisional']).lower()} | {w('scale_in_sample')} |")
    L += ["", "*1w is PROVISIONAL (a leg under its floor, the pick a whole-tape fallback, in-sample at every "
          "instant) — listed for the operator (BUILD §11 Q4).*"]
    return L


def family_block(X: dict) -> list[str]:
    m = T("fam.m", JS(FAMILY, "family_m"), "int")
    barx = T("fam.bar_exact", JS(FAMILY, "bar_exact"), "str")
    spent = T("fam.spent", JS(FAMILY, "tests_spent"), "int")
    return [f"**m = {m}, bar {barx}, {spent} tests spent; P-SCALP-2 closed by its precondition** (R2 1h: FAIL) — "
            "it spent no slot, and fewer tests never loosen the bar. Copied from the scorer's record:",
            "", md_block(S0MD, "## Family")]


def forward_block(X: dict) -> list[str]:
    opening = T("fwd.opening", JL(FWDJL, 0, "opening_iso"), "str")
    n912 = T("fwd.912.n", JL(FWDJL, 1, "books.trg912.n_appended_total"), "int")
    nv6 = T("fwd.v6.n", JL(FWDJL, 1, "books.v6.n_appended_total"), "int")
    nsc = T("fwd.n_score", JL(FWDJL, 0, "n_score"), "int")
    hdr = find_heading(FWDMD, "# TIER-C11 · THE FORWARD LEDGER")
    l1, l2 = block(FWDMD, "# TIER-C11 · THE FORWARD LEDGER", upto="## ")
    return [f"**Opened at {opening}; n {nv6} (v6) and n {n912} ({T.ex('9/12', 'the frozen 9/12 book: a trigger-pair NAME (contract :58), not a measured value')}) "
            f"appended; UNSCORED until each book's own n ≥ {nsc}; the v6 continuation and the "
            f"{T.ex('9/12', 'the frozen 9/12 book: a trigger-pair NAME (contract :58), not a measured value')} OPEN "
            "campaign are listed, never counted.** Copied from the ledger's own report:",
            "", verbatim(FWDMD, l1, l2), "", md_block(FWDMD, "## Both books, side by side")]


# ───────────────────────────────────────────────────────────── §1
def sec1(X: dict) -> list[str]:
    pr = X["progress"]
    L = ["## 1 · R0 and the build log", "", "### 1.1 · R0 — the census at the start", ""]
    L += [f"- **HEAD at R0:** `{pr['head_at_r0'][:7]}`; **census at** {pr['r0_census_utc']}.",
          f"- **R0 census** (`PROGRESS.json` `r0_census`): {pr['r0_census']}",
          f"- **Law 1** (`law_1_note`): {pr['law_1_note']}",
          f"- **Resume point at draft time** (`resume_point`): {pr['resume_point']}", "",
          "### 1.2 · The stage ledger (`PROGRESS.json` `stages`, as filed)", "",
          "| stage | status | as-of | artifacts | last fixture entry (legs · transcript sha) | one line |",
          "|---|---|---|---:|---|---|"]
    for st in pr["stages"]:
        fx = st.get("fixtures") or []
        last = f"{fx[-1]['legs_total']} · `{fx[-1]['transcript_sha_after'][:12]}`" if fx else "—"
        n_art = st.get("artifact_count", len(st.get("artifact_shas", {})))
        L.append(f"| {st['stage']} | {st['status']} | {st.get('as_of') or '—'} | {n_art} | {last} | "
                 f"{st['one_line'].replace('|', '/')} |")
    L += ["", "### 1.3 · Every tierc11 commit (git log, oldest first)", "",
          "| commit | committed | subject | on origin at draft time |", "|---|---|---|---|"]
    for h, s, d, subj in X["tier_commits"]:
        on = "yes" if is_ancestor(h, X["origin"]) else "**no**"
        L.append(f"| `{s}` | {d} | {subj.replace('|', '/')} | {on} |")
    L += ["", f"Not a tierc11 commit but in the range: `{X['origin7']}` — the operator's daily auto-publish, which "
          f"pushed the branch ({REMOTE_REF} = `{X['origin7']}` at draft time).", "",
          "### 1.4 · The workflows (the compute ledger is §14.3)", ""]
    for w in X["compute"]["workflows"]:
        L.append(f"- `{w['workflow']}`")
    L.append(f"- `{X['compute']['this_wave']['workflow']}` — {X['compute']['this_wave']['state']}")
    L += ["", "### 1.5 · The amendments of record (`LEANS_AMENDMENTS.md`, by title)", ""]
    for n, ln in enumerate(SRC.lines(AMEND), 1):
        m = re.match(r"^\*\*(AM-\d+(?: ERRATUM)?) · (.+?)\*\*", ln)
        if m:
            L.append(f"- **{m.group(1)}** — {m.group(2)} (`{AMEND}:{n}`)")
    L += [f"", f"`LEANS.md` stays byte-frozen (sha256 `{pr['leans_of_record']['sha256'][:16]}…`, pinned by "
          f"`REGISTRATIONS.json`); the amendments of record are sha256 `{pr['amendments_of_record']['sha256'][:16]}…`.",
          ""]
    return L


# ───────────────────────────────────────────────────────────── §2
def sec2(X: dict) -> list[str]:
    L = ["## 2 · STAGE R — ranges, done once", "", "### 2.1 · R1 — the lenses and the picks of record", "",
         f"*{COLLAR}. The picks are pins (`ranges/SCALE_PICKS.json`), never re-fitted.*", ""]
    L.append(md_block(R1MD, "### Picks of record per asset x lens", first_table=True))
    L += ["", "Pick stability, first half of tuning vs the whole tuning era:", ""]
    L.append(md_block(R1MD, "### Stability [L-R.2]", first_table=True))
    L += ["", f"The pins, the density grid whole and the per-era counts are in `{R1MD}` (sha256 "
          f"`{SRC.sha(R1MD)[:16]}…`).", "", "### 2.2 · R2 — feasibility per lens", ""]
    dl = find_heading(STAGE_R, "Disclosure [L-R.4]")
    L.append(verbatim(STAGE_R, dl, dl))
    L.append("")
    L.append(md_block(STAGE_R, "### THE LENS VERDICTS OF RECORD", first_table=True))
    L += ["", "**TC10 continuity** (the taker rows at 5m / 4h / 1d beside TC10's filed Q-R3 verdicts):", ""]
    tl = find_heading(STAGE_R, "- TC10 continuity [AM-1]")
    L.append(verbatim(STAGE_R, tl, tl))
    L += ["", f"Every R2 row whole (the record rows and the Tier-E `would_read` rows, and the height ÷ toll "
          f"distribution) is `{TC11}/stage_r/R2_FEASIBILITY.md` (sha256 `{SRC.sha(f'{TC11}/stage_r/R2_FEASIBILITY.md')[:16]}…`). "
          "TC10's lone 4h pooled holdout PASS is explained in the findings (FN-TRD-14).", "",
          "### 2.3 · R3 — the nesting grid, whole", "",
          f"*{COLLAR}. Calibrated = the scale of record, IN-SAMPLE on tuning-era entries; frozen3.0 = the causal twin; "
          "the HOLDOUT slice beside every cell. The contract's \"the nesting grid whole\": both grid files are printed "
          "here WHOLE — every line, in verbatim blocks, the files' own H1 / H2 lines re-printed as H4 labels (a "
          "verbatim block may not carry them); F-CLAIMS holds every line of both files to these blocks.*", "",
          f"#### R3 on the books — `{NESTMD}` whole (sha256 `{SRC.sha(NESTMD)[:16]}…`)", ""]
    L += whole_md(NESTMD)
    L += ["", f"#### R3 on the lane books — `{LANESMD}` whole (sha256 `{SRC.sha(LANESMD)[:16]}…`)", ""]
    L += whole_md(LANESMD)
    L += ["", "### 2.4 · R4 — the fractal grid's ★ cells", ""]
    L += r4_star(X)
    return L


def whole_md(rel: str) -> list[str]:
    """A markdown file printed WHOLE: every run of lines between its H1 / H2 headings as a verbatim block (blank
    edges trimmed), each H1 / H2 heading re-printed as an H4 label (a verbatim block may not carry an H1 / H2)."""
    L = SRC.lines(rel)
    out: list[str] = []
    run: list[int] = []

    def flush():
        nums = [n for n in run]
        while nums and not L[nums[0] - 1].strip():
            nums = nums[1:]
        while nums and not L[nums[-1] - 1].strip():
            nums = nums[:-1]
        if nums:
            out.extend([verbatim(rel, 0, None, lines=nums), ""])
        run.clear()
    for n, ln in enumerate(L, 1):
        if heading_level(ln) in (1, 2):
            flush()
            out.extend(["#### " + ln.split(" ", 1)[1], ""])
        else:
            run.append(n)
    flush()
    while out and out[-1] == "":
        out.pop()
    return out


def r4_star(X: dict) -> list[str]:
    g1, g2 = block(R4MD, "## 4 · The grid of record", first_table=True)
    n1, n2 = block(R4MD, "## 7 · Null (gaps+order, K = 20)", first_table=True)
    grid = md_table_rows(R4MD, g1, g2)
    null = {(r["lens"], r["event"], r["L+1 cell"], r["dir"]): (n, r) for n, r in md_table_rows(R4MD, n1, n2)}
    L = [f"*{COLLAR}. POOLED:CLASSIC5 · calibrated · cell law record · direction both; the contract's three conditions "
         "(EXP_ALIGNED*, IN_RANGE_COINCIDENT*, IN_RANGE_MID*) per lens × event. NET = median H-bar term − toll (ATR); "
         "Δcell = NET − the cell's base rate; the null percentile is a DESCRIPTION, never a p-value. Each row names "
         f"the `{R4MD}` lines it copies (§4 grid · §7 null).*", "",
         "| lens | event | L+1 cell | n ALL H20 | NET ALL H20 | Δcell ALL H20 | null pctile ALL H20 | NET ALL H100 | "
         "Δcell ALL H100 | null pctile ALL H100 | n holdout H20 | NET holdout H20 | Δcell holdout H20 | null pctile "
         "holdout H20 | lines (§4 · §7) |",
         "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|"]
    n_rows = 0
    for n, r in grid:
        if r["scale"] != "calibrated" or r["law"] != "record" or r["dir"] != "both" or not r["L+1 cell"].endswith("*"):
            continue
        k = (r["lens"], r["event"], r["L+1 cell"], r["dir"])
        if k not in null:
            halt(f"R4 null row missing for {k}")
        nn, z = null[k]
        L.append(f"| {r['lens']} | {r['event']} | {r['L+1 cell']} | {r['n ALL H20']} | {r['NET ALL H20']} | "
                 f"{r['Δcell ALL H20']} | {z['pctile ALL H20']} | {r['NET ALL H100']} | {r['Δcell ALL H100']} | "
                 f"{z['pctile ALL H100']} | {r['n holdout H20']} | {r['NET holdout H20']} | {r['Δcell holdout H20']} | "
                 f"{z['pctile holdout H20']} | :{n} · :{nn} |")
        n_rows += 1
    if n_rows == 0:
        halt("no R4 ★ row found")
    R4STAR["rows"] = n_rows
    L += ["", "**TC10 continuity** — frozen3.0 · one-shot · 4h · POOLED:CLASSIC5 · tap89 · H20 NET:", "",
          md_block(R4MD, "## 1 · TC10 continuity", first_table=True), "",
          "**The grid of record — every file, its rows and content sha** (the full grid is the parquet; the markdown "
          "is whole only over the scope each caption declares):", "", md_block(R4MD, "## Files", first_table=True),
          "", f"`{R4MD}` sha256 `{SRC.sha(R4MD)[:16]}…`; `R4_GRID.parquet` file sha256 "
          f"`{prog_art('research_outputs/tierc11/stage_r4/R4_GRID.parquet')[:16]}…` (PROGRESS.json, stage TC11-R4).", ""]
    return L


R4STAR: dict = {}


def prog_art(rel: str) -> str:
    hits = {st["artifact_shas"][rel]["sha256"] for st in SRC.j(PROGRESS)["stages"] if rel in st.get("artifact_shas", {})}
    if len(hits) != 1:
        halt(f"PROGRESS.json records {len(hits)} shas for {rel}")
    return hits.pop()


# ───────────────────────────────────────────────────────────── §3..§8
def collared(rel: str, l1: int, l2: int) -> str:
    """Source lines l1..l2 in verbatim blocks, split before every table so that the collar line (contract :8: "a
    SELECTION, not a result" on every non-registered table) stands directly above each table the draft copies."""
    L = SRC.lines(rel)
    out: list[str] = []
    run: list[int] = []

    def flush():
        nums = list(run)
        while nums and not L[nums[0] - 1].strip():
            nums = nums[1:]
        while nums and not L[nums[-1] - 1].strip():
            nums = nums[:-1]
        if nums:
            out.extend([verbatim(rel, 0, None, lines=nums), ""])
        run.clear()
    for n in range(l1, l2 + 1):
        if L[n - 1].startswith("|") and (n == l1 or not L[n - 2].startswith("|")):
            flush()
            out.extend([COLLAR_LINE, ""])
        run.append(n)
    flush()
    while out and out[-1] == "":
        out.pop()
    return "\n".join(out)


def collared_block(rel: str, heading: str, **kw) -> str:
    l1, l2 = block(rel, heading, **kw)
    return collared(rel, l1, l2)


def sec3(X: dict) -> list[str]:
    ll = find_heading(WMD, "Lead distributions, binned (whole):")
    b1, b2 = table_after_line(WMD, "Lead distributions, binned (whole):")
    return ["## 3 · STAGE W — early warnings from the 1h crosses", "",
            "### 3.1 · The P-WARN-1 condition block", "", md_block(WMD, "## P-WARN-1 · the condition block"), "",
            "### 3.2 · W2 — post-entry cohorts vs their at-risk sets", "",
            collared_block(WMD, "## W2 · post-entry cohorts vs their at-risk sets"), "",
            "### 3.3 · W2 — the forward leg", "", collared_block(WMD, "## W2 · the forward leg"), "",
            "### 3.4 · W2 — pre-entry classes", "", collared_block(WMD, "## W2 · PRE-ENTRY classes"), "",
            "### 3.5 · W2 — the relay's evidence", "",
            collared_block(WMD, "## W2 · relay evidence [L-W.6]", first_table=True), "",
            verbatim(WMD, ll, ll), "", collared(WMD, b1, b2), "",
            f"The per-window lead distribution (both populations, whole) is in `{WMD}` (sha256 `{SRC.sha(WMD)[:16]}…`).", ""]


def sec4(X: dict) -> list[str]:
    return ["## 4 · STAGE G — admission gates", "", "### 4.1 · The three gates crossed, 2 × 2 × 2 (whole)", "",
            md_block(GMD, "## The three gates crossed 2 × 2 × 2"), "",
            "### 4.2 · The gate rows — refused cohorts, shadows, the forfeit note", "",
            md_block(GMD, "## Gate rows [L-1.5]"), "",
            "### 4.3 · F-DEF — both tide-age definitions", "", md_block(GMD, "## F-DEF:", upto="### "), "",
            "### 4.4 · The lag bands", "", md_block(GMD, "## Lag bands (L-G.2)"), "",
            "### 4.5 · The within-window priority book", "",
            md_block(GMD, "## The within-window PRIORITY book [L-G.3]", upto="### "), "",
            md_block(GMD, "### Every window of the priority replay, by outcome (counts)"), "",
            f"The priority window log and the key-by-key comparison are in `{GMD}` (sha256 `{SRC.sha(GMD)[:16]}…`).", ""]


def sec5(X: dict) -> list[str]:
    return ["## 5 · STAGE T — triggers and lanes", "", "### 5.1 · P-BRK-4H — the registered book and its arms", "",
            md_block(TBRK, "## 1 · The registered book (scored arm)"), "",
            md_block(TBRK, "## 4 · Tier-E arms"), "",
            "### 5.2 · P-RELAY-1 — the arms, the miss column, the lead", "",
            md_block(TREL, "## Regbooks written (book, not a verdict)"), "",
            md_block(TREL, "## The window dispositions"), "",
            md_block(TREL, "## The lead of the relay over the v6 4h trigger", first_table=True), "",
            md_block(TREL, "## Era slices"), "",
            f"The miss column whole (every window the relay never activated) and the relay book whole are in `{TREL}` "
            f"(sha256 `{SRC.sha(TREL)[:16]}…`).", "",
            "### 5.3 · The forward ledger", "", md_block(FWDMD, "## Appended campaigns (whole)"), "",
            md_block(FWDMD, "## Refreshes"), ""]


def sec6(X: dict) -> list[str]:
    v1 = find_heading(CONTRACT, 'VETOES BY NAME:')
    return ["## 6 · STAGE S — the scalper's twins", "",
            "**Stage S is CLOSED BY R2 (1h: FAIL).** The scalper's precondition (R2 must PASS at 1h) fails, so no "
            "scalper book, no maker twin book and no 17-asset view exists; P-SCALP-2 prints no number and spends no "
            "slot. **F-SCALP is N/A** (3 scalps hand-walked: there are no scalps); F-SCALP-GATE proves the gate. "
            "**The \"scalp\" veto was never exercised.**", "",
            md_block(SMD, "## 0 · The verdict"), "",
            "**The scalper's twins, as far as they exist — the 1h R2 row of record and its taker / maker / charter / "
            "tuning words:**", "", md_block(SMD, "## 3 · The words beside the verdict of record"), "",
            "The contract's veto by name, for the record:", "", verbatim(CONTRACT, v1, v1 + 2), ""]


def sec7(X: dict) -> list[str]:
    return ["## 7 · STAGE A — the adds, head to head", "", md_block(AMD, "## 1 · Registered books"), "",
            collared_block(AMD, "## 3 · HEAD-TO-HEAD"), ""]


def sec8(X: dict) -> list[str]:
    return ["## 8 · STAGE H — P-TP-RNG, the take-profit at the 12h boundary", "",
            "*The D15 tail ratio and the named wall-exit risk are on the row (below, and in §0.2).*", "",
            md_block(HMD, "## 0 · The registered book"), "", md_block(HMD, "## 1 · The regbook arms"), ""]


# ───────────────────────────────────────────────────────────── §9
NAMED = [("F-CTRL", r"^F-CTRL"), ("F-NEST-ASOF", r"^F-NEST-ASOF$"), ("F-WARN-ASOF", r"^F-WARN-ASOF$"),
         ("F-DEF", r"^F-DEF$"), ("F-GATE", r"^F-GATE$"), ("F-RELAY", r"^F-RELAY$"), ("F-SCALP", r"^F-SCALP$"),
         ("F-ADD", r"^F-ADD$"), ("F-TP", r"^F-TP$"), ("F-FEAS", r"^F-FEAS$"), ("F-DET", r"^F-DET$"),
         ("F-GRID", r"^F-GRID$"), ("F-KEY", r"^F-KEY$"), ("import-closure", r"^F-CLOSURE"),
         ("worktree attestation", r"^F-ATTEST$")]


def transcripts(X: dict) -> list[dict]:
    rec: dict[str, dict] = {}
    for st in X["progress"]["stages"]:
        for rel, v in st.get("artifact_shas", {}).items():
            if "/FIXTURES_" in rel and rel.endswith(".txt"):
                r = rec.setdefault(rel, {"path": rel, "stages": [], "sha": v["sha256"]})
                r["stages"].append(st["stage"])
                if r["sha"] != v["sha256"]:
                    halt(f"PROGRESS.json records two shas for {rel}")
    out = []
    for rel in sorted(rec):
        r = rec[rel]
        if SRC.sha(rel) != r["sha"]:
            halt(f"{rel} on disk is not the PROGRESS.json record")
        ents = [f for st in X["progress"]["stages"] for f in st.get("fixtures", []) if f["transcript_sha_after"] == r["sha"]]
        if not ents:
            halt(f"no PROGRESS fixture entry for {rel}")
        legs = {e["legs_total"] for e in ents}
        if len(legs) != 1:
            halt(f"{rel}: PROGRESS entries disagree on legs_total")
        ids = re.findall(r"(?m)^  \[(?:PASS|FAIL)\] ([A-Za-z0-9._-]+):", SRC.t(rel))
        tail = [ln for ln in SRC.lines(rel) if re.match(r"^  \d+ GREEN, \d+ RED", ln)]
        r.update({"legs": legs.pop(), "suite": ents[-1]["suite"], "ids": ids, "tally": tail[-1].strip() if tail else ""})
        out.append(r)
    return out


def sec9(X: dict) -> list[str]:
    tr = transcripts(X)
    tot = sum(r["legs"] for r in tr)
    L = ["## 9 · FIXTURES — the transcripts of record", "",
         f"*{len(tr)} suites, {tot} fixtures, every transcript on disk equal to its `PROGRESS.json` sha "
         f"(`last_sweep_utc`: {X['progress']['last_sweep_utc']}).*", "",
         "| suite (PROGRESS.json, last entry) | transcript | fixtures | tally | sha256[:16] |", "|---|---|---:|---|---|"]
    for r in tr:
        L.append(f"| {r['suite']} | `{r['path']}` | {r['legs']} | {r['tally']} | `{r['sha'][:16]}` |")
    L += ["", "**The contract's named fixtures, and where they live** (leg ids read from the transcripts):", "",
          "| contract fixture | legs of record |", "|---|---|"]
    for name, pat in NAMED:
        where = [f"`{i}` ({Path(r['path']).stem.replace('FIXTURES_', '')})" for r in tr for i in r["ids"] if re.match(pat, i)]
        if name == "F-SCALP":
            gate = [f"`{i}` ({Path(r['path']).stem.replace('FIXTURES_', '')})" for r in tr for i in r["ids"] if i == "F-SCALP-GATE"]
            cell = ("**N/A** — Stage S is CLOSED BY R2: no scalp exists to hand-walk; " + ", ".join(gate) +
                    " proves the closing gate") if not where else ", ".join(where)
        elif name in ("F-DET", "F-GRID", "F-KEY"):
            cell = f"{len(where)} suites: " + ", ".join(sorted({w.split(' ')[1].strip('()') for w in where}))
        else:
            if not where:
                halt(f"contract fixture {name} has no leg of record")
            cell = ", ".join(where)
        L.append(f"| {name} | {cell} |")
    L += ["", "**The six attestation records** (`review/attest/*.json`):", "",
          "| record | lens | commit | verdict | staged artifacts | findings | tracked at HEAD |",
          "|---|---|---|---|---:|---:|---|"]
    for p in sorted((ROOT / ATTEST).glob("*.json")):
        rel = f"{ATTEST}/{p.name}"
        d = SRC.j(rel)
        tracked = "yes" if git_rc("ls-files", "--error-unmatch", "--", rel) == 0 else "**no — untracked**"
        L.append(f"| `{p.name}` | {d['lens']} | `{d['commit'][:7]}` | {d['verdict']} | {d['staged_artifacts']} | "
                 f"{len(d['findings'])} | {tracked} |")
    L += ["", f"The CLOSE's own suite is `{TRANSCRIPT}` (F-S0-NINE, F-NUM, F-FEAS-0, F-LAR11, F-BOXCOST, F-FNF, "
          "F-CLOSE-ORDER, F-DET); its sha is not quoted here because it certifies this document.", ""]
    return L


# ───────────────────────────────────────────────────────────── §10..§14
def sec10(X: dict, S5: dict, s5_md: bytes) -> list[str]:
    c = S5["counts"]["all"]
    L = ["## 10 · FINDINGS — REPORTED, NOT FIXED (condensed, ranked)", "",
         f"*The full harvest is `{OUT_S5M}` (sha256 `{hashlib.sha256(s5_md).hexdigest()}`), with its JSON twin: "
         f"{c['total']} findings — {c['operator']} operator-owned, {c['executor']} executor-owned "
         f"({S5['counts']['HARVESTED']['total']} harvested verbatim, {S5['counts']['MEASURED']['total']} measured, "
         f"{S5['counts']['LEAN']['total']} leans); duplicates merged under their primary; "
         f"{len(S5['superseded'])} harvested items superseded by a later record listed apart. Each line below is the "
         "finding's first line.*", ""]
    for f in S5["findings"]:
        lead = f["text"].split("\n", 1)[0]
        L.append(f"{f['rank']}. `{f['id']}` · {f['owner']} · {f['class']} — {lead}")
    L.append("")
    return L


def sec11(X: dict) -> list[str]:
    L = ["## 11 · OPERATOR QUESTIONS STILL OPEN", ""]
    for i, q in enumerate(open_questions(X, short=False), 1):
        L.append(f"{i}. {q}")
    L.append("")
    return L


def sec12(X: dict) -> list[str]:
    return ["## 12 · WHAT THIS BUILD IS NOT", "",
            "- **Not confirmation.** P-AGE-1's SUPPORTED is an in-sample re-score of a cohort TC10 filed; no campaign "
            "entered after the TC10 pin. The forward ledger is the only confirmation path, and it is at n "
            f"{T('fwd.v6.n', JL(FWDJL, 1, 'books.v6.n_appended_total'), 'int')} (v6) / "
            f"{T('fwd.912.n', JL(FWDJL, 1, 'books.trg912.n_appended_total'), 'int')} "
            f"({T.ex('9/12', 'the frozen 9/12 book: a trigger-pair NAME (contract :58), not a measured value')}).",
            "- **Not a SAIL act, not a card change.** SAIL stays HELD (contract CLOSE: \"SAIL still HELD\").",
            f"- **Not a licence for range trading.** Every lens word of record reads FAIL and no maker twin passes. "
            f"Under the R2 law the {lens_span(X['r2_closed'])} lenses are closed for range trading in this and every "
            f"later tier unless the toll model changes"
            + (f"; {', '.join(X['r2_prov'])} reads FAIL provisionally (a count under its floor) and its closure is "
               f"the operator's question (§11 Q4)." if X["r2_prov"] else "."),
            "- **Not a scalper result.** Stage S was closed by its precondition; nothing was built, scored or tuned.",
            "- **Not a promotion of any Tier-E cell.** The R4 grid, the R5 direction rows, the W2 cohorts, the gate "
            "crossings and every twin are selections; the reviews' post-hoc candidates are named for the operator, "
            "not registered.",
            "- **Not re-scored.** The nine rows are the scorer's record, copied; no verdict was recomputed here.",
            "- **Not published by the executor.** The push and publish are the operator's `close_acts.sh`.", ""]


def sec13_append(X: dict, append_text: str) -> list[str]:
    sha = hashlib.sha256(append_text.encode()).hexdigest()
    st = BOXC["stamp"]
    return ["## 13 · THE LEDGER APPEND — verbatim, as staged", "",
            f"*`{OUT_APPEND}` — {len(append_text.encode()):,} B, sha256 `{sha}`, pre-stamp. close_acts.sh step 3 fills "
            f"its one pending stamp after the push (the {st['bracket_bytes']:,} B bracket becomes the {st['fill_bytes']} B "
            f"fill 'N tierc11 commits, M on a remote' with {st['digits']}-digit counts: {st['stamped_bytes']:,} B stamped) "
            f"and F-LAR11 --stamped re-certifies it; the ledger receives the stamped bytes. F-LAR11 holds it to TC10's check_format "
            f"law and re-verifies every «cite»; close_acts.sh step 0 re-runs F-LAR11 before anything is pushed.*", "",
            "~~~text", append_text.rstrip("\n"), "~~~", ""]


def disposition_table(bc: dict) -> list[str]:
    """The seven-column table of CONVENTIONS §3.2, condensed: every box-bound, planned and outside-repo row one by
    one; every other row grouped by (set · tracked · pushed · protected by · box cost) with its count. Every row of
    close/BOX_COST.json lands in exactly one line (F-CLAIMS re-counts it)."""
    def cls(r):
        tr = r["tracked"].split(" (")[0].split(" ·")[0]
        pu = "yes — " + REMOTE_REF if r["pushed"].startswith("yes") else r["pushed"]
        pr = r["protected_by"].split(" · ")[0]
        bx = r["box_cost"].split(" (")[0]
        return (r["set"], tr, pu, pr, bx)
    single = [r for r in bc["rows"] if r["box_bound"] or r["set"].startswith(("d ·", "e ·"))]
    single_ids = {id(r) for r in single}
    groups: dict[tuple, list[dict]] = {}
    for r in bc["rows"]:
        if id(r) in single_ids:
            continue
        groups.setdefault(cls(r), []).append(r)
    L = ["| PATH | EXISTS | TRACKED | COMMITTED | PUSHED | PROTECTED BY | BOX COST |", "|---|---|---|---|---|---|---|"]
    for k in sorted(groups):
        rs = groups[k]
        dirs = sorted({"/".join(r["path"].split("/")[:3 if r["path"].startswith("research_outputs/") else 1])
                       for r in rs})
        on = sum(1 for r in rs if r["exists"].startswith("yes"))
        vol = sum(1 for r in rs if r["bytes"] is None and r["exists"].startswith(("yes", "volatile")))
        nb = sum(r["bytes"] for r in rs if r["bytes"] is not None)
        commits = sorted({r["committed"] for r in rs}, key=lambda c: (c == "not committed", c))
        rules = sorted({m for r in rs for m in re.findall(r"`(\.gitignore:\d+)`", r["tracked"])})
        forced = sum(1 for r in rs if "force-added past" in r["tracked"])
        wfs = sorted({r["protected_by"].split(" · ", 1)[1] for r in rs if " · " in r["protected_by"]})
        tops = sorted({m for r in rs for m in re.findall(r"\(`([^`]+)`\)", r["box_cost"])})
        L.append(f"| **{len(rs)} paths** · set {k[0]} · under {', '.join('`' + d + '`' for d in dirs[:5])}"
                 f"{' …' if len(dirs) > 5 else ''} | {on} on disk · {nb:,} B sized"
                 f"{f' · {vol} not sized (volatile or self)' if vol else ''} | {k[1]}"
                 f"{(f' ({forced} force-added past ' if forced else ' (') + ', '.join('`' + x + '`' for x in rules) + ')' if rules else ''} | "
                 f"{', '.join(commits)} | "
                 f"{k[2]} | {k[3]}{' · ' + '; '.join(wfs) if wfs else ''} | {k[4]}"
                 f"{' (' + ', '.join('`' + t + '`' for t in tops) + ')' if tops else ''} |")
    for r in single:
        L.append(f"| `{r['path']}` | {r['exists']} | {r['tracked']} | {r['committed']} | {r['pushed']} | "
                 f"{r['protected_by']} | {r['box_cost']} |")
    DISPO["lines"] = len(L) - 2
    DISPO["covered"] = sum(len(v) for v in groups.values()) + len(single)
    if DISPO["covered"] != bc["n_rows"]:
        halt(f"the disposition table covers {DISPO['covered']} of {bc['n_rows']} BOX-COST rows")
    return L


DISPO: dict = {}


def sec14_disposition(X: dict, flagged: bool) -> list[str]:
    bc = BOXC
    pj = bc["projection"]
    L = ["## 14 · DISPOSITION · BOX-COST", "",
         f"*A PRE-CLOSE SNAPSHOT (git-volatile). Constants read by ast, never imported: `BOX_BYTES` "
         f"{bc['const']['BOX_BYTES']['value']:,} (`{PUBLISH}:{bc['const']['BOX_BYTES']['line']}`), `FLAG_BYTES` "
         f"{bc['const']['FLAG_BYTES']['value']:,} (`:{bc['const']['FLAG_BYTES']['line']}`), `WARN_FRACTION` "
         f"{bc['const']['WARN_FRACTION']['value']} / `REFUSE_FRACTION` {bc['const']['REFUSE_FRACTION']['value']}; the "
         f"§4.2 per-file cap {bc['cap']['bytes']:,} B (`POINTER_RULE`, \"{bc['cap']['quote']}\"). The document ends, as "
         f"CONVENTIONS §3.2 asks, with the seven-column table (§14.5); its per-file form ({bc['n_rows']} rows) is "
         f"`{OUT_BOXM}` with `{OUT_BOXJ}`, re-derived by F-BOXCOST.*", "",
         "### 14.1 · Git", "",
         f"- HEAD `{X['head7']}` on `{X['branch']}`; `{REMOTE_REF}` at `{X['origin7']}` — the operator's daily "
         f"publish pushed the branch; HEAD is {bc['git']['ahead']} commit(s) ahead.",
         f"- {bc['git']['tier_on_remote']} of {bc['git']['tier_total']} tierc11 commits are in a remote-tracking ref; "
         f"not yet: {', '.join('`' + s + '`' for s in bc['git']['tier_off_remote']) or 'none'}.",
         f"- The CLOSE's own files are {'untracked' if bc['close_untracked'] else 'tracked'} at draft time; the CLOSE "
         "commit (the orchestrator's) adds them before the operator runs `close_acts.sh`.", "",
         "### 14.2 · The tick set now, and after both CLOSEs", "",
         f"- Now: `exchange/` index {bc['tick']['exchange_bytes']:,} B across {bc['tick']['exchange_files']} files + "
         f"`LEDGER.md` at HEAD {bc['tick']['ledger_md_bytes']:,} B = **{bc['tick']['tick_bytes']:,} B = "
         f"{bc['tick']['fraction_pct']} of the box · {bc['tick']['level']}** (WARN at "
         f"{bc['const']['WARN_FRACTION']['value']}).",
         (f"- TC10's CLOSE lands first (its close_acts.sh, the operator's): + its build document "
          f"{pj['tc10']['doc_bytes']:,} B + its builder's report {pj['tc10']['report_bytes']:,} B + its stamped append "
          f"{pj['tc10']['append_stamped_bytes']:,} B ({pj['tc10']['append_bytes']:,} B pre-stamp; its fill counts "
          f"{pj['tc10']['n']} tierc10 commits)." if pj["tc10"] else
          "- TC10's CLOSE has landed: its document, report and block are already in the tick set."),
         f"- Then this CLOSE: + this document (its exact bytes and the tick after it are `{OUT_BOXJ}` `projection`) + "
         f"the stamped append {pj['append_stamped_bytes']:,} B ({pj['append_bytes']:,} B pre-stamp) + the uncommitted "
         f"exchange/ edits publish() sweeps ({', '.join(bc['exchange_uncommitted']) or 'none'}: "
         f"{pj['exchange_sweep_bytes']:,} B).",
         f"- `{LEDGER_APOLLO}`: {pj['ledger_now_bytes']:,} B now → {pj['ledger_after_bytes']:,} B after "
         f"{'both appends' if pj['tc10'] else 'the append'} — already over the wire (append-only; it grew across it).",
         "",
         "### 14.3 · The compute ledger", "",
         f"*Source: `{COMPUTE}` — {X['compute']['source']}; each row corroborated against the harness's workflow "
         "journal when the record was filed. The orchestrator fills this wave's row; when it does, the generator and "
         "`scripts/tierc11_close_fixtures.py --refile-transcript` are re-run at the same HEAD before the CLOSE commit "
         "(§1.4 and this table read the row).*", "",
         "| workflow | agents | tokens | wall s |", "|---|---:|---:|---:|"]
    ta = tt = tw = 0
    for i, w in enumerate(X["compute"]["workflows"]):
        ag = T(f"compute.{w['workflow']}.agents", JS(COMPUTE, f"workflows[{i}].agents"), "int")
        tk = T(f"compute.{w['workflow']}.tokens", JS(COMPUTE, f"workflows[{i}].tokens"), "intc")
        ws = T(f"compute.{w['workflow']}.wall_s", JS(COMPUTE, f"workflows[{i}].wall_s"), "intc")
        ta, tt, tw = ta + w["agents"], tt + w["tokens"], tw + w["wall_s"]
        L.append(f"| `{w['workflow']}` | {ag} | {tk} | {ws} |")
    tw_ = X["compute"]["this_wave"]
    if all(k in tw_ for k in ("agents", "tokens", "wall_s")):
        L.append(f"| `{tw_['workflow']}` | {T('compute.this_wave.agents', JS(COMPUTE, 'this_wave.agents'), 'int')} | "
                 f"{T('compute.this_wave.tokens', JS(COMPUTE, 'this_wave.tokens'), 'intc')} | "
                 f"{T('compute.this_wave.wall_s', JS(COMPUTE, 'this_wave.wall_s'), 'intc')} |")
    else:
        L.append(f"| `{tw_['workflow']}` | {tw_['state']} | | |")
    L.append(f"| **the {len(X['compute']['workflows'])} journaled workflows, together** | {ta} | {tt:,} | {tw:,} |")
    L += ["", "### 14.4 · The CLOSE acts — the operator's (`research_outputs/tierc11/close/close_acts.sh`)", "",
          "0. Preconditions: the branch; **TC10's CLOSE has run and is committed** (its report tracked in "
          "`exchange/reports/`, its STATUS block committed on LEDGER_APOLLO — else STOP: \"run "
          "research_outputs/tierc10/close/close_acts.sh first (the ledger keeps tier order)\", or the named half-run "
          "stop that points at FN-M-TC10-ACTS-IGNORED); a clean index; the CLOSE files committed; the destinations "
          "absent; the stamp pending; and **F-LAR11 re-run on the pre-stamp append** (every «cite» against its "
          "source as it stands then) — all before anything is pushed.",
          "1. Push the committed work.",
          f"2. LAW 5: `{OUT_DRAFT}` → `{DOC}`, sha checked across the copy; the draft's removal committed on its own; pushed.",
          "3. Fill the append's stamp after the push; re-certify it (`scripts/tierc11_close_fixtures.py F-LAR11 "
          "--stamped`); a failure stops with the recovery named (restore the pending stamp, fix, run steps 3-7 by hand).",
          f"4. Append to `{LEDGER_APOLLO}`.",
          "5. Commit the non-exchange residue (the stamped append and its certificate).",
          "6. `publish()` exactly as TC10's step 7 does; the push result STATED.",
          "7. The bright paths, and the final line: \"Operator: click Sync now.\"", "",
          "### 14.5 · The file-disposition table (CONVENTIONS §3.2) — every file this build created, modified or moved",
          "",
          f"**FLAGGED, named to the operator with its home (CONVENTIONS §3.2):** `{DOC}` — this document, "
          f"{'over' if flagged else 'under'} the {bc['const']['FLAG_BYTES']['value']:,} B wire; home `exchange/reports/`. "
          f"`{LEDGER_APOLLO}` is already over the wire (append-only; it grew across it).", "",
          f"*Seven columns. The box-bound, planned and outside-repo rows one by one; every other row grouped by (set · "
          f"tracked · pushed · protected by · box cost) with its count — {bc['n_rows']} rows in all, the same rows as "
          f"`{OUT_BOXM}`. COMMITTED / PUSHED are true of HEAD `{X['head7']}` as last fetched.*", ""]
    L += disposition_table(bc)
    return L


# ═══════════════════════════════════════════════════════════════ BOX-COST
BOXC: dict = {}


def gitignore_line(rel: str) -> str | None:
    r = subprocess.run(["git", "-C", str(ROOT), "check-ignore", "-v", "--no-index", "--", rel],
                       capture_output=True, text=True)
    if r.returncode != 0:
        return None
    src, line, pat = r.stdout.split("\t")[0].split(":", 2)
    return f"{src}:{line}"


def workflow_scope(rel: str, sources) -> str:
    for s in sources:
        if rel == s or rel.startswith(s + "/"):
            return f"`--workflow` scope `{s}`"
    if "/" not in rel and rel.endswith(".md"):
        return "`--workflow` root glob `*.md`"
    return "outside `--workflow`"


def stamp_projection(X: dict, append_bytes: int) -> dict:
    """This append's bytes once close_acts.sh step 3 fills its stamp: the bracket becomes 'N tierc11 commits, N on a
    remote' with N = the tierc11 commits now + the LAW-5 commit (+ the CLOSE commit if it is a tierc11( commit — the
    digit count is the same either way, or this HALTs), every one of them on a remote after step 2's push."""
    n = len(X["tier_commits"]) + 1
    if len(str(n)) != len(str(n + 1)):
        halt(f"the stamp's digit count depends on whether the CLOSE commit is a tierc11( commit ({n} vs {n + 1})")
    fill = f"{n} tierc11 commits, {n} on a remote"
    br = len(STAMP_TEXT.encode())
    return {"bracket_bytes": br, "fill_bytes": len(fill.encode()), "digits": len(str(n)), "n_assumed": n,
            "stamped_bytes": append_bytes - br + len(fill.encode())}


def tc10_projection(X: dict) -> dict | None:
    """What TC10's close_acts.sh adds to the tick set and the ledger while it has not run: read from its own script
    (the variables it moves and appends) and from git (its stamp's count), never typed."""
    if X["tc10_closed"]:
        return None
    acts = SRC.lines(TC10_ACTS)
    assign = {m.group(1): m.group(2) for ln in acts for m in [re.match(r"^([A-Z_]+)=(\S+)$", ln)] if m}
    for k in ("DRAFT", "DOC", "RPT_SRC", "RPT", "APP"):
        if k not in assign:
            halt(f"{TC10_ACTS}: no {k}= assignment")
    if assign["DOC"] != TC10_DOC or assign["APP"] != TC10_APPEND:
        halt(f"{TC10_ACTS}: DOC / APP are not {TC10_DOC} / {TC10_APPEND}")
    app = SRC.t(assign["APP"])
    br = STAMP_RE.findall(app)
    if len(br) != 1:
        halt(f"{assign['APP']}: {len(br)} pending stamps (TC10's step fills exactly one)")
    pre = [ln for ln in acts if 'startswith("tierc10")' in ln]
    if len(pre) != 1:
        halt(f"{TC10_ACTS}: its stamp's commit rule (startswith(\"tierc10\")) is not found once")
    n = sum(1 for s in git("log", "--format=%s", "HEAD").splitlines() if s.startswith("tierc10")) + 1
    fill = f"{n} tierc10 commits, {n} on a remote"
    ab = len(app.encode())
    return {"doc_path": assign["DOC"], "doc_bytes": SRC.size(assign["DRAFT"]), "draft_path": assign["DRAFT"],
            "report_path": assign["RPT"], "report_src": assign["RPT_SRC"],
            "report_bytes": (ROOT / assign["RPT_SRC"]).stat().st_size if (ROOT / assign["RPT_SRC"]).is_file() else 0,
            "append_path": assign["APP"], "append_bytes": ab, "n": n,
            "append_stamped_bytes": ab - len(br[0].encode()) + len(fill.encode())}


def box_rows(X: dict, sizes_mem: dict[str, int], draft_bytes: int, append_bytes: int) -> dict:
    C = {n: {"value": ast_const(PUBLISH, n)[0], "line": ast_const(PUBLISH, n)[1]}
         for n in ("SCOPE", "SUBJECT", "BOX_BYTES", "WARN_FRACTION", "REFUSE_FRACTION", "TICK_EXTRA", "FLAG_BYTES")}
    wf_src, wf_line = ast_const(BACKUP, "WORKFLOW_SOURCES")
    BOX, FLAG = C["BOX_BYTES"]["value"], C["FLAG_BYTES"]["value"]
    scope = C["SCOPE"]["value"]
    tick_extra = tuple(C["TICK_EXTRA"]["value"])
    # (a) paths in tierc11 commits (b9ed953 included)
    a_paths: dict[str, list[str]] = {}
    cur = None
    for ln in git("log", "--reverse", "--name-status", "--format=%x00%H%x09%s", X["head"]).splitlines():
        if ln.startswith("\x00"):
            h, s = ln[1:].split("\t", 1)
            cur = h if s.startswith(TIER_PREFIX) else None
            continue
        if cur and ln.strip():
            parts = ln.split("\t")
            for p in parts[1:]:
                a_paths.setdefault(p, []).append(cur[:7])
    # (b) PROGRESS artifacts not in (a)
    b_paths = sorted({rel for st in X["progress"]["stages"] for rel in st.get("artifact_shas", {})} - set(a_paths))
    # (c) the CLOSE's files; (c2) other untracked tierc11 files
    c_paths = sorted((set(CLOSE_SOURCES) | set(VOLATILE)) - set(a_paths))
    others = [p for p in git("ls-files", "--others", "--exclude-standard", "--", TC11, "scripts").splitlines()
              if (p.startswith(TC11 + "/") or p.startswith("scripts/tierc11_")) and p not in c_paths
              and not p.startswith(CLOSE + "/") and p not in (OUT_DRAFT, OUT_APPEND)]
    rows = []
    commit_on_remote: dict[str, bool] = {}

    def on_remote(short: str) -> bool:
        if short not in commit_on_remote:
            commit_on_remote[short] = bool(git("branch", "-r", "--contains", short).strip())
        return commit_on_remote[short]

    def row(rel: str, set_name: str) -> dict:
        p = ROOT / rel
        tracked = git_rc("ls-files", "--error-unmatch", "--", rel) == 0
        ign = gitignore_line(rel)
        if rel in sizes_mem:
            exists, nbytes = f"yes · {sizes_mem[rel]:,} B (written by this generator)", sizes_mem[rel]
        elif rel in SELF_UNSIZED:
            exists, nbytes = "yes — written by this generator after this table (a file does not measure itself)", None
        elif rel in VOLATILE:
            exists, nbytes = "volatile — written by a fixture run; not sized", None
        elif p.is_file():
            nbytes = p.stat().st_size
            exists = f"yes · {nbytes:,} B"
        else:
            exists, nbytes = "no", None
        if tracked:
            mod = git_rc("diff", "--quiet", "HEAD", "--", rel) != 0
            tr = "tracked" + (" · MODIFIED in worktree" if mod else "")
            if ign:
                tr += f" · force-added past `{ign}`"
        elif ign:
            tr, mod = f"ignored (`{ign}`)", False
        else:
            tr, mod = "untracked", False
        last = git("log", "-1", "--format=%h", "--", rel).strip() if tracked else ""
        committed = f"`{last}`" if last else "not committed"
        pushed = ("yes — " + REMOTE_REF) if last and on_remote(last) else ("no" if last else "no — nothing committed")
        wf = workflow_scope(rel, wf_src)
        if last and on_remote(last) and not mod:
            prot = f"GitHub only · {wf}"
        elif last and not on_remote(last):
            prot = f"NOT PROTECTED — committed, not pushed · {wf}"
        elif mod:
            prot = f"NOT PROTECTED — modified since the pushed commit · {wf}"
        elif ign:
            prot = f"NOT PROTECTED — git-ignored, local disk only · {wf}"
        else:
            prot = f"NOT PROTECTED — untracked · {wf}"
        boxb = rel.startswith(scope) or rel in tick_extra
        if boxb and nbytes is not None:
            wire = "**FLAGGED** (over the wire)" if nbytes > FLAG else "under the wire"
            cost = f"{nbytes:,} B · {100.0 * nbytes / BOX:.3f}% of {BOX:,} B · {wire}"
        elif boxb:
            cost = "box-bound · not sized"
        else:
            top = rel.split("/")[0] + ("/" if "/" in rel else "")
            cost = f"n/a — unsynced (`{top}`)"
        return {"path": rel, "set": set_name, "exists": exists, "bytes": nbytes, "tracked": tr, "committed": committed,
                "pushed": pushed, "protected_by": prot, "box_cost": cost, "box_bound": boxb,
                "flagged": bool(boxb and nbytes is not None and nbytes > FLAG),
                "in_tierc11_commits": a_paths.get(rel, [])}
    for rel in sorted(a_paths):
        rows.append(row(rel, "a · a tierc11 commit"))
    for rel in b_paths:
        rows.append(row(rel, "b · a PROGRESS.json artifact"))
    for rel in c_paths:
        rows.append(row(rel, "c · the CLOSE's own files"))
    for rel in sorted(others):
        rows.append(row(rel, "c · untracked tierc11 file"))
    # (d) the planned exchange destinations
    if draft_bytes is None:        # the draft's own §13 reads this before the draft exists
        d_ex, d_cost, d_flag = "no — PLANNED · sized as the draft (close/BOX_COST.json)", "box-bound · sized after the draft", None
    else:
        d_ex = f"no — PLANNED · sized as the draft: {draft_bytes:,} B"
        d_cost = (f"{draft_bytes:,} B · {100.0 * draft_bytes / BOX:.3f}% of {BOX:,} B · "
                  + ("**FLAGGED** (over the wire)" if draft_bytes > FLAG else "under the wire"))
        d_flag = draft_bytes > FLAG
    d_doc = {"path": DOC, "set": "d · PLANNED destination", "exists": d_ex,
             "bytes": draft_bytes, "tracked": "untracked — PLANNED, not yet on disk", "committed": "not committed",
             "pushed": "no — nothing committed",
             "protected_by": "NOT PROTECTED — PLANNED; publish() commits and pushes `exchange/**` at CLOSE · "
                             + workflow_scope(DOC, wf_src),
             "box_cost": d_cost, "box_bound": True, "flagged": bool(d_flag), "in_tierc11_commits": []}
    if (ROOT / DOC).exists():
        halt(f"{DOC} exists: the CLOSE has run")
    led_now = (ROOT / LEDGER_APOLLO).stat().st_size
    stamp = stamp_projection(X, append_bytes)
    tc10 = tc10_projection(X)
    led_after = led_now + (tc10["append_stamped_bytes"] if tc10 else 0) + stamp["stamped_bytes"]
    led = row(LEDGER_APOLLO, "d · receives the append")
    after_w = "TC10's and this stamped append" if tc10 else "the stamped append"
    led["exists"] += f" · after {after_w} {led_after:,} B"
    led["box_cost"] = (f"{led_now:,} B now → {led_after:,} B after {after_w} · "
                       f"{100.0 * led_after / BOX:.3f}% of {BOX:,} B · "
                       + ("**FLAGGED** (over the wire; append-only, it grew across it)" if led_after > FLAG
                          else "under the wire"))
    led["flagged"] = bool(led_after > FLAG)
    rows += [d_doc, led]
    # (e) the snapshot
    nf = nb = 0
    for dp, dn, fn in os.walk(SNAPSHOT):
        for f in fn:
            nf += 1
            nb += os.stat(os.path.join(dp, f), follow_symlinks=False).st_size
    rows.append({"path": "~/.cache/naiad/snapshots/tc11_20260925", "set": "e · the frozen snapshot",
                 "exists": f"yes · {nf} files · {nb:,} B", "bytes": nb, "tracked": "n/a — outside repo",
                 "committed": "n/a — outside repo", "pushed": "n/a — outside repo",
                 "protected_by": "NOT PROTECTED — outside the repo, not mirrored", "box_cost": "n/a — outside repo",
                 "box_bound": False, "flagged": False, "in_tierc11_commits": []})
    # the tick set now
    ex = []
    for rec in git("ls-files", "-s", "-z", "--", scope.rstrip("/")).split("\0"):
        if rec:
            meta, _, path = rec.partition("\t")
            ex.append((meta.split()[1], path))
    sizes = git("cat-file", "--batch-check", stdin="".join(s + "\n" for s, _ in ex)).split("\n")
    ex_bytes = sum(int(ln.split()[2]) for ln in sizes if ln.strip())
    led_md = 0
    for pth in tick_extra:
        out = git("ls-tree", "-l", "HEAD", "--", pth).strip()
        if out:
            led_md += int(out.split()[3])
    tick = ex_bytes + led_md
    frac = tick / BOX
    level = ("REFUSE" if frac > C["REFUSE_FRACTION"]["value"] else
             "WARN" if frac >= C["WARN_FRACTION"]["value"] else "OK")
    mod_ex = [p for p in git("diff", "--name-only", "--", "exchange").splitlines() if p]
    sweep = 0
    for pth in mod_ex:
        idx = git("ls-files", "-s", "--", pth).split()
        ib = int(git("cat-file", "-s", idx[1]).strip()) if idx else 0
        sweep += (ROOT / pth).stat().st_size - ib if (ROOT / pth).exists() else -ib
    tc10_add = (tc10["doc_bytes"] + tc10["report_bytes"] + tc10["append_stamped_bytes"]) if tc10 else 0
    proj = tick + tc10_add + (draft_bytes or 0) + stamp["stamped_bytes"] + sweep
    pl = ("REFUSE" if proj / BOX > C["REFUSE_FRACTION"]["value"] else
          "WARN" if proj / BOX >= C["WARN_FRACTION"]["value"] else "OK")
    tier = X["tier_commits"]
    off = [s for h, s, d, subj in tier if not on_remote(s)]
    rule, rule_line = ast_const(PUBLISH, "POINTER_RULE")
    cm = re.search(r"(\d+) MB per file", rule)
    if not cm:
        halt("POINTER_RULE no longer names the per-file cap as 'N MB per file'")
    return {
        "const": C, "workflow_sources": {"value": list(wf_src), "line": wf_line},
        "rows": rows, "n_rows": len(rows),
        "cap": {"bytes": int(cm.group(1)) * 1_000_000, "quote": cm.group(0), "line": rule_line,
                "unit": "decimal MB (publish_exchange prints MB as B / 1e6)"},
        "stamp": stamp,
        "git": {"head": X["head"], "branch": X["branch"], "upstream": REMOTE_REF, "upstream_tip": X["origin"],
                "ahead": int(git("rev-list", "--count", f"{X['origin']}..{X['head']}").strip()),
                "tier_total": len(tier), "tier_on_remote": len(tier) - len(off), "tier_off_remote": off},
        "tick": {"exchange_bytes": ex_bytes, "exchange_files": len(ex), "ledger_md_bytes": led_md, "tick_bytes": tick,
                 "fraction": round(frac, 6), "fraction_pct": f"{100.0 * frac:.3f}%", "level": level},
        "projection": {"tc10": tc10, "draft_bytes": draft_bytes, "append_bytes": append_bytes,
                       "append_stamped_bytes": stamp["stamped_bytes"], "exchange_sweep_bytes": sweep,
                       "ledger_now_bytes": led_now, "ledger_after_bytes": led_after,
                       "tick_after_bytes": proj, "fraction_after_pct": f"{100.0 * proj / BOX:.3f}%", "level_after": pl,
                       "law": "tick now + TC10's CLOSE while it has not landed (its build document, its builder's "
                              "report, its stamped append) + this document + this stamped append + the uncommitted "
                              "exchange/ edits publish() sweeps; a stamped append = its pre-stamp bytes - the bracket "
                              "+ the fill 'N <tier> commits, N on a remote' (N read now + the LAW-5 commit, every "
                              "commit on a remote after the push)"},
        "append_bytes": append_bytes, "exchange_uncommitted": mod_ex,
        "close_untracked": any(git_rc("ls-files", "--error-unmatch", "--", p) != 0 for p in (OUT_DRAFT, OUT_APPEND)),
        "flagged": [r["path"] for r in rows if r["flagged"]],
    }


def render_box_md(bc: dict) -> str:
    C = bc["const"]
    L = ["# TIER-C11 · CLOSE · DISPOSITION · BOX-COST", "",
         "> **PRE-CLOSE SNAPSHOT — regenerate after the CLOSE commit and push.** Every git column is true of HEAD "
         f"`{bc['git']['head'][:7]}` and of the remote-tracking refs as last fetched (no fetch was made).",
         ">", "> **REPORT-ONLY · Tier-E bookkeeping — paths, bytes and git metadata; nothing scored, no verdict read.**",
         "",
         "Built to the seven-column standard of `exchange/status/CONVENTIONS.md` §3.2. Constants read by "
         "`ast.literal_eval` of their assignments — the module is never imported or executed:", ""]
    for n in ("SCOPE", "SUBJECT", "BOX_BYTES", "WARN_FRACTION", "REFUSE_FRACTION", "TICK_EXTRA", "FLAG_BYTES"):
        L.append(f"- `{n}` = `{C[n]['value']!r}` — `{PUBLISH}:{C[n]['line']}`")
    L.append(f"- `WORKFLOW_SOURCES` ({len(bc['workflow_sources']['value'])} roots) — `{BACKUP}:"
             f"{bc['workflow_sources']['line']}` (PROTECTED BY names the `--workflow` scope only; no archive is "
             "verified by this table)")
    g = bc["git"]
    L += ["", f"**Git:** HEAD `{g['head'][:7]}` on `{g['branch']}` · `{g['upstream']}` at `{g['upstream_tip'][:7]}` · "
          f"HEAD {g['ahead']} ahead · {g['tier_on_remote']} of {g['tier_total']} tierc11 commits in a remote-tracking "
          f"ref · not yet: {', '.join(g['tier_off_remote']) or 'none'}.", "",
          f"**The tick set now:** `exchange/` index {bc['tick']['exchange_bytes']:,} B ({bc['tick']['exchange_files']} "
          f"files) + `LEDGER.md` at HEAD {bc['tick']['ledger_md_bytes']:,} B = {bc['tick']['tick_bytes']:,} B = "
          f"{bc['tick']['fraction_pct']} · **{bc['tick']['level']}**.", "",
          f"**After both CLOSEs (projection; {bc['projection']['law']}):** "
          + (f"+ TC10's build document {bc['projection']['tc10']['doc_bytes']:,} B + TC10's builder's report "
             f"{bc['projection']['tc10']['report_bytes']:,} B + TC10's stamped append "
             f"{bc['projection']['tc10']['append_stamped_bytes']:,} B (TC10's CLOSE has not landed) "
             if bc['projection']['tc10'] else "(TC10's CLOSE has landed) ")
          + f"+ this build document {bc['projection']['draft_bytes']:,} B + this stamped append "
          f"{bc['projection']['append_stamped_bytes']:,} B ({bc['projection']['append_bytes']:,} B pre-stamp) + the "
          f"uncommitted exchange/ edits publish() sweeps {bc['projection']['exchange_sweep_bytes']:,} B = "
          f"{bc['projection']['tick_after_bytes']:,} B = {bc['projection']['fraction_after_pct']} · "
          f"**{bc['projection']['level_after']}**. `{LEDGER_APOLLO}`: {bc['projection']['ledger_now_bytes']:,} B now → "
          f"{bc['projection']['ledger_after_bytes']:,} B.", "",
          f"**The §4.2 per-file cap:** {bc['cap']['bytes']:,} B (`{PUBLISH}:{bc['cap']['line']}` POINTER_RULE: "
          f"\"{bc['cap']['quote']}\"; {bc['cap']['unit']}); this build document {bc['projection']['draft_bytes']:,} B is "
          f"{'UNDER' if bc['projection']['draft_bytes'] <= bc['cap']['bytes'] else 'OVER'} it.", "",
          "**FLAGGED (over the wire), named with the home:** " +
          ", ".join(f"`{p}`" for p in bc["flagged"]) + ".", "",
          "## The table", "",
          "| PATH | EXISTS | TRACKED | COMMITTED | PUSHED | PROTECTED BY | BOX COST |", "|---|---|---|---|---|---|---|"]
    for r in bc["rows"]:
        L.append(f"| `{r['path']}` | {r['exists']} | {r['tracked']} | {r['committed']} | {r['pushed']} | "
                 f"{r['protected_by']} | {r['box_cost']} |")
    L += ["", "## Volatile fields (named)", "",
          "- git-volatile: TRACKED, COMMITTED, PUSHED, PROTECTED BY, `git.*` — a commit, a push or a fetch moves them.",
          "- disk-volatile: EXISTS, BOX COST, `tick.*`, `projection.*` — any file landing moves them.",
          f"- never sized: {', '.join(VOLATILE)} (a fixture run rewrites them).", ""]
    return "\n".join(L)


# ═══════════════════════════════════════════════════════════════ close_acts.sh
def render_acts() -> str:
    residue_src = " ".join(f'"{p}"' for p in CLOSE_SOURCES)
    t10 = MEAS["tc10_acts_ignored"]
    t10_step = t10["step"]
    t10_rule = ", ".join(sorted({v[1] for v in t10["paths"].values()}))
    return f'''#!/usr/bin/env bash
# TIER-C11 · CLOSE ACTS — run by the OPERATOR.
# Generated by scripts/tierc11_close.py (do not hand-edit; re-run the generator instead).
#
# Why a script: the acts that publish (the push, publish()) are the operator's; the executor stages them.
#
# Order (each step checked; the script stops at the first failure and says where):
#   0  preconditions: right branch; TC10's CLOSE has run AND is committed (its report tracked in
#      exchange/reports, its STATUS block committed on LEDGER_APOLLO — the ledger keeps tier order); clean
#      index; the CLOSE files present and committed; destinations absent; the stamp pending; F-LAR11 re-run on
#      the pre-stamp append (every «cite» against its source as it stands NOW) — all before anything is pushed
#   1  push the committed work FIRST, before anything changes (safe to re-run if it fails)
#   2  LAW 5: the build document leaves research_outputs/ for exchange/reports/ (sha checked across the copy);
#      the draft's removal is committed on its own, since publish() may stage exchange/** only; pushed
#   3  the append's stamp is filled AFTER the push ("N tierc11 commits, M on a remote") and F-LAR11 --stamped
#      re-certifies it
#   4  the append goes onto {LEDGER_APOLLO} (the commissioning lane's ledger, CONVENTIONS §3.1)
#   5  the non-exchange residue (the stamped append + its certificate) is committed on its own
#   6  publish(): stages exchange/** only, guard-checks the index, commits and pushes (CONVENTIONS §3.4) —
#      and the push result is STATED
#   7  bright paths, and the final line
# Usage:  bash {OUT_ACTS} [--check]      (--check runs step 0 only and changes nothing)
# Nothing here deletes evidence, touches the live cache, or re-scores anything.

set -euo pipefail
ROOT="$(cd "$(dirname "${{BASH_SOURCE[0]}}")/../../.." && pwd)"
cd "$ROOT"

PY="$HOME/venvs/naiad/bin/python"
export NAIAD_CACHE_DIR="$HOME/.cache/naiad/snapshots/tc11_20260925" PYTHONDONTWRITEBYTECODE=1
BR={BRANCH}
DRAFT={OUT_DRAFT}
DOC={DOC}
APP={OUT_APPEND}
LAR={STAMPED_TRANSCRIPT}
LEDGER={LEDGER_APOLLO}
FIXT={FIXTURES_SCRIPT}
TC10_DOC={TC10_DOC}
TC10_ACTS={TC10_ACTS}
TRAILER="Co-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>"
SOURCES=({residue_src})

say()  {{ printf '\\n\\033[1;36m== %s\\033[0m\\n' "$*"; }}
die()  {{ printf '\\n\\033[1;31mSTOPPED at step %s: %s\\033[0m\\n' "$STEP" "$*"; exit 1; }}
sha()  {{ shasum -a 256 "$1" | cut -c1-64; }}

STEP=0; say "0 · preconditions"
[ "$(git rev-parse --abbrev-ref HEAD)" = "$BR" ] || die "not on $BR"
if [ ! -f "$TC10_DOC" ] || ! grep -qE '^=== STATUS_APOLLO — [0-9]{{4}}-[0-9]{{2}}-[0-9]{{2}} — TIER-C10 · ' "$LEDGER"; then
  die "run $TC10_ACTS first (the ledger keeps tier order)"
fi
git ls-files --error-unmatch -- "$TC10_DOC" >/dev/null 2>&1 || die "TC10's CLOSE did not finish: $TC10_DOC is not tracked (TC10's publish() adds it) — see FN-M-TC10-ACTS-IGNORED: TC10's step-{t10_step} 'git add' exits 1 on paths under {t10_rule} without -f; finish TC10's steps by hand, then re-run this"
git diff --quiet HEAD -- "$LEDGER" || die "TC10's CLOSE did not finish: $LEDGER differs from HEAD (TC10's block appended, not committed) — see FN-M-TC10-ACTS-IGNORED; finish TC10's steps by hand, then re-run this"
git diff --cached --quiet || die "the index is not clean"
for f in "${{SOURCES[@]}}" "$LEDGER"; do [ -f "$f" ] || die "missing $f"; done
for f in "${{SOURCES[@]}}"; do
  git ls-files --error-unmatch -- "$f" >/dev/null 2>&1 || die "$f is not committed (the CLOSE commit adds the CLOSE files first)"
  git diff --quiet HEAD -- "$f" || die "$f differs from HEAD (commit it first)"
done
[ ! -e "$DOC" ] || die "$DOC already exists"
if grep -qE '^=== STATUS_APOLLO — [0-9]{{4}}-[0-9]{{2}}-[0-9]{{2}} — TIER-C11 · ' "$LEDGER"; then die "$LEDGER already carries a TIER-C11 block"; fi
grep -q '⟦STAMP AT CLOSE' "$APP" || die "the append's stamp is not pending"
LARTMP="$(mktemp -d)"
"$PY" "$FIXT" F-LAR11 --root="$LARTMP" > /dev/null || die "F-LAR11 does not certify the pre-stamp append as the sources stand now (transcript $LARTMP/FIXTURES_CLOSE_partial.txt) — nothing was pushed; re-run the generator and the close suite, commit, then re-run this"
rm -rf "$LARTMP"
echo "ok · HEAD $(git rev-parse --short HEAD) · origin/$BR $(git rev-parse --short "origin/$BR") · F-LAR11 GREEN on the pre-stamp append"
if [ "${{1:-}}" = "--check" ]; then say "--check: step 0 passed; nothing was changed"; exit 0; fi

STEP=1; say "1 · push the committed work (nothing has changed yet; safe to re-run if this fails)"
git push origin "$BR" || die "the push failed — nothing has changed; fix the remote and re-run"
git fetch -q origin
[ "$(git rev-parse HEAD)" = "$(git rev-parse "origin/$BR")" ] || die "origin/$BR does not equal HEAD after the push"
echo "PUSHED · origin/$BR = $(git rev-parse --short HEAD)"

STEP=2; say "2 · LAW 5: the build document moves to exchange/reports/, and that commit is pushed"
a=$(sha "$DRAFT"); cp "$DRAFT" "$DOC"; b=$(sha "$DOC")
[ "$a" = "$b" ] || die "sha changed across the copy ($a vs $b)"
git rm -q "$DRAFT"
git commit -q -m "tierc11(CLOSE): LAW 5 — the build document leaves research_outputs/ for $DOC

The draft's removal is committed on its own because publish() may stage exchange/** only; the
document itself enters the record through publish(). sha256 across the move: $b.

$TRAILER"
echo "moved · sha256 $b · $(wc -c < "$DOC" | tr -d ' ') B"
git push origin "$BR" || die "the move is committed locally ($(git rev-parse --short HEAD)) but did not push; run 'git push origin $BR', then run steps 3-7 by hand from this file"
git fetch -q origin
[ "$(git rev-parse HEAD)" = "$(git rev-parse "origin/$BR")" ] || die "origin/$BR does not equal HEAD after the second push"
echo "PUSHED · origin/$BR = $(git rev-parse --short HEAD)"

STEP=3; say "3 · stamp the append after the push, then re-certify it (F-LAR11 --stamped)"
"$PY" - <<'PYEOF'
import re, subprocess
p = "{OUT_APPEND}"
def g(*a):
    return subprocess.run(["git", *a], capture_output=True, text=True, check=True).stdout
tc = [l.split("\\t", 1)[0] for l in g("log", "--format=%H%x09%s", "HEAD").splitlines()
      if l.split("\\t", 1)[-1].startswith("{TIER_PREFIX}")]
off = set(g("rev-list", "HEAD", "--not", "--remotes").split())
n, m = len(tc), sum(1 for h in tc if h not in off)
s = open(p, encoding="utf-8").read()
new, k = re.subn(r"⟦STAMP AT CLOSE[^⟧\\n]*⟧", f"{{n}} tierc11 commits, {{m}} on a remote", s, count=1)
if k != 1:
    raise SystemExit("no pending stamp found")
open(p, "w", encoding="utf-8").write(new)
print(f"stamp · {{n}} tierc11 commits, {{m}} on a remote")
PYEOF
"$PY" "$FIXT" F-LAR11 --stamped > /dev/null || die "F-LAR11 does not certify the stamped append — steps 1-2 are pushed; nothing was appended; the stamp stays filled in $APP for inspection. To resume: 'git checkout -- $APP' (the pending stamp back), fix the cause, then run steps 3-7 by hand from this file (re-running the script stops at step 0: the draft has moved)"
tail -1 "$LAR" | cut -c1-60

STEP=4; say "4 · append to $LEDGER"
before=$(wc -l < "$LEDGER" | tr -d ' ')
cat "$APP" >> "$LEDGER"
after=$(wc -l < "$LEDGER" | tr -d ' ')
echo "appended · $before -> $after lines · $(wc -c < "$LEDGER" | tr -d ' ') B"

STEP=5; say "5 · commit the non-exchange residue"
git add -- "$APP" "$LAR"
git commit -q -m "tierc11(CLOSE): the append stamped after the push and re-certified (F-LAR11 --stamped)

$TRAILER"
echo "committed $(git rev-parse --short HEAD)"

STEP=6; say "6 · publish exchange/** (CONVENTIONS §3.4) — the push result is STATED"
if "$PY" -c "import sys; from pathlib import Path; R=Path('.').resolve(); sys.path.insert(0,str(R/'scripts')); import publish_exchange as p; r=p.publish(R,'$(date +%F)'); print(r['status'], r['commit'], r['pushed'], r['offenders']); sys.exit(0 if r['status']=='PUBLISHED' and r['pushed'] else 1)"; then
  printf '\\n\\033[1;32mPUSH RESULT: SUCCEEDED — publish() reported PUBLISHED and pushed; origin/%s = %s\\033[0m\\n' "$BR" "$(git rev-parse --short "origin/$BR")"
else
  die "PUSH RESULT: FAILED — publish() did not report PUBLISHED + pushed (see its lines above); the local commits stay, nothing was lost"
fi

STEP=7; say "7 · bright paths"
printf '\\033[1;33m%s\\033[0m\\n' \\
  "$DOC" \\
  "$LEDGER  (TC11 STATUS appended)" \\
  "{CONTRACT}" \\
  "{OUT_S5M}" \\
  "{OUT_BOXM}" \\
  "{PROGRESS}  (CLOSE still to be recorded by the builder)" \\
  "origin/$BR = $(git rev-parse --short "origin/$BR")"
printf '\\n\\033[1;32mOperator: click Sync now.\\033[0m\\n'
'''


# ═══════════════════════════════════════════════════════════════ main
def write_out(out_root: Path, rel: str, data: bytes, mode: int | None = None) -> None:
    if rel not in OUTPUTS:
        halt(f"refusing to write {rel}: not an output of this generator")
    p = out_root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(data)
    if mode is not None:
        os.chmod(p, mode)


def main(argv: list[str]) -> int:
    out_root = ROOT
    for a in argv:
        if a.startswith("--out-root="):
            out_root = Path(a.split("=", 1)[1]).resolve()
        else:
            halt(f"unknown argument {a}")
    if (ROOT / DOC).exists():
        halt(f"{DOC} exists — the CLOSE has run; this generator is pre-close only")
    app_disk = ROOT / OUT_APPEND
    if app_disk.exists() and not STAMP_RE.search(app_disk.read_text("utf-8")):
        halt(f"{OUT_APPEND} carries a FILLED stamp — the stamped append of record is never re-rendered")
    X = gather()
    S5 = build_findings(X)                          # region s5 (the measured findings)
    append_text = render_append(X)                  # region append
    S5["inputs"] = {rel: {"bytes": n, "sha256": s} for rel, (n, s) in sorted(SRC.read.items())}
    s5_md = render_findings_md(S5).encode()
    s5_json = (json.dumps(S5, indent=2, ensure_ascii=False) + "\n").encode()
    acts = render_acts()
    flag_bytes = ast_const(PUBLISH, "FLAG_BYTES")[0]
    cp = T.checkpoint()
    sizes_mem = {OUT_DRAFT: 0, OUT_APPEND: len(append_text.encode()), OUT_S5J: len(s5_json),
                 OUT_S5M: len(s5_md), OUT_ACTS: len(acts.encode())}
    # the draft's §13 reads BOX-COST without the draft's own size (a document cannot carry its own size)
    BOXC.update(box_rows(X, sizes_mem, None, len(append_text.encode())))
    T.restore(cp)
    probe = render_draft(X, append_text, S5, s5_md, flagged=True)
    flagged = len(probe.encode()) > flag_bytes
    T.restore(cp)
    draft = render_draft(X, append_text, S5, s5_md, flagged=flagged)
    if (len(draft.encode()) > flag_bytes) != flagged:
        halt("the draft's FLAGGED word is not stable across the two passes")
    if len(draft.encode()) > BOXC["cap"]["bytes"]:
        halt(f"the build document is {len(draft.encode()):,} B, over the CONVENTIONS §4.2 per-file cap "
             f"{BOXC['cap']['bytes']:,} B (POINTER_RULE) — publish would refuse it")
    sizes_mem[OUT_DRAFT] = len(draft.encode())
    bc = box_rows(X, sizes_mem, len(draft.encode()), len(append_text.encode()))
    box_md = render_box_md(bc)
    box_json = {"schema": "tierc11.close.BOX_COST.v1", "tier": X["progress"]["tier"],
                "label": "REPORT-ONLY · Tier-E bookkeeping — a PRE-CLOSE SNAPSHOT (git- and disk-volatile)",
                "built_by": GENERATOR_SCRIPT, "draft_sha256": hashlib.sha256(draft.encode()).hexdigest(),
                "draft_bytes": len(draft.encode()), **bc}
    traces = {"schema": "tierc11.close.TRACES.v1", "built_by": GENERATOR_SCRIPT,
              "law": "every number the draft, the append and the measured findings print is a trace: its spec names "
                     "the record (file + field, a parquet cell, a text match, a git fact, an ast constant) and its "
                     "fmt the formatting; uses count the renders per region (s0 = the draft's §0, append = the "
                     "ledger append, s5 = the measured findings, doc = the rest of the draft). Exemptions are "
                     "digit-bearing NAMES, counted the same way.",
              "regions": {"s0": "the draft from '## 0 · VERDICTS' to '## 1 ·'", "append": "the ledger append's prose",
                          "s5": "measured findings", "doc": "the rest of the draft"},
              "traces": [dict(T.items[k], uses=T.uses[k]) for k in sorted(T.items)],
              "exemptions": [{"lit": k, "why": EXEMPT_WHY[k], "uses": T.ex_uses[k]} for k in sorted(T.ex_uses)],
              "r4_star_rows": R4STAR.get("rows")}
    write_out(out_root, OUT_S5J, s5_json)
    write_out(out_root, OUT_S5M, s5_md)
    write_out(out_root, OUT_APPEND, append_text.encode())
    write_out(out_root, OUT_DRAFT, draft.encode())
    write_out(out_root, OUT_BOXM, box_md.encode())
    write_out(out_root, OUT_BOXJ, (json.dumps(box_json, indent=2, ensure_ascii=False) + "\n").encode())
    write_out(out_root, OUT_TRACES, (json.dumps(traces, indent=2, ensure_ascii=False, default=str) + "\n").encode())
    write_out(out_root, OUT_ACTS, acts.encode(), mode=0o755)
    for rel in OUTPUTS:
        b = (out_root / rel).read_bytes()
        print(f"wrote {rel} · {len(b):,} B · sha256 {hashlib.sha256(b).hexdigest()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
