#!/usr/bin/env python
"""TIER-C11 · STAGE R-b · R4 — THE TWO TRADES PER LENS, TIER-E, WHOLE
[LEANS L-R.6 as written; AM-1, AM-4, AM-6].

Contract of record: exchange/queue/2026-09-24_TC11_APOLLO.md (sha256 bb38e016…,
STEP Q b9ed953), STAGE R · R4: "for L in {1h,4h,12h,1d}: (a) BREAKOUT = macro
death -> first retest that HOLDS (band taps 89/127/200 and the memory-line,
both printed); (b) SWING-FAILURE = deviation confirmed at a CONFIRMED boundary
(spring/upthrust). Each conditioned on the lens above ... Outcomes H20/H100 net
of L's toll, base rate, null (gaps+order), per direction."  Executor
HEPHAESTUS; seed 20260924 (sensitivity 20260816).  Everything here is TIER-E:
every table carries the collar tier='TIER-E' · selection_not_a_result='a
SELECTION, not a result' · gates='nothing', and no verdict word.

WHAT IT BUILDS (research_outputs/tierc11/stage_r4/)
  R4_EVENTS.parquet   every event of the grid, real machine: asset x lens x
                      scale x event, with its anchor (N's known_at), its L+1
                      cell (N.l1_cell at the known_at close: record, the
                      memory-line twin, and for SFP the post-redraw twin), its
                      outcome ledger (C.outcome_ledger: term / MFE / MAE at
                      H20 / H100 in bars of L from the known_at close, censored
                      never shortened, toll_atr = 10 bps x c / ATR_L) and the
                      honesty labels (pick window, scale-in-sample, stability).
  R4_GRID.parquet     the grid WHOLE: asset | pool x lens x scale x event x
                      cell law x L+1 cell x direction x era x horizon, every
                      statistic by C.grid_rows itself (unforked; pooled rows
                      quote the BINDING max toll), each row beside its cell's
                      base-rate row, its own-side base twin and the
                      unconditional base, with event NET - base NET.
  R4_GRID.md          the POOLED:CLASSIC5 grid whole (per-asset rows in the
                      parquet).
  R4_BASE.parquet     the base rate: the same statistics anchored at EVERY
                      closed bar of L, per asset | pool x era x direction,
                      (i) unconditional (cell ALL) and (ii) within each L+1
                      cell read at close_k (range_facts' base cells: coincidence
                      of record coin_top OR coin_bot, R-BASE-COIN), the per-side
                      twins (topside, botside), the own-side composites and the
                      memory-line twin.
  R4_NULL.parquet     the gaps+order null of record (ruling R10) rebuilt for
                      TC11, one row per real grid cell of record law: the real
                      value beside the null's median / IQR / min / max over
                      K = 20 draws, the mid-rank percentile ("a DESCRIPTION,
                      never a p-value"), every draw's n and NET, and the
                      sensitivity-seed (20260816) median / percentile of NET.
  R4_NULL_BOXES.parquet  every null draw's box schedule (seed of record).
  R4_SCAN.parquet     every EVALUATED touch of the first-retest-that-holds scan
                      (L-R.6(a) "every evaluated touch is a row"): the three taps
                      and the memory line, per asset x lens x scale, verdict
                      failed / hold / truncated, first holds flagged (N's frames).
  R4_DEATHS.parquet   every macro death of the grid's machines with, per band,
                      its evaluated-touch count and how its scan ended (hold ·
                      truncated · failed-out · no-touch) — the hold and
                      truncation counts per lens and band.
  STAGE_R4.md, build_manifest.json.

THE NULL (L-R.6 "the gaps+order null of record (ruling R10), rebuilt for TC11"):
per (asset, lens, scale) and draw d — the REAL confirmed macro ranges at the
filed pick (NL.real_box_set), the TC10 draw law unforked (NL.draw_rng:
default_rng([seed + d, crc32("asset|lens|scale_kind")]); NL.schedule with
keep_order=False: the m+1 gaps AND the order of the (life, height-in-ATR) pairs
permuted, each box re-centred on its new confirm close at a uniform %-position),
NL.static_box_machine, the real leash on the corpses (RC.flips_and_leash) —
then the TC11 events through N's own scan (N.scan_band, C.retest_holds,
N.scan_memory_of, N.oneshot_memory_of; the hardens), and each null event's L+1
cell read from the REAL L+1 machine at its known_at (N.l1_cell).  Never
tierc10_null.scale_for / compute_cell: the scale is N.scale_of (the TC11 pick).

PARALLELISM [AM-2]: this module never starts a process.  The build is split
into UNITS (panel x lens x scale); `--unit=P:L:K --parts=DIR` computes one unit
in THIS interpreter and writes its frames to DIR (pandas on path strings);
`--merge --parts=DIR` assembles the files of record.  A caller may run the
units in freshly started interpreters side by side (the shell, or the fixture
harness, which AM-2 allows to start processes); with no flag the whole build
runs serially in one interpreter.  Units are pure functions of the snapshot and
the filed picks, and the merge sorts every table by its key, so the bytes do
not depend on how the units were scheduled.

NEVER READ: Range.top / .bottom (the nest's law); never a price out of an event.

Run:  export NAIAD_CACHE_DIR=$HOME/.cache/naiad/snapshots/tc11_20260925 PYTHONDONTWRITEBYTECODE=1
      ~/venvs/naiad/bin/python -B scripts/tierc11_stage_r4.py [--out-dir=DIR]      # serial, whole
      ~/venvs/naiad/bin/python -B scripts/tierc11_stage_r4.py --units             # list the units
      ~/venvs/naiad/bin/python -B scripts/tierc11_stage_r4.py --unit=CLASSIC5:4h:calibrated --parts=DIR
      ~/venvs/naiad/bin/python -B scripts/tierc11_stage_r4.py --merge --parts=DIR [--out-dir=DIR]
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
import time
import zlib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import tierc11_nest as N                                             # noqa: E402  (the shim first; the range door)

import numpy as np                                                   # noqa: E402
import pandas as pd                                                  # noqa: E402

E, C, NL, RC = N.E, N.C, N.NL, N.RC
ROOT = E.ROOT
OUT = E.OUT / "stage_r4"
PARTS_DEFAULT = OUT / "_det_parts"            # gitignored (research_outputs/tierc11/**/_det_*/)
PIN_MS, PIN_ISO = E.PIN_MS, E.PIN_ISO
TC10_PIN_MS = E.TC10_PIN_MS                   # 2026-09-21T16:00:00Z
SEED, SEED_SENS, N_BOOT = E.SEED, E.SEED_SENS, E.N_BOOT
LEAN_TAG = E.LEAN_TAG
K_DRAWS = 20                                  # [L-R.6] "K = 20 draws"
NULL_SEEDS = (SEED, SEED_SENS)                # of record · sensitivity [L-1.4 seeds]
SCHEDULE_VARIANT = "gaps+order"               # ruling R10 (keep_order=False)

PANELS = {"CLASSIC5": tuple(E.CLASSIC5), "UNSEEN12": tuple(E.UNSEEN12)}
POOL = {"CLASSIC5": "POOLED:CLASSIC5", "UNSEEN12": "POOLED:UNSEEN12"}
LENSES_R4 = {"CLASSIC5": ("1h", "4h", "12h", "1d"), "UNSEEN12": ("1h", "4h", "1d")}
SCALE_KINDS = ("calibrated", "frozen3.0")     # the pick of record · the frozen twin
UNITS = tuple(f"{p}:{L}:{k}" for p in PANELS for L in LENSES_R4[p] for k in SCALE_KINDS)
BANDS = ("tap89", "tap127", "tap200")
RULES = ("first", "oneshot")
EVENTS = tuple(f"BRK_{b}_{r}" for b in BANDS + ("mem",) for r in RULES) + ("SFP_harden",)
DIRECTIONS = ("both", "long", "short")
DIR_OF = {"long": 1, "short": -1}
ERAS = tuple(C.ERAS)                          # ("ALL", "tuning", "holdout")
HORIZONS = tuple(h for h, _ in C.HORIZONS)    # ("H20", "H100"), bars of the lens
PARTITION = tuple(c for c in N.CELLS if c != "NA")
EV_LAWS_L1 = {"BRK": ("record", "mem_twin"), "SFP": ("record", "mem_twin", "post_redraw")}
EV_LAW_COL = {"record": "cell", "mem_twin": "cell_mem", "post_redraw": "cell_post"}
BASE_LAWS_L1 = ("record", "mem_twin", "topside", "botside", "own_side_brk", "own_side_sfp",
                "own_side_brk_mem", "own_side_sfp_mem")
CELL_BASE_LAW = {"record": "record", "mem_twin": "mem_twin", "post_redraw": "record"}
# the own-side base of an event row, by (family, cell law): the mem_twin rows take the
# own-side composite built on L's nest coin_*_mem (memory lines admitted), never the
# record one [repair of the verifier's MINOR-1: one law per row]
SIDE_BASE_LAW = {("BRK", "record"): "own_side_brk", ("BRK", "mem_twin"): "own_side_brk_mem",
                 ("SFP", "record"): "own_side_sfp", ("SFP", "mem_twin"): "own_side_sfp_mem",
                 ("SFP", "post_redraw"): "own_side_sfp"}
SCAN_BANDS_R4 = BANDS + ("memory-line",)
BAND_SLUG = {"tap89": "tap89", "tap127": "tap127", "tap200": "tap200", "memory-line": "mem"}
SCAN_ENDS = ("hold", "truncated", "failed-out", "no-touch")
NULL_STATS = ("median_term", "net", "hit_rate_net")
COLLAR = {"tier": "TIER-E", "selection_not_a_result": "a SELECTION, not a result",
          "gates": "nothing"}
PCTILE_LAW = ("mid-rank: 100 x (#null < real + 0.5 x #null == real) / valid draws — "
              "a DESCRIPTION of where the real value sits among the K draws, never a "
              "p-value; K = 20 resolves it to 5 points at best")
LED_COLS = (["era", "bad_atr", "toll_atr_evt"]
            + [f"{x}_{h}" for h in HORIZONS for x in ("cens", "term", "mfe", "mae")])
GRID_FIELDS = ("horizon_bars", "scale_mult", "n_events", "n", "n_censored", "n_bad_atr",
               "toll_atr_all", "median_term", "mean_term", "q25_term", "q75_term",
               "hit_rate", "hit_rate_net", "median_mfe", "median_mae", "toll_atr", "net",
               "binding_over_n_assets", "toll_pooling", "nan_reason", "provisional",
               "toll_bps", "toll_bps_source")
GRID_KEY = ["asset", "lens", "scale_kind", "event", "cell_law", "cell", "direction", "era",
            "horizon"]
BASE_KEY = ["asset", "lens", "scale_kind", "cell_law", "cell", "direction", "era", "horizon"]
EVENTS_KEY = ["asset", "lens", "scale_kind", "event", "rid", "side", "anchor_i"]
NULL_KEY = ["asset", "lens", "scale_kind", "event", "cell", "direction", "era", "horizon"]
BOXES_KEY = ["asset", "lens", "scale_kind", "draw", "box"]
SCAN_KEY = ["asset", "lens", "scale_kind", "band", "rid", "side", "touch_i"]
DEATHS_KEY = ["asset", "lens", "scale_kind", "rid", "side"]
TABLE_KEYS = {"R4_EVENTS": EVENTS_KEY, "R4_GRID": GRID_KEY, "R4_BASE": BASE_KEY,
              "R4_NULL": NULL_KEY, "R4_NULL_BOXES": BOXES_KEY, "R4_SCAN": SCAN_KEY,
              "R4_DEATHS": DEATHS_KEY}
FILES_OF_RECORD = ("R4_BASE.parquet", "R4_DEATHS.parquet", "R4_EVENTS.parquet", "R4_GRID.md",
                   "R4_GRID.parquet", "R4_NULL.parquet", "R4_NULL_BOXES.parquet",
                   "R4_SCAN.parquet", "STAGE_R4.md", "build_manifest.json")
OUTCOME_GRID_REL = "research_outputs/tierc10/census/outcome_grid.parquet"   # AM-1
TC10_CONT = {"asset": "POOLED:CLASSIC5", "lens": "4h", "cls": "retest-hold-tap89",
             "scale_kind": "frozen3.0", "horizon": "H20"}
NaN = float("nan")

READINGS = (
    "R4-1 COMMISSION [L-R.6]: CLASSIC5 x {1h, 4h, 12h, 1d} and UNSEEN12 x {1h, 4h, 1d}, per "
    "asset and pooled (POOLED:CLASSIC5, POOLED:UNSEEN12 — the pools never mix), x {calibrated "
    "(the filed pick of record, N.scale_of), frozen3.0 (the twin)} x eras {ALL, tuning, "
    "holdout} by the anchor bar's CLOSE [L-1.3] x directions {both, long, short} x {H20, H100} "
    "in bars of L. Everything is TIER-E.",
    "R4-2 EVENTS [L-R.6(a)(b)]: BREAKOUT = N's first-retest-that-HOLDS scan (rule 'first') on "
    "tap89 / tap127 / tap200 (C.RETEST_PINS 1.0 ATR / 3 bars / ttl 400) and the memory line "
    "(1.0 ATR / 6 bars), each beside its one-shot twin (rule 'oneshot': C.retest_holds' hold "
    "rows; the engine's one-shot flip for the memory line). Direction = the death side (top "
    "-> long). SWING-FAILURE = the machine's harden (bottom -> spring, long; top -> "
    "upthrust, short). Every event is anchored at N's known_at (touch + hold; the harden bar) "
    "and never recomputed here.",
    "R4-3 L+1 CELL [L-R.6, R-CELL]: N.l1_cell at the event's known_at CLOSE — record = "
    "coincidence of the event's boundary of L (BREAKOUT: the broken side as-of die_i - 1; "
    "SFP: the deviated side as-of harden_i - 1) with a LIVE L+1 boundary within 0.25 x ATR_L; "
    "twins: 'mem_twin' (L+1 live memory lines admitted, N's cell_mem) and, for SFP, "
    "'post_redraw' (the boundary as-of harden_i; 'n/a' where no post-redraw boundary exists). "
    "Cells: EXP_ALIGNED*, EXP_COUNTER, "
    "IN_RANGE_COINCIDENT*, IN_RANGE_MID*, IN_RANGE_OTHER, NONE (the contract's three starred); "
    "'ALL' = unconditioned; 'NA' where the ladder lacks L+1 in the commission (UNSEEN12 4h and "
    "1d, whose 12h / 1w are not built).",
    "R4-4 OUTCOMES: C.outcome_ledger (the census's own road, unforked): term = sgn x (c[k+H] - "
    "c[k]) / ATR_L[k] from the known_at close k, MFE / MAE likewise; CENSORED when k + H > "
    "n - 1 (never shortened); toll_atr_evt = (10 bps / 10^4) x c[k] / ATR_L[k] with the bps "
    "read from TC11's fee schedule (C.toll_bps_for). Statistics = C.grid_rows ITSELF on each "
    "cell's ledger slice (n_events, n, n_censored, median_term, mean_term, q25/q75, hit_rate, "
    "hit_rate_net, median MFE / MAE, toll_atr, net = median_term - toll_atr) fed the FILED "
    "(8 dp) ledger as the census feeds it (tierc10_census.compute_cell canons first); a pooled row "
    "quotes the BINDING max of its members' toll_atr (C.grid_rows' tolls= law, TC10's). "
    "Cells are packed up to eleven per C.grid_rows call under its eleven class labels; the "
    "label changes only the dropped metadata columns, never the arithmetic.",
    "R4-5 BASE RATE [L-R.6, AM-6 R-BASE-COIN]: C.outcome_ledger anchored at EVERY closed bar k "
    "of L, long and short; direction 'both' = the union of the two anchored sets (a cell that "
    "depends on direction — EXP_ALIGNED — takes each bar under its own direction). Cells from "
    "N.range_facts: record = coin_top OR coin_bot of L at k with L+1 read as-of close_k; "
    "twins topside / botside (one side alone), own_side_brk (long@topside + short@botside: a "
    "BREAKOUT's broken side), own_side_sfp (long@botside + short@topside: an SFP's deviated "
    "side), mem_twin (L's nest coin_*_mem), and the memory-line own-side twins own_side_brk_mem "
    "/ own_side_sfp_mem (the same composites on coin_top_mem / coin_bot_mem). Each event row "
    "carries its cell-base row (law record; mem_twin for mem_twin rows), its own-side base "
    "(BRK own_side_brk, SFP own_side_sfp; the _mem composite for mem_twin rows; post_redraw rows "
    "the record composite) and the unconditional base (cell ALL), with event NET - base NET.",
    "R4-6 NULL [L-R.6, ruling R10]: gaps+order, K = 20, per (asset, lens, scale) at the filed "
    "pick — NL.real_box_set, NL.draw_rng (default_rng([seed + draw, crc32('asset|lens|"
    "scale_kind')]); 'kind' read as the scale kind, TC10's key), NL.schedule(keep_order=False), "
    "NL.static_box_machine, RC.flips_and_leash on the corpses; events through N's scan and the "
    "null's hardens; the null box's static edge is the event boundary; the L+1 cell read from "
    "the REAL L+1 machine at the null event's known_at. Pooled null draw d = draw d of every "
    "member (TC10's law). One null row per real grid cell of law record: real beside the "
    "null's median / q25 / q75 / IQR / min / max over the valid draws and the mid-rank "
    "percentile — a DESCRIPTION, never a p-value; every draw's n and NET filed; the "
    "sensitivity seed 20260816 re-draws the null and prints its NET median and percentile "
    "beside. Built at both scales (calibrated of record; frozen3.0 = TC10's null scale).",
    "R4-7 CONTINUITY [AM-1]: at frozen3.0, one-shot, 4h, POOLED:CLASSIC5, tap89, H20 NET, "
    "TC11's value is printed beside TC10's census/outcome_grid.parquet row (read by absolute "
    "main-tree path), and the TC10 window is REPLAYED in TC11 code (the tapes cut at "
    "2026-09-21T16:00Z, C.run_scale at 3.0, C.retest_holds, C.outcome_ledger, C.grid_rows): "
    "the replay must equal the filed row at its 8 dp; the difference to TC11 is then "
    "decomposed event by event over the 20 extra 4h bars.",
    "R4-8 LABELS [L-R.2, AM-4]: every event row carries l_ / u_ pick_window, "
    "scale_in_sample and stability_changed; every grid / base / null row carries the pick "
    "windows and stability flags of L and L+1 (a pool: the distinct values joined) and the "
    "counts of its anchors whose L or L+1 read is scale-in-sample.",
    "R4-9 PARALLELISM [AM-2]: the runner starts no process; units run in-process (serial) or "
    "in fresh interpreters started by the caller; the merge alone writes the files of record.",
    "R4-10 SCAN LEDGER [L-R.6(a) 'every evaluated touch is a row']: R4_SCAN files N's "
    "first-retest scan rows verbatim (N.first_retest_scan: tap89 / tap127 / tap200 and the "
    "memory line; seq, touch, known_at = touch + 3 / + 6, verdict, first hold; era by the "
    "known_at close, 'beyond_pin' where a truncated row's known_at passes the tape); R4_DEATHS "
    "files every death of N.events with, per band, its evaluated-touch count and its END: hold "
    "(a first hold), truncated, failed-out (every touch in the candidacy window failed), "
    "no-touch.",
)


def log(msg: str = "") -> None:
    print(msg, flush=True)


def clock(msg: str) -> None:
    print(f"  [clock · stdout only] {msg}", flush=True)


# ═══════════════════════════════════════════════ 1 · THE COMMISSION
def has_l1(panel: str, lens: str) -> bool:
    U = N.LADDER[lens]
    return U is not None and all(U in N.LENSES_OF[s] for s in PANELS[panel])


def event_cells(panel: str, lens: str) -> list[tuple[str, str, str]]:
    """(event, cell_law, cell) of the grid, per (panel, lens) — the declared
    shape: law record carries ALL + the partition (ALL + NA without an L+1);
    the twins carry the partition only (they re-partition, ALL is the same)."""
    out = []
    l1 = has_l1(panel, lens)
    for ev in EVENTS:
        laws = EV_LAWS_L1[ev.split("_")[0]] if l1 else ("record",)
        for law in laws:
            cells = (("ALL",) if law == "record" else ()) + (PARTITION if l1 else ("NA",))
            out += [(ev, law, c) for c in cells]
    return out


def base_cells(panel: str, lens: str) -> list[tuple[str, str]]:
    out = []
    l1 = has_l1(panel, lens)
    for law in (BASE_LAWS_L1 if l1 else ("record",)):
        cells = (("ALL",) if law == "record" else ()) + (PARTITION if l1 else ("NA",))
        out += [(law, c) for c in cells]
    return out


def _parse_unit(u: str) -> tuple[str, str, str]:
    p, L, k = u.split(":")
    if u not in UNITS:
        raise SystemExit(f"HALT: unit {u!r} is not one of the {len(UNITS)} units {list(UNITS)}")
    return p, L, k


# ═══════════════════════════════════════════════ 2 · THE OUTCOME ROAD (hooks)
_STUB: dict = {}


def _stub_view(n: int) -> dict:
    """C.outcome_ledger captures five as-of stamps at the anchor; R4 files none of
    them (the real ones live in the nest), so it is handed zeros."""
    if n not in _STUB:
        _STUB[n] = {"state": np.zeros(n, np.int8), "in_range": np.zeros(n, bool),
                    "pct": np.full(n, np.nan), "dist_atr": np.full(n, np.nan),
                    "flip_pol": np.zeros(n, np.int8)}
    return _STUB[n]


_AT_COLS = ("state_at", "in_range_at", "pct_at", "dist_atr_at", "flip_pol_at")


def _round_led(led: pd.DataFrame) -> pd.DataFrame:
    """The FILED form of a ledger: every float at C.ROUND_ND (8) dp, as C.canon
    files it — C.grid_rows reads the filed ledger, so every statistic is an exact
    function of bytes a reader can open (tierc10_census.compute_cell's law)."""
    d = led.copy()
    for c in d.columns:
        if pd.api.types.is_float_dtype(d[c]):
            d[c] = d[c].round(C.ROUND_ND)
    return d


def _ledger(tape, evf: pd.DataFrame, bps: float) -> pd.DataFrame:
    """THE OUTCOME ROAD [R4-4]: C.outcome_ledger, unforked (term / MFE / MAE from
    the known_at close, censored when k + H > n - 1, toll in ATR_L), in its
    filed (8 dp) form."""
    led = C.outcome_ledger(tape, evf, _stub_view(tape.n), bps)
    return _round_led(led.drop(columns=list(_AT_COLS)))


def _anchor(f: pd.DataFrame) -> np.ndarray:
    """[R4-2] every event is anchored at N's known_at — the hook F-R4-EVENTS bends."""
    return f["known_at"].to_numpy(np.int64)


def _l1(stem: str, lens: str, kind: str, direction, boundary, known_ms) -> pd.DataFrame:
    """[R4-3] the L+1 cell, N.l1_cell at the known_at close — the hook F-R4-L1 bends."""
    return N.l1_cell(stem, lens, kind, direction, boundary, known_ms)


def _close_ms(tape, i) -> np.ndarray:
    i = np.asarray(i, dtype=np.int64)
    inside = (i >= 0) & (i < tape.n)
    return np.where(inside, tape.t0[np.where(inside, i, 0)] + tape.step, -1)


# ═══════════════════════════════════════════════ 3 · EVENTS
EV_FRAME_COLS = ["event", "family", "band", "rule", "rid", "side", "dir", "die_i", "anchor_i",
                 "seq", "known_at", "boundary", "boundary_post"]


def assemble(fr: dict, die_bnd: dict) -> pd.DataFrame:
    """The event rows of one machine run from its frames — {scan, oneshot,
    scan_mem, oneshot_mem, hardens} as N's events() shapes them — and the dead
    ranges' broken-side boundaries {die_i: px}.  The same code serves the real
    machine (N.events) and every null draw."""
    parts = []

    def put(f, event, band, rule, anchor_col, seq):
        if not len(f):
            return
        d = pd.DataFrame({
            "event": event, "family": event.split("_")[0], "band": band, "rule": rule,
            "rid": f["rid"].to_numpy(np.int64), "side": f["side"].astype(str).to_numpy(),
            "dir": f["dir"].to_numpy(np.int64),
            "die_i": (f["die_i"].to_numpy(np.int64) if "die_i" in f else
                      np.full(len(f), -1, np.int64)),
            "anchor_i": f[anchor_col].to_numpy(np.int64),
            "seq": seq(f), "known_at": _anchor(f)})
        parts.append(d)

    sc, os_ = fr["scan"], fr["oneshot"]
    for band in BANDS:
        put(sc[(sc["band"] == band) & sc["is_first_hold"]], f"BRK_{band}_first", band, "first",
            "touch_i", lambda f: f["seq"].to_numpy(np.int64))
        put(os_[(os_["band"] == band) & (os_["verdict"] == "hold")], f"BRK_{band}_oneshot",
            band, "oneshot", "touch_i", lambda f: np.zeros(len(f), np.int64))
    sm, om = fr["scan_mem"], fr["oneshot_mem"]
    put(sm[sm["is_first_hold"]], "BRK_mem_first", "memory-line", "first", "touch_i",
        lambda f: f["seq"].to_numpy(np.int64))
    put(om[om["verdict"] == "hold"], "BRK_mem_oneshot", "memory-line", "oneshot", "touch_i",
        lambda f: np.zeros(len(f), np.int64))
    hd = fr["hardens"]
    if len(hd):
        d = pd.DataFrame({
            "event": "SFP_harden", "family": "SFP", "band": "harden", "rule": "harden",
            "rid": hd["rid"].to_numpy(np.int64), "side": hd["side"].astype(str).to_numpy(),
            "dir": hd["dir"].to_numpy(np.int64), "die_i": np.full(len(hd), -1, np.int64),
            "anchor_i": hd["harden_i"].to_numpy(np.int64),
            "seq": np.zeros(len(hd), np.int64), "known_at": _anchor(hd)})
        d["boundary"] = hd["boundary_pre"].to_numpy(float)
        d["boundary_post"] = hd["boundary_post"].to_numpy(float)
        parts.append(d)
    if not parts:
        return pd.DataFrame({c: pd.Series(dtype=(object if c in ("event", "family", "band",
                                                                  "rule", "side")
                                                  else float if c.startswith("boundary")
                                                  else np.int64)) for c in EV_FRAME_COLS})
    f = pd.concat(parts, ignore_index=True)
    brk = f["family"] == "BRK"
    f.loc[brk, "boundary"] = [float(die_bnd.get(int(i), np.nan)) for i in f.loc[brk, "die_i"]]
    f.loc[brk, "boundary_post"] = np.nan
    f["boundary"] = f["boundary"].astype(float)
    f["boundary_post"] = f["boundary_post"].astype(float)
    return f[EV_FRAME_COLS]


def event_ledger(stem: str, lens: str, kind: str, tape, ev: pd.DataFrame, bps: float,
                 cells: bool = True, twins: bool = True) -> pd.DataFrame:
    """Outcomes and L+1 cells for assembled events."""
    evf = pd.DataFrame({"cls": "DIE", "i": ev["anchor_i"].to_numpy(np.int64),
                        "known_at": ev["known_at"].to_numpy(np.int64),
                        "rid": ev["rid"].to_numpy(np.int64), "side": ev["side"].to_numpy(),
                        "sgn": ev["dir"].to_numpy(np.int64)})
    led = _ledger(tape, evf, bps)
    out = ev.reset_index(drop=True).copy()
    for c in ["known_close_ms"] + LED_COLS:
        out[c] = led[c].to_numpy()
    k = out["known_at"].to_numpy(np.int64)
    ks = np.clip(k, 0, tape.n - 1)
    out["atr_known"] = np.where((k >= 0) & (k < tape.n), tape.atr[ks], np.nan)
    if cells:
        d = out["dir"].to_numpy(np.int64)
        kms = out["known_close_ms"].to_numpy(np.int64)
        c1 = _l1(stem, lens, kind, d, out["boundary"].to_numpy(float), kms)
        out["cell"] = c1["cell"].to_numpy()
        if twins:
            out["cell_mem"] = c1["cell_mem"].to_numpy()
            sfp = (out["family"] == "SFP").to_numpy()
            bpost = out["boundary_post"].to_numpy(float)
            post = np.array(["n/a"] * len(out), dtype=object)
            if sfp.any():
                c2 = _l1(stem, lens, kind, d[sfp], bpost[sfp], kms[sfp])
                post[sfp] = c2["cell"].to_numpy()
            # no post-redraw boundary -> no post-redraw twin (never a silent
            # 'not coincident') [verifier MINOR-5]
            post[~np.isfinite(bpost)] = "n/a"
            out["cell_post"] = post
            out["u_state"] = np.array([x if x is not None else "NA" for x in c1["u_state"]],
                                      dtype=object)
            out["u_pct"] = c1["u_pct"].to_numpy(float)
            out["u_k"] = c1["u_k"].to_numpy(np.int64)
        for p in ("l", "u"):
            out[f"{p}_pick_window"] = np.array([x if x is not None else "NA"
                                                for x in c1[f"{p}_pick_window"]], dtype=object)
            out[f"{p}_scale_in_sample"] = pd.array(c1[f"{p}_scale_in_sample"], dtype="boolean")
            out[f"{p}_stability_changed"] = pd.array(c1[f"{p}_stability_changed"],
                                                     dtype="boolean")
    return out


def real_events(stem: str, lens: str, kind: str) -> pd.DataFrame:
    """THE REAL EVENTS of one (asset, lens, scale) from N.events, with outcomes,
    cells and labels."""
    ev = N.events(stem, lens, kind)
    D = ev["deaths"]
    die_bnd = dict(zip(D["die_i"].astype(int).tolist(), D["boundary"].astype(float).tolist()))
    fr = {k: ev[k] for k in ("scan", "oneshot", "scan_mem", "oneshot_mem", "hardens")}
    evs = assemble(fr, die_bnd)
    tape = N.load11(stem, lens)
    bps = C.toll_bps_for(stem)[0]
    out = event_ledger(stem, lens, kind, tape, evs, bps)
    out.insert(0, "asset", stem)
    out.insert(1, "lens", lens)
    out.insert(2, "scale_kind", kind)
    out.insert(3, "scale_mult", N.scale_of(stem, lens, kind))
    return out


# ═══════════════════════════════════════════════ 4 · THE BASE RATE
def _base_cells(stem: str, lens: str, kind: str) -> dict:
    """{law: (cell names for LONG anchors, for SHORT anchors)} over every bar of L
    [R4-5]: range_facts' base cells (record = coin_top OR coin_bot, R-BASE-COIN;
    topside; botside), the own-side composites and the memory-line twin — the
    hook F-R4-BASE bends."""
    tape = N.load11(stem, lens)
    n = tape.n
    U = N.LADDER[lens]
    if U is None or U not in N.LENSES_OF[stem]:
        na = np.array(["NA"] * n, dtype=object)
        return {"record": (na, na)}
    rf = N.range_facts(stem, lens, kind)
    name = np.array(N.CELLS, dtype=object)
    out = {"record": (name[rf["base_cell_long"]], name[rf["base_cell_short"]]),
           "topside": (name[rf["base_cell_long_topside"]], name[rf["base_cell_short_topside"]]),
           "botside": (name[rf["base_cell_long_botside"]], name[rf["base_cell_short_botside"]])}
    out["own_side_brk"] = (out["topside"][0], out["botside"][1])
    out["own_side_sfp"] = (out["botside"][0], out["topside"][1])
    nv = N.nest_at(stem, rf["close_ms"], kind)
    ctm = nv[f"{lens}_coin_top_mem"].fillna(False).to_numpy(bool)
    cbm = nv[f"{lens}_coin_bot_mem"].fillna(False).to_numpy(bool)
    coin = ctm | cbm
    u_code = rf["l1_state4"].astype(np.int64)
    u_pct = rf["l1_pct"].astype(float)
    out["mem_twin"] = (N._cells(1, u_code, u_pct, coin).astype(object),
                       N._cells(-1, u_code, u_pct, coin).astype(object))
    # the memory-line twin's OWN side (a BREAKOUT's broken side, an SFP's deviated
    # side), so a mem_twin event row meets a base of its own law [MINOR-1]
    out["own_side_brk_mem"] = (N._cells(1, u_code, u_pct, ctm).astype(object),
                               N._cells(-1, u_code, u_pct, cbm).astype(object))
    out["own_side_sfp_mem"] = (N._cells(1, u_code, u_pct, cbm).astype(object),
                               N._cells(-1, u_code, u_pct, ctm).astype(object))
    return out


def base_ledger(stem: str, lens: str, kind: str) -> pd.DataFrame:
    """C.outcome_ledger at EVERY closed bar k of L, long then short, with each
    bar's cell under every base law and its honesty labels."""
    tape = N.load11(stem, lens)
    n = tape.n
    k = np.arange(n, dtype=np.int64)
    kk = np.concatenate([k, k])
    sg = np.concatenate([np.ones(n, np.int64), -np.ones(n, np.int64)])
    evf = pd.DataFrame({"cls": "DIE", "i": kk, "known_at": kk, "rid": -1, "side": "bar",
                        "sgn": sg})
    bps = C.toll_bps_for(stem)[0]
    led = _ledger(tape, evf, bps)
    out = pd.DataFrame({"k": kk, "dir": sg})
    for c in LED_COLS:
        out[c] = led[c].to_numpy()
    for law, (cl, cs) in _base_cells(stem, lens, kind).items():
        out[f"cell_{law}"] = np.concatenate([np.asarray(cl, dtype=object),
                                             np.asarray(cs, dtype=object)])
    close = tape.t0 + tape.step
    lab = N.scale_label(stem, lens, kind)
    lis = N.scale_in_sample(lab, close)
    U = N.LADDER[lens]
    uis = (N.scale_in_sample(N.scale_label(stem, U, kind), close)
           if U is not None and U in N.LENSES_OF[stem] else np.zeros(n, bool))
    out["l_scale_in_sample"] = np.concatenate([lis, lis])
    out["u_scale_in_sample"] = np.concatenate([uis, uis])
    return out


# ═══════════════════════════════════════════════ 5 · THE STATISTICS (C.grid_rows itself)
_LED_DTYPES = {"era": object, "bad_atr": bool, "toll_atr_evt": float,
               **{f"cens_{h}": bool for h in HORIZONS},
               **{f"{x}_{h}": float for h in HORIZONS for x in ("term", "mfe", "mae")}}


def _empty_led() -> pd.DataFrame:
    return pd.DataFrame({c: pd.Series(dtype=t) for c, t in {"cls": object, **_LED_DTYPES}.items()})


def packed_rows(led: pd.DataFrame, groups: list, asset: str, lens: str, kind: str,
                scale_mult: float, bps, bps_src: str, tolls: dict | None = None) -> dict:
    """{group key: [6 rows (3 eras x 2 horizons)]} — C.grid_rows ITSELF on each
    group's ledger slice [R4-4].  `groups` = [(key, boolean mask over led)].
    Groups are packed up to eleven per call under C.CLASSES' eleven labels (the
    label moves only the dropped metadata columns); a pooled call hands
    C.grid_rows the members' rows of the SAME group (`tolls`, relabelled alike),
    so the binding toll is TC10's law."""
    out: dict = {}
    labels = tuple(C.CLASSES)
    core = led[LED_COLS] if len(led) else _empty_led()[LED_COLS]
    for b0 in range(0, len(groups), len(labels)):
        batch = groups[b0:b0 + len(labels)]
        parts, tl, lab = [], [], {}
        for j, (key, m) in enumerate(batch):
            cls = labels[j]
            lab[cls] = key
            if len(core) and m.any():
                parts.append(core[m].assign(cls=cls))
            if tolls is not None:
                tl.append(tolls[key].assign(cls=cls))
        lb = pd.concat(parts, ignore_index=True) if parts else _empty_led()
        tdf = (pd.concat(tl, ignore_index=True) if tolls is not None else None)
        rows = C.grid_rows(lb, asset, lens, kind, scale_mult, bps, bps_src, tolls=tdf)
        for r in rows:
            if r["cls"] in lab:
                out.setdefault(lab[r["cls"]], []).append(
                    {"era": r["era"], "horizon": r["horizon"],
                     **{f: r[f] for f in GRID_FIELDS}})
    return out


def _rows_frame(res: dict, keycols: tuple) -> pd.DataFrame:
    rows = []
    for key, rs in res.items():
        for r in rs:
            rows.append({**dict(zip(keycols, key)), **r})
    return pd.DataFrame(rows)


def _dir_mask(d: np.ndarray, direction: str) -> np.ndarray:
    return np.ones(len(d), bool) if direction == "both" else d == DIR_OF[direction]


def event_groups(led: pd.DataFrame, panel: str, lens: str, laws_cells=None) -> list:
    """[(key (event, law, cell, direction), mask over led)] in declared order."""
    out = []
    n = len(led)
    ev = led["event"].to_numpy() if n else np.array([], dtype=object)
    d = led["dir"].to_numpy(np.int64) if n else np.array([], np.int64)
    for (e, law, cell) in (event_cells(panel, lens) if laws_cells is None else laws_cells):
        m_e = ev == e
        if cell != "ALL" and n:
            m_e = m_e & (led[EV_LAW_COL[law]].to_numpy() == cell)
        for direction in DIRECTIONS:
            out.append(((e, law, cell, direction), m_e & _dir_mask(d, direction)))
    return out


def base_groups(led: pd.DataFrame, panel: str, lens: str) -> list:
    out = []
    d = led["dir"].to_numpy(np.int64)
    for (law, cell) in base_cells(panel, lens):
        m_c = (np.ones(len(led), bool) if cell == "ALL"
               else led[f"cell_{law}"].to_numpy() == cell)
        for direction in DIRECTIONS:
            out.append(((law, cell, direction), m_c & _dir_mask(d, direction)))
    return out


def _attach_insample(df: pd.DataFrame, led: pd.DataFrame, groups: list,
                     keycols: tuple) -> pd.DataFrame:
    """n_l_scale_in_sample / n_u_scale_in_sample: the row's anchors (its n_events
    basis) whose L / L+1 read is scale-in-sample [R4-8]."""
    n = len(led)
    er = led["era"].to_numpy() if n else np.array([], dtype=object)
    flags = {}
    for c in ("l_scale_in_sample", "u_scale_in_sample"):
        flags[c] = (pd.array(led[c], dtype="boolean").fillna(False).to_numpy(bool)
                    if n and c in led else np.zeros(n, bool))
    tun, hol = er == "tuning", er == "holdout"
    cnt = {}
    for key, m in groups:
        cnt[key] = {c: {"ALL": int((v & m).sum()), "tuning": int((v & m & tun).sum()),
                        "holdout": int((v & m & hol).sum())} for c, v in flags.items()}
    kk = list(zip(*[df[c] for c in keycols]))
    df["n_l_scale_in_sample"] = [cnt[k]["l_scale_in_sample"][e] for k, e in zip(kk, df["era"])]
    df["n_u_scale_in_sample"] = [cnt[k]["u_scale_in_sample"][e] for k, e in zip(kk, df["era"])]
    return df


def _labels(stems, lens: str, kind: str) -> dict:
    """pick windows / stability of L and L+1 over the stems (joined distinct)."""
    def one(L):
        if L is None or any(L not in N.LENSES_OF[s] for s in stems):
            return "NA", "NA"
        labs = [N.scale_label(s, L, kind) for s in stems]
        pw = "+".join(sorted({x["pick_window"] for x in labs}))
        st = sorted({("NA" if x["stability_changed"] is None else str(bool(x["stability_changed"])))
                     for x in labs})
        return pw, "+".join(st)
    lp, ls = one(lens)
    up, us = one(N.LADDER[lens])
    return {"l_pick_window": lp, "l_stability_changed": ls, "u_pick_window": up,
            "u_stability_changed": us}


# ═══════════════════════════════════════════════ 6 · THE NULL
def null_frames(b: dict, bands: dict) -> dict:
    """The TC11 event frames of ONE machine run — N's scan (N.scan_band on each
    tap, memoised bands), the one-shot twin (C.retest_holds, as
    N.oneshot_bands_of), the memory line (N.scan_memory_of, N.oneshot_memory_of).
    Fed the REAL bundle it returns N.events' frames (F-NULL holds it to that)."""
    tape = b["tape"]
    rp = C.RETEST_PINS
    m, h, t = float(rp["margin_atr"]), int(rp["hold_bars"]), int(rp["ttl_bars"])
    rows, orows = [], []
    for name in BANDS:
        lo, hi = bands[name]
        rows += N.scan_band(tape, b["dies"], name, lo, hi, m, h, t)
        for g in C.retest_holds(tape, b["dies"], lo, hi, m, h, t):
            orows.append({"band": name, **g, "dir": N.UP[g["side"]]})
    scan = N._scan_frame(rows, tape)
    os_ = pd.DataFrame(orows, columns=["band", "rid", "side", "die_i", "touch_i", "known_at",
                                       "verdict", "dir"])
    for k in ("rid", "die_i", "touch_i", "known_at", "dir"):
        os_[k] = os_[k].astype(np.int64)
    os_["known_close_ms"] = _close_ms(tape, os_["known_at"].to_numpy())
    return {"scan": scan, "oneshot": os_, "scan_mem": N.scan_memory_of(b),
            "oneshot_mem": N.oneshot_memory_of(b)}


def band_memo(tape) -> dict:
    return {name: C.band_of(name)(tape.c) for name in BANDS}


def null_draw(stem: str, lens: str, kind: str, tape, real: dict, draw: int, seed: int,
              bands: dict) -> dict:
    """ONE null draw [R4-6]: TC10's draw law unforked, TC11's scan, the REAL L+1."""
    s = N.scale_of(stem, lens, kind)
    rng = NL.draw_rng(seed, draw, stem, lens, kind)
    boxes, info = NL.schedule(real, rng, keep_order=False)
    nm = NL.static_box_machine(tape, boxes)
    leash = RC.flips_and_leash(nm, tape.d, tape.atr, dict(RC.PINS_V2, SCALE_MULT=float(s)),
                               retests=False)
    # the null box's edges from what is known AT its confirm bar (NL.box_bounds:
    # the schedule's u and height re-priced by ATR[confirm]) — static, never a
    # Range field [N-b, N-e; R4-6]
    edge = {int(bx.box): NL.box_bounds(bx, float(tape.c[bx.confirm_i]),
                                       float(tape.atr[bx.confirm_i]))
            for bx in boxes if bx.confirm_i < tape.n}
    dies = sorted((int(e["i"]), int(e["rid"]), str(e["side"])) for e in nm["events"]
                  if e["event"] == "breakout-die")

    def px_of(rid: int, side: str) -> float:
        bot, top = edge[rid]
        return float(top if side == "top" else bot)
    mem_rows = []
    for _, rid, _side in dies:
        mem_rows += [{"rid": rid, "side": "top", "px": px_of(rid, "top")},
                     {"rid": rid, "side": "bottom", "px": px_of(rid, "bottom")}]
    mem = pd.DataFrame(mem_rows, columns=["rid", "side", "px"])
    b = {"tape": tape, "v2": {"macro": nm, "leash": leash}, "dies": dies, "mem": mem}
    fr = null_frames(b, bands)
    hrows = []
    for e in nm["events"]:
        if e["event"] == "harden":
            px = px_of(int(e["rid"]), str(e["side"]))
            hrows.append({"harden_i": int(e["i"]), "rid": int(e["rid"]), "side": str(e["side"]),
                          "dir": -N.UP[str(e["side"])], "known_at": int(e["i"]),
                          "boundary_pre": px, "boundary_post": px})
    fr["hardens"] = pd.DataFrame(hrows, columns=["harden_i", "rid", "side", "dir", "known_at",
                                                 "boundary_pre", "boundary_post"])
    die_bnd = {d_i: px_of(rid, side) for d_i, rid, side in dies}
    evs = assemble(fr, die_bnd)
    led = event_ledger(stem, lens, kind, tape, evs, C.toll_bps_for(stem)[0], cells=True,
                       twins=False)
    return {"boxes": boxes, "info": info, "machine": nm, "ledger": led}


def box_rows(stem, lens, kind, draw, d: dict) -> list[dict]:
    rows = []
    for bx, m in zip(d["boxes"], d["machine"]["boxes"]):
        rows.append({"asset": stem, "lens": lens, "scale_kind": kind, "draw": int(draw),
                     "box": int(bx.box), "src_rid": int(bx.src_rid),
                     "confirm_i": int(bx.confirm_i), "life": int(bx.life),
                     "sched_end": int(bx.confirm_i + bx.life), "height_atr": float(bx.height_atr),
                     "u": float(bx.u), "censored": bool(bx.censored), "fate": str(m["fate"]),
                     "die_i": int(m["die_i"]), "die_side": str(m["die_side"]),
                     "n_harden": int(m["n_harden"]),
                     "lead_gap_swapped": bool(d["info"]["lead_gap_swapped"]),
                     "identity_perm": bool(d["info"]["identity_perm"])})
    return rows


def _null_values(res: dict) -> dict:
    """{(event, cell, direction, era, horizon): {n, median_term, net, hit_rate_net}}."""
    out = {}
    for (e, law, cell, direction), rs in res.items():
        for r in rs:
            out[(e, cell, direction, r["era"], r["horizon"])] = {
                "n": int(r["n"]), **{s: r[s] for s in NULL_STATS}}
    return out


# ═══════════════════════════════════════════════ 7 · ONE UNIT
def _pooled_scale(stems, lens, kind) -> float:
    sc = sorted({N.scale_of(s, lens, kind) for s in stems})
    return sc[0] if len(sc) == 1 else NaN


EV_KEYCOLS = ("event", "cell_law", "cell", "direction")
BASE_KEYCOLS = ("cell_law", "cell", "direction")


def asset_real(stem: str, panel: str, lens: str, kind: str) -> dict:
    """ONE asset's real side: its events, their grid rows (C.grid_rows per cell),
    its base ledger and base rows — the unit's per-asset step, callable alone
    (the fixtures rebuild it under a mutation)."""
    ev = real_events(stem, lens, kind)
    bps, src = C.toll_bps_for(stem)
    sm = N.scale_of(stem, lens, kind)
    lab = _labels([stem], lens, kind)
    g_ev = event_groups(ev, panel, lens)
    ev_rows = packed_rows(ev, g_ev, stem, lens, kind, sm, bps, src)
    gdf = _attach_insample(_rows_frame(ev_rows, EV_KEYCOLS), ev, g_ev, EV_KEYCOLS)
    bl = base_ledger(stem, lens, kind)
    g_b = base_groups(bl, panel, lens)
    base_rows = packed_rows(bl, g_b, stem, lens, kind, sm, bps, src)
    bdf = _attach_insample(_rows_frame(base_rows, BASE_KEYCOLS), bl, g_b, BASE_KEYCOLS)
    return {"events": ev, "ev_rows": ev_rows, "base_led": bl, "base_rows": base_rows,
            "grid": gdf.assign(asset=stem, lens=lens, scale_kind=kind, **lab),
            "base": bdf.assign(asset=stem, lens=lens, scale_kind=kind, **lab)}


SCAN_COLS_R4 = ["band", "die_i", "rid", "side", "dir", "seq", "touch_i", "known_at",
                "known_close_ms", "verdict", "is_first_hold", "pick_window", "scale_in_sample",
                "stability_changed"]


def _era_known(close_ms: np.ndarray) -> np.ndarray:
    """era by the row's known_at CLOSE [L-1.3]; 'beyond_pin' where that close is not
    on the tape (a truncated verdict's touch + hold passes the last closed bar)."""
    c = np.asarray(close_ms, dtype=np.int64)
    return np.where(c < 0, "beyond_pin", E.era_of(c)).astype(object)


def asset_scan(stem: str, lens: str, kind: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """[R4-10] THE SCAN LEDGER of one (asset, lens, scale): every evaluated touch of
    N's first-retest scan (N.first_retest_scan, verbatim) and every death of
    N.events with, per band, its evaluated-touch count and how its scan ended."""
    sc = N.first_retest_scan(stem, lens, kind)[SCAN_COLS_R4].reset_index(drop=True)
    sc["era"] = _era_known(sc["known_close_ms"].to_numpy())
    D = N.events(stem, lens, kind)["deaths"]
    dd = pd.DataFrame({"rid": D["rid"].to_numpy(np.int64), "side": D["side"].astype(str),
                       "die_i": D["die_i"].to_numpy(np.int64), "dir": D["dir"].to_numpy(np.int64),
                       "known_at": D["known_at"].to_numpy(np.int64),
                       "known_close_ms": D["known_close_ms"].to_numpy(np.int64),
                       "boundary": D["boundary"].to_numpy(float),
                       "atr_known": D["atr_known"].to_numpy(float),
                       "pick_window": D["pick_window"].to_numpy(),
                       "scale_in_sample": D["scale_in_sample"].to_numpy(bool)})
    dd["era"] = _era_known(dd["known_close_ms"].to_numpy())
    key = list(zip(dd["rid"], dd["side"]))
    for band in SCAN_BANDS_R4:
        g = sc[sc["band"] == band].sort_values(["rid", "side", "seq"], kind="mergesort")
        cnt = g.groupby(["rid", "side"], sort=True).size().to_dict()
        last = g.groupby(["rid", "side"], sort=True)["verdict"].last().to_dict()
        hold = (g[g["is_first_hold"]].set_index(["rid", "side"])["touch_i"].to_dict())
        slug = BAND_SLUG[band]
        dd[f"n_touches_{slug}"] = np.array([int(cnt.get(k, 0)) for k in key], dtype=np.int64)
        dd[f"end_{slug}"] = np.array(
            [("no-touch" if k not in last else "failed-out" if last[k] == "failed"
              else str(last[k])) for k in key], dtype=object)
        dd[f"hold_touch_i_{slug}"] = np.array([int(hold.get(k, -1)) for k in key], dtype=np.int64)
    for df in (sc, dd):
        df.insert(0, "asset", stem)
        df.insert(1, "lens", lens)
        df.insert(2, "scale_kind", kind)
    return sc, dd


def pooled_rows(panel: str, lens: str, kind: str, stems, led: pd.DataFrame, groups: list,
                rows_by: dict, keycols: tuple) -> pd.DataFrame:
    """The pool's rows: C.grid_rows on the pooled ledger with the members' rows of
    the same cell as `tolls` (the binding toll)."""
    tolls = {key: pd.DataFrame([r for s in stems for r in rows_by[s][key]])
             for key, _ in groups}
    res = packed_rows(led, groups, POOL[panel], lens, kind, _pooled_scale(stems, lens, kind),
                      None, "per asset — see the asset rows", tolls=tolls)
    df = _attach_insample(_rows_frame(res, keycols), led, groups, keycols)
    return df.assign(asset=POOL[panel], lens=lens, scale_kind=kind,
                     **_labels(stems, lens, kind))


def asset_null(stem: str, panel: str, lens: str, kind: str, n_draws: int = K_DRAWS,
               seeds: tuple = NULL_SEEDS) -> dict:
    """ONE asset's null: every draw of every seed -> (its record-law rows, its
    ledger); the seed-of-record boxes."""
    tape = N.load11(stem, lens)
    b = N.bundle11(stem, lens, kind)
    real = NL.real_box_set(tape, b["v2"]["macro"])
    bands = band_memo(tape)
    bps, src = C.toll_bps_for(stem)
    sm = N.scale_of(stem, lens, kind)
    rec_cells = [(e, law, c) for (e, law, c) in event_cells(panel, lens) if law == "record"]
    vals, boxes = {}, []
    for seed in seeds:
        for draw in range(n_draws):
            d = null_draw(stem, lens, kind, tape, real, draw, seed, bands)
            if seed == seeds[0]:
                boxes += box_rows(stem, lens, kind, draw, d)
            g = event_groups(d["ledger"], panel, lens, rec_cells)
            vals[(seed, draw)] = (packed_rows(d["ledger"], g, stem, lens, kind, sm, bps, src),
                                  d["ledger"])
    return {"vals": vals, "boxes": boxes, "real": real}


def compute_unit(unit: str, n_draws: int = K_DRAWS, seeds: tuple = NULL_SEEDS,
                 stems=None) -> dict:
    """Everything one (panel, lens, scale) unit files, as frames — no I/O but the
    snapshot and the filed picks."""
    panel, lens, kind = _parse_unit(unit)
    stems = PANELS[panel] if stems is None else tuple(stems)
    pool = POOL[panel]
    t0 = time.perf_counter()
    A = {}
    for s in stems:
        A[s] = asset_real(s, panel, lens, kind)
        clock(f"{unit} {s}: real events {len(A[s]['events'])} · base "
              f"{len(A[s]['base_led'])} anchors · {time.perf_counter() - t0:.1f}s")
    pooled_ev = pd.concat([A[s]["events"] for s in stems], ignore_index=True)
    g_ev = event_groups(pooled_ev, panel, lens)
    gp = pooled_rows(panel, lens, kind, stems, pooled_ev, g_ev,
                     {s: A[s]["ev_rows"] for s in stems}, EV_KEYCOLS)
    pooled_b = pd.concat([A[s]["base_led"] for s in stems], ignore_index=True)
    g_b = base_groups(pooled_b, panel, lens)
    bp = pooled_rows(panel, lens, kind, stems, pooled_b, g_b,
                     {s: A[s]["base_rows"] for s in stems}, BASE_KEYCOLS)
    del pooled_b
    grid = pd.concat([A[s]["grid"] for s in stems] + [gp], ignore_index=True)
    base = pd.concat([A[s]["base"] for s in stems] + [bp], ignore_index=True)
    events = pd.concat([A[s]["events"] for s in stems], ignore_index=True)
    del A
    sd = [asset_scan(s, lens, kind) for s in stems]
    scan = pd.concat([x[0] for x in sd], ignore_index=True)
    deaths = pd.concat([x[1] for x in sd], ignore_index=True)
    clock(f"{unit}: pooled real + base · {time.perf_counter() - t0:.1f}s")
    # THE NULL
    rec_cells = [(e, law, c) for (e, law, c) in event_cells(panel, lens) if law == "record"]
    vals, boxes = {}, []
    for s in stems:
        nu = asset_null(s, panel, lens, kind, n_draws, seeds)
        boxes += nu["boxes"]
        for k, v in nu["vals"].items():
            vals[(s,) + k] = v
        clock(f"{unit} {s}: null {n_draws} draws x {len(seeds)} seeds · "
              f"{time.perf_counter() - t0:.1f}s")
    for seed in seeds:
        for draw in range(n_draws):
            pl = pd.concat([vals[(s, seed, draw)][1] for s in stems], ignore_index=True)
            g = event_groups(pl, panel, lens, rec_cells)
            tolls = {key: pd.DataFrame([r for s in stems for r in vals[(s, seed, draw)][0][key]])
                     for key, _ in g}
            rr = packed_rows(pl, g, pool, lens, kind, _pooled_scale(stems, lens, kind), None,
                             "per asset — see the asset rows", tolls=tolls)
            vals[(pool, seed, draw)] = (rr, None)
    nulls = []
    for a in list(stems) + [pool]:
        for seed in seeds:
            for draw in range(n_draws):
                for key, v in _null_values(vals[(a, seed, draw)][0]).items():
                    nulls.append({"asset": a, "lens": lens, "scale_kind": kind,
                                  "seed": int(seed), "draw": int(draw),
                                  "event": key[0], "cell": key[1], "direction": key[2],
                                  "era": key[3], "horizon": key[4], **v})
    clock(f"{unit}: null pooled · {time.perf_counter() - t0:.1f}s")
    return {"events": events, "grid": grid, "base": base,
            "null_draws": pd.DataFrame(nulls), "null_boxes": pd.DataFrame(boxes),
            "scan": scan, "deaths": deaths}


PART_NAMES = ("events", "grid", "base", "null_draws", "null_boxes", "scan", "deaths")


def _unit_dir(parts: Path, unit: str) -> Path:
    return Path(parts) / unit.replace(":", "__")


def write_unit(unit: str, parts: Path) -> None:
    fr = compute_unit(unit)
    d = _unit_dir(parts, unit)
    d.mkdir(parents=True, exist_ok=True)
    for name in PART_NAMES:
        fr[name].to_parquet(str(d / f"{name}.parquet"), index=False)
    (d / "DONE").write_text(unit + "\n", encoding="utf-8")


def read_unit(unit: str, parts: Path) -> dict:
    d = _unit_dir(parts, unit)
    if not (d / "DONE").exists():
        raise SystemExit(f"HALT: unit {unit} has no finished part under {parts} — the grid "
                         f"is filed WHOLE or not at all")
    return {name: pd.read_parquet(str(d / f"{name}.parquet")) for name in PART_NAMES}


# ═══════════════════════════════════════════════ 8 · THE MERGE
def _collar(df: pd.DataFrame) -> pd.DataFrame:
    d = df.copy()
    for k, v in COLLAR.items():
        d[k] = v
    d["m_selections_this_table"] = int(len(d))
    return d


def _stamp(df: pd.DataFrame, by_cols=("asset", "lens")) -> pd.DataFrame:
    """C.stamp per (asset | pool, lens) group: the nine as-of columns."""
    parts = []
    for (a, L), g in df.groupby(list(by_cols), sort=True):
        members = (PANELS["CLASSIC5"] if a == POOL["CLASSIC5"] else
                   PANELS["UNSEEN12"] if a == POOL["UNSEEN12"] else (a,))
        metas = [N.load11(s, L).meta for s in members]
        parts.append(C.stamp(g, metas, L, a if a.startswith("POOLED:") else f"ASSET:{a}"))
    return pd.concat(parts, ignore_index=True) if parts else df


def _base_join(grid: pd.DataFrame, base: pd.DataFrame) -> pd.DataFrame:
    """Each event row beside its base rows [R4-5]."""
    b = base.set_index(BASE_KEY)
    fam = grid["event"].str.split("_").str[0]

    def pull(law, cell, prefix):
        idx = pd.MultiIndex.from_arrays([grid["asset"], grid["lens"], grid["scale_kind"], law,
                                         cell, grid["direction"], grid["era"], grid["horizon"]])
        sub = b.reindex(idx)
        return {f"{prefix}_law": np.asarray(law, dtype=object),
                f"{prefix}_n": sub["n"].to_numpy(),
                f"{prefix}_median_term": sub["median_term"].to_numpy(float),
                f"{prefix}_toll_atr": sub["toll_atr"].to_numpy(float),
                f"{prefix}_net": sub["net"].to_numpy(float)}
    g = grid.copy()
    law_all = np.array(["record"] * len(g), dtype=object)
    cell_all = np.array(["ALL"] * len(g), dtype=object)
    for k, v in pull(law_all, cell_all, "base_all").items():
        g[k] = v
    cl = np.array([CELL_BASE_LAW[x] for x in g["cell_law"]], dtype=object)
    for k, v in pull(cl, g["cell"].to_numpy(), "base_cell").items():
        g[k] = v
    has = g["cell"].isin(PARTITION).to_numpy()
    sl = np.array([SIDE_BASE_LAW[(f, law)] if h else "record"
                   for f, law, h in zip(fam, g["cell_law"], has)], dtype=object)
    for k, v in pull(sl, g["cell"].to_numpy(), "base_side").items():
        g[k] = v
    nd = C.ROUND_ND
    for p in ("base_all", "base_cell", "base_side"):
        g[f"{p}_n"] = pd.array(g[f"{p}_n"], dtype="Int64")
        # struck on the FILED (8 dp) figures, so the identity holds on the row a reader opens
        g[f"net_minus_{p}"] = (np.round(g["net"].to_numpy(float), nd)
                               - np.round(g[f"{p}_net"].to_numpy(float), nd))
    return g


def _wide_draws(nd: pd.DataFrame, seed: int, keys: pd.DataFrame, n_draws: int) -> dict:
    """{col: (cells, K) array} of one seed's draws, aligned to `keys` (sorted by
    NULL_KEY).  HALTS unless every cell holds exactly draws 0..K-1."""
    x = nd[nd["seed"] == seed].sort_values(NULL_KEY + ["draw"], kind="mergesort")
    if len(x) != len(keys) * n_draws:
        raise SystemExit(f"HALT: null seed {seed}: {len(x)} draw rows for {len(keys)} cells x "
                         f"{n_draws} draws — the null is filed whole or not at all")
    head = x.iloc[::n_draws][NULL_KEY].reset_index(drop=True)
    if not head.equals(keys.reset_index(drop=True)):
        raise SystemExit(f"HALT: null seed {seed}: the draw cells are not the real grid's cells")
    dr = x["draw"].to_numpy(np.int64).reshape(-1, n_draws)
    if not (dr == np.arange(n_draws)[None, :]).all():
        raise SystemExit(f"HALT: null seed {seed}: a cell does not hold draws 0..{n_draws - 1}")
    # the FILED (8 dp) draw values: every summary figure is an exact function of
    # bytes a reader can open (TC10 summarise's law)
    return {c: np.round(x[c].to_numpy(float), C.ROUND_ND).reshape(-1, n_draws)
            for c in ("n",) + NULL_STATS}


def _pctile(V: np.ndarray, rv: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    ok = np.isfinite(V)
    nv = ok.sum(axis=1)
    with np.errstate(invalid="ignore", divide="ignore"):
        less = ((V < rv[:, None]) & ok).sum(axis=1)
        eq = ((V == rv[:, None]) & ok).sum(axis=1)
        pc = 100.0 * (less + 0.5 * eq) / nv
    return np.where((nv > 0) & np.isfinite(rv), pc, np.nan), nv


def null_summary(grid: pd.DataFrame, nd: pd.DataFrame, n_draws: int = K_DRAWS) -> pd.DataFrame:
    """One row per real grid cell of law record [R4-6]: the real value beside the
    null's distribution over the VALID draws (median, q25, q75, IQR, min, max),
    the mid-rank percentile (PCTILE_LAW), every draw's n and NET, and the
    sensitivity seed's NET median / percentile beside."""
    import warnings
    real = (grid[grid["cell_law"] == "record"].sort_values(NULL_KEY, kind="mergesort")
            .reset_index(drop=True))
    keys = real[NULL_KEY]
    W = _wide_draws(nd, SEED, keys, n_draws)
    S = _wide_draws(nd, SEED_SENS, keys, n_draws)
    out = keys.copy()
    out["real_n"] = real["n"].to_numpy(np.int64)
    out["null_n_median"] = np.median(W["n"], axis=1)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        for stat in NULL_STATS:
            V = W[stat]
            rv = np.round(real[stat].to_numpy(float), C.ROUND_ND)
            pc, nv = _pctile(V, rv)
            out[f"real_{stat}"] = rv
            out[f"n_draws_valid_{stat}"] = nv.astype(np.int64)
            q25 = np.nanquantile(V, 0.25, axis=1)
            q75 = np.nanquantile(V, 0.75, axis=1)
            out[f"null_median_{stat}"] = np.nanmedian(V, axis=1)
            out[f"null_q25_{stat}"] = q25
            out[f"null_q75_{stat}"] = q75
            out[f"null_iqr_{stat}"] = q75 - q25
            out[f"null_min_{stat}"] = np.nanmin(V, axis=1)
            out[f"null_max_{stat}"] = np.nanmax(V, axis=1)
            out[f"real_pctile_in_null_{stat}"] = pc
        rvn = np.round(real["net"].to_numpy(float), C.ROUND_ND)
        spc, snv = _pctile(S["net"], rvn)
        out["sens_seed"] = int(SEED_SENS)
        out["sens_n_draws_valid_net"] = snv.astype(np.int64)
        out["sens_null_median_net"] = np.nanmedian(S["net"], axis=1)
        out["sens_real_pctile_in_null_net"] = spc
    for i in range(n_draws):
        out[f"n_d{i:02d}"] = W["n"][:, i].astype(np.int64)
        out[f"net_d{i:02d}"] = W["net"][:, i]
    nvn = out["n_draws_valid_net"].to_numpy()
    out["nan_reason"] = np.where(~np.isfinite(rvn), "the real row has no scored event",
                                 np.where(nvn == 0, "no null draw produced a scored event", ""))
    out["pctile_law"] = PCTILE_LAW
    out["seed"] = int(SEED)
    out["n_draws"] = int(n_draws)
    out["schedule_variant"] = SCHEDULE_VARIANT
    for c in ("l_pick_window", "l_stability_changed", "u_pick_window", "u_stability_changed"):
        out[c] = real[c].to_numpy()
    return out


def _canon(df: pd.DataFrame, key: list) -> pd.DataFrame:
    return C.canon(df, key)


def content_sha(df: pd.DataFrame) -> str:
    return C.content_sha(df)


def _put(df: pd.DataFrame, name: str, out: Path) -> tuple[str, pd.DataFrame]:
    """canon (8 dp, total key order, HALT on a duplicate key) -> atomic parquet
    through pandas on a path string [AM-2] -> content sha."""
    d = _canon(df, TABLE_KEYS[name])
    p = out / f"{name}.parquet"
    tmp = out / f"{name}.parquet.tmp"
    d.to_parquet(str(tmp), index=False)
    os.replace(str(tmp), str(p))
    return content_sha(d), d


def _sha_file(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def input_shas() -> dict:
    out = {}
    for p in PANELS:
        for s in PANELS[p]:
            for L in sorted(set(LENSES_R4[p]) | {N.LADDER[x] for x in LENSES_R4[p]
                                                 if N.LADDER[x] in N.LENSES_OF[s]}):
                m = N.load11(s, L).meta
                out[f"{s}|{L}"] = {"source_file": m["source_file"],
                                   "source_sha256": m["source_sha256"]}
    return out


def code_shas() -> dict:
    files = {"scripts/tierc11_stage_r4.py": Path(__file__).resolve(),
             "scripts/tierc11_nest.py": ROOT / "scripts" / "tierc11_nest.py",
             "scripts/tierc11_env.py": ROOT / "scripts" / "tierc11_env.py",
             "scripts/tierc10_census.py": ROOT / "scripts" / "tierc10_census.py",
             "scripts/tierc10_null.py": ROOT / "scripts" / "tierc10_null.py",
             "analytics/rangefinder_census.py": ROOT / "analytics" / "rangefinder_census.py",
             "engine/indicators.py": ROOT / "engine" / "indicators.py"}   # EMA / ATR
    return {k: _sha_file(v) for k, v in files.items()}


# ═══════════════════════════════════════════════ 9 · TC10 CONTINUITY [AM-1]
def tc10_filed_rows() -> pd.DataFrame:
    g = pd.read_parquet(str(E.tc10_record(OUTCOME_GRID_REL)))
    sel = g[(g["asset"] == TC10_CONT["asset"]) & (g["lens"] == TC10_CONT["lens"])
            & (g["cls"] == TC10_CONT["cls"]) & (g["scale_kind"] == TC10_CONT["scale_kind"])
            & (g["horizon"] == TC10_CONT["horizon"])]
    return sel[["era", "n_events", "n", "n_censored", "median_term", "toll_atr",
                "net"]].reset_index(drop=True)


def tc10_replay() -> dict:
    """The TC10 window REPLAYED in TC11 code: 4h tapes cut at 2026-09-21T16:00Z,
    C.run_scale at 3.0, C.retest_holds on tap89 with C.RETEST_PINS, the hold rows
    through C.outcome_ledger and C.grid_rows (per asset, then pooled with the
    binding toll)."""
    rp = C.RETEST_PINS
    per, leds, evs = [], [], []
    for s in PANELS["CLASSIC5"]:
        tape = N.load11(s, "4h")
        n10 = int(((tape.t0 + tape.step) <= TC10_PIN_MS).sum())
        t10 = tape.head(n10)
        v2 = C.run_scale(t10, float(C.FROZEN_SCALE))
        dies = N._dies(v2["macro"])
        lo, hi = C.band_of("tap89")(t10.c)
        got = [g for g in C.retest_holds(t10, dies, lo, hi, float(rp["margin_atr"]),
                                         int(rp["hold_bars"]), int(rp["ttl_bars"]))
               if g["verdict"] == "hold"]
        evf = pd.DataFrame({"cls": "retest-hold-tap89",
                            "i": [g["touch_i"] for g in got],
                            "known_at": [g["known_at"] for g in got],
                            "rid": [g["rid"] for g in got], "side": [g["side"] for g in got],
                            "sgn": [N.UP[g["side"]] for g in got]})
        for k in ("i", "known_at", "rid", "sgn"):
            evf[k] = evf[k].astype(np.int64)
        bps, src = C.toll_bps_for(s)
        led = _round_led(C.outcome_ledger(t10, evf, _stub_view(t10.n), bps)).assign(asset=s)
        leds.append(led)
        per += [dict(r, asset=s) for r in C.grid_rows(led, s, "4h", "frozen3.0",
                                                     float(C.FROZEN_SCALE), bps, src)
                if r["cls"] == "retest-hold-tap89"]
        evs += [{"asset": s, "die_i": int(g["die_i"]), "touch_i": int(g["touch_i"]),
                 "known_at": int(g["known_at"]), "n10": n10} for g in got]
    tolls = pd.DataFrame(per)
    led = pd.concat(leds, ignore_index=True)
    pooled = [r for r in C.grid_rows(led, "POOLED:CLASSIC5", "4h", "frozen3.0",
                                     float(C.FROZEN_SCALE), None, "per asset", tolls=tolls)
              if r["cls"] == "retest-hold-tap89" and r["horizon"] == "H20"]
    return {"pooled": pooled, "ledger": led, "events": pd.DataFrame(evs)}


def continuity(grid: pd.DataFrame, events: pd.DataFrame) -> dict:
    filed = tc10_filed_rows()
    rep = tc10_replay()
    tc11 = grid[(grid["asset"] == "POOLED:CLASSIC5") & (grid["lens"] == "4h")
                & (grid["scale_kind"] == "frozen3.0") & (grid["event"] == "BRK_tap89_oneshot")
                & (grid["cell_law"] == "record") & (grid["cell"] == "ALL")
                & (grid["direction"] == "both") & (grid["horizon"] == "H20")]
    out = {"filed": {}, "replay": {}, "tc11": {}, "replay_equals_filed": True}
    for era in ERAS:
        f = filed[filed["era"] == era].iloc[0]
        r = next(x for x in rep["pooled"] if x["era"] == era)
        t = tc11[tc11["era"] == era].iloc[0]
        out["filed"][era] = {"n": int(f["n"]), "n_events": int(f["n_events"]),
                             "median_term": float(f["median_term"]),
                             "toll_atr": float(f["toll_atr"]), "net": float(f["net"])}
        out["replay"][era] = {"n": int(r["n"]), "n_events": int(r["n_events"]),
                              "median_term": round(float(r["median_term"]), 8),
                              "toll_atr": round(float(r["toll_atr"]), 8),
                              "net": round(float(r["net"]), 8)}
        out["tc11"][era] = {"n": int(t["n"]), "n_events": int(t["n_events"]),
                            "median_term": round(float(t["median_term"]), 8),
                            "toll_atr": round(float(t["toll_atr"]), 8),
                            "net": round(float(t["net"]), 8)}
        for k in ("n", "n_events", "median_term", "toll_atr", "net"):
            if out["replay"][era][k] != round(out["filed"][era][k], 8):
                out["replay_equals_filed"] = False
    # the decomposition over the 20 extra 4h bars
    ev11 = events[(events["lens"] == "4h") & (events["scale_kind"] == "frozen3.0")
                  & (events["event"] == "BRK_tap89_oneshot")
                  & events["asset"].isin(PANELS["CLASSIC5"])]
    k11 = {(a, int(d), int(t)): (bool(c), float(x), int(ka)) for a, d, t, c, x, ka in
           zip(ev11["asset"], ev11["die_i"], ev11["anchor_i"], ev11["cens_H20"],
               ev11["term_H20"], ev11["known_at"])}
    L10 = rep["ledger"]
    k10 = {(a, int(d), int(t)): (bool(c), float(x), int(ka)) for a, d, t, c, x, ka in
           zip(L10["asset"], rep["events"]["die_i"], L10["i"], L10["cens_H20"],
               L10["term_H20"], L10["known_at"])}
    both = sorted(set(k11) & set(k10))
    same = [k for k in both if (k10[k][0] and k11[k][0]) or
            (not k10[k][0] and not k11[k][0] and k10[k][1] == k11[k][1])]
    uncens = [k for k in both if k10[k][0] and not k11[k][0]]
    moved = [k for k in both if k not in same and k not in uncens]
    only11 = sorted(set(k11) - set(k10))
    only10 = sorted(set(k10) - set(k11))
    n10 = {s: int(((N.load11(s, "4h").t0 + LENS_MS4H) <= TC10_PIN_MS).sum())
           for s in PANELS["CLASSIC5"]}
    n11 = {s: N.load11(s, "4h").n for s in PANELS["CLASSIC5"]}
    new_deaths, last_known, gaps_ = [], {}, []
    for s_ in PANELS["CLASSIC5"]:
        ev_ = N.events(s_, "4h", "frozen3.0")
        os_ = ev_["oneshot"][ev_["oneshot"]["band"] == "tap89"]
        for r_ in ev_["deaths"].itertuples(index=False):
            if int(r_.die_i) >= n10[s_] - 1:
                o = os_[os_["die_i"] == int(r_.die_i)]
                new_deaths.append(f"{s_} {r_.side} death at bar {int(r_.die_i)} (TC10 window "
                                  f"ends at bar {n10[s_] - 1}; TC11 at {n11[s_] - 1}): tap89 "
                                  f"one-shot {o['verdict'].iloc[0] + ' at touch ' + str(int(o['touch_i'].iloc[0])) if len(o) else 'not yet retested at the pin'}")
        ka = [v[2] for k_, v in k11.items() if k_[0] == s_]
        if ka:
            gaps_.append(n10[s_] - 1 - max(ka))
        last_known[s_] = (f"last tap89 one-shot hold known at bar {max(ka)} = "
                          f"{n10[s_] - 1 - max(ka)} bars before the TC10 window's last bar"
                          if ka else "none")
    out["decomposition"] = {
        "new_deaths_rows": new_deaths, "last_hold_rows": [f"{a}: {t}" for a, t in
                                                          last_known.items()],
        "min_bars_before_edge": int(min(gaps_)) if gaps_ else None,
        "extra_4h_bars": {s: n11[s] - n10[s] for s in PANELS["CLASSIC5"]},
        "events_tc10_window": len(k10), "events_tc11": len(k11), "in_both": len(both),
        "in_both_same_h20": len(same), "in_both_censored_at_tc10_uncensored_now": len(uncens),
        "in_both_term_moved": len(moved),
        "only_tc11": len(only11),
        "only_tc11_known_after_tc10_pin": sum(1 for k in only11
                                               if k11[k][2] >= n10[k[0]]),
        "only_tc10_window": len(only10),
        "only_tc11_rows": [f"{a} die {d} touch {t} known {k11[(a, d, t)][2]} "
                           f"(TC10 window ends at bar {n10[a] - 1})" for a, d, t in only11],
        "uncensored_rows": [f"{a} die {d} touch {t} known {k11[(a, d, t)][2]} term_H20 "
                            f"{k11[(a, d, t)][1]:+.6f}" for a, d, t in uncens],
        "only_tc10_rows": [f"{a} die {d} touch {t}" for a, d, t in only10],
        "moved_rows": [f"{a} die {d} touch {t}" for a, d, t in moved],
    }
    return out


LENS_MS4H = N.LENS_MS["4h"]


# ═══════════════════════════════════════════════ 10 · THE REPORTS
def _f(x, nd=3, sign=True) -> str:
    try:
        v = float(x)
    except (TypeError, ValueError):
        return str(x)
    if not np.isfinite(v):
        return "—"
    return f"{v:+.{nd}f}" if sign else f"{v:.{nd}f}"


def _i(x) -> str:
    try:
        return "—" if pd.isna(x) else str(int(x))
    except (TypeError, ValueError):
        return str(x)


def _wide(grid: pd.DataFrame, asset, laws=None, kinds=SCALE_KINDS, lenses=None,
          cells=None) -> list:
    """One md line per (lens, scale, event, law, cell, direction): n / NET / Δ vs
    the cell base for every era x horizon — WHOLE over its declared scope.  `asset`
    = one asset | pool, or a tuple of them (then an asset column leads)."""
    many = isinstance(asset, tuple)
    assets = asset if many else (asset,)
    g = grid[grid["asset"].isin(assets)]
    if laws is not None:
        g = g[g["cell_law"].isin(laws)]
    g = g[g["scale_kind"].isin(kinds)]
    if lenses is not None:
        g = g[g["lens"].isin(lenses)]
    if cells is not None:
        g = g[g["cell"].isin(cells)]
    idx = g.set_index(["asset", "lens", "scale_kind", "event", "cell_law", "cell", "direction",
                       "era", "horizon"])
    head = (["asset"] if many else []) + ["lens", "scale", "event", "law", "L+1 cell", "dir"]
    for era in ERAS:
        for h in HORIZONS:
            head += [f"n {era} {h}", f"NET {era} {h}", f"Δcell {era} {h}"]
    L = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    keys = (g[["asset", "lens", "scale_kind", "event", "cell_law", "cell", "direction"]]
            .drop_duplicates())
    order = {"asset": {x: i for i, x in enumerate(assets)},
             "lens": {x: i for i, x in enumerate(("1h", "4h", "12h", "1d"))},
             "scale_kind": {x: i for i, x in enumerate(SCALE_KINDS)},
             "event": {x: i for i, x in enumerate(EVENTS)},
             "cell_law": {x: i for i, x in enumerate(("record", "mem_twin", "post_redraw"))},
             "cell": {x: i for i, x in enumerate(("ALL",) + PARTITION + ("NA",))},
             "direction": {x: i for i, x in enumerate(DIRECTIONS)}}
    keys = keys.assign(**{f"_o{c}": keys[c].map(m) for c, m in order.items()}).sort_values(
        [f"_o{c}" for c in order])
    for r in keys.itertuples(index=False):
        k6 = (r.asset, r.lens, r.scale_kind, r.event, r.cell_law, r.cell, r.direction)
        star = "*" if r.cell in N.STARRED else ""
        cells = (([r.asset] if many else [])
                 + [r.lens, r.scale_kind, r.event, r.cell_law, r.cell + star, r.direction])
        for era in ERAS:
            for h in HORIZONS:
                x = idx.loc[k6 + (era, h)]
                cells += [_i(x["n"]), _f(x["net"]), _f(x["net_minus_base_cell"])]
        L.append("| " + " | ".join(cells) + " |")
    return L


def grid_md(grid: pd.DataFrame) -> str:
    L = [f"# TIER-C11 · STAGE R-b · R4_GRID — POOLED:CLASSIC5, WHOLE",
         "",
         f"as_of_last_closed_4h: {PIN_ISO} · substrate {E.SNAPSHOT.name} · seed {SEED} · "
         f"TIER-E · a SELECTION, not a result · gates nothing",
         "",
         "Every (lens, scale, event, cell law, L+1 cell, direction) of the POOLED:CLASSIC5 grid, "
         "one line each; every era x horizon in columns: n (uncensored anchors), NET = median "
         "term - the BINDING toll (ATR of the lens), Δcell = NET - the NET of the base rate "
         "anchored at every bar of the lens in the SAME L+1 cell (law record; mem_twin rows "
         "against the mem_twin base). Starred cells (*) are the contract's three. The per-asset "
         "rows, every other statistic (mean, q25/q75, hit rates, MFE/MAE, tolls, censoring), the "
         "own-side and unconditional base columns and the labels are in R4_GRID.parquet. "
         "`—` = no uncensored anchor (the row's nan_reason says why).",
         ""]
    L += _wide(grid, "POOLED:CLASSIC5")
    n = int(((grid["asset"] == "POOLED:CLASSIC5")).sum())
    L += ["", f"rows of the POOLED:CLASSIC5 grid printed above (x 3 eras x 2 horizons): {n}"]
    return "\n".join(L) + "\n"


def _counts_table(events: pd.DataFrame) -> list:
    head = ["panel", "lens", "scale", "event", "n ALL", "n tuning", "n holdout", "long",
            "short"]
    L = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    for p in PANELS:
        for lens in LENSES_R4[p]:
            for kind in SCALE_KINDS:
                for ev in EVENTS:
                    s = events[(events["asset"].isin(PANELS[p])) & (events["lens"] == lens)
                               & (events["scale_kind"] == kind) & (events["event"] == ev)]
                    L.append("| " + " | ".join([p, lens, kind, ev, str(len(s)),
                                                str(int((s["era"] == "tuning").sum())),
                                                str(int((s["era"] == "holdout").sum())),
                                                str(int((s["dir"] == 1).sum())),
                                                str(int((s["dir"] == -1).sum()))]) + " |")
    return L


def _base_table(base: pd.DataFrame, asset: str, kind: str) -> list:
    g = base[(base["asset"] == asset) & (base["scale_kind"] == kind)
             & (base["cell_law"] == "record")].set_index(BASE_KEY)
    head = ["lens", "L+1 cell", "dir"]
    for era in ERAS:
        for h in HORIZONS:
            head += [f"n {era} {h}", f"median {era} {h}", f"NET {era} {h}"]
    L = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    panel = "CLASSIC5" if asset == POOL["CLASSIC5"] else "UNSEEN12"
    for lens in LENSES_R4[panel]:
        for law, cell in base_cells(panel, lens):
            if law != "record":
                continue
            for d in DIRECTIONS:
                row = [lens, cell + ("*" if cell in N.STARRED else ""), d]
                for era in ERAS:
                    for h in HORIZONS:
                        x = g.loc[(asset, lens, kind, law, cell, d, era, h)]
                        row += [_i(x["n"]), _f(x["median_term"]), _f(x["net"])]
                L.append("| " + " | ".join(row) + " |")
    return L


def _null_table(null: pd.DataFrame, asset: str, kind: str, lenses) -> list:
    g = null[(null["asset"] == asset) & (null["scale_kind"] == kind)].set_index(NULL_KEY)
    head = ["lens", "event", "L+1 cell", "dir"]
    for era in ("ALL", "holdout"):
        for h in HORIZONS:
            head += [f"real NET {era} {h}", f"null med [q25, q75] {era} {h}",
                     f"pctile {era} {h}"]
    L = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    panel = "CLASSIC5" if asset == POOL["CLASSIC5"] else "UNSEEN12"
    for lens in lenses:
        for (ev, law, cell) in event_cells(panel, lens):
            if law != "record":
                continue
            for d in DIRECTIONS:
                row = [lens, ev, cell + ("*" if cell in N.STARRED else ""), d]
                for era in ("ALL", "holdout"):
                    for h in HORIZONS:
                        x = g.loc[(asset, lens, kind, ev, cell, d, era, h)]
                        row += [_f(x["real_net"]),
                                f"{_f(x['null_median_net'])} [{_f(x['null_q25_net'])}, "
                                f"{_f(x['null_q75_net'])}]",
                                _f(x["real_pctile_in_null_net"], 1, sign=False)]
                L.append("| " + " | ".join(row) + " |")
    return L


def _labels_table() -> list:
    head = ["asset", "lens", "pick of record", "window", "stability changed", "L+1",
            "L+1 pick", "L+1 window", "L+1 stability changed"]
    L = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    for p in PANELS:
        for s in PANELS[p]:
            for lens in LENSES_R4[p]:
                lab = N.scale_label(s, lens, "calibrated")
                U = N.LADDER[lens]
                ok = U is not None and U in N.LENSES_OF[s]
                ul = N.scale_label(s, U, "calibrated") if ok else None
                L.append("| " + " | ".join([
                    s, lens, str(N.scale_of(s, lens, "calibrated")), lab["pick_window"],
                    str(lab["stability_changed"]), U if ok else "NA",
                    str(N.scale_of(s, U, "calibrated")) if ok else "—",
                    ul["pick_window"] if ok else "—",
                    str(ul["stability_changed"]) if ok else "—"]) + " |")
    return L


def _scan_table(scan: pd.DataFrame, deaths: pd.DataFrame) -> list:
    """[R4-10] per panel x lens x scale x band: deaths, the scan's END per death,
    evaluated touches by verdict — WHOLE over the commission."""
    head = ["panel", "lens", "scale", "band", "deaths", "end hold (first hold)",
            "end truncated", "end failed-out", "end no-touch", "evaluated touches",
            "touches failed", "touches hold", "touches truncated"]
    L = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    for p in PANELS:
        for lens in LENSES_R4[p]:
            for kind in SCALE_KINDS:
                d = deaths[deaths["asset"].isin(PANELS[p]) & (deaths["lens"] == lens)
                           & (deaths["scale_kind"] == kind)]
                s = scan[scan["asset"].isin(PANELS[p]) & (scan["lens"] == lens)
                         & (scan["scale_kind"] == kind)]
                for band in SCAN_BANDS_R4:
                    e = d[f"end_{BAND_SLUG[band]}"]
                    v = s.loc[s["band"] == band, "verdict"]
                    L.append("| " + " | ".join(
                        [p, lens, kind, band, str(len(d))]
                        + [str(int((e == x).sum())) for x in SCAN_ENDS]
                        + [str(len(v))] + [str(int((v == x).sum()))
                                           for x in ("failed", "hold", "truncated")]) + " |")
    return L


def stage_md(grid, base, null, events, boxes, cont: dict, shas: dict, scan: pd.DataFrame,
             deaths: pd.DataFrame) -> str:
    L = [f"# TIER-C11 · STAGE R-b · R4 — THE TWO TRADES PER LENS (TIER-E, WHOLE)",
         "",
         f"as_of_last_closed_4h: {PIN_ISO} · substrate {E.SNAPSHOT.name} · seed {SEED} "
         f"(null sensitivity seed {SEED_SENS}) · K = {K_DRAWS} draws · schedule "
         f"{SCHEDULE_VARIANT} (ruling R10)",
         "",
         "**TIER-E · a SELECTION, not a result · gates nothing.** No row of this stage is a "
         "test or a verdict; no cell may be promoted to one. Every table below is WHOLE over "
         "the scope its caption declares; the parquets hold every asset row.",
         "",
         "## 0 · Scope — which file is the grid of record",
         "",
         f"- **The grid of record is `R4_GRID.parquet`** ({shas['R4_GRID']['rows']:,} rows = "
         f"exactly the declared cells, F-GRID) with its base rate `R4_BASE.parquet` "
         f"({shas['R4_BASE']['rows']:,}) and null `R4_NULL.parquet` "
         f"({shas['R4_NULL']['rows']:,}). The markdown tables are WHOLE only over the scope "
         f"each caption declares; a build document that quotes this stage quotes the parquets "
         f"for anything outside those scopes.",
         "- Printed here: §4 POOLED:CLASSIC5 · calibrated · law record (every lens x event x "
         "L+1 cell x direction); §5 POOLED:UNSEEN12 · calibrated · law record; §6 base "
         "POOLED:CLASSIC5 · calibrated · law record; §7 null POOLED:CLASSIC5 · calibrated · NET "
         "· eras ALL and holdout; §9 scan ledger per panel; §10 every ASSET (and both pools) · "
         "calibrated · law record · cell ALL (every lens x event x direction). `R4_GRID.md` "
         "prints POOLED:CLASSIC5 at both scales and every cell law.",
         "- In the parquets only: per-asset L+1-partitioned rows; POOLED:UNSEEN12 at frozen3.0 "
         "and its twin laws; every frozen3.0 per-asset row; the base twins (mem_twin, topside, "
         "botside, own_side_*) and every per-asset base row; the null's tuning era, its "
         "frozen3.0 scale, its per-asset rows and every statistic but NET; mean / q25 / q75 / "
         "hit rates / MFE / MAE / tolls / censoring on every row; the scan ledger per asset "
         "(R4_SCAN, R4_DEATHS).",
         "",
         "## Readings (lean block)", ""]
    L += [f"- {LEAN_TAG} {x}" for x in READINGS]
    L += ["", "## Files", "", "| file | rows | content sha256 (parquet: canonical csv) |",
          "|---|---|---|"]
    for name in ("R4_EVENTS", "R4_GRID", "R4_BASE", "R4_NULL", "R4_NULL_BOXES", "R4_SCAN",
                 "R4_DEATHS"):
        L.append(f"| {name}.parquet | {shas[name]['rows']} | {shas[name]['sha']} |")
    L += ["", "## 1 · TC10 continuity [AM-1] — frozen3.0 · one-shot · 4h · POOLED:CLASSIC5 · "
          "tap89 · H20 NET", "",
          "| era | TC10 filed n | TC10 filed NET | TC10 window replayed in TC11 code n | "
          "replay NET | TC11 n | TC11 NET | TC11 − TC10 |", "|---|---|---|---|---|---|---|---|"]
    for era in ERAS:
        f, r, t = cont["filed"][era], cont["replay"][era], cont["tc11"][era]
        L.append(f"| {era} | {f['n']} | {f['net']:+.6f} | {r['n']} | {r['net']:+.6f} | "
                 f"{t['n']} | {t['net']:+.6f} | {t['net'] - f['net']:+.6f} |")
    dcm = cont["decomposition"]
    L += ["", f"- replay == filed (n, n_events, median, toll, NET at 8 dp, every era): "
          f"**{cont['replay_equals_filed']}**.",
          f"- extra 4h bars per asset (TC11 pin 2026-09-25T00:00Z vs TC10 pin "
          f"2026-09-21T16:00Z): {dcm['extra_4h_bars']}.",
          f"- events: TC10 window {dcm['events_tc10_window']}, TC11 {dcm['events_tc11']}; in "
          f"both {dcm['in_both']} (H20 term identical or censored in both: "
          f"{dcm['in_both_same_h20']}; censored in the TC10 window and uncensored now: "
          f"{dcm['in_both_censored_at_tc10_uncensored_now']}; term moved: "
          f"{dcm['in_both_term_moved']}); only in TC11 {dcm['only_tc11']} (known after the "
          f"TC10 window: {dcm['only_tc11_known_after_tc10_pin']}); only in the TC10 window "
          f"{dcm['only_tc10_window']}."]
    for k in ("last_hold_rows", "new_deaths_rows", "uncensored_rows", "only_tc11_rows",
              "only_tc10_rows", "moved_rows"):
        for x in dcm[k]:
            L.append(f"  - {k.replace('_rows', '')}: {x}")
        if not dcm[k]:
            L.append(f"  - {k.replace('_rows', '')}: none")
    same = (all(cont["tc11"][e]["net"] == cont["filed"][e]["net"] for e in ERAS)
            and not dcm["only_tc11"] and not dcm["in_both_censored_at_tc10_uncensored_now"]
            and not dcm["in_both_term_moved"] and not dcm["only_tc10_window"])
    # every clause below is branched on the figure it states [verifier MINOR-2]
    deaths_clause = (
        "no CLASSIC5 macro death (frozen 3.0) falls in them" if not dcm["new_deaths_rows"] else
        f"the {len(dcm['new_deaths_rows'])} CLASSIC5 macro death(s) (frozen 3.0) at or after "
        f"the TC10 window's last bar (listed above) produced no tap89 one-shot hold known by the "
        f"pin")
    edge = dcm["min_bars_before_edge"]
    edge_clause = (f"every hold of the TC10 window was known at least {edge} bars before its "
                   f"edge (uncensored at H20 then)" if edge is not None and edge >= 20 else
                   f"the latest hold of the TC10 window was known {edge} bars before its edge")
    L.append(f"- explanation: " + (
        f"the 20 extra 4h bars move nothing in this cell — no tap89 one-shot hold becomes "
        f"known in them (only-TC11: none), {deaths_clause}, and {edge_clause} — so the event "
        f"set, every H20 term and every toll are the same; TC11 == TC10 at 8 dp."
        if same else
        "the difference is carried by the rows listed above (events new in the 20 extra bars, "
        "censored at H20 in the TC10 window and uncensored now, or a term moved)."))
    L += ["", "## 2 · Honesty labels per lens [L-R.2, AM-4]", ""]
    L += _labels_table()
    L += ["", "## 3 · Event counts, per panel (per-asset counts in R4_EVENTS.parquet)", ""]
    L += _counts_table(events)
    L += ["", "## 4 · The grid of record — POOLED:CLASSIC5 · calibrated · cell law record "
          "(whole over lens x event x L+1 cell x direction; frozen3.0 and the twin laws in "
          "R4_GRID.md)", ""]
    L += _wide(grid, "POOLED:CLASSIC5", laws=("record",), kinds=("calibrated",))
    L += ["", "## 5 · POOLED:UNSEEN12 · calibrated · cell law record (whole; 4h / 1d have no "
          "L+1 in the commission: cells ALL + NA)", ""]
    L += _wide(grid, "POOLED:UNSEEN12", laws=("record",), kinds=("calibrated",))
    L += ["", "## 6 · Base rate — POOLED:CLASSIC5 · calibrated · law record (every bar of L; "
          "whole over lens x cell x direction)", ""]
    L += _base_table(base, "POOLED:CLASSIC5", "calibrated")
    L += ["", "## 7 · Null (gaps+order, K = 20) — POOLED:CLASSIC5 · calibrated · law record · "
          "NET (whole over lens x event x cell x direction; eras ALL and holdout; tuning, "
          "every other statistic and the frozen twin in R4_NULL.parquet). The percentile is "
          "a DESCRIPTION, never a p-value.", ""]
    L += _null_table(null, "POOLED:CLASSIC5", "calibrated", LENSES_R4["CLASSIC5"])
    per_draw = boxes.groupby(["asset", "lens", "scale_kind", "draw"], sort=True).agg(
        boxes=("box", "size"), swapped=("lead_gap_swapped", "max"),
        identity=("identity_perm", "max")).reset_index()
    nb = per_draw.groupby(["asset", "lens", "scale_kind"], sort=True).agg(
        draws=("draw", "size"), boxes=("boxes", "first"), swapped=("swapped", "sum"),
        identity=("identity", "sum")).reset_index()
    L += ["", "## 8 · Null schedule diagnostics (seed of record; every (asset, lens, scale))",
          "", "| asset | lens | scale | draws | boxes per draw (= real confirmed ranges) | "
          "draws whose lead gap was swapped (< ATR_LEN) | draws whose schedule IS the real one "
          "|", "|---|---|---|---|---|---|---|"]
    for r in nb.itertuples(index=False):
        L.append(f"| {r.asset} | {r.lens} | {r.scale_kind} | {r.draws} | {r.boxes} | "
                 f"{int(r.swapped)} | {int(r.identity)} |")
    L += ["", "## 9 · Scan ledger [R4-10] — every evaluated touch (R4_SCAN) and every death "
          "(R4_DEATHS), per panel x lens x scale x band (whole; per asset in the parquets). "
          "END per death: hold = its first hold (the BREAKOUT event, rule first); truncated = a "
          "touch whose hold window passes the tape ended it; failed-out = every touch in the "
          "candidacy window failed; no-touch = no qualifying touch in the window. A truncated "
          "touch's known_at lies beyond the pin (era 'beyond_pin').", ""]
    L += _scan_table(scan, deaths)
    everyone = (tuple(PANELS["CLASSIC5"]) + (POOL["CLASSIC5"],) + tuple(PANELS["UNSEEN12"])
                + (POOL["UNSEEN12"],))
    L += ["", "## 10 · Appendix — every asset and both pools · calibrated · cell law record · "
          "L+1 cell ALL (whole over asset x lens x event x direction; n / NET / Δcell as in §4; "
          "the partitioned cells in R4_GRID.parquet)", ""]
    L += _wide(grid, everyone, laws=("record",), kinds=("calibrated",), cells=("ALL",))
    return "\n".join(L) + "\n"


# ═══════════════════════════════════════════════ 11 · MERGE + BUILD
def merge(parts: Path, out: Path) -> dict:
    t0 = time.perf_counter()
    out.mkdir(parents=True, exist_ok=True)
    fr = {name: [] for name in PART_NAMES}
    for u in UNITS:
        d = read_unit(u, parts)
        for name in PART_NAMES:
            fr[name].append(d[name])
    events = pd.concat(fr["events"], ignore_index=True)
    grid = pd.concat(fr["grid"], ignore_index=True)
    base = pd.concat(fr["base"], ignore_index=True)
    nd = pd.concat(fr["null_draws"], ignore_index=True)
    boxes = pd.concat(fr["null_boxes"], ignore_index=True)
    scan = pd.concat(fr["scan"], ignore_index=True)
    deaths = pd.concat(fr["deaths"], ignore_index=True)
    grid = _base_join(grid, base)
    null = null_summary(grid, nd)
    cont = continuity(grid, events)
    if not cont["replay_equals_filed"]:
        raise SystemExit(f"HALT: the TC10 window replayed in TC11 code does not equal TC10's "
                         f"filed outcome_grid row [AM-1]: {cont['replay']} vs {cont['filed']}")
    tables = {"R4_EVENTS": events, "R4_GRID": grid, "R4_BASE": base, "R4_NULL": null,
              "R4_NULL_BOXES": boxes, "R4_SCAN": scan, "R4_DEATHS": deaths}
    shas, filed = {}, {}
    for name, df in tables.items():
        d = _collar(_stamp(df))
        sha, dd = _put(d, name, out)
        shas[name] = {"sha": sha, "rows": int(len(dd))}
        filed[name] = dd
        clock(f"wrote {name} rows {len(dd):,} sha {sha[:16]}…")
    (out / "R4_GRID.md").write_text(grid_md(filed["R4_GRID"]), encoding="utf-8")
    (out / "STAGE_R4.md").write_text(
        stage_md(filed["R4_GRID"], filed["R4_BASE"], filed["R4_NULL"], filed["R4_EVENTS"],
                 filed["R4_NULL_BOXES"], cont, shas, filed["R4_SCAN"], filed["R4_DEATHS"]),
        encoding="utf-8")
    man = {
        "stage": "TIER-C11 · STAGE R-b · R4 (TC11-R)", "tier": "TIER-E",
        "selection_not_a_result": COLLAR["selection_not_a_result"], "gates": "nothing",
        "as_of_last_closed_4h": PIN_ISO, "as_of_close_ms": PIN_MS,
        "substrate": E.SNAPSHOT.name, "seed": SEED, "seed_sensitivity": SEED_SENS,
        "n_boot": "not used (no bootstrap in R4)", "k_draws": K_DRAWS,
        "schedule_variant": SCHEDULE_VARIANT,
        "commission": {"panels": {p: list(v) for p, v in PANELS.items()},
                       "lenses": {p: list(v) for p, v in LENSES_R4.items()},
                       "scale_kinds": list(SCALE_KINDS), "events": list(EVENTS),
                       "directions": list(DIRECTIONS), "eras": list(ERAS),
                       "horizons": [list(x) for x in C.HORIZONS], "partition": list(PARTITION),
                       "event_laws": {k: list(v) for k, v in EV_LAWS_L1.items()},
                       "base_laws": list(BASE_LAWS_L1), "units": list(UNITS),
                       "side_base_law": {f"{f}|{law}": v for (f, law), v in
                                         sorted(SIDE_BASE_LAW.items())},
                       "scan_bands": list(SCAN_BANDS_R4), "scan_ends": list(SCAN_ENDS),
                       "has_l1": {f"{p}|{L}": has_l1(p, L) for p in PANELS
                                  for L in LENSES_R4[p]}},
        "retest_pins": {k: C.RETEST_PINS[k] for k in ("margin_atr", "hold_bars", "ttl_bars",
                                                      "grid_sha")},
        "picks": {f"{s}|{L}": N.scale_of(s, L, "calibrated") for p in PANELS
                  for s in PANELS[p] for L in LENSES_R4[p]},
        "readings": list(READINGS), "pctile_law": PCTILE_LAW,
        "sha": {k: v["sha"] for k, v in shas.items()},
        "rows": {k: v["rows"] for k, v in shas.items()},
        "keys": {k: TABLE_KEYS[k] for k in shas},
        "files_of_record": list(FILES_OF_RECORD),
        "input_sha": input_shas(), "code_sha": code_shas(),
        "tc10_continuity": cont,
    }
    (out / "build_manifest.json").write_text(
        json.dumps(man, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")
    clock(f"merge {time.perf_counter() - t0:.1f}s")
    return man


def build(out: Path = OUT, parts: Path | None = None) -> dict:
    """The whole build SERIALLY in this interpreter (every unit, then the merge)."""
    parts = Path(parts) if parts is not None else Path(out) / "_det_parts"
    for u in UNITS:
        t0 = time.perf_counter()
        write_unit(u, parts)
        clock(f"unit {u} {time.perf_counter() - t0:.1f}s")
    return merge(parts, Path(out))


def lean_block() -> str:
    L = [f"{LEAN_TAG} STAGE R-b · R4 (tierc11_stage_r4) · substrate {E.SNAPSHOT.name} · pin "
         f"{PIN_ISO} ({PIN_MS}) · seed {SEED} · sensitivity {SEED_SENS} · K {K_DRAWS}"]
    L += [f"{LEAN_TAG} {x}" for x in READINGS]
    return "\n".join(L) + "\n"


def main() -> int:
    args = sys.argv[1:]
    opt = {a.split("=", 1)[0]: (a.split("=", 1)[1] if "=" in a else True) for a in args}
    out = Path(opt["--out-dir"]).resolve() if "--out-dir" in opt else OUT
    parts = (Path(opt["--parts"]).resolve() if "--parts" in opt else None)
    if "--units" in opt:
        sys.stdout.write("\n".join(UNITS) + "\n")
        return 0
    if "--lean" in opt:
        sys.stdout.write(lean_block())
        return 0
    if "--unit" in opt:
        if parts is None:
            raise SystemExit("HALT: --unit needs --parts=DIR")
        t0 = time.perf_counter()
        write_unit(str(opt["--unit"]), parts)
        clock(f"unit {opt['--unit']} {time.perf_counter() - t0:.1f}s")
        return 0
    if "--merge" in opt:
        merge(parts if parts is not None else out / "_det_parts", out)
        return 0
    build(out, parts)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
