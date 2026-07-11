"""Engine 1.0.2 fixtures N1–N5 — the cache no-shrink invariant.

All synthetic, all hermetic: every test points NAIAD_CACHE_DIR at its own
tmp dir and drives the real save/load choke points in engine.data — no
network, no real estate, CI-safe. The N-series is the data-side twin of the
stop-ratchet fixtures: it pins "a cache file never loses rows through the save
path" mechanically, so the truncation that motivated 1.0.2 cannot recur.
"""

import hashlib

import numpy as np
import pandas as pd
import pytest

from fixtures.conftest import ROOT  # noqa: F401  (sys.path side effect)
from engine.data import (_kline_path, _load_cache, _load_funding,
                         _save_cache, _save_funding, _funding_path)

H = 3_600_000          # one hour in ms
D = 86_400_000         # one day in ms
T0 = 1_704_067_200_000  # 2024-01-01T00:00:00Z


@pytest.fixture()
def noshrink_env(tmp_path, monkeypatch):
    """A fake NAIAD_CACHE_DIR; the real cache is never touched."""
    cache = tmp_path / "cache"
    cache.mkdir()
    monkeypatch.setenv("NAIAD_CACHE_DIR", str(cache))
    return cache


def kline_frame(open_times: np.ndarray, close: float = 100.5) -> pd.DataFrame:
    n = len(open_times)
    return pd.DataFrame({
        "open_time": open_times.astype(np.int64),
        "open": np.full(n, 100.0),
        "high": np.full(n, 101.0),
        "low": np.full(n, 99.0),
        "close": np.full(n, close, dtype=float),
        "volume": np.full(n, 10.0),
    })


def funding_frame(times: np.ndarray, rate: float = 1e-4) -> pd.DataFrame:
    return pd.DataFrame({
        "funding_time": times.astype(np.int64),
        "funding_rate": np.full(len(times), rate, dtype=float),
    })


# ── N1 — merge-preserve (the invariant itself) ───────────────────────────────

def test_n1_merge_preserve(noshrink_env):
    full_t = np.arange(T0, T0 + 90 * D, H)          # 90 days of hourly bars
    _save_cache("BTCUSDT", "1h", kline_frame(full_t, close=100.5))
    assert len(_load_cache("BTCUSDT", "1h")) == len(full_t)

    # a one-month windowed slice with ALTERED values in the overlap — exactly
    # the shape every replay writer assembles, and the shape that truncated the
    # estate before 1.0.2
    win_t = np.arange(T0 + 30 * D, T0 + 60 * D, H)
    _save_cache("BTCUSDT", "1h", kline_frame(win_t, close=200.0))
    after = _load_cache("BTCUSDT", "1h")

    # bounds and total row count survive the windowed save
    assert int(after["open_time"].min()) == int(full_t[0])
    assert int(after["open_time"].max()) == int(full_t[-1])
    assert len(after) == len(full_t)

    # overlapping timestamps carry the NEW values; everything else is untouched
    inside = after[after["open_time"].isin(win_t)]
    outside = after[~after["open_time"].isin(win_t)]
    assert len(inside) == len(win_t)
    assert (inside["close"] == 200.0).all()
    assert (outside["close"] == 100.5).all()

    # repeating the windowed save changes nothing (idempotent)
    before = _load_cache("BTCUSDT", "1h")
    _save_cache("BTCUSDT", "1h", kline_frame(win_t, close=200.0))
    pd.testing.assert_frame_equal(_load_cache("BTCUSDT", "1h"), before)


# ── N2 — loud load ───────────────────────────────────────────────────────────

def test_n2_loud_load(noshrink_env):
    path = _kline_path("BTCUSDT", "1h")
    path.write_bytes(b"this is not a parquet file")   # present but unreadable
    # "unreadable" must never masquerade as "absent" (a silent empty frame);
    # any exception is acceptable EXCEPT a quiet return.
    with pytest.raises(Exception) as exc:
        _load_cache("BTCUSDT", "1h")
    assert not isinstance(exc.value, FileNotFoundError)


# ── N3 — atomic abort ────────────────────────────────────────────────────────

def test_n3_atomic_abort(noshrink_env, monkeypatch):
    _save_cache("BTCUSDT", "1h", kline_frame(np.arange(T0, T0 + 30 * D, H)))
    path = _kline_path("BTCUSDT", "1h")
    before = hashlib.sha256(path.read_bytes()).hexdigest()

    def boom(*args, **kwargs):
        raise RuntimeError("simulated disk failure mid-write")

    monkeypatch.setattr(pd.DataFrame, "to_parquet", boom)
    win = kline_frame(np.arange(T0 + 30 * D, T0 + 60 * D, H), close=200.0)
    with pytest.raises(RuntimeError):
        _save_cache("BTCUSDT", "1h", win)

    # the destination file's bytes are byte-for-byte unchanged by the failed
    # save — os.replace never ran, so the original can't be truncated/corrupted
    after = hashlib.sha256(path.read_bytes()).hexdigest()
    assert after == before


# ── N4 — first save (FileNotFoundError branch on the merge-read) ──────────────

def test_n4_first_save(noshrink_env):
    path = _kline_path("BTCUSDT", "1h")
    assert not path.exists()
    t = np.arange(T0, T0 + 10 * D, H)
    _save_cache("BTCUSDT", "1h", kline_frame(t))       # must not raise on absent
    assert path.exists()
    got = _load_cache("BTCUSDT", "1h")
    assert len(got) == len(t)
    assert int(got["open_time"].min()) == int(t[0])
    assert int(got["open_time"].max()) == int(t[-1])


# ── N5 — funding mirror (N1 replayed against the funding cache path) ──────────

def test_n5_funding_mirror(noshrink_env):
    full_t = np.arange(T0, T0 + 90 * D, 8 * H)         # 90 days, 8h grid
    _save_funding("BTCUSDT", funding_frame(full_t, rate=1e-4))
    assert not _funding_path("BTCUSDT").with_suffix(".tmp").exists()

    win_t = np.arange(T0 + 30 * D, T0 + 60 * D, 8 * H)
    _save_funding("BTCUSDT", funding_frame(win_t, rate=9e-4))
    after = _load_funding("BTCUSDT")

    assert int(after["funding_time"].min()) == int(full_t[0])
    assert int(after["funding_time"].max()) == int(full_t[-1])
    assert len(after) == len(full_t)

    inside = after[after["funding_time"].isin(win_t)]
    outside = after[~after["funding_time"].isin(win_t)]
    assert len(inside) == len(win_t)
    assert (inside["funding_rate"] == 9e-4).all()
    assert (outside["funding_rate"] == 1e-4).all()
