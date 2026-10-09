#!/usr/bin/env python
"""TIER-C12 · TC12-REG · THE WRITE-ONCE REGISTRY [LEANS L-X.16 … L-X.22, L-X.13, L-X.18, L-X.1, L-X.2;
CANON-01, CANON-36; AMENDMENTS_PROPOSED AP-1 (its DEFAULT)].

"Families declared by MECHANISM before the look" (contract :8).  This module files the five
registrations — the contract's own lines and the executor's operative specs — ONCE, before any bar
is read and before any book exists.  It types no text, no spec and no number: it SLICES the pinned
prefix of the contract, PARSES the plan and the frozen readings, CARRIES the five spec blocks and
HASHES.  Stdlib only; env-free; no git; no network; no bar, tape or book is opened.

WHAT IT READS
  the contract      through the pin door's ONE prefix function (scripts/tierc12_pins.py): N and the
                    sha from progress/STEP_Q.json; a `BUILT:` line appended later moves nothing.
  the families      the pin door's parse (`families()`): name, stage, header line, m, q, bar.
  the plan          research_outputs/tierc12/REGISTRATION_PLAN.md: §0 the line map (L-X.17's table),
                    §1 the table and the five blocks `### 1.k <id>`, §2 the law strings.
  the readings      research_outputs/tierc12/LEANS.md (frozen; its sha held to the TC12-LEANS
                    record): the five `### REGISTRATION SPEC · <id>` blocks, L-X.17's line map,
                    L-X.13's template table, the common verdict sentence — each read by its marker.
  the filed records TC11's SCORES.json (`n_boot`, `seed_sens`; sha held to TC12-R0), AS_OF_PIN.json,
                    REGISTRATIONS.json (`law`, by TC11's chain head — never a whole-file sha); X's
                    PINS_X.json (`era_cut_ms`) and REGISTRY_PIN_X.json (`n_boot`) from x_rec/, each
                    held to its X_REC_MANIFEST row by the pin door.

WHAT IT WRITES (research_outputs/tierc12/registrations/)
  REGISTRATIONS.json   `--file`, by exclusive create.  Insertion order (L-X.19).
  REGISTRY_PIN.json    `--file`, by exclusive create.  Sorted keys (L-X.20).
  ATTEST_REG.json      `--attest`: the sorted listing (path, sha) of every file then on disk under
                       research_outputs/tierc12/ and of scripts/tierc12_*.py, except itself (L-X.21).

THE HASH LAW   payload sha = sha256(json.dumps(body without text_sha256 and sha256, sort_keys=True,
               ensure_ascii=False) as UTF-8); chain line = {seq, registration, sha256, prev},
               line_sha256 = sha256(json.dumps(line, sort_keys=True)); prev of the first = GENESIS
               (the character 0 repeated to the length of a sha256 hex digest); head = the last.

THE DETECTORS (every finding and every HALT begins with its detector's name):
  CONTRACT-PREFIX · CONTRACT-TAIL · TEXT-SLICE · CONTEXT-SLICE · EXTERNAL-SLICE · PAYLOAD-SHA · SEED ·
  FAMILY-PARSE · FAMILY-BAR · FAMILY-MEMBER · FAMILY-M-COUNT · RULER-TEXT · TEMPLATE · SPEC-GRAMMAR ·
  PRECOND-GRAMMAR · CHAIN · HEAD-PIN · SPEC-VERBATIM · PLAN==LEANS            (L-X.22's nineteen)
  and, at filing only: PLAN-TABLE · RECORD-PIN · N-BOOT · LAW-HEAD · PIN-CENSUS-SHA · WRITE-ONCE ·
  ATTEST-REG.
RULER-TEXT is AP-1's default: the RULER SENTENCE (the common sentence up to "Printed beside,
deciding nothing:") stands byte for byte at the head of every `verdict_rule` after runs of
whitespace are collapsed, and each rule's printed-beside list holds every item of the common list.

PUBLIC API
  Filing(root=, door=, plan=, leans=, out_dir=)   one filing over one set of paths (the default:
        the tree this file stands in).  .build() -> doc · .pin_of(doc, reg_bytes) -> pin ·
        .file() -> (REGISTRATIONS.json, REGISTRY_PIN.json) · .inputs(doc) -> the verifier's bytes
  verify_filing(doc, pin, contract_bytes, reg_bytes, ext_bytes, plan_bytes, leans_bytes, door=None)
        -> [finding]      the scorer's first act; [] iff every detector is silent
  verify(root=ROOT) -> [finding]                  the filed pair against the tree
  filed(root=ROOT) -> (doc, pin, reg_bytes)       the filed pair, read
  stamp(root=ROOT) -> {registry_head, registrations_sha256}     what every book carries [L-X.21 (2)]
  registration(rid, root=ROOT) -> body            one filed body
  carry(block_lines, rid) -> carried              L-X.18's carry law over one spec block
  payload_sha(body) · chain_of(bodies) -> (chain, head) · GENESIS
  scored_arm(body) -> str                         CANON-36 point 5: the one `scored` element of arms
  labels_of(body) -> [{key, tag, label, text, items}]
  preconditions_of(body) -> [] | [{record, certified_by {record, key}, selector, required {kind,
        value}, commentary}]
  template_of(verdict_rule) -> str                the one `prints '<verdict> …'` template
  attest_findings(root=ROOT) -> [finding] · attest_doc(root=ROOT) -> dict       ATTEST-REG

Run (TC12-REG; no env, no network, no bar):
  ~/venvs/naiad/bin/python -B /Users/luis/Naiad/scripts/tierc12_registrations.py            # dry run: build, verify, print
  … --texts      # also print the five text_of_record strings
  … --file       # write REGISTRATIONS.json and REGISTRY_PIN.json ONCE (HALT if either exists)
  … --verify     # the filed pair against the tree
  … --attest     # write ATTEST_REG.json (after --file; re-run at the gate)
  [--out-dir=DIR] [--plan=PATH] [--leans=PATH]   (scratch twins of the fixture suite)
Exit 0 = GREEN · 1 = a finding · a HALT raises SystemExit with its text.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
from fractions import Fraction
from pathlib import Path

import tierc12_frozen as FROZEN
import tierc12_pins as PINS

ROOT = PINS.ROOT
TIER = "TIER-C12"
T12_REL = "research_outputs/tierc12"
T11_REL = "research_outputs/tierc11"
PLAN_REL = T12_REL + "/REGISTRATION_PLAN.md"
LEANS_REL = T12_REL + "/LEANS.md"
AMENDMENTS_REL = T12_REL + "/LEANS_AMENDMENTS.md"
RULINGS_REL = T12_REL + "/ORCHESTRATOR_RULINGS.md"
DISCLOSURES_REL = T12_REL + "/DISCLOSURES.md"
REVIEW_REL = T12_REL + "/review/LEANS_REVIEW_2026-10-09.json"
RESUME_PASTE_REL = "exchange/queue/2026-10-09_TC12_RESUME_APOLLO.md"
PROGRESS_REL = T12_REL + "/PROGRESS.json"
PROGRESS_DIR_REL = T12_REL + "/progress"
STEP_Q_RECORD = "STEP_Q.json"
R0_RECORD = "TC12-R0.json"
LEANS_RECORD = "TC12-LEANS.json"
R0_FROZEN_KEY = "frozen_estate_shas_at_r0"
OUT_REL = T12_REL + "/registrations"
REG_NAME = "REGISTRATIONS.json"
PIN_NAME = "REGISTRY_PIN.json"
ATTEST_NAME = "ATTEST_REG.json"
T11_REG_REL = T11_REL + "/registrations/REGISTRATIONS.json"
T11_PIN_REL = T11_REL + "/registrations/REGISTRY_PIN.json"
T11_SCORES_REL = T11_REL + "/scores/SCORES.json"
T11_ASOF_REL = T11_REL + "/data/AS_OF_PIN.json"
T11_ASOF_KEY = "as_of_last_closed_4h_close_ms"
X_REC_REL = T12_REL + "/x_rec/"
X_PINS_REL = X_REC_REL + "tierc11x/pins/PINS_X.json"
X_ERA_KEY = "era_cut_ms"
X_REG_PIN_REL = X_REC_REL + "tierc11x/registrations/REGISTRY_PIN_X.json"
SEED_PIN = "seed"
AM_ON_FILE = "## AM-1 · "

GENESIS = "0" * len(hashlib.sha256(b"").hexdigest())

# ── L-X.18: the carry law and the field grammar ──
FIELDS = ("id", "family", "family_m", "family_bar", "prior", "mechanism", "population", "arms",
          "statistic", "comparison", "preconditions", "verdict_rule", "labels", "disclosed_beside",
          "failure_conditions")
CHECKED = ("id", "family", "family_m", "family_bar", "prior")
SPEC_KEYS = ("mechanism", "population", "arms", "statistic", "comparison", "preconditions", "labels",
             "disclosed_beside", "failure_conditions")
LIST_FIELDS = ("arms", "labels")
RULE_FIELD = "verdict_rule"
SHA_KEYS = ("text_sha256", "sha256")
SPEC_HEAD = "### REGISTRATION SPEC · "
HEADINGS = ("### ", "## ")
SUB = "  - "
SUB_CONT = "    "
TOP_CONT = "  "
TOP_RX = re.compile(r"- \*\*(?P<name>[a-z_]+):\*\*(?P<rest>.*)")
RULE_LINE_RX = re.compile(r"-{3,}")
DIGITS_RX = re.compile(r"[0-9]+")
BAR_RX = re.compile(r"[0-9]+\.[0-9]+")
FAMILY_RX = re.compile(r"[A-Z][A-Z-]*")
SCORED_RX = re.compile(r"`scored`\s")
LABEL_RX = re.compile(r'`?(?P<key>[a-z_]+)`? — tag: (?P<tag>[^;]+); label: (?P<label>[^;]+); '
                      r'text: "(?P<text>[^"]*)"; items: (?P<items>.+)')
NONE_RX = re.compile(r"none(?: — .+)?")
PRECOND_RX = re.compile(r'\{record: (?P<record>\S+), certified_by: (?P<cert_record>\S+) (?P<cert_key>\S+), '
                        r'selector: (?P<selector>.+?), required: (?:"(?P<equals>[^"]*)"|'
                        r'contains "(?P<contains>[^"]*)"|(?P<true>true))\}(?: — (?P<commentary>.+))?')
TEMPLATE_RX = re.compile(r"prints '(<verdict>[^']*)'")
EXTERNAL_RX = re.compile(r"external_context `(?P<path>[^`]+)` lines (?P<lines>[0-9]+(?:-[0-9]+)?"
                         r"(?: and [0-9]+(?:-[0-9]+)?)*) \(sha256 `(?P<sha>[0-9a-f]+)`\)")
RANGE_JOIN = " and "
PRIOR_RX = re.compile(r"\[(\d+)%\]")

# ── the markers the plan and the frozen readings are read by ──
MAP_ROW_RX = re.compile(r"\| (?P<object>.+?) \| (?P<a>[0-9]+)(?:-(?P<b>[0-9]+))? \| `(?P<sha>[0-9a-f]+)` \|")
TPL_ROW_RX = re.compile(r"\| (?P<id>P-[A-Z0-9-]+) \| `(?P<key>[a-z_]+)` \| `(?P<tag>[^`]+)` \| "
                        r"`(?P<label>[^`]+)` \| `(?P<template>[^`]+)`.*\|")
REG_ROW_RX = re.compile(r"\| (?P<seq>[0-9]+) \| (?P<id>\S+) \| (?P<family>\S+) \| (?P<m>[0-9]+) \| "
                        r"(?P<bar>[0-9.]+) \| (?P<prior>[0-9]+) \| (?P<a>[0-9]+)-(?P<b>[0-9]+) \| "
                        r"(?P<comparison>[^|]+?) \| (?P<preconditions>[^|]+?) \| (?P<labels>[^|]+?) \|")
PLAN_BLOCK_RX = re.compile(r"### 1\.(?P<k>[0-9]+) (?P<id>\S+)")
PLAN_MAP_FROM, PLAN_MAP_TO = "## 0 ", "## 1 "
PLAN_TABLE_FROM, PLAN_TABLE_TO = "## 1 ", "### 1."
LEANS_MAP_FROM = "**L-X.17 "
LEANS_TPL_FROM = "**L-X.13 "
LEANS_READING = "**L-X."
COMMON_HEAD = "- **verdict_rule, common sentence:**"
QUOTED_RX = re.compile(r'"([^"]+)"')
BESIDE_MARK = "Printed beside, deciding nothing:"
BESIDE_TAIL = "Tier-E arms carry no verdict word."
ITEM_SEP = ", "
RULERS = ("two-sample vs v6", "vs zero")
TEXT_OBJ = "**{id} [{prior}%]**"
HEADER_OBJ_RX = re.compile(r"STAGE [A-Z] header \(family\)")
LAWS_OBJ = "LAWS"
VERDICT_LAW_RX = re.compile(r'- `verdict_law` \{clause_a: "([^"]+)", clause_b: "([^"]+)", '
                            r'clause_c: "([^"]+)", reading: "([^"]+)", rival: "([^"]+)"\}')
VERDICT_LAW_KEYS = ("clause_a", "clause_b", "clause_c", "reading", "rival")
CLAUSE_KEYS = ("clause_a", "clause_b", "clause_c")
LAW_RX = re.compile(r'- `(?P<key>[a-z_]+)`: "(?P<text>[^"]+)"')
LAW_KEYS = ("spec_carry_law", "witness_law", "text_before_result_law")

# ── L-X.21: the two typed sets (paths relative to research_outputs/tierc12/ unless they begin scripts/) ──
SCRIPTS = "scripts/"
SCRIPT_GLOB = "tierc12_*.py"
TREE = "/**"
PARQUET = ".parquet"
X_REC_DIR = "x_rec/"
PRE_REG_RECORDS = (STEP_Q_RECORD, R0_RECORD, LEANS_RECORD)       # "the artifact paths of STEP Q, TC12-R0 and TC12-LEANS"
PRE_REG = ("progress/**", "PROGRESS.json", ".gitignore", "scout/**", "x_rec/**", "leans_draft/**",
           "review/**", "LEANS.md", "LEANS_AMENDMENTS.md", "AMENDMENTS_PROPOSED.md",
           "ORCHESTRATOR_RULINGS.md", "DISCLOSURES.md")
PRE_REG_SCRIPTS = ("scripts/tierc12_progress.py",)
REG_SET = ("REGISTRATION_PLAN.md",
           "registrations/REGISTRATIONS.json", "registrations/REGISTRY_PIN.json",
           "registrations/ATTEST_REG.json", "registrations/FIXTURES_REG.txt",
           "pins/CONTRACT_PIN_MAP.json", "pins/CONTRACT_PINS.json", "pins/PIN_REGISTER.json",
           "pins/CONTRACT_TOKENS_UNPINNED.json", "pins/FIXTURES_PINS.txt",
           "frozen/FROZEN_ESTATE.json", "resume/FIXTURES_RESUME_TC12-REG.txt",
           "closure/FIXTURES_CLOSURE_TC12-REG.txt", "progress/TC12-REG.json",
           "scripts/tierc12_fx.py", "scripts/tierc12_units.py", "scripts/tierc12_pins.py",
           "scripts/tierc12_frozen.py", "scripts/tierc12_registrations.py",
           "scripts/tierc12_registrations_fixtures.py", "scripts/tierc12_pins_fixtures.py",
           "scripts/tierc12_resume_fixtures.py", "scripts/tierc12_closure_fixtures.py")
ATTEST_SELF = "registrations/" + ATTEST_NAME
ATTEST_WHAT = ("TIER-C12 · ATTEST-REG (LEANS L-X.21 clause 3): the listing (path, sha256) of every file on "
               "disk under research_outputs/tierc12/ and of scripts/tierc12_*.py, taken after --file, "
               "except this file")
ATTEST_LAW = ("the disk walk holds no file outside PRE_REG ∪ REG_SET and no .parquet outside x_rec/, and "
              "scripts/tierc12_*.py holds nothing outside {tierc12_progress.py} ∪ REG_SET's scripts; paths "
              "are relative to research_outputs/tierc12/ unless they begin scripts/; a REG_SET member not "
              "yet on disk is listed under `absent`")


HALT = "HALT "


def halt(tag: str, msg: str):
    raise SystemExit(f"{HALT}{tag}: {msg}")


def raise_first(found: list) -> None:
    """A filing HALTs on its first finding, under that finding's detector."""
    if found:
        tag, _, msg = found[0].partition(" ")
        halt(tag, msg)


def finding_of(e) -> str:
    """A HALT as a finding: `HALT <TAG>: <text>` -> `<TAG> <text>`, the detector's name first."""
    text = str(e)
    text = text[len(HALT):] if text.startswith(HALT) else text
    tag, sep, msg = text.partition(": ")
    return f"{tag} {msg}" if sep else text


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha_text(s: str) -> str:
    return sha_bytes(s.encode("utf-8"))


def unwrap(parts) -> str:
    """A markdown bullet's wrapped lines joined by one space — the only change the carry law makes."""
    return " ".join(p.strip() for p in parts if p.strip())


def squeeze(s: str) -> str:
    """Runs of whitespace collapsed (AP-1's default comparison)."""
    return " ".join(s.split())


def render(doc: dict) -> bytes:
    """REGISTRATIONS.json: insertion order, two-space indent, a trailing newline, UTF-8 [L-X.19]."""
    return (json.dumps(doc, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def render_sorted(doc: dict) -> bytes:
    """REGISTRY_PIN.json and ATTEST_REG.json: the same with sorted keys [L-X.20]."""
    return (json.dumps(doc, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


# ═══════════════════════════════════════════════════════ THE HASH LAW [L-X.19]
def payload_sha(body: dict) -> str:
    b = {k: v for k, v in body.items() if k not in SHA_KEYS}
    return sha_bytes(json.dumps(b, sort_keys=True, ensure_ascii=False).encode("utf-8"))


def chain_of(bodies: list) -> tuple:
    """(chain, head): one line per registration in the order given, from GENESIS."""
    prev, chain = GENESIS, []
    for r in bodies:
        line = {"seq": r.get("seq"), "registration": r.get("registration"), "sha256": r.get("sha256"),
                "prev": prev}
        line["line_sha256"] = sha_bytes(json.dumps(line, sort_keys=True).encode())
        prev = line["line_sha256"]
        chain.append(line)
    return chain, prev


# ═══════════════════════════════════════════════════════ READING THE PLAN AND THE FROZEN READINGS
def _between(lines: list, start: str, stop: str, what: str) -> list:
    """The lines after the ONE line beginning `start`, up to the next line beginning `stop`."""
    i = [k for k, ln in enumerate(lines) if ln.startswith(start)]
    if len(i) != 1:
        halt("PLAN==LEANS", f"{what}: {len(i)} lines begin {start!r} (exactly one is the law)")
    j = next((k for k in range(i[0] + 1, len(lines)) if lines[k].startswith(stop)), len(lines))
    return lines[i[0] + 1:j]


def line_map(lines: list, start: str, stop: str, what: str) -> list:
    """[{object, lines [a, b], sha256}] — the rows of a line-map table."""
    rows = []
    for ln in _between(lines, start, stop, what):
        m = MAP_ROW_RX.fullmatch(ln.strip())
        if m:
            a = int(m.group("a"))
            rows.append({"object": m.group("object"), "lines": [a, int(m.group("b") or a)],
                         "sha256": m.group("sha")})
    return rows


def template_table(leans: list) -> dict:
    """L-X.13's table: {registration id: {key, tag, label, template}} — the bytes of record."""
    out = {}
    for ln in _between(leans, LEANS_TPL_FROM, LEANS_READING, "L-X.13"):
        m = TPL_ROW_RX.fullmatch(ln.strip())
        if m:
            out[m.group("id")] = {k: m.group(k) for k in ("key", "tag", "label", "template")}
    return out


def common_sentence(leans: list) -> dict:
    """The common verdict sentence of the frozen readings -> {ruler, items}: the RULER SENTENCE (up
    to the printed-beside mark) and the items of its printed-beside list (AP-1)."""
    i = [k for k, ln in enumerate(leans) if ln.startswith(COMMON_HEAD)]
    if len(i) != 1:
        halt("RULER-TEXT", f"the frozen readings hold {len(i)} common verdict sentences")
    parts, k = [leans[i[0]]], i[0] + 1
    while k < len(leans) and leans[k].startswith(TOP_CONT) and not leans[k].startswith(SUB):
        parts.append(leans[k])
        k += 1
    m = QUOTED_RX.search(unwrap(parts))
    if not m or m.group(1).count(BESIDE_MARK) != 1 or BESIDE_TAIL not in m.group(1):
        halt("RULER-TEXT", "the common verdict sentence is not `<ruler> Printed beside, deciding nothing: "
                           "<list>. Tier-E arms carry no verdict word.`")
    ruler, rest = m.group(1).split(BESIDE_MARK)
    items = rest.split(BESIDE_TAIL)[0].strip().rstrip(".").split(ITEM_SEP)
    return {"ruler": squeeze(ruler), "items": [squeeze(x) for x in items]}


def leans_block(leans: list, rid: str) -> list:
    """The frozen `### REGISTRATION SPEC · <id>` block: every line after that heading up to the next
    line beginning `### ` or `## `."""
    i = [k for k, ln in enumerate(leans) if ln == SPEC_HEAD + rid]
    if len(i) != 1:
        halt("PLAN==LEANS", f"{rid}: the frozen readings hold {len(i)} `{SPEC_HEAD}{rid}` headings")
    j = next((k for k in range(i[0] + 1, len(leans)) if leans[k].startswith(HEADINGS)), len(leans))
    return leans[i[0] + 1:j]


def plan_blocks(plan: list) -> list:
    """[(k, registration id, block lines)] — the plan's `### 1.k <id>` blocks, in the plan's order."""
    out = []
    for i, ln in enumerate(plan):
        m = PLAN_BLOCK_RX.fullmatch(ln)
        if m:
            j = next((k for k in range(i + 1, len(plan)) if plan[k].startswith(HEADINGS)), len(plan))
            out.append((int(m.group("k")), m.group("id"), plan[i + 1:j]))
    return out


def plan_table(plan: list) -> list:
    """The rows of the plan's §1 table, cells as written."""
    return [m.groupdict() for m in (REG_ROW_RX.fullmatch(ln.strip())
                                    for ln in _between(plan, PLAN_TABLE_FROM, PLAN_TABLE_TO, "plan §1"))
            if m]


def plan_laws(plan: list) -> dict:
    """§2's verdict_law and the three law strings, verbatim."""
    hits = [m for m in (VERDICT_LAW_RX.fullmatch(ln) for ln in plan) if m]
    if len(hits) != 1:
        halt("PLAN-TABLE", f"the plan's §2 holds {len(hits)} verdict_law lines")
    laws = {m.group("key"): m.group("text") for m in (LAW_RX.fullmatch(ln) for ln in plan) if m}
    if sorted(laws) != sorted(LAW_KEYS):
        halt("PLAN-TABLE", f"the plan's §2 states the law strings {sorted(laws)}, not {sorted(LAW_KEYS)}")
    return {"verdict_law": dict(zip(VERDICT_LAW_KEYS, hits[0].groups())), **laws}


def readings_of(leans_bytes: bytes) -> dict:
    """Everything the filing reads from the frozen readings, by marker."""
    leans = leans_bytes.decode("utf-8").split("\n")
    return {"lines": leans, "map": line_map(leans, LEANS_MAP_FROM, LEANS_READING, "L-X.17"),
            "templates": template_table(leans), "common": common_sentence(leans)}


def plan_leans_findings(plan: list, R: dict) -> list:
    """PLAN==LEANS: the plan's line map is L-X.17's, row for row; each §1.k block is the frozen
    block byte for byte; the blocks stand in seq order 1 … n."""
    out = []
    if line_map(plan, PLAN_MAP_FROM, PLAN_MAP_TO, "plan §0") != R["map"]:
        out.append("PLAN==LEANS the plan's line map is not L-X.17's table of the frozen readings, row for row")
    blocks = plan_blocks(plan)
    if [k for k, _, _ in blocks] != list(range(1, len(blocks) + 1)) or not blocks:
        out.append(f"PLAN==LEANS the plan's blocks are numbered {[k for k, _, _ in blocks]}")
    for _, rid, block in blocks:
        try:
            same = block == leans_block(R["lines"], rid)
        except SystemExit as e:
            out.append(finding_of(e))
            continue
        if not same:
            out.append(f"PLAN==LEANS {rid}: the plan's block is not the frozen `{SPEC_HEAD}{rid}` block "
                       f"byte for byte")
    return out


# ═══════════════════════════════════════════════════════ THE CARRY LAW AND THE FIELD GRAMMAR [L-X.18]
def carry(block: list, rid: str) -> dict:
    """One spec block -> {field: value}: fifteen top-level bullets `- **<field>:** <text>` in the
    fixed order; a bullet's wrapped lines join with one space; one level of sub-bullets becomes a
    list (a head AND sub-bullets: {text, items}); markdown kept.  The five checked fields file the
    text up to the first space (`family_m` and `prior` as integers).  Blank lines and the trailing
    rule line of the frozen text carry nothing.  HALT SPEC-GRAMMAR otherwise."""
    body = list(block)
    while body and (not body[len(body) - 1].strip() or RULE_LINE_RX.fullmatch(body[len(body) - 1])):
        body.pop()
    while body and not body[0].strip():
        body.pop(0)
    bullets, cur, item = [], None, None
    for ln in body:
        m = TOP_RX.fullmatch(ln)
        if m:
            cur, item = {"name": m.group("name"), "rest": [m.group("rest")], "items": []}, None
            bullets.append(cur)
        elif cur is None:
            halt("SPEC-GRAMMAR", f"{rid}: the block opens with a line that is not a field bullet: {ln!r}")
        elif ln.startswith(SUB):
            item = [ln[len(SUB):]]
            cur["items"].append(item)
        elif ln.startswith(SUB_CONT) and item is not None and not ln.startswith(SUB_CONT + SUB.lstrip()):
            item.append(ln)
        elif ln.startswith(TOP_CONT) and not ln.startswith(SUB_CONT) and item is None:
            cur["rest"].append(ln)
        else:
            halt("SPEC-GRAMMAR", f"{rid}: a line of the block is no bullet and no wrapped line: {ln!r}")
    names = tuple(b["name"] for b in bullets)
    if names != FIELDS:
        halt("SPEC-GRAMMAR", f"{rid}: the block's fields are {list(names)}; the law is the fifteen fields "
                             f"{list(FIELDS)} in this order — a missing, extra, renamed or reordered field")
    out = {}
    for b in bullets:
        name, head, items = b["name"], unwrap(b["rest"]), [unwrap(x) for x in b["items"]]
        if name in CHECKED:
            token = head.split(" ", 1)[0]
            if items or not token:
                halt("SPEC-GRAMMAR", f"{rid}: the checked field {name} is not one leading token")
            out[name] = token
        elif items and head:
            out[name] = {"text": head, "items": items}
        elif items:
            out[name] = items
        elif head:
            out[name] = head
        else:
            halt("SPEC-GRAMMAR", f"{rid}: the field {name} is empty")
    forms = (("id", None), ("family", FAMILY_RX), ("family_m", DIGITS_RX), ("family_bar", BAR_RX),
             ("prior", DIGITS_RX))
    for name, rx in forms:
        if (rx is None and out[name] != rid) or (rx is not None and not rx.fullmatch(out[name])):
            halt("SPEC-GRAMMAR", f"{rid}: the checked field {name} reads {out[name]!r} — the value is the "
                                 f"text up to the first space (`prior` and `family_m` digits only)")
    out["family_m"], out["prior"] = int(out["family_m"]), int(out["prior"])
    return out


def carried_of(body: dict) -> dict:
    """A FILED body back in the carried form, for the detectors a filed payload is judged by."""
    spec = body.get("operative_spec")
    spec = spec if isinstance(spec, dict) else {}
    return {"id": body.get("registration"), "family": body.get("family"), "family_m": body.get("family_m"),
            "family_bar": body.get("family_bar"), "prior": body.get("prior_pct"),
            RULE_FIELD: body.get(RULE_FIELD), **{k: spec[k] for k in spec},
            "_spec_keys": tuple(spec)}


def grammar_findings(c: dict) -> list:
    """SPEC-GRAMMAR and PRECOND-GRAMMAR on a carried block (the plan's, or a filed payload's)."""
    rid, out = c.get("id"), []
    keys = c.get("_spec_keys", SPEC_KEYS)
    if tuple(keys) != SPEC_KEYS:
        out.append(f"SPEC-GRAMMAR {rid}: the operative_spec holds {list(keys)}, not the nine fields "
                   f"{list(SPEC_KEYS)} in order")
    if type(c.get("family_m")) is not int or type(c.get("prior")) is not int \
            or not isinstance(c.get("family_bar"), str) or not BAR_RX.fullmatch(c["family_bar"]) \
            or not isinstance(c.get("family"), str) or not FAMILY_RX.fullmatch(c["family"]):
        out.append(f"SPEC-GRAMMAR {rid}: a checked field is not in its form (family {c.get('family')!r}, "
                   f"family_m {c.get('family_m')!r}, family_bar {c.get('family_bar')!r}, prior "
                   f"{c.get('prior')!r})")
    if not isinstance(c.get(RULE_FIELD), str):
        out.append(f"SPEC-GRAMMAR {rid}: verdict_rule is not one text")
    for name in LIST_FIELDS:
        v = c.get(name)
        if not isinstance(v, list) or not v or not all(isinstance(x, str) for x in v):
            out.append(f"SPEC-GRAMMAR {rid}: `{name}` is not a list of sub-bullets")
    arms = c.get("arms") if isinstance(c.get("arms"), list) else []
    n = sum(1 for x in arms if isinstance(x, str) and SCORED_RX.match(x))
    if n != 1:
        out.append(f"SPEC-GRAMMAR {rid}: {n} sub-bullets of `arms` begin `scored` (exactly one is the law)")
    labels = c.get("labels") if isinstance(c.get("labels"), list) else []
    hits = [LABEL_RX.fullmatch(x) if isinstance(x, str) else None for x in labels]
    if not all(hits) or len({m.group("key") for m in hits if m}) != len(hits):
        out.append(f"SPEC-GRAMMAR {rid}: a `labels` sub-bullet is not `<key> — tag: <TAG|none>; label: "
                   f"<label>; text: \"<text>\"; items: <items>`, or a key stands twice")
    pre = c.get("preconditions")
    if isinstance(pre, str):
        if not NONE_RX.fullmatch(pre):
            out.append(f"PRECOND-GRAMMAR {rid}: `preconditions` is prose — neither the bare word `none` "
                       f"(optionally ` — <commentary>`) nor items")
    elif not isinstance(pre, list) or not pre or not all(isinstance(x, str) and PRECOND_RX.fullmatch(x)
                                                         for x in pre):
        out.append(f"PRECOND-GRAMMAR {rid}: a `preconditions` item is not `{{record: <path>, certified_by: "
                   f"<progress record> <key>, selector: <selector>, required: <\"string\" | contains "
                   f"\"string\" | true>}}` — no other form and no numeric comparator exists")
    return out


def template_of(verdict_rule: str) -> str:
    """The ONE `prints '<verdict> …'` template of a filed rule; HALT TEMPLATE unless exactly one."""
    got = TEMPLATE_RX.findall(verdict_rule)
    if len(got) != 1:
        halt("TEMPLATE", f"the rule carries {len(got)} `prints '<verdict> …'` templates")
    return got[0]


def template_findings(c: dict, templates: dict) -> list:
    """TEMPLATE: the rule's one template, and the label's key, tag and label, are L-X.13's row FOR
    THIS REGISTRATION ID, byte for byte."""
    rid, want = c.get("id"), templates.get(c.get("id"))
    if want is None:
        return [f"TEMPLATE {rid}: L-X.13's table holds no row for this registration"]
    rule = c.get(RULE_FIELD) if isinstance(c.get(RULE_FIELD), str) else ""
    got, out = TEMPLATE_RX.findall(rule), []
    if got != [want["template"]]:
        out.append(f"TEMPLATE {rid}: the rule carries {len(got)} template(s) {got}; L-X.13's row for this "
                   f"id is {want['template']!r}")
    labels = c.get("labels") if isinstance(c.get("labels"), list) else []
    have = [(m.group("key"), m.group("tag"), m.group("label"))
            for m in (LABEL_RX.fullmatch(x) for x in labels if isinstance(x, str)) if m]
    if have != [(want["key"], want["tag"], want["label"])]:
        out.append(f"TEMPLATE {rid}: the labels read (key, tag, label) {have}; L-X.13's row is "
                   f"{(want['key'], want['tag'], want['label'])}")
    return out


def ruler_findings(c: dict, common: dict, text: str, header_text: str, stats: dict) -> list:
    """RULER-TEXT (AP-1's default): the ruler sentence at the head of the rule; the printed-beside
    list holds every common item; the comparison names one ruler and the contract's text or family
    header names the same; the rule states N_BOOT and both seeds."""
    rid, out = c.get("id"), []
    rule = squeeze(c.get(RULE_FIELD)) if isinstance(c.get(RULE_FIELD), str) else ""
    if not rule.startswith(common["ruler"]):
        out.append(f"RULER-TEXT {rid}: the verdict_rule does not open with the ruler sentence of the frozen "
                   f"readings, byte for byte after collapsing whitespace")
    if rule.count(BESIDE_MARK) != 1 or BESIDE_TAIL not in rule.split(BESIDE_MARK)[1]:
        out.append(f"RULER-TEXT {rid}: the verdict_rule does not hold one `{BESIDE_MARK} … {BESIDE_TAIL}`")
    else:
        span = rule.split(BESIDE_MARK)[1].split(BESIDE_TAIL)[0]
        missing = [x for x in common["items"] if x not in span]
        if missing:
            out.append(f"RULER-TEXT {rid}: the printed-beside list lacks {missing}")
    comparison = c.get("comparison") if isinstance(c.get("comparison"), str) else ""
    named = [r for r in RULERS if comparison.startswith(r)]
    if len(named) != 1:
        out.append(f"RULER-TEXT {rid}: the comparison names no ruler of {list(RULERS)}")
    elif named[0] not in text and named[0] not in header_text:
        out.append(f"RULER-TEXT {rid}: neither the text slice nor its family header reads `{named[0]}`")
    unstated = [k for k in ("n_boot", "seed", "seed_sens") if str(stats[k]) not in rule]
    if unstated:
        out.append(f"RULER-TEXT {rid}: the verdict_rule does not state {unstated} "
                   f"({[stats[k] for k in unstated]})")
    return out


def carried_findings(c: dict, R: dict, text: str, header_text: str, stats: dict) -> list:
    return grammar_findings(c) + template_findings(c, R["templates"]) \
        + ruler_findings(c, R["common"], text, header_text, stats)


# ── what a consumer reads from a filed body ──
def scored_arm(body: dict) -> str:
    """CANON-36 point 5: the ONE element of `operative_spec.arms` matching ^`scored`\\s."""
    hits = [x for x in body["operative_spec"]["arms"] if SCORED_RX.match(x)]
    if len(hits) != 1:
        halt("SPEC-GRAMMAR", f"{body.get('registration')}: {len(hits)} `scored` elements in arms")
    return hits[0]


def labels_of(body: dict) -> list:
    out = []
    for x in body["operative_spec"]["labels"]:
        m = LABEL_RX.fullmatch(x)
        if not m:
            halt("SPEC-GRAMMAR", f"{body.get('registration')}: a label outside the grammar")
        out.append(m.groupdict())
    return out


def preconditions_of(body: dict) -> list:
    """[] for `none`; else one dict per item.  `required.kind` is equals | contains | true."""
    pre = body["operative_spec"]["preconditions"]
    if isinstance(pre, str) and NONE_RX.fullmatch(pre):
        return []
    out = []
    for x in pre if isinstance(pre, list) else [pre]:
        m = PRECOND_RX.fullmatch(x) if isinstance(x, str) else None
        if not m:
            halt("PRECOND-GRAMMAR", f"{body.get('registration')}: a precondition outside the grammar")
        kind = next(k for k in ("equals", "contains", "true") if m.group(k) is not None)
        out.append({"record": m.group("record"),
                    "certified_by": {"record": m.group("cert_record"), "key": m.group("cert_key")},
                    "selector": m.group("selector"),
                    "required": {"kind": kind, "value": True if kind == "true" else m.group(kind)},
                    "commentary": m.group("commentary")})
    return out


def external_declared(c: dict) -> list:
    """[(path, file sha256, [a, b])] — the external slices a block declares inside its labels."""
    out = []
    for x in c.get("labels") if isinstance(c.get("labels"), list) else []:
        for m in EXTERNAL_RX.finditer(x if isinstance(x, str) else ""):
            for r in m.group("lines").split(RANGE_JOIN):
                a, _, b = r.partition("-")
                out.append((m.group("path"), m.group("sha"), [int(a), int(b or a)]))
    return out


# ═══════════════════════════════════════════════════════ THE SLICES [L-X.17]
def banned_external() -> tuple:
    """The files TC12's own close acts move (L-0.24's sets as the census tool types them, and
    TC11's contract): no slice is cut from one and no TC12 pin is its whole-file sha."""
    return tuple(sorted({p for v in FROZEN.STAMP_SETS_T.values() for p in v}))


def roles(lmap: list, fam: dict) -> tuple:
    """(laws row, {header line: row}, findings) — FAMILY-PARSE: the rows the map marks as family
    headers are exactly the pin door's header lines; the q line lies inside the LAWS slice."""
    heads = {r["lines"][0]: r for r in lmap if HEADER_OBJ_RX.fullmatch(r["object"])
             and r["lines"][0] == r["lines"][1]}
    laws = [r for r in lmap if r["object"].startswith(LAWS_OBJ)]
    out = []
    if sorted(heads) != sorted(f["header_line"] for f in fam["families"]):
        out.append(f"FAMILY-PARSE the line map marks {sorted(heads)} as family headers; the pin door "
                   f"parses {sorted(f['header_line'] for f in fam['families'])}")
    if len(laws) != 1 or not laws[0]["lines"][0] <= fam["q_line"] <= laws[0]["lines"][1]:
        out.append(f"FAMILY-PARSE the line stating `bar = q ÷ m` (:{fam['q_line']}) does not lie inside "
                   f"one LAWS slice of the line map")
    return (laws[0] if len(laws) == 1 else None), heads, out


def cut_row(lines: list, row: dict, tag: str, rid: str) -> tuple:
    """(text, findings): a line-map row re-cut from the prefix by TC11's slice law, its sha held."""
    try:
        text = PINS.cut(lines, row["lines"][0], row["lines"][1])
    except SystemExit as e:
        return None, [f"{tag} {rid}: {e}"]
    if sha_text(text) != row["sha256"]:
        return text, [f"{tag} {rid}: contract :{row['lines'][0]}-{row['lines'][1]} "
                      f"({row['object']}) does not hash to the line map's sha"]
    return text, []


def external_items(declared: list, ext_bytes: dict, rid: str) -> tuple:
    """(items, findings): each declared external slice cut by the same law, the file's sha first."""
    items, out, banned = [], [], banned_external()
    for path, sha, (a, b) in declared:
        raw = ext_bytes.get(path)
        if path in banned:
            out.append(f"EXTERNAL-SLICE {rid}: {path} is a file TC12's own close acts move — no slice "
                       f"is cut from it [L-0.24]")
        elif raw is None:
            out.append(f"EXTERNAL-SLICE {rid}: no bytes of {path} were handed to the filing")
        elif sha_bytes(raw) != sha:
            out.append(f"EXTERNAL-SLICE {rid}: {path} does not hash to the sha its block declares")
        else:
            xl = raw.decode("utf-8").split("\n")
            if not 1 <= a <= b <= len(xl):
                out.append(f"EXTERNAL-SLICE {rid}: lines {a}-{b} are not a slice of {path}")
            else:
                items.append({"path": path, "sha256": sha, "lines": [a, b], "text": "\n".join(xl[a - 1:b])})
    return items, out


# ═══════════════════════════════════════════════════════ THE DERIVATION (shared by filing and verifier)
def derive(lines: list, fam: dict, plan_bytes: bytes, R: dict, ext_bytes: dict, stats: dict) -> tuple:
    """(bodies, plan document, findings): the five bodies as THIS plan, these readings and this
    prefix give them.  A registration whose block cannot be carried yields no body."""
    plan = plan_bytes.decode("utf-8").split("\n")
    out = plan_leans_findings(plan, R)
    lmap = line_map(plan, PLAN_MAP_FROM, PLAN_MAP_TO, "plan §0")
    laws, heads, found = roles(lmap, fam)
    out += found
    table = {r["id"]: r for r in plan_table(plan)}
    bodies, firsts = [], []
    for k, rid, block in plan_blocks(plan):
        try:
            c = carry(block, rid)
        except SystemExit as e:
            out.append(finding_of(e))
            continue
        want = fam["by_registration"].get(rid)
        rows = [r for r in lmap if r["object"] == TEXT_OBJ.format(id=rid, prior=c["prior"])]
        if want is None or len(rows) != 1:
            out.append(f"TEXT-SLICE {rid}: {len(rows)} line-map rows read "
                       f"`{TEXT_OBJ.format(id=rid, prior=c['prior'])}`, or the contract registers no such id")
            continue
        text, found = cut_row(lines, rows[0], "TEXT-SLICE", rid)
        out += found
        if text is None:
            continue
        priors = PRIOR_RX.findall(text)
        if not text.lstrip().startswith(rid + " ") or priors[:1] != [str(c["prior"])] \
                or rows[0]["lines"][0] != want["line"] or c["prior"] != want["prior_pct"]:
            out.append(f"TEXT-SLICE {rid}: the slice :{rows[0]['lines'][0]}-{rows[0]['lines'][1]} does not "
                       f"begin with the id, or its `[<prior>%]` is not the block's prior {c['prior']}")
        if c["family"] != want["family"]:
            out.append(f"FAMILY-MEMBER {rid}: the block names family {c['family']}; the contract stands it "
                       f"under {want['family']}")
        if c["family_m"] != want["m"]:
            out.append(f"FAMILY-M-COUNT {rid}: the block states m = {c['family_m']}; the header declares "
                       f"{want['m']}")
        if c["family_bar"] != want["bar"] or Fraction(c["family_bar"]) != want["bar_fraction"]:
            out.append(f"FAMILY-BAR {rid}: the block states the bar {c['family_bar']}; the header's is "
                       f"{want['bar']} ({want['bar_exact']})")
        header = next((f for f in fam["families"] if f["family"] == want["family"]), None)
        context = []
        for row in (laws, heads.get(header["header_line"]) if header else None):
            if row is None:
                out.append(f"CONTEXT-SLICE {rid}: the line map holds no LAWS slice or no row for its "
                           f"family header")
                continue
            ctext, found = cut_row(lines, row, "CONTEXT-SLICE", rid)
            out += found
            context.append({"lines": list(row["lines"]), "text": ctext})
        external, found = external_items(external_declared(c), ext_bytes, rid)
        out += found
        out += carried_findings(c, R, text, header["header_text"] if header else "", stats)
        t = table.get(rid)
        cells = None if t is None else (int(t["seq"]), t["family"], int(t["m"]), t["bar"], int(t["prior"]),
                                        [int(t["a"]), int(t["b"])], t["comparison"], t["preconditions"],
                                        t["labels"])
        pre = c["preconditions"]
        n_pre = len(pre) if isinstance(pre, list) else 0
        mine = (k, c["family"], c["family_m"], c["family_bar"], c["prior"], list(rows[0]["lines"]),
                next((r for r in RULERS if str(c["comparison"]).startswith(r)), None),
                (f"{n_pre} item" + ("" if n_pre == 1 else "s")) if n_pre else "none",
                ITEM_SEP.join(m.group("key") for m in (LABEL_RX.fullmatch(x) for x in c["labels"]
                                                      if isinstance(x, str)) if m))
        if cells != mine:
            out.append(f"PLAN-TABLE {rid}: the plan's §1 row reads {cells}; the parse and the block give "
                       f"{mine}")
        body = {"registration": rid, "seq": k, "family": c["family"], "family_m": c["family_m"],
                "family_bar": c["family_bar"], "prior_pct": c["prior"], "seed": stats["seed"],
                "text_of_record": text, "text_lines": list(rows[0]["lines"]),
                "context_of_record": context}
        if external:
            body["external_context"] = external
        body["operative_spec"] = {key: c[key] for key in SPEC_KEYS}
        body[RULE_FIELD] = c[RULE_FIELD]
        body["text_sha256"] = sha_text(text)
        body["sha256"] = payload_sha(body)
        bodies.append(body)
        firsts.append(rows[0]["lines"][0])
    if firsts != sorted(firsts) or sorted(b["registration"] for b in bodies) != sorted(fam["by_registration"]):
        out.append(f"CHAIN the plan's blocks {[b['registration'] for b in bodies]} are not the contract's "
                   f"registrations {sorted(fam['by_registration'])} in ascending order of first text line")
    return bodies, plan, out


def families_filed(fam: dict) -> list:
    keys = ("family", "stage", "header_line", "header_text", "header_text_sha256", "m", "q", "bar",
            "bar_exact", "n_registrations")
    return [{k: f[k] for k in keys} for f in fam["families"]]


# ═══════════════════════════════════════════════════════ ONE FILING OVER ONE SET OF PATHS
class Filing:
    """The default filing reads the tree this file stands in; the suite builds a `Filing` over
    scratch copies (a door over a scratch contract, a scratch plan, a scratch output directory)."""

    def __init__(self, *, root=None, door=None, plan=None, leans=None, out_dir=None):
        self.root = Path(root) if root is not None else ROOT
        self.door = door if door is not None else PINS.Door(root=self.root)
        self.main = self.door.main
        self.plan = Path(plan) if plan is not None else self.root / PLAN_REL
        self.leans = Path(leans) if leans is not None else self.root / LEANS_REL
        self.out_dir = Path(out_dir) if out_dir is not None else self.root / OUT_REL

    # ── the pinned files ──
    def record(self, name: str) -> dict:
        return PINS.read_json(self.root / PROGRESS_DIR_REL / name)

    def pointer(self, rel: str, path=None) -> dict:
        return {"path": rel, "sha256": sha_bytes((path if path is not None else self.root / rel).read_bytes())}

    def texts(self) -> dict:
        """{key: {path, sha256}} of every text the filing pins by a sha read from the file; HALT
        RECORD-PIN unless the frozen ones re-hash to the TC12-LEANS record."""
        rec = self.record(LEANS_RECORD)
        out = {"resume_paste": self.pointer(RESUME_PASTE_REL), "leans": self.pointer(LEANS_REL, self.leans),
               "amendments": self.pointer(AMENDMENTS_REL), "review": self.pointer(REVIEW_REL),
               "plan": self.pointer(PLAN_REL, self.plan), "rulings": self.pointer(RULINGS_REL),
               "disclosures": self.pointer(DISCLOSURES_REL)}
        for key in ("leans", "review", "resume_paste"):
            want = rec["artifact_shas"].get(out[key]["path"], {}).get("sha256")
            if out[key]["sha256"] != want:
                halt("RECORD-PIN", f"{out[key]['path']} does not re-hash to the sha the TC12-LEANS record "
                                   f"certifies for it")
        if AM_ON_FILE not in (self.root / AMENDMENTS_REL).read_text(encoding="utf-8"):
            halt("RECORD-PIN", f"{AMENDMENTS_REL} does not hold AM-1 at filing [L-X.19]")
        return out

    def statistics(self) -> dict:
        """N_BOOT, the two seeds, the scored window's end and the era cut — each read from the
        file that supplies it [L-X.3, L-X.19].  HALT N-BOOT / SEED."""
        raw = (self.main / T11_SCORES_REL).read_bytes()
        cert = f"{PROGRESS_DIR_REL}/{R0_RECORD} {R0_FROZEN_KEY}"
        if sha_bytes(raw) != self.record(R0_RECORD)[R0_FROZEN_KEY].get(T11_SCORES_REL, {}).get("sha256"):
            halt("N-BOOT", f"{T11_SCORES_REL} does not re-hash to {cert}")
        scores = json.loads(raw.decode("utf-8"))
        if scores["n_boot"] != self.door.x_json(X_REG_PIN_REL)["n_boot"]:
            halt("N-BOOT", f"{T11_SCORES_REL} n_boot is not {X_REG_PIN_REL} n_boot")
        seed = self.door.pin(SEED_PIN)
        if seed != PINS.read_json(self.root / PROGRESS_REL)["seed"]:
            halt("SEED", f"the contract's seed {seed} is not {PROGRESS_REL}'s")
        return {
            "statistics": {
                "n_boot": scores["n_boot"],
                "n_boot_source": {"path": T11_SCORES_REL, "key": "n_boot", "certified_by": cert,
                                  "equal_to": {"path": X_REG_PIN_REL, "key": "n_boot"}},
                "seed": seed,
                "seed_source": {"path": PINS.CONTRACT_REL, "pin": SEED_PIN,
                                "lines": list(self.door.map_row(SEED_PIN)["lines"]),
                                "equal_to": {"path": PROGRESS_REL, "key": "seed"}},
                "seed_sens": scores["seed_sens"],
                "seed_sens_source": {"path": T11_SCORES_REL, "key": "seed_sens", "certified_by": cert}},
            "scored_window": {"end_ms": PINS.read_json(self.main / T11_ASOF_REL)[T11_ASOF_KEY],
                              "source": {"path": T11_ASOF_REL, "key": T11_ASOF_KEY}},
            "era_cut": {"ms": self.door.x_json(X_PINS_REL)[X_ERA_KEY],
                        "source": {"path": X_PINS_REL, "key": X_ERA_KEY,
                                   "certified_by": PINS.X_MANIFEST_REL}}}

    def law(self) -> tuple:
        """(law, law_source): TC11's hash law BY OBJECT, its file pinned by TC11's chain head —
        the head recomputed from the payloads — and never by a whole-file sha [L-X.19, L-0.24]."""
        t11 = PINS.read_json(self.main / T11_REG_REL)
        head = PINS.read_json(self.main / T11_PIN_REL)["head"]
        regs = t11["registrations"]
        if any(r["sha256"] != payload_sha(r) for r in regs) or chain_of(regs)[1] != head or t11["head"] != head:
            halt("LAW-HEAD", f"{T11_REG_REL} does not re-derive to the head {T11_PIN_REL} names")
        return t11["law"], {"path": T11_REG_REL, "key": "law", "head": head,
                            "head_source": {"path": T11_PIN_REL, "key": "head"}}

    def external_bytes(self, plan_bytes: bytes) -> dict:
        """{path: bytes} of every external file the plan's blocks declare; a copy under x_rec/ is
        held to its X_REC_MANIFEST row [O-4]."""
        out = {}
        for _, rid, block in plan_blocks(plan_bytes.decode("utf-8").split("\n")):
            try:
                declared = external_declared(carry(block, rid))
            except SystemExit:
                continue
            for path, _, _ in declared:
                p = self.main / path
                if path in out or not p.is_file():
                    continue
                raw = p.read_bytes()
                if path.startswith(X_REC_REL) and self.door.x_manifest().get(path) != sha_bytes(raw):
                    halt("EXTERNAL-SLICE", f"{path} is not at its X_REC_MANIFEST sha")
                out[path] = raw
        return out

    # ── the filing ──
    def build(self) -> dict:
        """The REGISTRATIONS.json document.  Writes nothing.  HALTs on the first law broken."""
        pre = self.door.prefix()                               # HALT CONTRACT-PREFIX / CONTRACT-TAIL
        fam = self.door.families()                             # HALT FAMILY-PARSE / -BAR / -MEMBER / -M-COUNT
        texts = self.texts()
        stats = self.statistics()
        plan_bytes, leans_bytes = self.plan.read_bytes(), self.leans.read_bytes()
        R = readings_of(leans_bytes)
        bodies, plan, found = derive(pre["lines"], fam, plan_bytes, R, self.external_bytes(plan_bytes),
                                     stats["statistics"])
        raise_first(found)
        laws = plan_laws(plan)
        for key in CLAUSE_KEYS:
            if laws["verdict_law"][key] not in R["common"]["ruler"]:
                halt("RULER-TEXT", f"the plan's verdict_law {key} is not a clause of the ruler sentence")
        chain, head = chain_of(bodies)
        law, law_source = self.law()
        doc = {"tier": TIER,
               "contract": {"path": pre["path"], "prefix_bytes": pre["prefix_bytes"],
                            "prefix_sha256": pre["prefix_sha256"], "n_lines": pre["n_lines"],
                            "whole_file_sha256_at_filing": pre["whole_file_sha256"]},
               "resume_paste": texts["resume_paste"], "leans": texts["leans"],
               "amendments": texts["amendments"], "review": texts["review"], "plan": texts["plan"],
               "rulings": texts["rulings"], "disclosures": texts["disclosures"],
               "families": families_filed(fam), "verdict_law": laws["verdict_law"], **stats,
               "registrations": bodies, "chain": chain, "head": head, "law": law, "law_source": law_source}
        shas = {p: sha_bytes((self.main / p).read_bytes()) for p in banned_external()
                if (self.main / p).is_file()}
        raise_first(PINS.census_sha_findings(REG_NAME, render(doc).decode("utf-8"), shas, len(GENESIS)))
        return doc

    def pin_of(self, doc: dict, reg_bytes: bytes) -> dict:
        """REGISTRY_PIN.json: the witness of the chain [L-X.20]."""
        laws = plan_laws(self.plan.read_bytes().decode("utf-8").split("\n"))
        stats = doc["statistics"]
        return {"tier": TIER,
                "registrations_file": {"path": f"{OUT_REL}/{REG_NAME}", "bytes": len(reg_bytes),
                                       "sha256": sha_bytes(reg_bytes)},
                "order_of_filing": [r["registration"] for r in doc["registrations"]],
                "registry_len": len(doc["registrations"]), "genesis": GENESIS, "head": doc["head"],
                "chain": [c["line_sha256"] for c in doc["chain"]],
                "registrations": {r["registration"]: {
                    "seq": r["seq"], "sha256": r["sha256"], "text_sha256": r["text_sha256"],
                    "text_lines": r["text_lines"], "prior_pct": r["prior_pct"], "family": r["family"],
                    "family_m": r["family_m"], "family_bar": r["family_bar"]} for r in doc["registrations"]},
                "families": doc["families"], "contract": doc["contract"],
                "resume_paste": doc["resume_paste"], "leans": doc["leans"], "amendments": doc["amendments"],
                "plan": doc["plan"], "review": doc["review"], "rulings": doc["rulings"],
                "disclosures": doc["disclosures"], "seed": stats["seed"], "seed_sens": stats["seed_sens"],
                "n_boot": stats["n_boot"], "law": doc["law"], "law_source": doc["law_source"],
                **{k: laws[k] for k in LAW_KEYS}}

    def inputs(self, doc: dict) -> dict:
        """The bytes `verify_filing` is handed, read from this filing's paths."""
        plan_bytes = self.plan.read_bytes()
        ext = self.external_bytes(plan_bytes)
        for r in doc.get("registrations", ()):
            for e in r.get("external_context", ()):
                p = self.main / e["path"]
                if e["path"] not in ext and p.is_file():
                    ext[e["path"]] = p.read_bytes()
        return {"contract_bytes": self.door.contract.read_bytes(), "ext_bytes": ext,
                "plan_bytes": plan_bytes, "leans_bytes": self.leans.read_bytes()}

    def file(self) -> tuple:
        """WRITE-ONCE [L-X.20]: HALT if either file exists; build; the built filing must pass its
        own verifier; then both files by exclusive create.  Nothing is ever overwritten."""
        reg_p, pin_p = self.out_dir / REG_NAME, self.out_dir / PIN_NAME
        for p in (reg_p, pin_p):
            if p.exists():
                halt("WRITE-ONCE", f"{p.name} exists in {self.out_dir.name}/ — the filing is write-once; "
                                   f"nothing was written")
        doc = self.build()
        reg_bytes = render(doc)
        pin = self.pin_of(doc, reg_bytes)
        raise_first(verify_filing(doc, pin, reg_bytes=reg_bytes, door=self.door, **self.inputs(doc)))
        self.out_dir.mkdir(parents=True, exist_ok=True)
        create(reg_p, reg_bytes)
        create(pin_p, render_sorted(pin))
        return reg_p, pin_p


def create(path: Path, body: bytes) -> None:
    """EXCLUSIVE CREATE: the file is made by this call or the call fails — no check-then-write."""
    with open(path, "xb") as f:
        f.write(body)


# ═══════════════════════════════════════════════════════ THE VERIFIER [L-X.22]
def _door_over(contract_bytes: bytes, door, scratch: str):
    """The pin door over exactly the bytes the verifier is handed (the ONE prefix function reads a
    path): the same STEP Q record, map and filed pins as `door`."""
    p = Path(scratch) / Path(PINS.CONTRACT_REL).name
    p.write_bytes(contract_bytes)
    return PINS.Door(root=door.root, contract=p, step_q=door.step_q, pins_dir=door.pins_dir,
                     amendments=door.amendments, main=door.main)


def verify_filing(doc: dict, pin: dict, contract_bytes: bytes, reg_bytes: bytes, ext_bytes: dict,
                  plan_bytes: bytes, leans_bytes: bytes, door=None) -> list:
    """The scorer's first act.  [] iff every detector of L-X.22 is silent.  Every finding begins
    with its detector's name; a HALT of the pin door is a finding carrying its own text."""
    door = door if door is not None else PINS.door()
    scratch = tempfile.mkdtemp(prefix="tierc12_reg_verify_")
    try:
        return _verify(doc, pin, _door_over(contract_bytes, door, scratch), reg_bytes, ext_bytes,
                       plan_bytes, leans_bytes)
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


def _verify(doc, pin, door, reg_bytes, ext_bytes, plan_bytes, leans_bytes) -> list:
    out = []
    try:
        pre = door.prefix()
    except SystemExit as e:
        return [finding_of(e)]                           # CONTRACT-PREFIX / CONTRACT-TAIL
    filed_c = doc.get("contract") or {}
    if any(filed_c.get(k) != pre[k] for k in ("path", "prefix_bytes", "prefix_sha256", "n_lines")):
        out.append("CONTRACT-PREFIX the filing's `contract` leaf does not name the STEP Q prefix")
    try:
        fam = door.families()
        seed = door.pin(SEED_PIN)
    except SystemExit as e:
        return out + [finding_of(e)]                     # FAMILY-PARSE / -BAR / -MEMBER / -M-COUNT
    lines = pre["lines"]
    if doc.get("families") != families_filed(fam):
        out.append("FAMILY-PARSE the filed families[] are not the pin door's parse of the prefix")
    stats = doc.get("statistics") or {}
    stated = all(k in stats for k in ("n_boot", "seed", "seed_sens"))
    if not stated:
        out.append("SEED the filing's `statistics` leaf does not state n_boot, seed and seed_sens")
        stats = {"n_boot": None, "seed": seed, "seed_sens": None}
    if stats.get("seed") != seed:
        out.append(f"SEED the filing's seed {stats.get('seed')!r} is not the contract's {seed}")
    for key, raw in (("plan", plan_bytes), ("leans", leans_bytes)):
        if (doc.get(key) or {}).get("sha256") != sha_bytes(raw):
            out.append(f"PLAN==LEANS the bytes handed as `{key}` do not hash to the filing's {key}.sha256")
    regs = doc.get("registrations") or []
    try:
        R = readings_of(leans_bytes)
        want, _, found = derive(lines, fam, plan_bytes, R, ext_bytes, stats)
        out += found
    except SystemExit as e:
        out.append(finding_of(e))
        R, want = None, []
    want = {b["registration"]: b for b in want}
    lmap = line_map(plan_bytes.decode("utf-8").split("\n"), PLAN_MAP_FROM, PLAN_MAP_TO, "plan §0") \
        if R is not None else []
    laws_row, heads, _ = roles(lmap, fam) if R is not None else (None, {}, [])
    by_lines = {tuple(r["lines"]): r for r in lmap}
    for r in regs:
        rid = r.get("registration")
        a, b = _pair(r.get("text_lines"))
        row = by_lines.get((a, b))
        text = r.get("text_of_record")
        try:
            recut = PINS.cut(lines, a, b)
        except SystemExit:
            recut = None
        if not isinstance(text, str) or text != recut or r.get("text_sha256") != sha_text(text) \
                or row is None or row["sha256"] != sha_text(text) \
                or row["object"] != TEXT_OBJ.format(id=rid, prior=r.get("prior_pct")) \
                or not text.lstrip().startswith(f"{rid} ") \
                or PRIOR_RX.findall(text)[:1] != [str(r.get("prior_pct"))]:
            out.append(f"TEXT-SLICE {rid}: text_of_record is not contract :{a}-{b} re-cut from the pinned "
                       f"prefix under the line map's sha, with its id and prior")
        own = fam["by_registration"].get(rid)
        header = next((f for f in fam["families"] if own and f["family"] == own["family"]), None)
        need = [tuple(x["lines"]) for x in (laws_row, heads.get(header["header_line"]) if header else None)
                if x is not None]
        ctx = r.get("context_of_record") or []
        bad = [c for c in ctx if tuple(c.get("lines") or ()) not in by_lines
               or c.get("text") is None or sha_text(c["text"]) != by_lines[tuple(c["lines"])]["sha256"]
               or c["text"] != "\n".join(lines[c["lines"][0] - 1:c["lines"][1]])]
        if bad or [tuple(c.get("lines") or ()) for c in ctx] != need:
            out.append(f"CONTEXT-SLICE {rid}: context_of_record is not the LAWS slice and its family "
                       f"header, each a row of the line map re-cut from the prefix")
        c = carried_of(r)
        ext, found = external_items([(e.get("path"), e.get("sha256"), list(_pair(e.get("lines"))))
                                     for e in r.get("external_context") or []
                                     if None not in _pair(e.get("lines"))], ext_bytes, rid)
        out += found
        if ext != (r.get("external_context") or []) \
                or [(e["path"], e["sha256"], e["lines"]) for e in ext] != external_declared(c):
            out.append(f"EXTERNAL-SLICE {rid}: external_context is not the slices its labels declare, "
                       f"re-cut from bytes of the declared sha")
        if r.get("sha256") != payload_sha(r):
            out.append(f"PAYLOAD-SHA {rid}: the payload sha does not re-derive from the filed body")
        if r.get("seed") != seed:
            out.append(f"SEED {rid}: filed at seed {r.get('seed')!r}, not the contract's {seed}")
        if own is None or r.get("family") != own["family"]:
            out.append(f"FAMILY-MEMBER {rid}: filed under family {r.get('family')!r}; the contract stands "
                       f"it under {own['family'] if own else 'no header'}")
        elif r.get("family_m") != own["m"]:
            out.append(f"FAMILY-M-COUNT {rid}: filed at m = {r.get('family_m')!r}; its header declares "
                       f"{own['m']}")
        elif r.get("family_bar") != own["bar"]:
            out.append(f"FAMILY-BAR {rid}: filed at the bar {r.get('family_bar')!r}; its header's is "
                       f"{own['bar']} ({own['bar_exact']})")
        if R is not None:
            out += [x for x in carried_findings(c, R, text if isinstance(text, str) else "",
                                                header["header_text"] if header else "", stats)
                    if x not in out]
        w = want.get(rid)
        if w is None:
            out.append(f"SPEC-VERBATIM {rid}: the plan carries no block this body can be held to")
            continue
        diff = [k for k in SPEC_KEYS if (r.get("operative_spec") or {}).get(k) != w["operative_spec"][k]]
        diff += [RULE_FIELD] if r.get(RULE_FIELD) != w[RULE_FIELD] else []
        diff += ["(keys)"] if tuple(r.get("operative_spec") or {}) != SPEC_KEYS else []
        if diff:
            out.append(f"SPEC-VERBATIM {rid}: {diff} differ from the plan's block carried by L-X.18's law")
    if [r.get("registration") for r in regs] != list(want) and R is not None:
        out.append(f"SPEC-VERBATIM the filing holds {[r.get('registration') for r in regs]}; the plan "
                   f"carries {list(want)}")
    chain, head = chain_of(regs)
    firsts = [(r.get("text_lines") or [0])[0] for r in regs]
    if chain != doc.get("chain") or [r.get("seq") for r in regs] != list(range(1, len(regs) + 1)) \
            or firsts != sorted(firsts):
        out.append("CHAIN the filed chain does not re-derive from the genesis string over the filed "
                   "registrations in seq order (ascending first text line)")
    if doc.get("head") != head:
        out.append("HEAD-PIN the filed head is not the end of the re-derived chain")
    pin = pin or {}
    file_pin = pin.get("registrations_file") or {}
    if pin.get("head") != head or pin.get("head") != doc.get("head") or pin.get("genesis") != GENESIS \
            or pin.get("chain") != [c["line_sha256"] for c in chain]:
        out.append("HEAD-PIN REGISTRY_PIN.json's head, genesis or chain is not the re-derived chain's")
    if file_pin.get("sha256") != sha_bytes(reg_bytes) or file_pin.get("bytes") != len(reg_bytes):
        out.append("HEAD-PIN REGISTRY_PIN.json's registrations_file is not the filing's bytes")
    for r in regs:
        pr = (pin.get("registrations") or {}).get(r.get("registration")) or {}
        if any(pr.get(k) != r.get(k) for k in ("seq", "sha256", "text_sha256", "text_lines", "prior_pct",
                                               "family", "family_m", "family_bar")):
            out.append(f"HEAD-PIN REGISTRY_PIN.json's entry for {r.get('registration')} is not the filing's")
    return out


def _pair(v) -> tuple:
    return (v[0], v[1]) if isinstance(v, list) and len(v) == len(("a", "b")) else (None, None)


def filed(root=ROOT) -> tuple:
    """(doc, pin, reg_bytes) of the filed pair; HALT HEAD-PIN if either is not on file."""
    d = Path(root) / OUT_REL
    if not (d / REG_NAME).is_file() or not (d / PIN_NAME).is_file():
        halt("HEAD-PIN", f"{OUT_REL}/{REG_NAME} and {PIN_NAME} are not both on file")
    reg_bytes = (d / REG_NAME).read_bytes()
    return json.loads(reg_bytes.decode("utf-8")), PINS.read_json(d / PIN_NAME), reg_bytes


def verify(root=ROOT) -> list:
    """The filed pair against the tree it stands in."""
    doc, pin, reg_bytes = filed(root)
    f = Filing(root=root)
    return verify_filing(doc, pin, reg_bytes=reg_bytes, door=f.door, **f.inputs(doc))


def stamp(root=ROOT) -> dict:
    """{registry_head, registrations_sha256} — what every regbook STATUS, arm sidecar and book
    manifest carries [L-X.21 clause 2], read from REGISTRY_PIN.json."""
    _, pin, _ = filed(root)
    return {"registry_head": pin["head"], "registrations_sha256": pin["registrations_file"]["sha256"]}


def registration(rid: str, root=ROOT) -> dict:
    """The filed body of one registration; HALT HEAD-PIN on an id the registry does not hold."""
    hit = [r for r in filed(root)[0]["registrations"] if r["registration"] == rid]
    if len(hit) != 1:
        halt("HEAD-PIN", f"{rid!r} is not a registration of the filed registry")
    return hit[0]


# ═══════════════════════════════════════════════════════ ATTEST-REG [L-X.21 clause 3, at filing]
def _in(rel: str, patterns) -> bool:
    return any(rel == p or (p.endswith(TREE) and rel.startswith(p[:-len(TREE)] + "/")) for p in patterns)


def attest_sets(root=ROOT) -> tuple:
    """(PRE_REG, REG_SET) as the walk judges them: the typed patterns, and the artifact paths of
    STEP Q, TC12-R0 and TC12-LEANS read from those records."""
    pre = list(PRE_REG) + list(PRE_REG_SCRIPTS)
    for name in PRE_REG_RECORDS:
        p = Path(root) / PROGRESS_DIR_REL / name
        if p.is_file():
            for path in PINS.read_json(p).get("artifact_shas", {}):
                pre.append(path[len(T12_REL) + 1:] if path.startswith(T12_REL + "/") else path)
    return tuple(sorted(set(pre))), REG_SET


def attest_walk(root=ROOT) -> dict:
    """{path: sha256} of every file under research_outputs/tierc12/ (ignored and untracked files
    included) and of scripts/tierc12_*.py — paths relative to research_outputs/tierc12/ unless they
    begin scripts/ — except ATTEST_REG.json itself."""
    root, out = Path(root), {}
    base = root / T12_REL
    for d, dirs, names in os.walk(base):
        dirs.sort()
        for x in sorted(names):
            p = Path(d) / x
            rel = p.relative_to(base).as_posix()
            if rel != ATTEST_SELF:
                with p.open("rb") as f:
                    out[rel] = hashlib.file_digest(f, "sha256").hexdigest()
    for p in sorted((root / SCRIPTS).glob(SCRIPT_GLOB)):
        out[SCRIPTS + p.name] = sha_bytes(p.read_bytes())
    return dict(sorted(out.items()))


def attest_findings(root=ROOT, walk=None) -> list:
    """ATTEST-REG: a file outside PRE_REG ∪ REG_SET, a .parquet outside x_rec/, a tierc12 script
    outside the typed set, or no registry on file (the listing is taken AFTER --file)."""
    walk = attest_walk(root) if walk is None else walk
    pre, reg = attest_sets(root)
    out = [f"ATTEST-REG {p}: on disk at filing and outside PRE_REG ∪ REG_SET"
           for p in walk if not _in(p, pre) and not _in(p, reg)]
    out += [f"ATTEST-REG {p}: a .parquet outside x_rec/ at filing — no book exists before the registry"
            for p in walk if p.endswith(PARQUET) and not p.startswith(X_REC_DIR)]
    out += [f"ATTEST-REG {p}: not on file — the listing is taken after --file"
            for p in (f"registrations/{REG_NAME}", f"registrations/{PIN_NAME}") if p not in walk]
    return sorted(set(out))


def attest_doc(root=ROOT) -> dict:
    """The ATTEST_REG.json document; HALT ATTEST-REG on any finding (nothing is then written)."""
    walk = attest_walk(root)
    raise_first(attest_findings(root, walk))
    pre, reg = attest_sets(root)
    pin = PINS.read_json(Path(root) / OUT_REL / PIN_NAME)
    return {"what": ATTEST_WHAT, "law": ATTEST_LAW, "tier": TIER,
            "taken_after": {"registrations_sha256": walk[f"registrations/{REG_NAME}"],
                            "registry_head": pin["head"]},
            "pre_reg": list(pre), "reg_set": list(reg), "n_files": len(walk),
            "files": [{"path": p, "sha256": s} for p, s in walk.items()],
            "absent": [p for p in reg if p not in walk and p != ATTEST_SELF]}


# ═══════════════════════════════════════════════════════ THE COMMAND LINE
def main(argv) -> int:
    opt = {a.split("=", 1)[0]: a.split("=", 1)[1] for a in argv if a.startswith("--") and "=" in a}
    f = Filing(plan=opt.get("--plan"), leans=opt.get("--leans"), out_dir=opt.get("--out-dir"))
    if "--attest" in argv:
        doc = attest_doc(ROOT)
        (ROOT / OUT_REL / ATTEST_NAME).write_bytes(render_sorted(doc))
        print(f"{OUT_REL}/{ATTEST_NAME} written: {doc['n_files']} files listed, {len(doc['absent'])} "
              f"REG_SET member(s) not yet on disk {doc['absent']}")
        return 0
    if "--verify" in argv:
        found = verify(ROOT)
        for x in found:
            print(x)
        print(f"REGISTRY: {'VERIFIED — head ' + filed(ROOT)[0]['head'] if not found else str(len(found)) + ' finding(s)'}")
        return 1 if found else 0
    if "--file" in argv:
        reg_p, pin_p = f.file()
        doc = json.loads(reg_p.read_bytes().decode("utf-8"))
        print(f"FILED {reg_p.name} sha256 {sha_bytes(reg_p.read_bytes())} · {pin_p.name} sha256 "
              f"{sha_bytes(pin_p.read_bytes())}")
    else:
        doc = f.build()
        reg_bytes = render(doc)
        found = verify_filing(doc, f.pin_of(doc, reg_bytes), reg_bytes=reg_bytes, door=f.door, **f.inputs(doc))
        for x in found:
            print(x)
        if found:
            print(f"DRY RUN: {len(found)} finding(s) — nothing would be filed")
            return 1
        print("DRY RUN: nothing written (file with --file)")
    for r in doc["registrations"]:
        print(f"{r['seq']} {r['registration']:<10} [{r['prior_pct']}%] {r['family']} m={r['family_m']} "
              f"bar {r['family_bar']} · contract :{r['text_lines'][0]}-{r['text_lines'][1]} · text "
              f"{r['text_sha256']} · payload {r['sha256']}")
        if "--texts" in argv:
            print(r["text_of_record"])
    print(f"contract prefix {doc['contract']['prefix_sha256']} ({doc['contract']['prefix_bytes']} B) · "
          f"LEANS {doc['leans']['sha256']} · plan {doc['plan']['sha256']}")
    print(f"head {doc['head']}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
