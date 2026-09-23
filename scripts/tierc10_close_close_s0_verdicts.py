#!/usr/bin/env python
"""TIER-C10 · CLOSE §0 — SIX VERDICT ROWS, THE ADMITTED LIST, THE FORWARD STRIP.

Contract of record: exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md:131
    "· §0 verdicts first: six rows + the admitted list + the forward strip"

WHAT THIS IS
  A REPORT-ONLY TRANSCRIPTION.  It builds a FRAGMENT —
  research_outputs/tierc10/close/S0_VERDICTS.md and S0_VERDICTS.json — to be
  spliced over BUILD_DRAFT.md "## 0 · VERDICTS" at CLOSE.  THIS SCRIPT NEVER
  EDITS BUILD_DRAFT.md.  It scores nothing, re-scores nothing, rounds nothing,
  reads no bar, imports no estate module, and writes nowhere but
  research_outputs/tierc10/close/.

SOURCE PRECISION, MECHANICALLY
  Every JSON input is parsed with parse_float = parse_int = Tok, a str subclass
  that holds a number EXACTLY as its file spells it.  No float is ever made on
  the table code path, so nothing can be rounded; F-S0-NOTYPE scans the AST.
  Every printed value is recorded in S0_VERDICTS.json as (source, JSON pointer,
  printed string) and F-S0-READ re-reads each one by an INDEPENDENT route
  (plain json.loads, the writer's own repr) and compares string-for-string.

INPUTS (read-only)
  scores/FAMILY.json            family_m_declared, fdr_bar_q_over_m, rows[*]
                                .clears_bh_bar, scored_slots_halted, law
  scores/<REG>.rows.json  x6    the ONE arm with scored_in_family true: its
                                score_row and its beside (haircut_twin,
                                brk_sealed_row.height_vs_toll)
  REGISTRY_PIN.json             order_of_filing, registry_len, registry_head
  REGISTRATION_TEXTS.json       prior_pct; the P-SPR-2 superseded draft; the
                                R8-supersedes-R2 panel paragraphs
  data/STAGE_D_MANIFEST.json    admission.{rule, rows, excluded}; panels
  REGISTRATION_PLAN.md          the note that UNSEEN12 is P-GEN-1's panel
  BUILD_DRAFT.md §R0.1          the record that the interrupted run filed nothing
  the contract                  LAW 3, quoted
  OPERATOR_RULINGS.md           the open PUMPFUN / MNT lean, quoted
  close/FORWARD_STRIP.md        inlined byte-for-byte

OUTPUTS
  research_outputs/tierc10/close/S0_VERDICTS.md
  research_outputs/tierc10/close/S0_VERDICTS.json
  research_outputs/tierc10/close/FIXTURES_CLOSE_s0_verdicts.txt  (transcript)

THE LEGS (each states FAILS IF; each carries a sabotage that must go RED)
  F-S0-READ     FAILS IF any printed value differs string-for-string from a
                fresh read of its source field.
                BREAK: one ci_lo perturbed in a COPY of a rows file.
  F-S0-SIX      FAILS IF there are not exactly 6 rows in REGISTRY_PIN order.
                BREAK: P-BE-1 dropped.
  F-S0-BAR      FAILS IF clears_bh_bar is true where p > fdr_bar_q_over_m, or
                where the CI straddles 0, or where LOAO is below its bar (and,
                conversely, false where p <= bar).
                BREAK: P-GEN-1's clears set true in a COPY of FAMILY.json.
  F-S0-HALT     FAILS IF P-BE-1 shows a point, CI or p.
                BREAK: its Tier-E A2 numbers injected.
  F-S0-ADMIT    FAILS IF the admitted list differs from STAGE_D_MANIFEST
                admission.  BREAK: one asset dropped.
  F-S0-STRIP    FAILS IF close/FORWARD_STRIP.md is absent or not byte-inlined.
                BREAKS: the strip absent; the inlined bytes one byte short.
  F-S0-NOTYPE   FAILS IF a float literal appears in the module, or a float() /
                round() call or a format spec on the table code path (AST).
                BREAKS: a planted float literal; a planted round().
  F-S0-CLOSURE  FAILS IF the module imports outside the stdlib allowlist or
                names a scorer / registrar / bar loader.  BREAKS: a planted
                estate import; a planted TP.score call.
  F-S0-WRITES   FAILS IF a build writes anything but the two named outputs, or
                BUILD_DRAFT.md's sha moves across a build.
                BREAK: a writer that drops a third file.
  F-DET         FAILS IF two builds (in-process, and a fresh process) are not
                byte-identical.  BREAK: a build stamp that counts.

Run:
  export NAIAD_CACHE_DIR=/Users/luis/.cache/naiad/snapshots/tc10_20260921 \\
         PYTHONDONTWRITEBYTECODE=1
  ~/venvs/naiad/bin/python scripts/tierc10_close_close_s0_verdicts.py
"""
from __future__ import annotations

import argparse
import ast
import contextlib
import decimal
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLOSE_REL = "research_outputs/tierc10/close"
CLOSE_DIR = ROOT / CLOSE_REL
SNAPSHOT = "/Users/luis/.cache/naiad/snapshots/tc10_20260921"
VENV_PREFIX = str(Path.home() / "venvs" / "naiad")
SCRIPT_REL = "scripts/" + Path(__file__).name
MD_NAME = "S0_VERDICTS.md"
JSON_NAME = "S0_VERDICTS.json"
TRANSCRIPT_NAME = "FIXTURES_CLOSE_s0_verdicts.txt"
OUTPUT_NAMES = (MD_NAME, JSON_NAME)
DASH = "—"
STRIP_TAG = "close/FORWARD_STRIP.md"
STRIP_END = f"<!-- END INLINE {STRIP_TAG} -->"

FIXED_SOURCES = {
    "pin": "research_outputs/tierc10/REGISTRY_PIN.json",
    "family": "research_outputs/tierc10/scores/FAMILY.json",
    "texts": "research_outputs/tierc10/REGISTRATION_TEXTS.json",
    "manifest": "research_outputs/tierc10/data/STAGE_D_MANIFEST.json",
    "plan": "research_outputs/tierc10/REGISTRATION_PLAN.md",
    "draft": "research_outputs/tierc10/BUILD_DRAFT.md",
    "contract": "exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md",
    "rulings": "research_outputs/tierc10/OPERATOR_RULINGS.md",
    "strip": CLOSE_REL + "/FORWARD_STRIP.md",
}
TEXT_KEYS = ("plan", "draft", "contract", "rulings")

VCOLS = ("#", "registration", "prior", "arm", "panel", "era", "ruler", "n",
         "point", "[CI lo, CI hi]", "p (one-sided)", "verdict",
         "clears BH bar", "LOAO above / present vs bar · line",
         "haircut twin E[R]", "height-vs-toll (BRK)")
VHEADER = "| " + " | ".join(VCOLS) + " |"
ACOLS = ("asset", "stem", "venue", "closed 4h bars", "admitted")
AHEAD_A = "| " + " | ".join(ACOLS) + " |"
AHEAD_B = "| " + " | ".join(ACOLS + ("panel",)) + " |"


class Halt(SystemExit):
    """A refusal.  Its text always starts 'HALT:'."""


def HALT(msg: str):
    raise Halt("HALT: " + msg)


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


# ═══════════════════════════════════════════════════════ THE RUN/HALT PREAMBLE
def preamble() -> list:
    """RUN only under the lane's interpreter law; HALT otherwise.  Returns the
    RUN lines (no clock, no temp path, no HEAD — two runs must be identical)."""
    env = os.environ.get("NAIAD_CACHE_DIR")
    if env != SNAPSHOT:
        HALT(f"NAIAD_CACHE_DIR must be exported as {SNAPSHOT} before python "
             f"starts (got {env!r}); the live data_cache is never touched.")
    if os.environ.get("PYTHONDONTWRITEBYTECODE") != "1":
        HALT("PYTHONDONTWRITEBYTECODE=1 must be exported before python starts.")
    if str(Path(sys.prefix)) != VENV_PREFIX:
        HALT(f"run under ~/venvs/naiad/bin/python (sys.prefix is {sys.prefix}).")
    return [f"RUN · {SCRIPT_REL}",
            f"RUN · NAIAD_CACHE_DIR={SNAPSHOT} · PYTHONDONTWRITEBYTECODE=1 · "
            f"interpreter ~/venvs/naiad",
            "RUN · REPORT-ONLY TRANSCRIPTION: scores nothing, reads no bar, "
            "never edits BUILD_DRAFT.md, writes only under " + CLOSE_REL + "/"]


# ═══════════════════════════════════════════════ READING AT SOURCE PRECISION
class Tok(str):
    """A JSON number exactly as its source file spells it.  Never converted."""
    __slots__ = ()


def parse_tok(text: str):
    return json.loads(text, parse_float=Tok, parse_int=Tok,
                      parse_constant=Tok)


def render(v) -> str:
    if v is True:
        return "true"
    if v is False:
        return "false"
    if v is None:
        return "null"
    if isinstance(v, str):
        return str(v)
    HALT(f"not a printable scalar: {type(v).__name__}")


def esc(k) -> str:
    return str(k).replace("~", "~0").replace("/", "~1")


def resolve(doc, ptr: str):
    cur = doc
    for raw in ptr.split("/")[1:]:
        k = raw.replace("~1", "/").replace("~0", "~")
        cur = cur[int(k)] if isinstance(cur, list) else cur[k]
    return cur


def rows_rel(reg: str) -> str:
    return f"research_outputs/tierc10/scores/{reg}.rows.json"


def src_rel(key: str) -> str:
    return rows_rel(key[5:]) if key.startswith("rows:") else FIXED_SOURCES[key]


def filing_order(pin: dict) -> list:
    return [str(r) for r in pin["order_of_filing"]]


class Ctx:
    """Every input, read once.  `over` maps a source key to another path — a
    sabotage reads a COPY; the recorded path is always the canonical one."""

    def __init__(self, over: dict | None = None):
        self.over = dict(over or {})
        self.docs, self.raw, self.lines = {}, {}, {}
        self.order = filing_order(self._json("pin"))
        for reg in self.order:
            self._json("rows:" + reg)
        for k in ("family", "texts", "manifest"):
            self._json(k)
        for k in TEXT_KEYS:
            p = self.path(k)
            if not p.is_file():
                HALT(f"input absent: {src_rel(k)}")
            self.raw[k] = p.read_bytes()
            self.lines[k] = self.raw[k].decode("utf-8").split("\n")
        sp = self.path("strip")
        self.strip = sp.read_bytes() if sp.is_file() else None

    def path(self, key: str) -> Path:
        return Path(self.over[key]) if key in self.over else ROOT / src_rel(key)

    def _json(self, key: str):
        p = self.path(key)
        if not p.is_file():
            HALT(f"input absent: {src_rel(key)}")
        self.raw[key] = p.read_bytes()
        self.docs[key] = parse_tok(self.raw[key].decode("utf-8"))
        return self.docs[key]


# ═════════════════════════════════════════════════════════════ TEMPLATE PARTS
def lit(s: str, col: str | None = None) -> dict:
    p = {"t": "lit", "s": s}
    if col:
        p["col"] = col
    return p


def val(ctx: Ctx, key: str, ptr: str, col: str | None = None,
        in_code: bool = False) -> dict:
    s = render(resolve(ctx.docs[key], ptr))
    if "|" in s or "\n" in s or (in_code and "`" in s):
        HALT(f"{src_rel(key)}{ptr} cannot sit in a table cell verbatim: {s!r}")
    p = {"t": "val", "src": key, "path": src_rel(key), "ptr": ptr, "s": s}
    if col:
        p["col"] = col
    return p


def code(ctx: Ctx, key: str, ptr: str, col: str | None = None) -> list:
    return [lit("`"), val(ctx, key, ptr, col, in_code=True), lit("`")]


def der(what: str, s: str, arg: str | None = None,
        col: str | None = None) -> dict:
    p = {"t": "der", "what": what, "s": s}
    if arg is not None:
        p["arg"] = arg
    if col:
        p["col"] = col
    return p


def row_parts(cells: list) -> list:
    out = [lit("| ")]
    for i, c in enumerate(cells):
        if i:
            out.append(lit(" | "))
        out.extend(c)
    out.append(lit(" |"))
    return out


class Doc:
    def __init__(self):
        self.lines, self.recs, self.quotes = [], [], []

    def add(self, *ss: str):
        for s in ss:
            self.lines.append(s)

    def tpl(self, parts: list, kind: str, **meta):
        rec = {"line": len(self.lines), "kind": kind}
        rec.update(meta)
        rec["parts"] = parts
        self.recs.append(rec)
        self.lines.append("".join(p["s"] for p in parts))

    def quote(self, head: str, key: str, loc: dict, text: str, style: str):
        if "```" in text:
            HALT(f"a quote from {src_rel(key)} holds a code fence")
        hdr = len(self.lines)
        self.lines.append(head)
        self.lines.append("")
        start = len(self.lines)
        self.lines.extend(quote_lines(text, style))
        self.quotes.append({"src": key, "path": src_rel(key), "loc": loc,
                            "style": style, "hdr_line": hdr,
                            "md_lines": [start, len(self.lines)],
                            "text": text})
        self.lines.append("")


def quote_lines(text: str, style: str) -> list:
    if style == "fence":
        return ["```text"] + text.split("\n") + ["```"]
    return [("> " + ln) if ln else ">" for ln in text.split("\n")]


def loc_label(loc: dict) -> str:
    if "lines" in loc:
        return f"lines {loc['lines'][0]}–{loc['lines'][1]}"
    return f"`{loc['reg']}.text` characters {loc['chars'][0]}–{loc['chars'][1]}"


# ═══════════════════════════════════════════════════ THE SIX VERDICT ROWS
def family_index(ctx: Ctx, reg: str, arm: str) -> int:
    hits = [k for k, r in enumerate(ctx.docs["family"]["rows"])
            if str(r["registration"]) == reg and str(r["arm"]) == arm
            and r.get("scored_in_family") is True]
    if len(hits) != 1:
        HALT(f"FAMILY.json holds {len(hits)} scored rows for {reg} / {arm}")
    return hits[0]


def scored_index(ctx: Ctx, reg: str) -> int:
    doc = ctx.docs["rows:" + reg]
    if str(doc["registration"]) != reg:
        HALT(f"{rows_rel(reg)} names {doc['registration']}, not {reg}")
    hits = [j for j, r in enumerate(doc["rows"])
            if r.get("scored_in_family") is True]
    if len(hits) != 1:
        HALT(f"{rows_rel(reg)} holds {len(hits)} scored arms (one law: one)")
    return hits[0]


def score_cells(ctx: Ctx, key: str, b: str) -> list:
    s = b + "/score_row"
    return [
        [val(ctx, key, s + "/panel_name", "panel_name")],
        [val(ctx, key, s + "/arm_era", "arm_era")],
        [val(ctx, key, s + "/ruler", "ruler")],
        code(ctx, key, s + "/n", "n"),
        code(ctx, key, s + "/ci_point", "ci_point"),
        [lit("[`"), val(ctx, key, s + "/ci_lo", "ci_lo", True), lit("`, `"),
         val(ctx, key, s + "/ci_hi", "ci_hi", True), lit("`]")],
        code(ctx, key, s + "/p_one_sided", "p_one_sided"),
    ]


def loao_cell(ctx: Ctx, key: str, b: str) -> list:
    s = b + "/score_row"
    return [lit("`"), val(ctx, key, s + "/loao_above_of_record",
                          "loao_above_of_record", True),
            lit("/"), val(ctx, key, s + "/loao_assets_present",
                          "loao_assets_present", True),
            lit("` vs bar `"), val(ctx, key, s + "/loao_bar_above_half",
                                   "loao_bar_above_half", True),
            lit("` · "), val(ctx, key, s + "/loao_line", "loao_line")]


def twin_cell(ctx: Ctx, key: str, b: str, row: dict) -> list:
    h = b + "/beside/haircut_twin"
    out = code(ctx, key, h + "/twin_expectancy_r", "twin_expectancy_r")
    if "twin_difference_r" in row["beside"]["haircut_twin"]:
        out += [lit(" · Δ ")] + code(ctx, key, h + "/twin_difference_r",
                                     "twin_difference_r")
    return out


def brk_cell(ctx: Ctx, key: str, b: str, row: dict) -> list:
    if "brk_sealed_row" not in row["beside"]:
        return [lit(DASH, "height_vs_toll")]
    h = b + "/beside/brk_sealed_row/height_vs_toll"
    return [val(ctx, key, h + "/lens", "hvt_lens"), lit(" · verdict_pass `"),
            val(ctx, key, h + "/verdict_pass", "hvt_verdict_pass", True),
            lit("` · "), val(ctx, key, h + "/reason", "hvt_reason")]


def halt_cells(ctx: Ctx, reg: str, key: str, b: str) -> list:
    """The HALTed slot: FAMILY.json's scored_slots_halted text, verbatim, and
    NO number — no n, point, CI, p, clears, LOAO or twin."""
    dash = [[lit(DASH, c)] for c in ("panel_name", "arm_era", "ruler", "n",
                                     "ci_point", "ci", "p_one_sided")]
    return dash + [
        [val(ctx, "family", "/scored_slots_halted/" + esc(reg), "halt")],
        [lit(DASH, "clears_bh_bar")], [lit(DASH, "loao")],
        [lit(DASH, "twin")], [lit(DASH, "height_vs_toll")]]


def verdict_cells(ctx: Ctx, i: int, reg: str) -> list:
    key = "rows:" + reg
    j = scored_index(ctx, reg)
    b = f"/rows/{j}"
    row = ctx.docs[key]["rows"][j]
    head = [code(ctx, "pin", f"/registrations/{esc(reg)}/seq", "seq"),
            [val(ctx, "pin", f"/order_of_filing/{i}", "registration")],
            code(ctx, "texts", f"/{esc(reg)}/prior_pct", "prior_pct")
            + [lit("%")],
            [val(ctx, key, b + "/arm", "arm")]]
    if "score_row" not in row:
        return head + halt_cells(ctx, reg, key, b)
    k = family_index(ctx, reg, str(row["arm"]))
    return head + score_cells(ctx, key, b) + [
        [lit("**"), val(ctx, key, b + "/score_row/verdict", "verdict"),
         lit("**")],
        code(ctx, "family", f"/rows/{k}/clears_bh_bar", "clears_bh_bar"),
        loao_cell(ctx, key, b),
        twin_cell(ctx, key, b, row),
        brk_cell(ctx, key, b, row)]


def n_run(family: dict) -> str:
    return str(sum(1 for r in family["rows"]
                   if r.get("clears_bh_bar") is not None))


def clears_true(family: dict) -> str:
    regs = [str(r["registration"]) for r in family["rows"]
            if r.get("clears_bh_bar") is True]
    return ", ".join(regs) if regs else "none"


def beside_lines(ctx: Ctx, d: Doc):
    fam = ctx.docs["family"]
    d.tpl([lit("- **m = `"), val(ctx, "family", "/family_m_declared",
                                 "m_declared", True),
           lit("` declared / `"), der("n_run", n_run(fam), col="n_run"),
           lit("` run** — N counts the FAMILY.json rows whose `clears_bh_bar` "
               "is not null. One fixed bar q/m = `"),
           val(ctx, "family", "/fdr_bar_q_over_m", "fdr_bar_q_over_m", True),
           lit("` (FAMILY.json `fdr_bar_q_over_m`), no step-up.")],
          "beside", what="m")
    d.tpl([lit("- `clears_bh_bar` is `true` on: **"),
           der("clears_true", clears_true(fam)), lit("**.")],
          "beside", what="clears_true")
    d.tpl([lit("- FAMILY.json `law`: "), val(ctx, "family", "/law")],
          "beside", what="law")
    for reg in ctx.order:
        key = "rows:" + reg
        j = scored_index(ctx, reg)
        row = ctx.docs[key]["rows"][j]
        b = f"/rows/{j}"
        if "score_row" not in row:
            d.tpl([lit("- **"), val(ctx, key, "/registration"),
                   lit("** HALTed at `"), val(ctx, key, b + "/at", None, True),
                   lit("`: its row prints FAMILY.json `scored_slots_halted` "
                       "verbatim and no point, CI or p. Its Tier-E arms are "
                       "report-only and are not in §0. The filed text, as the "
                       "rows file carries it: “"),
                   val(ctx, key, b + "/text_prescribes/1"), lit("”")],
                  "beside", what="halt", reg=reg)
    first = ctx.order[0]
    j0 = scored_index(ctx, first)
    d.tpl([lit("- **Haircut twin** (`beside.haircut_twin.twin_expectancy_r`; "
               "the two-sample row adds `twin_difference_r` as Δ): "),
           val(ctx, "rows:" + first,
               f"/rows/{j0}/beside/haircut_twin/law")],
          "beside", what="twin_law")
    for reg in ctx.order:
        key = "rows:" + reg
        j = scored_index(ctx, reg)
        row = ctx.docs[key]["rows"][j]
        sr = row.get("score_row")
        if sr is None or str(sr["loao_assets_present"]) == str(sr["loao_panels"]):
            continue
        s = f"/rows/{j}/score_row"
        d.tpl([lit("- **"), val(ctx, key, "/registration"),
               lit("** LOAO: `"), val(ctx, key, s + "/loao_assets_present",
                                      None, True),
               lit("` assets present of `"),
               val(ctx, key, s + "/loao_panels", None, True),
               lit("` declared panels; zero-campaign assets `"),
               val(ctx, key, s + "/loao_zero_campaign_assets", None, True),
               lit("`; the line of record reads `"),
               val(ctx, key, s + "/loao_line", None, True), lit("` — "),
               val(ctx, key, s + "/loao_zero_campaign_note")],
              "beside", what="loao_present", reg=reg)
    for reg in ctx.order:
        key = "rows:" + reg
        j = scored_index(ctx, reg)
        brk = ctx.docs[key]["rows"][j]["beside"].get("brk_sealed_row")
        if brk is None or brk["toll"].get("stamped") is False:
            continue
        h = f"/rows/{j}/beside/brk_sealed_row"
        d.tpl([lit("- **"), val(ctx, key, "/registration"),
               lit("** toll: "), val(ctx, key, h + "/toll_accounting_status"),
               lit(" Authority: "),
               val(ctx, key, h + "/toll_accounting/authority")],
              "beside", what="toll", reg=reg)


# ═════════════════════════════════════════════════════════════════ QUOTES
def find_lines(lines: list, first_pred, cont_pred, last: bool = False):
    starts = [i for i, ln in enumerate(lines) if first_pred(ln)]
    if not starts:
        return None
    i = starts[-1] if last else starts[0]
    j = i + 1
    while j < len(lines) and cont_pred(lines[j]):
        j += 1
    return i, j


def line_quote(ctx: Ctx, key: str, span) -> tuple:
    if span is None:
        HALT(f"the passage to quote is not in {src_rel(key)}")
    a, b = span
    return {"lines": [a + 1, b]}, "\n".join(ctx.lines[key][a:b])


def law3_span(lines: list):
    return find_lines(lines, lambda s: s.startswith(" 3 · registration texts"),
                      lambda s: s.startswith("     "))


def r01_span(lines: list):
    try:
        top = lines.index("### R0.1 · The interruption")
    except ValueError:
        return None
    sub = find_lines(lines[top:], lambda s: s.startswith("- `draft:registrations`"),
                     lambda s: s.startswith("  "))
    return None if sub is None else (top + sub[0], top + sub[1])


def plan_span(lines: list):
    return find_lines(lines, lambda s: s.startswith("`UNSEEN12 admitted = ("),
                      lambda s: s.strip() != "")


def lean_span(lines: list):
    return find_lines(lines, lambda s: s.startswith("- **PUMPFUN → PUMPUSDT**"),
                      lambda s: s.startswith("  "), last=True)


def paragraphs(t: str) -> list:
    out, pos = [], 0
    for part in t.split("\n\n"):
        out.append((pos, pos + len(part), part))
        pos += len(part) + 2
    return out


def text_quotes(ctx: Ctx) -> list:
    """(reg, start, end, text, kind): the P-SPR-2 superseded draft, then each
    paragraph that records R8 superseding R2."""
    texts = ctx.docs["texts"]
    out = []
    spr = [p for p in paragraphs(str(texts["P-SPR-2"]["text"]))
           if p[2].startswith("THE SUPERSEDED DRAFT")]
    if len(spr) != 1:
        HALT(f"P-SPR-2's text holds {len(spr)} superseded-draft paragraphs")
    out.append(("P-SPR-2",) + spr[0] + ("superseded draft",))
    for reg in ctx.order:
        hits = [p for p in paragraphs(str(texts[reg]["text"]))
                if "R8" in p[2] and "SUPERSEDES" in p[2] and "R2" in p[2]]
        if len(hits) > 1:
            HALT(f"{reg}'s text holds {len(hits)} R8-supersedes-R2 paragraphs")
        if hits:
            out.append((reg,) + hits[0] + ("R8 supersedes R2",))
    if len(out) < 2:
        HALT("no R8-supersedes-R2 panel paragraph in REGISTRATION_TEXTS.json")
    return out


# ═══════════════════════════════════════════════════════ THE ADMITTED LIST
def admission_order(ctx: Ctx) -> tuple:
    """(table A indices in panels.UNSEEN_admitted_stems order, table B indices
    = every other admission row in manifest order)."""
    man = ctx.docs["manifest"]
    rows = man["admission"]["rows"]
    by_stem = {str(r["stem"]): k for k, r in enumerate(rows)}
    unseen = [str(s) for s in man["panels"]["UNSEEN_admitted_stems"]]
    missing = [s for s in unseen if s not in by_stem]
    if missing:
        HALT(f"UNSEEN_admitted_stems {missing} have no admission row")
    a = [(u, by_stem[s]) for u, s in enumerate(unseen)]
    taken = {k for _, k in a}
    return a, [k for k in range(len(rows)) if k not in taken]


def admit_cells(ctx: Ctx, k: int) -> list:
    b = f"/admission/rows/{k}"
    return [[val(ctx, "manifest", b + "/asset", "asset")],
            code(ctx, "manifest", b + "/stem", "stem"),
            [val(ctx, "manifest", b + "/venue", "venue")],
            code(ctx, "manifest", b + "/closed_4h_bars", "closed_4h_bars"),
            code(ctx, "manifest", b + "/admitted", "admitted")]


def admitted_section(ctx: Ctx, d: Doc):
    man = ctx.docs["manifest"]
    d.add("### 0.2 · The admitted list", "",
          "*REPORT-ONLY — transcribed from `data/STAGE_D_MANIFEST.json` "
          "`admission` and `panels`; it printed before any scoring and is "
          "P-GEN-1's panel.*", "")
    d.tpl([lit("- Admission rule (`admission.rule`): "),
           val(ctx, "manifest", "/admission/rule")], "admit_rule")
    exc = man["admission"]["excluded"]
    if exc:
        for x, e in enumerate(exc):
            d.tpl([lit("- EXCLUDED: ")] + [
                p for kk in sorted(e) for p in
                (lit(f"{kk} "), val(ctx, "manifest",
                                    f"/admission/excluded/{x}/{esc(kk)}",
                                    "excluded"), lit(" · "))],
                "admit_excluded")
    else:
        d.tpl([lit("- Excluded: "), der("excluded_none",
                                      "none — `admission.excluded` is empty")],
              "admit_excluded")
    d.add("")
    loc, text = line_quote(ctx, "plan", plan_span(ctx.lines["plan"]))
    d.quote(f"Why the twelve — `REGISTRATION_PLAN.md` {loc_label(loc)}:",
            "plan", loc, text, "bq")
    a, rest = admission_order(ctx)
    d.add("**The ADMITTED LIST — P-GEN-1's panel, UNSEEN12 "
          "(`panels.UNSEEN_admitted_stems`, in that order):**", "",
          AHEAD_A, "|---" * len(ACOLS) + "|")
    for u, k in a:
        d.tpl(row_parts(admit_cells(ctx, k)), "admit_row", table="A",
              stem_ptr=f"/panels/UNSEEN_admitted_stems/{u}")
    d.add("", "**The other admission rows — admitted, not in P-GEN-1's "
          "panel:**", "", AHEAD_B, "|---" * (len(ACOLS) + 1) + "|")
    classic = {str(s) for s in man["panels"]["CLASSIC5"]}
    for k in rest:
        stem = str(man["admission"]["rows"][k]["stem"])
        d.tpl(row_parts(admit_cells(ctx, k) + [
            [der("classic5_member", "CLASSIC5" if stem in classic else DASH,
                 arg=stem, col="panel")]]), "admit_row", table="B")
    d.add("")
    loc, text = line_quote(ctx, "rulings", lean_span(ctx.lines["rulings"]))
    d.quote(f"The venue / stem leans still open — `OPERATOR_RULINGS.md` "
            f"{loc_label(loc)}:", "rulings", loc, text, "bq")


# ═══════════════════════════════════════════════════════ THE FORWARD STRIP
def strip_begin(b: bytes) -> str:
    return (f"<!-- BEGIN INLINE {STRIP_TAG} sha256={sha256(b)} "
            f"bytes={len(b)} -->")


def inline_strip(b: bytes) -> bytes:
    return b


def build_stamp() -> str:
    return (f"<!-- S0_VERDICTS.md · TIER-C10 CLOSE §0 fragment · built by "
            f"{SCRIPT_REL} · splice over BUILD_DRAFT.md \"## 0 · VERDICTS\" at "
            f"CLOSE; this script never edits BUILD_DRAFT.md -->")


# ═════════════════════════════════════════════════════════════════ ASSEMBLY
def assemble(ctx: Ctx) -> tuple:
    d = Doc()
    pin = ctx.docs["pin"]
    d.add(build_stamp(), "## 0 · VERDICTS", "")
    if ctx.strip is None:
        d.add("> **INCOMPLETE — DO NOT SPLICE.** `close/FORWARD_STRIP.md` was "
              "absent when this fragment was built; F-S0-STRIP is RED.", "")
    d.add("> **REPORT-ONLY TRANSCRIPTION.** Every value in this section is "
          "copied string-for-string, at source precision, from the file and "
          "field that `S0_VERDICTS.json` records beside it; F-S0-READ re-reads "
          "each one. Nothing here is scored, re-scored, rounded or re-chosen. "
          "The verdicts are those of record: `scores/<REG>.rows.json` (the one "
          "arm with `scored_in_family` true — its `score_row` and its "
          "`beside`) and `scores/FAMILY.json` (`clears_bh_bar`).", "")
    d.tpl([lit("Corridor as-of of record `"),
           val(ctx, "pin", "/as_of_of_record", None, True),
           lit("` · registry len `"), val(ctx, "pin", "/registry_len", None, True),
           lit("` · registry head `"),
           val(ctx, "pin", "/registry_head", None, True),
           lit("` · seed `"), val(ctx, "pin", "/seed", None, True),
           lit("` (`REGISTRY_PIN.json`).")], "corridor")
    d.add("", "### 0.1 · Six registered rows, in order of filing", "",
          "*REPORT-ONLY — one row per registration, its scored arm only; the "
          "Tier-E arms stay in `scores/<REG>.rows.json` and gate nothing.*", "",
          VHEADER, "|---" * len(VCOLS) + "|")
    order = filing_order(pin)
    if order != ctx.order:
        HALT("the filing order moved between two reads of REGISTRY_PIN.json")
    for i, reg in enumerate(order):
        d.tpl(row_parts(verdict_cells(ctx, i, reg)), "verdict_row", reg=reg)
    d.add("", "**Beside the table**", "")
    beside_lines(ctx, d)
    d.add("", "#### LAW 3's beside-print — empty, by fact", "")
    loc, text = line_quote(ctx, "contract", law3_span(ctx.lines["contract"]))
    d.quote(f"LAW 3 — `exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md` "
            f"{loc_label(loc)}:", "contract", loc, text, "fence")
    loc, text = line_quote(ctx, "draft", r01_span(ctx.lines["draft"]))
    d.quote("**Empty by fact, not by omission.** The interrupted run filed no "
            "registration, so it computed no verdict: there is nothing to "
            "re-compute and print beside the six fresh rows. The record — "
            f"`BUILD_DRAFT.md` §R0.1, {loc_label(loc)}:",
            "draft", loc, text, "bq")
    d.add("#### The superseded draft and the supersession of record", "",
          "*Quoted verbatim from `REGISTRATION_TEXTS.json`; the texts are "
          "frozen and nothing here re-words them.*", "")
    for reg, a, b, text, kind in text_quotes(ctx):
        loc = {"reg": reg, "chars": [a, b]}
        d.quote(f"**{reg} — {kind}** — {loc_label(loc)}:", "texts", loc,
                text, "bq")
    admitted_section(ctx, d)
    d.add("### 0.3 · The forward strip", "",
          "*REPORT-ONLY — the contract's FORWARD STRIP: printed, labeled, never "
          "scored. Inlined byte-for-byte from "
          f"`{FIXED_SOURCES['strip']}` (F-S0-STRIP).*", "")
    head = "\n".join(d.lines) + "\n"
    if ctx.strip is None:
        md = head + f"<!-- ABSENT {STRIP_TAG} -->\n**ABSENT.**\n"
        strip_meta = {"path": FIXED_SOURCES["strip"], "present": False}
    else:
        try:
            ctx.strip.decode("utf-8")
        except UnicodeDecodeError:
            HALT(f"{STRIP_TAG} is not UTF-8")
        md = (head + strip_begin(ctx.strip) + "\n"
              + inline_strip(ctx.strip).decode("utf-8") + STRIP_END + "\n")
        strip_meta = {"path": FIXED_SOURCES["strip"], "present": True,
                      "sha256": sha256(ctx.strip), "bytes": len(ctx.strip)}
    mdb = md.encode("utf-8")
    inputs = {}
    for key in (["pin"] + ["rows:" + r for r in ctx.order]
                + ["family", "texts", "manifest"] + list(TEXT_KEYS)):
        inputs[key] = {"path": src_rel(key), "sha256": sha256(ctx.raw[key]),
                       "bytes": len(ctx.raw[key])}
    meta = {
        "fragment": "TIER-C10 CLOSE §0 — six verdict rows + the admitted list "
                    "+ the forward strip",
        "contract": "exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md:131",
        "label": "REPORT-ONLY TRANSCRIPTION — scores nothing, gates nothing; "
                 "every value at source precision",
        "builder": SCRIPT_REL,
        "splice": "over BUILD_DRAFT.md '## 0 · VERDICTS' at CLOSE; this "
                  "script never edits BUILD_DRAFT.md",
        "md": {"path": CLOSE_REL + "/" + MD_NAME, "sha256": sha256(mdb),
               "bytes": len(mdb)},
        "inputs": inputs,
        "forward_strip": strip_meta,
        "order_of_filing": list(ctx.order),
        "verdict_header": VHEADER,
        "lines": d.recs,
        "quotes": d.quotes,
    }
    jsb = (json.dumps(meta, indent=1, ensure_ascii=False) + "\n").encode("utf-8")
    return mdb, jsb, meta


def build(over: dict | None = None) -> tuple:
    return assemble(Ctx(over))


def guard_out(path: Path, out_dir: Path):
    p = Path(path).resolve()
    if p.parent != Path(out_dir).resolve() or p.name not in OUTPUT_NAMES:
        HALT(f"refused to write {p.name}: the builder writes only "
             f"{', '.join(OUTPUT_NAMES)} in its out dir")


def write_outputs(mdb: bytes, jsb: bytes, out_dir: Path):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    for name, b in ((MD_NAME, mdb), (JSON_NAME, jsb)):
        guard_out(out_dir / name, out_dir)
        (out_dir / name).write_bytes(b)


TABLE_CODE_PATH = (
    "parse_tok", "render", "esc", "resolve", "Ctx", "lit", "val", "code",
    "der", "row_parts", "Doc", "quote_lines", "family_index", "scored_index",
    "score_cells", "loao_cell", "twin_cell", "brk_cell", "halt_cells",
    "verdict_cells", "n_run", "clears_true", "beside_lines", "admission_order",
    "admit_cells", "admitted_section", "inline_strip", "strip_begin",
    "assemble")


# ══════════════════════════════════════════════════════════════ THE FIXTURES
_TMP: list = []


@contextlib.contextmanager
def tmpdir():
    d = tempfile.mkdtemp(prefix="tc10_s0_fx_")
    _TMP.append(d)
    try:
        yield Path(d)
    finally:
        shutil.rmtree(d, ignore_errors=True)


def clean(msg) -> str:
    s = str(msg)
    for d in _TMP:
        for form in (str(Path(d).resolve()), str(d),
                     str(d).replace("/private/", "/", 1)):
            s = s.replace(form, "<tmp>")
    return s


@contextlib.contextmanager
def mutated(name: str, value):
    mod = sys.modules[__name__]
    old = getattr(mod, name)
    setattr(mod, name, value)
    try:
        yield
    finally:
        setattr(mod, name, old)


class Fresh:
    """THE INDEPENDENT READ: plain json.loads over the canonical files, each
    value re-spelled by the writer's own json.dumps — never through Tok."""

    def __init__(self):
        self.docs, self.text = {}, {}

    def doc(self, key: str):
        if key not in self.docs:
            self.docs[key] = json.loads(
                (ROOT / src_rel(key)).read_text("utf-8"))
        return self.docs[key]

    def lines(self, key: str) -> list:
        if key not in self.text:
            self.text[key] = (ROOT / src_rel(key)).read_text("utf-8").split("\n")
        return self.text[key]

    def spell(self, key: str, ptr: str) -> str:
        v = resolve(self.doc(key), ptr)
        return v if isinstance(v, str) else json.dumps(v)

    def derived(self, p: dict) -> str:
        fam = self.doc("family")
        if p["what"] == "n_run":
            return str(len([r for r in fam["rows"]
                            if r.get("clears_bh_bar") is not None]))
        if p["what"] == "clears_true":
            regs = [r["registration"] for r in fam["rows"]
                    if r.get("clears_bh_bar") is True]
            return ", ".join(regs) if regs else "none"
        if p["what"] == "excluded_none":
            exc = self.doc("manifest")["admission"]["excluded"]
            return "none — `admission.excluded` is empty" if exc == [] else \
                "<excluded is NOT empty>"
        if p["what"] == "classic5_member":
            c5 = self.doc("manifest")["panels"]["CLASSIC5"]
            return "CLASSIC5" if p["arg"] in c5 else DASH
        return "<unknown derived value>"


def md_lines_of(mdb: bytes) -> list:
    return mdb.decode("utf-8").split("\n")


def head_region(lines: list) -> list:
    for i, ln in enumerate(lines):
        if ln.startswith("<!-- BEGIN INLINE ") or ln.startswith("<!-- ABSENT "):
            return lines[:i]
    return lines


def check_read(mdb: bytes, meta: dict, fr: Fresh) -> tuple:
    bad, n_vals, lines = [], 0, md_lines_of(mdb)
    rec_lines = set()
    for rec in meta["lines"]:
        rec_lines.add(rec["line"])
        want = []
        for p in rec["parts"]:
            if p["t"] == "lit":
                want.append(p["s"])
                continue
            if p["t"] == "val":
                n_vals += 1
                if p["path"] != src_rel(p["src"]):
                    bad.append(f"line {rec['line']}: {p['ptr']} recorded from "
                               f"{p['path']}, not {src_rel(p['src'])}")
                got = fr.spell(p["src"], p["ptr"])
            else:
                n_vals += 1
                got = fr.derived(p)
            if got != p["s"]:
                bad.append(f"line {rec['line']}: {p['src'] if 'src' in p else p['what']}"
                           f"{p.get('ptr', '')} printed {p['s']!r}, source reads "
                           f"{got!r}")
            want.append(got)
        w = "".join(want)
        printed = lines[rec["line"]] if rec["line"] < len(lines) else None
        if printed != w:
            bad.append(f"line {rec['line']}: printed line differs from the "
                       f"fresh re-read")
    for q in meta["quotes"]:
        if "lines" in q["loc"]:
            a, b = q["loc"]["lines"]
            src = "\n".join(fr.lines(q["src"])[a - 1:b])
        else:
            a, b = q["loc"]["chars"]
            src = fr.doc("texts")[q["loc"]["reg"]]["text"][a:b]
        if src != q["text"]:
            bad.append(f"quote from {q['path']} {q['loc']} is not verbatim")
        s, e = q["md_lines"]
        if lines[s:e] != quote_lines(src, q["style"]):
            bad.append(f"quote at md lines {s}-{e} is not the source's bytes")
        if loc_label(q["loc"]) not in lines[q["hdr_line"]]:
            bad.append(f"quote header at md line {q['hdr_line']} mis-cites")
    for i, ln in enumerate(head_region(lines)):
        if (ln.startswith("| ") and ln not in (VHEADER, AHEAD_A, AHEAD_B)
                and i not in rec_lines):
            bad.append(f"md line {i} is a table row no source record covers")
    return bad, n_vals


def table_rows(lines: list, header: str) -> list:
    if header not in lines:
        return []
    i = lines.index(header) + 2
    out = []
    while i < len(lines) and lines[i].startswith("| "):
        out.append(lines[i][2:-2].split(" | "))
        i += 1
    return out


def check_six(mdb: bytes, meta: dict, fr: Fresh) -> list:
    bad = []
    rows = table_rows(md_lines_of(mdb), VHEADER)
    pin = fr.doc("pin")
    want = pin["order_of_filing"]
    got = [c[1] if len(c) > 1 else "?" for c in rows]
    if len(rows) != 6:
        bad.append(f"{len(rows)} verdict rows printed, not 6")
    if len(want) != pin["registry_len"]:
        bad.append("REGISTRY_PIN order_of_filing disagrees with registry_len")
    if got != want:
        bad.append(f"printed order {got} != REGISTRY_PIN order_of_filing {want}")
    for c in rows:
        if len(c) != len(VCOLS):
            bad.append(f"row {c[:2]} has {len(c)} cells, not {len(VCOLS)}")
        elif c[1] in pin["registrations"] and \
                c[0] != f"`{pin['registrations'][c[1]]['seq']}`":
            bad.append(f"row {c[1]} prints seq {c[0]}")
    if meta["order_of_filing"] != want:
        bad.append("S0_VERDICTS.json order_of_filing != REGISTRY_PIN")
    return bad


def by_col(rec: dict) -> dict:
    return {p["col"]: p["s"] for p in rec["parts"] if "col" in p}


def check_bar(meta: dict) -> tuple:
    bad, seen = [], []
    D = decimal.Decimal
    bars = [p["s"] for rec in meta["lines"] if rec.get("what") == "m"
            for p in rec["parts"] if p.get("col") == "fdr_bar_q_over_m"]
    if len(bars) != 1:
        return [f"{len(bars)} printed q/m bars, not 1"], seen
    bar = D(bars[0])
    for rec in meta["lines"]:
        if rec["kind"] != "verdict_row":
            continue
        c = by_col(rec)
        clr = c.get("clears_bh_bar")
        if clr not in ("true", "false"):
            continue
        p, lo, hi = D(c["p_one_sided"]), D(c["ci_lo"]), D(c["ci_hi"])
        above, lbar = int(c["loao_above_of_record"]), int(c["loao_bar_above_half"])
        seen.append(f"{rec['reg']}: clears {clr}, p {c['p_one_sided']} "
                    f"{'<=' if p <= bar else '>'} bar, CI "
                    f"[{c['ci_lo']}, {c['ci_hi']}], LOAO {above} vs {lbar}")
        if clr == "true":
            if p > bar:
                bad.append(f"{rec['reg']}: clears true but p {p} > bar {bar}")
            if lo <= 0:
                bad.append(f"{rec['reg']}: clears true but the CI "
                           f"[{lo}, {hi}] does not lie above 0")
            if above < lbar:
                bad.append(f"{rec['reg']}: clears true but LOAO {above} < "
                           f"bar {lbar}")
        elif p <= bar:
            bad.append(f"{rec['reg']}: clears false but p {p} <= bar {bar}")
    return bad, seen


def check_halt(mdb: bytes, meta: dict, fr: Fresh) -> list:
    bad = []
    reg = "P-BE-1"
    recs = [r for r in meta["lines"] if r["kind"] == "verdict_row"
            and r.get("reg") == reg]
    if len(recs) != 1:
        return [f"{len(recs)} {reg} rows printed, not 1"]
    rec = recs[0]
    line = md_lines_of(mdb)[rec["line"]]
    cells = line[2:-2].split(" | ")
    if len(cells) != len(VCOLS):
        return [f"{reg} row has {len(cells)} cells"]
    for name in ("n", "point", "[CI lo, CI hi]", "p (one-sided)"):
        cell = cells[VCOLS.index(name)]
        if cell != DASH:
            bad.append(f"{reg} shows {name} = {cell!r}")
    for p in rec["parts"]:
        if p["t"] == "val" and ("/score_row/" in p["ptr"]
                                or "/haircut_twin/" in p["ptr"]):
            bad.append(f"{reg} row reads a result field {p['ptr']}")
    halt = fr.doc("family")["scored_slots_halted"].get(reg)
    if cells[VCOLS.index("verdict")] != halt:
        bad.append(f"{reg} verdict cell is not FAMILY.json scored_slots_halted "
                   f"verbatim")
    rows = fr.doc("rows:" + reg)["rows"]
    filed = [r.get("halt") for r in rows if r.get("scored_in_family") is True]
    if filed != [halt]:
        bad.append(f"the rows file's halt {filed} != FAMILY.json's")
    for r in rows:
        sr = r.get("score_row")
        if not sr:
            continue
        for f in ("ci_point", "ci_lo", "ci_hi", "p_one_sided"):
            tok = json.dumps(sr[f])
            if tok in line:
                bad.append(f"{reg} row carries Tier-E {r['arm']} {f} {tok}")
    return bad


def check_admit(mdb: bytes, fr: Fresh) -> list:
    bad = []
    lines = md_lines_of(mdb)
    man = fr.doc("manifest")
    rows = man["admission"]["rows"]
    unseen = man["panels"]["UNSEEN_admitted_stems"]

    def spell(r):
        return [r["asset"], f"`{r['stem']}`", r["venue"],
                f"`{json.dumps(r['closed_4h_bars'])}`",
                f"`{json.dumps(r['admitted'])}`"]
    by_stem = {r["stem"]: r for r in rows}
    want_a = [spell(by_stem[s]) for s in unseen]
    want_b = [spell(r) for r in rows if r["stem"] not in unseen]
    got_a = table_rows(lines, AHEAD_A)
    got_b = [c[:len(ACOLS)] for c in table_rows(lines, AHEAD_B)]
    if got_a != want_a:
        bad.append(f"UNSEEN12 table: {len(got_a)} rows printed vs {len(want_a)} "
                   f"in panels.UNSEEN_admitted_stems order; differ at "
                   f"{[w[1] for w in want_a if w not in got_a]}")
    if got_b != want_b:
        bad.append(f"other-rows table: {len(got_b)} printed vs {len(want_b)}; "
                   f"missing {[w[1] for w in want_b if w not in got_b]}")
    if len(got_a) + len(got_b) != len(rows):
        bad.append(f"{len(got_a) + len(got_b)} admission rows printed, "
                   f"manifest holds {len(rows)}")
    if any(c[4] != "`true`" for c in got_a):
        bad.append("a row of P-GEN-1's panel prints admitted != true")
    exc = man["admission"]["excluded"]
    if exc == [] and "- Excluded: none — `admission.excluded` is empty" not in lines:
        bad.append("the empty excluded list is not printed as such")
    if exc and sum(1 for ln in lines if ln.startswith("- EXCLUDED: ")) != len(exc):
        bad.append("excluded assets not each named")
    return bad


def check_strip(mdb: bytes, strip_path: Path) -> list:
    if not Path(strip_path).is_file():
        return [f"{STRIP_TAG} is ABSENT"]
    b = Path(strip_path).read_bytes()
    begin = (strip_begin(b) + "\n").encode("utf-8")
    whole = begin + b + STRIP_END.encode("utf-8")
    bad = []
    if mdb.count(b"<!-- BEGIN INLINE ") != 1:
        bad.append("not exactly one inline marker")
    if mdb.find(whole) < 0:
        bad.append(f"{STRIP_TAG} ({len(b)} bytes, sha256 {sha256(b)[:16]}…) is "
                   f"not byte-inlined between its markers")
    return bad


FLOAT_CALLS = {"float", "round", "format"}


def check_notype(src: str) -> list:
    bad = []
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and type(node.value) in (float, complex):
            bad.append(f"float literal {node.value!r} at line {node.lineno}")
    found = set()
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)) and \
                node.name in TABLE_CODE_PATH:
            found.add(node.name)
            for sub in ast.walk(node):
                if isinstance(sub, ast.Call) and isinstance(sub.func, ast.Name) \
                        and sub.func.id in FLOAT_CALLS:
                    bad.append(f"{sub.func.id}() in {node.name} at line "
                               f"{sub.lineno}")
                if isinstance(sub, ast.FormattedValue) and sub.format_spec:
                    bad.append(f"a format spec in {node.name} at line "
                               f"{sub.lineno}")
    missing = sorted(set(TABLE_CODE_PATH) - found)
    if missing:
        bad.append(f"table-path names not found for the scan: {missing}")
    return bad


STDLIB_OK = {"__future__", "argparse", "ast", "contextlib", "decimal",
             "hashlib", "json", "os", "shutil", "subprocess", "sys",
             "tempfile", "pathlib"}
FORBIDDEN = {"score", "finish_family", "register", "_mark_scored",
             "load_klines", "load_asof", "publish_exchange"}


def check_closure(src: str) -> list:
    bad = []
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, ast.Import):
            for a in node.names:
                if a.name.split(".")[0] not in STDLIB_OK:
                    bad.append(f"import {a.name} (line {node.lineno})")
        elif isinstance(node, ast.ImportFrom):
            if (node.module or "").split(".")[0] not in STDLIB_OK:
                bad.append(f"from {node.module} import … (line {node.lineno})")
        elif isinstance(node, ast.Attribute) and node.attr in FORBIDDEN:
            bad.append(f".{node.attr} (line {node.lineno})")
        elif isinstance(node, ast.Name) and node.id in FORBIDDEN:
            bad.append(f"{node.id} (line {node.lineno})")
    return bad


def plant(src: str, fn: str, stmt: str) -> str:
    tree = ast.parse(src)
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == fn:
            node.body.insert(0, ast.parse(stmt).body[0])
            return ast.unparse(tree)
    raise RuntimeError(f"no function {fn} to plant into")


def perturb_copy(src: Path, dst: Path, ptr: str, new_tok: str):
    """Rewrite ONE field in a copy, at the text level, and prove nothing else
    moved."""
    text = Path(src).read_text("utf-8")
    base = json.loads(text)
    parent_ptr, key = ptr.rsplit("/", 1)
    pat = f'"{key}": {json.dumps(resolve(base, ptr))}'
    start = 0
    while True:
        i = text.find(pat, start)
        if i < 0:
            raise RuntimeError(f"perturb: no occurrence of {pat} is {ptr}")
        cand = text[:i] + f'"{key}": {new_tok}' + text[i + len(pat):]
        d = json.loads(cand)
        if json.dumps(resolve(d, ptr)) == new_tok:
            resolve(d, parent_ptr)[key] = resolve(base, ptr)
            if d == base:
                Path(dst).write_text(cand, "utf-8")
                return
        start = i + 1


def bump(tok: str) -> str:
    return tok[:-1] + ("2" if tok[-1] == "1" else "1")


# ── the legs: each returns (ok, lines) for the real build, and a list of
#    (break name, ok_under_break, detail) — a break must make ok False.
def leg_read(real, fr):
    mdb, jsb, meta = real
    bad, n = check_read(mdb, meta, fr)
    lines = [f"real build: {n} printed values and {len(meta['quotes'])} quotes "
             f"re-read by an independent route; {len(bad)} differ"]
    lines += ["  " + b for b in bad[:12]]
    breaks = []
    reg = meta["order_of_filing"][0]
    j = [k for k, r in enumerate(fr.doc("rows:" + reg)["rows"])
         if r.get("scored_in_family")][0]
    ptr = f"/rows/{j}/score_row/ci_lo"
    old = fr.spell("rows:" + reg, ptr)
    with tmpdir() as t:
        cp = t / f"{reg}.rows.json"
        perturb_copy(ROOT / rows_rel(reg), cp, ptr, bump(old))
        m2, _, meta2 = build({"rows:" + reg: cp})
        b2, _ = check_read(m2, meta2, fr)
    breaks.append((f"ci_lo of {reg}'s scored arm perturbed {old} -> "
                   f"{bump(old)} in a COPY of its rows file", not b2,
                   b2[0] if b2 else "no difference seen"))
    return not bad, lines, breaks


def leg_six(real, fr):
    mdb, jsb, meta = real
    bad = check_six(mdb, meta, fr)
    order = table_rows(md_lines_of(mdb), VHEADER)
    lines = [f"real build: {len(order)} rows · order "
             f"{' → '.join(c[1] for c in order)}"] + ["  " + b for b in bad]
    orig = filing_order
    with mutated("filing_order",
                 lambda pin: [r for r in orig(pin) if r != "P-BE-1"]):
        m2, _, meta2 = build()
    b2 = check_six(m2, meta2, fr)
    return not bad, lines, [("P-BE-1 dropped from the filing order", not b2,
                             b2[0] if b2 else "no difference seen")]


def leg_bar(real, fr):
    mdb, jsb, meta = real
    bad, seen = check_bar(meta)
    lines = ["real build: " + s for s in seen] + ["  " + b for b in bad]
    fam = fr.doc("family")
    k = [i for i, r in enumerate(fam["rows"]) if r["registration"] == "P-GEN-1"
         and r.get("scored_in_family")][0]
    with tmpdir() as t:
        cp = t / "FAMILY.json"
        perturb_copy(ROOT / src_rel("family"), cp, f"/rows/{k}/clears_bh_bar",
                     "true")
        _, _, meta2 = build({"family": cp})
        b2, _ = check_bar(meta2)
    return not bad, lines, [("P-GEN-1's clears_bh_bar set true in a COPY of "
                             "FAMILY.json", not b2,
                             b2[0] if b2 else "no difference seen")]


def leg_halt(real, fr):
    mdb, jsb, meta = real
    bad = check_halt(mdb, meta, fr)
    lines = [f"real build: P-BE-1 prints no n / point / CI / p; its verdict "
             f"cell is FAMILY.json scored_slots_halted verbatim; "
             f"{len(bad)} problems"] + ["  " + b for b in bad]

    def sab(ctx, reg, key, b):
        doc = ctx.docs[key]
        j2 = [j for j, r in enumerate(doc["rows"]) if "score_row" in r][0]
        return score_cells(ctx, key, f"/rows/{j2}") + [
            [val(ctx, "family", "/scored_slots_halted/" + esc(reg), "halt")],
            [lit(DASH)], [lit(DASH)], [lit(DASH)], [lit(DASH)]]
    with mutated("halt_cells", sab):
        m2, _, meta2 = build()
    b2 = check_halt(m2, meta2, fr)
    return not bad, lines, [("P-BE-1's Tier-E A2 numbers injected into its "
                             "row", not b2, b2[0] if b2 else "no difference seen")]


def leg_admit(real, fr):
    mdb, jsb, meta = real
    bad = check_admit(mdb, fr)
    lines_ = md_lines_of(mdb)
    a, b = table_rows(lines_, AHEAD_A), table_rows(lines_, AHEAD_B)
    lines = [f"real build: {len(a)} rows in P-GEN-1's panel + {len(b)} other "
             f"admission rows = {len(a) + len(b)} vs manifest "
             f"{len(fr.doc('manifest')['admission']['rows'])}"] + \
        ["  " + x for x in bad]
    orig = admission_order

    def sab(ctx):
        aa, rest = orig(ctx)
        return aa[:-1], rest
    with mutated("admission_order", sab):
        m2, _, _ = build()
    b2 = check_admit(m2, fr)
    return not bad, lines, [("the last asset dropped from the admitted list",
                             not b2, b2[0] if b2 else "no difference seen")]


def leg_strip(real, fr):
    mdb, jsb, meta = real
    sp = ROOT / FIXED_SOURCES["strip"]
    bad = check_strip(mdb, sp)
    if sp.is_file():
        b = sp.read_bytes()
        lines = [f"real build: {STRIP_TAG} present, {len(b)} bytes, sha256 "
                 f"{sha256(b)}; {len(bad)} problems"]
    else:
        lines = [f"real build: {STRIP_TAG} ABSENT — the fragment is "
                 f"INCOMPLETE and must not be spliced"]
    lines += ["  " + x for x in bad]
    breaks = []
    with tmpdir() as t:
        gone = t / "FORWARD_STRIP.md"
        m2, _, _ = build({"strip": gone})
        b2 = check_strip(m2, gone)
        breaks.append(("the strip absent", not b2,
                       b2[0] if b2 else "no difference seen"))
        if sp.is_file():
            syn, note = sp, "the strip of record"
        else:
            syn = t / "SYN_STRIP.md"
            syn.write_bytes("SYNTHETIC FIXTURE STRIP — not the strip of "
                            "record.\n".encode("utf-8"))
            note = "a SYNTHETIC strip (the strip of record is absent)"
        with mutated("inline_strip", lambda bb: bb[:-1]):
            m3, _, _ = build({"strip": syn})
        b3 = check_strip(m3, syn)
        breaks.append((f"the inlined bytes one byte short ({note})", not b3,
                       b3[0] if b3 else "no difference seen"))
    return not bad, lines, breaks


def leg_notype(real, fr):
    src = Path(__file__).read_text("utf-8")
    bad = check_notype(src)
    lines = [f"real module: AST scan of the whole module for float literals, "
             f"and of {len(TABLE_CODE_PATH)} table-path definitions for "
             f"float()/round()/format specs; {len(bad)} found"] + \
        ["  " + b for b in bad]
    b1 = check_notype(plant(src, "verdict_cells", "_planted = 2" + "." + "5"))
    b2 = check_notype(plant(src, "render", "_planted = round(len('ab'), 4)"))
    return not bad, lines, [
        ("a float literal planted in verdict_cells", not b1,
         b1[0] if b1 else "no difference seen"),
        ("a round() planted in render", not b2,
         b2[0] if b2 else "no difference seen")]


def leg_closure(real, fr):
    src = Path(__file__).read_text("utf-8")
    bad = check_closure(src)
    lines = [f"real module: imports within the stdlib allowlist "
             f"({len(STDLIB_OK)} names); no scorer, registrar or bar loader "
             f"named; {len(bad)} found"] + ["  " + b for b in bad]
    b1 = check_closure(plant(src, "assemble", "import tierc10_panel as TP"))
    b2 = check_closure(plant(src, "assemble", "TP.score(None)"))
    return not bad, lines, [
        ("an estate import planted in assemble", not b1,
         b1[0] if b1 else "no difference seen"),
        ("a TP.score call planted in assemble", not b2,
         b2[0] if b2 else "no difference seen")]


def run_writes(writer) -> list:
    draft = ROOT / FIXED_SOURCES["draft"]
    before = sha256(draft.read_bytes())
    with tmpdir() as t:
        mdb, jsb, _ = build()
        writer(mdb, jsb, t)
        names = sorted(p.name for p in t.iterdir())
    bad = []
    if names != sorted([MD_NAME, JSON_NAME]):
        bad.append(f"the build wrote {names}, not exactly "
                   f"{sorted([MD_NAME, JSON_NAME])}")
    if sha256(draft.read_bytes()) != before:
        bad.append("BUILD_DRAFT.md's sha moved across a build")
    return bad


def leg_writes(real, fr):
    bad = run_writes(write_outputs)
    try:
        guard_out(ROOT / FIXED_SOURCES["draft"], CLOSE_DIR)
        bad.append("the writer's guard let BUILD_DRAFT.md through")
    except Halt:
        pass
    lines = [f"real writer: exactly {MD_NAME} + {JSON_NAME} written; "
             f"BUILD_DRAFT.md sha unchanged across a build; the guard refuses "
             f"BUILD_DRAFT.md; {len(bad)} problems"] + ["  " + b for b in bad]

    def sab(mdb, jsb, out_dir):
        write_outputs(mdb, jsb, out_dir)
        (Path(out_dir) / "EXTRA.md").write_bytes(b"stray")
    b2 = run_writes(sab)
    return not bad, lines, [("a writer that drops a third file", not b2,
                             b2[0] if b2 else "no difference seen")]


def det_problems(one: tuple, two: tuple) -> list:
    bad = []
    if one[0] != two[0]:
        bad.append(f"MD differs: {sha256(one[0])[:16]}… vs {sha256(two[0])[:16]}…")
    if one[1] != two[1]:
        bad.append(f"JSON differs: {sha256(one[1])[:16]}… vs "
                   f"{sha256(two[1])[:16]}…")
    return bad


def leg_det(real, fr):
    mdb, jsb, meta = real
    again = build()
    bad = det_problems((mdb, jsb), again[:2])
    with tmpdir() as t:
        r = subprocess.run([sys.executable, str(Path(__file__).resolve()),
                            "--build-only", "--out-dir", str(t)],
                           capture_output=True, text=True, cwd=str(ROOT))
        if r.returncode != 0:
            bad.append("the fresh-process build failed: "
                       + clean(r.stderr.strip().splitlines()[-1:]))
        else:
            bad += ["fresh process: " + x for x in det_problems(
                (mdb, jsb), ((t / MD_NAME).read_bytes(),
                             (t / JSON_NAME).read_bytes()))]
    lines = [f"real: two in-process builds and one fresh-process build; MD "
             f"sha256 {sha256(mdb)}, JSON sha256 {sha256(jsb)}; "
             f"{len(bad)} differ"] + ["  " + b for b in bad]
    counter = iter(range(1, 1000))
    orig = build_stamp
    with mutated("build_stamp", lambda: orig() + f" #{next(counter)}"):
        b2 = det_problems(build()[:2], build()[:2])
    return not bad, lines, [("a build stamp that counts", not b2,
                             b2[0] if b2 else "no difference seen")]


LEGS = (
    ("F-S0-READ", "any printed value differs string-for-string from a fresh "
                  "read of its source field", leg_read),
    ("F-S0-SIX", "there are not exactly 6 rows in REGISTRY_PIN order",
     leg_six),
    ("F-S0-BAR", "clears_bh_bar is true where p > fdr_bar_q_over_m, or where "
                 "the CI straddles 0 (or lies below it), or where LOAO is below "
                 "its bar — or false where p <= the bar", leg_bar),
    ("F-S0-HALT", "P-BE-1 shows a point, CI or p (or any result field, or a "
                  "verdict cell other than FAMILY.json's HALT text)", leg_halt),
    ("F-S0-ADMIT", "the admitted list differs from STAGE_D_MANIFEST "
                   "admission", leg_admit),
    ("F-S0-STRIP", "close/FORWARD_STRIP.md is absent or not byte-inlined",
     leg_strip),
    ("F-S0-NOTYPE", "a float literal appears in the module, or a float() / "
                    "round() call or a format spec on the table code path "
                    "(AST scan)", leg_notype),
    ("F-S0-CLOSURE", "the module imports outside the stdlib allowlist or "
                     "names a scorer, registrar or bar loader", leg_closure),
    ("F-S0-WRITES", "a build writes anything but the two named outputs, or "
                    "BUILD_DRAFT.md's sha moves across a build", leg_writes),
    ("F-DET", "two builds (in-process, and a fresh process) are not "
              "byte-identical", leg_det),
)


def run_fixtures(real: tuple) -> tuple:
    out, green, n_breaks, red_breaks = [], 0, 0, 0
    fr = Fresh()
    for name, fails_if, fn in LEGS:
        out.append("")
        out.append(f"{name}  FAILS IF {fails_if}.")
        try:
            ok, lines, breaks = fn(real, fr)
        except SystemExit as e:
            ok, lines, breaks = False, [f"HALT inside the leg: {e}"], []
        except Exception as e:                                   # noqa: BLE001
            ok, lines, breaks = False, [f"ERROR inside the leg: "
                                        f"{type(e).__name__}: {e}"], []
        out.append(f"  [{'GREEN' if ok else 'RED  '}] " + clean(lines[0]))
        out += ["    " + clean(x) for x in lines[1:]]
        leg_ok = ok
        for bname, bok, detail in breaks:
            n_breaks += 1
            if bok:
                leg_ok = False
                out.append(f"  [BREAK] {bname} -> GREEN — VOID BREAK: the leg "
                           f"cannot see its own sabotage")
            else:
                red_breaks += 1
                out.append(f"  [BREAK] {bname} -> RED (correct): "
                           + clean(detail)[:240])
        if not breaks:
            leg_ok = False
            out.append("  [BREAK] none ran — a leg without a sabotage is not "
                       "a witness")
        green += 1 if leg_ok else 0
        out.append(f"  => {name} {'GREEN' if leg_ok else 'RED'}")
    return out, green, n_breaks, red_breaks


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--build-only", action="store_true",
                    help="build the fragment into --out-dir; no fixtures")
    ap.add_argument("--out-dir", default=None)
    a = ap.parse_args(argv)
    run_lines = preamble()
    if a.build_only:
        if not a.out_dir:
            HALT("--build-only needs --out-dir")
        mdb, jsb, _ = build()
        write_outputs(mdb, jsb, Path(a.out_dir))
        return 0
    real = build()
    write_outputs(real[0], real[1], CLOSE_DIR)
    meta = real[2]
    out = ["TIER-C10 · CLOSE §0 · SIX VERDICT ROWS + THE ADMITTED LIST + THE "
           "FORWARD STRIP — FIXTURES", ""] + run_lines + ["", "INPUTS (read-only)"]
    for k, v in meta["inputs"].items():
        out.append(f"  {k:<14} {v['path']}  sha256 {v['sha256']}  "
                   f"{v['bytes']} bytes")
    fs = meta["forward_strip"]
    out.append(f"  {'strip':<14} {fs['path']}  " + (
        f"sha256 {fs['sha256']}  {fs['bytes']} bytes" if fs["present"]
        else "ABSENT"))
    out += ["", "OUTPUTS",
            f"  {CLOSE_REL}/{MD_NAME}  sha256 {sha256(real[0])}  "
            f"{len(real[0])} bytes",
            f"  {CLOSE_REL}/{JSON_NAME}  sha256 {sha256(real[1])}  "
            f"{len(real[1])} bytes"]
    legs, green, n_breaks, red_breaks = run_fixtures(real)
    out += legs
    code_ = 0 if (green == len(LEGS) and red_breaks == n_breaks) else 1
    out += ["", f"FIXTURE SUMMARY  legs GREEN {green}/{len(LEGS)} · breaks RED "
                f"{red_breaks}/{n_breaks} · exit {code_}"]
    text = "\n".join(out) + "\n"
    guard_path = CLOSE_DIR / TRANSCRIPT_NAME
    guard_path.write_text(text, "utf-8")
    sys.stdout.write(text)
    return code_


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Halt as e:
        sys.stdout.write(f"{e}\n")
        sys.exit(2)
