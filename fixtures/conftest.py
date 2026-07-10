"""Shared fixture machinery.

Everything here is synthetic and seeded — the F1–F5/F7/F8 suite runs with no
network and no real cache (CI-safe). F6 and the dead-column half of F8
validate committed real-data artifacts (research_outputs/).
"""

import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from engine.cells import INTERVAL_MS, make_cell  # noqa: E402
from engine.signals import SignalEvent, SignalResult  # noqa: E402

BASE_MS = 1_704_067_200_000  # 2024-01-01T00:00:00Z
SYNTH_DAYS = 20
SYNTH_START = "2024-01-15"          # leaves 14 days of warm-up on 1m/1h
SYNTH_END = "2024-01-20"


def synth_1m(seed: int = 7) -> pd.DataFrame:
    """Seeded 1m random walk with drift regimes and volume spikes — enough
    structure to produce governor crosses, zone tags and PRIMEs naturally."""
    rng = np.random.default_rng(seed)
    n = SYNTH_DAYS * 1440
    # drift flips every ~3 days so the 1h 9/89 crosses several times
    seg = 3 * 1440
    drift = np.repeat([1, -1, 1, -1, 1, -1, 1][: (n + seg - 1) // seg],
                      seg)[:n] * 4e-5
    ret = rng.normal(0, 6e-4, n) + drift
    close = 100.0 * np.exp(np.cumsum(ret))
    open_ = np.concatenate(([100.0], close[:-1]))
    spread = np.abs(rng.normal(0, 4e-4, n))
    high = np.maximum(open_, close) * (1 + spread)
    low = np.minimum(open_, close) * (1 - spread)
    vol = np.exp(rng.normal(3, 0.5, n))
    spike = rng.random(n) < 0.002
    vol[spike] *= 8.0
    return pd.DataFrame({
        "open_time": BASE_MS + np.arange(n, dtype=np.int64) * 60_000,
        "open": open_, "high": high, "low": low, "close": close, "volume": vol,
    })


def resample(df1m: pd.DataFrame, interval: str) -> pd.DataFrame:
    step = INTERVAL_MS[interval]
    g = df1m.groupby(df1m["open_time"] // step * step)
    out = pd.DataFrame({
        "open_time": g["open_time"].first().index.astype(np.int64),
        "open": g["open"].first().to_numpy(),
        "high": g["high"].max().to_numpy(),
        "low": g["low"].min().to_numpy(),
        "close": g["close"].last().to_numpy(),
        "volume": g["volume"].sum().to_numpy(),
    })
    return out.reset_index(drop=True)


@pytest.fixture(scope="session")
def synth_cache(tmp_path_factory):
    """A fake NAIAD_CACHE_DIR holding synthetic BTCUSDT klines + funding."""
    cache = tmp_path_factory.mktemp("naiad_cache")
    (cache / "klines").mkdir()
    (cache / "funding").mkdir()
    df1m = synth_1m()
    for iv in INTERVAL_MS:
        resample(df1m, iv).to_parquet(cache / "klines" / f"BTCUSDT_{iv}.parquet",
                                      index=False)
    ft = np.arange(BASE_MS, BASE_MS + SYNTH_DAYS * 86_400_000, 8 * 3_600_000,
                   dtype=np.int64)
    pd.DataFrame({"funding_time": ft,
                  "funding_rate": np.full(len(ft), 1e-4)}) \
        .to_parquet(cache / "funding" / "BTCUSDT.parquet", index=False)
    return cache


@pytest.fixture()
def synth_env(synth_cache, monkeypatch):
    monkeypatch.setenv("NAIAD_CACHE_DIR", str(synth_cache))
    return synth_cache


@pytest.fixture(scope="session")
def synth_cell():
    return make_cell("BTCUSDT", "intraday")   # 1h governor / 1m exec


# ── Hand-built halt scenario (F4/F5): five full-loss rounds in one UTC day ──

def halt_scenario(offset_days: int = 14) -> SignalResult:
    """A minimal, fully hand-controlled SignalResult: one long campaign
    re-armed once (campaign ids 1 then 2), five PRIME signals whose fills all
    stop out at -0.5R gross, all inside one UTC day -> the -2R day breaker
    must trip at the 4th realized loss and block the 5th fill.

    Bars start offset_days after BASE_MS so the scenario sits INSIDE the
    synthetic cache's warmed-up replay window (2024-01-15 on)."""
    n = 400
    step = 60_000
    open_ms = (BASE_MS + offset_days * 86_400_000
               + np.arange(n, dtype=np.int64) * step)
    o = np.full(n, 100.0)
    h = np.full(n, 100.4)
    l = np.full(n, 99.8)
    c = np.full(n, 100.0)
    v = np.full(n, 10.0)
    e9 = np.full(n, 100.0)
    e89 = np.full(n, 99.5)
    e200 = np.full(n, 120.0)   # far above: the XA trail never engages (long)
    atr = np.full(n, 0.4)
    g_atr = np.full(n, 1.0)
    g_e89 = np.full(n, 99.0)
    dir_ = np.zeros(n, dtype=np.int8)
    cc = np.zeros(n, dtype=bool)
    sl = np.full(n, np.nan)
    ss = np.full(n, np.nan)
    zone = np.zeros(n, dtype=np.int8)
    stage = np.ones(n, dtype=np.int8)
    camp = np.zeros(n, dtype=np.int64)
    events: list[SignalEvent] = []

    dir_[2:] = 1
    camp[2:200] = 1
    camp[200:] = 2
    events.append(SignalEvent(2, "REGIME", 1, stage=2, tier="full",
                              arrow_visible=True))
    events.append(SignalEvent(200, "REGIME", 1, stage=2, tier="full",
                              arrow_visible=True))

    # five PRIME signals; each fill (next bar open @100) stops out at 99
    prime_bars = [10, 60, 110, 210, 260]
    for k, b in enumerate(prime_bars):
        rc = k + 1 if b < 200 else k - 2   # rc resets in campaign 2
        is_r1 = b in (10, 210)
        # ratchet: stop 99 from this signal on (never loosened)
        sl[b:] = 99.0
        events.append(SignalEvent(b, "PRIME", 1, grade="A", rc=max(rc, 1),
                                  zone="Z2", retr=0.6, stop=99.0, stage=2,
                                  tier="full", is_r1=is_r1, is_add=not is_r1,
                                  grade_uncapped="A"))
        # price path: fill at b+1 open 100, drop through 99 on bar b+2,
        # then recover so the NEXT add is eligible (no open tranches anyway)
        l[b + 2] = 98.7
        c[b + 2] = 99.2
        c[b + 3] = 100.0

    return SignalResult(
        exec_open_ms=open_ms, o=o, h=h, l=l, c=c, v=v,
        e9x=e9, e89x=e89, e200x=e200, atr_x=atr, g_atr=g_atr, g_e89=g_e89,
        dir=dir_, camp_counter=cc, stop_long=sl, stop_short=ss,
        active_zone=zone, stage=stage, campaign_id=camp, events=events)
