#!/usr/bin/env python
"""ARGUS cycle 4 stage 2 -- both parity readings, one run.

2.1  CONFIRMATION READING   1D chart, hlc3, BTCUSDT.P, candle 2026-08-02
2.2  RULED-SUBSTRATE READING 1H chart, hlc3, BTCUSDT.P, closed bar 2026-08-05T17:00Z

NO pass/fail and NO tolerance: this COMPUTES and reports deltas.  What counts as
a match is the reviewer's call.
"""
import json
import sys
from pathlib import Path

ROOT = Path(r"C:\Users\luisf\OneDrive\Desktop\Midas-Claude Code Resources\naiad")
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import numpy as np                                                  # noqa: E402
import pandas as pd                                                 # noqa: E402
import parity_check as PC                                           # noqa: E402
from engine.data import cache_dir                                   # noqa: E402

SYM = "BTCUSDT"

# ---------------------------------------------------------------- operator's
# 2.1 -- 1D chart, candle 2026-08-02
OP_1D = {
    "avwap_M": {"vwap": 63112.3, "+1s": 63432.2, "-1s": 62792.4,
                "+2s": 63752.0, "-2s": 62472.5, "+3s": 64071.9, "-3s": 62152.6},
    "rvwap_365": {"vwap": 83686.7, "+1s": 102555.3, "-1s": 64818.1,
                  "+2s": 121423.9, "-2s": 45949.5, "+3s": 140292.6, "-3s": 27080.9},
}
# 2.2 -- 1H chart, closed bar 2026-08-05T17:00Z
OP_1H = {
    "rvwap_7": {"vwap": 63737.7, "+1s": 64396.6, "-1s": 63078.8,
                "+2s": 65055.6, "-2s": 62419.9, "+3s": 65714.5, "-3s": 61761.0},
    "rvwap_30": {"vwap": 64026.5, "+1s": 65040.9, "-1s": 63012.2,
                 "+2s": 66055.3, "-2s": 61997.8, "+3s": 67069.7, "-3s": 60983.4},
    "rvwap_90": {"vwap": 66248.8, "+1s": 72537.5, "-1s": 59960.1,
                 "+2s": 78826.3, "-2s": 53671.4, "+3s": 85115.0, "-3s": 47382.7},
    "rvwap_365": {"vwap": 83430.8, "+1s": 102289.4, "-1s": 64572.1,
                  "+2s": 121148.0, "-2s": 45713.5, "+3s": 140006.7, "-3s": 26854.9},
    "avwap_Q": {"vwap": 63486.3},
    "avwap_M": {"vwap": 63602.4},
}
# 2.5 -- reviewer's implied sigmas from the 2.2 screenshots
IMPLIED_SIGMA = {"rvwap_7": 658.9, "rvwap_30": 1014.35,
                 "rvwap_90": 6288.7, "rvwap_365": 18858.65}

# 2.1 raw bar the operator's 1D reading rests on (the anchor's 2nd bar)
OP_BAR_1H = {"open": 64631.8, "high": 64780.0, "low": 64506.3,
             "close": 64733.6, "volume": 4460.0}   # "4.46K", 3 s.f.


def rows(measure, param, tf, candle):
    return PC.evaluate(SYM, tf, candle, measure, param)


def cmp_block(title, ours, op, keys=("vwap", "+1s", "-1s", "+2s", "-2s", "+3s", "-3s")):
    print(f"\n### {title}")
    print(f"{'level':<8}{'ours (full)':>20}{'ours (rounded)':>17}"
          f"{'operator':>13}{'delta':>12}{'bps':>10}")
    print("-" * 80)
    worst = 0.0
    for k in keys:
        if k not in op:
            continue
        o = ours["value"] if k == "vwap" else ours["extra"].get(k)
        if o is None:
            print(f"{k:<8}{'n/a':>20}")
            continue
        p = op[k]
        d = o - p
        b = 1e4 * d / p if p else float("nan")
        worst = max(worst, abs(d))
        print(f"{k:<8}{o:>20.6f}{round(o,1):>17.1f}{p:>13.1f}{d:>+12.4f}{b:>+10.4f}")
    print(f"{'':8}worst absolute delta: {worst:.4f}")
    return worst


def symmetry(ours, name):
    """2.5 -- assert exact symmetry and reproduce the implied sigma."""
    v, s = ours["value"], ours["extra"]["sigma"]
    ok = True
    for k in (1, 2, 3):
        up, dn = ours["extra"][f"+{k}s"], ours["extra"][f"-{k}s"]
        mid = (up + dn) / 2.0
        halfw = (up - dn) / 2.0
        sym = abs(mid - v)
        mult = abs(halfw - k * s)
        if sym > 1e-9 or mult > 1e-9:
            ok = False
        print(f"    sigma{k}: midpoint-vwap={sym:.2e}  halfwidth-{k}*sigma={mult:.2e}")
    print(f"    -> exactly symmetric at exact integer multiples: {ok}")
    if name in IMPLIED_SIGMA:
        imp = IMPLIED_SIGMA[name]
        print(f"    our sigma {s:.4f}  vs reviewer-implied {imp}  "
              f"delta {s-imp:+.4f} ({1e4*(s-imp)/imp:+.2f} bps)")
    return ok


print("=" * 80)
print("STAGE 2.3 -- RAW BAR CHECK, before any indicator")
print("=" * 80)
df = pd.read_parquet(cache_dir() / "klines" / f"{SYM}_1h.parquet")
df["dt"] = pd.to_datetime(df["open_time"], unit="ms", utc=True)
b = df[df["dt"] == "2026-08-05 17:00:00+00:00"]
print("\n1H bar 2026-08-05T17:00Z")
print(f"{'field':<9}{'ours':>14}{'operator':>14}{'delta':>12}")
print("-" * 49)
for f_ in ("open", "high", "low", "close", "volume"):
    o = float(b[f_].iloc[0])
    p = OP_BAR_1H[f_]
    note = "  (operator quoted 4.46K, 3 s.f.)" if f_ == "volume" else ""
    print(f"{f_:<9}{o:>14.4f}{p:>14.2f}{o-p:>+12.4f}{note}")

# 1D bar 2026-08-02, resampled from 1h closed buckets
bars1d, sub1d = PC._load(SYM, "1d")
t1d = np.asarray(bars1d["open_time"], dtype="int64")
i = int(np.flatnonzero(t1d == PC._parse_utc("2026-08-02T00:00Z"))[0])
print(f"\n1D bar 2026-08-02T00:00Z   substrate: {sub1d}")
print(f"  O {bars1d['open'][i]:.1f}  H {bars1d['high'][i]:.1f}  "
      f"L {bars1d['low'][i]:.1f}  C {bars1d['close'][i]:.1f}  "
      f"V {bars1d['volume'][i]:,.3f}")
print("  (operator supplied no raw 1D OHLCV for this candle -- nothing to diff)")

print()
print("=" * 80)
print("STAGE 2.1 -- CONFIRMATION READING   1D / hlc3 / candle 2026-08-02")
print("=" * 80)
am = rows("avwap", "M", "1d", "2026-08-02T00:00Z")
print(f"\nevaluated bar {am['evaluated_candle_utc']}  exact={am['exact_candle_match']}"
      f"  substrate={am['substrate']}")
print(f"anchor {am['extra']['anchor_utc']}  first anchored bar "
      f"{am['extra']['anchor_bar_utc']}  bars={am['extra']['bars_since_anchor']}")
w_am = cmp_block("Anchored Month VWAP", am, OP_1D["avwap_M"])
print("\n  symmetry / sigma:")
symmetry(am, "avwap_M_1d")
print(f"  our sigma = {am['extra']['sigma']:.4f}")
print(f"  reviewer back-solved 320.13; operator's observed band-1 distance 319.9")
s_ = am["extra"]["sigma"]
print(f"    ours vs observed 319.9 : {s_-319.9:+.4f}  ({100*(s_-319.9)/319.9:+.4f}%)")
print(f"    back-solve vs observed : {320.13-319.9:+.4f}  "
      f"({100*(320.13-319.9)/319.9:+.4f}%)")

r365d = rows("rvwap", 365, "1d", "2026-08-02T00:00Z")
w_r365d = cmp_block("RVWAP 365d (1D substrate)", r365d, OP_1D["rvwap_365"])
print("\n  symmetry / sigma:")
symmetry(r365d, "rvwap_365_1d")

print()
print("=" * 80)
print("STAGE 2.2 -- RULED-SUBSTRATE READING   1H / hlc3 / bar 2026-08-05T17:00Z")
print("            THE FIRST PARITY EVER RUN ON THE 1h PATH")
print("=" * 80)
worst_1h = {}
for wd in (7, 30, 90, 365):
    r = rows("rvwap", wd, "1h", "2026-08-05T17:00Z")
    if wd == 7:
        print(f"\nevaluated bar {r['evaluated_candle_utc']}  "
              f"exact={r['exact_candle_match']}  substrate={r['substrate']}  "
              f"last closed {r['last_closed_candle_utc']}")
    w = cmp_block(f"RVWAP {wd}d  (bars in window: "
                  f"{r['extra']['bars_in_window']})", r, OP_1H[f"rvwap_{wd}"])
    worst_1h[f"rvwap_{wd}"] = w
    print("\n  symmetry / sigma (2.5):")
    symmetry(r, f"rvwap_{wd}")

print()
print("=" * 80)
print("STAGE 2.6 -- ANCHORED ON THE 1h SUBSTRATE")
print("=" * 80)
for per in ("M", "Q"):
    a = rows("avwap", per, "1h", "2026-08-05T17:00Z")
    w = cmp_block(f"Anchored {per} VWAP  (bars since anchor: "
                  f"{a['extra']['bars_since_anchor']})", a,
                  OP_1H[f"avwap_{per}"], keys=("vwap",))
    worst_1h[f"avwap_{per}"] = w
    e = a["extra"]
    print(f"    anchor {e['anchor_utc']}  our sigma {e['sigma']:.4f}  "
          f"maturity line_ok={e['maturity']['line_ok']} "
          f"band_ok={e['maturity']['band_ok']}")
    print(f"    our +1s {e['+1s']:.4f}  -1s {e['-1s']:.4f}  "
          f"+2s {e['+2s']:.4f}  -2s {e['-2s']:.4f}  "
          f"+3s {e['+3s']:.4f}  -3s {e['-3s']:.4f}")
    print("    ^ ANCHORED SIGMA ON 1h IS UNVERIFIED -- operator captured no "
          "anchored bands on the 1H chart.")

print()
print("=" * 80)
print("SUMMARY OF WORST ABSOLUTE DELTAS")
print("=" * 80)
print(f"  2.1 anchored Month  1D : {w_am:.4f}")
print(f"  2.1 RVWAP 365       1D : {w_r365d:.4f}")
for k, v in worst_1h.items():
    print(f"  2.2/2.6 {k:<14} 1h : {v:.4f}")
print("\nNO pass/fail asserted. The reviewer judges what counts as a match.")
