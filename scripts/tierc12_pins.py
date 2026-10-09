#!/usr/bin/env python
"""TIER-C12 · THE CONTRACT PIN DOOR [LEANS L-0.17, L-0.18, L-0.23; CANON-25; L-0.1 / L-X.16].

"No number typed that a file can supply" (contract :8).  Every number the contract states reaches
TC12 code through THIS door and no other: a regex capture over the pinned PREFIX of the contract
of record, driven by the filed map.  STDLIB ONLY — it runs at TC12-REG, before any substrate, and
imports neither the env shim nor the lineage.  It reads no bar and no book.

THE FILES (research_outputs/tierc12/pins/):
  CONTRACT_PIN_MAP.json          DATA.  One row per contract pin: {pin, lines [a, b], regex (one or
                                 more capture groups), type (a tuple of the regex's arity; members
                                 int | fraction | word | iso | str), word_map, also [{lines, regex,
                                 group}]}.  No `veto` field.  A multi-group row's value is a tuple.
                                 `slices` and `grammar` hold the three texts that are not pins: the
                                 VETOES line, the FIXTURES line, the registration and stage lines.
  CONTRACT_PINS.json             DERIVED by `--file`: every pin's lines, slice sha, captured text
                                 and exact value; the families; the veto tokens; the fixture names.
                                 At EVERY run the door re-derives all of it from the prefix and
                                 HALTs unless equal to this file.
  PIN_REGISTER.json              DATA.  One row per pin of EVERY door: {pin, kind (contract |
                                 x_record | stage_d | fitted | lineage | ruling), source {path, key
                                 or lines}, door, consumers [record ids], witness, veto (a token of
                                 the VETOES line or null)}.  A ruling row has no value.  A lineage
                                 row of a frozen source's literal carries `node_sha256` =
                                 sha256(ast.dump(node)) — never the file's sha [L-0.24].  A row's
                                 `equal_to` lists what its value is asserted equal to and by whom.
  CONTRACT_TOKENS_UNPINNED.json  DATA.  Every digit-bearing token of the prefix that is not inside
                                 a map row's capture, with its class [TOTALITY].

THE LAWS THE DOOR HOLDS (each a HALT; the suite scripts/tierc12_pins_fixtures.py plants each):
  CONTRACT-PREFIX · CONTRACT-TAIL  the first N bytes hash to the STEP Q sha; the tail is empty or
                                   whole `BUILT: ` lines [L-0.1, L-X.16].  ONE function,
                                   `contract_prefix`, for every reader of the contract.
  PIN-SLICE                        text = "\\n".join(lines[a-1:b]), 1-indexed, inclusive, inside
                                   the prefix (TC11's slice law).
  PIN-MAP · PIN-ARITY              the map's schema; a row's `type` arity == its regex's groups.
  PIN-PARSE                        a row's regex matches its slice exactly once.
  PIN-ALSO                         a second citation (a stage line and the VETOES line) parses to
                                   the SAME value.
  FAMILY-PARSE · FAMILY-BAR · FAMILY-MEMBER · FAMILY-M-COUNT
                                   the three stage headers, q, bar == q ÷ m exactly (fractions),
                                   and the registration ids standing under each header == m
                                   [L-0.18, L-X.1, L-X.2].
  PIN-FILED · PIN-SLICE-SHA        the re-derivation == CONTRACT_PINS.json.
  PIN-REGISTER · REGISTER-KIND · REGISTER-VETO · LINEAGE-NODE · X-SOURCE · PIN-EQUAL · PIN-TOTALITY
                                   `check()` — the register against the map, the sources that
                                   exist at TC12-REG, the equalities the door itself makes (a
                                   literal of a frozen file read as TEXT by `ast`, its node sha
                                   asserted, or an X record read as JSON, its manifest sha
                                   asserted), and the totality of the contract's digits.
Values are parsed EXACTLY (`fractions.Fraction` on the captured text) and converted to float only
at the use site.  A value the operator substitutes by veto is filed in LEANS_AMENDMENTS.md as a
line `PIN <name> := <value>` under a heading whose basis is `operator veto "<token>"`, and is read
from there by this door; it is never typed in code [L-0.23].

PUBLIC API (the default door reads the tree this file stands in; `Door(...)` takes other paths —
the suite's scratch copies):
  contract_prefix(contract, step_q, rel=CONTRACT_REL) -> {path, lines, n_lines, prefix_bytes,
                 prefix_sha256, whole_file_sha256}        THE one prefix function [L-0.1]
  cut(lines, a, b) -> str                                 TC11's slice law, inside the prefix
  load() -> {pin: value}          the HALTing door (prefix, map, parse, also, families, filed file)
  pin(name) -> int | Fraction | str | tuple               one contract pin, exact
  text(name) -> tuple[str, ...]                           the captured text (decimals as written)
  families() -> {q, q_text, q_exact, q_line, families [...], by_registration {...}}  [L-0.18]
  family_of(registration_id) -> dict
  veto_tokens() -> [{token, value_text}]                  the VETOES line, in order
  fixture_names() -> [str]                                the FIXTURES line's names [L-0.19]
  register() -> [row] · row(name) -> row · veto_rows() -> {token: [pin]}   the register and
                 its veto map [L-0.23]
  x_value(name) -> the value at an x_record row's source, the X manifest sha asserted [O-4]
  prefix() -> the default door's `contract_prefix` result (memoised)
  amended() -> {pin: {am, token, values, quoted}}         operator substitutions on file
  flow_line(name) -> "  [FLOW] <pin> @ <door>: <witness> moved"   F-TYPED-FLOW's fixed line
  bend(name, value) -> context manager                    the bend AT THE DOOR of the flow leg
  check() -> [finding]            everything the door asserts at filing; [] is GREEN
  iso_ms(text) -> int · literal_node(text, name, at=()) · node_sha(node) · main_tree(root)
  census_sha_findings(name, text, shas, min_len) -> [finding]   PIN-CENSUS-SHA [L-0.24]

Run (TC12-REG; no env, no network, no bar):
  ~/venvs/naiad/bin/python -B /Users/luis/Naiad/scripts/tierc12_pins.py            # check, print
  ~/venvs/naiad/bin/python -B /Users/luis/Naiad/scripts/tierc12_pins.py --file     # CONTRACT_PINS.json
      [--refile] [--pins-dir=DIR]
Exit 0 = the door is GREEN · 1 = a finding · a HALT raises SystemExit with its text.
"""
from __future__ import annotations

import ast
import contextlib
import hashlib
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_REL = "exchange/queue/2026-10-08_TC12_APOLLO.md"
T12_REL = "research_outputs/tierc12"
STEP_Q_REL = T12_REL + "/progress/STEP_Q.json"
PINS_REL = T12_REL + "/pins"
AMENDMENTS_REL = T12_REL + "/LEANS_AMENDMENTS.md"
X_REC_REL = T12_REL + "/x_rec"
X_MANIFEST_REL = X_REC_REL + "/X_REC_MANIFEST.json"
UNITS_REL = "scripts/tierc12_units.py"
MAP_NAME = "CONTRACT_PIN_MAP.json"
PINS_NAME = "CONTRACT_PINS.json"
REGISTER_NAME = "PIN_REGISTER.json"
UNPINNED_NAME = "CONTRACT_TOKENS_UNPINNED.json"

KINDS = ("contract", "x_record", "stage_d", "fitted", "lineage", "ruling")
TYPES = ("int", "fraction", "word", "iso", "str")
MAP_ROW_KEYS = ("pin", "lines", "regex", "type", "word_map", "also")
ALSO_KEYS = ("lines", "regex", "group")
REGISTER_KEYS = ("pin", "kind", "source", "door", "consumers", "witness", "veto")
FAM_Q = "fam.q"
FAM_PREFIX = "fam."
ISO_FORMAT = "%Y-%m-%dT%H:%MZ"
FLOW_FORM = "  [FLOW] {pin} @ {door}: {witness} moved"
LAW = ("derived by scripts/tierc12_pins.py --file from the first prefix_bytes bytes of the contract "
       "through CONTRACT_PIN_MAP.json; at every run the pin door re-derives every leaf and HALTs "
       "unless equal [LEANS L-0.17]")

TAIL_RX = re.compile(r"BUILT: \S.*")
DIGITS_RX = re.compile(r"[0-9]+")
EXACT_RX = re.compile(r"[0-9]+/[0-9]+")
AM_HEAD_RX = re.compile(r"## (AM-[0-9]+) · ")
AM_VETO_RX = re.compile(r'operator veto "([^"]+)"')
AM_PIN_RX = re.compile(r"PIN (\S+) := (\S.*)")
AM_QUOTE_RX = re.compile(r'operator\b[^"\n]*"[^"\n]+"', re.IGNORECASE)


def halt(tag: str, msg: str):
    raise SystemExit(f"HALT {tag}: {msg}")


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def read_json(p: Path):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def render(doc) -> bytes:
    """The one rendering of every file under pins/: sorted keys, a trailing newline, UTF-8."""
    return (json.dumps(doc, indent=1, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


def main_tree(root: Path) -> Path:
    """The main working tree: `root` itself, or — in a linked worktree whose .git is a `gitdir:`
    file — the tree that owns .git/worktrees/<name> (TC11's `_main_tree`, mirrored).  x_rec/ is
    git-ignored and exists only there [CANON-26]."""
    g = Path(root) / ".git"
    if g.is_file():
        txt = g.read_text(encoding="utf-8").strip()
        if txt.startswith("gitdir:"):
            gd = Path(txt.split(":", 1)[1].strip())
            gd = gd if gd.is_absolute() else (Path(root) / gd).resolve()
            if gd.parent.name == "worktrees" and gd.parent.parent.name == ".git":
                return gd.parent.parent.parent
    return Path(root)


# ═══════════════════════════════════════════════════════ THE PREFIX PIN [L-0.1, L-X.16]
def contract_prefix(contract: Path, step_q: Path, rel: str = CONTRACT_REL) -> dict:
    """THE one function every reader of the contract applies.  N and the sha are read from the
    STEP Q record, never typed.  HALT CONTRACT-PREFIX unless the file holds N bytes hashing to
    that sha and byte N is a newline; HALT CONTRACT-TAIL unless the bytes after N are empty or
    whole `BUILT: ` lines.  `lines[i - 1]` is contract line i; the last element is the empty
    string after the prefix's final newline."""
    rec = read_json(step_q)["artifact_shas"][rel]
    n, want = rec["bytes"], rec["sha256"]
    raw = Path(contract).read_bytes()
    if len(raw) < n or sha_bytes(raw[:n]) != want or raw[n - 1:n] != b"\n":
        halt("CONTRACT-PREFIX", f"the first {n} bytes of {rel} are not the STEP Q bytes "
                                f"(sha {want}); the contract of record is unreadable")
    tail = raw[n:].decode("utf-8", errors="replace")
    if tail and (not tail.endswith("\n")
                 or not all(TAIL_RX.fullmatch(x) for x in tail.split("\n")[:tail.count("\n")])):
        halt("CONTRACT-TAIL", f"the bytes after byte {n} of {rel} are not whole `BUILT: ` lines")
    lines = raw[:n].decode("utf-8").split("\n")
    return {"path": rel, "lines": lines, "n_lines": len(lines) - 1, "prefix_bytes": n,
            "prefix_sha256": want, "whole_file_sha256": sha_bytes(raw)}


def cut(lines: list, a, b) -> str:
    """TC11's slice law: "\\n".join(lines[a-1:b]) — 1-indexed, inclusive, leading whitespace kept,
    no trailing newline.  HALT PIN-SLICE on a slice outside the prefix."""
    if not (type(a) is int and type(b) is int and 1 <= a <= b <= len(lines) - 1):
        halt("PIN-SLICE", f"lines [{a}, {b}] are not a slice of the prefix "
                          f"(1..{len(lines) - 1})")
    return "\n".join(lines[a - 1:b])


def iso_ms(text: str) -> int:
    """A contract instant at minutes precision (`<date>T<hh>:<mm>Z`) as epoch milliseconds."""
    t = datetime.strptime(text, ISO_FORMAT).replace(tzinfo=timezone.utc)
    return (t - datetime.fromtimestamp(0, tz=timezone.utc)) // timedelta(milliseconds=1)


# ═══════════════════════════════════════════════════════ EXACT VALUES
def _parse(pin: str, kind: str, text: str, word_map) -> object:
    """One captured text -> its canonical, JSON-ready exact value."""
    if kind == "int":
        if not DIGITS_RX.fullmatch(text):
            halt("PIN-TYPE", f"{pin}: {text!r} is not an integer")
        return int(text)
    if kind == "fraction":
        try:
            f = Fraction(text)
        except (ValueError, ZeroDivisionError):
            halt("PIN-TYPE", f"{pin}: {text!r} is not an exact number")
        return f"{f.numerator}/{f.denominator}"
    if kind == "word":
        if not isinstance(word_map, dict) or text not in word_map:
            halt("PIN-WORD", f"{pin}: the word {text!r} is not in the row's word_map")
        return word_map[text]
    if kind == "iso":
        try:
            iso_ms(text)
        except ValueError:
            halt("PIN-TYPE", f"{pin}: {text!r} is not an instant of the form {ISO_FORMAT}")
        return text
    if kind == "str":
        return text
    halt("PIN-MAP", f"{pin}: type member {kind!r} is not one of {list(TYPES)}")


def _py(kind: str, canon) -> object:
    """The canonical value -> the object a consumer receives (never a float)."""
    if type(canon) is str and (kind == "fraction" or (kind == "word" and EXACT_RX.fullmatch(canon))):
        return Fraction(canon)
    return canon


def _canon(v) -> object:
    """Exact comparison form: every number a Fraction (a float through its shortest decimal)."""
    if isinstance(v, bool):
        return v
    if isinstance(v, (int, Fraction)):
        return Fraction(v)
    if isinstance(v, float):
        return Fraction(repr(v))
    if isinstance(v, (list, tuple)):
        return tuple(_canon(x) for x in v)
    return v


def _spans(slice_text: str, first_line: int, m, groups) -> list:
    """The (line, start, end) spans of the named capture groups of a match over a slice."""
    out = []
    for g in groups:
        s, e = m.span(g)
        if s < 0:
            continue
        line = first_line + slice_text.count("\n", 0, s)
        base = slice_text.rfind("\n", 0, s) + 1
        if "\n" in slice_text[s:e]:
            halt("PIN-PARSE", f"a capture group spans a line break at contract :{line}")
        out.append((line, s - base, e - base))
    return out


# ═══════════════════════════════════════════════════════ FROZEN TEXT, READ AS TEXT
_TREES: dict = {}       # source text sha -> its parsed module (a frozen source is parsed once)


def literal_node(text: str, name: str, at=()):
    """The value node of the LAST module-level assignment to `name` in source TEXT — or, for a
    name written `<function>.<parameter>`, the default of that parameter of the module-level
    function — walked by `at`: steps ["key", k] (a dict display's constant key), ["index", i] (a
    tuple or list display's element) or ["call_arg", fn, i] (argument i of the one call to `fn`
    inside the node).  The source is never imported."""
    node = None
    key = sha_bytes(text.encode("utf-8"))
    if key not in _TREES:
        _TREES[key] = ast.parse(text)
    fn_name, _, param = name.partition(".")
    for st in _TREES[key].body if param else ():
        if isinstance(st, ast.FunctionDef) and st.name == fn_name:
            pos = st.args.posonlyargs + st.args.args
            dflt = dict(zip([a.arg for a in pos[len(pos) - len(st.args.defaults):]],
                            st.args.defaults))
            dflt.update({a.arg: d for a, d in zip(st.args.kwonlyargs, st.args.kw_defaults)
                         if d is not None})
            node = dflt.get(param)
    for st in () if param else _TREES[key].body:
        targets = (st.targets if isinstance(st, ast.Assign)
                   else [st.target] if isinstance(st, ast.AnnAssign) and st.value is not None
                   else [])
        if any(isinstance(t, ast.Name) and t.id == name for t in targets):
            node = st.value
    if node is None:
        raise KeyError(f"no module-level assignment to {name}")
    for step in at:
        op = step[0]
        if op == "key" and isinstance(node, ast.Dict):
            hits = [v for k, v in zip(node.keys, node.values)
                    if isinstance(k, ast.Constant) and k.value == step[1]]
            if len(hits) != 1:
                raise KeyError(f"{name}: key {step[1]!r} stands {len(hits)} times")
            node = hits[0]
        elif op == "index" and isinstance(node, (ast.Tuple, ast.List)):
            node = node.elts[step[1]]
        elif op == "call_arg":
            hits = [c for c in ast.walk(node) if isinstance(c, ast.Call)
                    and isinstance(c.func, ast.Name) and c.func.id == step[1]]
            if len(hits) != 1:
                raise KeyError(f"{name}: {len(hits)} calls to {step[1]}")
            node = hits[0].args[step[2]]
        else:
            raise KeyError(f"{name}: step {step!r} does not apply to {type(node).__name__}")
    return node


def node_sha(node) -> str:
    """sha256(ast.dump(node)) — the pin of a literal read from a script whose FILE sha TC12's own
    close acts move [L-0.24]."""
    return sha_bytes(ast.dump(node).encode("utf-8"))


def _walk(value, at):
    """Value-level steps over a parsed object: ["key", k], ["index", i], ["each", i]."""
    for step in at:
        op = step[0]
        if op == "each":
            value = [x[step[1]] for x in value]
        elif op in ("key", "index"):
            value = value[step[1]]
        else:
            raise KeyError(f"step {step!r} is not a value step")
    return value


def census_sha_findings(name: str, text: str, shas: dict, min_len: int) -> list:
    """PIN-CENSUS-SHA: `text` carries the sha — whole, or abbreviated to a hex run of at least
    `min_len` characters that is a prefix of it — of a path of `shas` {path: sha256}: the files
    TC12's own close act moves, which no TC12 pin may name by whole-file sha [L-0.24]."""
    runs = sorted(set(re.findall(f"[0-9a-f]{{{min_len},}}", text)))
    return [f"PIN-CENSUS-SHA {name}: carries {run} — the whole-file sha of {path}, a file the "
            f"tc11-stamp close act moves; pin its AST node or its chain head instead"
            for path, sha in sorted(shas.items()) for run in runs if sha.startswith(run)]


# ═══════════════════════════════════════════════════════ THE DOOR
class Door:
    """One pin door over one set of paths.  The default door (module level) reads the tree this
    file stands in; a fixture builds a `Door` over scratch copies."""

    def __init__(self, *, root=None, contract=None, step_q=None, pins_dir=None, amendments=None,
                 main=None):
        self.root = Path(root) if root is not None else ROOT
        self.contract = Path(contract) if contract is not None else self.root / CONTRACT_REL
        self.step_q = Path(step_q) if step_q is not None else self.root / STEP_Q_REL
        self.pins_dir = Path(pins_dir) if pins_dir is not None else self.root / PINS_REL
        self.amendments = (Path(amendments) if amendments is not None
                           else self.root / AMENDMENTS_REL)
        self.main = Path(main) if main is not None else main_tree(self.root)
        self._memo: dict = {}
        self._loaded: dict | None = None

    # ── the texts ──
    def prefix(self) -> dict:
        if "prefix" not in self._memo:
            self._memo["prefix"] = contract_prefix(self.contract, self.step_q)
        return self._memo["prefix"]

    def map(self) -> dict:
        if "map" not in self._memo:
            p = self.pins_dir / MAP_NAME
            doc = read_json(p)
            bad = map_findings(doc)
            if bad:
                halt(bad[0].split(" ", 1)[0], bad[0].split(" ", 1)[1])
            self._memo["map"] = doc
            self._memo["map_sha"] = sha_bytes(p.read_bytes())
        return self._memo["map"]

    def map_row(self, name: str) -> dict:
        hit = [r for r in self.map()["rows"] if r["pin"] == name]
        if len(hit) != 1:
            halt("PIN-UNKNOWN", f"{name!r} is not a row of {MAP_NAME}")
        return hit[0]

    # ── the parse ──
    def _cite(self, pin: str, lines: list, cite: dict) -> tuple:
        a, b = cite["lines"]
        text = cut(lines, a, b)
        hits = list(re.finditer(cite["regex"], text))
        if len(hits) != 1:
            halt("PIN-PARSE", f"{pin}: the regex matches {len(hits)} times in contract "
                              f":{a}-{b} (exactly one is the law)")
        return text, hits[0]

    def parsed(self) -> dict:
        """{pin: {lines, slice_sha256, type, text, value, also [...], spans}} — the map applied to
        the prefix.  HALTs PIN-PARSE, PIN-TYPE, PIN-WORD, PIN-ALSO."""
        if "parsed" in self._memo:
            return self._memo["parsed"]
        lines = self.prefix()["lines"]
        out = {}
        for r in self.map()["rows"]:
            pin, kinds, wm = r["pin"], r["type"], r.get("word_map")
            text, m = self._cite(pin, lines, r)
            caps = list(m.groups())
            vals = [_parse(pin, k, c, wm) for k, c in zip(kinds, caps)]
            rec = {"lines": list(r["lines"]), "slice_sha256": sha_bytes(text.encode("utf-8")),
                   "type": list(kinds), "text": caps,
                   "value": vals[0] if len(vals) == 1 else vals}
            spans = [(pin, s) for s in _spans(text, r["lines"][0], m,
                                              range(1, len(caps) + 1))]
            also = []
            for c in r.get("also", ()):
                ctext, cm = self._cite(pin, lines, c)
                groups = [c["group"]] if "group" in c else list(range(1, len(kinds) + 1))
                ccaps = [cm.group(g) for g in groups]
                got = [_parse(pin, k, x, wm) for k, x in zip(kinds, ccaps)]
                if got != vals:
                    halt("PIN-ALSO", f"{pin}: contract :{r['lines'][0]}-{r['lines'][1]} reads "
                                     f"{caps} and its second citation "
                                     f":{c['lines'][0]}-{c['lines'][1]} reads {ccaps} — the two "
                                     f"places of the contract do not parse to one value")
                also.append({"lines": list(c["lines"]), "text": ccaps,
                             "slice_sha256": sha_bytes(ctext.encode("utf-8"))})
                spans += [(pin, s) for s in _spans(ctext, c["lines"][0], cm, groups)]
            if also:
                rec["also"] = also
            rec["spans"] = spans
            out[pin] = rec
        self._memo["parsed"] = out
        return out

    # ── the grammar texts that are not pins ──
    def _items(self, key: str, tag: str) -> list:
        s = self.map()["slices"][key]
        text = cut(self.prefix()["lines"], *s["lines"])
        if not text.startswith(s["head"]):
            halt(tag, f"contract :{s['lines'][0]} does not begin {s['head']!r}")
        body = " ".join(text[len(s["head"]):].split())
        if not body.endswith(s["end"]):
            halt(tag, f"contract :{s['lines'][1]} does not end {s['end']!r}")
        return body[:len(body) - len(s["end"])].split(s["sep"])

    def veto_tokens(self) -> list:
        """The tokens of the VETOES line, in order: [{token, value_text}] — value_text is the
        parenthesis the line gives after the token, or None."""
        out = []
        for item in self._items("vetoes", "VETO-PARSE"):
            m = re.fullmatch(self.map()["slices"]["vetoes"]["item"], item)
            if not m:
                halt("VETO-PARSE", f"{item!r} is not `\"<token>\"` or `\"<token>\" (<value>)`")
            out.append({"token": m.group(1), "value_text": m.group(2)})
        if len({v["token"] for v in out}) != len(out):
            halt("VETO-PARSE", "a veto token stands twice on the VETOES line")
        return out

    def fixture_names(self) -> list:
        """The fixture names of the FIXTURES line, in order: tokens `F-<NAME>`, a pair written
        `F-<X>-2/3` read as two, and the unprefixed names the map lists [L-0.19]."""
        s, out = self.map()["slices"]["fixtures"], []
        for item in self._items("fixtures", "FIXTURE-PARSE"):
            m = re.match(s["item"], item)
            if m:
                out.append(m.group(1))
                if m.group(2) is not None:
                    stem = m.group(1)
                    out.append(stem[:len(stem) - len(DIGITS_RX.findall(stem).pop())] + m.group(2))
            elif item in s["unprefixed"]:
                out.append(item)
            else:
                halt("FIXTURE-PARSE", f"{item!r} names no fixture")
        if len(set(out)) != len(out):
            halt("FIXTURE-PARSE", "a fixture name stands twice on the FIXTURES line")
        return out

    # ── the families [L-0.18, L-X.1, L-X.2] ──
    def _families(self, values: dict) -> dict:
        lines, m = self.prefix()["lines"], self.map()
        g = m["grammar"]
        n = self.prefix()["n_lines"]
        fam_rows = sorted((r for r in m["rows"]
                           if r["pin"].startswith(FAM_PREFIX) and r["pin"] != FAM_Q),
                          key=lambda r: r["lines"][0])
        q_row = self.map_row(FAM_Q)
        rx = sorted({r["regex"] for r in fam_rows})
        if len(rx) != 1 or any(r["lines"][0] != r["lines"][1] for r in fam_rows + [q_row]):
            halt("FAMILY-PARSE", "the family rows of the map do not share one header regex on "
                                 "one line each")
        heads = [i for i in range(1, n + 1) if re.match(rx[0], lines[i - 1])]
        if heads != [r["lines"][0] for r in fam_rows]:
            halt("FAMILY-PARSE", f"the lines matching the family header regex are {heads}; the "
                                 f"map's family rows stand on "
                                 f"{[r['lines'][0] for r in fam_rows]}")
        qs = [i for i in range(1, n + 1) if re.search(q_row["regex"], lines[i - 1])]
        if qs != [q_row["lines"][0]]:
            halt("FAMILY-PARSE", f"the lines stating `bar = q ÷ m` are {qs}; the map's "
                                 f"{FAM_Q} row stands on {q_row['lines'][0]}")
        q = values[FAM_Q]
        fams = []
        for r in fam_rows:
            stage, name, m_f, bar = values[r["pin"]]
            if r["pin"] != FAM_PREFIX + stage:
                halt("FAMILY-PARSE", f"the row {r['pin']} captures stage letter {stage!r}")
            if type(m_f) is not int or m_f < 1 or bar != q / m_f:
                halt("FAMILY-BAR", f"family {name} (contract :{r['lines'][0]}): the header's bar "
                                   f"{bar} is not q ÷ m = {q} ÷ {m_f}")
            h = r["lines"][0]
            fams.append({"family": name, "stage": stage, "header_line": h,
                         "header_text": lines[h - 1],
                         "header_text_sha256": sha_bytes(lines[h - 1].encode("utf-8")),
                         "m": m_f, "q": self.parsed()[FAM_Q]["text"][0],
                         "bar": self.parsed()[r["pin"]]["text"][len(r["type"]) - 1],
                         "bar_exact": f"{bar.numerator}/{bar.denominator}", "bar_fraction": bar,
                         "n_registrations": 0, "registrations": [], "registration_lines": [],
                         "priors_pct": []})
        if (len({f["family"] for f in fams}) != len(fams)
                or len({f["stage"] for f in fams}) != len(fams)):
            halt("FAMILY-PARSE", "two families share a name or a stage letter")
        by_id = {}
        for i in range(1, n + 1):
            mm = re.match(g["registration"], lines[i - 1])
            if not mm:
                continue
            below = [f for f in fams if f["header_line"] < i]
            f = below.pop() if below else None
            if f is None or any(re.match(g["stage"], lines[j - 1])
                                for j in range(f["header_line"] + 1, i + 1)):
                halt("FAMILY-MEMBER", f"registration {mm.group(1)} (contract :{i}) stands under "
                                      f"no family header")
            if mm.group(1) in by_id:
                halt("FAMILY-MEMBER", f"registration id {mm.group(1)} stands twice")
            f["registrations"].append(mm.group(1))
            f["registration_lines"].append(i)
            f["priors_pct"].append(int(mm.group(2)))
            f["n_registrations"] += 1
            by_id[mm.group(1)] = {"registration": mm.group(1), "line": i,
                                  "prior_pct": int(mm.group(2)), "family": f["family"],
                                  "stage": f["stage"], "m": f["m"], "bar": f["bar"],
                                  "bar_exact": f["bar_exact"], "bar_fraction": f["bar_fraction"]}
        for f in fams:
            if f["n_registrations"] != f["m"]:
                halt("FAMILY-M-COUNT", f"family {f['family']}: {f['n_registrations']} "
                                       f"registration id(s) stand under contract "
                                       f":{f['header_line']} ({f['registrations']}); the header "
                                       f"declares m = {f['m']}")
        return {"q": q, "q_text": self.parsed()[FAM_Q]["text"][0],
                "q_exact": f"{q.numerator}/{q.denominator}", "q_line": q_row["lines"][0],
                "families": fams, "by_registration": by_id}

    def families(self) -> dict:
        """{q (Fraction), q_text, q_exact, q_line, families [{family, stage, header_line,
        header_text, header_text_sha256, m, q, bar, bar_exact, bar_fraction, n_registrations,
        registrations, registration_lines, priors_pct}], by_registration {id: {...}}} — read from
        the LOADED pins, so a bend at the door reaches it.  HALT unless bar == q ÷ m and the ids
        under each header number m."""
        return self._families(self.load())

    def family_of(self, registration_id: str) -> dict:
        by = self.families()["by_registration"]
        if registration_id not in by:
            halt("FAMILY-MEMBER", f"{registration_id!r} is not a registration id of the contract")
        return by[registration_id]

    # ── the derived file ──
    def derive(self) -> dict:
        """The whole derived document — what `--file` writes and every run re-derives."""
        pre, parsed = self.prefix(), self.parsed()
        self.map()
        values = {p: self._value(p, parsed[p]["value"]) for p in parsed}
        fam = self._families(values)
        fam_doc = {"q": fam["q_text"], "q_exact": fam["q_exact"], "q_line": fam["q_line"],
                   "families": [{k: v for k, v in f.items() if k != "bar_fraction"}
                                for f in fam["families"]]}
        return {"law": LAW,
                "contract": {"path": pre["path"], "prefix_bytes": pre["prefix_bytes"],
                             "prefix_sha256": pre["prefix_sha256"], "n_lines": pre["n_lines"]},
                "map": {"path": f"{PINS_REL}/{MAP_NAME}", "sha256": self._memo["map_sha"]},
                "pins": {p: {k: v for k, v in rec.items() if k != "spans"}
                         for p, rec in sorted(parsed.items())},
                "families": fam_doc, "veto_tokens": self.veto_tokens(),
                "fixture_names": self.fixture_names()}

    def _value(self, pin: str, canon):
        kinds = self.map_row(pin)["type"]
        if len(kinds) == 1:
            return _py(kinds[0], canon)
        return tuple(_py(k, c) for k, c in zip(kinds, canon))

    def filed(self) -> dict:
        p = self.pins_dir / PINS_NAME
        if not p.exists():
            halt("PIN-FILED", f"{PINS_NAME} is not on file — run scripts/tierc12_pins.py --file")
        return read_json(p)

    def filed_findings(self) -> list:
        """PIN-SLICE-SHA / PIN-FILED: the re-derivation against the filed file, leaf by leaf."""
        new, old, out = self.derive(), self.filed(), []
        for p in sorted(set(new["pins"]) | set(old.get("pins", {}))):
            a, b = new["pins"].get(p), old.get("pins", {}).get(p)
            if a is None or b is None:
                out.append(f"PIN-FILED {p}: {'derived' if b is None else 'filed'} only — the "
                           f"map and {PINS_NAME} do not hold the same pins")
            elif (a["lines"], a["slice_sha256"]) != (b.get("lines"), b.get("slice_sha256")):
                out.append(f"PIN-SLICE-SHA {p}: the slice of the map row "
                           f"(:{a['lines'][0]}-{a['lines'][1]}, sha {a['slice_sha256'][:12]}…) "
                           f"is not the filed slice")
            elif a != b:
                out.append(f"PIN-FILED {p}: re-derived {a['value']!r} from {a['text']}, filed "
                           f"{b.get('value')!r} from {b.get('text')}")
        for k in sorted(set(new) | set(old)):
            if k != "pins" and new.get(k) != old.get(k):
                out.append(f"PIN-FILED {k}: the re-derived leaf is not the filed leaf")
        return out

    # ── the HALTing door ──
    def load(self) -> dict:
        """{pin: value} — every contract pin, exact.  HALTs unless the prefix is the STEP Q
        bytes, the map is well-formed, every row parses once, every second citation agrees, the
        families hold bar == q ÷ m, and the re-derivation equals CONTRACT_PINS.json.  An operator
        substitution on file (LEANS_AMENDMENTS.md) replaces the contract's value."""
        if self._loaded is None:
            bad = self.filed_findings()
            if bad:
                halt(bad[0].split(" ", 1)[0], bad[0].split(" ", 1)[1])
            parsed = self.parsed()
            values = {p: self._value(p, parsed[p]["value"]) for p in sorted(parsed)}
            for p, sub in sorted(self.amended().items()):
                if p in values:
                    r = self.map_row(p)
                    if len(sub["values"]) != len(r["type"]):
                        halt("PIN-AMENDED", f"{sub['am']} gives {p} {len(sub['values'])} "
                                            f"value(s); the pin holds {len(r['type'])}")
                    canon = [_parse(p, k, t, r.get("word_map"))
                             for k, t in zip(r["type"], sub["values"])]
                    values[p] = self._value(p, canon[0] if len(canon) == 1 else canon)
            self._loaded = values
        return self._loaded

    def pin(self, name: str):
        vals = self.load()
        if name not in vals:
            halt("PIN-UNKNOWN", f"{name!r} is not a contract pin (a row of {MAP_NAME})")
        return vals[name]

    def text(self, name: str) -> tuple:
        self.load()
        if name not in self.parsed():
            halt("PIN-UNKNOWN", f"{name!r} is not a contract pin (a row of {MAP_NAME})")
        return tuple(self.parsed()[name]["text"])

    @contextlib.contextmanager
    def bend(self, name: str, value):
        """The flow leg's bend AT THE DOOR [L-0.17]: inside the block `pin(name)` and every door
        function that reads it see `value`; the filed files and the comparator are untouched."""
        vals = self.load()
        if name not in vals:
            halt("PIN-UNKNOWN", f"{name!r} is not a contract pin (a row of {MAP_NAME})")
        kept = vals[name]
        vals[name] = value
        try:
            yield kept
        finally:
            vals[name] = kept

    # ── the register and the veto map [L-0.17, L-0.23] ──
    def register_doc(self) -> dict:
        if "register" not in self._memo:
            self._memo["register"] = read_json(self.pins_dir / REGISTER_NAME)
        return self._memo["register"]

    def register(self) -> list:
        return self.register_doc()["rows"]

    def row(self, name: str) -> dict:
        hit = [r for r in self.register() if r.get("pin") == name]
        if len(hit) != 1:
            halt("PIN-UNKNOWN", f"{name!r} is not a row of {REGISTER_NAME}")
        return hit[0]

    def veto_rows(self) -> dict:
        """{token: sorted register rows carrying it} over the tokens of the VETOES line and any
        other token a row carries."""
        out = {v["token"]: [] for v in self.veto_tokens()}
        for r in self.register():
            if r.get("veto") is not None:
                out.setdefault(r["veto"], []).append(r["pin"])
        return {k: sorted(v) for k, v in sorted(out.items())}

    def flow_line(self, name: str) -> str:
        """F-TYPED-FLOW's fixed line for a pin, read from its register row."""
        r = self.row(name)
        return FLOW_FORM.format(pin=name, door=r["door"], witness=r["witness"])

    # ── the other doors' sources that exist at TC12-REG ──
    def x_manifest(self) -> dict:
        if "x_manifest" not in self._memo:
            doc = read_json(self.main / X_MANIFEST_REL)
            self._memo["x_manifest"] = {f["copy"]: f["sha256"] for f in doc["files"]}
        return self._memo["x_manifest"]

    def x_json(self, rel: str):
        """An X record under x_rec/, read as JSON with its sha asserted against the manifest
        [O-4].  `rel` is the repo-relative path of the byte copy."""
        want = self.x_manifest().get(rel)
        raw = (self.main / rel).read_bytes()
        if want is None or sha_bytes(raw) != want:
            halt("X-SOURCE", f"{rel} is not at its X_REC_MANIFEST sha")
        return json.loads(raw.decode("utf-8"))

    def x_value(self, name: str):
        """The value at an x_record row's source (the lookbacks, O-15), manifest sha asserted."""
        r = self.row(name)
        if r["kind"] != "x_record":
            halt("PIN-UNKNOWN", f"{name!r} is not an x_record row")
        return _walk(self.x_json(r["source"]["path"]),
                     [["key", k] for k in r["source"]["key"].split(".")])

    def _unit(self, name: str):
        return ast.literal_eval(literal_node((self.root / UNITS_REL).read_text(encoding="utf-8"),
                                             name))

    def _object(self, spec: dict) -> tuple:
        """One second object of an `equal_to` the door itself reads: (value, how it is pinned)."""
        at = spec.get("at", [])
        if spec["read"] == "ast":
            node_at = [s for s in at if s[0] != "each"]
            text = (self.main / spec["path"]).read_text(encoding="utf-8")
            node = literal_node(text, spec["name"], node_at)
            got = node_sha(node)
            if got != spec.get("node_sha256"):
                halt("LINEAGE-NODE", f"{spec['path']} `{spec['name']}` {node_at}: the AST node "
                                     f"hashes {got}, the register files "
                                     f"{spec.get('node_sha256')}")
            return _walk(ast.literal_eval(node), [s for s in at if s[0] == "each"]), "node sha"
        if spec["read"] == "json":
            return _walk(self.x_json(spec["path"]),
                         [["key", k] for k in spec["key"].split(".")] + at), "manifest sha"
        halt("PIN-EQUAL", f"read {spec['read']!r} is not `ast` or `json`")

    def equal_findings(self) -> list:
        """PIN-EQUAL: every `equal_to` item the register assigns to the DOOR — a literal of a
        frozen file read as text, or an X record read as JSON [L-0.17; seam 6 leaves the rest to
        the pin's consumer at its own stage]."""
        out = []
        vals = self.load()
        for r in self.register():
            for spec in r.get("equal_to", ()):
                if spec.get("by") != "door":
                    continue
                pin, op = r["pin"], spec.get("op", "eq")
                try:
                    obj, how = self._object(spec)
                    mine = iso_ms(vals[pin]) if op == "iso_ms" else _canon(vals[pin])
                    theirs = _canon(obj)
                    if op in ("eq", "iso_ms"):
                        ok = mine == theirs
                    elif op == "member":
                        ok = mine in theirs
                    elif op == "object_times_unit":
                        ok = mine == theirs * self._unit(spec["unit"])
                    elif op == "pin_times_unit":
                        ok = mine * self._unit(spec["unit"]) == theirs
                    else:
                        halt("PIN-EQUAL", f"{pin}: op {op!r} is not a relation of the door")
                except SystemExit as e:
                    out.append(str(e).replace("HALT ", "", 1))
                    continue
                except (KeyError, IndexError, OSError, ValueError, SyntaxError) as e:
                    out.append(f"PIN-EQUAL {pin}: the object {spec.get('object')!r} cannot be "
                               f"read — {type(e).__name__}: {e}")
                    continue
                if not ok:
                    out.append(f"PIN-EQUAL {pin}: the contract reads {vals[pin]!r}; "
                               f"{spec.get('object')} reads {obj!r} ({op}, by {how})")
        return out

    def register_findings(self) -> list:
        """The register against the map and against the sources that exist at TC12-REG."""
        out, seen, kind_of = [], set(), {}
        tokens = [v["token"] for v in self.veto_tokens()]
        map_rows = {r["pin"]: r for r in self.map()["rows"]}
        for r in self.register():
            pin = r.get("pin")
            miss = [k for k in REGISTER_KEYS if k not in r]
            if miss:
                out.append(f"REGISTER-ROW {pin}: lacks {miss}")
                continue
            if pin in seen:
                out.append(f"REGISTER-ROW {pin}: stands twice")
            seen.add(pin)
            kind_of.setdefault(pin, r["kind"])
            if r["kind"] not in KINDS:
                out.append(f"REGISTER-KIND {pin}: kind {r['kind']!r} is outside {list(KINDS)}")
                continue
            if r["veto"] is not None and r["veto"] not in tokens:
                out.append(f"REGISTER-VETO {pin}: {r['veto']!r} is not a token of the VETOES line")
            src = r["source"]
            if (not isinstance(src, dict) or "path" not in src
                    or ("key" in src) == ("lines" in src)):
                out.append(f"REGISTER-ROW {pin}: source is not {{path, key or lines}}")
                continue
            if (not isinstance(r["consumers"], list) or not r["consumers"]
                    or not isinstance(r["witness"], str) or not r["witness"]):
                out.append(f"REGISTER-ROW {pin}: no consumer record or no witness")
            if r["kind"] == "ruling" and ("value" in r or r["door"] is not None):
                out.append(f"REGISTER-ROW {pin}: a ruling row has no value and no door")
            if r["kind"] == "contract":
                m = map_rows.get(pin)
                if m is None:
                    out.append(f"PIN-REGISTER {pin}: a register row of kind contract with no "
                               f"row in {MAP_NAME}")
                elif src.get("lines") != m["lines"] or src["path"] != CONTRACT_REL:
                    out.append(f"PIN-REGISTER {pin}: the register cites {src}, the map cites "
                               f"contract :{m['lines'][0]}-{m['lines'][1]}")
            if r["kind"] == "lineage" and "node_sha256" in r:
                try:
                    node = literal_node((self.main / src["path"]).read_text(encoding="utf-8"),
                                        src["key"], r.get("at", []))
                    if node_sha(node) != r["node_sha256"]:
                        out.append(f"LINEAGE-NODE {pin}: `{src['key']}` of {src['path']} hashes "
                                   f"{node_sha(node)}, the register files {r['node_sha256']}")
                except (KeyError, IndexError, OSError, SyntaxError) as e:
                    out.append(f"LINEAGE-NODE {pin}: `{src['key']}` of {src['path']} cannot be "
                               f"read — {type(e).__name__}: {e}")
            if r["kind"] == "x_record":
                try:
                    self.x_value(pin)
                except SystemExit as e:
                    out.append(str(e).replace("HALT ", "", 1))
                except (KeyError, IndexError, OSError, ValueError) as e:
                    out.append(f"X-SOURCE {pin}: {src['key']} of {src['path']} cannot be read "
                               f"— {type(e).__name__}: {e}")
        for pin in sorted(set(map_rows) - seen):
            out.append(f"PIN-REGISTER {pin}: a map row with no register row")
        for pin in sorted(set(map_rows) & seen):
            if kind_of[pin] != "contract":
                out.append(f"PIN-REGISTER {pin}: a map row whose register row is of kind "
                           f"{kind_of[pin]!r}")
        return out

    # ── the totality of the contract's digits ──
    def unpinned(self) -> dict:
        if "unpinned" not in self._memo:
            self._memo["unpinned"] = read_json(self.pins_dir / UNPINNED_NAME)
        return self._memo["unpinned"]

    def digit_runs(self) -> list:
        """Every maximal digit run of the prefix: (line, start, end, text), in order."""
        lines = self.prefix()["lines"]
        return [(i + 1, m.start(), m.end(), m.group(0))
                for i, text in enumerate(lines) for m in DIGITS_RX.finditer(text)]

    def totality_findings(self) -> list:
        """PIN-TOTALITY: every digit run of the prefix lies inside exactly one map row's capture
        or inside exactly one classed token of CONTRACT_TOKENS_UNPINNED.json — never both, never
        neither.  Every line of the prefix is operative."""
        lines, out = self.prefix()["lines"], []
        doc = self.unpinned()
        classes = doc.get("classes", {})
        caps = [(pin, s) for rec in self.parsed().values() for pin, s in rec["spans"]]
        toks = []
        for t in doc.get("tokens", ()):
            where = f":{t.get('line')}:{t.get('start')}-{t.get('end')}"
            try:
                here = lines[t["line"] - 1][t["start"]:t["end"]]
            except (KeyError, IndexError, TypeError):
                out.append(f"PIN-TOTALITY {where}: not a span of the prefix")
                continue
            if t["line"] < 1 or here != t.get("token") or not DIGITS_RX.search(here):
                out.append(f"PIN-TOTALITY {where}: the entry reads {t.get('token')!r}, the "
                           f"prefix reads {here!r} — a stale or digitless token")
                continue
            if t.get("class") not in classes:
                out.append(f"PIN-TOTALITY {where} {here!r}: class {t.get('class')!r} is not one "
                           f"of {sorted(classes)}")
            toks.append((t["line"], t["start"], t["end"]))
        for line, s, e, text in self.digit_runs():
            c = sorted({pin for pin, (cl, cs, ce) in caps if cl == line and cs <= s and e <= ce})
            n_cap = sum(1 for pin, (cl, cs, ce) in caps if cl == line and cs <= s and e <= ce)
            n_tok = sum(1 for tl, ts, te in toks if tl == line and ts <= s and e <= te)
            here = lines[line - 1]
            stop = here.find(" ", e)
            ctx = here[here.rfind(" ", 0, s) + 1:len(here) if stop < 0 else stop]
            if n_cap + n_tok == 0:
                out.append(f"PIN-TOTALITY contract :{line}:{s} — the digit run {text!r} in "
                           f"`{ctx}` is unaccounted: inside no map row's capture and not "
                           f"classed in {UNPINNED_NAME}")
            elif n_cap + n_tok > 1:
                out.append(f"PIN-TOTALITY contract :{line}:{s} — the digit run {text!r} in "
                           f"`{ctx}` is accounted {n_cap + n_tok} times (captures of {c}, "
                           f"{n_tok} classed token(s))")
        return out

    # ── operator substitutions [L-0.23] ──
    def amendment_sections(self) -> list:
        """[{am, heading, token, pins [(name, value text)], quoted}] over LEANS_AMENDMENTS.md."""
        if not self.amendments.exists():
            return []
        out = []
        for line in self.amendments.read_text(encoding="utf-8").split("\n"):
            h = AM_HEAD_RX.match(line)
            if h:
                v = AM_VETO_RX.search(line)
                out.append({"am": h.group(1), "heading": line, "pins": [], "quoted": False,
                            "token": v.group(1) if v else None})
            elif out:
                p = AM_PIN_RX.fullmatch(line)
                if p:
                    out[len(out) - 1]["pins"].append((p.group(1), p.group(2)))
                elif AM_QUOTE_RX.search(line):
                    out[len(out) - 1]["quoted"] = True
        return out

    def amended(self) -> dict:
        """{pin: {am, token, values [text], quoted}} — the LAST substitution on file per pin."""
        out = {}
        for s in self.amendment_sections():
            for name, value in s["pins"]:
                out[name] = {"am": s["am"], "token": s["token"], "values": value.split(),
                             "quoted": s["quoted"]}
        return out

    def amendment_findings(self) -> list:
        """VETO-AMENDMENT: an amendment that changes a pin must carry the basis `operator veto
        "<token>"` with the token of that pin's register row, and quote the operator's words in
        its body."""
        out = []
        rows = {r["pin"]: r for r in self.register()}
        for s in self.amendment_sections():
            for name, value in s["pins"]:
                if name not in rows:
                    out.append(f"VETO-AMENDMENT {s['am']}: changes {name!r}, which is no row of "
                               f"{REGISTER_NAME}")
                elif s["token"] is None or rows[name]["veto"] != s["token"]:
                    out.append(f"VETO-AMENDMENT {s['am']}: changes {name} under the basis "
                               f"{s['token']!r}; the pin's veto token is "
                               f"{rows[name]['veto']!r} — only the operator's veto by that name "
                               f"changes it")
                if not s["quoted"]:
                    out.append(f"VETO-AMENDMENT {s['am']}: changes {name} and names no operator "
                               f"quote")
        return out

    # ── everything, at filing ──
    def check(self) -> list:
        """Every assertion of the door at TC12-REG, as findings ([] is GREEN).  `load()` HALTs
        first on its own laws."""
        self.load()
        self.families()
        return (self.register_findings() + self.totality_findings() + self.equal_findings()
                + self.amendment_findings())

    def file(self, refile: bool = False) -> str:
        """Write CONTRACT_PINS.json from the prefix (no clobber: differing bytes on file HALT
        unless `refile`)."""
        body = render(self.derive())
        p = self.pins_dir / PINS_NAME
        if p.exists() and p.read_bytes() != body and not refile:
            halt("PIN-FILED", f"{PINS_NAME} is on file with other bytes; nothing written "
                              f"(--refile replaces it, before the TC12-REG commit only)")
        if not p.exists() or p.read_bytes() != body:
            p.write_bytes(body)
        return sha_bytes(body)


def map_findings(doc: dict) -> list:
    """PIN-MAP / PIN-ARITY: the schema of CONTRACT_PIN_MAP.json [CANON-25 point 1]."""
    out, seen = [], set()
    for k in ("rows", "slices", "grammar"):
        if k not in doc:
            return [f"PIN-MAP the map lacks `{k}`"]
    for r in doc["rows"]:
        pin = r.get("pin")
        extra = sorted(set(r) - set(MAP_ROW_KEYS))
        if extra or any(k not in r for k in ("pin", "lines", "regex", "type")):
            out.append(f"PIN-MAP {pin}: a row is {{pin, lines, regex, type, word_map, also}}; "
                       f"this one carries {sorted(r)}")
            continue
        if pin in seen:
            out.append(f"PIN-MAP {pin}: stands twice")
        seen.add(pin)
        try:
            n = re.compile(r["regex"]).groups
        except re.error as e:
            out.append(f"PIN-MAP {pin}: the regex does not compile — {e}")
            continue
        if not isinstance(r["type"], list) or any(k not in TYPES for k in r["type"]):
            out.append(f"PIN-MAP {pin}: type {r['type']!r} is not a tuple over {list(TYPES)}")
        elif len(r["type"]) != n or n < 1:
            out.append(f"PIN-ARITY {pin}: the regex has {n} capture group(s), the row's type "
                       f"has {len(r['type'])} member(s)")
        if "word" in r["type"] and not isinstance(r.get("word_map"), dict):
            out.append(f"PIN-MAP {pin}: a word row carries no word_map")
        for c in r.get("also", ()):
            extra = sorted(set(c) - set(ALSO_KEYS))
            if extra or "lines" not in c or "regex" not in c:
                out.append(f"PIN-MAP {pin}: an `also` item is {{lines, regex, group}}")
                continue
            try:
                cn = re.compile(c["regex"]).groups
            except re.error as e:
                out.append(f"PIN-MAP {pin}: an `also` regex does not compile — {e}")
                continue
            if "group" in c:
                if len(r["type"]) != 1 or type(c["group"]) is not int or not 1 <= c["group"] <= cn:
                    out.append(f"PIN-ARITY {pin}: `group` {c['group']!r} names no single "
                               f"capture of a {cn}-group citation for a one-value row")
            elif cn != len(r["type"]):
                out.append(f"PIN-ARITY {pin}: a second citation has {cn} capture group(s), "
                           f"the row's type has {len(r['type'])} member(s), and no `group`")
    return out


# ═══════════════════════════════════════════════════════ THE DEFAULT DOOR
_DOOR: Door | None = None


def door() -> Door:
    global _DOOR
    if _DOOR is None:
        _DOOR = Door()
    return _DOOR


def load() -> dict:
    return door().load()


def pin(name: str):
    return door().pin(name)


def text(name: str) -> tuple:
    return door().text(name)


def families() -> dict:
    return door().families()


def family_of(registration_id: str) -> dict:
    return door().family_of(registration_id)


def veto_tokens() -> list:
    return door().veto_tokens()


def fixture_names() -> list:
    return door().fixture_names()


def register() -> list:
    return door().register()


def row(name: str) -> dict:
    return door().row(name)


def veto_rows() -> dict:
    return door().veto_rows()


def x_value(name: str):
    return door().x_value(name)


def amended() -> dict:
    return door().amended()


def flow_line(name: str) -> str:
    return door().flow_line(name)


def bend(name: str, value):
    return door().bend(name, value)


def check() -> list:
    return door().check()


def prefix() -> dict:
    return door().prefix()


def main(argv) -> int:
    opt = {a.split("=", 1)[0]: a.split("=", 1)[1] for a in argv if a.startswith("--") and "=" in a}
    d = Door(pins_dir=opt["--pins-dir"]) if "--pins-dir" in opt else door()
    if "--file" in argv:
        print(f"{PINS_NAME} sha256 {d.file(refile='--refile' in argv)}")
    found = d.check()
    fam = d.families()
    pre = d.prefix()
    print(f"contract {pre['path']} · prefix {pre['prefix_bytes']} B · sha {pre['prefix_sha256']} "
          f"· {pre['n_lines']} lines")
    print(f"q = {fam['q_text']} ({fam['q_exact']})")
    for f in fam["families"]:
        print(f"  STAGE {f['stage']} · {f['family']} · m = {f['m']} · bar {f['bar']} "
              f"({f['bar_exact']}) · {' '.join(f['registrations'])}")
    kinds = [r["kind"] for r in d.register()]
    print("register: " + " · ".join(f"{k} {kinds.count(k)}" for k in KINDS)
          + f" · {len(kinds)} rows; map {len(d.map()['rows'])} rows; "
            f"{len(d.unpinned().get('tokens', []))} classed tokens")
    for p, v in sorted(d.load().items()):
        print(f"  {p} = {v!r}")
    for f in found:
        print(f"FINDING: {f}")
    print(f"{len(found)} finding(s)")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
