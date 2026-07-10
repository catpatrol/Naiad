"""v12 Study V1 fixtures F1–F9 (census build prompt §6).

All synthetic, all hermetic: every test builds its own cache under tmp_path
and points NAIAD_CACHE_DIR at it — no network, no real estate, CI-safe.
The Phase 1 suite (F1–F8 in the other files) is untouched.
"""

import json
import shutil
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from fixtures.conftest import ROOT  # noqa: F401  (sys.path side effect)
from engine.cells import INTERVAL_MS
from study import census as cz
from study import loader
from study.loader import (EDGE_EXCL_MS, LIT_FLOOR_STUDY_MS, LOCKBOX_END_EXCL_MS,
                          LOCKBOX_START_MS, LockboxViolation,
                          load_study_klines, partition_class)

H = 3_600_000
D = 86_400_000


def utc_ms(s: str) -> int:
    from datetime import datetime, timezone
    return int(datetime.strptime(s, "%Y-%m-%d %H:%M")
               .replace(tzinfo=timezone.utc).timestamp() * 1000)


def write_klines(cache: Path, symbol: str, interval: str,
                 open_times: np.ndarray) -> Path:
    (cache / "klines").mkdir(parents=True, exist_ok=True)
    n = len(open_times)
    df = pd.DataFrame({
        "open_time": open_times.astype(np.int64),
        "open": np.full(n, 100.0), "high": np.full(n, 101.0),
        "low": np.full(n, 99.0), "close": np.full(n, 100.5),
        "volume": np.full(n, 10.0),
    })
    p = cache / "klines" / f"{symbol}_{interval}.parquet"
    df.to_parquet(p, index=False)
    return p


def write_funding(cache: Path, symbol: str, times: np.ndarray) -> Path:
    (cache / "funding").mkdir(parents=True, exist_ok=True)
    p = cache / "funding" / f"{symbol}.parquet"
    pd.DataFrame({"funding_time": times.astype(np.int64),
                  "funding_rate": np.full(len(times), 1e-4)}) \
        .to_parquet(p, index=False)
    return p


def grid(start_ms: int, end_ms: int, step: int) -> np.ndarray:
    return np.arange(start_ms, end_ms + step, step, dtype=np.int64)


def guard_events(cache: Path) -> list[dict]:
    p = cache / "guard_log.jsonl"
    if not p.exists():
        return []
    return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines()]


@pytest.fixture()
def study_cache(tmp_path, monkeypatch):
    cache = tmp_path / "cache"
    cache.mkdir()
    monkeypatch.setenv("NAIAD_CACHE_DIR", str(cache))
    return cache


# ── F1 — LIT floor ───────────────────────────────────────────────────────────

def test_v12_f1_lit_floor(study_cache):
    pre = utc_ms("2025-12-20 00:00")          # pre-floor rows in the cache
    end = utc_ms("2025-12-24 00:00")
    for iv, step in INTERVAL_MS.items():
        write_klines(study_cache, "LITUSDT", iv, grid(pre, end, step))
        df = load_study_klines("LITUSDT", iv, pre, end)
        assert len(df) and int(df["open_time"].min()) >= LIT_FLOOR_STUDY_MS, iv
    # request entirely before the floor -> empty + guard event
    df = load_study_klines("LITUSDT", "1h",
                           utc_ms("2025-01-01 00:00"), utc_ms("2025-12-22 00:00"))
    assert len(df) == 0
    ev = [e["event"] for e in guard_events(study_cache)]
    assert "lit_floor_empty" in ev and "lit_floor_clamp" in ev


# ── F2 — study right edge ────────────────────────────────────────────────────

def test_v12_f2_right_edge(study_cache):
    start = utc_ms("2026-07-07 00:00")
    write_klines(study_cache, "BTCUSDT", "1h",
                 grid(start, utc_ms("2026-07-09 12:00"), H))
    df = load_study_klines("BTCUSDT", "1h", start, utc_ms("2026-07-09 12:00"))
    assert int(df["open_time"].max()) == utc_ms("2026-07-07 23:00")
    assert int(df["open_time"].max()) < EDGE_EXCL_MS
    ev = [e["event"] for e in guard_events(study_cache)]
    assert "right_edge_clamp" in ev
    # entirely past the edge -> empty + guard event
    df2 = load_study_klines("BTCUSDT", "1h",
                            utc_ms("2026-07-08 00:00"), utc_ms("2026-07-09 00:00"))
    assert len(df2) == 0
    assert "right_edge_empty" in [e["event"] for e in guard_events(study_cache)]


# ── F3 — lockbox seal ────────────────────────────────────────────────────────

def test_v12_f3_lockbox_seal(study_cache):
    start = utc_ms("2024-06-25 00:00")
    end = utc_ms("2024-07-05 00:00")
    write_klines(study_cache, "BTCUSDT", "4h", grid(start, end, 4 * H))
    with pytest.raises(LockboxViolation):
        load_study_klines("BTCUSDT", "4h",
                          utc_ms("2024-06-28 00:00"), utc_ms("2024-07-03 00:00"))
    # integrity mode on the same range: counts/hashes only, no OHLCV anywhere
    view = load_study_klines("BTCUSDT", "4h",
                             utc_ms("2024-06-28 00:00"), utc_ms("2024-07-03 00:00"),
                             integrity_only=True)
    assert view.row_count == 31 and view.duplicate_count == 0
    assert len(view.file_sha256) == 64
    assert not any(hasattr(view, a) for a in ("open", "high", "low", "close",
                                              "volume"))
    # value reads that stay outside the box are lawful
    df = load_study_klines("BTCUSDT", "4h", start, utc_ms("2024-06-30 23:59"))
    assert int(df["open_time"].max()) < LOCKBOX_START_MS


# ── F4 — timestamp discipline ────────────────────────────────────────────────

def test_v12_f4_timestamp_discipline(study_cache):
    t0 = utc_ms("2024-01-10 00:00")
    ts = [t0, t0 + H, t0 + H,            # duplicate
          t0 + 3 * H, t0 + 2 * H,        # backward
          t0 + 4 * H + 123]              # off-grid
    write_klines(study_cache, "BTCUSDT", "1h", np.array(ts))
    rep = cz.census_kline_file("BTCUSDT", "1h", {}, {}, "synthetic")
    a = rep["anomalies"]
    assert [d["open_ms"] for d in a["duplicates"]] == [t0 + H]
    assert a["duplicates"][0]["occurrences"] == 2
    assert [d["open_ms"] for d in a["backward"]] == [t0 + 2 * H]
    assert [d["open_ms"] for d in a["off_grid"]] == [t0 + 4 * H + 123]
    assert rep["anomaly_count"] == 3


# ── F5 — gap detection ───────────────────────────────────────────────────────

def test_v12_f5_gap_detection(study_cache):
    t0 = utc_ms("2024-01-01 00:00")
    ts = grid(t0, t0 + 10 * D, H)
    hole_start = t0 + 5 * D              # 3 candles removed, > 24h from birth
    hole = (ts >= hole_start) & (ts < hole_start + 3 * H)
    write_klines(study_cache, "ETHUSDT", "1h", ts[~hole])
    rep = cz.census_kline_file("ETHUSDT", "1h", {}, {}, "synthetic")
    assert rep["gap_count"] == 1
    g = rep["gaps"][0]
    assert g["gap_start_ms"] == hole_start
    assert g["gap_end_ms"] == hole_start + 2 * H
    assert g["bars_missing"] == 3
    assert g["classification"] == "download_hole"
    # ...and two failed re-fetch attempts escalate it to exchange_side
    refetch = {f"ETHUSDT|1h|{hole_start}": {"attempts": 2,
                                            "result": "still_missing"}}
    rep2 = cz.census_kline_file("ETHUSDT", "1h", refetch, {}, "synthetic")
    assert rep2["gaps"][0]["classification"] == "exchange_side"


# ── F6 — census determinism ──────────────────────────────────────────────────

def test_v12_f6_census_determinism(study_cache, tmp_path):
    t0 = utc_ms("2024-01-01 00:00")
    for sym in ("BTCUSDT", "ETHUSDT"):
        for iv in ("1h", "4h"):
            write_klines(study_cache, sym, iv,
                         grid(t0, t0 + 30 * D, INTERVAL_MS[iv]))
        write_funding(study_cache, sym, grid(t0, t0 + 30 * D, 8 * H))
    out1, out2 = tmp_path / "run1", tmp_path / "run2"
    side = tmp_path / "sidecars"
    cz.run_census(out1, side, symbols=["BTCUSDT", "ETHUSDT"],
                  intervals=["1h", "4h"])
    cz.run_census(out2, side, symbols=["BTCUSDT", "ETHUSDT"],
                  intervals=["1h", "4h"])
    b1 = (out1 / "census.json").read_bytes()
    b2 = (out2 / "census.json").read_bytes()
    assert b1 == b2
    assert (out1 / "DATA_CENSUS.md").read_bytes() == \
           (out2 / "DATA_CENSUS.md").read_bytes()


# ── F7 — partition tagging ───────────────────────────────────────────────────

def test_v12_f7_partition_tagging(study_cache):
    m = utc_ms
    assert partition_class("BTCUSDT", m("2024-06-30 23:59")) == "exploration-classic"
    assert partition_class("BTCUSDT", m("2024-07-01 00:00")) == "lockbox"
    assert partition_class("BTCUSDT", m("2025-10-05 23:59")) == "lockbox"
    assert partition_class("BTCUSDT", m("2025-10-06 00:00")) == "spent"
    for sym in ("ETHUSDT", "LITUSDT", "FARTCOINUSDT"):
        assert partition_class(sym, m("2025-10-06 00:00")) == "regime-contaminated"
        assert partition_class(sym, m("2024-07-01 00:00")) == "lockbox"
    assert partition_class("BTCUSDT", m("2026-07-08 00:00")) == "forward"
    # end-to-end: histogram puts the boundary minutes in the right buckets
    ts = np.array([m("2024-06-30 23:59"), m("2024-07-01 00:00"),
                   m("2025-10-05 23:59"), m("2025-10-06 00:00")])
    write_klines(study_cache, "BTCUSDT", "1m", ts)
    rep = cz.census_kline_file("BTCUSDT", "1m", {}, {}, "synthetic")
    p = rep["partition_rows"]
    assert p["exploration-classic"] == 1 and p["lockbox"] == 2
    assert p["spent"] == 1 and p["regime-contaminated"] == 0
    write_klines(study_cache, "ETHUSDT", "1m", ts)
    rep2 = cz.census_kline_file("ETHUSDT", "1m", {}, {}, "synthetic")
    p2 = rep2["partition_rows"]
    assert p2["spent"] == 0 and p2["regime-contaminated"] == 1


# ── F8 — hash integrity ──────────────────────────────────────────────────────

def test_v12_f8_hash_integrity(study_cache, tmp_path, monkeypatch):
    t0 = utc_ms("2024-01-01 00:00")
    write_klines(study_cache, "BTCUSDT", "1h", grid(t0, t0 + 10 * D, H))
    write_funding(study_cache, "BTCUSDT", grid(t0, t0 + 10 * D, 8 * H))
    out = tmp_path / "out"
    census = cz.run_census(out, tmp_path / "side", symbols=["BTCUSDT"],
                           intervals=["1h"])
    assert cz.verify_hashes(census) == []
    # flip one byte in a COPY of the estate and re-verify against the manifest
    flipped = tmp_path / "flipped"
    shutil.copytree(study_cache, flipped)
    target = flipped / "klines" / "BTCUSDT_1h.parquet"
    raw = bytearray(target.read_bytes())
    raw[len(raw) // 2] ^= 0xFF
    target.write_bytes(bytes(raw))
    monkeypatch.setenv("NAIAD_CACHE_DIR", str(flipped))
    bad = cz.verify_hashes(census)
    assert [b["path"] for b in bad] == ["klines/BTCUSDT_1h.parquet"]


# ── F9 — funding continuity ──────────────────────────────────────────────────

def test_v12_f9_funding_continuity(study_cache):
    t0 = utc_ms("2024-01-01 00:00")
    times = grid(t0, t0 + 20 * D, 8 * H)
    missing = t0 + 10 * D                      # drop one 8h settlement
    times = times[times != missing]
    jitter = np.zeros(len(times), dtype=np.int64)
    jitter[1::7] = 15                          # observed Binance ms jitter
    write_funding(study_cache, "BTCUSDT", times + jitter)
    rep = cz.census_funding_file("BTCUSDT", {}, {}, "synthetic")
    assert rep["gap_count"] == 1
    g = rep["gaps"][0]
    assert g["gap_start_ms"] == missing and g["gap_end_ms"] == missing
    assert g["records_missing"] == 1 and g["local_grid_hours"] == 8
    assert rep["max_jitter_ms"] == 15 and not rep["jitter_over_tolerance"]
    assert rep["grid_segments"][0]["spacing_hours"] == 8.0
