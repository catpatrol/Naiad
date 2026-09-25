#!/usr/bin/env python
"""TIER-C11 · CLOSE FIXTURES — the build document, the findings, BOX-COST, the ledger append, the acts.

Every leg runs its BREAK leg first (the named plants, each of which must be caught by its NAMED detector,
one at a time), then its REAL leg on the files of record.  A break leg that does not go RED voids the
fixture.  Nothing here writes under exchange/, commits, pushes or calls publish(); the only files written
are the transcript and the scratch area under RUN_ROOT (research_outputs/tierc11/close/, or --root=DIR).

  F-S0-NINE      FAILS IF the draft's §0.2 rows are not the S0_VERDICTS.md §0 table rows byte for byte, or
                 not m rows in FAMILY.json's order, or a row's verdict disagrees with FAMILY.json.
  F-NUM          FAILS IF a trace in TRACES.json does not re-derive from its record (file + field), a
                 verbatim block differs from its source lines, a digit in §0 or in the append prose is
                 neither a traced literal (used exactly its declared number of times), a verified block or
                 cite, a masked token nor a counted exemption, or an R4 ★ cell differs from STAGE_R4.md.
  F-FEAS-0       FAILS IF a §0.3 lens word or number differs from R2_LENS_VERDICTS.json, or the lens set is
                 not the JSON's seven lenses.
  F-LAR11        FAILS IF the append breaks TC10's check_format law (exec'd from TC10's own source), a «cite»
                 does not verify through TC10's verify_quote, a commissioned item is missing, a word claim is
                 false (the tier line's count, the R2 closure — the non-provisional FAILs under the law's caveat,
                 the provisional lenses named with Q4 —, a TC10 state in a tense the landing falsifies, R5's whole
                 collar), the pending stamp is not exactly one (or, --stamped, the filled stamp is not git's
                 count), or the draft's §13 is not the append byte for byte.
  F-BOXCOST      FAILS IF the BOX-COST table differs from a re-derivation from git and publish_exchange's
                 constants (ast, never imported), a box-bound file over FLAG_BYTES is not FLAGGED, the
                 projection (TC10's CLOSE first, the append STAMPED, the sweep) does not re-derive, or the md
                 is not the json.
  F-FNF          FAILS IF the findings md is not the json, a finding lacks class / owner / owner basis /
                 source / status, an id repeats, a harvested text does not re-extract from its locator, an
                 executor-owned finding ranks above an operator-owned one, or the counts are not the rows'.
  F-CLAIMS       FAILS IF a hand-worded claim is not its record's: §0.6's P-AGE-1 label and cohort (the B4 OLD
                 band named REFUSED), the R2 closure (§0.6, §12), TC10's state, the collar above every W2 /
                 head-to-head table, every line of both nesting-grid files in §2.3, §0 opening with R5's chop
                 test, the calibrated reads' SCALE-IN-SAMPLE counts, the document ending with the seven-column
                 table; or a sandbox clone reading 1w PASS does not HALT the generator on its R2 GUARD.
  F-CLOSE-ORDER  FAILS IF close_acts.sh is not valid bash, a fixture run or a push is not guarded by a die, or
                 in a sandbox clone a step-0 gate (TC10 report absent, TC10's half-run close, branch, index,
                 CLOSE files uncommitted, a bent cite source) does not STOP before any push, or steps 0-5 (cut
                 before publish(), against a local bare origin) do not push twice, move the document sha-equal,
                 stamp git's count, append the stamped bytes and commit the residue, or TC10's step-6 'git add'
                 does not reproduce its exit, or the real repository changes.
  F-DET          FAILS IF two generator runs (PYTHONHASHSEED 1 and 20260924, --out-root under RUN_ROOT) differ
                 from each other or from the files of record in any byte.

Run:  export NAIAD_CACHE_DIR=/Users/luis/.cache/naiad/snapshots/tc11_20260925 PYTHONDONTWRITEBYTECODE=1
      ~/venvs/naiad/bin/python scripts/tierc11_close_fixtures.py [leg ...] [--refile-transcript] [--root=DIR]
      ~/venvs/naiad/bin/python scripts/tierc11_close_fixtures.py F-LAR11 --stamped     (close_acts.sh step 3)
Exit: 0 every leg GREEN · 1 a RED leg, a void fixture, or a transcript that is not byte-identical.
"""
from __future__ import annotations

import ast
import datetime as _dt
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
SNAPSHOT = Path.home() / ".cache" / "naiad" / "snapshots" / "tc11_20260925"
LIVE_CACHE = Path.home() / ".cache" / "naiad" / "data_cache"


def guard_env() -> None:
    env = os.environ.get("NAIAD_CACHE_DIR")
    if not env:
        raise SystemExit(f"HALT: NAIAD_CACHE_DIR is unset — the TC11 CLOSE fixtures run only on {SNAPSHOT}")
    norm = Path(os.path.normpath(os.path.expanduser(env)))
    if norm == LIVE_CACHE or LIVE_CACHE in norm.parents:
        raise SystemExit("HALT: NAIAD_CACHE_DIR names the LIVE cache")
    if norm.resolve() != SNAPSHOT.resolve():
        raise SystemExit(f"HALT: NAIAD_CACHE_DIR={norm} is not the TC11 snapshot")
    if os.environ.get("PYTHONDONTWRITEBYTECODE") != "1":
        raise SystemExit("HALT: PYTHONDONTWRITEBYTECODE is not 1")


guard_env()
sys.path.insert(0, str(ROOT / "scripts"))
import tierc10_close_close_ledger_append as LA   # TC10's quote parser / verifier  # noqa: E402

# ═══════════════════════════════════════════════════════════════ paths (re-declared; never imported)
TC11 = "research_outputs/tierc11"
CLOSE = f"{TC11}/close"
CONTRACT = "exchange/queue/2026-09-24_TC11_APOLLO.md"
DRAFT = f"{TC11}/BUILD_DRAFT.md"
APPEND = f"{TC11}/LEDGER_APOLLO_APPEND.md"
S5J = f"{CLOSE}/S5_FINDINGS_NOT_FIXED.json"
S5M = f"{CLOSE}/S5_FINDINGS_NOT_FIXED.md"
BOXM = f"{CLOSE}/BOX_COST.md"
BOXJ = f"{CLOSE}/BOX_COST.json"
TRACES = f"{CLOSE}/TRACES.json"
ACTS = f"{CLOSE}/close_acts.sh"
OUTPUTS = (DRAFT, APPEND, S5J, S5M, BOXM, BOXJ, TRACES, ACTS)
S0MD = f"{TC11}/scores/S0_VERDICTS.md"
FAMILY = f"{TC11}/scores/FAMILY.json"
SCORES = f"{TC11}/scores/SCORES.json"
REGS = f"{TC11}/registrations/REGISTRATIONS.json"
R2J = f"{TC11}/stage_r/R2_LENS_VERDICTS.json"
R4MD = f"{TC11}/stage_r4/STAGE_R4.md"
PUBLISH = "scripts/publish_exchange.py"
TC10_ROOT_MOD = "scripts/tierc10_close_ledger_append_root.py"
GENERATOR = "scripts/tierc11_close.py"
TC10_DOC = "exchange/reports/BUILD_2026-09-21_TIERC10_UNSEEN_RANGES.md"
LEDGER_APOLLO = "exchange/status/LEDGER_APOLLO.md"
DOC = "exchange/reports/BUILD_2026-09-24_TIERC11_EVENTS.md"
TRANSCRIPT = "FIXTURES_CLOSE.txt"
STAMPED = "FIXTURES_CLOSE_LEDGER_STAMPED.txt"
BRANCH = "v12-v1-census"
TC10_MSG = "run research_outputs/tierc10/close/close_acts.sh first (the ledger keeps tier order)"
TC10_ACTS = "research_outputs/tierc10/close/close_acts.sh"
TC10_APPEND = "research_outputs/tierc10/LEDGER_APOLLO_APPEND.md"
TC10_HDR_RE = re.compile(r"(?m)^=== STATUS_APOLLO — \d{4}-\d{2}-\d{2} — TIER-C10 · ")
COLLAR = "tier TIER-E · a SELECTION, not a result · gates nothing"
COLLAR_LINE = f"*{COLLAR}.*"
LENSES = ("5m", "15m", "1h", "4h", "12h", "1d", "1w")
R5MD = f"{TC11}/stage_r/R5_CHOP.md"
NESTMD = f"{TC11}/stage_r/NEST_GRID.md"
LANESMD = f"{TC11}/stage_r/lanes/NEST_GRID_LANES.md"
WMD = f"{TC11}/stage_w/STAGE_W.md"
AMD = f"{TC11}/stage_a/STAGE_A.md"
STAMP_RE = re.compile(r"⟦STAMP AT CLOSE[^⟧\n]*⟧")
FILLED_RE = re.compile(r"(\d+) tierc11 commits, (\d+) on a remote")
VERBATIM_RE = re.compile(r"^<!-- verbatim: ([^:]+):([0-9,\-]+) -->$")
SEEDS = (1, 20260924)
RUN_ROOT = ROOT / CLOSE
LINES: list[str] = []
PASSED: list[str] = []
FAILED: list[str] = []
_TMP_RX = re.compile(r"(/private)?/(var/folders|tmp)/[^\s'\"]+")


def _norm(line: str) -> str:
    line = line.replace(str(RUN_ROOT), "<RUN_ROOT>")
    return _TMP_RX.sub("<tmp>", line).replace(str(ROOT), "<ROOT>").replace(str(Path.home()), "~")


def say(line: str = "") -> None:
    line = _norm(line)
    print(line)
    LINES.append(line)


def clock(line: str) -> None:
    print(f"  [clock · stdout only] {line}")


def rd(rel: str, root: Path = ROOT) -> str:
    return (root / rel).read_text("utf-8")


def rj(rel: str, root: Path = ROOT):
    t = (root / rel).read_text("utf-8")
    if rel.endswith(".jsonl"):
        return [json.loads(x) for x in t.splitlines() if x.strip()]
    return json.loads(t)


def sha_b(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def git(*a: str, cwd: Path = ROOT, check: bool = True, stdin: str | None = None) -> str:
    r = subprocess.run(["git", "-C", str(cwd), *a], capture_output=True, text=True, input=stdin)
    if check and r.returncode != 0:
        raise RuntimeError(f"git {' '.join(a)}: {r.stderr.strip()}")
    return r.stdout


def git_rc(*a: str, cwd: Path = ROOT) -> int:
    return subprocess.run(["git", "-C", str(cwd), *a], capture_output=True, text=True).returncode


def prove(fid: str, title: str, fails_if: str, break_leg, real_leg) -> None:
    """Break first; it must go RED (ok False) or the fixture is VOID."""
    say(f"\n{fid} — {title}")
    say(f"  FAILS IF: {fails_if}")
    try:
        b_ok, b_why = break_leg()
    except BaseException as e:              # noqa: BLE001  a break leg that errors proved nothing
        if isinstance(e, KeyboardInterrupt):
            raise
        b_ok, b_why = True, f"break leg RAISED {type(e).__name__}: {e}"
    say(f"  [BREAK] deliberate violation -> {'RED (correct)' if not b_ok else 'GREEN (FIXTURE IS VOID)'}: {b_why}")
    try:
        r_ok, r_why = real_leg()
    except SystemExit as e:
        r_ok, r_why = False, f"HALT {e}"
    except Exception as e:                  # noqa: BLE001
        r_ok, r_why = False, f"raised {type(e).__name__}: {e}"
    say(f"  [{'PASS' if r_ok else 'FAIL'}] {fid}: {r_why}")
    if b_ok:
        FAILED.append(f"{fid} (break leg did not go RED — fixture proves nothing)")
    elif not r_ok:
        FAILED.append(fid)
    else:
        PASSED.append(fid)


def plants(rows) -> tuple[bool, str]:
    """rows = (name, detector, thunk -> list of findings).  CAUGHT only if a finding names the detector.
    Returns (ok=False, why) when every plant is caught (the break leg goes RED)."""
    caught, bad = [], []
    for name, want, thunk in rows:
        try:
            fs = thunk()
        except SystemExit as e:
            fs = [f"HALT {e}"]
        except Exception as e:              # noqa: BLE001
            bad.append(f"{name}: CRASHED {type(e).__name__}: {e}")
            continue
        if not fs:
            bad.append(f"{name}: not caught (no finding)")
        elif not any(want in f for f in fs):
            bad.append(f"{name}: caught by the WRONG detector ({fs[0][:80]})")
        else:
            caught.append(f"{name} -> {[f for f in fs if want in f][0][:110]}")
    if bad:
        return True, "; ".join(bad)
    return False, f"all {len(rows)} plants caught by their named detector, one at a time: " + " · ".join(caught)


# ═══════════════════════════════════════════════════════════════ shared readers
def section(text: str, start_prefix: str, end_prefix: str | None) -> tuple[int, int]:
    """0-based line indices [s, e) from the line starting start_prefix to the next line starting end_prefix."""
    L = text.split("\n")
    s = [i for i, ln in enumerate(L) if ln.startswith(start_prefix)]
    if len(s) != 1:
        raise RuntimeError(f"section {start_prefix!r} found {len(s)} times")
    e = len(L)
    if end_prefix:
        es = [i for i in range(s[0] + 1, len(L)) if L[i].startswith(end_prefix)]
        e = es[0] if es else len(L)
    return s[0], e


def spans_lines(spec: str) -> list[int]:
    out = []
    for part in spec.split(","):
        if "-" in part:
            a, b = part.split("-")
            out.extend(range(int(a), int(b) + 1))
        else:
            out.append(int(part))
    return out


def verbatim_blocks(text: str) -> list[dict]:
    """Every verbatim marker: its line index, the source, the source lines, the block's lines."""
    L = text.split("\n")
    out = []
    for i, ln in enumerate(L):
        m = VERBATIM_RE.match(ln)
        if m:
            nums = spans_lines(m.group(2))
            out.append({"at": i, "path": m.group(1), "nums": nums, "block": L[i + 1:i + 1 + len(nums)]})
    return out


def check_verbatim(text: str, root: Path = ROOT, only_paths=None) -> list[str]:
    f = []
    for b in verbatim_blocks(text):
        if only_paths and b["path"] not in only_paths:
            continue
        src = (root / b["path"]).read_text("utf-8").split("\n")
        for k, (n, got) in enumerate(zip(b["nums"], b["block"])):
            if n < 1 or n > len(src) or src[n - 1] != got:
                f.append(f"NUM-VERBATIM: {b['path']}:{n} is not the block's line {k + 1} (marker at line {b['at'] + 1})")
                break
    return f


def md_cells(line: str) -> list[str]:
    s = line.strip()
    s = s[1:-1] if s.startswith("|") and s.endswith("|") else s
    return [p.strip() for p in re.split(r"(?<!\\)\|", s)]


# ═══════════════════════════════════════════════════════════════ F-S0-NINE
def s0_findings(draft: str, s0: str, fam: dict) -> list[str]:
    f = []
    s, e = section(draft, "### 0.2 ·", "### 0.3 ·")
    part = "\n".join(draft.split("\n")[s:e])
    blocks = verbatim_blocks(part)
    if len(blocks) != 1:
        return [f"S0-MARKER: §0.2 holds {len(blocks)} verbatim blocks (exactly one is required)"]
    b = blocks[0]
    if b["path"] != S0MD:
        f.append(f"S0-MARKER: §0.2's block cites {b['path']}, not {S0MD}")
    L = s0.split("\n")
    h = [i for i, ln in enumerate(L) if ln.startswith("## §0 table")]
    if len(h) != 1:
        return f + ["S0-SOURCE: the S0_VERDICTS.md '## §0 table' heading is not found exactly once"]
    t = [i for i in range(h[0] + 1, len(L)) if L[i].startswith("|")]
    run = [t[0]]
    for i in t[1:]:
        if i == run[-1] + 1:
            run.append(i)
        else:
            break
    src_rows = [L[i] for i in run]
    if [i + 1 for i in run] != b["nums"]:
        f.append(f"S0-MARKER: the marker's lines {b['nums'][:1]}..{b['nums'][-1:]} are not the §0 table's "
                 f"{run[0] + 1}..{run[-1] + 1}")
    got = b["block"]
    for k in range(max(len(got), len(src_rows))):
        a = got[k] if k < len(got) else None
        c = src_rows[k] if k < len(src_rows) else None
        if a != c:
            f.append(f"S0-ROW-DIFF: row {k + 1} of the §0 table differs byte for byte (draft {str(a)[:50]!r} vs "
                     f"S0 {str(c)[:50]!r})")
            break
    data = got[2:]
    if len(data) != fam["family_m"]:
        f.append(f"S0-COUNT: {len(data)} rows, family_m {fam['family_m']}")
    regs = [md_cells(r)[0].split(" · ")[1] if " · " in md_cells(r)[0] and r.startswith("|") else "?" for r in data]
    want = [r["registration"] for r in fam["rows"]]
    if regs != want[:len(regs)] or len(regs) != len(want):
        f.append(f"S0-ORDER: rows {regs} are not FAMILY.json's order {want}")
    for r, fr in zip(data, fam["rows"]):
        cs = md_cells(r)
        if len(cs) < 5:
            f.append(f"S0-ROW-DIFF: a §0.2 line is not a table row ({r[:50]!r})")
            continue
        cell = cs[4]
        v = fr["verdict_of_record"]
        ok = cell.startswith("CLOSED BY PRECONDITION") if v == "CLOSED_BY_PRECONDITION" else (
            cell == v or cell.startswith(v + " ") or cell.startswith(v + " —") or cell.startswith(v + " ·"))
        if v == "NOT SUPPORTED" and cell.startswith("NOT SUPPORTED — CI wholly below zero"):
            ok = False
        if not ok:
            f.append(f"S0-VERDICT: {fr['registration']} cell {cell[:40]!r} is not FAMILY's {v!r}")
    return f


def s0_break():
    draft, s0, fam = rd(DRAFT), rd(S0MD), rj(FAMILY)
    s, e = section(draft, "### 0.2 ·", "### 0.3 ·")
    L = draft.split("\n")
    row1 = [i for i in range(s, e) if L[i].startswith("| 1 · P-WARN-1")][0]

    def bent_word():
        M = list(L)
        M[row1] = M[row1].replace("| NOT SUPPORTED |", "| SUPPORTED |", 1)
        return s0_findings("\n".join(M), s0, fam)

    def dropped():
        M = [x for i, x in enumerate(L) if not x.startswith("| 9 · P-TP-RNG")]
        return s0_findings("\n".join(M), s0, fam)

    def bent_source():
        return s0_findings(draft, s0.replace("| 1 · P-WARN-1 · 40%", "| 1 · P-WARN-1 · 41%", 1), fam)

    def family_bent():
        f2 = json.loads(json.dumps(fam))
        f2["rows"][0]["verdict_of_record"] = "SUPPORTED"
        return s0_findings(draft, s0, f2)
    return plants([("a verdict word changed in a copy of the draft (row 1 NOT SUPPORTED -> SUPPORTED)", "S0-ROW-DIFF", bent_word),
                   ("row 9 dropped from a copy of the draft", "S0-ROW-DIFF", dropped),
                   ("the source table bent in a copy (a prior)", "S0-ROW-DIFF", bent_source),
                   ("FAMILY.json bent in a copy (row 1's verdict of record)", "S0-VERDICT", family_bent)])


def s0_real():
    fam = rj(FAMILY)
    f = s0_findings(rd(DRAFT), rd(S0MD), fam)
    if f:
        return False, "; ".join(f[:3])
    return True, (f"§0.2 = S0_VERDICTS.md's §0 table byte for byte ({fam['family_m'] + 2} lines: header, separator, "
                  f"{fam['family_m']} rows); order = FAMILY.json's; every verdict cell opens with its "
                  f"verdict_of_record (SUPPORTED: {', '.join(fam['supported'])}; tests spent {fam['tests_spent']})")


# ═══════════════════════════════════════════════════════════════ F-FEAS-0
FEAS_COLS = ("word", "maker_twin", "charter_twin", "tier_e_tuning_word", "tier_e_all_word")


def feas_findings(draft: str, r2: dict) -> list[str]:
    f = []
    s, e = section(draft, "### 0.3 ·", "### 0.4 ·")
    rows = [ln for ln in draft.split("\n")[s:e] if ln.startswith("| ") and not ln.startswith("| lens")]
    got = {}
    for r in rows:
        c = md_cells(r)
        got[c[0]] = c
    if sorted(got) != sorted(r2["lenses"]):
        f.append(f"FEAS-LENS: §0.3 lenses {sorted(got)} != R2_LENS_VERDICTS.json {sorted(r2['lenses'])}")
    for k, v in r2["lenses"].items():
        if k not in got:
            continue
        c = got[k]
        words = [c[1].strip("*"), c[2], c[3], c[4], c[5]]
        for col, w in zip(FEAS_COLS, words):
            if w != v[col]:
                f.append(f"FEAS-WORD: {k} {col} prints {w!r}, the JSON reads {v[col]!r}")
        if v["word"] != v["verdict"]:
            f.append(f"FEAS-WORD: {k} JSON word {v['word']!r} != verdict {v['verdict']!r}")
        nums = [(c[6], str(int(v["n_ranges"]))), (c[7], str(int(v["edge_n_ranges"]))),
                (c[8], f"{float(v['edge_net_h20']):+.8f}"), (c[9], str(v["provisional"]).lower()),
                (c[10], v["scale_in_sample"])]
        for g, w in nums:
            if g != w:
                f.append(f"FEAS-NUM: {k} prints {g!r}, the JSON reads {w!r}")
    return f


def feas_break():
    draft, r2 = rd(DRAFT), rj(R2J)
    L = draft.split("\n")
    s, e = section(draft, "### 0.3 ·", "### 0.4 ·")
    r1h = [i for i in range(s, e) if L[i].startswith("| 1h |")][0]

    def maker():
        M = list(L)
        c = md_cells(M[r1h])
        c[2] = "PASS"
        M[r1h] = "| " + " | ".join(c) + " |"
        return feas_findings("\n".join(M), r2)

    def dropped():
        return feas_findings("\n".join(x for i, x in enumerate(L) if i != r1h), r2)

    def json_bent():
        r = json.loads(json.dumps(r2))
        r["lenses"]["4h"]["word"] = r["lenses"]["4h"]["verdict"] = "PASS"
        return feas_findings(draft, r)

    def num_bent():
        M = list(L)
        M[r1h] = M[r1h].replace("| 816 |", "| 817 |", 1)
        return feas_findings("\n".join(M), r2)
    return plants([("the 1h maker twin flipped to PASS in a copy of the draft", "FEAS-WORD", maker),
                   ("the 1h row dropped", "FEAS-LENS", dropped),
                   ("R2_LENS_VERDICTS.json bent in a copy (4h PASS)", "FEAS-WORD", json_bent),
                   ("the 1h n_ranges bent by one", "FEAS-NUM", num_bent)])


def feas_real():
    r2 = rj(R2J)
    f = feas_findings(rd(DRAFT), r2)
    if f:
        return False, "; ".join(f[:3])
    words = " · ".join(f"{k} {r2['lenses'][k]['word']}" for k in ("5m", "15m", "1h", "4h", "12h", "1d", "1w"))
    makers = sorted({v["maker_twin"] for v in r2["lenses"].values()})
    return True, (f"§0.3 == R2_LENS_VERDICTS.json on all {len(r2['lenses'])} lenses × 5 words × 5 numbers/labels: "
                  f"{words}; maker twins {makers} (the reopening path fails too)")


# ═══════════════════════════════════════════════════════════════ F-NUM — resolver, formats, coverage
def resolve_sel(obj, sel):
    return LA.resolve(obj, sel)


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


def tier_commits(rev: str) -> list[tuple[str, str]]:
    out = []
    for ln in git("log", "--format=%H%x09%s", rev).splitlines():
        h, s = ln.split("\t", 1)
        if s.startswith("tierc11("):
            out.append((h, s))
    return out


def ast_value(text: str, name: str):
    for node in ast.parse(text).body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in node.targets):
            return ast.literal_eval(node.value)
    raise KeyError(name)


def fx_resolve(spec: dict, root: Path = ROOT):
    k = spec["kind"]
    if k == "json":
        v = resolve_sel(rj(spec["path"], root), spec["sel"])
    elif k == "jsonl":
        v = resolve_sel(rj(spec["path"], root)[spec["line"]], spec["sel"])
    elif k == "parquet":
        import pandas as pd
        df = pd.read_parquet(root / spec["path"])
        for c, val in spec["where"].items():
            df = df[df[c].astype(str) == str(val)]
        if len(df) != 1:
            raise RuntimeError(f"parquet selection matched {len(df)} rows")
        v = df.iloc[0][spec["col"]]
        v = v.item() if hasattr(v, "item") else v
    elif k == "text":
        ms = list(re.finditer(spec["re"], rd(spec["path"], root), flags=re.M))
        if len(ms) != 1:
            raise RuntimeError(f"text pattern matched {len(ms)} times")
        v = ms[0].group(1)
    elif k == "git":
        w = spec["what"]
        if w == "tierc11_count_in":
            v = len(tier_commits(spec["rev"]))
        elif w == "tierc11_count_ancestor_of":
            v = sum(1 for h, _ in tier_commits(spec["rev"]) if git_rc("merge-base", "--is-ancestor", h, spec["base"]) == 0)
        elif w == "tierc11_not_ancestor_of":
            v = " ".join(git("rev-parse", "--short=7", h).strip() for h, _ in reversed(tier_commits(spec["rev"]))
                         if git_rc("merge-base", "--is-ancestor", h, spec["base"]) != 0)
        elif w == "subject":
            v = git("log", "-1", "--format=%s", spec["rev"]).strip()
        elif w == "date":
            v = git("log", "-1", "--format=%cI", spec["rev"]).strip()
        elif w == "short":
            v = git("rev-parse", "--short=7", spec["rev"]).strip()
        elif w == "json_leaves":
            a = leaves(json.loads(git("show", f"{spec['base']}:{spec['path']}")))
            b = leaves(json.loads(git("show", f"{spec['rev']}:{spec['path']}")))
            st = spec["stat"]
            v = {"added": len(set(b) - set(a)), "removed": len(set(a) - set(b)),
                 "changed": sum(1 for x in set(a) & set(b) if a[x] != b[x]),
                 "changed_non_string": sum(1 for x in set(a) & set(b) if a[x] != b[x]
                                           and not (isinstance(a[x], str) and isinstance(b[x], str)))}[st]
        else:
            raise RuntimeError(f"unknown git spec {w}")
    elif k == "mdcell":
        # re-read with this suite's own parser: the ONE line starting `heading`, the first table after it, the ONE
        # row whose first cell is `row`, the cell under `col`
        Ls = rd(spec["path"], root).split("\n")
        hs = [i for i, x in enumerate(Ls) if x.startswith(spec["heading"])]
        if len(hs) != 1:
            raise RuntimeError(f"mdcell heading found {len(hs)} times")
        i = hs[0] + 1
        while i < len(Ls) and not Ls[i].startswith("|"):
            i += 1
        head = md_cells(Ls[i])
        hits = []
        j = i + 2
        while j < len(Ls) and Ls[j].startswith("|"):
            c = md_cells(Ls[j])
            if c and c[0] == spec["row"]:
                hits.append(dict(zip(head, c)))
            j += 1
        if len(hits) != 1:
            raise RuntimeError(f"mdcell row matched {len(hits)} times")
        v = hits[0][spec["col"]]
    elif k == "const":
        v = ast_value(rd(spec["path"], root), spec["name"])
        if spec.get("index") is not None:
            v = v[spec["index"]]
    elif k == "file":
        b = (root / spec["path"]).read_bytes()
        v = len(b) if spec["what"] == "bytes" else sha_b(b)
    else:
        raise RuntimeError(f"unknown spec kind {k}")
    if spec.get("agg") == "len":
        v = len(v)
    if spec.get("re_in_value"):
        ms = list(re.finditer(spec["re_in_value"], str(v)))
        if len(ms) != 1:
            raise RuntimeError("re_in_value did not match once")
        v = ms[0].group(1)
    return v


def fx_fmt(fmt: str, v) -> str:
    if fmt == "int":
        return str(int(float(v)))
    if fmt == "intc":
        return f"{int(float(v)):,}"
    m = re.fullmatch(r"f(\d)(s?)", fmt)
    if m:
        return (f"{float(v):+.{m.group(1)}f}" if m.group(2) else f"{float(v):.{m.group(1)}f}")
    if fmt == "str":
        return str(v)
    if fmt == "date":
        return str(v)[:10]
    if fmt == "iso_ms":
        return _dt.datetime.fromtimestamp(int(v) / 1000, _dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    m = re.fullmatch(r"sha(\d+)", fmt)
    if m:
        return str(v)[:int(m.group(1))]
    raise RuntimeError(f"unknown format {fmt}")


def trace_findings(traces: dict) -> list[str]:
    f = []
    for t in traces["traces"]:
        try:
            lit = fx_fmt(t["fmt"], fx_resolve(t["spec"]))
        except Exception as e:                # noqa: BLE001
            f.append(f"NUM-TRACE: {t['key']} does not resolve from {t['spec'].get('path', t['spec'].get('what'))} ({e})")
            continue
        if lit != t["lit"]:
            f.append(f"NUM-TRACE: {t['key']} re-derives {lit!r} from its record, the outputs print {t['lit']!r}")
    return f


ISO_RE = re.compile(r"^\d{4}-\d{2}-\d{2}([T ][0-9:]+(Z|[+-]\d{2}:\d{2})?)?$")
# a statistic's letter glued to a number (n141, p0.03, n<30, sd=1.2, q75) is a MEASURED value, not a name (v6,
# sha256, 12h are names): its digits are NOT covered by the letter-bearing-token mask (the close verifier's m4:
# "n141" would have escaped)
STAT_GLUE = re.compile(r"^(?:n|p|k|m|q|sd|se)[=<>≤≥]?[+\-−]?\d[\d.,]*%?$")
TOKEN_STRIP = "()[]{},;:*\"'`«»|.!?"


def region_text(draft: str, append: str, region: str) -> tuple[str, list[tuple[int, int]]]:
    """(text, hard-masked spans) of a coverage region.  s0: the draft's §0; append: the append's block.
    Hard masks: verbatim blocks (verified by their own check), «cite» + quote lines (verify_quote), headings'
    section numbers, list numbering, HTML comments, the pending stamp, table separator lines."""
    if region == "s0":
        s, e = section(draft, "## 0 · VERDICTS", "## 1 ·")
        L = draft.split("\n")[s:e]
    else:
        L = append.split("\n")
    text = "\n".join(L)
    starts, pos = [], 0
    for ln in L:
        starts.append(pos)
        pos += len(ln) + 1
    masks = []

    def mline(i):
        masks.append((starts[i], starts[i] + len(L[i])))
    for b in verbatim_blocks(text):
        for i in range(b["at"], b["at"] + 1 + len(b["nums"])):
            mline(i)
    for q in LA.parse_quotes(text):
        i = q["at"] - 1
        mline(i)
        j = i + 1
        ind = len(L[i]) - len(L[i].lstrip(" "))
        while j < len(L) and re.match("^" + " " * (ind + 2) + r"[|+] ", L[j]):
            mline(j)
            j += 1
    for i, ln in enumerate(L):
        m = re.match(r"^(#{1,6} [0-9.]+ ·)", ln) or re.match(r"^(\d+\. )", ln)
        if m:
            masks.append((starts[i], starts[i] + len(m.group(1))))
        if ln.startswith("<!--") or re.match(r"^\|[-:| ]+\|$", ln):
            mline(i)
    for m in STAMP_RE.finditer(text):
        masks.append((m.start(), m.end()))
    return text, masks


def coverage_findings(draft: str, append: str, traces: dict, region: str) -> list[str]:
    text, masks = region_text(draft, append, region)
    covered = [False] * len(text)
    for a, b in masks:
        for k in range(a, b):
            covered[k] = True
    want: dict[str, int] = {}
    for t in traces["traces"]:
        n = t["uses"].get(region, 0)
        if n and re.search(r"\d", t["lit"]):
            want[t["lit"]] = want.get(t["lit"], 0) + n
    for x in traces["exemptions"]:
        n = x["uses"].get(region, 0)
        if n:
            want[x["lit"]] = want.get(x["lit"], 0) + n
    f = []
    for lit in sorted(want, key=lambda s: (-len(s), s)):
        cnt = 0
        start = 0
        while True:
            i = text.find(lit, start)
            if i < 0:
                break
            j = i + len(lit)
            start = i + 1
            if any(covered[k] for k in range(i, j)):
                continue
            prev = text[i - 1] if i > 0 else " "
            nxt = text[j] if j < len(text) else " "
            if (prev.isalnum() or prev in "_.§#") or (lit[0].isdigit() and prev in "+-−"):
                continue
            if nxt.isalnum() or nxt == "_" or (nxt == "." and j + 1 < len(text) and text[j + 1].isdigit()):
                continue
            cnt += 1
            for k in range(i, j):
                covered[k] = True
        if cnt != want[lit]:
            f.append(f"NUM-COUNT: {region}: literal {lit!r} printed {cnt}x standalone, traced {want[lit]}x")
    # masked tokens: a letter-bearing token (not an ISO date/time, not a statistic glued to its number) covers its
    # digits
    for m in re.finditer(r"\S+", text):
        tok = m.group(0).strip(TOKEN_STRIP)
        if re.search(r"[A-Za-z_§]", tok) and not ISO_RE.match(tok) and not STAT_GLUE.match(tok):
            for k in range(m.start(), m.end()):
                if text[k].isdigit():
                    covered[k] = True
    for m in re.finditer(r"\d+", text):
        if not all(covered[k] for k in range(m.start(), m.end())):
            ln = text.count("\n", 0, m.start())
            ctx = text.split("\n")[ln].strip()
            f.append(f"NUM-UNTRACED: {region} line {ln + 1}: {m.group(0)!r} in «{ctx[:80]}»")
    return f


def r4_findings(draft: str) -> list[str]:
    f = []
    src = rd(R4MD).split("\n")
    s, e = section(draft, "### 2.4 ·", "## 3 ·")
    hdr = None
    n_rows = 0
    for ln in draft.split("\n")[s:e]:
        if ln.startswith("| lens | event | L+1 cell |"):
            hdr = md_cells(ln)
            continue
        if hdr and ln.startswith("| ") and not ln.startswith("|---"):
            c = dict(zip(hdr, md_cells(ln)))
            if "lines (§4 · §7)" not in c:
                break
            m = re.fullmatch(r":(\d+) · :(\d+)", c["lines (§4 · §7)"])
            if not m:
                f.append(f"NUM-R4: a ★ row carries no line pointer ({ln[:60]})")
                continue
            g, nl = int(m.group(1)), int(m.group(2))
            gh = md_cells(src[[i for i in range(g - 1, 0, -1) if src[i].startswith("| lens | scale | event")][0]])
            nh = md_cells(src[[i for i in range(nl - 1, 0, -1) if src[i].startswith("| lens | event | L+1 cell | dir")][0]])
            G = dict(zip(gh, md_cells(src[g - 1])))
            N = dict(zip(nh, md_cells(src[nl - 1])))
            pairs = [("lens", G["lens"]), ("event", G["event"]), ("L+1 cell", G["L+1 cell"])]
            pairs += [(k, G[k]) for k in ("n ALL H20", "NET ALL H20", "Δcell ALL H20", "NET ALL H100", "Δcell ALL H100",
                                          "n holdout H20", "NET holdout H20", "Δcell holdout H20")]
            pairs += [("null pctile ALL H20", N["pctile ALL H20"]), ("null pctile ALL H100", N["pctile ALL H100"]),
                      ("null pctile holdout H20", N["pctile holdout H20"])]
            for k, v in pairs:
                if c.get(k) != v:
                    f.append(f"NUM-R4: {c.get('lens')} {c.get('event')} {c.get('L+1 cell')} {k} prints {c.get(k)!r}, "
                             f"STAGE_R4.md:{g if 'pctile' not in k else nl} reads {v!r}")
            if not (G["scale"] == "calibrated" and G["law"] == "record" and G["dir"] == "both"
                    and G["L+1 cell"].endswith("*") and N["dir"] == "both"):
                f.append(f"NUM-R4: the pointed rows are not calibrated · record · both · a ★ cell ({g}, {nl})")
            n_rows += 1
    if n_rows == 0:
        f.append("NUM-R4: no ★ row found in §2.4")
    return f


def num_all(draft, append, traces) -> list[str]:
    f = trace_findings(traces)
    f += check_verbatim(draft)
    f += coverage_findings(draft, append, traces, "s0")
    f += coverage_findings(draft, append, traces, "append")
    f += r4_findings(draft)
    return f


def num_break():
    draft, append, traces = rd(DRAFT), rd(APPEND), rj(TRACES)
    tr_only = {"traces": traces["traces"], "exemptions": traces["exemptions"]}

    def s0_plant():
        return coverage_findings(draft.replace("**P-AGE-1 is the only SUPPORTED row", "**P-AGE-1 (+0.9999) is the only "
                                                                                    "SUPPORTED row", 1), append, tr_only, "s0")

    def app_plant():
        return coverage_findings(draft, append.replace("  ALSO FILED\n", "  ALSO FILED\n    - a planted 0.4242 R.\n", 1),
                                 tr_only, "append")

    def glue_plant():
        return coverage_findings(draft.replace("**P-AGE-1 is the only SUPPORTED row", "**P-AGE-1 (n141) is the only "
                                                                                    "SUPPORTED row", 1), append, tr_only, "s0")

    def dup_plant():
        return coverage_findings(draft.replace("Δ +0.2461 R per campaign", "Δ +0.2461 R (+0.2461) per campaign", 1),
                                 append, tr_only, "s0")

    def trace_plant():
        t2 = json.loads(json.dumps(traces))
        for t in t2["traces"]:
            if t["key"] == "P-AGE-1.point":
                t["lit"] = "+0.2462"
        return trace_findings(t2)

    def verb_plant():
        return check_verbatim(draft.replace("| [0,10) | 8 | -0.3976 |", "| [0,10) | 8 | -0.3975 |", 1))

    def r4_plant():
        s, e = section(draft, "### 2.4 ·", "## 3 ·")
        L = draft.split("\n")
        k = [i for i in range(s, e) if L[i].startswith("| 4h | BRK_tap89_first | EXP_ALIGNED* |")][0]
        c = md_cells(L[k])
        c[4] = "+9.999"
        L[k] = "| " + " | ".join(c) + " |"
        return r4_findings("\n".join(L))
    return plants([("an untraceable number (+0.9999) planted in the §0 headline", "NUM-UNTRACED", s0_plant),
                   ("an untraceable number (0.4242) planted in the append's prose", "NUM-UNTRACED", app_plant),
                   ("a number glued to a statistic's letter (n141) planted in the §0 prose", "NUM-UNTRACED", glue_plant),
                   ("a traced literal printed once more than traced (P-AGE-1's point)", "NUM-COUNT", dup_plant),
                   ("a trace's literal bent in a copy of TRACES.json", "NUM-TRACE", trace_plant),
                   ("a line of the R5 verbatim block bent", "NUM-VERBATIM", verb_plant),
                   ("an R4 ★ cell bent (4h tap89 first EXP_ALIGNED* NET ALL H20)", "NUM-R4", r4_plant)])


def num_real():
    draft, append, traces = rd(DRAFT), rd(APPEND), rj(TRACES)
    f = num_all(draft, append, traces)
    if f:
        return False, f"{len(f)} finding(s): " + "; ".join(f[:4])
    nv = len(verbatim_blocks(draft))
    per = {r: sum(t["uses"].get(r, 0) for t in traces["traces"]) for r in ("s0", "append", "s5", "doc")}
    return True, (f"{len(traces['traces'])} traces re-derive from their records (file + field); {nv} verbatim blocks "
                  f"equal their source lines; every digit of §0 and of the append prose is a traced literal used "
                  f"exactly its declared times (uses s0 {per['s0']} · append {per['append']} · s5 {per['s5']} · "
                  f"doc {per['doc']}), a verified block or cite, a masked token or a counted exemption "
                  f"({', '.join(x['lit'] for x in traces['exemptions'])}); {traces['r4_star_rows']} R4 ★ rows equal "
                  "STAGE_R4.md at their pointed lines")


# ═══════════════════════════════════════════════════════════════ F-LAR11
def tc10_check_format():
    """TC10's check_format, exec'd from TC10's own source (the module HALTs off the TC10 snapshot, so it is
    never imported): the FunctionDef and the SEP literal read by ast."""
    src = rd(TC10_ROOT_MOD)
    tree = ast.parse(src)
    fn = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "check_format"][0]
    sep = ast_value(src, "SEP")
    ns = {"re": re, "SEP": sep}
    exec(compile(ast.Module(body=[fn], type_ignores=[]), TC10_ROOT_MOD, "exec"), ns)   # noqa: S102
    return ns["check_format"], sep


def append_sources(append: str, root: Path = ROOT) -> dict:
    out = {}
    for q in LA.parse_quotes(append):
        p = root / q["path"]
        if p.is_file():
            out[q["path"]] = p.read_bytes()
    return out


def r2_span(r2: dict) -> tuple[str, list[str], list[str]]:
    closed = [k for k in LENSES if not r2["lenses"][k]["provisional"]]
    prov = [k for k in LENSES if r2["lenses"][k]["provisional"]]
    return (closed[0] if len(closed) == 1 else f"{closed[0]}–{closed[-1]}") if closed else "", closed, prov


def r2_claims(text: str, r2: dict, where: str) -> list[str]:
    """The R2 sentences (MAJOR-2 of the close verification): the closed set is the non-provisional FAILs, named with
    the law's caveat; every provisional lens is named provisional with the operator's Q4; no 'every lens' closure,
    no 'no reopening path exists'; and every word and maker twin of record reads FAIL (else no sentence is true)."""
    f = []
    flat = " ".join(text.split())
    bad = [f"{k} {fld} {r2['lenses'][k][fld]!r}" for k in LENSES for fld in ("word", "maker_twin")
           if not str(r2["lenses"][k][fld]).startswith("FAIL")]
    if bad:
        f.append(f"CLAIM-R2: {where}: a lens of record does not read FAIL ({bad[:2]}): every range sentence is false")
    span, closed, prov = r2_span(r2)
    if not re.search(r"(?i)clos\w* (?:it|range trading) on " + re.escape(span) + r"\b", flat) and \
            not re.search(r"(?i)range trading is closed on " + re.escape(span) + r"\b", flat):
        f.append(f"CLAIM-R2: {where}: the closed lens set is not named as {span!r} (the non-provisional FAILs)")
    if "unless the toll model changes" not in flat:
        f.append(f"CLAIM-R2: {where}: the R2 law's caveat 'unless the toll model changes' is missing")
    for k in prov:
        if not re.search(r"(?<![0-9A-Za-z])" + re.escape(k) + r".{0,40}(?i:provisional).{0,400}Q4", flat):
            f.append(f"CLAIM-R2: {where}: provisional lens {k} is not named provisional with the operator's Q4")
    if prov and re.search(r"(?i)closed on every lens|clos\w* range trading on every lens|every lens is closed", flat):
        f.append(f"CLAIM-R2: {where}: 'closed on every lens' while {prov} is provisional")
    if re.search(r"(?i)no reopening path exists", flat):
        f.append(f"CLAIM-R2: {where}: 'no reopening path exists' drops the law's 'unless the toll model changes'")
    return f


def tc10_state(root: Path = ROOT) -> bool:
    return (root / TC10_DOC).exists() and bool(TC10_HDR_RE.search((root / LEDGER_APOLLO).read_text("utf-8")))


def tc10_claims(text: str, where: str, root: Path = ROOT) -> list[str]:
    """Nothing about TC10's CLOSE may be stated in a present tense that turns false when the block lands
    (MAJOR-3 of the close verification); the append's tier-line cite follows the repo's TC10 state."""
    f = []
    flat = " ".join(text.split())
    for pat in (r"TC10's CLOSE has not run", r"not yet on this ledger", r"waits for TC10's"):
        if re.search(pat, flat):
            f.append(f"CLAIM-TC10: {where}: present-tense TC10 state ({pat!r}) that is false once the block lands")
    if where == "append":
        # before TC10's CLOSE only its staged file exists to cite; after it, its block on LEDGER_APOLLO (what the
        # generator cites when it runs after TC10's CLOSE) or the staged file (whose wording is true in both states)
        want = {LEDGER_APOLLO, TC10_APPEND} if tc10_state(root) else {TC10_APPEND}
        cites = [q for q in LA.parse_quotes(text) if "TEN TIERS." in q["text"]]
        if len(cites) != 1 or cites[0]["path"] not in want:
            f.append(f"CLAIM-TC10: the tier line cites {[q['path'] for q in cites]}, the TC10 state wants one of "
                     f"{sorted(want)}")
        if cites and cites[0]["path"] == TC10_APPEND and "required on this ledger before this block" not in \
                " ".join(text.split()):
            f.append("CLAIM-TC10: the tier line cites TC10's staged file without the time-invariant wording")
    return f


def lar_findings(append: str, draft: str | None, stamped: bool = False, head_append: str | None = None) -> list[str]:
    f = []
    check_format, sep = tc10_check_format()
    ok, why = check_format(append)
    if not ok:
        f.append(f"LAR-FORMAT: {why}")
    qs = LA.parse_quotes(append)
    src = append_sources(append)
    for q in qs:
        good, why = LA.verify_quote(q, src)
        if not good:
            f.append(f"LAR-CITE: line {q['at']} {LA.cite_of(q)}: {why}")
    fam, regs, r2 = rj(FAMILY), rj(REGS), rj(R2J)
    if f"m = {fam['family_m']}" not in append:
        f.append("LAR-REQUIRED: 'm = family_m' is not printed")
    need = [(CONTRACT, None, None, "SAIL still HELD")]
    if not any(q["path"] == CONTRACT and "m = 9 independently-failable hypotheses (bar 0.10/9)" in q["text"] for q in qs):
        f.append("LAR-REQUIRED: the contract's family clause (m = 9, bar 0.10/9) is not cited")
    for r in regs["registrations"]:
        a, b = r["text_lines"]
        need.append((CONTRACT, a, b, r["registration"]))
        need.append((SCORES, f"rows[registration={r['registration']}].verdict_cell", None, r["registration"]))
    for path, a, b, what in need:
        if path == CONTRACT and a is None:
            hit = [q for q in qs if q["path"] == CONTRACT and "SAIL still HELD" in q["text"]]
        elif isinstance(a, int):
            hit = [q for q in qs if q["path"] == path and q["l1"] == a and q["l2"] == b]
        else:
            hit = [q for q in qs if q["path"] == path and q["sel"] == a]
        if not hit:
            f.append(f"LAR-REQUIRED: no «cite» of {what} ({path} {a or ''}-{b or ''})")
    if not any(q["path"].endswith("FORWARD_LEDGER.md") and "opening" in q["text"] for q in qs):
        f.append("LAR-REQUIRED: the forward ledger's opening is not cited")
    pend = STAMP_RE.findall(append)
    if not stamped:
        if len(pend) != 1:
            f.append(f"LAR-STAMP: {len(pend)} pending stamps (exactly one is required before CLOSE)")
    else:
        if pend:
            f.append("LAR-STAMP: the stamp is still pending in --stamped mode")
        m = FILLED_RE.findall(append)
        if len(m) != 1:
            f.append(f"LAR-STAMP: {len(m)} filled stamps (exactly one)")
        else:
            tc = tier_commits("HEAD")
            off = set(git("rev-list", "HEAD", "--not", "--remotes").split())
            n, mm = len(tc), sum(1 for h, _ in tc if h not in off)
            if (int(m[0][0]), int(m[0][1])) != (n, mm):
                f.append(f"LAR-STAMP: the stamp reads {m[0]}, git reads ({n}, {mm})")
        if head_append is None:
            f.append("LAR-STAMP: no committed pre-stamp append at HEAD to hold the stamped bytes against")
        else:
            fill = FILLED_RE.search(append)
            if fill and STAMP_RE.sub(fill.group(0), head_append, count=1) != append:
                f.append("LAR-STAMP: the stamped append is not the committed pre-stamp append with its one stamp filled")
    # word claims
    n_ns = sum(1 for r in fam["rows"] if r["verdict_of_record"].startswith("NOT SUPPORTED"))
    words = {7: "SEVEN", 8: "EIGHT", 6: "SIX", 5: "FIVE"}
    if f"{words.get(n_ns, '?')} SCORED ROWS DO NOT" not in append:
        f.append(f"LAR-CLAIM: the tier line's count of NOT SUPPORTED rows is not {words.get(n_ns, n_ns)}")
    if "ELEVEN TIERS" not in append or rj(f"{TC11}/PROGRESS.json")["tier"] != "TIER-C11":
        f.append("LAR-CLAIM: 'ELEVEN TIERS' is not the tier of record")
    if "reads FAIL" in append and any(not v["maker_twin"].startswith("FAIL") for v in r2["lenses"].values()):
        f.append("LAR-CLAIM: a maker twin does not read FAIL")
    if fam["supported"] != ["P-AGE-1"] and "ONE IN-SAMPLE RE-SCORE (P-AGE-1" in append:
        f.append("LAR-CLAIM: P-AGE-1 is not the one SUPPORTED row")
    f += [x.replace("CLAIM-", "LAR-CLAIM: ", 1) for x in r2_claims(append, r2, "append")]
    f += [x.replace("CLAIM-", "LAR-CLAIM: ", 1) for x in tc10_claims(append, "append")]
    flat = " ".join(append.split())
    if not re.search(r"R5 \(" + re.escape(COLLAR) + r"\)", flat):
        f.append("LAR-CLAIM: the append's R5 line does not carry the whole collar (tier · SELECTION · gates nothing)")
    if draft is not None and not stamped:
        s, e = section(draft, "## 13 ·", "## 14 ·")
        L = draft.split("\n")[s:e]
        i = L.index("~~~text")
        j = len(L) - 1 - L[::-1].index("~~~")
        inner = "\n".join(L[i + 1:j])
        if inner != append.rstrip("\n"):
            f.append("LAR-S14: the draft's §13 is not the staged append byte for byte")
    return f


def lar_break():
    append, draft = rd(APPEND), rd(DRAFT)

    def end_dropped():
        return lar_findings(append.replace("\n=== END ===\n", "\n"), None)

    def sync_inside():
        return lar_findings(append.replace("  INTEGRITY\n", "  INTEGRITY\n    Operator: click Sync now.\n", 1), None)

    def bent_quote():
        return lar_findings(append.replace("| (m=9; SAIL still HELD; the forward ledger opened)",
                                           "| (m=9; SAIL now RELEASED; the forward ledger opened)", 1), None)

    def sep_missing():
        return lar_findings(append[len("\n---\n\n"):], None)

    def stamp_gone():
        return lar_findings(STAMP_RE.sub("stamp", append), None)

    def cite_gone():
        L = append.split("\n")
        k = [i for i, x in enumerate(L) if x.strip().startswith("«exchange/queue/2026-09-24_TC11_APOLLO.md:83-86»")][0]
        return lar_findings("\n".join(L[:k] + L[k + 5:]), None)

    def s14_bent():
        return lar_findings(append, draft.replace("  SAIL · STILL HELD.", "  SAIL · STILL  HELD.", 1))
    def every_lens():
        return lar_findings(append.replace("range trading is closed on 5m–1d.", "range trading is closed on every "
                                           "lens.", 1), None)

    def tc10_present():
        return lar_findings(append.replace("This block follows TC10's:", "TC10's CLOSE has not run, so this block "
                                           "waits for TC10's:", 1), None)

    def r5_thin():
        return lar_findings(append.replace("R5 (tier TIER-E · a SELECTION, not a result · gates nothing)",
                                           "R5 (Tier-E, a SELECTION, not a result)", 1), None)
    return plants([("the END line dropped", "LAR-FORMAT", end_dropped),
                   ("the session's Sync line inside the block", "LAR-FORMAT", sync_inside),
                   ("the R2 closure widened to 'every lens' (1w is provisional)", "LAR-CLAIM", every_lens),
                   ("TC10's state stated in a present tense", "LAR-CLAIM", tc10_present),
                   ("the R5 line's collar thinned (no 'gates nothing')", "LAR-CLAIM", r5_thin),
                   ("a bent quote (SAIL still HELD -> SAIL now RELEASED)", "LAR-CITE", bent_quote),
                   ("the separator dropped", "LAR-FORMAT", sep_missing),
                   ("the pending stamp removed", "LAR-STAMP", stamp_gone),
                   ("P-TP-RNG's text cite removed", "LAR-REQUIRED", cite_gone),
                   ("the draft's §13 bent (one space)", "LAR-S14", s14_bent)])


def lar_break_stamped():
    """The --stamped break leg: plants on the STAMPED append (the draft is gone by then: LAW 5 moved it)."""
    append = rd(APPEND)
    head = subprocess.run(["git", "-C", str(ROOT), "show", f"HEAD:{APPEND}"], capture_output=True, text=True)
    head_append = head.stdout if head.returncode == 0 else None

    def wrong_count():
        return lar_findings(FILLED_RE.sub(lambda m: f"{m.group(1)} tierc11 commits, {int(m.group(2)) + 1} on a "
                                          "remote", append, count=1), None, stamped=True, head_append=head_append)

    def end_dropped():
        return lar_findings(append.replace("\n=== END ===\n", "\n"), None, stamped=True, head_append=head_append)

    def bent_quote():
        return lar_findings(append.replace("| (m=9; SAIL still HELD; the forward ledger opened)",
                                           "| (m=9; SAIL now RELEASED; the forward ledger opened)", 1), None,
                            stamped=True, head_append=head_append)

    def sync_inside():
        return lar_findings(append.replace("  INTEGRITY\n", "  INTEGRITY\n    Operator: click Sync now.\n", 1), None,
                            stamped=True, head_append=head_append)
    return plants([("the filled stamp's remote count off by one", "LAR-STAMP", wrong_count),
                   ("the END line dropped", "LAR-FORMAT", end_dropped),
                   ("a bent quote (SAIL still HELD -> SAIL now RELEASED)", "LAR-CITE", bent_quote),
                   ("the session's Sync line inside the block", "LAR-FORMAT", sync_inside)])


def lar_real(stamped: bool = False):
    append = rd(APPEND)
    head_append = None
    if stamped:
        r = subprocess.run(["git", "-C", str(ROOT), "show", f"HEAD:{APPEND}"], capture_output=True, text=True)
        head_append = r.stdout if r.returncode == 0 else None
        draft = None
    else:
        draft = rd(DRAFT)
    f = lar_findings(append, draft, stamped=stamped, head_append=head_append)
    extra = ""
    if not stamped:
        # the stamp law, exercised on filled copies (what close_acts.sh step 3 will do after the push)
        tc = tier_commits("HEAD")
        off = set(git("rev-list", "HEAD", "--not", "--remotes").split())
        n, m = len(tc), sum(1 for h, _ in tc if h not in off)
        good = STAMP_RE.sub(f"{n} tierc11 commits, {m} on a remote", append, count=1)
        bad = STAMP_RE.sub(f"{n} tierc11 commits, {m + 1} on a remote", append, count=1)
        fg = [x for x in lar_findings(good, None, stamped=True, head_append=append) if x.startswith("LAR-STAMP")]
        fb = [x for x in lar_findings(bad, None, stamped=True, head_append=append) if x.startswith("LAR-STAMP")]
        if fg or not fb:
            f.append(f"LAR-STAMP: the stamped-mode law does not hold on filled copies (correct fill {fg[:1]}, "
                     f"wrong fill caught: {bool(fb)})")
        extra = ("; the --stamped law exercised on filled copies: git's count passes, a count off by one is "
                 "caught (LAR-STAMP)")
    if f:
        return False, "; ".join(f[:4])
    qs = LA.parse_quotes(append)
    return True, (f"TC10's check_format law holds (exec'd from {TC10_ROOT_MOD}); {len(qs)} «cite»s verify through "
                  f"TC10's verify_quote against {len(append_sources(append))} sources read this run; m, the SAIL hold, "
                  "the nine texts and verdict cells, the forward ledger's opening present; the word claims hold; "
                  + ("the filled stamp equals git's count and the committed pre-stamp append"
                     if stamped else "exactly one pending stamp; the draft's §13 is the append byte for byte")
                  + extra + f"; {len(append.encode()):,} B, sha256 {sha_b(append.encode())[:16]}…")


# ═══════════════════════════════════════════════════════════════ F-BOXCOST
def box_rederive(rows_json: dict, publish_text: str) -> list[str]:
    f = []
    C = rows_json["const"]
    for n in ("BOX_BYTES", "FLAG_BYTES", "SCOPE", "TICK_EXTRA", "WARN_FRACTION", "REFUSE_FRACTION"):
        v = ast_value(publish_text, n)
        v = list(v) if isinstance(v, tuple) else v
        cv = C[n]["value"]
        cv = list(cv) if isinstance(cv, tuple) else cv
        if v != cv:
            f.append(f"BOX-CONST: {n} = {v!r} in publish_exchange.py, the table read {cv!r}")
    BOX = ast_value(publish_text, "BOX_BYTES")
    FLAG = ast_value(publish_text, "FLAG_BYTES")
    scope = ast_value(publish_text, "SCOPE")
    tick_extra = tuple(ast_value(publish_text, "TICK_EXTRA"))
    head = rows_json["git"]["head"]
    # the row set
    a_paths = set()
    cur = False
    for ln in git("log", "--name-status", "--format=%x00%s", head).splitlines():
        if ln.startswith("\x00"):
            cur = ln[1:].startswith("tierc11(")
            continue
        if cur and ln.strip():
            a_paths.update(ln.split("\t")[1:])
    prog = rj(f"{TC11}/PROGRESS.json")
    b_paths = {rel for st in prog["stages"] for rel in st.get("artifact_shas", {})}
    got = {r["path"]: r for r in rows_json["rows"]}
    missing = sorted((a_paths | b_paths | {DOC, LEDGER_APOLLO} | set(OUTPUTS)) - set(got))
    if missing:
        f.append(f"BOX-SET: {len(missing)} path(s) this build created or modified are not rows: {missing[:3]}")
    remote_cache: dict[str, bool] = {}
    for rel, r in got.items():
        if r["set"].startswith("e ·") or r["set"].startswith("d · PLANNED"):
            continue
        tracked = git_rc("ls-files", "--error-unmatch", "--", rel) == 0
        if tracked != r["tracked"].startswith("tracked"):
            f.append(f"BOX-COL: {rel} TRACKED reads {r['tracked']!r}, git says tracked={tracked}")
        last = git("log", "-1", "--format=%h", "--", rel).strip() if tracked else ""
        want_c = f"`{last}`" if last else "not committed"
        if r["committed"] != want_c:
            f.append(f"BOX-COL: {rel} COMMITTED reads {r['committed']!r}, git says {want_c!r}")
        if last:
            if last not in remote_cache:
                remote_cache[last] = bool(git("branch", "-r", "--contains", last).strip())
            want_p = remote_cache[last]
            if r["pushed"].startswith("yes") != want_p:
                f.append(f"BOX-COL: {rel} PUSHED reads {r['pushed']!r}, git says pushed={want_p}")
        boxb = rel.startswith(scope) or rel in tick_extra
        if boxb != r["box_bound"]:
            f.append(f"BOX-COL: {rel} box-bound reads {r['box_bound']}, the constants say {boxb}")
        if r["bytes"] is not None and rel not in OUTPUTS and not r["exists"].startswith("volatile"):
            p = ROOT / rel
            if p.is_file() and p.stat().st_size != r["bytes"]:
                f.append(f"BOX-COL: {rel} bytes {r['bytes']} != disk {p.stat().st_size}")
        if boxb and r["bytes"] is not None:
            size = r["bytes"]
            if rel == LEDGER_APOLLO:
                size = proj_rederive(rows_json)[1]["ledger_after_bytes"]
            if (size > FLAG) != r["flagged"]:
                f.append(f"BOX-FLAG: {rel} ({size:,} B) flagged={r['flagged']} against FLAG_BYTES {FLAG:,}")
        if not boxb and not r["box_cost"].startswith("n/a"):
            f.append(f"BOX-COL: {rel} is not box-bound but its BOX COST reads {r['box_cost']!r}")
    doc = got.get(DOC)
    if doc:
        want = rows_json["draft_bytes"] > FLAG
        if doc["flagged"] != want or doc["bytes"] != rows_json["draft_bytes"]:
            f.append(f"BOX-FLAG: the planned build document is not sized as the draft ({rows_json['draft_bytes']:,} B) "
                     f"or its FLAGGED ({doc['flagged']}) is not the wire's ({want})")
    # the tick set, re-derived
    ex = []
    for rec in git("ls-files", "-s", "-z", "--", scope.rstrip("/")).split("\0"):
        if rec:
            meta, _, path = rec.partition("\t")
            ex.append(meta.split()[1])
    sizes = git("cat-file", "--batch-check", stdin="".join(s + "\n" for s in ex)).split("\n")
    exb = sum(int(x.split()[2]) for x in sizes if x.strip())
    ledb = sum(int(git("ls-tree", "-l", "HEAD", "--", p).split()[3]) for p in tick_extra
               if git("ls-tree", "-l", "HEAD", "--", p).strip())
    if (exb, ledb) != (rows_json["tick"]["exchange_bytes"], rows_json["tick"]["ledger_md_bytes"]):
        f.append(f"BOX-COL: the tick set re-derives to {exb:,} + {ledb:,} B, the table reads "
                 f"{rows_json['tick']['exchange_bytes']:,} + {rows_json['tick']['ledger_md_bytes']:,} B")
    frac = (exb + ledb) / BOX
    # the projection (the close verifier's m3: TC10's CLOSE lands first; the append lands STAMPED), re-derived
    pf, want = proj_rederive(rows_json, exb + ledb)
    f += pf
    for k2, v2 in want.items():
        got = rows_json["projection"].get(k2) if k2 != "tc10" else rows_json["projection"].get("tc10")
        if got != v2:
            f.append(f"BOX-PROJ: projection {k2} reads {got!r}, the re-derivation {v2!r}")
    return f


def proj_rederive(rows_json: dict, tick: int | None = None) -> tuple[list[str], dict]:
    """The CLOSE projection from its parts: this append stamped (the bracket replaced by 'N tierc11 commits, N on a
    remote', N = the tierc11 commits now + the LAW-5 commit), TC10's CLOSE while it has not landed (read from its
    own script's assignments and its staged append), the sweep of uncommitted exchange/ edits."""
    f = []
    head = rows_json["git"]["head"]
    app = rd(APPEND)
    br = STAMP_RE.findall(app)
    n = len(tier_commits(head)) + 1
    stamped = len(app.encode()) - (len(br[0].encode()) if len(br) == 1 else 0) + len(f"{n} tierc11 commits, {n} on a remote".encode())
    if len(br) != 1:
        f.append("BOX-PROJ: the append does not carry exactly one pending stamp")
    tc10 = None
    if not tc10_state():
        acts = rd(TC10_ACTS).split("\n")
        asg = {}
        for ln in acts:
            m = re.match(r"^([A-Z_]+)=(\S+)$", ln)
            if m:
                asg[m.group(1)] = m.group(2)
        a10 = rd(asg["APP"])
        b10 = STAMP_RE.findall(a10)
        n10 = sum(1 for x in git("log", "--format=%s", "HEAD").splitlines() if x.startswith("tierc10")) + 1
        rs = ROOT / asg["RPT_SRC"]
        tc10 = {"doc_path": asg["DOC"], "doc_bytes": (ROOT / asg["DRAFT"]).stat().st_size, "draft_path": asg["DRAFT"],
                "report_path": asg["RPT"], "report_src": asg["RPT_SRC"],
                "report_bytes": rs.stat().st_size if rs.is_file() else 0,
                "append_path": asg["APP"], "append_bytes": len(a10.encode()), "n": n10,
                "append_stamped_bytes": len(a10.encode()) - len(b10[0].encode()) + len(f"{n10} tierc10 commits, {n10} on a remote".encode())}
    sweep = 0
    for pth in [x for x in git("diff", "--name-only", "--", "exchange").splitlines() if x]:
        idx = git("ls-files", "-s", "--", pth).split()
        ib = int(git("cat-file", "-s", idx[1]).strip()) if idx else 0
        sweep += (ROOT / pth).stat().st_size - ib if (ROOT / pth).exists() else -ib
    led_now = (ROOT / LEDGER_APOLLO).stat().st_size
    want = {"tc10": tc10, "append_bytes": len(app.encode()), "append_stamped_bytes": stamped,
            "exchange_sweep_bytes": sweep, "ledger_now_bytes": led_now,
            "ledger_after_bytes": led_now + (tc10["append_stamped_bytes"] if tc10 else 0) + stamped}
    if tick is not None:
        tc10_add = (tc10["doc_bytes"] + tc10["report_bytes"] + tc10["append_stamped_bytes"]) if tc10 else 0
        want["tick_after_bytes"] = tick + tc10_add + (rows_json["draft_bytes"] or 0) + stamped + sweep
    return f, want


def box_md_findings(md: str, rows_json: dict) -> list[str]:
    f = []
    for r in rows_json["rows"]:
        line = (f"| `{r['path']}` | {r['exists']} | {r['tracked']} | {r['committed']} | {r['pushed']} | "
                f"{r['protected_by']} | {r['box_cost']} |")
        if line not in md:
            f.append(f"BOX-MD: the md does not carry the json row of {r['path']}")
            break
    for p in rows_json["flagged"]:
        if f"`{p}`" not in md.split("## The table")[0]:
            f.append(f"BOX-MD: FLAGGED {p} is not named above the table")
    return f


def box_break():
    bj, pub, md = rj(BOXJ), rd(PUBLISH), rd(BOXM)

    def flag_flip():
        b = json.loads(json.dumps(bj))
        for r in b["rows"]:
            if r["path"] == DOC:
                r["flagged"] = not r["flagged"]
        return box_rederive(b, pub)

    def row_drop():
        b = json.loads(json.dumps(bj))
        b["rows"] = [r for r in b["rows"] if r["path"] != CONTRACT]
        return box_rederive(b, pub)

    def const_bent():
        return box_rederive(bj, pub.replace("FLAG_BYTES = 64_000", "FLAG_BYTES = 640_000", 1))

    def pushed_flip():
        b = json.loads(json.dumps(bj))
        for r in b["rows"]:
            if r["path"] == CONTRACT:
                r["pushed"] = "no"
        return box_rederive(b, pub)

    def md_bent():
        return box_md_findings(md.replace("| `exchange/queue/2026-09-24_TC11_APOLLO.md` | yes", "| `exchange/queue/"
                                          "2026-09-24_TC11_APOLLO.md` | no", 1), bj)

    def tc10_dropped():
        b = json.loads(json.dumps(bj))
        b["projection"]["tc10"] = None
        return box_rederive(b, pub)

    def prestamp():
        b = json.loads(json.dumps(bj))
        b["projection"]["append_stamped_bytes"] = b["projection"]["append_bytes"]
        return box_rederive(b, pub)
    return plants([("the projection's TC10 CLOSE dropped (verifier m3)", "BOX-PROJ", tc10_dropped),
                   ("the append projected at its pre-stamp size (verifier m3)", "BOX-PROJ", prestamp),("the planned build document's FLAGGED flipped in a copy of BOX_COST.json", "BOX-FLAG", flag_flip),
                   ("the contract's row dropped", "BOX-SET", row_drop),
                   ("FLAG_BYTES bent in a copy of publish_exchange.py's text", "BOX-CONST", const_bent),
                   ("the contract's PUSHED flipped", "BOX-COL", pushed_flip),
                   ("the md's contract row bent", "BOX-MD", md_bent)])


def box_real():
    bj, pub, md = rj(BOXJ), rd(PUBLISH), rd(BOXM)
    f = box_rederive(bj, pub) + box_md_findings(md, bj)
    draft = rd(DRAFT)
    if not re.search(r"\*\*FLAGGED, named to the operator with its home \(CONVENTIONS §3\.2\):\*\* `" +
                     re.escape(DOC) + "` — this document, over", draft):
        f.append("BOX-FLAG: the draft's §14 does not name the build document FLAGGED with its home")
    if f:
        return False, "; ".join(f[:4])
    return True, (f"{len(bj['rows'])} rows re-derived from git (tracked, committed, pushed) and publish_exchange's "
                  f"constants by ast (BOX_BYTES {bj['const']['BOX_BYTES']['value']:,}, FLAG_BYTES "
                  f"{bj['const']['FLAG_BYTES']['value']:,}); the row set covers every path of the tierc11 commits, "
                  f"every PROGRESS artifact, the CLOSE's files and the two destinations; FLAGGED: "
                  f"{', '.join(bj['flagged'])}; tick set {bj['tick']['tick_bytes']:,} B = {bj['tick']['fraction_pct']} "
                  f"· {bj['tick']['level']}; md == json")


# ═══════════════════════════════════════════════════════════════ F-FNF
def fx_section_items(text: str, heading: str, style: str, stop: str | None) -> list[str]:
    lines = text.split("\n")
    hs = [i for i, ln in enumerate(lines) if ln.startswith(heading)]
    if len(hs) != 1:
        raise RuntimeError(f"section {heading!r} found {len(hs)} times")
    h = hs[0]
    lvl = len(re.match(r"^(#+)", lines[h]).group(1)) if lines[h].startswith("#") else 7
    end = len(lines)
    for i in range(h + 1, len(lines)):
        m = re.match(r"^(#{1,6}) ", lines[i])
        if (m and len(m.group(1)) <= lvl) or (stop and re.match(stop, lines[i])):
            end = i
            break
    rx = {"bold-bullet": r"^- \*\*", "bullet": r"^- ", "numbered": r"^\d+\. ", "fnf": r"^\*\*FNF-\d+ "}[style]
    st = [i for i in range(h + 1, end) if re.match(rx, lines[i])]
    return ["\n".join(lines[s:(st[k + 1] if k + 1 < len(st) else end)]).rstrip() for k, s in enumerate(st)]


def fx_harvest(src: dict) -> str:
    base = resolve_sel(rj(src["path"]), src["field"]) if src.get("field") else rd(src["path"])
    if src["how"] == "item":
        return fx_section_items(base, src["section"], src["style"], src.get("stop"))[src["item"] - 1]
    if src["how"] == "line":
        hits = [ln for ln in base.split("\n") if ln.startswith(src["prefix"])]
        if len(hits) != 1:
            raise RuntimeError("line prefix not unique")
        return hits[0].rstrip()
    raise RuntimeError(f"unknown locator {src}")


def fnf_findings(S: dict, md: str) -> list[str]:
    f = []
    ids = [x["id"] for x in S["findings"]]
    if len(ids) != len(set(ids)):
        f.append(f"FNF-ID: ids repeat: {sorted({i for i in ids if ids.count(i) > 1})}")
    seen_exec = False
    for k, x in enumerate(S["findings"], 1):
        for fld in ("id", "class", "owner", "owner_basis", "source", "status", "text"):
            if not x.get(fld):
                f.append(f"FNF-FIELD: {x.get('id')} lacks {fld}")
        if x.get("class") not in ("HARVESTED", "MEASURED", "LEAN"):
            f.append(f"FNF-FIELD: {x.get('id')} class {x.get('class')!r}")
        if x.get("owner") not in ("operator", "executor"):
            f.append(f"FNF-FIELD: {x.get('id')} owner {x.get('owner')!r}")
        if x.get("status") != "REPORTED, NOT FIXED":
            f.append(f"FNF-FIELD: {x.get('id')} status {x.get('status')!r}")
        if not (x.get("owner_basis") or {}).get("reading"):
            f.append(f"FNF-FIELD: {x.get('id')} owner basis has no reading")
        if x.get("rank") != k:
            f.append(f"FNF-RANK: {x.get('id')} rank {x.get('rank')} at position {k}")
        if x.get("owner") == "executor":
            seen_exec = True
        elif seen_exec:
            f.append(f"FNF-RANK: operator-owned {x['id']} ranks below an executor-owned finding")
        if x.get("class") == "HARVESTED" and x.get("source"):
            try:
                if fx_harvest(x["source"]) != x["text"]:
                    f.append(f"FNF-TEXT: {x['id']}'s text does not re-extract from its locator")
            except Exception as e:           # noqa: BLE001
                f.append(f"FNF-TEXT: {x['id']}'s locator fails ({e})")
        for a in x.get("also_reported_by", []):
            try:
                if fx_harvest(a["source"]) != a["text"]:
                    f.append(f"FNF-TEXT: {x['id']} also-reported text does not re-extract")
            except Exception as e:           # noqa: BLE001
                f.append(f"FNF-TEXT: {x['id']} also-reported locator fails ({e})")
        blk = f"#### {x['id']}\n"
        if blk not in md or ("~~~text\n" + x.get("text", "") + "\n~~~") not in md:
            f.append(f"FNF-MD: {x['id']} is not in the md with its text verbatim")
        head = f"- **{x.get('class')}** · owner **{x.get('owner')}** · status **{x.get('status')}** · rank {x.get('rank')}"
        if head not in md:
            f.append(f"FNF-MD: {x['id']}'s class / owner / status line is not the json's")
    md_ids = re.findall(r"(?m)^#### (\S+)$", md.split("## 3 ·")[0])
    if md_ids != ids:
        f.append(f"FNF-MD: the md's finding ids ({len(md_ids)}) are not the json's ({len(ids)}) in order")
    for c in ("HARVESTED", "MEASURED", "LEAN"):
        for o in ("operator", "executor"):
            n = sum(1 for x in S["findings"] if x.get("class") == c and x.get("owner") == o)
            if S["counts"][c][o] != n:
                f.append(f"FNF-COUNT: {c}/{o} counts {S['counts'][c][o]}, the rows {n}")
    for s in S.get("superseded", []):
        if fx_harvest(s["source"]) != s["text"]:
            f.append(f"FNF-TEXT: superseded {s['id']} does not re-extract")
    return f


def fnf_break():
    S, md = rj(S5J), rd(S5M)

    def dup():
        s = json.loads(json.dumps(S))
        s["findings"][1]["id"] = s["findings"][0]["id"]
        return fnf_findings(s, md)

    def no_owner():
        s = json.loads(json.dumps(S))
        s["findings"][2]["owner"] = ""
        return fnf_findings(s, md)

    def md_bent():
        x = S["findings"][0]["text"]
        return fnf_findings(S, md.replace(x, x.replace("late entries", "early entries", 1), 1))

    def text_bent():
        s = json.loads(json.dumps(S))
        s["findings"][3]["text"] = s["findings"][3]["text"].replace("R", "R ", 1)
        return fnf_findings(s, md)

    def rank_swap():
        s = json.loads(json.dumps(S))
        e = [i for i, x in enumerate(s["findings"]) if x["owner"] == "executor"][0]
        s["findings"].insert(0, s["findings"].pop(e))
        for i, x in enumerate(s["findings"], 1):
            x["rank"] = i
        return fnf_findings(s, md)

    def count_bent():
        s = json.loads(json.dumps(S))
        s["counts"]["HARVESTED"]["operator"] += 1
        return fnf_findings(s, md)
    return plants([("a duplicated id", "FNF-ID", dup), ("an owner blanked", "FNF-FIELD", no_owner),
                   ("the md's first text bent", "FNF-MD", md_bent), ("a harvested text bent in the json", "FNF-TEXT", text_bent),
                   ("an executor-owned finding moved to rank 1", "FNF-RANK", rank_swap),
                   ("a count bent", "FNF-COUNT", count_bent)])


def fnf_real():
    S, md = rj(S5J), rd(S5M)
    f = fnf_findings(S, md)
    if f:
        return False, "; ".join(f[:4])
    c = S["counts"]
    also = sum(len(x["also_reported_by"]) for x in S["findings"])
    return True, (f"{c['all']['total']} findings (operator {c['all']['operator']}, executor {c['all']['executor']}; "
                  f"HARVESTED {c['HARVESTED']['total']}, MEASURED {c['MEASURED']['total']}, LEAN {c['LEAN']['total']}), "
                  f"ids unique, operator-owned first, every harvested text and its {also} merged duplicates re-extract "
                  f"from their locators, {len(S['superseded'])} superseded items re-extract; md == json")


# ═══════════════════════════════════════════════════════════════ F-CLAIMS
def draft_sections(draft: str, start: str, end: str | None) -> str:
    s, e = section(draft, start, end)
    return "\n".join(draft.split("\n")[s:e])


def claims_findings(draft: str, append: str, bj: dict, root: Path = ROOT) -> list[str]:
    """The hand-worded claims of §0, §2.3, §3, §7, §12 and the document's end, each held against its record (the
    close verification's MAJOR-1..5, m8, m10)."""
    f = []
    scores, r2 = rj(SCORES, root), rj(R2J, root)
    ag = [r for r in scores["rows"] if r["registration"] == "P-AGE-1"][0]
    words = draft_sections(draft, "### 0.6 ·", "## 1 ·")
    b1 = [ln for ln in words.split("\n") if ln.startswith("1. **P-AGE-1")]
    # HONESTY (MAJOR-1's row; mutation M1): the label printed is the scorer's, never a stronger word
    m = re.match(r"^SUPPORTED — ([A-Z][A-Z ,-]*?) \(", ag["verdict_cell"])
    if not m or len(b1) != 1:
        f.append("CLAIM-HONESTY: the P-AGE-1 bullet or the scorer's label is not found")
    else:
        if f"it is an {m.group(1)}." not in b1[0]:
            f.append(f"CLAIM-HONESTY: §0.6's P-AGE-1 bullet does not print the scorer's label {m.group(1)!r}")
        if re.search(r"\bCONFIRMED\b|\bOUT[- ]OF[- ]SAMPLE\b", b1[0]):
            f.append("CLAIM-HONESTY: §0.6's P-AGE-1 bullet claims confirmation / out-of-sample")
        # COHORT (MAJOR-1): the cohort is the scorer's pre_seen clause; the B4 OLD band is the REFUSED one
        c = re.match(r"^(the scored cohort IS [^(;]*?) \(", ag["labels"]["pre_seen"])
        band = re.search(r"\((B4 OLD);", ag["provenance"]["scored"]["description"])
        if not c or c.group(1) not in b1[0]:
            f.append("CLAIM-COHORT: §0.6's P-AGE-1 bullet does not carry the scorer's pre_seen cohort clause")
        if not band or f"with the {band.group(1)} band refused" not in b1[0]:
            f.append("CLAIM-COHORT: §0.6 does not name the B4 OLD band as the REFUSED cohort")
        if re.search(r"(?i)scored cohort is [^.]{0,40}B4 OLD", b1[0]):
            f.append("CLAIM-COHORT: §0.6 calls the B4 OLD band the scored cohort (it is the refused one)")
    # R2 (MAJOR-2): §0.6's bullet and §12's line
    b3 = [ln for ln in words.split("\n") if ln.startswith("3. **")]
    f += r2_claims(b3[0] if b3 else "", r2, "§0.6")
    s12 = [ln for ln in draft_sections(draft, "## 12 ·", "## 13 ·").split("\n") if "range trading" in ln]
    f += [x for x in r2_claims(s12[0] if s12 else "", r2, "§12") if "not named as" not in x]
    span = r2_span(r2)[0]
    if not s12 or f"the {span} lenses are closed" not in s12[0]:
        f.append(f"CLAIM-R2: §12 does not name the closed lenses {span}")
    # TC10 (MAJOR-3)
    f += tc10_claims(draft, "draft", root)
    # COLLARS (MAJOR-4): every table the draft copies into §3.2-§3.5 and §7's head-to-head stands under the collar
    L = draft.split("\n")
    hh = [i + 1 for i, x in enumerate(rd(AMD, root).split("\n")) if x.startswith("## 3 · HEAD-TO-HEAD")]
    s3, e3 = section(draft, "### 3.2 ·", "## 4 ·")
    s7, e7 = section(draft, "## 7 ·", "## 8 ·")
    n_tab = 0
    for b in verbatim_blocks(draft):
        in3 = s3 <= b["at"] < e3 and b["path"] == WMD
        in7 = s7 <= b["at"] < e7 and b["path"] == AMD and hh and min(b["nums"]) >= hh[0]
        if not (in3 or in7):
            continue
        for k, x in enumerate(b["block"]):
            if x.startswith("|") and (k == 0 or not b["block"][k - 1].startswith("|")):
                n_tab += 1
                prev = [y for y in L[:b["at"]] if y.strip()][-1:]
                if k != 0 or prev != [COLLAR_LINE]:
                    f.append(f"CLAIM-COLLAR: the table at {b['path']}:{b['nums'][k]} (draft line {b['at'] + 2 + k}) "
                             "does not stand directly under the collar line")
    if n_tab == 0:
        f.append("CLAIM-COLLAR: no W2 / head-to-head table found in §3.2-§3.5 / §7")
    # NEST WHOLE (MAJOR-5): every line of both grid files is in §2.3 (a verbatim line, or an H1/H2 re-printed as H4)
    s23, e23 = section(draft, "### 2.3 ·", "### 2.4 ·")
    part = L[s23:e23]
    for rel in (NESTMD, LANESMD):
        got = set()
        for b in verbatim_blocks("\n".join(part)):
            if b["path"] == rel:
                got.update(b["nums"])
        labels = {x[5:] for x in part if x.startswith("#### ")}
        src = rd(rel, root).split("\n")
        miss = [n for n, x in enumerate(src, 1) if x.strip() and n not in got
                and not (re.match(r"^#{1,2} ", x) and x.split(" ", 1)[1] in labels)]
        if miss:
            f.append(f"CLAIM-NEST: {rel}: {len(miss)} non-blank line(s) not printed in §2.3 (first {miss[:3]})")
    # ORDER (m8): §0 opens with R5's chop test, then the nine rows, then the feasibility verdicts
    s0, e0 = section(draft, "## 0 · VERDICTS", "## 1 ·")
    subs = [x for x in L[s0:e0] if x.startswith("### 0.")]
    if not subs or not subs[0].startswith("### 0.1 · R5's chop table") or \
            [x[:9] for x in subs] != ["### 0.1 ·", "### 0.2 ·", "### 0.3 ·", "### 0.4 ·", "### 0.5 ·", "### 0.6 ·"]:
        f.append(f"CLAIM-ORDER: §0's subsections are not 0.1 (R5's chop test) .. 0.6 in order ({[x[:12] for x in subs]})")
    s01 = draft_sections(draft, "### 0.1 ·", "### 0.2 ·")
    if not any(b["path"] == R5MD for b in verbatim_blocks(s01)):
        f.append("CLAIM-ORDER: §0.1 does not carry R5's chop table")
    first = [x for x in L[s0 + 1:e0] if x.strip()][:3]
    if any(x.startswith(("1. ", "2. ", "- ")) for x in first):
        f.append("CLAIM-ORDER: §0 opens with bullets before R5's chop test")
    # IN-SAMPLE (m8): every calibrated read in §0.1's answer carries its SCALE-IN-SAMPLE count inline
    for x in s01.split("\n"):
        if x.startswith("- calibrated ") and "SCALE-IN-SAMPLE:" not in x:
            f.append(f"CLAIM-INSAMPLE: {x[:50]!r} has no SCALE-IN-SAMPLE count inline")
    # END (m10): the document ends with the seven-column disposition table, covering every BOX-COST row
    heads = [x for x in L if x.startswith("## ")]
    tail = [x for x in L if x.strip()]
    hdr = "| PATH | EXISTS | TRACKED | COMMITTED | PUSHED | PROTECTED BY | BOX COST |"
    if not heads or not heads[-1].startswith("## 14 · DISPOSITION") or hdr not in L:
        f.append("CLAIM-END: the last section is not the disposition, or it carries no seven-column table")
    else:
        h = max(i for i, x in enumerate(L) if x == hdr)
        rows = [x for x in L[h + 2:] if x.strip()]
        if not rows or not all(x.startswith("| ") for x in rows) or tail[-1] != rows[-1]:
            f.append("CLAIM-END: the document does not END with the seven-column table")
        cover = sum(int(m2.group(1)) if (m2 := re.match(r"^\| \*\*(\d+) paths\*\*", x)) else 1 for x in rows)
        if cover != bj["n_rows"]:
            f.append(f"CLAIM-END: the table covers {cover} rows, BOX_COST.json has {bj['n_rows']}")
    return f


def guard_findings(base: Path, gen_text: str | None = None) -> list[str]:
    """The generator's R2 GUARD (mutation M4): in a sandbox clone whose R2_LENS_VERDICTS.json reads 1w PASS, the
    generator must HALT with 'R2 GUARD' before writing anything."""
    sb = make_sandbox(base)
    if gen_text is not None:
        (sb / GENERATOR).write_text(gen_text, "utf-8")
    p = sb / R2J
    r = json.loads(p.read_text("utf-8"))
    r["lenses"]["1w"]["word"] = r["lenses"]["1w"]["verdict"] = "PASS"
    p.write_text(json.dumps(r, indent=2), "utf-8")
    out = base / "gen_out"
    rr = subprocess.run([sys.executable, str(sb / GENERATOR), f"--out-root={out}"], capture_output=True, text=True,
                        env=dict(os.environ), timeout=600)
    tail = (rr.stdout + rr.stderr).strip()
    f = []
    if rr.returncode == 0 or "R2 GUARD" not in tail:
        f.append(f"CLAIM-GUARD: with 1w PASS the generator exited {rr.returncode} without the R2 GUARD HALT "
                 f"({tail.splitlines()[-1][:90] if tail else ''!r})")
    if out.exists() and any(out.rglob("*.md")):
        f.append("CLAIM-GUARD: the generator wrote outputs before its R2 GUARD")
    return f


def claims_break():
    draft, append, bj = rd(DRAFT), rd(APPEND), rj(BOXJ)

    def honesty():
        return claims_findings(draft.replace("it is an IN-SAMPLE RE-SCORE, NOT CONFIRMATORY.",
                                             "it is CONFIRMED out of sample.", 1), append, bj)

    def cohort():
        return claims_findings(re.sub(r"reads: the scored cohort IS [^—]*— v6 \(n \d+\) with the B4 OLD band refused",
                                      "reads: the scored cohort is TC10's filed B4 OLD band", draft, count=1), append, bj)

    def every_lens():
        return claims_findings(draft.replace("**The R2 law closes range trading on 5m–1d.**",
                                             "**Range trading is closed on every lens.**", 1), append, bj)

    def tc10():
        return claims_findings(draft.replace("This CLOSE follows TC10's:", "TC10's CLOSE has not run, so this CLOSE "
                                             "waits for it:", 1), append, bj)

    def collar():
        L = draft.split("\n")
        s3, _ = section(draft, "### 3.2 ·", "## 4 ·")
        k = [i for i in range(s3, len(L)) if L[i] == COLLAR_LINE][0]
        return claims_findings("\n".join(L[:k] + L[k + 1:]), append, bj)

    def nest():
        L = draft.split("\n")
        k = [i for i, x in enumerate(L) if x.startswith(f"<!-- verbatim: {LANESMD}:")][-1]
        m = VERBATIM_RE.match(L[k])
        nums = spans_lines(m.group(2))
        L2 = L[:k] + [f"<!-- verbatim: {LANESMD}:{nums[0]}-{nums[-1] - 1} -->"] + L[k + 1:k + len(nums)] + L[k + 1 + len(nums):]
        return claims_findings("\n".join(L2), append, bj)

    def order():
        s, e = section(draft, "### 0.6 ·", "## 1 ·")
        s1, _ = section(draft, "### 0.1 ·", "### 0.2 ·")
        L = draft.split("\n")
        moved = L[s:e]
        rest = L[:s] + L[e:]
        return claims_findings("\n".join(rest[:s1] + moved + rest[s1:]), append, bj)

    def insample():
        return claims_findings(re.sub(r"(- calibrated 4h: n \d+) \(SCALE-IN-SAMPLE: \d+ of them read in-sample\)",
                                      r"\1", draft, count=1), append, bj)

    def end():
        L = draft.split("\n")
        s, e = section(draft, "## 13 ·", "## 14 ·")
        return claims_findings("\n".join(L[:s] + L[e:] + L[s:e]), append, bj)

    def guard_gone():
        base = fresh_base("claims_break")
        try:
            g = rd(GENERATOR)
            g2 = re.sub(r"(?m)^    # THE R2 GUARD\..*?(?=^    X\[\"r2_closed\"\])", "", g, flags=re.S)
            g2 = g2.replace('halt(f"R2 GUARD: the non-provisional', 'halt(f"R2 CHECK: the non-provisional', 1)
            if g2 == g:
                return ["CLAIM-GUARD: the plant could not remove the guard (anchor moved)"]
            return guard_findings(base, g2)
        finally:
            shutil.rmtree(base, ignore_errors=True)
    return plants([("the P-AGE-1 honesty label bent to 'CONFIRMED out of sample' (mutation M1)", "CLAIM-HONESTY", honesty),
                   ("the cohort bent back to 'TC10's filed B4 OLD band' (MAJOR-1)", "CLAIM-COHORT", cohort),
                   ("§0.6 bent to 'closed on every lens' (MAJOR-2)", "CLAIM-R2", every_lens),
                   ("§0.6 bent to a present-tense TC10 state (MAJOR-3)", "CLAIM-TC10", tc10),
                   ("the collar above a W2 table deleted (MAJOR-4)", "CLAIM-COLLAR", collar),
                   ("the lanes grid's last line dropped from §2.3 (MAJOR-5)", "CLAIM-NEST", nest),
                   ("§0.6 moved above R5's chop test (m8)", "CLAIM-ORDER", order),
                   ("the calibrated 4h read's SCALE-IN-SAMPLE count dropped (m8)", "CLAIM-INSAMPLE", insample),
                   ("the append section moved after the disposition (m10)", "CLAIM-END", end),
                   ("the generator's R2 GUARD removed, run on a 1w-PASS sandbox (mutation M4)", "CLAIM-GUARD", guard_gone)])


def claims_real():
    draft, append, bj = rd(DRAFT), rd(APPEND), rj(BOXJ)
    f = claims_findings(draft, append, bj)
    if f:
        return False, "; ".join(f[:4])
    base = fresh_base("claims_real")
    try:
        g = guard_findings(base)
    finally:
        shutil.rmtree(base, ignore_errors=True)
    if g:
        return False, "; ".join(g)
    span, closed, prov = r2_span(rj(R2J))
    return True, ("§0.6's P-AGE-1 bullet prints the scorer's own label and pre_seen cohort, the B4 OLD band named as "
                  f"the REFUSED one; the R2 sentences (§0.6, §12) close {span} under the law's caveat, {prov} "
                  "provisional with Q4; no present-tense TC10 state; every W2 / head-to-head table in §3.2-§3.5 and §7 "
                  "stands under the collar line; §2.3 prints every line of NEST_GRID.md and NEST_GRID_LANES.md; §0 "
                  "opens with R5's chop test (0.1 .. 0.6 in order), every calibrated read with its SCALE-IN-SAMPLE "
                  f"count; the document ends with the seven-column table covering all {bj['n_rows']} BOX-COST rows; "
                  "and in a sandbox clone reading 1w PASS the generator HALTs on its R2 GUARD, writing nothing")


# ═══════════════════════════════════════════════════════════════ F-CLOSE-ORDER
SB_GIT = ("-c", "user.name=tc11-close-sandbox", "-c", "user.email=sandbox@invalid", "-c", "commit.gpgsign=false")
CLOSE_FILES = (DRAFT, APPEND, S5J, S5M, BOXM, BOXJ, TRACES, ACTS, f"{CLOSE}/COMPUTE_LEDGER.json",
               f"{CLOSE}/TC11_FIX_VERIFY.json", f"{CLOSE}/{TRANSCRIPT}", GENERATOR, "scripts/tierc11_close_fixtures.py",
               f"{TC11}/review/attest/fix-head.json")
SANDBOX_STOP = "SANDBOX-STOP before step 6 (publish() is never called by this suite)"


def tree_state(sb: Path) -> dict:
    h = hashlib.sha256()
    for dp, dn, fn in os.walk(sb):
        dn[:] = sorted(d for d in dn if d != ".git")
        for x in sorted(fn):
            p = Path(dp) / x
            h.update(str(p.relative_to(sb)).encode())
            h.update(p.read_bytes() if p.is_file() and not p.is_symlink() else b"<link>")
    return {"tree": h.hexdigest(), "head": git("rev-parse", "HEAD", cwd=sb).strip(),
            "porcelain": git("status", "--porcelain", "--untracked-files=all", cwd=sb),
            "refs": git("for-each-ref", cwd=sb)}


def make_sandbox(base: Path, acts_text: str | None = None, name: str = "sandbox") -> Path:
    sb = base / name
    if sb.exists():
        shutil.rmtree(sb)
    subprocess.run(["git", "clone", "--quiet", "--shared", "--branch", BRANCH, str(ROOT), str(sb)], check=True,
                   capture_output=True)
    git("remote", "set-url", "origin", str(base / "no-such-remote.git"), cwd=sb)
    for rel in set(OUTPUTS) | set(CLOSE_FILES):
        src = ROOT / rel
        if src.is_file() and not (sb / rel).exists():
            (sb / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, sb / rel)
    if acts_text is not None:
        (sb / ACTS).write_text(acts_text, "utf-8")
    return sb


def sb_commit(sb: Path, paths: list[str], msg: str) -> None:
    git(*SB_GIT, "add", "-f", "--", *paths, cwd=sb)
    git(*SB_GIT, "commit", "-q", "-m", msg, cwd=sb)


def sim_tc10(sb: Path, commit: bool = True, doc_tracked: bool = True) -> None:
    """TC10's CLOSE, simulated in the sandbox: its build document in exchange/reports, its staged append on the
    ledger; committed (the finished close) or left as TC10's script leaves them when it stops at its step 6."""
    (sb / TC10_DOC).parent.mkdir(parents=True, exist_ok=True)
    (sb / TC10_DOC).write_bytes((ROOT / "research_outputs/tierc10/BUILD_DRAFT.md").read_bytes())
    led = sb / LEDGER_APOLLO
    led.write_bytes(led.read_bytes() + (ROOT / TC10_APPEND).read_bytes())
    if commit:
        sb_commit(sb, [TC10_DOC, LEDGER_APOLLO], "tc10(CLOSE, simulated in the TC11 close sandbox)")
    elif doc_tracked:
        sb_commit(sb, [TC10_DOC], "tc10(CLOSE, simulated: the report only)")


def sb_close_commit(sb: Path) -> None:
    sb_commit(sb, list(CLOSE_FILES), "tierc11(CLOSE): the CLOSE files (simulated in the TC11 close sandbox)")


def sb_origin(base: Path, sb: Path, name: str = "origin.git") -> Path:
    """A local bare origin sharing the real repo's objects (read-only alternates): pushes land there, never on the
    real remote."""
    o = base / name
    shutil.rmtree(o, ignore_errors=True)
    subprocess.run(["git", "clone", "--quiet", "--bare", "--shared", str(ROOT), str(o)], check=True, capture_output=True)
    git("remote", "set-url", "origin", str(o), cwd=sb)
    if git("remote", "get-url", "--push", "origin", cwd=sb).strip() != str(o):
        raise RuntimeError("the sandbox's push URL is not the local bare origin")
    git("fetch", "-q", "origin", cwd=sb)
    return o


def truncated(acts: str) -> str:
    """close_acts.sh cut before step 6: this suite never calls publish()."""
    k = acts.index("STEP=6;")
    return acts[:k] + f'echo "{SANDBOX_STOP}"\nexit 0\n'


def run_acts(sb: Path, *args: str, script: str | None = None) -> tuple[int, str]:
    env = dict(os.environ)
    path = sb / ACTS
    if script is not None:
        path = sb / CLOSE / "close_acts_sandbox.sh"
        path.write_text(script, "utf-8")
    r = subprocess.run(["bash", str(path), *args], capture_output=True, text=True, env=env, timeout=600)
    return r.returncode, re.sub(r"\x1b\[[0-9;]*m", "", r.stdout + r.stderr)


def last_line(out: str) -> str:
    return out.strip().splitlines()[-1][:110] if out.strip() else ""


def order_findings(sb: Path, args=()) -> list[str]:
    f = []
    before = tree_state(sb)
    rc, out = run_acts(sb, *args)
    after = tree_state(sb)
    if before != after:
        f.append(f"ORDER-CHANGED: the sandbox changed ({[k for k in before if before[k] != after[k]]})")
    if rc == 0 or "STOPPED at step 0:" not in out or TC10_MSG not in out:
        f.append(f"ORDER-GATE: with TC10's report absent the script did not STOP at step 0 with the TC10 message "
                 f"(exit {rc}; last line {last_line(out)!r})")
    return f


def guard_static(acts: str) -> list[str]:
    """Every irreversible act is guarded by a die (mutation M2: a step-3 F-LAR11 failure that prints instead of dying
    must be caught); step 0 carries the TC10 gates and the pre-stamp F-LAR11 gate before anything is pushed."""
    f = []
    L = acts.split("\n")
    if "set -euo pipefail" not in L:
        f.append("ORDER-GUARD: 'set -euo pipefail' is missing")
    for i, ln in enumerate(L, 1):
        if re.search(r"\|\|\s*(echo|true|:|printf)\b", ln):
            f.append(f"ORDER-GUARD: line {i} swallows a failure ({ln.strip()[:60]!r})")
        if '"$FIXT"' in ln and not re.search(r'\|\| die "[^"]+"\s*$', ln):
            f.append(f"ORDER-GUARD: line {i} runs the fixtures without '|| die' ({ln.strip()[:60]!r})")
        if re.match(r"^git push ", ln) and not re.search(r'\|\| die "[^"]+"\s*$', ln):
            f.append(f"ORDER-GUARD: line {i} pushes without '|| die'")
    s1 = next((i for i, ln in enumerate(L) if ln.startswith("STEP=1;")), len(L))
    pre = "\n".join(L[:s1])
    for need, why in (('"$FIXT" F-LAR11 --root=', "the pre-stamp F-LAR11 gate"),
                      ('git ls-files --error-unmatch -- "$TC10_DOC"', "TC10's report tracked"),
                      ('git diff --quiet HEAD -- "$LEDGER"', "TC10's block committed")):
        if need not in pre:
            f.append(f"ORDER-GUARD: step 0 lacks {why} before the first push")
    return f


def fresh_base(name: str) -> Path:
    base = RUN_ROOT / "_det_close_order" / name
    shutil.rmtree(base, ignore_errors=True)
    base.mkdir(parents=True)
    return base


def bend_source(sb: Path) -> None:
    """A committed one-line edit to a source the append cites (the verifier's m1 case: a Q5 refresh)."""
    p = sb / f"{TC11}/forward/FORWARD_LEDGER.md"
    t = p.read_text("utf-8").split("\n")
    t[4] = t[4].replace("opening 2026-09-21T16:00:00Z", "opening 2026-09-21T20:00:00Z", 1)
    p.write_text("\n".join(t), "utf-8")
    sb_commit(sb, [f"{TC11}/forward/FORWARD_LEDGER.md"], "tierc11(FWD): a refresh (simulated)")


def prepush_findings(base: Path, acts_text: str) -> list[str]:
    """A bent cite source is committed after the CLOSE commit: step 0's F-LAR11 gate must stop the script before
    any push (the bare origin unchanged)."""
    sb = make_sandbox(base, name="sb_bent")
    sim_tc10(sb)
    sb_close_commit(sb)
    bend_source(sb)
    o = sb_origin(base, sb, "origin_bent.git")
    tip0 = git("rev-parse", BRANCH, cwd=o).strip()
    rc, out = run_acts(sb, script=truncated(acts_text))
    tip1 = git("rev-parse", BRANCH, cwd=o).strip()
    f = []
    if tip1 != tip0:
        f.append("ORDER-PREPUSH: a bent cite source let the script push (the bare origin moved) before F-LAR11 stopped it")
    if rc == 0 or "STOPPED at step 0:" not in out or "F-LAR11" not in out:
        f.append(f"ORDER-PREPUSH: with a bent cite source the script did not STOP at step 0 on F-LAR11 ({last_line(out)!r})")
    return f


def halfrun_findings(base: Path, acts_text: str) -> list[str]:
    """TC10's script stopped at its step 6 (report untracked, block appended but uncommitted, its two files staged):
    step 0 must stop on the TC10 gate that names the cause."""
    sb = make_sandbox(base, acts_text, name="sb_half")
    sim_tc10(sb, commit=False, doc_tracked=False)
    for rel in (TC10_APPEND, "research_outputs/tierc10/close/FIXTURES_CLOSE_ledger_append_root.txt"):
        p = sb / rel
        if p.is_file():
            p.write_bytes(p.read_bytes() + b"\n")
            subprocess.run(["git", "-C", str(sb), "add", "--", rel], capture_output=True, text=True)
    rc, out = run_acts(sb, "--check")
    f = []
    if rc == 0 or "TC10's CLOSE did not finish" not in out or "FN-M-TC10-ACTS-IGNORED" not in out:
        f.append(f"ORDER-TC10: TC10's half-run close did not stop step 0 on the named TC10 gate ({last_line(out)!r})")
    return f


def order_break():
    base = fresh_base("break")
    try:
        acts = rd(ACTS)

        def gate_gone():
            t = re.sub(r"if \[ ! -f \"\$TC10_DOC\" \].*?\nfi\n", "", acts, flags=re.S)
            sb = make_sandbox(base, t)
            return order_findings(sb, ("--check",))

        def changes():
            t = acts.replace('STEP=0; say "0 · preconditions"', 'STEP=0; say "0 · preconditions"\ntouch "$ROOT/PLANTED"', 1)
            sb = make_sandbox(base, t)
            return order_findings(sb)

        def syntax():
            t = acts.replace("fi\n", "fi fi\n", 1)
            p = base / "bad.sh"
            p.write_text(t, "utf-8")
            r = subprocess.run(["bash", "-n", str(p)], capture_output=True, text=True)
            return [] if r.returncode == 0 else ["ORDER-SYNTAX: bash -n exits " + str(r.returncode) + " (syntax error)"]

        def m2():
            t = re.sub(r'(F-LAR11 --stamped > /dev/null) \|\| die "[^"]*"', r'\1 || echo "F-LAR11 did not certify"',
                       acts, count=1)
            return guard_static(t) if t != acts else ["(the plant's anchor moved)"]

        def no_lar_gate():
            t = re.sub(r'(?m)^"\$PY" "\$FIXT" F-LAR11 --root=.*\n', "", acts, count=1)
            return prepush_findings(base, t) if t != acts else ["(the plant's anchor moved)"]

        def no_tc10_gates():
            t = re.sub(r'(?m)^git ls-files --error-unmatch -- "\$TC10_DOC".*\n^git diff --quiet HEAD -- "\$LEDGER".*\n',
                       "", acts, count=1)
            return halfrun_findings(base, t) if t != acts else ["(the plant's anchor moved)"]
        return plants([("the TC10 gate deleted from a copy of close_acts.sh (run --check, TC10 absent)", "ORDER-GATE", gate_gone),
                       ("a copy that touches a file before the gate", "ORDER-CHANGED", changes),
                       ("a copy with a syntax error", "ORDER-SYNTAX", syntax),
                       ("step 3's F-LAR11 failure made to print instead of die (mutation M2)", "ORDER-GUARD", m2),
                       ("step 0's pre-stamp F-LAR11 gate deleted, run with a bent cite source (m1)", "ORDER-PREPUSH", no_lar_gate),
                       ("step 0's TC10 tracked / committed gates deleted, run on TC10's half-run close (m2)", "ORDER-TC10", no_tc10_gates)])
    finally:
        shutil.rmtree(base, ignore_errors=True)


def tc10_add_repro(sb: Path) -> tuple[bool, str]:
    """FN-M-TC10-ACTS-IGNORED, reproduced: TC10's own bare 'git add' line, its two tracked paths modified, run in the
    sandbox: it must stage both and exit nonzero."""
    acts = rd(TC10_ACTS).split("\n")
    line = [ln for ln in acts if re.match(r"^git add (?!-f)", ln)]
    asg = {m.group(1): m.group(2) for ln in acts for m in [re.match(r"^([A-Z_]+)=(\S+)$", ln)] if m}
    if len(line) != 1:
        return False, f"{len(line)} bare 'git add' lines in {TC10_ACTS}"
    names = re.findall(r'"\$([A-Z_]+)"', line[0])
    paths = [asg[n] for n in names]
    for p in paths:
        (sb / p).write_bytes((sb / p).read_bytes() + b"\n")
    r = subprocess.run(["git", "-C", str(sb), "add", *paths], capture_output=True, text=True)
    staged = set(git("diff", "--cached", "--name-only", cwd=sb).split())
    git("reset", "-q", "--", *paths, cwd=sb)
    git("checkout", "-q", "--", *paths, cwd=sb)
    ok = r.returncode != 0 and set(paths) <= staged
    ver = subprocess.run(["git", "--version"], capture_output=True, text=True).stdout.strip()
    return ok, (f"TC10's '{line[0].strip()}' ({', '.join(paths)}) under {ver}: exit {r.returncode}, "
                f"staged {sorted(set(paths) & staged)}")


def order_real():
    acts = rd(ACTS)
    r = subprocess.run(["bash", "-n", str(ROOT / ACTS)], capture_output=True, text=True)
    if r.returncode != 0:
        return False, f"ORDER-SYNTAX: {r.stderr.strip()}"
    g = guard_static(acts)
    if g:
        return False, "; ".join(g)
    if (ROOT / TC10_DOC).exists():
        return False, f"precondition of this leg: {TC10_DOC} exists in the repo; the sandbox law needs it absent"
    repo_before = (git("rev-parse", "HEAD").strip(), git("status", "--porcelain", "--untracked-files=all"),
                   git("for-each-ref"))
    base = fresh_base("real")
    notes = ["bash -n clean; every fixture run, every push guarded by a die; step 0 holds the TC10 gates and the "
             "pre-stamp F-LAR11 gate before the first push"]
    try:
        sb = make_sandbox(base)
        f = order_findings(sb)
        if f:
            return False, "; ".join(f)
        notes.append("full run in the sandbox: STOPPED at step 0 with the TC10 message, nothing changed")
        rc, out = run_acts(sb, "--check")
        if rc == 0 or TC10_MSG not in out:
            return False, "--check did not stop on the TC10 gate"
        (sb / TC10_DOC).parent.mkdir(parents=True, exist_ok=True)
        (sb / TC10_DOC).write_text("probe\n", "utf-8")
        rc, out = run_acts(sb, "--check")
        (sb / TC10_DOC).unlink()
        if rc == 0 or TC10_MSG not in out:
            return False, "TC10's report present but its ledger block absent: the gate did not hold"
        notes.append("report present, block absent: STOP (TC10 message)")
        ok, why = tc10_add_repro(sb)
        if not ok:
            return False, f"FN-M-TC10-ACTS-IGNORED not reproduced: {why}"
        notes.append(f"FN-M-TC10-ACTS-IGNORED reproduced: {why}")
        h = halfrun_findings(base, acts)
        if h:
            return False, "; ".join(h)
        notes.append("TC10's half-run close (report untracked, block uncommitted, its files staged): STOP on the named "
                     "TC10 gate (FN-M-TC10-ACTS-IGNORED)")
        sim_tc10(sb, commit=False, doc_tracked=True)
        rc, out = run_acts(sb, "--check")
        if rc == 0 or f"{LEDGER_APOLLO} differs from HEAD" not in out:
            return False, f"TC10's block appended but not committed: step 0 did not stop ({last_line(out)!r})"
        notes.append("TC10's report tracked, its block not committed: STOP (ledger differs from HEAD)")
        git("checkout", "-q", "--", LEDGER_APOLLO, cwd=sb)
        led = sb / LEDGER_APOLLO
        led.write_bytes(led.read_bytes() + (ROOT / TC10_APPEND).read_bytes())
        sb_commit(sb, [LEDGER_APOLLO], "tc10(CLOSE, simulated: the block)")
        git("checkout", "-q", "-b", "tc11-close-probe", cwd=sb)
        rc, out = run_acts(sb, "--check")
        git("checkout", "-q", BRANCH, cwd=sb)
        git("branch", "-q", "-D", "tc11-close-probe", cwd=sb)
        if rc == 0 or f"not on {BRANCH}" not in out:
            return False, "the branch gate did not hold"
        notes.append("another branch: STOP (not on the branch)")
        tmp = sb / "PROBE_STAGED.txt"
        tmp.write_text("probe\n", "utf-8")
        git("add", "--", "PROBE_STAGED.txt", cwd=sb)
        rc, out = run_acts(sb, "--check")
        git("rm", "-q", "--cached", "--", "PROBE_STAGED.txt", cwd=sb)
        tmp.unlink()
        if rc == 0 or "the index is not clean" not in out:
            return False, f"the clean-index gate did not hold ({last_line(out)!r})"
        notes.append("TC10 closed, a staged file: STOP (index not clean)")
        rc, out = run_acts(sb, "--check")
        if rc == 0 or "is not committed (the CLOSE commit adds the CLOSE files first)" not in out:
            return False, f"the CLOSE files uncommitted: step 0 did not stop ({last_line(out)!r})"
        notes.append("TC10 closed, the CLOSE files uncommitted: STOP")
        # the CLOSE commit, a local bare origin, then steps 0-5 for real (cut before publish())
        sb_close_commit(sb)
        o = sb_origin(base, sb)
        tip0 = git("rev-parse", BRANCH, cwd=o).strip()
        rc, out = run_acts(sb, "--check")
        if rc != 0 or "--check: step 0 passed" not in out or git("rev-parse", BRANCH, cwd=o).strip() != tip0:
            return False, f"--check with TC10 closed and the CLOSE committed did not pass cleanly ({last_line(out)!r})"
        notes.append("TC10 closed, the CLOSE committed: --check passes (the pre-stamp F-LAR11 gate GREEN), nothing pushed")
        head_close = git("rev-parse", "HEAD", cwd=sb).strip()
        draft_sha = sha_b((sb / DRAFT).read_bytes())
        app_pre = (sb / APPEND).read_bytes()
        led_pre = (sb / LEDGER_APOLLO).read_bytes()
        rc, out = run_acts(sb, script=truncated(acts))
        if rc != 0 or SANDBOX_STOP not in out:
            return False, f"steps 0-5 did not run to the cut ({last_line(out)!r})"
        bad = []
        law5 = git("rev-parse", "HEAD~1", cwd=sb).strip()
        if git("rev-parse", BRANCH, cwd=o).strip() != law5 or git("rev-parse", "HEAD~2", cwd=sb).strip() != head_close:
            bad.append("the pushes: the bare origin is not at the LAW-5 commit on top of the CLOSE commit")
        if (sb / DRAFT).exists() or not (sb / DOC).is_file() or sha_b((sb / DOC).read_bytes()) != draft_sha:
            bad.append("LAW 5: the document did not move sha-equal")
        app = (sb / APPEND).read_text("utf-8")
        tc = [ln.split("\t", 1)[0] for ln in git("log", "--format=%H%x09%s", law5, cwd=sb).splitlines()
              if ln.split("\t", 1)[1].startswith("tierc11(")]
        off = set(git("rev-list", law5, "--not", "--remotes", cwd=sb).split())
        want = f"{len(tc)} tierc11 commits, {sum(1 for h in tc if h not in off)} on a remote"
        if want not in app or STAMP_RE.search(app) or STAMP_RE.sub(want, app_pre.decode(), count=1) != app:
            bad.append(f"step 3: the stamp is not git's count ({want}) on the pre-stamp bytes")
        if (sb / LEDGER_APOLLO).read_bytes() != led_pre + app.encode():
            bad.append("step 4: the ledger is not its old bytes + the stamped append")
        names = set(git("show", "--name-only", "--format=", "HEAD", cwd=sb).split())
        if names != {APPEND, f"{CLOSE}/{STAMPED}"}:
            bad.append(f"step 5: the residue commit carries {sorted(names)}")
        lar = (sb / CLOSE / STAMPED).read_text("utf-8") if (sb / CLOSE / STAMPED).is_file() else ""
        if "1 GREEN, 0 RED" not in lar:
            bad.append("step 3: the stamped F-LAR11 transcript is not GREEN")
        if bad:
            return False, "; ".join(bad)
        notes.append(f"steps 0-5 run in the sandbox against a local bare origin (cut before publish()): two pushes, the "
                     f"document moved sha-equal, the stamp = git's count ({want}), the ledger = its old bytes + the "
                     "stamped append, the residue commit = the append + its GREEN certificate")
        p = prepush_findings(base, acts)
        if p:
            return False, "; ".join(p)
        notes.append("a cite source bent and committed after the CLOSE commit: STOP at step 0 on F-LAR11, nothing pushed")
    finally:
        shutil.rmtree(base, ignore_errors=True)
    repo_after = (git("rev-parse", "HEAD").strip(), git("status", "--porcelain", "--untracked-files=all"),
                  git("for-each-ref"))
    if repo_before != repo_after:
        return False, "the REAL repository changed during the sandbox runs"
    return True, "; ".join(notes) + "; the real repository unchanged (HEAD, porcelain, refs)"


# ═══════════════════════════════════════════════════════════════ F-DET
def det_run(seed: int, out: Path) -> tuple[int, str]:
    env = dict(os.environ, PYTHONHASHSEED=str(seed))
    r = subprocess.run([sys.executable, str(ROOT / GENERATOR), f"--out-root={out}"], capture_output=True, text=True,
                       env=env, timeout=900)
    return r.returncode, r.stdout[-400:] + r.stderr[-400:]


def det_compare(a: Path, b: Path) -> list[str]:
    f = []
    for rel in OUTPUTS:
        x, y = (a / rel), (b / rel)
        if not x.is_file() or not y.is_file():
            f.append(f"DET-FILES: {rel} missing in one build")
            continue
        bx, by = x.read_bytes(), y.read_bytes()
        if bx != by:
            k = next((i for i in range(min(len(bx), len(by))) if bx[i] != by[i]), min(len(bx), len(by)))
            f.append(f"DET-BYTES: {rel} differs at byte {k}")
    return f


DET_CACHE: dict = {}


def det_builds() -> dict:
    if not DET_CACHE:
        d = RUN_ROOT / "_det_close"
        shutil.rmtree(d, ignore_errors=True)
        for s in SEEDS:
            o = d / f"seed_{s}"
            DET_CACHE[s] = (det_run(s, o), o)
    return DET_CACHE


def det_break():
    b = det_builds()
    (rc, _), o = b[SEEDS[0]]
    if rc != 0:
        return True, "the build under the first seed failed; nothing to bend"
    bent = RUN_ROOT / "_det_close" / "bent"
    shutil.rmtree(bent, ignore_errors=True)
    shutil.copytree(o, bent)
    p = bent / S5M
    data = bytearray(p.read_bytes())
    data[len(data) // 2] ^= 1
    p.write_bytes(bytes(data))
    r = plants([("one byte bent in a copy of the findings md", "DET-BYTES", lambda: det_compare(o, bent))])
    shutil.rmtree(bent, ignore_errors=True)
    return r


def det_real():
    b = det_builds()
    f = []
    for s in SEEDS:
        (rc, tail), o = b[s]
        if rc != 0:
            f.append(f"DET-RUN: seed {s} exited {rc}: {tail.strip()[-160:]}")
    if f:
        return False, "; ".join(f)
    f += det_compare(b[SEEDS[0]][1], b[SEEDS[1]][1])
    f += det_compare(b[SEEDS[0]][1], ROOT)
    if f:
        return False, "; ".join(f[:3])
    shas = " · ".join(f"{Path(rel).name} {sha_b((ROOT / rel).read_bytes())[:12]}…" for rel in OUTPUTS)
    return True, (f"exit 0/0; the {len(OUTPUTS)} outputs byte-identical seed {SEEDS[0]} == seed {SEEDS[1]} == the "
                  f"files of record ({shas})")


# ═══════════════════════════════════════════════════════════════ main
FIXTURES = [
    ("F-S0-NINE", "§0.2 = the scorer's §0 table, byte for byte, nine rows in family order",
     "the draft's §0.2 rows are not S0_VERDICTS.md's §0 table rows byte for byte, or not m rows in FAMILY.json's "
     "order, or a verdict cell disagrees with FAMILY.json's verdict_of_record", s0_break, s0_real),
    ("F-NUM", "every number in §0 and in the append traced to its record file and field",
     "a trace does not re-derive from its record, a verbatim block is not its source lines, a digit of §0 or of the "
     "append prose is untraced or a traced literal is printed other than its declared number of times, or an R4 ★ "
     "cell is not STAGE_R4.md's", num_break, num_real),
    ("F-FEAS-0", "§0.3 = R2_LENS_VERDICTS.json, every lens, every word",
     "a lens word (taker / maker / charter / tuning / ALL) or number in §0.3 differs from R2_LENS_VERDICTS.json, or "
     "the lens set is not the JSON's", feas_break, feas_real),
    ("F-LAR11", "the append passes TC10's check_format law and every «cite» verifies",
     "check_format (TC10's own) fails, a «cite» fails TC10's verify_quote, a commissioned item is missing, a word "
     "claim is false, the pending stamp is not exactly one, or §14 is not the append", lar_break, lar_real),
    ("F-BOXCOST", "the box table re-derived from git and publish_exchange's constants",
     "a row's TRACKED / COMMITTED / PUSHED / BOX COST / FLAGGED differs from git and the ast-read constants, a path "
     "this build touched is not a row, the tick set does not re-derive, or the md is not the json", box_break, box_real),
    ("F-FNF", "the findings: json == md, class / owner / source on every finding, ids unique",
     "the md is not the json, a finding lacks class / owner / owner basis / source / status, an id repeats, a "
     "harvested text does not re-extract, operator-owned findings do not rank first, or a count is off",
     fnf_break, fnf_real),
    ("F-CLAIMS", "the hand-worded claims held against their records; the generator's R2 GUARD HALTs",
     "§0.6's P-AGE-1 bullet does not print the scorer's label and pre_seen cohort (B4 OLD named refused), an R2 "
     "sentence closes more than the non-provisional FAILs or drops the law's caveat, a TC10 state is stated in a "
     "tense the landing falsifies, a W2 / head-to-head table stands without the collar, a line of either nesting-grid "
     "file is missing from §2.3, §0 does not open with R5's chop test, a calibrated read lacks its SCALE-IN-SAMPLE "
     "count, the document does not end with the seven-column table, or a 1w-PASS sandbox does not HALT the generator "
     "on its R2 GUARD", claims_break, claims_real),
    ("F-CLOSE-ORDER", "close_acts.sh: step 0 STOPS until TC10's CLOSE has run AND is committed and F-LAR11 holds; "
     "steps 0-5 run true in a sandbox against a local bare origin",
     "bash -n fails, a fixture run or a push is not guarded by a die, in a sandbox clone a step-0 gate (TC10 absent, "
     "TC10 half-run, branch, index, CLOSE files, a bent cite source) does not STOP before any push, the run changes "
     "the sandbox before its gate, steps 0-5 do not push twice, move the document sha-equal, stamp git's count, append "
     "the stamped bytes and commit the residue, TC10's step-6 'git add' does not reproduce its exit, or the real "
     "repository changes", order_break, order_real),
    ("F-DET", "two generator runs under two hash seeds, one set of bytes",
     "the PYTHONHASHSEED 1 and 20260924 runs (--out-root under RUN_ROOT/_det_close) differ from each other or "
     "from the files of record in any byte, or either exits nonzero", det_break, det_real),
]


def file_transcript(out: Path, body: bytes, refile: bool) -> list[str]:
    """NEVER CLOBBER the transcript of record."""
    if not out.exists() and not refile:
        return [f"{out.name} ABSENT — nothing written; re-file with --refile-transcript"]
    if out.exists() and out.read_bytes() == body:
        return []
    if out.exists() and not refile:
        rr = out.with_name(out.stem + "_rerun.txt")
        rr.write_bytes(body)
        return [f"{out.name} NOT byte-identical; this run -> {rr.name}; record untouched"]
    out.write_bytes(body)
    return []


def main() -> int:
    global RUN_ROOT
    args = sys.argv[1:]
    RUN_ROOT = Path(next((a.split("=", 1)[1] for a in args if a.startswith("--root=")), str(ROOT / CLOSE))).resolve()
    RUN_ROOT.mkdir(parents=True, exist_ok=True)
    stamped = "--stamped" in args
    pick = [a.lower() for a in args if not a.startswith("--")]
    t0 = time.time()
    fam = rj(FAMILY)
    say(f"as_of_last_closed_4h: {fam['as_of_last_closed_4h']}")
    say("=" * 78)
    say("TIER-C11 CLOSE FIXTURES — scripts/tierc11_close.py (the build draft, the findings, BOX-COST, the "
        "ledger append, close_acts.sh) — break leg first, RED or void")
    say("=" * 78)
    say(f"contract {CONTRACT} sha256 {sha_b((ROOT / CONTRACT).read_bytes())[:16]}… · family m {fam['family_m']} · "
        f"outputs {len(OUTPUTS)} · mode {'STAMPED (close_acts.sh step 3)' if stamped else 'pre-close'}")
    if stamped:
        prove("F-LAR11", "the STAMPED append: TC10's format law, every «cite», the stamp equal to git",
              "check_format fails, a «cite» fails verify_quote, the stamp is pending or not git's count, or the "
              "stamped bytes are not the committed pre-stamp append with its one stamp filled",
              lar_break_stamped, lambda: lar_real(stamped=True))
    else:
        for fid, title, fails_if, b, r in FIXTURES:
            if not pick or any(q == fid.lower() for q in pick):
                prove(fid, title, fails_if, b, r)
    say(f"\n  {len(PASSED)} GREEN, {len(FAILED)} RED")
    for x in FAILED:
        say(f"    RED: {x}")
    body = ("\n".join(LINES) + "\n").encode("utf-8")
    if stamped:
        (ROOT / CLOSE / STAMPED).write_bytes(body)
        bad = []
    else:
        name = TRANSCRIPT if not pick else TRANSCRIPT.replace(".txt", "_partial.txt")
        bad = file_transcript(RUN_ROOT / name, body, "--refile-transcript" in args or bool(pick))
    for x in bad:
        clock(x)
    clock(f"wall {time.time() - t0:.1f}s · transcript sha {sha_b(body)}")
    if FAILED:
        print("*** HALT: fixture mismatch. Nothing downstream is trustworthy. ***")
    return 1 if (FAILED or bad) else 0


if __name__ == "__main__":
    raise SystemExit(main())
