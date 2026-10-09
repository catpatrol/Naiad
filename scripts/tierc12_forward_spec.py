#!/usr/bin/env python
"""TIER-C12 · TC12-REG.ledger-spec — THE FOURTH BOOK'S SPEC AND THE FIVE-LINE LEDGER
[LEANS L-L.1 · L-L.2 · L-L.3 · L-L.4 · L-L.5 · L-L.6 · L-L.8 · L-L.14 · L-L.17; O-24; contract :108-110, :122].

"fourth frozen book = v6 with P-ADM-1's refusal" (contract :108); "F-LEDGER (append-only on the three existing
books; the fourth re-hashes)" (:122).  A plain process: the stdlib, the contract pin door and
tierc12_progress.certified.  NO env shim, no numpy, no pandas; it reads NO BAR and no book.  It is on L-0.22's
VA_BLIND_T: the files it may open are typed below (SPEC_READS_T) and every one is read sha-first.

WHAT IT FILES (research_outputs/tierc12/forward/), ONCE:
  BOOK_SPEC_COMBINED.json  the fourth book `gated-v6-combined`, hashed AFRESH into its own document (X's spec
                           is never rewritten to hold four books).  Every value is read from a named source:
                           the gate text of record is the ONE element of the filed registry's
                           registrations[P-ADM-1].operative_spec.arms that matches ^`scored`\\s; its two
                           components are TC11's P-AGE-1 and P-WIN-1 `operative_spec.scored_arm`, TC11's
                           registry pinned by its chain head VALUE and by each payload sha (never by a
                           whole-file sha, which the "tc11-stamp" close act moves — L-0.24); the card, the
                           roles and the panel are X's `books.v6`, by object; `n_law` fixes the row set of
                           record of any later forward score before a strip bar is on disk; `flags` states
                           the three row flags and files the STEP Q instant (the fourth book's own freeze
                           instant is written later, once, by the orchestrator: forward/BOOK4_FREEZE.json).
                           WRITE-ONCE: an existing file must be rebuilt byte-equal (HALT FWD-SPEC-FROZEN).
  FORWARD_LEDGER.jsonl     TC12's ledger of record.  Its first bytes ARE X's ledger (the x_rec byte copy,
                           sha asserted against its manifest row) — a byte-prefix law, not a re-serialisation
                           — continued by ONE more line, the fourth book's `book_open`, whose `spec_sha256`
                           is the sha of BOOK_SPEC_COMBINED.json and whose `prev_sha256` is X's head.  Rows
                           and the one refresh line are TC12-L's.  TC11's two-line ledger is a different
                           chain law: cited by sha, re-verified by its own law re-implemented here, never
                           continued.

THE CHAIN LAW IS scripts/forward_log.py's (O-24).  Its six functions stand here as PORTS and are exposed as
the namespace `FL` (so X's ported functions keep X's own call sites): forward_log.main holds function-local
imports whose static closure reaches a module the import-closure wall forbids to every decision module
(L-0.22 (ii)), so this module does not import it — a default on mechanics, reported to the orchestrator as an
amendment proposal and in force until ruled.  Every run HALTs (FWD-FL-PORT) unless the ports are AST-identical to scripts/forward_log.py at the sha
X's spec names for it; the suite imports forward_log itself as the independent verifier (F-LEDGER [CHAIN],
F-PORT).  Two guards forward_log does not have are applied before every append: the line must serialise
under allow_nan=False (FWD-NAN), and no string in it may hold a character `str.splitlines` breaks on
(FWD-LINE-BREAK) — forward_log.read_lines splits on splitlines and writes such characters raw.

THE THREE GATE PREDICATES live here and nowhere else (L-L.2): pure functions of a row's `tide_band` and `lag`.
OLD is the last element of X's BAND_CODES, read from X's source TEXT by ast.literal_eval; the window-age cut is
the contract pin `adm.lag_cut`, read through the pin door at each call and never copied into a constant.

A DIARY, NOT A SCOREBOARD (forward_log's own law, L-L.15): this module computes nothing over a ledger row's
values — it holds no aggregate of any kind.

API (the ledger module of TC12-L imports these and holds no copy):
  Reader(root=None)                the env-free sha-first reader.  An ARMED process hands `sources` an object
                                   with the same methods over the shim's verified readers instead:
                                   .root · .path(rel) · .x(rel) · .x_row(rel) · .tc11(rel) · .tc11_entry(rel)
                                   · .tc11_plain(rel) · .tc12(rel) · .lineage(rel)
  sources(reader=None) -> dict     every verified input (bytes and parsed documents)
  spec_doc(S) -> dict              the fourth spec's content — a pure function of `sources` and the pin door
  render_json(doc) -> bytes        X's rendering of a spec document
  freeze_spec(out, body) -> sha    write-once
  read_spec(out) -> (doc, sha, bytes)
  open_ledger(out, S, spec_bytes) -> [lines]   the five-line ledger (atomic; reproduces it byte for byte)
  atomic_append(record, bodies, base_bytes, check) -> bytes   TC11's writer law, for every TC12 ledger write
  build(out=None, reader=None) -> dict         sources -> spec -> ledger
  chained · body_of · append · book_open_body · chain_findings · parse_lines · line_findings
  FL.canonical · FL.chain_hash · FL.read_lines · FL.last_sha · FL.append_entry · FL.verify_chain · FL.GENESIS
  old_code(reader=None) · lag_cut() · p_age_1_refuses(row) · p_win_1_refuses(row) · p_adm_1_refuses(row)
  tc11_chain(raw) -> (lines, findings)         TC11's chain law, re-implemented (no TC11 import)
  iso(ms) · iso_ms(text) · sha_bytes(b)

Run (TC12-REG.ledger-spec; no env, no network, no bar):
  ~/venvs/naiad/bin/python -B /Users/luis/Naiad/scripts/tierc12_forward_spec.py [--out-dir=DIR]
HALTS, each naming its detector: SPEC-READS · FWD-READ · FWD-REGISTRY · FWD-T11-REGISTRY · FWD-GATE-TEXT ·
FWD-OLD-TEXT · FWD-CUT-TEXT · FWD-OLD-CODE · FWD-OPENING · FWD-NMIN · FWD-SCORE-EDGE · FWD-STEP-Q ·
FWD-ANCESTOR · FWD-SPEC-PATH · FWD-FL-PORT · FWD-KINDS · FWD-SPEC-FROZEN · FWD-OPEN · FWD-CHAIN · FWD-NAN ·
FWD-LINE-BREAK · FWD-BAND-NONE · FWD-OUT.
"""
from __future__ import annotations

import ast
import hashlib
import json
import os
import re
import sys
import types
from datetime import datetime, timedelta, timezone
from pathlib import Path

import tierc12_pins as PINS
import tierc12_progress as PG

ROOT = Path(__file__).resolve().parents[1]
TIER = "TIER-C12"
STAGE = "TC12-REG.ledger-spec"
T12 = "research_outputs/tierc12"
T11 = "research_outputs/tierc11"
XR = T12 + "/x_rec"
OUT_REL = T12 + "/forward"
SPEC_NAME = "BOOK_SPEC_COMBINED.json"
LEDGER_NAME = "FORWARD_LEDGER.jsonl"
FREEZE_REL = OUT_REL + "/BOOK4_FREEZE.json"            # the orchestrator's, written after this record's commit
BUILD_DIR = "_det_build"                               # the atomic write's scratch (git-ignored `_det_*/`)
DET_PREFIX = "_det_"

# ── the files this tool may open [L-L.3 SPEC_READS_T] — every one read sha-first; the 18 lineage files are
#    added BY OBJECT from X's spec (`path_modules`); the contract is read by the pin door, the two progress
#    records by tierc12_progress.  No path here is a tape, a book, a journal or a value-area table.
SPEC_READS_T = (
    "exchange/queue/2026-10-08_TC12_APOLLO.md",
    "research_outputs/tierc12/progress/STEP_Q.json",
    "research_outputs/tierc12/progress/TC12-R0.json",
    "research_outputs/tierc12/registrations/REGISTRATIONS.json",
    "research_outputs/tierc12/registrations/REGISTRY_PIN.json",
    "research_outputs/tierc12/x_rec/X_REC_MANIFEST.json",
    "research_outputs/tierc12/x_rec/tierc11x/forward/FORWARD_LEDGER.jsonl",
    "research_outputs/tierc12/x_rec/tierc11x/forward/BOOK_SPECS.json",
    "research_outputs/tierc12/x_rec/scripts/tc11x_forward.py",
    "research_outputs/tierc12/x_rec/scripts/tc11x_books.py",
    "research_outputs/tierc11/forward/FORWARD_LEDGER.jsonl",
    "research_outputs/tierc11/registrations/REGISTRATIONS.json",
    "research_outputs/tierc11/registrations/REGISTRY_PIN.json",
    "research_outputs/tierc11/LEANS.md",
    "research_outputs/tierc11/data/AS_OF_PIN.json",
    "research_outputs/tierc11/PROGRESS.json",
    "research_outputs/tierc12/close/TC11_STAMP_MAP.json",
)
REG_REL = T12 + "/registrations/REGISTRATIONS.json"
REG_PIN_REL = T12 + "/registrations/REGISTRY_PIN.json"
X_MANIFEST_REL = XR + "/X_REC_MANIFEST.json"
X_LEDGER_REL = XR + "/tierc11x/forward/FORWARD_LEDGER.jsonl"
X_SPEC_REL = XR + "/tierc11x/forward/BOOK_SPECS.json"
XF_REL = XR + "/scripts/tc11x_forward.py"
XB_REL = XR + "/scripts/tc11x_books.py"
T11_LEDGER_REL = T11 + "/forward/FORWARD_LEDGER.jsonl"
T11_REG_REL = T11 + "/registrations/REGISTRATIONS.json"
T11_PIN_REL = T11 + "/registrations/REGISTRY_PIN.json"
T11_LEANS_REL = T11 + "/LEANS.md"
T11_ASOF_REL = T11 + "/data/AS_OF_PIN.json"
T11_PROGRESS_REL = T11 + "/PROGRESS.json"
STAMP_MAP_REL = T12 + "/close/TC11_STAMP_MAP.json"
FL_REL = "scripts/forward_log.py"
X_OWN_PREFIX = "scripts/tc11x_"                        # X's own three path modules: not carried
STEP_Q_ID, R0_ID = "STEP Q", "TC12-R0"
R0_FROZEN_KEY = "frozen_estate_shas_at_r0"

# ── names (texts; no number) ──
BOOK4 = "gated-v6-combined"
BASE_BOOK = "v6"
OLD_GATED = "gated-v6-oldtide"
ROLE = {BOOK4: "of record"}
TITLE = {BOOK4: BOOK4 + " (of record)"}
RUNNER = "the v6 ride, post-filtered"
K_OPEN, K_REFRESH, K_ROW = "book_open", "refresh", "row"
CHAIN_FIELDS = ("prev_sha256", "entry_sha256")         # forward_log's two chain fields; == X's literal (F-PORT)
REG_ADM, REG_AGE, REG_WIN = "P-ADM-1", "P-AGE-1", "P-WIN-1"
PIN_CUT, PIN_OPENING, PIN_N_MIN = "adm.lag_cut", "ledger.opening", "ledger.n_min"
SHA_KEYS = ("text_sha256", "sha256")                   # the registries' payload law: the body without its shas
ROW_FIELDS_ADDED = ("p_age_1_refuses", "p_win_1_refuses", "p_adm_1_refuses", "in_o9_scored_window",
                    "entered_before_gate_text_filed", "entered_before_book_frozen")
T11_GENESIS_KIND, T11_REFRESH_KIND = "GENESIS", "REFRESH"
T11_SHA_FIELD, T11_PREV_FIELD = "line_sha256", "prev"
ROLE_PERIODS = ("tide_f", "tide_s", "trg_f", "trg_s", "win_f", "win_s")
FL_PORTS_T = ("canonical", "chain_hash", "read_lines", "last_sha", "append_entry", "verify_chain")
FL_CHANGED_T = {"last_sha": ("lines[-1]", "lines[len(lines) - 1]")}    # the ONE declared difference, as text

SCORED_RX = re.compile(r"`scored`\s")
OLD_REFUSE_RX = re.compile(r"tide_band == '([^']+)'")
CUT_RX = re.compile(r"entry_i - arm_i >= (\d+)")
LT6_BLOCK_RX = re.compile(r"\*\*L-T\.6 FORWARD LEDGER\*\*\n(.*?)\n\n", re.S)
LT6_OPENING_RX = re.compile(r"It opens at \*\*(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ)\*\* \(TC10's pin\)")
LT6_N_RX = re.compile(r"unscored until its own n ≥ (\d+)")
STEP_Q_RX = re.compile(r"committed (\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ)")
OLD_NEEDLE = "{code} OLD"
EDGES_NEEDLE = "tierc9._trailing_edges"
ISO_SECONDS = "%Y-%m-%dT%H:%M:%SZ"
EPOCH = datetime.fromtimestamp(0, tz=timezone.utc)

STRUCTURE_LAW = (
    "S1 forward_log.verify_chain(path) is ok",
    "S2 every line kind is one of X's chain.kinds",
    "S3 the raw bytes of the first lines are X's ledger (the prefix law is on bytes); they open X's book_order "
    "in order and name X's spec sha; the line after them is X's refresh",
    "S4 exactly ONE book_open follows X's lines; it is the next line; its book is the fourth id; its "
    "spec_sha256 is the sha of the bytes of BOOK_SPEC_COMBINED.json and differs from X's spec sha; its "
    "opening_ms and n_min equal those of X's book_open lines",
    "S5 every row line names one of the four books, carries exactly row_fields + row_fields_added + the two "
    "chain fields, and no (book, symbol, entry_ms) occurs twice",
    "S6 the pins of the refresh lines strictly increase; the file never ends on a row line; inside one refresh "
    "block rows stand in book order, then (entry_close_ms, symbol)",
    "S7 every row of a gated book has, earlier in the file, the base row of the same key, equal on every "
    "field but `book`",
)
DECLARED_DIFFERENCE = (
    "X's chain_findings (scripts/tc11x_forward.py) reports any book_open after its third line; run on this "
    "file it reports the fourth book's book_open, by design. TC12's structure law admits exactly one more "
    "book_open, directly after X's lines. X's file and X's module are untouched.")
T11_CHAIN_LAW = (
    "TC11's law, not forward_log's: line_sha256 = sha256(canonical JSON of the line without line_sha256), "
    "`prev` INSIDE the line (genesis: the zeros), canonical = sort_keys, compact separators, ensure_ascii "
    "False, allow_nan False, written compact. Under forward_log.canonical a field named line_sha256 would be "
    "hashed into its own digest, so this head cannot be a prev_sha256 of TC12's chain: the file is CITED, "
    "never appended, never continued.")


def halt(tag: str, msg: str):
    raise SystemExit(f"HALT {tag}: {msg}")


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def iso(ms: int) -> str:
    """An epoch-ms instant as X's ledger writes it (seconds precision, Z)."""
    return (EPOCH + timedelta(milliseconds=int(ms))).strftime(ISO_SECONDS)


def iso_ms(text: str) -> int:
    t = datetime.strptime(text, ISO_SECONDS).replace(tzinfo=timezone.utc)
    return (t - EPOCH) // timedelta(milliseconds=1)


def out_dir() -> Path:
    return ROOT / OUT_REL


# ═══════════════════════════════════════════════════════ THE CHAIN LAW — scripts/forward_log.py, PORTED
# forward_log's diary path is not TC12's: every call here passes its path, and an omitted one raises.
LOG_PATH = None
GENESIS = "0" * len(hashlib.sha256(b"").hexdigest())


# PORT VERBATIM <- scripts/forward_log.py:67-76 sha256 74e9657fbcf26cce3040ee52d28a96bc1cf60897e375ba26a09b2e13676e1967
def canonical(entry):
    """Canonical JSON of an entry EXCLUDING its own sha.

    A digest cannot cover itself, so `entry_sha256` is removed before hashing.
    Sorted keys and compact separators make the bytes independent of field
    order, so re-reading and re-hashing a stored line reproduces the digest.
    """
    body = {k: v for k, v in entry.items() if k != "entry_sha256"}
    return json.dumps(body, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False)


# PORT VERBATIM <- scripts/forward_log.py:79-82 sha256 74e9657fbcf26cce3040ee52d28a96bc1cf60897e375ba26a09b2e13676e1967
def chain_hash(entry, prev_sha256):
    """entry_sha256 = sha256(canonical_json(entry_without_own_sha) + prev_sha256)."""
    blob = (canonical(entry) + str(prev_sha256)).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


# PORT VERBATIM <- scripts/forward_log.py:85-103 sha256 74e9657fbcf26cce3040ee52d28a96bc1cf60897e375ba26a09b2e13676e1967
def read_lines(path=LOG_PATH):
    """Raw entries in file order.  For APPEND and VERIFY only.

    Deliberately not a sampling surface: nothing here selects, filters or
    combines entries for analysis.  `entries_of_kind` is the only selector and
    it requires an explicit kind (F-F4).
    """
    p = Path(path)
    if not p.exists():
        return []
    out = []
    for i, line in enumerate(p.read_text(encoding="utf-8").splitlines()):
        if not line.strip():
            continue
        try:
            out.append(json.loads(line))
        except ValueError as exc:
            raise ValueError(f"{p.name}:{i + 1} is not valid JSON: {exc}") from exc
    return out


# PORT CHANGED <- scripts/forward_log.py:106-108 sha256 74e9657fbcf26cce3040ee52d28a96bc1cf60897e375ba26a09b2e13676e1967
# (the one difference, FL_CHANGED_T: the last line is indexed len(lines) - 1 — F-TYPED's rule (G) names no
#  referee for this module, so forward_log's negative index literal cannot stand here)
def last_sha(path=LOG_PATH):
    lines = read_lines(path)
    return lines[len(lines) - 1]["entry_sha256"] if lines else GENESIS


# PORT VERBATIM <- scripts/forward_log.py:152-166 sha256 74e9657fbcf26cce3040ee52d28a96bc1cf60897e375ba26a09b2e13676e1967
def append_entry(entry, path=LOG_PATH):
    """Append one entry.  NEVER rewrites, NEVER reorders (F-F2)."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    expected_prev = last_sha(p)
    if entry["prev_sha256"] != expected_prev:
        raise ValueError(
            f"refusing to append: prev_sha256 {entry['prev_sha256'][:12]}... "
            f"does not match the log head {expected_prev[:12]}.... Rewriting "
            f"history is refused; append a new line instead.")
    if entry["entry_sha256"] != chain_hash(entry, entry["prev_sha256"]):
        raise ValueError("entry_sha256 does not match the entry's own content")
    with p.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(entry, sort_keys=True, ensure_ascii=False) + "\n")
    return entry


# PORT VERBATIM <- scripts/forward_log.py:209-232 sha256 74e9657fbcf26cce3040ee52d28a96bc1cf60897e375ba26a09b2e13676e1967
def verify_chain(path=LOG_PATH):
    """F-F1/F-F2 -- walk the chain and report the first break.

    Returns integrity metadata only.  `checked` counts LINES for the integrity
    report; it is not a statistic about trading, and nothing here touches
    outcome fields.
    """
    lines = read_lines(path)
    prev = GENESIS
    for i, e in enumerate(lines):
        if e.get("prev_sha256") != prev:
            return {"ok": False, "checked": i, "first_bad_line": i + 1,
                    "reason": "prev_sha256 does not match the previous entry's "
                              "digest -- a line was inserted, removed or reordered",
                    "id": e.get("id")}
        recomputed = chain_hash(e, prev)
        if recomputed != e.get("entry_sha256"):
            return {"ok": False, "checked": i, "first_bad_line": i + 1,
                    "reason": "entry_sha256 does not match the line's own "
                              "content -- the line was edited after it was written",
                    "id": e.get("id")}
        prev = e["entry_sha256"]
    return {"ok": True, "checked": len(lines), "head": prev,
            "first_bad_line": None, "reason": None}


# The namespace X's ported functions call (`FL.chain_hash`, `FL.last_sha`, …).  If the default is overruled,
# the one line `import forward_log as FL` replaces this block and the six ports above.
FL = types.SimpleNamespace(GENESIS=GENESIS, canonical=canonical, chain_hash=chain_hash, read_lines=read_lines,
                           last_sha=last_sha, append_entry=append_entry, verify_chain=verify_chain)


def _function(text: str, name: str):
    hit = [n for n in ast.parse(text).body if isinstance(n, ast.FunctionDef) and n.name == name]
    return hit[0] if len(hit) == 1 else None


def fl_port_findings(fl_text: str, own_text: str) -> list:
    """FWD-FL-PORT: a port of FL_PORTS_T that is not AST-identical to forward_log's function — after the ONE
    declared text substitution for a name of FL_CHANGED_T — in the two source TEXTS given."""
    out = []
    for name in FL_PORTS_T:
        theirs, ours = _function(fl_text, name), _function(own_text, name)
        if theirs is None or ours is None:
            out.append(f"FWD-FL-PORT {name}: not one module-level function of that name on both sides")
            continue
        want = ast.dump(theirs)
        if name in FL_CHANGED_T:
            old, new = FL_CHANGED_T[name]
            seg = ast.get_source_segment(fl_text, theirs)
            if seg.count(old) != 1:
                out.append(f"FWD-FL-PORT {name}: forward_log's text holds `{old}` {seg.count(old)} times, not once")
                continue
            want = ast.dump(ast.parse(seg.replace(old, new)).body[0])
        if ast.dump(ours) != want:
            out.append(f"FWD-FL-PORT {name}: the port is not forward_log's function"
                       + (" under its one declared substitution" if name in FL_CHANGED_T else " (AST)"))
    return out


# ═══════════════════════════════════════════════════════ THE CHAIN — X's functions, PORTED
# PORT VERBATIM <- research_outputs/tierc12/x_rec/scripts/tc11x_forward.py:590-594 sha256 33f65b5eca8e50dfce6690bb827270f7de1cf7207ef14245416210ce88bbe80b
def chained(body: dict, prev: str) -> dict:
    """A ledger line: body + prev_sha256, entry_sha256 = forward_log.chain_hash (verbatim)."""
    line = dict(body, prev_sha256=prev)
    line["entry_sha256"] = FL.chain_hash(line, prev)
    return line


# PORT VERBATIM <- research_outputs/tierc12/x_rec/scripts/tc11x_forward.py:597-598 sha256 33f65b5eca8e50dfce6690bb827270f7de1cf7207ef14245416210ce88bbe80b
def body_of(line: dict) -> dict:
    return {k: v for k, v in line.items() if k not in CHAIN_FIELDS}


def _strings(o):
    """Every string of a JSON value, keys included."""
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for k, v in o.items():
            yield from _strings(k)
            yield from _strings(v)
    elif isinstance(o, (list, tuple)):
        for v in o:
            yield from _strings(v)


def line_findings(line: dict) -> list:
    """THE TWO GUARDS forward_log does not have [L-L.5].  FWD-NAN: the line does not serialise under
    allow_nan=False.  FWD-LINE-BREAK: a string of the line holds a character `str.splitlines` breaks on."""
    out = []
    try:
        json.dumps(line, sort_keys=True, ensure_ascii=False, allow_nan=False)
    except ValueError as e:
        out.append(f"FWD-NAN: a {line.get('kind')} line does not serialise under allow_nan=False ({e}) — "
                   f"forward_log would write the bare token [L-L.5]")
    for s in _strings(line):
        bad = sorted({c for c in s if len(("a" + c + "b").splitlines()) > 1})
        if bad:
            out.append(f"FWD-LINE-BREAK: a string of a {line.get('kind')} line holds "
                       f"{', '.join(f'U+{ord(c):04X}' for c in bad)} — forward_log.read_lines splits on "
                       f"str.splitlines and would read one line as two [L-L.5]")
    return out


# PORT CHANGED <- research_outputs/tierc12/x_rec/scripts/tc11x_forward.py:601-607 sha256 33f65b5eca8e50dfce6690bb827270f7de1cf7207ef14245416210ce88bbe80b
# (the difference: the two guards of line_findings run on each line before forward_log.append_entry)
def append(path: Path, bodies: list) -> list:
    """Append each body, chained on the current head, through forward_log.append_entry (it refuses a stale
    prev or a line whose sha is not its own content) — after the two guards (HALT FWD-NAN / FWD-LINE-BREAK)."""
    out = []
    for b in bodies:
        line = chained(b, FL.last_sha(path))
        bad = line_findings(line)
        if bad:
            raise SystemExit("HALT " + " | ".join(bad))
        out.append(FL.append_entry(line, path))
    return out


# PORT VERBATIM <- research_outputs/tierc12/x_rec/scripts/tc11x_forward.py:610-613 sha256 33f65b5eca8e50dfce6690bb827270f7de1cf7207ef14245416210ce88bbe80b
def book_open_body(book: str, spec_sha: str, opening_ms: int, n_min: int) -> dict:
    return {"kind": "book_open", "tier": TIER, "book": book, "role": ROLE[book],
            "spec_sha256": spec_sha, "opening_ms": int(opening_ms), "opening_iso": iso(int(opening_ms)),
            "n_min": int(n_min), "scored": False}


# PORT VERBATIM <- research_outputs/tierc12/x_rec/scripts/tc11x_forward.py:409-410 sha256 33f65b5eca8e50dfce6690bb827270f7de1cf7207ef14245416210ce88bbe80b
def render_json(doc: dict) -> bytes:
    return (json.dumps(doc, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


def parse_lines(raw: bytes) -> list:
    """The entries of ledger BYTES, in file order (forward_log.read_lines' own split)."""
    return [json.loads(x) for x in raw.decode("utf-8").splitlines() if x.strip()]


# PORT CHANGED <- research_outputs/tierc12/x_rec/scripts/tc11x_forward.py:616-648 sha256 33f65b5eca8e50dfce6690bb827270f7de1cf7207ef14245416210ce88bbe80b
# (the difference: THE STRUCTURE LAW S1-S7 of L-L.6 — the prefix law on bytes, exactly one more book_open
#  naming the fourth spec's own sha, the row field set, the refresh order, the gated-subset law — in place
#  of X's three-book law; a pure function of the file and three byte strings)
def chain_findings(path, spec_bytes: bytes, x_spec_bytes: bytes, x_ledger_bytes: bytes) -> list:
    """FWD-CHAIN S1..S7 [L-L.6]: every breach of the structure law on the ledger at `path`, judged against
    the BYTES of the fourth spec, of X's spec and of X's ledger.  [] is a lawful file."""
    try:
        v = FL.verify_chain(path)
    except ValueError as e:
        return [f"FWD-CHAIN S1: the ledger does not parse ({e})"]
    if not v["ok"]:
        return [f"FWD-CHAIN S1: forward_log.verify_chain breaks at line {v['first_bad_line']}: {v['reason']}"]
    out = []
    lines = FL.read_lines(path)
    raw = Path(path).read_bytes()
    spec, xspec = json.loads(spec_bytes.decode("utf-8")), json.loads(x_spec_bytes.decode("utf-8"))
    s_sha, x_sha = sha_bytes(spec_bytes), sha_bytes(x_spec_bytes)
    kinds, x_order = list(xspec["chain"]["kinds"]), list(xspec["book_order"])
    order, book4 = list(spec["book_order"]), spec["book"]
    n_x, n_open = len(parse_lines(x_ledger_bytes)), len(x_order)
    # S2
    bad = [f"{i + 1}:{x.get('kind')}" for i, x in enumerate(lines) if x.get("kind") not in kinds]
    if bad:
        out.append(f"FWD-CHAIN S2: line kind(s) outside X's chain.kinds {kinds}: {bad}")
    # S3
    if not raw.startswith(x_ledger_bytes):
        out.append(f"FWD-CHAIN S3 FWD-PREFIX: the first {len(x_ledger_bytes)} bytes of the file are not X's "
                   f"ledger — the prefix law is on bytes")
    head = [x.get("book") for x in lines[:n_open] if x.get("kind") == K_OPEN]
    if head != x_order:
        out.append(f"FWD-CHAIN S3: the first lines open {head}, not X's book_order {x_order}")
    other = [i + 1 for i, x in enumerate(lines[:n_x]) if x.get("spec_sha256") != x_sha]
    if other:
        out.append(f"FWD-CHAIN S3 FWD-X-SPEC: line(s) {other} name another spec sha than X's {x_sha}")
    if [x.get("kind") for x in lines[n_open:n_x]] != [K_REFRESH] * (n_x - n_open):
        out.append(f"FWD-CHAIN S3: lines {n_open + 1}..{n_x} are not X's refresh")
    # S4
    opens = [i + 1 for i, x in enumerate(lines) if x.get("kind") == K_OPEN and i >= n_x]
    if opens != [n_x + 1]:
        out.append(f"FWD-CHAIN S4: exactly one book_open follows X's {n_x} lines, at line {n_x + 1}; found at "
                   f"line(s) {opens}")
    else:
        line = lines[n_x]
        if line.get("book") != book4:
            out.append(f"FWD-CHAIN S4: line {n_x + 1} opens {line.get('book')!r}, not the fourth book {book4!r}")
        if line.get("spec_sha256") == x_sha:
            out.append(f"FWD-CHAIN S4 FWD-SPEC-REUSED: line {n_x + 1} names X's spec sha — the fourth book "
                       f"re-hashes into its own document [contract F-LEDGER]")
        elif line.get("spec_sha256") != s_sha:
            out.append(f"FWD-CHAIN S4 FWD-SPEC: line {n_x + 1} names {line.get('spec_sha256')}, not the sha of "
                       f"{SPEC_NAME} {s_sha}")
        for f in ("opening_ms", "n_min"):
            if {json.dumps(x.get(f)) for x in lines[:n_open]} != {json.dumps(line.get(f))}:
                out.append(f"FWD-CHAIN S4: line {n_x + 1} carries {f} {line.get(f)!r}, not the value of X's "
                           f"book_open lines")
    # S5
    fields = set(xspec["row_fields"]) | set(spec["row_fields_added"]) | set(CHAIN_FIELDS)
    seen, good = {}, []
    for i, x in enumerate(lines):
        if x.get("kind") != K_ROW:
            continue
        lawful = True
        if x.get("book") not in order:
            lawful = False
            out.append(f"FWD-CHAIN S5: line {i + 1} is a row of an unknown book {x.get('book')!r}")
        if set(x) != fields:
            lawful = False
            out.append(f"FWD-CHAIN S5 FWD-ROW-FIELDS: line {i + 1} differs from the row field set on "
                       f"{sorted(set(x) ^ fields)}")
        key = (x.get("book"), x.get("symbol"), x.get("entry_ms"))
        if key in seen:
            out.append(f"FWD-CHAIN S5 FWD-DUP-KEY: line {i + 1} holds {list(key)} again (first at line "
                       f"{seen[key]}) — a campaign is appended exactly once")
        seen.setdefault(key, i + 1)
        if lawful:
            good.append(i)
    # S6
    pins = [x.get("pin_ms") for x in lines if x.get("kind") == K_REFRESH]
    twice = [b for a, b in zip(pins, pins[1:]) if b <= a]
    if twice:
        out.append(f"FWD-CHAIN S6 FWD-REFRESH-TWICE: refresh pin(s) {twice} do not advance — a second refresh "
                   f"at one pin appends nothing")
    if lines and lines[len(lines) - 1].get("kind") == K_ROW:
        out.append("FWD-CHAIN S6 FWD-TORN-REFRESH: the file ends on a row line — a refresh block closes with "
                   "its refresh line")
    block = []
    for i, x in enumerate(lines + [{}]):
        if i in good:
            block.append(((order.index(x["book"]), x["entry_close_ms"], x["symbol"]), i + 1))
            continue
        if x.get("kind") != K_ROW:
            if [k for k, _ in block] != sorted(k for k, _ in block):
                out.append(f"FWD-CHAIN S6 FWD-ROW-ORDER: the rows at lines {block[0][1]}..{block[len(block) - 1][1]} "
                           f"do not stand in book order, then (entry_close_ms, symbol)")
            block = []
    # S7
    gated = {b: xspec["books"][b]["gate"]["base_book"] for b in x_order if xspec["books"][b].get("gate")}
    gated[book4] = spec["books"][book4]["gate"]["base_book"]
    skip = CHAIN_FIELDS + ("book",)
    earlier = {}
    for i in good:
        x = lines[i]
        key = (x["symbol"], x["entry_ms"])
        if x["book"] not in gated:
            earlier[(x["book"],) + key] = x
            continue
        base = earlier.get((gated[x["book"]],) + key)
        if base is None:
            out.append(f"FWD-CHAIN S7 FWD-SUBSET: line {i + 1}, a {x['book']} row {list(key)}, has no "
                       f"{gated[x['book']]} row of that key earlier in the file")
            continue
        moved = sorted(f for f in x if f not in skip and FL.canonical({"v": x[f]}) != FL.canonical({"v": base.get(f)}))
        if moved:
            out.append(f"FWD-CHAIN S7 FWD-SUBSET: line {i + 1}, a {x['book']} row {list(key)}, differs from "
                       f"its base row on {moved}")
    return out


# ═══════════════════════════════════════════════════════ THE ENV-FREE SHA-FIRST READER [L-L.3]
class Reader:
    """Every read is sha-first: an X file against its row of X_REC_MANIFEST.json (the manifest's own sha
    through `certified`); a TC11 file against the sha TC11's PROGRESS.json certifies, that file accepted at
    the sha TC12-R0's frozen_estate_shas_at_r0 holds or at the stamped value L-0.24 allows; TC11's two
    registry files by NO file sha (the head and the payload shas are held by `sources`); a TC12 file through
    `certified` from the moment a progress record names it."""

    def __init__(self, root=None):
        self.root = Path(ROOT if root is None else root)
        self.main = PINS.main_tree(self.root)          # x_rec/ is git-ignored: it stands in the main tree
        self.allowed = set(SPEC_READS_T)
        self._memo: dict = {}

    def path(self, rel: str) -> Path:
        if rel not in self.allowed:
            halt("SPEC-READS", f"{rel} is not a file this tool may open (SPEC_READS_T and the lineage files "
                               f"X's spec names) [L-L.3]")
        return (self.main if rel.startswith(XR + "/") else self.root) / rel

    def _read(self, rel: str) -> bytes:
        p = self.path(rel)
        if not p.is_file():
            halt("FWD-READ", f"{rel} is not on file")
        return p.read_bytes()

    def records(self) -> dict:
        if "records" not in self._memo:
            self._memo["records"] = PG.records(self.root)
        return self._memo["records"]

    def manifest(self) -> dict:
        if "manifest" not in self._memo:
            raw = self._read(X_MANIFEST_REL)
            cert = PG.certified(X_MANIFEST_REL, self.root)
            if (len(raw), sha_bytes(raw)) != (cert["bytes"], cert["sha256"]):
                halt("FWD-READ", f"{X_MANIFEST_REL} does not re-hash to the entry {cert['record']} certifies")
            self._memo["manifest"] = {r["copy"]: r for r in json.loads(raw.decode("utf-8"))["files"]}
        return self._memo["manifest"]

    def x_row(self, rel: str) -> dict:
        row = self.manifest().get(rel)
        if row is None:
            halt("FWD-READ", f"{rel} has no row in {X_MANIFEST_REL}")
        return row

    def x(self, rel: str) -> bytes:
        row, raw = self.x_row(rel), self._read(rel)
        if (len(raw), sha_bytes(raw)) != (row["bytes"], row["sha256"]):
            halt("FWD-READ", f"{rel} is not at its {X_MANIFEST_REL} row [O-4]")
        return raw

    def _stamped(self, rel: str, sha_now: str) -> bool:
        """L-0.24's one acceptance: the stamp map reads applied: true and names these bytes for the path."""
        if not self.path(STAMP_MAP_REL).is_file():
            return False
        doc = json.loads(self._read(STAMP_MAP_REL).decode("utf-8"))
        return doc.get("applied") is True and any(
            r.get("path") == rel and r.get("sha256_after") == sha_now for r in doc.get("moved", []))

    def tc11_progress(self) -> dict:
        if "tc11_progress" not in self._memo:
            raw = self._read(T11_PROGRESS_REL)
            r0 = self.records()[R0_ID][R0_FROZEN_KEY][T11_PROGRESS_REL]
            if sha_bytes(raw) != r0["sha256"] and not self._stamped(T11_PROGRESS_REL, sha_bytes(raw)):
                halt("FWD-READ", f"{T11_PROGRESS_REL} is neither at the sha {R0_ID} holds for it nor at a "
                                 f"stamped value [L-0.24]")
            self._memo["tc11_progress"] = json.loads(raw.decode("utf-8"))
        return self._memo["tc11_progress"]

    def tc11_entry(self, rel: str) -> dict:
        hits = [s["artifact_shas"][rel] for s in self.tc11_progress()["stages"]
                if rel in s.get("artifact_shas", {})]
        if not hits:
            halt("FWD-READ", f"{T11_PROGRESS_REL} certifies no sha for {rel}")
        return hits[len(hits) - 1]

    def tc11(self, rel: str) -> bytes:
        e, raw = self.tc11_entry(rel), self._read(rel)
        if (len(raw), sha_bytes(raw)) != (e["bytes"], e["sha256"]):
            halt("FWD-READ", f"{rel} is not at the sha {T11_PROGRESS_REL} certifies")
        return raw

    def tc11_plain(self, rel: str) -> bytes:
        return self._read(rel)

    def tc12(self, rel: str) -> bytes:
        raw = self._read(rel)
        if any(rel in rec.get("artifact_shas", {}) for rec in self.records().values()):
            cert = PG.certified(rel, self.root)
            if (len(raw), sha_bytes(raw)) != (cert["bytes"], cert["sha256"]):
                halt("FWD-READ", f"{rel} does not re-hash to the entry {cert['record']} certifies [L-0.4]")
        return raw

    def lineage(self, rel: str) -> bytes:
        return self._read(rel)


# ═══════════════════════════════════════════════════════ THE REGISTRIES' HASH LAW (TC11's, carried by TC12)
def payload_sha(body: dict) -> str:
    b = {k: v for k, v in body.items() if k not in SHA_KEYS}
    return sha_bytes(json.dumps(b, sort_keys=True, ensure_ascii=False).encode("utf-8"))


def registry_head(bodies: list) -> str:
    """The chain head recomputed from the payloads: line_sha256 over {seq, registration, sha256, prev}."""
    prev = GENESIS
    for r in bodies:
        line = {"seq": r.get("seq"), "registration": r.get("registration"), "sha256": payload_sha(r),
                "prev": prev}
        prev = sha_bytes(json.dumps(line, sort_keys=True).encode())
    return prev


def registration(doc: dict, rid: str, tag: str) -> dict:
    hit = [r for r in doc.get("registrations", []) if r.get("registration") == rid]
    if len(hit) != 1:
        halt(tag, f"{len(hit)} registrations {rid} in the registry, not one")
    if payload_sha(hit[0]) != hit[0].get("sha256"):
        halt(tag, f"{rid}: the payload does not hash to its filed payload sha")
    return hit[0]


# ═══════════════════════════════════════════════════════ TC11's CHAIN LAW, RE-IMPLEMENTED [L-L.4]
def tc11_canonical(obj: dict) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def tc11_chain(raw: bytes) -> tuple:
    """(lines, findings) of TC11's ledger bytes under TC11's OWN law: each line's bytes are its canonical
    compact JSON; each line_sha256 recomputes over the line without it; each `prev` is the previous
    line_sha256, the first the zeros.  No TC11 module is imported."""
    out, lines, prev = [], [], GENESIS
    for i, text in enumerate(raw.decode("utf-8").split("\n")[:raw.count(b"\n")]):
        try:
            line = json.loads(text)
        except ValueError as e:
            return lines, out + [f"line {i + 1} does not parse ({e})"]
        if tc11_canonical(line) != text:
            out.append(f"line {i + 1} is not its canonical compact JSON")
        body = {k: v for k, v in line.items() if k != T11_SHA_FIELD}
        if sha_bytes(tc11_canonical(body).encode("utf-8")) != line.get(T11_SHA_FIELD):
            out.append(f"line {i + 1}: {T11_SHA_FIELD} does not recompute")
        if line.get(T11_PREV_FIELD) != prev:
            out.append(f"line {i + 1}: `{T11_PREV_FIELD}` is not the previous {T11_SHA_FIELD}")
        prev = line.get(T11_SHA_FIELD)
        lines.append(line)
    if not raw.endswith(b"\n") or not lines:
        out.append("the file is empty or does not end on a newline")
    return lines, out


# ═══════════════════════════════════════════════════════ THE SOURCES — every read, verified [L-L.3]
def sources(reader=None) -> dict:
    """Every input of the fourth spec and of the five-line ledger, read sha-first.  HALTs on the first read
    that does not verify.  The result is plain data: `spec_doc` is a pure function of it and of the pin door."""
    rd = Reader() if reader is None else reader
    S: dict = {}
    pre = PINS.prefix()
    S["contract"] = {"path": pre["path"], "prefix_bytes": pre["prefix_bytes"], "prefix_sha256": pre["prefix_sha256"]}
    step_q = PG.records(rd.root)[STEP_Q_ID]
    when = STEP_Q_RX.findall(step_q.get("one_line", ""))
    if len(when) != 1 or not step_q.get("commit"):
        halt("FWD-STEP-Q", f"progress/STEP_Q.json names {len(when)} commit instants in `one_line`, not one")
    S["step_q"] = {"commit": step_q["commit"], "instant_ms": iso_ms(when[0]), "instant_iso": when[0]}

    # TC12's filed registry: its own pin, its chain, and `certified` once a record names it
    reg_raw, pin_raw = rd.tc12(REG_REL), rd.tc12(REG_PIN_REL)
    reg, pin = json.loads(reg_raw.decode("utf-8")), json.loads(pin_raw.decode("utf-8"))
    filed = pin.get("registrations_file", {})
    if (filed.get("path"), filed.get("bytes"), filed.get("sha256")) != (REG_REL, len(reg_raw), sha_bytes(reg_raw)):
        halt("FWD-REGISTRY", f"{REG_REL} is not the file {REG_PIN_REL} pins")
    if not registry_head(reg.get("registrations", [])) == reg.get("head") == pin.get("head"):
        halt("FWD-REGISTRY", f"the head recomputed from the payloads of {REG_REL} is not the head it and "
                             f"{REG_PIN_REL} carry")
    S["registry"], S["registry_pin"] = reg, pin

    # TC11's registry: by its chain head VALUE and each payload sha — never by a whole-file sha [L-0.24]
    t11 = json.loads(rd.tc11_plain(T11_REG_REL).decode("utf-8"))
    t11_pin = json.loads(rd.tc11_plain(T11_PIN_REL).decode("utf-8"))
    if not registry_head(t11.get("registrations", [])) == t11.get("head") == t11_pin.get("head"):
        halt("FWD-T11-REGISTRY", f"the head recomputed from the payloads of {T11_REG_REL} is not the head it "
                                 f"and {T11_PIN_REL} carry")
    S["t11_registry"] = t11

    # X's records and source texts
    S["x_spec_bytes"] = rd.x(X_SPEC_REL)
    S["x_spec"] = json.loads(S["x_spec_bytes"].decode("utf-8"))
    S["x_spec_row"] = dict(rd.x_row(X_SPEC_REL))
    S["x_ledger"] = rd.x(X_LEDGER_REL)
    S["x_ledger_row"] = dict(rd.x_row(X_LEDGER_REL))
    v = FL.verify_chain(rd.path(X_LEDGER_REL))
    if not v["ok"] or v["head"] != FL.last_sha(rd.path(X_LEDGER_REL)):
        halt("FWD-ANCESTOR", f"X's ledger does not verify under forward_log's law: {v.get('reason')}")
    S["x_head"] = v["head"]
    xf, xb = rd.x(XF_REL).decode("utf-8"), rd.x(XB_REL).decode("utf-8")
    S["x_row_nullable"] = list(ast.literal_eval(PINS.literal_node(xf, "ROW_NULLABLE")))
    S["x_chain_fields"] = list(ast.literal_eval(PINS.literal_node(xf, "CHAIN_FIELDS")))
    S["x_kinds"] = list(ast.literal_eval(PINS.literal_node(xf, "KINDS")))
    S["x_band_codes"] = list(ast.literal_eval(PINS.literal_node(xb, "BAND_CODES")))

    # TC11's records
    S["t11_ledger"] = rd.tc11(T11_LEDGER_REL)
    S["t11_ledger_entry"] = dict(rd.tc11_entry(T11_LEDGER_REL))
    r0 = PG.records(rd.root)[R0_ID][R0_FROZEN_KEY].get(T11_LEDGER_REL)
    if r0 != S["t11_ledger_entry"]:
        halt("FWD-ANCESTOR", f"{T11_LEDGER_REL}: the sha {R0_ID} holds for it is not the sha TC11's "
                             f"PROGRESS.json certifies")
    S["t11_leans"] = rd.tc11(T11_LEANS_REL).decode("utf-8")
    S["t11_asof"] = json.loads(rd.tc11(T11_ASOF_REL).decode("utf-8"))

    # the lineage files X's spec names, hashed now (X's own three modules are not carried)
    paths = sorted(p for p in S["x_spec"]["path_modules"] if not p.startswith(X_OWN_PREFIX))
    if hasattr(rd, "allowed"):
        rd.allowed |= set(paths)
    S["lineage"] = {p: sha_bytes(rd.lineage(p)) for p in paths}
    S["fl_text"] = rd.lineage(FL_REL).decode("utf-8")
    S["own_text"] = Path(__file__).read_text(encoding="utf-8")      # this module's own ports, for FWD-FL-PORT
    return S


# ═══════════════════════════════════════════════════════ THE TEXTS OF RECORD, BY OBJECT [L-L.2]
def gate_text(registry: dict) -> tuple:
    """(the ONE `scored` element of registrations[P-ADM-1].operative_spec.arms, P-ADM-1's payload sha).
    HALT FWD-GATE-TEXT unless exactly one element matches ^`scored`\\s."""
    body = registration(registry, REG_ADM, "FWD-GATE-TEXT")
    arms = body.get("operative_spec", {}).get("arms")
    hits = [x for x in arms if isinstance(x, str) and SCORED_RX.match(x)] if isinstance(arms, list) else []
    if len(hits) != 1:
        halt("FWD-GATE-TEXT", f"{len(hits)} element(s) of registrations[{REG_ADM}].operative_spec.arms match "
                              f"^`scored`\\s — exactly one is the fourth book's gate text [L-L.2]")
    return hits[0], body["sha256"]


def old_text(t11_registry: dict, code: str) -> tuple:
    """(TC11's P-AGE-1 scored_arm, its payload sha).  HALT FWD-OLD-TEXT unless the text names the OLD band
    and the trailing edges — X's own two assertions."""
    body = registration(t11_registry, REG_AGE, "FWD-OLD-TEXT")
    arm = str(body.get("operative_spec", {}).get("scored_arm") or "")
    if OLD_NEEDLE.format(code=code) not in arm or EDGES_NEEDLE not in arm:
        halt("FWD-OLD-TEXT", f"{REG_AGE}'s scored_arm does not name `{OLD_NEEDLE.format(code=code)}` on "
                             f"`{EDGES_NEEDLE}`: {arm!r}")
    return arm, body["sha256"]


def cut_text(t11_registry: dict) -> tuple:
    """(TC11's P-WIN-1 scored_arm, its payload sha, the captured cut).  HALT FWD-CUT-TEXT unless the cut
    regex matches exactly once and the integer equals the contract pin adm.lag_cut."""
    body = registration(t11_registry, REG_WIN, "FWD-CUT-TEXT")
    arm = str(body.get("operative_spec", {}).get("scored_arm") or "")
    caps = CUT_RX.findall(arm)
    if len(caps) != 1 or int(caps[0]) != lag_cut():
        halt("FWD-CUT-TEXT", f"{REG_WIN}'s scored_arm captures {caps} for `{CUT_RX.pattern}` — exactly one "
                             f"capture equal to the contract pin {PIN_CUT} ({lag_cut()}) is the law")
    return arm, body["sha256"], int(caps[0])


def contract_opening_ms() -> int:
    """The contract's own literal (the pin ledger.opening, minutes precision) as epoch ms — compared with
    the file value, never used in its place [L-L.8]."""
    return PINS.iso_ms(PINS.pin("ledger.opening"))


def contract_n_min() -> int:
    """The contract pin ledger.n_min — what the fourth book's book_open line files [L-L.14]."""
    return PINS.pin("ledger.n_min")


def _one(values: dict, tag: str, what: str):
    """HALT `tag` unless every named value is one object; returns it."""
    distinct = sorted({json.dumps(v, sort_keys=True) for v in values.values()})
    if len(distinct) != 1:
        halt(tag, f"{what} is not one value: " + "; ".join(f"{k} = {v!r}" for k, v in values.items()))
    return next(iter(values.values()))


def ancestor_facts(S: dict) -> dict:
    """TC11's ledger verified by its own law, and every fact both ancestors state held EQUAL [L-L.4].
    HALT FWD-ANCESTOR otherwise.  Returns what the spec cites."""
    lines, bad = tc11_chain(S["t11_ledger"])
    if bad:
        halt("FWD-ANCESTOR", f"TC11's ledger does not verify under TC11's own law: {bad[0]}")
    if [x.get("kind") for x in lines][:1] != [T11_GENESIS_KIND] or lines[len(lines) - 1].get("kind") != T11_REFRESH_KIND:
        halt("FWD-ANCESTOR", f"TC11's ledger is not a {T11_GENESIS_KIND} line … a {T11_REFRESH_KIND} line")
    genesis, refresh = lines[0], lines[len(lines) - 1]
    xs, x_lines = S["x_spec"], parse_lines(S["x_ledger"])
    x_refresh = x_lines[len(x_lines) - 1]
    diffs = []
    if genesis.get("panel") != xs["books"][BASE_BOOK]["panel"]:
        diffs.append("the panel")
    for b in sorted(genesis.get("books", {})):
        roles, xb = genesis["books"][b].get("roles", {}), xs["books"].get(b, {})
        if roles.get("name") != xb.get("roles_name"):
            diffs.append(f"{b}: the roles name")
        if {k: repr(roles.get(k)) for k in ROLE_PERIODS} != {
                k: xb.get("ride_spec", {}).get("roles_fields", {}).get(k) for k in ROLE_PERIODS}:
            diffs.append(f"{b}: the six periods")
        if refresh.get("books", {}).get(b, {}).get("book_sha") != xs["x_found_books"]["book_sha"].get(b):
            diffs.append(f"{b}: the book sha at the score edge")
        if [x.get("key") for x in refresh.get("books", {}).get(b, {}).get("open", [])] != \
                x_refresh["books"][b]["open_keys"]:
            diffs.append(f"{b}: the open keys at the score edge")
    if sorted(genesis.get("books", {})) != sorted(b for b in xs["book_order"] if not xs["books"][b].get("gate")):
        diffs.append("the ridden books")
    if refresh.get("pin_ms") != x_refresh.get("pin_ms") or refresh.get("corridor_lo_ms") != xs["pool_lo_ms"]:
        diffs.append("the refresh pin or the corridor's lower bound")
    if diffs:
        halt("FWD-ANCESTOR", f"a fact both ancestors state differs: {diffs}")
    return {"lines": lines, "genesis": genesis, "refresh": refresh}


# ═══════════════════════════════════════════════════════ THE SPEC [L-L.3]
def spec_doc(S: dict) -> dict:
    """BOOK_SPEC_COMBINED.json's content.  Pure description: nothing is ridden, no bar is read.  Every value
    is read from `S` or through the pin door; every cross-assertion HALTs under its own detector."""
    xs = S["x_spec"]
    x_lines = parse_lines(S["x_ledger"])
    x_order = list(xs["book_order"])
    x_opens = [x for x in x_lines if x.get("kind") == K_OPEN]
    x_gate = xs["books"][OLD_GATED]["gate"]
    anc = ancestor_facts(S)
    if sorted(S["x_kinds"]) != sorted([K_OPEN, K_REFRESH, K_ROW]) or S["x_kinds"] != list(xs["chain"]["kinds"]) \
            or S["x_chain_fields"] != list(CHAIN_FIELDS) or xs["chain"]["genesis"] != GENESIS:
        halt("FWD-KINDS", "X's line kinds, chain fields or genesis are not the ones this module names")
    if [x.get("book") for x in x_opens] != x_order or len(x_lines) != len(x_order) + 1 \
            or x_lines[len(x_lines) - 1].get("kind") != K_REFRESH \
            or {x.get("spec_sha256") for x in x_lines} != {S["x_spec_row"]["sha256"]}:
        halt("FWD-ANCESTOR", "X's ledger is not one book_open per book of X's book_order and one refresh "
                             "line, each naming X's spec sha")
    lt6 = LT6_BLOCK_RX.findall(S["t11_leans"])
    lt6_open = LT6_OPENING_RX.findall(lt6[0]) if len(lt6) == 1 else []
    lt6_n = LT6_N_RX.findall(lt6[0]) if len(lt6) == 1 else []
    if len(lt6_open) != 1 or len(lt6_n) != 1:
        halt("FWD-OPENING", f"TC11's L-T.6 names {len(lt6_open)} openings and {len(lt6_n)} unscored-until "
                            f"counts in {len(lt6)} block(s) — one of each is the law")

    # the opening, by object [L-L.8] — the file value is what code uses; the contract's is compared
    opening = _one({"X's spec opening.ms": xs["opening"]["ms"],
                    "opening_ms of X's book_open lines": _one(
                        {x["book"]: x.get("opening_ms") for x in x_opens}, "FWD-OPENING", "opening_ms on X's lines"),
                    "TC11's AS_OF_PIN tc10_pin_close_ms": S["t11_asof"].get("tc10_pin_close_ms"),
                    "TC11's GENESIS opening_ms": anc["genesis"].get("opening_ms"),
                    "TC11's L-T.6 text": iso_ms(lt6_open[0]),
                    f"the contract pin {PIN_OPENING}": contract_opening_ms()},
                   "FWD-OPENING", "the forward origin")
    if not iso(opening) == xs["opening"]["iso"] == x_opens[0].get("opening_iso"):
        halt("FWD-OPENING", "the opening's ISO form is not the one X's spec and X's first line carry")
    # n_min [L-L.14]
    n_min = _one({"X's spec n_min": xs["n_min"],
                  "n_min of X's book_open lines": _one(
                      {x["book"]: x.get("n_min") for x in x_opens}, "FWD-NMIN", "n_min on X's lines"),
                  "TC11's GENESIS n_score": anc["genesis"].get("n_score"),
                  "TC11's L-T.6 text": int(lt6_n[0]),
                  f"the contract pin {PIN_N_MIN}": contract_n_min()},
                 "FWD-NMIN", "the unscored-until count")
    # the score edge
    edge = _one({"TC11's AS_OF_PIN as_of_last_closed_4h_close_ms": S["t11_asof"].get("as_of_last_closed_4h_close_ms"),
                 "X's spec opening_rival.ms": xs["opening_rival"]["ms"],
                 "X's spec x_found_books.as_of_close_ms": xs["x_found_books"]["as_of_close_ms"],
                 "the filed registry's scored_window.end_ms": S["registry"].get("scored_window", {}).get("end_ms")},
                "FWD-SCORE-EDGE", "the score edge")
    pool_lo = _one({"X's spec pool_lo_ms": xs["pool_lo_ms"], "X's third-book gate pool_lo_ms": x_gate["pool_lo_ms"]},
                   "FWD-ANCESTOR", "pool_lo_ms")
    # the OLD band code
    codes = S["x_band_codes"]
    caps = OLD_REFUSE_RX.findall(x_gate["refuse"])
    if len(caps) != 1 or not codes or caps[0] != codes[len(codes) - 1]:
        halt("FWD-OLD-CODE", f"the last element of X's BAND_CODES {codes} is not the one capture {caps} of "
                             f"`{OLD_REFUSE_RX.pattern}` in X's third-book gate")
    old = caps[0]
    # the texts of record
    text, adm_sha = gate_text(S["registry"])
    age_text, age_sha = old_text(S["t11_registry"], old)
    win_text, win_sha, win_cut = cut_text(S["t11_registry"])
    if age_text != x_gate["text_of_record"] or age_sha != x_gate["p_age_1_payload_sha256"]:
        halt("FWD-OLD-TEXT", f"TC11's {REG_AGE} scored_arm or payload sha is not the one X's third book froze")
    if S["registry_pin"].get("leans", {}).get("sha256") != S["registry"].get("leans", {}).get("sha256"):
        halt("FWD-REGISTRY", "the registry's two pins of the readings' sha differ")
    # the lineage files and the chain law's own file
    moved = sorted(p for p, s in S["lineage"].items() if s != xs["path_modules"][p])
    if moved:
        halt("FWD-SPEC-PATH", f"lineage file(s) {moved} do not hash to the value X's spec names")
    bad = fl_port_findings(S["fl_text"], S["own_text"])
    if bad:
        halt("FWD-FL-PORT", " | ".join(x.split(" ", 1)[1] for x in bad))
    base = xs["books"][BASE_BOOK]
    cut_row = PINS.row(PIN_CUT)

    return {
        "tier": TIER, "stage": STAGE,
        "contract": dict(S["contract"]),
        "leans_sha256": S["registry"]["leans"]["sha256"],
        "registry": {"path": REG_REL, "head": S["registry_pin"]["head"]},
        "book": BOOK4,
        "book_order": x_order + [BOOK4],
        "books": {BOOK4: {
            "role": ROLE[BOOK4], "title": TITLE[BOOK4],
            "card_name": base["card_name"], "roles_name": base["roles_name"],
            "ride_spec": base["ride_spec"], "panel": base["panel"],
            "runner": RUNNER,
            "gate": {
                "kind": x_gate["kind"],
                "base_book": BASE_BOOK,
                "text_of_record": text,
                "text_sha256": sha_bytes(text.encode("utf-8")),
                "text_source": f"{REG_REL} registrations[{REG_ADM}].operative_spec.arms — the ONE element "
                               f"matching ^`scored`\\s",
                "p_adm_1_payload_sha256": adm_sha,
                "combine": "OR",
                "components": {
                    "old": {"registration": REG_AGE, "text_of_record": age_text, "payload_sha256": age_sha,
                            "refuse": x_gate["refuse"], "code": old,
                            "lineage_functions": x_gate["lineage_functions"],
                            "band_quantiles": x_gate["band_quantiles"],
                            "min_pool_bars": x_gate["min_pool_bars"], "pool_lo_ms": x_gate["pool_lo_ms"]},
                    "stale": {"registration": REG_WIN, "text_of_record": win_text, "payload_sha256": win_sha,
                              "refuse": "lag >= cut, lag = entry_i - arm_i in 4h bars (a row field)",
                              "cut": {"value": lag_cut(), "pin": PIN_CUT,
                                      "contract_lines": list(cut_row["source"]["lines"]),
                                      "tc11_capture": {"regex": CUT_RX.pattern, "value": win_cut}}},
                },
                "none_band": x_gate["none_band"],
                "stamps_only": x_gate["stamps_only"],
                "rivals": x_gate["rivals"],
            }}},
        "tc11_registry": {"path": T11_REG_REL, "head": S["t11_registry"]["head"],
                          "p_age_1_payload_sha256": age_sha, "p_win_1_payload_sha256": win_sha,
                          "pinned_by": "the chain head VALUE (recomputed from the payloads) and each payload "
                                       "sha read — never the file's own sha [L-0.24]"},
        "existing_books": {"spec": S["x_spec_row"]["x_path"], "copy": X_SPEC_REL,
                           "sha256": S["x_spec_row"]["sha256"],
                           "book_open_entry_sha256": {x["book"]: x["entry_sha256"] for x in x_opens}},
        "ancestors": {
            "x_ledger": {"path": S["x_ledger_row"]["x_path"], "copy": X_LEDGER_REL,
                         "bytes": S["x_ledger_row"]["bytes"], "sha256": S["x_ledger_row"]["sha256"],
                         "n_lines": len(x_lines), "head": S["x_head"],
                         "chain_law": xs["chain"]["law"], "continued": True},
            "tc11_ledger": {"path": T11_LEDGER_REL, "bytes": S["t11_ledger_entry"]["bytes"],
                            "sha256": S["t11_ledger_entry"]["sha256"], "n_lines": len(anc["lines"]),
                            "genesis_line_sha256": anc["genesis"][T11_SHA_FIELD],
                            "head_line_sha256": anc["refresh"][T11_SHA_FIELD],
                            "chain_law": T11_CHAIN_LAW, "verified": True, "continued": False},
        },
        "opening": xs["opening"],
        "opening_held_equal": [
            "opening_ms of X's three book_open lines and of the fourth book's",
            f"{T11_ASOF_REL} tc10_pin_close_ms",
            "TC11's GENESIS opening_ms",
            f"the one capture of L-T.6's `It opens at` in {T11_LEANS_REL}",
            f"the contract pin {PIN_OPENING}, parsed to ms",
            "at the refresh (TC12-L, an armed process): the shim's TC10 pin and TC10's STEP0 record — this "
            "env-free tool opens no TC10 record"],
        "opening_rival": xs["opening_rival"],
        "scored_window_end_ms": edge,
        "admission": xs["admission"],
        "append_law": xs["append_law"],
        "n_min": n_min,
        "pool_lo_ms": pool_lo,
        "refresh_law": xs["refresh_law"],
        "row_fields": xs["row_fields"],
        "row_fields_added": list(ROW_FIELDS_ADDED),
        "row_nullable": S["x_row_nullable"],
        "ctrl_cols": xs["ctrl_cols"],
        "flags": {
            "in_o9_scored_window": "opening.ms < entry_close_ms <= scored_window_end_ms",
            "entered_before_gate_text_filed": "entry_close_ms <= flags.step_q.instant_ms",
            "entered_before_book_frozen": "entry_close_ms <= the committer_time_ms of flags.book_frozen.record",
            "step_q": dict(S["step_q"]),
            "book_frozen": {"rule": f"the committer time (ms) of the commit that first adds line "
                                    f"{len(x_lines) + 1} of forward/{LEDGER_NAME}",
                            "record": FREEZE_REL},
        },
        "n_law": {
            "x_n_law": xs["n_law"],
            "row_set_of_record": {
                "every_book": "in_o9_scored_window == false",
                BOOK4: "in_o9_scored_window == false and entered_before_book_frozen == false"},
            "beside": "the all-rows figure, printed beside under the collar",
            "chooser": "none — the row set of record for any later score is fixed here; no later "
                       "registration chooses",
        },
        "chain": dict(xs["chain"], structure_law=list(STRUCTURE_LAW)),
        "continuation": {"x_prefix_bytes": len(S["x_ledger"]), "x_prefix_sha256": sha_bytes(S["x_ledger"]),
                         "first_tc12_line": len(x_lines) + 1,
                         "declared_difference_from_x_verifier": DECLARED_DIFFERENCE},
        "path_modules": dict(sorted(S["lineage"].items())),
    }


def guard_out(out) -> Path:
    """The directory of record, a directory under a `_det_*` name, or one outside the tree (a scratch build)."""
    o = Path(out).resolve()
    root = ROOT.resolve()
    inside = o == root or root in o.parents
    if inside and o != out_dir().resolve() and not any(p.startswith(DET_PREFIX) for p in o.relative_to(root).parts):
        halt("FWD-OUT", f"{o.relative_to(root).as_posix()} is neither {OUT_REL}, a `{DET_PREFIX}*` directory "
                        f"nor a directory outside the tree")
    return o


def freeze_spec(out, body: bytes) -> str:
    """Write BOOK_SPEC_COMBINED.json ONCE; an existing file must equal `body` byte for byte."""
    p = Path(out) / SPEC_NAME
    if p.exists():
        if p.read_bytes() != body:
            halt("FWD-SPEC-FROZEN", f"{SPEC_NAME} exists and the spec rebuilt now from its sources differs — "
                                    f"the fourth book's spec is frozen; a changed module or text needs an "
                                    f"AMENDMENT and a re-opened ledger [L-L.3]")
    else:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(body)
    return sha_bytes(body)


def read_spec(out) -> tuple:
    p = Path(out) / SPEC_NAME
    if not p.is_file():
        halt("FWD-OPEN", f"{SPEC_NAME} is absent — freeze the spec first")
    b = p.read_bytes()
    return json.loads(b.decode("utf-8")), sha_bytes(b), b


# ═══════════════════════════════════════════════════════ THE LEDGER [L-L.4, L-L.5]
def atomic_append(record: Path, bodies: list, base_bytes: bytes, check) -> bytes:
    """THE ATOMIC WRITE (TC11's writer law): the record's bytes — `base_bytes` when it is absent — are copied
    to the scratch `_det_build/`, the bodies are appended there through the guards, the scratch is checked
    (`check(path) -> findings`) and must still start with the bytes it began from, then os.replace.  The
    record is never appended in place, so a crash cannot leave a torn tracked line."""
    record = Path(record)
    start = record.read_bytes() if record.exists() else base_bytes
    scratch = record.parent / BUILD_DIR / record.name
    scratch.parent.mkdir(parents=True, exist_ok=True)
    scratch.write_bytes(start)
    try:
        append(scratch, bodies)
        bad = check(scratch)
        new = scratch.read_bytes()
        if bad or not new.startswith(start):
            halt("FWD-CHAIN", " | ".join(bad) if bad else "the scratch ledger no longer starts with the record's bytes")
        os.replace(scratch, record)
    finally:
        if scratch.exists():
            scratch.unlink()
        if not any(scratch.parent.iterdir()):
            scratch.parent.rmdir()
    return new


def open_ledger(out, S: dict, spec_bytes: bytes) -> list:
    """The five-line ledger: X's bytes, then ONE line — the fourth book's book_open, chained on X's head.
    An absent record is written (atomically); a record on file must START with exactly those bytes and
    verify (anything else HALTs FWD-OPEN) and is left untouched."""
    out = Path(out)
    x_lines = parse_lines(S["x_ledger"])
    spec = json.loads(spec_bytes.decode("utf-8"))
    body = book_open_body(BOOK4, sha_bytes(spec_bytes), spec["opening"]["ms"], contract_n_min())
    if set(body) != set(body_of(x_lines[0])) or body["opening_iso"] != x_lines[0]["opening_iso"] \
            or body["n_min"] != spec["n_min"]:
        halt("FWD-OPEN", "the fourth book's book_open body is not X's key set with X's opening and the "
                         "spec's n_min")

    def check(path):
        return chain_findings(path, spec_bytes, S["x_spec_bytes"], S["x_ledger"])

    record = out / LEDGER_NAME
    if not record.exists():
        atomic_append(record, [body], S["x_ledger"], check)
    raw = record.read_bytes()
    want = S["x_ledger"] + (json.dumps(chained(body, S["x_head"]), sort_keys=True, ensure_ascii=False)
                            + "\n").encode("utf-8")
    if not raw.startswith(want):
        halt("FWD-OPEN", f"{LEDGER_NAME} does not start with X's ledger and the fourth book's book_open line "
                         f"as this spec opens it — the ledger is append-only [L-L.5]")
    bad = check(record)
    if bad:
        halt("FWD-CHAIN", " | ".join(bad))
    return parse_lines(want)


def build(out=None, reader=None) -> dict:
    """sources -> the spec (write-once) -> the five-line ledger.  Idempotent: a second run writes nothing."""
    out = guard_out(out_dir() if out is None else out)
    S = sources(reader)
    body = render_json(spec_doc(S))
    spec_sha = freeze_spec(out, body)
    lines = open_ledger(out, S, body)
    return {"out": out, "spec_sha256": spec_sha, "spec_bytes": len(body), "lines": lines,
            "gate_text": json.loads(body.decode("utf-8"))["books"][BOOK4]["gate"]["text_of_record"]}


# ═══════════════════════════════════════════════════════ THE GATE PREDICATES — the ONE implementation [L-L.2]
_OLD: dict = {}


def old_code(reader=None) -> str:
    """OLD: the last element of X's BAND_CODES, read from X's source TEXT (sha asserted) by ast.literal_eval
    and held equal to the code X's third-book gate refuses.  Bound once per process."""
    if "code" not in _OLD:
        rd = Reader() if reader is None else reader
        codes = list(ast.literal_eval(PINS.literal_node(rd.x(XB_REL).decode("utf-8"), "BAND_CODES")))
        gate = json.loads(rd.x(X_SPEC_REL).decode("utf-8"))["books"][OLD_GATED]["gate"]
        caps = OLD_REFUSE_RX.findall(gate["refuse"])
        if len(caps) != 1 or not codes or caps[0] != codes[len(codes) - 1]:
            halt("FWD-OLD-CODE", f"the last element of X's BAND_CODES {codes} is not the one capture {caps} "
                                 f"of `{OLD_REFUSE_RX.pattern}` in X's third-book gate")
        _OLD["code"] = caps[0]
    return _OLD["code"]


def lag_cut() -> int:
    """CUT: the contract pin adm.lag_cut, read through the pin door AT EACH CALL — never a module constant."""
    return PINS.pin("adm.lag_cut")


def p_age_1_refuses(row: dict) -> bool:
    """P-AGE-1 on a ledger row: refuse the OLD band at the ENTRY bar.  A None band HALTs — the gate cannot
    decide, and the third book's frozen spec says none_band: HALT."""
    band = row.get("tide_band")
    if band is None:
        halt("FWD-BAND-NONE", f"{row.get('symbol')} {row.get('entry_ms')} carries no tide band — the gate "
                              f"cannot decide [L-L.2]")
    return band == old_code()


def p_win_1_refuses(row: dict) -> bool:
    """P-WIN-1 on a ledger row: refuse a window age (lag = entry_i - arm_i, 4h bars) at or above the cut."""
    return int(row["lag"]) >= lag_cut()


def p_adm_1_refuses(row: dict) -> bool:
    """P-ADM-1, the combined refusal: OLD or stale (inclusive)."""
    return p_age_1_refuses(row) or p_win_1_refuses(row)


# ═══════════════════════════════════════════════════════ THE COMMAND LINE
def main(argv) -> int:
    out = next((a.split("=", 1)[1] for a in argv if a.startswith("--out-dir=")), None)
    r = build(out)
    try:
        shown = r["out"].relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        shown = str(r["out"])
    print(f"{TIER} · {STAGE} — the fourth book's spec and the five-line ledger [L-L.3, L-L.5]")
    print(f"out {shown}")
    print(f"{SPEC_NAME} sha256 {r['spec_sha256']} ({r['spec_bytes']} B) — write-once")
    for i, x in enumerate(r["lines"]):
        print(f"line {i + 1} {x['kind']:<9} {str(x.get('book') or '-'):<18} entry_sha256 {x['entry_sha256']}")
    print(f"gate text of record ({BOOK4}): {r['gate_text']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
