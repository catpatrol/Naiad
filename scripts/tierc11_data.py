#!/usr/bin/env python
"""TIER-C11 · STAGE TC11-D — THE CORRIDOR.  One as-of pin, one frozen snapshot.

Contract of record: exchange/queue/2026-09-24_TC11_APOLLO.md (sha256 bb38e016…,
STEP Q b9ed953).  Executor HEPHAESTUS; seed 20260924.  Executor readings:
research_outputs/tierc11/LEANS.md §0 (L-0.1 CORRIDOR, L-0.2 SNAPSHOT, L-0.3 CODE
REUSE, L-0.4 NAMES) and §1 (L-1.1 taker toll of record, L-1.2 maker twin).  The
plan of record is research_outputs/tierc11/scout/C_data_corridor.md §7.

This module FETCHES and DESCRIBES.  It scores nothing and runs no card.

WHY A NEW MODULE.  scripts/tierc10_data.py HALTs at import on every substrate
but tc10_20260921 (assert_substrate, :94-117), and the TC10 snapshot must never
move.  The functions this stage needs are therefore PORTED here.  Each carries
the comment 'ported from scripts/tierc10_data.py:<lines> @ sha256
2cbf9bb6bcfea3ec'.  A port marked VERBATIM is AST-identical to its source
(F-D11-PORT proves it); a port marked CHANGED names its change.  The TC10
constants that are data (UNSEEN12, the slippage clause) are READ out of that
source by AST, never retyped.  engine.data (ED) is reused for Binance REST
exactly as TC10 used it.

WHAT IT DOES, IN ORDER
  --clone     APFS-clones (cp -cpR) ~/.cache/naiad/snapshots/tc10_20260921 to
              ~/.cache/naiad/snapshots/tc11_20260925 when the target does not
              exist, then re-hashes EVERY cloned file against TC10's
              STAGE_D_MANIFEST.json (read-only) and HALTs on any mismatch ->
              CLONE_ATTEST.json (write-once).  The ONLY subcommand that runs
              without the substrate guard (its target does not exist yet).
  --pin       AS_OF = 2026-09-25T00:00:00Z (close ms 1790294400000) [L-0.1],
              pinned BY VALUE and proven closed by the venue (Binance
              /fapi/v1/time + the BTCUSDT 4h closeTime).  The latest closed 4h at
              run time is printed and filed beside it -> AS_OF_PIN.json
              (write-once; TC10's keys, plus extra keys).  --pin, --fetch and
              --all also file the venue clock and the latest closed 4h at that
              moment as a kind='clock' row of FETCH_LOG.jsonl
              (record_fetch_clock; --all files it before the fetch and seal).
  --fetch     CONTRACT_SPECS.json (write-once; proves every symbol still
              TRADING), PRE_STATE.json (write-once; every in-scope file's edge,
              rows and shas before the first fetch), EDGE_AUDIT.json (write-once;
              the inherited rows past TC10's as-of vs REST, read-only), then REST
              from each file's edge + one step to the last bar closing <= the
              pin: 17 x {5m, 1h, 4h, 12h}, CLASSIC5 x 15m, and 17 funding tapes.
              Every HTTP request is a row of FETCH_LOG.jsonl.
  --derive    1d / 1w from native 4h [TC10 LEAN L1], exactly as tierc10_data.
  --seal      WRITE_ONCE_SEAL.json: the provenance records' shas + the fetch-log
              head (its line prefix).
  --manifest  [--out DIR]  No network and no snapshot write.  Files
              STAGE_D_MANIFEST.json/.md and fee_schedule.json in TC10's schema
              (+ the maker twin, + the charter slippage tier, + 15m, + the TC11
              extension and audit blocks).  F-DET runs this twice.
  --all       pin, fetch, derive, seal, manifest.

WHAT WOULD MAKE THIS WRONG: reading or writing the live cache; writing the TC10
snapshot or anything under research_outputs/tierc10/; starting a fetch at or
before a file's pre-state edge (engine.data._save_cache keeps the NEW row at an
identical open_time, so an early start would overwrite an inherited bar);
calling a derived day "native"; letting a wall clock into the manifest.

Run:  export NAIAD_CACHE_DIR=$HOME/.cache/naiad/snapshots/tc11_20260925 PYTHONDONTWRITEBYTECODE=1
      ~/venvs/naiad/bin/python scripts/tierc11_data.py --all
      (--clone alone needs no NAIAD_CACHE_DIR)
Exit: 0 complete · 2 fetch incomplete (a re-run resumes from each edge) · 1 HALT.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = Path.home() / ".cache" / "naiad" / "snapshots" / "tc11_20260925"
TC10_SNAPSHOT = Path.home() / ".cache" / "naiad" / "snapshots" / "tc10_20260921"
LIVE_CACHE = Path.home() / ".cache" / "naiad" / "data_cache"


def guard_substrate(env: str | None) -> Path:
    """THE FROZEN-SUBSTRATE GUARD [L-0.2].  Runs at import, BEFORE engine.data
    or any tier module can bind a cache path (every subcommand but --clone).

    HALTS IF: NAIAD_CACHE_DIR is unset; is not an absolute path AS GIVEN (a
    '~' or a relative value: engine.data binds Path(env) with no expansion,
    relative to the working directory, so the guard and the engine would name
    different directories — TC11-D verification round 2, defect 4); names the
    live cache (tested on the path STRING first, then resolved); names the TC10
    snapshot; is anything but the TC11 snapshot; or the TC11 snapshot has no
    klines/ directory.
    """
    if not env:
        raise SystemExit(f"HALT: NAIAD_CACHE_DIR is unset — TC11 reads and writes ONLY "
                         f"the snapshot {SNAPSHOT}")
    if os.path.expanduser(env) != env or not os.path.isabs(env):
        raise SystemExit(f"HALT: NAIAD_CACHE_DIR={env!r} is not an absolute path as given — "
                         "engine.data binds Path(env) with no '~' expansion, relative to the "
                         "working directory, so it would name another directory than this guard")
    norm = Path(os.path.normpath(env))
    for bad, why in ((LIVE_CACHE, "the LIVE cache — READ-NEVER, WRITE-NEVER"),
                     (TC10_SNAPSHOT, "the TC10 snapshot — frozen, WRITE-NEVER for TC11")):
        if (norm == bad or bad in norm.parents or norm.resolve() == bad.resolve()
                or bad.resolve() in norm.resolve().parents):
            raise SystemExit(f"HALT: NAIAD_CACHE_DIR={norm} names {why}")
    got = norm.resolve()
    if got != SNAPSHOT.resolve():
        raise SystemExit(f"HALT: NAIAD_CACHE_DIR={got} is not the TC11 snapshot {SNAPSHOT}")
    if not (got / "klines").is_dir():
        raise SystemExit(f"HALT: the TC11 snapshot has no klines/ directory: {got}")
    return got


# --clone (alone) is the one entry point that must run before its target
# exists; everything else — including every importer of this module — is
# guarded before the first engine import.
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

SEED = 20260924
TIER, STAGE = "TIER-C11", "TC11-D"
OUT = ROOT / "research_outputs" / "tierc11" / "data"
RANGE_PINS_SOURCE = ROOT / "engine" / "rangefinder.py"

TC10_SRC = ROOT / "scripts" / "tierc10_data.py"
TC10_SRC_SHA256 = "2cbf9bb6bcfea3ec6184d5502ba5c530f5c0089d95288ab848a745ad5b3015fc"
TC10_DATA = ROOT / "research_outputs" / "tierc10" / "data"            # READ-ONLY
TC10_MANIFEST = TC10_DATA / "STAGE_D_MANIFEST.json"
TC10_PROBE = TC10_DATA / "VENUE_PROBE.json"
TC10_PIN_FILE = TC10_DATA / "AS_OF_PIN.json"
CONTRACT = ROOT / "exchange" / "queue" / "2026-09-24_TC11_APOLLO.md"
CONTRACT_SHA256 = "bb38e016a8f3e55ca3bcc09fec53ba6b8dc40accb60d054f8163d033a898f835"
LEANS_DOC = "research_outputs/tierc11/LEANS.md"
C_MAP_DOC = "research_outputs/tierc11/scout/C_data_corridor.md"

PIN_CLOSE_MS = 1_790_294_400_000          # 2026-09-25T00:00:00Z [L-0.1]
TC10_PIN_CLOSE_MS = 1_790_006_400_000     # 2026-09-21T16:00:00Z (TC10's AS_OF_PIN)


def _port_tag(fn: str) -> str:
    return f"scripts/tierc10_data.py:{fn} @ sha256 {TC10_SRC_SHA256[:16]}"


# ported from scripts/tierc10_data.py:135-152 @ sha256 2cbf9bb6bcfea3ec — VERBATIM
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


MS_1H = 3_600_000
MS_4H = 4 * MS_1H
DAY_MS = 86_400_000
WEEK_MS = 7 * DAY_MS
MONDAY_EPOCH_OFFSET_MS = 4 * DAY_MS          # 1970-01-05 was a Monday

KLINE_COLS = list(ED.KLINE_COLS)
FUNDING_COLS = list(ED.FUNDING_COLS)
NATIVE_IVS = ("5m", "1h", "4h", "12h")       # fetched, venue-native, all 17
FIFTEEN = "15m"                              # fetched, venue-native, CLASSIC5 only [L-0.2]
DERIVED_IVS = ("1d", "1w")                   # derived from native 4h [TC10 LEAN L1]
LENS_ORDER = ("5m", "15m", "1h", "4h", "12h", "1d", "1w")
# ported from scripts/tierc10_data.py:204-205 @ sha256 2cbf9bb6bcfea3ec — CHANGED: gains "15m": 900_000
STEP_MS = {**{iv: INTERVAL_MS[iv] for iv in NATIVE_IVS}, "15m": 900_000,
           "1d": DAY_MS, "1w": WEEK_MS}
if STEP_MS["15m"] != INTERVAL_MS["15m"]:
    raise SystemExit(f"HALT: engine.cells INTERVAL_MS['15m']={INTERVAL_MS['15m']} != 900000")
GRID_ANCHOR_MS = {"1w": MONDAY_EPOCH_OFFSET_MS}     # every other lens: 0

FUNDING_JITTER_MS = 60_000                   # study/census.py FUNDING_JITTER_MAX_MS [TC10 D-b]
MEM_TTL_BARS = int(pin_literal(RANGE_PINS_SOURCE, "PINS_V2", "MEM_TTL_BARS"))
ADMISSION_MIN_4H = int(R2.TIDE_SLOW) + MEM_TTL_BARS                       # 316 + 400

# ── the charter's tiered slippage, READ out of TC10's clause [tierc10_data.py:217-220]
CONTRACT_SLIPPAGE_CLAUSE, _CLAUSE_L1, _CLAUSE_L2 = source_literal(TC10_SRC, "CONTRACT_SLIPPAGE_CLAUSE")
CHARTER_SOURCE = ROOT / "Naiad_Phase0_Charter.md"
CHARTER_SLIPPAGE_NEEDLE = "**Slippage** per side"
_TIER_RX = re.compile(r"tier ([A-Z]) \{([^}]*)\} (\d+)")


# ported from scripts/tierc10_data.py:226-240 @ sha256 2cbf9bb6bcfea3ec — VERBATIM
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

# ── the MAKER TWIN [L-1.2]: READ out of the README sentence, never typed ────
MAKER_SOURCE = ROOT / "README.md"
_MAKER_RX = re.compile(r"maker is (\d+(?:\.\d+)?)%")
MAKER_PRECEDENT = ROOT / "scripts" / "v3_recompute.py"
MAKER_PRECEDENT_NEEDLE = "maker entries 2 bps/side"


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
if CLASSIC5 != ("BTCUSDT", "ETHUSDT", "SOLUSDT", "NEARUSDT", "ZECUSDT"):
    raise SystemExit(f"HALT: tierc2_rules UNIVERSE moved: {CLASSIC5}")
UNSEEN12, _U12_L1, _U12_L2 = source_literal(TC10_SRC, "UNSEEN12")
# The commission's seventeen stems, in the order the orchestrator named them.
# Resolved against TC10's venue of record (VENUE_PROBE.json); a mismatch HALTs.
PANEL17 = CLASSIC5 + ("ENAUSDT", "PUMPUSDT", "HYPEUSDT", "MNTUSDT_BYBIT", "SUIUSDT",
                      "LTCUSDT", "XMRUSDT", "BNBUSDT", "UNIUSDT", "1000PEPEUSDT",
                      "DOGEUSDT", "1000BONKUSDT")
ALT_VENUE_ASSETS = ("MNT",)
BYBIT_STEM_SUFFIX = "_BYBIT"

BYBIT_BASE = "https://api.bybit.com"
BYBIT_IV = {"5m": "5", "1h": "60", "4h": "240", "12h": "720"}      # no 15m [TC10 :274]
BYBIT_PAGE = 1000
BYBIT_FUNDING_PAGE = 200

CHUNK_BARS = 15_000                          # 10 REST pages per save (resumable)
WEIGHT_SOFT_CAP = 1200                       # of Binance's 2400 / minute
RETRIES = 6

LIVE_CACHE_BASIS = (
    "by construction (guard + _assert_bound), NOT MEASURED: guard_substrate HALTs at import unless "
    "NAIAD_CACHE_DIR is the TC11 snapshot (F-D11-GUARD) and _assert_bound HALTs before every "
    "snapshot write unless engine.data.cache_dir() still resolves to it (F-D11-BOUND); "
    "live_cache_touched keeps the bool of TC10's schema")
CONTENT_SHA_LAW = (
    "content_sha = frame_sha of the file's rows sorted by their stamp (kline: open_time + OHLCV; "
    "funding: funding_time + funding_rate) — the raw little-endian column bytes, independent of "
    "the parquet writer; derivation_content_sha = frame_sha of the in-memory 1d/1w re-derivation. "
    "F-DET compares every one across the two hash-seed builds [L-F.1]")

WARRANTY = ("these files are described AS OF the pinned last closed 4h bar named "
            "here and of no other; bars stamped after it are counted, never read "
            "[TC6V-a, carried by TIER-C11]")

LEANS = (
    f"[LEAN-HEPHAESTUS] L-0.1 ({LEANS_DOC}) CORRIDOR: AS_OF = 2026-09-25T00:00:00Z (close ms "
    f"{PIN_CLOSE_MS}), the latest 4h bar closed when STEP Q was filed (2026-09-25T00:09:43Z); "
    "pinned BY VALUE, proven closed by the venue's own closeTime < the venue clock, write-once; "
    "every stage reads it, and the latest close at FETCH time is printed beside it "
    "(record_fetch_clock also files it as a kind='clock' row of FETCH_LOG.jsonl; the 2026-09-25 "
    "run printed it only, and FETCH_CLOCK_NOTE.json records it from the sealed log). The latest "
    "close at PIN time is filed in AS_OF_PIN.json besides.",
    f"[LEAN-HEPHAESTUS] L-0.2 ({LEANS_DOC}) SNAPSHOT: tc11_20260925 is an APFS clone (cp -cpR) of "
    "tc10_20260921; every cloned file is re-hashed against TC10's STAGE_D_MANIFEST before the "
    "first write (CLONE_ATTEST.json); it is extended over REST only. The live cache is never "
    "read or written and the TC10 snapshot is never written.",
    "[LEAN-HEPHAESTUS] TC10 L1 CARRIED: 1d = exactly six complete native-4h bars per UTC day; "
    "1w = seven complete derived days, MONDAY-anchored UTC, complete weeks only; the source is "
    "native 4h, never 1h/5m aggregates.",
    "[LEAN-HEPHAESTUS] TC10 D-b CARRIED: funding is kept through AS_OF close + 60 s.",
    "[LEAN-HEPHAESTUS] TC10 D-c CARRIED: MNT's whole tape (klines and funding) is Bybit v5 "
    "linear, stem MNTUSDT_BYBIT, never spliced. Bybit serves no 15m in BYBIT_IV and R1 needs no "
    "15m for the twelve, so MNT has none.",
    "[LEAN-HEPHAESTUS] TC10 D-d CARRIED: PUMPFUN = PUMPUSDT (baseAsset PUMP); PUMPBTCUSDT is a "
    "different asset.",
    "[LEAN-HEPHAESTUS] TC10 D-g CARRIED: a funding print belongs to the hour its stamp FLOORS to.",
    "[LEAN-HEPHAESTUS] D11-a PRE_STATE SCOPE: 124 files = 17 x {5m,1h,4h,12h,1d,1w} + CLASSIC5 x "
    "15m + 17 funding tapes (the C map's §7 step 4). It is a SUPERSET of the brief's native + "
    "15m + funding list: the derived lenses are included so the no-rewrite proof covers them.",
    "[LEAN-HEPHAESTUS] D11-b NEVER EARLIER: every fetch starts at the file's PRE_STATE edge + "
    "one step (engine.data._save_cache keeps the NEW row at an identical open_time, so an "
    "earlier start would let REST overwrite an inherited bar). The rows TC10's as-of excluded "
    "but TC11's includes (5m 16:00-16:25Z for 14 stems, 15m 16:00/16:15Z for CLASSIC5) are "
    "INHERITED from the TC10 snapshot and never refetched into a file; EDGE_AUDIT.json compares "
    "them with REST read-only and the manifest prints the result.",
    "[LEAN-HEPHAESTUS] D11-c VENUE OF RECORD: TC10's VENUE_PROBE.json (read-only, pinned by sha) "
    "— the venue of a tape is decided once. TC11 re-captures CONTRACT_SPECS.json in TC10's "
    "schema only to prove every symbol is still TRADING at the pin (and to give the re-rooted "
    "modules a TC11 file of that name).",
    "[LEAN-HEPHAESTUS] D11-d CARRIED BLOCKS: two_token_trap, data_spend and "
    "venue_publications_disagree are TC10's (measured on the TC10 snapshot, whose every byte "
    "the TC11 clone reproduces — F-D11-CLONE). They are carried VERBATIM with the TC10 "
    "manifest's sha, not re-measured; carried_from_tc10 says so.",
    "[LEAN-HEPHAESTUS] D11-e 15m: CLASSIC5 only [L-0.2], audited against the three 5m bars it "
    "spans; a mismatch is a DISCLOSURE, never a failure (the venue's intervals disagree on "
    "incident bars; TC10's derivation law never aggregates across native intervals).",
    "[LEAN-HEPHAESTUS] D11-f complete_to_as_of is STRICT on every lens. TC10 let a derived lens "
    "pass by construction (`or iv in DERIVED_IVS`); here 1d and 1w must also end at their own "
    "last bar closing <= the pin.",
    "[LEAN-HEPHAESTUS] D11-g ORDER: --all seals BEFORE it describes, so the manifest's "
    "write_once block verifies the filed seal (TC10 re-described after --seal for the same "
    "reason). The seal covers AS_OF_PIN, CLONE_ATTEST, CONTRACT_SPECS, EDGE_AUDIT, PRE_STATE "
    "and the fetch-log head — a superset of the brief's three.",
    f"[LEAN-HEPHAESTUS] L-1.1 ({LEANS_DOC}) TOLL OF RECORD: taker {float(R2.FEE_BPS_SIDE)} bps/side, "
    f"{float(R2.FEE_BPS_ROUND_TRIP)} round trip (tierc2_rules); the charter slippage tier "
    "(A 2 / B 5 / C 10 bps/side) is a haircut TWIN beside it, never in its place.",
    f"[LEAN-HEPHAESTUS] L-1.2 ({LEANS_DOC}) MAKER TWIN: {MAKER_BPS_SIDE} bps/side (README.md:"
    f"{MAKER_SOURCE_LINE} 'maker is 0.02%'; precedent scripts/v3_recompute.py R10), an "
    "ASSUMPTION, MNT included (Bybit's maker rate is not in the repo); maker legs (entry and "
    f"target only) carry zero slippage; stop and invalidation legs stay taker "
    f"({float(R2.FEE_BPS_SIDE)} bps/side, the toll of record's rate — the charter slippage "
    "belongs to the haircut twin only [L-1.1]).",
)

LOG_LINES: list[str] = []


# ported from scripts/tierc10_data.py:408-410 @ sha256 2cbf9bb6bcfea3ec — VERBATIM
def log(msg: str = "") -> None:
    print(msg, flush=True)
    LOG_LINES.append(msg)


# ported from scripts/tierc10_data.py:413-417 @ sha256 2cbf9bb6bcfea3ec — VERBATIM
def iso(ms: int | float | None) -> str | None:
    if ms is None:
        return None
    return (datetime.fromtimestamp(int(ms) / 1000, tz=timezone.utc)
            .strftime("%Y-%m-%dT%H:%M:%SZ"))


# ported from scripts/tierc10_data.py:420-425 @ sha256 2cbf9bb6bcfea3ec — VERBATIM
def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# ported from scripts/tierc10_data.py:428-437 @ sha256 2cbf9bb6bcfea3ec — VERBATIM
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


# ported from scripts/tierc10_data.py:440-445 @ sha256 2cbf9bb6bcfea3ec — VERBATIM
def _dump(obj, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(obj, indent=2, sort_keys=True, default=str) + "\n",
                   encoding="utf-8")
    os.replace(tmp, path)


# ported from scripts/tierc10_data.py:448-454 @ sha256 2cbf9bb6bcfea3ec — VERBATIM
def _dump_once(obj, path: Path) -> None:
    """WRITE-ONCE, in code: a provenance record that exists is never written
    again.  HALTS IF the file is already there."""
    if path.exists():
        raise SystemExit(f"HALT: {path.name} is WRITE-ONCE and already exists — "
                         f"refusing to overwrite {path}")
    _dump(obj, path)


# ported from scripts/tierc10_data.py:457-458 @ sha256 2cbf9bb6bcfea3ec — VERBATIM (SNAPSHOT is TC11's)
def kline_path(stem: str, iv: str, root: Path | None = None) -> Path:
    return (root or SNAPSHOT) / "klines" / f"{stem}_{iv}.parquet"


# ported from scripts/tierc10_data.py:461-462 @ sha256 2cbf9bb6bcfea3ec — VERBATIM (SNAPSHOT is TC11's)
def funding_path(stem: str, root: Path | None = None) -> Path:
    return (root or SNAPSHOT) / "funding" / f"{stem}.parquet"


# ported from scripts/tierc10_data.py:465-468 @ sha256 2cbf9bb6bcfea3ec — VERBATIM
def target_last_open(iv: str, as_of_close_ms: int) -> int:
    """Open of the last bar of lens `iv` that is CLOSED at the AS_OF close."""
    step, anchor = STEP_MS[iv], GRID_ANCHOR_MS.get(iv, 0)
    return ((as_of_close_ms - step - anchor) // step) * step + anchor


def lenses_of(stem: str) -> tuple[str, ...]:
    """The in-scope lenses of one stem: native 5m/1h/4h/12h + derived 1d/1w for
    all 17; 15m for CLASSIC5 only [L-0.2]."""
    return tuple(iv for iv in LENS_ORDER
                 if iv in NATIVE_IVS or iv in DERIVED_IVS or (iv == FIFTEEN and stem in CLASSIC5))


def scope_paths() -> list[str]:
    """Every in-scope snapshot file, panel order then lens order (124)."""
    rels = []
    for stem in PANEL17:
        rels += [f"klines/{stem}_{iv}.parquet" for iv in lenses_of(stem)]
        rels.append(f"funding/{stem}.parquet")
    return rels


def split_rel(rel: str) -> tuple[str, str]:
    """'klines/MNTUSDT_BYBIT_5m.parquet' -> ('MNTUSDT_BYBIT', '5m')."""
    stem, _, iv = rel[len("klines/"):-len(".parquet")].rpartition("_")
    return stem, iv


def _assert_bound() -> None:
    """Belt and braces before every snapshot write: engine.data's cache_dir()
    (read on every call) must still resolve to the TC11 snapshot.
    HALTS IF it does not."""
    got = Path(ED.cache_dir()).resolve()
    if got != SNAPSHOT.resolve():
        raise SystemExit(f"HALT: engine.data.cache_dir() = {got} — not the TC11 snapshot")


# ═══════════════════════════════════════════════ 0 · THE CLONE [L-0.2]
CLONE_ATTEST = "CLONE_ATTEST.json"


def tc10_expected_shas() -> dict[str, str]:
    """rel path -> sha256, for every file TC10's STAGE_D_MANIFEST.json pins
    (files[] that are present + out_of_scope_snapshot_files[]).  Read-only."""
    man = json.loads(TC10_MANIFEST.read_text(encoding="utf-8"))
    exp = {f["path"]: f["sha256"] for f in man["files"] if f.get("present") and f.get("sha256")}
    for o in man["out_of_scope_snapshot_files"]:
        exp[o["path"]] = o["sha256"]
    return exp


def tree_files(root: Path) -> list[str]:
    """Every regular file under root (hidden ones included), sorted rel paths."""
    out = []
    for d, _, names in os.walk(root):
        for n in names:
            q = Path(d) / n
            if q.is_file():
                out.append(q.relative_to(root).as_posix())
    return sorted(out)


def clone_findings(root: Path, exp: dict[str, str], ref_root: Path) -> tuple[list[str], dict]:
    """Every file under `root` against its reference: TC10's manifest sha where
    the manifest pins it, else the same file's bytes under `ref_root`.
    FAILS IF a sha differs, a pinned file is missing, or the two trees differ."""
    faults, rows = [], {}
    have, ref = tree_files(root), tree_files(ref_root)
    if have != ref:
        faults.append(f"file sets differ: only in clone {sorted(set(have) - set(ref))[:5]}, "
                      f"only in source {sorted(set(ref) - set(have))[:5]}")
    for rel in sorted(set(exp) - set(have)):
        faults.append(f"{rel}: pinned by TC10's manifest but ABSENT")
    for rel in have:
        q = root / rel
        sha = file_sha256(q)
        if rel in exp:
            want, basis = exp[rel], "TC10 STAGE_D_MANIFEST.json"
        else:
            r = ref_root / rel
            want = file_sha256(r) if r.exists() else None
            basis = ("NOT in TC10's manifest — compared with the same file's bytes in the "
                     "TC10 snapshot (read-only)")
        rows[rel] = {"sha256": sha, "bytes": q.stat().st_size, "reference_sha256": want,
                     "reference": basis, "equal": sha == want}
        if sha != want:
            faults.append(f"{rel}: sha {sha[:12]} != reference {str(want)[:12]} ({basis[:26]})")
    return faults, rows


def clone_snapshot(out: Path) -> dict:
    """cp -cpR (APFS clonefile) the TC10 snapshot to the TC11 path when the
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
    if not (TC10_SNAPSHOT / "klines").is_dir():
        raise SystemExit(f"HALT: the TC10 snapshot {TC10_SNAPSHOT} has no klines/")
    out.mkdir(parents=True, exist_ok=True)
    SNAPSHOT.parent.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    subprocess.run(["cp", "-cpR", str(TC10_SNAPSHOT), str(SNAPSHOT)], check=True)
    t1 = time.time()
    exp = tc10_expected_shas()
    faults, rows = clone_findings(SNAPSHOT, exp, TC10_SNAPSHOT)
    log(f"CLONE: cp -cpR {TC10_SNAPSHOT} -> {SNAPSHOT} in {t1 - t0:.1f}s; "
        f"{len(rows)} files re-hashed in {time.time() - t1:.1f}s")
    if faults:
        for f in faults:
            log(f"  !! {f}")
        raise SystemExit(f"HALT: {len(faults)} cloned file(s) do not re-hash to TC10's record — "
                         "the clone is left in place for inspection; nothing was filed")
    doc = {
        "tier": TIER, "stage": STAGE, "seed": SEED,
        "source": str(TC10_SNAPSHOT), "target": str(SNAPSHOT),
        "method": "cp -cpR (APFS clonefile, permissions and times preserved)",
        "law": "every cloned file re-hashes to TC10's STAGE_D_MANIFEST.json (files[] + "
               "out_of_scope_snapshot_files[]); a file the manifest does not pin is compared with "
               "its own bytes in the TC10 snapshot; any mismatch HALTs before anything is filed",
        "tc10_manifest": {"path": "research_outputs/tierc10/data/STAGE_D_MANIFEST.json",
                          "sha256": file_sha256(TC10_MANIFEST)},
        "n_files": len(rows),
        "n_pinned_by_tc10_manifest": sum(1 for r in rows if r in exp),
        "n_not_in_tc10_manifest": sorted(r for r in rows if r not in exp),
        "all_equal": all(v["equal"] for v in rows.values()),
        "cloned_wall_clock_utc": iso(t0 * 1000),
        "files": rows,
    }
    _dump_once(doc, p)
    log(f"CLONE ATTESTED: {doc['n_files']} files, {doc['n_pinned_by_tc10_manifest']} pinned by "
        f"TC10's manifest, all_equal={doc['all_equal']} -> {p}")
    return doc


def load_clone_attest(out: Path | None = None) -> dict:
    p = (out or OUT) / CLONE_ATTEST
    if not p.exists():
        raise SystemExit(f"HALT: no {CLONE_ATTEST} at {p} — run --clone first")
    return json.loads(p.read_text(encoding="utf-8"))


# ═══════════════════════════════════════════════ 1 · THE AS-OF PIN [L-0.1]
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


def _venue_4h_row(open_ms: int) -> list:
    rows = ED._get(ED.REST_BASE + "/fapi/v1/klines",
                   params={"symbol": "BTCUSDT", "interval": "4h",
                           "startTime": open_ms, "endTime": open_ms, "limit": 1}).json()
    if not rows or int(rows[0][0]) != open_ms:
        raise SystemExit(f"HALT: venue does not serve BTCUSDT 4h open {iso(open_ms)}")
    return rows[0]


def pin_findings(pin: dict, tc10_keys: set | None = None) -> list[str]:
    """Faults of a filed pin.  FAILS IF: the close is not the contract's value
    or not a 4h close; open != close - 4h; the ISO strings disagree; the venue
    closeTime of the pinned bar is not close - 1 ms or is not before the venue
    clock; the filed venue kline is not that bar; the seed is not TC11's; or a
    key of TC10's AS_OF_PIN schema is missing."""
    bad = []
    try:
        c, o = int(pin["as_of_last_closed_4h_close_ms"]), int(pin["as_of_last_closed_4h_open_ms"])
        vc, vs = int(pin["venue_close_time_of_pinned_bar_ms"]), int(pin["venue_server_time_ms"])
    except (KeyError, TypeError, ValueError) as e:
        return [f"pin unreadable: {e!r}"]
    if c != PIN_CLOSE_MS:
        bad.append(f"close {c} != the contract's pin {PIN_CLOSE_MS}")
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
    if pin.get("seed") != SEED:
        bad.append(f"seed {pin.get('seed')} != {SEED}")
    miss = sorted((tc10_keys or set()) - set(pin))
    if miss:
        bad.append(f"TC10 AS_OF_PIN keys missing: {miss}")
    return bad


def tc10_pin_keys() -> set:
    return set(json.loads(TC10_PIN_FILE.read_text(encoding="utf-8")))


# ported from scripts/tierc10_data.py:472-517 @ sha256 2cbf9bb6bcfea3ec — CHANGED:
#   the pin is the contract's VALUE (L-0.1), proven closed; the run-time latest is filed beside it
def pin_as_of(out: Path) -> dict:
    """Write-once.  The pin is the 4h close the contract names [L-0.1], proven
    closed by the venue's own closeTime for that bar against the venue clock;
    the latest closed 4h at run time is read off the same clock and filed.

    HALTS IF: the venue does not serve the pinned bar, serves it with a
    closeTime that is not before its own clock, or a filed pin has a fault.
    """
    p = out / "AS_OF_PIN.json"
    if p.exists():
        pin = json.loads(p.read_text(encoding="utf-8"))
        bad = pin_findings(pin, tc10_pin_keys())
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
    venue_close_ms = int(row[6])
    if venue_close_ms >= server_ms:
        raise SystemExit(f"HALT: pinned bar {iso(open_ms)} is still forming on the venue "
                         f"(closeTime {venue_close_ms} >= serverTime {server_ms})")
    if venue_close_ms != PIN_CLOSE_MS - 1:
        raise SystemExit(f"HALT: the venue closes the pinned bar at {venue_close_ms}, not "
                         f"{PIN_CLOSE_MS - 1}")
    if int(lrow[6]) >= server_ms:
        raise SystemExit("HALT: the run-time latest 4h is not closed by the venue clock")
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
        "law": "AS_OF = the 4h bar close the TIER-C11 contract's STEP Q filing names: the latest "
               "4h bar closed when it was filed (2026-09-25T00:09:43Z) [L-0.1]; pinned BY VALUE, "
               "proven closed by the venue's own closeTime < the venue clock; write-once; every "
               "fetch stops at bars closed by as_of_last_closed_4h",
        "seed": SEED,
        # ── TC11 extra keys (TC10's schema above is kept whole) ──
        "tier": TIER, "stage": STAGE,
        "pin_source": f"{LEANS_DOC} L-0.1; contract exchange/queue/2026-09-24_TC11_APOLLO.md "
                      f"sha256 {CONTRACT_SHA256}",
        "venue_kline_of_pinned_bar": row,
        "venue_kline_endpoint": ED.REST_BASE + "/fapi/v1/klines?symbol=BTCUSDT&interval=4h",
        "latest_closed_4h_at_pin_run_open_ms": latest_open,
        "latest_closed_4h_at_pin_run_open": iso(latest_open),
        "latest_closed_4h_at_pin_run_close_ms": latest_open + MS_4H,
        "latest_closed_4h_at_pin_run": iso(latest_open + MS_4H),
        "latest_closed_4h_at_pin_run_venue_close_time_ms": int(lrow[6]),
        "pin_equals_latest_closed_at_pin_run": latest_open == open_ms,
        "tc10_pin_close_ms": TC10_PIN_CLOSE_MS,
        "tc10_pin": iso(TC10_PIN_CLOSE_MS),
        "bars_4h_past_tc10_pin": (open_ms + MS_4H - TC10_PIN_CLOSE_MS) // MS_4H,
    }
    bad = pin_findings(pin, tc10_pin_keys())
    if bad:
        raise SystemExit(f"HALT: the pin about to be filed has faults: {bad}")
    _dump_once(pin, p)
    log(f"AS_OF PINNED: open {pin['as_of_last_closed_4h_open']} close "
        f"{pin['as_of_last_closed_4h']} (venue clock {pin['venue_server_time']}, venue closeTime "
        f"of the bar {venue_close_ms} < serverTime {server_ms}: CLOSED)")
    log(f"  latest closed 4h at run time: {pin['latest_closed_4h_at_pin_run']} "
        f"(== pin: {pin['pin_equals_latest_closed_at_pin_run']})")
    return pin


def venue_latest_closed(out: Path) -> tuple[int, int]:
    """(venue clock ms, close ms of the latest closed 4h) — printed beside the
    pin on every networked run.  One /fapi/v1/time call, logged."""
    with CallLog(out, "clock"):
        server_ms = int(ED._get(ED.REST_BASE + "/fapi/v1/time").json()["serverTime"])
    return server_ms, (server_ms // MS_4H) * MS_4H


def record_fetch_clock(out: Path, pin: dict | None = None) -> tuple[int, int]:
    """[L-0.1] "the latest close at fetch time is printed beside it" — PRINTED
    AND FILED.  One /fapi/v1/time call (its kind='http' row), then one
    kind='clock' row of FETCH_LOG.jsonl carrying the venue clock and the close
    of the latest closed 4h it implies, beside the pin.  --all files it after
    the pin and BEFORE the fetch and the seal; --pin and --fetch file it too.
    [TC11-D_VERIFY defect 8: the 2026-09-25 --all run printed this to stdout
    only and its clock row carries no serverTime; FETCH_CLOCK_NOTE.json records
    what the filed log shows — the write-once log and seal are not rewritten.]"""
    srv, latest = venue_latest_closed(out)
    row = {"kind": "clock", "venue_server_time_ms": srv, "venue_server_time": iso(srv),
           "latest_closed_4h_close_ms": latest, "latest_closed_4h": iso(latest)}
    if pin is not None:
        pinned = int(pin["as_of_last_closed_4h_close_ms"])
        row.update(pinned_close_ms=pinned, pinned=iso(pinned), latest_equals_pin=latest == pinned)
    _fetch_log(out, row)
    log(f"  latest closed 4h at THIS run (venue clock {iso(srv)}): {iso(latest)}"
        + (f" · pinned {iso(row['pinned_close_ms'])}" if pin is not None else "")
        + " -> FETCH_LOG.jsonl kind=clock")
    return srv, latest


# ported from scripts/tierc10_data.py:520-524 @ sha256 2cbf9bb6bcfea3ec — CHANGED: names tierc11_data in the HALT
def load_pin(out: Path | None = None) -> dict:
    p = (out or OUT) / "AS_OF_PIN.json"
    if not p.exists():
        raise SystemExit(f"HALT: no AS_OF pin at {p} — run scripts/tierc11_data.py --pin first")
    return json.loads(p.read_text())


def load_probe() -> dict:
    """TC10's venue of record, read-only [D11-c].  HALTS IF its stems are not
    the commission's seventeen in the commission's order."""
    probe = json.loads(TC10_PROBE.read_text(encoding="utf-8"))
    stems = tuple(a["stem"] for a in probe["classic5"] + probe["unseen12"] if a.get("stem"))
    if stems != PANEL17:
        raise SystemExit(f"HALT: TC10's VENUE_PROBE resolves {stems}, not the commission's {PANEL17}")
    return probe


def panel_assets() -> list[dict]:
    probe = load_probe()
    return [a for a in probe["classic5"] + probe["unseen12"] if a.get("stem")]


# ═══════════════════════════════════════════════ 2 · VENUE (Bybit) + FETCH HELPERS
# ported from scripts/tierc10_data.py:528-546 @ sha256 2cbf9bb6bcfea3ec — VERBATIM
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


# ported from scripts/tierc10_data.py:656-667 @ sha256 2cbf9bb6bcfea3ec — VERBATIM
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


# ported from scripts/tierc10_data.py:670-680 @ sha256 2cbf9bb6bcfea3ec — VERBATIM
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


# ported from scripts/tierc10_data.py:683-686 @ sha256 2cbf9bb6bcfea3ec — VERBATIM
def _fetch_log(out: Path, row: dict) -> None:
    row = {"wall_clock_utc": iso(time.time() * 1000), **row}
    with open(out / "FETCH_LOG.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(row, sort_keys=True) + "\n")


# ported from scripts/tierc10_data.py:689-693 @ sha256 2cbf9bb6bcfea3ec — VERBATIM
def _edge(path: Path, col: str) -> int | None:
    if not path.exists():
        return None
    t = pd.read_parquet(path, columns=[col])[col]
    return int(t.max()) if len(t) else None


# ported from scripts/tierc10_data.py:696-700 @ sha256 2cbf9bb6bcfea3ec — VERBATIM
def _assert_grid(df: pd.DataFrame, iv: str, what: str) -> None:
    off = (df["open_time"].to_numpy(np.int64) - GRID_ANCHOR_MS.get(iv, 0)) % STEP_MS[iv]
    if len(df) and (off != 0).any():
        raise SystemExit(f"HALT: {what}: venue served {int((off != 0).sum())} off-grid "
                         f"open_time(s) — refusing to save")


# ported from scripts/tierc10_data.py:703-724 @ sha256 2cbf9bb6bcfea3ec — VERBATIM
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


# ported from scripts/tierc10_data.py:727-751 @ sha256 2cbf9bb6bcfea3ec — VERBATIM
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


# ═══════════════════════════════════════════════ 3 · CONTRACT SPECS (the TRADING check)
CONTRACT_SPECS = "CONTRACT_SPECS.json"
MULTIPLIER_FIELDS = ("multiplier", "contractSize", "contract_size", "quantity_multiplier",
                     "contractMultiplier", "multiplierSize")
_MULT_PREFIX = re.compile(r"^(\d+)(?=[A-Z])")
NORMALIZATION_LAW, _NL1, _NL2 = source_literal(TC10_SRC, "NORMALIZATION_LAW")


# ported from scripts/tierc10_data.py:1172-1176 @ sha256 2cbf9bb6bcfea3ec — VERBATIM
def base_multiplier(base_asset: str) -> int:
    """TOKENS per contract unit, READ off the venue's own baseAsset name
    [LEAN D-l]: '1000PEPE' -> 1000, 'BTC' -> 1.  Never typed per symbol."""
    m = _MULT_PREFIX.match(base_asset or "")
    return int(m.group(1)) if m else 1


# ported from scripts/tierc10_data.py:1179-1182 @ sha256 2cbf9bb6bcfea3ec — VERBATIM
def normalize_price(px, multiplier: int):
    """Venue price (per contract unit) -> price PER ONE TOKEN.  A PURE SCALING
    by the constant 1/multiplier."""
    return px / multiplier


# ported from scripts/tierc10_data.py:1185-1188 @ sha256 2cbf9bb6bcfea3ec — VERBATIM
def normalize_qty(q, multiplier: int):
    """Venue quantity (contract units) -> quantity in TOKENS.  The inverse
    scaling, so notional px*q is invariant."""
    return q * multiplier


# ported from scripts/tierc10_data.py:1210-1313 @ sha256 2cbf9bb6bcfea3ec — CHANGED:
#   the asset list is TC10's VENUE_PROBE (read-only); a symbol not TRADING HALTs (it is the TRADING check)
def capture_contract_specs(out: Path, pin: dict) -> dict:
    """ONE venue reach per venue, write-once: the venue's own contract spec per
    panel symbol, in TC10's schema.  In TC11 it is also the proof that every
    symbol of record is still TRADING at the pin.

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
        raise SystemExit(f"HALT: symbol(s) of record not TRADING at the TC11 capture: {not_trading}")
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


# ported from scripts/tierc10_data.py:1316-1318 @ sha256 2cbf9bb6bcfea3ec — VERBATIM
def load_contract_specs(out: Path | None = None) -> dict | None:
    p = (out or OUT) / CONTRACT_SPECS
    return json.loads(p.read_text()) if p.exists() else None


# ported from scripts/tierc10_data.py:1334-1365 @ sha256 2cbf9bb6bcfea3ec — CHANGED: artifact path is tierc11's
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
        "artifact": f"research_outputs/tierc11/data/{CONTRACT_SPECS}",
        "artifact_sha256": file_sha256((out or OUT) / CONTRACT_SPECS),
        "capture_instant": ("NOT carried here, and not by name either: no run-time clock key "
                            "enters a deterministic artifact (F-DET scans these files for the "
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


# ═══════════════════════════════════════════════ 4 · PRE_STATE + the inherited-edge audit
# ported from scripts/tierc10_data.py:817-852 @ sha256 2cbf9bb6bcfea3ec — CHANGED:
#   scope = all 124 in-scope files (15m, 1d, 1w included); each row carries its TC10 / clone shas
def write_pre_state(pin: dict, out: Path) -> dict:
    """WRITE-ONCE ledger of every in-scope file of the TC11 clone BEFORE TC11
    fetched anything: file sha, rows, edges, content sha, and the TC10 manifest
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
            raise SystemExit(f"HALT: in-scope file {rel} is missing from the TC11 clone")
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
            "tc10_manifest_sha256": at["reference_sha256"],
            "equals_tc10_manifest": sha == at["reference_sha256"]}
    pre = {"as_of_last_closed_4h": pin["as_of_last_closed_4h"],
           "as_of_last_closed_4h_open": pin["as_of_last_closed_4h_open"],
           "warranty": WARRANTY,
           "law": "write-once; taken on the TC11 clone BEFORE the first TC11 fetch; an old prefix "
                  "may be EXTENDED, never rewritten",
           "scope": "17 x {5m,1h,4h,12h,1d,1w} + CLASSIC5 x 15m + 17 funding tapes [D11-a]",
           "tier": TIER, "stage": STAGE, "seed": SEED,
           "files": files}
    _dump_once(pre, p)
    log(f"PRE_STATE filed: {len(files)} pre-existing in-scope files, all equal to TC10's "
        f"manifest: {all(v['equals_tc10_manifest'] for v in files.values())}")
    return pre


EDGE_AUDIT = "EDGE_AUDIT.json"


def inherited_rows(rel: str, root: Path | None = None) -> pd.DataFrame:
    """The rows of a native kline file that TC10's as-of EXCLUDED (open + step >
    the TC10 close) — pre-existing rows TC11's as-of now includes [D11-b]."""
    _, iv = split_rel(rel)
    d = pd.read_parquet((root or SNAPSHOT) / rel).sort_values("open_time")
    return d[d["open_time"] + STEP_MS[iv] > TC10_PIN_CLOSE_MS].reset_index(drop=True)


def audit_inherited_rows(pin: dict, pre: dict, out: Path) -> dict:
    """READ-ONLY, WRITE-ONCE: every inherited row past TC10's as-of, field by
    field against the venue's REST bar of the same stamp.  Nothing fetched here
    is saved to any file; a difference is a DISCLOSURE (a prefix is never
    rewritten), never a repair."""
    p = out / EDGE_AUDIT
    if p.exists():
        return json.loads(p.read_text())
    ven = {a["stem"]: a for a in panel_assets()}
    rows = {}
    with CallLog(out, "edge_audit"):
        for rel in sorted(pre["files"]):
            if not rel.startswith("klines/"):
                continue
            stem, iv = split_rel(rel)
            if iv in DERIVED_IVS:
                continue
            inh = inherited_rows(rel)
            if not len(inh):
                continue
            a = ven[stem]
            lo, hi = int(inh["open_time"].min()), int(inh["open_time"].max())
            if a["venue"] != "BINANCE_USDTM":
                rest = _retry(lambda: bybit_klines(a["symbol"], iv, lo, hi), f"{stem} {iv} audit")
            else:
                rest = _retry(lambda: ED._fetch_rest_klines(a["symbol"], iv, lo, hi),
                              f"{stem} {iv} audit")
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
            log(f"    edge audit {rel}: {len(inh)} inherited rows {iso(lo)}..{iso(hi)} — "
                f"{'EQUAL to REST' if rows[rel]['all_equal'] else f'{len(diffs)} differ, {len(missing)} missing at REST'}")
    doc = {"as_of_last_closed_4h": pin["as_of_last_closed_4h"],
           "as_of_last_closed_4h_open": pin["as_of_last_closed_4h_open"],
           "warranty": WARRANTY, "tier": TIER, "stage": STAGE, "seed": SEED,
           "law": "READ-ONLY: the pre-existing rows TC10's as-of excluded (open + step > "
                  f"{iso(TC10_PIN_CLOSE_MS)}) but TC11's includes, compared field by field with the "
                  "venue's REST bar of the same stamp; NOTHING fetched here is saved; a difference "
                  "is disclosed, never repaired [D11-b]",
           "audited_wall_clock_utc": iso(time.time() * 1000),
           "files_audited": len(rows),
           "rows_audited": sum(v["inherited_rows"] for v in rows.values()),
           "all_equal": all(v["all_equal"] for v in rows.values()),
           "rows": rows}
    _dump_once(doc, p)
    log(f"EDGE AUDIT filed: {doc['files_audited']} files, {doc['rows_audited']} inherited rows, "
        f"all equal to REST: {doc['all_equal']}")
    return doc


# ported from scripts/tierc10_data.py:855-875 @ sha256 2cbf9bb6bcfea3ec — VERBATIM
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


# ═══════════════════════════════════════════════ 5 · FETCH (the TC11 snapshot only)
# ported from scripts/tierc10_data.py:754-794 @ sha256 2cbf9bb6bcfea3ec — CHANGED:
#   never a whole-tape fetch (a missing file HALTs); the first stamp must lie past the PRE_STATE edge
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
        raise SystemExit(f"HALT: {rel} is absent or not in PRE_STATE — TC11 never fetches a whole tape")
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


# ported from scripts/tierc10_data.py:797-814 @ sha256 2cbf9bb6bcfea3ec — CHANGED:
#   a missing tape HALTs; nothing is asked when the edge's hour is already the pin's (no print can be due)
def extend_funding(a: dict, pin: dict, first_kline_ms: int, out: Path) -> dict:
    stem, sym, venue = a["stem"], a["symbol"], a["venue"]
    close_ms = pin["as_of_last_closed_4h_close_ms"]
    end_ms = close_ms + FUNDING_JITTER_MS
    start_ms = int(first_kline_ms) - DAY_MS
    old = _edge(funding_path(stem), "funding_time")
    if old is None:
        raise SystemExit(f"HALT: funding/{stem}.parquet is absent — TC11 never fetches a whole tape")
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


def run_fetch(pin: dict, out: Path) -> tuple[list[str], dict]:
    """specs -> PRE_STATE -> inherited-edge audit -> 4h, 12h, 1h, funding, 15m,
    5m (TC10's order, 15m added before the 5m).  Returns (incomplete, stats)."""
    capture_contract_specs(out, pin)
    pre = write_pre_state(pin, out)
    audit_inherited_rows(pin, pre, out)
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
    stats["t1"] = time.time()
    return incomplete, stats


# ═══════════════════════════════════════════════ 6 · THE WRITE-ONCE SEAL
SEAL = "WRITE_ONCE_SEAL.json"
SEALED_FILES = ("AS_OF_PIN.json", CLONE_ATTEST, CONTRACT_SPECS, EDGE_AUDIT, "PRE_STATE.json")
FETCH_LOG = "FETCH_LOG.jsonl"


# ported from scripts/tierc10_data.py:884-885 @ sha256 2cbf9bb6bcfea3ec — VERBATIM
def _lines_sha(lines: list[str]) -> str:
    return hashlib.sha256(("\n".join(lines) + "\n").encode("utf-8")).hexdigest()


# ported from scripts/tierc10_data.py:888-926 @ sha256 2cbf9bb6bcfea3ec — CHANGED:
#   SEALED_FILES are TC11's five; a record written after the last fetch row is disclosed as NOT as-first-written
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


# ported from scripts/tierc10_data.py:929-952 @ sha256 2cbf9bb6bcfea3ec — VERBATIM
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


# ═══════════════════════════════════════════════ 7 · DERIVED LENSES [TC10 LEAN L1]
# ported from scripts/tierc10_data.py:956-970 @ sha256 2cbf9bb6bcfea3ec — VERBATIM
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


# ported from scripts/tierc10_data.py:973-986 @ sha256 2cbf9bb6bcfea3ec — VERBATIM
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


# ported from scripts/tierc10_data.py:989-995 @ sha256 2cbf9bb6bcfea3ec — VERBATIM
def _write_if_changed(df: pd.DataFrame, path: Path) -> str:
    if path.exists() and frame_sha(pd.read_parquet(path), KLINE_COLS) == frame_sha(df, KLINE_COLS):
        return "unchanged"
    tmp = path.with_name(f"{path.name}.{os.getpid()}.tmp")
    df.to_parquet(tmp, index=False)
    os.replace(tmp, path)
    return "written"


# ported from scripts/tierc10_data.py:998-1009 @ sha256 2cbf9bb6bcfea3ec — VERBATIM (kline_path is TC11's)
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


def run_derive(pin: dict) -> dict:
    _assert_bound()
    out = {}
    for stem in PANEL17:
        out[stem] = derive_lenses(stem, pin)
        dv = out[stem]
        log(f"    DERIVE {stem:14s} 1d {dv['1d']['rows']:5d} ({dv['1d']['write']:9s}) "
            f"1w {dv['1w']['rows']:4d} ({dv['1w']['write']})")
    return out


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
# ported from scripts/tierc10_data.py:1013-1043 @ sha256 2cbf9bb6bcfea3ec — VERBATIM
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


# ported from scripts/tierc10_data.py:1046-1074 @ sha256 2cbf9bb6bcfea3ec — VERBATIM
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


# ported from scripts/tierc10_data.py:1077-1095 @ sha256 2cbf9bb6bcfea3ec — VERBATIM
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


def fifteen_minute_audit(close_ms: int, root: Path | None = None) -> dict:
    """DISCLOSURE, never a failure [D11-e]: every CLASSIC5 15m bar closed at the
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
            listed.append({"open": iso(tt[k]), "kind": "price" if pm[k] else "volume_only",
                           "era": "tc10" if tt[k] + STEP_MS[FIFTEEN] <= TC10_PIN_CLOSE_MS else "tc11_new",
                           "15m": [float(o15[ok][k]), float(h15[ok][k]), float(l15[ok][k]),
                                   float(c15[ok][k]), float(v15[ok][k])],
                           "from_5m": [float(so[k]), float(sh[k]), float(sl[k]), float(sc[k]),
                                       float(sv[k])]})
        new = tt + STEP_MS[FIFTEEN] > TC10_PIN_CLOSE_MS
        per[stem] = {"bars_15m_as_of": int(len(t15)), "compared": int(ok.sum()),
                     "no_complete_5m_triple": [iso(x) for x in t15[~ok]],
                     "price_mismatch": int(pm.sum()), "volume_only_mismatch": int(vm.sum()),
                     "price_mismatch_tc11_new_bars": int((pm & new).sum()),
                     "volume_only_mismatch_tc11_new_bars": int((vm & new).sum()),
                     "mismatches": listed}
        tot["compared"] += int(ok.sum())
        tot["price_mismatch"] += int(pm.sum())
        tot["volume_only_mismatch"] += int(vm.sum())
        tot["no_complete_5m_triple"] += int((~ok).sum())
    return {"law": "DISCLOSURE, NOT A FAILURE [D11-e]: 15m vs the three native 5m bars it spans; "
                   "open/high/low/close EXACT, volume to relative 1e-9; the venue's intervals "
                   "disagree on incident bars and nothing is reconciled by rewriting a bar",
            "per_asset": per, "totals": tot}


# ═══════════════════════════════════════════════ 9 · FEES [L-1.1, L-1.2]
# ported from scripts/tierc10_data.py:1099-1103 @ sha256 2cbf9bb6bcfea3ec — VERBATIM
def _source_line(path: Path, needle: str) -> int | None:
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if needle in line:
            return i
    return None


# ported from scripts/tierc10_data.py:1369-1376 @ sha256 2cbf9bb6bcfea3ec — VERBATIM
def tier_of(asset: str) -> str:
    """The charter tier of a CONTRACT asset name.  HALTS IF unassigned — an
    unassigned asset must stop the build, never default to the cheapest tier."""
    t = TIER_OF_ASSET.get(asset)
    if t is None:
        raise SystemExit(f"HALT: asset {asset!r} is in NO slippage tier of the contract clause "
                         f"({sorted(TIER_OF_ASSET)}) — the haircut twin refuses to guess")
    return t


# ported from scripts/tierc10_data.py:1379-1381 @ sha256 2cbf9bb6bcfea3ec — VERBATIM
def slippage_bps_side(asset: str) -> float:
    """Charter slippage, bps PER SIDE, for a contract asset name."""
    return float(SLIPPAGE_TIERS[tier_of(asset)]["bps"])


# ported from scripts/tierc10_data.py:1384-1388 @ sha256 2cbf9bb6bcfea3ec — VERBATIM
def charter_bps_side(asset: str) -> float:
    """The charter model's per-side rate: the estate's taker fee PLUS the
    charter slippage of the asset's tier.  Never a replacement for the
    TC-series toll — the caller keeps both."""
    return float(R2.FEE_BPS_SIDE) + slippage_bps_side(asset)


# ported from scripts/tierc10_data.py:1391-1392 @ sha256 2cbf9bb6bcfea3ec — VERBATIM
def charter_round_trip_bps(asset: str) -> float:
    return 2.0 * charter_bps_side(asset)


# ported from scripts/tierc10_data.py:1395-1405 @ sha256 2cbf9bb6bcfea3ec — VERBATIM
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


# ported from scripts/tierc10_data.py:1408-1441 @ sha256 2cbf9bb6bcfea3ec — VERBATIM
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


# ported from scripts/tierc10_data.py:1444-1451 @ sha256 2cbf9bb6bcfea3ec — VERBATIM (load_manifest reads TC11's)
def haircut_twin_for_stem(stem: str, gross_r: float, entry_px: float, exit_px: float,
                          risk_px: float, out: Path | None = None) -> dict:
    """The same, addressed by file stem: the stem -> contract asset map is READ
    from the filed manifest's venue table, never typed."""
    by = {v["stem"]: v["asset"] for v in load_manifest(out)["venues"] if v["stem"]}
    if stem not in by:
        raise SystemExit(f"HALT: the manifest's venue table names no stem {stem}")
    return haircut_twin_net_r(by[stem], gross_r, entry_px, exit_px, risk_px)


# ported from scripts/tierc10_data.py:1454-1496 @ sha256 2cbf9bb6bcfea3ec — VERBATIM
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
    f"MAKER TWIN [L-1.2] — an ADDED column, never the toll of record: maker fee "
    f"{MAKER_BPS_SIDE} bps per side ({2 * MAKER_BPS_SIDE} bps round trip) on the maker legs, "
    "ENTRY and TARGET only, with ZERO slippage on a maker leg; stop and invalidation legs stay "
    f"TAKER at {float(R2.FEE_BPS_SIDE)} bps per side, the toll of record's side rate, with no "
    "slippage in this twin (the charter slippage tier belongs to the haircut twin only "
    "[L-1.1]). A maker leg "
    "is ASSUMED filled at the named price (the contract's wording); the fill-risk column is the "
    "consuming stage's. MNT (Bybit) carries the same figure, an ASSUMPTION: Bybit's maker rate "
    "is not in the repo.")


# ported from scripts/tierc10_data.py:1106-1159 @ sha256 2cbf9bb6bcfea3ec — CHANGED:
#   + maker_* keys [L-1.2] and charter_slippage_* keys per asset; the TC10 keys are kept whole
def fee_schedule(assets: list[dict], funding: dict, pin: dict) -> dict:
    """The estate has NO per-asset venue fee source (the account-rate endpoint
    is signed; the repo holds no key).  What every Tier-C card charges is one
    flat taker figure — filed here per asset, marked ASSUMPTION, with the line
    it is read from.  The value is READ from tierc2_rules, never typed.  The
    maker twin and the charter slippage tier ride beside it as ADDED keys."""
    rules, cfg = ROOT / "scripts" / "tierc2_rules.py", ROOT / "configs" / "naiad_v0.yaml"
    src = [f"scripts/tierc2_rules.py:{_source_line(rules, 'FEE_BPS_SIDE: float')}",
           f"scripts/tierc2_rules.py:{_source_line(rules, 'FEE_BPS_ROUND_TRIP: float')}",
           f"configs/naiad_v0.yaml:{_source_line(cfg, 'fee_bps_side')}"]
    maker_src = [f"README.md:{MAKER_SOURCE_LINE} — {MAKER_SOURCE_TEXT!r}",
                 f"scripts/v3_recompute.py:{_source_line(MAKER_PRECEDENT, MAKER_PRECEDENT_NEEDLE)}"
                 " — the V3 R10 precedent ('maker entries 2 bps/side, taker stops 5 bps/side')"]
    slip_src = [f"Naiad_Phase0_Charter.md:{_source_line(CHARTER_SOURCE, CHARTER_SLIPPAGE_NEEDLE)}",
                f"scripts/tierc10_data.py:{_CLAUSE_L1}-{_CLAUSE_L2} (CONTRACT_SLIPPAGE_CLAUSE, "
                "read by AST)"]
    rows = []
    for a in assets:
        fu = funding.get(a["stem"], {})
        bybit = a["venue"] == "BYBIT_V5_LINEAR"
        rows.append({
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
            # ── TC11 ADDED keys [L-1.2 maker twin; the charter slippage tier] ──
            "maker_bps_per_side": MAKER_BPS_SIDE,
            "maker_round_trip_bps": 2.0 * MAKER_BPS_SIDE,
            "maker_slippage_bps_side": 0.0,
            "maker_kind": ("ASSUMPTION — Bybit's maker rate is not in the repo; the Binance VIP0 "
                           "figure is applied to MNT unchanged [L-1.2]" if bybit else
                           "ASSUMPTION — Binance USDT-M VIP0 maker per README; the engine books "
                           "every fill as taker; this is a TWIN, never the toll of record [L-1.2]"),
            "maker_source": maker_src,
            "charter_slippage_tier": tier_of(a["asset"]),
            "charter_slippage_bps_per_side": slippage_bps_side(a["asset"]),
            "charter_slippage_source": slip_src,
        })
    return {"as_of_last_closed_4h": pin["as_of_last_closed_4h"],
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
            "maker_bps_per_side": MAKER_BPS_SIDE,
            "maker_law": MAKER_LAW,
            "maker_source": maker_src,
            "charter_slippage_tiers": {t: {"bps_per_side": b["bps"], "assets": list(b["assets"])}
                                       for t, b in sorted(SLIPPAGE_TIERS.items())},
            "charter_slippage_source": slip_src,
            "tier": TIER, "seed": SEED,
            "assets": rows}


# ═══════════════════════════════════════════════ 10 · THE MANIFEST (no network, no write)
# ported from scripts/tierc10_data.py:1838-1861 @ sha256 2cbf9bb6bcfea3ec — VERBATIM
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
    "BULK ARCHIVE, is the record on incident bars). TC11 fetched REST only; its rows past each "
    "TC10 edge are REST by construction.",
    "CARRIED FROM TC10, STILL OPEN: PUMPFUN -> PUMPUSDT [LEAN D-d] and MNT -> Bybit v5 linear "
    "[LEAN D-c] await the operator's nod.",
    "CARRIED FROM TC10, STILL OPEN: the LaCie mirror [LEAN L5] — the TC11 snapshot, like TC10's, "
    "exists only on this laptop.",
    "TC11: the maker twin's 2.0 bps/side is an ASSUMPTION read from README.md (Binance VIP0), "
    "applied to MNT (Bybit) as well [L-1.2]; whether slippage joins the toll of record is TC10's "
    "open question Q2 and is not answered here [L-1.1].",
)
STANDING_DISCLOSURES = (
    "The executor made two connectivity probes (Binance /fapi/v1/time and one BTCUSDT 4h kline, "
    "Bybit /v5/market/time) with curl BEFORE this module existed; they are not in FETCH_LOG.jsonl "
    "and nothing they returned was saved or used.",
    "The 5m rows 16:00-16:25Z of 2026-09-21 (14 Binance stems) and the 15m rows 16:00/16:15Z "
    "(CLASSIC5) PRE-DATE TC10 (copied from the live cache before TC10's pin) and sat past TC10's "
    "as-of; TC11's as-of includes them. They are INHERITED, not refetched [D11-b]; EDGE_AUDIT.json "
    "compares each with REST read-only and inherited_edge_audit prints the result.",
    "The 15m tapes of the nine non-CLASSIC5 stems that hold one stay in the snapshot untouched "
    "and out of scope (listed by sha under out_of_scope_snapshot_files), as the 1m tapes do.",
)
CARRIED_KEYS = ("two_token_trap", "data_spend", "venue_publications_disagree")


def _tc10_manifest() -> tuple[dict, str]:
    return json.loads(TC10_MANIFEST.read_text(encoding="utf-8")), file_sha256(TC10_MANIFEST)


def cache_manifest_staleness(q: Path, files: list[dict], other: list[dict],
                             extended: list[str]) -> dict:
    """[TC11-D verification round 2, defect 7] The snapshot root's MANIFEST.json,
    DESCRIBED (never used): what it says of itself, and how many of the files
    it lists it still describes at their TC11 bytes.  Read-only; the shas
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
        "listed_files_absent_from_the_tc11_snapshot": absent,
        "listed_files_at_their_tc11_bytes": len(at_bytes),
        "in_scope_files_it_lists": len(in_scope_listed),
        "tc11_extended_files": len(extended),
        "tc11_extended_files_it_describes_at_their_tc11_bytes": len(ext_described),
        "disclosure": (
            f"The snapshot root's MANIFEST.json ({q.stat().st_size} B, sha256 "
            f"{file_sha256(q)[:16]}…) is carried byte-for-byte from the TC10 snapshot; TC10's "
            "manifest does not pin it (CLONE_ATTEST compares it with the TC10 snapshot's own "
            "bytes). It is a cache manifest written by another estate (self-described "
            f"created_utc {selfd['created_utc']}, mode {selfd['mode']!r}, {len(listed)} files) and "
            f"it is {'STALE' if stale else 'CURRENT'}: of the other {len(known)} files of the TC11 "
            f"snapshot it describes {len(at_bytes)} at their current bytes ({absent} of the files "
            f"it lists are not in the snapshot), and "
            f"{len(ext_described)} of the {len(extended)} files TC11 extended. No TC11 loader "
            "reads it; it is listed under out_of_scope_snapshot_files and read only to describe "
            "it here."),
    }


def build_manifest(pin: dict, pre: dict) -> dict:
    """TC10's STAGE_D_MANIFEST schema, at the TC11 pin, read-only: nothing is
    fetched and nothing in the snapshot is written (the derived lenses are
    re-derived IN MEMORY and must equal the files).  Same top-level keys as
    TC10's, plus the TC11 blocks (tc11_extension, fifteen_minute_audit,
    inherited_edge_audit, clone_attestation, carried_from_tc10, tc10_record)."""
    close_ms = int(pin["as_of_last_closed_4h_close_ms"])
    probe = load_probe()
    tc10, tc10_sha = _tc10_manifest()
    tc10_rows = {f["path"]: f for f in tc10["files"]}
    tc10_other = {o["path"]: o for o in tc10["out_of_scope_snapshot_files"]}
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
                "DERIVED from native 4h [TC10 LEAN L1], re-derived at the TC11 pin" if derived else
                ("PRE-EXISTING in the TC10 snapshot (bytes == TC10's manifest, F-D11-CLONE); old "
                 f"edge {iso(was['last_ms'])}; rows past it are TC11 REST"
                 + (" (15m: out of TC10's scope, listed there by sha only; copied from the live "
                    "cache before TC10's pin)" if iv == FIFTEEN else "")))
            if derived:
                row["publication_inherited_from"] = f"klines/{stem}_4h.parquet"
            if q.exists():
                df = pd.read_parquet(q)
                row.update(sha256=file_sha256(q), bytes=q.stat().st_size,
                           **scan_klines(df, iv, close_ms))
                # [L-F.1; TC11-D verification round 2, defect 8] the parquet CONTENT sha
                row["content_sha"] = frame_sha(df.sort_values("open_time"), KLINE_COLS)
                tgt = target_last_open(iv, close_ms)
                row["complete_to_as_of"] = bool(row["as_of_last_closed_bar_open"] == iso(tgt))
                row["lens_last_closed_bar_at_pin"] = {"open": iso(tgt), "close": iso(tgt + STEP_MS[iv])}
                row["last_bar_close_equals_lens_last_closed_at_pin"] = bool(row["last_open_ms"] == tgt)
                row["tc10_manifest_sha256"] = (tc10_rows.get(rel, {}).get("sha256")
                                               or tc10_other.get(rel, {}).get("sha256"))
                row["pre_state"] = {"rows": was["rows"], "last_open": iso(was["last_ms"]),
                                    "file_sha256": was["file_sha256"],
                                    "content_sha": was["content_sha"]}
                row["tc11_rows_added"] = int(len(df) - was["rows"])
                ext.setdefault(iv, {})[stem] = {
                    "added": row["tc11_rows_added"],
                    "first_new_open": (iso(was["last_ms"] + STEP_MS[iv])
                                       if row["tc11_rows_added"] else None),
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
                    t10pub = tc10_rows.get(rel, {}).get("publication")
                    if a["venue"] != "BINANCE_USDTM":
                        pub = dict(t10pub or {"carries": "BYBIT-REST"})
                    elif t10pub is not None:
                        pub = dict(t10pub)
                    else:
                        pub = {"carries": "UNAUDITED", "differs_from_rest_bars": None,
                               "differs_from_archive_bars": None,
                               "rest_basis": "NO REST census (15m was out of TC10's scope)",
                               "archive_lacks_bars": None}
                    pub["tc11_rows_past_tc10_edge"] = (
                        "REST — fetched by TC11 over the venue's REST API (Bybit v5 REST for MNT); "
                        "not archive-censused")
                    pub["measured_by"] = ("TC10 (carried from its manifest)" if t10pub is not None
                                          else "nobody (UNAUDITED)")
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
            row["tc10_manifest_sha256"] = tc10_rows.get(rel, {}).get("sha256")
            row["pre_state"] = {"rows": was["rows"], "last": iso(was["last_ms"]),
                                "file_sha256": was["file_sha256"], "content_sha": was["content_sha"]}
            row["tc11_rows_added"] = int(fs["rows"] - was["rows"])
            ext.setdefault("funding", {})[stem] = {"added": row["tc11_rows_added"],
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
                              "tc10_manifest_sha256": ref, "unchanged_since_tc10": sha == ref})
    # [TC11-D verification round 2, defect 7] every OTHER file of the snapshot (the root
    # MANIFEST.json above all), appended after the klines/funding rows so their order holds
    extended = sorted(f["path"] for f in files if f.get("tc11_rows_added"))
    root_disclosures = []
    for rel in tree_files(SNAPSHOT):
        if rel in in_scope or rel.startswith(("klines/", "funding/")):
            continue
        q = SNAPSHOT / rel
        sha = file_sha256(q)
        ref = attest["files"].get(rel, {}).get("reference_sha256")
        row = {"path": rel, "sha256": sha, "bytes": q.stat().st_size,
               "tc10_manifest_sha256": None, "tc10_snapshot_sha256": ref,
               "unchanged_since_tc10": sha == ref}
        if rel == "MANIFEST.json":
            row.update(cache_manifest_staleness(q, files, other, extended))
            root_disclosures.append(row["disclosure"])
        other.append(row)
    adm = [r for r in admission if r["admitted"]]
    prefixes = verify_prefixes(pre)
    lens_set = LENS_ORDER
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
        # BY CONSTRUCTION (guard + _assert_bound), NOT MEASURED [TC11-D_VERIFY defect 3]: the
        # substrate guard (import) + _assert_bound (before every snapshot write) are its basis
        # (F-D11-GUARD, F-D11-BOUND). The key stays the bool TC10's schema holds; its basis is
        # filed beside it [TC11-D verification round 2, finding 2].
        "live_cache_touched": False,
        "live_cache_touched_basis": LIVE_CACHE_BASIS,
        "venues": [{**{k: a.get(k) for k in ("asset", "venue", "symbol", "stem", "status",
                                             "contract_type", "listing", "venue_reason")},
                    "status_at_tc11_capture": status.get(a.get("stem"))}
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
        "mirror": "LaCie mirror NOT done [TC10 LEAN L5 carried] — every file TC11 fetched exists "
                  "ONLY in the TC11 snapshot on this laptop",
        "leans": list(LEANS),
    }
    for k in CARRIED_KEYS:
        man[k] = tc10.get(k)
    man["carried_from_tc10"] = {
        "keys": list(CARRIED_KEYS),
        "manifest": "research_outputs/tierc10/data/STAGE_D_MANIFEST.json",
        "manifest_sha256": tc10_sha,
        "why": "[D11-d] measured by TC10 on the TC10 snapshot; the TC11 clone reproduces every "
               "byte of it (F-D11-CLONE) and every pre-existing row is byte-identical after the "
               "fetch (F-D11-PREFIX), so the measurement stands for the inherited rows; the rows "
               "TC11 added are REST and are not re-audited against the archive. Carried VERBATIM, "
               "not re-measured."}
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
        "kline_law": "a TC11 file holding rows past the pin would be read past it by "
                     "tierc2_baseline.load_klines (whole file); tierc11_data.load_asof cuts them",
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
        "artifact": f"research_outputs/tierc11/data/{SEAL}" if seal else None,
        "sealed_sha256": {n: v["sha256"] for n, v in sorted(seal.get("files", {}).items())},
        "fetch_log_sealed_lines": seal.get("fetch_log", {}).get("sealed_lines"),
        "fetch_log_sha256_of_sealed_lines": seal.get("fetch_log", {}).get("sha256_of_sealed_lines"),
        "faults": seal_faults, "all_ok": not seal_faults,
        "disclosure": seal.get("disclosure", [])}
    # ── the TC11 blocks ──
    man["tc11_extension"] = {
        "law": "every in-scope file extended from its PRE_STATE edge + one step to the last bar "
               "closing <= the pin (REST only); 1d/1w re-derived from the extended native 4h",
        "per_lens": {iv: {"files": len(ext[iv]),
                          "rows_added_total": int(sum(v["added"] for v in ext[iv].values())),
                          "rows_added_per_stem": {s: ext[iv][s] for s in ext[iv]}}
                     for iv in list(lens_set) + ["funding"] if iv in ext}}
    man["fifteen_minute_audit"] = fifteen_minute_audit(close_ms)
    ea_p = OUT / EDGE_AUDIT
    ea = json.loads(ea_p.read_text()) if ea_p.exists() else None
    man["inherited_edge_audit"] = (None if ea is None else {
        "artifact": f"research_outputs/tierc11/data/{EDGE_AUDIT}",
        "artifact_sha256": file_sha256(ea_p), "law": ea["law"],
        "files_audited": ea["files_audited"], "rows_audited": ea["rows_audited"],
        "all_equal": ea["all_equal"],
        "per_file": {k: {kk: v[kk] for kk in ("inherited_rows", "first_open", "last_open",
                                              "equal_rows", "differing", "missing_at_rest",
                                              "all_equal")}
                     for k, v in sorted(ea["rows"].items())}})
    man["clone_attestation"] = {
        "artifact": f"research_outputs/tierc11/data/{CLONE_ATTEST}",
        "artifact_sha256": file_sha256(OUT / CLONE_ATTEST),
        "source": attest["source"], "target": attest["target"], "method": attest["method"],
        "n_files": attest["n_files"], "n_pinned_by_tc10_manifest": attest["n_pinned_by_tc10_manifest"],
        "n_not_in_tc10_manifest": attest["n_not_in_tc10_manifest"],
        "all_equal": attest["all_equal"],
        "tc10_manifest_sha256_at_clone": attest["tc10_manifest"]["sha256"],
        "tc10_manifest_sha256_now": tc10_sha}
    man["tc10_record"] = {
        "tc10_as_of_last_closed_4h": tc10["as_of_last_closed_4h"],
        "venue_probe": {"path": "research_outputs/tierc10/data/VENUE_PROBE.json",
                        "sha256": file_sha256(TC10_PROBE)},
        "as_of_pin": {"path": "research_outputs/tierc10/data/AS_OF_PIN.json",
                      "sha256": file_sha256(TC10_PIN_FILE)},
        "manifest": {"path": "research_outputs/tierc10/data/STAGE_D_MANIFEST.json",
                     "sha256": tc10_sha},
        "ported_from": {"path": "scripts/tierc10_data.py", "sha256": TC10_SRC_SHA256,
                        "sha256_now": file_sha256(TC10_SRC)}}
    man["contract"] = {"path": "exchange/queue/2026-09-24_TC11_APOLLO.md", "sha256": CONTRACT_SHA256,
                       "leans": LEANS_DOC, "plan": C_MAP_DOC}
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
                       and not man["two_token_trap"]["intended_asset_unconfirmed"])
    return man


def manifest_md(man: dict, fees: dict) -> str:
    """A compact reading of the manifest (deterministic; the JSON is the record)."""
    L = [f"# {TIER} · STAGE {STAGE} — THE CORRIDOR (STAGE_D_MANIFEST)", "",
         f"- **AS_OF** {man['as_of_last_closed_4h']} (close ms {man['as_of_last_closed_4h_close_ms']}) "
         f"· seed {man['seed']} · snapshot `{man['snapshot_root']}` · complete **{man['complete']}**",
         f"- Clone: {man['clone_attestation']['n_files']} files, all equal to TC10's record: "
         f"{man['clone_attestation']['all_equal']} · prefix attestation all_ok "
         f"{man['prefix_attestation']['all_ok']} ({len(man['prefix_attestation']['rows'])} files) · "
         f"seal all_ok {man['write_once']['all_ok']}",
         f"- Panel: {man['panels']['panel_size']} admitted — {' '.join(man['panels']['PANEL17_stems'])}",
         "", "## Last closed bar per lens at the pin", "", "| lens | open | close |", "|---|---|---|"]
    for iv, b in man["as_of_last_closed_bar_per_lens"].items():
        L.append(f"| {iv} | {b['open']} | {b['close']} |")
    L += ["", "## Rows added by TC11 per lens (every file whole)", "",
          "| lens | files | rows added | per stem |", "|---|---|---|---|"]
    for iv, b in man["tc11_extension"]["per_lens"].items():
        per = " ".join(f"{s}:{v['added']}" for s, v in b["rows_added_per_stem"].items())
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
          "| stem | compared | price mismatch | volume-only | no 5m triple | of which TC11-new bars |",
          "|---|---|---|---|---|---|"]
    for s, v in fa["per_asset"].items():
        L.append(f"| {s} | {v['compared']} | {v['price_mismatch']} | {v['volume_only_mismatch']} | "
                 f"{len(v['no_complete_5m_triple'])} | {v['price_mismatch_tc11_new_bars']} price, "
                 f"{v['volume_only_mismatch_tc11_new_bars']} volume |")
    ea = man["inherited_edge_audit"]
    if ea:
        L += ["", f"## Inherited rows past TC10's as-of vs REST — {ea['rows_audited']} rows in "
                  f"{ea['files_audited']} files, all equal: {ea['all_equal']}", ""]
        for k, v in ea["per_file"].items():
            if not v["all_equal"]:
                L.append(f"- {k}: {len(v['differing'])} differ, {len(v['missing_at_rest'])} missing")
    L += ["", "## Fees", "", "| stem | taker bps/side | round trip | maker bps/side | slippage tier |",
          "|---|---|---|---|---|"]
    for a in fees["assets"]:
        L.append(f"| {a['stem']} | {a['taker_bps_side_used']} | {a['round_trip_bps_used']} | "
                 f"{a['maker_bps_per_side']} | {a['charter_slippage_tier']} "
                 f"{a['charter_slippage_bps_per_side']} |")
    L += ["", "## Leans", ""] + [f"- {x}" for x in man["leans"]]
    L += ["", "## Standing disclosures", ""] + [f"- {x}" for x in man["standing_disclosures"]]
    L += ["", "## Operator rulings needed", ""] + [f"- {x}" for x in man["operator_rulings_needed"]]
    return "\n".join(L) + "\n"


def _out_guard(dst: Path) -> Path:
    """--out must be the stage directory, a directory under it, or a system
    temp directory.  HALTS IF it is anywhere else (the TC10 tree above all)."""
    r = dst.expanduser().resolve()
    tmps = {Path(tempfile.gettempdir()).resolve(), Path("/private/tmp").resolve()}
    if r == OUT.resolve() or OUT.resolve() in r.parents or any(t in r.parents for t in tmps):
        return r
    raise SystemExit(f"HALT: --out {r} is not {OUT}, under it, or under a temp directory")


def write_manifest(dst: Path) -> dict:
    """STAGE_D_MANIFEST.json + .md and fee_schedule.json into `dst` — no network,
    no snapshot write.  F-DET runs exactly this twice."""
    dst = _out_guard(dst)
    pin = load_pin(OUT)
    pre = json.loads((OUT / "PRE_STATE.json").read_text())
    man = build_manifest(pin, pre)
    assets = [a for a in load_probe()["classic5"] + load_probe()["unseen12"] if a.get("stem")]
    fees = fee_schedule(assets, {f["stem"]: f for f in man["files"]
                                 if f["kind"] == "funding" and f["present"]}, pin)
    man["tiered_costs_haircut_twin"] = haircut_twin_table(
        [a for a in assets if a["asset"] in {r["asset"] for r in man["admission"]["rows"]
                                             if r["admitted"]}], fees)
    _dump(man, dst / "STAGE_D_MANIFEST.json")
    _dump(fees, dst / "fee_schedule.json")
    (dst / "STAGE_D_MANIFEST.md").write_text(manifest_md(man, fees), encoding="utf-8")
    return man


# ═══════════════════════════════════════════════ downstream API (no network)
# ported from scripts/tierc10_data.py:2772-2776 @ sha256 2cbf9bb6bcfea3ec — VERBATIM
def load_manifest(out: Path | None = None) -> dict:
    p = (out or OUT) / "STAGE_D_MANIFEST.json"
    if not p.exists():
        raise SystemExit(f"HALT: no Stage D manifest at {p}")
    return json.loads(p.read_text())


# ported from scripts/tierc10_data.py:2779-2783 @ sha256 2cbf9bb6bcfea3ec — VERBATIM
def panel(out: Path | None = None) -> dict:
    """{'CLASSIC5': [...], 'UNSEEN': [...admitted stems...], 'PANEL17': [...]}"""
    m = load_manifest(out)["panels"]
    return {"CLASSIC5": m["CLASSIC5"], "UNSEEN": m["UNSEEN_admitted_stems"],
            "PANEL17": m["PANEL17_stems"]}


# ported from scripts/tierc10_data.py:2786-2794 @ sha256 2cbf9bb6bcfea3ec — VERBATIM (STEP_MS has 15m)
def load_asof(stem: str, iv: str, out: Path | None = None) -> pd.DataFrame:
    """The ONLY as-of-safe kline read for TC10: bars of lens `iv` CLOSED at the
    pinned AS_OF, ascending.  HALTs on a missing file (never an empty frame)."""
    close_ms = load_pin(out)["as_of_last_closed_4h_close_ms"]
    p = kline_path(stem, iv)
    if not p.exists():
        raise SystemExit(f"HALT: missing {p}")
    d = pd.read_parquet(p).sort_values("open_time")
    return d[d["open_time"] + STEP_MS[iv] <= close_ms].reset_index(drop=True)


# ported from scripts/tierc10_data.py:2797-2807 @ sha256 2cbf9bb6bcfea3ec — VERBATIM
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


# ported from scripts/tierc10_data.py:2810-2825 @ sha256 2cbf9bb6bcfea3ec — VERBATIM
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


# The ported functions and their provenance, for F-D11-PORT (name -> reason; "" = VERBATIM)
PORTS = {
    "pin_literal": "", "parse_slippage_clause": "", "log": "", "iso": "", "file_sha256": "",
    "frame_sha": "", "_dump": "", "_dump_once": "", "kline_path": "", "funding_path": "",
    "target_last_open": "", "_bybit_get": "", "_retry": "", "binance_brake": "",
    "_fetch_log": "", "_edge": "", "_assert_grid": "", "bybit_klines": "", "bybit_funding": "",
    "base_multiplier": "", "normalize_price": "", "normalize_qty": "",
    "load_contract_specs": "", "verify_prefixes": "", "_lines_sha": "", "verify_seal": "",
    "derive_1d": "", "derive_1w": "", "_write_if_changed": "", "derive_lenses": "",
    "scan_klines": "", "scan_funding": "", "funding_coverage": "", "_source_line": "",
    "tier_of": "", "slippage_bps_side": "", "charter_bps_side": "", "charter_round_trip_bps": "",
    "assert_tiers_cover": "", "haircut_twin_net_r": "", "haircut_twin_for_stem": "",
    "haircut_twin_table": "", "premise_checks": "", "load_manifest": "", "panel": "",
    "load_asof": "", "with_funding_hour": "", "load_funding_asof": "",
    "pin_as_of": "the pin is the contract's VALUE [L-0.1], proven closed; the run-time latest filed beside",
    "load_pin": "the HALT names tierc11_data",
    "capture_contract_specs": "asset list from TC10's VENUE_PROBE (read-only); not-TRADING HALTs",
    "contract_multiplier_table": "artifact path is tierc11's",
    "write_pre_state": "scope = 124 files (15m, 1d, 1w in); TC10/clone shas per row",
    "extend_klines": "no whole-tape fetch; first stamp must lie past the PRE_STATE edge",
    "extend_funding": "a missing tape HALTs; skip when the edge is already in the pin's hour",
    "seal_provenance": "TC11's five SEALED_FILES; a late write is disclosed as a finding",
    "fee_schedule": "+ maker_* [L-1.2] and charter_slippage_* keys; TC10 keys whole",
    "STEP_MS": 'gains "15m": 900_000',                     # a constant port (an Assign, not a def)
}


# ═══════════════════════════════════════════════ run
def summarize(pin: dict, man: dict) -> None:
    log(f"\nAS_OF {pin['as_of_last_closed_4h']} (open {pin['as_of_last_closed_4h_open']}); venue "
        f"closeTime {pin['venue_close_time_of_pinned_bar_ms']} < venue clock "
        f"{pin['venue_server_time_ms']} ({pin['venue_server_time']})")
    log("NEW BARS PER LENS (rows added by TC11, per stem):")
    for iv, b in man["tc11_extension"]["per_lens"].items():
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
        log(f"INHERITED EDGE ROWS vs REST: {ea['rows_audited']} rows / {ea['files_audited']} files, "
            f"all equal {ea['all_equal']}")
    log(f"SEAL faults: {man['write_once']['faults'] or 'none'} · complete={man['complete']}")


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
    log("\nDERIVE 1d/1w from native 4h")
    run_derive(pin)
    seal_provenance(OUT)
    man = write_manifest(OUT)
    summarize(pin, man)
    log(f"elapsed {time.time() - t0:.0f}s")
    if not man["prefix_attestation"]["all_ok"]:
        log("*** HALT: an old prefix moved. ***")
        return 1
    if incomplete or not man["complete"]:
        log("INCOMPLETE:")
        for x in sorted(set(incomplete)):
            log(f"  - {x}")
        return 2
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    for flag in ("clone", "pin", "fetch", "derive", "seal", "manifest", "all"):
        ap.add_argument(f"--{flag}", action="store_true")
    ap.add_argument("--out", default=str(OUT), help="--manifest only: the directory to file into")
    a = ap.parse_args()
    picked = [f for f in ("clone", "pin", "fetch", "derive", "seal", "manifest", "all") if getattr(a, f)]
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
        record_fetch_clock(OUT, pin)                    # [L-0.1] the latest close AT FETCH TIME
        incomplete, stats = run_fetch(pin, OUT)
        log(f"FETCH wall {stats['t1'] - stats['t0']:.1f}s; HTTP calls {CallLog.counts}")
        return 2 if incomplete else 0
    if cmd == "derive":
        run_derive(load_pin(OUT))
        return 0
    if cmd == "seal":
        seal_provenance(OUT)
        bad = verify_seal(OUT)
        log(f"seal faults: {bad or 'none'}")
        return 1 if bad else 0
    if cmd == "manifest":
        man = write_manifest(Path(a.out))
        return 0 if man["complete"] else 2
    return run_all()


if __name__ == "__main__":
    sys.exit(main())
