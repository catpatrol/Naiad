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

LAW 4 BINDS THESE FIXTURES TOO.  UNTIL 371123f the only trade book ridden on
real bars was the KNOWN CONTROL — card v6, every knob at its default,
CLASSIC5 — ridden to prove it is UNCHANGED.  SINCE P-BE-1 AND P-SPR-2 WERE
FILED THERE IS EXACTLY ONE MORE, and it comes through the FILED DOOR
(`run_lane` -> TP.require_arm with the text of record and the pinned head ->
TP.external_book): F-C10-BE-CENSUS rides P-BE-1's SCORED arm A1 to read its
LATCH BARS' 5m ORDER — a sequencing fact, not an outcome — and the suite
files BE_LATCH_CENSUS.json with identity, class and agreement flags only.
No exit or outcome field is read into it, no outcome sum is computed or
printed, TP.score is never called and no .scored.json is written.  (F-C10-BE
reports the Tier-E arms' journal ORDERS beside it, through the same door,
report-only.)  Every OTHER breakeven or spring campaign in this file rides a
SYNTHETIC 4h + 5m tape pair built here, under a symbol that is not an asset,
installed into the lineage's frame memo and torn down in `finally`.  No
unseen asset's price is read.  This suite files NO registration in the
registry of record (the six of record were filed by Stage B at 371123f);
the gate legs file into throwaway temp roots and delete them, and
F-LANES-GATE proves no throwaway line ever lands in the canonical registry.
Every attack on the gate is COUNTED against a frame counter that must read
ZERO.

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


def be_tape(rows, side: str = "bottom", sym: str | None = None) -> tuple:
    """The spring base + `rows` of (favourable, adverse, close) offsets in R.

    `side="bottom"` is the LONG tape every leg written before 2026-09-22
    rides, and its arithmetic is UNCHANGED (`d == 1` collapses every term
    below to what was there before), which is why those legs' transcript
    lines are byte-identical across this edit.  `side="top"` is the MIRROR:
    the same rows, read as a SHORT — the favourable offset becomes the bar's
    LOW and the adverse offset its HIGH — so one authored row set proves both
    directions instead of two hand-tuned ones.  `sym` installs the tape
    under another SYNTHETIC name (F-C10-BE-RULE rides ten at once).

    R is NOT known before the base exists (it comes from the sweep extreme
    and the ATR at the reclaim bar, neither of which any later bar can move),
    so the base is built and measured FIRST and the ride bars are authored
    against the measured R.  That is a construction order, not a fit: nothing
    downstream of bar `BASE_BARS + 3` can change `entry`, `stop` or `R`, and
    the real leg asserts exactly that by re-measuring them on the full tape.
    """
    sym, d = (sym or BE_SYM_OF[side]), (1 if side == "bottom" else -1)
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


# ═══════ F-LANES-GATE · the filed door, the pinned registry [LAW 4, D]
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


ERA_TAG = "[ERA-GUARD]"     # every era check below carries it, so the era
#                             mutation break can prove it went RED THERE
_GATE: dict = {}


def _stub_ride(fn) -> tuple:
    """Run `fn` with `replay10` swapped for a COUNTING stub; restore it.
    Returns (refused?, why, stub calls, fn's result or None)."""
    cnt = _Counter()
    old = LN.replay10
    LN.replay10 = cnt
    out = {}
    try:
        did, why = refused(lambda: out.update(r=fn()))
    finally:
        LN.replay10 = old
    return did, why, cnt.n, out.get("r")


def _gate_checks() -> tuple:
    lines, ok = [], True
    b = books()
    head0 = _GATE.get("head0") or TP.registry_head()
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
        lines.append(f"[{'OK ' if g else 'BAD'}] {ERA_TAG} an arm filed for "
                     f"the HOLDOUT era (throwaway root), handed the FULL "
                     f"corridor (lo {LN.iso(int(b['lo']))} < the era's first "
                     f"instant "
                     f"{'OPEN' if elo is None else LN.iso(int(elo))}), is "
                     f"refused at the door with {cnt.n} replay calls: "
                     f"{why_e[:110]}")

    # ══ POST-FILING LAW [371123f].  UNTIL THEN THIS LEG ENDED ON "the
    # ══ registry of record is EMPTY" — true before the filing, FALSE since,
    # ══ and on the first run after it the leg went RED for a claim about a
    # ══ world that no longer exists (and the era mutation below was then
    # ══ decided in advance: the checks were RED with or without it).  What
    # ══ the filing makes true is checked instead, against the TRACKED pin.
    pin = json.loads(LN.REGISTRY_PIN_PATH.read_text(encoding="utf-8"))
    pin_s = f"{int(pin['registry_len'])}:{pin['registry_head']}"
    reg_lines = [json.loads(x) for x in (TP.REG_DIR / "REGISTRY.jsonl")
                 .read_text().splitlines() if x.strip()]
    names = [ln_.get("registration") for ln_ in reg_lines]
    hd = TP.registry_head()
    g = (len(reg_lines) == int(pin["registry_len"]) == hd["registry_len"]
         == int(pin["family_m"])
         and hd["registry_head"] == pin["registry_head"]
         == reg_lines[-1].get("line_sha256")
         and names == list(pin["order_of_filing"])
         and len(set(names)) == len(names)
         and all(ln_.get("sha256") == (pin["registrations"].get(
             ln_.get("registration")) or {}).get("sha256")
                 for ln_ in reg_lines))
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] THE REGISTRY OF RECORD IS "
                 f"EXACTLY THE {pin['registry_len']} LINES PINNED in "
                 f"REGISTRY_PIN.json (m = {pin['family_m']}): chain head "
                 f"{hd['registry_len']}:{hd['registry_head'][:16]}… vs pin "
                 f"{pin_s[:18]}…; filed in order {names}; every line's "
                 f"payload sha equals its pin")
    syn_lines = [x for x in names if "SYN" in str(x).upper()]
    syn_files = sorted(p_.name for p_ in TP.REG_DIR.iterdir()
                       if "SYN" in p_.name.upper())
    hd_now = TP.registry_head()
    g = (not syn_lines and not syn_files
         and (hd_now["registry_len"], hd_now["registry_head"])
         == (head0["registry_len"], head0["registry_head"]))
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] NO THROWAWAY LINE LANDS IN THE "
                 f"REGISTRY OF RECORD: P-SYN-* lines {syn_lines or 'none'}, "
                 f"P-SYN-* files {syn_files or 'none'}, and the canonical "
                 f"head is UNMOVED across every throwaway filing of this "
                 f"leg ({head0['registry_len']}:"
                 f"{head0['registry_head'][:16]}… -> "
                 f"{hd_now['registry_len']}:{hd_now['registry_head'][:16]}…)")
    # BOTH LANE REGISTRATIONS OPEN THROUGH THE FILED DOOR — every filed arm,
    # with the text of record (REGISTRATION_TEXTS.json) and the pinned head.
    opened, why_not, scored = [], [], {}
    for reg in LN.LANE_REGS:
        try:
            txt, head = LN.filed_text(reg), LN.filed_head(reg)
            want = pin["registrations"][reg]
            if TP._sha(txt) != want["text_sha256"] \
                    or tuple(head) != (int(pin["registry_len"]),
                                       pin["registry_head"]):
                why_not.append(f"{reg}: the text or head in hand is not the "
                               f"pinned one (text {TP._sha(txt)[:12]} vs "
                               f"{want['text_sha256'][:12]}; head "
                               f"{head[0]}:{str(head[1])[:12]})")
            rec = TP.require_registered(reg, txt, head_of_record=head)
            for a_ in rec["book_spec"]["arms"]:
                gt = TP.require_arm(reg, txt, a_["arm"], tuple(a_["panel"]),
                                    lanes=tuple(a_["lanes"]),
                                    head_of_record=head)
                opened.append((reg, gt["arm"], gt["era"],
                               bool(gt["registry_head_pinned"]),
                               gt["registry_pin"]))
                if gt["scored_in_family"]:
                    scored.setdefault(reg, []).append(gt["arm"])
        except SystemExit as e:
            why_not.append(f"{reg}: {_norm(str(e))[:150]}")
    n_arms = {r_: sum(1 for x in opened if x[0] == r_) for r_ in LN.LANE_REGS}
    g = (not why_not and all(n_arms[r_] >= 1 for r_ in LN.LANE_REGS)
         and all(x[3] and x[4] == pin_s for x in opened)
         and scored.get(LN.BE1_REG) == [LN.BE1_SCORED_ARM]
         and len(scored.get(LN.SPR2_REG) or []) == 1)
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] BOTH LANE REGISTRATIONS OPEN "
                 f"THROUGH THE FILED DOOR with the text of record and the "
                 f"pinned head {pin_s[:18]}…: arms opened {n_arms}, eras "
                 f"{sorted({(x[0], x[2]) for x in opened})}, one scored arm "
                 f"each {scored}; refusals {why_not or 'none'}")
    # run_lane's OWN door opens on each SCORED arm — onto a counting stub, so
    # no bar is ridden here (P-BE-1's A1 is ridden in F-C10-BE-CENSUS).
    for reg, card, spr in ((LN.BE1_REG, LN.CARD_BE1, None),
                           (LN.SPR2_REG, LN.CARD_SPR2,
                            {s: [] for s in TP.CLASSIC5})):
        arm = (scored.get(reg) or ["<no scored arm opened>"])[0]
        lo_e, hi_e, _m = TP.corridor_era(TP.CLASSIC5, "full")
        did, why, calls, bk = _stub_ride(
            lambda reg=reg, card=card, spr=spr, arm=arm: LN.run_lane(
                card, T9.V6_ROLES, TP.CLASSIC5, lo_e, hi_e, reg_id=reg,
                text=LN.filed_text(reg), arm=arm,
                lanes=(card.lane,), head_of_record=LN.filed_head(reg),
                springs_by_sym=spr))
        g = (not did and isinstance(bk, TP.Book)
             and bk.spec.get("registration") == reg
             and bk.spec.get("arm") == arm and bk.spec.get("era") == "full"
             and calls == len(TP.CLASSIC5))
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] run_lane opens {reg}'s "
                     f"SCORED arm {arm!r} with the text of record + pinned "
                     f"head, onto the STUB ({calls} calls): "
                     + (f"a Book wearing arm {bk.spec.get('arm')!r} / era "
                        f"{bk.spec.get('era')!r}" if bk is not None
                        else f"REFUSED: {why[:110]}"))
    # THE FILED ERA AT THE DOOR, ON THE REAL FILED ERA ARMS: each handed the
    # FULL corridor must be refused before one stub call.
    for reg, arm, card, spr in (
            (LN.BE1_REG, "be-floor-1R vs card-v6 (CLASSIC5, holdout) "
                         "[Tier-E]", LN.CARD_BE1, None),
            (LN.SPR2_REG, "standalone vs zero · tuning era", LN.CARD_SPR2,
             {s: [] for s in TP.CLASSIC5})):
        era = "holdout" if "holdout" in arm else "tuning"
        did, why, calls, _bk = _stub_ride(
            lambda reg=reg, arm=arm, card=card, spr=spr: LN.run_lane(
                card, T9.V6_ROLES, TP.CLASSIC5, b["lo"], b["hi"], reg_id=reg,
                text=LN.filed_text(reg), arm=arm, lanes=(card.lane,),
                head_of_record=LN.filed_head(reg), springs_by_sym=spr))
        g = did and f"is filed for the {era!r} era" in why and calls == 0
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] {ERA_TAG} {reg}'s FILED "
                     f"{era.upper()} arm {arm!r}, handed the FULL corridor, "
                     f"is refused at the door with {calls} stub calls: "
                     f"{why[:120]}")
    # NO LANES .scored.json — scoring is B-CORE's, never this suite's.
    sj = sorted(p_.name for p_ in TP.REG_DIR.glob("*.scored.json")
                if any(p_.name.startswith(r_ + ".") for r_ in LN.LANE_REGS))
    g = not sj
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] no lanes .scored.json on file "
                 f"({sj or 'none'}) — TP.score is never called here; "
                 f"scoring is B-CORE's")
    lines.append(f"      frame reads made by every REFUSED attack above: "
                 f"{_ATTACK_CALLS['n']} (it must be 0)")
    ok &= (_ATTACK_CALLS["n"] == 0)
    return ok, lines


_ATTACK_CALLS = {"n": 0}


def _counted_attack(fn, must: str | None = None):
    """An attack that must be refused BEFORE a single asset's FRAME is asked
    for — the strongest form of "no bar was replayed".

    The counter is installed on `tierc10_panel.frame_n` and `tierc9.frame`,
    the two doors every bar in this lineage comes through, and NOT on
    `replay10`: `run_lane`'s last guard is the IDENTITY test
    `replay10 is _REPLAY10_AT_IMPORT` (a throwaway registry may open the gate
    only onto a stub), and a counter installed in `replay10`'s place would
    defeat the very guard the sabotage leg exists to test.

    `must`, when given, is a phrase the REFUSAL must carry: a refusal for
    some other reason is not the refusal the leg claims, and the leg then
    reports GREEN (VOID) rather than RED."""
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
        if ok and must and must not in why:
            return True, (f"refused for the WRONG reason (wanted "
                          f"{must!r}): {why}")
        return (not ok), (f"refused with {n['k']} frame read(s): {why}"
                          if ok else f"NOT REFUSED — it ran ({n['k']} frame "
                                     f"reads)")
    return leg


def mutated_at(obj, attr: str, wrong, checks, tag: str):
    """`mutated`, and the RED must be RED *AT* `tag`: the break is VOID
    (GREEN) unless one of the checks' BAD lines carries the tag.  A break
    whose checks were RED for some other reason proved nothing about the
    guard it names — which is how 'every era made OPEN' sat decided in
    advance while the registry check was failing on its own."""
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
        at = [ln for ln in bad if tag in ln]
        if ok or not at:
            return True, (f"NOT RED AT {tag} — ok={ok}, BAD lines "
                          f"{[x[:90] for x in bad] or 'none'}")
        return False, (f"RED AT {tag} ({len(at)} of {len(bad)} BAD lines): "
                       + at[0][:150])
    return leg


def f_lanes_gate() -> bool:
    b = books()
    lo, hi = b["lo"], b["hi"]
    _GATE["head0"] = TP.registry_head()      # BEFORE any throwaway filing
    true_text, true_head = LN.filed_text, LN.filed_head

    def no_reg_be():
        LN.run_lane(LN.CARD_BE1, T9.V6_ROLES, TP.CLASSIC5, lo, hi)

    def no_reg_spring():
        LN.run_lane(LN.CARD_SPR2, T9.V6_ROLES, TP.CLASSIC5, lo, hi,
                    springs_by_sym={s: [] for s in TP.CLASSIC5})

    def not_the_text_on_file():
        """P-BE-1 IS filed (371123f).  Offered a text that is NOT the text
        of record, the door must refuse — and the refusal must be the
        REGISTRY's 'not the text on file', not a loader's."""
        LN.run_lane(LN.CARD_BE1, T9.V6_ROLES, TP.CLASSIC5, lo, hi,
                    reg_id="P-BE-1", text="P-BE-1: the breakeven floor.",
                    arm=LN.BE1_SCORED_ARM, lanes=("card",),
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

    def _amended(reg_id, path=None):
        """A named wrong: the claim moved after it was filed."""
        return true_text(reg_id, path) + " And it will print positive."

    def _stale_head(reg_id, path=None):
        """A named wrong: the head as it stood at registry line 1 (P-GEN-1
        alone), BEFORE either lane line was filed — it cannot vouch for a
        registration filed after it."""
        first = json.loads((TP.REG_DIR / "REGISTRY.jsonl").read_text()
                           .splitlines()[0])
        return (1, str(first.get("line_sha256")))

    return prove(
        "F-LANES-GATE",
        "the filed door: P-BE-1 and P-SPR-2 open ONLY with the text of "
        "record and the pinned head, the registry of record is the six "
        "pinned lines, and every unfiled, misnamed, widened or out-of-era "
        "ride HALTs with ZERO frame reads",
        "any attack rides; any attack replays a bar before being refused; a "
        "throwaway registry opens the gate onto the REAL replay; the control "
        "exception is wider by one field; the runner accepts a card with a "
        "knob it does not read; an arm filed for the HOLDOUT (or TUNING) "
        "era is handed the full corridor and reads a bar before being "
        "refused; the registry of record is not exactly the lines pinned in "
        "REGISTRY_PIN.json (length, head, order, payload shas); a P-SYN-* "
        "throwaway line or file lands in it, or its head moves during this "
        "leg; either lane registration fails to open ANY of its filed arms "
        "through the door with the text of record and the pinned head; "
        "run_lane fails to open a scored arm onto the stub; a text that is "
        "not the text on file is refused for any reason but that one; or a "
        "lanes .scored.json exists before B-CORE.",
        [("the BE floor ON, CLASSIC5, no registration",
          _counted_attack(no_reg_be)),
         ("the spring lane, CLASSIC5, no registration",
          _counted_attack(no_reg_spring)),
         ("P-BE-1 named, with a text that is NOT the text on file",
          _counted_attack(not_the_text_on_file,
                          must="is not the text on file")),
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
         ("the text of record amended after filing (one clause appended)",
          mutated(LN, "filed_text", _amended, _gate_checks)),
         ("a STALE head pin (registry line 1, taken before either lane line "
          "was filed)",
          mutated(LN, "filed_head", _stale_head, _gate_checks)),
         ("every era made OPEN (era_window := (None, None)) — the holdout "
          "arm would then ride the tuning era it is not entitled to; RED "
          f"must be AT the era guard ({ERA_TAG})",
          mutated_at(TP, "era_window", lambda era: (None, None),
                     _gate_checks, ERA_TAG))],
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
                   "r_dist", "bar_high", "bar_low", "expected_class",
                   "journal_order")
# THE CONTRACT'S THREE CLASSES, typed HERE from P-BE-1 §9 ("one of each 5m
# order — dip-before, dip-after, and a tie or a 4h/5m mismatch") and held
# against the module's BE_REQUIRED on every run: a closing rule that quietly
# lost a class would otherwise pass a book that lacks it.
FX_REQUIRED = ("dip_before", "dip_after", "tie_or_mismatch")
FX_CLASSES = ("dip_before", "dip_after", "print_no_dip", "tie", "mismatch")
FX_DIPS = ("dip_before", "dip_after")


# ── THE FIXTURE'S OWN WALK — plain loops, no LN helper ────────────────────
# Every class the fixtures hold the census and the checker against is
# RE-DERIVED here from the raw 5m children: first AND last print child,
# first AND last dip child, and the parent check.  Reversing the prices maps
# the FIRST child that did a thing onto the LAST one, so the converse's class
# is PREDICTED from the original children, never read back off the module.
def _fx_children(sym: str, bar_open_ms: int) -> tuple:
    t0, h5, l5, c5 = LN._FIVE_SOURCE(sym)
    a = int(np.searchsorted(t0, int(bar_open_ms), "left"))
    b = int(np.searchsorted(t0, int(bar_open_ms) + MS_4H, "left"))
    return t0[a:b], h5[a:b], l5[a:b], c5[a:b]


def _fx_cls(first_up, first_dip, parent_ok: bool) -> str:
    if not parent_ok:
        return "mismatch"
    if first_up is None:
        return "no_print"
    if first_dip is None:
        return "print_no_dip"
    if first_dip < first_up:
        return "dip_before"
    return "dip_after" if first_up < first_dip else "tie"


def _fx_classes(kids, d: int, e: float, trig: float, bar_open_ms: int,
                bar_hi: float, bar_lo: float) -> tuple:
    """(class, the converse's class) of one latch bar, by the fixture."""
    t5, h5, l5, _c5 = kids
    n = len(t5)
    fu = fd = lu = ld = None
    for k in range(n):
        fav = float(h5[k]) if d == 1 else float(l5[k])
        adv = float(l5[k]) if d == 1 else float(h5[k])
        if (fav - e) * d >= (trig - e) * d:
            fu = k if fu is None else fu
            lu = k
        if (adv - e) * d <= 0.0:
            fd = k if fd is None else fd
            ld = k
    pok = (n == 48
           and all(int(t5[k]) == int(bar_open_ms) + k * MS_5M
                   for k in range(n))
           and max(float(x) for x in h5) == float(bar_hi)
           and min(float(x) for x in l5) == float(bar_lo)) if n else False
    rev = _fx_cls(None if lu is None else n - 1 - lu,
                  None if ld is None else n - 1 - ld, pok)
    return _fx_cls(fu, fd, pok), rev


def _fx_flip_ok(cls: str, rev: str) -> bool:
    """The converse's law, typed by the fixture: a dip row must FLIP to the
    other dip class; a no-dip or mismatch row is INVARIANT; a tie is
    EXEMPT (one child holds no order)."""
    if cls in FX_DIPS:
        return rev in FX_DIPS and rev != cls
    if cls in ("print_no_dip", "mismatch"):
        return rev == cls
    return cls == "tie"


def _c10_be_checks(rows) -> tuple:
    """THE F-C10-BE CHECKS, on whatever rows they are handed.

    Per row: the module's class equals the fixture's own re-derivation AND
    the class the row was chosen for, the module agrees with the hand walk
    (+ the hand's parent check, so a GENUINE mismatch can agree) and with
    the row's JOURNAL; and THE CONVERSE (prices reversed, stamps kept) is
    answered by the module as the fixture predicts, the hand agrees, and it
    obeys the converse law (dip rows flip; no-dip and mismatch rows are
    invariant; a tie is exempt).  CLOSING: one row of EACH required class —
    dip-before, dip-after WITH an actual dip, tie-or-mismatch — must pass,
    and the module's BE_REQUIRED must be the contract's three."""
    lines, ok, have = [], True, []
    for row in rows:
        d = dict(row) if isinstance(row, dict) \
            else dict(zip(CAMPAIGN_FIELDS, row))
        sym, om = d["symbol"], int(d["latch_bar_open_ms"])
        dd, e, r = int(d["direction"]), float(d["entry_px"]), float(d["r_dist"])
        hi4, lo4 = float(d["bar_high"]), float(d["bar_low"])
        args = (sym, om, dd, e, r, hi4, lo4)
        ev = LN.be_campaign_evidence(*args)
        rv = LN.be_campaign_evidence(*args, converse=True)
        trig = e + dd * 1.0 * r
        fx, fx_rev = _fx_classes(_fx_children(sym, om), dd, e, trig, om, hi4,
                                 lo4)
        g1 = bool(ev["agree"] and ev["module_class"] == fx
                  == d["expected_class"]
                  and ev["module"]["order"] == d["journal_order"])
        g2 = bool(rv["agree"] and rv["module_class"] == fx_rev
                  and _fx_flip_ok(fx, fx_rev)
                  and LN.be_converse_ok(ev["module_class"],
                                        rv["module_class"]))
        ok &= g1 and g2
        if g1 and g2:
            have.append(LN.be_required_class(fx))
        lines.append(
            f"[{'OK ' if g1 else 'BAD'}] {sym} {LN.iso(om)} "
            f"{'LONG' if dd == 1 else 'SHORT'}: module "
            f"{ev['module']['order']!r} -> {ev['module_class']!r} / hand "
            f"{ev['hand']['order']!r}, parent "
            f"{'reproduced' if ev['parent']['ok'] else 'NOT reproduced'} -> "
            f"{ev['hand_class']!r} / journal {d['journal_order']!r} / "
            f"fixture {fx!r} (chosen as {d['expected_class']!r}); up child "
            f"{ev['module']['i_up']} dip child {ev['module']['i_dip']}")
        lines.append(
            f"[{'OK ' if g2 else 'BAD'}]   converse (prices reversed, stamps "
            f"kept): module {rv['module_class']!r} / hand "
            f"{rv['hand_class']!r} / fixture-predicted {fx_rev!r} — "
            + ("must FLIP" if fx in FX_DIPS else "EXEMPT (a tie holds no "
               "order)" if fx == "tie" else "must be INVARIANT"))
    need = set(FX_REQUIRED)
    got = set(have)
    nt = re.sub(r"\s+", " ", LN.filed_text(LN.BE1_REG))
    g = (len(rows) >= 3 and need <= got
         and tuple(LN.BE_REQUIRED) == FX_REQUIRED
         and LN.BE_REQUIRED_QUOTE in nt)
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] CLOSING — one passing row of "
                 f"EACH required class {list(FX_REQUIRED)} (the contract's "
                 f"\"{LN.BE_REQUIRED_QUOTE}\", quoted from P-BE-1 §9: "
                 f"{'present' if LN.BE_REQUIRED_QUOTE in nt else 'ABSENT'}; "
                 f"module BE_REQUIRED {list(LN.BE_REQUIRED)}): {len(rows)} "
                 f"rows, passing classes {sorted(got)}, missing "
                 f"{sorted(need - got) or 'none'}")
    return ok, lines


# ═══════ F-C10-BE-RULE · the checker F-C10-BE runs, certified — SYNTHETIC
# CERTIFICATION ONLY.  These tapes prove the CHECKER can pass a complete set
# and cannot pass an incomplete or corrupted one.  They are NOT F-C10-BE and
# cannot stand in for it: P-BE-1 §9 forbids substituting a synthetic bar
# there, and nothing here is handed to that leg.
CERT_PLANS = (
    ("dip_before", "bottom", "BE", lambda h, l, c: kids(h, l, c, 10, 3)),
    ("dip_after", "bottom", "BE", lambda h, l, c: kids(h, l, c, 3, 10)),
    ("tie", "bottom", "BE", lambda h, l, c: kids(h, l, c, 7, 7)),
    ("mismatch", "bottom", "BE",
     lambda h, l, c: kids(h, l, c, 3, 10, cap_hi=h - 0.02 * (h - c))),
    ("print_no_dip", "bottom", "MONO", None),
    # the SHORT mirror: a short's DIP is the bar's HIGH, its PRINT the LOW
    ("dip_before", "top", "BE", lambda h, l, c: kids(h, l, c, 3, 10)),
    ("dip_after", "top", "BE", lambda h, l, c: kids(h, l, c, 10, 3)),
    ("tie", "top", "BE", lambda h, l, c: kids(h, l, c, 7, 7)),
    ("mismatch", "top", "BE",
     lambda h, l, c: kids(h, l, c, 10, 3, cap_lo=l + 0.02 * (c - l))),
    ("print_no_dip", "top", "MONO", None),
)
CERT_SYMS = tuple(f"SYN-BE-CERT{k}-4H" for k in range(len(CERT_PLANS)))
_CERT: dict = {}


def _cert() -> tuple:
    """(rows, trades, 5m sources) of the certification set — each plan on
    its OWN synthetic symbol, ridden by `replay10` so every row carries the
    ride's own journal answer.  Built once."""
    if _CERT:
        return _CERT["rows"], _CERT["trades"], _CERT["src"]
    rows, trades, src = [], [], {}
    card = LN.Card(name="syn-cert", lane="spring", be_floor_after_r=1.0)
    for sym, (cls, side, rws, pk) in zip(CERT_SYMS, CERT_PLANS):
        st, om, h, l, c, sig, e, R, stp = be_tape(
            BE_ROWS if rws == "BE" else MONO_ROWS, side, sym=sym)
        plan = ({LATCH: pk(float(h[LATCH]), float(l[LATCH]), float(c[LATCH]))}
                if pk else {})
        src[sym] = five_source(om, h, l, c, plan)(sym)
        old = LN._FIVE_SOURCE
        LN._FIVE_SOURCE = lambda _s, _a=src[sym]: _a
        try:
            _, tr = LN.replay10(sym, card, T9.V6_ROLES, int(om[0]),
                                int(om[-1]) + MS_4H - 1, springs=[sig])
        finally:
            LN._FIVE_SOURCE = old
        t = tr[0]
        f = st["f"]
        j = int(t.be_bar) if t.be_bar is not None else LATCH
        trades.append(t)
        rows.append({"symbol": sym, "latch_bar_open_ms": int(f.open_ms[j]),
                     "direction": int(t.direction),
                     "entry_px": float(t.entry_px),
                     "r_dist": float(t.r_dist), "bar_high": float(f.h[j]),
                     "bar_low": float(f.l[j]), "expected_class": cls,
                     "journal_order": str(t.be_order)})
    _CERT.update(rows=rows, trades=trades, src=src)
    return rows, trades, src


def _with_cert(fn):
    """Run `fn` with the certification tapes' 5m children reachable (and the
    real tapes behind them, for a real row)."""
    _rows, _tr, src = _cert()
    old = LN._FIVE_SOURCE
    LN._FIVE_SOURCE = lambda s, _o=old: src[s] if s in src else _o(s)
    try:
        return fn()
    finally:
        LN._FIVE_SOURCE = old


def _rule_checks() -> tuple:
    rows, trades, _src = _cert()

    def run():
        lines, ok = [], True
        lines.append("      CERTIFICATION ONLY — ten SYNTHETIC latch bars "
                     "(five classes x both directions). This is NOT F-C10-BE "
                     "and cannot stand in for it: P-BE-1 §9 forbids a "
                     "synthetic bar there.")
        cen = LN.be_latch_census(trades, be_r=1.0)
        exp = {r["symbol"]: r["expected_class"] for r in rows}
        got = {r["symbol"]: r["class"] for r in cen["rows"]}
        c = cen["counts"]
        g = (got == exp and c["n_three_way"] == len(rows)
             and c["n_converse_ok"] == len(rows)
             and c["by_class"] == {k: 2 for k in FX_CLASSES})
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] the census builder on the "
                     f"certification set: classes {c['by_class']}, three-way "
                     f"{c['n_three_way']}/{len(rows)}, converse ok "
                     f"{c['n_converse_ok']}/{len(rows)}; every row's class is "
                     f"the one it was built as: {got == exp}")
        dec = cen["f_c10_be"]
        picked = [LN.be_required_class(r["class"]) for r in dec["rows"]]
        g = dec["decision"] == "RUN" and picked == list(FX_REQUIRED)
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] with all three classes "
                     f"present the rule decides {dec['decision']!r} on rows "
                     f"{picked} — so the NOT RUN on the filed book is the "
                     f"book's answer, not a rule that cannot say RUN")
        ok2, l2 = _c10_be_checks(rows)
        ok &= ok2
        lines += l2
        return ok, lines
    return _with_cert(run)


def f_c10_be_rule() -> bool:
    rows, _tr, _src = _cert()
    by = {}
    for r in rows:
        by.setdefault((r["expected_class"], r["direction"]), r)
    real = _census()["rows"]

    def corrupted(sel, title):
        def leg():
            ok, lines = _with_cert(lambda: _c10_be_checks(sel()))
            bad = [x for x in lines if x.startswith("[BAD]")]
            return ok, (f"{title}: " + (bad[-1][:170] if bad
                                        else "no BAD line"))
        return leg

    def three_real():
        """THREE REAL rows off the filed book's census — one of each class it
        holds, filled in census order — the book's own situation."""
        seen, out = set(), []
        for r in real:
            if r["class"] not in seen:
                seen.add(r["class"])
                out.append(r)
        for r in real:
            if len(out) >= 3:
                break
            if r not in out:
                out.append(r)
        return [_campaign_row(r) for r in out[:3]]

    def no_tie():
        return [by[("dip_before", 1)], by[("dip_after", 1)],
                by[("dip_before", -1)]]

    def no_dip_in_dip_after():
        return [by[("dip_before", 1)],
                dict(by[("print_no_dip", 1)], expected_class="dip_after"),
                by[("tie", 1)]]

    def old_converse(t5, h5, l5, c5):
        return t5[::-1], h5[::-1], l5[::-1], c5[::-1]

    true_ev = LN.be_campaign_evidence

    def order_agree(*a, **k):
        ev = true_ev(*a, **k)
        return dict(ev, agree=bool(
            ev["module"]["order"] == ev["hand"]["order"]
            and ev["module"]["i_up"] == ev["hand"]["i_up"]
            and ev["module"]["i_dip"] == ev["hand"]["i_dip"]))

    return prove(
        "F-C10-BE-RULE",
        "the checker F-C10-BE runs, certified on a SYNTHETIC set of every "
        "class in both directions (certification only — never F-C10-BE): it "
        "passes a complete set, and no set lacking a required class, no "
        "old-style converse and no order-only `agree` can pass",
        "the certification set fails the checks; the census builder "
        "misclassifies a synthetic bar or its rule cannot decide RUN on a "
        "complete set; OR any of these passes: three rows lacking a "
        "tie/mismatch class (real or synthetic), a print with no dip in the "
        "dip-after slot, a converse that reverses the timestamps, an `agree` "
        "that is blind to a genuine mismatch, or a closing rule that lost "
        "a class.",
        [("three REAL rows off the filed book's census, lacking a "
          "tie/mismatch class (the book's own situation) — cannot pass",
          corrupted(three_real, "three real rows")),
         ("the synthetic tie and mismatch rows dropped, a second dip-before "
          "in their place — cannot pass", corrupted(no_tie, "no tie")),
         ("a print with NO dip offered in the dip-after slot (the old "
          "closing check counted any `plus1r_first`)",
          corrupted(no_dip_in_dip_after, "no-dip as dip-after")),
         ("the converse reverses the TIMESTAMPS too (the pre-repair "
          "converse: every reversed bar is a `mismatch`, so 'the order moved' "
          "held by construction)",
          mutated(LN, "converse_children", old_converse, _rule_checks)),
         ("the hand's parent check neutered — `agree` then cannot hold on a "
          "GENUINE mismatch",
          mutated(LN, "hand_parent_check",
                  lambda *a, **k: {"ok": True, "n_children": N5,
                                   "grid": True, "same_high": True,
                                   "same_low": True}, _rule_checks)),
         ("`agree` restored to pre-repair ORDER equality (a genuine mismatch "
          "campaign could never agree)",
          mutated(LN, "be_campaign_evidence", order_agree, _rule_checks)),
         ("the closing rule loses its tie-or-mismatch class "
          "(BE_REQUIRED shortened)",
          mutated(LN, "BE_REQUIRED", ("dip_before", "dip_after"),
                  _rule_checks))],
        _rule_checks)


# ═══════ F-C10-BE-CENSUS · the filed book's latch bars, OUTCOME-FREE
# P-BE-1's SCORED arm A1, ridden through the filed door, read for its LATCH
# BARS' 5m order and nothing else.  The census is filed by main() as
# BE_LATCH_CENSUS.json ONLY after a WHOLE run in which this fixture PASSED.
FX_ROW_FIELDS = (
    "symbol", "direction", "entry_ms", "entry_px", "r_dist",
    "latch_bar_open_ms", "latch_bar_open", "trigger_px",
    "journal_order", "module_order", "hand_order", "parent_reproduced",
    "i_up", "i_dip", "class", "hand_class",
    "module_eq_journal", "module_eq_hand", "three_way",
    "converse_module_class", "converse_hand_class", "converse_agree",
    "converse_ok")
FX_TOP_KEYS = frozenset((
    "artifact", "tier", "registration", "arm", "era", "panel",
    "registration_sha256", "window_lo", "window_hi", "be_floor_after_r",
    "rule", "classes", "required", "converse_exempt", "converse_invariant",
    "row_fields", "withheld", "section9", "counts", "f_c10_be", "rows"))
OUTCOME_KEY = re.compile(
    r"exit|net_r|gross|fee_r|funding|pnl|mfe|mae|harvest|bars_held|be_exit|"
    r"be_bound|stop_path|final_stop|advance|ratchet|blocked|outcome|"
    r"expectancy|_ci\b|won|loss", re.I)
_BE_BOOK: dict = {}
_CEN: dict = {}


def _ride_a1():
    """P-BE-1's scored arm A1 through the FILED DOOR: run_lane ->
    TP.require_arm (text of record, pinned head) -> TP.external_book."""
    lo, hi, _m = TP.corridor_era(TP.CLASSIC5, LN.BE1_SCORED_ERA)
    return LN.run_lane(LN.CARD_BE1, T9.V6_ROLES, TP.CLASSIC5, lo, hi,
                       reg_id=LN.BE1_REG, text=LN.filed_text(LN.BE1_REG),
                       arm=LN.BE1_SCORED_ARM, lanes=("card",),
                       head_of_record=LN.filed_head(LN.BE1_REG))


def _be_book():
    if "book" not in _BE_BOOK:
        _BE_BOOK["book"] = _ride_a1()
    return _BE_BOOK["book"]


def _census() -> dict:
    """THE census of this run — computed ONCE, outside every mutation, from
    the Book the filed door returned.  This is what main() files."""
    if "c" not in _CEN:
        _CEN["c"] = LN.be_latch_census(
            _be_book(), be_r=float(LN.CARD_BE1.be_floor_after_r))
    return _CEN["c"]


def _campaign_row(r: dict) -> dict:
    """A census row as an F-C10-BE row — the parent bar's extremes read off
    the RIDE's 4h frame, never off the children."""
    f = T9.frame(r["symbol"])["f"]
    j = int(np.searchsorted(f.open_ms, int(r["latch_bar_open_ms"]), "left"))
    return {"symbol": r["symbol"],
            "latch_bar_open_ms": int(r["latch_bar_open_ms"]),
            "direction": int(r["direction"]), "entry_px": float(r["entry_px"]),
            "r_dist": float(r["r_dist"]), "bar_high": float(f.h[j]),
            "bar_low": float(f.l[j]), "expected_class": r["class"],
            "journal_order": r["journal_order"]}


def _census_checks() -> tuple:
    lines, ok = [], True
    reg, arm = LN.BE1_REG, LN.BE1_SCORED_ARM
    g = LN.BE_CAMPAIGNS == ()
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] BE_CAMPAIGNS is EMPTY "
                 f"({len(LN.BE_CAMPAIGNS)} rows) — no row is typed; §9 "
                 f"forbids the substitution a typed row would be")
    pin = json.loads(LN.REGISTRY_PIN_PATH.read_text(encoding="utf-8"))
    pin_s = f"{int(pin['registry_len'])}:{pin['registry_head']}"
    try:
        gate = TP.require_arm(reg, LN.filed_text(reg), arm, TP.CLASSIC5,
                              lanes=("card",),
                              head_of_record=LN.filed_head(reg))
        g = (gate["era"] == LN.BE1_SCORED_ERA and gate["scored_in_family"]
             and gate["registry_head_pinned"]
             and gate["registry_pin"] == pin_s
             and gate["registration_seq"]
             == int(pin["registrations"][reg]["seq"]))
        why = (f"era {gate['era']!r}, scored_in_family "
               f"{gate['scored_in_family']}, pin {gate['registry_pin'][:18]}…"
               f", seq {gate['registration_seq']}")
    except SystemExit as e:
        g, why = False, f"REFUSED: {_norm(str(e))[:150]}"
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] THE FILED DOOR opens {reg} / "
                 f"{arm!r} with the text of record and the pinned head: "
                 f"{why}")
    bk = _SELF._be_book()
    lo, hi, _m = TP.corridor_era(TP.CLASSIC5, LN.BE1_SCORED_ERA)
    spec = dict(getattr(bk, "spec", None) or {})
    g = (isinstance(bk, TP.Book) and spec.get("registration") == reg
         and spec.get("arm") == arm and spec.get("era") == LN.BE1_SCORED_ERA
         and spec.get("lo_ms") == int(lo) and spec.get("hi_ms") == int(hi)
         and len(bk) > 0)
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] the Book is the one the door "
                 f"returned: {type(bk).__name__} wearing registration "
                 f"{spec.get('registration')!r} / arm {spec.get('arm')!r} / "
                 f"era {spec.get('era')!r} over "
                 f"{LN.iso(int(lo))}..{LN.iso(int(hi) + 1)}, {len(bk)} "
                 f"campaigns (no outcome of it is read)")
    cen = LN.be_latch_census(bk, be_r=float(LN.CARD_BE1.be_floor_after_r))
    rows, cnt = cen["rows"], cen["counts"]
    latched = [t for t in bk if bool(getattr(t, "be_reached", False))]
    g = (cnt["n_campaigns"] == len(bk) and cnt["n_latch"] == len(latched)
         == len(rows) and len(rows) > 0)
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] {cnt['n_latch']} latch rows = "
                 f"the {len(latched)} campaigns the journal says latched, "
                 f"of {cnt['n_campaigns']}")
    leaks = sorted({k for r in rows for k in r if OUTCOME_KEY.search(k)})
    shapes = sorted({tuple(r) for r in rows})
    g = (not leaks and shapes == [FX_ROW_FIELDS]
         and tuple(LN.BE_CENSUS_ROW_FIELDS) == FX_ROW_FIELDS
         and set(cen) == FX_TOP_KEYS)
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] OUTCOME-FREE: every row carries "
                 f"exactly the fixture's {len(FX_ROW_FIELDS)} whitelisted "
                 f"fields (identity, entry geometry, sequencing facts) "
                 f"({len(shapes)} key shape(s)); outcome-pattern keys "
                 f"{leaks or 'none'}; top-level keys whitelisted "
                 f"{set(cen) == FX_TOP_KEYS}")
    by_t = {(t.symbol, int(t.entry_ms), int(t.direction)): t for t in latched}
    n_j = n_3 = n_c = 0
    fx_by: dict = {}
    first_bad = []
    for r in rows:
        t = by_t.get((r["symbol"], int(r["entry_ms"]), int(r["direction"])))
        f = T9.frame(r["symbol"])["f"]
        om = int(r["latch_bar_open_ms"])
        j = int(np.searchsorted(f.open_ms, om, "left"))
        jr = (t is not None and int(f.open_ms[int(t.be_bar)]) == om
              and r["journal_order"] == str(t.be_order))
        trig = float(r["entry_px"]) + int(r["direction"]) * float(
            LN.CARD_BE1.be_floor_after_r) * float(r["r_dist"])
        fx, fx_rev = _fx_classes(_fx_children(r["symbol"], om),
                                 int(r["direction"]), float(r["entry_px"]),
                                 trig, om, float(f.h[j]), float(f.l[j]))
        fx_by[fx] = fx_by.get(fx, 0) + 1
        three = bool(jr and r["three_way"]
                     and r["module_order"] == r["journal_order"]
                     and r["class"] == r["hand_class"] == fx)
        conv = bool(r["converse_agree"]
                    and r["converse_module_class"] == fx_rev
                    and r["converse_ok"] == _fx_flip_ok(fx, fx_rev))
        n_j += int(jr)
        n_3 += int(three)
        n_c += int(conv)
        if not (three and conv) and len(first_bad) < 2:
            first_bad.append(f"{r['symbol']} {r['latch_bar_open']} class "
                             f"{r['class']!r} hand {r['hand_class']!r} "
                             f"fixture {fx!r} journal {r['journal_order']!r}"
                             f" module {r['module_order']!r}; converse "
                             f"{r['converse_module_class']!r} vs predicted "
                             f"{fx_rev!r}")
    n = len(rows)
    g = n_j == n and n_3 == n and n > 0
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] THREE-WAY AGREEMENT on every "
                 f"latch bar — journal be_order (the ride's own answer, "
                 f"re-found at its be_bar) == module be_sequence == "
                 f"hand_walk_5m + the hand's parent check, and the class == "
                 f"the fixture's own plain-loop class: {n_3}/{n} (journal "
                 f"re-found {n_j}/{n})"
                 + (f"; first disagreements {first_bad}" if first_bad else ""))
    g = n_c == n and n > 0
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] THE CONVERSE on every latch bar "
                 f"(prices reversed, stamps kept): module == hand == the "
                 f"fixture's prediction (first child <-> last child), and "
                 f"converse_ok obeys the law (dip rows flip, no-dip / "
                 f"mismatch rows invariant, a tie exempt): {n_c}/{n}; "
                 f"census converse_ok {cnt['n_converse_ok']}/{n}")
    want_by = {k: fx_by.get(k, 0) for k in FX_CLASSES}
    g = (cnt["by_class"] == want_by and sum(want_by.values()) == n
         and set(fx_by) <= set(FX_CLASSES))
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] the census's class counts are "
                 f"the fixture's own tally: {cnt['by_class']} (fixture "
                 f"{want_by}); per symbol {cnt['by_symbol']}")
    b1 = LN.be_census_json(cen)
    b2 = LN.be_census_json(LN.be_latch_census(
        _ride_a1(), be_r=float(LN.CARD_BE1.be_floor_after_r)))
    b0 = LN.be_census_json(_census())
    g = b1 == b2 == b0
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] DETERMINISTIC: the census of a "
                 f"FRESH ride through the door is byte-identical — sha256 "
                 f"{hashlib.sha256(b1.encode()).hexdigest()[:16]} / "
                 f"{hashlib.sha256(b2.encode()).hexdigest()[:16]} (and the "
                 f"census this run files: "
                 f"{hashlib.sha256(b0.encode()).hexdigest()[:16]}); no wall "
                 f"clock in it")
    nt = re.sub(r"\s+", " ", LN.filed_text(reg))
    dec = cen["f_c10_be"]
    want_nr = (want_by["tie"] + want_by["mismatch"]) == 0
    g = (LN.BE_SECTION9 in nt
         and (dec["decision"] == "NOT RUN") == want_nr
         and (not want_nr or (dec["governed_by"] == "P-BE-1 §9"
                              and LN.BE_SECTION9 in dec["reason"]
                              and not dec["rows"])))
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] P-BE-1 §9, quoted from the "
                 f"text of record "
                 f"({'found' if LN.BE_SECTION9 in nt else 'NOT FOUND'}), "
                 f"decides F-C10-BE from the fixture's tally (tie "
                 f"{want_by['tie']} + mismatch {want_by['mismatch']}): "
                 f"{dec['decision']!r}, governed by {dec['governed_by']!r}, "
                 f"missing {dec['missing']}")
    return ok, lines


def f_c10_be_census() -> bool:
    _census()                         # computed ONCE, before any mutation
    true_text, true_seq = LN.filed_text, LN.be_sequence

    def _amended(reg_id, path=None):
        return true_text(reg_id, path) + " And it will print positive."

    def _stale_head(reg_id, path=None):
        first = json.loads((TP.REG_DIR / "REGISTRY.jsonl").read_text()
                           .splitlines()[0])
        return (1, str(first.get("line_sha256")))

    def _control_book():
        b = books()
        return LN.run_lane(LN.CARD_TC10_CONTROL, T9.V6_ROLES, TP.CLASSIC5,
                           b["lo"], b["hi"])

    def _always_dip_first(*a, **k):
        return dict(true_seq(*a, **k), order="dip_first")

    def _relabel(order, dip):
        return "tie" if order == "dip_first" else LN_BE_CLASS(order, dip)

    def _reversed_children(sym, bar_open_ms):
        t5, h5, l5, c5 = _orig_children(sym, bar_open_ms)
        return t5[::-1], h5[::-1], l5[::-1], c5[::-1]

    def old_converse(t5, h5, l5, c5):
        return t5[::-1], h5[::-1], l5[::-1], c5[::-1]

    return prove(
        "F-C10-BE-CENSUS",
        "P-BE-1's scored arm A1, ridden through the FILED door, read for its "
        "latch bars' 5m order ONLY: an outcome-free census, three-way "
        "agreed, converse-checked, deterministic, and it decides F-C10-BE "
        "by P-BE-1 §9",
        "the door opens with an amended text or a stale pin; the census is "
        "not taken from the Book the door returned; its latch rows are not "
        "exactly the journal's latched campaigns; a row carries any field "
        "outside the whitelist or any outcome-pattern field; any latch bar's "
        "journal order, module sequencer, hand walk (+ parent check) and the "
        "fixture's own class disagree; any converse disagrees with the "
        "fixture's first<->last prediction or breaks the converse law; the "
        "counts are not the fixture's tally; a fresh ride gives different "
        "bytes; BE_CAMPAIGNS is hand-filled; or the F-C10-BE decision does "
        "not follow §9 from the fixture's own tally.",
        [("the text of record amended after filing",
          mutated(LN, "filed_text", _amended, _census_checks)),
         ("a STALE head pin (registry line 1)",
          mutated(LN, "filed_head", _stale_head, _census_checks)),
         ("the census taken from the CONTROL book instead of the filed arm",
          mutated(_SELF, "_be_book", _control_book, _census_checks)),
         ("the sequencer answers `dip_first` on every latch bar",
          mutated(LN, "be_sequence", _always_dip_first, _census_checks)),
         ("the hand walk answers a constant",
          mutated(LN, "hand_walk_5m",
                  lambda *a, **k: {"order": "plus1r_first", "i_up": 0,
                                   "i_dip": 1, "n_children": N5},
                  _census_checks)),
         ("a dip_first latch bar RELABELLED `tie` (the move P-BE-1 §9 "
          "forbids — it would fake the missing class)",
          mutated(LN, "be_class", _relabel, _census_checks)),
         ("an OUTCOME field (exit_px) leaked into the census rows",
          mutated(LN, "BE_CENSUS_ROW_FIELDS",
                  tuple(LN.BE_CENSUS_ROW_FIELDS) + ("exit_px",),
                  _census_checks)),
         ("the latch bar's children read in REVERSE tape order",
          mutated(LN, "children_5m", _reversed_children, _census_checks)),
         ("the converse reverses the TIMESTAMPS too (the pre-repair "
          "converse)",
          mutated(LN, "converse_children", old_converse, _census_checks))],
        _census_checks)


LN_BE_CLASS = LN.be_class          # the real classifier, for the relabel leg


# ═══════════════ F-C10-BE · the 5m sequence on 3 REAL campaigns [P-BE-1 §9]
BE1_TIER_E_BE_R = {"be-floor-2R sensitivity vs card-v6 (CLASSIC5, full) "
                   "[Tier-E]": 2.0}


def _tier_e_orders() -> list:
    """REPORT-ONLY: the JOURNAL latch orders of P-BE-1's three Tier-E arms,
    each opened through the filed door.  Not the census of record (that is
    the scored arm's), not re-walked, and no outcome is read."""
    out = []
    reg = LN.BE1_REG
    rec = TP.require_registered(reg, LN.filed_text(reg),
                                head_of_record=LN.filed_head(reg))
    for a_ in rec["book_spec"]["arms"]:
        if a_["scored_in_family"]:
            continue
        be_r = BE1_TIER_E_BE_R.get(a_["arm"], 1.0)
        card = (LN.CARD_BE1 if be_r == 1.0 else
                LN.Card(name=f"tc10-be-floor-{be_r:g}R",
                        be_floor_after_r=be_r))
        lo, hi, _m = TP.corridor_era(TP.CLASSIC5, a_["era"])
        bk = LN.run_lane(card, T9.V6_ROLES, TP.CLASSIC5, lo, hi, reg_id=reg,
                         text=LN.filed_text(reg), arm=a_["arm"],
                         lanes=tuple(a_["lanes"]),
                         head_of_record=LN.filed_head(reg))
        od: dict = {}
        for t in bk:
            if bool(getattr(t, "be_reached", False)):
                od[str(t.be_order)] = od.get(str(t.be_order), 0) + 1
        out.append((a_["arm"], a_["era"], be_r, len(bk),
                    {k: od.get(k, 0) for k in ("dip_first", "plus1r_first",
                                               "tie", "mismatch")}))
    return out


def f_c10_be():
    """THE REAL-CAMPAIGN LEG — decided by P-BE-1 §9 from the census of the
    filed book.  NOT RUN whenever the census cannot supply all three
    classes; never PASS then."""
    fails_if = ("it is ever reported PASS while the filed book's census "
                "lacks any required class (dip-before, dip-after WITH a dip, "
                "tie-or-mismatch); while BE_CAMPAIGNS is hand-filled or a "
                "synthetic bar or relabelled case stands in (§9); or, once "
                "the census supplies all three, while any row's module "
                "answer differs from its hand walk (+ parent check), its "
                "journal, the fixture's own class or the class it was chosen "
                "for, or its converse (prices reversed, stamps kept) breaks "
                "the law — a dip row that does not flip, a no-dip or "
                "mismatch row that is not invariant (a tie is exempt).")
    cen = _census()
    dec, c = cen["f_c10_be"], cen["counts"]
    if dec["decision"] != "RUN":
        say("\n--- F-C10-BE — the 5m sequence proven on 3 REAL campaigns, "
            "hand-walked with plain numpy [decided by P-BE-1 §9]")
        say(f"  [NOT RUN] {dec['reason']}")
        verified = RESULTS.get("F-C10-BE-CENSUS")
        g = (c["n_three_way"] == c["n_latch"] > 0
             and c["n_converse_agree"] == c["n_latch"])
        tag = ("OK " if g and verified is True
               else "-- " if g and verified is None else "BAD")
        say(f"    [{tag}] sub-check (GREEN is NOT a PASS "
            f"of this leg): on the filed book's {c['n_latch']} latch bars "
            f"the THREE answers agree — journal be_order == module "
            f"be_sequence == hand_walk_5m (+ the hand's parent check) — "
            f"{c['n_three_way']}/{c['n_latch']}, and the converse (prices "
            f"reversed, stamps kept) {c['n_converse_agree']}/"
            f"{c['n_latch']}; independently re-derived by F-C10-BE-CENSUS: "
            f"{'PASS' if verified else 'NOT VERIFIED IN THIS RUN'}")
        say(f"    census of record (BE_LATCH_CENSUS.json): "
            f"{c['n_campaigns']} campaigns, {c['n_latch']} latch bars — "
            f"dip-before {c['by_class']['dip_before']}, dip-after "
            f"{c['by_class']['dip_after']}, print-no-dip "
            f"{c['by_class']['print_no_dip']}, tie {c['by_class']['tie']}, "
            f"4h/5m mismatch {c['by_class']['mismatch']}; required classes "
            f"absent {dec['missing']}")
        try:
            for arm, era, be_r, n, od in _tier_e_orders():
                say(f"    report-only, through the door: {arm!r} (era "
                    f"{era!r}, be_floor_after_r {be_r:g}) — {n} campaigns, "
                    f"journal latch orders {od}")
        except SystemExit as e:
            say(f"    report-only Tier-E orders: REFUSED at the door: "
                f"{_norm(str(e))[:150]}")
        say("    the checker this leg would run is certified in "
            "F-C10-BE-RULE, on SYNTHETIC bars — certification only; no "
            "synthetic bar is handed to this leg and BE_CAMPAIGNS stays "
            "empty (§9).")
        if dec["operator_question"]:
            say("    *** OPERATOR QUESTION: §9 does not prescribe this case "
                "***")
        say(f"      FAILS IF: {fails_if}")
        NOT_RUN["F-C10-BE"] = dec["reason"]
        return None
    rows = [_campaign_row(r) for r in dec["rows"]]
    return prove(
        "F-C10-BE",
        "the 5m sequence proven on 3 REAL campaigns of the filed book, one "
        "of each required class, hand-walked with plain numpy, plus the "
        "converse of each",
        fails_if,
        [("the hand walk answers a constant",
          mutated(LN, "hand_walk_5m",
                  lambda *a, **k: {"order": "plus1r_first", "i_up": 0,
                                   "i_dip": 1, "n_children": N5},
                  lambda: _c10_be_real(cen, rows))),
         ("the tie-or-mismatch row dropped (two rows cannot pass)",
          lambda: (lambda r: (r[0], "rows lacking tie/mismatch"))(
              _c10_be_real(cen, rows[:2]))),
         ("a census that is NOT the filed book's (§9: no substitution)",
          lambda: (lambda r: (r[0], "a census of another book"))(
              _c10_be_real(dict(cen, registration="P-SYN-BE"), rows)))],
        lambda: _c10_be_real(cen, rows))


def _c10_be_real(cen: dict, rows) -> tuple:
    """F-C10-BE's real checks: the census MUST be the filed book's — P-BE-1,
    its scored arm, its filed era, the pinned payload sha, CLASSIC5 symbols
    only, BE_CAMPAIGNS empty — and then `_c10_be_checks` on its rows.  A
    census of any other book (a synthetic one above all) cannot pass."""
    pin = json.loads(LN.REGISTRY_PIN_PATH.read_text(encoding="utf-8"))
    g = (cen.get("registration") == LN.BE1_REG
         and cen.get("arm") == LN.BE1_SCORED_ARM
         and cen.get("era") == LN.BE1_SCORED_ERA
         and cen.get("registration_sha256")
         == pin["registrations"][LN.BE1_REG]["sha256"]
         and all(dict(r)["symbol"] in TP.CLASSIC5 for r in rows)
         and LN.BE_CAMPAIGNS == ())
    line = (f"[{'OK ' if g else 'BAD'}] the rows are the FILED book's: "
            f"census of {cen.get('registration')!r} / {cen.get('arm')!r} / "
            f"era {cen.get('era')!r}, payload sha "
            f"{str(cen.get('registration_sha256'))[:12]} (pin "
            f"{pin['registrations'][LN.BE1_REG]['sha256'][:12]}), symbols "
            f"{sorted({dict(r)['symbol'] for r in rows})}, BE_CAMPAIGNS "
            f"{len(LN.BE_CAMPAIGNS)} rows")
    ok2, l2 = _c10_be_checks(rows)
    return bool(g and ok2), [line] + l2


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
            f"artifact this suite writes (this transcript, whose first line "
            f"is the as-of; BE_LATCH_CENSUS.json; build_manifest.json)"]

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
        f_lanes_closure, f_c10_be_harness, f_c10_be_rule, f_c10_be_census,
        f_c10_be, f_det)


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
                  BUILD_SYM + "-CUT", *SPR_SYM.values(), *CERT_SYMS):
            drop_frame(s)
    n = sum(RESULTS.values())
    say(f"\nFIXTURE SUMMARY  {n}/{len(RESULTS)} PASS  {json.dumps(RESULTS)}")
    if NOT_RUN:
        say(f"NOT RUN (never PASS): {json.dumps(NOT_RUN)}")
    try:
        meta = books()["meta"] if _B else TP.corridor_n(TP.CLASSIC5)[2]
        LANES_OUT.mkdir(parents=True, exist_ok=True)
        # THE LATCH CENSUS — filed ONLY after a WHOLE run in which
        # F-C10-BE-CENSUS PASSED, from the census computed once outside every
        # mutation.  A whole run in which it did not pass REMOVES a census
        # left by an earlier run, so the manifest never attests a stale one.
        qc = LANES_OUT / "BE_LATCH_CENSUS.json"
        if not only and RESULTS.get("F-C10-BE-CENSUS") is True and _CEN:
            body = LN.be_census_json(_CEN["c"])
            qc.write_text(body)
            say(f"BE_LATCH_CENSUS.json filed: sha256 "
                f"{hashlib.sha256(body.encode()).hexdigest()} "
                f"({_CEN['c']['counts']['n_latch']} latch rows; identity, "
                f"class and agreement flags only)")
        elif not only and qc.exists():
            qc.unlink()
            say("BE_LATCH_CENSUS.json REMOVED: F-C10-BE-CENSUS did not pass "
                "in this whole run, and a stale census may not be attested")
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
