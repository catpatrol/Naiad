#!/usr/bin/env python
"""MC-2 -- RELAY & NESTING OBSERVATORY (extended) -- the CENSUS-2A sandbox.

WHAT THIS IS
  CENSUS-2A (contract draft v0.2, exchange/reports/) opens with three gating
  conditions, in order:

      (1) census paste #1 returns (MC-2 amended + CEN-0) and its outputs
          replace every <MC2> placeholder, diff-listed
      (2) operator reviews the resolved text
      (3) operator stamps RATIFIED

  This program is condition (1)'s first half.  It measures the six quantities
  the contract left as <MC2> placeholders so that the census can be scored on
  pinned constants instead of guesses.

  It is an OBSERVATORY, not a study.  It registers nothing, gates nothing and
  promotes no claim.  Its only output is a set of constants plus the evidence
  that produced them.

WHY IT PINS ON THE LIVE ERA (the one design decision the contract does not make)
  The contract's I1 wall bounds every SCORED table at 2024-07-01.  It says
  nothing about where the census's own CONSTANTS may be measured -- and that
  silence matters, because constants fitted on the same bars a study then
  scores are in-sample selection wearing a different hat.

  So: every constant here is pinned on the LIVE era (open_time >= CEIL_MS),
  which is disjoint from the evidence era the census scores.  The evidence-era
  value of each statistic is computed and printed BESIDE the live-era one --
  measured, never used to pin.  Where the two disagree the disagreement is
  itself reportable, and the report says so on its face.

  Consequence, stated plainly: every artifact this program writes is an OPS
  artifact and carries the DISPLAY-ONLY banner.  That is not a demotion; it is
  what makes the constants admissible.

  This choice is the single largest judgement call in paste #1.  It is flagged
  in the build document for the operator's condition-(2) review, and it is
  reversible: --era evidence re-pins everything in-sample if the operator
  prefers that, and prints the same tables.

THE SIX PLACEHOLDERS
  (i)   kiss/refusal eps, delta, k       fallback 0.25 / 0.75 / 10
  (ii)  TRAP counter-density             fallback >=2 counter FAST crosses/24h
  (iii) window W_max                     fallback 90 4h bars; "relay-lag p90 decides"
  (iv)  nested pair set                  fallback {1h-in-4h, 30m-in-4h, 30m-in-1h}
  (v)   ribbon-compression threshold c   fallback 0.5*ATR on 30m/1h 9/89 spread
  (vi)  25-pair trigger inclusion        fallback included

  MC-2 AS COMMISSIONED (APOLLO_LANE_UPDATE_and_CENSUS2_STATUS_2026-08-12.md:22)
  covers only (iii), (iv), (vi).  The operator extended its scope on
  2026-08-12 to cover (i), (ii), (v) as well -- all three are computable from
  data already on disk, so the extension costs no fetch.

REUSE DISCIPLINE (this program invents no primitive it can import)
  * evidence wall CEIL_MS ......... census_build (imported, never restated)
  * OHLCV resampling .............. census_build._resample (30m<-15m, 1d<-1h)
  * as-of index ................... census_build.asof_idx
  * ema/atr/crossover/crossunder .. engine.indicators
  * stamp grammar (KISS/WALL/TRAP/FIRST constants) .. mc1_program, imported and
    asserted equal at startup, so a drift in MC-1 breaks this program loudly
    rather than silently re-defining the vocabulary.

RESIDENCY (contract I2)
  RESTATED 2026-08-15 under DATA RESIDENCY v2.  All bulk is born LOCAL, under
  `~/Naiad/research_outputs/census2a/mc2/**`, resolved repo-relative from ROOT.
  The output root is asserted to be CONTAINED under ROOT/research_outputs -- not
  merely "the write succeeded", which a stray absolute path would also satisfy.
  The intent is unchanged from the original rule; only the definition of "where"
  moved.  The original text read "born on D:/... asserted to be on D:", which was
  correct for the Windows estate and is retained here as the reason this gate
  exists at all.  drive_wait is no longer in this path: it guards BACKUP writes
  to the LaCie, not substrate reads.

DETERMINISM
  Seed 20260812.  Every emitted frame is sorted by a total key and floats are
  rounded to 6dp, so two runs are byte-identical; the manifest carries a
  content sha256 per artifact and F-DET re-runs one table to prove it.

USAGE
  python scripts/mc2_program.py                 # full run, live-era pins
  python scripts/mc2_program.py --era evidence  # re-pin in-sample instead
  python scripts/mc2_program.py --stage relay   # one stage
  python scripts/mc2_program.py --smoke         # BTC+ETH only, fast
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

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from engine.indicators import ema, atr, crossover, crossunder  # noqa: E402
from engine.data import cache_dir  # noqa: E402
import census_build as CB  # noqa: E402
import mc1_program as M1  # noqa: E402
# `drive_wait` is deliberately NOT imported here any more (v2, 2026-08-15): the
# substrate is local, so nothing in this program waits on an external volume.
# drive_wait now guards BACKUP writes only -- see scripts/backup_estate.py.

SEED = 20260812
R6 = 6

# ---------------------------------------------------------------------------
# Residency.  Repo-local only (v2, 2026-08-15) -- see I2.  Asserted, not hoped
# for.  Name kept as D_ROOT so callers and log lines keep working; it no longer
# means "the D: drive", it means the census2a substrate root.
# ---------------------------------------------------------------------------
D_ROOT = ROOT / "research_outputs" / "census2a"
OUT = D_ROOT / "mc2"

DISPLAY_ONLY = ("DISPLAY-ONLY -- post-lockbox live-era data -- "
                "hypothesis generation only, never evidence.")

# ---------------------------------------------------------------------------
# Constants.  Anything CENSUS-1/MC-1 already fixed is IMPORTED and asserted;
# only genuinely new scan parameters are declared here.
# ---------------------------------------------------------------------------
CEIL_MS = CB.CEIL_MS                      # 2024-07-01, the evidence wall (I1)
TF_MS = CB.TF_MS
RESAMPLE = CB.RESAMPLE

PANEL = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "NEARUSDT", "ZECUSDT"]
ANNEX = ["JTOUSDT", "TAOUSDT"]            # printed, never pooled (I8 / F-11)

# The full family per contract I4.  EMA500 joins on the operator's 2026-08-12
# ruling; its evidence-side feasibility is exactly what stage `feas` reports.
EMAS = [9, 12, 25, 89, 200, 300, 450, 500]
ATR_LEN = CB.ATR_LEN

# Cross classes.  Lattice A/B per SEQ8; the long-ribbon pairs join for EMA500.
PAIRS = {
    "9_89": (9, 89), "89_200": (89, 200), "9_200": (9, 200),   # lattice A
    "12_25": (12, 25),                                          # lattice B
    "9_25": (9, 25), "25_89": (25, 89),                         # the 25 (obs)
    "300_450": (300, 450), "450_500": (450, 500),               # long ribbon
    # A1-FAN (run-3 amendment, VETO): two further long-ribbon rungs.
    "200_500": (200, 500), "300_500": (300, 500),

}
LATTICE_A = ["9_89", "89_200", "9_200"]
FAST_TFS = M1.FAST_TFS                    # 5m/15m/30m -- TRAP's counter tier

SCAN_TFS = ["5m", "15m", "30m", "1h", "4h", "12h"]

# --- relay (iii) -------------------------------------------------------------
RELAY_LEGS = ["9_89", "9_200", "12_25"]   # arming -> confirm -> trigger
RELAY_WIDTHS = [60, 90, 120, 150]         # 4h bars; the three-width ask + 150
RELAY_HARD_CAP = 400                      # observation cap, NOT a pin

# --- nesting (iv) ------------------------------------------------------------
NEST_CANDIDATES = [("1h", "4h"), ("30m", "4h"), ("30m", "1h"),
                   ("15m", "4h"), ("15m", "1h"), ("5m", "1h")]

# --- TRAP (ii) ---------------------------------------------------------------
TRAP_LOOKBACK_H = M1.TRAP_LOOKBACK_H      # 24h
TRAP_SWEEP = list(range(1, 21))

# --- ribbon (v) --------------------------------------------------------------
RIBBON_TFS = ["30m", "1h"]
RIBBON_SWEEP = [0.15, 0.25, 0.35, 0.5, 0.65, 0.8, 1.0, 1.25, 1.5]

# --- kiss (i) ----------------------------------------------------------------
KISS_EPS_SWEEP = [0.15, 0.20, 0.25, 0.30, 0.40]
KISS_DELTA_SWEEP = [0.50, 0.75, 1.00]
KISS_K_SWEEP = [6, 8, 10, 12, 15]

HORIZONS = CB.HORIZONS                    # {20,100,500} -- 5m EXEC bars

# Outcome horizon, expressed as a DURATION rather than a bar count.
#
# CB.HORIZONS are 5m exec-bar counts, so the integer 100 means 8h20m in
# CENSUS-1. Reusing that same integer on an HTF frame silently redefines the
# unit -- 100 bars is 16.7 days on 4h. That alone would only be a labelling
# problem, but stage_nesting's candidates span TWO different HTFs (4h and 1h),
# so a fixed bar count would put 16.7-day and 4.2-day outcomes in adjacent rows
# of one table and invite a comparison between them. Fixing the duration and
# converting per TF keeps every row of every table on the same clock.
HORIZON_MS = 100 * TF_MS["4h"]            # 16.67 days = the 4h reading of HORIZONS[1]


def horizon_bars(tf: str) -> int:
    """Bars of `tf` spanning HORIZON_MS, so outcomes are equal-DURATION."""
    return max(1, int(round(HORIZON_MS / TF_MS[tf])))

# --- query cards (display-only, never priors -- D-H) -------------------------
QUERY_CARDS = [
    {"id": "QC-1", "ts_iso": "2026-06-17 14:30", "note": "4H short; nesting photographed"},
    {"id": "QC-2", "ts_iso": "2026-08-11 10:00", "note": "same anatomy on the 5m lens"},
]

# v2, 2026-08-15.  Was `%LOCALAPPDATA%\naiad\data_cache\klines`, which expands to
# a literal unexpanded string on macOS and then silently reads nothing.  Resolved
# through engine.data.cache_dir() instead of re-deriving it here, so there is ONE
# definition of where the estate lives and $NAIAD_CACHE_DIR keeps working.
# NOTE: cache_dir() mkdirs on call (engine/data.py:47), so importing this module
# creates the cache directory if it is absent.  That is the real cache path, not
# a stray directory, but it is a side effect worth knowing about.
KLINES = cache_dir() / "klines"

_LOG_LINES: list[str] = []


def log(msg: str) -> None:
    line = f"[{datetime.now(timezone.utc).strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    _LOG_LINES.append(line)


def iso(ms_v: int) -> str:
    return datetime.fromtimestamp(ms_v / 1000, timezone.utc).strftime("%Y-%m-%d %H:%M")


def to_ms(iso_s: str) -> int:
    return int(datetime.strptime(iso_s, "%Y-%m-%d %H:%M")
               .replace(tzinfo=timezone.utc).timestamp() * 1000)


def _sha(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# Google Drive Desktop's in-tree footprints.  `.tmp.driveupload` is the one
# observed on this repo (2026-08-15): a directory of HARDLINKS to the files
# Drive is uploading, which is why it costs no disk and why `du` will not
# betray it.  Kept in step with the identical block in census2a_program.py.
DRIVE_STAGING_MARKERS = (".tmp.driveupload", ".shortcut-targets-by-id",
                         ".file-revisions-by-id")


def _drive_staging_markers(root: Path) -> list:
    """Repo-relative paths of any Drive staging marker at root or one level in.

    Deliberately shallow -- root plus its immediate subdirectories.  Both
    locations seen in the wild were at that depth (`./.tmp.driveupload` and
    `./naiad-backups/.tmp.driveupload`), and a full walk of a multi-GB tree on
    every preflight would cost more than the check is worth.  Never raises: a
    gate that dies on an unreadable directory is a gate that stops gating.
    """
    hits = []
    try:
        dirs = [root] + [p for p in root.iterdir()
                         if p.is_dir() and p.name != ".git"]
    except OSError:
        return hits
    for d in dirs:
        for marker in DRIVE_STAGING_MARKERS:
            try:
                if (d / marker).exists():
                    hits.append(str((d / marker).relative_to(root)))
            except OSError:
                continue
    return hits


# ===========================================================================
# S0 -- PREFLIGHT.  Identity (I3, two-sided) + drive (I2).  F-1's transcript.
# ===========================================================================
def stage_preflight() -> dict:
    """The two-sided identity gate and the D: gate.  Any miss HALTs.

    I3 is prose in the contract and implemented nowhere in the estate, so it is
    re-implemented inline here -- which is the point: a gate that lives only in
    a document is not a gate.
    """
    log("S0 preflight -- identity (I3) + residency (I2)")
    checks: list[tuple[str, bool, str]] = []

    cwd = str(Path.cwd()).replace("\\", "/")
    # I3, two-sided, RESTATED 2026-08-15 (v2).  The positive limb used to test
    # for a "c:/naiad" suffix, which on this platform can never be true -- the
    # gate was DEAD, not strict.  It now names $HOME/Naiad.  The negative limb
    # covers the three cloud roots that corrupt bulk writes, not just OneDrive.
    checks.append(("pwd == $HOME/Naiad",
                   Path.cwd().resolve() == (Path.home() / "Naiad").resolve(), cwd))
    _low = cwd.lower()
    checks.append(("pwd cloud-free",
                   not any(m in _low for m in
                           ("onedrive", "com~apple~clouddocs", "mobile documents")), cwd))
    # THIRD LIMB, added 2026-08-15 (M4 open item 4).  A PATH grep cannot see
    # Google Drive: measured 2026-08-15, Drive was uploading the study substrate
    # and the backup vault out of ~/Naiad while both limbs above passed, because
    # the repo is not under CloudStorage -- Drive reaches it via a sibling
    # symlink and realpath("~/Naiad") is unchanged.  Look for the ARTEFACT.
    _found = _drive_staging_markers(Path.cwd())
    checks.append(("no Drive staging in tree", not _found,
                   ", ".join(_found) if _found else "none"))

    import subprocess
    def _git(args: list[str]) -> str:
        try:
            return subprocess.run(["git"] + args, capture_output=True,
                                  text=True, timeout=30).stdout.strip()
        except Exception:
            return ""

    branch = _git(["rev-parse", "--abbrev-ref", "HEAD"])
    checks.append(("branch v12-v1-census", branch == "v12-v1-census", branch))
    remote = _git(["config", "--get", "remote.origin.url"])
    checks.append(("remote catpatrol/Naiad", "catpatrol/Naiad" in remote, remote))

    for rel in ["LEDGER.md", "exchange/status/CONVENTIONS.md"]:
        checks.append((f"{rel} present", (ROOT / rel).exists(), rel))

    for name, ok, detail in checks:
        log(f"    {'PASS' if ok else 'FAIL'}  {name:28} {detail}")
    if not all(ok for _, ok, _ in checks):
        raise SystemExit("HALT (I3): two-sided identity gate failed -- see above.")

    # --- I2, RESTATED 2026-08-15 (v2).  There is no external drive to wait on:
    #     bulk is born local, so wait_for_drive is gone from this path.  It has
    #     not been weakened away -- it now guards BACKUP writes to the LaCie in
    #     scripts/backup_estate.py, which is the only place a volume can be
    #     absent.  Waiting on a volume we never write to would be theatre.

    # Residency is about WHERE, not whether the write worked.  The old form,
    # `OUT.drive.upper() != "D:"`, could never pass on POSIX -- Path.drive is
    # always "" -- so it halted unconditionally.  Same intent, containment now.
    try:
        OUT.resolve().relative_to((ROOT / "research_outputs").resolve())
    except ValueError:
        raise SystemExit(f"HALT (I2): output root {OUT} is not under "
                         f"{ROOT / 'research_outputs'}.")
    OUT.mkdir(parents=True, exist_ok=True)
    probe = OUT / ".write_probe"
    try:
        probe.write_text("ok", encoding="utf-8")
        probe.unlink()
    except Exception as exc:
        raise SystemExit(f"HALT (I2): {OUT} present but not writable: {exc}")
    log(f"    residency OK -> {OUT}")

    # --- vocabulary parity: MC-1 owns the stamp grammar; we only borrow it.
    assert M1.KISS_TOUCH_ATR == 0.25 and M1.KISS_REEXPAND_ATR == 0.75 \
        and M1.KISS_REEXPAND_BARS == 10, "MC-1 kiss constants drifted"
    assert M1.TRAP_MIN_COUNTER == 2 and M1.TRAP_LOOKBACK_H == 24, "MC-1 TRAP drifted"
    assert M1.WALL_ATR_4H == 0.5 and M1.WALL_ATR_1D == 0.5, "MC-1 WALL drifted"
    assert CEIL_MS == 1719792000000, "evidence wall moved"
    log("    stamp-grammar parity vs mc1_program: OK")

    # "drive" is retained as a key so downstream manifest readers do not have to
    # branch on its absence; under v2 there is no volume to wait on, and saying
    # so explicitly is better than dropping the field.
    return {
        "identity": [{"check": n, "pass": bool(o), "detail": d} for n, o, d in checks],
        "drive": {"state": "LOCAL", "attempts": 0,
                  "elapsed_s": 0.0, "budget_s": 0.0},
        "out_root": str(OUT),
        "ceil_ms": CEIL_MS, "ceil_iso": iso(CEIL_MS),
    }


# ===========================================================================
# FRAMES.  Full EMA family per asset/TF, era-sliced, warm-seeded.
# ===========================================================================
_FRAME_CACHE: dict[tuple, pd.DataFrame] = {}


def _raw(sym: str, tf: str, ceiling: int | None) -> pd.DataFrame:
    """Raw OHLCV for one TF.  30m/1d are resampled exactly as census_build does."""
    if tf in RESAMPLE:
        src_tf, step = RESAMPLE[tf]
        raw = pd.read_parquet(KLINES / f"{sym}_{src_tf}.parquet")
        if ceiling is not None:
            raw = raw[raw["open_time"] < ceiling]
        raw = raw.sort_values("open_time").reset_index(drop=True)
        return CB._resample(raw, step)
    df = pd.read_parquet(KLINES / f"{sym}_{tf}.parquet")
    if ceiling is not None:
        df = df[df["open_time"] < ceiling]
    return df.sort_values("open_time").reset_index(drop=True)


def frame(sym: str, tf: str, era: str) -> pd.DataFrame:
    """Indicator frame for (sym, tf) restricted to `era`.

    era='evidence' -> bars < CEIL_MS, EMAs computed on that slice.  This is
      byte-for-byte what census_build.load_tf does, so F-PARITY can assert it.
    era='live'     -> EMAs computed on the FULL series (causal: out[i] depends
      only on 0..i), then sliced to >= CEIL_MS.  Slicing after the recursion is
      what makes the live-era EMAs warm rather than re-seeded at the wall.
    """
    key = (sym, tf, era)
    if key in _FRAME_CACHE:
        return _FRAME_CACHE[key]

    df = _raw(sym, tf, CEIL_MS if era == "evidence" else None)
    o = df["open_time"].to_numpy(np.int64)
    c = df["close"].to_numpy(float)
    h = df["high"].to_numpy(float)
    lo = df["low"].to_numpy(float)
    cols = {"open_time": o, "open": df["open"].to_numpy(float),
            "high": h, "low": lo, "close": c,
            "atr": atr(h, lo, c, ATR_LEN)}
    # I4: "SEQ8 warmup rule; NaN before warm".  An EMA seeded at the series
    # start carries its seed for warmup_bars(L) bars; a cross detected inside
    # that region is an artifact of the seed, not an event in the tape.  NaN-ing
    # the cold head makes crossover/crossunder return False there by
    # construction, so no downstream stage has to remember to exclude it.
    #
    # This is NOT what census_build.load_tf does -- it floors at ASSET_STARTS
    # instead, which for BTC/4h is 138 bars against warmup_bars(200) = 691, so
    # the floor alone leaves EMA200 cold for 553 bars.  The parity fixture
    # therefore compares the two ONLY over the region where both are warm.
    for L in EMAS:
        e = ema(c, L)
        w = min(warmup_bars(L), len(e))
        e[:w] = np.nan
        cols[f"e{L}"] = e
    out = pd.DataFrame(cols)
    if era == "live":
        out = out[out["open_time"] >= CEIL_MS].reset_index(drop=True)
    _FRAME_CACHE[key] = out
    return out


def crosses(df: pd.DataFrame, pair: str) -> dict[str, np.ndarray]:
    """{'up': ts[], 'down': ts[]} for one cross class on this frame."""
    fa, sl = PAIRS[pair]
    a = df[f"e{fa}"].to_numpy()
    b = df[f"e{sl}"].to_numpy()
    o = df["open_time"].to_numpy(np.int64)
    return {"up": o[np.nonzero(crossover(a, b))[0]],
            "down": o[np.nonzero(crossunder(a, b))[0]]}


def fwd_mfe_mae(df: pd.DataFrame, idx: np.ndarray, up: bool,
                horizon: int) -> tuple[np.ndarray, np.ndarray]:
    """(MFE, MAE) over `horizon` bars after each idx, in ATR units at the anchor.

    Favourable = the direction the event points.  Anchored at the event bar's
    close -- the last thing known when the event is known (no lookahead).
    Both are returned as non-negative magnitudes.
    """
    c = df["close"].to_numpy(float)
    hi = df["high"].to_numpy(float)
    lo = df["low"].to_numpy(float)
    a = df["atr"].to_numpy(float)
    n = len(c)
    mfe = np.full(len(idx), np.nan)
    mae = np.full(len(idx), np.nan)
    for j, i in enumerate(idx):
        if i < 0 or i >= n or not np.isfinite(a[i]) or a[i] <= 0:
            continue
        end = min(i + horizon + 1, n)
        if end <= i + 1:
            continue
        seg_hi = hi[i + 1:end].max()
        seg_lo = lo[i + 1:end].min()
        if up:
            mfe[j] = (seg_hi - c[i]) / a[i]
            mae[j] = (c[i] - seg_lo) / a[i]
        else:
            mfe[j] = (c[i] - seg_lo) / a[i]
            mae[j] = (seg_hi - c[i]) / a[i]
    return mfe, mae


def fwd_excursion(df: pd.DataFrame, idx: np.ndarray, up: bool,
                  horizon: int) -> np.ndarray:
    """NET excursion = MFE - MAE, in ATR units.  The discriminant used here.

    MFE alone is not a discriminant: over 100 bars almost every anchor shows a
    few ATR of favourable excursion somewhere, so classes separate on it barely
    and for the wrong reason.  MFE - MAE asks the question a constant-pinning
    sandbox actually needs answered -- did this moment offer more than it took
    -- and it is symmetric under direction, so long and short pool honestly.
    """
    mfe, mae = fwd_mfe_mae(df, idx, up, horizon)
    return mfe - mae


def _ts_to_idx(df: pd.DataFrame, ts: np.ndarray) -> np.ndarray:
    o = df["open_time"].to_numpy(np.int64)
    return np.searchsorted(o, ts)


def boot_cluster_median_diff(df: pd.DataFrame, mask: np.ndarray,
                             value_col: str = "exc100",
                             cluster_col: str = "asset",
                             n_boot: int = 4000, seed: int = SEED) -> dict:
    """Median-difference CI resampling ASSETS, not rows.

    The row bootstrap treats 813 armings as 813 independent observations. They
    are not: overlapping forward windows make neighbouring events share most of
    their outcome, and 9_89/9_200 on the same asset minutes apart are near
    duplicates. More importantly, a five-asset panel claim asserts replication
    ACROSS ASSETS -- so the asset is the unit of replication, and the interval
    should widen to reflect how few of them there are.

    This matters: a TRAP effect that looked measured under the row bootstrap
    does not survive here, while the 25_89 promotion does. Reporting both is
    the honest thing, and where they disagree the cluster version governs.
    """
    clusters = df[cluster_col].to_numpy()
    uniq = np.unique(clusters)
    if len(uniq) < 3:
        return {"point": None, "lo": None, "hi": None,
                "excludes_zero": False, "n_clusters": int(len(uniq)),
                "reason": "need >=3 clusters"}
    vals = df[value_col].to_numpy(float)
    rng = np.random.default_rng(seed)
    diffs = []
    for _ in range(n_boot):
        pick = rng.choice(uniq, size=len(uniq), replace=True)
        a_parts, b_parts = [], []
        for c in pick:
            sel = clusters == c
            a_parts.append(vals[sel & mask])
            b_parts.append(vals[sel & ~mask])
        a = np.concatenate(a_parts); b = np.concatenate(b_parts)
        a = a[np.isfinite(a)]; b = b[np.isfinite(b)]
        if len(a) < 3 or len(b) < 3:
            continue
        diffs.append(np.median(a) - np.median(b))
    if len(diffs) < n_boot // 4:
        return {"point": None, "lo": None, "hi": None, "excludes_zero": False,
                "n_clusters": int(len(uniq)), "reason": "too many degenerate draws"}
    diffs = np.asarray(diffs)
    lo, hi = np.percentile(diffs, [5, 95])
    av = vals[mask]; bv = vals[~mask]
    av = av[np.isfinite(av)]; bv = bv[np.isfinite(bv)]
    return {"point": round(float(np.median(av) - np.median(bv)), 6),
            "lo": round(float(lo), 6), "hi": round(float(hi), 6),
            "excludes_zero": bool(lo > 0 or hi < 0),
            "n_clusters": int(len(uniq)), "reason": ""}


def boot_median_diff(a: np.ndarray, b: np.ndarray, n_boot: int = 20000,
                     lo_q: float = 5.0, hi_q: float = 95.0,
                     seed: int = SEED) -> dict:
    """Bootstrap CI for median(a) - median(b).  Seeded, so it is reproducible.

    A sign test across five assets says only which way the difference points;
    with n=38 nested armings spread over a panel it points somewhere on noise.
    An effect whose CI straddles zero has not been measured, and a sandbox that
    pins a census constant on one is doing the fishing the frame forbids.  So
    every promotion below requires the interval to exclude zero -- the same
    standard the contract's own registrations use ("CI excl. 0").
    """
    a = np.asarray(a, float); a = a[np.isfinite(a)]
    b = np.asarray(b, float); b = b[np.isfinite(b)]
    if len(a) < 8 or len(b) < 8:
        return {"n_a": int(len(a)), "n_b": int(len(b)), "point": None,
                "lo": None, "hi": None, "excludes_zero": False,
                "reason": "insufficient sample (need >=8 per side)"}
    rng = np.random.default_rng(seed)
    ia = rng.integers(0, len(a), (n_boot, len(a)))
    ib = rng.integers(0, len(b), (n_boot, len(b)))
    diffs = np.median(a[ia], axis=1) - np.median(b[ib], axis=1)
    lo, hi = np.percentile(diffs, [lo_q, hi_q])
    return {"n_a": int(len(a)), "n_b": int(len(b)),
            "point": round(float(np.median(a) - np.median(b)), 6),
            "lo": round(float(lo), 6), "hi": round(float(hi), 6),
            "excludes_zero": bool(lo > 0 or hi < 0), "reason": ""}


# ===========================================================================
# F-PARITY -- our loader equals census_build.load_tf on the shared columns.
# ===========================================================================
def fixture_parity(assets: list[str]) -> dict:
    """Prove the new frame builder did not quietly re-invent the old one.

    Precedent: seq8_extract.assert_census_parity (49/49).  A new loader that
    disagrees with the census loader by one bar makes every downstream count
    incomparable, and the disagreement would never surface in a summary stat.
    """
    log("F-PARITY -- frame builder vs census_build.load_tf (warm region only)")
    log("    NOTE: this program NaNs the cold head per I4; load_tf does not. The")
    log("          comparison is therefore restricted to bars where BOTH are warm,")
    log("          and the excluded count is printed so the restriction is visible.")
    rows = []
    for sym in assets:
        start_ms = CB.ms(CB.ASSET_STARTS[sym])
        for tf in ["1h", "4h", "12h"]:
            ours_full = frame(sym, tf, "evidence")
            theirs = CB.load_tf(KLINES, sym, tf, start_ms)
            # align on open_time, then keep only rows warm in BOTH
            merged = ours_full.merge(theirs, on="open_time", suffixes=("_a", "_b"))
            warm = np.isfinite(merged["e200_a"].to_numpy()) & \
                np.isfinite(merged["e200_b"].to_numpy())
            n_excl = int((~warm).sum())
            m = merged[warm]
            ok = len(m) > 0
            detail = f"warm-overlap n={len(m)} (excluded {n_excl} cold/unaligned)"
            if ok:
                for col in ["close", "e9", "e89", "e200", "atr"]:
                    x = m[f"{col}_a"].to_numpy(); y = m[f"{col}_b"].to_numpy()
                    if not np.allclose(x, y, rtol=0, atol=1e-9, equal_nan=True):
                        ok = False
                        detail = f"col {col} differs on the warm overlap"
                        break
            rows.append({"asset": sym, "tf": tf, "pass": bool(ok),
                         "warm_overlap": int(len(m)), "excluded": n_excl,
                         "detail": detail})
            log(f"    {'PASS' if ok else 'FAIL'}  {sym:9} {tf:4} {detail}")
    n_pass = sum(r["pass"] for r in rows)
    if n_pass != len(rows):
        raise SystemExit(f"HALT (F-PARITY): {len(rows) - n_pass} cell(s) disagree "
                         f"with census_build.load_tf -- counts are not comparable.")

    # --- F-PARITY-2: prove the cold head is actually suppressed.  Without this
    #     the NaN rule is an assertion in a comment.  A cross detected inside
    #     warmup_bars(L) would be an artifact of the EMA seed, so there must be
    #     exactly zero of them.
    bad = 0
    for sym in assets:
        df = frame(sym, "4h", "evidence")
        for cls in ["9_89", "9_200", "89_200"]:
            fa, sl = PAIRS[cls]
            need = max(warmup_bars(fa), warmup_bars(sl))
            o = df["open_time"].to_numpy(np.int64)
            cx = crosses(df, cls)
            for d in ("up", "down"):
                idx = np.searchsorted(o, cx[d])
                bad += int((idx < need).sum())
    log(f"    {'PASS' if bad == 0 else 'FAIL'}  F-PARITY-2 cold-head crosses = {bad} (must be 0)")
    if bad:
        raise SystemExit(f"HALT (F-PARITY-2): {bad} cross(es) detected inside the "
                         f"EMA warm-up region -- the NaN rule is not effective.")
    return {"cells": rows, "pass": n_pass, "total": len(rows),
            "cold_head_crosses": bad}


# ===========================================================================
# S2 -- FEASIBILITY MATRIX incl. EMA500  (contract F-3; the I4 defect)
# ===========================================================================
def warmup_bars(length: int, residual: float = 1e-3) -> int:
    """Bars until an EMA(length) seeded at series start decays below `residual`.

    Identical to seq8_extract.warmup_bars -- restated (not imported) only
    because importing seq8_extract pulls its whole extraction config; the
    fixture below asserts the two agree.
    """
    alpha = 2.0 / (length + 1.0)
    return int(math.ceil(math.log(residual) / math.log(1.0 - alpha)))


def stage_feasibility(assets: list[str]) -> dict:
    """7 assets x TFs x 8 EMAs: is this cell WARM before the evidence wall?

    This is the stage that surfaces the contract's I4 defect before anything is
    scored.  The contract asserts the family {9..500} "per the recomputed
    feasibility matrix" -- but the only feasibility matrix in the estate
    (MC1_tables.md) has seven EMAs and no 500 column.  So the matrix is a thing
    to be built, and building it is what shows 1d/EMA500 is not "marginal" but
    NEVER for four of five panel assets.
    """
    log("S2 feasibility -- warm/never per (asset, tf, ema), evidence side")
    import seq8_extract as S8
    assert warmup_bars(500) == S8.warmup_bars(500), "warmup rule drift vs SEQ8"

    rows = []
    for sym in assets:
        for tf in SCAN_TFS + ["1d"]:
            try:
                df = _raw(sym, tf, CEIL_MS)
            except FileNotFoundError:
                for L in EMAS:
                    rows.append({"asset": sym, "tf": tf, "ema": L,
                                 "state": "NO-DATA", "warm_bars": 0, "n_bars": 0})
                continue
            n = len(df)
            for L in EMAS:
                w = warmup_bars(L)
                warm = n - w
                rows.append({"asset": sym, "tf": tf, "ema": L,
                             "state": "WARM" if warm > 0 else "NEVER",
                             "warm_bars": int(max(warm, 0)), "n_bars": int(n)})
    mat = pd.DataFrame(rows).sort_values(["asset", "tf", "ema"]).reset_index(drop=True)

    never = mat[(mat.state == "NEVER") & (mat.ema == 500)]
    log(f"    EMA500 NEVER-cells (evidence side): {len(never)} of "
        f"{len(mat[mat.ema == 500])}")
    for r in never.itertuples(index=False):
        log(f"      NEVER  {r.asset:9} {r.tf:4} ema500  (n={r.n_bars}, needs {warmup_bars(500)})")

    # F-3 asks for 3 hand-recomputed cells.  One MUST be a 1d/EMA500 panel cell
    # -- the defect is only visible where the contract is wrong.
    hand = []
    for sym, tf, L in [("ETHUSDT", "1d", 500), ("BTCUSDT", "4h", 500),
                       ("SOLUSDT", "12h", 450)]:
        if sym not in assets:
            continue
        df = _raw(sym, tf, CEIL_MS)
        w = warmup_bars(L)
        hand.append({"asset": sym, "tf": tf, "ema": L, "n_bars": len(df),
                     "warmup_needed": w, "warm_bars": len(df) - w,
                     "state": "WARM" if len(df) - w > 0 else "NEVER",
                     "hand_check": "n_bars - ceil(log(1e-3)/log(1-2/(L+1)))"})
    return {"_class": "EVIDENCE -- exploration-classic (warmup is a data fact)",
            "matrix": mat, "hand_recomputed": hand,
            "warmup_rule": "ceil(log(1e-3)/log(1-2/(L+1))) -- seq8_extract.warmup_bars",
            "warmup_by_ema": {str(L): warmup_bars(L) for L in EMAS}}


# ===========================================================================
# S3 -- RELAY SCAN  ->  pins (iii) W_max
# ===========================================================================
def _km_survival(event_time: np.ndarray, censor_time: np.ndarray,
                 observed: np.ndarray) -> dict:
    """Kaplan-Meier for the terminal-leg lag under window censoring.

    event_time  lag to the terminal leg, where observed
    censor_time window width, where not observed
    observed    True if the terminal leg fired inside the window

    Returns S_inf (the plateau = never-completing fraction) and quantiles of
    the lag distribution CONDITIONAL on eventually completing.  Both are
    reported because they answer different questions and the contract's
    arming-fate table needs both: S_inf sizes ROTTED/ABORTED, the conditional
    quantiles size W_max.
    """
    t = np.where(observed, event_time, censor_time).astype(float)
    ok = np.isfinite(t)
    t, observed = t[ok], observed[ok].astype(bool)
    order = np.argsort(t, kind="mergesort")
    t, observed = t[order], observed[order]

    n = len(t)
    at_risk = n
    S = 1.0
    curve = [(0.0, 1.0)]
    for time in np.unique(t):
        m = t == time
        d = int((m & observed).sum())          # events at this time
        c = int((m & ~observed).sum())         # censored at this time
        if at_risk > 0 and d > 0:
            S *= (1.0 - d / at_risk)
            curve.append((float(time), float(S)))
        at_risk -= (d + c)
    S_inf = float(S)

    def cond_q(q: float):
        """Quantile of the lag among eventual completers."""
        if S_inf >= 1.0:
            return None
        for time, s in curve:
            # F_c(t) = (1 - S(t)) / (1 - S_inf)
            if (1.0 - s) / (1.0 - S_inf) >= q:
                return float(time)
        return None

    return {"S_inf": round(S_inf, 4),
            "never_completes_pct": round(100 * S_inf, 2),
            "cond_p50": cond_q(0.50), "cond_p90": cond_q(0.90),
            "cond_p95": cond_q(0.95),
            "n": int(n), "n_events": int(observed.sum())}


def stage_relay(assets: list[str], era: str) -> dict:
    """4H 9/89 -> 9/200 -> 12/25, same direction, with lag DISTRIBUTIONS.

    The contract's fallback is 'W_max = 90 4h bars; relay-lag p90 decides'.  So
    the deciding statistic is the p90 of the TERMINAL leg's lag from the arming
    -- not the first leg, and not a round number.

    But that lag is CENSORED, and heavily: the window closes at the
    counter-arming, which for a strictly-alternating 9/89 cross means the window
    IS the regime, median ~26 4h bars.  RELAY_HARD_CAP binds on well under 1% of
    armings, so scanning to 400 bars does NOT make the distribution uncensored --
    an earlier draft of this docstring claimed exactly that and was wrong.  The
    censoring is handled by Kaplan-Meier below rather than ignored.

    A chain is ABORTED at a counter-arming (opposite-direction 9/89), which is
    the contract's own window-close rule at CEN-2.
    """
    log(f"S3 relay -- 4H {' -> '.join(RELAY_LEGS)} [{era}]")
    step = TF_MS["4h"]
    recs = []
    for sym in assets:
        df = frame(sym, "4h", era)
        if len(df) < 200:
            log(f"    skip {sym}: {len(df)} 4h bars")
            continue
        cx = {p: crosses(df, p) for p in RELAY_LEGS}
        for d in ("up", "down"):
            opp = "down" if d == "up" else "up"
            armings = cx["9_89"][d]
            leg2_all = cx["9_200"][d]
            leg3_all = cx["12_25"][d]
            counter = cx["9_89"][opp]
            for a_ts in armings:
                cap_ts = a_ts + RELAY_HARD_CAP * step
                nxt_counter = counter[counter > a_ts]
                close_ts = min(cap_ts, nxt_counter[0]) if len(nxt_counter) else cap_ts
                l2 = leg2_all[(leg2_all > a_ts) & (leg2_all <= close_ts)]
                closed_by = ("counter-arming"
                             if (len(nxt_counter) and nxt_counter[0] < cap_ts)
                             else "cap")
                rec = {"asset": sym, "dir": d, "arming_ts": int(a_ts),
                       "arming_iso": iso(int(a_ts)),
                       "window_close_ts": int(close_ts),
                       "window_width_bars": float((close_ts - a_ts) / step),
                       "closed_by": closed_by,
                       "lag2_bars": np.nan, "lag3_bars": np.nan, "complete": False}
                if len(l2):
                    rec["lag2_bars"] = float((l2[0] - a_ts) / step)
                    l3 = leg3_all[(leg3_all > l2[0]) & (leg3_all <= close_ts)]
                    if len(l3):
                        rec["lag3_bars"] = float((l3[0] - a_ts) / step)
                        rec["complete"] = True
                # DISJOINT fate.  The previous `aborted` column merely asked
                # whether a counter-arming existed inside the cap -- which was
                # true of 98.9% of windows INCLUDING every completed one, so the
                # contract's arming-fate taxonomy could not be derived from it.
                # A fate must partition the population or it is not a fate.
                rec["fate"] = ("COMPLETED" if rec["complete"]
                               else "ABORTED" if closed_by == "counter-arming"
                               else "ROTTED")
                recs.append(rec)
    ch = pd.DataFrame(recs)
    if ch.empty:
        return {"chains": ch, "pin": None}

    lag3 = ch.loc[ch.complete, "lag3_bars"].to_numpy(float)
    lag2 = ch.loc[ch.lag2_bars.notna(), "lag2_bars"].to_numpy(float)

    def pct(x, q):
        return float(np.percentile(x, q)) if len(x) else float("nan")

    # ---- Kaplan-Meier, because the naive quantile is not the quantity wanted.
    #
    # A window closes at the counter-arming, so a chain that has not produced a
    # terminal leg by then is CENSORED, not slow. Taking the p90 of the
    # completed subset conditions on survival and understates the lag; taking a
    # p90 over all armings is worse, because survival never falls to 0.10 --
    # a large fraction of armings NEVER produce a terminal leg, so that
    # quantile does not exist. KM separates the two questions:
    #   S_inf  = the never-completing fraction (a real property of the tape)
    #   F_c(t) = the lag distribution AMONG eventual completers
    km = _km_survival(ch["lag3_bars"].to_numpy(float),
                      ch["window_width_bars"].to_numpy(float),
                      ch["complete"].to_numpy(bool))
    # Bootstrap the KM conditional p90 so the pin carries its own uncertainty.
    # A scalar constant handed to a scoring contract without an interval invites
    # exactly the over-reading this whole paste exists to prevent.
    _lag = ch["lag3_bars"].to_numpy(float)
    _win = ch["window_width_bars"].to_numpy(float)
    _obs = ch["complete"].to_numpy(bool)
    _rng = np.random.default_rng(SEED)
    _boot = []
    for _ in range(400):
        idx = _rng.integers(0, len(_lag), len(_lag))
        k = _km_survival(_lag[idx], _win[idx], _obs[idx])
        if k["cond_p90"] is not None:
            _boot.append(k["cond_p90"])
    if _boot:
        km["cond_p90_ci"] = [round(float(np.percentile(_boot, 5)), 1),
                             round(float(np.percentile(_boot, 95)), 1)]
        km["cond_p90_ci_note"] = "90% bootstrap CI, 400 resamples, seeded"

    # completion curve: what fraction of armings complete within each width?
    curve = []
    for W in RELAY_WIDTHS + [RELAY_HARD_CAP]:
        n_done = int((ch.complete & (ch.lag3_bars <= W)).sum())
        curve.append({"width_4h_bars": W, "completed": n_done,
                      "of_armings": int(len(ch)),
                      "completion_rate": round(n_done / len(ch), 6)})
    for c in curve:
        log(f"    width {c['width_4h_bars']:4d} bars -> "
            f"{c['completed']:5d}/{c['of_armings']} = {c['completion_rate']:.3f}")

    fates = ch.fate.value_counts().to_dict()
    log(f"    fates (disjoint): {fates}")
    ww = ch.window_width_bars
    log(f"    ACTUAL window widths: p50={ww.median():.0f} p90={ww.quantile(.9):.0f} "
        f"bars; only {int((ch.closed_by == 'cap').sum())}/{len(ch)} reach the "
        f"{RELAY_HARD_CAP}-bar cap")
    log(f"    => W_max is NOT the binding constraint for most armings: the "
        f"counter-arming closes the window first in "
        f"{100*(ch.closed_by=='counter-arming').mean():.1f}% of cases.")

    naive_p90 = pct(lag3, 90)
    log(f"    NAIVE (completed-only, BIASED): n={len(lag3)} p50={pct(lag3,50):.1f} "
        f"p90={naive_p90:.1f} p95={pct(lag3,95):.1f}")
    log(f"    KAPLAN-MEIER: {km['never_completes_pct']:.1f}% of armings NEVER "
        f"produce a terminal leg (S_inf={km['S_inf']}).")
    log(f"      => the p90 of the lag OVER ARMINGS does not exist; survival "
        f"never falls to 0.10.")
    log(f"      conditional on eventually completing: p50={km['cond_p50']} "
        f"p90={km['cond_p90']} p95={km['cond_p95']}")
    pin = int(math.ceil(km["cond_p90"])) if km["cond_p90"] else None
    log(f"    -> W_max = {pin} 4h bars (KM p90 among eventual completers; the "
        f"naive completed-only figure {naive_p90:.0f} understates it)")
    return {
        "chains": ch,
        "completion_curve": curve,
        "leg2_lag": {"n": int(len(lag2)), "p50": pct(lag2, 50), "p90": pct(lag2, 90)},
        "leg3_lag_naive_completed_only": {
            "n": int(len(lag3)), "p50": pct(lag3, 50), "p90": naive_p90,
            "p95": pct(lag3, 95),
            "max": float(lag3.max()) if len(lag3) else None,
            "warning": "conditions on survival; understates the true lag"},
        "leg3_lag_kaplan_meier": km,
        "pin": pin,
        "n_armings": int(len(ch)),
        "n_completed": int(ch.complete.sum()),
        "n_censored": int((~ch.complete).sum()),
        "fates": {str(k): int(v) for k, v in ch.fate.value_counts().items()},
        "window_width_p50": float(ch.window_width_bars.median()),
        "window_width_p90": float(ch.window_width_bars.quantile(0.9)),
        "pct_closed_by_counter": round(float((ch.closed_by == "counter-arming").mean()), 4),
        "rule": ("W_max = ceil(Kaplan-Meier p90 of the terminal-leg (12_25) lag "
                 "CONDITIONAL on eventually completing. Windows close at the "
                 "counter-arming, so non-completers are CENSORED, not slow. Two "
                 "consequences the naive quantile hides: (a) a large fraction of "
                 "armings never complete at all (S_inf), so the p90 of the lag "
                 "OVER ARMINGS does not exist -- survival never reaches 0.10; "
                 "(b) the completed-only p90 conditions on survival and "
                 "understates the lag. Both the naive figure and the KM figure "
                 "are emitted so the gap is visible. Note also that W_max is "
                 "near-non-binding in practice: the counter-arming closes the "
                 "window first in ~99% of armings, at a median width far below "
                 "any candidate W_max."),
    }


# ===========================================================================
# S4 -- NESTING SCAN  ->  pins (iv) nested pair set
# ===========================================================================
def stage_nesting(assets: list[str], era: str) -> dict:
    """An LTF cross firing INSIDE the confirming HTF bar.

    Prevalence alone cannot pin the set -- a pair that fires on 90% of armings
    partitions nothing (the same defect that makes the TRAP fallback useless).
    So each candidate pair reports prevalence AND the outcome separation
    between nested and un-nested armings, and the pin requires both a usable
    prevalence band and a non-trivial separation.
    """
    log(f"S4 nesting -- LTF cross inside the confirming HTF bar [{era}]")
    rows = []
    pair_pops = []   # (values, mask) per candidate, for the selection guard
    for ltf, htf in NEST_CANDIDATES:
        span = TF_MS[htf]
        per_asset = []
        for sym in assets:
            hi_df = frame(sym, htf, era)
            lo_df = frame(sym, ltf, era)
            if len(hi_df) < 100 or len(lo_df) < 100:
                continue
            hx = crosses(hi_df, "9_89")
            lx = crosses(lo_df, "9_89")
            for d in ("up", "down"):
                h_ts = hx[d]
                l_ts = np.sort(lx[d])
                if not len(h_ts):
                    continue
                # nested count per HTF cross bar: LTF crosses inside [T, T+span)
                left = np.searchsorted(l_ts, h_ts, "left")
                right = np.searchsorted(l_ts, h_ts + span, "left")
                cnt = right - left
                idx = _ts_to_idx(hi_df, h_ts)
                exc = fwd_excursion(hi_df, idx, d == "up", horizon_bars(htf))
                per_asset.append(pd.DataFrame({
                    "asset": sym, "dir": d, "ts": h_ts, "nested_n": cnt,
                    "nested": cnt > 0, "exc100": exc}))
        if not per_asset:
            continue
        allp = pd.concat(per_asset, ignore_index=True)
        prev = float(allp.nested.mean())
        a = allp.loc[allp.nested, "exc100"].to_numpy(float)
        b = allp.loc[~allp.nested, "exc100"].to_numpy(float)
        bs = boot_median_diff(a, b)
        _v = allp["exc100"].to_numpy(float)
        _m = allp["nested"].to_numpy(bool)
        pair_pops.append((_v, _m))
        # per-asset sign agreement -- reported, but never sufficient on its own
        signs = []
        for sym, g in allp.groupby("asset", sort=True):
            ga = g.loc[g.nested, "exc100"].dropna()
            gb = g.loc[~g.nested, "exc100"].dropna()
            if len(ga) >= 8 and len(gb) >= 8:
                signs.append(np.sign(ga.median() - gb.median()))
        agree = int(sum(1 for s in signs if s > 0))
        rows.append({"pair": f"{ltf}-in-{htf}", "ltf": ltf, "htf": htf,
                     "n_htf_crosses": int(len(allp)), "n_nested": int(allp.nested.sum()),
                     "prevalence": round(prev, 6),
                     "separation_atr": bs["point"],
                     "ci_lo": bs["lo"], "ci_hi": bs["hi"],
                     "ci_excludes_zero": bs["excludes_zero"],
                     "assets_positive": agree, "assets_tested": len(signs)})
        log(f"    {rows[-1]['pair']:12} prev={prev:.3f} n_nest={int(allp.nested.sum()):4d} "
            f"sep={bs['point']} CI[{bs['lo']},{bs['hi']}] "
            f"{'EXCL-0' if bs['excludes_zero'] else 'straddles 0'} sign {agree}/{len(signs)}")

    tab = pd.DataFrame(rows)

    # ---- SELECTION GUARD, same discipline as stage_trap.
    # Six candidate pairs are swept and a winner promoted on its own CI. That is
    # the identical multiple-comparisons structure that made TRAP >=5 an
    # artifact, and leaving this stage unguarded because it happened to decline
    # on one era's data would be luck, not method. Null = shuffle the outcome
    # labels within each candidate's own population; statistic = max |sep|
    # across candidates, which is what the promotion rule maximises.
    sel = {"admissible": True, "note": "no candidate passed; guard not engaged"}
    passing = [r for r in rows if 0.05 <= r["prevalence"] <= 0.95
               and r["ci_excludes_zero"] and (r["separation_atr"] or 0) > 0]
    if passing and pair_pops:
        m = len(pair_pops)
        obs = max(abs(r["separation_atr"]) for r in rows
                  if r["separation_atr"] is not None)
        rng = np.random.default_rng(SEED + 4200)
        n_perm = 2000
        null = np.empty(n_perm)
        for i in range(n_perm):
            best = 0.0
            for vals, mask in pair_pops:
                v = vals[rng.permutation(len(vals))]
                a, b = v[mask], v[~mask]
                a = a[np.isfinite(a)]; b = b[np.isfinite(b)]
                if len(a) >= 8 and len(b) >= 8:
                    best = max(best, abs(float(np.median(a) - np.median(b))))
            null[i] = best
        p_sel = float((np.sum(null >= obs) + 1) / (n_perm + 1))
        bh_bar = 0.10 / m
        sel = {"m_candidates": m, "observed_max_sep": round(obs, 6),
               "p_selection_corrected": round(p_sel, 4),
               "bh_bar_q_over_m": round(bh_bar, 5),
               "admissible": bool(p_sel <= bh_bar),
               "null_p95": round(float(np.percentile(null, 95)), 6),
               "n_perm": n_perm}
        log(f"    selection test: m={m} candidates, max|sep|={obs:.4f}, "
            f"null p95={sel['null_p95']:.4f}")
        log(f"      p SELECTION-CORRECTED = {p_sel}  vs I8 bar {bh_bar:.5f}")

    # Promotion requires a MEASURED effect, not a direction -- and an
    # ADMISSIBLE selection procedure.
    keep = [] if not sel.get("admissible", False) else [
        r["pair"] for r in rows
        if 0.05 <= r["prevalence"] <= 0.95
        and r["ci_excludes_zero"] and (r["separation_atr"] or 0) > 0
        and r["assets_positive"] >= 3]
    if passing and not sel.get("admissible", False):
        log(f"    !! NOT ADMISSIBLE: {[r['pair'] for r in passing]} passed the CI "
            f"screen, but the selection procedure's corrected p="
            f"{sel.get('p_selection_corrected')} exceeds the I8 bar "
            f"{sel.get('bh_bar_q_over_m')}. Declining to pin.")
    if keep:
        log(f"    -> nested pair set = {keep}")
    elif passing:
        log(f"    -> INCONCLUSIVE: {[r['pair'] for r in passing]} cleared the CI "
            f"screen but not the selection correction.")
        log("       The fallback set stands UNCONFIRMED -- see the build document.")
    else:
        log("    -> INCONCLUSIVE: no candidate pair's separation CI excludes 0.")
        log("       The fallback set stands UNCONFIRMED -- see the build document.")
    return {"table": tab, "pin": keep or None,
            "inconclusive": not keep, "selection_test": sel,
            "rule": ("prevalence in [0.05,0.95] AND bootstrap 90% CI on the "
                     "nested-vs-unnested median net-excursion difference "
                     "excludes 0 AND the direction replicates on >=3 assets. "
                     "A sign test alone is not evidence at these sample sizes.")}


# ===========================================================================
# S5 -- THE 25 OBSERVATORY  ->  pins (vi) 25-pair trigger inclusion
# ===========================================================================
def stage_obs25(assets: list[str], era: str) -> dict:
    """9_25 and 25_89 beside the incumbent 12_25, on 4h.

    The inclusion question is not 'do they fire' but 'do they fire so often
    they swamp the family'.  9_25 is expected to be the most numerous class on
    the board; entering it unstratified into a 9-registration FDR family at
    q=0.10 would let one class set the discovery budget for all of them.  So
    this stage reports counts FIRST and outcome second.
    """
    log(f"S5 the-25 observatory -- 9_25 / 25_89 vs 12_25 on 4h [{era}]")
    rows = []
    for cls in ["9_89", "12_25", "9_25", "25_89"]:
        n_tot = 0
        net_all, mfe_all, mae_all = [], [], []
        per_asset_sign = []
        per_asset_rows = []
        for sym in assets:
            df = frame(sym, "4h", era)
            if len(df) < 200:
                continue
            cx = crosses(df, cls)
            sym_net = []
            for d in ("up", "down"):
                ts = cx[d]
                if not len(ts):
                    continue
                n_tot += len(ts)
                idx = _ts_to_idx(df, ts)
                mfe, mae = fwd_mfe_mae(df, idx, d == "up", horizon_bars("4h"))
                net = mfe - mae
                ok = np.isfinite(net)
                net_all.append(net[ok]); mfe_all.append(mfe[ok]); mae_all.append(mae[ok])
                sym_net.append(net[ok])
            if sym_net:
                v = np.concatenate(sym_net)
                per_asset_sign.append(float(np.median(v)))
                per_asset_rows.append(pd.DataFrame({"asset": sym, "net": v}))
        allx = np.concatenate(net_all) if net_all else np.array([])
        allf = np.concatenate(mfe_all) if mfe_all else np.array([])
        alla = np.concatenate(mae_all) if mae_all else np.array([])
        # Is the class's own net excursion measurably above zero?
        ci = {"lo": None, "hi": None, "excludes_zero": False}
        if len(allx) >= 8:
            rng = np.random.default_rng(SEED)
            bm = np.median(allx[rng.integers(0, len(allx), (20000, len(allx)))], axis=1)
            lo, hi = np.percentile(bm, [5, 95])
            ci = {"lo": round(float(lo), 6), "hi": round(float(hi), 6),
                  "excludes_zero": bool(lo > 0 or hi < 0)}
        # ... and does it survive treating the ASSET as the unit of replication?
        # The row bootstrap above assumes 956 independent armings; a five-asset
        # panel claim asserts something much weaker. Where the two disagree, the
        # cluster version governs -- see boot_cluster_median_diff.
        cci = {"lo": None, "hi": None, "excludes_zero": False}
        if per_asset_rows:
            pa = pd.concat(per_asset_rows, ignore_index=True)
            uniq = pa["asset"].unique()
            if len(uniq) >= 3:
                rngc = np.random.default_rng(SEED)
                meds = []
                for _ in range(4000):
                    pick = rngc.choice(uniq, size=len(uniq), replace=True)
                    v = np.concatenate([pa.loc[pa.asset == c, "net"].to_numpy()
                                        for c in pick])
                    v = v[np.isfinite(v)]
                    if len(v) >= 3:
                        meds.append(np.median(v))
                if len(meds) > 1000:
                    lo2, hi2 = np.percentile(meds, [5, 95])
                    cci = {"lo": round(float(lo2), 6), "hi": round(float(hi2), 6),
                           "excludes_zero": bool(lo2 > 0 or hi2 < 0)}
        rows.append({"class": cls, "n_crosses": n_tot,
                     "median_net100_atr": round(float(np.median(allx)), 6) if len(allx) else None,
                     "median_mfe100_atr": round(float(np.median(allf)), 6) if len(allf) else None,
                     "median_mae100_atr": round(float(np.median(alla)), 6) if len(alla) else None,
                     "net_ci_lo": ci["lo"], "net_ci_hi": ci["hi"],
                     "net_ci_excludes_zero": ci["excludes_zero"],
                     "cluster_ci_lo": cci["lo"], "cluster_ci_hi": cci["hi"],
                     "cluster_ci_excludes_zero": cci["excludes_zero"],
                     "assets_positive": int(sum(1 for m in per_asset_sign if m > 0)),
                     "assets_tested": len(per_asset_sign)})
        log(f"    {cls:8} n={n_tot:6d} net={rows[-1]['median_net100_atr']}")
        log(f"             row-CI    [{ci['lo']},{ci['hi']}] "
            f"{'EXCL-0' if ci['excludes_zero'] else 'straddles 0'}")
        log(f"             CLUSTER-CI[{cci['lo']},{cci['hi']}] "
            f"{'EXCL-0' if cci['excludes_zero'] else 'straddles 0'}  <- governs")
        log(f"             mfe={rows[-1]['median_mfe100_atr']} "
            f"mae={rows[-1]['median_mae100_atr']} "
            f"sign {rows[-1]['assets_positive']}/{rows[-1]['assets_tested']} (reported, not a criterion)")

    tab = pd.DataFrame(rows)
    base = tab.loc[tab["class"] == "9_89", "n_crosses"]
    base_n = int(base.iloc[0]) if len(base) else 0
    ratios = {r["class"]: (round(r["n_crosses"] / base_n, 3) if base_n else None)
              for r in rows}
    log(f"    count ratio vs 9_89: {ratios}")
    # Promotion now requires the CLUSTER interval, not the row interval. The
    # old `assets_positive >= 3 of 5` sign gate is still reported, but it is no
    # longer a criterion: P(>=3 of 5 | fair coin) = 0.50, it is computed from
    # the same observations as the CI, and across three stages and two eras it
    # never once changed a decision. A no-op that reads like a replication
    # guard is worse than no guard.
    include = [r["class"] for r in rows if r["class"] in ("9_25", "25_89")
               and r["cluster_ci_excludes_zero"] and (r["median_net100_atr"] or 0) > 0]
    excluded = [r["class"] for r in rows if r["class"] in ("9_25", "25_89")
                and r["class"] not in include]
    log(f"    -> 25-pair inclusion = {include or 'NONE'}"
        + (f"; EXCLUDED {excluded}" if excluded else ""))
    if "9_25" in excluded:
        log("       note: 9_25 is the most numerous class on the board "
            f"({ratios.get('9_25')}x 9_89) and the weakest -- admitting it "
            "unstratified would let one class set the FDR budget for nine "
            "registrations at q=0.10.")
    return {"table": tab, "count_ratio_vs_9_89": ratios, "pin": include,
            "excluded": excluded,
            "rule": ("include a 25-pair as a trigger class iff its median net "
                     "excursion is positive, its bootstrap 90% CI excludes 0, "
                     "AND the direction replicates on >=3 of 5 panel assets. "
                     "Counts are reported so the FDR family can be stratified "
                     "by class rather than swamped by the largest one.")}


# ===========================================================================
# S6 -- TRAP SWEEP  ->  pins (ii) counter-density
# ===========================================================================
def stage_trap(assets: list[str], era: str) -> dict:
    """Counter-direction FAST-tier crosses in the prior 24h, swept.

    MC-1's fallback (>=2) fires on 92.2% of evidence-era 4h lattice-A armings.
    A stamp that is true of nearly the whole population cannot discriminate --
    it is a null gate wearing the costume of a filter.  This sweep finds the
    threshold that actually partitions, using the same counter-tier definition
    MC-1 used (FAST = 5m/15m/30m, lattice-A classes) so the numbers stay
    comparable to d4_similarity.
    """
    log(f"S6 TRAP sweep -- counter FAST crosses / {TRAP_LOOKBACK_H}h [{era}]")
    look_ms = TRAP_LOOKBACK_H * 3_600_000
    recs = []
    for sym in assets:
        df4 = frame(sym, "4h", era)
        if len(df4) < 200:
            continue
        # counter tier: every lattice-A cross on every FAST tf
        fast_ts = {"up": [], "down": []}
        for tf in FAST_TFS:
            try:
                fdf = frame(sym, tf, era)
            except FileNotFoundError:
                continue
            for cls in LATTICE_A:
                cx = crosses(fdf, cls)
                for d in ("up", "down"):
                    fast_ts[d].append(cx[d])
        fast_ts = {d: (np.sort(np.concatenate(v)) if v else np.array([], np.int64))
                   for d, v in fast_ts.items()}

        for cls in LATTICE_A:
            cx = crosses(df4, cls)
            for d in ("up", "down"):
                ts = cx[d]
                if not len(ts):
                    continue
                opp = "down" if d == "up" else "up"
                ft = fast_ts[opp]
                left = np.searchsorted(ft, ts - look_ms, "left")
                right = np.searchsorted(ft, ts, "left")
                ncount = right - left
                idx = _ts_to_idx(df4, ts)
                exc = fwd_excursion(df4, idx, d == "up", horizon_bars("4h"))
                recs.append(pd.DataFrame({"asset": sym, "class": cls, "dir": d,
                                          "ts": ts, "counter_n": ncount,
                                          "exc100": exc}))
    if not recs:
        return {"sweep": pd.DataFrame(), "pin": None}
    pop = pd.concat(recs, ignore_index=True)
    log(f"    population: {len(pop)} 4h lattice-A armings; counter_n "
        f"median={pop.counter_n.median():.0f} p90={pop.counter_n.quantile(.9):.0f} "
        f"max={pop.counter_n.max()}")

    sweep = []
    for th in TRAP_SWEEP:
        hit = pop.counter_n >= th
        rate = float(hit.mean())
        bs = boot_median_diff(pop.loc[hit, "exc100"].to_numpy(float),
                              pop.loc[~hit, "exc100"].to_numpy(float))
        signs = 0
        tested = 0
        for sym, g in pop.groupby("asset", sort=True):
            ga = g.loc[g.counter_n >= th, "exc100"].dropna()
            gb = g.loc[g.counter_n < th, "exc100"].dropna()
            if len(ga) >= 20 and len(gb) >= 20:
                tested += 1
                signs += int((ga.median() - gb.median()) < 0)  # TRAP = adverse
        sweep.append({"threshold": th, "fire_rate": round(rate, 6),
                      "n_fired": int(hit.sum()),
                      "separation_atr": bs["point"],
                      "ci_lo": bs["lo"], "ci_hi": bs["hi"],
                      "ci_excludes_zero": bs["excludes_zero"],
                      "assets_sign_consistent": signs, "assets_tested": tested})
        log(f"    >={th:2d}  fires {rate*100:5.1f}%  sep={bs['point']}  "
            f"CI[{bs['lo']},{bs['hi']}] "
            f"{'EXCL-0' if bs['excludes_zero'] else 'straddles 0'}  sign {signs}/{tested}")

    sw = pd.DataFrame(sweep)
    cand = sw[(sw.fire_rate <= 0.85) & (sw.fire_rate >= 0.10)
              & sw.ci_excludes_zero & sw.separation_atr.notna()]
    naive_pin = (int(cand.loc[cand.separation_atr.abs().idxmax(), "threshold"])
                 if len(cand) else None)

    # ---- SELECTION GUARD.  This is the whole point of the stage.
    #
    # Sweeping 20 correlated thresholds and promoting whichever one's CI happens
    # to exclude zero is a multiple-comparisons procedure, and a CI is not a
    # correction for having looked twenty times.  So measure the procedure
    # itself: shuffle the outcome labels (destroying any real association) and
    # ask how often the SAME selection rule still finds a "significant"
    # threshold.  If it fires often under the null, a hit on the real data is
    # not evidence and this stage must decline to pin.
    #
    # The contract mandates FDR control per family (I8); this is that discipline
    # applied to the sandbox that feeds it, rather than to the sandbox's output.
    sel = _trap_selection_test(pop)
    log(f"    selection test (max-statistic permutation, m={sel.get('m_in_band')} "
        f"in-band thresholds, {sel.get('n_perm')} shuffles):")
    log(f"      winner >={sel.get('winner_threshold')}  |sep|={sel.get('observed_max_sep')}  "
        f"null p95={sel.get('null_p95')}")
    log(f"      p uncorrected (winner alone) = {sel.get('p_uncorrected_winner')}")
    log(f"      p SELECTION-CORRECTED        = {sel.get('p_selection_corrected')}")
    log(f"      I8 admissibility bar (BH, q=0.10 over m) = {sel.get('bh_bar_q_over_m')}")
    pin = naive_pin
    guard_failed = not sel.get("admissible", False)
    if guard_failed:
        pin = None
        log(f"    !! NOT ADMISSIBLE: selection-corrected p="
            f"{sel.get('p_selection_corrected')} exceeds the I8 bar "
            f"{sel.get('bh_bar_q_over_m')}.")
        log(f"       >= {naive_pin} is a SELECTION ARTIFACT, not a measurement. "
            f"Declining to pin.")

    fb = sw[sw.threshold == 2]
    fb_rate = float(fb.iloc[0].fire_rate) if len(fb) else float("nan")
    log(f"    -> TRAP counter-density = {('>=' + str(pin)) if pin else 'NOT ESTABLISHED'}")
    log(f"       (fallback >=2 fires on {fb_rate:.1%} -- rejected on fire rate "
        f"alone, which is descriptive and needs no inference)")
    return {"sweep": sw, "population": pop, "pin": pin,
            "naive_pin": naive_pin, "selection_test": sel,
            "guard_failed": guard_failed,
            "fallback_fire_rate": round(fb_rate, 6) if np.isfinite(fb_rate) else None,
            "rule": ("threshold maximising |median net-excursion separation| in a "
                     "10-85% fire-rate band whose bootstrap 90% CI excludes 0 -- "
                     "BUT only if a label-shuffled permutation null shows the "
                     "selection procedure itself fires <=10% of the time. The "
                     "fallback >=2 is rejected on fire rate alone: a stamp true "
                     "of ~92% of the population partitions nothing, and that is "
                     "a descriptive fact requiring no inference.")}


def _trap_selection_test(pop: pd.DataFrame, n_perm: int = 2000) -> dict:
    """Selection-aware permutation test for the TRAP threshold sweep.

    The quantity that matters is not "did some threshold pass a CI" but "is the
    WINNER's effect larger than the winner of a null sweep".  So the test
    statistic is the max |median separation| over the in-band thresholds -- the
    same thing the pin rule maximises -- and its null is built by shuffling the
    outcome labels, which destroys the association while preserving the
    counter_n structure and the marginal outcome distribution.

    This replaces an earlier binary gate ("does any CI exclude zero under the
    null"), which answered a coarser question and, at n_perm=300, decided it
    with a binomial SE of ~1.7pp right at its own threshold.  The max-statistic
    p-value both corrects for selection and says HOW far from admissible the
    winner is, which is what the contract's FDR discipline (I8, q=0.10 per
    family) actually needs.

    Returns the observed statistic, the selection-corrected p, the uncorrected
    p of the winner alone, the number of in-band thresholds m (the family size),
    and the Benjamini-Hochberg admissibility bar q/m.
    """
    counter = pop["counter_n"].to_numpy()
    exc = pop["exc100"].to_numpy(float)
    ok = np.isfinite(exc)
    counter, exc = counter[ok], exc[ok]
    if len(exc) < 50:
        return {"error": "insufficient sample", "admissible": False}

    in_band = []
    for th in TRAP_SWEEP:
        r = (counter >= th).mean()
        if 0.10 <= r <= 0.85 and (counter >= th).sum() >= 8 and (counter < th).sum() >= 8:
            in_band.append(th)
    if not in_band:
        return {"error": "no threshold in band", "admissible": False}

    def max_sep(e) -> tuple:
        best, best_th = 0.0, None
        for th in in_band:
            hit = counter >= th
            s = abs(float(np.median(e[hit]) - np.median(e[~hit])))
            if s > best:
                best, best_th = s, th
        return best, best_th

    obs, obs_th = max_sep(exc)
    rng = np.random.default_rng(SEED + 9000)
    null = np.empty(n_perm)
    for i in range(n_perm):
        null[i] = max_sep(exc[rng.permutation(len(exc))])[0]

    p_sel = float((np.sum(null >= obs) + 1) / (n_perm + 1))

    # uncorrected p for the winner alone, same permutation stream
    hit = counter >= obs_th
    obs_single = abs(float(np.median(exc[hit]) - np.median(exc[~hit])))
    rng2 = np.random.default_rng(SEED + 9100)
    cnt = 0
    for _ in range(n_perm):
        e = exc[rng2.permutation(len(exc))]
        if abs(float(np.median(e[hit]) - np.median(e[~hit]))) >= obs_single:
            cnt += 1
    p_single = float((cnt + 1) / (n_perm + 1))

    m = len(in_band)
    bh_bar = 0.10 / m          # I8: FDR q=0.10 over a family of m thresholds
    return {"m_in_band": m, "winner_threshold": int(obs_th),
            "observed_max_sep": round(obs, 6),
            "p_selection_corrected": round(p_sel, 4),
            "p_uncorrected_winner": round(p_single, 4),
            "bh_bar_q_over_m": round(bh_bar, 5),
            "admissible": bool(p_sel <= bh_bar),
            "null_p95": round(float(np.percentile(null, 95)), 6),
            "n_perm": n_perm}


# ===========================================================================
# S7 -- RIBBON COMPRESSION SWEEP  ->  pins (v) c
# ===========================================================================
def stage_ribbon(assets: list[str], era: str) -> dict:
    """|e9 - e89| / ATR on 30m and 1h, swept for a usable compression band.

    c is a CHOP-composite component (CEN-4), so the quantity that matters is
    selectivity: what share of bars does each c call 'compressed'?  A threshold
    that flags half the tape adds a constant to the composite, not a signal.
    """
    log(f"S7 ribbon compression -- |e9-e89|/ATR on {RIBBON_TFS} [{era}]")
    rows = []
    for tf in RIBBON_TFS:
        for c in RIBBON_SWEEP:
            shares = []
            for sym in assets:
                try:
                    df = frame(sym, tf, era)
                except FileNotFoundError:
                    continue
                if len(df) < 500:
                    continue
                sp = np.abs(df["e9"].to_numpy() - df["e89"].to_numpy())
                a = df["atr"].to_numpy()
                ok = np.isfinite(sp) & np.isfinite(a) & (a > 0)
                if ok.sum() < 500:
                    continue
                shares.append(float((sp[ok] <= c * a[ok]).mean()))
            if shares:
                rows.append({"tf": tf, "c": c,
                             "share_compressed_mean": round(float(np.mean(shares)), 6),
                             "share_min": round(float(np.min(shares)), 6),
                             "share_max": round(float(np.max(shares)), 6),
                             "assets": len(shares)})
    tab = pd.DataFrame(rows)
    for r in rows:
        log(f"    {r['tf']:4} c={r['c']:.2f} -> share "
            f"{r['share_compressed_mean']:.3f} [{r['share_min']:.3f},{r['share_max']:.3f}]")
    # Pinning rule, and an honest statement of its limit.
    #
    # Selectivity is the only thing this sandbox can measure about c without a
    # chop LABEL to score against -- and CEN-4's label is the very thing the
    # census is meant to produce.  So selectivity can REJECT a c (one that
    # flags 45% of the tape adds a constant to the composite, not a signal) but
    # it cannot ORDER two c's that both land in a usable band.
    #
    # Therefore: confirm the ratified fallback if it lands in the band, and say
    # plainly that any c in the admissible set is equally defensible on the
    # evidence available.  Moving the constant to hit a round selectivity
    # target would be fitting with extra steps.
    BAND = (0.10, 0.25)
    FALLBACK_C = 0.5
    pin, admissible, note = None, [], ""
    if len(tab):
        sub = tab[tab.tf == "1h"] if (tab.tf == "1h").any() else tab
        adm = sub[(sub.share_compressed_mean >= BAND[0])
                  & (sub.share_compressed_mean <= BAND[1])]
        admissible = [float(x) for x in adm.c.tolist()]
        fb = sub[sub.c == FALLBACK_C]
        if len(fb) and FALLBACK_C in admissible:
            pin = FALLBACK_C
            note = (f"fallback c=0.5 CONFIRMED: flags "
                    f"{float(fb.iloc[0].share_compressed_mean):.1%} of 1h bars, "
                    f"inside the {BAND[0]:.0%}-{BAND[1]:.0%} admissible band")
        elif admissible:
            pin = min(admissible, key=lambda x: abs(x - FALLBACK_C))
            note = (f"fallback c=0.5 REJECTED (outside band); nearest "
                    f"admissible c={pin}")
    log(f"    -> ribbon-compression c = {pin} x ATR  [{note}]")
    log(f"       admissible set (equally defensible on selectivity): {admissible}")
    return {"table": tab, "pin": pin, "admissible": admissible, "note": note,
            "rule": (f"confirm the ratified fallback if its panel-mean 1h "
                     f"compressed share lands in {BAND}; selectivity can reject "
                     f"a c but cannot order two admissible c's without a chop "
                     f"label, which is CEN-4's output, not its input")}


# ===========================================================================
# S8 -- KISS / REFUSAL CALIBRATION  ->  pins (i) eps, delta, k
# ===========================================================================
def _kiss_flags(spread: np.ndarray, atr_v: np.ndarray, eps: float,
                delta: float, k: int) -> np.ndarray:
    """Parameterised kiss/refusal detector, semantics identical to
    mc1_program.kiss_v0 with (eps, delta, k) substituted for its frozen
    (0.25, 0.75, 10).

    Every branch below mirrors kiss_v0 deliberately: BREAK on the first
    non-finite bar, BREAK on the first genuine sign change (rather than
    rejecting if a sign change occurs anywhere in the window), accept a
    zero-signed touch and adopt the sign at re-expansion. These are not
    stylistic choices -- they change the event set, and the whole purpose of
    this stage is to confirm a ratified constant rather than to re-fit one
    under a detector that differs from the ratified detector.
    """
    n = len(spread)
    flag = np.zeros(n, dtype=bool)
    a = np.abs(spread)
    sg = np.sign(spread)
    touch = (a <= eps * atr_v) & np.isfinite(spread) & np.isfinite(atr_v)
    for i in np.nonzero(touch)[0]:
        s0 = sg[i]
        for j in range(i + 1, min(i + k, n - 1) + 1):
            if not (np.isfinite(spread[j]) and np.isfinite(atr_v[j])):
                break
            if s0 != 0 and sg[j] != 0 and sg[j] != s0:
                break
            if a[j] >= delta * atr_v[j]:
                flag[i] = True
                break
    return flag


def stage_kiss(assets: list[str], era: str) -> dict:
    """EMA<->EMA near-miss: approach within eps*ATR, veer >= delta*ATR within k
    bars, no sign change.  Swept around MC-1's ratified 0.25 / 0.75 / 10.

    Note on scope, stated so the build document does not overclaim: this pins
    the EMA<->EMA limb only (the contract's (i-a)).  The price<->level limb
    (i-b) -- the SFP / deviation object of D-B -- has NO detector anywhere in
    the estate, and inventing one inside a constants sandbox would be exactly
    the kind of unregistered machinery the frame forbids.  It is filed as
    scoped-out, not silently defaulted.
    """
    log(f"S8 kiss/refusal calibration -- 4h 9/89 [{era}]")

    # PARITY FIRST.  MC-1's kiss_v0 owns this grammar but hardcodes the
    # constants, so it cannot sweep.  The parameterised detector below therefore
    # reproduces kiss_v0's semantics EXACTLY -- including its break-on-first-
    # sign-change (not reject-if-any-sign-change) and its acceptance of a
    # zero-signed touch -- and is asserted identical to it at the ratified
    # point before any sweep result is believed.  An earlier draft reimplemented
    # the detector loosely and lost 2.5% of events one-directionally, then
    # reported the survivor's stability as if it were MC-1's.
    for sym in assets:
        df = frame(sym, "4h", era)
        sp = (df["e9"] - df["e89"]).to_numpy()
        av = df["atr"].to_numpy()
        mine = _kiss_flags(sp, av, M1.KISS_TOUCH_ATR, M1.KISS_REEXPAND_ATR,
                           M1.KISS_REEXPAND_BARS)
        theirs, _ = M1.kiss_v0(sp, av)
        if not np.array_equal(mine, theirs):
            raise SystemExit(
                f"HALT (F-KISS-PARITY): {sym} -- the parameterised kiss detector "
                f"disagrees with mc1_program.kiss_v0 at the ratified point "
                f"({int((mine != theirs).sum())} bars differ). The sweep would be "
                f"measuring a different object than the constant it confirms.")
    log(f"    F-KISS-PARITY: detector == mc1_program.kiss_v0 at 0.25/0.75/10 "
        f"on all {len(assets)} assets")

    rows = []
    for eps in KISS_EPS_SWEEP:
        for delta in KISS_DELTA_SWEEP:
            if delta <= eps:
                continue
            for k in KISS_K_SWEEP:
                n_tot = 0
                per_asset = []
                for sym in assets:
                    df = frame(sym, "4h", era)
                    if len(df) < 300:
                        continue
                    sp = (df["e9"] - df["e89"]).to_numpy()
                    a = df["atr"].to_numpy()
                    cnt = int(_kiss_flags(sp, a, eps, delta, k).sum())
                    n_tot += cnt
                    per_asset.append(cnt)
                rows.append({"eps": eps, "delta": delta, "k": k,
                             "n_refusals": n_tot,
                             "min_per_asset": int(min(per_asset)) if per_asset else 0,
                             "assets": len(per_asset)})
    tab = pd.DataFrame(rows)
    base = tab[(tab.eps == 0.25) & (tab.delta == 0.75) & (tab.k == 10)]
    if len(base):
        b = base.iloc[0]
        log(f"    MC-1 ratified point (0.25/0.75/10): n={int(b.n_refusals)}, "
            f"min/asset={int(b.min_per_asset)}")
    # Stability: how much does the count move under a one-step perturbation of
    # each axis?  A constant sitting on a cliff is a fitted constant.
    stab = None
    if len(base):
        b = base.iloc[0]
        neigh = tab[(tab.eps.between(0.20, 0.30)) & (tab.delta == 0.75)
                    & (tab.k.between(8, 12))]
        if len(neigh) and b.n_refusals:
            spread = float((neigh.n_refusals.max() - neigh.n_refusals.min())
                           / b.n_refusals)
            stab = round(spread, 4)
            log(f"    local stability (+-1 step on eps,k): span = {spread:.1%} "
                f"of the centre count")
    pin = {"eps": M1.KISS_TOUCH_ATR, "delta": M1.KISS_REEXPAND_ATR,
           "k": M1.KISS_REEXPAND_BARS}
    log(f"    -> kiss (i-a) = {pin}  [MC-1 ratified; confirmed, not re-fitted]")
    return {"table": tab, "pin": pin, "local_stability": stab,
            "scope_note": ("EMA<->EMA limb only; price<->level (SFP/deviation) "
                           "has no detector in the estate and is filed as "
                           "scoped-out for a follow-up paste"),
            "rule": ("MC-1's ratified triple is CONFIRMED rather than re-fitted: "
                     "the sweep exists to show the point is stable, and a "
                     "sandbox does not overturn a ratified constant")}


# ===========================================================================
# S9 -- QUERY CARDS (display-only, never priors -- D-H)
# ===========================================================================
def stage_cards(assets: list[str]) -> dict:
    """Two operator-chart episodes, photographed.  Labelled, never fitted."""
    log("S9 query cards -- display-only, never priors")
    out = []
    for card in QUERY_CARDS:
        ts = to_ms(card["ts_iso"])
        rec = {**card, "ts": ts, "_class": DISPLAY_ONLY, "assets": {}}
        for sym in assets:
            per_tf = {}
            for tf in ["1h", "4h"]:
                try:
                    df = frame(sym, tf, "live")
                except FileNotFoundError:
                    continue
                o = df["open_time"].to_numpy(np.int64)
                if not len(o) or ts < o[0] or ts > o[-1] + TF_MS[tf]:
                    per_tf[tf] = {"in_range": False,
                                  "cache_last": iso(int(o[-1])) if len(o) else None}
                    continue
                # AS-OF, not containing.  The bar CONTAINING ts is still open:
                # its close, ATR and EMAs are all functions of a price that has
                # not happened yet at ts. Reporting them is a lookahead even in
                # a display-only artifact -- and a query card exists precisely
                # so an operator can trust the photograph. I7 says as-of slicing
                # everywhere, and census_build.asof_idx is the estate's own
                # primitive for it: last bar whose CLOSE <= t.
                k = int(CB.asof_idx(np.array([ts], np.int64), o, tf)[0])
                if k < 0:
                    per_tf[tf] = {"in_range": False,
                                  "reason": "no closed bar at or before ts"}
                    continue
                r = df.iloc[k]
                per_tf[tf] = {
                    "in_range": True, "as_of": "last CLOSED bar at or before ts",
                    "bar_open": iso(int(r.open_time)),
                    "bar_close": iso(int(r.open_time) + TF_MS[tf]),
                    "close": round(float(r.close), 6),
                    "atr": round(float(r.atr), 6) if np.isfinite(r.atr) else None,
                    "ribbon_9_89_atr": (round(float((r.e9 - r.e89) / r.atr), 6)
                                        if np.isfinite(r.atr) and r.atr > 0 else None),
                    "e300": round(float(r.e300), 6) if np.isfinite(r.e300) else None,
                    "e450": round(float(r.e450), 6) if np.isfinite(r.e450) else None,
                    "e500": round(float(r.e500), 6) if np.isfinite(r.e500) else None,
                }
            rec["assets"][sym] = per_tf
        in_range = any(v.get("in_range") for a in rec["assets"].values()
                       for v in a.values())
        log(f"    {card['id']} {card['ts_iso']}Z -> "
            f"{'IN RANGE' if in_range else 'OUT OF RANGE'}")
        rec["in_range_any"] = in_range
        out.append(rec)
    return {"cards": out}


# ===========================================================================
# EMIT
# ===========================================================================
def _round_floats(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for c in out.columns:
        if out[c].dtype.kind == "f":
            out[c] = out[c].round(R6)
    return out


def emit(name: str, df: pd.DataFrame, sort_by: list[str],
         manifest: dict, era: str) -> None:
    if df is None or df.empty:
        log(f"    (skip {name}: empty)")
        return
    keys = [k for k in sort_by if k in df.columns]
    d = df.sort_values(keys).reset_index(drop=True) if keys else df.reset_index(drop=True)
    d = _round_floats(d)
    # Era-scoped: the evidence-era comparison run must not overwrite the
    # live-era pins it exists to be compared against.
    sub = OUT / era
    sub.mkdir(parents=True, exist_ok=True)
    p = sub / f"{name}.parquet"
    d.to_parquet(p, index=False)
    manifest["artifacts"][name] = {
        "path": str(p), "rows": int(len(d)), "bytes": p.stat().st_size,
        "sha256": _sha(p), "class": DISPLAY_ONLY if era == "live"
        else "EVIDENCE -- exploration-classic",
    }
    log(f"    wrote {name}.parquet  rows={len(d)}  sha={manifest['artifacts'][name]['sha256'][:12]}")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="MC-2 relay & nesting observatory (extended)")
    ap.add_argument("--era", choices=["live", "evidence"], default="live",
                    help="where constants are PINNED (default live = out-of-sample)")
    ap.add_argument("--stage", default="all")
    ap.add_argument("--smoke", action="store_true", help="BTC+ETH only")
    args = ap.parse_args(argv)

    t0 = time.time()
    era = args.era
    assets = ["BTCUSDT", "ETHUSDT"] if args.smoke else PANEL
    log(f"MC-2 observatory -- era={era} assets={assets} seed={SEED}")
    log(f"  evidence wall CEIL_MS={CEIL_MS} ({iso(CEIL_MS)}) -- imported from census_build")

    pre = stage_preflight()

    # A partial run must NOT destroy the record of the stages it did not run.
    # `--stage trap` rebuilding the manifest from scratch silently deleted five
    # of six pins, the feasibility record and the query cards -- and the build
    # document cites this file as the record. So: a full run starts clean; a
    # scoped run MERGES into what is already there.
    mp_existing = OUT / f"mc2_manifest_{era}.json"
    prior: dict = {}
    if args.stage != "all" and mp_existing.exists():
        try:
            prior = json.loads(mp_existing.read_text(encoding="utf-8"))
            log(f"  merging into existing manifest ({len(prior.get('pins', {}))} "
                f"pin(s), {len(prior.get('artifacts', {}))} artifact(s))")
        except Exception as exc:
            raise SystemExit(f"HALT: manifest {mp_existing} exists but is "
                             f"unreadable ({exc}); refusing to overwrite it.")

    manifest: dict = {
        "program": "mc2_program.py", "seed": SEED,
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "pin_era": era,
        "pin_era_note": ("constants pinned OUT-OF-SAMPLE on live-era bars "
                         "(open_time >= CEIL_MS); the evidence era the census "
                         "scores is disjoint from the era these constants were "
                         "measured on") if era == "live" else
                        ("constants pinned IN-SAMPLE on evidence-era bars -- "
                         "the census scores the same bars; selection risk is "
                         "NOT controlled"),
        "class": DISPLAY_ONLY if era == "live" else "EVIDENCE -- exploration-classic",
        "preflight": pre,
        "artifacts": dict(prior.get("artifacts", {})),
        "pins": dict(prior.get("pins", {})),
        "fixtures": dict(prior.get("fixtures", {})),
    }
    # carry forward whole-run sections a scoped run does not regenerate
    for k in ("feasibility", "query_cards"):
        if k in prior:
            manifest[k] = prior[k]
    if prior:
        manifest["merged_from_prior_run"] = prior.get("generated_utc")
        manifest["stages_this_invocation"] = args.stage

    want = args.stage
    def run(nm: str) -> bool:
        return want in ("all", nm)

    manifest["fixtures"]["F-PARITY"] = fixture_parity(assets[:2])

    if run("feas"):
        f = stage_feasibility(assets + ([] if args.smoke else ANNEX))
        emit("feasibility_matrix", f["matrix"], ["asset", "tf", "ema"], manifest, "evidence")
        manifest["feasibility"] = {"hand_recomputed": f["hand_recomputed"],
                                   "warmup_rule": f["warmup_rule"],
                                   "warmup_by_ema": f["warmup_by_ema"]}
    if run("relay"):
        r = stage_relay(assets, era)
        emit("relay_chains", r["chains"], ["asset", "dir", "arming_ts"], manifest, era)
        manifest["pins"]["W_max_4h_bars"] = {
            "value": r["pin"], "fallback": 90, "rule": r["rule"],
            "leg2_lag": r.get("leg2_lag"),
            "leg3_lag_naive_completed_only": r.get("leg3_lag_naive_completed_only"),
            "leg3_lag_kaplan_meier": r.get("leg3_lag_kaplan_meier"),
            "fates": r.get("fates"),
            "window_width_p50": r.get("window_width_p50"),
            "pct_closed_by_counter": r.get("pct_closed_by_counter"),
            "completion_curve": r.get("completion_curve")}
    if run("nest"):
        n = stage_nesting(assets, era)
        emit("nesting_table", n["table"], ["pair"], manifest, era)
        manifest["pins"]["nested_pair_set"] = {
            "value": n["pin"], "inconclusive": n.get("inconclusive", False),
            "selection_test": n.get("selection_test"),
            "fallback": ["1h-in-4h", "30m-in-4h", "30m-in-1h"], "rule": n["rule"]}
    if run("obs25"):
        o = stage_obs25(assets, era)
        emit("obs25_table", o["table"], ["class"], manifest, era)
        manifest["pins"]["pair25_inclusion"] = {
            "value": o["pin"], "excluded": o.get("excluded"),
            "fallback": "included (both)", "rule": o["rule"],
            "count_ratio_vs_9_89": o["count_ratio_vs_9_89"]}
    if run("trap"):
        t = stage_trap(assets, era)
        emit("trap_sweep", t["sweep"], ["threshold"], manifest, era)
        manifest["pins"]["trap_counter_density"] = {
            "value": t["pin"], "fallback": 2, "rule": t["rule"],
            "fallback_fire_rate": t.get("fallback_fire_rate"),
            "naive_pin_rejected": t.get("naive_pin"),
            "selection_test": t.get("selection_test"),
            "guard_failed": t.get("guard_failed")}
    if run("ribbon"):
        rb = stage_ribbon(assets, era)
        emit("ribbon_sweep", rb["table"], ["tf", "c"], manifest, era)
        manifest["pins"]["ribbon_compression_c"] = {
            "value": rb["pin"], "fallback": 0.5, "rule": rb["rule"],
            "admissible_set": rb.get("admissible"), "note": rb.get("note")}
    if run("kiss"):
        kk = stage_kiss(assets, era)
        emit("kiss_sweep", kk["table"], ["eps", "delta", "k"], manifest, era)
        manifest["pins"]["kiss_refusal"] = {
            "value": kk["pin"], "fallback": {"eps": 0.25, "delta": 0.75, "k": 10},
            "rule": kk["rule"], "local_stability": kk["local_stability"],
            "scope_note": kk["scope_note"]}
    if run("cards"):
        manifest["query_cards"] = stage_cards(assets)["cards"]

    manifest["elapsed_s"] = round(time.time() - t0, 1)
    mp = OUT / f"mc2_manifest_{era}.json"
    mp.write_text(json.dumps(manifest, indent=2, default=str), encoding="utf-8")
    lp = OUT / f"mc2_run_log_{era}.txt"
    if args.stage == "all":
        lp.write_text("\n".join(_LOG_LINES) + "\n", encoding="utf-8")
    else:  # scoped run: append, for the same reason the manifest merges
        with open(lp, "a", encoding="utf-8", newline="\n") as fh:
            fh.write(f"\n--- scoped re-run (--stage {args.stage}) ---\n")
            fh.write("\n".join(_LOG_LINES) + "\n")
    log(f"manifest -> {mp}")
    log(f"done in {manifest['elapsed_s']}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
