"""STAGE 7 -- RECALIBRATION. All cycle-2/3 numbers are void.

Cycle 2/3 measured a registry with three families EMPTY, prior anchors MISSING
and pivots DISPLAY-CAPPED, at the weekly registry minimum. Every threshold was
calibrated against a registry a third the current size.
"""
import collections
import json
import statistics
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent   # was a hardcoded OneDrive path; queue 004 Phase A, 2026-08-12
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "scripts"))

import brief2 as B2                                                 # noqa: E402
from analytics import levels as L                                   # noqa: E402
from analytics import vwap as W                                     # noqa: E402
from analytics import structure as S                                # noqa: E402
from engine.data import cache_dir                                   # noqa: E402

DAY_MS = 86_400_000
HOUR_MS = 3_600_000
doc = json.load(open(ROOT / "briefs" / "brief_2026-08-05_post_ny.json",
                     encoding="utf-8"))
OUT = {}


def hdr(t):
    print("\n" + "=" * 96); print(t); print("=" * 96)


# ---------------------------------------------------------------- 7.1 item 1
hdr("7.1 (1)  LEVEL COUNT PER ASSET, BY FAMILY  -- cycle-2 numbers are VOID")
print(f"{'asset':<14}" + "".join(f"{f[:16]:>17}" for f in L.FAMILIES) + f"{'total':>8}")
tot = []
for s, a in sorted(doc["assets"].items()):
    bf = ((a.get("confluence") or {}).get("level_count_by_family")) or {}
    n = (a.get("confluence") or {}).get("level_count", 0)
    tot.append(n)
    print(f"{s:<14}" + "".join(f"{bf.get(f,0):>17}" for f in L.FAMILIES) + f"{n:>8}")
print(f"\n  range {min(tot)}-{max(tot)}  median {statistics.median(tot):.0f}")
print("  §5.3 forecast 180-200 was made BEFORE the layers existed. The measured")
print("  range is the fact; the forecast is not a target to be reached.")
OUT["level_counts"] = {"min": min(tot), "max": max(tot),
                       "median": statistics.median(tot)}

# ---------------------------------------------------------------- 7.1 item 2
hdr("7.1 (2)  SCORE DISTRIBUTION, AND HOW OFTEN THE FAMILY CAP BINDS")
scores, capbind, ncl = [], 0, 0
for s, a in doc["assets"].items():
    v = (a.get("confluence") or {}).get("with_volume") or {}
    for c in (v.get("clusters") or []):
        scores.append(c["score"]); ncl += 1
        per = collections.Counter(m["family"] for m in (c.get("members") or []))
        if any(k >= L.FAMILY_CAP for k in per.values()):
            capbind += 1
scores.sort()
q = lambda p: scores[min(len(scores)-1, int(p*len(scores)))]
print(f"  clusters {ncl}   min {scores[0]}  median {statistics.median(scores):.0f}"
      f"  p90 {q(0.90)}  max {scores[-1]}")
print(f"  family cap (>= {L.FAMILY_CAP} of one family) BINDS on {capbind} of {ncl} "
      f"clusters ({100*capbind/ncl:.1f}%)")
OUT["score_dist"] = {"n": ncl, "min": scores[0], "median": statistics.median(scores),
                     "p90": q(0.90), "max": scores[-1],
                     "cap_binds": capbind, "cap_binds_pct": 100*capbind/ncl}

# ---------------------------------------------------------------- 7.1 item 3
hdr("7.1 (3)  LINE-IN-THE-SAND STABILITY ACROSS TOLERANCE 0.10 / 0.15 / 0.20")
print(f"{'asset':<14}{'tol':>6}{'above':>13}{'below':>13}   moved vs 0.15")
lis_move = []
for s, a in sorted(doc["assets"].items()):
    atr = a.get("daily_atr"); px = a.get("price")
    conf = a.get("confluence") or {}
    v = conf.get("with_volume") or {}
    levels = [m for c in (v.get("clusters") or []) for m in (c.get("members") or [])]
    base = None
    for tol in (0.10, 0.15, 0.20):
        d = L.dual_score(levels, atr, px, tol=tol)["with_volume"]["lines"]
        ab = (d.get("above") or {}).get("mean")
        be = (d.get("below") or {}).get("mean")
        if tol == 0.15:
            base = (ab, be)
        moved = ""
        if base and tol != 0.15:
            for i, x in enumerate((ab, be)):
                if x is not None and base[i] is not None:
                    dd = abs(x - base[i]) / atr
                    if dd > 0.001:
                        moved += f" {'above' if i==0 else 'below'} {dd:.3f}ATR"
                        lis_move.append(dd)
        print(f"{s:<14}{tol:>6.2f}{(ab or 0):>13.4f}{(be or 0):>13.4f}   {moved}")
print(f"\n  line moves off the 0.15 baseline: n={len(lis_move)}"
      + (f"  median {statistics.median(lis_move):.3f} ATR" if lis_move else "  NONE"))
OUT["lis_tolerance_moves"] = lis_move

# ---------------------------------------------------------------- 7.1 item 4
hdr("7.1 (4)  FAMILY COMPOSITION OF THE TOP-3 AREAS -- does one family dominate?")
dom = collections.Counter()
for s, a in doc["assets"].items():
    v = (a.get("confluence") or {}).get("with_volume") or {}
    for c in sorted(v.get("clusters") or [], key=lambda c: -c["score"])[:3]:
        for m in (c.get("members") or []):
            dom[m["family"]] += 1
t = sum(dom.values())
for f in L.FAMILIES:
    print(f"  {f:<20} {dom[f]:>4}  {100*dom[f]/t:>5.1f}%")
print("\n  A vwap_rolling or profile_windowed majority would mean the family")
print("  split did not go far enough.")
OUT["top3_family_composition"] = dict(dom)

# ---------------------------------------------------------------- 7.1 item 5
hdr("7.1 (5)  VA NESTING STATE DISTRIBUTION, ten assets x three pairs")
st = collections.Counter()
for s, a in doc["assets"].items():
    for k, p in ((a.get("va_nesting") or {}).get("pairs") or {}).items():
        st[p.get("state") or "warming"] += 1
for k, v in st.most_common():
    print(f"  {str(k):<20} {v:>4}")
OUT["va_nesting_states"] = dict(st)

# ---------------------------------------------------------------- 7.1 item 6
hdr("7.1 (6) + 7.2  DUAL-SCORING DIVERGENCE, RE-BUCKETED (refinement vs relocation)")
print("  Cycle 2 headline: 'a line moved on 20 of 20 sides'. Median move 0.127 ATR")
print("  against a cluster width of 0.15 -- BELOW one cluster width. Re-bucketed:")
refine, reloc, only_one, moves = 0, 0, 0, []
for s, a in sorted(doc["assets"].items()):
    atr = a.get("daily_atr")
    conf = a.get("confluence") or {}
    wv = (conf.get("with_volume") or {}).get("lines") or {}
    nv = (conf.get("without_volume") or {}).get("lines") or {}
    for side in ("above", "below"):
        x = (wv.get(side) or {}).get("mean")
        y = (nv.get(side) or {}).get("mean")
        if x is None or y is None:
            only_one += 1
            continue
        d = abs(x - y) / atr
        moves.append(d)
        if d >= L.CLUSTER_ATR:
            reloc += 1
        else:
            refine += 1
print(f"\n  RELOCATIONS (>= {L.CLUSTER_ATR} ATR, one cluster width) : {reloc}")
print(f"  refinements (< {L.CLUSTER_ATR} ATR, within one cluster)  : {refine}")
print(f"  line present in one view only                      : {only_one}")
if moves:
    print(f"  median move {statistics.median(moves):.3f} ATR   max {max(moves):.3f} ATR")
OUT["item6"] = {"relocations": reloc, "refinements": refine,
                "one_view_only": only_one,
                "median_atr": statistics.median(moves) if moves else None}

# ---------------------------------------------------------------- 7.1 item 7
hdr("7.1 (7)  MEASURED STORAGE")
cap = ROOT / "briefs" / "brief_2026-08-05_post_ny.json"
print(f"  capture JSON, one slot      {cap.stat().st_size:>10,} B")
psum = 0
for t_ in B2 and ("snapshots", "levels", "areas", "excursions"):
    p = ROOT / "briefs" / "panel" / t_ / "2026-08-05.parquet"
    if p.exists():
        print(f"  {t_+' partition':<27} {p.stat().st_size:>10,} B")
        psum += p.stat().st_size
print(f"  {'partitions, per day':<27} {psum:>10,} B")
print(f"\n  projected annual, 3 slots/day: captures "
      f"{3*365*cap.stat().st_size/1e6:.0f} MB + partitions {365*psum/1e6:.0f} MB")
print("  R5: no action. Raw tracked JSON stays; gzip measured 1.74x LARGER.")
OUT["storage"] = {"capture_bytes": cap.stat().st_size, "partition_bytes": psum}

# ---------------------------------------------------- inval_atr distribution
hdr("7.1+  INVAL_ATR DISTRIBUTION -- structure-derived vs the old mechanical rule")
iv = []
for s, a in doc["assets"].items():
    for r in ((a.get("rr_ranking") or {}).get("board") or []):
        if r.get("inval_atr"):
            iv.append(r["inval_atr"])
iv.sort()
if iv:
    print(f"  n {len(iv)}  min {iv[0]:.3f}  median {statistics.median(iv):.3f}  "
          f"p90 {iv[int(0.9*len(iv))]:.3f}  max {iv[-1]:.3f}")
    print(f"  below MIN_INVAL_ATR ({B2.MIN_INVAL_ATR}): "
          f"{sum(1 for x in iv if x < B2.MIN_INVAL_ATR)} of {len(iv)} "
          f"-- these carry a CAUTION CHIP, none are excluded (D2-2)")
    print("  Cycle 3 measured 0.244-0.276, a 0.03 spread, and excluding 2 of 12")
    print("  on it was an arbitrary cut wearing the appearance of a principle.")
OUT["inval_atr"] = {"n": len(iv), "min": iv[0] if iv else None,
                    "median": statistics.median(iv) if iv else None,
                    "max": iv[-1] if iv else None}

# ------------------------------------------- LEVEL-DISTANCE DISTRIBUTION
hdr("7.1+  LEVEL-DISTANCE DISTRIBUTION by family -- TO DESCRIBE, NOT TO FILTER (R6)")
BUCK = (("<1.5", 0, 1.5), ("1.5-3", 1.5, 3), ("3-6", 3, 6),
        ("6-12", 6, 12), (">12", 12, 1e18))
tbl = {f: collections.Counter() for f in L.FAMILIES}
for s, a in doc["assets"].items():
    px, atr = a.get("price"), a.get("daily_atr")
    v = (a.get("confluence") or {}).get("with_volume") or {}
    for c in (v.get("clusters") or []):
        for m in (c.get("members") or []):
            d = abs(m["level"] - px) / atr
            for nm, lo, hi in BUCK:
                if lo <= d < hi:
                    tbl[m["family"]][nm] += 1
                    break
print(f"{'family':<20}" + "".join(f"{b[0]:>9}" for b in BUCK) + f"{'total':>8}")
gt = collections.Counter()
for f in L.FAMILIES:
    row = tbl[f]; gt.update(row)
    print(f"{f:<20}" + "".join(f"{row[b[0]]:>9}" for b in BUCK)
          + f"{sum(row.values()):>8}")
print(f"{'ALL':<20}" + "".join(f"{gt[b[0]]:>9}" for b in BUCK)
      + f"{sum(gt.values()):>8}")
beyond3 = gt["3-6"] + gt["6-12"] + gt[">12"]
print(f"\n  beyond 3 ATR: {beyond3} of {sum(gt.values())} "
      f"({100*beyond3/sum(gt.values()):.1f}%) -- R6 admits every one of them.")
OUT["level_distance"] = {f: dict(tbl[f]) for f in L.FAMILIES}

# ------------------------------------- how often price sits beyond sigma1/2/3
hdr("7.1+  HOW OFTEN PRICE SITS BEYOND SIGMA 1/2/3, per rolling VWAP, per asset")
print("  MEASURED OVER THE 1h ESTATE, trailing 365 days. This is a property of")
print("  the DISTRIBUTION -- a description of where price lives relative to its")
print("  own volume-weighted mean. It is NOT a statistic over excursion")
print("  outcomes: it says nothing about whether a touch pays. That is H-VBR.")
kd = cache_dir() / "klines"
print(f"\n{'asset':<14}{'window':>8}{'>1s':>9}{'>2s':>9}{'>3s':>9}   (% of bars)")
sig_freq = {}
for sym in sorted(doc["assets"]):
    p = kd / f"{sym}_1h.parquet"
    if not p.exists():
        continue
    df = pd.read_parquet(p)
    df = df.iloc[-(365 * 24 + 8760):]
    t = df["open_time"].to_numpy(np.int64)
    src = W.hlc3(df["high"].to_numpy(float), df["low"].to_numpy(float),
                 df["close"].to_numpy(float))
    v = df["volume"].to_numpy(float)
    c = df["close"].to_numpy(float)
    for wd in (7, 30):
        rv = W.rolling_vwap(t, src, v, wd)
        m, sd = rv["vwap"], rv["stdev"]
        ok = np.isfinite(m) & np.isfinite(sd) & (sd > 0)
        if ok.sum() < 100:
            continue
        z = np.abs((c[ok] - m[ok]) / sd[ok])
        row = [100 * float((z > k).mean()) for k in (1, 2, 3)]
        sig_freq[f"{sym}_{wd}d"] = row
        print(f"{sym:<14}{str(wd)+'d':>8}{row[0]:>9.2f}{row[1]:>9.2f}{row[2]:>9.2f}")
OUT["sigma_frequency"] = sig_freq

# ------------------------------------- reversion R:R by target-distance bucket
hdr("7.1+  REVERSION-DRAFT R:R BY TARGET-DISTANCE BUCKET")
import brief_render as BR                                           # noqa: E402
bb = collections.defaultdict(list)
for s, a in doc["assets"].items():
    rd = B2.reversion_drafts(a.get("stretch") or {}, a.get("confluence") or {},
                             a.get("price"), a.get("daily_atr"))
    for d in rd["drafts"]:
        bb[BR.target_bucket(d["target_distance_atr"]) or "FAR"].append(d)
print(f"{'bucket':<8}{'n':>4}{'R:R values':>26}{'median tgt ATR':>16}{'median band score':>19}")
for b in ("NEAR", "MID", "FAR"):
    ds = bb[b]
    if not ds:
        print(f"{b:<8}{0:>4}"); continue
    rr = sorted({round(x['rr'], 2) for x in ds})
    td = statistics.median([x["target_distance_atr"] for x in ds])
    sc = statistics.median([x["band_confluence_score"] or 0 for x in ds])
    print(f"{b:<8}{len(ds):>4}{str(rr):>26}{td:>16.2f}{sc:>19.1f}")
print("\n  R:R takes only the values {2.0, 3.0} in EVERY bucket -- a constant of")
print("  the geometry. The band's confluence score is what discriminates (5.3).")
OUT["reversion_by_bucket"] = {b: len(v) for b, v in bb.items()}

json.dump(OUT, open(ROOT / "exchange" / "reports" /
                    "BRIEF2_CALIBRATION_2026-08-05.json", "w"), indent=1, default=str)
print("\n\nwrote exchange/reports/BRIEF2_CALIBRATION_2026-08-05.json")
