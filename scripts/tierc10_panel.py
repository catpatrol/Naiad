#!/usr/bin/env python
"""TIER-C10 · THE N-ASSET PANEL MACHINERY.

RATIFIED operator 2026-09-21 (contract TIER-C10 · TWELVE UNSEEN ASSETS + THE
RANGE CENSUS + THREE SETUPS ON TRIAL).  Drafted APOLLO, executed HEPHAESTUS;
seed 20260921.  This module is MACHINERY: it scores nothing by itself and it
files no registration.  What it builds is the set of pieces nine tiers
hard-wired to the five-asset `UNIVERSE`, generalised to a DECLARED panel —
WITHOUT editing a single tierc2..tierc9 file:

  · the panels            CLASSIC5 · UNSEEN12 · PANEL17, as named constants;
  · the admission         >= 316 + 400 closed 4h bars, excluded assets NAMED;
  · corridor_n            one unbroken window over a declared panel, with
                          per-asset floors (warm-up 316);
  · run_cell_n            the book of a panel over `tierc9.replay9` — GATED:
                          any book that is not the known control needs a
                          FILED registration OF THAT BOOK (card class + every
                          field, roles, panel) before one bar is replayed;
  · loao_n                leave-one-asset-out over N assets, direction split,
                          the above-half bar (3/5 -> 7/12), seed threaded;
  · the co-headlines      raw panel + equal-asset-risk, and — NEW HERE, it did
                          not exist in the estate — an asset-cluster bootstrap
                          CI FOR the equal-asset-risk number;
  · the registration gate register() files TEXT **and the BOOK SPEC it is a
                          registration OF** (sha256, monotone sequence,
                          hash-chained registry); score() REFUSES to run
                          unless that file exists, its sha matches AND the
                          offered arm / panel / ruler / lanes / book ARE the
                          filed ones.  The registry lives in a gitignored
                          directory, so its HEAD is printed at every door and
                          pinned by the caller (`head_of_record`) — the
                          witness a wipe cannot take with it.  A pin vouches
                          ONLY for the lines it includes: a head taken before
                          a registration's own line HALTs at both doors;
  · require_arm           the door an EXTERNAL runner (spring, breakeven, BRK
                          — other files) must walk through before it rides;
  · the eras              corridor_era + `arm_spec(..., era=...)`: the window
                          a lane is REGISTERED to ride (R1's tuning/holdout
                          cut), hashed with the text and held against every
                          campaign at the scorer;
  · the as-of warranty    `tierc8.stamp` + lens-aware columns.

THE ONE BOOK THIS MODULE MAY RIDE UNREGISTERED is the known control: card v6
(all knobs at default) on V6_ROLES over a subset of CLASSIC5.  `run()` below
rides exactly that and nothing else.

[LEAN-HEPHAESTUS] the executor leans L1..L8 are carried VERBATIM in `LEANS`
and written as a table on every run; none is applied silently.

Run: NAIAD_CACHE_DIR=~/.cache/naiad/snapshots/tc10_20260921 \\
     ~/venvs/naiad/bin/python scripts/tierc10_panel.py [--rerun]
"""
from __future__ import annotations

import dataclasses
import hashlib
import json
import math
import os
import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import tierc9 as T9                                                  # noqa: E402
import tierc8 as T8                                                  # noqa: E402
import tierc7 as T7                                                  # noqa: E402
import tierc7_rules as RC                                            # noqa: E402
import tierc6 as T6                                                  # noqa: E402
import tierc6_rules as V6                                            # noqa: E402
import tierc5 as T5                                                  # noqa: E402
import tierc2_baseline as TB                                         # noqa: E402

_ms, iso, r4, r6, pct = TB._ms, TB.iso, TB.r4, TB.r6, TB.pct
write_table, assert_key, log = TB.write_table, TB.assert_key, TB.log
cluster_boot, cluster_boot_diff, _ci_from = (T7.cluster_boot,
                                             T7.cluster_boot_diff, T7._ci_from)
agg, d15, journal_frame = T7.agg, T7.d15, T7.journal_frame
agg_both = T6.agg_both
FDR_Q = T7.FDR_Q
MS_4H, MS_1H, MS_1D = TB.MS_4H, TB.MS_1H, TB.MS_1D

# ═══════════════════════════════════════════════════════ THE SEEDS [LEAN L8]
SEED = 20260921                 # the contract's seed — DRIVES every ruler here
SEED_LINEAGE = T5.SEED          # 20260816 — the estate's bootstrap seed TC5..TC9
SEEDS = (SEED, SEED_LINEAGE)    # (ruler, sensitivity)
N_BOOT = 4000

OUT = ROOT / "research_outputs" / "tierc10"
OUT_RERUN = ROOT / "research_outputs" / "tierc10_run2"
PANEL_SUB = "panel"             # this module's own tables live under OUT/panel
REG_DIR = OUT / "registrations"
REGISTRY = "REGISTRY.jsonl"     # hash-chained, append-only, one line per filing
STAGE_D_MANIFEST = OUT / "data" / "STAGE_D_MANIFEST.json"

FAMILY_M = 6                    # the contract: "FDR m=6 independently failable"
LIVE_CACHE = Path.home() / ".cache" / "naiad" / "data_cache"   # READ-NEVER

AS_OF: str = ""                 # set by run(); every table carries it [TC6V-a]
# The LONGEST native funding interval of either venue of record (Binance
# USDT-M and Bybit v5 linear both settle every 8h at most; 4h/2h/1h contracts
# settle MORE often).  A spacing longer than this is not a schedule — it is a
# HOLE, and the accounting would read every stamp inside it as zero cost.
FUNDING_MAX_NATIVE_INTERVAL_H = 8.0

LEANS = {
    "L1": "1d = exactly SIX complete native-4h bars per UTC day (the twin's "
          "law); 1w = seven such complete days, MONDAY-anchored UTC, complete "
          "weeks only. Source = native 4h, never 1h/5m aggregates.",
    "L2": "SCALE_MULT: every registered lane and every Stage-A stamp uses the "
          "FROZEN 3.0 (Pine/twin pin of record). CENSUS-R prints the "
          "self-calibrated SCALE tables WITH the frozen-3.0 tables beside. "
          "Calibrator = grid 1.5..4.0 step 0.25 (Pine minval/step), nearest "
          "confirmed-macro-range density to 0.75 per 100 bars, tie-break "
          "toward 3.0 then lower; the whole grid printed (F-GRID: every grid "
          "whole).",
    "L3": "analytics module = analytics/rangefinder_census.py: a PURE numpy "
          "port (no engine import, no IO, ATR passed IN as an argument), NOT "
          "added to analytics._MODULES (analytics_sha stays put) — printed "
          "as a finding.",
    "L4": "Outcome horizons H20/H100 = BARS OF THE LENS; censor (require "
          "k+H <= n-1), never shorten; anchor = close of the bar the event "
          "is KNOWN (known_at); signs and toll law per map_critic.md §4.6.",
    "L5": "All TC10 fetching lands in the snapshot only; promotion to the "
          "live cache and the LaCie mirror happen at CLOSE (the mirror "
          "command pushes — map_critic §4.2).",
    "L6": "Panels: CLASSIC5 = BTC ETH SOL NEAR ZEC; UNSEEN12 = the contract's "
          "twelve; PANEL17 = CLASSIC5 + admitted UNSEEN12. LOAO "
          "\"above-half\": 3/5 generalises to strict majority ceil((N+1)/2) "
          "→ 7/12.",
    "L7": "FDR: ONE fixed bar q/m = 0.10/6 = 0.016667 per scored row (no "
          "step-up) — that is what makes the six independently failable.",
    "L8": "Rulers seeded 20260921; a sensitivity block re-runs with the "
          "lineage seed 20260816.",
}
LEAN_TAG = "[LEAN-HEPHAESTUS]"
# ONE MORE, RAISED BY THIS MODULE AND PRINTED, NOT ONE OF THE EIGHT: which of
# the two co-headlines carries the VERDICT.  The lineage has scored the RAW
# per-campaign mean for nine tiers and it is the only number with a history;
# the equal-asset-risk CI is new code.  So RAW carries the verdict and the BH
# bar; EAR rides beside it with its own CI and a would-be verdict, and gates
# nothing.  A disagreement between the two is flagged on the row.
LEAN_PANEL_VERDICT = (
    "the SCORED statistic (verdict, p vs the BH bar) is the RAW panel "
    "expectancy — the lineage's ruler since TIER-C5; the equal-asset-risk "
    "co-headline carries its own NEW cluster-bootstrap CI and a would-be "
    "verdict beside it and gates nothing; disagreement is flagged on the row.")


# ═══════════════════════════════════════════ THE SUBSTRATE — FROZEN [LAW 3]
_SUB: dict = {}


def substrate() -> dict:
    """THE CACHE THIS PROCESS READS, PROVEN BEFORE ANY BAR IS READ.

    `tierc2_baseline.KLINES` is bound AT IMPORT from `engine.data.cache_dir()`,
    so exporting NAIAD_CACHE_DIR after python starts changes nothing and says
    nothing.  This guard compares the path the loaders are actually bound to
    with the environment, and refuses the live cache outright.

    WHAT WOULD MAKE THIS WRONG: trusting the env var alone (the binding is
    what reads the bars), or running TC10 against the live cache, which the
    OR-1 lane tops up mid-build — the as-of would move under the tables.
    """
    if _SUB:
        return _SUB
    env = os.environ.get("NAIAD_CACHE_DIR")
    if not env:
        raise SystemExit(
            "HALT: NAIAD_CACHE_DIR is not set. TIER-C10 reads the FROZEN "
            "snapshot only; export it BEFORE python starts (tierc2_baseline "
            "binds its paths at import).")
    root = Path(env).expanduser().resolve()
    if root == LIVE_CACHE.resolve():
        raise SystemExit(
            f"HALT: NAIAD_CACHE_DIR points at the LIVE cache {root} — "
            f"read-never, write-never for TIER-C10 [LAW 3].")
    if (TB.KLINES.resolve() != (root / "klines").resolve()
            or TB.FUNDING.resolve() != (root / "funding").resolve()):
        raise SystemExit(
            f"HALT: the loaders are bound to {TB.KLINES.parent} but "
            f"NAIAD_CACHE_DIR says {root} — the variable was exported AFTER "
            f"the import bound the paths. Nothing may be read.")
    _SUB.update(cache_root=str(root), substrate=root.name)
    return _SUB


# ═══════════════════════════════════════════════════════════ THE PANELS [L6]
CLASSIC5 = RC.UNIVERSE          # BTC ETH SOL NEAR ZEC — the lineage's OBJECT
if CLASSIC5 != ("BTCUSDT", "ETHUSDT", "SOLUSDT", "NEARUSDT", "ZECUSDT"):
    raise SystemExit(f"HALT: the lineage UNIVERSE moved: {CLASSIC5}")

# The contract's twelve, in the contract's order, under the contract's names.
UNSEEN12_CONTRACT = ("ENA", "PUMPFUN", "HYPE", "MNT", "SUI", "LTC", "XMR",
                     "BNB", "UNI", "PEPE", "DOGE", "BONK")

# THE PROVISIONAL SPELLINGS — used ONLY where STAGE D's manifest is absent
# (it is gitignored, so a fresh worktree has none).  They are the cache STEMS
# Stage D resolved on 2026-09-21, written down so that a tree without the
# record still DECLARES the same twelve:
#   · eleven are Binance USDT-M perpetuals (the 1000x contracts for PEPE and
#     BONK are Binance's own; PUMPFUN is `PUMPUSDT`, baseAsset PUMP — Stage D
#     REJECTED the near-match `PUMPBTCUSDT` as a different asset);
#   · MNT has NO Binance USDT-M perp: its ENTIRE tape is Bybit v5 linear,
#     cached under the stem `MNTUSDT_BYBIT` — one venue, never spliced, and
#     never confusable by filename with a Binance series.
# A declaration is not an admission: an asset whose 4h file is missing fails
# admission with 0 bars and is NAMED as excluded — it can never be silently
# dropped or silently run.
UNSEEN12_PROVISIONAL = (
    ("ENA", "ENAUSDT", "BINANCE_USDTM"),
    ("PUMPFUN", "PUMPUSDT", "BINANCE_USDTM (PUMPBTCUSDT rejected)"),
    ("HYPE", "HYPEUSDT", "BINANCE_USDTM"),
    ("MNT", "MNTUSDT_BYBIT", "BYBIT_V5_LINEAR (no Binance perp)"),
    ("SUI", "SUIUSDT", "BINANCE_USDTM"),
    ("LTC", "LTCUSDT", "BINANCE_USDTM"),
    ("XMR", "XMRUSDT", "BINANCE_USDTM"),
    ("BNB", "BNBUSDT", "BINANCE_USDTM"),
    ("UNI", "UNIUSDT", "BINANCE_USDTM"),
    ("PEPE", "1000PEPEUSDT", "BINANCE_USDTM"),
    ("DOGE", "DOGEUSDT", "BINANCE_USDTM"),
    ("BONK", "1000BONKUSDT", "BINANCE_USDTM"),
)
_NAME_KEYS = ("asset", "contract_name", "name", "ticker", "contract")
# THE STEM COMES FIRST.  Stage D keys every cache file on a `stem`, and for an
# alternate-venue asset the stem is NOT the venue's symbol: MNT trades as
# `MNTUSDT` on Bybit and is cached as `MNTUSDT_BYBIT_*` so that a Bybit tape
# can never be mistaken for (or spliced onto) a Binance one.  Reading `symbol`
# first would send every loader to a file that does not exist.
_SYM_KEYS = ("stem", "cache_symbol", "symbol", "venue_symbol")
_ADMIT_KEYS = ("admitted", "admit", "admission")
AS_OF_PIN = OUT / "data" / "AS_OF_PIN.json"


def _first(d: dict, keys: tuple):
    for k in keys:
        if k in d:
            return d[k]
    return None


def resolve_unseen12(manifest_path: Path | None = None) -> dict:
    """THE TWELVE, RESOLVED FROM STAGE D'S MANIFEST WHEN IT EXISTS.

    The shape Stage D files (scripts' own manifest, read 2026-09-21):
        {"complete": true,
         "admission": {"rows": [ {"asset": "MNT", "stem": "MNTUSDT_BYBIT",
                                  "venue": "BYBIT_V5_LINEAR",
                                  "closed_4h_bars": 6513, "admitted": true,
                                  "bars_1d": ..., "bars_1w": ...}, ... ]}}
    A plain `{"assets": [...]}` list (or dict keyed by name) with the same
    row keys is accepted too.  An asset Stage D could not source carries a
    null stem and is reported as unresolved.  `complete: false` HALTs — a
    half-written record resolves nothing.

    WHAT WOULD MAKE THIS WRONG: falling back to the provisional tuple when a
    manifest EXISTS but cannot be read — a panel must never be resolved from a
    guess while the record of what was actually fetched sits beside it.  A
    present-but-unreadable manifest HALTs.
    """
    p = Path(manifest_path) if manifest_path else STAGE_D_MANIFEST
    if not p.exists():
        return {"source": "PROVISIONAL (no STAGE_D_MANIFEST.json yet)",
                "names": UNSEEN12_CONTRACT,
                "symbol_of": {n: s for n, s, _ in UNSEEN12_PROVISIONAL},
                "manifest_admitted": None, "manifest_by_stem": None,
                "note": {n: w for n, _, w in UNSEEN12_PROVISIONAL}}
    try:
        man = json.loads(p.read_text())
        assets = (man["admission"]["rows"] if "admission" in man
                  else man["assets"])
    except Exception as e:                                  # noqa: BLE001
        raise SystemExit(f"HALT: {p} exists but is unreadable as a Stage D "
                         f"manifest ({e!r}). The provisional panel is NOT a "
                         f"fallback for a broken record.")
    if man.get("complete") is False:
        raise SystemExit(f"HALT: {p} says complete=false — Stage D has not "
                         f"finished; the panel is not resolved from a "
                         f"half-written record.")
    rows = ([dict(v, **{"asset": k}) for k, v in assets.items()]
            if isinstance(assets, dict) else list(assets))
    sym_of, adm, note, by_stem = {}, {}, {}, {}
    for r_ in rows:
        n = _first(r_, _NAME_KEYS)
        if n is None:
            continue
        n = str(n).upper()
        s = _first(r_, _SYM_KEYS)
        if s:
            by_stem[str(s)] = dict(r_)
        if s in CLASSIC5:
            continue                        # the five ride the same table
        if n in sym_of:
            raise SystemExit(f"HALT: {p} names {n} twice.")
        sym_of[n] = str(s) if s else None
        a = _first(r_, _ADMIT_KEYS)
        adm[n] = None if a is None else bool(a)
        note[n] = str(r_.get("venue", r_.get("venue_of_record", "")))
    missing = [n for n in UNSEEN12_CONTRACT if n not in sym_of]
    if missing:
        raise SystemExit(f"HALT: {p} does not name {missing} — the contract's "
                         f"twelve must ALL appear, admitted or excluded.")
    clash = [n for n in UNSEEN12_CONTRACT if sym_of[n] in CLASSIC5]
    if clash:
        raise SystemExit(f"HALT: {p} maps {clash} onto a CLASSIC5 symbol.")
    return {"source": f"STAGE_D_MANIFEST ({p.name})",
            "names": UNSEEN12_CONTRACT,
            "symbol_of": {n: sym_of[n] for n in UNSEEN12_CONTRACT},
            "manifest_admitted": {n: adm[n] for n in UNSEEN12_CONTRACT},
            "manifest_by_stem": by_stem,
            "note": {n: note[n] for n in UNSEEN12_CONTRACT}}


_U12 = resolve_unseen12()
UNSEEN12_SOURCE = _U12["source"]
UNSEEN12_NAME_OF = {s: n for n, s in _U12["symbol_of"].items() if s}
UNSEEN12_UNRESOLVED = tuple(n for n in UNSEEN12_CONTRACT
                            if not _U12["symbol_of"][n])
# UNSEEN12 = the resolved cache symbols of the contract's twelve, contract order.
UNSEEN12 = tuple(_U12["symbol_of"][n] for n in UNSEEN12_CONTRACT
                 if _U12["symbol_of"][n])
if len(set(UNSEEN12)) != len(UNSEEN12):
    raise SystemExit(f"HALT: UNSEEN12 has a duplicate symbol: {UNSEEN12}")
# PANEL17 = CLASSIC5 + the twelve AS DECLARED.  With a Stage D manifest it is
# CLASSIC5 + the manifest's admitted; before one it is CLASSIC5 + all resolved
# spellings, ADMISSION PENDING.  Either way `corridor_n` re-measures admission
# from the bars and HALTs on an unadmitted member — the constant is a
# declaration, never the proof.  Use `panel17()` for the measured panel.
PANEL17 = CLASSIC5 + tuple(
    _U12["symbol_of"][n] for n in UNSEEN12_CONTRACT
    if _U12["symbol_of"][n]
    and (_U12["manifest_admitted"] is None
         or _U12["manifest_admitted"][n] is not False))


def panel_name(panel) -> str:
    p = tuple(panel)
    if p == CLASSIC5:
        return "CLASSIC5"
    if p == UNSEEN12:
        return "UNSEEN12"
    if p == PANEL17:
        return "PANEL17"
    h = hashlib.sha256(",".join(p).encode()).hexdigest()[:8]
    return f"CUSTOM{len(p)}:{h}"


# ═══════════════════════════════════════════ THE ADMISSION — contract STAGE D
WARMUP_BARS = RC.WARMUP_BARS            # 316 — the card's own floor, by OBJECT
ADMIT_MIN_SCORED_BARS = 400
ADMIT_MIN_BARS = WARMUP_BARS + ADMIT_MIN_SCORED_BARS     # 716, derived
MONDAY_EPOCH_OFFSET_MS = 4 * MS_1D      # 1970-01-05 was a Monday [L1]

_OPEN: dict[str, np.ndarray | None] = {}


def open_ms_4h(sym: str) -> np.ndarray | None:
    """Bar OPEN stamps of one asset's native 4h file, or None when the
    snapshot holds no such file.  Timestamps only — no price is read, so this
    is safe on an unseen asset before any registration is filed."""
    substrate()
    if sym not in _OPEN:
        p = TB.KLINES / f"{sym}_4h.parquet"
        _OPEN[sym] = (np.sort(pd.read_parquet(p, columns=["open_time"])
                              ["open_time"].to_numpy(np.int64))
                      if p.exists() else None)
    return _OPEN[sym]


def _complete_days(om: np.ndarray) -> np.ndarray:
    """UTC day opens holding EXACTLY six native-4h bars [L1]."""
    day = om // MS_1D * MS_1D
    u, c = np.unique(day, return_counts=True)
    return u[c == 6]


def _complete_weeks(om: np.ndarray) -> int:
    """MONDAY-anchored UTC weeks made of SEVEN complete days [L1]."""
    d = _complete_days(om)
    wk = (d - MONDAY_EPOCH_OFFSET_MS) // (7 * MS_1D)
    _, c = np.unique(wk, return_counts=True)
    return int(np.sum(c == 7))


def admission(symbols) -> pd.DataFrame:
    """THE ADMISSION TABLE — one row per DECLARED asset, excluded ones NAMED
    WITH THEIR COUNTS (the contract's words).

    The rule is `n_closed_4h >= 316 + 400`: the card may not arm before bar 316
    of an asset's own history, and an asset must then offer at least 400 bars
    the card can actually be scored on.  Every cached 4h row is treated as a
    CLOSED bar — the estate's writer clamps to the last closed bar
    (engine/data.py) and a frozen snapshot cannot be re-checked against the
    wall clock; that basis rides on the row.

    WHAT WOULD MAKE THIS WRONG: counting the warm-up as scorable history, or
    dropping a failing asset from the table instead of naming it.
    """
    rows = []
    rec = _U12["manifest_by_stem"] or {}
    for s in symbols:
        om = open_ms_4h(s)
        n = 0 if om is None else int(len(om))
        dif = np.diff(om) if n > 1 else np.zeros(0, np.int64)
        ok = n >= ADMIT_MIN_BARS
        mr = rec.get(s, {})
        m4 = mr.get("closed_4h_bars")
        rows.append({
            "symbol": s,
            "venue_of_record": mr.get("venue", "" if rec else
                                      "UNPRINTED (no Stage D manifest yet)"),
            "stage_d_closed_4h_bars": m4,
            "stage_d_bars_1d": mr.get("bars_1d"),
            "stage_d_bars_1w": mr.get("bars_1w"),
            "stage_d_admitted": mr.get("admitted"),
            "agrees_with_stage_d": (None if m4 is None else bool(
                int(m4) == n and bool(mr.get("admitted")) == bool(ok))),
            "contract_name": UNSEEN12_NAME_OF.get(s, s.replace("USDT", "")),
            "panel_class": "CLASSIC5" if s in CLASSIC5 else "UNSEEN12",
            "n_closed_4h": n,
            "first_4h": iso(int(om[0])) if n else None,
            "last_4h_open": iso(int(om[-1])) if n else None,
            "n_gaps_4h": int(np.sum(dif != MS_4H)),
            "n_offgrid_4h": int(np.sum(om % MS_4H != 0)) if n else 0,
            "warmup_bars": WARMUP_BARS,
            "min_scored_bars": ADMIT_MIN_SCORED_BARS,
            "need_bars": ADMIT_MIN_BARS,
            "scorable_bars": max(n - WARMUP_BARS, 0),
            "n_complete_1d": int(len(_complete_days(om))) if n else 0,
            "n_complete_1w": _complete_weeks(om) if n else 0,
            "admitted": bool(ok),
            "excluded_because": (
                "" if ok else
                "no 4h kline file in the snapshot (0 bars)" if om is None else
                f"{n} closed 4h bars < {ADMIT_MIN_BARS} "
                f"(= {WARMUP_BARS} warm-up + {ADMIT_MIN_SCORED_BARS})"),
            "closed_bar_basis": "every cached row is a closed bar (the "
                                "writer clamps; a frozen snapshot cannot be "
                                "re-checked against the wall clock)",
            "derived_lens_law": f"{LEAN_TAG} L1: " + LEANS["L1"],
        })
    return pd.DataFrame(rows)


def admitted(symbols) -> tuple:
    a = admission(symbols)
    return tuple(a.loc[a["admitted"], "symbol"])


def panel17() -> tuple:
    """CLASSIC5 + the ADMITTED twelve, MEASURED from the snapshot's bars —
    and cross-checked against Stage D's own admitted flags when it filed any.
    A disagreement between the record and the bars HALTs."""
    adm = admission(CLASSIC5 + UNSEEN12)
    got = tuple(adm.loc[adm["admitted"] & adm["symbol"].isin(UNSEEN12),
                        "symbol"])
    off = adm[adm["agrees_with_stage_d"].eq(False)]
    if len(off):
        raise SystemExit(
            "HALT: Stage D's record and the snapshot's bars DISAGREE — "
            + "; ".join(f"{r_.symbol}: manifest {r_.stage_d_closed_4h_bars} "
                        f"bars/admitted={r_.stage_d_admitted}, snapshot "
                        f"{r_.n_closed_4h}/admitted={r_.admitted}"
                        for r_ in off.itertuples())
            + ". Neither is used until they agree.")
    rec = _U12["manifest_admitted"]
    if rec is not None:
        want = tuple(_U12["symbol_of"][n] for n in UNSEEN12_CONTRACT
                     if _U12["symbol_of"][n] and rec[n])
        if set(want) != set(got):
            raise SystemExit(
                f"HALT: Stage D's manifest admits {sorted(want)} but the "
                f"snapshot's bars admit {sorted(got)} — the record and the "
                f"data disagree; neither is used.")
    return CLASSIC5 + got


# ══════════════════════════════════════════════ FUNDING — NEVER THE SILENT {}
def funding_coverage(sym: str) -> dict:
    """What the snapshot holds for one asset's funding — presence, span, grid.

    `tierc2_baseline.load_funding` returns `{}` when the file is missing, and
    the accounting reads a missing stamp as ZERO cost.  On the five classics
    that hole never opened; on a twelve-asset panel it would make every new
    asset's book silently funding-free."""
    substrate()
    p = TB.FUNDING / f"{sym}.parquet"
    om = open_ms_4h(sym)
    edge = int(om[-1]) + MS_4H if om is not None and len(om) else None
    floor = (int(om[WARMUP_BARS]) if om is not None and len(om) > WARMUP_BARS
             else None)
    if not p.exists():
        return {"symbol": sym, "funding_present": False, "n_stamps": 0,
                "first_stamp": None, "last_stamp": None,
                "modal_interval_h": None, "n_off_modal_spacings": None,
                "max_spacing_h_after_floor": None,
                "n_holes_after_floor": None,
                "kline_edge": iso(edge) if edge else None,
                "stale_hours_vs_kline_edge": None,
                "first_scorable_bar": iso(floor) if floor else None,
                "head_gap_hours_vs_first_scorable_bar": None}
    ft = np.sort(pd.read_parquet(p, columns=["funding_time"])
                 ["funding_time"].to_numpy(np.int64)) // MS_1H * MS_1H
    n = int(len(ft))
    dif = np.diff(ft) if n > 1 else np.zeros(0, np.int64)
    if len(dif):
        u, c = np.unique(dif, return_counts=True)
        modal = float(u[int(np.argmax(c))]) / MS_1H
        off = int(np.sum(dif != u[int(np.argmax(c))]))
    else:
        modal, off = None, None
    # INTERIOR HOLES, measured where a book can ride (after the asset's first
    # scorable bar): a spacing longer than the venue's longest native interval.
    ins = (dif[ft[1:] > floor] if floor is not None else dif) / MS_1H
    return {"symbol": sym, "funding_present": True, "n_stamps": n,
            "first_stamp": iso(int(ft[0])) if n else None,
            "last_stamp": iso(int(ft[-1])) if n else None,
            "modal_interval_h": modal, "n_off_modal_spacings": off,
            "max_spacing_h_after_floor": (float(ins.max()) if len(ins)
                                          else None),
            "n_holes_after_floor": int(np.sum(
                ins > FUNDING_MAX_NATIVE_INTERVAL_H)),
            "kline_edge": iso(edge) if edge else None,
            "stale_hours_vs_kline_edge": (
                round((edge - int(ft[-1])) / MS_1H, 2) if (n and edge)
                else None),
            "first_scorable_bar": iso(floor) if floor else None,
            # > 0 means campaigns could be ridden BEFORE the first stamp —
            # the silent zero again, at the head instead of the tail.
            "head_gap_hours_vs_first_scorable_bar": (
                round((int(ft[0]) - floor) / MS_1H, 2) if (n and floor)
                else None)}


def require_funding(panel, strict_edge: bool = True) -> list[dict]:
    """HALT — not print — when a panel asset has no funding [F-D-3's law, held
    at the door of the book].  By default it ALSO HALTs when the stamps do not
    span what the book can ride: the last stamp older than the kline edge by
    more than one funding interval plus one bar (the estate's funding sat
    stale at 2026-08-15 for five weeks and the four newest control campaigns
    rode funding-free until Stage D topped it up), or the first stamp later
    than the asset's first SCORABLE bar, or — the INTERIOR — any spacing
    after that bar longer than the venues' longest native interval (8h): a
    hole in the middle is the same silent zero as a hole at either end.
    `strict_edge=False` is for a coverage REPORT, never for a book.

    WHAT WOULD MAKE THIS WRONG: a panel asset reaching `_account_chain` with an
    empty — or a too-short — funding dict: a zero that looks like a number."""
    out = []
    for s in panel:
        cov = funding_coverage(s)
        if not cov["funding_present"] or cov["n_stamps"] == 0:
            raise SystemExit(
                f"HALT: no funding for panel asset {s} in the snapshot "
                f"({TB.FUNDING / (s + '.parquet')}). load_funding would "
                f"return the silent {{}} and the book would ride funding-"
                f"free. Fetch it (Stage D) or name the asset excluded.")
        if strict_edge:
            lim = (cov["modal_interval_h"] or 8.0) + 4.0
            if (cov["stale_hours_vs_kline_edge"] or 0.0) > lim:
                raise SystemExit(
                    f"HALT: {s} funding ends {cov['last_stamp']}, "
                    f"{cov['stale_hours_vs_kline_edge']}h before the kline "
                    f"edge {cov['kline_edge']} (> one interval + one bar).")
            if (cov["head_gap_hours_vs_first_scorable_bar"] or 0.0) > 0.0:
                raise SystemExit(
                    f"HALT: {s} funding STARTS {cov['first_stamp']}, after "
                    f"its first scorable bar {cov['first_scorable_bar']} — "
                    f"early campaigns would ride funding-free.")
            if (cov["n_holes_after_floor"] or 0) > 0:
                raise SystemExit(
                    f"HALT: {s} funding has {cov['n_holes_after_floor']} "
                    f"INTERIOR hole(s) after its first scorable bar (longest "
                    f"spacing {cov['max_spacing_h_after_floor']}h > the "
                    f"venues' longest native interval "
                    f"{FUNDING_MAX_NATIVE_INTERVAL_H}h) — campaigns riding "
                    f"through it would be charged zero.")
        out.append(cov)
    return out


def frame_n(sym: str) -> dict:
    """`tierc5.frame`, entered through a door.

    The lineage memoises frames (and role arrays, anchor series, fractals) on
    the BARE SYMBOL.  That is safe for any symbol string — nothing in the memo
    is five-asset-specific — PROVIDED every frame under that key is the
    asset's native 4h frame from the frozen substrate, with funding loaded.
    This door proves exactly those three things each time a panel is ridden.

    WHAT WOULD MAKE THIS WRONG: a lens-parameterised frame (5m, 1d) stored
    under the bare-symbol key — it would poison the 4h book of the same asset
    [the F-C8-MATCH lesson].  TC10's other lenses must key on (sym, lens) in
    their OWN memo; this door HALTs if it ever finds a non-4h frame here.
    """
    substrate()
    require_funding((sym,))
    st = T5.frame(sym)
    om = st["f"].open_ms
    ref = open_ms_4h(sym)
    if ref is None or len(om) != len(ref) or int(om[0]) != int(ref[0]) \
            or int(om[-1]) != int(ref[-1]):
        raise SystemExit(f"HALT: the memoised frame for {sym} is not the "
                         f"snapshot's native 4h file (poisoned memo).")
    dif = np.diff(om)
    if len(dif) and (int(dif.min()) != MS_4H or np.any(dif % MS_4H)):
        raise SystemExit(f"HALT: the frame under key {sym!r} is not on the "
                         f"4h grid — a foreign lens was stored under the "
                         f"bare-symbol key.")
    if not st["fund"]:
        raise SystemExit(f"HALT: the memoised frame for {sym} holds an EMPTY "
                         f"funding dict (built before the file landed).")
    return st


# ═══════════════════════════════════════════════════════ THE CORRIDOR, N-ASSET
VOLATILE_META = ("wall_clock_at_run", "cache_lag_hours")


def _iso_ms(s: str) -> int:
    from datetime import datetime, timezone
    return int(datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")
               .replace(tzinfo=timezone.utc).timestamp() * 1000)


def stage_d_pin() -> int | None:
    """Stage D's WRITE-ONCE as-of (close of the last closed 4h bar at its
    first fetch), in ms, or None before Stage D has run."""
    if not AS_OF_PIN.exists():
        return None
    try:
        v = int(json.loads(AS_OF_PIN.read_text())
                ["as_of_last_closed_4h_close_ms"])
    except Exception as e:                                  # noqa: BLE001
        raise SystemExit(f"HALT: {AS_OF_PIN} exists but carries no "
                         f"as_of_last_closed_4h_close_ms ({e!r}).")
    if v % MS_4H:
        raise SystemExit(f"HALT: {AS_OF_PIN} pins {v}, not a 4h bar close.")
    return v


def corridor_n(panel, pin_close_iso: str | None = None,
               floor_bars: int = WARMUP_BARS) -> tuple[int, int, dict]:
    """`tierc5.corridor`, over a DECLARED panel.

    Same law as the parent: panel start = the earliest first bar; panel end =
    the latest 4h bar closed ON EVERY asset (the minimum of the last opens),
    one unbroken window.  New here: PER-ASSET FLOORS — each asset may first
    arm at its own bar `floor_bars` (316), so a 2025 listing joins the panel
    316 bars after ITS first candle, not the panel's — and the contract's
    ADMISSION, enforced: an unadmitted member HALTs.

    On CLASSIC5 this returns exactly `tierc5.corridor()`'s (lo, hi) — asserted
    by F-CTRL, because a control that rides a different window is not one.

    WHAT WOULD MAKE THIS WRONG: taking the panel end as the MAX of the last
    opens (assets would be scored over windows where others have no bars), or
    pinning by day count rather than by bar [tierc6.corridor_pinned's law].
    """
    panel = tuple(panel)
    if not panel or len(set(panel)) != len(panel):
        raise SystemExit(f"HALT: a panel is a non-empty set of DISTINCT "
                         f"symbols; got {panel}")
    adm = admission(panel)
    bad = adm[~adm["admitted"]]
    if len(bad):
        raise SystemExit(
            "HALT: panel holds UNADMITTED assets — "
            + "; ".join(f"{r_.symbol}: {r_.excluded_because}"
                        for r_ in bad.itertuples())
            + ". Name them excluded (admitted(panel)) before riding.")
    oms = {s: open_ms_4h(s) for s in panel}
    lo = min(int(oms[s][0]) for s in panel)
    hi_open = min(int(oms[s][-1]) for s in panel)
    binding = sorted(s for s in panel if int(oms[s][-1]) == hi_open)
    close = hi_open + MS_4H
    sd_pin = stage_d_pin()
    if sd_pin is not None and sd_pin < close:
        # bars stamped AFTER Stage D's write-once as-of are COUNTED by its
        # manifest and never read [its warranty]; the corridor honours that.
        close = sd_pin
    if pin_close_iso is not None:
        pin = _iso_ms(pin_close_iso)
        if pin > close:
            raise SystemExit(f"HALT: corridor pin {pin_close_iso} is AFTER "
                             f"the panel's last closed 4h bar {iso(close)} — "
                             f"a pin may only look back.")
        if pin % MS_4H:
            raise SystemExit(f"HALT: corridor pin {pin_close_iso} is not a "
                             f"4h bar close — pin by BAR, never by day count.")
        close = pin
    now = int(time.time() * 1000)
    hi = close - 1
    meta = {
        "panel_start": iso(lo),
        "last_closed_4h_open": iso(close - MS_4H),
        "last_closed_4h_close": iso(close),
        "wall_clock_at_run": iso(now),
        "cache_lag_hours": round((now - close) / 3_600_000.0, 2),
        "span_days": round((close - lo) / MS_1D, 1),
        "per_asset_first_4h": {s: iso(int(oms[s][0])) for s in panel},
        "per_asset_last_4h_open": {s: iso(int(oms[s][-1])) for s in panel},
        "per_asset_n_4h": {s: int(len(oms[s])) for s in panel},
        "per_asset_floor_4h": {s: iso(int(oms[s][floor_bars]))
                               for s in panel},
        "per_asset_scorable_bars_in_corridor": {
            s: int(max(int(np.searchsorted(oms[s], hi, "right"))
                       - floor_bars, 0)) for s in panel},
        "floor_bars": int(floor_bars),
        "panel": list(panel), "panel_name": panel_name(panel),
        "n_assets": len(panel),
        "binding_edge_assets": binding,
        "admission_rule": f"n_closed_4h >= {WARMUP_BARS} + "
                          f"{ADMIT_MIN_SCORED_BARS} = {ADMIT_MIN_BARS}",
        "substrate": substrate()["substrate"],
        "stage_d_as_of_pin": iso(sd_pin) if sd_pin is not None else None,
        "stage_d_pin_binds": bool(sd_pin is not None
                                  and sd_pin < hi_open + MS_4H),
        "note": "the corridor END is the latest 4h bar closed on EVERY panel "
                "asset in the FROZEN snapshot, never later than Stage D's "
                "write-once as-of pin; no network call is made.",
    }
    if pin_close_iso is not None:
        meta["corridor_pinned_to"] = pin_close_iso
    return lo, hi, meta


# ═══════════════════════════ THE ERAS — THE CORRIDOR, CUT [OPERATOR RULING R1]
# R1, verbatim: the RB3 hold pins are TUNED on "bars with close time <=
# 2024-06-30T23:59:59Z (the estate's 'exploration-classic' era, LEDGER.md:97)"
# and P-BRK-S1 is "SCORED ON THE HOLDOUT ERA ONLY (all 17 assets), so the
# tuned pins and the chosen band are out-of-sample where they are judged".
# A tuned pin judged on the bars that tuned it is not evidence — so the ERA a
# lane is scored on is part of WHAT IS REGISTERED: `arm_spec(..., era=...)`,
# hashed with the text, re-read at both doors, and held against the offered
# window AND against every campaign in the book.  An era the registration does
# not name HALTs at `score()`.
ERA_CUT_ISO = "2024-06-30T23:59:59Z"    # the LAST instant of the tuning era
ERA_CUT_MS = _iso_ms(ERA_CUT_ISO)
ERAS = ("full", "tuning", "holdout")
_ERA_NOTE = {
    "full": "FULL CORRIDOR — every bar the panel's corridor holds.",
    "tuning": f"TUNING ERA [R1] — entries at or before {ERA_CUT_ISO} (the "
              f"estate's exploration-classic era). A pin tuned here is NOT "
              f"out of sample here.",
    "holdout": f"HOLDOUT ERA [R1] — entries AFTER {ERA_CUT_ISO}; the era "
               f"P-BRK-S1 is scored on, where its tuned pins and its chosen "
               f"band are out of sample."}


def era_window(era: str) -> tuple[int | None, int | None]:
    """The INCLUSIVE ms bounds of an era, `None` where it is open.
    tuning = (None, ERA_CUT_MS] · holdout = (ERA_CUT_MS, None) · full = all.
    The bound is the operator's instant, not a bar: a campaign is IN the era
    iff its `entry_ms` falls inside it [R1 "entries after ..."]."""
    if era not in ERAS:
        raise SystemExit(f"HALT: unknown era {era!r}; one of {ERAS} "
                         f"(cut {ERA_CUT_ISO} [R1]).")
    return {"full": (None, None), "tuning": (None, ERA_CUT_MS),
            "holdout": (ERA_CUT_MS + 1, None)}[era]


def in_era(ms, era: str) -> bool:
    """Is this instant inside the era?  One place, so the corridor, the door
    and the scorer cannot drift apart."""
    lo, hi = era_window(era)
    ms = int(ms)
    return not ((lo is not None and ms < lo) or (hi is not None and ms > hi))


def era_note(era: str) -> str:
    era_window(era)                                    # validates, or HALTs
    return _ERA_NOTE[era]


def corridor_era(panel, era: str = "full", pin_close_iso: str | None = None,
                 floor_bars: int = WARMUP_BARS) -> tuple[int, int, dict]:
    """`corridor_n`, CUT TO AN ERA — the window a lane registered for that era
    may ride, on the 4h grid: the start moves up to the first 4h bar OPENING
    at or after the era's first instant, the end down to the last 4h bar
    CLOSING at or before its last.  The as-of stamp is NOT moved: `meta` keeps
    the corridor's own edge (what the frozen snapshot allowed anyone to read)
    and states the era beside it, because a table stamped with the era's end
    would claim the snapshot stopped there.

    WHAT WOULD MAKE THIS WRONG: cutting by DAY rather than by bar (a bar that
    straddles the cut would be ridden in both eras), or moving the as-of stamp
    to the era end (the row would lie about what was readable)."""
    lo, hi, meta = corridor_n(panel, pin_close_iso, floor_bars)
    elo, ehi = era_window(era)
    lo_e = lo if elo is None else max(
        lo, ((int(elo) + MS_4H - 1) // MS_4H) * MS_4H)
    hi_e = hi if ehi is None else min(
        hi, ((int(ehi) + 1) // MS_4H) * MS_4H - 1)
    if lo_e > hi_e:
        raise SystemExit(
            f"HALT: the {era!r} era leaves {panel_name(panel)} no window "
            f"(corridor {iso(lo)} → {iso(hi + 1)}, era cut {ERA_CUT_ISO}).")
    meta = dict(meta, era=era, era_cut=ERA_CUT_ISO, era_note=era_note(era),
                era_window_lo=iso(lo_e), era_window_hi=iso(hi_e + 1),
                era_corridor_lo=iso(lo), era_corridor_hi=iso(hi + 1),
                era_bars_dropped_head=int((lo_e - lo) // MS_4H),
                era_bars_dropped_tail=int((hi - hi_e) // MS_4H))
    return lo_e, hi_e, meta


# ═══════════════════════════════════ THE BOOK OF A PANEL — GATED [LAW 4]
CONTROL_CARD = T8.Card(name="v6-control")
_REPLAY9_AT_IMPORT = T9.replay9     # the REAL replay; a fixture stubs the name
RULERS = ("vs_zero", "two_sample", "set_change")
RUNNERS = ("run_cell_n", "external")
BASES = ("zero", "card-v6")
CONTROL_ARM = "(control)"       # the unfiled control's arm name — RESERVED
# WHICH LOAO COUNT CARRIES THE ABOVE-HALF LINE.  `loao_n` prints two counts
# and they can disagree the moment a DECLARED asset yields no campaign (its
# leave-out panel IS the headline): the lineage's count (N = the declared
# panel, parity with tierc7.loao) and the count excluding such panels.  Which
# one is the line of record is a choice that must be made BEFORE the look —
# so the registration says it, in its text AND in its hashed book spec, or
# neither door opens.
LOAO_LINES = ("lineage", "excl_zero_campaign")
_LOAO_CLAUSE = {
    "lineage": "LOAO LINE OF RECORD: lineage count",
    "excl_zero_campaign": "LOAO LINE OF RECORD: excl-zero-campaign count"}


def loao_line_clause(choice: str) -> str:
    """The literal sentence a registration's TEXT must contain for the LOAO
    count its book spec names (`arm_spec(..., loao_line=choice)`)."""
    if choice not in LOAO_LINES:
        raise SystemExit(f"HALT: unknown LOAO line {choice!r}; one of "
                         f"{LOAO_LINES}")
    return _LOAO_CLAUSE[choice]


class Book(list):
    """A JOURNAL THAT KNOWS WHICH BOOK IT IS.  `run_cell_n` returns one: the
    trades, plus `.spec` — the card's class and EVERY field, the roles' class
    and every field, the panel, the window, and the registration arm that
    opened the gate.  `score()` reads it back: an arm filed for `run_cell_n`
    is scored ONLY on a Book whose spec IS the filed one, and a "vs card v6"
    arm ONLY against a Book that is card v6 on the arm's own panel.

    Provenance does NOT survive a slice, a filter or a `+` — those return a
    plain list, and that is the design: a filtered book is not the book that
    was registered.  It is provenance, not cryptography: building a Book by
    hand is possible, and it is a deliberate act a reviewer can grep for.
    """

    def __init__(self, trades=(), spec: dict | None = None):
        super().__init__(trades)
        self.spec = dict(spec or {})


def _cls(o) -> str:
    return f"{type(o).__module__}.{type(o).__qualname__}"


def _fields_of(o) -> dict:
    """Every dataclass FIELD but the free `name`, as repr.  Read from the
    fields — never from a property, which a subclass can override to lie."""
    return {f.name: repr(getattr(o, f.name))
            for f in dataclasses.fields(o) if f.name != "name"}


def ride_spec(card, roles) -> dict:
    """What `replay9` is handed, as a hashable claim: both classes, and every
    field of both.  ALL fields, not the non-default ones — a default that
    moves under a registration must show."""
    return {"card_class": _cls(card), "card_fields": _fields_of(card),
            "roles_class": _cls(roles), "roles_fields": _fields_of(roles)}


CONTROL_RIDE = ride_spec(CONTROL_CARD, T9.V6_ROLES)


def _check_panel(panel) -> tuple:
    panel = tuple(panel)
    if not panel or len(set(panel)) != len(panel) \
            or not all(isinstance(x, str) and x for x in panel):
        raise SystemExit(f"HALT: a panel is a non-empty set of DISTINCT "
                         f"symbols; got {panel}")
    return panel


def arm_spec(arm: str, panel, ruler: str, scored_in_family: bool = True,
             lanes=("card",), card=None, roles=None,
             base: str | None = None, loao_line: str | None = None,
             era: str | None = None) -> dict:
    """ONE ARM OF A REGISTRATION, AS A STRUCTURED CLAIM — what `register()`
    hashes beside the text and what both doors compare the offered book to.

        arm               its name on the scored row
        scored_in_family  True for THE arm that owns the registration's slot
                          in m (at most one); False for a report-only view
                          (P-GEN-1's 17-asset table, a BRK lane's OTHER anchor)
        panel             the declared symbols, in order
        lanes             the `lane` values its campaigns may carry
        ruler / base      "vs_zero" <-> "zero"; a twin ruler <-> "card-v6"
        runner            "run_cell_n" when `card` and `roles` are given — the
                          arm is then ridden through `run_cell_n` and `ride`
                          (both classes, every field) binds it; "external"
                          for a lane with its own runner (spring, breakeven,
                          BRK), which `score()` binds by panel, lanes, ruler —
                          and whose runner MUST enter through `require_arm`.
        loao_line         WHICH LOAO COUNT CARRIES THE ABOVE-HALF LINE: one of
                          `LOAO_LINES` — "lineage" (N = the declared panel, a
                          silent asset's leave-out panel counts: tierc7.loao's
                          law) or "excl_zero_campaign" (such panels excluded).
                          `register()` REFUSES a filing that does not say, and
                          both doors refuse a record that does not.
        era               WHICH ERA THE ARM RIDES: one of `ERAS` — "full",
                          "tuning" (entries <= the R1 cut) or "holdout"
                          (entries after it, where P-BRK-S1's tuned pins are
                          out of sample).  Mandatory, for the same reason the
                          LOAO line is: an era chosen after the look is a
                          choice of the friendlier sample.
    """
    if not isinstance(arm, str) or not arm.strip():
        raise SystemExit("HALT: an arm needs a name.")
    if arm.strip() == CONTROL_ARM:
        raise SystemExit(f"HALT: the arm name {CONTROL_ARM!r} is RESERVED for "
                         f"the unfiled control; a registered book would wear "
                         f"the control's provenance.")
    if loao_line is not None and loao_line not in LOAO_LINES:
        raise SystemExit(f"HALT: arm {arm!r}: unknown loao_line "
                         f"{loao_line!r}; one of {LOAO_LINES}")
    if era is not None:
        era_window(era)                       # unknown era -> HALT, named
    panel = _check_panel(panel)
    if ruler not in RULERS:
        raise SystemExit(f"HALT: arm {arm!r}: unknown ruler {ruler!r}; one "
                         f"of {RULERS}")
    base = base if base is not None else (
        "zero" if ruler == "vs_zero" else "card-v6")
    if base not in BASES or (ruler == "vs_zero") != (base == "zero"):
        raise SystemExit(f"HALT: arm {arm!r}: ruler {ruler!r} and base "
                         f"{base!r} disagree (vs_zero <-> 'zero'; a twin "
                         f"ruler <-> 'card-v6').")
    if (card is None) != (roles is None):
        raise SystemExit(f"HALT: arm {arm!r}: give BOTH card and roles (an "
                         f"arm ridden by run_cell_n) or NEITHER (external).")
    lanes = sorted({str(x) for x in lanes})
    if not lanes:
        raise SystemExit(f"HALT: arm {arm!r} declares no lane.")
    out = {"arm": arm, "scored_in_family": bool(scored_in_family),
           "panel": list(panel), "panel_name": panel_name(panel),
           "lanes": lanes, "ruler": ruler, "base": base,
           "runner": "run_cell_n" if card is not None else "external"}
    if loao_line is not None:
        out["loao_line"] = loao_line
    if era is not None:
        out["era"] = era
    if card is not None:
        if not (dataclasses.is_dataclass(card)
                and dataclasses.is_dataclass(roles)):
            raise SystemExit(f"HALT: arm {arm!r}: card and roles must be "
                             f"dataclass instances (their FIELDS are the "
                             f"claim).")
        out["ride"] = ride_spec(card, roles)
    return out


_ARM_KEYS = {"arm", "scored_in_family", "panel", "panel_name", "lanes",
             "ruler", "base", "runner"}


def _check_spec(arms, where: str) -> dict:
    """A book spec is a NON-EMPTY list of `arm_spec` dicts: distinct names, at
    most ONE scored arm (each registration owns exactly one slot in m), every
    arm re-validated key by key — a hand-written dict gets no easier door
    than `arm_spec` offers."""
    if not isinstance(arms, (list, tuple)) or not arms:
        raise SystemExit(
            f"HALT: {where} — a registration must say WHICH BOOK it is a "
            f"registration of: arms=[arm_spec(...), ...] is mandatory.")
    out = []
    for a in arms:
        if not isinstance(a, dict) or not _ARM_KEYS <= set(a) \
                or set(a) - _ARM_KEYS - {"ride", "loao_line", "era"}:
            raise SystemExit(f"HALT: {where} — not an arm_spec: {a!r:.120}")
        chk = arm_spec(a["arm"], a["panel"], a["ruler"],
                       a["scored_in_family"], a["lanes"], base=a["base"],
                       loao_line=a.get("loao_line"), era=a.get("era"))
        if a["runner"] not in RUNNERS \
                or (a["runner"] == "run_cell_n") != ("ride" in a):
            raise SystemExit(f"HALT: {where} — arm {a['arm']!r}: runner "
                             f"{a['runner']!r} and `ride` disagree.")
        if "ride" in a:
            r_ = a["ride"]
            if set(r_) != set(CONTROL_RIDE) or not all(
                    isinstance(r_[k], (str, dict)) for k in r_):
                raise SystemExit(f"HALT: {where} — arm {a['arm']!r}: `ride` "
                                 f"is not a ride_spec.")
            chk = dict(chk, runner="run_cell_n", ride=r_)
        if json.dumps(chk, sort_keys=True) != json.dumps(a, sort_keys=True):
            raise SystemExit(f"HALT: {where} — arm {a['arm']!r} does not "
                             f"survive re-validation (edited by hand, or the "
                             f"panel constants moved since it was filed).")
        out.append(chk)
    names = [a["arm"] for a in out]
    if len(set(names)) != len(names):
        raise SystemExit(f"HALT: {where} — arm names repeat: {names}")
    if sum(1 for a in out if a["scored_in_family"]) > 1:
        raise SystemExit(f"HALT: {where} — more than ONE scored arm; each "
                         f"registration owns exactly one slot in m.")
    return {"arms": out}


def _require_loao_line(spec: dict, text: str, where: str) -> str:
    """THE LOAO LINE OF RECORD IS NAMED BEFORE THE LOOK — by the book spec
    (hashed) AND by the text (the claim a reader reads).  Every arm of one
    registration names the SAME count (one text, one law) and the text carries
    that count's literal clause (`loao_line_clause`).  HALTs otherwise.

    WHAT WOULD MAKE THIS WRONG: defaulting the choice (the scorer would then
    pick for the claimant, after the look, whichever count clears), or letting
    the spec say one count while the text a reader sees says the other."""
    said = sorted({str(a.get("loao_line")) for a in spec["arms"]})
    if len(said) != 1 or said[0] not in LOAO_LINES:
        raise SystemExit(
            f"HALT: {where} — the book spec does not say WHICH LOAO COUNT "
            f"carries the above-half line (arms say {said}). Every arm needs "
            f"arm_spec(..., loao_line=<one of {LOAO_LINES}>), the same on "
            f"all arms: a declared asset with no campaign makes the two "
            f"counts disagree, and the choice cannot follow the look.")
    have = [c for c in LOAO_LINES if _LOAO_CLAUSE[c] in (text or "")]
    if have != [said[0]]:
        raise SystemExit(
            f"HALT: {where} — the book spec names the {said[0]!r} LOAO count "
            f"but the TEXT states {have or 'none'}. The text must contain "
            f"the literal clause {_LOAO_CLAUSE[said[0]]!r} and no other "
            f"[loao_line_clause].")
    return said[0]


def _require_era(spec: dict, where: str) -> dict:
    """THE ERA IS NAMED BEFORE THE LOOK [R1].  Every arm says which era it
    rides (`arm_spec(..., era=...)`, hashed with the text); arms of one
    registration MAY differ (a holdout-scored lane beside a full-corridor
    Tier-E view), but an arm that names NO era HALTs — at `register()` when
    the filing is written, and at both doors for anything filed earlier or
    edited since.  Returns {arm: era}.

    WHAT WOULD MAKE THIS WRONG: defaulting the era to "full" (a lane tuned on
    the classic era would then be scored on the bars that tuned it, and the
    row would say nothing about it), or holding the era only in the text,
    where no code can read it."""
    said = {a["arm"]: a.get("era") for a in spec["arms"]}
    bad = sorted(k for k, v in said.items() if v not in ERAS)
    if bad:
        raise SystemExit(
            f"HALT: {where} — arm(s) {bad} name NO era. Every arm needs "
            f"arm_spec(..., era=<one of {ERAS}>): a lane whose pins were "
            f"tuned on the classic era is evidence only on the HOLDOUT era "
            f"(cut {ERA_CUT_ISO} [R1]), and an era chosen after the look is a "
            f"choice of the friendlier sample.")
    return said


def _spec_diff(filed: dict, offered: dict) -> list[str]:
    """The keys on which an offered ride differs from the filed one."""
    out = []
    for k in sorted(set(filed) | set(offered)):
        fv, ov = filed.get(k), offered.get(k)
        if isinstance(fv, dict) and isinstance(ov, dict):
            out += [f"{k}.{j}: filed {fv.get(j)} / offered {ov.get(j)}"
                    for j in sorted(set(fv) | set(ov))
                    if fv.get(j) != ov.get(j)]
        elif fv != ov:
            out.append(f"{k}: filed {fv} / offered {ov}")
    return out


def is_control_book(card, roles, panel) -> bool:
    """True iff this is THE KNOWN CONTROL: card v6 with every knob at its
    default (the name is free), the v6 roles, a non-empty subset of CLASSIC5.
    Both classes are checked EXACTLY and the roles are compared FIELD BY
    FIELD — a subclass overriding `.periods` cannot pass for v6."""
    if type(card) is not T8.Card or type(roles) is not T9.Roles:
        return False
    panel = tuple(panel)
    return bool(panel and ride_spec(card, roles) == CONTROL_RIDE
                and set(panel) <= set(CLASSIC5))


def run_cell_n(card, roles, panel, lo_ms: int, hi_ms: int,
               reg_id: str | None = None, text: str | None = None,
               reg_root: Path | None = None, arm: str | None = None,
               head_of_record=None) -> Book:
    """`tierc9.run_cell9`, over a DECLARED panel — and GATED ON THE BOOK.

    THE GATE.  Exactly one book rides without paperwork: the known control
    (`is_control_book`).  EVERY other book — any unseen asset, any swapped
    trigger, any knob — needs:
      · `reg_id` AND `text`: a registration ALREADY FILED by `register()`,
        verified by sha and by the hash-chained registry;
      · THE FILED BOOK: one of that registration's `run_cell_n` arms must
        carry exactly this card (class + every field), these roles, THIS
        panel.  P-GEN-1's paperwork opens P-GEN-1's book and no other — not
        trigger 9/12 under its id, not a moved knob, not PANEL17 under a
        CLASSIC5 filing;
      · under any registry but the canonical one, a STUBBED replay: real bars
        are replayed only on the word of `REG_DIR`, never of a throwaway
        directory a fixture (or anyone) can file into and delete.
    All of it BEFORE one bar is replayed or one frame built.

    THE WINDOW.  `hi_ms` must be a 4h bar close no later than the panel's own
    corridor end (`corridor_n`: the frozen snapshot's edge under Stage D's
    as-of pin) — the frames hold bars stamped after the pin, and a generous
    `hi_ms` would read them.  And it must lie inside the ERA the filed arm
    names [R1]: a "holdout" arm handed the full corridor HALTs, because the
    bars that tuned a pin cannot also judge it (`corridor_era`).

    WHAT WOULD MAKE THIS WRONG: checking the gate AFTER the replay (the result
    would already exist in memory), checking that SOME registration verifies
    rather than that THIS BOOK's does, or letting a panel asset ride with no
    funding file (the silent `{}`)."""
    panel = _check_panel(panel)
    via, era = CONTROL_ARM, "full"      # the control rides the whole corridor
    if not is_control_book(card, roles, panel):
        if reg_id is None or text is None:
            raise SystemExit(
                f"HALT: run_cell_n refuses — card={card.name!r} "
                f"roles={roles.name!r} panel={panel_name(panel)} is not the "
                f"known control, and reg_id/text were not BOTH given. TEXT "
                f"BEFORE RESULT: file it with register() first.")
        root = Path(reg_root) if reg_root else REG_DIR
        rec = require_registered(reg_id, text, root=root,
                                 head_of_record=head_of_record)
        offered = ride_spec(card, roles)
        cands = [a for a in rec["book_spec"]["arms"]
                 if a["runner"] == "run_cell_n"
                 and (arm is None or a["arm"] == arm)]
        hit = [a for a in cands
               if a["ride"] == offered and tuple(a["panel"]) == panel]
        if not hit:
            why = "; ".join(
                f"arm {a['arm']!r}: " + ", ".join(
                    (_spec_diff(a["ride"], offered)
                     + ([f"panel: filed {a['panel_name']} / offered "
                         f"{panel_name(panel)}"]
                        if tuple(a["panel"]) != panel else []))[:4])
                for a in cands) or "it files no such run_cell_n arm"
            raise SystemExit(
                f"HALT: run_cell_n refuses — registration {reg_id} is NOT a "
                f"registration of this book ({why}). A filed text opens ITS "
                f"OWN book and no other.")
        if root.resolve() != REG_DIR.resolve() \
                and T9.replay9 is _REPLAY9_AT_IMPORT:
            raise SystemExit(
                f"HALT: run_cell_n refuses — {root} is not the canonical "
                f"registry {REG_DIR}; a throwaway registry opens the gate "
                f"onto a STUBBED replay only (fixtures). Real bars need the "
                f"registry of record.")
        via, era = hit[0]["arm"], hit[0]["era"]
        e_lo, e_hi = era_window(era)
        if (e_lo is not None and int(lo_ms) < e_lo) \
                or (e_hi is not None and int(hi_ms) > e_hi):
            raise SystemExit(
                f"HALT: run_cell_n refuses — arm {via!r} is filed for the "
                f"{era!r} era ({era_note(era)}), and the offered window "
                f"[{iso(int(lo_ms))}, {iso(int(hi_ms) + 1)}) leaves it. Ride "
                f"corridor_era(panel, {era!r}).")
    lo_c, hi_c, _ = corridor_n(panel)
    if hi_ms > hi_c or (int(hi_ms) + 1) % MS_4H or lo_ms > hi_ms:
        raise SystemExit(
            f"HALT: run_cell_n window [{iso(int(lo_ms))}, "
            f"{iso(int(hi_ms) + 1)}) — the end must be a 4h bar CLOSE no "
            f"later than the panel's corridor end {iso(hi_c + 1)} (the "
            f"as-of); a later end would read bars stamped after it.")
    for s in panel:
        frame_n(s)                  # substrate · funding · memo safety
    out = Book(spec={"ride": ride_spec(card, roles), "panel": list(panel),
                     "lo_ms": int(lo_ms), "hi_ms": int(hi_ms),
                     "registration": reg_id if via != CONTROL_ARM else None,
                     "arm": via, "era": era})
    for s in panel:
        _, t = T9.replay9(s, card, roles, lo_ms, hi_ms)
        out += t
    return out


# ═══════════════════════════════ E1, N-ASSET · THE ABOVE-HALF LINE [LEAN L6]
def above_half_bar(n_panels: int) -> int:
    """STRICT MAJORITY: ceil((N+1)/2).  3 of 5 · 7 of 12 · 9 of 17.  The only
    reading of "above-half" that reproduces the lineage's 3/5."""
    bar = math.ceil((n_panels + 1) / 2)
    if bar != n_panels // 2 + 1:
        raise SystemExit("HALT: above_half_bar arithmetic")
    return bar


def _loao_summary(per: list, n_panels: int) -> dict:
    n_ex = sum(1 for p in per if p["excludes_zero"])
    n_ab = sum(1 for p in per if p.get("excludes_above"))
    n_be = sum(1 for p in per if p.get("excludes_below"))
    bar = above_half_bar(n_panels)
    out = {"loao_panels": n_panels, "loao_excluding_zero": n_ex,
           "loao_excluding_above": n_ab, "loao_excluding_below": n_be,
           "loao_line": f"{n_ab}/{n_panels} above"
                        + (f", {n_be}/{n_panels} BELOW" if n_be else ""),
           "loao_bar_above_half": bar,
           "loao_clears_above_half": bool(n_ab >= bar),
           "loao_sign_note": (
               f"the above-half line ({bar}/{n_panels}, strict majority "
               f"{LEAN_TAG} L6) is taken on panels excluding zero ABOVE. A "
               f"panel excluding zero BELOW is robust evidence the arm is "
               f"WORSE, and counting it toward robustness would read a "
               f"reliable loss as a reliable gain."),
           "loao_detail": "; ".join(
               f"-{p['dropped']}: [{p['ci_lo']}, {p['ci_hi']}]"
               f"{'*' if p['excludes_zero'] else ''}" for p in per),
           "loao_worst_drop": (min(
               (p for p in per if p["ci_lo"] is not None),
               key=lambda p: p.get("point", 0.0), default={"dropped": None}
           )["dropped"]),
           "_per": per}
    if n_panels == 5:
        # the lineage's key, kept ONLY where it is literally true — on a
        # twelve-asset row a column named 3_of_5 would lie to every consumer.
        out["loao_clears_3_of_5"] = bool(n_ab >= 3)
    return out


def loao_n(new: list, base: list | None, panel, two_sample: bool = False,
           seed: int = SEED, label: str = "", n_boot: int = N_BOOT) -> dict:
    """LEAVE-ONE-ASSET-OUT OVER A DECLARED PANEL [E1 law, generalised].

    `tierc7.loao` loops the five-asset UNIVERSE, takes the literal `>= 3`, and
    has no seed; on a twelve-asset book it would print "x/5" and clear at 3.
    This is the same function with three things made explicit:
      · the PANEL is an argument, and N = len(panel) — a declared asset whose
        leave-out panel cannot be bootstrapped counts AGAINST the line;
      · the bar is `above_half_bar(N)` (strict majority), named before the look;
      · the SEED is threaded.
    Three rulers, THE SAME ONE AS THE HEADLINE [tierc7's law]:
        base is None        -> VS ZERO, one-sample cluster bootstrap of the mean
        two_sample=True     -> cluster_boot_diff on both books minus the asset
        two_sample=False    -> PAIRED deltas on (symbol, lane, entry_ms)
    With panel=CLASSIC5 and seed=20260816 it reproduces `tierc7.loao` key for
    key — asserted by F-LOAO-N.

    WHAT WOULD MAKE THIS WRONG: taking N as the number of panels that HAPPENED
    to bootstrap, counting a BELOW panel toward the line, or scoring the
    panels with a different ruler than the headline.
    """
    panel = tuple(panel)
    stray = sorted(({t.symbol for t in new}
                    | {t.symbol for t in (base or [])}) - set(panel))
    if stray:
        raise SystemExit(f"HALT: loao_n — book holds {stray}, outside the "
                         f"declared panel; such an asset would never be "
                         f"dropped and the line would overstate robustness.")
    mode = ("vs_zero" if base is None
            else "two_sample" if two_sample else "paired")
    bu = ({(t.symbol, t.lane, t.entry_ms): t.net_r for t in base}
          if base is not None else {})

    def _row(drop, n, pt, ci):
        above = bool(ci["lo"] is not None and ci["lo"] > 0)
        below = bool(ci["hi"] is not None and ci["hi"] < 0)
        return {"dropped": drop, "n": n, "point": r6(pt),
                "ci_lo": r6(ci["lo"]), "ci_hi": r6(ci["hi"]),
                "excludes_zero": bool(above or below),
                "excludes_above": above, "excludes_below": below, "note": ""}

    def _few(drop, n):
        return {"dropped": drop, "n": n, "ci_lo": None, "ci_hi": None,
                "excludes_zero": False, "excludes_above": False,
                "excludes_below": False, "note": "too few clusters"}

    per = []
    for drop in sorted(panel):
        av = [t.net_r for t in new if t.symbol != drop]
        ac = [t.symbol for t in new if t.symbol != drop]
        if mode == "vs_zero":
            if len(av) < 2 or len(set(ac)) < 2:
                per.append(_few(drop, len(av)))
                continue
            pt = float(np.mean(av))
            per.append(_row(drop, len(av), pt, _ci_from(
                cluster_boot(av, ac, seed=seed, n_boot=n_boot), pt)))
        elif mode == "two_sample":
            bv = [t.net_r for t in base if t.symbol != drop]
            bc = [t.symbol for t in base if t.symbol != drop]
            if len(av) < 2 or len(bv) < 2 or len(set(ac)) < 2:
                per.append(_few(drop, len(av)))
                continue
            pt = float(np.mean(av)) - float(np.mean(bv))
            per.append(_row(drop, len(av), pt, _ci_from(
                cluster_boot_diff(av, ac, bv, bc, seed=seed, n_boot=n_boot),
                pt)))
        else:
            pv, pc = [], []
            for t in new:
                k = (t.symbol, t.lane, t.entry_ms)
                if t.symbol != drop and k in bu:
                    pv.append(t.net_r - bu[k])
                    pc.append(t.symbol)
            if len(pv) < 2 or len(set(pc)) < 2:
                per.append(_few(drop, len(pv)))
                continue
            pt = float(np.mean(pv))
            per.append(_row(drop, len(pv), pt, _ci_from(
                cluster_boot(pv, pc, seed=seed, n_boot=n_boot), pt)))
    out = _loao_summary(per, len(panel))
    # A DECLARED ASSET WITH NO CAMPAIGN leaves the book unchanged when it is
    # dropped: its leave-out panel IS the headline and carries no independent
    # evidence.  The lineage's line counts it (N = the DECLARED panel, parity
    # with tierc7.loao); the count WITHOUT such panels rides beside it.
    zero = sorted(set(panel) - {t.symbol for t in new})
    n_ab_x = sum(1 for p in per
                 if p.get("excludes_above") and p["dropped"] not in zero)
    out.update(loao_mode=mode, loao_seed=int(seed), loao_label=label,
               loao_panel_name=panel_name(panel),
               loao_assets_present=len(panel) - len(zero),
               loao_zero_campaign_assets=",".join(zero),
               loao_above_excl_zero_campaign_panels=int(n_ab_x),
               loao_clears_excl_zero_campaign_panels=bool(
                   n_ab_x >= out["loao_bar_above_half"]),
               loao_zero_campaign_note=(
                   "dropping an asset with no campaign reproduces the "
                   "headline; such a panel is counted by the line (N = the "
                   "DECLARED panel, the lineage's law) and EXCLUDED from "
                   "loao_above_excl_zero_campaign_panels — both printed; "
                   "where they disagree the row says so here."
                   + (" THEY DISAGREE ON THIS ROW." if bool(
                       n_ab_x >= out["loao_bar_above_half"])
                      != out["loao_clears_above_half"] else "")))
    return out


# ═════════════════ THE EQUAL-ASSET-RISK CI — NEW IN TIER-C10, SAID OUT LOUD
EAR_CI_IS_NEW = (
    "NEW IN TIER-C10: the estate had equal-asset-risk only as a display "
    "aggregation (tierc6.agg_ear); no CI on it existed. This is the SAME "
    "asset-cluster bootstrap as the raw ruler — same seed, same asset draws "
    "— with the statistic re-weighted PER DRAW so every drawn asset carries "
    "equal risk.")


def ear_expectancy(values, clusters) -> float | None:
    """The equal-asset-risk expectancy = the MEAN OF PER-ASSET MEANS over the
    assets PRESENT (tierc6.ear_weights' law: K = assets present, w = (N/K)/n_a,
    sum(w r)/N)."""
    v, c = np.asarray(values, float), np.asarray(clusters)
    if not len(v):
        return None
    return float(np.mean([float(np.mean(v[c == u])) for u in np.unique(c)]))


def cluster_boot_ear(values, clusters, seed: int = SEED,
                     n_boot: int = N_BOOT) -> np.ndarray:
    """Asset-cluster bootstrap draws of the EQUAL-ASSET-RISK expectancy.

    THE DESIGN.  Draw K assets with replacement — the identical
    `rng.choice(uniq, K)` stream `tierc5.cluster_boot` consumes, so under one
    seed the raw and the equal-risk intervals are computed on THE SAME asset
    draws and differ only by the weighting.  Then recompute the EAR weights ON
    THE DRAW: each drawn SLOT is its own cluster, w = (N_draw/K) / n_slot, and
    the draw's statistic is sum(w r)/N_draw — which is the mean over the K
    slots of the slot's per-asset mean.  That closed form is what is computed.

    WHAT WOULD MAKE THIS WRONG: recomputing the weights on SYMBOL LABELS.  An
    asset drawn twice would then be collapsed into one cluster with half
    weight per trade, the draw would hold fewer than K clusters, and the
    interval would come out too NARROW — the bootstrap distribution of a
    different statistic.  F-EAR-BOOT plants exactly that and must go RED.
    """
    v, c = np.asarray(values, float), np.asarray(clusters)
    uniq = np.unique(c)
    m = np.array([float(np.mean(v[c == u])) for u in uniq])
    rng = np.random.default_rng(seed)
    out = np.empty(n_boot)
    lut = {u: i for i, u in enumerate(uniq)}
    for b in range(n_boot):
        pick = rng.choice(uniq, size=len(uniq), replace=True)
        out[b] = (float(np.mean(m[[lut[u] for u in pick]])) if len(pick)
                  else np.nan)
    return out


def cluster_boot_ear_diff(va, ca, vb, cb, seed: int = SEED,
                          n_boot: int = N_BOOT) -> np.ndarray:
    """Two-sample twin: EAR(A) − EAR(B) with THE SAME asset draw into both
    books (`tierc5.cluster_boot_diff`'s stream).  K is counted PER BOOK over
    the drawn slots whose asset is PRESENT in that book — tierc6's law that
    the denominator is the assets present, never the universe."""
    va, vb = np.asarray(va, float), np.asarray(vb, float)
    ca, cb = np.asarray(ca), np.asarray(cb)
    uniq = np.unique(np.concatenate([ca, cb]))
    ma = {u: (float(np.mean(va[ca == u])) if np.any(ca == u) else None)
          for u in uniq}
    mb = {u: (float(np.mean(vb[cb == u])) if np.any(cb == u) else None)
          for u in uniq}
    rng = np.random.default_rng(seed)
    out = np.empty(n_boot)
    for b in range(n_boot):
        pick = rng.choice(uniq, size=len(uniq), replace=True)
        xa = [ma[u] for u in pick if ma[u] is not None]
        xb = [mb[u] for u in pick if mb[u] is not None]
        out[b] = ((float(np.mean(xa)) if xa else np.nan)
                  - (float(np.mean(xb)) if xb else np.nan))
    return out


def _verdict(ci: dict) -> str:
    """THE LINEAGE'S VERDICT LAW, reproduced — not re-invented [tierc8.score:
    `good = bool(ci["lo"] is not None and ci["lo"] > 0)`; tierc5/7/9 the same]:

        SUPPORTED  iff  the 90% percentile CI's LOWER bound is STRICTLY > 0.

    A bound of exactly 0.0, a missing bound (no finite draw), a straddling
    interval and an interval wholly below zero are all NOT SUPPORTED.  The
    verdict reads NOTHING but `ci["lo"]`: not the point, not the upper bound,
    not p.  The BH bar is a SEPARATE column in the lineage and here
    (`finish_family`: clears_bh_bar = p_one_sided <= q/m); the two are
    reported side by side and neither is folded into the other.

    WHAT WOULD MAKE THIS WRONG: reading the point estimate (a +0.17 R arm
    whose interval straddles zero would pass), `>=` (a degenerate [0, 0]
    interval — tierc5's union-arm arithmetic — would pass), or folding p into
    the verdict (no tier ever did; the rows would stop being comparable)."""
    return ("SUPPORTED" if (ci["lo"] is not None and ci["lo"] > 0)
            else "NOT SUPPORTED")


def co_headline(book: list, seed: int = SEED, n_boot: int = N_BOOT) -> dict:
    """RAW + EQUAL-ASSET-RISK, each with its cluster-bootstrap CI vs zero, on
    ONE seed.  The columns every P-GEN-1-shaped row carries."""
    rs = [t.net_r for t in book]
    ac = [t.symbol for t in book]
    if len(rs) < 2 or len(set(ac)) < 2:
        return {"raw_expectancy_r": r6(float(np.mean(rs))) if rs else None,
                "ear_expectancy_r": r6(ear_expectancy(rs, ac)),
                "co_headline_note": "too few clusters to bootstrap"}
    raw = _ci_from(cluster_boot(rs, ac, seed=seed, n_boot=n_boot),
                   float(np.mean(rs)))
    ear = _ci_from(cluster_boot_ear(rs, ac, seed=seed, n_boot=n_boot),
                   ear_expectancy(rs, ac))
    return {"raw_expectancy_r": r6(raw["point"]), "raw_ci_lo": r6(raw["lo"]),
            "raw_ci_hi": r6(raw["hi"]),
            "raw_p_one_sided": r6(raw["p_one_sided"]),
            "raw_verdict": _verdict(raw),
            "ear_expectancy_r": r6(ear["point"]), "ear_ci_lo": r6(ear["lo"]),
            "ear_ci_hi": r6(ear["hi"]),
            "ear_p_one_sided": r6(ear["p_one_sided"]),
            "ear_verdict_would_be": _verdict(ear),
            "co_headlines_disagree": bool(_verdict(raw) != _verdict(ear)),
            "co_headline_seed": int(seed),
            "ear_ci_is_new": EAR_CI_IS_NEW,
            "verdict_carried_by": f"{LEAN_TAG} " + LEAN_PANEL_VERDICT}


def headline_n(book: list, label: str, panel, seed: int = SEED) -> pd.DataFrame:
    """THE HEADLINE OVER A DECLARED PANEL — both aggregations x {ALL, EVERY
    panel asset, per-direction, per-exit-reason}.

    `tierc6.headline_v6` lists the assets PRESENT in the book, so an asset
    that never traded vanishes from the table.  On a twelve-asset panel that
    is the row a reader most needs: "per-asset rows" means every declared
    asset, the n = 0 ones included.  The ALL rows carry the co-headline CIs
    on the ruler seed AND on the lineage seed [L8].
    Key: ["label", "group", "key", "aggregation"].
    """
    panel = tuple(panel)
    rows: list[dict] = []
    rows += agg_both(book, label, "ALL", "ALL", window="full_corridor")
    for s in sorted(panel):
        rows += agg_both([t for t in book if t.symbol == s], label, s,
                         "asset", window="full_corridor")
    for dn, dv in (("long", 1), ("short", -1)):
        rows += agg_both([t for t in book if t.direction == dv], label, dn,
                         "direction", window="full_corridor")
    for er in sorted(set(t.exit_reason for t in book)):
        rows += agg_both([t for t in book if t.exit_reason == er], label, er,
                         "exit_reason", window="full_corridor")
    df = pd.DataFrame(rows)
    df["universe"] = panel_name(panel)
    df["n_panel_assets"] = len(panel)
    ch = {s_: co_headline(book, seed=s_) for s_ in _seed_pair(seed)}
    for tag, s_ in zip(("", "sens_"), _seed_pair(seed)):
        for agn, pre in (("raw_panel", "raw"), ("equal_asset_risk", "ear")):
            m = (df["group"] == "ALL") & (df["aggregation"] == agn)
            df.loc[m, f"{tag}ci_seed"] = int(s_)
            df.loc[m, f"{tag}ci_lo"] = ch[s_].get(f"{pre}_ci_lo")
            df.loc[m, f"{tag}ci_hi"] = ch[s_].get(f"{pre}_ci_hi")
            df.loc[m, f"{tag}p_one_sided"] = ch[s_].get(f"{pre}_p_one_sided")
    df["ci_note"] = np.where(
        df["group"] == "ALL",
        "asset-cluster bootstrap vs zero, 90% percentile CI; the "
        "equal_asset_risk row's CI is " + EAR_CI_IS_NEW,
        "no cluster CI on a slice row — one asset is one cluster")
    return df


def _seed_pair(seed: int) -> tuple[int, int]:
    """(ruler seed, sensitivity seed) [L8]: 20260921 scored, 20260816 beside;
    asked to score ON the lineage seed, the contract seed becomes the echo."""
    return (int(seed), SEED_LINEAGE if int(seed) != SEED_LINEAGE else SEED)


# ═══════════════════════ THE REGISTRATION GATE — TEXT BEFORE RESULT, IN CODE
_ID_OK = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
UNPINNED = "UNPINNED"           # the explicit, PRINTED opt-out of the head pin
WITNESS_LAW = (
    "THE REGISTRY'S WITNESS. research_outputs/tierc10/** is gitignored (the "
    "lineage's rule for every tier's outputs), so git never sees a filing and "
    "a wiped directory restarts the chain at GENESIS with nothing on disk to "
    "betray it. The order of record is therefore witnessed OUTSIDE the "
    "directory: register() and every door print the registry HEAD "
    "(line_sha256 of the last line) and its length; the caller pins them as "
    "head_of_record=(length, head) from a TRACKED file (the Stage B runner, "
    "the BUILD doc's filing transcript); every scored row and .scored.json "
    "carries them. A wipe-and-refile with ANY changed byte of text, prior, m "
    "or book spec moves the head and HALTs against the pin; an identical "
    "refile reproduces the same head and changes nothing. A PIN VOUCHES ONLY "
    "FOR THE LINES IT INCLUDES: a head taken BEFORE a registration's own "
    "registry line says nothing about that line — it could be cut, the text "
    "sharpened and the chain re-grown behind the pin — so a door offered a "
    "pin shorter than the registration's sequence number HALTs. Pin the head "
    "printed AT OR AFTER the filing; the head printed after the LAST filing "
    "vouches for all of them.")


def _sha(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def _payload(reg_id: str, text: str, prior_pct, family_m: int,
             fields: dict | None, book_spec: dict) -> dict:
    return {"registration": reg_id, "text": text,
            "prior_pct": None if prior_pct is None else int(prior_pct),
            "family_m": int(family_m), "book_spec": book_spec,
            "fields": {str(k): str(v) for k, v in sorted((fields or {}).items())}}


def _payload_sha(p: dict) -> str:
    return _sha(json.dumps(p, sort_keys=True, ensure_ascii=False))


def _registry_lines(root: Path) -> list[dict]:
    p = root / REGISTRY
    if not p.exists():
        return []
    return [json.loads(ln) for ln in p.read_text().splitlines() if ln.strip()]


def _chain_ok(lines: list[dict]) -> tuple[bool, str]:
    prev = "GENESIS"
    for k, ln in enumerate(lines, 1):
        body = {x: ln[x] for x in ("seq", "registration", "sha256", "prev")}
        if ln.get("prev") != prev:
            return False, f"registry line {k}: prev-link broken"
        if ln.get("seq") != k:
            return False, f"registry line {k}: sequence is {ln.get('seq')}"
        if ln.get("line_sha256") != _sha(json.dumps(body, sort_keys=True)):
            return False, f"registry line {k}: line hash does not verify"
        prev = ln["line_sha256"]
    return True, "chain verifies"


def registry_head(root: Path | None = None) -> dict:
    """The registry's HEAD and LENGTH — the two values to pin OUTSIDE the
    registry's own directory [WITNESS_LAW].  HALTs on a broken chain."""
    root = Path(root) if root else REG_DIR
    lines = _registry_lines(root)
    ok, why = _chain_ok(lines)
    if not ok:
        raise SystemExit(f"HALT: {root / REGISTRY} — {why}.")
    return {"registry_len": len(lines),
            "registry_head": lines[-1]["line_sha256"] if lines else "GENESIS",
            "registry_root_is_canonical":
                bool(root.resolve() == REG_DIR.resolve())}


def _check_head(lines: list[dict], head_of_record, root: Path,
                rec: dict) -> dict:
    """The pin, held against the chain — FOR ONE REGISTRATION.
    `head_of_record=(length, head)` must satisfy THREE things:
      · line `length` of the registry carries exactly that line_sha256 — a
        PREFIX check, so LATER filings never invalidate an earlier pin;
      · `length >= rec["seq"]`: the pinned head INCLUDES this registration's
        own line.  A head taken before it cannot vouch for it — the line
        could be cut, the text amended and the chain re-grown behind the pin
        with the pinned line untouched [TC10 review, the witness hole];
      · the chain from the registration's line up to the pinned line verifies
        link by link, and that line names THIS id with THIS payload sha — so
        the pinned head is a commitment to the filed bytes, by construction.
    Under the CANONICAL registry a door with no pin HALTs; the literal
    "UNPINNED" is the explicit opt-out and rides the row.  A throwaway
    registry (fixtures) may go unpinned: its rows say
    `registration_root_is_canonical=False`.

    WHAT WOULD MAKE THIS WRONG: checking only that the pinned line is still
    there (a STALE pin would then certify `registry_head_pinned=True` for a
    registration amended after the look), or trusting the record's own `seq`
    without holding it against the line the chain keeps at that position."""
    canonical = bool(root.resolve() == REG_DIR.resolve())
    head = lines[-1]["line_sha256"] if lines else "GENESIS"
    out = {"registry_len": len(lines), "registry_head": head,
           "registration_root_is_canonical": canonical,
           "registry_head_pinned": False, "registry_pin": None,
           "registry_pin_covers_seq": None}
    if head_of_record is None:
        if canonical:
            raise SystemExit(
                f"HALT: no head_of_record at a door of the CANONICAL "
                f"registry. Pin what register() printed at filing — "
                f"head_of_record=({len(lines)}, '{head[:16]}...') — from a "
                f"TRACKED file, or say head_of_record='{UNPINNED}' and let "
                f"the row carry that. [WITNESS_LAW]")
        return out
    if head_of_record == UNPINNED:
        return out
    try:
        n, h = head_of_record
        n, h = int(n), str(h)
    except Exception:                                       # noqa: BLE001
        raise SystemExit(f"HALT: head_of_record must be (length, "
                         f"line_sha256) or '{UNPINNED}'; got "
                         f"{head_of_record!r}.")
    if not (1 <= n <= len(lines)) or lines[n - 1]["line_sha256"] != h:
        got = lines[n - 1]["line_sha256"][:16] if 1 <= n <= len(lines) else None
        raise SystemExit(
            f"HALT: the registry under {root} is NOT the registry of record "
            f"— the pin says line {n} = {h[:16]}..., the chain holds "
            f"{len(lines)} line(s) and line {n} = {got}. It was wiped, cut "
            f"or re-filed with different text after the pin was taken.")
    rid, seq = rec.get("registration"), rec.get("seq")
    if not isinstance(seq, int) or seq < 1 or n < seq:
        raise SystemExit(
            f"HALT: STALE PIN — head_of_record names registry line {n}, but "
            f"{rid} was filed at line {seq}. A head taken BEFORE a "
            f"registration's own line cannot vouch for it: that line could "
            f"be cut, its text amended and the chain re-grown behind the pin "
            f"without moving line {n}. Pin (registry_len, registry_head) as "
            f"printed AT OR AFTER {rid}'s filing — the head after the LAST "
            f"filing vouches for every registration. [WITNESS_LAW]")
    prev = lines[seq - 2]["line_sha256"] if seq > 1 else "GENESIS"
    for k in range(seq, n + 1):
        ln = lines[k - 1]
        body = {x: ln.get(x) for x in ("seq", "registration", "sha256",
                                       "prev")}
        if ln.get("prev") != prev or ln.get("seq") != k \
                or ln.get("line_sha256") != _sha(json.dumps(body,
                                                            sort_keys=True)):
            raise SystemExit(
                f"HALT: the chain from {rid}'s line {seq} to the pinned "
                f"line {n} does not verify at line {k} — the pin cannot "
                f"vouch for this registration. [WITNESS_LAW]")
        prev = ln["line_sha256"]
    own = lines[seq - 1]
    if own.get("registration") != rid or own.get("sha256") != rec.get("sha256"):
        raise SystemExit(
            f"HALT: registry line {seq} — the line the pin vouches for — "
            f"names {own.get('registration')} / "
            f"{str(own.get('sha256'))[:16]}, not {rid} / "
            f"{str(rec.get('sha256'))[:16]}. The pinned chain is not a "
            f"commitment to this filing. [WITNESS_LAW]")
    return dict(out, registry_head_pinned=True, registry_pin=f"{n}:{h}",
                registry_pin_covers_seq=True)


def register(reg_id: str, text: str, prior_pct, arms=None,
             family_m: int = FAMILY_M, fields: dict | None = None,
             root: Path | None = None) -> dict:
    """FILE THE TEXT — AND THE BOOK IT IS A REGISTRATION OF.  Writes
    `<root>/<reg_id>.json` — the text, its sha256, the BOOK SPEC (`arms`, a
    list of `arm_spec(...)`: panel, lanes, ruler, base, scored slot and, for a
    `run_cell_n` arm, the card's and the roles' class and every field), the
    payload sha256 (text + prior + m + book spec + fields), and a MONOTONE
    SEQUENCE NUMBER — and appends one hash-chained line to REGISTRY.jsonl.
    `fields` stays a free, hashed annotation; NOTHING consults it.  The book
    spec is what both doors consult.  EVERY arm must name the LOAO count that
    carries the above-half line (`arm_spec(..., loao_line=...)`, the same on
    all arms) and the TEXT must carry that count's clause
    (`loao_line_clause`) — a filing that does not say is refused HERE, before
    a registry line exists.

    A FILED REGISTRATION IS NEVER AMENDED.  Filing the same payload again is a
    no-op that returns the record on file (a rebuild must be able to call this
    unconditionally); filing DIFFERENT text under a filed id HALTs; filing an
    id for which a RESULT already exists HALTs — the text cannot follow the
    result.  No wall clock is written: the sequence number and the chain are
    the order of record.  GIT IS NOT THE WITNESS — the directory is gitignored
    [WITNESS_LAW]; the returned (and logged) `registry_len` / `registry_head`
    are, once the caller pins them in a tracked file.

    WHAT WOULD MAKE THIS WRONG: deriving the sequence from anything but the
    registry (a deleted file would hand its number to a rewritten one),
    hashing the text after normalising it (the filed bytes are the claim), or
    hashing a book spec nobody then reads (the gate would open for any book).
    """
    root = Path(root) if root else REG_DIR
    if not _ID_OK.match(reg_id or ""):
        raise SystemExit(f"HALT: registration id {reg_id!r} is not a plain "
                         f"token [A-Za-z0-9._-].")
    if not isinstance(text, str) or not text.strip():
        raise SystemExit(f"HALT: registration {reg_id} has no text.")
    spec = _check_spec(arms, f"register({reg_id})")
    _require_loao_line(spec, text, f"register({reg_id})")
    _require_era(spec, f"register({reg_id})")
    pay = _payload(reg_id, text, prior_pct, family_m, fields, spec)
    sha = _payload_sha(pay)
    root.mkdir(parents=True, exist_ok=True)
    p = root / f"{reg_id}.json"
    lines = _registry_lines(root)
    ok, why = _chain_ok(lines)
    if not ok:
        raise SystemExit(f"HALT: {root / REGISTRY} — {why}.")
    mine = [ln for ln in lines if ln["registration"] == reg_id]
    if p.exists():
        rec = json.loads(p.read_text())
        if rec.get("sha256") == sha and mine and mine[0]["sha256"] == sha:
            return dict(rec, already_filed=True, **registry_head(root))
        raise SystemExit(
            f"HALT: registration {reg_id} is ALREADY FILED (seq "
            f"{rec.get('seq')}, sha {str(rec.get('sha256'))[:16]}) with "
            f"different text/prior/m/book spec. A filed registration is "
            f"never amended in place — file a NEW id and say why.")
    if mine:
        raise SystemExit(
            f"HALT: the registry already records {reg_id} (seq "
            f"{mine[0]['seq']}) but its file is gone — a registration was "
            f"REMOVED after filing. It cannot be re-filed.")
    if (root / f"{reg_id}.scored.json").exists():
        raise SystemExit(
            f"HALT: a RESULT already exists for {reg_id} "
            f"({reg_id}.scored.json). The text cannot follow the result.")
    seq = len(lines) + 1
    rec = dict(pay, seq=seq, text_sha256=_sha(text), sha256=sha,
               sha_law="sha256 = sha256(json.dumps({registration, text, "
                       "prior_pct, family_m, book_spec, fields}, "
                       "sort_keys=True, ensure_ascii=False)); text_sha256 = "
                       "sha256(text)")
    body = {"seq": seq, "registration": reg_id, "sha256": sha,
            "prev": lines[-1]["line_sha256"] if lines else "GENESIS"}
    line = dict(body, line_sha256=_sha(json.dumps(body, sort_keys=True)))
    tmp = p.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(rec, indent=2, sort_keys=True,
                              ensure_ascii=False) + "\n")
    os.replace(tmp, p)
    with open(root / REGISTRY, "a") as fh:
        fh.write(json.dumps(line, sort_keys=True) + "\n")
    head = registry_head(root)
    log(f"  REGISTERED {reg_id} seq {seq} · registry_len "
        f"{head['registry_len']} · registry_head {head['registry_head']} "
        f"— PIN THESE TWO in a tracked file [WITNESS_LAW]")
    return dict(rec, already_filed=False, **head)


def _verify_record(reg_id: str, root: Path, family_m: int) -> tuple:
    """(record, registry lines) — the file against its own shas, the chain,
    the chain's word for THIS file, the book spec's shape, the family size."""
    p = root / f"{reg_id}.json"
    if not p.exists():
        raise SystemExit(
            f"HALT: TEXT BEFORE RESULT — no registration is filed for "
            f"{reg_id!r} under {root}. Nothing is scored, nothing is ridden.")
    rec = json.loads(p.read_text())
    pay = _payload(rec.get("registration"), rec.get("text", ""),
                   rec.get("prior_pct"), rec.get("family_m", -1),
                   rec.get("fields"), rec.get("book_spec"))
    if (rec.get("registration") != reg_id
            or rec.get("sha256") != _payload_sha(pay)
            or rec.get("text_sha256") != _sha(rec.get("text", ""))):
        raise SystemExit(
            f"HALT: registration file {p.name} does NOT verify against its "
            f"own sha256 — the filed text was altered after filing.")
    lines = _registry_lines(root)
    ok, why = _chain_ok(lines)
    if not ok:
        raise SystemExit(f"HALT: {root / REGISTRY} — {why}.")
    mine = [ln for ln in lines if ln["registration"] == reg_id]
    if len(mine) != 1 or mine[0]["sha256"] != rec["sha256"] \
            or mine[0]["seq"] != rec.get("seq"):
        raise SystemExit(
            f"HALT: the registry does not vouch for {reg_id} "
            f"({len(mine)} line(s); file seq {rec.get('seq')}) — a "
            f"registration was deleted, re-filed or swapped.")
    _check_spec((rec.get("book_spec") or {}).get("arms"),
                f"{p.name} book_spec")
    if int(rec["family_m"]) != int(family_m):
        raise SystemExit(
            f"HALT: {reg_id} was filed under family m={rec['family_m']}, "
            f"the scorer declares m={family_m}.")
    return rec, lines


def require_registered(reg_id: str, text: str, root: Path | None = None,
                       family_m: int = FAMILY_M, head_of_record=None) -> dict:
    """THE GATE'S FIRST HALF (the second is the BOOK — `run_cell_n`, `score`).
    Returns the filed record + the registry head, or HALTs.  Refuses when:
      · `text` is not offered — BOTH doors take the claim in hand, always;
      · no file exists for `reg_id`;
      · the file's recorded shas do not match its own text (tampered file);
      · the caller's `text` is not the filed text (the claim moved after filing);
      · the registry chain is broken, omits the id, names it twice, or records
        a different sha (a delete-and-refile, a swapped file);
      · the chain is not the one `head_of_record` pinned (a WIPED directory);
      · the pin is STALE — taken before this registration's own registry line
        (an amend-and-re-chain behind the pin would otherwise ride certified);
      · the filing does not say which LOAO count carries the above-half line
        (`_require_loao_line`: book spec AND text);
      · an arm of the filing names NO era (`_require_era` [R1]);
      · the declared family size is not the contract's m."""
    root = Path(root) if root else REG_DIR
    if not isinstance(text, str) or not text.strip():
        raise SystemExit(
            f"HALT: {reg_id} — no text offered. The door compares the claim "
            f"IN THE CALLER'S HAND with the claim on file; a caller with no "
            f"text has nothing to compare.")
    rec, lines = _verify_record(reg_id, root, family_m)
    if _sha(text) != rec["text_sha256"]:
        raise SystemExit(
            f"HALT: the text offered for {reg_id} is not the text on file "
            f"(sha {_sha(text)[:16]} vs filed {rec['text_sha256'][:16]}). "
            f"The claim moved after it was registered.")
    _require_loao_line(rec["book_spec"], rec["text"], f"{reg_id}.json")
    _require_era(rec["book_spec"], f"{reg_id}.json")
    return dict(rec, _head=_check_head(lines, head_of_record, root, rec))


def require_arm(reg_id: str, text: str, arm: str, panel, lanes=None,
                head_of_record=None, root: Path | None = None,
                family_m: int = FAMILY_M) -> dict:
    """THE DOOR AN EXTERNAL RUNNER MUST WALK THROUGH BEFORE IT RIDES ONE BAR.

    `run_cell_n` gates the books IT rides.  The spring lane, the breakeven
    floor and the BRK lanes have runners of their own, in other files — and
    this module cannot stand in front of a replay it does not own.  So those
    runners call THIS, first:

        gate = TP.require_arm("P-BRK-S1", TEXT, "P-BRK-S1 vs zero", panel,
                              lanes=("brk-s1",), head_of_record=HEAD_OF_RECORD)
        ...ride...
        book = TP.external_book(trades, gate, lo_ms, hi_ms)
        row  = TP.score("P-BRK-S1", TEXT, book, panel, arm=gate["arm"], ...)

    It is `require_registered` (text on file, sha, chain, the pin — STALE pins
    refused — the LOAO line of record) PLUS the arm lookup: the named arm must
    be FILED, filed for an EXTERNAL runner (a `run_cell_n` arm is ridden by
    `run_cell_n` and by nothing else), on exactly the offered panel, and every
    lane the runner means to emit must be a filed lane.  It returns the GATE —
    what `external_book` stamps onto the trades, and what `score()` reads
    back: under the registry of record an external arm is scored ONLY on a
    Book that came through here.

    It is provenance, not cryptography: a runner that rides first and calls
    this afterwards has broken the law in a way no code in this file can see;
    a reviewer greps the runner for `require_arm(` ABOVE its first replay."""
    root = Path(root) if root else REG_DIR
    rec = require_registered(reg_id, text, root=root, family_m=family_m,
                             head_of_record=head_of_record)
    panel = _check_panel(panel)
    arms = rec["book_spec"]["arms"]
    pick = [a for a in arms if a["arm"] == arm]
    if not pick:
        raise SystemExit(f"HALT: require_arm — {reg_id} files no arm "
                         f"{arm!r}; it files {[a['arm'] for a in arms]}.")
    a = pick[0]
    bad = []
    if a["runner"] != "external":
        bad.append(f"runner: filed {a['runner']!r} — that arm is ridden by "
                   f"run_cell_n, not by an external runner")
    if tuple(a["panel"]) != panel:
        bad.append(f"panel: filed {a['panel_name']} / offered "
                   f"{panel_name(panel)}")
    if lanes is not None:
        stray = sorted({str(x) for x in lanes} - set(a["lanes"]))
        if stray or not list(lanes):
            bad.append(f"lanes: filed {a['lanes']} / the runner means to "
                       f"emit {stray or 'none'}")
    if bad:
        raise SystemExit(
            f"HALT: require_arm({reg_id}) — the runner's book is NOT the "
            f"book registered as arm {arm!r}: " + " | ".join(bad)
            + ". Nothing is ridden.")
    return {"runner": "external", "registration": reg_id, "arm": a["arm"],
            "panel": list(a["panel"]), "lanes": list(a["lanes"]),
            "ruler": a["ruler"], "base": a["base"],
            "scored_in_family": bool(a["scored_in_family"]),
            "loao_line": a.get("loao_line"), "era": a["era"],
            "era_window": list(era_window(a["era"])),
            "era_note": era_note(a["era"]),
            "registration_seq": rec["seq"],
            "registration_sha256": rec["sha256"], **rec["_head"]}


def external_book(trades, gate: dict, lo_ms: int | None = None,
                  hi_ms: int | None = None) -> Book:
    """An external runner's journal, wearing the gate it entered through.
    `gate` is `require_arm(...)`'s return, whole — a hand-built dict is a
    deliberate act a reviewer can grep for, exactly like a hand-built Book.
    The journal is held against the gate HERE, where the runner still has the
    trades in hand: a symbol outside the filed panel, a lane the filing does
    not name, or a campaign whose ENTRY falls outside the filed era [R1] is
    refused before the journal can become a row."""
    need = {"runner", "registration", "arm", "panel", "lanes", "era",
            "registration_sha256"}
    if not isinstance(gate, dict) or not need <= set(gate) \
            or gate.get("runner") != "external":
        raise SystemExit("HALT: external_book needs the gate require_arm() "
                         "returned.")
    trades = list(trades)
    stray = sorted({str(t.symbol) for t in trades} - set(gate["panel"]))
    lane_x = sorted({str(t.lane) for t in trades} - set(gate["lanes"]))
    if stray or lane_x:
        raise SystemExit(
            f"HALT: external_book — the journal holds symbols {stray} / "
            f"lanes {lane_x} outside the gate's filed panel and lanes.")
    out_e = [t for t in trades if not in_era(t.entry_ms, gate["era"])]
    if out_e:
        raise SystemExit(
            f"HALT: external_book — {len(out_e)} of {len(trades)} campaigns "
            f"ENTER outside the arm's filed {gate['era']!r} era "
            f"(first {iso(int(min(t.entry_ms for t in out_e)))}); "
            f"{era_note(gate['era'])} Ride corridor_era(panel, "
            f"{gate['era']!r}).")
    return Book(trades, spec={
        "runner": "external", "registration": gate["registration"],
        "arm": gate["arm"], "panel": list(gate["panel"]),
        "era": gate["era"],
        "registration_sha256": gate["registration_sha256"],
        "lo_ms": None if lo_ms is None else int(lo_ms),
        "hi_ms": None if hi_ms is None else int(hi_ms)})


def registration_table(root: Path | None = None) -> pd.DataFrame:
    """Every filed registration, in filing order — the `registration_text`
    table, to be written BEFORE any result table.  HALTs if any file fails
    the gate or a registry line has no file (totality, both directions)."""
    root = Path(root) if root else REG_DIR
    lines = _registry_lines(root)
    ok, why = _chain_ok(lines)
    if not ok:
        raise SystemExit(f"HALT: {root / REGISTRY} — {why}.")
    on_disk = sorted(p.stem for p in root.glob("*.json")
                     if not p.name.endswith(".scored.json")) \
        if root.exists() else []
    if sorted(ln["registration"] for ln in lines) != on_disk:
        raise SystemExit(
            f"HALT: registry names {[ln['registration'] for ln in lines]} "
            f"but the files are {on_disk} — totality fails.")
    head = registry_head(root)
    rows = []
    for ln in lines:
        rec, _ = _verify_record(
            ln["registration"], root,
            json.loads((root / f"{ln['registration']}.json")
                       .read_text())["family_m"])
        arms = rec["book_spec"]["arms"]
        sc = [a for a in arms if a["scored_in_family"]]
        rows.append({"registration": rec["registration"], "seq": rec["seq"],
                     "prior_pct": rec["prior_pct"],
                     "family_m": rec["family_m"], "text": rec["text"],
                     "n_arms": len(arms),
                     "scored_arm": sc[0]["arm"] if sc else None,
                     "scored_panel": sc[0]["panel_name"] if sc else None,
                     "scored_ruler": sc[0]["ruler"] if sc else None,
                     "scored_runner": sc[0]["runner"] if sc else None,
                     "scored_era": sc[0].get("era") if sc else None,
                     "scored_loao_line": sc[0].get("loao_line") if sc
                     else None,
                     "book_spec_json": json.dumps(rec["book_spec"],
                                                  sort_keys=True),
                     **{f"field_{k}": v for k, v in rec["fields"].items()},
                     "text_sha256": rec["text_sha256"],
                     "registration_sha256": rec["sha256"],
                     "registry_line_sha256": ln["line_sha256"],
                     "registry_len": head["registry_len"],
                     "registry_head": head["registry_head"],
                     "registry_root_is_canonical":
                         head["registry_root_is_canonical"]})
    return pd.DataFrame(rows)


def _book_sha(book) -> str | None:
    """sha256 of a book's (symbol, lane, entry_ms, net_r) rows, sorted — what
    `.scored.json` binds on the FIRST score of an arm."""
    if book is None:
        return None
    return _sha(json.dumps(sorted(
        [str(t.symbol), str(t.lane), int(t.entry_ms), repr(float(t.net_r))]
        for t in book)))


def _mark_scored(rec: dict, root: Path, arm: str, stamp: dict) -> None:
    """A result now exists under this registration; say so on disk, so the
    text can never be (re)filed behind it — and BIND THE RESULT'S INPUTS: the
    book sha, the base sha, the ruler seed and n_boot of the arm's FIRST
    score.  A re-score must reproduce them (that is what `--rerun` does); a
    different book, or a different seed, under an already-scored arm HALTs —
    that is a second look, and it needs a new id.  Deterministic, no clock."""
    p = root / f"{rec['registration']}.scored.json"
    old = {}
    if p.exists():
        try:
            old = json.loads(p.read_text()) or {}
        except Exception:                                   # noqa: BLE001
            old = {}
    arms = dict(old.get("arms") or {})
    if arm in arms and arms[arm] != stamp:
        moved = sorted(k for k in set(arms[arm]) | set(stamp)
                       if arms[arm].get(k) != stamp.get(k))
        raise SystemExit(
            f"HALT: {rec['registration']} arm {arm!r} was ALREADY SCORED on "
            f"different inputs ({moved} moved). A re-score must reproduce "
            f"the first; a second look needs a NEW registration.")
    arms[arm] = stamp
    body = json.dumps({
        "registration": rec["registration"], "seq": rec["seq"],
        "registration_sha256": rec["sha256"], "arms": arms,
        "law": "a result has been computed under this registration; its "
               "text can no longer be filed or amended, and each arm is "
               "bound to the inputs of its first score"},
        indent=2, sort_keys=True) + "\n"
    if not p.exists() or p.read_text() != body:
        tmp = p.with_suffix(".json.tmp")
        tmp.write_text(body)
        os.replace(tmp, p)


def _ci_cols(ci: dict, pre: str) -> dict:
    return {f"{pre}ci_point": r6(ci["point"]), f"{pre}ci_lo": r6(ci["lo"]),
            f"{pre}ci_hi": r6(ci["hi"])}


def _set_change_law(ruler: str, changes) -> bool:
    """IS THE ROW SCORED TWO-SAMPLE?  The lineage's set-change law, in ONE
    place [tierc8.score: `ci = ci_2 if changes else ci_p`, and
    `T7.loao(..., two_sample=changes)`]:

        vs_zero      never (there is no twin);
        two_sample   always (COMMISSIONED; its premise is measured by score());
        set_change   iff the arm CHANGES the campaign set — a base campaign
                     with no twin in the arm, or an arm campaign with none in
                     the base, keyed (symbol, lane, entry_ms).

    Both the headline CI (`_rule`) and the LOAO panels (`score`) read THIS
    function, so the panels can never be scored by another ruler than the
    headline [tierc7's law].

    WHAT WOULD MAKE THIS WRONG: keeping the PAIRED interval on a changed set —
    the unpaired campaigns, which are the arm's whole effect on the set, would
    be dropped from the statistic and the row would score the survivors."""
    if ruler == "vs_zero":
        return False
    return bool(ruler == "two_sample" or changes)


def _rule(book, base, ruler, seed, n_boot):
    """One ruler pass on one seed -> (ci, ci_paired, ci_two, changes, pv)."""
    rs = [t.net_r for t in book]
    ac = [t.symbol for t in book]
    none = {"point": None, "lo": None, "hi": None, "p_one_sided": None}
    if ruler == "vs_zero":
        pt = float(np.mean(rs))
        ci = _ci_from(cluster_boot(rs, ac, seed=seed, n_boot=n_boot), pt)
        return ci, none, none, None, []
    bnet = [t.net_r for t in base]
    bcl = [t.symbol for t in base]
    bu = {(t.symbol, t.lane, t.entry_ms): t.net_r for t in base}
    pv, pc = [], []
    for t in book:
        k = (t.symbol, t.lane, t.entry_ms)
        if k in bu:
            pv.append(t.net_r - bu[k])
            pc.append(t.symbol)
    changes = (len(base) - len(pv)) > 0 or (len(book) - len(pv)) > 0
    ci_p = (_ci_from(cluster_boot(pv, pc, seed=seed, n_boot=n_boot),
                     float(np.mean(pv))) if pv else none)
    ci_2 = _ci_from(cluster_boot_diff(rs, ac, bnet, bcl, seed=seed,
                                      n_boot=n_boot),
                    float(np.mean(rs)) - float(np.mean(bnet)))
    ci = ci_2 if _set_change_law(ruler, changes) else ci_p
    return ci, ci_p, ci_2, changes, pv


def _bind_arm(rec: dict, arm, panel: tuple, ruler: str,
              scored_in_family: bool, book, base) -> dict:
    """THE GATE'S SECOND HALF, AT THE SCORER: the offered arm IS a filed one.
    Panel, ruler, scored slot, lanes — and, for a `run_cell_n` arm, the Book's
    own provenance; for a "card-v6" base, a Book that is card v6 on the arm's
    panel over the same window.  HALTs with the first difference."""
    rid = rec["registration"]
    arms = rec["book_spec"]["arms"]
    if arm is None:
        pick = [a for a in arms if a["scored_in_family"]] \
            if scored_in_family else []
        if len(pick) != 1:
            raise SystemExit(
                f"HALT: {rid} — name the arm: "
                f"{[a['arm'] for a in arms]} (only the ONE scored arm may "
                f"be left implicit).")
        a = pick[0]
    else:
        pick = [a for a in arms if a["arm"] == arm]
        if not pick:
            raise SystemExit(f"HALT: {rid} files no arm {arm!r}; it files "
                             f"{[a['arm'] for a in arms]}.")
        a = pick[0]
    bad = []
    if tuple(a["panel"]) != panel:
        bad.append(f"panel: filed {a['panel_name']} / offered "
                   f"{panel_name(panel)}")
    if a["ruler"] != ruler:
        bad.append(f"ruler: filed {a['ruler']} / offered {ruler}")
    if bool(a["scored_in_family"]) != bool(scored_in_family):
        bad.append(f"scored_in_family: filed {a['scored_in_family']} / "
                   f"offered {scored_in_family}")
    stray = sorted({str(t.lane) for t in book} - set(a["lanes"]))
    if stray:
        bad.append(f"lanes: filed {a['lanes']} / the book carries {stray}")
    if a["runner"] == "run_cell_n":
        sp = getattr(book, "spec", None)
        if not isinstance(book, Book) or not sp:
            bad.append("book: the arm is filed for run_cell_n, the offered "
                       "book is not a Book from run_cell_n (a filtered or "
                       "re-assembled list has no provenance)")
        elif sp.get("ride") != a["ride"] or sp.get("panel") != a["panel"]:
            bad.append("book provenance: " + "; ".join(
                (_spec_diff(a["ride"], sp.get("ride") or {})
                 + [f"panel {sp.get('panel')}"])[:3]))
    else:
        sp = getattr(book, "spec", None)
        if isinstance(book, Book) and sp:
            want = {"runner": "external", "registration": rid,
                    "arm": a["arm"], "panel": a["panel"], "era": a["era"],
                    "registration_sha256": rec["sha256"]}
            off = [f"{k}: gate {sp.get(k)!r:.40} / filed {v!r:.40}"
                   for k, v in want.items() if sp.get(k) != v]
            if off:
                bad.append("book gate (require_arm -> external_book): "
                           + "; ".join(off[:3]))
        elif rec["_head"]["registration_root_is_canonical"]:
            bad.append("book: under the REGISTRY OF RECORD an external arm "
                       "is scored only on a Book that entered through "
                       "require_arm() -> external_book(); a bare list has "
                       "no gate")
    if a["base"] == "card-v6":
        sp = getattr(base, "spec", None)
        if not isinstance(base, Book) or not sp:
            bad.append("base: filed 'card-v6' — the base must be a Book "
                       "from run_cell_n, not a bare list")
        elif sp.get("ride") != CONTROL_RIDE or sp.get("panel") != a["panel"]:
            bad.append(f"base: filed card v6 on {a['panel_name']}; offered "
                       + "; ".join((_spec_diff(CONTROL_RIDE,
                                               sp.get("ride") or {})
                                    + [f"panel {sp.get('panel')}"])[:3]))
        elif isinstance(book, Book) and book.spec and (
                (book.spec.get("lo_ms"), book.spec.get("hi_ms"))
                != (sp.get("lo_ms"), sp.get("hi_ms"))):
            bad.append("base: ridden over a DIFFERENT window than the book")
    if bad:
        raise SystemExit(
            f"HALT: score({rid}) — the offered book is NOT the book "
            f"registered as arm {a['arm']!r}: " + " | ".join(bad)
            + ". A registration scores ITS OWN book and no other.")
    return a


def score(reg_id: str, text: str, book: list, panel, base: list | None = None,
          ruler: str = "vs_zero", seed: int = SEED, arm: str | None = None,
          scored_in_family: bool = True, note: str = "",
          root: Path | None = None, n_boot: int = N_BOOT,
          head_of_record=None, era: str | None = None) -> dict:
    """ONE REGISTRATION ROW — AND IT REFUSES TO EXIST WITHOUT ITS TEXT, OR ON
    ANY BOOK BUT ITS OWN.

    The first act is `require_registered(reg_id, text, head_of_record)`: no
    file, a tampered file, moved text, a broken or WIPED registry, a STALE pin
    (one taken before this registration's own registry line), a filing that
    does not name its LOAO line of record, a filing whose arms name NO ERA
    -> HALT.
    The second is `_bind_arm`: the arm, the panel, the ruler, the scored
    slot, the lanes and the book's provenance must be the FILED ones.  The
    third binds the INPUTS on disk (`.scored.json`: book sha, base sha, seed,
    n_boot) BEFORE a single number is computed — a re-score must reproduce
    them.  Then `tierc8.score`'s row, one registration at a time:

      ruler="vs_zero"     one-sample asset-cluster bootstrap of the mean
                          (P-GEN-1, the BRK lanes); LOAO in vs-zero mode; the
                          D15 trio is DEGENERATE BY CONSTRUCTION (no twin) and
                          is printed as None with the reason.
      ruler="two_sample"  COMMISSIONED two-sample (the contract's word): the
                          premise — the arm CHANGES the campaign set — is
                          MEASURED, and HALTs if false [tierc9's precedent].
      ruler="set_change"  tierc8's law: two-sample iff the set changed, else
                          PAIRED.  Both rulers are always printed.

    Verdict: SUPPORTED iff the 90% CI lower bound > 0 (`_verdict` — the
    lineage's law, strict, CI-only), on the RAW expectancy
    (LEAN_PANEL_VERDICT); the equal-asset-risk co-headline, the LOAO
    above-half line — `loao_clears_line_of_record` is the count the FILING
    named (`loao_line`), the other count rides beside it — the D15 trio and
    the L8 seed-sensitivity block ride the row.  The BH bar is a SEPARATE
    column, applied by `finish_family` once the family is whole.
    An EXTERNAL arm's book must, under the registry of record, be the Book
    `external_book(trades, require_arm(...))` made; every check that can HALT
    stands AHEAD of the result marker.
    `scored_in_family=False` files a report-only arm (no slot in m).
    """
    root = Path(root) if root else REG_DIR
    rec = require_registered(reg_id, text, root=root,       # REFUSES FIRST
                             head_of_record=head_of_record)
    if ruler not in RULERS:
        raise SystemExit(f"HALT: unknown ruler {ruler!r}; one of {RULERS}")
    if not book:
        raise SystemExit(f"HALT: {reg_id} — an empty book cannot be scored.")
    if (ruler == "vs_zero") != (base is None):
        raise SystemExit(f"HALT: {reg_id} — ruler {ruler!r} and base="
                         f"{'None' if base is None else 'book'} disagree.")
    panel = _check_panel(panel)
    filed = _bind_arm(rec, arm, panel, ruler, scored_in_family, book, base)
    if ruler == "two_sample":
        # the commissioned ruler's PREMISE, measured on the campaign KEYS
        # alone — before the result marker is written or a number computed.
        bk = {(t.symbol, t.lane, t.entry_ms) for t in base}
        n_pair = sum(1 for t in book
                     if (t.symbol, t.lane, t.entry_ms) in bk)
        if not (len(base) > n_pair or len(book) > n_pair):
            raise SystemExit(
                f"HALT: {reg_id} — the arm shares the WHOLE campaign set "
                f"with its base; the commissioned two-sample ruler's premise "
                f"failed. File a NEW id under ruler='set_change' and "
                f"disclose.")
    # EVERY CHECK THAT CAN HALT STANDS AHEAD OF THE RESULT MARKER [TC10
    # review]: a book holding a symbol outside the panel used to pass
    # _bind_arm, have its sha BOUND by _mark_scored, and only then HALT inside
    # loao_n — no row existed, yet the id was burnt for the right book.
    stray = sorted(({t.symbol for t in book}
                    | {t.symbol for t in (base or [])}) - set(panel))
    if stray:
        raise SystemExit(
            f"HALT: {reg_id} — the book holds {stray}, outside the declared "
            f"panel {panel_name(panel)} (cache STEMS, e.g. MNTUSDT_BYBIT — "
            f"not venue symbols). Nothing is scored and NO result marker is "
            f"written.")
    bad_r = [t for t in list(book) + list(base or [])
             if not np.isfinite(float(t.net_r))]
    if bad_r:
        raise SystemExit(f"HALT: {reg_id} — {len(bad_r)} campaign(s) carry a "
                         f"non-finite net_r. Nothing is scored.")
    # THE ERA, HELD AGAINST THE CAMPAIGNS [R1].  The filing named it before
    # the look; a caller may PIN it here, and then the two must agree.  The
    # book (and its base) must ENTER inside it — a holdout-registered lane
    # scored on campaigns from the era that tuned it is the whole hazard the
    # ruling exists to close.  Ahead of the result marker, like every HALT.
    filed_era = filed["era"]
    if era is not None and str(era) != str(filed_era):
        raise SystemExit(
            f"HALT: {reg_id} — the caller offers the {str(era)!r} era, the "
            f"filing registered arm {filed['arm']!r} for {filed_era!r}. The "
            f"era is part of the claim; it cannot move at the scorer.")
    sp_era = (getattr(book, "spec", None) or {}).get("era")
    if sp_era is not None and sp_era != filed_era:
        raise SystemExit(
            f"HALT: {reg_id} — the book was ridden on the {sp_era!r} era, "
            f"arm {filed['arm']!r} is filed for {filed_era!r}.")
    out_e = [t for t in list(book) + list(base or [])
             if not in_era(t.entry_ms, filed_era)]
    if out_e:
        raise SystemExit(
            f"HALT: {reg_id} — {len(out_e)} of {len(book) + len(base or [])} "
            f"campaigns ENTER outside arm {filed['arm']!r}'s filed "
            f"{filed_era!r} era (first "
            f"{iso(int(min(t.entry_ms for t in out_e)))}, last "
            f"{iso(int(max(t.entry_ms for t in out_e)))}). "
            f"{era_note(filed_era)} Nothing is scored and NO result marker "
            f"is written.")
    s0, s1 = _seed_pair(seed)
    _mark_scored(rec, root, filed["arm"], {
        "book_sha256": _book_sha(book), "base_sha256": _book_sha(base),
        "n": len(book), "seed": int(s0), "n_boot": int(n_boot)})
    ci, ci_p, ci_2, changes, pv = _rule(book, base, ruler, s0, n_boot)
    two = _set_change_law(ruler, changes)
    sci, *_ = _rule(book, base, ruler, s1, n_boot)
    lo_ = loao_n(book, base, panel, two_sample=two, seed=s0, label=reg_id,
                 n_boot=n_boot)
    slo = loao_n(book, base, panel, two_sample=two, seed=s1, label=reg_id,
                 n_boot=n_boot)
    rs = [t.net_r for t in book]
    ac = [t.symbol for t in book]
    if base is None:
        dd = {"n_paired": None, "paired_delta_expectancy_r": None,
              "tail_exit_ratio": None, "max_single_trade_delta_share": None,
              "unpaired_cell_n": None, "unpaired_base_n": None,
              "d15_note": "D15 trio DEGENERATE BY CONSTRUCTION: a vs-zero "
                          "lane has no twin to pair against "
                          "[tierc8_an2 precedent]; printed, gates nothing"}
        ear_draws = cluster_boot_ear(rs, ac, seed=s0, n_boot=n_boot)
        ear_ci = _ci_from(ear_draws, ear_expectancy(rs, ac))
        ear_sci = _ci_from(cluster_boot_ear(rs, ac, seed=s1, n_boot=n_boot),
                           ear_expectancy(rs, ac))
        ear_pt_book, ear_pt_base = ear_expectancy(rs, ac), None
        extra = {"paired_n": None, "unpaired_base_n_lane_keyed": None,
                 "unpaired_base_net_r": None, "whole_book_difference_r": None}
    else:
        dd = dict(d15(book, base),
                  d15_note="D15 caveats not hard gates [THE_RULING]")
        bnet = [t.net_r for t in base]
        bcl = [t.symbol for t in base]
        ear_pt_book = ear_expectancy(rs, ac)
        ear_pt_base = ear_expectancy(bnet, bcl)
        ear_draws = cluster_boot_ear_diff(rs, ac, bnet, bcl, seed=s0,
                                          n_boot=n_boot)
        ear_ci = _ci_from(ear_draws, ear_pt_book - ear_pt_base)
        ear_sci = _ci_from(cluster_boot_ear_diff(rs, ac, bnet, bcl, seed=s1,
                                                 n_boot=n_boot),
                           ear_pt_book - ear_pt_base)
        keys = {(t.symbol, t.lane, t.entry_ms) for t in book}
        extra = {"paired_n": len(pv),
                 "unpaired_base_n_lane_keyed": len(base) - len(pv),
                 "unpaired_base_net_r": r4(sum(
                     t.net_r for t in base
                     if (t.symbol, t.lane, t.entry_ms) not in keys)),
                 "whole_book_difference_r": r4(sum(rs) - sum(bnet))}
    head = rec["_head"]
    row = {
        "registration": reg_id, "arm": filed["arm"],
        "arm_runner": filed["runner"], "arm_base": filed["base"],
        "arm_lanes": ",".join(filed["lanes"]),
        # THE ERA OF RECORD [R1] — the one the FILING named, with the window
        # it means and the count of campaigns measured inside it.
        "arm_era": filed_era, "era_cut_iso": ERA_CUT_ISO,
        # ms, not iso: the holdout bound is the cut PLUS ONE MILLISECOND and
        # an iso string would print it as the cut itself.
        "era_window_lo_ms": era_window(filed_era)[0],
        "era_window_hi_ms": era_window(filed_era)[1],
        "era_first_entry_ms": int(min(t.entry_ms for t in book)),
        "era_last_entry_ms": int(max(t.entry_ms for t in book)),
        "era_note": era_note(filed_era),
        "prior_pct": rec["prior_pct"], "n": len(book),
        "expectancy_r": r6(float(np.mean(rs))), "net_r": r4(sum(rs)),
        "panel_name": panel_name(panel), "n_panel_assets": len(panel),
        "assets_present": len(set(ac)),
        "ruler": ("VS ZERO (one-sample asset-cluster)" if base is None else
                  "TWO-SAMPLE (the arm CHANGES the campaign set)" if two
                  else "PAIRED (the arm rides inside the set)"),
        "ruler_commissioned": ruler, "ruler_is_two_sample": two,
        "set_changes_measured": changes,
        **_ci_cols(ci, ""), "p_one_sided": r6(ci["p_one_sided"]),
        "verdict": _verdict(ci),
        **_ci_cols(ci_p, "paired_"), **_ci_cols(ci_2, "two_sample_"),
        **extra,
        "ear_expectancy_r": r6(ear_pt_book),
        "ear_base_expectancy_r": r6(ear_pt_base),
        **_ci_cols(ear_ci, "ear_"),
        "ear_p_one_sided": r6(ear_ci["p_one_sided"]),
        "ear_verdict_would_be": _verdict(ear_ci),
        # draws where a book held NONE of the drawn assets are NaN and the
        # lineage's _ci_from drops them silently; the count rides the row.
        "ear_n_finite_draws": int(np.sum(np.isfinite(ear_draws))),
        "sens_ear_ci_lo": r6(ear_sci["lo"]),
        "sens_ear_ci_hi": r6(ear_sci["hi"]),
        "co_headlines_disagree": bool(_verdict(ear_ci) != _verdict(ci)),
        "ear_ci_is_new": EAR_CI_IS_NEW,
        "verdict_carried_by": f"{LEAN_TAG} " + LEAN_PANEL_VERDICT,
        "scored_in_family": bool(scored_in_family),
        **{k: v for k, v in lo_.items() if not k.startswith("_")},
        # THE LOAO LINE OF RECORD — the count the FILING named before the
        # look; the other count rides beside it and gates nothing.
        "loao_line_of_record": filed["loao_line"],
        "loao_above_of_record": int(
            lo_["loao_excluding_above"] if filed["loao_line"] == "lineage"
            else lo_["loao_above_excl_zero_campaign_panels"]),
        "loao_clears_line_of_record": bool(
            lo_["loao_clears_above_half"] if filed["loao_line"] == "lineage"
            else lo_["loao_clears_excl_zero_campaign_panels"]),
        **dd,
        "seed": s0, "n_boot": int(n_boot),
        "sens_seed": s1, "sens_ci_lo": r6(sci["lo"]),
        "sens_ci_hi": r6(sci["hi"]),
        "sens_p_one_sided": r6(sci["p_one_sided"]),
        "sens_verdict": _verdict(sci), "sens_loao_line": slo["loao_line"],
        "sens_loao_seed": slo["loao_seed"],
        "verdict_stable_across_seeds": bool(_verdict(sci) == _verdict(ci)),
        "seed_note": f"{LEAN_TAG} L8: " + LEANS["L8"],
        "registration_seq": rec["seq"],
        "registration_sha256": rec["sha256"],
        "book_sha256": _book_sha(book), "base_sha256": _book_sha(base),
        "book_gate_attested": bool(isinstance(book, Book) and book.spec),
        "book_window_lo_ms": (getattr(book, "spec", None) or {}).get("lo_ms"),
        "book_window_hi_ms": (getattr(book, "spec", None) or {}).get("hi_ms"),
        "registration_root_is_canonical":
            head["registration_root_is_canonical"],
        "registry_len": head["registry_len"],
        "registry_head": head["registry_head"],
        "registry_head_pinned": head["registry_head_pinned"],
        "registry_pin": head["registry_pin"],
        "registry_pin_covers_seq": head["registry_pin_covers_seq"],
        "note": note,
    }
    log(f"  SCORED {reg_id} arm {filed['arm']!r} · registry_len "
        f"{head['registry_len']} · registry_head {head['registry_head']} · "
        f"pinned={head['registry_head_pinned']} · canonical="
        f"{head['registration_root_is_canonical']}")
    return row


def reference_row(base: list, seed: int = SEED, n_boot: int = N_BOOT) -> dict:
    """`(reference)  CARD v6 vs zero` — the known control through the same
    bar.  Not an acceptance test, excluded from m, needs no registration —
    and for that very reason it accepts THE CONTROL ONLY: a Book from
    `run_cell_n` whose provenance is card v6 / v6 roles on a CLASSIC5 subset.
    A registered ROW is made by `score()` and its gate, or not at all.

    SAID PLAINLY: the bare rulers (`co_headline`, `headline_n`, `loao_n`,
    `cluster_boot_ear*`) are public and UNGATED.  The gate stands at the two
    doors — where a BOOK is obtained (`run_cell_n`) and where a ROW is made
    (`score`); a caller who hands a ruler a book obtained elsewhere has left
    this module's law, and only caller discipline holds there."""
    stray = sorted({t.symbol for t in base} - set(CLASSIC5))
    sp = getattr(base, "spec", None)
    if stray or not isinstance(base, Book) or not sp \
            or sp.get("ride") != CONTROL_RIDE or sp.get("arm") != "(control)":
        raise SystemExit(
            f"HALT: reference_row is the CLASSIC5 control's — a Book from "
            f"run_cell_n(CONTROL_CARD, V6_ROLES, <CLASSIC5 subset>); got "
            f"{'assets ' + str(stray) if stray else 'a book with no control provenance'}"
            f". Every other book goes through score().")
    s0, s1 = _seed_pair(seed)
    rs = [t.net_r for t in base]
    ac = [t.symbol for t in base]
    ci = _ci_from(cluster_boot(rs, ac, seed=s0, n_boot=n_boot),
                  float(np.mean(rs)))
    sci = _ci_from(cluster_boot(rs, ac, seed=s1, n_boot=n_boot),
                   float(np.mean(rs)))
    ear = _ci_from(cluster_boot_ear(rs, ac, seed=s0, n_boot=n_boot),
                   ear_expectancy(rs, ac))
    lo_ = loao_n(base, None, CLASSIC5, seed=s0, label="(reference)",
                 n_boot=n_boot)
    return {"registration": "(reference)", "arm": "CARD v6 vs zero",
            "prior_pct": None, "n": len(base),
            "expectancy_r": r6(float(np.mean(rs))), "net_r": r4(sum(rs)),
            "panel_name": "CLASSIC5", "n_panel_assets": len(CLASSIC5),
            "assets_present": len(set(ac)), "ruler": "vs zero",
            **_ci_cols(ci, ""), "p_one_sided": r6(ci["p_one_sided"]),
            "verdict": _verdict(ci),
            "ear_expectancy_r": r6(ear["point"]), **_ci_cols(ear, "ear_"),
            "ear_p_one_sided": r6(ear["p_one_sided"]),
            "ear_verdict_would_be": _verdict(ear),
            "ear_ci_is_new": EAR_CI_IS_NEW,
            **{k: v for k, v in lo_.items() if not k.startswith("_")},
            "seed": s0, "n_boot": int(n_boot), "sens_seed": s1,
            "sens_ci_lo": r6(sci["lo"]), "sens_ci_hi": r6(sci["hi"]),
            "sens_p_one_sided": r6(sci["p_one_sided"]),
            "sens_verdict": _verdict(sci),
            "verdict_stable_across_seeds": bool(_verdict(sci) == _verdict(ci)),
            "scored_in_family": False,
            "note": "not an acceptance test; excluded from m"}


def finish_family(rows: list[dict], family_m: int = FAMILY_M,
                  canonical_only: bool = True) -> pd.DataFrame:
    """THE BAR, ONCE THE FAMILY IS WHOLE [LEAN L7].

    ONE fixed bar q/m on every scored row — no ranks, no step-up — so each
    registration passes or fails ON ITS OWN p.  m is the DECLARED family size
    (the contract's six, fixed before the look): running FEWER tests does not
    loosen the bar, and running MORE than were declared HALTs.  One scored arm
    per registration [F-C5-n: TC5 paid m=3 for two registrations].  A scored
    row vouched for by a THROWAWAY registry (`registration_root_is_canonical`
    False) HALTs unless `canonical_only=False` — which only a fixture says."""
    d = pd.DataFrame(rows)
    sc = d[d["scored_in_family"].astype(bool)]
    m_run = int(len(sc))
    if canonical_only and "registration_root_is_canonical" in sc.columns:
        off = sorted(sc.loc[sc["registration_root_is_canonical"].eq(False),
                            "registration"])
        if off:
            raise SystemExit(
                f"HALT: {off} were scored under a registry that is NOT "
                f"{REG_DIR} — a throwaway registry fills no slot in m.")
    dup = sorted(sc["registration"][sc["registration"].duplicated()].unique())
    if dup:
        raise SystemExit(f"HALT: {dup} hold more than ONE scored arm — each "
                         f"registration owns exactly one slot in m.")
    if m_run > family_m:
        raise SystemExit(f"HALT: {m_run} scored tests against a declared "
                         f"family of m={family_m}.")
    bar = FDR_Q / family_m
    d["fdr_m_declared"] = int(family_m)
    d["fdr_m_tests_actually_run"] = m_run
    d["fdr_bar_q_over_m"] = r6(bar)
    d["clears_bh_bar"] = [
        (None if not r_["scored_in_family"]
         else bool(r_["p_one_sided"] is not None
                   and r_["p_one_sided"] <= bar))
        for _, r_ in d.iterrows()]
    d["fdr_note"] = (
        f"{LEAN_TAG} L7: {LEANS['L7']} m = {family_m} DECLARED, {m_run} "
        f"run; q = {FDR_Q}, bar = q/m = {bar:.6f}; min attainable p = "
        f"1/{N_BOOT + 1}. The verdict column is CI-based; clears_bh_bar is a "
        f"SEPARATE column and both are reported.")
    return d


# ═══════════════════════════════════════════ THE WARRANTY, LENS-AWARE [TC6V-a]
LENS_MS = {"5m": 300_000, "1h": MS_1H, "4h": MS_4H, "12h": 12 * MS_1H,
           "1d": MS_1D, "1w": 7 * MS_1D}


def lens_edge(hi_ms: int, lens: str) -> int:
    """CLOSE time of the last bar of `lens` that is closed at the corridor
    end.  1w is MONDAY-anchored [L1]; every other lens sits on the epoch grid.
    This is the corridor-IMPLIED edge — "no bar of this lens closing after
    this instant was readable" — and a lane whose own tape ends earlier passes
    its measured edge to `stamp_n` instead."""
    if lens not in LENS_MS:
        raise SystemExit(f"HALT: unknown lens {lens!r}; one of {list(LENS_MS)}")
    step = LENS_MS[lens]
    off = MONDAY_EPOCH_OFFSET_MS if lens == "1w" else 0
    return ((int(hi_ms) + 1 - off) // step) * step + off


def stamp_n(df: pd.DataFrame, meta: dict, lens: str = "4h",
            lens_last_closed_ms: int | None = None) -> pd.DataFrame:
    """`tierc8.stamp` — its four columns UNCHANGED, because F-KEY demands
    `as_of_last_closed_4h` on every table — plus the lens and the panel:

        as_of_lens             the lens the row's numbers were measured on
        as_of_last_closed_bar  the last CLOSED bar of THAT lens the row could
                               see (close time, ISO)
        as_of_panel / as_of_n_assets   which declared panel
        as_of_substrate        the frozen snapshot's name

    WHAT WOULD MAKE THIS WRONG: stamping a 5m or 1d table with the 4h edge
    only — a daily row would then claim knowledge of a day that has not
    closed — or stamping the wall clock."""
    d = T8.stamp(df, meta)
    hi = _iso_ms(meta["last_closed_4h_close"]) - 1
    edge = (int(lens_last_closed_ms) if lens_last_closed_ms is not None
            else lens_edge(hi, lens))
    if edge > hi + 1:
        raise SystemExit(f"HALT: a {lens} as-of edge {iso(edge)} AFTER the "
                         f"corridor end {meta['last_closed_4h_close']}.")
    d["as_of_lens"] = lens
    d["as_of_last_closed_bar"] = iso(edge)
    d["as_of_panel"] = meta.get("panel_name", "CLASSIC5")
    d["as_of_n_assets"] = int(meta.get("n_assets", len(CLASSIC5)))
    d["as_of_substrate"] = meta.get("substrate", substrate()["substrate"])
    return d


AS_OF_COLUMNS = ("as_of_last_closed_4h", "as_of_panel_start",
                 "as_of_span_days", "warranty", "as_of_lens",
                 "as_of_last_closed_bar", "as_of_panel", "as_of_n_assets",
                 "as_of_substrate")


def make_put(root: Path, meta: dict, lens: str = "4h"):
    """The lineage's `put` closure, lens-aware.  Returns (put, W, K, SK):
    shas, declared keys, skipped-empty names — the manifest's three blocks."""
    W: dict[str, str] = {}
    K: dict[str, list] = {}
    SK: list[str] = []

    def put(df, name: str, key: list, lens_: str | None = None,
            lens_last_closed_ms: int | None = None,
            meta_: dict | None = None):
        """`meta_` = THIS table's own corridor meta, when it is not the
        run's (a 17-asset table inside a CLASSIC5 build must not be stamped
        as_of_panel=CLASSIC5).  A frame that arrives already stamped — a
        table whose ROWS belong to different panels — is written as is."""
        if df is None or not len(df):
            SK.append(name)
            log(f"    (skipped empty: {name})")
            return
        d = df.copy()
        if "as_of_lens" not in d.columns:
            d = stamp_n(d, meta_ or meta, lens_ or lens, lens_last_closed_ms)
        d.attrs = {}
        d.columns = [str(c) for c in d.columns]
        W[name] = write_table(d, name, key, root)
        K[name] = key
    return put, W, K, SK


# ════════════════════════════════════ THE CHECKS OTHER TC10 BUILDERS REUSE
def grid_whole(declared, written: pd.DataFrame, cell_col: str = "cell",
               require_cols: tuple = (), require_false: tuple = (),
               label: str = "grid") -> tuple[bool, list[str]]:
    """F-GRID's helper — EVERY GRID WHOLE.  `declared` is the commission's
    LITERAL cell list; `written` is the table as filed.  Two objects, never
    one counted twice: exact set equality, no duplicate, no extra, every
    required column present and non-null, every collar flag False on EVERY
    row."""
    ok, lines = True, []
    dec = [str(c) for c in declared]
    if cell_col not in written.columns:
        return False, [f"[BAD] {label}: no `{cell_col}` column"]
    got = [str(c) for c in written[cell_col]]
    miss = sorted(set(dec) - set(got))
    extra = sorted(set(got) - set(dec))
    dups = sorted({c for c in got if got.count(c) > 1})
    ddec = sorted({c for c in dec if dec.count(c) > 1})
    g = not (miss or extra or dups or ddec) and len(got) == len(dec)
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] {label}: declared {len(dec)} "
                 f"cells, written {len(got)}; missing {miss or 'none'}, "
                 f"undeclared {extra or 'none'}, duplicated "
                 f"{(dups + ddec) or 'none'}")
    for c in require_cols:
        g = c in written.columns and bool(written[c].notna().all())
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] {label}: column `{c}` "
                     f"present and non-null on every row")
    for c in require_false:
        g = c in written.columns and not bool(written[c].astype(bool).any())
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] {label}: `{c}` is False on "
                     f"every row (no promotion)")
    return bool(ok), lines


def check_keys(root: Path, manifest: dict | None = None,
               need_cols: tuple = AS_OF_COLUMNS) -> tuple[bool, list[str]]:
    """F-KEY's TOTALITY over one output root: every parquet has a declared
    key in the manifest, no key duplicates, every table carries EVERY as-of
    column (the four of tierc8.stamp AND the lens-aware five)."""
    root = Path(root)
    man = manifest if manifest is not None else json.loads(
        (root / "build_manifest.json").read_text())
    keys = man["keys"]
    stems = sorted(p.stem for p in root.glob("*.parquet"))
    und = [s for s in stems if s not in keys]
    ghost = [s for s in keys if s not in stems]
    dup_bad, asof_bad = [], []
    for s_ in stems:
        d = pd.read_parquet(root / f"{s_}.parquet")
        if s_ in keys and int(d.duplicated(subset=keys[s_]).sum()):
            dup_bad.append(s_)
        lack = [c for c in need_cols if c not in d.columns]
        if lack or (len(d) and d[list(set(need_cols) & set(d.columns))]
                    .isna().any().any()):
            asof_bad.append(f"{s_}:{lack or 'null stamp'}")
    ok = bool(stems) and not (und or ghost or dup_bad or asof_bad)
    return ok, [
        f"[{'OK ' if stems and not und else 'BAD'}] TOTALITY: {len(stems)} "
        f"parquets, undeclared: {und or 'none'}",
        f"[{'OK ' if not ghost else 'BAD'}] every declared key has its "
        f"table (ghosts: {ghost or 'none'})",
        f"[{'OK ' if not dup_bad else 'BAD'}] unique keys hold on every "
        f"table (dupes: {dup_bad or 'none'})",
        f"[{'OK ' if not asof_bad else 'BAD'}] all {len(need_cols)} as-of "
        f"columns on every table, none null (missing: {asof_bad or 'none'})"]


def check_det(root_a: Path, root_b: Path) -> tuple[bool, list[str]]:
    """F-DET's comparison of two output roots: same table SET, no content sha
    moved between the manifests, and an INDEPENDENT byte re-hash of every
    parquet pair (the shas are the build's claim; the bytes are the output)."""
    a, b = Path(root_a), Path(root_b)
    m1 = json.loads((a / "build_manifest.json").read_text())
    m2 = json.loads((b / "build_manifest.json").read_text())
    same = set(m1["sha"]) == set(m2["sha"]) and bool(m1["sha"])
    moved = sorted(k for k in m1["sha"] if m1["sha"][k] != m2["sha"].get(k))
    byte_bad = []
    for k in sorted(set(m1["sha"]) & set(m2["sha"])):
        pa, pb = a / f"{k}.parquet", b / f"{k}.parquet"
        if not (pa.exists() and pb.exists()) or (
                hashlib.sha256(pa.read_bytes()).hexdigest()
                != hashlib.sha256(pb.read_bytes()).hexdigest()):
            byte_bad.append(k)
    inp = m1.get("input_sha") == m2.get("input_sha")
    ok = same and not moved and not byte_bad
    lines = [
        f"[{'OK ' if same else 'BAD'}] same table set "
        f"({len(m1['sha'])} vs {len(m2['sha'])} tables)",
        f"[{'OK ' if not moved else 'BAD'}] no content sha moved "
        f"(moved: {moved or 'none'})",
        f"[{'OK ' if not byte_bad else 'BAD'}] independent byte re-hash of "
        f"every parquet pair (differs: {byte_bad or 'none'})",
        f"[{'OK ' if inp else 'BAD'}] both runs read the SAME input bytes "
        f"(input_sha {'equal' if inp else 'DIFFERS — the SUBSTRATE moved '}"
        f"{'' if inp else 'between the runs; that is drift, not the code'})"]
    return bool(ok and inp), lines


def input_sha(panel) -> dict:
    """sha256 of every input file the panel's book reads (4h klines +
    funding).  Rides the manifest so a moved number can be attributed: to the
    code, or to a substrate somebody topped up between two runs."""
    substrate()
    out = {}
    for s in panel:
        for p in (TB.KLINES / f"{s}_4h.parquet", TB.FUNDING / f"{s}.parquet"):
            out[f"{p.parent.name}/{p.name}"] = (
                hashlib.sha256(p.read_bytes()).hexdigest() if p.exists()
                else "ABSENT")
    return out


# ═══════════════════════════════════════════════════════════════════ THE RUN
CTRL_COLS = ("entry_ms", "exit_ms", "entry_px", "exit_px", "stop_px",
             "r_dist", "net_r", "gross_r", "fee_r", "funding_r", "mfe_r",
             "n_advances")


def ctrl_diff(got: pd.DataFrame, want: pd.DataFrame) -> tuple[bool, float, str]:
    """F-CTRL's comparator: two journals, sorted on (asset, entry_ms); equal
    count, EXACT zero on twelve numeric columns, identical exit reasons."""
    g = got.sort_values(["asset", "entry_ms"]).reset_index(drop=True)
    w = want.sort_values(["asset", "entry_ms"]).reset_index(drop=True)
    if len(g) != len(w):
        return False, float("inf"), f"campaigns {len(g)} vs {len(w)}"
    worst = max(float(np.max(np.abs(g[c].to_numpy(dtype=float)
                                    - w[c].to_numpy(dtype=float))))
                for c in CTRL_COLS) if len(g) else 0.0
    er = list(g["exit_reason"]) == list(w["exit_reason"])
    return bool(worst == 0.0 and er), worst, (
        f"n={len(g)} worst={worst:.3e} exit_reasons_identical={er}")


def control_window() -> tuple[int, int]:
    """The PARENT's window for the control: `tierc5.corridor()`'s (lo, hi),
    clamped to Stage D's as-of pin when the pin is the earlier of the two —
    the same clamp `corridor_n` applies, computed from the parent's side so
    F-CTRL compares two independently derived windows."""
    lo5, hi5, _ = T5.corridor()
    pin = stage_d_pin()
    return lo5, (min(hi5, pin - 1) if pin is not None else hi5)


def ctrl_prefix(live: pd.DataFrame, filed: pd.DataFrame,
                filed_edge_open_ms: int, label: str) -> tuple[bool, list[str]]:
    """F-CTRL's CROSS-PROCESS leg, PREFIX-ROBUST [tierc6_fixtures' repair].

    The referee is a journal FILED by another process on an EARLIER corridor.
    The corridor advances, so "the same number of campaigns" is the wrong
    claim (tierc9's `len(merged) == len(live)` went RED the day the cache
    moved: 196 filed, 200 live).  The honest claims, all four asserted:
      1. EVERY filed campaign is present live, on (asset, entry_ms);
      2. its entry_px / stop_px / r_dist are EXACT — the columns a
         multiplicative poison of the shared frame memo cannot leave invariant;
      3. a campaign the referee saw CLOSE closed live on the same bar, at the
         same price, for the same reason (only a `corridor_end` row may move);
      4. every LIVE-ONLY campaign entered AFTER the referee's last bar — an
         extra campaign inside the filed window is drift, not new data;
      5. on the campaigns the referee saw close, gross_r / fee_r / mfe_r are
         EXACT, and any net_r that moved moved by EXACTLY its funding_r (at
         the journal's own 6 dp).  net_r itself is NOT asserted across
         processes: the referees were filed while the estate's funding sat
         stale at 2026-08-15, Stage D topped it up, and a campaign that rode
         funding-free THEN is charged NOW.  That drift is the substrate's,
         it is printed campaign by campaign, and nothing else may hide in it.
    """
    ks = ["asset", "entry_ms"]
    lv = live.sort_values(ks).reset_index(drop=True)
    fl = filed.sort_values(ks).reset_index(drop=True)
    kl = set(zip(lv["asset"], lv["entry_ms"]))
    kf = set(zip(fl["asset"], fl["entry_ms"]))
    missing, extra = sorted(kf - kl), sorted(kl - kf)
    ok, lines = True, []
    g = not missing
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] {label}: every one of the "
                 f"{len(fl)} FILED campaigns is present in the live "
                 f"{len(lv)} ({len(missing)} missing {missing[:2]})")
    mg = lv.merge(fl, on=ks, suffixes=("", "_filed"))
    worst = max((float(np.max(np.abs(mg[c].to_numpy(float)
                                     - mg[c + "_filed"].to_numpy(float))))
                 for c in ("entry_px", "stop_px", "r_dist")),
                default=float("inf")) if len(mg) else float("inf")
    g = worst == 0.0
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] {label}: entry_px/stop_px/"
                 f"r_dist EXACT on the {len(mg)} shared campaigns (worst "
                 f"{worst:.3e}) — a poisoned shared load cannot pass this "
                 f"and the in-process zero-diff together")
    cl = mg[mg["exit_reason_filed"] != "corridor_end"]
    moved = cl[(cl["exit_ms"] != cl["exit_ms_filed"])
               | (cl["exit_reason"] != cl["exit_reason_filed"])
               | (cl["exit_px"].to_numpy(float)
                  != cl["exit_px_filed"].to_numpy(float))]
    g = len(moved) == 0 and len(cl) > 0
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] {label}: the {len(cl)} "
                 f"campaigns the referee saw CLOSE closed live on the same "
                 f"bar, price and reason ({len(moved)} moved)")
    px = max((float(np.max(np.abs(cl[c].to_numpy(float)
                                  - cl[c + "_filed"].to_numpy(float))))
              for c in ("gross_r", "fee_r", "mfe_r")),
             default=float("inf")) if len(cl) else float("inf")
    d_net = cl["net_r"].to_numpy(float) - cl["net_r_filed"].to_numpy(float)
    d_fun = (cl["funding_r"].to_numpy(float)
             - cl["funding_r_filed"].to_numpy(float))
    unexplained = int(np.sum(np.round(d_net + d_fun, 6) != 0.0))
    g = px == 0.0 and unexplained == 0
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] {label}: gross_r/fee_r/mfe_r "
                 f"EXACT on the {len(cl)} closed campaigns (worst {px:.3e}); "
                 f"net_r drift NOT explained by funding_r at 6 dp: "
                 f"{unexplained} campaign(s)")
    mv = cl[d_fun != 0.0]
    lines.append(
        f"[NB ] {label}: funding_r moved on {len(mv)} closed campaign(s)"
        + ("".join(f" — {r_.asset} {iso(int(r_.entry_ms))}: funding_r "
                   f"{r_.funding_r_filed} -> {r_.funding_r}, net_r "
                   f"{r_.net_r_filed} -> {r_.net_r}"
                   for r_ in mv.itertuples()) or "")
        + " [ATTRIBUTION: the referee rode on funding stale at 2026-08-15; "
          "Stage D's top-up supplied the stamps. Substrate drift, not code.]")
    early = [(a, iso(m)) for a, m in extra if m <= filed_edge_open_ms]
    g = not early
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] {label}: {len(extra)} live-only "
                 f"campaign(s) {[(a, iso(m)) for a, m in extra[:4]]}, all "
                 f"entered AFTER the referee's last bar "
                 f"{iso(filed_edge_open_ms)} (inside the filed window: "
                 f"{early or 'none'})")
    return bool(ok), lines


def run(root: Path) -> dict:
    """THE PANEL MODULE'S OWN BUILD — control artifacts ONLY.  It rides the
    known control on CLASSIC5 and nothing else; of the twelve unseen assets it
    reads BAR STAMPS AND FUNDING STAMPS, never a price, never a book."""
    t0 = time.time()
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    sub = substrate()
    lo, hi, cmeta = corridor_n(CLASSIC5)
    global AS_OF
    AS_OF = cmeta["last_closed_4h_close"]
    log(f"TIER-C10 PANEL · substrate {sub['substrate']} · corridor "
        f"{cmeta['panel_start']} → {AS_OF} ({cmeta['span_days']}d) · "
        f"seed {SEED} (sensitivity {SEED_LINEAGE})")
    for k in sorted(LEANS):
        log(f"  {LEAN_TAG} {k}: {LEANS[k]}")
    log(f"  {LEAN_TAG} panel-verdict: {LEAN_PANEL_VERDICT}")
    log(f"  UNSEEN12 source: {UNSEEN12_SOURCE}; unresolved names: "
        f"{list(UNSEEN12_UNRESOLVED) or 'none'}")

    # ═══ F-CTRL PRECONDITION — BEFORE ANYTHING [tierc9's commissioned order].
    if (lo, hi) != control_window():
        raise SystemExit(f"HALT: corridor_n(CLASSIC5) = ({lo}, {hi}) but "
                         f"tierc5.corridor() under Stage D's pin = "
                         f"{control_window()}.")
    base = run_cell_n(CONTROL_CARD, T9.V6_ROLES, CLASSIC5, lo, hi)
    want = T6.run_cell(V6.CARD_V6, lo, hi)
    ok, worst, why = ctrl_diff(journal_frame(base), journal_frame(want))
    if not ok:
        raise SystemExit(f"HALT: F-CTRL precondition — {why}; worst abs "
                         f"diff {worst:.3e} != 0.000e+00. Nothing runs.")
    log(f"  F-CTRL precondition: n={len(base)} worst={worst:.3e}  [HELD]")

    put, W, K, SK = make_put(root, cmeta, lens="4h")
    declared = CLASSIC5 + UNSEEN12
    # THE STAMP SAYS WHICH PANEL THE ROWS ARE TRUE OF.  The admission and the
    # funding tables hold every DECLARED asset, so they carry the measured
    # 17-asset corridor's edge and the declared panel's name and size — not
    # the CLASSIC5 meta the control tables carry.
    _, _, m17 = corridor_n(panel17())
    m_decl = dict(m17, panel_name=panel_name(declared),
                  n_assets=len(declared))
    adm = admission(declared)
    put(adm, "panel_admission", ["symbol"], meta_=m_decl)
    for r_ in adm[~adm["admitted"]].itertuples():
        log(f"    EXCLUDED {r_.symbol}: {r_.excluded_because}")
    put(pd.DataFrame([funding_coverage(s) for s in declared]),
        "panel_funding", ["symbol"], meta_=m_decl)
    parts = []
    for pn, pnl in (("CLASSIC5", CLASSIC5), ("PANEL17_MEASURED", panel17())):
        _, _, m_ = corridor_n(pnl)
        rows = []
        for s in pnl:
            rows.append({
                "panel": pn, "symbol": s, "n_assets": m_["n_assets"],
                "panel_start": m_["panel_start"],
                "panel_last_closed_4h_close": m_["last_closed_4h_close"],
                "first_4h": m_["per_asset_first_4h"][s],
                "floor_4h": m_["per_asset_floor_4h"][s],
                "last_4h_open": m_["per_asset_last_4h_open"][s],
                "n_4h": m_["per_asset_n_4h"][s],
                "scorable_bars_in_corridor":
                    m_["per_asset_scorable_bars_in_corridor"][s],
                "binds_the_edge": s in m_["binding_edge_assets"]})
        parts.append(stamp_n(pd.DataFrame(rows), m_, "4h"))   # ITS OWN panel
    put(pd.concat(parts, ignore_index=True), "panel_corridor",
        ["panel", "symbol"])
    put(pd.DataFrame([{"lean": k, "tag": LEAN_TAG, "text": v}
                      for k, v in sorted(LEANS.items())]
                     + [{"lean": "panel-verdict", "tag": LEAN_TAG,
                         "text": LEAN_PANEL_VERDICT}]), "leans", ["lean"])
    put(journal_frame(base), "control_journal", ["asset", "entry_ms"])
    put(headline_n(base, "v6-control", CLASSIC5, seed=SEED),
        "control_headline", ["label", "group", "key", "aggregation"])
    ref = reference_row(base, seed=SEED)
    put(finish_family([ref]), "control_reference", ["registration", "arm"])
    lo_ = loao_n(base, None, CLASSIC5, seed=SEED, label="(reference)")
    put(pd.DataFrame(lo_["_per"]).assign(
        loao_line=lo_["loao_line"], loao_mode=lo_["loao_mode"],
        loao_seed=lo_["loao_seed"],
        loao_bar_above_half=lo_["loao_bar_above_half"]),
        "control_loao", ["dropped"])
    put(registration_table() if REG_DIR.exists() else None,
        "registrations_filed", ["registration"])

    man = {
        "seed": SEED, "seed_sensitivity": SEED_LINEAGE,
        "stage": "TIER-C10 · PANEL MACHINERY", "as_of": AS_OF,
        "substrate": sub["substrate"],
        "corridor": {k: v for k, v in cmeta.items()
                     if k not in VOLATILE_META},
        "corridor_warranty": "every table carries the four tierc8.stamp "
                             "columns AND the five lens-aware columns",
        "bootstrap_seed_note": (
            f"every ruler here is seeded EXPLICITLY with {SEED}; the "
            f"lineage seed {SEED_LINEAGE} rides as the sensitivity block "
            f"{LEAN_TAG} L8. No default-argument seed is relied on."),
        "leans": dict(LEANS, **{"panel-verdict": LEAN_PANEL_VERDICT}),
        "unseen12_source": UNSEEN12_SOURCE,
        "unseen12": list(UNSEEN12),
        "unseen12_unresolved_names": list(UNSEEN12_UNRESOLVED),
        "panel17_declared": list(PANEL17),
        "panel17_measured": list(panel17()),
        "family_m": FAMILY_M, "fdr_bar": r6(FDR_Q / FAMILY_M),
        # THE ERAS [R1] — printed so the BUILD doc quotes the window, never
        # a typed date.  In MILLISECONDS (None = open): the holdout era
        # begins at the cut PLUS ONE, and an iso string would print that
        # instant as the cut itself.
        "era_cut": ERA_CUT_ISO, "era_cut_ms": ERA_CUT_MS,
        "eras": {e: {"first_ms": era_window(e)[0],
                     "last_ms": era_window(e)[1], "note": era_note(e)}
                 for e in ERAS},
        # the registry's HEAD at build time — None until a text is filed.
        # The BUILD doc pins it from here [WITNESS_LAW].
        "registry": registry_head() if REG_DIR.exists() else None,
        "registry_witness_law": WITNESS_LAW,
        "counts": {"control_n": len(base),
                   "control_net_r": r4(sum(t.net_r for t in base)),
                   "control_worst_abs_diff_vs_tierc6": worst},
        "input_sha": input_sha(CLASSIC5),
        "sha": W, "keys": K, "skipped_empty": SK,
    }
    (root / "build_manifest.json").write_text(
        json.dumps(man, indent=2, sort_keys=True, default=str))
    log(f"  manifest → {root / 'build_manifest.json'}  "
        f"({round(time.time() - t0, 1)}s)")
    return man


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--rerun", action="store_true")
    a = ap.parse_args()
    run((OUT_RERUN if a.rerun else OUT) / PANEL_SUB)
