#!/usr/bin/env python
"""TIER-C10 BRK FIXTURES — P-BRK-S1 / P-BRK-I1 MECHANICS.

TWO KINDS OF LEG PER FIXTURE, the BREAK legs first: each plants ONE corruption
and the guard must go RED on it, or the fixture is VOID — a check that cannot
fail proves nothing.  A break leg is one of two things and never a third: a
CORRUPTED INPUT handed to the module's own function (which must change its
verdict), or a MUTATION of the module (`mutated(...)`: a named wrong planted as
the implementation, under which the REAL leg's own checks must go RED).  A leg
that re-derives a wrong answer locally and never calls the module proves
nothing about the module.  Every fixture states inline what would make it FAIL.
The banned failure modes remain banned:
  · SELF-COMPARISON — re-deriving a number the way the program derived it;
  · ONE EXAMPLE where cardinality was possible;
  · a TUNED MAGNITUDE BOUND standing in for an identity;
  · a check whose claim is NOT the design's claim.

LAW 4 BINDS THESE FIXTURES, AND REAL BARS ENTER IN EXACTLY TWO WAYS:
  (1) THE KNOWN CONTROL — card v6, all pins frozen, on CLASSIC5 — which
      F-BRK-RIDE-4H rides through the lens-parameterised ride and demands
      0.000e+00 from.  That is the one real TRADE BOOK the contract allows,
      and it is what licenses the phrase "v6 management lens-scaled".
  (2) EVENT DETECTION, REPORT-ONLY — the macro DIE detector and the retest-
      hold detector read on real bars, with NO stop, NO ride, NO campaign and
      NO statistic: F-C10-HOLD's REAL half (3 holds hand-verified per lens on
      real bars, TUNING-ERA only, the bars the R1 tuning had already looked
      at) and F-BRK-ERA's as-of leg (the dies below the era cut are the same
      on the full tape and on the cut tape).  LAW 4 names this class ALLOWED;
      the R1 era rule is honoured by never touching a holdout retest-hold.
No unseen asset's price is read anywhere in this file.  No BRK lane rides any
real tape — every BRK campaign here is on a SYNTHETIC one.  No P-BRK-S1 or
P-BRK-I1 number is computed, printed or filed.  Sabotage operates on COPIES
(temp roots, copied arrays, a mutated attribute restored in a finally) — never
on a real artifact.

Run: NAIAD_CACHE_DIR=~/.cache/naiad/snapshots/tc10_20260921 \\
     ~/venvs/naiad/bin/python scripts/tierc10_brk_fixtures.py [leg_substring ...]
Exit 0 = all fixtures pass; exit 1 = at least one failed and NOTHING
DOWNSTREAM IS TRUSTWORTHY.
"""
from __future__ import annotations

import contextlib
import dataclasses
import io
import json
import math
import os
import re
import subprocess
import sys
import tempfile
import traceback
from pathlib import Path
from types import SimpleNamespace as NS

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import tierc10_brk as B                                              # noqa: E402
import tierc10_panel as TP                                           # noqa: E402
import tierc9 as T9                                                  # noqa: E402
import tierc7 as T7                                                  # noqa: E402
import tierc7_rules as RC                                            # noqa: E402
import tierc5_rules as V5                                            # noqa: E402
from engine import htf as HTF                                        # noqa: E402
from engine import indicators as ind                                 # noqa: E402

PY = str(Path.home() / "venvs" / "naiad" / "bin" / "python")
BRK_OUT = B.OUT
MS_5M, MS_4H, MS_1D = 300_000, 4 * 3_600_000, 86_400_000

T: list[str] = []
RESULTS: dict[str, bool] = {}
_B: dict = {}
_TAPES: dict = {}


# ── THE CENSUS MODULE, REACHED THE WAY THE MODULE UNDER TEST REACHES IT ──────
# `tierc10_brk` imports the range machine through ONE function-local door
# (§12); these fixtures do the same, so importing this file can never put
# `analytics.rangefinder_census` in anybody's module-level closure and
# F-BRK-CLOSURE's fresh-interpreter probe stays the honest test it is.
def census():
    import tierc10_census as C                              # noqa: PLC0415
    return C


def real_tape(sym: str, lens: str):
    """(tape, tuning-era cut index) from the FROZEN snapshot, loaded once.

    LAW 4: this hands back BARS.  Every caller in this file uses them for
    EVENT DETECTION ONLY — no stop, no ride, no campaign, no statistic — and
    the retest-hold callers use only the TUNING-ERA head, which the R1 tuning
    had already read.  Nothing here touches a holdout retest-hold.
    """
    key = (sym, lens)
    if key not in _TAPES:
        C = census()
        tape = C.load_tape(sym, lens)
        _TAPES[key] = (tape, int(C.era_cut(tape)))
    return _TAPES[key]


def macro_dies(tape) -> list:
    """[(i, rid, side)] of the macro breakout-DIEs on a tape, at the FROZEN
    scale — the census's own detector, through the census's own call."""
    C = census()
    m = C.run_scale(tape, B.FROZEN_SCALE)
    return sorted((int(e["i"]), int(e["rid"]), str(e["side"]))
                  for e in m["macro"]["events"] if e["event"] == "breakout-die")

_TMP = re.compile(r"[^\s'\"(),;]*/(f-[a-z0-9-]+-)[A-Za-z0-9_]{8}")


def _norm(s: str) -> str:
    """Throwaway directories carry a RANDOM name; the filed transcript must
    not (F-DET's law applies to the evidence too)."""
    return _TMP.sub(r"<tmp>/\1*", str(s))


def say(s: str = "") -> None:
    s = _norm(s)
    print(s)
    T.append(s)


def _halts(fn) -> bool:
    """True iff `fn` raises SystemExit.  ANY other exception is False, so a
    guard that merely CRASHES never passes for a guard that HALTS — which is
    what tells a readable-slot mutation apart from the real PendingVerdict."""
    try:
        fn()
    except SystemExit:
        return True
    except BaseException:                                   # noqa: BLE001
        return False
    return False


def refused(fn) -> tuple[bool, str]:
    """(True, why) iff `fn` HALTed.  The estate's guards raise SystemExit."""
    try:
        fn()
    except SystemExit as e:
        return True, _norm(str(e))[:220]
    return False, "ran to completion"


def refused_long(fn) -> tuple[bool, str]:
    """(True, the WHOLE HALT text) — `refused` truncates at 220 characters,
    which is shorter than the evidence some [Q-R3] HALTs carry (the census
    row's key, the two table paths, the sample floor and both n's).

    A CRASH IS NOT A HALT.  Any other exception comes back False and NAMED,
    so a guard that merely falls over on a malformed table never passes for
    one that refuses it — which is the difference between the repair and a
    KeyError standing in for it."""
    try:
        fn()
    except SystemExit as e:
        return True, _norm(str(e))
    except BaseException as e:                              # noqa: BLE001
        return False, (f"CRASHED rather than HALTed: {type(e).__name__}: "
                       f"{_norm(str(e))[:160]}")
    return False, "ran to completion"


def mutated(obj, attr: str, wrong, checks):
    """A BREAK LEG BY MUTATION.  Swap ONE attribute of the module under test
    for a WRONG implementation, run the REAL leg's own checks against it,
    restore.  `ok == True` means the checks stayed GREEN — i.e. the fixture
    cannot see the wrong it claims to guard, and the fixture is VOID."""
    def leg():
        old = getattr(obj, attr)
        setattr(obj, attr, wrong)
        try:
            ok, lines = checks()
        except SystemExit as e:
            ok, lines = False, [f"[BAD] the checks HALTed: {_norm(str(e))}"]
        except Exception as e:                              # noqa: BLE001
            ok, lines = False, [f"[BAD] the checks crashed: "
                                f"{type(e).__name__}: {_norm(str(e))[:120]}"]
        finally:
            setattr(obj, attr, old)
        bad = [ln for ln in lines if ln.startswith("[BAD]")]
        return ok, ("the REAL leg's checks under the mutation: "
                    + (bad[0][:160] if bad else "no BAD line"))
    return leg


def mutated2(obj, pairs: list, checks):
    """A BREAK LEG BY MUTATION, TWO ATTRIBUTES AT ONCE.

    Some defects are a PAIR of guards, and restoring only one of them leaves
    the other catching the wrong — which would make the break leg go RED for
    a reason that proves nothing about the guard under test.  The two-table
    cross-check is exactly that: the shipped defect was BOTH that the shared
    columns were not required of the verdict table AND that an absent one was
    skipped rather than HALTed.  This restores both, together, so the leg is
    the defect as it actually shipped.
    """
    def leg():
        old = [(a, getattr(obj, a)) for a, _ in pairs]
        for a, wrong in pairs:
            setattr(obj, a, wrong)
        try:
            ok, lines = checks()
        except SystemExit as e:
            ok, lines = False, [f"[BAD] the checks HALTed: {_norm(str(e))}"]
        except Exception as e:                              # noqa: BLE001
            ok, lines = False, [f"[BAD] the checks crashed: "
                                f"{type(e).__name__}: {_norm(str(e))[:120]}"]
        finally:
            for a, o in old:
                setattr(obj, a, o)
        bad = [ln for ln in lines if ln.startswith("[BAD]")]
        return ok, ("the REAL leg's checks under the mutation: "
                    + (bad[0][:160] if bad else "no BAD line"))
    return leg


def prove(fid: str, title: str, fails_if: str, breaks: list, real) -> bool:
    """BREAK legs first, judged ONE AT A TIME; any that comes back GREEN voids
    the fixture.  A break leg that CRASHES proves nothing and voids it too."""
    say(f"\n--- {fid} — {title}")
    void = False
    for name, fn in breaks:
        try:
            b_ok, b_detail = fn()
        except BaseException as e:                          # noqa: BLE001
            b_ok, b_detail = True, (f"break leg CRASHED "
                                    f"({type(e).__name__}: {str(e)[:140]})")
        say(f"  [BREAK] {name} -> "
            f"{'RED (correct)' if not b_ok else 'GREEN (FIXTURE IS VOID)'}: "
            f"{_norm(b_detail)}")
        void |= bool(b_ok)
    try:
        r_ok, lines = real()
    except SystemExit as e:
        r_ok, lines = False, [f"[BAD] the real leg HALTed: {_norm(e)}"]
    except Exception:                                       # noqa: BLE001
        r_ok, lines = False, ["[BAD] the real leg crashed: "
                              + traceback.format_exc()[-700:]]
    for ln in lines:
        say("    " + _norm(ln))
    say(f"      FAILS IF: {fails_if}")
    ok = bool(r_ok) and not void and bool(breaks)
    say(f"  [{'PASS' if ok else 'FAIL'}] {fid}"
        + (" — a break leg passed; the fixture proves nothing" if void
           else ""))
    RESULTS[fid] = ok
    return ok


def mark(ok: bool, s: str) -> str:
    return ("[OK ] " if ok else "[BAD] ") + s


# ═══════════════════════════════════════════════ SYNTHETIC TAPE CONSTRUCTORS
def syn_frame(sym: str, lens: str, c, h=None, l=None, t0: int = 0,
              fund: tuple | None = None) -> B.LensFrame:
    """A LensFrame with NO asset behind it: closes given, wicks derived, ATR
    the engine's.  `fund` = (hour_ms array, rate array) or None."""
    c = np.asarray(c, float)
    h = c + 0.5 if h is None else np.asarray(h, float)
    l = c - 0.5 if l is None else np.asarray(l, float)
    step = int(B.LENS_MS[lens])
    fh, fr = fund if fund else (np.zeros(0, np.int64), np.zeros(0, float))
    return B.LensFrame(sym=sym, lens=lens,
                       open_ms=int(t0) + np.arange(len(c), dtype=np.int64) * step,
                       o=np.r_[c[0], c[:-1]], h=h, l=l, c=c,
                       atr=ind.atr(h, l, c, B.ATR_LEN), step_ms=step,
                       fund_hour_ms=np.asarray(fh, np.int64),
                       fund_rate=np.asarray(fr, float))


def hold_tape(n: int = 60, die_i: int = 10, touch_i: int = 20,
              hold_bars: int = 6, side: str = "top", fail_at: int | None = None,
              band_px: float = 100.0, margin_atr: float = 1.0):
    """A PLANTED HOLD, with the band handed in as a CONSTANT array.

    The band arrives as an ARGUMENT to the detector, so the geometry can be
    planted exactly rather than coaxed out of an EMA: away from the band price
    sits clear on the DIE side; at `touch_i` the bar's range meets the band;
    for the next `hold_bars` it stays put — unless `fail_at` is given, where
    ONE close is pushed through the far edge by more than margin x ATR.
    Returns (h, l, c, atr, lo, hi, dies, extreme).
    """
    far = 1.0 if side == "top" else -1.0          # the die side, in price
    base = band_px + far * 10.0
    c = np.full(n, base)
    atr = np.ones(n)
    lo = np.full(n, band_px)
    hi = np.full(n, band_px)
    h = c + 1.0
    l = c - 1.0
    # the retest: the bar's range MEETS the band, the close sits back on the
    # die side, and the prior close is beyond it (the approach condition).
    if side == "top":
        l[touch_i] = band_px - 0.5
        h[touch_i] = band_px + 5.0
        c[touch_i] = band_px + 3.0
    else:
        h[touch_i] = band_px + 0.5
        l[touch_i] = band_px - 5.0
        c[touch_i] = band_px - 3.0
    for k in range(touch_i + 1, min(touch_i + hold_bars + 1, n)):
        c[k] = band_px + far * 3.0
        h[k] = c[k] + 1.0
        l[k] = c[k] - 1.0
    if fail_at is not None:
        # THROUGH the far edge by more than margin x ATR — the failed hold.
        c[fail_at] = band_px - far * (margin_atr + 1.0)
        h[fail_at] = c[fail_at] + 0.2
        l[fail_at] = c[fail_at] - 0.2
    seg = slice(touch_i, min(touch_i + hold_bars + 1, n))
    extreme = (float(np.min(l[seg])) if side == "top"
               else float(np.max(h[seg])))
    return h, l, c, atr, lo, hi, [(die_i, 7, side)], extreme


def lifecycle_tape() -> tuple:
    """THE OPERATOR'S OWN SENTENCE, AS A PRICE PATH [R4]: expansion of the
    bands -> consolidation and closing -> new expansion as CONTINUATION ->
    interweaving of the EMAs and a final cross -> new expansion as REVERSAL."""
    seg = np.r_[np.full(40, 100.0),                  # warm-up, flat
                np.linspace(100, 140, 40),           # EXPANDING  +1  (first)
                np.linspace(140, 141, 25),           # CONSOLIDATING
                np.linspace(141, 190, 40),           # EXPANDING  +1  (cont.)
                np.linspace(190, 188, 30),           # interweave, final cross
                np.linspace(188, 110, 60)]           # EXPANDING  -1  (reversal)
    c = np.asarray(seg, float)
    return c, c + 0.5, c - 0.5


def warm_tape() -> tuple:
    """A tape on which a counter 12/89 WINDOW bell fires at a bar an entry at
    bar 30 can reach — so "the component is INACTIVE" is a claim with a
    consequence, not a label."""
    c = np.r_[np.linspace(100, 130, 40),
              np.linspace(130, 101, 40),
              np.linspace(101, 140, 40)]
    return np.asarray(c, float), np.asarray(c, float) + 0.5, np.asarray(c, float) - 0.5


def funding_series(t0: int, n_stamps: int, every_h: int = 8,
                   rate: float = 0.0001) -> tuple:
    hours = int(t0) + np.arange(n_stamps, dtype=np.int64) * (every_h * 3_600_000)
    return hours, np.full(n_stamps, float(rate))


# ══════════════════════════════════════════ F-BRK-RIDE-4H · the control, zero
CMP_EXACT = ("entry_i", "exit_i", "exit_reason", "harvested",
             "harvest_i", "harvest_blocked_by", "ratchet_exit", "bars_held")
CMP_NUM = ("entry_px", "exit_px", "stop_px", "r_dist", "final_stop_px",
           "gross_r", "fee_r", "funding_r", "net_r", "mfe_r",
           "stop_advanced_atr")

# ── THE FIVE FIELDS THE RE-RIDE IS NOT GIVEN, NAMED IN ADVANCE ───────────────
# `_reride` is fed the control's ENTRIES and STOPS (a `Leg`) and NOT its
# ARMING PATH, so the five fields the arming stage writes cannot match and are
# not claimed to.  Review asked that this be said out loud, because "all 8
# exact + 11 numeric fields" reads like "the whole Trade record".  So the
# stronger statement is made instead: `_full_field_diff` compares EVERY field
# of `RC.Trade` on every campaign and the set that differs must be EXACTLY
# these five — more would be a real disagreement, fewer would mean the fixture
# had stopped exercising the arming difference it is excusing.
ARMING_FIELDS = ("anchor_bar_ms", "anchor_was_sealed", "arm_i", "arm_ms",
                 "disp_at_arming")
TRADE_FIELDS = tuple(f.name for f in dataclasses.fields(RC.Trade))


def _same_value(x, y) -> bool:
    if isinstance(x, float) and isinstance(y, float):
        return (math.isnan(x) and math.isnan(y)) or x == y
    return x == y


def _full_field_diff(got: list, want: list) -> tuple:
    """(the set of RC.Trade fields that differ anywhere, n_fields, n_pairs)."""
    g = sorted(got, key=lambda t: (t.symbol, t.entry_i))
    w = sorted(want, key=lambda t: (t.symbol, t.entry_i))
    bad = set()
    for a, b in zip(g, w):
        bad |= {f_ for f_ in TRADE_FIELDS
                if not _same_value(getattr(a, f_), getattr(b, f_))}
    return bad, len(TRADE_FIELDS), min(len(g), len(w))


def ctrl_compare(got: list, want: list) -> tuple:
    """Campaign by campaign, EXACT.  Returns (ok, worst, why)."""
    if len(got) != len(want):
        return False, float("inf"), f"cardinality {len(got)} vs {len(want)}"
    g = sorted(got, key=lambda t: (t.symbol, t.entry_i))
    w = sorted(want, key=lambda t: (t.symbol, t.entry_i))
    worst, why = 0.0, ""
    for a, b in zip(g, w):
        if a.symbol != b.symbol:
            return False, float("inf"), f"symbol {a.symbol} vs {b.symbol}"
        for f_ in CMP_EXACT:
            if getattr(a, f_) != getattr(b, f_):
                return False, float("inf"), (f"{a.symbol}@{a.entry_i} {f_}: "
                                             f"{getattr(a, f_)!r} vs "
                                             f"{getattr(b, f_)!r}")
        for f_ in CMP_NUM:
            x, y = getattr(a, f_), getattr(b, f_)
            if x is None and y is None:
                continue
            d = abs(float(x) - float(y))
            if d > worst:
                worst, why = d, f"{a.symbol}@{a.entry_i} {f_}"
    return worst == 0.0, worst, (why or "every field identical")


def books() -> dict:
    """The control book, ridden ONCE — CLASSIC5, card v6, all pins frozen."""
    if _B:
        return _B
    lo, hi, meta = TP.corridor_n(TP.CLASSIC5)
    control = TP.run_cell_n(TP.CONTROL_CARD, T9.V6_ROLES, TP.CLASSIC5, lo, hi)
    _B.update(lo=lo, hi=hi, meta=meta, control=list(control))
    return _B


def _reride() -> list:
    """The control's OWN entries and OWN stops, re-ridden at lens='4h'."""
    Bk = books()
    out = []
    for sym in TP.CLASSIC5:
        lf = B.frame_l(sym, "4h")
        lo_i, hi_i = B.idx_range(lf.open_ms, Bk["lo"], Bk["hi"])
        legs = [B.Leg(direction=t.direction, entry_i=t.entry_i,
                      stop_px=t.stop_px, r_dist=t.r_dist, anchor=t.anchor)
                for t in Bk["control"] if t.symbol == sym]
        out += B.brk_campaigns(lf, legs, TP.CONTROL_CARD, T9.V6_ROLES,
                               "card", lo_i, hi_i, ribbon=None, era=None)
    return out


def _ride_checks() -> tuple:
    Bk = books()
    got = _reride()
    ok, worst, why = ctrl_compare(got, Bk["control"])
    lines = [mark(ok, f"lens-parameterised ride vs the control book: "
                      f"{len(got)} campaigns, worst |diff| = {worst:.3e} "
                      f"({why})")]
    bad, n_f, n_c = _full_field_diff(got, Bk["control"])
    g = (bad == set(ARMING_FIELDS)) and len(got) == len(Bk["control"])
    ok = ok and g
    lines.append(mark(g, f"FULL-FIELD re-check — all {n_f} fields of "
                         f"RC.Trade on all {n_c} campaigns, not the 19 the "
                         f"comparator names: {n_f - len(bad)} identical, and "
                         f"the ONLY fields that differ are the "
                         f"{len(ARMING_FIELDS)} ARMING-STAGE ones "
                         f"{sorted(bad)} — the re-ride is fed the control's "
                         f"entries and stops, never its arming path (want "
                         f"exactly {list(ARMING_FIELDS)})"))
    return ok, lines


def f_brk_ride_4h() -> bool:
    def tape_identity():
        lines, ok = [], True
        for sym in TP.CLASSIC5:
            lf = B.frame_l(sym, "4h")
            st = TP.frame_n(sym)
            same = (np.array_equal(lf.open_ms, st["f"].open_ms)
                    and np.array_equal(lf.c, st["f"].c)
                    and np.array_equal(lf.h, st["f"].h)
                    and np.array_equal(lf.l, st["f"].l)
                    and np.array_equal(lf.atr, st["f"].atr))
            ok &= same
            lines.append(mark(same, f"{sym}: the Stage D 4h tape IS the "
                                    f"lineage's frame (open_ms/h/l/c/atr "
                                    f"bit-identical, {lf.n} bars)"))
        return ok, lines

    def real():
        ok1, l1 = tape_identity()
        ok2, l2 = _ride_checks()
        Bk = books()
        n_fund = sum(1 for t in Bk["control"] if t.funding_r)
        l2.append(f"[OK ] {n_fund} of {len(Bk['control'])} campaigns carry "
                  f"non-zero funding, so the interval-sum law is exercised, "
                  f"not merely bypassed")
        return ok1 and ok2 and n_fund > 0, l1 + l2

    def _cold(*a, **k):
        return {x: False for x in B.COMPONENTS}

    def _per_bar_open(lf, entry_ms, exit_ms, d, qty):
        """THE LINEAGE'S DEFECT, PLANTED: look funding up by BAR OPEN only."""
        fh = {int(x): float(y) for x, y in zip(lf.fund_hour_ms, lf.fund_rate)}
        lo_i = int(np.searchsorted(lf.open_ms, np.int64(entry_ms)))
        hi_i = int(np.searchsorted(lf.open_ms, np.int64(exit_ms)))
        s = 0.0
        for j in range(lo_i + 1, hi_i + 1):
            r = fh.get(int(lf.open_ms[j]))
            if r:
                s += r * float(lf.c[j - 1]) * d * qty * 2.0     # doubled: a
        #        named wrong, so the mutation cannot be masked by a tape with
        #        no funding stamps inside any campaign.
        return {"amount": s, "n_stamps": 0, "n_priced": 0, "n_unpriced": 0,
                "n_on_bar_open": 0}

    def corrupt_copy():
        Bk = books()
        got = [t for t in _reride()]
        import copy as _c
        bad = _c.copy(got[0])
        object.__setattr__(bad, "net_r", float(got[0].net_r) + 1e-12)
        ok, worst, why = ctrl_compare([bad] + got[1:], Bk["control"])
        return ok, f"comparator on the corrupted COPY: worst {worst:.3e} ({why})"

    return prove(
        "F-BRK-RIDE-4H",
        "the lens-parameterised ride reproduces the CLASSIC5 control book at "
        "0.000e+00 (the one real-data run LAW 4 allows)",
        "any campaign differs in any exact field, or any numeric field differs "
        "by more than 0.000000000000000e+00 — this is what licenses the phrase "
        "'v6 management lens-scaled'",
        [("every component forced COLD (the warm gate mis-fires)",
          mutated(B, "warm_components", _cold, _ride_checks)),
         ("funding looked up by BAR OPEN and doubled (the lineage's 1d defect)",
          mutated(B, "funding_interval", _per_bar_open, _ride_checks)),
         ("one net_r nudged by 1e-12 in a COPY of the re-ridden book",
          corrupt_copy)],
        real)


# ═══════════════════════════════════ F-BRK-HOLD-SYN · the anchors, both ways
def _hold_checks() -> tuple:
    """The four planted holds and the four planted failures, both anchors,
    both directions — cardinality, not one example."""
    lines, ok = [], True
    for lens in ("5m", "1d"):
        for side, d in (("top", 1), ("bottom", -1)):
            h, l, c, atr, lo, hi, dies, ext = hold_tape(side=side)
            cands, tal = B.band_hold_candidates(h, l, c, atr, dies, lo, hi,
                                                1.0, 6, B.MEM_TTL_BARS)
            g = (len(cands) == 1 and tal["n_hold"] == 1
                 and cands[0].direction == d and cands[0].touch_i == 20
                 and cands[0].known_i == 26 and cands[0].extreme == ext)
            ok &= g
            lines.append(mark(g, f"{lens} {side}-DIE HOLD -> 1 candidate, "
                                 f"dir {cands[0].direction if cands else None}, "
                                 f"touch 20, entry bar "
                                 f"{cands[0].known_i if cands else None} "
                                 f"(= touch + hold_bars), extreme {ext}"))
            h2, l2, c2, atr2, lo2, hi2, dies2, _ = hold_tape(
                side=side, fail_at=23)
            c3, t3 = B.band_hold_candidates(h2, l2, c2, atr2, dies2, lo2, hi2,
                                            1.0, 6, B.MEM_TTL_BARS)
            g2 = (len(c3) == 0 and t3["n_failed"] == 1 and t3["n_hold"] == 0)
            ok &= g2
            lines.append(mark(g2, f"{lens} {side}-DIE retest FAILS THROUGH -> "
                                  f"NO entry (n_failed={t3['n_failed']}, "
                                  f"n_hold={t3['n_hold']})"))
    # truncation: the hold window runs off the end of the tape
    h, l, c, atr, lo, hi, dies, _ = hold_tape(n=24, die_i=10, touch_i=20)
    cd, tl = B.band_hold_candidates(h, l, c, atr, dies, lo, hi, 1.0, 6,
                                    B.MEM_TTL_BARS)
    g = len(cd) == 0 and tl["n_truncated"] == 1
    ok &= g
    lines.append(mark(g, f"a hold window the tape TRUNCATES never confirms "
                         f"(n_truncated={tl['n_truncated']}, candidates="
                         f"{len(cd)})"))
    # the memory anchor, both directions, and the candidacy window
    h, l, c, atr, lo, hi, dies, _ = hold_tape(n=80, die_i=10, touch_i=20)
    for pol, d in (("support", 1), ("resistance", -1)):
        cd, tl = B.memory_flip_candidates(h, l, dies,
                                          [{"i": 20, "polarity": pol, "rid": 7}],
                                          len(c))
        g = (len(cd) == 1 and cd[0].direction == d and cd[0].touch_i == 20
             and cd[0].known_i == 20 + B.FLIP_HOLD_BARS)
        ok &= g
        lines.append(mark(g, f"memory-line flip polarity={pol} -> 1 candidate, "
                             f"dir {cd[0].direction if cd else None}, entry bar "
                             f"{cd[0].known_i if cd else None} = flip.i + "
                             f"FLIP_HOLD_BARS ({B.FLIP_HOLD_BARS}) — never the "
                             f"stamp bar"))
    for label, flip, want in (
            ("BEFORE the DIE", {"i": 5, "polarity": "support", "rid": 7}, 0),
            ("after the TTL window", {"i": 70, "polarity": "support", "rid": 7}, 0),
            ("inside the window", {"i": 30, "polarity": "support", "rid": 7}, 1)):
        cd, _t = B.memory_flip_candidates(h, l, dies, [flip], len(c),
                                          ttl_bars=40)
        g = len(cd) == want
        ok &= g
        lines.append(mark(g, f"a flip {label} -> {len(cd)} candidates "
                             f"(want {want}) [B5 candidacy window]"))
    # the entry is at known_i, never at the stamp bar
    h, l, c, atr, lo, hi, dies, _ = hold_tape()
    cands, _ = B.band_hold_candidates(h, l, c, atr, dies, lo, hi, 1.0, 6,
                                      B.MEM_TTL_BARS)
    lf = syn_frame("SYNHOLD", "5m", c, h, l)
    legs, ref = B.legs_from_candidates(lf, cands, B.LANE_S1, permit=None)
    g = len(legs) == 1 and legs[0].entry_i == 26 and legs[0].touch_i == 20
    ok &= g
    lines.append(mark(g, f"legs_from_candidates enters at known_i "
                         f"({legs[0].entry_i if legs else None}), not at the "
                         f"touch bar ({legs[0].touch_i if legs else None})"))
    return ok, lines


def f_brk_hold_syn() -> bool:
    def census_equal():
        """The claim the contract makes: this detector IS the census
        builder's rule.  Proved on a random tape with a REAL R1 band, both
        die sides, row for row."""
        import tierc10_census as C                           # noqa: PLC0415
        rng = np.random.default_rng(B.SEED)
        n = 900
        c = np.cumsum(rng.normal(0, 1.0, n)) + 200.0
        h, l = c + 1.2, c - 1.2
        atr = ind.atr(h, l, c, B.ATR_LEN)
        rows_all, mine_all, names = [], [], []
        for nm in B.R1_BANDS:
            lo, hi = B.r1_band(nm)(c)
            dies = [(300, 1, "top"), (520, 2, "bottom")]
            _, tal = B.band_hold_candidates(h, l, c, atr, dies, lo, hi,
                                            1.0, 6, B.MEM_TTL_BARS)
            tape = C.Tape(sym="SYN", lens="5m", o=np.r_[c[0], c[:-1]], h=h,
                          l=l, c=c,
                          t0=np.arange(n, dtype=np.int64) * MS_5M,
                          ts=[""] * n, atr=atr, meta={})
            rows_all.append(C.retest_holds(tape, dies, lo, hi, 1.0, 6,
                                           B.MEM_TTL_BARS))
            mine_all.append(tal["rows"])
            names.append(nm)
        same = rows_all == mine_all
        return same, [mark(same, f"band_hold_candidates == "
                                 f"tierc10_census.retest_holds, row for row, "
                                 f"on all five R1 bands "
                                 f"({sum(len(r) for r in rows_all)} rows "
                                 f"total): {names}")]

    def real():
        ok1, l1 = _hold_checks()
        ok2, l2 = census_equal()
        l2.append("[OK ] HARNESS FOR THE REAL HALF OF F-C10-HOLD: "
                  "hold_harness(lens, tape, rows) below re-walks a hold with "
                  "a plain loop and compares the module's verdict; it needs "
                  "ONLY the event ids (sym, lens, die_i, touch_i, side) once "
                  "a registration exists — no code change")
        return ok1 and ok2, l1 + l2

    def leaked_hold():
        """A CORRUPTED INPUT: one close pushed through the far edge INSIDE the
        hold window.  The detector must stop emitting the candidate."""
        h, l, c, atr, lo, hi, dies, _ = hold_tape(fail_at=24)
        cd, _t = B.band_hold_candidates(h, l, c, atr, dies, lo, hi, 1.0, 6,
                                        B.MEM_TTL_BARS)
        return len(cd) == 1, (f"the detector on the corrupted hold: "
                              f"{len(cd)} candidates (a failed hold must FAIL)")

    def _wide_window(dies, n, ttl_bars=B.MEM_TTL_BARS):
        return [(int(d), int(r), str(s), int(n) - 1) for d, r, s in dies]

    def _entry_at_touch(lf, cands, lane, permit=None, rail_atr=B.MIN_STOP_ATR):
        legs = []
        for cd in cands:
            legs.append(B.Leg(direction=cd.direction, entry_i=cd.touch_i,
                              stop_px=float(lf.c[cd.touch_i]) - 1.0,
                              r_dist=1.0, touch_i=cd.touch_i))
        return legs, {}

    return prove(
        "F-BRK-HOLD-SYN",
        "a planted DIE + retest that HOLDS gives exactly one entry at the hold "
        "close; a retest that FAILS THROUGH gives none — both anchors, both "
        "directions, on synthetic multi-lens tapes",
        "a held retest yields no entry, a failed retest yields one, an entry "
        "lands anywhere but touch_i + hold_bars, the candidacy window is not "
        "the census builder's, or the detector's rows differ from "
        "tierc10_census.retest_holds on any of the five R1 bands",
        [("a close pushed THROUGH the far edge inside the hold window "
          "(corrupted input, judged on the planted bar alone)", leaked_hold),
         ("the candidacy window widened to the whole tape",
          mutated(B, "candidacy_window", _wide_window, _hold_checks)),
         ("the entry moved to the TOUCH bar (a 6-bar look-ahead leak)",
          mutated(B, "legs_from_candidates", _entry_at_touch, _hold_checks))],
        real)


def hold_harness(lens: str, tape: dict, rows: list, margin_atr: float,
                 hold_bars: int) -> list:
    """THE HAND-VERIFICATION HARNESS for the REAL half of F-C10-HOLD.

    `tape` = {'h','l','c','atr','lo','hi'} raw arrays; `rows` = the event ids
    [{'die_i','rid','side'}].  It re-walks EACH hold with a plain loop — no
    module code — and returns [{id..., 'module', 'by_hand', 'agree'}].  A
    failed hold that the module calls a hold, or the reverse, shows as
    agree=False.  After a registration exists this needs the event ids and
    nothing else.

    THE WINDOW IS WALKED BY HAND TOO — `end = min(die + ttl, next die - 1,
    n - 1)`, the law as written, NOT `B.candidacy_window`, which would be
    self-comparison.  On a one-DIE planted tape the window is the whole tape
    and it makes no difference; on a real tape with hundreds of DIEs it is
    the difference between a hand walk and a fiction.
    """
    h, l, c = tape["h"], tape["l"], tape["c"]
    atr, lo, hi = tape["atr"], tape["lo"], tape["hi"]
    dies = [(int(r["die_i"]), int(r.get("rid", -1)), str(r["side"]))
            for r in rows]
    _, tal = B.band_hold_candidates(h, l, c, atr, dies, lo, hi, margin_atr,
                                    hold_bars, B.MEM_TTL_BARS)
    mod = {(r["die_i"], r["side"]): r for r in tal["rows"]}
    out = []
    n = len(c)
    for q, (d_i, rid, side) in enumerate(dies):
        nxt = int(dies[q + 1][0]) if q + 1 < len(dies) else n
        end = min(d_i + B.MEM_TTL_BARS, nxt - 1, n - 1)
        j = None
        for k in range(d_i + 1, end + 1):
            if not (l[k] <= hi[k] and h[k] >= lo[k]):
                continue
            beyond = (c[k - 1] > hi[k - 1]) if side == "top" else (c[k - 1] < lo[k - 1])
            if beyond:
                j = k
                break
        if j is None:
            by_hand = None
        elif j + hold_bars >= len(c):
            by_hand = "truncated"
        else:
            bad = False
            for k in range(j, j + hold_bars + 1):
                if not (np.isfinite(lo[k]) and np.isfinite(hi[k])):
                    bad = True
                    break
                if side == "top" and c[k] < lo[k] - margin_atr * atr[k]:
                    bad = True
                    break
                if side == "bottom" and c[k] > hi[k] + margin_atr * atr[k]:
                    bad = True
                    break
            by_hand = "failed" if bad else "hold"
        m = mod.get((d_i, side))
        out.append({"lens": lens, "die_i": d_i, "side": side,
                    "module": (m or {}).get("verdict"),
                    "module_touch_i": (m or {}).get("touch_i"),
                    "by_hand": by_hand, "by_hand_touch_i": j,
                    "agree": (m or {}).get("verdict") == by_hand
                             and (m or {}).get("touch_i", j) == j})
    return out


# ── THE REAL HALF — 3 HOLDS HAND-VERIFIED PER LENS ON REAL BARS ─────────────
# LAW 4 lists "Tier-E range-census EVENT-OUTCOME statistics ... report-only"
# as ALLOWED and forbids trade books; hold DETECTION is event detection, so it
# is allowed, and the earlier decision to skip the real half entirely was
# over-cautious (review).  Two collars are kept anyway, because the R1 era
# rule binds the retest-hold classes:
#   · the tape is CUT AT THE TUNING-ERA BOUNDARY before any detector sees it
#     (`tierc10_census.era_cut`), so only bars the R1 tuning had already read
#     are touched and no holdout retest-hold is looked at;
#   · nothing is counted, pooled, averaged or filed — three holds per lens are
#     walked BY HAND and compared, verdict and touch bar, against the module.
# The pins are the TUNED ones for the lens (R1) where the census filed them,
# and the DIEs are the census's own macro DIEs at the FROZEN scale.
REAL_HOLD_CASES = (("BTCUSDT", "5m"), ("ETHUSDT", "4h"), ("BTCUSDT", "1d"))


def _real_hold_checks() -> tuple:
    lines, ok = [], True
    for sym, lens in REAL_HOLD_CASES:
        tape, k = real_tape(sym, lens)
        cut = tape.head(k)
        dies = macro_dies(cut)
        pins = (B.tuned_pins(lens) if lens in B.TUNED_LENSES
                else {"band": B.R1_BANDS[1], "margin_atr": 1.0,
                      "hold_bars": 6, "ttl_bars": B.MEM_TTL_BARS,
                      "source": "(no R1 tuning on this lens — the frozen "
                                "flip-hold pins, printed)"})
        band = B.r1_band(pins["band"])
        lo, hi = band(cut.c)
        tp = {"h": cut.h, "l": cut.l, "c": cut.c, "atr": cut.atr,
              "lo": lo, "hi": hi}
        rows = [{"die_i": d, "rid": r, "side": s} for d, r, s in dies]
        walked = hold_harness(lens, tp, rows, pins["margin_atr"],
                              pins["hold_bars"])
        holds = [w for w in walked if w["module"] == "hold"][:3]
        n_fail = len([w for w in walked if w["module"] == "failed"])
        n_eval = len([w for w in walked if w["module"] is not None])
        g = (len(holds) == 3 and all(w["agree"] for w in holds)
             and n_fail >= 1 and all(w["agree"] for w in walked))
        ok &= g
        lines.append(mark(g, f"REAL {sym} {lens} (tuning-era head, {cut.n:,} "
                             f"bars, {len(dies)} macro DIEs, band "
                             f"{pins['band']} margin {pins['margin_atr']} "
                             f"hold {pins['hold_bars']}): "
                             f"{len(holds)} holds hand-verified at touch bars "
                             f"{[w['module_touch_i'] for w in holds]} "
                             f"(hand {[w['by_hand_touch_i'] for w in holds]}), "
                             f"{n_fail} retests FAIL, and the hand walk agrees "
                             f"with the module — verdict AND touch bar — on "
                             f"all {len(walked)} DIEs ({n_eval} of them "
                             f"retested at all)"))
    return ok, lines


def f_c10_hold_harness() -> bool:
    def checks():
        lines, ok = [], True
        for lens in ("5m", "4h", "1d"):
            got = []
            for side in ("top", "bottom", "top"):
                h, l, c, atr, lo, hi, dies, _ = hold_tape(side=side)
                got += hold_harness(lens, {"h": h, "l": l, "c": c, "atr": atr,
                                           "lo": lo, "hi": hi},
                                    [{"die_i": 10, "rid": 7, "side": side}],
                                    1.0, 6)
            h, l, c, atr, lo, hi, dies, _ = hold_tape(fail_at=23)
            fail = hold_harness(lens, {"h": h, "l": l, "c": c, "atr": atr,
                                       "lo": lo, "hi": hi},
                                [{"die_i": 10, "rid": 7, "side": "top"}],
                                1.0, 6)
            g = (len(got) == 3 and all(x["agree"] and x["module"] == "hold"
                                       for x in got)
                 and len(fail) == 1 and fail[0]["agree"]
                 and fail[0]["module"] == "failed")
            ok &= g
            lines.append(mark(g, f"{lens}: 3 holds hand-verified "
                                 f"({[x['module'] for x in got]}) + 1 failed "
                                 f"hold that FAILS ({fail[0]['module']}), "
                                 f"hand-walk agrees on all four"))
        return ok, lines

    def both():
        ok1, l1 = checks()
        ok2, l2 = _real_hold_checks()
        return ok1 and ok2, l1 + l2

    def real():
        ok, lines = both()
        lines.append("[NB ] the real half reads REAL BARS and detects EVENTS "
                     "on them — no stop, no ride, no campaign, no statistic — "
                     "and only on the TUNING-ERA head of each tape, which is "
                     "what LAW 4 allows report-only and what the R1 era rule "
                     "permits for a retest-hold class")
        return ok, lines

    true_band_hold = B.band_hold_candidates          # captured, not stashed

    def _never_fails(h, l, c, atr, dies, lo, hi, margin_atr, hold_bars,
                     ttl_bars=B.MEM_TTL_BARS, anchor_label=B.ANCHOR_BAND):
        """A named wrong: every evaluated retest is called a HOLD."""
        cands, tal = true_band_hold(h, l, c, atr, dies, lo, hi, margin_atr,
                                    hold_bars, ttl_bars, anchor_label)
        for r in tal["rows"]:
            r["verdict"] = "hold"
        tal["n_hold"], tal["n_failed"] = len(tal["rows"]), 0
        return cands, tal

    return prove(
        "F-C10-HOLD (synthetic + REAL, per lens)",
        "3 holds hand-verified per lens against a plain-loop walk — on "
        "planted tapes AND on real tuning-era bars — and a failed hold that "
        "must FAIL",
        "the module's verdict or touch bar disagrees with the hand walk on any "
        "hold (12 planted, 3 per lens real, plus every other evaluated DIE on "
        "the real tapes), or a planted/real failure is not reported failed",
        [("every evaluated retest relabelled a HOLD (planted tapes)",
          mutated(B, "band_hold_candidates", _never_fails, checks)),
         ("every evaluated retest relabelled a HOLD (REAL tapes)",
          mutated(B, "band_hold_candidates", _never_fails,
                  _real_hold_checks))],
        real)


# ═════════════════════════════════════════════ F-BRK-PERM · the permissions
def _perm_checks() -> tuple:
    lines, ok = [], True
    c, h, l = lifecycle_tape()
    atr = ind.atr(h, l, c, B.ATR_LEN)
    life = B.ribbon_lifecycle(c, atr)
    eps = [(e["sign"], e["kind"]) for e in life["episodes"]]
    want = [(1, "first"), (1, "continuation"), (-1, "reversal")]
    g = eps == want
    ok &= g
    lines.append(mark(g, f"the operator's sentence, as episodes: {eps} "
                         f"(want {want}) — expansion, consolidation, "
                         f"continuation, final cross, reversal"))
    warm_at = max(B.RIBBON_FAST, B.RIBBON_SLOW)
    g = (all(life["phase"][t] == B.PHASE_WARMUP and life["direction"][t] == 0
             for t in range(warm_at))
         and life["phase"][warm_at + B.LIFECYCLE_K] != B.PHASE_WARMUP)
    ok &= g
    lines.append(mark(g, f"NaN warm-up is NO permission: bars 0..{warm_at - 1} "
                         f"are {B.PHASE_WARMUP} with direction 0"))
    exp = life["expanding"]
    g = (np.all(life["direction"][~exp] == 0)
         and np.all(np.abs(life["direction"][exp]) == 1))
    ok &= g
    lines.append(mark(g, f"DIRECTION is sign(s) on every EXPANDING bar "
                         f"({int(exp.sum())}) and 0 on every other "
                         f"({int((~exp).sum())})"))
    # the interweave: a sign change inside the consolidation before the reversal
    if len(life["episodes"]) < 3:
        ok = False
        lines.append(mark(False, f"only {len(life['episodes'])} episodes — "
                                 f"the lifecycle cannot show an interweave "
                                 f"between a continuation and a reversal"))
    else:
        e1, e2 = life["episodes"][1], life["episodes"][2]
        seg = life["sign"][e1["end"] + 1:e2["start"] + 1]
        g = bool(len(set(int(x) for x in seg if x)) > 1)
        ok &= g
        lines.append(mark(g, f"the EMAs interweave between the continuation "
                             f"and the reversal: sign(s) takes "
                             f"{sorted(set(int(x) for x in seg))} across the "
                             f"consolidation"))
    # weekly posture, as-of the closed week, with a cold-EMA refusal.
    # THE TAPE RISES FROM BAR 0 ON PURPOSE: on a flat head e12 == e25 and a
    # warm-blind posture would read 0 anyway, so the leg could not see the
    # wrong it claims to guard.
    wc = np.linspace(100.0, 160.0, 70)
    wk = B.weekly_posture(wc)
    g = (np.all(wk[:B.RIBBON_SLOW] == 0) and wk[-1] == 1)
    ok &= g
    lines.append(mark(g, f"weekly 12/25 posture: 0 while EMA{B.RIBBON_SLOW} is "
                         f"cold (bars 0..{B.RIBBON_SLOW - 1}), +1 at the last "
                         f"closed week ({int(wk[-1])})"))
    # HTF visibility, against the engine's own function, at the exact boundary
    ex = np.arange(0, 20 * MS_4H, MS_5M, dtype=np.int64)
    ht = np.arange(0, 20 * MS_4H, MS_4H, dtype=np.int64)
    mine = B.visible_htf_idx(ex, ht, MS_4H)
    eng = HTF.map_htf_to_exec(ex, ht, "4h")
    g = np.array_equal(mine, eng)
    ok &= g
    lines.append(mark(g, f"visible_htf_idx == engine.htf.map_htf_to_exec on "
                         f"{len(ex)} 5m bars against 4h ({g})"))
    at = int(np.searchsorted(ex, MS_4H))
    g = (mine[at] == 0 and mine[at - 1] == -1)
    ok &= g
    lines.append(mark(g, f"the boundary: the exec bar OPENING at the 4h close "
                         f"sees bar {int(mine[at])}; the one 5m earlier sees "
                         f"{int(mine[at - 1])} (none)"))
    wk_idx = B.visible_htf_idx(np.arange(0, 21 * MS_1D, MS_1D, dtype=np.int64),
                               np.arange(0, 21 * MS_1D, 7 * MS_1D,
                                         dtype=np.int64), 7 * MS_1D)
    g = (wk_idx[6] == -1 and wk_idx[7] == 0 and wk_idx[13] == 0
         and wk_idx[14] == 1)
    ok &= g
    lines.append(mark(g, f"weekly onto daily (the map engine.cells cannot "
                         f"make): day 6 sees no week, day 7 sees week 0, day "
                         f"13 still week 0, day 14 week 1"))
    # the two permissions themselves
    dd = np.array([0, 1, -1, 1], np.int64)
    wks = np.array([1, -1], np.int64)
    widx = np.array([0, 0, 1, 1], np.int64)
    got = [B.i1_permission(i, d, dd, wks, widx)["ok"]
           for i, d in ((1, 1), (0, 1), (2, -1), (3, 1))]
    g = got == [True, False, True, False]
    ok &= g
    lines.append(mark(g, f"i1_permission (weekly AND daily, mirrored): {got} "
                         f"(want [True, False, True, False])"))
    tide = np.array([1, -1, 0], np.int64)
    got = [B.s1_permission(i, d, tide)["ok"]
           for i, d in ((0, 1), (0, -1), (1, -1), (2, 1))]
    g = got == [True, False, True, False]
    ok &= g
    lines.append(mark(g, f"s1_permission (4h tide aligned, STAND DOWN is not "
                         f"permission): {got} (want [True, False, True, "
                         f"False])"))
    return ok, lines


def f_brk_perm() -> bool:
    def _left(ex, ht, step):
        return np.searchsorted(np.asarray(ht, np.int64) + np.int64(step),
                               np.atleast_1d(np.asarray(ex, np.int64)),
                               side="left") - 1

    def _vs_close(ex, ht, step):
        """THE OFF-BY-ONE: visibility measured against the exec bar's CLOSE."""
        ex = np.atleast_1d(np.asarray(ex, np.int64))
        return np.searchsorted(np.asarray(ht, np.int64) + np.int64(step),
                               ex + np.int64(MS_5M), side="right") - 1

    true_lifecycle = B.ribbon_lifecycle              # captured, not stashed

    def _no_growth(c, atr, fast=B.RIBBON_FAST, slow=B.RIBBON_SLOW,
                   k=B.LIFECYCLE_K):
        """A named wrong: EXPANDING wherever the sign is defined — no |s|
        growth test, no K-bar sign window."""
        out = true_lifecycle(c, atr, fast, slow, k)
        exp = out["sign"] != 0
        out["expanding"] = exp
        out["direction"] = np.where(exp, out["sign"], 0).astype(np.int64)
        eps, prev, t = [], None, 0
        n = len(c)
        while t < n:
            if not exp[t]:
                t += 1
                continue
            u = t
            while u + 1 < n and exp[u + 1] and out["sign"][u + 1] == out["sign"][t]:
                u += 1
            eps.append({"start": t, "end": u, "sign": int(out["sign"][t]),
                        "kind": ("first" if prev is None else
                                 "continuation" if int(out["sign"][t]) == prev
                                 else "reversal")})
            prev = int(out["sign"][t])
            t = u + 1
        out["episodes"] = eps
        return out

    def _warm_blind(c_1w, fast=B.RIBBON_FAST, slow=B.RIBBON_SLOW):
        e_f, e_s = ind.ema(np.asarray(c_1w, float), int(fast)), \
            ind.ema(np.asarray(c_1w, float), int(slow))
        return np.where(e_f > e_s, 1, np.where(e_f < e_s, -1, 0)).astype(np.int64)

    return prove(
        "F-BRK-PERM",
        "the R4 ribbon lifecycle on a known-answer series, the weekly posture "
        "as of the CLOSED week, and the HTF visibility law",
        "the lifecycle does not read expansion -> consolidation -> "
        "continuation -> interweave/final cross -> reversal; a cold EMA grants "
        "permission; or visible_htf_idx disagrees with engine.htf anywhere, "
        "including at the exact close/open boundary",
        [("HTF visibility with side='left' (an HTF bar visible one exec bar "
          "early)", mutated(B, "visible_htf_idx", _left, _perm_checks)),
         ("HTF visibility measured against the exec bar's CLOSE",
          mutated(B, "visible_htf_idx", _vs_close, _perm_checks)),
         ("EXPANDING wherever the sign is defined (no growth test, no K "
          "window)", mutated(B, "ribbon_lifecycle", _no_growth, _perm_checks)),
         ("weekly posture blind to its own warm-up",
          mutated(B, "weekly_posture", _warm_blind, _perm_checks))],
        _perm_checks)


# ══════════════════════════════════════════ F-BRK-FUND · the interval sum
def _fund_checks() -> tuple:
    lines, ok = [], True
    # (1) on 4h the interval sum IS the lineage's per-bar-open loop, exactly.
    n = 200
    c = 100.0 + np.cumsum(np.full(n, 0.37))
    fh, fr = funding_series(0, 70, every_h=8, rate=0.0001)
    lf4 = syn_frame("SYNFUND", "4h", c, fund=(fh, fr))
    fdict = {int(x): float(y) for x, y in zip(fh, fr)}
    for ti, xi, d, qty in ((3, 60, 1, 1.0), (10, 11, -1, 0.5),
                           (0, 199, 1, 0.5), (50, 50, 1, 1.0)):
        want = 0.0
        for j in range(ti + 1, xi + 1):
            r = fdict.get(int(lf4.open_ms[j]))
            if r:
                want += r * float(lf4.c[j - 1]) * d * qty
        got = B.funding_interval(lf4, int(lf4.open_ms[ti]),
                                 int(lf4.open_ms[xi]), d, qty)
        g = got["amount"] == want
        ok &= g
        lines.append(mark(g, f"4h [{ti},{xi}] d={d} qty={qty}: interval sum "
                             f"{got['amount']!r} == the lineage's loop "
                             f"{want!r} (BIT-identical, not close)"))
    # (2) on 1d the per-bar-open lookup drops two stamps in three.
    n = 40
    c = 100.0 + np.arange(n) * 1.5
    fh, fr = funding_series(0, 3 * n, every_h=8, rate=0.0002)
    lf1 = syn_frame("SYNFUND", "1d", c, fund=(fh, fr))
    got = B.funding_interval(lf1, int(lf1.open_ms[5]), int(lf1.open_ms[10]),
                             1, 1.0)
    want_n = 3 * 5
    hand = 0.0
    for s in fh[(fh > lf1.open_ms[5]) & (fh <= lf1.open_ms[10])]:
        k = int(np.searchsorted(lf1.open_ms + lf1.step_ms, s, side="right")) - 1
        hand += 0.0002 * float(lf1.c[k]) * 1 * 1.0
    g = (got["n_stamps"] == want_n and got["n_on_bar_open"] == 5
         and got["n_priced"] == want_n and got["n_unpriced"] == 0
         and abs(got["amount"] - hand) < 1e-15)
    ok &= g
    lines.append(mark(g, f"1d, 8h funding, 5 days: interval sum counts "
                         f"{got['n_stamps']} stamps; the per-bar-open lookup "
                         f"would find {got['n_on_bar_open']} "
                         f"({got['n_on_bar_open'] / got['n_stamps']:.3f} of "
                         f"them) — every print COUNTED, amount "
                         f"{got['amount']:.6f}"))
    # (3) an unpriceable stamp is counted, not dropped in silence.
    lf2 = syn_frame("SYNFUND", "1d", c, t0=MS_1D,
                    fund=(np.array([1, 3 * MS_1D], np.int64),
                          np.array([0.001, 0.001])))
    g0 = B.funding_interval(lf2, 0, int(lf2.open_ms[5]), 1, 1.0)
    g = (g0["n_stamps"] == 2 and g0["n_unpriced"] == 1 and g0["n_priced"] == 1)
    ok &= g
    lines.append(mark(g, f"a stamp before the tape's first CLOSE: "
                         f"n_stamps={g0['n_stamps']}, priced={g0['n_priced']}, "
                         f"unpriced={g0['n_unpriced']} — reported, never "
                         f"silently dropped"))
    # (4) account_l's census adds up across a harvested campaign's fractions.
    leg = {"entry_i": 5, "exit_i": 20, "exit_px": float(lf1.c[20]),
           "entry_px": float(lf1.c[5]), "harvest": (12, float(lf1.c[12]), 1.0)}
    acc = B.account_l(lf1, TP.CONTROL_CARD, 1, 4.0, leg)
    cs = acc["funding_census"]
    g = (cs["n_stamps"] == 3 * (7 + 15 + 15) and cs["n_unpriced"] == 0
         and abs((acc["n1"] + acc["n2"]) - (acc["gross_r"] - acc["fee_r"]
                                            - acc["funding_r_uncapped"])) < 1e-9)
    ok &= g
    lines.append(mark(g, f"a harvested campaign: the census sums the three "
                         f"funding legs ({cs['n_stamps']} stamps) and the "
                         f"fractions book the leg (n1 + n2 == net, 1e-9)"))
    return ok, lines


def f_brk_fund() -> bool:
    def _left(lf, stamp_ms):
        return np.searchsorted(lf.open_ms + lf.step_ms,
                               np.atleast_1d(np.asarray(stamp_ms, np.int64)),
                               side="left") - 1

    def _per_bar_open(lf, entry_ms, exit_ms, d, qty):
        fh = {int(x): float(y) for x, y in zip(lf.fund_hour_ms, lf.fund_rate)}
        lo_i = int(np.searchsorted(lf.open_ms, np.int64(entry_ms)))
        hi_i = int(np.searchsorted(lf.open_ms, np.int64(exit_ms)))
        s, n_ = 0.0, 0
        for j in range(lo_i + 1, hi_i + 1):
            r = fh.get(int(lf.open_ms[j]))
            if r:
                s += r * float(lf.c[j - 1]) * d * qty
                n_ += 1
        return {"amount": s, "n_stamps": n_, "n_priced": n_, "n_unpriced": 0,
                "n_on_bar_open": n_}

    return prove(
        "F-BRK-FUND",
        "funding by INTERVAL SUM — entry_ms < funding_hour_ms <= exit_ms — "
        "against the per-bar-open lookup, every print counted",
        "the 4h interval sum is not bit-identical to the lineage's loop, the "
        "1d sum does not find three stamps for every one the per-bar lookup "
        "finds, an unpriceable stamp is dropped without being counted, or a "
        "harvested campaign's fractions do not book the leg",
        [("the price index taken with side='left' (a stamp priced at a close "
          "that had not printed)",
          mutated(B, "funding_price_idx", _left, _fund_checks)),
         ("funding looked up by BAR OPEN (the lineage's 1d defect, restored)",
          mutated(B, "funding_interval", _per_bar_open, _fund_checks))],
        _fund_checks)


# ═══════════════════════════════════════════════ F-BRK-ERA · the holdout law
def _era_tape() -> tuple:
    """A synthetic 5m tape stamped INSIDE the tuning era, with one planted
    hold, so the era guard has something real to refuse."""
    h, l, c, atr, lo, hi, dies, _ = hold_tape(n=60)
    t0 = int(TP.ERA_CUT_MS) - 200 * MS_5M
    lf = syn_frame("SYNERA", "5m", c, h, l, t0=t0)
    cands, _ = B.band_hold_candidates(h, l, c, atr, dies, lo, hi, 1.0, 6,
                                      B.MEM_TTL_BARS)
    legs, _ = B.legs_from_candidates(lf, cands, B.LANE_S1, permit=None)
    return lf, legs


def _era_checks() -> tuple:
    lines, ok = [], True
    g = (B.ERA_CUT_MS is TP.ERA_CUT_MS and B.ERA_CUT_ISO is TP.ERA_CUT_ISO)
    ok &= g
    lines.append(mark(g, f"the cut is the PANEL MODULE's object, not a "
                         f"restatement: {B.ERA_CUT_ISO} / {B.ERA_CUT_MS}"))
    tune_ms, hold_ms = TP.ERA_CUT_MS - 1, TP.ERA_CUT_MS + 1
    cases = ((tune_ms, "holdout", True), (hold_ms, "holdout", False),
             (tune_ms, "tuning", False), (hold_ms, "tuning", True),
             (tune_ms, "full", False), (hold_ms, "full", False))
    for ms, era, want_halt in cases:
        did, why = refused(lambda ms=ms, era=era:
                           B.require_era(ms, "SYNERA", B.LANE_S1, era))
        g = did == want_halt
        ok &= g
        lines.append(mark(g, f"require_era({TP.iso(ms)}, era={era!r}) -> "
                             f"{'HALT' if did else 'passes'} "
                             f"(want {'HALT' if want_halt else 'passes'})"))
    lf, legs = _era_tape()
    g0 = len(legs) == 1
    ok &= g0
    lines.append(mark(g0, f"the synthetic tuning-era tape offers "
                          f"{len(legs)} entry at "
                          f"{TP.iso(int(lf.open_ms[legs[0].entry_i])) if legs else '-'}"))
    did, why = refused(lambda: B.brk_campaigns(
        lf, legs, TP.CONTROL_CARD, T9.V6_ROLES, B.LANE_S1, 0, lf.n - 1,
        ribbon=(B.RIBBON_FAST, B.RIBBON_SLOW), era="holdout"))
    g = did and "holdout" in why and "era" in why.lower()
    ok &= g
    lines.append(mark(g, f"brk_campaigns on that tape with era='holdout' -> "
                         f"{'HALT' if did else 'RODE IT'}: {why[:130]}"))
    rode = B.brk_campaigns(lf, legs, TP.CONTROL_CARD, T9.V6_ROLES, B.LANE_S1,
                           0, lf.n - 1, ribbon=(B.RIBBON_FAST, B.RIBBON_SLOW),
                           era=None)
    g = len(rode) == 1
    ok &= g
    lines.append(mark(g, f"the SAME tape with era=None rides "
                         f"{len(rode)} campaign — so the HALT is the era's "
                         f"doing and not a crash"))
    g = B.LANE_ERA[B.LANE_S1] == "holdout" and B.LANE_ERA[B.LANE_I1] == "full"
    ok &= g
    lines.append(mark(g, f"LANE_ERA: S1={B.LANE_ERA[B.LANE_S1]!r} [R1 tuned "
                         f"pins out of sample], I1={B.LANE_ERA[B.LANE_I1]!r} "
                         f"[R2 nothing tuned]"))
    return ok, lines


# ── THE DEPENDENCY THE HOLDOUT RESTS ON [B5], CHECKED ON REAL BARS ──────────
# A holdout lane detects its macro DIEs on the FULL history and is then
# windowed; the R1 tuning detected ITS DIEs on tapes CUT at the era boundary
# before the detector ran.  The two agree ONLY because the detector is AS-OF.
# If it ever stopped being, the holdout would carry the shape of the tuning
# era and nothing in the lane would notice — so it is proved, not assumed.
# LAW 4: event detection, report-only, no trade and no statistic.
def _detector_asof_checks() -> tuple:
    lines, ok = [], True
    for sym, lens in (("BTCUSDT", "1d"), ("BTCUSDT", "5m")):
        tape, k = real_tape(sym, lens)
        full = macro_dies(tape)
        cut = macro_dies(tape.head(k))
        below = [d for d in full if d[0] < k]
        g = bool(cut) and below == cut
        ok &= g
        lines.append(mark(g, f"{sym} {lens}: {len(full)} macro DIEs on the "
                             f"FULL tape ({tape.n:,} bars), {len(below)} of "
                             f"them below the R1 cut, and the tape CUT at the "
                             f"cut ({k:,} bars) finds {len(cut)} — "
                             f"{'IDENTICAL' if below == cut else 'DIFFERENT'} "
                             f"triple for triple (i, rid, side).  The "
                             f"detector reads no bar after the event"))
    return ok, lines


def f_brk_era() -> bool:
    def _noop(entry_ms, sym, lane, era):
        return None

    def real():
        ok1, l1 = _era_checks()
        ok2, l2 = _detector_asof_checks()
        return ok1 and ok2, l1 + l2

    true_scale = census().run_scale              # captured, not stashed

    def _length_dependent(tape, scale_mult):
        """A named wrong: a detector whose event BARS depend on how many bars
        the tape holds — the exact failure the as-of claim denies."""
        m = true_scale(tape, scale_mult)
        for e in m["macro"]["events"]:
            if e.get("event") == "breakout-die":
                e["i"] = int(e["i"]) + (int(tape.n) % 7)
        return m

    return prove(
        "F-BRK-ERA",
        "a tuning-era entry HALTs — it is not a filter applied after the fact "
        "— and the DIE detector the holdout rests on is as-of on real bars",
        "a tuning-era entry rides a HOLDOUT arm, a holdout entry is refused by "
        "one, the cut is anything but the panel module's own object, or the "
        "dies below the cut differ between the full tape and the cut tape",
        [("the era guard replaced by a no-op",
          mutated(B, "require_era", _noop, _era_checks)),
         ("a macro detector whose event bars depend on the tape's LENGTH",
          mutated(census(), "run_scale", _length_dependent,
                  _detector_asof_checks))],
        real)


# ════════════════════════════════════════ F-BRK-WARM · the inactive components
def _warm_checks() -> tuple:
    lines, ok = [], True
    R = T9.V6_ROLES
    rib = (B.RIBBON_FAST, B.RIBBON_SLOW)
    want = {0: (), 24: (), 25: ("bell_ribbon",), 88: ("bell_ribbon",),
            89: ("bell_window", "bell_ribbon"),
            315: ("bell_window", "bell_ribbon"),
            316: ("bell_window", "bell_tide", "harvest", "bell_ribbon")}
    for ti, warm_names in sorted(want.items()):
        w = B.warm_components(ti, R, rib)
        got = tuple(k for k in B.COMPONENTS if w[k] and k != "trail")
        g = got == warm_names
        ok &= g
        lines.append(mark(g, f"entry bar {ti}: WARM = {got} (want "
                             f"{warm_names}); inactive = "
                             f"{B.inactive_note(w)}"))
    w = B.warm_components(30, R, rib, active=())
    g = (B.inactive_note(w, active=()) ==
         tuple(f"{k}:off" for k in B.COMPONENTS))
    ok &= g
    lines.append(mark(g, f"a component the CARD does not carry is ':off', not "
                         f"':cold' — {B.inactive_note(w, active=())}"))
    # the count has a consequence: a cold window bell is NOT rung
    c, h, l = warm_tape()
    lf = syn_frame("SYNWARM", "5m", c, h, l)
    ra = B.roles_l(lf, R, None)
    bell_bar = int(np.flatnonzero(ra["w_dn"])[0])
    leg = B.ride_leg_l(lf, TP.CONTROL_CARD, R, 1, 30, float(c[30]),
                       float(c[30]) - 60.0, 60.0, lf.n - 1, ribbon=None)
    g = (bell_bar > 30 and leg["exit_reason"] == "corridor_end"
         and leg["inactive"] == ("bell_window:cold", "bell_tide:cold",
                                 "harvest:cold")
         and leg["n_inactive"] == 3)
    ok &= g
    lines.append(mark(g, f"a counter 12/89 cross prints at bar {bell_bar}, but "
                         f"a campaign entered at bar 30 has EMA89 cold: exit "
                         f"is {leg['exit_reason']!r}, inactive "
                         f"{leg['inactive']} (n={leg['n_inactive']}) — skipped, "
                         f"never imputed"))
    tr = B.brk_campaigns(lf, [B.Leg(direction=1, entry_i=30,
                                    stop_px=float(c[30]) - 60.0, r_dist=60.0)],
                         TP.CONTROL_CARD, R, B.LANE_I1, 0, lf.n - 1,
                         ribbon=None, era=None, account=False)
    g = (len(tr) == 1 and tr[0].n_inactive_components == 3
         and tr[0].inactive_components == ("bell_window:cold",
                                           "bell_tide:cold", "harvest:cold"))
    ok &= g
    lines.append(mark(g, f"the count rides ON the campaign: "
                         f"n_inactive_components="
                         f"{tr[0].n_inactive_components if tr else None}, "
                         f"{tr[0].inactive_components if tr else None}"))
    return ok, lines


def f_brk_warm() -> bool:
    def _all_warm(*a, **k):
        return {x: True for x in B.COMPONENTS}

    return prove(
        "F-BRK-WARM",
        "a component whose EMA is not warm on the lens is INACTIVE for that "
        "campaign — counted and printed, never imputed",
        "a cold component acts, a warm one is reported inactive, the per-bar "
        "warm boundaries move off max(period), or the count does not ride on "
        "the campaign",
        [("every component forced WARM (a cold EMA's bell would ring)",
          mutated(B, "warm_components", _all_warm, _warm_checks))],
        _warm_checks)


# ═══════════════════════════════════════════════ F-BRK-GATE · the panel gate
FAKE_PANEL = ("SYNZZ1USDT", "SYNZZ2USDT")
_CL = " " + TP.loao_line_clause("lineage") + "."
GATE_TEXT = ("MECHANICS FIXTURE ONLY — a throwaway filing in a temp registry, "
             "never the registry of record, and no result is ever scored "
             "against it." + _CL)


def _file_arm(root: Path, reg_id: str, arm: dict) -> None:
    TP.register(reg_id, GATE_TEXT, 30, arms=[arm], root=root)


def _gate_checks() -> tuple:
    lines, ok = [], True
    n_before = len(B._FRAMES)
    did, why = refused(lambda: B.run_lane_s1(
        FAKE_PANEL, "P-BRK-S1", "any text at all" + _CL, "P-BRK-S1 vs zero",
        {}, tuned={"lens": "5m", "band": "tap-89", "margin_atr": 1.0,
                   "hold_bars": 6, "ttl_bars": 400, "source": "(none)"},
        head_of_record=TP.UNPINNED))
    g = did and "P-BRK-S1" in why and "SYNZZ" not in why
    ok &= g
    lines.append(mark(g, f"run_lane_s1 with NOTHING filed -> "
                         f"{'HALT' if did else 'RODE IT'}, and the refusal is "
                         f"the REGISTRY's, not a loader's: {why[:120]}"))
    g = len(B._FRAMES) == n_before
    ok &= g
    lines.append(mark(g, f"not one bar was read: the lens-frame memo holds "
                         f"{len(B._FRAMES)} frames, unchanged from "
                         f"{n_before}"))
    did, why = refused(lambda: B.run_lane_i1(
        FAKE_PANEL, "P-BRK-I1", "any text at all" + _CL, "P-BRK-I1 vs zero",
        {}, head_of_record=TP.UNPINNED))
    g = did and "P-BRK-I1" in why
    ok &= g
    lines.append(mark(g, f"run_lane_i1 with NOTHING filed -> "
                         f"{'HALT' if did else 'RODE IT'}: {why[:110]}"))
    with tempfile.TemporaryDirectory(prefix="f-brk-gate-") as td:
        root = Path(td) / "registrations"
        root.mkdir(parents=True)
        _file_arm(root, "P-BRK-X-RUNCELL", TP.arm_spec(
            "wrong runner", FAKE_PANEL, "vs_zero", card=TP.CONTROL_CARD,
            roles=T9.V6_ROLES, loao_line="lineage", era="holdout"))
        did, why = refused(lambda: B.gate(
            "P-BRK-X-RUNCELL", GATE_TEXT, "wrong runner", FAKE_PANEL,
            B.LANE_S1, TP.UNPINNED, root))
        g = did and "runner" in why
        ok &= g
        lines.append(mark(g, f"a run_cell_n arm offered to an EXTERNAL runner "
                             f"-> HALT naming the runner: {why[:110]}"))
        _file_arm(root, "P-BRK-X-LANE", TP.arm_spec(
            "wrong lane", FAKE_PANEL, "vs_zero", lanes=("some-other-lane",),
            loao_line="lineage", era="holdout"))
        did, why = refused(lambda: B.gate(
            "P-BRK-X-LANE", GATE_TEXT, "wrong lane", FAKE_PANEL, B.LANE_S1,
            TP.UNPINNED, root))
        g = did and "lanes" in why
        ok &= g
        lines.append(mark(g, f"a lane the filing does not name -> HALT naming "
                             f"the lanes: {why[:110]}"))
        _file_arm(root, "P-BRK-X-PANEL", TP.arm_spec(
            "wrong panel", ("SYNQQUSDT",), "vs_zero", lanes=(B.LANE_S1,),
            loao_line="lineage", era="holdout"))
        did, why = refused(lambda: B.gate(
            "P-BRK-X-PANEL", GATE_TEXT, "wrong panel", FAKE_PANEL, B.LANE_S1,
            TP.UNPINNED, root))
        g = did and "panel" in why
        ok &= g
        lines.append(mark(g, f"a panel the filing does not name -> HALT naming "
                             f"the panel: {why[:110]}"))
        _file_arm(root, "P-BRK-X-OK", TP.arm_spec(
            "the right arm", FAKE_PANEL, "vs_zero", lanes=(B.LANE_S1,),
            loao_line="lineage", era="holdout"))
        gt = B.gate("P-BRK-X-OK", GATE_TEXT, "the right arm", FAKE_PANEL,
                    B.LANE_S1, TP.UNPINNED, root)
        g = (gt["runner"] == "external" and gt["era"] == "holdout"
             and gt["lanes"] == [B.LANE_S1])
        ok &= g
        lines.append(mark(g, f"a MATCHING filing opens the gate and hands the "
                             f"runner its era: runner={gt['runner']!r}, "
                             f"era={gt['era']!r}, lanes={gt['lanes']}"))
    filed = sorted(p.stem for p in TP.REG_DIR.glob("*.json")
                   if not p.name.endswith(".scored.json")) \
        if TP.REG_DIR.exists() else []
    brk = [x for x in filed if "BRK" in x.upper()]
    g = not brk
    ok &= g
    lines.append(mark(g, f"LAW 4, as of this run: the registry of record "
                         f"files {filed or 'nothing'} — no BRK registration "
                         f"({brk or 'none'}), so no BRK lane can ride"))
    g = bool(B.GATE_HELPER == "TP.require_arm" and B.gate.__doc__
             and "require_registered" in B.gate.__doc__)
    ok &= g
    lines.append(mark(g, f"gate helper of record: {B.GATE_HELPER} — the panel "
                         f"module's CURRENT external door; the "
                         f"require_registered fallback is named and NOT used"))
    return ok, lines


def f_brk_gate() -> bool:
    def _open(reg_id, text, arm, panel, lane, head_of_record=None,
              reg_root=None):
        return {"runner": "external", "registration": reg_id, "arm": arm,
                "panel": list(panel), "lanes": [lane], "era": "full",
                "registration_sha256": "0" * 64}

    return prove(
        "F-BRK-GATE",
        "every runner calls the panel gate helper before replaying a single "
        "bar; unregistered -> HALT",
        "a runner rides one bar without a filed arm, the refusal comes from a "
        "loader rather than the registry, a run_cell_n arm or a wrong "
        "panel/lane opens the external door, or a BRK registration is found in "
        "the registry of record while this fixture claims none",
        [("the gate replaced by an always-open no-op",
          mutated(B, "gate", _open, _gate_checks))],
        _gate_checks)


# ═════════════════════════════════════════ F-C10-TOLL · the toll is READ
def _toll_checks() -> tuple:
    from tierc10_census_fixtures import toll_literals                # noqa: PLC0415
    lines, ok = [], True
    src = (ROOT / "scripts" / "tierc10_brk.py").read_text(encoding="utf-8")
    hits = toll_literals(src)
    g = not hits
    ok &= g
    lines.append(mark(g, f"AST scan of scripts/tierc10_brk.py for a numeric "
                         f"literal in a TOLL position: {hits or 'none'}"))
    v = B.toll_pct_of_1r(0.27, 2.0, 1.0)
    g = abs(v - 13.5) < 1e-12
    ok &= g
    lines.append(mark(g, f"toll_pct_of_1r(0.27 ATR, R = 2.0 ATR) = {v} % of "
                         f"1R (hand: 0.27 / 2.0 x 100 = 13.5)"))
    v2 = B.toll_pct_of_1r(0.27, 1.0, 1.0)
    g = abs(v2 - 27.0) < 1e-12
    ok &= g
    lines.append(mark(g, f"at the 1.0 ATR rail the same toll is {v2} % of 1R "
                         f"— the scalper's arithmetic, ~9x the 4h card's"))
    did, why = refused(lambda: B.grid_toll_atr("BTC", "5m", "DIE"))
    g = did
    ok &= g
    lines.append(mark(g, f"grid_toll_atr with no filed grid -> "
                         f"{'HALT' if did else 'returned a number'}: "
                         f"{why[:110]} — a toll that cannot be READ is not a "
                         f"toll that may be guessed"))
    g = (B.toll_class(B.ANCHOR_MEMORY) == "flip-hold"
         and B.toll_class(B.ANCHOR_BAND, "ribbon-89/127")
         == "retest-hold-ribbon89_127"
         and B.toll_class(B.ANCHOR_BAND, "ribbon89_127")
         == "retest-hold-ribbon89_127")
    ok &= g
    lines.append(mark(g, f"the grid ROW a lane's toll comes from: memory "
                         f"anchor -> {B.toll_class(B.ANCHOR_MEMORY)!r}, band "
                         f"anchor -> "
                         f"{B.toll_class(B.ANCHOR_BAND, 'ribbon-89/127')!r} "
                         f"— built from the band actually ridden, in the "
                         f"CENSUS's spelling, from EITHER house style"))
    # ── THE SPELLING LAW, BOTH DIRECTIONS, AGAINST THE FILED CENSUS ─────────
    C = census()
    mine = tuple(B.census_band(b) for b in B.R1_BANDS)
    g = (sorted(mine) == sorted(C.RETEST_BAND_NAMES)
         and all(B.band_key(n) in B.R1_BANDS for n in C.RETEST_BAND_NAMES)
         and all(B.census_band(B.band_key(n)) == n
                 for n in C.RETEST_BAND_NAMES))
    ok &= g
    lines.append(mark(g, f"census_band/band_key round-trip on ALL five, both "
                         f"ways: {list(B.R1_BANDS)} <-> "
                         f"{list(C.RETEST_BAND_NAMES)} "
                         f"(tierc10_census.RETEST_BAND_NAMES, the names the "
                         f"filed grid keys its rows on)"))
    cc = np.asarray(np.linspace(50.0, 900.0, 1200)
                    + 40.0 * np.sin(np.arange(1200) / 11.0), float)
    worst, where = 0.0, ""
    for nm in B.R1_BANDS:
        a_lo, a_hi = B.r1_band(nm)(cc)
        b_lo, b_hi = C.band_of(B.census_band(nm))(cc.copy())
        for x, y, tag in ((a_lo, b_lo, "lo"), (a_hi, b_hi, "hi")):
            if not np.array_equal(np.isnan(x), np.isnan(y)):
                worst, where = float("inf"), f"{nm} {tag} NaN pattern"
            d = float(np.nanmax(np.abs(x - y))) if np.isfinite(x).any() else 0.0
            if d > worst:
                worst, where = d, f"{nm} {tag}"
    g = worst == 0.0
    where = where or "identical, NaN pattern included"
    ok &= g
    lines.append(mark(g, f"and the BAND MATH is the same object either side "
                         f"of the spelling: r1_band vs tierc10_census.band_of "
                         f"on 1200 bars x all five bands, worst |diff| = "
                         f"{worst:.3e} ({where})"))
    # ── A REAL ROW OUT OF THE FILED GRID, FOR THE BAND THE TUNING SCORED.
    # ── The absent-grid HALT below proves the reader refuses; this proves it
    # ── can also READ — the half that was missing when P-BRK-S1's "NET OF
    # ── MEASURED 5m TOLL" turned out to be unreachable (review).
    if B.TUNING_RESULT_FOR["5m"].exists() and C.OUT.joinpath(
            "outcome_grid.parquet").exists():
        tp = B.tuned_pins("5m")
        cls = B.toll_class(B.ANCHOR_BAND, tp["band"])
        toll = B.grid_toll_atr("BTCUSDT", "5m", cls)
        mem = B.grid_toll_atr("BTCUSDT", "1d",
                              B.toll_class(B.ANCHOR_MEMORY))
        pct = B.toll_pct_of_1r(toll, 2.0, 1.0)
        g = (np.isfinite(toll) and toll > 0 and np.isfinite(mem)
             and abs(pct - toll / 2.0 * 100.0) < 1e-12)
        ok &= g
        lines.append(mark(g, f"THE FILED GRID, READ: class {cls!r} (the band "
                             f"the R1 tuning scored) x BTCUSDT x 5m -> "
                             f"toll_atr {toll} = {pct:.4f} % of 1R at R = 2.0 "
                             f"ATR (hand: {toll} / 2.0 x 100); the memory "
                             f"anchor's 'flip-hold' x BTCUSDT x 1d -> "
                             f"{mem}.  Both READ, neither typed"))
        old_cls = "retest-hold-" + tp["band"]
        did, why = refused(lambda: B.grid_toll_atr("BTCUSDT", "5m", old_cls))
        g = did and "0 row" in why
        ok &= g
        lines.append(mark(g, f"and the OPERATOR-spelled class {old_cls!r} — "
                             f"what this module asked the grid for BEFORE the "
                             f"spelling law, and the reason P-BRK-S1's toll "
                             f"print was unreachable — is still a row no grid "
                             f"holds: {'HALT' if did else 'IT RETURNED A NUMBER'} "
                             f"{why[:70]}"))
    did, why = refused(lambda: B.toll_class(B.ANCHOR_BAND))
    g = did
    ok &= g
    lines.append(mark(g, f"the band anchor's toll class with no band -> "
                         f"{'HALT' if did else 'guessed one'}: {why[:90]}"))
    # stamp_toll RIDES THE READER, BOTH WAYS.  A row the grid does not hold
    # is a HALT with nothing stamped; a row it does hold is stamped on every
    # campaign.  (Until the census filed the R1 classes this leg could only
    # make the first claim, and that is precisely how the unreachable toll
    # print survived review-less: a reader proved only to REFUSE was never
    # proved to READ.)
    fake = [NS(symbol="NOSUCHUSDT", r_dist=2.0, atr_at_entry=1.0)]
    did, why = refused(lambda: B.stamp_toll(fake, "5m", B.ANCHOR_BAND,
                                            "tap-89"))
    g = did and not hasattr(fake[0], "toll_pct_of_1r")
    ok &= g
    lines.append(mark(g, f"stamp_toll for an asset the grid has no row for -> "
                         f"{'HALT' if did else 'stamped something'}, and no "
                         f"campaign was stamped: {why[:90]}"))
    if C.OUT.joinpath("outcome_grid.parquet").exists():
        band = B.tuned_pins("5m")["band"] if B.TUNING_RESULT_FOR["5m"].exists() \
            else B.BAND_EXAMPLE
        real2 = [NS(symbol="BTCUSDT", r_dist=2.0, atr_at_entry=1.0),
                 NS(symbol="BTCUSDT", r_dist=1.0, atr_at_entry=1.0),
                 NS(symbol="BTCUSDT", r_dist=4.0, atr_at_entry=2.0),
                 NS(symbol="ETHUSDT", r_dist=2.0, atr_at_entry=1.0)]
        rep = B.stamp_toll(real2, "5m", B.ANCHOR_BAND, band)
        want = {a: B.grid_toll_atr(a, "5m", rep["cls"]) for a in rep["per_asset"]}
        pct = [t.toll_pct_of_1r for t in real2]
        g = (rep["per_asset"] == want and len(want) == 2
             and all(np.isfinite(t.toll_atr_grid) for t in real2)
             and abs(pct[1] - 2.0 * pct[0]) < 1e-9        # half the R, twice the toll
             and abs(pct[2] - pct[0]) < 1e-9              # R in ATR units is what counts
             and want["BTCUSDT"] != want["ETHUSDT"]       # the toll is PER ASSET
             and abs(pct[3] - want["ETHUSDT"] / 2.0 * 100.0) < 1e-9)
        ok &= g
        lines.append(mark(g, f"stamp_toll for the band the tuning SCORED -> "
                             f"cls {rep['cls']!r}, per-asset tolls READ "
                             f"{rep['per_asset']}, campaigns stamped "
                             f"{[round(x, 4) for x in pct]} % of 1R: half the "
                             f"R pays twice the toll, R in ATR units is what "
                             f"decides (2.0/1.0 == 4.0/2.0), and the two "
                             f"assets differ because the GRID says they do"))
    g = B.FEE_BPS_SIDE is RC.FEE_BPS_SIDE
    ok &= g
    lines.append(mark(g, f"the fee is the estate's OBJECT "
                         f"(tierc7_rules.FEE_BPS_SIDE = {B.FEE_BPS_SIDE} bps a "
                         f"side = {2 * B.FEE_BPS_SIDE} bps round trip), not a "
                         f"literal"))
    return ok, lines


def f_c10_toll() -> bool:
    def planted():
        from tierc10_census_fixtures import toll_literals            # noqa: PLC0415
        src = (ROOT / "scripts" / "tierc10_brk.py").read_text(encoding="utf-8")
        bad = src + "\n\ntoll_atr = 0.2670\n"
        hits = toll_literals(bad)
        return not hits, f"the scan on the corrupted COPY found {hits}"

    def planted_kw():
        from tierc10_census_fixtures import toll_literals            # noqa: PLC0415
        src = (ROOT / "scripts" / "tierc10_brk.py").read_text(encoding="utf-8")
        bad = src + "\n\n_x = grid_toll_atr('BTC', '5m', 'DIE')\n" \
                    "_y = dict(toll_atr=0.27)\n"
        hits = toll_literals(bad)
        return not hits, f"the scan on the corrupted COPY found {hits}"

    return prove(
        "F-C10-TOLL",
        "the 5m toll is READ from the filed grid and never typed (AST scan + "
        "the reader HALTs without a grid)",
        "a numeric literal sits in a toll position anywhere in "
        "scripts/tierc10_brk.py, the fee stops being the estate object, or "
        "grid_toll_atr invents a number when the grid is absent",
        [("a module-level `toll_atr = 0.2670` planted in a COPY of the source",
          planted),
         ("a `dict(toll_atr=0.27)` keyword planted in a COPY of the source",
          planted_kw)],
        _toll_checks)


# ══════════════════════════════════ F-BRK-CLOSURE · the decision half is clean
# THE PRE-EXISTING ANALYTICS CLOSURE, PINNED BY NAME.  `analytics` is NOT the
# range machine: it is the estate's display/measurement package, and it enters
# this module's closure through the LINEAGE's own baseline runners
# (tierc2_baseline .. tierc8), which every tier since TIER-C2 has imported.
# That is pre-existing and is reported, not failed.  It is pinned as an EXACT
# SET so that a NEW analytics module — `analytics.rangefinder_census` above all
# — could not slip in unnoticed behind the word "pre-existing".
ANALYTICS_PREEXISTING = ["analytics", "analytics.momentum", "analytics.structure",
                         "analytics.volatility", "analytics.vwap"]
RANGE_WORDS = ("rangefinder", "tierc10_census", "tierc10_null")
CLOSURE_PROBE = (
    "import sys, json; sys.path[:0] = %r;\n"
    "import %s;\n"
    "print(json.dumps(sorted(m for m in sys.modules "
    "if any(w in m for w in %r) or m == 'analytics' "
    "or m.startswith('analytics.'))))"
)


def _probe_closure(paths: list, mod: str) -> list:
    p = subprocess.run([PY, "-c", CLOSURE_PROBE % (paths, mod, RANGE_WORDS)],
                       capture_output=True, text=True, env=dict(os.environ),
                       cwd=str(ROOT))
    if p.returncode != 0:
        return ["<probe failed: " + p.stderr[-200:] + ">"]
    return json.loads(p.stdout.strip().splitlines()[-1])


def _closure_checks() -> tuple:
    import ast                                               # noqa: PLC0415
    lines, ok = [], True
    got = _probe_closure([str(ROOT), str(ROOT / "scripts")], "tierc10_brk")
    rng = [m for m in got if any(w in m for w in RANGE_WORDS)]
    g = not rng
    ok &= g
    lines.append(mark(g, f"a FRESH interpreter importing only tierc10_brk "
                         f"loads NO range module ({rng or 'none'}); the words "
                         f"searched are {list(RANGE_WORDS)}"))
    an = [m for m in got if m == "analytics" or m.startswith("analytics.")]
    g = an == ANALYTICS_PREEXISTING
    ok &= g
    lines.append(mark(g, f"the analytics closure is EXACTLY the lineage's "
                         f"pre-existing set {an} — it arrives through "
                         f"tierc2_baseline..tierc8 (the estate's display "
                         f"package, not the range machine), and the set is "
                         f"pinned so a new member cannot slip in"))
    src = (ROOT / "scripts" / "tierc10_brk.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    top = [n for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom))]
    names = sorted({(a.name if isinstance(n, ast.Import) else (n.module or ""))
                    for n in top for a in n.names})
    bad = [x for x in names if "rangefinder" in x or "census" in x
           or x.startswith("analytics")]
    g = not bad
    ok &= g
    lines.append(mark(g, f"module-level imports: {names} — none reaches the "
                         f"range machine ({bad or 'none'})"))
    inside = []
    for fn in ast.walk(tree):
        if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        for sub in ast.walk(fn):
            if isinstance(sub, ast.Import) and any(
                    "census" in a.name or "rangefinder" in a.name
                    for a in sub.names):
                inside.append(fn.name)
    g = sorted(set(inside)) == ["grid_toll_atr", "macro_signals"]
    ok &= g
    lines.append(mark(g, f"the range machine is reached ONLY inside the named "
                         f"adapters: {sorted(set(inside))} (want "
                         f"['grid_toll_atr', 'macro_signals'])"))
    return ok, lines


def f_brk_closure() -> bool:
    def planted_scan():
        import ast                                           # noqa: PLC0415
        src = (ROOT / "scripts" / "tierc10_brk.py").read_text(encoding="utf-8")
        bad = "import tierc10_census\n" + src
        tree = ast.parse(bad)
        top = [n for n in tree.body
               if isinstance(n, (ast.Import, ast.ImportFrom))]
        names = sorted({(a.name if isinstance(n, ast.Import)
                         else (n.module or ""))
                        for n in top for a in n.names})
        hit = [x for x in names if any(w in x for w in RANGE_WORDS)]
        return not hit, f"the scan on the corrupted COPY found {hit}"

    def planted_probe():
        """A SHIM that imports tierc10_brk AND the range machine, run through
        the SAME subprocess probe — which must then see the range modules.  A
        probe that could not see a planted import would make the real leg's
        empty result meaningless."""
        with tempfile.TemporaryDirectory(prefix="f-brk-closure-") as td:
            (Path(td) / "brk_planted.py").write_text(
                "import tierc10_brk\n"
                "import analytics.rangefinder_census\n"
                "import tierc10_census\n", encoding="utf-8")
            got = _probe_closure([str(ROOT), str(ROOT / "scripts"), td],
                                 "brk_planted")
            hit = [m for m in got if any(w in m for w in RANGE_WORDS)]
            return not hit, (f"the probe on the planted shim found "
                             f"{hit[:4]} ({len(hit)} range modules) out of "
                             f"{len(got)}")

    return prove(
        "F-BRK-CLOSURE",
        "the decision half imports no RANGE code; the machine is reached only "
        "inside the named adapters",
        "importing tierc10_brk loads any module whose name reaches the range "
        "machine, the analytics closure gains a member the lineage did not "
        "already carry, a module-level import names the census, or a function "
        "other than macro_signals / grid_toll_atr imports it",
        [("a top-level `import tierc10_census` planted in a COPY of the "
          "source (AST scan)", planted_scan),
         ("a COPY importing analytics.rangefinder_census at module level, run "
          "through the same subprocess probe", planted_probe)],
        _closure_checks)


# ═══════════════════════════════ F-BRK-TUNED · the R1 pins are READ, not typed
def _tuned_checks() -> tuple:
    lines, ok = [], True
    with tempfile.TemporaryDirectory(prefix="f-brk-tuned-") as td:
        p = Path(td) / "TUNING_RESULT.json"
        did, why = refused(lambda: B.tuned_pins("5m", p))
        g = did and "absent" in why
        ok &= g
        lines.append(mark(g, f"with NO TUNING_RESULT.json -> "
                             f"{'HALT' if did else 'invented pins'}: "
                             f"{why[:120]}"))
        # THE SHAPES THE CENSUS BUILDER MIGHT FILE — the reader must find the
        # scored cell in each, and must not care which one it gets.
        # THE SHAPES THE CENSUS BUILDER MIGHT FILE, IN BOTH HOUSE STYLES.
        # The band is written the CENSUS's way in half of them, because that
        # is what the file of record actually holds and a reader tested only
        # against its own spelling is a reader that has never been tested.
        for name, doc in (
                ("flat, operator spelling",
                 {"band": "ribbon-89/127", "margin_atr": 0.5, "hold_bars": 12}),
                ("flat, CENSUS spelling",
                 {"band": "ribbon89_127", "margin_atr": 0.5, "hold_bars": 12}),
                ("under 'scored'",
                 {"scored": {"band": "ribbon89_127", "margin_atr": 0.5,
                             "hold_bars": 12}, "grid": []}),
                ("under 'result'",
                 {"result": {"band": "ribbon-89/127", "margin_atr": 0.5,
                             "hold_bars": 12}}),
                ("per-lens map",
                 {"by_lens": {"5m": {"band": "ribbon89_127",
                                     "margin_atr": 0.5, "hold_bars": 12}}}),
                ("lens key at the top",
                 {"5m": {"band": "ribbon-89/127", "margin_atr": 0.5,
                         "hold_bars": 12}, "1d": {}}),
                ("aliases", {"band_name": "ribbon89_127", "margin": 0.5,
                             "hold": 12})):
            p.write_text(json.dumps(doc))
            got = B.tuned_pins("5m", p)
            g = (got["band"] == "ribbon-89/127"
                 and got["band_census"] == "ribbon89_127"
                 and got["margin_atr"] == 0.5 and got["hold_bars"] == 12
                 and got["ttl_bars"] == B.MEM_TTL_BARS)
            ok &= g
            lines.append(mark(g, f"shape {name!r}: as filed "
                                 f"{got['band_as_filed']!r} -> band "
                                 f"{got['band']!r} / census "
                                 f"{got['band_census']!r}, "
                                 f"margin={got['margin_atr']} "
                                 f"hold={got['hold_bars']} ttl="
                                 f"{got['ttl_bars']} (ttl defaults to the "
                                 f"frozen MEM_TTL_BARS)"))
        for name, doc, word in (
                ("a band outside the operator's five",
                 {"band": "ema200_300", "margin_atr": 1.0, "hold_bars": 6},
                 "five"),
                ("a band that only LOOKS like one of the five",
                 {"band": "ribbon89_200", "margin_atr": 1.0, "hold_bars": 6},
                 "five"),
                ("no margin", {"band": "tap-89", "hold_bars": 6}, "margin"),
                ("no hold", {"band": "tap-89", "margin_atr": 1.0}, "hold"),
                ("a non-positive hold",
                 {"band": "tap-89", "margin_atr": 1.0, "hold_bars": 0},
                 "non-positive"),
                ("a cell whose OWN lens is not the lens asked for",
                 {"lens": "1d", "band": "tap89", "margin_atr": 1.0,
                  "hold_bars": 6}, "not '5m'"),
                ("no scored cell at all", {"grid": [1, 2, 3]}, "no scored cell")):
            p.write_text(json.dumps(doc))
            did, why = refused(lambda: B.tuned_pins("5m", p))
            g = did and word in why
            ok &= g
            lines.append(mark(g, f"{name} -> {'HALT' if did else 'accepted'} "
                                 f"naming {word!r}: {why[:100]}"))
        did, why = refused(lambda: B.tuned_pins("4h"))
        g = did and "no tuned pins exist" in why
        ok &= g
        lines.append(mark(g, f"a lens the R1 protocol never tuned ('4h') -> "
                             f"{'HALT' if did else 'invented a file'}: "
                             f"{why[:100]}"))
    # ── THE FILES OF RECORD, READ.  Everything above is a document this
    # ── fixture wrote itself; this is the one the census actually filed, and
    # ── it is the leg that would have caught the spelling HALT on day one.
    C = census()
    mine = {k: v.name for k, v in B.TUNING_RESULT_FOR.items()}
    theirs = dict(C.TUNING_RESULT_NAME)
    g = mine == theirs
    ok &= g
    lines.append(mark(g, f"the path map is the census builder's own ({mine} "
                         f"vs tierc10_census.TUNING_RESULT_NAME {theirs}) — "
                         f"one file per tuned lens, and they cannot drift in "
                         f"silence"))
    for lens in B.TUNED_LENSES:
        p = B.TUNING_RESULT_FOR[lens]
        if not p.exists():
            lines.append(mark(True, f"lens {lens}: {p.name} is NOT filed yet "
                                    f"— tuned_pins HALTs, which the leg above "
                                    f"proves; nothing to read"))
            continue
        got = B.tuned_pins(lens)
        cell = got["cell"]
        g = (got["band"] in B.R1_BANDS
             and got["band_census"] in C.RETEST_BAND_NAMES
             and got["band_as_filed"] == cell.get("band")
             and str(cell.get("lens")) == lens
             and got["margin_atr"] > 0 and got["hold_bars"] > 0)
        ok &= g
        lines.append(mark(g, f"THE FILE OF RECORD, lens {lens}: {p.name} "
                             f"names band {got['band_as_filed']!r} -> "
                             f"{got['band']!r} (one of the operator's five) "
                             f"-> census class "
                             f"{B.toll_class(B.ANCHOR_BAND, got['band'])!r} "
                             f"(one of {len(C.RETEST_BAND_NAMES)} the grid "
                             f"carries); margin {got['margin_atr']}, hold "
                             f"{got['hold_bars']}, n {cell.get('n')}"))
    a, b = B.TUNING_RESULT_FOR["5m"], B.TUNING_RESULT_FOR["1d"]
    if a.exists() and b.exists():
        p5, p1 = B.tuned_pins("5m"), B.tuned_pins("1d")
        g = (p5["source"] != p1["source"]
             and (p5["band"], p5["margin_atr"], p5["hold_bars"])
             != (p1["band"], p1["margin_atr"], p1["hold_bars"]))
        ok &= g
        lines.append(mark(g, f"and the two lenses are NOT the same cell — 5m "
                             f"({p5['band']}, {p5['margin_atr']}, "
                             f"{p5['hold_bars']}) vs 1d ({p1['band']}, "
                             f"{p1['margin_atr']}, {p1['hold_bars']}) — so a "
                             f"single-path reader WOULD have mis-pinned the "
                             f"1d Tier-E print, silently"))
        did, why = refused(lambda: B.tuned_pins("1d", a))
        g = did and "not '1d'" in why
        ok &= g
        verb = "HALT" if did else "ACCEPTED THE WRONG CELL"
        lines.append(mark(g, f"the 5m FILE OF RECORD offered to the 1d lens "
                             f"-> {verb}: {why[:110]}"))
    for nm in B.R1_BANDS:
        bd = B.r1_band(nm)
        c = np.linspace(100.0, 300.0, 400)
        lo, hi = bd(c)
        warm = max(bd.periods)
        g = (np.all(~np.isfinite(lo[:warm])) and np.all(np.isfinite(lo[warm:]))
             and np.all(hi >= lo) if np.isfinite(hi[warm:]).all() else False)
        g = bool(np.all(~np.isfinite(lo[:warm]))
                 and np.all(np.isfinite(lo[warm:]))
                 and np.all(hi[warm:] >= lo[warm:]))
        ok &= g
        lines.append(mark(g, f"R1 band {nm!r} ({bd.label}): NaN until bar "
                             f"{warm} (its slowest EMA's own period), then "
                             f"lo <= hi everywhere"))
    did, why = refused(lambda: B.r1_band("ema89"))
    g = did
    ok &= g
    lines.append(mark(g, f"a band the operator did not name -> "
                         f"{'HALT' if did else 'accepted'}: {why[:90]}"))
    return ok, lines


def f_brk_tuned() -> bool:
    def _default(lens="5m", path=None):
        """A named wrong: the reader falls back to the pins on disk — a
        COMPLETE record, so the leg fails on the CLAIM and not on a KeyError."""
        return {"lens": lens, "band": "tap-89", "band_as_filed": "tap-89",
                "band_census": "tap89", "margin_atr": 1.0, "hold_bars": 6,
                "ttl_bars": B.MEM_TTL_BARS, "source": "(fallback)",
                "cell": {"lens": lens, "band": "tap-89"}}

    def _one_path(lens="5m", path=None):
        """A named wrong: ONE tuning file for every lens, and the lens field
        overwritten with the one asked for — the defect review found."""
        p = Path(path) if path else B.TUNING_RESULT_FOR["5m"]
        raw = json.loads(p.read_text()) if p.exists() else {}
        cell = B._tune_dig(raw, lens) or {}
        band = B.band_key(cell.get("band", "tap-89"))
        return {"lens": lens, "band": band, "band_as_filed": cell.get("band"),
                "band_census": B.census_band(band),
                "margin_atr": float(cell.get("margin_atr", 1.0)),
                "hold_bars": int(cell.get("hold_bars", 6)),
                "ttl_bars": B.MEM_TTL_BARS, "source": str(p), "cell": cell}

    return prove(
        "F-BRK-TUNED",
        "the band and hold pins are READ — from the census builder's own file "
        "FOR THE LENS ASKED FOR, in either house spelling — and every way of "
        "not having them is a HALT",
        "the reader invents a pin, falls back to the pins on disk, reads one "
        "lens's cell for another, accepts a band outside the operator's five "
        "in any spelling, accepts a missing or non-positive margin/hold, or an "
        "R1 band is readable before its slowest EMA is warm",
        [("the reader given a silent fallback to the pins on disk",
          mutated(B, "tuned_pins", _default, _tuned_checks)),
         ("ONE tuning file for every lens, its lens field overwritten",
          mutated(B, "tuned_pins", _one_path, _tuned_checks))],
        _tuned_checks)


# ══════════════════════════ F-BRK-LANE-SYN · both lanes, end to end, synthetic
def _lane_syn_checks() -> tuple:
    """BOTH LANES DRIVEN END TO END ON SYNTHETIC TAPES: anchor -> permission ->
    stop -> ride -> accounting.  No registry, no real asset, no P-BRK number —
    the campaign's existence and its STOP GEOMETRY are the claims."""
    lines, ok = [], True
    R = T9.V6_ROLES
    rib = (B.RIBBON_FAST, B.RIBBON_SLOW)
    # ── S1: a 5m tape stamped in the HOLDOUT era, a 4h tape that carries the
    # ── tide, and the real tide map between them.
    h, l, c, atr, lo, hi, dies, ext = hold_tape(n=60)
    t0_4h = int(TP.ERA_CUT_MS) + MS_4H
    c4_up = np.linspace(50.0, 400.0, 500)
    c4_dn = np.linspace(400.0, 50.0, 500)
    t0_5m = t0_4h + 450 * MS_4H
    fh, fr = funding_series(t0_5m, 4, every_h=1, rate=0.0003)
    lf = syn_frame("SYNS1", "5m", c, h, l, t0=t0_5m, fund=(fh, fr))
    cands, tal = B.band_hold_candidates(h, l, c, atr, dies, lo, hi, 1.0, 6,
                                        B.MEM_TTL_BARS)
    got = {}
    # THE TWO 4h TAPES WEAR THE SAME SYMBOL ON PURPOSE.  A memo keyed on the
    # NAME would serve the rising tape's EMAs to the falling one and report
    # tide 0 where the answer is -1 (measured: it did, before LensFrame.uid).
    for label, c4 in (("aligned", c4_up), ("opposed", c4_dn)):
        f4 = syn_frame("SYNS1", "4h", c4, t0=t0_4h)
        tide, _ = B.tide_4h_for_exec(lf.open_ms, f4, R)
        legs, ref = B.legs_from_candidates(
            lf, cands, B.LANE_S1,
            permit=lambda i, d, _t=tide: B.s1_permission(i, d, _t))
        tr = B.brk_campaigns(lf, legs, TP.CONTROL_CARD, R, B.LANE_S1, 0,
                             lf.n - 1, ribbon=rib, era="holdout")
        got[label] = (tr, ref, int(tide[cands[0].known_i]))
    g = (len(got["aligned"][0]) == 1 and len(got["opposed"][0]) == 0
         and got["opposed"][1]["permission"] == 1
         and got["aligned"][2] == 1 and got["opposed"][2] == -1)
    ok &= g
    lines.append(mark(g, f"the memo is keyed on the FRAME, not the name: two "
                         f"4h tapes under the symbol 'SYNS1' read tides "
                         f"{got['aligned'][2]:+d} and {got['opposed'][2]:+d} "
                         f"(a name-keyed memo returns 0 for the second) "
                         f"[F-C8-MATCH]"))
    lines.append(mark(g, f"S1 end to end: 4h tide "
                         f"{got['aligned'][2]:+d} -> "
                         f"{len(got['aligned'][0])} campaign; tide "
                         f"{got['opposed'][2]:+d} -> "
                         f"{len(got['opposed'][0])} campaigns "
                         f"(permission refusals "
                         f"{got['opposed'][1]['permission']}, COUNTED)"))
    t = got["aligned"][0][0]
    a_sig = float(lf.atr[t.entry_i])
    want_stop = min(ext - B.STOP_BUF_ATR * a_sig,
                    float(lf.c[t.entry_i]) - B.MIN_STOP_ATR * a_sig)
    g = (t.stop_px == want_stop
         and abs(t.r_dist - abs(float(lf.c[t.entry_i]) - want_stop)) < 1e-12
         and t.entry_i == 26 and t.lane == B.LANE_S1)
    ok &= g
    lines.append(mark(g, f"the stop is spring_stop's geometry on the RETEST "
                         f"extreme {ext}: farther of "
                         f"{{extreme - {B.STOP_BUF_ATR} ATR, entry - "
                         f"{B.MIN_STOP_ATR} ATR}} = {t.stop_px} (hand "
                         f"{want_stop}), R = {t.r_dist:.6f}"))
    # BOTH BRANCHES OF "the farther of", as units — one example would leave
    # half the geometry unproved.
    for d, extreme, entry, want_px, want_rail in (
            (1, 99.0, 100.0, 98.5, False),      # the pivot (retest) binds
            (1, 99.9, 100.0, 99.0, True),       # the rail binds
            (-1, 101.0, 100.0, 101.5, False),
            (-1, 100.1, 100.0, 101.0, True)):
        st = B.brk_stop(d, extreme, 5, entry, 1.0)
        g = (abs(st.stop_px - want_px) < 1e-12
             and bool(st.rail_binding) == want_rail)
        ok &= g
        lines.append(mark(g, f"brk_stop(d={d:+d}, extreme {extreme}, entry "
                             f"{entry}, ATR 1.0) = {st.stop_px} (want "
                             f"{want_px}), rail_binding={st.rail_binding} "
                             f"(want {want_rail})"))
    g = (t.funding_r != 0.0
         and t.funding_census["n_stamps"] == t.funding_census["n_priced"]
         and t.fee_r > 0)
    ok &= g
    lines.append(mark(g, f"the campaign pays: fee_r {t.fee_r:.6f} (the estate "
                         f"object), funding_r {t.funding_r:.6f} over "
                         f"{t.funding_census['n_stamps']} interval-sum stamps, "
                         f"net_r {t.net_r:.6f}"))
    g = t.entry_ms > TP.ERA_CUT_MS
    ok &= g
    lines.append(mark(g, f"and it enters in the HOLDOUT era "
                         f"({TP.iso(int(t.entry_ms))} > {TP.ERA_CUT_ISO})"))
    # ── I1: a 1d tape, a memory-line flip, and the real i1_permission with
    # ── hand-built lifecycle/posture arrays (the arrays themselves are proved
    # ── in F-BRK-PERM; what is proved HERE is the wiring).
    h, l, c, atr, lo, hi, dies, ext = hold_tape(n=80, die_i=10, touch_i=20)
    fh, fr = funding_series(0, 300, every_h=8, rate=0.0001)
    lfd = syn_frame("SYNI1", "1d", c, h, l, t0=0, fund=(fh, fr))
    flips = [{"i": 20, "polarity": "support", "rid": 7}]
    cd, tl = B.memory_flip_candidates(h, l, dies, flips, lfd.n)
    widx = B.visible_htf_idx(lfd.open_ms,
                             np.arange(0, 100 * MS_1D, 7 * MS_1D, np.int64),
                             7 * MS_1D)
    for label, dd, wk, want in (("both agree", 1, 1, 1),
                                ("daily NONE", 0, 1, 0),
                                ("weekly cold", 1, 0, 0),
                                ("weekly against", 1, -1, 0)):
        life_dir = np.full(lfd.n, dd, np.int64)
        wks = np.full(20, wk, np.int64)
        legs, ref = B.legs_from_candidates(
            lfd, cd, B.LANE_I1,
            permit=lambda i, d, _l=life_dir, _w=wks, _x=widx:
                B.i1_permission(i, d, _l, _w, _x))
        tr = B.brk_campaigns(lfd, legs, TP.CONTROL_CARD, R, B.LANE_I1, 0,
                             lfd.n - 1, ribbon=rib, era="full")
        g = len(tr) == want
        ok &= g
        lines.append(mark(g, f"I1 end to end, {label} (daily {dd:+d}, weekly "
                             f"{wk:+d}) -> {len(tr)} campaigns (want {want}); "
                             f"entry bar "
                             f"{tr[0].entry_i if tr else '-'} = flip 20 + "
                             f"FLIP_HOLD_BARS {B.FLIP_HOLD_BARS}"))
    return ok, lines


def f_brk_lane_syn() -> bool:
    def _always(entry_i, direction, tide_state_exec):
        return {"ok": True, "tide_4h": 0, "why": ""}

    def _no_beyond(direction, retest_extreme, touch_i, entry_px, atr_sig,
                   rail_atr=B.MIN_STOP_ATR):
        """A named wrong: the stop sits AT the retest extreme — the card's
        word "beyond" (STOP_BUF_ATR) dropped."""
        d, e, a = int(direction), float(retest_extreme), float(atr_sig)
        rail = float(entry_px) - d * float(rail_atr) * a
        px = min(e, rail) if d == 1 else max(e, rail)
        return V5.Stop(stop_px=float(px), anchor=e, anchor_bar=int(touch_i),
                       pivot_stop_px=e, pivot_dist=abs(float(entry_px) - e),
                       rail_dist=float(rail_atr) * a,
                       r_dist=abs(float(entry_px) - px),
                       rail_binding=bool(float(rail_atr) * a
                                         > abs(float(entry_px) - e)),
                       n_eligible=1)

    return prove(
        "F-BRK-LANE-SYN",
        "both lanes end to end on synthetic tapes: anchor -> permission -> "
        "stop -> ride -> accounting",
        "a permission refusal does not stop the lane or is not counted, the "
        "stop is not spring_stop's geometry on the retest extreme railed "
        "1.0 ATR, the entry is not flip.i + FLIP_HOLD_BARS, or a campaign "
        "rides without paying the estate's fee and its interval-sum funding",
        [("the 4h tide permission forced open",
          mutated(B, "s1_permission", _always, _lane_syn_checks)),
         ("the card's 'beyond' (STOP_BUF_ATR) dropped from the stop",
          mutated(B, "brk_stop", _no_beyond, _lane_syn_checks))],
        _lane_syn_checks)


# ══════════════ F-BRK-SPINE · the runners, past the gate, all the way to a book
# WHY THIS FIXTURE EXISTS (review, 2026-09-21).  Fourteen green fixtures and
# twenty-four RED break legs said NOTHING about the post-gate half of either
# runner, because no leg had ever executed one past its gate: F-BRK-GATE calls
# them with NOTHING filed (they must HALT at their first statement) and
# F-BRK-LANE-SYN rebuilds the lane by hand out of its parts.  So `tuned_pins`,
# `r1_band(tuned['band'])`, `corridor_era`, `stamp_toll` and `external_book` —
# the whole spine — were never executed, and three real defects lived there:
# a band spelling that made `tuned_pins` refuse the census's OWN filed result,
# a toll class no grid has ever held, and a single-path tuning reader that
# handed the 5m cell to the 1d lens.  Every one of them would have gone RED
# here on the day it appeared.
#
# WHAT IS REAL AND WHAT IS NOT, EXACTLY:
#   · THE REGISTRY IS A THROWAWAY in a temp root.  The registry of record
#     files nothing, and F-BRK-GATE re-attests that on every run.
#   · THE PANEL IS A REAL NAME (BTCUSDT), because the corridor, the era window
#     and the filed census grid are all keyed on an asset's NAME — so the
#     window the runner rides, the era it is held to and the toll it reads are
#     the REAL ones, which is the whole point.
#   · THE BARS ARE NOT REAL.  A synthetic tape is planted in this module's
#     frame memo under that name and the memo is restored exactly afterwards.
#     The corridor call reads the asset's real BAR STAMPS and its funding
#     coverage — that is what a corridor IS — and no real OHLC value ever
#     reaches a campaign: every price, high, low and ATR here is invented.
#   · NO P-BRK NUMBER IS COMPUTED (LAW 4).  What is proved is that the spine
#     RUNS and that every pin it picks up on the way is the pin of record.
SPINE_SYM = "BTCUSDT"
SPINE_PANEL = (SPINE_SYM,)
SPINE_TEXT = (GATE_TEXT + "  This arm exists to drive the BRK runners past "
              "their own gate on a SYNTHETIC tape; it is filed in a temp "
              "registry and scores nothing." + _CL)
_MISSING = object()


@contextlib.contextmanager
def planted_frames(frames: dict):
    """Plant synthetic LensFrames in `tierc10_brk`'s frame memo under real
    names, and put the memo back EXACTLY as it was — the sabotage-on-copies
    law applied to a cache: what is planted is removed, what was there is
    returned, and nothing is written to disk."""
    saved = {k: B._FRAMES.get(k, _MISSING) for k in frames}
    B._FRAMES.update(frames)
    try:
        yield
    finally:
        for k, v in saved.items():
            if v is _MISSING:
                B._FRAMES.pop(k, None)
            else:
                B._FRAMES[k] = v


def _spine_s1_tapes(t0_5m: int, tuned: dict) -> tuple:
    """The 5m tape the scalper rides and the 4h tape that permits it.

    The retest is planted against THE MODULE'S OWN BAND — `r1_band(tuned
    ['band'])` evaluated on these very closes — and not against a constant
    array, so the tuned band, its warm-up and its geometry are all exercised.
    Price runs away from the ribbon, ONE bar wicks back into it, and the next
    `hold_bars` closes stay clear of the far edge: a HOLD, by the law.
    """
    n, touch = 700, 500
    c = np.linspace(100.0, 400.0, n)
    lo, hi = B.r1_band(tuned["band"])(c)
    h, l = c + 0.5, (c - 0.5).copy()
    l[touch] = float(hi[touch]) - 1.0         # the wick that MEETS the band
    fh, fr = funding_series(t0_5m + 2 * 3_600_000, 8, every_h=8, rate=0.0002)
    lf = syn_frame(SPINE_SYM, "5m", c, h, l, t0=t0_5m, fund=(fh, fr))
    c4 = np.linspace(50.0, 500.0, 500)
    f4 = syn_frame(SPINE_SYM, "4h", c4, t0=int(t0_5m) - 420 * MS_4H)
    dies = [(touch - 50, 11, "top")]          # the DIE this retest answers
    return lf, f4, dies, touch


def _spine_i1_tapes(t0_1d: int) -> tuple:
    """The 1d tape the investor rides — the operator's OWN lifecycle shape
    (R4) — plus the weekly tape its posture comes from.  The flip is placed so
    the entry lands on a bar whose DAILY DIRECTION the lifecycle itself says
    is +1; the fixture does not hand the permission an array of its own."""
    c, h, l = lifecycle_tape()
    fh, fr = funding_series(t0_1d, 400, every_h=8, rate=0.00005)
    lf = syn_frame(SPINE_SYM, "1d", c, h, l, t0=t0_1d, fund=(fh, fr))
    life = B.ribbon_lifecycle(lf.c, lf.atr)
    up = [i for i in range(60, lf.n) if int(life["direction"][i]) == 1]
    entry = int(up[0]) + 2                    # comfortably inside the episode
    flip_i = entry - B.FLIP_HOLD_BARS
    dies = [(flip_i - 4, 13, "top")]
    flips = [{"i": flip_i, "polarity": "support", "rid": 13}]
    cw = np.linspace(40.0, 400.0, 120)
    w1 = syn_frame(SPINE_SYM, "1w", cw,
                   t0=int(t0_1d) - 60 * 7 * MS_1D)
    return lf, w1, dies, flips, entry


def _spine_checks() -> tuple:
    lines, ok = [], True
    with tempfile.TemporaryDirectory(prefix="f-brk-spine-") as td:
        root = Path(td) / "registrations"
        root.mkdir(parents=True)
        # ── S1: the scalper, gate -> tuned pins -> band -> tide -> book ─────
        s_lo, s_hi, _ = TP.corridor_era(SPINE_PANEL, "holdout")
        tuned = B.tuned_pins("5m")
        lf, f4, dies, touch = _spine_s1_tapes(int(s_lo) + 30 * MS_1D, tuned)
        TP.register("P-BRK-X-SPINE-S1", SPINE_TEXT, 30, root=root, arms=[
            TP.arm_spec("spine s1", SPINE_PANEL, "vs_zero",
                        lanes=(B.LANE_S1,), loao_line="lineage",
                        era="holdout")])
        with planted_frames({(SPINE_SYM, "5m", True): lf,
                             (SPINE_SYM, "4h", False): f4}):
            out = B.run_lane_s1(
                SPINE_PANEL, "P-BRK-X-SPINE-S1", SPINE_TEXT, "spine s1",
                {SPINE_SYM: {"dies": dies, "flips": []}},
                head_of_record=TP.UNPINNED, reg_root=root)
        tr = out["trades"]
        g = (len(tr) == 1 and out["era"] == "holdout"
             and out["gate"]["runner"] == "external"
             and out["book"].spec["era"] == "holdout"
             and out["book"].spec["registration"] == "P-BRK-X-SPINE-S1")
        ok &= g
        lines.append(mark(g, f"run_lane_s1 rode the GATE -> TUNED PINS -> "
                             f"BAND -> TIDE -> RIDE -> TOLL -> BOOK: "
                             f"{len(tr)} campaign, era {out['era']!r}, book "
                             f"spec registration "
                             f"{out['book'].spec['registration']!r} / era "
                             f"{out['book'].spec['era']!r}"))
        g = (out["tuned"]["source"] == str(B.TUNING_RESULT_FOR["5m"])
             and out["tuned"]["band"] == tuned["band"]
             and out["tuned"]["band_as_filed"] == tuned["band_as_filed"]
             and out["tuned"]["margin_atr"] == tuned["margin_atr"]
             and out["tuned"]["hold_bars"] == tuned["hold_bars"])
        ok &= g
        lines.append(mark(g, f"the pins it picked up are the FILE OF RECORD's "
                             f"— band {out['tuned']['band_as_filed']!r} as "
                             f"filed -> {out['tuned']['band']!r}, margin "
                             f"{out['tuned']['margin_atr']}, hold "
                             f"{out['tuned']['hold_bars']}, from "
                             f"{Path(out['tuned']['source']).name} — read "
                             f"INSIDE the runner, not handed in"))
        t = tr[0] if tr else None
        want_toll = B.grid_toll_atr(SPINE_SYM, "5m", out["toll"]["cls"])
        g = (t is not None
             and out["toll"]["cls"] == B.toll_class(B.ANCHOR_BAND,
                                                    tuned["band"])
             and out["toll"]["per_asset"][SPINE_SYM] == want_toll
             and t.toll_atr_grid == want_toll
             and np.isfinite(t.toll_pct_of_1r) and t.toll_pct_of_1r > 0)
        ok &= g
        lines.append(mark(g, f"and the contract's 'NET OF MEASURED 5m TOLL' "
                             f"is REACHABLE: cls {out['toll']['cls']!r} -> "
                             f"toll_atr {want_toll} -> stamped on the campaign "
                             f"as {t.toll_pct_of_1r if t else float('nan'):.4f} "
                             f"% of 1R (R = {t.r_dist if t else float('nan'):.4f} "
                             f"= {(t.r_dist / t.atr_at_entry) if t else float('nan'):.4f} ATR)"))
        g = (t is not None and t.entry_i == touch + tuned["hold_bars"]
             and t.touch_i == touch and t.die_i == dies[0][0]
             and t.lane == B.LANE_S1 and t.entry_ms > TP.ERA_CUT_MS
             and s_lo <= t.entry_ms <= s_hi and t.fee_r > 0)
        ok &= g
        lines.append(mark(g, f"the campaign is the planted one and nothing "
                             f"else: entry bar {t.entry_i if t else '-'} = "
                             f"touch {touch} + hold {tuned['hold_bars']}, die "
                             f"{t.die_i if t else '-'}, lane "
                             f"{t.lane if t else '-'}, entry "
                             f"{TP.iso(int(t.entry_ms)) if t else '-'} inside "
                             f"the HOLDOUT window "
                             f"{TP.iso(int(s_lo))}..{TP.iso(int(s_hi) + 1)}"))
        # ── the era door is the runner's, not the caller's: a window that
        # ── reaches into the tuning era is NARROWED, never widened.
        with planted_frames({(SPINE_SYM, "5m", True): lf,
                             (SPINE_SYM, "4h", False): f4}):
            wide = B.run_lane_s1(
                SPINE_PANEL, "P-BRK-X-SPINE-S1", SPINE_TEXT, "spine s1",
                {SPINE_SYM: {"dies": dies, "flips": []}},
                head_of_record=TP.UNPINNED, reg_root=root,
                lo_ms=0, hi_ms=2 ** 62)
        g = wide["window"] == (int(s_lo), int(s_hi))
        ok &= g
        lines.append(mark(g, f"a caller offering the whole of time gets the "
                             f"ARM'S window back: {[TP.iso(x) for x in wide['window']]} "
                             f"— corridor_era narrows, a caller cannot widen"))
        # ── I1: the investor, full corridor, memory anchor ──────────────────
        i_lo, i_hi, _ = TP.corridor_era(SPINE_PANEL, "full")
        lfd, w1, d_dies, d_flips, want_entry = _spine_i1_tapes(
            int(i_lo) + 500 * MS_1D)
        TP.register("P-BRK-X-SPINE-I1", SPINE_TEXT, 30, root=root, arms=[
            TP.arm_spec("spine i1", SPINE_PANEL, "vs_zero",
                        lanes=(B.LANE_I1,), loao_line="lineage", era="full")])
        with planted_frames({(SPINE_SYM, "1d", True): lfd,
                             (SPINE_SYM, "1w", False): w1}):
            out1 = B.run_lane_i1(
                SPINE_PANEL, "P-BRK-X-SPINE-I1", SPINE_TEXT, "spine i1",
                {SPINE_SYM: {"dies": d_dies, "flips": d_flips}},
                head_of_record=TP.UNPINNED, reg_root=root)
        t1 = out1["trades"][0] if out1["trades"] else None
        g = (len(out1["trades"]) == 1 and t1 is not None
             and t1.entry_i == want_entry
             and t1.touch_i == d_flips[0]["i"]
             and t1.lane == B.LANE_I1 and t1.direction == 1
             and out1["era"] == "full"
             and out1["book"].spec["arm"] == "spine i1"
             and "toll" not in out1)
        ok &= g
        lines.append(mark(g, f"run_lane_i1 rode the GATE -> MEMORY FLIP -> "
                             f"R4 PERMISSION -> RIDE -> BOOK: "
                             f"{len(out1['trades'])} campaign, entry bar "
                             f"{t1.entry_i if t1 else '-'} = flip "
                             f"{d_flips[0]['i']} + FLIP_HOLD_BARS "
                             f"{B.FLIP_HOLD_BARS}, era {out1['era']!r}, and "
                             f"NO toll block (the 5m toll is S1's print, not "
                             f"I1's)"))
        # ── THE OTHER ANCHOR, the contract's Tier-E print, through the SAME
        # ── runner: I1 on the tuned 1d BAND rather than the memory line.
        with planted_frames({(SPINE_SYM, "1d", True): lfd,
                             (SPINE_SYM, "1w", False): w1}):
            out1b = B.run_lane_i1(
                SPINE_PANEL, "P-BRK-X-SPINE-I1", SPINE_TEXT, "spine i1",
                {SPINE_SYM: {"dies": d_dies, "flips": d_flips}},
                head_of_record=TP.UNPINNED, reg_root=root,
                anchor=B.ANCHOR_BAND)
        t1d = B.tuned_pins("1d")
        g = (out1b["anchor"] == B.ANCHOR_BAND
             and t1d["lens"] == "1d"
             and t1d["source"] == str(B.TUNING_RESULT_FOR["1d"])
             and t1d["band"] != tuned["band"])
        ok &= g
        lines.append(mark(g, f"the Tier-E OTHER anchor runs through the same "
                             f"runner and reads the 1d TUNING FILE, not the "
                             f"5m one: band {t1d['band']!r} margin "
                             f"{t1d['margin_atr']} hold {t1d['hold_bars']} "
                             f"from {Path(t1d['source']).name} (the 5m cell "
                             f"says {tuned['band']!r} / {tuned['margin_atr']} "
                             f"/ {tuned['hold_bars']} — a single-path reader "
                             f"would have ridden THOSE), "
                             f"{len(out1b['trades'])} campaigns"))
        g = B._FRAMES.get((SPINE_SYM, "5m", True)) is not lf
        ok &= g
        lines.append(mark(g, f"and the frame memo is back as it was: the "
                             f"planted tapes are gone "
                             f"({sorted(k for k in B._FRAMES if k[0] == SPINE_SYM)})"))
    return ok, lines


def f_brk_spine() -> bool:
    def _identity_band(name):
        """A named wrong: the spelling law removed — the census's own band
        name is passed through untranslated, which is what this module did
        before review and what made the toll unreachable."""
        return str(name)

    true_tuned = B.tuned_pins                    # captured, not stashed

    def _five_m_only(lens="5m", path=None):
        """A named wrong: ONE tuning file for every lens, its `lens` field
        overwritten with the one asked for."""
        return dict(true_tuned("5m", path), lens=lens)

    return prove(
        "F-BRK-SPINE",
        "both runners execute PAST the gate to a Book — tuned pins, band, "
        "permission, era window, toll and journal — on synthetic tapes under "
        "a real panel name",
        "a runner cannot reach its book, picks up a pin that is not the one "
        "of record, builds a toll class the filed grid does not hold, reads "
        "one lens's tuning cell for another, lets a caller widen the arm's "
        "era window, or leaves a planted tape behind in the frame memo",
        [("the spelling law removed (census band names passed through raw)",
          mutated(B, "census_band", _identity_band, _spine_checks)),
         ("ONE tuning file for every lens",
          mutated(B, "tuned_pins", _five_m_only, _spine_checks))],
        _spine_checks)


# ═══════════════════════════════════════════════════════════ F-DET · twin runs
def _det_pair(a: Path, b: Path) -> tuple:
    for d in (a, b):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            B.main(["--out", str(d)])
    fa = sorted(p.name for p in a.iterdir())
    fb = sorted(p.name for p in b.iterdir())
    diff = [n for n in fa if n in fb
            and (a / n).read_bytes() != (b / n).read_bytes()]
    return fa, fb, diff


def f_det() -> bool:
    def real():
        with tempfile.TemporaryDirectory(prefix="f-brk-det-") as td:
            a, b = Path(td) / "A", Path(td) / "B"
            fa, fb, diff = _det_pair(a, b)
            g = fa == fb and not diff and bool(fa)
            lines = [mark(g, f"two runs of tierc10_brk.main() into separate "
                             f"roots: files {fa}, byte-differences "
                             f"{diff or 'none'}")]
            # ── THE HALF THAT IS DETERMINISTIC ACROSS DISKS, NOT MERELY
            # ── ACROSS AN INSTANT.  Two runs in one instant read the same
            # ── disk, so they structurally CANNOT see a card that depends on
            # ── what happens to be filed — which is how the run2 twin filed
            # ── in the last round came to contradict the card of record
            # ── (review).  `out_root` re-points ONLY the disk reads.
            empty = Path(td) / "EMPTY"
            (empty / "data").mkdir(parents=True)
            J = dict(sort_keys=True, default=str)
            pure_here = json.dumps(B.mechanics_card(disk=False), **J)
            # THE AS-OF IS A PIN, NOT A DISK READING (review, 2026-09-22).
            # `out_root` re-points the OUTPUT-directory reads and must NOT
            # re-point `as_of_of_record()`, which reads Stage D's write-once
            # AS_OF_PIN.json.  So the card computed against a root where
            # NOTHING is filed still carries the REAL as-of, and that is
            # correct behaviour, not a leak: the two `pure_*` strings below
            # are identical BECAUSE the as-of is the same pin on both.
            pure_there = json.dumps(
                B.mechanics_card(disk=False, out_root=empty), **J)
            env_here = B.mechanics_card()["environment"]
            env_there = B.mechanics_card(out_root=empty)["environment"]
            g2 = (pure_here == pure_there
                  and json.loads(pure_here)["environment"] is None
                  and env_here != env_there
                  and env_there["tuning_result_present"] ==
                  {k: False for k in B.TUNED_LENSES}
                  and env_there["fee_matches_stage_d_schedule"] is None)
            g = g and g2
            lines.append(mark(g2, f"the card MINUS its environment block is "
                                  f"the same bytes on a disk where NOTHING is "
                                  f"filed ({len(pure_here)} bytes, identical) "
                                  f"— while the environment block itself "
                                  f"correctly changes: filed here "
                                  f"{env_here['tuning_result_present']} / fee "
                                  f"agrees {env_here['fee_matches_stage_d_schedule']}, "
                                  f"on the empty root "
                                  f"{env_there['tuning_result_present']} / "
                                  f"{env_there['fee_matches_stage_d_schedule']}"))
            # ── THE AS-OF WARRANTY, ON THE CARD OF RECORD ───────────────────
            # THE LEG THAT WAS MISSING.  BRK_MECHANICS.json was filed with NO
            # as_of_last_closed_4h at any depth, at any key, while the report
            # attested it carried one.  A card true of no stated instant can
            # be re-read after the corridor moves and silently believed.
            card = B.mechanics_card()
            filed = json.loads((a / "BRK_MECHANICS.json").read_text())
            man = json.loads((a / B.MANIFEST_NAME).read_text())

            def _scan(o, p=""):
                """EVERY as-of stamp in the tree, at any depth."""
                hit = {}
                if isinstance(o, dict):
                    for k, v in o.items():
                        if k == "as_of_last_closed_4h":
                            hit[p + "/" + k] = v
                        hit.update(_scan(v, p + "/" + str(k)))
                elif isinstance(o, list):
                    for i, v in enumerate(o):
                        hit.update(_scan(v, p + f"[{i}]"))
                return hit
            stamps = _scan(filed)
            g3 = (card["pins"]["as_of_last_closed_4h"] == ASOF
                  and card["pins"]["as_of_source"].startswith("Stage D")
                  and filed["pins"]["as_of_last_closed_4h"] == ASOF
                  and bool(stamps)
                  and all(v == ASOF for v in stamps.values())
                  and man["as_of_last_closed_4h"] == ASOF
                  and json.loads(pure_there)["pins"]
                  ["as_of_last_closed_4h"] == ASOF)
            g = g and g3
            lines.append(mark(g3, f"the FILED card of record carries the "
                                  f"AS-OF WARRANTY in `pins` (a pin, not the "
                                  f"`environment` reading): "
                                  f"pins.as_of_last_closed_4h "
                                  f"{filed['pins'].get('as_of_last_closed_4h')!r} "
                                  f"from {filed['pins'].get('as_of_source')!r}; "
                                  f"{len(stamps)} as-of stamp(s) at any depth "
                                  f"in the card, all == {ASOF} "
                                  f"({sorted(stamps)}); the manifest agrees "
                                  f"({man['as_of_last_closed_4h']}); and the "
                                  f"EMPTY-root card still carries it, because "
                                  f"`out_root` re-points disk READINGS and "
                                  f"the as-of is a WRITE-ONCE PIN"))
            return g, lines

    def corrupt():
        with tempfile.TemporaryDirectory(prefix="f-brk-det-") as td:
            a, b = Path(td) / "A", Path(td) / "B"
            _det_pair(a, b)
            p = b / "BRK_MECHANICS.json"
            p.write_text(p.read_text().replace("\"seed\":", "\"seed \":"))
            diff = [n.name for n in a.iterdir()
                    if (b / n.name).read_bytes() != n.read_bytes()]
            return not diff, f"the comparator on the corrupted COPY: {diff}"

    def pure_is_not_pure():
        """A break leg for the PURITY half: if the disk reads were inside
        `pins` (where they used to be), the card computed against an empty
        root would differ from the card of record — and that is precisely
        what `disk=False` must NOT do."""
        with tempfile.TemporaryDirectory(prefix="f-brk-det-") as td:
            empty = Path(td) / "EMPTY"
            (empty / "data").mkdir(parents=True)
            J = dict(sort_keys=True, default=str)
            a = json.dumps(B.mechanics_card(disk=True), **J)
            b = json.dumps(B.mechanics_card(disk=True, out_root=empty), **J)
            verdict = ("identical — the environment block reads nothing"
                       if a == b else "differs, as it must")
            return a == b, (f"the WHOLE card (environment included) on two "
                            f"different disks: {verdict}")

    _real_card = B.mechanics_card

    def _card_without_asof(disk: bool = True, out_root=None) -> dict:
        """A named wrong: THE SHIPPED DEFECT — the card of record filed with
        no as-of stamp anywhere in it, true of no stated instant."""
        c = dict(_real_card(disk=disk, out_root=out_root))
        c["pins"] = {k: v for k, v in c["pins"].items()
                     if k != "as_of_last_closed_4h"}
        return c

    return prove(
        "F-DET",
        "the mechanics card is deterministic — no clock, no bar, no result — "
        "its `pins` half is the same bytes on ANY disk, and it CARRIES THE "
        "AS-OF WARRANTY it is filed under",
        "two runs of main() into separate roots differ in any byte, write "
        "different file sets, the card minus its environment block changes "
        "when what is filed on disk changes, the filed card carries no "
        "as_of_last_closed_4h at any depth, it carries one that is not "
        "2026-09-21T16:00:00Z, or the as-of stops being a pin and starts "
        "following `out_root`",
        [("one byte changed in a COPY of the second run's card", corrupt),
         ("the disk reads treated as pins (whole card, two disks)",
          pure_is_not_pure),
         ("the AS-OF STAMP stripped from the card of record (the shipped "
          "defect)", mutated(B, "mechanics_card", _card_without_asof, real))],
        real)


# ══════════════════ F-BRK-LANE-ERA · the DECLARED era pin vs the FILED arm
# WHY THIS FIXTURE EXISTS (R0, 2026-09-22).  `LANE_ERA = {brk-s1: "holdout",
# brk-i1: "full"}` was a DECLARED PIN THAT NOTHING CHECKED: both runners took
# `era = g["era"]` from the filed arm and never compared it to the pin.  The
# holdout collar is the whole reason P-BRK-S1's tuned pins are honest — R1's
# protocol is "tune on era <= 2024-06-30, score on the holdout" — so an arm
# filed at era='full' would have scored the scalper IN SAMPLE on the very grid
# that chose its band, its margin and its hold, and `external_book`'s door
# would NOT have caught it: that door holds the journal to the ARM's own era,
# which is exactly the thing that was wrong.
ERA_SYM = "BTCUSDT"
ERA_PANEL = (ERA_SYM,)
ERA_TEXT = (GATE_TEXT + "  This arm exists to offer the BRK runners a WRONG "
            "era and prove they refuse it before reading a bar; it is filed "
            "in a temp registry and scores nothing." + _CL)


@contextlib.contextmanager
def watched(pairs):
    """Replace each (obj, attr) with a probe that COUNTS its calls and then
    calls the real thing, and put every one back in a finally.  It is how
    "not one bar was read" becomes a MEASURED ZERO instead of a hope: the
    guard must fire with frame_l and corridor_era both at 0 calls."""
    saved = [(o, a, getattr(o, a)) for o, a in pairs]
    hits = {a: 0 for _, a in pairs}

    def make(a, real):
        def probe(*args, **kw):
            hits[a] += 1
            return real(*args, **kw)
        return probe

    for o, a, real in saved:
        setattr(o, a, make(a, real))
    try:
        yield hits
    finally:
        for o, a, real in saved:
            setattr(o, a, real)


def _call_order(fn_name: str) -> dict:
    """The FIRST line number at which each named call appears inside a named
    function of the module under test — read out of the AST, so "the pin is
    tested before the corridor is read" is a claim about the SOURCE and not
    about one lucky run."""
    import ast                                               # noqa: PLC0415
    tree = ast.parse((ROOT / "scripts" / "tierc10_brk.py").read_text(
        encoding="utf-8"))
    want = ("require_lane_era", "corridor_era", "frame_l", "tuned_pins",
            "gate")
    for fn in ast.walk(tree):
        if not isinstance(fn, ast.FunctionDef) or fn.name != fn_name:
            continue
        got: dict = {}
        for sub in ast.walk(fn):
            if not isinstance(sub, ast.Call):
                continue
            f = sub.func
            nm = (f.attr if isinstance(f, ast.Attribute)
                  else (f.id if isinstance(f, ast.Name) else None))
            if nm in want and nm not in got:
                got[nm] = int(sub.lineno)
        return got
    raise SystemExit(f"HALT: no function {fn_name!r} in tierc10_brk.py")


def _era_pin_checks() -> tuple:
    lines, ok = [], True
    # ── 1 · the DECLARATION is total and legal ──────────────────────────────
    g = (set(B.LANE_ERA) == set(B.LANE_LENS) == set(B.LANE_ORDER)
         and B.LANE_ERA == {B.LANE_S1: "holdout", B.LANE_I1: "full"}
         and not (set(B.LANE_ERA.values()) - set(TP.ERAS))
         and set(B.LANE_ERA_REASON) == set(B.LANE_ERA))
    ok &= g
    lines.append(mark(g, f"LANE_ERA declares EVERY lane and only legal eras: "
                         f"{dict(sorted(B.LANE_ERA.items()))} out of "
                         f"{list(TP.ERAS)}, with a NAMED reason per lane"))
    # ── 2 · the pin is tested BEFORE the corridor and the bars, IN SOURCE ───
    for fn_name in ("run_lane_s1", "run_lane_i1"):
        o = _call_order(fn_name)
        g = ("require_lane_era" in o and "gate" in o
             and o["gate"] < o["require_lane_era"]
             and o["require_lane_era"] < o.get("corridor_era", 10 ** 9)
             and o["require_lane_era"] < o.get("frame_l", 10 ** 9)
             and o["require_lane_era"] < o.get("tuned_pins", 10 ** 9))
        ok &= g
        lines.append(mark(g, f"{fn_name}: gate at line {o.get('gate')} -> "
                             f"require_lane_era at "
                             f"{o.get('require_lane_era')} -> tuned_pins "
                             f"{o.get('tuned_pins')} / corridor_era "
                             f"{o.get('corridor_era')} / frame_l "
                             f"{o.get('frame_l')} — the pin is tested BEFORE "
                             f"anything reads a bar or a bar stamp"))
    # ── 3 · the live HALT, with the bar readers COUNTED at zero ─────────────
    with tempfile.TemporaryDirectory(prefix="f-brk-era-pin-") as td:
        root = Path(td) / "registrations"
        root.mkdir(parents=True)
        cases = (
            ("P-BRK-X-ERA-S1-FULL", B.LANE_S1, "full", B.run_lane_s1,
             "the SCALPER filed on the FULL corridor — in sample on its own "
             "tuning grid"),
            ("P-BRK-X-ERA-S1-TUNE", B.LANE_S1, "tuning", B.run_lane_s1,
             "the SCALPER filed on the TUNING era — wholly in sample"),
            ("P-BRK-X-ERA-I1-HOLD", B.LANE_I1, "holdout", B.run_lane_i1,
             "the INVESTOR collared to the holdout — a window its text does "
             "not name"),
        )
        for reg_id, lane, era, runner, why in cases:
            TP.register(reg_id, ERA_TEXT, 30, root=root, arms=[
                TP.arm_spec("wrong era", ERA_PANEL, "vs_zero", lanes=(lane,),
                            loao_line="lineage", era=era)])
            with watched([(B, "frame_l"), (TP, "corridor_era")]) as hits:
                did, msg = refused(lambda _r=runner, _i=reg_id: _r(
                    ERA_PANEL, _i, ERA_TEXT, "wrong era", {},
                    head_of_record=TP.UNPINNED, reg_root=root))
            g = (did and "LANE_ERA" in msg and repr(era) in msg
                 and repr(B.LANE_ERA[lane]) in msg
                 and hits["frame_l"] == 0 and hits["corridor_era"] == 0)
            ok &= g
            lines.append(mark(g, f"{lane} filed at era={era!r} ({why}) -> "
                                 f"{'HALT' if did else 'RODE IT'}; frame_l "
                                 f"called {hits['frame_l']}x, corridor_era "
                                 f"{hits['corridor_era']}x (want 0 and 0). "
                                 f"{msg[:150]}"))
        # ── 4 · and the DECLARED era is let through, at the same door ───────
        for lane in B.LANE_ORDER:
            good = {"runner": "external", "registration": "P-BRK-X-ERA-OK",
                    "arm": "right era", "panel": list(ERA_PANEL),
                    "lanes": [lane], "era": B.LANE_ERA[lane],
                    "registration_sha256": "0" * 64}
            got = B.require_lane_era(lane, good)
            g = got == B.LANE_ERA[lane]
            ok &= g
            lines.append(mark(g, f"{lane} filed at era="
                                 f"{B.LANE_ERA[lane]!r} passes the pin and "
                                 f"the runner rides on (require_lane_era "
                                 f"-> {got!r}); F-BRK-SPINE then drives both "
                                 f"runners all the way to a Book at exactly "
                                 f"these eras"))
    # ── 5 · the pin refuses what is not a lane and what is not a gate ───────
    did, why = refused(lambda: B.require_lane_era("card", {"era": "full"}))
    g = did and "LANE_ERA" in why
    ok &= g
    lines.append(mark(g, f"a lane with NO declared era -> "
                         f"{'HALT' if did else 'ran'}: {why[:110]}"))
    did, why = refused(lambda: B.require_lane_era(B.LANE_S1, "holdout"))
    g = did and "FILED ARM" in why
    ok &= g
    lines.append(mark(g, f"an era handed in as a STRING instead of the "
                         f"gate -> {'HALT' if did else 'ran'}: {why[:110]} — "
                         f"the era must come from the filing, never from the "
                         f"caller"))
    return ok, lines


def f_brk_lane_era() -> bool:
    def _noop(lane, gate_):
        """A named wrong: the pin DECLARED and not enforced — the module as
        R0 found it, where `era = g['era']` was taken on trust."""
        return str(gate_["era"] if isinstance(gate_, dict) else gate_)

    def _pin_is_the_arm(lane, gate_):
        """A named wrong that is subtler and worse: the pin looked up with a
        default of whatever the arm happens to say, so it can never disagree."""
        e = gate_["era"] if isinstance(gate_, dict) else gate_
        return str(B.LANE_ERA.get(lane, e))

    return prove(
        "F-BRK-LANE-ERA",
        "LANE_ERA is ENFORCED against the filed arm inside both runners, and "
        "the HALT fires before one bar or one bar-stamp is read",
        "a P-BRK-S1 arm filed at era='full' (or 'tuning') rides, a P-BRK-I1 "
        "arm collared to one era rides, the refusal comes after the corridor "
        "or a frame has been read, the declared era is itself refused, or "
        "require_lane_era is called anywhere but before corridor_era / "
        "tuned_pins / frame_l in BOTH runners",
        [("the era pin declared but not enforced (the defect R0 found)",
          mutated(B, "require_lane_era", _noop, _era_pin_checks)),
         ("LANE_ERA rewritten so both lanes ride 'full'",
          mutated(B, "LANE_ERA", {B.LANE_S1: "full", B.LANE_I1: "full"},
                  _era_pin_checks)),
         ("the pin looked up with the ARM's own era as its default",
          mutated(B, "require_lane_era", _pin_is_the_arm, _era_pin_checks))],
        _era_pin_checks)


# ═══════════════ F-BRK-ROW · the row, the OTHER anchor, and the [Q-R3] slot
# WHY THIS FIXTURE EXISTS (R0, 2026-09-22).  `research_outputs/tierc10/brk/`
# held NO parquet at all, so the contract's line 112 — "Each BRK form also
# prints the OTHER anchor as Tier-E, and carries its lens's height-vs-toll
# verdict ON ITS ROW" — had no row to ride on.  The MECHANISM existed
# (LANE_TIER_E_ANCHOR, `anchor=` on both runners, `stamp_toll`); the ASSEMBLY
# did not.
#
# WHAT IS REAL AND WHAT IS NOT.  Exactly F-BRK-SPINE's settlement: a THROWAWAY
# registry in a temp root, a REAL panel name (so the corridor, the era and the
# filed census grid are the real ones), and SYNTHETIC BARS — no real OHLC
# value reaches any campaign here.  The [Q-R3] table this fixture reads is
# likewise a TEMP-ROOT FIXTURE FILE carrying the obviously-fake verdict string
# `SYN-FIXTURE-VERDICT`: it proves the READ PATH and invents no measurement.
# Nothing is written to the census directory and no BRK row is filed anywhere.
ROW_VERDICT_PASS = False
ROW_VERDICT_LAW = "SYN-FIXTURE-LAW — no measurement produced this"
ROW_VERDICT_REASON = "SYN-FIXTURE-REASON"
# THE ASSET THE SPINE'S BOOK ACTUALLY DERIVES [review round 2, finding 1].
# This constant used to read "POOLED:CLASSIC5" while every row in this fixture
# is built on SPINE_PANEL = ('BTCUSDT',) — which is precisely the substitution
# the finding is about, written into the fixture's own expectations.  It is
# now the label the Book's panel DERIVES, so the synthetic tables are keyed on
# the row the reader will actually ask for.
ROW_ASSET = "BTCUSDT"
ASOF = "2026-09-21T16:00:00Z"
# the SHARED figures, written into BOTH synthetic tables so the cross-check
# has something true to agree on
SYN_FIG = {"n_ranges": 1234, "height_atr_median": 3.25,
           "toll_atr_median": 0.41061594}
# the LAW half of the cross-check, and the census's sample-floor columns —
# both REQUIRED of the verdict table since the round-2 repair
SYN_SHA = {"gate_law_sha": "SYN-FIXTURE-GATE-LAW-SHA-not-a-real-sha"}
SYN_FLOOR = {"provisional": False, "provisional_reason": "",
             "edge_n_ranges": 1200, "min_n_ranges_pinned": 30,
             "edge_min_n_ranges_pinned": 30}
# WHAT THE CENSUS FILED FOR THE SPINE'S OWN BOOK, at both lenses.  The 1d row
# is PROVISIONAL, which is why a BRK row on this book cannot take it quietly.
REAL_BTC_5M = {"n_ranges": 2832, "height_atr_median": 6.33176614,
               "toll_atr_median": 0.5042885, "ratio_median": 13.0844195,
               "verdict_pass": False,
               "reason": "height gate PASS + edge-fade leg FAIL"}
REAL_BTC_1D_N = 11
REAL_BTC_1D_EDGE_N = 11
REAL_BTC_1D_FLOOR = 30
REAL_CLASSIC5_5M_N = 13025          # what the DEFAULT used to hand this book
REAL_CLASSIC5_1D_N = 53

# ── WHAT THE CENSUS TRACK ACTUALLY FILED, READ AND ASSERTED VERBATIM ────────
# The last round's interface was a GUESS (`census/height_vs_toll.parquet`,
# columns toll_atr / height_over_toll_median / verdict / n) that matched
# NOTHING on disk, and it survived 22 green checks because every [Q-R3] leg
# ran against a synthetic temp-root twin the fixture wrote itself in its own
# declared schema.  These are the REAL filed numbers, and the leg below reads
# them through the module's own reader.
REAL_HVT = {
    ("5m", "POOLED:CLASSIC5"): {
        "n_ranges": 13025, "height_atr_median": 6.48087293,
        "toll_atr_median": 0.29265442, "ratio_median": 23.25581395,
        "verdict_pass": False,
        "reason": "height gate PASS + edge-fade leg FAIL"},
    ("1d", "POOLED:CLASSIC5"): {
        "n_ranges": 53, "height_atr_median": 6.23716024,
        "toll_atr_median": 0.01718173, "ratio_median": 413.99176955,
        "verdict_pass": True,
        "reason": "height gate PASS + edge-fade leg PASS"},
}


def _hvt_table(path: Path, lens: str = "5m", asset: str = ROW_ASSET,
               drop: str | None = None, dupe: bool = False,
               asof: str = ASOF, drop_many: tuple = (), **fig) -> Path:
    """A SYNTHETIC [Q-R3] FIGURES table in the DECLARED schema, in a temp
    root — key (asset, lens, scale_kind, era), the census's own column
    names, the gate-law sha the cross-check compares, and the as-of stamp the
    reader requires."""
    import pandas as pd                                      # noqa: PLC0415
    row = {"asset": asset, "lens": lens,
           "scale_kind": B.HEIGHT_VS_TOLL_SCALE,
           "era": B.HEIGHT_VS_TOLL_ERA,
           "ratio_median": 7.9148,
           B.HEIGHT_VS_TOLL_ASOF_COL: asof, **SYN_FIG, **SYN_SHA, **fig}
    for c in ((drop,) if drop else ()) + tuple(drop_many):
        row.pop(c)
    pd.DataFrame([row, row] if dupe else [row]).to_parquet(path, index=False)
    return path


def _hvt_verdict(path: Path, lens: str = "5m", asset: str = ROW_ASSET,
                 drop: str | None = None, dupe: bool = False,
                 asof: str = ASOF, verdict_pass=ROW_VERDICT_PASS,
                 verdict_law: str = ROW_VERDICT_LAW,
                 reason: str = ROW_VERDICT_REASON,
                 drop_many: tuple = (), **fig) -> Path:
    """A SYNTHETIC [Q-R3] VERDICT table — key (asset, lens, scale_kind) with
    NO era column, exactly as the census files it, carrying the three verdict
    fields verbatim, the figures and the gate-law sha the cross-check
    compares, and the sample-floor columns the round-2 repair requires."""
    import pandas as pd                                      # noqa: PLC0415
    row = {"asset": asset, "lens": lens,
           "scale_kind": B.HEIGHT_VS_TOLL_SCALE,
           "verdict_pass": verdict_pass, "verdict_law": verdict_law,
           "reason": reason,
           B.HEIGHT_VS_TOLL_ASOF_COL: asof,
           **SYN_FIG, **SYN_SHA, **SYN_FLOOR, **fig}
    for c in ((drop,) if drop else ()) + tuple(drop_many):
        row.pop(c)
    pd.DataFrame([row, row] if dupe else [row]).to_parquet(path, index=False)
    return path


def _hvt_pair(d: Path, tag: str = "ok", fig: dict | None = None,
              ver: dict | None = None) -> tuple:
    """Both [Q-R3] tables, written side by side under a distinct tag."""
    f = _hvt_table(d / f"hvt_fig_{tag}.parquet", **(fig or {}))
    v = _hvt_verdict(d / f"hvt_ver_{tag}.parquet", **(ver or {}))
    return f, v


def _shared_cols(fig_path: Path, ver_path: Path) -> list:
    """THE FIELDS A CROSS-CHECK COULD ACTUALLY COMPARE, computed by the
    FIXTURE from the two files on disk — so `cross_checked` is judged against
    what is there, never against the module's own constant.  The constant is
    what the shipped defect attested from while comparing nothing."""
    import pandas as pd                                      # noqa: PLC0415
    fc = set(pd.read_parquet(fig_path).columns)
    vc = set(pd.read_parquet(ver_path).columns)
    return [f for f in (list(B.HEIGHT_VS_TOLL_AGREE)
                        + list(B.HEIGHT_VS_TOLL_AGREE_STR))
            if f in fc and f in vc]


def _real_hvt_copy(d: Path, drop_many: tuple = (), flip: bool = False,
                   lens: str = "5m", asset: str = "POOLED:CLASSIC5") -> tuple:
    """THE REVIEWER'S OWN REPRODUCTION, AS A LEG.  The two REAL filed census
    tables are COPIED into a temp dir (the filed ones are never touched), the
    named columns are dropped from the VERDICT copy, and the asked row's
    verdict is flipped to True with a reason that says so out loud.  Before
    the round-2 repair this pair read clean: verdict_pass True, reason
    'INVENTED', cross_checked ['n_ranges', 'height_atr_median',
    'toll_atr_median'] — an attestation for a check that never ran."""
    import pandas as pd                                      # noqa: PLC0415
    f = pd.read_parquet(B.HEIGHT_VS_TOLL_PATH)
    v = pd.read_parquet(B.HEIGHT_VS_TOLL_VERDICT_PATH)
    fp, vp = d / "real_fig.parquet", d / "real_ver.parquet"
    f.to_parquet(fp, index=False)
    if drop_many:
        v = v.drop(columns=list(drop_many))
    if flip:
        m = ((v["lens"] == lens) & (v["asset"] == asset)
             & (v["scale_kind"] == B.HEIGHT_VS_TOLL_SCALE))
        v.loc[m, "verdict_pass"] = True
        v.loc[m, "reason"] = "INVENTED — this row is not the figures row"
    v.to_parquet(vp, index=False)
    return fp, vp


def _orphan_scan() -> list:
    """THE ORPHAN GUARD.  Names every parquet in `census/` that carries the
    DECLARED key columns of a [Q-R3] table whose declared path is NOT filed.

    This is the leg whose absence let the last round's interface pass: the
    declaration pointed at `census/height_vs_toll.parquet`, which has never
    existed, while `census/height_toll.parquet` and
    `census/height_toll_verdict.parquet` sat in the same directory carrying
    exactly those key columns.  Empty list = the declaration points at what
    is filed, or the measurement is genuinely absent from the directory.
    """
    import pandas as pd                                      # noqa: PLC0415
    out = []
    for declared, key in ((B.HEIGHT_VS_TOLL_PATH, B.HEIGHT_VS_TOLL_KEY),
                          (B.HEIGHT_VS_TOLL_VERDICT_PATH,
                           B.HEIGHT_VS_TOLL_VERDICT_KEY)):
        if declared.is_file():
            continue
        d = declared.parent
        for q in sorted(d.glob("*.parquet")) if d.is_dir() else []:
            try:
                cols = set(pd.read_parquet(q, columns=None).columns)
            except Exception:                               # noqa: BLE001
                continue
            if set(key) <= cols:
                out.append(f"{declared.name} is NOT filed, but {q.name} "
                           f"carries its declared key {list(key)}")
    return out


def _row_runs(root: Path) -> dict:
    """Both BRK forms, each run TWICE — once on its scored anchor and once on
    the OTHER one — on synthetic tapes under a real panel name."""
    out: dict = {}
    s_lo, _s_hi, _ = TP.corridor_era(SPINE_PANEL, "holdout")
    tuned = B.tuned_pins("5m")
    lf, f4, dies, touch = _spine_s1_tapes(int(s_lo) + 30 * MS_1D, tuned)
    flips = [{"i": 600, "polarity": "support", "rid": 11}]
    TP.register("P-BRK-X-ROW-S1", SPINE_TEXT, 30, root=root, arms=[
        TP.arm_spec("row s1", SPINE_PANEL, "vs_zero", lanes=(B.LANE_S1,),
                    loao_line="lineage", era="holdout")])
    sig = {SPINE_SYM: {"dies": dies, "flips": flips}}
    with planted_frames({(SPINE_SYM, "5m", True): lf,
                         (SPINE_SYM, "4h", False): f4}):
        for key, anc in (("scored", B.ANCHOR_BAND),
                         ("tier_e", B.ANCHOR_MEMORY)):
            out[(B.LANE_S1, key)] = B.run_lane_s1(
                SPINE_PANEL, "P-BRK-X-ROW-S1", SPINE_TEXT, "row s1", sig,
                head_of_record=TP.UNPINNED, reg_root=root, anchor=anc)
    i_lo, _i_hi, _ = TP.corridor_era(SPINE_PANEL, "full")
    lfd, w1, d_dies, d_flips, _want = _spine_i1_tapes(int(i_lo) + 500 * MS_1D)
    TP.register("P-BRK-X-ROW-I1", SPINE_TEXT, 30, root=root, arms=[
        TP.arm_spec("row i1", SPINE_PANEL, "vs_zero", lanes=(B.LANE_I1,),
                    loao_line="lineage", era="full")])
    sig1 = {SPINE_SYM: {"dies": d_dies, "flips": d_flips}}
    with planted_frames({(SPINE_SYM, "1d", True): lfd,
                         (SPINE_SYM, "1w", False): w1}):
        for key, anc in (("scored", B.ANCHOR_MEMORY),
                         ("tier_e", B.ANCHOR_BAND)):
            out[(B.LANE_I1, key)] = B.run_lane_i1(
                SPINE_PANEL, "P-BRK-X-ROW-I1", SPINE_TEXT, "row i1", sig1,
                head_of_record=TP.UNPINNED, reg_root=root, anchor=anc)
    return out


def _row_checks() -> tuple:
    lines, ok = [], True
    J = dict(sort_keys=True, default=str)
    with tempfile.TemporaryDirectory(prefix="f-brk-row-") as td:
        root = Path(td) / "registrations"
        root.mkdir(parents=True)
        runs = _row_runs(root)
        s_sc, s_te = runs[(B.LANE_S1, "scored")], runs[(B.LANE_S1, "tier_e")]
        i_sc, i_te = runs[(B.LANE_I1, "scored")], runs[(B.LANE_I1, "tier_e")]
        # ── 0 · a row can only be built on a Book, i.e. on a FILED arm ──────
        bare = dict(s_sc, book=list(s_sc["book"]))
        did, why = refused(lambda: B.brk_row(B.LANE_S1, bare, s_te,
                                             require_verdict=False))
        g = did and "TP.Book" in why
        ok &= g
        lines.append(mark(g, f"a row offered a PLAIN LIST instead of the Book "
                             f"-> {'HALT' if did else 'assembled anyway'}: "
                             f"{why[:130]} — [LAW 4] no BRK registration "
                             f"exists, so no real Book can be offered at all"))
        # ── 1 · the row itself, with the verdict slot left PENDING ──────────
        r = B.brk_row(B.LANE_S1, s_sc, s_te, require_verdict=False)
        spec = s_sc["book"].spec
        g = (tuple(r) == B.ROW_FIELDS
             and r["form"] == "P-BRK-S1" and r["lane"] == B.LANE_S1
             and r["lens"] == "5m" and r["era"] == "holdout"
             and r["anchor_scored"] == B.ANCHOR_BAND
             and r["anchor_tier_e"] == B.ANCHOR_MEMORY
             and r["registration"] == spec["registration"]
             and r["arm"] == spec["arm"]
             and r["registration_sha256"] == spec["registration_sha256"]
             and r["panel"] == list(spec["panel"])
             and r["panel_name"] == TP.panel_name(spec["panel"])
             and r["as_of_last_closed_4h"] == "2026-09-21T16:00:00Z"
             and r["seed"] == B.SEED)
        ok &= g
        lines.append(mark(g, f"P-BRK-S1's row carries EXACTLY the "
                             f"{len(B.ROW_FIELDS)} declared fields: lens "
                             f"{r['lens']}, era {r['era']}, panel "
                             f"{r['panel_name']} {r['panel']}, registration "
                             f"{r['registration']!r}/{r['arm']!r} (sha "
                             f"{str(r['registration_sha256'])[:16]}), as_of "
                             f"{r['as_of_last_closed_4h']}"))
        # ── 2 · the SCORED figures are the journal's, and no ruler ran ──────
        tr = list(s_sc["book"])
        f_ = r["scored_figures"]
        hand = round(sum(float(t.net_r) for t in tr), B.ROW_ROUND_ND)
        g = (f_["tier"] == "SCORED" and f_["anchor"] == B.ANCHOR_BAND
             and f_["n_campaigns"] == len(tr) == 1
             and f_["net_r_sum"] == hand
             and f_["scored_statistic"] is None
             and "TP.score" in f_["scored_statistic_note"]
             and f_["book_spec"]["registration"] == spec["registration"])
        ok &= g
        lines.append(mark(g, f"the SCORED block is the journal and NOT a "
                             f"verdict: {f_['n_campaigns']} campaign(s), "
                             f"net_r sum {f_['net_r_sum']} (hand {hand}), "
                             f"fee_r {f_['fee_r_sum']}, funding_r "
                             f"{f_['funding_r_sum']}, scored_statistic "
                             f"{f_['scored_statistic']} — the ruler stays "
                             f"tierc10_panel's"))
        # ── 3 · the OTHER anchor, as Tier-E, on the same row [line 112] ─────
        o = r["tier_e_other_anchor"]
        g = (o is not None and o["anchor"] == B.ANCHOR_MEMORY
             and o["anchor"] != f_["anchor"]
             and o["tier"].startswith("TIER-E")
             and o["n_campaigns"] == len(list(s_te["book"]))
             and r["tier_e_other_anchor_note"] is None)
        ok &= g
        lines.append(mark(g, f"the OTHER anchor rides the SAME row, labelled "
                             f"Tier-E: scored {f_['anchor']!r} "
                             f"({f_['n_campaigns']} campaigns) vs Tier-E "
                             f"{o['anchor'] if o else '-'!r} "
                             f"({o['n_campaigns'] if o else '-'} campaigns), "
                             f"tier {o['tier'] if o else '-'}"))
        did, why = refused(lambda: B.brk_row(B.LANE_S1, s_sc, s_sc,
                                             require_verdict=False))
        g = did and "OTHER anchor" in why
        ok &= g
        lines.append(mark(g, f"the SAME anchor offered twice -> "
                             f"{'HALT' if did else 'accepted'}: {why[:130]}"))
        did, why = refused(lambda: B.brk_row(B.LANE_S1, s_sc, s_te, s_te,
                                             require_verdict=False))
        g = did and "SECOND VIEW" in why
        ok &= g
        lines.append(mark(g, f"an R8 17-asset Tier-E slot fed the SAME panel "
                             f"-> {'HALT' if did else 'accepted'}: "
                             f"{why[:130]}"))
        g = (r["tier_e_panel17"] is None
             and "R8" in r["tier_e_panel17_note"])
        ok &= g
        lines.append(mark(g, f"and with no PANEL17 arm filed the 17-asset "
                             f"Tier-E slot is a NAMED ABSENCE, not a blank: "
                             f"{r['tier_e_panel17_note'][:110]}"))
        # ── 4 · the era pin rides the row too ──────────────────────────────
        did, why = refused(lambda: B.brk_row(B.LANE_S1, dict(s_sc, era="full"),
                                             s_te, require_verdict=False))
        g = did and "LANE_ERA" in why
        ok &= g
        lines.append(mark(g, f"a row assembled from a 'full'-era P-BRK-S1 run "
                             f"-> {'HALT' if did else 'assembled'}: "
                             f"{why[:120]}"))
        # ── 5 · the toll, as stamp_toll left it, and said to be a PRINT ─────
        t = r["toll"]
        med = f_["toll_pct_of_1r_median"]
        hand_med = float(np.median([float(x.toll_pct_of_1r) for x in tr]))
        g = (t["cls"] == s_sc["toll"]["cls"]
             and t["per_asset"] == s_sc["toll"]["per_asset"]
             and med is not None and abs(med - round(hand_med, 8)) < 1e-9
             and r["toll_accounting"]["status"].startswith("PRINT, NOT A "
                                                           "DEDUCTION"))
        ok &= g
        lines.append(mark(g, f"the toll on the row is the one stamp_toll "
                             f"stamped: cls {t['cls']!r}, per asset "
                             f"{t['per_asset']}, median {med} % of 1R — and "
                             f"the row SAYS what it is: "
                             f"{r['toll_accounting']['status'][:70]}"))
        # ── 6 · P-BRK-I1's row: the mirror, and NO toll block ──────────────
        r1 = B.brk_row(B.LANE_I1, i_sc, i_te, require_verdict=False)
        g = (r1["form"] == "P-BRK-I1" and r1["lens"] == "1d"
             and r1["era"] == "full"
             and r1["anchor_scored"] == B.ANCHOR_MEMORY
             and r1["tier_e_other_anchor"]["anchor"] == B.ANCHOR_BAND
             and r1["toll"].get("stamped") is False
             and "P-BRK-S1's contract clause" in r1["toll"]["why"]
             and r1["scored_figures"]["n_campaigns"]
             == len(list(i_sc["book"])))
        ok &= g
        lines.append(mark(g, f"P-BRK-I1's row mirrors it: lens "
                             f"{r1['lens']}, era {r1['era']}, scored anchor "
                             f"{r1['anchor_scored']!r}, Tier-E "
                             f"{r1['tier_e_other_anchor']['anchor']!r}, and "
                             f"the toll block is a STATED ABSENCE "
                             f"({r1['toll']['why'][:70]})"))
        # ── 7 · the VERDICT SLOT, before [Q-R3] exists ─────────────────────
        gone = Path(td) / "not_filed.parquet"
        try:
            B.brk_row(B.LANE_S1, s_sc, s_te, hvt_path=gone)
            did, full = False, "ran to completion — a verdict was INVENTED"
        except SystemExit as e:                             # noqa: PERF203
            did, full = True, _norm(str(e))
        g = (did and "height-vs-toll" in full and _norm(str(gone)) in full
             and all(w in full for w in B.HEIGHT_VS_TOLL_FIELDS)
             and all(w in full for w in B.HEIGHT_VS_TOLL_KEY))
        ok &= g
        lines.append(mark(g, f"with [Q-R3] unfiled, assembling a row that "
                             f"REQUIRES the verdict -> "
                             f"{'HALT naming the whole expected schema'
                                if did else 'a default'}: {full[:230]}"))
        pv = r["height_vs_toll"]
        # COMPARISON IS A READ TOO (review, 2026-09-22): `pv == 'PASS'` used
        # to answer False SILENTLY, so `if row['height_vs_toll'] != 'TOLL
        # DOMINATES': ship()` proceeded on an unread verdict.  Twelve reads,
        # not ten.
        reads = {"str": lambda: str(pv), "repr": lambda: repr(pv),
                 "format": lambda: f"{pv}", "float": lambda: float(pv),
                 "bool": lambda: bool(pv), "len": lambda: len(pv),
                 "iter": lambda: list(pv), "getitem": lambda: pv["verdict"],
                 "getattr": lambda: pv.verdict,
                 "json": lambda: json.dumps(r, **J),
                 "eq": lambda: pv == "PASS", "ne": lambda: pv != "FAIL",
                 "in_list": lambda: pv in ["PASS", "FAIL"],
                 "reflected_eq": lambda: "PASS" in [pv],
                 "lt": lambda: pv < 1, "hash": lambda: hash(pv)}
        red = {k: _halts(v) for k, v in reads.items()}
        g = (isinstance(pv, B.PendingVerdict) and all(red.values())
             and (pv is None) is False          # identity is NOT a read
             and pv.lens == "5m" and pv.asset == ROW_ASSET)
        ok &= g
        lines.append(mark(g, f"and the slot itself CANNOT BE READ: every one "
                             f"of {sorted(red)} HALTs ({red}) — including "
                             f"EQUALITY, which used to answer False silently "
                             f"— while `is None` stays False and the REQUEST "
                             f"stays legible (lens {pv.lens!r}, asset "
                             f"{pv.asset!r}, scale {pv.scale_kind!r}, era "
                             f"{pv.era!r}, verdict table "
                             f"{Path(pv.verdict_path).name}), so a reporter "
                             f"can say WHICH verdict is missing without "
                             f"tripping the guard"))
        # ── 8 · and once [Q-R3] IS filed, the verdict is READ, verbatim ────
        hp, hvp = _hvt_pair(Path(td))
        r2 = B.brk_row(B.LANE_S1, s_sc, s_te, hvt_path=hp,
                       hvt_verdict_path=hvp)
        hv = r2["height_vs_toll"]
        g = (hv["verdict_pass"] is ROW_VERDICT_PASS
             and hv["verdict_law"] == ROW_VERDICT_LAW
             and hv["reason"] == ROW_VERDICT_REASON
             and hv["lens"] == "5m" and hv["asset"] == ROW_ASSET
             and hv["scale_kind"] == B.HEIGHT_VS_TOLL_SCALE
             and hv["era"] == B.HEIGHT_VS_TOLL_ERA
             and hv["ratio_median"] == 7.9148
             and hv["n_ranges"] == 1234
             and hv["height_atr_median"] == SYN_FIG["height_atr_median"]
             and hv["toll_atr_median"] == SYN_FIG["toll_atr_median"]
             and hv["as_of_last_closed_4h"] == ASOF
             and hv["read_not_computed"] is True
             and hv["source"] == str(hp) and hv["verdict_source"] == str(hvp)
             # THE ATTESTATION IS THE CHECK'S OWN OUTPUT [round 2, finding 2]:
             # `cross_checked` is compared against the fields THIS FIXTURE
             # can see in both filed tables, computed independently of the
             # module's constant.
             and hv["cross_checked"] == _shared_cols(hp, hvp)
             and hv["provisional"] is False)
        ok &= g
        lines.append(mark(g, f"with BOTH [Q-R3] tables in the declared "
                             f"schemas the slot FILLS FROM THEM: "
                             f"verdict_pass {hv['verdict_pass']}, law "
                             f"{hv['verdict_law'][:40]!r}, reason "
                             f"{hv['reason']!r} (all three carried verbatim "
                             f"— this module pins no vocabulary), "
                             f"ratio_median {hv['ratio_median']}, n_ranges "
                             f"{hv['n_ranges']}, as_of "
                             f"{hv['as_of_last_closed_4h']}, sources "
                             f"{Path(hv['source']).name} + "
                             f"{Path(hv['verdict_source']).name}, "
                             f"cross-checked on {hv['cross_checked']}, "
                             f"read_not_computed {hv['read_not_computed']}"))
        # ── 8b · THE INTERFACE AGAINST THE REAL FILED CENSUS TABLES ────────
        # THE LEG THAT WAS MISSING.  Every [Q-R3] check above reads a table
        # THIS FIXTURE WROTE, in the schema THIS MODULE declared — which is
        # exactly how an interface pointed at a filename that has never
        # existed collected 22 green checks.  This leg reads what the CENSUS
        # TRACK actually filed, through the module's own reader, and asserts
        # its numbers.
        for (lens_, asset_), want in sorted(REAL_HVT.items()):
            got = B.height_vs_toll(lens_, asset_)
            g = (all(got[k] == v for k, v in want.items())
                 and got["source"] == str(B.HEIGHT_VS_TOLL_PATH)
                 and got["verdict_source"] == str(
                     B.HEIGHT_VS_TOLL_VERDICT_PATH)
                 and got["as_of_last_closed_4h"] == ASOF
                 and got["read_not_computed"] is True)
            ok &= g
            lines.append(mark(g, f"the REAL filed [Q-R3] read, lens {lens_} / "
                                 f"{asset_} / {B.HEIGHT_VS_TOLL_SCALE} / "
                                 f"era {B.HEIGHT_VS_TOLL_ERA}: n_ranges "
                                 f"{got['n_ranges']}, height_atr_median "
                                 f"{got['height_atr_median']}, "
                                 f"toll_atr_median {got['toll_atr_median']}, "
                                 f"ratio_median {got['ratio_median']}, "
                                 f"verdict_pass {got['verdict_pass']} "
                                 f"({got['reason']}) — expected "
                                 f"{ {k: want[k] for k in sorted(want)} }"))
        # ── 8c · THE DECLARED PATHS ARE THE FILED PATHS, OR AN ORPHAN IS
        # ──      NAMED.  The guard that would have caught the dead interface
        # ──      the moment the census filed at 10:25: either the declared
        # ──      table exists, or NO other parquet in census/ carries the
        # ──      declared key columns (i.e. the measurement really is absent
        # ──      rather than sitting ten characters away under another name).
        orph = _orphan_scan()
        g = not orph
        ok &= g
        lines.append(mark(g, f"the DECLARED [Q-R3] paths are the FILED ones: "
                             f"figures {B.HEIGHT_VS_TOLL_PATH.name} "
                             f"present={B.HEIGHT_VS_TOLL_PATH.is_file()}, "
                             f"verdict {B.HEIGHT_VS_TOLL_VERDICT_PATH.name} "
                             f"present="
                             f"{B.HEIGHT_VS_TOLL_VERDICT_PATH.is_file()}; "
                             f"orphan candidates in census/ carrying the "
                             f"declared key columns while the declaration "
                             f"points elsewhere: {orph or 'none'}"))
        # ── 8d · THE VERDICT ROW'S ASSET IS DERIVED FROM THE BOOK ─────────
        # [review round 2, finding 1]  brk_row used to read
        #   asset = str(verdict_asset) if verdict_asset else "POOLED:CLASSIC5"
        # with `verdict_asset` derived from NOTHING.  These are the
        # derivations, the HALT where nothing can be derived, and the
        # override rules.
        for pnl, want_a, tag in (
                (TP.CLASSIC5, "POOLED:CLASSIC5", "the 5-asset book [R8]"),
                (TP.UNSEEN12, "POOLED:UNSEEN12", "the twelve"),
                ((SPINE_SYM,), SPINE_SYM, "a ONE-ASSET book")):
            va = B.verdict_asset_of(pnl)
            g = (va["asset"] == want_a and va["derived"] == want_a
                 and va["override"] is None
                 and va["source"] == "DERIVED FROM THE BOOK")
            ok &= g
            lines.append(mark(g, f"{tag}: panel {va['panel_name']} "
                                 f"({va['n_panel_assets']} assets) -> census "
                                 f"row {va['asset']!r} — {va['derived_how']}"))
        did, why = refused_long(lambda: B.verdict_asset_of(TP.PANEL17))
        g = (did and "PANEL17" in why and "POOLED:ALL" in why
             and "cannot be DERIVED" in why)
        ok &= g
        lines.append(mark(g, f"PANEL17 — the view R8 orders printed as "
                             f"Tier-E — has NO census counterpart and "
                             f"-> {'HALT' if did else 'a default'}: "
                             f"{why[:200]}"))
        did, why = refused_long(lambda: B.verdict_asset_of(()))
        g = did and "EMPTY panel" in why
        ok &= g
        lines.append(mark(g, f"an EMPTY panel -> "
                             f"{'HALT' if did else 'a default'}: "
                             f"{why[:120]}"))
        did, why = refused_long(
            lambda: B.verdict_asset_of((SPINE_SYM,), "POOLED:CLASSIC5"))
        g = did and "OVERRIDDEN" in why and "verdict_asset_why" in why
        ok &= g
        lines.append(mark(g, f"an OVERRIDE that disagrees with the "
                             f"derivation and says nothing -> "
                             f"{'HALT' if did else 'accepted'}: {why[:170]}"))
        va = B.verdict_asset_of((SPINE_SYM,), "POOLED:CLASSIC5",
                                "a stated reason, filed on the row")
        g = (va["asset"] == "POOLED:CLASSIC5" and va["derived"] == SPINE_SYM
             and va["override"] == "POOLED:CLASSIC5"
             and va["override_why"] == "a stated reason, filed on the row"
             and va["source"].startswith("EXPLICIT OVERRIDE"))
        ok &= g
        lines.append(mark(g, f"and the SAME override WITH a stated reason is "
                             f"taken and RECORDED: asset {va['asset']!r}, "
                             f"derived {va['derived']!r}, why "
                             f"{va['override_why']!r} ({va['source']})"))
        did, why = refused_long(
            lambda: B.verdict_asset_of(TP.PANEL17, "POOLED:ALL"))
        g = did and "NOTHING can be derived" in why
        ok &= g
        lines.append(mark(g, f"PANEL17 named POOLED:ALL with no reason -> "
                             f"{'HALT' if did else 'accepted'}: {why[:150]}"))
        # ── 8e · A ROW ON A NON-CLASSIC5 BOOK DOES NOT RECEIVE CLASSIC5'S
        # ──      FIGURES.  The REAL filed census tables, the real reader,
        # ──      and the spine's real one-asset Book.
        r_real = B.brk_row(B.LANE_S1, s_sc, s_te)
        vaq, hvq = r_real["height_vs_toll_asset"], r_real["height_vs_toll"]
        c5 = B.height_vs_toll("5m", "POOLED:CLASSIC5")
        g = (tuple(r_real) == B.ROW_FIELDS
             and r_real["panel"] == [SPINE_SYM]
             and vaq["asset"] == SPINE_SYM
             and vaq["source"] == "DERIVED FROM THE BOOK"
             and hvq["asset"] == SPINE_SYM
             and all(hvq[k] == v for k, v in REAL_BTC_5M.items())
             and c5["n_ranges"] == REAL_CLASSIC5_5M_N
             and hvq["n_ranges"] != c5["n_ranges"]
             and hvq["provisional"] is False)
        ok &= g
        lines.append(mark(g, f"a row on the NON-CLASSIC5 book "
                             f"{r_real['panel_name']} {r_real['panel']} reads "
                             f"its OWN census row {hvq['asset']!r}: n_ranges "
                             f"{hvq['n_ranges']}, height_atr_median "
                             f"{hvq['height_atr_median']}, toll_atr_median "
                             f"{hvq['toll_atr_median']}, ratio_median "
                             f"{hvq['ratio_median']}, verdict_pass "
                             f"{hvq['verdict_pass']} — and NOT "
                             f"POOLED:CLASSIC5's {c5['n_ranges']} / "
                             f"{c5['ratio_median']} / {c5['verdict_pass']}, "
                             f"which is what the literal default handed it "
                             f"before the repair"))
        bufa = io.StringIO()
        B.print_rows([r_real], out=bufa)
        ta = bufa.getvalue()
        g = (f"asset {SPINE_SYM!r}" in ta and "DERIVED FROM THE BOOK" in ta)
        ok &= g
        lines.append(mark(g, f"and the choice PRINTS ON THE ROW: "
                             f"\"asset {SPINE_SYM!r}\" present="
                             f"{f'asset {SPINE_SYM!r}' in ta}, "
                             f"'DERIVED FROM THE BOOK' present="
                             f"{'DERIVED FROM THE BOOK' in ta}"))
        # ── 8f · A PROVISIONAL CENSUS ROW CANNOT REACH A BRK ROW SILENTLY ──
        # The census re-filed [Q-R3] with a sample floor; BTCUSDT 1d rests on
        # 11 confirmed ranges against a floor of 30.  P-BRK-I1's lens IS 1d,
        # so this is not a hypothetical.
        did, why = refused_long(lambda: B.brk_row(B.LANE_I1, i_sc, i_te))
        g = (did and "PROVISIONAL" in why and "edge_n_ranges" in why
             and str(REAL_BTC_1D_FLOOR) in why
             and "allow_provisional" in why)
        ok &= g
        lines.append(mark(g, f"P-BRK-I1's row on the 1d census row for "
                             f"{SPINE_SYM} (n_ranges {REAL_BTC_1D_N} against "
                             f"floor {REAL_BTC_1D_FLOOR}) -> "
                             f"{'HALT' if did else 'carried silently'}: "
                             f"{why[:230]}"))
        r_prov = B.brk_row(B.LANE_I1, i_sc, i_te, allow_provisional=True)
        hpv = r_prov["height_vs_toll"]
        g = (hpv["provisional"] is True
             and hpv["provisional_taken_by_name"] is True
             and "PROVISIONAL_MIN_N" in hpv["provisional_reason"]
             and hpv["sample_floor"]["n_ranges"] == REAL_BTC_1D_N
             and hpv["sample_floor"]["edge_n_ranges"] == REAL_BTC_1D_EDGE_N
             and hpv["sample_floor"]["min_n_ranges_pinned"]
             == REAL_BTC_1D_FLOOR)
        ok &= g
        lines.append(mark(g, f"taken BY NAME it rides the row FLAGGED: "
                             f"provisional {hpv['provisional']}, reason "
                             f"{hpv['provisional_reason']!r}, floor block "
                             f"{ {k: hpv['sample_floor'][k] for k in
                                  ('n_ranges', 'min_n_ranges_pinned',
                                   'edge_n_ranges',
                                   'edge_min_n_ranges_pinned')} }"))
        bufb = io.StringIO()
        B.print_rows([r_prov], out=bufb)
        tb = bufb.getvalue()
        star = "*** PROVISIONAL [Q-R3] ROW, TAKEN BY NAME"
        g = star in tb and "gates nothing" in tb
        ok &= g
        lines.append(mark(g, f"and it PRINTS LOUDLY: the starred PROVISIONAL "
                             f"block is present={star in tb}, "
                             f"'gates nothing' present="
                             f"{'gates nothing' in tb}"))
        # ── 8g · THE REVIEWER'S OWN REPRODUCTION, ON THE REAL FILED TABLES ─
        d_rv = Path(td) / "real_copy"
        d_rv.mkdir()
        fpx, vpx = _real_hvt_copy(
            d_rv, drop_many=("n_ranges", "height_atr_median",
                             "toll_atr_median"), flip=True)
        did, why = refused_long(
            lambda: B.height_vs_toll("5m", "POOLED:CLASSIC5", path=fpx,
                                     verdict_path=vpx))
        g = (did and all(w in why for w in ("n_ranges", "height_atr_median",
                                            "toll_atr_median")))
        ok &= g
        shipped_said = ("verdict_pass True with an attestation for a check "
                        "that never ran")
        lines.append(mark(g, f"the two REAL filed tables, with "
                             f"['n_ranges', 'height_atr_median', "
                             f"'toll_atr_median'] dropped from the VERDICT "
                             f"copy AND 5m/POOLED:CLASSIC5/frozen3.0 flipped "
                             f"to verdict_pass=True, reason 'INVENTED' -> "
                             f"{'HALT' if did else shipped_said}: "
                             f"{why[:210]}"))
        g = (c5["verdict_pass"] is False
             and c5["reason"] != "INVENTED — this row is not the figures row")
        ok &= g
        lines.append(mark(g, f"so the flipped verdict never reaches a row: "
                             f"the UNMODIFIED filed pair still reads "
                             f"verdict_pass {c5['verdict_pass']} "
                             f"({c5['reason']!r}) for 5m POOLED:CLASSIC5. "
                             f"STATED LIMIT: the cross-check proves the two "
                             f"rows are ONE MEASUREMENT (figures + "
                             f"gate_law_sha); it does not audit verdict_pass "
                             f"itself — that is the census's own gate, and "
                             f"[B10] says this row carries a verdict and "
                             f"computes none. A verdict re-filed wrong WITH "
                             f"consistent figures and the same gate law is "
                             f"invisible here and visible only to [Q-R3]."))
        # ── 9 · every way those tables can be wrong is a HALT, not a default ─
        for k_, (name, mk, word) in enumerate((
                ("a missing declared FIGURES column",
                 lambda d: (_hvt_table(d / "f.parquet", drop="ratio_median"),
                            _hvt_verdict(d / "v.parquet")),
                 "ratio_median"),
                ("a missing declared VERDICT column",
                 lambda d: (_hvt_table(d / "f.parquet"),
                            _hvt_verdict(d / "v.parquet", drop="reason")),
                 "reason"),
                ("no as-of stamp on the FIGURES table",
                 lambda d: (_hvt_table(d / "f.parquet",
                                       drop=B.HEIGHT_VS_TOLL_ASOF_COL),
                            _hvt_verdict(d / "v.parquet")),
                 B.HEIGHT_VS_TOLL_ASOF_COL),
                ("a FIGURES row stamped at another as-of",
                 lambda d: (_hvt_table(d / "f.parquet",
                                       asof="2026-09-22T00:00:00Z"),
                            _hvt_verdict(d / "v.parquet")),
                 "AS-OF WARRANTY"),
                ("a VERDICT row stamped at another as-of",
                 lambda d: (_hvt_table(d / "f.parquet"),
                            _hvt_verdict(d / "v.parquet",
                                         asof="2026-09-22T00:00:00Z")),
                 "AS-OF WARRANTY"),
                ("no FIGURES row for this lens",
                 lambda d: (_hvt_table(d / "f.parquet", lens="4h"),
                            _hvt_verdict(d / "v.parquet")), "0 row(s)"),
                ("no VERDICT row for this lens",
                 lambda d: (_hvt_table(d / "f.parquet"),
                            _hvt_verdict(d / "v.parquet", lens="4h")),
                 "0 row(s)"),
                ("the FIGURES key repeated",
                 lambda d: (_hvt_table(d / "f.parquet", dupe=True),
                            _hvt_verdict(d / "v.parquet")), "2 row(s)"),
                ("the VERDICT key repeated",
                 lambda d: (_hvt_table(d / "f.parquet"),
                            _hvt_verdict(d / "v.parquet", dupe=True)),
                 "2 row(s)"),
                ("the two tables DISAGREEING on a shared figure",
                 lambda d: (_hvt_table(d / "f.parquet"),
                            _hvt_verdict(d / "v.parquet", n_ranges=9999)),
                 "disagree"),
                ("a non-boolean verdict_pass",
                 lambda d: (_hvt_table(d / "f.parquet"),
                            _hvt_verdict(d / "v.parquet",
                                         verdict_pass=float("nan"))),
                 "not a boolean"),
                ("a blank verdict_law",
                 lambda d: (_hvt_table(d / "f.parquet"),
                            _hvt_verdict(d / "v.parquet", verdict_law="   ")),
                 "carries no verdict_law"),
                ("a blank reason",
                 lambda d: (_hvt_table(d / "f.parquet"),
                            _hvt_verdict(d / "v.parquet", reason="   ")),
                 "carries no reason"),
                ("the VERDICT table not filed at all",
                 lambda d: (_hvt_table(d / "f.parquet"), d / "gone.parquet"),
                 "no height-vs-toll VERDICT table"),
                # ── THE ROUND-2 FINDING-2 LEG.  The VERDICT table re-filed
                # ── WITHOUT the shared figures AND with its verdict flipped:
                # ── the drop is what severed the join, and the flip is what
                # ── the severed join used to let through.
                ("the VERDICT table RE-FILED WITHOUT THE SHARED FIGURES and "
                 "its verdict FLIPPED to PASS",
                 lambda d: (_hvt_table(d / "f.parquet"),
                            _hvt_verdict(
                                d / "v.parquet",
                                drop_many=tuple(B.HEIGHT_VS_TOLL_AGREE),
                                verdict_pass=True,
                                reason=("INVENTED — this row is not the "
                                        "figures row"))),
                 "missing the declared column(s)"),
                ("the VERDICT table re-filed WITHOUT the gate-law sha",
                 lambda d: (_hvt_table(d / "f.parquet"),
                            _hvt_verdict(d / "v.parquet",
                                         drop="gate_law_sha")),
                 "missing the declared column(s)"),
                ("the two tables built under DIFFERENT gate laws",
                 lambda d: (_hvt_table(d / "f.parquet"),
                            _hvt_verdict(d / "v.parquet",
                                         gate_law_sha="A-DIFFERENT-LAW")),
                 "disagree"),
                ("the VERDICT table re-filed WITHOUT the census's "
                 "provisional flag",
                 lambda d: (_hvt_table(d / "f.parquet"),
                            _hvt_verdict(d / "v.parquet",
                                         drop="provisional")),
                 "missing the declared column(s)"),
                ("the VERDICT table re-filed without edge_n_ranges",
                 lambda d: (_hvt_table(d / "f.parquet"),
                            _hvt_verdict(d / "v.parquet",
                                         drop="edge_n_ranges")),
                 "missing the declared column(s)"),
                ("a PROVISIONAL verdict row not asked for by name",
                 lambda d: (_hvt_table(d / "f.parquet"),
                            _hvt_verdict(d / "v.parquet", provisional=True,
                                         provisional_reason=(
                                             "n_ranges 5 < "
                                             "PROVISIONAL_MIN_N (30)"))),
                 "PROVISIONAL"),
                ("a provisional flag with NO reason behind it",
                 lambda d: (_hvt_table(d / "f.parquet"),
                            _hvt_verdict(d / "v.parquet", provisional=True,
                                         provisional_reason="   ")),
                 "no provisional_reason"),
                ("a non-boolean provisional flag",
                 lambda d: (_hvt_table(d / "f.parquet"),
                            _hvt_verdict(d / "v.parquet",
                                         provisional=float("nan"))),
                 "not a boolean"))):
            # the name is an INDEX, never hash(str): Python salts string
            # hashing per process, and a filed transcript must be the same
            # bytes on every run (DETERMINISM — the law applies to the
            # evidence too, F-DET's own reason for `_norm`).
            d_ = Path(td) / f"hvt_{k_}"
            d_.mkdir()
            fq, vq = mk(d_)
            did, why = refused_long(
                lambda _f=fq, _v=vq: B.height_vs_toll("5m", ROW_ASSET,
                                                      path=_f,
                                                      verdict_path=_v))
            g = did and word in why
            ok &= g
            lines.append(mark(g, f"[Q-R3] with {name} -> "
                                 f"{'HALT' if did else 'a number'}: "
                                 f"{why[:150]}"))
        # ── 10 · DETERMINISM: two assemblies, one byte string ──────────────
        a = json.dumps(B.brk_row(B.LANE_S1, s_sc, s_te, hvt_path=hp,
                                 hvt_verdict_path=hvp), **J)
        b = json.dumps(B.brk_row(B.LANE_S1, s_sc, s_te, hvt_path=hp,
                                 hvt_verdict_path=hvp), **J)
        g = a == b and len(a) > 2000
        ok &= g
        lines.append(mark(g, f"two assemblies of the same runs are the same "
                             f"bytes ({len(a)} B, identical={a == b})"))
        # ── 11 · brk_rows: every form, in order, nothing dropped ───────────
        rows = B.brk_rows({B.LANE_S1: {"scored": s_sc, "tier_e": s_te},
                           B.LANE_I1: {"scored": i_sc, "tier_e": i_te}},
                          require_verdict=False)
        g = ([x["lane"] for x in rows] == list(B.LANE_ORDER)
             and [x["form"] for x in rows] == ["P-BRK-S1", "P-BRK-I1"])
        ok &= g
        lines.append(mark(g, f"brk_rows emits ONE ROW PER FORM in "
                             f"LANE_ORDER: {[x['form'] for x in rows]}"))
        did, why = refused(lambda: B.brk_rows({"brk-x9": {"scored": s_sc}}))
        g = did and "brk-x9" in why
        ok &= g
        lines.append(mark(g, f"a lane the module does not carry -> "
                             f"{'HALT' if did else 'silently dropped'}: "
                             f"{why[:100]}"))
        # ── 12 · the PRINTER prints PENDING rather than a blank ────────────
        buf = io.StringIO()
        B.print_rows(rows, out=buf)
        txt = buf.getvalue()
        g = ("PENDING" in txt and "Reading this slot HALTs" in txt
             and "TIER-E" in txt and "P-BRK-S1" in txt and "P-BRK-I1" in txt)
        ok &= g
        lines.append(mark(g, f"print_rows on PENDING rows names the absence "
                             f"({len(txt)} B; 'PENDING' present={'PENDING' in txt}, "
                             f"Tier-E labelled={'TIER-E' in txt})"))
        buf2 = io.StringIO()
        B.print_rows([r2], out=buf2)
        t2 = buf2.getvalue()
        g = (ROW_VERDICT_REASON in t2
             and f"verdict_pass {ROW_VERDICT_PASS}" in t2)
        ok &= g
        lines.append(mark(g, f"and on a filled row it prints the verdict it "
                             f"READ (verdict_pass {ROW_VERDICT_PASS} "
                             f"present={f'verdict_pass {ROW_VERDICT_PASS}' in t2}, "
                             f"reason {ROW_VERDICT_REASON!r} "
                             f"present={ROW_VERDICT_REASON in t2})"))
    return ok, lines


def f_brk_row() -> bool:
    class _Readable:
        """A named wrong: the empty verdict slot made READABLE — the `None`
        that serialises to `null` and prints as a blank, which is the kind of
        blank a later reader fills in from memory."""
        def __init__(self, *a, **k):
            self.lens, self.asset = "5m", ROW_ASSET
            self.scale_kind, self.era, self.path = "frozen3.0", "ALL", ""
            self.verdict_path = ""      # so this leg goes RED on READABILITY
            self.verdict = "UNKNOWN"    # and not on a missing attribute

        def __str__(self):
            return "UNKNOWN"

    class _IdentityEq(B.PendingVerdict):
        """A named wrong: the empty verdict slot left at OBJECT IDENTITY for
        comparison — the shipped defect (review, 2026-09-22).  Every OTHER
        read still HALTs, so only a leg that actually compares can see it."""
        __eq__ = object.__eq__
        __ne__ = object.__ne__
        __hash__ = B.PendingVerdict.__hash__

    def _defaulted(lens, asset, scale_kind=B.HEIGHT_VS_TOLL_SCALE,
                   era=B.HEIGHT_VS_TOLL_ERA, path=None, verdict_path=None,
                   allow_provisional=False):
        """A named wrong: a verdict INVENTED when [Q-R3] is not filed."""
        return {"asset": asset, "lens": lens, "scale_kind": scale_kind,
                "era": era, "height_atr_median": None,
                "toll_atr_median": None, "ratio_median": None,
                "n_ranges": 0, "verdict_pass": True,
                "verdict_law": "(default)", "reason": "(default)",
                "provisional": False, "provisional_reason": "",
                "provisional_taken_by_name": False,
                "sample_floor": {"n_ranges": 0, "min_n_ranges_pinned": 0,
                                 "edge_n_ranges": 0,
                                 "edge_min_n_ranges_pinned": 0,
                                 "read_not_pinned_here": "(default)"},
                "gate_law_sha": "(default)",
                "as_of_last_closed_4h": ASOF, "source": "(default)",
                "verdict_source": "(default)",
                "cross_checked": list(B.HEIGHT_VS_TOLL_AGREE),
                "read_not_computed": False}

    def _shipped_asset(panel, override=None, why=None):
        """A named wrong: THE SHIPPED DEFECT of round 2, finding 1 — the
        verdict row's asset DEFAULTED to POOLED:CLASSIC5 for any book.  It is
        `brk_row`'s old line, moved behind the new seam:
            asset = str(verdict_asset) if verdict_asset else "POOLED:CLASSIC5"
        R8 makes CLASSIC5 the BRK panel of record, so this looks right today
        and is wrong for every other book — which is the whole finding."""
        a = str(override) if override else "POOLED:CLASSIC5"
        return {"asset": a, "panel_name": TP.panel_name(tuple(panel or ())),
                "n_panel_assets": len(tuple(panel or ())),
                "derived": a, "derived_how": "(defaulted)",
                "override": str(override) if override else None,
                "override_why": why, "source": "DERIVED FROM THE BOOK",
                "law": "(defaulted)"}

    def _shipped_required(what):
        """A named wrong, half one of the round-2 finding-2 pair: the shared
        cross-check columns NOT required of the VERDICT table, so a verdict
        table lacking them passes every column check."""
        if what == "VERDICT":
            return (list(B.HEIGHT_VS_TOLL_VERDICT_KEY)
                    + list(B.HEIGHT_VS_TOLL_VERDICT_FIELDS)
                    + list(B.HEIGHT_VS_TOLL_PROVISIONAL_FIELDS)
                    + [B.HEIGHT_VS_TOLL_ASOF_COL])
        return (list(B.HEIGHT_VS_TOLL_KEY) + list(B.HEIGHT_VS_TOLL_FIELDS)
                + [B.HEIGHT_VS_TOLL_ASOF_COL])

    def _shipped_shared(r, v, p_, vp_, sel):
        """A named wrong, half two of the pair: an ABSENT shared column
        SKIPPED (`continue`) instead of HALTing, and `cross_checked` attested
        from the CONSTANT instead of from what was compared."""
        for f_ in B.HEIGHT_VS_TOLL_AGREE:
            if f_ not in v.index:
                continue
            if B._num(r[f_]) != B._num(v[f_]):
                raise SystemExit(f"HALT: disagree on {f_}")
        return list(B.HEIGHT_VS_TOLL_AGREE)

    def _no_floor(v, sel, vp_, allow):
        """A named wrong: the census's PROVISIONAL flag ignored, so a row
        resting under the filed sample floor rides a BRK row in silence."""
        return False, ""

    return prove(
        "F-BRK-ROW",
        "each BRK form's row carries the scored anchor, the OTHER anchor as "
        "Tier-E, the lens, era, panel, the stamped toll, and a [Q-R3] verdict "
        "slot that cannot be read before the census files it — the census "
        "row it reads is DERIVED FROM THE BOOK'S PANEL and never defaulted, "
        "a row under the census's sample floor HALTs or prints its flag, and "
        "the declared [Q-R3] interface is the one the CENSUS ACTUALLY FILED",
        "a row is assembled without a Book, the Tier-E block is not the OTHER "
        "anchor, the toll on the row is not the one stamp_toll stamped, the "
        "verdict slot is defaulted, readable or silently COMPARABLE while "
        "[Q-R3] is unfiled, a malformed [Q-R3] pair yields a number instead "
        "of a HALT, the two census tables disagree on a shared figure and are "
        "read anyway, the declared [Q-R3] paths are not the filed ones while "
        "another file in census/ carries the declared keys, the REAL filed "
        "census numbers are not what this reader returns, a form is dropped "
        "from brk_rows, two assemblies of one journal differ, THE VERDICT "
        "ROW'S ASSET IS DEFAULTED RATHER THAN DERIVED FROM THE BOOK'S PANEL "
        "(or a panel with no census counterpart yields one anyway, or an "
        "unexplained override is taken), A VERDICT TABLE RE-FILED WITHOUT THE "
        "SHARED FIGURES IS READ ANYWAY OR `cross_checked` ATTESTS MORE THAN "
        "WAS COMPARED, or A PROVISIONAL CENSUS ROW REACHES A BRK ROW WITHOUT "
        "a HALT or a printed flag",
        [("the verdict row's ASSET defaulted to POOLED:CLASSIC5 for any "
          "book (the shipped defect, round 2 finding 1)",
          mutated(B, "verdict_asset_of", _shipped_asset, _row_checks)),
         ("the two-table cross-check disarmed exactly as it shipped: the "
          "shared figures NOT required of the VERDICT table AND an absent "
          "one SKIPPED, with `cross_checked` attested from the constant "
          "(round 2 finding 2)",
          mutated2(B, [("_hvt_required", _shipped_required),
                       ("_hvt_shared_or_halt", _shipped_shared)],
                   _row_checks)),
         ("the census's PROVISIONAL flag ignored, so a row under the filed "
          "sample floor rides in silence",
          mutated(B, "_hvt_provisional_or_halt", _no_floor, _row_checks)),
         ("the height-vs-toll verdict DEFAULTED when [Q-R3] is absent",
          mutated(B, "height_vs_toll", _defaulted, _row_checks)),
         ("the empty verdict slot made readable (a blank, not a HALT)",
          mutated(B, "PendingVerdict", _Readable, _row_checks)),
         ("the empty verdict slot left COMPARABLE at object identity "
          "(`pv == 'PASS'` answering False silently)",
          mutated(B, "PendingVerdict", _IdentityEq, _row_checks)),
         ("the [Q-R3] interface pointed back at the filename the census "
          "never filed (the shipped defect)",
          mutated(B, "HEIGHT_VS_TOLL_PATH",
                  B.TP.OUT / "census" / "height_vs_toll.parquet",
                  _row_checks)),
         ("the two-table cross-check disarmed (no shared figure compared)",
          mutated(B, "HEIGHT_VS_TOLL_AGREE", (), _row_checks)),
         ("the OTHER anchor declared to be the SAME anchor",
          mutated(B, "LANE_TIER_E_ANCHOR",
                  {B.LANE_S1: B.ANCHOR_BAND, B.LANE_I1: B.ANCHOR_MEMORY},
                  _row_checks))],
        _row_checks)


# ═══════════════════════════════════════════ THE LEANS + RULINGS, PRINTED [L*]
def f_leans() -> bool:
    say("\n--- LEANS + OPERATOR RULINGS — printed verbatim (an attestation, "
        "not a check)")
    for r in B.RULINGS:
        say("    " + r)
    for ln in B.LEANS:
        say("    " + ln)
    say("    FINDINGS NOT FIXED:")
    for f_ in B.FINDINGS:
        say("      · " + f_)
    say("      FAILS IF: never — it is an attestation, and it rides with the "
        "transcript so the pins and the evidence travel together.")
    RESULTS["LEANS+RULINGS"] = True
    return True


LEGS = (f_brk_ride_4h, f_brk_hold_syn, f_c10_hold_harness, f_brk_tuned,
        f_brk_perm, f_brk_fund, f_brk_era, f_brk_lane_era, f_brk_warm,
        f_brk_lane_syn, f_brk_gate, f_brk_spine, f_brk_row, f_c10_toll,
        f_brk_closure, f_det, f_leans)


def main() -> int:
    say("=" * 78)
    say("TIER-C10 BRK FIXTURE TRANSCRIPT — break legs first, RED or void")
    say("=" * 78)
    say(f"substrate {B.substrate()['substrate']} · seed {B.SEED} "
        f"(sensitivity {B.SEED_LINEAGE}) · gate helper {B.GATE_HELPER}")
    say(f"LAW 4: the only real bars read here are the CONTROL's "
        f"(card v6 x CLASSIC5); every BRK lane rides SYNTHETIC tapes only.")
    only = [a.lower().replace("-", "_") for a in sys.argv[1:] if a != "--only"]
    for leg in LEGS:
        if only and not any(o in leg.__name__ for o in only):
            continue
        leg()
    n = sum(RESULTS.values())
    say(f"\nFIXTURE SUMMARY  {n}/{len(RESULTS)} PASS  {json.dumps(RESULTS)}")
    try:
        meta = _B["meta"] if _B else TP.corridor_n(TP.CLASSIC5)[2]
        body = (f"as_of_last_closed_4h: {meta['last_closed_4h_close']}\n"
                + "\n".join(T) + "\n")
        if only:
            # ── THE LAW-2 MECHANISM, CLOSED (review, 2026-09-22) ───────────
            # This line used to write FIXTURES_BRK_partial.txt straight into
            # research_outputs/tierc10/brk/ on ANY filtered run — a KILL-
            # PARTIAL filed beside the artifacts of record, which is the
            # exact class R0 has quarantined three times.  The already-filed
            # FIXTURES_BRK_partial.txt is NOT deleted (a filed artifact is
            # never removed by an executor) and stays named in the
            # manifest's `undeclared_artifacts_present`; what is closed here
            # is the MECHANISM that recreates it.  A filtered run is a debug
            # run: its transcript goes to the system temp directory and the
            # path is printed.
            p = Path(tempfile.gettempdir()) / "FIXTURES_BRK_partial.txt"
            p.write_text(body)
            print(f"FILTERED RUN ({only}) — transcript NOT filed into "
                  f"{BRK_OUT} [LAW 2: a partial transcript is not a stage "
                  f"record]. Written to {p} instead.")
        else:
            BRK_OUT.mkdir(parents=True, exist_ok=True)
            (BRK_OUT / "FIXTURES_BRK.txt").write_text(body)
    except BaseException as e:                              # noqa: BLE001
        print(f"(transcript filing failed, non-fatal: {e})")
    if n != len(RESULTS):
        print("*** HALT: fixture mismatch. Nothing downstream is "
              "trustworthy. ***")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
