#!/usr/bin/env python
"""TIER-C10 · STAGE 0c — THE NULL MODEL OF CENSUS-R: RANDOM-BOUNDARY BOXES.

RATIFIED operator 2026-09-21 (contract TIER-C10: "NULL MODEL: random-boundary
box sets at matched coverage, same tables").  Drafted APOLLO, executed
HEPHAESTUS; seed 20260921.  TIER-E: a MEASUREMENT, collared, report-only.  It
files no registration, takes no slot in m = 6, runs no card, no trigger, no
floor, no lane — it imports none of them.  No precedent in the estate (its
guards permute LABELS; none redraws a BOX), so the design is a printed lean,
item by item, below.

THE QUESTION.  CENSUS-R says what price did after a range event.  A number
like "+0.80 ATR a hundred bars after a DIE" means nothing until one knows what
price does a hundred bars after it leaves ANY box of that size by that law.
The null answers with boxes that carry the real ranges' lives and heights and
NONE of their location: the same pins, the same leash, the same eight labels,
the same outcome function, the same toll law — and a boundary drawn at random.

WHAT IT DOES, IN ORDER, PER (asset, lens, scale kind) AND PER SEEDED DRAW
  1. READS the real confirmed macro ranges off the census's own run: each
     one's LIFE (confirm .. die, in bars) and HEIGHT ((top0 - bottom0) in ATR
     of its confirm bar), and the m + 1 GAPS around them.
  2. DRAWS THE SCHEDULE UNDER ONE OF TWO LABELLED VARIANTS [N-c], BOTH FILED,
     side by side, NEITHER CHOSEN HERE (APOLLO rules):
       gaps-only   THE CONTRACT-LITERAL DESIGN — the m + 1 gaps permuted, the
                   lives left in their real order;
       gaps+order  THE BUILDER'S LEAK-REDUCED VARIANT — the gaps permuted AND
                   the (life, height) pairs dealt in a permuted order.
     Every life keeps its bars and its own height under both: the alive-bar
     count of the schedule IS the real one's, exactly — an identity by
     construction, and F-NULL-COV holds the filed draws to it.  (Gaps ALONE
     leave each box beside the place its life was earned, and a life is a
     FUTURE fact about that place — own_window_overlap_pct is filed per draw
     under both so the size of that is a printed number, not an argument.)
     The two variants share one RNG stream per (seed, draw, cell): the same
     gap permutation and the same u's — a PAIRED comparison.
  3. RE-CENTRES each box on the close of its NEW confirm bar at a uniform
     %-position [N-e], its height re-priced by that bar's ATR [N-b].  The
     box is a function of (the schedule, one uniform, c and atr AT its confirm
     bar) — nothing after it.
  4. WALKS A STATIC-BOX STATE MACHINE with the FROZEN pins, by object: breach
     = body close outside; harden = back inside within DEV_RETURN_BARS; DIE =
     BREAK_CONFIRM_N closes beyond, or one close BREAK_MARGIN x ATR beyond.
     Every event is stamped and KNOWN at its own bar's close.  Static: no
     redraw [N-d].
  5. FEEDS THE CORPSES TO THE REAL LEASH — analytics.rangefinder_census
     .flips_and_leash reads only state / confirm_i / die_i / rid / top / bottom
     of a Range, and gets exactly that — for memory-touch-2s and flip-hold;
     the census's own detector for retest-hold; the machine's one-sided v1
     touch law written again for corpses [N-f].
  6. SENDS THE EVENTS THROUGH THE CENSUS'S OWN FUNCTIONS, unchanged and
     unforked: census_events -> outcome_ledger -> grid_rows.  Same signs,
     same anchors (known_at), same horizons in bars of the lens, same
     censoring, same toll law, same collar.
  7. FILES per-draw rows keyed (asset, lens, scale_kind, cls, draw, horizon) —
     the REAL row rides in the same table as draw -1, through the same
     functions, and HALTS if it is not the filed census cell's row [N-h] —
     and a SUMMARY: the null's median / IQR across draws beside the real
     value, and the real value's percentile within the null [N-i].
  "MATCHED COVERAGE" is PRINTED, per draw: real vs achieved close-inside-span
  coverage.  The identity is the alive-bar count; the close-inside figure is
  what a random box achieves with it, and no tolerance is tuned to make the
  two look alike.

WHAT WOULD MAKE THIS WRONG: a null box that knows anything after its confirm
bar (its own window's end, a later close, the real range it stands in for —
including a life left beside the place it was earned [N-c]); a null event
anchored before it is known; an outcome or a toll computed by a second copy of
the arithmetic; a height carried in price across a 10x move; draws that share
a stream; a tolerance standing where the alive-bar identity should; reading
the percentile as a p-value.

Run: NAIAD_CACHE_DIR=~/.cache/naiad/snapshots/tc10_20260921 \\
     ~/venvs/naiad/bin/python scripts/tierc10_null.py \\
         [--assets PANEL17|CLASSIC5|UNSEEN12|SYM,SYM] [--lenses 5m,4h,1d] \\
         [--scale-kind both|frozen3.0|calibrated] [--draws K] [--seed S] \\
         [--schedule gaps+order|gaps-only] [--out DIR] [--census-root DIR] \\
         [--force] [--merge-only]
     ~/venvs/naiad/bin/python scripts/tierc10_null.py --side-by-side
         (joins the two filed variant roots into null/variants_side_by_side)
     (the smoke: --assets BTCUSDT --lenses 4h --draws 5 \\
                 --out research_outputs/tierc10/null/smoke)
Exit: 0 complete · 1 HALT.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
import zlib
from dataclasses import asdict, dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import tierc10_census as C           # noqa: E402  HALTS at import unless the
                                     # substrate is the TC10 snapshot [LAW 3]
import numpy as np                                                   # noqa: E402
import pandas as pd                                                  # noqa: E402

from analytics import rangefinder_census as RC                       # noqa: E402
from engine.data import cache_dir                                    # noqa: E402

SEED = C.SEED                       # 20260921, by object; draw d runs on SEED + d
K_DEFAULT = 20
REAL_DRAW = -1                      # the REAL machine's row, in the same table
OUT = ROOT / "research_outputs" / "tierc10" / "null"
SELF_PATH = Path(__file__).resolve()
CENSUS_PATH = ROOT / "scripts" / "tierc10_census.py"

SUMMARY_STATS = ("median_term", "net", "hit_rate", "hit_rate_net", "median_mfe",
                 "median_mae")

# THE TWO SCHEDULES [N-c] -> schedule()'s keep_order.  BOTH are filed, each in
# its own root, each row labelled; neither is "the" null until APOLLO rules.
SCHEDULE_VARIANTS = {"gaps+order": False, "gaps-only": True}
VARIANT_DEFAULT = "gaps+order"      # the code's default since the null was built
                                    # (schedule(keep_order=False)) — a DEFAULT, not
                                    # a ruling
VARIANT_DIR = {"gaps+order": "gaps_order", "gaps-only": "gaps_only"}
VARIANT_TEXT = {
    "gaps-only": "THE CONTRACT-LITERAL DESIGN: the m + 1 gaps permuted, the lives in "
                 "their REAL order (schedule(keep_order=True))",
    "gaps+order": "THE BUILDER'S LEAK-REDUCED VARIANT: the gaps permuted AND the (life, "
                  "height) pairs dealt in a permuted order (schedule(keep_order=False))",
}
SCHEDULE_DIAG_LAW = ("own_window_overlap_pct_mean = mean over this row's (cell, draw) "
                     "schedules of the share of the schedule inside each box's OWN real "
                     "window; n_identity_perm = draws whose schedule IS the real one; "
                     "n_distinct_schedules = distinct schedules among the draws (a pooled "
                     "row prints the MIN over its member cells). HIGH overlap / FEW distinct "
                     "schedules = a cell the null cannot move off itself (small m): read its "
                     "null row with that beside it.")

NULL_GRID_KEY = ["asset", "lens", "scale_kind", "cls", "era", "draw", "horizon"]
NULL_LEDGER_KEY = ["asset", "lens", "scale_kind", "draw", "cls", "rid", "side", "i"]
NULL_BOX_KEY = ["asset", "lens", "scale_kind", "draw", "box"]
NULL_COV_KEY = ["asset", "lens", "scale_kind", "draw"]
NULL_SUMMARY_KEY = ["asset", "lens", "scale_kind", "cls", "era", "horizon", "stat"]
CELL_TABLES = {
    "null_grid": NULL_GRID_KEY,
    "null_events": NULL_LEDGER_KEY,
    "null_boxes": NULL_BOX_KEY,
    "null_coverage": NULL_COV_KEY,
    "null_summary": NULL_SUMMARY_KEY,
}
ROOT_TABLES = {
    "null_grid": NULL_GRID_KEY,
    "null_coverage": NULL_COV_KEY,
    "null_summary": NULL_SUMMARY_KEY,
    "leans": ["lean"],
}
# the ledger is filed NARROW: what a pooled row and a re-derivation need, and
# no as-of stamp AT the anchor — the null has no pivot, so it has no honest
# analogue of the machine's state latch to capture there
LEDGER_COLUMNS = (["cls", "i", "known_at", "rid", "side", "sgn", "known_close_ms",
                   "era", "bad_atr", "toll_atr_evt"]
                  + [f"{x}_{hn}" for hn, _ in C.HORIZONS
                     for x in ("cens", "term", "mfe", "mae")])
POOL_COLUMNS = ["draw"] + list(C.POOL_COLUMNS)

LEANS = (
    "[LEAN-HEPHAESTUS] N-a THE SCHEDULE IS THE LIFE: a null box is alive on [confirm, "
    "confirm + the real range's life) — the schedule's alive-bar count is the real one's "
    "EXACTLY, by construction, and F-NULL-COV holds every draw to it. The static-box "
    "machine's own DIE is TERMINAL for the box's EVENTS (one corpse, two memory lines born "
    "at the DIE bar — the real machine's law) but does not move the schedule; a box whose "
    "DIE never fires inside its window is RETIRED at the window's end: no DIE row, no "
    "corpse, an open breach dropped. A random box dies SOONER than the range it stands in "
    "for, so its EVENT-alive bars (confirm .. null DIE) fall short of the schedule — "
    "printed beside it, per draw, never hidden.",
    "[LEAN-HEPHAESTUS] N-b HEIGHT IS KEPT IN ATR: (top0 - bottom0) / ATR[real confirm bar], "
    "re-priced by ATR[new confirm bar]. Every pin of the machine is an ATR multiple; a "
    "height carried in price across a 10x move would be a different box.",
    "[LEAN-HEPHAESTUS] N-c GAPS, AND ORDER — TWO SCHEDULES FILED SIDE BY SIDE, NEITHER "
    "CHOSEN: `gaps-only` = the contract-literal design (the m + 1 gaps — lead, between, trail "
    "— permuted, the lives left in their real order); `gaps+order` = the builder's "
    "leak-reduced variant (the gaps permuted AND the m (life, height) pairs dealt to the "
    "slots in a permuted order; each pair stays whole). Gaps alone leave box k within a few "
    "gaps of the place its life was earned (the first and last boxes move by ONE gap), and a "
    "life is a FUTURE fact about that place — 'price stays range-bound for L bars from here' "
    "— which the null would inherit; on a driftless random walk an as-of-clean event's MEAN "
    "term is zero, and F-NULL-SANE prints both schedules' mean terms side by side. "
    "own_window_overlap_pct is filed per draw under BOTH variants (how much of the schedule "
    "sits inside each box's OWN real window). The variant rides every row as "
    "schedule_variant; the two share one RNG stream per (seed, draw, cell) — the same gap "
    "permutation, the same u's. A permuted LEAD gap shorter than ATR_LEN is swapped with the "
    "first gap that is not (the real lead gap always qualifies) — counted per draw. A "
    "censored last life (the range alive at the tape's end) travels as the life it has.",
    "[LEAN-HEPHAESTUS] N-d STATIC: the null box never redraws — a harden is a return inside "
    "within DEV_RETURN_BARS and nothing else; its span IS the box. The real machine's "
    "REDRAW_BASIS (wick) is therefore NOT in the null: a real range's next breach needs a "
    "close beyond the hardened wick, a null box's beyond its original edge.",
    "[LEAN-HEPHAESTUS] N-e UNIFORM %-POSITION: u ~ U[0,1), bottom = close - u x height. A "
    "real range confirms NEAR a boundary (a touch within TOUCH_EPS); the null does not "
    "imitate that.",
    "[LEAN-HEPHAESTUS] N-f memory-touch-v1 is the machine's one-sided first-touch law "
    "written again for corpses (the machine computes it inline and it cannot be called "
    "apart); memory-touch-2s and flip-hold come from the REAL leash of the analytics port "
    "fed synthetic Range corpses; retest-hold from the census's own detector "
    "[PROVISIONAL-PINS, as there]. All eight labels then pass through the census's "
    "census_events -> outcome_ledger -> grid_rows, unchanged.",
    "[LEAN-HEPHAESTUS] N-g RNG = numpy default_rng([seed + draw, crc32('asset|lens|"
    "scale_kind')]): seed 20260921 + draw per the design, the cell key beside it so two "
    "cells with the same range count do not share one permutation. Drawn in this order: "
    "the gap permutation, the u's, the order of the lives. [L8] a sensitivity run re-seeds "
    "with --seed 20260816.",
    "[LEAN-HEPHAESTUS] N-h THE REAL ROW rides in the same table as draw -1, computed "
    "through the census's own functions, and the build HALTS if it is not the filed "
    "census cell's row when one is on disk (UNANCHORED is printed when none is).",
    "[LEAN-HEPHAESTUS] N-i real_pctile_in_null = the mid-rank percentile of the real value "
    "among the draws' values: 100 x (#null < real + 0.5 x #null == real) / valid draws. A "
    "DESCRIPTION of where the real number sits, never a p-value: Tier-E, no bar, no "
    "verdict; K draws resolve it to 100 / K at best.",
)

NULL_LAW = ("static box · breach = body close outside · harden = back inside within "
            "DEV_RETURN_BARS · DIE = BREAK_CONFIRM_N closes beyond or one close "
            "BREAK_MARGIN x ATR beyond · no redraw · every event known at its own bar")
PCTILE_LAW = "mid-rank: 100 x (#null < real + 0.5 x #null == real) / valid draws"

log, clock, iso = C.log, C.clock, C.iso
_NAN = float("nan")


def code_sha() -> str:
    """One sha over the three files a null cell's numbers are a function of."""
    h = hashlib.sha256()
    for p in (SELF_PATH, CENSUS_PATH, C.PORT_PATH):
        h.update(p.read_bytes())
    return h.hexdigest()


# ═══════════════════════════════════════════════ 1 · THE REAL BOX SET
def real_box_set(tape: C.Tape, macro: dict) -> dict:
    """The REAL confirmed macro ranges as (life, height-in-ATR) pairs in bar
    order, and the m + 1 gaps around them.  sum(lives) + sum(gaps) == n.

    life = die_i - confirm_i (dead BY the close of die_i, the census's law);
    the range still alive at the tape's end carries n - confirm_i, CENSORED.

    RAISES IF: confirmed lives overlap (ONE_ACTIVE broken), a range other than
    the last is still alive, or a confirm bar has no positive ATR.
    """
    n, atr = tape.n, tape.atr
    conf = [r for r in macro["ranges"] if r.confirm_i >= 0]
    rows, gaps, prev_end = [], [], 0
    for q, r in enumerate(conf):
        a = int(r.confirm_i)
        dead = r.state == "DEAD" and r.die_i >= 0
        if a < prev_end:
            raise ValueError("null: confirmed lives overlap (ONE_ACTIVE broken)")
        if not dead and q != len(conf) - 1:
            raise ValueError(f"null: rid {r.rid} is alive but is not the last range")
        if not atr[a] > 0:
            raise ValueError(f"null: rid {r.rid} confirms on a bar with no ATR")
        end = int(r.die_i) if dead else n
        gaps.append(a - prev_end)
        rows.append({"src_rid": int(r.rid), "real_confirm_i": a, "life": end - a,
                     "height_atr": float((r.top0 - r.bottom0) / atr[a]),
                     "censored": not dead})
        prev_end = end
    gaps.append(n - prev_end)
    if sum(x["life"] for x in rows) + sum(gaps) != n:
        raise ValueError("null: lives + gaps do not tile the tape")
    return {"boxes": rows, "gaps": gaps, "n": n,
            "alive_bars": int(sum(x["life"] for x in rows))}


# ═══════════════════════════════════════════════ 2 · ONE DRAW'S SCHEDULE
@dataclass(frozen=True)
class Box:
    box: int            # 1-based, schedule order == the synthetic Range's rid
    src_rid: int        # the REAL range whose life and height it carries
    confirm_i: int      # its NEW confirm bar
    life: int           # scheduled alive bars: [confirm_i, confirm_i + life)
    height_atr: float   # the REAL (top0 - bottom0) / atr[real confirm bar]
    u: float            # %-position of the confirm close inside the box, [0, 1)
    censored: bool      # the real life ran into the tape's end


def draw_rng(seed: int, draw: int, asset: str, lens: str, scale_kind: str):
    """[N-g] one independent stream per (seed + draw, cell).  crc32, not
    hash(): the cell key must not move with PYTHONHASHSEED."""
    cell = zlib.crc32(f"{asset}|{lens}|{scale_kind}".encode("utf-8"))
    return np.random.default_rng([int(seed) + int(draw), int(cell)])


def schedule(real: dict, rng, keep_order: bool = False) -> tuple[list[Box], dict]:
    """[N-c] permute the GAPS and the ORDER of the lives; each (life, height)
    pair stays whole.  Returns (boxes, info); info carries both permutations
    and whether the lead-gap swap fired.  keep_order=True is the variant
    `gaps-only` (the contract-literal design); keep_order=False is `gaps+order`
    (the builder's leak-reduced variant) [SCHEDULE_VARIANTS].  The order of the
    lives is drawn LAST, so both variants read the same gap permutation and the
    same u's off one stream.

    RAISES IF: the schedule does not tile the tape (it cannot, short of a bug:
    the gaps and the lives are permutations of the real ones).
    """
    rows, gaps, n = real["boxes"], real["gaps"], real["n"]
    m = len(rows)
    perm = [int(k) for k in rng.permutation(m + 1)]
    u = rng.random(m)
    order = list(range(m)) if keep_order else [int(k) for k in rng.permutation(m)]
    g = [gaps[k] for k in perm]
    swapped = False
    if m and g[0] < RC.ATR_LEN:
        # the ZigZag's warm floor: no real range confirms inside it, so no
        # null box is born inside it either
        j = next(k for k in range(1, m + 1) if g[k] >= RC.ATR_LEN)
        g[0], g[j] = g[j], g[0]
        perm[0], perm[j] = perm[j], perm[0]
        swapped = True
    boxes, pos, own = [], (g[0] if g else 0), 0
    for k in range(m):
        x = rows[order[k]]
        boxes.append(Box(box=k + 1, src_rid=x["src_rid"], confirm_i=int(pos),
                         life=int(x["life"]), height_atr=float(x["height_atr"]),
                         u=float(u[k]), censored=bool(x["censored"])))
        own += max(0, min(pos + x["life"], x["real_confirm_i"] + x["life"])
                   - max(pos, x["real_confirm_i"]))
        pos += x["life"] + g[k + 1]
    if pos != n:
        raise ValueError(f"null: the schedule ends at {pos}, the tape at {n}")
    return boxes, {"perm": perm, "order": order, "gaps": g, "lead_gap_swapped": swapped,
                   "identity_perm": perm == list(range(m + 1)) and order == list(range(m)),
                   "own_window_overlap_bars": int(own)}


def box_bounds(b: Box, c_a: float, atr_a: float) -> tuple[float, float]:
    """(bottom, top) of a box from what is known AT its confirm bar [N-b, N-e]."""
    height = b.height_atr * atr_a
    bot = c_a - b.u * height
    return bot, bot + height


# ═══════════════════════════════════════════════ 3 · THE STATIC-BOX MACHINE
def _first_true(test, start: int, n: int) -> int:
    """First bar in [start, n) where test(lo, hi) -> mask is True; -1 if none.
    Doubling chunks: a first touch is usually close, and a 5m tape is long."""
    i, chunk = start, 256
    while i < n:
        j = min(n, i + chunk)
        hit = np.nonzero(test(i, j))[0]
        if len(hit):
            return i + int(hit[0])
        i, chunk = j, chunk * 2
    return -1


def static_box_machine(tape: C.Tape, boxes: list, pins: dict | None = None) -> dict:
    """The breach lifecycle of the machine of record on boxes that do not move.
    Bar order inside a box is the machine's (analytics port, "breach lifecycle,
    per alive range"): an open breach is first updated by this bar's close
    (another close beyond, or the return: harden within DEV_RETURN_BARS, lapse
    past it), a closed box may open one, and the death test runs last — so a
    margin death CAN share a bar with its breach-open, as in the machine.

    AS-OF: a box is (schedule, u, c[confirm], atr[confirm]); each event reads
    c[i], atr[i] and the box — it is stamped AND known at bar i.  On a prefix
    tape[:t] the same boxes give the same events up to t - 1 [F-NULL-ASOF]:
    a box not yet born is skipped, a window the tape cuts is walked to the cut.

    Returns a dict shaped like the port's run_machine where the census reads it
    ("events", "ranges") plus the null's own masks.  No price is logged: the
    census reads bar indices from events and prices from Range fields.
    """
    p = RC.PINS if pins is None else pins
    dev_ret, brk_n, brk_m = p["DEV_RETURN_BARS"], p["BREAK_CONFIRM_N"], p["BREAK_MARGIN"]
    n, ts = tape.n, tape.ts
    c, atr = tape.c.tolist(), tape.atr.tolist()
    ev: list[dict] = []
    ranges, rows = [], []
    alive_sched = np.zeros(n, dtype=bool)
    alive_evt = np.zeros(n, dtype=bool)
    top_a, bot_a = np.full(n, _NAN), np.full(n, _NAN)
    prev_end = 0

    def put(i, kind, rid, **kw):
        ev.append({"i": int(i), "ts": ts[i], "event": kind, "rid": int(rid), **kw})

    for b in boxes:
        a = b.confirm_i
        if a >= n:
            break                       # a prefix: not born yet
        if a < prev_end:
            raise ValueError("null: scheduled windows overlap (ONE_ACTIVE broken)")
        end = min(a + b.life, n)
        prev_end = a + b.life
        bot, top = box_bounds(b, c[a], atr[a])
        put(a, "confirm", b.box)
        pending = None
        die_i, die_side, die_by = -1, "", ""
        n_breach = n_harden = n_lapse = 0
        for i in range(a, end):
            c_i = c[i]
            if pending is None:
                if c_i > top:
                    pending = {"side": "top", "open_i": i, "closes": 1}
                elif c_i < bot:
                    pending = {"side": "bottom", "open_i": i, "closes": 1}
                if pending is not None:
                    n_breach += 1
                    put(i, "breach-open", b.box, side=pending["side"])
            else:
                beyond = c_i > top if pending["side"] == "top" else c_i < bot
                if beyond:
                    pending["closes"] += 1
                else:
                    bars_out = i - pending["open_i"]
                    if bars_out <= dev_ret:
                        n_harden += 1
                        put(i, "harden", b.box, side=pending["side"], bars_outside=bars_out)
                    else:
                        n_lapse += 1
                        put(i, "breach-lapse", b.box, side=pending["side"],
                            bars_outside=bars_out)
                    pending = None
            if pending is not None:
                bnd = top if pending["side"] == "top" else bot
                by_n = pending["closes"] >= brk_n
                by_m = (abs(c_i - bnd) >= brk_m * atr[i]
                        and (c_i > bnd if pending["side"] == "top" else c_i < bnd))
                if by_n or by_m:
                    die_i, die_side = i, pending["side"]
                    die_by = "n_closes" if by_n else "margin"
                    put(i, "breakout-die", b.box, side=die_side, by=die_by,
                        closes=pending["closes"])
                    break
        stop = die_i if die_i >= 0 else end
        alive_sched[a:end] = True
        alive_evt[a:stop] = True
        top_a[a:stop], bot_a[a:stop] = top, bot
        fate = ("DEAD" if die_i >= 0 else
                "RETIRED" if a + b.life <= n else "CONFIRMED")   # CONFIRMED = the
                                        # tape cut the window: still alive at its end
        ranges.append(RC.Range(rid=b.box, top=top, bottom=bot, top0=top, bottom0=bot,
                               seed_i=a, confirm_i=a, die_i=die_i, state=fate))
        rows.append({"box": b.box, "die_i": die_i, "die_side": die_side, "die_by": die_by,
                     "fate": fate, "n_breach": n_breach, "n_harden": n_harden,
                     "n_lapse": n_lapse, "event_alive_bars": stop - a,
                     "window_cut_by_tape": bool(a + b.life > n)})

    # [N-f] the machine's v1 memory-touch, for corpses: ONE-SIDED, first touch
    # per side, never on the die bar
    h_a, l_a = tape.h, tape.l
    for r in ranges:
        if r.state != "DEAD":
            continue
        i = _first_true(lambda lo, hi, px=r.top: h_a[lo:hi] >= px, r.die_i + 1, n)
        if i >= 0:
            r.mem_top_frozen_i = i
            put(i, "memory-touch", r.rid, side="top")
        i = _first_true(lambda lo, hi, px=r.bottom: l_a[lo:hi] <= px, r.die_i + 1, n)
        if i >= 0:
            r.mem_bot_frozen_i = i
            put(i, "memory-touch", r.rid, side="bottom")
    ev.sort(key=lambda e: e["i"])                  # stable, as the machine's
    with np.errstate(invalid="ignore"):
        inside = (bot_a <= tape.c) & (tape.c <= top_a)
    sched_top, sched_bot = np.full(n, _NAN), np.full(n, _NAN)
    for b, r in zip(boxes, ranges):
        sched_top[b.confirm_i:b.confirm_i + b.life] = r.top
        sched_bot[b.confirm_i:b.confirm_i + b.life] = r.bottom
    with np.errstate(invalid="ignore"):
        inside_sched = (sched_bot <= tape.c) & (tape.c <= sched_top)
    return {"events": ev, "ranges": ranges, "n_bars": n, "n_confirmed": len(ranges),
            "boxes": rows, "alive_sched": alive_sched, "alive_evt": alive_evt,
            "top": top_a, "bot": bot_a,
            "covered_sched": alive_sched & inside_sched, "covered_evt": alive_evt & inside}


def null_view(tape: C.Tape, nm: dict, leash: list) -> dict:
    """What census_events and outcome_ledger ask of a view, for the null: the
    leash frame (known_at per leash event — the census's own law) and the
    per-bar arrays the ledger captures at an anchor.  in_range is EVENT-alive;
    top / bot are the static box while it is; state is the null's own latch —
    0 while a box is event-alive and before any null DIE, the DIE's direction
    from a DIE to the next confirm.  (The real latch also reads the first
    sealed PIVOT; the null has none, which is why these captures are not filed
    [LEDGER_COLUMNS].)"""
    n, c = tape.n, tape.c
    hold = int(RC.PINS_V2["FLIP_HOLD_BARS"])
    cps = [(e["i"], 0 if e["event"] == "confirm" else (1 if e["side"] == "top" else -1))
           for e in nm["events"] if e["event"] in ("confirm", "breakout-die")]
    state = C._step_fill(n, cps, 0, np.int8)
    with np.errstate(invalid="ignore", divide="ignore"):
        pct = 100.0 * (c - nm["bot"]) / (nm["top"] - nm["bot"])
        dist = np.minimum(np.abs(nm["top"] - c), np.abs(c - nm["bot"])) / tape.atr
    lf = C.leash_frame(leash, hold)
    fl = lf[lf["event"] == "flip"].sort_values(["known_at", "pos"], kind="mergesort")
    pol = [1 if s == "top" else -1 for s in fl["side"]]
    flip_pol = C._step_fill(n, list(zip(fl["known_at"].tolist(), pol)), 0, np.int8)
    return {"n": n, "in_range": nm["alive_evt"], "state": state, "top": nm["top"],
            "bot": nm["bot"], "pct": pct, "dist_atr": dist, "flip_pol": flip_pol,
            "_leash_frame": lf}


# ═══════════════════════════════════════════════ 4 · EVENTS -> THE CENSUS'S TABLES
def memo_bands(tape: C.Tape) -> tuple:
    """The census's RETEST_BANDS evaluated ONCE on this tape — the same
    callables, the same arithmetic; K draws need not recompute three EMAs."""
    out = []
    for name, band in C.RETEST_BANDS:
        lo, hi = band(tape.c)

        def held(_c, _lo=lo, _hi=hi):
            return _lo, _hi
        held.label = band.label
        out.append((name, held))
    return tuple(out)


def events_of(tape: C.Tape, macro: dict, leash: list, view: dict, bps: float,
              bands: tuple) -> pd.DataFrame:
    """THE ONE ROAD both sides take: the census's census_events, then the
    census's outcome_ledger.  `macro` is the port's dict (real) or the
    static-box machine's (null); nothing here knows which."""
    evf, _ = C.census_events(tape, macro, leash, view, bands=bands)
    return C.outcome_ledger(tape, evf, view, bps)


def real_side(tape: C.Tape, scale_mult: float, bps: float, bands: tuple) -> tuple:
    """(macro, ledger) of the REAL machine at one SCALE — the census's calls."""
    v2 = C.run_scale(tape, scale_mult)
    view = C.asof_view(tape, v2["macro"], v2["leash"])
    return v2["macro"], events_of(tape, v2["macro"], v2["leash"], view, bps, bands)


def null_draw(tape: C.Tape, real: dict, draw: int, seed: int, scale_kind: str,
              scale_mult: float, bps: float, bands: tuple, keep_order: bool = False) -> dict:
    """One seeded draw, whole: schedule -> boxes -> static-box machine -> the
    REAL leash on the corpses -> the census's events and ledger.  keep_order
    = SCHEDULE_VARIANTS[the build's variant] [schedule, N-c]."""
    rng = draw_rng(seed, draw, tape.sym, tape.lens, scale_kind)
    boxes, info = schedule(real, rng, keep_order=keep_order)
    nm = static_box_machine(tape, boxes)
    leash = RC.flips_and_leash(nm, tape.d, tape.atr,
                               dict(RC.PINS_V2, SCALE_MULT=float(scale_mult)),
                               retests=False)
    view = null_view(tape, nm, leash)
    return {"boxes": boxes, "info": info, "machine": nm, "leash": leash, "view": view,
            "ledger": events_of(tape, nm, leash, view, bps, bands)}


def _filed_ledger(led: pd.DataFrame, sym: str, lens: str, kind: str, draw: int) -> pd.DataFrame:
    d = led[LEDGER_COLUMNS].assign(asset=sym, lens=lens, scale_kind=kind, draw=int(draw))
    return C.canon(d, NULL_LEDGER_KEY)


def coverage_row(tape: C.Tape, macro: dict, real: dict, d: dict, draw: int) -> dict:
    """"MATCHED COVERAGE", printed: the alive-bar IDENTITY, and beside it what
    the close did inside the span — real vs achieved, no tolerance."""
    n, nm = tape.n, d["machine"]
    fates = [x["fate"] for x in nm["boxes"]]
    return {
        "draw": int(draw), "n_bars": n, "n_boxes": len(d["boxes"]),
        "real_alive_bars": real["alive_bars"],
        "null_alive_bars_scheduled": int(nm["alive_sched"].sum()),
        "alive_bars_identity": bool(int(nm["alive_sched"].sum()) == real["alive_bars"]),
        "null_alive_bars_event": int(nm["alive_evt"].sum()),
        "real_coverage_pct": 100.0 * float(np.asarray(macro["covered"]).sum()) / n,
        "null_coverage_pct_scheduled": 100.0 * float(nm["covered_sched"].sum()) / n,
        "null_coverage_pct_event": 100.0 * float(nm["covered_evt"].sum()) / n,
        "real_n_die": int(sum(1 for r in macro["ranges"]
                              if r.state == "DEAD" and r.confirm_i >= 0)),
        "null_n_die": fates.count("DEAD"), "null_n_retired": fates.count("RETIRED"),
        "null_n_alive_at_end": fates.count("CONFIRMED"),
        "lead_gap_swapped": bool(d["info"]["lead_gap_swapped"]),
        "identity_perm": bool(d["info"]["identity_perm"]),
        # how much of the schedule sits inside the box's OWN real window — the
        # place its life was earned [N-c]; chance alone under the permuted order
        "own_window_overlap_pct": (100.0 * d["info"]["own_window_overlap_bars"]
                                   / real["alive_bars"] if real["alive_bars"] else 0.0),
        "coverage_law": "close inside the alive span, % of ALL bars — real: the machine's "
                        "mask (boundaries + deviation zones); null: the static box, over "
                        "its SCHEDULED window and over its EVENT-alive bars",
    }


def box_rows(d: dict, draw: int) -> list[dict]:
    """The filed box set.  ATR-unit and bar-index fields only — no raw price
    is ever filed (the census's law); a bound is re-derivable from these and
    the tape: box_bounds(u, height_atr, c[confirm_i], atr[confirm_i])."""
    return [dict(asdict(b), draw=int(draw), sched_end=b.confirm_i + b.life, **{
        k: m[k] for k in ("die_i", "die_side", "die_by", "fate", "n_breach", "n_harden",
                          "n_lapse", "event_alive_bars", "window_cut_by_tape")})
            for b, m in zip(d["boxes"], d["machine"]["boxes"])]


# ═══════════════════════════════════════════════ 5 · THE SUMMARY
def summarise(grid: pd.DataFrame) -> pd.DataFrame:
    """Per (asset | pool, lens, scale_kind, cls, horizon, stat): the real value
    beside the null's median / IQR across draws, and the real value's mid-rank
    percentile within the null [N-i].  `grid` is the FILED (rounded) null
    grid, so a row here is an exact function of bytes a reader can open.
    WHOLE: a cell with no valid draw, or no real value, files NaN and says why.
    """
    rows = []
    gk = ["asset", "lens", "scale_kind", "cls", "era", "horizon"]
    for key, G in grid.groupby(gk, sort=True):
        real, null = G[G["draw"] == REAL_DRAW], G[G["draw"] >= 0]
        if len(real) != 1:
            raise SystemExit(f"HALT: {key}: {len(real)} real row(s) in the null grid")
        for stat in SUMMARY_STATS:
            rv = float(real[stat].iloc[0])
            nv = null[stat].to_numpy(float)
            ok = nv[np.isfinite(nv)]
            r = dict(zip(gk, key), stat=stat, real=rv, real_n=int(real["n"].iloc[0]),
                     n_draws=int(len(nv)), n_draws_valid=int(len(ok)),
                     null_n_events_median=float(null["n"].median()) if len(null) else _NAN)
            if len(ok):
                q25, q75 = np.quantile(ok, 0.25), np.quantile(ok, 0.75)
                r.update(null_median=float(np.median(ok)), null_q25=float(q25),
                         null_q75=float(q75), null_iqr=float(q75 - q25),
                         null_min=float(ok.min()), null_max=float(ok.max()),
                         real_minus_null_median=(rv - float(np.median(ok))
                                                 if np.isfinite(rv) else _NAN))
            else:
                r.update(null_median=_NAN, null_q25=_NAN, null_q75=_NAN, null_iqr=_NAN,
                         null_min=_NAN, null_max=_NAN, real_minus_null_median=_NAN)
            if len(ok) and np.isfinite(rv):
                r["real_pctile_in_null"] = 100.0 * (float((ok < rv).sum())
                                                    + 0.5 * float((ok == rv).sum())) / len(ok)
                r["nan_reason"] = ""
            else:
                r["real_pctile_in_null"] = _NAN
                r["nan_reason"] = ("no null draw produced a scored event of this class"
                                   if not len(ok) else
                                   "the real row has no scored event of this class")
            r["pctile_law"] = PCTILE_LAW
            r["pins_status"] = C.PINS_STATUS[key[3]]
            r["printable"] = bool(C.printable(key[1], key[3], key[4]))
            rows.append(r)
    return pd.DataFrame(rows)


# ═══════════════════════════════════════════════ 6 · ONE CELL
def scale_for(tape: C.Tape, kind: str, census_root: Path) -> tuple[float, str]:
    """frozen3.0 -> the pin, by object.  calibrated -> the filed census cell's
    pick when its receipt is on disk (the null stands BESIDE that table), the
    calibrator otherwise — the source rides the row."""
    if kind == "frozen3.0":
        return float(C.FROZEN_SCALE), "analytics port PINS_V2['SCALE_MULT'] (frozen)"
    p = C.cell_dir(census_root, tape.sym, tape.lens) / "cell.json"
    if p.exists():
        return (float(json.loads(p.read_text())["calibrated_scale"]),
                "the filed census cell's calibrated_scale")
    return float(C.calibrate(tape)[0]), "C.calibrate (no filed census cell)"


ANCHOR_COLUMNS = ("n_events", "n", "n_censored", "n_bad_atr", "toll_atr_all") + C.STAT_COLS


def anchor_to_census(grid: pd.DataFrame, sym: str, lens: str, kinds: tuple,
                     census_root: Path) -> str:
    """[N-h] the null's REAL rows against the FILED census cell's grid.
    HALTS IF one number differs: the null would then stand beside a table it
    was not measured against."""
    p = C.cell_dir(census_root, sym, lens) / "grid.parquet"
    if not p.exists():
        return f"UNANCHORED: no filed census cell at {p.parent.name} under {census_root.name}/"
    filed = pd.read_parquet(p)
    filed = filed[filed["scale_kind"].isin(kinds)].set_index(C.GRID_KEY).sort_index()
    mine = (grid[grid["draw"] == REAL_DRAW].set_index(C.GRID_KEY).sort_index())
    if not filed.index.equals(mine.index):
        raise SystemExit(f"HALT: {sym} {lens}: the null's real rows and the filed census "
                         "cell do not hold the same keys")
    for col in ANCHOR_COLUMNS:
        a, b = mine[col].to_numpy(float), filed[col].to_numpy(float)
        if not np.array_equal(a, b, equal_nan=True):
            k = int(np.nonzero(~((a == b) | (np.isnan(a) & np.isnan(b))))[0][0])
            raise SystemExit(f"HALT: {sym} {lens}: the null's real row {mine.index[k]} has "
                             f"{col} = {a[k]!r}, the filed census cell {b[k]!r} [N-h]")
    return (f"ANCHORED: {len(mine)} real rows x {len(ANCHOR_COLUMNS)} columns equal the "
            f"filed census cell ({census_root.name}/cells/{p.parent.name}/grid.parquet)")


def compute_cell(tape: C.Tape, kinds: tuple, n_draws: int, seed: int,
                 census_root: Path, timing: dict | None = None,
                 variant: str = VARIANT_DEFAULT) -> dict:
    """Everything one (asset, lens) null cell files, as frames — no IO but the
    read of the census cell it anchors to.  `variant` names the schedule [N-c]
    and rides every row."""
    tm = {} if timing is None else timing
    keep_order = SCHEDULE_VARIANTS[variant]
    diag: dict = {}
    sym, lens = tape.sym, tape.lens
    bps, bps_src = C.toll_bps_for(sym)
    bands = memo_bands(tape)
    grid_all, led_all, box_all, cov_all, scales = [], [], [], [], {}
    real_runs: dict = {}
    for kind in kinds:
        s, s_src = scale_for(tape, kind, census_root)
        scales[kind] = {"scale_mult": s, "source": s_src}
        if s not in real_runs:
            t1 = time.perf_counter()
            real_runs[s] = real_side(tape, s, bps, bands)
            tm[f"real@{s}_s"] = time.perf_counter() - t1
        macro, led_real = real_runs[s]
        real = real_box_set(tape, macro)
        t1 = time.perf_counter()
        for draw in [REAL_DRAW] + list(range(n_draws)):
            if draw == REAL_DRAW:
                led = _filed_ledger(led_real, sym, lens, kind, draw)
            else:
                d = null_draw(tape, real, draw, seed, kind, s, bps, bands,
                              keep_order=keep_order)
                led = _filed_ledger(d["ledger"], sym, lens, kind, draw)
                diag.setdefault(kind, []).append(
                    (tuple((b.confirm_i, b.src_rid) for b in d["boxes"]),
                     100.0 * d["info"]["own_window_overlap_bars"] / real["alive_bars"]
                     if real["alive_bars"] else 0.0, bool(d["info"]["identity_perm"])))
                cov_all.append(dict(coverage_row(tape, macro, real, d, draw),
                                    asset=sym, lens=lens, scale_kind=kind, scale_mult=s))
                box_all += [dict(r, asset=sym, lens=lens, scale_kind=kind)
                            for r in box_rows(d, draw)]
            led_all.append(led)
            grid_all += [dict(r, draw=int(draw),
                              source="REAL" if draw == REAL_DRAW else "NULL")
                         for r in C.grid_rows(led, sym, lens, kind, s, bps, bps_src)]
        tm[f"{n_draws} draws@{kind}_s"] = time.perf_counter() - t1
    grid = C.canon(pd.DataFrame(grid_all), NULL_GRID_KEY)
    anchor = anchor_to_census(grid, sym, lens, kinds, census_root)
    box_cols = ["asset", "lens", "scale_kind", "draw", "box", "src_rid", "confirm_i",
                "life", "sched_end", "height_atr", "u", "censored", "die_i", "die_side",
                "die_by", "fate", "n_breach", "n_harden", "n_lapse", "event_alive_bars",
                "window_cut_by_tape"]
    summ = summarise(grid)
    for col, fn in (("own_window_overlap_pct_mean",
                     lambda v: float(np.mean([x[1] for x in v])) if v else _NAN),
                    ("n_identity_perm", lambda v: int(sum(x[2] for x in v))),
                    ("n_distinct_schedules", lambda v: int(len({x[0] for x in v})))):
        summ[col] = summ["scale_kind"].map({k: fn(diag.get(k, [])) for k in kinds})
    summ["schedule_diag_law"] = SCHEDULE_DIAG_LAW
    frames = {
        "null_grid": grid,
        "null_events": pd.concat(led_all, ignore_index=True),
        "null_boxes": pd.DataFrame(box_all, columns=box_cols),
        "null_coverage": pd.DataFrame(cov_all),
        "null_summary": summ,
    }
    out = {}
    for name, df in frames.items():
        if not len(df):
            continue                    # a tape with no confirmed range draws no box
        out[name] = C.stamp(C.collar(df.assign(schedule_variant=variant),
                                     f"CENSUS-R NULL {name}, {sym} {lens}, {n_draws} draws, "
                                     f"schedule {variant}"), [tape.meta], lens,
                            f"ASSET:{sym}")
    return {"frames": out, "scales": scales, "toll_bps": bps, "toll_bps_source": bps_src,
            "census_anchor": anchor}


def _pins_block(n_draws: int, seed: int, variant: str = VARIANT_DEFAULT) -> dict:
    return dict(C._pins_block(), NULL_DRAWS=int(n_draws), NULL_SEED=int(seed),
                NULL_LAW=NULL_LAW, SUMMARY_STATS=list(SUMMARY_STATS),
                NULL_SCHEDULE=variant)


def census_cell_sha(census_root: Path, sym: str, lens: str) -> str | None:
    """The content sha of the filed census cell's grid — what a null cell's
    real rows were anchored to; None when no census cell is on disk."""
    p = C.cell_dir(census_root, sym, lens) / "cell.json"
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text())["tables"]["grid"]["sha"]
    except (json.JSONDecodeError, KeyError):
        return None


def cell_is_current(root: Path, sym: str, lens: str, kinds: tuple, n_draws: int,
                    seed: int, code: str, variant: str = VARIANT_DEFAULT,
                    census_root: Path | None = None) -> tuple[bool, str]:
    """RESUME LAW, the census's: a cell is reused only under THIS code sha,
    THESE pins, THIS K, seed and schedule variant, THIS as-of, the SAME input
    bytes, at least the asked scale kinds — every table it lists on disk with
    its sha — and, when `census_root` is given, only if the census cell it
    anchored to is the one on disk NOW (a cell built UNANCHORED is not reused
    once its census cell has been filed; one anchored to a re-filed cell is
    not reused either)."""
    cd = C.cell_dir(root, sym, lens)
    p = cd / "cell.json"
    if not p.exists():
        return False, "no receipt"
    try:
        rc = json.loads(p.read_text())
    except json.JSONDecodeError:
        return False, "unreadable receipt"
    if not rc.get("complete"):
        return False, "receipt not complete"
    if rc.get("code_sha") != code:
        return False, "code sha moved"
    if rc.get("pins") != _pins_block(n_draws, seed, variant):
        return False, "pins, K, seed or schedule variant moved"
    if census_root is not None and rc.get("census_cell_grid_sha") != census_cell_sha(
            census_root, sym, lens):
        return False, "the census cell it anchors to moved (or has now been filed)"
    if not set(kinds) <= set(rc.get("scale_kinds", [])):
        return False, "scale kinds not covered"
    if rc.get("as_of_close_ms") != C.as_of_close_ms(sym)[0]:
        return False, "as-of moved"
    src = cache_dir() / rc["tape"]["source_file"]
    if not src.exists() or C.file_sha256(src) != rc["tape"]["source_sha256"]:
        return False, "input bytes moved"
    for name, t in rc["tables"].items():
        q = cd / f"{name}.parquet"
        if not q.exists() or C.content_sha(pd.read_parquet(q)) != t["sha"]:
            return False, f"table {name} missing or moved"
    return True, "current"


def run_cell(root: Path, sym: str, lens: str, kinds: tuple, n_draws: int, seed: int,
             census_root: Path, force: bool = False,
             variant: str = VARIANT_DEFAULT) -> dict:
    """Compute-or-reuse one null cell; returns its receipt."""
    code = code_sha()
    cd = C.cell_dir(root, sym, lens)
    if not force:
        ok, why = cell_is_current(root, sym, lens, kinds, n_draws, seed, code, variant,
                                  census_root)
        if ok:
            log(f"  {sym:>16} {lens:>3}  REUSED (receipt current)")
            return json.loads((cd / "cell.json").read_text())
        if (cd / "cell.json").exists():
            log(f"  {sym:>16} {lens:>3}  recomputing: {why}")
    t0 = time.perf_counter()
    tape = C.load_tape(sym, lens)
    res = compute_cell(tape, kinds, n_draws, seed, census_root, variant=variant)
    (cd / "cell.json").unlink(missing_ok=True)      # no receipt while tables move
    tables = {}
    for name, df in res["frames"].items():
        tables[name] = {"sha": C.write_table(df, name, CELL_TABLES[name], cd),
                        "rows": int(len(df)), "key": CELL_TABLES[name]}
    rc = {"asset": sym, "lens": lens, "complete": True, "seed": int(seed),
          "n_draws": int(n_draws), "code_sha": code,
          "pins": _pins_block(n_draws, seed, variant), "schedule_variant": variant,
          "scale_kinds": list(kinds), "scales": res["scales"],
          "toll_bps": res["toll_bps"], "toll_bps_source": res["toll_bps_source"],
          "census_anchor": res["census_anchor"],
          "census_cell_grid_sha": census_cell_sha(census_root, sym, lens),
          "as_of_close_ms": tape.meta["as_of_close_ms"],
          "as_of_last_closed_4h": tape.meta["as_of_last_closed_4h"],
          "tape": tape.meta, "tables": tables}
    C._dump(rc, cd / "cell.json")
    log(f"  {sym:>16} {lens:>3}  n={tape.n:>7,}  {n_draws} draws x {list(kinds)} [{variant}]  "
        f"ledger rows {tables.get('null_events', {}).get('rows', 0):,}  "
        f"{res['census_anchor'].split(':')[0]}")
    clock(f"{sym} {lens}: {time.perf_counter() - t0:.2f}s")
    return rc


# ═══════════════════════════════════════════════ 7 · THE MERGE
def merge(root: Path, assets: list, lenses: list, kinds: tuple, n_draws: int, seed: int,
          label: str, census_root: Path, variant: str = VARIANT_DEFAULT) -> dict:
    """Per-cell artifacts -> the root tables.  HALTS IF a commissioned cell has
    no current receipt.  POOLED:ALL rows are computed PER DRAW from the filed
    per-cell ledgers — draw d of every asset pooled with draw d of every other,
    the real rows (draw -1) with the real rows — and quote the BINDING toll,
    the census's law; the pooled summary is then the pooled real against the
    pooled draws."""
    code = code_sha()
    receipts, parts = {}, {k: [] for k in CELL_TABLES}
    for sym in assets:
        for lens in lenses:
            ok, why = cell_is_current(root, sym, lens, kinds, n_draws, seed, code, variant)
            if not ok:
                raise SystemExit(f"HALT: null cell {sym} {lens} is not current ({why}) — "
                                 "the grid is filed whole or not at all")
            cd = C.cell_dir(root, sym, lens)
            receipts[f"{sym}__{lens}"] = json.loads((cd / "cell.json").read_text())
            for name in ("null_grid", "null_events", "null_coverage", "null_summary"):
                q = cd / f"{name}.parquet"
                if not q.exists():
                    continue
                d = pd.read_parquet(q, columns=POOL_COLUMNS if name == "null_events" else None)
                parts[name].append(d[d["scale_kind"].isin(kinds)])
    grid = pd.concat(parts["null_grid"], ignore_index=True)
    pooled = []
    for lens in lenses:
        metas = [receipts[f"{s}__{lens}"]["tape"] for s in assets]
        for kind in kinds:
            led_k = pd.concat([d[(d["lens"] == lens) & (d["scale_kind"] == kind)]
                               for d in parts["null_events"]], ignore_index=True)
            tolls_k = grid[(grid["lens"] == lens) & (grid["scale_kind"] == kind)]
            scales = sorted(set(tolls_k["scale_mult"]))
            rows = []
            for draw in [REAL_DRAW] + list(range(n_draws)):
                rows += [dict(r, draw=int(draw),
                              source="REAL" if draw == REAL_DRAW else "NULL")
                         for r in C.grid_rows(led_k[led_k["draw"] == draw], "POOLED:ALL",
                                              lens, kind,
                                              scales[0] if len(scales) == 1 else _NAN, None,
                                              "per asset — see the asset rows",
                                              tolls=tolls_k[tolls_k["draw"] == draw])]
            pooled.append(C.stamp(pd.DataFrame(rows), metas, lens, label))
    surface = (f"{label}: {len(assets)} asset(s) x {lenses} x {list(kinds)} x "
               f"{n_draws} draws")
    full_grid = pd.concat([grid] + pooled, ignore_index=True)
    pooled_grid = C.canon(pd.concat(pooled, ignore_index=True), NULL_GRID_KEY)
    pooled_summary = []
    for lens in lenses:
        metas = [receipts[f"{s}__{lens}"]["tape"] for s in assets]
        pooled_summary.append(C.stamp(summarise(pooled_grid[pooled_grid["lens"] == lens]),
                                      metas, lens, label))
    frames = {"null_grid": full_grid,
              "null_coverage": pd.concat(parts["null_coverage"], ignore_index=True),
              "null_summary": pd.concat(parts["null_summary"] + pooled_summary,
                                        ignore_index=True)}
    for name in list(frames):           # the collar speaks for the MERGED table
        # the SCHEDULE rides every merged row, POOLED rows included: the pooled
        # rows are struck here, outside compute_cell, and would carry no variant
        frames[name] = C.collar(frames[name].drop(columns=list(C.COLLAR_COLUMNS),
                                                  errors="ignore")
                                .assign(schedule_variant=variant),
                                f"CENSUS-R NULL {name}, {surface}")
    any_meta = [next(iter(receipts.values()))["tape"]]
    frames["leans"] = C.stamp(C.collar(pd.DataFrame(
        [{"lean": f"{i:02d}", "text": x} for i, x in enumerate(LEANS)]),
        "the null model's leans, verbatim"), any_meta, "4h", label)
    sha, keys = {}, {}
    for name, df in frames.items():
        sha[name] = C.write_table(df, name, ROOT_TABLES[name], root)
        keys[name] = ROOT_TABLES[name]
        log(f"    wrote {name:16} rows={len(df):>7,}  sha={sha[name][:16]}")
    full = None
    if C.stage_d_manifest() is not None:
        full = (list(assets) == C.panels()["PANEL17"] and tuple(lenses) == C.LENSES
                and tuple(kinds) == C.SCALE_KINDS and n_draws >= K_DEFAULT
                and seed == SEED)
    draws = [REAL_DRAW] + list(range(n_draws))
    man = {
        "seed": int(seed), "n_draws": int(n_draws),
        "stage": "TIER-C10 · STAGE 0c · CENSUS-R NULL MODEL", "tier": C.TIER,
        "as_of": any_meta[0]["as_of_last_closed_4h"],
        "as_of_source": any_meta[0]["as_of_source"], "substrate": C.SNAPSHOT.name,
        "commission": {"label": label, "assets": list(assets), "lenses": list(lenses),
                       "scale_kinds": list(kinds), "classes": list(C.CLASSES),
                       "horizons": [list(x) for x in C.HORIZONS], "draws": draws,
                       "real_draw": REAL_DRAW, "pooled": ["POOLED:ALL"],
                       "summary_stats": list(SUMMARY_STATS),
                       "eras": list(C.ERAS), "era_law": C.ERA_LAW,
                       "schedule_variant": variant, "schedule_variants_filed":
                       list(SCHEDULE_VARIANTS), "schedule_variant_text": VARIANT_TEXT,
                       "collar_5m_retest": C.COLLAR_5M_RETEST,
                       "retest_pins": {k: v for k, v in C.RETEST_PINS.items()},
                       "is_the_contract_null": bool(full),
                       "n_declared_grid_rows": (len(assets) + 1) * len(lenses) * len(kinds)
                       * len(C.CLASSES) * len(C.ERAS) * len(draws) * len(C.HORIZONS)},
        "pins": _pins_block(n_draws, seed, variant), "leans": list(LEANS),
        "null_law": NULL_LAW,
        "pctile_law": PCTILE_LAW, "sign_law": C.SIGN_LAW, "anchor_law": C.ANCHOR_LAW,
        "pins_status": C.PINS_STATUS, "code_sha": code,
        "census_code_sha": C.code_sha(), "port_sha256": C.file_sha256(C.PORT_PATH),
        "census_root": (census_root.relative_to(ROOT).as_posix()
                        if census_root.is_relative_to(ROOT) else str(census_root)),
        "input_sha": {r["tape"]["source_file"]: r["tape"]["source_sha256"]
                      for r in receipts.values()},
        "cells": {k: {"tables": r["tables"], "scales": r["scales"],
                      "n_bars": r["tape"]["n_bars"], "toll_bps": r["toll_bps"],
                      "toll_bps_source": r["toll_bps_source"],
                      "census_anchor": r["census_anchor"]}
                  for k, r in receipts.items()},
        "sha": sha, "keys": keys, "skipped_empty": [],
        "warranty": C.WARRANTY,
    }
    C._dump(man, root / "build_manifest.json")
    return man


# ═══════════════════════════════════════════════ printing
def print_report(root: Path) -> None:
    cov = pd.read_parquet(root / "null_coverage.parquet")
    log("\n  MATCHED COVERAGE — PRINTED, PER DRAW (the identity is the alive-bar count; the "
        "close-inside figures are what a random box achieves with it)")
    log(f"  {'asset':>16} {'lens':>4} {'kind':>10} {'draw':>4} {'boxes':>5} {'alive real':>10} "
        f"{'alive null':>10} {'=':>2} {'evt-alive':>9} {'cov% real':>9} {'null sched':>10} "
        f"{'null evt':>8} {'DIE r/n':>9} {'retired':>7} {'own-win%':>8}")
    for r in cov.itertuples():
        log(f"  {r.asset:>16} {r.lens:>4} {r.scale_kind:>10} {r.draw:>4} {r.n_boxes:>5} "
            f"{r.real_alive_bars:>10,} {r.null_alive_bars_scheduled:>10,} "
            f"{'==' if r.alive_bars_identity else '!=':>2} {r.null_alive_bars_event:>9,} "
            f"{r.real_coverage_pct:>9.2f} {r.null_coverage_pct_scheduled:>10.2f} "
            f"{r.null_coverage_pct_event:>8.2f} {r.real_n_die:>4}/{r.null_n_die:<4} "
            f"{r.null_n_retired:>7} {r.own_window_overlap_pct:>8.2f}")
    log("  own-win% = share of the schedule inside each box's OWN real window [N-c]; retired = "
        "boxes whose DIE never fired inside their window [N-a]")
    s = pd.read_parquet(root / "null_summary.parquet")
    s = s[s["stat"].isin(("median_term", "net"))]
    log(f"\n  {C.COLLAR_5M_RETEST}")
    log("\n  OUTCOME AFTER EVENT — REAL BESIDE THE NULL (ATR; H in BARS OF THE LENS; pctile = "
        "where the real value sits among the draws — a description, not a p-value)")
    log(f"  {'asset':>16} {'lens':>4} {'kind':>10} {'class':>26} {'era':>8} {'H':>4} "
        f"{'stat':>11} {'n real':>7} {'real':>8} {'null med':>8} {'null q25':>8} "
        f"{'null q75':>8} {'pctile':>6} {'draws':>5} {'n null':>7}  pins")

    def f(v, w=8):
        return f"{v:>{w}.3f}" if np.isfinite(v) else f"{'NaN':>{w}}"
    held = 0
    for r in s.sort_values(["asset", "lens", "scale_kind", "cls", "era", "horizon", "stat"],
                           kind="mergesort").itertuples():
        if not C.printable(r.lens, r.cls, r.era):
            held += 1
            continue
        if not str(r.asset).startswith("POOLED:") and r.era != C.ERA_ALL:
            continue                     # the per-asset era rows live in the parquet
        log(f"  {r.asset:>16} {r.lens:>4} {r.scale_kind:>10} {r.cls:>26} {r.era:>8} "
            f"{r.horizon:>4} {r.stat:>11} {r.real_n:>7,} {f(r.real)} {f(r.null_median)} "
            f"{f(r.null_q25)} {f(r.null_q75)} {f(r.real_pctile_in_null, 6)} "
            f"{r.n_draws_valid:>5} {f(r.null_n_events_median, 7)}  "
            f"{'TUNED' if r.cls in C.RETEST_CLASSES else 'frozen'}"
            f"{' · ' + r.nan_reason if r.nan_reason else ''}")
    if held:
        log(f"    [COLLARED] {held} summary row(s) filed and NOT printed (5m retest-hold "
            "outside the tuning era) [LAW 4 + R1]")


def main() -> int:
    ap = argparse.ArgumentParser(description="TIER-C10 CENSUS-R NULL MODEL (Tier-E, "
                                             "report-only)")
    ap.add_argument("--assets", default="PANEL17")
    ap.add_argument("--lenses", default=",".join(C.LENSES))
    ap.add_argument("--scale-kind", default="both")
    ap.add_argument("--draws", type=int, default=K_DEFAULT)
    ap.add_argument("--seed", type=int, default=SEED)
    ap.add_argument("--out", default=str(OUT))
    ap.add_argument("--census-root", default=None)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--merge-only", action="store_true")
    ap.add_argument("--variant", default=VARIANT_DEFAULT, choices=list(SCHEDULE_VARIANTS),
                    help="the SCHEDULE [N-c]: both are filed side by side, neither is "
                         "chosen here")
    a = ap.parse_args()
    label = a.assets if a.assets in ("PANEL17", "CLASSIC5", "UNSEEN12") else "NAMED"
    assets = (C.panels()[a.assets] if label != "NAMED"
              else [s.strip() for s in a.assets.split(",") if s.strip()])
    lenses = [x for x in C.LENSES if x in {s.strip() for s in a.lenses.split(",")}]
    kinds = C.SCALE_KINDS if a.scale_kind == "both" else tuple(
        k for k in C.SCALE_KINDS if k in {s.strip() for s in a.scale_kind.split(",")})
    if not assets or not lenses or not kinds or a.draws < 1:
        raise SystemExit("HALT: empty commission (assets / lenses / scale kinds / draws)")
    if label == "NAMED":
        label = f"NAMED({len(assets)})"
    root = Path(a.out).expanduser().resolve()
    census_root = (Path(a.census_root).expanduser().resolve() if a.census_root else
                   C.OUT if (C.OUT / "build_manifest.json").exists() else C.OUT / "smoke")
    close_ms, src = C.as_of_close_ms(assets[0])
    log(f"TIER-C10 · STAGE 0c · CENSUS-R NULL MODEL · {C.TIER}")
    log(f"  seed {a.seed} (+ draw) · K = {a.draws} draws · substrate {C.SNAPSHOT} · AS_OF "
        f"{iso(close_ms)} ({src})")
    log(f"  commission {label}: {len(assets)} asset(s) x {lenses} x {list(kinds)} -> {root}")
    log(f"  the real side is anchored to the census at {census_root}")
    log(f"  NULL LAW: {NULL_LAW}")
    log(f"  SCHEDULE [N-c] = {a.variant}: {VARIANT_TEXT[a.variant]}")
    log(f"  the OTHER variant is filed beside it: {[v for v in SCHEDULE_VARIANTS if v != a.variant]} "
        f"— neither is chosen here; APOLLO rules")
    log(f"  ERA: {C.ERA_LAW}")
    log(f"  {C.COLLAR_5M_RETEST}")
    for x in LEANS:
        log(f"  {x}")
    t0 = time.perf_counter()
    if not a.merge_only:
        for sym in assets:
            for lens in lenses:
                run_cell(root, sym, lens, kinds, a.draws, a.seed, census_root,
                         force=a.force, variant=a.variant)
    man = merge(root, assets, lenses, kinds, a.draws, a.seed, label, census_root,
                variant=a.variant)
    print_report(root)
    log(f"\n  null grid -> {root / 'null_grid.parquet'}  "
        f"({man['commission']['n_declared_grid_rows']} declared rows; "
        f"is_the_contract_null = {man['commission']['is_the_contract_null']})")
    log(f"  manifest -> {root / 'build_manifest.json'}")
    clock(f"total {time.perf_counter() - t0:.1f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
