"""ITEM 4 -- EXCURSION EPISODES. Reviewer correction to C4 §5.3.

4.1 The C4 comparison of time-fractions to a normal distribution is a CATEGORY
    ERROR. Price relative to a VWAP is a PERSISTENT, AUTOCORRELATED series, not
    a set of independent draws. A ~50% time-fraction reflects trending
    persistence, not tail fatness.
4.2 The decision-relevant unit is the EPISODE, not the bar.
4.3 DESCRIPTIVE ONLY. Counting episodes is market-state observation; what
    fraction REVERT, or any hit rate or expectancy, is CENSUS work under G-7.
"""
import json
import statistics
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent   # was a hardcoded OneDrive path; queue 004 Phase A, 2026-08-12
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "scripts"))

import brief_panel as BP                                            # noqa: E402
from analytics import vwap as W                                     # noqa: E402
from engine.data import cache_dir                                   # noqa: E402

WINDOWS = (7, 30)
CAL_BARS = 365 * 24


def episodes(z, k):
    """ONE implementation, imported from brief_panel so the firewall fixture
    that scans it is scanning the code this calibration actually ran."""
    return [(e["length_bars"], e["max_abs_z"]) for e in BP.episode_runs(z, k)]


kd = cache_dir() / "klines"
syms = sorted({p.name.split("_")[0] for p in kd.glob("*_1h.parquet")})

print("=" * 104)
print("ITEM 4.1 -- THE C4 COMPARISON IS WITHDRAWN")
print("=" * 104)
print("""
  C4 §5.3 reported time beyond +/-1s ~50%, +/-2s ~9.5%, +/-3s ~0.4% and compared
  them to a normal distribution's 31.7 / 4.6 / 0.27, concluding the tails were
  "roughly double" and a "2 sigma is rare" prior was "wrong by a factor of two".

  THAT COMPARISON IS A CATEGORY ERROR. The normal figures describe INDEPENDENT
  DRAWS. Price relative to a VWAP is a PERSISTENT, AUTOCORRELATED series: once
  price is beyond a band it TENDS TO STAY there, because trending is exactly
  what carries it there. A ~50% time-fraction is a statement about persistence,
  not about tail fatness, and no conclusion about tails follows from it.

  The C4 sentence must be removed from the report. What follows replaces it.
""")

print("=" * 104)
print("ITEM 4.2 -- EPISODES: contiguous runs beyond the band")
print("=" * 104)
print(f"\n  calibration window: trailing {CAL_BARS} 1h bars (365 days)\n")
print(f"{'asset':<14}{'VWAP':>7}{'k':>3}{'episodes':>10}{'med len':>9}"
      f"{'p90 len':>9}{'med max|z|':>12}{'bars beyond':>13}{'time %':>8}")
print("-" * 104)

rows = []
OUT = {}
for sym in syms:
    p = kd / f"{sym}_1h.parquet"
    df = pd.read_parquet(p)
    df = df.iloc[-(CAL_BARS + 8760):]
    t = df["open_time"].to_numpy(np.int64)
    src = W.hlc3(df["high"].to_numpy(float), df["low"].to_numpy(float),
                 df["close"].to_numpy(float))
    v = df["volume"].to_numpy(float)
    c = df["close"].to_numpy(float)
    for wd in WINDOWS:
        rv = W.rolling_vwap(t, src, v, wd)
        m, sd = rv["vwap"], rv["stdev"]
        ok = np.isfinite(m) & np.isfinite(sd) & (sd > 0)
        if ok.sum() < 1000:
            continue
        z = (c[ok] - m[ok]) / sd[ok]
        z = z[-CAL_BARS:] if len(z) > CAL_BARS else z
        for k in (2, 3):
            eps = episodes(z, k)
            nbeyond = int((np.abs(z) >= k).sum())
            if not eps:
                print(f"{sym:<14}{str(wd)+'d':>7}{k:>3}{0:>10}"
                      f"{'-':>9}{'-':>9}{'-':>12}{nbeyond:>13}"
                      f"{100*nbeyond/len(z):>8.2f}")
                continue
            lens = sorted(e[0] for e in eps)
            maxz = sorted(e[1] for e in eps)
            med = statistics.median(lens)
            p90 = lens[min(len(lens) - 1, int(0.90 * len(lens)))]
            medz = statistics.median(maxz)
            print(f"{sym:<14}{str(wd)+'d':>7}{k:>3}{len(eps):>10}{med:>9.1f}"
                  f"{p90:>9}{medz:>12.3f}{nbeyond:>13}{100*nbeyond/len(z):>8.2f}")
            rows.append(dict(asset=sym, window=f"{wd}d", k=k, episodes=len(eps),
                             median_len=med, p90_len=p90, median_max_z=medz,
                             bars_beyond=nbeyond, time_pct=100*nbeyond/len(z)))
OUT["episodes"] = rows

print()
print("=" * 104)
print("ITEM 4.4 -- WHAT THIS DOES TO H-VBR's DEFLATION GAUGE")
print("=" * 104)
for k in (2, 3):
    sub = [r for r in rows if r["k"] == k]
    if not sub:
        continue
    tot = sum(r["episodes"] for r in sub)
    tpct = statistics.median([r["time_pct"] for r in sub])
    mlen = statistics.median([r["median_len"] for r in sub])
    print(f"\n  sigma{k}:  {tot} episodes across {len(sub)} asset-windows "
          f"in a YEAR")
    print(f"           median time beyond = {tpct:.2f}% of bars")
    print(f"           median episode length = {mlen:.1f} bars")
    print(f"           => per asset-window, ~{tot/len(sub):.1f} episodes/year")
print("""
  THE POINT. A 9.5%-of-bars figure sounds like abundant opportunity. Counted as
  EPISODES it is a modest number of events per instrument per year, and each is
  ONE decision, not N independent ones. H-VBR's baseline must therefore be
  per-EPISODE, and its usable sample is far smaller than the bar fraction
  implies -- which raises, not lowers, the evidential bar the hypothesis must
  clear.

  FIREWALL UNCHANGED. Counting episodes and measuring their length is
  market-state observation and is OPS. What fraction of them REVERT to the mean,
  any hit rate, any expectancy -- that is H-VBR, census work under G-7, routed
  to APOLLO. Nothing above computes it.
""")

json.dump(OUT, open(ROOT / "exchange" / "reports" /
                    "EXCURSION_EPISODES_2026-08-06.json", "w"),
          indent=1, default=str)
print("wrote exchange/reports/EXCURSION_EPISODES_2026-08-06.json")
