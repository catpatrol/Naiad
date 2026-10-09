#!/usr/bin/env python
"""TIER-C12 · THE CLOSURE SUITE [LEANS L-0.22, L-0.17, L-0.14, L-0.2; CANON-02, CANON-24, CANON-29].

"decision modules import NOTHING from it — import-closure extends to it" (contract :25-26, :124).
O-29 takes the sentence in its strong form: value-area facts enter every module that builds a book,
a gate, an order or a score ONLY AS FILED DATA.  This suite holds that wall, and the three AST laws
L-0 hosts beside it, on the tierc12 sources a `--stage` names.

  THE GLOB        every scripts/tierc12_*.py whose stem does not end `_fixtures`.
  DOORS_T         tierc12_va, tierc12_va_trades — the only GLOB members that may import
                  analytics.value_area or analytics.profile; each EARNED, each importing tierc12_env first.
  THE READER      tierc12_va_stamps is NOT a door: a DECISION module, data-only.
  DECISION        every other GLOB member, with no exemption; a module this file does not name
                  defaults to DECISION and is scanned.

WHAT IT FILES, one block per leg (CANON-24's row):
  at TC12-REG   F-TYPED · F-SEED · F-FX-MIRROR · F-FX-FORM · F-CLOSURE [ii] · F-CLOSURE [iii]
  from TC12-ENV also F-CLOSURE [i] · F-CLOSURE [i-b] · F-HOOK-ESCAPE · F-WALL (they need the shim)

  F-TYPED        [L-0.17] a computation module holds a numeric literal outside the allow-list (A
                 structural 0 1 2 0.0 1.0 · B the units module · F f-string · G refereed text), a
                 numeric-only expression that does not fold to a structural value (C), a numeric
                 string handed to a number maker (D), a literal default (E); tierc12_units differs
                 from UNITS_T; a process tool's exemption is unearned.
  F-SEED         [L-0.2] a ruler call omits its seed or passes one that does not resolve to the
                 pin-door seed (or E.SEED), an integer draw index or a crc32 call; an X-record seed
                 outside X_SEED_MIRROR_T.
  F-FX-MIRROR    [L-0.14] say / clock / prove / plants / file_transcript of the harness differ by
                 ast.dump from the text of scripts/tierc11_closure_fixtures.py (its sha from the
                 census), or the harness imports outside the stdlib.
  F-FX-FORM      [L-0.14] by AST over every suite in scope: an empty break_if / real_if, a plants
                 row that is not a triple with a non-empty detector, a break leg that is not a
                 plants call, a not_run outside NOT_RUN_FIDS_T, no `--root=`, a default_rng seed
                 off F's form, a network import; and the form of every transcript of record.
  F-CLOSURE [i]  a fresh interpreter importing a decision module holds analytics.value_area,
                 analytics.profile, a door or a forbidden name, or loads the module from elsewhere.
  F-CLOSURE [i-b] the shim's VA_WALL_DOORS / VA_WALL_FIXTURES are not this file's two tuples, or a
                 fresh interpreter of leg (i) does not exit 0 without a BLOCKED:va-wall line.
  F-CLOSURE [ii] AST over each decision source and the static repo closure of its imports: a
                 forbidden import anywhere, a dynamic import, exec / eval / compile, a sys.modules
                 reach, `value_area` / `profile` on the analytics package, a .top / .bottom read;
                 the TC10 layer DISCLOSED and not walked, its function-local range imports ==
                 TC10_LAZY_RANGE_T; and [seam 16] the two L-D detectors — the pin as an int or ISO
                 string, a tick literal or a float `x ± tick` compare — over every non-fixture source.
  F-CLOSURE [iii] DATA-ONLY (no value-area NAME outside the doors) · VA-BLIND (keyed on a
                 directory's one parquet writer, seam 62) · DOOR OUTPUT (earned, env first, no
                 TRADE_COLS_T column, no regbooks/ root, imported only by tierc12_va_fixtures).
  F-HOOK-ESCAPE  E.hook_escapes over every GLOB member finds nothing; subprocess only at the four
                 typed call sites of SUBPROC_SITE_T.
  F-WALL         analytics/value_area.py imports numpy and VA_IMPORTS_T only, no engine, no I/O
                 token; analytics/__init__.py is the census's bytes, holds no value_area token,
                 `_MODULES` lacks it, and analytics_sha() recomputed == INTERFACE.md's.

SCOPE [L-0.11].  `--stage=<ORDER stage>`; the sources in scope are the scripts named by the records
up to that stage in RESUME_ORDER (read from scripts/tierc12_progress.py, the data of record).  At the
stage's own gate its record does not exist yet (gate step 2 precedes step 3): the tierc12 scripts on
disk that NO record names are then the gated record's own and are in scope.  A typed-list member
with no file in scope is printed `not yet filed` — never guessed, never a pass for a present file.
Transcripts of record are those the records BEFORE the stage name (a transcript is of record once a
record names it), so a filed transcript never changes when later records add files.

PLANTS run on scratch COPIES under $TMPDIR (a copy of the in-scope sources with one file bent or a
shadow module added) — never on a source of record — and are judged ONE AT A TIME by the same
detector function the real leg runs, on what the copy ADDS to the findings the tree of record
already holds: a plant is never "caught" by a finding that was there before it.  BANNED: self-comparison; one example where cardinality was
possible; a check whose claim is not the design's claim.  No bar, tape or book is opened: this file
reads source TEXT and JSON records.  The transcript carries no clock, no temp path, no line number
of a GREEN scan, no sha of a tierc12 source.

Run:  export PYTHONDONTWRITEBYTECODE=1
      ~/venvs/naiad/bin/python -B /Users/luis/Naiad/scripts/tierc12_closure_fixtures.py \\
          --stage=<S> [--at=<sha>] [leg-substring ...] [--refile-transcript] [--root=DIR]
`--at` is accepted (the gate hands every enumerating suite the same pair) and read by no leg here.
Exit 0 = every leg GREEN, every break RED · 1 = a RED or VOID leg, a transcript finding, or a HALT.
"""
from __future__ import annotations

import ast
import fractions
import hashlib
import io
import json
import math
import operator
import os
import re
import shutil
import subprocess
import sys
import tempfile
import tokenize
from decimal import Decimal, InvalidOperation
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))
import tierc12_fx as FX                                              # noqa: E402  (the harness)
import tierc12_pins as PINS                                          # noqa: E402  (the contract's door)
import tierc12_progress as PG                                        # noqa: E402  (ORDER, RESUME_ORDER, records)

# ── FIXTURE-TYPED LITERALS: the commission, a second object, never a module's own ──
T12_REL = "research_outputs/tierc12"
T12 = ROOT / T12_REL
OUT = T12 / "closure"
FIRST_STAGE_T = "TC12-REG"                    # CANON-24: ORDER stages from TC12-REG
SHIM_STAGE_T = "TC12-ENV"                     # L-0.22: legs (i), (i-b), (iv), (v) first run here
SUBSTRATE_STAGE_T = "TC12-D"                  # L-0.10 point 11: the pre-substrate header before it
VA_STAGE_T = "TC12-V"                         # L-0.10: the record that files analytics/value_area.py
# L-0.22 point 2 / CANON-02 point 2
DOORS_T = ("tierc12_va", "tierc12_va_trades")
# L-0.22 point 6
VA_MODULE_FIXTURES_T = ("tierc12_va_fixtures",)
# L-0.22 point 3
READER_T = "tierc12_va_stamps"
SHIM_T = "tierc12_env"
# L-0.22 point 5 / CANON-02 point 5
VA_BLIND_T = ("tierc12_books", "tierc12_tide", "tierc12_stage_g", "tierc12_data", "tierc12_env",
              "tierc12_vendor", "tierc12_tables", "tierc12_asof", "tierc12_pins", "tierc12_units",
              "tierc12_tick", "tierc12_registrations", "tierc12_forward_spec", "tierc12_era",
              "tierc12_pct")
TRADE_COLS_T = ("net_r", "gross_r", "fee_r", "funding_r", "entry_px", "stop_px", "exit_reason")
# L-0.22 "FORBIDDEN to every decision module" — by exact name (and each DOORS_T name)
FORBIDDEN_EXACT_T = ("analytics.value_area", "analytics.profile", "analytics.rangefinder_census")
# … and to every member of the glob, doors included — by substring, and by module-name prefix
FORBIDDEN_SUBSTR_T = ("rangefinder", "tierc10_census", "tierc10_stamps", "tierc10_null", "tierc11_nest")
FORBIDDEN_PREFIX_T = ("tc11x_", "tierc11_")
GLOB_EXACT_T = ("analytics.rangefinder_census",)
ANALYTICS_T = "analytics"
WALL_ATTRS_T = ("value_area", "profile")
# L-0.22 leg (iii)
VA_NAMES_T = ("volume_profile", "value_area", "va_series", "va_machine", "va_columns", "va_traverse",
              "va_coincidence", "null_volume")
# L-0.22 leg (ii), THE TC10 CLAUSE: (module, enclosing function) of each function-local range import
TC10_LAZY_RANGE_T = (("tierc10_brk", "grid_toll_atr"), ("tierc10_brk", "macro_signals"),
                     ("tierc10_lanes", "spring_signals_from_census"))
TC10_PREFIX_T = "tierc10_"
LINEAGE_PINS_REL = T12_REL + "/env/LINEAGE_PINS.json"            # seam 14: filed by TC12-ENV.vendor
DYN_FUNCS_T = ("import_module", "__import__")
DYN_DECLARED_T = ((SHIM_T, "tc10_import"),)                       # L-D.26 hunk 7: the env's one door, CLOSED
EXEC_FUNCS_T = ("exec", "eval", "compile")
TOPBOT_T = ("top", "bottom")
TOPBOT_CALLS_T = ("getattr", "hasattr", "setattr", "delattr", "attrgetter")
SYSMOD_CALLS_T = ("get", "pop", "setdefault")
# L-0.22 leg (iv) / CANON-29 point 1: (module, enclosing function, argv heads, the verbs it may pass)
SUBPROC_SITE_T = (
    ("tierc12_data", "clone_snapshot", ("cp",), ("-cpR",)),
    ("tierc12_worktree_attest", "git", ("git",), ("worktree", "rev-parse", "status", "show")),
    ("tierc12_close", "git_ro", ("git",), ("rev-parse", "log", "ls-files", "ls-tree", "cat-file", "show",
                                           "merge-base")),
    ("tierc12_tc11_stamp", "run", ("git", "<the interpreter>"), ("worktree",)),
)
INTERPRETER_T = "<the interpreter>"
GIT_RO_FLAG_T = "--no-optional-locks"
# L-0.22 leg (v)
VA_IMPORTS_T = ("__future__", "dataclasses", "typing", "math", "enum")
VA_THIRD_PARTY_T = ("numpy",)
WALL_BANNED_T = ("read_parquet", "requests", "urllib", "os.environ", "socket")   # tests/test_analytics.py F-AN-4
VA_MODULE_REL = "analytics/value_area.py"
VA_MODULE_NAME_T = "value_area.py"
# L-0.22 leg (i-b) / L-D.26 hunk 7
WALL_LINE_T = "BLOCKED:va-wall"
WALL_EXIT_T = 70
# L-0.17
UNITS_MODULE_T = "tierc12_units"
UNITS_T = {"PCT_PER_UNIT": 100, "BPS_PER_UNIT": 10000, "BYTES_PER_MB": 1000000}
STRUCT_INTS_T = (0, 1, 2)
STRUCT_FLOATS_T = (0.0, 1.0)
PROCESS_TOOLS_T = ("tierc12_fx", "tierc12_progress", "tierc12_worktree_attest", "tierc12_frozen")
RENDERERS_T = ("tierc12_close", "tierc12_close_acts_template")
PROCESS_BANNED_T = (SHIM_T, "numpy", "pandas", ANALYTICS_T)
LINEAGE_RX = re.compile(r"(tierc(?!12_)[0-9]+\w*|engine|tc11x_\w+)")
NUMSTR_FUNCS_T = ("int", "float", "Decimal", "Fraction", "float64", "loads", "literal_eval", "eval")
# rule (G): a module whose text has a committed referee — a statement AST-identical to one of the
# referee's is the referee's (held by L-D's F-VENDOR / F-D-PORT); every other statement is scanned
REFEREES_T = {SHIM_T: (T12_REL + "/vendor/tierc11_env@1526093b.py",),
              "tierc12_data": ("scripts/tierc11_data.py",)}
# L-0.2
RULERS_T = ("cluster_boot", "cluster_boot_diff", "loao_n", "default_rng")
KEYWORD_SEED_RULERS_T = ("cluster_boot", "cluster_boot_diff", "loao_n")
SEED_NAME_T = "seed"
SEED_ATTR_T = "SEED"
PIN_DOOR_T = "tierc12_pins"
SEED_HOLDERS_T = (SHIM_T, PIN_DOOR_T)
DRAW_NAME_T = "draw"
# X_SEED_MIRROR_T: `tierc12_era.compute` and "the F-VA-NULL stream builder" of DOOR 2, whose function
# name no reading gives — its row is typed when DOOR 2 is filed (reported; never guessed)
X_SEED_MIRROR_T = (("tierc12_era", "compute"),)
X_SEED_MIRROR_UNNAMED_T = ("tierc12_va_trades",)
# L-0.14
MIRROR_REFEREE_REL = "scripts/tierc11_closure_fixtures.py"
MIRRORED_T = ("say", "clock", "prove", "plants", "file_transcript")
NOT_RUN_FIDS_T = ("F-MIRROR", "F-TOLL [data d]")
NETWORK_T = ("socket", "ssl", "http", "urllib.request", "requests", "ftplib")
ROOT_FLAG_T = "--root="
PROVE_ARGS_T = ("fid", "title", "break_if", "real_if", "break_leg", "real_leg")
LEG_PARTS_T = ("break_if", "real_if", "break_leg")
BLOCK_RX_T = re.compile(r"F-[A-Z0-9]+(?:-[A-Z0-9]+)*(?: \[[^\[\]]+\])?")
QUAL_SEP_T = " · "
TALLY_RX_T = re.compile(r"  [0-9]+ GREEN, [0-9]+ RED, [0-9]+ NOT RUN")
TALLY_LOOSE_RX = re.compile(r"\s*[0-9]+ GREEN, [0-9]+ RED\b.*")
BREAK_IF_T = "  [BREAK] FAILS IF: "
REAL_IF_T = "  [REAL]  FAILS IF: "
# L-0.19: the contract's name and the FIDs that answer it
CONTRACT_NAME_T = "import-closure"
CONTRACT_FIDS_T = ("F-CLOSURE", "F-HOOK-ESCAPE", "F-WALL", "F-CLOSURE-ENV")
ADDED_FIDS_T = ("F-TYPED", "F-SEED", "F-FX-MIRROR", "F-FX-FORM")
# seam 16: where the three pins are on file before Stage D writes TC12's
RULINGS_REL = T12_REL + "/ORCHESTRATOR_RULINGS.md"
PIN_O7_RX = re.compile(r"\*\*O-7 THE PIN\.\*\*.*?close `([0-9]+)` = \*\*([0-9T:Z-]+)\*\*", re.DOTALL)
TC11_PIN_REL = "research_outputs/tierc11/data/AS_OF_PIN.json"
TC12_PIN_REL = T12_REL + "/data/AS_OF_PIN.json"
SPECS_REL = T12_REL + "/data/CONTRACT_SPECS.json"
STAGE_D_MANIFEST_REL = T12_REL + "/data/STAGE_D_MANIFEST.json"
SNAPSHOT_KEYS_T = ("snapshot_root", "snapshot_name", "snapshot")   # TC11's manifest key first (its port)
# the ORDER stage from whose gate a record file is read (L-0.10's table and SUBSTAGES_T)
FILED_AT_T = {TC12_PIN_REL: SUBSTRATE_STAGE_T, SPECS_REL: SUBSTRATE_STAGE_T,
              LINEAGE_PINS_REL: SHIM_STAGE_T, VA_MODULE_REL: VA_STAGE_T}
TICK_WORD_T = "tick"
CENSUS_DIR_REL = T12_REL + "/frozen"
CENSUS_STEM_T = "FROZEN_ESTATE"
SCRIPT_RX = re.compile(r"scripts/(tierc12_\w+)\.py")
TRANSCRIPT_RX = re.compile(re.escape(T12_REL) + r"/(?:[^/]+/)*FIXTURES_[^/]*\.txt")
MANIFEST_NAME_T = "build_manifest.json"
NOT_OWN_T = ("/_det_", "/x_rec/")              # twins and X's byte copies are no TC12 directory of record
READ_SET_GLOB_T = "READ_SET*.json"
VA_DIR_REL = T12_REL + "/va/"
DOOR_TABLE_RX = re.compile(re.escape(T12_REL) + r"/va/(?:trades/)?[^/]+\.parquet")
REGBOOKS_T = "regbooks"
MOD_RX = re.compile(r"[A-Za-z_][A-Za-z0-9_]*(\.[A-Za-z_][A-Za-z0-9_]*)*")
PROBE_MARK = "@@PROBE "
ESC_MARK = "@@ESC "
SHADOW = "tierc12_zz_shadow"
SHADOW_SUITE = "tierc12_zz_fixtures"

CTX: dict = {}                                 # the run: stage, scope, the tree of record, scratch


# ═══════════════════════════════════════════════════════════════ THE SCOPE [L-0.11]
def halt(msg: str):
    raise SystemExit(f"HALT: {msg}")


def stage_at_least(stage: str, floor: str) -> bool:
    return PG.ORDER.index(stage) >= PG.ORDER.index(floor)


def build_scope(stage: str) -> dict:
    """The paths a run at `stage` reads, from the records on file — never from a typed list."""
    order = list(PG.RESUME_ORDER)
    upto = order[:order.index(stage) + 1]
    recs = PG.records(ROOT)
    named_all = {p for r in recs.values() for p in r.get("artifact_shas", {})}
    named = {p for rid in upto if rid in recs for p in recs[rid].get("artifact_shas", {})}
    gated = stage not in recs                  # the record being gated does not exist yet
    on_disk = sorted(FX.rel(p, ROOT) for p in SCRIPTS.glob("tierc12_*.py"))
    paths = set(named)
    if gated:
        paths |= {p for p in on_disk if p not in named_all}
        paths |= {FX.rel(p, ROOT) for pat in ("**/" + MANIFEST_NAME_T, "va/*.parquet", "va/trades/*.parquet")
                  for p in T12.glob(pat) if not any(x in FX.rel(p, ROOT) for x in NOT_OWN_T)
                  and FX.rel(p, ROOT) not in named_all}
    scripts = sorted(m.group(1) for m in map(SCRIPT_RX.fullmatch, sorted(paths)) if m)
    missing = sorted(n for n in scripts if not (SCRIPTS / f"{n}.py").is_file())
    before = [rid for rid in upto if rid != stage and rid in recs]
    transcripts = sorted({t for rid in before for t in
                          [f.get("transcript", "") for f in recs[rid].get("fixtures", [])]
                          + list(recs[rid].get("artifact_shas", {})) if TRANSCRIPT_RX.fullmatch(t)})
    latest = not gated and not any(rid in recs for rid in order[order.index(stage) + 1:])
    unrecorded = [p for p in on_disk if p not in named_all] if latest else []
    return {"stage": stage, "upto": upto, "paths": paths, "names": [n for n in scripts if n not in missing],
            "missing": missing, "transcripts": transcripts, "unrecorded": unrecorded}


def filed_by_now(rel: str) -> bool:
    """A record file whose filing STAGE is typed (FILED_AT_T): read from that stage's gate on —
    by stage, not by what happens to be on disk, so a transcript never moves when a later record
    files it."""
    return stage_at_least(CTX["stage"], FILED_AT_T[rel]) and (ROOT / rel).is_file()


class Tree:
    """The tierc12 sources ONE scan reads: {module: text}, read from one scripts directory."""

    def __init__(self, directory, names):
        self.dir = Path(directory)
        self.names = tuple(sorted(names))
        self.src = {n: (self.dir / f"{n}.py").read_text(encoding="utf-8") for n in self.names}
        self._ast: dict = {}

    @property
    def glob(self) -> list:
        return [n for n in self.names if not n.endswith("_fixtures")]

    @property
    def suites(self) -> list:
        return [n for n in self.names if n.endswith("_fixtures")]

    @property
    def decision(self) -> list:
        return [n for n in self.glob if n not in DOORS_T]

    def ast(self, name: str) -> ast.Module:
        if name not in self._ast:
            self._ast[name] = ast.parse(self.src[name])
        return self._ast[name]


def plant(over: dict, drop=()) -> Tree:
    """A scratch COPY under $TMPDIR of the in-scope sources, with `over` = {module: text} replaced
    or added (a shadow module) and `drop` left out.  No source of record moves."""
    base = CTX["tree"]
    d = Path(tempfile.mkdtemp(prefix="plant_", dir=CTX["scratch"]))
    names = [n for n in base.names if n not in drop and n not in over]
    for n in names:
        (d / f"{n}.py").write_text(base.src[n], encoding="utf-8")
    for n, text in over.items():
        (d / f"{n}.py").write_text(text, encoding="utf-8")
    return Tree(d, set(names) | set(over))


def scratch_text(name: str, text: str) -> str:
    """A scratch COPY of one text (a transcript, a referee), written under $TMPDIR and read back."""
    d = Path(tempfile.mkdtemp(prefix="text_", dir=CTX["scratch"]))
    (d / name).write_text(text, encoding="utf-8")
    return (d / name).read_text(encoding="utf-8")


def mut(text: str, old: str, new: str) -> str:
    if text.count(old) != 1:
        raise RuntimeError(f"the plant's anchor occurs {text.count(old)} time(s), not once")
    return text.replace(old, new)


def filed(names, tree: Tree) -> str:
    """`a on file · b not yet filed` for the members of a typed list."""
    return " · ".join(f"{n} {'on file' if n in tree.names else 'not yet filed'}" for n in names)


_LINE_RX = re.compile(r"\bline [0-9]+")


def added(fn, tree, *args, **kw) -> list:
    """What a planted copy ADDS to the findings the tree of record already holds under the same
    detector function (line numbers aside) — a plant is never 'caught' by a finding that was
    there before it."""
    if fn.__name__ not in CTX["base"]:
        CTX["base"][fn.__name__] = {_LINE_RX.sub("line #", x) for x in fn(CTX["tree"])}
    return [x for x in fn(tree, *args, **kw) if _LINE_RX.sub("line #", x) not in CTX["base"][fn.__name__]]


SHADOW_TEXT = ('"""a shadow module (planted under $TMPDIR; never a source of record)."""\n'
               "from __future__ import annotations\n\n\ndef f(x):\n    return x\n")
DOOR_SHADOW_TEXT = ('"""a shadow door (planted under $TMPDIR; never a source of record)."""\n'
                    "from __future__ import annotations\n\nimport sys\n\nimport tierc12_env as E\n"
                    "from analytics import value_area as VA\n\nOUT = E.OUT / \"va\"\n")


# ═══════════════════════════════════════════════════════════════ AST HELPERS (this file's own walk)
def _fn(call: ast.Call) -> str:
    f = call.func
    return f.attr if isinstance(f, ast.Attribute) else getattr(f, "id", "")


def _cstr(node):
    return node.value if isinstance(node, ast.Constant) and isinstance(node.value, str) else None


def _root(node):
    """The leftmost Name of an attribute / call / subscript chain, or None."""
    while isinstance(node, (ast.Attribute, ast.Call, ast.Subscript)):
        node = node.func if isinstance(node, ast.Call) else node.value
    return node.id if isinstance(node, ast.Name) else None


def _parents(tree) -> dict:
    return {c: p for p in ast.walk(tree) for c in ast.iter_child_nodes(p)}


def _functions(parents: dict, node) -> list:
    """The function nodes enclosing `node`, innermost first."""
    out = []
    while node in parents:
        node = parents[node]
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
            out.append(node)
    return out


def _where(parents: dict, node) -> str:
    return next((f.name for f in _functions(parents, node) if not isinstance(f, ast.Lambda)), "<module>")


def imports_of(tree) -> list:
    """Every module name a source imports by statement, ANYWHERE (function bodies included); a
    from-import also as module.name."""
    out = []
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            out += [(n.lineno, a.name) for a in n.names]
        elif isinstance(n, ast.ImportFrom):
            mod = n.module or ""
            out += [(n.lineno, mod)] if mod else []
            out += [(n.lineno, f"{mod}.{a.name}" if mod else a.name) for a in n.names]
    return out


def dyn_sites(tree) -> list:
    """Every import_module / __import__ call: (line, callee, enclosing function, the constant
    module name or None, the repo modules a non-constant name can be)."""
    parents = _parents(tree)
    lits = {t.id: n.value for n in tree.body if isinstance(n, ast.Assign)
            for t in n.targets if isinstance(t, ast.Name)}
    out = []
    for n in ast.walk(tree):
        if not (isinstance(n, ast.Call) and _fn(n) in DYN_FUNCS_T):
            continue
        const = _cstr(n.args[0]) if n.args else None
        targets = []
        if const is None:
            encl = [f for f in _functions(parents, n) if not isinstance(f, ast.Lambda)]
            scope = encl[0] if encl else tree
            strings = {c.value for c in ast.walk(scope) if _cstr(c) is not None}
            for nm in ast.walk(scope):
                if isinstance(nm, ast.Name) and nm.id in lits:
                    strings |= {c.value for c in ast.walk(lits[nm.id]) if _cstr(c) is not None}
            targets = sorted(s for s in strings if repo_file(s) is not None)
        out.append((n.lineno, _fn(n), _where(parents, n), const, targets))
    return out


def imported_names(tree) -> list:
    """imports_of plus the constant-string dynamic imports."""
    return imports_of(tree) + [(ln, c) for ln, _, _, c, _ in dyn_sites(tree) if c is not None]


def aliases(tree) -> dict:
    """{bound name: the module it came from} for every import statement of a source."""
    out = {}
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            for a in n.names:
                out[a.asname or a.name.split(".")[0]] = a.name if a.asname else a.name.split(".")[0]
        elif isinstance(n, ast.ImportFrom) and n.module:
            for a in n.names:
                out[a.asname or a.name] = f"{n.module}.{a.name}"
    return out


def repo_file(name: str):
    """The repo file a module name resolves to (scripts/ first, then the repo root), or None."""
    if not MOD_RX.fullmatch(name or ""):
        return None
    rel = name.replace(".", "/")
    for base in (SCRIPTS, ROOT):
        for p in (base / f"{rel}.py", base / rel / "__init__.py"):
            if p.is_file():
                return p
    return None


def repo_candidates(x: str) -> list:
    """The repo modules an import of `x` executes: the longest dotted prefix that resolves to a
    repo file, and each parent package of it that does."""
    parts = x.split(".")
    for k in range(len(parts), 0, -1):
        if repo_file(".".join(parts[:k])) is not None:
            return [".".join(parts[:j]) for j in range(1, k + 1)
                    if repo_file(".".join(parts[:j])) is not None]
    return []


def forbidden_rule(name: str, role: str):
    """Why `name` may not be imported by a module of `role` (decision | door | lineage), or None."""
    for s in FORBIDDEN_SUBSTR_T:
        if s in name:
            return f"the range-machine substring {s!r}"
    for p in FORBIDDEN_PREFIX_T:
        if name.split(".")[0].startswith(p):
            return f"a module named {p}* (O-3, O-4)"
    exact = GLOB_EXACT_T if role == "door" else FORBIDDEN_EXACT_T + DOORS_T
    for e in exact:
        if name == e or name.startswith(e + "."):
            return f"the forbidden name {e}"
    return None


# ═══════════════════════════════════════════════════════════════ F-TYPED [L-0.17]
_FOLD = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv,
         ast.FloorDiv: operator.floordiv, ast.Mod: operator.mod, ast.Pow: operator.pow,
         ast.LShift: operator.lshift, ast.RShift: operator.rshift, ast.BitOr: operator.or_,
         ast.BitAnd: operator.and_, ast.BitXor: operator.xor}
_UNARY = {ast.USub: operator.neg, ast.UAdd: operator.pos, ast.Invert: operator.invert}


def _is_num(n) -> bool:
    return isinstance(n, ast.Constant) and type(n.value) in (int, float, complex)


def _num_only(n) -> bool:
    if _is_num(n):
        return True
    if isinstance(n, ast.UnaryOp) and type(n.op) in _UNARY:
        return _num_only(n.operand)
    if isinstance(n, ast.BinOp) and type(n.op) in _FOLD:
        return _num_only(n.left) and _num_only(n.right)
    return False


def _fold(n):
    if isinstance(n, ast.Constant):
        return n.value
    if isinstance(n, ast.UnaryOp):
        return _UNARY[type(n.op)](_fold(n.operand))
    return _FOLD[type(n.op)](_fold(n.left), _fold(n.right))


def _structural(v) -> bool:
    return (type(v) is int and v in STRUCT_INTS_T) or (type(v) is float and v in STRUCT_FLOATS_T)


def _holds_number(v) -> bool:
    if isinstance(v, dict):
        return any(_holds_number(x) for x in list(v) + list(v.values()))
    if isinstance(v, (list, tuple, set)):
        return any(_holds_number(x) for x in v)
    return type(v) in (int, float, complex)


def _numeric_string(s: str, fn: str) -> bool:
    if fn in ("loads", "literal_eval", "eval"):
        try:
            return _holds_number(json.loads(s) if fn == "loads" else ast.literal_eval(s))
        except (ValueError, SyntaxError):
            return False
    try:
        fractions.Fraction(s)
        return True
    except (ValueError, ZeroDivisionError):
        pass
    try:
        return math.isfinite(float(s))
    except ValueError:
        return False


def _dumps(text: str) -> frozenset:
    return frozenset(ast.dump(s) for s in ast.walk(ast.parse(text)) if isinstance(s, ast.stmt))


def numeric_findings(name: str, src: str, refereed=frozenset()) -> list:
    """Rules (A), (C), (D), (E), (F), (G) on one computation source."""
    tree = ast.parse(src)
    skip: set = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.JoinedStr) or (refereed and isinstance(n, ast.stmt) and ast.dump(n) in refereed):
            skip.update(id(x) for x in ast.walk(n))
    out, done = [], set()
    for n in ast.walk(tree):
        if id(n) in skip or id(n) in done:
            continue
        if isinstance(n, (ast.BinOp, ast.UnaryOp)) and _num_only(n):
            done.update(id(x) for x in ast.walk(n))
            bad = [c.value for c in ast.walk(n) if _is_num(c) and not _structural(c.value)]
            if bad:
                out.append(f"TYPED-LITERAL {name} line {n.lineno}: `{ast.unparse(n)}` types {bad} — not a "
                           f"structural literal [L-0.17 A]")
                continue
            try:
                v = _fold(n)
            except (ArithmeticError, TypeError, ValueError) as e:
                v = f"<{type(e).__name__}>"
            if not _structural(v):
                out.append(f"TYPED-FOLD {name} line {n.lineno}: `{ast.unparse(n)}` is built only from numeric "
                           f"literals and folds to {v!r}, not a structural value [L-0.17 C]")
        elif _is_num(n):
            if type(n.value) is complex:
                out.append(f"TYPED-LITERAL {name} line {n.lineno}: the complex literal {n.value!r} [L-0.17]")
            elif not _structural(n.value):
                out.append(f"TYPED-LITERAL {name} line {n.lineno}: the numeric literal {n.value!r} is neither "
                           f"structural nor read through a door [L-0.17 A, E]")
        elif isinstance(n, ast.Call) and _fn(n) in NUMSTR_FUNCS_T and n.args \
                and _cstr(n.args[0]) is not None and _numeric_string(n.args[0].value, _fn(n)):
            out.append(f"TYPED-NUMSTR {name} line {n.lineno}: {_fn(n)}({n.args[0].value!r}) — a numeric string "
                       f"handed to a number maker [L-0.17 D]")
    return out


def units_findings(src: str) -> list:
    """Rule (B): the units module holds exactly `NAME = <number>` rows and its map == UNITS_T."""
    out, got = [], {}
    for n in ast.parse(src).body:
        ok = (isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name)
              and _is_num(n.value) and n.targets[0].id not in got)
        if ok:
            got[n.targets[0].id] = n.value.value
        else:
            out.append(f"TYPED-UNITS {UNITS_MODULE_T} line {n.lineno}: holds something other than one "
                       f"`NAME = <number>` row per name ({type(n).__name__})")
    if {k: (type(v), v) for k, v in got.items()} != {k: (type(v), v) for k, v in UNITS_T.items()}:
        out.append(f"TYPED-UNITS {UNITS_MODULE_T}: its name -> value map {got} != UNITS_T {UNITS_T}")
    return out


def unearned_findings(name: str, src: str) -> list:
    """A process tool's exemption is EARNED: it imports none of tierc12_env, numpy, pandas, the
    lineage or analytics, so it cannot compute on a bar by itself."""
    bad = sorted({x for _, x in imported_names(ast.parse(src))
                  if x.split(".")[0] in PROCESS_BANNED_T or LINEAGE_RX.fullmatch(x.split(".")[0])})
    return [f"TYPED-UNEARNED {name}: a process tool imports {bad} — its exemption from the literal scan is "
            f"not earned [L-0.17]"] if bad else []


def referee_dumps(name: str) -> frozenset:
    out: set = set()
    for rel in REFEREES_T.get(name, ()):
        if (ROOT / rel).is_file():
            out |= _dumps((ROOT / rel).read_text(encoding="utf-8"))
    return frozenset(out)


def computation(tree: Tree) -> list:
    return [n for n in tree.glob if n not in PROCESS_TOOLS_T + RENDERERS_T and n != UNITS_MODULE_T]


def typed_findings(tree: Tree, va_text=None) -> list:
    out = []
    for n in computation(tree):
        out += numeric_findings(n, tree.src[n], referee_dumps(n))
    if va_text is not None:
        out += numeric_findings(VA_MODULE_REL, va_text)
    if UNITS_MODULE_T in tree.names:
        out += units_findings(tree.src[UNITS_MODULE_T])
    for n in PROCESS_TOOLS_T:
        if n in tree.names:
            out += unearned_findings(n, tree.src[n])
    return out


def va_text():
    return (ROOT / VA_MODULE_REL).read_text(encoding="utf-8") if filed_by_now(VA_MODULE_REL) else None


def typed_break():
    tree = CTX["tree"]
    rows = [
        ("`K = 0.25` typed in a copy of a computation module", "TYPED-LITERAL",
         lambda: added(typed_findings, plant({SHADOW: SHADOW_TEXT + "K = 0.25\n"}))),
        ('`float("1.5")` in a copy', "TYPED-NUMSTR",
         lambda: added(typed_findings, plant({SHADOW: SHADOW_TEXT + 'K = float("1.5")\n'}))),
        ("`K = 2 + 1` in a copy", "TYPED-FOLD",
         lambda: added(typed_findings, plant({SHADOW: SHADOW_TEXT + "K = 2 + 1\n"}))),
        ("a default `def g(n=8)` in a copy", "TYPED-LITERAL",
         lambda: added(typed_findings, plant({SHADOW: SHADOW_TEXT + "\n\ndef g(n=8):\n    return n\n"}))),
        ("an extra row in a tierc12_units copy", "TYPED-UNITS",
         lambda: added(typed_findings, plant({UNITS_MODULE_T: tree.src[UNITS_MODULE_T]
                                               + "HOURS_PER_DAY = 24\n"}))),
        ("`import numpy` added to a copy of the process tool tierc12_progress", "TYPED-UNEARNED",
         lambda: added(typed_findings, plant({"tierc12_progress": tree.src["tierc12_progress"]
                                               + "\nimport numpy\n"}))),
    ]
    if SHIM_T in tree.names:
        rows.append(("a literal typed inside a hunk of the vendored shim copy", "TYPED-LITERAL",
                     lambda: added(typed_findings, plant({SHIM_T: tree.src[SHIM_T]
                                                          + "\nHUNK_PLANT = 0.25\n"}))))
    return FX.plants(rows)


def typed_real():
    tree = CTX["tree"]
    f = typed_findings(tree, va_text())
    tools = " · ".join(f"{n} {'EARNED' if n in tree.names else 'not yet filed'}" for n in PROCESS_TOOLS_T)
    return (not f), (
        f"computation modules scanned for numeric literals: {computation(tree) or 'none in scope'}; "
        f"{UNITS_MODULE_T} == UNITS_T (three rows and nothing else); process tools (exempt, the exemption "
        f"proven by AST — none imports {list(PROCESS_BANNED_T)} or the lineage): {tools}; renderers (held on "
        f"their OUTPUT by L-X's digit trace): {filed(RENDERERS_T, tree)}; {VA_MODULE_REL} "
        f"{'scanned' if va_text() is not None else 'not yet filed'}"
        + (f" — {len(f)} finding(s): " + " | ".join(f) if f else ""))


# ═══════════════════════════════════════════════════════════════ F-SEED [L-0.2]
def seed_wrappers(trees: dict) -> dict:
    """Every TC12 wrapper of a ruler: a function taking `seed` whose body calls a ruler or another
    wrapper -> the positional index of its `seed` parameter (None: keyword-only)."""
    funcs = [f for t in trees.values() for f in ast.walk(t)
             if isinstance(f, (ast.FunctionDef, ast.AsyncFunctionDef))]
    wrap: dict = {}
    grew = True
    while grew:
        grew = False
        for f in funcs:
            pos = [a.arg for a in f.args.posonlyargs + f.args.args]
            if f.name in wrap or SEED_NAME_T not in pos + [a.arg for a in f.args.kwonlyargs]:
                continue
            if {_fn(c) for c in ast.walk(f) if isinstance(c, ast.Call)} & (set(RULERS_T) | set(wrap)):
                own = 1 if pos and pos[0] in ("self", "cls") else 0
                wrap[f.name] = pos.index(SEED_NAME_T) - own if SEED_NAME_T in pos else None
                grew = True
    return wrap


def _seed_arg(call: ast.Call, wrappers: dict):
    for k in call.keywords:
        if k.arg == SEED_NAME_T:
            return k.value
    name = _fn(call)
    if any(isinstance(a, ast.Starred) for a in call.args) or name in KEYWORD_SEED_RULERS_T:
        return None
    i = 0 if name == "default_rng" else wrappers.get(name)
    return call.args[i] if i is not None and len(call.args) > i else None


class _SeedScope:
    """What a seed expression at one call site may name."""

    def __init__(self, module: str, tree, parents: dict, call):
        fns = _functions(parents, call)
        self.module, self.where = module, _where(parents, call)
        self.alias = aliases(tree)
        self.params = {a.arg for f in fns for a in f.args.posonlyargs + f.args.args + f.args.kwonlyargs}
        inner = fns[0] if fns else tree
        self.loops = set()
        for n in ast.walk(inner):
            target = n.target if isinstance(n, (ast.For, ast.comprehension)) else None
            self.loops |= {x.id for x in ast.walk(target) if isinstance(x, ast.Name)} if target else set()
        self.local, self.glob = {}, {}
        for held, body in ((self.local, ast.walk(inner) if fns else ()), (self.glob, tree.body)):
            for n in body:
                if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name):
                    held.setdefault(n.targets[0].id, []).append(n.value)

    def origin(self, node) -> str:
        """The module the leftmost name of an expression was imported from ('' if none)."""
        return (self.alias.get(_root(node)) or "").split(".")[0]

    def pin_door(self, node, seen=frozenset()) -> bool:
        """A read THROUGH the pin door: a call on its alias, or a name bound to one."""
        if isinstance(node, ast.Name) and self.values(node.id) and node.id not in seen:
            return any(self.pin_door(v, seen | {node.id}) for v in self.values(node.id))
        return self.origin(node) == PIN_DOOR_T and any(isinstance(c, ast.Call) for c in ast.walk(node))

    def values(self, name: str):
        return self.local.get(name) or self.glob.get(name)


def seed_leaves(e, s: _SeedScope, seen=frozenset()) -> list:
    """Why a seed expression does not RESOLVE ([] = it does): every leaf must be the pin-door seed
    (or E.SEED), an integer draw index, or a crc32 call."""
    if isinstance(e, (ast.List, ast.Tuple)):
        return [x for elt in e.elts for x in seed_leaves(elt, s, seen)]
    if isinstance(e, ast.BinOp):
        return seed_leaves(e.left, s, seen) + seed_leaves(e.right, s, seen)
    if isinstance(e, ast.Constant):
        return [f"SEED-UNRESOLVED a literal seed {e.value!r}"]
    key = None
    if isinstance(e, ast.Subscript) and _cstr(e.slice) is not None:
        key = e.value
    elif isinstance(e, ast.Call) and _fn(e) == "get" and e.args and _cstr(e.args[0]) is not None:
        key = e.func.value
    if key is not None:                        # a seed read BY KEY from a record
        if s.pin_door(key) or (s.module, s.where) in X_SEED_MIRROR_T:
            return []
        return [f"SEED-X-OUTSIDE-MIRROR a seed read by key from a record (`{ast.unparse(e)}`) in "
                f"{s.module}.{s.where}, outside X_SEED_MIRROR_T — elsewhere only the pin door or E.SEED supplies it"]
    if isinstance(e, ast.Call):
        if _fn(e) == "crc32" or (s.origin(e) == PIN_DOOR_T and any(_cstr(a) == SEED_NAME_T for a in e.args)):
            return []
        if _fn(e) in ("int", "stream_seed") and e.args:
            return seed_leaves(e.args[0], s, seen)
        return [f"SEED-UNRESOLVED the call `{ast.unparse(e)}`"]
    if isinstance(e, ast.Attribute):                # `E.SEED` exactly, on the shim's (or the pin door's) alias
        exact = e.attr == SEED_ATTR_T and isinstance(e.value, ast.Name) and s.origin(e) in SEED_HOLDERS_T
        return [] if exact else [f"SEED-UNRESOLVED `{ast.unparse(e)}` is not the pin-door seed or E.SEED"]
    if isinstance(e, ast.Name):
        if e.id in s.params:
            return [] if e.id in (SEED_NAME_T, DRAW_NAME_T) else \
                [f"SEED-UNRESOLVED the parameter `{e.id}` is neither `seed` nor `draw`"]
        if e.id in s.loops:
            return []
        if e.id in seen:
            return [f"SEED-UNRESOLVED `{e.id}` is bound to itself"]
        if s.values(e.id):
            return [x for v in s.values(e.id) for x in seed_leaves(v, s, seen | {e.id})]
        if s.alias.get(e.id) in tuple(f"{m}.{SEED_ATTR_T}" for m in SEED_HOLDERS_T):
            return []
        return [f"SEED-UNRESOLVED the name `{e.id}`"]
    return [f"SEED-UNRESOLVED the expression `{ast.unparse(e)}`"]


def seed_findings(tree: Tree) -> list:
    trees = {n: tree.ast(n) for n in tree.glob}
    wrappers = seed_wrappers(trees)
    out = []
    for name, t in trees.items():
        parents = _parents(t)
        for c in ast.walk(t):
            if not (isinstance(c, ast.Call) and _fn(c) in set(RULERS_T) | set(wrappers)):
                continue
            arg = _seed_arg(c, wrappers)
            if arg is None:
                out.append(f"SEED-OMITTED {name} line {c.lineno}: {_fn(c)}(…) in {_where(parents, c)}() passes "
                           f"no explicit seed [L-0.2]")
                continue
            out += [f"{x} — {name} line {c.lineno}, the seed of {_fn(c)}(…)"
                    for x in seed_leaves(arg, _SeedScope(name, t, parents, c))]
    return out


SCORER_SHADOW = (SHADOW_TEXT + "import zlib\n\nimport tierc12_pins as PINS\n\n\n"
                 "def cluster_boot(values, clusters, seed, n_boot):\n    return values\n\n\n")
SEED_CONTROL = (SCORER_SHADOW +
                "def streams(np, seed, tag, n):\n"
                "    one = np.random.default_rng([seed, zlib.crc32(tag)])\n"
                "    many = [np.random.default_rng([seed + draw, zlib.crc32(tag)]) for draw in range(n)]\n"
                "    return one, many\n\n\n"
                "def ruler(x, c):\n    return cluster_boot(x, c, seed=PINS.pin(\"seed\"), n_boot=len(x))\n\n\n"
                f"def ruler_e(x, c):\n    import {SHIM_T} as E\n"
                "    return cluster_boot(x, c, seed=E.SEED, n_boot=len(x))\n")


def seed_break():
    literal = f"def bad(x, c):\n    return cluster_boot(x, c, seed={CTX['seed']}, n_boot=len(x))\n"
    return FX.plants([
        ("a `cluster_boot(x, c)` call with no `seed=` in a shadow scorer", "SEED-OMITTED",
         lambda: added(seed_findings, plant({SHADOW: SCORER_SHADOW
                                      + "def bad(x, c):\n    return cluster_boot(x, c)\n"}))),
        ("a literal seed in the same call", "SEED-UNRESOLVED",
         lambda: added(seed_findings, plant({SHADOW: SCORER_SHADOW + literal}))),
        ("a seed read from an X record in a function outside X_SEED_MIRROR_T", "SEED-X-OUTSIDE-MIRROR",
         lambda: added(seed_findings, plant({SHADOW: SCORER_SHADOW + "def bad(x, c, rec):\n"
                                      "    return cluster_boot(x, c, seed=rec[\"seed\"], n_boot=len(x))\n"}))),
        ("`seed=E.SEED_SENS` — a seed that is neither the pin-door seed nor E.SEED", "SEED-UNRESOLVED",
         lambda: added(seed_findings, plant({SHADOW: SCORER_SHADOW + f"import {SHIM_T} as E\n\n\ndef bad(x, c):\n"
                                             "    return cluster_boot(x, c, seed=E.SEED_SENS, n_boot=len(x))\n"}))),
        ("a seed passed positionally to a lineage ruler (not `seed=`)", "SEED-OMITTED",
         lambda: added(seed_findings, plant({SHADOW: SCORER_SHADOW + "def bad(x, c, seed):\n"
                                      "    return cluster_boot(x, c, seed, len(x))\n"}))),
    ])


def seed_real():
    tree = CTX["tree"]
    f = seed_findings(tree)
    control = added(seed_findings, plant({SHADOW: SEED_CONTROL}))
    wrappers = sorted(seed_wrappers({n: tree.ast(n) for n in tree.glob}))
    mirror = " · ".join(f"{m}.{fn} ({'on file' if m in tree.names else 'not yet filed'})"
                        for m, fn in X_SEED_MIRROR_T)
    unnamed = " · ".join(f"{m} ({'ON FILE — its stream builder must be typed' if m in tree.names else 'not yet filed'})"
                         for m in X_SEED_MIRROR_UNNAMED_T)
    ok = not f and not control and not any(m in tree.names for m in X_SEED_MIRROR_UNNAMED_T)
    return ok, (
        f"every call of {list(RULERS_T)} and of the TC12 wrappers found by AST ({wrappers or 'none'}) in "
        f"{len(tree.glob)} non-fixture source(s) passes a seed that resolves; X_SEED_MIRROR_T: {mirror}; DOOR 2's "
        f"F-VA-NULL stream builder — function name not given by a reading: {unnamed}; control GREEN, printed: a "
        f"list seed `[seed, crc32(tag)]`, a list seed `[seed + draw, crc32(tag)]` with `draw` an integer loop "
        f"index, `seed=PINS.pin(\"seed\")` and `seed=E.SEED` -> {len(control)} finding(s)"
        + (f" — {len(f)} finding(s): " + " | ".join(f + control) if f or control else ""))


# ═══════════════════════════════════════════════════════════════ F-FX-MIRROR [L-0.14]
def census_file():
    """The census the verdict reads: FROZEN_ESTATE_<n>.json with the highest n, else the first."""
    d = ROOT / CENSUS_DIR_REL
    numbered = {int(p.stem.rsplit("_", 1).pop()): p for p in d.glob(f"{CENSUS_STEM_T}_*.json")
                if p.stem.rsplit("_", 1).pop().isdigit()} if d.is_dir() else {}
    first = d / f"{CENSUS_STEM_T}.json"
    return numbered[max(numbered)] if numbered else (first if first.is_file() else None)


def census_sha(rel: str):
    p = census_file()
    if p is None:
        return None
    return json.loads(p.read_text(encoding="utf-8")).get("files", {}).get(rel, {}).get("sha256")


def mirror_findings(head: str, ref_bytes: bytes, ref_sha) -> list:
    out, ref = [], ref_bytes.decode("utf-8")
    if ref_sha is None:
        out.append(f"FX-REFEREE-SHA: no census entry for {MIRROR_REFEREE_REL} under {CENSUS_DIR_REL}/ — the "
                   f"referee's text cannot be asserted")
    elif FX.sha_bytes(ref_bytes) != ref_sha:
        out.append(f"FX-REFEREE-SHA: the text of {MIRROR_REFEREE_REL} does not hash to its census sha")
    for n in MIRRORED_T:
        try:
            same = FX.func_dump(head, n) == FX.func_dump(ref, n)
        except KeyError as e:
            out.append(f"FX-MIRROR {n}: {e}")
            continue
        if not same:
            out.append(f"FX-MIRROR {n}: ast.dump differs from the referee's")
    for _, m in imported_names(ast.parse(head)):
        if m.split(".")[0] not in sys.stdlib_module_names:
            out.append(f"FX-STDLIB: the harness imports {m}, outside the stdlib")
    return out


def _mirror_inputs():
    return (CTX["tree"].src["tierc12_fx"], (ROOT / MIRROR_REFEREE_REL).read_bytes(),
            census_sha(MIRROR_REFEREE_REL))


def mirror_break():
    head, ref, sha = _mirror_inputs()
    crash = ("            crashed.append(f\"{name} -> RAISED {type(e).__name__}: {e}\")\n"
             "            continue\n")
    return FX.plants([
        ("`plants` in a harness copy changed to count a crash as a catch", "FX-MIRROR plants",
         lambda: mirror_findings(scratch_text("fx.py", mut(head, crash, "            found = [want]\n")),
                                 ref, sha)),
        ("`import pandas` added to a harness copy", "FX-STDLIB",
         lambda: mirror_findings(scratch_text("fx.py", mut(head, "import zlib\n", "import zlib\nimport pandas\n")),
                                 ref, sha)),
        ("a referee text copy with one statement appended", "FX-REFEREE-SHA",
         lambda: [x for x in mirror_findings(head, scratch_text(
             "ref.py", ref.decode("utf-8") + "\nPLANT = None\n").encode("utf-8"), sha)
                  if x not in mirror_findings(head, ref, sha)]),
    ])


def mirror_real():
    head, ref, sha = _mirror_inputs()
    f = mirror_findings(head, ref, sha)
    return (not f), (f"the {len(MIRRORED_T)} mirrored functions {list(MIRRORED_T)} of scripts/tierc12_fx.py are "
                     f"AST-identical to the same functions parsed from the TEXT of {MIRROR_REFEREE_REL}, whose "
                     f"sha is the census's ({CENSUS_DIR_REL}/); every import of the harness is stdlib"
                     + (f" — {len(f)} finding(s): " + " | ".join(f) if f else ""))


# ═══════════════════════════════════════════════════════════════ F-FX-FORM [L-0.14]
def _defs(tree) -> dict:
    out = {n.name: n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}
    for n in tree.body:
        if isinstance(n, ast.Assign) and isinstance(n.value, ast.Lambda):
            out.update({t.id: n.value for t in n.targets if isinstance(t, ast.Name)})
    return out


def _reaches_plants(node, defs: dict, seen=frozenset()) -> bool:
    if any(isinstance(c, ast.Call) and _fn(c) == "plants" for c in ast.walk(node)):
        return True
    return any(isinstance(c, ast.Name) and c.id in defs and c.id not in seen
               and _reaches_plants(defs[c.id], defs, seen | {c.id}) for c in ast.walk(node))


def _legs(tree) -> list:
    """Every leg a suite states by AST: a `prove(...)` call, or a six-item row whose first item is
    a block id -> (line, break_if, real_if, break_leg)."""
    out = []
    for n in ast.walk(tree):
        if isinstance(n, ast.Call) and _fn(n) == "prove" and not any(isinstance(a, ast.Starred) for a in n.args):
            kw = {k.arg: k.value for k in n.keywords}
            args = dict(zip(PROVE_ARGS_T, n.args))
            out.append((n.lineno, *[kw.get(k, args.get(k)) for k in LEG_PARTS_T]))
        elif isinstance(n, ast.Tuple) and len(n.elts) == len(PROVE_ARGS_T):
            head = n.elts[0].values[0] if isinstance(n.elts[0], ast.JoinedStr) and n.elts[0].values else n.elts[0]
            row = dict(zip(PROVE_ARGS_T, n.elts))
            if (_cstr(head) or "").startswith("F-") and not any(
                    isinstance(row[k], ast.Constant) for k in ("break_leg", "real_leg")):
                out.append((n.lineno, *[row[k] for k in LEG_PARTS_T]))
    return out


def _rows_of(arg, scope_node) -> list:
    """The row displays a `plants` argument holds, where the AST shows them."""
    if isinstance(arg, (ast.List, ast.Tuple)):
        return list(arg.elts)
    if isinstance(arg, ast.ListComp):
        return [arg.elt]
    if isinstance(arg, ast.Name):
        rows = []
        for n in ast.walk(scope_node):
            if isinstance(n, (ast.Assign, ast.AugAssign)):
                targets = n.targets if isinstance(n, ast.Assign) else [n.target]
                if any(isinstance(t, ast.Name) and t.id == arg.id for t in targets):
                    rows += _rows_of(n.value, scope_node) if not isinstance(n.value, ast.Name) else []
            elif isinstance(n, ast.Call) and _fn(n) == "append" and _root(n) == arg.id and n.args:
                rows.append(n.args[0])
        return rows
    return []


def suite_findings(name: str, src: str) -> list:
    tree = ast.parse(src)
    parents, defs, out = _parents(tree), _defs(tree), []
    consts = {t.id: n.value for n in tree.body if isinstance(n, ast.Assign)
              for t in n.targets if isinstance(t, ast.Name)}
    for ln, b_if, r_if, b_leg in _legs(tree):
        for label, e in (("break_if", b_if), ("real_if", r_if)):
            e = consts.get(e.id, e) if isinstance(e, ast.Name) else e
            if e is not None and _cstr(e) is not None and not e.value.strip():
                out.append(f"FORM-EMPTY-IF {name} line {ln}: a leg with an empty `{label}` [L-0.14 A]")
        if b_leg is not None and not _reaches_plants(b_leg, defs):
            out.append(f"FORM-BREAK {name} line {ln}: the break leg `{ast.unparse(b_leg)}` is not a `plants` "
                       f"call [L-0.14 A]")
    for n in ast.walk(tree):
        if not isinstance(n, ast.Call):
            continue
        if _fn(n) == "plants" and n.args:
            fns = [f for f in _functions(parents, n) if not isinstance(f, ast.Lambda)]
            for row in _rows_of(n.args[0], fns[0] if fns else tree):
                if not isinstance(row, ast.Tuple):
                    continue
                want = row.elts[1] if len(row.elts) == len(("name", "detector", "thunk")) else None
                if want is None or (isinstance(want, ast.Constant)
                                    and not (isinstance(want.value, str) and want.value.strip())):
                    out.append(f"FORM-PLANTS-ROW {name} line {row.lineno}: a `plants` row that is not a triple "
                               f"with a non-empty detector string [L-0.14 A]")
        elif _fn(n) == "not_run":
            fid = n.args[0] if n.args else None
            fid = consts.get(fid.id, fid) if isinstance(fid, ast.Name) else fid
            if fid is None or _cstr(fid) not in NOT_RUN_FIDS_T:
                shown = repr(_cstr(fid)) if fid is not None and _cstr(fid) is not None else "a non-constant id"
                out.append(f"FORM-NOT-RUN-FID {name} line {n.lineno}: not_run names {shown}, outside "
                           f"NOT_RUN_FIDS_T {list(NOT_RUN_FIDS_T)} [L-0.14 C, seam 3]")
        elif _fn(n) == "default_rng":
            arg = n.args[0] if n.args else next((k.value for k in n.keywords if k.arg == SEED_NAME_T), None)
            form = (isinstance(arg, (ast.List, ast.Tuple)) and len(arg.elts) == len(("seed", "crc32"))
                    and not _is_num(arg.elts[0]) and isinstance(arg.elts[1], ast.Call)
                    and _fn(arg.elts[1]) == "crc32") or (isinstance(arg, ast.Call) and _fn(arg) == "stream_seed")
            if not form:
                out.append(f"FORM-RNG {name} line {n.lineno}: a default_rng seed that is not "
                           f"[SEED, crc32(\"<suite tag>|<block id>\")] [L-0.14 F]")
    if not any(_cstr(a) == ROOT_FLAG_T for n in ast.walk(tree) if isinstance(n, ast.Call) for a in n.args):
        out.append(f"FORM-ROOT {name}: the suite does not parse `{ROOT_FLAG_T}` [L-0.14 H]")
    for ln, m in imported_names(tree):
        if any(m == x or m.startswith(x + ".") for x in NETWORK_T):
            out.append(f"FORM-NETWORK {name} line {ln}: imports {m} — no fixture leg makes a network call "
                       f"[L-0.14 D]")
    return out


def transcript_findings(name: str, text: str) -> list:
    """B's block grammar, both `FAILS IF:` lines of a PASS / FAIL block, a NOT RUN block that is
    exactly its header and its line, the tally of C's form."""
    lines, out = text.split("\n"), []
    heads = [i for i in range(1, len(lines)) if lines[i - 1] == "" and lines[i]
             and not lines[i].startswith(" ") and " — " in lines[i]]
    for i in heads:
        bid = lines[i].split(" — ", 1)[0]
        body = lines[i + 1:lines.index("", i) if "" in lines[i:] else len(lines)]
        m = BLOCK_RX_T.fullmatch(bid)
        qual = bid.split(" [", 1)[1][:-1].split(QUAL_SEP_T) if m and " [" in bid else []
        if not m or len(qual) > len(("leg", "instance")) or any(not q or q != q.strip() for q in qual):
            out.append(f"FORM-BLOCK-ID {name}: {bid!r} is outside the block grammar [L-0.14 B]")
            continue
        state = [w for w in ("PASS", "FAIL", "NOT RUN", "NOT BUILT")
                 if any(x.startswith(f"  [{w}] {bid}: ") for x in body)]
        if len(state) != 1:
            out.append(f"FORM-STATE {name}: block {bid!r} prints {len(state)} state lines {state}")
        elif state[0] in ("PASS", "FAIL"):
            for mark in (BREAK_IF_T, REAL_IF_T):
                if not any(x.startswith(mark) and x[len(mark):].strip() for x in body):
                    out.append(f"FORM-FAILS-IF {name}: the {state[0]} block {bid!r} lacks its "
                               f"`{mark.strip()}` line [L-0.14 A]")
        elif len(body) != 1:
            out.append(f"FORM-NOT-RUN {name}: the {state[0]} block {bid!r} is not exactly its header and its "
                       f"`[{state[0]}]` line [L-0.14 C]")
    tallies = [x for x in lines if TALLY_LOOSE_RX.fullmatch(x)]
    if len(tallies) != 1 or not TALLY_RX_T.fullmatch(tallies[0]):
        out.append(f"FORM-TALLY {name}: {len(tallies)} tally line(s) {tallies} — not exactly one "
                   f"`  N GREEN, M RED, K NOT RUN` [L-0.14 C]")
    return out


def harness_list_findings(head: str) -> list:
    got = tuple(FX.literal_from_text(head, "NOT_RUN_FIDS_T"))
    return [] if got == NOT_RUN_FIDS_T else [
        f"FORM-NOT-RUN-LIST: the harness's NOT_RUN_FIDS_T {list(got)} != this fixture's typed "
        f"{list(NOT_RUN_FIDS_T)} [seam 3]"]


def form_findings(tree: Tree, transcripts=None) -> list:
    transcripts = transcripts or {}
    out = [x for n in tree.suites for x in suite_findings(n, tree.src[n])]
    out += harness_list_findings(tree.src["tierc12_fx"])
    return out + [x for n in sorted(transcripts) for x in transcript_findings(n, transcripts[n])]


SUITE_SHADOW_TEXT = (
    '"""a shadow suite (planted under $TMPDIR; never a source of record)."""\n'
    "from __future__ import annotations\n\nimport sys\n\nimport tierc12_fx as FX\n\n\n"
    "def leg_break():\n"
    "    return FX.plants([(\"a bent copy\", \"DETECTOR\", lambda: [\"DETECTOR caught\"])])\n\n\n"
    "def leg_real():\n    return True, \"holds\"\n\n\n"
    "FIXTURES = ((\"F-SHADOW [a]\", \"a shadow leg\", \"the copy is bent\", \"the record is bent\", leg_break, "
    "leg_real),)\n\n\n"
    "def main():\n"
    "    args = sys.argv[1:]\n"
    "    return FX.run_suite(args=args, root=FX.opt(args, \"--root=\", \".\"), transcript=\"T.txt\", "
    "banner=\"shadow\", seed=None, fixtures=FIXTURES)\n")


def specimen() -> str:
    """A transcript the HARNESS itself writes — one PASS block, one NOT RUN block, the tally — for
    the transcript plants to bend (no transcript of record exists before the first gate)."""
    with FX.capture() as s:
        FX.header("SPECIMEN — a harness session held in memory", seed=CTX["seed"])
        FX.prove("F-GATE [SET · P-ADM-1]", "specimen", "the copy is bent", "the record is bent",
                 lambda: FX.plants([("a bent copy", "DETECTOR", lambda: ["DETECTOR caught"])]),
                 lambda: (True, "holds"))
        FX.not_run("F-MIRROR", "specimen", "the drive is unreachable")
        FX.tally()
    return "\n".join(s["LINES"]) + "\n"


def scoped_transcripts() -> dict:
    return {t: (ROOT / t).read_text(encoding="utf-8") for t in CTX["scope"]["transcripts"]}


def form_break():
    tree, spec = CTX["tree"], specimen()
    if suite_findings(SHADOW_SUITE, SUITE_SHADOW_TEXT) or transcript_findings("specimen", spec):
        raise RuntimeError("the unbent shadow suite or the harness's own specimen is not clean")

    def suite(tail: str = "", old: str = "", new: str = ""):
        text = mut(SUITE_SHADOW_TEXT, old, new) if old else SUITE_SHADOW_TEXT
        return lambda: added(form_findings, plant({SHADOW_SUITE: text + tail}))

    def script(old: str, new: str):
        return lambda: added(form_findings, tree, {"specimen": scratch_text("T.txt", mut(spec, old, new))})

    return FX.plants([
        ("`prove(…, break_if=\"\", …)` in a suite copy", "FORM-EMPTY-IF",
         suite("\n\ndef more():\n    FX.prove(\"F-SHADOW [b]\", \"t\", \"\", \"r\", leg_break, leg_real)\n")),
        ("a `plants` row with an empty detector string in a suite copy", "FORM-PLANTS-ROW",
         suite(old="\"DETECTOR\", lambda", new="\"\", lambda")),
        ("a leg whose break leg is not a `plants` call in a suite copy", "FORM-BREAK",
         suite(old="leg_break, leg_real),)", new="leg_real, leg_real),)")),
        ("`not_run(\"F-SCALP [a HAND-3]\", …)` in a suite copy", "FORM-NOT-RUN-FID",
         suite("\n\ndef more():\n    FX.not_run(\"F-SCALP [a HAND-3]\", \"t\", \"no book\")\n")),
        ("a suite copy that does not parse `--root=`", "FORM-ROOT",
         suite(old="FX.opt(args, \"--root=\", \".\")", new="\".\"")),
        ("`default_rng(seed)` off F's form in a suite copy", "FORM-RNG",
         suite("\n\ndef more(np, seed):\n    return np.random.default_rng(seed)\n")),
        ("`import urllib.request` in a suite copy", "FORM-NETWORK",
         suite("\nimport urllib.request\n")),
        ("a harness copy whose NOT_RUN_FIDS_T gains an FID", "FORM-NOT-RUN-LIST",
         lambda: added(form_findings, plant({"tierc12_fx": mut(
             tree.src["tierc12_fx"], "NOT_RUN_FIDS_T = (", "NOT_RUN_FIDS_T = (\"F-SCALP\", ")}))),
        ("a transcript copy with one `[REAL]  FAILS IF:` line removed", "FORM-FAILS-IF",
         script(REAL_IF_T + "the record is bent\n", "")),
        ("a block id `F-GATE (P-ADM-1)` in a transcript copy", "FORM-BLOCK-ID",
         script("\nF-GATE [SET · P-ADM-1] — ", "\nF-GATE (P-ADM-1) — ")),
        ("a NOT RUN block with a second line in a transcript copy", "FORM-NOT-RUN",
         script("the drive is unreachable\n", "the drive is unreachable\n  and more\n")),
        ("a tally line without its NOT RUN count in a transcript copy", "FORM-TALLY",
         script(" RED, 1 NOT RUN", " RED")),
    ])


def form_real():
    tree, scripts = CTX["tree"], scoped_transcripts()
    control = transcript_findings("specimen", specimen())
    f = form_findings(tree, scripts) + control
    names = ", ".join(scripts) if scripts else ("none — no record before this gate names a transcript")
    return (not f), (
        f"by AST over the {len(tree.suites)} suite(s) in scope {tree.suites}: no empty break_if / real_if, every "
        f"`plants` row a triple with a detector, every break leg a `plants` call, no not_run outside "
        f"NOT_RUN_FIDS_T (== the harness's own list), `{ROOT_FLAG_T}` parsed, no default_rng off F's form, none "
        f"of {list(NETWORK_T)} imported; transcripts of record before {CTX['stage']}: {names}; control GREEN: a "
        f"transcript the harness writes in memory (one PASS block, one NOT RUN block, the tally) holds the form"
        + (f" — {len(f)} finding(s): " + " | ".join(f) if f else ""))


# ═══════════════════════════════════════════════════════════════ F-CLOSURE [ii] — AST + the static walk
def _sys_modules(node) -> bool:
    return (isinstance(node, ast.Attribute) and node.attr == "modules"
            and isinstance(node.value, ast.Name) and node.value.id == "sys")


def scan_ii(name: str, tree, role: str) -> list:
    """Leg (ii) on ONE source of `role` (decision | door | lineage)."""
    parents, out = _parents(tree), []
    for ln, x in imported_names(tree):
        why = forbidden_rule(x, role)
        if why:
            out.append(f"CLOSURE-IMPORT [{role}] {name} line {ln}: imports {x} — {why}")
    for ln, fn, where, const, targets in dyn_sites(tree):
        if role == "lineage":                   # TC11's filed law for the lineage's name-held imports
            if const is None and not targets:
                out.append(f"CLOSURE-DYNAMIC [lineage] {name} line {ln}: {fn}(<non-constant>) in {where}() "
                           f"names no repo module")
            out += [f"CLOSURE-IMPORT [lineage] {name} line {ln}: {fn}({t!r}) name-held in {where}() — "
                    f"{forbidden_rule(t, role)}" for t in targets if forbidden_rule(t, role)]
        elif const is not None:
            out.append(f"CLOSURE-DYNAMIC [{role}] {name} line {ln}: {fn}({const!r}) — a constant-string "
                       f"dynamic import")
        elif (name, where) not in DYN_DECLARED_T:
            out.append(f"CLOSURE-DYNAMIC [{role}] {name} line {ln}: {fn}(<non-constant>) in {where}() — not a "
                       f"door L-D declares")
    pkg = {k for k, v in aliases(tree).items() if v == ANALYTICS_T}
    for n in ast.walk(tree):
        if isinstance(n, ast.Call):
            f = n.func
            name_called = (f.id if isinstance(f, ast.Name) and f.id in EXEC_FUNCS_T else
                           f.attr if (isinstance(f, ast.Attribute) and f.attr in EXEC_FUNCS_T
                                      and isinstance(f.value, ast.Name) and f.value.id == "builtins") else None)
            if name_called and role != "lineage":
                out.append(f"CLOSURE-EXEC [{role}] {name} line {n.lineno}: {name_called}(…) in "
                           f"{_where(parents, n)}() — code built at run time")
            if isinstance(f, ast.Attribute) and f.attr in SYSMOD_CALLS_T and _sys_modules(f.value) and n.args \
                    and forbidden_rule(_cstr(n.args[0]) or "", role):
                out.append(f"CLOSURE-SYSMODULES [{role}] {name} line {n.lineno}: sys.modules.{f.attr}"
                           f"({n.args[0].value!r})")
            if _fn(n) == "getattr" and n.args and isinstance(n.args[0], ast.Name) and n.args[0].id in pkg \
                    and role != "door" and (len(n.args) < len(("obj", "name")) or _cstr(n.args[1]) is None
                         or n.args[1].value in WALL_ATTRS_T):
                out.append(f"CLOSURE-ATTR [{role}] {name} line {n.lineno}: `{ast.unparse(n)}` on the "
                           f"{ANALYTICS_T} package")
            if _fn(n) in TOPBOT_CALLS_T:
                out += [f"CLOSURE-TOPBOT [{role}] {name} line {n.lineno}: {_fn(n)}(…, {a.value!r})"
                        for a in n.args if _cstr(a) in TOPBOT_T]
        elif isinstance(n, ast.Subscript) and _sys_modules(n.value) and forbidden_rule(_cstr(n.slice) or "", role):
            out.append(f"CLOSURE-SYSMODULES [{role}] {name} line {n.lineno}: sys.modules[{n.slice.value!r}]")
        elif isinstance(n, ast.Attribute):
            if n.attr in WALL_ATTRS_T and isinstance(n.value, ast.Name) and n.value.id in pkg \
                    and role != "door":
                out.append(f"CLOSURE-ATTR [{role}] {name} line {n.lineno}: `{ast.unparse(n)}` — "
                           f"`{n.attr}` on a name bound to the {ANALYTICS_T} package")
            if n.attr in TOPBOT_T:
                out.append(f"CLOSURE-TOPBOT [{role}] {name} line {n.lineno}: a .{n.attr} read")
    return out


def tc10_lazy(texts: dict) -> set:
    """{(module, enclosing function)} of every function-local range import in TC10-layer TEXT."""
    out = set()
    for mod, text in texts.items():
        tree = ast.parse(text)
        parents = _parents(tree)
        for n in ast.walk(tree):
            if isinstance(n, (ast.Import, ast.ImportFrom)) and _where(parents, n) != "<module>":
                names = [a.name for a in n.names] + ([n.module] if isinstance(n, ast.ImportFrom) and n.module else [])
                if any(s in x for x in names for s in FORBIDDEN_SUBSTR_T):
                    out.add((mod, _where(parents, n)))
    return out


def static_walk(tree: Tree) -> dict:
    """The static repo closure of the decision sources' imports: lineage modules (walked), the
    TC10 layer (disclosed, not walked), and what a tierc12 import reaches outside the scope."""
    lineage, tc10, outside, seen = {}, {}, [], set()
    queue = [(n, x) for n in tree.decision for _, x in imported_names(tree.ast(n))]
    while queue:
        src, x = queue.pop(0)
        root = x.split(".")[0]
        if root.startswith("tierc12_"):
            if root not in tree.names and (src, root) not in outside:
                outside.append((src, root))
            continue
        if forbidden_rule(x, "decision"):
            continue                            # a finding at its importer; never walked
        for c in repo_candidates(x):
            if c in seen:
                continue
            seen.add(c)
            if c.startswith(TC10_PREFIX_T):
                tc10[c] = FX.rel(repo_file(c), ROOT)
                continue
            t = ast.parse(repo_file(c).read_text(encoding="utf-8"))
            lineage[c] = t
            queue += [(c, y) for _, y in imported_names(t)]
            queue += [(c, y) for _, _, _, _, tg in dyn_sites(t) for y in tg]
    return {"lineage": dict(sorted(lineage.items())), "tc10": dict(sorted(tc10.items())),
            "outside": sorted(outside)}


def lineage_pins() -> dict:
    """{repo-relative path: sha256} of the disclosed layer, from env/LINEAGE_PINS.json — {} before
    TC12-ENV.vendor files it (seam 14: stated EMPTY, never guessed)."""
    if not filed_by_now(LINEAGE_PINS_REL):
        return {}
    out = {}

    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                sha = v.get("sha256") if isinstance(v, dict) else v
                if isinstance(k, str) and k.endswith(".py") and isinstance(sha, str):
                    out[k] = sha
                walk(v)
            if isinstance(o.get("path"), str) and isinstance(o.get("sha256"), str):
                out[o["path"]] = o["sha256"]
        elif isinstance(o, list):
            for v in o:
                walk(v)
    walk(json.loads((ROOT / LINEAGE_PINS_REL).read_text(encoding="utf-8")))
    return out


def pins_of_record() -> dict:
    """{label: (close ms, ISO)} — TC12's pin (O-7's printed value; Stage D's record once a record
    names it), TC11's and TC10's, each read from its file, never typed."""
    m = PIN_O7_RX.search((ROOT / RULINGS_REL).read_text(encoding="utf-8"))
    if not m:
        halt(f"{RULINGS_REL}: O-7's printed pin is not found")
    t11 = json.loads((ROOT / TC11_PIN_REL).read_text(encoding="utf-8"))
    out = {"TC12's pin (O-7)": (int(m.group(1)), m.group(2)),
           "TC11's pin": (t11["as_of_last_closed_4h_close_ms"], t11["as_of_last_closed_4h"]),
           "TC10's pin": (t11["tc10_pin_close_ms"], t11["tc10_pin"])}
    if filed_by_now(TC12_PIN_REL):
        d = json.loads((ROOT / TC12_PIN_REL).read_text(encoding="utf-8"))
        out["TC12's pin (data/AS_OF_PIN.json)"] = (d["as_of_last_closed_4h_close_ms"], d["as_of_last_closed_4h"])
    return out


def captured_ticks() -> list:
    """The sealed capture's tick strings — [] before Stage D seals it (stated, never guessed)."""
    if not filed_by_now(SPECS_REL):
        return []
    d = json.loads((ROOT / SPECS_REL).read_text(encoding="utf-8"))
    return sorted({str(a["price_tick"]) for a in d.get("assets", []) if "price_tick" in a})


def pin_findings(name: str, src: str, pins: dict) -> list:
    """L-D's F-D-PIN [e] on a wider scope: a pin as an int or as an ISO string, by text scan."""
    out = []
    for label, (ms, iso) in sorted(pins.items()):
        stem = iso.rsplit(":", 1)[0]               # the instant to the minute, seconds and zone dropped
        forms = (("an int", re.compile(r"(?<![0-9_])" + "_?".join(str(ms)) + r"(?![0-9_])")),
                 ("an ISO string", re.compile(re.escape(stem).replace("T", "[T ]"))))
        for what, rx in forms:
            for hit in rx.finditer(src):
                ln = src.count("\n", 0, hit.start()) + 1
                out.append(f"PIN-LITERAL {name} line {ln}: holds {label} as {what} ({hit.group(0)}) — every "
                           f"read of a pin is by object [L-D.1, seam 16]")
    return out


def _ticky(node) -> bool:
    word = node.id if isinstance(node, ast.Name) else node.attr if isinstance(node, ast.Attribute) else ""
    return TICK_WORD_T in word.lower()


def tick_findings(name: str, tree, ticks) -> list:
    """L-D's F-TICK [b] on a wider scope: a tick literal in an assignment or comparison naming
    `tick`, or a BinOp with a tick-named operand under a comparison."""
    held = set()
    for t in ticks:
        held.add(Decimal(t))
    out, seen = [], set()

    def literal(ln: int, value) -> None:
        for c in ast.walk(value):
            if isinstance(c, ast.Constant) and type(c.value) in (int, float, str):
                try:
                    hit = Decimal(str(c.value)) in held
                except InvalidOperation:
                    hit = False
                if hit:
                    out.append(f"TICK-LITERAL {name} line {ln}: the tick typed as the literal {c.value!r} "
                               f"[L-D.23, seam 16]")

    for n in ast.walk(tree):
        if isinstance(n, ast.Compare):
            sides = [n.left] + list(n.comparators)
            if any(_ticky(x) for s in sides for x in ast.walk(s)):
                for s in sides:
                    literal(n.lineno, s)
            for b in ast.walk(n):
                if isinstance(b, ast.BinOp) and (_ticky(b.left) or _ticky(b.right)) and id(b) not in seen:
                    seen.add(id(b))
                    out.append(f"TICK-FLOAT-COMPARE {name} line {b.lineno}: `{ast.unparse(b)}` under a "
                               f"comparison — tick arithmetic is exact integer ticks, never a float compare "
                               f"[O-20, L-D.23, seam 16]")
        elif isinstance(n, (ast.Assign, ast.AnnAssign, ast.AugAssign)) and n.value is not None:
            targets = n.targets if isinstance(n, ast.Assign) else [n.target]
            if any(_ticky(x) for t in targets for x in ast.walk(t)):
                literal(n.lineno, n.value)
        elif isinstance(n, ast.keyword) and n.arg and TICK_WORD_T in n.arg.lower():
            literal(n.value.lineno, n.value)
    return out


def closure_ii_findings(tree: Tree, tc10_over=None, loaded=None) -> list:
    stage, out = CTX["stage"], [f"CLOSURE-SCOPE: {n}.py is named by a record up to {CTX['stage']} and is not "
                                f"on file" for n in CTX["scope"]["missing"]]
    for n in tree.glob:
        out += scan_ii(n, tree.ast(n), "door" if n in DOORS_T else "decision")
    walk = static_walk(tree)
    for n, t in walk["lineage"].items():
        out += scan_ii(n, t, "lineage")
    out += [f"CLOSURE-REACH {src} imports {x}, a tierc12 module no record up to {stage} names"
            for src, x in walk["outside"]]
    if not stage_at_least(stage, SHIM_STAGE_T) and (walk["lineage"] or walk["tc10"]):
        out.append(f"CLOSURE-REACH: at {stage} no module in scope may reach the lineage; the static closure "
                   f"holds {sorted(walk['lineage']) + sorted(walk['tc10'])}")
    pins = lineage_pins()
    for mod, rel in walk["tc10"].items():
        sha = FX.sha_bytes((ROOT / rel).read_bytes())
        if pins.get(rel) != sha:
            out.append(f"CLOSURE-TC10-UNDISCLOSED {mod}: {rel} is reached and {LINEAGE_PINS_REL} "
                       f"{'pins another sha' if rel in pins else 'does not name it'}")
    mods = sorted({m for m, _ in TC10_LAZY_RANGE_T} | set(walk["tc10"]))
    texts = {m: (tc10_over or {}).get(m) or repo_file(m).read_text(encoding="utf-8") for m in mods}
    got = tc10_lazy(texts)
    if got != set(TC10_LAZY_RANGE_T):
        out.append(f"TC10-LAZY: the function-local range imports found by AST {sorted(got)} != "
                   f"TC10_LAZY_RANGE_T {sorted(TC10_LAZY_RANGE_T)}")
    if loaded is not None:                      # COVERAGE: what a fresh interpreter loaded
        known = set(walk["lineage"]) | set(walk["tc10"]) | set(tree.names)
        miss = sorted(m for m in loaded if repo_file(m) is not None and m not in known)
        if miss:
            out.append(f"CLOSURE-COVERAGE: a fresh interpreter loaded repo module(s) {miss} that are neither "
                       f"in the static walk nor in the disclosed TC10 layer")
    pin_set, ticks = pins_of_record(), captured_ticks()
    for n in tree.glob:
        out += pin_findings(n, tree.src[n], pin_set) + tick_findings(n, tree.ast(n), ticks)
    return out


def ii_break():
    tree = CTX["tree"]
    ms, iso = pins_of_record()["TC12's pin (O-7)"]

    def shadow(tail: str):
        return lambda: added(closure_ii_findings, plant({SHADOW: SHADOW_TEXT + tail}))

    brk = repo_file("tierc10_brk").read_text(encoding="utf-8")
    rows = [
        ("a decision-module copy importing analytics.value_area inside a function body", "CLOSURE-IMPORT",
         shadow("\n\ndef g():\n    import analytics.value_area as VA\n    return VA\n")),
        ("a decision-module copy importing a door inside a function body", "CLOSURE-IMPORT",
         shadow("\n\ndef g():\n    import tierc12_va\n    return tierc12_va\n")),
        ('`importlib.import_module("analytics.value_area")` in a copy', "CLOSURE-DYNAMIC",
         shadow('import importlib\nVA = importlib.import_module("analytics.value_area")\n')),
        ("a non-constant `importlib.import_module(name)` in a copy", "CLOSURE-DYNAMIC",
         shadow("import importlib\n\n\ndef g(name):\n    return importlib.import_module(name)\n")),
        ('`sys.modules["analytics.value_area"]` in a copy', "CLOSURE-SYSMODULES",
         shadow('import sys\nVA = sys.modules["analytics.value_area"]\n')),
        ("`AN.value_area.x` on the package alias in a copy", "CLOSURE-ATTR",
         shadow("import analytics as AN\nX = AN.value_area.x\n")),
        ("`import tierc10_census` in a copy", "CLOSURE-IMPORT", shadow("import tierc10_census\n")),
        ("`import tc11x_va` in a door copy", "CLOSURE-IMPORT [door]",
         lambda: added(closure_ii_findings, plant({DOORS_T[0]: DOOR_SHADOW_TEXT + "import tc11x_va\n"}))),
        ('`exec("import tierc10_census")` in a copy', "CLOSURE-EXEC",
         shadow('\n\ndef g():\n    exec("import tierc10_census")\n')),
        ("a `.top` read of a range object in a copy", "CLOSURE-TOPBOT",
         shadow("\n\ndef g(r):\n    return r.top\n")),
        ("a fourth function-local range import planted in a text copy of tierc10_brk.py", "TC10-LAZY",
         lambda: added(closure_ii_findings, tree, tc10_over={"tierc10_brk": scratch_text(
             "tierc10_brk.py", brk + "\n\ndef planted():\n    import tierc10_census as C\n    return C\n")})),
        ("the pin typed as an int in a copy", "PIN-LITERAL", shadow(f"PIN_MS = {ms}\n")),
        ("the pin typed as an ISO string in a copy", "PIN-LITERAL", shadow(f'PIN_ISO = "{iso}"\n')),
        ("a float `low < limit - tick` compare in a copy", "TICK-FLOAT-COMPARE",
         shadow("\n\ndef g(low, limit, tick):\n    return low < limit - tick\n")),
    ]
    if captured_ticks():
        rows.append(("a captured tick typed and assigned to `tick` in a copy", "TICK-LITERAL",
                     shadow(f"tick = {captured_ticks()[0]}\n")))
    if not stage_at_least(CTX["stage"], SHIM_STAGE_T):
        rows.append((f"a copy importing a lineage module at {CTX['stage']}", "CLOSURE-REACH",
                     shadow("import tierc9\n")))
    else:
        walk = static_walk(tree)
        known = set(walk["lineage"]) | set(walk["tc10"]) | set(tree.names)
        stray = next(q.stem for q in sorted(SCRIPTS.glob("*.py")) if q.stem not in known
                     and not q.stem.startswith("tierc12_"))
        rows.append(("a repo module outside both the walk and the TC10 layer among those a fresh interpreter "
                     "loaded", "CLOSURE-COVERAGE",
                     lambda: [x for x in closure_ii_findings(tree, loaded=sorted(fresh_loaded()) + [stray])
                              if x not in closure_ii_findings(tree, loaded=sorted(fresh_loaded()))]))
    return FX.plants(rows)


def ii_real():
    tree, stage = CTX["tree"], CTX["stage"]
    shim = stage_at_least(stage, SHIM_STAGE_T)
    f = closure_ii_findings(tree, loaded=sorted(fresh_loaded()) if shim else None)
    walk, pins, ticks = static_walk(tree), lineage_pins(), captured_ticks()
    if walk["tc10"]:
        layer = "; ".join(f"{m} {rel} sha256 {pins.get(rel, 'NOT PINNED')}" for m, rel in walk["tc10"].items())
    else:
        layer = (f"EMPTY — {LINEAGE_PINS_REL} is not yet filed (TC12-ENV.vendor files it); nothing is on file "
                 f"to read and nothing is guessed [seam 14]" if not pins else "EMPTY — no decision source reaches it")
    lazy = sorted({m for m, _ in TC10_LAZY_RANGE_T} | set(walk["tc10"]))
    return (not f), (
        f"AST over {len(tree.decision)} decision source(s) {tree.decision} and the doors "
        f"[{filed(DOORS_T, tree)}]: no forbidden import anywhere (function bodies included), no dynamic import "
        f"outside {[f'{a}.{b}' for a, b in DYN_DECLARED_T]}, no exec / eval / compile, no sys.modules reach of a "
        f"forbidden name, no `value_area` / `profile` on the {ANALYTICS_T} package, no .top / .bottom read; the "
        f"static repo closure of their imports: lineage modules walked {sorted(walk['lineage']) or 'none'}"
        + ("" if shim else f" — no module in scope at {stage} reaches the lineage, asserted")
        + f"; TC10 LAYER, disclosed and not walked: {layer}; TC10_LAZY_RANGE_T "
        f"{[f'{a}.{b}' for a, b in TC10_LAZY_RANGE_T]} == the function-local range imports found by AST in the "
        f"TEXT of {lazy}; COVERAGE "
        + ("every repo module a fresh interpreter loaded is in the walk or the disclosed layer" if shim else
           f"binds with leg (i) from {SHIM_STAGE_T}")
        + f"; [seam 16] over the {len(tree.glob)} non-fixture source(s): no source holds "
        f"{', '.join(sorted(pins_of_record()))} as an int or as an ISO string; captured ticks: "
        + (f"{len(ticks)} string(s) of the sealed capture, none typed" if ticks else
           f"not yet filed ({SUBSTRATE_STAGE_T} seals the capture) — the literal clause has no referee")
        + "; no BinOp with a tick-named operand under a comparison"
        + (f" — {len(f)} finding(s): " + " | ".join(f) if f else ""))


# ═══════════════════════════════════════════════════════════════ F-CLOSURE [iii] — data-only, VA-blind, doors
def door_tables() -> dict:
    """{repo-relative table: its columns} for every door table a record in scope names."""
    paths = sorted(p for p in CTX["scope"]["paths"] if DOOR_TABLE_RX.fullmatch(p) and (ROOT / p).is_file())
    if not paths:
        return {}
    import pyarrow.parquet as pq               # schema only; reached only once a door table exists
    return {p: list(pq.read_schema(str(ROOT / p)).names) for p in paths}


def blind_dirs() -> list:
    """(directory, its one writer, its READ_SET documents) for every parquet directory in scope."""
    out = []
    for p in sorted(x for x in CTX["scope"]["paths"] if x.endswith("/" + MANIFEST_NAME_T) and (ROOT / x).is_file()):
        d = (ROOT / p).parent
        writer = Path(str(json.loads((ROOT / p).read_text(encoding="utf-8")).get("source_script", ""))).stem
        out.append((FX.rel(d, ROOT), writer, [json.loads(q.read_text(encoding="utf-8"))
                                              for q in sorted(d.glob(READ_SET_GLOB_T))]))
    return out


def _strings(o) -> list:
    if isinstance(o, dict):
        return [s for k, v in o.items() for s in _strings(k) + _strings(v)]
    if isinstance(o, list):
        return [s for v in o for s in _strings(v)]
    return [o] if isinstance(o, str) else []


def blind_dir_findings(dirs) -> list:
    out = []
    for where, writer, read_sets in dirs:
        hits = sorted({s for r in read_sets for s in _strings(r) if s.startswith(VA_DIR_REL)})
        if writer in VA_BLIND_T and hits:
            out.append(f"VA-BLIND {where}: its one parquet writer {writer} is on VA_BLIND_T and its READ_SET "
                       f"holds {hits} [seam 62]")
    return out


def door_col_findings(tables: dict) -> list:
    return [f"DOOR-COLS {t}: a door table holds the TRADE_COLS_T column(s) "
            f"{sorted(set(cols) & set(TRADE_COLS_T))}" for t, cols in sorted(tables.items())
            if set(cols) & set(TRADE_COLS_T)]


def closure_iii_findings(tree: Tree, dirs=(), tables=None) -> list:
    out = []
    for n in tree.glob:
        if n in DOORS_T:
            continue
        hits = sorted({(x.lineno, x.id if isinstance(x, ast.Name) else x.attr) for x in ast.walk(tree.ast(n))
                       if (isinstance(x, ast.Name) and x.id in VA_NAMES_T)
                       or (isinstance(x, ast.Attribute) and x.attr in VA_NAMES_T)})
        out += [f"VA-NAME {n} line {ln}: holds the value-area name `{w}` outside DOORS_T — data only"
                for ln, w in hits]
    for n in tree.names:
        imps = imported_names(tree.ast(n))
        if n in VA_BLIND_T and any(x == READER_T or x.startswith(READER_T + ".") for _, x in imps):
            out.append(f"VA-BLIND {n}: a VA_BLIND_T member imports the reader {READER_T}")
        doors = sorted({x.split(".")[0] for _, x in imps if x.split(".")[0] in DOORS_T})
        if doors and n not in VA_MODULE_FIXTURES_T:
            out.append(f"DOOR-IMPORTER {n}: imports {doors} — only {list(VA_MODULE_FIXTURES_T)} may import a door")
        module = any(x == FORBIDDEN_EXACT_T[0] or x.startswith(FORBIDDEN_EXACT_T[0] + ".") for _, x in imps)
        if module and n not in DOORS_T + VA_MODULE_FIXTURES_T:
            out.append(f"DOOR-UNTYPED {n}: imports {FORBIDDEN_EXACT_T[0]} and is not typed in DOORS_T "
                       f"{list(DOORS_T)}")
        if n in DOORS_T:
            if not module:
                out.append(f"DOOR-UNEARNED {n}: a typed door that does not import {FORBIDDEN_EXACT_T[0]}")
            first = next((a.name for s in tree.ast(n).body if isinstance(s, (ast.Import, ast.ImportFrom))
                          for a in ([ast.alias(name=s.module or "")] if isinstance(s, ast.ImportFrom) else s.names)
                          if a.name.split(".")[0] not in sys.stdlib_module_names), None)
            if first != SHIM_T:
                out.append(f"DOOR-ENV-FIRST {n}: its first non-stdlib import is {first!r}, not {SHIM_T}")
            roots = sorted({c.value for c in ast.walk(tree.ast(n)) if _cstr(c) is not None
                            and REGBOOKS_T in re.split(r"[/\\]", c.value)})
            if roots:
                out.append(f"DOOR-ROOT {n}: a door names a path under {REGBOOKS_T}/ {roots}")
    return out + blind_dir_findings(dirs) + door_col_findings(tables or {})


def iii_break():
    table = {VA_DIR_REL + "va_shadow.parquet": ["symbol", "close_ms", "state", "val", "vah", "poc"]}
    bent = {k: v + [TRADE_COLS_T[0]] for k, v in table.items()}
    read_set = {"tc12-record": [VA_DIR_REL + "va_shadow.parquet"]}
    if [x for x in closure_iii_findings(plant({DOORS_T[0]: DOOR_SHADOW_TEXT}), tables=table)
            if x.startswith("DOOR-")]:
        raise RuntimeError("the unbent shadow door or its table is not clean")
    return FX.plants([
        ("a decision-module copy holding the name `va_machine`", "VA-NAME",
         lambda: added(closure_iii_findings, plant({SHADOW: SHADOW_TEXT + "\n\ndef g(E):\n    return E.va_machine\n"}))),
        ("a tierc12_books copy importing the reader", "VA-BLIND tierc12_books",
         lambda: added(closure_iii_findings, plant({VA_BLIND_T[0]: SHADOW_TEXT + f"import {READER_T}\n"}))),
        ("a READ_SET copy of a VA-blind writer's directory holding a path under va/", "VA-BLIND",
         lambda: added(closure_iii_findings, CTX["tree"],
                       dirs=[(T12_REL + "/books", VA_BLIND_T[0], [read_set])])),
        ("a third module importing analytics.value_area that is not typed in DOORS_T", "DOOR-UNTYPED",
         lambda: added(closure_iii_findings, plant({SHADOW: SHADOW_TEXT + "from analytics import value_area as VA\n"}))),
        ("a shadow suite, not tierc12_va_fixtures, importing a door", "DOOR-IMPORTER",
         lambda: added(closure_iii_findings, plant({SHADOW_SUITE: SUITE_SHADOW_TEXT + f"import {DOORS_T[0]}\n"}))),
        ("a door copy without its import", "DOOR-UNEARNED",
         lambda: added(closure_iii_findings, plant({DOORS_T[0]: mut(
             DOOR_SHADOW_TEXT, "from analytics import value_area as VA\n", "")}))),
        ("a door copy importing analytics.value_area before tierc12_env", "DOOR-ENV-FIRST",
         lambda: added(closure_iii_findings, plant({DOORS_T[0]: mut(
             DOOR_SHADOW_TEXT, "import tierc12_env as E\nfrom analytics import value_area as VA\n",
             "from analytics import value_area as VA\nimport tierc12_env as E\n")}))),
        ("a DOOR 2 copy writing under regbooks/", "DOOR-ROOT",
         lambda: added(closure_iii_findings, plant({DOORS_T[1]: DOOR_SHADOW_TEXT
                                             + f'BOOK = E.OUT / "{REGBOOKS_T}" / "P-SFP-VA-1"\n'}))),
        ("a door table copy with a `net_r` column", "DOOR-COLS",
         lambda: added(closure_iii_findings, CTX["tree"], tables=bent)),
    ])


def iii_real():
    tree = CTX["tree"]
    dirs, tables = blind_dirs(), door_tables()
    f = closure_iii_findings(tree, dirs, tables)
    return (not f), (
        f"DATA-ONLY: none of the {len(tree.decision)} GLOB source(s) outside DOORS_T holds a Name or Attribute "
        f"in {list(VA_NAMES_T)}; VA-BLIND [{filed(VA_BLIND_T, tree)}]: no member on file imports the reader "
        f"{READER_T}; parquet directories in scope, keyed on their one writer [seam 62]: "
        f"{[(d, w) for d, w, _ in dirs] or 'none on file'}; DOORS [{filed(DOORS_T, tree)}]: every door on file "
        f"is EARNED and imports {SHIM_T} first, names no {REGBOOKS_T}/ root, and is imported only by "
        f"{list(VA_MODULE_FIXTURES_T)}; no other module in scope imports {FORBIDDEN_EXACT_T[0]}; door tables in "
        f"scope: {sorted(tables) or 'none on file'} — none holds a column of {list(TRADE_COLS_T)}"
        + (f" — {len(f)} finding(s): " + " | ".join(f) if f else ""))


# ═══════════════════════════════════════════════════════════════ F-CLOSURE [i], [i-b] — fresh interpreters
_PROBE = ("import importlib, json, sys\n"
          "sys.path[:0] = sys.argv[2:]\n"
          "m = importlib.import_module(sys.argv[1])\n"
          f"print({PROBE_MARK!r} + json.dumps({{'file': getattr(m, '__file__', None), "
          "'modules': sorted(sys.modules)}))\n")


def _python(argv: list, stdin: str = "") -> tuple:
    """One fresh interpreter: (exit code, stdout + stderr)."""
    r = subprocess.run([sys.executable, "-B", *argv], input=stdin, capture_output=True, text=True,
                       cwd=str(ROOT), env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
    return r.returncode, r.stdout + r.stderr


def fresh(mod: str, pre=()) -> dict:
    rc, text = _python(["-c", _PROBE, mod, *[str(p) for p in pre], str(SCRIPTS), str(ROOT)])
    info = next((json.loads(x[len(PROBE_MARK):]) for x in text.splitlines() if x.startswith(PROBE_MARK)), None)
    return {"rc": rc, "info": info, "text": text}


def fresh_findings(mod: str, res: dict, expect: Path) -> list:
    out = []
    if res["info"] is None:
        return [f"FRESH-EXIT {mod}: the fresh interpreter did not finish its import (exit {res['rc']})"]
    held = [m for m in res["info"]["modules"] if forbidden_rule(m, "decision")]
    if held:
        out.append(f"FRESH-FORBIDDEN {mod}: after `import {mod}` sys.modules holds {held}")
    got = res["info"]["file"]
    if got is None or Path(got).resolve() != expect.resolve():
        out.append(f"FRESH-FILE {mod}: loaded from {FX.rel(got, ROOT) if got else None}, not scripts/{mod}.py")
    return out


def exit_findings(label: str, res: dict) -> list:
    out = []
    if WALL_LINE_T in res["text"]:
        out.append(f"WALL-EXIT {label}: the exit check logged `{WALL_LINE_T}` (exit {res['rc']})")
    elif res["rc"] != 0:
        out.append(f"WALL-EXIT {label}: exit {res['rc']}, not 0")
    return out


def fresh_all() -> dict:
    """One fresh interpreter per decision module of the tree of record (run once per suite run)."""
    if "fresh" not in CTX:
        CTX["fresh"] = {n: fresh(n) for n in CTX["tree"].decision}
    return CTX["fresh"]


def fresh_loaded() -> set:
    return {m for r in fresh_all().values() if r["info"] for m in r["info"]["modules"]}


def shadow_dir(files: dict) -> Path:
    d = Path(tempfile.mkdtemp(prefix="shadow_", dir=CTX["scratch"]))
    for rel, text in files.items():
        (d / rel).parent.mkdir(parents=True, exist_ok=True)
        (d / rel).write_text(text, encoding="utf-8")
    return d


def i_break():
    def run(mod: str, files: dict):
        d = shadow_dir(files)
        return fresh_findings(mod, fresh(mod, pre=[d]), d / f"{mod}.py")

    stub = {f"{DOORS_T[0]}.py": "", f"{ANALYTICS_T}/__init__.py": "", f"{ANALYTICS_T}/value_area.py": ""}
    return FX.plants([
        ("a P-SFP builder copy importing tierc12_va", "FRESH-FORBIDDEN",
         lambda: run("tierc12_stage_r_sfp", dict(stub, **{"tierc12_stage_r_sfp.py": f"import {DOORS_T[0]}\n"}))),
        ("`import analytics.value_area` at the top of a book-module copy", "FRESH-FORBIDDEN",
         lambda: run("tierc12_books", dict(stub, **{"tierc12_books.py": "import analytics.value_area\n"}))),
        ("a NEW unnamed tierc12 shadow module importing a module that imports a door (transitive)",
         "FRESH-FORBIDDEN",
         lambda: run(SHADOW, dict(stub, **{f"{SHADOW}.py": "import tierc12_zz_helper\n",
                                           "tierc12_zz_helper.py": f"import {DOORS_T[0]}\n"}))),
    ])


def i_real():
    tree, res = CTX["tree"], fresh_all()
    f = [x for n in tree.decision for x in fresh_findings(n, res[n], SCRIPTS / f"{n}.py")]
    return (not f), (f"one fresh interpreter per decision module ({len(tree.decision)}): after `import <module>` "
                     f"sys.modules holds no {list(FORBIDDEN_EXACT_T)}, no DOORS_T name and no forbidden name, and "
                     f"each loaded from scripts/<name>.py: {tree.decision}"
                     + (f" — {len(f)} finding(s): " + " | ".join(f) if f else ""))


def wall_tuple_findings(shim_text: str) -> list:
    out = []
    for name, want in (("VA_WALL_DOORS", DOORS_T), ("VA_WALL_FIXTURES", VA_MODULE_FIXTURES_T)):
        try:
            got = tuple(FX.literal_from_text(shim_text, name))
        except (KeyError, ValueError) as e:
            out.append(f"WALL-TUPLES {name}: not readable as a literal from the shim's text ({e})")
            continue
        if got != want:
            out.append(f"WALL-TUPLES {name}: the shim types {list(got)}, this fixture {list(want)}")
    return out


def ib_break():
    shim = CTX["tree"].src[SHIM_T]

    def run(script: str, files: dict):
        d = shadow_dir(files)
        rc, text = _python([str(d / script)])
        return exit_findings(script, {"rc": rc, "text": text})

    head = f"import sys\nsys.path[:0] = [{str(SCRIPTS)!r}, {str(ROOT)!r}]\nimport {SHIM_T} as E\n"
    lazy = head + f"\n\ndef main():\n    import {DOORS_T[0]}\n\n\nmain()\n"
    return FX.plants([
        ("a shadow builder with a run-time lazy door import, run as a subprocess", f"exit {WALL_EXIT_T}",
         lambda: run("tierc12_zz_builder.py", {"tierc12_zz_builder.py": lazy, f"{DOORS_T[0]}.py": ""})),
        ("a shadow non-fixture module importing analytics.profile, run as a subprocess", f"exit {WALL_EXIT_T}",
         lambda: run("tierc12_zz_profile.py", {"tierc12_zz_profile.py": head + "import analytics.profile\n"})),
        ("a shim-text copy whose VA_WALL_DOORS lacks DOOR 2", "WALL-TUPLES",
         lambda: wall_tuple_findings(scratch_text("shim.py", mut(shim, f', "{DOORS_T[1]}")', ",)")))),
    ])


def ib_real():
    tree, res = CTX["tree"], fresh_all()
    f = wall_tuple_findings(tree.src[SHIM_T]) if SHIM_T in tree.names else [f"WALL-TUPLES: {SHIM_T} is not on file"]
    f += [x for n in tree.decision for x in exit_findings(n, res[n])]
    return (not f), (f"the shim's VA_WALL_DOORS / VA_WALL_FIXTURES, read as text, are {list(DOORS_T)} / "
                     f"{list(VA_MODULE_FIXTURES_T)}; each of leg (i)'s {len(tree.decision)} fresh interpreters "
                     f"exited 0 with no `{WALL_LINE_T}` line"
                     + (f" — {len(f)} finding(s): " + " | ".join(f) if f else ""))


# ═══════════════════════════════════════════════════════════════ F-HOOK-ESCAPE — leg (iv)
_ESC = ("import json, sys\n"
        "sys.path[:0] = sys.argv[1:]\n"
        f"import {SHIM_T} as E\n"
        "data = json.load(sys.stdin)\n"
        f"print({ESC_MARK!r} + json.dumps({{k: E.hook_escapes(v) for k, v in sorted(data.items())}}))\n")
_SP_IMPORT_RX = re.compile(r"HOOK-ESCAPE line [0-9]+: (import subprocess|from subprocess import)")


def hook_escapes(sources: dict) -> dict:
    """E.hook_escapes over {label: source text}, computed in ONE fresh interpreter under the shim
    (this suite's own process imports no shim)."""
    rc, text = _python(["-c", _ESC, str(SCRIPTS), str(ROOT)], stdin=json.dumps(sources))
    line = next((x for x in text.splitlines() if x.startswith(ESC_MARK)), None)
    if line is None:
        raise RuntimeError(f"the shim's hook_escapes did not answer (exit {rc})")
    return json.loads(line[len(ESC_MARK):])


def site_findings(name: str, src: str) -> list:
    """The ONE pinned subprocess call site of a SUBPROC_SITE_T module, and the verbs it may pass."""
    row = next(r for r in SUBPROC_SITE_T if r[0] == name)
    _, fn, heads, verbs = row
    tree = ast.parse(src)
    parents, out = _parents(tree), []
    uses = [n for n in ast.walk(tree) if isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name)
            and n.value.id == "subprocess"]
    calls = [parents[u] for u in uses if isinstance(parents.get(u), ast.Call) and parents[u].func is u]
    if len(calls) != 1 or _where(parents, calls[0]) != fn:
        out.append(f"SUBPROC-SITE {name}: {len(calls)} subprocess call site(s) in "
                   f"{sorted({_where(parents, c) for c in calls})} — not the one pinned site {name}.{fn}")
    out += [f"SUBPROC-SITE {name} line {u.lineno}: subprocess.{u.attr} referenced in {_where(parents, u)}(), "
            f"outside {fn}()" for u in uses if _where(parents, u) != fn]
    for c in calls:
        if any(k.arg == "shell" and not (isinstance(k.value, ast.Constant) and k.value.value is False)
               for k in c.keywords):
            out.append(f"SUBPROC-SITE {name} line {c.lineno}: shell= passed to subprocess")
        argv = c.args[0] if c.args else None
        consts = [x.value for x in ast.walk(argv) if _cstr(x) is not None] if argv is not None else []
        if isinstance(argv, (ast.List, ast.Tuple)) and argv.elts and _cstr(argv.elts[0]) is not None \
                and argv.elts[0].value not in heads:
            out.append(f"SUBPROC-VERB {name} line {c.lineno}: argv head {argv.elts[0].value!r} not in "
                       f"{list(heads)}")
        if heads == ("cp",) and not set(verbs) <= set(consts):
            out.append(f"SUBPROC-VERB {name} line {c.lineno}: the clone's argv lacks {list(verbs)}")
        if fn == "git_ro" and GIT_RO_FLAG_T not in consts:
            out.append(f"SUBPROC-VERB {name} line {c.lineno}: the read-only helper's argv lacks {GIT_RO_FLAG_T}")
    if heads != ("cp",):
        for n in ast.walk(tree):
            if isinstance(n, ast.Call) and _fn(n) == fn and isinstance(n.func, (ast.Name, ast.Attribute)) \
                    and _where(parents, n) != fn:
                argv = n.args[0] if n.args else None
                elts = argv.elts if isinstance(argv, (ast.List, ast.Tuple)) else None
                verb = next((x.value for x in elts or [] if _cstr(x) is not None
                             and not x.value.startswith("-") and x.value not in heads), None)
                if elts is None:
                    out.append(f"SUBPROC-VERB {name} line {n.lineno}: {fn}(…) is handed a non-literal argv")
                elif elts and _cstr(elts[0]) is None and INTERPRETER_T in heads:
                    continue                    # the interpreter's argv (its head is sys.executable, by object)
                elif verb not in verbs:
                    out.append(f"SUBPROC-VERB {name} line {n.lineno}: {fn}(…) passes the verb {verb!r}, outside "
                               f"{list(verbs)}")
    return out


def escape_findings(tree: Tree) -> list:
    typed = {r[0] for r in SUBPROC_SITE_T}
    found = hook_escapes({n: tree.src[n] for n in tree.glob})
    out = []
    for n in tree.glob:
        keep = [x for x in found[n] if not (n in typed and _SP_IMPORT_RX.match(x))]
        out += [f"{x} — in {n}" for x in keep]
        if n in typed:
            out += site_findings(n, tree.src[n])
    return out


def escape_break():
    tree = CTX["tree"]

    def shadow(tail: str):
        return lambda: added(escape_findings, plant({SHADOW: SHADOW_TEXT + tail}))

    rows = [
        ("`pq.read_table(` in a copy", "HOOK-ESCAPE",
         shadow("\n\ndef g(pq, p):\n    return pq.read_table(p)\n")),
        ("`os.system(` in a copy", "HOOK-ESCAPE", shadow("import os\n\n\ndef g():\n    return os.system(\"true\")\n")),
        ("a `subprocess.run` in a builder copy, outside SUBPROC_SITE_T", "HOOK-ESCAPE",
         shadow("import subprocess\n\n\ndef g():\n    return subprocess.run([\"true\"])\n")),
    ]
    attest = SUBPROC_SITE_T[1][0]
    if attest in tree.names:
        rows.append(("`git push` through the attestation helper", "SUBPROC-VERB",
                     lambda: added(escape_findings, plant({attest: tree.src[attest] + "\n\ndef planted():\n"
                                                           "    return git([\"push\", \"origin\"])\n"}))))
    return FX.plants(rows)


def escape_real():
    tree = CTX["tree"]
    f = escape_findings(tree)
    sites = " · ".join(f"{m}.{fn} {'on file' if m in tree.names else 'not yet filed'}"
                       for m, fn, _, _ in SUBPROC_SITE_T)
    return (not f), (f"E.hook_escapes over the {len(tree.glob)} GLOB member(s) finds no pyarrow-native I/O and no "
                     f"os-level out-of-process call; subprocess appears only at the typed call sites "
                     f"SUBPROC_SITE_T [{sites}], one pinned site each, verbs inside the typed sets"
                     + (f" — {len(f)} finding(s): " + " | ".join(f) if f else ""))


# ═══════════════════════════════════════════════════════════════ F-WALL — leg (v)
def _code_only(source: str) -> str:
    return " ".join(t.string for t in tokenize.generate_tokens(io.StringIO(source).readline)
                    if t.type not in (tokenize.STRING, tokenize.COMMENT))


def wall_findings(pkg: Path, va, init_sha) -> list:
    """Leg (v) on one analytics directory (the package of record, or a scratch copy) and on the
    value-area module's text `va` (None: not yet filed)."""
    out = []
    init = (pkg / "__init__.py").read_text(encoding="utf-8")
    if init_sha is None or FX.sha_bytes((pkg / "__init__.py").read_bytes()) != init_sha:
        out.append(f"WALL-INIT: {ANALYTICS_T}/__init__.py is not the census's bytes")
    if WALL_ATTRS_T[0] in init:
        out.append(f"WALL-INIT: {ANALYTICS_T}/__init__.py holds a `{WALL_ATTRS_T[0]}` token")
    modules = tuple(FX.literal_from_text(init, "_MODULES"))
    if VA_MODULE_NAME_T in modules:
        out.append(f"WALL-MODULES: {VA_MODULE_NAME_T} is in `_MODULES`")
    h = hashlib.sha256()
    for name in modules:
        if (pkg / name).exists():
            h.update(name.encode("utf-8"))
            h.update((pkg / name).read_bytes())
    printed = re.search(r"`analytics_sha\(\)` = `([0-9a-f]+)`", (pkg / "INTERFACE.md").read_text(encoding="utf-8"))
    if printed is None or printed.group(1) != h.hexdigest():
        out.append("WALL-SHA: analytics_sha() recomputed by this fixture's own loop != the value printed in "
                   f"{ANALYTICS_T}/INTERFACE.md")
    if va is None:
        return out
    for _, m in imported_names(ast.parse(va)):
        root = m.split(".")[0]
        if root in sys.stdlib_module_names and root not in VA_IMPORTS_T:
            out.append(f"WALL-IMPORT: {VA_MODULE_REL} imports the stdlib module {root}, outside VA_IMPORTS_T")
        elif root not in sys.stdlib_module_names and root not in VA_THIRD_PARTY_T:
            out.append(f"WALL-IMPORT: {VA_MODULE_REL} imports {m} — numpy is its only non-stdlib import")
    if re.search(r"^\s*(from|import)\s+engine\b", va, re.M):
        out.append(f"WALL-ENGINE: {VA_MODULE_REL} imports engine")
    body = _code_only(va)
    out += [f"WALL-IO: {VA_MODULE_REL} holds the banned token `{t}`" for t in WALL_BANNED_T if t in body]
    if re.search(r"\bopen\s*\(", body):
        out.append(f"WALL-IO: {VA_MODULE_REL} holds an `open(` call")
    return out


def _pkg_copy(over: dict) -> Path:
    d = Path(tempfile.mkdtemp(prefix="pkg_", dir=CTX["scratch"]))
    for p in sorted((ROOT / ANALYTICS_T).iterdir()):
        if p.is_file():
            shutil.copy2(p, d / p.name)
    for name, text in over.items():
        (d / name).write_text(text, encoding="utf-8")
    return d


VA_SHADOW_TEXT = ('"""a shadow value-area module (planted)."""\nfrom __future__ import annotations\n\n'
                  "import math\n\nimport numpy as np\n\n\ndef f(*, x):\n    return np.asarray(x) * math.pi\n")


def wall_break():
    pkg = ROOT / ANALYTICS_T
    sha = census_sha(f"{ANALYTICS_T}/__init__.py")
    va = va_text() or VA_SHADOW_TEXT
    init = (pkg / "__init__.py").read_text(encoding="utf-8")
    return FX.plants([
        ("`import engine` planted in a value_area.py copy", "WALL-ENGINE",
         lambda: wall_findings(pkg, scratch_text("va.py", va + "\nimport engine\n"), sha)),
        ("a `read_parquet` call planted in a value_area.py copy", "WALL-IO",
         lambda: wall_findings(pkg, scratch_text("va.py", va + "\n\ndef g(pd, p):\n    return pd.read_parquet(p)\n"),
                               sha)),
        ("`import json` (stdlib, outside VA_IMPORTS_T) planted in a value_area.py copy", "WALL-IMPORT",
         lambda: wall_findings(pkg, scratch_text("va.py", va + "\nimport json\n"), sha)),
        ("`value_area.py` added to a copy of `_MODULES` (the sha moves)", "WALL-MODULES",
         lambda: wall_findings(_pkg_copy({"__init__.py": mut(init, '"nesting.py")', '"nesting.py", '
                                                             f'"{VA_MODULE_NAME_T}")')}), va, sha)),
    ])


def wall_real():
    f = wall_findings(ROOT / ANALYTICS_T, va_text(), census_sha(f"{ANALYTICS_T}/__init__.py"))
    return (not f), (f"{ANALYTICS_T}/__init__.py is the census's bytes, holds no `{WALL_ATTRS_T[0]}` token, "
                     f"`_MODULES` lacks {VA_MODULE_NAME_T}, and analytics_sha() recomputed by this fixture's own "
                     f"loop == the value printed in {ANALYTICS_T}/INTERFACE.md; {VA_MODULE_REL}: "
                     + (f"numpy is its only non-stdlib import, its stdlib imports are inside {list(VA_IMPORTS_T)}, "
                        f"no engine import, none of {list(WALL_BANNED_T)} and no open( call in its code"
                        if va_text() is not None else "not yet filed — its clauses bind from the record that files it")
                     + (f" — {len(f)} finding(s): " + " | ".join(f) if f else ""))


# ═══════════════════════════════════════════════════════════════ THE ROLL
REG_FIXTURES = (
    ("F-TYPED", "no number typed that a file can supply — the AST scan of every computation module [L-0.17]",
     "a 0.25, a float(\"1.5\"), a `2 + 1`, a literal default, an extra units row or a process tool importing "
     "numpy is planted in a scratch copy and the scan finds nothing",
     "a computation module in scope holds a numeric literal that none of (A), (B), (F), (G) permits or violates "
     "(C)-(E), tierc12_units differs from UNITS_T, or a process tool's exemption is unearned",
     typed_break, typed_real),
    ("F-SEED", "every ruler is handed the tier seed explicitly [L-0.2]",
     "a ruler call with no seed=, with a literal seed, with a positional seed, with E.SEED_SENS, or with a "
     "seed read from an X record outside X_SEED_MIRROR_T is planted in a scratch copy and passes",
     "a call of a ruler or of a TC12 wrapper of one omits its seed argument or passes a seed expression that "
     "does not resolve; the two list-seed controls do not stay GREEN",
     seed_break, seed_real),
    ("F-FX-MIRROR", "the harness is a COPY of the harness of record, AST-identical [L-0.14]",
     "`plants` in a harness copy counts a crash as a catch, a harness copy imports pandas, or the referee's "
     "text is bent, and the comparison passes",
     "ast.dump of say, clock, prove, plants or file_transcript in scripts/tierc12_fx.py differs from the same "
     "function parsed from the text of scripts/tierc11_closure_fixtures.py (its sha asserted from the census), "
     "or the harness imports anything outside the stdlib",
     mirror_break, mirror_real),
    ("F-FX-FORM", "every suite and every transcript of record holds the leg law's form [L-0.14]",
     "an empty break_if, a plants row with no detector, a break leg that is not a plants call, a not_run off "
     "the typed list, a suite without --root=, a default_rng off F's form, a network import, a harness list "
     "with a third FID, or a transcript copy missing a FAILS IF line, with a bad block id, a padded NOT RUN "
     "block or a short tally is planted and passes",
     "by AST over every scripts/tierc12_*_fixtures.py in scope a leg, a plants row, a not_run, the --root= "
     "parse, a default_rng seed or an import breaks the form; or a transcript of record has a block id outside "
     "the grammar, a PASS / FAIL block lacking a FAILS IF line, a NOT RUN block that is not its header and its "
     "line, or a tally not of C's form",
     form_break, form_real),
)
SHIM_FIXTURES = (
    ("F-CLOSURE [i]", "a fresh interpreter per decision module holds no door and no value-area module",
     "a builder copy importing a door, a book-module copy importing analytics.value_area, or a new shadow "
     "module reaching a door transitively is imported by a fresh interpreter and nothing is found",
     "after `import <module>` in a fresh interpreter sys.modules holds analytics.value_area, analytics.profile, "
     "a DOORS_T name or a forbidden name, or the module did not load from scripts/<name>.py",
     i_break, i_real),
    ("F-CLOSURE [i-b]", "the shim's exit check refuses a door reached at run time",
     "a shadow builder that imports a door lazily, or a shadow module that imports analytics.profile, exits 0, "
     "or a shim copy whose VA_WALL_DOORS lacks DOOR 2 equals the typed tuples",
     "the shim's VA_WALL_DOORS / VA_WALL_FIXTURES, read as text, differ from DOORS_T / VA_MODULE_FIXTURES_T, or "
     "a fresh interpreter of leg (i) does not exit 0 or logs BLOCKED:va-wall",
     ib_break, ib_real),
)
AST_FIXTURES = (
    ("F-CLOSURE [ii]", "the static import graph of every decision source, and the two L-D detectors",
     "a forbidden import in a function body, a door import in a function body, a dynamic import, exec, a "
     "sys.modules reach, a value_area attribute on the package alias, a .top read, a range or X import, a "
     "fourth TC10 lazy range import, a typed pin, a float tick compare or a reach outside the scope is planted "
     "in a scratch copy and the walk finds nothing",
     "a decision source, a door or a module of the static repo closure breaks a clause of leg (ii); the AST's "
     "set of TC10 lazy range imports differs from TC10_LAZY_RANGE_T; a reached TC10 module is not disclosed; "
     "the walk misses a repo module a fresh interpreter loaded; or a non-fixture source holds a pin as an int "
     "or ISO string, a tick literal, or a BinOp with a tick-named operand under a comparison",
     ii_break, ii_real),
    ("F-CLOSURE [iii]", "value-area facts are DATA: no name of the module, no reader on the blind list, doors earned",
     "a value-area name in a decision copy, the reader imported by a VA-blind copy, a va/ path in a VA-blind "
     "writer's READ_SET, a third importer of the module, a suite importing a door, an unearned door, a door "
     "that imports the module before the shim, a regbooks/ root or a net_r column is planted and passes",
     "a GLOB source outside DOORS_T holds a Name or Attribute of VA_NAMES_T; a VA_BLIND_T source imports the "
     "reader or the READ_SET of a directory it writes holds a path under va/; a door is unearned, does not "
     "import tierc12_env first, names a regbooks/ root, files a table with a TRADE_COLS_T column or is imported "
     "outside tierc12_va_fixtures; or a module not typed in DOORS_T imports analytics.value_area",
     iii_break, iii_real),
)
TAIL_FIXTURES = (
    ("F-HOOK-ESCAPE", "no I/O the audit hook cannot see; subprocess only at the four typed sites",
     "pq.read_table, os.system, an unlisted subprocess.run or `git push` through the attestation helper is "
     "planted in a scratch copy and the scan finds nothing",
     "E.hook_escapes finds pyarrow-native I/O or an os-level out-of-process call in a GLOB member, subprocess "
     "appears outside SUBPROC_SITE_T, or a typed module holds other than its one pinned call site and verbs",
     escape_break, escape_real),
    ("F-WALL", "analytics/value_area.py is numpy-only and performs no I/O; the package's sha is unmoved",
     "import engine, a read_parquet call or a stdlib I/O import planted in a value_area.py copy, or "
     "value_area.py added to a copy of _MODULES, passes",
     "value_area.py imports anything but numpy and VA_IMPORTS_T, imports engine, or holds a banned I/O token or "
     "an open( call; analytics/__init__.py moved or holds a value_area token; value_area.py is in _MODULES; or "
     "analytics_sha() recomputed differs from INTERFACE.md's",
     wall_break, wall_real),
)


def fixtures_of(stage: str) -> tuple:
    if not stage_at_least(stage, SHIM_STAGE_T):
        return REG_FIXTURES + AST_FIXTURES
    return REG_FIXTURES + SHIM_FIXTURES + AST_FIXTURES + TAIL_FIXTURES


def substrate_header(stage: str) -> dict:
    """The header's pin and snapshot name, read from Stage D's records once the stage has them."""
    if not stage_at_least(stage, SUBSTRATE_STAGE_T):
        return {}
    pin = json.loads((ROOT / TC12_PIN_REL).read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / STAGE_D_MANIFEST_REL).read_text(encoding="utf-8"))
    name = next((manifest[k] for k in SNAPSHOT_KEYS_T if isinstance(manifest.get(k), str)), None)
    if name is None:
        halt(f"{STAGE_D_MANIFEST_REL} names no snapshot (keys {sorted(manifest)})")
    return {"substrate": Path(name).name, "as_of_iso": pin["as_of_last_closed_4h"],
            "pin": pin["as_of_last_closed_4h_close_ms"]}


def typed_lines(stage: str, tree: Tree) -> list:
    rows = fixtures_of(stage)
    later = [r[0] for r in SHIM_FIXTURES + TAIL_FIXTURES if r not in rows]
    return [
        f"--stage={stage} · scope [L-0.11]: the scripts named by the records up to {stage} in RESUME_ORDER; at "
        f"the stage's own gate, before its record exists, the tierc12 scripts on disk that no record names",
        f"GLOB members in scope ({len(tree.glob)}): {tree.glob}",
        f"suites in scope ({len(tree.suites)}): {tree.suites}",
        f"contract fixture name `{CONTRACT_NAME_T}` (one of the {len(PINS.fixture_names())} names the pin door "
        f"parses from the FIXTURES line) -> FIDs {list(CONTRACT_FIDS_T)}; this run files "
        f"{[r[0] for r in rows if FX.fid_of(r[0]) in CONTRACT_FIDS_T]}"
        + (f"; {later} first run at {SHIM_STAGE_T} (they need the shim) and are no block of this transcript; "
           if later else "; ") + f"{CONTRACT_FIDS_T[3]} is the env suite's",
        f"the readings' additions hosted here, rolled after the contract's: {list(ADDED_FIDS_T)}",
        f"DOORS_T {list(DOORS_T)} · VA_MODULE_FIXTURES_T {list(VA_MODULE_FIXTURES_T)} · the reader {READER_T} "
        f"(a DECISION module, not a door)",
        f"VA_BLIND_T {list(VA_BLIND_T)}",
        f"FORBIDDEN exact {list(FORBIDDEN_EXACT_T)} + DOORS_T (decision modules) · substrings "
        f"{list(FORBIDDEN_SUBSTR_T)} · prefixes {list(FORBIDDEN_PREFIX_T)} (every GLOB member, doors included)",
        f"VA_NAMES_T {list(VA_NAMES_T)} · TRADE_COLS_T {list(TRADE_COLS_T)}",
        f"TC10_LAZY_RANGE_T {[f'{a}.{b}' for a, b in TC10_LAZY_RANGE_T]} · DYN_DECLARED_T "
        f"{[f'{a}.{b}' for a, b in DYN_DECLARED_T]}",
        "SUBPROC_SITE_T " + "; ".join(f"{m}.{fn}: {list(h)} {list(v)}" for m, fn, h, v in SUBPROC_SITE_T),
        f"VA_IMPORTS_T {list(VA_IMPORTS_T)} · exit check `{WALL_LINE_T}` exit {WALL_EXIT_T}",
        f"UNITS_T {UNITS_T} · structural {list(STRUCT_INTS_T)} {list(STRUCT_FLOATS_T)} · PROCESS_TOOLS_T "
        f"{list(PROCESS_TOOLS_T)} · RENDERERS_T {list(RENDERERS_T)}",
        f"RULERS_T {list(RULERS_T)} · X_SEED_MIRROR_T {[f'{a}.{b}' for a, b in X_SEED_MIRROR_T]} + the "
        f"F-VA-NULL stream builder of {list(X_SEED_MIRROR_UNNAMED_T)} (unnamed by the readings)",
        f"MIRRORED_T {list(MIRRORED_T)} · NOT_RUN_FIDS_T {list(NOT_RUN_FIDS_T)} · NETWORK_T {list(NETWORK_T)}",
    ]


def main() -> int:
    args = sys.argv[1:]
    stage = FX.opt(args, "--stage=")
    legal = PG.ORDER[PG.ORDER.index(FIRST_STAGE_T):]
    if stage not in legal:
        halt(f"--stage={stage!r}: this suite runs at the gate of an ORDER stage from {FIRST_STAGE_T} {legal}")
    at = FX.opt(args, "--at=")
    if at is not None and not re.fullmatch(r"[0-9a-f]+", at):
        halt(f"--at={at!r} is not a commit sha")
    if CONTRACT_NAME_T not in PINS.fixture_names():
        halt(f"the contract's FIXTURES line does not name `{CONTRACT_NAME_T}`")
    root = Path(FX.opt(args, "--root=", OUT))
    scope = build_scope(stage)
    CTX.update(stage=stage, scope=scope, seed=PINS.pin("seed"), tree=Tree(SCRIPTS, scope["names"]),
               scratch=tempfile.mkdtemp(prefix="tc12_closure_"), base={})
    for p in scope["unrecorded"]:
        FX.clock(f"UNRECORDED: {p} is on disk and no record names it")
    try:
        return FX.run_suite(
            args=args, root=root, transcript=f"FIXTURES_CLOSURE_{stage}.txt",
            banner=f"TIER-C12 CLOSURE FIXTURES at {stage} — the file-only wall (L-0.22), the typed-number scan "
                   f"(L-0.17), the seed law (L-0.2), the harness mirror and form (L-0.14) — break leg first, RED "
                   f"or void",
            seed=CTX["seed"], fixtures=fixtures_of(stage), typed=typed_lines(stage, CTX["tree"]),
            **substrate_header(stage))
    finally:
        shutil.rmtree(CTX["scratch"], ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
