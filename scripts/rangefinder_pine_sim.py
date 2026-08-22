#!/usr/bin/env python
"""SS12-RangeFinder v1 — the PINE-PARITY SIMULATOR (F-RF-8's engine).

A faithful python port of pine/SS12_RangeFinder_v1.pine's bar loop,
maintained BESIDE the pine: any semantic edit to the pine must land here
too, and F-RF-8 will go red if either drifts from the twin's chapters.
Lineage: written by the RF-2 pre-publish review lens that caught the v1
seed-law BLOCKER, validated to reproduce the twin EXACTLY in both modes
(body 71.19% / 5 chapters; wick 64.05% / 5 chapters) — then adopted.

Run: ~/venvs/naiad/bin/python scripts/rangefinder_pine_sim.py
"""
import sys, math
sys.path.insert(0, "/Users/luis/Naiad")
sys.path.insert(0, "/Users/luis/Naiad/scripts")
import numpy as np
import rangefinder_twin as RF
from engine import indicators as ind

ATR_LEN = 14


def run_pine_repaired(boundaryMode="body", legMin=0.5, revMin=1.75, touchEps=0.60,
                      devRet=7, brkN=8, brkMargin=1.5, tape=None):
    d = RF.daily_bars() if tape is None else tape
    o = d["o"].to_numpy(float); h = d["h"].to_numpy(float)
    l = d["l"].to_numpy(float); c = d["c"].to_numpy(float)
    n = len(d)
    atr = ind.atr(h, l, c, ATR_LEN)
    NA = float("nan")
    def na(x): return x is None or (isinstance(x, float) and math.isnan(x))
    zdir = 0; extBar = None; extPx = NA; extLo = NA
    extBodyHi = NA; extBodyLo = NA
    lastPivPx = NA; lastPivBody = NA; lastPivDir = 0
    prevPivPx = NA; prevPivBody = NA; prevPivBar = None; lastPivBar = None
    nPivots = 0
    rTop = NA; rBot = NA; devTopExt = NA; devBotExt = NA
    rP0Bar = None; rState = "NONE"; confirmSide = ""
    cands = []          # THE CANDIDATE LIST [twin law; the single slot
                        # diverged on the 4h tape — F-RF-12]
    pivs = []           # (wickBar, px, dir) — terminal test scans BY WICK
                        # BAR against the floor [twin law verbatim]
    pendSide = 0; pendOpen = None; pendExt = NA; pendCloses = 0
    nConfirmed = 0; nPotential = 0; coveredBars = 0
    expansionFloorBar = -1
    ranges = []; cur = None; seeds = 0; inval = 0; hard = []
    for i in range(n):
        open_, high, low, close = o[i], h[i], l[i], c[i]
        if i < ATR_LEN:      # twin parity: bar 14 IS processed [F-RF-12
                             # off-by-one, chapter-moving on 4h]
            if na(extPx) or high >= extPx:
                extPx = high; extBar = i; extLo = low
                extBodyHi = max(open_, close)
        if i >= ATR_LEN and not na(atr[i]):
            a = atr[i]
            sealedNow = False                       # R1
            if zdir == 0:
                if high - extLo >= revMin * a and extLo <= low:
                    zdir = 1; extPx = high; extBar = i; extBodyHi = max(open_, close)
                elif extPx - low >= revMin * a:
                    zdir = -1
                    prevPivPx = lastPivPx; prevPivBody = lastPivBody; prevPivBar = lastPivBar
                    lastPivPx = extPx; lastPivBody = extBodyHi; lastPivDir = 1; lastPivBar = extBar
                    nPivots += 1; sealedNow = True
                    pivs.append((lastPivBar, lastPivPx, 1))
                    extPx = low; extBar = i; extBodyLo = min(open_, close)
                elif high > extPx:
                    extPx = high; extBar = i; extLo = low; extBodyHi = max(open_, close)
            elif zdir == 1:
                if high > extPx:
                    extPx = high; extBar = i; extBodyHi = max(open_, close)
                elif extPx - low >= revMin * a and (na(lastPivPx) or abs(extPx - lastPivPx) >= legMin * a):
                    prevPivPx = lastPivPx; prevPivBody = lastPivBody; prevPivBar = lastPivBar
                    lastPivPx = extPx; lastPivBody = extBodyHi; lastPivDir = 1; lastPivBar = extBar
                    nPivots += 1; sealedNow = True
                    pivs.append((lastPivBar, lastPivPx, 1))
                    zdir = -1; extPx = low; extBar = i; extBodyLo = min(open_, close)
            else:
                if low < extPx:
                    extPx = low; extBar = i; extBodyLo = min(open_, close)
                elif high - extPx >= revMin * a and (na(lastPivPx) or abs(extPx - lastPivPx) >= legMin * a):
                    prevPivPx = lastPivPx; prevPivBody = lastPivBody; prevPivBar = lastPivBar
                    lastPivPx = extPx; lastPivBody = extBodyLo; lastPivDir = -1; lastPivBar = extBar
                    nPivots += 1; sealedNow = True
                    pivs.append((lastPivBar, lastPivPx, -1))
                    zdir = 1; extPx = high; extBar = i; extBodyHi = max(open_, close)
            # SEED — R1 sealedNow gate; R2 no floor bar-guard; R3 na->true
            if rState != "CONFIRMED" and sealedNow and lastPivDir != 0 and not na(prevPivPx):
                segHi = [px for (b, px, d_) in pivs
                         if b > expansionFloorBar and d_ == 1]
                segLo = [px for (b, px, d_) in pivs
                         if b > expansionFloorBar and d_ == -1]
                bullTerm = (lastPivDir == -1
                            and (not segHi or prevPivPx >= max(segHi))
                            and prevPivPx > lastPivPx)
                bearTerm = (lastPivDir == 1
                            and (not segLo or prevPivPx <= min(segLo))
                            and prevPivPx < lastPivPx)
                bodyM = boundaryMode == "body"
                if bullTerm or bearTerm:
                    if bullTerm:
                        cTop = prevPivBody if bodyM else prevPivPx
                        cBot = lastPivBody if bodyM else lastPivPx
                        cDevT = prevPivPx if (bodyM and prevPivPx > cTop) else NA
                        cDevB = lastPivPx if (bodyM and lastPivPx < cBot) else NA
                        cSide = "top"
                    else:
                        cTop = lastPivBody if bodyM else lastPivPx
                        cBot = prevPivBody if bodyM else prevPivPx
                        cDevT = lastPivPx if (bodyM and lastPivPx > cTop) else NA
                        cDevB = prevPivPx if (bodyM and prevPivPx < cBot) else NA
                        cSide = "bottom"
                    if cTop > cBot:
                        # the CANDIDATE LIST [twin law] — append, never replace
                        cands.append({"top": cTop, "bot": cBot,
                                      "devT": cDevT, "devB": cDevB,
                                      "p0": prevPivBar, "side": cSide})
                        nPotential += 1; seeds += 1
            if rState != "CONFIRMED" and cands:
                # twin order: creation order; invalidate first, first confirm
                # wins the bar and supersedes the rest
                keep = []
                won = None
                for cd in cands:
                    if won is not None:
                        continue          # superseded at confirm below
                    if close > cd["top"] or close < cd["bot"]:
                        nPotential -= 1; inval += 1
                        expansionFloorBar = i    # a lifecycle boundary
                        continue
                    eps = touchEps * a
                    hitTop = cd["side"] == "top" and high >= cd["top"] - eps
                    hitBot = cd["side"] == "bottom" and low <= cd["bot"] + eps
                    if hitTop or hitBot:
                        won = cd
                        continue
                    keep.append(cd)
                if won is not None:
                    rTop, rBot = won["top"], won["bot"]
                    devTopExt, devBotExt = won["devT"], won["devB"]
                    rP0Bar = won["p0"]
                    confirmSide = won["side"]
                    rState = "CONFIRMED"
                    nPotential -= 1
                    nPotential -= len(keep)          # superseded
                    nConfirmed += 1
                    cands = []
                    expansionFloorBar = i        # confirm closes an expansion
                    leftEdge = i if rP0Bar is None else rP0Bar
                    cur = {"conf": i, "top": rTop, "bot": rBot,
                           "left": leftEdge, "die": -1, "ndev": 0,
                           "incept": int(not na(devTopExt))
                                     + int(not na(devBotExt))}
                    ranges.append(cur)
                else:
                    cands = keep
            if rState == "CONFIRMED":
                if pendSide == 0:
                    if close > rTop:
                        pendSide = 1; pendOpen = i; pendExt = high; pendCloses = 1
                    elif close < rBot:
                        pendSide = -1; pendOpen = i; pendExt = low; pendCloses = 1
                else:
                    pendExt = max(pendExt, high) if pendSide == 1 else min(pendExt, low)
                    beyond = close > rTop if pendSide == 1 else close < rBot
                    if beyond:
                        pendCloses += 1
                    else:
                        if i - pendOpen <= devRet:
                            if pendSide == 1:
                                rTop = max(rTop, pendExt)
                                devTopExt = pendExt if na(devTopExt) else max(devTopExt, pendExt)
                            else:
                                rBot = min(rBot, pendExt)
                                devBotExt = pendExt if na(devBotExt) else min(devBotExt, pendExt)
                            cur["top"] = rTop; cur["bot"] = rBot; cur["ndev"] += 1
                            hard.append((i, "top" if pendSide == 1 else "bottom", round(pendExt, 1)))
                        pendSide = 0; pendCloses = 0
                if pendSide != 0:
                    bnd = rTop if pendSide == 1 else rBot
                    dieN = pendCloses >= brkN
                    dieM = (close - bnd >= brkMargin * a) if pendSide == 1 else (bnd - close >= brkMargin * a)
                    if dieN or dieM:
                        cur["die"] = i
                        rState = "NONE"; pendSide = 0; pendCloses = 0
                        expansionFloorBar = i
            covTop = rTop if na(devTopExt) else max(rTop, devTopExt)
            covBot = rBot if na(devBotExt) else min(rBot, devBotExt)
            if rState == "CONFIRMED" and not na(covTop) and close <= covTop and close >= covBot:
                coveredBars += 1
    return {"ranges": ranges, "cov": 100.0 * coveredBars / n, "nPivots": nPivots,
            "nConfirmed": nConfirmed, "seeds": seeds, "inval": inval, "hard": hard}

if __name__ == "__main__":
    for mode in ("body", "wick"):
        r = run_pine_repaired(boundaryMode=mode)
        print(f"=== PINE SIM {mode} ===")
        print(f"pivots={r['nPivots']} confirmed={r['nConfirmed']} "
              f"cov={r['cov']:.2f}% seeds={r['seeds']} inval={r['inval']} "
              f"hardens={len(r['hard'])}")
        for x in r["ranges"]:
            if x.get("conf", -1) >= 0:
                print(f"  conf@{x['conf']} die@{x['die']} left={x['left']} "
                      f"[{x['bot']:.1f} … {x['top']:.1f}] ndev={x['ndev']} "
                      f"incept={x['incept']}")
