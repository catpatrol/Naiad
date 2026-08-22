#!/usr/bin/env python
"""SS12-RANGEFINDER v1 · the PYTHON TWIN — the operator's grammar.

QUEUE RF-2 (v1) atop RF-1 v2, drafted ARGUS 2026-08-22, ratified by firing
("ok, make it better"). DISPLAY-ONLY:
this module renders and measures; it rules NOTHING and no decision path may
import it. RECONSTRUCTION, NOT CODE ACCESS: the semantics are rebuilt from
the public artifacts of a closed-source system (@sergio_tesla_, 2026-08-10
post + two screenshots). Hypotheses route to APOLLO under G-7.

ONE SEMANTICS, TWIN AND PINE — the .pine port must implement exactly the
machine below; F-RF-5 pins its input defaults to the calibrated pins.

THE PINNED READINGS (where the artifacts underdetermine the machine, the
reading is NAMED here rather than smuggled — evidence class per line):
  SEED [inferred]   the POTENTIAL is created when the first counter-pivot P1
                    confirms after an expansion-terminal pivot P0; {top,
                    bottom} = the two wick extremes. "Fails to exceed"
                    operates FORWARD: a body close beyond either boundary
                    before confirmation INVALIDATES the candidate.
  CONFIRM [observed] first traverse touching the boundary OPPOSITE the
                    seed's final pivot, within TOUCH_EPS*ATR; diamond at the
                    touched boundary's bar.
  ONE ACTIVE RANGE [inferred] when a range confirms, outstanding candidates
                    resolve as SUPERSEDED (the stock falls) and seeding
                    pauses until the range dies.
  LATE RETURN [inferred] a body close back inside AFTER DEV_RETURN_BARS
                    without breakout confirmation resolves the breach as
                    BREACH-LAPSED: the range survives, NO redraw, no zone.
  CONSECUTIVE [inferred] the breakout close-count starts AT the breach-open
                    close and resets on any inside body close.
  COVERAGE [observed format, inferred evaluation] a bar is covered when a
                    CONFIRMED range is alive at that bar and the close sits
                    inside its CURRENT (redrawn-so-far) boundaries —
                    deviation zones count as inside; evaluation is LIVE,
                    never retroactive.
  MERGE [inferred]  a reversal that passes REV_MIN but whose completed leg
                    is shorter than LEG_MIN*ATR does not confirm a pivot;
                    the running leg keeps extending (alternation preserved).
  BODY MODE [C1, operator grammar] boundaries sit at the pivot-bar BODY
                    extremes (max/min of open,close); the wick territory
                    beyond is deviation-eligible FROM INCEPTION — the seed
                    is born WITH a deviation zone at its wick extreme
                    (spring-birth). wick mode preserves v0/Sergio parity.
  HARDEN [C2]       the v1 name for deviation-confirm: a pending breach
                    (hollow box) HARDENS solid on return-inside within
                    DEV_RETURN_BARS; the status line carries the live
                    count of open pendings ("D pending").
  BACKDATE [C3]     at range CONFIRMATION the left edge extends back to
                    the terminal pivot; inception zones are classified
                    retroactively; the log records born_at AND
                    backdated_from.
  WINDOW [C6]       420 complete days (v0 ran 200) — KEY-B's L-R1 opens
                    Jul 2025; disclosed, not silent.
  SAME-BAR TIE [inferred, review-pinned] a bar that both touches the
                    confirm boundary intrabar AND body-closes beyond a
                    boundary INVALIDATES the candidate — the close outranks
                    the wick (checked first in code, mirrored in the pine).
  STATE EXPORT      final STATE rides the export; state transitions are not
                    events in v0 (they would change the 57-event log) —
                    recorded omission, review-named.

Cache-only, no network. Run: ~/venvs/naiad/bin/python scripts/rangefinder_twin.py
        (--calibrate for the grid; default runs the calibrated pins)
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
from dataclasses import dataclass, asdict
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from engine import indicators as ind                                 # noqa: E402
from engine.data import cache_dir                                    # noqa: E402

OUT = ROOT / "research_outputs" / "rangefinder"
WINDOW_BARS = 420          # covers KEY-B's Jul-2025 opening [C6, disclosed]
ATR_LEN = 14               # house pin, never swept

# THE CALIBRATED PINS [VETO] — measured by --calibrate, never guessed.
# Values below are written by the calibration run of record (STEP 2c) and
# asserted equal to the Pine defaults by F-RF-5.
PINS = {
    # v1 CALIBRATION OF RECORD 2026-08-22 (KEY-A objective, BODY mode, 420
    # bars, coarse 5,120 + fine, edge-avoiding tie-break): score 3.5507 —
    # v0's 200-bar wick-mode record was 10.7601. Q4 SATISFIED (68.2 in
    # [51,154]); Q1 near-miss (71.19 vs floor 72.6); Q3 near-miss (1.19 vs
    # 1.12); Q2 RESISTS (7.78 bars/pivot vs [19.95,37.05]) — the pivot
    # cadence remains the named suspect (the ZigZag reads far more MS
    # pivots than the reference draws). TOUCH_EPS 0.6 and BREAK_CONFIRM_N 8
    # sit at fine/coarse grid edges — disclosed, not hidden.
    "LEG_MIN": 0.5,
    "REV_MIN": 1.75,
    "TOUCH_EPS": 0.60,
    "DEV_RETURN_BARS": 7,
    "BREAK_CONFIRM_N": 8,
    # DISCLOSED [review]: at these pins the LATE-RETURN (breach-lapse) state
    # is UNREACHABLE — BREAK_CONFIRM_N <= DEV_RETURN_BARS + 1 empties the
    # lapse window [DEV+1, N-1].  The law stays implemented (v0 pins reach
    # it; F-RF-3 exercises it off-defaults) rather than silently dead.
    "BREAK_MARGIN": 1.5,
    # C1 — the operator's grammar. "body" places boundaries at pivot-bar
    # body extremes with spring-birth inception zones; "wick" preserves the
    # v0/Sergio reconstruction exactly.
    "BOUNDARY_MODE": "body",
    # DIAGNOSTIC ONLY (not swept, not shipped as default): C2 pins redraw
    # to the WICK extreme ("per v0 rules"); KEY-B's residual pattern says
    # the operator's own redraws land at the breach cluster's BODY edge.
    # The experiment is filed as evidence for the finding; the queue law
    # stays the default.
    "REDRAW_BASIS": "wick",
    # A READING, not a numeric pin: may several CONFIRMED ranges coexist?
    # The artifacts underdetermine it; calibration ARBITRATES and the
    # chosen reading is recorded in the contract [inferred].
    "MULTI_ACTIVE": 0,
}


# ═══════════════════════════════════════════════════ the tape, cache-only
def daily_bars() -> pd.DataFrame:
    """BTCUSDT 4h → 1D UTC, COMPLETE days only (six 4h bars — the AN-2
    head-bucket law applied at birth rather than repaired later); the true
    window is printed, never assumed."""
    f = pd.read_parquet(cache_dir() / "klines" / "BTCUSDT_4h.parquet")
    f["day"] = f["open_time"] // 86_400_000
    g = f.groupby("day").agg(n=("open_time", "size"), o=("open", "first"),
                             h=("high", "max"), l=("low", "min"),
                             c=("close", "last"), t0=("open_time", "first"))
    dropped = int((g["n"] != 6).sum())
    d = g[g["n"] == 6].tail(WINDOW_BARS).reset_index(drop=True)
    d["ts"] = pd.to_datetime(d["t0"], unit="ms", utc=True).dt.strftime(
        "%Y-%m-%d")
    d.attrs["dropped_incomplete_days"] = dropped
    return d


# ═══════════════════════════════════════════════════════ the machine
@dataclass
class Range:
    rid: int
    top: float
    bottom: float
    top0: float            # original (pre-redraw) boundaries
    bottom0: float
    seed_i: int
    confirm_i: int = -1
    die_i: int = -1
    state: str = "POTENTIAL"        # POTENTIAL|CONFIRMED|DEAD|INVALIDATED|SUPERSEDED
    confirm_side: str = ""          # boundary touched at confirmation
    dev_top_ext: float = float("nan")     # furthest deviation extremes
    dev_bot_ext: float = float("nan")
    n_deviations: int = 0
    mem_top_frozen_i: int = -1      # memory-line first-touch bars
    mem_bot_frozen_i: int = -1
    pending: dict | None = None     # the open breach, if any
    born_at: int = -1               # C3: the confirm bar
    backdated_from: int = -1        # C3: the terminal pivot's bar
    n_inception_zones: int = 0      # C1: spring-birth zones at the seed
    p0_bar: int = -1
    p1_bar: int = -1

    @property
    def mid(self) -> float:
        return (self.top + self.bottom) / 2.0


def run_machine(d: pd.DataFrame, pins: dict) -> dict:
    """The whole lifecycle over one tape.  Returns events (ordered), ranges,
    pivots, coverage — everything the fixtures and the JSON export read."""
    h, l, c = (d["h"].to_numpy(float), d["l"].to_numpy(float),
               d["c"].to_numpy(float))
    o = d["o"].to_numpy(float)
    body_hi = np.maximum(o, c)      # C1: the pivot-bar BODY extremes
    body_lo = np.minimum(o, c)
    body_mode = pins.get("BOUNDARY_MODE", "body") == "body"
    atr = ind.atr(h, l, c, ATR_LEN)
    n = len(d)
    ts = d["ts"].tolist()
    ev: list[dict] = []

    def log(i, kind, **kw):
        ev.append({"i": int(i), "ts": ts[i], "event": kind,
                   **{k: (round(float(v), 2) if isinstance(v, (int, float))
                          and k not in ("rid", "bars", "count") else v)
                      for k, v in kw.items()}})

    # ── ZigZag pivots (alternating by construction; merge law in header)
    pivots: list[tuple[int, float, int]] = []   # (bar, px, dir +1 high/-1 low)
    zdir = 0
    ext_i, ext_px = 0, c[0]
    warm = ATR_LEN                               # ATR seed floor
    for i in range(n):
        if i < warm:
            if h[i] >= ext_px:
                ext_i, ext_px = i, h[i]
            continue
        if zdir == 0:
            if h[i] - l[ext_i] >= pins["REV_MIN"] * atr[i] and l[ext_i] <= l[i]:
                zdir, ext_i, ext_px = 1, i, h[i]
            elif ext_px - l[i] >= pins["REV_MIN"] * atr[i]:
                zdir = -1
                pivots.append((ext_i, ext_px, 1))
                log(ext_i, "pivot", px=ext_px, side="high")
                ext_i, ext_px = i, l[i]
            elif h[i] > ext_px:
                ext_i, ext_px = i, h[i]
            continue
        if zdir == 1:
            if h[i] > ext_px:
                ext_i, ext_px = i, h[i]
            elif (ext_px - l[i] >= pins["REV_MIN"] * atr[i]
                  and (not pivots
                       or abs(ext_px - pivots[-1][1])
                       >= pins["LEG_MIN"] * atr[i])):
                pivots.append((ext_i, ext_px, 1))
                log(ext_i, "pivot", px=ext_px, side="high")
                zdir, ext_i, ext_px = -1, i, l[i]
        else:
            if l[i] < ext_px:
                ext_i, ext_px = i, l[i]
            elif (h[i] - ext_px >= pins["REV_MIN"] * atr[i]
                  and (not pivots
                       or abs(ext_px - pivots[-1][1])
                       >= pins["LEG_MIN"] * atr[i])):
                pivots.append((ext_i, ext_px, -1))
                log(ext_i, "pivot", px=ext_px, side="low")
                zdir, ext_i, ext_px = 1, i, h[i]
    pivots.sort(key=lambda p: p[0])

    # ── the lifecycle sweep
    piv_by_bar = {}
    for p in pivots:
        piv_by_bar.setdefault(p[0], []).append(p)
    confirmed_at: dict[int, int] = {}      # pivot bar -> bar it CONFIRMED at
    # a pivot at bar b is only knowable at its reversal bar; replay that:
    conf_order: list[tuple[int, tuple]] = []   # (confirm_bar, pivot)
    for k, p in enumerate(pivots):
        # the pivot confirms at the first bar whose counter-move sealed it —
        # conservatively the NEXT pivot's own extreme bar is too late; use
        # the first bar j > p.bar where the reversal condition held. For the
        # twin's event ORDER a bar-accurate confirmation suffices: the
        # reversal bar is the first j with excursion >= REV_MIN*atr[j].
        b, px, pd_ = p
        j = b + 1
        while j < n:
            exc = (px - l[j]) if pd_ == 1 else (h[j] - px)
            if exc >= pins["REV_MIN"] * atr[j]:
                break
            j += 1
        conf_order.append((min(j, n - 1), p))
    conf_order.sort(key=lambda x: (x[0], x[1][0]))

    ranges: list[Range] = []
    multi = bool(pins.get("MULTI_ACTIVE", 0))
    state = "NEUTRAL"
    covered = np.zeros(n, dtype=bool)
    rid_seq = 0
    known: list[tuple] = []          # pivots visible so far
    ci = 0

    for i in range(n):
        # pivots that became knowable this bar
        while ci < len(conf_order) and conf_order[ci][0] == i:
            known.append(conf_order[ci][1])
            ci += 1
            # SEED check on the newest pivot pair (P0 expansion-terminal,
            # P1 first counter-pivot); under ONE_ACTIVE only while no
            # confirmed range is alive, under MULTI always
            alive_any = any(r.state == "CONFIRMED" for r in ranges)
            if (multi or not alive_any) and len(known) >= 2:
                p1 = known[-1]
                p0 = known[-2]
                # p0 must be the expansion extreme among visible pivots
                # since the last death (or window start)
                # the CURRENT expansion starts at the last lifecycle
                # boundary — a confirm closes an expansion exactly as a
                # death opens one; measuring "terminal" against all pivots
                # since the last DEATH alone starves seeding forever once
                # the window's absolute extreme is on the board [found in
                # calibration; the reading is pinned here]
                floor_i = max([r.die_i for r in ranges if r.die_i >= 0]
                              + [r.confirm_i for r in ranges
                                 if r.confirm_i >= 0] + [-1])
                seg = [p for p in known if p[0] > floor_i]
                if p0[2] == 1:
                    is_term = p0[1] >= max((p[1] for p in seg if p[2] == 1),
                                           default=p0[1])
                else:
                    is_term = p0[1] <= min((p[1] for p in seg if p[2] == -1),
                                           default=p0[1])
                if is_term and p1[2] == -p0[2]:
                    hi_p = p0 if p0[2] == 1 else p1
                    lo_p = p1 if p0[2] == 1 else p0
                    if body_mode:
                        # C1: boundaries at the defining pivots' BODY
                        # extremes; the wick beyond is a spring-birth
                        # inception zone
                        top = float(body_hi[hi_p[0]])
                        bot = float(body_lo[lo_p[0]])
                    else:
                        top, bot = hi_p[1], lo_p[1]
                    if top <= bot:      # degenerate body cluster — refuse
                        continue
                    rid_seq += 1
                    r = Range(rid=rid_seq, top=top, bottom=bot, top0=top,
                              bottom0=bot, seed_i=i)
                    r.p0_bar, r.p1_bar = int(p0[0]), int(p1[0])
                    if body_mode:
                        if hi_p[1] > top:
                            r.dev_top_ext = hi_p[1]
                            r.n_inception_zones += 1
                        if lo_p[1] < bot:
                            r.dev_bot_ext = lo_p[1]
                            r.n_inception_zones += 1
                    # the seed's FINAL pivot P1 is the last-touched side;
                    # confirmation must touch the OPPOSITE boundary
                    r.confirm_side = "top" if p1[2] == -1 else "bottom"
                    ranges.append(r)
                    log(i, "seed", rid=r.rid, top=top, bottom=bot,
                        p0_bar=p0[0], p1_bar=p1[0],
                        inception_zones=r.n_inception_zones)
        atr_i = atr[i]

        # potentials: invalidate / confirm
        for r in ranges:
            if r.state != "POTENTIAL":
                continue
            if c[i] > r.top or c[i] < r.bottom:
                r.state = "INVALIDATED"
                r.die_i = i
                log(i, "potential-invalidate", rid=r.rid,
                    px=c[i], boundary=("top" if c[i] > r.top else "bottom"))
                continue
            eps = pins["TOUCH_EPS"] * atr_i
            if r.confirm_side == "top" and h[i] >= r.top - eps:
                r.state = "CONFIRMED"
            elif r.confirm_side == "bottom" and l[i] <= r.bottom + eps:
                r.state = "CONFIRMED"
            if r.state == "CONFIRMED":
                r.confirm_i = i
                r.born_at = i
                r.backdated_from = r.p0_bar
                log(i, "confirm", rid=r.rid, boundary=r.confirm_side,
                    top=r.top, bottom=r.bottom, mid=r.mid)
                log(i, "backdate", rid=r.rid, born_at=i,
                    backdated_from=r.p0_bar)
                if not np.isnan(r.dev_top_ext):
                    log(i, "inception-deviation", rid=r.rid, side="top",
                        extreme=r.dev_top_ext, boundary=r.top)
                if not np.isnan(r.dev_bot_ext):
                    log(i, "inception-deviation", rid=r.rid, side="bottom",
                        extreme=r.dev_bot_ext, boundary=r.bottom)
                if not multi:
                    for q in ranges:
                        if q.state == "POTENTIAL":
                            q.state, q.die_i = "SUPERSEDED", i
                            log(i, "potential-superseded", rid=q.rid)
                    break

        # breach lifecycle, per alive range
        for r in [x for x in ranges if x.state == "CONFIRMED"]:
            pending = r.pending
            if pending is None:
                if c[i] > r.top:
                    r.pending = {"side": "top", "open_i": i,
                                 "extreme": h[i], "body_ext": body_hi[i],
                                 "closes": 1}
                    log(i, "breach-open", rid=r.rid, side="top", px=c[i],
                        boundary=r.top)
                elif c[i] < r.bottom:
                    r.pending = {"side": "bottom", "open_i": i,
                                 "extreme": l[i], "body_ext": body_lo[i],
                                 "closes": 1}
                    log(i, "breach-open", rid=r.rid, side="bottom",
                        px=c[i], boundary=r.bottom)
                pending = r.pending
            else:
                beyond = (c[i] > r.top if pending["side"] == "top"
                          else c[i] < r.bottom)
                if pending["side"] == "top":
                    pending["extreme"] = max(pending["extreme"], h[i])
                    pending["body_ext"] = max(pending["body_ext"], body_hi[i])
                else:
                    pending["extreme"] = min(pending["extreme"], l[i])
                    pending["body_ext"] = min(pending["body_ext"], body_lo[i])
                if beyond:
                    pending["closes"] += 1
                else:
                    # body close back INSIDE
                    bars_out = i - pending["open_i"]
                    if bars_out <= pins["DEV_RETURN_BARS"]:
                        r.n_deviations += 1
                        rd = (pending["body_ext"]
                              if pins.get("REDRAW_BASIS", "wick") == "body"
                              else pending["extreme"])
                        if pending["side"] == "top":
                            r.dev_top_ext = (pending["extreme"]
                                             if np.isnan(r.dev_top_ext)
                                             else max(r.dev_top_ext,
                                                      pending["extreme"]))
                            old_b = r.top
                            r.top = max(r.top, rd)
                        else:
                            r.dev_bot_ext = (pending["extreme"]
                                             if np.isnan(r.dev_bot_ext)
                                             else min(r.dev_bot_ext,
                                                      pending["extreme"]))
                            old_b = r.bottom
                            r.bottom = min(r.bottom, rd)
                        log(i, "harden", rid=r.rid,
                            side=pending["side"], bars_outside=bars_out,
                            extreme=pending["extreme"])
                        log(i, "redraw", rid=r.rid, side=pending["side"],
                            frm=old_b, to=(r.top if pending["side"] == "top"
                                           else r.bottom), mid=r.mid)
                        r.pending = pending = None
                    else:
                        log(i, "breach-lapse", rid=r.rid,
                            side=pending["side"], bars_outside=bars_out)
                    r.pending = pending = None
            if pending is not None:
                die_by_n = pending["closes"] >= pins["BREAK_CONFIRM_N"]
                bnd = r.top if pending["side"] == "top" else r.bottom
                die_by_m = (abs(c[i] - bnd) >= pins["BREAK_MARGIN"] * atr_i
                            and ((c[i] > bnd) if pending["side"] == "top"
                                 else (c[i] < bnd)))
                if die_by_n or die_by_m:
                    r.state, r.die_i = "DEAD", i
                    log(i, "breakout-die", rid=r.rid, side=pending["side"],
                        by=("n_closes" if die_by_n else "margin"),
                        closes=pending["closes"], px=c[i])
                    state = ("BULL_EXP" if pending["side"] == "top"
                             else "BEAR_EXP")
                    r.pending = None
        # memory-line first touches on dead ranges
        for r in ranges:
            if r.state != "DEAD" or r.die_i == i:
                continue
            if r.mem_top_frozen_i < 0 and h[i] >= r.top:
                r.mem_top_frozen_i = i
                log(i, "memory-touch", rid=r.rid, side="top", px=r.top)
            if r.mem_bot_frozen_i < 0 and l[i] <= r.bottom:
                r.mem_bot_frozen_i = i
                log(i, "memory-touch", rid=r.rid, side="bottom", px=r.bottom)
        # coverage + state — union over alive ranges
        alive = [r for r in ranges if r.state == "CONFIRMED"]
        if alive:
            state = "NEUTRAL"
            for r_cov in alive:
                lo_b = (r_cov.bottom if np.isnan(r_cov.dev_bot_ext)
                        else min(r_cov.bottom, r_cov.dev_bot_ext))
                hi_b = (r_cov.top if np.isnan(r_cov.dev_top_ext)
                        else max(r_cov.top, r_cov.dev_top_ext))
                if lo_b <= c[i] <= hi_b:
                    covered[i] = True
                    break
        elif state == "NEUTRAL" and known:
            state = "BULL_EXP" if known[-1][2] == -1 else "BEAR_EXP"

    # pivot events are stamped at their WICK bar with the bar they became
    # KNOWABLE at riding beside; the log ships stable-sorted by bar index
    # [review: "ordered" must mean ordered]
    know = {(p[0], p[1]): cb for cb, p in conf_order}
    for e in ev:
        if e["event"] == "pivot":
            e["knowable_at"] = int(know.get((e["i"], e["px"]),
                                            know.get((e["i"],
                                                      round(e["px"], 2)), -1)))
    ev.sort(key=lambda e: e["i"])

    n_pending_open = sum(1 for r in ranges
                         if r.state == "CONFIRMED" and r.pending is not None)

    conf = [r for r in ranges if r.confirm_i >= 0]
    # censored (still-alive-at-window-end) lifetimes are EXCLUDED from the
    # Q4 mean and counted beside it [review: censoring-as-completion biased
    # the grid for pin sets leaving an open range]
    lifetimes = [r.die_i - r.confirm_i for r in conf if r.die_i >= 0]
    n_censored = sum(1 for r in conf if r.die_i < 0)
    out = {
        "events": ev, "pivots": pivots, "ranges": ranges,
        "coverage_pct": round(100.0 * covered.sum() / n, 2),
        "n_bars": n, "n_pivots": len(pivots),
        "n_confirmed": len(conf),
        "n_potential_unresolved": sum(1 for r in ranges
                                      if r.state == "POTENTIAL"),
        "mean_confirmed_lifetime": (round(float(np.mean(lifetimes)), 1)
                                    if lifetimes else None),
        "n_lifetime_censored": n_censored,
        "n_pending_open": n_pending_open,
        "final_state": state,
        "status_line": "",
    }
    out["status_line"] = (f"{n} CANDLES · {out['coverage_pct']}% RANGE "
                          f"COVERAGE · {out['n_potential_unresolved']} "
                          f"POTENTIAL · {out['n_confirmed']} CONFIRMED · "
                          f"{out['n_pivots']} SUPPORTING PIVOTS · "
                          f"{n_pending_open} D PENDING")
    return out


# ═════════════════════════ STEP 2c · CALIBRATION — KEY-A · VERIFY — KEY-B
# KEY-A: the reference's published statistics (unchanged from RF-1).
# KEY-B: the operator's chart transcription (BTCUSDT.P 1D; our tape is
# BTCUSDT SPOT resampled 4h→1D — a DISCLOSED feed divergence inside the
# ±1,500 USD transcription tolerance).  Calibrate on A; VERIFY on B; a
# divergence IS the finding, never forced.
TARGETS_Q = {
    "Q1_coverage": (80.6, 8.0, 3.0),          # (center, halfband, weight)
    "Q2_pivot_per_bars": (28.5, 8.55, 2.0),    # 27–30 ±30%
    "Q3_conf_per_100": (0.75, 0.375, 1.0),
    "Q4_lifetime": (102.5, 51.5, 1.0),         # 85–110 ±40% → [51, 154]
}

# KEY-B, transcription-grade: (name, from, to, top, bottom, deviations)
# each deviation carries the transcription's own DATE ANCHOR [review: a
# first-hit matcher credited the Oct ATH spike to a July inception event —
# the verdicts survived but the evidence pointers lied]
KEY_B = [
    ("L-R1", "2025-07-01", "2025-11-20", 124_200.0, 100_300.0,
     [("top", 124_000.0, 128_000.0, "2025-10-07"),
      ("bottom", 100_000.0, 107_000.0, "2025-10-10")]),
    ("L-R2", "2025-11-20", "2026-02-10", 96_200.0, 84_600.0,
     [("top", 96_000.0, 99_300.0, "2026-01-15"),
      ("bottom", 83_000.0, 86_500.0, "2025-12-15")]),
    ("L-R3", "2026-02-10", "2026-05-31", 80_100.0, 60_800.0,
     [("bottom", 57_900.0, 62_000.0, "2026-02-20"),
      ("top", 78_000.0, 81_000.0, "2026-05-15")]),
    ("L-R4", "2026-06-01", "2026-08-22", 67_400.0, 60_100.0,
     [("bottom", 57_600.0, 60_300.0, "2026-07-02")]),
]
KEY_B_TOL_USD = 1_500.0
KEY_B_TOL_BARS = 6

# ONE_ACTIVE is PINNED by the v0 calibration of record (multi lost in the
# RF-1 grid); v1 sweeps the six numeric pins in BODY mode [C6].
GRID_COARSE = {
    "LEG_MIN": [0.25, 0.5, 1.0, 1.5],
    "REV_MIN": [1.5, 2.0, 2.5, 3.0, 3.5],
    "TOUCH_EPS": [0.0, 0.15, 0.30, 0.50],
    "DEV_RETURN_BARS": [3, 5, 8, 13],
    "BREAK_CONFIRM_N": [2, 3, 5, 8],
    "BREAK_MARGIN": [1.0, 1.5, 2.0, 3.0],
}


def score(m: dict, d: pd.DataFrame) -> tuple[float, dict]:
    """KEY-A only — the calibration objective (v1)."""
    res = {}
    vals = {
        "Q1_coverage": m["coverage_pct"],
        "Q2_pivot_per_bars": (m["n_bars"] / m["n_pivots"]
                              if m["n_pivots"] else 1e9),
        "Q3_conf_per_100": 100.0 * m["n_confirmed"] / m["n_bars"],
        "Q4_lifetime": (m["mean_confirmed_lifetime"]
                        if m["mean_confirmed_lifetime"] else 0.0),
    }
    s = 0.0
    for k, (c0, hb, w) in TARGETS_Q.items():
        v = vals[k]
        viol = max(0.0, abs(v - c0) - hb) / hb
        res[k] = {"value": round(float(v), 2),
                  "band": [round(c0 - hb, 2), round(c0 + hb, 2)],
                  "violation": round(float(viol), 4)}
        s += w * viol
    return round(s, 4), res


def _bar_of(d: pd.DataFrame, iso_date: str) -> int:
    ts = d["ts"].tolist()
    for i, t in enumerate(ts):
        if t >= iso_date:
            return i
    return len(d) - 1


def verify_key_b(m: dict, d: pd.DataFrame) -> list[dict]:
    """One row per L-R target: the matched range (largest bar-overlap with
    the target window), boundary residuals against the transcription, and
    each transcribed deviation found-or-not (a harden OR an
    inception-deviation on the given side whose extreme falls inside the
    transcribed band ±1,500, within the window ±6 bars)."""
    n = m["n_bars"]
    rows = []
    conf = [r for r in m["ranges"] if r.confirm_i >= 0]
    for name, a, b, top_t, bot_t, devs in KEY_B:
        ia, ib = _bar_of(d, a), _bar_of(d, b)
        best, best_ov = None, 0
        for r in conf:
            lo_r = r.confirm_i
            hi_r = r.die_i if r.die_i >= 0 else n - 1
            ov = max(0, min(ib, hi_r) - max(ia, lo_r))
            if ov > best_ov:
                best, best_ov = r, ov
        row = {"target": name, "window": f"{a}→{b}",
               "target_top": top_t, "target_bottom": bot_t,
               "matched_rid": best.rid if best else None,
               "overlap_bars": best_ov}
        if best:
            # THE TRANSCRIPTION'S OBJECT IS THE BOX [operator grammar]: the
            # range numbers on his chart are the BODY-cluster boundaries;
            # the zones beyond carry the extremes.  So the box basis
            # (top0/bottom0, pre-redraw) is the comparison of record; the
            # redrawn extent prints beside it — two bases, both shown,
            # neither shopped.
            row.update({
                "box_top": round(float(best.top0), 1),
                "box_bottom": round(float(best.bottom0), 1),
                "redrawn_top": round(float(best.top), 1),
                "redrawn_bottom": round(float(best.bottom), 1),
                "top_residual_usd": round(abs(best.top0 - top_t), 1),
                "bottom_residual_usd": round(abs(best.bottom0 - bot_t), 1),
                "top_within_tol": bool(abs(best.top0 - top_t)
                                       <= KEY_B_TOL_USD),
                "bottom_within_tol": bool(abs(best.bottom0 - bot_t)
                                          <= KEY_B_TOL_USD),
            })
            for side, lo_d, hi_d, anchor in devs:
                anchor_i = _bar_of(d, anchor)
                cands = [e for e in m["events"]
                         if e["event"] in ("harden", "inception-deviation")
                         and e.get("rid") == best.rid
                         and e.get("side") == side
                         and ia - KEY_B_TOL_BARS <= e["i"]
                         <= ib + KEY_B_TOL_BARS
                         and lo_d - KEY_B_TOL_USD <= e["extreme"]
                         <= hi_d + KEY_B_TOL_USD]
                hit = (min(cands, key=lambda e: abs(e["i"] - anchor_i))
                       if cands else None)
                key = f"dev_{side}_{int(lo_d / 1000)}k"
                row[key] = (f"FOUND@{hit['ts']} ext {hit['extreme']:.0f} "
                            f"({hit['event']})" if hit else "NOT FOUND")
                row[key + "_found"] = bool(hit)
        rows.append(row)
    return rows


def calibrate(d: pd.DataFrame, verbose: bool = True):
    """Coarse-then-fine over the six free pins.  If nothing satisfies
    Q-1..Q-5, the best three sets print WITH the resisting target — that
    names the wrong rule; it is not forced."""
    import itertools
    keys = list(GRID_COARSE)
    rows = []
    for combo in itertools.product(*(GRID_COARSE[k] for k in keys)):
        pins = dict(zip(keys, combo))
        m = run_machine(d, pins)
        s, res = score(m, d)
        rows.append((s, pins, res, m["status_line"]))
    # DETERMINISTIC TIE-BREAK, disclosed: equal scores prefer FEWER
    # grid-edge pins (an edge choice is a truncated search wearing a
    # winner's name), then lexicographic pins.
    def _edges(p):
        e = 0
        for k, ax in GRID_COARSE.items():
            if isinstance(ax[0], (int, float)) and len(ax) > 1:
                if p[k] <= min(ax) or p[k] >= max(ax):
                    e += 1
        return e
    rows.sort(key=lambda r: (r[0], _edges(r[1]),
                             tuple(sorted(r[1].items()))))
    best = rows[0]
    # fine pass around the winner: ±one half-step per continuous pin
    fine_axes = {
        "LEG_MIN": [max(0.25, best[1]["LEG_MIN"] - 0.25),
                    best[1]["LEG_MIN"], best[1]["LEG_MIN"] + 0.25],
        "REV_MIN": [max(1.0, best[1]["REV_MIN"] - 0.25),
                    best[1]["REV_MIN"], best[1]["REV_MIN"] + 0.25],
        "TOUCH_EPS": [max(0.0, best[1]["TOUCH_EPS"] - 0.1),
                      best[1]["TOUCH_EPS"], best[1]["TOUCH_EPS"] + 0.1],
        "DEV_RETURN_BARS": sorted({max(1, best[1]["DEV_RETURN_BARS"] - 1),
                                   best[1]["DEV_RETURN_BARS"],
                                   best[1]["DEV_RETURN_BARS"] + 1}),
        "BREAK_CONFIRM_N": sorted({max(2, best[1]["BREAK_CONFIRM_N"] - 1),
                                   best[1]["BREAK_CONFIRM_N"],
                                   best[1]["BREAK_CONFIRM_N"] + 1}),
        "BREAK_MARGIN": [max(0.5, best[1]["BREAK_MARGIN"] - 0.25),
                         best[1]["BREAK_MARGIN"],
                         best[1]["BREAK_MARGIN"] + 0.25],
    }
    for combo in itertools.product(*(fine_axes[k] for k in keys)):
        pins = dict(zip(keys, combo), BOUNDARY_MODE="body", MULTI_ACTIVE=0)
        m = run_machine(d, pins)
        s, res = score(m, d)
        rows.append((s, pins, res, m["status_line"]))
    rows.sort(key=lambda r: (r[0], _edges(r[1]),
                             tuple(sorted(r[1].items()))))
    if verbose:
        print(f"\nCALIBRATION SCOREBOARD (coarse {len(list(__import__('itertools').product(*(GRID_COARSE[k] for k in keys))))} + fine) — top 5 of {len(rows)}:")
        for s, pins, res, sl in rows[:5]:
            print(f"  score {s:7.4f}  {pins}")
            print(f"          {sl}")
        s0, p0, r0, _ = rows[0]
        print("\nCHOSEN SET:", p0)
        print("RESIDUALS:")
        for k, v in r0.items():
            print(f"  {k:32} {v}")
        hardq = [k for k, v in r0.items()
                 if k.startswith("Q") and isinstance(v.get("violation"), float)
                 and v["violation"] > 0]
        if hardq:
            print(f"\nRESISTING TARGET(S): {hardq} — the rule they lean on "
                  f"is the suspect; NOT forced. Best three sets above.")
        else:
            print("\nKEY-A (Q-1..Q-4) all satisfied by the chosen set.")
    return rows


# ═══════════════════════════════════════════════════ STEP 2d · EXPORT
def export(d: pd.DataFrame, pins: dict) -> Path:
    """v1: BOTH modes ridden, BOTH keys scored, one artifact."""
    OUT.mkdir(parents=True, exist_ok=True)
    p = OUT / "BTCUSD_1d_ranges_v1.json"
    modes = {}
    for mode in ("body", "wick"):
        mp = dict(pins, BOUNDARY_MODE=mode)
        m = run_machine(d, mp)
        _, res_a = score(m, d)
        modes[mode] = {
            "status_line": m["status_line"],
            "coverage_pct": m["coverage_pct"],
            "key_a_residuals": res_a,
            "key_b": verify_key_b(m, d),
            "events": m["events"],
            "ranges": [asdict(r) for r in m["ranges"]],
        }
    payload = {
        "source": "SS12-RangeFinder v1 twin — the operator's grammar atop "
                  "the v0 reconstruction (@sergio_tesla_); display-only",
        "window": {"start": d["ts"].iloc[0], "end": d["ts"].iloc[-1],
                   "bars": int(len(d)),
                   "dropped_incomplete_days":
                       int(d.attrs["dropped_incomplete_days"])},
        "pins": pins, "atr_len": ATR_LEN,
        "modes": modes,
    }
    txt = json.dumps(payload, indent=1, default=str)
    txt = txt.replace(": NaN", ": null")     # strict JSON [review]
    p.write_text(txt)
    return p


def main() -> int:
    d = daily_bars()
    print(f"WINDOW: {d['ts'].iloc[0]} → {d['ts'].iloc[-1]}  ({len(d)} bars; "
          f"{d.attrs['dropped_incomplete_days']} incomplete day(s) dropped "
          f"at resample)")
    if "--calibrate" in sys.argv:
        rows = calibrate(d)
        return 0
    for mode in ("body", "wick"):
        m = run_machine(d, dict(PINS, BOUNDARY_MODE=mode))
        _, res = score(m, d)
        print(f"\n═══ MODE {mode.upper()} ═══")
        print(m["status_line"])
        print("KEY-A RESIDUALS:", json.dumps(res, default=str))
        print("RANGE TABLE:")
        for r in m["ranges"]:
            if r.confirm_i >= 0:
                print(f"  #{r.rid} {r.state:10} conf@{r.confirm_i} "
                      f"die@{r.die_i} [{r.bottom:.0f} … {r.top:.0f}] "
                      f"dev n={r.n_deviations} incept={r.n_inception_zones} "
                      f"born@{r.born_at}<-{r.backdated_from}")
        print("KEY-B CONCORDANCE:")
        for row in verify_key_b(m, d):
            print("  " + json.dumps(row, default=str))
        if mode == "body":
            print("\nBODY EVENT LOG (lifecycle only):")
            for e in m["events"]:
                if e["event"] != "pivot":
                    print("  " + json.dumps(e))
    p = export(d, PINS)
    sha = hashlib.sha256(p.read_bytes()).hexdigest()
    print(f"\nEXPORT {p}  {p.stat().st_size:,} B  sha256 {sha[:16]}…")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
