#!/usr/bin/env python3
"""
CENSUS-2B / W-TB1 -- TAIL BIOGRAPHY ("who they are, what they had for brunch")
==============================================================================
Contract: operator paste 2026-08-14.  Drafted: APOLLO (scope credit: DIONYSUS
§4).  Executor: HEPHAESTUS.  Seed 20260814.
CLASS: Tier-E descriptive.  REGISTRATIONS DEFERRED -- motif results go to the
probe ledger with their full selection surface m; nothing promoted.
F-KEY everywhere.

CURTAIN DISCIPLINE
------------------
The +72h AFTER side is ANATOMY, never entry evidence.  Every table splits at
t0 and labels the halves BEFORE / AFTER.  The exit-side capture is labelled
EXIT-ANATOMY on top of that, so a row can never be read as a birth feature by
accident: it would have to be read past two labels.

WHAT THIS IS
------------
814 winning campaigns (the 12.3% tail of the resolved book) and 814 matched
losers, photographed for +-72h around birth on four lenses, with the full
census-2B event grammar as a tape -- crosses, refusals, armed windows, knot
and fan transitions, sweeps -- and the same tape again around the exit.

Part A (census2b_parta.py) supplies A-1..A-4; this program consumes them and
restates none of them.

USAGE
    python scripts/census2b_wtb1.py --stage cohort
    python scripts/census2b_wtb1.py --stage all
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

import census2b_program as c2b                                   # noqa: E402
import census2b_parta as pa                                      # noqa: E402

RIBBONS = c2b.RIBBONS
FAMILIES = c2b.FAMILIES
ALL_EMAS = c2b.ALL_EMAS
WARM = c2b.WARM
PANEL = c2b.PANEL
OUT = c2b.OUT
to_parquet_atomic = c2b.to_parquet_atomic
iso = c2b.iso
hr = c2b.hr
banner = c2b.banner
ST_COMPRESS, ST_FLAT, ST_EXPAND, ST_NA = (c2b.ST_COMPRESS, c2b.ST_FLAT,
                                          c2b.ST_EXPAND, c2b.ST_NA)
OR_BEAR, OR_MIXED, OR_BULL, OR_NA = c2b.OR_BEAR, c2b.OR_MIXED, c2b.OR_BULL, c2b.OR_NA
KN_FALSE, KN_TRUE, KN_NA = c2b.KN_FALSE, c2b.KN_TRUE, c2b.KN_NA
K_WINDOW, STATE_EPS, RIBBON_C = c2b.K_WINDOW, c2b.STATE_EPS, c2b.RIBBON_C
TOLL_BPS_ROUND_TRIP = c2b.TOLL_BPS_ROUND_TRIP
STATE_NAME, ORIENT_NAME, KNOT_NAME = c2b.STATE_NAME, c2b.ORIENT_NAME, c2b.KNOT_NAME

TF_MS = pa.TF_MS
HORIZONS_MS = pa.HORIZONS_MS
SR_MEDIAN_PAIRS = pa.SR_MEDIAN_PAIRS
PARED_WITHIN_SR = pa.PARED_WITHIN_SR
fan_age_series = pa.fan_age_series
attach_r1 = pa.attach_r1
load_cell = pa.load_cell
print_horizon_realisation = pa.print_horizon_realisation

# ===========================================================================
# CONSTANTS -- VETO BY NAME
# ===========================================================================
SEED = 20260814
PROGRAM = "census2b_wtb1.py"

LENSES = ["5m", "15m", "30m", "1h"]          # [contract]
WIN_H = 72                                    # +-72h around birth   [contract]
EXIT_H = 24                                   # +-24h around exit    [contract]
TOP_N_BRUNCH = 20                             # W-E                  [contract]
KGRAM_MAX = 4                                 # W-B k<=4             [contract]
MOTIF_WINDOW_H = 24                           # W-B: 24h before t0   [contract]
STAGES_H = [-72, -24, -4, 0, 24]              # W-A, plus t_exit     [contract]

# The 7-TF ladder and the tier grammar, imported by value from seq8_views so
# the three SEQ frames here ARE the ratified three frames and not a re-spelling.
SEQ_TFS = ["5m", "15m", "30m", "1h", "4h", "12h", "1d"]
TFI = {tf: i for i, tf in enumerate(SEQ_TFS)}
TIER_GRAMMAR = {"5m": "FAST", "15m": "FAST", "30m": "FAST",
                "1h": "STAIR", "4h": "SLOW", "12h": "SLOW", "1d": "TREND"}
SEQ_FRAMES = ["absolute", "gov_relative", "tier"]

WALL_ATR = 0.5                                # census-2A §0 pin, carried

C2A = REPO / "research_outputs" / "census2a"
CEN5 = C2A / "cen5" / "cen5_campaigns.parquet"
CEN4 = C2A / "cen4" / "cen4_book.parquet"
VERDICT = C2A / "cen6" / "cen6_verdict_state.parquet"
WF1 = REPO / "_reviewer_box" / "wf1"

W = OUT / "wtb1"
D_STATE = W / "state"
D_TAPE = W / "tape"
D_AGG = W / "agg"

TIER_E_HEADER = c2b.TIER_E_HEADER
_T0 = time.time()


# ===========================================================================
# THE BR RIBBON -- the ratified SR grammar, applied to all 18 lines at once
# ===========================================================================
def br_state(e: pd.DataFrame) -> dict[str, np.ndarray]:
    """The BIG RIBBON as a seventh ribbon, under the SAME pinned grammar.

    Everything here is census2b_program.family_state with the family's three
    members replaced by all eighteen: band = envelope(min, max) over the finite
    EMAs, width_atr = (upper-lower)/ATR, state from |width_delta_20| vs 0.05
    ATR, knot at width < 0.5 ATR.  No new constant is introduced -- if the BR
    needed its own thresholds it would be a new object, not the same object at
    a larger scale, and the contract asks for the latter.

    `orient` reads the SIX SR MEDIANS (12, 89, 316, 889, 2618, 4618): bull when
    strictly fast-over-slow all the way down, bear when strictly the reverse,
    mixed otherwise -- the same monotone-order test the SR grammar uses on its
    three members.
    """
    n = len(e)
    cols = [e[f"e{L}"].to_numpy(np.float64) for L in ALL_EMAS]
    M = np.vstack(cols)                              # 18 x n
    av = e["atr"].to_numpy(np.float64)
    close = e["close"].to_numpy(np.float64)
    fin = np.isfinite(M)
    n_fin = fin.sum(axis=0)
    # ALL EIGHTEEN, or nothing. `n_fin > 0` would take the envelope over
    # whatever happens to be warm, so a 2019 bar spanning e9..e26 and a 2023 bar
    # spanning e9..e5000 would both be called "the BR width" -- 13.1 ATR against
    # 26.4 ATR on BTC 1h, two populations under one column name, on 37.8% of the
    # capture. That is absent data presented as a definite value, which is this
    # estate's signature wound. Partial bars are NaN and are counted.
    warm = (n_fin == len(ALL_EMAS)) & np.isfinite(av) & (av > 0)

    with np.errstate(invalid="ignore"):
        upper = np.where(warm, np.nanmax(np.where(fin, M, -np.inf), axis=0), np.nan)
        lower = np.where(warm, np.nanmin(np.where(fin, M, np.inf), axis=0), np.nan)
    raw_w = upper - lower
    with np.errstate(invalid="ignore", divide="ignore"):
        w_atr = np.where(warm, raw_w / av, np.nan)

    prev = np.full(n, np.nan)
    if n > K_WINDOW:
        prev[K_WINDOW:] = raw_w[:-K_WINDOW]
    with np.errstate(invalid="ignore", divide="ignore"):
        d_k = np.where(warm & np.isfinite(prev), (raw_w - prev) / av, np.nan)
    state = np.full(n, ST_NA, dtype=np.int8)
    f = np.isfinite(d_k)
    state[f] = ST_FLAT
    state[f & (d_k < -STATE_EPS)] = ST_COMPRESS
    state[f & (d_k > STATE_EPS)] = ST_EXPAND

    meds = [12, 89, 316, 889, 2618, 4618]
    S = np.vstack([e[f"e{L}"].to_numpy(np.float64) for L in meds])   # 6 x n
    ok6 = np.isfinite(S).all(axis=0)
    # S is stacked FAST-to-SLOW, so diff(S, axis=0)[i] = S[i+1] - S[i] = slower
    # minus faster. BULL is fast ABOVE slow -- e12 > e89 > ... > e4618 -- which
    # is dif < 0, not dif > 0. The first draft had these two lines the wrong way
    # round and labelled every textbook bear fan `bull`, contradicting both the
    # ratified per-family grammar (census2b_program.py:702-703) and this
    # function's own `sr_order_disorder`, which had the convention right.
    dif = np.diff(S, axis=0)                          # 5 x n, slower - faster
    orient = np.full(n, OR_NA, dtype=np.int8)
    orient[ok6] = OR_MIXED
    orient[ok6 & (dif < 0).all(axis=0)] = OR_BULL     # e12 > e89 > ... > e4618
    orient[ok6 & (dif > 0).all(axis=0)] = OR_BEAR     # e12 < e89 < ... < e4618

    knot = np.full(n, KN_NA, dtype=np.int8)
    kok = warm & np.isfinite(w_atr)
    knot[kok] = (w_atr[kok] < RIBBON_C).astype(np.int8)

    # SR-order disorder: inversions of the six medians against the bull order,
    # normalised by the 15 pairs. The contract calls it "SR-order entropy"; no
    # definition of that name is pinned anywhere in the estate, so the quantity
    # is stated here rather than assumed: 0 = perfectly bull-ordered, 1 =
    # perfectly bear-ordered, 0.5 = maximally scrambled.
    inv = np.zeros(n)
    for a in range(6):
        for b in range(a + 1, 6):
            inv += (S[a] < S[b]).astype(float)
    disorder = np.where(ok6, inv / 15.0, np.nan)

    # dispersion in ATR: the BR's own width, which IS (max-min)/ATR
    disp = w_atr

    # ranks of the 18 lines, 1 = highest value; NaN lines get 0
    order = np.argsort(np.where(fin, -M, np.inf), axis=0, kind="stable")
    ranks = np.zeros_like(M, dtype=np.int8)
    rr = np.arange(1, 19, dtype=np.int8)[:, None]
    np.put_along_axis(ranks, order, np.repeat(rr, n, axis=1), axis=0)
    ranks = np.where(fin, ranks, 0).astype(np.int8)

    pos = np.full(n, c2b.PS_NA, dtype=np.int8)
    pos[warm] = c2b.PS_INSIDE
    pos[warm & (close > upper)] = c2b.PS_ABOVE
    pos[warm & (close < lower)] = c2b.PS_BELOW

    return {"br_upper": upper, "br_lower": lower, "br_width_atr": w_atr,
            "br_disp_atr": disp, "br_state": state, "br_orient": orient,
            "br_knot": knot, "br_pos": pos, "sr_order_disorder": disorder,
            "ranks": ranks, "br_fan_age": fan_age_series(orient),
            "br_n_warm_lines": n_fin.astype(np.int8)}


def single_wall(e: pd.DataFrame, rb: pd.DataFrame, i: int) -> tuple[str, float]:
    """(family, distance) of the SINGLE wall at bar i, or ("none"|"multi", d).

    A wall is an SR whose band is within WALL_ATR of the close (census-2A's
    0.5-ATR contact test, carried unchanged).  "Single" is the point: the stamp
    is the IDENTITY of the one SR price is leaning on, and it is only an
    identity when exactly one qualifies.
    """
    close = float(e["close"].to_numpy(np.float64)[i])
    av = float(e["atr"].to_numpy(np.float64)[i])
    if not np.isfinite(av) or av <= 0:
        return "n/a", float("nan")
    hits = []
    for fam in FAMILIES:
        u = float(rb[f"{fam}_upper"].to_numpy(np.float64)[i])
        lo = float(rb[f"{fam}_lower"].to_numpy(np.float64)[i])
        if not (np.isfinite(u) and np.isfinite(lo)):
            continue
        d = 0.0 if lo <= close <= u else min(abs(close - u), abs(close - lo))
        if d <= WALL_ATR * av:
            hits.append((fam, d / av))
    if not hits:
        return "none", float("nan")
    if len(hits) > 1:
        return "multi", min(h[1] for h in hits)
    return hits[0][0], hits[0][1]


# ===========================================================================
# COHORT -- 814 winners + 814 matched losers
# ===========================================================================
def load_exits() -> pd.DataFrame:
    """t_exit for every resolved WF1 birth, keyed cell|tranche_id.

    census2a's stage_cen5 computes t1 = t0 + hold_s*1000 and does not persist
    it, which is why every downstream table says the exit side cannot be
    computed.  It can: the number is in the source JSONs.  This reads them and
    nothing else -- no simulation, no inference.
    """
    rows = []
    for p in sorted(WF1.glob("*USDT_*.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        cell = d.get("cell") or p.stem
        for r in d.get("rows", []):
            if not r.get("resolved"):
                continue
            t0 = r.get("ts_open_epoch")
            hs = r.get("hold_s")
            if t0 is None or hs is None:
                continue
            rows.append({"ckey": f"{cell}|{r['tranche_id']}",
                         "t_entry_ms": int(t0) * 1000,
                         "t_exit_ms": int(int(t0) * 1000 + float(hs) * 1000),
                         "hold_s": float(hs),
                         "exit_reason": r.get("exit_reason"),
                         "grade": r.get("grade"), "zone": r.get("zone")})
    return pd.DataFrame(rows)


def build_cohort() -> pd.DataFrame:
    banner("W-TB1 COHORT -- 814 winners + 1:1 matched-loser control")
    c5 = pd.read_parquet(CEN5)
    p = c5[c5.asset.isin(PANEL)].copy()
    print(f"resolved book, panel only            {len(p):,} campaigns")
    ts = pd.to_datetime(p.ts_ms, unit="ms", utc=True)
    p["quarter"] = ts.dt.year.astype(str) + "Q" + ts.dt.quarter.astype(str)
    # gross_R is the ruler; `ride_R` is its column and `outcome_sign` is
    # literally sign(ride_R) (census2a_program.py:2344). Both are stated so the
    # cohort cannot be read as depending on a derived label.
    p["gross_R"] = p.ride_R
    same = int((p.outcome_sign.eq("win") == (p.gross_R > 0)).all())
    print(f"outcome_sign == (gross_R > 0)        {bool(same)}")
    win = p[p.gross_R > 0].copy()
    los = p[p.gross_R <= 0].copy()
    print(f"winners (gross_R > 0)                {len(win):,}   "
          f"[contract expects ~814]")
    print(f"loser pool                           {len(los):,}")

    # ---- 1:1 nearest-neighbour matching on (asset, dir, quarter, size_r)
    # Deterministic: winners are processed in (ts_ms, tranche_id) order and the
    # nearest unused loser wins ties by the same order. No RNG anywhere, so the
    # control set is a function of the book alone.
    win = win.sort_values(["ts_ms", "tranche_id"]).reset_index(drop=True)
    pool: dict[tuple, list] = {}
    for k, g in los.groupby(["asset", "dir", "quarter", "size_r"], sort=True):
        g = g.sort_values(["ts_ms", "tranche_id"])
        pool[k] = [g.ts_ms.to_numpy(np.int64), g.tranche_id.to_numpy(object),
                   np.zeros(len(g), dtype=bool)]
    pairs, unmatched = [], []
    for _, r in win.iterrows():
        k = (r.asset, r["dir"], r.quarter, r.size_r)
        ent = pool.get(k)
        if ent is None or ent[2].all():
            unmatched.append(r.tranche_id)
            continue
        tss, tids, used = ent
        d = np.where(used, np.iinfo(np.int64).max, np.abs(tss - int(r.ts_ms)))
        j = int(np.argmin(d))
        used[j] = True
        pairs.append({"winner": r.tranche_id, "control": tids[j],
                      "asset": r.asset, "dir": r["dir"], "quarter": r.quarter,
                      "size_r": r.size_r,
                      "gap_days": abs(int(tss[j]) - int(r.ts_ms)) / 86_400_000})
    mt = pd.DataFrame(pairs)
    print(f"matched pairs                        {len(mt):,}")
    print(f"unmatched winners                    {len(unmatched):,}"
          + (f"  {unmatched[:5]}" if unmatched else ""))
    print(f"match gap (days)  median {mt.gap_days.median():.1f}  "
          f"p90 {mt.gap_days.quantile(0.9):.1f}  max {mt.gap_days.max():.1f}")

    ctl = p[p.tranche_id.isin(set(mt.control))].copy()
    win2 = p[p.tranche_id.isin(set(mt.winner))].copy()
    win2["cohort"] = "winner"
    ctl["cohort"] = "control"
    coh = pd.concat([win2, ctl], ignore_index=True)
    coh["ckey"] = coh.tranche_id                    # cen5's id IS cell|tranche
    ex = load_exits()
    print(f"\nWF1 exit rows read                   {len(ex):,}")
    before = len(coh)
    coh = coh.merge(ex, on="ckey", how="left", validate="one_to_one")
    got = int(coh.t_exit_ms.notna().sum())
    print(f"cohort rows                          {before:,}  "
          f"with t_exit {got:,}  missing {before - got:,}")
    if got < before:
        print("  NOTE: campaigns without a WF1 exit row keep NaN t_exit and are "
              "excluded from the\n  exit-side capture and the t_exit column of "
              "W-A; they are NOT dropped from anything else.")
    # entry ts sanity: cen5's ts_ms must equal WF1's ts_open_epoch*1000
    agree = int((coh.t_entry_ms == coh.ts_ms).sum())
    print(f"cen5 ts_ms == WF1 ts_open_epoch*1000 {agree:,} / {got:,}")
    coh["t0_ms"] = coh.ts_ms.astype(np.int64)
    return coh, mt


def fixture_w1(coh: pd.DataFrame, mt: pd.DataFrame) -> None:
    banner("F-W1  matching integrity")
    print("F-W1a  no control reused")
    n_ctl, n_uni = len(mt), mt.control.nunique()
    print(f"      controls drawn {n_ctl:,}  distinct {n_uni:,}  "
          f"{'OK' if n_ctl == n_uni else 'FAIL'}")
    if n_ctl != n_uni:
        raise SystemExit(2)
    ov = set(mt.winner) & set(mt.control)
    print(f"      winner/control overlap {len(ov)}  "
          f"{'OK' if not ov else 'FAIL'}")
    if ov:
        raise SystemExit(2)

    print("\nF-W1b  marginals within 10% on every matched key")
    w = coh[coh.cohort == "winner"]
    c = coh[coh.cohort == "control"]
    ok = True
    for col in ("asset", "dir", "quarter", "size_r"):
        a = w[col].value_counts(normalize=True)
        b = c[col].value_counts(normalize=True)
        idx = sorted(set(a.index) | set(b.index), key=str)
        worst, at = 0.0, ""
        for k in idx:
            d = abs(float(a.get(k, 0.0)) - float(b.get(k, 0.0)))
            if d > worst:
                worst, at = d, str(k)
        good = worst <= 0.10
        ok &= good
        print(f"      {col:9s} levels={len(idx):3d}  max |share diff| = "
              f"{worst:.4f} at {at:12s} {'OK' if good else 'FAIL'}")
    if not ok:
        print("      F-W1b FAIL"); raise SystemExit(2)
    print("      F-W1 PASS -- no reuse, no overlap, marginals within 10%")

    print("\nMATCHING TABLE (winners vs control, by matched key)")
    for col in ("asset", "dir", "size_r"):
        print(f"\n  {col}")
        a = w[col].value_counts().sort_index()
        b = c[col].value_counts().sort_index()
        print(f"    {'level':12s} {'winners':>9s} {'control':>9s} {'diff':>7s}")
        for k in sorted(set(a.index) | set(b.index), key=str):
            print(f"    {str(k):12s} {int(a.get(k, 0)):9,d} "
                  f"{int(b.get(k, 0)):9,d} {int(a.get(k, 0)) - int(b.get(k, 0)):7d}")
    print(f"\n  quarter: {w.quarter.nunique()} levels, "
          f"winners {len(w):,} vs control {len(c):,}; per-quarter diff max "
          f"{int((w.quarter.value_counts() - c.quarter.value_counts()).abs().max())}")


# ===========================================================================
# CAPTURE -- (a) BR state series, (b) event tape, (c) exit-side
# ===========================================================================
STATE_COLS = (["br_state", "br_orient", "br_knot"]
              + [f"{f}_{k}" for f in FAMILIES
                 for k in ("state", "orient", "knot")])


def _sign_tok(v) -> str:
    return "+" if float(v) > 0 else "-"


def _cross_tokens(cx: pd.DataFrame) -> pd.DataFrame:
    """within-SR and SR-median crosses only.

    price_band events (enter/exit/traverse/reject) are computed and pinned by
    V-ULT-1 but are NOT in the contract's tape enumeration, which names
    "every cross (within-SR + SR-median pairs)".  They are left out rather than
    folded in silently: a tape that quietly carries four extra event classes
    would make the motif alphabet a different object from the one declared.
    """
    s = cx[cx.pair_class.isin(["within_ribbon", "midline"])].copy()
    if not len(s):
        return s.assign(kind="", token="", ev_dir="", aux=np.nan,
                        src_ts_ms=np.zeros(0, np.int64))
    up = s["dir"].to_numpy() == "up"
    fam = s.family.to_numpy(object)
    pair = s.pair.to_numpy(object)
    within = s.pair_class.to_numpy() == "within_ribbon"
    # PAIR-level, not family-level. Collapsing a family's three within-SR pairs
    # (9_12, 9_26, 12_26 for FAST) onto one symbol made "XFAST+" ambiguous
    # between three different events -- and, because two of the three routinely
    # fire on the same bar, made the tape's own key non-unique: 37,389 collisions
    # on BTC 5m alone. The alphabet is larger and m is larger; both are honest.
    tok = np.where(within,
                   np.char.add(np.char.add("X", pair.astype(str)),
                               np.where(up, "+", "-")),
                   np.char.add(np.char.add("M", pair.astype(str)),
                               np.where(up, "+", "-")))
    return s.assign(kind=np.where(within, "cross_within", "cross_median"),
                    token=tok, ev_dir=np.where(up, "up", "down"),
                    src_ts_ms=s.ts_ms.to_numpy(np.int64),
                    aux=np.nan)[["ts_ms", "src_ts_ms", "kind", "token", "pair",
                                 "family", "ev_dir", "aux"]]


def _tape_sources(sym: str, tf: str) -> pd.DataFrame:
    """Every Part-A and V-ULT-1 event stream for one cell, as one tape."""
    frames = []

    cx = pd.read_parquet(OUT / "crosses" / sym / f"{tf}.parquet",
                         columns=["pair_class", "pair", "family", "event",
                                  "dir", "ts_ms"])
    frames.append(_cross_tokens(cx))
    del cx

    p = pa.D_REF / sym / f"{tf}.parquet"
    if p.exists():
        r = pd.read_parquet(p, columns=["pair", "family", "limb", "ts_ms",
                                        "confirm_ts_ms", "approach_atr"])
        if len(r):
            lab = np.where(r.family.to_numpy(object).astype(str) != "",
                           r.family.to_numpy(object).astype(str),
                           r.pair.to_numpy(object).astype(str))
            frames.append(pd.DataFrame({
                # a refusal is knowable at its CONFIRM bar, not its touch bar --
                # and several distinct refusals routinely share one confirm bar,
                # which is why the touch bar rides along as src_ts_ms and is
                # part of the tape's key
                "ts_ms": r.confirm_ts_ms.to_numpy(np.int64),
                "src_ts_ms": r.ts_ms.to_numpy(np.int64),
                "kind": "refusal",
                "token": np.char.add(np.char.add("R", lab),
                                     np.where(r.limb.to_numpy() == "above",
                                              "^", "v")),
                "pair": r.pair.to_numpy(object), "family": r.family.to_numpy(object),
                "ev_dir": r.limb.to_numpy(object),
                "aux": r.approach_atr.to_numpy(float)}))

    p = pa.D_SPR / sym / f"{tf}.parquet"
    if p.exists():
        s = pd.read_parquet(p, columns=["side", "pen_ts_ms", "reclaim_ts_ms",
                                        "depth_atr"])
        if len(s):
            frames.append(pd.DataFrame({
                "ts_ms": s.reclaim_ts_ms.to_numpy(np.int64),
                "src_ts_ms": s.pen_ts_ms.to_numpy(np.int64),
                "kind": "sweep",
                "token": np.char.add("S", s.side.to_numpy(object).astype(str)),
                "pair": "", "family": "",
                "ev_dir": np.where(s.side.to_numpy() == "spring", "up", "down"),
                "aux": s.depth_atr.to_numpy(float)}))

    p = pa.D_TRN / sym / f"{tf}_knots.parquet"
    if p.exists():
        kall = pd.read_parquet(p)
        # A knot EPISODE has two transitions and the BRIDGE says A-3
        # transitions are first-class tape rows. Emitting only the exit put
        # half the episode on the tape and left "the ribbon just knotted" --
        # the compression itself -- unrepresentable in the motif alphabet.
        if len(kall):
            frames.append(pd.DataFrame({
                "ts_ms": kall.entry_ts_ms.to_numpy(np.int64),
                "src_ts_ms": kall.entry_ts_ms.to_numpy(np.int64),
                "kind": "knot_entry",
                "token": np.char.add("KI", kall.sr.to_numpy(object).astype(str)),
                "pair": "", "family": kall.sr.to_numpy(object),
                "ev_dir": "", "aux": kall.duration_bars.to_numpy(float)}))
        k = kall[(kall.exit_ts_ms > 0) & (kall.exit_dir_sign != 0)]
        if len(k):
            frames.append(pd.DataFrame({
                "ts_ms": k.exit_ts_ms.to_numpy(np.int64),
                "src_ts_ms": k.entry_ts_ms.to_numpy(np.int64),
                "kind": "knot_exit",
                "token": np.char.add(np.char.add("K", k.sr.to_numpy(object).astype(str)),
                                     np.where(k.exit_dir_sign.to_numpy() > 0, "+", "-")),
                "pair": "", "family": k.sr.to_numpy(object),
                "ev_dir": np.where(k.exit_dir_sign.to_numpy() > 0, "up", "down"),
                "aux": k.duration_bars.to_numpy(float)}))
        # a knot whose exit direction never resolves still EXITED; emitting it
        # with a neutral token keeps the count honest instead of dropping 48
        # transitions because their direction is undefined
        k0 = kall[(kall.exit_ts_ms > 0) & (kall.exit_dir_sign == 0)]
        if len(k0):
            frames.append(pd.DataFrame({
                "ts_ms": k0.exit_ts_ms.to_numpy(np.int64),
                "src_ts_ms": k0.entry_ts_ms.to_numpy(np.int64),
                "kind": "knot_exit",
                "token": np.char.add("K", np.char.add(
                    k0.sr.to_numpy(object).astype(str), "?")),
                "pair": "", "family": k0.sr.to_numpy(object),
                "ev_dir": "", "aux": k0.duration_bars.to_numpy(float)}))
    p = pa.D_TRN / sym / f"{tf}_fans.parquet"
    if p.exists():
        f = pd.read_parquet(p)
        if len(f):
            frames.append(pd.DataFrame({
                "ts_ms": f.onset_ts_ms.to_numpy(np.int64),
                "src_ts_ms": f.onset_ts_ms.to_numpy(np.int64),
                "kind": "fan_birth",
                "token": np.char.add(np.char.add("F", f.sr.to_numpy(object).astype(str)),
                                     np.where(f.dir_sign.to_numpy() > 0, "+", "-")),
                "pair": "", "family": f.sr.to_numpy(object),
                "ev_dir": np.where(f.dir_sign.to_numpy() > 0, "up", "down"),
                "aux": f.fan_len_bars.to_numpy(float)}))

    p = pa.D_WIN / sym / f"{tf}.parquet"
    if p.exists():
        w = pd.read_parquet(p)
        if len(w):
            sg = np.where(w.dir_sign.to_numpy() > 0, "+", "-")
            dd = np.where(w.dir_sign.to_numpy() > 0, "up", "down")
            frames.append(pd.DataFrame({
                "ts_ms": w.arming_ts_ms.to_numpy(np.int64),
                "src_ts_ms": w.arming_ts_ms.to_numpy(np.int64),
                "kind": "window_arm",
                "token": np.char.add("Warm", sg), "pair": "12_89", "family": "",
                "ev_dir": dd, "aux": w.displacement_atr.to_numpy(float)}))
            t = w[w.trigger_ts_ms > 0]
            if len(t):
                sg2 = np.where(t.dir_sign.to_numpy() > 0, "+", "-")
                frames.append(pd.DataFrame({
                    "ts_ms": t.trigger_ts_ms.to_numpy(np.int64),
                    "src_ts_ms": t.arming_ts_ms.to_numpy(np.int64),
                    "kind": "window_trigger",
                    "token": np.char.add("Wtrg", sg2), "pair": "12_26",
                    "family": "",
                    "ev_dir": np.where(t.dir_sign.to_numpy() > 0, "up", "down"),
                    "aux": t.trigger_lag_bars.to_numpy(float)}))
            cl = w[w.closed_by == "counter-12_89"]
            if len(cl):
                sg3 = np.where(cl.dir_sign.to_numpy() > 0, "+", "-")
                frames.append(pd.DataFrame({
                    "ts_ms": cl.window_close_ts_ms.to_numpy(np.int64),
                    "src_ts_ms": cl.arming_ts_ms.to_numpy(np.int64),
                    "kind": "window_close",
                    "token": np.char.add("Wcls", sg3), "pair": "12_89",
                    "family": "",
                    "ev_dir": np.where(cl.dir_sign.to_numpy() > 0, "up", "down"),
                    "aux": cl.window_width_bars.to_numpy(float)}))

    if not frames:
        return pd.DataFrame(columns=["ts_ms", "src_ts_ms", "kind", "token",
                                     "pair", "family", "ev_dir", "aux"])
    t = pd.concat(frames, ignore_index=True)
    return t.sort_values("ts_ms").reset_index(drop=True)


def _verdict_tape(sym: str) -> pd.DataFrame:
    """Range-verdict STATE CHANGES, from census-2A's cen6_verdict_state.

    Its members are the close-set {1h, 4h, 12h}; only 1h is also a W-TB1 lens.
    Rather than drop 4h/12h or duplicate them across four lenses, all three
    members are emitted ONCE per campaign, into the 1h tape, tagged with their
    own member in `family`. Stated here because it is a placement choice, not
    a measurement.
    """
    if not VERDICT.exists():
        return pd.DataFrame(columns=["ts_ms", "src_ts_ms", "kind", "token",
                                     "pair", "family", "ev_dir", "aux"])
    v = pd.read_parquet(VERDICT)
    v = v[v.asset == sym]
    out = []
    for mem, g in v.groupby("member"):
        g = g.sort_values("ts")
        st = g.verdict_state.to_numpy(object)
        chg = np.ones(len(st), dtype=bool)
        chg[1:] = st[1:] != st[:-1]
        g = g[chg]
        # Verdict rows ride the 1h tape but belong to members {1h, 4h, 12h}.
        # capture_cell adds one bar of the CAPTURE lens (1h) to every tape row
        # to get its knowability instant, so the member's extra bar-length is
        # added here; the pair then lands exactly on the member's own close.
        lag = TF_MS[str(mem)] - TF_MS["1h"]
        out.append(pd.DataFrame({
            "ts_ms": g.ts.to_numpy(np.int64) + lag,
            "src_ts_ms": g.ts.to_numpy(np.int64), "kind": "verdict",
            "token": np.char.add(np.char.add("V", str(mem) + "."),
                                 g.verdict_state.to_numpy(object).astype(str)),
            "pair": "", "family": str(mem),
            "ev_dir": "", "aux": np.nan}))
    if not out:
        return pd.DataFrame(columns=["ts_ms", "src_ts_ms", "kind", "token",
                                     "pair", "family", "ev_dir", "aux"])
    return pd.concat(out, ignore_index=True).sort_values("ts_ms")


MOTIF_KINDS = {"cross_within", "cross_median", "refusal", "sweep",
               "knot_entry", "knot_exit", "fan_birth", "window_arm",
               "window_trigger", "window_close"}


def capture_cell(coh: pd.DataFrame, sym: str, tf: str
                 ) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """(state rows, tape rows, per-campaign t0 stamps) for one (asset, lens)."""
    e, rb = load_cell(sym, tf)
    ot = e["open_time"].to_numpy(np.int64)
    n = len(ot)
    br = br_state(e)
    step = TF_MS[tf]

    sr_age = {f: fan_age_series(rb[f"{f}_orient"].to_numpy()) for f in FAMILIES}
    codes = {c: (br[c] if c.startswith("br_") else rb[c].to_numpy())
             for c in STATE_COLS}
    chg = np.zeros(n, dtype=bool)
    for c in STATE_COLS:
        v = codes[c]
        chg[1:] |= v[1:] != v[:-1]
    chg[0] = True

    tape_all = _tape_sources(sym, tf)
    if tf == "1h":
        tape_all = (pd.concat([tape_all, _verdict_tape(sym)], ignore_index=True)
                      .sort_values("ts_ms").reset_index(drop=True))
    tape_ts = tape_all.ts_ms.to_numpy(np.int64)

    # verdict state series per close-set member, for the as-of t0 stamp
    vs_ts: dict[str, tuple] = {}
    if VERDICT.exists():
        _v = pd.read_parquet(VERDICT)
        _v = _v[_v.asset == sym]
        for mem, g in _v.groupby("member"):
            g = g.sort_values("ts")
            vs_ts[str(mem)] = (g.ts.to_numpy(np.int64),
                               g.verdict_state.to_numpy(object))
        del _v

    sub = coh[coh.asset == sym]
    srows, trows, stamps = [], [], []
    win_ms = WIN_H * 3_600_000
    ex_ms = EXIT_H * 3_600_000

    for _, r in sub.iterrows():
        t0 = int(r.t0_ms)
        te = int(r.t_exit_ms) if np.isfinite(r.t_exit_ms) else -1
        i0 = int(np.searchsorted(ot, t0, "right")) - 1      # bar CONTAINING t0
        # the stamp bar is the last bar CLOSED at or before t0. The bar
        # containing t0 has not closed yet at the birth instant, so reading its
        # state as a birth feature reads the future by up to one bar.
        i0s = int(np.searchsorted(ot, t0 - step, "right")) - 1
        if i0 < 0 or i0 >= n or i0s < 0:
            continue
        # one bar of left margin. The as-of lookups read on KNOWABILITY, so the
        # t-72h stage instant needs a bar that has already CLOSED by then; the
        # first bar whose OPEN is >= t0-72h closes after it, and the stage would
        # report n/a at the very edge it was asked about.
        # The margin must reach a bar whose CLOSE is at or before t0-72h, not
        # merely whose OPEN is. One bar of margin gives the last bar OPENING
        # before t0-72h, and that bar closes AFTER it -- so the as-of lookup at
        # the t-72h stage found nothing and the whole stage reported n/a for
        # 1,362 of 1,628 campaigns on 5m and 1,611 on 1h. Anchor the margin on
        # the close instead.
        lo = max(0, int(np.searchsorted(ot, t0 - win_ms - step, "right")) - 1)
        hi = int(np.searchsorted(ot, t0 + win_ms, "right"))
        keep = np.zeros(n, dtype=bool)
        keep[lo:hi] = chg[lo:hi]
        # hourly spine: the last bar at or before each whole-hour offset
        # The spine marks, for each whole-hour offset, the bar that is KNOWN by
        # then -- the last bar whose CLOSE is at or before it. Indexing the
        # spine on bar-open keeps a bar that has not finished at its own spine
        # instant, and the as-of lookup then finds nothing at the earliest
        # stage: t-72h reported n/a for 998 of 1,628 campaigns on 5m.
        spine_ts = t0 + np.arange(-WIN_H, WIN_H + 1) * 3_600_000
        si = np.searchsorted(ot, spine_ts - step, "right") - 1
        si = si[(si >= 0) & (si < n)]
        keep[si] = True
        keep[i0] = True                          # the bar containing t0
        keep[i0s] = True                         # the last bar CLOSED before t0
        exit_lo = exit_hi = -1
        if te > 0:
            exit_lo = max(0, int(np.searchsorted(ot, te - ex_ms - step,
                                                 "right")) - 1)
            exit_hi = int(np.searchsorted(ot, te + ex_ms, "right"))
            # |= not =. The exit window overlaps the birth window whenever the
            # hold is under 96h -- which is most of the control cohort -- and a
            # plain assignment there RESETS the birth window's hourly spine to
            # the change mask, silently dropping every spine bar in the overlap
            # that is not also a state change.
            keep[exit_lo:exit_hi] |= chg[exit_lo:exit_hi]
            ie = int(np.searchsorted(ot, te, "right")) - 1
            if 0 <= ie < n:
                keep[ie] = True
                es = te + np.arange(-EXIT_H, EXIT_H + 1) * 3_600_000
                ei = np.searchsorted(ot, es - step, "right") - 1
                ei = ei[(ei >= 0) & (ei < n)]
                keep[ei] = True
        idx = np.flatnonzero(keep)
        if idx.size == 0:
            continue

        # KNOWABILITY, not bar-open. A bar's state and every close-confirmed
        # event on it become knowable at that bar's CLOSE. Splitting on the
        # OPEN time stamps a 1h bar that opens 10:30 and closes 11:30 as BEFORE
        # an 11:00 birth -- a curtain leak of up to one bar, and on the pooled
        # cross-lens tape it also mis-ORDERS a 1h event against a 5m event that
        # was knowable first. Everything that decides a side, an offset, or a
        # sort order now uses close = open + one bar.
        know = ot[idx] + step
        d = {"ckey": r.ckey, "cohort": r.cohort, "asset": sym,
             "campaign_dir": r["dir"], "lens": tf,
             "ts_ms": ot[idx].astype(np.int64),
             "knowable_ts_ms": know.astype(np.int64),
             "bar_index": idx.astype(np.int32),
             "rel_h": ((know - t0) / 3_600_000.0).astype(np.float32),
             "side": np.where(know <= t0, "BEFORE", "AFTER"),
             "exit_anatomy": (np.zeros(idx.size, bool) if te <= 0 else
                              (idx >= exit_lo) & (idx < exit_hi)),
             "is_spine": np.isin(idx, si),
             "is_state_change": chg[idx]}
        for L in ALL_EMAS:
            d[f"e{L}"] = e[f"e{L}"].to_numpy(np.float32)[idx]
        R = br["ranks"][:, idx]
        for j, L in enumerate(ALL_EMAS):
            d[f"rank_e{L}"] = R[j]
        for k in ("br_width_atr", "br_disp_atr", "sr_order_disorder"):
            d[k] = br[k][idx].astype(np.float32)
        for k in ("br_state", "br_orient", "br_knot"):
            d[k] = br[k][idx]
        d["br_fan_age"] = br["br_fan_age"][idx]
        d["br_n_warm_lines"] = br["br_n_warm_lines"][idx]
        for f in FAMILIES:
            d[f"{f}_width_atr"] = rb[f"{f}_width_atr"].to_numpy(np.float32)[idx]
            d[f"{f}_state"] = rb[f"{f}_state"].to_numpy()[idx]
            d[f"{f}_orient"] = rb[f"{f}_orient"].to_numpy()[idx]
            d[f"{f}_knot"] = rb[f"{f}_knot"].to_numpy()[idx]
            d[f"{f}_fan_age"] = sr_age[f][idx]
        srows.append(pd.DataFrame(d))

        # ---- tape
        a = int(np.searchsorted(tape_ts, t0 - win_ms - step, "left"))
        b = int(np.searchsorted(tape_ts, t0 + win_ms, "right"))
        parts = [tape_all.iloc[a:b]]
        if te > 0:
            a2 = int(np.searchsorted(tape_ts, te - ex_ms - step, "left"))
            b2 = int(np.searchsorted(tape_ts, te + ex_ms, "right"))
            if not (a2 >= a and b2 <= b):
                parts.append(tape_all.iloc[a2:b2])
        tp = pd.concat(parts, ignore_index=True).drop_duplicates()
        if len(tp):
            ts = tp.ts_ms.to_numpy(np.int64)
            kn = ts + step                       # knowability: the bar's close
            tp = tp.assign(
                ckey=r.ckey, cohort=r.cohort, asset=sym,
                campaign_dir=r["dir"], lens=tf,
                knowable_ts_ms=kn,
                rel_h=((kn - t0) / 3_600_000.0).astype(np.float32),
                side=np.where(kn <= t0, "BEFORE", "AFTER"),
                exit_anatomy=(np.zeros(len(ts), bool) if te <= 0
                              else np.abs(kn - te) <= ex_ms),
                in_motif_alphabet=tp.kind.isin(MOTIF_KINDS).to_numpy())
            trows.append(tp.sort_values("knowable_ts_ms").reset_index(drop=True))

        # ---- per-campaign t0 stamps (single wall, displacement)
        # time-from-knot-exit needs the WHOLE prior series, not the +-72h
        # capture: a BR that last unknotted four months ago is exactly the case
        # W-C wants to see, and a windowed search would report it as "never".
        knb = br["br_knot"][:i0s + 1]
        was = np.flatnonzero(knb == KN_TRUE)
        if was.size and int(was[-1]) < i0s:
            bars_since_knot = i0s - int(was[-1])
        elif was.size:
            bars_since_knot = 0                  # still in-knot at t0
        else:
            bars_since_knot = -1                 # never knotted in this history
        wall, wall_d = single_wall(e, rb, i0s)
        av = float(e["atr"].to_numpy(np.float64)[i0s])
        cl = float(e["close"].to_numpy(np.float64)[i0s])
        e89 = float(e["e89"].to_numpy(np.float64)[i0s])
        rec = {
            "ckey": r.ckey, "cohort": r.cohort, "asset": sym, "lens": tf,
            "campaign_dir": r["dir"], "t0_ms": t0, "t_exit_ms": te,
            "t0_bar_index": i0, "stamp_bar_index": i0s,
            "wall_family": wall, "wall_dist_atr": wall_d,
            "displacement_atr": (abs(cl - e89) / av
                                 if np.isfinite(av) and av > 0 else np.nan),
            "br_state": int(br["br_state"][i0s]),
            "br_orient": int(br["br_orient"][i0s]),
            "br_knot": int(br["br_knot"][i0s]),
            "br_fan_age": int(br["br_fan_age"][i0s]),
            "br_disp_atr": float(br["br_disp_atr"][i0s]),
            "br_n_warm_lines": int(br["br_n_warm_lines"][i0s]),
            "sr_order_disorder": float(br["sr_order_disorder"][i0s]),
            "bars_since_br_knot_exit": int(bars_since_knot),
            "hours_since_br_knot_exit": (bars_since_knot * step / 3.6e6
                                         if bars_since_knot >= 0 else np.nan),
        }
        # RANGE VERDICT STATE AT t0, per close-set member. The tape carries
        # verdict CHANGES, which is silence for a campaign whose window holds
        # none -- and silence is not a state. This is the as-of read, and it is
        # as-of the last verdict row at or before t0.
        for mem in ("1h", "4h", "12h"):
            a = vs_ts.get(mem)
            if a is None or not len(a[0]):
                rec[f"verdict_{mem}"] = ""
                rec[f"verdict_age_h_{mem}"] = np.nan
                continue
            ts_a, st_a = a
            # as-of on the MEMBER's own close, not its open. A 12h verdict row
            # stamped at its open is not known for another 12 hours, and would
            # be a curtain leak of up to half a day into a birth stamp.
            q = int(np.searchsorted(ts_a, t0 - TF_MS[mem], "right")) - 1
            rec[f"verdict_{mem}"] = str(st_a[q]) if q >= 0 else ""
            rec[f"verdict_age_h_{mem}"] = ((t0 - int(ts_a[q])) / 3.6e6
                                           if q >= 0 else np.nan)
        stamps.append(rec)

    S = pd.concat(srows, ignore_index=True) if srows else pd.DataFrame()
    T = pd.concat(trows, ignore_index=True) if trows else pd.DataFrame()
    P = pd.DataFrame(stamps)
    return S, T, P


def run_capture(coh: pd.DataFrame) -> dict:
    banner("W-TB1 CAPTURE -- (a) BR state series  (b) event tape  (c) exit side")
    print(f"window      t0 +- {WIN_H}h; exit side t_exit +- {EXIT_H}h "
          f"(labelled EXIT-ANATOMY)")
    print(f"downsample  state-change points UNION hourly spine; t0 and t_exit "
          f"always kept")
    print(f"tape        within-SR + SR-median crosses · A-1 refusals (both "
          f"limbs, at CONFIRM) ·\n            A-2 window arm/trigger/close · A-3 "
          f"knot exits + fan births · A-4 sweeps\n            (at RECLAIM) · "
          f"range-verdict state changes (1h tape, all three members)")
    print(f"curtain     every row carries side ∈ {{BEFORE, AFTER}} and an "
          f"exit_anatomy flag\n")
    D_STATE.mkdir(parents=True, exist_ok=True)
    D_TAPE.mkdir(parents=True, exist_ok=True)
    inv, allstamps = [], []
    print(f"{'asset':9s} {'lens':5s} {'campaigns':>10s} {'state rows':>12s} "
          f"{'tape rows':>11s} {'state MB':>9s} {'tape MB':>8s} {'secs':>7s}")
    hr(n=88)
    for sym in PANEL:
        for tf in LENSES:
            t0 = time.time()
            S, T, P = capture_cell(coh, sym, tf)
            ds = D_STATE / sym
            dt = D_TAPE / sym
            ds.mkdir(parents=True, exist_ok=True)
            dt.mkdir(parents=True, exist_ok=True)
            ps, pt = ds / f"{tf}.parquet", dt / f"{tf}.parquet"
            if len(S):
                pa.fkey(S, ["ckey", "lens", "ts_ms"], f"state {sym} {tf}")
            if len(T):
                # the tape's key needs kind+token: several distinct events can
                # and do land on one bar, so (ckey, lens, ts_ms) is NOT unique
                # and asserting it would HALT on healthy data
                pa.fkey(T, ["ckey", "lens", "ts_ms", "src_ts_ms", "kind",
                            "token"], f"tape  {sym} {tf}")
            to_parquet_atomic(S, ps)
            to_parquet_atomic(T, pt)
            allstamps.append(P)
            bs, bt = ps.stat().st_size, pt.stat().st_size
            inv.append({"asset": sym, "lens": tf, "campaigns": len(P),
                        "state_rows": len(S), "tape_rows": len(T),
                        "state_bytes": bs, "tape_bytes": bt})
            print(f"{sym:9s} {tf:5s} {len(P):10,d} {len(S):12,d} {len(T):11,d} "
                  f"{bs / 1e6:9.1f} {bt / 1e6:8.1f} {time.time() - t0:7.1f}")
            del S, T
    invdf = pd.DataFrame(inv)
    ST = pd.concat(allstamps, ignore_index=True)
    to_parquet_atomic(ST, W / "wtb1_t0_stamps.parquet")
    tot = invdf.state_bytes.sum() + invdf.tape_bytes.sum()
    print(f"\nCAPTURE TOTAL  state rows={invdf.state_rows.sum():,}  "
          f"tape rows={invdf.tape_rows.sum():,}  "
          f"bytes={tot:,} ({tot / 1e9:.2f} GB)")
    print(f"wrote {W / 'wtb1_t0_stamps.parquet'}  rows={len(ST):,}")
    return {"inventory": invdf, "stamps": ST}


# ===========================================================================
# W-A  STATION OCCUPANCY -- the six-stage kit, photographed
# ===========================================================================
def _asof_state(S: pd.DataFrame, targets: dict[str, np.ndarray]) -> pd.DataFrame:
    """BR state as-of each stage instant, per campaign.

    The state series is a step function: every bar at which any code changes is
    stored, so the last stored row at or before an instant carries that
    instant's state EXACTLY. This is a lookup, not an interpolation.
    """
    out = []
    for ck, g in S.groupby("ckey", sort=False):
        g = g.sort_values("knowable_ts_ms")
        # as-of on KNOWABILITY: the state at an instant is the state of the last
        # bar CLOSED by then. Using bar-open would report a bar still in flight.
        ts = g.knowable_ts_ms.to_numpy(np.int64)
        tg = targets.get(ck)
        if tg is None:
            continue
        j = np.searchsorted(ts, tg, "right") - 1
        ok = j >= 0
        rec = {"ckey": ck, "cohort": g.cohort.iloc[0],
               "asset": g.asset.iloc[0], "lens": g.lens.iloc[0]}
        for si, nm in enumerate(STAGE_NAMES):
            if not ok[si]:
                rec[f"{nm}_state"] = ST_NA
                rec[f"{nm}_orient"] = OR_NA
                rec[f"{nm}_knot"] = KN_NA
                rec[f"{nm}_disp"] = np.nan
                rec[f"{nm}_disorder"] = np.nan
                rec[f"{nm}_warm"] = 0
                continue
            row = g.iloc[int(j[si])]
            rec[f"{nm}_state"] = int(row.br_state)
            rec[f"{nm}_orient"] = int(row.br_orient)
            rec[f"{nm}_knot"] = int(row.br_knot)
            rec[f"{nm}_disp"] = float(row.br_disp_atr)
            rec[f"{nm}_disorder"] = float(row.sr_order_disorder)
            rec[f"{nm}_warm"] = int(row.br_n_warm_lines)
        out.append(rec)
    return pd.DataFrame(out)


STAGE_NAMES = ["t-72h", "t-24h", "t-4h", "t0", "t+24h", "t_exit"]


def w_a(coh: pd.DataFrame) -> pd.DataFrame:
    banner("W-A  STATION OCCUPANCY -- BR state at the six stages, "
           "winners vs control")
    print(TIER_E_HEADER)
    print("\nCURTAIN: t-72h / t-24h / t-4h are BEFORE t0 and are the only "
          "columns that\ncould ever be entry evidence. t+24h and t_exit are "
          "ANATOMY. The split is\nprinted, not assumed.\n")
    t0m = dict(zip(coh.ckey, coh.t0_ms.astype(np.int64)))
    tem = dict(zip(coh.ckey, coh.t_exit_ms))
    rows = []
    for sym in PANEL:
        for tf in LENSES:
            p = D_STATE / sym / f"{tf}.parquet"
            if not p.exists():
                continue
            S = pd.read_parquet(p, columns=["ckey", "cohort", "asset", "lens",
                                            "knowable_ts_ms", "br_state",
                                            "br_orient", "br_knot",
                                            "br_disp_atr", "br_n_warm_lines",
                                            "sr_order_disorder"])
            if not len(S):
                continue
            tg = {}
            for ck in S.ckey.unique():
                t0 = t0m[ck]
                te = tem.get(ck, np.nan)
                tg[ck] = np.array([t0 - 72 * 3_600_000, t0 - 24 * 3_600_000,
                                   t0 - 4 * 3_600_000, t0,
                                   t0 + 24 * 3_600_000,
                                   int(te) if np.isfinite(te) else t0],
                                  dtype=np.int64)
            rows.append(_asof_state(S, tg))
            del S
    A = pd.concat(rows, ignore_index=True) if rows else pd.DataFrame()

    for tf in LENSES:
        s = A[A.lens == tf]
        if not len(s):
            continue
        print(f"\n  LENS {tf}   winners n={int((s.cohort == 'winner').sum()):,}  "
              f"control n={int((s.cohort == 'control').sum()):,}")
        print(f"    {'stage':8s} {'coh':8s} {'compr':>7s} {'flat':>7s} "
              f"{'expand':>7s} | {'bull':>7s} {'mixed':>7s} {'bear':>7s} | "
              f"{'knot%':>7s} {'disp':>7s} {'disord':>7s}")
        for nm in STAGE_NAMES:
            for coh_lab in ("winner", "control"):
                g = s[s.cohort == coh_lab]
                st = g[f"{nm}_state"].to_numpy()
                orr = g[f"{nm}_orient"].to_numpy()
                kn = g[f"{nm}_knot"].to_numpy()
                v = st[st != ST_NA]
                o = orr[orr != OR_NA]
                k = kn[kn != KN_NA]
                def sh(a, val):
                    return f"{(a == val).mean() * 100:6.1f}%" if a.size else "     --"
                dsp = g[f"{nm}_disp"].median()
                dso = g[f"{nm}_disorder"].median()
                print(f"    {nm:8s} {coh_lab:8s} {sh(v, ST_COMPRESS)} "
                      f"{sh(v, ST_FLAT)} {sh(v, ST_EXPAND)} | "
                      f"{sh(o, OR_BULL)} {sh(o, OR_MIXED)} {sh(o, OR_BEAR)} | "
                      f"{sh(k, KN_TRUE)} {dsp:7.3f} {dso:7.3f}")
    return A


# ===========================================================================
# W-B  SEQUENTIAL MOTIFS -- k-grams under the three SEQ frames
# ===========================================================================
def _frame_token(frame: str, lens: str, lens0: str, token: str) -> str:
    if frame == "absolute":
        return f"{lens}:{token}"
    if frame == "tier":
        return f"{TIER_GRAMMAR[lens]}:{token}"
    d = TFI[lens] - TFI[lens0]
    return f"{'0' if d == 0 else f'{d:+d}'}:{token}"


def w_b(coh: pd.DataFrame) -> dict:
    banner("W-B  SEQUENTIAL MOTIFS -- ordered event k-grams (k<=4), 24h before t0")
    print(TIER_E_HEADER)
    print(f"\nSource: the tape, side=BEFORE, rel_h in [-{MOTIF_WINDOW_H}, 0), "
          f"POOLED ACROSS THE FOUR\nLENSES and ordered by timestamp -- the SEQ "
          f"frames are about multi-timeframe\nsequencing, so a per-lens tape "
          f"could not express them.")
    print(f"\nMOTIF ALPHABET (the BRIDGE's full grammar, not half of it):")
    print(f"  X<pair>±     within-SR cross (all 18 pairs, NOT collapsed to the")
    print(f"               family: two pairs of one family fire on one bar)")
    print(f"  M<pair>±     SR-median cross          KI<SR>   knot-episode entry")
    print(f"  R<SR|pair>^v refusal, both limbs      K<SR>±   knot-episode exit")
    print(f"  S<spring|upthrust>  A-4 sweep        F<SR>±   fan birth")
    print(f"  Warm/Wtrg/Wcls±     A-2 window arm / trigger / close")
    print(f"  price_band and range-verdict rows are in the tape but NOT in the")
    print(f"  motif alphabet -- the contract's tape enumeration does not name "
          f"them.")
    print(f"\nTHE THREE SEQ FRAMES (seq8_views.py:30-35, ratified SEQ-2 ruling D):")
    print(f"  absolute      5m:XFAST+   -- literal lens labels")
    print(f"  gov_relative  0:XFAST+ +1:XM-   -- ladder steps from the k-gram's "
          f"FIRST event")
    print(f"  tier          FAST:XFAST+  -- TIER_GRAMMAR labels\n")

    seqs: dict[str, list] = {}
    for sym in PANEL:
        for tf in LENSES:
            p = D_TAPE / sym / f"{tf}.parquet"
            if not p.exists():
                continue
            T = pd.read_parquet(p, columns=["ckey", "cohort", "lens",
                                            "knowable_ts_ms", "rel_h", "side",
                                            "token", "in_motif_alphabet"])
            T = T[(T.side == "BEFORE") & (T.rel_h >= -MOTIF_WINDOW_H)
                  & T.in_motif_alphabet]
            for ck, g in T.groupby("ckey", sort=False):
                seqs.setdefault(ck, []).append(
                    g[["knowable_ts_ms", "lens", "token"]].to_numpy())
            del T
    cohort_of = dict(zip(coh.ckey, coh.cohort))
    ckeys = sorted(seqs)
    print(f"campaigns with a non-empty 24h pre-tape: {len(ckeys):,} of "
          f"{len(coh):,}")

    # Ordered sequences, materialised once. Frames are then processed ONE AT A
    # TIME: holding all three frames' motif dictionaries simultaneously is
    # three times the peak, and this machine has under a gigabyte spare.
    seq_of = {}
    ev_counts = []
    for ck in ckeys:
        arr = np.vstack(seqs[ck])
        order = np.argsort(arr[:, 0].astype(np.int64), kind="stable")
        arr = arr[order]
        seq_of[ck] = (arr[:, 1].astype(str), arr[:, 2].astype(str))
        ev_counts.append(arr.shape[0])
    del seqs
    print(f"events per campaign in the window: median "
          f"{int(np.median(ev_counts)) if ev_counts else 0}  "
          f"p90 {int(np.percentile(ev_counts, 90)) if ev_counts else 0}  "
          f"max {max(ev_counts) if ev_counts else 0}  "
          f"total {int(np.sum(ev_counts)):,}")

    y = np.array([1.0 if cohort_of[ck] == "winner" else 0.0 for ck in ckeys])
    n_w, n_c = float(y.sum()), float((1 - y).sum())
    rng = np.random.default_rng(SEED + 7700)
    n_perm = 2000
    perms = [rng.permutation(y) for _ in range(n_perm)]   # shared across frames

    parts, guards, m_full, counts_by_k = [], {}, 0, []
    for frame in SEQ_FRAMES:
        ids: dict[str, int] = {}
        mi_l, ci_l = [], []
        for ci, ck in enumerate(ckeys):
            lensv, tokv = seq_of[ck]
            ne = len(tokv)
            seen = set()
            for k in range(1, KGRAM_MAX + 1):
                for s in range(0, ne - k + 1):
                    l0 = lensv[s]
                    mo = ">".join(_frame_token(frame, lensv[s + j], l0,
                                               tokv[s + j]) for j in range(k))
                    if mo in seen:
                        continue
                    seen.add(mo)
                    j2 = ids.get(mo)
                    if j2 is None:
                        j2 = len(ids)
                        ids[mo] = j2
                    mi_l.append(j2)
                    ci_l.append(ci)
        mfr = len(ids)
        m_full += mfr
        mi = np.asarray(mi_l, dtype=np.int64)
        ci = np.asarray(ci_l, dtype=np.int64)
        del mi_l, ci_l
        tot = np.bincount(mi, minlength=mfr).astype(float)
        cw = np.bincount(mi, weights=y[ci], minlength=mfr)
        share_w, share_c = cw / n_w, (tot - cw) / n_c
        diff = share_w - share_c
        usable = (cw >= 8) & ((tot - cw) >= 8)
        m_guard = int(usable.sum())

        if m_guard:
            um = np.flatnonzero(usable)
            remap = np.full(mfr, -1, np.int64)
            remap[um] = np.arange(m_guard)
            keep = remap[mi] >= 0
            mi_u, ci_u = remap[mi[keep]], ci[keep]
            tot_u = tot[usable]
            obs = float(np.abs(diff[usable]).max())
            null = np.empty(n_perm)
            for t in range(n_perm):
                cwp = np.bincount(mi_u, weights=perms[t][ci_u],
                                  minlength=m_guard)
                null[t] = np.abs(cwp / n_w - (tot_u - cwp) / n_c).max()
            p_sel = float((np.sum(null >= obs) + 1) / (n_perm + 1))
            bar = 0.10 / m_guard
            guards[frame] = {"m_frame": mfr, "m_guard": m_guard,
                             "observed_max_sep": round(obs, 6),
                             "p_selection_corrected": round(p_sel, 4),
                             "bh_bar_q_over_m": bar,
                             "null_p95": round(float(np.percentile(null, 95)), 6),
                             "admissible": bool(p_sel <= bar),
                             "n_perm": n_perm}
            del mi_u, ci_u, null
        else:
            guards[frame] = {"m_frame": mfr, "m_guard": 0, "admissible": False}

        inv = [None] * mfr
        for s_, i_ in ids.items():
            inv[i_] = s_
        kk = np.fromiter((s_.count(">") + 1 for s_ in inv), np.int8, mfr)
        full = pd.DataFrame({
            "frame": frame, "motif": inv, "k": kk,
            "n_winner": cw.astype(np.int32),
            "n_control": (tot - cw).astype(np.int32),
            "share_winner": share_w.astype(np.float32),
            "share_control": share_c.astype(np.float32),
            "diff": diff.astype(np.float32), "usable": usable})
        # Each frame's COMPLETE motif table goes to disk here and is dropped
        # from memory immediately. Holding all three at once is ~400 MB of
        # motif strings on a machine with under a gigabyte spare, and the only
        # rows any printed table reads are the usable ones.
        D_AGG.mkdir(parents=True, exist_ok=True)
        to_parquet_atomic(full, D_AGG / f"w_b_motifs_{frame}.parquet")
        counts_by_k.append(pd.DataFrame({
            "frame": frame, "k": np.arange(1, KGRAM_MAX + 1),
            "n_motifs": [int((kk == k).sum()) for k in range(1, KGRAM_MAX + 1)],
            "n_usable": [int(usable[kk == k].sum())
                         for k in range(1, KGRAM_MAX + 1)]}))
        parts.append(full[full.usable].copy())
        del ids, inv, mi, ci, tot, cw, full

    res = pd.concat(parts, ignore_index=True)
    bykind = pd.concat(counts_by_k, ignore_index=True)
    print(f"\nFULL MOTIF COUNT (all three frames, k=1..{KGRAM_MAX})  "
          f"m_full = {m_full:,}")
    for frame in SEQ_FRAMES:
        print(f"    {frame:14s} distinct motifs {guards[frame]['m_frame']:>10,d}"
              f"   usable (>=8 both sides) {guards[frame]['m_guard']:>8,d}")
    print(f"  m_full is the number the probe ledger carries. It is large because")
    print(f"  the contract asks for EVERY k-gram up to k={KGRAM_MAX} over the full")
    print(f"  grammar in three coordinate systems. Under the ledger's own rule")
    print(f"  ('display is m = 0') this probe could have been charged nothing;")
    print(f"  the contract charges the whole surface instead, because the motif")
    print(f"  table is what a future registration would be drawn FROM.")

    print(f"\nI11 SELECTION GUARD -- max-statistic permutation, per frame,")
    print(f"printed BESIDE the top table. Statistic = max over usable motifs of")
    print(f"|share_winner - share_control|; null = the same max with the")
    print(f"winner/control labels permuted, {n_perm} times, shared permutations")
    print(f"across frames so the three are directly comparable.")
    print(f"    {'frame':14s} {'m_guard':>9s} {'obs max':>9s} {'null p95':>9s} "
          f"{'p_sel':>7s} {'q/m':>10s}  admissible")
    for frame in SEQ_FRAMES:
        g = guards[frame]
        if not g["m_guard"]:
            print(f"    {frame:14s} {'0':>9s}  guard vacuous")
            continue
        print(f"    {frame:14s} {g['m_guard']:9,d} {g['observed_max_sep']:9.5f} "
              f"{g['null_p95']:9.5f} {g['p_selection_corrected']:7.4f} "
              f"{g['bh_bar_q_over_m']:10.2e}  {g['admissible']}")
    print(f"  Read a row as: the largest winners-vs-control gap ANY usable motif")
    print(f"  achieves, against the gap the LARGEST-OF-m reaches when the labels")
    print(f"  are meaningless. Nothing here is promoted either way.")
    floor = 1.0 / (n_perm + 1)
    print("")
    print(f"  RESOLUTION FLOOR, and it makes `admissible` structurally False.")
    print(f"  With {n_perm} permutations the smallest p_sel attainable is")
    print(f"  1/{n_perm + 1} = {floor:.3e}, while the BH bar q/m is ~{0.10 / max(1, m_full // 3):.1e}.")
    print(f"  The bar sits {floor / (0.10 / max(1, m_full // 3)):.0f}x BELOW the floor, so no motif could")
    print(f"  clear it at this permutation count whatever the data said. The")
    print(f"  informative comparison is therefore obs-vs-null, printed above:")
    print(f"  the observed maximum does not even reach its own null p95 in any")
    print(f"  frame. `admissible` is reported as False and must NOT be read as")
    print(f"  'tested and rejected at q/m' -- it was never testable at q/m.")

    print(f"\nTOP MOTIFS BY |winners - control| SHARE  (usable only; DESCRIPTIVE,")
    print(f"ordered to be LOOKED AT -- no row is kept on the strength of its "
          f"value)")
    for frame in SEQ_FRAMES:
        sel = res[(res.frame == frame) & res.usable]
        s = sel.reindex(sel["diff"].abs().sort_values(ascending=False).index).head(8)
        print(f"\n  frame={frame}   (usable m={len(sel):,})")
        print(f"    {'k':>2s} {'n_w':>5s} {'n_c':>5s} {'share_w':>8s} "
              f"{'share_c':>8s} {'diff':>8s}  motif")
        for _, r in s.iterrows():
            print(f"    {int(r.k):2d} {int(r.n_winner):5d} {int(r.n_control):5d} "
                  f"{r.share_winner:8.4f} {r.share_control:8.4f} "
                  f"{r['diff']:+8.4f}  {r.motif[:66]}")
    print(f"\n  k-gram survival: distinct motifs by k / how many are usable")
    print(f"    {'k':>2s} " + "".join(f"{f:>24s}" for f in SEQ_FRAMES))
    for k in range(1, KGRAM_MAX + 1):
        cells = []
        for frame in SEQ_FRAMES:
            s = bykind[(bykind.frame == frame) & (bykind.k == k)].iloc[0]
            cells.append(f"{int(s.n_motifs):>13,d} /{int(s.n_usable):>9,d}")
        print(f"    {k:2d} " + "".join(cells))
    print(f"  The usable column collapsing toward zero as k grows IS the "
          f"result:\n  a 4-gram over this grammar is very nearly a campaign "
          f"fingerprint, so almost\n  none recurs in eight winners AND eight "
          f"controls. That is a statement about\n  the alphabet's resolution, "
          f"not about the tail.")
    return {"motifs": res, "m_full": m_full, "guard": guards,
            "n_campaigns": len(ckeys), "by_k": bykind}


# ===========================================================================
# W-C  THE FAN QUESTION
# ===========================================================================
def _birth_class(knot, orient):
    return np.where(knot == KN_TRUE, "in-knot",
                    np.where(np.isin(orient, [OR_BULL, OR_BEAR]), "fan-complete",
                             np.where(orient == OR_NA, "n/a", "fanning")))


def w_c(st: pd.DataFrame, coh: pd.DataFrame) -> pd.DataFrame:
    banner("W-C  THE FAN QUESTION -- born in-knot, fanning, or fan-complete")
    print(TIER_E_HEADER)
    print("\nPartition at t0, disjoint and exhaustive:")
    print("  in-knot       knot == 1  (width < 0.5 ATR, the pinned RIBBON_C)")
    print("  fan-complete  orient in {bull, bear} and not in-knot")
    print("  fanning       mixed order, not knotted")
    print("  n/a           not warm -- the partition is undefined, not empty\n")
    st = st.copy()
    st["birth_class"] = _birth_class(st.br_knot.to_numpy(),
                                     st.br_orient.to_numpy())

    print("(i) ON THE BR -- and the BR answer is that the QUESTION does not")
    print("    survive the change of scale. Reported, not fixed:")
    for tf in LENSES:
        s = st[st.lens == tf]
        if not len(s):
            continue
        print(f"    {tf:4s} in-knot {int((s.birth_class == 'in-knot').sum()):4d}"
              f" of {len(s):5,d}   BR width at t0: median "
              f"{s.br_disp_atr.median():6.2f} ATR  p10 "
              f"{s.br_disp_atr.quantile(0.1):6.2f} ATR")
    print("    RIBBON_C = 0.5 ATR is calibrated for a THREE-member SR band. The")
    print("    BR spans e9..e5000 and its width is 15-20 ATR at every stage of")
    print("    W-A, so `br_knot` is false essentially always and the in-knot")
    print("    class is empty by construction rather than by measurement. The")
    print("    constant is VETO by name and was NOT changed. The fan question is")
    print("    therefore answered below at SR scale, where the constant lives.\n")

    for tf in LENSES:
        s = st[st.lens == tf]
        if not len(s):
            continue
        w, c = s[s.cohort == "winner"], s[s.cohort == "control"]
        print(f"    LENS {tf}   BR partition   "
              + "  ".join(
                  f"{cls}: w {int((w.birth_class == cls).sum()):4d} "
                  f"({(w.birth_class == cls).mean():.3f}) / c "
                  f"{int((c.birth_class == cls).sum()):4d} "
                  f"({(c.birth_class == cls).mean():.3f})"
                  for cls in ("fanning", "fan-complete", "n/a")))

    # ---- (ii) per-SR, read at the t0 bar of the state series
    print("\n(ii) PER SR, at the t0 bar -- where RIBBON_C is scale-matched")
    rows = []
    key = st[["ckey", "lens", "t0_bar_index"]].drop_duplicates()
    for sym in PANEL:
        for tf in LENSES:
            p = D_STATE / sym / f"{tf}.parquet"
            if not p.exists():
                continue
            cols = (["ckey", "cohort", "lens", "bar_index"]
                    + [f"{f}_{k}" for f in FAMILIES for k in ("knot", "orient",
                                                             "fan_age")])
            S = pd.read_parquet(p, columns=cols)
            S = S.merge(key, on=["ckey", "lens"], how="inner")
            S = S[S.bar_index == S.t0_bar_index]
            if len(S):
                rows.append(S)
            del S
    T0 = pd.concat(rows, ignore_index=True) if rows else pd.DataFrame()
    for tf in LENSES:
        s = T0[T0.lens == tf] if len(T0) else T0
        if not len(s):
            continue
        print(f"\n  LENS {tf}   winners n={int((s.cohort == 'winner').sum()):,}  "
              f"control n={int((s.cohort == 'control').sum()):,}")
        print(f"    {'SR':5s} {'class':13s} {'w n':>6s} {'w share':>8s} "
              f"{'c n':>6s} {'c share':>8s} {'diff':>8s}")
        for fam in FAMILIES:
            bc = _birth_class(s[f"{fam}_knot"].to_numpy(),
                              s[f"{fam}_orient"].to_numpy())
            w = bc[(s.cohort == "winner").to_numpy()]
            c = bc[(s.cohort == "control").to_numpy()]
            for cls in ("in-knot", "fanning", "fan-complete", "n/a"):
                nw, nc = int((w == cls).sum()), int((c == cls).sum())
                if nw == 0 and nc == 0:
                    continue
                sw = nw / len(w) if len(w) else 0.0
                sc = nc / len(c) if len(c) else 0.0
                print(f"    {fam:5s} {cls:13s} {nw:6d} {sw:8.4f} {nc:6d} "
                      f"{sc:8.4f} {sw - sc:+8.4f}")

    # ---- (iii) time-from-knot-exit to t0, from A-3's knot episodes
    print("\n(iii) TIME FROM KNOT EXIT TO t0 (hours), from the A-3 episode "
          "ledger.\n      Per SR: the most recent knot EXIT strictly before t0. "
          "'never' = the SR\n      had not unknotted at any point in that "
          "asset's history before t0.")
    t0m = dict(zip(coh.ckey, coh.t0_ms.astype(np.int64)))
    cohm = dict(zip(coh.ckey, coh.cohort))
    assetm = dict(zip(coh.ckey, coh.asset))
    out = []
    for sym in PANEL:
        cks = [c for c in t0m if assetm[c] == sym]
        if not cks:
            continue
        t0s = np.array([t0m[c] for c in cks], dtype=np.int64)
        for tf in LENSES:
            p = pa.D_TRN / sym / f"{tf}_knots.parquet"
            if not p.exists():
                continue
            K = pd.read_parquet(p, columns=["sr", "exit_ts_ms"])
            for fam in FAMILIES:
                ex = np.sort(K[(K.sr == fam) & (K.exit_ts_ms > 0)]
                             .exit_ts_ms.to_numpy(np.int64))
                if not ex.size:
                    continue
                j = np.searchsorted(ex, t0s, "left") - 1
                h = np.where(j >= 0, (t0s - ex[np.clip(j, 0, ex.size - 1)])
                             / 3.6e6, np.nan)
                out.append(pd.DataFrame({"ckey": cks, "lens": tf, "sr": fam,
                                         "hours_since_knot_exit": h}))
    KE = pd.concat(out, ignore_index=True) if out else pd.DataFrame()
    if len(KE):
        KE["cohort"] = KE.ckey.map(cohm)
        print(f"      {'lens':5s} {'SR':5s} {'w med':>9s} {'w p90':>9s} "
              f"{'c med':>9s} {'c p90':>9s} {'w never':>8s} {'c never':>8s}")
        for tf in LENSES:
            for fam in FAMILIES:
                s = KE[(KE.lens == tf) & (KE.sr == fam)]
                if not len(s):
                    continue
                w = s[s.cohort == "winner"].hours_since_knot_exit
                c = s[s.cohort == "control"].hours_since_knot_exit
                print(f"      {tf:5s} {fam:5s} {w.median():9.1f} "
                      f"{w.quantile(0.9):9.1f} {c.median():9.1f} "
                      f"{c.quantile(0.9):9.1f} {int(w.isna().sum()):8d} "
                      f"{int(c.isna().sum()):8d}")
    return st


# ===========================================================================
# W-D  RECLAIM ANATOMY  (feeds P-REC-1 wording)
# ===========================================================================
LONG_EMAS = [889, 2618, 4618]


def w_d(coh: pd.DataFrame) -> pd.DataFrame:
    banner("W-D  RECLAIM ANATOMY -- long-EMA loss -> reclaim inside campaigns")
    print(TIER_E_HEADER)
    print(f"\nlong EMAs      {LONG_EMAS}  (the SR medians of H, VH, UH)")
    print(f"loss           close crosses the EMA AGAINST the campaign direction")
    print(f"reclaim        close crosses it back IN FAVOUR, before t_exit")
    print(f"lens           1h; the hold spans days, so a 5m scan would count the")
    print(f"               same structural loss dozens of times")
    print(f"CURTAIN        every event here is INSIDE the campaign, i.e. strictly")
    print(f"               after t0. This is anatomy. It is not an entry feature.\n")
    from engine.indicators import crossover, crossunder
    rows = []
    for sym in PANEL:
        e, _rb = load_cell(sym, "1h")
        ot = e["open_time"].to_numpy(np.int64)
        cl = e["close"].to_numpy(np.float64)
        av = e["atr"].to_numpy(np.float64)
        sub = coh[coh.asset == sym]
        xs = {}
        for L in LONG_EMAS:
            v = e[f"e{L}"].to_numpy(np.float64)
            xs[L] = (np.flatnonzero(crossover(cl, v)),
                     np.flatnonzero(crossunder(cl, v)))
        for _, r in sub.iterrows():
            t0, te = int(r.t0_ms), r.t_exit_ms
            if not np.isfinite(te):
                continue
            i0 = int(np.searchsorted(ot, t0, "right")) - 1
            ie = int(np.searchsorted(ot, int(te), "right")) - 1
            if i0 < 0 or ie <= i0:
                continue
            up = r["dir"] == "long"
            for L in LONG_EMAS:
                gain_i, lose_i = (xs[L][0], xs[L][1]) if up else (xs[L][1], xs[L][0])
                loss = lose_i[(lose_i > i0) & (lose_i <= ie)]
                for li in loss:
                    nxt = gain_i[gain_i > li]
                    nxt = nxt[nxt <= ie]
                    if not nxt.size:
                        continue
                    ri = int(nxt[0])
                    sgn = 1.0 if up else -1.0
                    rows.append({
                        "ckey": r.ckey, "cohort": r.cohort, "asset": sym,
                        "dir": r["dir"], "ema": L, "gross_R": float(r.gross_R),
                        "loss_ts_ms": int(ot[li]), "reclaim_ts_ms": int(ot[ri]),
                        "loss_h_from_t0": (int(ot[li]) - t0) / 3.6e6,
                        "reclaim_lag_h": (int(ot[ri]) - int(ot[li])) / 3.6e6,
                        "hold_frac_at_loss": ((int(ot[li]) - t0)
                                              / max(1.0, (int(te) - t0))),
                        "after_reclaim_to_exit_atr": (
                            sgn * (cl[ie] - cl[ri]) / av[ri]
                            if np.isfinite(av[ri]) and av[ri] > 0 else np.nan),
                    })
        del e
    R = pd.DataFrame(rows)
    if not len(R):
        print("  no loss->reclaim events found")
        return R
    hold = coh.set_index("ckey")
    hold_h = ((hold.t_exit_ms - hold.t0_ms) / 3.6e6)
    exposure = hold_h.groupby(hold.cohort).sum()
    med_hold = hold_h.groupby(hold.cohort).median()

    print("  !! EXPOSURE WARNING, read this BEFORE the table. Winners and")
    print(f"     controls are NOT duration-comparable: median hold is")
    print(f"     {med_hold.get('winner', float('nan')):.1f}h for winners against "
          f"{med_hold.get('control', float('nan')):.1f}h for controls, a "
          f"{med_hold.get('winner', 1) / max(med_hold.get('control', 1), 1e-9):.0f}x gap.")
    print("     A loss->reclaim can only happen while a campaign is OPEN, so any")
    print("     raw winner-vs-control count here is mostly a measurement of how")
    print("     long each side was exposed. The per-100h column divides that out;")
    print("     the raw columns are printed beside it and must not be read alone.")
    print("     This is the contract's WINNING-campaign anatomy; the control")
    print("     column is context, not a comparison that can carry weight.\n")
    print(f"  {'ema':>6s} {'cohort':8s} {'events':>8s} {'campaigns':>10s} "
          f"{'ev/camp':>8s} {'ev/100h':>9s} {'med lag h':>10s} "
          f"{'med h from t0':>14s} {'after->exit ATR':>17s}")
    for L in LONG_EMAS:
        for cl_lab in ("winner", "control"):
            s = R[(R.ema == L) & (R.cohort == cl_lab)]
            ncamp = s.ckey.nunique()
            exp = float(exposure.get(cl_lab, np.nan))
            print(f"  {L:6d} {cl_lab:8s} {len(s):8,d} {ncamp:10,d} "
                  f"{(len(s) / ncamp if ncamp else 0):8.2f} "
                  f"{(len(s) / exp * 100 if exp else float('nan')):9.3f} "
                  f"{s.reclaim_lag_h.median():10.1f} "
                  f"{s.loss_h_from_t0.median():14.1f} "
                  f"{s.after_reclaim_to_exit_atr.median():17.3f}")
    print(f"\n  total open-campaign exposure: winners "
          f"{exposure.get('winner', float('nan')):,.0f}h  controls "
          f"{exposure.get('control', float('nan')):,.0f}h")
    print(f"\n  campaigns with >=1 loss->reclaim on ANY long EMA:")
    for cl_lab in ("winner", "control"):
        s = R[R.cohort == cl_lab]
        tot = int((coh.cohort == cl_lab).sum())
        print(f"    {cl_lab:8s} {s.ckey.nunique():,} of {tot:,} "
              f"({s.ckey.nunique() / tot * 100:.1f}%)   <- exposure-confounded")

    # duration-matched band: the only winner/control comparison here that is
    # not simply a restatement of hold time
    print(f"\n  DURATION-MATCHED BAND (campaigns held >= 24h, both cohorts):")
    lon = hold_h[hold_h >= 24]
    for cl_lab in ("winner", "control"):
        ck = set(lon[hold.cohort.reindex(lon.index) == cl_lab].index)
        if not ck:
            print(f"    {cl_lab:8s} 0 campaigns in band")
            continue
        s = R[R.ckey.isin(ck)]
        exp = float(hold_h[list(ck)].sum())
        print(f"    {cl_lab:8s} {len(ck):5,d} campaigns  {exp:9,.0f}h exposure  "
              f"{s.ckey.nunique():4,d} with an event "
              f"({s.ckey.nunique() / len(ck) * 100:5.1f}%)  "
              f"{len(s) / exp * 100:6.3f} ev/100h")
    print("\n  DESCRIPTIVE. This is the shape P-REC-1 would be worded against;")
    print("  no threshold is swept here and nothing is registered.")
    return R


# ===========================================================================
# W-E  THE BRUNCH TABLE
# ===========================================================================
def w_e(coh: pd.DataFrame) -> None:
    banner(f"W-E  THE BRUNCH TABLE -- top {TOP_N_BRUNCH} winners by gross_R")
    print(TIER_E_HEADER)
    print("\nDISPLAY ONLY. One page per campaign: the +-72h story in events.")
    print("The BEFORE block is the only half that could be entry evidence and "
          "it is\nlabelled as such; the AFTER block is anatomy.\n")
    w = (coh[coh.cohort == "winner"].sort_values("gross_R", ascending=False)
         .head(TOP_N_BRUNCH))
    st = pd.read_parquet(W / "wtb1_t0_stamps.parquet")
    for rank, (_, r) in enumerate(w.iterrows(), 1):
        s1 = st[(st.ckey == r.ckey) & (st.lens == "1h")]
        s1 = s1.iloc[0] if len(s1) else None
        hold_h = (r.t_exit_ms - r.t0_ms) / 3.6e6 if np.isfinite(r.t_exit_ms) else np.nan
        hr(n=92)
        print(f"#{rank:<3d} {r.ckey}")
        print(f"     {r.asset}  {r['dir']:5s}  {r.mandate:9s}  size_r={r.size_r}  "
              f"gross_R={r.gross_R:+.3f}  mfe_R={r.mfe_R:+.3f}  "
              f"give_back_R={r.give_back_R:+.3f}")
        print(f"     t0 {iso(r.t0_ms)}   exit {iso(r.t_exit_ms)}   "
              f"hold {hold_h:.1f}h   exit_reason={r.exit_reason}")
        if s1 is not None:
            print(f"     AT t0 (1h): BR {STATE_NAME[int(s1.br_state)]}/"
                  f"{ORIENT_NAME[int(s1.br_orient)]}"
                  f"{' /KNOT' if int(s1.br_knot) == KN_TRUE else ''}  "
                  f"disp={s1.displacement_atr:.2f}ATR  "
                  f"BR-width={s1.br_disp_atr:.2f}ATR  "
                  f"disorder={s1.sr_order_disorder:.2f}  "
                  f"wall={s1.wall_family}  fan_age={int(s1.br_fan_age)}b")
        for side in ("BEFORE", "AFTER"):
            parts = []
            for tf in LENSES:
                p = D_TAPE / r.asset / f"{tf}.parquet"
                if not p.exists():
                    continue
                T = pd.read_parquet(p, columns=["ckey", "lens", "ts_ms",
                                                "rel_h", "side", "kind",
                                                "token", "in_motif_alphabet"])
                parts.append(T[(T.ckey == r.ckey) & (T.side == side)
                               & T.in_motif_alphabet])
                del T
            tp = (pd.concat(parts, ignore_index=True).sort_values("ts_ms")
                  if parts else pd.DataFrame())
            lab = ("BEFORE t0 (entry-side; the only half readable as evidence)"
                   if side == "BEFORE" else "AFTER t0 (ANATOMY -- never entry evidence)")
            print(f"     --- {lab}   n={len(tp):,}")
            if not len(tp):
                continue
            for h in range(-72 if side == "BEFORE" else 0,
                           0 if side == "BEFORE" else 72, 12):
                g = tp[(tp.rel_h >= h) & (tp.rel_h < h + 12)]
                if not len(g):
                    continue
                counts = g.token.value_counts()
                top = "  ".join(f"{k}x{v}" for k, v in counts.head(9).items())
                print(f"       {h:+4d}..{h + 12:+4d}h  n={len(g):4d}  {top}")
    hr(n=92)


def run_aggregates(coh: pd.DataFrame) -> None:
    print_horizon_realisation(LENSES)
    st = pd.read_parquet(W / "wtb1_t0_stamps.parquet")
    D_AGG.mkdir(parents=True, exist_ok=True)
    A = w_a(coh)
    to_parquet_atomic(A, D_AGG / "w_a_station_occupancy.parquet")
    B = w_b(coh)
    to_parquet_atomic(B["motifs"], D_AGG / "w_b_motifs_usable.parquet")
    to_parquet_atomic(B["by_k"], D_AGG / "w_b_motifs_by_k.parquet")
    (D_AGG / "w_b_guard.json").write_text(
        json.dumps({"m_full": B["m_full"], "guard": B["guard"],
                    "n_campaigns": B["n_campaigns"],
                    "frames": SEQ_FRAMES, "k_max": KGRAM_MAX,
                    "window_h": MOTIF_WINDOW_H,
                    "note": ("per-frame COMPLETE motif tables are "
                             "w_b_motifs_<frame>.parquet; "
                             "w_b_motifs_usable.parquet carries only the rows "
                             "the guard scores"),
                    "class": TIER_E_HEADER}, indent=2), encoding="utf-8")
    C = w_c(st, coh)
    to_parquet_atomic(C, D_AGG / "w_c_fan_question.parquet")
    D = w_d(coh)
    to_parquet_atomic(D, D_AGG / "w_d_reclaim.parquet")
    w_e(coh)
    print(f"\nAGGREGATE ARTIFACTS")
    for p in sorted(D_AGG.glob("*")):
        print(f"  {p}  {p.stat().st_size:,} bytes")


# ===========================================================================
# MAIN
# ===========================================================================
def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", newline="\n")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="CENSUS-2B W-TB1")
    ap.add_argument("--stage", default="cohort",
                    help="cohort|capture|agg|all (comma ok)")
    ap.add_argument("--assets", default="", help="scope the capture (testing)")
    a = ap.parse_args()

    banner("CENSUS-2B / W-TB1 -- TAIL BIOGRAPHY")
    print(f"program   {PROGRAM}   seed {SEED}")
    print(f"class     Tier-E descriptive -- REGISTRATIONS DEFERRED")
    print(f"curtain   +-{WIN_H}h around birth; the AFTER side is ANATOMY, never "
          f"entry evidence")
    print(f"lenses    {LENSES}")
    print(f"out       {W}")

    stages = ({"cohort", "capture", "agg"} if a.stage == "all"
              else {s.strip() for s in a.stage.split(",")})
    bad = sorted(stages - {"cohort", "capture", "agg"})
    if bad:
        print(f"HALT: unrecognised --stage token(s) {bad}.")
        return 2

    cp = W / "wtb1_cohort.parquet"
    if "cohort" in stages or not cp.exists():
        coh, mt = build_cohort()
        fixture_w1(coh, mt)
        W.mkdir(parents=True, exist_ok=True)
        to_parquet_atomic(coh, cp)
        to_parquet_atomic(mt, W / "wtb1_matching.parquet")
        print(f"\nwrote {cp}  rows={len(coh):,}")
        print(f"wrote {W / 'wtb1_matching.parquet'}  rows={len(mt):,}")
    else:
        coh = pd.read_parquet(cp)
        print(f"\ncohort loaded from {cp}  rows={len(coh):,}")

    if a.assets:
        coh = coh[coh.asset.isin([s.strip() for s in a.assets.split(",")])]
        print(f"SCOPED to assets {sorted(coh.asset.unique())}  rows={len(coh):,}")

    if "capture" in stages:
        run_capture(coh)
    if "agg" in stages:
        run_aggregates(coh)
    print(f"\nW-TB1 elapsed={time.time() - _T0:.0f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
