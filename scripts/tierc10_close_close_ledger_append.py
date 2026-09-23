#!/usr/bin/env python
"""TIER-C10 · CLOSE · THE LEDGER_APOLLO APPEND — DRAFTED HERE, NEVER APPENDED HERE.

The contract of record, exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md, commits
the CLOSE step to one append to exchange/status/LEDGER_APOLLO.md: the Q6 hold
verbatim, m = 6, the 2026-07-29 RS rulings cited, the slippage-twin question
named for the autopsy, and CENSUS-3 next.  This module DRAFTS that append under
research_outputs/tierc10/close/ and never touches exchange/ (LAW 5: a draft
under exchange/ is not a draft).  The CLOSE step appends it after the
operator's word.

WHAT IT READS FIRST
  close/S0_VERDICTS.json — the §0 of record, built FIRST by its own builder
  (scripts/tierc10_close_close_s0_verdicts.py).  This module never writes it.
  It HALTS if the file is absent, and HALTS if any of its six rows disagrees
  with an INDEPENDENT in-memory derivation from scores/FAMILY.json and
  scores/<REG>.rows.json (verdict or HALT text, arm, n, point, CI, p, the BH
  column, the LOAO line, the prior).  A ledger is not drafted over a disputed §0.

WHAT IT WRITES (under research_outputs/tierc10/close/, nothing else)
  LEDGER_APOLLO_APPEND.draft.md     the append block between two marker lines,
                                    FORMAT mirroring the last '=== STATUS_APOLLO
                                    ... ===' / '=== END ===' block of the ledger.
  FIXTURES_CLOSE_ledger_append.txt  the F-LA transcript (deterministic: no clock,
                                    no write-status, nothing that varies by run).

HOW EVERY STATEMENT IS SOURCED
  A number is read from a file this run, never typed.  A quote is LOCATED by
  pattern search at draft time (grep-equivalent) and rendered as a cite line
  «path:L1[-L2]» or «path#field.selector» followed by the verbatim text, one
  source line per '|' line; a long source line wraps onto '+' lines (rejoined
  with ONE space, which is exact because the wrap splits only on single
  spaces).  The F-LA legs re-parse the rendered draft and re-verify every quote
  against its source bytes, and every number against a FRESH read of its file.

WHAT THIS FILE NEVER DOES
  It never scores (no TP.score / TP.finish_family / TP.register), never
  consults a verdict to choose anything (the verdicts are COPIED into the
  record), never re-words or adds a registration, never refits a pin, never
  acts on SAIL, reads NO bars (no loader is imported; bars would come only
  through tierc10_data.load_asof), never writes under exchange/, never writes a
  sibling builder's output, never touches ~/.cache/naiad/data_cache, never
  commits and never publishes.

FIXTURE LEGS (each states FAILS IF and carries sabotages that must go RED)
  F-LA-Q6 · F-LA-M · F-LA-RS · F-LA-TWIN · F-LA-NOWRITE · F-DET ·
  F-LA-S0 · F-LA-TIER · F-LA-CITE · F-LA-FORMAT · F-LA-CLOSURE

Run:
  export NAIAD_CACHE_DIR=/Users/luis/.cache/naiad/snapshots/tc10_20260921 \\
         PYTHONDONTWRITEBYTECODE=1
  ~/venvs/naiad/bin/python scripts/tierc10_close_close_ledger_append.py

HALTS (SystemExit, nothing written): NAIAD_CACHE_DIR unset, live, or not the
TC10 snapshot; PYTHONDONTWRITEBYTECODE != 1; close/S0_VERDICTS.json absent or
disagreeing with FAMILY.json; the contract's sha is not PROGRESS.json's
contract_of_record; a rows file's sha is not the one FAMILY.json finished
over; a FAMILY row differs from its rows.json score_row outside the FDR
columns; any located quote matches zero or several times; an output path
outside research_outputs/tierc10/close/.  Exit 0 = every leg GREEN; 1 otherwise.
"""
from __future__ import annotations

import ast
import copy
import hashlib
import io
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "research_outputs" / "tierc10"
CLOSE = OUT / "close"
SCORES = OUT / "scores"
CONTRACT = ROOT / "exchange" / "queue" / "2026-09-22_TC10_RESUME_APOLLO.md"
LEDGER_APOLLO = ROOT / "exchange" / "status" / "LEDGER_APOLLO.md"
LEDGER_MD = ROOT / "LEDGER.md"
FAMILY = SCORES / "FAMILY.json"
PROGRESS = OUT / "PROGRESS.json"
FEE = OUT / "data" / "fee_schedule.json"
REG_TEXTS = OUT / "REGISTRATION_TEXTS.json"          # the texts of record (READ)
S0_PATH = CLOSE / "S0_VERDICTS.json"                 # READ (a sibling's output)
V6_TWIN = CLOSE / "V6_CONTROL_HAIRCUT_TWIN.parquet"  # READ if present
DRAFT_PATH = CLOSE / "LEDGER_APOLLO_APPEND.draft.md"
TRANSCRIPT_PATH = CLOSE / "FIXTURES_CLOSE_ledger_append.txt"
EXCHANGE = ROOT / "exchange"

SNAPSHOT = Path("/Users/luis/.cache/naiad/snapshots/tc10_20260921")
LIVE_CACHE = Path.home() / ".cache" / "naiad" / "data_cache"

# The question is the AUDITOR's wording, carried as commissioned; it is NAMED
# in the draft and NOT answered.
QUESTION = ("does the charter tier model replace the TC-series flat toll for "
            "SAIL, and must the twin carry funding?")

BEGIN = "~~~~~~~~ BEGIN APPEND — the bytes from the next line up to END APPEND ~~~~~~~~"
END = "~~~~~~~~ END APPEND ~~~~~~~~"
QUOTE_WIDTH = 78
FDR_KEYS = frozenset({"clears_bh_bar", "fdr_bar_q_over_m", "fdr_m_declared",
                      "fdr_m_tests_actually_run", "fdr_note"})
V6_COLS = ("era", "key", "n", "tc_expectancy_r", "twin_expectancy_r",
           "companion_expectancy_r", "sign_disagrees", "companion_sign_disagrees")


def halt(msg: str):
    raise SystemExit(f"HALT: {msg}")


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def rel(p: Path) -> str:
    return str(Path(p).resolve().relative_to(ROOT))


def f6(x) -> str:
    return f"{float(x):+.6f}"


def p6(x) -> str:
    return f"{float(x):.6f}"


def jb(x) -> str:
    """A boolean as JSON spells it (the form close/S0_VERDICTS.json carries)."""
    return json.dumps(x)


def rows_path(reg: str) -> Path:
    return SCORES / f"{reg}.rows.json"


# ═══════════════════════════════════════════════════════════ THE PREAMBLE
def preamble() -> dict:
    """RUN only on the frozen snapshot; HALT otherwise.  No bar is read by this
    module, but the lineage's guard runs first all the same (TP.substrate)."""
    if os.environ.get("PYTHONDONTWRITEBYTECODE") != "1":
        halt("PYTHONDONTWRITEBYTECODE is not 1 — export it BEFORE python "
             "starts (the TC10 run law).")
    env = os.environ.get("NAIAD_CACHE_DIR")
    if not env:
        halt("NAIAD_CACHE_DIR is not set. TIER-C10 reads the FROZEN snapshot "
             "only; export it BEFORE python starts.")
    root = Path(env).expanduser().resolve()
    if root == LIVE_CACHE.resolve():
        halt(f"NAIAD_CACHE_DIR points at the LIVE cache {root} — read-never, "
             f"write-never for TIER-C10 [LAW 3].")
    if root != SNAPSHOT.resolve():
        halt(f"NAIAD_CACHE_DIR is {root}, not the TC10 snapshot {SNAPSHOT}.")
    for p in (ROOT, ROOT / "scripts"):
        if str(p) not in sys.path:
            sys.path.insert(0, str(p))
    import tierc10_panel as TP                                  # noqa: E402
    return TP.substrate()


# ═══════════════════════════════════════════════════════════ READING
def read_sources() -> dict:
    """Every file the draft reads, read ONCE, as bytes, keyed by repo-relative
    path.  All quoting and all numbers come out of these bytes."""
    if not S0_PATH.exists():
        halt(f"{rel(S0_PATH)} is absent — §0 is built FIRST, by "
             f"scripts/tierc10_close_close_s0_verdicts.py; this drafter reads "
             f"it and never builds it.")
    S = {}
    for p in (CONTRACT, LEDGER_APOLLO, LEDGER_MD, FAMILY, PROGRESS, FEE, REG_TEXTS,
              S0_PATH):
        S[rel(p)] = p.read_bytes()
    fam = json.loads(S[rel(FAMILY)])
    for reg in fam["rows_files_sha256"]:
        S[rel(rows_path(reg))] = rows_path(reg).read_bytes()
    if V6_TWIN.exists():
        S[rel(V6_TWIN)] = V6_TWIN.read_bytes()
    return S


def locate(text: str, pattern: str, what: str, *, start: int = 0,
           end: int | None = None, group: int = 0) -> dict:
    """The ONE match of `pattern` in text[start:end], with 1-based line numbers
    of the whole file.  HALTS on zero or several matches."""
    hi = len(text) if end is None else end
    ms = [m for m in re.finditer(pattern, text, re.MULTILINE)
          if m.start(group) >= start and m.end(group) <= hi]
    if len(ms) != 1:
        halt(f"{what}: pattern {pattern!r} matched {len(ms)} times "
             f"(exactly one is required).")
    m = ms[0]
    s, e = m.start(group), m.end(group)
    t = text[s:e]
    if not t or t.endswith("\n"):
        halt(f"{what}: a located quote may not be empty or end in a newline.")
    return {"text": t, "l1": text.count("\n", 0, s) + 1,
            "l2": text.count("\n", 0, e) + 1, "start": s, "end": e}


def locate_str(value: str, pattern: str, what: str) -> str:
    ms = list(re.finditer(pattern, value))
    if len(ms) != 1:
        halt(f"{what}: pattern {pattern!r} matched {len(ms)} times in the "
             f"field (exactly one is required).")
    return ms[0].group(0)


SEL_RE = re.compile(r"\.([^.\[\]]+)|\[(\d+)\]|\[([^=\]]+)=([^\]]+)\]")


def resolve(obj, sel: str):
    """A tiny selector: .key · [N] · [key=value] (the one dict in a list whose
    key equals value)."""
    s = sel if sel.startswith((".", "[")) else "." + sel
    pos, cur = 0, obj
    while pos < len(s):
        m = SEL_RE.match(s, pos)
        if not m:
            raise KeyError(f"bad selector {sel!r} at {pos}")
        if m.group(1) is not None:
            cur = cur[m.group(1)]
        elif m.group(2) is not None:
            cur = cur[int(m.group(2))]
        else:
            k, v = m.group(3), m.group(4)
            hits = [x for x in cur if isinstance(x, dict) and str(x.get(k)) == v]
            if len(hits) != 1:
                raise KeyError(f"selector [{k}={v}] hit {len(hits)}")
            cur = hits[0]
        pos = m.end()
    return cur


def qline(path: Path, loc: dict) -> dict:
    return {"path": rel(path), "l1": loc["l1"], "l2": loc["l2"],
            "sel": None, "text": loc["text"]}


def qjson(path: Path, sel: str, text: str) -> dict:
    return {"path": rel(path), "l1": None, "l2": None, "sel": sel,
            "text": text}


# ═══════════════════════════════════════════════════════════ THE SIX
def derive_six(S: dict) -> dict:
    """THE INDEPENDENT DERIVATION the §0 of record is held against — in memory,
    never written.  Each field is FAMILY.json's; each FAMILY row is held
    against its rows.json score_row outside the FDR columns; the rows files are
    the ones FAMILY.json finished over."""
    fam = json.loads(S[rel(FAMILY)])
    regs = list(fam["rows_files_sha256"])
    rows = {}
    for reg in regs:
        b = S[rel(rows_path(reg))]
        if sha(b) != fam["rows_files_sha256"][reg]:
            halt(f"{rel(rows_path(reg))} sha {sha(b)[:12]}… is not the one "
                 f"FAMILY.json finished over "
                 f"({fam['rows_files_sha256'][reg][:12]}…).")
        rows[reg] = json.loads(b)
    order = sorted(regs, key=lambda r: rows[r]["seq"])
    halted = fam.get("scored_slots_halted") or {}
    as_ofs = {rows[r]["as_of_last_closed_4h"] for r in regs}
    if len(as_ofs) != 1:
        halt(f"the six rows files carry {len(as_ofs)} as-ofs: {sorted(as_ofs)}")
    six = []
    for reg in order:
        frows = [r for r in fam["rows"] if r["registration"] == reg]
        srows = [r["score_row"] for r in rows[reg]["rows"] if "score_row" in r]
        if len(frows) != len(srows):
            halt(f"{reg}: FAMILY holds {len(frows)} rows, rows.json "
                 f"{len(srows)} score_rows.")
        for a, b in zip(srows, frows):
            bad = sorted(k for k in set(a) | set(b)
                         if k not in FDR_KEYS and a.get(k) != b.get(k))
            if bad:
                halt(f"{reg} arm {b.get('arm')!r}: FAMILY row differs from its "
                     f"rows.json score_row on {bad}.")
        priors = {r["prior_pct"] for r in frows}
        if len(priors) != 1:
            halt(f"{reg}: prior_pct is not one value: {sorted(priors)}")
        prior = priors.pop()
        scored = [r for r in frows if r["scored_in_family"]]
        if reg in halted:
            hr = [(i, r) for i, r in enumerate(rows[reg]["rows"])
                  if r.get("scored_in_family") and "halt" in r]
            if scored or len(hr) != 1 or hr[0][1]["halt"] != halted[reg]:
                halt(f"{reg}: the HALTed slot does not read back as ONE "
                     f"halted scored arm carrying FAMILY's HALT text.")
            i, h = hr[0]
            six.append({"registration": reg, "prior_pct": prior,
                        "slot": "HALTED", "verdict": None, "arm": h["arm"],
                        "rows_index": i, "halted_at": h["at"], "halt": h["halt"],
                        "text_prescribes": h["text_prescribes"]})
            continue
        if len(scored) != 1:
            halt(f"{reg}: {len(scored)} scored rows (one is required).")
        s = scored[0]
        six.append({
            "registration": reg, "prior_pct": prior, "slot": "SCORED",
            "arm": s["arm"], "panel_name": s["panel_name"],
            "n_panel_assets": s["n_panel_assets"], "arm_era": s["arm_era"],
            "arm_base": s["arm_base"], "ruler": s["ruler"], "n": s["n"],
            "ci_point": s["ci_point"], "ci_lo": s["ci_lo"], "ci_hi": s["ci_hi"],
            "p_one_sided": s["p_one_sided"], "verdict": s["verdict"],
            "clears_bh_bar": s["clears_bh_bar"],
            "fdr_bar_q_over_m": s["fdr_bar_q_over_m"],
            "loao_line": s["loao_line"],
            "loao_above_of_record": s["loao_above_of_record"],
            "loao_bar_above_half": s["loao_bar_above_half"],
            "loao_clears_line_of_record": s["loao_clears_line_of_record"],
            "clears_all_three": bool(s["verdict"] == "SUPPORTED"
                                     and s["loao_clears_line_of_record"] is True
                                     and s["clears_bh_bar"] is True),
        })
    return {"fam": fam, "rows": rows, "order": order, "six": six,
            "as_of": as_ofs.pop()}


def read_s0(b: bytes) -> dict:
    """close/S0_VERDICTS.json's six verdict rows as {reg: {col: s}} in its own
    order_of_filing.  Its cells are strings at source precision."""
    d = json.loads(b)
    out = {}
    for ln in d["lines"]:
        if ln.get("kind") != "verdict_row":
            continue
        cols = {p["col"]: p["s"] for p in ln["parts"]
                if p.get("t") == "val" and p.get("col")}
        out[ln["reg"]] = cols
    return {"order": list(d["order_of_filing"]), "rows": out,
            "builder": d.get("builder"), "fragment": d.get("fragment")}


S0_FIELDS = ("arm", "n", "ci_point", "ci_lo", "ci_hi", "p_one_sided", "verdict",
             "clears_bh_bar", "loao_line", "prior_pct")


def s0_expect(v: dict) -> dict:
    """The derivation, in the §0 file's string forms, for comparison."""
    if v["slot"] == "HALTED":
        return {"arm": v["arm"], "halt": v["halt"], "prior_pct": str(v["prior_pct"])}
    return {"arm": v["arm"], "n": str(v["n"]), "ci_point": f6(v["ci_point"]),
            "ci_lo": f6(v["ci_lo"]), "ci_hi": f6(v["ci_hi"]),
            "p_one_sided": p6(v["p_one_sided"]), "verdict": v["verdict"],
            "clears_bh_bar": jb(v["clears_bh_bar"]), "loao_line": v["loao_line"],
            "prior_pct": str(v["prior_pct"])}


def s0_got(cols: dict) -> dict:
    if "halt" in cols:
        return {"arm": cols.get("arm"), "halt": cols.get("halt"),
                "prior_pct": cols.get("prior_pct"),
                **({"verdict": cols["verdict"]} if "verdict" in cols else {})}
    g = {}
    for k in S0_FIELDS:
        if k not in cols:
            g[k] = None
        elif k in ("ci_point", "ci_lo", "ci_hi"):
            g[k] = f6(cols[k])
        elif k == "p_one_sided":
            g[k] = p6(cols[k])
        else:
            g[k] = cols[k]
    return g


def s0_disagreements(s0: dict, derived: dict) -> list:
    exp = {v["registration"]: s0_expect(v) for v in derived["six"]}
    got = {r: s0_got(c) for r, c in s0["rows"].items()}
    bad = [f"{r}: §0 {got.get(r)} != derived {exp.get(r)}"
           for r in sorted(set(exp) | set(got)) if exp.get(r) != got.get(r)]
    if s0["order"] != derived["order"]:
        bad.append(f"order_of_filing {s0['order']} != seq order {derived['order']}")
    return bad


# ═══════════════════════════════════════════════════════════ THE CONTEXT
def twin_records(rows: dict, order: list) -> tuple:
    recs, without, n_arm_rows = [], [], 0
    for reg in order:
        for i, r in enumerate(rows[reg]["rows"]):
            n_arm_rows += 1
            ht = (r.get("beside") or {}).get("haircut_twin")
            if ht is None:
                without.append((reg, i, "HALTed" if "halt" in r else "no twin"))
                continue
            rec = {"reg": reg, "idx": i, "arm": r["arm"],
                   "fam": bool(r.get("scored_in_family")), "n": ht["n"],
                   "tc": ht["tc_expectancy_r"], "twin": ht["twin_expectancy_r"],
                   "comp": ht["twin_with_funding_companion_expectancy_r"],
                   "flag": ht["sign_disagrees_with_tc"],
                   "cflag": ht["companion_sign_disagrees_with_tc"],
                   "note": ht["funding_note"], "law": ht["law"], "diff": None}
            if "tc_difference_r" in ht:
                rec["diff"] = (ht["base_n"], ht["tc_difference_r"],
                               ht["twin_difference_r"],
                               ht["twin_with_funding_companion_difference_r"])
            recs.append(rec)
    return recs, without, n_arm_rows


def v6_rows(b: bytes):
    """close/V6_CONTROL_HAIRCUT_TWIN.parquet as a list of dicts over V6_COLS, or
    a string naming what its schema lacks."""
    import pyarrow.parquet as pqt                                  # noqa: E402
    t = pqt.read_table(io.BytesIO(b))
    miss = [c for c in V6_COLS if c not in t.column_names]
    if miss:
        return f"schema lacks {miss}"
    cols = {c: t.column(c).to_pylist() for c in V6_COLS}
    return [{c: cols[c][i] for c in V6_COLS} for i in range(t.num_rows)]


def v6_counts(rs: list) -> dict:
    up = [r for r in rs if r["twin_expectancy_r"] > r["tc_expectancy_r"]]
    return {"n": len(rs),
            "flag": sum(bool(r["sign_disagrees"]) for r in rs),
            "cflag": sum(bool(r["companion_sign_disagrees"]) for r in rs),
            "up": len(up),
            "up_c": sum(1 for r in up
                        if r["companion_expectancy_r"] <= r["tc_expectancy_r"])}


def collect(S: dict) -> dict:
    D = derive_six(S)
    s0 = read_s0(S[rel(S0_PATH)])
    bad = s0_disagreements(s0, D)
    if bad:
        halt(f"{rel(S0_PATH)} DISAGREES with FAMILY.json/rows.json — no ledger "
             f"is drafted over a disputed §0: {bad[:3]}")
    X = {"D": D, "s0": s0, "fam": D["fam"], "rows": D["rows"],
         "order": D["order"]}
    ctext = S[rel(CONTRACT)].decode("utf-8")
    prog = json.loads(S[rel(PROGRESS)])
    X["contract_sha"] = sha(S[rel(CONTRACT)])
    X["contract_sha_agrees"] = (
        prog["contract_of_record"]["sha256"] == X["contract_sha"]
        and prog["contract_of_record"]["path"] == rel(CONTRACT))
    if not X["contract_sha_agrees"]:
        halt(f"the contract's sha {X['contract_sha'][:12]}… is not "
             f"PROGRESS.json's contract_of_record — the contract moved.")
    X["prog"] = prog
    # ── the contract, located by search
    X["q6_hold"] = qline(CONTRACT, locate(ctext, r"Q6[^;()]*?autopsied", "Q6 hold"))
    X["q6_137"] = qline(CONTRACT, locate(ctext, r'Q6 hold verbatim \("[^"\n]*"\)',
                                         "Q6 hold verbatim"))
    X["no_sail"] = qline(CONTRACT, locate(ctext, r"no SAIL act \([^)\n]*\)",
                                          "no SAIL act"))
    X["commission"] = qline(CONTRACT, locate(
        ctext, r"LEDGER_APOLLO append:[\s\S]*?CENSUS-3 next\.", "the commission"))
    X["census3"] = qline(CONTRACT, locate(ctext, r"CENSUS-3 next\.", "CENSUS-3 next"))
    X["fdr_m"] = qline(CONTRACT, locate(ctext, r"FDR m=\d+, independently failable",
                                        "FDR m"))
    X["prenamed"] = qline(CONTRACT, locate(
        ctext, r"P-TRG-2 \[\d+%\][^\n]*?pre-naming\.", "the one pre-naming"))
    X["costs"] = qline(CONTRACT, locate(
        ctext, r"COSTS: every row[\s\S]*?ADDED\s+column\.", "COSTS clause"))
    X["c_qr5"] = qline(CONTRACT, locate(
        ctext, r"\[Q-R5\] grep-attest[\s\S]*?\(2026-07-29 ruling\)\.", "[Q-R5]"))
    X["c_qr4"] = qline(CONTRACT, locate(
        ctext, r"\[Q-R4\] the four acceptance[\s\S]*?nothing promoted", "[Q-R4]"))
    X["c_qr3"] = qline(CONTRACT, locate(
        ctext, r"\[Q-R3\] HEIGHT-vs-TOLL[\s\S]*?stays Tier-E", "[Q-R3]"))
    t1 = locate(ctext, r"\ATIER-C\d+ · [A-Z-]+ —", "contract title")
    m1 = re.match(r"(TIER-C\d+) · ([A-Z-]+) —", t1["text"])
    X["tier"], X["mode"] = m1.group(1), m1.group(2)
    bd = locate(ctext, r"BUILD_\d{4}-\d{2}-\d{2}_TIERC\d+_[A-Z_]+\.md", "build doc")
    X["build_title"] = re.match(r"BUILD_\d{4}-\d{2}-\d{2}_TIERC\d+_([A-Z_]+)\.md",
                                bd["text"]).group(1).replace("_", " ")
    roles = locate(ctext, r"Drafted: \w+\. Executor:\s*\w+\.", "roles")
    mr = re.match(r"Drafted: (\w+)\. Executor:\s*(\w+)\.", roles["text"])
    X["drafted_by"], X["executor"] = mr.group(1), mr.group(2)
    X["date"] = re.match(r"(\d{4}-\d{2}-\d{2})_", CONTRACT.name).group(1)
    # ── LEDGER.md: the 07-29 RS rulings, located by search
    ltext = S[rel(LEDGER_MD)].decode("utf-8")
    head = locate(ltext, r"^## 2026-07-29 — Range-and-Structure layer[^\n]*$",
                  "RS heading")
    nxt = ltext.find("\n## ", head["end"])
    sec_end = len(ltext) if nxt < 0 else nxt
    X["rs_head"] = qline(LEDGER_MD, head)
    for k in ("3", "4", "5"):
        loc = locate(ltext, rf"^  - (Q-R{k} [^\n]*)$", f"Q-R{k}",
                     start=head["start"], end=sec_end, group=1)
        if k == "5":                     # the first two sentences only
            t = loc["text"]
            cut = [m.end() for m in re.finditer(r"\. ", t)]
            if len(cut) < 2:
                halt("Q-R5: fewer than two sentences.")
            loc = dict(loc, text=t[:cut[1] - 1])
        X[f"rs_qr{k}"] = qline(LEDGER_MD, loc)
    X["rs_ratified"] = qline(LEDGER_MD, locate(
        ltext, r"^- Reviewer: [^\n]*2026-07-29\. Operator: ratified\.$",
        "RS ratification", start=head["start"], end=sec_end))
    # ── LEDGER_APOLLO.md: the last tier block, its separator, TC9's words
    atext = S[rel(LEDGER_APOLLO)].decode("utf-8")
    starts = [m.start() for m in re.finditer(r"^=== STATUS_APOLLO — [^\n]* ===$",
                                             atext, re.MULTILINE)]
    if len(starts) < 2:
        halt("LEDGER_APOLLO.md holds fewer than two tier blocks.")
    last = starts[-1]
    prev_end = atext.rfind("=== END ===", 0, last)
    if prev_end < 0 or not atext.endswith("=== END ===\n"):
        halt("LEDGER_APOLLO.md does not end on a '=== END ===' line.")
    sep = atext[prev_end + len("=== END ==="):last]
    X["sep"] = sep[1:]                   # the file already ends in '\n'
    X["last_header"] = qline(LEDGER_APOLLO, locate(
        atext, r"^=== STATUS_APOLLO — [^\n]* ===$", "last header", start=last))
    X["tc9_close"] = qline(LEDGER_APOLLO, locate(
        atext, r"[A-Z]+ TIERS IN-SAMPLE; NOTHING HAS CLEARED ITS OWN BAR\.",
        "TC9's close", start=last))
    X["tc9_trg"] = qline(LEDGER_APOLLO, locate(
        atext, r"trigger-9/12[\s\S]*?this one did not\.", "TC9's trigger cell",
        start=last))

    # ── PROGRESS.json record lines
    def pst(stage):
        return resolve(prog, f"stages[stage={stage}]")

    def pfield(stage, field, pattern, what):
        v = resolve(prog, f"stages[stage={stage}].{field}")
        return qjson(PROGRESS, f"stages[stage={stage}].{field}",
                     locate_str(v, pattern, what))

    def pnote(stage, pattern, what):
        notes = pst(stage)["notes"]
        hits = [i for i, n in enumerate(notes) if re.search(pattern, n)]
        if len(hits) != 1:
            halt(f"{what}: {len(hits)} notes match.")
        i = hits[0]
        return qjson(PROGRESS, f"stages[stage={stage}].notes[{i}]",
                     locate_str(notes[i], pattern, what))

    X["p_qr5"] = pfield("STEP 0", "one_line", r"Q-R5 attestation [^;]*", "STEP 0 Q-R5")
    X["p_built"] = pfield("CENSUS-R{4h,1d}", "one_line",
                          r"\[Q-R3\] height-vs-toll and \[Q-R4\] the acceptance "
                          r"head-to-head are BUILT", "Q-R3/Q-R4 BUILT")
    X["p_gate"] = pfield("CENSUS-R{4h,1d}", "one_line",
                         r"\[Q-R3\] is a GATE per LEDGER\.md:\d+, not a table: [^.]*\.",
                         "Q-R3 gate")
    X["p_gate5m"] = pfield("CENSUS-R{5m}", "one_line",
                           r"The 5m height-vs-toll gate [^\n]*?row\)\.", "5m gate")
    X["p_mstays"] = pnote("B-5M", r"m stays \d+ DECLARED \(\d+ run\): [^.]*\.",
                          "m stays")
    X["p_operator"] = pnote("B-CORE", r"adding a registration is outside the "
                            r"contract[\s\S]*?OPERATOR's to order\.",
                            "the set_change filing")
    X["p_dcore"] = pfield("D-CORE", "one_line", r"PARTIAL because [^.]*\.",
                          "D-CORE partial")
    X["p_d5m"] = pfield("D-5M", "one_line", r"PARTIAL only on [^.]*\.", "D-5M partial")
    X["p_statuses"] = {st: pst(st)["status"] for st in ("D-CORE", "D-5M")}
    X["as_of_of_record"] = prog["as_of_of_record"]
    X["branch"], X["seed"] = prog["branch"], prog["seed"]
    # ── what a clearing registration's OWN filed text says about its sample
    texts = json.loads(S[rel(REG_TEXTS)])
    X["insample"] = {}
    for v in D["six"]:
        if not v.get("clears_all_three"):
            continue
        t = texts[v["registration"]]["text"]
        ms = list(re.finditer(r"\(b\) THE SAMPLE IS[\s\S]*?IN-SAMPLE RE-SCORE[^.]*\.", t))
        if len(ms) == 1:
            X["insample"][v["registration"]] = qjson(
                REG_TEXTS, f"{v['registration']}.text", ms[0].group(0))
    # ── the family, the halted slot, the twin
    fam, rows, regs = D["fam"], D["rows"], D["order"]
    X["halted_q"] = {r: qjson(FAMILY, f"scored_slots_halted.{r}", t)
                     for r, t in (fam.get("scored_slots_halted") or {}).items()}
    X["twin"], X["twin_without"], X["n_arm_rows"] = twin_records(rows, regs)
    X["v6"] = None
    if rel(V6_TWIN) in S:
        X["v6"] = {"sha": sha(S[rel(V6_TWIN)]), "rows": v6_rows(S[rel(V6_TWIN)])}
    fee = json.loads(S[rel(FEE)])
    X["fee"] = fee
    X["fee_law"] = qjson(FEE, "haircut_twin_law", locate_str(
        fee["haircut_twin_law"], r"ADDED, never a replacement:[^\]]*\]\.",
        "twin law"))
    X["fee_formula"] = qjson(FEE, "haircut_twin_law", locate_str(
        fee["haircut_twin_law"], r"net_r_twin = [^()\n;]*?risk_px", "twin formula"))
    # ── BRK rows: the Q-R3 gate as carried on each form's row
    X["brk"] = []
    for reg in regs:
        br = (rows[reg].get("beside_registration") or {}).get("brk_sealed_row")
        if not br:
            continue
        base = "beside_registration.brk_sealed_row"
        hv = br["height_vs_toll"]
        X["brk"].append({
            "reg": reg, "lens": hv["lens"], "era": hv["era"],
            "pass": hv["verdict_pass"],
            "q_reason": qjson(rows_path(reg), f"{base}.height_vs_toll.reason",
                              hv["reason"]),
            "q_toll": qjson(rows_path(reg), f"{base}.toll_accounting_status",
                            br["toll_accounting_status"]),
        })
    return X


# ═══════════════════════════════════════════════════════════ RENDERING
def wrap_tokens(line: str, width: int) -> list:
    """Split on SINGLE spaces only, so ' '.join(chunks) == line exactly."""
    toks = line.split(" ")
    out, cur = [], None
    for t in toks:
        if cur is None:
            cur = t
        elif len(cur) + 1 + len(t) <= width:
            cur += " " + t
        else:
            out.append(cur)
            cur = t
    out.append(cur)
    return out


def cite_of(q: dict) -> str:
    if q["sel"] is not None:
        return f"«{q['path']}#{q['sel']}»"
    span = f"{q['l1']}" if q["l1"] == q["l2"] else f"{q['l1']}-{q['l2']}"
    return f"«{q['path']}:{span}»"


NO_WRAP_UP_TO = 104         # a source line this short is quoted as it stands


def render_quote(indent: int, q: dict) -> list:
    out = [" " * indent + cite_of(q)]
    pad = " " * (indent + 2)
    width = max(24, QUOTE_WIDTH - indent - 4)
    for src in q["text"].split("\n"):
        chunks = [src] if len(src) <= NO_WRAP_UP_TO else wrap_tokens(src, width)
        out.append(f"{pad}| {chunks[0]}")
        out.extend(f"{pad}+ {c}" for c in chunks[1:])
    return out


def twin_line(label: str, n, tc, tw, cp, flag, cflag, tail: str) -> str:
    cmp_ = "twin>TC" if tw > tc else "twin<=TC"
    return (f"{label}n {n:<5} TC {f6(tc)}  twin {f6(tw)}  twin+fund {f6(cp)}  "
            f"{cmp_:<8} flags {flag}/{cflag}{tail}")


def render_block(X: dict) -> str:
    D, s0, fam = X["D"], X["s0"], X["fam"]
    m = fam["family_m_declared"]
    n_sc = sum(1 for r in fam["rows"] if r["scored_in_family"])
    n_rows = len(fam["rows"])
    n_reg = len(s0["order"])
    halted = fam.get("scored_slots_halted") or {}
    six = {v["registration"]: v for v in D["six"]}
    L = []
    a = L.append
    a(f"=== STATUS_APOLLO — {X['date']} — {X['tier']} · {X['build_title']} · "
      f"{X['mode']} ===")
    a(f"LANE      {X['drafted_by']} (drafted) · {X['executor']} (executor) · "
      f"branch {X['branch']} · seed {X['seed']}")
    a(f"CLASS     {n_reg} REGISTRATIONS, TEXT FROZEN · FDR m = {m} DECLARED, "
      f"{n_sc} SCORED,")
    a(f"          {len(halted)} SLOT HALTED AS ITS FILED TEXT PRESCRIBES. As-of "
      f"{X['as_of_of_record']}.")
    a(f"          Contract of record {rel(CONTRACT)}")
    a(f"          (sha {X['contract_sha'][:16]}…, = PROGRESS.json "
      f"contract_of_record: {X['contract_sha_agrees']}).")
    a("          Every quote below is verbatim and cited «path:line» or "
      "«path#field»;")
    a("          every number is read from the file named beside it.")
    a("")
    # ── Q6
    a("  Q6 · THE SAIL SPEC HOLD, VERBATIM — BOTH PLACES THE CONTRACT STATES IT,")
    a("  AND THE LIMIT IT SETS ON THIS TIER:")
    for k in ("q6_hold", "q6_137", "no_sail"):
        L.extend(render_quote(4, X[k]))
    a("    The hold is quoted, not lifted. Nothing in this tier acts on SAIL;")
    a("    a registration clearing its bar below is a verdict, not a SAIL act.")
    a("")
    # ── the verdicts, from the §0 of record
    a(f"  §0 · THE {n_reg} — READ, NOT RE-SCORED: the scored row of record per")
    a(f"  registration, from {rel(S0_PATH)}")
    a(f"  (built first by {s0['builder']}), every cell held")
    a("  against an independent read of scores/FAMILY.json + scores/<REG>.rows.json:")
    for reg in s0["order"]:
        c = s0["rows"][reg]
        if "halt" in c:
            v = six[reg]
            a(f"    {reg:<9} [{c['prior_pct']}%]  HALT — NO VERDICT")
            a(f"        '{c['arm']}' · halted at {v['halted_at']};")
            a("        the slot finishes WITHOUT a row:")
            L.extend(render_quote(8, X["halted_q"][reg]))
            a("        and what the filed text prescribes for this HALT:")
            for j, tp in enumerate(v["text_prescribes"]):
                L.extend(render_quote(8, qjson(
                    rows_path(reg),
                    f"rows[{v['rows_index']}].text_prescribes[{j}]", tp)))
            continue
        tail = " · CI ENTIRELY BELOW ZERO" if float(c["ci_hi"]) < 0 else ""
        a(f"    {reg:<9} [{c['prior_pct']}%]  {c['verdict']}{tail}")
        a(f"        '{c['arm']}' · {c['panel_name']} · era {c['arm_era']} · "
          f"n {c['n']}")
        a(f"        {c['ruler']}")
        a(f"        point {f6(c['ci_point'])} R · CI [{f6(c['ci_lo'])}, "
          f"{f6(c['ci_hi'])}] · p {p6(c['p_one_sided'])}")
        a(f"        clears_bh_bar {c['clears_bh_bar']} · LOAO {c['loao_line']} "
          f"(above of record {c['loao_above_of_record']} vs bar "
          f"{c['loao_bar_above_half']})")
    a("")
    # ── m
    a(f"  FAMILY · m = {m} DECLARED (scores/FAMILY.json family_m_declared) ·")
    a(f"    bar q/m = {fam['fdr_bar_q_over_m']!r} (fdr_bar_q_over_m) ·")
    a(f"    {n_sc} scored rows of {n_rows} family rows (scored_in_family) · "
      f"halted slots {len(halted)}: {', '.join(halted) or 'none'}.")
    a("    The contract's m, and the record's reason it does not shrink:")
    for k in ("fdr_m", "p_mstays"):
        L.extend(render_quote(4, X[k]))
    a("")
    # ── RS rulings
    a("  THE 07-29 RS RULINGS, CITED — LEDGER.md, located by pattern search at")
    a("  draft time (grep -n equivalent): the heading, the Q-R3 / Q-R4 / Q-R5")
    a("  bullets, the ratification:")
    for k in ("rs_head", "rs_qr3", "rs_qr4", "rs_qr5", "rs_ratified"):
        L.extend(render_quote(4, X[k]))
    a("    Where TIER-C10 carried them — the contract's anchor, then the record:")
    a("    [Q-R5]")
    L.extend(render_quote(6, X["c_qr5"]))
    L.extend(render_quote(6, X["p_qr5"]))
    a("    [Q-R4]")
    L.extend(render_quote(6, X["c_qr4"]))
    L.extend(render_quote(6, X["p_built"]))
    a("    [Q-R3]")
    L.extend(render_quote(6, X["c_qr3"]))
    L.extend(render_quote(6, X["p_gate"]))
    L.extend(render_quote(6, X["p_gate5m"]))
    a("      on each BRK form's row (REPORT-ONLY — the gate as carried, read):")
    for b in X["brk"]:
        a(f"      {b['reg']} · lens {b['lens']} · era {b['era']} · "
          f"verdict_pass {b['pass']}")
        L.extend(render_quote(8, b["q_reason"]))
    a("")
    # ── the slippage-twin question
    recs = X["twin"]
    nt = len(recs)
    up = [r for r in recs if r["twin"] > r["tc"]]
    up_comp = [r for r in up if r["comp"] <= r["tc"]]
    a("  THE SLIPPAGE-TWIN QUESTION — NAMED FOR THE AUTOPSY, NOT ANSWERED HERE:")
    a(f'    QUESTION: "{QUESTION}"')
    a("    The clause that put a twin on every row:")
    L.extend(render_quote(4, X["costs"]))
    a("    EVIDENCE — TIER-E · REPORT-ONLY · the twin gates nothing:")
    L.extend(render_quote(4, qjson(rows_path(recs[0]["reg"]),
                                   f"rows[{recs[0]['idx']}].beside.haircut_twin.law",
                                   recs[0]["law"])))
    L.extend(render_quote(4, X["fee_law"]))
    L.extend(render_quote(4, X["fee_formula"]))
    a("    the tiers (research_outputs/tierc10/data/fee_schedule.json "
      "haircut_twin_tiers):")
    for tier, spec in X["fee"]["haircut_twin_tiers"].items():
        a(f"      tier {tier} {{{' '.join(spec['assets'])}}} "
          f"{spec['bps_per_side']!r} bps/side")
    assets = X["fee"]["assets"]
    tc_rt = Counter(x["round_trip_bps_used"] for x in assets)
    a("    per asset (fee_schedule.json assets[]):")
    a("      TC-series toll · round_trip_bps_used · "
      + " · ".join(f"{k!r} x{c}" for k, c in sorted(tc_rt.items()))
      + f" · of {len(assets)} assets")
    by_tier = {}
    for x in assets:
        by_tier.setdefault(x["haircut_twin_tier"], Counter())[
            x["haircut_twin_round_trip_bps"]] += 1
    a("      charter twin · haircut_twin_round_trip_bps · "
      + " · ".join(f"{t} {k!r} x{c}" for t in sorted(by_tier)
                   for k, c in sorted(by_tier[t].items())))
    n_gt = sum(1 for x in assets
               if x["haircut_twin_round_trip_bps"] > x["round_trip_bps_used"])
    a(f"      twin round trip > TC toll on {n_gt}/{len(assets)} assets")
    a("    every arm row that carries a twin — expectancy R per campaign, as filed.")
    a("    IN = the registration's scored arm, -- = a Tier-E arm; twin+fund = the")
    a("    with-funding companion, which is NOT the filed twin; flags =")
    a("    sign_disagrees_with_tc / companion_sign_disagrees_with_tc:")
    for r in recs:
        a(twin_line(f"      {r['reg']:<9}#{r['idx']} {'IN' if r['fam'] else '--'}  ",
                    r["n"], r["tc"], r["twin"], r["comp"], r["flag"], r["cflag"],
                    f"  '{r['arm']}'"))
    wo = ", ".join(f"{g}#{i} ({why})" for g, i, why in X["twin_without"]) or "none"
    a(f"    COUNTS: {nt} of {X['n_arm_rows']} arm rows carry a twin "
      f"(without: {wo}) ·")
    a(f"      flags: sign_disagrees_with_tc {sum(r['flag'] for r in recs)}/{nt} · "
      f"companion_sign_disagrees_with_tc {sum(r['cflag'] for r in recs)}/{nt} ·")
    a(f"      twin > TC on {len(up)}/{nt} · of those {len(up)}, twin+fund <= TC "
      f"on {len(up_comp)}/{len(up)}")
    notes = Counter(r["note"] for r in recs)
    a(f"    the twin's funding, in the rows' own words (the same note on "
      f"{notes.most_common(1)[0][1]}/{nt} twin rows):")
    L.extend(render_quote(4, qjson(rows_path(recs[0]["reg"]),
                                   f"rows[{recs[0]['idx']}].beside.haircut_twin."
                                   f"funding_note", recs[0]["note"])))
    a("    the arms ridden against card-v6 — the Δ as filed, TC / twin / twin+fund:")
    for r in recs:
        if r["diff"] is None:
            continue
        bn, td, wd, cd = r["diff"]
        a(f"      {r['reg']:<9}#{r['idx']} {'IN' if r['fam'] else '--'}  "
          f"base_n {bn:<4} TC Δ {f6(td)}  twin Δ {f6(wd)}  twin+fund Δ {f6(cd)}  "
          f"'{r['arm']}'")
    v6 = X["v6"]
    if v6 is None:
        a(f"    {rel(V6_TWIN)}: ABSENT at draft time —")
        a("      the 5-asset control's own twin column is not read here.")
    elif isinstance(v6["rows"], str):
        a(f"    {rel(V6_TWIN)}: sha {v6['sha'][:16]}… · PRESENT, NOT READ: "
          f"{v6['rows']}")
    else:
        vr = v6["rows"]
        k = v6_counts(vr)
        a(f"    the 5-asset v6 control's own twin — {rel(V6_TWIN)}")
        a(f"      (sha {v6['sha'][:16]}…, {k['n']} rows; TIER-E · REPORT-ONLY; "
          f"key ALL per era):")
        for r in vr:
            if r["key"] != "ALL":
                continue
            a(twin_line(f"      v6 ALL · era {r['era']:<8}· ", r["n"],
                        r["tc_expectancy_r"], r["twin_expectancy_r"],
                        r["companion_expectancy_r"], r["sign_disagrees"],
                        r["companion_sign_disagrees"], ""))
        a(f"      V6 COUNTS over all {k['n']} rows: sign_disagrees "
          f"{k['flag']}/{k['n']} · companion_sign_disagrees {k['cflag']}/{k['n']} ·")
        a(f"      twin > TC on {k['up']}/{k['n']} · of those {k['up']}, twin+fund "
          f"<= TC on {k['up_c']}/{k['up']}")
    for b in X["brk"]:
        if b["lens"] == "5m":
            a(f"    beside it, the 5m toll on {b['reg']}'s row is a PRINT:")
            L.extend(render_quote(4, b["q_toll"]))
    a("    The autopsy owns the answer. Nothing here replaces the TC-series toll;")
    a("    every verdict above is the TC-series row's.")
    a("")
    # ── the tier line
    cleared = [v for v in D["six"] if v.get("clears_all_three")]
    a("  THE TIER LINE — read from scores/FAMILY.json and scores/<REG>.rows.json,")
    a("  nothing typed. TC9 closed on:")
    L.extend(render_quote(4, X["tc9_close"]))
    if not cleared:
        a(f"    {X['tier']}: 0 OF THE m = {m} DECLARED CLEARS ITS OWN BAR.")
    for v in cleared:
        reg = v["registration"]
        eras = {}
        for i, r in enumerate(X["rows"][reg]["rows"]):
            sr = r.get("score_row")
            if sr and sr["arm_base"] == v["arm_base"] and sr["arm_era"] in (
                    "tuning", "holdout"):
                eras.setdefault(sr["arm_era"], []).append((i, sr))
        tun = eras.get("tuning", [])
        tun_ok = len(tun) == 1 and tun[0][1]["verdict"] == "SUPPORTED"
        a(f"    {X['tier']}: {len(cleared)} OF THE m = {m} DECLARED CLEARS ITS "
          f"OWN BAR — {reg},")
        a("    THE ONE CELL THE CONTRACT PRE-NAMED"
          + ("." if tun_ok else "; ITS TUNING ERA ALONE DOES NOT."))
        if reg in X["insample"]:
            a("    AND ITS OWN FILED TEXT CALLS IT, IN LARGE PART, AN IN-SAMPLE "
              "RE-SCORE:")
            L.extend(render_quote(4, X["insample"][reg]))
        a(f"    {reg}'s SCORED arm '{v['arm']}' is SUPPORTED (CI-only); "
          f"LOAO and BH beside, both clear:")
        a(f"      CI (the deciding clause) verdict {v['verdict']} — CI [{f6(v['ci_lo'])}, "
          f"{f6(v['ci_hi'])}], lo > 0 {jb(v['ci_lo'] > 0)}")
        a(f"      LOAO (beside, deciding nothing) {v['loao_line']} — line of record clears "
          f"{jb(v['loao_clears_line_of_record'])}")
        a(f"      BH (beside, deciding nothing) p {p6(v['p_one_sided'])} <= bar "
          f"{p6(v['fdr_bar_q_over_m'])} — clears_bh_bar {jb(v['clears_bh_bar'])}")
        for era in ("tuning", "holdout"):
            for i, sr in eras.get(era, []):
                a(f"    Its {era.upper()}-ERA arm '{sr['arm']}' reads "
                  f"{sr['verdict']}")
                a(f"      (Δ {f6(sr['ci_point'])}, CI [{f6(sr['ci_lo'])}, "
                  f"{f6(sr['ci_hi'])}], p {p6(sr['p_one_sided'])}, "
                  f"LOAO {sr['loao_line']}) · {reg}.rows.json rows[{i}]")
        a("    It is the cell TC9's grid lit, and the contract's one pre-naming:")
        L.extend(render_quote(4, X["tc9_trg"]))
        L.extend(render_quote(4, X["prenamed"]))
        a(f"    TIER-C10 scored it on panel {v['panel_name']} "
          f"({v['n_panel_assets']} assets), as-of {D['as_of']}.")
    a("")
    # ── next
    a("  NEXT · CENSUS-3.")
    L.extend(render_quote(4, X["census3"]))
    a("    Carried to it, not ruled here:")
    a("    · the new id the HALTed slot's own words ask for is the operator's "
      "to order:")
    L.extend(render_quote(6, X["p_operator"]))
    a("    · the slippage-twin question above, and the 5m toll print-vs-deduction;")
    a(f"    · D-CORE {X['p_statuses']['D-CORE']} and D-5M "
      f"{X['p_statuses']['D-5M']} (PROGRESS.json):")
    L.extend(render_quote(6, X["p_dcore"]))
    L.extend(render_quote(6, X["p_d5m"]))
    a("")
    nf = len(fam["rows_files_sha256"])
    a("  INTEGRITY  drafted by scripts/tierc10_close_close_ledger_append.py — "
      "REPORT-ONLY:")
    a(f"    FAMILY.json rows_files_sha256 re-hash {nf}/{nf} on disk before a "
      f"field was read;")
    a(f"    §0 ({rel(S0_PATH)}) agrees cell-for-cell with that read;")
    a("    every «cite» above is re-verified against its source by the F-LA legs")
    a("    (research_outputs/tierc10/close/FIXTURES_CLOSE_ledger_append.txt);")
    a("    this block was DRAFTED, not appended — F-LA-NOWRITE holds "
      "LEDGER_APOLLO.md's")
    a("    bytes across the run. SAIL stays HELD (Q6).")
    a("=== END ===")
    return X["sep"] + "\n".join(L) + "\n"


def render_draft(S: dict, X: dict, *, salt=None) -> str:
    H = []
    h = H.append
    h(f"{X['tier']} · CLOSE · LEDGER_APOLLO APPEND — DRAFT, NOT APPENDED")
    h("drafted by scripts/tierc10_close_close_ledger_append.py · REPORT-ONLY: it "
      "reads filed")
    h("records, scores nothing, re-words nothing, and writes nothing under "
      "exchange/.")
    h("The text between the two ~~~~ marker lines is a SOURCE-QUOTE DRAFT of the")
    h("append, re-verified by the F-LA legs. It is NOT the append of record: the")
    h("CLOSE appends research_outputs/tierc10/LEDGER_APOLLO_APPEND.md, certified by")
    h("F-LAR (scripts/tierc10_close_ledger_append_root.py). Appending is the CLOSE")
    h(f"step's act (contract :{X['commission']['l1']}-"
      f"{X['commission']['l2']}, quoted in full below), after the")
    h("operator's word — not this script's. The commission, verbatim:")
    H.extend(render_quote(2, X["commission"]))
    h("")
    h("SOURCES READ THIS RUN (sha256 · bytes · path)")
    for k in sorted(S):
        h(f"  {sha(S[k])} · {len(S[k])} · {k}")
    if salt is not None:
        h(f"  salt {salt()}")
    h("")
    h(BEGIN)
    return "\n".join(H) + "\n" + render_block(X) + END + "\n"


def render_all(S: dict, *, salt=None) -> tuple:
    X = collect(S)
    return X, render_draft(S, X, salt=salt).encode()


# ═══════════════════════════════════════════════════════════ WRITING
def output_guard(paths) -> tuple:
    """Every output under research_outputs/tierc10/close/, none under exchange/,
    and none a file this module only READS (a sibling's output)."""
    bad = []
    for p in paths:
        rp = Path(p).resolve()
        if (not rp.is_relative_to(CLOSE.resolve())
                or rp.is_relative_to(EXCHANGE.resolve())
                or rp in (S0_PATH.resolve(), V6_TWIN.resolve())):
            bad.append(str(p))
    return (not bad), bad


def write_out(path: Path, b: bytes):
    ok, bad = output_guard([path])
    if not ok:
        halt(f"refusing to write {bad} — this module writes only its own "
             f"outputs under {rel(CLOSE)}/.")
    CLOSE.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b)


# ═══════════════════════════════════════════════════════════ PARSING THE DRAFT
CITE_RE = re.compile(r"^( *)«([^»#:]+)(?::(\d+)(?:-(\d+))?|#([^»]+))»$")


def extract_block(draft: str):
    i = draft.find(BEGIN + "\n")
    if i < 0:
        return None
    s = i + len(BEGIN) + 1
    k = draft.find("\n" + END + "\n", s)
    if k < 0:
        return None
    return draft[s:k + 1]


def parse_quotes(text: str) -> list:
    lines = text.split("\n")
    out, i = [], 0
    while i < len(lines):
        m = CITE_RE.match(lines[i])
        if not m:
            i += 1
            continue
        ind = len(m.group(1))
        qre = re.compile("^" + " " * (ind + 2) + r"([|+]) (.*)$")
        parts, j = [], i + 1
        while j < len(lines):
            q = qre.match(lines[j])
            if not q:
                break
            parts.append((q.group(1), q.group(2)))
            j += 1
        body = ""
        for n, (mk, t) in enumerate(parts):
            if n == 0:
                body = t
            elif mk == "|":
                body += "\n" + t
            else:
                body += " " + t
        l1 = int(m.group(3)) if m.group(3) else None
        l2 = int(m.group(4)) if m.group(4) else l1
        out.append({"path": m.group(2), "l1": l1, "l2": l2, "sel": m.group(5),
                    "text": body, "at": i + 1,
                    "shape_ok": bool(parts) and parts[0][0] == "|"})
        i = j
    return out


def verify_quote(q: dict, src: dict) -> tuple:
    b = src.get(q["path"])
    if b is None:
        return False, f"{q['path']} is not a source this run read"
    if not q["shape_ok"] or not q["text"]:
        return False, "empty or malformed quote"
    if q["sel"] is None:
        lines = b.decode("utf-8").split("\n")
        parts = q["text"].split("\n")
        l1, l2 = q["l1"], q["l2"]
        if l2 < l1 or l1 < 1 or l2 > len(lines):
            return False, f"cited lines {l1}-{l2} outside the file"
        if l2 - l1 + 1 != len(parts):
            return False, (f"cites {l2 - l1 + 1} line(s), quote spans "
                           f"{len(parts)}")
        if len(parts) == 1:
            ok = parts[0] in lines[l1 - 1]
        else:
            ok = (lines[l1 - 1].endswith(parts[0])
                  and all(lines[l1 - 1 + k] == parts[k]
                          for k in range(1, len(parts) - 1))
                  and lines[l2 - 1].startswith(parts[-1]))
        if not ok:
            return False, f"line(s) {l1}-{l2} do not hold the quoted text"
        if q["text"].encode() not in b:
            return False, "not a byte substring of the file"
        return True, "ok"
    try:
        v = resolve(json.loads(b), q["sel"])
    except Exception as e:                                   # noqa: BLE001
        return False, f"selector {q['sel']!r} does not resolve ({e})"
    if isinstance(v, str):
        return (q["text"] in v), ("ok" if q["text"] in v else
                                  "quote is not a substring of the field")
    ok = q["text"] == json.dumps(v, ensure_ascii=False)
    return ok, ("ok" if ok else f"field is {json.dumps(v)}, quote {q['text']!r}")


def check_quotes(draft: str, src: dict, *, path: str | None = None,
                 required=()) -> tuple:
    """Every «cite» in the WHOLE draft (header and block) verifies; every
    required quote is present in the block."""
    block = extract_block(draft)
    if block is None:
        return False, "the append markers are missing"
    head = draft[:draft.find(BEGIN)]
    qs = [q for q in parse_quotes(head) + parse_quotes(block)
          if path is None or q["path"] == path]
    in_block = [q for q in parse_quotes(block) if path is None or q["path"] == path]
    bad = []
    for q in qs:
        ok, why = verify_quote(q, src)
        if not ok:
            bad.append(f"line {q['at']} {cite_of(q)}: {why}")
    missing = [cite_of(r) for r in required
               if not any(q["path"] == r["path"] and q["l1"] == r["l1"]
                          and q["l2"] == r["l2"] and q["sel"] == r["sel"]
                          and q["text"] == r["text"] for q in in_block)]
    ok = bool(qs) and not bad and not missing
    det = (f"{len(qs)} quote(s) verify" if ok else
           f"{len(bad)} bad {bad[:2]} · missing {missing[:3]}"
           + ("" if qs else " · no quotes found"))
    return ok, det


# ═══════════════════════════════════════════════════════════ THE LEGS
def _split_at_block(draft: str) -> tuple:
    i = draft.find(BEGIN)
    if i < 0:
        raise AssertionError("sabotage could not be planted: no BEGIN marker")
    return draft[:i], draft[i:]


def plant(draft: str, old: str, new: str) -> str:
    """Replace the FIRST occurrence at or after the BEGIN marker (the header
    quotes the commission, which repeats the Q6 phrase — a plant there would
    miss the block).  A plant that finds nothing RAISES (a vacuous sabotage is
    a blind leg, and run_legs scores it so)."""
    head, rest = _split_at_block(draft)
    if old not in rest:
        raise AssertionError(f"sabotage could not be planted: {old[:50]!r} absent")
    return head + rest.replace(old, new, 1)


def resub(draft: str, pattern: str, repl) -> str:
    head, rest = _split_at_block(draft)
    new, n = re.subn(pattern, repl, rest, count=1)
    if n != 1:
        raise AssertionError(f"sabotage could not be planted: {pattern[:50]!r}")
    return head + new


def leg_q6(ctx):
    src, X, draft = ctx["src"], ctx["X"], ctx["draft"]
    req = (X["q6_hold"], X["q6_137"])
    c = rel(CONTRACT)

    def chk(d):
        return check_quotes(d, src, path=c, required=req)
    h, q137 = X["q6_hold"], X["q6_137"]
    sab = [
        (f"paraphrase :{q137['l1']} ('until' -> 'till')",
         lambda: chk(plant(draft, 'spec held until TC10 autopsied")',
                           'spec held till TC10 autopsied")'))),
        (f"paraphrase :{h['l1']}-{h['l2']} ('until TC10 autopsied' -> "
         f"'until TC10 is autopsied')",
         lambda: chk(plant(draft, "| until TC10 autopsied\n",
                           "| until TC10 is autopsied\n"))),
        (f"mis-cite the hold :{h['l1']}-{h['l2']} -> :{h['l1'] + 1}-{h['l2'] + 1}",
         lambda: chk(plant(draft, f"{c}:{h['l1']}-{h['l2']}»",
                           f"{c}:{h['l1'] + 1}-{h['l2'] + 1}»"))),
    ]
    ok, det = chk(draft)
    return (ok, f"{det}; the hold located at :{h['l1']}-{h['l2']} and the "
                f"phrase at :{q137['l1']} both present in the block"), sab


def check_m(draft: str, src: dict) -> tuple:
    fam = json.loads(src[rel(FAMILY)])
    block = extract_block(draft) or ""
    mm = re.search(r"FAMILY · m = (\d+) DECLARED", block)
    mb = re.search(r"bar q/m = (\S+) \(fdr_bar_q_over_m\)", block)
    mn = re.search(r"(\d+) scored rows of (\d+) family rows", block)
    mh = re.search(r"halted slots (\d+): ([^.]*)\.", block)
    if not (mm and mb and mn and mh):
        return False, "the FAMILY line is absent or malformed"
    halted = fam.get("scored_slots_halted") or {}
    n_sc = sum(1 for r in fam["rows"] if r["scored_in_family"])
    probs = []
    if int(mm.group(1)) != fam["family_m_declared"]:
        probs.append(f"m {mm.group(1)} != family_m_declared "
                     f"{fam['family_m_declared']}")
    if mb.group(1) != repr(fam["fdr_bar_q_over_m"]):
        probs.append(f"bar {mb.group(1)} != {fam['fdr_bar_q_over_m']!r}")
    if int(mn.group(1)) != n_sc or int(mn.group(2)) != len(fam["rows"]):
        probs.append(f"rows {mn.group(1)}/{mn.group(2)} != {n_sc}/{len(fam['rows'])}")
    if int(mh.group(1)) != len(halted) or mh.group(2) != (", ".join(halted) or "none"):
        probs.append(f"halted {mh.group(1)} {mh.group(2)!r} != {len(halted)} "
                     f"{list(halted)}")
    cm = re.search(r"CLASS     \d+ REGISTRATIONS, TEXT FROZEN · FDR m = (\d+) "
                   r"DECLARED, (\d+) SCORED", block)
    if not cm or int(cm.group(1)) != fam["family_m_declared"] or int(cm.group(2)) != n_sc:
        probs.append("the CLASS line's m / scored count disagree with FAMILY.json")
    qs = parse_quotes(block)
    for q in qs:                      # the contract's m and the record's
        for mq in re.finditer(r"\bm ?= ?(\d+)\b|m stays (\d+) DECLARED", q["text"]):
            val = int(mq.group(1) or mq.group(2))
            if val != fam["family_m_declared"]:
                probs.append(f"quoted m {val} ({cite_of(q)}) != "
                             f"family_m_declared {fam['family_m_declared']}")
    for reg, t in halted.items():
        if not any(q["sel"] == f"scored_slots_halted.{reg}" and q["text"] == t
                   for q in qs):
            probs.append(f"the halted slot {reg}'s text is not quoted")
    return (not probs), (f"m = {mm.group(1)} = family_m_declared; bar "
                         f"{mb.group(1)}; {mn.group(1)}/{mn.group(2)} scored; "
                         f"halted {mh.group(2)} quoted verbatim; the contract's "
                         f"and the record's quoted m agree"
                         if not probs else "; ".join(probs))


def leg_m(ctx):
    src, draft = ctx["src"], ctx["draft"]
    fam = json.loads(src[rel(FAMILY)])
    m = fam["family_m_declared"]
    sab = [
        (f"m = {m} -> m = {m - 1} on the FAMILY line",
         lambda: check_m(plant(draft, f"FAMILY · m = {m} DECLARED",
                               f"FAMILY · m = {m - 1} DECLARED"), src)),
        ("the bar bent (x1.1)",
         lambda: check_m(plant(draft, f"bar q/m = {fam['fdr_bar_q_over_m']!r}",
                               f"bar q/m = {fam['fdr_bar_q_over_m'] * 1.1!r}"), src)),
        ("the scored-row count bent (+1)",
         lambda: check_m(resub(draft, r"(\d+) scored rows of",
                               lambda mo: f"{int(mo.group(1)) + 1} scored rows of"),
                         src)),
    ]
    return check_m(draft, src), sab


def leg_rs(ctx):
    src, X, draft = ctx["src"], ctx["X"], ctx["draft"]
    req = tuple(X[k] for k in ("rs_head", "rs_qr3", "rs_qr4", "rs_qr5"))
    lp = rel(LEDGER_MD)

    def chk(d):
        ok, det = check_quotes(d, src, path=lp, required=req)
        # the record's own pointer to Q-R3 must be the line grep finds
        pg = re.search(r"GATE per LEDGER\.md:(\d+)", X["p_gate"]["text"])
        if not pg or int(pg.group(1)) != X["rs_qr3"]["l1"]:
            return False, f"{det}; PROGRESS's Q-R3 pointer != grep's line"
        return ok, det
    q3, q4 = X["rs_qr3"], X["rs_qr4"]
    sab = [
        (f"off-by-one: LEDGER.md:{q3['l1']} -> :{q3['l1'] + 1}",
         lambda: chk(plant(draft, f"«{lp}:{q3['l1']}»", f"«{lp}:{q3['l1'] + 1}»"))),
        ("Q-R4's quoted ruling bent ((a) -> (b))",
         lambda: chk(plant(draft, "| Q-R4 ACCEPTANCE DEFINITION: (a)",
                           "| Q-R4 ACCEPTANCE DEFINITION: (b)"))),
    ]
    ok, det = chk(draft)
    return (ok, f"{det}; heading :{X['rs_head']['l1']}, Q-R3 :{q3['l1']}, "
                f"Q-R4 :{q4['l1']}, Q-R5 :{X['rs_qr5']['l1']}, ratified "
                f":{X['rs_ratified']['l1']}; PROGRESS's Q-R3 pointer agrees"), sab


NUM = r"[+-]\d+\.\d{6}"
TWIN_RE = re.compile(
    rf"^      (P-[A-Z0-9-]+) *#(\d+) (IN|--)  n (\d+) +TC ({NUM})  "
    rf"twin ({NUM})  twin\+fund ({NUM})  (twin>TC|twin<=TC) *"
    rf"flags (True|False)/(True|False)  '(.*)'$")
DIFF_RE = re.compile(
    rf"^      (P-[A-Z0-9-]+) *#(\d+) (IN|--)  base_n (\d+) +TC Δ ({NUM})  "
    rf"twin Δ ({NUM})  twin\+fund Δ ({NUM})  '(.*)'$")
V6_RE = re.compile(
    rf"^      v6 ALL · era (\S+) *· n (\d+) +TC ({NUM})  twin ({NUM})  "
    rf"twin\+fund ({NUM})  (twin>TC|twin<=TC) *flags (True|False)/(True|False)$")


def check_twin(draft: str, src: dict) -> tuple:
    block = extract_block(draft) or ""
    probs = []
    if f'QUESTION: "{QUESTION}"' not in block:
        probs.append("the question is absent or re-worded")
    fam = json.loads(src[rel(FAMILY)])
    exp, exp_diff, n_arm = {}, {}, 0
    for reg in fam["rows_files_sha256"]:
        d = json.loads(src[rel(rows_path(reg))])
        for i, r in enumerate(d["rows"]):
            n_arm += 1
            ht = (r.get("beside") or {}).get("haircut_twin")
            if ht is None:
                continue
            exp[(reg, i)] = (bool(r.get("scored_in_family")), ht["n"],
                             f6(ht["tc_expectancy_r"]), f6(ht["twin_expectancy_r"]),
                             f6(ht["twin_with_funding_companion_expectancy_r"]),
                             "twin>TC" if ht["twin_expectancy_r"] >
                             ht["tc_expectancy_r"] else "twin<=TC",
                             str(ht["sign_disagrees_with_tc"]),
                             str(ht["companion_sign_disagrees_with_tc"]), r["arm"])
            if "tc_difference_r" in ht:
                exp_diff[(reg, i)] = (ht["base_n"], f6(ht["tc_difference_r"]),
                                      f6(ht["twin_difference_r"]),
                                      f6(ht["twin_with_funding_companion_difference_r"]),
                                      r["arm"])
    got, got_diff, got_v6 = {}, {}, {}
    for line in block.split("\n"):
        m = TWIN_RE.match(line)
        if m:
            got[(m.group(1), int(m.group(2)))] = (
                m.group(3) == "IN", int(m.group(4)), m.group(5), m.group(6),
                m.group(7), m.group(8), m.group(9), m.group(10), m.group(11))
        m = DIFF_RE.match(line)
        if m:
            got_diff[(m.group(1), int(m.group(2)))] = (
                int(m.group(4)), m.group(5), m.group(6), m.group(7), m.group(8))
        m = V6_RE.match(line)
        if m:
            got_v6[m.group(1)] = m.groups()[1:]
    for k in sorted(set(exp) | set(got)):
        if exp.get(k) != got.get(k):
            probs.append(f"twin row {k}: draft {got.get(k)} != rows.json {exp.get(k)}")
    for k in sorted(set(exp_diff) | set(got_diff)):
        if exp_diff.get(k) != got_diff.get(k):
            probs.append(f"Δ row {k}: draft {got_diff.get(k)} != rows.json "
                         f"{exp_diff.get(k)}")
    nt = len(exp)
    up = [k for k, v in exp.items() if v[5] == "twin>TC"]
    up_c = [k for k in up if float(exp[k][4]) <= float(exp[k][2])]
    want = [f"COUNTS: {nt} of {n_arm} arm rows carry a twin",
            f"flags: sign_disagrees_with_tc "
            f"{sum(v[6] == 'True' for v in exp.values())}/{nt}",
            f"companion_sign_disagrees_with_tc "
            f"{sum(v[7] == 'True' for v in exp.values())}/{nt}",
            f"twin > TC on {len(up)}/{nt} · of those {len(up)}, twin+fund <= TC "
            f"on {len(up_c)}/{len(up)}"]
    fee = json.loads(src[rel(FEE)])
    for t, spec in fee["haircut_twin_tiers"].items():
        want.append(f"tier {t} {{{' '.join(spec['assets'])}}} "
                    f"{spec['bps_per_side']!r} bps/side")
    assets = fee["assets"]
    tc_rt = Counter(x["round_trip_bps_used"] for x in assets)
    want.append("TC-series toll · round_trip_bps_used · "
                + " · ".join(f"{k!r} x{c}" for k, c in sorted(tc_rt.items()))
                + f" · of {len(assets)} assets")
    n_gt = sum(1 for x in assets
               if x["haircut_twin_round_trip_bps"] > x["round_trip_bps_used"])
    want.append(f"twin round trip > TC toll on {n_gt}/{len(assets)} assets")
    v6k = rel(V6_TWIN)
    if v6k in src:
        vr = v6_rows(src[v6k])
        if isinstance(vr, str):
            want.append(f"PRESENT, NOT READ: {vr}")
        else:
            exp_v6 = {r["era"]: (str(r["n"]), f6(r["tc_expectancy_r"]),
                                 f6(r["twin_expectancy_r"]),
                                 f6(r["companion_expectancy_r"]),
                                 "twin>TC" if r["twin_expectancy_r"] >
                                 r["tc_expectancy_r"] else "twin<=TC",
                                 str(r["sign_disagrees"]),
                                 str(r["companion_sign_disagrees"]))
                      for r in vr if r["key"] == "ALL"}
            if exp_v6 != got_v6:
                probs.append(f"v6 ALL rows: draft {got_v6} != parquet {exp_v6}")
            k = v6_counts(vr)
            want += [f"V6 COUNTS over all {k['n']} rows: sign_disagrees "
                     f"{k['flag']}/{k['n']} · companion_sign_disagrees "
                     f"{k['cflag']}/{k['n']}",
                     f"twin > TC on {k['up']}/{k['n']} · of those {k['up']}, "
                     f"twin+fund <= TC on {k['up_c']}/{k['up']}"]
    else:
        want.append(f"{v6k}: ABSENT at draft time")
    for w in want:
        if w not in block:
            probs.append(f"missing/bent: {w!r}")
    return (not probs), (f"question present verbatim; {len(got)} twin rows, "
                         f"{len(got_diff)} Δ rows and {len(got_v6)} v6 ALL rows "
                         f"equal a fresh read of rows.json / the parquet; counts, "
                         f"tiers and tolls equal fee_schedule.json"
                         if not probs else "; ".join(probs[:4]))


def leg_twin(ctx):
    src, draft = ctx["src"], ctx["draft"]
    block = extract_block(draft) or ""
    first = next(ln for ln in block.split("\n") if TWIN_RE.match(ln))
    tc_tok = TWIN_RE.match(first).group(5)
    bent = f"{float(tc_tok) + 1e-6:+.6f}"
    sab = [
        (f"one number bent (first row's TC {tc_tok} -> {bent})",
         lambda: check_twin(plant(draft, first,
                                  first.replace(f"TC {tc_tok}", f"TC {bent}", 1)),
                            src)),
        ("the question withheld",
         lambda: check_twin(plant(draft, f'QUESTION: "{QUESTION}"',
                                  "QUESTION: (withheld)"), src)),
        ("a count bent (sign_disagrees_with_tc +1)",
         lambda: check_twin(resub(draft, r"flags: sign_disagrees_with_tc (\d+)/",
                                  lambda mo: f"flags: sign_disagrees_with_tc "
                                             f"{int(mo.group(1)) + 1}/"), src)),
        ("a tier's bps bent (tier A -> 99.0)",
         lambda: check_twin(resub(draft, r"(tier A \{[^}]*\}) (\S+) bps/side",
                                  r"\1 99.0 bps/side"), src)),
    ]
    if any(V6_RE.match(ln) for ln in block.split("\n")):
        sab.append(("a v6 control number bent (tuning-era twin sign flipped)",
                    lambda: check_twin(resub(
                        draft, r"(v6 ALL · era tuning *· n \d+ +TC \S+  twin )([+-])",
                        lambda mo: mo.group(1) + ("-" if mo.group(2) == "+" else "+")),
                        src)))
    return check_twin(draft, src), sab


def check_nowrite(read_fn, action) -> tuple:
    b0 = read_fn()
    action()
    b1 = read_fn()
    return (b0 == b1), (f"sha {sha(b0)[:16]}… before == after"
                        if b0 == b1 else
                        f"sha {sha(b0)[:16]}… -> {sha(b1)[:16]}… — CHANGED")


def stat_of(p: Path) -> dict:
    st = p.stat()
    return {"sha": sha(p.read_bytes()), "size": st.st_size,
            "mtime_ns": st.st_mtime_ns}


def leg_nowrite(ctx):
    before, draft = ctx["before"], ctx["draft"]

    def real():
        now = {rel(p): stat_of(p) for p in (LEDGER_APOLLO, S0_PATH)}
        same = now == before
        ok2, det2 = check_nowrite(LEDGER_APOLLO.read_bytes, ctx["rebuild_and_write"])
        g_ok, _ = output_guard([DRAFT_PATH, TRANSCRIPT_PATH])
        return (same and ok2 and g_ok), (
            f"LEDGER_APOLLO.md sha {before[rel(LEDGER_APOLLO)]['sha'][:16]}… "
            f"size {before[rel(LEDGER_APOLLO)]['size']}, and the S0 of record, "
            f"unchanged in bytes AND mtime since run start: {same}; a whole "
            f"re-build + write bracketed: {det2}; outputs only under close/ "
            f"and never a sibling's file: {g_ok}")

    buf = {"b": LEDGER_APOLLO.read_bytes()}

    def planted_append():
        buf["b"] = buf["b"] + (extract_block(draft) or "").encode()
    sab = [
        ("a planted APPEND of the draft block to an in-memory ledger copy",
         lambda: check_nowrite(lambda: buf["b"], planted_append)),
        ("an output path under exchange/status/",
         lambda: (lambda r: (r[0], f"guard refuses {r[1]}"))(
             output_guard([DRAFT_PATH, LEDGER_APOLLO]))),
        ("an output path onto the sibling's S0_VERDICTS.json",
         lambda: (lambda r: (r[0], f"guard refuses {[rel(Path(x)) for x in r[1]]}"))(
             output_guard([DRAFT_PATH, S0_PATH]))),
    ]
    return real(), sab


def leg_det(ctx):
    S = ctx["S"]

    def chk(salt=None):
        _, d1 = render_all(S, salt=salt)
        _, d2 = render_all(S, salt=salt)
        ok = d1 == d2
        if salt is not None:        # a salted sha varies by design: print no sha
            return ok, f"two salted builds byte-identical: {ok}"
        disk = d1 == DRAFT_PATH.read_bytes()
        return (ok and disk), (f"draft {sha(d1)[:16]}… vs {sha(d2)[:16]}…; "
                               f"== the file on disk: {disk}")
    import time
    sab = [("a wall-clock salt in the header (time.perf_counter_ns)",
            lambda: chk(salt=time.perf_counter_ns))]
    return chk(), sab


VERD_RE = re.compile(r"^    (P-[A-Z0-9-]+) +\[(\d+)%\]  (NOT SUPPORTED|SUPPORTED|"
                     r"HALT — NO VERDICT)")


def check_s0(s0_bytes: bytes, draft: str, src: dict) -> tuple:
    """THREE WAYS: a fresh read of FAMILY.json/rows.json == the §0 of record ==
    the draft's §0 lines."""
    probs = []
    try:
        D = derive_six(src)
    except SystemExit as e:
        return False, f"the fresh derivation HALTs: {e}"
    exp = {v["registration"]: s0_expect(v) for v in D["six"]}
    try:
        s0 = read_s0(s0_bytes)
        bad = s0_disagreements(s0, D)
    except Exception as e:                                   # noqa: BLE001
        return False, f"the §0 of record does not parse ({type(e).__name__}: {e})"
    probs += bad
    block = extract_block(draft) or ""
    lines = block.split("\n")
    seen = {}
    for i, line in enumerate(lines):
        m = VERD_RE.match(line)
        if not m:
            continue
        reg, prior, verd = m.group(1), m.group(2), m.group(3)
        if verd == "HALT — NO VERDICT":
            a1 = re.match(r"^        '(.*)' · halted at ", lines[i + 1])
            nxt = next((j for j in range(i + 1, len(lines))
                        if VERD_RE.match(lines[j]) or not lines[j].strip()),
                       len(lines))
            qs = [q for q in parse_quotes("\n".join(lines[i:nxt]))
                  if q["sel"] == f"scored_slots_halted.{reg}"]
            seen[reg] = {"arm": a1.group(1) if a1 else None,
                         "halt": qs[0]["text"] if qs else None, "prior_pct": prior}
            continue
        a1 = re.match(r"^        '(.*)' · \S+ · era \S+ · n (\d+)$", lines[i + 1])
        a2 = re.match(rf"^        point ({NUM}) R · CI \[({NUM}), ({NUM})\] · "
                      rf"p (\d+\.\d{{6}})$", lines[i + 3])
        a3 = re.match(r"^        clears_bh_bar (\S+) · LOAO (.*) \(above of record",
                      lines[i + 4])
        if not (a1 and a2 and a3):
            probs.append(f"{reg}: its §0 lines are malformed")
            continue
        seen[reg] = {"arm": a1.group(1), "n": a1.group(2), "ci_point": a2.group(1),
                     "ci_lo": a2.group(2), "ci_hi": a2.group(3),
                     "p_one_sided": a2.group(4), "verdict": verd,
                     "clears_bh_bar": a3.group(1), "loao_line": a3.group(2),
                     "prior_pct": prior}
    if seen != exp:
        probs.append("the draft's §0 lines != the fresh derivation on "
                     + str(sorted(k for k in set(exp) | set(seen)
                                  if exp.get(k) != seen.get(k))))
    return (not probs), (f"{len(exp)} slots agree three ways — FAMILY.json/"
                         f"rows.json (fresh) == {rel(S0_PATH)} == the draft"
                         if not probs else "; ".join(probs[:3]))


def leg_s0(ctx):
    draft, src = ctx["draft"], ctx["src"]
    disk = S0_PATH.read_bytes()
    obj = json.loads(disk)
    ns = next(ln["reg"] for ln in obj["lines"] if ln.get("kind") == "verdict_row"
              and any(p.get("col") == "verdict" and p["s"] == "NOT SUPPORTED"
                      for p in ln["parts"]))

    def mutate(fn):
        o = copy.deepcopy(obj)
        fn(o)
        return json.dumps(o, ensure_ascii=False).encode()

    def flip(o):
        for ln in o["lines"]:
            if ln.get("reg") == ns and ln.get("kind") == "verdict_row":
                for p in ln["parts"]:
                    if p.get("col") == "verdict":
                        p["s"] = "SUPPORTED"

    def drop_halted(o):
        o["lines"] = [ln for ln in o["lines"]
                      if not (ln.get("kind") == "verdict_row"
                              and any(p.get("col") == "halt" for p in ln["parts"]))]
    sab = [
        (f"the §0 file flips {ns} to SUPPORTED",
         lambda: check_s0(mutate(flip), draft, src)),
        ("the §0 file drops the HALTed slot",
         lambda: check_s0(mutate(drop_halted), draft, src)),
        (f"the draft types {ns} SUPPORTED",
         lambda: check_s0(disk, resub(
             draft, rf"(    {re.escape(ns)} +\[\d+%\]  )NOT SUPPORTED",
             r"\1SUPPORTED"), src)),
    ]
    return check_s0(disk, draft, src), sab


def check_tier(draft: str, src: dict) -> tuple:
    fam = json.loads(src[rel(FAMILY)])
    block = extract_block(draft) or ""
    probs = []
    cleared = [r for r in fam["rows"] if r["scored_in_family"]
               and r["verdict"] == "SUPPORTED" and r["clears_bh_bar"] is True
               and r["loao_clears_line_of_record"] is True]
    m = fam["family_m_declared"]
    head = re.search(r"TIER-C\d+: (\d+) OF THE m = (\d+) DECLARED CLEARS ITS OWN BAR",
                     block)
    if not head or int(head.group(1)) != len(cleared) or int(head.group(2)) != m:
        probs.append("the tier headline's count is not FAMILY.json's")
    for s in cleared:
        reg = s["registration"]
        want = [f"{reg}'s SCORED arm '{s['arm']}' is SUPPORTED (CI-only); "
                f"LOAO and BH beside, both clear:",
                f"CI (the deciding clause) verdict {s['verdict']} — CI [{f6(s['ci_lo'])}, "
                f"{f6(s['ci_hi'])}], lo > 0 {jb(s['ci_lo'] > 0)}",
                f"LOAO (beside, deciding nothing) {s['loao_line']} — line of record clears "
                f"{jb(s['loao_clears_line_of_record'])}",
                f"BH (beside, deciding nothing) p {p6(s['p_one_sided'])} <= bar "
                f"{p6(s['fdr_bar_q_over_m'])} — clears_bh_bar {jb(s['clears_bh_bar'])}"]
        for w in want:
            if w not in block:
                probs.append(f"clause line missing/bent: {w[:60]!r}")
        d = json.loads(src[rel(rows_path(reg))])
        tun = [(i, r["score_row"]) for i, r in enumerate(d["rows"])
               if r.get("score_row") and r["score_row"]["arm_era"] == "tuning"
               and r["score_row"]["arm_base"] == s["arm_base"]]
        if len(tun) != 1:
            probs.append(f"{reg}: {len(tun)} tuning-era arms")
            continue
        i, sr = tun[0]
        got = re.search(rf"Its TUNING-ERA arm '([^']*)' reads (NOT SUPPORTED|SUPPORTED)\n"
                        rf" +\(Δ ({NUM}), CI \[({NUM}), ({NUM})\], p (\d+\.\d{{6}}), "
                        rf"LOAO ([^)]*)\) · (\S+)\.rows\.json rows\[(\d+)\]", block)
        exp = (sr["arm"], sr["verdict"], f6(sr["ci_point"]), f6(sr["ci_lo"]),
               f6(sr["ci_hi"]), p6(sr["p_one_sided"]), sr["loao_line"], reg, str(i))
        if not got or got.groups() != exp:
            probs.append(f"the tuning-era line {got.groups() if got else None} "
                         f"!= rows.json {exp}")
        tail = ("." if sr["verdict"] == "SUPPORTED"
                else "; ITS TUNING ERA ALONE DOES NOT.")
        if f"THE ONE CELL THE CONTRACT PRE-NAMED{tail}" not in block:
            probs.append("the headline's tuning-era clause disagrees with rows.json")
        texts = json.loads(src[rel(REG_TEXTS)])
        if "IN-SAMPLE RE-SCORE" in texts[reg]["text"]:
            qs = [q for q in parse_quotes(block)
                  if q["path"] == rel(REG_TEXTS) and q["sel"] == f"{reg}.text"
                  and "IN-SAMPLE RE-SCORE" in q["text"]]
            if (not qs or "AND ITS OWN FILED TEXT CALLS IT, IN LARGE PART, AN "
                          "IN-SAMPLE RE-SCORE:" not in block):
                probs.append(f"{reg}'s own filed IN-SAMPLE caveat is not carried")
    return (not probs), (f"{len(cleared)} of m = {m} SUPPORTED (CI-only) with LOAO and "
                         f"BH beside, both clear; each line and the tuning-era arm's verdict equal "
                         f"FAMILY.json / rows.json"
                         if not probs else "; ".join(probs[:3]))


def leg_tier(ctx):
    src, draft = ctx["src"], ctx["draft"]
    sab = [
        ("the tuning-era verdict typed SUPPORTED",
         lambda: check_tier(resub(draft,
                                  r"(Its TUNING-ERA arm '[^']*' reads )NOT SUPPORTED",
                                  r"\1SUPPORTED"), src)),
        ("the BH column typed clears_bh_bar false",
         lambda: check_tier(plant(draft, "— clears_bh_bar true",
                                  "— clears_bh_bar false"), src)),
        ("the filed IN-SAMPLE caveat dropped from the tier line",
         lambda: check_tier(plant(draft, "AND ITS OWN FILED TEXT CALLS IT, IN "
                                  "LARGE PART, AN IN-SAMPLE RE-SCORE:",
                                  "AND IT STANDS ON ITS OWN:"), src)),
    ]
    return check_tier(draft, src), sab


def leg_cite(ctx):
    src, X, draft = ctx["src"], ctx["X"], ctx["draft"]

    def chk(d):
        return check_quotes(d, src)
    word = X["tc9_close"]["text"].split(" ")[0]
    sab = [
        (f"TC9's closing words bent ('{word}' -> 'TEN')",
         lambda: chk(plant(draft, f"| {X['tc9_close']['text']}",
                           f"| {X['tc9_close']['text'].replace(word, 'TEN', 1)}"))),
        ("a JSON cite re-pointed (text_prescribes[1] -> [0])",
         lambda: chk(plant(draft, ".text_prescribes[1]»", ".text_prescribes[0]»"))),
        ("a PROGRESS quote bent (HOLDS -> FAILS)",
         lambda: chk(plant(draft, "Q-R5 attestation HOLDS", "Q-R5 attestation FAILS"))),
    ]
    return chk(draft), sab


def check_format(draft: str, X: dict) -> tuple:
    block = extract_block(draft)
    if block is None:
        return False, "the append markers are missing"
    probs = []
    if not block.startswith(X["sep"]):
        probs.append(f"does not open with the ledger's separator {X['sep']!r}")
    body = block[len(X["sep"]):]
    if not re.match(r"=== STATUS_APOLLO — \d{4}-\d{2}-\d{2} — TIER-C\d+ · [^\n]+ ===\n"
                    r"LANE      [^\n]+\nCLASS     ", body):
        probs.append("header / LANE / CLASS lines do not mirror the last block")
    if not block.endswith("\n=== END ===\n") or block.count("=== END ===") != 1:
        probs.append("does not close on exactly one '=== END ===' line")
    return (not probs), (f"opens on the ledger's own separator {X['sep']!r}; "
                         f"header / LANE / CLASS mirror the block at "
                         f"LEDGER_APOLLO.md:{X['last_header']['l1']}; closes on "
                         f"one '=== END ==='" if not probs else "; ".join(probs))


def leg_format(ctx):
    X, draft = ctx["X"], ctx["draft"]
    sab = [
        ("the '=== END ===' terminator dropped",
         lambda: check_format(plant(draft, "\n=== END ===\n" + END,
                                    "\n" + END), X)),
        ("the separator dropped",
         lambda: check_format(plant(draft, BEGIN + "\n" + X["sep"],
                                    BEGIN + "\n"), X)),
    ]
    return check_format(draft, X), sab


FORBIDDEN_MODULES = ("tierc2_baseline", "engine")
FORBIDDEN_ATTRS = ("score", "finish_family", "register", "_mark_scored",
                   "load_klines", "load_funding")


def check_closure(source: str) -> tuple:
    tree = ast.parse(source)
    probs = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                if a.name.split(".")[0] in FORBIDDEN_MODULES:
                    probs.append(f"import {a.name}")
        elif isinstance(node, ast.ImportFrom):
            if (node.module or "").split(".")[0] in FORBIDDEN_MODULES:
                probs.append(f"from {node.module} import …")
        elif isinstance(node, ast.Attribute) and node.attr in FORBIDDEN_ATTRS:
            probs.append(f".{node.attr}")
        elif isinstance(node, ast.Name) and node.id in FORBIDDEN_ATTRS:
            probs.append(node.id)
    return (not probs), ("no bar loader, no engine import, no "
                         "score / finish_family / register reference"
                         if not probs else f"forbidden: {sorted(set(probs))}")


def leg_closure(ctx):
    own = Path(__file__).read_text(encoding="utf-8")
    sab = [
        ("a bar read planted (import tierc2_baseline; TB.load_klines)",
         lambda: check_closure(own + "\nimport tierc2_baseline as TB\n"
                                     "TB.load_klines('BTCUSDT', '4h')\n")),
        ("a score call planted (TP.score)",
         lambda: check_closure(own + "\nTP.score(None)\n")),
    ]
    return check_closure(own), sab


LEGS = [
    ("F-LA-Q6", "a quoted Q6 text is not a byte substring of the contract file, "
     "its cited lines do not hold it, or either located hold (the ':2-3' hold and "
     "the ':137' phrase) is absent from the block", leg_q6),
    ("F-LA-M", "the draft's m != FAMILY.json family_m_declared (or the bar, the N "
     "scored rows, the halted slot's quoted text, the CLASS line, or any m the "
     "draft quotes disagrees with FAMILY.json)", leg_m),
    ("F-LA-RS", "a cited LEDGER.md line does not contain its quoted text, or the "
     "07-29 RS heading / Q-R3 / Q-R4 / Q-R5 citation is absent, or PROGRESS's "
     "Q-R3 pointer is not grep's line", leg_rs),
    ("F-LA-TWIN", "the slippage-twin question is absent or re-worded, or any twin "
     "number, Δ, count, tier or toll figure differs from a fresh read of "
     "rows.json / fee_schedule.json / V6_CONTROL_HAIRCUT_TWIN.parquet", leg_twin),
    ("F-LA-NOWRITE", "exchange/status/LEDGER_APOLLO.md's bytes (or size or mtime) "
     "change during the run, the S0 of record changes, or any output path lies "
     "outside research_outputs/tierc10/close/ or onto a sibling's file",
     leg_nowrite),
    ("F-DET", "two builds from the same bytes differ, or a build differs from the "
     "draft this run wrote", leg_det),
    ("F-LA-S0", "the §0 of record (close/S0_VERDICTS.json), a fresh read of "
     "FAMILY.json/rows.json and the draft's §0 lines disagree on any slot "
     "(verdict or HALT text, arm, n, point, CI, p, BH column, LOAO line, prior)",
     leg_s0),
    ("F-LA-TIER", "the tier line's count, any clause value, or the tuning-era arm's "
     "verdict differs from FAMILY.json / P-TRG-2.rows.json, or the clearing "
     "registration's own filed IN-SAMPLE caveat is not carried", leg_tier),
    ("F-LA-CITE", "ANY «cite» in the draft (contract, LEDGER.md, LEDGER_APOLLO.md, "
     "PROGRESS.json, FAMILY.json, rows.json, fee_schedule.json, "
     "REGISTRATION_TEXTS.json) does not verify against its source", leg_cite),
    ("F-LA-FORMAT", "the block does not open on the ledger's own inter-block "
     "separator, mirror the last block's header / LANE / CLASS lines, and close "
     "on exactly one '=== END ==='", leg_format),
    ("F-LA-CLOSURE", "this module imports a bar loader or the engine, or names "
     "score / finish_family / register / _mark_scored / load_klines / "
     "load_funding", leg_closure),
]


def run_legs(ctx) -> tuple:
    T = []
    green = sab_red = sab_total = 0
    for name, fails_if, fn in LEGS:
        T.append(f"{name} · FAILS IF {fails_if}")
        try:
            (ok, det), sabs = fn(ctx)
        except Exception as e:                               # noqa: BLE001
            ok, det, sabs = False, f"leg raised {type(e).__name__}: {e}", []
        T.append(f"  real      {'GREEN' if ok else 'RED'} — {det}")
        sabs_ok = bool(sabs)
        for sname, sfn in sabs:
            sab_total += 1
            try:
                sok, sdet = sfn()
            except Exception as e:                           # noqa: BLE001
                sok, sdet = True, f"sabotage raised {type(e).__name__}: {e}"
            if not sok:
                sab_red += 1
            else:
                sabs_ok = False
            T.append(f"  sabotage  {sname}: "
                     f"{'RED (as required)' if not sok else 'GREEN — THE LEG IS BLIND'}"
                     f" — {sdet}")
        leg_ok = ok and sabs_ok
        green += leg_ok
        T.append(f"  => {name} {'GREEN' if leg_ok else 'RED'}")
        T.append("")
    T.append(f"SUMMARY  {green}/{len(LEGS)} GREEN · {len(LEGS) - green} RED · "
             f"sabotages {sab_red}/{sab_total} RED as required")
    return T, green == len(LEGS)


# ═══════════════════════════════════════════════════════════ MAIN
def main() -> int:
    before = {rel(p): stat_of(p) for p in (LEDGER_APOLLO, S0_PATH) if p.exists()}
    sub = preamble()
    S = read_sources()
    X, draftb = render_all(S)
    write_out(DRAFT_PATH, draftb)

    def rebuild_and_write():
        _, d2 = render_all(read_sources())
        write_out(DRAFT_PATH, d2)

    ctx = {"S": S, "src": read_sources(), "X": X, "draft": draftb.decode(),
           "before": before, "rebuild_and_write": rebuild_and_write}
    T = [f"{X['tier']} · CLOSE · LEDGER_APOLLO APPEND — FIXTURES (F-LA)",
         f"substrate {sub['substrate']} · as-of {X['as_of_of_record']} · "
         f"REPORT-ONLY: drafts only; scores nothing; reads no bars; writes "
         f"nothing under exchange/ and no sibling's file",
         f"contract {rel(CONTRACT)} sha {X['contract_sha']} (= PROGRESS.json "
         f"contract_of_record: {X['contract_sha_agrees']})",
         f"§0 of record {rel(S0_PATH)} sha {sha(S[rel(S0_PATH)])} (builder "
         f"{X['s0']['builder']}) — agrees cell-for-cell with FAMILY.json/rows.json",
         "located this run: "
         f"Q6 hold :{X['q6_hold']['l1']}-{X['q6_hold']['l2']} · "
         f"Q6 phrase :{X['q6_137']['l1']} · CENSUS-3 :{X['census3']['l1']} · "
         f"LEDGER.md RS heading :{X['rs_head']['l1']} · Q-R3 :{X['rs_qr3']['l1']} · "
         f"Q-R4 :{X['rs_qr4']['l1']} · Q-R5 :{X['rs_qr5']['l1']} · "
         f"LEDGER_APOLLO last block :{X['last_header']['l1']}",
         "OUTPUT (sha256 · bytes)",
         f"  {sha(draftb)} · {len(draftb)} · {rel(DRAFT_PATH)}",
         ""]
    legs, all_ok = run_legs(ctx)
    T.extend(legs)
    tb = ("\n".join(T) + "\n").encode()
    write_out(TRANSCRIPT_PATH, tb)
    after = {rel(p): stat_of(p) for p in (LEDGER_APOLLO, S0_PATH) if p.exists()}
    tail_ok = after == before
    print(tb.decode(), end="")
    print(f"[run] transcript {rel(TRANSCRIPT_PATH)} sha256 {sha(tb)}")
    print(f"[run] draft {rel(DRAFT_PATH)} sha256 {sha(draftb)}")
    print(f"[run] LEDGER_APOLLO.md and the S0 of record unchanged at exit: {tail_ok}")
    return 0 if (all_ok and tail_ok) else 1


if __name__ == "__main__":
    sys.exit(main())
