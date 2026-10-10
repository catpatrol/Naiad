#!/usr/bin/env python
"""TIER-C12 · STAGE TC12-D — THE SUBSTRATE TOP-UP.  One pin, one frozen snapshot, one fee file.

Contract of record: exchange/queue/2026-10-08_TC12_APOLLO.md (lines 18-23), the resume paste
exchange/queue/2026-10-09_TC12_RESUME_APOLLO.md beside it (["mirror"], ["maker-bps"]).  Executor
HEPHAESTUS.  Readings of record: research_outputs/tierc12/LEANS.md, L-D.1 … L-D.24 (the pin, the
snapshot and its guard, the fetch scope, the run order, the extension rule, the forming-bar guard,
the derived lenses, funding, venue of record, the manifest and the port law, the fee pin, the tick
of record, the LaCie mirror); rulings O-7, O-8, O-19, O-20, O-26, O-27.

This module FETCHES and DESCRIBES.  It rides no book and computes no outcome of any kind.

WHY A NEW MODULE — THE PORT LAW [L-D.11].  scripts/tierc11_data.py and scripts/tierc10_data.py
HALT at import off their own snapshots, and neither snapshot may ever move.  The functions this
stage needs are PORTED from scripts/tierc11_data.py (read as TEXT, never imported).  Every ported
def carries a provenance comment naming its lines and the first 16 hex of the sha TC11's PROGRESS
certifies for that file, and one of three labels:
    VERBATIM   AST-identical to the function in scripts/tierc11_data.py.
    TEXT-ONLY  AST-identical once every string constant is blanked (messages, docstrings and
               filed sentences name TC12; no logic moves).
    CHANGED    the logic differs; the difference is named in the comment and in PORTS.
F-D-PORT (scripts/tierc12_data_fixtures.py) holds every label against the source.  A literal
inside a VERBATIM or TEXT-ONLY port is a QUOTATION of that source; every NEW number is READ from
the object that supplies it (the register at the head of LEANS section L-D): the pin from the
filed STEP Q record, TC11's and TC10's pins from TC11's pin record, the steps from engine.cells,
the module constants of scripts/tierc11_data.py by AST, the seed through the contract pin door,
the unit identities from scripts/tierc12_units.py, the tick from this stage's own capture.

WHAT IT DOES, IN ORDER (exactly one subcommand per invocation) [L-D.5]
  --clone     (alone, no guard) cp -cpR (APFS clonefile) ~/.cache/naiad/snapshots/tc11_20260925 to
              ~/.cache/naiad/snapshots/tc12_20261008 when the target does not exist, then re-hash
              EVERY cloned file against TC11's STAGE_D_MANIFEST.json (its own sha asserted against
              TC11's PROGRESS) and HALT on any mismatch -> CLONE_ATTEST.json (write-once).
  --pin       the pin DERIVED from the instant in progress/STEP_Q.json (the latest 4h bar closed
              when STEP Q was committed), held equal to the value O-7 prints, proven CLOSED on
              BOTH venue clocks (Binance: closeTime of the pinned bar < serverTime; Bybit: the
              pinned bar served, the envelope clock past the pin); the latest closed 4h at the run
              filed beside it -> AS_OF_PIN.json (write-once) + kind='clock' rows.
  --fetch     CONTRACT_SPECS.json (the TRADING check; the tick of record) -> PRE_STATE.json (all
              124 in-scope files BEFORE the first fetch) -> EDGE_AUDIT.json (the seam bar,
              read-only) -> FEE_SOURCE.json + the two fee-page bodies (no parsing) -> the
              extension, REST ONLY, each tape from ITS OWN edge + one step to the last bar closing
              <= the pin: 4h, 12h, 1h; funding; 15m (CLASSIC5); 5m -> FLAT_BAR_ATTEST.json (the
              venue re-asked for the seeded 5m flat-bar sample and every zero-volume flat bar among
              the rows this stage added; nothing it fetches is saved to a tape).
              Every HTTP request is one kind='http' row of FETCH_LOG.jsonl.
  --derive    1d / 1w re-derived WHOLE from the extended native 4h [TC10 LEAN L1].
  --seal      WRITE_ONCE_SEAL.json: the seven provenance records' bytes + the fetch log's line prefix.
  --manifest  [--out DIR]  No network, no snapshot write, no clock call.  STAGE_D_MANIFEST.json /
              .md, fee_schedule.json and TICK_GRID_AUDIT.json (THE DETERMINISM SET).  The fee
              extraction runs here; it HALTs while a venue captured with HTTP 200 has no grammar
              of record in FEE_GRAMMAR.json.
  --mirror    a sha-verified plain copy of the sealed snapshot and the fee-source bodies to
              /Volumes/LaCie/Naiad/{snapshots,provenance}/tc12_20261008/ when the drive is
              reachable -> MIRROR_ATTEST.json; "MIRROR NOT RUN" (exit 2, nothing written to the
              drive, nothing waits on it) when it is not [L-D.24, the paste's "mirror"].
  --all       pin, clock rows, fetch, derive, seal, manifest (it SEALS BEFORE it describes).

WHAT WOULD MAKE THIS WRONG: reading or writing the live cache; writing the TC10 or the TC11
snapshot; starting a fetch at or before a file's PRE_STATE edge (engine.data._save_cache keeps the
NEW row at an identical open_time, so an early start would overwrite an inherited bar — on seven
stems the inherited history is archive-assembled and differs from REST on incident bars); saving a
bar that is not closed at the pin; calling a derived day "native"; a typed pin, tick or maker
rate; a wall clock in the determinism set.

Run:  export NAIAD_CACHE_DIR="$HOME/.cache/naiad/snapshots/tc12_20261008" PYTHONDONTWRITEBYTECODE=1
      ~/venvs/naiad/bin/python -B /Users/luis/Naiad/scripts/tierc12_data.py --all
      (--clone alone needs no NAIAD_CACHE_DIR)
Exit: 0 complete · 2 fetch incomplete, or the mirror not run (a re-run resumes) · 1 HALT.
"""
from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import zipfile
import zlib
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT_NAME = "tc12_20261008"               # asserted == "tc12_" + the pin's UTC date [L-D.3]
SNAPSHOTS = Path.home() / ".cache" / "naiad" / "snapshots"
SNAPSHOT = SNAPSHOTS / SNAPSHOT_NAME
TC11_SNAPSHOT = SNAPSHOTS / "tc11_20260925"
TC10_SNAPSHOT = SNAPSHOTS / "tc10_20260921"
LIVE_CACHE = Path.home() / ".cache" / "naiad" / "data_cache"


# ported from scripts/tierc11_data.py:87-117 @ sha256 b2fe090f4a6cefe4 — CHANGED: refuses the TC11 snapshot too; the one substrate it admits is TC12's
def guard_substrate(env: str | None) -> Path:
    """THE FROZEN-SUBSTRATE GUARD [L-D.3].  Runs at import, BEFORE engine.data or any tier module
    can bind a cache path (every subcommand but --clone).

    HALTS IF: NAIAD_CACHE_DIR is unset; is not an absolute path AS GIVEN (a '~' or a relative
    value: engine.data binds Path(env) with no expansion and mkdirs it); names the live cache, the
    TC10 snapshot or the TC11 snapshot (tested on the path STRING first, then resolved); is
    anything but the TC12 snapshot; or the TC12 snapshot has no klines/ directory.
    """
    if not env:
        raise SystemExit(f"HALT: NAIAD_CACHE_DIR is unset — TC12 reads and writes ONLY "
                         f"the snapshot {SNAPSHOT}")
    if os.path.expanduser(env) != env or not os.path.isabs(env):
        raise SystemExit(f"HALT: NAIAD_CACHE_DIR={env!r} is not an absolute path as given — "
                         "engine.data binds Path(env) with no '~' expansion, relative to the "
                         "working directory, so it would name another directory than this guard")
    norm = Path(os.path.normpath(env))
    for bad, why in ((LIVE_CACHE, "the LIVE cache — READ-NEVER, WRITE-NEVER"),
                     (TC10_SNAPSHOT, "the TC10 snapshot — frozen, WRITE-NEVER for TC12"),
                     (TC11_SNAPSHOT, "the TC11 snapshot — frozen, WRITE-NEVER for TC12")):
        if (norm == bad or bad in norm.parents or norm.resolve() == bad.resolve()
                or bad.resolve() in norm.resolve().parents):
            raise SystemExit(f"HALT: NAIAD_CACHE_DIR={norm} names {why}")
    got = norm.resolve()
    if got != SNAPSHOT.resolve():
        raise SystemExit(f"HALT: NAIAD_CACHE_DIR={got} is not the TC12 snapshot {SNAPSHOT}")
    if not (got / "klines").is_dir():
        raise SystemExit(f"HALT: the TC12 snapshot has no klines/ directory: {got}")
    return got


# --clone (alone) is the one entry point that must run before its target exists; everything else —
# including every importer of this module — is guarded before the first engine import.
_CLONE_ONLY = __name__ == "__main__" and sys.argv[1:] == ["--clone"]
if not _CLONE_ONLY:
    guard_substrate(os.environ.get("NAIAD_CACHE_DIR"))

import numpy as np                                                   # noqa: E402
import pandas as pd                                                  # noqa: E402
import requests                                                      # noqa: E402

sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from engine import data as ED                                        # noqa: E402
from engine.cells import INTERVAL_MS                                 # noqa: E402
import tierc2_rules as R2                                            # noqa: E402
import tierc12_pins as PINS                                          # noqa: E402  (the contract's door: stdlib only)
import tierc12_progress as PG                                        # noqa: E402  (certified(): stdlib only)
import tierc12_units as UNITS                                        # noqa: E402
from tierc12_tick import TickGrid                                    # noqa: E402

SEED = PINS.pin("seed")                       # the contract's seed, through the pin door [L-0.17]
TIER, STAGE = "TIER-C12", "TC12-D"
T12_REL = "research_outputs/tierc12"
T11_REL = "research_outputs/tierc11"
T10_REL = "research_outputs/tierc10"
DATA_REL = T12_REL + "/data"
OUT = ROOT / T12_REL / "data"
PROVENANCE = Path.home() / ".cache" / "naiad" / "provenance" / SNAPSHOT_NAME   # outside the repo and the snapshot
RANGE_PINS_SOURCE = ROOT / "engine" / "rangefinder.py"
CONTRACT_REL = PINS.CONTRACT_REL
RESUME_PASTE_REL = PG.RESUME_PASTE
LEANS_DOC = T12_REL + "/LEANS.md"
RULINGS_REL = T12_REL + "/ORCHESTRATOR_RULINGS.md"
STEP_Q_REL = T12_REL + "/progress/STEP_Q.json"
R0_REL = T12_REL + "/progress/TC12-R0.json"
STAMP_MAP_REL = T12_REL + "/close/TC11_STAMP_MAP.json"
X_MANIFEST_REL = T12_REL + "/x_rec/X_REC_MANIFEST.json"
X_FEE_REL = T12_REL + "/x_rec/tierc11x/data/tc11_rec/data/fee_schedule.json"

D11_REL = "scripts/tierc11_data.py"           # THE REFEREE of every port below (read as text)
D10_REL = "scripts/tierc10_data.py"
FX10_REL = "scripts/tierc10_data_fixtures.py"
ENV11_REL = "scripts/tierc11_env.py"
TB_REL = "scripts/tierc2_baseline.py"
D11_SRC = ROOT / D11_REL
TC10_SRC = ROOT / D10_REL


# ported from scripts/tierc11_data.py:150-162 @ sha256 b2fe090f4a6cefe4 — VERBATIM
def _main_tree(root: Path) -> Path:
    """The main working tree: `root` itself, or — in a linked worktree whose
    .git is a `gitdir:` file — the tree that owns .git/worktrees/<name>.
    TC10 records are read there by absolute path [L-0.3, L-F.3]."""
    g = root / ".git"
    if g.is_file():
        txt = g.read_text(encoding="utf-8").strip()
        if txt.startswith("gitdir:"):
            gd = Path(txt.split(":", 1)[1].strip())
            gd = gd if gd.is_absolute() else (root / gd).resolve()
            if gd.parent.name == "worktrees" and gd.parent.parent.name == ".git":
                return gd.parent.parent.parent
    return root


# TC10's records and the x_rec copies are gitignored, so a review worktree does not carry them:
# they are read by ABSOLUTE MAIN-TREE path.  In the main tree MAIN_TREE is ROOT and nothing moves.
MAIN_TREE = _main_tree(ROOT)
TC10_DATA = MAIN_TREE / T10_REL / "data"                              # READ-ONLY
TC10_MANIFEST = TC10_DATA / "STAGE_D_MANIFEST.json"
TC10_PROBE = TC10_DATA / "VENUE_PROBE.json"
TC10_PIN_FILE = TC10_DATA / "AS_OF_PIN.json"
TC10_STAGE_D_TABLE = MAIN_TREE / T10_REL / "close" / "S3_STAGE_D.md"  # "TC10's Stage D table" (contract :20)
TC11_DATA = ROOT / T11_REL / "data"                                   # READ-ONLY (tracked)
TC11_MANIFEST = TC11_DATA / "STAGE_D_MANIFEST.json"
TC11_PIN_FILE = TC11_DATA / "AS_OF_PIN.json"
TC11_SPECS = TC11_DATA / "CONTRACT_SPECS.json"
TC11_FEES = TC11_DATA / "fee_schedule.json"
TC11_PROGRESS = ROOT / T11_REL / "PROGRESS.json"


def halt(msg: str):
    raise SystemExit(f"HALT: {msg}")


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


# ═══════════════════════════════════════════════ THE CERTIFIED READS (no sha is typed here)
def tc11_progress() -> dict:
    """TC11's PROGRESS.json, its bytes held to the sha TC12's R0 census recorded for it
    (progress/TC12-R0.json `frozen_estate_shas_at_r0`), or to the stamped value
    close/TC11_STAMP_MAP.json names for it when that map reads `applied: true` [L-0.24].
    HALTS IF neither holds."""
    rel = T11_REL + "/PROGRESS.json"
    raw = TC11_PROGRESS.read_bytes()
    want = json.loads((ROOT / R0_REL).read_text(encoding="utf-8"))["frozen_estate_shas_at_r0"][rel]["sha256"]
    stamp = ROOT / STAMP_MAP_REL
    if stamp.exists():
        doc = json.loads(stamp.read_text(encoding="utf-8"))
        if doc.get("applied") is True:
            for m in doc.get("moved", []):
                if m.get("path") == rel:
                    want = m["sha256_after"]
    if sha_bytes(raw) != want:
        halt(f"{rel} does not hash to the sha TC12's R0 census (or the applied stamp map) holds for it")
    return json.loads(raw)


def tc11_certified(rel: str) -> str:
    """The sha256 TC11's PROGRESS certifies for a repo-relative path: the entry of the LAST stage
    of `stages[]` whose `artifact_shas` names it.  HALTS IF no stage names it."""
    sha = None
    for s in tc11_progress()["stages"]:
        e = s.get("artifact_shas", {}).get(rel)
        if e is not None:
            sha = e["sha256"] if isinstance(e, dict) else e
    if sha is None:
        halt(f"TC11's PROGRESS certifies no sha for {rel}")
    return sha


def tc11_read(rel: str) -> bytes:
    """The bytes of a TC11 record, held to the sha TC11's PROGRESS certifies.  HALTS IF moved."""
    raw = (ROOT / rel).read_bytes()
    if sha_bytes(raw) != tc11_certified(rel):
        halt(f"{rel} does not hash to the sha TC11's PROGRESS certifies")
    return raw


def tc12_record(record_id: str) -> tuple[dict, str]:
    """(a filed TC12 progress record, its sha256), the sha held equal to the `_record` entry
    TC12's merged PROGRESS.json carries for it.  HALTS IF they differ."""
    p = ROOT / T12_REL / "progress" / PG.record_name(record_id)
    raw = p.read_bytes()
    prog = json.loads((ROOT / T12_REL / "PROGRESS.json").read_text(encoding="utf-8"))
    hit = [s for s in prog["stages"] if s.get("stage") == record_id]
    if len(hit) != 1 or hit[0]["_record"]["sha256"] != sha_bytes(raw):
        halt(f"progress/{p.name} is not the bytes PROGRESS.json records for {record_id}")
    return json.loads(raw), sha_bytes(raw)


D11_SHA256 = tc11_certified(D11_REL)          # the sha every provenance comment below abbreviates
if sha_bytes(D11_SRC.read_bytes()) != D11_SHA256:
    halt(f"{D11_REL} is not the file TC11's PROGRESS certifies — the referee of the ports moved")


# ported from scripts/tierc11_data.py:187-204 @ sha256 b2fe090f4a6cefe4 — VERBATIM
def pin_literal(path: Path, table: str, key: str):
    """ONE pin READ out of the literal table `table` in the SOURCE of `path` —
    never typed here, and never IMPORTED: this module is imported for
    load_asof / panel, and an import of the range machine at this level would
    put it in the closure of every module that does so (the v6 path must stay
    range-free).  F-D-ADMIT holds the value read here against the live object.

    HALTS IF: the table is not a plain literal in that source, or lacks the key.
    """
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
        if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == table for t in node.targets):
            try:
                return ast.literal_eval(node.value)[key]
            except (ValueError, KeyError) as e:
                raise SystemExit(f"HALT: {path.name}:{table}[{key!r}] is not a readable "
                                 f"literal pin ({e!r})")
    raise SystemExit(f"HALT: no literal table {table} in {path}")


# ported from scripts/tierc11_data.py:207-219 @ sha256 b2fe090f4a6cefe4 — VERBATIM
def source_literal(path: Path, name: str):
    """ONE module-level literal READ out of another module's SOURCE — never
    imported (tierc10_data HALTs at import off its own snapshot) and never
    retyped.  Returns (value, first_line, last_line).
    HALTS IF: the name is absent at module level or is not a literal."""
    for node in ast.parse(path.read_text(encoding="utf-8")).body:
        if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == name for t in node.targets):
            try:
                return ast.literal_eval(node.value), node.lineno, node.end_lineno
            except ValueError as e:
                raise SystemExit(f"HALT: {path.name}:{name} is not a literal ({e!r})")
    raise SystemExit(f"HALT: no module-level {name} in {path}")


def source_arith(path: Path, name: str, seen: tuple = ()):
    """ONE module-level constant READ out of another module's SOURCE where its right-hand side is
    integer arithmetic over literals and other module-level names of that source (`WEEK_MS = 7 *
    DAY_MS`): evaluated by a walk of the syntax tree — never imported, never retyped, never handed
    to an evaluator.  A plain literal (a number, a string, a dict display) is returned as it is.
    HALTS IF the name is absent, refers to itself, or holds anything but + - * // over those."""
    if name in seen:
        halt(f"{path.name}:{name} refers to itself")
    ops = {ast.Add: lambda a, b: a + b, ast.Sub: lambda a, b: a - b,
           ast.Mult: lambda a, b: a * b, ast.FloorDiv: lambda a, b: a // b}

    def walk(node):
        if isinstance(node, ast.Constant):
            return node.value
        if isinstance(node, ast.Name):
            return source_arith(path, node.id, seen + (name,))
        if isinstance(node, ast.BinOp) and type(node.op) in ops:
            return ops[type(node.op)](walk(node.left), walk(node.right))
        halt(f"{path.name}:{name} holds {type(node).__name__} — not literal arithmetic")

    for node in ast.parse(path.read_text(encoding="utf-8")).body:
        if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == name for t in node.targets):
            try:
                return ast.literal_eval(node.value)
            except ValueError:
                return walk(node.value)
    halt(f"no module-level {name} in {path}")


def d11_const(name: str):
    """A module-level constant of scripts/tierc11_data.py, read by AST [the register of L-D]."""
    return source_arith(D11_SRC, name)


MS_1H = INTERVAL_MS["1h"]
MS_4H = INTERVAL_MS["4h"]
DAY_MS = d11_const("DAY_MS")
WEEK_MS = d11_const("WEEK_MS")
MONDAY_EPOCH_OFFSET_MS = d11_const("MONDAY_EPOCH_OFFSET_MS")          # 1970-01-05 was a Monday
if d11_const("MS_1H") != MS_1H or d11_const("MS_4H") != MS_4H or DAY_MS % MS_4H or WEEK_MS % DAY_MS:
    halt("the steps read from scripts/tierc11_data.py disagree with engine.cells.INTERVAL_MS")

KLINE_COLS = list(ED.KLINE_COLS)
FUNDING_COLS = list(ED.FUNDING_COLS)
NATIVE_IVS = d11_const("NATIVE_IVS")          # fetched, venue-native, all 17
FIFTEEN = d11_const("FIFTEEN")                # fetched, venue-native, CLASSIC5 only
DERIVED_IVS = d11_const("DERIVED_IVS")        # derived from native 4h [TC10 LEAN L1]
LENS_ORDER = d11_const("LENS_ORDER")
# ported from scripts/tierc11_data.py:235-236 @ sha256 b2fe090f4a6cefe4 — CHANGED: the 15m step is read from engine.cells.INTERVAL_MS, not typed
STEP_MS = {**{iv: INTERVAL_MS[iv] for iv in NATIVE_IVS}, FIFTEEN: INTERVAL_MS[FIFTEEN],
           "1d": DAY_MS, "1w": WEEK_MS}
GRID_ANCHOR_MS = {"1w": MONDAY_EPOCH_OFFSET_MS}     # every other lens: 0
AUDIT_LENSES = ("5m", "1h")                   # the lenses of the on-grid audit [L-D.22]
PRICE_FIELDS = ("open", "high", "low", "close")

FUNDING_JITTER_MS = d11_const("FUNDING_JITTER_MS")
MEM_TTL_BARS = int(pin_literal(RANGE_PINS_SOURCE, "PINS_V2", "MEM_TTL_BARS"))
ADMISSION_MIN_4H = int(R2.TIDE_SLOW) + MEM_TTL_BARS

# ── the charter's tiered slippage, READ out of TC10's clause [scripts/tierc10_data.py, by AST]
CONTRACT_SLIPPAGE_CLAUSE, _CLAUSE_L1, _CLAUSE_L2 = source_literal(TC10_SRC, "CONTRACT_SLIPPAGE_CLAUSE")
CHARTER_SOURCE = ROOT / "Naiad_Phase0_Charter.md"
CHARTER_SLIPPAGE_NEEDLE = d11_const("CHARTER_SLIPPAGE_NEEDLE")
_TIER_RX = re.compile(r"tier ([A-Z]) \{([^}]*)\} (\d+)")


# ported from scripts/tierc11_data.py:253-267 @ sha256 b2fe090f4a6cefe4 — VERBATIM
def parse_slippage_clause(clause: str) -> dict:
    """The contract's slippage sentence -> {tier: {'bps': float, 'assets': (...)}}.
    READ, never typed.  HALTS IF the sentence carries no tier at all, or names
    one asset in two tiers."""
    tiers, seen = {}, {}
    for name, assets, bps in _TIER_RX.findall(clause):
        a = tuple(assets.split())
        for x in a:
            if x in seen:
                raise SystemExit(f"HALT: asset {x} is in tier {seen[x]} AND tier {name}")
            seen[x] = name
        tiers[name] = {"bps": float(bps), "assets": a}
    if not tiers:
        raise SystemExit(f"HALT: no tier found in the slippage clause: {clause!r}")
    return tiers


SLIPPAGE_TIERS = parse_slippage_clause(CONTRACT_SLIPPAGE_CLAUSE)
TIER_OF_ASSET = {a: t for t, b in SLIPPAGE_TIERS.items() for a in b["assets"]}

# ── the maker figure ON FILE: READ out of the README sentence, never typed [L-D.18] ────
MAKER_SOURCE = ROOT / "README.md"
_MAKER_RX = re.compile(r"maker is (\d+(?:\.\d+)?)%")


# ported from scripts/tierc11_data.py:280-287 @ sha256 b2fe090f4a6cefe4 — VERBATIM
def read_maker_bps_side() -> tuple[float, int, str]:
    """(maker bps per side, README line, the line) — the only register the
    estate has for a maker rate (C map G4).  HALTS IF the sentence is gone."""
    for i, line in enumerate(MAKER_SOURCE.read_text(encoding="utf-8").splitlines(), 1):
        m = _MAKER_RX.search(line)
        if m:
            return round(float(m.group(1)) * 100.0, 6), i, line.strip()
    raise SystemExit(f"HALT: no 'maker is <x>%' sentence in {MAKER_SOURCE}")


MAKER_BPS_SIDE, MAKER_SOURCE_LINE, MAKER_SOURCE_TEXT = read_maker_bps_side()

# ── panels [TC10 LEAN L6] ─────────────────────────────────────────────────
CLASSIC5 = tuple(R2.UNIVERSE)
UNSEEN12, _U12_L1, _U12_L2 = source_literal(TC10_SRC, "UNSEEN12")


def d11_panel17() -> tuple:
    """The commission's seventeen stems in the commission's order — `CLASSIC5 + (<the twelve>)`,
    the twelve READ out of scripts/tierc11_data.py by AST.  HALTS IF the assignment has another form."""
    for node in ast.parse(D11_SRC.read_text(encoding="utf-8")).body:
        if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == "PANEL17" for t in node.targets):
            v = node.value
            if (isinstance(v, ast.BinOp) and isinstance(v.op, ast.Add)
                    and isinstance(v.left, ast.Name) and v.left.id == "CLASSIC5"):
                return CLASSIC5 + tuple(ast.literal_eval(v.right))
    halt(f"{D11_REL}: PANEL17 is not `CLASSIC5 + (<literal stems>)`")


# The commission's seventeen stems, in the order the orchestrator named them (TC10).  Resolved
# against TC10's venue of record (the table, the probe, TC11's manifest); a mismatch HALTs.
PANEL17 = d11_panel17()
ALT_VENUE_ASSETS = d11_const("ALT_VENUE_ASSETS")
BYBIT_STEM_SUFFIX = d11_const("BYBIT_STEM_SUFFIX")

BYBIT_BASE = d11_const("BYBIT_BASE")
BYBIT_IV = d11_const("BYBIT_IV")
BYBIT_PAGE = d11_const("BYBIT_PAGE")
BYBIT_FUNDING_PAGE = d11_const("BYBIT_FUNDING_PAGE")

CHUNK_BARS = d11_const("CHUNK_BARS")
WEIGHT_SOFT_CAP = d11_const("WEIGHT_SOFT_CAP")
RETRIES = d11_const("RETRIES")
ERA_CUT_MS = source_arith(ROOT / ENV11_REL, "ERA_CUT_MS")           # the last tuning instant (TC11's shim, by AST)


# ═══════════════════════════════════════════════ THE PIN, BY OBJECT [L-D.1; O-7]
STEP_Q_INSTANT_RX = re.compile(r"committed (\S+Z)")
STEP_Q_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
O7_RX = re.compile(r"\*\*O-7 THE PIN\.\*\*.*?close `(?P<ms>[0-9]+)` = \*\*(?P<iso>[0-9T:Z-]+)\*\*, "
                   r"(?P<bars>[0-9]+) 4h bars past TC11's pin", re.DOTALL)
EPOCH = datetime.fromtimestamp(0, timezone.utc)
PIN_DERIVATION_TEXT = (
    "instant = the ONE match of `committed (\\S+Z)` in progress/STEP_Q.json `one_line`, parsed "
    "%Y-%m-%dT%H:%M:%SZ as UTC; ct_ms = (instant - datetime.fromtimestamp(0, utc)) // "
    "timedelta(milliseconds=1); PIN = (ct_ms // MS_4H) * MS_4H — the largest multiple of the 4h step "
    "(engine.cells.INTERVAL_MS['4h']) that is <= the STEP Q commit instant; PIN_OPEN = PIN - MS_4H; "
    "asserted equal to the 13-digit value ORCHESTRATOR_RULINGS.md prints in O-7's paragraph, and "
    "(PIN - TC11's pin) // MS_4H to the bar count printed there")


def tc11_pin_record() -> dict:
    """TC11's write-once pin record (its sha held to TC11's PROGRESS): the SCORE EDGE of the tier
    (`as_of_last_closed_4h_close_ms`) and TC10's pin (`tc10_pin_close_ms`), by object."""
    return json.loads(tc11_read(T11_REL + "/data/AS_OF_PIN.json"))


def derive_pin(step_q: Path | None = None, rulings: Path | None = None) -> dict:
    """THE PIN, derived and never typed [L-D.1]: the close of the latest 4h bar that was closed
    when STEP Q was committed.  `step_q` / `rulings` default to the filed records (their shas held);
    a fixture hands scratch COPIES.  This function runs no git: F-D-PIN holds the instant equal to
    the committer time of the commit the record names.

    HALTS IF: the STEP Q record is not the bytes PROGRESS.json records; its `one_line` does not
    hold exactly one `committed <instant>Z`; the derived pin is not the value O-7 prints; or the
    4h bars past TC11's pin are not the count O-7 prints."""
    if step_q is None:
        doc, rec_sha = tc12_record("STEP Q")
        raw_rulings = PG.read_certified(RULINGS_REL, ROOT) if rulings is None else Path(rulings).read_bytes()
    else:
        raw = Path(step_q).read_bytes()
        doc, rec_sha = json.loads(raw), sha_bytes(raw)
        raw_rulings = (ROOT / RULINGS_REL).read_bytes() if rulings is None else Path(rulings).read_bytes()
    hits = STEP_Q_INSTANT_RX.findall(doc.get("one_line", ""))
    if len(hits) != 1:
        halt(f"progress/STEP_Q.json `one_line` holds {len(hits)} `committed <instant>Z` stamps, not exactly one")
    instant = datetime.strptime(hits[0], STEP_Q_FORMAT).replace(tzinfo=timezone.utc)
    ct_ms = (instant - EPOCH) // timedelta(milliseconds=1)
    pin_ms = (ct_ms // MS_4H) * MS_4H
    m = O7_RX.search(raw_rulings.decode("utf-8"))
    if m is None:
        halt(f"{RULINGS_REL}: O-7's printed pin is not found")
    tc11_pin = int(tc11_pin_record()["as_of_last_closed_4h_close_ms"])
    if int(m.group("ms")) != pin_ms:
        halt(f"pin != derivation from STEP Q: O-7 prints {m.group('ms')}, the STEP Q instant "
             f"{hits[0]} derives {pin_ms}")
    if int(m.group("bars")) != (pin_ms - tc11_pin) // MS_4H:
        halt(f"O-7 prints {m.group('bars')} 4h bars past TC11's pin; the derivation gives "
             f"{(pin_ms - tc11_pin) // MS_4H}")
    contract = doc["artifact_shas"][CONTRACT_REL]
    return {"pin_close_ms": pin_ms, "pin_open_ms": pin_ms - MS_4H, "ct_ms": ct_ms,
            "instant_iso": hits[0], "commit": doc.get("commit"),
            "record_path": STEP_Q_REL, "record_sha256": rec_sha,
            "contract_path": CONTRACT_REL, "contract_sha256": contract["sha256"],
            "contract_prefix_bytes": contract["bytes"],
            "o7_printed_ms": int(m.group("ms")), "o7_printed_iso": m.group("iso"),
            "o7_printed_bars_past_tc11_pin": int(m.group("bars"))}


_T11_PIN = tc11_pin_record()
TC11_PIN_CLOSE_MS = int(_T11_PIN["as_of_last_closed_4h_close_ms"])      # the SCORE EDGE [L-0.7]
TC10_PIN_CLOSE_MS = int(_T11_PIN["tc10_pin_close_ms"])
PIN_DERIVATION = derive_pin()
PIN_CLOSE_MS = PIN_DERIVATION["pin_close_ms"]
PIN_OPEN_MS = PIN_DERIVATION["pin_open_ms"]
if SNAPSHOT_NAME != "tc12_" + (EPOCH + timedelta(milliseconds=PIN_CLOSE_MS)).strftime("%Y%m%d"):
    halt(f"the snapshot name {SNAPSHOT_NAME} is not tc12_<the pin's UTC date>")
if not TC10_PIN_CLOSE_MS < TC11_PIN_CLOSE_MS < PIN_CLOSE_MS:
    halt("the three pins are not in order TC10 < TC11 < TC12")

LIVE_CACHE_BASIS = (
    "by construction (guard + _assert_bound), NOT MEASURED: guard_substrate HALTs at import unless "
    "NAIAD_CACHE_DIR is the TC12 snapshot (F-D-GUARD) and _assert_bound HALTs before every "
    "snapshot write unless engine.data.cache_dir() still resolves to it (F-D-BOUND); "
    "live_cache_touched keeps the bool of TC10's schema")
CONTENT_SHA_LAW = d11_const("CONTENT_SHA_LAW")

WARRANTY = ("these files are described AS OF the pinned last closed 4h bar named "
            "here and of no other; bars stamped after it are counted, never read "
            "[TC6V-a, carried by TIER-C12]")

LOG_LINES: list[str] = []


def now_iso() -> str:
    """The wall clock, to the second — for PROVENANCE records only; never reached from --manifest."""
    return datetime.now(timezone.utc).strftime(STEP_Q_FORMAT)


# ported from scripts/tierc11_data.py:393-395 @ sha256 b2fe090f4a6cefe4 — VERBATIM
def log(msg: str = "") -> None:
    print(msg, flush=True)
    LOG_LINES.append(msg)


# ported from scripts/tierc11_data.py:399-403 @ sha256 b2fe090f4a6cefe4 — VERBATIM
def iso(ms: int | float | None) -> str | None:
    if ms is None:
        return None
    return (datetime.fromtimestamp(int(ms) / 1000, tz=timezone.utc)
            .strftime("%Y-%m-%dT%H:%M:%SZ"))


# ported from scripts/tierc11_data.py:407-412 @ sha256 b2fe090f4a6cefe4 — VERBATIM
def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# ported from scripts/tierc11_data.py:416-425 @ sha256 b2fe090f4a6cefe4 — VERBATIM
def frame_sha(df: pd.DataFrame, cols: list[str]) -> str:
    """Content sha of a frame: the raw little-endian column bytes, in column
    order.  Parquet bytes move with the writer; these do not."""
    h = hashlib.sha256()
    h.update(f"{len(df)}|{','.join(cols)}".encode())
    for c in cols:
        a = df[c].to_numpy()
        a = a.astype(np.int64) if c.endswith("_time") else a.astype(np.float64)
        h.update(np.ascontiguousarray(a).tobytes())
    return h.hexdigest()


# ported from scripts/tierc11_data.py:429-434 @ sha256 b2fe090f4a6cefe4 — VERBATIM
def _dump(obj, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(obj, indent=2, sort_keys=True, default=str) + "\n",
                   encoding="utf-8")
    os.replace(tmp, path)


# ported from scripts/tierc11_data.py:438-444 @ sha256 b2fe090f4a6cefe4 — VERBATIM
def _dump_once(obj, path: Path) -> None:
    """WRITE-ONCE, in code: a provenance record that exists is never written
    again.  HALTS IF the file is already there."""
    if path.exists():
        raise SystemExit(f"HALT: {path.name} is WRITE-ONCE and already exists — "
                         f"refusing to overwrite {path}")
    _dump(obj, path)


# ported from scripts/tierc11_data.py:448-449 @ sha256 b2fe090f4a6cefe4 — VERBATIM
def kline_path(stem: str, iv: str, root: Path | None = None) -> Path:
    return (root or SNAPSHOT) / "klines" / f"{stem}_{iv}.parquet"


# ported from scripts/tierc11_data.py:453-454 @ sha256 b2fe090f4a6cefe4 — VERBATIM
def funding_path(stem: str, root: Path | None = None) -> Path:
    return (root or SNAPSHOT) / "funding" / f"{stem}.parquet"


# ported from scripts/tierc11_data.py:458-461 @ sha256 b2fe090f4a6cefe4 — VERBATIM
def target_last_open(iv: str, as_of_close_ms: int) -> int:
    """Open of the last bar of lens `iv` that is CLOSED at the AS_OF close."""
    step, anchor = STEP_MS[iv], GRID_ANCHOR_MS.get(iv, 0)
    return ((as_of_close_ms - step - anchor) // step) * step + anchor


# ported from scripts/tierc11_data.py:464-468 @ sha256 b2fe090f4a6cefe4 — VERBATIM
def lenses_of(stem: str) -> tuple[str, ...]:
    """The in-scope lenses of one stem: native 5m/1h/4h/12h + derived 1d/1w for
    all 17; 15m for CLASSIC5 only [L-0.2]."""
    return tuple(iv for iv in LENS_ORDER
                 if iv in NATIVE_IVS or iv in DERIVED_IVS or (iv == FIFTEEN and stem in CLASSIC5))


# ported from scripts/tierc11_data.py:471-477 @ sha256 b2fe090f4a6cefe4 — VERBATIM
def scope_paths() -> list[str]:
    """Every in-scope snapshot file, panel order then lens order (124)."""
    rels = []
    for stem in PANEL17:
        rels += [f"klines/{stem}_{iv}.parquet" for iv in lenses_of(stem)]
        rels.append(f"funding/{stem}.parquet")
    return rels


# ported from scripts/tierc11_data.py:480-483 @ sha256 b2fe090f4a6cefe4 — VERBATIM
def split_rel(rel: str) -> tuple[str, str]:
    """'klines/MNTUSDT_BYBIT_5m.parquet' -> ('MNTUSDT_BYBIT', '5m')."""
    stem, _, iv = rel[len("klines/"):-len(".parquet")].rpartition("_")
    return stem, iv


# ported from scripts/tierc11_data.py:486-492 @ sha256 b2fe090f4a6cefe4 — TEXT-ONLY: the HALT names the TC12 snapshot
def _assert_bound() -> None:
    """Belt and braces before every snapshot write: engine.data's cache_dir()
    (read on every call) must still resolve to the TC12 snapshot.
    HALTS IF it does not."""
    got = Path(ED.cache_dir()).resolve()
    if got != SNAPSHOT.resolve():
        raise SystemExit(f"HALT: engine.data.cache_dir() = {got} — not the TC12 snapshot")


LEANS = (
    f"[LEAN-HEPHAESTUS] L-D.1 ({LEANS_DOC}) THE PIN: AS_OF = {iso(PIN_CLOSE_MS)} (close ms "
    f"{PIN_CLOSE_MS}), the latest 4h bar closed when STEP Q was committed "
    f"({PIN_DERIVATION['instant_iso']}); DERIVED from the filed STEP Q record, never typed, held "
    "equal to the value O-7 prints; proven closed on both venue clocks; write-once; every later "
    "read is by object.",
    f"[LEAN-HEPHAESTUS] L-D.3 SNAPSHOT: {SNAPSHOT_NAME} is an APFS clone (cp -cpR) of tc11_20260925; "
    "every cloned file is re-hashed against TC11's STAGE_D_MANIFEST before the first write "
    "(CLONE_ATTEST.json); it is extended over REST only. The live cache is never read or written "
    "and the TC10 and TC11 snapshots are never written.",
    "[LEAN-HEPHAESTUS] L-D.4 SCOPE: TC11's scope of record BY OBJECT (O-26): 17 stems x native "
    "{5m,1h,4h,12h} + CLASSIC5 x 15m + 17 x derived {1d,1w} + 17 funding tapes. A SUPERSET of the "
    "contract's list: the contract's 'twelve new assets 1h/4h/1d only' binds which lenses Stage V "
    "stamps, not which tapes the snapshot carries.",
    "[LEAN-HEPHAESTUS] L-D.6 ZERO OVERLAP: every tape is extended from ITS OWN edge + one step "
    "(engine.data._save_cache keeps the NEW row at an identical open_time, so an overlapping start "
    "would let REST overwrite an inherited bar). Gaps are counted and listed, never filled. The "
    "seam bar of every native file and the last inherited funding print of every tape are compared "
    "with the venue read-only (EDGE_AUDIT.json); a difference is disclosed, never repaired.",
    "[LEAN-HEPHAESTUS] L-D.7 FORMING BAR: the fetch target is a function of the pin alone; every "
    "reply is filtered to [lo, hi] before any save; each venue's clock is read and must be past the "
    "pin before its first kline request; every file ends exactly at its lens's last bar closing <= "
    "the pin.",
    "[LEAN-HEPHAESTUS] L-D.8 / TC10 L1 CARRIED: 1d = exactly six complete native-4h bars per UTC "
    "day; 1w = seven complete derived days, MONDAY-anchored UTC, complete weeks only; the source is "
    "native 4h, never 1h/5m aggregates, never a native 1d/1w fetch. A derived bar is a declared "
    "aggregate of venue bars that all exist — not a synthetic bar.",
    "[LEAN-HEPHAESTUS] L-D.9 / TC10 D-b, D-g CARRIED: funding is kept through AS_OF close + the "
    "jitter and a print belongs to the hour its stamp FLOORS to; the funding prefix is cut on the "
    "floor hour, never on the raw stamp.",
    "[LEAN-HEPHAESTUS] L-D.10 VENUE OF RECORD: TC10's Stage D table, TC10's VENUE_PROBE.json and "
    "TC11's manifest venues[] must agree row for row, 17 of 17; the venue of a tape is decided once "
    "and never re-probed. MNT's whole tape (klines and funding) is Bybit v5 linear, stem "
    "MNTUSDT_BYBIT, never spliced; PUMPFUN = PUMPUSDT.",
    "[LEAN-HEPHAESTUS] L-D.13 / L-D.16 FLAT BARS: a zero-volume flat bar is a bar the VENUE "
    "published during an outage — kept, counted, attributed to the venue from a sealed capture "
    "(FLAT_BAR_ATTEST.json), never removed, filled or altered. The claim is 'Naiad inserted no "
    "bar', not 'the venue published no flat bar'.",
    f"[LEAN-HEPHAESTUS] L-D.17-21 FEES: taker {float(R2.FEE_BPS_SIDE)} bps/side, "
    f"{float(R2.FEE_BPS_ROUND_TRIP)} round trip (tierc2_rules) — the toll of record of the "
    "TC-series, unchanged; the charter slippage tiers unchanged; maker_bps_side per VENUE is the "
    "venue's published entry-tier USDT-margined rate when its page is retrieved and parsed from "
    "saved bytes, else the figure on file (README) flagged NOT RE-CONFIRMED, applied to Bybit as an "
    "ASSUMPTION. No figure enters by keyboard.",
    "[LEAN-HEPHAESTUS] L-D.22-23 TICK: the tick of record is the price_tick STRING of this stage's "
    "own CONTRACT_SPECS.json capture — a point-in-time venue spec taken at the fetch run, applied "
    "over the whole corridor (O-20); TICK_GRID_AUDIT.json prints the on-grid shares and the "
    "observed granularity per calendar month and LISTS every month where the tape is coarser than "
    "the recorded tick (O-27).",
    "[LEAN-HEPHAESTUS] L-D.24 MIRROR: a sha-verified plain copy of the sealed snapshot to the LaCie "
    "by --mirror, filed under the non-blocking child record TC12-D.mirror; its status lives in "
    "MIRROR_ATTEST.json, never in this manifest.",
)


# ═══════════════════════════════════════════════ 0 · THE CLONE [L-D.3]
CLONE_ATTEST = "CLONE_ATTEST.json"


# ported from scripts/tierc11_data.py:499-506 (tc10_expected_shas) @ sha256 b2fe090f4a6cefe4 — CHANGED: the reference is TC11's manifest, its own sha held to TC11's PROGRESS
def tc11_expected_shas() -> dict[str, str]:
    """rel path -> sha256, for every file TC11's STAGE_D_MANIFEST.json pins
    (files[] that are present + out_of_scope_snapshot_files[]).  Read-only; the manifest's own
    bytes are held to the sha TC11's PROGRESS certifies."""
    man = json.loads(tc11_read(T11_REL + "/data/STAGE_D_MANIFEST.json"))
    exp = {f["path"]: f["sha256"] for f in man["files"] if f.get("present") and f.get("sha256")}
    for o in man["out_of_scope_snapshot_files"]:
        exp[o["path"]] = o["sha256"]
    return exp


# ported from scripts/tierc11_data.py:509-517 @ sha256 b2fe090f4a6cefe4 — VERBATIM
def tree_files(root: Path) -> list[str]:
    """Every regular file under root (hidden ones included), sorted rel paths."""
    out = []
    for d, _, names in os.walk(root):
        for n in names:
            q = Path(d) / n
            if q.is_file():
                out.append(q.relative_to(root).as_posix())
    return sorted(out)


# ported from scripts/tierc11_data.py:520-545 @ sha256 b2fe090f4a6cefe4 — TEXT-ONLY: the filed reference strings name TC11's manifest and snapshot
def clone_findings(root: Path, exp: dict[str, str], ref_root: Path) -> tuple[list[str], dict]:
    """Every file under `root` against its reference: TC11's manifest sha where
    the manifest pins it, else the same file's bytes under `ref_root`.
    FAILS IF a sha differs, a pinned file is missing, or the two trees differ."""
    faults, rows = [], {}
    have, ref = tree_files(root), tree_files(ref_root)
    if have != ref:
        faults.append(f"file sets differ: only in clone {sorted(set(have) - set(ref))[:5]}, "
                      f"only in source {sorted(set(ref) - set(have))[:5]}")
    for rel in sorted(set(exp) - set(have)):
        faults.append(f"{rel}: pinned by TC11's manifest but ABSENT")
    for rel in have:
        q = root / rel
        sha = file_sha256(q)
        if rel in exp:
            want, basis = exp[rel], "TC11 STAGE_D_MANIFEST.json"
        else:
            r = ref_root / rel
            want = file_sha256(r) if r.exists() else None
            basis = ("NOT in TC11's manifest — compared with the same file's bytes in the "
                     "TC11 snapshot (read-only)")
        rows[rel] = {"sha256": sha, "bytes": q.stat().st_size, "reference_sha256": want,
                     "reference": basis, "equal": sha == want}
        if sha != want:
            faults.append(f"{rel}: sha {sha[:12]} != reference {str(want)[:12]} ({basis[:26]})")
    return faults, rows


# ported from scripts/tierc11_data.py:548-602 @ sha256 b2fe090f4a6cefe4 — CHANGED: the source is the TC11 snapshot and the reference TC11's manifest (its sha held to TC11's PROGRESS)
def clone_snapshot(out: Path) -> dict:
    """cp -cpR (APFS clonefile) the TC11 snapshot to the TC12 path when the
    target does not exist, then re-hash every cloned file.  WRITE-ONCE record.

    HALTS IF: the target exists without a filed attestation (a snapshot of
    unknown provenance), an attestation exists without its snapshot, or any
    cloned file's sha differs from its reference."""
    p = out / CLONE_ATTEST
    if SNAPSHOT.exists():
        if p.exists():
            doc = json.loads(p.read_text(encoding="utf-8"))
            log(f"CLONE: {SNAPSHOT} exists; attestation filed {doc['cloned_wall_clock_utc']} "
                f"({doc['n_files']} files, all_equal={doc['all_equal']}) — not re-cloned")
            return doc
        raise SystemExit(f"HALT: {SNAPSHOT} exists but no {CLONE_ATTEST} was filed — a "
                         "snapshot of unknown provenance; refusing to adopt it")
    if p.exists():
        raise SystemExit(f"HALT: {p} is filed but {SNAPSHOT} is gone — refusing to re-clone "
                         "under a filed record")
    if not (TC11_SNAPSHOT / "klines").is_dir():
        raise SystemExit(f"HALT: the TC11 snapshot {TC11_SNAPSHOT} has no klines/")
    exp = tc11_expected_shas()                  # HALTs here, before the copy, if TC11's manifest moved
    out.mkdir(parents=True, exist_ok=True)
    SNAPSHOT.parent.mkdir(parents=True, exist_ok=True)
    started = now_iso()
    t0 = time.time()
    subprocess.run(["cp", "-cpR", str(TC11_SNAPSHOT), str(SNAPSHOT)], check=True)
    t1 = time.time()
    faults, rows = clone_findings(SNAPSHOT, exp, TC11_SNAPSHOT)
    log(f"CLONE: cp -cpR {TC11_SNAPSHOT} -> {SNAPSHOT} in {t1 - t0:.1f}s; "
        f"{len(rows)} files re-hashed in {time.time() - t1:.1f}s")
    if faults:
        for f in faults:
            log(f"  !! {f}")
        raise SystemExit(f"HALT: {len(faults)} cloned file(s) do not re-hash to TC11's record — "
                         "the clone is left in place for inspection; nothing was filed")
    doc = {
        "tier": TIER, "stage": STAGE, "seed": SEED,
        "source": str(TC11_SNAPSHOT), "target": str(SNAPSHOT),
        "method": "cp -cpR (APFS clonefile, permissions and times preserved)",
        "law": "every cloned file re-hashes to TC11's STAGE_D_MANIFEST.json (files[] + "
               "out_of_scope_snapshot_files[]) BEFORE any extension; a file the manifest does not pin "
               "is compared with its own bytes in the TC11 snapshot; the clone's file set equals the "
               "source tree's; any mismatch HALTs before anything is filed",
        "tc11_manifest": {"path": T11_REL + "/data/STAGE_D_MANIFEST.json",
                          "sha256": file_sha256(TC11_MANIFEST),
                          "certified_by": T11_REL + "/PROGRESS.json (artifact_shas)"},
        "n_files": len(rows),
        "n_pinned_by_tc11_manifest": sum(1 for r in rows if r in exp),
        "n_not_in_tc11_manifest": sorted(r for r in rows if r not in exp),
        "all_equal": all(v["equal"] for v in rows.values()),
        "cloned_wall_clock_utc": started,
        "files": rows,
    }
    _dump_once(doc, p)
    log(f"CLONE ATTESTED: {doc['n_files']} files, {doc['n_pinned_by_tc11_manifest']} pinned by "
        f"TC11's manifest, all_equal={doc['all_equal']} -> {p}")
    return doc


# ported from scripts/tierc11_data.py:605-609 @ sha256 b2fe090f4a6cefe4 — VERBATIM
def load_clone_attest(out: Path | None = None) -> dict:
    p = (out or OUT) / CLONE_ATTEST
    if not p.exists():
        raise SystemExit(f"HALT: no {CLONE_ATTEST} at {p} — run --clone first")
    return json.loads(p.read_text(encoding="utf-8"))


# ═══════════════════════════════════════════════ 1 · THE AS-OF PIN AND ITS VENUE PROOF [L-D.1, L-D.2]
# ported from scripts/tierc11_data.py:613-666 @ sha256 b2fe090f4a6cefe4 — VERBATIM
class CallLog:
    """EVERY HTTP request made inside the block — engine.data's included (it
    calls `requests.get` through the module attribute, which is patched here),
    retries included — is one kind='http' row of FETCH_LOG.jsonl."""
    counts: dict = {}

    def __init__(self, out: Path, phase: str):
        self.out, self.phase = out, phase

    def __enter__(self):
        self._orig = requests.get
        requests.get = self._get
        return self

    def __exit__(self, *exc):
        requests.get = self._orig
        return False

    @staticmethod
    def _items(r) -> int | None:
        try:
            j = r.json()
        except ValueError:
            return None
        if isinstance(j, list):
            return len(j)
        if isinstance(j, dict):
            res = j.get("result")
            if isinstance(res, dict) and isinstance(res.get("list"), list):
                return len(res["list"])
            if isinstance(j.get("symbols"), list):
                return len(j["symbols"])
        return None

    def _get(self, url, params=None, **kw):
        t0, r, err = time.time(), None, None
        try:
            r = self._orig(url, params=params, **kw)
            return r
        except Exception as e:                              # noqa: BLE001
            err = repr(e)
            raise
        finally:
            venue = ("BINANCE" if "binance" in url else "BYBIT" if "bybit" in url else "OTHER")
            CallLog.counts[venue] = CallLog.counts.get(venue, 0) + 1
            _fetch_log(self.out, {
                "kind": "http", "phase": self.phase, "venue": venue,
                "endpoint": urlparse(url).path,
                "params": {k: params[k] for k in sorted(params)} if params else {},
                "status": getattr(r, "status_code", None), "error": err,
                "elapsed_ms": int((time.time() - t0) * 1000),
                "used_weight_1m": (r.headers.get("x-mbx-used-weight-1m") if r is not None else None),
                "bybit_limit_status": (r.headers.get("X-Bapi-Limit-Status") if r is not None else None),
                "items": self._items(r) if r is not None else None})


WITNESS_SYMBOL = CLASSIC5[0]                   # the Binance witness of the pin proof [L-D.2]


def _close_time(row: list) -> int:
    """The closeTime of a Binance kline row — the statement below is scripts/tierc11_data.py's
    own (a quotation: the row index is the referee's)."""
    venue_close_ms = int(row[6])
    return venue_close_ms


# ported from scripts/tierc11_data.py:669-675 @ sha256 b2fe090f4a6cefe4 — CHANGED: the witness symbol is CLASSIC5[0], read from tierc2_rules.UNIVERSE
def _venue_4h_row(open_ms: int) -> list:
    rows = ED._get(ED.REST_BASE + "/fapi/v1/klines",
                   params={"symbol": WITNESS_SYMBOL, "interval": "4h",
                           "startTime": open_ms, "endTime": open_ms, "limit": 1}).json()
    if not rows or int(rows[0][0]) != open_ms:
        raise SystemExit(f"HALT: venue does not serve {WITNESS_SYMBOL} 4h open {iso(open_ms)}")
    return rows[0]


def bybit_symbol() -> str:
    """The symbol of the one alternate-venue stem (MNT's), from the venue table [L-D.10]."""
    alt = [a for a in panel_assets() if a["venue"] != "BINANCE_USDTM"]
    if len(alt) != 1:
        halt(f"the venue table holds {len(alt)} alternate-venue stems, not exactly one")
    return alt[0]["symbol"]


def bybit_pinned_bar(open_ms: int) -> tuple[list, object, object]:
    """ONE call: Bybit's 4h kline of the bar opening `open_ms` for MNT's symbol.  Returns (the
    rows served, the envelope's `time` field, retCode).  The envelope clock is the venue clock of
    the Bybit proof [L-D.2]; nothing here is saved to a tape."""
    j = ED._get(BYBIT_BASE + "/v5/market/kline",
                params={"category": "linear", "symbol": bybit_symbol(),
                        "interval": BYBIT_IV["4h"], "start": open_ms, "end": open_ms,
                        "limit": 1}).json()
    rows = (j.get("result") or {}).get("list") or []
    return rows, j.get("time"), j.get("retCode")


def prove_closed(pin_ms: int, server_ms: int, row: list, lrow: list,
                 bybit_rows: list, bybit_clock, bybit_ret=0) -> None:
    """THE VENUE PROOF [L-D.2], a pure function of the venues' answers (a fixture hands it stubbed
    ones).  Binance: the witness row is the pinned bar, its closeTime == pin - 1 and < serverTime.
    Bybit: exactly one row, its start == the pinned open, and pin < the envelope clock (Bybit rows
    carry no closeTime: closure is start + step <= pin < the venue clock).

    HALTS IF any of that fails; if the latest-at-run bar is not closed; or if the Bybit envelope
    carries no `time`, or one that is not an integer with as many digits as Binance's serverTime
    read in the same run (the unit check, with no typed constant)."""
    open_ms = pin_ms - MS_4H
    venue_close_ms = _close_time(row)
    if int(row[0]) != open_ms:
        halt(f"the venue's row opens {row[0]}, not the pinned open {open_ms}")
    if venue_close_ms >= server_ms:
        halt(f"pinned bar {iso(open_ms)} is still forming on the venue "
             f"(closeTime {venue_close_ms} >= serverTime {server_ms})")
    if venue_close_ms != pin_ms - 1:
        halt(f"the venue closes the pinned bar at {venue_close_ms}, not {pin_ms - 1}")
    if _close_time(lrow) >= server_ms:
        halt("the run-time latest 4h is not closed by the venue clock")
    if bybit_ret != 0:
        halt(f"bybit answered retCode {bybit_ret!r} for the pinned bar")
    if len(bybit_rows) != 1 or int(bybit_rows[0][0]) != open_ms:
        halt(f"bybit does not serve exactly the pinned 4h bar {iso(open_ms)}: {bybit_rows!r}")
    if type(bybit_clock) is not int or len(str(bybit_clock)) != len(str(server_ms)):
        halt(f"the bybit envelope `time` {bybit_clock!r} is absent or is not an integer in the unit "
             f"of Binance's serverTime ({server_ms})")
    if not pin_ms < bybit_clock:
        halt(f"the bybit clock {bybit_clock} is not past the pin {pin_ms} — the bar may be forming")


# ported from scripts/tierc11_data.py:678-710 @ sha256 b2fe090f4a6cefe4 — CHANGED: the pin is the DERIVATION (by object); the Bybit proof is checked; the key set is TC11's
def pin_findings(pin: dict, tc11_keys: set | None = None) -> list[str]:
    """Faults of a filed pin.  FAILS IF: the close is not the derivation from STEP Q
    or not a 4h close; open != close - 4h; the ISO strings disagree; the venue
    closeTime of the pinned bar is not close - 1 ms or is not before the venue
    clock; the filed venue kline is not that bar; the Bybit clock is not past the pin or its
    filed row is not the pinned bar; the seed is not the contract's; or a
    key of TC11's AS_OF_PIN schema is missing."""
    bad = []
    try:
        c, o = int(pin["as_of_last_closed_4h_close_ms"]), int(pin["as_of_last_closed_4h_open_ms"])
        vc, vs = int(pin["venue_close_time_of_pinned_bar_ms"]), int(pin["venue_server_time_ms"])
    except (KeyError, TypeError, ValueError) as e:
        return [f"pin unreadable: {e!r}"]
    if c != PIN_CLOSE_MS:
        bad.append(f"close {c} != the derivation from STEP Q {PIN_CLOSE_MS}")
    if c % MS_4H:
        bad.append(f"close {c} is not a 4h bar close (remainder {c % MS_4H} ms)")
    if o != c - MS_4H:
        bad.append(f"open {o} != close - 4h ({c - MS_4H})")
    if pin.get("as_of_last_closed_4h") != iso(c) or pin.get("as_of_last_closed_4h_open") != iso(o):
        bad.append("ISO strings disagree with the ms")
    if vc != c - 1:
        bad.append(f"venue closeTime {vc} != close - 1 ms ({c - 1})")
    if not vc < vs:
        bad.append(f"venue closeTime {vc} is not before the venue clock {vs} — still forming")
    k = pin.get("venue_kline_of_pinned_bar") or []
    if not (len(k) >= 7 and int(k[0]) == o and int(k[6]) == vc):
        bad.append("the filed venue kline row is not the pinned bar")
    by = pin.get("bybit_server_time_ms")
    if type(by) is not int or not c < by:
        bad.append(f"the bybit clock {by!r} is not past the pin {c}")
    bk = pin.get("bybit_kline_of_pinned_bar") or []
    if not bk or int(bk[0]) != o or pin.get("bybit_pin_bar_closed") is not True:
        bad.append("the filed bybit kline row is not the pinned bar, or it is not filed closed")
    if pin.get("seed") != SEED:
        bad.append(f"seed {pin.get('seed')} != {SEED}")
    miss = sorted((tc11_keys or set()) - set(pin))
    if miss:
        bad.append(f"TC11 AS_OF_PIN keys missing: {miss}")
    return bad


# ported from scripts/tierc11_data.py:713-714 (tc10_pin_keys) @ sha256 b2fe090f4a6cefe4 — CHANGED: the key set carried is TC11's pin record's
def tc11_pin_keys() -> set:
    return set(tc11_pin_record())


# ported from scripts/tierc11_data.py:719-793 @ sha256 b2fe090f4a6cefe4 — CHANGED: the pin by object (derived from STEP Q, never typed); proven on BOTH venue clocks; TC11's keys carried
def pin_as_of(out: Path) -> dict:
    """Write-once.  The pin is the DERIVATION of L-D.1, proven closed on each venue of record's
    own clock [L-D.2]; the latest closed 4h at run time is read off Binance's clock, its own kline
    fetched and proven closed, and filed beside the pin.

    HALTS IF: a venue does not serve the pinned bar, serves it still forming, or a filed pin has
    a fault.
    """
    p = out / "AS_OF_PIN.json"
    if p.exists():
        pin = json.loads(p.read_text(encoding="utf-8"))
        bad = pin_findings(pin, tc11_pin_keys())
        if bad:
            raise SystemExit(f"HALT: the filed pin has faults: {bad}")
        log(f"AS_OF (re-read, pinned {pin['pinned_wall_clock_utc']}): open "
            f"{pin['as_of_last_closed_4h_open']} close {pin['as_of_last_closed_4h']}")
        return pin
    out.mkdir(parents=True, exist_ok=True)
    open_ms = PIN_CLOSE_MS - MS_4H
    with CallLog(out, "pin"):
        server_ms = int(ED._get(ED.REST_BASE + "/fapi/v1/time").json()["serverTime"])
        local_ms = int(time.time() * 1000)
        row = _venue_4h_row(open_ms)
        latest_open = (server_ms // MS_4H) * MS_4H - MS_4H
        lrow = row if latest_open == open_ms else _venue_4h_row(latest_open)
        bybit_rows, bybit_clock, bybit_ret = bybit_pinned_bar(open_ms)
    prove_closed(PIN_CLOSE_MS, server_ms, row, lrow, bybit_rows, bybit_clock, bybit_ret)
    venue_close_ms = _close_time(row)
    q = PIN_DERIVATION
    pin = {
        "as_of_last_closed_4h_open_ms": open_ms,
        "as_of_last_closed_4h_open": iso(open_ms),
        "as_of_last_closed_4h_close_ms": open_ms + MS_4H,
        "as_of_last_closed_4h": iso(open_ms + MS_4H),
        "venue_server_time_ms": server_ms,
        "venue_server_time": iso(server_ms),
        "venue_close_time_of_pinned_bar_ms": venue_close_ms,
        "local_clock_skew_ms": local_ms - server_ms,
        "pinned_wall_clock_utc": iso(local_ms),
        "law": "AS_OF = the close of the latest 4h bar that was closed when the TIER-C12 contract's "
               f"STEP Q was committed ({q['instant_iso']}) [L-D.1, O-7]; DERIVED from the filed STEP Q "
               "record, never typed; proven closed by each venue of record's own clock; write-once; "
               "every fetch stops at bars closed by as_of_last_closed_4h",
        "seed": SEED,
        # ── the extra keys of TC11's schema (TC10's schema above is kept whole) ──
        "tier": TIER, "stage": STAGE,
        "pin_source": f"{LEANS_DOC} L-D.1; {STEP_Q_REL} sha256 {q['record_sha256']}; contract "
                      f"{CONTRACT_REL} sha256 {q['contract_sha256']} (its STEP Q prefix)",
        "venue_kline_of_pinned_bar": row,
        "venue_kline_endpoint": ED.REST_BASE + f"/fapi/v1/klines?symbol={WITNESS_SYMBOL}&interval=4h",
        "latest_closed_4h_at_pin_run_open_ms": latest_open,
        "latest_closed_4h_at_pin_run_open": iso(latest_open),
        "latest_closed_4h_at_pin_run_close_ms": latest_open + MS_4H,
        "latest_closed_4h_at_pin_run": iso(latest_open + MS_4H),
        "latest_closed_4h_at_pin_run_venue_close_time_ms": _close_time(lrow),
        "pin_equals_latest_closed_at_pin_run": latest_open == open_ms,
        "tc10_pin_close_ms": TC10_PIN_CLOSE_MS,
        "tc10_pin": iso(TC10_PIN_CLOSE_MS),
        "bars_4h_past_tc10_pin": (open_ms + MS_4H - TC10_PIN_CLOSE_MS) // MS_4H,
        # ── TC12's keys [L-D.1] ──
        "tc11_pin_close_ms": TC11_PIN_CLOSE_MS,
        "tc11_pin": iso(TC11_PIN_CLOSE_MS),
        "bars_4h_past_tc11_pin": (open_ms + MS_4H - TC11_PIN_CLOSE_MS) // MS_4H,
        "step_q": {"commit": q["commit"], "instant": q["ct_ms"], "instant_iso": q["instant_iso"],
                   "record_path": q["record_path"], "record_sha256": q["record_sha256"],
                   "contract_path": q["contract_path"], "contract_sha256": q["contract_sha256"]},
        "pin_derivation": PIN_DERIVATION_TEXT,
        "o7_printed": {"path": RULINGS_REL, "close_ms": q["o7_printed_ms"], "iso": q["o7_printed_iso"],
                       "bars_4h_past_tc11_pin": q["o7_printed_bars_past_tc11_pin"]},
        "bybit_server_time_ms": bybit_clock,
        "bybit_server_time": iso(bybit_clock),
        "bybit_kline_of_pinned_bar": bybit_rows[0],
        "bybit_kline_endpoint": BYBIT_BASE + f"/v5/market/kline?category=linear&symbol={bybit_symbol()}"
                                             f"&interval={BYBIT_IV['4h']}",
        "bybit_pin_bar_closed": True,
        "bybit_closure_law": "Bybit rows carry no closeTime: the bar is closed because start + 4h <= "
                             "pin < the venue clock in the v5 response envelope (`time`, ms)",
    }
    bad = pin_findings(pin, tc11_pin_keys())
    if bad:
        raise SystemExit(f"HALT: the pin about to be filed has faults: {bad}")
    _dump_once(pin, p)
    log(f"AS_OF PINNED: open {pin['as_of_last_closed_4h_open']} close "
        f"{pin['as_of_last_closed_4h']} (Binance clock {pin['venue_server_time']}, closeTime "
        f"of the bar {venue_close_ms} < serverTime {server_ms}: CLOSED; Bybit clock "
        f"{pin['bybit_server_time']} past the pin: CLOSED)")
    log(f"  latest closed 4h at run time: {pin['latest_closed_4h_at_pin_run']} "
        f"(== pin: {pin['pin_equals_latest_closed_at_pin_run']})")
    return pin


# ported from scripts/tierc11_data.py:796-801 @ sha256 b2fe090f4a6cefe4 — VERBATIM
def venue_latest_closed(out: Path) -> tuple[int, int]:
    """(venue clock ms, close ms of the latest closed 4h) — printed beside the
    pin on every networked run.  One /fapi/v1/time call, logged."""
    with CallLog(out, "clock"):
        server_ms = int(ED._get(ED.REST_BASE + "/fapi/v1/time").json()["serverTime"])
    return server_ms, (server_ms // MS_4H) * MS_4H


# ported from scripts/tierc11_data.py:804-823 @ sha256 b2fe090f4a6cefe4 — CHANGED: a Bybit clock row is filed too, and a venue clock at or before the pin HALTs (G3)
def record_fetch_clock(out: Path, pin: dict | None = None) -> tuple[int, int]:
    """[L-D.2] "the latest-at-fetch bar printed beside it" — PRINTED AND FILED.  One
    /fapi/v1/time call and one Bybit kline call for the pinned bar (their kind='http' rows), then
    one kind='clock' row PER VENUE of FETCH_LOG.jsonl carrying the venue clock and, for Binance,
    the close of the latest closed 4h it implies, beside the pin.  --all files them after the pin
    and BEFORE the fetch and the seal; --pin and --fetch file them too.

    HALTS IF (G3 of L-D.7) a venue's clock is not past the pin: no kline request may follow."""
    srv, latest = venue_latest_closed(out)
    row = {"kind": "clock", "venue": "BINANCE_USDTM", "venue_server_time_ms": srv,
           "venue_server_time": iso(srv),
           "latest_closed_4h_close_ms": latest, "latest_closed_4h": iso(latest)}
    with CallLog(out, "clock"):
        _, by, ret = bybit_pinned_bar(PIN_OPEN_MS)
    if ret != 0 or type(by) is not int or len(str(by)) != len(str(srv)):
        halt(f"the bybit envelope clock {by!r} (retCode {ret!r}) is not an integer in the unit of "
             f"Binance's serverTime")
    brow = {"kind": "clock", "venue": "BYBIT_V5_LINEAR", "venue_server_time_ms": by,
            "venue_server_time": iso(by)}
    if pin is not None:
        pinned = int(pin["as_of_last_closed_4h_close_ms"])
        row.update(pinned_close_ms=pinned, pinned=iso(pinned), latest_equals_pin=latest == pinned)
        brow.update(pinned_close_ms=pinned, pinned=iso(pinned), clock_past_pin=pinned < by)
    _fetch_log(out, row)
    _fetch_log(out, brow)
    log(f"  latest closed 4h at THIS run (Binance clock {iso(srv)}): {iso(latest)}"
        + (f" · pinned {iso(row['pinned_close_ms'])}" if pin is not None else "")
        + f" · Bybit clock {iso(by)} -> FETCH_LOG.jsonl kind=clock x 2")
    if not PIN_CLOSE_MS < srv or not PIN_CLOSE_MS < by:
        halt(f"a venue clock is not past the pin {PIN_CLOSE_MS} (Binance {srv}, Bybit {by}) — "
             "no kline may be asked of a venue whose clock has not passed the pin")
    return srv, latest


# ported from scripts/tierc11_data.py:827-831 @ sha256 b2fe090f4a6cefe4 — TEXT-ONLY: the HALT names tierc12_data
def load_pin(out: Path | None = None) -> dict:
    p = (out or OUT) / "AS_OF_PIN.json"
    if not p.exists():
        raise SystemExit(f"HALT: no AS_OF pin at {p} — run scripts/tierc12_data.py --pin first")
    return json.loads(p.read_text())


# ═══════════════════════════════════════════════ VENUE OF RECORD — three objects, one answer [L-D.10]
VENUE_TABLE_HEAD = ("asset", "venue", "symbol", "file stem")
VENUE_KEYS = ("asset", "venue", "symbol", "stem")


def stage_d_table(path: Path | None = None) -> list[dict]:
    """"TC10's Stage D table" (contract :20): the venue table of
    research_outputs/tierc10/close/S3_STAGE_D.md, parsed — its (asset, venue, symbol, file stem)
    columns, row by row.  HALTS IF no table with those four leading headers is found."""
    lines = (path or TC10_STAGE_D_TABLE).read_text(encoding="utf-8").splitlines()
    rows, live = [], False
    for line in lines:
        cells = [c.strip() for c in line.strip().strip("|").split("|")] if line.startswith("|") else None
        if cells is None:
            if live:
                break
            continue
        if not live:
            live = tuple(cells[:len(VENUE_TABLE_HEAD)]) == VENUE_TABLE_HEAD
            continue
        if set("".join(cells)) <= set("-: "):
            continue
        rows.append(dict(zip(VENUE_KEYS, cells)))
    if not rows:
        halt(f"no venue table (| {' | '.join(VENUE_TABLE_HEAD)} | …) in {TC10_STAGE_D_TABLE}")
    return rows


def venue_agreement(table: list[dict] | None = None, probe: dict | None = None,
                    tc11_venues: list[dict] | None = None) -> list[str]:
    """THE THREE-WAY AGREEMENT [L-D.10]: TC10's Stage D table, TC10's venue probe and TC11's
    manifest `venues[]` name the same (asset, venue, symbol, stem) row for row; the probe's sha is
    the one two tracked TC11 records carry for it.  Returns the disagreements ([] = agreed).  The
    arguments default to the filed objects; a fixture hands COPIES."""
    bad = []
    man = json.loads(tc11_read(T11_REL + "/data/STAGE_D_MANIFEST.json"))
    if probe is None:
        probe = json.loads(TC10_PROBE.read_text(encoding="utf-8"))
        sha = file_sha256(TC10_PROBE)
        specs = json.loads(tc11_read(T11_REL + "/data/CONTRACT_SPECS.json"))
        for what, want in (("TC11 CONTRACT_SPECS.json venue_of_record.sha256", specs["venue_of_record"]["sha256"]),
                           ("TC11 STAGE_D_MANIFEST.json tc10_record.venue_probe.sha256",
                            man["tc10_record"]["venue_probe"]["sha256"])):
            if sha != want:
                bad.append(f"VENUE_PROBE.json sha {sha[:12]} != {what} {want[:12]}")
    table = stage_d_table() if table is None else table
    tc11_venues = man["venues"] if tc11_venues is None else tc11_venues
    of_probe = [{k: a.get(k) for k in VENUE_KEYS} for a in probe["classic5"] + probe["unseen12"]]
    of_man = [{k: a.get(k) for k in VENUE_KEYS} for a in tc11_venues]
    if not (len(table) == len(of_probe) == len(of_man)):
        bad.append(f"table / probe / manifest disagree: {len(table)} / {len(of_probe)} / {len(of_man)} rows")
    for t, p, m in zip(table, of_probe, of_man):
        if not (t == p == m):
            bad.append(f"table / probe / manifest disagree on {t.get('asset')}: {t} / {p} / {m}")
    return bad


# ported from scripts/tierc11_data.py:834-841 @ sha256 b2fe090f4a6cefe4 — CHANGED: the three-way agreement of L-D.10 is required before the probe is used
def load_probe() -> dict:
    """TC10's venue of record, read-only [L-D.10].  HALTS IF TC10's Stage D table, the probe and
    TC11's manifest venues[] disagree on any row, or the probe's stems are not
    the commission's seventeen in the commission's order."""
    probe = json.loads(TC10_PROBE.read_text(encoding="utf-8"))
    bad = venue_agreement()
    if bad:
        raise SystemExit(f"HALT: venue of record: {bad}")
    stems = tuple(a["stem"] for a in probe["classic5"] + probe["unseen12"] if a.get("stem"))
    if stems != PANEL17:
        raise SystemExit(f"HALT: TC10's VENUE_PROBE resolves {stems}, not the commission's {PANEL17}")
    return probe


# ported from scripts/tierc11_data.py:844-846 @ sha256 b2fe090f4a6cefe4 — VERBATIM
def panel_assets() -> list[dict]:
    probe = load_probe()
    return [a for a in probe["classic5"] + probe["unseen12"] if a.get("stem")]


# ═══════════════════════════════════════════════ 2 · VENUE (Bybit) + FETCH HELPERS
# ported from scripts/tierc11_data.py:851-869 @ sha256 b2fe090f4a6cefe4 — VERBATIM
def _bybit_get(path: str, params: dict) -> dict:
    last = None
    for attempt in range(RETRIES):
        try:
            r = requests.get(BYBIT_BASE + path, params=params, timeout=30)
            if r.status_code == 200:
                j = r.json()
                if j.get("retCode") == 0:
                    left = r.headers.get("X-Bapi-Limit-Status")
                    if left is not None and int(left) < 20:
                        time.sleep(2.0)
                    return j["result"]
                last = RuntimeError(f"bybit retCode {j.get('retCode')} {j.get('retMsg')}")
            else:
                last = RuntimeError(f"bybit HTTP {r.status_code}")
        except requests.RequestException as e:
            last = e
        time.sleep(3.0 * (attempt + 1))
    raise RuntimeError(f"bybit failed after {RETRIES} attempts: {path} {params}") from last


# ported from scripts/tierc11_data.py:873-884 @ sha256 b2fe090f4a6cefe4 — VERBATIM
def _retry(fn, what: str):
    last = None
    for attempt in range(RETRIES):
        try:
            return fn()
        except (RuntimeError, requests.RequestException, ValueError,
                zipfile.BadZipFile) as e:
            last = e
            wait = 20.0 * (attempt + 1)
            log(f"    retry {attempt + 1}/{RETRIES} in {wait:.0f}s — {what}: {e!r}")
            time.sleep(wait)
    raise RuntimeError(f"gave up: {what}") from last


# ported from scripts/tierc11_data.py:888-898 @ sha256 b2fe090f4a6cefe4 — VERBATIM
def binance_brake() -> int:
    """Read the venue's own used-weight header (a 1-weight ping) and wait out
    the minute when past the soft cap.  engine.data sleeps between pages but
    never reads the header; a full-history 5m pull needs the brake."""
    r = ED._get(ED.REST_BASE + "/fapi/v1/ping")
    used = int(r.headers.get("x-mbx-used-weight-1m", 0))
    if used >= WEIGHT_SOFT_CAP:
        wait = 61.0 - (time.time() % 60.0)
        log(f"    weight {used} >= {WEIGHT_SOFT_CAP}: braking {wait:.0f}s")
        time.sleep(wait)
    return used


# ported from scripts/tierc11_data.py:902-905 @ sha256 b2fe090f4a6cefe4 — VERBATIM
def _fetch_log(out: Path, row: dict) -> None:
    row = {"wall_clock_utc": iso(time.time() * 1000), **row}
    with open(out / "FETCH_LOG.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(row, sort_keys=True) + "\n")


# ported from scripts/tierc11_data.py:909-913 @ sha256 b2fe090f4a6cefe4 — VERBATIM
def _edge(path: Path, col: str) -> int | None:
    if not path.exists():
        return None
    t = pd.read_parquet(path, columns=[col])[col]
    return int(t.max()) if len(t) else None


# ported from scripts/tierc11_data.py:917-921 @ sha256 b2fe090f4a6cefe4 — VERBATIM
def _assert_grid(df: pd.DataFrame, iv: str, what: str) -> None:
    off = (df["open_time"].to_numpy(np.int64) - GRID_ANCHOR_MS.get(iv, 0)) % STEP_MS[iv]
    if len(df) and (off != 0).any():
        raise SystemExit(f"HALT: {what}: venue served {int((off != 0).sum())} off-grid "
                         f"open_time(s) — refusing to save")


# ported from scripts/tierc11_data.py:925-946 @ sha256 b2fe090f4a6cefe4 — VERBATIM
def bybit_klines(symbol: str, iv: str, start_ms: int, end_ms: int) -> pd.DataFrame:
    """Bybit v5 linear klines, forward windows of one page each (the venue
    answers newest-first and caps at 1000, so the window IS the page)."""
    step, frames, cursor = STEP_MS[iv], [], start_ms
    while cursor <= end_ms:
        hi = min(cursor + (BYBIT_PAGE - 1) * step, end_ms)
        res = _bybit_get("/v5/market/kline",
                         {"category": "linear", "symbol": symbol,
                          "interval": BYBIT_IV[iv], "start": cursor, "end": hi,
                          "limit": BYBIT_PAGE})
        rows = res.get("list") or []
        if rows:
            df = pd.DataFrame([r[:6] for r in rows], columns=KLINE_COLS)
            df["open_time"] = df["open_time"].astype(np.int64)
            for c in KLINE_COLS[1:]:
                df[c] = df[c].astype(np.float64)
            frames.append(df.sort_values("open_time"))
        cursor = hi + step
        time.sleep(0.12)
    if not frames:
        return pd.DataFrame(columns=KLINE_COLS)
    return pd.concat(frames, ignore_index=True)


# ported from scripts/tierc11_data.py:950-974 @ sha256 b2fe090f4a6cefe4 — VERBATIM
def bybit_funding(symbol: str, start_ms: int, end_ms: int) -> pd.DataFrame:
    """Bybit v5 funding history, paged BACKWARD from end_ms (newest-first, 200
    a page; the endpoint refuses a bare startTime)."""
    frames, hi = [], end_ms
    while hi >= start_ms:
        res = _bybit_get("/v5/market/funding/history",
                         {"category": "linear", "symbol": symbol,
                          "startTime": start_ms, "endTime": hi,
                          "limit": BYBIT_FUNDING_PAGE})
        rows = res.get("list") or []
        if not rows:
            break
        df = pd.DataFrame({
            "funding_time": [int(x["fundingRateTimestamp"]) for x in rows],
            "funding_rate": [float(x["fundingRate"]) for x in rows]})
        frames.append(df)
        nxt = int(df["funding_time"].min()) - 1
        if nxt >= hi:
            break
        hi = nxt
        time.sleep(0.12)
    if not frames:
        return pd.DataFrame(columns=FUNDING_COLS)
    return (pd.concat(frames, ignore_index=True).drop_duplicates("funding_time")
            .sort_values("funding_time").reset_index(drop=True))


def fetch_log_rows(out: Path) -> list[dict]:
    """The rows of FETCH_LOG.jsonl, in order ([] when no log is filed)."""
    p = out / FETCH_LOG
    return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()] if p.exists() else []


# ═══════════════════════════════════════════════ 3 · CONTRACT SPECS (the TRADING check; the tick of record)
CONTRACT_SPECS = "CONTRACT_SPECS.json"
MULTIPLIER_FIELDS = d11_const("MULTIPLIER_FIELDS")
_MULT_PREFIX = re.compile(r"^(\d+)(?=[A-Z])")
NORMALIZATION_LAW, _NL1, _NL2 = source_literal(TC10_SRC, "NORMALIZATION_LAW")


# ported from scripts/tierc11_data.py:986-990 @ sha256 b2fe090f4a6cefe4 — VERBATIM
def base_multiplier(base_asset: str) -> int:
    """TOKENS per contract unit, READ off the venue's own baseAsset name
    [LEAN D-l]: '1000PEPE' -> 1000, 'BTC' -> 1.  Never typed per symbol."""
    m = _MULT_PREFIX.match(base_asset or "")
    return int(m.group(1)) if m else 1


# ported from scripts/tierc11_data.py:994-997 @ sha256 b2fe090f4a6cefe4 — VERBATIM
def normalize_price(px, multiplier: int):
    """Venue price (per contract unit) -> price PER ONE TOKEN.  A PURE SCALING
    by the constant 1/multiplier."""
    return px / multiplier


# ported from scripts/tierc11_data.py:1001-1004 @ sha256 b2fe090f4a6cefe4 — VERBATIM
def normalize_qty(q, multiplier: int):
    """Venue quantity (contract units) -> quantity in TOKENS.  The inverse
    scaling, so notional px*q is invariant."""
    return q * multiplier


# ported from scripts/tierc11_data.py:1009-1114 @ sha256 b2fe090f4a6cefe4 — TEXT-ONLY: the not-TRADING HALT and the log lines name the TC12 capture (the filed `doc` statement is the referee's, unchanged)
def capture_contract_specs(out: Path, pin: dict) -> dict:
    """ONE venue reach per venue, write-once: the venue's own contract spec per
    panel symbol, in TC10's schema.  In TC12 it is the proof that every symbol of record is still
    TRADING, and its `price_tick` strings are THE TICK OF RECORD [L-D.22, O-20] — a point-in-time
    venue spec taken at the fetch run (the record carries its own capture stamp beside the pin).

    HALTS IF: the venue does not serve a stem's symbol, or serves it not TRADING.
    """
    p = out / CONTRACT_SPECS
    if p.exists():
        doc = json.loads(p.read_text())
        log(f"CONTRACT SPECS (re-read, captured {doc['captured_wall_clock_utc']})")
        return doc
    assets = panel_assets()
    with CallLog(out, "contract_specs"):
        r = ED._get(ED.REST_BASE + "/fapi/v1/exchangeInfo")
        info = r.json()
        by_sym = {s["symbol"]: s for s in info["symbols"]}
        rows, absent, not_trading = [], {}, []
        for a in assets:
            if a["venue"] == "BINANCE_USDTM":
                s = by_sym.get(a["symbol"])
                if s is None:
                    raise SystemExit(f"HALT: {a['symbol']} absent from exchangeInfo at capture")
                if s["status"] != "TRADING" or s["contractType"] != "PERPETUAL":
                    not_trading.append(f"{a['symbol']} {s['status']} {s['contractType']}")
                filt = {f["filterType"]: f for f in s["filters"]}
                base = s["baseAsset"]
                row = {
                    "asset": a["asset"], "stem": a["stem"], "symbol": s["symbol"],
                    "venue": "BINANCE_USDTM", "base_asset": base, "quote_asset": s["quoteAsset"],
                    "contract_type": s["contractType"], "status": s["status"],
                    "price_tick": filt["PRICE_FILTER"]["tickSize"],
                    "qty_step": filt["LOT_SIZE"]["stepSize"],
                    "min_qty": filt["LOT_SIZE"]["minQty"],
                    "min_notional_usdt": filt.get("MIN_NOTIONAL", {}).get("notional"),
                    "price_precision": s["pricePrecision"], "quantity_precision": s["quantityPrecision"],
                    "venue_object": s,
                }
            else:
                inst = _bybit_get("/v5/market/instruments-info",
                                  {"category": "linear", "symbol": a["symbol"]})["list"]
                if not inst:
                    raise SystemExit(f"HALT: bybit serves no instrument {a['symbol']} at capture")
                s = inst[0]
                if s["status"] != "Trading" or s["contractType"] != "LinearPerpetual":
                    not_trading.append(f"{a['symbol']} {s['status']} {s['contractType']}")
                base = s["baseCoin"]
                row = {
                    "asset": a["asset"], "stem": a["stem"], "symbol": s["symbol"],
                    "venue": "BYBIT_V5_LINEAR", "base_asset": base, "quote_asset": s["quoteCoin"],
                    "contract_type": s["contractType"], "status": s["status"],
                    "price_tick": s["priceFilter"]["tickSize"],
                    "qty_step": s["lotSizeFilter"]["qtyStep"],
                    "min_qty": s["lotSizeFilter"]["minOrderQty"],
                    "min_notional_usdt": s["lotSizeFilter"].get("minNotionalValue"),
                    "price_precision": s.get("priceScale"), "quantity_precision": None,
                    "funding_interval_minutes": s.get("fundingInterval"),
                    "venue_object": s,
                }
            mult = base_multiplier(base)
            blob = json.dumps(row["venue_object"])
            present = [k for k in MULTIPLIER_FIELDS if f'"{k}"' in blob]
            absent[row["symbol"]] = present
            row.update(
                multiplier_tokens_per_contract_unit=mult,
                quotes_per_tokens=mult,
                multiplier_source=(f"baseAsset {base!r} -> leading integer {mult} [LEAN D-l]; the "
                                   f"venue publishes NO {list(MULTIPLIER_FIELDS)} field for this "
                                   f"contract (fields found in its object: {present or 'none'})"),
                price_is_per_tokens=(f"EVERY PRICE ON {row['symbol']} IS QUOTED PER {mult} TOKENS"
                                     if mult != 1 else
                                     f"prices on {row['symbol']} are per ONE {base} (multiplier 1)"),
                normalized_price_law=(f"normalized price = venue price / {mult} (USDT per one "
                                      f"{base.lstrip('0123456789') or base})"),
                normalized_qty_law=(f"normalized quantity = venue quantity x {mult} "
                                    f"({base.lstrip('0123456789') or base} tokens)"))
            rows.append(row)
    if not_trading:
        raise SystemExit(f"HALT: symbol(s) of record not TRADING at the TC12 capture: {not_trading}")
    doc = {
        "as_of_last_closed_4h": pin["as_of_last_closed_4h"],
        "as_of_last_closed_4h_open": pin["as_of_last_closed_4h_open"],
        "warranty": WARRANTY, "seed": SEED,
        "captured_wall_clock_utc": iso(time.time() * 1000),
        "binance_endpoint": ED.REST_BASE + "/fapi/v1/exchangeInfo",
        "binance_response_sha256": hashlib.sha256(r.content).hexdigest(),
        "binance_symbols_in_response": len(info["symbols"]),
        "bybit_endpoint": BYBIT_BASE + "/v5/market/instruments-info?category=linear",
        "law": "the venue's OWN contract spec per panel symbol, captured ONCE; the multiplier is "
               "READ off baseAsset because the venue publishes no multiplier field [LEAN D-l]; in "
               "TIER-C11 the capture is also the proof that every symbol of record is TRADING",
        "multiplier_fields_searched": list(MULTIPLIER_FIELDS),
        "multiplier_fields_found_per_symbol": absent,
        "normalization": NORMALIZATION_LAW,
        "venue_of_record": {"path": "research_outputs/tierc10/data/VENUE_PROBE.json",
                            "sha256": file_sha256(TC10_PROBE)},
        "all_trading": True,
        "assets": rows,
    }
    _dump_once(doc, p)
    _fetch_log(out, {"kind": "contract_specs", "stem": "ALL",
                     "venue": "BINANCE_USDTM+BYBIT_V5_LINEAR",
                     "symbols": len(rows),
                     "binance_response_sha256": doc["binance_response_sha256"]})
    log(f"CONTRACT SPECS captured for {len(rows)} symbols, all TRADING -> {p}")
    return doc


# ported from scripts/tierc11_data.py:1118-1120 @ sha256 b2fe090f4a6cefe4 — VERBATIM
def load_contract_specs(out: Path | None = None) -> dict | None:
    p = (out or OUT) / CONTRACT_SPECS
    return json.loads(p.read_text()) if p.exists() else None


# ported from scripts/tierc11_data.py:1124-1155 @ sha256 b2fe090f4a6cefe4 — TEXT-ONLY: the artifact path is tierc12's
def contract_multiplier_table(out: Path | None = None) -> dict | None:
    """The manifest's view of the capture: per symbol, and the two that quote
    per 1000 tokens named out loud."""
    doc = load_contract_specs(out)
    if doc is None:
        return None
    rows = [{k: a[k] for k in ("asset", "stem", "symbol", "venue", "base_asset", "quote_asset",
                               "multiplier_tokens_per_contract_unit", "multiplier_source",
                               "price_is_per_tokens", "normalized_price_law",
                               "normalized_qty_law", "price_tick", "qty_step", "min_qty",
                               "min_notional_usdt", "price_precision", "quantity_precision")}
            for a in doc["assets"]]
    scaled = [a["symbol"] for a in rows if a["multiplier_tokens_per_contract_unit"] != 1]
    return {
        "artifact": f"research_outputs/tierc12/data/{CONTRACT_SPECS}",
        "artifact_sha256": file_sha256((out or OUT) / CONTRACT_SPECS),
        "capture_instant": ("NOT carried here, and not by name either: no run-time clock key "
                            "enters a deterministic artifact (F-D-DET scans these files for the "
                            f"key names themselves). The capture's own stamp lives in "
                            f"{CONTRACT_SPECS} — a PROVENANCE file, which holds clocks by design "
                            "and is never in the determinism set. This row pins that file's BYTES "
                            "by sha256 instead."),
        "binance_response_sha256": doc["binance_response_sha256"],
        "finding": (f"the venue publishes NO {list(MULTIPLIER_FIELDS)} field for any of these "
                    f"contracts — the multiplier lives in the baseAsset NAME and is read from it "
                    f"[LEAN D-l]. Symbols whose multiplier is not 1: {scaled or 'none'}. "
                    f"{' AND '.join(a['price_is_per_tokens'] for a in rows if a['multiplier_tokens_per_contract_unit'] != 1) or 'no symbol is scaled'}."),
        "multiplier_fields_found_per_symbol": doc["multiplier_fields_found_per_symbol"],
        "normalization": doc["normalization"],
        "symbols_quoting_per_1000_tokens": scaled,
        "rows": rows,
    }


# ═══════════════════════════════════════════════ 4 · PRE_STATE + the seam audit [L-D.6]
# ported from scripts/tierc11_data.py:1161-1205 @ sha256 b2fe090f4a6cefe4 — TEXT-ONLY: each row's keys and the filed sentences name the TC11 manifest sha it must equal (the clone's reference)
def write_pre_state(pin: dict, out: Path) -> dict:
    """WRITE-ONCE ledger of every in-scope file of the TC12 clone BEFORE TC12
    fetched anything: file sha, rows, edges, content sha, and the TC11 manifest
    sha it must equal.  The no-rewrite proof reads the old prefix back out of
    the CURRENT file and re-hashes.

    HALTS IF: an in-scope file is missing, or a file's bytes moved between the
    clone and now."""
    p = out / "PRE_STATE.json"
    if p.exists():
        return json.loads(p.read_text())
    attest = load_clone_attest(out)
    files = {}
    for rel in scope_paths():
        q = SNAPSHOT / rel
        if not q.exists():
            raise SystemExit(f"HALT: in-scope file {rel} is missing from the TC12 clone")
        col, cols = (("open_time", KLINE_COLS) if rel.startswith("klines/")
                     else ("funding_time", FUNDING_COLS))
        sha = file_sha256(q)
        at = attest["files"].get(rel)
        if at is None or at["sha256"] != sha:
            raise SystemExit(f"HALT: {rel} moved between the clone and PRE_STATE "
                             f"({sha[:12]} vs clone {at and at['sha256'][:12]})")
        d = pd.read_parquet(q)
        files[rel] = {
            "file_sha256": sha, "rows": int(len(d)),
            "first_ms": int(d[col].min()), "last_ms": int(d[col].max()),
            "last": iso(int(d[col].max())),
            "content_sha": frame_sha(d.sort_values(col), cols),
            "bytes": q.stat().st_size,
            "tc11_manifest_sha256": at["reference_sha256"],
            "equals_tc11_manifest": sha == at["reference_sha256"]}
    pre = {"as_of_last_closed_4h": pin["as_of_last_closed_4h"],
           "as_of_last_closed_4h_open": pin["as_of_last_closed_4h_open"],
           "warranty": WARRANTY,
           "law": "write-once; taken on the TC12 clone BEFORE the first TC12 fetch; an old prefix "
                  "may be EXTENDED, never rewritten",
           "scope": "TC11's scope of record by object (O-26): 17 x {5m,1h,4h,12h,1d,1w} + CLASSIC5 x "
                    "15m + 17 funding tapes",
           "tier": TIER, "stage": STAGE, "seed": SEED,
           "files": files}
    _dump_once(pre, p)
    log(f"PRE_STATE filed: {len(files)} pre-existing in-scope files, all equal to TC11's "
        f"manifest: {all(v['equals_tc11_manifest'] for v in files.values())}")
    return pre


EDGE_AUDIT = "EDGE_AUDIT.json"


# ported from scripts/tierc11_data.py:1211-1216 @ sha256 b2fe090f4a6cefe4 — CHANGED: the cut is TC11's as-of (the pin of the snapshot this clone inherits)
def inherited_rows(rel: str, root: Path | None = None) -> pd.DataFrame:
    """The rows of a native kline file that TC11's as-of EXCLUDED (open + step >
    the TC11 close) at the clone.  TC11's manifest files `rows_after_as_of` 0 on every row, so
    in the TC12 clone this population is EMPTY — measured and recorded, not assumed."""
    _, iv = split_rel(rel)
    d = pd.read_parquet((root or SNAPSHOT) / rel).sort_values("open_time")
    return d[d["open_time"] + STEP_MS[iv] > TC11_PIN_CLOSE_MS].reset_index(drop=True)


def _venue_funding_prints(a: dict, hour_ms: int) -> list[list]:
    """The venue's own funding print(s) of ONE hour (the stamps that floor to it), as
    [[stamp ms, rate string]] — asked of the stem's venue of record; nothing is saved."""
    hi = hour_ms + FUNDING_JITTER_MS
    if a["venue"] == "BINANCE_USDTM":
        rows = ED._get(ED.REST_BASE + "/fapi/v1/fundingRate",
                       params={"symbol": a["symbol"], "startTime": hour_ms, "endTime": hi}).json()
        got = [[int(x["fundingTime"]), str(x["fundingRate"])] for x in rows]
    else:
        res = _bybit_get("/v5/market/funding/history",
                         {"category": "linear", "symbol": a["symbol"],
                          "startTime": hour_ms, "endTime": hi, "limit": BYBIT_FUNDING_PAGE})
        got = [[int(x["fundingRateTimestamp"]), str(x["fundingRate"])] for x in res.get("list") or []]
    return sorted(x for x in got if x[0] // MS_1H * MS_1H == hour_ms)


# ported from scripts/tierc11_data.py:1219-1281 @ sha256 b2fe090f4a6cefe4 — CHANGED: the population past TC11's as-of is empty and recorded so; THE SEAM BAR of each native file and the last inherited funding print of each tape are compared with the venue
def audit_inherited_rows(pin: dict, pre: dict, out: Path) -> dict:
    """READ-ONLY, WRITE-ONCE [L-D.6].  TC11's audit compared the inherited rows past TC10's as-of;
    in the TC12 clone that population is empty and the record says so.  TC12's audit compares THE
    SEAM BAR — the last inherited row of each native in-scope kline file — with the venue's REST
    bar of the same stamp (exact float equality on O, H, L, C, V), and the last inherited funding
    print of each tape with the venue's print of that hour (rate equality).  Nothing fetched here
    is saved to any file; a difference is a DISCLOSURE (a prefix is never rewritten), never a
    repair and never a HALT."""
    p = out / EDGE_AUDIT
    if p.exists():
        return json.loads(p.read_text())
    ven = {a["stem"]: a for a in panel_assets()}
    rows, frows, past = {}, {}, {}
    with CallLog(out, "edge_audit"):
        for rel in sorted(pre["files"]):
            lo = int(pre["files"][rel]["last_ms"])
            if not rel.startswith("klines/"):
                stem = rel[len("funding/"):len(rel) - len(".parquet")]
                a = ven[stem]
                d = pd.read_parquet(SNAPSHOT / rel)
                tape = float(d[d["funding_time"] == lo]["funding_rate"].iloc[0])
                hour = lo // MS_1H * MS_1H
                prints = _retry(lambda: _venue_funding_prints(a, hour), f"{stem} funding seam")
                same = [x for x in prints if float(x[1]) == tape]
                frows[rel] = {"stem": stem, "venue": a["venue"], "last_inherited_ms": lo,
                              "last_inherited": iso(lo), "funding_hour": iso(hour),
                              "tape_rate": tape, "venue_prints_of_the_hour": prints,
                              "all_equal": len(prints) == 1 and len(same) == 1}
                log(f"    seam audit {rel}: last inherited print {iso(lo)} — "
                    f"{'EQUAL to the venue' if frows[rel]['all_equal'] else f'venue prints {prints}'}")
                continue
            stem, iv = split_rel(rel)
            if iv in DERIVED_IVS:
                continue
            past[rel] = int(len(inherited_rows(rel)))
            a = ven[stem]
            d = pd.read_parquet(SNAPSHOT / rel)
            inh = d[d["open_time"] == lo].reset_index(drop=True)
            hi = lo
            if a["venue"] != "BINANCE_USDTM":
                rest = _retry(lambda: bybit_klines(a["symbol"], iv, lo, hi), f"{stem} {iv} audit")
            else:
                rest = _retry(lambda: ED._fetch_rest_klines(a["symbol"], iv, lo, hi),
                              f"{stem} {iv} audit")
                binance_brake()
            rest = rest[(rest["open_time"] >= lo) & (rest["open_time"] <= hi)]
            m = inh.merge(rest, on="open_time", how="left", suffixes=("", "_rest"),
                          indicator=True)
            diffs, missing = [], []
            for _, r in m.iterrows():
                if r["_merge"] != "both":
                    missing.append(iso(r["open_time"]))
                    continue
                bad = {c: [float(r[c]), float(r[c + "_rest"])] for c in KLINE_COLS[1:]
                       if float(r[c]) != float(r[c + "_rest"])}
                if bad:
                    diffs.append({"open": iso(r["open_time"]), "fields": bad})
            rows[rel] = {"stem": stem, "iv": iv, "venue": a["venue"],
                         "inherited_rows": int(len(inh)), "first_open": iso(lo),
                         "last_open": iso(hi), "rest_rows": int(len(rest)),
                         "equal_rows": int(len(inh) - len(diffs) - len(missing)),
                         "differing": diffs, "missing_at_rest": missing,
                         "all_equal": not diffs and not missing}
            log(f"    seam audit {rel}: the seam bar {iso(lo)} — "
                f"{'EQUAL to REST' if rows[rel]['all_equal'] else f'{len(diffs)} differ, {len(missing)} missing at REST'}")
    doc = {"as_of_last_closed_4h": pin["as_of_last_closed_4h"],
           "as_of_last_closed_4h_open": pin["as_of_last_closed_4h_open"],
           "warranty": WARRANTY, "tier": TIER, "stage": STAGE, "seed": SEED,
           "law": "READ-ONLY: THE SEAM BAR — the last inherited row of every native in-scope kline "
                  "file — compared field by field with the venue's REST bar of the same stamp, and "
                  "the last inherited funding print of every tape with the venue's print of that "
                  "hour; NOTHING fetched here is saved; a difference is disclosed, never repaired "
                  "[L-D.6]",
           "audited_wall_clock_utc": now_iso(),
           "inherited_rows_past_tc11_as_of": {
               "law": f"the population TC11's audit compared at ITS clone (rows with open + step > the "
                      f"previous pin) is, in the TC12 clone, the rows with open + step > {iso(TC11_PIN_CLOSE_MS)}: "
                      "EMPTY — recorded, not dropped",
               "files_measured": len(past), "rows": sum(past.values()),
               "files_holding_any": sorted(k for k, v in past.items() if v)},
           "files_audited": len(rows),
           "rows_audited": sum(v["inherited_rows"] for v in rows.values()),
           "all_equal": all(v["all_equal"] for v in rows.values()),
           "rows": rows,
           "funding_tapes_audited": len(frows),
           "funding_all_equal": all(v["all_equal"] for v in frows.values()),
           "funding": frows}
    _dump_once(doc, p)
    log(f"SEAM AUDIT filed: {doc['files_audited']} native kline files (the seam bar of each), all equal "
        f"to REST: {doc['all_equal']}; {doc['funding_tapes_audited']} funding tapes, all equal: "
        f"{doc['funding_all_equal']}; inherited rows past TC11's as-of: "
        f"{doc['inherited_rows_past_tc11_as_of']['rows']}")
    return doc


# ported from scripts/tierc11_data.py:1285-1305 @ sha256 b2fe090f4a6cefe4 — VERBATIM
def verify_prefixes(pre: dict, root: Path | None = None) -> list[dict]:
    """For every pre-existing file: the rows at or before its OLD last stamp,
    read back from the CURRENT file, must hash to the OLD content sha.
    FAILS IF any old row moved, vanished, or a row was inserted behind the edge."""
    rows = []
    for rel, was in sorted(pre["files"].items()):
        q = (root or SNAPSHOT) / rel
        col, cols = (("open_time", KLINE_COLS) if rel.startswith("klines/")
                     else ("funding_time", FUNDING_COLS))
        if not q.exists():
            rows.append({"file": rel, "ok": False, "why": "file vanished"})
            continue
        d = pd.read_parquet(q).sort_values(col)
        pref = d[d[col] <= was["last_ms"]]
        sha = frame_sha(pref, cols)
        rows.append({"file": rel, "ok": sha == was["content_sha"],
                     "old_rows": was["rows"], "prefix_rows_now": int(len(pref)),
                     "rows_now": int(len(d)), "extended_by": int(len(d) - len(pref)),
                     "untouched_file": file_sha256(q) == was["file_sha256"],
                     "why": "" if sha == was["content_sha"] else "old-prefix content sha moved"})
    return rows


# ═══════════════════════════════════════════════ 4b · THE FEE-SOURCE CAPTURE — Act 1, no parsing [L-D.18]
FEE_SOURCE = "FEE_SOURCE.json"
FEE_GRAMMAR = "FEE_GRAMMAR.json"
FEE_BODY_DIR = PROVENANCE / "fee_source"
# One public, unauthenticated page per venue, on the venue's own domain — frozen with the readings
# (L-D.18).  After the capture no URL is substituted.
FEE_PAGES = {
    "BINANCE_USDTM": {"url": "https://www.binance.com/en/fee/futureFee", "domain": "binance.com"},
    "BYBIT_V5_LINEAR": {"url": "https://www.bybit.com/en/help-center/article/Trading-Fee-Structure",
                        "domain": "bybit.com"},
}
FEE_REASONS = ("transport", "http_<status>", "off_domain_redirect", "no_entry_tier_label",
               "no_rate_in_body", "ambiguous")
MAKER_PUBLISHED = "PUBLISHED"
MAKER_ON_FILE = "ON FILE — NOT RE-CONFIRMED"
MAKER_ASSUMED = "ASSUMPTION — NOT RE-CONFIRMED; no Bybit figure is on file"
FEE_DEFINITION = (
    "the MAKER fee, in percent of notional per fill, that the venue's own public fee schedule lists "
    "for USDT-margined perpetual futures at its ENTRY tier — the tier an account holds with no "
    "volume, balance or token-holding qualification — WITHOUT any token-payment discount, referral "
    "kickback, market-maker or liquidity-provider programme, zero-fee promotion or pair-specific "
    "special rate; where the entry tier lists more than one qualifying figure the HIGHEST is taken; "
    "a zero or negative figure is a rebate or a promotion and is never a base rate [L-D.18]")


def venues_of_record() -> list[str]:
    """The distinct venues of TC10's Stage D table, in table order [L-D.10]."""
    out = []
    for row in stage_d_table():
        if row["venue"] not in out:
            out.append(row["venue"])
    return out


def last_http_status(out: Path, start: int):
    """The status of the last kind='http' row filed after line `start` of the fetch log, or None."""
    rows = [r for r in fetch_log_rows(out)[start:] if r.get("kind") == "http"]
    return rows[len(rows) - 1].get("status") if rows else None


def capture_fee_sources(out: Path) -> dict:
    """Act 1 — CAPTURE [L-D.18], write-once: ONE request per venue through engine.data._get (its
    transport retries included, each a kind='http' row, phase `fee_source`) with the library's
    default headers — no forged browser identity.  The response body is saved byte for byte
    OUTSIDE the repo and outside the snapshot; the record holds NO parsed figure.  A failed
    capture is a filed status — never a HALT and never an "incomplete" exit."""
    p = out / FEE_SOURCE
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    venues = {}
    with CallLog(out, "fee_source"):
        for venue in venues_of_record():
            page = FEE_PAGES.get(venue)
            if page is None:
                halt(f"no fee page is frozen for the venue of record {venue}")
            before = len(fetch_log_rows(out))
            stamp = now_iso()
            date, _, _ = stamp.partition("T")
            row = {"url": page["url"], "venue_domain": page["domain"], "final_url": None,
                   "http_status": None, "error": None, "body_path": None, "body_sha256": None,
                   "body_bytes": None, "redirects": [], "retrieved_wall_clock_utc": stamp,
                   "retrieved_utc_date": date}
            try:
                r = ED._get(page["url"])
            except RuntimeError as e:
                row["error"] = f"{e} <- {e.__cause__!r}"
                row["http_status"] = last_http_status(out, before)
            else:
                body = r.content
                q = FEE_BODY_DIR / f"{venue}.body"
                q.parent.mkdir(parents=True, exist_ok=True)
                if q.exists():
                    halt(f"{q} is on file without a {FEE_SOURCE} — refusing to overwrite a captured body")
                q.write_bytes(body)
                row.update(final_url=r.url, http_status=r.status_code, body_path=str(q),
                           body_sha256=sha_bytes(body), body_bytes=len(body),
                           redirects=[h.url for h in r.history])
            row["http_requests_logged"] = len(fetch_log_rows(out)) - before
            venues[venue] = row
            log(f"    fee source {venue}: {row['url']} -> status {row['http_status']} "
                f"({row['body_bytes']} body bytes; error {row['error']})")
    doc = {"tier": TIER, "stage": STAGE, "seed": SEED,
           "law": "Act 1 of L-D.18: one request per venue with the library's default headers; the "
                  "body saved byte for byte outside the repo and the snapshot; NO parsed figure "
                  "here; a failed capture is a filed status. The retrieval instant lives only in "
                  "this record and in FETCH_LOG.jsonl; --manifest copies the url and the calendar "
                  "date out of this sealed record and makes no clock call [L-D.20]",
           "definition": FEE_DEFINITION,
           "body_dir": str(FEE_BODY_DIR),
           "venues": venues}
    _dump_once(doc, p)
    _fetch_log(out, {"kind": "fee_source",
                     "venues": {v: venues[v]["http_status"] for v in sorted(venues)}})
    log(f"FEE SOURCES captured for {len(venues)} venue(s) -> {p}")
    return doc


# ═══════════════════════════════════════════════ 5 · FETCH (the TC12 snapshot only)
# ported from scripts/tierc11_data.py:1311-1354 @ sha256 b2fe090f4a6cefe4 — TEXT-ONLY: the HALTs name TC12
def extend_klines(a: dict, iv: str, pin: dict, out: Path, pre: dict) -> dict:
    """Extend ONE (asset, lens) forward to the AS_OF, chunk by chunk, each
    chunk saved through engine.data._save_cache (no-shrink + atomic) before
    the next is asked for — an interrupted run resumes from the file's edge.

    HALTS IF: the file is absent or not in PRE_STATE, the venue has no such
    lens, or the first stamp asked for is at or before the PRE_STATE edge."""
    stem, sym, venue = a["stem"], a["symbol"], a["venue"]
    step = STEP_MS[iv]
    tgt = target_last_open(iv, pin["as_of_last_closed_4h_close_ms"])
    path = kline_path(stem, iv)
    rel = f"klines/{path.name}"
    edge = _edge(path, "open_time")
    if edge is None or rel not in pre["files"]:
        raise SystemExit(f"HALT: {rel} is absent or not in PRE_STATE — TC12 never fetches a whole tape")
    if venue != "BINANCE_USDTM" and iv not in BYBIT_IV:
        raise SystemExit(f"HALT: {stem}: Bybit serves no {iv} lens in BYBIT_IV")
    cursor = edge + step
    if cursor <= pre["files"][rel]["last_ms"]:
        raise SystemExit(f"HALT: {rel}: first stamp {iso(cursor)} is not past the PRE_STATE edge "
                         f"{iso(pre['files'][rel]['last_ms'])} — an early start would overwrite")
    fetched = 0
    while cursor <= tgt:
        hi = min(cursor + (CHUNK_BARS - 1) * step, tgt)
        lo = cursor
        if venue == "BINANCE_USDTM":
            df = _retry(lambda: ED._fetch_rest_klines(sym, iv, lo, hi), f"{sym} {iv} klines")
        else:
            df = _retry(lambda: bybit_klines(sym, iv, lo, hi), f"{sym} {iv} bybit klines")
        df = df[(df["open_time"] >= lo) & (df["open_time"] <= hi)]
        _assert_grid(df, iv, f"{stem} {iv}")
        if len(df):
            _assert_bound()
            ED._save_cache(stem, iv, df[KLINE_COLS])
            fetched += len(df)
        _fetch_log(out, {"kind": "klines", "stem": stem, "iv": iv, "venue": venue,
                         "from": iso(lo), "to": iso(hi), "bars": int(len(df))})
        log(f"    {stem} {iv}: {iso(lo)} -> {iso(hi)}  +{len(df)} bars")
        cursor = hi + step
        if venue == "BINANCE_USDTM":
            binance_brake()
    new_edge = _edge(path, "open_time")
    return {"stem": stem, "iv": iv, "target": tgt, "edge": new_edge, "fetched": fetched,
            "complete": bool(new_edge is not None and new_edge >= tgt)}


# ported from scripts/tierc11_data.py:1359-1383 @ sha256 b2fe090f4a6cefe4 — TEXT-ONLY: the HALT names TC12
def extend_funding(a: dict, pin: dict, first_kline_ms: int, out: Path) -> dict:
    stem, sym, venue = a["stem"], a["symbol"], a["venue"]
    close_ms = pin["as_of_last_closed_4h_close_ms"]
    end_ms = close_ms + FUNDING_JITTER_MS
    start_ms = int(first_kline_ms) - DAY_MS
    old = _edge(funding_path(stem), "funding_time")
    if old is None:
        raise SystemExit(f"HALT: funding/{stem}.parquet is absent — TC12 never fetches a whole tape")
    if old // MS_1H * MS_1H >= close_ms:
        log(f"    {stem} funding: edge {iso(old)} already in the pin's hour — nothing can be due")
        return {"stem": stem, "old_edge": old, "edge": old, "skipped": True}
    _assert_bound()
    if venue == "BINANCE_USDTM":
        _retry(lambda: ED.backfill_funding(sym, start_ms, end_ms, log=None),
               f"{sym} funding")
    else:
        lo = old + 1
        df = _retry(lambda: bybit_funding(sym, lo, end_ms), f"{sym} bybit funding")
        if len(df):
            ED._save_funding(stem, df[FUNDING_COLS])
    new = _edge(funding_path(stem), "funding_time")
    _fetch_log(out, {"kind": "funding", "stem": stem, "venue": venue,
                     "old_edge": iso(old), "new_edge": iso(new)})
    log(f"    {stem} funding: edge {iso(old)} -> {iso(new)}")
    return {"stem": stem, "old_edge": old, "edge": new}


FETCH_LOG = "FETCH_LOG.jsonl"
FILE_FEEDING_PHASES = ("fetch",)               # the HTTP phases whose answers reach a tape [L-D.6]


def http_404_findings(rows: list[dict]) -> list[str]:
    """NO 404 FEEDS A FILE [L-D.6]: engine.data._get returns a 404 as success.  A status-404 row
    among the HTTP rows of a file-feeding phase is a finding; every other non-200 row there is a
    retried transient (counted by the caller)."""
    return [f"FETCH-404 {r.get('venue')} {r.get('endpoint')} {r.get('params')}: status 404 in the "
            f"file-feeding phase {r.get('phase')!r}" for r in rows
            if r.get("kind") == "http" and r.get("phase") in FILE_FEEDING_PHASES
            and r.get("status") == requests.codes.not_found]


def assert_no_404(out: Path) -> dict:
    """HALT if a 404 answered a request of a file-feeding phase; return the count of the other
    non-200 rows there (retried transients), printed."""
    rows = fetch_log_rows(out)
    bad = http_404_findings(rows)
    if bad:
        halt(f"a 404 answered a file-feeding request: {bad}")
    feed = [r for r in rows if r.get("kind") == "http" and r.get("phase") in FILE_FEEDING_PHASES]
    transient = [r for r in feed if r.get("status") != requests.codes.ok]
    log(f"  no status 404 among the {len(feed)} HTTP rows of the file-feeding phase(s) "
        f"{list(FILE_FEEDING_PHASES)}; other non-200 rows there (retried transients): {len(transient)}")
    return {"http_rows": len(feed), "status_404": 0, "retried_transients": len(transient)}


# ═══════════════════════════════════════════════ 5b · THE FLAT-BAR ATTESTATION CAPTURE [L-D.13, L-D.16]
FLAT_ATTEST = "FLAT_BAR_ATTEST.json"
FLAT_STREAM_TAG = "data|F-D-2 [4]"             # L-0.14 F: crc32("<suite tag>|<block id>")
PUBLICATIONS = ("both", "rest", "rest-only", "archive-only", "neither")
_ARCHIVE_MEMO: dict = {}


def is_zero_volume_flat(o, h, l, c, v):
    """THE PREDICATE OF RECORD [L-D.16]: a zero-volume flat bar — o == h == l == c AND volume ==
    0 — a bar the VENUE published during an outage.  Kept, counted, attributed, never removed."""
    return (o == h) & (h == l) & (l == c) & (v == 0)


def flat_sample_n() -> int:
    """The per-stem count of the seeded 5m flat-bar sample: FX10's, READ from
    scripts/tierc10_data_fixtures.py by AST — the first argument of `min` in the `size=` keyword
    of the `rng.choice` call of `fd2_real` [L-D.13].  HALTS IF that call has another form."""
    tree = ast.parse((ROOT / FX10_REL).read_text(encoding="utf-8"))
    for fn in tree.body:
        if isinstance(fn, ast.FunctionDef) and fn.name == "fd2_real":
            for c in ast.walk(fn):
                if isinstance(c, ast.Call) and isinstance(c.func, ast.Attribute) and c.func.attr == "choice":
                    for k in c.keywords:
                        v = k.value
                        if (k.arg == "size" and isinstance(v, ast.Call) and isinstance(v.func, ast.Name)
                                and v.func.id == "min" and v.args and isinstance(v.args[0], ast.Constant)
                                and type(v.args[0].value) is int):
                            return v.args[0].value
    halt(f"{FX10_REL}: fd2_real holds no `rng.choice(…, size=min(<int>, …))`")


def flat_populations(pre: dict, root: Path | None = None) -> dict:
    """The two populations of the attestation [L-D.13], from the snapshot:
    (a) THE SEEDED 5m SAMPLE — stems in panel order; for each stem whose 5m tape holds a
        zero-volume flat bar, `rng.choice(stamps, size=min(n, len(stamps)), replace=False)` over
        its flat-bar stamps in ascending order, all on ONE stream
        default_rng([seed, crc32("data|F-D-2 [4]")]);
    (b) EVERY zero-volume flat bar among the rows TC12 ADDED (a stamp past the file's PRE_STATE
        edge), on every native lens of every in-scope file.
    Returns {(stem, lens, open_ms): {"populations": [...], "row": {col: float}, "added": bool}}."""
    rng = np.random.default_rng([SEED, zlib.crc32(FLAT_STREAM_TAG.encode("utf-8"))])
    n = flat_sample_n()
    bars: dict = {}

    def put(stem: str, iv: str, df: pd.DataFrame, t: int, pop: str) -> None:
        was = pre["files"][f"klines/{stem}_{iv}.parquet"]
        r = df[df["open_time"] == t].iloc[0]
        b = bars.setdefault((stem, iv, int(t)), {
            "populations": [], "added": bool(int(t) > int(was["last_ms"])),
            "row": {k: float(r[k]) for k in KLINE_COLS[1:]}})
        b["populations"].append(pop)

    for stem in PANEL17:
        for iv in lenses_of(stem):
            if iv in DERIVED_IVS:
                continue
            df = pd.read_parquet(kline_path(stem, iv, root)).sort_values("open_time")
            z = is_zero_volume_flat(*(df[k].to_numpy(np.float64) for k in KLINE_COLS[1:]))
            t = df["open_time"].to_numpy(np.int64)
            if iv == "5m" and z.any():
                stamps = t[z]
                for x in sorted(int(x) for x in rng.choice(stamps, size=min(n, len(stamps)), replace=False)):
                    put(stem, iv, df, x, "a")
            was = pre["files"][f"klines/{stem}_{iv}.parquet"]
            for x in t[z & (t > int(was["last_ms"]))]:
                put(stem, iv, df, int(x), "b")
    return bars


def _bar_strings(row: list) -> list:
    """[open_ms, o, h, l, c, v] of a venue row — the stamp an int, the five fields the venue's strings."""
    return [int(row[0])] + [str(x) for x in row[1:len(KLINE_COLS)]]


def _rest_bar(a: dict, iv: str, open_ms: int) -> list | None:
    """ONE native bar by stamp from the stem's venue of record over REST, or None when the venue
    serves no bar there.  Raises RuntimeError when the venue cannot be reached or answers an error."""
    if a["venue"] == "BINANCE_USDTM":
        r = ED._get(ED.REST_BASE + "/fapi/v1/klines",
                    params={"symbol": a["symbol"], "interval": iv, "startTime": open_ms,
                            "endTime": open_ms, "limit": 1})
        if r.status_code != requests.codes.ok:
            raise RuntimeError(f"binance klines HTTP {r.status_code}")
        rows = r.json()
    else:
        r = ED._get(BYBIT_BASE + "/v5/market/kline",
                    params={"category": "linear", "symbol": a["symbol"], "interval": BYBIT_IV[iv],
                            "start": open_ms, "end": open_ms, "limit": 1})
        j = r.json() if r.status_code == requests.codes.ok else {}
        if j.get("retCode") != 0:
            raise RuntimeError(f"bybit kline HTTP {r.status_code} retCode {j.get('retCode')}")
        rows = (j.get("result") or {}).get("list") or []
    for row in rows:
        if int(row[0]) == open_ms:
            return _bar_strings(row)
    return None


def _archive_bar(a: dict, iv: str, open_ms: int, monthly: bool, out: Path) -> tuple:
    """The SAME bar from the venue's OTHER publication, the bulk archive: its DAILY zip, or its
    MONTHLY zip on request; stamps normalised by the engine's own _normalize_ms.  Returns (the
    row or None, [first, last] line of the request's kind='http' rows in the fetch log, whether
    the venue publishes that zip at all).  NOTHING read here is saved to a tape."""
    day = iso(open_ms).split("T")[0]
    stamp = day.rsplit("-", 1)[0] if monthly else day
    kind = "monthly" if monthly else "daily"
    key = (a["symbol"], iv, kind, stamp)
    if key not in _ARCHIVE_MEMO:
        before = len(fetch_log_rows(out))
        r = ED._get(f"{ED.BULK_BASE}/{kind}/klines/{a['symbol']}/{iv}/{a['symbol']}-{iv}-{stamp}.zip")
        rows = None
        if r.status_code == requests.codes.ok:
            with zipfile.ZipFile(io.BytesIO(r.content)) as z:
                text = z.read(z.namelist()[0]).decode("utf-8")
            recs = [rec for rec in csv.reader(io.StringIO(text)) if rec and rec[0].isdigit()]
            ts = ED._normalize_ms(np.array([int(rec[0]) for rec in recs], dtype=np.int64))
            rows = {int(t): [int(t)] + [str(x) for x in rec[1:len(KLINE_COLS)]] for t, rec in zip(ts, recs)}
        _ARCHIVE_MEMO[key] = (rows, [before + 1, len(fetch_log_rows(out))])
    rows, lines = _ARCHIVE_MEMO[key]
    return (None if rows is None else rows.get(int(open_ms))), lines, rows is not None


def bar_field_equal(tape: dict, venue: list | None) -> bool:
    """EQUAL, field for field: float(venue string) == the tape's float64 on O, H, L, C, V."""
    return venue is not None and all(float(venue[i + 1]) == float(tape[k])
                                     for i, k in enumerate(KLINE_COLS[1:]))


def capture_flat_bar_attest(pin: dict, pre: dict, out: Path) -> dict:
    """Step 3f [L-D.5, L-D.13], write-once, sealed: the venue's answers for the two populations of
    `flat_populations`, each bar re-asked of its venue of record over REST; a bar of the INHERITED
    prefix on a Binance stem is also asked of the bulk archive (the daily zip, then the monthly zip
    when neither REST nor the daily zip is field-equal).  A TC12-added row is REST by construction
    and gets no archive fallback.  The capture RECORDS and decides nothing: a bar the venue does
    not publish field-equal is filed `neither` (the fixture's RED, not a HALT here).  A venue that
    cannot be reached raises, leaving the record unfiled.  Nothing is saved to any tape."""
    p = out / FLAT_ATTEST
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    ven = {a["stem"]: a for a in panel_assets()}
    pops = flat_populations(pre)
    order = {s: i for i, s in enumerate(PANEL17)}
    lens_i = {iv: i for i, iv in enumerate(LENS_ORDER)}
    bars = []
    with CallLog(out, "flat_attest"):
        for stem, iv, t in sorted(pops, key=lambda k: (order[k[0]], lens_i[k[1]], k[2])):
            b, a = pops[(stem, iv, t)], ven[stem]
            before = len(fetch_log_rows(out))
            rest = _rest_bar(a, iv, t)
            rest_lines = [before + 1, len(fetch_log_rows(out))]
            eq_rest = bar_field_equal(b["row"], rest)
            arch, form, arch_lines, eq_arch = None, None, None, False
            if b["added"] or a["venue"] != "BINANCE_USDTM":
                pub = "rest" if eq_rest else "neither"
            else:
                arch, arch_lines, published = _archive_bar(a, iv, t, False, out)
                form = "daily" if published else None
                eq_arch = bar_field_equal(b["row"], arch)
                if not eq_rest and not eq_arch:
                    arch_m, lines_m, published_m = _archive_bar(a, iv, t, True, out)
                    if bar_field_equal(b["row"], arch_m):
                        arch, form, arch_lines, eq_arch = arch_m, "monthly", lines_m, True
                pub = ("both" if eq_rest and eq_arch else
                       ("rest" if arch is None else "rest-only") if eq_rest else
                       "archive-only" if eq_arch else "neither")
            bars.append({"stem": stem, "lens": iv, "open_ms": int(t), "open": iso(t),
                         "populations": sorted(set(b["populations"])), "tc12_added_row": b["added"],
                         "venue": a["venue"], "tape_row": b["row"],
                         "rest_row": rest[1:] if rest is not None else None,
                         "archive_row": arch[1:] if arch is not None else None,
                         "archive_form": form, "publication": pub,
                         "fetch_log_lines_rest": rest_lines,
                         "fetch_log_lines_archive": arch_lines})
    doc = {"as_of_last_closed_4h": pin["as_of_last_closed_4h"],
           "as_of_last_closed_4h_open": pin["as_of_last_closed_4h_open"],
           "warranty": WARRANTY, "tier": TIER, "stage": STAGE, "seed": SEED,
           "law": "the venue's answers for (a) the seeded 5m zero-volume-flat-bar sample and (b) every "
                  "zero-volume flat bar among the rows TC12 added, captured ONCE by the builder and "
                  "sealed; F-D-2 [4] re-derives both populations from the snapshot and holds every bar "
                  "field-equal to its sealed venue row. THE CLAIM IS 'Naiad inserted no bar', NOT 'the "
                  "venue published no flat bar' [L-D.13]",
           "stream": "numpy.random.default_rng([seed, crc32('" + FLAT_STREAM_TAG + "')])",
           "n_per_stem": flat_sample_n(),
           "n_per_stem_source": f"{FX10_REL} fd2_real: the first argument of `min` in `size=` of rng.choice (read by AST)",
           "publications": list(PUBLICATIONS),
           "captured_wall_clock_utc": now_iso(),
           "n_bars": len(bars),
           "n_population_a": sum(1 for b in bars if "a" in b["populations"]),
           "n_population_b": sum(1 for b in bars if "b" in b["populations"]),
           "by_publication": {k: sum(1 for b in bars if b["publication"] == k) for k in PUBLICATIONS},
           "bars": bars}
    _dump_once(doc, p)
    _fetch_log(out, {"kind": "flat_attest", "bars": len(bars), "by_publication": doc["by_publication"]})
    log(f"FLAT-BAR ATTESTATION captured: {len(bars)} bars ({doc['n_population_a']} seeded 5m, "
        f"{doc['n_population_b']} among the rows TC12 added); by publication {doc['by_publication']} -> {p}")
    return doc


# ported from scripts/tierc11_data.py:1386-1422 @ sha256 b2fe090f4a6cefe4 — CHANGED: + the fee-source capture (3d), the no-404 assertion, and the flat-bar attestation capture (3f) once the extension is complete
def run_fetch(pin: dict, out: Path) -> tuple[list[str], dict]:
    """specs -> PRE_STATE -> the seam audit -> the fee-source capture -> 4h, 12h, 1h, funding, 15m,
    5m (TC10's order, 15m before the 5m) -> the flat-bar attestation capture, only once the
    extension is complete for every in-scope native file [L-D.5 steps 3a-3f].
    Returns (incomplete, stats)."""
    capture_contract_specs(out, pin)
    pre = write_pre_state(pin, out)
    audit_inherited_rows(pin, pre, out)
    capture_fee_sources(out)
    assets = panel_assets()
    incomplete: list[str] = []
    stats = {"t0": time.time(), "results": []}
    with CallLog(out, "fetch"):
        log("\nFETCH — 4h, 12h, 1h, funding, 15m (CLASSIC5), 5m; each from its edge + one step")
        for iv in ("4h", "12h", "1h"):
            for a in assets:
                r = extend_klines(a, iv, pin, out, pre)
                stats["results"].append(r)
                if not r["complete"]:
                    incomplete.append(f"{a['stem']} {iv}: edge {iso(r['edge'])} < {iso(r['target'])}")
        for a in assets:
            try:
                first = int(pd.read_parquet(kline_path(a["stem"], "4h"),
                                            columns=["open_time"])["open_time"].min())
                r = extend_funding(a, pin, first, out)
                if not r.get("skipped"):
                    time.sleep(1.0)
            except RuntimeError as e:
                incomplete.append(f"{a['stem']} funding: {e}")
                log(f"  !! {a['stem']} funding: {e}")
        for iv in (FIFTEEN, "5m"):
            for a in assets:
                if iv not in lenses_of(a["stem"]):
                    continue
                r = extend_klines(a, iv, pin, out, pre)
                stats["results"].append(r)
                if not r["complete"]:
                    incomplete.append(f"{a['stem']} {iv}: edge {iso(r['edge'])} < {iso(r['target'])}")
    stats["http"] = assert_no_404(out)
    if not incomplete:
        try:
            capture_flat_bar_attest(pin, pre, out)
        except RuntimeError as e:
            incomplete.append(f"flat-bar attestation: a venue could not be reached — {e}")
            log(f"  !! flat-bar attestation NOT filed: {e}")
    stats["t1"] = time.time()
    return incomplete, stats


# ═══════════════════════════════════════════════ 6 · THE WRITE-ONCE SEAL
SEAL = "WRITE_ONCE_SEAL.json"
# ported from scripts/tierc11_data.py:1427-1427 @ sha256 b2fe090f4a6cefe4 — CHANGED: TC11's five plus the fee-source capture and the flat-bar attestation capture (seven) [L-D.11]
SEALED_FILES = ("AS_OF_PIN.json", CLONE_ATTEST, CONTRACT_SPECS, EDGE_AUDIT, "PRE_STATE.json",
                FEE_SOURCE, FLAT_ATTEST)


# ported from scripts/tierc11_data.py:1432-1433 @ sha256 b2fe090f4a6cefe4 — VERBATIM
def _lines_sha(lines: list[str]) -> str:
    return hashlib.sha256(("\n".join(lines) + "\n").encode("utf-8")).hexdigest()


# ported from scripts/tierc11_data.py:1438-1473 @ sha256 b2fe090f4a6cefe4 — VERBATIM
def seal_provenance(out: Path) -> dict:
    """Pin the provenance records' bytes — ONCE.  Every record here was written
    by code through _dump_once before the fetch it describes; the seal makes
    every LATER write detectable.  The fetch log is append-only, so its sealed
    LINE PREFIX (its head) is pinned, not the file."""
    p = out / SEAL
    if p.exists():
        return json.loads(p.read_text())
    pin = load_pin(out)
    lines = (out / FETCH_LOG).read_text(encoding="utf-8").splitlines()
    last_fetch = json.loads(lines[-1])["wall_clock_utc"]
    files, disclosure = {}, []
    for n in SEALED_FILES:
        q = out / n
        written = iso(q.stat().st_mtime * 1000)
        files[n] = {"sha256": file_sha256(q), "bytes": q.stat().st_size, "last_written_utc": written}
        if written > last_fetch:
            disclosure.append(f"{n}: last written {written}, AFTER the last fetch row {last_fetch} "
                              "— NOT as first written; a finding")
        else:
            disclosure.append(f"{n}: last written {written}, before the last fetch row "
                              f"{last_fetch} — as first written")
    seal = {"as_of_last_closed_4h": pin["as_of_last_closed_4h"],
            "as_of_last_closed_4h_open": pin["as_of_last_closed_4h_open"],
            "warranty": WARRANTY, "sealed_utc": iso(time.time() * 1000),
            "law": "from this seal on, a sealed file's bytes never move and the fetch log only "
                   "grows past its sealed line prefix; the seal itself is write-once (_dump_once)",
            "files": files,
            "fetch_log": {"file": FETCH_LOG, "sealed_lines": len(lines),
                          "sha256_of_sealed_lines": _lines_sha(lines),
                          "first_row_utc": json.loads(lines[0])["wall_clock_utc"],
                          "last_row_utc": last_fetch},
            "disclosure": disclosure}
    _dump_once(seal, p)
    log(f"SEALED {len(files)} provenance records + {len(lines)} fetch-log lines -> {p}")
    return seal


# ported from scripts/tierc11_data.py:1477-1500 @ sha256 b2fe090f4a6cefe4 — VERBATIM
def verify_seal(out: Path | None = None, root: Path | None = None) -> list[str]:
    """Faults of the seal at `out` against the files under `root` (default: the
    same directory).  FAILS IF a sealed file's bytes moved or vanished, or the
    fetch log lost or changed any sealed line."""
    out = out or OUT
    root = root or out
    p = out / SEAL
    if not p.exists():
        return [f"{SEAL}: not filed — write-once-ness is unproven"]
    seal, bad = json.loads(p.read_text()), []
    for n, was in sorted(seal["files"].items()):
        q = root / n
        if not q.exists():
            bad.append(f"{n}: vanished")
        elif file_sha256(q) != was["sha256"]:
            bad.append(f"{n}: bytes moved since the seal ({file_sha256(q)[:12]} != {was['sha256'][:12]})")
    fl = seal["fetch_log"]
    q = root / fl["file"]
    lines = q.read_text(encoding="utf-8").splitlines() if q.exists() else []
    if len(lines) < fl["sealed_lines"]:
        bad.append(f"{fl['file']}: {len(lines)} lines < the {fl['sealed_lines']} sealed")
    elif _lines_sha(lines[: fl["sealed_lines"]]) != fl["sha256_of_sealed_lines"]:
        bad.append(f"{fl['file']}: a sealed line changed")
    return bad


# ═══════════════════════════════════════════════ 7 · DERIVED LENSES [TC10 LEAN L1; L-D.8]
# ported from scripts/tierc11_data.py:1505-1519 @ sha256 b2fe090f4a6cefe4 — VERBATIM
def derive_1d(f4h: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    """Native 4h -> 1d.  A day exists ONLY if all six of its 4h bars do (the
    twin's law, scripts/rangefinder_twin.py daily_bars).  Returns (frame,
    dropped_incomplete_days)."""
    f = f4h.sort_values("open_time")
    day = f["open_time"] // DAY_MS
    g = f.groupby(day).agg(n=("open_time", "size"), open=("open", "first"),
                           high=("high", "max"), low=("low", "min"),
                           close=("close", "last"), volume=("volume", "sum"))
    keep = g[g["n"] == 6]
    d = pd.DataFrame({"open_time": (keep.index.to_numpy(np.int64) * DAY_MS),
                      "open": keep["open"].to_numpy(), "high": keep["high"].to_numpy(),
                      "low": keep["low"].to_numpy(), "close": keep["close"].to_numpy(),
                      "volume": keep["volume"].to_numpy()})
    return d, int((g["n"] != 6).sum())


# ported from scripts/tierc11_data.py:1523-1536 @ sha256 b2fe090f4a6cefe4 — VERBATIM
def derive_1w(d1: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    """Complete days -> 1w, MONDAY-anchored UTC.  A week exists ONLY if all
    seven of its days are complete days.  Returns (frame, dropped_weeks)."""
    wk = (d1["open_time"] - MONDAY_EPOCH_OFFSET_MS) // WEEK_MS
    g = d1.groupby(wk).agg(n=("open_time", "size"), open=("open", "first"),
                           high=("high", "max"), low=("low", "min"),
                           close=("close", "last"), volume=("volume", "sum"))
    keep = g[g["n"] == 7]
    w = pd.DataFrame({"open_time": (keep.index.to_numpy(np.int64) * WEEK_MS
                                    + MONDAY_EPOCH_OFFSET_MS),
                      "open": keep["open"].to_numpy(), "high": keep["high"].to_numpy(),
                      "low": keep["low"].to_numpy(), "close": keep["close"].to_numpy(),
                      "volume": keep["volume"].to_numpy()})
    return w, int((g["n"] != 7).sum())


# ported from scripts/tierc11_data.py:1540-1546 @ sha256 b2fe090f4a6cefe4 — VERBATIM
def _write_if_changed(df: pd.DataFrame, path: Path) -> str:
    if path.exists() and frame_sha(pd.read_parquet(path), KLINE_COLS) == frame_sha(df, KLINE_COLS):
        return "unchanged"
    tmp = path.with_name(f"{path.name}.{os.getpid()}.tmp")
    df.to_parquet(tmp, index=False)
    os.replace(tmp, path)
    return "written"


# ported from scripts/tierc11_data.py:1550-1561 @ sha256 b2fe090f4a6cefe4 — VERBATIM
def derive_lenses(stem: str, pin: dict) -> dict:
    close_ms = pin["as_of_last_closed_4h_close_ms"]
    src = kline_path(stem, "4h")
    f = pd.read_parquet(src)
    f = f[f["open_time"] + MS_4H <= close_ms]
    d1, drop_d = derive_1d(f)
    w1, drop_w = derive_1w(d1)
    st_d = _write_if_changed(d1, kline_path(stem, "1d"))
    st_w = _write_if_changed(w1, kline_path(stem, "1w"))
    return {"1d": {"rows": int(len(d1)), "dropped_incomplete_days": drop_d, "write": st_d},
            "1w": {"rows": int(len(w1)), "dropped_incomplete_weeks": drop_w, "write": st_w},
            "source": f"klines/{src.name}", "source_rows_as_of": int(len(f))}


# ported from scripts/tierc11_data.py:1564-1572 @ sha256 b2fe090f4a6cefe4 — VERBATIM
def run_derive(pin: dict) -> dict:
    _assert_bound()
    out = {}
    for stem in PANEL17:
        out[stem] = derive_lenses(stem, pin)
        dv = out[stem]
        log(f"    DERIVE {stem:14s} 1d {dv['1d']['rows']:5d} ({dv['1d']['write']:9s}) "
            f"1w {dv['1w']['rows']:4d} ({dv['1w']['write']})")
    return out


# ported from scripts/tierc11_data.py:1575-1583 @ sha256 b2fe090f4a6cefe4 — VERBATIM
def derive_in_memory(stem: str, close_ms: int, root: Path | None = None) -> dict:
    """The same derivation, read-only (the manifest never writes the snapshot)."""
    f = pd.read_parquet(kline_path(stem, "4h", root))
    f = f[f["open_time"] + MS_4H <= close_ms]
    d1, drop_d = derive_1d(f)
    w1, drop_w = derive_1w(d1)
    return {"1d": d1, "1w": w1, "dropped_incomplete_days": drop_d,
            "dropped_incomplete_weeks": drop_w, "source_rows_as_of": int(len(f)),
            "n4": int(len(f))}


# ═══════════════════════════════════════════════ 8 · SCANS — count, never fill
# ported from scripts/tierc11_data.py:1588-1618 @ sha256 b2fe090f4a6cefe4 — VERBATIM
def scan_klines(df: pd.DataFrame, iv: str, as_of_close_ms: int) -> dict:
    """Every number a reader needs to distrust a kline file.  Gaps are LISTED
    whole; nothing is patched.  A zero-volume flat bar (o=h=l=c, volume 0) is
    a bar the VENUE published during an outage — counted, attributed, kept."""
    step, anchor = STEP_MS[iv], GRID_ANCHOR_MS.get(iv, 0)
    t = df["open_time"].to_numpy(np.int64)
    o, h, l, c, v = (df[k].to_numpy(np.float64) for k in KLINE_COLS[1:])
    d = np.diff(t)
    gaps = [{"after_ms": int(t[i]), "after": iso(t[i]),
             "missing_bars": int(d[i] // step - 1)} for i in np.nonzero(d > step)[0]]
    flat = (o == h) & (h == l) & (l == c)
    fin = np.isfinite(o) & np.isfinite(h) & np.isfinite(l) & np.isfinite(c) & np.isfinite(v)
    closed = t + step <= as_of_close_ms
    last_asof = int(t[closed].max()) if closed.any() else None
    return {
        "rows": int(len(t)), "rows_as_of": int(closed.sum()),
        "rows_after_as_of": int((~closed).sum()),
        "first_open_ms": int(t[0]) if len(t) else None, "first_open": iso(t[0]) if len(t) else None,
        "last_open_ms": int(t[-1]) if len(t) else None, "last_open": iso(t[-1]) if len(t) else None,
        "as_of_last_closed_bar_open": iso(last_asof),
        "as_of_last_closed_bar_close": iso(last_asof + step) if last_asof is not None else None,
        "gap_count": len(gaps), "missing_bars_total": int(sum(g["missing_bars"] for g in gaps)),
        "gaps": gaps,
        "duplicates": int(len(t) - len(np.unique(t))), "backward": int((d < 0).sum()),
        "off_grid": int((((t - anchor) % step) != 0).sum()),
        "non_finite": int((~fin).sum()),
        "ohlc_incoherent": int(((h < np.maximum(o, c)) | (l > np.minimum(o, c)) | (h < l)).sum()),
        "venue_zero_volume_bars": int((v == 0).sum()),
        "venue_flat_bars": int(flat.sum()),
        "venue_zero_volume_flat_bars": int((flat & (v == 0)).sum()),
    }


# ported from scripts/tierc11_data.py:1622-1650 @ sha256 b2fe090f4a6cefe4 — VERBATIM
def scan_funding(df: pd.DataFrame, as_of_close_ms: int) -> dict:
    """Funding grid as OBSERVED: stamps snapped to the hour, the spacing
    histogram filed WHOLE (a venue changes cadence; a histogram shows it, a
    single 'interval' would hide it)."""
    t = np.sort(df["funding_time"].to_numpy(np.int64))
    snap = (t + MS_1H // 2) // MS_1H * MS_1H
    hour = t // MS_1H * MS_1H                       # LEAN D-g: the estate's load_funding key
    sp = np.diff(snap) // MS_1H
    hist = {int(k): int(n) for k, n in zip(*np.unique(sp, return_counts=True))} if len(sp) else {}
    tail = sp[-10:] if len(sp) else sp
    tail_h = int(np.median(tail)) if len(tail) else None
    modal_h = int(max(hist, key=lambda k: (hist[k], -k))) if hist else None
    return {
        "rows": int(len(t)),
        "first_ms": int(t[0]) if len(t) else None, "first": iso(t[0]) if len(t) else None,
        "last_ms": int(t[-1]) if len(t) else None, "last": iso(t[-1]) if len(t) else None,
        "rows_after_as_of": int((t > as_of_close_ms + FUNDING_JITTER_MS).sum()),
        "max_jitter_ms": int(np.abs(t - snap).max()) if len(t) else None,
        "ms_past_hour_min": int((t - hour).min()) if len(t) else None,
        "ms_past_hour_max": int((t - hour).max()) if len(t) else None,
        "floor_hour_equals_nearest_hour": bool((hour == snap).all()),
        "same_hour_prints": int(len(hour) - len(np.unique(hour))),
        "prints_stamped_after_as_of_close_within_jitter": int(
            ((t > as_of_close_ms) & (t <= as_of_close_ms + FUNDING_JITTER_MS)).sum()),
        "interval_hours_observed_modal": modal_h,
        "interval_hours_observed_tail": tail_h,
        "spacing_hours_histogram": {str(k): hist[k] for k in sorted(hist)},
        "duplicates": int(len(t) - len(np.unique(t))),
    }


# ported from scripts/tierc11_data.py:1654-1672 @ sha256 b2fe090f4a6cefe4 — VERBATIM
def funding_coverage(stem: str, as_of_close_ms: int, root: Path | None = None) -> dict:
    """F-D-3's law as a pure function of (root, stem, as-of).
    ok is False IF: the file is absent, empty, or its last stamp is older than
    the kline edge (the AS_OF close) minus ONE observed funding interval."""
    p = funding_path(stem, root)
    if not p.exists():
        return {"stem": stem, "ok": False, "why": f"funding file ABSENT: {p.name}"}
    d = pd.read_parquet(p)
    d = d[d["funding_time"] <= as_of_close_ms + FUNDING_JITTER_MS]
    if not len(d):
        return {"stem": stem, "ok": False, "why": "funding file has no row at or before AS_OF"}
    s = scan_funding(d, as_of_close_ms)
    ivl = s["interval_hours_observed_tail"] or s["interval_hours_observed_modal"] or 8
    floor_ms = as_of_close_ms - ivl * MS_1H
    ok = s["last_ms"] + FUNDING_JITTER_MS >= floor_ms
    return {"stem": stem, "ok": bool(ok), "rows": s["rows"], "first": s["first"],
            "last": s["last"], "interval_hours_tail": ivl, "floor": iso(floor_ms),
            "why": "" if ok else f"last stamp {s['last']} older than kline edge minus one "
                                 f"funding interval ({iso(floor_ms)})"}


FIFTEEN_VOLUME_RTOL = 1e-9     # a sum of three floats vs one parsed decimal: rounding, not data


# ported from scripts/tierc11_data.py:1678-1731 @ sha256 b2fe090f4a6cefe4 — CHANGED: the era boundary is TC11's pin (bars closing after it are TC12's new rows); the keys say tc12_new
def fifteen_minute_audit(close_ms: int, root: Path | None = None) -> dict:
    """DISCLOSURE, never a failure [D11-e carried]: every CLASSIC5 15m bar closed at the
    pin against the three native 5m bars it spans (open = first open, high =
    max, low = min, close = last close, volume = the sum).  Price fields are
    compared EXACTLY; volume to a relative 1e-9 (three float additions vs one
    parsed decimal).  Every mismatch is LISTED whole."""
    per, tot = {}, {"compared": 0, "price_mismatch": 0, "volume_only_mismatch": 0,
                    "no_complete_5m_triple": 0}
    for stem in CLASSIC5:
        f15 = pd.read_parquet(kline_path(stem, FIFTEEN, root)).sort_values("open_time")
        f15 = f15[f15["open_time"] + STEP_MS[FIFTEEN] <= close_ms].reset_index(drop=True)
        f5 = pd.read_parquet(kline_path(stem, "5m", root)).sort_values("open_time")
        f5 = f5[f5["open_time"] + STEP_MS["5m"] <= close_ms].reset_index(drop=True)
        t15 = f15["open_time"].to_numpy(np.int64)
        t5 = f5["open_time"].to_numpy(np.int64)
        i0 = np.searchsorted(t5, t15)
        ok = i0 + 2 < len(t5)
        j = np.where(ok, i0, 0)
        ok &= ((t5[j] == t15) & (t5[np.minimum(j + 1, len(t5) - 1)] == t15 + 300_000)
               & (t5[np.minimum(j + 2, len(t5) - 1)] == t15 + 600_000))
        o5, h5, l5, c5, v5 = (f5[k].to_numpy(np.float64) for k in KLINE_COLS[1:])
        o15, h15, l15, c15, v15 = (f15[k].to_numpy(np.float64) for k in KLINE_COLS[1:])
        jj = j[ok]
        so = o5[jj]
        sh = np.maximum(np.maximum(h5[jj], h5[jj + 1]), h5[jj + 2])
        sl = np.minimum(np.minimum(l5[jj], l5[jj + 1]), l5[jj + 2])
        sc = c5[jj + 2]
        sv = (v5[jj] + v5[jj + 1]) + v5[jj + 2]
        pm = (so != o15[ok]) | (sh != h15[ok]) | (sl != l15[ok]) | (sc != c15[ok])
        vm = (~pm) & (np.abs(sv - v15[ok]) > FIFTEEN_VOLUME_RTOL * np.maximum(1.0, np.abs(v15[ok])))
        tt = t15[ok]
        listed = []
        for k in np.nonzero(pm | vm)[0]:
            era = "tc11" if tt[k] + STEP_MS[FIFTEEN] <= TC11_PIN_CLOSE_MS else "tc12_new"
            listed.append({"open": iso(tt[k]), "kind": "price" if pm[k] else "volume_only",
                           "era": era,
                           "15m": [float(x[ok][k]) for x in (o15, h15, l15, c15, v15)],
                           "from_5m": [float(x[k]) for x in (so, sh, sl, sc, sv)]})
        new = tt + STEP_MS[FIFTEEN] > TC11_PIN_CLOSE_MS
        per[stem] = {"bars_15m_as_of": int(len(t15)), "compared": int(ok.sum()),
                     "no_complete_5m_triple": [iso(x) for x in t15[~ok]],
                     "price_mismatch": int(pm.sum()), "volume_only_mismatch": int(vm.sum()),
                     "price_mismatch_tc12_new_bars": int((pm & new).sum()),
                     "volume_only_mismatch_tc12_new_bars": int((vm & new).sum()),
                     "mismatches": listed}
        tot["compared"] += int(ok.sum())
        tot["price_mismatch"] += int(pm.sum())
        tot["volume_only_mismatch"] += int(vm.sum())
        tot["no_complete_5m_triple"] += int((~ok).sum())
    return {"law": "DISCLOSURE, NOT A FAILURE [D11-e carried]: 15m vs the three native 5m bars it "
                   "spans; open/high/low/close EXACT, volume to the relative tolerance "
                   "FIFTEEN_VOLUME_RTOL of scripts/tierc11_data.py; the venue's intervals "
                   "disagree on incident bars and nothing is reconciled by rewriting a bar",
            "per_asset": per, "totals": tot}


# ═══════════════════════════════════════════════ 9 · FEES [L-D.17 … L-D.21]
# ported from scripts/tierc11_data.py:1736-1740 @ sha256 b2fe090f4a6cefe4 — VERBATIM
def _source_line(path: Path, needle: str) -> int | None:
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if needle in line:
            return i
    return None


# ported from scripts/tierc11_data.py:1744-1751 @ sha256 b2fe090f4a6cefe4 — VERBATIM
def tier_of(asset: str) -> str:
    """The charter tier of a CONTRACT asset name.  HALTS IF unassigned — an
    unassigned asset must stop the build, never default to the cheapest tier."""
    t = TIER_OF_ASSET.get(asset)
    if t is None:
        raise SystemExit(f"HALT: asset {asset!r} is in NO slippage tier of the contract clause "
                         f"({sorted(TIER_OF_ASSET)}) — the haircut twin refuses to guess")
    return t


# ported from scripts/tierc11_data.py:1755-1757 @ sha256 b2fe090f4a6cefe4 — VERBATIM
def slippage_bps_side(asset: str) -> float:
    """Charter slippage, bps PER SIDE, for a contract asset name."""
    return float(SLIPPAGE_TIERS[tier_of(asset)]["bps"])


# ported from scripts/tierc11_data.py:1761-1765 @ sha256 b2fe090f4a6cefe4 — VERBATIM
def charter_bps_side(asset: str) -> float:
    """The charter model's per-side rate: the estate's taker fee PLUS the
    charter slippage of the asset's tier.  Never a replacement for the
    TC-series toll — the caller keeps both."""
    return float(R2.FEE_BPS_SIDE) + slippage_bps_side(asset)


# ported from scripts/tierc11_data.py:1769-1770 @ sha256 b2fe090f4a6cefe4 — VERBATIM
def charter_round_trip_bps(asset: str) -> float:
    return 2.0 * charter_bps_side(asset)


# ported from scripts/tierc11_data.py:1774-1784 @ sha256 b2fe090f4a6cefe4 — VERBATIM
def assert_tiers_cover(assets: list[str]) -> dict:
    """Every admitted asset is in exactly one tier and the tiers name nothing
    else.  HALTS IF an admitted asset is unassigned."""
    missing = [a for a in assets if a not in TIER_OF_ASSET]
    if missing:
        raise SystemExit(f"HALT: admitted asset(s) with no slippage tier: {missing}")
    sizes = {t: len(b["assets"]) for t, b in sorted(SLIPPAGE_TIERS.items())}
    extra = sorted(set(TIER_OF_ASSET) - set(assets))
    return {"tier_sizes": sizes, "tier_total": sum(sizes.values()),
            "admitted": len(assets), "covers_all_admitted": not missing,
            "tiered_but_not_admitted": extra}


# ported from scripts/tierc11_data.py:1788-1821 @ sha256 b2fe090f4a6cefe4 — VERBATIM
def haircut_twin_net_r(asset: str, gross_r: float, entry_px: float, exit_px: float,
                       risk_px: float) -> dict:
    """THE ADDED COLUMN.  The charter cost model — the estate's own fee law's
    shape with the charter's per-side SLIPPAGE added to the per-side fee —
    expressed as an R haircut, so a Stage B row can carry a twin net_r beside
    its TC-series net_r WITHOUT re-deriving the tiers.

    The TC-series toll is returned UNCHANGED in the same dict and is never
    replaced: a caller that drops `tc_series_round_trip_bps_used` or writes the
    twin over it is caught by F-D-HAIRCUT.

    cost_px = ((FEE_BPS_SIDE + slip_side) / 10_000) * (entry_px + exit_px)
              — tierc2_baseline's fee law, with slippage folded into the side rate
    cost_r  = cost_px / risk_px            (risk_px = |entry - stop|, price units)
    net_r_twin = gross_r - cost_r

    HALTS IF: risk_px is not positive (an R with no denominator is not an R).
    """
    if not (risk_px > 0):
        raise SystemExit(f"HALT: haircut twin for {asset}: risk_px {risk_px!r} is not positive")
    slip = slippage_bps_side(asset)
    fee = float(R2.FEE_BPS_SIDE)
    cost_px = ((fee + slip) / 10_000.0) * (float(entry_px) + float(exit_px))
    cost_r = cost_px / float(risk_px)
    return {
        "asset": asset, "tier": tier_of(asset), "slippage_bps_side": slip,
        "fee_bps_side": fee, "charter_bps_side": fee + slip,
        "charter_round_trip_bps": 2.0 * (fee + slip),
        "tc_series_round_trip_bps_used": float(R2.FEE_BPS_ROUND_TRIP),
        "cost_px": cost_px, "cost_r": cost_r,
        "gross_r": float(gross_r), "net_r_twin": float(gross_r) - cost_r,
        "law": "HAIRCUT TWIN — an ADDED column beside the TC-series toll, never a "
               "replacement for it [VETO 'tiers']",
    }


# ported from scripts/tierc11_data.py:1825-1832 @ sha256 b2fe090f4a6cefe4 — VERBATIM
def haircut_twin_for_stem(stem: str, gross_r: float, entry_px: float, exit_px: float,
                          risk_px: float, out: Path | None = None) -> dict:
    """The same, addressed by file stem: the stem -> contract asset map is READ
    from the filed manifest's venue table, never typed."""
    by = {v["stem"]: v["asset"] for v in load_manifest(out)["venues"] if v["stem"]}
    if stem not in by:
        raise SystemExit(f"HALT: the manifest's venue table names no stem {stem}")
    return haircut_twin_net_r(by[stem], gross_r, entry_px, exit_px, risk_px)


# ported from scripts/tierc11_data.py:1836-1878 @ sha256 b2fe090f4a6cefe4 — VERBATIM
def haircut_twin_table(assets: list[dict], fees: dict) -> dict:
    """The filed table: the contract clause, the tiers parsed out of it, the
    charter line the model comes from, and the per-asset twin rate beside the
    UNTOUCHED TC-series toll."""
    names = [a["asset"] for a in assets]
    cover = assert_tiers_cover(names)
    line = _source_line(CHARTER_SOURCE, CHARTER_SLIPPAGE_NEEDLE)
    rows = [{"asset": a["asset"], "stem": a["stem"], "tier": tier_of(a["asset"]),
             "slippage_bps_side": slippage_bps_side(a["asset"]),
             "fee_bps_side": float(R2.FEE_BPS_SIDE),
             "charter_bps_side": float(R2.FEE_BPS_SIDE) + slippage_bps_side(a["asset"]),
             "charter_round_trip_bps": 2.0 * (float(R2.FEE_BPS_SIDE)
                                              + slippage_bps_side(a["asset"])),
             "tc_series_round_trip_bps_used": float(R2.FEE_BPS_ROUND_TRIP)}
            for a in assets]
    return {
        "law": "every row gets the charter model as a HAIRCUT TWIN BESIDE the TC-series toll. "
               "The 5-asset control's TC-series accounting stays UNTOUCHED — round_trip_bps_used "
               "is the same object it always was, on every one of the 17 rows; the twin is an "
               "ADDED column and nothing reads it unless it asks for it [VETO 'tiers'].",
        "contract_clause": CONTRACT_SLIPPAGE_CLAUSE,
        "tier_table_source": "PARSED from contract_clause at import (parse_slippage_clause); no "
                             "bps figure is typed anywhere in this module",
        "charter_source": (f"Naiad_Phase0_Charter.md:{line} — "
                           f"{CHARTER_SOURCE.read_text(encoding='utf-8').splitlines()[line - 1].strip()}"
                           if line else "Naiad_Phase0_Charter.md: slippage line NOT FOUND"),
        "charter_note": "the charter's own tiers name the ratification basket (BTC ETH | SOL NEAR "
                        "ZEC JTO TAO | HYPE FARTCOIN LIT); the TIER-C10 contract clause EXTENDS "
                        "the same model to the seventeen, and it is the contract clause — not the "
                        "charter line — that this table is parsed from",
        "tiers": {t: {"bps_per_side": b["bps"], "assets": list(b["assets"])}
                  for t, b in sorted(SLIPPAGE_TIERS.items())},
        "coverage": cover,
        "arithmetic": f"{' + '.join(str(v) for _, v in sorted(cover['tier_sizes'].items()))} = "
                      f"{cover['tier_total']} assets, admitted {cover['admitted']}",
        "cost_law": "cost_px = ((FEE_BPS_SIDE + slippage_bps_side) / 10_000) * (entry_px + "
                    "exit_px); cost_r = cost_px / risk_px; net_r_twin = gross_r - cost_r "
                    "(tierc10_data.haircut_twin_net_r / haircut_twin_for_stem — importable, so "
                    "Stage B never re-derives a tier)",
        "tc_series_toll_untouched": all(
            r["round_trip_bps_used"] == float(R2.FEE_BPS_ROUND_TRIP) for r in fees["assets"]),
        "rows": rows,
    }


MAKER_LAW = (
    "MAKER — THE DATA LAW [L-D.17]: maker_bps_side is filed PER VENUE (`venues[<VENUE>]`), with its "
    "source and kind: the venue's published entry-tier USDT-margined maker rate when its page was "
    "retrieved and parsed from saved bytes (PUBLISHED), else the figure on file in README.md "
    "(ON FILE — NOT RE-CONFIRMED), applied to Bybit as an ASSUMPTION. A maker leg carries the "
    "maker_slippage_bps_side of TC11's rows (carried). By the operator's ruling of the filing day "
    "of the contract (\"maker as toll of record for scalper mode\") the maker rate is a toll of "
    "record; WHICH LEGS pay it is defined by the registration texts and the stage that rides them, "
    "not by this file. Taker and charter tiers are unchanged and equal to TC11's file.")
TC11_EQUAL_TOP = ("fee_law", "haircut_twin_law", "haircut_twin_clause", "haircut_twin_tiers",
                  "charter_slippage_tiers", "charter_slippage_source")
TC11_EQUAL_ROW = ("asset", "venue", "symbol", "stem", "taker_bps_side_used", "round_trip_bps_used",
                  "kind", "source", "haircut_twin_tier", "haircut_twin_slippage_bps_side",
                  "haircut_twin_bps_side", "haircut_twin_round_trip_bps", "haircut_twin_kind",
                  "haircut_twin_source", "charter_slippage_tier", "charter_slippage_bps_per_side",
                  "charter_slippage_source", "maker_slippage_bps_side", "venue_note")
FEE_PCT_GROUP = "pct"                         # the named capture of every grammar pattern
FEE_ROW_GROUP = "row"


def pct_to_bps(pct: Fraction) -> Fraction:
    """THE ONE CONVERSION [L-D.18]: bps = percent x BPS_PER_UNIT / PCT_PER_UNIT — the two unit
    objects of scripts/tierc12_units.py; exact (a Fraction in, a Fraction out)."""
    return pct * UNITS.BPS_PER_UNIT / UNITS.PCT_PER_UNIT


def extract_fee(body: bytes, grammar: dict) -> dict:
    """Act 2 — EXTRACTION [L-D.18]: the grammar of record applied to saved bytes.  `grammar` is
    one venue's entry of FEE_GRAMMAR.json: `entry_tier_label` (a pattern), optionally `scope` (a
    pattern whose named group `row` holds the entry tier's own text, searched from each label
    match), `maker` and `taker` (lists of patterns, each with the named group `pct` capturing a
    percent as written).  Per label occurrence the qualifying figures are the POSITIVE ones (a zero
    or negative figure is a rebate or a promotion, never a base rate) and the HIGHEST is taken; if
    two occurrences give different values the venue is `ambiguous`.  Percents are parsed exactly
    (fractions.Fraction on the captured text).  A null grammar returns its filed reason.
    Returns {label_found, label_text, maker_pct, taker_pct, maker_reason, taker_reason,
    maker_figures, taker_figures} — percents as Fractions, None when unretrievable."""
    out = {"label_found": False, "label_text": None, "maker_pct": None, "taker_pct": None,
           "maker_reason": None, "taker_reason": None, "maker_figures": [], "taker_figures": []}
    if grammar.get("null_grammar"):
        out["maker_reason"] = out["taker_reason"] = grammar["reason"]
        return out
    text = body.decode("utf-8", errors="replace")
    labels = list(re.finditer(grammar["entry_tier_label"], text))
    if not labels:
        out["maker_reason"] = out["taker_reason"] = "no_entry_tier_label"
        return out
    out["label_found"] = True
    out["label_text"] = sorted({m.group() for m in labels})
    for side in ("maker", "taker"):
        values = []
        for m in labels:
            scope = text[m.start():]
            if grammar.get("scope"):
                sm = re.search(grammar["scope"], scope)
                scope = sm.group(FEE_ROW_GROUP) if sm else ""
            figs = [Fraction(x.group(FEE_PCT_GROUP)) for rx in grammar[side] for x in re.finditer(rx, scope)]
            out[side + "_figures"] += [str(f) for f in figs]
            pos = [f for f in figs if f > Fraction()]
            if pos:
                values.append(max(pos))
        if not values:
            out[side + "_reason"] = "no_rate_in_body"
        elif min(values) != max(values):
            out[side + "_reason"] = "ambiguous"
        else:
            out[side + "_pct"] = max(values)
    return out


def load_fee_grammar(out: Path | None = None) -> tuple[dict, str | None]:
    """(FEE_GRAMMAR.json — the tracked DATA record of the grammars of record, {} when absent, its
    sha256 or None)."""
    p = (out or OUT) / FEE_GRAMMAR
    if not p.exists():
        return {}, None
    return json.loads(p.read_text(encoding="utf-8")), file_sha256(p)


def fee_pins(out: Path | None = None) -> dict:
    """THE MAKER PIN PER VENUE [L-D.18, O-19], from sealed bytes and the grammar of record — no
    network, no clock.  PUBLISHED only if ALL hold: HTTP 200; the final URL's host is under the
    venue's own domain; the body holds the entry tier's label; the grammar yields a qualifying
    maker figure and, after the highest-of rule, exactly one value > 0.  Otherwise the venue is
    UNRETRIEVABLE with a reason of the closed set and carries the figure ON FILE (README), flagged.

    HALTS IF: FEE_SOURCE.json is not filed; a venue captured with HTTP 200 has no grammar of record
    or one written against another body; or a saved body is not the bytes the record pins."""
    out = out or OUT
    p = out / FEE_SOURCE
    if not p.exists():
        halt(f"no {FEE_SOURCE} at {p} — the fee-source capture has not run")
    src = json.loads(p.read_text(encoding="utf-8"))
    grammar, grammar_sha = load_fee_grammar(out)
    ok = requests.codes.ok
    pins = {}
    for venue in venues_of_record():
        s = src["venues"][venue]
        row = {"venue": venue, "url": s["url"], "attempted_utc_date": s["retrieved_utc_date"],
               "http_status": s["http_status"], "body_sha256": s["body_sha256"], "reason": None,
               "label": None, "maker_pct": None, "taker_pct": None, "taker_reason": None,
               "grammar": None, "published": False}
        if s["http_status"] is None:
            row["reason"] = "transport"
        elif s["http_status"] != ok:
            row["reason"] = f"http_{s['http_status']}"
        else:
            g = (grammar.get("venues") or {}).get(venue)
            if g is None:
                halt(f"{venue}: its fee page was captured with HTTP {ok} and no grammar of record "
                     f"exists in {FEE_GRAMMAR} — --manifest waits for the ruled grammar [L-D.18]")
            if g.get("body_sha256") != s["body_sha256"]:
                halt(f"{venue}: the grammar of record was written against body {g.get('body_sha256')}, "
                     f"not the captured body {s['body_sha256']}")
            body = Path(s["body_path"]).read_bytes()
            if sha_bytes(body) != s["body_sha256"]:
                halt(f"{venue}: the saved body is not the bytes {FEE_SOURCE} pins")
            row["grammar"] = {"record": DATA_REL + "/" + FEE_GRAMMAR, "sha256": grammar_sha,
                              "amendment": g.get("amendment")}
            host = urlparse(s["final_url"] or "").hostname or ""
            ex = extract_fee(body, g)
            row["label"] = ex["label_text"]
            row["taker_pct"], row["taker_reason"] = ex["taker_pct"], ex["taker_reason"]
            if not (host == s["venue_domain"] or host.endswith("." + s["venue_domain"])):
                row["reason"] = "off_domain_redirect"
                row["taker_pct"] = None
            elif ex["maker_pct"] is None:
                row["reason"] = ex["maker_reason"]
            else:
                row["maker_pct"] = ex["maker_pct"]
                row["published"] = True
        pins[venue] = row
    return pins


# ported from scripts/tierc11_data.py:1895-1973 @ sha256 b2fe090f4a6cefe4 — CHANGED: maker_bps_side per VENUE from the venue block (published, or on file and flagged); TC11's row keys kept and held equal; no top-level maker scalar [L-D.19]
def fee_schedule(assets: list[dict], funding: dict, pin: dict, pins: dict, out: Path | None = None) -> dict:
    """TC12's fee file [L-D.19].  The estate's flat taker figure per asset, READ from
    tierc2_rules, never typed (the toll of record of the TC-series — NOT a venue schedule); the
    charter slippage tiers; and THE MAKER PIN per venue — `pins` is `fee_pins()`.  Six top-level
    keys and nineteen row keys are asserted EQUAL to TC11's file (its sha held to TC11's
    PROGRESS).  This function holds NO numeric literal (F-TOLL [data a])."""
    out = out or OUT
    rules, cfg = ROOT / "scripts" / "tierc2_rules.py", ROOT / "configs" / "naiad_v0.yaml"
    src = [f"scripts/tierc2_rules.py:{_source_line(rules, 'FEE_BPS_SIDE: float')}",
           f"scripts/tierc2_rules.py:{_source_line(rules, 'FEE_BPS_ROUND_TRIP: float')}",
           f"configs/naiad_v0.yaml:{_source_line(cfg, 'fee_bps_side')}"]
    slip_src = [f"Naiad_Phase0_Charter.md:{_source_line(CHARTER_SOURCE, CHARTER_SLIPPAGE_NEEDLE)}",
                f"scripts/tierc10_data.py:{_CLAUSE_L1}-{_CLAUSE_L2} (CONTRACT_SLIPPAGE_CLAUSE, "
                "read by AST)"]
    tc11 = json.loads(tc11_read(T11_REL + "/data/fee_schedule.json"))
    tc11_rows = {r["stem"]: r for r in tc11["assets"]}
    xman = json.loads(PG.read_certified(X_MANIFEST_REL, ROOT))
    xrow = [f for f in xman["files"] if f.get("copy") == X_FEE_REL]
    xraw = (MAIN_TREE / X_FEE_REL).read_bytes()
    if not xrow or [f["sha256"] for f in xrow] != [sha_bytes(xraw)]:
        halt(f"{X_FEE_REL} is not the bytes its X_REC_MANIFEST.json row pins")
    x_assumed = sorted({float(r["maker_bps_per_side"]) for r in json.loads(xraw)["assets"]})
    if not x_assumed or min(x_assumed) != max(x_assumed):
        halt(f"X's fee file holds {len(x_assumed)} maker figures over its rows, not one")
    on_file_source = f"README.md:{MAKER_SOURCE_LINE} — {MAKER_SOURCE_TEXT!r}"
    source_record = {"path": DATA_REL + "/" + FEE_SOURCE, "sha256": file_sha256(out / FEE_SOURCE)}
    venues = {}
    for venue, q in pins.items():
        stems = [a["stem"] for a in assets if a["venue"] == venue]
        slips = sorted({float(tc11_rows[s]["maker_slippage_bps_side"]) for s in stems})
        if not slips or min(slips) != max(slips):
            halt(f"{venue}: TC11's maker_slippage_bps_side is not uniform over its rows: {slips}")
        maker = float(pct_to_bps(q["maker_pct"])) if q["published"] else float(MAKER_BPS_SIDE)
        kind = (MAKER_PUBLISHED if q["published"] else
                MAKER_ASSUMED if venue == "BYBIT_V5_LINEAR" else MAKER_ON_FILE)
        taker_pub = None if q["taker_pct"] is None else float(pct_to_bps(q["taker_pct"]))
        venues[venue] = {
            "stems": stems,
            "maker_bps_side": maker,
            "maker_round_trip_bps": maker + maker,
            "maker_slippage_bps_side": min(slips),
            "maker_kind": kind,
            "maker_basis": (f"{FEE_DEFINITION}; entry-tier label found: {q['label']}" if q["published"] else
                            f"UNRETRIEVABLE ({q['reason']}): the figure on file is carried — "
                            f"{on_file_source}"),
            "maker_unretrievable_reason": q["reason"],
            "maker_source_url": q["url"],
            "maker_retrieved_utc_date": q["attempted_utc_date"] if q["published"] else None,
            "maker_retrieval_attempted_utc_date": q["attempted_utc_date"],
            "maker_retrieval_http_status": q["http_status"],
            "maker_source_record": source_record,
            "maker_source_body_sha256": q["body_sha256"],
            "maker_grammar": q["grammar"],
            "maker_on_file_bps_side": float(MAKER_BPS_SIDE),
            "maker_on_file_source": on_file_source,
            "maker_equals_on_file": maker == float(MAKER_BPS_SIDE),
            "taker_bps_side": float(R2.FEE_BPS_SIDE),
            "taker_round_trip_bps": float(R2.FEE_BPS_ROUND_TRIP),
            "taker_kind": min({tc11_rows[s]["kind"] for s in stems}),
            "taker_published_bps_side": taker_pub,
            "taker_published_note": "DISCLOSURE ONLY — no reader consumes it; the taker of record is "
                                    "the estate's object (contract: 'taker … unchanged')",
        }
    rows = []
    for a in assets:
        fu = funding.get(a["stem"], {})
        bybit = a["venue"] == "BYBIT_V5_LINEAR"
        v = venues[a["venue"]]
        row = {
            "asset": a["asset"], "venue": a["venue"], "symbol": a["symbol"], "stem": a["stem"],
            "taker_bps_side_used": float(R2.FEE_BPS_SIDE),
            "round_trip_bps_used": float(R2.FEE_BPS_ROUND_TRIP),
            "kind": "ASSUMPTION — the estate's flat FEE_BPS_SIDE object, NOT a venue schedule",
            "source": src,
            "haircut_twin_tier": tier_of(a["asset"]),
            "haircut_twin_slippage_bps_side": slippage_bps_side(a["asset"]),
            "haircut_twin_bps_side": charter_bps_side(a["asset"]),
            "haircut_twin_round_trip_bps": charter_round_trip_bps(a["asset"]),
            "haircut_twin_kind": ("CHARTER MODEL — an ADDED column beside the TC-series toll; "
                                  "round_trip_bps_used above is untouched and stays the "
                                  "accounting figure of record [VETO 'tiers']"),
            "haircut_twin_source": CONTRACT_SLIPPAGE_CLAUSE,
            "venue_note": ("Bybit's published base taker rate for linear perpetuals is NOT "
                           "fetched here (signed endpoint) and is widely quoted ABOVE 5.0 bps "
                           "[UNVERIFIED, general knowledge]; the estate figure is applied "
                           "unchanged and that is the assumption of record"
                           if bybit else
                           "Binance USDT-M per-account commissionRate is a signed endpoint; "
                           "not fetched"),
            "funding_interval_hours_observed_tail": fu.get("interval_hours_observed_tail"),
            "funding_interval_hours_observed_modal": fu.get("interval_hours_observed_modal"),
            "funding_spacing_hours_histogram": fu.get("spacing_hours_histogram"),
            # ── the maker keys: FROM THE VENUE BLOCK [L-D.19] ──
            "maker_bps_side": v["maker_bps_side"],
            "maker_bps_per_side": v["maker_bps_side"],
            "maker_round_trip_bps": v["maker_round_trip_bps"],
            "maker_slippage_bps_side": v["maker_slippage_bps_side"],
            "maker_kind": v["maker_kind"],
            "maker_source": [v["maker_source_url"],
                             f"{source_record['path']} sha256 {source_record['sha256']}",
                             on_file_source],
            "charter_slippage_tier": tier_of(a["asset"]),
            "charter_slippage_bps_per_side": slippage_bps_side(a["asset"]),
            "charter_slippage_source": slip_src,
        }
        moved = [k for k in TC11_EQUAL_ROW if row[k] != tc11_rows[a["stem"]][k]]
        if moved:
            halt(f"fee row {a['stem']}: {moved} differ from TC11's file — 'taker and charter tiers unchanged'")
        rows.append(row)
    doc = {"tier": TIER, "stage": STAGE, "seed": SEED,
           "as_of_last_closed_4h": pin["as_of_last_closed_4h"],
           "as_of_last_closed_4h_open": pin["as_of_last_closed_4h_open"],
           "warranty": WARRANTY, "fee_law": "fee = (FEE_BPS_SIDE / 10_000) * (entry_px + exit_px) "
                                           "(scripts/tierc2_baseline.py)",
           "haircut_twin_law": ("ADDED, never a replacement: haircut_twin_* keys carry the "
                                "charter model (per-side taker fee + the charter's per-side "
                                "slippage tier) beside round_trip_bps_used, which stays the "
                                "TC-series accounting figure on every row [VETO 'tiers']. "
                                "twin cost_px = ((FEE_BPS_SIDE + slippage_bps_side) / 10_000) * "
                                "(entry_px + exit_px); net_r_twin = gross_r - cost_px / risk_px "
                                "(tierc10_data.haircut_twin_net_r)"),
           "haircut_twin_clause": CONTRACT_SLIPPAGE_CLAUSE,
           "haircut_twin_tiers": {t: {"bps_per_side": b["bps"], "assets": list(b["assets"])}
                                  for t, b in sorted(SLIPPAGE_TIERS.items())},
           "charter_slippage_tiers": {t: {"bps_per_side": b["bps"], "assets": list(b["assets"])}
                                      for t, b in sorted(SLIPPAGE_TIERS.items())},
           "charter_slippage_source": slip_src,
           "venues": venues,
           "maker_pin": {"name": "maker-bps",
                         "values": {v: venues[v]["maker_bps_side"] for v in venues},
                         "kinds": {v: venues[v]["maker_kind"] for v in venues},
                         "x_assumed_bps_side": min(x_assumed),
                         "x_assumed_source": {"path": X_FEE_REL, "sha256": sha_bytes(xraw),
                                              "certified_by": X_MANIFEST_REL},
                         "differs_from_x_assumption": {v: venues[v]["maker_bps_side"] != min(x_assumed)
                                                       for v in venues}},
           "maker_law": MAKER_LAW,
           "tc11_fee_schedule": {"path": T11_REL + "/data/fee_schedule.json",
                                 "sha256": tc11_certified(T11_REL + "/data/fee_schedule.json"),
                                 "keys_compared_top": list(TC11_EQUAL_TOP),
                                 "keys_compared_row": list(TC11_EQUAL_ROW),
                                 "all_equal": True},
           "keys_removed_vs_tc11": {
               "maker_bps_per_side (top level)": "a scalar cannot carry two venues",
               "maker_source (top level)": "replaced by the per-venue block"},
           "assets": rows}
    moved = [k for k in TC11_EQUAL_TOP if doc[k] != tc11[k]]
    if moved:
        halt(f"fee_schedule: top-level {moved} differ from TC11's file — 'taker and charter tiers unchanged'")
    return doc


def pin_lines(fees: dict) -> list[str]:
    """THE PIN LINE [L-D.21], one per venue, then X's assumption — every number read from the fee
    document handed in:
    PIN ["maker-bps"] <VENUE> <bps> bps/side (<round trip> round trip) · <kind> · <url> ·
    retrieved <date or "—"> · body sha <8 hex or "—">"""
    out = []
    for venue, v in fees["venues"].items():
        sha = v["maker_source_body_sha256"]
        out.append(f'PIN ["maker-bps"] {venue} {v["maker_bps_side"]} bps/side '
                   f'({v["maker_round_trip_bps"]} round trip) · {v["maker_kind"]} · '
                   f'{v["maker_source_url"]} · retrieved {v["maker_retrieved_utc_date"] or "—"} · '
                   f'body sha {sha[:8] if sha else "—"}')
    mp = fees["maker_pin"]
    x = mp["x_assumed_bps_side"]
    out.append(f"X assumed {x} bps/side ({x + x} round trip); differs: "
               + ", ".join(f"{v}: {d}" for v, d in mp["differs_from_x_assumption"].items()))
    return out


# ═══════════════════════════════════════════════ 9b · THE TICK OF RECORD AND THE GRID AUDIT [L-D.22, O-20, O-27]
TICK_AUDIT = "TICK_GRID_AUDIT.json"
SEGMENTS = ("tuning", "holdout_to_tc11_pin", "strip")


def table_decimals() -> int:
    """The lineage's table rounding: the default of `nd` in tierc2_baseline._round_floats, READ
    from the signature by AST (scripts/tierc2_baseline.py is not imported here)."""
    for fn in ast.parse((ROOT / TB_REL).read_text(encoding="utf-8")).body:
        if isinstance(fn, ast.FunctionDef) and fn.name == "_round_floats":
            names = [a.arg for a in fn.args.args]
            defaults = dict(zip(names[len(names) - len(fn.args.defaults):], fn.args.defaults))
            if "nd" in defaults and isinstance(defaults["nd"], ast.Constant):
                return defaults["nd"].value
    halt(f"{TB_REL}: _round_floats has no literal default for `nd`")


def ticks_of_record(out: Path | None = None) -> dict:
    """{stem: price_tick STRING} from this stage's own capture [L-D.22].  HALTS IF a panel stem
    lacks one or a tick is not a string."""
    specs = load_contract_specs(out)
    if specs is None:
        halt(f"no {CONTRACT_SPECS} — the tick of record is not captured yet")
    got = {a["stem"]: a["price_tick"] for a in specs["assets"]}
    for stem in PANEL17:
        if type(got.get(stem)) is not str:
            halt(f"{stem}: no price_tick string in {CONTRACT_SPECS}")
    return {stem: got[stem] for stem in PANEL17}


def segment_of(close_ms):
    """The segment index of each bar by its CLOSE (an int64 array of closes): tuning
    (<= ERA_CUT_MS) · holdout to TC11's pin · strip (TC11's pin < close <= the pin)."""
    return (close_ms > ERA_CUT_MS).astype(np.int64) + (close_ms > TC11_PIN_CLOSE_MS).astype(np.int64)


def tick_grid_audit(pin: dict, out: Path | None = None, root: Path | None = None) -> dict:
    """data/TICK_GRID_AUDIT.json [L-D.22] — determinism set; no network, no clock.
    ON-GRID SHARES, computed EXACTLY (TickGrid.on_grid on the unique values of each column,
    weighted by their counts): for every stem x lens in {5m, 1h} x segment x price field — n,
    n_on_grid, the share as the exact fraction and as a float at the lineage's table rounding, and
    the last off-grid bar's open.
    OBSERVED GRANULARITY PER CALENDAR MONTH (5m, the four price fields pooled): the coarsest
    decimal grid that contains every unique price of the month — the gcd of the prices in integer
    units of the finest decimal place present — beside the recorded tick, with the flag
    `coarser_than_recorded_tick`; every flagged month LISTED (O-27)."""
    close_ms = int(pin["as_of_last_closed_4h_close_ms"])
    ticks = ticks_of_record(out)
    nd = table_decimals()
    cells, monthly, coarser = {}, {}, []
    for stem in PANEL17:
        grid = TickGrid(ticks[stem])
        frames = {}
        for iv in AUDIT_LENSES:
            d = pd.read_parquet(kline_path(stem, iv, root)).sort_values("open_time")
            frames[iv] = d[d["open_time"] + STEP_MS[iv] <= close_ms].reset_index(drop=True)
        uniq = np.unique(np.concatenate([frames[iv][f].to_numpy(np.float64)
                                         for iv in AUDIT_LENSES for f in PRICE_FIELDS]))
        decs = [grid.dec(float(x)) for x in uniq]
        on = np.array([grid.on_grid(d) for d in decs], dtype=bool)
        for iv in AUDIT_LENSES:
            f = frames[iv]
            t = f["open_time"].to_numpy(np.int64)
            seg = segment_of(t + STEP_MS[iv])
            for field in PRICE_FIELDS:
                ok = on[np.searchsorted(uniq, f[field].to_numpy(np.float64))]
                for k, name in enumerate(SEGMENTS):
                    m = seg == k
                    n, n_on = int(m.sum()), int((ok & m).sum())
                    off = t[m & ~ok]
                    cells[f"{stem}|{iv}|{name}|{field}"] = {
                        "n": n, "n_on_grid": n_on, "share": f"{n_on}/{n}",
                        "share_float": round(n_on / n, nd) if n else None,
                        "last_off_grid_open_ms": int(off.max()) if len(off) else None,
                        "last_off_grid_open": iso(int(off.max())) if len(off) else None}
        # ── the observed granularity per calendar month (5m, O/H/L/C pooled) ──
        f5 = frames["5m"]
        finest = min(d.normalize().as_tuple().exponent for d in decs)
        units = np.array([int(d.scaleb(-finest)) for d in decs], dtype=np.int64)
        month = pd.to_datetime(f5["open_time"], unit="ms", utc=True).dt.strftime("%Y-%m").to_numpy()
        pooled = pd.DataFrame({
            "month": np.concatenate([month for _ in PRICE_FIELDS]),
            "units": np.concatenate([units[np.searchsorted(uniq, f5[f].to_numpy(np.float64))]
                                     for f in PRICE_FIELDS])})
        recorded = Decimal(ticks[stem])
        per = {}
        for mon, g in pooled.groupby("month", sort=True)["units"]:
            u = np.unique(g.to_numpy(np.int64))
            gran = Decimal(int(np.gcd.reduce(u))).scaleb(finest)
            flag = bool(gran > recorded)
            per[mon] = {"observed_granularity": format(gran, "f"), "recorded_tick": ticks[stem],
                        "coarser_than_recorded_tick": flag, "n_unique_prices": int(len(u)),
                        "n_bars": int(len(g) // len(PRICE_FIELDS))}
            if flag:
                coarser.append({"stem": stem, "month": mon, "observed_granularity": format(gran, "f"),
                                "recorded_tick": ticks[stem]})
        monthly[stem] = per
    return {
        "tier": TIER, "stage": STAGE, "seed": SEED,
        "as_of_last_closed_4h": pin["as_of_last_closed_4h"],
        "as_of_last_closed_4h_open": pin["as_of_last_closed_4h_open"],
        "warranty": WARRANTY,
        "law": "the tick of record is the price_tick STRING of TC12's own CONTRACT_SPECS.json capture "
               "(a point-in-time venue spec taken at the fetch run), applied over the whole corridor "
               "[O-20]. On-grid shares are EXACT (TickGrid on unique values, integer counts). The "
               "monthly column is the measurement O-27 orders: 'stricter than history' is claimed "
               "only where the tape's observed granularity is <= the recorded tick; an era whose "
               "tick was FINER shows as off-grid shares, an era whose tick was COARSER leaves every "
               "price on today's grid and shows only in the monthly column",
        "tick_source": {"path": DATA_REL + "/" + CONTRACT_SPECS,
                        "sha256": file_sha256((out or OUT) / CONTRACT_SPECS), "key": "assets[].price_tick"},
        "ticks": ticks,
        "lenses": list(AUDIT_LENSES), "fields": list(PRICE_FIELDS), "segments": {
            SEGMENTS[0]: f"close <= {ERA_CUT_MS} (the era cut of TC11's shim, read by AST)",
            SEGMENTS[1]: f"{ERA_CUT_MS} < close <= {TC11_PIN_CLOSE_MS} (TC11's pin)",
            SEGMENTS[2]: f"{TC11_PIN_CLOSE_MS} < close <= {close_ms} (the pin)"},
        "share_float_decimals": nd,
        "cell_key": "<stem>|<lens>|<segment>|<field>",
        "cells": cells,
        "monthly_granularity_lens": "5m",
        "monthly_granularity": monthly,
        "months_measured": sum(len(v) for v in monthly.values()),
        "coarser_months": coarser,
        "n_coarser_months": len(coarser),
        "never_looser": ("MEASURED: no month's observed granularity is coarser than the recorded tick"
                         if not coarser else
                         f"NOT HELD on {len(coarser)} stem-month(s) — listed under coarser_months [O-27]"),
    }


def tick_of_record_block(ticks: dict, out: Path | None = None) -> dict:
    """The manifest block `tick_of_record` [L-D.22]: per stem, TC12's and TC11's price_tick,
    qty_step, min_notional_usdt and status, and `equal_as_decimal` (so "0.10" equals "0.1")."""
    mine = {a["stem"]: a for a in load_contract_specs(out)["assets"]}
    theirs = {a["stem"]: a for a in json.loads(tc11_read(T11_REL + "/data/CONTRACT_SPECS.json"))["assets"]}
    keys = ("price_tick", "qty_step", "min_notional_usdt", "status")
    rows = {}
    for stem in PANEL17:
        a, b = mine[stem], theirs[stem]
        rows[stem] = {"tc12": {k: a.get(k) for k in keys}, "tc11": {k: b.get(k) for k in keys},
                      "equal_as_decimal": Decimal(a["price_tick"]) == Decimal(b["price_tick"]),
                      "tick_used": ticks[stem]}
    moved = sorted(s for s, r in rows.items() if not r["equal_as_decimal"])
    return {"law": "TC12's capture is of record (O-20); TC11's is printed beside it. A moved tick is "
                   "printed here and entered by the executor in DISCLOSURES_BUILD.md at the TC12-D gate",
            "tc12_capture": {"path": DATA_REL + "/" + CONTRACT_SPECS,
                             "sha256": file_sha256((out or OUT) / CONTRACT_SPECS)},
            "tc11_capture": {"path": T11_REL + "/data/CONTRACT_SPECS.json",
                             "sha256": tc11_certified(T11_REL + "/data/CONTRACT_SPECS.json")},
            "audit": DATA_REL + "/" + TICK_AUDIT,
            "ticks_moved_vs_tc11": moved,
            "per_stem": rows}


def zero_volume_block(close_ms: int, root: Path | None = None) -> dict:
    """The manifest block `zero_volume_bars` [L-D.16]: for all 17 stems x native lens, the count
    of zero-volume flat bars (the predicate of record) and of zero-volume bars, split by segment."""
    per = {}
    for stem in PANEL17:
        for iv in lenses_of(stem):
            if iv in DERIVED_IVS:
                continue
            d = pd.read_parquet(kline_path(stem, iv, root)).sort_values("open_time")
            d = d[d["open_time"] + STEP_MS[iv] <= close_ms]
            o, h, l, c, v = (d[k].to_numpy(np.float64) for k in KLINE_COLS[1:])
            seg = segment_of(d["open_time"].to_numpy(np.int64) + STEP_MS[iv])
            zf, z = is_zero_volume_flat(o, h, l, c, v), v == 0
            per[f"{stem}|{iv}"] = {
                "zero_volume_flat_bars": {name: int((zf & (seg == k)).sum()) for k, name in enumerate(SEGMENTS)},
                "zero_volume_bars": {name: int((z & (seg == k)).sum()) for k, name in enumerate(SEGMENTS)},
                "zero_volume_flat_bars_total": int(zf.sum()), "zero_volume_bars_total": int(z.sum())}
    return {"law": "a zero-volume flat bar (o == h == l == c and volume == 0) is a bar the VENUE "
                   "published during an outage: KEPT, COUNTED, attributed to the venue (F-D-2 [4]), "
                   "never removed, filled or altered; no loader drops it; it COUNTS AS ONE BAR in every "
                   "bar count of every consumer [L-D.16]",
            "predicate": "scripts/tierc12_data.py is_zero_volume_flat(o, h, l, c, v)",
            "segments": list(SEGMENTS), "key": "<stem>|<native lens>",
            "per_file": per}


# ═══════════════════════════════════════════════ 10 · THE MANIFEST (no network, no snapshot write, no clock)
# ported from scripts/tierc11_data.py:1978-2001 @ sha256 b2fe090f4a6cefe4 — VERBATIM
def premise_checks(probe: dict) -> list[dict]:
    """The contract's venue premises, held against the probe of record.  A
    premise the venue contradicts is printed as STALE in the FILED manifest,
    not only in a run log."""
    by = {a["asset"]: a for a in probe["unseen12"]}
    out = []
    for name, premise in (
            ("XMR", "alternate venue only where Binance lacks history — 'XMR post-delisting'"),
            ("HYPE", "alternate venue 'if absent' from Binance"),
            ("MNT", "alternate venue 'if absent' from Binance")):
        a = by[name]
        on_binance = a.get("venue") == "BINANCE_USDTM"
        verdict = (
            f"STALE — {a['symbol']} is a {a['status']} Binance USDT-M {a['contract_type']} "
            f"(listed {a['listing']}); the WHOLE tape is Binance, no alternate venue is used and "
            f"no splice question arises" if name == "XMR" and on_binance else
            f"NOT TRIGGERED — {a['symbol']} is a {a['status']} Binance USDT-M contract; default "
            f"venue, whole tape" if on_binance else
            f"TRIGGERED — absent from Binance USDT-M; the WHOLE tape is {a.get('venue')} "
            f"(stem {a.get('stem')}), one venue, never spliced" if a.get("venue") else
            "TRIGGERED — absent from Binance and no alternate venue found: EXCLUDED by name")
        out.append({"asset": name, "contract_premise": premise, "venue_of_record": a.get("venue"),
                    "binance_probe": a.get("binance"), "verdict": verdict})
    return out


OPERATOR_RULINGS = (
    "CARRIED FROM TC10, STILL OPEN: F-D-1 (which of the venue's two publications, REST or the "
    "BULK ARCHIVE, is the record on incident bars). TC12, like TC10 and TC11, fetched REST only; its "
    "rows past each TC11 edge are REST by construction. TC12 runs no such leg and re-cuts nothing.",
    "CARRIED FROM TC10, STILL OPEN: PUMPFUN -> PUMPUSDT [LEAN D-d] and MNT -> Bybit v5 linear "
    "[LEAN D-c] await the operator's nod (default: as TC10's table).",
    "CARRIED FROM TC10, STILL OPEN: whether charter slippage joins the toll of record (default: a "
    "twin only — the contract says the tiers are unchanged).",
    f"THE LaCie MIRROR [L-D.24; the resume paste's \"mirror\"]: default destination "
    f"/Volumes/LaCie/Naiad/snapshots/{SNAPSHOT_NAME}/ (+ /Volumes/LaCie/Naiad/provenance/{SNAPSHOT_NAME}/), a "
    "sha-verified plain copy by `tierc12_data.py --mirror` when the drive is reachable; its status is "
    "in data/MIRROR_ATTEST.json and progress/TC12-D.mirror.json, never here. The TC10 and TC11 "
    "snapshots stay UNMIRRORED and are LISTED for ATHENA: ~/.cache/naiad/snapshots/tc10_20260921, "
    "~/.cache/naiad/snapshots/tc11_20260925.",
    "THE \"maker-bps\" PIN (veto by name, contract :137): per venue, the published base rate when "
    "the page is retrieved and parsed; otherwise the figure on file (README.md) flagged NOT "
    "RE-CONFIRMED, applied to Bybit as an ASSUMPTION. A figure given by the operator replaces it "
    "and is recorded as his.",
)
STANDING_DISCLOSURES = (
    "The R0 scout's three unauthenticated GETs (scout map U4, section 1.16: Binance /fapi/v1/time, "
    "one BTCUSDT 4h kline, one Bybit MNTUSDT 4h kline) are NOT the venue proof of the pin: they are "
    "in no FETCH_LOG and nothing they returned was saved. The proof is AS_OF_PIN.json's.",
    "Before this module first ran, the executor resolved the three hostnames it would use "
    "(fapi.binance.com, api.bybit.com, data.binance.vision) by DNS only — a name lookup, no HTTP "
    "request to any venue; nothing was returned by a venue and nothing was saved.",
    "At TC11's pin every one of the 17 funding tapes holds exactly one print of that hour (16 "
    "Binance tapes stamped a few ms past the pin instant, MNT stamped exactly at it); it is "
    "INHERITED, kept by the floor-hour law, and belongs to the bar that OPENS at TC11's pin — the "
    "first bar of the forward strip.",
    "The 15m tapes of the nine non-CLASSIC5 stems that hold one, the 1m tapes, the out-of-panel "
    "stems' tapes and the root MANIFEST.json stay in the snapshot untouched and out of scope "
    "(listed by sha under out_of_scope_snapshot_files); several end in 2026-08 or at TC10's edge.",
    "No TC12 stage reads 15m; the five CLASSIC5 15m tapes are extended only so that no in-scope "
    "file ends short of the pin.",
)
CARRIED_KEYS = d11_const("CARRIED_KEYS")
MIRROR_SENTENCE = ("see data/MIRROR_ATTEST.json — a provenance record outside the determinism set; the "
                   "mirror's status is not carried here")
# TC11's manifest schema -> TC12's: the renames of L-D.11 (and no other)
MANIFEST_RENAMES_TOP = {"tc11_extension": "tc12_extension", "carried_from_tc10": "carried_from_tc11"}
MANIFEST_RENAMES_ROW = {"tc11_rows_added": "tc12_rows_added", "tc10_manifest_sha256": "tc11_manifest_sha256"}
MANIFEST_NEW_TOP = ("tc11_record", "pins", "tick_of_record", "fee_sources", "zero_volume_bars")


# ported from scripts/tierc11_data.py:2030-2031 (_tc10_manifest) @ sha256 b2fe090f4a6cefe4 — CHANGED: TC11's manifest (its sha held to TC11's PROGRESS) is the previous record
def _tc11_manifest() -> tuple[dict, str]:
    raw = tc11_read(T11_REL + "/data/STAGE_D_MANIFEST.json")
    return json.loads(raw), sha_bytes(raw)


# ported from scripts/tierc11_data.py:2034-2072 @ sha256 b2fe090f4a6cefe4 — TEXT-ONLY: the keys and the disclosure sentence name the TC11 -> TC12 inheritance
def cache_manifest_staleness(q: Path, files: list[dict], other: list[dict],
                             extended: list[str]) -> dict:
    """The snapshot root's MANIFEST.json, DESCRIBED (never used): what it says of itself, and how
    many of the files it lists it still describes at their TC12 bytes.  Read-only; the shas
    compared are the ones this manifest already computed for files[] and
    out_of_scope_snapshot_files[]."""
    doc = json.loads(q.read_text(encoding="utf-8"))
    known = {f["path"]: f.get("sha256") for f in files} | {o["path"]: o["sha256"] for o in other}
    listed = [(e.get("rel_path"), e.get("sha256")) for e in doc.get("files", [])]
    at_bytes = sorted(p for p, s in listed if p in known and known[p] == s)
    in_scope_listed = sorted(p for p, _ in listed if p in {f["path"] for f in files})
    ext_described = sorted(set(at_bytes) & set(extended))
    selfd = {k: doc.get(k) for k in ("created_utc", "mode", "file_count", "total_bytes",
                                     "repo_head", "naiad_cache_dir_override")}
    absent = sum(1 for p, _ in listed if p not in known)
    stale = len(at_bytes) < len(known) or absent > 0
    return {
        "stale": stale,
        "self_described": selfd,
        "listed_files": len(listed),
        "listed_files_absent_from_the_tc12_snapshot": absent,
        "listed_files_at_their_tc12_bytes": len(at_bytes),
        "in_scope_files_it_lists": len(in_scope_listed),
        "tc12_extended_files": len(extended),
        "tc12_extended_files_it_describes_at_their_tc12_bytes": len(ext_described),
        "disclosure": (
            f"The snapshot root's MANIFEST.json ({q.stat().st_size} B, sha256 "
            f"{file_sha256(q)[:16]}…) is carried byte-for-byte from the TC11 snapshot; TC11's "
            "manifest pins it by sha (CLONE_ATTEST compares it with that record). "
            "It is a cache manifest written by another estate (self-described "
            f"created_utc {selfd['created_utc']}, mode {selfd['mode']!r}, {len(listed)} files) and "
            f"it is {'STALE' if stale else 'CURRENT'}: of the other {len(known)} files of the TC12 "
            f"snapshot it describes {len(at_bytes)} at their current bytes ({absent} of the files "
            f"it lists are not in the snapshot), and "
            f"{len(ext_described)} of the {len(extended)} files TC12 extended. No TC12 loader "
            "reads it; it is listed under out_of_scope_snapshot_files and read only to describe "
            "it here."),
    }


# ported from scripts/tierc11_data.py:2075-2375 @ sha256 b2fe090f4a6cefe4 — CHANGED: TC11's schema key for key under the renames of L-D.11 (tc12_extension, tc12_rows_added, tc11_manifest_sha256, carried_from_tc11), a tc11_record block, the zero_volume_bars block, and the three-way venue agreement in `complete`
def build_manifest(pin: dict, pre: dict) -> dict:
    """TC11's STAGE_D_MANIFEST schema, at the TC12 pin, read-only: nothing is
    fetched and nothing in the snapshot is written (the derived lenses are
    re-derived IN MEMORY and must equal the files).  The renames are L-D.11's and no other;
    write_manifest adds the blocks that need the fee file (pins, fee_sources, tick_of_record,
    tiered_costs_haircut_twin)."""
    close_ms = int(pin["as_of_last_closed_4h_close_ms"])
    probe = load_probe()
    tc11, tc11_sha = _tc11_manifest()
    tc11_rows = {f["path"]: f for f in tc11["files"]}
    tc11_other = {o["path"]: o for o in tc11["out_of_scope_snapshot_files"]}
    attest = load_clone_attest()
    specs = load_contract_specs()
    status = {a["stem"]: a["status"] for a in specs["assets"]} if specs else {}
    assets = probe["classic5"] + probe["unseen12"]
    files, funding, admission, excluded, ext = [], {}, [], [], {}
    derived_ok = {}
    for a in assets:
        if not a.get("stem"):
            excluded.append({"asset": a["asset"], "reason": a["venue_reason"],
                             "closed_4h_bars": 0, "bars_1d": 0, "bars_1w": 0})
            continue
        stem = a["stem"]
        dv = derive_in_memory(stem, close_ms)
        n4 = dv["n4"]
        admitted = n4 >= ADMISSION_MIN_4H
        counts = {"asset": a["asset"], "stem": stem, "venue": a["venue"],
                  "closed_4h_bars": n4, "admission_min": ADMISSION_MIN_4H,
                  "margin": n4 - ADMISSION_MIN_4H,
                  "bars_1d": int(len(dv["1d"])), "bars_1w": int(len(dv["1w"])),
                  "admitted": bool(admitted)}
        admission.append(counts)
        if not admitted:
            excluded.append({"asset": a["asset"], "reason": f"{n4} closed 4h bars < {ADMISSION_MIN_4H}",
                             "closed_4h_bars": n4, "bars_1d": counts["bars_1d"],
                             "bars_1w": counts["bars_1w"]})
        for iv in lenses_of(stem):
            q = kline_path(stem, iv)
            rel = f"klines/{q.name}"
            derived = iv in DERIVED_IVS
            row = {"path": rel, "asset": a["asset"], "stem": stem,
                   "venue": a["venue"], "listing": a["listing"], "kind": "klines",
                   "as_of_lens": iv, "present": q.exists(), "native": not derived}
            was = pre["files"].get(rel)
            row["source"] = (
                "DERIVED from native 4h [TC10 LEAN L1], re-derived WHOLE at the TC12 pin" if derived else
                ("PRE-EXISTING in the TC11 snapshot (bytes == TC11's manifest, F-D-CLONE); old "
                 f"edge {iso(was['last_ms'])}; rows past it are TC12 REST"
                 + (" (15m: CLASSIC5 only; no TC12 stage reads it)" if iv == FIFTEEN else "")))
            if derived:
                row["publication_inherited_from"] = f"klines/{stem}_4h.parquet"
            if q.exists():
                df = pd.read_parquet(q)
                row.update(sha256=file_sha256(q), bytes=q.stat().st_size,
                           **scan_klines(df, iv, close_ms))
                row["content_sha"] = frame_sha(df.sort_values("open_time"), KLINE_COLS)
                tgt = target_last_open(iv, close_ms)
                row["complete_to_as_of"] = bool(row["as_of_last_closed_bar_open"] == iso(tgt))
                row["lens_last_closed_bar_at_pin"] = {"open": iso(tgt), "close": iso(tgt + STEP_MS[iv])}
                row["last_bar_close_equals_lens_last_closed_at_pin"] = bool(row["last_open_ms"] == tgt)
                row["tc11_manifest_sha256"] = (tc11_rows.get(rel, {}).get("sha256")
                                               or tc11_other.get(rel, {}).get("sha256"))
                row["pre_state"] = {"rows": was["rows"], "last_open": iso(was["last_ms"]),
                                    "file_sha256": was["file_sha256"],
                                    "content_sha": was["content_sha"]}
                row["tc12_rows_added"] = int(len(df) - was["rows"])
                ext.setdefault(iv, {})[stem] = {
                    "added": row["tc12_rows_added"],
                    "first_new_open": (iso(was["last_ms"] + STEP_MS[iv])
                                       if row["tc12_rows_added"] else None),
                    "last_open": row["last_open"]}
                if derived:
                    same = frame_sha(df, KLINE_COLS) == frame_sha(dv[iv], KLINE_COLS)
                    derived_ok[rel] = same
                    row["derived_file_equals_derivation"] = same
                    row["derivation_content_sha"] = frame_sha(dv[iv], KLINE_COLS)
                    row["derived_from"] = (
                        f"klines/{stem}_4h.parquet (native 4h, {dv['source_rows_as_of']} rows closed "
                        f"as-of) — " + ("1d = exactly six complete 4h bars of one UTC day"
                                        if iv == "1d" else
                                        "1w = seven complete derived days, MONDAY-anchored UTC")
                        + " [LEAN L1]; incomplete buckets dropped: "
                        + str(dv["dropped_incomplete_days"] if iv == "1d"
                              else dv["dropped_incomplete_weeks"]))
                else:
                    pub = dict(tc11_rows.get(rel, {}).get("publication") or {"carries": "UNAUDITED"})
                    pub["tc12_rows_past_tc11_edge"] = (
                        "REST — fetched by TC12 over the venue's REST API (Bybit v5 REST for MNT); "
                        "not archive-censused")
                    pub["carried_from"] = "TC11's manifest row (measured by TC10 where it says so)"
                    row["publication"] = pub
            files.append(row)
        q = funding_path(stem)
        rel = f"funding/{q.name}"
        row = {"path": rel, "asset": a["asset"], "stem": stem,
               "venue": a["venue"], "listing": a["listing"], "kind": "funding",
               "as_of_lens": "funding", "present": q.exists()}
        if q.exists():
            fdf = pd.read_parquet(q)
            fs = scan_funding(fdf, close_ms)
            funding[stem] = fs
            was = pre["files"][rel]
            row.update(sha256=file_sha256(q), bytes=q.stat().st_size, **fs)
            row["content_sha"] = frame_sha(fdf.sort_values("funding_time"), FUNDING_COLS)
            row["coverage"] = funding_coverage(stem, close_ms)
            row["tc11_manifest_sha256"] = tc11_rows.get(rel, {}).get("sha256")
            row["pre_state"] = {"rows": was["rows"], "last": iso(was["last_ms"]),
                                "file_sha256": was["file_sha256"], "content_sha": was["content_sha"]}
            row["tc12_rows_added"] = int(fs["rows"] - was["rows"])
            ext.setdefault("funding", {})[stem] = {"added": row["tc12_rows_added"],
                                                   "old_edge": iso(was["last_ms"]),
                                                   "last": fs["last"]}
        files.append(row)
    in_scope = {f["path"] for f in files}
    other = []
    for sub in ("klines", "funding"):
        for q in sorted((SNAPSHOT / sub).glob("*.parquet")):
            rel = f"{sub}/{q.name}"
            if rel not in in_scope:
                sha = file_sha256(q)
                ref = attest["files"].get(rel, {}).get("reference_sha256")
                other.append({"path": rel, "sha256": sha, "bytes": q.stat().st_size,
                              "tc11_manifest_sha256": ref, "unchanged_since_tc11": sha == ref})
    extended = sorted(f["path"] for f in files if f.get("tc12_rows_added"))
    root_disclosures = []
    for rel in tree_files(SNAPSHOT):
        if rel in in_scope or rel.startswith(("klines/", "funding/")):
            continue
        q = SNAPSHOT / rel
        sha = file_sha256(q)
        ref = attest["files"].get(rel, {}).get("reference_sha256")
        row = {"path": rel, "sha256": sha, "bytes": q.stat().st_size,
               "tc11_manifest_sha256": ref, "unchanged_since_tc11": sha == ref}
        if rel == "MANIFEST.json":
            row.update(cache_manifest_staleness(q, files, other, extended))
            root_disclosures.append(row["disclosure"])
        other.append(row)
    adm = [r for r in admission if r["admitted"]]
    prefixes = verify_prefixes(pre)
    lens_set = LENS_ORDER
    venue_faults = venue_agreement()
    man = {
        "tier": TIER, "stage": STAGE, "seed": SEED,
        "as_of_last_closed_4h": pin["as_of_last_closed_4h"],
        "as_of_last_closed_4h_open": pin["as_of_last_closed_4h_open"],
        "as_of_last_closed_4h_close_ms": close_ms,
        "as_of_last_closed_bar_per_lens": {
            iv: {"open": iso(target_last_open(iv, close_ms)),
                 "close": iso(target_last_open(iv, close_ms) + STEP_MS[iv])}
            for iv in lens_set},
        "warranty": WARRANTY,
        "snapshot_root": str(SNAPSHOT),
        # BY CONSTRUCTION (guard + _assert_bound), NOT MEASURED: its basis is filed beside it.
        "live_cache_touched": False,
        "live_cache_touched_basis": LIVE_CACHE_BASIS,
        "venues": [{**{k: a.get(k) for k in ("asset", "venue", "symbol", "stem", "status",
                                             "contract_type", "listing", "venue_reason")},
                    "status_at_tc12_capture": status.get(a.get("stem"))}
                   for a in assets],
        "venue_rejections": probe["rejections"],
        "panels": {"CLASSIC5": list(CLASSIC5),
                   "UNSEEN12_contract": [u[0] for u in UNSEEN12],
                   "UNSEEN_admitted_stems": [r["stem"] for r in adm if r["stem"] not in CLASSIC5],
                   "PANEL17_stems": [r["stem"] for r in adm],
                   "panel_size": len(adm)},
        "admission": {"rule": f">= TIDE_SLOW ({int(R2.TIDE_SLOW)}) + MEM_TTL_BARS "
                              f"({MEM_TTL_BARS}) = {ADMISSION_MIN_4H} closed 4h bars",
                      "rows": admission, "excluded": excluded},
        "gap_policy": "gaps are COUNTED and LISTED per file and NEVER filled; zero-volume "
                      "flat bars are the VENUE's outage placeholders — counted, attributed, kept",
        "derivation": "1d/1w derived from NATIVE 4h only [LEAN L1]; never fetched native, never "
                      "aggregated from 1h/5m (the venue's own intervals disagree on incident bars)",
        "files": files,
        "out_of_scope_snapshot_files": other,
        "prefix_attestation": {"law": pre["law"], "rows": prefixes,
                               "all_ok": all(r["ok"] for r in prefixes)},
        "mirror": MIRROR_SENTENCE,
        "leans": list(LEANS),
    }
    for k in CARRIED_KEYS:
        man[k] = tc11.get(k)
    man["carried_from_tc11"] = {
        "keys": list(CARRIED_KEYS),
        "manifest": T11_REL + "/data/STAGE_D_MANIFEST.json",
        "manifest_sha256": tc11_sha,
        "sha_chain": {"tc10_manifest_sha256": tc11["carried_from_tc10"]["manifest_sha256"],
                      "tc11_manifest_sha256": tc11_sha,
                      "law": "TC10 measured the three blocks on the TC10 snapshot; TC11 carried them "
                             "VERBATIM under TC10's manifest sha; TC12 carries TC11's copy VERBATIM "
                             "under TC11's manifest sha"},
        "why": "measured by TC10 on the TC10 snapshot, carried by TC11; the TC12 clone reproduces "
               "every byte of the TC11 snapshot (F-D-CLONE) and every row closing at or before TC11's "
               "pin is bit-identical after the fetch (F-D-PREFIX), so the measurement stands for the "
               "inherited rows; the rows TC12 added are REST and are not re-audited against the "
               "archive. Carried VERBATIM, not re-measured."}
    man["contract_premise_checks"] = premise_checks(probe)
    man["contract_multipliers"] = contract_multiplier_table()
    man["standing_disclosures"] = list(STANDING_DISCLOSURES) + root_disclosures
    man["content_sha_law"] = {
        "law": CONTENT_SHA_LAW,
        "files_with_content_sha": sum(1 for f in files if f.get("content_sha")),
        "derivations_with_content_sha": sum(1 for f in files if f.get("derivation_content_sha"))}
    man["operator_rulings_needed"] = list(OPERATOR_RULINGS)
    late = [{"path": f["path"], "rows_after_as_of": f["rows_after_as_of"]} for f in files
            if f["kind"] == "klines" and f.get("rows_after_as_of")]
    fstamp = [f for f in files if f["kind"] == "funding" and f["present"]]
    man["as_of_hazards"] = {
        "kline_files_holding_rows_after_as_of": late,
        "kline_law": "a TC12 file holding rows past the pin would be read past it by "
                     "tierc2_baseline.load_klines (whole file); load_asof / load_asof_at cut them",
        "funding_files_with_a_print_stamped_after_the_as_of_close": [
            f["path"] for f in fstamp if f["prints_stamped_after_as_of_close_within_jitter"]],
        "funding_law": "[LEAN D-g] a print belongs to the hour its stamp FLOORS to; load_funding_asof "
                       "returns funding_hour_ms and cuts on it; an interval-sum funding law must sum on "
                       "funding_hour_ms, never on the raw stamp",
        "funding_floor_hour_equals_nearest_hour_on_every_file": all(
            f["floor_hour_equals_nearest_hour"] for f in fstamp),
        "funding_ms_past_hour_max_over_panel": max(
            [f["ms_past_hour_max"] for f in fstamp], default=None)}
    seal_faults = verify_seal(OUT)
    sp = OUT / SEAL
    seal = json.loads(sp.read_text()) if sp.exists() else {}
    man["write_once"] = {
        "artifact": f"{DATA_REL}/{SEAL}" if seal else None,
        "sealed_sha256": {n: v["sha256"] for n, v in sorted(seal.get("files", {}).items())},
        "fetch_log_sealed_lines": seal.get("fetch_log", {}).get("sealed_lines"),
        "fetch_log_sha256_of_sealed_lines": seal.get("fetch_log", {}).get("sha256_of_sealed_lines"),
        "faults": seal_faults, "all_ok": not seal_faults,
        "disclosure": seal.get("disclosure", [])}
    # ── the extension and audit blocks ──
    man["tc12_extension"] = {
        "law": "every in-scope file extended from its PRE_STATE edge + one step to the last bar "
               "closing <= the pin (REST only, zero overlap); 1d/1w re-derived whole from the extended "
               "native 4h",
        "per_lens": {iv: {"files": len(ext[iv]),
                          "rows_added_total": int(sum(v["added"] for v in ext[iv].values())),
                          "rows_added_per_stem": {s: ext[iv][s] for s in ext[iv]}}
                     for iv in list(lens_set) + ["funding"] if iv in ext}}
    man["fifteen_minute_audit"] = fifteen_minute_audit(close_ms)
    ea_p = OUT / EDGE_AUDIT
    ea = json.loads(ea_p.read_text()) if ea_p.exists() else None
    man["inherited_edge_audit"] = (None if ea is None else {
        "artifact": f"{DATA_REL}/{EDGE_AUDIT}",
        "artifact_sha256": file_sha256(ea_p), "law": ea["law"],
        "files_audited": ea["files_audited"], "rows_audited": ea["rows_audited"],
        "all_equal": ea["all_equal"],
        "inherited_rows_past_tc11_as_of": ea["inherited_rows_past_tc11_as_of"],
        "funding_tapes_audited": ea["funding_tapes_audited"],
        "funding_all_equal": ea["funding_all_equal"],
        "funding_differing": sorted(k for k, v in ea["funding"].items() if not v["all_equal"]),
        "per_file": {k: {kk: v[kk] for kk in ("inherited_rows", "first_open", "last_open",
                                              "equal_rows", "differing", "missing_at_rest",
                                              "all_equal")}
                     for k, v in sorted(ea["rows"].items())}})
    man["clone_attestation"] = {
        "artifact": f"{DATA_REL}/{CLONE_ATTEST}",
        "artifact_sha256": file_sha256(OUT / CLONE_ATTEST),
        "source": attest["source"], "target": attest["target"], "method": attest["method"],
        "n_files": attest["n_files"], "n_pinned_by_tc11_manifest": attest["n_pinned_by_tc11_manifest"],
        "n_not_in_tc11_manifest": attest["n_not_in_tc11_manifest"],
        "all_equal": attest["all_equal"],
        "tc11_manifest_sha256_at_clone": attest["tc11_manifest"]["sha256"],
        "tc11_manifest_sha256_now": tc11_sha}
    tc10 = json.loads(TC10_MANIFEST.read_text(encoding="utf-8"))
    man["tc10_record"] = {
        "tc10_as_of_last_closed_4h": tc10["as_of_last_closed_4h"],
        "venue_probe": {"path": T10_REL + "/data/VENUE_PROBE.json",
                        "sha256": file_sha256(TC10_PROBE)},
        "stage_d_table": {"path": T10_REL + "/close/S3_STAGE_D.md",
                          "sha256": file_sha256(TC10_STAGE_D_TABLE)},
        "as_of_pin": {"path": T10_REL + "/data/AS_OF_PIN.json",
                      "sha256": file_sha256(TC10_PIN_FILE)},
        "manifest": {"path": T10_REL + "/data/STAGE_D_MANIFEST.json",
                     "sha256": file_sha256(TC10_MANIFEST),
                     "equals_the_sha_tc11_carried": file_sha256(TC10_MANIFEST)
                     == tc11["carried_from_tc10"]["manifest_sha256"]},
        "source_read_by_ast": {"path": D10_REL, "sha256": file_sha256(TC10_SRC)}}
    man["tc11_record"] = {
        "tc11_as_of_last_closed_4h": tc11["as_of_last_closed_4h"],
        "certified_by": T11_REL + "/PROGRESS.json (artifact_shas; its own sha from TC12's R0 census)",
        "manifest": {"path": T11_REL + "/data/STAGE_D_MANIFEST.json", "sha256": tc11_sha},
        "as_of_pin": {"path": T11_REL + "/data/AS_OF_PIN.json",
                      "sha256": tc11_certified(T11_REL + "/data/AS_OF_PIN.json")},
        "fee_schedule": {"path": T11_REL + "/data/fee_schedule.json",
                         "sha256": tc11_certified(T11_REL + "/data/fee_schedule.json")},
        "contract_specs": {"path": T11_REL + "/data/CONTRACT_SPECS.json",
                           "sha256": tc11_certified(T11_REL + "/data/CONTRACT_SPECS.json")},
        "ported_from": {"path": D11_REL, "sha256": D11_SHA256}}
    man["contract"] = {"path": CONTRACT_REL, "prefix_sha256": PIN_DERIVATION["contract_sha256"],
                       "prefix_bytes": PIN_DERIVATION["contract_prefix_bytes"],
                       "resume_paste": {"path": RESUME_PASTE_REL,
                                        "sha256": PG.certified(RESUME_PASTE_REL, ROOT)["sha256"]},
                       "leans": LEANS_DOC, "leans_sha256": PG.certified(LEANS_DOC, ROOT)["sha256"],
                       "rulings": RULINGS_REL}
    man["zero_volume_bars"] = zero_volume_block(close_ms)
    man["tc10_record"]["three_way_agreement"] = {
        "law": "TC10's Stage D table, TC10's VENUE_PROBE.json and TC11's manifest venues[] agree row "
               "for row on (asset, venue, symbol, stem) [L-D.10]",
        "faults": venue_faults, "all_agree": not venue_faults}
    kfiles = [f for f in files if f["kind"] == "klines"]
    man["complete"] = (all(f["present"] and (f["kind"] == "funding" or f["complete_to_as_of"])
                           for f in files)
                       and all(f["last_bar_close_equals_lens_last_closed_at_pin"]
                               and f["gap_count"] == 0 and f["duplicates"] == 0
                               and f["off_grid"] == 0 and f["backward"] == 0
                               and f["rows_after_as_of"] == 0 for f in kfiles)
                       and all(f["coverage"]["ok"] for f in files
                               if f["kind"] == "funding" and f["present"])
                       and all(derived_ok.values()) and len(derived_ok) == 2 * len(adm)
                       and man["prefix_attestation"]["all_ok"]
                       and man["write_once"]["all_ok"]
                       and man["clone_attestation"]["all_equal"]
                       and man["contract_multipliers"] is not None
                       and man["two_token_trap"]["all_hard_floored"]
                       and not man["two_token_trap"]["discontinuous_floor_seams"]
                       and not man["two_token_trap"]["intended_asset_unconfirmed"]
                       and not venue_faults)
    return man


# ported from scripts/tierc11_data.py:2378-2430 @ sha256 b2fe090f4a6cefe4 — CHANGED: TC12's document — the pin lines, the fee sources, the tick of record with the on-grid shares and the monthly granularity, the zero-volume bars; the TC11 sections under their renamed keys
def manifest_md(man: dict, fees: dict, audit: dict) -> str:
    """A compact reading of the manifest (deterministic; the JSON is the record)."""
    L = [f"# {TIER} · STAGE {STAGE} — THE SUBSTRATE TOP-UP (STAGE_D_MANIFEST)", "",
         f"- **AS_OF** {man['as_of_last_closed_4h']} (close ms {man['as_of_last_closed_4h_close_ms']}) "
         f"· seed {man['seed']} · snapshot `{man['snapshot_root']}` · complete **{man['complete']}**",
         f"- Clone: {man['clone_attestation']['n_files']} files, all equal to TC11's record: "
         f"{man['clone_attestation']['all_equal']} · prefix attestation all_ok "
         f"{man['prefix_attestation']['all_ok']} ({len(man['prefix_attestation']['rows'])} files) · "
         f"seal all_ok {man['write_once']['all_ok']} · venue table / probe / TC11 manifest agree: "
         f"{man['tc10_record']['three_way_agreement']['all_agree']}",
         f"- Panel: {man['panels']['panel_size']} admitted — {' '.join(man['panels']['PANEL17_stems'])}",
         f"- Mirror: {man['mirror']}",
         "", "## The \"maker-bps\" pin", ""]
    L += [f"- `{x}`" for x in man["pins"]["maker-bps"]["lines"]]
    L += ["", "| venue | status | url | retrieval attempted | retrieved | body sha256 |", "|---|---|---|---|---|---|"]
    for v in sorted(man["fee_sources"]):
        s = man["fee_sources"][v]
        L.append(f"| {v} | {s['status']} | {s['maker_source_url']} | {s['retrieval_attempted_utc_date']} | "
                 f"{s['retrieved_utc_date'] or '—'} | {s['body_sha256'] or '—'} |")
    L += ["", "## Last closed bar per lens at the pin", "", "| lens | open | close |", "|---|---|---|"]
    for iv in LENS_ORDER:
        b = man["as_of_last_closed_bar_per_lens"][iv]
        L.append(f"| {iv} | {b['open']} | {b['close']} |")
    L += ["", "## Rows added by TC12 per lens (every file whole)", "",
          "| lens | files | rows added | per stem |", "|---|---|---|---|"]
    for iv in list(LENS_ORDER) + ["funding"]:
        b = man["tc12_extension"]["per_lens"].get(iv)
        if b is None:
            continue
        per = " ".join(f"{s}:{b['rows_added_per_stem'][s]['added']}" for s in PANEL17 if s in b["rows_added_per_stem"])
        L.append(f"| {iv} | {b['files']} | {b['rows_added_total']} | {per} |")
    L += ["", "## Files", "",
          "| path | rows | first open | last open | gaps | complete | sha256 |",
          "|---|---|---|---|---|---|---|"]
    for f in man["files"]:
        if f["kind"] == "klines":
            L.append(f"| {f['path']} | {f['rows']} | {f['first_open']} | {f['last_open']} | "
                     f"{f['gap_count']} | {f['complete_to_as_of']} | `{f['sha256'][:16]}…` |")
        else:
            L.append(f"| {f['path']} | {f['rows']} | {f['first']} | {f['last']} | — | "
                     f"{f['coverage']['ok']} | `{f['sha256'][:16]}…` |")
    fa = man["fifteen_minute_audit"]
    L += ["", "## 15m vs three 5m bars — a DISCLOSURE, not a failure", "",
          "| stem | compared | price mismatch | volume-only | no 5m triple | of which TC12-new bars |",
          "|---|---|---|---|---|---|"]
    for s in CLASSIC5:
        v = fa["per_asset"][s]
        L.append(f"| {s} | {v['compared']} | {v['price_mismatch']} | {v['volume_only_mismatch']} | "
                 f"{len(v['no_complete_5m_triple'])} | {v['price_mismatch_tc12_new_bars']} price, "
                 f"{v['volume_only_mismatch_tc12_new_bars']} volume |")
    ea = man["inherited_edge_audit"]
    if ea:
        L += ["", f"## The seam bar vs REST — {ea['rows_audited']} bars in {ea['files_audited']} native "
                  f"files, all equal: {ea['all_equal']} · the last inherited funding print of "
                  f"{ea['funding_tapes_audited']} tapes, all equal: {ea['funding_all_equal']} · inherited "
                  f"rows past TC11's as-of: {ea['inherited_rows_past_tc11_as_of']['rows']}", ""]
        for k in sorted(ea["per_file"]):
            v = ea["per_file"][k]
            if not v["all_equal"]:
                L.append(f"- {k}: {len(v['differing'])} differ, {len(v['missing_at_rest'])} missing")
        L += [f"- {k}: the venue's print of the hour differs from the tape" for k in ea["funding_differing"]]
    L += ["", "## Fees", "", "| stem | venue | taker bps/side | round trip | maker bps/side | maker kind | slippage tier |",
          "|---|---|---|---|---|---|---|"]
    for a in fees["assets"]:
        L.append(f"| {a['stem']} | {a['venue']} | {a['taker_bps_side_used']} | {a['round_trip_bps_used']} | "
                 f"{a['maker_bps_side']} | {a['maker_kind']} | {a['charter_slippage_tier']} "
                 f"{a['charter_slippage_bps_per_side']} |")
    tk = man["tick_of_record"]
    L += ["", "## The tick of record (TC12's capture) beside TC11's", "",
          "| stem | price_tick (TC12) | price_tick (TC11) | equal as Decimal | qty_step | min notional | status |",
          "|---|---|---|---|---|---|---|"]
    for s in PANEL17:
        r = tk["per_stem"][s]
        L.append(f"| {s} | {r['tc12']['price_tick']} | {r['tc11']['price_tick']} | {r['equal_as_decimal']} | "
                 f"{r['tc12']['qty_step']} | {r['tc12']['min_notional_usdt']} | {r['tc12']['status']} |")
    L += ["", f"Ticks moved vs TC11's capture: {tk['ticks_moved_vs_tc11'] or 'none'}.",
          "", "## On-grid shares of the tape on the recorded tick (exact; n_on_grid/n per price field)", "",
          "| stem | lens | segment | open | high | low | close | last off-grid open (any field) |",
          "|---|---|---|---|---|---|---|---|"]
    for stem in PANEL17:
        for iv in audit["lenses"]:
            for seg in SEGMENTS:
                c = [audit["cells"][f"{stem}|{iv}|{seg}|{f}"] for f in audit["fields"]]
                last = max([x["last_off_grid_open"] for x in c if x["last_off_grid_open"]], default="—")
                L.append(f"| {stem} | {iv} | {seg} | " + " | ".join(x["share"] for x in c) + f" | {last} |")
    L += ["", f"## Observed granularity per calendar month (5m) — {audit['months_measured']} stem-months; "
              f"coarser than the recorded tick: {audit['n_coarser_months']}", "",
          f"- {audit['never_looser']}"]
    if audit["coarser_months"]:
        L += ["", "| stem | month | observed granularity | recorded tick |", "|---|---|---|---|"]
        L += [f"| {c['stem']} | {c['month']} | {c['observed_granularity']} | {c['recorded_tick']} |"
              for c in audit["coarser_months"]]
    zv = man["zero_volume_bars"]
    L += ["", "## Zero-volume flat bars per native file, by segment (kept, counted, never filled)", "",
          "| stem \\| lens | " + " | ".join(zv["segments"]) + " | total | zero-volume bars (total) |",
          "|---|" + "---|" * len(zv["segments"]) + "---|---|"]
    for k in (f"{stem}|{iv}" for stem in PANEL17 for iv in lenses_of(stem) if iv not in DERIVED_IVS):
        r = zv["per_file"][k]
        L.append(f"| {k} | " + " | ".join(str(r["zero_volume_flat_bars"][s]) for s in zv["segments"])
                 + f" | {r['zero_volume_flat_bars_total']} | {r['zero_volume_bars_total']} |")
    L += ["", "## Leans", ""] + [f"- {x}" for x in man["leans"]]
    L += ["", "## Standing disclosures", ""] + [f"- {x}" for x in man["standing_disclosures"]]
    L += ["", "## Operator rulings needed", ""] + [f"- {x}" for x in man["operator_rulings_needed"]]
    return "\n".join(L) + "\n"


# ported from scripts/tierc11_data.py:2433-2447 @ sha256 b2fe090f4a6cefe4 — VERBATIM
def _out_guard(dst: Path) -> Path:
    """--out must be the stage directory, a directory under it, or a system
    temp directory OUTSIDE the repo trees (a tree checked out under a temp
    directory — a review copy — is still the repo: its research_outputs/tierc10
    and the stage dir's parent stay refused).  HALTS IF it is anywhere else
    (the TC10 tree above all)."""
    r = dst.expanduser().resolve()
    tmps = {Path(tempfile.gettempdir()).resolve(), Path("/private/tmp").resolve()}
    trees = {ROOT.resolve(), MAIN_TREE.resolve()}
    in_tree = any(r == t or t in r.parents for t in trees)
    if r == OUT.resolve() or OUT.resolve() in r.parents or (
            not in_tree and any(t in r.parents for t in tmps)):
        return r
    raise SystemExit(f"HALT: --out {r} is not {OUT}, under it, or under a temp directory outside "
                     f"the repo tree")


# ported from scripts/tierc11_data.py:2450-2466 @ sha256 b2fe090f4a6cefe4 — CHANGED: also files TICK_GRID_AUDIT.json; the fee extraction runs here; the pins, fee_sources and tick_of_record blocks are added
def write_manifest(dst: Path) -> dict:
    """THE DETERMINISM SET — STAGE_D_MANIFEST.json + .md, fee_schedule.json and
    TICK_GRID_AUDIT.json into `dst` — no network, no snapshot write, no clock call.  F-D-DET runs
    exactly this twice.  HALTs (in fee_pins) while a venue captured with HTTP 200 has no grammar
    of record."""
    dst = _out_guard(dst)
    pin = load_pin(OUT)
    pre = json.loads((OUT / "PRE_STATE.json").read_text())
    pins = fee_pins(OUT)
    man = build_manifest(pin, pre)
    assets = [a for a in load_probe()["classic5"] + load_probe()["unseen12"] if a.get("stem")]
    fees = fee_schedule(assets, {f["stem"]: f for f in man["files"]
                                 if f["kind"] == "funding" and f["present"]}, pin, pins, OUT)
    audit = tick_grid_audit(pin, OUT)
    man["tiered_costs_haircut_twin"] = haircut_twin_table(
        [a for a in assets if a["asset"] in {r["asset"] for r in man["admission"]["rows"]
                                             if r["admitted"]}], fees)
    man["pins"] = {"maker-bps": {
        "lines": pin_lines(fees),
        "source": {"path": DATA_REL + "/fee_schedule.json", "key": "venues[<VENUE>].maker_bps_side"},
        "register_rows": [f"fee.maker_bps_side.{v}" for v in fees["venues"]],
        "veto": "maker-bps",
        "values": fees["maker_pin"]["values"], "kinds": fees["maker_pin"]["kinds"],
        "x_assumed_bps_side": fees["maker_pin"]["x_assumed_bps_side"],
        "differs_from_x_assumption": fees["maker_pin"]["differs_from_x_assumption"]}}
    man["fee_sources"] = {
        v: {"maker_source_url": b["maker_source_url"],
            "retrieved_utc_date": b["maker_retrieved_utc_date"],
            "retrieval_attempted_utc_date": b["maker_retrieval_attempted_utc_date"],
            "record": b["maker_source_record"], "body_sha256": b["maker_source_body_sha256"],
            "status": (MAKER_PUBLISHED if b["maker_kind"] == MAKER_PUBLISHED
                       else f"UNRETRIEVABLE ({b['maker_unretrievable_reason']})"),
            "http_status": b["maker_retrieval_http_status"], "grammar": b["maker_grammar"]}
        for v, b in fees["venues"].items()}
    man["tick_of_record"] = {**tick_of_record_block(audit["ticks"], OUT),
                             "months_measured": audit["months_measured"],
                             "n_coarser_months": audit["n_coarser_months"],
                             "coarser_months": audit["coarser_months"],
                             "never_looser": audit["never_looser"]}
    _dump(man, dst / "STAGE_D_MANIFEST.json")
    _dump(fees, dst / "fee_schedule.json")
    _dump(audit, dst / TICK_AUDIT)
    (dst / "STAGE_D_MANIFEST.md").write_text(manifest_md(man, fees, audit), encoding="utf-8")
    return man


# ═══════════════════════════════════════════════ downstream API (no network)
# ported from scripts/tierc11_data.py:2471-2475 @ sha256 b2fe090f4a6cefe4 — VERBATIM
def load_manifest(out: Path | None = None) -> dict:
    p = (out or OUT) / "STAGE_D_MANIFEST.json"
    if not p.exists():
        raise SystemExit(f"HALT: no Stage D manifest at {p}")
    return json.loads(p.read_text())


# ported from scripts/tierc11_data.py:2479-2483 @ sha256 b2fe090f4a6cefe4 — VERBATIM
def panel(out: Path | None = None) -> dict:
    """{'CLASSIC5': [...], 'UNSEEN': [...admitted stems...], 'PANEL17': [...]}"""
    m = load_manifest(out)["panels"]
    return {"CLASSIC5": m["CLASSIC5"], "UNSEEN": m["UNSEEN_admitted_stems"],
            "PANEL17": m["PANEL17_stems"]}


# ported from scripts/tierc11_data.py:2487-2495 @ sha256 b2fe090f4a6cefe4 — VERBATIM
def load_asof(stem: str, iv: str, out: Path | None = None) -> pd.DataFrame:
    """The ONLY as-of-safe kline read for TC10: bars of lens `iv` CLOSED at the
    pinned AS_OF, ascending.  HALTs on a missing file (never an empty frame)."""
    close_ms = load_pin(out)["as_of_last_closed_4h_close_ms"]
    p = kline_path(stem, iv)
    if not p.exists():
        raise SystemExit(f"HALT: missing {p}")
    d = pd.read_parquet(p).sort_values("open_time")
    return d[d["open_time"] + STEP_MS[iv] <= close_ms].reset_index(drop=True)


# ported from scripts/tierc11_data.py:2499-2509 @ sha256 b2fe090f4a6cefe4 — VERBATIM
def with_funding_hour(d: pd.DataFrame, what: str = "funding") -> pd.DataFrame:
    """Adds funding_hour_ms [LEAN D-g]: the hour a print's stamp FLOORS to.
    HALTS IF a stamp sits more than FUNDING_JITTER_MS past its hour — such a
    print belongs to no hour and an interval-sum law could not place it."""
    t = d["funding_time"].to_numpy(np.int64)
    hour = t // MS_1H * MS_1H
    if len(t) and int((t - hour).max()) > FUNDING_JITTER_MS:
        k = int(np.argmax(t - hour))
        raise SystemExit(f"HALT: {what}: print stamped {iso(t[k])} sits {int(t[k] - hour[k])} ms "
                         f"past its hour (> {FUNDING_JITTER_MS}) — not attributable to an hour")
    return d.assign(funding_hour_ms=hour)


# ported from scripts/tierc11_data.py:2513-2528 @ sha256 b2fe090f4a6cefe4 — VERBATIM
def load_funding_asof(stem: str, out: Path | None = None) -> pd.DataFrame:
    """Funding prints known at the AS_OF, with funding_hour_ms [LEAN D-g] —
    the column an interval-sum law (entry_ms < t <= exit_ms) must sum on; the
    raw stamp jitters a few ms PAST every bar close.  HALTs on a missing or
    empty file — the silent `{}` of tierc2_baseline.load_funding must be
    unreachable."""
    close_ms = load_pin(out)["as_of_last_closed_4h_close_ms"]
    p = funding_path(stem)
    if not p.exists():
        raise SystemExit(f"HALT: missing {p} — a panel asset without funding is a HALT, not zero cost")
    d = pd.read_parquet(p).sort_values("funding_time").reset_index(drop=True)
    d = with_funding_hour(d, p.name)
    d = d[d["funding_hour_ms"] <= close_ms].reset_index(drop=True)
    if not len(d):
        raise SystemExit(f"HALT: {p} holds no funding print at or before AS_OF")
    return d


def load_asof_at(stem: str, iv: str, cut_ms: int) -> pd.DataFrame:
    """THE CUT LAW [L-D.28], for the Stage D fixtures (which cannot import the shim): the rows of
    the bound file with open_time + STEP_MS[iv] <= cut_ms, ascending, read through pandas on a
    path string into FRESH arrays.  ANY instant is admitted (no 4h-modulus clause).
    HALTS unless cut_ms is an int <= the pin, and on a missing file."""
    if type(cut_ms) is not int or cut_ms > PIN_CLOSE_MS:
        halt(f"load_asof_at: cut {cut_ms!r} is not an int at or before the pin {PIN_CLOSE_MS}")
    p = kline_path(stem, iv)
    if not p.exists():
        halt(f"missing {p}")
    d = pd.read_parquet(str(p)).sort_values("open_time")
    return d[d["open_time"] + STEP_MS[iv] <= cut_ms].reset_index(drop=True)


def load_funding_asof_at(stem: str, cut_ms: int) -> pd.DataFrame:
    """The funding twin of the cut law: the prints whose FLOOR HOUR is <= cut_ms, with
    funding_hour_ms — never a cut on the raw stamp [L-D.9].  HALTS unless cut_ms is an int <= the
    pin, on a missing file, and on a stamp more than FUNDING_JITTER_MS past its hour."""
    if type(cut_ms) is not int or cut_ms > PIN_CLOSE_MS:
        halt(f"load_funding_asof_at: cut {cut_ms!r} is not an int at or before the pin {PIN_CLOSE_MS}")
    p = funding_path(stem)
    if not p.exists():
        halt(f"missing {p} — a panel asset without funding is a HALT, not zero cost")
    d = pd.read_parquet(str(p)).sort_values("funding_time").reset_index(drop=True)
    d = with_funding_hour(d, p.name)
    return d[d["funding_hour_ms"] <= cut_ms].reset_index(drop=True)


# ═══════════════════════════════════════════════ 11 · THE LaCie MIRROR [L-D.24; the paste's "mirror"]
MIRROR_ATTEST = "MIRROR_ATTEST.json"
WAKE_LOG_NAME = "DRIVE_WAKE_LOG_TC12.md"
LACIE_MOUNT = Path("/Volumes/LaCie")           # the MOUNT POINT handed to drive_wait, never a path inside it
MIRROR_SNAPSHOT = LACIE_MOUNT / "Naiad" / "snapshots" / SNAPSHOT_NAME
MIRROR_PROVENANCE = LACIE_MOUNT / "Naiad" / "provenance" / SNAPSHOT_NAME
MIRROR_SELF = ("STAGE_D_MANIFEST.json", "SHA256SUMS")      # placed in the destination so it describes itself
MIRROR_RECORD = "TC12-D.mirror"


def mirror_plan(out: Path | None = None) -> dict:
    """What a mirror holds [L-D.24]: every file of the TC12 snapshot (the manifest's in-scope and
    out-of-scope paths, each with the sha the manifest files for it) and the fee-source bodies
    (FEE_SOURCE.json's shas).  {key: {"src", "dst_root", "rel", "sha256"}}, key = <root>/<rel>."""
    out = out or OUT
    man = load_manifest(out)
    plan = {}
    for f in man["files"] + man["out_of_scope_snapshot_files"]:
        plan["snapshots/" + f["path"]] = {"src": SNAPSHOT / f["path"], "root": "snapshots",
                                          "rel": f["path"], "sha256": f["sha256"]}
    src = json.loads((out / FEE_SOURCE).read_text(encoding="utf-8"))
    for venue, s in sorted(src["venues"].items()):
        if s.get("body_sha256"):
            q = Path(s["body_path"])
            rel = q.relative_to(PROVENANCE).as_posix()
            plan["provenance/" + rel] = {"src": q, "root": "provenance", "rel": rel,
                                         "sha256": s["body_sha256"]}
    return plan


def mirror_findings(plan: dict, snap_dst: Path, prov_dst: Path) -> list[str]:
    """VERIFY BY RE-READING FROM THE DESTINATION: the sha256 of every destination file equals the
    manifest's sha for it (the bodies against FEE_SOURCE.json), and the destination's file set
    equals the plan's (plus the two self-describing files).  A listing is not a verification."""
    bad = []
    roots = {"snapshots": snap_dst, "provenance": prov_dst}
    for key in sorted(plan):
        e = plan[key]
        q = roots[e["root"]] / e["rel"]
        if not q.is_file():
            bad.append(f"MIRROR-FILE-SET {key}: absent from the mirror")
        elif file_sha256(q) != e["sha256"]:
            bad.append(f"MIRROR-SHA {key}: sha != manifest ({file_sha256(q)[:12]} != {e['sha256'][:12]})")
    for root, d in roots.items():
        want = {e["rel"] for e in plan.values() if e["root"] == root}
        if root == "snapshots":
            want |= set(MIRROR_SELF)
        have = set(tree_files(d)) if d.is_dir() else set()
        if have != want:
            bad.append(f"MIRROR-FILE-SET {root}: only in the mirror {sorted(have - want)[:5]}, only in the "
                       f"manifest {sorted(want - have)[:5]}")
    return bad


def _mirror_copy(src: Path, dst: Path) -> None:
    """One file: <dst>.part, fsync, os.replace (exFAT has no clonefile)."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    part = dst.with_name(dst.name + ".part")
    with open(src, "rb") as fi, open(part, "wb") as fo:
        shutil.copyfileobj(fi, fo)
        fo.flush()
        os.fsync(fo.fileno())
    os.replace(part, dst)


def mirror_snapshot(out: Path) -> int:
    """--mirror [L-D.24]: a plain directory mirror — a sha-verified byte copy of every file of the
    sealed TC12 snapshot plus the fee-source bodies — to the LaCie when the drive is reachable.
    Nothing else on the drive is touched; nothing is deleted or overwritten outside the two
    destination directories.  Returns 0 (mirrored and verified) or 2 ("MIRROR NOT RUN": the drive
    was unreachable after drive_wait's full budget — nothing written to the drive, nothing waits).

    HALTS IF: TC12-D is not COMPLETE-VERIFIED; a destination exists that no filed MIRROR_ATTEST.json
    names; two relative paths collide under casefold; or the re-read verification fails."""
    import drive_wait                           # stdlib only; its WAKE_LOG default lies under exchange/
    row = [r for r in PG.ledger(ROOT) if r["record"] == STAGE]
    if not row or row[0]["status"] != PG.COMPLETE:
        halt(f"--mirror requires {STAGE} COMPLETE-VERIFIED; the record ledger says "
             f"{row[0]['status'] if row else 'ABSENT'} {row[0]['why'] if row else ''}")
    drive_wait.WAKE_LOG = out / WAKE_LOG_NAME   # rebound BEFORE the call: nothing is written under exchange/
    r = drive_wait.wait_for_drive(str(LACIE_MOUNT))
    if not r.ok:
        log(f"MIRROR NOT RUN — {LACIE_MOUNT} UNREACHABLE after {r.elapsed:.1f} s "
            f"({r.attempts} attempts; budget {r.budget:.1f} s); nothing was written to the drive")
        return 2
    plan = mirror_plan(out)
    folded = {}
    for key in sorted(plan):
        if folded.setdefault(key.casefold(), key) != key:
            halt(f"mirror: {key} and {folded[key.casefold()]} collide under casefold (exFAT is case-insensitive)")
    p = out / MIRROR_ATTEST
    earlier = json.loads(p.read_text(encoding="utf-8")) if p.exists() else None
    for d in (MIRROR_SNAPSHOT, MIRROR_PROVENANCE):
        named = earlier is not None and str(d) in (earlier["destination"]["snapshot"],
                                                   earlier["destination"]["provenance"])
        if d.exists() and not named:
            halt(f"mirror: {d} exists and no filed {MIRROR_ATTEST} names it — refusing to adopt, delete or "
                 "overwrite anything on the drive")
    roots = {"snapshots": MIRROR_SNAPSHOT, "provenance": MIRROR_PROVENANCE}
    copied, kept, n_bytes = [], [], 0
    for key in sorted(plan):
        e = plan[key]
        dst = roots[e["root"]] / e["rel"]
        if dst.is_file() and file_sha256(dst) == e["sha256"]:
            kept.append(key)
        else:
            _mirror_copy(e["src"], dst)
            copied.append(key)
        n_bytes += dst.stat().st_size
    man_bytes = (out / "STAGE_D_MANIFEST.json").read_bytes()
    sums = "".join(f"{plan[k]['sha256']}  {plan[k]['rel']}\n" for k in sorted(plan) if plan[k]["root"] == "snapshots")
    MIRROR_SNAPSHOT.mkdir(parents=True, exist_ok=True)
    (MIRROR_SNAPSHOT / MIRROR_SELF[0]).write_bytes(man_bytes)
    (MIRROR_SNAPSHOT / MIRROR_SELF[1]).write_text(sums, encoding="utf-8")
    bad = mirror_findings(plan, MIRROR_SNAPSHOT, MIRROR_PROVENANCE)
    if bad:
        halt(f"the mirror does not verify on re-read from the destination: {bad[:5]}")
    vfs = os.statvfs(str(LACIE_MOUNT))
    doc = {
        "tier": TIER, "stage": MIRROR_RECORD, "seed": SEED,
        "law": "a sha-verified plain copy: every destination file was RE-READ from the destination and "
               "its sha256 equals STAGE_D_MANIFEST.json's (the bodies: FEE_SOURCE.json's); the "
               "destination's file set equals the manifest's. Stated limit: a read served from the OS "
               "cache cannot be told from a read off the platter; F-MIRROR re-hashes again on any "
               "later run [L-D.24]",
        "destination": {"snapshot": str(MIRROR_SNAPSHOT), "provenance": str(MIRROR_PROVENANCE),
                        "mount_point": str(LACIE_MOUNT)},
        "volume_observed": {"statvfs": {k: getattr(vfs, k) for k in ("f_bsize", "f_frsize", "f_blocks",
                                                                     "f_bavail", "f_namemax")},
                            "case_insensitive": (MIRROR_SNAPSHOT / MIRROR_SELF[1].lower()).exists(),
                            "filesystem_name": "not read by this process — it makes no out-of-process "
                                               "call here (L-D.11: one site, the clone)"},
        "drive_wait": {"state": r.state, "attempts": r.attempts, "elapsed_s": round(r.elapsed, 2),
                       "budget_s": r.budget, "wake_logged": r.logged,
                       "wake_log": DATA_REL + "/" + WAKE_LOG_NAME if r.logged else None},
        "manifest": {"path": DATA_REL + "/STAGE_D_MANIFEST.json", "sha256": sha_bytes(man_bytes)},
        "fee_source": {"path": DATA_REL + "/" + FEE_SOURCE, "sha256": file_sha256(out / FEE_SOURCE)},
        "self_describing_files": list(MIRROR_SELF),
        "n_files": len(plan), "bytes": n_bytes,
        "n_snapshot_files": sum(1 for e in plan.values() if e["root"] == "snapshots"),
        "n_provenance_files": sum(1 for e in plan.values() if e["root"] == "provenance"),
        "provenance_note": "the provenance destination holds the fee-source bodies FEE_SOURCE.json records; "
                           "where it records none (no page was retrieved) nothing is written there",
        "n_copied_this_run": len(copied), "n_already_equal": len(kept),
        "all_equal": True, "faults": [],
        "mirrored_wall_clock_utc": now_iso(),
        "files": {k: {"sha256": plan[k]["sha256"], "equal": True} for k in sorted(plan)},
        "unmirrored_for_athena": [str(TC10_SNAPSHOT), str(TC11_SNAPSHOT)],
    }
    _dump(doc, p)
    log(f"MIRROR VERIFIED: {len(plan)} files, {n_bytes} bytes ({len(copied)} copied, {len(kept)} already "
        f"equal) re-read from {MIRROR_SNAPSHOT} and {MIRROR_PROVENANCE}; drive {r.state} -> {p}")
    return 0


# The ported objects and their provenance, for F-D-PORT: name -> (label, the name in
# scripts/tierc11_data.py, the reason; "" for a VERBATIM port).  A def unless noted.
PORTS = {
    'guard_substrate': ('CHANGED', 'guard_substrate', "refuses the TC11 snapshot too; the one substrate it admits is TC12's"),
    "_main_tree": ("VERBATIM", "_main_tree", ""),
    "pin_literal": ("VERBATIM", "pin_literal", ""),
    "source_literal": ("VERBATIM", "source_literal", ""),
    "STEP_MS": ("CHANGED", "STEP_MS", "the 15m step is read from engine.cells.INTERVAL_MS, not typed"),
    "parse_slippage_clause": ("VERBATIM", "parse_slippage_clause", ""),
    "read_maker_bps_side": ("VERBATIM", "read_maker_bps_side", ""),
    "log": ("VERBATIM", "log", ""),
    "iso": ("VERBATIM", "iso", ""),
    "file_sha256": ("VERBATIM", "file_sha256", ""),
    "frame_sha": ("VERBATIM", "frame_sha", ""),
    "_dump": ("VERBATIM", "_dump", ""),
    "_dump_once": ("VERBATIM", "_dump_once", ""),
    "kline_path": ("VERBATIM", "kline_path", ""),
    "funding_path": ("VERBATIM", "funding_path", ""),
    "target_last_open": ("VERBATIM", "target_last_open", ""),
    "lenses_of": ("VERBATIM", "lenses_of", ""),
    "scope_paths": ("VERBATIM", "scope_paths", ""),
    "split_rel": ("VERBATIM", "split_rel", ""),
    "_assert_bound": ("TEXT-ONLY", "_assert_bound", "the HALT names the TC12 snapshot"),
    'tc11_expected_shas': ('CHANGED', 'tc10_expected_shas', "the reference is TC11's manifest, its own sha held to TC11's PROGRESS"),
    "tree_files": ("VERBATIM", "tree_files", ""),
    'clone_findings': ('TEXT-ONLY', 'clone_findings', "the filed reference strings name TC11's manifest and snapshot"),
    'clone_snapshot': ('CHANGED', 'clone_snapshot', "the source is the TC11 snapshot and the reference TC11's manifest (its sha held to TC11's PROGRESS)"),
    "load_clone_attest": ("VERBATIM", "load_clone_attest", ""),
    "CallLog": ("VERBATIM", "CallLog", ""),
    "_venue_4h_row": ("CHANGED", "_venue_4h_row", "the witness symbol is CLASSIC5[0], read from tierc2_rules.UNIVERSE"),
    'pin_findings': ('CHANGED', 'pin_findings', "the pin is the DERIVATION (by object); the Bybit proof is checked; the key set is TC11's"),
    'tc11_pin_keys': ('CHANGED', 'tc10_pin_keys', "the key set carried is TC11's pin record's"),
    'pin_as_of': ('CHANGED', 'pin_as_of', "the pin by object (derived from STEP Q, never typed); proven on BOTH venue clocks; TC11's keys carried"),
    "venue_latest_closed": ("VERBATIM", "venue_latest_closed", ""),
    "record_fetch_clock": ("CHANGED", "record_fetch_clock", "a Bybit clock row is filed too, and a venue clock at or before the pin HALTs (G3)"),
    "load_pin": ("TEXT-ONLY", "load_pin", "the HALT names tierc12_data"),
    "load_probe": ("CHANGED", "load_probe", "the three-way agreement of L-D.10 is required before the probe is used"),
    "panel_assets": ("VERBATIM", "panel_assets", ""),
    "_bybit_get": ("VERBATIM", "_bybit_get", ""),
    "_retry": ("VERBATIM", "_retry", ""),
    "binance_brake": ("VERBATIM", "binance_brake", ""),
    "_fetch_log": ("VERBATIM", "_fetch_log", ""),
    "_edge": ("VERBATIM", "_edge", ""),
    "_assert_grid": ("VERBATIM", "_assert_grid", ""),
    "bybit_klines": ("VERBATIM", "bybit_klines", ""),
    "bybit_funding": ("VERBATIM", "bybit_funding", ""),
    "base_multiplier": ("VERBATIM", "base_multiplier", ""),
    "normalize_price": ("VERBATIM", "normalize_price", ""),
    "normalize_qty": ("VERBATIM", "normalize_qty", ""),
    'capture_contract_specs': ('TEXT-ONLY', 'capture_contract_specs', "the not-TRADING HALT and the log lines name the TC12 capture (the filed `doc` statement is the referee's, unchanged)"),
    "load_contract_specs": ("VERBATIM", "load_contract_specs", ""),
    'contract_multiplier_table': ('TEXT-ONLY', 'contract_multiplier_table', "the artifact path is tierc12's"),
    'write_pre_state': ('TEXT-ONLY', 'write_pre_state', "each row's keys and the filed sentences name the TC11 manifest sha it must equal (the clone's reference)"),
    'inherited_rows': ('CHANGED', 'inherited_rows', "the cut is TC11's as-of (the pin of the snapshot this clone inherits)"),
    'audit_inherited_rows': ('CHANGED', 'audit_inherited_rows', "the population past TC11's as-of is empty and recorded so; THE SEAM BAR of each native file and the last inherited funding print of each tape are compared with the venue"),
    "verify_prefixes": ("VERBATIM", "verify_prefixes", ""),
    "extend_klines": ("TEXT-ONLY", "extend_klines", "the HALTs name TC12"),
    "extend_funding": ("TEXT-ONLY", "extend_funding", "the HALT names TC12"),
    "run_fetch": ("CHANGED", "run_fetch", "+ the fee-source capture (3d), the no-404 assertion, and the flat-bar attestation capture (3f) once the extension is complete"),
    'SEALED_FILES': ('CHANGED', 'SEALED_FILES', "TC11's five plus the fee-source capture and the flat-bar attestation capture (seven) [L-D.11]"),
    "_lines_sha": ("VERBATIM", "_lines_sha", ""),
    "seal_provenance": ("VERBATIM", "seal_provenance", ""),
    "verify_seal": ("VERBATIM", "verify_seal", ""),
    "derive_1d": ("VERBATIM", "derive_1d", ""),
    "derive_1w": ("VERBATIM", "derive_1w", ""),
    "_write_if_changed": ("VERBATIM", "_write_if_changed", ""),
    "derive_lenses": ("VERBATIM", "derive_lenses", ""),
    "run_derive": ("VERBATIM", "run_derive", ""),
    "derive_in_memory": ("VERBATIM", "derive_in_memory", ""),
    "scan_klines": ("VERBATIM", "scan_klines", ""),
    "scan_funding": ("VERBATIM", "scan_funding", ""),
    "funding_coverage": ("VERBATIM", "funding_coverage", ""),
    'fifteen_minute_audit': ('CHANGED', 'fifteen_minute_audit', "the era boundary is TC11's pin (bars closing after it are TC12's new rows); the keys say tc12_new"),
    "_source_line": ("VERBATIM", "_source_line", ""),
    "tier_of": ("VERBATIM", "tier_of", ""),
    "slippage_bps_side": ("VERBATIM", "slippage_bps_side", ""),
    "charter_bps_side": ("VERBATIM", "charter_bps_side", ""),
    "charter_round_trip_bps": ("VERBATIM", "charter_round_trip_bps", ""),
    "assert_tiers_cover": ("VERBATIM", "assert_tiers_cover", ""),
    "haircut_twin_net_r": ("VERBATIM", "haircut_twin_net_r", ""),
    "haircut_twin_for_stem": ("VERBATIM", "haircut_twin_for_stem", ""),
    "haircut_twin_table": ("VERBATIM", "haircut_twin_table", ""),
    'fee_schedule': ('CHANGED', 'fee_schedule', "maker_bps_side per VENUE from the venue block (published, or on file and flagged); TC11's row keys kept and held equal; no top-level maker scalar [L-D.19]"),
    "premise_checks": ("VERBATIM", "premise_checks", ""),
    '_tc11_manifest': ('CHANGED', '_tc10_manifest', "TC11's manifest (its sha held to TC11's PROGRESS) is the previous record"),
    "cache_manifest_staleness": ("TEXT-ONLY", "cache_manifest_staleness", "the keys and the disclosure sentence name the TC11 -> TC12 inheritance"),
    'build_manifest': ('CHANGED', 'build_manifest', "TC11's schema key for key under the renames of L-D.11 (tc12_extension, tc12_rows_added, tc11_manifest_sha256, carried_from_tc11), a tc11_record block, the zero_volume_bars block, and the three-way venue agreement in `complete`"),
    'manifest_md': ('CHANGED', 'manifest_md', "TC12's document — the pin lines, the fee sources, the tick of record with the on-grid shares and the monthly granularity, the zero-volume bars; the TC11 sections under their renamed keys"),
    "_out_guard": ("VERBATIM", "_out_guard", ""),
    "write_manifest": ("CHANGED", "write_manifest", "also files TICK_GRID_AUDIT.json; the fee extraction runs here; the pins, fee_sources and tick_of_record blocks are added"),
    "load_manifest": ("VERBATIM", "load_manifest", ""),
    "panel": ("VERBATIM", "panel", ""),
    "load_asof": ("VERBATIM", "load_asof", ""),
    "with_funding_hour": ("VERBATIM", "with_funding_hour", ""),
    "load_funding_asof": ("VERBATIM", "load_funding_asof", ""),
    "summarize": ("TEXT-ONLY", "summarize", "the lines name TC12 and read the renamed key tc12_extension"),
    'run_all': ('CHANGED', 'run_all', "the no-404 assertion before the derivation; the pin lines printed; TC12's names"),
    "main": ("CHANGED", "main", "+ --mirror; the no-404 assertion before --derive; the pin lines after --manifest"),
}


# ═══════════════════════════════════════════════ run
# ported from scripts/tierc11_data.py:2559-2581 @ sha256 b2fe090f4a6cefe4 — TEXT-ONLY: the lines name TC12 and read the renamed key tc12_extension
def summarize(pin: dict, man: dict) -> None:
    log(f"\nAS_OF {pin['as_of_last_closed_4h']} (open {pin['as_of_last_closed_4h_open']}); venue "
        f"closeTime {pin['venue_close_time_of_pinned_bar_ms']} < venue clock "
        f"{pin['venue_server_time_ms']} ({pin['venue_server_time']})")
    log("NEW BARS PER LENS (rows added by TC12, per stem):")
    for iv, b in man["tc12_extension"]["per_lens"].items():
        vals = sorted({v["added"] for v in b["rows_added_per_stem"].values()})
        log(f"  {iv:8s} files {b['files']:2d}  total +{b['rows_added_total']:6d}  per-file {vals}")
    kf = [f for f in man["files"] if f["kind"] == "klines"]
    log(f"EDGES: {sum(f['last_bar_close_equals_lens_last_closed_at_pin'] for f in kf)}/{len(kf)} kline "
        f"files end at their lens's last bar closing <= the pin; gaps "
        f"{sum(f['gap_count'] for f in kf)}; rows after as-of {sum(f['rows_after_as_of'] for f in kf)}")
    log(f"PREFIX attestation all_ok {man['prefix_attestation']['all_ok']} "
        f"({len(man['prefix_attestation']['rows'])} files)")
    fa = man["fifteen_minute_audit"]
    log("15m vs 5m triples (DISCLOSURE): " + " · ".join(
        f"{s} price {v['price_mismatch']} vol {v['volume_only_mismatch']} "
        f"notriple {len(v['no_complete_5m_triple'])}" for s, v in fa["per_asset"].items()))
    ea = man["inherited_edge_audit"]
    if ea:
        log(f"THE SEAM BAR vs REST: {ea['rows_audited']} rows / {ea['files_audited']} files, "
            f"all equal {ea['all_equal']}")
    log(f"SEAL faults: {man['write_once']['faults'] or 'none'} · complete={man['complete']}")


def print_pins(man: dict) -> None:
    """THE PIN LINE, in the Stage D log [L-D.21] — read from the manifest just built."""
    for line in man["pins"]["maker-bps"]["lines"]:
        log(line)
    tk = man["tick_of_record"]
    log(f"TICK OF RECORD: {len(tk['per_stem'])} stems from {tk['tc12_capture']['path']}; moved vs TC11: "
        f"{tk['ticks_moved_vs_tc11'] or 'none'}; months coarser than the recorded tick: {tk['n_coarser_months']}")


# ported from scripts/tierc11_data.py:2584-2608 @ sha256 b2fe090f4a6cefe4 — CHANGED: the no-404 assertion before the derivation; the pin lines printed; TC12's names
def run_all() -> int:
    t0 = time.time()
    OUT.mkdir(parents=True, exist_ok=True)
    log(f"{TIER} · STAGE {STAGE} · seed {SEED} · snapshot {SNAPSHOT}")
    for x in LEANS:
        log(x)
    pin = pin_as_of(OUT)
    srv, latest = record_fetch_clock(OUT, pin)          # filed BEFORE the fetch and the seal
    incomplete, stats = run_fetch(pin, OUT)
    log(f"FETCH wall {stats['t1'] - stats['t0']:.1f}s; HTTP calls this process {CallLog.counts}")
    if incomplete:
        log("INCOMPLETE (nothing is derived, sealed or described; a re-run resumes from each edge):")
        for x in sorted(set(incomplete)):
            log(f"  - {x}")
        return 2
    log("\nDERIVE 1d/1w from native 4h")
    assert_no_404(OUT)
    run_derive(pin)
    seal_provenance(OUT)
    man = write_manifest(OUT)
    summarize(pin, man)
    print_pins(man)
    log(f"elapsed {time.time() - t0:.0f}s")
    if not man["prefix_attestation"]["all_ok"]:
        log("*** HALT: an old prefix moved. ***")
        return 1
    if not man["complete"]:
        log("INCOMPLETE: the manifest's `complete` is False")
        return 2
    return 0


# ported from scripts/tierc11_data.py:2611-2647 @ sha256 b2fe090f4a6cefe4 — CHANGED: + --mirror; the no-404 assertion before --derive; the pin lines after --manifest
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    flags = ("clone", "pin", "fetch", "derive", "seal", "manifest", "mirror", "all")
    for flag in flags:
        ap.add_argument(f"--{flag}", action="store_true")
    ap.add_argument("--out", default=str(OUT), help="--manifest only: the directory to file into")
    a = ap.parse_args()
    picked = [f for f in flags if getattr(a, f)]
    if len(picked) != 1:
        raise SystemExit(f"HALT: name exactly one subcommand (got {picked or 'none'})")
    cmd = picked[0]
    if cmd == "clone":
        if not _CLONE_ONLY:
            raise SystemExit("HALT: --clone runs alone")
        clone_snapshot(OUT)
        return 0
    if cmd == "pin":
        pin = pin_as_of(OUT)
        record_fetch_clock(OUT, pin)
        return 0
    if cmd == "fetch":
        pin = load_pin(OUT)
        record_fetch_clock(OUT, pin)                    # the latest close AT FETCH TIME; G3
        incomplete, stats = run_fetch(pin, OUT)
        log(f"FETCH wall {stats['t1'] - stats['t0']:.1f}s; HTTP calls {CallLog.counts}")
        for x in sorted(set(incomplete)):
            log(f"  - INCOMPLETE {x}")
        return 2 if incomplete else 0
    if cmd == "derive":
        assert_no_404(OUT)
        run_derive(load_pin(OUT))
        return 0
    if cmd == "seal":
        seal_provenance(OUT)
        bad = verify_seal(OUT)
        log(f"seal faults: {bad or 'none'}")
        return 1 if bad else 0
    if cmd == "manifest":
        man = write_manifest(Path(a.out))
        print_pins(man)
        return 0 if man["complete"] else 2
    if cmd == "mirror":
        return mirror_snapshot(OUT)
    return run_all()


if __name__ == "__main__":
    sys.exit(main())
