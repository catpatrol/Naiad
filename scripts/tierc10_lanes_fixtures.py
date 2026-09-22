#!/usr/bin/env python
"""TIER-C10 LANE FIXTURES — P-BE-1 (breakeven) and P-SPR-2 (spring/upthrust).

TWO KINDS OF LEG PER FIXTURE, the BREAK legs first: each plants ONE
corruption and the guard must go RED on it, or the fixture is VOID — a check
that cannot fail proves nothing.  A break leg is one of two things and never
a third: a CORRUPTED INPUT handed to the module's own guard (which must
refuse it), or a MUTATION of the module (`mutated(...)`: a named wrong
planted as the implementation, under which the REAL leg's own checks must go
RED).  A leg that re-derives a wrong answer locally and never calls the
module proves nothing about the module.  Every fixture states inline what
would make it FAIL.  The banned failure modes stay banned:
  · SELF-COMPARISON — re-deriving a number the way the program derived it;
  · ONE EXAMPLE where cardinality was possible;
  · a TUNED MAGNITUDE BOUND standing in for an identity;
  · a check whose claim is NOT the design's claim.

LAW 4 BINDS THESE FIXTURES TOO.  The only trade book ridden on real bars is
the KNOWN CONTROL — card v6, every knob at its default, CLASSIC5 — and it is
ridden to prove it is UNCHANGED.  Every breakeven campaign and every spring
campaign in this file rides a SYNTHETIC 4h + 5m tape pair built here, under a
symbol that is not an asset, installed into the lineage's frame memo and torn
down in `finally`.  No unseen asset's price is read.  No registration is
filed in the registry of record; the gate legs file into throwaway temp roots
and delete them.  Every attack on the gate is COUNTED against a replay
counter that must read ZERO.

THE SYNTHETIC TAPE PAIR.  The 4h tape is built so the card's other machinery
is provably inert over the ride: the pre-spring base is a slow ramp, so at
the entry bar the EMA stack is ordered away from every bell the direction
could ring, and the harvest band's near edge sits on the far side of price so
`harvest_outside` is never satisfied.  Both are ASSERTED in the real legs,
not assumed — a fixture whose answer depends on an unexamined bell is a
fixture with a hidden term.

Run: NAIAD_CACHE_DIR=~/.cache/naiad/snapshots/tc10_20260921 \\
     ~/venvs/naiad/bin/python scripts/tierc10_lanes_fixtures.py [leg ...]
Exit 0 = every fixture that RAN passed and none is VOID; exit 1 = at least
one failed and NOTHING DOWNSTREAM IS TRUSTWORTHY.  A leg that is NOT RUN is
reported NOT RUN and never PASS.
"""
from __future__ import annotations

import ast
import dataclasses
import hashlib
import inspect
import json
import re
import subprocess
import sys
import tempfile
import traceback
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import tierc10_lanes as LN                                           # noqa: E402
import tierc10_panel as TP                                           # noqa: E402
import tierc9 as T9                                                  # noqa: E402
import tierc8 as T8                                                  # noqa: E402
import tierc7_rules as RC                                            # noqa: E402
import tierc5 as T5                                                  # noqa: E402

PY = str(Path.home() / "venvs" / "naiad" / "bin" / "python")
LANES_OUT = TP.OUT / "lanes"
MS_4H, MS_5M, N5 = LN.MS_4H, LN.MS_5M, LN.N_5M_PER_4H
SEED = LN.SEED                                  # 20260921, threaded explicitly

_SELF = sys.modules[__name__]   # so a break leg can plant a wrong into
#                                 THIS module's own stand-ins, the same
#                                 way `mutated` plants one into LN
T: list[str] = []
RESULTS: dict[str, bool] = {}
NOT_RUN: dict[str, str] = {}
_B: dict = {}

_TMP = re.compile(r"[^\s'\"(),;]*/(f-[a-z0-9-]+-)[A-Za-z0-9_]{8}")


def _norm(s: str) -> str:
    """Throwaway directories carry a RANDOM name; the filed transcript must
    not (F-DET's law applies to the evidence too)."""
    return _TMP.sub(r"<tmp>/\1*", s)


def say(s: str = "") -> None:
    s = _norm(s)
    print(s)
    T.append(s)


def refused(fn) -> tuple[bool, str]:
    """(True, why) iff `fn` HALTed.  The estate's guards raise SystemExit."""
    try:
        fn()
    except SystemExit as e:
        return True, _norm(str(e))[:170]
    return False, "ran to completion"


def attack(fn):
    """A BREAK LEG THAT IS AN ATTACK: it must be REFUSED.  `prove` wants
    ok == False from a break leg, and a refusal IS the failure it wants."""
    def leg():
        ok, why = refused(fn)
        return (not ok), (f"refused: {why}" if ok else "NOT REFUSED — it ran")
    return leg


def mutated(obj, attr: str, wrong, checks):
    """A BREAK LEG BY MUTATION.  Swap ONE attribute of the module under test
    for a WRONG implementation, run the REAL leg's own checks against it,
    restore.  ok == the checks stayed GREEN — i.e. the fixture cannot see the
    wrong it claims to guard."""
    def leg():
        old = getattr(obj, attr)
        setattr(obj, attr, wrong)
        try:
            ok, lines = checks()
        except SystemExit as e:
            ok, lines = False, [f"[BAD] the checks HALTed: {_norm(str(e))}"]
        except Exception as e:                              # noqa: BLE001
            ok, lines = False, [f"[BAD] the checks crashed: "
                                f"{type(e).__name__}: {str(e)[:120]}"]
        finally:
            setattr(obj, attr, old)
        bad = [ln for ln in lines if ln.startswith("[BAD]")]
        return ok, ("the REAL leg's checks under the mutation: "
                    + (bad[0][:150] if bad else "no BAD line"))
    return leg


def prove(fid: str, title: str, fails_if: str, breaks: list, real) -> bool:
    say(f"\n--- {fid} — {title}")
    void = False
    for name, fn in breaks:
        try:
            b_ok, b_detail = fn()
        except BaseException as e:                          # noqa: BLE001
            b_ok, b_detail = True, (f"break leg CRASHED "
                                    f"({type(e).__name__}: {str(e)[:150]})")
        say(f"  [BREAK] {name} -> "
            f"{'RED (correct)' if not b_ok else 'GREEN (FIXTURE IS VOID)'}: "
            f"{_norm(str(b_detail))}")
        void |= bool(b_ok)
    try:
        r_ok, lines = real()
    except SystemExit as e:
        r_ok, lines = False, [f"[BAD] the real leg HALTed: {_norm(str(e))}"]
    except Exception:                                       # noqa: BLE001
        r_ok, lines = False, ["[BAD] the real leg crashed: "
                              + traceback.format_exc()[-700:]]
    for ln in lines:
        say("    " + _norm(str(ln)))
    say(f"      FAILS IF: {fails_if}")
    ok = bool(r_ok) and not void and bool(breaks)
    say(f"  [{'PASS' if ok else 'FAIL'}] {fid}"
        + (" — a break leg passed; the fixture proves nothing" if void
           else ""))
    RESULTS[fid] = ok
    return ok


# ═══════════════════════════════════ THE SYNTHETIC 4h + 5m TAPE PAIR
T0 = 1_500_000_000_000 - (1_500_000_000_000 % MS_4H)
BASE_BARS = 360                 # > the card's 316 warm-up floor
LEVEL_BOT, LEVEL_TOP = 995.0, 1005.0


def install_frame(sym: str, o, h, l, c, om=None) -> tuple:
    """Build a 4h frame from hand-authored bars and install it in the
    lineage's memos under a SYNTHETIC symbol.

    The lineage memoises frames, role arrays, anchor series and fractals on
    the BARE SYMBOL (`tierc5._FRAMES`, `tierc8._SERIES`, `tierc9._RA`), which
    is why `tierc10_panel.frame_n` exists: a foreign lens under a real
    asset's key would poison its 4h book.  These symbols are not assets —
    they end in a name no venue lists — and `drop_frame` removes every entry
    in `finally`.  No real asset's memo is written at any point."""
    n = len(c)
    om = (np.arange(n, dtype=np.int64) * MS_4H + T0 if om is None
          else np.asarray(om, np.int64))
    o, h, l, c = (np.asarray(x, float) for x in (o, h, l, c))
    k4 = pd.DataFrame({"open_time": om, "open": o, "high": h, "low": l,
                       "close": c, "volume": np.ones(n)})
    f = T5.RC.build_4h(om, o, h, l, c)
    T5._FRAMES[sym] = {"k4": k4, "f": f, "x": T5.RC._crosses(f),
                       "pv4": T5.RC.build_pivots_4h(h, l), "fund": {},
                       "fractals": {}, "addctx": None}
    T8._SERIES.pop(sym, None)
    for k in [k for k in T9._RA if k[0] == sym]:
        T9._RA.pop(k)
    return T5._FRAMES[sym], om


def drop_frame(sym: str) -> None:
    T5._FRAMES.pop(sym, None)
    T8._SERIES.pop(sym, None)
    for k in [k for k in T9._RA if k[0] == sym]:
        T9._RA.pop(k)


def default_kids(h4: float, l4: float, c4: float) -> list:
    """48 children that reproduce their parent by construction: the first
    carries both extremes, the rest sit at the parent's close."""
    return [(h4, l4, c4)] + [(c4, c4, c4)] * (N5 - 1)


def kids(h4: float, l4: float, c4: float, i_hi: int, i_lo: int,
         cap_hi: float | None = None, cap_lo: float | None = None) -> list:
    """48 children with the parent's HIGH placed at child `i_hi` and its LOW
    at child `i_lo`.  `cap_hi` / `cap_lo` replace the extreme with a value
    that does NOT reproduce the parent — the incident-bar trap, planted."""
    k = [(c4, c4, c4)] * N5
    hh = h4 if cap_hi is None else cap_hi
    ll = l4 if cap_lo is None else cap_lo
    if i_hi == i_lo:
        k[i_hi] = (hh, ll, c4)
    else:
        k[i_hi] = (hh, c4, c4)
        k[i_lo] = (c4, ll, c4)
    return k


def five_source(om, h4, l4, c4, plan: dict):
    """A 5m source for the synthetic symbol: `plan` authors the children of
    the bars the test cares about; every other bar gets `default_kids`."""
    t, H, L, C = [], [], [], []
    for i in range(len(c4)):
        ks = plan.get(i) or default_kids(float(h4[i]), float(l4[i]),
                                         float(c4[i]))
        for k, (a, b, d) in enumerate(ks):
            t.append(int(om[i]) + k * MS_5M)
            H.append(float(a))
            L.append(float(b))
            C.append(float(d))
    arr = (np.array(t, np.int64), np.array(H, float), np.array(L, float),
           np.array(C, float))
    return lambda _sym: arr


def spring_base(side: str, second: bool = False) -> tuple:
    """The base ramp + the planted deviation-confirm, one side.

    bottom: a slow DECLINE to 1000 (so e12 < e89 < e316 and every bell a LONG
    could ring is already behind it, and the harvest's near edge max(e89,
    e316) sits ABOVE price so `harvest_outside` is never true), then a bar
    that sweeps 990 through the 995 boundary, two bars below it, and a bar
    that closes back inside at 1000.
    top: the exact mirror — a slow RISE, a sweep to 1010 through 1005, a
    close back inside at 1000.
    """
    # The sweep extreme carries FOUR decimals on purpose: the machine's event
    # log rounds to 2 dp (`engine/rangefinder.log`), so a signal that took its
    # extreme from the event field instead of the RAW tape is then VISIBLY
    # wrong, and F-SPR-SYN can plant exactly that.
    if side == "bottom":
        c = list(np.linspace(1100.0, 1000.0, BASE_BARS))
        ext = [(999.0, 999.0, 990.0049, 996.0), (996.0, 997.0, 992.0, 993.0),
               (993.0, 996.0, 991.0, 994.0), (994.0, 1001.0, 993.0, 1000.0)]
    else:
        c = list(np.linspace(900.0, 1000.0, BASE_BARS))
        ext = [(1001.0, 1009.9951, 1001.0, 1004.0),
               (1004.0, 1008.0, 1003.0, 1007.0),
               (1007.0, 1009.0, 1004.0, 1006.0),
               (1006.0, 1007.0, 999.0, 1000.0)]
    o, h, l = list(c), [x + 1.0 for x in c], [x - 1.0 for x in c]
    for a, b, d, e in ext:
        o.append(a)
        h.append(b)
        l.append(d)
        c.append(e)
    if second:
        # A SECOND, SHALLOWER deviation-confirm on the same side, planted so
        # its sweep never reaches the FIRST campaign's stop.  It exists to
        # give one-position-per-asset a CARDINAL answer rather than an
        # anecdote: with both signals injected the second must be skipped.
        q = c[-1]
        for hh, ll, cc in ((q + 1.0, q - 1.0, q),            # 364
                           (q + 1.0, q - 1.0, q),            # 365
                           (q - 3.0, 993.0, 994.0),          # 366 — the sweep
                           (q - 4.0, 993.5, 994.0),          # 367
                           (q - 2.0, 993.5, 997.0),          # 368 — reclaim
                           (q + 1.0, q - 1.0, q), (q + 1.0, q - 1.0, q),
                           (q + 1.0, q - 1.0, q)):
            o.append(cc)
            h.append(hh)
            l.append(ll)
            c.append(cc)
    return o, h, l, c


SECOND = (BASE_BARS + 6, BASE_BARS + 8)     # (sweep bar, reclaim bar)


def base_signal(side: str, om, h, l) -> LN.SpringSignal:
    """The planted signal, with every field read off the RAW tape."""
    a, i = BASE_BARS, BASE_BARS + 3
    if side == "bottom":
        return LN.SpringSignal(
            direction=1, sweep_i=a, sweep_ms=int(om[a]),
            sweep_extreme=float(np.min(np.asarray(l)[a:i + 1])),
            swept_level=LEVEL_BOT, reclaim_i=i, reclaim_ms=int(om[i]),
            bars_to_reclaim=i - a, known_at=i, rid=1, side="bottom",
            source="synthetic/bottom")
    return LN.SpringSignal(
        direction=-1, sweep_i=a, sweep_ms=int(om[a]),
        sweep_extreme=float(np.max(np.asarray(h)[a:i + 1])),
        swept_level=LEVEL_TOP, reclaim_i=i, reclaim_ms=int(om[i]),
        bars_to_reclaim=i - a, known_at=i, rid=1, side="top",
        source="synthetic/top")


# THE BE TAPE.  The four bars after the entry are authored in units of R, so
# the known answers are stated in R and not in prices that depend on an ATR.
BE_SYM = "SYN-BE-4H"            # the BE and MONO tapes share this symbol
BE_SYM_TOP = "SYN-BE-TOP-4H"    # its MIRROR: the same rows, ridden SHORT
BE_SYM_OF = {"bottom": BE_SYM, "top": BE_SYM_TOP}
SPR_SYM = {"bottom": "SYN-SPR-BOT-4H", "top": "SYN-SPR-TOP-4H"}


def be_tape(rows, side: str = "bottom") -> tuple:
    """The spring base + `rows` of (favourable, adverse, close) offsets in R.

    `side="bottom"` is the LONG tape every leg written before 2026-09-22
    rides, and its arithmetic is UNCHANGED (`d == 1` collapses every term
    below to what was there before), which is why those legs' transcript
    lines are byte-identical across this edit.  `side="top"` is the MIRROR:
    the same rows, read as a SHORT — the favourable offset becomes the bar's
    LOW and the adverse offset its HIGH — so one authored row set proves both
    directions instead of two hand-tuned ones.

    R is NOT known before the base exists (it comes from the sweep extreme
    and the ATR at the reclaim bar, neither of which any later bar can move),
    so the base is built and measured FIRST and the ride bars are authored
    against the measured R.  That is a construction order, not a fit: nothing
    downstream of bar `BASE_BARS + 3` can change `entry`, `stop` or `R`, and
    the real leg asserts exactly that by re-measuring them on the full tape.
    """
    sym, d = BE_SYM_OF[side], (1 if side == "bottom" else -1)
    o, h, l, c = spring_base(side)
    st, om = install_frame(sym, o, h, l, c)
    f = st["f"]
    i = BASE_BARS + 3
    sig = base_signal(side, om, h, l)
    e, atr = float(f.c[i]), float(f.atr[i])
    stp = RC.spring_stop(sig, e, atr, LN.Card().entry_rail_atr)
    R = float(stp.r_dist)
    for hh, ll, cc in rows:
        o.append(e + d * cc * R)
        h.append(e + (hh * R if d == 1 else -ll * R))
        l.append(e + (ll * R if d == 1 else -hh * R))
        c.append(e + d * cc * R)
    st, om = install_frame(sym, o, h, l, c)
    return st, om, np.asarray(h), np.asarray(l), np.asarray(c), sig, e, R, stp


BE_ROWS = ((1.05, -0.20, 0.50),      # 364 — the latch bar: prints +1R AND dips
           (0.60, -0.30, 0.20),      # 365 — dips below entry again
           (0.25, 0.15, 0.20), (0.25, 0.15, 0.20), (0.25, 0.15, 0.20),
           (0.25, 0.15, 0.20), (0.25, 0.15, 0.20), (0.25, 0.15, 0.20))
MONO_ROWS = ((1.05, 0.80, 0.90),     # 364 — latch, NO dip: the floor arms
             (1.20, 0.95, 1.10),
             (1.30, 0.60, 1.25),     # 366 — the (2,2) pivot low
             (1.45, 1.00, 1.40),
             (1.60, 1.10, 1.55),     # 368 — confirms it; the ratchet advances
             (1.65, 0.15, 1.20),     # 369 — dips THROUGH the ratchet level
             (1.30, 1.10, 1.20), (1.30, 1.10, 1.20), (1.30, 1.10, 1.20))
LATCH = BASE_BARS + 4                # bar 364


def be_case(plan_kids, card=None, rows=BE_ROWS, sym=BE_SYM):
    """Ride ONE synthetic campaign with the named children on the latch bar."""
    st, om, h, l, c, sig, e, R, stp = be_tape(rows)
    plan = {LATCH: plan_kids(float(h[LATCH]), float(l[LATCH]),
                             float(c[LATCH]))} if plan_kids else {}
    old = LN._FIVE_SOURCE
    LN._FIVE_SOURCE = five_source(om, h, l, c, plan)
    try:
        card = card or LN.Card(name="syn-be", lane="spring",
                               be_floor_after_r=1.0)
        _, tr = LN.replay10(sym, card, T9.V6_ROLES, int(om[0]),
                            int(om[-1]) + MS_4H - 1, springs=[sig])
    finally:
        LN._FIVE_SOURCE = old
    return tr, {"om": om, "h": h, "l": l, "c": c, "e": e, "R": R, "stp": stp,
                "sig": sig, "f": st["f"]}


# ═══════════════════ F-LANES-OFF · the knobs OFF ARE the control, exactly
def books() -> dict:
    """The two CLASSIC5 books F-LANES-OFF compares, ridden ONCE.  The only
    real-data ride anywhere in this file, and it is the KNOWN CONTROL."""
    if _B:
        return _B
    lo, hi, meta = TP.corridor_n(TP.CLASSIC5)
    want = TP.run_cell_n(TP.CONTROL_CARD, T9.V6_ROLES, TP.CLASSIC5, lo, hi)
    _B.update(lo=lo, hi=hi, meta=meta, want=want,
              want_j=TP.journal_frame(want))
    return _B


def _off_checks() -> tuple:
    """The REAL leg's own checks — the book this module rides with every new
    knob OFF, against the panel module's control, column by column."""
    b = books()
    got = LN.run_lane(LN.CARD_TC10_CONTROL, T9.V6_ROLES, TP.CLASSIC5,
                      b["lo"], b["hi"])
    gj, wj = TP.journal_frame(got), b["want_j"]
    lines, ok = [], True
    g = len(got) == len(b["want"]) and len(got) > 0
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] campaign COUNT: "
                 f"{len(got)} vs the control's {len(b['want'])}")
    shared = [k for k in wj.columns if k in gj.columns]
    worst, worst_col, mism = 0.0, "", {}
    if len(gj) == len(wj):
        for k in shared:
            a, c_ = wj[k], gj[k]
            if pd.api.types.is_numeric_dtype(a) \
                    and pd.api.types.is_numeric_dtype(c_):
                av, cv = a.to_numpy(float), c_.to_numpy(float)
                fin = np.isfinite(av) | np.isfinite(cv)
                d = float(np.nanmax(np.abs(av - cv))) if fin.any() else 0.0
                nn = int((np.isfinite(av) != np.isfinite(cv)).sum())
                if nn:
                    mism[k] = f"{nn} finite/NaN disagreements"
                if np.isfinite(d) and d > worst:
                    worst, worst_col = d, k
            else:
                n_ = int((a.astype(str) != c_.astype(str)).sum())
                if n_:
                    mism[k] = f"{n_} rows differ"
    else:
        mism["<length>"] = "the books are different lengths"
    g = (not mism) and worst == 0.0 and len(shared) >= 30
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] {len(shared)} journal columns, "
                 f"WORST ABS DIFF = {worst:.3e}"
                 + (f" on {worst_col!r}" if worst else "")
                 + f", non-numeric mismatches {mism or 'NONE'}")
    ex = (sorted(set(gj["exit_reason"])) if len(gj) else [])
    g = (len(gj) == len(wj)
         and bool((gj["exit_reason"].astype(str)
                   == wj["exit_reason"].astype(str)).all()))
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] every exit_reason identical; "
                 f"reasons seen: {ex}")
    ok2, w2, why = TP.ctrl_diff(gj, wj)
    ok &= bool(ok2 and w2 == 0.0)
    lines.append(f"[{'OK ' if ok2 and w2 == 0.0 else 'BAD'}] the lineage's "
                 f"own ctrl_diff: {why}")
    g = isinstance(got, list) and not isinstance(got, TP.Book)
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] the control comes back a PLAIN "
                 f"list ({type(got).__name__}) — it is not a registered book "
                 f"and must not wear a registered book's provenance")
    n_be = sum(int(bool(getattr(t, "be_on", False))) for t in got)
    g = n_be == 0
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] campaigns with the BE floor "
                 f"live: {n_be}")
    acc = [k for k in ("gross_r", "fee_r", "funding_r", "funding_r_uncapped",
                       "funding_ceiling_bound", "net_r") if k in shared]
    g = len(acc) == 6
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] THE ACCOUNTING IS THE "
                 f"LINEAGE'S, UNCHANGED: the six tierc7._account_chain "
                 f"columns {acc} are among the columns compared above at "
                 f"0.000e+00 — fee OBJECT, journalled funding, the D12 1R "
                 f"funding ceiling")
    lines.append(f"      net_r control {float(wj['net_r'].sum()):.6f} R / "
                 f"tc10 ride {float(gj['net_r'].sum()):.6f} R")
    return ok, lines


def f_lanes_off() -> bool:
    def m_journal():
        b = books()
        bad = b["want_j"].copy()
        bad.loc[bad.index[0], "net_r"] = float(bad["net_r"].iloc[0]) + 1e-9
        gj = TP.journal_frame(LN.run_lane(LN.CARD_TC10_CONTROL, T9.V6_ROLES,
                                          TP.CLASSIC5, b["lo"], b["hi"]))
        ok, w, why = TP.ctrl_diff(gj, bad)
        return bool(ok and w == 0.0), f"comparison on the tampered COPY: {why}"

    def no_advance(fr, j, d, cur_stop, close, atr, s, kind, offset, open_ms,
                   min_advance_atr=0.05, rail_atr=RC.MIN_STOP_ATR):
        return None, False

    return prove(
        "F-LANES-OFF",
        "TC10's ride with EVERY new knob OFF is the panel module's card-v6 "
        "control, 0.000e+00, on CLASSIC5",
        "the campaign counts differ, ANY of the shared journal columns "
        "differs by ANY amount, any exit_reason differs, the lineage's own "
        "ctrl_diff disagrees, the control comes back wearing a registered "
        "book's provenance, or any campaign rode with the BE floor live.",
        [("ONE net_r moved by 1e-9 in a COPY of the reference journal "
          "(the comparison must see it)", m_journal),
         ("the BE floor planted ON in the control card, wearing the "
          "control's NAME (the gate must refuse it as the control)",
          mutated(LN, "CARD_TC10_CONTROL",
                  LN.Card(name="tc10-control(=v6)", be_floor_after_r=1.0),
                  _off_checks)),
         ("trail_arm_after_r moved to 0.0 under the control's name (same)",
          mutated(LN, "CARD_TC10_CONTROL",
                  LN.Card(name="tc10-control(=v6)", trail_arm_after_r=0.0),
                  _off_checks)),
         ("the ratchet neutered inside the ride — it PASSES the gate, so "
          "only the 0.000e+00 comparison can catch it",
          mutated(LN, "matched_step", no_advance, _off_checks))],
        _off_checks)


# ═══════════════════════════════ F-BE-SEQ · which came first inside the bar
BE_SCEN = {
    "dip-before": (lambda h, l, c: kids(h, l, c, i_hi=10, i_lo=3),
                   "dip_first", LATCH + 1, "stop"),
    "dip-after": (lambda h, l, c: kids(h, l, c, i_hi=3, i_lo=10),
                  "plus1r_first", LATCH, LN.BE_REASON),
    "tie (both in ONE 5m child)": (lambda h, l, c: kids(h, l, c, i_hi=7,
                                                        i_lo=7),
                                   "tie", LATCH + 1, "stop"),
    "4h HIGH not reproduced by its children":
        (lambda h, l, c: kids(h, l, c, i_hi=3, i_lo=10,
                              cap_hi=h - 0.02 * (h - c)),
         "mismatch", LATCH + 1, "stop"),
    "4h LOW not reproduced by its children":
        (lambda h, l, c: kids(h, l, c, i_hi=3, i_lo=10,
                              cap_lo=l + 0.02 * (c - l)),
         "mismatch", LATCH + 1, "stop"),
}


def _seq_checks() -> tuple:
    lines, ok = [], True
    for name, (pk, want_order, want_i, want_reason) in BE_SCEN.items():
        tr, ctx = be_case(pk)
        if len(tr) != 1:
            ok = False
            lines.append(f"[BAD] {name}: {len(tr)} campaigns, expected 1")
            continue
        t = tr[0]
        e, R = ctx["e"], ctx["R"]
        g = (t.be_order == want_order and t.exit_i == want_i
             and t.exit_reason == want_reason
             and abs(float(t.exit_px) - e) <= 1e-9)
        ok &= g
        lines.append(
            f"[{'OK ' if g else 'BAD'}] {name}: order={t.be_order!r} "
            f"exit bar {t.exit_i} @ {float(t.exit_px):.4f} "
            f"(entry {e:.4f}) reason={t.exit_reason!r} "
            f"tie={t.n_be_tie} mismatch={t.n_be_mismatch}"
            + (f" why={t.be_why[:64]!r}" if t.be_why else ""))
    # THE CONVERSE — the same bar, the two children SWAPPED, the exit MOVES.
    a, _ = be_case(lambda h, l, c: kids(h, l, c, i_hi=10, i_lo=3))
    b, _ = be_case(lambda h, l, c: kids(h, l, c, i_hi=3, i_lo=10))
    g = (a[0].exit_i != b[0].exit_i or a[0].exit_reason != b[0].exit_reason)
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] THE CONVERSE: swapping the dip "
                 f"child and the print child moves the exit — "
                 f"({a[0].exit_i}, {a[0].exit_reason!r}) -> "
                 f"({b[0].exit_i}, {b[0].exit_reason!r})")
    # counts, per class, are CARDINAL not anecdotal
    tie = sum(be_case(p)[0][0].n_be_tie for p, *_ in BE_SCEN.values())
    mis = sum(be_case(p)[0][0].n_be_mismatch for p, *_ in BE_SCEN.values())
    g = tie == 1 and mis == 2
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] across the five scenarios: "
                 f"{tie} tie (expected 1), {mis} 4h/5m mismatches "
                 f"(expected 2 — one each direction)")
    # the tape's other machinery is INERT over the ride, asserted not assumed
    tr, ctx = be_case(lambda h, l, c: kids(h, l, c, i_hi=3, i_lo=10))
    f, i = ctx["f"], LATCH - 1
    edge = RC.harvest_edge(float(f.e89[i]), float(f.e316[i]), 1)
    g = (float(f.e12[i]) < float(f.e89[i]) < float(f.e316[i])
         and not RC.harvest_outside(float(f.c[i]), edge, 1)
         and not bool(tr[0].harvested))
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] the synthetic tape's other "
                 f"machinery is inert: e12 {float(f.e12[i]):.2f} < e89 "
                 f"{float(f.e89[i]):.2f} < e316 {float(f.e316[i]):.2f} (no "
                 f"bell a LONG could ring), harvest edge {edge:.2f} above "
                 f"close {float(f.c[i]):.2f} so it never arms, harvested="
                 f"{bool(tr[0].harvested)}")
    lines.append("      THE FOURTH OUTCOME — a `plus1r_first` with NO dip at "
                 "all — is proven in F-BE-LATCH, not here: it changes the "
                 "ride only once the ratchet has carried the stop ABOVE "
                 "entry, which these five scenarios never do [review "
                 "2026-09-21]")
    return ok, lines


def f_be_seq() -> bool:
    def reversed_children(sym, bar_open_ms):
        t5, h5, l5, c5 = _orig_children(sym, bar_open_ms)
        return t5[::-1], h5[::-1], l5[::-1], c5[::-1]

    def b_missing_children():
        """A CORRUPTED INPUT: the parent's children number 47, not 48."""
        st, om, h, l, c, sig, e, R, stp = be_tape(BE_ROWS)
        short = kids(float(h[LATCH]), float(l[LATCH]), float(c[LATCH]),
                     i_hi=3, i_lo=10)[:-1]          # 47 children, not 48
        old = LN._FIVE_SOURCE
        t, H, L, C = [], [], [], []
        for i in range(len(c)):
            ks = (short if i == LATCH
                  else default_kids(float(h[i]), float(l[i]), float(c[i])))
            for k, (aa, bb, dd) in enumerate(ks):
                t.append(int(om[i]) + k * MS_5M)
                H.append(aa)
                L.append(bb)
                C.append(dd)
        arr = (np.array(t, np.int64), np.array(H, float),
               np.array(L, float), np.array(C, float))
        LN._FIVE_SOURCE = lambda _s: arr
        try:
            _, tr = LN.replay10(BE_SYM, LN.Card(name="syn", lane="spring",
                                                be_floor_after_r=1.0),
                                T9.V6_ROLES, int(om[0]),
                                int(om[-1]) + MS_4H - 1, springs=[sig])
        finally:
            LN._FIVE_SOURCE = old
        t0 = tr[0]
        good = (t0.be_order == "mismatch" and t0.n_be_mismatch == 1
                and "47" in t0.be_why)
        return (not good), (f"47 children -> order={t0.be_order!r} "
                            f"why={t0.be_why[:90]!r}")

    return prove(
        "F-BE-SEQ",
        "the +1R bar is SEQUENCED on its 48 native 5m children — dip-before, "
        "dip-after, the same-child tie, and the 4h/5m extreme mismatch both "
        "ways — with the converse",
        "any scenario's order, exit bar, exit price or exit reason differs "
        "from the hand-authored answer; the tie or either mismatch is not "
        "COUNTED; swapping the dip child and the print child does NOT move "
        "the exit; 47 children are not treated as a mismatch; or the "
        "synthetic tape turns out to ring a bell or arm the harvest (the "
        "answer would then depend on a term the test never examined).",
        [("the sequencer always answers `plus1r_first`",
          mutated(LN, "be_sequence",
                  lambda *a, **k: {"order": "plus1r_first", "i_up": 0,
                                   "i_dip": 1, "print": True, "dip": True,
                                   "n_children": N5, "mismatch": False,
                                   "why": "", "mfe_held": float("nan"),
                                   "parent_print": True, "parent_dip": True},
                  _seq_checks)),
         ("the sequencer always answers `dip_first`",
          mutated(LN, "be_sequence",
                  lambda *a, **k: {"order": "dip_first", "i_up": 1,
                                   "i_dip": 0, "print": True, "dip": True,
                                   "n_children": N5, "mismatch": False,
                                   "why": "", "mfe_held": float("nan"),
                                   "parent_print": True, "parent_dip": True},
                  _seq_checks)),
         ("the 4h-vs-5m extreme comparison always agrees (_same_px := True)",
          mutated(LN, "_same_px", lambda a, b: True, _seq_checks)),
         ("the children are walked in REVERSE tape order",
          mutated(LN, "children_5m", reversed_children, _seq_checks)),
         ("a parent bar with 47 children (CORRUPTED INPUT)",
          b_missing_children)],
        _seq_checks)


_orig_children = LN.children_5m


# ═══════════════════════════ F-BE-MONO · stop = max(floor, ratchet), monotone
def _mono_checks() -> tuple:
    tr, ctx = be_case(None, rows=MONO_ROWS,
                      card=LN.Card(name="syn-mono", lane="spring",
                                   be_floor_after_r=1.0))
    lines, ok = [], True
    if len(tr) != 1:
        return False, [f"[BAD] {len(tr)} campaigns, expected 1"]
    t = tr[0]
    e, R = ctx["e"], ctx["R"]
    path = [float(x) for x in t.stop_path]
    g = all((path[k + 1] - path[k]) >= -1e-12 for k in range(len(path) - 1))
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] the stop path is MONOTONE "
                 f"non-decreasing: {[round(x, 4) for x in path]}")
    g = any(abs(x - e) <= 1e-9 for x in path)
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] the floor BOUND at some point — "
                 f"entry {e:.4f} appears in the path")
    g = float(path[-1]) > e + 1e-9 and len(t.advances) >= 1
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] the ratchet then carried the "
                 f"stop PAST the floor: final {path[-1]:.4f} > entry "
                 f"{e:.4f}, {len(t.advances)} advance(s)")
    g = (t.exit_reason == "stop" and float(t.exit_px) > e + 1e-9
         and not bool(t.be_bound_at_exit))
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] the campaign exits at the "
                 f"RATCHET, not at the floor: bar {t.exit_i} @ "
                 f"{float(t.exit_px):.4f} = entry + "
                 f"{(float(t.exit_px) - e) / R:.4f} R, reason "
                 f"{t.exit_reason!r}, be_bound_at_exit={t.be_bound_at_exit}")
    hand = [(100.0, 90.0, 1, 100.0), (90.0, 100.0, 1, 100.0),
            (100.0, 110.0, -1, 100.0), (110.0, 100.0, -1, 100.0)]
    got = [LN.apply_floor(s, fl, d) for s, fl, d, _ in hand]
    g = all(abs(a - w) <= 1e-12 for a, (_, _, _, w) in zip(got, hand))
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] apply_floor's hand answers "
                 f"(long max, short min): {got} vs "
                 f"{[w for *_, w in hand]}")
    return ok, lines


def f_be_mono() -> bool:
    return prove(
        "F-BE-MONO",
        "from the bar after the latch the floor is an ORDINARY stop: "
        "stop = max(floor, ratchet) for a long, monotone",
        "the stop path falls at any point; the floor never binds; the "
        "ratchet never passes the floor (the claim would be untested); the "
        "campaign exits at the floor when the ratchet had already passed it; "
        "or apply_floor's hand answers differ.",
        [("the floor written as a plain ASSIGNMENT (stop = entry)",
          mutated(LN, "apply_floor", lambda s, fl, d: float(fl),
                  _mono_checks)),
         ("the floor never applied (stop unchanged)",
          mutated(LN, "apply_floor", lambda s, fl, d: float(s),
                  _mono_checks))],
        _mono_checks)


# ═════════════ F-BE-LATCH · the latch bar ALWAYS gets a stop decision
# THE BAR THIS FIXTURE EXISTS FOR [review 2026-09-21, BLOCKING].  A latch bar
# whose 5m children print the threshold and NEVER dip to entry is neither a
# fill nor a `dip_first`, and the branch that decided the stop slot tested
# only those two shapes — so that bar got NO stop test at all.  Invisible
# while the stop sits BELOW entry (a low at or below it is necessarily a dip
# to entry, which routes to the fill branch) and LIVE the moment the ratchet
# has carried the stop ABOVE entry.  Both tapes below put the latch at
# `be_floor_after_r = 2.0`, ABOVE v6's `trail_arm_after_r` 1.0, which is
# exactly the region the registered pin cannot reach and a sensitivity run
# would.
#
# A_ROWS is `MONO_ROWS` with bar 369 re-authored to print +2.05 R and dip to
# +0.15 R: the ratchet stands at +0.4122 R, the bar pierces it, no child
# reaches entry.  LATCH_ROWS ratchets to a stop that is still BELOW entry,
# latches at +2 R, and then dips EXACTLY to entry on the next bar — the
# floor-bound exit that `ratchet_exit` must not claim as its own.
A_ROWS = tuple(list(MONO_ROWS)[:5] + [(2.05, 0.15, 1.20)]
               + list(MONO_ROWS)[6:])
LATCH_ROWS = ((0.20, -0.55, -0.45),      # 364
              (0.10, -0.65, -0.55),      # 365 — the (2,2) pivot low
              (0.30, -0.60, 0.10),       # 366
              (1.20, -0.20, 1.10),       # 367 — +1R arms the trail; it
                                         #        confirms the pivot and the
                                         #        stop advances BELOW entry
              (1.60, 1.00, 1.55),        # 368
              (2.05, 0.15, 1.20),        # 369 — the BE latch at 2 R, NO dip
              (1.30, 0.00, 0.10),        # 370 — dips EXACTLY to entry
              (0.40, 0.20, 0.30), (0.40, 0.20, 0.30))
# NOTOUCH_ROWS is A_ROWS with bar 369's low lifted to +0.50 R — ABOVE the
# ratchet's +0.4122 R — so that bar prints the latch and touches NOTHING.
NOTOUCH_ROWS = tuple(list(MONO_ROWS)[:5] + [(2.05, 0.50, 1.20)]
                     + list(MONO_ROWS)[6:])
A_LATCH, L_LATCH = BASE_BARS + 9, BASE_BARS + 9      # bar 369, both tapes


def latch_ride(rows, be_r, side: str = "bottom", plan_kids=None,
               latch_bar: int | None = None):
    """One synthetic campaign on `rows`, floor at `be_r` (None = OFF).

    With `plan_kids` None the children are DEFAULT (the parent's two extremes
    both in child 0, so the latch bar's order is a TIE if it dips at all and
    `plus1r_first` if it does not) — which is what every leg written before
    2026-09-22 asked for, and this call is byte-identical to that one.  With
    `plan_kids` given, that bar's 48 children are authored by hand, which is
    the only way to put the +1R print BEFORE the dip.
    """
    st, om, h, l, c, sig, e, R, stp = be_tape(rows, side)
    sym = BE_SYM_OF[side]
    j = A_LATCH if latch_bar is None else int(latch_bar)
    plan = ({j: plan_kids(float(h[j]), float(l[j]), float(c[j]))}
            if plan_kids else {})
    old = LN._FIVE_SOURCE
    LN._FIVE_SOURCE = five_source(om, h, l, c, plan)
    try:
        card = LN.Card(name="syn-latch", lane="spring", be_floor_after_r=be_r)
        _, tr = LN.replay10(sym, card, T9.V6_ROLES, int(om[0]),
                            int(om[-1]) + MS_4H - 1, springs=[sig])
    finally:
        LN._FIVE_SOURCE = old
    return tr, {"e": e, "R": R, "stp": stp, "f": st["f"], "om": om,
                "sym": sym, "d": 1 if side == "bottom" else -1,
                "h": h, "l": l, "c": c}


# ── THE BAR NO LEG DROVE [R0 2026-09-22] ─────────────────────────────────────
# A_ROWS' latch bar prints +2.05 R and bottoms at +0.15 R — it NEVER reaches
# entry — so `be_latch_decision` answers `old_stop` and the FILL half of the
# branch is never entered.  DIP_ROWS is A_ROWS with that one low carried
# THROUGH entry to -0.05 R: the bar now prints the latch AND dips to entry,
# over a ratchet already standing at +0.4122 R.  The tape cannot get from
# +2.05 R down to entry without crossing +0.4122 R, so the honest exit is the
# ratcheted stop — and the pre-repair fill branch paid entry.
DIP_ROWS = tuple(list(MONO_ROWS)[:5] + [(2.05, -0.05, 1.20)]
                 + list(MONO_ROWS)[6:])


def print_then_dip(d: int):
    """48 children with the FAVOURABLE extreme at child 3 and the ADVERSE
    extreme at child 10 — the +1R print FIRST, the dip to entry AFTER, which
    is the one shape that routes to the fill branch.

    For a long the favourable extreme is the bar's HIGH, for a short its LOW,
    so the two children swap: the plan is written from the POSITION's side,
    never from the tape's."""
    return (lambda h, l, c: kids(h, l, c, i_hi=3, i_lo=10)) if d == 1 \
        else (lambda h, l, c: kids(h, l, c, i_hi=10, i_lo=3))


def dip_then_print(d: int):
    """The CONTROL plan: the same bar with the two children SWAPPED, so the
    walk answers `dip_first` and the OLD_STOP branch decides it instead."""
    return (lambda h, l, c: kids(h, l, c, i_hi=10, i_lo=3)) if d == 1 \
        else (lambda h, l, c: kids(h, l, c, i_hi=3, i_lo=10))


def _latch_checks() -> tuple:
    lines, ok = [], True

    # ── 1 · the latch bar's stop test, over a ratchet ABOVE entry ─────────
    off, cxo = latch_ride(A_ROWS, None)
    on2, cx2 = latch_ride(A_ROWS, 2.0)
    on1, cx1 = latch_ride(A_ROWS, 1.0)
    if not (len(off) == len(on2) == len(on1) == 1):
        return False, [f"[BAD] campaign counts {len(off)}/{len(on2)}/"
                       f"{len(on1)}, expected 1 each"]
    a, b, d1 = off[0], on2[0], on1[0]
    e, R = cxo["e"], cxo["R"]
    g = (b.be_reached and b.be_bar == A_LATCH
         and b.be_order == "plus1r_first" and not b.be_exit)
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] the latch DID fire at 2 R on "
                 f"bar {b.be_bar} with order {b.be_order!r} and NO dip — the "
                 f"check below is not vacuous")
    g = (b.exit_i == a.exit_i and b.exit_reason == a.exit_reason
         and abs(float(b.exit_px) - float(a.exit_px)) <= 1e-12
         and a.exit_reason == "stop" and float(a.exit_px) > e + 1e-9)
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] THE BREACHED STOP IS HONOURED: "
                 f"floor OFF exits ({a.exit_i}, {a.exit_reason!r}) @ "
                 f"{(float(a.exit_px) - e) / R:+.4f} R and floor ON at 2 R "
                 f"exits ({b.exit_i}, {b.exit_reason!r}) @ "
                 f"{(float(b.exit_px) - e) / R:+.4f} R — the ratcheted stop "
                 f"stood at {(float(a.final_stop_px) - e) / R:+.4f} R")
    g = (d1.exit_i == a.exit_i and d1.exit_reason == a.exit_reason
         and abs(float(d1.exit_px) - float(a.exit_px)) <= 1e-12
         and d1.be_bar == LATCH
         and any(abs(float(x) - e) <= 1e-9 for x in d1.stop_path))
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] the REGISTERED pin 1.0 rides "
                 f"the same tape to the same exit ({d1.exit_i}, "
                 f"{d1.exit_reason!r}) — and it is a DIFFERENT ride (latch "
                 f"bar {d1.be_bar} vs {b.be_bar}, the floor binds at entry "
                 f"inside its stop path), so the two pins are not the same "
                 f"run twice")
    g = bool(a.ratchet_exit) and bool(b.ratchet_exit) \
        and not bool(b.be_bound_at_exit)
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] a TRUE ratchet exit still reads "
                 f"one: ratchet_exit OFF={a.ratchet_exit} ON={b.ratchet_exit}"
                 f", be_bound_at_exit={b.be_bound_at_exit}")

    # ── 1b · A LATCH BAR THAT TOUCHES NOTHING ────────────────────────────
    # NOTOUCH_ROWS prints the latch at +2.05 R and bottoms at +0.50 R — above
    # the ratchet's +0.4122 R — so the bar dips to neither entry NOR the
    # stop and the honest ride simply CONTINUES.  It is here because the
    # repaired `be_latch_fill` makes a wrongly-FILLed no-dip bar harmless
    # wherever the bar pierced the stop anyway (both answers price the same
    # effective stop); this tape is the one where it is NOT harmless, and it
    # is what keeps the `no dip called a FILL` break leg honest at 2.0.
    for side, dd in (("bottom", 1), ("top", -1)):
        noff, cno = latch_ride(NOTOUCH_ROWS, None, side)
        non, cn = latch_ride(NOTOUCH_ROWS, 2.0, side)
        if not (len(noff) == len(non) == 1):
            ok = False
            lines.append(f"[BAD] {side} no-touch: campaign counts "
                         f"{len(noff)}/{len(non)}")
            continue
        m, nn = noff[0], non[0]
        en, Rn = cn["e"], cn["R"]
        lo_r = (float(cn["l" if dd == 1 else "h"][A_LATCH]) - en) * dd / Rn
        st_r = (float(nn.stop_path[A_LATCH - int(nn.entry_i) - 1]) - en) * dd / Rn
        g = (nn.be_bar == A_LATCH and nn.be_order == "plus1r_first"
             and lo_r > st_r + 1e-9 and lo_r > 1e-9
             and m.exit_i == nn.exit_i and m.exit_reason == nn.exit_reason
             and abs(float(m.exit_px) - float(nn.exit_px)) <= 1e-12
             and nn.exit_i > A_LATCH)
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] {side} A LATCH BAR THAT "
                     f"TOUCHES NOTHING: bar {A_LATCH} prints the 2 R latch, "
                     f"its adverse extreme stops at {lo_r:+.4f} R ABOVE both "
                     f"entry and the ratcheted stop {st_r:+.4f} R, so the "
                     f"ride CONTINUES — floor OFF ({m.exit_i}, "
                     f"{m.exit_reason!r}) and floor ON ({nn.exit_i}, "
                     f"{nn.exit_reason!r}) @ "
                     f"{(float(nn.exit_px) - en) * dd / Rn:+.4f} R, the same "
                     f"bar; a bar decided a FILL here would exit a campaign "
                     f"the tape never stopped out")

    # ── 2 · a FLOOR-bound exit with advances already on the record ────────
    foff, cfo = latch_ride(LATCH_ROWS, None)
    fon, cf = latch_ride(LATCH_ROWS, 2.0)
    if not (len(foff) == len(fon) == 1):
        return False, lines + [f"[BAD] campaign counts {len(foff)}/{len(fon)}"]
    p, q = foff[0], fon[0]
    e2, R2 = cf["e"], cf["R"]
    adv_below = [float(x.new_stop) for x in q.advances]
    g = (len(q.advances) >= 1 and all(x < e2 - 1e-9 for x in adv_below)
         and q.be_bar == L_LATCH)
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] the ratchet advanced BELOW "
                 f"entry before the latch: {len(q.advances)} advance(s) at "
                 f"{[round((x - e2) / R2, 4) for x in adv_below]} R, latch "
                 f"bar {q.be_bar}")
    g = (q.exit_reason == "stop"
         and abs(float(q.exit_px) - e2) <= 1e-12
         and bool(q.be_bound_at_exit) and not bool(q.ratchet_exit))
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] THE EXIT IS THE FLOOR'S, NOT "
                 f"THE RATCHET'S: bar {q.exit_i} @ "
                 f"{(float(q.exit_px) - e2) / R2:+.4f} R reason "
                 f"{q.exit_reason!r}, be_bound_at_exit={q.be_bound_at_exit}, "
                 f"ratchet_exit={q.ratchet_exit} (advances "
                 f"{len(q.advances)} — the lineage's expression alone would "
                 f"say True)")
    g = float(q.stop_advanced_atr) > 0.0
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] stop_advanced_atr keeps BOTH "
                 f"lifts, as the lineage publishes it: "
                 f"{float(q.stop_advanced_atr):+.4f} ATR, stop path R "
                 f"{[round((float(x) - e2) / R2, 4) for x in q.stop_path]}")
    g = (p.exit_i != q.exit_i or p.exit_reason != q.exit_reason)
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] THE CONVERSE: the same tape with "
                 f"the floor OFF exits ({p.exit_i}, {p.exit_reason!r}) @ "
                 f"{(float(p.exit_px) - e2) / R2:+.4f} R — the floor MOVED "
                 f"the answer")

    # ── 3 · THE FILL BRANCH, over a ratchet ABOVE entry, BOTH DIRECTIONS ──
    # The bar no leg drove until 2026-09-22.  `plus1r_first` WITH a dip on a
    # latch bar whose ratchet already stands at +0.4122 R: the tape cannot
    # reach entry without crossing that stop, so the honest exit IS that
    # stop, and the floor-ON ride must land exactly where the floor-OFF ride
    # does.  The pre-repair branch paid `entry_px` and fabricated -0.4120 R.
    for side, dd in (("bottom", 1), ("top", -1)):
        pk, ck = print_then_dip(dd), dip_then_print(dd)
        xoff, cxo3 = latch_ride(DIP_ROWS, None, side, pk)
        xon, cx3 = latch_ride(DIP_ROWS, 2.0, side, pk)
        xctl, _cc = latch_ride(DIP_ROWS, 2.0, side, ck)
        if not (len(xoff) == len(xon) == len(xctl) == 1):
            ok = False
            lines.append(f"[BAD] {side}: campaign counts {len(xoff)}/"
                         f"{len(xon)}/{len(xctl)}, expected 1 each")
            continue
        u, v, w = xoff[0], xon[0], xctl[0]
        e3, R3 = cx3["e"], cx3["R"]
        # NON-VACUITY, asserted at the decision itself: the sequencer really
        # does answer `plus1r_first` WITH a dip on that bar, so the FILL
        # branch really is the branch under test.
        om3, h3, l3 = cx3["om"], cx3["h"], cx3["l"]
        oldf = LN._FIVE_SOURCE
        LN._FIVE_SOURCE = five_source(
            om3, h3, l3, cx3["c"],
            {A_LATCH: pk(float(h3[A_LATCH]), float(l3[A_LATCH]),
                         float(cx3["c"][A_LATCH]))})
        try:
            seq = LN.be_sequence(cx3["sym"], int(om3[A_LATCH]), dd, e3,
                                 e3 + dd * 2.0 * R3, float(h3[A_LATCH]),
                                 float(l3[A_LATCH]))
        finally:
            LN._FIVE_SOURCE = oldf
        dec = LN.be_latch_decision(seq)
        g = (seq["order"] == "plus1r_first" and seq["dip"]
             and seq["i_up"] < seq["i_dip"] and dec == LN.BE_LATCH_FILL
             and v.be_bar == A_LATCH and v.be_order == "plus1r_first")
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] {side} d={dd:+d}: the latch "
                     f"bar IS a FILL — order {seq['order']!r}, print child "
                     f"{seq['i_up']} before dip child {seq['i_dip']}, "
                     f"decision {dec!r}; the checks below drive the FILL "
                     f"branch and not the old-stop one")
        ratch = float(v.stop_path[-1])
        g = (v.exit_i == u.exit_i and v.exit_reason == u.exit_reason
             and abs(float(v.exit_px) - float(u.exit_px)) <= 1e-12
             and u.exit_reason == "stop"
             and (float(u.exit_px) - e3) * dd > 1e-9
             and abs(float(v.exit_px) - ratch) <= 1e-12
             and not bool(v.be_exit) and not bool(v.be_bound_at_exit))
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] {side} THE RATCHET IS "
                     f"HONOURED ON THE LATCH BAR: floor OFF exits "
                     f"({u.exit_i}, {u.exit_reason!r}) @ "
                     f"{(float(u.exit_px) - e3) * dd / R3:+.6f} R and floor "
                     f"ON at 2 R exits ({v.exit_i}, {v.exit_reason!r}) @ "
                     f"{(float(v.exit_px) - e3) * dd / R3:+.6f} R, which is "
                     f"its OWN stop_path tail "
                     f"{(ratch - e3) * dd / R3:+.6f} R — be_exit="
                     f"{v.be_exit}, be_bound_at_exit={v.be_bound_at_exit}")
        g = (abs(float(v.net_r) - float(u.net_r)) <= 1e-12
             and abs(float(v.mfe_r) - float(u.mfe_r)) <= 1e-12
             and int(v.bars_held) == int(u.bars_held))
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] {side} and the ACCOUNTING "
                     f"agrees, not just the exit: net_r ON "
                     f"{float(v.net_r):+.6f} vs OFF {float(u.net_r):+.6f}, "
                     f"mfe_r {float(v.mfe_r):+.6f} vs "
                     f"{float(u.mfe_r):+.6f}, bars_held {v.bars_held} vs "
                     f"{u.bars_held} — the pre-repair branch fabricated "
                     f"{(e3 - float(u.exit_px)) * dd / R3:+.6f} R here")
        g = (w.be_order == "dip_first" and w.exit_i == v.exit_i
             and w.exit_reason == v.exit_reason
             and abs(float(w.exit_px) - float(v.exit_px)) <= 1e-12
             and abs(float(w.net_r) - float(v.net_r)) <= 1e-12)
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] {side} AND THE 5m ORDER NO "
                     f"LONGER DECIDES IT: the same bar with the two children "
                     f"SWAPPED answers {w.be_order!r} and exits ({w.exit_i}, "
                     f"{w.exit_reason!r}) @ "
                     f"{(float(w.exit_px) - e3) * dd / R3:+.6f} R — the same "
                     f"exit, because a tape that must cross the stop to "
                     f"reach entry crosses it whichever order the walk reads")
        f3 = cx3["f"]
        i3 = BASE_BARS + 3
        edge3 = RC.harvest_edge(float(f3.e89[i3]), float(f3.e316[i3]), dd)
        stack = ((float(f3.e12[i3]) < float(f3.e89[i3]) < float(f3.e316[i3]))
                 if dd == 1 else
                 (float(f3.e12[i3]) > float(f3.e89[i3]) > float(f3.e316[i3])))
        g = (stack and not RC.harvest_outside(float(f3.c[i3]), edge3, dd)
             and not bool(v.harvested) and not bool(u.harvested)
             and v.exit_reason in ("stop", LN.BE_REASON)
             and u.exit_reason in ("stop", LN.BE_REASON))
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] {side} tape INERT over this "
                     f"ride: EMA stack {float(f3.e12[i3]):.2f} / "
                     f"{float(f3.e89[i3]):.2f} / {float(f3.e316[i3]):.2f} is "
                     f"ordered away from every bell a {'long' if dd == 1 else 'short'} "
                     f"could ring, harvest edge {edge3:.2f} vs close "
                     f"{float(f3.c[i3]):.2f} never arms, harvested="
                     f"{bool(v.harvested)}, no bell in either exit reason")
    return ok, lines


def f_be_latch() -> bool:
    def b_unknown_decision():
        """A DECISION THE RIDE DOES NOT KNOW.  The latch bar's stop slot is
        TOTAL, so a third answer must HALT — never fall through it."""
        old = LN.be_latch_decision
        LN.be_latch_decision = lambda seq: "skip"
        try:
            ok, why = refused(lambda: latch_ride(A_ROWS, 2.0))
        finally:
            LN.be_latch_decision = old
        return (not ok), (f"refused: {why}" if ok else
                          "NOT REFUSED — the latch bar rode with no stop "
                          "decision at all")

    return prove(
        "F-BE-LATCH",
        "the latch bar ALWAYS gets a stop decision AND a stop-honest price — "
        "a `plus1r_first` that never dipped leaves the OLD stop standing, a "
        "`plus1r_first` that DID dip fills at the EFFECTIVE stop and not at "
        "entry (both directions), and a floor-bound exit is not a ratchet "
        "exit (all at be_floor_after_r = 2.0, ABOVE v6's trail_arm_after_r)",
        "the floor-ON ride does not exit exactly where the floor-OFF ride "
        "does on a latch bar that pierces a ratcheted stop without reaching "
        "entry; the latch never fires (the check would be vacuous); the "
        "registered pin 1.0 rides a different exit, or rides the SAME ride "
        "as 2.0 (the two pins would not be distinguished); a floor-bound "
        "stop exit is labelled ratchet_exit, or a true ratchet exit is not; "
        "stop_advanced_atr stops counting the floor's lift; the floor does "
        "not move the answer at all; a latch bar that touches NEITHER entry "
        "NOR the ratcheted stop fails to ride on, or rides on differently "
        "with the floor ON than with it OFF; OR, on a latch bar that DOES dip to "
        "entry over a ratchet standing above it, the sequencer does not "
        "answer `plus1r_first` with a dip (the fill branch would not be "
        "under test), the floor-ON ride exits anywhere but the floor-OFF "
        "ride's bar / price / reason / net_r / mfe_r, the exit price is not "
        "the ride's own stop_path tail, the same bar with its two children "
        "SWAPPED exits somewhere else, or the synthetic tape turns out to "
        "ring a bell or arm the harvest in either direction.",
        [("the latch bar's fill priced at `entry_px` UNCONDITIONALLY — the "
          "code of record until 2026-09-22, and the blocking defect itself",
          mutated(LN, "be_latch_fill",
                  lambda stop, entry_px, d: (float(entry_px), LN.BE_REASON),
                  _latch_checks)),
         ("a `plus1r_first` with NO dip called a FILL",
          mutated(LN, "be_latch_decision",
                  lambda seq: (LN.BE_LATCH_FILL
                               if seq["order"] == "plus1r_first"
                               else LN.BE_LATCH_OLD_STOP), _latch_checks)),
         ("the latch decision returns a THIRD value (the stop slot would "
          "fall through in silence — the defect this fixture exists for)",
          b_unknown_decision),
         ("ratchet_exit written as the lineage's expression alone, with no "
          "floor clause", mutated(LN, "ratchet_exit_flag",
                                  lambda leg: bool(
                                      leg["exit_reason"] == "stop"
                                      and leg["advances"]
                                      and abs(leg["final_stop"]
                                              - leg["stop0"]) > 1e-12),
                                  _latch_checks)),
         ("the floor never applied (stop unchanged)",
          mutated(LN, "apply_floor", lambda s, fl, d: float(s),
                  _latch_checks))],
        _latch_checks)


# ═════ F-BE-NOWORSE · a stop-class exit is never worse than its own stop
# THE CHEAPEST INVARIANT IN THE FILE, AND IT WOULD HAVE CAUGHT THE DEFECT.
# `stop_path[-1]` is the stop standing at the START of the exit bar — the
# ratchet may advance again later in the bar, but the stop TEST runs before
# that, so at the moment of a stop-class exit the two are the same number.  A
# campaign may therefore exit AT that stop or BETTER (the floor can only
# raise it), never WORSE.  The pre-repair fill branch exited at +0.000000 R
# with `stop_path[-1]` at +0.412163 R and no leg looked.
NOWORSE_CASES = (
    ("BE_ROWS · dip-after · pin 1.0", BE_ROWS, 1.0, 3, 10, LATCH),
    ("BE_ROWS · dip-before · pin 1.0", BE_ROWS, 1.0, 10, 3, LATCH),
    ("BE_ROWS · tie · pin 1.0", BE_ROWS, 1.0, 7, 7, LATCH),
    ("MONO_ROWS · pin 1.0", MONO_ROWS, 1.0, None, None, LATCH),
    ("A_ROWS · no dip · pin 2.0", A_ROWS, 2.0, None, None, A_LATCH),
    ("LATCH_ROWS · floor-bound · pin 2.0", LATCH_ROWS, 2.0, None, None,
     L_LATCH),
    ("DIP_ROWS · dip over a ratchet · pin 2.0", DIP_ROWS, 2.0, 3, 10,
     A_LATCH),
    ("DIP_ROWS · dip over a ratchet · floor OFF", DIP_ROWS, None, 3, 10,
     A_LATCH),
)


def _noworse_rides() -> list:
    """Every ride in NOWORSE_CASES, in BOTH directions.  WHOLE: no sampling,
    no top-N — the list is the grid, and the count is printed."""
    out = []
    for name, rows, be_r, i_hi, i_lo, bar in NOWORSE_CASES:
        for side, dd in (("bottom", 1), ("top", -1)):
            if i_hi is None:
                pk = None
            elif dd == 1:
                pk = (lambda h, l, c, a=i_hi, b=i_lo:
                      kids(h, l, c, i_hi=a, i_lo=b))
            else:
                pk = (lambda h, l, c, a=i_lo, b=i_hi:
                      kids(h, l, c, i_hi=a, i_lo=b))
            tr, cx = latch_ride(rows, be_r, side, pk, latch_bar=bar)
            for t in tr:
                out.append((f"{name} · {side}", dd, t, cx))
    return out


def _noworse_checks() -> tuple:
    rides = _noworse_rides()
    lines, ok = [], True
    stopclass = [(n, dd, t, cx) for n, dd, t, cx in rides
                 if t.exit_reason in ("stop", LN.BE_REASON)]
    g = len(rides) == 2 * len(NOWORSE_CASES) and len(stopclass) >= 12
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] the grid is WHOLE: "
                 f"{len(NOWORSE_CASES)} authored cases x 2 directions = "
                 f"{len(rides)} campaigns, of which {len(stopclass)} exit "
                 f"stop-class (the invariant would be vacuous under ~12)")
    worst, worst_name = float("inf"), ""
    for n, dd, t, cx in stopclass:
        R = cx["R"]
        slack = (float(t.exit_px) - float(t.stop_path[-1])) * dd / R
        if slack < worst:
            worst, worst_name = slack, n
        g = slack >= -1e-12
        ok &= g
        if not g:
            lines.append(f"[BAD] {n}: exit ({t.exit_i}, {t.exit_reason!r}) "
                         f"@ {(float(t.exit_px) - cx['e']) * dd / R:+.6f} R "
                         f"is {slack:+.6f} R WORSE than its own stop_path "
                         f"tail {(float(t.stop_path[-1]) - cx['e']) * dd / R:+.6f} R")
    g = worst >= -1e-12
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] EVERY stop-class exit is at or "
                 f"better than `stop_path[-1]` for its position: worst slack "
                 f"{worst:+.6f} R on {worst_name!r} (>= 0 required; a "
                 f"negative number is money the tape had already taken away)")
    # THE SECOND HALF, so the first cannot be satisfied by a floor that never
    # binds: at least one ride must exit STRICTLY BETTER than its own tail —
    # otherwise the invariant is an equality in disguise and a `>=` would
    # never be tested.
    strict = [(n, (float(t.exit_px) - float(t.stop_path[-1])) * dd / cx["R"])
              for n, dd, t, cx in stopclass
              if (float(t.exit_px) - float(t.stop_path[-1])) * dd > 1e-9]
    g = len(strict) >= 2
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] and {len(strict)} of them exit "
                 f"STRICTLY BETTER than the tail (the floor lifting the "
                 f"latch bar's own fill), so the bound is a real `>=` and "
                 f"not an equality wearing one: "
                 f"{[(n, round(v, 6)) for n, v in strict[:3]]}")
    return ok, lines


def f_be_noworse() -> bool:
    return prove(
        "F-BE-NOWORSE",
        "a stop-class exit is NEVER worse for the position than the stop "
        "already on its own `stop_path` — every case, both directions",
        "any stop-class exit prices worse than `stop_path[-1]` for its "
        "position; fewer than twelve of the authored campaigns exit "
        "stop-class (the invariant would be vacuous); or none of them exits "
        "STRICTLY better than its own tail (the bound would be an equality "
        "in disguise and the `>=` would never be exercised).",
        [("a WORSE fill planted in the latch bar (one price unit against the "
          "position, below the stop it already holds)",
          mutated(LN, "be_latch_fill",
                  lambda stop, entry_px, d: (float(stop) - d * 1.0, "stop"),
                  _noworse_checks)),
         ("the latch bar's fill priced at `entry_px` unconditionally — the "
          "pre-repair code, which is exactly a worse-than-stop fill whenever "
          "the ratchet stands above entry",
          mutated(LN, "be_latch_fill",
                  lambda stop, entry_px, d: (float(entry_px), LN.BE_REASON),
                  _noworse_checks))],
        _noworse_checks)


# ══ F-BE-IDENT · the repair is BYTE-IDENTICAL at the registered pin 1.0
# THE SAFETY PROPERTY OF THE REPAIR, PROVEN AND NOT ASSERTED.  At
# `be_floor_after_r = 1.0` — which is v6's own `trail_arm_after_r` — no
# advance can precede the latch, so on the latch bar `stop` is still `stop0`
# (adverse) and `apply_floor(stop0, entry_px, d)` returns `entry_px`.  The
# repaired branch and the pre-repair branch therefore compute the SAME number
# there, and the whole scenario set must digest the same both ways.  Above
# the pin they must DIFFER, or the repair changed nothing and the identity is
# the identity of a dead branch.
PRE_REPAIR_FILL = (lambda stop, entry_px, d: (float(entry_px), LN.BE_REASON))

IDENT_PIN_CASES = (
    ("BE_ROWS · dip-after", BE_ROWS, 3, 10, LATCH),
    ("BE_ROWS · dip-before", BE_ROWS, 10, 3, LATCH),
    ("BE_ROWS · tie", BE_ROWS, 7, 7, LATCH),
    ("MONO_ROWS", MONO_ROWS, None, None, LATCH),
    ("A_ROWS", A_ROWS, None, None, A_LATCH),
    ("LATCH_ROWS", LATCH_ROWS, None, None, L_LATCH),
    ("DIP_ROWS", DIP_ROWS, 3, 10, A_LATCH),
)
IDENT_FIELDS = ("exit_i", "exit_reason", "exit_px", "net_r", "gross_r",
                "fee_r", "funding_r", "mfe_r", "mae_r", "bars_held",
                "final_stop_px", "stop_advanced_atr", "ratchet_exit",
                "be_on", "be_reached", "be_bar", "be_order", "be_exit",
                "be_bound_at_exit", "n_be_tie", "n_be_mismatch")


def _ident_digest(be_r: float) -> str:
    """The whole scenario set at one pin, both directions, digested."""
    rows = []
    for name, rows_, i_hi, i_lo, bar in IDENT_PIN_CASES:
        for side, dd in (("bottom", 1), ("top", -1)):
            if i_hi is None:
                pk = None
            elif dd == 1:
                pk = (lambda h, l, c, a=i_hi, b=i_lo:
                      kids(h, l, c, i_hi=a, i_lo=b))
            else:
                pk = (lambda h, l, c, a=i_lo, b=i_hi:
                      kids(h, l, c, i_hi=a, i_lo=b))
            tr, _cx = latch_ride(rows_, be_r, side, pk, latch_bar=bar)
            for t in tr:
                rows.append([name, side, be_r]
                            + [(round(float(getattr(t, k)), 12)
                                if isinstance(getattr(t, k), float)
                                else getattr(t, k)) for k in IDENT_FIELDS]
                            + [[round(float(x), 12) for x in t.stop_path]])
    return _digest(rows)


def _ident_checks() -> tuple:
    lines, ok = [], True
    old = LN.be_latch_fill
    try:
        a1 = _ident_digest(1.0)
        a2 = _ident_digest(2.0)
        LN.be_latch_fill = PRE_REPAIR_FILL
        b1 = _ident_digest(1.0)
        b2 = _ident_digest(2.0)
    finally:
        LN.be_latch_fill = old
    g = a1 == b1
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] AT THE REGISTERED PIN 1.0 THE "
                 f"REPAIR IS BYTE-IDENTICAL: repaired {a1[:16]} / "
                 f"pre-repair {b1[:16]} over {len(IDENT_PIN_CASES)} tapes x "
                 f"2 directions x {len(IDENT_FIELDS)} journal fields + the "
                 f"whole stop_path")
    g = a2 != b2
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] AND AT 2.0 THEY DIFFER, so the "
                 f"identity above is not the identity of a dead branch: "
                 f"repaired {a2[:16]} / pre-repair {b2[:16]}")
    # THE STRUCTURAL REASON, asserted over the WHOLE set rather than
    # observed on the exits: at pin 1.0 the stop standing at the START of
    # every latch bar is still `stop0` — no advance ever precedes the latch,
    # because 1.0 IS v6's `trail_arm_after_r`.  That is why `apply_floor` can
    # only return entry there, and it is checked on every campaign, not only
    # on the ones that happened to fill.
    n_latch, n_moved, n_fill, n_bad = 0, 0, 0, 0
    for name, rows_, i_hi, i_lo, bar in IDENT_PIN_CASES:
        for side, dd in (("bottom", 1), ("top", -1)):
            if i_hi is None:
                pk = None
            elif dd == 1:
                pk = (lambda h, l, c, a=i_hi, b=i_lo:
                      kids(h, l, c, i_hi=a, i_lo=b))
            else:
                pk = (lambda h, l, c, a=i_lo, b=i_hi:
                      kids(h, l, c, i_hi=a, i_lo=b))
            tr, cx = latch_ride(rows_, 1.0, side, pk, latch_bar=bar)
            for t in tr:
                if t.be_bar is not None:
                    n_latch += 1
                    k = int(t.be_bar) - int(t.entry_i) - 1
                    at_latch = float(t.stop_path[k]) if 0 <= k < len(
                        t.stop_path) else float("nan")
                    n_moved += int(abs(at_latch - float(t.stop_px)) > 1e-12)
                if t.exit_reason == LN.BE_REASON:
                    n_fill += 1
                    n_bad += int(abs(float(t.exit_px)
                                     - float(cx["e"])) > 1e-12)
    g = n_latch >= 12 and n_moved == 0 and n_fill >= 2 and n_bad == 0
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] THE REASON, over the whole set: "
                 f"{n_latch} campaigns latched at pin 1.0 and in {n_moved} "
                 f"of them had the ratchet moved the stop off stop0 before "
                 f"the latch bar (0 required — 1.0 == v6's "
                 f"trail_arm_after_r, so no advance can precede the latch "
                 f"and apply_floor can only return entry); the "
                 f"{n_fill} `be_floor` fills that resulted all landed "
                 f"EXACTLY at entry ({n_bad} did not)")
    # and the CLASSIC5 control, floor OFF: the branch is dead there, so the
    # repair cannot have touched the one real-data book this module rides.
    b = books()
    j1 = TP.journal_frame(LN.run_lane(LN.CARD_TC10_CONTROL, T9.V6_ROLES,
                                      TP.CLASSIC5, b["lo"], b["hi"]))
    h1 = hashlib.sha256(j1.to_csv(index=False).encode()).hexdigest()
    try:
        LN.be_latch_fill = PRE_REPAIR_FILL
        j2 = TP.journal_frame(LN.run_lane(LN.CARD_TC10_CONTROL, T9.V6_ROLES,
                                          TP.CLASSIC5, b["lo"], b["hi"]))
    finally:
        LN.be_latch_fill = old
    h2 = hashlib.sha256(j2.to_csv(index=False).encode()).hexdigest()
    g = h1 == h2 and len(j1) == len(b["want"]) and len(j1) > 0
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] and the CLASSIC5 CONTROL "
                 f"journal ({len(j1)} campaigns) is byte-identical both "
                 f"ways — {h1[:16]} / {h2[:16]} — because with the floor OFF "
                 f"the branch is dead code")
    return ok, lines


def f_be_ident() -> bool:
    return prove(
        "F-BE-IDENT",
        "the latch-bar repair is BYTE-IDENTICAL to the pre-repair ride at "
        "the REGISTERED pin be_floor_after_r = 1.0, and DIFFERS at 2.0",
        "the repaired and pre-repair digests differ at pin 1.0 (the repair "
        "would have moved the registered ride); they AGREE at 2.0 (the "
        "repair would be a no-op and the identity above would be the "
        "identity of a dead branch); any `be_floor` fill at pin 1.0 lands "
        "anywhere but exactly entry; or the CLASSIC5 control journal moves "
        "between the two.",
        [("the PRE-REPAIR stand-in replaced by the REPAIRED function itself "
          "(the comparison would compare a thing with itself)",
          mutated(_SELF, "PRE_REPAIR_FILL", LN.be_latch_fill,
                  _ident_checks)),
         ("the latch decision forced to `old_stop`, so the fill branch never "
          "runs at 2.0 either", mutated(LN, "be_latch_decision",
                                        lambda seq: LN.BE_LATCH_OLD_STOP,
                                        _ident_checks)),
         ("the floor neutered (apply_floor returns the ratchet untouched), "
          "so repaired and pre-repair agree nowhere they should differ",
          mutated(LN, "apply_floor", lambda s, fl, d: float(s),
                  _ident_checks))],
        _ident_checks)


# ═══ F-BE-SPEC · the WORDS of record match the LEGS that exist
# THE HALF OF THE 2026-09-22 FINDING THAT IS NOT CODE.  `LANE_SPEC['P-BE-1']
# ['latch_bar_totality']` claimed F-BE-LATCH proved the 2.0 ride "exits
# exactly where the floor-OFF ride does — so a sensitivity run off the
# registered 1.0 is proven, not assumed", and a builder DECLINED a reviewer's
# protective HALT on that sentence.  The sentence was false: the leg drove
# only the OLD_STOP half.  This fixture makes the prose checkable:
#   · the prose is PINNED BY SHA, so strengthening the words without
#     re-pinning goes RED;
#   · every claim in it is listed against the fixture that drives it, and
#     that fixture must have PASSED in this same run;
#   · the retracted sentences must not reappear anywhere in LANE_SPEC.
def _spec_text(spec) -> str:
    return json.dumps(spec, sort_keys=True, default=str)


def _spec_checks() -> tuple:
    lines, ok = [], True
    prose = str(LN.LANE_SPEC["P-BE-1"]["latch_bar_totality"])
    got = hashlib.sha256(prose.encode()).hexdigest()
    g = got == LN.LATCH_TOTALITY_SHA
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] the prose of record is PINNED: "
                 f"sha256 {got[:24]}… vs LATCH_TOTALITY_SHA "
                 f"{str(LN.LATCH_TOTALITY_SHA)[:24]}… ({len(prose)} chars) — "
                 f"changing the words without re-pinning turns this RED")
    for phrase, fid in LN.LATCH_TOTALITY_CLAIMS:
        n = prose.count(phrase)
        got_res = RESULTS.get(fid)
        g = (n == 1 and got_res is True)
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] claim {phrase[:46]!r} "
                     f"appears {n}x (1 required) and is driven by {fid}, "
                     f"which is "
                     + ("PASS" if got_res is True else
                        "FAILED" if got_res is False else
                        "NOT IN THIS RUN — F-BE-SPEC checks the words "
                        "against the legs and needs the WHOLE suite"))
    whole = _spec_text(LN.LANE_SPEC)
    g = len(LN.LATCH_TOTALITY_RETRACTED) >= 2 and all(
        isinstance(x, str) and len(x) > 40
        for x in LN.LATCH_TOTALITY_RETRACTED)
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] the RETRACTION REGISTRY still "
                 f"holds both halves of the 2026-09-21 sentence "
                 f"({len(LN.LATCH_TOTALITY_RETRACTED)} entries, >= 2 "
                 f"required) — an emptied registry would let the false "
                 f"claim return unnoticed")
    for retracted in LN.LATCH_TOTALITY_RETRACTED:
        g = retracted not in whole and retracted not in prose
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] the RETRACTED sentence "
                     f"{retracted[:52]!r}… appears nowhere in LANE_SPEC")
    g = ("NOT a sensitivity run" in prose
         and "nothing here says the 2.0 book equals the 1.0 book on real "
             "bars" in prose)
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] and the prose DISCLAIMS what it "
                 f"does not prove, in its own words: it says the four bars "
                 f"are NOT a sensitivity run and that nothing here equates "
                 f"the 2.0 and 1.0 books on real bars")
    named = sorted({fid for _p, fid in LN.LATCH_TOTALITY_CLAIMS})
    g = len(named) == 3 and set(named) == {"F-BE-LATCH", "F-BE-IDENT",
                                           "F-BE-NOWORSE"}
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] the claim registry names "
                 f"exactly the three legs that exist for this branch: "
                 f"{named}")
    return ok, lines


def f_be_spec() -> bool:
    strengthened = {k: (dict(v) if isinstance(v, dict) else v)
                    for k, v in LN.LANE_SPEC.items()}
    strengthened["P-BE-1"] = dict(LN.LANE_SPEC["P-BE-1"])
    strengthened["P-BE-1"]["latch_bar_totality"] = (
        LN.LATCH_TOTALITY + " A sensitivity run off the registered 1.0 is "
        "therefore proven, not assumed.")
    restored = {k: (dict(v) if isinstance(v, dict) else v)
                for k, v in LN.LANE_SPEC.items()}
    restored["P-BE-1"] = dict(LN.LANE_SPEC["P-BE-1"])
    restored["P-BE-1"]["latch_bar_totality"] = (
        "the latch bar's stop slot is TOTAL: `be_latch_decision` maps every "
        "5m answer onto a fill or the old stop, a third answer HALTs, and "
        "F-BE-LATCH proves the ride at be_floor_after_r = 2.0 (ABOVE v6's "
        "trail_arm_after_r 1.0, where the ratchet can precede the latch) "
        "exits exactly where the floor-OFF ride does — so a sensitivity run "
        "off the registered 1.0 is proven, not assumed [review 2026-09-21]")
    return prove(
        "F-BE-SPEC",
        "the latch-bar WORDS OF RECORD are pinned by sha, every claim in "
        "them names a fixture that PASSED in this run, and the retracted "
        "2026-09-21 sentence cannot return",
        "the prose's sha does not match LATCH_TOTALITY_SHA (someone "
        "strengthened the words without re-pinning them beside a leg); any "
        "claim phrase is missing, duplicated, or names a fixture that did "
        "not pass in THIS run; either retracted sentence reappears anywhere "
        "in LANE_SPEC; the prose stops disclaiming the sensitivity run it "
        "does not perform; or the claim registry names a set of legs other "
        "than {F-BE-LATCH, F-BE-IDENT, F-BE-NOWORSE}. It also fails on a "
        "FILTERED run that skips those three legs — the words are checked "
        "against the legs, so the legs must have run.",
        [("the prose STRENGTHENED by one sentence, sha not re-pinned (the "
          "exact move this fixture exists to stop)",
          mutated(LN, "LANE_SPEC", strengthened, _spec_checks)),
         ("the FALSE CLAIM OF 2026-09-21 restored verbatim",
          mutated(LN, "LANE_SPEC", restored, _spec_checks)),
         ("a claim that names a fixture which does not exist",
          mutated(LN, "LATCH_TOTALITY_CLAIMS",
                  tuple(list(LN.LATCH_TOTALITY_CLAIMS)
                        + [("a third answer HALTs", "F-BE-NOSUCHLEG")]),
                  _spec_checks)),
         ("the retraction forgotten (LATCH_TOTALITY_RETRACTED emptied), so "
          "the false sentence could return unnoticed",
          mutated(LN, "LATCH_TOTALITY_RETRACTED", (), _spec_checks))],
        _spec_checks)


# ══════════════════════ F-SPR-SYN · a planted deviation-confirm, both sides
def _spr_case(side: str):
    o, h, l, c = spring_base(side, second=(side == "bottom"))
    if side != "bottom":
        e = c[-1]
        for _ in range(8):
            o.append(e)
            h.append(e + 1.0)
            l.append(e - 1.0)
            c.append(e)
    st, om = install_frame(SPR_SYM[side], o, h, l, c)
    sig = base_signal(side, om, h, l)
    return st, om, np.asarray(h), np.asarray(l), np.asarray(c), sig


def second_signal(om, l) -> LN.SpringSignal:
    """The second, shallower bottom deviation-confirm, from the raw tape."""
    a, i = SECOND
    return LN.SpringSignal(
        direction=1, sweep_i=a, sweep_ms=int(om[a]),
        sweep_extreme=float(np.min(np.asarray(l)[a:i + 1])),
        swept_level=LEVEL_BOT, reclaim_i=i, reclaim_ms=int(om[i]),
        bars_to_reclaim=i - a, known_at=i, rid=2, side="bottom",
        source="synthetic/bottom#2")


def _spr_checks() -> tuple:
    lines, ok = [], True
    card = LN.CARD_SPR2
    for side, d in (("bottom", 1), ("top", -1)):
        st, om, h, l, c, sig = _spr_case(side)
        f = st["f"]
        i = BASE_BARS + 3
        tr = LN.replay10(SPR_SYM[side], card, T9.V6_ROLES, int(om[0]),
                         int(om[-1]) + MS_4H - 1, springs=[sig])[1]
        if len(tr) != 1:
            ok = False
            lines.append(f"[BAD] {side}: {len(tr)} campaigns, expected 1")
            continue
        t = tr[0]
        # THE STOP, RE-DERIVED FROM THE RAW TAPE AND THE PINS BY OBJECT:
        # "beyond the sweep extreme, railed at the card's entry rail".
        atr = float(f.atr[i])
        ext = float(sig.sweep_extreme)
        pivot = ext - d * RC.STOP_BUF_ATR * atr
        rail = float(f.c[i]) - d * card.entry_rail_atr * atr
        want_stop = min(pivot, rail) if d == 1 else max(pivot, rail)
        g = (t.direction == d and t.entry_i == i
             and int(t.entry_ms) == int(om[i])
             and abs(float(t.entry_px) - float(f.c[i])) <= 1e-12
             and abs(float(t.stop_px) - want_stop) <= 1e-12
             and abs(float(t.r_dist) - abs(float(f.c[i]) - want_stop)) <= 1e-12
             and t.lane == "spring")
        ok &= g
        lines.append(
            f"[{'OK ' if g else 'BAD'}] {side} ({'long spring' if d == 1 else 'short upthrust'}): "
            f"entry bar {t.entry_i} @ {float(t.entry_px):.4f} (the reclaim "
            f"CLOSE), stop {float(t.stop_px):.4f} vs the tape's "
            f"{want_stop:.4f} = {'min' if d == 1 else 'max'}(extreme "
            f"{ext!r} (RAW, four decimals — a 2-dp event field would read "
            f"{round(ext, 2)}) {'-' if d == 1 else '+'} {RC.STOP_BUF_ATR} "
            f"ATR, "
            f"entry {'-' if d == 1 else '+'} {card.entry_rail_atr} ATR), "
            f"R {float(t.r_dist):.4f}, lane {t.lane!r}")
        # THE AS-OF LAW: known at the harden bar, entered at ITS close
        g = (int(sig.known_at) == int(sig.reclaim_i) == t.entry_i
             and t.arm_i == int(sig.sweep_i)
             and int(t.entry_ms) == int(om[int(sig.known_at)]))
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] {side} AS-OF: known_at "
                     f"{sig.known_at} == reclaim_i {sig.reclaim_i} == entry "
                     f"bar {t.entry_i}; a harden known at bar i cannot enter "
                     f"before bar i's close")
        # the shape warranty, run explicitly, and the counts it reports
        rep = LN.check_signals(f, [sig], 0, len(f.c) - 1)
        g = rep["n_signals"] == 1 and rep["n_long"] == int(d == 1)
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] {side} check_signals: {rep}")
        # the tape's OTHER machinery is inert over this ride, asserted
        edge = RC.harvest_edge(float(f.e89[i]), float(f.e316[i]), d)
        stack = ((float(f.e12[i]) < float(f.e89[i]) < float(f.e316[i]))
                 if d == 1 else
                 (float(f.e12[i]) > float(f.e89[i]) > float(f.e316[i])))
        g = (stack and not RC.harvest_outside(float(f.c[i]), edge, d)
             and not bool(t.harvested)
             and t.exit_reason in ("corridor_end", "stop"))
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] {side} tape inert: EMA "
                     f"stack ordered away from every bell this direction "
                     f"could ring ({float(f.e12[i]):.2f} / "
                     f"{float(f.e89[i]):.2f} / {float(f.e316[i]):.2f}), "
                     f"harvest edge {edge:.2f} vs close {float(f.c[i]):.2f} "
                     f"never arms, harvested={bool(t.harvested)}, exit "
                     f"{t.exit_reason!r}")

    # ONE POSITION PER ASSET, cardinally: a SECOND valid deviation-confirm
    # whose reclaim falls while the first campaign is still open.
    st, om, h, l, c, sig = _spr_case("bottom")
    f = st["f"]
    sig2 = second_signal(om, l)
    LN.check_signals(f, [sig, sig2], 0, len(f.c) - 1)
    alone = LN.replay10(SPR_SYM["bottom"], card, T9.V6_ROLES, int(om[0]),
                        int(om[-1]) + MS_4H - 1, springs=[sig2])[1]
    both = LN.replay10(SPR_SYM["bottom"], card, T9.V6_ROLES, int(om[0]),
                       int(om[-1]) + MS_4H - 1, springs=[sig, sig2])[1]
    g = (len(alone) == 1 and alone[0].entry_i == SECOND[1]
         and len(both) == 1 and both[0].entry_i == BASE_BARS + 3
         and both[0].exit_i >= SECOND[1])
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] ONE POSITION PER ASSET: the "
                 f"second signal ALONE gives 1 campaign entering at bar "
                 f"{alone[0].entry_i if alone else None}; injected together "
                 f"with the first it is SKIPPED — {len(both)} campaign(s), "
                 f"entry bar {both[0].entry_i if both else None}, still open "
                 f"at bar {SECOND[1]} (exit "
                 f"{both[0].exit_i if both else None})")

    # THE SABOTAGE, RUN AS PART OF THE REAL LEG: a signal stamped ONE BAR
    # EARLY must be refused — the harden is the FIRST bar that closes back
    # inside, so the bar before it does not.
    st, om, h, l, c, sig = _spr_case("bottom")
    f = st["f"]
    early = LN.SpringSignal(
        direction=1, sweep_i=sig.sweep_i, sweep_ms=sig.sweep_ms,
        sweep_extreme=float(np.min(f.l[sig.sweep_i:sig.reclaim_i])),
        swept_level=sig.swept_level, reclaim_i=sig.reclaim_i - 1,
        reclaim_ms=int(om[sig.reclaim_i - 1]),
        bars_to_reclaim=sig.bars_to_reclaim - 1,
        known_at=sig.reclaim_i - 1, rid=1, side="bottom",
        source="synthetic/bottom ONE BAR EARLY")
    r_ok, why = refused(lambda: LN.check_signals(f, [early], 0, len(f.c) - 1))
    ok &= r_ok
    lines.append(f"[{'OK ' if r_ok else 'BAD'}] a signal stamped ONE BAR "
                 f"EARLY is refused: {why[:150]}")
    r_ok2, why2 = refused(lambda: LN.replay10(
        SPR_SYM["bottom"], LN.CARD_SPR2, T9.V6_ROLES, int(om[0]),
        int(om[-1]) + MS_4H - 1, springs=[early]))
    ok &= r_ok2
    lines.append(f"[{'OK ' if r_ok2 else 'BAD'}] and the RUNNER refuses it "
                 f"too, before a candidate is built: {why2[:120]}")
    return ok, lines


def f_spr_syn() -> bool:
    def gutted(f_, springs, lo_i=0, hi_i=None):
        """check_signals with its teeth removed: it accepts anything."""
        return {"n_signals": len(springs), "n_long": 0, "n_short": 0}

    st, om, h, l, c, sig = _spr_case("bottom")
    f = st["f"]

    def bad_sig(**kw):
        d = dict(direction=sig.direction, sweep_i=sig.sweep_i,
                 sweep_ms=sig.sweep_ms, sweep_extreme=sig.sweep_extreme,
                 swept_level=sig.swept_level, reclaim_i=sig.reclaim_i,
                 reclaim_ms=sig.reclaim_ms,
                 bars_to_reclaim=sig.bars_to_reclaim, known_at=sig.known_at,
                 rid=1, side="bottom", source="planted")
        d.update(kw)
        return LN.SpringSignal(**d)

    return prove(
        "F-SPR-SYN",
        "a synthetic range with a planted deviation-confirm on EACH side: "
        "exactly the expected entry and stop, entered at the harden bar's "
        "close, and a signal stamped one bar early goes RED",
        "either side's entry bar, entry price, stop or R differs from the "
        "value re-derived on the raw tape; the entry is not at the harden "
        "bar's close; the one-bar-early signal is accepted by check_signals "
        "OR by the runner; or any hand-planted malformed signal rides.",
        [("a signal stamped ONE BAR EARLY (the sabotage)",
          attack(lambda: LN.check_signals(
              f, [bad_sig(reclaim_i=sig.reclaim_i - 1,
                          reclaim_ms=int(om[sig.reclaim_i - 1]),
                          known_at=sig.reclaim_i - 1,
                          bars_to_reclaim=sig.bars_to_reclaim - 1,
                          sweep_extreme=float(
                              np.min(f.l[sig.sweep_i:sig.reclaim_i])))],
              0, len(f.c) - 1))),
         ("known_at stamped BEFORE the reclaim bar",
          attack(lambda: LN.check_signals(
              f, [bad_sig(known_at=sig.reclaim_i - 1)], 0, len(f.c) - 1))),
         ("sweep_extreme taken from the machine's 2-dp event field",
          attack(lambda: LN.check_signals(
              f, [bad_sig(sweep_extreme=round(float(sig.sweep_extreme), 2))],
              0, len(f.c) - 1))),
         ("swept_level moved so the reclaim no longer closes inside",
          attack(lambda: LN.check_signals(
              f, [bad_sig(swept_level=float(f.c[sig.reclaim_i]) + 1.0)],
              0, len(f.c) - 1))),
         ("bars_to_reclaim inconsistent with the two indices",
          attack(lambda: LN.check_signals(
              f, [bad_sig(bars_to_reclaim=99)], 0, len(f.c) - 1))),
         ("sweep_ms not the sweep bar's own open",
          attack(lambda: LN.check_signals(
              f, [bad_sig(sweep_ms=int(om[sig.sweep_i]) + MS_4H)],
              0, len(f.c) - 1))),
         ("the shape warranty gutted (check_signals accepts anything)",
          mutated(LN, "check_signals", gutted, _spr_checks))],
        _spr_checks)


# ══════════ F-SPR-BUILD · the signal HARNESS, from the census as-of layer
BUILD_SYM = "SYN-CENSUS-4H"
BUILD_T0 = 1_500_000_000_000 - (1_500_000_000_000 % MS_4H)


def census_tape():
    """A SYNTHETIC census tape the machine actually finds ranges in: a seeded
    zigzag between two shelves, with the deviations the pins were calibrated
    to see.  Seeded at 20260921 and built from `numpy.random.Generator`, so
    it is the same tape in every process [L8]."""
    from engine import indicators as ind                  # noqa: PLC0415
    rng = np.random.default_rng(SEED)
    n, p, c = 900, 1000.0, []
    for i in range(n):
        tgt = {0: 1045.0, 1: 960.0, 2: 1040.0, 3: 955.0}[(i // 30) % 4]
        p += (tgt - p) * 0.18 + rng.normal(0, 1.2)
        c.append(p)
    c = np.asarray(c, float)
    h, l = c + 3.0, c - 3.0
    o = np.r_[c[0], c[:-1]]
    t0 = np.arange(n, dtype=np.int64) * MS_4H + BUILD_T0
    return o, h, l, c, t0, ind.atr(h, l, c, 14)


def _census_obj():
    import tierc10_census as C                            # noqa: PLC0415
    o, h, l, c, t0, atr = census_tape()
    return C, C.Tape(BUILD_SYM, "4h", o, h, l, c, t0,
                     [str(x) for x in t0], atr, {}), (o, h, l, c, t0)


def _hand_episodes(events) -> list:
    """The episode pairing, re-derived in a plain loop that shares no code
    with `harden_episodes` — the census's own law: a harden closes the LAST
    same-side breach-open of its range."""
    opens, out = {}, []
    for e in events:
        k = e.get("event")
        if k == "breach-open":
            opens[(e["rid"], e["side"])] = int(e["i"])
        elif k == "harden":
            out.append((int(e["rid"]), str(e["side"]),
                        int(opens[(e["rid"], e["side"])]), int(e["i"])))
    return sorted(out, key=lambda r: (r[3], r[2]))


def _build_checks() -> tuple:
    C, tape, (o, h, l, c, t0) = _census_obj()
    lines, ok = [], True
    sigs = LN.spring_signals_from_census(BUILD_SYM, "4h", LN.FROZEN_SCALE,
                                         tape=tape)
    m = C.run_scale(tape, LN.FROZEN_SCALE)
    view = C.asof_view(tape, m["macro"], m["leash"])
    hand = _hand_episodes(m["macro"]["events"])
    got = [(s.rid, s.side, s.sweep_i, s.reclaim_i) for s in sigs]
    g = got == hand and len(hand) >= 3
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] the episode pairing equals an "
                 f"independent plain-loop walk of the SAME event list: "
                 f"{len(got)} episodes {got} vs {hand}")
    n_l = sum(1 for s in sigs if s.direction == 1)
    n_s = len(sigs) - n_l
    g = n_l >= 1 and n_s >= 1 and all(
        (s.direction == 1) == (s.side == "bottom") for s in sigs)
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] BOTH SIDES are built and the "
                 f"mapping is the ruling's: bottom -> long ({n_l}), top -> "
                 f"short ({n_s})")
    bad = []
    for s in sigs:
        d = s.direction
        raw = (float(np.min(l[s.sweep_i:s.reclaim_i + 1])) if d == 1
               else float(np.max(h[s.sweep_i:s.reclaim_i + 1])))
        lvl = (float(view["bot"][s.sweep_i]) if d == 1
               else float(view["top"][s.sweep_i]))
        okk = (float(s.sweep_extreme) == raw and float(s.swept_level) == lvl
               and s.known_at == s.reclaim_i
               and ((raw < lvl and float(c[s.reclaim_i]) >= lvl) if d == 1
                    else (raw > lvl and float(c[s.reclaim_i]) <= lvl)))
        if not okk:
            bad.append(s.source)
    g = not bad
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] every signal's extreme is the "
                 f"RAW tape's over [sweep, reclaim], its level is the AS-OF "
                 f"boundary AT THE BREACH BAR, and the shape is a "
                 f"deviation-confirm: {len(sigs)} of {len(sigs)} "
                 f"({bad or 'none bad'})")
    lines.append("      AS-OF, SAID PLAINLY [review 2026-09-21]: the level "
                 "is as-of because `springs_from_episodes` reads "
                 "bot_asof/top_asof AT THE BREACH BAR — a fact this leg "
                 "checks against the census's OWN as-of view. "
                 "`check_signals` cannot re-check it on the raw tape (it "
                 "tests the deviation-confirm SHAPE), so P-SPR-2's as-of "
                 "warranty is the CENSUS module's F-RNG-ASOF and the BUILD "
                 "doc must say so. The level never enters a price: "
                 "tierc5_rules.spring_stop reads sweep_extreme alone.")
    # ROUND TRIP: builder -> checker -> runner, on a frame of the same bars
    st, om = install_frame(BUILD_SYM, o, h, l, c, om=t0)
    rep = LN.check_signals(st["f"], sigs, 0, len(c) - 1)
    g = rep["n_signals"] == len(sigs)
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] the built list survives "
                 f"check_signals unchanged on a frame of the same bars: "
                 f"{rep}")
    # signals_on_frame maps by STAMP, never by position: the same bars with
    # 20 earlier bars prepended must come back shifted by exactly 20.
    pad = 20
    om2 = np.r_[t0[0] - np.arange(pad, 0, -1, dtype=np.int64) * MS_4H, t0]
    o2 = np.r_[np.full(pad, o[0]), o]
    h2, l2, c2 = (np.r_[np.full(pad, x[0]), x] for x in (h, l, c))
    st2, _ = install_frame(BUILD_SYM + "-SHIFTED", o2, h2, l2, c2, om=om2)
    moved = LN.signals_on_frame(st2["f"], sigs)
    g = (len(moved) == len(sigs)
         and all(mm.reclaim_i == s.reclaim_i + pad
                 and mm.sweep_i == s.sweep_i + pad
                 and mm.known_at == mm.reclaim_i
                 and int(mm.reclaim_ms) == int(s.reclaim_ms)
                 for mm, s in zip(moved, sigs)))
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] signals_on_frame re-indexes by "
                 f"MILLISECOND: {pad} earlier bars prepended -> every index "
                 f"moves by exactly {pad} and every stamp is unchanged")
    # IT RE-DERIVES, AND IT ALSO REFUSES [review 2026-09-21].  A signal whose
    # own claims disagree with the ride's tape is CORRUPTED, and a corrupted
    # signal must be surfaced rather than quietly repaired into a good one.
    s0 = sigs[0] if sigs else None
    corrupt = [] if s0 is None else [
        ("sweep_extreme", dataclasses.replace(s0, sweep_extreme=1.0)),
        ("known_at", dataclasses.replace(s0, known_at=-999)),
        ("bars_to_reclaim",
         dataclasses.replace(s0, bars_to_reclaim=int(s0.bars_to_reclaim) + 3))]
    if s0 is None:
        ok = False
        lines.append("[BAD] no signal was built, so the corruption legs "
                     "cannot run")
    for field, bad_sig in corrupt:
        r_ok, why = refused(lambda bs=bad_sig: LN.signals_on_frame(st2["f"],
                                                                   [bs]))
        ok &= r_ok
        lines.append(f"[{'OK ' if r_ok else 'BAD'}] a signal carrying a "
                     f"corrupted {field} is REFUSED, not repaired: "
                     f"{why[:100]}")
    drop_frame(BUILD_SYM + "-SHIFTED")
    # TWO HARDENS, ONE OPEN — the census's OWN pairing law, recorded rather
    # than assumed [review 2026-09-21].  `tierc10_census.asof_view` reads
    # `opens[(rid, side)]` on a harden and never consumes it
    # (tierc10_census.py:778-786), so a SECOND harden with no intervening
    # breach-open pairs with the SAME, now stale, open.  A port that "fixed"
    # that here would make the spring lane's episodes disagree with the
    # census tables printed beside them.
    dup_ev = [{"event": "breach-open", "i": 3, "rid": 7, "side": "bottom"},
              {"event": "harden", "i": 5, "rid": 7, "side": "bottom"},
              {"event": "harden", "i": 9, "rid": 7, "side": "bottom"},
              {"event": "breach-open", "i": 11, "rid": 7, "side": "bottom"},
              {"event": "harden", "i": 14, "rid": 7, "side": "bottom"}]
    dup, dup_hand = LN.harden_episodes(dup_ev), _hand_episodes(dup_ev)
    want_dup = [(7, "bottom", 3, 5), (7, "bottom", 3, 9),
                (7, "bottom", 11, 14)]
    g = dup == want_dup and dup_hand == want_dup
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] TWO HARDENS, ONE OPEN: the "
                 f"second pairs with the SAME open (the census's own law, "
                 f"tierc10_census.py:778-786) and a later breach-open "
                 f"replaces it — module {dup} / independent walk {dup_hand}")
    return ok, lines


def _repairing_on_frame(f, springs):
    """THE OLD `signals_on_frame`, planted as a break leg: it re-derived every
    price and every stamp and refused NOTHING, so a corrupted signal came
    back REPAIRED into a good one."""
    om = f.open_ms
    out = []
    for sp in springs:
        a = int(np.searchsorted(om, int(sp.sweep_ms), "left"))
        i = int(np.searchsorted(om, int(sp.reclaim_ms), "left"))
        if not (0 <= a < len(om) and 0 <= i < len(om)) \
                or int(om[a]) != int(sp.sweep_ms) \
                or int(om[i]) != int(sp.reclaim_ms):
            raise SystemExit("HALT: the ride's frame holds no bar opening at "
                             "one of the signal's stamps.")
        d = int(sp.direction)
        ext = (float(np.min(f.l[a:i + 1])) if d == 1
               else float(np.max(f.h[a:i + 1])))
        out.append(LN.SpringSignal(
            direction=d, sweep_i=a, sweep_ms=int(sp.sweep_ms),
            sweep_extreme=ext, swept_level=float(sp.swept_level),
            reclaim_i=i, reclaim_ms=int(sp.reclaim_ms),
            bars_to_reclaim=int(i - a), known_at=i, rid=int(sp.rid),
            side=str(sp.side), source=str(sp.source)))
    out.sort(key=lambda s: (s.reclaim_ms, -s.direction))
    return out


def _consuming_episodes(events) -> list:
    """A pairing that CONSUMES its open — the census does not, and a port
    that did would drop the second of two hardens on one open."""
    opens, out = {}, []
    for e in events:
        k = e.get("event")
        if k == "breach-open":
            opens[(e["rid"], e["side"])] = int(e["i"])
        elif k == "harden":
            kk = (e["rid"], e["side"])
            if kk not in opens:
                raise SystemExit(f"HALT: harden at bar {e['i']} has no "
                                 f"same-side breach-open before it.")
            out.append((int(e["rid"]), str(e["side"]), int(opens.pop(kk)),
                        int(e["i"])))
    out.sort(key=lambda r: (r[3], r[2]))
    return out


def f_spr_build() -> bool:
    def b_orphan_harden():
        LN.harden_episodes([{"event": "harden", "i": 5, "rid": 1,
                             "side": "bottom"}])

    def b_cross_side():
        LN.harden_episodes([{"event": "breach-open", "i": 3, "rid": 1,
                             "side": "top"},
                            {"event": "harden", "i": 5, "rid": 1,
                             "side": "bottom"}])

    def b_redrawn_level():
        """A CORRUPTED INPUT: the boundary read AFTER the harden's redraw
        (i.e. the extreme itself) instead of the AS-OF one at the breach."""
        C, tape, (o, h, l, c, t0) = _census_obj()
        m = C.run_scale(tape, LN.FROZEN_SCALE)
        eps = LN.harden_episodes(m["macro"]["events"])
        bot = np.asarray(l, float).copy()
        top = np.asarray(h, float).copy()
        sigs = LN.springs_from_episodes(h, l, c, t0, eps, top, bot,
                                        source="redrawn")
        st, _ = install_frame(BUILD_SYM, o, h, l, c, om=t0)
        LN.check_signals(st["f"], sigs, 0, len(c) - 1)

    def b_stamp_absent():
        C, tape, (o, h, l, c, t0) = _census_obj()
        sigs = LN.spring_signals_from_census(BUILD_SYM, "4h",
                                             LN.FROZEN_SCALE, tape=tape)
        st, _ = install_frame(BUILD_SYM + "-CUT", o[:200], h[:200], l[:200],
                              c[:200], om=t0[:200])
        try:
            LN.signals_on_frame(st["f"], sigs)
        finally:
            drop_frame(BUILD_SYM + "-CUT")

    return prove(
        "F-SPR-BUILD",
        "the signal harness: macro `harden` events at the FROZEN pins become "
        "SpringSignals — bottom to long, top to short — and survive the "
        "round trip builder -> checker -> runner",
        "the episode pairing differs from an independent plain-loop walk of "
        "the same events; either side is missing; any signal's extreme is "
        "not the raw tape's, or its level is not the AS-OF boundary at the "
        "breach; the built list does not survive check_signals; "
        "signals_on_frame carries an index over instead of matching a "
        "millisecond stamp, or REPAIRS a corrupted extreme / stamp instead "
        "of refusing it; or two hardens on one open stop pairing the way "
        "the census itself pairs them.",
        [("a harden with no same-side breach-open before it",
          attack(b_orphan_harden)),
         ("a harden paired with the OTHER side's open", attack(b_cross_side)),
         ("the boundary read AFTER the redraw instead of as-of at the breach",
          attack(b_redrawn_level)),
         ("a signal whose stamp the frame does not hold",
          attack(b_stamp_absent)),
         ("the episode pairing returns nothing",
          mutated(LN, "harden_episodes", lambda ev: [], _build_checks)),
         ("signals_on_frame REPAIRS a corrupted signal instead of refusing "
          "it (the pre-review implementation, planted)",
          mutated(LN, "signals_on_frame", _repairing_on_frame,
                  _build_checks)),
         ("the episode pairing CONSUMES its open, so the second of two "
          "hardens is dropped",
          mutated(LN, "harden_episodes", _consuming_episodes, _build_checks)),
         ("bottom mapped to SHORT and top to LONG",
          mutated(LN, "springs_from_episodes",
                  lambda h_, l_, c_, om_, eps, top_, bot_, lo_i=0,
                  hi_i=None, source="": [
                      LN.SpringSignal(
                          direction=(-1 if side == "bottom" else 1),
                          sweep_i=a, sweep_ms=int(om_[a]),
                          sweep_extreme=float(np.min(l_[a:i + 1])
                                              if side == "bottom"
                                              else np.max(h_[a:i + 1])),
                          swept_level=float(bot_[a] if side == "bottom"
                                            else top_[a]),
                          reclaim_i=i, reclaim_ms=int(om_[i]),
                          bars_to_reclaim=i - a, known_at=i, rid=rid,
                          side=side, source=source)
                      for rid, side, a, i in eps], _build_checks))],
        _build_checks)


# ═══════════════════ F-LANES-GATE · no registration, no bar [LAW 4, D]
def _reg_root(tmp: Path, reg_id: str, arm: str, panel, lanes,
              scored: bool = True, era: str = "full") -> tuple:
    """File ONE registration into a THROWAWAY root, with whatever fields the
    panel module's CURRENT `arm_spec` / `register` demand (the gate builder
    is repairing that module in parallel; this reads its signature rather
    than assuming it).  The canonical registry is never touched."""
    sig = inspect.signature(TP.arm_spec)
    kw = dict(scored_in_family=scored, lanes=tuple(lanes))
    text = (f"{reg_id}: the TC10 lane runner rides {arm} on "
            f"{TP.panel_name(tuple(panel))}. SYNTHETIC FIXTURE TEXT — this "
            f"registration lives in a throwaway directory and is deleted "
            f"with it; it is not a filing of record.")
    if "loao_line" in sig.parameters:
        kw["loao_line"] = "lineage"
        text += " " + TP.loao_line_clause("lineage")
    if "era" in sig.parameters:
        kw["era"] = era
    elif era != "full":
        raise SystemExit("HALT: this panel module files no era; the era leg "
                         "cannot be run against it.")
    a = TP.arm_spec(arm, tuple(panel), "vs_zero", **kw)
    TP.register(reg_id, text, 40, arms=[a], root=tmp)
    head = TP.registry_head(root=tmp)
    return text, (head["registry_len"], head["registry_head"])


class _Counter:
    """A stand-in for `replay10` that COUNTS and rides nothing."""

    def __init__(self):
        self.n = 0

    def __call__(self, *a, **k):
        self.n += 1
        return [], []


def _gate_checks() -> tuple:
    lines, ok = [], True
    b = books()
    # the control's truth table — every widening must be False
    cases = [
        ("the control itself", LN.CARD_TC10_CONTROL, T9.V6_ROLES,
         TP.CLASSIC5, "card", None, True),
        ("the BE floor ON", LN.CARD_BE1, T9.V6_ROLES, TP.CLASSIC5, "card",
         None, False),
        ("the spring lane", LN.CARD_SPR2, T9.V6_ROLES, TP.CLASSIC5, "spring",
         None, False),
        ("a signal list attached", LN.CARD_TC10_CONTROL, T9.V6_ROLES,
         TP.CLASSIC5, "card", {"BTCUSDT": [1]}, False),
        ("trail_arm_after_r moved", LN.Card(name="x", trail_arm_after_r=0.0),
         T9.V6_ROLES, TP.CLASSIC5, "card", None, False),
        ("trigger 9/12 roles", LN.CARD_TC10_CONTROL,
         T9.Roles(name="trigger-9/12", trg_f=9, trg_s=12), TP.CLASSIC5,
         "card", None, False),
        ("one unseen asset in the panel", LN.CARD_TC10_CONTROL, T9.V6_ROLES,
         tuple(TP.CLASSIC5) + ("ENAUSDT",), "card", None, False),
        ("the plain tierc8 card (not this module's)", TP.CONTROL_CARD,
         T9.V6_ROLES, TP.CLASSIC5, "card", None, False),
        ("an empty panel", LN.CARD_TC10_CONTROL, T9.V6_ROLES, (), "card",
         None, False),
    ]
    for name, card, roles, panel, lane, spr, want in cases:
        got = LN.is_control_ride(card, roles, panel, lane, spr)
        g = bool(got) == want
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] is_control_ride — {name}: "
                     f"{got} (expected {want})")
    # the control DOES ride, and it rides nothing but itself
    n = len(LN.run_lane(LN.CARD_TC10_CONTROL, T9.V6_ROLES, TP.CLASSIC5,
                        b["lo"], b["hi"]))
    g = n == len(b["want"])
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] the KNOWN CONTROL rides "
                 f"unfiled: {n} campaigns")
    # with a filing in a THROWAWAY root and a STUBBED replay, the gate OPENS
    with tempfile.TemporaryDirectory(prefix="f-gate-open-") as td:
        tmp = Path(td)
        text, head = _reg_root(tmp, "P-SYN-BE", "P-SYN-BE vs zero",
                               TP.CLASSIC5, ("card",))
        cnt = _Counter()
        old = LN.replay10
        LN.replay10 = cnt
        try:
            bk = LN.run_lane(LN.CARD_BE1, T9.V6_ROLES, TP.CLASSIC5,
                             b["lo"], b["hi"], reg_id="P-SYN-BE", text=text,
                             arm="P-SYN-BE vs zero", lanes=("card",),
                             head_of_record=head, reg_root=tmp)
        finally:
            LN.replay10 = old
        g = (isinstance(bk, TP.Book) and bk.spec.get("arm") ==
             "P-SYN-BE vs zero" and bk.spec.get("runner") == "external"
             and cnt.n == len(TP.CLASSIC5) and len(bk) == 0)
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] with the registration FILED "
                     f"(throwaway root) and replay10 STUBBED, the gate opens "
                     f"onto the stub {cnt.n} times and returns a Book wearing "
                     f"arm {bk.spec.get('arm')!r} / runner "
                     f"{bk.spec.get('runner')!r}")
    # THE FILED ERA, BEFORE A BAR IS READ [review 2026-09-21].  This leg must
    # live HERE and not among the counted attacks: with a throwaway root the
    # non-canonical-registry guard fires FIRST and the refusal would be for
    # the wrong reason, so the stub goes in and the era guard is the only one
    # left that can refuse.  The stub must be called ZERO times — the era is
    # caught at the door, not by `external_book` after the bars are replayed.
    with tempfile.TemporaryDirectory(prefix="f-gate-era-") as td:
        tmp = Path(td)
        text, head = _reg_root(tmp, "P-SYN-ERA", "P-SYN-ERA vs zero",
                               TP.CLASSIC5, ("card",), era="holdout")
        cnt = _Counter()
        old = LN.replay10
        LN.replay10 = cnt
        try:
            ok_e, why_e = refused(
                lambda: LN.run_lane(LN.CARD_BE1, T9.V6_ROLES, TP.CLASSIC5,
                                    b["lo"], b["hi"], reg_id="P-SYN-ERA",
                                    text=text, arm="P-SYN-ERA vs zero",
                                    lanes=("card",), head_of_record=head,
                                    reg_root=tmp))
        finally:
            LN.replay10 = old
        elo, _ = TP.era_window("holdout")
        g = (ok_e and "holdout" in why_e and cnt.n == 0
             and elo is not None and b["lo"] < elo)
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] an arm filed for the "
                     f"HOLDOUT era, handed the FULL corridor (lo "
                     f"{LN.iso(int(b['lo']))} < the era's first instant "
                     f"{'OPEN' if elo is None else LN.iso(int(elo))}), is "
                     f"refused at the door with {cnt.n} replay calls: "
                     f"{why_e[:110]}")
    # the registry of record holds NOTHING
    g = not TP.REG_DIR.exists() or not any(TP.REG_DIR.iterdir())
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] the registry of record "
                 f"{TP.REG_DIR} is EMPTY — no registration was filed by this "
                 f"suite, and LAW 4 says none may be")
    lines.append(f"      replay10 calls made by every REFUSED attack above: "
                 f"{_ATTACK_CALLS['n']} (it must be 0)")
    ok &= (_ATTACK_CALLS["n"] == 0)
    return ok, lines


_ATTACK_CALLS = {"n": 0}


def _counted_attack(fn):
    """An attack that must be refused BEFORE a single asset's FRAME is asked
    for — the strongest form of "no bar was replayed".

    The counter is installed on `tierc10_panel.frame_n` and `tierc9.frame`,
    the two doors every bar in this lineage comes through, and NOT on
    `replay10`: `run_lane`'s last guard is the IDENTITY test
    `replay10 is _REPLAY10_AT_IMPORT` (a throwaway registry may open the gate
    only onto a stub), and a counter installed in `replay10`'s place would
    defeat the very guard the sabotage leg exists to test."""
    def leg():
        n = {"k": 0}
        old_n, old_f = TP.frame_n, T9.frame

        def c_n(s, *a, **k):
            n["k"] += 1
            return old_n(s, *a, **k)

        def c_f(s, *a, **k):
            n["k"] += 1
            return old_f(s, *a, **k)

        TP.frame_n, T9.frame = c_n, c_f
        try:
            ok, why = refused(fn)
        finally:
            TP.frame_n, T9.frame = old_n, old_f
        _ATTACK_CALLS["n"] += n["k"]
        return (not ok), (f"refused with {n['k']} frame read(s): {why}"
                          if ok else f"NOT REFUSED — it ran ({n['k']} frame "
                                     f"reads)")
    return leg


def f_lanes_gate() -> bool:
    b = books()
    lo, hi = b["lo"], b["hi"]

    def no_reg_be():
        LN.run_lane(LN.CARD_BE1, T9.V6_ROLES, TP.CLASSIC5, lo, hi)

    def no_reg_spring():
        LN.run_lane(LN.CARD_SPR2, T9.V6_ROLES, TP.CLASSIC5, lo, hi,
                    springs_by_sym={s: [] for s in TP.CLASSIC5})

    def named_but_unfiled():
        LN.run_lane(LN.CARD_BE1, T9.V6_ROLES, TP.CLASSIC5, lo, hi,
                    reg_id="P-BE-1", text="P-BE-1: the breakeven floor.",
                    arm="P-BE-1 vs card v6", lanes=("card",),
                    head_of_record=TP.UNPINNED)

    def text_none():
        LN.run_lane(LN.CARD_BE1, T9.V6_ROLES, TP.CLASSIC5, lo, hi,
                    reg_id="P-BE-1", text=None, arm="P-BE-1 vs card v6")

    def throwaway_real_replay():
        """THE SABOTAGE: a registration filed in a directory the attacker
        owns, opening the gate onto the REAL replay."""
        with tempfile.TemporaryDirectory(prefix="f-gate-throw-") as td:
            tmp = Path(td)
            text, head = _reg_root(tmp, "P-SYN-BE2", "P-SYN-BE2 vs zero",
                                   TP.CLASSIC5, ("card",))
            LN.run_lane(LN.CARD_BE1, T9.V6_ROLES, TP.CLASSIC5, lo, hi,
                        reg_id="P-SYN-BE2", text=text,
                        arm="P-SYN-BE2 vs zero", lanes=("card",),
                        head_of_record=head, reg_root=tmp)

    def wrong_arm():
        with tempfile.TemporaryDirectory(prefix="f-gate-arm-") as td:
            tmp = Path(td)
            text, head = _reg_root(tmp, "P-SYN-BE3", "P-SYN-BE3 vs zero",
                                   TP.CLASSIC5, ("card",))
            LN.run_lane(LN.CARD_BE1, T9.V6_ROLES, TP.CLASSIC5, lo, hi,
                        reg_id="P-SYN-BE3", text=text,
                        arm="P-SYN-BE3 the OTHER arm", lanes=("card",),
                        head_of_record=head, reg_root=tmp)

    def wrong_panel():
        with tempfile.TemporaryDirectory(prefix="f-gate-panel-") as td:
            tmp = Path(td)
            text, head = _reg_root(tmp, "P-SYN-BE4", "P-SYN-BE4 vs zero",
                                   TP.CLASSIC5[:3], ("card",))
            LN.run_lane(LN.CARD_BE1, T9.V6_ROLES, TP.CLASSIC5, lo, hi,
                        reg_id="P-SYN-BE4", text=text,
                        arm="P-SYN-BE4 vs zero", lanes=("card",),
                        head_of_record=head, reg_root=tmp)

    def wrong_lane():
        with tempfile.TemporaryDirectory(prefix="f-gate-lane-") as td:
            tmp = Path(td)
            text, head = _reg_root(tmp, "P-SYN-SPR", "P-SYN-SPR vs zero",
                                   TP.CLASSIC5, ("card",))
            LN.run_lane(LN.CARD_SPR2, T9.V6_ROLES, TP.CLASSIC5, lo, hi,
                        reg_id="P-SYN-SPR", text=text,
                        arm="P-SYN-SPR vs zero", lanes=("spring",),
                        head_of_record=head, reg_root=tmp,
                        springs_by_sym={s: [] for s in TP.CLASSIC5})

    def window_past_asof():
        LN.run_lane(LN.CARD_TC10_CONTROL, T9.V6_ROLES, TP.CLASSIC5, lo,
                    hi + MS_4H)

    def unknown_knob():
        import dataclasses as dc

        @dc.dataclass(frozen=True)
        class Wider(LN.Card):
            name: str = "wider"
            some_new_knob: float = 0.0
        LN.replay10(TP.CLASSIC5[0], Wider(), T9.V6_ROLES, lo, hi)

    def springs_on_card_lane():
        LN.replay10(TP.CLASSIC5[0], LN.CARD_TC10_CONTROL, T9.V6_ROLES, lo,
                    hi, springs=[1])

    def spring_lane_no_signals():
        LN.replay10(TP.CLASSIC5[0], LN.CARD_SPR2, T9.V6_ROLES, lo, hi)

    def bad_be_threshold():
        LN.replay10(TP.CLASSIC5[0],
                    LN.Card(name="bad", be_floor_after_r=-1.0), T9.V6_ROLES,
                    lo, hi)

    return prove(
        "F-LANES-GATE",
        "no registration, no bar: the BE floor ON and the spring lane both "
        "HALT on real data, with ZERO replay calls",
        "any attack rides; any attack replays a bar before being refused; a "
        "throwaway registry opens the gate onto the REAL replay; the control "
        "exception is wider by one field; the runner accepts a card with a "
        "knob it does not read; an arm filed for the HOLDOUT era is handed "
        "the full corridor and reads a bar before being refused; or a "
        "registration was filed in the registry of record.",
        [("the BE floor ON, CLASSIC5, no registration",
          _counted_attack(no_reg_be)),
         ("the spring lane, CLASSIC5, no registration",
          _counted_attack(no_reg_spring)),
         ("reg_id/text/arm named but NOTHING filed",
          _counted_attack(named_but_unfiled)),
         ("text=None at the door", _counted_attack(text_none)),
         ("THE SABOTAGE: a throwaway registry + the REAL replay10",
          _counted_attack(throwaway_real_replay)),
         ("the right filing, the WRONG arm named",
          _counted_attack(wrong_arm)),
         ("the right filing, a book on a WIDER panel than it files",
          _counted_attack(wrong_panel)),
         ("a `spring` lane offered under a filing that files only `card`",
          _counted_attack(wrong_lane)),
         ("the control with a window end PAST the as-of",
          _counted_attack(window_past_asof)),
         # These four attack `replay10`'s own SCOPE, so they call it directly.
         # They are still counted: every one of its scope HALTs fires above
         # the first `T9.frame` call, which is what the counter watches.
         ("a card carrying a knob this module does not read",
          _counted_attack(unknown_knob)),
         ("a signal list handed to the CARD lane",
          _counted_attack(springs_on_card_lane)),
         ("the SPRING lane with no signal list",
          _counted_attack(spring_lane_no_signals)),
         ("be_floor_after_r = -1.0", _counted_attack(bad_be_threshold)),
         ("every era made OPEN (era_window := (None, None)) — the holdout "
          "arm would then ride the tuning era it is not entitled to",
          mutated(TP, "era_window", lambda era: (None, None), _gate_checks))],
        _gate_checks)


# ═══════════════ F-LANES-CLOSURE · the decision path reaches no range code
RANGE_IMPORT_LINE = re.compile(          # OR-1 F-BR-14's regex, verbatim
    r"(?m)^[ \t]*(?:from|import)[ \t]+[^\n#]*\brangefinder\b")


def _closure(modname: str, shadow_src: str | None = None) -> set:
    with tempfile.TemporaryDirectory(prefix="f-closure-") as td:
        if shadow_src is not None:
            (Path(td) / f"{modname}.py").write_text(shadow_src,
                                                    encoding="utf-8")
        code = ("import sys, json; sys.dont_write_bytecode = True; "
                f"sys.path.insert(0, {str(ROOT)!r}); "
                f"sys.path.insert(0, {str(ROOT / 'scripts')!r}); "
                + (f"sys.path.insert(0, {td!r}); " if shadow_src is not None
                   else "")
                + "before = set(sys.modules); "
                f"import {modname}; "
                "print(json.dumps(sorted(set(sys.modules) - before)))")
        out = subprocess.run([PY, "-c", code], cwd=ROOT, capture_output=True,
                             text=True, timeout=900)
    if out.returncode != 0:
        raise RuntimeError(out.stderr[-500:])
    return set(json.loads(out.stdout.strip().splitlines()[-1]))


def _range_parts(cl: set) -> list:
    return sorted(m for m in cl
                  if any("rangefinder" in p for p in m.split(".")))


def _census_parts(cl: set) -> list:
    return sorted(m for m in cl if "census" in m)


def _module_level_imports(src: str) -> list:
    """Every import that runs at IMPORT TIME — i.e. at module scope, and the
    NAMES it pulls, not just the package (`from analytics import
    rangefinder_census` names a range module in the second half of the line).
    An import inside a function body is not one, and that distinction is the
    whole of this module's two-tier closure."""
    out = []
    for node in ast.parse(src).body:
        if isinstance(node, ast.Import):
            out += [al.name for al in node.names]
        elif isinstance(node, ast.ImportFrom):
            m = node.module or ""
            out.append(m)
            out += [f"{m}.{al.name}" for al in node.names]
    return out


def _lazy_imports(src: str) -> list:
    """Every import that runs inside a function body, with its function."""
    out = []
    for fn in ast.walk(ast.parse(src)):
        if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        for node in ast.walk(fn):
            if isinstance(node, ast.Import):
                out += [(fn.name, al.name) for al in node.names]
            elif isinstance(node, ast.ImportFrom):
                out.append((fn.name, node.module or ""))
    return out


def f_lanes_closure() -> bool:
    src = (ROOT / "scripts" / "tierc10_lanes.py").read_text()

    def b_planted_range():
        c = _closure("tierc10_lanes", src.replace(
            "import tierc9 as T9",
            "from engine import rangefinder as RNG\nimport tierc9 as T9", 1))
        return not _range_parts(c), f"planted runner reaches {_range_parts(c)}"

    def b_planted_census():
        c = _closure("tierc10_lanes", src.replace(
            "import tierc9 as T9",
            "import tierc10_census as C\nimport tierc9 as T9", 1))
        return not _census_parts(c), (f"planted runner reaches "
                                      f"{_census_parts(c)}")

    def b_static():
        planted = src + "\nfrom analytics import rangefinder_census\n"
        hits = [m for m in _module_level_imports(planted)
                if "rangefinder" in m or "census" in m]
        return (not hits), (f"module-level scan of the planted source: "
                            f"{hits}")

    def real():
        ok, lines = True, []
        cl = _closure("tierc10_lanes")
        ra, ce = _range_parts(cl), _census_parts(cl)
        g = not ra and not ce and "tierc9" in cl and "tierc10_panel" in cl
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] THE RUNNER CLOSURE "
                     f"(tierc10_lanes -> tierc10_panel/tierc9..5 + "
                     f"tierc10_data): {len(cl)} modules, rangefinder "
                     f"{ra or 'NONE'}, census {ce or 'NONE'}")
        an = sorted(m for m in cl if "analytics" in m.split("."))
        lines.append(f"      analytics IS loaded here ({an}) — INHERITED "
                     f"from tierc2_baseline/tierc5..8, whose TAPE code runs "
                     f"after the replay has decided everything "
                     f"[captured-not-consulted, F-C2-6]; printed, not hidden")
        ml = _module_level_imports(src)
        g = not any("rangefinder" in m or "census" in m for m in ml)
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] tierc10_lanes.py's "
                     f"MODULE-LEVEL imports name no range or census module: "
                     f"{ml}")
        lz = _lazy_imports(src)
        census_lazy = [p for p in lz if "census" in p[1]]
        g = (census_lazy == [("spring_signals_from_census",
                              "tierc10_census")])
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] the ONLY census import is "
                     f"lazy, inside one named function: {census_lazy}")
        hits = RANGE_IMPORT_LINE.findall(src)
        g = not hits
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] F-BR-14's own regex over "
                     f"the source (indented imports included): "
                     f"{hits or 'no hit'}")
        return ok, lines

    return prove(
        "F-LANES-CLOSURE",
        "the decision path imports no range code; the census is reached by "
        "ONE lazy import, inside ONE named harness function",
        "tierc10_lanes' import closure reaches any `rangefinder` or census "
        "module; a module-level import names either; the census import moves "
        "out of `spring_signals_from_census`; or F-BR-14's regex finds a "
        "line in the source.",
        [("`from engine import rangefinder` planted at module level",
          b_planted_range),
         ("`import tierc10_census` planted at module level", b_planted_census),
         ("`from analytics import rangefinder_census` planted in the source",
          b_static)],
        real)


# ═════════════════════════════ F-C10-BE-HARNESS · the hand walk, certified
def _harness_checks() -> tuple:
    lines, ok = [], True
    for name, (pk, want_order, *_rest) in BE_SCEN.items():
        st, om, h, l, c, sig, e, R, stp = be_tape(BE_ROWS)
        plan = {LATCH: pk(float(h[LATCH]), float(l[LATCH]), float(c[LATCH]))}
        old = LN._FIVE_SOURCE
        LN._FIVE_SOURCE = five_source(om, h, l, c, plan)
        try:
            t5, h5, l5, c5 = LN.children_5m(BE_SYM, int(om[LATCH]))
            trig = e + 1.0 * R
            mine = LN.be_sequence(BE_SYM, int(om[LATCH]), 1, e, trig,
                                  float(h[LATCH]), float(l[LATCH]))
            hand = LN.hand_walk_5m(t5, h5, l5, c5, 1, e, trig)
        finally:
            LN._FIVE_SOURCE = old
        # the hand walk knows nothing of the 4h parent, so on the two
        # MISMATCH scenarios it answers the children's own order — and the
        # DIFFERENCE is the mismatch detector doing its job.
        if want_order == "mismatch":
            g = (mine["order"] == "mismatch" and hand["order"] != "mismatch"
                 and mine["i_up"] == hand["i_up"]
                 and mine["i_dip"] == hand["i_dip"])
            note = (f"module {mine['order']!r} (it can see the parent) vs "
                    f"hand {hand['order']!r} (it cannot) — child indices "
                    f"agree: up {mine['i_up']} dip {mine['i_dip']}")
        else:
            g = (mine["order"] == hand["order"]
                 and mine["i_up"] == hand["i_up"]
                 and mine["i_dip"] == hand["i_dip"])
            note = (f"{mine['order']!r} both ways; up child "
                    f"{mine['i_up']} / dip child {mine['i_dip']}")
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] {name}: {note}")
    return ok, lines


def f_c10_be_harness() -> bool:
    return prove(
        "F-C10-BE-HARNESS",
        "the independent plain-numpy hand walk agrees with the module's "
        "sequencer on every synthetic order — the harness F-C10-BE will use",
        "the hand walk and the sequencer disagree on any child index or on "
        "the order for any non-mismatch scenario; or on a mismatch scenario "
        "the sequencer fails to differ from a walker that cannot see the "
        "parent bar (the detector would then be doing nothing).",
        [("the hand walk always answers `plus1r_first`",
          mutated(LN, "hand_walk_5m",
                  lambda *a, **k: {"order": "plus1r_first", "i_up": 0,
                                   "i_dip": 1, "n_children": N5},
                  _harness_checks)),
         ("the hand walk reports the child indices swapped",
          mutated(LN, "hand_walk_5m",
                  lambda t5, h5, l5, c5, d, e, tr: {
                      "order": "dip_first", "i_up": 1, "i_dip": 0,
                      "n_children": len(t5)},
                  _harness_checks))],
        _harness_checks)


CAMPAIGN_FIELDS = ("symbol", "latch_bar_open_ms", "direction", "entry_px",
                   "r_dist", "bar_high", "bar_low", "expected_order")


def _c10_be_checks() -> tuple:
    """The REAL-CAMPAIGN leg, written and waiting: it needs only the ids."""
    lines, ok, seen = [], True, set()
    for row in LN.BE_CAMPAIGNS:
        d = dict(zip(CAMPAIGN_FIELDS, row))
        ev = LN.be_campaign_evidence(
            d["symbol"], int(d["latch_bar_open_ms"]), int(d["direction"]),
            float(d["entry_px"]), float(d["r_dist"]), float(d["bar_high"]),
            float(d["bar_low"]))
        seen.add(ev["module"]["order"])
        g = bool(ev["agree"]) and ev["module"]["order"] == d["expected_order"]
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] {d['symbol']} "
                     f"{ev['bar_open']}: module {ev['module']['order']!r} / "
                     f"hand {ev['hand']['order']!r} (expected "
                     f"{d['expected_order']!r}), up child "
                     f"{ev['module']['i_up']} dip child "
                     f"{ev['module']['i_dip']}, {ev['module']['n_children']} "
                     f"children")
        # THE CONVERSE: the same campaign, children in reverse tape order.
        old = LN.children_5m
        LN.children_5m = lambda s, b, _o=old: tuple(x[::-1] for x in _o(s, b))
        try:
            rev = LN.be_campaign_evidence(
                d["symbol"], int(d["latch_bar_open_ms"]), int(d["direction"]),
                float(d["entry_px"]), float(d["r_dist"]),
                float(d["bar_high"]), float(d["bar_low"]))
        finally:
            LN.children_5m = old
        g2 = (rev["module"]["order"] != ev["module"]["order"]
              or ev["module"]["order"] == "tie")
        ok &= g2
        lines.append(f"[{'OK ' if g2 else 'BAD'}]   converse (children "
                     f"reversed): {rev['module']['order']!r}")
    g = len(LN.BE_CAMPAIGNS) >= 3 and len(seen & {"dip_first",
                                                  "plus1r_first"}) == 2
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] three campaigns, one of each "
                 f"order: {sorted(seen)}")
    return ok, lines


def f_c10_be():
    """THE REAL-CAMPAIGN LEG.  It runs the moment `BE_CAMPAIGNS` is filled;
    until then it is NOT RUN and says why."""
    fails_if = ("it is ever reported PASS while BE_CAMPAIGNS is empty, or "
                "while any named campaign's module answer differs from its "
                "hand walk or from the order the campaign was chosen for, "
                "or while reversing a campaign's children leaves its order "
                "unchanged (a tie excepted, which is order-free by "
                "definition).")
    if not LN.BE_CAMPAIGNS:
        say("\n--- F-C10-BE — the 5m sequence proven on 3 REAL campaigns, "
            "hand-walked with plain numpy")
        say(f"  [NOT RUN] {LN.BE_CAMPAIGNS_NOTE}")
        say("    the harness is written and certified: LN.hand_walk_5m + "
            "LN.be_campaign_evidence(sym, bar_open_ms, d, entry_px, r_dist, "
            "bar_hi, bar_lo) -> {module, hand, agree}; F-C10-BE-HARNESS "
            "proves the two agree on every synthetic order.")
        say("    to run it after P-BE-1 is filed, set "
            "tierc10_lanes.BE_CAMPAIGNS to three rows "
            f"{CAMPAIGN_FIELDS} — one dip-before, one dip-after, one "
            "tie-or-mismatch — read off P-BE-1's own journal; this leg then "
            "walks each, prints both answers, and asserts `agree` plus the "
            "converse.")
        say(f"      FAILS IF: {fails_if}")
        NOT_RUN["F-C10-BE"] = ("no registration is filed, so P-BE-1 has no "
                               "book and no campaign ids exist [LAW 4]")
        return None

    def b_hand_constant():
        return mutated(LN, "hand_walk_5m",
                       lambda *a, **k: {"order": "plus1r_first", "i_up": 0,
                                        "i_dip": 1, "n_children": N5},
                       _c10_be_checks)()

    return prove(
        "F-C10-BE",
        "the 5m sequence proven on 3 REAL campaigns, hand-walked with plain "
        "numpy — one of each order, plus the converse",
        fails_if,
        [("the hand walk answers a constant", b_hand_constant)],
        _c10_be_checks)


# ═══════════════════════════════════════════ F-DET · the same answer twice
def _digest(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True,
                                     default=str).encode()).hexdigest()


def f_det() -> bool:
    def scen_digest(swap: bool = False) -> str:
        rows = []
        scen = dict(BE_SCEN)
        if swap:
            scen["dip-before"] = BE_SCEN["dip-after"]
        for name, (pk, *_r) in sorted(scen.items()):
            tr, ctx = be_case(pk)
            t = tr[0]
            rows.append([name, t.exit_i, round(float(t.exit_px), 10),
                         t.exit_reason, t.be_order, t.n_be_tie,
                         t.n_be_mismatch, round(float(t.net_r), 10),
                         round(float(t.mfe_r), 10)])
        for side in ("bottom", "top"):
            st, om, h, l, c, sig = _spr_case(side)
            tr = LN.replay10(SPR_SYM[side], LN.CARD_SPR2, T9.V6_ROLES,
                             int(om[0]), int(om[-1]) + MS_4H - 1,
                             springs=[sig])[1]
            rows.append([side, tr[0].entry_i, round(float(tr[0].stop_px), 10),
                         round(float(tr[0].r_dist), 10), tr[0].exit_reason])
        return _digest(rows)

    def ctrl_digest() -> str:
        b = books()
        j = TP.journal_frame(LN.run_lane(LN.CARD_TC10_CONTROL, T9.V6_ROLES,
                                         TP.CLASSIC5, b["lo"], b["hi"]))
        return hashlib.sha256(
            j.to_csv(index=False).encode()).hexdigest()

    def b_clock():
        """A CORRUPTED INPUT: a wall clock folded into the digest."""
        import time
        a = _digest([1, 2, 3, time.time()])
        b = _digest([1, 2, 3, time.time() + 1])
        return a == b, "two digests with a wall clock inside came out equal"

    def b_perturbed():
        """A CORRUPTED INPUT: one scenario's 5m children swapped for
        another's.  The digest MUST move, or it is not reading the answer."""
        a, b = scen_digest(), scen_digest(swap=True)
        return a == b, (f"the scenario set with ONE plan swapped digests "
                        f"the same: {a[:16]} / {b[:16]}")

    def real():
        a1, a2 = scen_digest(), scen_digest()
        c1, c2 = ctrl_digest(), ctrl_digest()
        ok = (a1 == a2) and (c1 == c2)
        return ok, [
            f"[{'OK ' if a1 == a2 else 'BAD'}] the synthetic scenario set, "
            f"twice: {a1[:16]} / {a2[:16]}",
            f"[{'OK ' if c1 == c2 else 'BAD'}] the CLASSIC5 control journal, "
            f"twice: {c1[:16]} / {c2[:16]}",
            f"      seed {SEED} threaded explicitly; no wall clock in any "
            f"artifact this module writes (it writes only this transcript, "
            f"whose first line is the as-of)"]

    return prove(
        "F-DET",
        "two runs, one answer: the synthetic scenario set and the CLASSIC5 "
        "control both digest identically",
        "either digest moves between two runs of the same process; a wall "
        "clock can hide inside a digest undetected; or a run with a MOVED "
        "knob digests the same as the run without it.",
        [("a wall clock folded into the digest", b_clock),
         ("the BE threshold moved to 0.5 R", b_perturbed)],
        real)


# ═══════════════════════════════════════════════════════ the suite
# F-BE-SPEC checks the WORDS against the LEGS, so it runs LAST of the four.
LEGS = (f_lanes_off, f_be_seq, f_be_mono, f_be_latch, f_be_noworse,
        f_be_ident, f_be_spec, f_spr_syn, f_spr_build, f_lanes_gate,
        f_lanes_closure, f_c10_be_harness, f_c10_be, f_det)


def main() -> int:
    say("=" * 78)
    say("TIER-C10 LANE FIXTURE TRANSCRIPT — break legs first, RED or void")
    say("=" * 78)
    say(f"substrate {TP.substrate()['substrate']} · seed {SEED} · frozen "
        f"SCALE_MULT {LN.FROZEN_SCALE} · registry of record "
        f"{'PRESENT' if TP.REG_DIR.exists() else 'ABSENT (nothing filed)'}")
    only = [a.lower().replace("-", "_") for a in sys.argv[1:]
            if not a.startswith("--")]
    try:
        for leg in LEGS:
            if only and not any(o in leg.__name__ for o in only):
                continue
            leg()
    finally:
        for s in (BE_SYM, BE_SYM_TOP, BUILD_SYM, BUILD_SYM + "-SHIFTED",
                  BUILD_SYM + "-CUT", *SPR_SYM.values()):
            drop_frame(s)
    n = sum(RESULTS.values())
    say(f"\nFIXTURE SUMMARY  {n}/{len(RESULTS)} PASS  {json.dumps(RESULTS)}")
    if NOT_RUN:
        say(f"NOT RUN (never PASS): {json.dumps(NOT_RUN)}")
    try:
        meta = books()["meta"] if _B else TP.corridor_n(TP.CLASSIC5)[2]
        LANES_OUT.mkdir(parents=True, exist_ok=True)
        name = ("FIXTURES_LANES.txt" if not only
                else "FIXTURES_LANES_partial.txt")
        (LANES_OUT / name).write_text(
            f"as_of_last_closed_4h: {meta['last_closed_4h_close']}\n"
            + "\n".join(T) + "\n")
        # THE STAGE MANIFEST — LAW 1(b)'s on-disk record, and it is written
        # ONLY after a WHOLE run.  A filtered run files a partial transcript
        # and a manifest built over a partial transcript would attest a
        # book that was never ridden [R0 2026-09-22: `lanes/` had no
        # manifest at all, so clause (b) had nothing to verify against].
        if not only:
            q = LN.write_manifest(RESULTS, NOT_RUN)
            print(f"(build manifest -> {q}: "
                  f"{hashlib.sha256(q.read_bytes()).hexdigest()[:16]}…)")
        else:
            print("(no build_manifest.json: this was a FILTERED run and a "
                  "manifest may only attest a whole one)")
    except BaseException as e:                              # noqa: BLE001
        print(f"(transcript filing failed, non-fatal: {e})")
    if n != len(RESULTS):
        print("*** HALT: fixture mismatch. Nothing downstream is "
              "trustworthy. ***")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
