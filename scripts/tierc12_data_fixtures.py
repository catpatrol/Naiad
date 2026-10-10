#!/usr/bin/env python
"""TIER-C12 · STAGE TC12-D — the substrate's fixtures (scripts/tierc12_data.py, scripts/tierc12_tick.py).

ONE SUITE, TWO INVOCATIONS, ONE TRANSCRIPT EACH [LEANS L-D.15; L-0.9: never a leg filter]:
  scripts/tierc12_data_fixtures.py                        record TC12-D         data/FIXTURES_DATA.txt
  scripts/tierc12_data_fixtures.py --stage=TC12-D.mirror  record TC12-D.mirror  data/FIXTURES_MIRROR.txt
                                                          (the tier's one PROVENANCE transcript)

THE LEG LAW [L-0.14; the common law of LEANS section L-D, part C].  A leg is one `prove` call and
one transcript block.  The BREAK half runs first and must go RED, or the leg is VOID and counts
RED; a plant counts as caught only when a finding NAMES the detector it was planted for; every
plant is made on a COPY (a dict, a frame, a source text, a temp directory) — no real artifact
moves.  NO LEG MAKES A NETWORK CALL: `requests.get` is replaced at import by a refusal, and the
legs that exercise the fetch path hand it an offline STUB venue; the venue was asked by the
BUILDER, once, and its answers are sealed (FLAT_BAR_ATTEST.json, EDGE_AUDIT.json, AS_OF_PIN.json).
The suite HALTs unless NAIAD_CACHE_DIR is the TC12 snapshot (the import of tierc12_data), and it
never imports the shim.

data/FIXTURES_DATA.txt — 41 blocks:
  F-D-GUARD       FAILS IF the guard accepts an unset variable, a '~' or relative spelling, the live
                  cache or a directory inside it, the TC10 or the TC11 snapshot, a foreign directory,
                  or the TC12 path without klines/; or importing the module in a fresh interpreter
                  under any of those does not HALT before engine.data loads.
  F-D-BOUND       FAILS IF a call that writes the snapshot does not sit behind _assert_bound() on
                  every path, or a file-writing call sits outside the typed write owners.
  F-D-PORT        FAILS IF a port labelled VERBATIM is not AST-identical to its function in
                  scripts/tierc11_data.py at the sha TC11's PROGRESS certifies; a TEXT-ONLY port differs
                  from it once string constants are blanked; a provenance comment names the wrong
                  lines or sha; or the port set read off the comments is not PORTS.
  F-D-CLONE       FAILS IF any cloned file's sha differs from TC11's manifest, the clone's file set
                  differs from the source's, or CLONE_ATTEST.json is not write-once.
  F-D-PIN [a]-[f] FAILS IF (a) the filed pin != the derivation from the instant in progress/STEP_Q.json,
                  that instant != the committer time of the commit the record names, or that commit
                  is not the one that added the contract; (b) the pin != the value O-7 prints; (c) it
                  is not a 4h close, open != close - 4h, or the ISO strings disagree; (d) the Binance
                  closeTime != pin - 1 or is not before the venue clock, or the Bybit clock is not past
                  the pin; (e) a scoped non-fixture source holds the pin, TC11's pin or TC10's pin as an
                  int literal or an ISO string; (f) the record moved since the seal or a rewrite gets through.
  F-D-SCOPE       FAILS IF scope_paths(), PRE_STATE's files or the manifest's files[].path differ as a
                  set from TC11's manifest files[].path.
  F-D-FETCHPATH   (offline, a temp snapshot, stub venues) FAILS IF a HALT of the fetch path does not
                  fire, a --fetch resume over the filed snapshot asks or saves anything, the flat-bar
                  capture runs before the extension is complete, an extension can start at or behind a
                  file's PRE_STATE edge, or the fetch path replayed from clone-time bytes does not
                  reproduce the filed content.
  F-D-FORMING     FAILS IF any row past the lens's last bar closing <= the pin is saved to the TEMP
                  snapshot, or a stub venue clock <= the pin does not HALT.
  F-D-VENUE       FAILS IF TC10's Stage D table, the probe and TC11's manifest venues[] disagree on any
                  row; a file's venue is not its asset's; a fetch for a stem came from another venue;
                  or an alternate-venue tape lacks the venue in its stem or has a default-named twin.
  F-D-MANIFEST    FAILS IF a top-level or row key set differs from TC11's under the rename table, a
                  filed sha does not re-hash, or the .md disagrees with the .json.
  F-D-SEAL        FAILS IF one of the seven sealed records, or a sealed line of the fetch log, is not
                  the bytes the seal pinned.
  F-D-PREFIX [i]-[iv]  FAILS IF, for any of the 124 in-scope files, the rows with CLOSE <= TC11's pin are
                  not bit-identical to the TC11 snapshot's file (the four legs of L-D.12).
  F-D-2 [1]-[4]   NO SYNTHETIC BARS ("Naiad inserted no bar"): grid · flat-bar recount == manifest ·
                  banned tokens in the fetch-path code · the sealed venue attribution.
  F-D-3           FUNDING COVERAGE PER ASSET (all 17): coverage ok, load_funding non-empty, the
                  funding-hour law on every print.
  F-D-EDGE        FAILS IF a kline file does not end exactly at its lens's last bar closing <= the pin,
                  has a duplicate, an off-grid stamp or a row past the pin; a funding tape stops short,
                  repeats a print or holds one past pin + jitter; the manifest mis-describes a file;
                  or a status 404 sits among the fetch phase's HTTP rows.
  F-D-DERIVE      FAILS IF 1d / 1w recomputed from native 4h by a plain loop (the COMPENSATED sum
                  stated explicitly) differ by one bit from the derived files, the manifest's content
                  shas are not the loop's, or a week does not open on a Monday.
  F-D-OUT         FAILS IF --out admits research_outputs/tierc10/data or tierc11/data, a symlink or
                  '..' traversal to either, or the stage directory's parent; or a write of
                  write_manifest does not sit behind _out_guard().
  F-D-UNTOUCHED   FAILS IF the TC11 snapshot does not re-hash to TC11's manifest or the TC10 snapshot
                  to TC10's; or the live cache's MANIFEST.json stat moved across this fixture run.
  F-D-DET         FAILS IF two subprocess --manifest builds (hash seeds 1 and the contract seed) differ
                  from each other or from the filed bytes in any determinism-set file, hold a
                  different file set, exit non-zero, carry a clock-named key, or differ in any parquet
                  content sha; OR the call graph of write_manifest holds a clock call.
  F-TOLL [data a]-[data g]  the fee file's maker figure is the extractor's or the README regex's, never
                  a typed one; taker == the estate's object; the carried keys == TC11's file; the URL
                  and date == the sealed capture's; the second extractor agrees; rows == venue blocks.
  F-TICK [a]-[d]  TickGrid == a brute-force Fraction evaluation; no scoped source types a tick or
                  compares in float; the audit's tick is the sealed capture's string; the on-grid
                  shares == the fixture's own Fraction recount on three seeded cells.
data/FIXTURES_MIRROR.txt — 1 block:
  F-MIRROR        FAILS IF any mirrored file re-read from the LaCie differs from the manifest's sha,
                  the file sets differ, or MIRROR_ATTEST.json mis-states either; NOT RUN (never PASS)
                  when the drive is unreachable or no mirror was made.
BANNED: self-comparison; one example where cardinality was possible; a tolerance standing in for an
identity.  The transcripts carry no clock, no temp path and no absolute tree or home path.

Run:  export NAIAD_CACHE_DIR="$HOME/.cache/naiad/snapshots/tc12_20261008" PYTHONDONTWRITEBYTECODE=1
      ~/venvs/naiad/bin/python -B /Users/luis/Naiad/scripts/tierc12_data_fixtures.py \\
          [--stage=TC12-D.mirror] [leg-substring ...] [--refile-transcript] [--root=DIR]
Exit 0 = every leg GREEN (or lawfully NOT RUN), every break RED · 1 = a RED or VOID leg, a
transcript finding, or a HALT.
"""
from __future__ import annotations

import ast
import copy
import hashlib
import html.parser
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from contextlib import contextmanager
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
import tierc12_fx as FX             # noqa: E402  the harness (stdlib only)
import tierc12_pins as PINS         # noqa: E402  the contract's door
import tierc12_progress as PG       # noqa: E402
import tierc12_data as D            # noqa: E402  its import-time guard HALTs off the TC12 snapshot
import numpy as np                  # noqa: E402
import pandas as pd                 # noqa: E402

ARGS = sys.argv[1:]
SEED = PINS.pin("seed")
TAG = FX.suite_tag(__file__)        # "data"
OUT = D.OUT
RUN_ROOT = Path(FX.opt(ARGS, "--root=", str(OUT))).resolve()
STAGE_ARG = FX.opt(ARGS, "--stage=", "TC12-D")

# ── FIXTURE-TYPED LITERALS: the commission, a second object, never the module's own constants ──
STAGES_T = ("TC12-D", "TC12-D.mirror")
TRANSCRIPT_T = {"TC12-D": "FIXTURES_DATA.txt", "TC12-D.mirror": "FIXTURES_MIRROR.txt"}
SNAPSHOT_NAME_T = "tc12_20261008"
OWN_MODULES_T = ("scripts/tierc12_data.py", "scripts/tierc12_tick.py")
STEP_T = {"5m": 300_000, "15m": 900_000, "1h": 3_600_000, "4h": 14_400_000,
          "12h": 43_200_000, "1d": 86_400_000, "1w": 604_800_000}
HOUR_T, DAY_T, WEEK_T, MONDAY_T = 3_600_000, 86_400_000, 604_800_000, 4 * 86_400_000   # 1970-01-05: Monday
JITTER_T = 60_000
PANEL17_T = ("BTCUSDT", "ETHUSDT", "SOLUSDT", "NEARUSDT", "ZECUSDT", "ENAUSDT", "PUMPUSDT",
             "HYPEUSDT", "MNTUSDT_BYBIT", "SUIUSDT", "LTCUSDT", "XMRUSDT", "BNBUSDT", "UNIUSDT",
             "1000PEPEUSDT", "DOGEUSDT", "1000BONKUSDT")
CLASSIC5_T = PANEL17_T[:5]
NATIVE_T = ("5m", "1h", "4h", "12h")
DERIVED_T = ("1d", "1w")
KCOLS_T = ("open_time", "open", "high", "low", "close", "volume")
FCOLS_T = ("funding_time", "funding_rate")
SEALED_T = ("AS_OF_PIN.json", "CLONE_ATTEST.json", "CONTRACT_SPECS.json", "EDGE_AUDIT.json",
            "PRE_STATE.json", "FEE_SOURCE.json", "FLAT_BAR_ATTEST.json")
DET_FILES_T = ("STAGE_D_MANIFEST.json", "STAGE_D_MANIFEST.md", "fee_schedule.json", "TICK_GRID_AUDIT.json")
RENAME_TOP_T = {"tc11_extension": "tc12_extension", "carried_from_tc10": "carried_from_tc11"}
RENAME_ROW_T = {"tc11_rows_added": "tc12_rows_added", "tc10_manifest_sha256": "tc11_manifest_sha256"}
NEW_TOP_T = ("tc11_record", "pins", "tick_of_record", "fee_sources", "zero_volume_bars")
FLAT_N_T = 2                        # F-D-2 [4]: the seeded 5m sample per stem (FX10's count)
TICK_CELLS_T = 3                    # F-TICK [d]: the seeded cells
PORT_LABELS_T = ("VERBATIM", "TEXT-ONLY", "CHANGED")
PORT_RX = re.compile(r"# ported from scripts/tierc11_data\.py:(\d+)-(\d+)(?: \((\w+)\))? @ sha256 "
                     r"([0-9a-f]{16}) — (VERBATIM|TEXT-ONLY|CHANGED)(?:: (.*))?")
STEP_Q_RX_T = re.compile(r"committed (\S+Z)")
O7_RX_T = re.compile(r"\*\*O-7 THE PIN\.\*\*.*?close `([0-9]+)` = \*\*([0-9T:Z-]+)\*\*", re.DOTALL)
MAKER_RX_T = re.compile(r"maker is (\d+(?:\.\d+)?)%")
SINKS_T = ("_save_cache", "_save_funding", "backfill_funding", "backfill_klines", "to_parquet")
SNAPSHOT_WRITERS_T = ("extend_klines", "extend_funding", "_write_if_changed")
FILE_WRITERS_T = ("_dump", "_fetch_log", "capture_fee_sources", "_write_if_changed", "write_manifest",
                  "_mirror_copy", "mirror_snapshot")
FEE_FUNCS_T = ("fee_schedule", "extract_fee", "pct_to_bps", "capture_fee_sources")
EQUAL_TOP_T = ("fee_law", "haircut_twin_law", "haircut_twin_clause", "haircut_twin_tiers",
               "charter_slippage_tiers", "charter_slippage_source")
EQUAL_ROW_T = ("asset", "venue", "symbol", "stem", "taker_bps_side_used", "round_trip_bps_used",
               "kind", "source", "haircut_twin_tier", "haircut_twin_slippage_bps_side",
               "haircut_twin_bps_side", "haircut_twin_round_trip_bps", "haircut_twin_kind",
               "haircut_twin_source", "charter_slippage_tier", "charter_slippage_bps_per_side",
               "charter_slippage_source", "maker_slippage_bps_side", "venue_note")
CLOCK_CALLS_T = ("now", "utcnow", "today")
SEGMENTS_T = ("tuning", "holdout_to_tc11_pin", "strip")
REST_ENDPOINTS_T = {"BINANCE": ("/fapi/v1/klines", "/fapi/v1/fundingRate", "/fapi/v1/ping"),
                    "BYBIT": ("/v5/market/kline", "/v5/market/funding/history")}
ARCHIVE_PREFIX_T = "/data/futures/um/"
LACIE_T = "/Volumes/LaCie"
TYPED_LINES = (
    f"substrate {SNAPSHOT_NAME_T}; own modules {list(OWN_MODULES_T)}",
    f"steps (ms) {STEP_T}; funding jitter {JITTER_T}; Monday anchor {MONDAY_T}",
    f"panel (17) {' '.join(PANEL17_T)}",
    f"sealed files (7) {list(SEALED_T)}; determinism set (4) {list(DET_FILES_T)}",
    f"manifest renames top {RENAME_TOP_T} row {RENAME_ROW_T} new {list(NEW_TOP_T)}",
    f"F-D-2 [4] seeded 5m sample n = {FLAT_N_T} per stem on the stream [seed, crc32('data|F-D-2 [4]')]",
    f"F-TICK [d] seeded cells n = {TICK_CELLS_T} on the stream [seed, crc32('data|F-TICK [d]')]",
)

_HOME, _TREES = str(Path.home()), sorted({str(ROOT), str(ROOT.resolve()), str(D.MAIN_TREE),
                                           str(D.MAIN_TREE.resolve())}, key=len, reverse=True)
TMP = Path(tempfile.mkdtemp(prefix="tc12_fd_"))            # every temp copy; removed at exit
LIVE_MANIFEST = D.LIVE_CACHE / "MANIFEST.json"             # os.stat ONLY — never opened


def _stat3(p: Path):
    try:
        s = os.stat(p)
        return (s.st_size, s.st_mtime_ns, s.st_ino)
    except OSError:
        return None


LIVE_STAT_AT_START = _stat3(LIVE_MANIFEST)


def scrub(s: str) -> str:
    """No absolute tree or home path reaches a transcript: the trees print <tree>, home prints ~."""
    for t in _TREES:
        s = s.replace(t, "<tree>")
    return s.replace(_HOME, "~")


def plants(rows) -> tuple[bool, str]:
    """FX.plants over the same rows, every finding (a HALT's text among them) scrubbed first."""
    def wrap(thunk):
        def run():
            try:
                return [scrub(str(x)) for x in thunk()]
            except SystemExit as e:
                raise SystemExit(scrub(str(e))) from None
        return run
    return FX.plants([(name, want, wrap(thunk)) for name, want, thunk in rows])


def _no_network(*a, **k):
    raise RuntimeError(f"NETWORK REFUSED — no fixture leg makes a network call [L-0.14 D]: {a[:1]}")


D.requests.get = _no_network        # engine.data reaches requests.get through the same module object


def sha_b(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha_f(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def frame_sha_t(df: pd.DataFrame, cols) -> str:
    """The fixture's OWN content sha (the law of scripts/tierc11_data.py frame_sha, re-stated):
    sha256 over "<rows>|<cols>" then each column's raw little-endian bytes — int64 for a *_time
    column, float64 otherwise."""
    h = hashlib.sha256()
    h.update(f"{len(df)}|{','.join(cols)}".encode())
    for c in cols:
        a = df[c].to_numpy()
        h.update(np.ascontiguousarray(a.astype("<i8") if c.endswith("_time") else a.astype("<f8")).tobytes())
    return h.hexdigest()


def jload(p: Path):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def lens_of(rel: str) -> tuple[str, str]:
    stem, _, iv = rel[len("klines/"):-len(".parquet")].rpartition("_")
    return stem, iv


def anchor_t(iv: str) -> int:
    return MONDAY_T if iv == "1w" else 0


def target_t(iv: str, pin_ms: int) -> int:
    """The fixture's own formula for the open of the last bar of a lens closed at an instant."""
    return ((pin_ms - STEP_T[iv] - anchor_t(iv)) // STEP_T[iv]) * STEP_T[iv] + anchor_t(iv)


# ── the filed records (read once; a missing one HALTs the suite: Stage D is not built) ──
def _need(name: str):
    p = OUT / name
    if not p.exists():
        raise SystemExit(f"HALT: {name} is not on file under research_outputs/tierc12/data — Stage D is not built")
    return jload(p)


PIN = _need("AS_OF_PIN.json")
PIN_MS = int(PIN["as_of_last_closed_4h_close_ms"])
PIN_ISO = PIN["as_of_last_closed_4h"]
MAN = _need("STAGE_D_MANIFEST.json")
PRE = _need("PRE_STATE.json")
FEES = _need("fee_schedule.json")
AUDIT = _need("TICK_GRID_AUDIT.json")
SPECS = _need("CONTRACT_SPECS.json")
FEE_SRC = _need("FEE_SOURCE.json")
FLAT = _need("FLAT_BAR_ATTEST.json")
ATTEST = _need("CLONE_ATTEST.json")
SEAL = _need("WRITE_ONCE_SEAL.json")
T11_MAN_BYTES = D.tc11_read("research_outputs/tierc11/data/STAGE_D_MANIFEST.json")
T11_MAN = json.loads(T11_MAN_BYTES)
T11_PIN = D.tc11_pin_record()
T11_PIN_MS = int(T11_PIN["as_of_last_closed_4h_close_ms"])
T10_PIN_MS = int(T11_PIN["tc10_pin_close_ms"])
T11_ROWS = {f["path"]: f for f in T11_MAN["files"]}
T11_OTHER = {o["path"]: o for o in T11_MAN["out_of_scope_snapshot_files"]}
MAN_ROWS = {f["path"]: f for f in MAN["files"]}
SRC_TEXT = (ROOT / "scripts" / "tierc12_data.py").read_text(encoding="utf-8")
TICK_TEXT = (ROOT / "scripts" / "tierc12_tick.py").read_text(encoding="utf-8")
D11_TEXT = (ROOT / "scripts" / "tierc11_data.py").read_text(encoding="utf-8")
FETCH_ROWS = D.fetch_log_rows(OUT)
REAL = D.SNAPSHOT                   # the TC12 snapshot, held while a leg binds the module to a temp one
_FRAMES: dict = {}


def KL(stem: str, iv: str) -> pd.DataFrame:
    """One in-scope kline file of the TC12 snapshot, read once per run (rows sorted by stamp)."""
    if (stem, iv) not in _FRAMES:
        _FRAMES[(stem, iv)] = (pd.read_parquet(str(REAL / "klines" / f"{stem}_{iv}.parquet"))
                               .sort_values("open_time").reset_index(drop=True))
    return _FRAMES[(stem, iv)]


def FU(stem: str) -> pd.DataFrame:
    if (stem, "funding") not in _FRAMES:
        _FRAMES[(stem, "funding")] = (pd.read_parquet(str(REAL / "funding" / f"{stem}.parquet"))
                                      .sort_values("funding_time").reset_index(drop=True))
    return _FRAMES[(stem, "funding")]


def frame_of(rel: str) -> pd.DataFrame:
    if rel.startswith("klines/"):
        return KL(*lens_of(rel))
    return FU(rel[len("funding/"):-len(".parquet")])


def lenses_t(stem: str) -> list:
    return [iv for iv in STEP_T if iv != "15m" or stem in CLASSIC5_T]


SCOPE_T = tuple(rel for s in PANEL17_T for rel in
                [f"klines/{s}_{iv}.parquet" for iv in lenses_t(s)] + [f"funding/{s}.parquet"])


# ── source surgery on COPIES ──
def fn_text(src: str, name: str) -> str:
    """The text of one module-level def of a source."""
    for n in ast.parse(src).body:
        if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name == name:
            a = min([n.lineno] + [d.lineno for d in n.decorator_list])
            return "\n".join(src.splitlines()[a - 1:n.end_lineno]) + "\n"
    raise KeyError(name)


def mut(text: str, old: str, new: str) -> str:
    if text.count(old) != 1:
        raise RuntimeError(f"the plant's anchor {old[:50]!r} occurs {text.count(old)} times, not once")
    return text.replace(old, new)


def shadow(name: str, old: str, new: str, src: str = SRC_TEXT):
    """A mutated COPY of one production function, compiled into the module's own namespace under
    another name (so it sees what the module sees) — the production function is untouched."""
    text = mut(fn_text(src, name), old, new)
    alias = f"_shadow_{name}"
    code = mut(text, f"def {name}(", f"def {alias}(")
    exec(compile(code, f"<shadow {name}>", "exec"), D.__dict__)       # noqa: S102  (a fixture's plant)
    return D.__dict__.pop(alias)


# ── an OFFLINE stub venue and a TEMP snapshot the module is bound to ──
class Resp:
    def __init__(self, payload, status=200, headers=None, url=""):
        self._p, self.status_code, self.headers = payload, status, headers or {}
        self.content, self.url, self.history = json.dumps(payload).encode(), url, []

    def json(self):
        return self._p


class Stub:
    """Answers the module's (and engine.data's) GETs from frames handed in.  `klines` =
    {(symbol, venue interval string): frame}; `funding` = {symbol: frame}; `ignore_window` serves
    every row at or after the start whatever the end asked for (a venue that returns the forming bar)."""

    def __init__(self, klines=None, funding=None, binance_clock=None, bybit_clock=None,
                 ignore_window=False, info=None, bybit_info=None):
        self.klines, self.funding = klines or {}, funding or {}
        self.bclock, self.yclock = binance_clock, bybit_clock
        self.ignore, self.info, self.yinfo, self.calls = ignore_window, info, bybit_info, []

    def _rows(self, key, lo, hi):
        f = self.klines.get(key)
        if f is None:
            return []
        f = f[f["open_time"] >= lo] if self.ignore else f[(f["open_time"] >= lo) & (f["open_time"] <= hi)]
        return [[int(r[0])] + [repr(float(x)) for x in r[1:]] for r in f[list(KCOLS_T)].itertuples(index=False)]

    def __call__(self, url, params=None, **kw):
        q = dict(params or {})
        path = urlparse(url).path
        self.calls.append((path, q))
        if path == "/fapi/v1/ping":
            return Resp({}, headers={"x-mbx-used-weight-1m": "1"})
        if path == "/fapi/v1/time":
            return Resp({"serverTime": self.bclock})
        if path == "/fapi/v1/exchangeInfo":
            return Resp(self.info)
        if path == "/fapi/v1/klines":
            rows = self._rows((q["symbol"], q["interval"]), int(q["startTime"]), int(q["endTime"]))
            return Resp([r + [r[0] + 1] for r in rows[:int(q.get("limit", 1500))]])
        if path == "/fapi/v1/fundingRate":
            f = self.funding.get(q["symbol"], pd.DataFrame(columns=list(FCOLS_T)))
            f = f[(f["funding_time"] >= int(q["startTime"])) & (f["funding_time"] <= int(q["endTime"]))]
            return Resp([{"symbol": q["symbol"], "fundingTime": int(t), "fundingRate": repr(float(r))}
                         for t, r in f[list(FCOLS_T)].itertuples(index=False)])
        if path == "/v5/market/kline":
            rows = self._rows((q["symbol"], q["interval"]), int(q["start"]), int(q["end"]))
            rows = [[str(r[0])] + r[1:] + ["0"] for r in rows][::-1][:int(q.get("limit", 200))]
            return Resp({"retCode": 0, "result": {"list": rows}, "time": self.yclock})
        if path == "/v5/market/funding/history":
            f = self.funding.get(q["symbol"], pd.DataFrame(columns=list(FCOLS_T)))
            f = f[(f["funding_time"] >= int(q["startTime"])) & (f["funding_time"] <= int(q["endTime"]))]
            rows = [{"fundingRateTimestamp": str(int(t)), "fundingRate": repr(float(r))}
                    for t, r in f[list(FCOLS_T)].itertuples(index=False)][::-1]
            return Resp({"retCode": 0, "result": {"list": rows}, "time": self.yclock})
        if path == "/v5/market/instruments-info":
            return Resp({"retCode": 0, "result": {"list": self.yinfo or []}})
        raise RuntimeError(f"the stub venue knows no endpoint {path}")


@contextmanager
def bound(snapshot: Path, stub=None):
    """The module bound to a TEMP snapshot (and to a stub venue) for the duration; restored after."""
    old = (os.environ.get("NAIAD_CACHE_DIR"), D.SNAPSHOT, D.requests.get)
    os.environ["NAIAD_CACHE_DIR"], D.SNAPSHOT = str(snapshot), snapshot
    if stub is not None:
        D.requests.get = stub
    try:
        yield
    finally:
        os.environ["NAIAD_CACHE_DIR"], D.SNAPSHOT, D.requests.get = old


def temp_dir(tag: str) -> Path:
    return Path(tempfile.mkdtemp(prefix=f"{tag}_", dir=TMP))


def temp_snapshot(rels, source: Path = D.TC11_SNAPSHOT) -> Path:
    """A TEMP snapshot holding COPIES of the named files of an old snapshot (read-only source)."""
    snap = temp_dir("snap")
    for sub in ("klines", "funding"):
        (snap / sub).mkdir()
    for rel in rels:
        shutil.copy(source / rel, snap / rel)
    return snap


def pre_of(snap: Path, rels) -> dict:
    """A PRE_STATE-shaped ledger of a temp snapshot (the fixture's own, for its temp copies)."""
    files = {}
    for rel in rels:
        col, cols = ("open_time", KCOLS_T) if rel.startswith("klines/") else ("funding_time", FCOLS_T)
        d = pd.read_parquet(str(snap / rel))
        files[rel] = {"file_sha256": sha_f(snap / rel), "rows": int(len(d)), "first_ms": int(d[col].min()),
                      "last_ms": int(d[col].max()), "content_sha": frame_sha_t(d.sort_values(col), cols)}
    return {"files": files, "law": "a fixture's temp ledger"}


VEN = {a["stem"]: a for a in D.panel_assets()}


# ═══════════════════════════════════════════════ F-D-GUARD
PY = sys.executable


def guard_cases() -> list:
    """(label, value) of every bad NAIAD_CACHE_DIR the guard must refuse."""
    foreign = temp_dir("foreign")
    (foreign / "klines").mkdir()
    inside = D.LIVE_CACHE / "klines"
    return [("unset", None), ("a '~' spelling", "~/.cache/naiad/snapshots/" + SNAPSHOT_NAME_T),
            ("a relative spelling", "snapshots/" + SNAPSHOT_NAME_T), ("the live cache", str(D.LIVE_CACHE)),
            ("a directory inside the live cache", str(inside)), ("the TC10 snapshot", str(D.TC10_SNAPSHOT)),
            ("the TC11 snapshot", str(D.TC11_SNAPSHOT)), ("a foreign directory holding klines/", str(foreign))]


def guard_findings(guard) -> list:
    """GUARD-ACCEPTS: a guard that returns (or raises anything but its HALT) on a bad value."""
    out = []
    for label, value in guard_cases():
        try:
            guard(value)
            out.append(f"GUARD-ACCEPTS {label}: the guard returned instead of HALTing")
        except SystemExit:
            pass
        except Exception as e:                                  # noqa: BLE001
            out.append(f"GUARD-ACCEPTS {label}: raised {type(e).__name__}, not its HALT")
    bare = temp_dir("bare") / SNAPSHOT_NAME_T
    bare.mkdir()
    old = D.SNAPSHOT
    try:
        D.SNAPSHOT = bare                                       # the TC12 path WITHOUT klines/
        try:
            guard(str(bare))
            out.append("GUARD-ACCEPTS the TC12 path without klines/")
        except SystemExit:
            pass
    finally:
        D.SNAPSHOT = old
    return out


def guard_import_findings() -> list:
    """A FRESH interpreter importing the module under a bad value must HALT before engine.data loads."""
    probe = ("import sys\nsys.path.insert(0, sys.argv[1])\n"
             "try:\n    import tierc12_data\n    print('IMPORTED')\n"
             "except SystemExit as e:\n    print('HALT' if str(e).startswith('HALT') else 'EXIT', "
             "'engine.data' in sys.modules)\n")
    out = []
    for label, value in guard_cases():
        env = {k: v for k, v in os.environ.items() if k != "NAIAD_CACHE_DIR"}
        if value is not None:
            env["NAIAD_CACHE_DIR"] = value
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        r = subprocess.run([PY, "-B", "-c", probe, str(ROOT / "scripts")], env=env, capture_output=True,
                           text=True, cwd=str(TMP))
        if r.stdout.strip() != "HALT False":
            out.append(f"GUARD-IMPORT {label}: a fresh interpreter printed {r.stdout.strip()!r} "
                       f"(wanted the HALT before engine.data loads)")
    return out


def guard_break():
    cases = dict(guard_cases())
    no_eq = shadow("guard_substrate", "    if got != SNAPSHOT.resolve():\n"
                   "        raise SystemExit(f\"HALT: NAIAD_CACHE_DIR={got} is not the TC12 snapshot {SNAPSHOT}\")\n", "")
    no_t11 = shadow("guard_substrate", "    if got != SNAPSHOT.resolve():\n"
                    "        raise SystemExit(f\"HALT: NAIAD_CACHE_DIR={got} is not the TC12 snapshot {SNAPSHOT}\")\n", "",
                    src=mut(SRC_TEXT, "                     (TC11_SNAPSHOT, \"the TC11 snapshot — frozen, WRITE-NEVER for TC12\")):",
                            "                     ):"))
    return plants([
        ("NAIAD_CACHE_DIR unset", "is unset", lambda: D.guard_substrate(cases["unset"])),
        ("a '~' spelling", "not an absolute path as given", lambda: D.guard_substrate(cases["a '~' spelling"])),
        ("a relative spelling", "not an absolute path as given",
         lambda: D.guard_substrate(cases["a relative spelling"])),
        ("the live cache", "the LIVE cache", lambda: D.guard_substrate(cases["the live cache"])),
        ("a directory inside the live cache", "the LIVE cache",
         lambda: D.guard_substrate(cases["a directory inside the live cache"])),
        ("the TC10 snapshot", "the TC10 snapshot", lambda: D.guard_substrate(cases["the TC10 snapshot"])),
        ("the TC11 snapshot", "the TC11 snapshot", lambda: D.guard_substrate(cases["the TC11 snapshot"])),
        ("a foreign directory holding klines/", "is not the TC12 snapshot",
         lambda: D.guard_substrate(cases["a foreign directory holding klines/"])),
        ("a guard copy with its final equality test removed", "GUARD-ACCEPTS a foreign directory",
         lambda: guard_findings(no_eq)),
        ("a guard copy with the equality test and the TC11 refusal removed (it accepts the TC11 path)",
         "GUARD-ACCEPTS the TC11 snapshot", lambda: guard_findings(no_t11)),
    ])


def guard_real():
    bad = guard_findings(D.guard_substrate) + guard_import_findings()
    try:
        ok = D.guard_substrate(os.environ.get("NAIAD_CACHE_DIR")) == D.SNAPSHOT.resolve()
    except SystemExit as e:
        ok, bad = False, bad + [f"GUARD-REFUSES the TC12 snapshot: {scrub(str(e))}"]
    n = len(guard_cases())
    return (ok and not bad), (
        f"the guard HALTs on {n} bad values and on the TC12 path without klines/, admits the TC12 snapshot "
        f"({SNAPSHOT_NAME_T}) alone, and a fresh interpreter importing the module under each of the {n} "
        f"HALTs before engine.data is loaded" + (f" — {len(bad)} finding(s): {bad[:3]}" if bad else ""))


# ═══════════════════════════════════════════════ F-D-BOUND
def _calls(node):
    return [c for c in ast.walk(node) if isinstance(c, ast.Call)]


def _name(c: ast.Call) -> str:
    f = c.func
    return f.attr if isinstance(f, ast.Attribute) else f.id if isinstance(f, ast.Name) else ""


def _write_call(c: ast.Call) -> bool:
    n = _name(c)
    if n in ("write_text", "write_bytes", "to_parquet", "replace", "copyfileobj", "copy", "copyfile",
             "copytree", "move", "rename", "unlink", "rmtree", "remove"):
        return not (n == "replace" and isinstance(c.func, ast.Attribute)
                    and not (isinstance(c.func.value, ast.Name) and c.func.value.id == "os"))
    if n == "open":
        mode = c.args[1] if len(c.args) > 1 else next((k.value for k in c.keywords if k.arg == "mode"), None)
        return isinstance(mode, ast.Constant) and any(x in str(mode.value) for x in "wax+")
    return False


def bound_findings(src: str) -> list:
    """BOUND-BARRIER: a snapshot-writing sink not behind _assert_bound(); BOUND-OWNER: a sink or a
    file write outside the typed owners; BOUND-CHAIN: the derivation's writer reached off its chain."""
    tree = ast.parse(src)
    fns = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    out = []
    for name, fn in fns.items():
        sinks = [c for c in _calls(fn) if _name(c) in SINKS_T]
        if sinks and name not in SNAPSHOT_WRITERS_T:
            out.append(f"BOUND-OWNER {name}(): calls {sorted({_name(c) for c in sinks})} and is not a typed "
                       f"snapshot writer {list(SNAPSHOT_WRITERS_T)}")
        writes = [c for c in _calls(fn) if _write_call(c)]
        if writes and name not in FILE_WRITERS_T:
            out.append(f"BOUND-OWNER {name}(): a file-writing call ({sorted({_name(c) for c in writes})}) "
                       f"outside the typed write owners")
        if name in ("extend_klines", "extend_funding"):
            bars = [c.lineno for c in _calls(fn) if _name(c) == "_assert_bound"]
            for c in sinks:
                if not any(b < c.lineno for b in bars):
                    out.append(f"BOUND-BARRIER {name}(): {_name(c)} is not behind _assert_bound()")
    top = [c for n in tree.body if not isinstance(n, (ast.FunctionDef, ast.ClassDef)) for c in _calls(n)]
    if any(_name(c) in SINKS_T or _write_call(c) for c in top):
        out.append("BOUND-OWNER <module>: a write at module level")
    callers = {name: {_name(c) for c in _calls(fn)} for name, fn in fns.items()}
    for callee, want in (("_write_if_changed", {"derive_lenses"}), ("derive_lenses", {"run_derive"})):
        got = {n for n, cs in callers.items() if callee in cs}
        if got != want:
            out.append(f"BOUND-CHAIN {callee}() is called from {sorted(got)}, not from {sorted(want)} alone")
    first = fns["run_derive"].body[0] if "run_derive" in fns else None
    if not (isinstance(first, ast.Expr) and isinstance(first.value, ast.Call)
            and _name(first.value) == "_assert_bound"):
        out.append("BOUND-BARRIER run_derive(): its first statement is not _assert_bound()")
    return out


def _moved_env():
    old = os.environ.get("NAIAD_CACHE_DIR")
    try:
        os.environ["NAIAD_CACHE_DIR"] = str(temp_dir("moved"))
        D._assert_bound()
        return []
    finally:
        os.environ["NAIAD_CACHE_DIR"] = old


def bound_break():
    return plants([
        ("NAIAD_CACHE_DIR moved to a temp dir mid-process", "not the TC12 snapshot", _moved_env),
        ("the barrier removed from a source copy of extend_klines", "BOUND-BARRIER extend_klines",
         lambda: bound_findings(mut(SRC_TEXT, "        if len(df):\n            _assert_bound()\n",
                                    "        if len(df):\n"))),
        ("a raw to_parquet appended in a source copy", "BOUND-OWNER _planted",
         lambda: bound_findings(SRC_TEXT + "\n\ndef _planted(df, p):\n    df.to_parquet(p)\n")),
    ])


def bound_real():
    bad = bound_findings(SRC_TEXT)
    try:
        D._assert_bound()
    except SystemExit as e:
        bad.append(f"BOUND-RUNTIME {scrub(str(e))}")
    return (not bad), (
        f"every snapshot-writing sink {list(SINKS_T)} of scripts/tierc12_data.py sits in a typed writer "
        f"{list(SNAPSHOT_WRITERS_T)} behind _assert_bound() (the derivation's to_parquet through "
        f"run_derive -> derive_lenses -> _write_if_changed, run_derive opening on the barrier); every "
        f"file-writing call sits in a typed owner {list(FILE_WRITERS_T)}; _assert_bound() holds on the "
        f"bound process" + (f" — {len(bad)} finding(s): {bad[:3]}" if bad else ""))


# ═══════════════════════════════════════════════ F-D-PORT
def _blank(node):
    """A deep copy with every string constant blanked and the constant parts of f-strings dropped."""
    node = copy.deepcopy(node)
    for n in ast.walk(node):
        if isinstance(n, ast.JoinedStr):
            n.values = [v for v in n.values if not (isinstance(v, ast.Constant) and isinstance(v.value, str))]
    for n in ast.walk(node):
        if isinstance(n, ast.Constant) and isinstance(n.value, str):
            n.value = ""
    return node


def _objects(text: str) -> dict:
    """{name: (first line, last line, node)} of the module-level defs, classes and assignments."""
    out = {}
    for n in ast.parse(text).body:
        if isinstance(n, (ast.FunctionDef, ast.ClassDef)):
            out[n.name] = (min([n.lineno] + [d.lineno for d in n.decorator_list]), n.end_lineno, n)
        elif isinstance(n, ast.Assign):
            for t in n.targets:
                if isinstance(t, ast.Name):
                    out[t.id] = (n.lineno, n.end_lineno, n)
    return out


def _as(node, name: str):
    """The node under another name (a port may carry its own name: tc11_expected_shas)."""
    node = copy.deepcopy(node)
    if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
        node.name = name
    return node


def port_findings(src: str, ports: dict, d11_text: str, d11_sha: str) -> list:
    """PORT-COMMENT / PORT-LINES / PORT-SHA: a provenance comment that names the wrong lines or sha;
    PORT-VERBATIM: a VERBATIM port not AST-identical; PORT-TEXT-ONLY: a TEXT-ONLY port that differs
    outside string constants; PORT-LABEL: a label that lies; PORT-SET: comments != PORTS."""
    out, mine, theirs, lines, seen = [], _objects(src), _objects(d11_text), src.splitlines(), {}
    if sha_b(d11_text.encode("utf-8")) != d11_sha:
        out.append("PORT-SHA the referee text is not the file TC11's PROGRESS certifies")
    for i, line in enumerate(lines):
        if not line.startswith("# ported from"):
            continue
        m = PORT_RX.fullmatch(line)
        nxt = lines[i + 1] if i + 1 < len(lines) else ""
        got = re.match(r"(?:def|class) (\w+)|(\w+) =", nxt)
        if not m or not got:
            out.append(f"PORT-COMMENT `{line[:70]}…` is not a provenance comment standing on a def or an assignment")
            continue
        name = got.group(1) or got.group(2)
        a, b, alias, sha16, label = int(m.group(1)), int(m.group(2)), m.group(3) or name, m.group(4), m.group(5)
        seen[name] = (label, alias)
        if alias not in theirs:
            out.append(f"PORT-COMMENT {name}: scripts/tierc11_data.py defines no {alias}")
            continue
        ta, tb, tnode = theirs[alias]
        if (a, b) != (ta, tb):
            out.append(f"PORT-LINES {name}: the comment names lines {a}-{b}; {alias} stands at {ta}-{tb}")
        if sha16 != d11_sha[:len(sha16)]:
            out.append(f"PORT-SHA {name}: the comment names a sha that is not the certified one")
        node = _as(mine[name][2], alias)
        same, same_blank = ast.dump(node) == ast.dump(tnode), ast.dump(_blank(node)) == ast.dump(_blank(tnode))
        if label == "VERBATIM" and not same:
            out.append(f"PORT-VERBATIM {name}: labelled VERBATIM and not AST-identical to {alias}")
        elif label == "TEXT-ONLY" and not same_blank:
            out.append(f"PORT-TEXT-ONLY {name}: labelled TEXT-ONLY and differs outside string constants")
        elif label == "TEXT-ONLY" and same:
            out.append(f"PORT-LABEL {name}: labelled TEXT-ONLY and is AST-identical (it is VERBATIM)")
        elif label == "CHANGED" and same_blank:
            out.append(f"PORT-LABEL {name}: labelled CHANGED and no logic differs")
    table = {k: (v[0], v[1]) for k, v in ports.items()}
    if seen != table:
        diff = sorted(set(seen.items()) ^ set(table.items()))
        out.append(f"PORT-SET the ports read off the comments != PORTS ({len(diff)} differing entries: "
                   f"{[d[0] for d in diff][:5]})")
    return out


def _bend_comment(src: str, defname: str, old: str, new: str) -> str:
    """A COPY of a source whose provenance comment above one def is bent."""
    lines = src.split("\n")
    i = next(k for k, x in enumerate(lines) if x.startswith(f"def {defname}("))
    lines[i - 1] = mut(lines[i - 1], old, new)
    return "\n".join(lines)


def port_break():
    sha16 = D.D11_SHA256[:16]
    return plants([
        ("one token changed in a copy of a VERBATIM port (target_last_open)", "PORT-VERBATIM target_last_open",
         lambda: port_findings(mut(SRC_TEXT, "    return ((as_of_close_ms - step - anchor) // step) * step + anchor",
                                   "    return ((as_of_close_ms - step + anchor) // step) * step + anchor"),
                               D.PORTS, D11_TEXT, D.D11_SHA256)),
        ("a comparison flipped in a copy of a TEXT-ONLY port (extend_klines)", "PORT-TEXT-ONLY extend_klines",
         lambda: port_findings(mut(SRC_TEXT, "    if cursor <= pre[\"files\"][rel][\"last_ms\"]:",
                                   "    if cursor < pre[\"files\"][rel][\"last_ms\"]:"),
                               D.PORTS, D11_TEXT, D.D11_SHA256)),
        ("a provenance comment naming the wrong sha", "PORT-SHA frame_sha",
         lambda: port_findings(_bend_comment(SRC_TEXT, "frame_sha", sha16, "0" * len(sha16)), D.PORTS,
                               D11_TEXT, D.D11_SHA256)),
        ("a port dropped from a copy of PORTS", "PORT-SET",
         lambda: port_findings(SRC_TEXT, {k: v for k, v in D.PORTS.items() if k != "iso"}, D11_TEXT,
                               D.D11_SHA256)),
    ])


def port_real():
    bad = port_findings(SRC_TEXT, D.PORTS, D11_TEXT, D.D11_SHA256)
    n = {lab: sum(1 for v in D.PORTS.values() if v[0] == lab) for lab in PORT_LABELS_T}
    return (not bad), (
        f"{len(D.PORTS)} ported objects of scripts/tierc12_data.py against scripts/tierc11_data.py at the sha "
        f"TC11's PROGRESS certifies: {n['VERBATIM']} VERBATIM (AST-identical), {n['TEXT-ONLY']} TEXT-ONLY "
        f"(AST-identical once string constants are blanked), {n['CHANGED']} CHANGED (each differing in "
        f"logic, the difference named); every provenance comment names its source's lines and the certified "
        f"sha; the port set read off the comments is PORTS; TEXT-ONLY: "
        f"{sorted(k for k, v in D.PORTS.items() if v[0] == 'TEXT-ONLY')}"
        + (f" — {len(bad)} finding(s): {bad[:3]}" if bad else ""))


# ═══════════════════════════════════════════════ F-D-CLONE
def clone_record_findings(attest: dict, t11: dict) -> list:
    """CLONE-SHA / CLONE-SET: the filed attestation against TC11's manifest (in-scope + out-of-scope)."""
    exp = {f["path"]: f["sha256"] for f in t11["files"]} | {o["path"]: o["sha256"]
                                                            for o in t11["out_of_scope_snapshot_files"]}
    out = []
    if set(attest["files"]) != set(exp):
        out.append(f"CLONE-SET the clone's file set != TC11's manifest ({sorted(set(attest['files']) ^ set(exp))[:4]})")
    for rel, row in sorted(attest["files"].items()):
        if row["sha256"] != exp.get(rel) or row["reference_sha256"] != exp.get(rel) or not row["equal"]:
            out.append(f"CLONE-SHA {rel}: sha != reference (TC11's manifest)")
    if not attest["all_equal"] or attest["n_files"] != len(exp):
        out.append("CLONE-SHA the attestation does not say all equal over TC11's file count")
    if attest["tc11_manifest"]["sha256"] != sha_b(T11_MAN_BYTES):
        out.append("CLONE-SHA the attestation names another TC11 manifest sha than the certified one")
    return out


def _clone_tree(flip: bool = False, stray: bool = False) -> list:
    rels = ["funding/BTCUSDT.parquet", "funding/MNTUSDT_BYBIT.parquet", "klines/BTCUSDT_1w.parquet"]
    a, b = temp_snapshot(rels), temp_snapshot(rels)
    if flip:
        raw = bytearray((a / rels[0]).read_bytes())
        raw[len(raw) // 2] ^= 1
        (a / rels[0]).write_bytes(bytes(raw))
    if stray:
        (a / "funding" / "STRAY.parquet").write_bytes(b"x")
    faults, _ = D.clone_findings(a, {r: T11_ROWS[r]["sha256"] for r in rels}, b)
    return [f"CLONE-TREE {x}" for x in faults]


def clone_break():
    return plants([
        ("a flipped byte in a temp copy of a cloned file", "!= reference", lambda: _clone_tree(flip=True)),
        ("a stray file added to a temp tree", "file sets differ", lambda: _clone_tree(stray=True)),
        ("a rewrite of the filed CLONE_ATTEST.json", "WRITE-ONCE",
         lambda: D._dump_once({"rewritten": True}, OUT / "CLONE_ATTEST.json")),
        ("one sha altered in a COPY of the attestation", "CLONE-SHA",
         lambda: clone_record_findings({**ATTEST, "files": {**ATTEST["files"], "MANIFEST.json": {
             **ATTEST["files"]["MANIFEST.json"], "sha256": "0" * 64}}}, T11_MAN)),
    ])


def clone_real():
    bad = clone_record_findings(ATTEST, T11_MAN) + _clone_tree()
    if SEAL["files"].get("CLONE_ATTEST.json", {}).get("sha256") != sha_f(OUT / "CLONE_ATTEST.json"):
        bad.append("CLONE-SEAL CLONE_ATTEST.json is not the bytes the seal pinned")
    return (not bad), (
        f"CLONE_ATTEST.json (sealed, write-once): {ATTEST['n_files']} cloned files, each re-hashed BEFORE any "
        f"extension equal to TC11's manifest ({len(T11_ROWS)} in-scope + {len(T11_OTHER)} out-of-scope), the "
        f"file set equal to the source's, under the TC11 manifest sha TC11's PROGRESS certifies; the "
        f"comparator is clean on an untouched temp tree" + (f" — {len(bad)} finding(s): {bad[:3]}" if bad else ""))


# ═══════════════════════════════════════════════ F-D-PIN [a] … [f]
def git(*argv) -> str:
    r = subprocess.run(["git", "--no-optional-locks", "-C", str(D.MAIN_TREE)] + list(argv),
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"git {' '.join(argv[:2])} failed: {r.stderr.strip()[:120]}")
    return r.stdout.strip()


def step_q_instant_ms(step_q: dict) -> int:
    """The fixture's OWN reading of the STEP Q instant (calendar arithmetic, no datetime)."""
    hits = STEP_Q_RX_T.findall(step_q.get("one_line", ""))
    if len(hits) != 1:
        raise SystemExit(f"HALT: {len(hits)} `committed <instant>Z` stamps in the STEP Q record")
    y, mo, d, h, mi, s = (int(x) for x in re.fullmatch(r"(\d+)-(\d+)-(\d+)T(\d+):(\d+):(\d+)Z", hits[0]).groups())
    y2, m2 = (y - 1, mo + 9) if mo <= 2 else (y, mo - 3)                # days from civil (proleptic Gregorian)
    era, yoe = y2 // 400, y2 % 400
    days = era * 146097 + yoe * 365 + yoe // 4 - yoe // 100 + (153 * m2 + 2) // 5 + d - 1 - 719468
    return ((days * 24 + h) * 60 + mi) * 60_000 + s * 1000


def pin_a_findings(pin_ms: int, step_q: dict) -> list:
    """PIN-DERIVATION: the pin != the derivation from the STEP Q instant; PIN-COMMITTER: that instant
    != the committer time of the commit the record names; PIN-ADD: that commit did not add the contract."""
    out = []
    ct = step_q_instant_ms(step_q)
    want = (ct // STEP_T["4h"]) * STEP_T["4h"]
    if pin_ms != want:
        out.append(f"PIN-DERIVATION pin != derivation from STEP Q: {pin_ms} vs {want}")
    commit = str(step_q.get("commit"))
    if int(git("show", "-s", "--format=%ct", commit)) * 1000 != ct:
        out.append("PIN-COMMITTER the STEP Q instant != git committer time of the commit the record names")
    added = git("log", "--diff-filter=A", "--format=%H", "--", D.CONTRACT_REL).split("\n")
    if not added[len(added) - 1].startswith(commit):
        out.append("PIN-ADD the commit the record names is not the one that added the contract file")
    return out


def o7_findings(pin_ms: int, pin_iso: str, rulings_text: str) -> list:
    m = O7_RX_T.search(rulings_text)
    if not m:
        return ["PIN-O7 O-7's paragraph prints no pin"]
    return [] if (int(m.group(1)), m.group(2)) == (pin_ms, pin_iso) else [
        f"PIN-O7 the filed pin {pin_ms} / {pin_iso} != the value O-7 prints ({m.group(1)} / {m.group(2)})"]


def pin_literal_findings(name: str, src: str) -> list:
    """PIN-LITERAL: a pin (TC12's, TC11's, TC10's) as an int literal (AST and text, underscores
    admitted) or as an ISO string to the minute, anywhere in a scoped source."""
    out = []
    pins = {"TC12's pin": (PIN_MS, PIN_ISO), "TC11's pin": (T11_PIN_MS, T11_PIN["as_of_last_closed_4h"]),
            "TC10's pin": (T10_PIN_MS, T11_PIN["tc10_pin"])}
    ints = {c.value for c in ast.walk(ast.parse(src)) if isinstance(c, ast.Constant) and type(c.value) is int}
    for label, (ms, iso) in sorted(pins.items()):
        if ms in ints or re.search(r"(?<![0-9_])" + "_?".join(str(ms)) + r"(?![0-9_])", src):
            out.append(f"PIN-LITERAL {name}: holds {label} as an int")
        if re.search(re.escape(iso.rsplit(":", 1)[0]).replace("T", "[T ]"), src):
            out.append(f"PIN-LITERAL {name}: holds {label} as an ISO string")
    return out


def scoped_sources() -> dict:
    """THE SCOPE [the common law of L-D part C; L-0.11]: the non-fixture scripts/tierc12_*.py named
    by the records before TC12-D in the resume order, plus this record's own modules (typed)."""
    order = list(PG.RESUME_ORDER)
    recs = PG.records(ROOT)
    rels = {p for rid in order[:order.index("TC12-D")] if rid in recs for p in recs[rid].get("artifact_shas", {})
            if re.fullmatch(r"scripts/tierc12_\w+\.py", p) and not p.endswith("_fixtures.py")}
    return {rel: (ROOT / rel).read_text(encoding="utf-8") for rel in sorted(rels | set(OWN_MODULES_T))}


def sealed_copy_findings(name: str, edit) -> list:
    """A sealed record rewritten in a TEMP copy of the stage directory -> the seal's own verifier."""
    tmp = temp_dir("seal")
    for n in SEALED_T + ("FETCH_LOG.jsonl",):
        shutil.copy(OUT / n, tmp / n)
    (tmp / name).write_text(edit((tmp / name).read_text(encoding="utf-8")), encoding="utf-8")
    return [f"SEAL-MOVED {x}" for x in D.verify_seal(OUT, tmp)]


def _stub_rows():
    row, lrow = list(PIN["venue_kline_of_pinned_bar"]), list(PIN["venue_kline_of_pinned_bar"])
    return row, lrow, [list(PIN["bybit_kline_of_pinned_bar"])]


def pin_legs() -> list:
    step_q = jload(ROOT / D.STEP_Q_REL)
    rulings = (ROOT / D.RULINGS_REL).read_text(encoding="utf-8")
    keys = D.tc11_pin_keys()
    srcs = scoped_sources()
    row, lrow, yrows = _stub_rows()
    srv, yclk = int(PIN["venue_server_time_ms"]), int(PIN["bybit_server_time_ms"])
    moved = dict(step_q, one_line=step_q["one_line"].replace("T22:52:13Z", "T18:52:13Z"))
    first = sorted(srcs)[0]

    def d_filed() -> list:
        out = []
        if int(PIN["venue_close_time_of_pinned_bar_ms"]) != PIN_MS - 1:
            out.append("PIN-CLOSED the filed Binance closeTime != pin - 1")
        if not int(PIN["venue_close_time_of_pinned_bar_ms"]) < srv:
            out.append("PIN-CLOSED the filed Binance closeTime is not before the filed venue clock")
        if not PIN_MS < yclk:
            out.append("PIN-CLOSED the filed Bybit clock is not past the pin")
        try:
            D.prove_closed(PIN_MS, srv, row, lrow, yrows, yclk)
        except SystemExit as e:
            out.append(f"PIN-CLOSED the proof function refuses the filed answers: {scrub(str(e))}")
        return out

    def rewrite():
        D._dump_once(dict(PIN), OUT / "AS_OF_PIN.json")
        return []

    return [
        ("F-D-PIN [a]", "the pin is the derivation from the filed STEP Q instant, and that instant is git's",
         "a pin one bar later than the derivation, or a STEP_Q.json copy whose instant is moved by four hours",
         "the filed pin != the derivation from the instant in progress/STEP_Q.json, that instant != the "
         "committer time of the commit the record names (git show -s --format=%ct), or that commit is not "
         "the one that added the contract file (git log --diff-filter=A)",
         lambda: plants([
             ("a pin typed one 4h bar later than the derivation", "PIN-DERIVATION",
              lambda: pin_a_findings(PIN_MS + STEP_T["4h"], step_q)),
             ("a STEP_Q.json copy whose instant is moved by four hours", "PIN-COMMITTER",
              lambda: pin_a_findings(PIN_MS, moved)),
             ("production's derivation on that moved copy", "pin != derivation from STEP Q",
              lambda: D.derive_pin(step_q=_write(temp_dir("sq") / "STEP_Q.json", json.dumps(moved)))),
         ]),
         lambda: _ok(pin_a_findings(PIN_MS, step_q) + ([] if D.PIN_CLOSE_MS == PIN_MS else [
             "PIN-DERIVATION the module's derivation != the filed pin"]),
             f"the filed pin {PIN_ISO} == (instant // 4h) x 4h for the one `committed <instant>Z` of "
             f"progress/STEP_Q.json ({step_q_instant_ms(step_q)} ms, the fixture's own calendar arithmetic) == "
             f"the module's derivation; that instant == the committer time of commit {step_q.get('commit')}, "
             f"which is the commit that added the contract file")),
        ("F-D-PIN [b]", "the pin is the value O-7 prints",
         "a rulings copy whose printed value is one bar off",
         "the filed pin != the value printed in O-7's paragraph of ORCHESTRATOR_RULINGS.md",
         lambda: plants([
             ("a rulings copy whose printed pin is one 4h bar off", "PIN-O7",
              lambda: o7_findings(PIN_MS, PIN_ISO, rulings.replace(str(PIN_MS), str(PIN_MS + STEP_T["4h"])))),
             ("production's derivation against that rulings copy", "pin != derivation from STEP Q",
              lambda: D.derive_pin(step_q=ROOT / D.STEP_Q_REL, rulings=_write(
                  temp_dir("o7") / "R.md", rulings.replace(str(PIN_MS), str(PIN_MS + STEP_T["4h"]))))),
         ]),
         lambda: _ok(o7_findings(PIN_MS, PIN_ISO, rulings),
                     f"the filed pin {PIN_MS} = {PIN_ISO} is the 13-digit value and the ISO instant O-7's "
                     f"paragraph prints (parsed here from the rulings file — a second object)")),
        ("F-D-PIN [c]", "a 4h close; open = close - 4h; the ISO strings agree",
         "a pin record copy off the 4h modulus",
         "the filed pin is not a 4h close, open != close - 4h, or the ISO strings disagree with the ms",
         lambda: plants([
             ("a pin record copy whose close is off the 4h modulus", "is not a 4h bar close",
              lambda: [f"PIN-RECORD {x}" for x in D.pin_findings(
                  dict(PIN, as_of_last_closed_4h_close_ms=PIN_MS + 1), keys)]),
             ("a pin record copy whose open is one hour late", "!= close - 4h",
              lambda: [f"PIN-RECORD {x}" for x in D.pin_findings(
                  dict(PIN, as_of_last_closed_4h_open_ms=PIN_MS - STEP_T["4h"] + HOUR_T), keys)]),
             ("a pin record copy whose ISO string is another instant", "ISO strings disagree",
              lambda: [f"PIN-RECORD {x}" for x in D.pin_findings(
                  dict(PIN, as_of_last_closed_4h=PIN["as_of_last_closed_4h_open"]), keys)]),
         ]),
         lambda: _ok(D.pin_findings(PIN, keys) + ([] if PIN_MS % STEP_T["4h"] == 0 and int(
             PIN["as_of_last_closed_4h_open_ms"]) == PIN_MS - STEP_T["4h"] else ["PIN-RECORD off the grid"]),
             f"close {PIN_MS} is a multiple of the 4h step, open = close - 4h, both ISO strings agree with "
             f"the ms, and the record carries every key of TC11's pin record ({len(keys)})")),
        ("F-D-PIN [d]", "closed on both venue clocks (the filed record; the proof function on stubbed answers)",
         "a Binance row whose closeTime >= serverTime ('still forming'), or a Bybit clock <= the pin",
         "the filed Binance closeTime != pin - 1 or is not before the filed venue clock, or the filed Bybit "
         "clock is not past the pin",
         lambda: plants([
             ("a stubbed Binance answer whose closeTime >= serverTime", "still forming",
              lambda: D.prove_closed(PIN_MS, PIN_MS - 1, row, lrow, yrows, yclk)),
             ("a stubbed Bybit clock at the pin", "is not past the pin",
              lambda: D.prove_closed(PIN_MS, srv, row, lrow, yrows, PIN_MS)),
             ("a stubbed Bybit envelope without `time`", "absent or is not an integer",
              lambda: D.prove_closed(PIN_MS, srv, row, lrow, yrows, None)),
             ("a stubbed Bybit clock in seconds", "absent or is not an integer",
              lambda: D.prove_closed(PIN_MS, srv, row, lrow, yrows, yclk // 1000)),
         ]),
         lambda: _ok(d_filed(), f"filed: Binance closeTime of the pinned bar = pin - 1 ms < the Binance clock "
                                f"{D.iso(srv)}; Bybit served the pinned bar and its envelope clock "
                                f"{D.iso(yclk)} is past the pin; the latest closed 4h at the pin run was "
                                f"{PIN['latest_closed_4h_at_pin_run']} (== pin: "
                                f"{PIN['pin_equals_latest_closed_at_pin_run']})")),
        ("F-D-PIN [e]", "no scoped source holds a pin as a literal",
         "the pin as an int and as an ISO string typed into copies of a scoped source",
         "a non-fixture scripts/tierc12_*.py in this suite's scope holds the pin, TC11's pin or TC10's pin as "
         "an int literal or an ISO string (AST + text scan)",
         lambda: plants([
             ("the pin typed as an int in a copy of a scoped source", "PIN-LITERAL",
              lambda: pin_literal_findings(first, srcs[first] + f"\nPIN_MS = {PIN_MS}\n")),
             ("the pin typed as an ISO string in a copy", "PIN-LITERAL",
              lambda: pin_literal_findings(first, srcs[first] + f'\nPIN_ISO = "{PIN_ISO}"\n')),
             ("TC11's pin typed with underscores in a copy", "PIN-LITERAL",
              lambda: pin_literal_findings(first, srcs[first] + f"\nW = {T11_PIN_MS:_}\n")),
         ]),
         lambda: _ok([x for rel, s in srcs.items() for x in pin_literal_findings(rel, s)],
                     f"{len(srcs)} scoped non-fixture sources (the records before TC12-D in the resume order, "
                     f"plus {list(OWN_MODULES_T)}) hold none of the three pins as an int or an ISO string")),
        ("F-D-PIN [f]", "the pin record is sealed and write-once",
         "a pin record copy rewritten after the seal",
         "the record moved since the seal, or a rewrite of it gets through",
         lambda: plants([
             ("a pin record copy rewritten after the seal", "bytes moved since the seal",
              lambda: sealed_copy_findings("AS_OF_PIN.json", lambda t: t.replace("TC12-D", "TC12-X"))),
             ("a second write of the filed record through the write-once door", "WRITE-ONCE", rewrite),
         ]),
         lambda: _ok(([] if SEAL["files"]["AS_OF_PIN.json"]["sha256"] == sha_f(OUT / "AS_OF_PIN.json") else [
             "PIN-SEAL AS_OF_PIN.json is not the bytes the seal pinned"]),
             "AS_OF_PIN.json is the bytes WRITE_ONCE_SEAL.json pinned, and the write-once door refuses a "
             "second write")),
    ]


def _write(p: Path, text: str) -> Path:
    p.write_text(text, encoding="utf-8")
    return p


def _ok(findings: list, why: str) -> tuple[bool, str]:
    findings = [scrub(str(x)) for x in findings]
    return (not findings), (why if not findings else f"{len(findings)} finding(s): {findings[:4]}")


# ═══════════════════════════════════════════════ F-D-SCOPE
def scope_findings(scope, pre_files, man_paths) -> list:
    want = {f["path"] for f in T11_MAN["files"]}
    out = []
    for label, got in (("scope_paths()", set(scope)), ("PRE_STATE.json files", set(pre_files)),
                       ("the manifest's files[].path", set(man_paths)), ("the fixture's typed scope", set(SCOPE_T))):
        if got != want:
            out.append(f"SCOPE {label} != TC11's manifest files[].path: missing {sorted(want - got)[:3]}, "
                       f"extra {sorted(got - want)[:3]}")
    return out


def scope_break():
    sp = D.scope_paths()
    return plants([
        ("a path dropped from a copy of the scope", "SCOPE scope_paths()",
         lambda: scope_findings(sp[1:], PRE["files"], MAN_ROWS)),
        ("a 15m path added for a non-CLASSIC5 stem in a copy", "SCOPE scope_paths()",
         lambda: scope_findings(sp + ["klines/ENAUSDT_15m.parquet"], PRE["files"], MAN_ROWS)),
        ("a path dropped from a copy of the manifest's rows", "SCOPE the manifest",
         lambda: scope_findings(sp, PRE["files"], list(MAN_ROWS)[1:])),
    ])


def scope_real():
    bad = scope_findings(D.scope_paths(), PRE["files"], MAN_ROWS)
    kinds = {"native": sum(1 for f in MAN["files"] if f["kind"] == "klines" and f["native"]),
             "derived": sum(1 for f in MAN["files"] if f["kind"] == "klines" and not f["native"]),
             "funding": sum(1 for f in MAN["files"] if f["kind"] == "funding")}
    return _ok(bad, f"scope_paths(), PRE_STATE.json, the manifest's files[] and the fixture's typed scope are, "
                    f"as sets, TC11's manifest files[].path: {len(T11_ROWS)} paths ({kinds['native']} native "
                    f"kline files, {kinds['derived']} derived, {kinds['funding']} funding tapes); the "
                    f"{len(T11_OTHER)} out-of-scope files ride along untouched (F-D-PREFIX [iii])")


# ═══════════════════════════════════════════════ F-D-FETCHPATH (offline: a temp snapshot, a stub venue)
REPLAY_T = (("BTCUSDT", "12h"), ("MNTUSDT_BYBIT", "4h"))      # one Binance file, one Bybit file, and their funding
REPLAY_RELS = tuple(f"klines/{s}_{iv}.parquet" for s, iv in REPLAY_T) + tuple(
    f"funding/{s}.parquet" for s, _ in REPLAY_T)


def added(rel: str) -> pd.DataFrame:
    """The rows of a FILED file past its PRE_STATE edge — what the venue served the builder."""
    col = "open_time" if rel.startswith("klines/") else "funding_time"
    d = frame_of(rel)
    return d[d[col] > int(PRE["files"][rel]["last_ms"])].reset_index(drop=True)


def replay_stub(extra=None, ignore_window=False) -> Stub:
    kl = {}
    for stem, iv in REPLAY_T:
        a = VEN[stem]
        key = (a["symbol"], iv if a["venue"] == "BINANCE_USDTM" else D.BYBIT_IV[iv])
        f = added(f"klines/{stem}_{iv}.parquet")
        if extra and (stem, iv) in extra:
            f = pd.concat([f, extra[(stem, iv)]], ignore_index=True).sort_values("open_time").reset_index(drop=True)
        kl[key] = f
    fu = {VEN[s]["symbol"]: added(f"funding/{s}.parquet") for s, _ in REPLAY_T}
    return Stub(klines=kl, funding=fu, ignore_window=ignore_window)


def replay_findings(extend=None, stub=None) -> list:
    """REPLAY: the fetch path run from clone-time bytes (TEMP copies of the TC11 snapshot's files)
    against a stub venue serving the rows the builder was served must reproduce the FILED content."""
    snap, out_dir = temp_snapshot(REPLAY_RELS), temp_dir("out")
    pre = pre_of(snap, REPLAY_RELS)
    first = int(KL("BTCUSDT", "4h")["open_time"].min())
    with bound(snap, stub or replay_stub()):
        for stem, iv in REPLAY_T:
            (extend or D.extend_klines)(VEN[stem], iv, PIN, out_dir, pre)
            D.extend_funding(VEN[stem], PIN, first, out_dir)
    out = []
    for rel in REPLAY_RELS:
        col, cols = ("open_time", KCOLS_T) if rel.startswith("klines/") else ("funding_time", FCOLS_T)
        got = frame_sha_t(pd.read_parquet(str(snap / rel)).sort_values(col), cols)
        if got != MAN_ROWS[rel]["content_sha"]:
            out.append(f"REPLAY {rel}: the replayed content != the filed content sha")
    out += [f"PREFIX-I {r['file']}: {r['why']}" for r in D.verify_prefixes(pre, snap) if not r["ok"]]
    return out


def resume_findings() -> tuple[list, str]:
    """RESUME: over the FILED snapshot a kline extension asks nothing and saves nothing; a funding
    tape whose edge floors to the pin's hour is skipped; the other tapes (one print short of the
    pin's hour by cadence) are re-asked — measured on TEMP copies, where the content must not move."""
    stub, out_dir = Stub(), temp_dir("resume")
    before = {rel: _stat3(D.SNAPSHOT / rel) for rel in SCOPE_T}
    out, due = [], []
    old = D.requests.get
    D.requests.get = stub
    try:
        for stem in PANEL17_T:
            for iv in lenses_t(stem):
                if iv in DERIVED_T:
                    continue
                r = D.extend_klines(VEN[stem], iv, PIN, out_dir, PRE)
                if r["fetched"] or not r["complete"]:
                    out.append(f"RESUME klines/{stem}_{iv}: fetched {r['fetched']}, complete {r['complete']}")
            if (int(FU(stem)["funding_time"].max()) // HOUR_T) * HOUR_T >= PIN_MS:
                if not D.extend_funding(VEN[stem], PIN, 0, out_dir).get("skipped"):
                    out.append(f"RESUME funding/{stem}: not skipped though its edge is in the pin's hour")
            else:
                due.append(stem)
    finally:
        D.requests.get = old
    if stub.calls:
        out.append(f"RESUME the kline resume asked the venue {len(stub.calls)} time(s)")
    moved = [rel for rel in SCOPE_T if _stat3(D.SNAPSHOT / rel) != before[rel]]
    if moved:
        out.append(f"RESUME a resume saved {len(moved)} file(s): {moved[:3]}")
    rels = [f"funding/{s}.parquet" for s in due]
    snap = temp_snapshot(rels, source=REAL)
    firsts = {s: int(KL(s, "4h")["open_time"].min()) for s in due}
    stub2 = Stub()
    with bound(snap, stub2):
        for s in due:
            D.extend_funding(VEN[s], PIN, firsts[s], out_dir)
    for rel in rels:
        got = frame_sha_t(pd.read_parquet(str(snap / rel)).sort_values("funding_time"), FCOLS_T)
        if got != MAN_ROWS[rel]["content_sha"]:
            out.append(f"RESUME {rel}: a resume against a venue with no new print moved its content")
    return out, (f"{len(PANEL17_T) - len(due)} funding tapes end in the pin's hour and are skipped; "
                 f"{len(due)} tapes of a longer cadence end one print before it and ARE re-asked by a "
                 f"resume ({len(stub2.calls)} stubbed requests on temp copies; no content moved)")


def fetch_order_findings(src: str) -> list:
    """FETCH-ORDER: run_fetch must file specs, PRE_STATE, the seam audit and the fee capture BEFORE
    the first extension, and capture the flat bars only AFTER the last one, behind `if not incomplete`."""
    fn = next(n for n in ast.parse(src).body if isinstance(n, ast.FunctionDef) and n.name == "run_fetch")
    at = {}
    for c in _calls(fn):
        at.setdefault(_name(c), []).append(c.lineno)
    ext = at.get("extend_klines", []) + at.get("extend_funding", [])
    out = []
    order = ("capture_contract_specs", "write_pre_state", "audit_inherited_rows", "capture_fee_sources")
    for a, b in zip(order, order[1:]):
        if not (at.get(a) and at.get(b) and max(at[a]) < min(at[b])):
            out.append(f"FETCH-ORDER {a} does not precede {b}")
    if not ext or not at.get("capture_fee_sources") or min(ext) < max(at["capture_fee_sources"]) \
            or min(ext) < max(at.get("write_pre_state", [0])):
        out.append("FETCH-ORDER an extension is asked before write_pre_state / the pre-fetch records")
    if not at.get("capture_flat_bar_attest") or min(at["capture_flat_bar_attest"]) < max(ext or [0]):
        out.append("FETCH-ORDER the flat-bar capture runs before the extension is complete")
    guards = [n for n in ast.walk(fn) if isinstance(n, ast.If) and ast.unparse(n.test) == "not incomplete"
              and any(_name(c) == "capture_flat_bar_attest" for c in _calls(n))]
    if not guards:
        out.append("FETCH-ORDER the flat-bar capture is not behind `if not incomplete`")
    return out


def _halt_cases() -> list:
    """Each HALT of the fetch path, fired offline on temp copies (rows for `plants`)."""
    rel = "klines/BTCUSDT_12h.parquet"
    a, y = VEN["BTCUSDT"], VEN["MNTUSDT_BYBIT"]
    step = STEP_T["12h"]

    def run(rels, pre_edit=None, stub=None, call=None):
        snap, out_dir = temp_snapshot(rels), temp_dir("out")
        pre = pre_of(snap, rels)
        if pre_edit:
            pre_edit(pre)
        with bound(snap, stub or replay_stub()):
            call(out_dir, pre, snap)
        return []

    def early(pre):
        pre["files"][rel]["last_ms"] += step

    off = added(rel).copy()
    off["open_time"] = off["open_time"] + 1
    off_stub = Stub(klines={("BTCUSDT", "12h"): off})

    def bybit15(out_dir, pre, snap):
        shutil.copy(snap / rel, snap / "klines" / "MNTUSDT_BYBIT_15m.parquet")
        pre["files"]["klines/MNTUSDT_BYBIT_15m.parquet"] = pre["files"][rel]
        D.extend_klines(y, "15m", PIN, out_dir, pre)

    info = {"symbols": [dict(s["venue_object"], status="BREAK") if s["stem"] == "ETHUSDT" else s["venue_object"]
                        for s in SPECS["assets"] if s["venue"] == "BINANCE_USDTM"]}
    yinfo = [s["venue_object"] for s in SPECS["assets"] if s["venue"] != "BINANCE_USDTM"]

    def moved_since_clone(out_dir, pre, snap):
        first = D.scope_paths()[0]
        doc = copy.deepcopy(ATTEST)
        doc["files"][first]["sha256"] = "0" * 64
        (out_dir / "CLONE_ATTEST.json").write_text(json.dumps(doc), encoding="utf-8")
        D.write_pre_state(PIN, out_dir)

    return [
        ("the kline file absent from the temp snapshot", "absent or not in PRE_STATE",
         lambda: run([], call=lambda o, p, s: D.extend_klines(a, "12h", PIN, o, p))),
        ("the file present and not in PRE_STATE", "absent or not in PRE_STATE",
         lambda: run([rel], pre_edit=lambda p: p["files"].clear(),
                     call=lambda o, p, s: D.extend_klines(a, "12h", PIN, o, p))),
        ("a PRE_STATE edge at the first stamp asked for (an early start)", "is not past the PRE_STATE edge",
         lambda: run([rel], pre_edit=early, call=lambda o, p, s: D.extend_klines(a, "12h", PIN, o, p))),
        ("an off-grid stamp served by the stub venue", "off-grid",
         lambda: run([rel], stub=off_stub, call=lambda o, p, s: D.extend_klines(a, "12h", PIN, o, p))),
        ("a Bybit 15m extension", "Bybit serves no 15m", lambda: run([rel], call=bybit15)),
        ("the funding tape absent from the temp snapshot", "is absent",
         lambda: run([], call=lambda o, p, s: D.extend_funding(a, PIN, 0, o))),
        ("a symbol of record served not TRADING by the stub venue", "not TRADING at the TC12 capture",
         lambda: run([], stub=Stub(info=info, bybit_info=yinfo),
                     call=lambda o, p, s: D.capture_contract_specs(o, PIN))),
        ("a file moved between the clone and PRE_STATE", "moved between the clone and PRE_STATE",
         lambda: run([D.scope_paths()[0]], call=moved_since_clone)),
    ]


def fetchpath_break():
    overlap = shadow("extend_klines", "    cursor = edge + step\n", "    cursor = edge\n")
    blind = shadow("extend_klines", "    cursor = edge + step\n", "    cursor = edge\n", src=mut(
        SRC_TEXT, "    if cursor <= pre[\"files\"][rel][\"last_ms\"]:\n"
        "        raise SystemExit(f\"HALT: {rel}: first stamp {iso(cursor)} is not past the PRE_STATE edge \"\n"
        "                         f\"{iso(pre['files'][rel]['last_ms'])} — an early start would overwrite\")\n", ""))
    edge = {}
    for stem, iv in REPLAY_T:                       # a venue that now serves ANOTHER bar at the edge stamp
        e = frame_of(f"klines/{stem}_{iv}.parquet")
        e = e[e["open_time"] == int(PRE["files"][f"klines/{stem}_{iv}.parquet"]["last_ms"])].copy()
        e["close"] = e["close"] + 1.0
        edge[(stem, iv)] = e
    rows = _halt_cases() + [
        ("a copy of extend_klines whose cursor is the edge (a one-bar overlap)", "is not past the PRE_STATE edge",
         lambda: replay_findings(extend=overlap)),
        ("that mutant with its HALT removed, against a stub venue serving another bar at the edge stamp",
         "old-prefix content sha moved", lambda: replay_findings(extend=blind, stub=replay_stub(extra=edge))),
        ("a copy of run_fetch that fetches before write_pre_state", "FETCH-ORDER an extension is asked before",
         lambda: fetch_order_findings(mut(SRC_TEXT, "    pre = write_pre_state(pin, out)\n",
                                          "    extend_klines(panel_assets()[0], \"4h\", pin, out, {})\n"
                                          "    pre = write_pre_state(pin, out)\n"))),
        ("a copy of run_fetch that captures the flat bars before the 5m extension",
         "FETCH-ORDER the flat-bar capture runs before",
         lambda: fetch_order_findings(mut(SRC_TEXT, "        for iv in (FIFTEEN, \"5m\"):\n",
                                          "        capture_flat_bar_attest(pin, pre, out)\n"
                                          "        for iv in (FIFTEEN, \"5m\"):\n"))),
    ]
    return plants(rows)


def fetchpath_real():
    bad = replay_findings() + fetch_order_findings(SRC_TEXT)
    res, note = resume_findings()
    return _ok(bad + res, (
        f"offline, the module bound to TEMP snapshots and a stub venue: the fetch path replayed from "
        f"clone-time bytes of {list(REPLAY_RELS)} (one Binance and one Bybit kline file, their funding tapes) "
        f"reproduces the FILED content shas and moves no inherited row; a kline resume over the FILED "
        f"snapshot ({sum(1 for r in SCOPE_T if r.startswith('klines/') and lens_of(r)[1] not in DERIVED_T)} "
        f"native files) asks the venue nothing and saves nothing; {note}; run_fetch files the specs, "
        f"PRE_STATE, the seam audit and the fee capture before the first extension and captures the flat "
        f"bars only after the last one, behind `if not incomplete`"))


# ═══════════════════════════════════════════════ F-D-FORMING
def forming_findings(extend=None) -> list:
    """FORMING: a stub page holding one bar with open_time = the lens's target + one step must not
    reach the TEMP snapshot (G2: the reply is filtered to [lo, hi] before any save)."""
    rels = [f"klines/{s}_{iv}.parquet" for s, iv in REPLAY_T]
    snap, out_dir = temp_snapshot(rels), temp_dir("out")
    pre = pre_of(snap, rels)
    extra = {}
    for stem, iv in REPLAY_T:
        last = added(f"klines/{stem}_{iv}.parquet").tail(1).copy()
        last["open_time"] = target_t(iv, PIN_MS) + STEP_T[iv]
        extra[(stem, iv)] = last
    with bound(snap, replay_stub(extra=extra, ignore_window=True)):
        for stem, iv in REPLAY_T:
            (extend or D.extend_klines)(VEN[stem], iv, PIN, out_dir, pre)
    out = []
    for (stem, iv), rel in zip(REPLAY_T, rels):
        d = pd.read_parquet(str(snap / rel))
        if int(d["open_time"].max()) > target_t(iv, PIN_MS):
            out.append(f"FORMING {rel}: a row past the pin was saved ({VEN[stem]['venue']})")
        elif frame_sha_t(d.sort_values("open_time"), KCOLS_T) != MAN_ROWS[rel]["content_sha"]:
            out.append(f"FORMING {rel}: the saved content != the filed content")
    return out


def _clock(binance: int, bybit: int):
    with bound(temp_snapshot([]), Stub(binance_clock=binance, bybit_clock=bybit)):
        D.record_fetch_clock(temp_dir("out"), PIN)
    return []


def forming_break():
    nofilter = shadow("extend_klines",
                      "        df = df[(df[\"open_time\"] >= lo) & (df[\"open_time\"] <= hi)]\n", "")
    return plants([
        ("a copy of extend_klines with the [lo, hi] filter deleted", "a row past the pin was saved",
         lambda: forming_findings(extend=nofilter)),
        ("a stub Binance clock at the pin", "clock is not past the pin", lambda: _clock(PIN_MS, PIN_MS + HOUR_T)),
        ("a stub Bybit clock at the pin", "clock is not past the pin", lambda: _clock(PIN_MS + HOUR_T, PIN_MS)),
    ])


def forming_real():
    bad = forming_findings()
    try:
        _clock(PIN_MS + HOUR_T, PIN_MS + HOUR_T)
    except SystemExit as e:
        bad.append(f"FORMING a venue clock past the pin was refused: {scrub(str(e))}")
    return _ok(bad, "a stub Binance page and a stub Bybit page that each serve one bar opening at the lens's "
                    "target + one step (whatever window is asked): production saves nothing past the "
                    "target and the saved content is the filed content; record_fetch_clock admits venue "
                    "clocks past the pin and HALTs on a clock at the pin")


# ═══════════════════════════════════════════════ F-D-VENUE
def venue_faults(man: dict, fetch_rows: list, names: list) -> list:
    """VENUE-FILE / VENUE-SPLICE / VENUE-TWIN / VENUE-HOST — "never spliced" = one venue per tape."""
    out = []
    v_by_stem = {v["stem"]: v["venue"] for v in man["venues"] if v["stem"]}
    sym = {v["stem"]: v["symbol"] for v in man["venues"] if v["stem"]}
    host = {"BINANCE_USDTM": "BINANCE", "BYBIT_V5_LINEAR": "BYBIT"}
    for f in man["files"]:
        if f["venue"] != v_by_stem.get(f["stem"]):
            out.append(f"VENUE-FILE {f['path']}: venue {f['venue']} != its asset's {v_by_stem.get(f['stem'])}")
    by_host = {h: {sym[s] for s, v in v_by_stem.items() if host[v] == h} for h in host.values()}
    for r in fetch_rows:
        if r.get("kind") in ("klines", "funding") and r["venue"] != v_by_stem.get(r["stem"]):
            out.append(f"VENUE-SPLICE FETCH_LOG: {r['stem']} {r.get('iv', 'funding')} fetched from {r['venue']}")
        if r.get("kind") == "http" and r.get("phase") in ("fetch", "edge_audit", "flat_attest"):
            ep, h, s = r.get("endpoint", ""), r.get("venue"), (r.get("params") or {}).get("symbol")
            archive = r["phase"] == "flat_attest" and h == "BINANCE" and ep.startswith(ARCHIVE_PREFIX_T)
            if h not in REST_ENDPOINTS_T or not (ep in REST_ENDPOINTS_T[h] or archive):
                out.append(f"VENUE-HOST FETCH_LOG: phase {r['phase']} asked {h} {ep}")
            elif s is not None and s not in by_host[h]:
                out.append(f"VENUE-HOST FETCH_LOG: {h} was asked for {s}, not a symbol of record on that venue")
            elif archive and not any(f"/{x}/" in ep for x in by_host[h]):
                out.append(f"VENUE-HOST FETCH_LOG: the archive was asked for another symbol: {ep}")
    for stem, venue in v_by_stem.items():
        if venue != "BINANCE_USDTM":
            if not stem.endswith(D.BYBIT_STEM_SUFFIX):
                out.append(f"VENUE-TWIN {stem}: an alternate venue without the venue in its file stem")
            twin = stem[:-len(D.BYBIT_STEM_SUFFIX)]
            clash = [n for n in names if (n.startswith(twin + "_") or n == twin + ".parquet")
                     and not n.startswith(stem)]
            if clash:
                out.append(f"VENUE-TWIN {twin}: a default-named file beside the alternate tape: {clash}")
    return out


def snapshot_names() -> list:
    return sorted(q.name for sub in ("klines", "funding") for q in (D.SNAPSHOT / sub).glob("*.parquet"))


def venue_break():
    probe = jload(D.TC10_PROBE)
    bent = copy.deepcopy(probe)
    bent["unseen12"][0]["venue"] = "BYBIT_V5_LINEAR"
    return plants([
        ("a default-named twin MNTUSDT_4h.parquet in a COPY of the snapshot listing", "VENUE-TWIN MNTUSDT",
         lambda: venue_faults(MAN, FETCH_ROWS, snapshot_names() + ["MNTUSDT_4h.parquet"])),
        ("a FETCH_LOG row for MNT's stem from the other venue in a COPY", "VENUE-SPLICE",
         lambda: venue_faults(MAN, FETCH_ROWS + [{"kind": "klines", "stem": "MNTUSDT_BYBIT", "iv": "5m",
                                                  "venue": "BINANCE_USDTM"}], snapshot_names())),
        ("an HTTP row of the fetch phase asking Bybit for a Binance symbol in a COPY", "VENUE-HOST",
         lambda: venue_faults(MAN, FETCH_ROWS + [{"kind": "http", "phase": "fetch", "venue": "BYBIT",
                                                  "endpoint": "/v5/market/kline",
                                                  "params": {"symbol": "BTCUSDT"}}], snapshot_names())),
        ("one flipped `venue` in a COPY of the probe", "table / probe / manifest disagree",
         lambda: [f"VENUE-AGREE {x}" for x in D.venue_agreement(probe=bent)]),
    ])


def venue_real():
    bad = [f"VENUE-AGREE {x}" for x in D.venue_agreement()] + venue_faults(MAN, FETCH_ROWS, snapshot_names())
    table = D.stage_d_table()
    if [r["stem"] for r in table] != list(PANEL17_T):
        bad.append("VENUE-AGREE the table's stems are not the commission's seventeen in order")
    alt = {v["asset"]: v["venue"] for v in MAN["venues"] if v["venue"] != "BINANCE_USDTM"}
    n_http = sum(1 for r in FETCH_ROWS if r.get("kind") == "http" and r.get("phase") in (
        "fetch", "edge_audit", "flat_attest"))
    return _ok(bad, f"TC10's Stage D table, TC10's VENUE_PROBE.json (its sha the one two tracked TC11 records "
                    f"carry) and TC11's manifest venues[] agree row for row, {len(table)} of {len(table)}; "
                    f"every in-scope file's venue is its asset's; alternate venues: {alt}; "
                    f"{sum(1 for r in FETCH_ROWS if r.get('kind') in ('klines', 'funding'))} klines/funding log "
                    f"rows and {n_http} HTTP rows of the fetch, seam-audit and attestation phases each went to "
                    f"the stem's own venue (its REST endpoints; the bulk archive only in the attestation "
                    f"phase, for Binance symbols); no default-named twin of the alternate tape exists")


# ═══════════════════════════════════════════════ F-D-MANIFEST / F-D-SEAL
def manifest_findings(man: dict, md: str, rehash: bool = True) -> list:
    """MANIFEST-KEYS / MANIFEST-SHA / MANIFEST-MD."""
    out = []
    want = {RENAME_TOP_T.get(k, k) for k in T11_MAN} | set(NEW_TOP_T)
    if set(man) != want:
        return [f"MANIFEST-KEYS top level: missing {sorted(want - set(man))}, extra {sorted(set(man) - want)}"]
    for f in man["files"]:
        ref = {RENAME_ROW_T.get(k, k) for k in T11_ROWS[f["path"]]} if f["path"] in T11_ROWS else None
        if ref is None or set(f) != ref:
            out.append(f"MANIFEST-KEYS row {f['path']}: its key set is not TC11's under the rename table")
    if rehash:
        for f in man["files"] + man["out_of_scope_snapshot_files"]:
            q = D.SNAPSHOT / f["path"]
            if not q.is_file() or sha_f(q) != f["sha256"] or q.stat().st_size != f["bytes"]:
                out.append(f"MANIFEST-SHA {f['path']}: the filed sha / bytes do not re-hash")
        ptr = [("contract_multipliers.artifact_sha256", man["contract_multipliers"]["artifact_sha256"],
                sha_f(OUT / "CONTRACT_SPECS.json")),
               ("clone_attestation.artifact_sha256", man["clone_attestation"]["artifact_sha256"],
                sha_f(OUT / "CLONE_ATTEST.json")),
               ("inherited_edge_audit.artifact_sha256", man["inherited_edge_audit"]["artifact_sha256"],
                sha_f(OUT / "EDGE_AUDIT.json")),
               ("tc11_record.manifest.sha256", man["tc11_record"]["manifest"]["sha256"], sha_b(T11_MAN_BYTES)),
               ("carried_from_tc11.manifest_sha256", man["carried_from_tc11"]["manifest_sha256"],
                sha_b(T11_MAN_BYTES)),
               ("tc10_record.venue_probe.sha256", man["tc10_record"]["venue_probe"]["sha256"],
                sha_f(D.TC10_PROBE))]
        ptr += [(f"write_once.sealed_sha256[{n}]", man["write_once"]["sealed_sha256"].get(n), sha_f(OUT / n))
                for n in SEALED_T]
        ptr += [(f"fee_sources[{v}].record.sha256", s["record"]["sha256"], sha_f(OUT / "FEE_SOURCE.json"))
                for v, s in man["fee_sources"].items()]
        out += [f"MANIFEST-SHA {k}: the filed sha does not re-hash" for k, a, b in ptr if a != b]
        for k in D.CARRIED_KEYS:
            if man.get(k) != T11_MAN.get(k):
                out.append(f"MANIFEST-SHA {k}: the carried block is not TC11's block verbatim")
    if md != D.manifest_md(man, FEES, AUDIT):
        out.append("MANIFEST-MD the .md is not the document the .json renders to")
    lines = {x.split(" | ")[0][2:]: x for x in md.split("\n") if x.startswith("| klines/") or x.startswith("| funding/")}
    for f in man["files"]:
        line = lines.get(f["path"], "")
        if f"| {f['rows']} |" not in line or f["sha256"][:16] not in line:
            out.append(f"MANIFEST-MD {f['path']}: its .md row does not carry the .json's rows and sha")
    return out


def manifest_break():
    md = (OUT / "STAGE_D_MANIFEST.md").read_text(encoding="utf-8")
    row = copy.deepcopy(MAN)
    row["files"][0]["sha256"] = "0" * 64
    probe = MAN_ROWS["klines/BTCUSDT_4h.parquet"]
    return plants([
        ("a key dropped from a COPY of the manifest", "MANIFEST-KEYS top level",
         lambda: manifest_findings({k: v for k, v in MAN.items() if k != "zero_volume_bars"}, md, rehash=False)),
        ("a row key renamed back in a COPY (tc11_rows_added)", "MANIFEST-KEYS row",
         lambda: manifest_findings(dict(MAN, files=[{("tc11_rows_added" if k == "tc12_rows_added" else k): v
                                                     for k, v in MAN["files"][0].items()}] + MAN["files"][1:]),
                                   md, rehash=False)),
        ("a row's sha altered in a COPY", "MANIFEST-SHA", lambda: manifest_findings(row, md)),
        ("one figure changed in a COPY of the .md", "MANIFEST-MD",
         lambda: manifest_findings(MAN, mut(md, f"| klines/BTCUSDT_4h.parquet | {probe['rows']} |",
                                            f"| klines/BTCUSDT_4h.parquet | {probe['rows'] + 1} |"), rehash=False)),
    ])


def manifest_real():
    md = (OUT / "STAGE_D_MANIFEST.md").read_text(encoding="utf-8")
    bad = manifest_findings(MAN, md)
    if MAN["complete"] is not True:
        bad.append("MANIFEST-KEYS `complete` is not True")
    return _ok(bad, f"{len(MAN)} top-level keys = TC11's {len(T11_MAN)} under the renames {RENAME_TOP_T} plus "
                    f"{list(NEW_TOP_T)}; every row's key set is TC11's row's under {RENAME_ROW_T}; "
                    f"{len(MAN['files'])} in-scope and {len(MAN['out_of_scope_snapshot_files'])} out-of-scope "
                    f"snapshot files re-hash to their filed sha and bytes; the record pointers (specs, clone "
                    f"attestation, seam audit, the seven sealed records, TC11's manifest, the probe, the fee "
                    f"source) re-hash; the three carried blocks are TC11's verbatim; the .md is the document "
                    f"the .json renders to; complete = {MAN['complete']}")


def seal_findings(root: Path) -> list:
    out = [f"SEAL-MOVED {x}" for x in D.verify_seal(OUT, root)]
    if set(SEAL["files"]) != set(SEALED_T):
        out.append(f"SEAL-SET the seal pins {sorted(SEAL['files'])}, not the seven")
    lines = (root / "FETCH_LOG.jsonl").read_text(encoding="utf-8").splitlines()
    n = SEAL["fetch_log"]["sealed_lines"]
    if sha_b(("\n".join(lines[:n]) + "\n").encode("utf-8")) != SEAL["fetch_log"]["sha256_of_sealed_lines"]:
        out.append("SEAL-MOVED FETCH_LOG.jsonl: the sealed line prefix does not re-hash (the fixture's own hash)")
    for name in SEALED_T:
        if (root / name).is_file() and sha_f(root / name) != SEAL["files"].get(name, {}).get("sha256"):
            out.append(f"SEAL-MOVED {name}: not the bytes the seal pinned (the fixture's own hash)")
    return out


def _seal_copy(name: str, edit) -> list:
    tmp = temp_dir("seal")
    for n in SEALED_T + ("FETCH_LOG.jsonl",):
        shutil.copy(OUT / n, tmp / n)
    (tmp / name).write_text(edit((tmp / name).read_text(encoding="utf-8")), encoding="utf-8")
    return seal_findings(tmp)


def seal_break():
    return plants([
        ("a sealed record rewritten in a temp copy (PRE_STATE.json)", "bytes moved since the seal",
         lambda: _seal_copy("PRE_STATE.json", lambda t: t.replace("TIER-C12", "TIER-C13"))),
        ("a sealed line of the fetch log changed in a temp copy", "a sealed line changed",
         lambda: _seal_copy("FETCH_LOG.jsonl", lambda t: t.replace('"status": 200', '"status": 201', 1))),
        ("the fee-source capture rewritten in a temp copy", "bytes moved since the seal",
         lambda: _seal_copy("FEE_SOURCE.json", lambda t: t.replace("202", "200"))),
    ])


def seal_real():
    return _ok(seal_findings(OUT),
               f"the seven sealed provenance records {list(SEALED_T)} are the bytes WRITE_ONCE_SEAL.json pinned, "
               f"and the first {SEAL['fetch_log']['sealed_lines']} lines of FETCH_LOG.jsonl hash to the sealed "
               f"line prefix (production's verifier and the fixture's own hashes)")


# ═══════════════════════════════════════════════ F-D-PREFIX [i] … [iv]
_T11: dict = {}


def t11_frame(rel: str) -> pd.DataFrame:
    """A file of the TC11 snapshot, read by explicit absolute path in this plain process (read-only)."""
    if rel not in _T11:
        col = "open_time" if rel.startswith("klines/") else "funding_time"
        _T11[rel] = pd.read_parquet(str(D.TC11_SNAPSHOT / rel)).sort_values(col).reset_index(drop=True)
    return _T11[rel]


def prefix_cut(rel: str, df: pd.DataFrame, raw_stamp: bool = False) -> pd.DataFrame:
    """The rows with CLOSE <= TC11's pin: a kline by open + step, a funding print by its FLOOR HOUR."""
    if rel.startswith("klines/"):
        return df[df["open_time"] + STEP_T[lens_of(rel)[1]] <= T11_PIN_MS]
    if raw_stamp:
        return df[df["funding_time"] <= T11_PIN_MS]
    return df[(df["funding_time"] // HOUR_T) * HOUR_T <= T11_PIN_MS]


def prefix_i_findings(pre: dict, root=None) -> list:
    return [f"PREFIX-I {r['file']}: prefix rows {r.get('prefix_rows_now')} vs the old {r.get('old_rows')}; "
            f"{r['why']}" for r in D.verify_prefixes(pre, root) if not r["ok"]]


def prefix_ii_findings(rel: str, df12: pd.DataFrame) -> list:
    cols = KCOLS_T if rel.startswith("klines/") else FCOLS_T
    col = cols[0]
    pref, ref, row = prefix_cut(rel, df12.sort_values(col)), t11_frame(rel), T11_ROWS[rel]
    if len(pref) != row["rows"] or len(pref) != len(ref):
        return [f"PREFIX-II {rel}: prefix rows {len(pref)} != TC11's {row['rows']}"]
    sha = frame_sha_t(pref, cols)
    if sha != frame_sha_t(ref, cols) or sha != row["content_sha"]:
        return [f"PREFIX-II {rel}: the content sha of the prefix is not the TC11 file's / TC11's manifest's"]
    return []


def prefix_iii_findings(root: Path = D.SNAPSHOT, only=None) -> list:
    out = []
    for rel in (only or sorted(T11_OTHER)):
        q = root / rel
        if not q.is_file() or sha_f(q) != T11_OTHER[rel]["sha256"]:
            out.append(f"PREFIX-III {rel}: an out-of-scope file's sha != TC11's manifest")
    if only is None:
        have, want = set(D.tree_files(root)), set(T11_ROWS) | set(T11_OTHER)
        if have != want:
            out.append(f"PREFIX-III the snapshot's file set: stray {sorted(have - want)[:3]}, missing "
                       f"{sorted(want - have)[:3]}")
    return out


def atpin_findings(stem: str, df12: pd.DataFrame, raw_stamp: bool = False) -> tuple[list, int]:
    rel = f"funding/{stem}.parquet"
    pref = prefix_cut(rel, df12, raw_stamp)
    hour = (pref["funding_time"] // HOUR_T) * HOUR_T
    at, last = pref[hour == T11_PIN_MS], t11_frame(rel).tail(1)
    if len(at) != 1 or int(at["funding_time"].iloc[0]) != int(last["funding_time"].iloc[0]) \
            or float(at["funding_rate"].iloc[0]) != float(last["funding_rate"].iloc[0]):
        return [f"PREFIX-IV {stem}: at-pin print missing or not the last row of TC11's file "
                f"({len(at)} row(s) of TC11's pin hour in the prefix)"], 0
    rest = df12[~df12.index.isin(pref.index)]
    if len(rest) and int((rest["funding_time"].min() // HOUR_T) * HOUR_T) <= T11_PIN_MS:
        return [f"PREFIX-IV {stem}: the first row after the prefix is not of a later hour"], 0
    return [], int(int(at["funding_time"].iloc[0]) > T11_PIN_MS)


def prefix_legs() -> list:
    b4, bf = KL("BTCUSDT", "4h"), FU("BTCUSDT")
    rel4, relf = "klines/BTCUSDT_4h.parquet", "funding/BTCUSDT.parquet"

    def ulp():
        d = b4.copy()
        d.loc[d.index[100], "close"] = np.nextafter(d["close"].iloc[100], np.inf)
        return prefix_ii_findings(rel4, d)

    def inserted_ii():
        d = b4.copy()
        row = d.iloc[[100]].copy()
        row["open_time"] = row["open_time"] + HOUR_T
        return prefix_ii_findings(rel4, pd.concat([d, row], ignore_index=True))

    def before_first():
        d = b4.copy()
        row = d.iloc[[0]].copy()
        row["open_time"] = row["open_time"] - STEP_T["4h"]
        return prefix_ii_findings(rel4, pd.concat([row, d], ignore_index=True))

    def inserted_i():
        tmp = temp_dir("prefix")
        (tmp / "funding").mkdir()
        d = bf.copy()
        row = d.iloc[[100]].copy()
        row["funding_time"] = row["funding_time"] + HOUR_T
        pd.concat([d, row], ignore_index=True).sort_values("funding_time").to_parquet(tmp / relf, index=False)
        return prefix_i_findings({"files": {relf: PRE["files"][relf]}}, tmp)

    def flipped():
        rel = "funding/TAOUSDT.parquet"
        tmp = temp_dir("oos")
        (tmp / "funding").mkdir()
        raw = bytearray((D.SNAPSHOT / rel).read_bytes())
        raw[len(raw) // 2] ^= 1
        (tmp / rel).write_bytes(bytes(raw))
        return prefix_iii_findings(tmp, only=[rel])

    def iv_real():
        bad, late = [], 0
        for stem in PANEL17_T:
            f, n = atpin_findings(stem, FU(stem))
            bad, late = bad + f, late + n
        haz = T11_MAN["as_of_hazards"]["funding_files_with_a_print_stamped_after_the_as_of_close"]
        if late != len(haz):
            bad.append(f"PREFIX-IV {late} tapes hold the at-pin print stamped after TC11's pin; TC11's manifest "
                       f"lists {len(haz)}")
        return _ok(bad, f"each of the {len(PANEL17_T)} funding prefixes (cut on the FLOOR HOUR) holds exactly "
                        f"one row of TC11's pin hour, bit-identical (stamp and rate) to the last row of the "
                        f"TC11 file; on {late} tapes that stamp is past TC11's pin instant (the hazard list of "
                        f"TC11's manifest, {len(haz)}); the first row after every prefix is of a later hour")

    return [
        ("F-D-PREFIX [i]", "the rows at or before each file's OLD last stamp hash to the OLD content sha",
         "a row inserted behind the old edge of a temp copy of one file",
         "for any of the 124 in-scope files the rows at or before its PRE_STATE edge, read back from the "
         "current file, do not hash to its PRE_STATE content sha",
         lambda: plants([("a row inserted behind the old edge (temp copy of funding/BTCUSDT.parquet)",
                          "prefix rows", inserted_i)]),
         lambda: _ok(prefix_i_findings(PRE), f"verify_prefixes over PRE_STATE.json: {len(PRE['files'])} files, "
                                             f"every old prefix re-hashes to its old content sha")),
        ("F-D-PREFIX [ii]", "THE BYTE REFEREE: the TC12 prefix == the WHOLE TC11 snapshot file",
         "a one-ulp change of one historical close; a row inserted behind the old edge; a bar manufactured "
         "before the tape's first bar",
         "for any in-scope file the rows with close <= TC11's pin are not, in number, stamps and raw column "
         "bytes, the whole TC11 snapshot file (read by absolute path) and TC11's manifest content sha; or "
         "the TC11 file is not its manifest's bytes",
         lambda: plants([
             ("a one-ulp change of one historical close in a frame copy", "content sha", ulp),
             ("a row inserted behind the old edge in a frame copy", "prefix rows", inserted_ii),
             ("a bar manufactured BEFORE the tape's first bar in a frame copy", "prefix rows", before_first),
         ]),
         lambda: _ok([x for rel in SCOPE_T for x in prefix_ii_findings(rel, frame_of(rel))]
                     + [f"PREFIX-II {rel}: the TC11 file is not its manifest's bytes" for rel in SCOPE_T
                        if sha_f(D.TC11_SNAPSHOT / rel) != T11_ROWS[rel]["sha256"]],
                     f"{len(SCOPE_T)} in-scope files: the rows with close <= TC11's pin (a kline by open + step, "
                     f"a funding print by its floor hour) are, by row count and by the fixture's own content "
                     f"sha, the whole TC11 snapshot file and TC11's manifest content_sha; every TC11 file "
                     f"re-hashes to TC11's manifest (the derived 1d/1w files included)")),
        ("F-D-PREFIX [iii]", "the out-of-scope files ride along untouched; no stray file, none missing",
         "one byte flipped in a temp copy of an out-of-scope file",
         "an out-of-scope file's sha != TC11's manifest out_of_scope_snapshot_files[].sha256, or the file "
         "set of the TC12 snapshot != the union of TC11's two lists",
         lambda: plants([("one byte flipped in a temp copy of an out-of-scope file", "PREFIX-III", flipped)]),
         lambda: _ok(prefix_iii_findings(), f"{len(T11_OTHER)} out-of-scope files hash to TC11's manifest; the "
                                            f"snapshot holds exactly TC11's {len(T11_ROWS)} + {len(T11_OTHER)} "
                                            f"paths")),
        ("F-D-PREFIX [iv]", "THE AT-PIN PRINT: one print of TC11's pin hour in every funding prefix",
         "the raw-stamp cut applied to a tape copy (it drops the at-pin print)",
         "a funding prefix does not hold exactly one row of TC11's pin hour bit-identical to the last row of "
         "TC11's file; the count of tapes where that stamp is past TC11's pin != TC11's hazard list; or the "
         "first row after the prefix is not of a later hour",
         lambda: plants([("the raw-stamp cut applied to a copy of BTC's tape", "at-pin print missing",
                          lambda: atpin_findings("BTCUSDT", bf.copy(), raw_stamp=True)[0])]),
         iv_real),
    ]


# ═══════════════════════════════════════════════ F-D-2 [1] … [4]
FX10_TEXT = (ROOT / "scripts" / "tierc10_data_fixtures.py").read_text(encoding="utf-8")
BANNED_T = tuple(FX.literal_from_text(FX10_TEXT, "BANNED_TOKENS"))        # FX10's, read by AST
FETCH_PATH_T = ("engine/data.py", "scripts/tierc12_data.py")
KFILES = [(s, iv) for s in PANEL17_T for iv in lenses_t(s)]


def code_only(src: str) -> str:
    """AST round trip: comments gone, docstrings stripped, string literals KEPT (FX10's idiom)."""
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
            b = node.body
            if b and isinstance(b[0], ast.Expr) and isinstance(getattr(b[0], "value", None), ast.Constant) \
                    and isinstance(b[0].value.value, str):
                node.body = b[1:] or [ast.Pass()]
    return ast.unparse(tree)


def token_findings(sources: dict) -> list:
    return [f"FILL-TOKEN {name}: '{tok}'" for name, src in sources.items()
            for tok in BANNED_T if tok in code_only(src)]


def grid_findings(rel: str, df: pd.DataFrame) -> list:
    """Independent of scan_klines: plain diff / mod on the stamps."""
    iv = lens_of(rel)[1]
    t = df["open_time"].to_numpy(np.int64)
    out = []
    if ((t - anchor_t(iv)) % STEP_T[iv] != 0).any():
        out.append(f"GRID {rel}: {int(((t - anchor_t(iv)) % STEP_T[iv] != 0).sum())} off-grid")
    if len(t) > 1 and (np.diff(t) <= 0).any():
        out.append(f"GRID {rel}: {int((np.diff(t) <= 0).sum())} duplicate/backward")
    return out


def flat0(df: pd.DataFrame) -> np.ndarray:
    o, h, l, c, v = (df[k].to_numpy(np.float64) for k in KCOLS_T[1:])
    return (o == h) & (h == l) & (l == c) & (v == 0)


def recount_findings(rel: str, df: pd.DataFrame) -> list:
    n, filed = int(flat0(df).sum()), MAN_ROWS[rel]["venue_zero_volume_flat_bars"]
    return [] if n == filed else [f"FLAT-RECOUNT {rel}: recount != manifest ({n} vs {filed})"]


def carried_forward(df: pd.DataFrame, k: int) -> pd.DataFrame:
    """A COPY with a carried-forward flat bar (the previous close four times, volume 0) at row k."""
    d = df.copy()
    prev = float(d["close"].iloc[k - 1])
    d.loc[d.index[k], ["open", "high", "low", "close", "volume"]] = [prev] * 4 + [0.0]
    return d


def flat_expected(frames=None) -> dict:
    """The fixture's OWN two populations: (a) its own seeded draw on its own stream of the same
    expression; (b) its own recount of the rows past each PRE_STATE edge."""
    get = lambda s, iv: (frames or {}).get((s, iv), KL(s, iv))            # noqa: E731
    rng = FX.stream(np, SEED, TAG, "F-D-2 [4]")
    want: dict = {}
    for stem in PANEL17_T:
        for iv in lenses_t(stem):
            if iv in DERIVED_T:
                continue
            df = get(stem, iv)
            t, z = df["open_time"].to_numpy(np.int64), flat0(df)
            if iv == "5m" and z.any():
                for x in rng.choice(t[z], size=min(FLAT_N_T, int(z.sum())), replace=False):
                    want.setdefault((stem, iv, int(x)), set()).add("a")
            edge = int(PRE["files"][f"klines/{stem}_{iv}.parquet"]["last_ms"])
            for x in t[z & (t > edge)]:
                want.setdefault((stem, iv, int(x)), set()).add("b")
    return want


def flat_attest_findings(record: dict, frames=None, sealed: bool = True) -> list:
    get = lambda s, iv: (frames or {}).get((s, iv), KL(s, iv))            # noqa: E731
    want = flat_expected(frames)
    have = {(b["stem"], b["lens"], int(b["open_ms"])): b for b in record["bars"]}
    out = [f"FLAT-ATTEST {k[0]} {k[1]} {D.iso(k[2])}: absent from the sealed record"
           for k in sorted(set(want) - set(have))]
    out += [f"FLAT-ATTEST {k[0]} {k[1]} {D.iso(k[2])}: the record holds a bar outside the two populations"
            for k in sorted(set(have) - set(want))]
    for k in sorted(set(want) & set(have)):
        b = have[k]
        df = get(k[0], k[1])
        tape = df[df["open_time"] == k[2]].iloc[0]
        venue = b["archive_row"] if b["publication"] == "archive-only" else b["rest_row"]
        if set(b["populations"]) != want[k]:
            out.append(f"FLAT-ATTEST {k[0]} {k[1]} {D.iso(k[2])}: populations {b['populations']} != {sorted(want[k])}")
        if b["publication"] == "neither":
            out.append(f"FLAT-ATTEST {k[0]} {k[1]} {D.iso(k[2])}: publication is `neither`")
        elif venue is None or any(float(venue[i]) != float(tape[c]) for i, c in enumerate(KCOLS_T[1:])):
            out.append(f"FLAT-ATTEST {k[0]} {k[1]} {D.iso(k[2])}: a field differs from its sealed venue row")
    if sealed and SEAL["files"]["FLAT_BAR_ATTEST.json"]["sha256"] != sha_f(OUT / "FLAT_BAR_ATTEST.json"):
        out.append("FLAT-ATTEST the record moved since the seal")
    return out


def fd2_legs() -> list:
    b1 = KL("BTCUSDT", "1h")
    rel1 = "klines/BTCUSDT_1h.parquet"
    srcs = {rel: (ROOT / rel).read_text(encoding="utf-8") for rel in FETCH_PATH_T}

    def offgrid():
        row = b1.iloc[[100]].copy()
        row["open_time"] = row["open_time"] + HOUR_T // 2
        return grid_findings(rel1, pd.concat([b1, row]).sort_values("open_time"))

    def added_flat():
        k = len(b1) - 5                                           # a row past the PRE_STATE edge
        return flat_attest_findings(FLAT, frames={("BTCUSDT", "1h"): carried_forward(b1, k)})

    def field():
        rec = copy.deepcopy(FLAT)
        row = rec["bars"][0]
        key = "archive_row" if row["publication"] == "archive-only" else "rest_row"
        row[key][0] = repr(float(row[key][0]) + 1.0)
        return flat_attest_findings(rec, sealed=False)

    def four_real():
        bad = flat_attest_findings(FLAT)
        if FLAT["n_per_stem"] != FLAT_N_T:
            bad.append(f"FLAT-ATTEST the builder's n per stem {FLAT['n_per_stem']} != the fixture's {FLAT_N_T}")
        arch = [f"{b['stem']} {b['lens']} {b['open']}" for b in FLAT["bars"] if b["publication"] == "archive-only"]
        return _ok(bad, f"FLAT_BAR_ATTEST.json (sealed): the fixture's own seeded draw (n = {FLAT_N_T} per stem "
                        f"with a flat 5m bar, one stream) and its own recount of the rows past each PRE_STATE "
                        f"edge give exactly the record's {len(FLAT['bars'])} bars ({FLAT['n_population_a']} "
                        f"seeded, {FLAT['n_population_b']} among the rows TC12 added); every bar of the "
                        f"snapshot equals its sealed venue row field for field; by publication "
                        f"{FLAT['by_publication']}; none is `neither`; ARCHIVE-ONLY (REST serves a traded bar "
                        f"there now — listed, not a failure): {arch}")

    return [
        ("F-D-2 [1]", "GRID: every open_time on its lens grid, none duplicated or backward",
         "an off-grid bar inserted into a 1h frame copy",
         "any open_time of an in-scope kline file is off its lens grid (anchor 0; Monday for 1w), duplicated "
         "or backward",
         lambda: plants([("an off-grid bar inserted into a 1h frame copy", "GRID", offgrid)]),
         lambda: _ok([x for s, iv in KFILES for x in grid_findings(f"klines/{s}_{iv}.parquet", KL(s, iv))],
                     f"{len(KFILES)} in-scope kline files (17 x native and derived lenses, CLASSIC5 x 15m): no "
                     f"stamp off its lens grid, duplicated or backward")),
        ("F-D-2 [2]", "FLAT-BAR RECOUNT == the manifest's venue_zero_volume_flat_bars",
         "a carried-forward flat bar written over a real bar of a tape copy",
         "the recount of zero-volume flat bars (o == h == l == c and volume == 0) of any in-scope kline file "
         "differs from the manifest's count",
         lambda: plants([("a carried-forward flat bar written over a real bar of a 1h tape copy",
                          "recount != manifest", lambda: recount_findings(rel1, carried_forward(b1, len(b1) // 2)))]),
         lambda: _ok([x for s, iv in KFILES for x in recount_findings(f"klines/{s}_{iv}.parquet", KL(s, iv))],
                     f"{len(KFILES)} files recounted == the manifest: "
                     + " · ".join(f"{iv} " + " ".join(f"{s.replace('USDT', '')}:{int(flat0(KL(s, iv)).sum())}"
                                                       for s in PANEL17_T if int(flat0(KL(s, iv)).sum()))
                                  for iv in NATIVE_T if any(int(flat0(KL(s, iv)).sum()) for s in PANEL17_T))
                     + " — counted and KEPT (the claim is 'Naiad inserted no bar', not 'the venue published "
                       "no flat bar')")),
        ("F-D-2 [3]", "TOKEN SCAN: no fill / interpolate / resample token in the fetch-path code",
         "`def _planted(df): return df.ffill()` appended to a copy of tierc12_data.py",
         f"one of FX10's banned tokens {list(BANNED_T)} occurs in the code (comments and docstrings stripped, "
         f"string literals kept) of {list(FETCH_PATH_T)}",
         lambda: plants([("`def _planted(df): return df.ffill()` appended to a source copy", "FILL-TOKEN",
                          lambda: token_findings({**srcs, FETCH_PATH_T[1]: srcs[FETCH_PATH_T[1]]
                                                  + "\n\ndef _planted(df):\n    return df.ffill()\n"}))]),
         lambda: _ok(token_findings(srcs), f"none of {list(BANNED_T)} (read from FX10 by AST) occurs in the "
                                           f"code of {list(FETCH_PATH_T)}")),
        ("F-D-2 [4]", "VENUE ATTRIBUTION — offline, against the sealed capture",
         "a carried-forward flat bar written over a real bar among the TC12-added rows; one field of a sealed "
         "venue row altered; one sampled bar's entry removed",
         "a bar of population (a) or (b) is absent from the sealed record, the record holds a bar outside the "
         "two populations, a bar is not field-equal to its sealed venue row, a bar's publication is `neither`, "
         "or the record moved since the seal",
         lambda: plants([
             ("a carried-forward flat bar over a real bar among the TC12-ADDED rows of a 1h tape copy",
              "absent from the sealed record", added_flat),
             ("one field of one sealed venue row altered in a COPY of the record", "a field differs", field),
             ("one sampled bar's entry removed from a COPY of the record", "absent from the sealed record",
              lambda: flat_attest_findings(dict(FLAT, bars=FLAT["bars"][1:]), sealed=False)),
         ]),
         four_real),
    ]


# ═══════════════════════════════════════════════ F-D-3
def fd3_findings(root=None, funding_dir=None) -> tuple[list, list]:
    import tierc2_baseline as TB                          # the lineage's reader (bound to this snapshot)
    bad, lines = [], []
    old = TB.FUNDING
    try:
        if funding_dir is not None:
            TB.FUNDING = funding_dir
        for stem in PANEL17_T:
            cov = D.funding_coverage(stem, PIN_MS, root)
            lf = TB.load_funding(stem)
            if not cov["ok"]:
                bad.append(f"FUNDING-COVERAGE {stem}: {cov['why']}")
            if not lf:
                bad.append(f"FUNDING-COVERAGE {stem}: tierc2_baseline.load_funding returned {{}} — zero funding, silently")
            lines.append(f"{stem.replace('USDT', '')} {cov.get('interval_hours_tail')}h→{cov.get('last')}")
    finally:
        TB.FUNDING = old
    return bad, lines


def hour_faults(d: pd.DataFrame, what: str) -> list:
    """The funding-hour law, re-measured with plain arithmetic."""
    t = d["funding_time"].to_numpy(np.int64)
    floor_h, near_h = t // HOUR_T * HOUR_T, (t + HOUR_T // 2) // HOUR_T * HOUR_T
    bad = []
    if (floor_h != near_h).any():
        bad.append(f"FUNDING-HOUR {what}: {int((floor_h != near_h).sum())} print(s) whose floor hour is not the "
                   f"nearest hour")
    if "funding_hour_ms" not in d.columns:
        bad.append(f"FUNDING-HOUR {what}: the loader returned no funding_hour_ms")
    elif (d["funding_hour_ms"].to_numpy(np.int64) != floor_h).any():
        bad.append(f"FUNDING-HOUR {what}: funding_hour_ms is not the floor hour")
    elif len(d) and int(d["funding_hour_ms"].max()) > PIN_MS:
        bad.append(f"FUNDING-HOUR {what}: a print of an hour AFTER the pin came out of the loader")
    return bad


def fd3_break():
    base = D.load_funding_asof(PANEL17_T[0])

    def early():
        d = base.copy()
        d.loc[d.index[5], "funding_time"] -= 10
        return hour_faults(d, "planted")

    def late():
        d = base[list(FCOLS_T)].copy()
        d.loc[d.index[5], "funding_time"] += HOUR_T // 2
        D.with_funding_hour(d, "planted")
        return []

    def tree(edit):
        root = temp_dir("fd3")
        shutil.copytree(D.SNAPSHOT / "funding", root / "funding")
        edit(root)
        return fd3_findings(root, root / "funding")[0]

    def cut(root):
        p = root / "funding" / f"{PANEL17_T[0]}.parquet"
        pd.read_parquet(p).sort_values("funding_time").iloc[:-4].to_parquet(p, index=False)

    def missing():
        old = D.funding_path
        try:
            D.funding_path = lambda stem, root=None: TMP / "NOPE.parquet"
            D.load_funding_asof(PANEL17_T[0])
        finally:
            D.funding_path = old
        return []

    victim = PANEL17_T[len(PANEL17_T) - 1]
    return plants([
        ("a print stamped 10 ms BEFORE its hour in a COPY", "floor hour is not the nearest hour", early),
        ("a print stamped 30 min past its hour in a COPY (the loader must HALT)", "past its hour", late),
        (f"{victim} funding tape ABSENT in a COPY of the funding directory", "ABSENT",
         lambda: tree(lambda root: (root / "funding" / f"{victim}.parquet").unlink())),
        (f"{PANEL17_T[0]} funding tail cut by four prints in a COPY", "older than kline edge", lambda: tree(cut)),
        ("load_funding_asof on a missing file (must HALT)", "missing", missing),
    ])


def fd3_real():
    bad, lines = fd3_findings()
    past, late = [], []
    for stem in PANEL17_T:
        d = D.load_funding_asof(stem)
        bad += hour_faults(d, stem)
        past.append(int((d["funding_time"] - d["funding_hour_ms"]).max()))
        if int(d["funding_time"].max()) > PIN_MS:
            late.append(stem)
        row = MAN_ROWS[f"funding/{stem}.parquet"]
        if row["interval_hours_observed_tail"] is None or row["interval_hours_observed_modal"] is None:
            bad.append(f"FUNDING-COVERAGE {stem}: an observed interval is null (the fallback would be consumed)")
    return _ok(bad, f"{len(PANEL17_T)} panel stems at the pin {PIN_ISO}: funding present, non-empty, last stamp "
                    f"within ONE observed interval of the pin, tierc2_baseline.load_funding non-empty, both "
                    f"observed intervals non-null (the fallback constant is never consumed); observed cadence "
                    f"and edge: {' · '.join(lines)}; the funding-hour law holds on every print (largest stamp "
                    f"offset past its hour {max(past)} ms, none before it; prints stamped after the pin close "
                    f"yet of the pin's hour: {late or 'none'})")


# ═══════════════════════════════════════════════ F-D-EDGE
def edge_findings(rel: str, df: pd.DataFrame) -> list:
    iv = lens_of(rel)[1]
    t = df["open_time"].to_numpy(np.int64)
    out, tgt = [], target_t(iv, PIN_MS)
    if not len(t) or int(t.max()) != tgt:
        out.append(f"EDGE {rel}: ends at {D.iso(int(t.max())) if len(t) else None}, not at its lens's last bar "
                   f"closing <= the pin ({D.iso(tgt)})")
    if len(t) != len(np.unique(t)):
        out.append(f"EDGE {rel}: a duplicate stamp")
    if ((t - anchor_t(iv)) % STEP_T[iv] != 0).any():
        out.append(f"EDGE {rel}: an off-grid stamp")
    if (t + STEP_T[iv] > PIN_MS).any():
        out.append(f"EDGE {rel}: {int((t + STEP_T[iv] > PIN_MS).sum())} row(s) past the pin")
    return out


def funding_edge_findings(stem: str, df: pd.DataFrame) -> list:
    t = np.sort(df["funding_time"].to_numpy(np.int64))
    hour = t // HOUR_T * HOUR_T
    out = []
    ivl = int(np.median(np.diff(hour)[-10:]) // HOUR_T)             # the observed cadence of the tail
    if int(hour.max()) + ivl * HOUR_T <= PIN_MS:
        out.append(f"EDGE funding/{stem}: stops short of the pin's hour (last print {D.iso(int(t.max()))}, "
                   f"cadence {ivl}h)")
    if len(hour) != len(np.unique(hour)):
        out.append(f"EDGE funding/{stem}: repeats a print")
    if (t > PIN_MS + JITTER_T).any():
        out.append(f"EDGE funding/{stem}: holds a print past pin + jitter")
    return out


def manifest_row_findings(rel: str, row: dict, df: pd.DataFrame) -> list:
    """MANIFEST-ROW: the manifest mis-describes a file (sha, rows, flags, content sha)."""
    q = D.SNAPSHOT / rel
    cols = KCOLS_T if rel.startswith("klines/") else FCOLS_T
    out = []
    if row.get("sha256") != sha_f(q) or row.get("bytes") != q.stat().st_size:
        out.append(f"MANIFEST-ROW {rel}: sha256 / bytes")
    if row.get("rows") != len(df) or row.get("content_sha") != frame_sha_t(df.sort_values(cols[0]), cols):
        out.append(f"MANIFEST-ROW {rel}: rows / content sha")
    if rel.startswith("klines/"):
        t = df["open_time"].to_numpy(np.int64)
        iv = lens_of(rel)[1]
        flags = {"last_open_ms": int(t.max()), "first_open_ms": int(t.min()), "rows_after_as_of": 0,
                 "gap_count": int((np.diff(np.sort(t)) > STEP_T[iv]).sum()), "duplicates": 0, "off_grid": 0,
                 "backward": 0, "complete_to_as_of": True,
                 "last_bar_close_equals_lens_last_closed_at_pin": True,
                 "tc12_rows_added": len(df) - PRE["files"][rel]["rows"], "native": iv not in DERIVED_T}
    else:
        t = df["funding_time"].to_numpy(np.int64)
        flags = {"last_ms": int(t.max()), "first_ms": int(t.min()), "rows_after_as_of": 0, "duplicates": 0,
                 "tc12_rows_added": len(df) - PRE["files"][rel]["rows"]}
    bad = sorted(k for k, v in flags.items() if row.get(k) != v)
    if bad:
        out.append(f"MANIFEST-ROW {rel}: flags {bad}")
    return out


def edge_break():
    b = KL("BTCUSDT", "12h")
    past = b.tail(1).copy()
    past["open_time"] = past["open_time"] + STEP_T["12h"]
    rel = "klines/BTCUSDT_12h.parquet"
    f = FU("BTCUSDT")
    return plants([
        ("a row past the pin appended to a frame copy", "past the pin",
         lambda: edge_findings(rel, pd.concat([b, past], ignore_index=True))),
        ("a tape truncated by one bar (frame copy)", "not at its lens's last bar", lambda: edge_findings(rel, b.iloc[:-1])),
        ("a funding tape truncated by one print (frame copy)", "stops short of the pin's hour",
         lambda: funding_edge_findings("BTCUSDT", f.iloc[:-1])),
        ("a manifest row with a moved sha (COPY)", "MANIFEST-ROW",
         lambda: manifest_row_findings(rel, dict(MAN_ROWS[rel], sha256="0" * 64), b)),
        ("a 404 row planted in a COPY of the fetch log", "FETCH-404",
         lambda: D.http_404_findings(FETCH_ROWS + [{"kind": "http", "phase": "fetch", "status": 404,
                                                    "venue": "BINANCE", "endpoint": "/fapi/v1/klines",
                                                    "params": {}}])),
    ])


def edge_real():
    bad = []
    for rel in SCOPE_T:
        df = frame_of(rel)
        bad += manifest_row_findings(rel, MAN_ROWS[rel], df)
        bad += edge_findings(rel, df) if rel.startswith("klines/") else funding_edge_findings(
            rel[len("funding/"):-len(".parquet")], df)
    bad += D.http_404_findings(FETCH_ROWS)
    n_http = sum(1 for r in FETCH_ROWS if r.get("kind") == "http" and r.get("phase") == "fetch")
    lens = {iv: D.iso(target_t(iv, PIN_MS)) for iv in STEP_T}
    return _ok(bad, f"{sum(1 for r in SCOPE_T if r.startswith('klines/'))} kline files each end exactly at their "
                    f"lens's last bar closing <= {PIN_ISO} ({lens}): no duplicate, off-grid stamp or row past "
                    f"the pin; {len(PANEL17_T)} funding tapes reach the last print due at the pin by their "
                    f"observed cadence, repeat none and hold none past pin + jitter; the manifest's sha, bytes, "
                    f"rows, flags and content sha (re-hashed here) describe every file; no status 404 among "
                    f"the {n_http} HTTP rows of the fetch phase")


# ═══════════════════════════════════════════════ F-D-DERIVE
def kahan(vals) -> float:
    """pandas' groupby sum is COMPENSATED (Kahan); the plain loop states the compensated sum explicitly."""
    s = c = 0.0
    for v in vals:
        y = v - c
        t = s + y
        c = (t - s) - y
        s = t
    return s


def plain_derive(f: pd.DataFrame, naive: bool = False, keep_short: bool = False, anchor: int = MONDAY_T):
    """1d / 1w from native 4h by a plain loop sharing no code with derive_1d / derive_1w."""
    t = f["open_time"].to_numpy(np.int64)
    o, h, l, c, v = (f[k].to_numpy(np.float64) for k in KCOLS_T[1:])
    days: dict = {}
    for i in range(len(t)):
        if int(t[i]) + STEP_T["4h"] <= PIN_MS:
            days.setdefault(int(t[i]) // DAY_T, []).append(i)
    add = (lambda xs: sum(xs, 0.0)) if naive else kahan
    d1 = []
    for dk in sorted(days):
        ix = days[dk]
        if len(ix) == 6 or keep_short:
            d1.append((dk * DAY_T, o[ix[0]], max(h[j] for j in ix), min(l[j] for j in ix),
                       c[ix[len(ix) - 1]], add([v[j] for j in ix])))
    weeks: dict = {}
    for r in d1:
        weeks.setdefault((r[0] - anchor) // WEEK_T, []).append(r)
    w1 = []
    for wk in sorted(weeks):
        rs = weeks[wk]
        if len(rs) == 7:
            w1.append((wk * WEEK_T + anchor, rs[0][1], max(r[2] for r in rs), min(r[3] for r in rs),
                       rs[6][4], add([r[5] for r in rs])))
    mk = lambda rows: pd.DataFrame(rows, columns=list(KCOLS_T)).astype(                 # noqa: E731
        {"open_time": np.int64, **{k: np.float64 for k in KCOLS_T[1:]}})
    return mk(d1), mk(w1)


def derive_findings(stem: str, d1: pd.DataFrame, w1: pd.DataFrame, ref=None, rows=True) -> list:
    d_ref, w_ref = ref if ref is not None else plain_derive(KL(stem, "4h"))
    out = []
    for iv, got, want in (("1d", d1, d_ref), ("1w", w1, w_ref)):
        if frame_sha_t(got, KCOLS_T) != frame_sha_t(want, KCOLS_T):
            out.append(f"DERIVE [{iv}] {stem}: the {iv} frame != the plain loop ({len(got)} vs {len(want)} rows)")
        if rows:
            row = MAN_ROWS[f"klines/{stem}_{iv}.parquet"]
            if row["content_sha"] != frame_sha_t(want, KCOLS_T) or row["derivation_content_sha"] != frame_sha_t(
                    want, KCOLS_T):
                out.append(f"DERIVE [{iv}] {stem}: the manifest's content shas are not the plain loop's")
    wd = (w1["open_time"].to_numpy(np.int64) - MONDAY_T) % WEEK_T
    if len(w1) and (wd != 0).any():
        out.append(f"DERIVE [1w] {stem}: {int((wd != 0).sum())} week(s) do not open on a Monday")
    return out


def derive_break():
    f4 = KL("BTCUSDT", "4h")
    hole = f4.drop(f4.index[len(f4) // 2])                                  # a COPY with one 4h bar missing
    return plants([
        ("a 1d that KEEPS a five-bar day (a holed tape copy)", "DERIVE [1d]",
         lambda: derive_findings("BTCUSDT", *plain_derive(hole, keep_short=True), ref=plain_derive(hole),
                                 rows=False)),
        ("weeks anchored on the epoch (Thursday)", "DERIVE [1w]",
         lambda: derive_findings("BTCUSDT", *plain_derive(f4, anchor=0), rows=False)),
        ("a naive left-to-right volume sum (differs in the last bit)", "DERIVE [1d]",
         lambda: derive_findings("BTCUSDT", *plain_derive(f4, naive=True), rows=False)),
        ("production's derive_1d fed a tape the loop sees whole (one bar dropped)", "DERIVE [1d]",
         lambda: derive_findings("BTCUSDT", D.derive_1d(hole)[0], D.derive_1w(D.derive_1d(hole)[0])[0],
                                 rows=False)),
    ])


def derive_real():
    bad, n_d, n_w = [], 0, 0
    for stem in PANEL17_T:
        d1, w1 = KL(stem, "1d"), KL(stem, "1w")
        bad += derive_findings(stem, d1, w1)
        n_d, n_w = n_d + len(d1), n_w + len(w1)
    return _ok(bad, f"{len(PANEL17_T)} stems: {n_d} filed days and {n_w} filed weeks are, bit for bit (stamps, "
                    f"O, H, L, C, and the volume by the compensated sum), the plain loop's rebuild from the "
                    f"native 4h tape closed at the pin; the manifest's content_sha and derivation_content_sha "
                    f"of all {2 * len(PANEL17_T)} derived files are the loop's; every week opens on a Monday")


# ═══════════════════════════════════════════════ F-D-OUT / F-D-UNTOUCHED
def out_ast_findings(src: str) -> list:
    """OUT-GUARD: write_manifest must open on `dst = _out_guard(dst)` and write only under `dst`."""
    fn = next(n for n in ast.parse(src).body if isinstance(n, ast.FunctionDef) and n.name == "write_manifest")
    body = [s for s in fn.body if not (isinstance(s, ast.Expr) and isinstance(s.value, ast.Constant))]
    out = []
    if not body or ast.unparse(body[0]) != "dst = _out_guard(dst)":
        out.append("OUT-GUARD write_manifest does not open on `dst = _out_guard(dst)`")
    for c in _calls(fn):
        if _name(c) in ("_dump", "write_text", "write_bytes") and not any(
                isinstance(x, ast.Name) and x.id == "dst" for x in ast.walk(c)):
            out.append(f"OUT-GUARD write_manifest writes outside `dst`: {ast.unparse(c)[:60]}")
    return out


def out_cases() -> list:
    link = temp_dir("link") / "t11"
    os.symlink(ROOT / "research_outputs" / "tierc11" / "data", link)
    return [("research_outputs/tierc10/data", ROOT / "research_outputs" / "tierc10" / "data"),
            ("research_outputs/tierc11/data", ROOT / "research_outputs" / "tierc11" / "data"),
            ("a symlink to tierc11/data", link),
            ("a '..' traversal to tierc11/data", OUT / ".." / ".." / "tierc11" / "data"),
            ("the stage directory's parent", OUT.parent)]


def out_break():
    rows = [(f"--out {label}", "--out", (lambda p=p: D._out_guard(p))) for label, p in out_cases()]
    rows.append(("the guard call removed in a source copy", "OUT-GUARD",
                 lambda: out_ast_findings(mut(SRC_TEXT, "    dst = _out_guard(dst)\n    pin = load_pin(OUT)\n",
                                              "    pin = load_pin(OUT)\n"))))
    return plants(rows)


def out_real():
    bad = out_ast_findings(SRC_TEXT)
    for label, p in out_cases():
        try:
            D._out_guard(p)
            bad.append(f"OUT-ADMITS {label}")
        except SystemExit:
            pass
    for label, p in (("the stage directory", OUT), ("a directory under it", OUT / "_det_data" / "seed_1"),
                     ("a temp directory", temp_dir("out"))):
        try:
            D._out_guard(p)
        except SystemExit:
            bad.append(f"OUT-REFUSES {label}")
    return _ok(bad, f"--out refuses {[x for x, _ in out_cases()]} and admits the stage directory, a directory "
                    f"under it and a temp directory outside the repo; write_manifest opens on "
                    f"`dst = _out_guard(dst)` and every write of it lands under `dst`")


def old_snapshot_findings(root: Path, man: dict, label: str, only=None) -> list:
    exp = {f["path"]: f["sha256"] for f in man["files"] if f.get("present", True) and f.get("sha256")}
    exp.update({o["path"]: o["sha256"] for o in man["out_of_scope_snapshot_files"]})
    out = [f"UNTOUCHED {label} {rel}: sha != its manifest" for rel in (only or sorted(exp))
           if not (root / rel).is_file() or sha_f(root / rel) != exp[rel]]
    if only is None:
        stray = sorted(set(D.tree_files(root)) - set(exp) - {"MANIFEST.json"})
        if stray:
            out.append(f"UNTOUCHED {label}: files its manifest does not pin: {stray[:4]}")
    return out


def untouched_break():
    def flipped():
        rel = "funding/BTCUSDT.parquet"
        tmp = temp_snapshot([rel])
        raw = bytearray((tmp / rel).read_bytes())
        raw[len(raw) // 2] ^= 1
        (tmp / rel).write_bytes(bytes(raw))
        return old_snapshot_findings(tmp, T11_MAN, "a temp copy of the TC11 snapshot", only=[rel])
    return plants([("one byte flipped in a temp copy of an old-snapshot file", "UNTOUCHED", flipped)])


def untouched_real():
    t10 = jload(D.TC10_MANIFEST)
    bad = old_snapshot_findings(D.TC11_SNAPSHOT, T11_MAN, "TC11 snapshot")
    bad += old_snapshot_findings(D.TC10_SNAPSHOT, t10, "TC10 snapshot")
    now = _stat3(LIVE_MANIFEST)
    if now != LIVE_STAT_AT_START:
        bad.append("UNTOUCHED the live cache's MANIFEST.json stat (size, mtime, inode) moved across this run")
    n11 = len(T11_ROWS) + len(T11_OTHER)
    n10 = len([f for f in t10["files"] if f.get("present", True) and f.get("sha256")]) + len(
        t10["out_of_scope_snapshot_files"])
    return _ok(bad, f"after the build the TC11 snapshot re-hashes, file for file, to TC11's manifest ({n11} "
                    f"files) and the TC10 snapshot to TC10's ({n10} pinned files); the live cache's "
                    f"MANIFEST.json stat (size, mtime, inode — stat only, never opened) did not move across "
                    f"this fixture run (this bounds the run; the build's never-touched claim is by "
                    f"construction: F-D-GUARD + F-D-BOUND)")


# ═══════════════════════════════════════════════ F-D-DET
def det_base() -> Path:
    tmps = {Path(tempfile.gettempdir()).resolve(), Path("/private/tmp").resolve()}
    in_tmp = any(t in RUN_ROOT.parents for t in tmps)
    return RUN_ROOT if (RUN_ROOT == OUT.resolve() or in_tmp) else TMP


def launch(twin_dir: Path, hashseed):
    env = dict(os.environ, PYTHONHASHSEED=str(hashseed), PYTHONDONTWRITEBYTECODE="1")
    log = open(TMP / f"det_{hashseed}.log", "w")
    return subprocess.Popen([PY, "-B", str(ROOT / "scripts" / "tierc12_data.py"), "--manifest", "--out",
                             str(twin_dir)], env=env, stdout=log, stderr=subprocess.STDOUT, cwd=str(TMP))


def clock_call_findings(src: str) -> list:
    """DET-CLOCK-CALL: a `time.<x>()` call, or a `datetime.now / utcnow / today` call, in the call
    graph of write_manifest (conversions of a GIVEN instant — fromtimestamp, strptime — are not clocks)."""
    fns = {n.name: n for n in ast.parse(src).body if isinstance(n, ast.FunctionDef)}
    seen, queue = set(), ["write_manifest"]
    while queue:
        name = queue.pop()
        if name in seen or name not in fns:
            continue
        seen.add(name)
        queue += [_name(c) for c in _calls(fns[name])]
        queue += [x.id for x in ast.walk(fns[name]) if isinstance(x, ast.Name) and x.id in fns]
    out = []
    for name in sorted(seen):
        for c in _calls(fns[name]):
            f = c.func
            if isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name):
                if f.value.id == "time" or (f.value.id in ("datetime", "date") and f.attr in CLOCK_CALLS_T):
                    out.append(f"DET-CLOCK-CALL {name}(): {f.value.id}.{f.attr}() in the call graph of write_manifest")
    return out


def content_shas(man_bytes: bytes) -> dict:
    m = json.loads(man_bytes)
    return {f"{f['path']}|{k}": f[k] for f in m["files"] for k in ("content_sha", "derivation_content_sha")
            if f.get(k)}


def det_findings(twins: dict) -> list:
    canon = {n: (OUT / n).read_bytes() for n in DET_FILES_T if (OUT / n).is_file()}
    read = {lab: (rc, FX.read_dir(d)) for lab, (rc, d) in twins.items()}
    out = FX.det_findings(read, canon, DET_FILES_T)
    name = "STAGE_D_MANIFEST.json"
    shas = {lab: content_shas(x[name]) for lab, (_, x) in read.items() if name in x}
    shas["canonical"] = content_shas(canon[name]) if name in canon else {}
    labs = list(shas)
    for lab in labs[1:]:
        if shas[lab] != shas[labs[0]]:
            out.append(f"DET-CONTENT-SHA {labs[0]} vs {lab}: a parquet content sha differs")
    return out


def _hash_order_plant() -> list:
    """A builder twin that emits a line built from iterating a set, under the two hash seeds."""
    prog = "import sys\nopen(sys.argv[1], 'w').write(' '.join({'alpha', 'beta', 'gamma', 'delta', 'epsilon', 'zeta', 'eta'}))\n"
    twins = {}
    for s in FX.det_seeds(SEED):
        d = temp_dir(f"hash{s}")
        rc = subprocess.run([PY, "-B", "-c", prog, str(d / "LINE.txt")], env=dict(os.environ, PYTHONHASHSEED=s)).returncode
        twins[f"seed {s}"] = (rc, FX.read_dir(d))
    labs = list(twins)
    return FX.det_findings(twins, twins[labs[0]][1], ["LINE.txt"])


def det_break():
    return plants([
        ("a hash-order-dependent emission (a line built from iterating a set, under the two hash seeds)",
         "DET-BYTES", _hash_order_plant),
        ("a fee_schedule() copy that stamps datetime.now()'s date", "DET-CLOCK-CALL fee_schedule",
         lambda: clock_call_findings(mut(SRC_TEXT, "    out = out or OUT\n    rules, cfg = ROOT",
                                         "    out = out or OUT\n    stamp = datetime.now(timezone.utc)\n"
                                         "    rules, cfg = ROOT"))),
        ("an `elapsed_s` key planted in a COPY of a determinism-set file", "DET-CLOCK",
         lambda: FX.clock_findings({"fee_schedule.json": json.dumps(dict(FEES, elapsed_s=1.0)).encode()})),
    ])


def det_real():
    base = det_base()
    twins = FX.det_twins(launch, base, TAG, SEED)
    bad = det_findings(twins) + clock_call_findings(SRC_TEXT)
    shutil.rmtree(base / f"_det_{TAG}", ignore_errors=True)
    n = len(content_shas((OUT / "STAGE_D_MANIFEST.json").read_bytes()))
    return _ok(bad, f"two fresh-subprocess `--manifest` builds under PYTHONHASHSEED {list(FX.det_seeds(SEED))} "
                    f"exit 0 and write exactly {list(DET_FILES_T)}, byte-identical twin to twin and twin to the "
                    f"filed files; no clock-named key in any of them; the {n} parquet content shas (files and "
                    f"derivations) carried by the three manifests are equal; no `time.` call and no "
                    f"datetime.now / utcnow / today call stands in the call graph of write_manifest "
                    f"(fromtimestamp / strptime convert a GIVEN instant and are not clocks)")


# ═══════════════════════════════════════════════ F-TOLL [data a] … [data g]
PAGE_T = ("<html><body><h2>USD&#9416;-M Futures Trading</h2><table><tr><th>Level</th><th>30d Volume</th>"
          "<th>Maker / Taker</th><th>Maker / Taker (BNB 10% off)</th></tr>"
          "<tr><td>Regular User</td><td>&lt; 15,000,000</td><td>0.0200% / 0.0500%</td><td>0.0180% / 0.0450%</td></tr>"
          "<tr><td>VIP 1</td><td>&ge; 15,000,000</td><td>0.0160% / 0.0400%</td><td>0.0144% / 0.0360%</td></tr>"
          "</table><h2>USDC-M Futures Trading</h2><table><tr><th>Level</th><th>30d Volume</th>"
          "<th>Maker / Taker</th></tr><tr><td>Regular User</td><td>&lt; 15,000,000</td>"
          "<td>0.0000% / 0.0400%</td></tr></table></body></html>").encode("utf-8")
GRAMMAR_T = {"entry_tier_label": "Regular User",
             "scope": r"(?P<row>Regular User</td><td>[^<]*</td><td>[^<]*</td>)",
             "maker": [r"<td>(?P<pct>[0-9.]+)% / [0-9.]+%</td>"],
             "taker": [r"<td>[0-9.]+% / (?P<pct>[0-9.]+)%</td>"]}
ENTRY_LABEL_T, MAKER_HEAD_T, DISCOUNT_WORDS_T = "Regular User", "Maker / Taker", ("off", "discount", "bnb")


class _Tables(html.parser.HTMLParser):
    """A STRUCTURAL parse: every table as rows of cell texts (no pattern of the grammar is used)."""

    def __init__(self):
        super().__init__()
        self.tables, self._row, self._cell = [], None, None

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self.tables.append([])
        elif tag == "tr":
            self._row = []
        elif tag in ("td", "th"):
            self._cell = []

    def handle_endtag(self, tag):
        if tag in ("td", "th") and self._cell is not None:
            self._row.append("".join(self._cell).strip())
            self._cell = None
        elif tag == "tr" and self._row is not None and self.tables:
            self.tables[len(self.tables) - 1].append(self._row)
            self._row = None

    def handle_data(self, data):
        if self._cell is not None:
            self._cell.append(data)


def second_extractor(body: bytes):
    """THE FIXTURE'S OWN EXTRACTOR, under the same definition: in every table, the column headed
    exactly "Maker / Taker" (no discount word), the row whose first cell is the entry tier; the
    maker percent of each; positive figures only; the HIGHEST.  None when the body holds none."""
    p = _Tables()
    p.feed(body.decode("utf-8", errors="replace"))
    figs = []
    for table in p.tables:
        if not table:
            continue
        cols = [i for i, hcell in enumerate(table[0]) if hcell == MAKER_HEAD_T
                and not any(w in hcell.lower() for w in DISCOUNT_WORDS_T)]
        for row in table[1:]:
            if row and row[0] == ENTRY_LABEL_T:
                for i in cols:
                    m = re.fullmatch(r"([0-9.]+)% / ([0-9.]+)%", row[i]) if i < len(row) else None
                    if m and Fraction(m.group(1)) > 0:
                        figs.append(Fraction(m.group(1)))
    return max(figs) if figs else None


def readme_maker_bps() -> Fraction:
    """The figure ON FILE by the fixture's own read of README.md: percent x 10000 / 100."""
    for line in (ROOT / "README.md").read_text(encoding="utf-8").splitlines():
        m = MAKER_RX_T.search(line)
        if m:
            return Fraction(m.group(1)) * 10000 / 100
    raise SystemExit("HALT: no 'maker is <x>%' sentence in README.md")


def fee_literal_findings(src: str) -> list:
    out = []
    for fn in ast.parse(src).body:
        if isinstance(fn, ast.FunctionDef) and fn.name in FEE_FUNCS_T:
            lits = [c.value for c in ast.walk(fn) if isinstance(c, ast.Constant)
                    and type(c.value) in (int, float, complex)]
            if lits:
                out.append(f"TOLL-A {fn.name}(): numeric literal(s) {lits}")
    missing = set(FEE_FUNCS_T) - {fn.name for fn in ast.parse(src).body if isinstance(fn, ast.FunctionDef)}
    return out + [f"TOLL-A {n}() is not defined" for n in sorted(missing)]


def taker_findings(fees: dict) -> list:
    import tierc2_rules as R2
    side, rt = float(R2.FEE_BPS_SIDE), float(R2.FEE_BPS_ROUND_TRIP)
    out = []
    for a in fees["assets"]:
        if a["taker_bps_side_used"] != side or a["round_trip_bps_used"] != rt:
            out.append(f"TOLL-B {a['stem']}: a taker figure != tierc2_rules ({side} / {rt})")
        for s in a["source"]:
            path, _, line = s.rpartition(":")
            if not line.isdigit() or "fee_bps" not in (ROOT / path).read_text(
                    encoding="utf-8").splitlines()[int(line) - 1].lower():
                out.append(f"TOLL-B {a['stem']}: the source line {s} does not hold the fee object")
    for v, b in fees["venues"].items():
        if b["taker_bps_side"] != side or b["taker_round_trip_bps"] != rt:
            out.append(f"TOLL-B venue {v}: a taker figure != tierc2_rules")
    return out


def carried_findings(fees: dict) -> list:
    t11 = json.loads(D.tc11_read("research_outputs/tierc11/data/fee_schedule.json"))
    rows = {r["stem"]: r for r in t11["assets"]}
    out = [f"TOLL-C top-level {k} differs from TC11's file" for k in EQUAL_TOP_T if fees.get(k) != t11.get(k)]
    for a in fees["assets"]:
        moved = [k for k in EQUAL_ROW_T if a.get(k) != rows[a["stem"]].get(k)]
        if moved:
            out.append(f"TOLL-C row {a['stem']}: {moved} differ from TC11's file")
        if set(a) != set(rows[a["stem"]]) | {"maker_bps_side"}:
            out.append(f"TOLL-C row {a['stem']}: its keys are not TC11's 26 plus maker_bps_side")
    if fees["tc11_fee_schedule"]["sha256"] != sha_f(D.TC11_FEES):
        out.append("TOLL-C the TC11 fee file sha filed is not the file's")
    return out


def maker_findings(fees: dict, src: dict) -> list:
    """TOLL-D: a venue's maker_bps_side is neither the extractor's value on the saved body (when
    PUBLISHED) nor the README regex value (when ON FILE); a PUBLISHED venue lacks a URL, a date or a body sha."""
    out, on_file = [], readme_maker_bps()
    grammar = (jload(OUT / "FEE_GRAMMAR.json").get("venues") or {}) if (OUT / "FEE_GRAMMAR.json").exists() else {}
    for v, b in fees["venues"].items():
        s = src["venues"][v]
        if b["maker_kind"] == "PUBLISHED":
            body = Path(s["body_path"]).read_bytes()
            if sha_b(body) != s["body_sha256"] or b["maker_source_body_sha256"] != s["body_sha256"]:
                out.append(f"TOLL-D {v}: the saved body's sha is not FEE_SOURCE.json's")
            ex = D.extract_fee(body, grammar[v])
            if ex["maker_pct"] is None or Fraction(str(b["maker_bps_side"])) != D.pct_to_bps(ex["maker_pct"]):
                out.append(f"TOLL-D {v}: maker_bps_side is not the extractor's value on the saved body")
            if not (b["maker_source_url"] and b["maker_retrieved_utc_date"] and b["maker_source_body_sha256"]):
                out.append(f"TOLL-D {v}: PUBLISHED without a URL, a date or a body sha")
        else:
            if Fraction(str(b["maker_bps_side"])) != on_file:
                out.append(f"TOLL-D {v}: maker_bps_side {b['maker_bps_side']} is not the README regex value {on_file}")
            if s["http_status"] == 200 and s["body_sha256"]:
                out.append(f"TOLL-D {v}: captured with HTTP 200 and filed unretrievable without a ruled reason")
    return out


def date_findings(man: dict, fees: dict, src: dict) -> list:
    out = []
    for v, s in src["venues"].items():
        m, b = man["fee_sources"][v], fees["venues"][v]
        pub = b["maker_kind"] == "PUBLISHED"
        for label, got, want in (
                ("manifest url", m["maker_source_url"], s["url"]), ("fee-file url", b["maker_source_url"], s["url"]),
                ("manifest attempted date", m["retrieval_attempted_utc_date"], s["retrieved_utc_date"]),
                ("fee-file attempted date", b["maker_retrieval_attempted_utc_date"], s["retrieved_utc_date"]),
                ("manifest retrieved date", m["retrieved_utc_date"], s["retrieved_utc_date"] if pub else None),
                ("fee-file retrieved date", b["maker_retrieved_utc_date"], s["retrieved_utc_date"] if pub else None),
                ("manifest body sha", m["body_sha256"], s["body_sha256"])):
            if got != want:
                out.append(f"TOLL-E {v}: the {label} {got!r} != FEE_SOURCE.json's {want!r}")
    if SEAL["files"]["FEE_SOURCE.json"]["sha256"] != sha_f(OUT / "FEE_SOURCE.json"):
        out.append("TOLL-E FEE_SOURCE.json moved since the seal")
    return out


def second_findings(body: bytes, grammar: dict) -> list:
    ex = D.extract_fee(body, grammar)
    mine = second_extractor(body)
    return [] if ex["maker_pct"] == mine else [
        f"TOLL-F the extractor of record yields {ex['maker_pct']} ({ex['maker_reason']}); the second extractor "
        f"yields {mine}"]


def venue_row_findings(fees: dict) -> list:
    out = []
    want = D.venues_of_record()
    if sorted(fees["venues"]) != sorted(want):
        out.append(f"TOLL-G the venue blocks {list(fees['venues'])} are not the venues of the Stage D table {want}")
    for a in fees["assets"]:
        v = fees["venues"].get(a["venue"], {})
        if not (a["maker_bps_side"] == a["maker_bps_per_side"] == v.get("maker_bps_side")):
            out.append(f"TOLL-G row {a['stem']}: maker_bps_side / maker_bps_per_side / its venue block disagree")
        if a["stem"] not in v.get("stems", []):
            out.append(f"TOLL-G row {a['stem']}: not among its venue block's stems")
    mp = fees["maker_pin"]
    if mp["values"] != {v: b["maker_bps_side"] for v, b in fees["venues"].items()}:
        out.append("TOLL-G maker_pin.values are not the venue blocks' figures")
    if mp["differs_from_x_assumption"] != {v: b["maker_bps_side"] != mp["x_assumed_bps_side"]
                                           for v, b in fees["venues"].items()}:
        out.append("TOLL-G differs_from_x_assumption is not (value != X's assumed figure)")
    return out


def _bent(path, value):
    """A deep COPY of the fee document with one leaf replaced."""
    doc = copy.deepcopy(FEES)
    node = doc
    for k in path[:-1]:
        node = node[k]
    node[path[len(path) - 1]] = value
    return doc


def toll_d():
    title = "the maker figure of record is the extractor's on the sealed bytes, or the README regex's"
    lost = [v for v, s in FEE_SRC["venues"].items() if s["body_sha256"] and not Path(s["body_path"]).is_file()]
    if lost:
        FX.not_run("F-TOLL [data d]", title, f"FEE_SOURCE.json records a body for {lost} and the body file is absent")
        return
    v0 = list(FEES["venues"])[0]
    page_bps = D.pct_to_bps(D.extract_fee(PAGE_T, GRAMMAR_T)["maker_pct"])

    def real():
        bad = maker_findings(FEES, FEE_SRC)
        if page_bps != Fraction(2):
            bad.append(f"TOLL-D control: the extractor on the fixture's page yields {page_bps} bps, not 2")
        status = {v: (s["http_status"], FEES["venues"][v]["maker_unretrievable_reason"],
                      FEES["venues"][v]["maker_kind"]) for v, s in FEE_SRC["venues"].items()}
        return _ok(bad, f"per venue (HTTP status, reason, kind) from the sealed FEE_SOURCE.json and the fee file: "
                        f"{status}; no venue is PUBLISHED, so every maker_bps_side is the README regex value "
                        f"({float(readme_maker_bps())} bps/side — the fixture's own read) and no body exists to "
                        f"extract from; control: production's extractor on the fixture's constructed page and "
                        f"grammar yields {float(page_bps)} bps")

    FX.prove("F-TOLL [data d]", title, "a venue figure nudged in a copy of the fee file",
             "a venue's maker_bps_side is neither the value the extractor of record returns on the saved body "
             "under FEE_GRAMMAR.json (when PUBLISHED) nor the README regex value (when ON FILE); the saved "
             "body's sha is not FEE_SOURCE.json's; or a PUBLISHED venue lacks a URL, a date or a body sha",
             lambda: plants([("a venue figure nudged in a COPY", "TOLL-D",
                              lambda: maker_findings(_bent(("venues", v0, "maker_bps_side"),
                                                           FEES["venues"][v0]["maker_bps_side"] + 0.1), FEE_SRC))]),
             real)


def toll_legs() -> list:
    v0 = list(FEES["venues"])[0]
    bent_grammar = dict(GRAMMAR_T, maker=GRAMMAR_T["taker"])
    day = FEE_SRC["venues"][v0]["retrieved_utc_date"]
    off = copy.deepcopy(MAN)
    off["fee_sources"][v0]["retrieval_attempted_utc_date"] = day[:-2] + ("01" if day[-2:] != "01" else "02")

    def f_real():
        bad = second_findings(PAGE_T, GRAMMAR_T)
        published = [v for v, b in FEES["venues"].items() if b["maker_kind"] == "PUBLISHED"]
        for v in published:
            body = Path(FEE_SRC["venues"][v]["body_path"]).read_bytes()
            mine = second_extractor(body)
            if mine is None or D.pct_to_bps(mine) != Fraction(str(FEES["venues"][v]["maker_bps_side"])):
                bad.append(f"TOLL-F {v}: the second extractor disagrees with the PUBLISHED figure")
        none = {v: f"http_{s['http_status']}, no body" for v, s in FEE_SRC["venues"].items() if not s["body_sha256"]}
        return _ok(bad, f"PUBLISHED venues: {published or 'none'} — FEE_SOURCE.json files {none}, so there are no "
                        f"bytes for a second extraction; control: on the fixture's constructed page the "
                        f"structural second extractor (tables, the undiscounted 'Maker / Taker' column, the "
                        f"entry-tier row, positive figures, the highest) and production's extractor under the "
                        f"fixture's grammar agree ({second_extractor(PAGE_T)} %)")

    return [
        ("F-TOLL [data a]", "no numeric literal in the fee writer, the extractor, the conversion, the capture",
         "a typed 2.0 in a copy of fee_schedule()",
         f"{list(FEE_FUNCS_T)} holds ANY numeric literal (AST; not even 0, 1 or 2)",
         lambda: plants([("a typed `2.0` in a copy of fee_schedule()", "TOLL-A fee_schedule",
                          lambda: fee_literal_findings(mut(
                              SRC_TEXT, "            \"maker_round_trip_bps\": maker + maker,",
                              "            \"maker_round_trip_bps\": 2.0 * maker,")))]),
         lambda: _ok(fee_literal_findings(SRC_TEXT), f"{list(FEE_FUNCS_T)} hold no numeric literal")),
        ("F-TOLL [data b]", "every taker figure is the estate's object",
         "a row taker of 4.0 in a copy",
         "any taker figure in the file != tierc2_rules.FEE_BPS_SIDE / FEE_BPS_ROUND_TRIP, or a row's `source` "
         "line does not hold the fee object",
         lambda: plants([("a row taker of 4.0 in a COPY", "TOLL-B",
                          lambda: taker_findings(_bent(("assets", 0, "taker_bps_side_used"), 4.0))),
                         ("a source line that does not hold the fee object in a COPY", "TOLL-B",
                          lambda: taker_findings(_bent(("assets", 0, "source"), ["scripts/tierc2_rules.py:1"])))]),
         lambda: _ok(taker_findings(FEES), f"{len(FEES['assets'])} rows and {len(FEES['venues'])} venue blocks: "
                                           f"taker {FEES['assets'][0]['taker_bps_side_used']} bps/side, "
                                           f"{FEES['assets'][0]['round_trip_bps_used']} round trip == "
                                           f"tierc2_rules; every row's source lines hold the fee object")),
        ("F-TOLL [data c]", "taker and charter tiers unchanged: the carried keys == TC11's file",
         "a charter tier moved in a copy",
         "any of the 6 top-level or 19 row keys listed EQUAL in L-D.19 differs from TC11's fee file (its sha "
         "held to TC11's PROGRESS), or a row's key set is not TC11's 26 plus maker_bps_side",
         lambda: plants([("a charter tier moved in a COPY", "TOLL-C",
                          lambda: carried_findings(_bent(("assets", 0, "charter_slippage_tier"), "C"))),
                         ("a top-level tier table moved in a COPY", "TOLL-C top-level",
                          lambda: carried_findings(_bent(("charter_slippage_tiers", "A", "bps_per_side"), 3.0)))]),
         lambda: _ok(carried_findings(FEES), f"{len(EQUAL_TOP_T)} top-level and {len(EQUAL_ROW_T)} row keys equal "
                                             f"TC11's fee file on all {len(FEES['assets'])} rows; each row holds "
                                             f"TC11's 26 keys plus maker_bps_side")),
        ("F-TOLL [data d]", toll_d),
        ("F-TOLL [data e]", "the URL and the date cited are the sealed capture's",
         "a manifest copy whose retrieval date is one day off",
         "a date or URL in the manifest or the fee file differs from FEE_SOURCE.json's, or FEE_SOURCE.json "
         "moved since the seal",
         lambda: plants([("a manifest COPY whose retrieval date is another day", "TOLL-E",
                          lambda: date_findings(off, FEES, FEE_SRC))]),
         lambda: _ok(date_findings(MAN, FEES, FEE_SRC),
                     "the manifest's fee_sources and the fee file's venue blocks cite, per venue, the URL and "
                     "the calendar date of the sealed FEE_SOURCE.json: "
                     + str({v: (s['url'], s['retrieved_utc_date']) for v, s in FEE_SRC['venues'].items()})
                     + "; `retrieved` is null where the venue is not PUBLISHED")),
        ("F-TOLL [data f]", "the independent second extractor agrees",
         "a grammar copy whose maker pattern is bent to capture the neighbouring (taker) figure",
         "the fixture's own second extractor — a structural parse of the body, not the grammar's patterns — "
         "run on the same bytes under the same definition disagrees with the figure of record",
         lambda: plants([("a grammar COPY whose maker pattern captures the taker figure, run through the "
                          "production extractor on the same bytes", "TOLL-F",
                          lambda: second_findings(PAGE_T, bent_grammar))]),
         f_real),
        ("F-TOLL [data g]", "each row's maker is its venue block's; the blocks are the Stage D table's venues",
         "a row whose maker differs from its venue block",
         "a row's maker_bps_side != its maker_bps_per_side != its venue block's figure, or the venue blocks do "
         "not cover exactly the venues of the Stage D table",
         lambda: plants([("a row whose maker differs from its venue block (COPY)", "TOLL-G",
                          lambda: venue_row_findings(_bent(("assets", 3, "maker_bps_side"), 1.0))),
                         ("a venue block dropped in a COPY", "TOLL-G the venue blocks",
                          lambda: venue_row_findings({**FEES, "venues": {v0: FEES["venues"][v0]}}))]),
         lambda: _ok(venue_row_findings(FEES),
                     "the pin lines of the manifest: " + " | ".join(MAN["pins"]["maker-bps"]["lines"])
                     + f" — every one of the {len(FEES['assets'])} rows carries its venue block's figure under "
                       f"both keys; the blocks are exactly the Stage D table's venues")),
    ]


# ═══════════════════════════════════════════════ F-TICK [a] … [d]
def tick_cases(ticks) -> list:
    """(tick, level n, decimal string of x) — on-grid levels, one finer decimal place above and
    below, exact boundaries, and decimals longer than a float64 round-trips."""
    cases = []
    for tk in sorted(set(ticks) | {"0.1", "0.01", "0.5", "0.25"}):
        T = Decimal(tk)
        finer = T / 10
        for n in (1, 2, 3, 7, 10, 97, 1000, 123457):
            base = n * T
            for x in (base, base + finer, base - finer, base + T, base - T if n > 1 else base):
                cases.append((tk, n, format(x, "f")))
            cases.append((tk, n, format(base + Decimal("1E-30"), "f")))
            cases.append((tk, n, format(base - Decimal("1E-30"), "f")))
    return cases


def tick_findings(grid_cls, ticks) -> list:
    """TICK-A: a method disagrees with the brute-force Fraction evaluation, as a float or a Decimal;
    or [AM-59] a float level n is accepted by one of the four level comparisons."""
    out = []
    for tk, n, s in tick_cases(ticks):
        g = grid_cls(tk)
        ft, long_ = Fraction(tk), len(s.replace(".", "").lstrip("0")) > 15
        forms = [("Decimal", Decimal(s), Fraction(s))]
        if not long_:
            forms.append(("float", float(s), Fraction(repr(float(s)))))
        for kind, x, fx in forms:
            q = fx // ft
            want = {"floor_ticks": int(q), "ceil_ticks": int(q) + (0 if fx % ft == 0 else 1),
                    "on_grid": fx % ft == 0, "lt": fx < n * ft, "le": fx <= n * ft, "gt": fx > n * ft,
                    "ge": fx >= n * ft}
            got = {"floor_ticks": g.floor_ticks(x), "ceil_ticks": g.ceil_ticks(x), "on_grid": g.on_grid(x),
                   "lt": g.lt(x, n), "le": g.le(x, n), "gt": g.gt(x, n), "ge": g.ge(x, n)}
            bad = sorted(k for k in want if got[k] != want[k])
            if bad:
                out.append(f"TICK-A tick {tk} level {n} x = {s} as {kind}: {bad} disagree with Fraction")
                if len(out) > 5:
                    return out
    g = grid_cls(sorted(ticks)[0])
    for label, x in (("an int", 1), ("a str", "1.0"), ("a numpy.float32", np.float32(1.5)), ("nan", float("nan")),
                     ("inf", float("inf")), ("a negative", -1.0), ("zero", 0.0), ("a bool", True)):
        try:
            g.floor_ticks(x)
            out.append(f"TICK-A {label} was accepted")
        except SystemExit:
            pass
    if g.dec(g.px(7)) != 7 * g.T:
        out.append("TICK-A px(n) does not round-trip")
    x = g.px(7)                         # AM-59: a float level must HALT — an admissible x, the level 7 as a float
    for m in ("lt", "le", "gt", "ge"):
        try:
            getattr(g, m)(x, 7.0)
            out.append(f"TICK-A a float level was accepted by {m}")
        except SystemExit:
            pass
    return out


def tick_class(old: str, new: str):
    ns: dict = {}
    exec(compile(mut(TICK_TEXT, old, new), "<TickGrid copy>", "exec"), ns)       # noqa: S102  (a fixture's plant)
    return ns["TickGrid"]


def tick_literal_findings(name: str, src: str, ticks) -> list:
    """TICK-LITERAL: a numeric or string literal equal as Decimal to a captured tick in an
    assignment or comparison naming `tick`; TICK-FLOAT-COMPARE: a BinOp with a tick-named operand
    under a Compare."""
    held, out = {Decimal(t) for t in ticks}, []

    def ticky(n) -> bool:
        w = n.id if isinstance(n, ast.Name) else n.attr if isinstance(n, ast.Attribute) else ""
        return "tick" in w.lower()

    def literals(node):
        for c in ast.walk(node):
            if isinstance(c, ast.Constant) and type(c.value) in (int, float, str):
                try:
                    if Decimal(str(c.value)) in held:
                        out.append(f"TICK-LITERAL {name}: the tick typed as the literal {c.value!r}")
                except ArithmeticError:
                    pass

    for n in ast.walk(ast.parse(src)):
        if isinstance(n, ast.Compare):
            sides = [n.left] + list(n.comparators)
            if any(ticky(x) for s in sides for x in ast.walk(s)):
                for s in sides:
                    literals(s)
            for b in ast.walk(n):
                if isinstance(b, ast.BinOp) and (ticky(b.left) or ticky(b.right)):
                    out.append(f"TICK-FLOAT-COMPARE {name}: `{ast.unparse(b)}` under a comparison")
        elif isinstance(n, (ast.Assign, ast.AnnAssign, ast.AugAssign)) and n.value is not None:
            targets = n.targets if isinstance(n, ast.Assign) else [n.target]
            if any(ticky(x) for t in targets for x in ast.walk(t)):
                literals(n.value)
    return out


def tick_used_findings(specs: dict, audit: dict, man: dict) -> list:
    cap = {a["stem"]: a.get("price_tick") for a in specs["assets"]}
    out = []
    for stem in PANEL17_T:
        if type(cap.get(stem)) is not str:
            out.append(f"TICK-C {stem}: the capture holds no price_tick string")
        elif audit["ticks"].get(stem) != cap[stem] or man["tick_of_record"]["per_stem"][stem]["tick_used"] != cap[stem] \
                or man["tick_of_record"]["per_stem"][stem]["tc12"]["price_tick"] != cap[stem]:
            out.append(f"TICK-C {stem}: the tick the audit / the manifest used is not the sealed capture's string")
    return out


def cell_recount(key: str) -> tuple[int, int]:
    """One (stem, lens, segment, field) cell by the fixture's own Fraction arithmetic."""
    stem, iv, seg, field = key.split("|")
    df = KL(stem, iv)
    close = df["open_time"].to_numpy(np.int64) + STEP_T[iv]
    era = int(AUDIT_ERA_CUT)
    mask = {"tuning": close <= era, "holdout_to_tc11_pin": (close > era) & (close <= T11_PIN_MS),
            "strip": (close > T11_PIN_MS) & (close <= PIN_MS)}[seg]
    vals, counts = np.unique(df[field].to_numpy(np.float64)[mask], return_counts=True)
    tk = Fraction(next(a["price_tick"] for a in SPECS["assets"] if a["stem"] == stem))
    on = sum(int(c) for v, c in zip(vals, counts) if Fraction(repr(float(v))) % tk == 0)
    return int(mask.sum()), on


AUDIT_ERA_CUT = FX.literal_from_text((ROOT / "scripts" / "tierc11_env.py").read_text(encoding="utf-8"), "ERA_CUT_MS")


def tick_cell_findings(audit: dict, keys) -> list:
    out = []
    for k in keys:
        n, on = cell_recount(k)
        c = audit["cells"][k]
        if (c["n"], c["n_on_grid"], c["share"]) != (n, on, f"{on}/{n}"):
            out.append(f"TICK-D {k}: the audit's n_on_grid {c['n_on_grid']} of n {c['n']} (share {c['share']}) != the "
                       f"Fraction recount {on}/{n}")
    return out


def tick_legs() -> list:
    ticks = sorted({a["price_tick"] for a in SPECS["assets"]})
    from tierc12_tick import TickGrid
    srcs = scoped_sources()
    first = sorted(srcs)[0]
    cells = sorted(AUDIT["cells"])
    rng = FX.stream(np, SEED, TAG, "F-TICK [d]")
    picked = [cells[int(i)] for i in sorted(rng.choice(len(cells), size=TICK_CELLS_T, replace=False))]
    bent_specs = copy.deepcopy(SPECS)
    bent_specs["assets"][0]["price_tick"] = "0.5"
    bent_audit = copy.deepcopy(AUDIT)
    bent_audit["cells"][picked[0]]["n_on_grid"] += 1

    def c_real():
        bad = tick_used_findings(SPECS, AUDIT, MAN)
        if SEAL["files"]["CONTRACT_SPECS.json"]["sha256"] != sha_f(OUT / "CONTRACT_SPECS.json"):
            bad.append("TICK-C the capture moved since the seal")
        return _ok(bad, "the tick TICK_GRID_AUDIT.json and the manifest's tick_of_record used is, per stem and as "
                        "a string, the sealed capture's assets[].price_tick: "
                        + " ".join(f"{a['stem'].replace('USDT', '')}={a['price_tick']}" for a in SPECS["assets"])
                        + f"; ticks moved vs TC11's capture: {MAN['tick_of_record']['ticks_moved_vs_tc11'] or 'none'}; "
                          f"months where the tape's granularity is COARSER than the recorded tick: "
                          f"{AUDIT['n_coarser_months']} of {AUDIT['months_measured']} stem-months "
                        + (str(sorted({c['stem'] for c in AUDIT['coarser_months']})) + " "
                           + f"({AUDIT['coarser_months'][0]['month']} … "
                             f"{AUDIT['coarser_months'][len(AUDIT['coarser_months']) - 1]['month']})"
                           if AUDIT["coarser_months"] else ""))

    return [
        ("F-TICK [a]", "TickGrid == a brute-force Fraction evaluation, floats and Decimals alike",
         "a TickGrid copy whose lt compares in float; a copy whose dec passes a Decimal through float; a copy "
         "whose level check is removed",
         "floor_ticks, ceil_ticks, on_grid or one of the four comparisons disagrees with a brute-force Fraction "
         "evaluation on the enumerated cases (every captured tick x levels on-grid, one finer decimal place "
         "above and below, exact boundaries; each as a float and as a Decimal, plus Decimals longer than a "
         "float64 round-trips); or an x of another type, a non-finite or a non-positive x is accepted; or a "
         "float level n is accepted by lt, le, gt or ge [AM-59: a float level must HALT]",
         lambda: plants([
             ("a TickGrid copy whose lt is `x < n*float(T)` in float", "TICK-A",
              lambda: tick_findings(tick_class("        below = n - 1\n        return self.floor_ticks(x) <= below",
                                               "        return float(x) < n * float(self.T)"), ticks)),
             ("a TickGrid copy whose dec passes a Decimal through float", "TICK-A",
              lambda: tick_findings(tick_class("        elif isinstance(x, Decimal):\n            d = x",
                                               "        elif isinstance(x, Decimal):\n"
                                               "            d = Decimal(repr(float(x)))"), ticks)),
             ("a TickGrid copy that admits an int", "TICK-A an int was accepted",
              lambda: tick_findings(tick_class("        if isinstance(x, float):", "        if isinstance(x, (float, int)):"),
                                    ticks)),
             ("a TickGrid copy whose level check is removed (AM-59)", "TICK-A a float level was accepted",
              lambda: tick_findings(tick_class(
                  "        if type(n) is not int:\n"
                  "            halt(f\"{name}(x, n) takes an int level, got {type(n).__name__}\")\n"
                  "        return n", "        return n"), ticks)),
         ]),
         lambda: _ok(tick_findings(TickGrid, ticks),
                     f"{len(tick_cases(ticks))} enumerated cases over {len(set(ticks) | {'0.1', '0.01', '0.5', '0.25'})} "
                     f"ticks ({len(ticks)} captured tick strings): the seven methods equal the Fraction evaluation as "
                     f"a float and as a Decimal (and on 31-digit Decimals); an int, a str, a numpy.float32, a "
                     f"bool, nan, inf, a negative and zero HALT; px round-trips; a float level HALTs in each of "
                     f"lt, le, gt and ge [AM-59]")),
        ("F-TICK [b]", "no scoped source types a tick or compares a price in float",
         "a typed captured tick assigned to `tick` in a copy of a scoped source",
         "a non-fixture scripts/tierc12_*.py in this suite's scope holds a tick as a literal (a numeric or "
         "string literal equal as Decimal to a captured tick in an assignment or comparison naming `tick`) "
         "or compares a price to `x - tick` / `x + tick` in float (a BinOp with a tick-named operand under a "
         "Compare)",
         lambda: plants([
             ("a captured tick typed and assigned to `tick` in a copy", "TICK-LITERAL",
              lambda: tick_literal_findings(first, srcs[first] + f"\ntick = {ticks[0]}\n", ticks)),
             ("a float `low < limit - tick` compare in a copy", "TICK-FLOAT-COMPARE",
              lambda: tick_literal_findings(first, srcs[first] + "\n\ndef f(low, limit, tick):\n"
                                                                  "    return low < limit - tick\n", ticks)),
         ]),
         lambda: _ok([x for rel, s in srcs.items() for x in tick_literal_findings(rel, s, ticks)],
                     f"{len(srcs)} scoped non-fixture sources hold no captured tick as a literal and no float "
                     f"compare against `x ± tick`")),
        ("F-TICK [c]", "the tick used is the sealed capture's string",
         "a price_tick altered in a COPY of the specs",
         "the tick per stem that TICK_GRID_AUDIT.json and the manifest's tick_of_record used is not, as a "
         "string, the sealed capture's assets[].price_tick; a panel stem lacks one; or the capture moved since "
         "the seal",
         lambda: plants([("a price_tick altered in a COPY of the specs", "TICK-C",
                          lambda: tick_used_findings(bent_specs, AUDIT, MAN))]),
         c_real),
        ("F-TICK [d]", "the on-grid shares == the fixture's own Fraction recount on three seeded cells",
         "the n_on_grid of one of the three seeded cells altered by one in a COPY of the audit",
         f"the on-grid shares recomputed by the fixture's own Fraction code for {TICK_CELLS_T} (stem, lens, "
         f"segment, field) cells — drawn without replacement from the key-sorted cells on the stream "
         f"default_rng([SEED, crc32('data|F-TICK [d]')]) — differ from TICK_GRID_AUDIT.json",
         lambda: plants([("the n_on_grid of a seeded cell altered by one in a COPY of the audit", "TICK-D",
                          lambda: tick_cell_findings(bent_audit, picked))]),
         lambda: _ok(tick_cell_findings(AUDIT, picked),
                     f"the {TICK_CELLS_T} seeded cells of {len(cells)}: "
                     + " · ".join(f"{k} = {AUDIT['cells'][k]['share']}" for k in picked)
                     + " — each equal to the Fraction recount (n and n_on_grid)")),
    ]


# ═══════════════════════════════════════════════ F-MIRROR (--stage=TC12-D.mirror; PROVENANCE)
MIRROR_SELF_T = ("STAGE_D_MANIFEST.json", "SHA256SUMS")


def mirror_plan_t() -> dict:
    """The fixture's own plan: {<root>/<rel>: sha256} from the manifest and FEE_SOURCE.json."""
    plan = {f"snapshots/{f['path']}": f["sha256"] for f in MAN["files"] + MAN["out_of_scope_snapshot_files"]}
    for v, s in sorted(FEE_SRC["venues"].items()):
        if s.get("body_sha256"):
            plan[f"provenance/fee_source/{v}.body"] = s["body_sha256"]
    return plan


def mirror_tree_findings(snap_dst: Path, prov_dst: Path, plan: dict, self_files=MIRROR_SELF_T) -> list:
    """MIRROR-SHA: a mirrored file re-read from the destination differs from the manifest's sha;
    MIRROR-FILE-SET: the destination's file set is not the manifest's."""
    roots = {"snapshots": snap_dst, "provenance": prov_dst}
    out = []
    for key in sorted(plan):
        root, rel = key.split("/", 1)
        q = roots[root] / rel
        if not q.is_file():
            out.append(f"MIRROR-FILE-SET {key}: absent from the mirror")
        elif sha_f(q) != plan[key]:
            out.append(f"MIRROR-SHA {key}: sha != manifest")
    for root, d in roots.items():
        want = {k.split("/", 1)[1] for k in plan if k.startswith(root + "/")}
        want |= set(self_files) if root == "snapshots" else set()
        have = set(D.tree_files(d)) if d.is_dir() else set()
        if have != want:
            out.append(f"MIRROR-FILE-SET {root}: only in the mirror {sorted(have - want)[:4]}, only in the "
                       f"manifest {sorted(want - have)[:4]}")
    return out


def mirror_attest_findings(att: dict, plan: dict) -> list:
    out = []
    if att["manifest"]["sha256"] != sha_f(OUT / "STAGE_D_MANIFEST.json"):
        out.append("MIRROR-ATTEST the attestation names another manifest sha than the filed manifest's")
    if att["n_files"] != len(plan) or set(att["files"]) != set(plan) \
            or any(att["files"][k]["sha256"] != plan[k] or not att["files"][k]["equal"] for k in plan):
        out.append("MIRROR-ATTEST the attestation's file list is not the manifest's")
    if not att["all_equal"] or att["faults"]:
        out.append("MIRROR-ATTEST the attestation does not say all equal")
    return out


def mirror_leg():
    title = "the LaCie mirror, re-read from the destination, is the manifest's bytes"
    p = OUT / "MIRROR_ATTEST.json"
    import drive_wait
    drive_wait.WAKE_LOG = TMP / "WAKE.md"                     # a fixture writes nothing but its transcript
    r = drive_wait.wait_for_drive(LACIE_T)
    if not r.ok:
        FX.not_run("F-MIRROR", title, f"the drive is unreachable ({LACIE_T} {r.state} after {r.attempts} "
                                      f"attempts) — MIRROR NOT RUN; nothing waits on it [L-D.24]")
        return
    if not p.exists():
        FX.not_run("F-MIRROR", title, "no mirror was made: MIRROR_ATTEST.json is not on file (--mirror NOT RUN)")
        return
    att, plan = jload(p), mirror_plan_t()
    snap_dst, prov_dst = Path(att["destination"]["snapshot"]), Path(att["destination"]["provenance"])
    sub = {k: v for k, v in plan.items() if k.startswith("snapshots/funding/")}

    def temp_mirror(edit) -> list:
        tmp = temp_dir("mirror")
        shutil.copytree(snap_dst / "funding", tmp / "funding")
        edit(tmp)
        return mirror_tree_findings(tmp, tmp / "none", sub, self_files=())

    def flip(tmp):
        q = tmp / "funding" / "BTCUSDT.parquet"
        raw = bytearray(q.read_bytes())
        raw[len(raw) // 2] ^= 1
        q.write_bytes(bytes(raw))

    def real():
        bad = mirror_tree_findings(snap_dst, prov_dst, plan) + mirror_attest_findings(att, plan)
        bad += temp_mirror(lambda tmp: None)                 # control: an unbent temp copy is clean
        if (snap_dst / MIRROR_SELF_T[0]).is_file() and sha_f(snap_dst / MIRROR_SELF_T[0]) != att["manifest"]["sha256"]:
            bad.append("MIRROR-ATTEST the manifest copy in the destination is not the filed manifest")
        return _ok(bad, f"{len(plan)} mirrored files ({att['bytes']} bytes) re-read from "
                        f"{att['destination']['snapshot']} and {att['destination']['provenance']} hash to "
                        f"STAGE_D_MANIFEST.json's shas (in-scope and out-of-scope; the fee-source bodies to "
                        f"FEE_SOURCE.json's — {sum(1 for k in plan if k.startswith('provenance/'))} on file); the "
                        f"destination's file set is the manifest's plus {list(MIRROR_SELF_T)}; "
                        f"MIRROR_ATTEST.json states the manifest sha and the file list truly; drive "
                        f"{r.state}; stated limit: a read served from the OS cache cannot be told from a read "
                        f"off the platter")

    FX.prove("F-MIRROR", title,
             "one byte flipped in a TEMP copy of the mirror tree; one file removed from the temp copy",
             "any mirrored file re-read from the LaCie differs from the manifest's sha, the file sets differ, or "
             "MIRROR_ATTEST.json mis-states either",
             lambda: plants([
                 ("one byte flipped in a TEMP copy of the mirror's funding tree", "MIRROR-SHA", lambda: temp_mirror(flip)),
                 ("one file removed from the temp copy", "MIRROR-FILE-SET",
                  lambda: temp_mirror(lambda tmp: (tmp / "funding" / "BTCUSDT.parquet").unlink())),
                 ("a file's sha altered in a COPY of the attestation", "MIRROR-ATTEST",
                  lambda: mirror_attest_findings({**att, "files": {**att["files"], sorted(plan)[0]: {
                      "sha256": "0" * 64, "equal": True}}}, plan)),
             ]),
             real)


# ═══════════════════════════════════════════════ the roll and main
def data_rows() -> list:
    return [
        ("F-D-GUARD", "the frozen-substrate guard",
         "each bad NAIAD_CACHE_DIR; a guard copy with its final equality test removed",
         "the guard accepts an unset variable, a '~' or relative spelling, the live cache or a directory inside "
         "it, the TC10 or the TC11 snapshot, a foreign directory, or the TC12 path without klines/; or "
         "importing the module in a fresh interpreter under any of those does not HALT before engine.data loads",
         guard_break, guard_real),
        ("F-D-BOUND", "every snapshot write behind _assert_bound(); every file write in a typed owner",
         "NAIAD_CACHE_DIR moved mid-process; a barrier removed in a source copy; a raw to_parquet appended",
         "a call that writes the snapshot does not sit behind _assert_bound() on every path, or a file-writing "
         "call sits outside the typed write owners",
         bound_break, bound_real),
        ("F-D-PORT", "the port law: VERBATIM / TEXT-ONLY / CHANGED against scripts/tierc11_data.py",
         "one token changed in a VERBATIM port; a comparison flipped in a TEXT-ONLY port; a wrong sha in a comment",
         "a port labelled VERBATIM is not AST-identical to its function in scripts/tierc11_data.py at the sha "
         "TC11's PROGRESS certifies; a TEXT-ONLY port differs from it once string constants are blanked; a "
         "provenance comment names the wrong lines or sha; or the port set read off the comments is not PORTS",
         port_break, port_real),
        ("F-D-CLONE", "the clone re-hashed against TC11's manifest before any extension",
         "a flipped byte in a temp copy; a stray file added to a temp tree",
         "any cloned file's sha differs from TC11's manifest, the clone's file set differs from the source's, "
         "or CLONE_ATTEST.json is not write-once",
         clone_break, clone_real),
        *pin_legs(),
        ("F-D-SCOPE", "the fetch scope is TC11's scope of record, by object",
         "a path dropped; a 15m path added for a non-CLASSIC5 stem",
         "scope_paths(), PRE_STATE.json's files or the manifest's files[].path differ as a set from TC11's "
         "manifest files[].path",
         scope_break, scope_real),
        ("F-D-FETCHPATH", "the fetch path, offline: its HALTs, the resume, the order, the replay",
         "each HALT's condition on temp copies; a one-bar overlap; run_fetch copies that fetch before "
         "write_pre_state or capture the flat bars before the 5m extension",
         "a HALT of the fetch path does not fire, a --fetch resume over the filed snapshot asks or saves "
         "anything, the flat-bar capture runs before the extension is complete, an extension can start at or "
         "behind a file's PRE_STATE edge, or the fetch path replayed from clone-time bytes does not reproduce "
         "the filed content",
         fetchpath_break, fetchpath_real),
        ("F-D-FORMING", "no bar that is not closed at the pin can reach a file",
         "a copy of extend_klines with the [lo, hi] filter deleted; a stub venue clock at the pin",
         "any row past the lens's last bar closing <= the pin is saved to the TEMP snapshot, or a stub venue "
         "clock <= the pin does not HALT",
         forming_break, forming_real),
        ("F-D-VENUE", "venue of record; never spliced",
         "a default-named twin; a fetch row from the other venue; one flipped venue in a probe copy",
         "TC10's Stage D table, the probe and TC11's manifest venues[] disagree on any row; a file's venue is "
         "not its asset's; a fetch for a stem came from another venue; or an alternate-venue tape lacks the "
         "venue in its stem or has a default-named twin",
         venue_break, venue_real),
        ("F-D-MANIFEST", "the manifest: TC11's schema under the rename table; every sha re-hashes; .md == .json",
         "a key dropped; a row's sha altered; one figure changed in the .md",
         "a top-level or row key set differs from TC11's under the rename table, a filed sha does not re-hash, "
         "or the .md disagrees with the .json",
         manifest_break, manifest_real),
        ("F-D-SEAL", "the seven sealed records and the fetch log's line prefix",
         "a sealed record rewritten in a temp copy; a fetch-log sealed line changed",
         "one of the seven sealed records, or a sealed line of the fetch log, is not the bytes the seal pinned",
         seal_break, seal_real),
        *prefix_legs(),
        *fd2_legs(),
        ("F-D-3", "funding coverage per asset (all 17)",
         "a print 10 ms before its hour; one 30 min past it; a tape absent; a tail cut by four prints; a "
         "missing file handed to the loader",
         "any panel stem's funding file is absent or empty, its last stamp is older than the pin minus one "
         "observed interval, load_funding returns {}, any print's floor hour differs from its nearest hour, "
         "the loader's funding_hour_ms is missing or wrong, or a print of an hour after the pin is returned",
         fd3_break, fd3_real),
        ("F-D-EDGE", "every file ends exactly at the pin's edge and is truly described",
         "a row past the pin; a tape truncated by one bar; a manifest row with a moved sha; a 404 log row",
         "a kline file does not end exactly at its lens's last bar closing <= the pin, has a duplicate, an "
         "off-grid stamp or a row past the pin; a funding tape stops short of the pin's hour, repeats a print "
         "or holds a print past pin + jitter; the manifest mis-describes a file (sha, rows, flags, content "
         "sha); or a status 404 sits among the fetch phase's HTTP rows",
         edge_break, edge_real),
        ("F-D-DERIVE", "1d / 1w are the plain loop's rebuild from native 4h, bit for bit",
         "a 1d that keeps a five-bar day; weeks anchored on the epoch (Thursday); a naive volume sum",
         "1d / 1w recomputed from native 4h by a plain loop sharing no code with derive_1d / derive_1w differ "
         "by one bit from the derived files (the COMPENSATED sum stated explicitly), the manifest's content "
         "shas of a derived file and of its derivation are not the loop's, or a week does not open on a Monday",
         derive_break, derive_real),
        ("F-D-OUT", "--out cannot name a predecessor's data directory",
         "each bad --out; the guard call removed in a source copy",
         "--out admits research_outputs/tierc10/data or research_outputs/tierc11/data, a symlink or '..' "
         "traversal to either, or the stage directory's parent; or a write of write_manifest does not sit "
         "behind _out_guard()",
         out_break, out_real),
        ("F-D-UNTOUCHED", "the old snapshots and the live cache did not move",
         "one byte flipped in a temp copy of an old-snapshot file",
         "after the build the TC11 snapshot does not re-hash, file for file, to TC11's manifest or the TC10 "
         "snapshot to TC10's manifest; or the live cache's MANIFEST.json stat (size, mtime, inode — stat only, "
         "never opened) moved across this fixture run",
         untouched_break, untouched_real),
        ("F-D-DET", "the determinism set: two hash-seed builds, the filed bytes, no clock",
         "a hash-order-dependent emission; a fee_schedule() copy that stamps datetime.now()'s date",
         "two subprocess --manifest builds (hash seeds 1 and the contract seed) differ from each other or from "
         "the filed bytes in any determinism-set file, hold a different file set, exit non-zero, carry a "
         "clock-named key, or differ in any parquet content sha; OR the call graph of write_manifest holds a "
         "time. / datetime clock call",
         det_break, det_real),
        *toll_legs(),
        *tick_legs(),
    ]


def main() -> int:
    if STAGE_ARG not in STAGES_T:
        raise SystemExit(f"HALT: --stage={STAGE_ARG} is not one of {list(STAGES_T)}")
    substrate = Path(MAN["snapshot_root"]).name
    if substrate != SNAPSHOT_NAME_T or D.SNAPSHOT.name != SNAPSHOT_NAME_T:
        raise SystemExit(f"HALT: the manifest's snapshot {substrate} is not the fixture's typed {SNAPSHOT_NAME_T}")
    banner = {"TC12-D": ("TIER-C12 · STAGE TC12-D — THE SUBSTRATE TOP-UP: fixtures of scripts/tierc12_data.py and "
                         "scripts/tierc12_tick.py [L-D.15] — offline; no leg makes a network call"),
              "TC12-D.mirror": ("TIER-C12 · TC12-D.mirror — F-MIRROR [L-D.24] — the tier's one PROVENANCE "
                                "transcript (it depends on a mounted drive)")}[STAGE_ARG]
    try:
        fixtures = data_rows() if STAGE_ARG == "TC12-D" else [("F-MIRROR", mirror_leg)]
        return FX.run_suite(args=ARGS, root=RUN_ROOT, transcript=TRANSCRIPT_T[STAGE_ARG], banner=banner, seed=SEED,
                            fixtures=fixtures, substrate=substrate, as_of_iso=PIN_ISO, pin=PIN_MS, typed=TYPED_LINES)
    finally:
        shutil.rmtree(TMP, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
