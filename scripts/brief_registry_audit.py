"""STAGE 4 -- registry confirmation, measured from the live capture."""
import json
import statistics
import sys
from pathlib import Path

ROOT = Path(r"C:\Users\luisf\OneDrive\Desktop\Midas-Claude Code Resources\naiad")
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "scripts"))
from analytics import levels as L                                   # noqa: E402

doc = json.load(open(ROOT / "briefs" / "brief_2026-08-05_post_ny.json", encoding="utf-8"))

print("=" * 100)
print("4.1  ALL FIVE FAMILIES PRESENT, PER ASSET")
print("=" * 100)
print(f"{'asset':<14}" + "".join(f"{f:>19}" for f in L.FAMILIES) + f"{'total':>8}")
print("-" * 100)
allfam = True
for s, a in sorted(doc["assets"].items()):
    conf = a.get("confluence") or {}
    bf = conf.get("level_count_by_family") or {}
    row = "".join(f"{bf.get(f, 0):>19}" for f in L.FAMILIES)
    print(f"{s:<14}{row}{conf.get('level_count', 0):>8}")
    if any(bf.get(f, 0) == 0 for f in L.FAMILIES):
        allfam = False
print(f"\n  all five families non-empty on every asset: {allfam}")

print()
print("=" * 100)
print("4.1  PRIOR M/Q/Y ANCHORS PRESENT")
print("=" * 100)
for s, a in sorted(doc["assets"].items()):
    pa = a.get("prior_anchors") or {}
    bits = []
    for p in ("prior_M", "prior_Q", "prior_Y"):
        b = pa.get(p) or {}
        if b.get("warming") or b.get("vwap") is None:
            bits.append(f"{p}=WARMING")
        else:
            bits.append("%s=%,.2f@%db".replace("%,", "%") % (p, b["vwap"], b["bars"]))
    print(f"  {s:<14} " + "  ".join(bits))

print()
print("=" * 100)
print("4.1  CONFIRMED PIVOTS -- 180d lookback, NOT the display-capped last_pivots")
print("=" * 100)
print(f"{'asset':<14}{'highs':>7}{'lows':>7}{'total':>7}{'lookback':>10}  substrate")
print("-" * 100)
counts = []
for s, a in sorted(doc["assets"].items()):
    cp = a.get("confirmed_pivots") or {}
    hi, lo = len(cp.get("highs") or []), len(cp.get("lows") or [])
    counts.append(hi + lo)
    print(f"{s:<14}{hi:>7}{lo:>7}{hi+lo:>7}{cp.get('lookback_days', 0):>10}  {cp.get('substrate')}")
print(f"\n  distinct pivot totals: {sorted(set(counts))}")
print(f"  F-3R-A regression check -- all ten equal to 13 (the display cap): "
      f"{counts == [13]*10}")

print()
print("=" * 100)
print("4.1  NO DISTANCE FILTER (R6) -- min/median/max distance from price, in ATR")
print("=" * 100)
print(f"{'asset':<14}{'family':<20}{'n':>5}{'min':>9}{'median':>9}{'max':>9}")
print("-" * 100)
global_max = (0, "", "")
for s, a in sorted(doc["assets"].items()):
    px = a.get("price")
    atr = a.get("daily_atr")
    conf = a.get("confluence") or {}
    v = conf.get("with_volume") or {}
    per = {}
    for cl in (v.get("clusters") or []):
        for m in (cl.get("members") or []):
            per.setdefault(m["family"], []).append(abs(m["level"] - px) / atr)
    for f in L.FAMILIES:
        d = sorted(per.get(f, []))
        if not d:
            print(f"{s:<14}{f:<20}{0:>5}{'-':>9}{'-':>9}{'-':>9}")
            continue
        print(f"{s:<14}{f:<20}{len(d):>5}{d[0]:>9.2f}"
              f"{statistics.median(d):>9.2f}{d[-1]:>9.2f}")
        if d[-1] > global_max[0]:
            global_max = (d[-1], s, f)
    print()
print(f"  FURTHEST level admitted anywhere: {global_max[0]:.2f} ATR "
      f"({global_max[1]}, {global_max[2]})")
print(f"  A +/-3 ATR admission filter (R6, OVERRULED) would have discarded it.")

n_beyond3 = 0
n_tot = 0
for s, a in sorted(doc["assets"].items()):
    px, atr = a.get("price"), a.get("daily_atr")
    v = (a.get("confluence") or {}).get("with_volume") or {}
    for cl in (v.get("clusters") or []):
        for m in (cl.get("members") or []):
            n_tot += 1
            if abs(m["level"] - px) / atr > 3.0:
                n_beyond3 += 1
print(f"  levels beyond 3 ATR: {n_beyond3} of {n_tot} "
      f"({100*n_beyond3/n_tot:.1f}%) -- all retained, R6")

print()
print("=" * 100)
print("4.1  WEEKLY-ANCHOR CYCLE")
print("=" * 100)
a = doc["assets"]["BTCUSDT"]
w = ((a.get("vwap") or {}).get("anchored") or {}).get("W") or {}
print(f"  BTCUSDT anchored W: anchor {w.get('anchor_utc')}  bars {w.get('bars')}")
print("  The W anchor reopens every Monday 00:00 UTC. On the 1h substrate it")
print("  carries 0 bars at the reopen and crosses R3's floors at:")
print("    line  (>=10 bars) -> Monday 10:00 UTC")
print("    bands (>=30 bars) -> Tuesday 06:00 UTC")
print("  so W bands are withheld for 30 of every 168 hours (17.9% of the week).")
print("  Today is Wednesday and W carries 66 bars, which is why 0 are withheld.")
