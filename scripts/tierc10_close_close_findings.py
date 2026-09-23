#!/usr/bin/env python
"""TIER-C10 · CLOSE · §5 FINDINGS — REPORTED, NOT FIXED.

The RESUME contract (exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md) lists, under
CLOSE, "· findings-not-fixed · BOX-COST", and its PANEL PIN adds "the gap is filed
as a finding".  This module is that item, and only that item.  It HARVESTS what the
build already wrote down as open, verbatim and with its source, it MEASURES six
things at build time that nobody may type, and it FIXES NOTHING.

WHAT IT WRITES (and nothing else)
  research_outputs/tierc10/close/S5_FINDINGS_NOT_FIXED.md
  research_outputs/tierc10/close/S5_FINDINGS_NOT_FIXED.json
  research_outputs/tierc10/close/FIXTURES_CLOSE_findings.txt   (whole-suite runs only)

HARVESTED VERBATIM, each with source path + field
  · every PROGRESS.json stages[].blockers and stages[].notes string
  · both "## Still blocked" lists in OPERATOR_RULINGS.md
  · STAGE_D_MANIFEST.json operator_rulings_needed and as_of_hazards
  · FAMILY.json scored_slots_halted
  · every brk_sealed_row.toll_accounting_status under scores/
  · the REGISTRATION_PLAN.md "drafting error" paragraph
  · the BUILD_DRAFT.md §R0.3 smoke-roots paragraph (DISCLOSED ONLY — nothing is
    moved or deleted, LAW 2)
  · the rows of census/, panel/ and stamps/ leans.parquet, LABELLED AS LEANS

MEASURED at build time, recomputed on every run, never typed
  (i)   REGISTRATION_TEXTS.json texts found verbatim in REGISTRATION_TEXTS.md
  (ii)  arms whose beside.haircut_twin.twin_expectancy_r > tc_expectancy_r
  (iii) os.path.exists of analytics/rangefinder.py and analytics/rangefinder_census.py
  (iv)  PROGRESS.json head vs `git rev-parse HEAD`
  (v)   `git worktree list` HEADs vs the tierc10 commits reachable from HEAD
  (vi)  PROGRESS.json stages with no stage line in BUILD_DRAFT.md §1

Every finding carries id, text, source, owner (operator | executor) with a
verbatim owner basis, and status 'REPORTED, NOT FIXED'.  That status records what
THIS build did — it reports and never fixes — and does not claim the item is
still open: several harvested strings record their own repair, and the document
says which.

THE LEGS (every leg states its failure condition; every leg carries a sabotage
that must go RED, judged one plant at a time, on COPIES only)
  F-FN-HARVEST   FAILS IF any string under PROGRESS.json stages[].blockers or
                 stages[].notes (re-read independently) is absent from the
                 findings as a verbatim text sourced to PROGRESS.json, if the
                 PROGRESS-sourced findings are not exactly that multiset, or if any
                 declared harvest source contributed zero findings.
                 SABOTAGE: a blocker added to a COPY of PROGRESS.json; a PROGRESS
                 finding dropped; every stamps lean dropped.
  F-FN-SOURCE    FAILS IF a finding's source path does not exist, its field does
                 not re-resolve (an independent resolver: JSON path walker / line
                 slice / pyarrow) to its text verbatim, its owner is not operator |
                 executor, its owner-basis quote is not verbatim at the basis path,
                 its status is not 'REPORTED, NOT FIXED', or an id repeats.
                 SABOTAGE: a missing source path; a one-character text bend; a bent
                 basis quote; status 'FIXED'; owner 'nobody'; a duplicated id.
  F-FN-MEASURED  FAILS IF any of (i)-(vi) in the filed JSON differs from a second,
                 independent recomputation in the leg (bytes search, Decimal
                 parse, os.listdir, raw .git refs + rev-list sets, cat-file
                 subjects + merge-base, a line scanner).
                 SABOTAGE: a stale value planted in each of (i)-(vi).
  F-FN-NOSCORE   FAILS IF this module's AST imports a scoring, registration or
                 bar-loading module, calls score / finish_family / register /
                 load_klines / load_asof, or reads a 'verdict' key.
                 SABOTAGE: each of the three planted into a copy of the source.
  F-DET          FAILS IF two cross-process builds, and the canonical on-disk
                 build, are not byte-identical once the NAMED git-volatile fields
                 are masked — or if the mask is wider than named.
                 SABOTAGE: a non-volatile JSON byte bent; a non-volatile MD byte
                 bent.  CONTROL (must stay GREEN): a volatile-only bend.
  F-FN-READONLY  FAILS IF any input's bytes change between the start and the end
                 of the run; and the build, run against a COPY of the inputs,
                 must leave the copy byte-identical.
                 SABOTAGE: one byte appended to one input COPY.

HOUSE LAWS OBSERVED HERE
  · REPORT-ONLY / Tier-E.  Nothing is scored; no registration's verdict is read
    (the only values read out of scores/ are arm, beside.haircut_twin.{tc,twin}
    _expectancy_r, brk_sealed_row.toll_accounting_status and FAMILY.json
    scored_slots_halted); no bar is read at all, so tierc10_data.load_asof is
    not needed and tierc2_baseline.load_klines is never reached.
  · READ-ONLY on every input.  No registration, REGISTRY*, *.scored.json,
    scores/*, PROGRESS.json or FIXTURES_RESUME.txt is written.  No git write.
  · DETERMINISM.  No clock, no temp path, no set iteration order in any output.
    The git-volatile fields are NAMED in GIT_VOLATILE and excluded from F-DET.

Run:
  export NAIAD_CACHE_DIR=/Users/luis/.cache/naiad/snapshots/tc10_20260921 \\
         PYTHONDONTWRITEBYTECODE=1
  ~/venvs/naiad/bin/python -B scripts/tierc10_close_close_findings.py [leg-substring ...]

Exit: 0 every leg GREEN (every sabotage RED, every control GREEN) · 1 a leg RED
or a HALT (a HALT writes nothing) — the family's RUN/HALT convention.
"""
from __future__ import annotations

import ast
import copy
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = Path.home() / ".cache" / "naiad" / "snapshots" / "tc10_20260921"
LIVE_CACHE = Path.home() / ".cache" / "naiad" / "data_cache"

TC = "research_outputs/tierc10"
CONTRACT = "exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md"
PROGRESS = f"{TC}/PROGRESS.json"
RULINGS = f"{TC}/OPERATOR_RULINGS.md"
SDM = f"{TC}/data/STAGE_D_MANIFEST.json"
FAMILY = f"{TC}/scores/FAMILY.json"
SCORES_DIR = f"{TC}/scores"
PLAN = f"{TC}/REGISTRATION_PLAN.md"
DRAFT = f"{TC}/BUILD_DRAFT.md"
REGTEXTS_JSON = f"{TC}/REGISTRATION_TEXTS.json"
REGTEXTS_MD = f"{TC}/REGISTRATION_TEXTS.md"
LEANS = (   # (key, path, id column, text column) — the three schemas differ, so they are DECLARED
    ("CENSUS", f"{TC}/census/leans.parquet", "lean", "text"),
    ("PANEL", f"{TC}/panel/leans.parquet", "lean", "text"),
    ("STAMPS", f"{TC}/stamps/leans.parquet", "n", "lean"),
)
RF_PATHS = ("analytics/rangefinder.py", "analytics/rangefinder_census.py")

OUT_DIR_REL = f"{TC}/close"
OUT_JSON = "S5_FINDINGS_NOT_FIXED.json"
OUT_MD = "S5_FINDINGS_NOT_FIXED.md"
TRANSCRIPT = "FIXTURES_CLOSE_findings.txt"
SELF_REL = "scripts/tierc10_close_close_findings.py"

STATUS = "REPORTED, NOT FIXED"
OWNERS = ("operator", "executor")
TIERC10_SUBJECT_PREFIX = "tierc10"   # the build's own commit-subject convention

# ── THE GIT-VOLATILE FIELDS, NAMED.  They move with every commit or worktree the
#    orchestration makes, so F-DET masks EXACTLY these and nothing wider.
GIT_VOLATILE = (
    "git",
    "measured.iv",
    "measured.v",
    "findings[id=FN-M-iv].text",
    "findings[id=FN-M-v].text",
)
VOL_BEGIN = "<!-- git-volatile:begin -->"
VOL_END = "<!-- git-volatile:end -->"

HARVEST_KEYS = (   # every one must contribute >= 1 finding (F-FN-HARVEST)
    "PROGRESS", "RULINGS-L1", "RULINGS-L2", "SDM-ORN", "SDM-HAZ", "FAMILY",
    "TOLL", "PLAN", "DRAFT", "LEAN-CENSUS", "LEAN-PANEL", "LEAN-STAMPS", "MEASURED",
)

LABEL_DOC = ("REPORT-ONLY · Tier-E — findings harvested verbatim and measured at build "
             "time; nothing here is scored, no registration verdict is read, no bar is "
             "read, and nothing is fixed.")
LABEL_LEAN = ("LEAN — an executor operationalisation, labelled as such; not a ruling, "
              "not a defect, not a result.")

# ── OWNER RULES FOR PROGRESS.json STRINGS.  First rule whose QUOTE is verbatim in
#    the text wins; the quote IS the owner basis, and F-FN-SOURCE re-checks it.
#    The READING is the executor's typed rationale — words, never numbers.
PROGRESS_OWNER_RULES = (
    ("RESUME CLAUSE F-D-4 (TWO-TOKEN TRAP)", "executor",
     "a Stage D report clause the executor builds"),
    ("RESUME CLAUSE F-D-5 (DATA-SPEND AUDIT)", "executor",
     "a Stage D report clause the executor builds"),
    ("RESUME CLAUSE COSTS HAIRCUT TWIN", "executor",
     "a Stage D report clause the executor builds"),
    ("RESUME CLAUSE CONTRACT MULTIPLIERS", "executor",
     "a Stage D report clause the executor builds"),
    ("pending an operator ruling that does not yet exist", "operator",
     "the text names an operator ruling as the dependency"),
    ("CARRIED AS-OF HAZARD", "executor",
     "a load-path trap for executor code, not a question for the operator"),
    ("TRANSCRIPT BYTE-REPRODUCIBILITY IS DISPROVEN", "executor",
     "a property of the executor's fixture transcripts against a backfilling venue"),
    ("What remains is F-D-1's operator ruling: REST or ARCHIVE.", "operator",
     "the text names the operator's REST-or-ARCHIVE word as what remains"),
    ("Not a defect and not an operator question", "executor",
     "the text itself rules the operator out; disclosure of prescribed mechanics"),
    ("OPEN, for the operator", "operator",
     "the text names the operator as the one who settles it"),
    ("pending the operator's REST-or-ARCHIVE word", "operator",
     "the text names the operator's word as the dependency"),
    ("that filing is the OPERATOR's to order", "operator",
     "the text names the operator as the one who orders the new filing"),
    ("finish_family runs after B-5M", "executor",
     "an executor sequencing note (B-5M has since run: see PROGRESS stage B-5M)"),
    ("finish_family ran with P-BE-1's slot HALTed", "executor",
     "disclosure of the executor's finish_family invocation, prescribed by the texts"),
    ("names the print-vs-deduction question OPEN for the operator", "operator",
     "the text names the operator as the one who settles it"),
)


# ═══════════════════════════════════════════════════════════════ utilities ══
def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha256_file(p: Path) -> str:
    return sha256_bytes(p.read_bytes())


def read_text(p: Path) -> str:
    return p.read_bytes().decode("utf-8")


def canon(v) -> str:
    return json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(", ", ": "))


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    env = dict(os.environ, GIT_OPTIONAL_LOCKS="0")
    return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True,
                          text=True, check=check, env=env)


def input_paths(root: Path) -> list[str]:
    """Every file this module reads, repo-relative, sorted — the READ-ONLY set."""
    rows = sorted(f"{SCORES_DIR}/{q.name}" for q in (root / SCORES_DIR).glob("*.json"))
    fixed = [CONTRACT, PROGRESS, RULINGS, SDM, PLAN, DRAFT, REGTEXTS_JSON, REGTEXTS_MD]
    fixed += [p for _, p, _, _ in LEANS]
    return sorted(set(fixed) | set(rows))


def input_manifest(root: Path) -> dict[str, dict]:
    out = {}
    for rel in input_paths(root):
        p = root / rel
        if p.is_file():
            b = p.read_bytes()
            out[rel] = {"bytes": len(b), "sha256": sha256_bytes(b)}
        else:
            out[rel] = {"bytes": None, "sha256": None}
    return out


# ═══════════════════════════════════════════════════════════════ preamble ══
def preamble() -> list[str]:
    """RUN or HALT, before anything is read for the build or any file is written.
    HALTS IF: NAIAD_CACHE_DIR is unset, is the live cache, is not the TC10 snapshot
    or the snapshot has no klines/; PYTHONDONTWRITEBYTECODE is not 1; an input is
    missing; the branch is not the ledger's branch; the contract's bytes are not the
    ledger's contract_of_record.  A HALT writes NOTHING and exits 1 (the family's
    RUN/HALT convention: 0 every leg GREEN · 1 a leg RED or a HALT)."""
    env = os.environ.get("NAIAD_CACHE_DIR", "")
    if not env:
        raise SystemExit("HALT: NAIAD_CACHE_DIR is unset — TC10 runs ONLY against "
                         f"the frozen snapshot {SNAPSHOT}")
    got = Path(env).expanduser().resolve()
    if got == LIVE_CACHE.resolve():
        raise SystemExit("HALT: NAIAD_CACHE_DIR is the LIVE cache — READ-NEVER, "
                         "WRITE-NEVER for TC10")
    if got != SNAPSHOT.resolve():
        raise SystemExit(f"HALT: NAIAD_CACHE_DIR={got} is not the TC10 snapshot "
                         f"{SNAPSHOT}")
    if not (got / "klines").is_dir():
        raise SystemExit(f"HALT: snapshot has no klines/ directory: {got}")
    if os.environ.get("PYTHONDONTWRITEBYTECODE") != "1" or not sys.dont_write_bytecode:
        raise SystemExit("HALT: PYTHONDONTWRITEBYTECODE=1 is not in force")
    missing = [rel for rel in input_paths(ROOT) if not (ROOT / rel).is_file()]
    if missing:
        raise SystemExit(f"HALT: inputs missing: {missing}")
    prog = json.loads(read_text(ROOT / PROGRESS))
    branch = git("rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    if branch != prog.get("branch"):
        raise SystemExit(f"HALT: branch {branch!r} is not the ledger's branch "
                         f"{prog.get('branch')!r} (PROGRESS.json branch)")
    csha = sha256_file(ROOT / CONTRACT)
    rec = (prog.get("contract_of_record") or {}).get("sha256")
    if csha != rec:
        raise SystemExit(f"HALT: {CONTRACT} sha256 {csha} is not PROGRESS.json "
                         f"contract_of_record.sha256 {rec}")
    return [
        f"RUN · TIER-C10 CLOSE §5 findings-not-fixed · branch {branch} (== PROGRESS.json branch)",
        f"RUN · substrate NAIAD_CACHE_DIR={got} (the frozen snapshot; no bar is read by this module)",
        f"RUN · PYTHONDONTWRITEBYTECODE=1 · inputs present {len(input_paths(ROOT))}/{len(input_paths(ROOT))}",
        f"RUN · contract {CONTRACT} sha256 {csha} (== PROGRESS.json contract_of_record.sha256)",
        f"RUN · as_of_of_record {prog.get('as_of_of_record')} (PROGRESS.json as_of_of_record) · "
        f"seed {prog.get('seed')} (PROGRESS.json seed)",
    ]


# ══════════════════════════════════════════════════════════════ harvesting ══
def _finding(fid, hkey, cls, text, path, field, owner, basis_path, quote, reading,
             context=None, text_form="verbatim string") -> dict:
    return {
        "id": fid,
        "class": cls,
        "harvest_key": hkey,
        "label": LABEL_LEAN if cls == "LEAN" else "REPORT-ONLY · Tier-E",
        "text": text,
        "text_form": text_form,
        "source": {"path": path, "field": field, **({"context": context} if context else {})},
        "owner": owner,
        "owner_basis": {"path": basis_path, "quote": quote, "reading": reading},
        "status": STATUS,
    }


def harvest_progress(root: Path) -> list[dict]:
    prog = json.loads(read_text(root / PROGRESS))
    out = []
    for si, st in enumerate(prog.get("stages", [])):
        for kind, tag in (("blockers", "B"), ("notes", "N")):
            v = st.get(kind)
            if v is None:
                continue
            items = v if isinstance(v, list) else [v]
            for k, s in enumerate(items):
                field = f"stages[{si}].{kind}[{k}]" if isinstance(v, list) else f"stages[{si}].{kind}"
                text, form = (s, "verbatim string") if isinstance(s, str) else (canon(s), "canonical JSON of a non-string value")
                owner, quote, reading = None, None, None
                for q, o, r in PROGRESS_OWNER_RULES:
                    if q in text:
                        owner, quote, reading = o, q, r
                        break
                if owner is None:   # DEFAULT RULE — printed, never silent
                    owner = "operator" if re.search(r"\boperator", text, re.I) else "executor"
                    quote = text[:60]
                    reading = ("DEFAULT RULE: no declared owner rule matched; owner is "
                               "'operator' iff the word 'operator' occurs in the text")
                repair = [f"FN-PROG-{si:02d}-{tag}{j + 1}" for j, x in enumerate(items)
                          if j != k and isinstance(x, str) and x.startswith("REPAIRED")]
                ctx = {"stage": st.get("stage"), "stage_status": st.get("status")}
                if repair:
                    ctx["repair_line_in_same_list"] = repair
                out.append(_finding(
                    f"FN-PROG-{si:02d}-{tag}{k + 1}", "PROGRESS", "HARVESTED", text,
                    PROGRESS, field, owner, PROGRESS, quote, reading,
                    context=ctx, text_form=form))
    return out


def _md_sections(lines: list[str], starts_with: str) -> list[tuple[int, int]]:
    """(heading index, end index exclusive) of every section whose heading line
    starts with `starts_with`; a section ends at the next heading or '---'."""
    out = []
    for i, ln in enumerate(lines):
        if ln.startswith(starts_with):
            j = i + 1
            while j < len(lines) and not (lines[j].startswith("#") or lines[j].strip() == "---"):
                j += 1
            out.append((i, j))
    return out


def harvest_rulings(root: Path) -> list[dict]:
    lines = read_text(root / RULINGS).split("\n")
    out = []
    for li, (h, end) in enumerate(_md_sections(lines, "## Still blocked"), start=1):
        heading = lines[h]
        bullets: list[tuple[int, int]] = []
        cur = None
        for i in range(h + 1, end):
            ln = lines[i]
            if ln.startswith("- "):
                if cur is not None:
                    bullets.append(cur)
                cur = (i, i)
            elif cur is not None and ln.strip() and ln.startswith(" "):
                cur = (cur[0], i)
            elif cur is not None and not ln.strip():
                bullets.append(cur)
                cur = None
        if cur is not None:
            bullets.append(cur)
        for k, (a, b) in enumerate(bullets, start=1):
            text = "\n".join(lines[a:b + 1])
            out.append(_finding(
                f"FN-RUL-L{li}-{k}", f"RULINGS-L{li}", "HARVESTED", text, RULINGS,
                f"lines {a + 1}-{b + 1}", "operator", RULINGS, "Still blocked on the operator",
                "the list's own heading assigns every bullet to the operator",
                context={"list": li, "heading": heading, "heading_line": h + 1}))
    return out


def harvest_stage_d(root: Path) -> list[dict]:
    m = json.loads(read_text(root / SDM))
    out = []
    for k, s in enumerate(m.get("operator_rulings_needed") or []):
        text = s if isinstance(s, str) else canon(s)
        quote = next((q for q in ("RULING NEEDED", "Needs the operator's") if q in text), text[:60])
        out.append(_finding(
            f"FN-SDM-ORN-{k + 1}", "SDM-ORN", "HARVESTED", text, SDM,
            f"operator_rulings_needed[{k}]", "operator", SDM, quote,
            "the manifest files it under operator_rulings_needed"))
    haz = m.get("as_of_hazards") or {}
    laws = {"kline": haz.get("kline_law", ""), "funding": haz.get("funding_law", "")}
    law_quotes = {
        "kline": "a TC10 lane that loads one of these files through it without an as-of cut reads past the pin",
        "funding": "an interval-sum funding law must sum on funding_hour_ms, never on the raw stamp",
    }
    for key in sorted(haz):
        v = haz[key]
        text, form = (v, "verbatim string") if isinstance(v, str) else (canon(v), "canonical JSON of a non-string value")
        fam = "kline" if key.startswith("kline") else "funding"
        quote = law_quotes[fam] if law_quotes[fam] in laws[fam] else text[:60]
        out.append(_finding(
            f"FN-SDM-HAZ-{key}", "SDM-HAZ", "HARVESTED", text, SDM, f"as_of_hazards.{key}",
            "executor", SDM, quote,
            "an as-of hazard binds the executor's load path; the manifest's own law says how",
            text_form=form))
    return out


def harvest_family(root: Path) -> list[dict]:
    f = json.loads(read_text(root / FAMILY))
    out = []
    for slot in sorted(f.get("scored_slots_halted") or {}):
        v = f["scored_slots_halted"][slot]
        text = v if isinstance(v, str) else canon(v)
        out.append(_finding(
            f"FN-FAM-HALT-{slot}", "FAMILY", "HARVESTED", text, FAMILY,
            f"scored_slots_halted.{slot}", "operator", PROGRESS,
            "that filing is the OPERATOR's to order",
            "the ledger's B-CORE note assigns the new set_change filing to the operator"))
    return out


def _walk_for(o, path: str, suffix: tuple[str, str], hits: list):
    if isinstance(o, dict):
        for k, v in o.items():
            p = f"{path}.{k}" if path else k
            if k == suffix[1] and path.endswith(suffix[0]):
                hits.append((p, v))
            else:
                _walk_for(v, p, suffix, hits)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            _walk_for(v, f"{path}[{i}]", suffix, hits)


def harvest_toll(root: Path) -> list[dict]:
    out = []
    for q in sorted((root / SCORES_DIR).glob("*.json")):
        b = q.read_bytes()
        if b"brk_sealed_row" not in b:
            continue
        hits: list = []
        _walk_for(json.loads(b.decode("utf-8")), "", ("brk_sealed_row", "toll_accounting_status"), hits)
        for n, (p, v) in enumerate(hits, start=1):
            text = v if isinstance(v, str) else canon(v)
            stem = q.name.replace(".rows.json", "").replace(".json", "")
            out.append(_finding(
                f"FN-TOLL-{stem}-{n}", "TOLL", "HARVESTED", text, f"{SCORES_DIR}/{q.name}", p,
                "operator", PROGRESS, "OPEN, for the operator",
                "the ledger's BRK note leaves print-vs-deduction OPEN for the operator"))
    return out


def harvest_plan(root: Path) -> list[dict]:
    lines = read_text(root / PLAN).split("\n")
    a = next((i for i, ln in enumerate(lines) if "drafting error" in ln), None)
    if a is None:
        return []
    b = a
    while b + 1 < len(lines) and lines[b + 1].strip() and not lines[b + 1].startswith("**"):
        b += 1
    text = "\n".join(lines[a:b + 1])
    return [_finding(
        "FN-PLAN-DRAFTERR", "PLAN", "HARVESTED", text, PLAN, f"lines {a + 1}-{b + 1}",
        "operator", CONTRACT, "no registration re-worded or added",
        "the error sits in the contract paste, which the executor may not re-word; "
        "amending it is the operator's",
        context={"paragraph_rule": "from the line containing 'drafting error' through the "
                                   "last following non-blank line that does not open a new "
                                   "'**' lead"})]


def harvest_draft(root: Path) -> list[dict]:
    lines = read_text(root / DRAFT).split("\n")
    r03 = next((i for i, ln in enumerate(lines) if ln.startswith("### R0.3")), None)
    a = next((i for i, ln in enumerate(lines)
              if ln.startswith("**Disclosed, not moved:**") and (r03 is None or i > r03)), None)
    if a is None:
        return []
    b = a
    while b + 1 < len(lines) and lines[b + 1].strip():
        b += 1
    text = "\n".join(lines[a:b + 1])
    return [_finding(
        "FN-DRAFT-SMOKE", "DRAFT", "HARVESTED", text, DRAFT, f"lines {a + 1}-{b + 1}",
        "operator", DRAFT, "operator chooses; nothing is deleted (§5.12).",
        "rebuild or quarantine under _partial_<ts>/ is the operator's choice; THIS build "
        "discloses only and moves or deletes nothing (LAW 2)",
        context={"section": lines[r03] if r03 is not None else None,
                 "section_line": (r03 + 1) if r03 is not None else None})]


def harvest_leans(root: Path) -> list[dict]:
    import pandas as pd
    out = []
    for key, rel, id_col, text_col in LEANS:
        df = pd.read_parquet(root / rel)
        if id_col not in df.columns or text_col not in df.columns:
            raise SystemExit(f"HALT: {rel} lacks the declared columns "
                             f"{id_col!r}/{text_col!r}: {list(df.columns)} (nothing written)")
        for i in range(len(df)):
            lid = str(df[id_col].iloc[i])
            text = str(df[text_col].iloc[i])
            out.append(_finding(
                f"LEAN-{key}-{lid}" if len(lid) <= 16 else f"LEAN-{key}-{i:02d}",
                f"LEAN-{key}", "LEAN", text, rel, f"row {i} · column {text_col}",
                "executor", RULINGS, "the lean is marked as such and is NOT the ruling",
                "a lean is the executor's operationalisation; the operator may overrule it",
                context={"lean_id_column": id_col, "lean_id": lid}))
    return out


# ═══════════════════════════════════════════════════════════════ measuring ══
def _longest_prefix_in(t: str, hay: str) -> int:
    lo, hi = 0, len(t)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if t[:mid] in hay:
            lo = mid
        else:
            hi = mid - 1
    return lo


def m_i(root: Path) -> dict:
    j = json.loads(read_text(root / REGTEXTS_JSON))
    md = read_text(root / REGTEXTS_MD)
    per = []
    for rid, v in j.items():
        t = v["text"]
        ok = t in md
        per.append({"reg_id": rid, "chars": len(t), "verbatim": ok,
                    "longest_verbatim_prefix_chars": len(t) if ok else _longest_prefix_in(t, md)})
    return {"measure": "REGISTRATION_TEXTS.json texts found verbatim in REGISTRATION_TEXTS.md",
            "method": "Python `text in md` over every <reg>.text of the JSON",
            "value": {"verbatim": sum(p["verbatim"] for p in per), "total": len(per)},
            "per_registration": per}


def m_ii(root: Path) -> dict:
    arms, no_twin = [], []
    for q in sorted((root / SCORES_DIR).glob("P-*.rows.json")):
        o = json.loads(read_text(q))
        for i, r in enumerate(o.get("rows") or []):
            arm = r.get("arm")
            ht = (r.get("beside") or {}).get("haircut_twin")
            rel = f"{SCORES_DIR}/{q.name}"
            if ht is None:
                no_twin.append({"file": rel, "row": i, "arm": arm})
                continue
            tc, tw = ht["tc_expectancy_r"], ht["twin_expectancy_r"]
            arms.append({"file": rel, "row": i, "arm": arm, "tc_expectancy_r": tc,
                         "twin_expectancy_r": tw, "twin_minus_tc_r": tw - tc,
                         "twin_above_tc": tw > tc})
    return {"measure": "arms where beside.haircut_twin.twin_expectancy_r > tc_expectancy_r",
            "method": "rows[].beside.haircut_twin of every scores/P-*.rows.json; float compare",
            "value": {"twin_above_tc": sum(a["twin_above_tc"] for a in arms),
                      "arms_with_twin": len(arms), "arms_total": len(arms) + len(no_twin)},
            "arms": arms, "arms_without_twin": no_twin}


def m_iii(root: Path) -> dict:
    ex = [{"path": rel, "exists": os.path.exists(root / rel)} for rel in RF_PATHS]
    return {"measure": "os.path.exists for analytics/rangefinder.py and analytics/rangefinder_census.py",
            "method": "os.path.exists", "value": ex}


def m_iv(root: Path) -> dict:
    prog = json.loads(read_text(root / PROGRESS))
    ph = prog.get("head")
    gh = git("rev-parse", "HEAD").stdout.strip()
    anc = git("merge-base", "--is-ancestor", ph, gh, check=False).returncode == 0 if ph else False
    between = []
    if anc:
        between = [ln.split("\x1f", 1) for ln in
                   git("log", "--format=%h\x1f%s", f"{ph}..{gh}").stdout.splitlines() if ln]
    return {"measure": "PROGRESS.json head vs `git rev-parse HEAD`",
            "method": "git rev-parse HEAD; git merge-base --is-ancestor; git log ph..HEAD",
            "value": {"progress_head": ph, "git_head": gh, "equal": ph == gh,
                      "progress_head_is_ancestor": anc,
                      "commits_after_progress_head": len(between) if anc else None},
            "commits_after_progress_head": [{"sha7": s, "subject": t} for s, t in between]}


def _tierc10_set_primary() -> list[str]:
    out = []
    for ln in git("log", "--format=%H\x1f%s", "HEAD").stdout.splitlines():
        sha, subj = ln.split("\x1f", 1)
        if subj.startswith(TIERC10_SUBJECT_PREFIX):
            out.append(sha)
    return out


def _rel_to_root(p: str) -> str:
    rp = os.path.realpath(p)
    rr = os.path.realpath(ROOT)
    return "." if rp == rr else os.path.relpath(rp, rr)


def m_v(root: Path) -> dict:
    tc = _tierc10_set_primary()
    tcs = set(tc)
    wts, cur = [], {}
    for ln in git("worktree", "list", "--porcelain").stdout.split("\n"):
        if not ln.strip():
            if cur:
                wts.append(cur)
            cur = {}
            continue
        k, _, v = ln.partition(" ")
        cur[k] = v
    if cur:
        wts.append(cur)
    reach: dict[str, int] = {}
    rows = []
    for w in wts:
        head = w.get("HEAD", "")
        if head not in reach:
            reach[head] = len(tcs & set(git("rev-list", head).stdout.split())) if head else 0
        rows.append({"path": _rel_to_root(w.get("worktree", "")), "head": head,
                     "branch": w.get("branch", "(detached)").replace("refs/heads/", ""),
                     "tierc10_commits_reachable": reach[head]})
    rows.sort(key=lambda r: (r["path"] != ".", r["path"]))
    others = [r for r in rows if r["path"] != "."]
    heads: dict[str, int] = {}
    for r in others:
        heads[r["head"]] = heads.get(r["head"], 0) + 1
    return {"measure": "`git worktree list` HEADs vs the tierc10 commits reachable from HEAD",
            "method": (f"git worktree list --porcelain; tierc10 commits = commits reachable from "
                       f"HEAD whose subject starts with {TIERC10_SUBJECT_PREFIX!r}; per worktree "
                       f"HEAD, |that set ∩ git rev-list <head>|"),
            "value": {"tierc10_commits_on_HEAD": len(tc), "worktrees_total": len(rows),
                      "worktrees_besides_main": len(others),
                      "worktrees_besides_main_with_zero_tierc10": sum(
                          1 for r in others if r["tierc10_commits_reachable"] == 0),
                      "worktrees_besides_main_with_all_tierc10": sum(
                          1 for r in others if r["tierc10_commits_reachable"] == len(tc))},
            "heads_besides_main": [{"head": h, "worktrees": n} for h, n in sorted(heads.items())],
            "worktrees": rows}


def _draft_section1(draft: str) -> str:
    m = re.search(r"^## 1 · STAGE LOG[^\n]*\n(.*?)(?=^## |\Z)", draft, re.S | re.M)
    return m.group(1) if m else ""


def m_vi(root: Path) -> dict:
    prog = json.loads(read_text(root / PROGRESS))
    stages = [s.get("stage") for s in prog.get("stages", [])]
    sec = _draft_section1(read_text(root / DRAFT))
    labels = re.findall(r"^- \*\*(.+?)\*\*", sec, re.M)
    absent = [s for s in stages if not any(s in lab for lab in labels)]
    body_only = [s for s in absent if s in sec]
    return {"measure": "PROGRESS.json stages absent from BUILD_DRAFT.md §1",
            "method": ("a stage is PRESENT iff its PROGRESS `stage` string occurs inside the bold "
                       "label that opens a §1 bullet ('- **label**'); §1 = the text after the "
                       "'## 1 · STAGE LOG' heading up to the next '## ' heading"),
            "value": {"absent": len(absent), "stages": len(stages)},
            "absent_stages": absent, "section1_labels": labels,
            "absent_but_mentioned_in_section1_body": body_only}


MEASURES = (("i", m_i), ("ii", m_ii), ("iii", m_iii), ("iv", m_iv), ("v", m_v), ("vi", m_vi))

MEASURED_SOURCES = {
    "i": [REGTEXTS_JSON, REGTEXTS_MD],
    "ii": ["research_outputs/tierc10/scores"],
    "iii": ["analytics"],
    "iv": [PROGRESS, ".git"],
    "v": [".git"],
    "vi": [PROGRESS, DRAFT],
}
MEASURED_OWNER = {   # (owner, basis path, verbatim quote, reading)
    "i": ("executor", REGTEXTS_MD, "These are the exact bytes",
          "the document asserts byte-identity with the filing; re-rendering it is the executor's"),
    "ii": ("operator", CONTRACT, "the slippage-twin question named for the autopsy",
           "the contract routes the slippage-twin question to the autopsy"),
    "iii": ("operator", CONTRACT, "twin module-ized as analytics/rangefinder.py",
            "the contract names analytics/rangefinder.py; the executor's lean L3 names "
            "analytics/rangefinder_census.py; accepting the lean or ordering the rename is the "
            "operator's"),
    "iv": ("executor", CONTRACT, "after EVERY stage: commit + update research_outputs/tierc10/PROGRESS.json",
           "LAW 6 puts the ledger update on the executor"),
    "v": ("executor", CONTRACT, "Read-only worktrees for review",
          "the contract's worktree attestation is the executor's"),
    "vi": ("executor", CONTRACT, "+ one line to the draft",
           "LAW 6 puts the draft line on the executor"),
}


def _f4(x) -> str:
    return f"{x:+.4f}"


def measured_text(key: str, m: dict) -> str:
    v = m["value"]
    if key == "i":
        parts = [f"{p['reg_id']}: " + ("verbatim" if p["verbatim"] else
                 f"NOT verbatim — only its first {p['longest_verbatim_prefix_chars']:,} of "
                 f"{p['chars']:,} characters occur in the .md") for p in m["per_registration"]]
        return (f"{v['verbatim']} of {v['total']} REGISTRATION_TEXTS.json texts are found verbatim "
                f"in REGISTRATION_TEXTS.md. " + "; ".join(parts) + ".")
    if key == "ii":
        above = [a for a in m["arms"] if a["twin_above_tc"]]
        parts = [f"{Path(a['file']).name.replace('.rows.json', '')} rows[{a['row']}] "
                 f"'{a['arm']}': tc {_f4(a['tc_expectancy_r'])} R, twin {_f4(a['twin_expectancy_r'])} R"
                 for a in above]
        nt = [f"{Path(a['file']).name.replace('.rows.json', '')} rows[{a['row']}] '{a['arm']}'"
              for a in m["arms_without_twin"]]
        return (f"{v['twin_above_tc']} of {v['arms_with_twin']} arms that carry a haircut twin show "
                f"beside.haircut_twin.twin_expectancy_r > tc_expectancy_r"
                + (": " + "; ".join(parts) if parts else "") + ". "
                f"{v['arms_total'] - v['arms_with_twin']} of {v['arms_total']} arms carry no "
                f"haircut twin" + (": " + "; ".join(nt) if nt else "") + ".")
    if key == "iii":
        return "; ".join(f"os.path.exists({e['path']}) = {e['exists']}" for e in v) + "."
    if key == "iv":
        return (f"PROGRESS.json head {v['progress_head']} vs git rev-parse HEAD {v['git_head']}: "
                f"equal = {v['equal']}; the ledger's head is an ancestor of HEAD = "
                f"{v['progress_head_is_ancestor']}; commits on HEAD after the ledger's head = "
                f"{v['commits_after_progress_head']}.")
    if key == "v":
        hs = "; ".join(f"{h['head'][:12]} × {h['worktrees']}" for h in m["heads_besides_main"])
        main = next((r for r in m["worktrees"] if r["path"] == "."), None)
        return (f"{v['worktrees_besides_main']} worktree(s) besides the main one; "
                f"{v['worktrees_besides_main_with_zero_tierc10']} of them reach 0 of the "
                f"{v['tierc10_commits_on_HEAD']} tierc10 commits reachable from HEAD, "
                f"{v['worktrees_besides_main_with_all_tierc10']} reach all of them. Their HEADs: "
                f"{hs or 'none'}. The main working tree reaches "
                f"{main['tierc10_commits_reachable'] if main else 'n/a'} of "
                f"{v['tierc10_commits_on_HEAD']}.")
    if key == "vi":
        bo = m["absent_but_mentioned_in_section1_body"]
        return (f"{v['absent']} of {v['stages']} PROGRESS.json stages have no stage line in "
                f"BUILD_DRAFT.md §1: " + ", ".join(m["absent_stages"]) + ". §1's bullet labels are: "
                + ", ".join(m["section1_labels"]) + "."
                + (f" {len(bo)} of the absent stages are named in §1 only in passing: "
                   + ", ".join(bo) + "." if bo else ""))
    raise KeyError(key)


def measured_findings(measured: dict) -> list[dict]:
    out = []
    for key, _ in MEASURES:
        owner, bp, quote, reading = MEASURED_OWNER[key]
        out.append(_finding(
            f"FN-M-{key}", "MEASURED", "MEASURED", measured_text(key, measured[key]),
            MEASURED_SOURCES[key], f"measured.{key}", owner, bp, quote, reading,
            text_form="rendered from measured values recomputed this run"))
    return out


# ═══════════════════════════════════════════════════════════════════ build ══
def contract_clauses(root: Path) -> list[dict]:
    lines = read_text(root / CONTRACT).split("\n")
    out = []
    for needle in ("· findings-not-fixed", "the gap is filed as a finding"):
        hit = next((i for i, ln in enumerate(lines) if needle in ln), None)
        out.append({"needle": needle, "line": (hit + 1) if hit is not None else None,
                    "text": lines[hit] if hit is not None else None})
    return out


def build(root: Path) -> tuple[dict, str]:
    findings: list[dict] = []
    findings += harvest_progress(root)
    findings += harvest_rulings(root)
    findings += harvest_stage_d(root)
    findings += harvest_family(root)
    findings += harvest_toll(root)
    findings += harvest_plan(root)
    findings += harvest_draft(root)
    measured = {k: fn(root) for k, fn in MEASURES}
    findings += measured_findings(measured)
    findings += harvest_leans(root)
    prog = json.loads(read_text(root / PROGRESS))
    rul_lines = read_text(root / RULINGS).split("\n")
    r710 = next((i + 1 for i, ln in enumerate(rul_lines) if ln.startswith("# RULINGS OF")), None)
    r8 = next((i + 1 for i, ln in enumerate(rul_lines) if ln.startswith("## R8")), None)
    counts: dict[str, dict[str, int]] = {}
    for f in findings:
        c = counts.setdefault(f["class"], {"operator": 0, "executor": 0, "total": 0})
        c[f["owner"]] += 1
        c["total"] += 1
    doc = {
        "schema": "tierc10.close.S5_FINDINGS_NOT_FIXED.v1",
        "label": LABEL_DOC,
        "status_law": (f"every finding's status is '{STATUS}': it records what THIS build did "
                       f"(report, never fix); it does not claim the item is still open"),
        "tier": prog.get("tier"),
        "as_of_of_record": prog.get("as_of_of_record"),
        "contract": {"path": CONTRACT, "sha256": sha256_file(root / CONTRACT),
                     "clauses": contract_clauses(root)},
        "built_by": SELF_REL,
        "inputs": input_manifest(root),
        "git_volatile_fields": list(GIT_VOLATILE),
        "git": {"head_at_build": git("rev-parse", "HEAD").stdout.strip()},
        "cross_references": {
            "panel_pin_gap_filed_as": [f["id"] for f in findings if "PANEL PIN" in f["text"]],
            "rulings_r7_r10_heading_line": r710,
            "rulings_r8_heading_line": r8,
            "harvested_texts_recording_their_own_repair": [
                f["id"] for f in findings if f["text"].startswith("REPAIRED")],
            "owners_by_default_rule": [
                f["id"] for f in findings if f["owner_basis"]["reading"].startswith("DEFAULT RULE")],
        },
        "counts": counts,
        "measured": measured,
        "findings": findings,
    }
    return doc, render_md(doc)


# ════════════════════════════════════════════════════════════════ render ══
def _fence(text: str) -> str:
    runs = [len(m) for m in re.findall(r"~{3,}", text)]
    return "~" * max(3, (max(runs) + 1) if runs else 3)


def _src(f: dict) -> str:
    p = f["source"]["path"]
    ps = ", ".join(f"`{x}`" for x in p) if isinstance(p, list) else f"`{p}`"
    return f"{ps} · `{f['source']['field']}`"


def _finding_block(f: dict) -> list[str]:
    ctx = f["source"].get("context") or {}
    extra = ""
    if "stage" in ctx:
        extra = f" · stage **{ctx['stage']}** ({ctx['stage_status']})"
        if ctx.get("repair_line_in_same_list"):
            extra += (" · the same list's REPAIRED line: "
                      + ", ".join(f"`{r}`" for r in ctx["repair_line_in_same_list"]))
    elif "lean_id" in ctx:
        extra = f" · lean id `{ctx['lean_id']}` (column `{ctx['lean_id_column']}`)"
    fence = _fence(f["text"])
    ob = f["owner_basis"]
    return [
        f"#### {f['id']}",
        "",
        f"- **{f['class']}** · owner **{f['owner']}** · status **{f['status']}**{extra}",
        f"- source: {_src(f)}" + (f" · text form: {f['text_form']}" if f["text_form"] != "verbatim string" else ""),
        f"- owner basis: `{ob['path']}` — \"{ob['quote']}\" — *{ob['reading']}*",
        "",
        f"{fence}text",
        f["text"],
        fence,
        "",
    ]


def render_md(doc: dict) -> str:
    F = doc["findings"]
    by = lambda k: [f for f in F if f["harvest_key"] == k]   # noqa: E731
    L: list[str] = []
    a = L.append
    a("# TIER-C10 · CLOSE · §5 FINDINGS — REPORTED, NOT FIXED")
    a("")
    a(f"> **{doc['label']}**")
    a(">")
    a(f"> {doc['status_law'][0].upper()}{doc['status_law'][1:]}. Harvested texts are VERBATIM with "
      f"their source path and field; measured values are recomputed on every run and never typed. "
      f"Built by `{doc['built_by']}`; fixture transcript `{TRANSCRIPT}` beside this file.")
    a("")
    c = doc["contract"]
    a(f"- **Contract of record:** `{c['path']}` sha256 `{c['sha256']}` (equal to PROGRESS.json "
      f"`contract_of_record.sha256`, or the preamble would have HALTed)")
    for cl in c["clauses"]:
        a(f"- **Clause:** line {cl['line']} — `{(cl['text'] or '').strip()}`")
    a(f"- **AS-OF OF RECORD:** {doc['as_of_of_record']} (PROGRESS.json `as_of_of_record`)")
    xr = doc["cross_references"]
    a(f"- **The contract's PANEL PIN gap ('the gap is filed as a finding'):** filed here as "
      + (", ".join(f"`{i}`" for i in xr["panel_pin_gap_filed_as"]) or "*no finding names the PANEL PIN*")
      + f"; OPERATOR_RULINGS.md settles it at its `## R8` heading (line {xr['rulings_r8_heading_line']}).")
    a(f"- **Order of the two 'Still blocked' lists:** list 1 is headed at line "
      f"{by('RULINGS-L1')[0]['source']['context']['heading_line'] if by('RULINGS-L1') else '—'}, "
      f"BEFORE `# RULINGS OF 2026-09-22 (R7–R10)` at line {xr['rulings_r7_r10_heading_line']}; list 2 "
      f"is headed at line {by('RULINGS-L2')[0]['source']['context']['heading_line'] if by('RULINGS-L2') else '—'}. "
      f"List 1 is printed because the spec harvests both; where R7–R10 settled an item, list 2 is the later word.")
    a(f"- **Harvested texts that record their own repair:** "
      + (", ".join(f"`{i}`" for i in xr["harvested_texts_recording_their_own_repair"]) or "none")
      + " — read those beside the items they repair.")
    a(f"- **Owners assigned by the DEFAULT RULE (no declared rule matched):** "
      + (", ".join(f"`{i}`" for i in xr["owners_by_default_rule"]) or "none") + ".")
    a("")
    a("## 0 · Inputs, read-only")
    a("")
    a("*REPORT-ONLY · Tier-E — every file this build reads; F-FN-READONLY proves none changed.*")
    a("")
    a("| input | bytes | sha256 |")
    a("|---|---:|---|")
    for rel, m in doc["inputs"].items():
        a(f"| `{rel}` | {m['bytes'] if m['bytes'] is not None else 'MISSING'} | `{m['sha256']}` |")
    a("")
    a("## 1 · Counts and index")
    a("")
    a("*REPORT-ONLY · Tier-E — counts of this file's findings by class and owner.*")
    a("")
    a("| class | operator | executor | total |")
    a("|---|---:|---:|---:|")
    tot = {"operator": 0, "executor": 0, "total": 0}
    for cls in ("HARVESTED", "MEASURED", "LEAN"):
        cc = doc["counts"].get(cls, {"operator": 0, "executor": 0, "total": 0})
        for k in tot:
            tot[k] += cc[k]
        a(f"| {cls} | {cc['operator']} | {cc['executor']} | {cc['total']} |")
    a(f"| **all** | **{tot['operator']}** | **{tot['executor']}** | **{tot['total']}** |")
    a("")
    a("*REPORT-ONLY · Tier-E — the index: one row per finding, in document order.*")
    a("")
    a("| id | class | owner | source | field |")
    a("|---|---|---|---|---|")
    for f in F:
        p = f["source"]["path"]
        ps = ", ".join(p) if isinstance(p, list) else p
        a(f"| `{f['id']}` | {f['class']} | {f['owner']} | `{ps}` | `{f['source']['field']}` |")
    a("")
    a("## 2 · Measured at build time — (i) to (vi)")
    a("")
    a("*REPORT-ONLY · Tier-E — recomputed on every run, never typed; F-FN-MEASURED re-derives each "
      "by an independent path. (iv) and (v) are git-volatile and are printed in marked blocks.*")
    a("")
    a("| # | measure | value | owner |")
    a("|---|---|---|---|")
    M = doc["measured"]
    for key, _ in MEASURES:
        v = M[key]["value"]
        if key in ("iv", "v"):
            val = "git-volatile — see §2." + key
        elif key == "iii":
            val = "; ".join(f"`{e['path']}` {e['exists']}" for e in v)
        else:
            val = " / ".join(f"{k} {x}" for k, x in v.items())
        a(f"| ({key}) | {M[key]['measure']} | {val} | {MEASURED_OWNER[key][0]} |")
    a("")
    for key, _ in MEASURES:
        f = next(x for x in F if x["id"] == f"FN-M-{key}")
        vol = key in ("iv", "v")
        a(f"### 2.{key}")
        a("")
        if vol:
            a(VOL_BEGIN)
        a(f"*Method:* {M[key]['method']}.")
        a("")
        L.extend(_finding_block(f))
        if key == "ii":
            a("*REPORT-ONLY · Tier-E — the haircut-twin arms; values read from each file's "
              "`rows[n].beside.haircut_twin`; no verdict field is read.*")
            a("")
            a("| file | row | arm | tc_expectancy_r | twin_expectancy_r | twin − tc | twin > tc |")
            a("|---|---:|---|---:|---:|---:|---|")
            for r in M["ii"]["arms"]:
                a(f"| `{Path(r['file']).name}` | {r['row']} | {r['arm']} | {_f4(r['tc_expectancy_r'])} | "
                  f"{_f4(r['twin_expectancy_r'])} | {_f4(r['twin_minus_tc_r'])} | {r['twin_above_tc']} |")
            for r in M["ii"]["arms_without_twin"]:
                a(f"| `{Path(r['file']).name}` | {r['row']} | {r['arm']} | — | — | — | no twin on the row |")
            a("")
        if key == "v":
            a("*REPORT-ONLY · Tier-E — every worktree `git worktree list` names.*")
            a("")
            a("| path | head | branch | tierc10 commits reachable |")
            a("|---|---|---|---:|")
            for r in M["v"]["worktrees"]:
                a(f"| `{r['path']}` | `{r['head'][:12]}` | `{r['branch']}` | {r['tierc10_commits_reachable']} |")
            a("")
        if key == "iv" and M["iv"]["commits_after_progress_head"]:
            a("*REPORT-ONLY · Tier-E — commits on HEAD after the ledger's recorded head.*")
            a("")
            a("| sha | subject |")
            a("|---|---|")
            for r in M["iv"]["commits_after_progress_head"]:
                a(f"| `{r['sha7']}` | {r['subject'].replace('|', '/')} |")
            a("")
        if vol:
            a(VOL_END)
            a("")
    sections = (
        ("3.1", "PROGRESS.json — every stages[].blockers and stages[].notes string", "PROGRESS"),
        ("3.2", "OPERATOR_RULINGS.md — the first 'Still blocked' list", "RULINGS-L1"),
        ("3.3", "OPERATOR_RULINGS.md — the second 'Still blocked' list (after R7–R10)", "RULINGS-L2"),
        ("3.4", "STAGE_D_MANIFEST.json — operator_rulings_needed", "SDM-ORN"),
        ("3.5", "STAGE_D_MANIFEST.json — as_of_hazards", "SDM-HAZ"),
        ("3.6", "FAMILY.json — scored_slots_halted", "FAMILY"),
        ("3.7", "Every brk_sealed_row.toll_accounting_status under scores/", "TOLL"),
        ("3.8", "REGISTRATION_PLAN.md — the 'drafting error' paragraph", "PLAN"),
        ("3.9", "BUILD_DRAFT.md §R0.3 — the smoke-roots paragraph (DISCLOSED ONLY: nothing is "
                "moved or deleted, LAW 2)", "DRAFT"),
    )
    a("## 3 · Harvested — verbatim, by source")
    a("")
    for num, title, key in sections:
        a(f"### {num} · {title}")
        a("")
        items = by(key)
        if key.startswith("RULINGS") and items:
            ctx = items[0]["source"]["context"]
            a(f"*Heading (line {ctx['heading_line']}):* `{ctx['heading']}`")
            a("")
        for f in items:
            L.extend(_finding_block(f))
    a("## 4 · LEANS — labelled as leans")
    a("")
    a(f"> **{LABEL_LEAN}** OPERATOR_RULINGS.md: \"the lean is marked as such and is NOT the ruling.\"")
    a("")
    for key, rel, _, _ in LEANS:
        a(f"### 4.{key.lower()} · `{rel}`")
        a("")
        for f in by(f"LEAN-{key}"):
            L.extend(_finding_block(f))
    a("## 5 · The git-volatile fields — named, and excluded from F-DET")
    a("")
    for g in doc["git_volatile_fields"]:
        a(f"- `{g}`")
    a(f"- in this Markdown: every block between `{VOL_BEGIN}` and `{VOL_END}`")
    a("")
    a("## 6 · What this document is not")
    a("")
    a("- Not a fix. No input is edited; F-FN-READONLY proves it on every run.")
    a("- Not a score. No registration is scored or re-scored and no verdict field is read; the "
      "only values read out of the scores/ files are `arm`, "
      "`beside.haircut_twin.{tc,twin}_expectancy_r`, `brk_sealed_row.toll_accounting_status` and "
      "FAMILY.json `scored_slots_halted`.")
    a("- Not a read of bars. No kline or funding file is opened.")
    a("- Not a claim that every item is open: the status says what this build did, not what "
      "the item is. The texts that record their own repair are listed above.")
    a("- Not a ruling. Every owner is the executor's reading, and its basis is quoted verbatim "
      "so it can be checked.")
    a("")
    return "\n".join(L)


def write_outputs(doc: dict, md: str, outdir: Path) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / OUT_JSON).write_bytes((json.dumps(doc, indent=1, ensure_ascii=False) + "\n").encode("utf-8"))
    (outdir / OUT_MD).write_bytes(md.encode("utf-8"))


# ══════════════════════════════════════════════════════════════ fixtures ══
def _json_get(obj, field: str):
    """The INDEPENDENT resolver F-FN-SOURCE uses (not the harvest walk)."""
    for idx, key in re.findall(r"\[(\d+)\]|([^.\[\]]+)", field):
        obj = obj[int(idx)] if idx else obj[key]
    return obj


def _resolve(root: Path, path: str, field: str):
    p = root / path
    if path.endswith(".json"):
        v = _json_get(json.loads(p.read_bytes().decode("utf-8")), field)
        return v if isinstance(v, str) else canon(v)
    if path.endswith(".md"):
        m = re.fullmatch(r"lines (\d+)-(\d+)", field)
        lines = p.read_bytes().decode("utf-8").splitlines()
        return "\n".join(lines[int(m.group(1)) - 1:int(m.group(2))])
    if path.endswith(".parquet"):
        import pyarrow.parquet as pq
        m = re.fullmatch(r"row (\d+) · column (.+)", field)
        return str(pq.read_table(p).column(m.group(2))[int(m.group(1))].as_py())
    raise ValueError(f"no resolver for {path}")


def _all_strings(o) -> list[str]:
    if isinstance(o, str):
        return [o]
    if isinstance(o, dict):
        return [s for v in o.values() for s in _all_strings(v)]
    if isinstance(o, list):
        return [s for v in o for s in _all_strings(v)]
    return []


def _basis_holds(root: Path, path: str, quote: str) -> bool:
    p = root / path
    if not p.is_file():
        return False
    raw = p.read_bytes().decode("utf-8")
    if path.endswith(".json"):
        return any(quote in s for s in _all_strings(json.loads(raw)))
    return quote in raw


# ── F-FN-HARVEST
def check_harvest(findings: list[dict], progress_path: Path) -> list[str]:
    bad = []
    prog = json.loads(progress_path.read_bytes().decode("utf-8"))
    want: list[str] = []
    for st in prog.get("stages", []):
        for kind in ("blockers", "notes"):
            v = st.get(kind)
            if v is None:
                continue
            for s in (v if isinstance(v, list) else [v]):
                want.append(s if isinstance(s, str) else canon(s))
    got = [f["text"] for f in findings if f["source"]["path"] == PROGRESS
           and re.match(r"^stages\[\d+\]\.(blockers|notes)", f["source"]["field"])]
    for s in want:
        if s not in got:
            bad.append(f"HARVEST: PROGRESS string absent from the findings: {s[:90]!r}…")
    if sorted(want) != sorted(got):
        bad.append(f"HARVEST: PROGRESS-sourced findings ({len(got)}) are not exactly the "
                   f"ledger's blocker/note multiset ({len(want)})")
    for k in HARVEST_KEYS:
        if not any(f["harvest_key"] == k for f in findings):
            bad.append(f"HARVEST: declared source {k} contributed ZERO findings")
    return bad


# ── F-FN-SOURCE
def check_source(findings: list[dict], root: Path) -> list[str]:
    bad = []
    seen: set[str] = set()
    for f in findings:
        fid = f.get("id")
        if not fid or fid in seen:
            bad.append(f"SOURCE: id {fid!r} is missing or repeated")
        seen.add(fid)
        for k in ("text", "source", "owner", "status"):
            if k not in f:
                bad.append(f"SOURCE: {fid} lacks {k!r}")
        if f.get("status") != STATUS:
            bad.append(f"SOURCE: {fid} status {f.get('status')!r} is not {STATUS!r}")
        if f.get("owner") not in OWNERS:
            bad.append(f"SOURCE: {fid} owner {f.get('owner')!r} is not one of {OWNERS}")
        paths = f["source"]["path"]
        paths = paths if isinstance(paths, list) else [paths]
        for p in paths:
            if not (root / p).exists():
                bad.append(f"SOURCE: {fid} source path {p!r} does not exist")
        if f["class"] != "MEASURED" and all((root / p).exists() for p in paths):
            try:
                got = _resolve(root, paths[0], f["source"]["field"])
            except Exception as e:                       # a bad field is a finding, not a crash
                bad.append(f"SOURCE: {fid} field {f['source']['field']!r} does not resolve ({type(e).__name__})")
            else:
                if got != f["text"]:
                    bad.append(f"SOURCE: {fid} text is not VERBATIM at {paths[0]} · {f['source']['field']}")
        ob = f.get("owner_basis") or {}
        if not _basis_holds(root, ob.get("path", ""), ob.get("quote") or "\x00"):
            bad.append(f"SOURCE: {fid} owner-basis quote is not verbatim at {ob.get('path')!r}")
    return bad


# ── F-FN-MEASURED: the SECOND, INDEPENDENT recomputation
def _git_dir() -> Path:
    return ROOT / ".git"


def _resolve_ref_raw(ref: str) -> str:
    gd = _git_dir()
    loose = gd / ref
    if loose.is_file():
        return loose.read_text().strip()
    packed = gd / "packed-refs"
    if packed.is_file():
        for ln in packed.read_text().splitlines():
            if ln and not ln.startswith(("#", "^")):
                sha, _, name = ln.partition(" ")
                if name == ref:
                    return sha
    raise RuntimeError(f"ref {ref} unresolved")


def _head_file_raw(headfile: Path) -> str:
    s = headfile.read_text().strip()
    return _resolve_ref_raw(s[5:].strip()) if s.startswith("ref:") else s


def _tierc10_set_catfile() -> list[str]:
    shas = subprocess.run(["git", "-C", str(ROOT), "rev-list", "HEAD"], capture_output=True,
                          text=True, check=True).stdout.split()
    p = subprocess.run(["git", "-C", str(ROOT), "cat-file", "--batch"],
                       input=("\n".join(shas) + "\n").encode(), capture_output=True, check=True)
    buf, pos, out = p.stdout, 0, []
    while pos < len(buf):
        nl = buf.index(b"\n", pos)
        sha, typ, size = buf[pos:nl].decode().split()
        body = buf[nl + 1: nl + 1 + int(size)].decode("utf-8", "replace")
        pos = nl + 1 + int(size) + 1
        msg = body.split("\n\n", 1)[1] if "\n\n" in body else ""
        if typ == "commit" and msg.split("\n", 1)[0].startswith(TIERC10_SUBJECT_PREFIX):
            out.append(sha)
    return out


def recompute_independent(root: Path) -> dict:
    r: dict = {}
    # (i) bytes-level search
    jb = json.loads((root / REGTEXTS_JSON).read_bytes().decode("utf-8"))
    mdb = (root / REGTEXTS_MD).read_bytes()
    flags = {rid: mdb.find(v["text"].encode("utf-8")) >= 0 for rid, v in jb.items()}
    r["i"] = (sum(flags.values()), len(flags), tuple(sorted(flags.items())))
    # (ii) Decimal parse, generic walk for haircut_twin under rows[]
    above, with_twin, total, per = 0, 0, 0, []
    for q in sorted(os.listdir(root / SCORES_DIR)):
        if not (q.startswith("P-") and q.endswith(".rows.json")):
            continue
        o = json.loads((root / SCORES_DIR / q).read_bytes(), parse_float=Decimal)
        for i, row in enumerate(o["rows"]):
            total += 1
            b = row.get("beside")
            ht = b.get("haircut_twin") if isinstance(b, dict) else None
            if isinstance(ht, dict):
                with_twin += 1
                up = Decimal(ht["twin_expectancy_r"]) > Decimal(ht["tc_expectancy_r"])
                above += up
                per.append((f"{SCORES_DIR}/{q}", i, bool(up)))
    r["ii"] = (above, with_twin, total, tuple(per))
    # (iii) directory listing, not os.path.exists
    r["iii"] = tuple((rel, os.path.basename(rel) in os.listdir(root / os.path.dirname(rel))
                      if (root / os.path.dirname(rel)).is_dir() else False) for rel in RF_PATHS)
    # (iv) raw .git refs + rev-list set difference
    ph = json.loads((root / PROGRESS).read_bytes())["head"]
    gh = _head_file_raw(_git_dir() / "HEAD")
    head_set = set(subprocess.run(["git", "-C", str(ROOT), "rev-list", gh], capture_output=True,
                                  text=True, check=True).stdout.split())
    anc = ph in head_set
    ph_set = set(subprocess.run(["git", "-C", str(ROOT), "rev-list", ph], capture_output=True,
                                text=True, check=True).stdout.split()) if anc else set()
    r["iv"] = (ph, gh, ph == gh, anc, len(head_set - ph_set) if anc else None)
    # (v) .git/worktrees/*/{gitdir,HEAD} + cat-file subjects + merge-base per commit
    tc = _tierc10_set_catfile()
    wt = [(".", gh)]
    wdir = _git_dir() / "worktrees"
    if wdir.is_dir():
        for name in sorted(os.listdir(wdir)):
            gd = wdir / name
            if (gd / "gitdir").is_file() and (gd / "HEAD").is_file():
                wpath = os.path.dirname(gd.joinpath("gitdir").read_text().strip())
                wt.append((_rel_to_root(wpath), _head_file_raw(gd / "HEAD")))
    cache: dict[str, int] = {}
    rows = []
    for path, head in wt:
        if head not in cache:
            cache[head] = sum(subprocess.run(["git", "-C", str(ROOT), "merge-base", "--is-ancestor",
                                              c, head]).returncode == 0 for c in tc)
        rows.append((path, head, cache[head]))
    r["v"] = (len(tc), tuple(sorted(rows)))
    # (vi) a line scanner, not a regex over the section
    stages = [s["stage"] for s in json.loads((root / PROGRESS).read_bytes())["stages"]]
    sec_lines, inside = [], False
    for ln in (root / DRAFT).read_bytes().decode("utf-8").splitlines():
        if ln.startswith("## 1 · STAGE LOG"):
            inside = True
            continue
        if inside and ln.startswith("## "):
            break
        if inside:
            sec_lines.append(ln)
    labels = []
    for ln in sec_lines:
        if ln.startswith("- **"):
            end = ln.find("**", 4)
            if end > 4:
                labels.append(ln[4:end])
    body = "\n".join(sec_lines)
    absent = [s for s in stages if not any(s in lab for lab in labels)]
    r["vi"] = (tuple(absent), tuple(labels), tuple(s for s in absent if s in body))
    return r


def primary_tuple(doc: dict) -> dict:
    M = doc["measured"]
    t: dict = {}
    t["i"] = (M["i"]["value"]["verbatim"], M["i"]["value"]["total"],
              tuple(sorted((p["reg_id"], p["verbatim"]) for p in M["i"]["per_registration"])))
    v = M["ii"]["value"]
    t["ii"] = (v["twin_above_tc"], v["arms_with_twin"], v["arms_total"],
               tuple((a["file"], a["row"], a["twin_above_tc"]) for a in M["ii"]["arms"]))
    t["iii"] = tuple((e["path"], e["exists"]) for e in M["iii"]["value"])
    v = M["iv"]["value"]
    t["iv"] = (v["progress_head"], v["git_head"], v["equal"], v["progress_head_is_ancestor"],
               v["commits_after_progress_head"])
    t["v"] = (M["v"]["value"]["tierc10_commits_on_HEAD"],
              tuple(sorted((r["path"], r["head"], r["tierc10_commits_reachable"])
                           for r in M["v"]["worktrees"])))
    t["vi"] = (tuple(M["vi"]["absent_stages"]), tuple(M["vi"]["section1_labels"]),
               tuple(M["vi"]["absent_but_mentioned_in_section1_body"]))
    return t


def check_measured(doc: dict, indep: dict) -> list[str]:
    bad = []
    try:
        prim = primary_tuple(doc)
    except Exception as e:
        return [f"MEASURED: the filed JSON's measured block is malformed ({type(e).__name__}: {e})"]
    for key, _ in MEASURES:
        if prim[key] != indep[key]:
            bad.append(f"MEASURED ({key}): filed {str(prim[key])[:120]} != independent "
                       f"{str(indep[key])[:120]}")
    for key, _ in MEASURES:   # the finding's text must be the render of the filed value
        f = next((x for x in doc["findings"] if x["id"] == f"FN-M-{key}"), None)
        if f is None or f["text"] != measured_text(key, doc["measured"][key]):
            bad.append(f"MEASURED ({key}): FN-M-{key} text is not the render of measured.{key}")
    return bad


# ── F-FN-NOSCORE
FORBIDDEN_MODULES = ("tierc10_panel", "tierc10_score", "tierc2_baseline", "tierc10_data",
                     "tierc10_file_registrations", "engine")
FORBIDDEN_CALLS = ("score", "finish_family", "register", "load_klines", "load_asof")


def check_noscore(src: str) -> list[str]:
    bad = []
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for n in node.names:
                if n.name.split(".")[0] in FORBIDDEN_MODULES:
                    bad.append(f"NOSCORE: imports {n.name}")
        elif isinstance(node, ast.ImportFrom):
            if (node.module or "").split(".")[0] in FORBIDDEN_MODULES:
                bad.append(f"NOSCORE: imports from {node.module}")
        elif isinstance(node, ast.Call):
            fn = node.func
            name = fn.attr if isinstance(fn, ast.Attribute) else getattr(fn, "id", None)
            if name in FORBIDDEN_CALLS:
                bad.append(f"NOSCORE: calls {name}() at line {node.lineno}")
            if (name == "get" and node.args and isinstance(node.args[0], ast.Constant)
                    and node.args[0].value == "verdict"):
                bad.append(f"NOSCORE: .get('verdict') at line {node.lineno}")
        elif isinstance(node, ast.Subscript):
            s = node.slice
            if isinstance(s, ast.Constant) and s.value == "verdict":
                bad.append(f"NOSCORE: ['verdict'] at line {node.lineno}")
    return bad


# ── F-DET
def mask_json(doc: dict) -> dict:
    d = copy.deepcopy(doc)
    for spec in d.get("git_volatile_fields", GIT_VOLATILE):
        m = re.fullmatch(r"findings\[id=(.+?)\]\.(\w+)", spec)
        if m:
            for f in d["findings"]:
                if f["id"] == m.group(1):
                    f[m.group(2)] = "<git-volatile>"
            continue
        parts = spec.split(".")
        o = d
        for p in parts[:-1]:
            o = o[p]
        o[parts[-1]] = "<git-volatile>"
    return d


def mask_md(md: str) -> str:
    return re.sub(re.escape(VOL_BEGIN) + r".*?" + re.escape(VOL_END), "<git-volatile>", md, flags=re.S)


def check_det(ja: bytes, jb: bytes, ma: bytes, mb: bytes) -> list[str]:
    bad = []
    da, db = json.loads(ja), json.loads(jb)
    if da.get("git_volatile_fields") != list(GIT_VOLATILE) or db.get("git_volatile_fields") != list(GIT_VOLATILE):
        bad.append("DET: a build's git_volatile_fields is not exactly the NAMED GIT_VOLATILE tuple")
    if canon(mask_json(da)) != canon(mask_json(db)):
        bad.append("DET: the two JSON builds differ outside the named git-volatile fields")
    if mask_md(ma.decode("utf-8")) != mask_md(mb.decode("utf-8")):
        bad.append("DET: the two Markdown builds differ outside the git-volatile blocks")
    return bad


def _subprocess_build(outdir: Path) -> list[str]:
    p = subprocess.run([sys.executable, "-B", str(Path(__file__).resolve()), "--build-into",
                        str(outdir)], capture_output=True, text=True, env=dict(os.environ))
    if p.returncode != 0 or not (outdir / OUT_JSON).is_file() or not (outdir / OUT_MD).is_file():
        return [f"DET: a cross-process build exited {p.returncode} without both outputs: "
                f"{(p.stdout + p.stderr).strip()[:200]}"]
    return []


# ── F-FN-READONLY
def check_readonly(before: dict, after: dict) -> list[str]:
    bad = []
    for rel in sorted(set(before) | set(after)):
        if before.get(rel) != after.get(rel):
            bad.append(f"READONLY: {rel} changed ({(before.get(rel) or {}).get('sha256')} -> "
                       f"{(after.get(rel) or {}).get('sha256')})")
    return bad


def _copy_inputs(dst: Path) -> None:
    for rel in input_paths(ROOT):
        s = ROOT / rel
        if s.is_file():
            (dst / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(s, dst / rel)


# ══════════════════════════════════════════════════════════════════ legs ══
class Suite:
    def __init__(self):
        self.lines: list[str] = []
        self.results: list[tuple[str, bool]] = []

    def say(self, s: str = "") -> None:
        self.lines.append(s)
        print(s, flush=True)

    def leg(self, name: str, fails_if: str, real: list[str],
            sabotages: list[tuple[str, list[str]]], controls: list[tuple[str, list[str]]] = ()):
        self.say("-" * 78)
        self.say(f"{name}")
        self.say(f"  FAILS IF: {fails_if}")
        ok = not real
        self.say(f"  real: {'GREEN' if not real else 'RED'}" + ("" if not real else f" ({len(real)} problem(s))"))
        for p in real[:40]:
            self.say(f"    [BAD] {p}")
        for label, probs in sabotages:
            red = bool(probs)
            ok &= red
            self.say(f"  sabotage · {label}: {'RED (as required)' if red else 'GREEN — THE GUARD DID NOT FIRE'}")
            if red:
                self.say(f"    first: {probs[0][:150]}")
        for label, probs in controls:
            green = not probs
            ok &= green
            self.say(f"  control · {label}: {'GREEN (as required)' if green else 'RED — THE MASK IS WIDER THAN NAMED'}")
            for p in probs[:3]:
                self.say(f"    [BAD] {p[:150]}")
        self.say(f"  => {name}: {'PASS' if ok else 'FAIL'}")
        self.results.append((name, ok))


def run_suite(want: list[str]) -> int:
    S = Suite()
    try:
        pre = preamble()
    except SystemExit as e:
        print(str(e), flush=True)
        return 1
    S.say("=" * 78)
    S.say("TIER-C10 · CLOSE · §5 FINDINGS — REPORTED, NOT FIXED · fixtures (break legs RED or void)")
    S.say("=" * 78)
    for ln in pre:
        S.say(ln)
    before = input_manifest(ROOT)
    S.say(f"inputs (read-only): {len(before)} files")
    for rel, m in before.items():
        S.say(f"  {rel}  {m['bytes']} B  sha256 {m['sha256']}")

    doc, md = build(ROOT)
    outdir = ROOT / OUT_DIR_REL
    write_outputs(doc, md, outdir)
    jbytes = (outdir / OUT_JSON).read_bytes()
    mbytes = (outdir / OUT_MD).read_bytes()
    filed = json.loads(jbytes)
    S.say(f"built: {OUT_DIR_REL}/{OUT_JSON} sha256 {sha256_bytes(jbytes)} ({len(jbytes)} B)")
    S.say(f"built: {OUT_DIR_REL}/{OUT_MD} sha256 {sha256_bytes(mbytes)} ({len(mbytes)} B)")
    S.say(f"findings: {len(filed['findings'])} · counts {canon(filed['counts'])}")
    S.say(f"git_volatile_fields (excluded from F-DET): {', '.join(GIT_VOLATILE)}")
    for key, _ in MEASURES:
        f = next(x for x in filed["findings"] if x["id"] == f"FN-M-{key}")
        S.say(f"measured ({key}){' [git-volatile]' if key in ('iv', 'v') else ''}: {f['text']}")
    F = filed["findings"]
    sel = lambda n: not want or any(w in n.lower() for w in want)   # noqa: E731

    # ── F-FN-HARVEST
    if sel("f-fn-harvest"):
        real = check_harvest(F, ROOT / PROGRESS)
        with tempfile.TemporaryDirectory() as td:
            cp = Path(td) / "PROGRESS.json"
            pj = json.loads((ROOT / PROGRESS).read_bytes())
            pj["stages"][0]["blockers"] = list(pj["stages"][0].get("blockers") or []) + [
                "PLANTED BLOCKER — added to a COPY of PROGRESS.json by F-FN-HARVEST's sabotage"]
            cp.write_text(json.dumps(pj, ensure_ascii=False))
            sab1 = check_harvest(F, cp)
        drop_one = [f for f in F if f["id"] != next(x["id"] for x in F if x["harvest_key"] == "PROGRESS")]
        sab2 = check_harvest(drop_one, ROOT / PROGRESS)
        sab3 = check_harvest([f for f in F if f["harvest_key"] != "LEAN-STAMPS"], ROOT / PROGRESS)
        S.leg("F-FN-HARVEST",
              "any PROGRESS.json stages[].blockers / stages[].notes string (re-read independently) is "
              "absent from the findings verbatim, the PROGRESS-sourced findings are not exactly that "
              "multiset, or a declared harvest source contributed zero findings",
              real, [("a blocker added to a COPY of PROGRESS.json", sab1),
                     ("one PROGRESS finding dropped from a copy of the findings", sab2),
                     ("every stamps lean dropped (a silent empty source)", sab3)])

    # ── F-FN-SOURCE
    if sel("f-fn-source"):
        real = check_source(F, ROOT)
        def bent(fn):
            c = copy.deepcopy(F)
            fn(c)
            return check_source(c, ROOT)
        first_h = next(i for i, f in enumerate(F) if f["class"] == "HARVESTED")
        sabs = [
            ("a source path that does not exist",
             bent(lambda c: c[first_h]["source"].__setitem__("path", f"{TC}/NO_SUCH_FILE.json"))),
            ("the text bent by one character",
             bent(lambda c: c[first_h].__setitem__("text", c[first_h]["text"] + "."))),
            ("the owner-basis quote bent",
             bent(lambda c: c[first_h]["owner_basis"].__setitem__("quote", c[first_h]["owner_basis"]["quote"] + " PLANTED"))),
            ("status set to 'FIXED'", bent(lambda c: c[0].__setitem__("status", "FIXED"))),
            ("owner set to 'nobody'", bent(lambda c: c[0].__setitem__("owner", "nobody"))),
            ("a duplicated id", bent(lambda c: c[1].__setitem__("id", c[0]["id"]))),
        ]
        S.leg("F-FN-SOURCE",
              "a finding's source path does not exist, its field does not re-resolve to its text "
              "verbatim, its owner is not operator|executor, its owner-basis quote is not verbatim "
              "at the basis path, its status is not 'REPORTED, NOT FIXED', or an id repeats",
              real, sabs)

    # ── F-FN-MEASURED
    if sel("f-fn-measured"):
        indep = recompute_independent(ROOT)
        real = check_measured(filed, indep)
        def stale(fn):
            d = copy.deepcopy(filed)
            fn(d["measured"])
            return check_measured(d, indep)
        sabs = [
            ("(i) a stale verbatim count", stale(lambda m: m["i"]["value"].__setitem__("verbatim", m["i"]["value"]["verbatim"] + 1))),
            ("(ii) a stale twin>tc count", stale(lambda m: m["ii"]["value"].__setitem__("twin_above_tc", m["ii"]["value"]["twin_above_tc"] + 1))),
            ("(iii) a flipped existence", stale(lambda m: m["iii"]["value"][0].__setitem__("exists", not m["iii"]["value"][0]["exists"]))),
            ("(iv) a stale commits-after count", stale(lambda m: m["iv"]["value"].__setitem__(
                "commits_after_progress_head", (m["iv"]["value"]["commits_after_progress_head"] or 0) + 1))),
            ("(v) a stale per-worktree reach", stale(lambda m: m["v"]["worktrees"][-1].__setitem__(
                "tierc10_commits_reachable", m["v"]["worktrees"][-1]["tierc10_commits_reachable"] + 1))),
            ("(vi) a stale absent-stage list", stale(lambda m: m["vi"].__setitem__("absent_stages", m["vi"]["absent_stages"][1:]))),
        ]
        S.say("  independent recomputation: " + " · ".join(
            f"({k}) {str(indep[k][:2] if k in ('i', 'ii', 'iv') else (indep[k] if k == 'iii' else (indep[k][0] if k == 'v' else len(indep[k][0]))))}"
            for k, _ in MEASURES))
        S.leg("F-FN-MEASURED",
              "any of (i)-(vi) in the filed JSON differs from a second, independent recomputation "
              "(bytes search · Decimal parse · os.listdir · raw .git refs + rev-list sets · "
              "cat-file subjects + merge-base · a line scanner), or a measured finding's text is "
              "not the render of its filed value",
              real, sabs)

    # ── F-FN-NOSCORE
    if sel("f-fn-noscore"):
        src = read_text(Path(__file__).resolve())
        real = check_noscore(src)
        S.leg("F-FN-NOSCORE",
              "this module's AST imports a scoring / registration / bar-loading module, calls "
              "score / finish_family / register / load_klines / load_asof, or reads a 'verdict' key",
              real, [("an import of tierc10_score planted in a COPY of the source",
                      check_noscore(src + "\nimport tierc10_score\n")),
                     ("a call to finish_family planted", check_noscore(src + "\nTP.finish_family()\n")),
                     ("a ['verdict'] read planted", check_noscore(src + "\nx = row['verdict']\n"))])

    # ── F-DET
    if sel("f-det"):
        with tempfile.TemporaryDirectory() as td:
            d1, d2 = Path(td) / "a", Path(td) / "b"
            crash = _subprocess_build(d1) + _subprocess_build(d2)
            if crash:
                j1 = j2 = jbytes
                m1 = m2 = mbytes
            else:
                j1, j2 = (d1 / OUT_JSON).read_bytes(), (d2 / OUT_JSON).read_bytes()
                m1, m2 = (d1 / OUT_MD).read_bytes(), (d2 / OUT_MD).read_bytes()
        real = crash + check_det(j1, j2, m1, m2) + check_det(jbytes, j1, mbytes, m1)
        S.say(f"  run-a JSON sha256 {sha256_bytes(j1)} · run-b {sha256_bytes(j2)} · canonical "
              f"{sha256_bytes(jbytes)} · unmasked identical: {j1 == j2 == jbytes}")
        S.say(f"  run-a MD   sha256 {sha256_bytes(m1)} · run-b {sha256_bytes(m2)} · canonical "
              f"{sha256_bytes(mbytes)} · unmasked identical: {m1 == m2 == mbytes}")
        dj = json.loads(j2)
        dj["findings"][0]["text"] += "x"
        sab_j = check_det(j1, json.dumps(dj, indent=1, ensure_ascii=False).encode(), m1, m2)
        mb2 = m2.replace(b"REPORTED, NOT FIXED", b"REPORTED, NOT FIXEd", 1)
        sab_m = check_det(j1, j2, m1, mb2)
        dv = json.loads(j2)
        dv["git"]["head_at_build"] = "0" * 40
        dv["measured"]["iv"]["value"]["git_head"] = "0" * 40
        next(f for f in dv["findings"] if f["id"] == "FN-M-v")["text"] = "PLANTED volatile text"
        ctl = check_det(j1, json.dumps(dv, indent=1, ensure_ascii=False).encode(), m1, m2)
        dn = json.loads(j2)
        next(f for f in dn["findings"] if f["id"] == "FN-M-iii")["text"] += " PLANTED"
        sab_n = check_det(j1, json.dumps(dn, indent=1, ensure_ascii=False).encode(), m1, m2)
        S.leg("F-DET",
              "two cross-process builds, and the canonical on-disk build, are not byte-identical "
              "once the NAMED git-volatile fields are masked, or the mask is wider than named",
              real, [("a non-volatile JSON byte bent (findings[0].text)", sab_j),
                     ("a non-volatile Markdown byte bent", sab_m),
                     ("a field NEXT TO the volatile ones bent (FN-M-iii text)", sab_n)],
              controls=[("only named git-volatile fields bent", ctl)])

    # ── F-FN-READONLY (last: it closes over the whole run)
    if sel("f-fn-readonly"):
        after = input_manifest(ROOT)
        real = check_readonly(before, after)
        with tempfile.TemporaryDirectory() as td:
            troot = Path(td)
            _copy_inputs(troot)
            b0 = {k: v for k, v in input_manifest(troot).items()}
            _ = build(troot)                         # the build, run against the COPY
            b1 = input_manifest(troot)
            copy_ctl = check_readonly(b0, b1)
            victim = troot / PROGRESS
            with open(victim, "ab") as fh:
                fh.write(b" ")
            sab = check_readonly(b0, input_manifest(troot))
        S.leg("F-FN-READONLY",
              "any input's bytes change between the start and the end of the run, or the build run "
              "against a COPY of the inputs leaves the copy changed",
              real, [("one byte appended to a COPY of PROGRESS.json", sab)],
              controls=[("the build run against the input COPY leaves it byte-identical", copy_ctl)])

    S.say("=" * 78)
    n_ok = sum(ok for _, ok in S.results)
    S.say(f"SUMMARY: {n_ok}/{len(S.results)} legs PASS · "
          + " · ".join(f"{n} {'PASS' if ok else 'FAIL'}" for n, ok in S.results))
    rc = 0 if S.results and all(ok for _, ok in S.results) else 1
    S.say(f"EXIT {rc}")
    if not want:
        (outdir / TRANSCRIPT).write_bytes(("\n".join(S.lines) + "\n").encode("utf-8"))
        print(f"[stdout only] transcript written: {OUT_DIR_REL}/{TRANSCRIPT} sha256 "
              f"{sha256_file(outdir / TRANSCRIPT)}", flush=True)
    else:
        print("[stdout only] a filtered run writes no transcript", flush=True)
    return rc


def main(argv: list[str]) -> int:
    if len(argv) >= 2 and argv[0] == "--build-into":
        try:
            preamble()
        except SystemExit as e:
            print(str(e), flush=True)
            return 1
        doc, md = build(ROOT)
        write_outputs(doc, md, Path(argv[1]))
        return 0
    want = [a.lower() for a in argv]
    return run_suite(want)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
