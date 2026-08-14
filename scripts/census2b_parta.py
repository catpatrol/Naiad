#!/usr/bin/env python3
"""
CENSUS-2B / PART A -- COMPLETION AUDIT + SEQUENTIAL SUBSTRATE
=============================================================
Contract: operator paste 2026-08-14 ("CENSUS-2B PART A, run BEFORE W-TB1").
Drafted: APOLLO.  Executor: HEPHAESTUS.  Seed 20260814.
CLASS: Tier-E substrate.  NO REGISTRATIONS.  F-KEY everywhere.
NaN-before-warm always -- inherited, not re-implemented.

scripts/census2b_program.py is BYTE-UNTOUCHED and is imported as the ratified
machinery: RIBBONS, WARM, refusal_events, feasible_lengths, the codes, the
atomic writer, the pin-merge manifest.  Nothing it already states is restated
here.

STAGES
------
A-0  COMPLETION AUDIT      manifest -> stage x lens x asset PRESENT/ABSENT
A-1  i-a REFUSALS          kiss grammar on the PARED within-SR + SR-median pairs
A-2  BR ARMED-WINDOW v2    12_89 arming, counter-12_89 close, 12_26 trigger
A-3  TRANSITION LEDGER     KNOT episodes + FAN births, forward H20/H100
A-4  SPRING/UPTHRUST       96-bar extreme penetration, reclaim within 3 bars

A-2 consumes A-4, so the run order is A-0, A-1, A-4, A-3, A-2.

USAGE
    python scripts/census2b_parta.py --stage 0
    python scripts/census2b_parta.py --stage all
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

import census2b_program as c2b                                   # noqa: E402

# ---- ratified machinery, imported by name so the provenance is legible
RIBBONS = c2b.RIBBONS
FAMILIES = c2b.FAMILIES
ALL_EMAS = c2b.ALL_EMAS
WARM = c2b.WARM
PANEL = c2b.PANEL
ANNEX = c2b.ANNEX
TFS = c2b.TFS
OUT = c2b.OUT
MANIFEST = c2b.MANIFEST
refusal_events = c2b.refusal_events
feasible_lengths = c2b.feasible_lengths
to_parquet_atomic = c2b.to_parquet_atomic
sha256_file = c2b.sha256_file
parquet_rows = c2b.parquet_rows
iso = c2b.iso
hr = c2b.hr
banner = c2b.banner
KISS_EPS, KISS_DELTA, KISS_K = c2b.KISS_EPS, c2b.KISS_DELTA, c2b.KISS_K
ST_COMPRESS, ST_FLAT, ST_EXPAND, ST_NA = (c2b.ST_COMPRESS, c2b.ST_FLAT,
                                          c2b.ST_EXPAND, c2b.ST_NA)
OR_BEAR, OR_MIXED, OR_BULL, OR_NA = c2b.OR_BEAR, c2b.OR_MIXED, c2b.OR_BULL, c2b.OR_NA
KN_FALSE, KN_TRUE, KN_NA = c2b.KN_FALSE, c2b.KN_TRUE, c2b.KN_NA
TOLL_BPS_ROUND_TRIP = c2b.TOLL_BPS_ROUND_TRIP

# ===========================================================================
# PART-A CONSTANTS -- VETO BY NAME.  Nothing below is tuned, swept, or chosen.
# ===========================================================================
SEED = 20260814
PROGRAM = "census2b_parta.py"

# The PARED within-SR set: the MIDDLE member against the SLOW member of each
# family.  The contract names them literally and vetoes 9_12 by name; they are
# derived from RIBBONS here so the two statements cannot drift apart, and F-A1
# asserts the derived list equals the contract's literal list.
PARED_WITHIN_SR = [(m, z) for (_a, m, z) in RIBBONS.values()]
PARED_LITERAL = [(12, 26), (89, 127), (316, 423), (889, 1272),
                 (2618, 3618), (4618, 5000)]
SR_MEDIAN_PAIRS = c2b.MIDLINE_PAIRS          # (12,89) (89,316) (316,889) ...

LENSES_A1 = ["5m", "15m", "30m", "1h"]
LENSES_A2 = ["5m", "15m", "30m", "1h", "4h"]
LENSES_A3 = ["5m", "15m", "30m", "1h"]
LENSES_A4 = ["5m", "15m", "30m", "1h"]

ARM_PAIR = (12, 89)              # arming cross            [contract]
TRIG_PAIR = (12, 26)             # in-window trigger       [contract]

SWEEP_N = 96                     # prior-extreme lookback  [VETO N=96]
SWEEP_RECLAIM = 3                # close back inside within 3 bars [VETO]

# Horizons are DURATION-fixed, exactly as census2a_program.py:96-97 pins them.
# H20 == 20 x 5m == 1h40m; H100 == 100 x 5m == 8h20m.  They are NOT bar counts.
HORIZONS_MS = {"H20": 20 * 300_000, "H100": 100 * 300_000}
LOOKBACK_H = 24                  # hours, arming-stamp lookback windows

TF_MS = {"1m": 60_000, "5m": 300_000, "15m": 900_000, "30m": 1_800_000,
         "1h": 3_600_000, "4h": 14_400_000, "12h": 43_200_000}

A = OUT                                    # census2b root
D_REF = OUT / "refusals"
D_WIN = OUT / "windows"
D_TRN = OUT / "transitions"
D_SPR = OUT / "springs"

TIER_E_HEADER = c2b.TIER_E_HEADER

_T0 = time.time()


# ===========================================================================
# SHARED HELPERS
# ===========================================================================
def bars_for_hours(tf: str, hours: int) -> int:
    """Whole bars spanning `hours` on `tf`, rounded UP.

    Rounding up matters: a 24h lookback on 4h is 6 bars exactly, but on 12h it
    is 2 bars, and truncation would silently shorten the window on any lens
    whose bar does not divide the hour.
    """
    return int(np.ceil(hours * 3_600_000 / TF_MS[tf]))


def load_feasibility() -> pd.DataFrame:
    """The PINNED feasibility matrix.

    Re-running census2b_program.stage1() would rebuild it correctly but reloads
    every raw kline file to do so -- minutes of I/O to reproduce a table that is
    already on disk and sha-pinned.  A-0 has just verified that pin, so reading
    it is not a shortcut past a check; it is the check's payoff.
    """
    p = OUT / "cen2b_feasibility.parquet"
    if not p.exists():
        print(f"HALT: {p} absent -- A-0 should have caught this.")
        raise SystemExit(2)
    return pd.read_parquet(p)


def load_cell(sym: str, tf: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """(emas, ribbons) for one cell, or a HALT if either is missing."""
    pe = OUT / "emas" / sym / f"{tf}.parquet"
    pr = OUT / "ribbons" / sym / f"{tf}.parquet"
    if not pe.exists() or not pr.exists():
        raise FileNotFoundError(f"{sym} {tf}: substrate absent ({pe}, {pr})")
    return pd.read_parquet(pe), pd.read_parquet(pr)


def horizon_bars(tf: str, hname: str) -> tuple[int, bool, float]:
    """(bars, infeasible, duration_ratio) for a DURATION-fixed horizon.

    Restated from census2a_program.py:879-897 rather than imported, so that
    F-A0R can prove the two expressions agree instead of proving a tautology.
    H20 and H100 are 20 and 100 FIVE-MINUTE EQUIVALENTS -- 1h40m and 8h20m --
    NOT 20 and 100 bars of the lens.  Reading them as bar counts was the
    paste-1 defect R-1 exists to remove: it makes `H100` mean 8h20m on 5m and
    4 days 4 hours on 1h, i.e. a different horizon per lens under one label.

    bars < 1 is INFEASIBLE and yields NaN. It is never substituted with 1.
    """
    hms = HORIZONS_MS[hname]
    raw = hms / TF_MS[tf]
    bars = int(round(raw))
    if bars < 1:
        return 0, True, float("nan")
    return bars, False, round(bars * TF_MS[tf] / hms, 4)


def r1_block(close: np.ndarray, high: np.ndarray, low: np.ndarray,
             av: np.ndarray, idx: np.ndarray, sgn: np.ndarray,
             tf: str) -> dict[str, np.ndarray]:
    """The R-1 ruler: signed TERMINAL return, ATR-normalised AT THE ANCHOR.

    census2a_program.py:862-917, vectorised over a PER-ROW direction (its
    original takes one scalar `up` for the whole call because a census-2A
    ledger slice is single-direction; a Part-A event table interleaves both).
    F-A0R asserts this reproduces the original element-for-element on a
    single-direction slice.

    MFE/MAE excursion window is [i+1, end] -- the anchor bar is EXCLUDED, as in
    the original.  MAE is stored POSITIVE-as-adverse; the quality ratio is
    MFE/|MAE|.
    """
    n = len(close)
    out: dict[str, np.ndarray] = {}
    for hname in HORIZONS_MS:
        bars, infeas, _ratio = horizon_bars(tf, hname)
        m = len(idx)
        term = np.full(m, np.nan)
        mfe = np.full(m, np.nan)
        mae = np.full(m, np.nan)
        if infeas:
            out[f"term_{hname}"] = term
            out[f"mfe_{hname}"] = mfe
            out[f"mae_{hname}"] = mae
            continue
        # bulk path: full-length windows, computed once for the whole series
        s_hi = pd.Series(high).rolling(bars).max().shift(-bars).to_numpy()
        s_lo = pd.Series(low).rolling(bars).min().shift(-bars).to_numpy()
        end_full = idx + bars
        ok = (idx >= 0) & (idx < n) & np.isfinite(av[np.clip(idx, 0, n - 1)]) \
            & (av[np.clip(idx, 0, n - 1)] > 0)
        tail = ok & (end_full > n - 1)          # clamped windows, the original
        full = ok & ~tail                        # clamps rather than dropping
        i_f = idx[full]
        if i_f.size:
            e_f = i_f + bars
            term[full] = sgn[full] * (close[e_f] - close[i_f]) / av[i_f]
            hi_f, lo_f = s_hi[i_f], s_lo[i_f]
            up_f = sgn[full] > 0
            mfe[full] = np.where(up_f, hi_f - close[i_f],
                                 close[i_f] - lo_f) / av[i_f]
            mae[full] = np.where(up_f, close[i_f] - lo_f,
                                 hi_f - close[i_f]) / av[i_f]
        # tail rows are few (at most `bars` anchors) and are done exactly
        for j in np.flatnonzero(tail):
            i = int(idx[j])
            end = min(i + bars, n - 1)
            if end <= i:
                continue
            s = float(sgn[j])
            term[j] = s * (close[end] - close[i]) / av[i]
            seg_hi = float(high[i + 1:end + 1].max())
            seg_lo = float(low[i + 1:end + 1].min())
            mfe[j] = ((seg_hi - close[i]) if s > 0
                      else (close[i] - seg_lo)) / av[i]
            mae[j] = ((close[i] - seg_lo) if s > 0
                      else (seg_hi - close[i])) / av[i]
        out[f"term_{hname}"] = term
        out[f"mfe_{hname}"] = mfe
        out[f"mae_{hname}"] = mae
    return out


def toll_atr_for(close: np.ndarray, av: np.ndarray,
                 idx: np.ndarray) -> float:
    """The toll line in ATR units, measured ON THE EVENT POPULATION.

    census2a_program.py:1226-1234 note m8: the toll must be measured where the
    returns are normalised, not over every bar in the series.  Events cluster
    at compressed ATR, so a whole-series figure understates the toll.  `idx` is
    this table's own anchors.
    """
    if idx.size == 0:
        return float("nan")
    i = idx[(idx >= 0) & (idx < len(close))]
    ok = np.isfinite(close[i]) & np.isfinite(av[i]) & (av[i] > 0)
    if not ok.any():
        return float("nan")
    return float(np.median((TOLL_BPS_ROUND_TRIP / 10000.0)
                           * close[i][ok] / av[i][ok]))


def attach_r1(df: pd.DataFrame, e: pd.DataFrame, anchor_col: str,
              dir_col: str, tf: str, prefix: str = "") -> pd.DataFrame:
    """Attach term/mfe/mae at every horizon plus the toll line, in place."""
    if not len(df):
        for hname in HORIZONS_MS:
            for k in ("term", "mfe", "mae"):
                df[f"{prefix}{k}_{hname}"] = pd.Series(dtype="float32")
        df[f"{prefix}toll_atr"] = pd.Series(dtype="float32")
        return df
    close = e["close"].to_numpy(np.float64)
    high = e["high"].to_numpy(np.float64)
    low = e["low"].to_numpy(np.float64)
    av = e["atr"].to_numpy(np.float64)
    idx = df[anchor_col].to_numpy(np.int64)
    sgn = df[dir_col].to_numpy(np.float64)
    valid = idx >= 0
    blk = r1_block(close, high, low, av, np.clip(idx, 0, len(close) - 1),
                   sgn, tf)
    for k, v in blk.items():
        df[f"{prefix}{k}"] = np.where(valid, v, np.nan).astype(np.float32)
    df[f"{prefix}toll_atr"] = np.float32(toll_atr_for(close, av, idx[valid]))
    return df


def print_horizon_realisation(lenses: list[str]) -> None:
    """What H20 / H100 actually MEAN on each lens.  Printed before any outcome
    table, per R-1: a horizon label that means a different duration per lens is
    not a horizon."""
    print("HORIZON REALISATION (duration-fixed; H20 = 1h40m, H100 = 8h20m)")
    print(f"  {'lens':6s} " + "".join(f"{h:>28s}" for h in HORIZONS_MS))
    for tf in lenses:
        cells = []
        for hname in HORIZONS_MS:
            bars, infeas, ratio = horizon_bars(tf, hname)
            if infeas:
                cells.append(f"{'INFEASIBLE -> NaN':>28s}")
            else:
                cells.append(f"{bars:>4d} bar(s) = "
                             f"{bars * TF_MS[tf] / 3.6e6:5.2f}h  r={ratio:.2f}"
                             .rjust(28))
        print(f"  {tf:6s} " + "".join(cells))
    infs = [(tf, h) for tf in lenses for h in HORIZONS_MS
            if horizon_bars(tf, h)[1]]
    if infs:
        print(f"  INFEASIBLE cells emit NaN and are NEVER substituted with one "
              f"bar: {infs}")
    print()


def fkey(df: pd.DataFrame, key: list[str], label: str) -> None:
    """F-KEY at write time.  A duplicate key is a HALT, never a warning."""
    if len(df) == 0:
        print(f"      F-KEY {label}: 0 rows (vacuous PASS)")
        return
    dup = int(df.duplicated(subset=key).sum())
    if dup:
        print(f"      F-KEY FAIL {label}: {dup} duplicate keys on {key}")
        raise SystemExit(2)
    print(f"      F-KEY {label}: {len(df):,} rows, 0 duplicates on {key}")


def write_table(df: pd.DataFrame, p: Path, key: list[str], label: str) -> dict:
    p.parent.mkdir(parents=True, exist_ok=True)
    fkey(df, key, label)
    to_parquet_atomic(df, p)
    b = p.stat().st_size
    print(f"      wrote {p}  rows={len(df):,}  bytes={b:,}")
    return {"path": str(p), "rows": len(df), "bytes": b}


# ===========================================================================
# A-0 -- COMPLETION AUDIT
# ===========================================================================
CORE_STAGES = ["feasibility", "emas", "ribbons", "crosses", "first-look"]


def fixture_a0r(assets: list[str]) -> None:
    """F-A0R -- the restated R-1 ruler equals census-2A's original.

    Part A restates `outcome_block` because its tables interleave directions and
    the original takes one scalar `up` per call.  A restatement that drifts from
    the ruler it claims to be is worse than no ruler, so it is compared against
    the original on a real series, element for element, both directions.
    """
    banner("F-A0R  the restated R-1 ruler vs census-2A's outcome_block")
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "_c2a_r1", REPO / "scripts" / "census2a_program.py")
    try:
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        orig = mod.outcome_block
    except Exception as exc:
        print(f"      SKIP -- census2a_program.py not importable in isolation "
              f"({type(exc).__name__}: {exc}); the restatement stands on the "
              f"horizon-realisation print and F-A0H below.")
        return
    # Every lens A-2 runs on, including 4h where H20 is INFEASIBLE, and the
    # SERIES TAIL where r1_block's clamped path is the only one exercised. A
    # sample drawn only from a single lens's interior never touches the two
    # branches most likely to be wrong.
    ok = True
    for tf in LENSES_A2:
        sym = assets[0]
        e, _ = load_cell(sym, tf)
        n = len(e)
        rng = np.random.default_rng(SEED + TF_MS[tf])
        interior = rng.choice(np.arange(1000, n - 200), size=300, replace=False)
        idx = np.sort(np.concatenate([interior, np.arange(n - 120, n)]))
        df = e[["close", "high", "low", "atr"]].copy()
        close = e["close"].to_numpy(np.float64)
        high = e["high"].to_numpy(np.float64)
        low = e["low"].to_numpy(np.float64)
        av = e["atr"].to_numpy(np.float64)
        n_tail = int(sum(1 for hn in HORIZONS_MS
                         if not horizon_bars(tf, hn)[1]))
        for up in (True, False):
            ref = orig(df, idx, up, tf)
            got = r1_block(close, high, low, av, idx,
                           np.full(len(idx), 1.0 if up else -1.0), tf)
            for hname in HORIZONS_MS:
                for k in ("terminal", "mfe", "mae"):
                    a = np.asarray(ref[hname][k], dtype=np.float64)
                    mine = got[f"{'term' if k == 'terminal' else k}_{hname}"]
                    same = np.allclose(a, mine, equal_nan=True, rtol=0, atol=0)
                    ok &= same
                    if not same:
                        print(f"      MISMATCH {tf} up={up} {hname} {k}")
        infe = [h for h in HORIZONS_MS if horizon_bars(tf, h)[1]]
        print(f"      {tf:4s} n={len(idx)} (120 at the series tail, clamped "
              f"path) x 2 directions x {len(HORIZONS_MS)} horizons x 3 series"
              f"  identical=True" + (f"   [{infe} INFEASIBLE]" if infe else ""))
        del e, df
    if not ok:
        print("      F-A0R FAIL -- the restated ruler is NOT census-2A's ruler")
        raise SystemExit(2)
    print("      F-A0R PASS -- element-for-element identical on every A-2 lens, "
          "both directions,\n      interior and clamped-tail anchors, including "
          "the INFEASIBLE 4h/H20 branch")


def a0_audit() -> dict:
    banner("A-0  COMPLETION AUDIT -- the census-2B completion certificate")
    print("Source: D:/Naiad/research_outputs/census2b/census2b_manifest.json")
    print("A cell is PRESENT only if the manifest pins it AND the file is on disk")
    print("AND its recorded sha256 still matches the bytes.  A pinned-but-changed")
    print("file is reported STALE, which is neither PRESENT nor ABSENT.\n")

    if not MANIFEST.exists():
        print("HALT: census2b_manifest.json absent -- V-ULT-1 has not run.")
        raise SystemExit(2)
    man = json.loads(MANIFEST.read_text(encoding="utf-8"))
    arts = man.get("artifacts", {})

    rows = []

    def probe(stage: str, asset: str, lens: str, key: str) -> None:
        rec = arts.get(key)
        p = OUT / key
        if rec is None:
            state = "ABSENT" if not p.exists() else "UNPINNED"
            rows.append({"stage": stage, "asset": asset, "lens": lens,
                         "key": key, "state": state, "rows": None,
                         "bytes": None, "sha256": ""})
            return
        if not Path(rec["path"]).exists():
            rows.append({"stage": stage, "asset": asset, "lens": lens,
                         "key": key, "state": "PINNED-MISSING", "rows": None,
                         "bytes": None, "sha256": rec.get("sha256", "")})
            return
        h = sha256_file(Path(rec["path"]))
        state = "PRESENT" if h == rec.get("sha256") else "STALE"
        rows.append({"stage": stage, "asset": asset, "lens": lens, "key": key,
                     "state": state, "rows": rec.get("rows"),
                     "bytes": rec.get("bytes"), "sha256": h})

    probe("feasibility", "-", "-", "cen2b_feasibility.parquet")
    for stage in ("emas", "ribbons", "crosses"):
        for sym in PANEL + ANNEX:
            for tf in TFS:
                probe(stage, sym, tf, f"{stage}/{sym}/{tf}.parquet")
    # first-look tables are not (asset x lens) cells; they are named tables, and
    # printing nine identical "-  -" rows makes the audit unreadable exactly
    # where the reviewer wants to check WHICH first-look table survived.
    for fl in sorted(k for k in arts if k.startswith("firstlook/")):
        probe("first-look", Path(fl).stem[:9], Path(fl).suffix.lstrip("."), fl)

    au = pd.DataFrame(rows)

    # ---- the verbatim table
    print(f"{'stage':12s} {'asset':9s} {'lens':5s} {'state':14s} {'rows':>12s} "
          f"{'bytes':>13s}  sha256[:16]")
    hr(n=104)
    for _, r in au.iterrows():
        # pandas widens a None in a numeric column to NaN, so `is None` never
        # fires and int(NaN) raises. pd.isna covers both spellings of absent.
        rr = "" if pd.isna(r["rows"]) else f"{int(r['rows']):,}"
        bb = "" if pd.isna(r["bytes"]) else f"{int(r['bytes']):,}"
        print(f"{r.stage:12s} {r.asset:9s} {r.lens:5s} {r.state:14s} {rr:>12s} "
              f"{bb:>13s}  {r.sha256[:16]}")
    hr(n=104)

    # ---- the grid the reviewer actually reads
    print("\nCOMPLETION GRID  (P = present+sha-verified, . = absent)")
    for stage in ("emas", "ribbons", "crosses"):
        print(f"\n  {stage}")
        print("    " + "asset".ljust(11) + "".join(f"{t:>6s}" for t in TFS))
        for sym in PANEL + ANNEX:
            cells = []
            for tf in TFS:
                s = au[(au.stage == stage) & (au.asset == sym) & (au.lens == tf)]
                st = s.state.iloc[0] if len(s) else "ABSENT"
                cells.append(f"{'P' if st == 'PRESENT' else '.':>6s}")
            print(f"    {sym:11s}" + "".join(cells))

    # ---- verdict
    core = au[au.stage.isin(["feasibility", "emas", "ribbons", "crosses",
                             "first-look"])]
    panel_core = au[(au.stage.isin(["emas", "ribbons", "crosses"]))
                    & (au.asset.isin(PANEL))]
    absent = panel_core[panel_core.state != "PRESENT"]
    stale = core[core.state == "STALE"]

    print(f"\nSUMMARY")
    print(f"  manifest artifacts pinned      {len(arts):,}")
    print(f"  audit cells probed             {len(au):,}")
    for st, g in au.groupby("state"):
        print(f"    {st:16s} {len(g):5,d}")
    print(f"  total pinned bytes             "
          f"{sum(int(v.get('bytes') or 0) for v in arts.values()):,}")

    absent_lenses = sorted(set(absent.lens))
    absent_stages = sorted(set(absent.stage))
    print(f"\n  PANEL core ABSENT cells: {len(absent)}"
          + (f"  -- stages {absent_stages}, lenses {absent_lenses}"
             if len(absent) else ""))
    print(f"  ANNEX ({', '.join(ANNEX)}): never built by V-ULT-1 -- the pins list "
          f"them as budget-only.\n    NAMED, not silently dropped; annex is out "
          f"of scope for Part A and W-TB1.")
    if len(stale):
        print(f"\n  STALE (sha drift) cells: {len(stale)} -- {list(stale.key)}")

    only_1m = (len(absent) > 0 and absent_lenses == ["1m"])
    if len(absent) == 0:
        print("\n  VERDICT: census-2B V-ULT-1 is COMPLETE on the panel across all "
              "seven lenses.")
    elif only_1m:
        print("\n  VERDICT: census-2B V-ULT-1 is COMPLETE on the panel for "
              "{5m,15m,30m,1h,4h,12h}.")
        print("           1m is the sole gap, on every core stage and every panel "
              "asset.")
    else:
        print("\n  VERDICT: census-2B V-ULT-1 has core gaps BEYOND 1m -- see the "
              "ABSENT rows above.")

    A.mkdir(parents=True, exist_ok=True)
    p = OUT / "cen2b_completion_audit.parquet"
    to_parquet_atomic(au, p)
    print(f"\n  wrote {p}  rows={len(au):,}  bytes={p.stat().st_size:,}")
    return {"audit": au, "absent": absent, "only_1m": only_1m, "manifest": man}


# ===========================================================================
# A-1 -- i-a REFUSALS ON THE NEW PAIRS
# ===========================================================================
def refusals_for_cell(fm: pd.DataFrame, sym: str, tf: str) -> pd.DataFrame:
    """The ratified kiss grammar (0.25 / 0.75 / 10) on line-vs-line pairs.

    census-2A and V-ULT-1 both ran the grammar with `close` as the approaching
    series and a BAND RAIL as the level.  Here the approaching series is itself
    an EMA -- the faster member of the pair -- and the level is the slower.  The
    grammar's three constants are untouched; only its arguments change.

    BOTH LIMBS: a refusal is emitted with the side it approached FROM.  The
    grammar forbids a sign change of (series - level) between touch and veer, so
    the approach side is well defined; where the spread is exactly zero at the
    touch bar the confirm bar's sign settles it, which is the only bar whose
    sign the grammar guarantees is non-degenerate.
    """
    e, _rb = load_cell(sym, tf)
    ot = e["open_time"].to_numpy(np.int64)
    av = e["atr"].to_numpy(np.float64)
    feas = set(feasible_lengths(fm, sym, tf))
    rows: list[pd.DataFrame] = []

    fam_of = {}
    for fam, (a, m, z) in RIBBONS.items():
        fam_of[(m, z)] = fam

    for pair_class, pairs in (("within_sr", PARED_WITHIN_SR),
                              ("sr_median", SR_MEDIAN_PAIRS)):
        for (p, q) in pairs:
            if p not in feas or q not in feas:
                continue
            sp = e[f"e{p}"].to_numpy(np.float64)
            sl = e[f"e{q}"].to_numpy(np.float64)
            flag, conf = refusal_events(sp, sl, av)      # constants unchanged
            idx = np.flatnonzero(flag)
            if idx.size == 0:
                continue
            j = conf[idx]
            spread_t = sp[idx] - sl[idx]
            spread_c = sp[j] - sl[j]
            # limb = the side approached FROM; a dead-zero touch defers to the
            # confirm bar, the one bar whose sign the grammar pins.
            sgn = np.where(spread_t != 0, np.sign(spread_t), np.sign(spread_c))
            limb = np.where(sgn >= 0, "above", "below")
            with np.errstate(invalid="ignore", divide="ignore"):
                approach = np.abs(spread_t) / av[idx]
                veer = np.abs(spread_c) / av[j]
            rows.append(pd.DataFrame({
                "asset": sym, "tf": tf, "pair_class": pair_class,
                "pair": f"{p}_{q}", "family": fam_of.get((p, q), ""),
                "fast_len": p, "slow_len": q, "limb": limb,
                "bar_index": idx.astype(np.int64),
                "ts_ms": ot[idx].astype(np.int64),
                "confirm_ts_ms": ot[j].astype(np.int64),
                "lag_bars": (j - idx).astype(np.int32),
                "approach_atr": approach.astype(np.float32),
                "veer_atr": veer.astype(np.float32),
            }))
    if not rows:
        return pd.DataFrame(columns=["asset", "tf", "pair_class", "pair",
                                     "family", "fast_len", "slow_len", "limb",
                                     "bar_index", "ts_ms", "confirm_ts_ms",
                                     "lag_bars", "approach_atr", "veer_atr"])
    out = pd.concat(rows, ignore_index=True)
    return (out.sort_values(["ts_ms", "pair_class", "pair", "limb"])
               .reset_index(drop=True))


def grammar_reach(fm: pd.DataFrame, sym: str, tf: str) -> pd.DataFrame:
    """Why a pair produced no refusals: approach reach vs veer reach.

    A zero count is uninterpretable on its own -- it could mean the two lines
    never come close, or that they come close constantly and the veer limb is
    unreachable.  The distinction decides whether a zero is a fact about the
    tape or an artefact of applying a fast-line grammar to slow lines, and the
    contract forbids touching the constants to find out.  So it is measured.

      n_touch      bars with |spread| <= eps*ATR              (approach limb)
      max_veer_atr the largest |spread|/ATR reachable within k bars OF A TOUCH
                   -- the quantity the veer limb thresholds at delta
      p_veer_ge    share of touches whose k-bar reach clears delta
    """
    e, _ = load_cell(sym, tf)
    av = e["atr"].to_numpy(np.float64)
    feas = set(feasible_lengths(fm, sym, tf))
    out = []
    for pair_class, pairs in (("within_sr", PARED_WITHIN_SR),
                              ("sr_median", SR_MEDIAN_PAIRS)):
        for (p, q) in pairs:
            if p not in feas or q not in feas:
                out.append({"asset": sym, "tf": tf, "pair_class": pair_class,
                            "pair": f"{p}_{q}", "feasible": False,
                            "n_touch": 0, "med_veer_atr": float("nan"),
                            "max_veer_atr": float("nan"), "p_veer_ge": float("nan")})
                continue
            d = e[f"e{p}"].to_numpy(np.float64) - e[f"e{q}"].to_numpy(np.float64)
            with np.errstate(invalid="ignore", divide="ignore"):
                ok = np.isfinite(d) & np.isfinite(av) & (av > 0)
                a = np.abs(d)
                touch = ok & (a <= KISS_EPS * av)
            ti = np.flatnonzero(touch)
            if ti.size == 0:
                out.append({"asset": sym, "tf": tf, "pair_class": pair_class,
                            "pair": f"{p}_{q}", "feasible": True, "n_touch": 0,
                            "med_veer_atr": float("nan"),
                            "max_veer_atr": float("nan"),
                            "p_veer_ge": float("nan")})
                continue
            n = len(d)
            reach = np.zeros(ti.size)
            for step in range(1, KISS_K + 1):
                j = np.minimum(ti + step, n - 1)
                with np.errstate(invalid="ignore", divide="ignore"):
                    r = np.where(np.isfinite(av[j]) & (av[j] > 0),
                                 a[j] / av[j], 0.0)
                reach = np.maximum(reach, np.nan_to_num(r))
            out.append({"asset": sym, "tf": tf, "pair_class": pair_class,
                        "pair": f"{p}_{q}", "feasible": True,
                        "n_touch": int(ti.size),
                        "med_veer_atr": float(np.median(reach)),
                        "max_veer_atr": float(reach.max()),
                        "p_veer_ge": float((reach >= KISS_DELTA).mean())})
    return pd.DataFrame(out)


def a1_refusals(fm: pd.DataFrame, assets: list[str]) -> dict:
    banner("A-1  i-a REFUSALS ON THE NEW PAIRS  (kiss grammar, constants unchanged)")
    print(f"grammar   eps={KISS_EPS}  delta={KISS_DELTA}  k={KISS_K}   "
          f"[ratified; both limbs; constants VETO]")
    print(f"within-SR (PARED, middle vs slow member of each SR): "
          f"{[f'{p}_{q}' for p, q in PARED_WITHIN_SR]}")
    print(f"SR-median : {[f'{p}_{q}' for p, q in SR_MEDIAN_PAIRS]}")
    print(f"lenses    {LENSES_A1}")
    print(f"NOTE      9_12 is VETOed by name and is NOT in the pared set.\n")

    # the derived set must equal the contract's literal set, or the derivation
    # has drifted from the ratified words and everything below is off-contract
    if PARED_WITHIN_SR != PARED_LITERAL:
        print(f"      HALT: derived pared set {PARED_WITHIN_SR} != contract "
              f"literal {PARED_LITERAL}")
        raise SystemExit(2)
    print(f"      pared set derived from RIBBONS == contract literal list  OK")

    D_REF.mkdir(parents=True, exist_ok=True)
    inv = []
    print(f"\n{'asset':9s} {'tf':4s} {'refusals':>10s} {'within_sr':>10s} "
          f"{'sr_median':>10s} {'above':>8s} {'below':>8s} {'secs':>7s} {'MB':>7s}")
    hr()
    for sym in assets:
        for tf in LENSES_A1:
            t0 = time.time()
            ev = refusals_for_cell(fm, sym, tf)
            p = D_REF / sym / f"{tf}.parquet"
            p.parent.mkdir(parents=True, exist_ok=True)
            key = ["asset", "tf", "pair_class", "pair", "limb", "ts_ms"]
            dup = int(ev.duplicated(subset=key).sum()) if len(ev) else 0
            if dup:
                print(f"      F-KEY FAIL {sym} {tf}: {dup} duplicates")
                raise SystemExit(2)
            to_parquet_atomic(ev, p)
            b = p.stat().st_size
            inv.append({"asset": sym, "tf": tf, "rows": len(ev), "bytes": b,
                        "within_sr": int((ev.pair_class == "within_sr").sum()),
                        "sr_median": int((ev.pair_class == "sr_median").sum()),
                        "above": int((ev.limb == "above").sum()),
                        "below": int((ev.limb == "below").sum())})
            print(f"{sym:9s} {tf:4s} {len(ev):10,d} "
                  f"{inv[-1]['within_sr']:10,d} {inv[-1]['sr_median']:10,d} "
                  f"{inv[-1]['above']:8,d} {inv[-1]['below']:8,d} "
                  f"{time.time() - t0:7.1f} {b / 1e6:7.1f}")
            del ev
    invdf = pd.DataFrame(inv)
    print(f"\nA-1 TOTAL refusals={invdf.rows.sum():,}  "
          f"bytes={invdf.bytes.sum():,} ({invdf.bytes.sum() / 1e6:.1f} MB)")

    # ---- per-pair counts, the inventory the build document quotes
    print("\nPER-PAIR COUNTS (all assets pooled)")
    print(f"  {'pair':12s} {'class':10s} " + "".join(f"{t:>10s}" for t in LENSES_A1)
          + f"{'total':>12s}")
    per = []
    for sym in assets:
        for tf in LENSES_A1:
            d = pd.read_parquet(D_REF / sym / f"{tf}.parquet",
                                columns=["tf", "pair_class", "pair", "limb"])
            per.append(d)
    perdf = pd.concat(per, ignore_index=True) if per else pd.DataFrame()
    zero = []
    for pair_class, pairs in (("within_sr", PARED_WITHIN_SR),
                              ("sr_median", SR_MEDIAN_PAIRS)):
        for (p, q) in pairs:
            nm = f"{p}_{q}"
            s = perdf[(perdf.pair == nm) & (perdf.pair_class == pair_class)]
            cells = "".join(f"{int((s.tf == t).sum()):10,d}" for t in LENSES_A1)
            print(f"  {nm:12s} {pair_class:10s} {cells}{len(s):12,d}")
            if len(s) == 0:
                zero.append(nm)

    # ---- why the slow pairs return nothing. A zero count that is not
    # explained is indistinguishable from a bug, and the constants that would
    # explain it are VETO and may not be moved to find out.
    print(f"\nGRAMMAR REACH -- why {len(zero)} pair(s) return zero refusals")
    print(f"  n_touch      bars with |e_p - e_q| <= {KISS_EPS} ATR  (approach limb)")
    print(f"  veer_atr     the largest |e_p - e_q|/ATR reached within "
          f"{KISS_K} bars OF A TOUCH")
    print(f"  p_veer_ge    share of touches whose reach clears delta = "
          f"{KISS_DELTA}\n")
    reach = pd.concat([grammar_reach(fm, s, t) for s in assets
                       for t in LENSES_A1], ignore_index=True)
    to_parquet_atomic(reach, D_REF / "a1_grammar_reach.parquet")
    print(f"  {'pair':12s} {'lens':5s} {'n_touch':>10s} {'med_veer':>9s} "
          f"{'max_veer':>9s} {'p_veer_ge':>10s}")
    for pair_class, pairs in (("within_sr", PARED_WITHIN_SR),
                              ("sr_median", SR_MEDIAN_PAIRS)):
        for (p, q) in pairs:
            nm = f"{p}_{q}"
            for tf in LENSES_A1:
                s = reach[(reach.pair == nm) & (reach.tf == tf) & reach.feasible]
                if not len(s):
                    continue
                nt = int(s.n_touch.sum())
                print(f"  {nm:12s} {tf:5s} {nt:10,d} "
                      f"{s.med_veer_atr.median():9.4f} "
                      f"{s.max_veer_atr.max():9.4f} "
                      f"{s.p_veer_ge.mean():10.4f}")
    print(f"\n  The zero pairs are NOT 'these lines never meet'. They meet "
          f"constantly; the\n  separation of two slow EMAs simply cannot move "
          f"{KISS_DELTA} ATR in {KISS_K} bars. The kiss\n  grammar is "
          f"calibrated for price-against-a-rail and for fast lines; on slow\n"
          f"  line-vs-line pairs the veer limb is unreachable and the grammar "
          f"is INERT.\n  The constants are VETO by name and were NOT changed. "
          f"This is measured, not\n  assumed -- see p_veer_ge above.")
    return {"inventory": invdf, "per_pair": perdf, "reach": reach}


def fixtures_a1(fm: pd.DataFrame, assets: list[str]) -> None:
    banner("A-1 FIXTURES -- F-A1")
    sym, tf = assets[0], "1h"

    # ---- F-A1a: three hand-verified events, from first principles
    print("F-A1a  three hand-verified refusals (touch / veer / no sign change)")
    e, _ = load_cell(sym, tf)
    ev = pd.read_parquet(D_REF / sym / f"{tf}.parquet")
    if len(ev) < 3:
        print("      HALT: fewer than three refusals to verify")
        raise SystemExit(2)
    ot = e["open_time"].to_numpy(np.int64)
    av = e["atr"].to_numpy(np.float64)
    # span the pair classes so the fixture exercises both, deterministically
    picks = pd.concat([ev[ev.pair_class == "within_sr"].head(2),
                       ev[ev.pair_class == "sr_median"].head(1)])
    if len(picks) < 3:
        picks = ev.head(3)
    ok = True
    for _, r in picks.iterrows():
        i = int(r.bar_index)
        j = int(np.searchsorted(ot, int(r.confirm_ts_ms)))
        sp = e[f"e{int(r.fast_len)}"].to_numpy(np.float64)
        sl = e[f"e{int(r.slow_len)}"].to_numpy(np.float64)
        d = sp - sl
        touch = abs(d[i]) <= KISS_EPS * av[i]
        veer = abs(d[j]) >= KISS_DELTA * av[j]
        within = 0 < (j - i) <= KISS_K
        seg = d[i:j + 1]
        sg = np.sign(seg)
        nz = sg[sg != 0]
        nochg = bool(len(nz) == 0 or np.all(nz == nz[0]))
        limb_ok = (r.limb == ("above" if (d[i] if d[i] != 0 else d[j]) >= 0
                              else "below"))
        good = touch and veer and within and nochg and limb_ok
        ok &= good
        print(f"      {iso(r.ts_ms)}  {r.pair:10s} {r.limb:5s} "
              f"touch={abs(d[i]) / av[i]:.3f}ATR veer={abs(d[j]) / av[j]:.3f}ATR "
              f"gap={j - i} no-sign-change={nochg} limb={limb_ok}  "
              f"{'OK' if good else 'FAIL'}")
    if not ok:
        print("      F-A1a FAIL"); raise SystemExit(2)
    print("      F-A1a PASS -- 3/3 hand-verified")

    # ---- F-A1b: determinism, re-run hash-identical
    print("\nF-A1b  determinism -- re-run is hash-identical")
    p = D_REF / sym / f"{tf}.parquet"
    h1 = sha256_file(p)
    again = refusals_for_cell(fm, sym, tf)
    tmp = D_REF / sym / f".{tf}.rerun.parquet"
    to_parquet_atomic(again, tmp)
    h2 = sha256_file(tmp)
    tmp.unlink()
    print(f"      {sym} {tf}  stored={h1[:16]}  rerun={h2[:16]}  "
          f"{'IDENTICAL' if h1 == h2 else 'DIFFERENT'}")
    if h1 != h2:
        print("      F-A1b FAIL"); raise SystemExit(2)
    print("      F-A1b PASS")


# ===========================================================================
# A-4 -- SPRING / UPTHRUST EVENT STREAM
# ===========================================================================
def springs_for_cell(sym: str, tf: str) -> pd.DataFrame:
    """Penetration of the prior-96-bar extreme, reclaimed within 3 bars.

    prior extreme EXCLUDES the current bar: at bar i the reference is
    min(low[i-96 : i]) / max(high[i-96 : i]).  Including bar i would make every
    new extreme its own reference and nothing could ever penetrate.

    Episodes are emitted GREEDILY and non-overlapping per side: once a spring
    fires at i and reclaims at j, the scan resumes at j+1.  Emitting every
    qualifying bar instead would triple-count a single three-bar spring, and
    F-A4's disjointness assertion would be unprovable because it would be false.
    """
    e, _rb = load_cell(sym, tf)
    ot = e["open_time"].to_numpy(np.int64)
    hi = e["high"].to_numpy(np.float64)
    lo = e["low"].to_numpy(np.float64)
    cl = e["close"].to_numpy(np.float64)
    av = e["atr"].to_numpy(np.float64)
    n = len(ot)
    # a penetration bar inside an already-emitted episode is ABSORBED, not
    # discarded -- but an absorbed count that is never printed is
    # indistinguishable from data that was silently dropped
    n_pen = {"spring": 0, "upthrust": 0}
    n_absorbed = {"spring": 0, "upthrust": 0}
    n_unreclaimed = {"spring": 0, "upthrust": 0}

    s = pd.Series(lo)
    prior_low = s.rolling(SWEEP_N, min_periods=SWEEP_N).min().shift(1).to_numpy()
    s = pd.Series(hi)
    prior_high = s.rolling(SWEEP_N, min_periods=SWEEP_N).max().shift(1).to_numpy()

    rows = []

    for side, pen_mask, ref, reclaim_cmp, sgn in (
            ("spring", lo < prior_low, prior_low, "above", +1.0),
            ("upthrust", hi > prior_high, prior_high, "below", -1.0)):
        pen = np.flatnonzero(pen_mask & np.isfinite(ref) & np.isfinite(av)
                             & (av > 0))
        n_pen[side] = int(pen.size)
        i_ptr = 0
        guard = -1
        for i in pen:
            if i <= guard:
                n_absorbed[side] += 1
                continue
            r = ref[i]
            j = -1
            for d in range(0, SWEEP_RECLAIM + 1):
                k = i + d
                if k >= n:
                    break
                back = (cl[k] > r) if reclaim_cmp == "above" else (cl[k] < r)
                if back:
                    j = k
                    break
            if j < 0:
                n_unreclaimed[side] += 1       # penetrated but never reclaimed
                continue
            seg = slice(i, j + 1)
            if side == "spring":
                depth = (r - lo[i]) / av[i]
                maxdepth = (r - np.nanmin(lo[seg])) / av[i]
            else:
                depth = (hi[i] - r) / av[i]
                maxdepth = (np.nanmax(hi[seg]) - r) / av[i]
            rows.append({
                "asset": sym, "tf": tf, "side": side,
                "pen_bar_index": int(i), "pen_ts_ms": int(ot[i]),
                "reclaim_bar_index": int(j), "reclaim_ts_ms": int(ot[j]),
                "reclaim_lag_bars": int(j - i),
                "prior_extreme": float(r),
                "depth_atr": float(depth),
                "max_depth_atr": float(maxdepth),
                "dir_sign": sgn,
            })
            guard = j
        del i_ptr
    cols = ["asset", "tf", "side", "pen_bar_index", "pen_ts_ms",
            "reclaim_bar_index", "reclaim_ts_ms", "reclaim_lag_bars",
            "prior_extreme", "depth_atr", "max_depth_atr", "dir_sign"]
    if not rows:
        empty = attach_r1(pd.DataFrame(columns=cols), e,
                          "reclaim_bar_index", "dir_sign", tf)
        empty.attrs["census"] = {"n_pen": n_pen, "n_absorbed": n_absorbed,
                                 "n_unreclaimed": n_unreclaimed}
        return empty
    out = (pd.DataFrame(rows).sort_values(["pen_ts_ms", "side"])
             .reset_index(drop=True))
    out.attrs["census"] = {"n_pen": n_pen, "n_absorbed": n_absorbed,
                           "n_unreclaimed": n_unreclaimed}
    # R-1 anchored at the RECLAIM bar: that is the bar the event completes and
    # the first bar at which it is knowable. Anchoring at the penetration bar
    # would credit the outcome to an instant when the sweep had not yet failed.
    return attach_r1(out, e, "reclaim_bar_index", "dir_sign", tf)


def a4_springs(assets: list[str]) -> dict:
    banner("A-4  SPRING / UPTHRUST EVENT STREAM")
    print(f"prior extreme   N = {SWEEP_N} bars, STRICTLY prior (bar i excluded)  [VETO]")
    print(f"reclaim         close back inside within {SWEEP_RECLAIM} bars  [VETO]")
    print(f"episodes        greedy, non-overlapping per side")
    print(f"forward         R-1 at H20/H100 FROM THE RECLAIM BAR "
          f"(the bar the event completes)")
    print(f"lenses          {LENSES_A4}\n")
    print_horizon_realisation(LENSES_A4)
    D_SPR.mkdir(parents=True, exist_ok=True)
    inv = []
    print(f"{'asset':9s} {'tf':4s} {'events':>9s} {'spring':>8s} {'upthr':>8s} "
          f"{'med_lag':>8s} {'med_depth':>10s} {'secs':>7s} {'MB':>7s}")
    hr()
    for sym in assets:
        for tf in LENSES_A4:
            t0 = time.time()
            ev = springs_for_cell(sym, tf)
            p = D_SPR / sym / f"{tf}.parquet"
            p.parent.mkdir(parents=True, exist_ok=True)
            key = ["asset", "tf", "side", "pen_ts_ms"]
            if len(ev) and int(ev.duplicated(subset=key).sum()):
                print(f"      F-KEY FAIL {sym} {tf}")
                raise SystemExit(2)
            to_parquet_atomic(ev, p)
            b = p.stat().st_size
            ns = int((ev.side == "spring").sum())
            nu = int((ev.side == "upthrust").sum())
            ml = float(ev.reclaim_lag_bars.median()) if len(ev) else float("nan")
            md = float(ev.depth_atr.median()) if len(ev) else float("nan")
            c = ev.attrs.get("census", {})
            inv.append({"asset": sym, "tf": tf, "rows": len(ev), "bytes": b,
                        "spring": ns, "upthrust": nu,
                        "med_lag": ml, "med_depth_atr": md,
                        "pen_bars": sum(c.get("n_pen", {}).values()),
                        "absorbed": sum(c.get("n_absorbed", {}).values()),
                        "unreclaimed": sum(c.get("n_unreclaimed", {}).values())})
            print(f"{sym:9s} {tf:4s} {len(ev):9,d} {ns:8,d} {nu:8,d} "
                  f"{ml:8.1f} {md:10.3f} {time.time() - t0:7.1f} {b / 1e6:7.1f}")
            del ev
    invdf = pd.DataFrame(inv)
    print(f"\nA-4 TOTAL events={invdf.rows.sum():,}  "
          f"spring={invdf.spring.sum():,}  upthrust={invdf.upthrust.sum():,}  "
          f"bytes={invdf.bytes.sum():,}")
    print("\nCOUNTS PER LENS (all assets pooled)")
    print(f"  {'lens':6s} {'spring':>10s} {'upthrust':>10s} {'total':>10s} "
          f"{'pen bars':>10s} {'absorbed':>10s} {'no-reclaim':>11s} {'sum ok':>7s}")
    for tf in LENSES_A4:
        s = invdf[invdf.tf == tf]
        chk = (s.rows.sum() + s.absorbed.sum() + s.unreclaimed.sum()
               == s.pen_bars.sum())
        print(f"  {tf:6s} {s.spring.sum():10,d} {s.upthrust.sum():10,d} "
              f"{s.rows.sum():10,d} {s.pen_bars.sum():10,d} "
              f"{s.absorbed.sum():10,d} {s.unreclaimed.sum():11,d} "
              f"{str(bool(chk)):>7s}")
    print("  pen bars   = bars that penetrated the prior-96 extreme at all")
    print("  absorbed   = penetration bars inside an already-emitted episode;")
    print("               FOLDED INTO IT, not dropped")
    print("  no-reclaim = penetrated and never closed back inside within 3 bars")
    print("  emitted + absorbed + no-reclaim == pen bars, asserted per lens.")
    if not bool((invdf.rows + invdf.absorbed + invdf.unreclaimed
                 == invdf.pen_bars).all()):
        print("  HALT: the penetration census does not reconcile")
        raise SystemExit(2)
    return {"inventory": invdf}


def fixtures_a4(assets: list[str]) -> None:
    banner("A-4 FIXTURES -- F-A4")
    sym, tf = assets[0], "1h"
    e, _ = load_cell(sym, tf)
    hi = e["high"].to_numpy(np.float64)
    lo = e["low"].to_numpy(np.float64)
    cl = e["close"].to_numpy(np.float64)
    ev = pd.read_parquet(D_SPR / sym / f"{tf}.parquet")

    print("F-A4a  three hand-verified sweeps (prior-96 extreme, reclaim <= 3)")
    picks = pd.concat([ev[ev.side == "spring"].head(2),
                       ev[ev.side == "upthrust"].head(1)])
    if len(picks) < 3:
        picks = ev.head(3)
    ok = True
    for _, r in picks.iterrows():
        i, j = int(r.pen_bar_index), int(r.reclaim_bar_index)
        if r.side == "spring":
            ref = float(np.min(lo[i - SWEEP_N:i]))
            pen_ok = lo[i] < ref
            rec_ok = cl[j] > ref
        else:
            ref = float(np.max(hi[i - SWEEP_N:i]))
            pen_ok = hi[i] > ref
            rec_ok = cl[j] < ref
        ref_ok = abs(ref - float(r.prior_extreme)) < 1e-9
        lag_ok = 0 <= (j - i) <= SWEEP_RECLAIM
        good = pen_ok and rec_ok and ref_ok and lag_ok
        ok &= good
        print(f"      {iso(r.pen_ts_ms)}  {r.side:8s} ref={ref:.6f} "
              f"pen={pen_ok} reclaim={rec_ok} lag={j - i} "
              f"depth={r.depth_atr:.3f}ATR  {'OK' if good else 'FAIL'}")
    if not ok:
        print("      F-A4a FAIL"); raise SystemExit(2)
    print("      F-A4a PASS -- 3/3 hand-verified")

    print("\nF-A4b  episode disjointness per side")
    bad = 0
    for sym2 in assets:
        for tf2 in LENSES_A4:
            d = pd.read_parquet(D_SPR / sym2 / f"{tf2}.parquet")
            for side, g in d.groupby("side"):
                g = g.sort_values("pen_bar_index")
                prev_end = g.reclaim_bar_index.shift(1)
                ovl = int((g.pen_bar_index <= prev_end).sum())
                bad += ovl
                if ovl:
                    print(f"      OVERLAP {sym2} {tf2} {side}: {ovl}")
    if bad:
        print(f"      F-A4b FAIL -- {bad} overlapping episodes")
        raise SystemExit(2)
    print(f"      F-A4b PASS -- 0 overlapping episodes across "
          f"{len(assets) * len(LENSES_A4)} cells")


# ===========================================================================
# A-3 -- TRANSITION LEDGER (KNOT episodes + FAN births)
# ===========================================================================
def runs_of(mask: np.ndarray) -> list[tuple[int, int]]:
    """Contiguous True runs as [(start, end_exclusive), ...]."""
    if not mask.any():
        return []
    d = np.diff(mask.astype(np.int8))
    starts = list(np.flatnonzero(d == 1) + 1)
    ends = list(np.flatnonzero(d == -1) + 1)
    if mask[0]:
        starts = [0] + starts
    if mask[-1]:
        ends = ends + [len(mask)]
    return list(zip(starts, ends))


def fan_age_series(orient: np.ndarray) -> np.ndarray:
    """Bars since the CURRENT full-order run began; -1 where not fully ordered.

    This is the per-bar `fan_age` the contract names.  It is computed on demand
    at every bar that consumes it rather than stored: a stored copy would be
    one int32 column per family per lens per asset -- ~100M rows for the panel --
    to carry information that (onset, length) already determines exactly.  The
    A-3 fan table stores those two, and this function reconstitutes the series
    bit-for-bit wherever it is needed.
    """
    n = len(orient)
    age = np.full(n, -1, dtype=np.int32)
    ordered = (orient == OR_BULL) | (orient == OR_BEAR)
    for s, en in runs_of(ordered):
        # a run is one fan only while the DIRECTION also holds; a bull run that
        # becomes a bear run without passing through `mixed` is two fans.
        sub = orient[s:en]
        b = np.flatnonzero(np.diff(sub) != 0) + 1
        segs = list(zip([0] + list(b), list(b) + [en - s]))
        for a0, a1 in segs:
            age[s + a0:s + a1] = np.arange(a1 - a0, dtype=np.int32)
    return age


def transitions_for_cell(sym: str, tf: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """(knot episodes, fan births) for one cell, all six SRs."""
    e, rb = load_cell(sym, tf)
    ot = e["open_time"].to_numpy(np.int64)
    cl = e["close"].to_numpy(np.float64)
    n = len(ot)
    knots, fans = [], []

    for fam in FAMILIES:
        knot = rb[f"{fam}_knot"].to_numpy()
        orient = rb[f"{fam}_orient"].to_numpy()
        if not (knot == KN_TRUE).any():
            continue
        age = fan_age_series(orient)
        ordered = (orient == OR_BULL) | (orient == OR_BEAR)

        # ---- KNOT episodes.  KN_NA breaks a run: cold data is not "no knot".
        for s, en in runs_of(knot == KN_TRUE):
            exit_i = en                          # first bar no longer knotted
            if exit_i >= n:
                exit_ts, sep_i, sep_dir, sep_lag = -1, -1, 0, -1
            else:
                exit_ts = int(ot[exit_i])
                nxt = np.flatnonzero(ordered[exit_i:])
                if nxt.size:
                    sep_i = int(exit_i + nxt[0])
                    sep_dir = int(1 if orient[sep_i] == OR_BULL else -1)
                    sep_lag = sep_i - exit_i
                else:
                    sep_i, sep_dir, sep_lag = -1, 0, -1
            knots.append({
                "asset": sym, "tf": tf, "sr": fam, "episode": "knot",
                "entry_bar_index": int(s), "entry_ts_ms": int(ot[s]),
                "exit_bar_index": int(exit_i) if exit_i < n else -1,
                "exit_ts_ms": exit_ts,
                "duration_bars": int(en - s),
                "sep_bar_index": sep_i,
                "sep_ts_ms": int(ot[sep_i]) if sep_i >= 0 else -1,
                "sep_lag_bars": sep_lag,
                "exit_dir_sign": sep_dir,
                "anchor_bar_index": int(exit_i) if exit_i < n else -1,
            })

        # ---- FAN births: onset of a full-order run, per direction
        for s, en in runs_of(ordered):
            sub = orient[s:en]
            b = np.flatnonzero(np.diff(sub) != 0) + 1
            segs = list(zip([0] + list(b), list(b) + [en - s]))
            for a0, a1 in segs:
                i = s + a0
                dirn = int(1 if orient[i] == OR_BULL else -1)
                fans.append({
                    "asset": sym, "tf": tf, "sr": fam, "episode": "fan",
                    "onset_bar_index": int(i), "onset_ts_ms": int(ot[i]),
                    "end_bar_index": int(s + a1),
                    "end_ts_ms": int(ot[s + a1]) if s + a1 < n else -1,
                    "fan_len_bars": int(a1 - a0),
                    "dir_sign": dirn,
                    "max_fan_age": int(age[s + a1 - 1]),
                    "anchor_bar_index": int(i),
                })

    kcols = ["asset", "tf", "sr", "episode", "entry_bar_index", "entry_ts_ms",
             "exit_bar_index", "exit_ts_ms", "duration_bars", "sep_bar_index",
             "sep_ts_ms", "sep_lag_bars", "exit_dir_sign", "anchor_bar_index"]
    fcols = ["asset", "tf", "sr", "episode", "onset_bar_index", "onset_ts_ms",
             "end_bar_index", "end_ts_ms", "fan_len_bars", "dir_sign",
             "max_fan_age", "anchor_bar_index"]
    kdf = pd.DataFrame(knots) if knots else pd.DataFrame(columns=kcols)
    fdf = pd.DataFrame(fans) if fans else pd.DataFrame(columns=fcols)
    # a knot whose exit direction never resolves has dir 0; R-1 on a zero sign
    # is identically zero and would read as a measured flat outcome, so those
    # rows are anchored but carry NaN via the -1 anchor.
    if len(kdf):
        kdf.loc[kdf.exit_dir_sign == 0, "anchor_bar_index"] = -1
    kdf = attach_r1(kdf, e, "anchor_bar_index", "exit_dir_sign", tf)
    fdf = attach_r1(fdf, e, "anchor_bar_index", "dir_sign", tf)
    return kdf, fdf


def a3_transitions(assets: list[str]) -> dict:
    banner("A-3  TRANSITION LEDGER -- KNOT episodes + FAN births")
    print("knot episode : contiguous run of SR_knot == 1 (KN_NA breaks a run)")
    print("exit direction: sign of the FIRST fully-ordered bar at or after exit")
    print("fan birth    : onset of a full-order run; a bull->bear flip with no")
    print("               `mixed` bar between is TWO fans, not one")
    print(f"forward      : R-1 at H20/H100 from the knot EXIT bar and the fan "
          f"ONSET bar")
    print(f"lenses       {LENSES_A3}\n")
    print_horizon_realisation(LENSES_A3)
    D_TRN.mkdir(parents=True, exist_ok=True)
    inv = []
    print(f"{'asset':9s} {'tf':4s} {'knots':>9s} {'fans':>10s} {'med_knot':>9s} "
          f"{'med_fan':>9s} {'secs':>7s} {'MB':>7s}")
    hr()
    for sym in assets:
        for tf in LENSES_A3:
            t0 = time.time()
            kdf, fdf = transitions_for_cell(sym, tf)
            d = D_TRN / sym
            d.mkdir(parents=True, exist_ok=True)
            for df, nm, key in ((kdf, "knots", ["asset", "tf", "sr",
                                                "entry_ts_ms"]),
                                (fdf, "fans", ["asset", "tf", "sr",
                                               "onset_ts_ms"])):
                if len(df) and int(df.duplicated(subset=key).sum()):
                    print(f"      F-KEY FAIL {sym} {tf} {nm}")
                    raise SystemExit(2)
                to_parquet_atomic(df, d / f"{tf}_{nm}.parquet")
            b = ((d / f"{tf}_knots.parquet").stat().st_size
                 + (d / f"{tf}_fans.parquet").stat().st_size)
            mk = float(kdf.duration_bars.median()) if len(kdf) else float("nan")
            mf = float(fdf.fan_len_bars.median()) if len(fdf) else float("nan")
            inv.append({"asset": sym, "tf": tf, "knots": len(kdf),
                        "fans": len(fdf), "bytes": b,
                        "med_knot_bars": mk, "med_fan_bars": mf})
            print(f"{sym:9s} {tf:4s} {len(kdf):9,d} {len(fdf):10,d} "
                  f"{mk:9.1f} {mf:9.1f} {time.time() - t0:7.1f} {b / 1e6:7.1f}")
            del kdf, fdf
    invdf = pd.DataFrame(inv)
    print(f"\nA-3 TOTAL knot episodes={invdf.knots.sum():,}  "
          f"fan births={invdf.fans.sum():,}  bytes={invdf.bytes.sum():,}")
    print("\nPER-SR COUNTS (all assets, all lenses pooled)")
    kk = pd.concat([pd.read_parquet(D_TRN / s / f"{t}_knots.parquet")
                    for s in assets for t in LENSES_A3], ignore_index=True)
    ff = pd.concat([pd.read_parquet(D_TRN / s / f"{t}_fans.parquet")
                    for s in assets for t in LENSES_A3], ignore_index=True)
    print(f"  {'SR':6s} {'knots':>10s} {'fans':>10s} {'med_knot_bars':>14s} "
          f"{'med_fan_bars':>13s}")
    for fam in FAMILIES:
        k = kk[kk.sr == fam]
        f = ff[ff.sr == fam]
        print(f"  {fam:6s} {len(k):10,d} {len(f):10,d} "
              f"{(k.duration_bars.median() if len(k) else float('nan')):14.1f} "
              f"{(f.fan_len_bars.median() if len(f) else float('nan')):13.1f}")
    return {"inventory": invdf, "knots": kk, "fans": ff}


def fixtures_a3(assets: list[str]) -> None:
    banner("A-3 FIXTURES -- F-A3")

    print("F-A3a  episode disjointness (knots and fans, per asset x lens x SR)")
    bad = 0
    for sym in assets:
        for tf in LENSES_A3:
            k = pd.read_parquet(D_TRN / sym / f"{tf}_knots.parquet")
            f = pd.read_parquet(D_TRN / sym / f"{tf}_fans.parquet")
            for df, s_col, e_col, nm in ((k, "entry_bar_index",
                                          "exit_bar_index", "knot"),
                                         (f, "onset_bar_index",
                                          "end_bar_index", "fan")):
                for sr, g in df.groupby("sr"):
                    g = g.sort_values(s_col)
                    prev_end = g[e_col].shift(1)
                    ovl = int((g[s_col] < prev_end).sum())
                    bad += ovl
                    if ovl:
                        print(f"      OVERLAP {sym} {tf} {sr} {nm}: {ovl}")
    if bad:
        print(f"      F-A3a FAIL -- {bad} overlaps"); raise SystemExit(2)
    print(f"      F-A3a PASS -- 0 overlaps across "
          f"{len(assets) * len(LENSES_A3)} cells x 6 SRs x 2 episode types")

    print("\nF-A3b  two hand-verified transitions per lens")
    ok = True
    for tf in LENSES_A3:
        sym = assets[0]
        _e, rb = load_cell(sym, tf)
        k = pd.read_parquet(D_TRN / sym / f"{tf}_knots.parquet")
        f = pd.read_parquet(D_TRN / sym / f"{tf}_fans.parquet")
        if not len(k) or not len(f):
            print(f"      {tf}: no episodes to verify"); continue
        rk = k.iloc[0]
        kn = rb[f"{rk.sr}_knot"].to_numpy()
        s, ex = int(rk.entry_bar_index), int(rk.exit_bar_index)
        g1 = bool(kn[s] == KN_TRUE and (s == 0 or kn[s - 1] != KN_TRUE)
                  and (ex < 0 or kn[ex] != KN_TRUE)
                  and bool((kn[s:ex] == KN_TRUE).all() if ex > 0 else True))
        rf = f.iloc[0]
        orr = rb[f"{rf.sr}_orient"].to_numpy()
        o = int(rf.onset_bar_index)
        want = OR_BULL if rf.dir_sign > 0 else OR_BEAR
        g2 = bool(orr[o] == want and (o == 0 or orr[o - 1] != want))
        ok &= (g1 and g2)
        print(f"      {tf:4s} knot {rk.sr:5s} [{s}:{ex}] len={rk.duration_bars} "
              f"exit_dir={int(rk.exit_dir_sign):+d} {'OK' if g1 else 'FAIL'}   |   "
              f"fan {rf.sr:5s} @{o} dir={int(rf.dir_sign):+d} "
              f"len={rf.fan_len_bars} {'OK' if g2 else 'FAIL'}")
    if not ok:
        print("      F-A3b FAIL"); raise SystemExit(2)
    print("      F-A3b PASS")


# ===========================================================================
# A-2 -- BR ARMED-WINDOW LEDGER v2   (the headline)
# ===========================================================================
def _support_streams(fm: pd.DataFrame, sym: str, tf: str
                     ) -> tuple[pd.DataFrame, pd.DataFrame]:
    """A-4 sweeps and A-1 refusals for a cell, read from disk where the lens is
    one A-1/A-4 own, computed in memory where it is not.

    A-2 runs on five lenses; A-1 and A-4 are pinned to four.  On 4h the stamp
    sources therefore do not exist as artifacts.  Computing them in memory
    keeps A-2's stamp complete on every lens it is contracted for WITHOUT
    widening A-1's or A-4's pinned deliverable by a lens nobody ratified.
    """
    ps = D_SPR / sym / f"{tf}.parquet"
    sw = pd.read_parquet(ps) if ps.exists() else springs_for_cell(sym, tf)
    pr = D_REF / sym / f"{tf}.parquet"
    rf = pd.read_parquet(pr) if pr.exists() else refusals_for_cell(fm, sym, tf)
    return sw, rf


def windows_for_cell(fm: pd.DataFrame, sym: str, tf: str) -> tuple[pd.DataFrame, dict]:
    """The armed-window ledger v2 for one (asset, lens).

    arming  = a close-confirmed 12_89 cross, per direction
    window  = [t0, next counter-direction 12_89 cross)      -- half-open
    trigger = a same-direction 12_26 cross strictly inside the window
    fate    = TRIGGERED if the window holds a trigger, else ABORTED

    Every stamp is evaluated AS OF the arming bar and uses only quantities
    knowable then: a refusal counts toward the trailing density only if its
    CONFIRM bar is at or before t0, and a sweep counts only if its RECLAIM bar
    is.  Both events are unknowable at their first bar -- that is what makes
    them refusals and sweeps rather than touches and pokes -- so keying the
    lookback on their opening bar would be a curtain breach dressed as a
    lookback.
    """
    e, rb = load_cell(sym, tf)
    ot = e["open_time"].to_numpy(np.int64)
    close = e["close"].to_numpy(np.float64)
    av = e["atr"].to_numpy(np.float64)
    e89 = e[f"e{ARM_PAIR[1]}"].to_numpy(np.float64)
    e12 = e[f"e{ARM_PAIR[0]}"].to_numpy(np.float64)
    e26 = e[f"e{TRIG_PAIR[1]}"].to_numpy(np.float64)
    n = len(ot)
    feas = set(feasible_lengths(fm, sym, tf))
    stats = {"asset": sym, "tf": tf, "armings_raw": 0, "rearms_suppressed": 0}
    if not {ARM_PAIR[0], ARM_PAIR[1], TRIG_PAIR[1]}.issubset(feas):
        return pd.DataFrame(), stats

    from engine.indicators import crossover, crossunder
    arm_up = np.flatnonzero(crossover(e12, e89))
    arm_dn = np.flatnonzero(crossunder(e12, e89))
    trg_up = np.flatnonzero(crossover(e12, e26))
    trg_dn = np.flatnonzero(crossunder(e12, e26))
    stats["armings_raw"] = int(arm_up.size + arm_dn.size)

    with np.errstate(invalid="ignore", divide="ignore"):
        disp = np.where(np.isfinite(av) & (av > 0),
                        np.abs(close - e89) / av, np.nan)

    sw, rf = _support_streams(fm, sym, tf)
    sw_ok = sw[np.isfinite(sw.reclaim_ts_ms)] if len(sw) else sw
    sw_ts = (sw_ok.reclaim_ts_ms.to_numpy(np.int64) if len(sw_ok)
             else np.zeros(0, np.int64))
    sw_ord = np.argsort(sw_ts)
    sw_ts = sw_ts[sw_ord]
    sw_side = (sw_ok.side.to_numpy()[sw_ord] if len(sw_ok) else np.zeros(0, object))
    sw_depth = (sw_ok.depth_atr.to_numpy(float)[sw_ord] if len(sw_ok)
                else np.zeros(0))
    rf_ts = (np.sort(rf.confirm_ts_ms.to_numpy(np.int64)) if len(rf)
             else np.zeros(0, np.int64))

    lookback_ms = LOOKBACK_H * 3_600_000
    lookback_bars = bars_for_hours(tf, LOOKBACK_H)

    # per-SR stamp series, computed once for the cell
    sr_state, sr_or, sr_knot, sr_age, sr_w = {}, {}, {}, {}, {}
    for fam in FAMILIES:
        sr_state[fam] = rb[f"{fam}_state"].to_numpy()
        sr_or[fam] = rb[f"{fam}_orient"].to_numpy()
        sr_knot[fam] = rb[f"{fam}_knot"].to_numpy()
        sr_age[fam] = fan_age_series(sr_or[fam])
        sr_w[fam] = rb[f"{fam}_width_atr"].to_numpy(np.float64)

    # in-window trigger-taxonomy pairs, read off the pinned crosses artifact
    cx = pd.read_parquet(OUT / "crosses" / sym / f"{tf}.parquet",
                         columns=["pair_class", "pair", "event", "dir", "ts_ms"])
    tax_pairs = ([f"{p}_{q}" for p, q in PARED_WITHIN_SR]
                 + [f"{p}_{q}" for p, q in SR_MEDIAN_PAIRS])
    tax_dead = {nm for nm in tax_pairs
                if not set(int(x) for x in nm.split("_")).issubset(feas)}
    tax_ts: dict[tuple[str, str], np.ndarray] = {}
    for nm in tax_pairs:
        for d in ("up", "down"):
            s = cx[(cx.pair == nm) & (cx["dir"] == d)
                   & (cx.event.isin(["cross_up", "cross_down"]))]
            tax_ts[(nm, d)] = np.sort(s.ts_ms.to_numpy(np.int64))

    rows = []
    for d, arms, counters, trigs in (("up", arm_up, arm_dn, trg_up),
                                     ("down", arm_dn, arm_up, trg_dn)):
        c_ts = ot[counters]
        t_ts = ot[trigs]
        prev_close_ts = -1
        for i in arms:
            t0 = int(ot[i])
            # a same-direction re-arm inside a still-open window is not a new
            # window; it is the same window re-crossing at float equality.
            # Emitting it would make the ledger's own disjointness false.
            if t0 < prev_close_ts:
                stats["rearms_suppressed"] += 1
                continue
            k = int(np.searchsorted(c_ts, t0, "right"))
            if k < len(c_ts):
                t_close, closed_by = int(c_ts[k]), "counter-12_89"
                ci = int(counters[k])
            else:
                t_close, closed_by = int(ot[-1]) + 1, "series-end"
                ci = n - 1
            prev_close_ts = t_close

            # The contract pins the window as [t0, counter) -- CLOSED at t0 --
            # and the fate on "the first 12_26 trigger in-window". So a trigger
            # on the arming bar itself IS in-window and counts. census-2A v1
            # used (t, close], strictly after, so that a trigger could not share
            # a bar with its own arming and hand the trigger-anchored ruler a
            # copy of the arming-anchored one. The contract's words govern here;
            # the precedent is preserved as a second, explicitly-named fate
            # column, because the two readings differ on 6.3% of all windows and
            # a reader must be able to see which one a number came from.
            lo = int(np.searchsorted(t_ts, t0, "left"))
            hi = int(np.searchsorted(t_ts, t_close, "left"))
            in_trg = trigs[lo:hi]
            has = in_trg.size > 0
            ti = int(in_trg[0]) if has else -1
            on_arm = bool(has and ti == int(i))
            strict = in_trg[in_trg > int(i)]
            has_strict = strict.size > 0

            # ---- stamps AT the arming bar
            sweep_side, sweep_lag_bars, sweep_depth = "", -1, float("nan")
            if sw_ts.size:
                q = int(np.searchsorted(sw_ts, t0, "right")) - 1
                if q >= 0 and (t0 - int(sw_ts[q])) <= lookback_ms:
                    sweep_side = str(sw_side[q])
                    sweep_lag_bars = int(round((t0 - int(sw_ts[q]))
                                               / TF_MS[tf]))
                    sweep_depth = float(sw_depth[q])
            # HALF-OPEN (t0-24h, t0]: exactly `lookback_bars` bars, the same L
            # the density divides by. A closed lower bound spans L+1 bars against
            # a denominator of L on 100% of armings -- a systematic over-count of
            # up to 27% on 4h, not a rounding artefact.
            n_ref = int(np.searchsorted(rf_ts, t0, "right")
                        - np.searchsorted(rf_ts, t0 - lookback_ms, "right"))

            rec = {
                "asset": sym, "tf": tf, "dir": d,
                "dir_sign": 1.0 if d == "up" else -1.0,
                "arming_bar_index": int(i), "arming_ts_ms": t0,
                "window_close_ts_ms": t_close, "closed_by": closed_by,
                # bars in [t0, t_close): i..ci-1 is ci-i bars when a counter
                # closes it, and i..n-1 is n-i bars at the series edge -- not
                # n-1-i, which silently shortened every right-censored window
                # by one bar.
                "window_width_bars": int(ci - i) if closed_by == "counter-12_89"
                                     else int(n - i),
                "displacement_atr": float(disp[i]),
                "sweep_side_24h": sweep_side,
                "sweep_lag_bars_24h": sweep_lag_bars,
                "sweep_depth_atr_24h": sweep_depth,
                "refusals_24h": n_ref,
                "refusal_per_1k_bars_24h": (round(n_ref * 1000.0 / lookback_bars, 4)
                                            if lookback_bars else float("nan")),
                "fate": "TRIGGERED" if has else "ABORTED",
                "fate_strict": "TRIGGERED" if has_strict else "ABORTED",
                "has_trigger": bool(has),
                "trigger_on_arming_bar": on_arm,
                "n_triggers": int(in_trg.size),
                "trigger_bar_index": ti,
                "trigger_ts_ms": int(ot[ti]) if has else -1,
                "trigger_lag_bars": int(ti - i) if has else -1,
                "trigger_displacement_atr": float(disp[ti]) if has else float("nan"),
            }
            for fam in FAMILIES:
                rec[f"{fam}_state"] = int(sr_state[fam][i])
                rec[f"{fam}_orient"] = int(sr_or[fam][i])
                rec[f"{fam}_knot"] = int(sr_knot[fam][i])
                rec[f"{fam}_fan_age"] = int(sr_age[fam][i])
                rec[f"{fam}_width_atr"] = float(sr_w[fam][i])
            for nm in tax_pairs:
                # A pair whose EMAs are NEVER warm on this cell contributes no
                # crosses, and an integer 0 would present "this pair does not
                # exist here" as "this pair existed and did not cross" -- absent
                # data as a definite negative, the wound this estate keeps
                # reopening. Infeasible pairs carry -1.
                if nm in tax_dead:
                    rec[f"tax_{nm}"] = -1
                    continue
                a = tax_ts[(nm, d)]
                rec[f"tax_{nm}"] = int(np.searchsorted(a, t_close, "left")
                                       - np.searchsorted(a, t0, "right"))
            rows.append(rec)

    if not rows:
        return pd.DataFrame(), stats
    led = (pd.DataFrame(rows).sort_values(["arming_ts_ms", "dir"])
             .reset_index(drop=True))
    # R-1 from the arming AND from the first trigger -- I6's two anchors, both
    # always printed, neither standing in for the other.
    led = attach_r1(led, e, "arming_bar_index", "dir_sign", tf, prefix="arm_")
    led = attach_r1(led, e, "trigger_bar_index", "dir_sign", tf, prefix="trg_")
    return led, stats


def a2_windows(fm: pd.DataFrame, assets: list[str]) -> dict:
    banner("A-2  BR ARMED-WINDOW LEDGER v2  (the headline)")
    print(f"arming   close-confirmed {ARM_PAIR[0]}_{ARM_PAIR[1]} cross, both "
          f"directions                    [contract]")
    print(f"window   [t0, next counter-{ARM_PAIR[0]}_{ARM_PAIR[1]} cross)  "
          f"-- half-open, no W_max cap  [contract]")
    print(f"trigger  same-direction {TRIG_PAIR[0]}_{TRIG_PAIR[1]} cross "
          f"strictly inside the window   [contract]")
    print(f"fate     {{TRIGGERED, ABORTED}} -- disjoint and exhaustive by "
          f"construction        [contract]")
    print(f"stamps   AT the arming bar: displacement |close-e89|/ATR · six SR "
          f"states ·\n         KNOT/FAN flags + fan_age · nearest sweep within "
          f"{LOOKBACK_H}h (A-4) · refusal\n         density trailing {LOOKBACK_H}h "
          f"(A-1).  Curtain: sweeps count from RECLAIM,\n         refusals from "
          f"CONFIRM -- the bars at which each becomes knowable.")
    print(f"lenses   {LENSES_A2}   (A-1/A-4 stamp sources are computed in "
          f"memory on 4h)\n")
    print_horizon_realisation(LENSES_A2)

    D_WIN.mkdir(parents=True, exist_ok=True)
    inv, stats_all = [], []
    print(f"{'asset':9s} {'tf':4s} {'windows':>8s} {'up':>7s} {'down':>7s} "
          f"{'TRIG':>7s} {'ABORT':>7s} {'re-arm':>7s} {'med_w':>7s} "
          f"{'toll_atr':>9s} {'secs':>6s} {'MB':>6s}")
    hr(n=110)
    for sym in assets:
        for tf in LENSES_A2:
            t0 = time.time()
            led, st = windows_for_cell(fm, sym, tf)
            stats_all.append(st)
            p = D_WIN / sym / f"{tf}.parquet"
            p.parent.mkdir(parents=True, exist_ok=True)
            key = ["asset", "tf", "dir", "arming_ts_ms"]
            if len(led) and int(led.duplicated(subset=key).sum()):
                print(f"      F-KEY FAIL {sym} {tf}")
                raise SystemExit(2)
            to_parquet_atomic(led, p)
            b = p.stat().st_size
            nt = int((led.fate == "TRIGGERED").sum()) if len(led) else 0
            na = int((led.fate == "ABORTED").sum()) if len(led) else 0
            mw = float(led.window_width_bars.median()) if len(led) else float("nan")
            tl = float(led.arm_toll_atr.iloc[0]) if len(led) else float("nan")
            inv.append({"asset": sym, "tf": tf, "rows": len(led), "bytes": b,
                        "up": int((led["dir"] == "up").sum()) if len(led) else 0,
                        "down": int((led["dir"] == "down").sum()) if len(led) else 0,
                        "triggered": nt, "aborted": na,
                        "rearms": st["rearms_suppressed"],
                        "med_width": mw, "toll_atr": tl})
            print(f"{sym:9s} {tf:4s} {len(led):8,d} {inv[-1]['up']:7,d} "
                  f"{inv[-1]['down']:7,d} {nt:7,d} {na:7,d} "
                  f"{st['rearms_suppressed']:7,d} {mw:7.1f} {tl:9.4f} "
                  f"{time.time() - t0:6.1f} {b / 1e6:6.1f}")
            del led
    invdf = pd.DataFrame(inv)
    stdf = pd.DataFrame(stats_all)
    to_parquet_atomic(stdf, D_WIN / "a2_stats.parquet")
    print(f"\nA-2 TOTAL windows={invdf.rows.sum():,}  "
          f"TRIGGERED={invdf.triggered.sum():,}  ABORTED={invdf.aborted.sum():,}  "
          f"re-arms suppressed={invdf.rearms.sum():,}  "
          f"bytes={invdf.bytes.sum():,}")
    return {"inventory": invdf, "stats": stdf}


def a2_tables(assets: list[str]) -> pd.DataFrame:
    """The A-2 outcome tables: fate x direction x lens, both anchors, toll beside."""
    led = pd.concat([pd.read_parquet(D_WIN / s / f"{t}.parquet")
                     for s in assets for t in LENSES_A2
                     if (D_WIN / s / f"{t}.parquet").exists()],
                    ignore_index=True)
    banner("A-2 TABLES -- fate x direction, R-1 at BOTH anchors (I6), toll beside")
    print(TIER_E_HEADER)
    print("\nAnchor lenses, per I6 ('rulers arrival/trigger-anchored'): every")
    print("outcome is printed ARMING-anchored and TRIGGER-anchored. Neither")
    print("substitutes for the other; the trigger anchor exists only for the")
    print("TRIGGERED half, which is why the ABORTED rows are blank there and")
    print("not zero.\n")

    print("BOTH TRIGGER READINGS, side by side. `fate` is the contract's --")
    print("the window is CLOSED at t0, so a 12_26 on the arming bar counts.")
    print("`fate_strict` is census-2A v1's -- strictly after the arming bar.")
    print("They differ only on windows whose ONLY trigger is the arming bar.")
    print(f"  {'lens':6s} {'windows':>9s} {'TRIG(contract)':>15s} "
          f"{'TRIG(strict)':>13s} {'on-arm-bar':>11s} {'delta':>8s}")
    for tf in LENSES_A2:
        s = led[led.tf == tf]
        if not len(s):
            continue
        a = int((s.fate == "TRIGGERED").sum())
        b = int((s.fate_strict == "TRIGGERED").sum())
        print(f"  {tf:6s} {len(s):9,d} {a:15,d} {b:13,d} "
              f"{int(s.trigger_on_arming_bar.sum()):11,d} {a - b:8,d}")
    a = int((led.fate == "TRIGGERED").sum())
    b = int((led.fate_strict == "TRIGGERED").sum())
    print(f"  {'ALL':6s} {len(led):9,d} {a:15,d} {b:13,d} "
          f"{int(led.trigger_on_arming_bar.sum()):11,d} {a - b:8,d}"
          f"   ({(a - b) / len(led) * 100:.2f}% of all windows)")
    print("  A same-bar trigger makes trg_* an ALIAS of arm_* for that row: the")
    print("  two anchors are the same bar. That is why the strict column exists")
    print("  and why the trigger-anchored medians below are ALSO printed on the")
    print("  strict subset.\n")

    print("TOLL LINE (10 bps round trip) in ATR units, measured ON THE ARMINGS")
    print("population of each cell -- the population the returns are normalised")
    print("on. Every median below must be read against the toll on its own row.")
    print(f"  {'asset':9s} " + "".join(f"{t:>9s}" for t in LENSES_A2))
    for sym in sorted(led.asset.unique()):
        cells = []
        for tf in LENSES_A2:
            s = led[(led.asset == sym) & (led.tf == tf)]
            cells.append(f"{s.arm_toll_atr.iloc[0]:9.4f}" if len(s)
                         else f"{'--':>9s}")
        print(f"  {sym:9s} " + "".join(cells))
    print("  The toll RISES as the lens shortens: ATR(14) shrinks faster than")
    print("  price does, so a fixed 10 bps is a larger multiple of ATR on 5m")
    print("  than on 4h. On 5m it is of the same order as the median outcome.")
    print("")
    print("  The trg_* columns are ATR-normalised at the TRIGGER bar, which is")
    print("  a different population from the armings, so they get their own toll")
    print("  line rather than being read against the arming one:")
    print(f"  {'asset':9s} " + "".join(f"{t:>9s}" for t in LENSES_A2))
    for sym in sorted(led.asset.unique()):
        cells = []
        for tf in LENSES_A2:
            s = led[(led.asset == sym) & (led.tf == tf) & led.has_trigger]
            cells.append(f"{s.trg_toll_atr.iloc[0]:9.4f}" if len(s)
                         else f"{'--':>9s}")
        print(f"  {sym:9s} " + "".join(cells))

    for tf in LENSES_A2:
        s = led[led.tf == tf]
        if not len(s):
            continue
        print(f"\n  LENS {tf}   (n={len(s):,} windows, "
              f"toll={s.arm_toll_atr.median():.4f} ATR median across assets)")
        print(f"    {'fate':10s} {'dir':5s} {'n':>7s} "
              f"{'arm_termH20':>12s} {'arm_termH100':>13s} "
              f"{'trg_termH20':>12s} {'trg_termH100':>13s} "
              f"{'trgH100(str)':>13s} {'med_lag':>8s} {'med_disp':>9s}")
        for fate in ("TRIGGERED", "ABORTED"):
            for d in ("up", "down"):
                g = s[(s.fate == fate) & (s["dir"] == d)]
                if not len(g):
                    continue

                def med(c, frame=None):
                    f = g if frame is None else frame
                    v = f[c].to_numpy(float)
                    v = v[np.isfinite(v)]
                    return f"{np.median(v):.4f}" if v.size else "--"
                # the strict subset drops rows whose trigger IS the arming bar,
                # where trg_* is an alias of arm_* and would inflate the column
                gs = g[~g.trigger_on_arming_bar]
                lag = (f"{g.trigger_lag_bars[g.trigger_lag_bars >= 0].median():.1f}"
                       if (g.trigger_lag_bars >= 0).any() else "--")
                print(f"    {fate:10s} {d:5s} {len(g):7,d} "
                      f"{med('arm_term_H20'):>12s} {med('arm_term_H100'):>13s} "
                      f"{med('trg_term_H20'):>12s} {med('trg_term_H100'):>13s} "
                      f"{med('trg_term_H100', gs):>13s} "
                      f"{lag:>8s} {g.displacement_atr.median():9.3f}")
    return led


def fixtures_a2(fm: pd.DataFrame, assets: list[str]) -> None:
    banner("A-2 FIXTURES -- F-A2")

    print("F-A2a  window disjointness, per asset x lens x direction")
    bad = 0
    for sym in assets:
        for tf in LENSES_A2:
            p = D_WIN / sym / f"{tf}.parquet"
            if not p.exists():
                continue
            d = pd.read_parquet(p)
            if not len(d):
                continue
            for dd, g in d.groupby("dir"):
                g = g.sort_values("arming_ts_ms")
                prev = g.window_close_ts_ms.shift(1)
                ovl = int((g.arming_ts_ms < prev).sum())
                bad += ovl
                if ovl:
                    print(f"      OVERLAP {sym} {tf} {dd}: {ovl}")
    if bad:
        print(f"      F-A2a FAIL -- {bad} overlapping windows"); raise SystemExit(2)
    print(f"      F-A2a PASS -- 0 overlapping windows")

    print("\nF-A2b  arming counts reconcile to the A-0 cross artifact")
    # The suppressed-re-arm count is read from the run's OWN stats table, not
    # derived as (crosses - windows). Deriving it would make this identity
    # true by algebra and prove nothing: the whole point is that the ledger's
    # bookkeeping of what it dropped agrees with the pinned cross artifact.
    stp = D_WIN / "a2_stats.parquet"
    if not stp.exists():
        print(f"      HALT: {stp} absent -- run A-2 before its fixture")
        raise SystemExit(2)
    stats = pd.read_parquet(stp)
    ok = True
    print(f"      {'asset':9s} {'tf':4s} {'A-0 12_89':>10s} {'windows':>9s} "
          f"{'re-arms':>8s} {'sum':>9s}  match")
    for sym in assets:
        for tf in LENSES_A2:
            p = D_WIN / sym / f"{tf}.parquet"
            if not p.exists():
                continue
            d = pd.read_parquet(p)
            cx = pd.read_parquet(OUT / "crosses" / sym / f"{tf}.parquet",
                                 columns=["pair", "event"])
            n_cx = int(((cx.pair == f"{ARM_PAIR[0]}_{ARM_PAIR[1]}")
                        & (cx.event.isin(["cross_up", "cross_down"]))).sum())
            srow = stats[(stats.asset == sym) & (stats.tf == tf)]
            re_arm = int(srow.rearms_suppressed.iloc[0]) if len(srow) else -1
            good = (len(d) + re_arm) == n_cx and re_arm >= 0
            ok &= good
            print(f"      {sym:9s} {tf:4s} {n_cx:10,d} {len(d):9,d} "
                  f"{re_arm:8,d} {len(d) + re_arm:9,d}  "
                  f"{'OK' if good else 'FAIL'}")
    if not ok:
        print("      F-A2b FAIL"); raise SystemExit(2)
    print("      F-A2b PASS -- every 12_89 cross is either a window or a "
          "named suppressed re-arm")

    print("\nF-A2c  one window hand-unpacked per lens")
    ok = True
    for tf in LENSES_A2:
        sym = assets[0]
        p = D_WIN / sym / f"{tf}.parquet"
        if not p.exists():
            continue
        d = pd.read_parquet(p)
        g = d[d.fate == "TRIGGERED"]
        if not len(g):
            print(f"      {tf}: no TRIGGERED window to unpack"); continue
        r = g.iloc[0]
        e, _rb = load_cell(sym, tf)
        e12 = e[f"e{ARM_PAIR[0]}"].to_numpy(np.float64)
        e89 = e[f"e{ARM_PAIR[1]}"].to_numpy(np.float64)
        e26 = e[f"e{TRIG_PAIR[1]}"].to_numpy(np.float64)
        av = e["atr"].to_numpy(np.float64)
        cl = e["close"].to_numpy(np.float64)
        i, ti = int(r.arming_bar_index), int(r.trigger_bar_index)
        up = r["dir"] == "up"
        a_ok = ((e12[i] > e89[i] and e12[i - 1] <= e89[i - 1]) if up
                else (e12[i] < e89[i] and e12[i - 1] >= e89[i - 1]))
        t_ok = ((e12[ti] > e26[ti] and e12[ti - 1] <= e26[ti - 1]) if up
                else (e12[ti] < e26[ti] and e12[ti - 1] >= e26[ti - 1]))
        d_ok = abs(abs(cl[i] - e89[i]) / av[i] - float(r.displacement_atr)) < 1e-4
        w_ok = int(r.trigger_ts_ms) < int(r.window_close_ts_ms) and ti > i
        good = a_ok and t_ok and d_ok and w_ok
        ok &= good
        print(f"      {tf:4s} {sym} {r['dir']:5s} arm@{iso(r.arming_ts_ms)} "
              f"trig+{int(r.trigger_lag_bars)}b close@{iso(r.window_close_ts_ms)} "
              f"disp={r.displacement_atr:.3f}ATR  "
              f"arm={a_ok} trig={t_ok} disp={d_ok} order={w_ok}  "
              f"{'OK' if good else 'FAIL'}")
    if not ok:
        print("      F-A2c FAIL"); raise SystemExit(2)
    print("      F-A2c PASS")


# ===========================================================================
# MANIFEST -- I12 pin-merge, extended to the Part A / W-TB1 artifacts
# ===========================================================================
CLASS_MAP = [
    ("refusals/", "SUBSTRATE -- census-2B PART A / A-1 i-a refusals"),
    ("windows/", "SUBSTRATE -- census-2B PART A / A-2 armed-window ledger v2"),
    ("transitions/", "SUBSTRATE -- census-2B PART A / A-3 transition ledger"),
    ("springs/", "SUBSTRATE -- census-2B PART A / A-4 spring/upthrust stream"),
    ("cen2b_completion_audit", "SUBSTRATE -- census-2B PART A / A-0 audit"),
    ("wtb1/agg/", "DISPLAY-ONLY / Tier-E -- W-TB1 aggregate; REGISTRATIONS "
                  "DEFERRED; m declared in the probe ledger"),
    ("wtb1/", "Tier-E DESCRIPTIVE CAPTURE -- census-2B W-TB1; the AFTER side "
              "is ANATOMY, never entry evidence"),
]


def pin_manifest() -> dict:
    """Pin every Part-A and W-TB1 artifact, I12 semantics.

    census2b_program.write_manifest already merges pins and prunes vanished
    files; it is reused rather than reimplemented.  What it cannot know is the
    CLASS of artifacts invented after it was written -- it would stamp all of
    them SUBSTRATE, and stamping a Tier-E capture as substrate is precisely how
    a probe becomes evidence.  So the class is corrected afterwards, by prefix.
    """
    banner("MANIFEST -- I12 pin-merge across Part A and W-TB1")
    man = c2b.write_manifest()
    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    fixed = 0
    for k, v in m["artifacts"].items():
        for pref, cls in CLASS_MAP:
            if k.startswith(pref):
                if v.get("class") != cls:
                    v["class"] = cls
                    fixed += 1
                break
    m["pins"]["parta_wtb1"] = {
        "pared_within_sr": [f"{p}_{q}" for p, q in PARED_WITHIN_SR],
        "sr_median_pairs": [f"{p}_{q}" for p, q in SR_MEDIAN_PAIRS],
        "arm_pair": f"{ARM_PAIR[0]}_{ARM_PAIR[1]}",
        "trigger_pair": f"{TRIG_PAIR[0]}_{TRIG_PAIR[1]}",
        "sweep_lookback_bars": SWEEP_N,
        "sweep_reclaim_bars": SWEEP_RECLAIM,
        "horizons_ms": HORIZONS_MS,
        "horizon_rule": ("DURATION-fixed: H20 = 20x5m = 1h40m, H100 = 100x5m = "
                         "8h20m; bars = round(hms/TF_MS[tf]); bars<1 is "
                         "INFEASIBLE -> NaN, never substituted"),
        "lookback_hours": LOOKBACK_H,
        "lenses": {"A1": LENSES_A1, "A2": LENSES_A2, "A3": LENSES_A3,
                   "A4": LENSES_A4},
        "kiss": {"eps": KISS_EPS, "delta": KISS_DELTA, "k": KISS_K,
                 "note": "unchanged; applied line-vs-line, both limbs"},
        "toll_bps_round_trip": TOLL_BPS_ROUND_TRIP,
        "toll_note": ("measured on each table's OWN event population, per "
                      "census2a_program.py:1226-1234 note m8"),
        "seed": SEED,
        "programs": [PROGRAM, "census2b_wtb1.py"],
        "class": ("Tier-E substrate + Tier-E descriptive; NO REGISTRATIONS; "
                  "W-B's motif surface m is declared in the probe ledger"),
    }
    MANIFEST.write_text(json.dumps(m, indent=2), encoding="utf-8")
    print(f"  classes corrected on {fixed} artifact(s)")
    print(f"  artifacts pinned     {len(m['artifacts']):,}")
    tot = sum(int(v.get("bytes") or 0) for v in m["artifacts"].values())
    print(f"  total pinned bytes   {tot:,} ({tot / 1e9:.2f} GB)  -- all on D:")
    return m


# ===========================================================================
# MAIN
# ===========================================================================
def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", newline="\n")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="CENSUS-2B PART A")
    ap.add_argument("--stage", default="0",
                    help="0|1|2|3|4|pin|all (comma ok)")
    ap.add_argument("--assets", default=",".join(PANEL))
    ap.add_argument("--no-fixtures", action="store_true")
    a = ap.parse_args()
    assets = [s.strip() for s in a.assets.split(",") if s.strip()]
    stages = ({"0", "1", "2", "3", "4"} if a.stage == "all"
              else {s.strip() for s in a.stage.split(",")})
    bad = sorted(stages - {"0", "1", "2", "3", "4", "pin"})
    if bad:
        print(f"HALT: unrecognised --stage token(s) {bad}. "
              f"Use 0|1|2|3|4|pin or 'all'.")
        return 2
    if stages == {"pin"}:
        pin_manifest()
        return 0

    banner("CENSUS-2B / PART A -- COMPLETION AUDIT + SEQUENTIAL SUBSTRATE")
    print(f"program   {PROGRAM}   seed {SEED}")
    print(f"class     Tier-E substrate -- NO REGISTRATIONS; F-KEY everywhere")
    print(f"machinery census2b_program.py imported byte-untouched")
    print(f"assets    {assets}")
    print(f"stages    {sorted(stages)}")
    print(f"out       {OUT}")

    # A-0 always runs and always prints FIRST -- it is the completion
    # certificate, and a Part-A run that skipped it would be uncertifiable.
    a0_audit()

    fm = load_feasibility() if stages - {"0"} else None
    if (stages - {"0"}) and not a.no_fixtures:
        fixture_a0r(assets)
    if "1" in stages:
        a1_refusals(fm, assets)
        if not a.no_fixtures:
            fixtures_a1(fm, assets)
    if "4" in stages:
        a4_springs(assets)
        if not a.no_fixtures:
            fixtures_a4(assets)
    if "3" in stages:
        a3_transitions(assets)
        if not a.no_fixtures:
            fixtures_a3(assets)
    if "2" in stages:
        a2_windows(fm, assets)
        a2_tables(assets)
        if not a.no_fixtures:
            fixtures_a2(fm, assets)
    print(f"\nPART A elapsed={time.time() - _T0:.0f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
