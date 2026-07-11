"""Data layer (build prompt §4).

- Bulk backfill from data.binance.vision (USDT-M futures klines: monthly zips,
  then daily zips), incremental top-up via REST /fapi/v1/klines.
- Funding history via /fapi/v1/fundingRate.
- Raw candles live ONLY in a local cache directory (never committed —
  invariant 9). Default cache is OUTSIDE the repo (LOCALAPPDATA / ~/.cache) so
  cloud-synced repo folders don't ingest gigabytes; override with
  NAIAD_CACHE_DIR.
- Integrity checks after every backfill: gap scan, duplicate scan, monotonic
  open_time, coverage report per symbol/interval.
- LIT two-token trap: first_valid = max(detected_first_candle, 2025-12-01T00:00Z),
  asserted in the loader — earlier LITUSDT history is a different asset
  (Litentry) and must never load.

All timestamps are UTC milliseconds; bar identity = (symbol, interval, open_time).
"""

import io
import json
import os
import time
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import requests

from engine.cells import INTERVAL_MS, LIT_FLOOR_MS

BULK_BASE = "https://data.binance.vision/data/futures/um"
REST_BASE = "https://fapi.binance.com"

KLINE_COLS = ["open_time", "open", "high", "low", "close", "volume"]


def cache_dir() -> Path:
    env = os.environ.get("NAIAD_CACHE_DIR")
    if env:
        base = Path(env)
    elif os.name == "nt":
        base = Path(os.environ["LOCALAPPDATA"]) / "naiad" / "data_cache"
    else:
        base = Path.home() / ".cache" / "naiad" / "data_cache"
    base.mkdir(parents=True, exist_ok=True)
    return base


def _kline_path(symbol: str, interval: str) -> Path:
    p = cache_dir() / "klines"
    p.mkdir(parents=True, exist_ok=True)
    return p / f"{symbol}_{interval}.parquet"


def _funding_path(symbol: str) -> Path:
    p = cache_dir() / "funding"
    p.mkdir(parents=True, exist_ok=True)
    return p / f"{symbol}.parquet"


def _get(url: str, params: dict | None = None, retries: int = 4) -> requests.Response:
    last = None
    for attempt in range(retries):
        try:
            r = requests.get(url, params=params, timeout=60)
            if r.status_code in (200, 404):
                return r
            last = RuntimeError(f"HTTP {r.status_code} for {url}")
        except requests.RequestException as e:  # transient network error
            last = e
        time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"failed after {retries} attempts: {url}") from last


def _normalize_ms(ts: np.ndarray) -> np.ndarray:
    """Some archive files carry microsecond timestamps; normalize to ms."""
    ts = ts.astype(np.int64)
    return np.where(ts > 10_000_000_000_000_000, ts // 1000, ts)


def _parse_kline_csv(raw: bytes) -> pd.DataFrame:
    text = raw.decode("utf-8")
    first_line = text.split("\n", 1)[0]
    header = 0 if first_line.startswith("open_time") else None
    df = pd.read_csv(io.StringIO(text), header=header)
    df = df.iloc[:, :6]
    df.columns = KLINE_COLS
    df["open_time"] = _normalize_ms(df["open_time"].to_numpy())
    for c in KLINE_COLS[1:]:
        df[c] = df[c].astype(np.float64)
    return df


def _fetch_bulk_zip(symbol: str, interval: str, stamp: str, monthly: bool) -> pd.DataFrame | None:
    kind = "monthly" if monthly else "daily"
    url = f"{BULK_BASE}/{kind}/klines/{symbol}/{interval}/{symbol}-{interval}-{stamp}.zip"
    r = _get(url)
    if r.status_code == 404:
        return None
    with zipfile.ZipFile(io.BytesIO(r.content)) as z:
        name = z.namelist()[0]
        return _parse_kline_csv(z.read(name))


def _fetch_rest_klines(symbol: str, interval: str, start_ms: int, end_ms: int) -> pd.DataFrame:
    frames = []
    cursor = start_ms
    while cursor <= end_ms:
        r = _get(f"{REST_BASE}/fapi/v1/klines",
                 params={"symbol": symbol, "interval": interval,
                         "startTime": cursor, "endTime": end_ms, "limit": 1500})
        rows = r.json()
        if not rows:
            break
        df = pd.DataFrame(rows).iloc[:, :6]
        df.columns = KLINE_COLS
        df["open_time"] = _normalize_ms(df["open_time"].to_numpy())
        for c in KLINE_COLS[1:]:
            df[c] = df[c].astype(np.float64)
        frames.append(df)
        nxt = int(df["open_time"].iloc[-1]) + INTERVAL_MS[interval]
        if nxt <= cursor:
            break
        cursor = nxt
        time.sleep(0.15)  # stay far below REST weight limits
    if not frames:
        return pd.DataFrame(columns=KLINE_COLS)
    return pd.concat(frames, ignore_index=True)


def detect_first_candle(symbol: str, interval: str) -> int | None:
    """First available futures candle open_time (ms) for symbol/interval."""
    r = _get(f"{REST_BASE}/fapi/v1/klines",
             params={"symbol": symbol, "interval": interval, "startTime": 0, "limit": 1})
    rows = r.json()
    if not rows or (isinstance(rows, dict) and rows.get("code")):
        return None
    return int(rows[0][0])


def first_valid_ms(symbol: str, interval: str, detected_first: int) -> int:
    """Hard rule for LIT (build prompt §4): floor at 2025-12-01T00:00Z."""
    if symbol == "LITUSDT":
        return max(detected_first, LIT_FLOOR_MS)
    return detected_first


def _load_cache(symbol: str, interval: str) -> pd.DataFrame:
    path = _kline_path(symbol, interval)
    try:
        return pd.read_parquet(path)
    except FileNotFoundError:
        # the only legitimate "no cache yet" signal — a transient stat or
        # read failure must raise, never masquerade as an empty cache
        return pd.DataFrame(columns=KLINE_COLS)


def _save_cache(symbol: str, interval: str, df: pd.DataFrame) -> None:
    # No-shrink invariant (engine 1.0.2): a cache file never loses rows through
    # this save path. Rows already durably on disk are merged back in
    # regardless of what the caller assembled, and the whole file lands
    # atomically via a same-directory temp + os.replace, so an interrupted run
    # cannot corrupt or truncate the destination. New rows win at identical
    # open_time (keep="last"): values are correctable, timestamps never
    # droppable. This choke point covers EVERY writer, census --repair included.
    #
    # No deletion primitive: because the save path can no longer shrink a file,
    # genuine row removal is out-of-band — delete the file, then re-extend via
    # census.py --extend (which fetches from the 2019 listing, not a warm-up
    # anchor). Accepted residuals: (1) a concurrent last-writer may drop the
    # OTHER writer's freshly fetched rows — refetchable, never a shrink below
    # what was on disk; (2) a file deleted and recreated through an engine path
    # restarts at the warm-up anchor, not the listing — coverage_ok vs
    # data_starts.csv is the detector.
    path = _kline_path(symbol, interval)
    try:
        df = pd.concat([pd.read_parquet(path), df], ignore_index=True)
    except FileNotFoundError:
        pass
    df = df.drop_duplicates("open_time", keep="last").sort_values("open_time")
    df = df.reset_index(drop=True)
    tmp = path.with_name(f"{path.name}.{os.getpid()}.tmp")
    df.to_parquet(tmp, index=False)
    os.replace(tmp, path)  # atomic — an interrupted run can't corrupt the file


FUNDING_COLS = ["funding_time", "funding_rate"]


def _load_funding(symbol: str) -> pd.DataFrame:
    # Funding twin of _load_cache: only an absent file yields an empty frame;
    # any other read failure raises rather than masquerading as "no cache yet".
    path = _funding_path(symbol)
    try:
        return pd.read_parquet(path)
    except FileNotFoundError:
        return pd.DataFrame(columns=FUNDING_COLS)


def _save_funding(symbol: str, df: pd.DataFrame) -> pd.DataFrame:
    # Funding twin of _save_cache — same no-shrink + atomic invariant, same
    # no-delete property and accepted residuals (see _save_cache). Rows already
    # on disk are merged back in (new rows win at identical funding_time), then
    # the file lands atomically via a same-directory temp + os.replace.
    path = _funding_path(symbol)
    try:
        df = pd.concat([pd.read_parquet(path), df], ignore_index=True)
    except FileNotFoundError:
        pass
    df = (df.drop_duplicates("funding_time", keep="last")
            .sort_values("funding_time").reset_index(drop=True))
    tmp = path.with_name(f"{path.name}.{os.getpid()}.tmp")
    df.to_parquet(tmp, index=False)
    os.replace(tmp, path)  # atomic — an interrupted run can't corrupt the file
    return df


def _month_starts(start_ms: int, end_ms: int) -> list[datetime]:
    d = datetime.fromtimestamp(start_ms / 1000, timezone.utc).replace(
        day=1, hour=0, minute=0, second=0, microsecond=0)
    end = datetime.fromtimestamp(end_ms / 1000, timezone.utc)
    out = []
    while d <= end:
        out.append(d)
        d = (d.replace(day=28) + pd.Timedelta(days=4)).replace(day=1)
    return out


def backfill_klines(symbol: str, interval: str, start_ms: int, end_ms: int,
                    log=print) -> pd.DataFrame:
    """Ensure the cache covers [start_ms, end_ms]; returns the covering frame.

    Strategy: monthly zips for complete months, daily zips for the tail,
    REST /fapi/v1/klines for anything still missing (today's partial day).
    """
    detected = detect_first_candle(symbol, interval)
    if detected is None:
        raise RuntimeError(f"{symbol} {interval}: no futures klines exist")
    start_ms = max(start_ms, first_valid_ms(symbol, interval, detected))

    cache = _load_cache(symbol, interval)
    have = set(cache["open_time"].to_numpy()) if len(cache) else set()
    step = INTERVAL_MS[interval]
    now_ms = int(time.time() * 1000)
    end_ms = min(end_ms, (now_ms // step) * step - step)  # last CLOSED bar only

    frames = [cache] if len(cache) else []
    this_month = datetime.fromtimestamp(now_ms / 1000, timezone.utc).replace(
        day=1, hour=0, minute=0, second=0, microsecond=0)

    for m in _month_starts(start_ms, end_ms):
        m_start = int(m.timestamp() * 1000)
        m_end_dt = (m.replace(day=28) + pd.Timedelta(days=4)).replace(day=1)
        m_end = int(m_end_dt.timestamp() * 1000)
        expected = range(max(m_start, (start_ms // step) * step),
                         min(m_end, end_ms + step), step)
        if all(t in have for t in expected):
            continue
        if m < this_month:
            df = _fetch_bulk_zip(symbol, interval, m.strftime("%Y-%m"), monthly=True)
            if df is not None:
                frames.append(df)
                have.update(df["open_time"].to_numpy())
                log(f"  {symbol} {interval} {m:%Y-%m}: monthly zip, {len(df)} bars")
                continue
        # daily zips for the partial/missing month, then REST for the remainder
        day = max(m, datetime.fromtimestamp(start_ms / 1000, timezone.utc).replace(
            hour=0, minute=0, second=0, microsecond=0))
        end_day = min(m_end_dt, datetime.fromtimestamp(end_ms / 1000, timezone.utc))
        got_daily = 0
        while day <= end_day:
            d_start = int(day.timestamp() * 1000)
            d_expected = range(d_start, min(d_start + 86_400_000, end_ms + step), step)
            if not all(t in have for t in d_expected):
                df = _fetch_bulk_zip(symbol, interval, day.strftime("%Y-%m-%d"), monthly=False)
                if df is None:
                    break
                frames.append(df)
                have.update(df["open_time"].to_numpy())
                got_daily += 1
            day += pd.Timedelta(days=1)
        if got_daily:
            log(f"  {symbol} {interval} {m:%Y-%m}: {got_daily} daily zips")

    merged = (pd.concat(frames, ignore_index=True) if frames
              else pd.DataFrame(columns=KLINE_COLS))
    have = set(merged["open_time"].to_numpy()) if len(merged) else set()
    missing = [t for t in range((start_ms // step) * step, end_ms + step, step)
               if t not in have and t >= start_ms]
    if missing:
        df = _fetch_rest_klines(symbol, interval, missing[0], end_ms)
        if len(df):
            merged = pd.concat([merged, df], ignore_index=True)
            log(f"  {symbol} {interval}: REST top-up, {len(df)} bars")

    _save_cache(symbol, interval, merged)
    return load_klines(symbol, interval, start_ms, end_ms)


def load_klines(symbol: str, interval: str, start_ms: int, end_ms: int) -> pd.DataFrame:
    """Load from cache. Asserts the LIT floor (invariant: in the loader, not
    just the docs) and monotonic, duplicate-free open times."""
    df = _load_cache(symbol, interval)
    df = df[(df["open_time"] >= start_ms) & (df["open_time"] <= end_ms)]
    df = df.sort_values("open_time").reset_index(drop=True)
    if symbol == "LITUSDT" and len(df):
        if int(df["open_time"].min()) < LIT_FLOOR_MS:
            raise AssertionError(
                "LITUSDT candles before 2025-12-01T00:00Z reached the loader — "
                "that history is Litentry, a different asset. Refusing to load.")
    ot = df["open_time"].to_numpy()
    if len(ot) > 1:
        d = np.diff(ot)
        if (d <= 0).any():
            raise AssertionError(f"{symbol} {interval}: non-monotonic or duplicate open_time in cache")
    return df


def integrity_report(symbol: str, interval: str, df: pd.DataFrame) -> dict:
    """Gap/duplicate/monotonic scan; gaps are reported (exchange downtime
    exists), duplicates and disorder are hard failures upstream."""
    step = INTERVAL_MS[interval]
    ot = df["open_time"].to_numpy()
    gaps = []
    if len(ot) > 1:
        d = np.diff(ot)
        for i in np.nonzero(d != step)[0]:
            gaps.append({"after": int(ot[i]), "missing_bars": int(d[i] // step - 1)})
    return {
        "symbol": symbol, "interval": interval, "bars": int(len(df)),
        "first": int(ot[0]) if len(ot) else None,
        "last": int(ot[-1]) if len(ot) else None,
        "duplicates": int(len(df) - df["open_time"].nunique()),
        "gaps": gaps,
    }


def write_coverage_report(reports: list[dict], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(reports, f, indent=2, sort_keys=True)


def backfill_funding(symbol: str, start_ms: int, end_ms: int, log=print) -> pd.DataFrame:
    """Funding rate history via REST (1000/page). Cached like klines."""
    cache = _load_funding(symbol)
    cursor = start_ms
    if len(cache):
        covered = cache[(cache["funding_time"] >= start_ms)]
        if len(covered):
            cursor = int(cache["funding_time"].max()) + 1
    frames = [cache] if len(cache) else []
    while cursor <= end_ms:
        r = _get(f"{REST_BASE}/fapi/v1/fundingRate",
                 params={"symbol": symbol, "startTime": cursor,
                         "endTime": end_ms, "limit": 1000})
        rows = r.json()
        if not rows:
            break
        df = pd.DataFrame(rows)
        df = pd.DataFrame({
            "funding_time": _normalize_ms(df["fundingTime"].to_numpy(dtype=np.int64)),
            "funding_rate": df["fundingRate"].astype(np.float64),
        })
        frames.append(df)
        nxt = int(df["funding_time"].iloc[-1]) + 1
        if nxt <= cursor:
            break
        cursor = nxt
        time.sleep(0.15)
    assembled = (pd.concat(frames, ignore_index=True) if frames
                 else pd.DataFrame(columns=FUNDING_COLS))
    merged = _save_funding(symbol, assembled)  # merge-in-save + atomic replace
    if log:
        log(f"  {symbol} funding: {len(merged)} rows cached")
    return merged[(merged["funding_time"] >= start_ms) & (merged["funding_time"] <= end_ms)] \
        .reset_index(drop=True)


def load_funding(symbol: str, start_ms: int, end_ms: int) -> pd.DataFrame:
    df = _load_funding(symbol)
    return df[(df["funding_time"] >= start_ms) & (df["funding_time"] <= end_ms)] \
        .sort_values("funding_time").reset_index(drop=True)
