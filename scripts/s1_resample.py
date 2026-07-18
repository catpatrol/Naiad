"""S-1 data prep — build 30m (from 15m) and 1d (from 1h) locally (§3.6).

Deterministic OHLCV aggregation over the census estate's parquet caches,
OFFLINE (no network). Output goes to research_outputs/s1/resampled/ —
deliberately NOT into the census-verified estate cache, so the estate stays
exactly as V1 certified it; the s1 instrumentation loads these files
directly.

F-RESAMPLE invariants, asserted per output file:
  - bucket child-count == ratio (2 for 30m/15m, 24 for 1d/1h) on every
    interior bucket; boundary buckets reported, never dropped silently
  - open == first child open, close == last child close,
    high == max(child highs), low == min(child lows), volume == sum
  - span: output covers exactly the source span (same first bucket, same
    last bucket)
  - determinism: the aggregation runs twice; output parquet bytes hashed
    twice and identical

Usage: python scripts/s1_resample.py
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from engine.data import cache_dir  # noqa: E402

OUT = ROOT / "research_outputs" / "s1" / "resampled"
SYMBOLS = ["BTCUSDT", "ETHUSDT", "JTOUSDT", "NEARUSDT", "SOLUSDT",
           "TAOUSDT", "ZECUSDT"]
SPECS = [("30m", "15m", 1_800_000, 2), ("1d", "1h", 86_400_000, 24)]


def aggregate(src: pd.DataFrame, step_ms: int) -> pd.DataFrame:
    key = src["open_time"].to_numpy(np.int64) // step_ms * step_ms
    g = src.groupby(key, sort=True)
    return pd.DataFrame({
        "open_time": np.asarray(sorted(set(key)), dtype=np.int64),
        "open": g["open"].first().to_numpy(float),
        "high": g["high"].max().to_numpy(float),
        "low": g["low"].min().to_numpy(float),
        "close": g["close"].last().to_numpy(float),
        "volume": g["volume"].sum().to_numpy(float),
    })


def check(src: pd.DataFrame, out: pd.DataFrame, step_ms: int,
          ratio: int) -> dict:
    key = src["open_time"].to_numpy(np.int64) // step_ms * step_ms
    counts = pd.Series(key).value_counts().sort_index()
    interior = counts.iloc[1:-1] if len(counts) > 2 else counts.iloc[0:0]
    bad_children = int((interior != ratio).sum())
    viol = 0
    idx = {t: j for j, t in enumerate(out["open_time"].to_numpy())}
    src_o = src["open"].to_numpy(); src_h = src["high"].to_numpy()
    src_l = src["low"].to_numpy(); src_c = src["close"].to_numpy()
    src_v = src["volume"].to_numpy()
    o = out["open"].to_numpy(); h = out["high"].to_numpy()
    l = out["low"].to_numpy(); c = out["close"].to_numpy()
    v = out["volume"].to_numpy()
    order = np.argsort(key, kind="stable")
    for bucket, grp in pd.Series(np.arange(len(src))[order],
                                 index=key[order]).groupby(level=0):
        rows = grp.to_numpy()
        j = idx[bucket]
        if not (o[j] == src_o[rows[0]] and c[j] == src_c[rows[-1]]
                and h[j] == src_h[rows].max() and l[j] == src_l[rows].min()
                and np.isclose(v[j], src_v[rows].sum(), rtol=0, atol=1e-6)):
            viol += 1
    span_ok = (out["open_time"].iloc[0] == key.min()
               and out["open_time"].iloc[-1] == key.max())
    return {"buckets": len(out), "interior_buckets_wrong_childcount":
            bad_children, "agg_violations": viol, "span_ok": bool(span_ok),
            "boundary_children": [int(counts.iloc[0]), int(counts.iloc[-1])]}


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    klines = cache_dir() / "klines"
    report = {}
    all_ok = True
    for sym in SYMBOLS:
        for tf_out, tf_src, step, ratio in SPECS:
            src = pd.read_parquet(klines / f"{sym}_{tf_src}.parquet")
            src = src.sort_values("open_time").reset_index(drop=True)
            out_path = OUT / f"{sym}_{tf_out}.parquet"
            hashes = []
            for _ in range(2):          # determinism: build twice, hash twice
                out = aggregate(src, step)
                out.to_parquet(out_path, index=False)
                hashes.append(hashlib.sha256(out_path.read_bytes()).hexdigest())
            chk = check(src, out, step, ratio)
            chk["deterministic"] = hashes[0] == hashes[1]
            chk["sha256"] = hashes[0]
            chk["source_rows"] = len(src)
            ok = (chk["deterministic"] and chk["span_ok"]
                  and chk["agg_violations"] == 0
                  and chk["interior_buckets_wrong_childcount"] == 0)
            all_ok &= ok
            report[f"{sym}_{tf_out}"] = chk
            print(f"{sym}_{tf_out}: {'OK' if ok else '*** FAIL ***'} "
                  f"{chk['buckets']} buckets from {len(src)} source rows, "
                  f"boundary children {chk['boundary_children']}, "
                  f"sha {hashes[0][:12]}")
    (OUT / "resample_report.json").write_text(
        json.dumps(report, indent=1, sort_keys=True) + "\n",
        encoding="utf-8", newline="\n")
    print(f"\nF-RESAMPLE prep: {'ALL OK' if all_ok else 'FAILURES'}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
