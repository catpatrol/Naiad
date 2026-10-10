#!/usr/bin/env python
"""TIER-C12 · TC12-ENV.vendor — THE VENDORED REFEREE, THE HUNK TABLE AND THE LINEAGE PINS.

Contract of record: exchange/queue/2026-10-08_TC12_APOLLO.md ("one corridor", :5; "F-CTRL … to
0.000e+00", :48-49).  Executor HEPHAESTUS.  Readings of record: research_outputs/tierc12/LEANS.md
L-D.25 (the referee; the hunks as data), L-D.29 (the lineage modules, imported as-is and re-hashed
before any ride), L-D.30 (the order of the records); rulings O-3, O-4, O-31.

A PLAIN MODULE.  It imports the stdlib and the stdlib-only process tool tierc12_progress.  It never
imports the shim and never imports a lineage module: it reads source TEXT and hashes BYTES.  It opens
no tape, runs no out-of-process call and holds no clock.

THE REFEREE [L-D.25].  research_outputs/tierc12/vendor/tierc11_env@1526093b.py is a byte copy of TC11's
scripts/tierc11_env.py (copied, never retyped; never imported).  THREE SHAS MUST BE EQUAL: the copy's;
the one research_outputs/tierc11/PROGRESS.json certifies for scripts/tierc11_env.py under stage
TC11-ENV (read by key from `artifact_shas`; PROGRESS itself held to the sha TC12's R0 census recorded
for it, or to the stamped value close/TC11_STAMP_MAP.json names once that map reads applied: true);
and the live scripts/tierc11_env.py's — a difference there is a moved TC11 byte, a finding against
O-3.  The hex tag in the file name is a LABEL, asserted to prefix that sha; no sha is typed here.

THE HUNKS ARE DATA [L-D.25, L-D.26].  `ENV_HUNKS` is a table of (hunk number, what, old, new) entries
and `HUNK_NAMES` names the declared hunks; a hunk's number is its position in HUNK_NAMES, counted from
one.  `build_env_text(referee)` applies the entries in order: each `old` must occur EXACTLY ONCE in
the referee and in the text it is applied to; every declared hunk number is used and no other; the
built text must REVERT to the referee.  scripts/tierc12_env.py is that built text, written once and
byte-verified by --build-env at the TC12-ENV record; it is never hand-edited.  THE TABLE IS EMPTY AT
THIS RECORD: the referee is committed before any hunk is applied, and the entries are filed with the
shim they build.  The vendor transcript (env/FIXTURES_ENV_VENDOR.txt) stands on this module's API and
on its DETECTOR NAMES — referee_findings, three_shas, referee_tag, REFEREE_REL, hunk_numbers,
ENV_HUNKS, build_env_text; `sha != certified`, HUNK-NUMBER, HUNK-OLD, HUNK-UNUSED, HUNK-REVERT — and on
no wording: a record that extends this module keeps those and that transcript does not move.

THE LINEAGE PINS [L-D.29].  research_outputs/tierc12/env/LINEAGE_PINS.json, write-once:
  walk_roots       the lineage modules the REFEREE imports, read by AST from its import section (every
                   module-level `with _window(<name>, …): import <name> as <ALIAS>`), in its order;
  modules          {repo-relative path: sha256} for the STATIC repo import closure of those roots —
                   Import / ImportFrom anywhere (function bodies included), constant-string dynamic
                   imports and the repo modules a name-held dynamic import can name: the walk of
                   scripts/tierc11_closure_fixtures.py (`lineage_walk`), mirrored, NOT stopping at the
                   TC10 layer and not skipping the range machine.  Pinning is a superset law: this
                   record hashes every file the lineage can load, whether or not anything loads it;
  module_rows      the same modules with name, bytes and what each is held against;
  x_path_modules   X's filed record of the ride path, x_rec/tierc11x/forward/BOOK_SPECS.json
                   ["path_modules"] (its sha asserted against its X_REC_MANIFEST.json row, the
                   manifest's against tierc12_progress.certified): every key that is a main-tree file
                   must hash, in the main tree NOW, to X's value; X's own scripts are never imported
                   and are held equal to their x_rec/scripts/ copies;
  step_q_commit    the commit progress/STEP_Q.json names.

WHAT WOULD MAKE THIS WRONG: retyping the referee; taking a sha from a record by name instead of by
key; importing a module to learn what it imports (TC10's and TC11's modules guard their substrate at
import); stopping the pinning walk at the TC10 layer; re-pinning a drifted lineage module silently;
a hunk applied to a text in which its `old` stands twice.

Run (exactly one subcommand per invocation):
      export PYTHONDONTWRITEBYTECODE=1
      ~/venvs/naiad/bin/python -B /Users/luis/Naiad/scripts/tierc12_vendor.py --vendor
      ~/venvs/naiad/bin/python -B /Users/luis/Naiad/scripts/tierc12_vendor.py --pin-lineage
      ~/venvs/naiad/bin/python -B /Users/luis/Naiad/scripts/tierc12_vendor.py --verify
      ~/venvs/naiad/bin/python -B /Users/luis/Naiad/scripts/tierc12_vendor.py --build-env   (TC12-ENV)
  --out=DIR  the files a subcommand WRITES go under DIR at their repo-relative paths (a scratch
             build); every read is from this tree.
Exit: 0 done · 1 a HALT, or a finding of --verify.
"""
from __future__ import annotations

import ast
import hashlib
import json
import os
import re
import sys
from pathlib import Path

import tierc12_progress as PG                 # certified(): stdlib only

ROOT = Path(__file__).resolve().parents[1]
TIER, RECORD = "TIER-C12", "TC12-ENV.vendor"
T12_REL = PG.T12
T11_REL = "research_outputs/tierc11"
SOURCE_REL = "scripts/tierc11_env.py"         # TC11's shim: read as BYTES and as TEXT, never imported
SOURCE_STAGE = "TC11-ENV"                     # the stage of TC11's PROGRESS that certifies it
T11_PROGRESS_REL = T11_REL + "/PROGRESS.json"
R0_REL = T12_REL + "/progress/TC12-R0.json"
R0_KEY = "frozen_estate_shas_at_r0"
STAMP_MAP_REL = T12_REL + "/close/TC11_STAMP_MAP.json"
STEP_Q_REL = T12_REL + "/progress/" + PG.record_name(PG.ORDER[0])
PROGRESS_REL = T12_REL + "/PROGRESS.json"
VENDOR_REL = T12_REL + "/vendor"
REFEREE_REL = VENDOR_REL + "/tierc11_env@1526093b.py"      # the tag is a label, asserted to prefix the sha
README_REL = VENDOR_REL + "/README.md"
TAG_RX = re.compile(r"tierc11_env@([0-9a-f]+)\.py")
ENV_REL = "scripts/tierc12_env.py"            # built by --build-env at the TC12-ENV record
PINS_REL = T12_REL + "/env/LINEAGE_PINS.json"
X_REC_REL = T12_REL + "/x_rec"
X_MANIFEST_REL = X_REC_REL + "/X_REC_MANIFEST.json"
X_SPECS_REL = X_REC_REL + "/tierc11x/forward/BOOK_SPECS.json"
X_SPECS_KEY = "path_modules"
X_OWN_PREFIX = "scripts/tc11x_"               # X's own ride-path scripts: never imported, held to their copies
WINDOW_FN = "_window"                         # the referee's env window (its section 4)
DYN_FUNCS = ("import_module", "__import__", "tc10_import", "_tc10_import")
MOD_RX = re.compile(r"[A-Za-z_][A-Za-z0-9_]*(\.[A-Za-z_][A-Za-z0-9_]*)*")
HELD_X = "X path_modules"
HELD_OWN = "TC12 LINEAGE_PINS"


def halt(msg: str):
    raise SystemExit(f"HALT: {msg}")


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def render(doc) -> bytes:
    """The one rendering of a JSON record filed here: sorted keys, a trailing newline, UTF-8."""
    return (json.dumps(doc, indent=1, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


def main_tree(root) -> Path:
    """The main working tree: `root` itself, or — in a linked worktree whose .git is a `gitdir:`
    file — the tree that owns .git/worktrees/<name> (tierc12_pins.main_tree, mirrored).  x_rec/ is
    git-ignored and exists only there."""
    g = Path(root) / ".git"
    if g.is_file():
        txt = g.read_text(encoding="utf-8").strip()
        if txt.startswith("gitdir:"):
            gd = Path(txt.split(":", 1)[1].strip())
            gd = gd if gd.is_absolute() else (Path(root) / gd).resolve()
            if gd.parent.name == "worktrees" and gd.parent.parent.name == ".git":
                return gd.parent.parent.parent
    return Path(root)


def write_once(path: Path, body: bytes) -> str:
    """WRITE-ONCE, in code: a file that exists is never written again.  Identical bytes are left as
    they are; other bytes HALT.  A new file is written through a temp name and read back."""
    if path.exists():
        if path.read_bytes() != body:
            halt(f"{path.name} is WRITE-ONCE and is on file with other bytes — refusing to overwrite {path}")
        return "on file, identical — nothing written"
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_bytes(body)
    os.replace(tmp, path)
    if path.read_bytes() != body:
        halt(f"{path} does not read back as the bytes written")
    return "written once, byte-verified"


def require_depends(root=ROOT) -> None:
    """The record's floor [L-0.10 SUBSTAGES]: every record it depends on is on file and COMPLETE-VERIFIED
    (the referee is filed after TC12-D).  HALTS IF one is not."""
    recs = PG.records(root)
    for dep in PG.SUBSTAGES[RECORD]["depends_on"]:
        if recs.get(dep, {}).get("status") != PG.COMPLETE:
            halt(f"{RECORD} is filed after {dep} is {PG.COMPLETE}; its record reads "
                 f"{recs.get(dep, {}).get('status', PG.ABSENT)!r}")


# ═══════════════════════════════════════════════ 1 · THE REFEREE — three shas, one tag [L-D.25]
def tc11_progress(root=ROOT) -> dict:
    """TC11's PROGRESS.json, its bytes held to the sha TC12's R0 census recorded for it
    (progress/TC12-R0.json `frozen_estate_shas_at_r0`), or to the stamped value
    close/TC11_STAMP_MAP.json names for it when that map reads `applied: true` [L-0.24; L-0.4 seam
    12 — the one rule the Stage D builder, the suites and the shim share].  HALTS IF neither holds."""
    root = Path(root)
    raw = (root / T11_PROGRESS_REL).read_bytes()
    want = json.loads((root / R0_REL).read_text(encoding="utf-8"))[R0_KEY][T11_PROGRESS_REL]["sha256"]
    stamp = root / STAMP_MAP_REL
    if stamp.exists():
        doc = json.loads(stamp.read_text(encoding="utf-8"))
        if doc.get("applied") is True:
            for m in doc.get("moved", []):
                if m.get("path") == T11_PROGRESS_REL:
                    want = m["sha256_after"]
    if sha_bytes(raw) != want:
        halt(f"{T11_PROGRESS_REL} does not hash to the sha TC12's R0 census (or the applied stamp map) holds for it")
    return json.loads(raw)


def certified_source(root=ROOT) -> dict:
    """{bytes, sha256} TC11's PROGRESS certifies for scripts/tierc11_env.py UNDER STAGE TC11-ENV, read
    by key from that stage's `artifact_shas`.  HALTS IF the stage or the key is not there exactly once."""
    hits = [s for s in tc11_progress(root)["stages"] if s.get("stage") == SOURCE_STAGE]
    entry = hits[0].get("artifact_shas", {}).get(SOURCE_REL) if len(hits) == 1 else None
    if not isinstance(entry, dict):
        halt(f"{T11_PROGRESS_REL}: stage {SOURCE_STAGE} does not certify {SOURCE_REL} by key")
    return {"bytes": entry["bytes"], "sha256": entry["sha256"]}


def referee_tag() -> str:
    """The hex tag in the referee's file name (a label; `referee_findings` holds it to the sha)."""
    m = TAG_RX.fullmatch(Path(REFEREE_REL).name)
    if not m:
        halt(f"{REFEREE_REL}: the file name carries no hex tag")
    return m.group(1)


def three_shas(root=ROOT, referee=None) -> dict:
    """The three shas of L-D.25 as they stand: `certified` (TC11's PROGRESS, by key), `live`
    (scripts/tierc11_env.py now), `vendored` (the committed copy — or the bytes handed in as
    `referee`); None where a file is not on file."""
    root = Path(root)
    cert = certified_source(root)
    live, copy = root / SOURCE_REL, root / REFEREE_REL
    raw = referee if referee is not None else (copy.read_bytes() if copy.is_file() else None)
    return {"certified": cert["sha256"], "certified_bytes": cert["bytes"],
            "live": sha_bytes(live.read_bytes()) if live.is_file() else None,
            "vendored": None if raw is None else sha_bytes(raw),
            "vendored_bytes": None if raw is None else len(raw)}


def referee_findings(root=ROOT, referee=None) -> list:
    """What keeps the referee from being the referee.  VENDOR-ABSENT the copy is not on file ·
    VENDOR-SHA `sha != certified` (the copy's, or the live file's — a moved TC11 byte) · VENDOR-TAG
    the tag in the file name does not prefix the certified sha.  `referee` = bytes judged in place
    of the file's (a fixture's bent copy).  [] is GREEN."""
    s, out = three_shas(root, referee), []
    if s["vendored"] is None:
        out.append(f"VENDOR-ABSENT {REFEREE_REL}: the committed referee is not on file — run --vendor")
    elif s["vendored"] != s["certified"]:
        out.append(f"VENDOR-SHA {REFEREE_REL}: sha != certified — the copy hashes to {s['vendored']}, "
                   f"{T11_PROGRESS_REL} certifies {s['certified']} for {SOURCE_REL} under {SOURCE_STAGE}")
    if s["live"] != s["certified"]:
        out.append(f"VENDOR-SHA {SOURCE_REL}: sha != certified — the live file hashes to {s['live']}, not "
                   f"{s['certified']}: a moved TC11 byte, a finding against O-3")
    if not s["certified"].startswith(referee_tag()):
        out.append(f"VENDOR-TAG {REFEREE_REL}: the tag {referee_tag()!r} does not prefix the certified sha "
                   f"{s['certified']}")
    return out


README_TEXT = """# TC12 vendor referee

`{name}` is a byte-for-byte copy of TC11's `{source}`, taken from the main tree at the record `{record}` — after TC12-D, before any hunk is applied (LEANS L-D.25; ruling O-31).
- sha256 `{sha}`, {size} bytes, {lines} lines.
- This is the sha `{progress}` certifies for `{source}` under stage `{stage}`, read by key from `artifact_shas`. The tag `{tag}` in the file name is a label that prefixes it.
- Three shas are held equal: this copy's, the certified one, and the live `{source}`'s. `scripts/tierc12_vendor.py --verify` and F-VENDOR `[referee]` (`scripts/tierc12_env_fixtures.py --stage={record}`) hold them. A difference in the live file is a moved TC11 byte, a finding against O-3.

It is filed here, tracked, so that the referee survives any later TC11 edit and exists in every tree, detached review worktrees included. The file is never imported and never run. `{env}` is built from it by the declared hunks of `scripts/tierc12_vendor.py` (`ENV_HUNKS`) and nothing else; F-VENDOR reverts them and must meet this file byte for byte.
"""


def readme_bytes(raw: bytes) -> bytes:
    """vendor/README.md, rendered from the referee's own bytes (nothing in it is typed)."""
    return README_TEXT.format(
        name=Path(REFEREE_REL).name, source=SOURCE_REL, record=RECORD, sha=sha_bytes(raw), size=len(raw),
        lines=raw.count(b"\n"), progress=T11_PROGRESS_REL, stage=SOURCE_STAGE, tag=referee_tag(),
        env=ENV_REL).encode("utf-8")


def vendor(out=ROOT, root=ROOT) -> int:
    """--vendor: the BYTES of the live scripts/tierc11_env.py, copied to the referee path, with its
    README.  HALTS IF the live file is not the bytes TC11's PROGRESS certifies, or the tag does not
    prefix that sha — nothing is vendored from a moved file.  Write-once."""
    require_depends(root)
    cert = certified_source(root)
    raw = (Path(root) / SOURCE_REL).read_bytes()
    if sha_bytes(raw) != cert["sha256"] or len(raw) != cert["bytes"]:
        halt(f"the live {SOURCE_REL} is not the file {T11_PROGRESS_REL} certifies under {SOURCE_STAGE} — a "
             f"moved TC11 byte (O-3); nothing is vendored")
    if not cert["sha256"].startswith(referee_tag()):
        halt(f"the tag {referee_tag()!r} of {REFEREE_REL} does not prefix the certified sha {cert['sha256']}")
    print(f"{REFEREE_REL}: {write_once(Path(out) / REFEREE_REL, raw)} — sha256 {sha_bytes(raw)}, {len(raw)} bytes")
    print(f"{README_REL}: {write_once(Path(out) / README_REL, readme_bytes(raw))}")
    return 0


# ═══════════════════════════════════════════════ 2 · THE HUNKS ARE DATA [L-D.25, L-D.26]
# A hunk's NUMBER is its position in HUNK_NAMES, counted from one (L-D.26's table, in its order).
HUNK_NAMES = (
    "IDENTITY",
    "ROOTS AND GUARD",
    "PINS BY OBJECT",
    "RE-ROOTS, `fees()`, POST-SHIM",
    "PROTECTION (writes)",
    "READ JUDGES",
    "FORBIDDEN NAMES, THE RANGE DOOR AND THE VA-WALL EXIT CHECK",
    "ESTATE-MODULE EXEMPTION AND THE BINDING SCAN",
    "TEXT-ONLY",
    "API",
)
TEXT_ONLY_NAME = "TEXT-ONLY"                   # the one hunk that may change string literals only
# (hunk number, what, old, new), applied in order.  EMPTY AT THE RECORD TC12-ENV.vendor: the referee
# is committed before any hunk is applied; the entries are filed with the shim they build (TC12-ENV).
ENV_HUNKS: list = []


def H(no: int, what: str, old: str, new: str) -> None:
    ENV_HUNKS.append((no, what, old, new))


def hunk_numbers() -> tuple:
    """The declared hunk numbers: one per name of HUNK_NAMES, counted from one."""
    return tuple(range(1, len(HUNK_NAMES) + 1))


def text_only_hunk() -> int:
    return HUNK_NAMES.index(TEXT_ONLY_NAME) + 1


def revert_env_text(text: str, hunks=None) -> str:
    """The hunks reverted in REVERSE order.  Raises ValueError if a hunk's `new` is not exactly once
    in the text at its step (an undeclared edit inside a hunk's span shows as a miss here)."""
    hunks = ENV_HUNKS if hunks is None else hunks
    for i, (no, what, old, new) in reversed(list(enumerate(hunks))):
        if text.count(new) != 1:
            raise ValueError(f"ENV_HUNKS[{i}] hunk {no} ({what}): its `new` occurs {text.count(new)}x in the "
                             f"text at its revert step, not once")
        text = text.replace(new, old, 1)
    return text


def build_env_text(referee: str, hunks=None) -> str:
    """The referee + the hunks, in order.  HALTS IF a hunk number is not a declared one (HUNK-NUMBER);
    a hunk's `old` does not occur exactly once in the referee and in the text it is applied to
    (HUNK-OLD); a declared hunk number is unused (HUNK-UNUSED); or the built text does not revert to
    the referee (HUNK-REVERT)."""
    hunks = ENV_HUNKS if hunks is None else hunks
    text = referee
    for i, (no, what, old, new) in enumerate(hunks):
        if type(no) is not int or no not in hunk_numbers():
            halt(f"HUNK-NUMBER ENV_HUNKS[{i}] ({what}): hunk {no!r} is not one of the {len(HUNK_NAMES)} "
                 f"declared hunks [L-D.26]")
        if referee.count(old) != 1 or text.count(old) != 1:
            halt(f"HUNK-OLD ENV_HUNKS[{i}] hunk {no} ({what}): `old` occurs {referee.count(old)}x in the "
                 f"referee and {text.count(old)}x in the text so far — it must be exactly once in each")
        text = text.replace(old, new, 1)
    unused = sorted(set(hunk_numbers()) - {h[0] for h in hunks})
    if unused:
        halt(f"HUNK-UNUSED: hunk(s) {unused} of L-D.26 are declared and unused")
    try:
        back = revert_env_text(text, hunks)
    except ValueError as e:
        halt(f"HUNK-REVERT: {e}")
    if back != referee:
        halt("HUNK-REVERT: the built text does not revert to the referee — the hunk table is not a clean diff")
    return text


def build_env(out=ROOT, root=ROOT) -> int:
    """--build-env (the TC12-ENV record): scripts/tierc12_env.py = the referee + ENV_HUNKS and nothing
    else, written once and byte-verified.  HALTS on any law of `build_env_text`, and unless the
    referee is the referee."""
    bad = referee_findings(root)
    if bad:
        halt("the referee is not the referee — " + " | ".join(bad))
    referee = (Path(root) / REFEREE_REL).read_bytes()
    body = build_env_text(referee.decode("utf-8")).encode("utf-8")
    print(f"{ENV_REL}: {write_once(Path(out) / ENV_REL, body)} — sha256 {sha_bytes(body)}, {len(body)} bytes, "
          f"{len(ENV_HUNKS)} hunk entr{'y' if len(ENV_HUNKS) == 1 else 'ies'} over {REFEREE_REL}")
    return 0


# ═══════════════════════════════════════════════ 3 · THE LINEAGE PINS [L-D.29]
def _call_name(call: ast.Call) -> str:
    f = call.func
    return f.attr if isinstance(f, ast.Attribute) else getattr(f, "id", "")


def _const_str(node):
    return node.value if isinstance(node, ast.Constant) and isinstance(node.value, str) else None


def walk_roots(shim_text: str) -> list:
    """The lineage modules a shim text imports, in its order: every module-level
    `with _window(<name>, …): import <name> as <ALIAS>` of its import section.  Read by AST — the
    text is never imported.  HALTS IF a window's label is not the one module it imports, or there
    is no window."""
    roots = []
    for node in ast.parse(shim_text).body:
        if not isinstance(node, ast.With):
            continue
        calls = [i.context_expr for i in node.items
                 if isinstance(i.context_expr, ast.Call) and _call_name(i.context_expr) == WINDOW_FN]
        if not calls:
            continue
        label = _const_str(calls[0].args[0]) if calls[0].args else None
        names = [a.name for b in node.body if isinstance(b, ast.Import) for a in b.names]
        if label is None or names != [label]:
            halt(f"the import window labelled {label!r} imports {names} — not the one module it names")
        roots.append(label)
    if not roots:
        halt("the shim text holds no import window: its lineage roots cannot be read")
    return roots


def module_file(name: str, root=ROOT):
    """The repo file a module name resolves to (scripts/ first, then the repo root), or None
    (stdlib, third-party, absent)."""
    if not MOD_RX.fullmatch(name or ""):
        return None
    rel = name.replace(".", "/")
    for base in (Path(root) / "scripts", Path(root)):
        for p in (base / f"{rel}.py", base / rel / "__init__.py"):
            if p.is_file():
                return p
    return None


def walk_imports(tree) -> list:
    """Every module name a source can import by statement: Import / ImportFrom nodes ANYWHERE
    (function bodies included), each from-import also as module.name, plus a constant first
    argument of an import call."""
    out = []
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            out += [a.name for a in n.names]
        elif isinstance(n, ast.ImportFrom):
            mod = "." * n.level + (n.module or "")
            out.append(mod)
            out += [f"{mod}.{a.name}" if n.module else f"{mod}{a.name}" for a in n.names]
        elif isinstance(n, ast.Call) and _call_name(n) in DYN_FUNCS and n.args \
                and _const_str(n.args[0]) is not None:
            out.append(n.args[0].value)
    return out


def dyn_targets(tree, root=ROOT) -> list:
    """The repo modules a NAME-HELD import call can name: the string constants of its enclosing
    function, and of the module-level literals that function names, that resolve to a repo module."""
    lits = {t.id: n.value for n in tree.body if isinstance(n, ast.Assign)
            for t in n.targets if isinstance(t, ast.Name)}
    funcs = [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
    out = []
    for n in ast.walk(tree):
        if not (isinstance(n, ast.Call) and _call_name(n) in DYN_FUNCS):
            continue
        if n.args and _const_str(n.args[0]) is not None:
            continue
        enc = [g for g in funcs if g.lineno <= n.lineno <= (g.end_lineno or g.lineno)]
        scope = min(enc, key=lambda g: (g.end_lineno or g.lineno) - g.lineno) if enc else tree
        strings = {c.value for c in ast.walk(scope) if _const_str(c) is not None}
        for nm in ast.walk(scope):
            if isinstance(nm, ast.Name) and nm.id in lits:
                strings |= {c.value for c in ast.walk(lits[nm.id]) if _const_str(c) is not None}
        out += sorted(s for s in strings if module_file(s, root) is not None)
    return out


def repo_candidates(x: str, root=ROOT) -> list:
    """The repo modules an import of `x` executes: the longest dotted prefix that resolves to a repo
    file, and each parent package of it that does."""
    parts = x.split(".")
    for k in reversed(range(1, len(parts) + 1)):
        if module_file(".".join(parts[:k]), root) is not None:
            return [".".join(parts[:j]) for j in range(1, k + 1)
                    if module_file(".".join(parts[:j]), root) is not None]
    return []


def lineage_closure(roots, root=ROOT) -> dict:
    """{module name: repo-relative path} — the STATIC repo import closure of `roots`.  The walk does
    not stop at the TC10 layer and does not skip the range machine (a superset law)."""
    root = Path(root)
    queue, seen = list(roots), {}
    while queue:
        x = queue.pop(0)
        for c in repo_candidates(x, root):
            if c in seen:
                continue
            p = module_file(c, root)
            seen[c] = p.relative_to(root).as_posix()
            tree = ast.parse(p.read_text(encoding="utf-8"))
            queue += walk_imports(tree) + dyn_targets(tree, root)
    missing = [r for r in roots if r not in seen]
    if missing:
        halt(f"lineage root(s) {missing} resolve to no repo file")
    return dict(sorted(seen.items()))


def x_path_modules(root=ROOT) -> dict:
    """X's filed record of the ride path, verified and compared: BOOK_SPECS.json at its
    X_REC_MANIFEST.json row (the manifest at the sha `certified()` returns), every main-tree key
    re-hashed in the main tree NOW, X's own scripts held to their x_rec/scripts/ copies.  The
    manifest's own sha is asserted and NOT filed: a later record may lawfully re-record that file
    (L-0.4), and this record is write-once."""
    root, main = Path(root), main_tree(root)
    rows = {f["copy"]: f for f in json.loads(PG.read_certified(X_MANIFEST_REL, root))["files"]}
    raw = (main / X_SPECS_REL).read_bytes()
    if X_SPECS_REL not in rows or sha_bytes(raw) != rows[X_SPECS_REL]["sha256"]:
        halt(f"{X_SPECS_REL} is not the bytes its X_REC_MANIFEST.json row pins")
    pm = json.loads(raw)[X_SPECS_KEY]
    in_tree, own = {}, {}
    for key in sorted(pm):
        if key.startswith(X_OWN_PREFIX):
            copy = X_REC_REL + "/" + key
            held = (copy in rows and rows[copy]["sha256"] == pm[key] and (main / copy).is_file()
                    and sha_bytes((main / copy).read_bytes()) == pm[key])
            own[key] = {"sha256": pm[key], "copy": copy, "equal": held}
        else:
            p = root / key
            got = p.read_bytes() if p.is_file() else None
            in_tree[key] = {"sha256": pm[key], "bytes": None if got is None else len(got),
                            "equal": got is not None and sha_bytes(got) == pm[key]}
    return {"record_path": X_SPECS_REL, "sha256": sha_bytes(raw), "key": X_SPECS_KEY, "n_keys": len(pm),
            "n_main_tree_keys": len(in_tree),
            "all_equal": all(v["equal"] for v in in_tree.values()) and all(v["equal"] for v in own.values()),
            "main_tree": in_tree, "x_own": own, "manifest_path": X_MANIFEST_REL}


def step_q_commit(root=ROOT) -> str:
    """The commit the filed STEP Q record names; the record's bytes held equal to the `_record` entry
    TC12's merged PROGRESS.json carries for it."""
    root = Path(root)
    raw = (root / STEP_Q_REL).read_bytes()
    stages = json.loads((root / PROGRESS_REL).read_text(encoding="utf-8"))["stages"]
    hit = [s for s in stages if s.get("stage") == PG.ORDER[0]]
    if len(hit) != 1 or hit[0]["_record"]["sha256"] != sha_bytes(raw):
        halt(f"{STEP_Q_REL} is not the bytes {PROGRESS_REL} records for {PG.ORDER[0]}")
    return json.loads(raw)["commit"]


def lineage_doc(root=ROOT) -> dict:
    """LINEAGE_PINS.json as the tree derives it now.  HALTS IF the referee is not the referee, a
    root resolves to no file, or a key of X's record differs — a drifted lineage module HALTs the
    build; it is never pinned as it drifted."""
    root = Path(root)
    bad = referee_findings(root)
    if bad:
        halt("the referee is not the referee — " + " | ".join(bad))
    referee = (root / REFEREE_REL).read_bytes()
    roots = walk_roots(referee.decode("utf-8"))
    x = x_path_modules(root)
    if not x["all_equal"]:
        moved = sorted(k for part in (x["main_tree"], x["x_own"]) for k, v in part.items() if not v["equal"])
        halt(f"X's record {X_SPECS_REL}[{X_SPECS_KEY!r}] is not met by {moved} — a drifted lineage module; "
             f"nothing is pinned")
    rows = []
    for name, rel in sorted(lineage_closure(roots, root).items(), key=lambda kv: kv[1]):
        raw = (root / rel).read_bytes()
        rows.append({"name": name, "path": rel, "bytes": len(raw), "sha256": sha_bytes(raw),
                     "held_against": HELD_X if rel in x["main_tree"] else HELD_OWN})
    for r in rows:
        if r["held_against"] == HELD_X and r["sha256"] != x["main_tree"][r["path"]]["sha256"]:
            halt(f"{r['path']} was hashed twice with two results")
    for key, v in x["main_tree"].items():
        v["in_closure"] = any(r["path"] == key for r in rows)
    return {
        "tier": TIER, "record": RECORD,
        "what": "the lineage modules the TC12 shim imports as-is, and every repo file their import statements "
                "can reach, pinned by sha256 before any ride [LEANS L-D.29]",
        "law": "write-once; written by scripts/tierc12_vendor.py --pin-lineage, a plain process that only "
               "hashes files; the shim's post-shim clause P6 re-hashes every estate module it loaded against "
               "`modules`, and each main-tree key of X's record against X's value, at every import; a drifted "
               "module HALTs the build and is never re-pinned silently",
        "walk_law": "the STATIC repo import closure of walk_roots: Import / ImportFrom anywhere (function bodies "
                    "included), constant-string dynamic imports and the repo modules a name-held dynamic import "
                    "can name — the walk of scripts/tierc11_closure_fixtures.py (lineage_walk), mirrored, NOT "
                    "stopping at the TC10 layer and not skipping the range machine: pinning is a superset law",
        "referee": {"path": REFEREE_REL, "bytes": len(referee), "sha256": sha_bytes(referee),
                    "source": SOURCE_REL, "certified_by": {"path": T11_PROGRESS_REL, "stage": SOURCE_STAGE}},
        "walk_roots": roots,
        "modules": {r["path"]: r["sha256"] for r in rows},
        "module_rows": rows,
        "n_modules": len(rows),
        "n_held_against_x": sum(1 for r in rows if r["held_against"] == HELD_X),
        "n_held_by_tc12_alone": sum(1 for r in rows if r["held_against"] == HELD_OWN),
        "x_path_modules": x,
        "step_q_commit": step_q_commit(root),
    }


def pin_lineage(out=ROOT, root=ROOT) -> int:
    """--pin-lineage: env/LINEAGE_PINS.json, write-once."""
    require_depends(root)
    doc = lineage_doc(root)
    x = doc["x_path_modules"]
    print(f"{PINS_REL}: {write_once(Path(out) / PINS_REL, render(doc))} — {doc['n_modules']} modules in the "
          f"static closure of {len(doc['walk_roots'])} roots ({doc['n_held_against_x']} held against X's "
          f"record, {doc['n_held_by_tc12_alone']} by this file alone); X's {x['n_main_tree_keys']} main-tree "
          f"keys all equal: {x['all_equal']}")
    return 0


# ═══════════════════════════════════════════════ 4 · --verify
def verify(root=ROOT) -> int:
    """--verify: the referee, its README and the lineage pins against the tree as it stands.  Writes
    nothing.  Exit 1 on any finding."""
    root = Path(root)
    bad = referee_findings(root)
    s = three_shas(root)
    print(f"the three shas of {SOURCE_REL}: certified {s['certified']} ({SOURCE_STAGE}, {s['certified_bytes']} "
          f"bytes) · live {s['live']} · vendored {s['vendored']} ({s['vendored_bytes']} bytes) · tag "
          f"{referee_tag()!r}")
    copy, readme, pins = root / REFEREE_REL, root / README_REL, root / PINS_REL
    if copy.is_file() and not (readme.is_file() and readme.read_bytes() == readme_bytes(copy.read_bytes())):
        bad.append(f"VENDOR-README {README_REL}: not the rendering of the referee's own bytes")
    if not pins.is_file():
        bad.append(f"LINEAGE-PINS {PINS_REL}: not on file — run --pin-lineage")
    else:
        doc = lineage_doc(root)
        if pins.read_bytes() != render(doc):
            bad.append(f"LINEAGE-PINS {PINS_REL}: the record on file is not what the tree derives now — a "
                       f"drifted lineage module or a rewritten record; it is never re-pinned silently")
        named = [rid for rid, r in PG.records(root).items() if PINS_REL in r.get("artifact_shas", {})]
        if named and sha_bytes(pins.read_bytes()) != PG.certified(PINS_REL, root)["sha256"]:
            bad.append(f"LINEAGE-PINS {PINS_REL}: not the bytes the record {named[len(named) - 1]} certifies")
        print(f"{PINS_REL}: {doc['n_modules']} modules, {len(doc['walk_roots'])} roots, "
              f"{doc['n_held_against_x']} held against X's record, {doc['n_held_by_tc12_alone']} by this file "
              f"alone; certified by {named or 'no record yet'}")
    for x in bad:
        print(f"  FINDING: {x}")
    print("VERIFIED" if not bad else f"{len(bad)} finding(s)")
    return 1 if bad else 0


COMMANDS = {"--vendor": vendor, "--pin-lineage": pin_lineage, "--build-env": build_env, "--verify": verify}
WRITERS = ("--vendor", "--pin-lineage", "--build-env")
OUT_FLAG = "--out="


def main(argv=None) -> int:
    args = sys.argv[1:] if argv is None else list(argv)
    cmds = [a for a in args if a in COMMANDS]
    outs = [a.split("=", 1)[1] for a in args if a.startswith(OUT_FLAG)]
    if len(cmds) != 1 or len(cmds) + len(outs) != len(args) or len(outs) > (1 if cmds[0] in WRITERS else 0):
        halt(f"exactly one of {sorted(COMMANDS)}; {OUT_FLAG}DIR with a subcommand that writes {list(WRITERS)}")
    if cmds[0] not in WRITERS:
        return COMMANDS[cmds[0]]()
    return COMMANDS[cmds[0]](Path(outs[0]).resolve() if outs else ROOT)


if __name__ == "__main__":
    sys.exit(main())
