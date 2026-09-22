#!/usr/bin/env python
"""TIER-C10 · STAGE D — THE DATA MODULE.  Twelve unseen assets + the five classics.

RATIFIED operator 2026-09-21 (contract TIER-C10).  Drafted APOLLO, executed
HEPHAESTUS; seed 20260921.  This module FETCHES and DESCRIBES; it scores
nothing, runs no card, and imports no decision module's entry points.

WHAT IT DOES, IN ORDER
  1. PINS the as-of: AS_OF = the last CLOSED 4h bar at the FIRST run's start,
     read off the VENUE's clock (not this laptop's), proven closed against the
     venue's own closeTime, then persisted (AS_OF_PIN.json, write-once).  A
     resumed run re-reads the pin — a multi-hour 5m fetch must not move its
     own as-of.  Every fetch stops at closed bars <= AS_OF.
  2. PROBES the venue of record per asset and prints it: Binance USDT-M perps
     by default; an alternate ONLY where Binance has no contract at all, and
     then for the WHOLE tape (one venue per asset, NEVER spliced).
  3. EXTENDS the frozen snapshot forward: klines {5m,1h,4h,12h} + funding for
     every candidate, through the estate's OWN fetchers (engine.data), into
     $NAIAD_CACHE_DIR == the TC10 snapshot and nowhere else.  A file that
     already exists is only ever extended past its old edge; PRE_STATE.json
     holds every old prefix's sha so that is provable afterwards.  DISCLOSED
     [LEAN D-h]: PRE_STATE.json and VENUE_PROBE.json were taken before the
     first fetch but RE-STAMPED once afterwards (the as-of + warranty keys);
     "write-once" is enforced in CODE only from _dump_once / --seal onward —
     WRITE_ONCE_SEAL.json holds their shas and F-D-SEAL re-hashes them.
  4. DERIVES 1d and 1w from NATIVE 4h [LEAN L1]: 1d = exactly six complete
     4h bars of one UTC day; 1w = seven such days, MONDAY-anchored, complete
     weeks only.  Incomplete buckets are DROPPED and counted, never patched.
  5. ADMITS on >= TIDE_SLOW + MEM_TTL_BARS (316 + 400 = 716, derived from the
     two pins, not typed) closed 4h bars; the excluded are NAMED with counts.
  6. COUNTS gaps, duplicates, off-grid stamps and the venue's own zero-volume
     flat bars per file.  Nothing is ever inserted: a hole stays a hole and is
     listed; a flat bar the venue published is the venue's and says so.
  7. FILES fee_schedule.json (the estate's flat taker figure, marked
     ASSUMPTION with its source line; funding interval OBSERVED per asset)
     and STAGE_D_MANIFEST.json/.md (sha256 per file, rows, edges, gaps,
     venue, listing date, snapshot root, AS_OF).
  8. FILES the four RESUME-contract artifacts of 2026-09-22: CONTRACT_SPECS.json
     (the venue's own contract spec per symbol — the multiplier printed and
     normalized, 1000PEPEUSDT and 1000BONKUSDT quoting PER 1000 TOKENS), the
     TWO-TOKEN TRAP table (intended asset, listing instant + source, the hard
     floor, and price continuity AT the floor proven by rebuilding the floor bar
     from its own native 5m children), DATA_SPEND_AUDIT.json ({never-touched /
     display-only / scored} per asset with the evidence line — P-GEN-1's hard
     dependency) and the TIERED COSTS HAIRCUT TWIN (the charter model as an
     ADDED column beside the TC-series toll, never a replacement).
  9. AUDITS (--audit-rest / --audit-archive, read-only): the venue publishes
     every native bar TWICE — its REST API and its BULK ARCHIVE — and the two
     disagree on a few incident bars.  WHICH of the two a pre-existing file
     carries is MEASURED per (file, lens) over the WHOLE history, both ways
     (REST_VS_SNAPSHOT_AUDIT.json, ARCHIVE_VS_SNAPSHOT_AUDIT.json) — it is
     NOT inferred from how a file was assembled: the first filing inferred
     "pre-existing = archive" and the review measured the opposite for the
     classics.  The panel is publication-HETEROGENEOUS; nothing is reconciled
     by rewriting a bar [LEAN D-f].

WHAT WOULD MAKE THIS WRONG: pinning the wall clock instead of a closed bar;
writing anywhere but the snapshot (the live cache is READ-NEVER, WRITE-NEVER
for TC10 — the guard below HALTs before the first import that could bind a
path); rewriting behind an old edge; letting a second venue share a file
stem with the first; calling a derived day "native"; stating a provenance
that was inferred as if it had been measured; importing the range machine
here (any decision module that imports this one for load_asof / panel would
drag it into its closure — the MEM_TTL pin is READ from the source instead).

Run (network):  NAIAD_CACHE_DIR=~/.cache/naiad/snapshots/tc10_20260921 \\
                  ~/venvs/naiad/bin/python scripts/tierc10_data.py
Re-describe (no network, e.g. F-DET):  ... scripts/tierc10_data.py --offline [--out DIR]
Audit (read-only, network):  ... scripts/tierc10_data.py --audit-rest 4h,1h
                             ... scripts/tierc10_data.py --audit-archive 4h,1h
Seal (once, no network):     ... scripts/tierc10_data.py --seal
Contract specs (ONE venue reach, write-once):  ... scripts/tierc10_data.py --contract-specs
Exit: 0 complete · 2 fetch incomplete (re-run resumes) · 1 HALT.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import re
import sys
import time
import zipfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = Path.home() / ".cache" / "naiad" / "snapshots" / "tc10_20260921"
LIVE_CACHE = Path.home() / ".cache" / "naiad" / "data_cache"


def assert_substrate() -> Path:
    """THE FROZEN-SUBSTRATE GUARD [HARD LAW 3].  Runs BEFORE engine.data or any
    tier module is imported, because some of them bind cache paths at import.

    HALTS IF: NAIAD_CACHE_DIR is unset, points anywhere but the TC10 snapshot,
    or resolves to the live cache.
    """
    env = os.environ.get("NAIAD_CACHE_DIR", "")
    if not env:
        raise SystemExit("HALT: NAIAD_CACHE_DIR is unset — TC10 reads and "
                         f"writes ONLY the snapshot {SNAPSHOT}")
    got = Path(env).expanduser().resolve()
    if got == LIVE_CACHE.resolve():
        raise SystemExit("HALT: NAIAD_CACHE_DIR is the LIVE cache — READ-NEVER, "
                         "WRITE-NEVER for TC10")
    if got != SNAPSHOT.resolve():
        raise SystemExit(f"HALT: NAIAD_CACHE_DIR={got} is not the TC10 snapshot "
                         f"{SNAPSHOT}")
    if not (got / "klines").is_dir():
        raise SystemExit(f"HALT: snapshot has no klines/ directory: {got}")
    return got


assert_substrate()

import numpy as np                                                   # noqa: E402
import pandas as pd                                                  # noqa: E402
import requests                                                      # noqa: E402

sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from engine import data as ED                                        # noqa: E402
from engine.cells import INTERVAL_MS                                 # noqa: E402
import tierc2_rules as R2                                            # noqa: E402

SEED = 20260921
OUT = ROOT / "research_outputs" / "tierc10" / "data"
RANGE_PINS_SOURCE = ROOT / "engine" / "rangefinder.py"


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


def literal_path(path: Path, table: str, *keys: str):
    """ONE nested value out of a CLOSED REGISTER in another module's SOURCE,
    without importing that module.  pin_literal's sibling: it literal_evals
    only the requested SUBTREE, so a register whose OTHER rows hold expressions
    (oracle_daily's REGISTER does) is still readable, and it accepts the
    annotated form `TABLE: dict = {...}` (ast.AnnAssign) as well as a plain
    assignment.  Used to read the estate's universes — the TC-series scored
    UNIVERSE, the Oracle's display ROSTER, the frozen study basket — for the
    data-spend audit, which must NOT drag those modules into this one's import
    closure (F-D-CLOSURE).

    HALTS IF: the table is absent, a key is absent, or the subtree is not a
    literal.
    """
    src = path.read_text(encoding="utf-8")
    node = None
    for n in ast.walk(ast.parse(src)):
        tg = (n.targets if isinstance(n, ast.Assign) else
              [n.target] if isinstance(n, ast.AnnAssign) else [])
        if any(isinstance(t, ast.Name) and t.id == table for t in tg):
            node = n.value
            break
    if node is None:
        raise SystemExit(f"HALT: no table {table} in {path}")
    for k in keys:
        hit = None
        if isinstance(node, ast.Dict):
            for kk, vv in zip(node.keys, node.values):
                if isinstance(kk, ast.Constant) and kk.value == k:
                    hit = vv
        if hit is None:
            raise SystemExit(f"HALT: {path.name}:{table}[{k!r}] not found")
        node = hit
    try:
        return ast.literal_eval(node)
    except ValueError as e:
        raise SystemExit(f"HALT: {path.name}:{table}{list(keys)} is not a literal ({e!r})")


MS_1H = 3_600_000
MS_4H = 4 * MS_1H
DAY_MS = 86_400_000
WEEK_MS = 7 * DAY_MS
MONDAY_EPOCH_OFFSET_MS = 4 * DAY_MS          # 1970-01-05 was a Monday

KLINE_COLS = list(ED.KLINE_COLS)
FUNDING_COLS = list(ED.FUNDING_COLS)
NATIVE_IVS = ("5m", "1h", "4h", "12h")       # fetched, venue-native
DERIVED_IVS = ("1d", "1w")                   # derived from native 4h [LEAN L1]
STEP_MS = {**{iv: INTERVAL_MS[iv] for iv in NATIVE_IVS},
           "1d": DAY_MS, "1w": WEEK_MS}
GRID_ANCHOR_MS = {"1w": MONDAY_EPOCH_OFFSET_MS}     # every other lens: 0

FUNDING_JITTER_MS = 60_000                   # study/census.py FUNDING_JITTER_MAX_MS
MEM_TTL_BARS = int(pin_literal(RANGE_PINS_SOURCE, "PINS_V2", "MEM_TTL_BARS"))
ADMISSION_MIN_4H = int(R2.TIDE_SLOW) + MEM_TTL_BARS                       # 316 + 400

# ── the charter's tiered cost model, as a HAIRCUT TWIN [VETO "tiers"] ─────
# The TC-series toll (FEE_BPS_ROUND_TRIP, the ['accounting'] figure) is NEVER
# replaced; the twin is an ADDED column.  The tier table is not TYPED here: it
# is PARSED out of the contract's own clause below, so editing a number in the
# table without editing the contract sentence is impossible (F-D-HAIRCUT).
CONTRACT_SLIPPAGE_CLAUSE = (
    "every row gets the charter model as a HAIRCUT TWIN beside the TC-series toll — "
    "slippage/side tier A {BTC ETH} 2 bps · tier B {SOL NEAR ZEC LTC BNB DOGE UNI SUI XMR} 5 · "
    "tier C {ENA PUMPFUN HYPE MNT PEPE BONK} 10")
CHARTER_SOURCE = ROOT / "Naiad_Phase0_Charter.md"
CHARTER_SLIPPAGE_NEEDLE = "**Slippage** per side"
_TIER_RX = re.compile(r"tier ([A-Z]) \{([^}]*)\} (\d+)")


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

# ── contract multipliers ─────────────────────────────────────────────────
CONTRACT_SPECS = "CONTRACT_SPECS.json"
DATA_SPEND = "DATA_SPEND_AUDIT.json"
_MULT_PREFIX = re.compile(r"^(\d+)(?=[A-Z])")

# ── the two-token trap ───────────────────────────────────────────────────
# |ln(open_after / close_before)| across the listing floor.  There is no
# identity available for a price seam, so the limit is a LEAN [D-i]: it is set
# from the WHOLE-TAPE seam census printed in the manifest (largest real 4h seam
# over the panel: ETHUSDT 2019-11-27T08:00Z, |ln| 0.1551 of 179,996 seams) and
# sits an order of magnitude BELOW the ~6.9 a 1000x token swap would show.
SPLICE_JUMP_LIMIT_LN = 1.0

# ── panels [LEAN L6] ──────────────────────────────────────────────────────
CLASSIC5 = tuple(R2.UNIVERSE)
# (contract name, Binance symbol lean, Binance baseAsset the probe must show)
UNSEEN12 = (
    ("ENA", "ENAUSDT", "ENA"), ("PUMPFUN", "PUMPUSDT", "PUMP"),
    ("HYPE", "HYPEUSDT", "HYPE"), ("MNT", "MNTUSDT", "MNT"),
    ("SUI", "SUIUSDT", "SUI"), ("LTC", "LTCUSDT", "LTC"),
    ("XMR", "XMRUSDT", "XMR"), ("BNB", "BNBUSDT", "BNB"),
    ("UNI", "UNIUSDT", "UNI"), ("PEPE", "1000PEPEUSDT", "1000PEPE"),
    ("DOGE", "DOGEUSDT", "DOGE"), ("BONK", "1000BONKUSDT", "1000BONK"),
)
ALT_VENUE_ASSETS = ("MNT",)                  # the only asset allowed an alternate
BYBIT_STEM_SUFFIX = "_BYBIT"                 # MNTUSDT_BYBIT_<iv>.parquet — the venue is IN the stem

BYBIT_BASE = "https://api.bybit.com"
BYBIT_IV = {"5m": "5", "1h": "60", "4h": "240", "12h": "720"}
BYBIT_PAGE = 1000
BYBIT_FUNDING_PAGE = 200

CHUNK_BARS = 15_000                          # 10 REST pages per save (resumable)
WEIGHT_SOFT_CAP = 1200                       # of Binance's 2400 / minute
RETRIES = 6

LEANS = (
    "[LEAN-HEPHAESTUS] L1 1d = exactly SIX complete native-4h bars per UTC day "
    "(the twin's law); 1w = seven such complete days, MONDAY-anchored UTC, "
    "complete weeks only. Source = native 4h, never 1h/5m aggregates.",
    "[LEAN-HEPHAESTUS] L5 All TC10 fetching lands in the snapshot only; "
    "promotion to the live cache and the LaCie mirror happen at CLOSE (the "
    "mirror command pushes — map_critic §4.2).",
    "[LEAN-HEPHAESTUS] L6 Panels: CLASSIC5 = BTC ETH SOL NEAR ZEC; UNSEEN12 = "
    "the contract's twelve; PANEL17 = CLASSIC5 + admitted UNSEEN12.",
    "[LEAN-HEPHAESTUS] D-a AS_OF is read off the VENUE clock at the first "
    "run's start and persisted; a resumed run never re-pins.",
    "[LEAN-HEPHAESTUS] D-b funding is kept through AS_OF close + 60 s: the "
    "print stamped a few ms past the AS_OF bar's close is a fact of that "
    "instant, and the venue's stamps jitter (study/census FUNDING_JITTER_MAX_MS).",
    "[LEAN-HEPHAESTUS] D-c MNT has no Binance USDT-M contract: its ENTIRE "
    "tape (klines and funding) is Bybit v5 linear, file stem MNTUSDT_BYBIT — "
    "one venue, never spliced; the fee figure stays the estate's flat "
    "assumption and says so.",
    "[LEAN-HEPHAESTUS] D-d PUMPFUN = PUMPUSDT only because the probe shows "
    "baseAsset PUMP as a TRADING perpetual; PUMPBTCUSDT (baseAsset PUMPBTC) "
    "is a different asset and is rejected by name.",
    "[LEAN-HEPHAESTUS] D-e bars already in the snapshot PAST the AS_OF close "
    "(the 5m files' 16:00-16:25Z rows) are NOT removed — there is no deletion "
    "primitive and a prefix is never rewritten; they are counted per file as "
    "rows_after_as_of and load_asof() cuts them.",
    "[LEAN-HEPHAESTUS] D-f the venue's BULK ARCHIVE and its REST API disagree on a "
    "handful of incident bars, and the PANEL IS PUBLICATION-HETEROGENEOUS there: "
    "WHICH of the two a pre-existing file carries is MEASURED per (file, lens) by "
    "two whole-history censuses (REST_VS_SNAPSHOT_AUDIT.json, "
    "ARCHIVE_VS_SNAPSHOT_AUDIT.json) and printed in the manifest — never "
    "assumed from how the file was assembled (the first filing assumed "
    "'pre-existing = archive'; the review measured REST for the classics). What "
    "TC10 itself fetched is REST. NOTHING is rewritten to reconcile them. F-D-1 "
    "stays contract-literal (vs the REST API) and therefore FAILS on a file that "
    "carries the archive's bar; F-D-1b proves every sampled bar field-equal to "
    "at least one of the venue's own two publications. Which publication is "
    "the record is the operator's ruling, not the builder's.",
    "[LEAN-HEPHAESTUS] D-g THE FUNDING HOUR: a print belongs to the hour its stamp "
    "FLOORS to (funding_hour_ms = funding_time // 1h * 1h — the estate's own "
    "tierc2_baseline.load_funding key). Measured on all 17 files: every stamp "
    "sits 0..47 ms PAST its hour, never before it, so floor == nearest and no "
    "print changes hour. load_funding_asof() returns funding_hour_ms beside the "
    "raw stamp and cuts on it (funding_hour_ms <= AS_OF close); an INTERVAL-SUM "
    "funding law (entry_ms < t <= exit_ms) must sum on funding_hour_ms, not on "
    "the raw stamp — on raw stamps EVERY boundary print of a Binance tape falls "
    "on the wrong side of a bar close by a few ms. The one print per Binance "
    "file stamped 2 ms after the AS_OF close is the AS_OF hour's print.",
    "[LEAN-HEPHAESTUS] D-h WRITE-ONCE, DISCLOSED: AS_OF_PIN.json is as first "
    "written. PRE_STATE.json and VENUE_PROBE.json were taken before the first "
    "fetch and RE-STAMPED once, 12 minutes after the last fetch row, to add the "
    "as_of_last_closed_4h / as_of_last_closed_4h_open / warranty keys; their "
    "record content (every file sha, row count and edge; the probe response) "
    "was not altered — F-D-PREFIX re-proves the file rows from the snapshot. "
    "From the repair on, write-once is CODE: _dump_once refuses to overwrite, "
    "probe_venues re-reads like the pin, and WRITE_ONCE_SEAL.json pins the "
    "three files' shas and the fetch log's line prefix (F-D-SEAL).",
    "[LEAN-HEPHAESTUS] D-i THE SPLICE LIMIT. Price continuity across the listing "
    "floor has no IDENTITY to check against, so the limit is a lean: a seam is a "
    f"SPLICE if |ln(open_after / close_before)| > {SPLICE_JUMP_LIMIT_LN}. Chosen from "
    "the WHOLE-TAPE seam census filed in the manifest (every adjacent 4h seam of every "
    "panel asset, 179,996 of them; largest real seam ETHUSDT 2019-11-27T08:00Z at "
    "0.1551 — the bar after its own listing bar), and an order of magnitude below the "
    "~6.9 a 1000x token swap prints. On the FILED panel the limit binds on NOTHING: no "
    "asset's tape holds a bar before its floor, so no floor seam exists. That arm of "
    "F-D-4 is therefore proven by its BREAK leg alone and says so; the arm that rides "
    "real values is the floor-bar IDENTITY (below).",
    "[LEAN-HEPHAESTUS] D-j THE FLOOR BAR IS RECONSTRUCTED, NOT ASSUMED. A grid bar that "
    "CONTAINS the listing instant opens before it (BTCUSDT's first 4h bar opens 17:55 -> "
    "16:00). That is the venue's grid, not prior-asset history — and it is PROVEN so, "
    "per asset, by rebuilding the floor bar from its OWN native 5m children at or after "
    "the listing instant: open == the first child's open, high == max, low == min, close "
    "== the last child's close, volume == the sum. A bar carrying one trade of a previous "
    "token could not survive that rebuild. Where the venue serves no bar AT the floor "
    "(SUIUSDT, 1000PEPEUSDT: the tape begins hours after the listing instant), the "
    "subject is the tape's FIRST bar instead, and that is printed.",
    "[LEAN-HEPHAESTUS] D-k DATA-SPEND CLASSES ARE READ FROM CLOSED REGISTERS, not from "
    "prose. scored = the stem is in the TC-series scored universe (scripts/tierc2_rules.py "
    "REGISTER['UNIVERSE']); display-only = not scored AND in the Oracle's display ROSTER "
    "(scripts/oracle_daily.py REGISTER['ROSTER']) or the frozen study basket "
    "(engine/cells.py SYMBOLS); never-touched = neither, and no grep of the contract's "
    "corpus places it in a scored book. All three registers are READ as literals "
    "(literal_path) — importing them would drag analytics / the range machine into this "
    "module's closure (F-D-CLOSURE). The grep corpus is NAMED whole in the artifact and "
    "EXCLUDES _reviewer_box/, docs/history/ and research_outputs/tierc10*/ (this build's "
    "own outputs — a self-reference would make the audit unreproducible).",
    "[LEAN-HEPHAESTUS] D-l THE MULTIPLIER IS IN THE NAME. MEASURED at the venue: Binance "
    "USDT-M exchangeInfo publishes NO contractSize / contract_size / quantity_multiplier "
    "field for a linear perpetual, and neither does Bybit v5 instruments-info for a "
    "LinearPerpetual (contractSize there is an INVERSE-contract field). The only place "
    "the venue states the multiplier is the baseAsset NAME: baseAsset '1000PEPE' means "
    "one contract unit is 1000 PEPE, so every quoted price is PER 1000 TOKENS. The "
    "multiplier is therefore READ off the captured baseAsset's leading integer (1 when "
    "there is none), the ABSENCE of the fields is filed as a measured fact, and "
    "CONTRACT_SPECS.json carries the venue's whole symbol object so the reading can be "
    "re-checked without a second network reach.",
)

# The four RESUME-contract artifacts of Stage D that R0 proved ABSENT were built
# on 2026-09-22 (this file's second pass).  What the reader must not mistake for
# tampering is recorded here, in the artifact, once.
STANDING_DISCLOSURES = (
    "F-D-1b's VENUE CENSUS DRIFTS OVERNIGHT, BY DESIGN OF THE VENUE, NOT BY OURS. The "
    "bulk archive BACKFILLS: a stamp the archive did not publish when the census ran is "
    "published later, and a bar that was 'rest' (equal to REST, no archive twin to "
    "compare) becomes 'both' (equal to REST and to the archive). R0 re-ran F-D-1b on "
    "2026-09-22 and measured the kinds move from {both: 215, rest: 28} to {both: 223, "
    "rest: 20} — 8 bars migrated, none changed value, none became 'neither'. NO CACHED "
    "BAR MOVED: a prefix is never rewritten and F-D-PREFIX re-proves it every run. A "
    "future run seeing different both/rest counts is seeing the archive catch up, NOT "
    "tampering; what would be a finding is a bar equal to NEITHER publication, or any "
    "movement in 'neither' / 'REST-sourced rows differing from REST'.",
    "F-D-1 IS DESIGNED RED and stays RED until the operator rules. It is kept "
    "contract-literal ('vs the venue API ... FAILS IF any OHLCV field differs') while the "
    "venue's REST API and its BULK ARCHIVE disagree on incident bars and operator ruling "
    "R5 ('The USDT pair, either on Binance or Bybit') does not distinguish the two "
    "publications. Re-cutting the claim after the result to make it green would be a "
    "check whose claim is not the design's claim. F-D-1b carries the attribution.",
    f"{CONTRACT_SPECS} IS WRITE-ONCE IN CODE (_dump_once) BUT IS NOT IN THE FILED SEAL. "
    "WRITE_ONCE_SEAL.json is itself write-once and was filed before this capture existed, "
    "so it cannot name it. The capture's own bytes are pinned instead by the manifest's "
    "contract_multipliers.artifact_sha256, which F-D-MULT re-hashes.",
)

LOG_LINES: list[str] = []


def log(msg: str = "") -> None:
    print(msg, flush=True)
    LOG_LINES.append(msg)


def iso(ms: int | float | None) -> str | None:
    if ms is None:
        return None
    return (datetime.fromtimestamp(int(ms) / 1000, tz=timezone.utc)
            .strftime("%Y-%m-%dT%H:%M:%SZ"))


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


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


def _dump(obj, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(obj, indent=2, sort_keys=True, default=str) + "\n",
                   encoding="utf-8")
    os.replace(tmp, path)


def _dump_once(obj, path: Path) -> None:
    """WRITE-ONCE, in code: a provenance record that exists is never written
    again.  HALTS IF the file is already there."""
    if path.exists():
        raise SystemExit(f"HALT: {path.name} is WRITE-ONCE and already exists — "
                         f"refusing to overwrite {path}")
    _dump(obj, path)


def kline_path(stem: str, iv: str, root: Path | None = None) -> Path:
    return (root or SNAPSHOT) / "klines" / f"{stem}_{iv}.parquet"


def funding_path(stem: str, root: Path | None = None) -> Path:
    return (root or SNAPSHOT) / "funding" / f"{stem}.parquet"


def target_last_open(iv: str, as_of_close_ms: int) -> int:
    """Open of the last bar of lens `iv` that is CLOSED at the AS_OF close."""
    step, anchor = STEP_MS[iv], GRID_ANCHOR_MS.get(iv, 0)
    return ((as_of_close_ms - step - anchor) // step) * step + anchor


# ═══════════════════════════════════════════════ 1 · THE AS-OF PIN
def pin_as_of(out: Path) -> dict:
    """Write-once.  The pin is a BAR, read off the venue clock, and proven
    closed by the venue's own closeTime for that bar.

    HALTS IF: the venue does not serve the pinned bar, or serves it with a
    closeTime at or after its own clock (the bar is still forming).
    """
    p = out / "AS_OF_PIN.json"
    if p.exists():
        pin = json.loads(p.read_text())
        log(f"AS_OF (re-read, pinned {pin['pinned_wall_clock_utc']}): open "
            f"{pin['as_of_last_closed_4h_open']} close {pin['as_of_last_closed_4h']}")
        return pin
    server_ms = int(ED._get(ED.REST_BASE + "/fapi/v1/time").json()["serverTime"])
    local_ms = int(time.time() * 1000)
    open_ms = (server_ms // MS_4H) * MS_4H - MS_4H
    rows = ED._get(ED.REST_BASE + "/fapi/v1/klines",
                   params={"symbol": "BTCUSDT", "interval": "4h",
                           "startTime": open_ms, "endTime": open_ms,
                           "limit": 1}).json()
    if not rows or int(rows[0][0]) != open_ms:
        raise SystemExit(f"HALT: venue does not serve BTCUSDT 4h open {iso(open_ms)}")
    venue_close_ms = int(rows[0][6])
    if venue_close_ms >= server_ms:
        raise SystemExit(f"HALT: pinned bar {iso(open_ms)} is still forming on the "
                         f"venue (closeTime {venue_close_ms} >= serverTime {server_ms})")
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
        "law": "AS_OF = last CLOSED 4h bar at the first run's start, by the "
               "venue clock; write-once; every fetch stops at bars closed by "
               "as_of_last_closed_4h",
        "seed": SEED,
    }
    _dump_once(pin, p)
    log(f"AS_OF PINNED: open {pin['as_of_last_closed_4h_open']} close "
        f"{pin['as_of_last_closed_4h']} (venue clock {pin['venue_server_time']}, "
        f"venue closeTime of the bar {venue_close_ms} < serverTime: CLOSED)")
    return pin


def load_pin(out: Path | None = None) -> dict:
    p = (out or OUT) / "AS_OF_PIN.json"
    if not p.exists():
        raise SystemExit(f"HALT: no AS_OF pin at {p} — run scripts/tierc10_data.py first")
    return json.loads(p.read_text())


# ═══════════════════════════════════════════════ 2 · VENUE OF RECORD
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


def probe_venues(out: Path, pin: dict) -> dict:
    """Probe Binance USDT-M exchangeInfo for the twelve; Bybit only for an
    asset Binance does not list at all.  KEEP rule (the roster probe's):
    present AND contractType == PERPETUAL AND status == TRADING AND
    quoteAsset == USDT AND baseAsset == the expected base.

    WRITE-ONCE like the pin: a resumed run RE-READS the probe — the venue of
    record of a tape is decided once, before its first bar is fetched."""
    p = out / "VENUE_PROBE.json"
    if p.exists():
        probe = json.loads(p.read_text())
        log(f"VENUE PROBE (re-read, probed {probe['probed_wall_clock_utc']})")
        return probe
    r = ED._get(ED.REST_BASE + "/fapi/v1/exchangeInfo")
    info = r.json()
    by_sym = {s["symbol"]: s for s in info["symbols"]}
    assets, rejections = [], []
    for name, sym, base in UNSEEN12:
        s = by_sym.get(sym)
        rec = {"asset": name, "binance_symbol_lean": sym, "expected_base": base}
        keep = bool(s and s["contractType"] == "PERPETUAL" and s["status"] == "TRADING"
                    and s["quoteAsset"] == "USDT" and s["baseAsset"] == base)
        if s:
            rec["binance"] = {k: s[k] for k in ("symbol", "baseAsset", "quoteAsset",
                                                "contractType", "status", "onboardDate")}
            rec["binance"]["onboardDate_iso"] = iso(s["onboardDate"])
        else:
            rec["binance"] = None
        # near-matches that must be REJECTED by name, not silently skipped
        for cand in sorted(by_sym):
            c = by_sym[cand]
            if (cand != sym and cand.startswith(base) and c["quoteAsset"] == "USDT"
                    and c["baseAsset"] != base and name == "PUMPFUN"):
                rejections.append({"asset": name, "rejected_symbol": cand,
                                   "baseAsset": c["baseAsset"],
                                   "reason": f"baseAsset {c['baseAsset']} != {base}: a different asset"})
        if keep:
            rec.update(venue="BINANCE_USDTM", symbol=sym, stem=sym,
                       status=s["status"], contract_type=s["contractType"],
                       listing_ms=int(s["onboardDate"]), listing=iso(s["onboardDate"]),
                       venue_reason="Binance USDT-M perpetual, TRADING (default venue)")
        elif name in ALT_VENUE_ASSETS and s is None:
            inst = _bybit_get("/v5/market/instruments-info",
                              {"category": "linear", "symbol": sym})["list"]
            b = inst[0] if inst else None
            rec["bybit"] = ({k: b.get(k) for k in ("symbol", "contractType", "status",
                                                   "baseCoin", "quoteCoin", "launchTime",
                                                   "fundingInterval")} if b else None)
            if (b and b["contractType"] == "LinearPerpetual" and b["status"] == "Trading"
                    and b["baseCoin"] == base and b["quoteCoin"] == "USDT"):
                rec.update(venue="BYBIT_V5_LINEAR", symbol=sym,
                           stem=sym + BYBIT_STEM_SUFFIX, status=b["status"],
                           contract_type=b["contractType"],
                           listing_ms=int(b["launchTime"]), listing=iso(int(b["launchTime"])),
                           venue_reason="ABSENT from Binance USDT-M exchangeInfo; the ENTIRE "
                                        "tape is Bybit v5 linear — one venue, never spliced")
            else:
                rec.update(venue=None, symbol=None, stem=None,
                           venue_reason="absent from Binance AND no TRADING Bybit linear perpetual")
        else:
            why = ("absent from Binance USDT-M exchangeInfo" if s is None else
                   f"present but not KEEP (contractType {s['contractType']}, status "
                   f"{s['status']}, baseAsset {s['baseAsset']})")
            rec.update(venue=None, symbol=None, stem=None, venue_reason=why)
        assets.append(rec)
    classics = []
    for sym in CLASSIC5:
        s = by_sym.get(sym)
        if not s:
            raise SystemExit(f"HALT: classic {sym} absent from exchangeInfo")
        classics.append({"asset": sym.replace("USDT", ""), "venue": "BINANCE_USDTM",
                         "symbol": sym, "stem": sym, "status": s["status"],
                         "contract_type": s["contractType"],
                         "listing_ms": int(s["onboardDate"]), "listing": iso(s["onboardDate"]),
                         "venue_reason": "Binance USDT-M perpetual (the estate's venue of record)"})
    probe = {
        "as_of_last_closed_4h": pin["as_of_last_closed_4h"],
        "as_of_last_closed_4h_open": pin["as_of_last_closed_4h_open"],
        "warranty": WARRANTY,
        "endpoint": ED.REST_BASE + "/fapi/v1/exchangeInfo",
        "response_sha256": hashlib.sha256(r.content).hexdigest(),
        "symbols_in_response": len(info["symbols"]),
        "probed_wall_clock_utc": iso(time.time() * 1000),
        "keep_rule": "present AND contractType==PERPETUAL AND status==TRADING AND "
                     "quoteAsset==USDT AND baseAsset==expected",
        "unseen12": assets, "classic5": classics, "rejections": rejections,
    }
    _dump_once(probe, p)
    return probe


def print_venues(probe: dict) -> None:
    log("\nVENUE OF RECORD — per asset (probe of "
        f"{probe['endpoint']}, {probe['symbols_in_response']} symbols)")
    log(f"  {'asset':8s} {'venue':16s} {'symbol':14s} {'stem':16s} {'status':8s} listing")
    for a in probe["classic5"] + probe["unseen12"]:
        log(f"  {a['asset']:8s} {str(a['venue']):16s} {str(a['symbol']):14s} "
            f"{str(a['stem']):16s} {str(a.get('status')):8s} {a.get('listing')}"
            f"   [{a['venue_reason']}]")
    for rj in probe["rejections"]:
        log(f"  REJECTED {rj['asset']}: {rj['rejected_symbol']} — {rj['reason']}")
    x = next(a for a in probe["unseen12"] if a["asset"] == "XMR")
    log(f"  XMR LIVE STATUS: {x.get('binance')} — the contract's 'post-delisting' "
        f"premise is {'STALE (still TRADING on Binance; no alternate venue, no splice question)' if x['venue'] == 'BINANCE_USDTM' else 'LIVE'}")


# ═══════════════════════════════════════════════ 3 · FETCH (snapshot only)
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


def _fetch_log(out: Path, row: dict) -> None:
    row = {"wall_clock_utc": iso(time.time() * 1000), **row}
    with open(out / "FETCH_LOG.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(row, sort_keys=True) + "\n")


def _edge(path: Path, col: str) -> int | None:
    if not path.exists():
        return None
    t = pd.read_parquet(path, columns=[col])[col]
    return int(t.max()) if len(t) else None


def _assert_grid(df: pd.DataFrame, iv: str, what: str) -> None:
    off = (df["open_time"].to_numpy(np.int64) - GRID_ANCHOR_MS.get(iv, 0)) % STEP_MS[iv]
    if len(df) and (off != 0).any():
        raise SystemExit(f"HALT: {what}: venue served {int((off != 0).sum())} off-grid "
                         f"open_time(s) — refusing to save")


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


def extend_klines(a: dict, iv: str, pin: dict, out: Path) -> dict:
    """Extend ONE (asset, lens) forward to the AS_OF, chunk by chunk, each
    chunk saved through engine.data._save_cache (no-shrink + atomic) before
    the next is asked for — an interrupted run resumes from the file's edge."""
    stem, sym, venue = a["stem"], a["symbol"], a["venue"]
    step = STEP_MS[iv]
    tgt = target_last_open(iv, pin["as_of_last_closed_4h_close_ms"])
    path = kline_path(stem, iv)
    edge = _edge(path, "open_time")
    if edge is None:
        if venue == "BINANCE_USDTM":
            first = _retry(lambda: ED.detect_first_candle(sym, iv), f"{sym} {iv} first candle")
            if first is None:
                raise RuntimeError(f"{sym} {iv}: venue reports no klines")
        else:
            first = (int(a["listing_ms"]) // step) * step
        cursor = int(first)
    else:
        cursor = edge + step
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


def extend_funding(a: dict, pin: dict, first_kline_ms: int, out: Path) -> dict:
    stem, sym, venue = a["stem"], a["symbol"], a["venue"]
    end_ms = pin["as_of_last_closed_4h_close_ms"] + FUNDING_JITTER_MS
    start_ms = int(first_kline_ms) - DAY_MS
    old = _edge(funding_path(stem), "funding_time")
    if venue == "BINANCE_USDTM":
        _retry(lambda: ED.backfill_funding(sym, start_ms, end_ms, log=None),
               f"{sym} funding")
    else:
        lo = start_ms if old is None else old + 1
        df = _retry(lambda: bybit_funding(sym, lo, end_ms), f"{sym} bybit funding")
        if len(df):
            ED._save_funding(stem, df[FUNDING_COLS])
    new = _edge(funding_path(stem), "funding_time")
    _fetch_log(out, {"kind": "funding", "stem": stem, "venue": venue,
                     "old_edge": iso(old), "new_edge": iso(new)})
    log(f"    {stem} funding: edge {iso(old)} -> {iso(new)}")
    return {"stem": stem, "old_edge": old, "edge": new}


def write_pre_state(assets: list[dict], pin: dict, out: Path) -> dict:
    """WRITE-ONCE ledger of every in-scope file that existed BEFORE TC10
    fetched anything: file sha, rows, edges, content sha.  The no-rewrite
    proof reads the old prefix back out of the CURRENT file and re-hashes.
    (The FILED record was re-stamped once after the fetch — LEAN D-h; from
    the repair on _dump_once makes a second write a HALT.)"""
    p = out / "PRE_STATE.json"
    if p.exists():
        return json.loads(p.read_text())
    files = {}
    for a in assets:
        if not a.get("stem"):
            continue
        for iv in NATIVE_IVS:
            q = kline_path(a["stem"], iv)
            if q.exists():
                d = pd.read_parquet(q)
                files[f"klines/{q.name}"] = {
                    "file_sha256": file_sha256(q), "rows": int(len(d)),
                    "first_ms": int(d["open_time"].min()), "last_ms": int(d["open_time"].max()),
                    "content_sha": frame_sha(d.sort_values("open_time"), KLINE_COLS)}
        q = funding_path(a["stem"])
        if q.exists():
            d = pd.read_parquet(q)
            files[f"funding/{q.name}"] = {
                "file_sha256": file_sha256(q), "rows": int(len(d)),
                "first_ms": int(d["funding_time"].min()), "last_ms": int(d["funding_time"].max()),
                "content_sha": frame_sha(d.sort_values("funding_time"), FUNDING_COLS)}
    pre = {"as_of_last_closed_4h": pin["as_of_last_closed_4h"],
           "as_of_last_closed_4h_open": pin["as_of_last_closed_4h_open"],
           "warranty": WARRANTY,
           "law": "write-once; taken before the first TC10 fetch; an old prefix "
                  "may be EXTENDED, never rewritten", "files": files}
    _dump_once(pre, p)
    log(f"PRE_STATE filed: {len(files)} pre-existing in-scope files")
    return pre


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


# ═══════════════════════════════════════════════ 3b · THE WRITE-ONCE SEAL [LEAN D-h]
SEAL = "WRITE_ONCE_SEAL.json"
SEALED_FILES = ("AS_OF_PIN.json", "VENUE_PROBE.json", "PRE_STATE.json")
FETCH_LOG = "FETCH_LOG.jsonl"


def _lines_sha(lines: list[str]) -> str:
    return hashlib.sha256(("\n".join(lines) + "\n").encode("utf-8")).hexdigest()


def seal_provenance(out: Path) -> dict:
    """Pin the provenance records' bytes — ONCE.  A seal cannot prove what
    happened before it (the disclosure says what did: two of the three were
    re-stamped after the fetch); it makes every LATER write detectable, which
    is the part of "write-once" code can carry.  The fetch log is append-only,
    so its sealed LINE PREFIX is pinned, not the file."""
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
            disclosure.append(
                f"{n}: last written {written}, AFTER the last fetch row {last_fetch} — taken before "
                f"the first fetch, RE-STAMPED once afterwards with the as_of_last_closed_4h / "
                f"as_of_last_closed_4h_open / warranty keys; record content not altered [LEAN D-h]")
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


# ═══════════════════════════════════════════════ 4 · DERIVED LENSES [LEAN L1]
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


def _write_if_changed(df: pd.DataFrame, path: Path) -> str:
    if path.exists() and frame_sha(pd.read_parquet(path), KLINE_COLS) == frame_sha(df, KLINE_COLS):
        return "unchanged"
    tmp = path.with_name(f"{path.name}.{os.getpid()}.tmp")
    df.to_parquet(tmp, index=False)
    os.replace(tmp, path)
    return "written"


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


# ═══════════════════════════════════════════════ 6 · SCANS — count, never fill
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


# ═══════════════════════════════════════════════ 7 · FEE SCHEDULE
def _source_line(path: Path, needle: str) -> int | None:
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if needle in line:
            return i
    return None


def fee_schedule(assets: list[dict], funding: dict, pin: dict) -> dict:
    """The estate has NO per-asset venue fee source (the account-rate endpoint
    is signed; the repo holds no key).  What every Tier-C card charges is one
    flat taker figure — filed here per asset, marked ASSUMPTION, with the line
    it is read from.  The value is READ from tierc2_rules, never typed."""
    rules, cfg = ROOT / "scripts" / "tierc2_rules.py", ROOT / "configs" / "naiad_v0.yaml"
    src = [f"scripts/tierc2_rules.py:{_source_line(rules, 'FEE_BPS_SIDE: float')}",
           f"scripts/tierc2_rules.py:{_source_line(rules, 'FEE_BPS_ROUND_TRIP: float')}",
           f"configs/naiad_v0.yaml:{_source_line(cfg, 'fee_bps_side')}"]
    rows = []
    for a in assets:
        fu = funding.get(a["stem"], {})
        rows.append({
            "asset": a["asset"], "venue": a["venue"], "symbol": a["symbol"], "stem": a["stem"],
            "taker_bps_side_used": float(R2.FEE_BPS_SIDE),
            "round_trip_bps_used": float(R2.FEE_BPS_ROUND_TRIP),
            "kind": "ASSUMPTION — the estate's flat FEE_BPS_SIDE object, NOT a venue schedule",
            "source": src,
            # ── the HAIRCUT TWIN [VETO "tiers"]: ADDED keys, beside
            # round_trip_bps_used, which is NEVER replaced or recomputed here.
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
                           if a["venue"] == "BYBIT_V5_LINEAR" else
                           "Binance USDT-M per-account commissionRate is a signed endpoint; "
                           "not fetched"),
            "funding_interval_hours_observed_tail": fu.get("interval_hours_observed_tail"),
            "funding_interval_hours_observed_modal": fu.get("interval_hours_observed_modal"),
            "funding_spacing_hours_histogram": fu.get("spacing_hours_histogram"),
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
            "assets": rows}


WARRANTY = ("these files are described AS OF the pinned last closed 4h bar named "
            "here and of no other; bars stamped after it are counted, never read "
            "[TC6V-a, carried by TIER-C10]")


# ═══════════════════════════════════════════════ 7b · CONTRACT MULTIPLIERS
MULTIPLIER_FIELDS = ("multiplier", "contractSize", "contract_size", "quantity_multiplier",
                     "contractMultiplier", "multiplierSize")


def base_multiplier(base_asset: str) -> int:
    """TOKENS per contract unit, READ off the venue's own baseAsset name
    [LEAN D-l]: '1000PEPE' -> 1000, 'BTC' -> 1.  Never typed per symbol."""
    m = _MULT_PREFIX.match(base_asset or "")
    return int(m.group(1)) if m else 1


def normalize_price(px, multiplier: int):
    """Venue price (per contract unit) -> price PER ONE TOKEN.  A PURE SCALING
    by the constant 1/multiplier."""
    return px / multiplier


def normalize_qty(q, multiplier: int):
    """Venue quantity (contract units) -> quantity in TOKENS.  The inverse
    scaling, so notional px*q is invariant."""
    return q * multiplier


NORMALIZATION_LAW = (
    "NORMALIZED PRICE = venue price / multiplier (USDT per ONE token); NORMALIZED "
    "QUANTITY = venue quantity x multiplier (tokens). For 1000PEPEUSDT and "
    "1000BONKUSDT the multiplier is 1000, i.e. EVERY PRICE THE VENUE QUOTES ON THOSE "
    "TWO TAPES IS PER 1000 TOKENS; for the other fifteen it is 1 and normalization is "
    "the identity. THE NORMALIZATION IS A PURE SCALING OF THE PRICE SERIES BY A "
    "CONSTANT, AND THEREFORE CANNOT MOVE ANY RATIO-VALUED STATISTIC: for a constant "
    "k > 0, R = (exit - entry) / (entry - stop) has k in numerator and denominator and "
    "is unchanged; an ATR-normalized height (high - low) / ATR is a price over a price "
    "and is unchanged; a log return ln(p_t / p_{t-1}) is unchanged; the notional "
    "price x quantity is unchanged because the quantity scales by 1/k. What DOES move "
    "is anything quoted in absolute price units — a tick size, a MIN_NOTIONAL, a "
    "per-unit fee in USDT — and those are filed per symbol here, unnormalized, as the "
    "venue states them. NAIAD DOES NOT REWRITE THE TAPE: the parquet holds the venue's "
    "own numbers; normalization is a READING, applied by whoever needs per-token units, "
    "and F-D-MULT proves on the real 1000PEPEUSDT and 1000BONKUSDT tapes that applying "
    "it leaves every ratio-valued statistic identical.")


def capture_contract_specs(out: Path, pin: dict) -> dict:
    """THE ONE VENUE REACH OF THIS PASS.  Binance USDT-M exchangeInfo (the whole
    symbol object, filters included) for every Binance-venue stem, Bybit v5
    instruments-info for the alternate-venue one.  Write-once like the pin and
    the probe: a contract spec is captured before it is quoted, and quoted from
    the file afterwards — no fixture and no re-description ever asks the venue
    again (F-DET would not survive it).

    The MEASURED absence of every multiplier field is part of the record
    [LEAN D-l]: R0 found zero occurrences of multiplier / contractSize /
    contract_size / quantity_multiplier in STAGE_D_MANIFEST.json and zero in
    VENUE_PROBE.json, and the venue is the reason — it publishes none.

    HALTS IF: the venue does not serve a stem's symbol at all.
    """
    p = out / CONTRACT_SPECS
    if p.exists():
        doc = json.loads(p.read_text())
        log(f"CONTRACT SPECS (re-read, captured {doc['captured_wall_clock_utc']})")
        return doc
    probe = json.loads((out / "VENUE_PROBE.json").read_text())
    assets = [a for a in probe["classic5"] + probe["unseen12"] if a.get("stem")]
    r = ED._get(ED.REST_BASE + "/fapi/v1/exchangeInfo")
    info = r.json()
    by_sym = {s["symbol"]: s for s in info["symbols"]}
    rows, absent = [], {}
    for a in assets:
        if a["venue"] == "BINANCE_USDTM":
            s = by_sym.get(a["symbol"])
            if s is None:
                raise SystemExit(f"HALT: {a['symbol']} absent from exchangeInfo at capture")
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
               "READ off baseAsset because the venue publishes no multiplier field [LEAN D-l]",
        "multiplier_fields_searched": list(MULTIPLIER_FIELDS),
        "multiplier_fields_found_per_symbol": absent,
        "normalization": NORMALIZATION_LAW,
        "assets": rows,
    }
    _dump_once(doc, p)
    _fetch_log(out, {"kind": "contract_specs", "stem": "ALL",
                     "venue": "BINANCE_USDTM+BYBIT_V5_LINEAR",
                     "symbols": len(rows),
                     "binance_response_sha256": doc["binance_response_sha256"]})
    log(f"CONTRACT SPECS captured for {len(rows)} symbols -> {p}")
    return doc


def load_contract_specs(out: Path | None = None) -> dict | None:
    p = (out or OUT) / CONTRACT_SPECS
    return json.loads(p.read_text()) if p.exists() else None


def multiplier_of(stem: str, out: Path | None = None) -> int:
    """TOKENS per contract unit for a file stem, from the CAPTURE — never
    re-derived from the stem's own spelling.  HALTS IF the capture is missing
    or does not name the stem."""
    doc = load_contract_specs(out)
    if doc is None:
        raise SystemExit(f"HALT: no {CONTRACT_SPECS} — run tierc10_data.py --contract-specs")
    for a in doc["assets"]:
        if a["stem"] == stem:
            return int(a["multiplier_tokens_per_contract_unit"])
    raise SystemExit(f"HALT: {CONTRACT_SPECS} names no stem {stem}")


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
        "artifact": f"research_outputs/tierc10/data/{CONTRACT_SPECS}",
        "artifact_sha256": file_sha256((out or OUT) / CONTRACT_SPECS),
        "capture_instant": ("NOT carried here, and not by name either: no run-time clock key "
                            "enters a deterministic artifact (F-DET scans these files for the "
                            f"key names themselves). The capture's own stamp lives in "
                            f"{CONTRACT_SPECS} — a PROVENANCE file, which holds clocks by design "
                            "and is never in the determinism set. This row pins that file's BYTES "
                            "by sha256 instead, and F-D-MULT re-hashes it every run."),
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


# ═══════════════════════════════════════════════ 7c · THE HAIRCUT TWIN [VETO "tiers"]
def tier_of(asset: str) -> str:
    """The charter tier of a CONTRACT asset name.  HALTS IF unassigned — an
    unassigned asset must stop the build, never default to the cheapest tier."""
    t = TIER_OF_ASSET.get(asset)
    if t is None:
        raise SystemExit(f"HALT: asset {asset!r} is in NO slippage tier of the contract clause "
                         f"({sorted(TIER_OF_ASSET)}) — the haircut twin refuses to guess")
    return t


def slippage_bps_side(asset: str) -> float:
    """Charter slippage, bps PER SIDE, for a contract asset name."""
    return float(SLIPPAGE_TIERS[tier_of(asset)]["bps"])


def charter_bps_side(asset: str) -> float:
    """The charter model's per-side rate: the estate's taker fee PLUS the
    charter slippage of the asset's tier.  Never a replacement for the
    TC-series toll — the caller keeps both."""
    return float(R2.FEE_BPS_SIDE) + slippage_bps_side(asset)


def charter_round_trip_bps(asset: str) -> float:
    return 2.0 * charter_bps_side(asset)


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


def haircut_twin_for_stem(stem: str, gross_r: float, entry_px: float, exit_px: float,
                          risk_px: float, out: Path | None = None) -> dict:
    """The same, addressed by file stem: the stem -> contract asset map is READ
    from the filed manifest's venue table, never typed."""
    by = {v["stem"]: v["asset"] for v in load_manifest(out)["venues"] if v["stem"]}
    if stem not in by:
        raise SystemExit(f"HALT: the manifest's venue table names no stem {stem}")
    return haircut_twin_net_r(by[stem], gross_r, entry_px, exit_px, risk_px)


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


# ═══════════════════════════════════════════════ 7d · THE TWO-TOKEN TRAP [F-D-4]
def floor_open(listing_ms: int, iv: str) -> int:
    """The HARD FLOOR of lens `iv`: the open of the grid bar that CONTAINS the
    listing instant.  A bar opening before this is prior-asset history."""
    step, anchor = STEP_MS[iv], GRID_ANCHOR_MS.get(iv, 0)
    return ((int(listing_ms) - anchor) // step) * step + anchor


def seam_jump(close_before: float, open_after: float) -> float:
    """|ln(open_after / close_before)| — the quantity a token splice shows up in."""
    if not (close_before > 0 and open_after > 0):
        return float("inf")
    return float(abs(np.log(float(open_after) / float(close_before))))


def _floor_bar_rebuild(stem: str, listing_ms: int, close_ms: int) -> dict:
    """[LEAN D-j] Rebuild the 4h floor bar (or, where the venue serves none at
    the floor, the tape's FIRST bar) out of its OWN native 5m children at or
    after the listing instant, and report every field's agreement."""
    fl = floor_open(listing_ms, "4h")
    f4 = load_asof(stem, "4h")
    at = f4[f4["open_time"] == fl]
    subject_kind = "the bar AT the listing floor"
    if not len(at):
        at = f4.iloc[[0]]
        subject_kind = ("the tape's FIRST bar — the venue serves NO bar at the floor "
                        "(the tape begins after the listing instant)")
    b = at.iloc[0]
    t0 = int(b["open_time"])
    m5 = load_asof(stem, "5m")
    kids = m5[(m5["open_time"] >= t0) & (m5["open_time"] < t0 + MS_4H)].sort_values("open_time")
    out = {"subject": subject_kind, "subject_open": iso(t0), "subject_open_ms": t0,
           "floor_open": iso(fl), "children_5m": int(len(kids))}
    if not len(kids):
        out.update(rebuilt=False, why="the 5m tape serves no child of this bar — NOT rebuilt",
                   fields_equal=None)
        return out
    re_ = {"open": float(kids["open"].iloc[0]), "high": float(kids["high"].max()),
           "low": float(kids["low"].min()), "close": float(kids["close"].iloc[-1]),
           "volume": float(kids["volume"].sum())}
    got = {k: float(b[k]) for k in KLINE_COLS[1:]}
    eq = {k: (got[k] == re_[k] if k != "volume"
              else bool(np.isclose(got[k], re_[k], rtol=1e-12, atol=0.0))) for k in re_}
    out.update(first_child_open=iso(int(kids["open_time"].iloc[0])),
               first_child_at_or_after_listing=bool(int(kids["open_time"].iloc[0]) >= floor_open(listing_ms, "5m")),
               bar=got, rebuilt_from_5m_children=re_, fields_equal=eq,
               rebuilt=bool(all(eq.values())))
    return out


def listing_audit(probe: dict, pin: dict) -> dict:
    """F-D-4's table.  Per symbol: the INTENDED asset, its listing instant and
    the SOURCE of that instant, the first bar in our tape, whether the tape
    predates the listing, whether it is HARD-FLOORED at the listing instant,
    and the price continuity AT the floor.

    Nothing here is sampled: every lens of every asset is counted, and the
    whole-tape 4h seam census is summarised per asset so the reader can see
    what a REAL seam is worth beside SPLICE_JUMP_LIMIT_LN [LEAN D-i].
    """
    close_ms = pin["as_of_last_closed_4h_close_ms"]
    by_stem = {a["stem"]: a for a in probe["classic5"] + probe["unseen12"] if a.get("stem")}
    expected = {name: base for name, _sym, base in UNSEEN12}
    # the venue's OWN baseAsset for all seventeen, from the contract-spec capture
    # (VENUE_PROBE keeps the raw symbol object only for the twelve) — so the
    # intended-asset check is real for the classics too, with no escape hatch.
    specs = load_contract_specs()
    specs_base = {a["stem"]: a["base_asset"] for a in (specs or {}).get("assets", [])}
    rows, cells, unfloored, discontinuous = [], 0, [], []
    for stem, a in by_stem.items():
        L = int(a["listing_ms"])
        src = ("Binance USDT-M exchangeInfo['symbols'][].onboardDate, captured in "
               "VENUE_PROBE.json (write-once)" if a["venue"] == "BINANCE_USDTM" else
               "Bybit v5 instruments-info['list'][].launchTime, captured in "
               "VENUE_PROBE.json (write-once)")
        lenses = {}
        for iv in NATIVE_IVS + DERIVED_IVS:
            fl = floor_open(L, iv)
            t = pd.read_parquet(kline_path(stem, iv), columns=["open_time"])["open_time"] \
                .to_numpy(np.int64)
            pre = int((t < fl).sum())
            cells += 1
            lenses[iv] = {"floor_open": iso(fl), "first_open": iso(int(t.min())),
                          "bars_before_the_floor": pre,
                          "hard_floored": bool(pre == 0),
                          "tape_begins_at_the_floor": bool(int(t.min()) == fl)}
            if pre:
                unfloored.append(f"{stem} {iv}: {pre} bar(s) before {iso(fl)}")
        f4 = load_asof(stem, "4h")
        o = f4["open"].to_numpy(np.float64)
        c = f4["close"].to_numpy(np.float64)
        j = np.abs(np.log(o[1:] / c[:-1]))
        k = int(np.argmax(j))
        fl4 = floor_open(L, "4h")
        before = f4[f4["open_time"] < fl4]
        after = f4[f4["open_time"] >= fl4]
        if len(before) and len(after):
            fs = seam_jump(float(before["close"].iloc[-1]), float(after["open"].iloc[0]))
            cont = {"floor_seam_exists": True, "floor_seam_abs_ln_jump": fs,
                    "limit": SPLICE_JUMP_LIMIT_LN, "continuous": bool(fs <= SPLICE_JUMP_LIMIT_LN)}
            if not cont["continuous"]:
                discontinuous.append(f"{stem}: |ln jump| {fs:.4f} at the floor {iso(fl4)}")
        else:
            cont = {"floor_seam_exists": False, "floor_seam_abs_ln_jump": None,
                    "limit": SPLICE_JUMP_LIMIT_LN, "continuous": None,
                    "why": "the tape holds NO bar before the floor — there is no floor seam to be "
                           "discontinuous, and no splice is possible [LEAN D-i]"}
        probe_base = specs_base.get(stem) or (a.get("binance") or {}).get("baseAsset") \
            or (a.get("bybit") or {}).get("baseCoin")
        rows.append({
            "asset": a["asset"], "stem": stem, "symbol": a["symbol"], "venue": a["venue"],
            "intended_asset": a["asset"],
            "intended_base_expected": expected.get(a["asset"], a["asset"]),
            "probe_base_asset": probe_base,
            "probe_base_asset_source": ("CONTRACT_SPECS.json (the venue's own symbol object)"
                                        if stem in specs_base else "VENUE_PROBE.json"),
            "intended_asset_confirmed": bool(probe_base == expected.get(a["asset"], a["asset"])),
            "listing": iso(L), "listing_ms": L, "listing_source": src,
            "first_bar_4h": iso(int(f4["open_time"].iloc[0])),
            "tape_predates_listing_instant_4h": bool(int(f4["open_time"].iloc[0]) < L),
            "tape_predates_the_hard_floor": bool(int(f4["open_time"].iloc[0]) < fl4),
            "hard_floored_every_lens": all(v["hard_floored"] for v in lenses.values()),
            "per_lens": lenses,
            "floor_bar": _floor_bar_rebuild(stem, L, close_ms),
            "continuity_at_the_floor": cont,
            "whole_tape_4h_seams": {
                "seams": int(len(j)), "max_abs_ln_jump": float(j.max()) if len(j) else None,
                "at": iso(int(f4["open_time"].iloc[k + 1])) if len(j) else None},
        })
    rej = probe.get("rejections", [])
    return {
        "law": "FAILS IF any symbol's history predates its intended listing unfloored. The floor "
               "of a lens is the open of the grid bar that CONTAINS the listing instant; a bar "
               "opening before it is prior-asset history and is a HALT-grade finding.",
        "listing_source": "the VENUE's own onboardDate / launchTime, captured write-once in "
                          "VENUE_PROBE.json before the first bar was fetched",
        "cells_checked": cells, "assets": len(rows), "lenses": list(NATIVE_IVS + DERIVED_IVS),
        "bars_before_a_floor": unfloored,
        "all_hard_floored": not unfloored,
        "discontinuous_floor_seams": discontinuous,
        "floor_bars_rebuilt_from_5m": sum(1 for r in rows if r["floor_bar"].get("rebuilt")),
        "intended_asset_confirmed": sum(1 for r in rows if r["intended_asset_confirmed"]),
        "intended_asset_unconfirmed": [f"{r['stem']}: venue baseAsset {r['probe_base_asset']!r} "
                                       f"!= intended {r['intended_base_expected']!r}"
                                       for r in rows if not r["intended_asset_confirmed"]],
        "floor_seams_that_exist": sum(1 for r in rows
                                      if r["continuity_at_the_floor"]["floor_seam_exists"]),
        "splice_jump_limit_ln": SPLICE_JUMP_LIMIT_LN,
        "whole_tape_4h_seams_total": sum(r["whole_tape_4h_seams"]["seams"] for r in rows),
        "whole_tape_4h_max_abs_ln_jump": max(
            (r["whole_tape_4h_seams"]["max_abs_ln_jump"] for r in rows), default=None),
        "lit_precedent": "engine/cells.py LIT_FLOOR_MS (2025-12-23T00:00Z) — LITUSDT carried "
                         "Litentry before the Lighter perpetual listing and the loader asserts a "
                         "hard floor for it. THE LIVE RISK ON THIS PANEL IS PUMPFUN: the venue "
                         "probe recorded a REJECTED PUMPBTCUSDT (baseAsset PUMPBTC != PUMP, 'a "
                         "different asset') and PUMPFUN is mapped to PUMPUSDT by [LEAN D-d]. The "
                         "rejection is carried here so the two tokens can never be confused.",
        "rejections_carried": rej,
        "rows": rows,
    }


# ═══════════════════════════════════════════════ 7e · DATA-SPEND AUDIT [F-D-5]
SPEND_TOKENS = {
    "BTC": ("BTCUSDT", "BTC"), "ETH": ("ETHUSDT", "ETH"), "SOL": ("SOLUSDT", "SOL"),
    "NEAR": ("NEARUSDT", "NEAR"), "ZEC": ("ZECUSDT", "ZEC"), "ENA": ("ENAUSDT", "ENA"),
    "PUMPFUN": ("PUMPUSDT", "PUMPFUNUSDT", "PUMPFUN", "PUMP"),
    "HYPE": ("HYPEUSDT", "HYPE"), "MNT": ("MNTUSDT", "MNT"), "SUI": ("SUIUSDT", "SUI"),
    "LTC": ("LTCUSDT", "LTC"), "XMR": ("XMRUSDT", "XMR"), "BNB": ("BNBUSDT", "BNB"),
    "UNI": ("UNIUSDT", "UNI"), "PEPE": ("1000PEPEUSDT", "PEPEUSDT", "PEPE"),
    "DOGE": ("DOGEUSDT", "DOGE"), "BONK": ("1000BONKUSDT", "BONKUSDT", "BONK"),
}
SPEND_EXCLUDED_DIRS = ("_reviewer_box", "docs/history", "research_outputs/tierc10",
                       "research_outputs/tierc10_run2", ".git")
SPEND_LINE_CAP = 240                     # the GREP HAZARD: multi-MB single-line JSON


def _spend_corpus() -> list[tuple[str, str]]:
    """(class, repo-relative path), sorted and whole.  The contract's five
    sources, plus the estate's ROOT-LEVEL result books so that 'never-touched'
    is a claim about SCORED RESULTS and not only about ledgers [LEAN D-k]."""
    out: list[tuple[str, str]] = [("ledger", "LEDGER.md"), ("charter", "Naiad_Phase0_Charter.md"),
                                  ("probe_ledger", "exchange/reports/CENSUS2A_PROBE_LEDGER.md"),
                                  ("probe_ledger", "research_outputs/oracle/roster_probe_2026-09-21.json")]
    out += [("ledger", f"exchange/status/{q.name}")
            for q in sorted((ROOT / "exchange" / "status").glob("LEDGER_*.md"))]
    out += [("rangefinder_build", f"research_outputs/rangefinder/{q.name}")
            for q in sorted((ROOT / "research_outputs" / "rangefinder").glob("*"))
            if q.is_file()]
    out += [("root_book", q.name) for q in sorted(ROOT.glob("*.md"))]
    out += [("root_book", q.name) for q in sorted(ROOT.glob("*.json"))]
    seen, keep = set(), []
    for cls, rel in out:
        if rel in seen or any(rel.startswith(x) for x in SPEND_EXCLUDED_DIRS):
            continue
        if not (ROOT / rel).is_file():
            continue
        seen.add(rel)
        keep.append((cls, rel))
    return sorted(keep, key=lambda x: x[1])


def data_spend_audit(probe: dict, pin: dict) -> dict:
    """{never-touched / display-only / scored} per admitted asset, WITH the
    evidence line that justifies the class [LEAN D-k].  PUMPFUN and HYPE are
    READ out of the evidence, never assumed.

    THE CLASSES COME FROM CLOSED REGISTERS, READ AS LITERALS (no import):
      scored        the stem is in the TC-series scored universe
      display-only  not scored, but in the Oracle's display ROSTER or the
                    frozen study basket — it was LOOKED at, never scored
      never-touched neither, and no grep hit places it in a scored book
    """
    universe = literal_path(ROOT / "scripts" / "tierc2_rules.py", "REGISTER", "UNIVERSE", "value")
    roster = literal_path(ROOT / "scripts" / "oracle_daily.py", "REGISTER", "ROSTER", "value")
    roster_src = literal_path(ROOT / "scripts" / "oracle_daily.py", "REGISTER", "ROSTER", "source")
    basket = literal_path(ROOT / "engine" / "cells.py", "SYMBOLS")
    corpus = _spend_corpus()
    text = {}
    for cls, rel in corpus:
        text[rel] = (cls, (ROOT / rel).read_text(encoding="utf-8", errors="replace").splitlines())
    by_stem = {a["stem"]: a for a in probe["classic5"] + probe["unseen12"] if a.get("stem")}
    rows = []
    for stem, a in by_stem.items():
        name = a["asset"]
        # the DECLARED tokens, plus the asset's own three names, so no spelling
        # the estate could have used is missing (F-D-5 asserts that coverage).
        toks = tuple(sorted(set(SPEND_TOKENS[name]) | {name, a["symbol"], stem},
                            key=lambda x: (-len(x), x)))
        rx = re.compile(r"(?<![A-Za-z0-9])(" + "|".join(toks) + r")(?![A-Za-z0-9])")
        hits, per_class = [], {}
        for rel, (cls, lines) in text.items():
            for i, line in enumerate(lines, 1):
                if rx.search(line):
                    hits.append({"class": cls, "file": rel, "line": i,
                                 "text": line.strip()[:SPEND_LINE_CAP]})
                    per_class[cls] = per_class.get(cls, 0) + 1
        in_universe = stem in universe
        in_roster = stem in roster
        in_basket = stem in basket
        if in_universe:
            cls = "scored"
            why = (f"{stem} is in the TC-series SCORED UNIVERSE "
                   f"(scripts/tierc2_rules.py REGISTER['UNIVERSE']['value'] = {list(universe)}); "
                   f"every registered TC-series result rides it")
        elif in_roster or in_basket:
            cls = "display-only"
            where = ([f"the Oracle's display ROSTER (scripts/oracle_daily.py "
                      f"REGISTER['ROSTER']['value'], {len(roster)} symbols)"] if in_roster else []) \
                + ([f"the FROZEN STUDY BASKET (engine/cells.py SYMBOLS, tier "
                    f"{basket[stem]})"] if in_basket else [])
            why = (f"{stem} is NOT in the TC-series scored universe, and IS in "
                   + " and ".join(where) + " — looked at, never scored")
        else:
            cls = "never-touched"
            why = (f"{stem} is in NO estate register: not the TC-series scored universe, not the "
                   f"Oracle's display ROSTER, not the frozen study basket; and no line of the "
                   f"{len(corpus)}-file corpus places it in a scored book")
        rows.append({
            "asset": name, "stem": stem, "venue": a["venue"], "class": cls,
            "evidence": why,
            "in_tc_series_scored_universe": in_universe,
            "in_oracle_display_roster": in_roster,
            "in_frozen_study_basket": in_basket,
            "grep_tokens": list(toks),
            "grep_hits": len(hits), "grep_hits_by_class": per_class,
            "evidence_lines": hits,
        })
    classes = {k: [r["asset"] for r in rows if r["class"] == k]
               for k in ("scored", "display-only", "never-touched")}
    return {
        "law": "grep the contract's corpus WHOLE and classify every admitted asset "
               "{never-touched / display-only / scored} with the evidence line that justifies "
               "the class. HARD DEPENDENCY of P-GEN-1, whose text must promise 'LOAO printed "
               "twice (all admitted · never-touched only)' — without the never-touched list "
               "that clause cannot be honoured.",
        "as_of_last_closed_4h": pin["as_of_last_closed_4h"],
        "as_of_last_closed_4h_open": pin["as_of_last_closed_4h_open"],
        "warranty": WARRANTY, "seed": SEED,
        "definitions": {
            "never-touched": "the asset has never appeared in any scored result in this estate",
            "display-only": "it appeared in a chart / brief / census print but never in a scored book",
            "scored": "a registered or TC-series result rode it",
        },
        "corpus_class_note": "'root_book' is every root-level .md and .json — the estate's result "
                             "books, its builder contracts and its change logs together. A HIT "
                             "THERE IS NOT PROOF OF SCORING (HYPE is named 53 times there and is "
                             "display-only): the class of an asset is decided by the registers "
                             "below, not by a hit count. The one-directional rule F-D-5 asserts "
                             "is the conservative one — a NEVER-TOUCHED asset must have ZERO "
                             "root_book hits. That is stricter than the definition, so it can be "
                             "too strict, never too lenient: it cannot pass an asset a scored "
                             "result rode.",
        "registers_read_not_imported": {
            "tc_series_scored_universe": {"source": "scripts/tierc2_rules.py REGISTER['UNIVERSE']['value']",
                                          "value": list(universe)},
            "oracle_display_roster": {"source": "scripts/oracle_daily.py REGISTER['ROSTER']['value']",
                                      "value": list(roster), "ruling": roster_src},
            "frozen_study_basket": {"source": "engine/cells.py SYMBOLS (charter §4)",
                                    "value": basket},
        },
        "corpus": [{"class": c, "file": f, "lines": len(text[f][1])} for c, f in corpus],
        "corpus_files": len(corpus),
        "corpus_excluded": list(SPEND_EXCLUDED_DIRS),
        "corpus_exclusion_reason": "_reviewer_box/ and docs/history/ hold multi-megabyte "
                                   "single-line JSON (the GREP HAZARD; every kept line is also "
                                   f"cut at {SPEND_LINE_CAP} chars); research_outputs/tierc10*/ is "
                                   "THIS BUILD's own output and would make the audit "
                                   "self-referential and unreproducible",
        "classes": classes,
        "never_touched": classes["never-touched"],
        "counts": {k: len(v) for k, v in classes.items()},
        "rows": rows,
    }


# ═══════════════════════════════════════════════ 8 · THE MANIFEST
OPERATOR_RULINGS = (
    "F-D-1 IS RED and stays RED: the venue's REST API and its BULK ARCHIVE publish different bars "
    "on incident stamps and the panel is publication-heterogeneous on them (see "
    "venue_publications_disagree). RULING NEEDED: which publication is the record. Ruling ARCHIVE "
    "makes the REST-carrying files the odd ones out; ruling REST the ARCHIVE-carrying ones. The "
    "archive is no clean alternative: it lacks whole days, publishes nothing before 2020, and its "
    "monthly and daily zips disagree with each other on BTC incident bars. No bar is rewritten "
    "either way without the operator's word.",
    "PUMPFUN -> PUMPUSDT [LEAN D-d]: a printed lean, not a ruling. The roster probe recorded the "
    "near-match and explicitly did NOT map it; TC10 maps it because baseAsset PUMP is a TRADING "
    "perpetual and PUMPBTCUSDT is rejected by name. Needs the operator's nod at CLOSE.",
    "MNT -> Bybit v5 linear, whole tape, stem MNTUSDT_BYBIT [LEAN D-c]: a printed lean, not a "
    "ruling (no Binance USDT-M contract exists). The fee charged to it is the estate's flat "
    "Binance-era taker figure — an ASSUMPTION; Bybit's own base taker rate is widely quoted "
    "higher [UNVERIFIED]. Needs the operator's nod at CLOSE, or a named exclusion.",
    "LaCie mirror [LEAN L5]: not done. Every file TC10 fetched exists only in the snapshot on "
    "this laptop; the mirror command PUSHES and its default destination would create an empty "
    "vault. Needs the operator's destination and consent at CLOSE.",
)
PUB_LABELS = ("REST", "ARCHIVE", "BOTH", "MIXED", "UNAUDITED", "BYBIT-REST")


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


def _census_diff(e: dict | None) -> int | None:
    """Bars on which the snapshot is NOT that publication's bar: a differing
    value, a bar the publication lacks, or a bar the snapshot lacks."""
    if e is None:
        return None
    return int(e["price_mismatch"] + e["volume_only_mismatch"] + e["only_in_snapshot"]
               + e.get("only_at_rest", 0) + e.get("only_in_archive", 0))


def publications(files: list[dict], pre: dict) -> dict | None:
    """WHICH of the venue's two publications each native file carries —
    MEASURED from the two whole-history censuses, per (file, lens):
      REST      identical to REST, differs from the ARCHIVE somewhere
      ARCHIVE   identical to the ARCHIVE, differs from REST somewhere
      BOTH      identical to both (the two never disagreed on this file's bars)
      MIXED     differs from both somewhere
      UNAUDITED a census is missing for it (said, never guessed)
    A file TC10 fetched over REST is REST by construction on that side (F-D-1
    samples it); its ARCHIVE side is still censused."""
    rp, ap = OUT / REST_AUDIT, OUT / ARCHIVE_AUDIT
    if not rp.exists() and not ap.exists():
        return None
    rent = json.loads(rp.read_text())["entries"] if rp.exists() else {}
    aent = json.loads(ap.read_text())["entries"] if ap.exists() else {}
    carries, by_lens = {}, {}
    for f in files:
        if f["kind"] != "klines" or not f["native"] or not f["present"]:
            continue
        key, iv = f"{f['stem']}|{f['as_of_lens']}", f["as_of_lens"]
        if f["venue"] != "BINANCE_USDTM":
            label, dr, da, basis = "BYBIT-REST", None, None, "single publication (Bybit v5 REST); no archive twin"
        else:
            tc10 = f["path"] not in pre["files"]
            dr, da = _census_diff(rent.get(key)), _census_diff(aent.get(key))
            basis = ("TC10 REST fetch — REST by construction, sampled by F-D-1" if tc10 and dr is None
                     else "whole-history REST census" if dr is not None else "NO REST census")
            rest_same = dr == 0 or (dr is None and tc10)
            label = ("UNAUDITED" if da is None or (dr is None and not tc10) else
                     "BOTH" if rest_same and da == 0 else
                     "REST" if rest_same else
                     "ARCHIVE" if da == 0 else "MIXED")
        carries[f["path"]] = {"carries": label, "differs_from_rest_bars": dr,
                              "differs_from_archive_bars": da, "rest_basis": basis,
                              "archive_lacks_bars": (aent[key]["only_in_snapshot"] if key in aent else None)}
        by_lens.setdefault(iv, {k: [] for k in PUB_LABELS})[label].append(f["stem"])
    rkeys = ("bars_compared", "price_mismatch", "price_mismatch_not_placeholder",
             "snapshot_flat_placeholder_but_rest_real", "volume_only_mismatch",
             "only_in_snapshot", "only_at_rest", "mismatch_after_old_edge")
    akeys = ("bars_compared", "bars_archive_unpublished", "price_mismatch", "price_mismatch_not_placeholder",
             "snapshot_flat_placeholder_but_archive_real", "archive_flat_placeholder_but_snapshot_real",
             "volume_only_mismatch", "only_in_snapshot", "only_in_archive")

    def totals(ent: dict, keys: tuple) -> dict:
        return {iv: {k: int(sum(e[k] or 0 for e in ent.values() if e["as_of_lens"] == iv)) for k in keys}
                for iv in sorted({e["as_of_lens"] for e in ent.values()})}

    def differing(ent: dict, keys: tuple) -> dict:
        return {k: {q: ent[k][q] for q in keys} for k in sorted(ent) if _census_diff(ent[k])}

    h4 = by_lens.get("4h", {})
    fp = OUT / ARCHIVE_FORMS
    forms = json.loads(fp.read_text())["per_lens"] if fp.exists() else {}
    forms_sum = {iv: {k: b[k] for k in ("incident_days", "asset_days_compared", "bars_compared",
                                        "bars_where_monthly_and_daily_zips_disagree",
                                        "of_which_price_differs", "snapshot_equals")}
                 | {"assets": sorted({r["stem"] for r in b["rows"]})} for iv, b in forms.items()}
    per_stem: dict[str, dict] = {}
    for path, c in carries.items():
        stem, _, iv = path[len("klines/"):-len(".parquet")].rpartition("_")
        per_stem.setdefault(stem, {})[iv] = c["carries"]
    split = {stem: lens for stem, lens in per_stem.items()
             if len({v for v in lens.values() if v in ("REST", "ARCHIVE", "MIXED")}) > 1}
    return {
        "finding": "the venue publishes every native bar TWICE — its REST API and its BULK ARCHIVE — and "
                   "the two DIFFER on a small set of incident stamps. The panel is PUBLICATION-"
                   "HETEROGENEOUS there, MEASURED per file over the whole history, both ways. At 4h "
                   "(the lens 1d/1w derive from): identical to REST and differing from the archive: "
                   f"{h4.get('REST') or 'none'}; identical to the ARCHIVE and differing from REST: "
                   f"{h4.get('ARCHIVE') or 'none'}; identical to both: {h4.get('BOTH') or 'none'}; "
                   f"differing from both: {h4.get('MIXED') or 'none'}; unaudited: "
                   f"{h4.get('UNAUDITED') or 'none'}. Assets whose OWN lenses carry different "
                   f"publications (a lens TC10 fetched whole is REST even where the asset's older "
                   f"lenses carry the archive): {sorted(split) or 'none'}. The ARCHIVE is also "
                   f"INCOMPLETE as a publication: at 4h it LACKS "
                   f"{sum(e['only_in_snapshot'] for e in aent.values() if e['as_of_lens'] == '4h')} bars "
                   f"that the snapshot holds (whole days), and publishes nothing at all for "
                   f"{sum(e['bars_archive_unpublished'] for e in aent.values() if e['as_of_lens'] == '4h')} "
                   f"more (not compared, named per file in the census). And 'the ARCHIVE' is itself TWO "
                   f"forms: the census reads its MONTHLY zips (as the estate's backfill does); on the "
                   f"incident days probed the monthly and the DAILY zip of the same day disagree with "
                   f"EACH OTHER on "
                   f"{sum(b['bars_where_monthly_and_daily_zips_disagree'] for b in forms.values())} bars, "
                   f"assets {sorted({a for b in forms_sum.values() for a in b['assets']}) or 'none'} "
                   f"(archive_forms; NOT probed off the incident days). No cached bar was changed — a prefix is never "
                   "rewritten. Which publication is the record is the operator's ruling: ruling "
                   "ARCHIVE makes the REST-carrying files the odd ones out, ruling REST the "
                   "ARCHIVE-carrying ones. CORRECTION: the first filing of this manifest said "
                   "'pre-existing files carry the ARCHIVE's bar' — that was INFERRED from how the "
                   "files were assembled, not measured, and it is WRONG for the classics.",
        "artifact": f"research_outputs/tierc10/data/{REST_AUDIT}",
        "archive_artifact": f"research_outputs/tierc10/data/{ARCHIVE_AUDIT}",
        "carries": carries, "panel_by_publication": by_lens,
        "assets_split_across_their_own_lenses": {k: split[k] for k in sorted(split)},
        "archive_forms_artifact": f"research_outputs/tierc10/data/{ARCHIVE_FORMS}" if forms else None,
        "archive_forms": forms_sum,
        "per_lens": totals(rent, rkeys), "per_file": differing(rent, rkeys),
        "per_lens_archive": totals(aent, akeys), "per_file_archive": differing(aent, akeys),
        "entries_audited": len(rent), "archive_entries_audited": len(aent)}


def spend_summary(spend: dict) -> dict:
    """The manifest's view of the data-spend audit: the classes whole, and the
    first three evidence lines per asset (the rest live in the artifact)."""
    def head(lines: list[dict]) -> list[dict]:
        """The first TWO lines of EACH corpus class, so a ledger hit is never
        pushed out of the manifest by a run of result-book hits.  The whole
        list — every hit, uncut in number — lives in the artifact."""
        seen, out = {}, []
        for h in lines:
            if seen.get(h["class"], 0) < 2:
                seen[h["class"]] = seen.get(h["class"], 0) + 1
                out.append(h)
        return out

    return {k: v for k, v in spend.items() if k != "rows"} | {
        "artifact": f"research_outputs/tierc10/data/{DATA_SPEND}",
        "rows": [{k: v for k, v in r.items() if k != "evidence_lines"}
                 | {"evidence_lines_shown": head(r["evidence_lines"]),
                    "evidence_lines_shown_rule": "the first two hits of each corpus class; the "
                                                 "whole list is in the artifact",
                    "evidence_lines_total": len(r["evidence_lines"])}
                 for r in spend["rows"]]}


def build_manifest(probe: dict, pin: dict, pre: dict, spend: dict | None = None) -> dict:
    close_ms = pin["as_of_last_closed_4h_close_ms"]
    assets = probe["classic5"] + probe["unseen12"]
    files, funding, admission, derived, excluded = [], {}, [], {}, []
    for a in assets:
        if not a.get("stem"):
            excluded.append({"asset": a["asset"], "reason": a["venue_reason"],
                             "closed_4h_bars": 0, "bars_1d": 0, "bars_1w": 0})
            continue
        stem = a["stem"]
        p4 = kline_path(stem, "4h")
        n4 = 0
        if p4.exists():
            t4 = pd.read_parquet(p4, columns=["open_time"])["open_time"]
            n4 = int((t4 + MS_4H <= close_ms).sum())
        admitted = n4 >= ADMISSION_MIN_4H
        if p4.exists():
            derived[stem] = derive_lenses(stem, pin)
        counts = {"asset": a["asset"], "stem": stem, "venue": a["venue"],
                  "closed_4h_bars": n4, "admission_min": ADMISSION_MIN_4H,
                  "margin": n4 - ADMISSION_MIN_4H,
                  "bars_1d": derived.get(stem, {}).get("1d", {}).get("rows", 0),
                  "bars_1w": derived.get(stem, {}).get("1w", {}).get("rows", 0),
                  "admitted": bool(admitted)}
        admission.append(counts)
        if not admitted:
            excluded.append({"asset": a["asset"], "reason": f"{n4} closed 4h bars < {ADMISSION_MIN_4H}",
                             "closed_4h_bars": n4, "bars_1d": counts["bars_1d"],
                             "bars_1w": counts["bars_1w"]})
        for iv in NATIVE_IVS + DERIVED_IVS:
            q = kline_path(stem, iv)
            row = {"path": f"klines/{q.name}", "asset": a["asset"], "stem": stem,
                   "venue": a["venue"], "listing": a["listing"], "kind": "klines",
                   "as_of_lens": iv, "present": q.exists(),
                   "native": iv in NATIVE_IVS}
            was = pre["files"].get(row["path"])
            row["source"] = (
                "DERIVED from native 4h [LEAN L1]" if iv in DERIVED_IVS else
                "TC10 REST-only fetch (the venue's REST API, whole tape)" if was is None else
                "PRE-EXISTING before TC10 (assembled by the estate's engine.data fetchers — bulk "
                "archive and/or REST; WHICH publication its incident bars carry is MEASURED, see "
                f"`publication`, never inferred); old edge {iso(was['last_ms'])}; rows past it are "
                "TC10 REST")
            if iv in DERIVED_IVS:
                row["publication_inherited_from"] = f"klines/{stem}_4h.parquet"
            if q.exists():
                row.update(sha256=file_sha256(q), bytes=q.stat().st_size,
                           **scan_klines(pd.read_parquet(q), iv, close_ms))
                row["complete_to_as_of"] = bool(
                    row["as_of_last_closed_bar_open"] == iso(target_last_open(iv, close_ms))
                    or iv in DERIVED_IVS)
                if iv in DERIVED_IVS:
                    dv = derived[stem]
                    row["derived_from"] = (
                        f"{dv['source']} (native 4h, {dv['source_rows_as_of']} rows closed "
                        f"as-of) — " + ("1d = exactly six complete 4h bars of one UTC day"
                                        if iv == "1d" else
                                        "1w = seven complete derived days, MONDAY-anchored UTC")
                        + " [LEAN L1]; incomplete buckets dropped: "
                        + str(dv[iv].get("dropped_incomplete_days",
                                         dv[iv].get("dropped_incomplete_weeks"))))
            files.append(row)
        q = funding_path(stem)
        row = {"path": f"funding/{q.name}", "asset": a["asset"], "stem": stem,
               "venue": a["venue"], "listing": a["listing"], "kind": "funding",
               "as_of_lens": "funding", "present": q.exists()}
        if q.exists():
            fs = scan_funding(pd.read_parquet(q), close_ms)
            funding[stem] = fs
            row.update(sha256=file_sha256(q), bytes=q.stat().st_size, **fs)
            row["coverage"] = funding_coverage(stem, close_ms)
        files.append(row)
    in_scope = {f["path"] for f in files}
    other = []
    for sub in ("klines", "funding"):
        for q in sorted((SNAPSHOT / sub).glob("*.parquet")):
            rel = f"{sub}/{q.name}"
            if rel not in in_scope:
                other.append({"path": rel, "sha256": file_sha256(q), "bytes": q.stat().st_size})
    adm = [r for r in admission if r["admitted"]]
    prefixes = verify_prefixes(pre)
    man = {
        "tier": "TIER-C10", "stage": "D", "seed": SEED,
        "as_of_last_closed_4h": pin["as_of_last_closed_4h"],
        "as_of_last_closed_4h_open": pin["as_of_last_closed_4h_open"],
        "as_of_last_closed_4h_close_ms": close_ms,
        "as_of_last_closed_bar_per_lens": {
            iv: {"open": iso(target_last_open(iv, close_ms)),
                 "close": iso(target_last_open(iv, close_ms) + STEP_MS[iv])}
            for iv in NATIVE_IVS + DERIVED_IVS},
        "warranty": WARRANTY,
        "snapshot_root": str(SNAPSHOT),
        "live_cache_touched": False,
        "venues": [{k: a.get(k) for k in ("asset", "venue", "symbol", "stem", "status",
                                          "contract_type", "listing", "venue_reason")}
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
        "mirror": "LaCie mirror DEFERRED to CLOSE [LEAN L5] — every file fetched by TC10 "
                  "exists ONLY in the snapshot on this laptop until then",
        "leans": list(LEANS),
    }
    vd = publications(files, pre)
    if vd:
        man["venue_publications_disagree"] = vd
        for f in files:
            if f["kind"] == "klines" and f["native"]:
                f["publication"] = vd["carries"].get(f["path"])
    man["contract_premise_checks"] = premise_checks(probe)
    man["contract_multipliers"] = contract_multiplier_table()
    man["two_token_trap"] = listing_audit(probe, pin)
    man["data_spend"] = spend_summary(spend) if spend is not None else None
    man["standing_disclosures"] = list(STANDING_DISCLOSURES)
    man["operator_rulings_needed"] = list(OPERATOR_RULINGS)
    late = [{"path": f["path"], "rows_after_as_of": f["rows_after_as_of"]} for f in files
            if f["kind"] == "klines" and f.get("rows_after_as_of")]
    fstamp = [f for f in files if f["kind"] == "funding" and f["present"]]
    man["as_of_hazards"] = {
        "kline_files_holding_rows_after_as_of": late,
        "kline_law": "these rows PRE-DATE TC10 and are never deleted [LEAN D-e]; tierc10_data.load_asof "
                     "cuts them, but tierc2_baseline.load_klines reads the WHOLE file — a TC10 lane that "
                     "loads one of these files through it without an as-of cut reads past the pin",
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
        "artifact": f"research_outputs/tierc10/data/{SEAL}" if seal else None,
        "sealed_sha256": {n: v["sha256"] for n, v in sorted(seal.get("files", {}).items())},
        "fetch_log_sealed_lines": seal.get("fetch_log", {}).get("sealed_lines"),
        "faults": seal_faults, "all_ok": not seal_faults,
        "disclosure": seal.get("disclosure", [])}
    man["complete"] = (all(f["present"] and (f["kind"] == "funding" or f["complete_to_as_of"])
                           for f in files)
                       and all(f["coverage"]["ok"] for f in files
                               if f["kind"] == "funding" and f["present"])
                       and man["contract_multipliers"] is not None
                       and man["data_spend"] is not None
                       and man["two_token_trap"]["all_hard_floored"]
                       and not man["two_token_trap"]["discontinuous_floor_seams"]
                       and not man["two_token_trap"]["intended_asset_unconfirmed"])
    return man


def _md_contract_multipliers(man: dict) -> list[str]:
    cm = man.get("contract_multipliers")
    if not cm:
        return ["", "## Contract multipliers", "",
                f"NOT CAPTURED — {CONTRACT_SPECS} is absent. Run "
                f"`scripts/tierc10_data.py --contract-specs` (one venue reach).", ""]
    L = ["", "## Contract multipliers — printed and normalized", "", cm["finding"], "",
         f"Capture: `{cm['artifact']}` sha256 `{cm['artifact_sha256']}` (exchangeInfo response "
         f"sha256 `{cm['binance_response_sha256']}`). {cm['capture_instant']}", "",
         "| asset | symbol | venue | baseAsset | multiplier (tokens / contract unit) | tokens a "
         "quoted price covers | tick | qty step | min qty | min notional | multiplier fields the "
         "venue publishes |",
         "|---|---|---|---|---:|---|---|---|---|---|---|"]
    for r in cm["rows"]:
        found = cm["multiplier_fields_found_per_symbol"].get(r["symbol"]) or []
        L.append(f"| {r['asset']} | {r['symbol']} | {r['venue']} | {r['base_asset']} | "
                 f"{r['multiplier_tokens_per_contract_unit']} | "
                 f"{r['multiplier_tokens_per_contract_unit']} | {r['price_tick']} | "
                 f"{r['qty_step']} | {r['min_qty']} | {r['min_notional_usdt']} | "
                 f"{' '.join(found) if found else 'NONE'} |")
    L += ["", "### Normalization", "", cm["normalization"], "",
          "Per symbol, the reading:", ""]
    for r in cm["rows"]:
        if r["multiplier_tokens_per_contract_unit"] != 1:
            L.append(f"- **{r['symbol']}** — {r['price_is_per_tokens']}. "
                     f"{r['normalized_price_law']}; {r['normalized_qty_law']}.")
    L.append("")
    return L


def _md_two_token_trap(man: dict) -> list[str]:
    tt = man.get("two_token_trap")
    if not tt:
        return []
    L = ["", "## The two-token trap — F-D-4 (the LIT precedent)", "", tt["law"], "",
         f"Listing source: {tt['listing_source']}.", "", tt["lit_precedent"], "",
         "| asset | symbol | intended base | probe baseAsset | listing | first 4h bar | tape "
         "predates the listing INSTANT | tape predates the HARD FLOOR | hard-floored, every lens "
         "| floor bar rebuilt from its 5m children | floor seam |",
         "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in tt["rows"]:
        fb = r["floor_bar"]
        c = r["continuity_at_the_floor"]
        seam = (f"{c['floor_seam_abs_ln_jump']:.4f} vs limit {c['limit']}"
                if c["floor_seam_exists"] else "NO seam (no bar before the floor)")
        L.append(f"| {r['asset']} | {r['symbol']} | {r['intended_base_expected']} | "
                 f"{r['probe_base_asset']} | {r['listing']} | {r['first_bar_4h']} | "
                 f"{r['tape_predates_listing_instant_4h']} | {r['tape_predates_the_hard_floor']} | "
                 f"{r['hard_floored_every_lens']} | "
                 f"{fb.get('rebuilt')} ({fb.get('children_5m')} children, {fb['subject']}) | "
                 f"{seam} |")
    L += ["", f"{tt['cells_checked']} (asset, lens) cells over {tt['lenses']}: the INTENDED asset "
          f"is confirmed against the venue's own baseAsset on "
          f"**{tt['intended_asset_confirmed']} / {tt['assets']}** "
          f"({tt['intended_asset_unconfirmed'] or 'no mismatch'}); bars before a "
          f"floor: **{tt['bars_before_a_floor'] or 'NONE'}**; floor bars rebuilt exactly from "
          f"their own 5m children: **{tt['floor_bars_rebuilt_from_5m']} / {tt['assets']}**; floor "
          f"seams that EXIST at all: **{tt['floor_seams_that_exist']}** (a seam can only exist "
          f"where the tape holds a bar BEFORE the floor — none does, so the continuity limit "
          f"binds on nothing and that arm of F-D-4 is proven by its BREAK leg alone [LEAN D-i]); "
          f"discontinuous floor seams: **{tt['discontinuous_floor_seams'] or 'none'}**.", "",
          f"Whole-tape 4h seam census (context for the limit {tt['splice_jump_limit_ln']}): "
          f"{tt['whole_tape_4h_seams_total']} adjacent seams over the panel, largest real "
          f"|ln(open/close)| = {tt['whole_tape_4h_max_abs_ln_jump']:.4f}.", ""]
    for rj in tt["rejections_carried"]:
        L.append(f"REJECTED and carried: **{rj['asset']}** `{rj['rejected_symbol']}` — {rj['reason']}")
    L.append("")
    return L


def _md_data_spend(man: dict) -> list[str]:
    ds = man.get("data_spend")
    if not ds:
        return ["", "## Data-spend audit", "",
                f"NOT FILED — {DATA_SPEND} is absent; P-GEN-1's 'never-touched only' clause "
                f"cannot be honoured without it.", ""]
    L = ["", "## Data-spend audit — F-D-5 {never-touched / display-only / scored}", "",
         ds["law"], "",
         f"Corpus: {ds['corpus_files']} files, whole, no sampling. Excluded: "
         f"{ds['corpus_excluded']} — {ds['corpus_exclusion_reason']}.", "",
         ds["corpus_class_note"], "", "Definitions of record: "
         + " · ".join(f"**{k}** = {v}" for k, v in ds["definitions"].items()), "",
         "Registers READ as literals (never imported):", ""]
    for k, v in ds["registers_read_not_imported"].items():
        val = v["value"] if not isinstance(v["value"], dict) else sorted(v["value"])
        L.append(f"- `{k}` — {v['source']} = {val}")
    L += ["", "| asset | stem | class | in TC-series scored universe | in Oracle display roster | "
          "in frozen study basket | grep hits | evidence |",
          "|---|---|---|---|---|---|---:|---|"]
    for r in ds["rows"]:
        L.append(f"| {r['asset']} | {r['stem']} | **{r['class']}** | "
                 f"{r['in_tc_series_scored_universe']} | {r['in_oracle_display_roster']} | "
                 f"{r['in_frozen_study_basket']} | {r['grep_hits']} | {r['evidence']} |")
    L += ["", f"COUNTS: {ds['counts']}. **NEVER-TOUCHED: {ds['never_touched'] or 'none'}** — this "
          f"is the list P-GEN-1's 'LOAO printed twice (all admitted · never-touched only)' "
          f"clause needs, and without it that clause cannot be honoured.", "",
          "The evidence lines that decide the two the contract says must be READ, not assumed:", ""]
    for r in ds["rows"]:
        if r["asset"] in ("PUMPFUN", "HYPE"):
            L.append(f"- **{r['asset']}** -> `{r['class']}`. {r['evidence']}")
            for h in r["evidence_lines_shown"]:
                L.append(f"    - `{h['file']}:{h['line']}` [{h['class']}] {h['text']}")
            if not r["evidence_lines_shown"]:
                L.append(f"    - no line of the corpus names it at all "
                         f"({r['evidence_lines_total']} hits)")
    L.append("")
    return L


def _md_haircut_twin(man: dict) -> list[str]:
    ht = man.get("tiered_costs_haircut_twin")
    if not ht:
        return []
    L = ["", "## The tiered costs haircut twin [VETO \"tiers\"]", "", ht["law"], "",
         f"Contract clause, parsed (never typed): `{ht['contract_clause']}`", "",
         f"Charter source of the model: {ht['charter_source']}", "", ht["charter_note"], "",
         "| tier | bps per side | assets |", "|---|---:|---|"]
    for t, b in ht["tiers"].items():
        L.append(f"| {t} | {b['bps_per_side']} | {' '.join(b['assets'])} |")
    L += ["", f"COVERAGE: {ht['arithmetic']}; every admitted asset assigned: "
          f"**{ht['coverage']['covers_all_admitted']}**; tiered but not admitted: "
          f"{ht['coverage']['tiered_but_not_admitted'] or 'none'}.", "",
          f"Cost law: `{ht['cost_law']}`", "",
          f"THE TC-SERIES TOLL IS UNTOUCHED ON EVERY ROW: **{ht['tc_series_toll_untouched']}** "
          f"(round_trip_bps_used == FEE_BPS_ROUND_TRIP for all 17; the twin is an ADDED column).",
          "",
          "| asset | stem | tier | slippage bps/side | fee bps/side | charter bps/side | charter "
          "round trip bps | TC-series round trip bps (UNTOUCHED) |",
          "|---|---|---|---:|---:|---:|---:|---:|"]
    for r in ht["rows"]:
        L.append(f"| {r['asset']} | {r['stem']} | {r['tier']} | {r['slippage_bps_side']} | "
                 f"{r['fee_bps_side']} | {r['charter_bps_side']} | "
                 f"{r['charter_round_trip_bps']} | {r['tc_series_round_trip_bps_used']} |")
    L.append("")
    return L


def manifest_md(man: dict, fees: dict) -> str:
    L = [f"# TIER-C10 · STAGE D MANIFEST", "",
         f"**AS OF** `{man['as_of_last_closed_4h']}` (last closed 4h bar: open "
         f"`{man['as_of_last_closed_4h_open']}`) · seed {man['seed']} · complete: "
         f"**{man['complete']}**", "",
         f"Snapshot root: `{man['snapshot_root']}` · live cache touched: "
         f"{man['live_cache_touched']}", "", f"> {man['warranty']}", "",
         "## Venue of record", "",
         "| asset | venue | symbol | file stem | status | listing | why |",
         "|---|---|---|---|---|---|---|"]
    for v in man["venues"]:
        L.append(f"| {v['asset']} | {v['venue']} | {v['symbol']} | {v['stem']} | "
                 f"{v['status']} | {v['listing']} | {v['venue_reason']} |")
    for rj in man["venue_rejections"]:
        L.append(f"\nREJECTED for {rj['asset']}: `{rj['rejected_symbol']}` — {rj['reason']}")
    L += ["", "### The contract's venue premises, held against the probe", ""]
    for c in man["contract_premise_checks"]:
        L.append(f"- **{c['asset']}** — contract: \"{c['contract_premise']}\" → {c['verdict']}.")
    L += ["", f"## Admission — {man['admission']['rule']}", "",
          "| asset | stem | closed 4h | margin | 1d | 1w | admitted |", "|---|---|---:|---:|---:|---:|---|"]
    for r in man["admission"]["rows"]:
        L.append(f"| {r['asset']} | {r['stem']} | {r['closed_4h_bars']} | {r['margin']:+d} | "
                 f"{r['bars_1d']} | {r['bars_1w']} | {'ADMITTED' if r['admitted'] else 'EXCLUDED'} |")
    L.append("")
    if man["admission"]["excluded"]:
        for e in man["admission"]["excluded"]:
            L.append(f"EXCLUDED: **{e['asset']}** — {e['reason']} (4h {e['closed_4h_bars']}, "
                     f"1d {e['bars_1d']}, 1w {e['bars_1w']})")
    else:
        L.append("EXCLUDED: none.")
    L += ["", f"PANEL ({man['panels']['panel_size']}): "
          + " ".join(man["panels"]["PANEL17_stems"]), "",
          "## Klines — per file", "", f"Gap policy: {man['gap_policy']}", "",
          "| file | rows | as-of rows | after as-of | first open | last as-of open | gaps "
          "(missing) | dup/off-grid | venue zero-vol flat | sha256 |",
          "|---|---:|---:|---:|---|---|---|---|---:|---|"]
    for f in man["files"]:
        if f["kind"] != "klines":
            continue
        if not f["present"]:
            L.append(f"| {f['path']} | ABSENT | | | | | | | | |")
            continue
        L.append(f"| {f['path']} | {f['rows']} | {f['rows_as_of']} | {f['rows_after_as_of']} | "
                 f"{f['first_open']} | {f['as_of_last_closed_bar_open']} | {f['gap_count']} "
                 f"({f['missing_bars_total']}) | {f['duplicates']}/{f['off_grid']} | "
                 f"{f['venue_zero_volume_flat_bars']} | `{f['sha256'][:16]}` |")
    gapped = [f for f in man["files"] if f["kind"] == "klines" and f.get("gap_count")]
    L += ["", "### Gaps, listed (never filled)", ""]
    if not gapped:
        L.append("None in any native file.")
    for f in gapped:
        shown = ", ".join(f"after {g['after']} x{g['missing_bars']}" for g in f["gaps"][:12])
        more = f" … +{f['gap_count'] - 12} more (whole list in the JSON)" if f["gap_count"] > 12 else ""
        tag = " (derived lens: a gap here is a DROPPED incomplete bucket)" if not f["native"] else ""
        L.append(f"- `{f['path']}`{tag}: {shown}{more}")
    L += ["", "## Funding — per asset", "",
          "| file | rows | first | last | tail interval h | spacing histogram (h: n) | "
          "coverage | sha256 |", "|---|---:|---|---|---:|---|---|---|"]
    for f in man["files"]:
        if f["kind"] != "funding":
            continue
        if not f["present"]:
            L.append(f"| {f['path']} | ABSENT | | | | | **FAIL** | |")
            continue
        L.append(f"| {f['path']} | {f['rows']} | {f['first']} | {f['last']} | "
                 f"{f['interval_hours_observed_tail']} | {f['spacing_hours_histogram']} | "
                 f"{'OK' if f['coverage']['ok'] else 'FAIL: ' + f['coverage']['why']} | "
                 f"`{f['sha256'][:16]}` |")
    L += ["", "## Fee schedule (research_outputs/tierc10/data/fee_schedule.json)", "",
          "| asset | venue | taker bps/side USED | kind | source |", "|---|---|---:|---|---|"]
    for r in fees["assets"]:
        L.append(f"| {r['asset']} | {r['venue']} | {r['taker_bps_side_used']} | ASSUMPTION | "
                 f"{'; '.join(r['source'])} |")
    L += _md_contract_multipliers(man) + _md_two_token_trap(man) \
        + _md_data_spend(man) + _md_haircut_twin(man)
    pa = man["prefix_attestation"]
    ext = [r for r in pa["rows"] if r.get("extended_by")]
    L += ["", "## Old-prefix attestation", "",
          f"{len(pa['rows'])} pre-existing files; all old prefixes byte-content identical: "
          f"**{pa['all_ok']}**; extended forward: {len(ext)} "
          f"({', '.join(r['file'] + ' +' + str(r['extended_by']) for r in ext) or 'none'}).",
          ""]
    vd = man.get("venue_publications_disagree")
    if vd:
        L += ["## The venue's two publications disagree (archive vs REST) — and the panel is "
              "heterogeneous", "", vd["finding"], "",
              "### Which publication each native file carries (MEASURED, per lens)", "",
              "| lens | identical to REST (differs from archive) | identical to ARCHIVE (differs "
              "from REST) | identical to both | differs from both | unaudited | single publication |",
              "|---|---|---|---|---|---|---|"]
        for iv in NATIVE_IVS:
            b = vd["panel_by_publication"].get(iv)
            if b:
                L.append(f"| {iv} | " + " | ".join(" ".join(b[k]) or "—" for k in PUB_LABELS) + " |")
        L += ["", f"### Snapshot vs REST — whole history, {vd['entries_audited']} (file, lens) pairs — "
              f"`{vd['artifact']}`", "",
              "| lens | bars compared | price mismatch | of which snapshot-flat-but-REST-traded | "
              "price mismatch, not a placeholder | volume-only | only in snapshot | only at REST |",
              "|---|---:|---:|---:|---:|---:|---:|---:|"]
        for iv, t in vd["per_lens"].items():
            L.append(f"| {iv} | {t['bars_compared']} | {t['price_mismatch']} | "
                     f"{t['snapshot_flat_placeholder_but_rest_real']} | "
                     f"{t['price_mismatch_not_placeholder']} | {t['volume_only_mismatch']} | "
                     f"{t['only_in_snapshot']} | {t['only_at_rest']} |")
        L += ["", "Files differing from REST: " + (", ".join(
            f"{k} (px {v['price_mismatch']}, vol {v['volume_only_mismatch']})"
            for k, v in vd["per_file"].items()) or "none") + ".", "",
              f"### Snapshot vs BULK ARCHIVE — whole history, {vd['archive_entries_audited']} (file, "
              f"lens) pairs — `{vd['archive_artifact']}`", "",
              "| lens | bars compared | archive unpublished (not compared) | price mismatch | of which "
              "snapshot-flat-but-archive-traded | of which archive-flat-but-snapshot-traded | "
              "volume-only | archive LACKS the bar | snapshot lacks the bar |",
              "|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
        for iv, t in vd["per_lens_archive"].items():
            L.append(f"| {iv} | {t['bars_compared']} | {t['bars_archive_unpublished']} | "
                     f"{t['price_mismatch']} | {t['snapshot_flat_placeholder_but_archive_real']} | "
                     f"{t['archive_flat_placeholder_but_snapshot_real']} | {t['volume_only_mismatch']} | "
                     f"{t['only_in_snapshot']} | {t['only_in_archive']} |")
        if vd.get("archive_forms"):
            L += ["", f"The archive disagrees WITH ITSELF (monthly zip vs daily zip, incident days only) — "
                  f"`{vd['archive_forms_artifact']}`:", "",
                  "| lens | incident days | bars compared | monthly != daily | of which price | snapshot "
                  "equals monthly / daily / neither | assets |", "|---|---:|---:|---:|---:|---|---|"]
            for iv, b in vd["archive_forms"].items():
                q = b["snapshot_equals"]
                L.append(f"| {iv} | {len(b['incident_days'])} | {b['bars_compared']} | "
                         f"{b['bars_where_monthly_and_daily_zips_disagree']} | {b['of_which_price_differs']} | "
                         f"{q['monthly']} / {q['daily']} / {q['neither']} | {' '.join(b['assets']) or '—'} |")
        L += ["", "Files differing from the ARCHIVE: " + (", ".join(
            f"{k} (px {v['price_mismatch']}, vol {v['volume_only_mismatch']}, archive lacks "
            f"{v['only_in_snapshot']})" for k, v in vd["per_file_archive"].items()) or "none") + ".", ""]
    hz = man["as_of_hazards"]
    L += ["## As-of hazards for downstream loaders", "",
          f"- Klines: {hz['kline_law']}. Files: " + (", ".join(
              f"`{x['path']}` +{x['rows_after_as_of']}" for x in hz["kline_files_holding_rows_after_as_of"])
              or "none") + ".",
          f"- Funding: {hz['funding_law']}. Floor hour == nearest hour on every file: "
          f"**{hz['funding_floor_hour_equals_nearest_hour_on_every_file']}**; largest stamp offset past "
          f"its hour over the panel: {hz['funding_ms_past_hour_max_over_panel']} ms; files holding a print "
          f"stamped a few ms after the AS_OF close (it is the AS_OF hour's print): "
          f"{len(hz['funding_files_with_a_print_stamped_after_the_as_of_close'])}.", ""]
    wo = man["write_once"]
    L += ["## Write-once records — sealed, and disclosed", "",
          f"Seal: `{wo['artifact']}` · sealed files re-hash and the fetch log keeps its "
          f"{wo['fetch_log_sealed_lines']} sealed lines: **{wo['all_ok']}**"
          + (f" — FAULTS: {wo['faults']}" if wo["faults"] else "") + "", ""]
    L += [f"- {x}" for x in wo["disclosure"]]
    L += ["", "## Standing disclosures — what a later run must not mistake for tampering", ""]
    L += [f"{i}. {x}" for i, x in enumerate(man.get("standing_disclosures", []), 1)]
    L += ["", "## Operator rulings needed at CLOSE", ""]
    L += [f"{i}. {x}" for i, x in enumerate(man["operator_rulings_needed"], 1)]
    L.append("")
    L += ["## Mirror", "", man["mirror"], "", "## Leans", ""]
    L += [f"- {x}" for x in man["leans"]]
    L += ["", f"Out-of-scope snapshot files (sha'd in the JSON, untouched): "
          f"{len(man['out_of_scope_snapshot_files'])}.", ""]
    return "\n".join(L)


# ═══════════════════════════════════════════════ 9 · REST-vs-SNAPSHOT AUDIT
AUDIT_LIST_CAP = 60


def audit_vs_rest(ivs: tuple[str, ...], out: Path, stems: list[str] | None = None) -> dict:
    """READ-ONLY.  The pre-existing snapshot files were assembled by
    engine.data.backfill_klines from the venue's BULK ARCHIVE
    (data.binance.vision) plus a REST top-up; everything TC10 itself fetched
    is REST-only.  F-D-1 found bars where the venue's two publications
    disagree, so this census re-asks REST for the WHOLE history of a lens and
    counts the disagreement instead of sampling it.  Nothing is saved to the
    snapshot and no cached bar is changed — a prefix is never rewritten; the
    finding is filed, the ruling is the operator's.

    Resumable: one entry per (stem, lens) in REST_VS_SNAPSHOT_AUDIT.json.
    """
    pin, probe = load_pin(OUT), json.loads((OUT / "VENUE_PROBE.json").read_text())
    pre = json.loads((OUT / "PRE_STATE.json").read_text())["files"]
    close_ms = pin["as_of_last_closed_4h_close_ms"]
    p = out / "REST_VS_SNAPSHOT_AUDIT.json"
    aud = json.loads(p.read_text()) if p.exists() else {
        "as_of_last_closed_4h": pin["as_of_last_closed_4h"],
        "as_of_last_closed_4h_open": pin["as_of_last_closed_4h_open"], "warranty": WARRANTY,
        "law": "snapshot bar vs the venue's REST bar at the SAME native interval, whole history, "
               "closed as-of; read-only; lists capped at "
               f"{AUDIT_LIST_CAP} stamps (counts are whole)",
        "entries": {}}
    assets = [a for a in probe["classic5"] + probe["unseen12"]
              if a.get("venue") == "BINANCE_USDTM" and (stems is None or a["stem"] in stems)]
    for iv in ivs:
        for a in assets:
            stem, key = a["stem"], f"{a['stem']}|{iv}"
            if key in aud["entries"] or f"klines/{stem}_{iv}.parquet" not in pre:
                continue
            c = load_asof(stem, iv, OUT)
            step, tgt = STEP_MS[iv], target_last_open(iv, close_ms)
            frames, cursor = [], int(c["open_time"].iloc[0])
            while cursor <= tgt:
                lo, hi = cursor, min(cursor + (CHUNK_BARS - 1) * step, tgt)
                frames.append(_retry(lambda: ED._fetch_rest_klines(a["symbol"], iv, lo, hi),
                                     f"audit {stem} {iv}"))
                cursor = hi + step
                binance_brake()
            r = pd.concat(frames, ignore_index=True)
            r = r[(r["open_time"] >= int(c["open_time"].iloc[0])) & (r["open_time"] <= tgt)]
            m = c.merge(r, on="open_time", how="outer", suffixes=("_c", "_r"), indicator=True)
            both = m[m["_merge"] == "both"]
            px = np.zeros(len(both), dtype=bool)
            for k in ("open", "high", "low", "close"):
                px |= both[f"{k}_c"].to_numpy() != both[f"{k}_r"].to_numpy()
            vol = both["volume_c"].to_numpy() != both["volume_r"].to_numpy()
            flat_c = ((both["open_c"] == both["high_c"]) & (both["high_c"] == both["low_c"])
                      & (both["low_c"] == both["close_c"]) & (both["volume_c"] == 0)).to_numpy()
            placeholder = flat_c & (both["volume_r"].to_numpy() > 0)
            t = both["open_time"].to_numpy(np.int64)
            old_edge = pre[f"klines/{stem}_{iv}.parquet"]["last_ms"]
            rel_vol = np.abs(both["volume_c"].to_numpy() - both["volume_r"].to_numpy()) / \
                np.maximum(both["volume_r"].to_numpy(), 1e-300)
            aud["entries"][key] = {
                "stem": stem, "as_of_lens": iv, "audited_wall_clock_utc": iso(time.time() * 1000),
                "bars_compared": int(len(both)),
                "only_in_snapshot": int((m["_merge"] == "left_only").sum()),
                "only_at_rest": int((m["_merge"] == "right_only").sum()),
                "price_mismatch": int(px.sum()),
                "volume_only_mismatch": int((vol & ~px).sum()),
                "snapshot_flat_placeholder_but_rest_real": int(placeholder.sum()),
                "price_mismatch_not_placeholder": int((px & ~placeholder).sum()),
                "mismatch_after_old_edge": int(((px | vol) & (t > old_edge)).sum()),
                "volume_rel_diff_median_of_mismatches": (
                    float(np.median(rel_vol[vol])) if vol.any() else None),
                "volume_rel_diff_max": float(rel_vol[vol].max()) if vol.any() else None,
                "price_mismatch_stamps": [iso(x) for x in t[px][:AUDIT_LIST_CAP]],
                "volume_only_mismatch_stamps": [iso(x) for x in t[vol & ~px][:AUDIT_LIST_CAP]],
            }
            e = aud["entries"][key]
            log(f"  AUDIT {stem:14s} {iv:3s} compared {e['bars_compared']:7d}  price-mismatch "
                f"{e['price_mismatch']:5d} (placeholders {e['snapshot_flat_placeholder_but_rest_real']:4d})  "
                f"volume-only {e['volume_only_mismatch']:6d}  only-snapshot {e['only_in_snapshot']}  "
                f"only-REST {e['only_at_rest']}")
            _dump(aud, p)
    return aud


# ═══════════════════════════════════════════════ 9b · ARCHIVE-vs-SNAPSHOT AUDIT
ARCHIVE_AUDIT = "ARCHIVE_VS_SNAPSHOT_AUDIT.json"
REST_AUDIT = "REST_VS_SNAPSHOT_AUDIT.json"


def _month_stamps(first_ms: int, last_ms: int) -> list[str]:
    a = datetime.fromtimestamp(first_ms / 1000, tz=timezone.utc)
    b = datetime.fromtimestamp(last_ms / 1000, tz=timezone.utc)
    y, m, out = a.year, a.month, []
    while (y, m) <= (b.year, b.month):
        out.append(f"{y:04d}-{m:02d}")
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return out


def archive_tape(symbol: str, iv: str, first_ms: int, last_ms: int) -> tuple[pd.DataFrame, list[str]]:
    """The venue's BULK ARCHIVE for one (symbol, lens) over [first_ms, last_ms],
    through the estate's own zip reader: the monthly zip, and the DAILY zips of
    a month the venue has not rolled up (the running month).  Returns (frame,
    unpublished_days) — a day the archive does not publish is NAMED and its
    bars are left out of the comparison, never counted as equal."""
    frames, unpublished = [], []
    for ym in _month_stamps(first_ms, last_ms):
        df = _retry(lambda ym=ym: ED._fetch_bulk_zip(symbol, iv, ym, True),
                    f"archive {symbol} {iv} {ym}")
        if df is not None:
            frames.append(df)
            continue
        day = datetime(int(ym[:4]), int(ym[5:]), 1, tzinfo=timezone.utc)
        while f"{day.year:04d}-{day.month:02d}" == ym:
            lo = int(day.timestamp() * 1000)
            if lo + DAY_MS > first_ms and lo <= last_ms:
                stamp = day.strftime("%Y-%m-%d")
                d = _retry(lambda stamp=stamp: ED._fetch_bulk_zip(symbol, iv, stamp, False),
                           f"archive {symbol} {iv} {stamp}")
                if d is None:
                    unpublished.append(stamp)
                else:
                    frames.append(d)
            day += timedelta(days=1)
    if not frames:
        return pd.DataFrame(columns=KLINE_COLS), unpublished
    a = (pd.concat(frames, ignore_index=True).drop_duplicates("open_time", keep="last")
         .sort_values("open_time").reset_index(drop=True))
    return a, unpublished


def audit_vs_archive(ivs: tuple[str, ...], out: Path, stems: list[str] | None = None) -> dict:
    """READ-ONLY, the TWIN of audit_vs_rest.  The REST census can only see a
    file that differs from REST; a file that carries REST's bar where the
    ARCHIVE disagrees is invisible to it (the review found exactly that for
    the classics).  This census asks the venue's OTHER publication for the
    WHOLE history of a lens and counts the disagreement the same way, for
    EVERY Binance-venue file — pre-existing or fetched by TC10.  Nothing is
    saved to the snapshot; no cached bar is changed.

    Resumable: one entry per (stem, lens) in ARCHIVE_VS_SNAPSHOT_AUDIT.json.
    """
    pin, probe = load_pin(OUT), json.loads((OUT / "VENUE_PROBE.json").read_text())
    pre = json.loads((OUT / "PRE_STATE.json").read_text())["files"]
    close_ms = pin["as_of_last_closed_4h_close_ms"]
    p = out / ARCHIVE_AUDIT
    aud = json.loads(p.read_text()) if p.exists() else {
        "as_of_last_closed_4h": pin["as_of_last_closed_4h"],
        "as_of_last_closed_4h_open": pin["as_of_last_closed_4h_open"], "warranty": WARRANTY,
        "law": "snapshot bar vs the venue's BULK ARCHIVE bar (data.binance.vision monthly zips, "
               "daily zips for a month not rolled up) at the SAME native interval, whole history, "
               "closed as-of; read-only; a day the archive does not publish is named and NOT "
               f"compared; lists capped at {AUDIT_LIST_CAP} stamps (counts are whole)",
        "entries": {}}
    assets = [a for a in probe["classic5"] + probe["unseen12"]
              if a.get("venue") == "BINANCE_USDTM" and (stems is None or a["stem"] in stems)]
    for iv in ivs:
        for a in assets:
            stem, key = a["stem"], f"{a['stem']}|{iv}"
            if key in aud["entries"]:
                continue
            c = load_asof(stem, iv, OUT)
            step, tgt = STEP_MS[iv], target_last_open(iv, close_ms)
            first = int(c["open_time"].iloc[0])
            r, unpublished = archive_tape(a["symbol"], iv, first, tgt)
            r = r[(r["open_time"] >= first) & (r["open_time"] <= tgt)]
            dead = {int(datetime.strptime(d, "%Y-%m-%d").replace(tzinfo=timezone.utc)
                        .timestamp() * 1000) for d in unpublished}
            in_dead = (c["open_time"] // DAY_MS * DAY_MS).isin(dead)
            m = c[~in_dead].merge(r, on="open_time", how="outer", suffixes=("_c", "_r"),
                                  indicator=True)
            both = m[m["_merge"] == "both"]
            px = np.zeros(len(both), dtype=bool)
            for k in ("open", "high", "low", "close"):
                px |= both[f"{k}_c"].to_numpy() != both[f"{k}_r"].to_numpy()
            vol = both["volume_c"].to_numpy() != both["volume_r"].to_numpy()
            flat = {sfx: ((both[f"open{sfx}"] == both[f"high{sfx}"])
                          & (both[f"high{sfx}"] == both[f"low{sfx}"])
                          & (both[f"low{sfx}"] == both[f"close{sfx}"])
                          & (both[f"volume{sfx}"] == 0)).to_numpy() for sfx in ("_c", "_r")}
            ph_snap = flat["_c"] & (both["volume_r"].to_numpy() > 0)
            ph_arch = flat["_r"] & (both["volume_c"].to_numpy() > 0)
            t = both["open_time"].to_numpy(np.int64)
            was = pre.get(f"klines/{stem}_{iv}.parquet")
            aud["entries"][key] = {
                "stem": stem, "as_of_lens": iv, "audited_wall_clock_utc": iso(time.time() * 1000),
                "pre_existing_file": was is not None,
                "archive_days_unpublished": unpublished,
                "bars_archive_unpublished": int(in_dead.sum()),
                "bars_compared": int(len(both)),
                "only_in_snapshot": int((m["_merge"] == "left_only").sum()),
                "only_in_archive": int((m["_merge"] == "right_only").sum()),
                "price_mismatch": int(px.sum()),
                "volume_only_mismatch": int((vol & ~px).sum()),
                "snapshot_flat_placeholder_but_archive_real": int(ph_snap.sum()),
                "archive_flat_placeholder_but_snapshot_real": int(ph_arch.sum()),
                "price_mismatch_not_placeholder": int((px & ~ph_snap & ~ph_arch).sum()),
                "mismatch_after_old_edge": (int(((px | vol) & (t > was["last_ms"])).sum())
                                            if was is not None else None),
                "only_in_snapshot_stamps": [iso(x) for x in m.loc[m["_merge"] == "left_only",
                                                                  "open_time"][:AUDIT_LIST_CAP]],
                "only_in_archive_stamps": [iso(x) for x in m.loc[m["_merge"] == "right_only",
                                                                 "open_time"][:AUDIT_LIST_CAP]],
                "price_mismatch_stamps": [iso(x) for x in t[px][:AUDIT_LIST_CAP]],
                "volume_only_mismatch_stamps": [iso(x) for x in t[vol & ~px][:AUDIT_LIST_CAP]],
            }
            e = aud["entries"][key]
            log(f"  ARCHIVE {stem:14s} {iv:3s} compared {e['bars_compared']:7d}  price-mismatch "
                f"{e['price_mismatch']:5d} (snapshot-flat {e['snapshot_flat_placeholder_but_archive_real']:4d}, "
                f"archive-flat {e['archive_flat_placeholder_but_snapshot_real']:4d})  volume-only "
                f"{e['volume_only_mismatch']:6d}  only-snapshot {e['only_in_snapshot']}  only-archive "
                f"{e['only_in_archive']}  unpublished days {len(unpublished)}")
            _dump(aud, p)
    return aud


ARCHIVE_FORMS = "ARCHIVE_FORMS_PROBE.json"


def archive_forms_probe(out: Path) -> dict:
    """READ-ONLY.  The archive is itself published in TWO forms — a MONTHLY zip
    and a DAILY zip — and the census above reads the monthly one (as the
    estate's backfill does).  This probe asks BOTH forms for every INCIDENT
    DAY (a day on which either whole-history census lists a differing stamp
    for ANY asset at that lens), for EVERY Binance-venue asset, and counts the
    bars on which the archive disagrees WITH ITSELF, naming which form the
    snapshot carries there.  Bounded on purpose: incident days only — a
    whole-history daily-zip census is ~40k requests per lens."""
    pin, probe = load_pin(OUT), json.loads((OUT / "VENUE_PROBE.json").read_text())
    days: dict[str, set] = {}
    for name in (REST_AUDIT, ARCHIVE_AUDIT):
        q = OUT / name
        for e in (json.loads(q.read_text())["entries"].values() if q.exists() else []):
            for st in e["price_mismatch_stamps"] + e["volume_only_mismatch_stamps"]:
                days.setdefault(e["as_of_lens"], set()).add(st[:10])
    assets = [a for a in probe["classic5"] + probe["unseen12"] if a.get("venue") == "BINANCE_USDTM"]
    per_lens = {}
    for iv in [x for x in NATIVE_IVS if x in days]:
        rows, n_bars, n_cells, no_daily = [], 0, 0, []
        for a in assets:
            c = load_asof(a["stem"], iv, OUT).set_index("open_time")
            months: dict[str, pd.DataFrame | None] = {}
            for day in sorted(days[iv]):
                lo = int(datetime.strptime(day, "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp() * 1000)
                if not ((c.index >= lo) & (c.index < lo + DAY_MS)).any():
                    continue
                if day[:7] not in months:
                    months[day[:7]] = _retry(lambda m=day[:7]: ED._fetch_bulk_zip(a["symbol"], iv, m, True),
                                             f"forms {a['symbol']} {iv} {day[:7]}")
                mo = months[day[:7]]
                da = _retry(lambda d=day: ED._fetch_bulk_zip(a["symbol"], iv, d, False),
                            f"forms {a['symbol']} {iv} {day}")
                if mo is None or da is None:
                    no_daily.append(f"{a['stem']} {day}: monthly {mo is not None}, daily {da is not None}")
                    continue
                mo = mo[(mo["open_time"] >= lo) & (mo["open_time"] < lo + DAY_MS)]
                j = mo.merge(da, on="open_time", how="inner", suffixes=("_m", "_d"))
                n_cells, n_bars = n_cells + 1, n_bars + len(j)
                for r in j.itertuples(index=False):
                    m_ = [getattr(r, f"{k}_m") for k in KLINE_COLS[1:]]
                    d_ = [getattr(r, f"{k}_d") for k in KLINE_COLS[1:]]
                    if m_ == d_:
                        continue
                    have = [float(c.loc[r.open_time, k]) for k in KLINE_COLS[1:]] if r.open_time in c.index else None
                    rows.append({"stem": a["stem"], "stamp": iso(r.open_time),
                                 "price_differs": m_[:4] != d_[:4],
                                 "snapshot_equals": ("monthly" if have == m_ else "daily" if have == d_
                                                     else "neither" if have is not None else "no bar"),
                                 "monthly": m_, "daily": d_})
        eq = {k: sum(1 for r in rows if r["snapshot_equals"] == k) for k in ("monthly", "daily", "neither")}
        per_lens[iv] = {"incident_days": sorted(days[iv]), "asset_days_compared": n_cells,
                        "bars_compared": n_bars, "bars_where_monthly_and_daily_zips_disagree": len(rows),
                        "of_which_price_differs": sum(1 for r in rows if r["price_differs"]),
                        "snapshot_equals": eq, "form_unpublished": no_daily, "rows": rows}
        log(f"  ARCHIVE FORMS {iv:3s}: {len(days[iv])} incident days x {len(assets)} assets -> {n_bars} bars, "
            f"monthly != daily on {len(rows)} (price on {per_lens[iv]['of_which_price_differs']}); "
            f"snapshot equals {eq}")
    doc = {"as_of_last_closed_4h": pin["as_of_last_closed_4h"],
           "as_of_last_closed_4h_open": pin["as_of_last_closed_4h_open"], "warranty": WARRANTY,
           "law": "the archive's MONTHLY zip vs its DAILY zip, same native interval, INCIDENT DAYS ONLY "
                  "(days either whole-history census lists for any asset at that lens); read-only",
           "probed_utc": iso(time.time() * 1000), "per_lens": per_lens}
    _dump(doc, out / ARCHIVE_FORMS)
    return doc


def merge_audit(name: str, src_dir: Path, out: Path) -> int:
    """Fold a second read-only worker's entries (same function, its own --out)
    into the filed census.  An entry already filed is NEVER replaced; what was
    merged from where is recorded in the artifact, not in a hand note."""
    src, dst = src_dir / name, out / name
    if not src.exists():
        raise SystemExit(f"HALT: nothing to merge at {src}")
    a = json.loads(src.read_text())
    if not dst.exists():
        d = {k: v for k, v in a.items() if k != "entries"}
        d["entries"] = {}
    else:
        d = json.loads(dst.read_text())
    for k in ("as_of_last_closed_4h", "as_of_last_closed_4h_open"):
        if a.get(k) != d.get(k):
            raise SystemExit(f"HALT: {src} is stamped {a.get(k)}, the filed census {d.get(k)}")
    new = sorted(k for k in a["entries"] if k not in d["entries"])
    for k in new:
        d["entries"][k] = a["entries"][k]
    d.setdefault("merged_workers", []).append({"entries": new, "count": len(new)})
    _dump(d, dst)
    log(f"  MERGE {name}: +{len(new)} entries from {src_dir} ({len(d['entries'])} filed)")
    return len(new)


# ═══════════════════════════════════════════════ downstream API (no network)
def load_manifest(out: Path | None = None) -> dict:
    p = (out or OUT) / "STAGE_D_MANIFEST.json"
    if not p.exists():
        raise SystemExit(f"HALT: no Stage D manifest at {p}")
    return json.loads(p.read_text())


def panel(out: Path | None = None) -> dict:
    """{'CLASSIC5': [...], 'UNSEEN': [...admitted stems...], 'PANEL17': [...]}"""
    m = load_manifest(out)["panels"]
    return {"CLASSIC5": m["CLASSIC5"], "UNSEEN": m["UNSEEN_admitted_stems"],
            "PANEL17": m["PANEL17_stems"]}


def load_asof(stem: str, iv: str, out: Path | None = None) -> pd.DataFrame:
    """The ONLY as-of-safe kline read for TC10: bars of lens `iv` CLOSED at the
    pinned AS_OF, ascending.  HALTs on a missing file (never an empty frame)."""
    close_ms = load_pin(out)["as_of_last_closed_4h_close_ms"]
    p = kline_path(stem, iv)
    if not p.exists():
        raise SystemExit(f"HALT: missing {p}")
    d = pd.read_parquet(p).sort_values("open_time")
    return d[d["open_time"] + STEP_MS[iv] <= close_ms].reset_index(drop=True)


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


# ═══════════════════════════════════════════════ run
def run(offline: bool, out: Path) -> int:
    t0 = time.time()
    out.mkdir(parents=True, exist_ok=True)
    log(f"TIER-C10 · STAGE D · seed {SEED} · snapshot {SNAPSHOT}")
    for x in LEANS:
        log(x)
    if offline:
        pin = load_pin(OUT)
        probe = json.loads((OUT / "VENUE_PROBE.json").read_text())
        pre = json.loads((OUT / "PRE_STATE.json").read_text())
        log(f"OFFLINE: AS_OF {pin['as_of_last_closed_4h']} · probe and pre-state re-read")
    else:
        pin = pin_as_of(out)
        probe = probe_venues(out, pin)
        capture_contract_specs(out, pin)      # write-once; re-read on a resumed run
    print_venues(probe)
    assets = [a for a in probe["classic5"] + probe["unseen12"] if a.get("stem")]
    incomplete: list[str] = []
    if not offline:
        close_ms = pin["as_of_last_closed_4h_close_ms"]
        for a in probe["classic5"]:
            e = _edge(kline_path(a["stem"], "4h"), "open_time")
            rel = ("== AS_OF open" if e == pin["as_of_last_closed_4h_open_ms"] else
                   "BEHIND AS_OF (will be extended)" if e < pin["as_of_last_closed_4h_open_ms"]
                   else "AHEAD of AS_OF (rows_after_as_of will say how many)")
            log(f"  classic {a['stem']} 4h edge {iso(e)} (closes {iso(e + MS_4H)}): {rel}")
        pre = write_pre_state(assets, pin, out)
        log("\nFETCH — 4h first (admission), then 12h, 1h, funding, 5m last (the long one)")
        for iv in ("4h", "12h", "1h"):
            for a in assets:
                try:
                    r = extend_klines(a, iv, pin, out)
                    if not r["complete"]:
                        incomplete.append(f"{a['stem']} {iv}: edge {iso(r['edge'])} < {iso(r['target'])}")
                except RuntimeError as e:
                    incomplete.append(f"{a['stem']} {iv}: {e}")
                    log(f"  !! {a['stem']} {iv}: {e}")
        for a in assets:
            try:
                first = int(pd.read_parquet(kline_path(a["stem"], "4h"),
                                            columns=["open_time"])["open_time"].min())
                extend_funding(a, pin, first, out)
                time.sleep(1.0)
            except (RuntimeError, FileNotFoundError) as e:
                incomplete.append(f"{a['stem']} funding: {e}")
                log(f"  !! {a['stem']} funding: {e}")
        for a in assets:
            try:
                r = extend_klines(a, "5m", pin, out)
                if not r["complete"]:
                    incomplete.append(f"{a['stem']} 5m: edge {iso(r['edge'])} < {iso(r['target'])}")
            except RuntimeError as e:
                incomplete.append(f"{a['stem']} 5m: {e}")
                log(f"  !! {a['stem']} 5m: {e}")
        assert close_ms == pin["as_of_last_closed_4h_close_ms"]
    spend = data_spend_audit(probe, pin)
    _dump(spend, out / DATA_SPEND)
    log(f"DATA SPEND ({spend['corpus_files']} files grepped whole): {spend['counts']}; "
        f"never-touched: {spend['never_touched'] or 'none'}")
    man = build_manifest(probe, pin, pre, spend)
    fees = fee_schedule(assets, {f["stem"]: f for f in man["files"]
                                 if f["kind"] == "funding" and f["present"]}, pin)
    man["tiered_costs_haircut_twin"] = haircut_twin_table(
        [a for a in assets if a["asset"] in {r["asset"] for r in man["admission"]["rows"]
                                             if r["admitted"]}], fees)
    ht = man["tiered_costs_haircut_twin"]
    log(f"HAIRCUT TWIN [VETO 'tiers']: {ht['arithmetic']}; TC-series toll untouched on every "
        f"row: {ht['tc_series_toll_untouched']}")
    tt = man["two_token_trap"]
    log(f"TWO-TOKEN TRAP: {tt['cells_checked']} (asset, lens) cells, bars before a floor "
        f"{tt['bars_before_a_floor'] or 'NONE'}; floor bars rebuilt from their 5m children "
        f"{tt['floor_bars_rebuilt_from_5m']}/{tt['assets']}")
    cm = man["contract_multipliers"]
    log(f"CONTRACT MULTIPLIERS: quoting per 1000 tokens: "
        f"{(cm or {}).get('symbols_quoting_per_1000_tokens') if cm else 'NOT CAPTURED'}")
    _dump(man, out / "STAGE_D_MANIFEST.json")
    _dump(fees, out / "fee_schedule.json")
    (out / "STAGE_D_MANIFEST.md").write_text(manifest_md(man, fees), encoding="utf-8")

    log(f"\nADMISSION — {man['admission']['rule']}")
    for r in man["admission"]["rows"]:
        log(f"  {r['asset']:8s} {r['stem']:16s} 4h {r['closed_4h_bars']:6d} ({r['margin']:+6d})  "
            f"1d {r['bars_1d']:5d}  1w {r['bars_1w']:4d}  "
            f"{'ADMITTED' if r['admitted'] else 'EXCLUDED'}")
    for e in man["admission"]["excluded"]:
        log(f"  EXCLUDED {e['asset']}: {e['reason']}")
    if not man["admission"]["excluded"]:
        log("  EXCLUDED: none")
    g = [(f["path"], f["gap_count"], f["missing_bars_total"]) for f in man["files"]
         if f["kind"] == "klines" and f["present"] and f["native"] and f["gap_count"]]
    log(f"GAPS (native files, never filled): {g if g else 'none'}")
    log(f"OLD-PREFIX attestation all_ok: {man['prefix_attestation']['all_ok']}")
    for f in man["files"]:
        if not f["present"]:
            incomplete.append(f"{f['path']}: ABSENT")
        elif f["kind"] == "funding" and not f["coverage"]["ok"]:
            incomplete.append(f"{f['path']}: {f['coverage']['why']}")
            log(f"  FUNDING COVERAGE FAIL: {f['path']}: {f['coverage']['why']}")
    log(f"manifest -> {out / 'STAGE_D_MANIFEST.json'}  complete={man['complete']}  "
        f"elapsed {time.time() - t0:.0f}s")
    if not man["prefix_attestation"]["all_ok"]:
        log("*** HALT: an old prefix moved. ***")
        return 1
    if incomplete or not man["complete"]:
        log("INCOMPLETE (re-run resumes from each file's edge):")
        for x in sorted(set(incomplete)):
            log(f"  - {x}")
        return 2
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--offline", action="store_true",
                    help="no network: re-scan the snapshot, re-derive, re-write the manifest")
    ap.add_argument("--out", default=str(OUT), help="artifact directory (F-DET passes a scratch dir)")
    ap.add_argument("--audit-rest", default="", metavar="IVS",
                    help="READ-ONLY census of snapshot bars vs the venue's REST bars, e.g. 4h,1h")
    ap.add_argument("--audit-archive", default="", metavar="IVS",
                    help="READ-ONLY census of snapshot bars vs the venue's BULK ARCHIVE bars, e.g. 4h,1h")
    ap.add_argument("--probe-archive-forms", action="store_true",
                    help="READ-ONLY: the archive's monthly zip vs its daily zip on the incident days")
    ap.add_argument("--audit-stems", default="", metavar="STEMS",
                    help="restrict --audit-rest / --audit-archive to these file stems (comma list); default all")
    ap.add_argument("--audit-merge", default="", metavar="DIR",
                    help="fold a second audit worker's --out DIR into the filed censuses (never replaces an entry)")
    ap.add_argument("--seal", action="store_true",
                    help="file WRITE_ONCE_SEAL.json (once): shas of the provenance records + the fetch-log prefix")
    ap.add_argument("--contract-specs", action="store_true",
                    help="ONE venue reach: capture CONTRACT_SPECS.json (write-once) — the venue's own "
                         "contract spec per panel symbol, from which the multiplier is read")
    a = ap.parse_args()
    if a.contract_specs:
        capture_contract_specs(Path(a.out), load_pin(OUT))
        return 0
    stems = [x for x in a.audit_stems.split(",") if x] or None
    if a.audit_rest:
        audit_vs_rest(tuple(x for x in a.audit_rest.split(",") if x), Path(a.out), stems)
    if a.audit_archive:
        audit_vs_archive(tuple(x for x in a.audit_archive.split(",") if x), Path(a.out), stems)
    if a.audit_merge:
        for name in (REST_AUDIT, ARCHIVE_AUDIT):
            if (Path(a.audit_merge) / name).exists():
                merge_audit(name, Path(a.audit_merge), Path(a.out))
    if a.probe_archive_forms:
        archive_forms_probe(Path(a.out))
    if a.seal:
        seal_provenance(Path(a.out))
    if a.audit_rest or a.audit_archive or a.audit_merge or a.seal or a.probe_archive_forms:
        return 0
    return run(a.offline, Path(a.out))


if __name__ == "__main__":
    sys.exit(main())
