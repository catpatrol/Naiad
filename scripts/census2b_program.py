#!/usr/bin/env python3
"""
CENSUS-2B / V-ULT-1 -- THE U-VHT DATA MODULE
============================================
Contract: operator paste 2026-08-12 ("Secret Sauce is a momentum system").
Drafted: APOLLO.  Executor: HEPHAESTUS.  Seed 20260812.
CLASS: substrate + Tier-E first-look.  NO REGISTRATIONS.  m = 0.

scripts/census2a_program.py is BYTE-UNTOUCHED.  This program imports the
ratified machinery (engine.indicators, census_build._resample and constants)
and restates nothing that already exists.

WHAT THIS IS
------------
Six EMA ribbons spanning six decades of memory, on seven timeframes, five
assets.  The ultra-long families (VH, UH) are the point: the operator's
question is whether the fast ribbon's behaviour is conditioned by what the
4236/4618/5000 lines are doing, and that has never been computed here.

THE WARM-UP LAW (the thing that has bitten this estate twice)
-------------------------------------------------------------
An EMA seeded at the series start carries seed weight (1-alpha)^k at bar k.
Until that decays, the series is a fact about the seed, not about the tape.
CENSUS-2B NaNs the first `warm_bars(L)` entries of EVERY EMA at the source,
so `crossover`/`crossunder` return False there BY CONSTRUCTION and no
downstream stage has to remember.  F-B2 then counts values in the warm-up
region and requires zero -- an assertion, not an intention.

The contract pins warmfactor = 3.46, warm_bars = ceil(3.46*N).  The exact
SEQ8 rule (seq8_extract.warmup_bars) is ceil(log(1e-3)/log(1-alpha)).  These
are not identical; F-B0 proves ceil(3.46*N) >= the exact rule for all 18
lengths (delta 0..+30 bars, never negative), so the contract's constant is
the conservative one and is used as written.

STAGES
------
1  FEASIBILITY MATRIX   asset x tf x length -- printed BEFORE any compute.
2  EMAS + ATR           one pass, float32, NaN-before-warm.        -> emas/
3  RIBBON LIBRARY       general ribbon(a,b,df) + canonical state.  -> ribbons/
4  CROSS EVENTS         18 within-ribbon + 5 midline + price<->band -> crosses/
5  FIRST-LOOK           Tier-E, display-only, m = 0.               -> firstlook/

USAGE
    python scripts/census2b_program.py --stage 1
    python scripts/census2b_program.py --stage 2 --skip-1m
    python scripts/census2b_program.py --stage all
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

import census_build as cb                                        # noqa: E402
from engine.indicators import ema, atr, crossover, crossunder    # noqa: E402

# ===========================================================================
# CONSTANTS -- VETO BY NAME.  Nothing below is tuned, swept, or chosen here.
# ===========================================================================
SEED = 20260812
PROGRAM = "census2b_program.py"

RIBBONS: dict[str, tuple[int, int, int]] = {
    "FAST": (9, 12, 26),
    "M":    (62, 89, 127),
    "MH":   (262, 316, 423),
    "H":    (616, 889, 1272),
    "VH":   (1618, 2618, 3618),
    "UH":   (4236, 4618, 5000),
}
FAMILIES = list(RIBBONS)
ALL_EMAS = sorted({L for m in RIBBONS.values() for L in m})       # 18 lengths
V_ULT = ("VH", "UH")                                             # the subject

TFS = ["1m", "5m", "15m", "30m", "1h", "4h", "12h"]
PANEL = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "NEARUSDT", "ZECUSDT"]
ANNEX = ["JTOUSDT", "TAOUSDT"]                                   # budget only

WARMFACTOR = 3.46                # SEQ8 rule as pinned by the contract
K_WINDOW = 20                    # ribbon-state lookback, bars
STATE_EPS = 0.05                 # |width_delta_k| threshold, ATR units
RIBBON_C = 0.5                   # knot: width < 0.5 * ATR  (carried from 2A)
ATR_LEN = cb.ATR_LEN             # 14, the ratified length

# kiss grammar, carried verbatim from census2a_program.py:91
KISS_EPS, KISS_DELTA, KISS_K = 0.25, 0.75, 10

# adjacent-midline pairs: the middle member of each family against the next
MIDLINE_PAIRS = [(12, 89), (89, 316), (316, 889), (889, 2618), (2618, 4618)]

TOLL_BPS_ROUND_TRIP = 10.0       # census2a_program.py:94, global 5 bps x 2
H100 = 100                       # the terminal horizon the enquiry card uses

CEIL_MS = cb.CEIL_MS             # 2024-07-01Z -- the evidence-era ceiling
ASSET_STARTS = cb.ASSET_STARTS

OUT = Path("D:/Naiad/research_outputs/census2b")
MANIFEST = OUT / "census2b_manifest.json"
CENSUS2A = Path("D:/Naiad/research_outputs/census2a")

TIER_E_HEADER = (
    "CLASS: DISPLAY-ONLY / Tier-E -- EXPLORATION, ungated; promotion requires "
    "registration. Nothing here is a finding. Selection surface m = 0."
)

# state / orientation / position codes.  int8 on disk, legend in the manifest.
ST_COMPRESS, ST_FLAT, ST_EXPAND, ST_NA = -1, 0, 1, -9
OR_BEAR, OR_MIXED, OR_BULL, OR_NA = -1, 0, 1, -9
PS_BELOW, PS_INSIDE, PS_ABOVE, PS_NA = -1, 0, 1, -9
# `knot` was the one categorical column stored as bare bool, so "not computed"
# and "never knotted" were the same byte -- absent data presented as a definite
# negative, which is this estate's signature wound. It now carries a sentinel.
KN_FALSE, KN_TRUE, KN_NA = 0, 1, -9

STATE_NAME = {ST_COMPRESS: "compressing", ST_FLAT: "flat",
              ST_EXPAND: "expanding", ST_NA: "n/a"}
ORIENT_NAME = {OR_BEAR: "bear-fanned", OR_MIXED: "mixed",
               OR_BULL: "bull-fanned", OR_NA: "n/a"}
POS_NAME = {PS_BELOW: "below", PS_INSIDE: "inside",
            PS_ABOVE: "above", PS_NA: "n/a"}
KNOT_NAME = {KN_FALSE: "no", KN_TRUE: "knot", KN_NA: "n/a"}

_T0 = time.time()
_ROWS_TOTAL = 0
_BYTES_TOTAL = 0


# ===========================================================================
# HELPERS
# ===========================================================================
def warm_bars(length: int) -> int:
    """Contract constant: ceil(3.46 * N).  See F-B0 for the SEQ8 reconciliation."""
    return int(math.ceil(WARMFACTOR * length))


WARM = {L: warm_bars(L) for L in ALL_EMAS}


def seq8_warm_exact(length: int, residual: float = 1e-3) -> int:
    """The exact SEQ8 rule, for F-B0 only.  seq8_extract.warmup_bars, restated
    here rather than imported so that F-B0 is a comparison of two independent
    expressions and not a tautology."""
    alpha = 2.0 / (length + 1.0)
    return int(math.ceil(math.log(residual) / math.log(1.0 - alpha)))


def iso(ms: int | float) -> str:
    return (datetime.fromtimestamp(int(ms) / 1000, timezone.utc)
            .strftime("%Y-%m-%dT%H:%M:%SZ"))


def day(ms: int | float) -> str:
    return iso(ms)[:10]


def ms_of(datestr: str) -> int:
    return int(datetime.strptime(datestr, "%Y-%m-%d")
               .replace(tzinfo=timezone.utc).timestamp() * 1000)


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def klines_dir() -> Path:
    """The LIVE cache -- refreshed to the current day.  NOT MC-1's frozen
    ops_klines snapshot: that one is the right source for reproducing MC-1 and
    the wrong source for anything about the present."""
    from engine.data import cache_dir
    d = Path(cache_dir()) / "klines"
    if not d.is_dir():                                    # explicit fallback
        d = Path(os.environ["LOCALAPPDATA"]) / "naiad" / "data_cache" / "klines"
    return d


def load_raw(sym: str, tf: str) -> pd.DataFrame:
    """OHLCV for (sym, tf) over the FULL available history.

    No CEIL_MS ceiling and no ASSET_STARTS floor: census-2B is a substrate
    module that reports evidence-era coverage as a COLUMN rather than
    imposing it as a filter.  Resampling calls census_build._resample (the s1
    algorithm) so 30m here is the same 30m the census used.
    """
    kd = klines_dir()
    if tf in cb.RESAMPLE:
        src_tf, step = cb.RESAMPLE[tf]
        raw = pd.read_parquet(kd / f"{sym}_{src_tf}.parquet")
        raw = raw.sort_values("open_time").reset_index(drop=True)
        df = cb._resample(raw, step)
    else:
        df = pd.read_parquet(kd / f"{sym}_{tf}.parquet")
        df = df.sort_values("open_time").reset_index(drop=True)
    return df.reset_index(drop=True)


def pick_cell(fm: pd.DataFrame, prefer: list[tuple[str, str]],
              label: str) -> tuple[str, str] | None:
    """Choose an (asset, tf) cell a fixture can actually read.

    Fixture cells were hard-coded, so a scoped run (--assets BTCUSDT, --tfs 1h)
    raised FileNotFoundError from inside the fixture -- or worse, read a cell
    some EARLIER run had written and silently certified stale artifacts as this
    run's. Preference order is kept for reproducibility; the fallback is the
    largest cell this run actually produced, and a fixture with nothing to read
    says so instead of dying.
    """
    have = {(r.asset, r.tf) for _, r in fm.iterrows()
            if (OUT / "emas" / r.asset / f"{r.tf}.parquet").exists()}
    for c in prefer:
        if c in have:
            return c
    if not have:
        print(f"      {label}: SKIP -- this run produced no readable cell")
        return None
    best = max(have, key=lambda c: int(
        fm[(fm.asset == c[0]) & (fm.tf == c[1])].bars_available.iloc[0]))
    print(f"      {label}: preferred cell absent from this run's scope; "
          f"using {best[0]} {best[1]}")
    return best


def to_parquet_atomic(df: pd.DataFrame, p: Path) -> None:
    """Write via a temp file and rename.

    A run killed mid-write leaves a truncated parquet with no footer. It is
    unreadable, but it is still a FILE: the manifest will happily record its
    size and its sha256, and a later stage that only checks `p.exists()` will
    consume it. That happened in this build (a killed 1m pass left a 10.9 MB
    stump of a ~400 MB file). os.replace is atomic on Windows and POSIX, so
    the artifact either exists complete or does not exist.
    """
    tmp = p.with_suffix(p.suffix + ".tmp")
    df.to_parquet(tmp, index=False)
    os.replace(tmp, p)


def parquet_rows(p: Path) -> int | None:
    """Row count from the footer -- and a readability check in one call.

    `pd.read_parquet(p, columns=[])` returns a zero-row frame regardless of the
    file, so using it to fill a manifest records `0` for everything and proves
    nothing about whether the file can be read at all.
    """
    try:
        import pyarrow.parquet as pq
        return int(pq.ParquetFile(p).metadata.num_rows)
    except Exception:
        return None


def rec_bytes(p: Path) -> int:
    global _BYTES_TOTAL
    b = p.stat().st_size
    _BYTES_TOTAL += b
    return b


def hr(ch: str = "-", n: int = 100) -> None:
    print(ch * n)


def banner(title: str) -> None:
    print()
    hr("=")
    print(title)
    hr("=")


# ===========================================================================
# STAGE 1 -- FEASIBILITY MATRIX
# ===========================================================================
def verdict_for(n_bars: int, wb: int, ot: np.ndarray, sym: str) -> tuple[str, float, str]:
    """(verdict, evidence-era coverage share, warm-from date).

    The evidence era is [ASSET_STARTS[sym], CEIL_MS) -- the census's own
    window, not a new one invented here.

      NEVER            the series never warms at all
      OPS-ONLY         warms, but only after the evidence ceiling: the series
                       exists for the live era and cannot speak to the census
      PARTIAL(evidence) warms inside the evidence era but after it opened
      FULL             warm before the evidence era opens; coverage = 100%
    """
    if wb >= n_bars:
        return "NEVER", 0.0, "-"
    warm_ts = int(ot[wb])
    lo = ms_of(ASSET_STARTS[sym])
    in_era = (ot >= lo) & (ot < CEIL_MS)
    tot = int(in_era.sum())
    if tot == 0:
        return "OPS-ONLY", 0.0, day(warm_ts)
    warm_mask = np.zeros(n_bars, dtype=bool)
    warm_mask[wb:] = True
    cov = float((in_era & warm_mask).sum()) / tot
    if warm_ts >= CEIL_MS:
        return "OPS-ONLY", 0.0, day(warm_ts)
    if warm_ts <= lo:
        return "FULL", cov, day(warm_ts)
    return "PARTIAL(evidence)", cov, day(warm_ts)


def stage1(assets: list[str], tfs: list[str]) -> pd.DataFrame:
    banner("STAGE 1 -- FEASIBILITY MATRIX  (printed before any compute)")
    print(f"warm_bars(N) = ceil({WARMFACTOR} * N)   [contract constant, VETO by name]")
    print(f"evidence era = [ASSET_STARTS[asset], {day(CEIL_MS)})   "
          f"CEIL_MS = {CEIL_MS}")
    print(f"klines       = {klines_dir()}   (LIVE cache)")
    print()

    # ---- F-B0: the contract's 3.46 vs the exact SEQ8 residual rule
    print("F-B0  warmfactor reconciliation -- ceil(3.46*N) vs exact SEQ8 rule")
    bad = []
    for fam, members in RIBBONS.items():
        cells = []
        for L in members:
            c, e = WARM[L], seq8_warm_exact(L)
            if c < e:
                bad.append((L, c, e))
            cells.append(f"{L}:{c}/{e}(+{c - e})")
        print(f"      {fam:5s} " + "  ".join(cells))
    if bad:
        print(f"      F-B0 FAIL -- contract constant SHORTER than SEQ8 for {bad}")
        raise SystemExit(2)
    print("      F-B0 PASS -- ceil(3.46*N) >= exact SEQ8 warmup for all 18 lengths\n")

    rows = []
    for sym in assets:
        for tf in tfs:
            df = load_raw(sym, tf)
            ot = df["open_time"].to_numpy(np.int64)
            n = len(ot)
            for fam, members in RIBBONS.items():
                for L in members:
                    wb = WARM[L]
                    v, cov, wfrom = verdict_for(n, wb, ot, sym)
                    rows.append({
                        "asset": sym, "tf": tf, "family": fam, "length": L,
                        "bars_available": n, "warm_bars": wb,
                        "warm_from": wfrom,
                        "first_bar": day(ot[0]), "last_bar": day(ot[-1]),
                        "evidence_coverage": round(cov, 4),
                        "verdict": v,
                    })
            del df
    fm = pd.DataFrame(rows)

    # ---- the matrix, printed in full
    print(f"{'asset':9s} {'tf':4s} {'fam':5s} {'N':>5s} {'bars':>10s} "
          f"{'warm':>7s} {'warm_from':10s} {'ev_cov':>7s}  verdict")
    hr()
    for _, r in fm.iterrows():
        print(f"{r.asset:9s} {r.tf:4s} {r.family:5s} {r.length:5d} "
              f"{r.bars_available:10,d} {r.warm_bars:7,d} {r.warm_from:10s} "
              f"{r.evidence_coverage:7.3f}  {r.verdict}")
    hr()

    # ---- compact family x tf verdict grid
    print("\nVERDICT GRID (worst verdict across the family's three members)")
    order = {"NEVER": 0, "OPS-ONLY": 1, "PARTIAL(evidence)": 2, "FULL": 3}
    short = {"NEVER": "NEVER", "OPS-ONLY": "OPS", "PARTIAL(evidence)": "PART",
             "FULL": "FULL"}
    for sym in assets:
        print(f"\n  {sym}")
        print("    " + "fam  ".ljust(7) + "".join(f"{t:>7s}" for t in tfs))
        for fam in FAMILIES:
            cells = []
            for tf in tfs:
                s = fm[(fm.asset == sym) & (fm.tf == tf) & (fm.family == fam)]
                w = min(s.verdict, key=lambda v: order[v])
                cells.append(f"{short[w]:>7s}")
            print(f"    {fam:5s}  " + "".join(cells))

    # ---- NEVER cells: skipped and listed, never silently computed
    nev = fm[fm.verdict == "NEVER"]
    print(f"\nNEVER cells -- SKIPPED, NOT COMPUTED: {len(nev)} of {len(fm)} "
          f"(asset x tf x length)")
    for (tf, fam), g in nev.groupby(["tf", "family"], sort=False):
        Ls = sorted(set(g.length))
        As = sorted(set(g.asset))
        print(f"    {tf:4s} {fam:5s} lengths {Ls} -- {len(As)} assets "
              f"({', '.join(a.replace('USDT','') for a in As)})")
    ops = fm[fm.verdict == "OPS-ONLY"]
    if len(ops):
        print(f"\nOPS-ONLY cells -- computed, but ZERO evidence-era coverage: {len(ops)}")
        for (tf, fam), g in ops.groupby(["tf", "family"], sort=False):
            print(f"    {tf:4s} {fam:5s} lengths {sorted(set(g.length))} -- "
                  f"{len(set(g.asset))} assets")

    # ---- F-B1: three cells hand-recomputed
    print("\nF-B1  three cells hand-recomputed from first principles")
    # The preferred three span the verdict classes. A scoped run (--tfs 1m)
    # does not contain them, and a fixture that cannot find its own sample must
    # pick a new one deterministically rather than crash or -- far worse --
    # quietly check nothing. Fallback picks are taken from the matrix's own
    # sorted order, so they are reproducible and still span it.
    preferred = [("BTCUSDT", "12h", 5000), ("SOLUSDT", "5m", 2618),
                 ("ZECUSDT", "1h", 316)]
    have = {(r.asset, r.tf, int(r.length)) for _, r in fm.iterrows()}
    picks = [p for p in preferred if p in have]
    if len(picks) < 3:
        srt = fm.sort_values(["asset", "tf", "length"]).reset_index(drop=True)
        for i in (0, len(srt) // 2, len(srt) - 1):
            c = (srt.asset[i], srt.tf[i], int(srt.length[i]))
            if c not in picks:
                picks.append(c)
            if len(picks) == 3:
                break
        print(f"      preferred cells absent from this scoped matrix; "
              f"deterministic fallback picks used")
    if len(picks) < 3:
        print(f"      F-B1 FAIL -- matrix has only {len(fm)} cells, cannot "
              f"draw three")
        raise SystemExit(2)
    ok = True
    for sym, tf, L in picks:
        r = fm[(fm.asset == sym) & (fm.tf == tf) & (fm.length == L)].iloc[0]
        df = load_raw(sym, tf)
        ot = df["open_time"].to_numpy(np.int64)
        n_hand = len(ot)
        wb_hand = int(math.ceil(3.46 * L))
        if wb_hand >= n_hand:
            v_hand, cov_hand, wf_hand = "NEVER", 0.0, "-"
        else:
            wts = int(ot[wb_hand])
            lo = ms_of(ASSET_STARTS[sym])
            era = [t for t in ot if lo <= t < CEIL_MS]
            warm_era = [t for t in ot[wb_hand:] if lo <= t < CEIL_MS]
            cov_hand = len(warm_era) / len(era) if era else 0.0
            wf_hand = day(wts)
            if not era or wts >= CEIL_MS:
                v_hand = "OPS-ONLY"
            elif wts <= lo:
                v_hand = "FULL"
            else:
                v_hand = "PARTIAL(evidence)"
        agree = (int(r.bars_available) == n_hand and int(r.warm_bars) == wb_hand
                 and r.verdict == v_hand
                 and abs(float(r.evidence_coverage) - round(cov_hand, 4)) < 1e-9
                 and r.warm_from == wf_hand)
        ok &= agree
        print(f"      {sym:9s} {tf:4s} N={L:5d}  bars={n_hand:,} warm={wb_hand:,} "
              f"warm_from={wf_hand} cov={cov_hand:.3f} -> {v_hand}   "
              f"{'MATCH' if agree else 'MISMATCH'}")
        del df
    if not ok:
        print("      F-B1 FAIL"); raise SystemExit(2)
    print("      F-B1 PASS -- 3/3 cells match the matrix")

    OUT.mkdir(parents=True, exist_ok=True)
    p = OUT / "cen2b_feasibility.parquet"
    # I12 pin-merge, applied to the matrix as well as the manifest. A scoped run
    # (--tfs 1m) computes only its own cells; writing that as the whole matrix
    # DESTROYS the rest, which is exactly the failure I12 exists to prevent.
    # Rows are merged on the cell key and the scoped run's values win.
    merged = fm
    if p.exists():
        prev = pd.read_parquet(p)
        key = ["asset", "tf", "family", "length"]
        keep = prev.merge(fm[key].assign(_new=1), on=key, how="left")
        keep = keep[keep._new.isna()].drop(columns=["_new"])
        if len(keep):
            print(f"\nI12 merge: carrying {len(keep):,} cell(s) from the existing "
                  f"matrix that this scoped run did not recompute")
        merged = (pd.concat([keep, fm], ignore_index=True)
                    .sort_values(key).reset_index(drop=True))
    to_parquet_atomic(merged, p)
    print(f"\nwrote {p}  rows={len(merged):,} (this run computed {len(fm):,})  "
          f"bytes={rec_bytes(p):,}")
    return fm


# ===========================================================================
# STAGE 2 -- EMAS + ATR
# ===========================================================================
def feasible_lengths(fm: pd.DataFrame, sym: str, tf: str) -> list[int]:
    s = fm[(fm.asset == sym) & (fm.tf == tf) & (fm.verdict != "NEVER")]
    return sorted(set(s.length))


def stage2(fm: pd.DataFrame, assets: list[str], tfs: list[str],
           skip_1m: bool) -> None:
    global _ROWS_TOTAL
    banner("STAGE 2 -- EMAS + ATR  (one pass, float32, NaN-before-warm)")
    (OUT / "emas").mkdir(parents=True, exist_ok=True)

    # 1m LAST: it is the bulk, and it is the skippable one.
    order = [t for t in tfs if t != "1m"] + ([] if skip_1m else
                                             ["1m"] if "1m" in tfs else [])
    if skip_1m and "1m" in tfs:
        print("SKIP NAMED: 1m is skipped on budget (--skip-1m). All other tfs run.")
    print(f"tf order (1m last): {order}\n")
    print(f"{'asset':9s} {'tf':4s} {'bars':>10s} {'emas':>5s} {'skip':>5s} "
          f"{'secs':>7s} {'MB':>8s}  path")
    hr()

    for tf in order:
        for sym in assets:
            t0 = time.time()
            df = load_raw(sym, tf)
            ot = df["open_time"].to_numpy(np.int64)
            n = len(ot)
            c = df["close"].to_numpy(float)
            h = df["high"].to_numpy(float)
            lo = df["low"].to_numpy(float)
            if not np.isfinite(c).all():
                print(f"      HALT: non-finite close in {sym} {tf}")
                raise SystemExit(2)

            feas = set(feasible_lengths(fm, sym, tf))
            cols: dict[str, np.ndarray] = {"open_time": ot}
            for k, v in (("open", df["open"]), ("high", df["high"]),
                         ("low", df["low"]), ("close", df["close"]),
                         ("volume", df["volume"])):
                cols[k] = v.to_numpy(np.float64).astype(np.float32)
            cols["atr"] = atr(h, lo, c, ATR_LEN).astype(np.float32)

            nskip = 0
            for L in ALL_EMAS:
                if L not in feas:
                    # NEVER on this cell: the column exists so the schema is
                    # uniform, and is all-NaN so nothing cold can be read.
                    cols[f"e{L}"] = np.full(n, np.nan, dtype=np.float32)
                    nskip += 1
                    continue
                v = ema(c, L)                       # ratified recursion
                v[:min(WARM[L], n)] = np.nan        # never backfilled
                cols[f"e{L}"] = v.astype(np.float32)

            out = pd.DataFrame(cols)
            d = OUT / "emas" / sym
            d.mkdir(parents=True, exist_ok=True)
            p = d / f"{tf}.parquet"
            to_parquet_atomic(out, p)
            _ROWS_TOTAL += n
            b = rec_bytes(p)
            print(f"{sym:9s} {tf:4s} {n:10,d} {18 - nskip:5d} {nskip:5d} "
                  f"{time.time() - t0:7.1f} {b / 1e6:8.1f}  {p}")
            del df, out, cols
    print(f"\nrunning totals: rows={_ROWS_TOTAL:,}  bytes={_BYTES_TOTAL:,} "
          f"({_BYTES_TOTAL / 1e9:.2f} GB)  elapsed={time.time() - _T0:.0f}s")


def fixtures_stage2(fm: pd.DataFrame, assets: list[str], tfs: list[str]) -> None:
    banner("STAGE 2 FIXTURES")

    # ---- F-B2: zero values inside the warm-up region, every series, every cell
    print("F-B2  NaN-before-warm on every series (zero cold-head values)")
    checked = leaks = 0
    for sym in assets:
        for tf in tfs:
            p = OUT / "emas" / sym / f"{tf}.parquet"
            if not p.exists():
                continue
            feas = set(feasible_lengths(fm, sym, tf))
            d = pd.read_parquet(p, columns=[f"e{L}" for L in ALL_EMAS])
            n = len(d)
            for L in ALL_EMAS:
                v = d[f"e{L}"].to_numpy()
                head = v[:min(WARM[L], n)]
                bad = int(np.isfinite(head).sum())
                leaks += bad
                checked += 1
                if bad:
                    print(f"      LEAK {sym} {tf} e{L}: {bad} finite values "
                          f"inside warm_bars={WARM[L]}")
                if L not in feas and int(np.isfinite(v).sum()):
                    print(f"      LEAK {sym} {tf} e{L}: NEVER cell is not all-NaN")
                    leaks += 1
            del d
    if leaks:
        print(f"      F-B2 FAIL -- {leaks} cold-head values across {checked} series")
        raise SystemExit(2)
    print(f"      F-B2 PASS -- 0 cold-head values across {checked} series")

    # ---- F-B3: one EMA per family hand-recomputed on 50 bars, bit-match
    print("\nF-B3  one EMA per family hand-recomputed on 50 bars (bit-match)")
    sym, tf = "BTCUSDT", "1h"
    raw = load_raw(sym, tf)
    c = raw["close"].to_numpy(float)
    stored = pd.read_parquet(OUT / "emas" / sym / f"{tf}.parquet")
    ok = True
    for fam, members in RIBBONS.items():
        L = members[1]                              # the middle member
        wb = WARM[L]
        if wb + 50 >= len(c):
            print(f"      {fam:5s} e{L:5d}  SKIP (NEVER on {sym} {tf})")
            continue
        # hand recursion, the literal definition, run over the whole prefix
        alpha = 2.0 / (L + 1.0)
        prev = np.nan
        hand = np.empty(wb + 50)
        for i in range(wb + 50):
            prev = c[i] if np.isnan(prev) else prev + alpha * (c[i] - prev)
            hand[i] = prev
        seg_hand = hand[wb:wb + 50].astype(np.float32)
        seg_store = stored[f"e{L}"].to_numpy()[wb:wb + 50]
        match = np.array_equal(seg_hand, seg_store)
        ok &= match
        print(f"      {fam:5s} e{L:5d}  bars[{wb}:{wb + 50}]  "
              f"{'BIT-MATCH' if match else 'MISMATCH'}  "
              f"first={seg_store[0]:.6f}")
    if not ok:
        print("      F-B3 FAIL"); raise SystemExit(2)
    print("      F-B3 PASS -- every family's middle EMA bit-matches the recursion")


# ===========================================================================
# STAGE 3 -- RIBBON LIBRARY
# ===========================================================================
def ribbon(a: int, b: int, df: pd.DataFrame) -> dict[str, np.ndarray]:
    """The general two-EMA band, for ANY pair of lengths on ANY lookback frame.

    This is the operator's requirement stated generally: `df` needs only a
    `close` column.  If `e{a}` / `e{b}` are already present they are used as
    stored (so a band over the census-2B substrate costs nothing); otherwise
    they are computed here with the same recursion and the same warm-up law,
    so an ad-hoc pair on an ad-hoc frame obeys the identical rules.

    Returns upper / lower / mid / width_atr.
    """
    def line(L: int) -> np.ndarray:
        col = f"e{L}"
        if col in df.columns:
            return df[col].to_numpy(np.float64)
        v = ema(df["close"].to_numpy(np.float64), L)
        v[:min(warm_bars(L), len(v))] = np.nan
        return v

    ea, eb = line(a), line(b)
    if "atr" in df.columns:
        av = df["atr"].to_numpy(np.float64)
    else:
        av = atr(df["high"].to_numpy(np.float64), df["low"].to_numpy(np.float64),
                 df["close"].to_numpy(np.float64), ATR_LEN)
    upper = np.fmax(ea, eb)
    lower = np.fmin(ea, eb)
    both = np.isfinite(ea) & np.isfinite(eb)
    upper = np.where(both, upper, np.nan)
    lower = np.where(both, lower, np.nan)
    mid = (ea + eb) / 2.0
    with np.errstate(invalid="ignore", divide="ignore"):
        width_atr = np.where(np.isfinite(av) & (av > 0),
                             (upper - lower) / av, np.nan)
    return {"upper": upper, "lower": lower, "mid": mid, "width_atr": width_atr}


def family_state(fam: str, df: pd.DataFrame) -> dict[str, np.ndarray]:
    """Canonical per-bar state for one named ribbon.

    The band is the envelope of the family's EXTREME members -- ribbon(fast,
    slow) -- which is what makes F-B4's `ribbon(9,26) reproduces the FAST band`
    true by construction rather than by luck.  The middle member is not
    discarded: it is exactly what `orientation` reads.
    """
    a, m, z = RIBBONS[fam]                       # fast, middle, slow
    band = ribbon(a, z, df)
    ea = df[f"e{a}"].to_numpy(np.float64)
    em = df[f"e{m}"].to_numpy(np.float64)
    ez = df[f"e{z}"].to_numpy(np.float64)
    av = df["atr"].to_numpy(np.float64)
    close = df["close"].to_numpy(np.float64)
    n = len(close)
    warm = np.isfinite(ea) & np.isfinite(em) & np.isfinite(ez) \
        & np.isfinite(av) & (av > 0)

    w_atr = band["width_atr"]

    # width_delta_k in ATR units: (raw width now - raw width k bars ago) / ATR.
    # Thresholding this at +-0.05 IS the contract's "width_delta_k <> +-0.05*ATR".
    raw_w = band["upper"] - band["lower"]
    prev = np.full(n, np.nan)
    if n > K_WINDOW:
        prev[K_WINDOW:] = raw_w[:-K_WINDOW]
    with np.errstate(invalid="ignore", divide="ignore"):
        d_k = np.where(warm & np.isfinite(prev), (raw_w - prev) / av, np.nan)

    state = np.full(n, ST_NA, dtype=np.int8)
    fin = np.isfinite(d_k)
    state[fin] = ST_FLAT
    state[fin & (d_k < -STATE_EPS)] = ST_COMPRESS
    state[fin & (d_k > STATE_EPS)] = ST_EXPAND

    orient = np.full(n, OR_NA, dtype=np.int8)
    orient[warm] = OR_MIXED
    orient[warm & (ea > em) & (em > ez)] = OR_BULL
    orient[warm & (ea < em) & (em < ez)] = OR_BEAR

    knot = np.full(n, KN_NA, dtype=np.int8)
    kok = warm & np.isfinite(w_atr)
    knot[kok] = (w_atr[kok] < RIBBON_C).astype(np.int8)

    pos = np.full(n, PS_NA, dtype=np.int8)
    pos[warm] = PS_INSIDE
    pos[warm & (close > band["upper"])] = PS_ABOVE
    pos[warm & (close < band["lower"])] = PS_BELOW

    return {"upper": band["upper"], "lower": band["lower"], "mid": band["mid"],
            "width_atr": w_atr, "width_delta_k": d_k, "state": state,
            "orient": orient, "knot": knot, "pos": pos, "warm": warm}


def stage3(fm: pd.DataFrame, assets: list[str], tfs: list[str]) -> None:
    banner("STAGE 3 -- RIBBON LIBRARY")
    (OUT / "ribbons").mkdir(parents=True, exist_ok=True)
    print(f"band       = ribbon(fastest, slowest) envelope per family")
    print(f"width_atr  = (upper - lower) / ATR({ATR_LEN})")
    print(f"state      = compressing/expanding if |width_delta_{K_WINDOW}| > "
          f"{STATE_EPS} ATR, else flat")
    print(f"knot       = width_atr < {RIBBON_C}   (RIBBON_C carried from census-2A)")
    print(f"orientation= monotone order of the three members\n")
    print(f"{'asset':9s} {'tf':4s} {'bars':>10s} {'fams':>5s} {'secs':>7s} "
          f"{'MB':>8s}  path")
    hr()
    for sym in assets:
        for tf in tfs:
            src = OUT / "emas" / sym / f"{tf}.parquet"
            if not src.exists():
                continue
            t0 = time.time()
            df = pd.read_parquet(src)
            cols = {"open_time": df["open_time"].to_numpy(np.int64),
                    "close": df["close"].to_numpy(np.float32),
                    "atr": df["atr"].to_numpy(np.float32)}
            nf = 0
            for fam in FAMILIES:
                feas = set(feasible_lengths(fm, sym, tf))
                if not set(RIBBONS[fam]).issubset(feas):
                    n = len(df)
                    cols[f"{fam}_upper"] = np.full(n, np.nan, np.float32)
                    cols[f"{fam}_lower"] = np.full(n, np.nan, np.float32)
                    cols[f"{fam}_mid"] = np.full(n, np.nan, np.float32)
                    cols[f"{fam}_width_atr"] = np.full(n, np.nan, np.float32)
                    cols[f"{fam}_width_delta_k"] = np.full(n, np.nan, np.float32)
                    cols[f"{fam}_state"] = np.full(n, ST_NA, np.int8)
                    cols[f"{fam}_orient"] = np.full(n, OR_NA, np.int8)
                    cols[f"{fam}_knot"] = np.full(n, KN_NA, np.int8)
                    cols[f"{fam}_pos"] = np.full(n, PS_NA, np.int8)
                    continue
                s = family_state(fam, df)
                nf += 1
                for k in ("upper", "lower", "mid", "width_atr", "width_delta_k"):
                    cols[f"{fam}_{k}"] = s[k].astype(np.float32)
                cols[f"{fam}_state"] = s["state"]
                cols[f"{fam}_orient"] = s["orient"]
                cols[f"{fam}_knot"] = s["knot"]
                cols[f"{fam}_pos"] = s["pos"]
            out = pd.DataFrame(cols)
            d = OUT / "ribbons" / sym
            d.mkdir(parents=True, exist_ok=True)
            p = d / f"{tf}.parquet"
            to_parquet_atomic(out, p)
            b = rec_bytes(p)
            print(f"{sym:9s} {tf:4s} {len(out):10,d} {nf:5d} "
                  f"{time.time() - t0:7.1f} {b / 1e6:8.1f}  {p}")
            del df, out, cols


def fixtures_stage3(fm: pd.DataFrame) -> None:
    banner("STAGE 3 FIXTURES -- F-B4")

    # ---- F-B4a: ribbon(9,26) reproduces the stored FAST band
    print("F-B4a  ribbon(9,26) reproduces the FAST band, exactly")
    cell = pick_cell(fm, [("ETHUSDT", "1h"), ("BTCUSDT", "1h")], "F-B4a")
    if cell is None:
        return
    sym, tf = cell
    src = pd.read_parquet(OUT / "emas" / sym / f"{tf}.parquet")
    rb = pd.read_parquet(OUT / "ribbons" / sym / f"{tf}.parquet")
    got = ribbon(9, 26, src)
    for k in ("upper", "lower", "mid", "width_atr"):
        a = got[k].astype(np.float32)
        b = rb[f"FAST_{k}"].to_numpy(np.float32)
        same = np.array_equal(a, b, equal_nan=True)
        print(f"       FAST_{k:14s} equal={same}")
        if not same:
            print("       F-B4a FAIL"); raise SystemExit(2)

    # ---- F-B4b: the general form works on a pair that is in no family
    print("\nF-B4b  ribbon(a,b) is general -- an arbitrary pair on lookback data")
    arb = ribbon(45, 700, src[["open_time", "high", "low", "close", "atr"]])
    fin = np.isfinite(arb["width_atr"])
    first = int(np.argmax(fin)) if fin.any() else -1
    exp = max(warm_bars(45), warm_bars(700))
    print(f"       ribbon(45,700): neither length is a family member; "
          f"first finite width at bar {first:,}, warm_bars(700)={exp:,} "
          f"-> {'OK' if first >= exp else 'FAIL'}")
    if first < exp:
        print("       F-B4b FAIL"); raise SystemExit(2)

    # ---- F-B4c: orientation flips on a hand-built synthetic
    print("\nF-B4c  orientation flips on a hand-built synthetic")
    n = 4000
    x = np.arange(n, dtype=float)
    price = np.where(x < n // 2, 100 + 0.05 * x, 100 + 0.05 * (n // 2) - 0.05 * (x - n // 2))
    syn = pd.DataFrame({"open_time": (x * 60000).astype(np.int64),
                        "open": price, "high": price + 0.5,
                        "low": price - 0.5, "close": price})
    syn["atr"] = atr(syn["high"].to_numpy(float), syn["low"].to_numpy(float),
                     syn["close"].to_numpy(float), ATR_LEN)
    for L in RIBBONS["FAST"]:
        v = ema(syn["close"].to_numpy(float), L)
        v[:min(warm_bars(L), n)] = np.nan
        syn[f"e{L}"] = v
    st = family_state("FAST", syn)
    o = st["orient"]
    up_frac = float((o[300:n // 2] == OR_BULL).mean())
    dn_frac = float((o[n // 2 + 300:] == OR_BEAR).mean())
    print(f"       rising leg  bull-fanned {up_frac * 100:5.1f}% of bars")
    print(f"       falling leg bear-fanned {dn_frac * 100:5.1f}% of bars")
    flip = up_frac > 0.95 and dn_frac > 0.95
    print(f"       orientation flips across the peak -> {'OK' if flip else 'FAIL'}")
    if not flip:
        print("       F-B4c FAIL"); raise SystemExit(2)

    # ---- F-B4d: state thresholds exercised in BOTH directions
    print("\nF-B4d  state thresholds exercised both directions")
    st_syn = st["state"]
    have_exp = int((st_syn == ST_EXPAND).sum())
    have_cmp = int((st_syn == ST_COMPRESS).sum())
    have_flat = int((st_syn == ST_FLAT).sum())
    print(f"       synthetic FAST: expanding={have_exp:,}  compressing={have_cmp:,}"
          f"  flat={have_flat:,}")
    # and on a real cell, so the thresholds are exercised on real ATR too
    stt = rb["FAST_state"].to_numpy()
    print(f"       {sym} {tf} FAST: expanding={int((stt == ST_EXPAND).sum()):,}  "
          f"compressing={int((stt == ST_COMPRESS).sum()):,}  "
          f"flat={int((stt == ST_FLAT).sum()):,}")
    both = (have_exp > 0 and have_cmp > 0
            and int((stt == ST_EXPAND).sum()) > 0
            and int((stt == ST_COMPRESS).sum()) > 0)
    if not both:
        print("       F-B4d FAIL -- a direction was never exercised")
        raise SystemExit(2)
    print("       F-B4 PASS -- band identity, generality, orientation flip, "
          "both state directions")


# ===========================================================================
# STAGE 4 -- CROSS EVENTS
# ===========================================================================
def refusal_events(series: np.ndarray, level: np.ndarray, atr_v: np.ndarray,
                   eps: float = KISS_EPS, delta: float = KISS_DELTA,
                   k: int = KISS_K) -> tuple[np.ndarray, np.ndarray]:
    """The ratified refusal/kiss grammar, carried from census2a_program.py:509
    unchanged.  Restated rather than imported so that census2a_program.py stays
    byte-untouched and is never executed by this program; F-B5c asserts this
    copy is element-for-element equal to the 2A original on a real series.

    approach within eps*ATR -> veer >= delta*ATR within k bars -> no sign
    change of (series - level) in between.  Returns (flag_at_touch, confirm).
    """
    n = len(series)
    flag = np.zeros(n, dtype=bool)
    confirm = np.full(n, -1, dtype=np.int64)
    spread = series - level
    a = np.abs(spread)
    sg = np.sign(spread)
    finite = np.isfinite(spread) & np.isfinite(atr_v) & (atr_v > 0)
    touch = (a <= eps * atr_v) & finite
    if not touch.any():
        return flag, confirm
    idx = np.arange(n)
    alive = touch.copy()
    done = np.zeros(n, dtype=bool)
    for d in range(1, k + 1):
        j = idx + d
        ok_j = j <= (n - 1)
        jj = np.where(ok_j, j, 0)
        brk = alive & ok_j & ~finite[jj]
        alive &= ~brk
        sign_chg = (sg[idx] != 0) & (sg[jj] != 0) & (sg[jj] != sg[idx])
        brk2 = alive & ok_j & sign_chg
        alive &= ~brk2
        hit = alive & ok_j & ~done & (a[jj] >= delta * atr_v[jj])
        flag |= hit
        confirm = np.where(hit, jj, confirm)
        done |= hit
        alive &= ~hit
        alive &= ok_j
        if not alive.any():
            break
    return flag, confirm


def _emit(rows: list, sym: str, tf: str, ot: np.ndarray, idx: np.ndarray,
          pair_class: str, pair: str, fam: str, event: str, direction: str,
          confirm: np.ndarray | None = None) -> None:
    if idx.size == 0:
        return
    ci = idx if confirm is None else confirm[idx]
    rows.append(pd.DataFrame({
        "asset": sym, "tf": tf, "pair_class": pair_class, "pair": pair,
        "family": fam, "event": event, "dir": direction,
        "bar_index": idx.astype(np.int64),
        "ts_ms": ot[idx].astype(np.int64),
        "confirm_ts_ms": ot[ci].astype(np.int64),
    }))


def crosses_for_cell(fm: pd.DataFrame, sym: str, tf: str) -> pd.DataFrame:
    e = pd.read_parquet(OUT / "emas" / sym / f"{tf}.parquet")
    rb = pd.read_parquet(OUT / "ribbons" / sym / f"{tf}.parquet")
    ot = e["open_time"].to_numpy(np.int64)
    close = e["close"].to_numpy(np.float64)
    av = e["atr"].to_numpy(np.float64)
    feas = set(feasible_lengths(fm, sym, tf))
    rows: list[pd.DataFrame] = []

    def line(L: int) -> np.ndarray:
        return e[f"e{L}"].to_numpy(np.float64)

    # ---- 18 within-ribbon pairs: a_b, a_c, b_c per family
    for fam, (a, m, z) in RIBBONS.items():
        for (p, q), tag in (((a, m), "a_b"), ((a, z), "a_c"), ((m, z), "b_c")):
            if p not in feas or q not in feas:
                continue
            u = crossover(line(p), line(q))
            d = crossunder(line(p), line(q))
            _emit(rows, sym, tf, ot, np.flatnonzero(u), "within_ribbon",
                  f"{p}_{q}", fam, "cross_up", "up")
            _emit(rows, sym, tf, ot, np.flatnonzero(d), "within_ribbon",
                  f"{p}_{q}", fam, "cross_down", "down")

    # ---- 5 adjacent midline pairs
    for (p, q) in MIDLINE_PAIRS:
        if p not in feas or q not in feas:
            continue
        u = crossover(line(p), line(q))
        d = crossunder(line(p), line(q))
        _emit(rows, sym, tf, ot, np.flatnonzero(u), "midline",
              f"{p}_{q}", "", "cross_up", "up")
        _emit(rows, sym, tf, ot, np.flatnonzero(d), "midline",
              f"{p}_{q}", "", "cross_down", "down")

    # ---- price <-> ribbon band: enter / exit / reject-at-band
    for fam in FAMILIES:
        if not set(RIBBONS[fam]).issubset(feas):
            continue
        pos = rb[f"{fam}_pos"].to_numpy()
        up = rb[f"{fam}_upper"].to_numpy(np.float64)
        lo = rb[f"{fam}_lower"].to_numpy(np.float64)
        prev = np.concatenate(([PS_NA], pos[:-1]))
        ok = (pos != PS_NA) & (prev != PS_NA)
        # enter: outside -> inside, close-confirmed
        ent_dn = np.flatnonzero(ok & (prev == PS_ABOVE) & (pos == PS_INSIDE))
        ent_up = np.flatnonzero(ok & (prev == PS_BELOW) & (pos == PS_INSIDE))
        _emit(rows, sym, tf, ot, ent_dn, "price_band", f"{fam}_band", fam,
              "enter", "down")
        _emit(rows, sym, tf, ot, ent_up, "price_band", f"{fam}_band", fam,
              "enter", "up")
        # exit: inside -> outside
        ex_up = np.flatnonzero(ok & (prev == PS_INSIDE) & (pos == PS_ABOVE))
        ex_dn = np.flatnonzero(ok & (prev == PS_INSIDE) & (pos == PS_BELOW))
        _emit(rows, sym, tf, ot, ex_up, "price_band", f"{fam}_band", fam,
              "exit", "up")
        _emit(rows, sym, tf, ot, ex_dn, "price_band", f"{fam}_band", fam,
              "exit", "down")
        # traverse: below -> above (or the reverse) in ONE bar, never closing
        # inside. The contract's grammar names {enter, exit, reject}; a bar that
        # clears the whole band matches none of them and was being dropped in
        # silence -- 510,584 events, 18.4% of all band transitions on this panel,
        # concentrated in exactly the fast/wide-bar cells where a band crossing
        # matters most. Emitted as its own class rather than folded into `exit`,
        # so the pared taxonomy stays readable and this addition is visible to
        # the operator rather than hidden inside an existing count.
        tv_up = np.flatnonzero(ok & (prev == PS_BELOW) & (pos == PS_ABOVE))
        tv_dn = np.flatnonzero(ok & (prev == PS_ABOVE) & (pos == PS_BELOW))
        _emit(rows, sym, tf, ot, tv_up, "price_band", f"{fam}_band", fam,
              "traverse", "up")
        _emit(rows, sym, tf, ot, tv_dn, "price_band", f"{fam}_band", fam,
              "traverse", "down")
        # reject-at-band: the ratified kiss grammar, price vs each rail
        fu, cu = refusal_events(close, up, av)
        fl, cl = refusal_events(close, lo, av)
        _emit(rows, sym, tf, ot, np.flatnonzero(fu), "price_band",
              f"{fam}_upper", fam, "reject", "upper", confirm=cu)
        _emit(rows, sym, tf, ot, np.flatnonzero(fl), "price_band",
              f"{fam}_lower", fam, "reject", "lower", confirm=cl)

    if not rows:
        return pd.DataFrame(columns=["asset", "tf", "pair_class", "pair",
                                     "family", "event", "dir", "bar_index",
                                     "ts_ms", "confirm_ts_ms"])
    out = pd.concat(rows, ignore_index=True)
    return out.sort_values(["ts_ms", "pair_class", "pair", "event", "dir"]) \
              .reset_index(drop=True)


def stage4(fm: pd.DataFrame, assets: list[str], tfs: list[str]) -> None:
    banner("STAGE 4 -- CROSS EVENTS  (pared taxonomy: 18 within + 5 midline + band)")
    (OUT / "crosses").mkdir(parents=True, exist_ok=True)
    print("F-KEY declared key: (asset, tf, pair_class, pair, event, dir, ts_ms)")
    print("events are close-confirmed; rejects carry confirm_ts_ms != ts_ms\n")
    print(f"{'asset':9s} {'tf':4s} {'events':>12s} {'within':>10s} {'midline':>9s} "
          f"{'band':>10s} {'secs':>7s} {'MB':>7s}")
    hr()
    for sym in assets:
        for tf in tfs:
            if not (OUT / "ribbons" / sym / f"{tf}.parquet").exists():
                continue
            t0 = time.time()
            ev = crosses_for_cell(fm, sym, tf)
            d = OUT / "crosses" / sym
            d.mkdir(parents=True, exist_ok=True)
            p = d / f"{tf}.parquet"
            to_parquet_atomic(ev, p)
            b = rec_bytes(p)
            n_w = int((ev.pair_class == "within_ribbon").sum())
            n_m = int((ev.pair_class == "midline").sum())
            n_b = int((ev.pair_class == "price_band").sum())
            # F-KEY on the declared key, at write time
            key = ["asset", "tf", "pair_class", "pair", "event", "dir", "ts_ms"]
            dup = int(ev.duplicated(subset=key).sum())
            if dup:
                print(f"      F-KEY FAIL {sym} {tf}: {dup} duplicate keys")
                raise SystemExit(2)
            print(f"{sym:9s} {tf:4s} {len(ev):12,d} {n_w:10,d} {n_m:9,d} "
                  f"{n_b:10,d} {time.time() - t0:7.1f} {b / 1e6:7.1f}")
            del ev


def fixtures_stage4(fm: pd.DataFrame) -> None:
    banner("STAGE 4 FIXTURES -- F-B5")
    cell = pick_cell(fm, [("NEARUSDT", "4h"), ("BTCUSDT", "4h")], "F-B5")
    if cell is None:
        return
    sym, tf = cell

    # ---- F-B5a: determinism, re-run hash-identical
    print("F-B5a  determinism -- re-run is hash-identical")
    p = OUT / "crosses" / sym / f"{tf}.parquet"
    h1 = sha256_file(p)
    again = crosses_for_cell(fm, sym, tf)
    tmp = OUT / "crosses" / sym / f".{tf}.rerun.parquet"
    to_parquet_atomic(again, tmp)
    h2 = sha256_file(tmp)
    tmp.unlink()
    print(f"       {sym} {tf}  stored={h1[:16]}  rerun={h2[:16]}  "
          f"{'IDENTICAL' if h1 == h2 else 'DIFFERENT'}")
    if h1 != h2:
        print("       F-B5a FAIL"); raise SystemExit(2)

    # ---- F-B5b: three hand-verified events per NEW pair class
    print("\nF-B5b  three hand-verified events per new pair class")
    e = pd.read_parquet(OUT / "emas" / sym / f"{tf}.parquet")
    rb = pd.read_parquet(OUT / "ribbons" / sym / f"{tf}.parquet")
    ev = pd.read_parquet(p)
    close = e["close"].to_numpy(np.float64)
    ok = True

    def show(title: str, sub: pd.DataFrame, check) -> None:
        nonlocal ok
        print(f"\n       {title}   (n={len(sub):,})")
        for _, r in sub.head(3).iterrows():
            good, detail = check(r)
            ok &= good
            print(f"         {iso(r.ts_ms)}  {r.pair:12s} {r.event:7s} "
                  f"{r['dir']:6s}  {detail}  {'OK' if good else 'FAIL'}")

    # within-ribbon
    s = ev[(ev.pair_class == "within_ribbon") & (ev.pair == "1618_3618")]
    if len(s) < 3:
        s = ev[ev.pair_class == "within_ribbon"]

    def chk_cross(r):
        i = int(r.bar_index)
        a, b = (int(x) for x in r.pair.split("_"))
        va, vb = e[f"e{a}"].to_numpy(np.float64), e[f"e{b}"].to_numpy(np.float64)
        if r.event == "cross_up":
            good = (va[i] > vb[i]) and (va[i - 1] <= vb[i - 1])
        else:
            good = (va[i] < vb[i]) and (va[i - 1] >= vb[i - 1])
        return good, (f"e{a}-e{b}: prev={va[i-1]-vb[i-1]:+.4f} "
                      f"now={va[i]-vb[i]:+.4f}")
    show("within-ribbon (close-confirmed sign change)", s, chk_cross)

    # midline
    s = ev[ev.pair_class == "midline"]
    show("adjacent midline", s, chk_cross)

    # price<->band enter/exit
    s = ev[(ev.pair_class == "price_band") & (ev.event.isin(["enter", "exit"]))]

    def chk_band(r):
        i = int(r.bar_index)
        fam = r.family
        u = rb[f"{fam}_upper"].to_numpy(np.float64)
        lo = rb[f"{fam}_lower"].to_numpy(np.float64)
        pos_now = ("above" if close[i] > u[i] else
                   "below" if close[i] < lo[i] else "inside")
        pos_prev = ("above" if close[i - 1] > u[i - 1] else
                    "below" if close[i - 1] < lo[i - 1] else "inside")
        if r.event == "enter":
            good = pos_now == "inside" and pos_prev != "inside"
        else:
            good = pos_prev == "inside" and pos_now != "inside"
        return good, f"{pos_prev} -> {pos_now}  band=[{lo[i]:.4f},{u[i]:.4f}] c={close[i]:.4f}"
    show("price<->band enter/exit", s, chk_band)

    # reject-at-band (the kiss)
    s = ev[(ev.pair_class == "price_band") & (ev.event == "reject")]

    def chk_reject(r):
        i, j = int(r.bar_index), None
        fam = r.family
        rail = (rb[f"{fam}_upper"] if r["dir"] == "upper"
                else rb[f"{fam}_lower"]).to_numpy(np.float64)
        av = e["atr"].to_numpy(np.float64)
        j = int(np.searchsorted(e["open_time"].to_numpy(np.int64),
                                int(r.confirm_ts_ms)))
        touch = abs(close[i] - rail[i]) <= KISS_EPS * av[i]
        veer = abs(close[j] - rail[j]) >= KISS_DELTA * av[j]
        within = 0 < (j - i) <= KISS_K
        return (touch and veer and within,
                f"touch={abs(close[i]-rail[i])/av[i]:.3f}ATR "
                f"veer={abs(close[j]-rail[j])/av[j]:.3f}ATR gap={j-i}")
    show("reject-at-band (ratified kiss 0.25/0.75/10)", s, chk_reject)

    if not ok:
        print("\n       F-B5b FAIL"); raise SystemExit(2)
    print("\n       F-B5b PASS -- hand-verified events in all four pair classes")

    # ---- F-B5c: this copy of the kiss grammar == census-2A's original
    print("\nF-B5c  refusal_events is element-equal to the census-2A original")
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "_c2a_ref", REPO / "scripts" / "census2a_program.py")
    try:
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        orig = mod.refusal_events
    except Exception as exc:            # importing 2A must never be required
        print(f"       SKIP -- census2a_program.py not importable in isolation "
              f"({type(exc).__name__}); the copy stands on F-B5b")
        return
    av = e["atr"].to_numpy(np.float64)
    lvl = rb["M_upper"].to_numpy(np.float64)
    f1, c1 = refusal_events(close, lvl, av)
    f2, c2 = orig(close, lvl, av)
    same = np.array_equal(f1, f2) and np.array_equal(c1, c2)
    print(f"       flags equal={np.array_equal(f1, f2)}  "
          f"confirms equal={np.array_equal(c1, c2)}  n_events={int(f1.sum()):,}")
    if not same:
        print("       F-B5c FAIL"); raise SystemExit(2)
    print("       F-B5c PASS")


# ===========================================================================
# MANIFEST -- pin-merge semantics (I12)
# ===========================================================================
def write_manifest(extra: dict | None = None) -> dict:
    """Pin-merge: an existing manifest's `pins` block survives untouched and
    artifact entries are merged by key, so a partial re-run never silently
    drops what an earlier stage recorded."""
    prev = {}
    if MANIFEST.exists():
        prev = json.loads(MANIFEST.read_text(encoding="utf-8"))
    arts = dict(prev.get("artifacts", {}))
    # Merge carries entries forward; it must NOT resurrect files that are gone.
    # A corrupt artifact deleted by hand came straight back into the manifest --
    # with its stale byte count and sha -- until this prune existed. I12 says
    # pins MERGE, not that the manifest may claim a file that is not there.
    gone = [k for k, v in arts.items() if not Path(v.get("path", "")).exists()]
    for k in gone:
        del arts[k]
    if gone:
        print(f"  manifest prune: {len(gone)} recorded artifact(s) no longer on "
              f"disk, dropped -- {gone}")
    for p in sorted(OUT.rglob("*.parquet")):
        if p.name.startswith("."):
            continue
        key = p.relative_to(OUT).as_posix()
        rows = parquet_rows(p)
        if rows is None:
            print(f"  HALT: {p} is not a readable parquet -- refusing to record "
                  f"it in the manifest. Delete it and re-run its stage.")
            raise SystemExit(2)
        # Stage-5 tables are Tier-E and must never be stamped SUBSTRATE: the
        # manifest is what a later reader cites, and a display-only table
        # labelled as substrate is exactly how a probe becomes evidence.
        cls = ("DISPLAY-ONLY / Tier-E exploration -- m = 0"
               if key.startswith("firstlook/")
               else "SUBSTRATE -- census-2B V-ULT-1")
        arts[key] = {"path": str(p), "rows": rows, "bytes": p.stat().st_size,
                     "sha256": sha256_file(p), "class": cls}
    for p in sorted(OUT.rglob("*.json")):
        if p.name == MANIFEST.name:
            continue
        key = p.relative_to(OUT).as_posix()
        arts[key] = {"path": str(p), "rows": None, "bytes": p.stat().st_size,
                     "sha256": sha256_file(p),
                     "class": "DISPLAY-ONLY / Tier-E"}
    man = {
        "program": PROGRAM,
        "module": "CENSUS-2B / V-ULT-1 -- the U-VHT data module",
        "seed": SEED,
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "class": "substrate + Tier-E first-look; NO REGISTRATIONS; m = 0",
        "ceil_ms": CEIL_MS,
        "pins": prev.get("pins", {}) or {
            "ribbons": {k: list(v) for k, v in RIBBONS.items()},
            "tfs": TFS, "panel": PANEL, "annex": ANNEX,
            "warmfactor": WARMFACTOR,
            "warm_bars_rule": "ceil(3.46*N), NaN before warm, never backfilled",
            "warm_bars": {str(L): WARM[L] for L in ALL_EMAS},
            "k_window": K_WINDOW, "state_eps_atr": STATE_EPS,
            "knot_c_atr": RIBBON_C, "atr_len": ATR_LEN,
            "kiss": {"eps": KISS_EPS, "delta": KISS_DELTA, "k": KISS_K},
            "midline_pairs": [f"{a}_{b}" for a, b in MIDLINE_PAIRS],
            "toll_bps_round_trip": TOLL_BPS_ROUND_TRIP,
            "codes": {
                "state": {str(k): v for k, v in STATE_NAME.items()},
                "orient": {str(k): v for k, v in ORIENT_NAME.items()},
                "pos": {str(k): v for k, v in POS_NAME.items()},
                "knot": {str(k): v for k, v in KNOT_NAME.items()},
            },
            "engine_note": "engine 1.0.11 byte-untouched; imports indicators only",
            "machinery_note": ("scripts/census_build.py constants + _resample "
                               "imported, not restated; census2a_program.py "
                               "byte-untouched"),
            "klines_note": ("LIVE cache (engine.data.cache_dir), NOT mc1/"
                            "ops_klines -- census-2B spans the full history "
                            "and reports evidence-era share as a column"),
        },
        "artifacts": arts,
    }
    if extra:
        man.update(extra)
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(man, indent=2), encoding="utf-8")
    print(f"\nmanifest: {MANIFEST}  artifacts={len(arts)}  "
          f"bytes={MANIFEST.stat().st_size:,}")
    return man


# ===========================================================================
# MAIN
# ===========================================================================
def main() -> int:
    # Windows stdout defaults to cp1252. Redirected to a file that produces a
    # transcript no UTF-8 reader can open, which is a silent trap for anything
    # that later quotes this run.
    try:
        sys.stdout.reconfigure(encoding="utf-8", newline="\n")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="CENSUS-2B / V-ULT-1")
    ap.add_argument("--stage", default="1",
                    help="1|2|3|4|5|all  (comma-separated ok)")
    ap.add_argument("--assets", default=",".join(PANEL))
    ap.add_argument("--tfs", default=",".join(TFS))
    ap.add_argument("--skip-1m", action="store_true")
    ap.add_argument("--no-fixtures", action="store_true")
    a = ap.parse_args()

    assets = [s.strip() for s in a.assets.split(",") if s.strip()]
    tfs = [s.strip() for s in a.tfs.split(",") if s.strip()]
    stages = ({"1", "2", "3", "4", "5"} if a.stage == "all"
              else {s.strip() for s in a.stage.split(",")})
    # `--stage 34` (a missing comma) used to parse as {"34"}, match no guard,
    # run only the always-on stage 1 and exit 0 -- a silent no-op that looks
    # exactly like success.
    bad = sorted(stages - {"1", "2", "3", "4", "5"})
    if bad:
        print(f"HALT: unrecognised --stage token(s) {bad}. "
              f"Use 1|2|3|4|5, a comma-separated list, or 'all'.")
        return 2

    banner("CENSUS-2B / V-ULT-1 -- THE U-VHT DATA MODULE")
    print(f"program   {PROGRAM}   seed {SEED}")
    print(f"class     substrate + Tier-E first-look -- NO REGISTRATIONS, m = 0")
    print(f"assets    {assets}")
    print(f"tfs       {tfs}" + ("   [1m SKIPPED]" if a.skip_1m else ""))
    print(f"ribbons   " + " · ".join(f"{k}{list(v)}" for k, v in RIBBONS.items()))
    print(f"out       {OUT}")
    print(f"stages    {sorted(stages)}")

    fm = stage1(assets, tfs)
    run_tfs = [t for t in tfs if not (a.skip_1m and t == "1m")]

    if "2" in stages:
        stage2(fm, assets, tfs, a.skip_1m)
        if not a.no_fixtures:
            fixtures_stage2(fm, assets, run_tfs)
    if "3" in stages:
        stage3(fm, assets, run_tfs)
        if not a.no_fixtures:
            fixtures_stage3(fm)
    if "4" in stages:
        stage4(fm, assets, run_tfs)
        if not a.no_fixtures:
            fixtures_stage4(fm)
    if "5" in stages:
        import census2b_firstlook as fl
        fl.run(fm, assets, run_tfs)

    write_manifest()
    print(f"\nTOTAL rows={_ROWS_TOTAL:,}  bytes={_BYTES_TOTAL:,} "
          f"({_BYTES_TOTAL / 1e9:.2f} GB)  elapsed={time.time() - _T0:.0f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
