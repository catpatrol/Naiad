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
    seals: list[int] = []                       # the bar each pivot SEALED at
                                                # [F-RF-12: the post-hoc scan
                                                # diverged from the seal bar
                                                # on the 4h tape — knowability
                                                # IS the seal, recorded live]
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
                seals.append(i)
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
                seals.append(i)
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
                seals.append(i)
                log(ext_i, "pivot", px=ext_px, side="low")
                zdir, ext_i, ext_px = 1, i, h[i]
    order = sorted(range(len(pivots)), key=lambda k: pivots[k][0])
    pivots = [pivots[k] for k in order]
    seals = [seals[k] for k in order]

    # ── the lifecycle sweep
    piv_by_bar = {}
    for p in pivots:
        piv_by_bar.setdefault(p[0], []).append(p)
    confirmed_at: dict[int, int] = {}      # pivot bar -> bar it CONFIRMED at
    # a pivot at bar b is only knowable at its reversal bar; replay that:
    # knowability IS the recorded seal bar — the prior post-hoc REV-only
    # rescan ignored the LEG_MIN merge deferral and diverged from the
    # sequential machine on the 4h tape [F-RF-12]
    conf_order: list[tuple[int, tuple]] = list(zip(seals, pivots))
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
    know = {(p[0], round(p[1], 2)): cb for cb, p in conf_order}
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


# ═══════════════════════════ v2 · HIERARCHY + FLIPS + THE LEASH [RF-3]
# The identical machine runs TWICE on the 4h tape: MACRO (LEG_MIN and
# REV_MIN scaled by SCALE_MULT) is the primary structure and the ONLY
# writer of global state, memory lines and flips; MICRO (v1 pins FROZEN,
# never refit) renders subordinate and only inside a live macro range.
#
# v2 PINNED READINGS:
#   CONTAINMENT [H1]  a micro range is KEPT iff at its confirm bar a macro
#                     range is alive AND the micro's span-at-birth
#                     (boundaries + inception zones) lies inside the
#                     macro's current span (boundaries + zones). Everything
#                     else is filed as micro-suppressed, counted, unrendered.
#   FLIP [H2, observed — the operator's own grey arrows] the FIRST retest
#                     of a dead macro boundary, approached from the side
#                     OPPOSITE its birth side, that survives FLIP_HOLD_BARS
#                     bars with no body close through by FLIP_HOLD_MARGIN×
#                     ATR ⇒ ▲ (dead top → support) / ▼ (dead bottom →
#                     resistance). A truncated hold window (tape ends) does
#                     NOT confirm. A fail-through stays a plain touch —
#                     AND CONSUMES THE CANDIDACY [review-pinned]: one
#                     evaluation per line, ever; later opposite touches
#                     log "candidacy consumed" and can never flip. The
#                     rival first-retest-THAT-HOLDS reading would print a
#                     ▼ at 65,359 on 2026-06-17 — filed as the operator's
#                     arbitration exhibit, not enacted.
#   LEASH [H3]        memory lines are MACRO corpses only; a line untouched
#                     for MEM_TTL_BARS after death expires (reason ttl); at
#                     most 6 LIVE (unfrozen, unexpired) lines per side —
#                     the oldest expires (reason cap). Expiry precedes any
#                     later touch: an expired line neither freezes nor flips.
#   TTL DEFAULT       400 as PROPOSED by the commission — no KEY-C row
#                     constrains it, so it is adopted, not fitted; disclosed.

V2_WINDOW_BARS = 1700          # 4h bars: 2025-11-12 → now; the Jan shelf
                               # forms inside, per C-R3's "visible-left"
MEM_CAP_PER_SIDE = 6           # H3, commissioned

PINS_V2 = {
    # v2 CALIBRATION OF RECORD (written by --calibrate-v2; micro pins are
    # v1's ruled values, FROZEN, read by fixture from the v1 pine)
    # v2 CALIBRATION OF RECORD (KEY-C objective, 36 cells): score 2.9968.
    # TIED with SCALE 3.5 at the same score (3.5 covers 39.18% vs 31.94%);
    # the deterministic tie-break chose 3.0 — disclosed. FLIP_HOLD_MARGIN
    # 1.0 is what lets C-F2's Apr 18–19 hold window survive (deepest
    # window close 75,205.6 vs 75,998.9 − 1.0×ATR ≈ 75,104 — held by
    # ~101 USD; era ATR ~0.9–1.0k; margins 0.25/0.5 fail through, and
    # BARS 12/18 extend the window into the 2026-04-19T16:00 close
    # 74,917.9, which also fails — BARS 6 is load-bearing too)
    # [doc-prep lens: the first draft's story numbers were wrong on all
    # three counts while the headline claim survived].
    "SCALE_MULT": 3.0,
    "FLIP_HOLD_MARGIN": 1.0,
    "FLIP_HOLD_BARS": 6,
    "MEM_TTL_BARS": 400,       # PROPOSED, adopted, not fitted [disclosed]
}


def bars_4h(n_bars: int = V2_WINDOW_BARS) -> pd.DataFrame:
    """The raw 4h tape, no resample — KEY-C is a 4h transcription."""
    f = pd.read_parquet(cache_dir() / "klines" / "BTCUSDT_4h.parquet")
    d = f.tail(n_bars).reset_index(drop=True)
    d = d.rename(columns={"open": "o", "high": "h", "low": "l",
                          "close": "c", "open_time": "t0"})
    d["ts"] = pd.to_datetime(d["t0"], unit="ms", utc=True).dt.strftime(
        "%Y-%m-%dT%H:%M")
    d.attrs["dropped_incomplete_days"] = 0
    return d


def _span(r) -> tuple:
    lo = r.bottom if np.isnan(r.dev_bot_ext) else min(r.bottom, r.dev_bot_ext)
    hi = r.top if np.isnan(r.dev_top_ext) else max(r.top, r.dev_top_ext)
    return float(lo), float(hi)


def _span_at(r, events, i: int) -> tuple:
    """A range's span AS OF bar i, reconstructed from its own events —
    boundaries at their pre-redraw values plus any zone extremes logged at
    or before i.  [review L1/L3: the first draft read END-OF-RUN spans —
    look-ahead in the machine of record, and a third variant in the pine.]
    """
    top, bot = float(r.top0), float(r.bottom0)
    for e in events:
        if e.get("rid") != r.rid or e["i"] > i:
            continue
        if e["event"] in ("inception-deviation", "harden"):
            if e["side"] == "top":
                top = max(top, float(e["extreme"]))
            else:
                bot = min(bot, float(e["extreme"]))
    return bot, top


def containment(micro: dict, macro: dict) -> tuple[list, list]:
    """[H1] kept micro rids + suppression events.  Spans AS OF the micro's
    confirm bar — at-birth for the micro, current-as-of-that-bar for the
    macro [pinned law; never end-of-run]."""
    kept, sup = [], []
    for r in micro["ranges"]:
        if r.confirm_i < 0:
            continue
        i = r.confirm_i
        parent = None
        for q in macro["ranges"]:
            if q.confirm_i >= 0 and q.confirm_i <= i and (
                    q.die_i < 0 or q.die_i > i):
                parent = q
                break
        if parent is None:
            sup.append({"i": i, "event": "micro-suppressed", "rid": r.rid,
                        "reason": "no_live_macro"})
            continue
        mlo, mhi = _span_at(r, micro["events"], i)
        plo, phi = _span_at(parent, macro["events"], i)
        if mlo >= plo and mhi <= phi:
            kept.append((r.rid, parent.rid))
        else:
            sup.append({"i": i, "event": "micro-suppressed", "rid": r.rid,
                        "reason": "outside_macro_span",
                        "parent_rid": parent.rid})
    return kept, sup


def flips_and_leash(macro: dict, d: pd.DataFrame, pins: dict) -> list[dict]:
    """[H2+H3] the memory-line lifecycle, re-walked post-machine: expiry
    (ttl/cap) precedes touches; the first opposite-side touch that holds
    flips. Returns ordered leash/flip events."""
    h, l, c = (d["h"].to_numpy(float), d["l"].to_numpy(float),
               d["c"].to_numpy(float))
    atr = ind.atr(h, l, c, ATR_LEN)
    ts = d["ts"].tolist()
    n = len(d)
    ttl = int(pins["MEM_TTL_BARS"])
    hold_n = int(pins["FLIP_HOLD_BARS"])
    hold_m = float(pins["FLIP_HOLD_MARGIN"])
    # line registry: (rid, side, px, born_i)
    lines = []
    for r in macro["ranges"]:
        # corpses = DEAD CONFIRMED ranges only [H2/H3 law; the first run
        # admitted invalidated candidates and printed phantom flips]
        if r.state == "DEAD" and r.confirm_i >= 0 and r.die_i >= 0:
            lines.append({"rid": r.rid, "side": "top", "px": float(r.top),
                          "born": r.die_i, "state": "live", "die_ts":
                          ts[r.die_i]})
            lines.append({"rid": r.rid, "side": "bottom",
                          "px": float(r.bottom), "born": r.die_i,
                          "state": "live", "die_ts": ts[r.die_i]})
    ev = []
    for i in range(n):
        # cap: count live per side, expire oldest [H3]
        for side in ("top", "bottom"):
            live = [x for x in lines if x["side"] == side
                    and x["state"] == "live" and x["born"] <= i]
            if len(live) > MEM_CAP_PER_SIDE:
                for x in sorted(live, key=lambda y: y["born"])[
                        :len(live) - MEM_CAP_PER_SIDE]:
                    x["state"] = "expired"
                    ev.append({"i": i, "ts": ts[i], "event": "line-expired",
                               "rid": x["rid"], "side": side,
                               "px": round(x["px"], 1), "reason": "cap"})
        for x in lines:
            if x["state"] not in ("live", "frozen") or x["born"] >= i:
                continue
            if x.get("flip_done"):
                if l[i] <= x["px"] <= h[i]:
                    ev.append({"i": i, "ts": ts[i],
                               "event": ("flip-retest" if x.get("flipped")
                                         else "memory-retest"),
                               "rid": x["rid"], "side": x["side"],
                               "px": round(x["px"], 1),
                               **({} if x.get("flipped") else
                                  {"verdict": "candidacy consumed — the "
                                              "one evaluation is spent "
                                              "[pinned]"})})
                continue
            # ttl runs from death; an expired line neither freezes nor flips
            if x["state"] == "live" and i - x["born"] > ttl:
                x["state"] = "expired"
                ev.append({"i": i, "ts": ts[i], "event": "line-expired",
                           "rid": x["rid"], "side": x["side"],
                           "px": round(x["px"], 1), "reason": "ttl"})
                continue
            # TWO-SIDED touch [H2 law, review-of-first-run]: a dead bottom's
            # flip retest arrives from BELOW (h crosses up into it) — the
            # one-sided test could only see birth-side touches, so a line
            # frozen by a same-side crash was blind to the very retest the
            # operator's arrow marks.
            touched = l[i] <= x["px"] <= h[i]
            if not touched:
                continue
            if x["state"] == "live":
                x["state"] = "frozen"          # freeze at FIRST touch (any
                x["touch_i"] = i               # side) — the v1 render law
            # flip candidacy [H2]: the FIRST OPPOSITE-side approach gets ONE
            # evaluation, frozen or not; same-side touches spend nothing
            appr_above = c[i - 1] > x["px"]
            opposite = (appr_above if x["side"] == "top"
                        else not appr_above)
            if not opposite:
                ev.append({"i": i, "ts": ts[i], "event": "memory-retest",
                           "rid": x["rid"], "side": x["side"],
                           "px": round(x["px"], 1),
                           "verdict": "same-side touch, no flip candidacy"})
                continue
            x["flip_done"] = True          # one evaluation, consumed
            if i + hold_n >= n:
                ev.append({"i": i, "ts": ts[i], "event": "memory-retest",
                           "rid": x["rid"], "side": x["side"],
                           "px": round(x["px"], 1),
                           "verdict": "hold window truncated by tape end — "
                                      "NOT confirmed"})
                continue
            held = True
            for k in range(i, i + hold_n + 1):
                thr = hold_m * atr[k]
                through = (c[k] < x["px"] - thr if x["side"] == "top"
                           else c[k] > x["px"] + thr)
                if through:
                    held = False
                    break
            if held:
                ev.append({"i": i, "ts": ts[i], "event": "flip",
                           "rid": x["rid"], "side": x["side"],
                           "px": round(x["px"], 1),
                           "polarity": ("support" if x["side"] == "top"
                                        else "resistance"),
                           "glyph": "▲" if x["side"] == "top" else "▼",
                           "parent_death": x["die_ts"],
                           "retest": ts[i]})
                x["flipped"] = True
            else:
                ev.append({"i": i, "ts": ts[i], "event": "memory-retest",
                           "rid": x["rid"], "side": x["side"],
                           "px": round(x["px"], 1),
                           "verdict": "failed through within the hold "
                                      "window — touch only"})
    return ev


def run_v2(d: pd.DataFrame, pins_v2: dict) -> dict:
    micro_pins = dict(PINS)                    # v1 ruled values, FROZEN
    macro_pins = dict(PINS,
                      LEG_MIN=PINS["LEG_MIN"] * pins_v2["SCALE_MULT"],
                      REV_MIN=PINS["REV_MIN"] * pins_v2["SCALE_MULT"])
    macro = run_machine(d, macro_pins)
    micro = run_machine(d, micro_pins)
    kept, sup = containment(micro, macro)
    leash = flips_and_leash(macro, d, pins_v2)
    kept_rids = {k for k, _ in kept}
    micro_kept_events = [e for e in micro["events"]
                         if e.get("rid") is None or e["rid"] in kept_rids
                         or e["event"] == "pivot"]
    conf_feb_aug = [r for r in macro["ranges"] if r.confirm_i >= 0
                    and d["ts"].iloc[r.confirm_i] >= "2026-02-01"]
    out = {
        "macro": macro, "micro": micro, "kept": kept, "suppressed": sup,
        "micro_kept_events": micro_kept_events, "leash": leash,
        "flips": [e for e in leash if e["event"] == "flip"],
        "state": macro["final_state"],
        "macro_count_feb_aug": len(conf_feb_aug),
        "status_line": (f"{len(d)} CANDLES · {macro['final_state']} · "
                        f"{macro['coverage_pct']}% COV (MACRO) · "
                        f"{macro['n_pending_open']} PENDING · "
                        f"{macro['n_confirmed']} MACRO · "
                        f"{len(kept)} MICRO · "
                        f"{macro['n_pivots']} PIVOTS"),
    }
    return out


# ═══════════════════════════════════ v2 · KEY-C VERIFY + CALIBRATE
KEY_C_TOL_USD = 1_200.0
KEY_C_TOL_BARS = 8

KEY_C_RANGES = [
    # (name, window_a, window_b, top, bottom, midline, devs)
    ("C-R1", "2026-02-01", "2026-05-31", 75_000.0, 59_900.0, 66_500.0,
     [("bottom", 57_900.0, 62_000.0, "2026-02-20"),
      ("top", 75_000.0, 78_500.0, "2026-04-15")]),
    ("C-R2", "2026-06-01", "2026-08-22", 67_300.0, 59_900.0, None,
     [("bottom", 57_600.0, 60_300.0, "2026-07-02")]),
    ("C-R3", "2025-12-01", "2026-02-05", None, 84_500.0, None,
     [("top", 95_000.0, 97_500.0, "2026-01-05")]),
]
KEY_C_FLIPS = [
    ("C-F1", "resistance", 84_500.0, 1_500.0, "2026-02-01"),
    ("C-F2", "support", 75_000.0, 1_200.0, "2026-05-15"),
]


def verify_key_c(v2: dict, d: pd.DataFrame) -> list[dict]:
    ts = d["ts"].tolist()
    n = len(d)

    def bar_of(s):
        for i, t in enumerate(ts):
            if t >= s:
                return i
        return n - 1
    rows = []
    macro = v2["macro"]
    conf = [r for r in macro["ranges"] if r.confirm_i >= 0]
    for name, a, b, top_t, bot_t, mid_t, devs in KEY_C_RANGES:
        ia, ib = bar_of(a), bar_of(b)
        best, best_ov = None, 0
        for r in conf:
            hi_r = r.die_i if r.die_i >= 0 else n - 1
            ov = max(0, min(ib, hi_r) - max(ia, r.confirm_i))
            if ov > best_ov:
                best, best_ov = r, ov
        row = {"target": name, "matched_rid": best.rid if best else None,
               "overlap_bars": best_ov}
        if best:
            # the RF-2 finding carried: the operator's numbers track the
            # REDRAWN extent — both bases print, redrawn is the comparison
            for label, t_val, got_box, got_rd in (
                    ("top", top_t, best.top0, best.top),
                    ("bottom", bot_t, best.bottom0, best.bottom)):
                if t_val is None:
                    continue
                row[f"{label}_redrawn"] = round(float(got_rd), 1)
                row[f"{label}_box"] = round(float(got_box), 1)
                row[f"{label}_residual"] = round(abs(got_rd - t_val), 1)
                row[f"{label}_within"] = bool(abs(got_rd - t_val)
                                              <= KEY_C_TOL_USD)
            if mid_t is not None:
                mid = (best.top + best.bottom) / 2
                row["mid_residual"] = round(abs(mid - mid_t), 1)
                row["mid_within"] = bool(abs(mid - mid_t) <= KEY_C_TOL_USD)
            for side, lo_d, hi_d, anchor in devs:
                ai = bar_of(anchor)
                cands = [e for e in macro["events"]
                         if e["event"] in ("harden", "inception-deviation")
                         and e.get("rid") == best.rid
                         and e.get("side") == side
                         and lo_d - KEY_C_TOL_USD <= e["extreme"]
                         <= hi_d + KEY_C_TOL_USD]
                hit = (min(cands, key=lambda e: abs(e["i"] - ai))
                       if cands else None)
                key = f"dev_{side}_{int(lo_d / 1000)}k"
                row[key] = (f"FOUND@{hit['ts']} ext {hit['extreme']:.0f} "
                            f"({hit['event']})" if hit else "NOT FOUND")
                row[key + "_found"] = bool(hit)
        rows.append(row)
    for name, pol, px_t, tol, anchor in KEY_C_FLIPS:
        ai = bar_of(anchor)
        cands = [e for e in v2["flips"]
                 if e["polarity"] == pol and abs(e["px"] - px_t) <= tol]
        hit = min(cands, key=lambda e: abs(e["i"] - ai)) if cands else None
        in_time = bool(hit and abs(hit["i"] - ai) <= 180)  # ~30d of 4h
        # bars; computed-not-asserted [disclosed]: the April flip + May
        # flip-retests is the accepted C-F2 reading
        rows.append({"target": name, "polarity": pol, "line": px_t,
                     "found": (f"{hit['glyph']}@{hit['ts']} px {hit['px']}"
                               if hit else "NOT FOUND"),
                     "found_flag": bool(hit),
                     "near_anchor": in_time})
    rows.append({"target": "C-Q1",
                 "macro_confirms_feb_aug": v2["macro_count_feb_aug"],
                 "within_2_4": bool(2 <= v2["macro_count_feb_aug"] <= 4)})
    return rows


def score_key_c(v2: dict, d: pd.DataFrame) -> tuple[float, list]:
    rows = verify_key_c(v2, d)
    s = 0.0
    for row in rows:
        t = row["target"]
        if t.startswith("C-R"):
            if row.get("matched_rid") is None:
                s += 5.0
                continue
            for k, v in row.items():
                if k.endswith("_residual") and v is not None:
                    s += max(0.0, v - KEY_C_TOL_USD) / KEY_C_TOL_USD
                if k.endswith("_found") and not v:
                    s += 1.0
        elif t.startswith("C-F"):
            if not row["found_flag"]:
                s += 3.0
        elif t == "C-Q1" and not row["within_2_4"]:
            s += 3.0
    return round(s, 4), rows


def calibrate_v2(d: pd.DataFrame):
    """Fit ONLY the four v2 pins (TTL adopted at the proposed 400 — no
    KEY-C row constrains it, disclosed); micro pins FROZEN."""
    import itertools
    grid = {"SCALE_MULT": [2.5, 3.0, 3.5, 4.0],
            "FLIP_HOLD_MARGIN": [0.25, 0.5, 1.0],
            "FLIP_HOLD_BARS": [6, 12, 18]}
    rows = []
    for combo in itertools.product(*grid.values()):
        pins = dict(zip(grid, combo), MEM_TTL_BARS=400)
        v2 = run_v2(d, pins)
        s, res = score_key_c(v2, d)
        rows.append((s, pins, v2["status_line"]))
    rows.sort(key=lambda r: (r[0], tuple(sorted(r[1].items()))))
    print(f"\nKEY-C SCOREBOARD ({len(rows)} cells) — top 5:")
    for s, pins, sl in rows[:5]:
        print(f"  score {s:7.4f}  {pins}")
        print(f"          {sl}")
    s0, p0, _ = rows[0]
    print("\nCHOSEN v2 SET:", p0)
    v2 = run_v2(d, p0)
    _, res = score_key_c(v2, d)
    print("KEY-C RESIDUALS:")
    for row in res:
        print("  " + json.dumps(row, default=str))
    return rows


def export_v2(d: pd.DataFrame, pins_v2: dict) -> Path:
    v2 = run_v2(d, pins_v2)
    _, res = score_key_c(v2, d)
    OUT.mkdir(parents=True, exist_ok=True)
    p = OUT / "BTCUSD_4h_ranges_v2.json"
    payload = {
        "source": "SS12-RangeFinder v2 twin — hierarchy + flips + leash "
                  "(RF-3); display-only",
        "window": {"start": d["ts"].iloc[0], "end": d["ts"].iloc[-1],
                   "bars": int(len(d)), "tf": "4h"},
        "pins_v2": pins_v2, "micro_pins_frozen": PINS,
        "mem_cap_per_side": MEM_CAP_PER_SIDE,
        "status_line": v2["status_line"],
        "key_c": res,
        "flips": v2["flips"], "leash_events": v2["leash"],
        "suppressed_micro": v2["suppressed"],
        "kept_micro": v2["kept"],
        "macro_events": v2["macro"]["events"],
        "macro_ranges": [asdict(r) for r in v2["macro"]["ranges"]],
        "micro_ranges": [asdict(r) for r in v2["micro"]["ranges"]],
    }
    txt = json.dumps(payload, indent=1, default=str)
    txt = txt.replace(": NaN", ": null")
    p.write_text(txt)
    return p
