#!/usr/bin/env python
"""TIER-C11 · STAGE H — HARVEST AND TAKE-PROFIT TIED TO RANGE EVENTS: the
P-TP-RNG books [LEANS L-H.1, L-1.5, L-1.3, L-R.2; AM-6 (s2), AM-7].

Contract of record: exchange/queue/2026-09-24_TC11_APOLLO.md (sha256 bb38e016…,
STEP Q b9ed953).  Executor HEPHAESTUS; seed 20260924 (this stage draws nothing).
Readings of record: research_outputs/tierc11/LEANS.md (frozen) and
LEANS_AMENDMENTS.md (AM-1..AM-7).  Registration of record: REGISTRATIONS.json
seq 9, P-TP-RNG [35%], paired vs v6, CLASSIC5, full corridor.

A RUNNER (L-F.2): it imports tierc11_nest (the range door) and hands the ride
PLAIN ARRAYS — the 12h as-of TP levels per 4h bar — through RD's TP hook.  It
computes BOOKS only: no CI, no p, no verdict word (the scorer reads the regbook
interface and decides).

WHAT IT BUILDS
  THE LEVELS [L-H.1].  For each CLASSIC5 asset and each 4h bar j of its frame:
  the 12h AS-OF bar at j's OPEN = the last 12h bar whose close <= open_j
  (`asof_12h_index`, inclusive: a 12h bar closing exactly at the 4h open is
  known).  If that bar's as-of state is IN_RANGE: level_long = top − 0.25 ×
  ATR_12h, level_short = bot + 0.25 × ATR_12h, with that bar's as-of box
  (N.range_facts: tierc10_census.asof_view, full precision, never Range.top)
  and ATR (engine.indicators.atr(h, l, c, 14) on the 12h tape — recursive, so
  the value at bar k uses only bars <= k).  EXPANSION or NONE -> NaN (no order;
  the trail runs).  Scales: the calibrated 12h pick (SCALE_PICKS.json, the
  pick of record) and the frozen 3.0 twin.
  THE RIDE.  RD.transform_book(v6 book, v6 card, v6 roles, walk=False,
  tp_of=TPLevels): RD's TP hook applies the near-side rule ((level − c[j−1])·d
  > 0), the entry-side guard ((level − entry)·d > 10 bps · entry), the fill
  max(level, o[j]) / min(level, o[j]), and the order STOP -> TP -> (close)
  BELL -> HARVEST -> TRAIL; `_account_chain` books whatever is open (1.0
  before the band harvest, 0.5 after).  The ride is 4h-granular (the TP is a
  4h resting limit; the 1h walk only resolves instants and is not used).
  THE ARMS (regbooks/P-TP-RNG/<arm>.parquet + .json; STATUS.json):
    scored                    calibrated 12h, mode 'record', full corridor
    base                      the v6 book (the pairing base), full corridor
    tierE__tp_post_harvest    the rival: the TP rests only after the v6 harvest
    tierE__unguarded          without the entry-side guard (ii)
    tierE__frozen3            the frozen-3.0 12h scale (fully causal)
    tierE__tuning / __holdout the scored arm's era slices (era = entry CLOSE)
  THE IDENTITY LAW [L-1.5] is asserted on every paired arm before anything is
  written: the key set is v6's, n == len(v6), and every campaign the TP never
  filled carries v6's net_r, exit_ms and exit_reason at 0.000e+00
  (RD.identity_findings) — HALT otherwise.  A second, independent assertion:
  the per-bar audit's first fillable bar per campaign == each arm's TP exit.
  THE RE-RIDE RIVAL [L-1.5] is replay9's admission loop with the ride swapped
  for ride11(tp=...): a freed slot admits the next window's trigger.  Printed
  as a DISCLOSURE COUNT (new admissions, v6 campaigns not taken), Tier-E.
  STAGE TABLES (stage_h/, all Tier-E, collared, as-of stamped): tp_campaigns,
  tp_bars (every bar of every v6 campaign, both scales), tp_fills, tp_summary
  (the grid), tp_withheld, tp_exit_reasons, tp_reride, tp_picks; STAGE_H.md;
  STAGE_H_MANIFEST.json.

EXECUTOR SUB-READINGS (disclosed, printed in the lean block)
  SR-H1  the as-of 12h bar is the last with close <= the 4h OPEN (inclusive).
  SR-H2  box and ATR are that 12h bar's (as-of its close); state IN_RANGE =
         the as-of view's in_range (state4 == 2).
  SR-H3  4h-granular ride, no 1h walk; exit_close_ms = the exit 4h bar's close
         (for an intrabar STOP / TP exit the post-event close stamp; the L-R.5
         stamp of record rides beside as exit_stamp_ms = the bar's OPEN).
  SR-H4  a prior close exactly AT the level is not on the near side (RD's
         tie-break, measure zero).
  SR-H5  era slices by the entry bar's CLOSE (L-1.3); SCALE-IN-SAMPLE per
         campaign = any 12h read of the calibrated pick at a 4h open <= the
         era cut (N.scale_in_sample at the read instant).
  SR-H6  the re-ride rival re-runs tierc9.replay9's admission (first trigger
         per window, one position per asset) with ride11(tp=): only a
         DISCLOSURE, never an arm.
  AM-6 (s2)  on a TP exit bar mfe is capped at the fill price (RD).
  AM-7   haircut_net_r = net_r − fee_r × slip_bps_side / taker_bps_side with the
         stem's charter tier (E.fees(); A 2 · B 5 · C 10; taker 5.0).

REPAIR (stage-H verifier report, all MINOR; no reading moved, no book moved):
  the era-slice sidecars carry the identity counts OF THE SLICE (scope named),
  not the full arm's [finding 5]; on the unguarded twin the guard-withheld
  counts are labelled WOULD-WITHHOLD (the guard is off, those orders rested) in
  tp_withheld (guard_count_meaning), tp_campaigns
  (unguarded_guard_would_withhold_bars), its sidecar and the report [finding 6];
  STAGE_H.md prints tp_campaigns WHOLE (§12) [finding 7]; the manifest carries
  the file BYTE shas beside the content shas [builder-report error].

WHAT WOULD MAKE THIS WRONG: reading the 12h bar that CONTAINS the 4h open (a
bar closing after it — look-ahead); carrying a dead range's box into an
EXPANSION bar; admitting a new campaign into a slot a TP freed (the set would
move and the paired premise break); booking the TP on the full unit after the
harvest; a level inside 10 bps of entry resting.

Run:  export NAIAD_CACHE_DIR=$HOME/.cache/naiad/snapshots/tc11_20260925 PYTHONDONTWRITEBYTECODE=1
      ~/venvs/naiad/bin/python -B scripts/tierc11_stage_h.py               # canonical build
      ~/venvs/naiad/bin/python -B scripts/tierc11_stage_h.py --out-dir=DIR  # F-DET twin
      (DIR must be a direct child of research_outputs/tierc11/stage_h/_det_stage_h/,
       or of a `_det_stage_h/` directory OUTSIDE the repo tree)
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import sys
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
import tierc11_nest as N                    # noqa: E402  (the range door; imports the shim first)
import tierc11_ride as RD                   # noqa: E402
import tierc11_books as B                   # noqa: E402

import numpy as np                          # noqa: E402
import pandas as pd                         # noqa: E402

E = N.E
TP, T9, T5, TB = E.TP, E.T9, E.T5, E.TB
RC = T9.RC
iso = TB.iso

# ══════════════════════════════════════════════════════════ CONSTANTS OF RECORD
REG_ID = "P-TP-RNG"
STAGE = "TC11-H"
SEED = E.SEED                               # 20260924 — printed; nothing here draws
PIN_MS = E.PIN_MS
PIN_ISO = E.PIN_ISO
ERA_CUT_MS = E.ERA_CUT_MS
MS_4H = 14_400_000
MS_12H = 43_200_000
LENS_U = "12h"                              # "12h boundary for a 4h campaign" [L-H.1]
APPROACH_ATR = 0.25                         # "the approach (0.25 ATR)" [L-H.1]
GUARD_BPS = float(RD.TP_GUARD_BPS)          # 10 bps = the round-trip taker fee [L-H.1 (ii)]
if GUARD_BPS != 2.0 * float(RC.FEE_BPS_SIDE) or GUARD_BPS != 10.0:
    raise SystemExit("HALT: the TP guard is not the round-trip taker fee (10 bps) [L-H.1]")
SCALE_KINDS = ("calibrated", "frozen3.0")
CLASSIC5 = tuple(E.CLASSIC5)
CARD, ROLES = TP.CONTROL_CARD, T9.V6_ROLES
TP_REASON = RD.TP_REASON                    # 'tp'
COLLAR = {"tier": "TIER-E", "selection_not_a_result": "a SELECTION, not a result",
          "gates": "nothing"}               # L-1.4: every non-registered table
EXIT_REASONS = ("stop", "bell_12_89", "bell_89_316", "tp", "corridor_end")
# what the ride's `guard_withheld` count means per TP mode [verifier finding 6]:
# RD counts a near-side order failing the guard in EVERY mode; with the guard off
# ('unguarded') that order RESTED — it is a would-withhold count, not a withholding.
GUARD_MEANING = {"record": "withheld",
                 "post_harvest": "withheld",
                 "unguarded": "would-withhold (guard off: these near-side orders RESTED)"}
ERAS = ("full", "tuning", "holdout")
ASSETS_ALL = CLASSIC5 + ("ALL",)
WALL_LESSON = ("the wall-exit lesson (the NAMED RISK, REGISTRATIONS.json named_risk): P-WALL-1 "
               "(TC6) — exit the remainder on a close within 0.25 ATR of the profit-side 12h "
               "champion wall — paired Δ −0.0331, tail_exit_ratio 0.9329: it lost BY CUTTING THE "
               "TAIL. A take-profit near a structural level cuts the tail the card lives on.")

# the arms: (arm, kind, scale_kind, tp mode, era_scope, book key)
ARMS = (
    ("scored", "scored", "calibrated", "record", "full", "scored"),
    ("base", "base", None, None, "full", "base"),
    ("tierE__tp_post_harvest", "tierE", "calibrated", "post_harvest", "full", "tp_post_harvest"),
    ("tierE__unguarded", "tierE", "calibrated", "unguarded", "full", "unguarded"),
    ("tierE__frozen3", "tierE", "frozen3.0", "record", "full", "frozen3"),
    ("tierE__tuning", "tierE", "calibrated", "record", "tuning", "scored"),
    ("tierE__holdout", "tierE", "calibrated", "record", "holdout", "scored"),
)
# the TP books ridden: book key -> (scale_kind, mode)
TP_BOOKS = {"scored": ("calibrated", "record"),
            "tp_post_harvest": ("calibrated", "post_harvest"),
            "unguarded": ("calibrated", "unguarded"),
            "frozen3": ("frozen3.0", "record")}
BOOK_KEYS = ("base",) + tuple(TP_BOOKS)     # the summary grid's books

REQ_COLS = ("symbol", "entry_ms", "entry_close_ms", "direction", "entry_px", "stop_px", "r_dist",
            "exit_close_ms", "exit_reason", "net_r", "gross_r", "fee_r", "funding_r",
            "haircut_net_r", "era", "lane")
REQ_INT = ("entry_ms", "entry_close_ms", "exit_close_ms")
REQ_FLOAT = ("entry_px", "stop_px", "r_dist", "net_r", "gross_r", "fee_r", "funding_r",
             "haircut_net_r")
REQ_STR = ("symbol", "exit_reason", "era", "lane")
BOOK_SHA_LAW = ("sha256 of the UTF-8 canonical CSV of the 16 required columns in REQ order, rows "
                "sorted by (symbol, entry_close_ms) (mergesort), header = the column names joined "
                "by ',', one row per line joined by ',', '\\n' after every line (the last "
                "included); int columns as str(int), direction as str(int), floats as "
                "repr(float) (shortest round-trip), strings verbatim (no ',' or newline allowed)")

OUT = E.OUT / "stage_h"
REGBOOK_ROOT = E.OUT / "regbooks"
REGBOOKS = REGBOOK_ROOT / REG_ID
DET_ROOT = OUT / "_det_stage_h"
REPORT = "STAGE_H.md"
MANIFEST = "STAGE_H_MANIFEST.json"
STAGE_TABLES = {                            # name -> key
    "tp_campaigns": ["symbol", "entry_ms"],
    "tp_bars": ["scale_kind", "symbol", "entry_ms", "bar_open_ms"],
    "tp_fills": ["book", "symbol", "entry_ms"],
    "tp_summary": ["cell"],
    "tp_withheld": ["cell"],
    "tp_exit_reasons": ["cell"],
    "tp_reride": ["asset"],
    "tp_picks": ["asset"],
}
SOURCE = "scripts/tierc11_stage_h.py"

READINGS = (
    f"{E.LEAN_TAG} L-H.1 P-TP-RNG: v6's harvest law (50% at the opposing 89/316 band) is KEPT; at "
    "each 4h bar j after entry the 12h as-of state at j's OPEN (the last 12h bar closed <= open_j) "
    "— IN_RANGE: level = top − 0.25 × ATR_12h (long) / bot + 0.25 × ATR_12h (short); a resting "
    "limit for the REMAINDER (1.0 before the band harvest, 0.5 after) is live iff (i) the prior 4h "
    "close is on the near side and (ii) (level − entry)·d > 10 bps · entry; fill at max(level, "
    "o[j]) long / min(level, o[j]) short; EXPANSION or NONE -> no TP, the trail runs; same-bar order "
    "STOP -> TP -> (close) BELL -> HARVEST -> TRAIL. Rival twin 'tp-post-harvest' (TP only after the "
    "harvest, the 0.5 runner); the unguarded twin (no (ii)) and the guard-withheld counts printed.",
    f"{E.LEAN_TAG} L-1.5 PAIRED = the v6 campaign set TRANSFORMED: same arm, entry, stop, R; a slot a "
    "TP frees admits NO new entry (the re-ride rival is a disclosure count); the IDENTITY law — every "
    "campaign the TP never filled carries v6's net_r, exit_ms and exit_reason exactly — asserted "
    "over the whole book before any regbook is written.",
    f"{E.LEAN_TAG} L-1.3 era = the entry bar's CLOSE (E.era_of(entry_close_ms)); tuning closes <= "
    f"{E.ERA_CUT_ISO}; the registration names no era -> scored on the FULL corridor, tuning and "
    "holdout slices printed beside as Tier-E.",
    f"{E.LEAN_TAG} L-R.2 SCALE-IN-SAMPLE: the calibrated 12h pick (tuning-era calibration) makes "
    "every calibrated read at an instant <= the era cut structurally in-sample; the holdout slice "
    "(the only slice with a causal scale) and the frozen-3.0 twin (fully causal) print beside; pick "
    "stability per CLASSIC5 asset printed (tp_picks).",
    f"{E.LEAN_TAG} AM-6 (s2) on a TP exit bar mfe is capped at the FILL price (tierc11_ride).",
    f"{E.LEAN_TAG} AM-7 haircut_net_r = net_r − fee_r × (slip_bps_side / taker_bps_side), fee_r the "
    "ride's own taker fee over EVERY fill (entry, harvest, final exit), slip the stem's charter tier "
    "(A 2 · B 5 · C 10 bps/side, fee_schedule.json), taker 5.0; funding stays in (net_r carries it).",
    f"{E.LEAN_TAG} SR-H1 the as-of 12h bar = the last 12h bar with close <= the 4h bar's OPEN "
    "(inclusive: a 12h bar closing exactly at the 4h open is known at it).",
    f"{E.LEAN_TAG} SR-H2 box and ATR are the as-of 12h bar's own (tierc10_census.asof_view via "
    "N.range_facts, full precision; ATR = engine.indicators.atr(h, l, c, 14) on the whole 12h tape, "
    "recursive); IN_RANGE = the as-of view's in_range (state4 == 2).",
    f"{E.LEAN_TAG} SR-H3 the TP ride is 4h-granular (walk=False; the 1h walk resolves instants only); "
    "regbook exit_close_ms = the exit 4h bar's CLOSE (for an intrabar STOP or TP exit the post-event "
    "close stamp); exit_stamp_ms beside = the L-R.5 stamp of record (the bar's OPEN for an intrabar "
    "exit, the close for bell / corridor_end).",
    f"{E.LEAN_TAG} SR-H4 a prior close exactly AT the level is NOT on the near side (tierc11_ride's "
    "tie-break, measure zero).",
    f"{E.LEAN_TAG} SR-H5 SCALE-IN-SAMPLE per campaign = any calibrated 12h read at a 4h OPEN <= the "
    "era cut among the bars the arm rode (N.scale_in_sample at the read instant); frozen 3.0 never.",
    f"{E.LEAN_TAG} SR-H6 the re-ride rival = tierc9.replay9's admission loop (first trigger per "
    "window, one position per asset, struct_stop_4h railed 1.0 ATR) with the ride swapped for "
    "ride11(tp=); it reproduces the v6 book exactly with tp=None (asserted) and is a DISCLOSURE "
    "count only.",
)


def _halt(msg: str) -> None:
    raise SystemExit(f"HALT: {msg}")


# ══════════════════════════════════════════════════════════════ THE LEVELS
_FACTS: dict = {}


def facts_of(sym: str, scale_kind: str) -> dict:
    """N.range_facts(sym, '12h', scale_kind) — plain arrays (memoised)."""
    k = (sym, scale_kind)
    if k not in _FACTS:
        _FACTS[k] = N.range_facts(sym, LENS_U, scale_kind)
    return _FACTS[k]


def asof_12h_index(close12_ms: np.ndarray, instants_ms) -> np.ndarray:
    """SR-H1: the LAST 12h bar whose CLOSE is at or before the instant (inclusive);
    -1 before the first close.  A 12h bar still forming at the instant is never
    read."""
    return np.searchsorted(np.asarray(close12_ms, dtype=np.int64),
                           np.asarray(instants_ms, dtype=np.int64), side="right") - 1


def levels_from_facts(open4_ms, facts: dict) -> dict:
    """THE TP LEVELS [L-H.1] per 4h bar (aligned to `open4_ms`), from plain arrays.
    NaN = no order (EXPANSION / NONE / no 12h bar closed yet)."""
    o4 = np.asarray(open4_ms, dtype=np.int64)
    close12 = np.asarray(facts["close_ms"], dtype=np.int64)
    k = asof_12h_index(close12, o4)
    ok = k >= 0
    ks = np.where(ok, k, 0)
    inr = ok & np.asarray(facts["in_range"], dtype=bool)[ks]
    nan = np.full(len(o4), np.nan)
    top = np.where(inr, np.asarray(facts["top"], dtype=float)[ks], nan)
    bot = np.where(inr, np.asarray(facts["bot"], dtype=float)[ks], nan)
    atr = np.where(ok, np.asarray(facts["atr"], dtype=float)[ks], nan)
    state4 = np.where(ok, np.asarray(facts["state4"], dtype=np.int64)[ks],
                      N.STATE4["NONE"]).astype(np.int64)
    with np.errstate(invalid="ignore"):
        lvl_l = np.where(inr, top - APPROACH_ATR * atr, nan)
        lvl_s = np.where(inr, bot + APPROACH_ATR * atr, nan)
    return {"k": k.astype(np.int64), "close12_ms": np.where(ok, close12[ks], -1).astype(np.int64),
            "state4": state4, "in_range": inr, "top": top, "bot": bot, "atr": atr,
            "level_long": lvl_l, "level_short": lvl_s}


def levels_for(scale_kind: str) -> dict:
    """{sym: levels} for CLASSIC5 on each asset's own 4h frame."""
    out = {}
    for s in CLASSIC5:
        f = T9.frame(s)["f"]
        out[s] = levels_from_facts(np.asarray(f.open_ms, dtype=np.int64), facts_of(s, scale_kind))
    return out


def tp_levels(lv: dict, mode: str) -> RD.TPLevels:
    return RD.TPLevels(lv["level_long"], lv["level_short"], mode=mode, guard_bps=GUARD_BPS)


# ══════════════════════════════════════════════════════════════ THE BOOKS
def ride_tp_book(base: list, lo: int, hi: int, levels: dict, mode: str) -> list:
    """L-1.5: the v6 campaign set transformed by the TP hook (nothing re-admitted)."""
    return RD.transform_book(base, CARD, ROLES, lo, hi, walk=False,
                             tp_of=lambda s: tp_levels(levels[s], mode))


def paired_premise(base: list, book: list, name: str) -> list[str]:
    kb = [(t.symbol, int(t.entry_ms)) for t in base]
    kn = [(t.symbol, int(t.entry_ms)) for t in book]
    out = []
    if len(kn) != len(kb) or set(kn) != set(kb) or len(set(kn)) != len(kn):
        out.append(f"PAIRED PREMISE {name}: key sets differ (n {len(kn)} vs base {len(kb)})")
    return out


def reride(lo: int, hi: int, levels: dict | None, mode: str = "record") -> list:
    """SR-H6: replay9's admission loop, the ride swapped for ride11(tp=)."""
    out = []
    for s in CLASSIC5:
        st = T9.frame(s)
        f = st["f"]
        lo_i, hi_i, _ = B.ride_bounds(s, ROLES, lo, hi)
        if hi_i < lo_i:
            continue
        _, cc = T9.card_candidates9(s, ROLES, lo_i, hi_i)
        cands = sorted(((ti, d, "card", a) for ti, d, a in cc),
                       key=lambda c: (c[0], -c[1], c[2]))
        open_until = -1
        for ti, d, kind, arm in cands:
            if ti <= open_until:
                continue
            entry_px, atr_sig = float(f.c[ti]), float(f.atr[ti])
            if not (np.isfinite(atr_sig) and atr_sig > 0):
                continue
            stp = RC.struct_stop_4h(st["pv4"], ti, entry_px, d, atr_sig,
                                    min_stop_atr=CARD.entry_rail_atr, forbidden=None)
            if stp is None or not (np.isfinite(stp.r_dist) and stp.r_dist > 0):
                continue
            tpl = None if levels is None else tp_levels(levels[s], mode)
            leg = RD.ride11(s, CARD, ROLES, d, ti, entry_px, stp.stop_px, stp.r_dist, hi_i,
                            tp=tpl)
            open_until = leg["exit_i"]
            out.append(RD.trade11(s, CARD, ROLES, d, arm_i=arm.arm_i, arm_ms=arm.arm_ms,
                                  disp=arm.disp, entry_i=ti, entry_ms=int(f.open_ms[ti]),
                                  entry_px=entry_px, stp=stp, atr_sig=atr_sig, leg=leg,
                                  lane=kind))
    return out


# ══════════════════════════════════════════════════════════ THE PER-BAR AUDIT
BAR_COLS = ("scale_kind", "symbol", "entry_ms", "direction", "bar_open_ms", "j_rel",
            "asof12_close_ms", "state12", "top12", "bot12", "atr12", "level", "prior_close",
            "bar_open_px", "bar_high", "bar_low", "near", "guard_ok", "touched",
            "harvested_before", "stop_bar", "live_record", "live_post_harvest", "live_unguarded",
            "fill_px", "scale_in_sample")


def bar_audit(base: list, levels: dict, scale_kind: str) -> pd.DataFrame:
    """Every bar j in (entry_i, v6 exit_i] of every v6 campaign — the TP arms ride
    v6's path exactly until they fill, so this is each arm's path up to its exit.
    Mode-free facts plus the three modes' liveness [L-H.1]."""
    rows = []
    labs = {s: N.scale_label(s, LENS_U, scale_kind) for s in CLASSIC5}
    for t in base:
        s, d, ti, xi = t.symbol, int(t.direction), int(t.entry_i), int(t.exit_i)
        f = T9.frame(s)["f"]
        lv = levels[s]
        e = float(t.entry_px)
        js = np.arange(ti + 1, xi + 1)
        L = (lv["level_long"] if d == 1 else lv["level_short"])[js]
        prior = np.asarray(f.c, float)[js - 1]
        fin = np.isfinite(L)
        with np.errstate(invalid="ignore"):
            near = fin & ((L - prior) * d > 0.0)
            guard = fin & ((L - e) * d > GUARD_BPS / 10_000.0 * e)
            hi_, lo_ = np.asarray(f.h, float)[js], np.asarray(f.l, float)[js]
            touched = fin & ((hi_ >= L) if d == 1 else (lo_ <= L))
        op = np.asarray(f.o, float)[js]
        fill = np.where(touched, np.maximum(L, op) if d == 1 else np.minimum(L, op), np.nan)
        hb = (t.harvest_i is not None) & (js > (t.harvest_i if t.harvest_i is not None else 1 << 62))
        stop_bar = (js == xi) & (t.exit_reason == "stop")
        inst = np.asarray(f.open_ms, dtype=np.int64)[js]
        for n_, j in enumerate(js):
            rows.append({
                "scale_kind": scale_kind, "symbol": s, "entry_ms": int(t.entry_ms), "direction": d,
                "bar_open_ms": int(inst[n_]), "j_rel": int(j - ti),
                "asof12_close_ms": int(lv["close12_ms"][j]),
                "state12": str(N.STATE4_NAMES[int(lv["state4"][j]) + 1]),
                "top12": float(lv["top"][j]), "bot12": float(lv["bot"][j]),
                "atr12": float(lv["atr"][j]), "level": float(L[n_]),
                "prior_close": float(prior[n_]), "bar_open_px": float(op[n_]),
                "bar_high": float(hi_[n_]), "bar_low": float(lo_[n_]),
                "near": bool(near[n_]), "guard_ok": bool(guard[n_]),
                "touched": bool(touched[n_]), "harvested_before": bool(hb[n_]),
                "stop_bar": bool(stop_bar[n_]),
                "live_record": bool(near[n_] and guard[n_]),
                "live_post_harvest": bool(near[n_] and guard[n_] and hb[n_]),
                "live_unguarded": bool(near[n_]),
                "fill_px": float(fill[n_]),
                "scale_in_sample": bool(N.scale_in_sample(labs[s], [int(inst[n_])])[0])})
    df = pd.DataFrame(rows, columns=list(BAR_COLS))
    for c in ("entry_ms", "bar_open_ms", "j_rel", "asof12_close_ms"):
        df[c] = df[c].astype(np.int64)
    df["direction"] = df["direction"].astype(np.int8)
    return df


LIVE_COL = {"record": "live_record", "post_harvest": "live_post_harvest",
            "unguarded": "live_unguarded"}


def audit_findings(base: list, bars: pd.DataFrame, book: list, mode: str, name: str) -> list[str]:
    """The build-time cross-check (HALT on any): per campaign, the audit's first
    fillable bar (live under `mode`, touched, not the v6 stop bar) is the book's TP
    exit bar with the audit's fill price; no such bar -> the book is v6's; and the
    ride's per-campaign counts equal the audit's over the bars the arm rode."""
    out = []
    bm = {(t.symbol, int(t.entry_ms)): t for t in book}
    live_c = LIVE_COL[mode]
    for (s, em), g in bars.groupby(["symbol", "entry_ms"], sort=True):
        t = bm[(s, int(em))]
        v = next(b for b in base if b.symbol == s and int(b.entry_ms) == int(em))
        fillable = g[g[live_c] & g["touched"] & ~g["stop_bar"]]
        if len(fillable):
            r = fillable.iloc[0]
            j = int(v.entry_i) + int(r["j_rel"])
            if t.exit_reason != TP_REASON or int(t.exit_i) != j or float(t.exit_px) != float(
                    r["fill_px"]):
                out.append(f"AUDIT {name} {s} {iso(int(em))}: audit fills at bar {iso(int(r['bar_open_ms']))} "
                           f"px {r['fill_px']!r}; the book exits {t.exit_reason} at bar "
                           f"{iso(int(t.exit_ms))} px {t.exit_px!r}")
            rode = g[g["j_rel"] <= int(r["j_rel"])]
        else:
            if t.exit_reason == TP_REASON or int(t.exit_i) != int(v.exit_i):
                out.append(f"AUDIT {name} {s} {iso(int(em))}: no fillable bar, but the book exits "
                           f"{t.exit_reason} at {iso(int(t.exit_ms))}")
            rode = g
        fin = np.isfinite(rode["level"].to_numpy(float))
        want = {"live": int(rode[live_c].sum()),
                "guard_withheld": int((fin & rode["near"] & ~rode["guard_ok"]).sum()),
                "far_side": int((fin & ~rode["near"]).sum()),
                "preharvest_withheld": (int((rode["near"] & rode["guard_ok"]
                                             & ~rode["harvested_before"]).sum())
                                        if mode == "post_harvest" else 0),
                "filled": int(t.exit_reason == TP_REASON)}
        got = {k: int(t.tp_counts[k]) for k in want}
        if got != want:
            out.append(f"AUDIT {name} {s} {iso(int(em))}: ride counts {got} != audit {want}")
    return out


# ══════════════════════════════════════════════════════════ THE REGBOOK FRAMES
def exit_stamp(exit_ms: int, reason: str) -> int:
    """L-R.5: an intrabar exit (stop, tp) at its bar's OPEN; a close event at its close."""
    return int(exit_ms) if reason in ("stop", TP_REASON) else int(exit_ms) + MS_4H


def haircut(net_r: float, fee_r: float, stem: str) -> tuple[float, float, str]:
    """AM-7: net_r − fee_r × slip_bps_side / taker_bps_side."""
    fz = E.fees()[stem]
    tk, sl = float(fz["taker_bps_side"]), float(fz["slippage_bps_side"])
    if tk != float(RC.FEE_BPS_SIDE):
        _halt(f"{stem}: taker {tk} != FEE_BPS_SIDE {RC.FEE_BPS_SIDE} [AM-7]")
    return float(net_r) - float(fee_r) * (sl / tk), sl, str(fz["slippage_tier"])


def book_rows(book: list, base_by: dict, bars: pd.DataFrame | None, levels: dict | None,
              scale_kind: str | None) -> pd.DataFrame:
    """One row per campaign in the regbook schema (+ extras)."""
    labs = ({s: N.scale_label(s, LENS_U, scale_kind) for s in CLASSIC5}
            if scale_kind is not None else None)
    picks = {s: (N.scale_of(s, LENS_U, scale_kind) if scale_kind is not None else np.nan)
             for s in CLASSIC5}
    rows = []
    for t in book:
        s, d = t.symbol, int(t.direction)
        ec = int(getattr(t, "entry_close_ms", int(t.entry_ms) + MS_4H))
        if ec != int(t.entry_ms) + MS_4H:
            _halt(f"{s} {iso(int(t.entry_ms))}: a v6-derived entry is not the 4h close")
        hc, sl, tier = haircut(float(t.net_r), float(t.fee_r), s)
        st = exit_stamp(int(t.exit_ms), t.exit_reason)
        rs = getattr(t, "exit_stamp_ms", None)
        if rs is not None and int(rs) != st:
            _halt(f"{s} {iso(int(t.entry_ms))}: the ride's exit stamp {rs} != the L-R.5 law {st}")
        r = {"symbol": s, "entry_ms": int(t.entry_ms), "entry_close_ms": ec, "direction": d,
             "entry_px": float(t.entry_px), "stop_px": float(t.stop_px),
             "r_dist": float(t.r_dist), "exit_close_ms": int(t.exit_ms) + MS_4H,
             "exit_reason": str(t.exit_reason), "net_r": float(t.net_r),
             "gross_r": float(t.gross_r), "fee_r": float(t.fee_r),
             "funding_r": float(t.funding_r), "haircut_net_r": hc,
             "era": str(E.era_of(ec)), "lane": str(t.lane),
             # ── extras ──────────────────────────────────────────────────────
             "exit_ms": int(t.exit_ms), "exit_px": float(t.exit_px), "exit_stamp_ms": st,
             "harvested": bool(t.harvested),
             "harvest_ms": (int(t.harvest_ms) if t.harvest_ms is not None else -1),
             "reached_1r": bool(t.reached_1r), "mfe_r": float(t.mfe_r),
             "funding_r_uncapped": float(t.funding_r_uncapped),
             "funding_ceiling_bound": bool(t.funding_ceiling_bound),
             "slip_bps_side": sl, "slippage_tier": tier}
        if base_by is not None:
            v = base_by[(s, int(t.entry_ms))]
            tc = t.tp_counts
            is_tp = t.exit_reason == TP_REASON
            j = int(t.exit_i)
            lv = levels[s]
            L = (lv["level_long"] if d == 1 else lv["level_short"])
            g = bars[(bars["symbol"] == s) & (bars["entry_ms"] == int(t.entry_ms))
                     & (bars["j_rel"] <= int(t.exit_i) - int(t.entry_i))]
            r.update({
                "acted_by": str(t.acted_by), "tp_fill": bool(is_tp),
                "tp_level": float(L[j]) if is_tp else float("nan"),
                "tp_asof12_close_ms": int(lv["close12_ms"][j]) if is_tp else -1,
                "tp_live_bars": int(tc["live"]), "tp_guard_withheld": int(tc["guard_withheld"]),
                "tp_far_side": int(tc["far_side"]),
                "tp_preharvest_withheld": int(tc["preharvest_withheld"]),
                "tp_fill_blocked_by_stop": int(tc["fill_blocked_by_stop"]),
                "v6_net_r": float(v.net_r), "v6_exit_reason": str(v.exit_reason),
                "v6_exit_ms": int(v.exit_ms), "delta_r": float(t.net_r) - float(v.net_r),
                "scale_kind": scale_kind, "scale_pick_12h": float(picks[s]),
                "pick_window_12h": str(labs[s]["pick_window"]),
                "stability_changed_12h": (None if labs[s]["stability_changed"] is None
                                          else bool(labs[s]["stability_changed"])),
                "scale_in_sample_12h": bool(g["scale_in_sample"].any())})
        rows.append(r)
    df = pd.DataFrame(rows)
    for c in REQ_INT + ("exit_ms", "exit_stamp_ms", "harvest_ms"):
        df[c] = df[c].astype(np.int64)
    df["direction"] = df["direction"].astype(np.int8)
    if base_by is not None:
        for c in ("tp_asof12_close_ms", "v6_exit_ms"):
            df[c] = df[c].astype(np.int64)
        df["stability_changed_12h"] = pd.array(df["stability_changed_12h"], dtype="boolean")
    return df.sort_values(["symbol", "entry_close_ms"], kind="mergesort").reset_index(drop=True)


def book_sha256(df: pd.DataFrame) -> str:
    """BOOK_SHA_LAW (see the constant)."""
    d = df[list(REQ_COLS)].sort_values(["symbol", "entry_close_ms"], kind="mergesort")
    lines = [",".join(REQ_COLS)]
    for row in d.itertuples(index=False):
        vals = []
        for c, v in zip(REQ_COLS, row):
            if c in REQ_FLOAT:
                vals.append(repr(float(v)))
            elif c in REQ_INT or c == "direction":
                vals.append(str(int(v)))
            else:
                sv = str(v)
                if "," in sv or "\n" in sv:
                    _halt(f"book_sha256: a string cell {sv!r} holds ',' or a newline")
                vals.append(sv)
        lines.append(",".join(vals))
    return hashlib.sha256(("\n".join(lines) + "\n").encode("utf-8")).hexdigest()


def fsum(x) -> float:
    return float(math.fsum(float(v) for v in x))


def d15_of(book_df: pd.DataFrame, base_df: pd.DataFrame) -> dict:
    """T5.d15 (tierc5.py:579) on the frames (symbol, entry_ms, net_r)."""
    def objs(df):
        return [SimpleNamespace(symbol=s, entry_ms=int(e), net_r=float(r))
                for s, e, r in zip(df["symbol"], df["entry_ms"], df["net_r"])]
    return T5.d15(objs(book_df), objs(base_df))


# ══════════════════════════════════════════════════════════════ THE STAGE TABLES
def _collar(df: pd.DataFrame) -> pd.DataFrame:
    d = df.copy()
    for k, v in COLLAR.items():
        d[k] = v
    return d


def _era_mask(df: pd.DataFrame, era: str) -> np.ndarray:
    return np.ones(len(df), bool) if era == "full" else (df["era"] == era).to_numpy()


def summary_grid(frames: dict) -> pd.DataFrame:
    """THE GRID [every grid whole]: book × era × asset (CLASSIC5 + ALL)."""
    base = frames["base"]
    rows = []
    for b in BOOK_KEYS:
        df = frames[b]
        for era in ERAS:
            for a in ASSETS_ALL:
                m = _era_mask(df, era) & ((df["symbol"] == a).to_numpy() if a != "ALL"
                                          else np.ones(len(df), bool))
                c = df[m]
                mb = _era_mask(base, era) & ((base["symbol"] == a).to_numpy() if a != "ALL"
                                             else np.ones(len(base), bool))
                cb = base[mb]
                n = len(c)
                r = {"cell": f"{b}|{era}|{a}", "book": b, "era": era, "asset": a, "n": n}
                if n:
                    j = c.merge(cb[["symbol", "entry_ms", "net_r"]], on=["symbol", "entry_ms"],
                                suffixes=("", "_v6"), how="left", validate="one_to_one")
                    dl = (j["net_r"] - j["net_r_v6"]).to_numpy(float)
                    dd = d15_of(c, cb)
                    r.update({"sum_net_r": fsum(c["net_r"]), "mean_net_r": fsum(c["net_r"]) / n,
                              "win_rate": float((c["net_r"] > 0).mean()),
                              "sum_haircut_net_r": fsum(c["haircut_net_r"]),
                              "mean_haircut_net_r": fsum(c["haircut_net_r"]) / n,
                              "n_tp": int((c["exit_reason"] == TP_REASON).sum()),
                              "sum_delta_r": fsum(dl), "mean_delta_r": fsum(dl) / n,
                              "tail_exit_ratio": (float(dd["tail_exit_ratio"])
                                                  if dd["tail_exit_ratio"] is not None
                                                  else float("nan"))})
                    r["nan_reason"] = ("" if np.isfinite(r["tail_exit_ratio"]) else
                                       "n < 10: the top decile is empty — the D15 tail ratio "
                                       "is undefined")
                else:
                    r.update({k: float("nan") for k in (
                        "sum_net_r", "mean_net_r", "win_rate", "sum_haircut_net_r",
                        "mean_haircut_net_r", "sum_delta_r", "mean_delta_r", "tail_exit_ratio")})
                    r["n_tp"] = 0
                    r["nan_reason"] = "n = 0 — no campaign in this cell"
                rows.append(r)
    cols = ["cell", "book", "era", "asset", "n", "n_tp", "sum_net_r", "mean_net_r", "win_rate",
            "sum_haircut_net_r", "mean_haircut_net_r", "sum_delta_r", "mean_delta_r",
            "tail_exit_ratio", "nan_reason"]
    df = pd.DataFrame(rows, columns=cols)
    df["n"] = df["n"].astype(np.int64)
    df["n_tp"] = df["n_tp"].astype(np.int64)
    return df


def withheld_grid(books: dict, bars: dict) -> pd.DataFrame:
    """book (the four TP books) × asset: the TP order counts over the bars each arm
    rode (RD's per-campaign tp_counts, summed) + the audit's level/no-level bars and
    the guard-withheld bars the price reached."""
    rows = []
    for b, (kind, mode) in TP_BOOKS.items():
        bk = books[b]
        bt = bars[kind]
        exit_rel = {(t.symbol, int(t.entry_ms)): int(t.exit_i) - int(t.entry_i) for t in bk}
        er = np.array([exit_rel[(s, int(e))] for s, e in zip(bt["symbol"], bt["entry_ms"])])
        rode = bt[bt["j_rel"].to_numpy() <= er]
        for a in ASSETS_ALL:
            ts = [t for t in bk if a == "ALL" or t.symbol == a]
            g = rode if a == "ALL" else rode[rode["symbol"] == a]
            fin = np.isfinite(g["level"].to_numpy(float))
            tc = {k: sum(int(t.tp_counts[k]) for t in ts)
                  for k in ("live", "guard_withheld", "far_side", "preharvest_withheld", "filled",
                            "fill_blocked_by_stop")}
            rows.append({"cell": f"{b}|{a}", "book": b, "asset": a, "scale_kind": kind,
                         "mode": mode, "guard_count_meaning": GUARD_MEANING[mode],
                         "n_campaigns": len(ts),
                         "bars_ridden": int(len(g)), "bars_with_level": int(fin.sum()),
                         "bars_no_level_expansion_or_none": int((~fin).sum()),
                         "live_bars": tc["live"], "guard_withheld_bars": tc["guard_withheld"],
                         "far_side_bars": tc["far_side"],
                         "preharvest_withheld_bars": tc["preharvest_withheld"],
                         "fills": tc["filled"], "fill_blocked_by_stop": tc["fill_blocked_by_stop"],
                         "campaigns_with_guard_withheld": sum(1 for t in ts
                                                              if t.tp_counts["guard_withheld"]),
                         "guard_withheld_bars_touched": int((fin & g["near"] & ~g["guard_ok"]
                                                             & g["touched"]).sum())})
    df = pd.DataFrame(rows)
    for c in df.columns:
        if c not in ("cell", "book", "asset", "scale_kind", "mode", "guard_count_meaning"):
            df[c] = df[c].astype(np.int64)
    return df


def exit_reason_grid(frames: dict) -> pd.DataFrame:
    rows = []
    for b in BOOK_KEYS:
        vc = frames[b]["exit_reason"].value_counts()
        unk = sorted(set(vc.index) - set(EXIT_REASONS))
        if unk:
            _halt(f"exit reasons {unk} in book {b} are not the declared {EXIT_REASONS}")
        for x in EXIT_REASONS:
            rows.append({"cell": f"{b}|{x}", "book": b, "exit_reason": x,
                         "n": int(vc.get(x, 0))})
    df = pd.DataFrame(rows)
    df["n"] = df["n"].astype(np.int64)
    return df


def fills_table(frames: dict) -> pd.DataFrame:
    rows = []
    for b in TP_BOOKS:
        df = frames[b]
        for _, r in df[df["exit_reason"] == TP_REASON].iterrows():
            rows.append({"book": b, "symbol": r["symbol"], "entry_ms": int(r["entry_ms"]),
                         "direction": int(r["direction"]), "era": r["era"],
                         "entry_px": float(r["entry_px"]), "r_dist": float(r["r_dist"]),
                         "fill_bar_open_ms": int(r["exit_ms"]),
                         "asof12_close_ms": int(r["tp_asof12_close_ms"]),
                         "level": float(r["tp_level"]), "fill_px": float(r["exit_px"]),
                         "harvested": bool(r["harvested"]),
                         "net_r": float(r["net_r"]), "v6_net_r": float(r["v6_net_r"]),
                         "delta_r": float(r["delta_r"]), "v6_exit_reason": r["v6_exit_reason"],
                         "v6_exit_ms": int(r["v6_exit_ms"]),
                         "bars_saved": int((int(r["v6_exit_ms"]) - int(r["exit_ms"])) // MS_4H),
                         "scale_in_sample_12h": bool(r["scale_in_sample_12h"])})
    cols = ["book", "symbol", "entry_ms", "direction", "era", "entry_px", "r_dist",
            "fill_bar_open_ms", "asof12_close_ms", "level", "fill_px", "harvested", "net_r",
            "v6_net_r", "delta_r", "v6_exit_reason", "v6_exit_ms", "bars_saved",
            "scale_in_sample_12h"]
    df = pd.DataFrame(rows, columns=cols)
    for c in ("entry_ms", "fill_bar_open_ms", "asof12_close_ms", "v6_exit_ms", "bars_saved"):
        df[c] = df[c].astype(np.int64)
    df["direction"] = df["direction"].astype(np.int8)
    return df


def campaigns_table(frames: dict) -> pd.DataFrame:
    base = frames["base"]
    out = base[["symbol", "entry_ms", "entry_close_ms", "direction", "era", "entry_px",
                "stop_px", "r_dist"]].copy()
    out["v6_exit_reason"] = base["exit_reason"].to_numpy()
    out["v6_exit_ms"] = base["exit_ms"].to_numpy(np.int64)
    out["v6_net_r"] = base["net_r"].to_numpy(float)
    out["v6_harvested"] = base["harvested"].to_numpy(bool)
    for b in TP_BOOKS:
        df = frames[b].set_index(["symbol", "entry_ms"]).loc[
            list(zip(out["symbol"], out["entry_ms"]))]
        out[f"{b}_exit_reason"] = df["exit_reason"].to_numpy()
        out[f"{b}_exit_ms"] = df["exit_ms"].to_numpy(np.int64)
        out[f"{b}_net_r"] = df["net_r"].to_numpy(float)
        out[f"{b}_delta_r"] = df["delta_r"].to_numpy(float)
        out[f"{b}_tp_level"] = df["tp_level"].to_numpy(float)
        gcol = ("guard_would_withhold_bars" if TP_BOOKS[b][1] == "unguarded"
                else "guard_withheld_bars")                     # verifier finding 6
        out[f"{b}_{gcol}"] = df["tp_guard_withheld"].to_numpy(np.int64)
        out[f"{b}_scale_in_sample_12h"] = df["scale_in_sample_12h"].to_numpy(bool)
    return out.reset_index(drop=True)


def reride_table(v6: list, rr: list) -> pd.DataFrame:
    kv = {(t.symbol, int(t.entry_ms)) for t in v6}
    kr = {(t.symbol, int(t.entry_ms)) for t in rr}
    rows = []
    for a in ASSETS_ALL:
        def sel(ks):
            return {k for k in ks if a == "ALL" or k[0] == a}
        v, r = sel(kv), sel(kr)
        rows.append({"asset": a, "n_v6": len(v), "n_reride": len(r),
                     "n_new_admitted_in_freed_slots": len(r - v),
                     "n_v6_not_taken_by_reride": len(v - r),
                     "sum_net_r_reride": fsum(t.net_r for t in rr
                                              if a == "ALL" or t.symbol == a)})
    df = pd.DataFrame(rows)
    for c in ("n_v6", "n_reride", "n_new_admitted_in_freed_slots", "n_v6_not_taken_by_reride"):
        df[c] = df[c].astype(np.int64)
    return df


def picks_table() -> pd.DataFrame:
    rows = []
    by = N.picks()["_by_cell"]
    for s in CLASSIC5:
        c = by[(s, LENS_U)]
        lab = N.scale_label(s, LENS_U, "calibrated")
        if lab["stability_changed"] is None:
            _halt(f"{s} 12h: no tuning pick — a whole-tape fallback would be IN-SAMPLE "
                  f"everywhere and this table would need its label [L-R.2]")
        rows.append({"asset": s, "lens": LENS_U, "pick_of_record": float(c["pick_of_record"]),
                     "pick_window": str(c["pick_window"]),
                     "tuning_pick": (float(c["tuning_pick"]) if c["tuning_pick"] is not None
                                     else float("nan")),
                     "whole_tape_pick": float(c["whole_tape_pick"]),
                     "first_half_pick": float(c["first_half_pick"]),
                     "frozen_scale": float(c["frozen_scale"]),
                     "stability_changed": bool(lab["stability_changed"]),
                     "in_sample_holdout": bool(c["in_sample_holdout"]),
                     "label": str(c["label"])})
    return pd.DataFrame(rows)


# ══════════════════════════════════════════════════════════════ COMPUTE
def compute() -> dict:
    """Everything, in memory.  HALTs on the paired premise, the identity law, the
    audit cross-check or the re-ride's v6 reproduction."""
    lo, hi, meta = B.corridor()
    base = B.v6_book(lo, hi)
    base_by = {(t.symbol, int(t.entry_ms)): t for t in base}
    levels = {k: levels_for(k) for k in SCALE_KINDS}
    books = {b: ride_tp_book(base, lo, hi, levels[kind], mode)
             for b, (kind, mode) in TP_BOOKS.items()}
    bad = []
    ident = {}
    for b, bk in books.items():
        bad += paired_premise(base, bk, b)
        f_, st = RD.identity_findings(base, bk)
        bad += f_
        ident[b] = st
    if bad:
        _halt(f"L-1.5 — the paired premise / identity law fails: {bad[:4]}")
    for k in SCALE_KINDS:                   # L-H.1: a level iff the 12h as-of state is IN_RANGE
        for s in CLASSIC5:
            lv = levels[k][s]
            for side in ("level_long", "level_short"):
                fin = np.isfinite(lv[side])
                if not np.array_equal(fin, lv["state4"] == N.STATE4["IN_RANGE"]) \
                        or not np.array_equal(fin, lv["in_range"]):
                    _halt(f"{s} {k} {side}: a level where the 12h state is not IN_RANGE, or "
                          f"none where it is [L-H.1]")
    bars = {k: bar_audit(base, levels[k], k) for k in SCALE_KINDS}
    for b, (kind, mode) in TP_BOOKS.items():
        bad += audit_findings(base, bars[kind], books[b], mode, b)
    if bad:
        _halt(f"the per-bar audit disagrees with the ride: {bad[:4]}")
    frames = {"base": book_rows(base, None, None, None, None)}
    for b, (kind, _) in TP_BOOKS.items():
        frames[b] = book_rows(books[b], base_by, bars[kind], levels[kind], kind)
    # the re-ride rival (SR-H6): tp=None must reproduce v6 exactly
    rr0 = reride(lo, hi, None)
    if [(t.symbol, int(t.entry_ms), float(t.net_r), int(t.exit_ms), t.exit_reason) for t in rr0] \
            != [(t.symbol, int(t.entry_ms), float(t.net_r), int(t.exit_ms), t.exit_reason)
                for t in base]:
        _halt("SR-H6: the re-ride's admission loop with tp=None is not the v6 book")
    rr = reride(lo, hi, levels["calibrated"], "record")
    d15 = {b: d15_of(frames[b], frames["base"]) for b in TP_BOOKS}
    return {"lo": lo, "hi": hi, "meta": meta, "base": base, "levels": levels, "books": books,
            "bars": bars, "frames": frames, "ident": ident, "reride": rr, "d15": d15}


# ══════════════════════════════════════════════════════════════ WRITING
def _inside(p: Path, root: Path) -> bool:
    return p == root or root in p.parents


def targets(out: Path) -> tuple[Path, Path]:
    """(stage dir, regbook dir).  OUT -> (stage_h/, regbooks/P-TP-RNG/); an F-DET
    twin DIR -> (DIR/stage_h, DIR/regbooks/P-TP-RNG).  Guarded."""
    o = Path(out).resolve()
    if o == OUT.resolve():
        return OUT, REGBOOKS
    trees = {ROOT.resolve(), Path(E.MAIN_TREE).resolve()}
    if o.parent == DET_ROOT.resolve() or (o.parent.name == DET_ROOT.name
                                          and not any(_inside(o, t) for t in trees)):
        return o / "stage_h", o / "regbooks" / REG_ID
    _halt(f"output dir {o} is neither {OUT}, an F-DET run dir under {DET_ROOT}, nor one under "
          f"a {DET_ROOT.name}/ scratch outside the repo")
    raise AssertionError


def write_parquet(df: pd.DataFrame, path: Path) -> str:
    """Pandas on a path STRING (AM-2), atomic; returns the content sha."""
    path.parent.mkdir(parents=True, exist_ok=True)
    d = df.reset_index(drop=True)
    d.attrs = {}
    d.columns = [str(c) for c in d.columns]
    tmp = path.with_name(path.name + ".tmp")
    d.to_parquet(str(tmp), index=False)
    os.replace(str(tmp), str(path))
    return TB._content_sha(d)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(str(tmp), str(path))


def _json(obj) -> str:
    return json.dumps(obj, indent=2, sort_keys=True, default=str, ensure_ascii=False) + "\n"


def arm_frame(R: dict, arm: str) -> pd.DataFrame:
    spec = next(a for a in ARMS if a[0] == arm)
    df = R["frames"][spec[5]]
    if spec[4] != "full":
        df = df[df["era"] == spec[4]].reset_index(drop=True)
    return df


def slice_identity(df: pd.DataFrame, era: str) -> dict:
    """The identity counts OF AN ERA SLICE'S ROWS [verifier finding 5] — RD's law
    (acted = acted_by != ''; unacted carry v6's net_r / exit_ms / exit_reason at
    0.000e+00) re-read on the slice; HALT on any unacted difference."""
    acted = (df["acted_by"].astype(str) != "").to_numpy()
    un = df[~acted]
    worst = 0.0
    for c_new, c_v6 in (("net_r", "v6_net_r"), ("exit_ms", "v6_exit_ms")):
        dv = np.abs(un[c_new].to_numpy(float) - un[c_v6].to_numpy(float))
        worst = max(worst, float(dv.max()) if len(dv) else 0.0)
    if worst != 0.0 or bool((un["exit_reason"] != un["v6_exit_reason"]).any()):
        _halt(f"L-1.5 — the {era} slice holds an unacted campaign that is not v6's")
    return {"scope": f"this slice's {len(df)} rows (era == '{era}'), not the full arm",
            "acted": int(acted.sum()), "unacted": int((~acted).sum()),
            "worst_unacted_abs_diff": worst, "held": True}


def arm_description(arm: str) -> str:
    return {
        "scored": "P-TP-RNG scored arm: every v6 campaign re-ridden with a resting take-profit "
                  "limit for the remainder at the 12h far boundary ∓ 0.25 ATR_12h when the 12h "
                  "as-of state at the 4h bar's open is IN_RANGE (calibrated 12h pick), live only "
                  "with the prior 4h close on the near side and the level > 10 bps beyond entry; "
                  "fill max(level, open) / min(level, open); STOP -> TP -> BELL -> HARVEST -> "
                  "TRAIL; v6 harvest kept [L-H.1]. Paired vs base on (symbol, entry_ms).",
        "base": "the v6 book (card v6, V6_ROLES, CLASSIC5, full TC11 corridor) in the regbook "
                "schema — the pairing base [L-1.5, L-1.6].",
        "tierE__tp_post_harvest": "rival reading: the TP rests only after the v6 band harvest "
                                  "has fired (the 0.5 runner) [L-H.1 rival]. Paired vs base.",
        "tierE__unguarded": "the unguarded twin: the TP without the entry-side guard (ii) "
                            "[L-H.1 'also printed']. Paired vs base.",
        "tierE__frozen3": "the frozen-3.0 twin: 12h ranges at the frozen scale 3.0 (fully "
                          "causal) [L-R.2 SCALE-IN-SAMPLE]. Paired vs base.",
        "tierE__tuning": "the scored arm's tuning slice (entry close <= 2024-06-30T23:59:59Z) "
                         "[L-1.3]; paired vs the base restricted to era == 'tuning'.",
        "tierE__holdout": "the scored arm's holdout slice (entry close > the cut; the only slice "
                          "with a causal calibrated scale) [L-1.3, L-R.2]; paired vs the base "
                          "restricted to era == 'holdout'.",
    }[arm]


def build(out: Path = OUT) -> dict:
    sdir, rdir = targets(out)
    R = compute()
    meta = R["meta"]

    def stamped(df: pd.DataFrame, collar: bool) -> pd.DataFrame:
        d = TP.stamp_n(df, meta, "4h", None)
        return _collar(d) if collar else d

    # ── the regbooks ────────────────────────────────────────────────────────
    arm_meta = {}
    reg_shas = {}
    for arm, kind, scale_kind, mode, era, bkey in ARMS:
        df = arm_frame(R, arm)
        sha = book_sha256(df)
        dfw = stamped(df, kind == "tierE")
        reg_shas[f"{arm}.parquet"] = write_parquet(dfw, rdir / f"{arm}.parquet")
        side = {"registration": REG_ID, "arm": arm, "kind": kind, "ruler": "paired",
                "panel": list(CLASSIC5), "era_scope": era, "n": int(len(df)),
                "sum_net_r": fsum(df["net_r"]), "book_sha256": sha,
                "description": arm_description(arm), "source_script": SOURCE,
                "book_sha256_law": BOOK_SHA_LAW, "columns_required": list(REQ_COLS),
                "as_of_last_closed_4h": PIN_ISO, "seed": SEED,
                "scale_kind_12h": scale_kind, "tp_mode": mode,
                "pairing_key": ["symbol", "entry_ms"]}
        if kind == "tierE":
            side.update(COLLAR)
        if kind != "base":
            side["d15_vs_base"] = (R["d15"][bkey] if era == "full"
                                   else d15_of(df, R["frames"]["base"][
                                       R["frames"]["base"]["era"] == era]))
            side["named_risk"] = WALL_LESSON
            side["scale_in_sample"] = (
                "SCALE-IN-SAMPLE: calibrated-scale 12h reads at instants <= the era cut are "
                "structurally in-sample (tuning-era calibration); the holdout slice and the "
                "frozen-3.0 twin print beside [L-R.2]" if scale_kind == "calibrated" else
                "frozen 3.0: fully causal, never in-sample")
            if bkey in R["ident"]:
                side["identity_law"] = (
                    {"acted": R["ident"][bkey]["acted"],
                     "unacted": R["ident"][bkey]["unacted"],
                     "worst_unacted_abs_diff": R["ident"][bkey]["worst"], "held": True}
                    if era == "full" else slice_identity(df, era))
            if mode == "unguarded":
                side["tp_guard_withheld_meaning"] = (
                    "on this arm the guard is OFF: tp_guard_withheld counts WOULD-WITHHOLD bars "
                    "(near-side orders the entry-side guard would have refused; here they "
                    "rested and could fill) [verifier finding 6]")
        write_text(rdir / f"{arm}.json", _json(side))
        arm_meta[arm] = side
    status = {"registration": REG_ID, "status": "BUILT",
              "reason": (f"the paired premise and the identity law held on every paired arm "
                         f"(key sets identical to v6, n {len(R['base'])}; every campaign the TP "
                         f"never filled carries v6's net_r / exit_ms / exit_reason exactly); "
                         f"books only — no CI, no p, no verdict word [L-1.4, L-1.5]"),
              "arms": [a[0] for a in ARMS]}
    write_text(rdir / "STATUS.json", _json(status))

    # ── the stage tables ────────────────────────────────────────────────────
    F = R["frames"]
    tables = {
        "tp_campaigns": campaigns_table(F),
        "tp_bars": pd.concat([R["bars"][k] for k in SCALE_KINDS], ignore_index=True),
        "tp_fills": fills_table(F),
        "tp_summary": summary_grid(F),
        "tp_withheld": withheld_grid(R["books"], R["bars"]),
        "tp_exit_reasons": exit_reason_grid(F),
        "tp_reride": reride_table(R["base"], R["reride"]),
        "tp_picks": picks_table(),
    }
    st_shas = {}
    for name, key in STAGE_TABLES.items():
        df = tables[name]
        if df.duplicated(subset=key).any():
            _halt(f"{name}: key {key} is not unique")
        df = df.sort_values(key, kind="mergesort").reset_index(drop=True)
        tables[name] = df
        st_shas[f"{name}.parquet"] = write_parquet(stamped(df, True), sdir / f"{name}.parquet")
    R["tables"] = tables
    R["arm_meta"] = arm_meta
    md = render_md(R)
    write_text(sdir / REPORT, md)
    man = {"tier": "TIER-C11", "stage": STAGE, "registration": REG_ID, "seed": SEED,
           "as_of": PIN_ISO, "as_of_close_ms": PIN_MS, "substrate": meta["substrate"],
           "corridor": {"lo": iso(R["lo"]), "hi_close": iso(R["hi"] + 1),
                        "panel": list(CLASSIC5)},
           "sha_kinds": {"content_sha": "TB._content_sha of the frame as written (NOT the file "
                                        "bytes)",
                         "file_sha256": "sha256 of the file's BYTES on disk (shasum -a 256)"},
           "regbooks": {"dir": f"research_outputs/tierc11/regbooks/{REG_ID}",
                        "content_sha": reg_shas,
                        "file_sha256": {p.name: _sha_file(p) for p in sorted(
                            [rdir / f"{a[0]}.{x}" for a in ARMS for x in ("parquet", "json")]
                            + [rdir / "STATUS.json"])},
                        "book_sha256": {a: m["book_sha256"] for a, m in arm_meta.items()},
                        "n": {a: m["n"] for a, m in arm_meta.items()},
                        "sum_net_r": {a: m["sum_net_r"] for a, m in arm_meta.items()}},
           "stage_tables": {"dir": "research_outputs/tierc11/stage_h", "content_sha": st_shas,
                            "file_sha256": {p.name: _sha_file(p) for p in sorted(
                                [sdir / f"{n}.parquet" for n in STAGE_TABLES]
                                + [sdir / REPORT])},
                            "keys": dict(STAGE_TABLES),
                            "rows": {n: int(len(t)) for n, t in tables.items()}},
           "report_sha256": hashlib.sha256(md.encode("utf-8")).hexdigest(),
           "inputs": {"SCALE_PICKS.json": _sha_file(N.PICKS_PATH),
                      "fee_schedule.json": _sha_file(E.OUT / "data" / "fee_schedule.json"),
                      "books/build_manifest.json": _sha_file(B.OUT / B.MANIFEST),
                      "input_sha_classic5": TP.input_sha(E.CLASSIC5)},
           "code": {p: _sha_file(ROOT / "scripts" / p) for p in (
               "tierc11_stage_h.py", "tierc11_ride.py", "tierc11_nest.py", "tierc11_books.py",
               "tierc11_env.py")},
           "collar": {"applies_to": "every stage_h table and every tierE regbook", **COLLAR},
           "readings": list(READINGS)}
    write_text(sdir / MANIFEST, _json(man))
    R["manifest"] = man
    return R


def _sha_file(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


# ══════════════════════════════════════════════════════════════ THE REPORT
def _fmt(v, nd: int = 4) -> str:
    if v is None:
        return "—"
    if isinstance(v, (bool, np.bool_)):
        return "yes" if v else "no"
    if isinstance(v, (int, np.integer)):
        return f"{int(v):,}" if abs(int(v)) >= 10_000 else str(int(v))
    if isinstance(v, (float, np.floating)):
        if not np.isfinite(v):
            return "NaN"
        return f"{float(v):+.{nd}f}"
    return str(v)


def md_table(df: pd.DataFrame, cols: list[str], fmt: dict | None = None) -> str:
    """The WHOLE table, every row (column arrays keep their own dtypes)."""
    fmt = fmt or {}
    L = ["| " + " | ".join(cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    arr = {c: df[c].to_numpy() for c in cols}
    for i in range(len(df)):
        cells = []
        for c in cols:
            v = arr[c][i]
            if c in fmt:
                cells.append(fmt[c](v))
            elif c.endswith("_ms") and isinstance(v, (int, np.integer)) \
                    and not isinstance(v, (bool, np.bool_)):
                cells.append(iso(int(v))[:16] if int(v) > 0 else "—")
            else:
                cells.append(_fmt(v))
        L.append("| " + " | ".join(cells) + " |")
    return "\n".join(L)


def findings_lines(R: dict) -> list[str]:
    """Stage-intrinsic findings, every number read off the tables (no verdict word)."""
    F, T = R["frames"], R["tables"]
    out = []
    rr = T["tp_reride"]
    a = rr[rr["asset"] == "ALL"].iloc[0]
    out.append(f"H-1 the re-ride rival [L-1.5] admits {int(a['n_new_admitted_in_freed_slots'])} "
               f"new campaign(s) into slots a TP freed and drops "
               f"{int(a['n_v6_not_taken_by_reride'])} v6 campaign(s): on this corridor the "
               f"paired set and the re-ride set "
               + ("coincide." if int(a['n_new_admitted_in_freed_slots']) == 0
                  and int(a['n_v6_not_taken_by_reride']) == 0 else "differ (see table 7)."))
    wg = T["tp_withheld"]
    blk = {b: int(wg.loc[wg["cell"] == f"{b}|ALL", "fill_blocked_by_stop"].iloc[0])
           for b in TP_BOOKS}
    out.append(f"H-2 a live, touched TP beaten by the stop on the same bar (STOP -> TP): {blk} — "
               f"the adverse-first order " + ("never bound on this corridor."
                                              if not any(blk.values()) else "bound (counted)."))
    gaps = {}
    for b in TP_BOOKS:
        f_ = T["tp_fills"][T["tp_fills"]["book"] == b]
        gaps[b] = f"{int((f_['fill_px'] != f_['level']).sum())}/{len(f_)}"
    out.append(f"H-3 fills at the open (the bar opened beyond the level, fill = open) / all "
               f"fills: {gaps}.")
    sc, ug = F["scored"], F["unguarded"]
    diff = sc[(sc["exit_ms"].to_numpy() != ug["exit_ms"].to_numpy())
              | (sc["exit_reason"].to_numpy() != ug["exit_reason"].to_numpy())]
    parts = []
    for i in diff.index:
        u = ug.loc[i]
        bps = (float(u["tp_level"]) - float(u["entry_px"])) * int(u["direction"]) \
            / float(u["entry_px"]) * 1e4 if u["exit_reason"] == TP_REASON else float("nan")
        parts.append(f"{sc.loc[i, 'symbol']} {iso(int(sc.loc[i, 'entry_ms']))[:16]} "
                     f"({'long' if int(sc.loc[i, 'direction']) == 1 else 'short'}): unguarded "
                     f"{u['exit_reason']} at {iso(int(u['exit_ms']))[:16]} (level {bps:+.3f} bps "
                     f"beyond entry) vs scored {sc.loc[i, 'exit_reason']} at "
                     f"{iso(int(sc.loc[i, 'exit_ms']))[:16]}")
    out.append(f"H-4 the entry-side guard (ii) changes {len(diff)} campaign(s): "
               + ("; ".join(parts) if parts else "none") + ".")
    pk = T["tp_picks"]
    out.append("H-5 SCALE-IN-SAMPLE: every 12h pick of record is a tuning-era pick "
               f"({', '.join(f'{s} {p:.2f}' for s, p in zip(pk['asset'], pk['pick_of_record']))}); "
               f"the first-half-of-tuning pick differs on "
               + (", ".join(pk.loc[pk["stability_changed"], "asset"]) or "none")
               + "; the tuning slice is structurally in-sample, the holdout slice and the "
               "frozen-3.0 twin are the causal reads (table 1).")
    out.append("H-6 SR-H3 exit_close_ms convention: every regbook here stamps the exit 4h bar's "
               "CLOSE (the books/v6_campaigns.parquet convention; the base arm equals that file "
               "on the 13 shared columns at its 6 dp); a stage that rides the 1h walk stamps a "
               "1h-resolved exit instant instead — the paired statistic (net_r keyed on "
               "(symbol, entry_ms)) does not read it, a cross-stage base-identity check does.")
    return out


def render_md(R: dict) -> str:
    F, T, M = R["frames"], R["tables"], R["arm_meta"]
    sc, bs = F["scored"], F["base"]
    d15 = R["d15"]["scored"]
    L = [f"# TIER-C11 · STAGE H — P-TP-RNG (take-profit at the 12h range boundary)", "",
         f"as_of_last_closed_4h: {PIN_ISO} · substrate {R['meta']['substrate']} · seed {SEED} · "
         f"corridor {iso(R['lo'])} → {iso(R['hi'] + 1)} · panel CLASSIC5",
         "Contract of record `exchange/queue/2026-09-24_TC11_APOLLO.md` (sha256 bb38e016…). "
         "Readings: LEANS.md L-H.1, L-1.5, L-1.3, L-R.2; LEANS_AMENDMENTS AM-6 (s2), AM-7. "
         f"Source `{SOURCE}`. Books only: no CI, no p — the scorer decides.", "",
         "## 0 · The registered book (book, not a verdict)", ""]
    rows = []
    for arm in ("scored", "base"):
        df = arm_frame(R, arm)
        rows.append({"arm": arm, "n": len(df), "sum_net_r": fsum(df["net_r"]),
                     "mean_net_r": fsum(df["net_r"]) / len(df),
                     "sum_haircut_net_r": fsum(df["haircut_net_r"]),
                     "n_tp_exits": int((df["exit_reason"] == TP_REASON).sum()),
                     "book_sha256": M[arm]["book_sha256"][:16] + "…",
                     "label": "book, not a verdict"})
    L.append(md_table(pd.DataFrame(rows), ["arm", "n", "sum_net_r", "mean_net_r",
                                           "sum_haircut_net_r", "n_tp_exits", "book_sha256",
                                           "label"]))
    dl = sc["delta_r"].to_numpy(float)
    L += ["",
          f"- Paired descriptive (no interval): mean Δ(scored − v6) {fsum(dl) / len(dl):+.6f} R, "
          f"ΣΔ {fsum(dl):+.6f} R over n {len(dl)} (TP-acted {int(sc['tp_fill'].sum())}, "
          f"unacted {int((~sc['tp_fill']).sum())}).",
          f"- **D15 on the row** (T5.d15, scored vs base): n_paired {d15['n_paired']} · "
          f"paired_delta_expectancy_r {d15['paired_delta_expectancy_r']} · **tail_exit_ratio "
          f"{d15['tail_exit_ratio']}** · max_single_trade_delta_share "
          f"{d15['max_single_trade_delta_share']} · unpaired cell/base "
          f"{d15['unpaired_cell_n']}/{d15['unpaired_base_n']}.",
          f"- **Named risk:** {WALL_LESSON}",
          f"- **Identity law [L-1.5] asserted before writing:** key set == v6's on every paired "
          f"arm; unacted campaigns carry v6's net_r / exit_ms / exit_reason at 0.000e+00 — "
          + "; ".join(f"{b}: acted {st['acted']}, unacted {st['unacted']}, worst "
                      f"{st['worst']:.3e}" for b, st in R["ident"].items()) + ".",
          "- **SCALE-IN-SAMPLE [L-R.2]:** the calibrated 12h pick was fit on the tuning era, so "
          "every calibrated 12h read at an instant <= 2024-06-30T23:59:59Z is structurally "
          f"in-sample ({int(sc['scale_in_sample_12h'].sum())} of {len(sc)} scored campaigns read "
          "one). Beside it: the holdout slice (the only slice with a causal scale) and the "
          "frozen-3.0 twin (fully causal) — table 1. Pick stability — table 8; the 12h pick "
          "changed between the first half of tuning and the whole tuning era on: "
          + (", ".join(T["tp_picks"].loc[T["tp_picks"]["stability_changed"], "asset"])
             or "none") + " (flagged on every row that consumes the lens: "
          "stability_changed_12h).", ""]
    wg = T["tp_withheld"]
    w = wg[wg["cell"] == "scored|ALL"].iloc[0]
    L += [f"- **Withheld orders (scored, all assets):** the entry-side guard withheld "
          f"{int(w['guard_withheld_bars'])} bar-orders on {int(w['campaigns_with_guard_withheld'])} "
          f"campaigns ({int(w['guard_withheld_bars_touched'])} of those bars reached the level); "
          f"far-side (prior close beyond the level) {int(w['far_side_bars'])}; live "
          f"{int(w['live_bars'])}; fills {int(w['fills'])}; a live touched order beaten by the "
          f"stop {int(w['fill_blocked_by_stop'])}; bars with no level (12h EXPANSION / NONE) "
          f"{int(w['bars_no_level_expansion_or_none'])} of {int(w['bars_ridden'])} ridden.", ""]
    L += ["## 1 · The regbook arms (P-TP-RNG) — scored, base and the Tier-E arms", "",
          "Tier-E arms: tier TIER-E · a SELECTION, not a result · gates nothing.", ""]
    rows = []
    for arm, kind, scale_kind, mode, era, bkey in ARMS:
        df = arm_frame(R, arm)
        rows.append({"arm": arm, "kind": kind, "scale_12h": scale_kind or "—",
                     "tp_mode": mode or "—", "era_scope": era, "n": len(df),
                     "sum_net_r": fsum(df["net_r"]),
                     "mean_net_r": fsum(df["net_r"]) / len(df) if len(df) else float("nan"),
                     "sum_haircut_net_r": fsum(df["haircut_net_r"]),
                     "n_tp": int((df["exit_reason"] == TP_REASON).sum()),
                     "tail_exit_ratio": (M[arm]["d15_vs_base"]["tail_exit_ratio"]
                                         if "d15_vs_base" in M[arm] else None),
                     "book_sha256": M[arm]["book_sha256"][:16] + "…"})
    L.append(md_table(pd.DataFrame(rows), ["arm", "kind", "scale_12h", "tp_mode", "era_scope",
                                           "n", "sum_net_r", "mean_net_r", "sum_haircut_net_r",
                                           "n_tp", "tail_exit_ratio", "book_sha256"]))
    L += ["", "## 2 · The grid: book × era × asset (Tier-E · a SELECTION, not a result · gates "
          "nothing)", "",
          "Δ = net_r − v6 net_r on the same (symbol, entry_ms); tail_exit_ratio = T5.d15 vs the "
          "base cell.", ""]
    L.append(md_table(T["tp_summary"], ["book", "era", "asset", "n", "n_tp", "sum_net_r",
                                        "mean_net_r", "win_rate", "sum_haircut_net_r",
                                        "sum_delta_r", "mean_delta_r", "tail_exit_ratio",
                                        "nan_reason"]))
    L += ["", "## 3 · TP order counts (withheld / far side / live / fills) per TP book × asset "
          "(Tier-E · a SELECTION, not a result · gates nothing)", ""]
    L += ["guard_count_meaning: on the unguarded twin the guard is OFF, so its "
          "guard_withheld_bars / guard_withheld_bars_touched / campaigns_with_guard_withheld "
          "count WOULD-WITHHOLD bars — near-side orders the guard would have refused, which "
          "there RESTED (and could fill); on the other books they count orders the guard "
          "withheld.", ""]
    L.append(md_table(T["tp_withheld"], ["book", "asset", "guard_count_meaning", "n_campaigns",
                                         "bars_ridden", "bars_with_level",
                                         "bars_no_level_expansion_or_none",
                                         "live_bars", "guard_withheld_bars",
                                         "guard_withheld_bars_touched",
                                         "campaigns_with_guard_withheld", "far_side_bars",
                                         "preharvest_withheld_bars", "fills",
                                         "fill_blocked_by_stop"]))
    L += ["", "## 4 · Exit reasons per book (Tier-E · a SELECTION, not a result · gates nothing)",
          ""]
    er = T["tp_exit_reasons"].pivot(index="book", columns="exit_reason", values="n").reindex(
        index=list(BOOK_KEYS), columns=list(EXIT_REASONS)).reset_index()
    L.append(md_table(er, ["book"] + list(EXIT_REASONS)))
    L += ["", "## 5 · Every TP fill (all four TP books; Tier-E · a SELECTION, not a result · "
          "gates nothing)", "",
          "level = the 12h as-of boundary ∓ 0.25 ATR_12h read at the fill bar's open; fill = "
          "max(level, open) long / min(level, open) short.", ""]
    ft = T["tp_fills"].copy()
    ft["dir"] = ft["direction"].map({1: "long", -1: "short"})
    L.append(md_table(ft, ["book", "symbol", "entry_ms", "dir", "era", "fill_bar_open_ms",
                           "asof12_close_ms", "level", "fill_px", "harvested", "net_r",
                           "v6_net_r", "delta_r", "v6_exit_reason", "bars_saved"],
                      fmt={"level": lambda v: f"{v:.6g}", "fill_px": lambda v: f"{v:.6g}"}))
    L += ["", "## 6 · Bars audited, by 12h as-of state (every bar of every v6 campaign; Tier-E · "
          "a SELECTION, not a result · gates nothing)", ""]
    bt = T["tp_bars"]
    g = (bt.assign(has_level=np.isfinite(bt["level"].to_numpy(float)))
         .groupby(["scale_kind", "state12"], sort=True)
         .agg(bars=("level", "size"), with_level=("has_level", "sum"),
              near=("near", "sum"), guard_ok=("guard_ok", "sum"),
              live_record=("live_record", "sum"), touched=("touched", "sum"))
         .reset_index())
    decl = pd.DataFrame([(k, s) for k in SCALE_KINDS
                         for s in ("IN_RANGE", "BULL_EXP", "BEAR_EXP", "NONE")],
                        columns=["scale_kind", "state12"])
    g = decl.merge(g, on=["scale_kind", "state12"], how="left").fillna(0)
    for c in ("bars", "with_level", "near", "guard_ok", "live_record", "touched"):
        g[c] = g[c].astype(np.int64)
    L.append(md_table(g, ["scale_kind", "state12", "bars", "with_level", "near", "guard_ok",
                          "live_record", "touched"]))
    n_exp_lvl = int(g.loc[g["state12"] != "IN_RANGE", "with_level"].sum())
    n_in_nolvl = int((g.loc[g["state12"] == "IN_RANGE", "bars"]
                      - g.loc[g["state12"] == "IN_RANGE", "with_level"]).sum())
    L += ["", f"Bars whose 12h as-of state is BULL_EXP, BEAR_EXP or NONE carrying a level: "
          f"{n_exp_lvl}; IN_RANGE bars without one: {n_in_nolvl} (asserted 0 and 0 at build): "
          "no order rests outside a live 12h range, the trail runs.", "",
          f"tp_bars itself ({len(bt):,} rows × {len(bt.columns)} data columns, one per bar of "
          "every v6 campaign per scale) is whole in `stage_h/tp_bars.parquet` (typed key "
          "unique, manifest content and byte shas; every row refereed by F-TP / "
          "F-TP-EXPANSION / F-ROW); this report prints its WHOLE aggregation above (every "
          "declared scale × state cell) and not its rows: printed whole they are 2.0 MB of "
          "markdown, in a report that feeds the build doc.", ""]
    L += ["## 7 · The re-ride rival [L-1.5] — a DISCLOSURE count (Tier-E · a SELECTION, not a "
          "result · gates nothing)", "",
          "The scored arm admits nothing into a slot a TP frees. The rival re-runs replay9's "
          "admission with the TP ride (it reproduces v6 exactly with the TP off — asserted):", ""]
    L.append(md_table(T["tp_reride"], ["asset", "n_v6", "n_reride",
                                       "n_new_admitted_in_freed_slots",
                                       "n_v6_not_taken_by_reride", "sum_net_r_reride"]))
    L += ["", "## 8 · 12h scale picks and stability [L-R.2] (Tier-E · a SELECTION, not a result · "
          "gates nothing)", ""]
    L.append(md_table(T["tp_picks"], ["asset", "lens", "pick_of_record", "pick_window",
                                      "tuning_pick", "whole_tape_pick", "first_half_pick",
                                      "frozen_scale", "stability_changed", "in_sample_holdout"],
                      fmt={c: (lambda v: f"{v:.2f}") for c in (
                          "pick_of_record", "tuning_pick", "whole_tape_pick", "first_half_pick",
                          "frozen_scale")}))
    L += ["", "## 9 · Findings (stage-intrinsic, derived from the tables above)", ""]
    L += [f"- {x}" for x in findings_lines(R)]
    L += ["", "## 10 · Readings of record and executor sub-readings", ""]
    L += [f"- {x}" for x in READINGS]
    L += ["", "## 11 · Files", "",
          f"- regbooks: `research_outputs/tierc11/regbooks/{REG_ID}/` — "
          + ", ".join(f"`{a[0]}.parquet/.json`" for a in ARMS) + ", `STATUS.json` (BUILT).",
          "- stage tables: `research_outputs/tierc11/stage_h/` — "
          + ", ".join(f"`{n}.parquet` ({len(R['tables'][n])} rows)" for n in STAGE_TABLES)
          + f"; `{MANIFEST}` (content shas = TB._content_sha of the frame, and file_sha256 = "
          "the bytes on disk).", ""]
    tc = T["tp_campaigns"]
    L += [f"## 12 · Every campaign (tp_campaigns, WHOLE: {len(tc)} rows × {len(tc.columns)} "
          "columns; Tier-E · a SELECTION, not a result · gates nothing)", "",
          "Per v6 campaign: the v6 outcome and each TP book's (exit reason, exit bar, net R, Δ vs "
          "v6, the TP level at the exit bar, the guard count — would-withhold on the unguarded "
          "twin — and SCALE-IN-SAMPLE).", ""]
    L.append(md_table(tc, list(tc.columns),
                      fmt={c: (lambda v: f"{v:.6g}" if np.isfinite(v) else "NaN")
                           for c in tc.columns
                           if c in ("entry_px", "stop_px", "r_dist") or c.endswith("_tp_level")}))
    return "\n".join(L) + "\n"


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    od = next((a.split("=", 1)[1] for a in args if a.startswith("--out-dir=")), None)
    R = build(Path(od) if od else OUT)
    for arm in ("scored", "base") + tuple(a[0] for a in ARMS if a[1] == "tierE"):
        m = R["arm_meta"][arm]
        print(f"{arm:26} n {m['n']:>4} · ΣR {m['sum_net_r']:+.6f} · book sha {m['book_sha256']}")
    print(f"D15 scored vs base: {R['d15']['scored']}")
    return 0


__all__ = ["asof_12h_index", "levels_from_facts", "levels_for", "facts_of", "tp_levels",
           "ride_tp_book", "reride", "bar_audit", "audit_findings", "book_rows", "book_sha256",
           "d15_of", "compute", "build", "targets", "ARMS", "TP_BOOKS", "REQ_COLS", "OUT",
           "REGBOOKS", "DET_ROOT", "STAGE_TABLES", "READINGS", "GUARD_BPS", "APPROACH_ATR"]


if __name__ == "__main__":
    raise SystemExit(main())
