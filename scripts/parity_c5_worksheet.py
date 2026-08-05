"""ARGUS cycle 5 item 2 -- ANCHORED-BAND PARITY on the 1h substrate.

The last unverified quantity in the VWAP family. Two operator readings,
BINANCE:BTCUSDT.P, 1H chart, hlc3, StdDev bands 1/2/3, both CLOSED bars.

NO pass/fail and NO tolerance. This COMPUTES; the reviewer judges.
"""
import sys
from pathlib import Path

ROOT = Path(r"C:\Users\luisf\OneDrive\Desktop\Midas-Claude Code Resources\naiad")
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "scripts"))

import numpy as np                                                  # noqa: E402
import pandas as pd                                                 # noqa: E402
import parity_check as PC                                           # noqa: E402
from engine.data import cache_dir                                   # noqa: E402

SYM = "BTCUSDT"
LEVELS = ("vwap", "+1s", "-1s", "+2s", "-2s", "+3s", "-3s")

CAPTURES = {
    "A": {
        "bar": "2026-07-26T20:00Z",
        "raw": dict(open=64665.6, high=64676.2, low=64606.3, close=64621.3,
                    volume=748.27),
        "W": {"vwap": 65190.8, "+1s": 65989.3, "-1s": 64392.3,
              "+2s": 66787.7, "-2s": 63593.9, "+3s": 67586.2, "-3s": 62795.4},
        "M": {"vwap": 63334.0, "+1s": 65064.0, "-1s": 61604.1,
              "+2s": 66794.0, "-2s": 59874.1, "+3s": 68524.0, "-3s": 58144.1},
        "Q": {"vwap": 63334.0, "+1s": 65064.0, "-1s": 61604.1,
              "+2s": 66794.0, "-2s": 59874.1, "+3s": 68524.0, "-3s": 58144.1},
        "implied_sigma": {"W": 798.47, "M": 1729.95, "Q": 1729.95},
    },
    "B": {
        "bar": "2026-08-02T04:00Z",
        "raw": dict(open=63436.8, high=63600.0, low=63436.7, close=63557.1,
                    volume=3010.0),
        "W": {"vwap": 63949.7, "+1s": 64704.2, "-1s": 63195.3,
              "+2s": 65458.7, "-2s": 62440.8, "+3s": 66213.1, "-3s": 61686.4},
        "M": {"vwap": 62926.1, "+1s": 63239.5, "-1s": 62612.7,
              "+2s": 63552.8, "-2s": 62299.3, "+3s": 63866.2, "-3s": 61985.9},
        "Q": {"vwap": 63461.8, "+1s": 65070.4, "-1s": 61853.2,
              "+2s": 66679.1, "-2s": 60244.6, "+3s": 68287.7, "-3s": 58635.9},
        "implied_sigma": {"W": 754.45, "M": 313.37, "Q": 1608.63},
    },
}

print("=" * 100)
print("ITEM 2.1 -- RAW BAR CHECK, both candles, BEFORE any indicator")
print("=" * 100)
df = pd.read_parquet(cache_dir() / "klines" / f"{SYM}_1h.parquet")
df["dt"] = pd.to_datetime(df["open_time"], unit="ms", utc=True)
raw_ok = True
for tag, cap in CAPTURES.items():
    key = cap["bar"].replace("T", " ").replace("Z", "+00:00")
    r = df[df["dt"] == key]
    print(f"\n({tag})  {cap['bar']}")
    if not len(r):
        print("   *** BAR ABSENT FROM THE ESTATE ***")
        raw_ok = False
        continue
    r = r.iloc[0]
    print(f"   {'field':<8}{'ours':>14}{'operator':>14}{'delta':>12}")
    for f in ("open", "high", "low", "close", "volume"):
        d = float(r[f]) - cap["raw"][f]
        note = ""
        if f == "volume":
            note = "   (3 s.f. on the chart)"
        elif abs(d) > 1e-9:
            raw_ok = False
        print(f"   {f:<8}{float(r[f]):>14.4f}{cap['raw'][f]:>14.2f}{d:>+12.4f}{note}")
print(f"\n  ALL FOUR PRICES MATCH ON BOTH BARS: {raw_ok}")

all_rows = []
worst_overall = 0.0

for tag, cap in CAPTURES.items():
    print()
    print("=" * 100)
    print(f"ITEM 2.2 -- CAPTURE ({tag})   1H / hlc3 / bar {cap['bar']}")
    print("=" * 100)
    for per in ("W", "M", "Q"):
        row = PC.evaluate(SYM, "1h", cap["bar"], "avwap", per)
        e = row["extra"]
        ours = {"vwap": row["value"]}
        for k in (1, 2, 3):
            ours[f"+{k}s"] = e[f"+{k}s"]
            ours[f"-{k}s"] = e[f"-{k}s"]
        op = cap[per]

        print(f"\n--- VWAP {({'W':'Week','M':'Month','Q':'Quarter'})[per]} "
              f"--- anchor {e['anchor_utc']}  first bar {e['anchor_bar_utc']}  "
              f"bars {e['bars_since_anchor']}")
        print(f"    evaluated {row['evaluated_candle_utc']}  "
              f"exact={row['exact_candle_match']}  substrate={row['substrate']}")
        mat = e["maturity"]
        if not mat["band_ok"]:
            print(f"    *** THIN SAMPLE: {mat['bars']} bars < "
                  f"{mat['band_min_bars']}-bar BAND floor (R3) ***")
        print(f"    {'level':<7}{'ours (full)':>18}{'rounded':>11}"
              f"{'operator':>11}{'delta':>11}{'bps':>10}")
        worst = 0.0
        for k in LEVELS:
            o, p = ours[k], op[k]
            d = o - p
            worst = max(worst, abs(d))
            print(f"    {k:<7}{o:>18.6f}{round(o,1):>11.1f}{p:>11.1f}"
                  f"{d:>+11.4f}{1e4*d/p:>+10.4f}")
        worst_overall = max(worst_overall, worst)
        print(f"    worst |delta| : {worst:.4f}")

        # ---- 2.3 symmetry + implied sigma
        v, s = ours["vwap"], e["sigma"]
        sym_ok = True
        for k in (1, 2, 3):
            up, dn = ours[f"+{k}s"], ours[f"-{k}s"]
            mid_err = abs((up + dn) / 2.0 - v)
            mult_err = abs((up - dn) / 2.0 - k * s)
            if mid_err > 1e-9 or mult_err > 1e-9:
                sym_ok = False
        imp = cap["implied_sigma"][per]
        print(f"    symmetry: exactly symmetric at exact integer multiples "
              f"= {sym_ok}")
        print(f"    sigma ours {s:.4f}  vs reviewer-implied {imp}  "
              f"delta {s-imp:+.4f} ({1e4*(s-imp)/imp:+.2f} bps)")
        all_rows.append((tag, per, e["bars_since_anchor"], v, s, worst, sym_ok,
                         mat["band_ok"]))

print()
print("=" * 100)
print("SUMMARY -- 42 values (2 captures x 3 anchors x 7 levels)")
print("=" * 100)
print(f"{'cap':<5}{'anchor':<8}{'bars':>6}{'our vwap':>16}{'our sigma':>13}"
      f"{'worst |d|':>11}{'symmetric':>11}{'R3 band_ok':>12}")
for t, p, b, v, s, w, sy, bo in all_rows:
    print(f"{t:<5}{p:<8}{b:>6}{v:>16.4f}{s:>13.4f}{w:>11.4f}{str(sy):>11}"
          f"{str(bo):>12}")
print(f"\nWORST ABSOLUTE DELTA ACROSS ALL 42 VALUES: {worst_overall:.4f}")
print("\nNO pass/fail asserted. The reviewer judges what counts as a match.")

# ---------------------------------------------------------------- ITEM 3.1
print()
print("=" * 100)
print("ITEM 3.1 -- G7 ANCHOR DEGENERACY, capture (A): Month and Quarter")
print("=" * 100)
a_m = PC.evaluate(SYM, "1h", CAPTURES["A"]["bar"], "avwap", "M")
a_q = PC.evaluate(SYM, "1h", CAPTURES["A"]["bar"], "avwap", "Q")
print(f"  Month   anchor {a_m['extra']['anchor_utc']}  bars {a_m['extra']['bars_since_anchor']}")
print(f"  Quarter anchor {a_q['extra']['anchor_utc']}  bars {a_q['extra']['bars_since_anchor']}")
print(f"  July opens Q3, so both anchor at 2026-07-01 -- the SAME anchor bar.")
ident = True
print(f"\n  {'level':<7}{'Month':>18}{'Quarter':>18}{'identical':>11}")
for k in LEVELS:
    mv = a_m["value"] if k == "vwap" else a_m["extra"][k]
    qv = a_q["value"] if k == "vwap" else a_q["extra"][k]
    same = (mv == qv)
    ident &= same
    print(f"  {k:<7}{mv:>18.6f}{qv:>18.6f}{str(same):>11}")
print(f"\n  ALL SEVEN LEVELS BYTE-IDENTICAL: {ident}")
print(f"  sigma Month {a_m['extra']['sigma']:.6f}  sigma Quarter "
      f"{a_q['extra']['sigma']:.6f}  identical: "
      f"{a_m['extra']['sigma'] == a_q['extra']['sigma']}")

# ---------------------------------------------------------------- ITEM 3.2
print()
print("=" * 100)
print("ITEM 3.2 -- MATURITY FLOOR, REAL CASE: capture (B) Month anchor")
print("=" * 100)
b_w = PC.evaluate(SYM, "1h", CAPTURES["B"]["bar"], "avwap", "W")
b_m = PC.evaluate(SYM, "1h", CAPTURES["B"]["bar"], "avwap", "M")
b_q = PC.evaluate(SYM, "1h", CAPTURES["B"]["bar"], "avwap", "Q")
atr_d = 1628.44005908          # BTC daily ATR, measured 2026-08-05
print(f"  Month anchor {b_m['extra']['anchor_utc']}  ->  bar "
      f"{CAPTURES['B']['bar']}")
print(f"  EXACT BAR COUNT: {b_m['extra']['bars_since_anchor']}")
mm = b_m["extra"]["maturity"]
print(f"  R3 floors: line >= {mm['line_min_bars']}, bands >= {mm['band_min_bars']}")
print(f"  line_ok={mm['line_ok']}  band_ok={mm['band_ok']}  "
      f"thin_sample={mm['thin_sample']}")
print(f"  -> the LINE prints with a thin_sample chip; the SIX band levels are "
      f"WITHHELD from the registry")
print(f"\n  SCALE LADDER IN SIGMA-ATR (daily ATR {atr_d:,.2f}):")
print(f"    {'anchor':<9}{'bars':>6}{'sigma':>12}{'sigma in ATR':>15}")
for nm, r in (("Week", b_w), ("Month", b_m), ("Quarter", b_q)):
    s = r["extra"]["sigma"]
    print(f"    {nm:<9}{r['extra']['bars_since_anchor']:>6}{s:>12.4f}"
          f"{s/atr_d:>15.4f}")
sw, sm = b_w["extra"]["sigma"], b_m["extra"]["sigma"]
print(f"\n  REVIEWER NOTE VERIFIED: sigma_month {sm:.2f} vs sigma_week {sw:.2f}")
print(f"    ratio month/week = {sm/sw:.4f}  -- month is "
      f"{'LESS THAN HALF' if sm < sw/2 else 'NOT less than half'} the week")
print(f"    The MONTHLY band therefore sits INSIDE the WEEKLY band:")
print(f"      week  1s envelope  [{b_w['extra']['-1s']:,.2f} , {b_w['extra']['+1s']:,.2f}]")
print(f"      month 1s envelope  [{b_m['extra']['-1s']:,.2f} , {b_m['extra']['+1s']:,.2f}]")
print(f"    STRUCTURALLY BACKWARDS -- a longer lookback must not disperse less "
      f"than a shorter one.")
print(f"    Cause is purely IMMATURITY: {mm['bars']} bars of August against a "
      f"full week of history.")
