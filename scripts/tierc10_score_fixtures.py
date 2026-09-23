#!/usr/bin/env python
"""TIER-C10 · STAGE B · FIXTURES FOR THE SCORING DRIVER (scripts/tierc10_score.py).

Every leg states the condition under which it FAILS, runs GREEN on the code
as it stands, and then re-runs under each of its BREAKS — a sabotage of the
code it certifies — where it must go RED.  A break that leaves the leg GREEN
is VOID and fails the suite: a leg that cannot see its own sabotage is not a
witness.

WHAT THIS SUITE NEVER DOES: call the real `tierc10_panel.score`,
`finish_family`, `_mark_scored` or `register` (every leg that reaches one
installs a stub or a TRIPWIRE first), write a .scored.json, write under
research_outputs/, or compute an outcome of a registered arm.  Synthetic
trades carry synthetic numbers; the two legs that ride REAL bars (the door
order and the spring window) read entry-side facts only.  Temp directories
are created under --tmp (default: the system temp) and their names never
reach the transcript, so two whole runs are byte-identical.

Run:
  export NAIAD_CACHE_DIR=/Users/luis/.cache/naiad/snapshots/tc10_20260921 \\
         PYTHONDONTWRITEBYTECODE=1
  ~/venvs/naiad/bin/python scripts/tierc10_score_fixtures.py --out T.txt
"""
from __future__ import annotations

import argparse
import contextlib
import dataclasses
import functools
import io
import json
import math
import re
import shutil
import sys
import tempfile
import time
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import tierc10_score as SC                                          # noqa: E402

TP, LN, B, D, T9 = SC.TP, SC.LN, SC.B, SC.D, SC.T9
MS_4H = TP.MS_4H
TMP_ROOT: str | None = None
_TMP_NAMES: list = []           # every temp dir EVER made — a HALT can escape
#                                 its `with` and be printed after the rmtree


class Tripwire(Exception):
    """Raised by a stub standing in for a function this suite must never
    reach for real (score, finish_family, _mark_scored, register)."""


class _Stop(Exception):
    """Raised by a recorder standing in for a runner: the door-order leg
    stops the ride there, before a bar is replayed."""


@contextlib.contextmanager
def mutated(obj, name: str, value):
    old = getattr(obj, name)
    setattr(obj, name, value)
    try:
        yield
    finally:
        setattr(obj, name, old)


@contextlib.contextmanager
def tmpdir():
    d = tempfile.mkdtemp(prefix="tc10_score_fx_", dir=TMP_ROOT)
    _TMP_NAMES.append(d)
    try:
        yield Path(d)
    finally:
        shutil.rmtree(d, ignore_errors=True)


def clean(msg: str) -> str:
    """A message with every live temp path replaced by <tmp> — so no random
    name ever reaches the transcript [the F-D-3 lesson]."""
    s = str(msg)
    for d in _TMP_NAMES:
        for form in (str(Path(d).resolve()), str(d),
                     str(d).replace("/private/", "/", 1)):
            s = s.replace(form, "<tmp>")
    return s


def refused(fn) -> tuple:
    """(True, first line of the HALT) if `fn` HALTs; (False, '') if not."""
    try:
        fn()
    except SystemExit as e:
        return True, (clean(SC._halt_text(e)).splitlines() or ["?"])[0][:150]
    return False, ""


def T(sym, lane, entry_ms, net_r=0.25, **kw):
    """A synthetic campaign — synthetic numbers, never a registered arm's."""
    d = dict(symbol=sym, lane=lane, entry_ms=int(entry_ms),
             net_r=float(net_r), direction=1, entry_i=0, exit_i=0,
             gross_r=float(net_r) + 0.02, fee_r=0.015, funding_r=0.005,
             entry_px=100.0, exit_px=101.0, r_dist=2.0)
    d.update(kw)
    return SimpleNamespace(**d)


_CTX: dict = {}


def ctx() -> dict:
    if "c" not in _CTX:
        _CTX["c"] = SC.load_record()
    return _CTX["c"]


def arm_of(rid: str, k: int) -> dict:
    return ctx()["regs"][rid]["arms"][k]


# ═════════════════════════════════════════════════════════════ THE LEGS
def leg_record():
    """F-SC-RECORD — the record is read whole and held against its witness."""
    lines, ok = [], True
    c = SC.load_record()
    pin = json.loads(SC.REGISTRY_PIN_PATH.read_text("utf-8"))
    g = (c["order"] == pin["order_of_filing"] and c["registry_len"] == 6
         and c["registry_head"] == pin["registry_head"])
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] the registry of record: len "
                 f"{c['registry_len']}, head {c['registry_head'][:16]}…, "
                 f"order {c['order']} == REGISTRY_PIN.json")
    same = all(c["regs"][r]["arms"] == json.loads(
        (SC.REG_DIR / f"{r}.json").read_text("utf-8"))["book_spec"]["arms"]
        for r in c["order"])
    n_arms = sum(len(c["regs"][r]["arms"]) for r in c["order"])
    g = same and n_arms == 21
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] every arm is the FILED JSON's "
                 f"book_spec arm, byte for byte ({n_arms} arms over six "
                 f"filings)")
    with tmpdir() as td:
        # (i) a tampered filing
        rc = td / "reg_tampered"
        shutil.copytree(SC.REG_DIR, rc)
        j = json.loads((rc / "P-TRG-2.json").read_text("utf-8"))
        j["book_spec"]["arms"][0]["panel"] = \
            list(reversed(j["book_spec"]["arms"][0]["panel"]))
        (rc / "P-TRG-2.json").write_text(json.dumps(j, indent=2,
                                                    sort_keys=True))
        r1 = refused(lambda: SC.load_record(reg_dir=rc))
        # (ii) the pin's order swapped
        pp = td / "pin_swapped.json"
        p2 = dict(pin, order_of_filing=[pin["order_of_filing"][1],
                                        pin["order_of_filing"][0]]
                  + pin["order_of_filing"][2:])
        pp.write_text(json.dumps(p2))
        r2 = refused(lambda: SC.load_record(pin_path=pp))
        # (iii) a text of record amended by one character
        tt = td / "texts_amended.json"
        tx = json.loads(SC.REGISTRATION_TEXTS_PATH.read_text("utf-8"))
        tx["P-GEN-1"]["text"] = tx["P-GEN-1"]["text"].replace(
            "Prior 45%", "Prior 46%", 1)
        tt.write_text(json.dumps(tx))
        r3 = refused(lambda: SC.load_record(texts_path=tt))
        # (iv) a pin whose payload sha for one filing is not the filing's
        pq = td / "pin_sha.json"
        p3 = json.loads(json.dumps(pin))
        p3["registrations"]["P-SPR-2"]["sha256"] = "0" * 64
        pq.write_text(json.dumps(p3))
        r4 = refused(lambda: SC.load_record(pin_path=pq))
    for tag, (did, why) in (("a filing tampered after filing", r1),
                            ("the pin's order of filing swapped", r2),
                            ("P-GEN-1's text of record amended", r3),
                            ("a pin whose P-SPR-2 payload sha is wrong", r4)):
        ok &= did
        lines.append(f"[{'OK ' if did else 'BAD'}] REFUSED: {tag} — "
                     f"{why or 'ACCEPTED'}")
    return ok, lines


def _lenient_require_registered():
    real = TP.require_registered

    def lenient(reg_id, text, root=None, **kw):
        rec = json.loads((Path(root or TP.REG_DIR) / f"{reg_id}.json")
                         .read_text("utf-8"))
        return real(reg_id, rec["text"], root=root, **kw)
    return mutated(TP, "require_registered", lenient)


def leg_card():
    """F-SC-CARD — a run_cell_n arm's card and roles are REBUILT from the
    filed ride and round-trip it exactly."""
    lines, ok = [], True
    n = 0
    for rid in ("P-GEN-1", "P-TRG-2"):
        reg = ctx()["regs"][rid]
        for a in reg["arms"]:
            call = next((c for c in reg["arm_spec_calls"]
                         if f'"{a["arm"]}"' in c), "")
            card, roles = SC.card_roles_of_ride(a["ride"], call)
            g = json.dumps(TP.ride_spec(card, roles), sort_keys=True) \
                == json.dumps(a["ride"], sort_keys=True)
            if rid == "P-GEN-1":
                g &= (dataclasses.replace(card, name=TP.CONTROL_CARD.name)
                      == TP.CONTROL_CARD and roles == T9.V6_ROLES)
            else:
                g &= (card == TP.CONTROL_CARD
                      and roles in tuple(T9.SWEEP_CELLS)
                      and roles.name == "trigger-9/12")
            n += 1
            ok &= g
            lines.append(f"[{'OK ' if g else 'BAD'}] {rid} {a['arm']!r}: "
                         f"card {card.name!r} roles {roles.name!r} "
                         f"{roles.periods} round-trips the filed ride")
    base = arm_of("P-TRG-2", 0)["ride"]
    bad1 = dict(base, card_class="tierc8.Unknown")
    bad2 = json.loads(json.dumps(base))
    bad2["card_fields"]["bogus_knob"] = "1"
    bad3 = json.loads(json.dumps(base))
    bad3["roles_fields"]["trg_f"] = "nine("
    for tag, rd in (("an unknown card class", bad1),
                    ("a field the class does not have", bad2),
                    ("a value that is not a literal", bad3)):
        did, why = refused(lambda rd=rd: SC.card_roles_of_ride(rd))
        ok &= did
        lines.append(f"[{'OK ' if did else 'BAD'}] REFUSED: {tag} — "
                     f"{why or 'ACCEPTED'}")
    ok &= n == 7
    return ok, lines


def leg_lanes_card():
    """F-SC-LANES-CARD — an external arm's card is derived BY RULE from its
    filed lanes and name, and the P-BE-1 pin is held against the text."""
    lines, ok = [], True
    be = ctx()["regs"]["P-BE-1"]
    pins = [SC.be_pin_of_arm(a["arm"], be["text"]) for a in be["arms"]]
    cards = [SC.lanes_card(a, be["text"]) for a in be["arms"]]
    g = (pins == [1.0, 1.0, 1.0, 2.0] and cards[0] is LN.CARD_BE1
         and cards[1] is LN.CARD_BE1 and cards[2] is LN.CARD_BE1
         and cards[3].be_floor_after_r == 2.0
         and dataclasses.replace(cards[3], name=LN.CARD_BE1.name,
                                 be_floor_after_r=1.0) == LN.CARD_BE1)
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] P-BE-1 pins from the FILED arm "
                 f"names {pins}; A1-A3 ride CARD_BE1, A4 is CARD_BE1 with "
                 f"be_floor_after_r 2.0 and nothing else moved")
    sp = ctx()["regs"]["P-SPR-2"]
    cs = [SC.lanes_card(a, sp["text"]) for a in sp["arms"]]
    u = cs[3]
    g = (all(c is LN.CARD_SPR2 for c in cs[:3]) and u.lane == "union"
         and dataclasses.replace(u, name=LN.CARD_SPR2.name, lane="spring")
         == LN.CARD_SPR2)
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] P-SPR-2: arms 1-3 ride "
                 f"CARD_SPR2 (lane spring); arm 4 rides CARD_SPR2 on lane "
                 f"'union' and nothing else moved")
    kinds = {}
    for rid in ctx()["order"]:
        for a in ctx()["regs"][rid]["arms"]:
            kinds.setdefault(rid, set()).add(SC.door_kind(a))
    want = {"P-GEN-1": {"run_cell_n"}, "P-SPR-2": {"lanes"},
            "P-BE-1": {"lanes"}, "P-TRG-2": {"run_cell_n"},
            "P-BRK-I1": {"brk"}, "P-BRK-S1": {"brk"}}
    g = kinds == want
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] the door of every filed arm, "
                 f"from its filed runner + lanes: "
                 f"{ {k: sorted(v) for k, v in kinds.items()} }")
    roles = [SC.brk_role_of(a) for r in ("P-BRK-I1", "P-BRK-S1")
             for a in ctx()["regs"][r]["arms"]]
    g = len(set(roles)) == 6
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] every BRK arm maps to ONE "
                 f"tierc10_brk role by its filed name: {roles}")
    for tag, a in (
            ("a floor pin the text never quotes (be-floor-3R)",
             {"arm": "be-floor-3R vs card-v6 (CLASSIC5, full)",
              "lanes": ["card"]}),
            ("a card-lane arm naming no pin",
             {"arm": "floor vs card-v6", "lanes": ["card"]}),
            ("a lane set no lanes card rides",
             {"arm": "x", "lanes": ["card", "brk-s1"]})):
        did, why = refused(lambda a=a: SC.lanes_card(a, be["text"]))
        ok &= did
        lines.append(f"[{'OK ' if did else 'BAD'}] REFUSED: {tag} — "
                     f"{why or 'ACCEPTED'}")
    return ok, lines


def _no_text_pin(arm, text):
    m = SC.BE_PIN_RE.search(arm or "")
    if not m:
        raise SystemExit("HALT: no pin")
    return float(m.group(1))


def _trg_books(era_arm: int = 0, **over):
    a = arm_of("P-TRG-2", era_arm)
    L = 1_700_006_400_000 - 1_700_006_400_000 % MS_4H
    H = L + 400 * MS_4H - 1
    t0 = L + 10 * MS_4H
    tr = [T("BTCUSDT", "card", t0), T("ETHUSDT", "card", t0 + MS_4H),
          T("SOLUSDT", "card", t0 + 2 * MS_4H)]
    bt = [T("BTCUSDT", "card", t0), T("NEARUSDT", "card", t0 + 5 * MS_4H)]
    bs = {"ride": a["ride"], "panel": list(a["panel"]), "lo_ms": L,
          "hi_ms": H, "era": a["era"], "arm": a["arm"],
          "registration": "P-TRG-2"}
    bb = {"ride": TP.CONTROL_RIDE, "panel": list(TP.CLASSIC5), "lo_ms": L,
          "hi_ms": H, "era": "full", "arm": TP.CONTROL_ARM}
    bs.update(over.get("book_spec", {}))
    bb.update(over.get("base_spec", {}))
    return a, TP.Book(over.get("book", tr), spec=bs), \
        TP.Book(over.get("base", bt), spec=bb)


def leg_bind():
    """F-SC-BIND — the dry-run's binding is TP.score's pre-marker binding:
    it passes the filed book and refuses every book TP.score would refuse."""
    lines, ok = [], True
    rec = ctx()["regs"]["P-TRG-2"]["rec"]
    a, bk, ba = _trg_books()
    b = SC.bind_check(rec, a, bk, ba)
    g = b["ok"] and b["keys"] == {"n_paired": 1, "n_book_only": 2,
                                  "n_base_only": 1, "n_pair_score_law": 1,
                                  "moved": True}
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] a synthetic P-TRG-2 A1 book "
                 f"wearing the filed ride binds: {b['keys']}")
    L0 = bk.spec["lo_ms"]
    cut = TP.ERA_CUT_MS
    # TP.score's OWN premise arithmetic, not set arithmetic: a base holding a
    # key TWICE that the book holds once has MOVED under the scorer's law
    # (len(base) 2 > n_pair 1) though the key SETS are equal.
    tk = list(bk)[0]
    a_, bk_, ba_ = _trg_books(book=[tk], base=[
        T(tk.symbol, tk.lane, tk.entry_ms, 0.1),
        T(tk.symbol, tk.lane, tk.entry_ms, 0.2)])
    r = SC.bind_check(rec, a_, bk_, ba_)
    g = r["ok"] and r["keys"]["moved"] and r["keys"]["n_book_only"] == 0 \
        and r["keys"]["n_base_only"] == 0
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] the premise is TP.score's "
                 f"arithmetic (len(base) 2 > n_pair 1 -> moved) even where "
                 f"the key SETS are equal: {r['keys']}")
    cases = [
        ("identical campaign keys (two-sample premise)",
         dict(base=[T(t.symbol, t.lane, t.entry_ms, 0.5) for t in bk])),
        ("a campaign on a lane the arm never filed",
         dict(book=list(bk) + [T("ZECUSDT", "spring", L0 + 50 * MS_4H)])),
        ("a base ridden over a different window",
         dict(base_spec={"lo_ms": L0 + MS_4H})),
        ("a book whose provenance is the control's ride",
         dict(book_spec={"ride": TP.CONTROL_RIDE})),
        ("a non-finite net_r", dict(book=list(bk)[:2] + [
            T("SOLUSDT", "card", L0 + 12 * MS_4H, float("nan"))])),
        ("a symbol outside the declared panel",
         dict(book=list(bk) + [T("DOGEUSDT", "card", L0 + 60 * MS_4H)])),
    ]
    for tag, over in cases:
        a_, bk_, ba_ = _trg_books(**over)
        r = SC.bind_check(rec, a_, bk_, ba_)
        ok &= not r["ok"]
        lines.append(f"[{'OK ' if not r['ok'] else 'BAD'}] REFUSED: {tag} — "
                     f"{(r['halt'] or 'ACCEPTED').splitlines()[0][:130]}")
    # the era, on the filed HOLDOUT arm (A4): an entry before the cut
    a4, bk4, ba4 = _trg_books(3, book=[T("BTCUSDT", "card", cut - MS_4H),
                                       T("ETHUSDT", "card", cut + MS_4H)],
                              base=[T("NEARUSDT", "card", cut + 9 * MS_4H)],
                              book_spec={"lo_ms": cut + 1, "hi_ms": cut
                                         + 400 * MS_4H},
                              base_spec={"lo_ms": cut + 1, "hi_ms": cut
                                         + 400 * MS_4H})
    r = SC.bind_check(rec, a4, bk4, ba4)
    ok &= not r["ok"]
    lines.append(f"[{'OK ' if not r['ok'] else 'BAD'}] REFUSED: a holdout "
                 f"arm's book with an entry before the cut — "
                 f"{(r['halt'] or 'ACCEPTED')[:130]}")
    # a plain list where the arm is filed for run_cell_n
    r = SC.bind_check(rec, a, list(bk), ba)
    ok &= not r["ok"]
    lines.append(f"[{'OK ' if not r['ok'] else 'BAD'}] REFUSED: a plain list "
                 f"for a run_cell_n arm — {(r['halt'] or 'ACCEPTED')[:130]}")
    # an EXTERNAL arm offered a Book wearing ANOTHER arm's gate
    sp = ctx()["regs"]["P-SPR-2"]
    a1, a2 = sp["arms"][0], sp["arms"][1]
    xb = TP.Book([T("BTCUSDT", "spring", L0 + MS_4H)], spec={
        "runner": "external", "registration": "P-SPR-2", "arm": a2["arm"],
        "panel": list(a2["panel"]), "era": a2["era"],
        "registration_sha256": sp["rec"]["sha256"], "lo_ms": None,
        "hi_ms": None})
    r = SC.bind_check(sp["rec"], a1, xb, None)
    ok &= not r["ok"]
    lines.append(f"[{'OK ' if not r['ok'] else 'BAD'}] REFUSED: an external "
                 f"arm offered a Book wearing another arm's gate — "
                 f"{(r['halt'] or 'ACCEPTED')[:130]}")
    return ok, lines


def _neutered_bind_arm(rec, arm, panel, ruler, sif, book, base):
    return [a for a in rec["book_spec"]["arms"] if a["arm"] == arm][0]


def leg_door_first():
    """F-SC-DOOR-FIRST — every arm's door opens before one of its bars is
    read: the door call precedes corridor_era, every frame, every signal
    build and the runner."""
    lines, ok = [], True
    calls: list = []

    def rec_(name, fn, stop=False, ret=None, use_ret=False):
        def w(*a, **k):
            calls.append(name)
            if stop:
                raise _Stop(name)
            if use_ret:
                return ret
            return fn(*a, **k)
        return w
    saved = dict(SC._SPRINGS)
    SC._SPRINGS.clear()
    try:
        with contextlib.ExitStack() as es:
            es.enter_context(mutated(TP, "require_arm", rec_(
                "door:require_arm", TP.require_arm)))
            es.enter_context(mutated(TP, "require_registered", rec_(
                "door:require_registered", TP.require_registered)))
            es.enter_context(mutated(TP, "corridor_era", rec_(
                "bars:corridor_era", TP.corridor_era)))
            es.enter_context(mutated(T9, "frame", rec_(
                "bars:frame", T9.frame)))
            es.enter_context(mutated(LN, "spring_signals_from_census", rec_(
                "bars:spring_signals", None, use_ret=True, ret=[])))
            es.enter_context(mutated(TP, "run_cell_n", rec_(
                "runner:run_cell_n", None, stop=True)))
            es.enter_context(mutated(LN, "run_lane", rec_(
                "runner:run_lane", None, stop=True)))
            es.enter_context(mutated(B, "ready_run", rec_(
                "runner:ready_run", None, stop=True)))
            for rid, k in (("P-TRG-2", 0), ("P-GEN-1", 2), ("P-SPR-2", 1),
                           ("P-BE-1", 3), ("P-BRK-I1", 0), ("P-BRK-S1", 0)):
                calls.clear()
                reg = ctx()["regs"][rid]
                a = reg["arms"][k]
                try:
                    SC.ride_arm(reg, rid, a, {})
                    stopped = False
                except _Stop:
                    stopped = True
                door = [i for i, c in enumerate(calls)
                        if c.startswith("door:")]
                bars = [i for i, c in enumerate(calls)
                        if not c.startswith("door:")]
                g = (stopped and bool(door) and bool(bars)
                     and door[0] == 0 and door[0] < min(bars))
                ok &= g
                lines.append(f"[{'OK ' if g else 'BAD'}] {rid} "
                             f"{a['arm']!r}: {' > '.join(calls)}")
    finally:
        SC._SPRINGS.clear()
        SC._SPRINGS.update(saved)
    return ok, lines


def _corridor_before_door():
    real = SC.open_door

    def bad(reg, rid, arm):
        TP.corridor_era(tuple(arm["panel"]), arm["era"])
        return real(reg, rid, arm)
    return mutated(SC, "open_door", bad)


def leg_spring():
    """F-SC-SPRING — the spring list handed to replay10 is exactly the
    census's deviation-confirms whose harden bar lies in replay10's OWN
    window, and the refusals are counted consistently (real bars, P-SPR-2's
    tuning arm; entry-side facts only)."""
    lines, ok = [], True
    reg = ctx()["regs"]["P-SPR-2"]
    a2 = reg["arms"][1]
    SC.open_door(reg, "P-SPR-2", a2)                 # the door, first
    lo, hi, _m = TP.corridor_era(tuple(a2["panel"]), a2["era"])
    sym = "BTCUSDT"
    lst = SC.springs_for(sym, lo, hi, T9.V6_ROLES)
    f = T9.frame(sym)["f"]
    lo_i = max(int(np.searchsorted(f.open_ms, lo, "left")),
               T9.V6_ROLES.floor_bars)
    hi_i = int(np.searchsorted(f.open_ms, hi, "right")) - 1
    whole = SC._SPRINGS[sym]
    want = [s for s in whole if lo_i <= int(s.reclaim_i) <= hi_i]
    g = (SC.spring_window(sym, lo, hi, T9.V6_ROLES) == (lo_i, hi_i)
         and lst == want and len(lst) > 0 and len(whole) > len(lst))
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] {sym} tuning window "
                 f"[{lo_i}, {hi_i}] (independently re-derived): {len(lst)} "
                 f"of {len(whole)} whole-tape signals handed in")
    rep = LN.check_signals(f, lst, lo_i, hi_i)
    g = rep["n_signals"] == len(lst)
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] the list survives replay10's "
                 f"own check_signals: {rep}")
    out = next((s for s in whole if int(s.reclaim_i) > hi_i), None)
    did, why = refused(lambda: LN.check_signals(f, lst + [out], lo_i, hi_i))
    ok &= did and out is not None
    lines.append(f"[{'OK ' if did else 'BAD'}] REFUSED: one signal past the "
                 f"window handed in — {why[:110] or 'ACCEPTED'}")
    ride = SC.ride_arm(reg, "P-SPR-2", a2, {})
    sr = SC.spring_refusals(ride["book"], ride["springs"], ride["card"])
    g = (sr["consistent"] and sr["total"]["UNEXPLAINED"] == 0
         and sr["total"]["entered"] == len(ride["book"]))
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] the real tuning-arm ride: "
                 f"{sr['total']} consistent={sr['consistent']}")
    short = list(ride["book"])[1:]
    sr2 = SC.spring_refusals(short, ride["springs"], ride["card"])
    ok &= not sr2["consistent"]
    lines.append(f"[{'OK ' if not sr2['consistent'] else 'BAD'}] REFUSED: a "
                 f"book with one campaign dropped reads inconsistent "
                 f"(UNEXPLAINED {sr2['total'].get('UNEXPLAINED')})")
    return ok, lines


def _unfiltered_springs():
    real = SC.springs_for

    def bad(sym, lo, hi, roles):
        real(sym, lo, hi, roles)
        return list(SC._SPRINGS[sym])
    return mutated(SC, "springs_for", bad)


def _floorless_window():
    real = SC.spring_window

    def bad(sym, lo, hi, roles):
        return (T9.frame(sym)["f"].open_ms.searchsorted(lo, "left"),
                real(sym, lo, hi, roles)[1])
    return mutated(SC, "spring_window", bad)


SEAL_R = 7.123457


def _fake_ride(reg, rid, arm, cache):
    """A stub ride: three synthetic campaigns per arm, all with the
    distinctive net_r SEAL_R, so any sum or mean that leaks is findable."""
    lo, hi = TP.ERA_CUT_MS - 200 * MS_4H, TP.ERA_CUT_MS + 200 * MS_4H
    t0 = (TP.ERA_CUT_MS + 1) if arm["era"] == "holdout" \
        else TP.ERA_CUT_MS - 100 * MS_4H
    lane = arm["lanes"][0]
    pnl = list(arm["panel"])
    tr = [T(pnl[i % len(pnl)], lane, t0 + i * MS_4H, SEAL_R)
          for i in range(3)]
    book = TP.Book(tr, spec={"runner": "stub", "registration": rid,
                             "arm": arm["arm"], "era": arm["era"],
                             "lo_ms": lo, "hi_ms": hi})
    base = None
    if arm["base"] == "card-v6":
        base = TP.Book([T(pnl[0], "card", t0 + 7 * MS_4H, SEAL_R)],
                       spec={"ride": TP.CONTROL_RIDE, "panel": pnl,
                             "lo_ms": lo, "hi_ms": hi})
    return {"door": "stub", "gate": {}, "card": None, "run": None,
            "springs": None, "base": base, "book": book,
            "window": (lo, hi), "era_meta": {}}


def _trip(name):
    def w(*a, **k):
        _TRIPS.append(name)
        raise Tripwire(name)
    return w


_TRIPS: list = []


@contextlib.contextmanager
def stubbed_dry_run():
    with contextlib.ExitStack() as es:
        es.enter_context(mutated(SC, "ride_arm", _fake_ride))
        es.enter_context(mutated(SC, "be1_census", lambda book: {
            "decision": "NOT RUN", "governed_by": "P-BE-1 §9",
            "reason": "stub", "census_sha_rederived": "0" * 64,
            "census_sha_filed": "0" * 64, "byte_identical_to_filed": True}))
        for n in ("score", "finish_family", "_mark_scored", "register"):
            es.enter_context(mutated(TP, n, _trip(f"TP.{n}")))
        yield


def _dry_text() -> tuple:
    P = SC.Printer(echo=False)
    res = SC.dry_run(ctx(), None, P)
    return P.text(), res


def leg_noscore():
    """F-SC-NOSCORE — the dry-run path never reaches TP.score, finish_family,
    _mark_scored or register, writes no .scored.json and prints no outcome:
    no outcome token, and not one campaign's net_r nor any sum of them."""
    lines, ok = [], True
    _TRIPS.clear()
    before = SC.scored_json_on_file()
    with stubbed_dry_run():
        txt, res = _dry_text()
    after = SC.scored_json_on_file()
    g = not _TRIPS and before == after == []
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] tripwires on TP.score / "
                 f"finish_family / _mark_scored / register: {len(_TRIPS)} "
                 f"hit; .scored.json before {before} / after {after}")
    toks = [t for t in SC.OUTCOME_TOKENS if t in txt]
    nums = [x for x in (f"{SEAL_R}", f"{SEAL_R:.4f}", f"{SEAL_R:.2f}",
                        f"{3 * SEAL_R:.6f}", f"{3 * SEAL_R:.4f}",
                        f"{3 * SEAL_R:.2f}", f"{2 * SEAL_R:.4f}")
            if x in txt]
    g = not toks and not nums and len(res["arms"]) == 21
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] the stubbed dry-run of all 21 "
                 f"arms prints no outcome token ({toks or 'none'}) and no "
                 f"campaign net_r or sum of them ({nums or 'none'})")
    return ok, lines


def _bind_calls_score():
    real = SC.bind_check

    def bad(rec, arm, book, base):
        TP.score(rec["registration"], "x", book, arm["panel"])
        return real(rec, arm, book, base)
    return mutated(SC, "bind_check", bad)


def _counts_leak_sums():
    def bad(book, panel):
        return {s: round(sum(float(t.net_r) for t in book
                             if t.symbol == s), 6) for s in panel}
    return mutated(SC, "per_asset_counts", bad)


def leg_det():
    """F-SC-DET — two dry-runs print the same bytes (no clock, no temp name,
    no unordered set)."""
    with stubbed_dry_run():
        a, _ = _dry_text()
        b, _ = _dry_text()
    g = a == b
    return g, [f"[{'OK ' if g else 'BAD'}] two stubbed dry-runs: sha "
               f"{SC.sha256_bytes(a.encode())[:16]} / "
               f"{SC.sha256_bytes(b.encode())[:16]}"]


def _clock_in_header():
    return mutated(B, "as_of_of_record",
                   lambda *a, **k: str(time.perf_counter_ns()))


def leg_gen1():
    """F-SC-GEN1 — P-GEN-1 §5's arm-3 assertion: equal books HOLD; one
    campaign missing, or one campaign's content changed, reads BROKEN."""
    lines, ok = [], True
    arms = ctx()["regs"]["P-GEN-1"]["arms"]
    a1, a3 = arms[0]["arm"], arms[2]["arm"]
    t0 = 1_690_000_000_000
    b1 = [T("PUMPUSDT", "card", t0), T("LTCUSDT", "card", t0 + MS_4H),
          T("SUIUSDT", "card", t0 + 2 * MS_4H, 0.75),
          T("MNTUSDT_BYBIT", "card", t0 + 3 * MS_4H)]
    same = [T("PUMPUSDT", "card", t0), T("SUIUSDT", "card", t0 + 2 * MS_4H,
                                         0.75),
            T("MNTUSDT_BYBIT", "card", t0 + 3 * MS_4H)]
    g1 = SC.gen1_subset({a1: b1, a3: same}, arms)
    ok &= g1["checked"] and not g1["broken"]
    lines.append(f"[{'OK ' if g1['checked'] and not g1['broken'] else 'BAD'}"
                 f"] arm 3 == the three-symbol subset of arm 1: HOLDS "
                 f"(n {g1['n_subset_of_arm1']}/{g1['n_arm3']})")
    g2 = SC.gen1_subset({a1: b1, a3: same[:2]}, arms)
    ok &= g2["broken"]
    lines.append(f"[{'OK ' if g2['broken'] else 'BAD'}] REFUSED: arm 3 "
                 f"missing a campaign reads BROKEN (only in arm 1 "
                 f"{g2['keys_only_in_arm1']})")
    moved = [T("PUMPUSDT", "card", t0), T("SUIUSDT", "card",
                                          t0 + 2 * MS_4H, 0.76),
             T("MNTUSDT_BYBIT", "card", t0 + 3 * MS_4H)]
    g3 = SC.gen1_subset({a1: b1, a3: moved}, arms)
    ok &= g3["broken"]
    lines.append(f"[{'OK ' if g3['broken'] else 'BAD'}] REFUSED: arm 3 with "
                 f"one campaign's content changed reads BROKEN (keys equal "
                 f"{g3['keys_equal']}, shas equal {g3['book_sha_equal']}/"
                 f"{g3['content_sha_equal']})")
    return ok, lines


@contextlib.contextmanager
def _blind_shas():
    with mutated(TP, "_book_sha", lambda b: "0" * 64), \
            mutated(B, "book_content_sha", lambda b: "0" * 64):
        yield


# the contract clause's tiers, TYPED HERE, held against tierc10_data's parse
FIXTURE_SLIP = {"A": 2.0, "B": 5.0, "C": 10.0}


def leg_twin():
    """F-SC-TWIN — the haircut twin beside the row is tierc10_data's filed
    law, re-computed by hand from the contract's own tiers; the TC-series
    net_r is untouched; the stem map equals haircut_twin_for_stem."""
    lines, ok = [], True
    g = {t: float(b["bps"]) for t, b in D.SLIPPAGE_TIERS.items()} \
        == FIXTURE_SLIP
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] tierc10_data's parsed tiers == "
                 f"the fixture's typed contract tiers {FIXTURE_SLIP}")
    bk = [T("BTCUSDT", "card", 1, 0.40, gross_r=0.5, entry_px=100.0,
            exit_px=104.0, r_dist=2.0, funding_r=0.03),
          T("SUIUSDT", "card", 2, -0.30, gross_r=-0.2, entry_px=3.0,
            exit_px=2.9, r_dist=0.1, funding_r=-0.01),
          T("1000PEPEUSDT", "card", 3, 0.10, gross_r=0.2, entry_px=0.01,
            exit_px=0.011, r_dist=0.001, funding_r=0.0)]
    tier = {"BTCUSDT": "A", "SUIUSDT": "B", "1000PEPEUSDT": "C"}
    hand = []
    for t in bk:
        side = 5.0 + FIXTURE_SLIP[tier[t.symbol]]
        hand.append(t.gross_r - (side / 1e4) * (t.entry_px + t.exit_px)
                    / t.r_dist)
    tw = SC.haircut_twin_block(bk)
    g = (math.isclose(tw["twin_expectancy_r"], float(np.mean(hand)),
                      rel_tol=0, abs_tol=1e-12)
         and math.isclose(tw["tc_expectancy_r"],
                          float(np.mean([t.net_r for t in bk])),
                          rel_tol=0, abs_tol=1e-12)
         and math.isclose(tw["twin_with_funding_companion_expectancy_r"],
                          float(np.mean([h - t.funding_r for h, t
                                         in zip(hand, bk)])),
                          rel_tol=0, abs_tol=1e-12))
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] synthetic twin == the hand's "
                 f"(fee 5 bps/side + tier slippage, on (entry + exit) / "
                 f"r_dist, NO funding) and the TC-series column is the "
                 f"book's own net_r; the funding companion subtracts "
                 f"funding_r")
    by = {v["stem"]: v["asset"] for v in D.load_manifest()["venues"]
          if v["stem"]}
    bad = [s for s in TP.PANEL17
           if D.haircut_twin_for_stem(s, 0.5, 100.0, 101.0, 2.0)
           != D.haircut_twin_net_r(by[s], 0.5, 100.0, 101.0, 2.0)]
    g = not bad
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] the driver's stem->asset map "
                 f"== tierc10_data.haircut_twin_for_stem on all 17 stems "
                 f"({bad or 'no disagreement'})")
    base = [T("BTCUSDT", "card", 1, 0.2, gross_r=0.25, entry_px=100.0,
              exit_px=101.0, r_dist=2.0, funding_r=0.0)]
    tw2 = SC.haircut_twin_block(bk, base)
    g = "twin_difference_r" in tw2 and isinstance(
        tw2["sign_disagrees_with_tc"], bool)
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] a twin-ruled row carries the "
                 f"twin DIFFERENCE and a sign flag")
    return ok, lines


def _rows_file(rid, scored=True, canonical=True, halt=False, extra=()):
    rows = []
    if halt:
        rows.append({"arm": "A1", "halt": "HALT: stub", "at": "TP.score",
                     "scored_in_family": True, "text_prescribes": []})
    elif scored:
        rows.append({"arm": "A1", "scored_in_family": True, "beside": {},
                     "score_row": {
                         "registration": rid, "arm": "A1",
                         "scored_in_family": True,
                         "registration_root_is_canonical": canonical,
                         "verdict": "X", "p_one_sided": None,
                         "loao_clears_line_of_record": None}})
    rows += list(extra)
    return {"registration": rid, "rows": rows}


def leg_finish():
    """F-SC-FINISH — TP.finish_family is reached only when all six carry one
    canonical scored row, or a scored-arm HALT the operator NAMES."""
    lines, ok = [], True
    calls: list = []

    def fake_ff(rows, family_m=6, canonical_only=True):
        calls.append(len(rows))
        return pd.DataFrame(rows).assign(clears_bh_bar=None,
                                         fdr_bar_q_over_m=0.1 / 6)
    order = ctx()["order"]
    with mutated(TP, "finish_family", fake_ff), tmpdir() as td:
        def put(rid, doc):
            (td / f"{rid}{SC.ROWS_SUFFIX}").write_bytes(SC.rows_bytes(doc))

        def run(allow=()):
            P = SC.Printer(echo=False)
            return refused(lambda: SC.finish(ctx(), P, scores_dir=td,
                                             allow_halted=allow))
        for rid in order:
            put(rid, _rows_file(rid))
        did, why = run()
        g = not did and calls == [6] and (td / SC.FAMILY_NAME).exists()
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] six canonical scored rows: "
                     f"finish_family (stub) called once with {calls}")
        cases = []
        (td / SC.FAMILY_NAME).unlink()
        (td / f"P-TRG-2{SC.ROWS_SUFFIX}").unlink()
        cases.append(("five rows files", run()))
        put("P-TRG-2", _rows_file("P-TRG-2", canonical=False))
        cases.append(("a scored row from a throwaway registry", run()))
        put("P-TRG-2", _rows_file("P-TRG-2", extra=[
            {"arm": "A2", "scored_in_family": True,
             "score_row": {"registration": "P-TRG-2", "arm": "A2",
                           "scored_in_family": True,
                           "registration_root_is_canonical": True}}]))
        cases.append(("two scored rows in one registration", run()))
        put("P-TRG-2", _rows_file("P-TRG-2"))
        put("P-BE-1", _rows_file("P-BE-1", halt=True))
        cases.append(("a scored-arm HALT the operator did not name", run()))
        cases.append(("--allow-halted-slot naming no filed id",
                      run(("P-XYZ-9",))))
        n0 = len(calls)
        for tag, (did, why) in cases:
            ok &= did
            lines.append(f"[{'OK ' if did else 'BAD'}] REFUSED: {tag} — "
                         f"{why[:120] or 'ACCEPTED'}")
        g = len(calls) == n0 == 1
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] finish_family was reached "
                     f"by none of the refused families")
        did, why = run(("P-BE-1",))
        fam = json.loads((td / SC.FAMILY_NAME).read_text("utf-8")) \
            if (td / SC.FAMILY_NAME).exists() else {}
        g = (not did and calls[-1] == 5
             and fam.get("scored_slots_halted") == {"P-BE-1": "HALT: stub"})
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] the operator NAMES P-BE-1's "
                     f"recorded HALT: finish_family runs on {calls[-1]} "
                     f"scored rows at the declared m, and FAMILY.json names "
                     f"the halted slot")
    return ok, lines


def _lenient_gate():
    def bad(order, scores_dir, allow_halted=()):
        rows, srcs = [], {}
        for rid in order:
            p = scores_dir / f"{rid}{SC.ROWS_SUFFIX}"
            if p.exists():
                doc = json.loads(p.read_text("utf-8"))
                rows += [r["score_row"] for r in doc["rows"]
                         if "score_row" in r]
                srcs[rid] = "x"
        return rows, srcs, {}
    return mutated(SC, "finish_gate", bad)


def _fake_score_factory(counter: list, p_value: float = 0.5,
                        halt_scored: str | None = None):
    def fake(rid, text, book, panel, base=None, ruler="vs_zero", seed=0,
             arm=None, scored_in_family=True, note="", root=None,
             n_boot=0, head_of_record=None, era=None):
        counter.append(arm)
        if halt_scored and scored_in_family:
            raise SystemExit(halt_scored)
        return {"registration": rid, "arm": arm, "n": len(book),
                "expectancy_r": 0.0, "ci_lo": -1.0, "ci_hi": 1.0,
                "p_one_sided": p_value, "verdict": "NOT SUPPORTED",
                "loao_line": "0/5 above", "loao_line_of_record": "lineage",
                "loao_above_of_record": 0, "loao_panels": len(panel),
                "loao_bar_above_half": 3,
                "loao_clears_line_of_record": False,
                "ear_expectancy_r": 0.0, "ear_ci_lo": -1.0,
                "ear_ci_hi": 1.0, "scored_in_family": scored_in_family,
                "registration_root_is_canonical": True}
    return fake


PREMISE_HALT = ("HALT: P-BE-1 — the arm shares the WHOLE campaign set with "
                "its base; the commissioned two-sample ruler's premise "
                "failed. File a NEW id under ruler='set_change' and "
                "disclose.")


def leg_rows():
    """F-SC-ROWS — --score files reproducible rows, never overwrites a
    differing rows file, scores no Book the reviewed dry-run did not name,
    and stops at a scored-arm HALT unless the operator says continue."""
    lines, ok = [], True
    cnt: list = []
    with contextlib.ExitStack() as es:
        es.enter_context(mutated(SC, "ride_arm", _fake_ride))
        es.enter_context(mutated(SC, "per_asset_rows",
                                 lambda book, rid, arm: []))
        es.enter_context(mutated(TP, "score", _fake_score_factory(cnt)))
        td = es.enter_context(tmpdir())
        P = SC.Printer(echo=False)
        rc1 = SC.score_registration(ctx(), "P-TRG-2", None, P, scores_dir=td)
        p = td / f"P-TRG-2{SC.ROWS_SUFFIX}"
        s1 = SC.sha256_file(p)
        rc2 = SC.score_registration(ctx(), "P-TRG-2", None, P, scores_dir=td)
        s2 = SC.sha256_file(p)
        g = rc1 == rc2 == 0 and s1 == s2 and len(cnt) == 8
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] a re-score reproduces the "
                     f"rows file byte for byte ({s1[:16]} / {s2[:16]}; "
                     f"{len(cnt)} stub score calls over 2 x 4 arms)")
        with mutated(TP, "score", _fake_score_factory(cnt, 0.4)):
            did, why = refused(lambda: SC.score_registration(
                ctx(), "P-TRG-2", None, P, scores_dir=td))
        g = did and SC.sha256_file(p) == s1
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] REFUSED: a re-score whose "
                     f"bytes differ never overwrites the filed rows — "
                     f"{why[:100] or 'ACCEPTED'}")
        n0 = len(cnt)
        exp = {("P-TRG-2", a["arm"]): ("f" * 64, None)
               for a in ctx()["regs"]["P-TRG-2"]["arms"]}
        did, why = refused(lambda: SC.score_registration(
            ctx(), "P-TRG-2", exp, P, scores_dir=td / "x"))
        g = did and len(cnt) == n0
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] REFUSED: a Book whose sha "
                     f"is not the reviewed dry-run's, BEFORE TP.score "
                     f"({len(cnt) - n0} score calls) — {why[:90]}")
    for cont, want_calls, want_rows in ((False, 1, 1), (True, 4, 4)):
        c2: list = []
        with contextlib.ExitStack() as es:
            es.enter_context(mutated(SC, "ride_arm", _fake_ride))
            es.enter_context(mutated(SC, "per_asset_rows",
                                     lambda book, rid, arm: []))
            es.enter_context(mutated(SC, "be1_census", lambda book: {
                "decision": "NOT RUN", "governed_by": "P-BE-1 §9"}))
            es.enter_context(mutated(TP, "score", _fake_score_factory(
                c2, halt_scored=PREMISE_HALT)))
            td = es.enter_context(tmpdir())
            P = SC.Printer(echo=False)
            rc = SC.score_registration(ctx(), "P-BE-1", None, P,
                                       scores_dir=td,
                                       continue_after_scored_halt=cont) \
                if cont else SC.score_registration(ctx(), "P-BE-1", None, P,
                                                   scores_dir=td)
            doc = json.loads((td / f"P-BE-1{SC.ROWS_SUFFIX}")
                             .read_text("utf-8"))
        h = doc["rows"][0]
        g = (rc == 2 and len(c2) == want_calls
             and len(doc["rows"]) == want_rows
             and h.get("halt") == PREMISE_HALT
             and len(h.get("text_prescribes") or []) == 2
             and (h.get("beside") or {}).get("f_c10_be", {})
             .get("decision") == "NOT RUN")
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] P-BE-1's scored arm HALTs "
                     f"(the text's prescribed premise HALT, recorded with "
                     f"its 2 quotes and F-C10-BE's status beside it): "
                     f"continue={cont} -> {len(c2)} score call(s), "
                     f"{len(doc['rows'])} row entr(ies), rc {rc}")
    return ok, lines


def _nondeterministic_rows():
    real = SC.rows_bytes

    def bad(doc):
        return real(dict(doc, _ns=time.perf_counter_ns()))
    return mutated(SC, "rows_bytes", bad)


def _continue_by_default():
    real = SC.score_registration
    return mutated(SC, "score_registration",
                   functools.partial(real, continue_after_scored_halt=True))


def leg_prescribed():
    """F-SC-PRESCRIBED — a sentence printed as what the filed text prescribes
    is IN the text of record, verbatim (whitespace-normalised)."""
    lines, ok = [], True
    t = ctx()["regs"]["P-BE-1"]["text"]
    q = SC.prescribed("P-BE-1", PREMISE_HALT, t)
    g = len(q) == 2 and all(SC._norm(x) in SC._norm(t) for x in q)
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] P-BE-1's premise HALT carries "
                 f"{len(q)} quotes of its own text (§4, §11)")
    g = SC.prescribed("P-TRG-2", PREMISE_HALT,
                      ctx()["regs"]["P-TRG-2"]["text"]) == []
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] another registration's HALT is "
                 f"given no borrowed prescription")
    amended = t.replace("it\nHALTs. That HALT", "it\nhalts. That HALT")
    did, why = refused(lambda: SC.prescribed("P-BE-1", PREMISE_HALT,
                                             amended))
    ok &= did and amended != t
    lines.append(f"[{'OK ' if did else 'BAD'}] REFUSED: a quote the text no "
                 f"longer carries — {why[:100] or 'ACCEPTED'}")
    return ok, lines


def leg_trg2():
    """F-SC-TRG2 — P-TRG-2 §2: the filed ride differs from CONTROL_RIDE in
    EXACTLY the two trigger fields, on all four arms."""
    lines, ok = [], True
    for a in ctx()["regs"]["P-TRG-2"]["arms"]:
        d = SC.trg2_ride_diff(a)
        g = d["exactly_two_trigger_fields"] and d["sweep_cell"] == \
            ["trigger-9/12"]
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] {a['arm']!r}: {d['diff']}")
    a = json.loads(json.dumps(arm_of("P-TRG-2", 0)))
    a["ride"]["roles_fields"]["win_f"] = "9"
    d = SC.trg2_ride_diff(a)
    ok &= not d["exactly_two_trigger_fields"]
    lines.append(f"[{'OK ' if not d['exactly_two_trigger_fields'] else 'BAD'}"
                 f"] REFUSED: a third moved field (win_f) — {d['diff']}")
    return ok, lines


def _synthetic_trade(sym, k, net_r, direction=1):
    """A FULLY SYNTHETIC tierc7_rules.Trade — every number invented, so the
    score-mode beside-columns can be exercised without reading one outcome
    of a registered arm."""
    RCm = LN.RC
    t0 = 1_690_000_000_000 + k * MS_4H * 30
    return RCm.Trade(
        symbol=sym, lane="card", direction=direction, arm_i=k, arm_ms=t0,
        entry_i=k + 1, entry_ms=t0 + MS_4H, entry_px=100.0, stop_px=98.0,
        r_dist=2.0, anchor=98.5, anchor_bar_ms=t0, anchor_was_sealed=False,
        atr_at_entry=1.5, disp_at_arming=0.5, exit_i=k + 9,
        exit_ms=t0 + 9 * MS_4H, exit_px=100.0 + 2.0 * net_r,
        exit_reason="stop" if net_r < 0 else "trail", bars_held=8,
        scored=True, advances=[], adds=[], mfe_r=abs(net_r) + 0.5,
        gross_r=net_r + 0.02, fee_r=0.015, funding_r=0.005, net_r=net_r)


def leg_beside():
    """F-SC-BESIDE — the score-mode beside-columns on a synthetic book: the
    per-asset rows name EVERY DECLARED asset (n = 0 included, which is why
    TP.headline_n exists), and the twin rides every row."""
    lines, ok = [], True
    arm = arm_of("P-GEN-1", 0)
    vals = [0.9, -1.0, 0.4, 1.3, -0.6, 0.2]
    bk = [_synthetic_trade(s_, k, v, 1 if k % 2 else -1) for k, (s_, v) in
          enumerate(zip(["ENAUSDT", "LTCUSDT", "XMRUSDT", "BNBUSDT",
                         "LTCUSDT", "ENAUSDT"], vals))]
    rows = SC.per_asset_rows(bk, "P-GEN-1", arm)
    assets = sorted({r["key"] for r in rows if r["group"] == "asset"})
    zero = sorted(r["key"] for r in rows if r["group"] == "asset"
                  and r["aggregation"] == "raw_panel" and r["n"] == 0)
    g = (assets == sorted(arm["panel"]) and len(zero) == 8
         and {r["group"] for r in rows} == {"asset", "direction"})
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] per-asset rows name all "
                 f"{len(assets)} declared assets, {len(zero)} of them at "
                 f"n = 0 {zero}")
    tw = SC.haircut_twin_block(bk)
    g = tw["n"] == len(bk) and set(tw["twin_per_asset_expectancy_r"]) == {
        "ENAUSDT", "LTCUSDT", "XMRUSDT", "BNBUSDT"}
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] the twin rides the same book "
                 f"(n {tw['n']}, per asset {sorted(tw['twin_per_asset_expectancy_r'])})")
    b = SC.rows_bytes({"rows": rows, "twin": tw})
    ok &= bool(b)
    return ok, lines


def _headline_present_assets_only():
    real = TP.headline_n
    return mutated(TP, "headline_n", lambda book, label, panel, seed=TP.SEED:
                   real(book, label, tuple(sorted({t.symbol for t in book})),
                        seed))


def leg_json():
    """F-SC-JSON — the rows bytes are strict, deterministic JSON: numpy to
    python, non-finite floats to null, sorted keys."""
    doc = {"b": np.float64(float("nan")), "a": np.int64(3),
           "c": [np.bool_(True), float("inf"), (1, 2)],
           "d": pd.DataFrame([{"x": 1.5}])}
    b1 = SC.rows_bytes(doc)
    b2 = SC.rows_bytes(dict(reversed(list(doc.items()))))
    back = json.loads(b1)
    g = (b1 == b2 and back == {"a": 3, "b": None, "c": [True, None, [1, 2]],
                               "d": [{"x": 1.5}]})
    return g, [f"[{'OK ' if g else 'BAD'}] {b1.decode().strip()[:100]}"]


LEGS = [
    ("F-SC-RECORD",
     "load_record accepts a registry, pin or text that is not the record of "
     "record, or an arm that is not the filed JSON's",
     leg_record,
     [("the door accepts any text (require_registered neutered)",
       _lenient_require_registered),
      ("the pin's order/length/head are not compared",
       lambda: mutated(SC, "pin_disagreements", lambda lines, pin: [])),
      ("a filing is not held against its pin",
       lambda: mutated(SC, "filing_disagreements", lambda r, w, p: []))]),
    ("F-SC-CARD",
     "a run_cell_n arm's rebuilt card/roles do not round-trip the filed "
     "ride, or an unbuildable ride is accepted",
     leg_card,
     [("field values are not parsed (strings ride)",
       lambda: mutated(SC, "_parse_field", str)),
      ("-inf is parsed as 0.0",
       lambda: mutated(SC, "_parse_field",
                       lambda v, _r=SC._parse_field:
                       0.0 if v == "-inf" else _r(v)))]),
    ("F-SC-LANES-CARD",
     "an external arm's card is not derived by rule from its filed lanes and "
     "name, or P-BE-1's pin is not held against the filed text",
     leg_lanes_card,
     [("the pin is taken from the name without the text's quote",
       lambda: mutated(SC, "be_pin_of_arm", _no_text_pin))]),
    ("F-SC-BIND",
     "the dry-run binding accepts a book TP.score's pre-marker checks would "
     "refuse, or refuses the filed book",
     leg_bind,
     [("TP._bind_arm neutered", lambda: mutated(TP, "_bind_arm",
                                                _neutered_bind_arm)),
      ("the two-sample premise is not measured",
       lambda: mutated(SC, "key_sets", lambda b, a: {
           "n_paired": 0, "n_book_only": 1, "n_base_only": 1,
           "n_pair_score_law": 0, "moved": True})),
      ("the era is not held against the campaigns",
       lambda: mutated(TP, "in_era", lambda ms, era: True)),
      ("the premise decided by key SETS, not the scorer's arithmetic",
       lambda: mutated(SC, "key_sets", lambda b, a, _r=SC.key_sets: dict(
           _r(b, a), moved=bool(_r(b, a)["n_book_only"]
                                or _r(b, a)["n_base_only"]))))]),
    ("F-SC-DOOR-FIRST",
     "any bar is read (corridor_era, a frame, a signal, the runner) before "
     "the arm's door has opened",
     leg_door_first,
     [("the corridor is cut BEFORE the door", _corridor_before_door)]),
    ("F-SC-SPRING",
     "the spring list handed in is not exactly replay10's window, or the "
     "refusal count is inconsistent with the Book",
     leg_spring,
     [("the whole-tape list is handed in unfiltered", _unfiltered_springs),
      ("the window drops the warm-up floor", _floorless_window)]),
    ("F-SC-NOSCORE",
     "the dry-run reaches TP.score / finish_family / _mark_scored / "
     "register, writes a .scored.json, or prints an outcome",
     leg_noscore,
     [("the binding step calls TP.score", _bind_calls_score),
      ("the per-asset line prints each asset's net_r sum",
       _counts_leak_sums)]),
    ("F-SC-DET",
     "two dry-runs differ by one byte",
     leg_det,
     [("a clock in the header", _clock_in_header)]),
    ("F-SC-GEN1",
     "P-GEN-1 §5's arm-3 assertion misses a missing or changed campaign",
     leg_gen1,
     [("both shas blinded (keys alone decide)", _blind_shas)]),
    ("F-SC-TWIN",
     "the haircut twin beside a row is not tierc10_data's filed law, or it "
     "touches the TC-series net_r",
     leg_twin,
     [("the charter slippage is dropped",
       lambda: mutated(D, "slippage_bps_side", lambda asset: 0.0))]),
    ("F-SC-FINISH",
     "finish_family is reached without all six scored rows (or an "
     "operator-named scored-arm HALT), or a whole family is refused",
     leg_finish,
     [("the gate admits whatever rows files exist", _lenient_gate)]),
    ("F-SC-ROWS",
     "--score overwrites a differing rows file, scores a Book the reviewed "
     "dry-run did not name, or scores Tier-E arms behind a scored-arm HALT "
     "by default",
     leg_rows,
     [("the rows bytes carry a clock", _nondeterministic_rows),
      ("the --expect check is skipped",
       lambda: mutated(SC, "expect_check", lambda *a: None)),
      ("Tier-E arms are scored behind a scored-arm HALT by default",
       _continue_by_default)]),
    ("F-SC-PRESCRIBED",
     "a sentence printed as the filed text's prescription is not in the "
     "text of record",
     leg_prescribed,
     [("the quote check compares nothing",
       lambda: mutated(SC, "_norm", lambda s: ""))]),
    ("F-SC-TRG2",
     "P-TRG-2's filed ride is not exactly the two trigger fields off "
     "CONTROL_RIDE, or a third moved field passes",
     leg_trg2,
     [("the diff sees trigger fields only",
       lambda: mutated(TP, "_spec_diff",
                       lambda f, o, _r=TP._spec_diff:
                       [d for d in _r(f, o) if "trg_" in d]))]),
    ("F-SC-BESIDE",
     "the per-asset rows beside a scored row drop a declared asset with no "
     "campaign, or the twin does not ride the same book",
     leg_beside,
     [("the headline lists the assets PRESENT, not the declared panel",
       _headline_present_assets_only)]),
    ("F-SC-JSON",
     "the rows bytes are not strict, deterministic JSON",
     leg_json,
     [("no conversion (NaN and numpy ride raw)",
       lambda: mutated(SC, "_jsonable", lambda v: v))]),
]


def flat(s: str) -> str:
    """One transcript line per check: a multi-line HALT is joined with ' / '."""
    return " / ".join(x.strip() for x in str(s).splitlines() if x.strip())


def run_leg(fn) -> tuple:
    try:
        ok, lines = fn()
        return bool(ok), [flat(clean(x)) for x in lines]
    except SystemExit as e:
        return False, [f"[BAD] HALT: {flat(clean(SC._halt_text(e)))[:200]}"]
    except Tripwire as e:
        return False, [f"[BAD] TRIPWIRE: {e}"]
    except Exception as e:                                  # noqa: BLE001
        return False, [f"[BAD] {type(e).__name__}: {flat(clean(e))[:200]}"]


def main(argv=None) -> int:
    global TMP_ROOT
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=None)
    ap.add_argument("--tmp", default=None)
    ap.add_argument("--only", nargs="+", default=None)
    a = ap.parse_args(argv)
    TMP_ROOT = a.tmp
    TP.substrate()
    buf = io.StringIO()

    def P(s=""):
        buf.write(s + "\n")
        print(s, flush=True)
    P("TIER-C10 · STAGE B · FIXTURES — scripts/tierc10_score.py")
    P("the real TP.score / finish_family / _mark_scored / register are never "
      "called; no .scored.json; nothing written under research_outputs/")
    n_pass = n_legs = n_red = n_breaks = 0
    failed = []
    for name, fails_if, fn, breaks in LEGS:
        if a.only and name not in a.only:
            continue
        n_legs += 1
        P("")
        P(f"── {name}")
        P(f"   FAILS IF: {fails_if}")
        ok, lines = run_leg(fn)
        for ln in lines:
            P(f"   {ln}")
        red_all = True
        for title, cm in breaks:
            n_breaks += 1
            with cm():
                bok, blines = run_leg(fn)
            red = not bok
            n_red += red
            red_all &= red
            # a sabotage may itself be the clock (F-SC-DET, F-SC-ROWS), so a
            # BREAK line prints no digest: every hex run becomes <sha>
            first_bad = re.sub(r"\b[0-9a-f]{16,64}\b", "<sha>", next(
                (x for x in blines if x.startswith("[BAD]")), ""))
            P(f"   [BREAK] {title} -> "
              + ("RED (correct): " + first_bad[:150] if red
                 else "GREEN — VOID: the leg did not see its sabotage"))
        leg_ok = ok and red_all
        n_pass += leg_ok
        if not leg_ok:
            failed.append(name)
        P(f"   {'PASS' if leg_ok else 'FAIL'} {name}")
    after = SC.scored_json_on_file()
    P("")
    P(f"FIXTURE SUMMARY  {n_pass}/{n_legs} PASS · {n_red}/{n_breaks} break "
      f"legs RED · failed {failed or []} · .scored.json on file "
      f"{after or 'NONE'}")
    if a.out:
        Path(a.out).write_text(buf.getvalue(), encoding="utf-8")
    return 0 if (n_pass == n_legs and n_red == n_breaks and not after) else 1


if __name__ == "__main__":
    sys.exit(main())
