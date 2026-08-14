#!/usr/bin/env python3
"""
CENSUS-2B / V-ULT-1 -- STAGE 5, THE FIRST LOOK
==============================================
CLASS: DISPLAY-ONLY / Tier-E exploration.  Selection surface m = 0.
No comparison is promoted, no threshold is swept, no arm is ranked and kept.
Nothing in this file is a finding.  Every table is a count or a quantile over
a FIXED, COMPLETE population, printed with its toll line beside it.

  (a) EVENT-DENSITY MAP   -- where does each ribbon even move?
  (b) EQUIVALENCE TABLE   -- the "one chart, all horizons" card.  F-B6.
  (c) V-ULT OCCUPANCY     -- what VH/UH actually spend their time doing.
  (d) THE ENQUIRY CARD    -- the operator's question, made descriptive.

Called by census2b_program.py --stage 5.  Never run standalone against a
half-built substrate: it reads the artifacts, it does not rebuild them.
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import pandas as pd

import census2b_program as P
from census2b_program import (
    OUT, RIBBONS, FAMILIES, TFS, PANEL, V_ULT, TIER_E_HEADER,
    TOLL_BPS_ROUND_TRIP, CENSUS2A, K_WINDOW, RIBBON_C, STATE_EPS,
    ST_COMPRESS, ST_FLAT, ST_EXPAND, ST_NA,
    OR_BEAR, OR_MIXED, OR_BULL, OR_NA,
    PS_BELOW, PS_INSIDE, PS_ABOVE, PS_NA,
    STATE_NAME, ORIENT_NAME, hr, banner, iso, feasible_lengths,
)

FL = OUT / "firstlook"

# Duration-fixed, exactly as census-2A pinned it: H100 == 100 x 5m.  Fixing the
# DURATION rather than the bar count is what makes a 5m table and a 15m table
# answer the same question (census2a_program.py:83, paste-1 defect 6 fix).
H100_MS = 100 * 300_000
KNOT_SEARCH_CAP = 2000          # bars to look forward from a knot, then give up

TF_MS = {"1m": 60_000, "5m": 300_000, "15m": 900_000, "30m": 1_800_000,
         "1h": 3_600_000, "4h": 14_400_000, "12h": 43_200_000}

_TABLES: dict[str, pd.DataFrame] = {}


def _keep(name: str, df: pd.DataFrame) -> pd.DataFrame:
    _TABLES[name] = df
    return df


def toll_atr(close: np.ndarray, av: np.ndarray, mask: np.ndarray | None = None) -> float:
    """The round-trip toll in ATR units, on the population it is quoted beside.

    The toll is a fraction of PRICE; the ruler is a multiple of ATR.  The
    conversion is population-dependent, so it is measured on the same rows the
    returns are measured on -- never carried over from another table.
    """
    m = np.isfinite(close) & np.isfinite(av) & (av > 0)
    if mask is not None:
        m &= mask
    if not m.any():
        return float("nan")
    return float(np.median((TOLL_BPS_ROUND_TRIP / 10000.0) * close[m] / av[m]))


def q(v: np.ndarray, p: float) -> float:
    v = v[np.isfinite(v)]
    return float(np.quantile(v, p)) if v.size else float("nan")


def joint_vult(orient_vh: np.ndarray, orient_uh: np.ndarray) -> np.ndarray:
    """VH+UH joint orientation -- the operator's conditioning variable.

    bull-fanned  = BOTH ultra ribbons monotone up
    bear-fanned  = BOTH monotone down
    mixed        = anything else (including one warm and one not)
    """
    out = np.full(len(orient_vh), OR_NA, dtype=np.int8)
    warm = (orient_vh != OR_NA) & (orient_uh != OR_NA)
    out[warm] = OR_MIXED
    out[warm & (orient_vh == OR_BULL) & (orient_uh == OR_BULL)] = OR_BULL
    out[warm & (orient_vh == OR_BEAR) & (orient_uh == OR_BEAR)] = OR_BEAR
    return out


# ===========================================================================
# (a) EVENT-DENSITY MAP
# ===========================================================================
def look_a(assets: list[str], tfs: list[str]) -> pd.DataFrame:
    banner("5(a) EVENT-DENSITY MAP -- where does each ribbon even move?")
    print(TIER_E_HEADER)
    print("\ncounts are of CLOSE-CONFIRMED events over the FULL available series "
          "(both eras),\nover a fixed complete population; nothing is selected.\n")
    rows = []
    for sym in assets:
        for tf in tfs:
            p = OUT / "crosses" / sym / f"{tf}.parquet"
            if not p.exists():
                continue
            ev = pd.read_parquet(p, columns=["pair_class", "pair", "family",
                                             "event", "dir", "ts_ms"])
            bars = len(pd.read_parquet(OUT / "emas" / sym / f"{tf}.parquet",
                                       columns=["open_time"]))
            g = ev.groupby(["pair_class", "pair", "family", "event", "dir"],
                           dropna=False, sort=True).size()
            for (pc, pair, fam, evn, d), n in g.items():
                rows.append({"asset": sym, "tf": tf, "pair_class": pc,
                             "pair": pair, "family": fam, "event": evn,
                             "dir": d, "n": int(n), "bars": bars,
                             "per_1k_bars": round(1000.0 * n / bars, 4)})
            del ev
    dm = pd.DataFrame(rows)
    if dm.empty:
        print("  (no cross artifacts found)")
        return dm

    # ---- headline: within-ribbon density per family per tf, panel-summed
    print("WITHIN-RIBBON crosses per 1,000 bars -- panel total, by family x tf")
    print("(a ribbon that never moves at a tf is where that tf stops being its home)")
    sub = dm[dm.pair_class == "within_ribbon"]
    print(f"\n  {'family':7s}" + "".join(f"{t:>10s}" for t in tfs))
    hr()
    for fam in FAMILIES:
        cells = []
        for tf in tfs:
            s = sub[(sub.family == fam) & (sub.tf == tf)]
            if s.empty:
                cells.append(f"{'-':>10s}")
            else:
                cells.append(f"{1000.0 * s.n.sum() / s.bars.max() / 3:10.2f}")
        print(f"  {fam:7s}" + "".join(cells))
    print("\n  (per-pair average: family total / 3 pairs / bars of the cell)")

    # ---- per-direction split, as required on every first-look table
    print("\nPER-DIRECTION SPLIT -- within-ribbon, panel total")
    print(f"  {'family':7s} {'up':>12s} {'down':>12s} {'up share':>10s}")
    hr()
    for fam in FAMILIES:
        s = sub[sub.family == fam]
        u = int(s[s.dir == "up"].n.sum())
        d = int(s[s.dir == "down"].n.sum())
        sh = u / (u + d) if (u + d) else float("nan")
        print(f"  {fam:7s} {u:12,d} {d:12,d} {sh:10.4f}")

    # ---- the V-ULT question this map exists to answer
    print("\nV-ULT DENSITY -- VH and UH within-ribbon crosses, per asset per tf")
    print(f"  {'asset':9s} {'fam':4s}" + "".join(f"{t:>9s}" for t in tfs))
    hr()
    for sym in assets:
        for fam in V_ULT:
            cells = []
            for tf in tfs:
                s = sub[(sub.asset == sym) & (sub.family == fam) & (sub.tf == tf)]
                cells.append(f"{int(s.n.sum()):9,d}" if not s.empty else f"{'-':>9s}")
            print(f"  {sym:9s} {fam:4s}" + "".join(cells))

    # ---- midline + band, so the pared taxonomy is fully accounted for
    print("\nMIDLINE + PRICE<->BAND totals, panel")
    for pc in ("midline", "price_band"):
        s = dm[dm.pair_class == pc]
        if s.empty:
            continue
        print(f"\n  {pc}: {int(s.n.sum()):,} events")
        for (pair, evn), n in s.groupby(["pair", "event"]).n.sum().items():
            print(f"    {pair:14s} {evn:8s} {int(n):12,d}")
    return _keep("5a_event_density", dm)


# ===========================================================================
# (b) EQUIVALENCE TABLE  --  the "one chart, all horizons" card
# ===========================================================================
def look_b(tfs: list[str]) -> pd.DataFrame:
    banner("5(b) EQUIVALENCE TABLE -- EMA N @ tf ~ days of memory ~ nearest HTF EMA")
    print(TIER_E_HEADER)
    print("""
The card the operator asked for.  An EMA's identity is a DURATION, not a
number: EMA(N) on tf T spans N*T of tape.  Two (N, tf) pairs with the same
product are the same object drawn on different axes.  `centre of mass` is
(N-1)/2 bars -- where the weight of the average actually sits.
""")
    rows = []
    for fam, members in RIBBONS.items():
        for L in members:
            for tf in tfs:
                span_ms = L * TF_MS[tf]
                rows.append({
                    "family": fam, "length": L, "tf": tf,
                    "span_ms": span_ms,
                    "memory_days": round(span_ms / 86_400_000, 4),
                    "com_days": round(((L - 1) / 2) * TF_MS[tf] / 86_400_000, 4),
                    "warm_days": round(P.WARM[L] * TF_MS[tf] / 86_400_000, 4),
                })
    eq = pd.DataFrame(rows)

    print(f"  {'family':7s}{'N':>6s}" + "".join(f"{t:>10s}" for t in tfs)
          + "   <- memory, in DAYS")
    hr()
    for fam, members in RIBBONS.items():
        for L in members:
            cells = []
            for tf in tfs:
                d = eq[(eq.length == L) & (eq.tf == tf)].memory_days.iloc[0]
                cells.append(f"{d:10.3f}" if d < 1000 else f"{d:10.1f}")
            print(f"  {fam:7s}{L:6d}" + "".join(cells))

    # ---- the equivalence proper: EMA N @ tf == EMA N' @ tf', N' = N*T/T'
    print("\nNEAREST HTF EQUIVALENT -- 'this line, drawn on a slower chart'")
    print(f"  {'N @ tf':>14s} {'memory':>12s}   " + "  ".join(f"{t:>7s}" for t in tfs))
    hr()
    eqrows = []
    for fam, members in RIBBONS.items():
        for L in members:
            for tf in ("5m", "15m", "1h"):
                if tf not in tfs:
                    continue
                span = L * TF_MS[tf]
                cells = []
                for t2 in tfs:
                    n2 = span / TF_MS[t2]
                    cells.append(f"{n2:7.1f}" if n2 >= 1 else f"{n2:7.3f}")
                    eqrows.append({"family": fam, "length": L, "tf": tf,
                                   "equiv_tf": t2, "equiv_length": n2,
                                   "span_ms": span})
                d = span / 86_400_000
                print(f"  {f'{L} @ {tf}':>14s} {d:9.2f} d   " + "  ".join(cells))
    eqd = pd.DataFrame(eqrows)

    # ---- F-B6: the arithmetic check
    print("\nF-B6  arithmetic check -- equivalence must conserve the span exactly")
    bad = 0
    for _, r in eqd.iterrows():
        lhs = r.length * TF_MS[r.tf]
        rhs = r.equiv_length * TF_MS[r.equiv_tf]
        if abs(lhs - rhs) > 1e-6:
            bad += 1
    print(f"      {len(eqd):,} equivalences checked, span mismatches = {bad}")
    # and three spot values recomputed by hand, in the open
    spots = [(5000, "5m", "4h"), (2618, "15m", "12h"), (89, "1h", "1m")]
    for L, t1, t2 in spots:
        if t1 not in tfs or t2 not in tfs:
            continue
        want = L * TF_MS[t1] / TF_MS[t2]
        got = float(eqd[(eqd.length == L) & (eqd.tf == t1)
                        & (eqd.equiv_tf == t2)].equiv_length.iloc[0])
        ok = abs(want - got) < 1e-9
        print(f"      EMA{L} @ {t1} = {L}*{TF_MS[t1]}ms = {L * TF_MS[t1]:,}ms "
              f"= EMA{got:.4g} @ {t2}   {'OK' if ok else 'FAIL'}")
        bad += 0 if ok else 1
    if bad:
        print("      F-B6 FAIL"); raise SystemExit(2)
    print("      F-B6 PASS")

    # ---- warm-up cost, the other half of the card
    print("\nWARM-UP COST -- days of tape consumed before the line is readable")
    print(f"  {'family':7s}{'N':>6s}" + "".join(f"{t:>10s}" for t in tfs))
    hr()
    for fam, members in RIBBONS.items():
        for L in members:
            cells = []
            for tf in tfs:
                d = eq[(eq.length == L) & (eq.tf == tf)].warm_days.iloc[0]
                cells.append(f"{d:10.2f}")
            print(f"  {fam:7s}{L:6d}" + "".join(cells))
    _keep("5b_equivalence", eq)
    return _keep("5b_equivalence_htf", eqd)


# ===========================================================================
# (c) V-ULT OCCUPANCY
# ===========================================================================
def look_c(assets: list[str], tfs: list[str]) -> pd.DataFrame:
    banner("5(c) V-ULT OCCUPANCY -- what VH and UH spend their time doing")
    print(TIER_E_HEADER)
    want = [t for t in ("5m", "15m", "30m") if t in tfs]
    print(f"\ntimeframes: {want}   families: {list(V_ULT)}")
    print(f"shares are over WARM bars only (orientation != n/a); "
          f"knot = width_atr < {RIBBON_C}\n")
    rows = []
    for sym in assets:
        for tf in want:
            p = OUT / "ribbons" / sym / f"{tf}.parquet"
            if not p.exists():
                continue
            cols = [f"{f}_{c}" for f in V_ULT
                    for c in ("state", "orient", "knot", "width_atr")]
            rb = pd.read_parquet(p, columns=cols)
            for fam in V_ULT:
                o = rb[f"{fam}_orient"].to_numpy()
                st = rb[f"{fam}_state"].to_numpy()
                kn = rb[f"{fam}_knot"].to_numpy()
                w = rb[f"{fam}_width_atr"].to_numpy()
                warm = o != OR_NA
                n = int(warm.sum())
                if not n:
                    continue
                rec = {"asset": sym, "tf": tf, "family": fam, "warm_bars": n}
                for code, nm in ((ST_COMPRESS, "compressing"),
                                 (ST_FLAT, "flat"), (ST_EXPAND, "expanding")):
                    rec[f"pct_{nm}"] = round(100.0 * float((warm & (st == code)).sum()) / n, 3)
                for code, nm in ((OR_BULL, "bull"), (OR_MIXED, "mixed"),
                                 (OR_BEAR, "bear")):
                    rec[f"pct_{nm}"] = round(100.0 * float((warm & (o == code)).sum()) / n, 3)
                rec["pct_knot"] = round(100.0 * float((warm & kn).sum()) / n, 3)
                rec["width_atr_p50"] = round(q(w[warm], 0.50), 4)
                rec["width_atr_p10"] = round(q(w[warm], 0.10), 4)
                rec["width_atr_p90"] = round(q(w[warm], 0.90), 4)
                # state x orientation cross-tab, the thing actually asked for
                for scode, snm in ((ST_COMPRESS, "compressing"),
                                   (ST_FLAT, "flat"), (ST_EXPAND, "expanding")):
                    for ocode, onm in ((OR_BULL, "bull"), (OR_MIXED, "mixed"),
                                       (OR_BEAR, "bear")):
                        rec[f"pct_{snm}_{onm}"] = round(
                            100.0 * float((warm & (st == scode) & (o == ocode)).sum()) / n, 3)
                rows.append(rec)
            del rb
    oc = pd.DataFrame(rows)
    if oc.empty:
        print("  (no ribbon artifacts on 5m/15m/30m)")
        return oc

    print(f"{'asset':9s} {'tf':4s} {'fam':4s} {'warm':>10s} {'knot%':>7s} "
          f"{'comp%':>7s} {'flat%':>7s} {'exp%':>7s} {'bull%':>7s} {'mix%':>7s} "
          f"{'bear%':>7s} {'w_p50':>7s}")
    hr(n=110)
    for _, r in oc.iterrows():
        print(f"{r.asset:9s} {r.tf:4s} {r.family:4s} {r.warm_bars:10,d} "
              f"{r.pct_knot:7.2f} {r.pct_compressing:7.2f} {r.pct_flat:7.2f} "
              f"{r.pct_expanding:7.2f} {r.pct_bull:7.2f} {r.pct_mixed:7.2f} "
              f"{r.pct_bear:7.2f} {r.width_atr_p50:7.3f}")

    # ---- the scale-match observation, computed rather than asserted
    print("""
OBSERVED -- the state window is not scale-matched to the ultra ribbons.
`state` is pinned at k = 20 bars with a +-0.05 ATR threshold. Twenty bars is
a large fraction of a VH ribbon's own movement and a negligible one of UH's:
the UH lines (4236/4618/5000) span only 1.18x in length, so their band width
barely changes over 20 bars and the classifier returns `flat` almost always.
The shares below are the evidence for that statement; the constants are VETO
by name and are NOT changed here. What it means is that `UH state` carries
much less information than `VH state` does, and the two must not be read as
if they were the same measurement.""")
    print(f"\n  {'family':7s} {'flat% (panel mean)':>20s} {'width_atr p50':>15s}")
    hr(n=46)
    for fam in V_ULT:
        s = oc[oc.family == fam]
        if s.empty:
            continue
        print(f"  {fam:7s} {s.pct_flat.mean():20.2f} {s.width_atr_p50.mean():15.3f}")

    print("\nSTATE x ORIENTATION cross-tab, % of warm bars (panel mean over assets)")
    for fam in V_ULT:
        for tf in want:
            s = oc[(oc.family == fam) & (oc.tf == tf)]
            if s.empty:
                continue
            print(f"\n  {fam} @ {tf}   ({len(s)} assets, "
                  f"{int(s.warm_bars.sum()):,} warm bars)")
            print(f"    {'':13s}{'bull':>9s}{'mixed':>9s}{'bear':>9s}{'row':>9s}")
            for snm in ("compressing", "flat", "expanding"):
                vals = [s[f"pct_{snm}_{o}"].mean() for o in ("bull", "mixed", "bear")]
                print(f"    {snm:13s}" + "".join(f"{v:9.2f}" for v in vals)
                      + f"{sum(vals):9.2f}")
    return _keep("5c_vult_occupancy", oc)


# ===========================================================================
# (d)(i) FAST crosses conditioned on VH+UH orientation
# ===========================================================================
def look_d1(assets: list[str], tfs: list[str]) -> pd.DataFrame:
    banner("5(d)(i) FAST-RIBBON CROSSES CONDITIONED ON VH+UH ORIENTATION")
    print(TIER_E_HEADER)
    want = [t for t in ("5m", "15m") if t in tfs]
    print(f"""
The operator's question, made descriptive.  For every FAST within-ribbon cross
on {want}, the joint orientation of the two ULTRA ribbons at that same bar is
read off, and the forward terminal return is tabulated inside each stratum.

  ruler       signed terminal return over H100, ATR-normalised AT THE ANCHOR
              (census-2A R-1: MFE-MAE is retired as a discriminant)
  H100        DURATION-fixed at 100 x 5m = {H100_MS // 60000} minutes, so the
              5m and 15m tables answer the same question
  sign        + means price went the way the cross pointed; up and down crosses
              are ALSO split out separately, never pooled silently
  toll        the round-trip toll measured on THIS population, printed beside
              every row.  A stratum whose median sits inside the toll band has
              produced nothing a trader could have kept.

NOTHING IS PROMOTED.  Every stratum of a complete partition is printed; no
threshold is swept, no arm is ranked and kept.  m = 0.
""")
    rows = []
    for sym in assets:
        for tf in want:
            pe = OUT / "emas" / sym / f"{tf}.parquet"
            pc = OUT / "crosses" / sym / f"{tf}.parquet"
            pr = OUT / "ribbons" / sym / f"{tf}.parquet"
            if not (pe.exists() and pc.exists() and pr.exists()):
                continue
            e = pd.read_parquet(pe, columns=["open_time", "close", "atr"])
            rb = pd.read_parquet(pr, columns=[f"{f}_orient" for f in V_ULT])
            ot = e["open_time"].to_numpy(np.int64)
            close = e["close"].to_numpy(np.float64)
            av = e["atr"].to_numpy(np.float64)
            jv = joint_vult(rb["VH_orient"].to_numpy(), rb["UH_orient"].to_numpy())

            ev = pd.read_parquet(pc, columns=["pair_class", "family", "pair",
                                              "event", "dir", "bar_index"])
            ev = ev[(ev.pair_class == "within_ribbon") & (ev.family == "FAST")]
            if ev.empty:
                continue
            idx = ev.bar_index.to_numpy(np.int64)
            # forward terminal, duration-fixed
            tgt = ot[idx] + H100_MS
            j = np.searchsorted(ot, tgt, side="left")
            ok = (j < len(ot)) & np.isfinite(av[idx]) & (av[idx] > 0)
            j = np.clip(j, 0, len(ot) - 1)
            raw = np.where(ok, (close[j] - close[idx]) / av[idx], np.nan)
            sgn = np.where(ev["dir"].to_numpy() == "up", 1.0, -1.0)
            ev = ev.assign(term_raw=raw, term_signed=raw * sgn,
                           vult=jv[idx], resolved=ok)

            for pair in sorted(ev.pair.unique()):
                for vcode, vnm in ((OR_BULL, "bull-fanned"),
                                   (OR_MIXED, "mixed"),
                                   (OR_BEAR, "bear-fanned")):
                    s = ev[(ev.pair == pair) & (ev.vult == vcode) & ev.resolved]
                    if s.empty:
                        continue
                    sidx = s.bar_index.to_numpy(np.int64)
                    mask = np.zeros(len(ot), bool); mask[sidx] = True
                    tl = toll_atr(close, av, mask)
                    for dlab, ss in (("both", s), ("up", s[s.dir == "up"]),
                                     ("down", s[s.dir == "down"])):
                        if ss.empty:
                            continue
                        v = ss.term_signed.to_numpy(np.float64)
                        rows.append({
                            "asset": sym, "tf": tf, "pair": pair,
                            "vult_orient": vnm, "dir": dlab, "n": len(ss),
                            "term_p25": round(q(v, .25), 4),
                            "term_p50": round(q(v, .50), 4),
                            "term_p75": round(q(v, .75), 4),
                            "term_mean": round(float(np.nanmean(v)), 4),
                            "pct_positive": round(100.0 * float(np.nanmean(v > 0)), 2),
                            "toll_atr": round(tl, 4),
                            "median_inside_toll": bool(abs(q(v, .50)) <= tl),
                        })
            del e, rb, ev
    d1 = pd.DataFrame(rows)
    if d1.empty:
        print("  (no FAST crosses with warm VH+UH on 5m/15m)")
        return d1

    for tf in want:
        for pair in sorted(d1[d1.tf == tf].pair.unique()):
            print(f"\nFAST pair {pair} @ {tf} -- panel, by VH+UH orientation")
            print(f"  {'orient':13s} {'dir':5s} {'n':>9s} {'p25':>8s} {'p50':>8s} "
                  f"{'p75':>8s} {'mean':>8s} {'%>0':>7s} {'toll':>7s} {'in toll':>8s}")
            hr(n=100)
            s = d1[(d1.tf == tf) & (d1.pair == pair)]
            for vnm in ("bull-fanned", "mixed", "bear-fanned"):
                for dlab in ("both", "up", "down"):
                    g = s[(s.vult_orient == vnm) & (s.dir == dlab)]
                    if g.empty:
                        continue
                    n = int(g.n.sum())
                    # panel figure = count-weighted mean of the per-asset medians
                    p50 = float((g.term_p50 * g.n).sum() / n)
                    p25 = float((g.term_p25 * g.n).sum() / n)
                    p75 = float((g.term_p75 * g.n).sum() / n)
                    mu = float((g.term_mean * g.n).sum() / n)
                    pp = float((g.pct_positive * g.n).sum() / n)
                    tl = float((g.toll_atr * g.n).sum() / n)
                    print(f"  {vnm:13s} {dlab:5s} {n:9,d} {p25:8.4f} {p50:8.4f} "
                          f"{p75:8.4f} {mu:8.4f} {pp:7.2f} {tl:7.4f} "
                          f"{'YES' if abs(p50) <= tl else 'no':>8s}")
            print(f"  TOLL LINE: round-trip {TOLL_BPS_ROUND_TRIP:.0f} bps, measured "
                  f"on each stratum's own rows. 'in toll' = |median| <= toll.")
    return _keep("5d1_fast_by_vult", d1)


# ===========================================================================
# (d)(ii) VH/UH KNOT EPISODES -> time to expansion, direction, magnitude
# ===========================================================================
def knot_episodes(sym: str, tf: str, fam: str) -> pd.DataFrame:
    pr = OUT / "ribbons" / sym / f"{tf}.parquet"
    pe = OUT / "emas" / sym / f"{tf}.parquet"
    if not (pr.exists() and pe.exists()):
        return pd.DataFrame()
    rb = pd.read_parquet(pr, columns=[f"{fam}_knot", f"{fam}_state",
                                      f"{fam}_orient", f"{fam}_width_atr",
                                      "open_time"])
    e = pd.read_parquet(pe, columns=["close", "atr"])
    kn = rb[f"{fam}_knot"].to_numpy(bool)
    st = rb[f"{fam}_state"].to_numpy()
    o = rb[f"{fam}_orient"].to_numpy()
    w = rb[f"{fam}_width_atr"].to_numpy(np.float64)
    ot = rb["open_time"].to_numpy(np.int64)
    close = e["close"].to_numpy(np.float64)
    av = e["atr"].to_numpy(np.float64)
    n = len(kn)
    if not kn.any():
        return pd.DataFrame()

    # maximal runs of knot==True
    d = np.diff(np.concatenate(([0], kn.view(np.int8), [0])))
    starts = np.flatnonzero(d == 1)
    ends = np.flatnonzero(d == -1) - 1
    rows = []
    for s0, e0 in zip(starts, ends):
        hi = min(n - 1, e0 + KNOT_SEARCH_CAP)
        seg = st[e0 + 1:hi + 1]
        rel = np.flatnonzero(seg == ST_EXPAND)
        if rel.size:
            j = e0 + 1 + int(rel[0])
            ttl = j - e0
            # magnitude: peak width reached before the ribbon knots again
            k2 = np.flatnonzero(kn[j:hi + 1])
            stop = j + int(k2[0]) if k2.size else hi
            peak = float(np.nanmax(w[j:stop + 1])) if stop >= j else np.nan
            mag = peak - float(w[e0]) if np.isfinite(peak) else np.nan
            disp = ((close[stop] - close[e0]) / av[e0]
                    if np.isfinite(av[e0]) and av[e0] > 0 else np.nan)
            direction = ORIENT_NAME.get(int(o[j]), "n/a")
        else:
            j, ttl, mag, disp, direction, peak = -1, np.nan, np.nan, np.nan, "none", np.nan
        rows.append({
            "asset": sym, "tf": tf, "family": fam,
            "start_ts": int(ot[s0]), "end_ts": int(ot[e0]),
            "len_bars": int(e0 - s0 + 1),
            "width_at_end": round(float(w[e0]), 4),
            "expanded": bool(j >= 0),
            "bars_to_expansion": ttl,
            "immediate": bool(j == e0 + 1),
            "expansion_dir": direction,
            "span_bars": int(stop - e0) if j >= 0 else -1,
            "peak_width_atr": round(peak, 4) if np.isfinite(peak) else np.nan,
            "magnitude_atr": round(mag, 4) if np.isfinite(mag) else np.nan,
            "displacement_atr": round(disp, 4) if np.isfinite(disp) else np.nan,
            # the toll measured AT THE KNOT, on this episode's own bar -- never
            # a figure carried over from a table built on another timeframe
            "toll_atr": round(float((TOLL_BPS_ROUND_TRIP / 10000.0)
                                    * close[e0] / av[e0]), 5)
            if np.isfinite(av[e0]) and av[e0] > 0 else np.nan,
        })
    return pd.DataFrame(rows)


def look_d2(assets: list[str], tfs: list[str]) -> pd.DataFrame:
    banner("5(d)(ii) VH/UH KNOT EPISODES -- the knot->fan, at ultra scale, COUNTED")
    print(TIER_E_HEADER)
    want = [t for t in ("5m", "15m", "30m", "1h") if t in tfs]
    print(f"""
episode      a maximal run of bars with width_atr < {RIBBON_C} (the pinned knot)
expansion    the FIRST bar after the run whose state is `expanding`
             (|width_delta_{K_WINDOW}| > {STATE_EPS} ATR), searched at most
             {KNOT_SEARCH_CAP:,} bars forward; episodes that never expand are
             counted as such and are NOT dropped
direction    the ribbon's own orientation at the expansion bar
magnitude    peak width_atr reached before the next knot, minus width at the
             knot's last bar
displacement price move from the knot's last bar to that peak, in ATR at the knot
""")
    parts = []
    for sym in assets:
        for tf in want:
            for fam in V_ULT:
                ep = knot_episodes(sym, tf, fam)
                if not ep.empty:
                    parts.append(ep)
    if not parts:
        print("  (no VH/UH knot episodes found)")
        return pd.DataFrame()
    ep = pd.concat(parts, ignore_index=True)

    print(f"{'asset':9s} {'tf':4s} {'fam':4s} {'episodes':>9s} {'expanded':>9s} "
          f"{'never':>7s} {'len_p50':>8s} {'ttl_p50':>8s} {'ttl_p90':>8s} "
          f"{'mag_p50':>8s} {'disp_p50':>9s}")
    hr(n=110)
    for (sym, tf, fam), g in ep.groupby(["asset", "tf", "family"], sort=True):
        exp = g[g.expanded]
        print(f"{sym:9s} {tf:4s} {fam:4s} {len(g):9,d} {len(exp):9,d} "
              f"{len(g) - len(exp):7,d} {g.len_bars.median():8.1f} "
              f"{q(exp.bars_to_expansion.to_numpy(float), .5):8.1f} "
              f"{q(exp.bars_to_expansion.to_numpy(float), .9):8.1f} "
              f"{q(exp.magnitude_atr.to_numpy(float), .5):8.3f} "
              f"{q(exp.displacement_atr.to_numpy(float), .5):9.3f}")

    print("\nEXPANSION DIRECTION -- the per-direction split, on a complete partition")
    print(f"  {'fam':4s} {'tf':4s} {'bull':>10s} {'bear':>10s} {'mixed':>10s} "
          f"{'never':>10s} {'bull share':>11s}")
    hr(n=70)
    for (fam, tf), g in ep.groupby(["family", "tf"], sort=True):
        b = int((g.expansion_dir == "bull-fanned").sum())
        r = int((g.expansion_dir == "bear-fanned").sum())
        m = int((g.expansion_dir == "mixed").sum())
        nv = int((g.expansion_dir == "none").sum())
        tot = b + r
        print(f"  {fam:4s} {tf:4s} {b:10,d} {r:10,d} {m:10,d} {nv:10,d} "
              f"{(b / tot if tot else float('nan')):11.4f}")

    # ---- the definitional caveat, computed rather than asserted
    print("""
CAVEAT -- READ THIS BEFORE THE TIME-TO-EXPANSION COLUMN.
`knot` and `expanding` are two SEPARATELY pinned constants (c = 0.5 ATR;
|width_delta_20| > 0.05 ATR) and they are not scale-matched to each other.
A knot run ENDS precisely when the width rises back through 0.5 ATR -- which
is, mechanically, a width that is increasing. So for a ribbon whose width
moves at all on a 20-bar scale, the bar after the knot is ALREADY `expanding`
and time-to-expansion is 1 by construction, not by anything in the tape.
The share of episodes for which that happens is printed below. Where it is
near 100%, the time-to-expansion column is measuring the definition.""")
    print(f"\n  {'fam':4s} {'tf':4s} {'episodes':>9s} {'expanded':>9s} "
          f"{'immediate':>10s} {'immediate share':>16s}")
    hr(n=62)
    for (fam, tf), g in ep.groupby(["family", "tf"], sort=True):
        e2 = g[g.expanded]
        sh = float(e2.immediate.mean()) if len(e2) else float("nan")
        print(f"  {fam:4s} {tf:4s} {len(g):9,d} {len(e2):9,d} "
              f"{int(e2.immediate.sum()):10,d} {sh:16.4f}")

    print("\nDISPLACEMENT vs THE TOLL -- knot-to-peak move, in ATR")
    print("  NOTE: displacement is measured over the WHOLE span from the knot's last")
    print("  bar to the peak-width bar. That span is long and variable (`span_p50`),")
    print("  so this is a SPAN statistic, not a per-trade edge; the toll is a FLOOR")
    print("  it must clear, not a benchmark it can be compared to directly.\n")
    print(f"  {'fam':4s} {'tf':4s} {'n':>7s} {'span_p50':>9s} {'|d| p25':>8s} "
          f"{'|d| p50':>8s} {'|d| p75':>8s} {'signed p50':>11s} {'toll':>8s} "
          f"{'toll/|d|p50':>12s}")
    hr(n=95)
    for (fam, tf), g in ep.groupby(["family", "tf"], sort=True):
        v = g.displacement_atr.to_numpy(float)
        v = v[np.isfinite(v)]
        if not v.size:
            continue
        tl = float(np.nanmedian(g.toll_atr.to_numpy(float)))
        sp = q(g[g.expanded].span_bars.to_numpy(float), .50)
        dp50 = q(np.abs(v), .50)
        print(f"  {fam:4s} {tf:4s} {len(v):7,d} {sp:9.0f} "
              f"{q(np.abs(v), .25):8.3f} {dp50:8.3f} {q(np.abs(v), .75):8.3f} "
              f"{q(v, .50):+11.3f} {tl:8.4f} {tl / dp50 if dp50 else float('nan'):12.4f}")
    print(f"\n  TOLL LINE: {TOLL_BPS_ROUND_TRIP:.0f} bps round trip, measured on EACH "
          f"population's own bars.\n"
          f"  It is NOT the census-2A 4h figure (0.026-0.059 ATR): the toll in ATR "
          f"units GROWS as\n  the timeframe shortens, because ATR shrinks faster "
          f"than price does. Quoting a 4h toll\n  beside a 5m table would understate "
          f"the cost by roughly an order of magnitude.")
    return _keep("5d2_knot_episodes", ep)


# ===========================================================================
# (d)(iii) census-2A CAMPAIGN BOOK joined to VH ribbon state
# ===========================================================================
def assert_key(df: pd.DataFrame, keys: list[str], label: str) -> int:
    dup = int(df.duplicated(subset=keys).sum())
    print(f"    F-KEY  {label:30s} key={keys} rows={len(df):,} dup={dup}")
    if dup:
        raise SystemExit(f"HALT (F-KEY): '{label}' key {keys} is NOT unique -- "
                         f"{dup} duplicate row(s). A join on a non-unique key "
                         f"silently drops or multiplies rows.")
    return dup


def look_d3(assets: list[str], tfs: list[str]) -> pd.DataFrame:
    banner("5(d)(iii) CENSUS-2A CAMPAIGN BOOK x VH RIBBON STATE  (descriptive overlay)")
    print(TIER_E_HEADER)
    join_tf = "5m" if "5m" in tfs else (tfs[0] if tfs else None)
    bookp = CENSUS2A / "cen4" / "cen4_book.parquet"
    campp = CENSUS2A / "cen5" / "cen5_campaigns.parquet"
    if not (bookp.exists() and campp.exists() and join_tf):
        print(f"  SKIP -- census-2A book not found ({campp}) or no join tf")
        return pd.DataFrame()

    book = pd.read_parquet(bookp)
    camp = pd.read_parquet(campp)
    print(f"\n  cen5_campaigns {len(camp):,} rows  {campp}   <- THE campaign book")
    print(f"  cen4_book      {len(book):,} rows  {bookp}   <- realised-R side")
    print(f"  join tf        {join_tf}   (census EXEC_TF; VH state read at the "
          f"bar CONTAINING the entry)\n")

    print("  F-KEY -- declared keys asserted BEFORE the join, never after")
    assert_key(camp, ["tranche_id"], "cen5_campaigns")
    assert_key(camp, ["asset", "ts_ms", "mandate"], "cen5_campaigns composite")
    # cen4_book's tranche_id is unique only WITHIN a cell -- the exact defect
    # census2a_program.assert_key's docstring records. The whole key is the
    # campaign's own tranche_id, which is 'cell|tranche_id'.
    book = book.assign(ckey=book.cell.astype(str) + "|" + book.tranche_id.astype(str))
    assert_key(book, ["ckey"], "cen4_book (cell|tranche_id)")
    dup_at = int(camp.duplicated(subset=["asset", "ts_ms"]).sum())
    print(f"    NOTE  (asset, ts_ms) alone has dup={dup_at} in cen5_campaigns -- a BTC "
          f"intraday\n          and a BTC swing campaign share one instant. `mandate` "
          f"is part of the key\n          for that reason; it is not a defect.")

    m = camp.merge(book[["ckey", "realized_r", "r_norm", "cohort", "resolved"]],
                   left_on="tranche_id", right_on="ckey", how="left",
                   validate="one_to_one")
    unmatched = m[m.realized_r.isna()]
    print(f"    joined rows = {len(m):,}  matched = {int(m.realized_r.notna().sum()):,}"
          f"  unmatched = {len(unmatched):,} "
          f"({sorted(set(unmatched.asset))} -- the ANNEX assets, absent from the "
          f"panel-only cen4_book)")

    # ---- THE GAP, REPORTED NOT FIXED
    print("""
  REPORTED, NOT FIXED -- 'ribbon state at EXIT' cannot be computed.
  The contract asks for VH state at entry AND at exit.  cen4_book carries
  ts_open / ts_ms (both the ENTRY) and cen5_campaigns carries no exit
  timestamp at all -- only realised outcomes (ride_R, give_back_R, mfe_R).
  cen2_ledger's window_close_ts is the ARMING WINDOW's close, a different
  object, and using it as an exit would be an invention.  The ENTRY side is
  computed in full below; the exit side is left undone and named here.
""")

    rows = []
    for sym in sorted(set(m.asset) & set(assets)):
        pr = OUT / "ribbons" / sym / f"{join_tf}.parquet"
        pe = OUT / "emas" / sym / f"{join_tf}.parquet"
        if not (pr.exists() and pe.exists()):
            continue
        rb = pd.read_parquet(pr, columns=["open_time", "VH_state", "VH_orient",
                                          "VH_knot", "VH_pos", "VH_width_atr",
                                          "UH_orient"])
        e = pd.read_parquet(pe, columns=["close", "atr"])
        ot = rb["open_time"].to_numpy(np.int64)
        s = m[m.asset == sym]
        ts = s.ts_ms.to_numpy(np.int64)
        # the bar CONTAINING the entry: last bar whose open_time <= ts
        j = np.searchsorted(ot, ts, side="right") - 1
        inside = (j >= 0) & (j < len(ot))
        j = np.clip(j, 0, len(ot) - 1)
        jv = joint_vult(rb["VH_orient"].to_numpy(), rb["UH_orient"].to_numpy())
        rows.append(pd.DataFrame({
            "asset": sym, "tranche_id": s.tranche_id.to_numpy(),
            "dir": s.dir.to_numpy(), "mandate": s.mandate.to_numpy(),
            "ts_ms": ts,
            "ride_R": s.ride_R.to_numpy(),
            "mfe_R": s.mfe_R.to_numpy(),
            "give_back_R": s.give_back_R.to_numpy(),
            "outcome_sign": s.outcome_sign.to_numpy(),
            "realized_r": s.realized_r.to_numpy(),
            "in_range": inside,
            "vh_state": [STATE_NAME[int(x)] for x in rb["VH_state"].to_numpy()[j]],
            "vh_orient": [ORIENT_NAME[int(x)] for x in rb["VH_orient"].to_numpy()[j]],
            "vh_knot": rb["VH_knot"].to_numpy()[j],
            "vh_width_atr": rb["VH_width_atr"].to_numpy()[j],
            "vult_orient": [ORIENT_NAME[int(x)] for x in jv[j]],
            "toll_atr": np.where(np.isfinite(e["atr"].to_numpy()[j])
                                 & (e["atr"].to_numpy()[j] > 0),
                                 (TOLL_BPS_ROUND_TRIP / 10000.0)
                                 * e["close"].to_numpy()[j] / e["atr"].to_numpy()[j],
                                 np.nan),
        }))
        del rb, e
    if not rows:
        print("  (no overlap between the campaign book and the census-2B substrate)")
        return pd.DataFrame()
    j3 = pd.concat(rows, ignore_index=True)
    j3 = j3[j3.in_range]
    warm = j3[j3.vh_orient != "n/a"]
    print(f"  campaigns placed on a {join_tf} bar: {len(j3):,}   "
          f"of which VH is WARM at entry: {len(warm):,} "
          f"({100.0 * len(warm) / max(len(j3), 1):.1f}%)")
    print(f"  the cold remainder is NOT dropped silently -- it is "
          f"{len(j3) - len(warm):,} campaigns whose entry predates VH's warm-up "
          f"on {join_tf}, and it is excluded from the state tables below by "
          f"construction, not by choice.")

    # winners/losers use the campaign book's OWN label (outcome_sign, defined on
    # ride_R), not a threshold invented here. m stays 0 because the partition is
    # the census's, imported whole.
    win = warm[warm.outcome_sign == "win"]
    los = warm[warm.outcome_sign != "win"]
    tl = float(np.nanmedian(warm.toll_atr.to_numpy(float)))
    print(f"\n  winners {len(win):,}  losers {len(los):,}   "
          f"(census-2A `outcome_sign`, defined on ride_R -- not a cut made here)")
    print(f"  toll on this population = {tl:.4f} ATR")

    print("\nWINNERS vs LOSERS BY VH RIBBON STATE AT ENTRY (occupancy shares, %)")
    for col, label in (("vh_state", "VH state"), ("vh_orient", "VH orientation"),
                       ("vult_orient", "VH+UH joint orientation")):
        print(f"\n  {label}")
        print(f"    {'value':16s}{'winners%':>10s}{'losers%':>10s}"
              f"{'all%':>10s}{'n_win':>9s}{'n_los':>9s}")
        for v in sorted(set(warm[col])):
            wpc = 100.0 * float((win[col] == v).mean()) if len(win) else float("nan")
            lpc = 100.0 * float((los[col] == v).mean()) if len(los) else float("nan")
            apc = 100.0 * float((warm[col] == v).mean())
            print(f"    {v:16s}{wpc:10.2f}{lpc:10.2f}{apc:10.2f}"
                  f"{int((win[col] == v).sum()):9,d}"
                  f"{int((los[col] == v).sum()):9,d}")

    print("\n  knot at entry: winners "
          f"{100.0 * float(win.vh_knot.mean()) if len(win) else float('nan'):.2f}%  "
          f"losers {100.0 * float(los.vh_knot.mean()) if len(los) else float('nan'):.2f}%"
          f"  all {100.0 * float(warm.vh_knot.mean()):.2f}%")

    print("\nRIDE-R BY VH ORIENTATION AT ENTRY -- with the per-direction split")
    print(f"  {'vh_orient':14s} {'dir':6s} {'n':>8s} {'p25':>8s} {'p50':>8s} "
          f"{'p75':>8s} {'mean':>8s} {'%win':>7s} {'mfe_p50':>8s} {'toll':>7s}")
    hr(n=100)
    out_rows = []
    for grpcol, grps in (("vh_orient", sorted(set(warm.vh_orient))),
                         ("vult_orient", sorted(set(warm.vult_orient))),
                         ("vh_state", sorted(set(warm.vh_state)))):
        if grpcol != "vh_orient":
            print(f"\n  --- by {grpcol} ---")
        for v in grps:
            for dlab in ("both", "long", "short"):
                base = warm[warm[grpcol] == v]
                g = base if dlab == "both" else base[base.dir == dlab]
                if g.empty:
                    continue
                r = g.ride_R.to_numpy(float)
                mf = g.mfe_R.to_numpy(float)
                t = float(np.nanmedian(g.toll_atr.to_numpy(float)))
                pw = 100.0 * float((g.outcome_sign == "win").mean())
                print(f"  {v:14s} {dlab:6s} {len(g):8,d} {q(r, .25):8.4f} "
                      f"{q(r, .50):8.4f} {q(r, .75):8.4f} "
                      f"{float(np.nanmean(r)):8.4f} {pw:7.2f} "
                      f"{q(mf, .50):8.4f} {t:7.4f}")
                out_rows.append({"group": grpcol, "value": v, "dir": dlab,
                                 "n": len(g), "ride_p25": q(r, .25),
                                 "ride_p50": q(r, .50), "ride_p75": q(r, .75),
                                 "ride_mean": float(np.nanmean(r)),
                                 "pct_win": pw, "mfe_p50": q(mf, .50),
                                 "toll_atr": t})
    print(f"\n  TOLL LINE: {TOLL_BPS_ROUND_TRIP:.0f} bps round trip = {tl:.4f} ATR median "
          f"on this population.\n"
          f"  ride_R is already R-normalised by census-2A; the toll column is "
          f"printed in ATR,\n  so the two rulers sit side by side and are never "
          f"silently mixed.")
    print("\n  THIS IS A DESCRIPTIVE OVERLAY. No comparison above is promoted; the "
          "strata are a\n  COMPLETE partition of a fixed population, printed whole. "
          "m = 0.")
    _keep("5d3_campaign_by_vh_summary", pd.DataFrame(out_rows))
    return _keep("5d3_campaign_by_vh", warm)


# ===========================================================================
# RUN
# ===========================================================================
def run(fm: pd.DataFrame, assets: list[str], tfs: list[str]) -> None:
    t0 = time.time()
    banner("STAGE 5 -- FIRST LOOK  (DISPLAY-ONLY / Tier-E, m = 0)")
    print(TIER_E_HEADER)
    FL.mkdir(parents=True, exist_ok=True)

    look_a(assets, tfs)
    look_b(tfs)
    look_c(assets, tfs)
    look_d1(assets, tfs)
    look_d2(assets, tfs)
    look_d3(assets, tfs)

    banner("STAGE 5 ARTIFACTS")
    for name, df in _TABLES.items():
        if df is None or df.empty:
            print(f"  {name:34s} EMPTY -- not written")
            continue
        p = FL / f"{name}.parquet"
        df.to_parquet(p, index=False)
        print(f"  {name:34s} rows={len(df):9,d}  bytes={p.stat().st_size:9,d}  {p}")
    hdr = FL / "TIER_E.json"
    hdr.write_text(json.dumps({
        "class": "DISPLAY-ONLY / Tier-E exploration",
        "header": TIER_E_HEADER,
        "selection_surface_m": 0,
        "stamp": "EXPLORATION -- ungated; promotion requires registration.",
        "toll_bps_round_trip": TOLL_BPS_ROUND_TRIP,
        "h100_ms": H100_MS,
        "note": ("Every table is a count or a quantile over a fixed, complete "
                 "partition. No threshold swept, no arm ranked and kept, no "
                 "row dropped on the strength of its value."),
        "tables": sorted(_TABLES),
    }, indent=2), encoding="utf-8")
    print(f"  {'TIER_E.json':34s} {hdr}")
    print(f"\nstage 5 elapsed {time.time() - t0:.0f}s")
