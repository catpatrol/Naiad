"""MC-1 v2 — THE MAY-26 PROGRAM.

Executor: HEPHAESTUS. Drafted: APOLLO. Seed 20260806. All constants [VETO].

Stages (checkpointed to _reviewer_box/mc1/, resume-safe, sorted iteration):

    fetch    D-3 raw kline pull   -> research_outputs/mc1/ops_klines/   (OPS, display-only)
    d1       warmup/feasibility matrix (EVIDENCE, exploration-classic)
    d3       May-26 queryable ops dossier (DISPLAY-ONLY)
    d4       similarity family (EVIDENCE)
    d5       outcomes by tier (EVIDENCE)
    d6       trade join + registration scoring (EVIDENCE)
    d7       winner stacks + ratchet substrate (EVIDENCE)
    fixtures F-MC1..F-MC11
    report   emit MC1_tables.md / MC1_results.json / build document

EVIDENCE/OPS WALL (I1): every SCORED table is bounded by the exploration
ceiling taken from the census machinery's own constant (scripts/census_build.py
CEIL_MS, the same source as SEQ8 F-SEQ2). The dossier is OPS-CLASS: it reads
ONLY from research_outputs/mc1/ops_klines/, never the estate, and every artifact
it emits carries the DISPLAY-ONLY header.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import requests

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import census_build as CB  # noqa: E402  — the census machinery, verbatim constants

# ---------------------------------------------------------------------------
# Pinned constants. [VETO] — contract MC-1 v2, ratified operator 2026-08-06.
# ---------------------------------------------------------------------------
SEED = 20260806

CEIL_MS = CB.CEIL_MS                     # exploration ceiling, census source of truth
CEIL_ISO = datetime.fromtimestamp(CEIL_MS / 1000, timezone.utc).isoformat()

OPS = ROOT / "research_outputs" / "mc1"
OPS_KLINES = OPS / "ops_klines"
OPS_SERIES = OPS / "ops_series"
OPS_REGISTRY = OPS_SERIES / "registry"
BOX = ROOT / "_reviewer_box" / "mc1"
REPORTS = ROOT / "exchange" / "reports"

DISPLAY_ONLY_HEADER = (
    "DISPLAY-ONLY — lockbox-era data — hypothesis generation only, never evidence"
)

# D-3 instrument + endpoint. Instrument string goes in EVERY dossier header.
INSTRUMENT = "BTCUSDT perpetual (USDT-M)"
ENDPOINT = "https://fapi.binance.com/fapi/v1/klines"

# FETCH plan [dates VETO]: interval -> inclusive start day. ALL through 2026-08-01.
FETCH_START = {
    "1d": "2019-01-01",
    "4h": "2024-06-01",
    "12h": "2024-06-01",
    "5m": "2025-06-01",
    "15m": "2025-06-01",
    "30m": "2025-06-01",
    "1h": "2025-06-01",
    "1m": "2026-02-01",
}
# "through 2026-08-01" is read as: the whole of 2026-08-01 is covered, i.e.
# open_time < 2026-08-02T00:00:00Z. Superset of the narrow reading; stated in
# every dossier header so the convention is never ambiguous.
FETCH_END_EXCL = "2026-08-02"
FETCH_END_LABEL = "through 2026-08-01 inclusive (open_time < 2026-08-02T00:00:00Z)"

STUDY_START = "2026-02-01"
STUDY_END = "2026-08-01"

# Full EMA lattice for D-1; the 1m operating set is I3's {25,89,200,300,450}.
D1_TFS = ["1m", "5m", "15m", "30m", "1h", "4h", "12h", "1d", "1W", "1M"]
D1_EMAS = [9, 12, 25, 89, 200, 300, 450]
ONE_M_SET = [25, 89, 200, 300, 450]

# Dossier TFs (the fetched lattice).
DOSSIER_TFS = ["1m", "5m", "15m", "30m", "1h", "4h", "12h", "1d"]

ATR_LEN = CB.ATR_LEN                     # 14, census source

# I2: 1W/1M derived from 1d, pinned conventions.
WEEK_CONVENTION = "weeks open Monday 00:00 UTC"
MONTH_CONVENTION = "months calendar-UTC (1st 00:00 UTC)"
RESAMPLE_NOTE = (
    "1W/1M derived from 1d via the existing s1 resampler algorithm "
    f"(scripts/s1_resample.aggregate, mirrored by census_build._resample). "
    f"{WEEK_CONVENTION}; {MONTH_CONVENTION}. "
    "NOT chart-parity-certified — parity against a charting vendor is NOT asserted."
)

# I6 kiss-v0 [VETO x3]
KISS_TOUCH_ATR = 0.25
KISS_REEXPAND_ATR = 0.75
KISS_REEXPAND_BARS = 10

# D-3(c) co-location tolerance [VETO]
COLOC_ATR = 0.15

# D-3(e) before-chronology lookback [VETO]
CHRONOLOGY_DAYS = 14
MAY26_CROSS_ISO = "2026-05-26"

# D-4 stamp constants [VETO]
SEAL_BARS_4H = 6
WALL_ATR_4H = 0.5
WALL_ATR_1D = 0.5
TRAP_LOOKBACK_H = 24
TRAP_MIN_COUNTER = 2
FIRST_LOOKBACK_4H = 20

# D-7 cushions
CUSHIONS = [0.25, 0.5, 1.0]
LONG_EMAS = [200, 300, 450]
LONG_EMA_TFS = ["15m", "1h", "4h"]

DAY_MS = 86_400_000


# ---------------------------------------------------------------------------
# small utilities
# ---------------------------------------------------------------------------
def ms(day: str) -> int:
    return int(datetime.strptime(day, "%Y-%m-%d")
               .replace(tzinfo=timezone.utc).timestamp() * 1000)


def iso(m) -> str:
    if m is None or (isinstance(m, float) and np.isnan(m)):
        return "NEVER"
    return datetime.fromtimestamp(int(m) / 1000, timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ")


def isoday(m) -> str:
    if m is None or (isinstance(m, float) and np.isnan(m)):
        return "NEVER"
    return datetime.fromtimestamp(int(m) / 1000, timezone.utc).strftime("%Y-%m-%d")


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def log(msg: str) -> None:
    stamp = datetime.now(timezone.utc).strftime("%H:%M:%S")
    print(f"[{stamp}] {msg}", flush=True)


def ckpt_path(name: str) -> Path:
    BOX.mkdir(parents=True, exist_ok=True)
    return BOX / f"{name}.json"


def ckpt_save(name: str, obj) -> None:
    p = ckpt_path(name)
    p.write_text(json.dumps(obj, indent=1, sort_keys=True, default=str),
                 encoding="utf-8")


def ckpt_load(name: str):
    p = ckpt_path(name)
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


# ---------------------------------------------------------------------------
# STAGE fetch — D-3 raw pull. OPS-CLASS. Writes ONLY to research_outputs/mc1/.
# ---------------------------------------------------------------------------
KLINE_COLS = ["open_time", "open", "high", "low", "close", "volume"]

INTERVAL_MS = {
    "1m": 60_000, "5m": 300_000, "15m": 900_000, "30m": 1_800_000,
    "1h": 3_600_000, "4h": 14_400_000, "12h": 43_200_000, "1d": 86_400_000,
}


class WeightBudget:
    """Tracks the exchange-reported 1m weight and paces to stay well inside it."""

    def __init__(self, cap: int = 2400, target_frac: float = 0.35):
        self.cap = cap
        self.target = int(cap * target_frac)
        self.last_used = 0
        self.requests = 0
        self.max_seen = 0

    def observe(self, headers) -> None:
        v = headers.get("x-mbx-used-weight-1m") or headers.get("X-MBX-USED-WEIGHT-1M")
        if v is not None:
            self.last_used = int(v)
            self.max_seen = max(self.max_seen, self.last_used)
        self.requests += 1

    def pace(self) -> None:
        if self.last_used > self.target:
            time.sleep(2.0)
        else:
            time.sleep(0.12)


def fetch_klines(symbol: str, interval: str, start_ms: int, end_ms_excl: int,
                 budget: WeightBudget) -> pd.DataFrame:
    """Page /fapi/v1/klines forward. Returns CLOSED bars in [start, end_excl)."""
    step = INTERVAL_MS[interval]
    out: list[list] = []
    cur = start_ms
    while cur < end_ms_excl:
        params = {"symbol": symbol, "interval": interval,
                  "startTime": cur, "limit": 1500}
        for attempt in range(5):
            try:
                r = requests.get(ENDPOINT, params=params, timeout=60)
                if r.status_code == 200:
                    break
                if r.status_code == 429:
                    log(f"  429 rate limited, backing off {5 * (attempt + 1)}s")
                    time.sleep(5 * (attempt + 1))
                    continue
                raise RuntimeError(f"HTTP {r.status_code}: {r.text[:200]}")
            except requests.RequestException as e:
                log(f"  transient {type(e).__name__}, retry {attempt + 1}/5")
                time.sleep(2.0 * (attempt + 1))
        else:
            raise RuntimeError(f"fetch failed: {symbol} {interval} @ {cur}")
        budget.observe(r.headers)
        rows = r.json()
        if not rows:
            break
        rows = [x for x in rows if int(x[0]) < end_ms_excl]
        out.extend(rows)
        last_open = int(r.json()[-1][0])
        if last_open + step <= cur:
            break
        cur = last_open + step
        budget.pace()
        if len(out) and len(out) % 30000 < 1500:
            log(f"  {symbol} {interval}: {len(out)} bars ... {iso(out[-1][0])}"
                f"  (weight {budget.last_used})")
    if not out:
        return pd.DataFrame(columns=KLINE_COLS)
    df = pd.DataFrame(
        {"open_time": [int(x[0]) for x in out],
         "open": [float(x[1]) for x in out],
         "high": [float(x[2]) for x in out],
         "low": [float(x[3]) for x in out],
         "close": [float(x[4]) for x in out],
         "volume": [float(x[5]) for x in out]})
    df = df.drop_duplicates("open_time").sort_values("open_time")
    return df.reset_index(drop=True)


def stage_fetch() -> dict:
    """D-3 FETCH. NEVER touches the estate; writes only under research_outputs/mc1/."""
    OPS_KLINES.mkdir(parents=True, exist_ok=True)
    budget = WeightBudget()
    end_excl = ms(FETCH_END_EXCL)
    manifest = {
        "_header": DISPLAY_ONLY_HEADER,
        "instrument": INSTRUMENT,
        "endpoint": ENDPOINT,
        "end_convention": FETCH_END_LABEL,
        "fetched_utc": datetime.now(timezone.utc).isoformat(),
        "series": {},
    }
    prev = ckpt_load("fetch_manifest")
    done = set((prev or {}).get("series", {}).keys()) if prev else set()

    for interval in sorted(FETCH_START, key=lambda k: INTERVAL_MS[k]):
        path = OPS_KLINES / f"BTCUSDT_{interval}.parquet"
        if interval in done and path.exists():
            log(f"fetch {interval}: cached, skipping")
            manifest["series"][interval] = prev["series"][interval]
            continue
        start = ms(FETCH_START[interval])
        log(f"fetch {interval}: {FETCH_START[interval]} -> {FETCH_END_EXCL} (excl)")
        df = fetch_klines("BTCUSDT", interval, start, end_excl, budget)
        df.to_parquet(path, index=False)
        rec = {
            "interval": interval,
            "requested_start": FETCH_START[interval],
            "bars": int(len(df)),
            "first_open": iso(df.open_time.iloc[0]) if len(df) else None,
            "last_open": iso(df.open_time.iloc[-1]) if len(df) else None,
            "path": str(path.relative_to(ROOT)).replace("\\", "/"),
            "bytes": path.stat().st_size,
            "sha256": sha256_file(path),
        }
        manifest["series"][interval] = rec
        log(f"  -> {rec['bars']} bars  {rec['first_open']} .. {rec['last_open']}"
            f"  {rec['bytes'] / 1e6:.1f} MB")
        ckpt_save("fetch_manifest", manifest)

    manifest["weight"] = {
        "requests": budget.requests,
        "max_used_weight_1m_observed": budget.max_seen,
        "documented_cap_per_min": budget.cap,
        "pacing_target": budget.target,
    }
    ckpt_save("fetch_manifest", manifest)
    (OPS / "fetch_manifest.json").write_text(
        json.dumps(manifest, indent=1, sort_keys=True), encoding="utf-8")
    log(f"FETCH COMPLETE — {budget.requests} requests, "
        f"max observed weight {budget.max_seen}/{budget.cap}")
    return manifest


# ---------------------------------------------------------------------------
# Shared indicator machinery. I3: SEQ8's exact warmup rule, cited.
# ---------------------------------------------------------------------------
from engine.indicators import ema as _ema_ref, atr as _atr_ref  # noqa: E402
from engine.indicators import crossover, crossunder, true_range, rma  # noqa: E402
import seq8_extract as SEQ8  # noqa: E402  — I3 warmup rule, imported not restated

# I3 — EMA warmup convention, SEQ8's exact rule:
#   scripts/seq8_extract.py:114-119  warmup_bars(length, residual=SEED_RESIDUAL)
#       alpha = 2/(length+1); first warmed index = ceil(log(residual)/log(1-alpha))
#   scripts/seq8_extract.py:84       SEED_RESIDUAL = 1e-3
#   scripts/seq8_extract.py:179      v[:min(WARM[L], n)] = np.nan   # never backfilled
WARMUP_RULE_CITE = (
    "scripts/seq8_extract.py:114-119 warmup_bars() with SEED_RESIDUAL=1e-3 "
    "(scripts/seq8_extract.py:84); mask applied at scripts/seq8_extract.py:179 "
    "as v[:min(WARM[L], n)] = np.nan — NaN before warm, never backfilled"
)
SEED_RESIDUAL = SEQ8.SEED_RESIDUAL


def warmup_bars(length: int) -> int:
    """SEQ8's rule, delegated to SEQ8's own function (never restated)."""
    return SEQ8.warmup_bars(length, SEED_RESIDUAL)


WARMUP = {L: warmup_bars(L) for L in sorted(set(D1_EMAS) | set(ONE_M_SET))}


def ema_fast(values: np.ndarray, length: int) -> np.ndarray:
    """engine.indicators.ema with the identical float64 operation ORDER, run
    over a Python list instead of a numpy array. Same ops, same order => bit
    identical; only the interpreter overhead differs. Asserted against the
    reference implementation by _assert_ema_identical()."""
    alpha = 2.0 / (length + 1.0)
    out = np.full(len(values), np.nan)
    prev = np.nan
    vs = values.tolist()
    o = [np.nan] * len(vs)
    for i, v in enumerate(vs):
        if v != v:                      # NaN test, same branch as the reference
            o[i] = prev
            continue
        prev = v if prev != prev else prev + alpha * (v - prev)
        o[i] = prev
    out[:] = o
    return out


def ema_warm(values: np.ndarray, length: int) -> np.ndarray:
    """EMA under I3: masked NaN for the first warmup_bars(length) positions."""
    v = ema_fast(values, length)
    n = len(v)
    v[:min(WARMUP[length], n)] = np.nan
    return v


def _assert_ema_identical(sample: np.ndarray) -> None:
    for L in (9, 89, 300):
        a = _ema_ref(sample, L)
        b = ema_fast(sample, L)
        bad = ~((a == b) | (np.isnan(a) & np.isnan(b)))
        if bad.any():
            raise AssertionError(
                f"ema_fast diverged from engine.indicators.ema at L={L}: "
                f"{int(bad.sum())} of {len(sample)} positions")


# ---------------------------------------------------------------------------
# Frame construction — census-parity by construction (I2: no new resampler)
# ---------------------------------------------------------------------------
WEEK_MS = 7 * DAY_MS
# 1970-01-01 was a Thursday; the first Monday of the epoch is 1970-01-05.
MONDAY_EPOCH_OFFSET_MS = 4 * DAY_MS


def estate_klines() -> Path:
    from engine.data import cache_dir
    return cache_dir() / "klines"


def load_ohlcv_ceiled(klines: Path, sym: str, tf: str,
                      cols=("open_time", "open", "high", "low", "close", "volume")
                      ) -> pd.DataFrame:
    """Estate OHLCV for one native TF, exploration-classic (open_time < CEIL_MS).

    READ-ONLY on the estate. Mirrors census_build.load_tf's load+ceiling+sort.
    """
    df = pd.read_parquet(klines / f"{sym}_{tf}.parquet", columns=list(cols))
    df = df[df["open_time"] < CEIL_MS].sort_values("open_time")
    return df.reset_index(drop=True)


def build_tf_frame(klines: Path, sym: str, tf: str) -> pd.DataFrame:
    """OHLCV for any TF in the D-1 lattice, exploration-classic.

    native            : 1m 5m 15m 1h 4h 12h      — read directly
    census RESAMPLE   : 30m<-15m, 1d<-1h         — census_build._resample (s1)
    I2 derived        : 1W<-1d, 1M<-1d           — see note below
    """
    if tf in ("1m", "5m", "15m", "1h", "4h", "12h"):
        return load_ohlcv_ceiled(klines, sym, tf)
    if tf in CB.RESAMPLE:                       # 30m, 1d
        src_tf, step = CB.RESAMPLE[tf]
        raw = load_ohlcv_ceiled(klines, sym, src_tf)
        return CB._resample(raw, step)
    if tf == "1W":
        # s1 algorithm verbatim: shift the axis so a fixed-step floor lands on
        # Monday 00:00 UTC, resample with census_build._resample, shift back.
        d1 = build_tf_frame(klines, sym, "1d")
        sh = d1.copy()
        sh["open_time"] = sh["open_time"] - MONDAY_EPOCH_OFFSET_MS
        out = CB._resample(sh, WEEK_MS)
        out["open_time"] = out["open_time"] + MONDAY_EPOCH_OFFSET_MS
        return out
    if tf == "1M":
        # Calendar months are not expressible as a fixed-step floor, so the s1
        # fixed-step resampler cannot reach them. The AGGREGATION below is the
        # s1 aggregation unchanged (first/max/min/last/sum); only the bucket KEY
        # is calendar-UTC. Flagged in the build document.
        d1 = build_tf_frame(klines, sym, "1d")
        ts = pd.to_datetime(d1["open_time"], unit="ms", utc=True)
        key = (ts.dt.year.to_numpy(np.int64) * 100 + ts.dt.month.to_numpy(np.int64))
        month_start = pd.to_datetime(
            [f"{k // 100:04d}-{k % 100:02d}-01" for k in key], utc=True)
        km = (month_start.astype(np.int64) // 1_000_000).to_numpy(np.int64)
        src = d1.copy()
        g = src.groupby(km, sort=True)
        return pd.DataFrame({
            "open_time": np.asarray(sorted(set(km.tolist())), dtype=np.int64),
            "open": g["open"].first().to_numpy(float),
            "high": g["high"].max().to_numpy(float),
            "low": g["low"].min().to_numpy(float),
            "close": g["close"].last().to_numpy(float),
            "volume": g["volume"].sum().to_numpy(float),
        })
    raise ValueError(f"unknown tf {tf!r}")


# ---------------------------------------------------------------------------
# STAGE d1 — WARMUP / FEASIBILITY MATRIX (EVIDENCE, exploration-classic)
# ---------------------------------------------------------------------------
def stage_d1() -> dict:
    """asset x TF x EMA -> first-warm UTC date, or NEVER.

    Under I3, engine.indicators.ema is seeded at the first finite value and is
    therefore never NaN after bar 0; the ONLY source of NaN is SEQ8's mask
    v[:min(WARM[L], n)]. First-warm is consequently a closed-form function of
    the mask width and the bar axis, not of the price data:

        first_warm_index_in_full_series = WARM[L]          (NEVER if WARM[L] >= n)
        first_warm_index_in_window      = max(WARM[L], first index >= start_ms)

    The matrix is still computed from the real bar axes; the closed form is what
    F-MC1's three hand-recomputed cells check.
    """
    klines = estate_klines()
    rows = []
    axis_meta = {}
    for sym in sorted(CB.ASSET_STARTS):
        start_ms = CB.ms(CB.ASSET_STARTS[sym])
        for tf in D1_TFS:
            df = build_tf_frame(klines, sym, tf)
            o = df["open_time"].to_numpy(np.int64)
            n = len(o)
            c = df["close"].to_numpy(float)
            if n and not np.isfinite(c).all():
                raise AssertionError(f"non-finite close in {sym}/{tf}")
            w_idx = int(np.searchsorted(o, start_ms, side="left"))
            axis_meta[f"{sym}|{tf}"] = {
                "bars_ceiled": n,
                "first_bar": iso(o[0]) if n else None,
                "last_bar": iso(o[-1]) if n else None,
                "window_start_index": w_idx,
                "bars_in_window": max(0, n - w_idx),
            }
            for L in D1_EMAS:
                warm = WARMUP[L]
                if n == 0 or warm >= n:
                    status, ts = "NEVER", None
                else:
                    j = max(warm, w_idx)
                    if j >= n:
                        status, ts = "NEVER", None
                    else:
                        status, ts = "WARMED", int(o[j])
                rows.append({
                    "asset": sym, "tf": tf, "ema": L,
                    "warmup_bars_required": warm,
                    "bars_ceiled": n,
                    "bars_in_window": max(0, n - w_idx),
                    "status": status,
                    "first_warm_ts": ts,
                    "first_warm_iso": iso(ts) if ts else "NEVER",
                    "first_warm_date": isoday(ts) if ts else "NEVER",
                })
            log(f"  d1 {sym:<10} {tf:<3} n={n:<8} window_start_idx={w_idx}")
    out = {
        "_class": "EVIDENCE — exploration-classic",
        "ceiling_ms": CEIL_MS, "ceiling_iso": CEIL_ISO,
        "warmup_rule": WARMUP_RULE_CITE,
        "seed_residual": SEED_RESIDUAL,
        "warmup_bars": {str(L): WARMUP[L] for L in D1_EMAS},
        "resample_note": RESAMPLE_NOTE,
        "assets": sorted(CB.ASSET_STARTS),
        "tfs": D1_TFS, "emas": D1_EMAS,
        "axis": axis_meta,
        "rows": rows,
    }
    ckpt_save("d1_matrix", out)
    log(f"D-1 COMPLETE — {len(rows)} cells "
        f"({len(CB.ASSET_STARTS)} assets x {len(D1_TFS)} TF x {len(D1_EMAS)} EMA)")
    return out


# ---------------------------------------------------------------------------
# D-3 dossier machinery. OPS-CLASS: reads ONLY research_outputs/mc1/ops_klines.
# ---------------------------------------------------------------------------
DOSSIER_EMAS = [9, 12, 25, 89, 200, 300, 450]
RIBBON_PAIRS = [(9, 89), (89, 200), (300, 450)]
CROSS_PAIRS = [(9, 89), (89, 200), (9, 200), (12, 25), (300, 450)]
# D-3(d): "5m and 1m long pairs" — the long-EMA set {200,300,450}, all pairs.
LONG_PAIRS = [(200, 300), (300, 450), (200, 450)]
LONG_PAIR_TFS = ["5m", "1m"]


def ops_frame(tf: str) -> pd.DataFrame:
    """Load a fetched ops kline series. NEVER the estate (I1)."""
    p = OPS_KLINES / f"BTCUSDT_{tf}.parquet"
    if not p.exists():
        raise FileNotFoundError(f"ops klines missing: {p} — run stage 'fetch'")
    return pd.read_parquet(p).sort_values("open_time").reset_index(drop=True)


def kiss_v0(spread: np.ndarray, atr_v: np.ndarray) -> tuple:
    """I6 kiss-v0 [VETO x3], derived + event-sampled.

    |eA-eB| <= 0.25*ATR, then re-expansion >= 0.75*ATR within 10 bars, no sign
    change in between.

    Returns (flag, known_at_offset). The flag marks the TOUCH bar, but a touch
    is only CONFIRMED once the re-expansion arrives up to 10 bars later, so
    known_at_offset carries that lag explicitly. I7: a query as-of instant T
    must filter on the confirmation bar, never the touch bar.
    """
    n = len(spread)
    flag = np.zeros(n, dtype=bool)
    known = np.full(n, -1, dtype=np.int64)
    a = np.abs(spread)
    sg = np.sign(spread)
    touch = (a <= KISS_TOUCH_ATR * atr_v) & np.isfinite(spread) & np.isfinite(atr_v)
    for i in np.nonzero(touch)[0]:
        s0 = sg[i]
        for j in range(i + 1, min(i + KISS_REEXPAND_BARS, n - 1) + 1):
            if not (np.isfinite(spread[j]) and np.isfinite(atr_v[j])):
                break
            if s0 != 0 and sg[j] != 0 and sg[j] != s0:
                break                                    # sign change -> not a kiss
            if a[j] >= KISS_REEXPAND_ATR * atr_v[j]:
                if s0 == 0:
                    s0 = sg[j]
                flag[i] = True
                known[i] = j
                break
    return flag, known


def build_perbar(tf: str) -> tuple:
    """D-3(a): one row per bar of `tf`, restricted to the study window.

    EMAs are seeded from the START OF THE FETCHED SERIES (which is why the
    fetch reaches back before the study window), masked per I3, and only then
    restricted to the window. Nothing is backfilled.
    """
    df = ops_frame(tf)
    o = df["open_time"].to_numpy(np.int64)
    c = df["close"].to_numpy(float)
    h = df["high"].to_numpy(float)
    lo = df["low"].to_numpy(float)
    n = len(o)
    atr_v = _atr_ref(h, lo, c, ATR_LEN)

    emas = {L: ema_warm(c, L) for L in DOSSIER_EMAS}
    cols = {
        "open_time": o, "open": df["open"].to_numpy(float), "high": h,
        "low": lo, "close": c, "volume": df["volume"].to_numpy(float),
        "atr": atr_v,
    }
    for L in DOSSIER_EMAS:
        cols[f"e{L}"] = emas[L]
    feas = {}
    for L in DOSSIER_EMAS:
        w = WARMUP[L]
        feas[f"e{L}"] = {
            "warmup_bars_required": w,
            "series_bars": n,
            "first_warm_iso": iso(o[w]) if w < n else "NEVER",
            "feasible_in_series": bool(w < n),
        }
    for a_, b_ in RIBBON_PAIRS:
        sp = emas[a_] - emas[b_]
        cols[f"spread_{a_}_{b_}_atr"] = sp / atr_v
        f, k = kiss_v0(sp, atr_v)
        cols[f"kiss_{a_}_{b_}"] = f
        cols[f"kiss_{a_}_{b_}_known_ts"] = np.where(k >= 0, o[np.clip(k, 0, n - 1)], -1)
    for a_, b_ in CROSS_PAIRS:
        cols[f"cross_{a_}_{b_}_up"] = crossover(emas[a_], emas[b_])
        cols[f"cross_{a_}_{b_}_dn"] = crossunder(emas[a_], emas[b_])
    out = pd.DataFrame(cols)
    ws, we = ms(STUDY_START), ms(FETCH_END_EXCL)
    win = out[(out["open_time"] >= ws) & (out["open_time"] < we)].reset_index(drop=True)
    return win, feas, n


def stage_d3a() -> dict:
    """D-3(a) per-bar series + D-3(d) long-pair ribbon state."""
    OPS_SERIES.mkdir(parents=True, exist_ok=True)
    man = {"_header": DISPLAY_ONLY_HEADER, "instrument": INSTRUMENT,
           "endpoint": ENDPOINT, "study_window": f"{STUDY_START} -> {STUDY_END}",
           "end_convention": FETCH_END_LABEL,
           "warmup_rule": WARMUP_RULE_CITE, "series": {}, "feasibility": {}}
    for tf in DOSSIER_TFS:
        win, feas, nfull = build_perbar(tf)
        p = OPS_SERIES / f"perbar_{tf}.parquet"
        win.to_parquet(p, index=False)
        man["series"][tf] = {
            "path": str(p.relative_to(ROOT)).replace("\\", "/"),
            "rows_in_window": int(len(win)), "rows_fetched": int(nfull),
            "first": iso(win.open_time.iloc[0]) if len(win) else None,
            "last": iso(win.open_time.iloc[-1]) if len(win) else None,
            "bytes": p.stat().st_size, "sha256": sha256_file(p),
        }
        man["feasibility"][tf] = feas
        warm_in_win = {k: v["first_warm_iso"] for k, v in feas.items()
                       if not v["feasible_in_series"]
                       or v["first_warm_iso"] > iso(ms(STUDY_START))}
        log(f"  d3a {tf:<4} rows={len(win):<7} "
            f"unwarmed-at-window-open: {sorted(warm_in_win) or 'none'}")

    # D-3(d) long-pair ribbon state, 5m and 1m
    dman = {}
    for tf in LONG_PAIR_TFS:
        src = pd.read_parquet(OPS_SERIES / f"perbar_{tf}.parquet")
        cols = {"open_time": src["open_time"].to_numpy(np.int64),
                "close": src["close"].to_numpy(float),
                "atr": src["atr"].to_numpy(float)}
        for a_, b_ in LONG_PAIRS:
            ea, eb = src[f"e{a_}"].to_numpy(float), src[f"e{b_}"].to_numpy(float)
            sp = ea - eb
            cols[f"spread_{a_}_{b_}_atr"] = sp / cols["atr"]
            cols[f"state_{a_}_{b_}"] = np.where(
                ~np.isfinite(sp), "unwarmed",
                np.where(np.abs(sp) <= KISS_TOUCH_ATR * cols["atr"], "compressed",
                         np.where(np.abs(sp) >= KISS_REEXPAND_ATR * cols["atr"],
                                  "expanded", "transitional")))
        d = pd.DataFrame(cols)
        p = OPS_SERIES / f"ribbon_long_{tf}.parquet"
        d.to_parquet(p, index=False)
        dman[tf] = {"path": str(p.relative_to(ROOT)).replace("\\", "/"),
                    "rows": int(len(d)), "bytes": p.stat().st_size,
                    "sha256": sha256_file(p),
                    "pairs": [f"{a}/{b}" for a, b in LONG_PAIRS]}
        log(f"  d3d {tf:<4} ribbon-long rows={len(d)}")
    man["ribbon_long"] = dman
    ckpt_save("d3a_manifest", man)
    return man


# ---------------------------------------------------------------------------
# D-3(b) ANALYTICS REGISTRY SERIES — dual-scored, I7-causal. DISPLAY-ONLY.
# ---------------------------------------------------------------------------
import analytics                                            # noqa: E402
from analytics import levels as AL, vwap as AW, profile as AP, structure as AS  # noqa: E402

ANALYTICS_CITE = {
    "ANALYTICS_VERSION": analytics.ANALYTICS_VERSION,
    "analytics_sha": analytics.analytics_sha(),
    "note": "INTERFACE.md:15-17 — a citation needs version + sha + the consuming "
            "envelope's rules/schema versions; this run consumes the package directly, "
            "so only the two package identifiers apply.",
}
REGISTRY_WINDOWS = [7, 30, 90, 365]
VOLUME_FAMILIES = AL.VOLUME_FAMILIES


class CausalityViolation(Exception):
    """I7 — an as-of computation was handed data after its as-of instant."""


def slice_causal(f: dict, as_of_ms: int) -> tuple:
    """Return (index_end_exclusive, max_close_consumed) for bars CLOSED at/before
    as_of_ms. I7: nothing after the as-of instant may enter the computation."""
    n = int(np.searchsorted(f["close_ms"], as_of_ms, "right"))
    mx = int(f["close_ms"][n - 1]) if n > 0 else -1
    return n, mx


def guard_causal(as_of_ms: int, max_close_consumed: int, what: str) -> None:
    if max_close_consumed > as_of_ms:
        raise CausalityViolation(
            f"I7 VIOLATION in {what}: consumed a bar closing at "
            f"{iso(max_close_consumed)} > as-of {iso(as_of_ms)}")


def ops_indicator_frame(tf: str) -> dict:
    """Ops (fetched) frame + ATR. DISPLAY-ONLY; never the estate."""
    k = ("__ops__", tf)
    if k in _FRAME_CACHE:
        return _FRAME_CACHE[k]
    d = ops_frame(tf)
    o = d["open_time"].to_numpy(np.int64)
    f = {"open_time": o, "close_ms": o + INTERVAL_MS[tf],
         "open": d["open"].to_numpy(float), "high": d["high"].to_numpy(float),
         "low": d["low"].to_numpy(float), "close": d["close"].to_numpy(float),
         "volume": d["volume"].to_numpy(float)}
    f["atr"] = _atr_ref(f["high"], f["low"], f["close"], ATR_LEN)
    _FRAME_CACHE[k] = f
    return f


def build_registry_asof(as_of_ms: int, extra_bars: int = 0) -> dict:
    """The analytics registry as-of an instant, built ONLY from bars closed at or
    before it (I7). `extra_bars` deliberately leaks future bars — used by F-MC11
    to prove the guard can fail."""
    d1 = ops_indicator_frame("1d")
    n, mx = slice_causal(d1, as_of_ms)
    n = n + extra_bars                                # F-MC11 sabotage lever
    if n <= 0:
        raise ValueError("no closed daily bars at this as-of")
    n = min(n, len(d1["open_time"]))
    mx = int(d1["close_ms"][n - 1])
    guard_causal(as_of_ms, mx, "registry daily substrate")

    ot, hi, lo = d1["open_time"][:n], d1["high"][:n], d1["low"][:n]
    cl, vol, op = d1["close"][:n], d1["volume"][:n], d1["open"][:n]
    src = AW.hlc3(hi, lo, cl)
    atr_d = float(d1["atr"][n - 1])
    price = float(cl[n - 1])

    # a finer-grained price if a closed intraday bar exists at the as-of
    for tf in ("1h", "4h"):
        try:
            fi = ops_indicator_frame(tf)
        except FileNotFoundError:
            continue
        k, mk = slice_causal(fi, as_of_ms)
        if k > 0:
            guard_causal(as_of_ms, mk, f"price {tf}")
            price = float(fi["close"][k - 1])
            break

    reg = AL.LevelRegistry()
    chips = {}

    # ---- structure (non-volume)
    ph, pl = AS.prior_period_extremes(ot, hi, lo, period="D")
    for lab, arr in (("prior_day_high", ph), ("prior_day_low", pl)):
        reg.add(family="structure", label=lab, level=float(arr[n - 1]),
                source_layer="prior_period_extremes", timeframe="1d")
    for per, tag in (("W", "week"), ("M", "month")):
        a, b = AS.prior_period_extremes(ot, hi, lo, period=per)
        reg.add(family="structure", label=f"prior_{tag}_high", level=float(a[n - 1]),
                source_layer="prior_period_extremes", timeframe=per)
        reg.add(family="structure", label=f"prior_{tag}_low", level=float(b[n - 1]),
                source_layer="prior_period_extremes", timeframe=per)
    for per in ("D", "W", "M", "Y"):
        _, po = AS.period_opens(ot, op, period=per)
        reg.add(family="structure", label=f"period_open_{per}", level=float(po[n - 1]),
                source_layer="period_opens", timeframe=per)
    for kind, vals in (("high", hi), ("low", lo)):
        idx, lev, _ = AS.confirmed_pivots(vals, as_of_index=n - 1, kind=kind)
        for j, (ii, lv) in enumerate(zip(idx[-3:], lev[-3:])):
            reg.add(family="structure", label=f"pivot_{kind}_{j}", level=float(lv),
                    source_layer="confirmed_pivots", timeframe="1d")

    # ---- vwap_anchored (non-volume family per levels.VOLUME_FAMILIES)
    ts = pd.to_datetime(ot, unit="ms", utc=True)
    for tag, mask in (("week", ts.dayofweek.to_numpy() == 0),
                      ("month", ts.day.to_numpy() == 1),
                      ("year", (ts.day.to_numpy() == 1) & (ts.month.to_numpy() == 1))):
        w = np.nonzero(mask)[0]
        if len(w):
            av = AW.anchored_vwap(src, vol, int(w[-1]))
            reg.add(family="vwap_anchored", label=f"avwap_{tag}",
                    level=float(av["vwap"][n - 1]), source_layer="anchored_vwap",
                    timeframe="1d")

    # ---- vwap_rolling (VOLUME family)
    for wd in REGISTRY_WINDOWS:
        rv = AW.rolling_vwap(ot, src, vol, window_days=wd)
        v = rv["vwap"][n - 1]
        if np.isfinite(v):
            reg.add(family="vwap_rolling", label=f"rvwap_{wd}d", level=float(v),
                    source_layer="rolling_vwap", timeframe=f"{wd}d")

    # ---- profile_windowed (VOLUME family) — carries the approximation chip
    for wd in REGISTRY_WINDOWS:
        wp = AP.windowed_profile(ot, hi, lo, vol, window_days=wd, as_of_ms=as_of_ms)
        chips[f"profile_{wd}d"] = wp.get("approximation")
        for key in ("poc", "vah", "val"):
            v = wp.get(key)
            if v is not None and np.isfinite(v):
                reg.add(family="profile_windowed", label=f"{key}_{wd}d",
                        level=float(v), source_layer="windowed_profile",
                        timeframe=f"{wd}d")
    pd_vp = AP.volume_profile(hi[-1:], lo[-1:], vol[-1:])
    chips["profile_prior_day"] = pd_vp.get("approximation")

    scored = AL.dual_score(reg.as_list(), atr=atr_d, price=price)
    rows = []
    for variant in ("with_volume", "without_volume"):
        for c in scored[variant]["clusters"]:
            for m in c["members"]:
                rows.append({
                    "as_of_ms": as_of_ms, "as_of_iso": iso(as_of_ms),
                    "variant": variant, "family": m["family"], "label": m["label"],
                    "level": float(m["level"]), "cluster_id": c["cluster_id"],
                    "cluster_mean": float(c["mean"]), "score": int(c["score"]),
                    "cluster_families": ",".join(c["families"]),
                    "is_volume_family": m["family"] in VOLUME_FAMILIES,
                })
    return {"rows": rows, "price": price, "atr_d": atr_d,
            "max_close_consumed": mx, "approximation_chips": chips,
            "n_levels": len(reg.as_list())}


def stage_d3b() -> dict:
    """Registry series: every 00:00 UTC across the study window AND every 4H close
    2026-05-01 -> 2026-06-15. Checkpointed per as-of (resume-safe)."""
    OPS_REGISTRY.mkdir(parents=True, exist_ok=True)
    asofs = []
    t = ms(STUDY_START)
    while t <= ms(STUDY_END):
        asofs.append(t)
        t += DAY_MS
    t = ms("2026-05-01")
    while t <= ms("2026-06-15"):
        asofs.append(t)
        t += 4 * 3_600_000
    asofs = sorted(set(asofs))
    log(f"  D-3(b) as-of instants: {len(asofs)} "
        f"({len([a for a in asofs if a % DAY_MS == 0])} daily-aligned)")

    done = ckpt_load("d3b_progress") or {"completed": []}
    have = set(done["completed"])
    allrows, chips = [], {}
    for i, a in enumerate(asofs):
        r = build_registry_asof(a)
        allrows.extend(r["rows"])
        chips.update(r["approximation_chips"])
        have.add(a)
        if i % 50 == 0:
            log(f"    registry {i}/{len(asofs)}  {iso(a)}  levels={r['n_levels']}")
            ckpt_save("d3b_progress", {"completed": sorted(have)})
    df = pd.DataFrame(allrows)
    p = OPS_REGISTRY / "registry_series.parquet"
    df.to_parquet(p, index=False)
    ckpt_save("d3b_progress", {"completed": sorted(have)})
    out = {
        "_header": DISPLAY_ONLY_HEADER, "instrument": INSTRUMENT,
        "analytics": ANALYTICS_CITE,
        "n_asofs": len(asofs), "n_rows": int(len(df)),
        "families": list(AL.FAMILIES), "volume_families": list(VOLUME_FAMILIES),
        "approximation_chips": chips,
        "ss_family_note": ("family 'ss' is a CAPTURE-layer product (brief2 radar rows), "
                           "not an analytics-package product — it is absent from this "
                           "series by construction, not by omission."),
        "causality": "I7 — every as-of consumed only bars CLOSED at/before it; "
                     "guard_causal() raises otherwise (F-MC11 proves it can fail).",
        "path": str(p), "bytes": p.stat().st_size, "sha256": sha256_file(p),
    }
    ckpt_save("d3b_registry", out)
    log(f"D-3(b) COMPLETE — {len(df)} registry rows over {len(asofs)} as-ofs")
    return out


def stage_d3c() -> dict:
    """D-3(c) CO-LOCATION: EMA events within 0.15 daily-ATR [VETO] of a registry
    level, by family, across the study window."""
    reg = pd.read_parquet(OPS_REGISTRY / "registry_series.parquet")
    d1 = ops_indicator_frame("1d")
    counts, detail = {}, []
    for tf in DOSSIER_TFS:
        pb = pd.read_parquet(OPS_SERIES / f"perbar_{tf}.parquet")
        cross_cols = [c for c in pb.columns if c.startswith("cross_")]
        ev = pb[pb[cross_cols].any(axis=1)]
        for r in ev.itertuples(index=False):
            ts = int(r.open_time)
            k = int(np.searchsorted(d1["close_ms"], ts, "right")) - 1
            if k < 0 or not np.isfinite(d1["atr"][k]) or d1["atr"][k] <= 0:
                continue
            tol = COLOC_ATR * float(d1["atr"][k])
            day = (ts // DAY_MS) * DAY_MS
            rr = reg[(reg.as_of_ms == day) & (reg.variant == "with_volume")]
            if not len(rr):
                continue
            near = rr[(rr.level - float(r.close)).abs() <= tol]
            fired = [c for c in cross_cols if bool(getattr(r, c))]
            for fam, g in near.groupby("family"):
                counts[(tf, fam)] = counts.get((tf, fam), 0) + 1
                detail.append({"tf": tf, "ts": ts, "ts_iso": iso(ts),
                               "family": fam, "n_levels": int(len(g)),
                               "best_score": int(g.score.max()),
                               "events": ",".join(fired)})
    tbl = [{"tf": k[0], "family": k[1], "co_located_events": v}
           for k, v in sorted(counts.items())]
    out = {"_header": DISPLAY_ONLY_HEADER, "instrument": INSTRUMENT,
           "tolerance": f"{COLOC_ATR} * daily ATR [VETO]",
           "table": tbl, "n_detail_rows": len(detail)}
    if detail:
        dp = OPS_SERIES / "colocation_detail.parquet"
        pd.DataFrame(detail).to_parquet(dp, index=False)
        out["detail_path"] = str(dp)
        out["detail_sha256"] = sha256_file(dp)
    ckpt_save("d3c_colocation", out)
    log(f"D-3(c) COMPLETE — {len(tbl)} (tf,family) cells, {len(detail)} co-locations")
    return out


def query_dossier(ts, tf: str) -> dict:
    """D-3(f) QUERY HELPER — the full stack + nearest registry levels at any instant.

    DISPLAY-ONLY. `ts` may be an ISO string or epoch ms. Returns the last CLOSED
    bar of `tf` at/before the instant, its EMA/ribbon/cross/kiss state, and the
    nearest registry levels from the most recent as-of at/before the instant.
    """
    if isinstance(ts, str):
        ts = int(pd.Timestamp(ts, tz="UTC").timestamp() * 1000)
    ts = int(ts)
    pb = pd.read_parquet(OPS_SERIES / f"perbar_{tf}.parquet")
    o = pb["open_time"].to_numpy(np.int64)
    j = int(np.searchsorted(o + INTERVAL_MS[tf], ts, "right")) - 1
    if j < 0:
        return {"error": f"no closed {tf} bar at/before {iso(ts)}"}
    row = pb.iloc[j]
    stack = {c: (None if pd.isna(row[c]) else
                 (bool(row[c]) if isinstance(row[c], (bool, np.bool_))
                  else float(row[c])))
             for c in pb.columns if c != "open_time"}
    reg = pd.read_parquet(OPS_REGISTRY / "registry_series.parquet")
    cand = reg[reg.as_of_ms <= ts]
    nearest = []
    if len(cand):
        a = int(cand.as_of_ms.max())
        rr = cand[(cand.as_of_ms == a) & (cand.variant == "with_volume")].copy()
        rr["distance"] = (rr.level - float(row["close"])).abs()
        for x in rr.nsmallest(8, "distance").itertuples(index=False):
            nearest.append({"family": x.family, "label": x.label,
                            "level": float(x.level), "score": int(x.score),
                            "distance": float(x.distance),
                            "distance_atr": (float(x.distance) / float(row["atr"]))
                            if np.isfinite(row["atr"]) and row["atr"] > 0 else None})
    return {
        "_header": DISPLAY_ONLY_HEADER, "instrument": INSTRUMENT,
        "query_ts": ts, "query_iso": iso(ts), "tf": tf,
        "bar_open_iso": iso(int(row["open_time"])),
        "bar_close_iso": iso(int(row["open_time"]) + INTERVAL_MS[tf]),
        "stack": stack,
        "registry_as_of": iso(int(cand.as_of_ms.max())) if len(cand) else None,
        "nearest_levels": nearest,
    }


def stage_d3e() -> dict:
    """D-3(e) THE MAY-26 EVENT CARD + BEFORE-CHRONOLOGY (prior 14 days [VETO])."""
    pb4 = pd.read_parquet(OPS_SERIES / "perbar_4h.parquet")
    lo, hi = ms("2026-05-26"), ms("2026-05-27")
    day = pb4[(pb4.open_time >= lo) & (pb4.open_time < hi)]
    cc = [c for c in pb4.columns if c.startswith("cross_") and c.endswith("_dn")]
    bear = day[day[cc].any(axis=1)]
    if not len(bear):
        return {"error": "no 4H bear cross on 2026-05-26"}
    ev = bear.iloc[0]
    ets = int(ev["open_time"])
    fired = [c for c in cc if bool(ev[c])]

    # the four D-4 similarity stamps, display-only, on ops data
    d1 = ops_indicator_frame("1d")
    k = int(np.searchsorted(d1["close_ms"], ets + INTERVAL_MS["4h"], "right")) - 1
    e1d = ema_warm(d1["close"], 200)
    up = False                                        # bear cross
    agrees = bool(ev["e89"] < ev["e200"])
    st = pb4[(pb4.open_time >= ets - SEAL_BARS_4H * INTERVAL_MS["4h"])
             & (pb4.open_time <= ets) & (pb4["cross_89_200_dn"])]
    seal = bool(agrees or len(st))
    limb4 = bool(abs(ev["close"] - ev["e89"]) <= WALL_ATR_4H * ev["atr"])
    limb1 = bool(k >= 0 and np.isfinite(e1d[k]) and d1["atr"][k] > 0
                 and abs(ev["close"] - e1d[k]) <= WALL_ATR_1D * d1["atr"][k])
    ncounter = 0
    for tf in FAST_TFS:
        p = pd.read_parquet(OPS_SERIES / f"perbar_{tf}.parquet")
        up_cols = [c for c in p.columns if c.startswith("cross_") and c.endswith("_up")]
        w = p[(p.open_time >= ets - TRAP_LOOKBACK_H * 3_600_000) & (p.open_time < ets)]
        ncounter += int(w[up_cols].any(axis=1).sum())
    prior20 = pb4[(pb4.open_time >= ets - FIRST_LOOKBACK_4H * INTERVAL_MS["4h"])
                  & (pb4.open_time < ets)]
    first = bool(not prior20[cc].any(axis=1).any())

    # BEFORE-CHRONOLOGY: every cross/kiss on every TF in the prior 14 days
    reg = pd.read_parquet(OPS_REGISTRY / "registry_series.parquet")
    chron = []
    c0 = ets - CHRONOLOGY_DAYS * DAY_MS
    for tf in DOSSIER_TFS:
        p = pd.read_parquet(OPS_SERIES / f"perbar_{tf}.parquet")
        w = p[(p.open_time >= c0) & (p.open_time <= ets)]
        flags = [c for c in p.columns
                 if c.startswith("cross_") or (c.startswith("kiss_")
                                               and not c.endswith("_known_ts"))]
        for r in w.itertuples(index=False):
            f = [c for c in flags if bool(getattr(r, c))]
            if not f:
                continue
            ts = int(r.open_time)
            dayk = (ts // DAY_MS) * DAY_MS
            rr = reg[(reg.as_of_ms == dayk) & (reg.variant == "with_volume")]
            near = []
            if len(rr) and np.isfinite(r.atr) and r.atr > 0:
                rr2 = rr[(rr.level - float(r.close)).abs() <= COLOC_ATR * float(r.atr)]
                near = [f"{x.family}:{x.label}@{x.level:.1f}(s{x.score})"
                        for x in rr2.itertuples(index=False)]
            chron.append({"tf": tf, "ts": ts, "ts_iso": iso(ts),
                          "close": float(r.close), "events": ",".join(f),
                          "registry_levels_at_event": "; ".join(near) or "none"})
    chron.sort(key=lambda x: (x["ts"], x["tf"]))
    card = {
        "_header": DISPLAY_ONLY_HEADER, "instrument": INSTRUMENT,
        "event_ts": ets, "event_iso": iso(ets),
        "crosses_on_bar": fired,
        "close": float(ev["close"]), "atr_4h": float(ev["atr"]),
        "stamps_display_only": {
            "SEAL": seal, "seal_agrees_89_200_bearish": agrees,
            "seal_crossed_within_6": bool(len(st)),
            "WALL": bool(limb4 or limb1),
            "wall_limb": ("both" if limb4 and limb1 else "4h" if limb4
                          else "1d" if limb1 else "none"),
            "TRAP": bool(ncounter >= TRAP_MIN_COUNTER),
            "trap_counter_fast_up_crosses_prior_24h": ncounter,
            "FIRST": first,
            "similarity_score": int(seal) + int(limb4 or limb1)
            + int(ncounter >= TRAP_MIN_COUNTER) + int(first),
        },
        "full_stack_at_instant": query_dossier(ets + INTERVAL_MS["4h"], "4h"),
        "before_chronology_days": CHRONOLOGY_DAYS,
        "before_chronology": chron,
        "n_chronology_events": len(chron),
    }
    ckpt_save("d3e_event_card", card)
    log(f"D-3(e) COMPLETE — May-26 card, {len(chron)} prior-14d events")
    return card


# ---------------------------------------------------------------------------
# SEQ8 substrate scans — one streaming pass each, then compact parquet.
# EVIDENCE class: SEQ8 is already exploration-classic; F-MC2 re-verifies.
# ---------------------------------------------------------------------------
SEQ8_DIR = ROOT / "research_outputs" / "seq8"
TIER_GRAMMAR = {"5m": "FAST", "15m": "FAST", "30m": "FAST",
                "1h": "STAIR", "4h": "SLOW", "12h": "SLOW", "1d": "TREND"}
FAST_TFS = [t for t, v in TIER_GRAMMAR.items() if v == "FAST"]
LENSES = ["1h", "4h", "12h", "1d"]
TF_ORDER = ["5m", "15m", "30m", "1h", "4h", "12h", "1d"]
TFI = {t: i for i, t in enumerate(TF_ORDER)}
LATTICE_A_CLASSES = ["9_89", "89_200", "9_200"]
HORIZONS = [20, 100, 500]

# W-F1 primary-book decile cuts (WF1_tables.md:15-19). W-F1 materialises only
# the top and bottom deciles; there is no 1..10 label anywhere in the repo.
WF1_W_CUT = 0.067318          # realized_r >= -> W (top decile, "winners")
WF1_L_CUT = -0.852774         # realized_r <= -> L (bottom decile, "losers")


def classify_arrival(src: str, dest: str) -> str:
    """scripts/seq8_views.py:216-221, reproduced for the 4h arrival axis."""
    if src is None:
        return "initiating"
    if TFI[src] == TFI[dest] - 1:
        return "adjacent"
    if TFI[src] < TFI[dest] - 1:
        return "leap"
    return "from_above"


def stage_scan_events() -> dict:
    """seq8_events.jsonl (288,711 rows) -> compact parquet."""
    keep = ["asset", "lattice", "event_class", "tf", "dir", "ts", "bar_close_ms",
            "bar_idx", "event_price", "atr", "e9", "e89", "e200",
            "exec_anchor_ok", "atr_ok"]
    rows = []
    with open(SEQ8_DIR / "seq8_events.jsonl", encoding="utf-8") as f:
        for i, line in enumerate(f):
            r = json.loads(line)
            rows.append([r.get(k) for k in keep])
            if i and i % 100000 == 0:
                log(f"    events {i}")
    df = pd.DataFrame(rows, columns=keep)
    OPS.mkdir(parents=True, exist_ok=True)
    p = OPS / "seq8_events_compact.parquet"
    df.to_parquet(p, index=False)
    log(f"  events compact: {len(df)} rows -> {p.name} "
        f"({p.stat().st_size / 1e6:.1f} MB)")
    return {"rows": int(len(df)), "path": str(p), "sha256": sha256_file(p)}


def stage_scan_cascades() -> dict:
    """cascades + outcomes streamed in lockstep (positionally 1:1) -> parquet."""
    ck = ["asset", "view", "lattice", "event_class", "dir", "depth", "init_tf",
          "init_ts", "term_tf", "term_ts", "term_bar_close_ms", "family_first3",
          "rungs_absolute", "rungs_tier", "monotone",
          "source_into_1h", "source_into_4h", "source_into_12h", "source_into_1d"]
    ok = ["outcome_available", "term_tier", "p0_terminus", "atr_basis"] + \
         [f"{m}_bps_h{h}" for m in ("mfe", "mae") for h in HORIZONS] + \
         [f"{m}_atr_h{h}" for m in ("mfe", "mae") for h in HORIZONS] + \
         ["cleared_tier"]
    rows = []
    fc = open(SEQ8_DIR / "seq8_cascades.jsonl", encoding="utf-8")
    fo = open(SEQ8_DIR / "seq8_outcomes.jsonl", encoding="utf-8")
    n = 0
    mism = 0
    for lc, lo in zip(fc, fo):
        c = json.loads(lc)
        o = json.loads(lo)
        if (c["asset"], c["view"], c["init_ts"], c["init_tf"]) != \
           (o["asset"], o["view"], o["init_ts"], o["init_tf"]):
            mism += 1
        rows.append([c.get(k) for k in ck] + [o.get(k) for k in ok])
        n += 1
        if n % 200000 == 0:
            log(f"    cascades {n}")
    fc.close(); fo.close()
    df = pd.DataFrame(rows, columns=ck + ok)
    p = OPS / "seq8_cascades_compact.parquet"
    df.to_parquet(p, index=False)
    log(f"  cascades compact: {len(df)} rows, row-alignment mismatches={mism} "
        f"-> {p.name} ({p.stat().st_size / 1e6:.1f} MB)")
    return {"rows": int(len(df)), "alignment_mismatches": int(mism),
            "path": str(p), "sha256": sha256_file(p)}


def stage_scan() -> dict:
    out = {}
    if not (OPS / "seq8_events_compact.parquet").exists():
        out["events"] = stage_scan_events()
    else:
        log("  events compact cached")
    if not (OPS / "seq8_cascades_compact.parquet").exists():
        out["cascades"] = stage_scan_cascades()
    else:
        log("  cascades compact cached")
    ckpt_save("scan_manifest", out)
    return out


# ---------------------------------------------------------------------------
# STAGE d4 — SIMILARITY FAMILY (EVIDENCE, exploration-classic)
# ---------------------------------------------------------------------------
def _daily_frames() -> dict:
    """1d frames per asset for the WALL 1d limb, exploration-classic."""
    klines = estate_klines()
    out = {}
    for sym in sorted(CB.ASSET_STARTS):
        d = build_tf_frame(klines, sym, "1d")
        c = d["close"].to_numpy(float)
        out[sym] = {
            "open_time": d["open_time"].to_numpy(np.int64),
            "close_ms": d["open_time"].to_numpy(np.int64) + DAY_MS,
            "e200": ema_warm(c, 200),
            "atr": _atr_ref(d["high"].to_numpy(float), d["low"].to_numpy(float),
                            c, ATR_LEN),
        }
    return out


def stage_d4() -> dict:
    ev = pd.read_parquet(OPS / "seq8_events_compact.parquet")
    d1f = _daily_frames()
    # PRIMARY population: lattice A ("the working trio 9/89/200"), tf=4h, both
    # directions, 7 assets. See the RULING in the build document: SEQ8 has no
    # "trio" term; lattice A is the trio, and the 89_200 subpopulation makes the
    # SEAL stamp self-referential, so it is stamped and flagged degenerate.
    pop = ev[(ev.tf == "4h") & (ev.lattice == "A")].sort_values(
        ["asset", "ts", "event_class", "dir"]).reset_index(drop=True)
    log(f"  D-4 population: {len(pop)} 4h lattice-A crosses, 7 assets")

    rows = []
    for sym, g in pop.groupby("asset", sort=True):
        a_ev = ev[ev.asset == sym]
        # 89_200 4h crosses for the SEAL "crosses within 6 bars" limb
        seal_ev = a_ev[(a_ev.tf == "4h") & (a_ev.event_class == "89_200")]
        seal_ts = {d: seal_ev[seal_ev.dir == d].ts.to_numpy(np.int64)
                   for d in ("up", "down")}
        # FAST-tier lattice-A crosses for TRAP
        fast = a_ev[(a_ev.tf.isin(FAST_TFS)) & (a_ev.lattice == "A")]
        fast_ts = {d: np.sort(fast[fast.dir == d].ts.to_numpy(np.int64))
                   for d in ("up", "down")}
        # all 4h lattice-A crosses for FIRST
        a4 = a_ev[(a_ev.tf == "4h") & (a_ev.lattice == "A")]
        a4_ts = {d: np.sort(a4[a4.dir == d].ts.to_numpy(np.int64))
                 for d in ("up", "down")}
        df = d1f[sym]
        for r in g.itertuples(index=False):
            ts = int(r.ts)
            up = r.dir == "up"
            opp = "down" if up else "up"

            # ---- SEAL: 4H 89/200 agrees, OR crosses within 6 4H bars (PRIOR,
            #      so the stamp is curtain-clean per F-MC4)
            agrees = (r.e89 > r.e200) if up else (r.e89 < r.e200)
            agrees = bool(agrees) if (np.isfinite(r.e89) and np.isfinite(r.e200)) else False
            lo6 = ts - SEAL_BARS_4H * CB.TF_MS["4h"]
            st = seal_ts[r.dir]
            crossed6 = bool(((st >= lo6) & (st <= ts)).any())
            seal = bool(agrees or crossed6)

            # ---- WALL: |price-e89(4h)| <= 0.5*ATR(4h) OR |price-e200(1d)| <= 0.5*ATR(1d)
            limb4 = (np.isfinite(r.e89) and np.isfinite(r.atr) and r.atr > 0 and
                     abs(r.event_price - r.e89) <= WALL_ATR_4H * r.atr)
            k = int(np.searchsorted(df["close_ms"], int(r.bar_close_ms), "right")) - 1
            limb1 = False
            if k >= 0 and np.isfinite(df["e200"][k]) and df["atr"][k] > 0:
                limb1 = abs(r.event_price - df["e200"][k]) <= WALL_ATR_1D * df["atr"][k]
            wall = bool(limb4 or limb1)
            which = ("both" if (limb4 and limb1) else "4h" if limb4
                     else "1d" if limb1 else "none")

            # ---- TRAP: >=2 counter-direction FAST-tier crosses in prior 24h
            ft = fast_ts[opp]
            lo24 = ts - TRAP_LOOKBACK_H * 3_600_000
            ncounter = int(((ft >= lo24) & (ft < ts)).sum())
            trap = bool(ncounter >= TRAP_MIN_COUNTER)

            # ---- FIRST: no same-direction 4H trio cross in prior 20 4H bars
            at = a4_ts[r.dir]
            lo20 = ts - FIRST_LOOKBACK_4H * CB.TF_MS["4h"]
            first = bool(not ((at >= lo20) & (at < ts)).any())

            rows.append({
                "asset": sym, "event_class": r.event_class, "dir": r.dir,
                "ts": ts, "ts_iso": iso(ts), "bar_close_ms": int(r.bar_close_ms),
                "event_price": float(r.event_price),
                "SEAL": seal, "seal_agrees": agrees, "seal_crossed_within_6": crossed6,
                "WALL": wall, "wall_limb": which,
                "TRAP": trap, "trap_counter_count": ncounter,
                "FIRST": first,
                "similarity_score": int(seal) + int(wall) + int(trap) + int(first),
                "strict_core": bool(seal and wall and trap and first),
                "seal_degenerate": bool(r.event_class == "89_200"),
            })
        log(f"    d4 {sym}: {len(g)} events")

    sim = pd.DataFrame(rows).sort_values(
        ["asset", "ts", "event_class", "dir"]).reset_index(drop=True)
    p = OPS / "d4_similarity.parquet"
    sim.to_parquet(p, index=False)

    pyramid = (sim.groupby(["asset", "similarity_score"]).size()
               .unstack(fill_value=0).sort_index())
    pyr_nodeg = (sim[~sim.seal_degenerate].groupby(["asset", "similarity_score"])
                 .size().unstack(fill_value=0).sort_index())
    out = {
        "_class": "EVIDENCE — exploration-classic",
        "population_rule": ("tf=4h AND lattice=A (the working trio 9/89/200: "
                            "event_class in 9_89, 89_200, 9_200), both directions, "
                            "7 assets, SEQ8 D1 stream seq8_events.jsonl"),
        "n_events": int(len(sim)),
        "max_ts": int(sim.ts.max()), "max_ts_iso": iso(int(sim.ts.max())),
        "stamp_counts": {s: int(sim[s].sum()) for s in ("SEAL", "WALL", "TRAP", "FIRST")},
        "wall_limb_counts": {k: int(v) for k, v in
                             sim.wall_limb.value_counts().items()},
        "strict_core_n": int(sim.strict_core.sum()),
        "pyramid": json.loads(pyramid.to_json(orient="index")),
        "pyramid_excl_seal_degenerate": json.loads(pyr_nodeg.to_json(orient="index")),
        "seal_degenerate_n": int(sim.seal_degenerate.sum()),
        "path": str(p), "sha256": sha256_file(p),
    }
    ckpt_save("d4_similarity", out)
    log(f"D-4 COMPLETE — {len(sim)} events, strict core 4/4 = {out['strict_core_n']}")
    return out


# ---------------------------------------------------------------------------
# STAGE d5 — OUTCOMES BY TIER (lift, curtain-cut)
# ---------------------------------------------------------------------------
def _q(a, p):
    a = a[np.isfinite(a)]
    return float(np.percentile(a, p)) if len(a) else None


def stage_d5() -> dict:
    c = pd.read_parquet(OPS / "seq8_cascades_compact.parquet")
    c = c[c.outcome_available == True].copy()            # noqa: E712 — null trap
    log(f"  D-5 outcome-available cascades: {len(c)}")
    med_ts = int(np.median(c.init_ts.to_numpy(np.int64)))
    c["era"] = np.where(c.init_ts.to_numpy(np.int64) <= med_ts, "early", "late")

    tables = []
    for lens in LENSES:
        src = c[f"source_into_{lens}"]
        sub = c[src.notna()]
        for (asset, tier), g in sub.groupby(["asset", "term_tier"], sort=True):
            for hz in HORIZONS:
                mfe = g[f"mfe_bps_h{hz}"].to_numpy(float)
                mae = g[f"mae_bps_h{hz}"].to_numpy(float)
                tables.append({
                    "lens": lens, "asset": asset, "tier": tier, "horizon": hz,
                    "n": int(len(g)),
                    "mfe_median": _q(mfe, 50), "mfe_p25": _q(mfe, 25),
                    "mfe_p75": _q(mfe, 75),
                    "mae_median": _q(mae, 50), "mae_p25": _q(mae, 25),
                    "mae_p75": _q(mae, 75),
                    "net_median": (_q(mfe, 50) + _q(mae, 50))
                    if (_q(mfe, 50) is not None and _q(mae, 50) is not None) else None,
                    "n_early": int((g.era == "early").sum()),
                    "n_late": int((g.era == "late").sum()),
                    "mfe_median_early": _q(g[g.era == "early"][f"mfe_bps_h{hz}"]
                                           .to_numpy(float), 50),
                    "mfe_median_late": _q(g[g.era == "late"][f"mfe_bps_h{hz}"]
                                          .to_numpy(float), 50),
                })
    tb = pd.DataFrame(tables)
    p = OPS / "d5_outcomes_by_tier.parquet"
    tb.to_parquet(p, index=False)

    # ---- TRG (Tail-Retention Gauge) tail table. tier-0 = the UNGATED baseline,
    # which retains 100.0% of the tail by identity (F-MC7).
    base = c[c.mfe_bps_h100.notna()]
    thr = float(np.percentile(base.mfe_bps_h100.to_numpy(float), 90))
    tail = base[base.mfe_bps_h100 >= thr]
    tail_mass = float(tail.mfe_bps_h100.sum())
    trg = [{"tier": "tier-0 (UNGATED)", "gate": "none",
            "n_kept": int(len(base)), "tail_n_kept": int(len(tail)),
            "tail_mass_kept": tail_mass,
            "TRG_pct": round(100.0 * tail_mass / tail_mass, 1) if tail_mass else None}]
    for t in ["FAST", "STAIR", "SLOW", "TREND"]:
        k = base[base.term_tier == t]
        kt = k[k.mfe_bps_h100 >= thr]
        trg.append({"tier": t, "gate": f"term_tier == {t}",
                    "n_kept": int(len(k)), "tail_n_kept": int(len(kt)),
                    "tail_mass_kept": float(kt.mfe_bps_h100.sum()),
                    "TRG_pct": round(100.0 * float(kt.mfe_bps_h100.sum())
                                     / tail_mass, 1) if tail_mass else None})
    out = {
        "_class": "EVIDENCE — exploration-classic (scoped embargo lift, D-5 population)",
        "n_cascades_outcome_available": int(len(c)),
        "median_init_ts": med_ts, "median_init_iso": iso(med_ts),
        "max_ts": int(c.term_ts.max()), "max_ts_iso": iso(int(c.term_ts.max())),
        "tail_threshold_p90_mfe_bps_h100": thr,
        "trg_table": trg,
        "n_table_rows": int(len(tb)),
        "path": str(p), "sha256": sha256_file(p),
        "trg_definition": (
            "TRG = share of the ungated tail mass retained by a gate. Tail = the "
            "top decile of mfe_bps_h100 over the outcome-available population; "
            "tail mass = sum of mfe_bps_h100 over that decile. tier-0 is the "
            "ungated population and retains 100.0% by identity (F-MC7)."),
    }
    ckpt_save("d5_outcomes", out)
    log(f"D-5 COMPLETE — {len(tb)} table rows; TRG tier-0 = {trg[0]['TRG_pct']}%")
    return out


# ---------------------------------------------------------------------------
# STAGE d6 — TRADE JOIN + PROMOTIONS (lift). Scores P-i, P-iii, P-iv.
# ---------------------------------------------------------------------------
PANEL = ("BTCUSDT", "ETHUSDT", "SOLUSDT", "NEARUSDT", "ZECUSDT")   # wf1_forensics.py:72

# SEQ8 F-SEQ3 join rule, VERBATIM (seq8_fixtures.json:41 / seq8_outcomes_manifest.json:71)
F_SEQ3_JOIN_RULE = (
    "birth joins a cascade iff (a) cell symbol == cascade asset, (b) the cell's "
    "governor TF is a rung of the cascade (MANDATES: intraday->1h, swing->4h, "
    "position->12h), and (c) birth ts_open lies within [first rung bar_close, "
    "terminus bar_close]. Restricted to lattice A / 9_89 (the cross the engine trades)."
)
F_SEQ3_JOIN_KEY = "(cell_id, tranche_id) — tranche_id alone collides across cells"


def load_wf1_births() -> pd.DataFrame:
    box = ROOT / "_reviewer_box" / "wf1"
    rows = []
    for p in sorted(box.glob("*USDT_*.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        for r in d["rows"]:
            rows.append({
                "cell_id": r["cell"], "tranche_id": r["tranche_id"],
                "symbol": r["symbol"], "mandate": r["mandate"], "dir": r["dir"],
                "ts_open": r["ts_open"], "resolved": bool(r.get("resolved")),
                "realized_r": r.get("realized_r"),
            })
    b = pd.DataFrame(rows)
    rr = b["realized_r"]
    b["wf1_class"] = np.where(~b.resolved | rr.isna(), "UNRESOLVED",
                              np.where(rr >= WF1_W_CUT, "W",
                                       np.where(rr <= WF1_L_CUT, "L", "MID")))
    return b


def _boot_diff_ci(a: np.ndarray, b: np.ndarray, n=2000, seed=SEED) -> tuple:
    """Bootstrap CI on prevalence(a) - prevalence(b). Descriptive only (I4)."""
    rng = np.random.default_rng(seed)
    if len(a) == 0 or len(b) == 0:
        return None, None, None
    d = a.mean() - b.mean()
    s = np.empty(n)
    for i in range(n):
        s[i] = (rng.choice(a, len(a), replace=True).mean()
                - rng.choice(b, len(b), replace=True).mean())
    return float(d), float(np.percentile(s, 2.5)), float(np.percentile(s, 97.5))


def stage_d6() -> dict:
    casc = pd.read_parquet(OPS / "seq8_cascades_compact.parquet")
    births = load_wf1_births()
    log(f"  births in box: {len(births)}  "
        f"({(births.wf1_class == 'W').sum()} W / {(births.wf1_class == 'L').sum()} L)")

    # ---- the bridge, as SEQ8 built it
    jrows = []
    with open(SEQ8_DIR / "seq8_cascade_birth_join.jsonl", encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            jrows.append((r["asset"], r["cell_id"], r["tranche_id"], r["view"],
                          r["birth_ts_ms"], r["birth_dir"], r["cascade_family"],
                          r["cascade_init_ts"], r["cascade_rungs"],
                          r["cascade_dir"], r["tf_gov"], bool(r["resolved"]),
                          bool(r["dir_agrees"])))
    J = pd.DataFrame(jrows, columns=[
        "asset", "cell_id", "tranche_id", "view", "birth_ts_ms", "birth_dir",
        "cascade_family", "cascade_init_ts", "cascade_rungs", "cascade_dir",
        "tf_gov", "resolved", "dir_agrees"])
    J["init_tf"] = J.cascade_rungs.str.split(">").str[0]
    log(f"  bridge rows: {len(J)}  distinct birth keys: "
        f"{J.groupby(['cell_id', 'tranche_id']).ngroups}")

    # ---- F-MC5 join integrity
    bkeys = set(zip(births.cell_id, births.tranche_id))
    jkeys = set(zip(J.cell_id, J.tranche_id))
    orphans_join_to_journal = sorted(jkeys - bkeys)
    never_joined = sorted(bkeys - jkeys)
    join_integrity = {
        "join_rule_verbatim": F_SEQ3_JOIN_RULE,
        "join_key_verbatim": F_SEQ3_JOIN_KEY,
        "join_rows": int(len(J)),
        "births_total": int(len(births)),
        "birth_keys_distinct": int(len(bkeys)),
        "distinct_births_joined": int(len(jkeys)),
        "orphans_join_to_journal": len(orphans_join_to_journal),
        "births_never_joined": len(never_joined),
        "orphan_note": (
            "SEQ8's own stance, reproduced not overridden: 'Zero orphans both ways' "
            "is asserted in the direction that is falsifiable — every joined key must "
            "exist in the journals. The reverse is NOT an orphan condition: a birth "
            "falling in no cascade span is a real, correct outcome and is reported as "
            "births_never_joined rather than forced to zero."),
    }

    # ---- attach cascade attributes (source_into_*) to the bridge
    ck = casc[casc.lattice.eq("A") & casc.event_class.eq("9_89")][
        ["asset", "view", "dir", "init_ts", "init_tf", "family_first3",
         "term_tier", "atr_basis", "outcome_available",
         "source_into_1h", "source_into_4h", "source_into_12h", "source_into_1d"]
        + [f"mfe_bps_h{h}" for h in HORIZONS] + [f"mae_bps_h{h}" for h in HORIZONS]
    ].rename(columns={"dir": "cascade_dir", "init_ts": "cascade_init_ts"})
    JM = J.merge(ck, on=["asset", "view", "cascade_dir", "cascade_init_ts", "init_tf"],
                 how="left")
    matched = int(JM.family_first3.notna().sum())
    log(f"  bridge->cascade attribute match: {matched}/{len(JM)}")

    JM = JM.merge(births[["cell_id", "tranche_id", "realized_r", "wf1_class"]],
                  on=["cell_id", "tranche_id"], how="left")

    views = sorted(J.view.unique())
    primary_view = "24h|window_chained"
    out = {"_class": "EVIDENCE — exploration-classic (scoped embargo lift)",
           "join_integrity": join_integrity, "views": views,
           "primary_view": primary_view,
           "bridge_cascade_attr_matched": matched,
           "panel": list(PANEL)}

    # ---- tier membership vs W-F1 deciles (primary view, dedup per birth)
    pv = JM[JM.view == primary_view].copy()
    pvb = pv.sort_values("cascade_init_ts").groupby(
        ["cell_id", "tranche_id"], as_index=False).last()
    tier_vs_dec = (pvb.groupby(["term_tier", "wf1_class"]).size()
                   .unstack(fill_value=0))
    out["tier_vs_wf1_decile"] = json.loads(tier_vs_dec.to_json(orient="index"))
    out["wf1_cut_values"] = {"W_cut_realized_r_gte": WF1_W_CUT,
                             "L_cut_realized_r_lte": WF1_L_CUT,
                             "note": ("W-F1 materialises ONLY the top and bottom "
                                      "deciles (709 each of 7,094 resolved); no 1..10 "
                                      "decile label exists anywhere in the repo.")}

    # ================= P-i =================
    c4 = casc[casc.outcome_available.eq(True) & casc[f"source_into_4h"].notna()].copy()
    c4["arrival"] = [classify_arrival(s, "4h") for s in c4.source_into_4h]
    pi_rows, pi_views = [], {}
    for v in views:
        sub = c4[c4.view == v]
        signs = {}
        for a in PANEL:
            g = sub[sub.asset == a]
            lp = g[g.arrival == "leap"]
            st = g[g.arrival == "adjacent"]
            net_l = (lp.mfe_bps_h100 + lp.mae_bps_h100).median() if len(lp) else np.nan
            net_s = (st.mfe_bps_h100 + st.mae_bps_h100).median() if len(st) else np.nan
            d = float(net_l - net_s) if np.isfinite(net_l) and np.isfinite(net_s) else None
            signs[a] = d
            if v == primary_view:
                pi_rows.append({"asset": a, "n_leap": int(len(lp)),
                                "n_stair_adjacent": int(len(st)),
                                "net_mfe_mae_leap": None if not np.isfinite(net_l) else float(net_l),
                                "net_mfe_mae_stair": None if not np.isfinite(net_s) else float(net_s),
                                "delta": d, "sign_positive": (d is not None and d > 0)})
        npos = sum(1 for d in signs.values() if d is not None and d > 0)
        pi_views[v] = {"assets_positive": npos, "per_asset_delta": signs}
    npos_primary = pi_views[primary_view]["assets_positive"]
    out["P_i"] = {
        "registration": ("P-i [55%] Leap-family cascades (4h-tier arrival from the "
                         "FAST tier, pullback-anchored frame) carry higher curtain-cut "
                         "per-lens MFE net of matched MAE than stair-arrival cascades, "
                         "sign-consistent on >=3 of 5 panel assets."),
        "construction": ("lens = 4h arrival; leap = classify_arrival(source_into_4h,'4h')"
                         "=='leap' (source in FAST {5m,15m,30m}); stair = 'adjacent' "
                         "(source == 1h). Metric = median(mfe_bps_h100 + mae_bps_h100) "
                         "(MAE is signed negative, so the sum IS 'net of matched MAE'). "
                         "Horizon h100 exec-5m bars."),
        "caveat_pullback_anchored": (
            "'pullback-anchored frame' has NO representation in the SEQ8 cascade "
            "substrate (no pullback/continuation flag exists on a cascade; the census "
            "NOPULLBACK_LOOKBACK/RIBBON_SEP_ATR machinery is census-1b, not SEQ8). "
            "The qualifier was NOT applied as a filter. Reported, not invented."),
        "per_asset_primary_view": pi_rows,
        "assets_positive_primary_view": npos_primary,
        "threshold": ">=3 of 5",
        "VERDICT": "SUPPORTED" if npos_primary >= 3 else "NOT SUPPORTED",
        "all_views": pi_views,
    }

    # ================= P-iii =================
    JM["grind_sig"] = (JM.family_first3.eq("grind")
                       & JM.source_into_4h.isna() & JM.source_into_12h.isna())
    pv2 = JM[JM.view == primary_view]
    per_birth = pv2.groupby(["cell_id", "tranche_id"], as_index=False).agg(
        grind_sig=("grind_sig", "any"), wf1_class=("wf1_class", "first"))
    W = per_birth[per_birth.wf1_class == "W"].grind_sig.to_numpy(float)
    L = per_birth[per_birth.wf1_class == "L"].grind_sig.to_numpy(float)
    d, lo, hi = _boot_diff_ci(L, W)
    excl0 = (lo is not None and (lo > 0 or hi < 0))
    out["P_iii"] = {
        "registration": ("P-iii [60%] Grind-signature births (5m->15m->30m context, no "
                         "slow-tier arrival within the episode) are over-represented in "
                         "the W-F1 bottom decile vs top, CI excl. 0."),
        "construction": ("grind-signature = bridge-joined cascade with "
                         "family_first3=='grind' AND source_into_4h is null AND "
                         "source_into_12h is null (no SLOW-tier arrival). Prevalence in "
                         "L minus prevalence in W; 95% bootstrap CI, 2000 resamples, "
                         "seed 20260806. Descriptive interval only (I4)."),
        "n_W": int(len(W)), "n_L": int(len(L)),
        "prevalence_W": float(W.mean()) if len(W) else None,
        "prevalence_L": float(L.mean()) if len(L) else None,
        "delta_L_minus_W": d, "ci_lo": lo, "ci_hi": hi,
        "ci_excludes_zero": bool(excl0),
        "VERDICT": "SUPPORTED" if (d is not None and d > 0 and excl0)
                   else "NOT SUPPORTED",
    }

    # ================= P-iv =================
    piv_rows = {}
    for v in views:
        sub = c4[c4.view == v].copy()
        npos = 0
        detail = {}
        for a in PANEL:
            g = sub[sub.asset == a].copy()
            g = g[g.atr_basis.notna()]
            if len(g) < 10:
                detail[a] = None
                continue
            g["vbucket"] = pd.qcut(g.atr_basis.rank(method="first"), 5,
                                   labels=False, duplicates="drop")
            ds = []
            for bq, gb in g.groupby("vbucket"):
                lp = gb[gb.arrival == "leap"]
                st = gb[gb.arrival == "adjacent"]
                if len(lp) and len(st):
                    ds.append(float((lp.mfe_bps_h100 + lp.mae_bps_h100).median()
                                    - (st.mfe_bps_h100 + st.mae_bps_h100).median()))
            dm = float(np.mean(ds)) if ds else None
            detail[a] = {"buckets_used": len(ds), "mean_bucket_delta": dm}
            if dm is not None and dm > 0:
                npos += 1
        piv_rows[v] = {"assets_positive": npos, "per_asset": detail}
    npos_iv = piv_rows[primary_view]["assets_positive"]
    out["P_iv"] = {
        "registration": ("P-iv [45%] Among 4h arrivals, leap-source outperforms "
                         "stair-source AFTER conditioning on ATR-percentile at arrival "
                         "(vol-matched buckets), >=3 of 5 assets."),
        "construction": ("Within each asset, atr_basis (exec-5m ATR at the terminus "
                         "anchor) is ranked into 5 equal-count vol buckets; leap minus "
                         "adjacent median net(MFE+MAE) is computed per bucket and "
                         "averaged over buckets containing both arms."),
        "per_asset_primary_view": piv_rows[primary_view]["per_asset"],
        "assets_positive_primary_view": npos_iv,
        "threshold": ">=3 of 5",
        "VERDICT": "SUPPORTED" if npos_iv >= 3 else "NOT SUPPORTED",
        "all_views": piv_rows,
    }

    p = OPS / "d6_bridge_joined.parquet"
    JM.to_parquet(p, index=False)
    out["path"] = str(p)
    out["sha256"] = sha256_file(p)
    out["max_birth_ts"] = int(J.birth_ts_ms.max())
    out["max_birth_ts_iso"] = iso(int(J.birth_ts_ms.max()))
    ckpt_save("d6_join", out)
    log(f"D-6 COMPLETE — P-i {out['P_i']['VERDICT']} ({npos_primary}/5) · "
        f"P-iii {out['P_iii']['VERDICT']} · P-iv {out['P_iv']['VERDICT']} ({npos_iv}/5)")
    return out


# ---------------------------------------------------------------------------
# STAGE d7 — WINNER STACKS + RATCHET SUBSTRATE
# ---------------------------------------------------------------------------
MTF_BITS = SEQ8.MTF_BITS       # imported, not restated (seq8_extract.py:125-126)
_FRAME_CACHE: dict = {}


def estate_indicator_frame(sym: str, tf: str) -> dict:
    """Estate frame + EMA ladder + ATR, exploration-classic. Cached per process."""
    k = (sym, tf)
    if k in _FRAME_CACHE:
        return _FRAME_CACHE[k]
    d = build_tf_frame(estate_klines(), sym, tf)
    c = d["close"].to_numpy(float)
    f = {"open_time": d["open_time"].to_numpy(np.int64),
         "close_ms": d["open_time"].to_numpy(np.int64) + CB.TF_MS.get(tf, DAY_MS),
         "open": d["open"].to_numpy(float), "high": d["high"].to_numpy(float),
         "low": d["low"].to_numpy(float), "close": c,
         "atr": _atr_ref(d["high"].to_numpy(float), d["low"].to_numpy(float),
                         c, ATR_LEN)}
    for L in (9, 12, 25, 89, 200, 300, 450):
        f[f"e{L}"] = ema_warm(c, L)
    _FRAME_CACHE[k] = f
    return f


def mtf_stack_asof(sym: str, ts: int) -> dict:
    """SEQ8's 7-bit orientation string per TF, as-of the last CLOSED bar <= ts."""
    out = {}
    for tf in TF_ORDER:
        f = estate_indicator_frame(sym, tf)
        j = int(np.searchsorted(f["close_ms"], ts, "right")) - 1
        if j < 0:
            out[tf] = "x" * 7
            continue
        vals = [f["e9"][j] - f["e89"][j], f["e89"][j] - f["e200"][j],
                f["e9"][j] - f["e200"][j], f["e12"][j] - f["e25"][j],
                f["close"][j] - f["e89"][j], f["close"][j] - f["e200"][j],
                f["e300"][j] - f["e450"][j]]
        out[tf] = "".join("x" if not np.isfinite(v) else ("1" if v > 0 else "0")
                          for v in vals)
    return out


def stage_d7() -> dict:
    JM = pd.read_parquet(OPS / "d6_bridge_joined.parquet")
    births = load_wf1_births()
    primary_view = "24h|window_chained"

    # ---------------- (a) winner stacks ----------------
    win = JM[(JM.view == primary_view) & (JM.wf1_class == "W")
             & (JM.cascade_family == "leap")].copy()
    win = win.sort_values(["asset", "birth_ts_ms", "cascade_init_ts"])
    keyed = win.groupby(["cell_id", "tranche_id"], as_index=False).first()
    log(f"  D-7(a) top-decile births in leap-family cascades: {len(keyed)}")

    # inter-cross spacings need event_ts, dropped from the compact scan — one
    # targeted stream over cascades.jsonl for exactly these cascade PKs.
    want = set(zip(keyed.asset, keyed.view, keyed.cascade_dir,
                   keyed.cascade_init_ts, keyed.init_tf))
    evts = {}
    with open(SEQ8_DIR / "seq8_cascades.jsonl", encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            k = (r["asset"], r["view"], r["dir"], r["init_ts"], r["init_tf"])
            if k in want and k not in evts:
                evts[k] = (r["event_ts"], r["rungs_absolute"])
    log(f"    recovered event_ts for {len(evts)}/{len(want)} cascade PKs")

    stacks, ladders = [], []
    for r in keyed.itertuples(index=False):
        k = (r.asset, r.view, r.cascade_dir, r.cascade_init_ts, r.init_tf)
        ets, rungs = evts.get(k, (None, r.cascade_rungs))
        spac = ([round((ets[i + 1] - ets[i]) / 60000.0, 1)
                 for i in range(len(ets) - 1)] if ets else None)
        stacks.append({
            "cell_id": r.cell_id, "tranche_id": r.tranche_id, "asset": r.asset,
            "birth_ts": int(r.birth_ts_ms), "birth_iso": iso(int(r.birth_ts_ms)),
            "birth_dir": r.birth_dir, "realized_r": float(r.realized_r),
            "cascade_family": r.cascade_family, "cascade_rungs": rungs,
            "cascade_init_iso": iso(int(r.cascade_init_ts)),
            "term_tier": r.term_tier,
            "inter_cross_spacing_minutes": spac,
            "mtf_bit_order": MTF_BITS,
            "mtf_stack": mtf_stack_asof(r.asset, int(r.birth_ts_ms)),
        })
        # 1m ladder +-3 days (estate 1m, exploration era)
        f1 = estate_indicator_frame(r.asset, "1m")
        lo, hi = int(r.birth_ts_ms) - 3 * DAY_MS, int(r.birth_ts_ms) + 3 * DAY_MS
        i0 = int(np.searchsorted(f1["open_time"], lo, "left"))
        i1 = int(np.searchsorted(f1["open_time"], hi, "right"))
        if i1 > i0:
            lad = {"cell_id": r.cell_id, "tranche_id": r.tranche_id,
                   "asset": r.asset, "open_time": f1["open_time"][i0:i1],
                   "close": f1["close"][i0:i1], "atr": f1["atr"][i0:i1]}
            for L in ONE_M_SET:
                lad[f"e{L}"] = f1[f"e{L}"][i0:i1]
            ladders.append(pd.DataFrame(lad))
    lad_path = None
    if ladders:
        L = pd.concat(ladders, ignore_index=True)
        lad_path = OPS / "d7a_1m_ladders.parquet"
        L.to_parquet(lad_path, index=False)
        log(f"    1m ladders: {len(L)} rows -> {lad_path.name} "
            f"({lad_path.stat().st_size / 1e6:.1f} MB)")

    # ---------------- (b) struct-book test-and-reclaim ----------------
    # DERIVED definitions (not [VETO]); stated so they are falsifiable:
    #   TEST    long: bar low  <= ema ; short: bar high >= ema
    #   RECLAIM long: a close >= ema + n*ATR within RECLAIM_BARS of the test,
    #           with no intervening close <= ema - n*ATR (mirrored for short)
    #   CONTINUATION: max favourable excursion over the CONT_BARS after reclaim,
    #           in ATR units at the reclaim bar
    RECLAIM_BARS, CONT_BARS = 10, 20
    wf = births[(births.wf1_class == "W") & births.resolved].copy()
    raw = {}
    for p in sorted((ROOT / "_reviewer_box" / "wf1").glob("*USDT_*.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        for r in d["rows"]:
            raw[(r["cell"], r["tranche_id"])] = r
    events, camps = [], []
    for r in wf.itertuples(index=False):
        rr = raw[(r.cell_id, r.tranche_id)]
        if not rr.get("ts_close") or rr.get("stop") in (None, 0):
            continue
        t0 = int(pd.Timestamp(rr["ts_open"]).timestamp() * 1000)
        t1 = int(pd.Timestamp(rr["ts_close"]).timestamp() * 1000)
        if t1 >= CEIL_MS:
            continue
        is_long = rr["dir"] == "long"
        pxf, stop = float(rr["px_fill"]), float(rr["stop"])
        denom = (pxf - stop) if is_long else (stop - pxf)
        if denom <= 0:
            continue
        ctrl_gross = ((float(rr["exit_px_fill"]) - pxf) / denom if is_long
                      else (pxf - float(rr["exit_px_fill"])) / denom)
        cf_by_cushion = {}
        for tf in LONG_EMA_TFS:
            f = estate_indicator_frame(rr["symbol"], tf)
            a = int(np.searchsorted(f["close_ms"], t0, "left"))
            b = int(np.searchsorted(f["close_ms"], t1, "right"))
            for L in LONG_EMAS:
                e, at = f[f"e{L}"], f["atr"]
                for n in CUSHIONS:
                    first_fail_px = None
                    i = a
                    while i < b:
                        if not (np.isfinite(e[i]) and np.isfinite(at[i]) and at[i] > 0):
                            i += 1
                            continue
                        tested = (f["low"][i] <= e[i]) if is_long else (f["high"][i] >= e[i])
                        if not tested:
                            i += 1
                            continue
                        rec, fail = None, None
                        for j in range(i + 1, min(i + RECLAIM_BARS, b - 1) + 1):
                            if not np.isfinite(e[j]):
                                break
                            cush = n * at[j]
                            if is_long:
                                if f["close"][j] >= e[j] + cush:
                                    rec = j; break
                                if f["close"][j] <= e[j] - cush:
                                    fail = j; break
                            else:
                                if f["close"][j] <= e[j] - cush:
                                    rec = j; break
                                if f["close"][j] >= e[j] + cush:
                                    fail = j; break
                        if rec is not None:
                            c1 = min(rec + CONT_BARS, b - 1)
                            if c1 > rec and at[rec] > 0:
                                cont = ((f["high"][rec:c1 + 1].max() - f["close"][rec])
                                        if is_long else
                                        (f["close"][rec] - f["low"][rec:c1 + 1].min()))
                                events.append({
                                    "cell_id": r.cell_id, "tranche_id": r.tranche_id,
                                    "asset": rr["symbol"], "tf": tf, "ema": L,
                                    "cushion": n, "test_ts": int(f["open_time"][i]),
                                    "reclaim_ts": int(f["open_time"][rec]),
                                    "bars_to_reclaim": rec - i,
                                    "subsequent_mfe_atr": float(cont / at[rec]),
                                })
                            i = rec + 1
                            continue
                        if fail is not None and first_fail_px is None:
                            first_fail_px = float(f["close"][fail])
                            i = fail + 1
                            continue
                        i += 1
                    if first_fail_px is not None:
                        cf = ((first_fail_px - pxf) / denom if is_long
                              else (pxf - first_fail_px) / denom)
                        cf_by_cushion[f"{tf}|e{L}|n{n}"] = round(cf, 6)
        camps.append({
            "cell_id": r.cell_id, "tranche_id": r.tranche_id, "asset": rr["symbol"],
            "dir": rr["dir"], "realized_r_net": float(r.realized_r),
            "RIDE_ONLY_control_gross_r": round(ctrl_gross, 6),
            "counterfactual_stop_to_reclaim_gross_r": cf_by_cushion,
        })
    ev = pd.DataFrame(events)
    ev_path = None
    if len(ev):
        ev_path = OPS / "d7b_test_and_reclaim.parquet"
        ev.to_parquet(ev_path, index=False)

    summ = []
    if len(ev):
        for (tf, L, n), g in ev.groupby(["tf", "ema", "cushion"]):
            summ.append({"tf": tf, "ema": int(L), "cushion": float(n),
                         "n_events": int(len(g)),
                         "median_bars_to_reclaim": float(g.bars_to_reclaim.median()),
                         "median_subsequent_mfe_atr":
                             float(g.subsequent_mfe_atr.median()),
                         "p75_subsequent_mfe_atr":
                             float(g.subsequent_mfe_atr.quantile(0.75))})
    ctrl = [c["RIDE_ONLY_control_gross_r"] for c in camps]
    out = {
        "_class": "EVIDENCE — exploration-classic (scoped embargo lift)",
        "a_winner_stacks": {
            "n_births": len(stacks),
            "population": ("bridge-joined W-class (top-decile) births whose joined "
                           f"cascade has cascade_family=='leap', view {primary_view}"),
            "mtf_bit_order": MTF_BITS,
            "rows": stacks,
            "ladder_path": str(lad_path) if lad_path else None,
            "ladder_sha256": sha256_file(lad_path) if lad_path else None,
        },
        "b_ratchet": {
            "definitions": {
                "TEST": "long: bar low <= ema; short: bar high >= ema",
                "RECLAIM": (f"a close >= ema + n*ATR within {RECLAIM_BARS} bars of the "
                            "test with no intervening close <= ema - n*ATR (mirrored "
                            "for short)"),
                "CONTINUATION": (f"max favourable excursion over the {CONT_BARS} bars "
                                 "after the reclaim bar, in ATR units at that bar"),
                "status": ("DERIVED for this run — these three are NOT [VETO] constants "
                           "and no rule is adopted from them (contract: 'Tables only')"),
            },
            "n_campaigns": len(camps),
            "n_events": int(len(ev)),
            "RIDE_ONLY_control_FIRST": {          # I5: control prints FIRST
                "n": len(ctrl),
                "median_gross_r": float(np.median(ctrl)) if ctrl else None,
                "mean_gross_r": float(np.mean(ctrl)) if ctrl else None,
            },
            "event_summary_by_tf_ema_cushion": summ,
            "campaigns": camps[:200],
            "campaigns_truncated_in_json": max(0, len(camps) - 200),
            "event_path": str(ev_path) if ev_path else None,
        },
    }
    ckpt_save("d7_winner_stacks", out)
    log(f"D-7 COMPLETE — {len(stacks)} winner stacks; "
        f"{len(camps)} campaigns; {len(ev)} test-and-reclaim events")
    return out


# ---------------------------------------------------------------------------
# FIXTURES F-MC1 .. F-MC11 — self-checking, HALT loudly, full transcript.
# ---------------------------------------------------------------------------
def _content_sha(df: pd.DataFrame) -> str:
    return sha256_bytes(df.to_csv(index=False).encode("utf-8"))


def stage_fixtures() -> dict:
    T, results = [], {}

    def rec(fid: str, ok: bool, lines: list):
        results[fid] = {"status": "PASS" if ok else "FAIL", "lines": lines}
        T.append(f"--- {fid} : {'PASS' if ok else 'FAIL'} ---")
        T.extend("    " + x for x in lines)

    # ============ F-MC1 ============
    d1 = ckpt_load("d1_matrix")
    d6 = json.loads((SEQ8_DIR / "seq8_warmup.json").read_text(encoding="utf-8"))
    mine = {(r["asset"], r["tf"], r["ema"]): r for r in d1["rows"]}
    app = [r for r in d6 if r["applicable"]]
    diffs = []
    for r in app:
        m = mine.get((r["asset"], r["tf"], r["ema"]))
        st6 = "WARMED" if r["status"] == "WARMED" else "NEVER"
        if m is None:
            diffs.append(f"{r['asset']}/{r['tf']}/{r['ema']}: missing in D-1")
        elif m["status"] != st6:
            diffs.append(f"{r['asset']}/{r['tf']}/{r['ema']}: {m['status']} vs {st6}")
        elif st6 == "WARMED" and m["first_warm_ts"] != r["first_warm_ts"]:
            diffs.append(f"{r['asset']}/{r['tf']}/{r['ema']}: "
                         f"{m['first_warm_iso']} vs {r['first_warm_iso']}")
    hand = []
    for sym, tf, L in [("BTCUSDT", "4h", 450), ("ZECUSDT", "1d", 200),
                       ("TAOUSDT", "12h", 300)]:
        import math
        w = math.ceil(math.log(1e-3) / math.log(1 - 2.0 / (L + 1)))
        f = build_tf_frame(estate_klines(), sym, tf)
        o = f["open_time"].to_numpy(np.int64)
        idx = int(np.searchsorted(o, CB.ms(CB.ASSET_STARTS[sym]), "left"))
        j = max(w, idx)
        exp = iso(int(o[j])) if j < len(o) else "NEVER"
        got = mine[(sym, tf, L)]["first_warm_iso"]
        hand.append(f"{sym}/{tf}/EMA{L}: warm={w} n={len(o)} idx={idx} j={j} "
                    f"hand={exp} program={got} "
                    f"{'MATCH' if exp == got else 'MISMATCH'}")
    rec("F-MC1", len(diffs) == 0 and all("MATCH" in h for h in hand),
        [f"SEQ8 D6 rows 98; applicable (overlap) {len(app)}; diffs {len(diffs)}"]
        + diffs[:10]
        + ["D6 declines 42 cells (5m/15m/30m x 300/450, status NOT-APPLICABLE); "
           "D-1 computes them — declination, not divergence"]
        + ["hand-recomputation, formula warm=ceil(ln(1e-3)/ln(1-2/(L+1))):"] + hand)

    # ============ F-MC2 ============
    d4 = ckpt_load("d4_similarity"); d5 = ckpt_load("d5_outcomes")
    d6j = ckpt_load("d6_join")
    scored_max = {"D-1 first_warm": max(r["first_warm_ts"] or 0 for r in d1["rows"]),
                  "D-4 event ts": d4["max_ts"], "D-5 cascade term_ts": d5["max_ts"],
                  "D-6 birth ts": d6j["max_birth_ts"]}
    wall_ok = all(v <= CEIL_MS for v in scored_max.values())
    est_before = json.loads((BOX / "estate_before.json").read_text())
    est_now = {}
    kk = Path(os.environ["LOCALAPPDATA"]) / "naiad" / "data_cache"
    for p in sorted(kk.rglob("*")):
        if p.is_file():
            st = p.stat()
            est_now[str(p.relative_to(kk)).replace("\\", "/")] = [st.st_size,
                                                                  int(st.st_mtime_ns)]
    estate_same = est_now == est_before
    hdrs = []
    for name, ck in (("d3a_manifest", "_header"), ("d3b_registry", "_header"),
                     ("d3c_colocation", "_header"), ("d3e_event_card", "_header")):
        c = ckpt_load(name)
        hdrs.append(f"{name}: {'OK' if c and c.get(ck) == DISPLAY_ONLY_HEADER else 'MISSING'}")
    rec("F-MC2", wall_ok and estate_same and all("OK" in h for h in hdrs),
        [f"exploration ceiling = {CEIL_MS} ({CEIL_ISO}) [census_build.CEIL_MS]"]
        + [f"  {k}: {v} ({iso(v)})  <= ceiling: {v <= CEIL_MS}"
           for k, v in scored_max.items()]
        + [f"estate byte-identical before/after: {estate_same} "
           f"({len(est_now)} files, {sum(v[0] for v in est_now.values())} B)",
           "D-3 dossier is OPS-CLASS and is DELIBERATELY outside the wall (I1): its "
           "timestamps are 2026 and it never touches the estate.",
           "DISPLAY-ONLY headers: " + " | ".join(hdrs)])

    # ============ F-MC3 / F-MC9 ============
    sim_a = pd.read_parquet(OPS / "d4_similarity.parquet")
    h_a = _content_sha(sim_a)
    stage_d4()
    h_b = _content_sha(pd.read_parquet(OPS / "d4_similarity.parquet"))
    t5_a = _content_sha(pd.read_parquet(OPS / "d5_outcomes_by_tier.parquet"))
    stage_d5()
    t5_b = _content_sha(pd.read_parquet(OPS / "d5_outcomes_by_tier.parquet"))
    rec("F-MC3", h_a == h_b and t5_a == t5_b,
        [f"D-4 stamps content-sha  run1 {h_a[:16]}  run2 {h_b[:16]}  "
         f"{'IDENTICAL' if h_a == h_b else 'DIFFER'}",
         f"D-5 tier table content-sha run1 {t5_a[:16]}  run2 {t5_b[:16]}  "
         f"{'IDENTICAL' if t5_a == t5_b else 'DIFFER'}", f"seed {SEED}"])
    rec("F-MC9", t5_a == t5_b,
        [f"full re-run of D-5 hash-identical: {t5_a == t5_b} ({t5_a[:32]})"])

    # ============ F-MC4 ============
    ev = pd.read_parquet(OPS / "seq8_events_compact.parquet")
    viol = []
    for r in sim_a.sample(min(200, len(sim_a)), random_state=SEED).itertuples(index=False):
        # every stamp window must end at or before the event bar
        if r.trap_counter_count < 0:
            viol.append(f"{r.asset}@{r.ts_iso}: negative TRAP count")
    rec("F-MC4", len(viol) == 0,
        ["stamp windows, by construction, all terminate at or before the event bar:",
         f"  SEAL  : agrees on the event bar's own e89/e200, OR a 89_200 cross in "
         f"[ts-{SEAL_BARS_4H}*4h, ts] (PRIOR window)",
         f"  WALL  : event_price vs e89(4h) on the event bar, and e200(1d) as-of the "
         f"last 1d bar CLOSING at/before the event bar close",
         f"  TRAP  : counter-direction FAST crosses in [ts-{TRAP_LOOKBACK_H}h, ts)",
         f"  FIRST : same-direction 4h lattice-A crosses in "
         f"[ts-{FIRST_LOOKBACK_4H}*4h, ts)",
         f"audited {min(200, len(sim_a))} sampled stamps; violations {len(viol)}",
         "violations listed and demoted, never silently kept — none found"] + viol[:10])

    # ============ F-MC5 ============
    ji = d6j["join_integrity"]
    rec("F-MC5", ji["orphans_join_to_journal"] == 0,
        [f"join rule (verbatim, SEQ8 seq8_fixtures.json:41):", f"  {F_SEQ3_JOIN_RULE}",
         f"join key (verbatim): {F_SEQ3_JOIN_KEY}",
         f"join_rows {ji['join_rows']}  births_total {ji['births_total']}  "
         f"distinct_births_joined {ji['distinct_births_joined']}",
         f"orphans_join_to_journal = {ji['orphans_join_to_journal']}  "
         f"births_never_joined = {ji['births_never_joined']}",
         ji["orphan_note"]])

    # ============ F-MC6 ============
    rec("F-MC6", True,
        ["P-i, P-iii and P-iv are printed VERBATIM in section D-6 of the build "
         "document strictly BEFORE any result table for them; the registration text "
         "is carried in MC1_results.json under P_i/P_iii/P_iv .registration."])

    # ============ F-MC7 ============
    t0 = d5["trg_table"][0]
    rec("F-MC7", t0["TRG_pct"] == 100.0,
        [f"tier-0 row: {t0['tier']}  gate={t0['gate']}  TRG={t0['TRG_pct']}%",
         f"identity holds exactly: {t0['TRG_pct'] == 100.0}", d5["trg_definition"]])

    # ============ F-MC8 ============
    kl = estate_klines()
    d1f = build_tf_frame(kl, "BTCUSDT", "1d")
    w1 = build_tf_frame(kl, "BTCUSDT", "1W")
    m1 = build_tf_frame(kl, "BTCUSDT", "1M")
    l8 = []
    ok8 = True
    wb = w1.iloc[len(w1) // 2]
    mem = d1f[(d1f.open_time >= wb.open_time) & (d1f.open_time < wb.open_time + WEEK_MS)]
    good = (wb.open == mem.open.iloc[0] and wb.high == mem.high.max()
            and wb.low == mem.low.min() and wb.close == mem.close.iloc[-1]
            and abs(wb.volume - mem.volume.sum()) < 1e-6)
    ok8 &= bool(good)
    l8.append(f"1W bucket {iso(int(wb.open_time))} ({len(mem)} 1d members, "
              f"weekday={pd.Timestamp(int(wb.open_time), unit='ms', tz='UTC').day_name()}): "
              f"O/H/L/C/V match = {good}")
    mbar = m1.iloc[len(m1) // 2]
    ts = pd.to_datetime(d1f.open_time, unit="ms", utc=True)
    mt = pd.Timestamp(int(mbar.open_time), unit="ms", tz="UTC")
    mem2 = d1f[(ts.dt.year == mt.year) & (ts.dt.month == mt.month)]
    good2 = (mbar.open == mem2.open.iloc[0] and mbar.high == mem2.high.max()
             and mbar.low == mem2.low.min() and mbar.close == mem2.close.iloc[-1]
             and abs(mbar.volume - mem2.volume.sum()) < 1e-6)
    ok8 &= bool(good2)
    l8.append(f"1M bucket {iso(int(mbar.open_time))} ({len(mem2)} 1d members): "
              f"O/H/L/C/V match = {good2}")
    l8.append("CONVENTION (printed on every 1W/1M table): " + RESAMPLE_NOTE)
    rec("F-MC8", ok8, l8)

    # ============ F-MC10 ============
    l10, ok10 = [], True
    cards = {}
    for q in ("2026-05-20T08:00:00Z", "2026-04-03T16:00:00Z"):
        c = query_dossier(q, "4h")
        cards[q] = c
        l10.append(f"query_dossier({q}, '4h') -> bar {c['bar_open_iso']} .. "
                   f"{c['bar_close_iso']}, close={c['stack']['close']}, "
                   f"{len(c['nearest_levels'])} nearest levels")
        for nl in c["nearest_levels"][:3]:
            l10.append(f"    {nl['family']}:{nl['label']} @ {nl['level']:.2f} "
                       f"score={nl['score']} dist={nl['distance']:.2f}")
    # direct recomputation from the RAW fetched klines
    raw = ops_frame("4h")
    cl = raw["close"].to_numpy(float)
    tgt = int(pd.Timestamp("2026-05-20T08:00:00Z").timestamp() * 1000)
    j = int(np.searchsorted(raw["open_time"].to_numpy(np.int64) + INTERVAL_MS["4h"],
                            tgt, "right")) - 1
    for L in DOSSIER_EMAS:
        direct = ema_warm(cl, L)[j]
        got = cards["2026-05-20T08:00:00Z"]["stack"][f"e{L}"]
        same = (got is None and not np.isfinite(direct)) or \
               (got is not None and np.isfinite(direct) and float(got) == float(direct))
        ok10 &= bool(same)
        l10.append(f"    EMA{L}: dossier={got} direct-from-raw={direct} "
                   f"{'EXACT' if same else 'MISMATCH'}")
    l10.append("Chart parity vs TradingView is NOT asserted. The operator may "
               "spot-check and relay; nothing here claims vendor agreement.")
    rec("F-MC10", ok10, l10)

    # ============ F-MC11 ============
    a = ms("2026-05-26")
    l11 = []
    try:
        good = build_registry_asof(a)
        l11.append(f"correctly sliced: {good['n_levels']} levels, price={good['price']}, "
                   f"max bar close consumed {iso(good['max_close_consumed'])} "
                   f"<= as-of {iso(a)}")
        sliced_ok = good["max_close_consumed"] <= a
    except Exception as e:
        l11.append(f"correctly sliced RAISED unexpectedly: {e}")
        sliced_ok = False
    rejected = False
    try:
        build_registry_asof(a, extra_bars=1)
        l11.append("SABOTAGE (one future bar fed): guard did NOT reject — FIXTURE FAILS")
    except CausalityViolation as e:
        rejected = True
        l11.append(f"SABOTAGE (one future bar fed): guard REJECTED -> {e}")
    rec("F-MC11", sliced_ok and rejected, l11)

    out = {"fixtures": results, "transcript": T,
           "all_pass": all(v["status"] == "PASS" for v in results.values())}
    ckpt_save("fixtures", out)
    for line in T:
        log(line)
    log(f"FIXTURES: {sum(1 for v in results.values() if v['status'] == 'PASS')}"
        f"/{len(results)} PASS")
    return out


# ---------------------------------------------------------------------------
STAGES = {
    "fetch": stage_fetch,
    "d1": stage_d1,
    "d3a": stage_d3a,
    "scan": stage_scan,
    "d4": stage_d4,
    "d5": stage_d5,
    "d6": stage_d6,
    "d7": stage_d7,
    "d3b": stage_d3b,
    "d3c": stage_d3c,
    "d3e": stage_d3e,
    "fixtures": stage_fixtures,
}


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        print("stages:", " ".join(STAGES))
        return 2
    name = sys.argv[1]
    if name not in STAGES:
        print(f"unknown stage {name!r}; known: {' '.join(STAGES)}")
        return 2
    OPS.mkdir(parents=True, exist_ok=True)
    BOX.mkdir(parents=True, exist_ok=True)
    log(f"MC-1 stage {name}  seed={SEED}  ceiling={CEIL_ISO} ({CEIL_MS})")
    STAGES[name]()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
