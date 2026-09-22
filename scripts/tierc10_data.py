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
  8. AUDITS (--audit-rest / --audit-archive, read-only): the venue publishes
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
Exit: 0 complete · 2 fetch incomplete (re-run resumes) · 1 HALT.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
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
            "assets": rows}


WARRANTY = ("these files are described AS OF the pinned last closed 4h bar named "
            "here and of no other; bars stamped after it are counted, never read "
            "[TC6V-a, carried by TIER-C10]")


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


def build_manifest(probe: dict, pin: dict, pre: dict) -> dict:
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
    man["complete"] = all(f["present"] and (f["kind"] == "funding" or f["complete_to_as_of"])
                          for f in files) and all(
        f["coverage"]["ok"] for f in files if f["kind"] == "funding" and f["present"])
    return man


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
    man = build_manifest(probe, pin, pre)
    fees = fee_schedule(assets, {f["stem"]: f for f in man["files"]
                                 if f["kind"] == "funding" and f["present"]}, pin)
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
    a = ap.parse_args()
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
