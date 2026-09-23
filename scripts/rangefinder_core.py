"""SS12-RANGEFINDER · THE ORACLE'S MACHINE — the RangeFinder v2 state machine
as an importable module, under scripts/, where the Oracle lane may write.

DISPLAY-ONLY · A MEASUREMENT ORGAN. RENDERS, NEVER RULES: this module
describes structure on a tape and rules NOTHING. NO DECISION PATH MAY IMPORT
IT [OR-1 firewall, atop BR-1 §2]: no gate, filter, heat, station, card or
sizing computation may read a range. posture_engine, every tierc*_rules
module, engine.signals, engine.trading, engine.htf and engine.replay stay
strangers to this file; the range object exists in the Oracle's render and
in its SIBLING tape (research_outputs/oracle/tape_ranges/, A-OR1-1 v) and
nowhere else. F-BR-14 measures that rather than trusting it: this module's
name is on RANGE_BANNED_IN_DECISION and the decision modules' import closures
are scanned component-wise for it, and a planted gate read must go red.

WHY IT LIVES HERE — AMENDMENT A-OR1-1 (operator, 2026-09-22), clause iv,
verbatim: "The range module lives at scripts/rangefinder_core.py; engine/ is
outside this lane's write authority (BR-1 §2 clause 3); promotion into
engine/ is APOLLO's call." OR-1 STEP D1 (commit 1695a69) had CREATED
engine/rangefinder.py, and BR-1 §2 clause 3 lets this lane import engine
modules read-only and never modify them. That write is RECORDED, NOT UNDONE:
research_outputs/oracle/recovery/D1_engine_rangefinder_1695a69.patch
(`git show 1695a69 -- engine/rangefinder.py`, sha256 ed6d5170200b045f…,
51,672 B).

COPIED, NOT MOVED. Every byte below this docstring is a copy of
engine/rangefinder.py at sha256
bbae464fdc8e0e01fc90b286aa79e726fcff4422e6118dee1173f2460dab84d4 (960 lines,
49,981 B), from its `from __future__` line to its last. That file STAYS WHERE
IT IS, BYTE-FROZEN: TIER-C10 made it its machine of record
(F-C10-RESUME-6 pins its bytes; scripts/tierc10_rf_fixtures.py imports it and
its F-RF-EQ holds a port to it), so deleting or editing it would break a
ratified lane's filed registrations. Its disposition — keep it, delete it, or
promote this copy over it — is APOLLO's call (A-OR1-1 iv), not this lane's.
For the same reason scripts/rangefinder_twin.py is still a thin caller of
engine.rangefinder, not of this module: F-C10-RESUME-6 pins the twin's bytes
too, so re-pointing it here is REPORTED, NOT DONE.

TWO COPIES, ONE MACHINE, AND WHAT KEEPS THEM ONE. scripts/
rangefinder_core_fixtures.py holds three fixtures. F-RF-1c runs the five
event logs below through THIS module and requires each to equal the record
AND engine.rangefinder's own output on the same tape AND a second run byte
for byte. F-RF-1d requires snapshot() to agree between the two modules on
the live 4h cache for roster symbols. F-RF-1e compares an AST dump of every
top-level definition, name by name (expected: none differ). An edit that
lands in one copy and not the other is RED there — the pins, a constant, a
law, a docstring.

THE FIVE EVENT SHAS OF RECORD — sha256(json.dumps(events, sort_keys=True))
on the FROZEN tape: BTCUSDT 4h truncated in memory to open_time <=
1787371200000 (2026-08-22T04:00Z, rangefinder_twin.RECORD_ANCHOR_MS); the
last 1,700 4h bars for v2, the last 420 complete UTC days for v1, exactly as
the twin's loaders build them:
  v2 macro      92 events   2145418831a00be710fb401c3a7c16722c0857feda4a29d58d503f3dc2b09ed4
  v2 micro     573 events   73798d744a377d6f2398020b0ae891d2f34efab2e48fda1c0e745243e2b04c72
  v2 leash     153 events   824cdff43675053a54f5c2cbbec9ba8b87c2e3661fca20c00459880bd17ec54e
  v2 suppress   17 events   e7b0de6a072ea9ba0c5bb0b7dc2c0ebba72d68e2730b1e6056f26fa7189dba70
  v1 body      152 events   af2485e664bf822492e8bb86ef4c45afb05844bed5e342f4a9aa30588dba5404

THE QUIRKS ARE THE BYTES, AND NONE WAS TIDIED IN THE COPY: log() rounds every
int or float keyword to 2 dp THROUGH float() (so integer-valued fields ship
as floats) except rid/bars/count; event keys keep insertion order; pivots
are logged first and the list is then STABLE-sorted on "i"; Range field
order is the asdict() export order; PINS / PINS_V2 key order is export
order; pending/top carry np.float64; ATR is engine.indicators.atr at
ATR_LEN = 14, seeded at the window's first bar; run_v2's "2026-02-01" is a
BTC KEY-C literal. The PINNED READINGS the machine enacts are engine/
rangefinder.py's header, word for word; they are not repeated here.

THE FUNCTION DOCSTRINGS BELOW SPEAK FOR engine/rangefinder.py. They were
copied with the code, so that the AST comparison can include them. Where one
says "the twin's bars_4h now calls it", or names F-RF-10's monkeypatch of
rangefinder_twin.MEM_CAP_PER_SIDE, it describes the ENGINE copy's callers.
This module's one PRODUCTION caller is scripts/oracle_daily.py
(`import rangefinder_core as RNG`), which reads V2_WINDOW_BARS, PINS_V2,
tape_from_klines, run_v2 and snapshot. Its fixtures import it too:
scripts/rangefinder_core_fixtures.py (F-RF-1c/d/e) and F-BR-14's closure
probe in scripts/oracle_fixtures.py.

IMPORT SURFACE: numpy, pandas, dataclasses, and engine.indicators imported
read-only (BR-1 §2 clause 3). Nothing else — no IO, no network, no wall
clock, no cache path. F-BR-14 measures this module's closure against
RANGE_BANNED_IN_MACHINE (no trading, journal, analytics, signals, replay,
forward_log or positions component).

KNOWN HAZARD FOR LOW-PRICED SYMBOLS [reported, not fixed — fixing it would
move the bytes above]: log() rounds to 2 dp and _span_at reads the ROUNDED
"extreme" back, so MICRO containment is distorted on sub-dollar tapes. The
MACRO Range fields are full precision; snapshot() reads those, never the
events, and the Oracle prints no micro range.

NOTHING UNDER engine/ CHANGED, so there is no engine version bump and no
journal byte moves.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from engine import indicators as ind

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


def flips_and_leash(macro: dict, d: pd.DataFrame, pins: dict,
                    mem_cap: int | None = None) -> list[dict]:
    """[H2+H3] the memory-line lifecycle, re-walked post-machine: expiry
    (ttl/cap) precedes touches; the first opposite-side touch that holds
    flips. Returns ordered leash/flip events.

    mem_cap [OR-1 lift, TRAP 1]: the H3 cap, defaulting to THIS module's
    MEM_CAP_PER_SIDE read at CALL time. It is a keyword because F-RF-10's
    break leg monkeypatches rangefinder_twin.MEM_CAP_PER_SIDE and calls
    the twin's flips_and_leash: the twin keeps a thin wrapper that reads
    ITS OWN global at call time and hands it in here. A plain re-export
    would have made that patch inert and the fixture void."""
    cap = MEM_CAP_PER_SIDE if mem_cap is None else int(mem_cap)
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
            if len(live) > cap:
                for x in sorted(live, key=lambda y: y["born"])[
                        :len(live) - cap]:
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


def run_v2(d: pd.DataFrame, pins_v2: dict,
           mem_cap: int | None = None) -> dict:
    # mem_cap rides through to flips_and_leash untouched [OR-1 lift]: the
    # twin's run_v2 wrapper hands in the TWIN's own MEM_CAP_PER_SIDE so a
    # patched twin global governs everything the twin runs, exactly as it
    # did before the lift (export_v2 prints that same global).
    micro_pins = dict(PINS)                    # v1 ruled values, FROZEN
    macro_pins = dict(PINS,
                      LEG_MIN=PINS["LEG_MIN"] * pins_v2["SCALE_MULT"],
                      REV_MIN=PINS["REV_MIN"] * pins_v2["SCALE_MULT"])
    macro = run_machine(d, macro_pins)
    micro = run_machine(d, micro_pins)
    kept, sup = containment(micro, macro)
    leash = flips_and_leash(macro, d, pins_v2, mem_cap=mem_cap)
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


# ═══════════════ OR-1 · ADDITIVE — the Daily Oracle's display surface
# NEW at OR-1 STEP D, not lifted. Two pure functions, no IO, no wall clock:
# the Oracle (cache-only, never fetches) reads its own parquet and hands the
# frame in. DISPLAY-ONLY like everything above: what these return may reach
# the render and the tape and NOTHING that gates, filters, heats, stations,
# cards or sizes [OR-1 firewall].
def tape_from_klines(f: pd.DataFrame, n_bars: int = V2_WINDOW_BARS,
                     ts_fmt: str = "%Y-%m-%dT%H:%M") -> pd.DataFrame:
    """A cached klines frame (open_time ms, open, high, low, close[, volume])
    → the machine's tape (o h l c t0 ts): the LAST n_bars rows, renamed, with
    `ts` the bar-OPEN time in UTC rendered by ts_fmt (a sortable string — the
    machine compares and prints it, never parses it).

    This IS the body of the twin's bars_4h with the read_parquet left behind;
    the twin's bars_4h now calls it, so the frozen-tape sha of record
    (bda85c2e…, csv of t0,o,h,l,c) proves the two are one. `f` is never
    mutated (tail/reset_index/rename each return a new frame). A frame
    shorter than n_bars yields the shorter tape — no padding, no refusal;
    the caller prints the true bar count (snapshot carries n_bars).
    attrs["dropped_incomplete_days"] = 0 is a TRUE statement for a raw,
    un-resampled tape and keeps the frame interchangeable with the twin's."""
    d = f.tail(n_bars).reset_index(drop=True)
    d = d.rename(columns={"open": "o", "high": "h", "low": "l",
                          "close": "c", "open_time": "t0"})
    d["ts"] = pd.to_datetime(d["t0"], unit="ms", utc=True).dt.strftime(
        ts_fmt)
    d.attrs["dropped_incomplete_days"] = 0
    return d


def snapshot(d: pd.DataFrame, v2: dict) -> dict:
    """What the Oracle prints for one symbol, AS OF THE TAPE'S LAST BAR, from
    `v2 = run_v2(d, PINS_V2)` on that same tape `d`.

    PRICES COME FROM THE Range OBJECTS (full precision), NEVER from the
    events: log() rounds to 2 dp, which is noise on BTC and the whole number
    on a sub-dollar symbol. Nothing here is rounded — the renderer rounds.
    Every value is a builtin float/int/str/bool/None (json-ready), and the
    key order below is fixed.

    THE MACRO SCALE ONLY: macro is the primary structure and the only writer
    of global state [v2 law, above]; micro never reaches this dict except
    inside status_line's own count.

      state           v2["state"]: NEUTRAL | BULL_EXP | BEAR_EXP. ALWAYS
                      reported, range or no range.
      has_range       a CONFIRMED macro range is alive at the last bar. At the
                      shipped pins (MULTI_ACTIVE 0) there is at most one; were
                      several ever alive, the newest-seeded is the one read.
      top, bottom     its CURRENT (redrawn-so-far) boundaries.
      top0, bottom0   its original box, pre-redraw.
      mid             (top + bottom) / 2.
      pos_pct         100 * (close - bottom) / (top - bottom). NOT clamped:
                      during an open breach it reads < 0 or > 100, and that is
                      the truth worth printing.
      atr             engine.indicators.atr(h, l, c, ATR_LEN)[-1] on THIS tape
                      — the machine's own ATR (same call, same seed), on the
                      tape's own timeframe. Reported range or no range.
      dist_atr        min(|top - close|, |close - bottom|) / atr — the
                      distance to the NEAREST macro boundary, inside or
                      outside it, in ATR. None when atr is not a positive
                      finite number.
      nearest_side    "top" | "bottom", whichever boundary dist_atr measured;
                      an exact tie reads "top" (pinned, arbitrary, disclosed).
      pending         the open breach on that range, or None:
                      {side, open_ts, bars_out, closes} — bars_out counts
                      bars since the breach-open bar (the machine's own
                      `i - open_i`, taken at the last bar); closes is the
                      machine's consecutive-beyond count.
      n_pending_open  macro["n_pending_open"].
      n_potential     macro["n_potential_unresolved"].
      last_event      {event, ts, age_bars} of the last NON-PIVOT macro event
                      — a pivot is stamped at its WICK bar, not the bar it
                      became knowable, so its "age" would lie. age_bars =
                      n - 1 - i. Keyed on ts, never on rid: rid numbering is
                      per run and shifts as the window slides. None when the
                      log holds no lifecycle event yet.
      status_line     v2["status_line"], verbatim.
      as_of, close, n_bars   the last bar's ts, its close, and the tape
                      length — what every number above was measured against,
                      so a reader (or a fixture) can recompute them.

    THE EMPTY CASE, explicit — most symbols, most days (8 of 10 cached
    symbols on 2026-09-21): no live CONFIRMED macro range ⇒ has_range False
    and top, bottom, top0, bottom0, mid, pos_pct, dist_atr, nearest_side and
    pending are ALL None. state, atr, the counts, last_event and status_line
    are still reported. A renderer must print the absence ("no live macro
    range"), never a zero.

    Refuses (ValueError) an empty tape or a `d` that is not the tape `v2` was
    run on — a mismatched pair would print ages and distances against the
    wrong bar without any visible fault. Pure: no IO, no wall clock, and
    neither argument is mutated."""
    macro = v2["macro"]
    n = len(d)
    if n == 0:
        raise ValueError("snapshot: empty tape")
    if n != macro["n_bars"]:
        raise ValueError(f"snapshot: tape has {n} bars but v2 was run on "
                         f"{macro['n_bars']} — not the same tape")
    h, l, c = (d["h"].to_numpy(float), d["l"].to_numpy(float),
               d["c"].to_numpy(float))
    ts = d["ts"].tolist()
    close = float(c[-1])
    atr_last = float(ind.atr(h, l, c, ATR_LEN)[-1])
    atr_ok = bool(np.isfinite(atr_last) and atr_last > 0.0)

    alive = [r for r in macro["ranges"] if r.state == "CONFIRMED"]
    r = alive[-1] if alive else None

    top = bottom = top0 = bottom0 = mid = None
    pos_pct = dist_atr = nearest_side = pending = None
    if r is not None:
        top, bottom = float(r.top), float(r.bottom)
        top0, bottom0 = float(r.top0), float(r.bottom0)
        mid = float(r.mid)
        width = top - bottom
        if width > 0.0:
            pos_pct = 100.0 * (close - bottom) / width
        d_top, d_bot = abs(top - close), abs(close - bottom)
        nearest_side = "top" if d_top <= d_bot else "bottom"
        if atr_ok:
            dist_atr = min(d_top, d_bot) / atr_last
        if r.pending is not None:
            open_i = int(r.pending["open_i"])
            pending = {"side": str(r.pending["side"]),
                       "open_ts": ts[open_i],
                       "bars_out": int(n - 1 - open_i),
                       "closes": int(r.pending["closes"])}

    lifecycle = [e for e in macro["events"] if e["event"] != "pivot"]
    last_event = None
    if lifecycle:
        e = lifecycle[-1]
        last_event = {"event": str(e["event"]), "ts": str(e["ts"]),
                      "age_bars": int(n - 1 - e["i"])}

    return {
        "state": str(v2["state"]),
        "has_range": r is not None,
        "top": top, "bottom": bottom, "top0": top0, "bottom0": bottom0,
        "mid": mid,
        "pos_pct": pos_pct,
        "atr": atr_last if np.isfinite(atr_last) else None,
        "dist_atr": dist_atr,
        "nearest_side": nearest_side,
        "pending": pending,
        "n_pending_open": int(macro["n_pending_open"]),
        "n_potential": int(macro["n_potential_unresolved"]),
        "last_event": last_event,
        "status_line": str(v2["status_line"]),
        "as_of": str(ts[-1]), "close": close, "n_bars": int(n),
    }
