#!/usr/bin/env python
"""TIER-C10 PANEL FIXTURES.  TWO KINDS OF LEG PER FIXTURE, the BREAK legs
first: each plants ONE corruption and the guard must go RED on it, or the
fixture is VOID — a check that cannot fail proves nothing.  Then the REAL leg.
A break leg is one of two things and never a third: a CORRUPTED INPUT handed
to the module's own guard (which must refuse it), or a MUTATION of the module
(`mutated(...)`: a named wrong planted as the implementation, under which the
REAL leg's own checks must go RED).  A leg that re-derives a wrong answer
locally and never calls the module proves nothing about the module [TC10
review: F-LOAO-N's BELOW guard was such a leg, and a mutant passed it].
Every fixture states inline what would make it FAIL (the house rule since
F-C4-h).  The banned failure modes remain banned:
  · SELF-COMPARISON — re-deriving a number the way the program derived it;
  · ONE EXAMPLE where cardinality was possible;
  · a TUNED MAGNITUDE BOUND standing in for an identity;
  · a check whose claim is NOT the design's claim.

LAW 4 BINDS THESE FIXTURES TOO.  The only trade book ridden here is the known
control — card v6 on CLASSIC5.  Everything else is SYNTHETIC journals, bar
stamps, or a stubbed replay; no unseen asset's price is read, no unregistered
book exists at any point.  Sabotage operates on COPIES (temp roots, copied
frames, a shadowed module in a throwaway directory) — never on a real artifact.

Run: NAIAD_CACHE_DIR=~/.cache/naiad/snapshots/tc10_20260921 \\
     ~/venvs/naiad/bin/python scripts/tierc10_panel_fixtures.py [leg_substring ...]
Exit 0 = all fixtures pass; exit 1 = at least one failed and NOTHING
DOWNSTREAM IS TRUSTWORTHY.
"""
from __future__ import annotations

import ast
import hashlib
import inspect
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import traceback
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace as NS

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import tierc10_panel as TP                                           # noqa: E402
import tierc9 as T9                                                  # noqa: E402
import tierc8 as T8                                                  # noqa: E402
import tierc7 as T7                                                  # noqa: E402
import tierc6 as T6                                                  # noqa: E402
import tierc6_rules as V6                                            # noqa: E402
import tierc5 as T5                                                  # noqa: E402

PY = str(Path.home() / "venvs" / "naiad" / "bin" / "python")
PANEL_OUT = TP.OUT / TP.PANEL_SUB
PANEL_RERUN = TP.OUT_RERUN / TP.PANEL_SUB
MS_4H, MS_1D = TP.MS_4H, TP.MS_1D

T: list[str] = []
RESULTS: dict[str, bool] = {}
_B: dict = {}


_TMP = re.compile(r"[^\s'\"(),;]*/(f-[a-z0-9]+-)[A-Za-z0-9_]{8}")


def _norm(s: str) -> str:
    """Throwaway directories carry a RANDOM name; the filed transcript must
    not (F-DET's law applies to the evidence too).  Every `f-<leg>-XXXXXXXX`
    temp path is rewritten to `<tmp>/f-<leg>-*` BEFORE any truncation."""
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
        return True, _norm(str(e))[:150]
    return False, "ran to completion"


def mutated(obj, attr: str, wrong, checks):
    """A BREAK LEG BY MUTATION.  Swap ONE attribute of the module under test
    for a WRONG implementation, run the REAL leg's own checks against it,
    restore.  ok == the checks stayed GREEN — i.e. the fixture cannot see the
    wrong it claims to guard.  This is the only kind of break leg that proves
    the REAL leg's assertions have teeth; a leg that re-derives the wrong
    answer locally and never calls the module proves nothing about it."""
    def leg():
        old = getattr(obj, attr)
        setattr(obj, attr, wrong)
        try:
            ok, lines = checks()
        except SystemExit as e:
            ok, lines = False, [f"[BAD] the checks HALTed: {_norm(str(e))}"]
        finally:
            setattr(obj, attr, old)
        bad = [ln for ln in lines if ln.startswith("[BAD]")]
        return ok, ("the REAL leg's checks under the mutation: "
                    + (bad[0][:140] if bad else "no BAD line"))
    return leg


def prove(fid: str, title: str, fails_if: str, breaks: list, real) -> bool:
    """BREAK legs first, judged ONE AT A TIME; any that comes back GREEN
    voids the fixture.  A break leg that CRASHES proves nothing and voids it
    too.  `break() -> (ok, detail)` must return ok == False; `real() ->
    (ok, lines)`."""
    say(f"\n--- {fid} — {title}")
    void = False
    for name, fn in breaks:
        try:
            b_ok, b_detail = fn()
        except BaseException as e:                          # noqa: BLE001
            b_ok, b_detail = True, (f"break leg CRASHED "
                                    f"({type(e).__name__}: {str(e)[:120]})")
        say(f"  [BREAK] {name} -> "
            f"{'RED (correct)' if not b_ok else 'GREEN (FIXTURE IS VOID)'}: "
            f"{b_detail}")
        void |= bool(b_ok)
    try:
        r_ok, lines = real()
    except SystemExit as e:
        r_ok, lines = False, [f"[BAD] the real leg HALTed: {e}"]
    except Exception:                                       # noqa: BLE001
        r_ok, lines = False, ["[BAD] the real leg crashed: "
                              + traceback.format_exc()[-600:]]
    for ln in lines:
        say("    " + ln)
    say(f"      FAILS IF: {fails_if}")
    ok = bool(r_ok) and not void and bool(breaks)
    say(f"  [{'PASS' if ok else 'FAIL'}] {fid}"
        + (" — a break leg passed; the fixture proves nothing" if void
           else ""))
    RESULTS[fid] = ok
    return ok


def books() -> dict:
    """Corridor + the two books F-CTRL compares, ridden ONCE.  CLASSIC5 only."""
    if _B:
        return _B
    lo, hi, meta = TP.corridor_n(TP.CLASSIC5)
    control = TP.run_cell_n(TP.CONTROL_CARD, T9.V6_ROLES, TP.CLASSIC5, lo, hi)
    want = T6.run_cell(V6.CARD_V6, lo, hi)
    _B.update(lo=lo, hi=hi, meta=meta, control=control, want=want,
              got_j=TP.journal_frame(control), want_j=TP.journal_frame(want))
    return _B


def _syn(sym: str, vals, lane: str = "card", t0: int = 0) -> list:
    """A SYNTHETIC journal: only the four fields the rulers read, plus the
    ones the aggregators touch.  No bar, no price, no asset behind it."""
    return [NS(symbol=sym, lane=lane, entry_ms=t0 + i, exit_ms=t0 + i,
               net_r=float(v), direction=1, exit_reason="stop",
               gross_r=float(v), fee_r=0.0, funding_r=0.0)
            for i, v in enumerate(vals)]


SYN12 = tuple(f"SYN{i:02d}USDT" for i in range(12))
# EVERY filing names its LOAO line of record — in the book spec AND in the
# text [tierc10_panel._require_loao_line].  The fixtures' filings say
# "lineage" unless a leg is ABOUT that law, so that each break leg's planted
# corruption is the ONLY defect its filing carries.
_LL = "lineage"
_CL = " " + TP.loao_line_clause(_LL) + "."
# and every arm names the ERA it rides [R1, tierc10_panel._require_era]; the
# fixtures file "full" unless the leg is ABOUT the era law (F-ERA, F-ARM).
_ERA = "full"


# ═══════════════════════════════════════════════ F-CTRL/a · exact zero
def f_ctrl_a() -> bool:
    B = books()

    def _plant(kind):
        def leg():
            j = B["got_j"].copy()
            if kind == "net_r":
                j.loc[j.index[0], "net_r"] = float(j["net_r"].iloc[0]) + 1e-9
            elif kind == "exit_reason":
                j.loc[j.index[3], "exit_reason"] = "bell_12_89_PLANTED"
            else:
                j = j.iloc[1:]
            ok, worst, why = TP.ctrl_diff(j, B["want_j"])
            return ok, f"comparator on the corrupted COPY: {why}"
        return leg

    def real():
        g0 = (B["lo"], B["hi"]) == TP.control_window()
        ok, worst, why = TP.ctrl_diff(B["got_j"], B["want_j"])
        return g0 and ok, [
            f"[{'OK ' if g0 else 'BAD'}] corridor_n(CLASSIC5) == "
            f"tierc5.corridor() (under Stage D's as-of pin "
            f"{B['meta']['stage_d_as_of_pin']}, binds="
            f"{B['meta']['stage_d_pin_binds']}): ({TP.iso(B['lo'])} .. "
            f"{TP.iso(B['hi'] + 1)})",
            f"campaigns: got {len(B['got_j'])}  want {len(B['want_j'])}  "
            f"net {sum(t.net_r for t in B['control']):+.4f} R",
            f"[{'OK ' if ok else 'BAD'}] run_cell_n(v6-control, V6_ROLES, "
            f"CLASSIC5) vs tierc6.run_cell(CARD_V6): WORST ABS DIFF = "
            f"{worst:.3e} (bar EXACTLY 0.000e+00) over {len(TP.CTRL_COLS)} "
            f"columns; {why}"]
    return prove(
        "F-CTRL/a", "v6 on 5 assets, the N-asset path vs tierc6 — EXACT ZERO",
        "any of 12 numeric columns differs by ANY amount, any exit_reason "
        "differs, the counts differ, or corridor_n(CLASSIC5) is not "
        "tierc5.corridor()'s window.",
        [("1e-9 added to ONE net_r in a copy", _plant("net_r")),
         ("one exit_reason relabelled in a copy", _plant("exit_reason")),
         ("one campaign dropped from a copy", _plant("drop"))], real)


# ═══════════════════════════ F-CTRL/b · the cross-process anchor, PREFIX-ROBUST
def _referees() -> list:
    out = []
    p6 = ROOT / "research_outputs" / "tierc6" / "trade_journal.parquet"
    p9 = ROOT / "research_outputs" / "tierc9" / "trade_journal_control.parquet"
    if p6.exists():
        d = pd.read_parquet(p6)
        # tierc6's journal predates the as-of columns; its last bar is the
        # exit bar of the one campaign it left open at the corridor's end.
        out.append(("FILED tierc6/trade_journal", d, int(d["exit_ms"].max())))
    if p9.exists():
        d = pd.read_parquet(p9)
        edge = TP._iso_ms(str(d["as_of_last_closed_4h"].iloc[0])) - MS_4H
        out.append(("FILED tierc9/trade_journal_control", d, edge))
    return out


def f_ctrl_b() -> bool:
    B = books()
    refs = _referees()
    live = B["got_j"]

    def _plant(kind):
        def leg():
            if not refs:
                return True, "no referee on disk — nothing to break"
            name, filed, edge = refs[0]
            j = live.copy()
            shared = j[j["entry_ms"] <= edge].index
            if kind == "lost":
                j = j.drop(shared[5])
            elif kind == "poison":
                m = j["asset"] == "BTCUSDT"
                for c in ("entry_px", "stop_px", "r_dist"):
                    j.loc[m, c] = j.loc[m, c] * 1.005
            elif kind == "early_extra":
                r_ = j.loc[[shared[5]]].copy()
                r_["entry_ms"] = int(r_["entry_ms"].iloc[0]) + MS_4H * 3 + 1
                j = pd.concat([j, r_], ignore_index=True)
            elif kind == "gross":
                j.loc[shared[5], "gross_r"] = float(
                    j.loc[shared[5], "gross_r"]) + 1e-6
            elif kind == "net_unexplained":
                j.loc[shared[5], "net_r"] = float(
                    j.loc[shared[5], "net_r"]) + 1e-3
            else:
                j.loc[shared[5], "exit_ms"] = int(j.loc[shared[5],
                                                        "exit_ms"]) + MS_4H
            ok, lines = TP.ctrl_prefix(j, filed, edge, name)
            bad = [ln for ln in lines if ln.startswith("[BAD]")]
            return ok, (bad[0][:150] if bad else "no BAD line")
        return leg

    def real():
        if len(refs) < 2:
            return False, ["[BAD] a filed referee journal is ABSENT "
                           "(research_outputs/tierc6|tierc9 are gitignored; "
                           "a fresh worktree has none) — the cross-process "
                           "anchor cannot be proven and is NOT skipped."]
        ok, lines = True, []
        for name, filed, edge in refs:
            g, ln = TP.ctrl_prefix(live, filed, edge, name)
            ok &= g
            lines += ln
        return ok, lines
    return prove(
        "F-CTRL/b", "cross-process anchor vs the FILED journals — "
        "PREFIX-ROBUST (filed 196 rows, live 200)",
        "a FILED campaign is missing live; entry_px/stop_px/r_dist drift by "
        "ANY amount from the filed artifact; a campaign the referee saw "
        "close closed differently, or its gross_r/fee_r/mfe_r moved by ANY "
        "amount, or its net_r moved by anything but its own funding_r; a "
        "live-only campaign entered INSIDE the referee's window; or a "
        "referee is absent.  (net_r is NOT asserted across processes: the "
        "funding substrate was topped up; the drift is printed and "
        "attributed campaign by campaign.)",
        [("a filed campaign LOST from a copy of the live book",
          _plant("lost")),
         ("BTC prices x1.005 in a copy (the poisoned-shared-memo scenario)",
          _plant("poison")),
         ("an extra campaign planted INSIDE the filed window",
          _plant("early_extra")),
         ("a closed campaign's exit moved one bar in a copy",
          _plant("exit_moved")),
         ("1e-6 added to ONE closed campaign's gross_r in a copy",
          _plant("gross")),
         ("a closed campaign's net_r moved 1e-3 with NO funding_r to "
          "explain it", _plant("net_unexplained"))], real)


# ═══════════════════════════════════════ F-SUBSTRATE · the frozen snapshot
def f_substrate() -> bool:
    def _with(env_value):
        def leg():
            old_env = os.environ.get("NAIAD_CACHE_DIR")
            old = dict(TP._SUB)
            TP._SUB.clear()
            try:
                if env_value is None:
                    os.environ.pop("NAIAD_CACHE_DIR", None)
                else:
                    os.environ["NAIAD_CACHE_DIR"] = env_value
                r, why = refused(TP.substrate)
            finally:
                if old_env is None:
                    os.environ.pop("NAIAD_CACHE_DIR", None)
                else:
                    os.environ["NAIAD_CACHE_DIR"] = old_env
                TP._SUB.clear()
                TP._SUB.update(old)
            return (not r), why
        return leg

    def real():
        s = TP.substrate()
        g1 = Path(s["cache_root"]).resolve() != TP.LIVE_CACHE.resolve()
        g2 = TP.TB.KLINES.resolve().parent == Path(s["cache_root"]).resolve()
        return g1 and g2, [
            f"[{'OK ' if g1 else 'BAD'}] substrate = {s['substrate']} "
            f"({s['cache_root']}) — NOT the live cache",
            f"[{'OK ' if g2 else 'BAD'}] tierc2_baseline.KLINES is BOUND "
            f"inside it: {TP.TB.KLINES}"]
    with tempfile.TemporaryDirectory(prefix="f-substrate-") as td:
        return prove(
            "F-SUBSTRATE", "every read comes from the frozen snapshot [LAW 3]",
            "NAIAD_CACHE_DIR is unset, names the live cache, or names a "
            "directory the loaders were not bound to at import.",
            [("NAIAD_CACHE_DIR unset", _with(None)),
             ("NAIAD_CACHE_DIR = the LIVE cache", _with(str(TP.LIVE_CACHE))),
             ("NAIAD_CACHE_DIR exported AFTER import (a different dir)",
              _with(td))], real)


# ═══════════════════ F-PANEL · the three panels, resolved from Stage D's record
def f_panel() -> bool:
    have = TP.STAGE_D_MANIFEST.exists()
    man = json.loads(TP.STAGE_D_MANIFEST.read_text()) if have else None

    def _resolve_copy(mutate):
        """resolve_unseen12 over a MUTATED COPY of Stage D's manifest (or, in
        a tree where Stage D has not run, over a synthetic one in its shape).
        ok == the resolver accepted it AND every resolved stem has a 4h file."""
        def leg():
            m = json.loads(json.dumps(man)) if have else {
                "complete": True, "admission": {"rows": [
                    {"asset": n, "stem": s, "symbol": s, "admitted": True}
                    for n, s, _ in TP.UNSEEN12_PROVISIONAL]}}
            out = mutate(m)
            with tempfile.TemporaryDirectory(prefix="f-panel-") as td:
                p = Path(td) / "STAGE_D_MANIFEST.json"
                p.write_text(out if isinstance(out, str) else json.dumps(m))
                try:
                    r_ = TP.resolve_unseen12(p)
                except SystemExit as e:
                    return False, str(e)[:150]
            nofile = [s for s in r_["symbol_of"].values()
                      if s and TP.open_ms_4h(s) is None]
            if nofile and have:
                return False, (f"resolved to {nofile}: NO such 4h file in "
                               f"the snapshot — a loader would HALT, or "
                               f"worse, find another venue's tape")
            return True, "accepted"
        return leg

    def m_incomplete(m):
        m["complete"] = False

    def m_lost(m):
        m["admission"]["rows"] = [r_ for r_ in m["admission"]["rows"]
                                  if r_["asset"] != "SUI"]

    def m_twice(m):
        m["admission"]["rows"].append(dict(
            [r_ for r_ in m["admission"]["rows"] if r_["asset"] == "ENA"][0]))

    def m_garbage(m):
        return "{ this is not json"

    def m_symbol_not_stem(m):
        ven = {v["asset"]: v.get("symbol") for v in m.get("venues", [])}
        for r_ in m["admission"]["rows"]:
            r_["symbol"] = ven.get(r_["asset"], r_.get("stem"))
            r_.pop("stem", None)

    def b_record_vs_bars():
        if not have:
            return False, "no Stage D manifest in this tree — nothing to bend"
        m = json.loads(json.dumps(man))
        for r_ in m["admission"]["rows"]:
            if r_["asset"] == "LTC":
                r_["closed_4h_bars"] = int(r_["closed_4h_bars"]) + 1
        with tempfile.TemporaryDirectory(prefix="f-panel-") as td:
            p = Path(td) / "STAGE_D_MANIFEST.json"
            p.write_text(json.dumps(m))
            bent = TP.resolve_unseen12(p)
        real_u12 = dict(TP._U12)
        TP._U12.clear()
        TP._U12.update(bent)
        try:
            r, why = refused(TP.panel17)
        finally:
            TP._U12.clear()
            TP._U12.update(real_u12)
        return (not r), why

    def real():
        ok, lines = True, []
        g = (TP.CLASSIC5 is TP.RC.UNIVERSE and len(TP.UNSEEN12_CONTRACT) == 12
             and TP.UNSEEN12_CONTRACT == (
                 "ENA", "PUMPFUN", "HYPE", "MNT", "SUI", "LTC", "XMR", "BNB",
                 "UNI", "PEPE", "DOGE", "BONK")
             and not set(TP.UNSEEN12) & set(TP.CLASSIC5)
             and TP.PANEL17[:5] == TP.CLASSIC5)
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] CLASSIC5 IS the lineage's "
                     f"UNIVERSE object; the contract's twelve, in the "
                     f"contract's order; the panels are disjoint; PANEL17 "
                     f"leads with CLASSIC5")
        lines.append(f"      UNSEEN12 ({TP.UNSEEN12_SOURCE}): "
                     f"{list(TP.UNSEEN12)}")
        p17 = TP.panel17()
        g = p17 == TP.PANEL17 and len(set(p17)) == len(p17)
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] PANEL17 (declared, "
                     f"{len(TP.PANEL17)}) == panel17() (MEASURED from the "
                     f"snapshot's bars, {len(p17)}) — record and data agree "
                     f"on every asset's closed-4h count and admission")
        if have:
            mnt = TP._U12["symbol_of"]["MNT"]
            ven = {v["asset"]: v for v in man["venues"]}
            g = (mnt == ven["MNT"]["stem"] != ven["MNT"]["symbol"]
                 and TP.open_ms_4h(mnt) is not None
                 and TP.open_ms_4h(ven["MNT"]["symbol"]) is None
                 and list(man["panels"]["PANEL17_stems"]) == list(TP.PANEL17)
                 and list(man["panels"]["CLASSIC5"]) == list(TP.CLASSIC5))
            ok &= g
            lines.append(f"[{'OK ' if g else 'BAD'}] MNT resolves to its "
                         f"cache STEM {mnt!r} (venue "
                         f"{ven['MNT']['venue']}), not the venue's symbol "
                         f"{ven['MNT']['symbol']!r} — which has NO file; "
                         f"PANEL17 equals Stage D's own PANEL17_stems, in "
                         f"order")
        with tempfile.TemporaryDirectory(prefix="f-panel-") as td:
            pr = TP.resolve_unseen12(Path(td) / "absent.json")
        g = (pr["source"].startswith("PROVISIONAL")
             and list(pr["symbol_of"]) == list(TP.UNSEEN12_CONTRACT)
             and pr["manifest_admitted"] is None)
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] with NO manifest the "
                     f"documented PROVISIONAL tuple is used and SAYS SO "
                     f"({pr['source']})")
        return ok, lines
    return prove(
        "F-PANEL", "CLASSIC5 · UNSEEN12 · PANEL17 — named, resolved from "
        "Stage D's manifest, never from a guess beside a record",
        "a half-written, unreadable, short or double-naming manifest is "
        "accepted (or silently replaced by the provisional tuple); an "
        "alternate-venue asset resolves to the venue's symbol instead of "
        "its cache stem; the record and the bars disagree unnoticed; or "
        "PANEL17 is not CLASSIC5 + the admitted twelve.",
        [("a COPY of the manifest with complete=false",
          _resolve_copy(m_incomplete)),
         ("a COPY of the manifest that lost SUI", _resolve_copy(m_lost)),
         ("a COPY of the manifest naming ENA twice", _resolve_copy(m_twice)),
         ("an UNREADABLE manifest (the provisional tuple is no fallback)",
          _resolve_copy(m_garbage)),
         ("a COPY keyed on the venue SYMBOL, the stem removed",
          _resolve_copy(m_symbol_not_stem)),
         ("a COPY of the record claiming one more LTC bar than the snapshot "
          "holds", b_record_vs_bars)], real)


# ═══════════════════════════════ F-ADMIT · admission, floors, the corridor
def f_admit() -> bool:
    t0 = TP._ms("2024-01-01")                   # a MONDAY, 00:00Z
    syn = {
        "SYN715USDT": t0 + np.arange(715, dtype=np.int64) * MS_4H,
        "SYN716USDT": t0 + np.arange(716, dtype=np.int64) * MS_4H,
        "SYNAUSDT": t0 + np.arange(1000, dtype=np.int64) * MS_4H,
        "SYNBUSDT": t0 + (100 + np.arange(890, dtype=np.int64)) * MS_4H,
        "SYNWEEKUSDT": t0 + np.arange(42, dtype=np.int64) * MS_4H,
        "SYNRAGUSDT": t0 + MS_4H + np.arange(84, dtype=np.int64) * MS_4H,
    }

    def _seeded(fn):
        def leg():
            TP._OPEN.update(syn)
            try:
                return fn()
            finally:
                for k in syn:
                    TP._OPEN.pop(k, None)
        return leg

    def _b(panel=None, pin=None):
        def inner():
            r, why = refused(lambda: TP.corridor_n(
                panel or ("SYNAUSDT", "SYNBUSDT"), pin_close_iso=pin))
            return (not r), why
        return _seeded(inner)

    def real():
        a = TP.admission(tuple(syn)).set_index("symbol")
        ok, lines = True, []
        g = TP.ADMIT_MIN_BARS == TP.WARMUP_BARS + 400 == 716 \
            and TP.WARMUP_BARS is TP.RC.WARMUP_BARS
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] need = WARMUP_BARS (the "
                     f"card's OBJECT, {TP.WARMUP_BARS}) + 400 = "
                     f"{TP.ADMIT_MIN_BARS}, derived not typed")
        g = (not a.loc["SYN715USDT", "admitted"]
             and bool(a.loc["SYN716USDT", "admitted"])
             and "715 closed 4h bars < 716" in a.loc["SYN715USDT",
                                                     "excluded_because"])
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] the bar binds AT 716: 715 "
                     f"bars EXCLUDED and named with its count, 716 admitted")
        x = TP.admission(("NOSUCHUSDT",)).iloc[0]
        g = (not x["admitted"]) and x["n_closed_4h"] == 0 \
            and "no 4h kline file" in x["excluded_because"]
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] an asset with no file is a "
                     f"NAMED exclusion (0 bars), never a silent drop")
        g = (a.loc["SYNWEEKUSDT", "n_complete_1d"] == 7
             and a.loc["SYNWEEKUSDT", "n_complete_1w"] == 1
             and a.loc["SYNRAGUSDT", "n_complete_1d"] == 13
             and a.loc["SYNRAGUSDT", "n_complete_1w"] == 1
             and datetime(2024, 1, 1, tzinfo=timezone.utc).weekday() == 0)
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] [L1] Mon-Sun x 42 bars = 7 "
                     f"complete days, 1 MONDAY week; a tape starting Mon "
                     f"04:00 for 84 bars = 13 complete days (ragged first "
                     f"and last day refused), 1 week")
        lo, hi, m = TP.corridor_n(("SYNAUSDT", "SYNBUSDT"))
        want = {
            "lo": t0, "hi": t0 + 989 * MS_4H + MS_4H - 1,
            "fa": TP.iso(t0 + 316 * MS_4H), "fb": TP.iso(t0 + 416 * MS_4H),
            "sa": 990 - 316, "sb": 890 - 316}
        got = {"lo": lo, "hi": hi,
               "fa": m["per_asset_floor_4h"]["SYNAUSDT"],
               "fb": m["per_asset_floor_4h"]["SYNBUSDT"],
               "sa": m["per_asset_scorable_bars_in_corridor"]["SYNAUSDT"],
               "sb": m["per_asset_scorable_bars_in_corridor"]["SYNBUSDT"]}
        g = got == want and m["binding_edge_assets"] == ["SYNBUSDT"]
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] corridor_n on a 2-asset "
                     f"synthetic panel (A: 1000 bars; B: listed 100 bars "
                     f"later, ends 10 bars earlier): end = MIN of the last "
                     f"opens (B binds), floors = each asset's OWN bar 316, "
                     f"scorable A {got['sa']} / B {got['sb']} — hand answer "
                     f"{want['sa']} / {want['sb']}")
        _, hi_p, m_p = TP.corridor_n(("SYNAUSDT", "SYNBUSDT"),
                                     pin_close_iso=TP.iso(t0 + 900 * MS_4H))
        g = hi_p == t0 + 900 * MS_4H - 1 and "corridor_pinned_to" in m_p
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] a pin that looks BACK, on "
                     f"a bar close, is honoured to the millisecond")
        return ok, lines
    return prove(
        "F-ADMIT", "admission 316+400, per-asset floors, the N-asset "
        "corridor — known answers on SYNTHETIC stamps",
        "715 bars is admitted or 716 refused; an absent asset is dropped "
        "without a row; a week is counted on the Thursday anchor or a ragged "
        "day as complete; the corridor ends on the MAX of the last opens; a "
        "floor is the panel's instead of the asset's; or any guard below "
        "lets its plant through.",
        [("an UNADMITTED member (715 bars) in the panel",
          _b(panel=("SYNAUSDT", "SYN715USDT"))),
         ("a pin AFTER the panel's last closed bar",
          _b(pin=TP.iso(t0 + 2000 * MS_4H))),
         ("a pin OFF the 4h grid (pinned by day count, not by bar)",
          _b(pin=TP.iso(t0 + 900 * MS_4H + 3_600_000))),
         ("a duplicated symbol in the panel",
          _b(panel=("SYNAUSDT", "SYNAUSDT"))),
         # the estate's resample_ohlcv anchors weeks on the epoch's THURSDAY;
         # under that anchor the Monday-to-Sunday week above is NOT a week.
         ("MUTATION: the module's week anchor moved to the epoch's THURSDAY "
          "(MONDAY_EPOCH_OFFSET_MS := 0)",
          mutated(TP, "MONDAY_EPOCH_OFFSET_MS", 0, _seeded(real))),
         ("MUTATION: the admission bar loosened (ADMIT_MIN_BARS := 700)",
          mutated(TP, "ADMIT_MIN_BARS", 700, _seeded(real)))],
        _seeded(real))


# ═══════════════════════════ F-FUNDING · never the silent {} · memo safety
def f_funding() -> bool:
    def _memo(mutate):
        def leg():
            sym = "BTCUSDT"
            TP.frame_n(sym)
            real_entry = T5._FRAMES[sym]
            fake = dict(real_entry)
            mutate(fake)
            T5._FRAMES[sym] = fake
            try:
                r, why = refused(lambda: TP.frame_n(sym))
            finally:
                T5._FRAMES[sym] = real_entry
            return (not r), why
        return leg

    def _empty_fund(e):
        e["fund"] = {}

    def _foreign_lens(e):
        f = e["f"]
        om = f.open_ms.copy()
        om[1000] += 300_000                 # one 5m-grid stamp inside the tape
        e["f"] = NS(open_ms=om)

    def _short(e):
        e["f"] = NS(open_ms=e["f"].open_ms[:-1])

    def b_absent():
        r, why = refused(lambda: TP.require_funding(("NOSUCHUSDT",)))
        return (not r), why

    def _cov(**plant):
        """require_funding fed a COPY of BTC's real coverage row with ONE
        field corrupted — the file on disk is never touched."""
        def leg():
            real_cov = TP.funding_coverage
            TP.funding_coverage = lambda s: dict(real_cov(s), **plant)
            try:
                r, why = refused(lambda: TP.require_funding(("BTCUSDT",)))
            finally:
                TP.funding_coverage = real_cov
            return (not r), why
        return leg

    def real():
        silent = TP.TB.load_funding("NOSUCHUSDT")
        cov = TP.require_funding(TP.CLASSIC5)
        g1 = silent == {}
        g2 = all(c["funding_present"] and c["n_stamps"] > 1000
                 and c["n_holes_after_floor"] == 0
                 and c["max_spacing_h_after_floor"]
                 <= TP.FUNDING_MAX_NATIVE_INTERVAL_H for c in cov)
        st = [TP.frame_n(s) for s in TP.CLASSIC5]
        g3 = all(bool(s_["fund"]) for s_ in st)
        return g2 and g3, [
            f"[{'OK ' if g1 else 'NB '}] THE HAZARD, demonstrated: "
            f"tierc2_baseline.load_funding('NOSUCHUSDT') returns "
            f"{silent!r} with no error — zero funding that looks like a "
            f"number",
            f"[{'OK ' if g2 else 'BAD'}] require_funding(CLASSIC5) holds: "
            + "; ".join(f"{c['symbol']} {c['n_stamps']} stamps to "
                        f"{c['last_stamp']} (stale "
                        f"{c['stale_hours_vs_kline_edge']}h, longest spacing "
                        f"after the floor {c['max_spacing_h_after_floor']}h, "
                        f"holes {c['n_holes_after_floor']})"
                        for c in cov),
            f"[{'OK ' if g3 else 'BAD'}] frame_n: every CLASSIC5 frame is "
            f"the snapshot's native 4h tape with a NON-EMPTY funding dict"]
    return prove(
        "F-FUNDING", "funding absent -> HALT for a panel asset; the frame "
        "memo is safe under the bare-symbol key",
        "a panel asset with no funding file — or funding that stops short "
        "of the kline edge, or starts after the first scorable bar, or has "
        "an interior spacing longer than the venues' 8h — reaches the "
        "accounting; a frame with an empty funding dict, a foreign-lens "
        "stamp or a truncated tape is accepted under the bare-symbol key.",
        [("a panel asset with NO funding file", b_absent),
         ("funding 888h STALE at the tail (the estate's state on the "
          "morning of 2026-09-21, replayed on a copy of the coverage row)",
          _cov(stale_hours_vs_kline_edge=888.0)),
         ("funding that STARTS a day after the first scorable bar",
          _cov(head_gap_hours_vs_first_scorable_bar=24.0)),
         ("an INTERIOR hole: one 16h spacing after the first scorable bar "
          "(head and tail both fine)",
          _cov(n_holes_after_floor=1, max_spacing_h_after_floor=16.0)),
         ("a COPY of the BTC memo entry with an EMPTY funding dict",
          _memo(_empty_fund)),
         ("a COPY of the BTC memo entry with a 5m-grid stamp planted",
          _memo(_foreign_lens)),
         ("a COPY of the BTC memo entry one bar short of the snapshot file",
          _memo(_short))], real)


# ═══════════════════════ F-LAW4-GATE · no unregistered book can be ridden
_GATE_TXT = ("SYNTHETIC-GATE-TEST, shaped like P-GEN-1: card v6, all pins "
             "frozen, on the twelve, vs zero; the 17-asset view beside. "
             "Filed by a fixture in a throwaway directory; the replay is "
             "STUBBED and nothing is ridden." + _CL)


class _LyingRoles(T9.Roles):
    """trigger 9/12 in the FIELDS, v6 in the `.periods` PROPERTY."""
    @property
    def periods(self):
        return T9.V6_ROLES.periods


def f_law4_gate() -> bool:
    B = books()
    calls = []

    def _stubbed(fn, as_real: bool = False, stub_frames: bool = False):
        """Run `fn` with `tierc9.replay9` replaced by a call counter — NO bar
        is replayed inside this fixture, ever.  `as_real=True` additionally
        tells the gate the stub IS the real replay (the gate must then refuse
        a throwaway registry; were it to fail, only the stub would run).
        `stub_frames=True` keeps `frame_n` from building an unseen asset's
        frame when a leg is EXPECTED to open the gate."""
        def leg():
            stub = lambda s_, *a, **k: (calls.append(s_), ([], []))[1]  # noqa: E731
            real_replay, real_mark = T9.replay9, TP._REPLAY9_AT_IMPORT
            real_frame = TP.frame_n
            T9.replay9 = stub
            if as_real:
                TP._REPLAY9_AT_IMPORT = stub
            if stub_frames:
                TP.frame_n = lambda s_: None
            before = set(T5._FRAMES)
            calls.clear()
            try:
                out = fn()
            finally:
                T9.replay9, TP._REPLAY9_AT_IMPORT = real_replay, real_mark
                TP.frame_n = real_frame
            built = sorted(set(T5._FRAMES) - before)
            return out, list(calls), built
        return leg

    r912 = T9.Roles(name="trigger-9/12", trg_f=9, trg_s=12)
    knob = T8.Card(name="v6-control", trail_min_advance_atr=0.0)
    liar = _LyingRoles(name="v6-roles", trg_f=9, trg_s=12)
    unseen = tuple(s for s in TP.UNSEEN12 if s not in TP.CLASSIC5)[:1] \
        or ("ENAUSDT",)

    def _gen1(root):
        """P-GEN-1's SHAPE: v6 on UNSEEN12 (scored) + the PANEL17 view."""
        TP.register("P-GEN-1", _GATE_TXT, 45, root=root, arms=[
            TP.arm_spec("P-GEN-1 vs zero", TP.UNSEEN12, "vs_zero",
                        card=TP.CONTROL_CARD, roles=T9.V6_ROLES,
                        loao_line=_LL, era=_ERA),
            TP.arm_spec("P-GEN-1 17-asset view", TP.PANEL17, "vs_zero",
                        scored_in_family=False, card=TP.CONTROL_CARD,
                        roles=T9.V6_ROLES, loao_line=_LL, era=_ERA)])

    def _c5(root):
        TP.register("X-C5-1", _GATE_TXT, 1, root=root, arms=[
            TP.arm_spec("X-C5-1 trigger", TP.CLASSIC5, "two_sample",
                        card=TP.CONTROL_CARD, roles=r912, loao_line=_LL,
                        era=_ERA)])

    def _b(card, roles, panel, what, file=None, as_real=False, hi=None, **kw):
        """ok == the book RAN: not refused, or the (stubbed) replay was
        called, or a frame was built.  `file(root)` files a registration in a
        throwaway root first; `kw` is what the caller offers at the door."""
        def leg():
            with tempfile.TemporaryDirectory(prefix="f-law4-") as td:
                root = Path(td)
                k2 = dict(kw)
                if file:
                    file(root)
                    k2["reg_root"] = root
                (r, why), n, built = _stubbed(lambda: refused(
                    lambda: TP.run_cell_n(card, roles, panel, B["lo"],
                                          hi if hi is not None else B["hi"],
                                          **k2)), as_real=as_real)()
            ran = (not r) or bool(n) or bool(built)
            return ran, (f"{what}: refused={r}, replay calls={len(n)}, "
                         f"frames built={built or 'none'} — {why[:110]}")
        return leg

    def b_stale_pin():
        """THE WITNESS HOLE at run_cell_n's door: X-C5-1 is filed first and
        its head pinned; P-GEN-1 is filed after it, so that pin can say
        nothing about P-GEN-1's line.  The replay and frame_n are stubbed —
        if the door opened, the stub is what would run, not a bar."""
        with tempfile.TemporaryDirectory(prefix="f-law4-") as td:
            root = Path(td)
            a = TP.register("X-C5-1", _GATE_TXT, 1, root=root, arms=[
                TP.arm_spec("X-C5-1 trigger", TP.CLASSIC5, "two_sample",
                            card=TP.CONTROL_CARD, roles=r912, loao_line=_LL,
                            era=_ERA)])
            pin = (a["registry_len"], a["registry_head"])
            _gen1(root)                               # P-GEN-1 is line TWO
            lo_p, hi_p, _ = TP.corridor_n(TP.UNSEEN12)
            (r, why), n, built = _stubbed(lambda: refused(
                lambda: TP.run_cell_n(
                    TP.CONTROL_CARD, T9.V6_ROLES, TP.UNSEEN12, lo_p, hi_p,
                    reg_id="P-GEN-1", text=_GATE_TXT, reg_root=root,
                    head_of_record=pin)), stub_frames=True)()
        ran = (not r) or bool(n) or bool(built)
        return ran, (f"stale pin (line 1) at run_cell_n's door for a "
                     f"registration filed at line 2: refused={r}, replay "
                     f"calls={len(n)}, frames built={built or 'none'} — "
                     f"{why[:110]}")

    def _b_ref(make, what):
        """`reference_row` is the one ruler that needs NO registration — so
        it must take the control Book and nothing else."""
        def leg():
            r, why = refused(lambda: TP.reference_row(make()))
            return (not r), f"{what}: {why[:120]}"
        return leg

    def real():
        ok, lines = True, []
        g = (TP.is_control_book(TP.CONTROL_CARD, T9.V6_ROLES, TP.CLASSIC5)
             and TP.is_control_book(T8.Card(name="any-name"), T9.V6_ROLES,
                                    TP.CLASSIC5[:2])
             and not TP.is_control_book(knob, T9.V6_ROLES, TP.CLASSIC5)
             and not TP.is_control_book(TP.CONTROL_CARD, r912, TP.CLASSIC5)
             and not TP.is_control_book(TP.CONTROL_CARD, T9.V6_ROLES, unseen)
             and not TP.is_control_book(V6.CARD_V6, T9.V6_ROLES,
                                        TP.CLASSIC5)
             and liar.periods == T9.V6_ROLES.periods
             and not TP.is_control_book(TP.CONTROL_CARD, liar, TP.CLASSIC5)
             and not TP.is_control_book(TP.CONTROL_CARD, T9.V6_ROLES, ()))
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] is_control_book: TRUE for "
                     f"the v6 control under any name on any CLASSIC5 subset; "
                     f"FALSE for a moved knob, swapped roles, an unseen "
                     f"asset, a foreign Card class, an EMPTY panel, and a "
                     f"Roles SUBCLASS whose `.periods` property says v6 "
                     f"while its fields say 9/12")
        with tempfile.TemporaryDirectory(prefix="f-law4-") as td:
            root = Path(td)
            _c5(root)
            (out, n, built) = _stubbed(lambda: TP.run_cell_n(
                TP.CONTROL_CARD, r912, TP.CLASSIC5, B["lo"], B["hi"],
                reg_id="X-C5-1", text=_GATE_TXT, reg_root=root))()
            g = (n == list(TP.CLASSIC5) and list(out) == []
                 and isinstance(out, TP.Book)
                 and out.spec["arm"] == "X-C5-1 trigger"
                 and out.spec["registration"] == "X-C5-1"
                 and out.spec["ride"]["roles_fields"]["trg_s"] == "12")
            ok &= g
            lines.append(f"[{'OK ' if g else 'BAD'}] WITH the registration "
                         f"OF THIS BOOK filed, the gate opens: the (STUBBED) "
                         f"replay was called once per panel asset {n}; the "
                         f"returned Book carries its provenance (arm "
                         f"{out.spec.get('arm')!r}) and holds nothing, "
                         f"because no unregistered book may exist even "
                         f"inside a fixture")
            _gen1(root)
            got = {}
            for nm, pnl in (("P-GEN-1 vs zero", TP.UNSEEN12),
                            ("P-GEN-1 17-asset view", TP.PANEL17)):
                lo_p, hi_p, _ = TP.corridor_n(pnl)
                (o_, n_, b_) = _stubbed(lambda: TP.run_cell_n(
                    TP.CONTROL_CARD, T9.V6_ROLES, pnl, lo_p, hi_p,
                    reg_id="P-GEN-1", text=_GATE_TXT, reg_root=root),
                    stub_frames=True)()
                got[nm] = (n_ == list(pnl) and o_.spec["arm"] == nm
                           and not b_)
            g = all(got.values())
            ok &= g
            lines.append(f"[{'OK ' if g else 'BAD'}] a P-GEN-1-SHAPED filing "
                         f"opens BOTH of its own books — v6 on UNSEEN12 and "
                         f"the PANEL17 view — each matched to its own arm "
                         f"({got}); replay AND frame_n stubbed: no unseen "
                         f"asset's frame was built")
        bk = books()["control"]
        g = (isinstance(bk, TP.Book) and bk.spec["arm"] == "(control)"
             and bk.spec["ride"] == TP.CONTROL_RIDE
             and bk.spec["panel"] == list(TP.CLASSIC5)
             and not isinstance(bk[:10], TP.Book)
             and not isinstance([t for t in bk], TP.Book))
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] the control rides unfiled "
                     f"and returns a Book saying so; a SLICE or a FILTER of "
                     f"it is a plain list — provenance does not survive "
                     f"editing the book")
        return ok, lines
    return prove(
        "F-LAW4-GATE", "run_cell_n refuses every book but the known control "
        "— and every book but the REGISTERED one — BEFORE one bar is "
        "replayed",
        "any non-control book reaches replay9 or builds a frame without a "
        "filed registration OF THAT BOOK: an unseen asset, a swapped "
        "trigger, a moved knob with no filing; trigger 9/12 or a moved knob "
        "or another panel under SOME OTHER book's filing; no text offered; "
        "a STALE head pin (one taken before the registration's own registry "
        "line); a throwaway registry opening a REAL replay; a duplicated "
        "panel or "
        "an end beyond the as-of as 'the control'; the unregistered "
        "reference row taking a book that is not the control Book; or the "
        "gate stays shut for the book that WAS filed.",
        [(f"card v6 on an UNSEEN asset {unseen}, no registration",
          _b(TP.CONTROL_CARD, T9.V6_ROLES, unseen, "unseen asset")),
         ("trigger 9/12 on CLASSIC5, no registration",
          _b(TP.CONTROL_CARD, r912, TP.CLASSIC5, "swapped trigger")),
         ("a moved knob under the control's NAME, no registration",
          _b(knob, T9.V6_ROLES, TP.CLASSIC5, "lying card name")),
         ("RIGHT REGISTRY, WRONG BOOK: trigger 9/12 on UNSEEN12 under "
          "P-GEN-1's id (P-TRG-2 NOT filed)",
          _b(TP.CONTROL_CARD, r912, TP.UNSEEN12, "P-TRG-2's book", _gen1,
             reg_id="P-GEN-1", text=_GATE_TXT)),
         ("RIGHT REGISTRY, WRONG BOOK: a moved knob on PANEL17 under "
          "P-GEN-1's id",
          _b(knob, T9.V6_ROLES, TP.PANEL17, "moved knob", _gen1,
             reg_id="P-GEN-1", text=_GATE_TXT)),
         ("RIGHT REGISTRY, WRONG PANEL: a PANEL17 book under a CLASSIC5 "
          "registration",
          _b(TP.CONTROL_CARD, r912, TP.PANEL17, "wrong panel", _c5,
             reg_id="X-C5-1", text=_GATE_TXT)),
         ("RIGHT BOOK, WRONG ARM NAMED: UNSEEN12 offered as the '17-asset "
          "view'",
          _b(TP.CONTROL_CARD, T9.V6_ROLES, TP.UNSEEN12, "wrong arm", _gen1,
             reg_id="P-GEN-1", text=_GATE_TXT,
             arm="P-GEN-1 17-asset view")),
         ("the right book under P-GEN-1 with NO TEXT offered (text=None)",
          _b(TP.CONTROL_CARD, T9.V6_ROLES, TP.UNSEEN12, "no text", _gen1,
             reg_id="P-GEN-1")),
         ("the right book under P-GEN-1 with a STALE head pin (taken at the "
          "filing BEFORE it)", b_stale_pin),
         ("the right book, the right filing — in a THROWAWAY registry, "
          "with the replay the gate believes is REAL",
          _b(TP.CONTROL_CARD, r912, TP.CLASSIC5, "throwaway registry", _c5,
             as_real=True, reg_id="X-C5-1", text=_GATE_TXT)),
         ("a Roles SUBCLASS lying through `.periods` (fields 9/12), no "
          "registration",
          _b(TP.CONTROL_CARD, liar, TP.CLASSIC5, "lying roles")),
         ("('BTCUSDT', 'BTCUSDT') as 'the control' — BTC ridden twice",
          _b(TP.CONTROL_CARD, T9.V6_ROLES, ("BTCUSDT", "BTCUSDT"),
             "duplicate panel")),
         ("the control with an END beyond the as-of (hi + 1e12 ms)",
          _b(TP.CONTROL_CARD, T9.V6_ROLES, TP.CLASSIC5, "window",
             hi=books()["hi"] + 10 ** 12)),
         ("the control with an end OFF the 4h grid",
          _b(TP.CONTROL_CARD, T9.V6_ROLES, TP.CLASSIC5, "window",
             hi=books()["hi"] - 1)),
         ("reference_row handed the control's trades as a BARE LIST (no "
          "provenance)",
          _b_ref(lambda: list(books()["control"]), "bare list")),
         ("reference_row handed a SYNTHETIC journal under an unseen symbol, "
          "wearing the control's provenance",
          _b_ref(lambda: TP.Book(
              _syn(unseen[0], [1.0] * 5) + _syn("BTCUSDT", [1.0] * 5),
              spec=books()["control"].spec), "stray asset"))], real)


# ═══════════════════════════════ F-LOAO-N · known answers on SYNTHETIC books
def f_loao_n() -> bool:
    def _per(n_above, n=12, n_below=0):
        """`n_above` panels excluding zero ABOVE, then `n_below` excluding it
        BELOW, the rest straddling."""
        return [{"dropped": f"S{i}", "n": 10,
                 "point": -1.0 if n_above <= i < n_above + n_below else 1.0,
                 "ci_lo": 0.1, "ci_hi": 2.0,
                 "excludes_zero": i < n_above + n_below,
                 "excludes_above": i < n_above,
                 "excludes_below": n_above <= i < n_above + n_below}
                for i in range(n)]

    # THE TWO NAMED WRONGS, AS IMPLEMENTATIONS — planted INTO the module by
    # `mutated(...)`, so the REAL leg's own assertions are what must go RED.
    real_summary = TP._loao_summary

    def wrong_below_counts(per, n_panels):
        """the S-STOPGRID wrong: EITHER direction counts toward the line."""
        out = real_summary(per, n_panels)
        out["loao_clears_above_half"] = bool(
            out["loao_excluding_zero"] >= out["loao_bar_above_half"])
        return out

    def wrong_literal_3(per, n_panels):
        """tierc7.loao's bar, verbatim: the literal `>= 3`, on any N."""
        out = real_summary(per, n_panels)
        out["loao_clears_above_half"] = bool(out["loao_excluding_above"] >= 3)
        return out

    def b_stray():
        bk = _syn("SYN00USDT", [1.0] * 5) + _syn("STRAYUSDT", [1.0] * 5)
        r, why = refused(lambda: TP.loao_n(bk, None, SYN12))
        return (not r), why

    def real():
        ok, lines = True, []
        tt = {1: 1, 2: 2, 4: 3, 5: 3, 12: 7, 16: 9, 17: 9}
        g = all(TP.above_half_bar(k) == v for k, v in tt.items())
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] above_half_bar truth table "
                     f"{tt} — 3/5 reproduced, 7/12, 9/17")
        g = (not TP._loao_summary(_per(3), 12)["loao_clears_above_half"]
             and not TP._loao_summary(_per(6), 12)["loao_clears_above_half"]
             and TP._loao_summary(_per(7), 12)["loao_clears_above_half"]
             and "loao_clears_3_of_5" not in TP._loao_summary(_per(7), 12)
             and TP._loao_summary(_per(3, 5), 5)["loao_clears_3_of_5"])
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] on twelve: 3 above FAILS, "
                     f"6 above FAILS (half is not above half), 7 CLEARS; "
                     f"the key `loao_clears_3_of_5` exists ONLY on a "
                     f"five-asset row")
        # R2 (operator, verbatim: "All 17") — the BRK lanes ride PANEL17, so
        # the line they must clear is 9/17, and EIGHT is not a majority.
        s8, s9 = TP._loao_summary(_per(8, 17), 17), TP._loao_summary(
            _per(9, 17), 17)
        g = (s8["loao_bar_above_half"] == s9["loao_bar_above_half"] == 9
             and s8["loao_clears_above_half"] is False
             and s9["loao_clears_above_half"] is True
             and s9["loao_line"] == "9/17 above"
             and "loao_clears_3_of_5" not in s9)
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] on SEVENTEEN [R2 \"All "
                     f"17\"]: the bar is {s9['loao_bar_above_half']}/17 — 8 "
                     f"above does NOT clear, '{s9['loao_line']}' does")
        sb7 = TP._loao_summary(_per(0, 12, n_below=7), 12)
        sb12 = TP._loao_summary(_per(0, 12, n_below=12), 12)
        mix = TP._loao_summary(_per(4, 12, n_below=5), 12)
        g = (sb7["loao_excluding_zero"] == 7
             and sb7["loao_excluding_below"] == 7
             and sb7["loao_clears_above_half"] is False
             and sb12["loao_clears_above_half"] is False
             and mix["loao_excluding_zero"] == 9
             and mix["loao_clears_above_half"] is False
             and mix["loao_line"] == "4/12 above, 5/12 BELOW")
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] BELOW NEVER COUNTS: 7 of 12 "
                     f"panels excluding zero BELOW (7 >= the bar of 7) does "
                     f"NOT clear; 12 of 12 BELOW does not clear; 4 above + "
                     f"5 BELOW (9 excluding zero) does not clear — "
                     f"'{mix['loao_line']}'")
        allneg = []
        for s in SYN12:
            allneg += _syn(s, [-1.0] * 10)
        an = TP.loao_n(allneg, None, SYN12, seed=TP.SEED)
        g = (an["loao_line"] == "0/12 above, 12/12 BELOW"
             and an["loao_excluding_zero"] == 12
             and an["loao_clears_above_half"] is False)
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] an all -1 twelve-asset BOOK "
                     f"through loao_n -> '{an['loao_line']}', clears="
                     f"{an['loao_clears_above_half']} — a reliable loss is "
                     f"not a reliable gain")
        allpos, whale, mirror = [], [], []
        for i, s in enumerate(SYN12):
            allpos += _syn(s, [1.0] * 10)
            whale += _syn(s, [-100.0] * 10 if i == 0 else [1.0] * 10)
            mirror += _syn(s, [100.0] * 10 if i == 0 else [-1.0] * 10)
        a = TP.loao_n(allpos, None, SYN12, seed=TP.SEED)
        w = TP.loao_n(whale, None, SYN12, seed=TP.SEED)
        m = TP.loao_n(mirror, None, SYN12, seed=TP.SEED)
        g = (a["loao_line"] == "12/12 above" and a["loao_clears_above_half"]
             and w["loao_line"] == "1/12 above"
             and not w["loao_clears_above_half"]
             and [p["dropped"] for p in w["_per"] if p["excludes_above"]]
             == ["SYN00USDT"]
             and m["loao_line"] == "0/12 above, 1/12 BELOW"
             and not m["loao_clears_above_half"])
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] VS ZERO, twelve assets: all "
                     f"+1 -> '{a['loao_line']}' clears; eleven +1 and one "
                     f"-100 whale -> '{w['loao_line']}' (only the panel that "
                     f"DROPS the whale clears; P(whale drawn) = "
                     f"1-(10/11)^11 = 65% sinks the rest); the mirror -> "
                     f"'{m['loao_line']}' — the direction split holds")
        base0 = []
        for s in SYN12:
            base0 += _syn(s, [0.0] * 10)
        t2 = TP.loao_n(allpos, base0, SYN12, two_sample=True, seed=TP.SEED)
        pr = TP.loao_n(allpos, base0, SYN12, two_sample=False, seed=TP.SEED)
        g = (t2["loao_line"] == pr["loao_line"] == "12/12 above"
             and t2["loao_mode"] == "two_sample" and pr["loao_mode"] == "paired"
             and all(p["ci_lo"] == p["ci_hi"] == 1.0 for p in t2["_per"]))
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] TWO-SAMPLE and PAIRED: new "
                     f"= base + 1 on every campaign -> every leave-out CI is "
                     f"[1.0, 1.0], '{t2['loao_line']}' under both rulers")
        two = TP.loao_n(_syn("SYN00USDT", [1.0] * 9)
                        + _syn("SYN01USDT", [1.0] * 9), None, SYN12[:2])
        g = two["loao_line"] == "0/2 above" and two["loao_bar_above_half"] == 2
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] a leave-out panel with ONE "
                     f"cluster cannot be bootstrapped and counts AGAINST the "
                     f"line ('{two['loao_line']}', bar 2)")
        # SEVEN assets trade (+1 each), FIVE declared assets never do: every
        # one of the five "leave-out" panels IS the headline.
        seven = [t for s in SYN12[:7] for t in _syn(s, [1.0] * 10)]
        z = TP.loao_n(seven, None, SYN12, seed=TP.SEED)
        g = (z["loao_line"] == "12/12 above" and z["loao_assets_present"] == 7
             and z["loao_zero_campaign_assets"] == ",".join(SYN12[7:])
             and z["loao_above_excl_zero_campaign_panels"] == 7
             and a["loao_zero_campaign_assets"] == ""
             and a["loao_above_excl_zero_campaign_panels"] == 12)
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] a declared asset with NO "
                     f"campaign is SAID: 7 trading + 5 silent -> line "
                     f"'{z['loao_line']}' (N = the declared panel, the "
                     f"lineage's law) with assets_present "
                     f"{z['loao_assets_present']} and "
                     f"{z['loao_above_excl_zero_campaign_panels']} above "
                     f"once the five headline-copies are excluded, printed "
                     f"beside it")
        # PARITY WITH THE PARENT, key for key, on five assets and ITS seed.
        rng = np.random.default_rng(20260921)
        new5, base5 = [], []
        for s in TP.CLASSIC5:
            b_ = rng.normal(0.1, 1.0, 40)
            base5 += _syn(s, b_)
            new5 += _syn(s, np.concatenate([b_[:30] + rng.normal(0.3, .5, 30),
                                            rng.normal(0.5, 1.0, 8)]))
        bad = []
        for ts in (True, False):
            mine = TP.loao_n(new5, base5, TP.CLASSIC5, two_sample=ts,
                             seed=TP.SEED_LINEAGE)
            par = T7.loao(new5, base5, "x", two_sample=ts)
            for k in ("loao_panels", "loao_excluding_zero",
                      "loao_excluding_above", "loao_excluding_below",
                      "loao_line", "loao_detail", "loao_worst_drop",
                      "loao_clears_3_of_5"):
                if mine[k] != par[k]:
                    bad.append((ts, k))
            if [(p["ci_lo"], p["ci_hi"]) for p in mine["_per"]] != \
                    [(p["ci_lo"], p["ci_hi"]) for p in par["_per"]]:
                bad.append((ts, "_per"))
        g = not bad
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] PARITY: loao_n(panel="
                     f"CLASSIC5, seed=20260816) == tierc7.loao on 8 keys + "
                     f"every leave-out CI, two-sample AND paired, on a "
                     f"noisy synthetic pair of books (mismatches: "
                     f"{bad or 'none'})")
        return ok, lines
    return prove(
        "F-LOAO-N", "LOAO over N assets: the above-half bar, the direction "
        "split, three rulers, parity with tierc7.loao",
        "the bar is the literal 3 on twelve; half counts as above-half; a "
        "BELOW panel counts toward the line (7 or 12 BELOW of 12 clears, or "
        "4 above + 5 BELOW clears); a book asset outside the panel is "
        "accepted; any of four hand-built books gives a count other than "
        "12/12, 1/12, 0/12+1 BELOW, 0/12+12 BELOW; a silent declared asset "
        "is not named; or loao_n differs from tierc7.loao on five assets at "
        "the lineage seed.",
        [("MUTATION: tierc7's literal `>= 3` planted as the module's bar",
          mutated(TP, "_loao_summary", wrong_literal_3, real)),
         ("MUTATION: BELOW panels counted toward the line (excludes_zero "
          "planted as the module's count)",
          mutated(TP, "_loao_summary", wrong_below_counts, real)),
         ("MUTATION: half counts as above-half (above_half_bar := N // 2)",
          mutated(TP, "above_half_bar", lambda n: max(n // 2, 1), real)),
         ("a book holding an asset OUTSIDE the declared panel", b_stray)],
        real)


# ═══════════════════ F-EAR-BOOT · the NEW equal-asset-risk CI, known answers
def f_ear_boot() -> bool:
    B = books()
    vals = {"SYNAUSDT": [1.0, 3.0], "SYNBUSDT": [0.0, 0.0, 0.0, 0.0],
            "SYNCUSDT": [-2.0], "SYNDUSDT": [0.5, 1.5, 2.5],
            "SYNEUSDT": [4.0, -1.0, 0.0, 1.0, 1.0, 1.0]}
    bk = [t for s, v in vals.items() for t in _syn(s, v)]
    v = np.array([t.net_r for t in bk])
    c = np.array([t.symbol for t in bk])

    def _slot_weight_draws(n):
        """The design, written out the LONG way: per draw, every drawn SLOT
        is a cluster, w = (N_draw / K) / n_slot, stat = sum(w r) / N_draw."""
        uniq = np.unique(c)
        rng = np.random.default_rng(TP.SEED)
        out = []
        for _ in range(n):
            pick = rng.choice(uniq, size=len(uniq), replace=True)
            slots = [v[c == u] for u in pick]
            nd, k = sum(len(s) for s in slots), len(slots)
            out.append(sum(float(np.sum(((nd / k) / len(s)) * s))
                           for s in slots) / nd)
        return np.array(out)

    def _label_dedupe_draws(n):
        """THE NAMED WRONG: weights recomputed on SYMBOL LABELS
        (tierc6.ear_weights on the concatenated draw) — a twice-drawn asset
        collapses into one cluster."""
        uniq = np.unique(c)
        rng = np.random.default_rng(TP.SEED)
        out = []
        for _ in range(n):
            pick = rng.choice(uniq, size=len(uniq), replace=True)
            ts = [t for u in pick for t in bk if t.symbol == u]
            w = T6.ear_weights(ts)
            out.append(float(np.sum(w * np.array([t.net_r for t in ts])))
                       / len(ts))
        return np.array(out)

    mine = TP.cluster_boot_ear(v, c, seed=TP.SEED, n_boot=400)

    def b_dedupe():
        wrong = _label_dedupe_draws(400)
        same = bool(np.max(np.abs(wrong - mine)) <= 1e-12)
        return same, (f"label-dedupe draws vs the design: worst "
                      f"{np.max(np.abs(wrong - mine)):.3e}; 90% width "
                      f"{np.percentile(wrong, 95) - np.percentile(wrong, 5):.4f}"
                      f" vs {np.percentile(mine, 95) - np.percentile(mine, 5):.4f}"
                      f" — the wrong one is NARROWER")

    def b_raw_as_ear():
        raw = T7.cluster_boot(v, c, seed=TP.SEED, n_boot=400)
        same = bool(np.max(np.abs(raw - mine)) <= 1e-12)
        return same, (f"raw per-campaign draws passed off as EAR on an "
                      f"UNBALANCED book: worst "
                      f"{np.max(np.abs(raw - mine)):.3e}")

    def real():
        ok, lines = True, []
        hand = (2.0 + 0.0 - 2.0 + 1.5 + 1.0) / 5.0
        g = TP.ear_expectancy(v, c) == hand and abs(float(np.mean(v))
                                                    - 12.5 / 16.0) < 1e-15
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] point: mean of per-asset "
                     f"means = {TP.ear_expectancy(v, c)} (hand: (2+0-2+1.5+1)"
                     f"/5 = {hand}); the raw mean is {float(np.mean(v))} — "
                     f"two different numbers, as they must be")
        rs = [t.net_r for t in B["control"]]
        ac = [t.symbol for t in B["control"]]
        a6 = T6.agg_ear(B["control"], "x")["expectancy_r"]
        g = TP.r4(TP.ear_expectancy(rs, ac)) == a6
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] on the CLASSIC5 control the "
                     f"point equals tierc6.agg_ear's weighted expectancy "
                     f"({a6}) — another module's arithmetic, same number")
        long_way = _slot_weight_draws(400)
        worst = float(np.max(np.abs(long_way - mine)))
        g = worst <= 1e-12
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] 400 draws: the closed form "
                     f"== EAR weights recomputed PER DRAW on slots, written "
                     f"the long way on the same rng stream (worst "
                     f"{worst:.3e}; bar 1e-12 = ~1e3 x the rounding of a "
                     f"16-term O(1) sum, derived not tuned)")
        bal = [t for s in SYN12[:5] for t in _syn(
            s, np.random.default_rng(int(s[3:5]) + 7).normal(0, 1, 8))]
        bv = np.array([t.net_r for t in bal])
        bc = np.array([t.symbol for t in bal])
        worst = float(np.max(np.abs(
            TP.cluster_boot_ear(bv, bc, seed=TP.SEED, n_boot=400)
            - T7.cluster_boot(bv, bc, seed=TP.SEED, n_boot=400))))
        g = worst <= 1e-12
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] on a BALANCED book (equal n "
                     f"per asset) the EAR draws ARE the raw ruler's draws "
                     f"(worst {worst:.3e}) — same seed, same asset picks; "
                     f"only the weighting differs")
        same = TP.cluster_boot_ear_diff(v, c, v, c, seed=TP.SEED, n_boot=200)
        plus = TP.cluster_boot_ear_diff(v + 1.0, c, v, c, seed=TP.SEED,
                                        n_boot=200)
        g = bool(np.all(same == 0.0)) and float(np.max(np.abs(plus - 1.0))) \
            <= 1e-12
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] two-sample: A == B -> every "
                     f"draw 0.0; A = B + 1 -> every draw 1.0")
        va, ca = np.array([1.0, 1.0, 3.0, 3.0]), np.array(["X", "X", "Y", "Y"])
        vb, cb = np.array([0.0, 0.0]), np.array(["X", "X"])
        dd = TP.cluster_boot_ear_diff(va, ca, vb, cb, seed=TP.SEED, n_boot=400)
        fin = set(np.round(dd[np.isfinite(dd)], 12))
        g = fin == {1.0, 2.0} and bool(np.isnan(dd).any())
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] an asset PRESENT in A only: "
                     f"draws are exactly {{1.0 (X,X), 2.0 (X,Y)}} and NaN "
                     f"when B has no asset in the draw (Y,Y) — K is the "
                     f"assets PRESENT per book, never the universe")
        return ok, lines
    return prove(
        "F-EAR-BOOT", "the equal-asset-risk cluster-bootstrap CI — NEW in "
        "TIER-C10 — against hand answers",
        "the point is not the mean of per-asset means; the draws differ "
        "from EAR weights recomputed per draw on SLOTS; a twice-drawn asset "
        "is collapsed; a balanced book's EAR draws differ from the raw "
        "ruler's; or the two-sample twin misses 0 / 1 / {1, 2, NaN}.",
        [("EAR weights recomputed on SYMBOL LABELS (the named wrong)",
          b_dedupe),
         ("the RAW ruler's draws offered as the EAR draws", b_raw_as_ear)],
        real)


# ═══════════════════════ F-REG-GATE · text before result, enforced in code
_TXT = ("P-SYN-1 [45%] a SYNTHETIC claim on a SYNTHETIC twelve-asset book: "
        "expectancy vs zero. Filed by a fixture in a throwaway directory."
        + _CL)
_TXT_SHARP = ("P-SYN-1 [80%] SHARPENED AFTER THE LOOK: expectancy vs zero on "
              "the campaigns that happened to win." + _CL)
_TXT0 = "an earlier synthetic filing." + _CL
_TXT_LATER = "a better claim, written later." + _CL


def _syn_book():
    rng = np.random.default_rng(20260921)
    return [t for s in SYN12 for t in _syn(s, rng.normal(0.4, 1.0, 12))]


# A "vs card v6" arm is scored ONLY against a Book that says it IS card v6 on
# the arm's panel.  These journals are SYNTHETIC — they never touched a bar —
# so the fixture writes that provenance BY HAND, here, where a grep for
# `Book(` on real data finds this comment instead of a finding.
_V6_ON_SYN12 = {"ride": TP.CONTROL_RIDE, "panel": list(SYN12),
                "lo_ms": 0, "hi_ms": 1}


def _v6_base(trades) -> "TP.Book":
    return TP.Book(trades, spec=dict(_V6_ON_SYN12))


_N: dict = {}


def noisy() -> dict:
    """SYNTHETIC journals WITH NOISE — the books a verdict, a seed or a
    set-change law can actually be caught on.  The estate's older synthetic
    legs ride the degenerate +1 book: every draw is 1.0, the CI is [1, 1] and
    the row says SUPPORTED whatever `_verdict`, whichever seed and whichever
    ruler ran [TC10 review r2: five fatal mutants passed all 15 legs].  These
    are drawn ONCE from `default_rng(20260921)`, in this order, so the
    transcript is byte-reproducible:

      base      12 assets x 20 campaigns, mean 0.0   — the twin every ruler
                that is not vs-zero measures against;
      winning   the same 240 keys, mean +1.0, sd 0.3 — CI wholly ABOVE zero;
      straddle  the same keys, mean +0.05, sd 1.0    — POINT above zero and
                the interval straddling it (the one book on which "verdict =
                point > 0" differs from the lineage's law);
      losing    the same keys, mean -1.0, sd 0.3     — CI wholly BELOW zero;
      grown     straddle's 240 keys + 4 NEW keys per asset (288);
      shrunk    the first 15 keys per asset (180) — the base keeps 60 unpaired.
    """
    if _N:
        return _N
    rng = np.random.default_rng(20260921)
    mk = lambda mu, sd, n=20, t0=0: [                            # noqa: E731
        t for s in SYN12 for t in _syn(s, rng.normal(mu, sd, n), t0=t0)]
    base = mk(0.0, 1.0)
    winning = mk(1.0, 0.3)
    straddle = mk(0.05, 1.0)
    losing = mk(-1.0, 0.3)
    extra = mk(0.05, 1.0, n=4, t0=10_000)        # keys 10000..10003, unpaired
    _N.update(base=base, base_book=_v6_base(base), winning=winning,
              straddle=straddle, losing=losing, grown=straddle + extra,
              shrunk=[t for t in straddle if t.entry_ms < 15],
              n_base=len(base), n_grown=len(straddle) + len(extra),
              n_shrunk=len([t for t in straddle if t.entry_ms < 15]))
    return _N


def _arms12(name: str = "P-SYN-1 vs zero", ruler: str = "vs_zero", **kw):
    """One EXTERNAL-runner arm on the synthetic twelve."""
    kw.setdefault("loao_line", _LL)
    kw.setdefault("era", _ERA)
    return [TP.arm_spec(name, SYN12, ruler, **kw)]


def f_reg_gate() -> bool:
    book = _syn_book()
    base0 = TP.Book([t for s in SYN12 for t in _syn(s, [0.0] * 12)],
                    spec={"ride": TP.CONTROL_RIDE, "panel": list(SYN12),
                          "lo_ms": 0, "hi_ms": 1})

    def _scenario(prepare, act=None):
        """Fresh temp root; `prepare(root)` plants ONE corruption; then the
        act (default: score) is attempted.  ok == it RAN."""
        def leg():
            with tempfile.TemporaryDirectory(prefix="f-reg-") as td:
                root = Path(td) / "registrations"
                root.mkdir()
                carry = prepare(root)
                r, why = refused(act(root, carry) if act else (
                    lambda: TP.score("P-SYN-1", _TXT, book, SYN12,
                                     root=root)))
                return (not r), why
        return leg

    def _file(root):
        TP.register("P-SYN-0", _TXT0, 50, root=root,
                    arms=_arms12("P-SYN-0 vs zero"))
        return TP.register("P-SYN-1", _TXT, 45, root=root, arms=_arms12())

    def p_none(root):
        TP.register("P-SYN-0", _TXT0, 50, root=root,
                    arms=_arms12("P-SYN-0 vs zero"))

    def p_tamper_text(root):
        _file(root)
        p = root / "P-SYN-1.json"
        rec = json.loads(p.read_text())
        rec["text"] = rec["text"].replace("vs zero", "vs minus one")
        p.write_text(json.dumps(rec, indent=2, sort_keys=True))

    def _reforge(root, edit):
        """The smarter forger: edits the record AND recomputes both shas
        inside the file.  Only the hash-chained registry can see this."""
        _file(root)
        p = root / "P-SYN-1.json"
        rec = json.loads(p.read_text())
        edit(rec)
        pay = TP._payload(rec["registration"], rec["text"], rec["prior_pct"],
                          rec["family_m"], rec["fields"], rec["book_spec"])
        rec["sha256"] = TP._payload_sha(pay)
        rec["text_sha256"] = TP._sha(rec["text"])
        p.write_text(json.dumps(rec, indent=2, sort_keys=True))

    def p_forge_prior(root):
        _reforge(root, lambda rec: rec.update(prior_pct=5))

    def p_forge_spec(root):
        """the book spec quietly re-pointed at a friendlier ruler."""
        def edit(rec):
            rec["book_spec"] = {"arms": _arms12(ruler="two_sample")}
        _reforge(root, edit)

    def p_refile(root):
        _file(root)
        (root / "P-SYN-1.json").unlink()

    def p_registry_cut(root):
        _file(root)
        p = root / TP.REGISTRY
        p.write_text("\n".join(p.read_text().splitlines()[1:]) + "\n")

    def p_wrong_m(root):
        TP.register("P-SYN-1", _TXT, 45, family_m=5, root=root,
                    arms=_arms12())

    def p_scored_first(root):
        (root / "P-SYN-9.scored.json").write_text("{}")

    def p_wipe(root):
        """THE WHOLE-DIRECTORY WIPE.  File, score (the look), take the pin
        the way a tracked file would hold it, rmtree, re-file SHARPER."""
        rec = _file(root)
        pin = (rec["registry_len"], rec["registry_head"])
        TP.score("P-SYN-1", _TXT, book, SYN12, root=root, head_of_record=pin)
        shutil.rmtree(root)
        root.mkdir()
        TP.register("P-SYN-0", _TXT0, 50, root=root,
                    arms=_arms12("P-SYN-0 vs zero"))
        TP.register("P-SYN-1", _TXT_SHARP, 80, root=root, arms=_arms12())
        return pin

    def p_scored(root):
        _file(root)
        TP.score("P-SYN-1", _TXT, book, SYN12, root=root)

    def p_stale(root):
        """THE WITNESS HOLE [TC10 review r2, BLOCKING 1]: the pin is taken at
        the FIRST filing and carried — the natural usage — so it predates
        P-SYN-1's own registry line and can say nothing about it."""
        a = TP.register("P-SYN-0", _TXT0, 50, root=root,
                        arms=_arms12("P-SYN-0 vs zero"))
        TP.register("P-SYN-1", _TXT, 45, root=root, arms=_arms12())
        return (a["registry_len"], a["registry_head"])

    def p_amend_behind_pin(root):
        """The same hole, USED: file, look, then cut the line, sharpen the
        text and re-chain — all BEHIND a pin that names line 1, which the
        attack never touches (the reviewer's probeF, replayed)."""
        pin = p_stale(root)
        TP.score("P-SYN-1", _TXT, book, SYN12, root=root)          # THE LOOK
        (root / "P-SYN-1.json").unlink()
        (root / "P-SYN-1.scored.json").unlink()
        p = root / TP.REGISTRY
        p.write_text(p.read_text().splitlines()[0] + "\n")
        TP.register("P-SYN-1", _TXT_SHARP, 80, root=root, arms=_arms12())
        return pin

    def b_stale_canonical():
        """The stale pin at the CANONICAL door (the throwaway root stands in
        as REG_DIR; the real one is never touched)."""
        with tempfile.TemporaryDirectory(prefix="f-reg-") as td:
            root = Path(td) / "registrations"
            root.mkdir()
            pin = p_stale(root)
            old = TP.REG_DIR
            TP.REG_DIR = root
            try:
                r, why = refused(lambda: TP.score(
                    "P-SYN-1", _TXT, book, SYN12, root=root,
                    head_of_record=pin))
            finally:
                TP.REG_DIR = old
        return (not r), why

    def p_no_loao_line(root):
        """A record filed BEFORE the LOAO-line law: the law is lifted off the
        module for the filing only, so the file, its shas and the chain are
        consistent and the ONLY defect is the unsaid count."""
        old = TP._require_loao_line
        TP._require_loao_line = lambda spec, text, where: _LL
        try:
            TP.register("P-SYN-1", _TXT, 45, root=root, arms=[TP.arm_spec(
                "P-SYN-1 vs zero", SYN12, "vs_zero", era=_ERA)])
        finally:
            TP._require_loao_line = old

    def p_two_arm(root):
        TP.register("P-SYN-1", _TXT, 45, root=root, arms=[
            TP.arm_spec("P-SYN-1 vs zero", SYN12, "vs_zero",
                        loao_line=_LL, era=_ERA),
            TP.arm_spec("P-SYN-1 view", SYN12[:6], "vs_zero",
                        scored_in_family=False, loao_line=_LL, era=_ERA)])

    def _canonical(fn):
        """Run `fn` with the throwaway root standing in AS the canonical
        registry — the real REG_DIR is never touched."""
        def act(root, carry):
            def go():
                old = TP.REG_DIR
                TP.REG_DIR = root
                try:
                    return fn(root)
                finally:
                    TP.REG_DIR = old
            return go
        return act

    def checks():
        ok, lines = True, []
        with tempfile.TemporaryDirectory(prefix="f-reg-") as td:
            root = Path(td) / "registrations"
            a = TP.register("P-SYN-0", _TXT0, 50,
                            root=root, arms=_arms12("P-SYN-0 vs zero"))
            b = TP.register("P-SYN-1", _TXT, 45, root=root, arms=_arms12(),
                            fields={"ruler": "vs zero", "panel": "SYN12"})
            byts = (root / "P-SYN-1.json").read_bytes()
            again = TP.register("P-SYN-1", _TXT, 45, root=root,
                                arms=_arms12(),
                                fields={"panel": "SYN12", "ruler": "vs zero"})
            last = json.loads((root / TP.REGISTRY).read_text()
                              .splitlines()[-1])
            g = ((a["seq"], b["seq"]) == (1, 2) and again["already_filed"]
                 and (root / "P-SYN-1.json").read_bytes() == byts
                 and b["text_sha256"]
                 == hashlib.sha256(_TXT.encode("utf-8")).hexdigest()
                 and b["family_m"] == 6 and b["prior_pct"] == 45
                 and b["book_spec"]["arms"][0]["panel"] == list(SYN12)
                 and (b["registry_len"], b["registry_head"])
                 == (2, last["line_sha256"])
                 and TP.registry_head(root)["registry_head"]
                 == last["line_sha256"])
            ok &= g
            lines.append(f"[{'OK ' if g else 'BAD'}] register(): monotone "
                         f"seq {a['seq']}, {b['seq']}; text_sha256 == an "
                         f"independent sha256 of the text; the BOOK SPEC is "
                         f"in the hashed payload; re-filing the SAME payload "
                         f"is a no-op (bytes unchanged); the returned "
                         f"registry_len/registry_head == the registry "
                         f"file's own last line (2, "
                         f"{b['registry_head'][:12]}...) — the pin")
            pin = (b["registry_len"], b["registry_head"])
            row = TP.score("P-SYN-1", _TXT, book, SYN12, root=root,
                           head_of_record=pin)
            want_sha = hashlib.sha256(json.dumps(sorted(
                [str(t.symbol), str(t.lane), int(t.entry_ms),
                 repr(float(t.net_r))] for t in book)).encode()).hexdigest()
            g = (row["registration_seq"] == 2
                 and row["registration_sha256"] == b["sha256"]
                 and row["prior_pct"] == 45 and row["seed"] == 20260921
                 and row["sens_seed"] == 20260816
                 and row["loao_seed"] == row["seed"]
                 and row["sens_loao_seed"] == row["sens_seed"]
                 and row["loao_panels"] == 12
                 and row["loao_bar_above_half"] == 7
                 and row["arm"] == "P-SYN-1 vs zero"
                 and row["book_sha256"] == want_sha
                 and row["registry_head_pinned"] is True
                 and row["registry_pin"] == f"2:{b['registry_head']}"
                 and row["registry_head"] == b["registry_head"]
                 and row["registration_root_is_canonical"] is False
                 and (root / "P-SYN-1.scored.json").exists())
            ok &= g
            lines.append(f"[{'OK ' if g else 'BAD'}] score() RUNS with the "
                         f"text on file and the head PINNED: the row carries "
                         f"seq {row['registration_seq']}, the registration "
                         f"sha, the filed arm, prior 45, seed 20260921 "
                         f"THREADED INTO LOAO (loao_seed "
                         f"{row['loao_seed']}, echo "
                         f"{row['sens_loao_seed']}), LOAO {row['loao_line']} "
                         f"(bar 7/12), an independently recomputed "
                         f"book_sha256, registry_head_pinned=True, "
                         f"registration_root_is_canonical=False (a fixture "
                         f"root SAYS so); verdict {row['verdict']} on a "
                         f"SYNTHETIC book")
            g = (row["registry_pin_covers_seq"] is True
                 and row["loao_line_of_record"] == _LL
                 and row["loao_above_of_record"] == row["loao_excluding_above"]
                 and row["arm_era"] == _ERA)
            ok &= g
            lines.append(f"[{'OK ' if g else 'BAD'}] the row says WHICH pin "
                         f"vouched and that it COVERS this registration's own "
                         f"line (registry_pin_covers_seq "
                         f"{row['registry_pin_covers_seq']}), and it names "
                         f"the LOAO count the FILING chose "
                         f"({row['loao_line_of_record']} -> "
                         f"{row['loao_above_of_record']}/12) and the era it "
                         f"was filed for ({row['arm_era']})")
            sb = (root / "P-SYN-1.scored.json").read_bytes()
            row2 = TP.score("P-SYN-1", _TXT, book, SYN12, root=root,
                            head_of_record=pin)
            g = (row2 == row
                 and (root / "P-SYN-1.scored.json").read_bytes() == sb
                 and json.loads(sb)["arms"]["P-SYN-1 vs zero"]["book_sha256"]
                 == want_sha)
            ok &= g
            lines.append(f"[{'OK ' if g else 'BAD'}] a RE-SCORE of the same "
                         f"book under the same seed is legal and identical "
                         f"(--rerun); .scored.json binds the arm to its "
                         f"first inputs and its bytes do not move")
            tb = TP.registration_table(root)
            g = list(tb["registration"]) == ["P-SYN-0", "P-SYN-1"] \
                and list(tb["seq"]) == [1, 2] and "field_ruler" in tb.columns \
                and list(tb["scored_panel"]) == [TP.panel_name(SYN12)] * 2 \
                and set(tb["registry_head"]) == {b["registry_head"]}
            ok &= g
            lines.append(f"[{'OK ' if g else 'BAD'}] registration_table(): "
                         f"both filings, in filing order, the scored arm's "
                         f"panel/ruler and the registry head riding")
            # A LATER FILING MUST NOT INVALIDATE AN EARLIER PIN — the prefix
            # law — and the head taken AFTER the last filing vouches for all
            # of them.  (Only a pin BEFORE a registration's line is refused.)
            c3 = TP.register("P-SYN-2", _TXT0.replace("earlier", "third"), 30,
                             root=root, arms=_arms12("P-SYN-2 vs zero"))
            pin3 = (c3["registry_len"], c3["registry_head"])
            r_old = TP.score("P-SYN-1", _TXT, book, SYN12, root=root,
                             head_of_record=pin)
            r_new = TP.score("P-SYN-1", _TXT, book, SYN12, root=root,
                             head_of_record=pin3)
            g = (pin3[0] == 3 and r_old["registry_head_pinned"] is True
                 and r_new["registry_head_pinned"] is True
                 and r_new["registry_pin"] == f"3:{c3['registry_head']}"
                 and r_new["registry_pin_covers_seq"] is True
                 and r_old["registry_pin"] == f"2:{b['registry_head']}")
            ok &= g
            lines.append(f"[{'OK ' if g else 'BAD'}] THE PREFIX LAW, BOTH "
                         f"WAYS: with a THIRD registration filed after the "
                         f"look, P-SYN-1 still opens under its OWN pin (line "
                         f"2) and under the NEWER head (line 3) — a pin at "
                         f"or after a registration's line vouches for it, a "
                         f"pin before it does not (break legs above)")
            # THE LOAO COUNT OF RECORD FOLLOWS THE FILING, not the look: the
            # same book, two filings, two lines — 7 assets trade, 5 declared
            # assets are silent, so the two counts DISAGREE by construction.
            seven = [t for s in SYN12[:7] for t in _syn(s, [1.0] * 10)]
            rows_ll = {}
            for ch in TP.LOAO_LINES:
                rid = f"P-SYN-L-{ch}"
                t_ = (f"P-SYN-L [40%] the same synthetic book under the "
                      f"{ch} count. " + TP.loao_line_clause(ch) + ".")
                TP.register(rid, t_, 40, root=root,
                            arms=_arms12(f"{rid} arm", loao_line=ch))
                rows_ll[ch] = TP.score(rid, t_, seven, SYN12, root=root,
                                       n_boot=_NB_FIX)
            li, ex = rows_ll["lineage"], rows_ll["excl_zero_campaign"]
            g = (li["loao_line_of_record"] == "lineage"
                 and ex["loao_line_of_record"] == "excl_zero_campaign"
                 and li["loao_above_of_record"] == 12
                 and ex["loao_above_of_record"] == 7
                 and li["loao_excluding_above"] == ex["loao_excluding_above"]
                 == 12
                 and li["loao_above_excl_zero_campaign_panels"]
                 == ex["loao_above_excl_zero_campaign_panels"] == 7
                 and li["loao_clears_line_of_record"] is True
                 and ex["loao_clears_line_of_record"] is True)
            ok &= g
            lines.append(f"[{'OK ' if g else 'BAD'}] WHICH COUNT CARRIES THE "
                         f"LINE IS THE FILING'S CHOICE: one book (7 assets "
                         f"trading, 5 declared and silent), two filings — "
                         f"the lineage row's line of record is "
                         f"{li['loao_above_of_record']}/12, the "
                         f"excl-zero-campaign row's is "
                         f"{ex['loao_above_of_record']}/12, and BOTH rows "
                         f"print BOTH counts beside each other")
            # THE HAZARD, DEMONSTRATED — and the property the pin rests on.
            shutil.rmtree(root)
            TP.register("P-SYN-0", _TXT0, 50,
                        root=root, arms=_arms12("P-SYN-0 vs zero"))
            same = TP.register("P-SYN-1", _TXT, 45, root=root,
                               arms=_arms12(),
                               fields={"ruler": "vs zero", "panel": "SYN12"})
            shutil.rmtree(root)
            TP.register("P-SYN-0", _TXT0, 50,
                        root=root, arms=_arms12("P-SYN-0 vs zero"))
            sharp = TP.register("P-SYN-1", _TXT_SHARP, 80, root=root,
                                arms=_arms12())
            unp = TP.score("P-SYN-1", _TXT_SHARP,
                           [t for t in book if t.net_r > -0.5], SYN12,
                           root=root)
            g = (same["registry_head"] == b["registry_head"]
                 and sharp["registry_head"] != b["registry_head"]
                 and sharp["seq"] == 2
                 and unp["registry_head_pinned"] is False
                 and unp["registry_head"] != b["registry_head"])
            ok &= g
            lines.append(f"[{'OK ' if g else 'BAD'}] THE HAZARD, "
                         f"demonstrated: wipe the WHOLE directory and "
                         f"re-file sharper text -> seq {sharp['seq']} again, "
                         f"the chain restarts at GENESIS and an UNPINNED "
                         f"score is ACCEPTED (row says registry_head_pinned="
                         f"{unp['registry_head_pinned']}). What betrays it: "
                         f"the head MOVED ({b['registry_head'][:12]}... -> "
                         f"{sharp['registry_head'][:12]}...), while an "
                         f"IDENTICAL re-file reproduces the head exactly. "
                         f"The wipe is visible ONLY against a head recorded "
                         f"outside the directory — so the canonical registry "
                         f"REFUSES a door without one (break legs below)")
        return ok, lines

    real_loao = TP.loao_n

    def loao_drops_seed(new, base, panel, two_sample=False, seed=TP.SEED,
                        label="", n_boot=TP.N_BOOT):
        return real_loao(new, base, panel, two_sample, TP.SEED_LINEAGE,
                         label, n_boot)

    sc = lambda **kw: (lambda root, carry: (lambda: TP.score(  # noqa: E731
        **dict(dict(reg_id="P-SYN-1", text=_TXT, book=book, panel=SYN12,
                    root=root), **kw))))
    return prove(
        "F-REG-GATE", "score() REFUSES without its registration AND on any "
        "book but its own; a filed text can be neither amended, swapped, "
        "deleted, wiped nor back-filled",
        "score() returns a row when the registration is missing, its text "
        "or its BOOK SPEC was altered (even with the in-file shas "
        "recomputed), no text or another text is offered, the file was "
        "deleted and re-filed, the registry was cut, m differs, a text is "
        "filed behind an existing result, the offered panel / ruler / arm / "
        "scored slot / lane / base is not the filed one, a scored arm is "
        "re-scored on a different book or seed, a registration names no "
        "book or two scored arms, a filing does not say which LOAO count "
        "carries the above-half line (in its spec AND in its text), the "
        "canonical registry is entered without a head pin or under a STALE "
        "one (a head taken BEFORE this registration's own line — which "
        "leaves amend-after-look invisible), or when the WHOLE DIRECTORY was "
        "wiped and re-filed and the caller holds the pin.  It also fails if "
        "a pin taken AT or AFTER a registration's line stops opening its "
        "door.  A wipe is visible ONLY against an externally recorded head: "
        "without a pin it is ACCEPTED, and the real leg demonstrates exactly "
        "that, prints it, and asserts the head moved.",
        [("score() with NO registration filed", _scenario(p_none)),
         ("the filed TEXT edited after filing", _scenario(p_tamper_text)),
         ("the PRIOR forged and both in-file shas recomputed",
          _scenario(p_forge_prior)),
         ("the BOOK SPEC forged (ruler re-pointed) and both in-file shas "
          "recomputed", _scenario(p_forge_spec)),
         ("the caller's text is not the filed text", _scenario(
             _file, sc(text=_TXT + " (sharpened after the look)"))),
         ("NO text offered at the scorer (text=None)", _scenario(
             _file, sc(text=None))),
         ("file deleted, then RE-FILED with new text", _scenario(
             p_refile, lambda root, c: (lambda: TP.register(
                 "P-SYN-1", _TXT_LATER, 45,
                 root=root, arms=_arms12())))),
         ("AMENDED in place (same id, new text)", _scenario(
             _file, lambda root, c: (lambda: TP.register(
                 "P-SYN-1", _TXT_LATER, 45,
                 root=root, arms=_arms12())))),
         ("AMENDED in place (same id, SAME text, another PANEL in the book "
          "spec)", _scenario(
             _file, lambda root, c: (lambda: TP.register(
                 "P-SYN-1", _TXT, 45, root=root,
                 arms=[TP.arm_spec("P-SYN-1 vs zero", SYN12[:6],
                                   "vs_zero", loao_line=_LL,
                                   era=_ERA)])))),
         ("the registry's first line cut out", _scenario(p_registry_cut)),
         ("filed under m=5, scored under the contract's m=6",
          _scenario(p_wrong_m)),
         ("a text filed BEHIND an existing result", _scenario(
             p_scored_first, lambda root, c: (lambda: TP.register(
                 "P-SYN-9", "text after result." + _CL, 45, root=root,
                 arms=_arms12("P-SYN-9 vs zero"))))),
         ("the WHOLE DIRECTORY wiped after the look and re-filed SHARPER — "
          "scored by a caller holding the pin taken at filing", _scenario(
              p_wipe, lambda root, pin: (lambda: TP.score(
                  "P-SYN-1", _TXT_SHARP, book, SYN12, root=root,
                  head_of_record=pin)))),
         ("a pin that names a line the chain does not have", _scenario(
             _file, sc(head_of_record=(7, "0" * 64)))),
         ("a STALE PIN: the head taken at the FIRST filing, offered for a "
          "registration filed AFTER it", _scenario(
              p_stale, lambda root, pin: (lambda: TP.score(
                  "P-SYN-1", _TXT, book, SYN12, root=root,
                  head_of_record=pin)))),
         ("AMEND BEHIND THE PIN: file, look, cut the line, re-file SHARPER, "
          "score under the pin taken before it", _scenario(
              p_amend_behind_pin, lambda root, pin: (lambda: TP.score(
                  "P-SYN-1", _TXT_SHARP, book, SYN12, root=root,
                  head_of_record=pin)))),
         ("the CANONICAL registry entered with a STALE pin",
          b_stale_canonical),
         ("a filing whose arms do not say WHICH LOAO COUNT carries the line",
          _scenario(lambda root: None, lambda root, c: (lambda: TP.register(
              "P-SYN-1", _TXT, 45, root=root, arms=[TP.arm_spec(
                  "P-SYN-1 vs zero", SYN12, "vs_zero", era=_ERA)])))),
         ("a filing whose book spec says 'excl_zero_campaign' while its TEXT "
          "states the lineage count", _scenario(
              lambda root: None, lambda root, c: (lambda: TP.register(
                  "P-SYN-1", _TXT, 45, root=root,
                  arms=_arms12(loao_line="excl_zero_campaign"))))),
         ("a filing whose TEXT states NO LOAO clause at all", _scenario(
             lambda root: None, lambda root, c: (lambda: TP.register(
                 "P-SYN-1", "a claim that never says which count carries "
                            "the line.", 45, root=root, arms=_arms12())))),
         ("a filed record whose arms name NO LOAO count (filed before the "
          "law), scored", _scenario(p_no_loao_line)),
         ("the CANONICAL registry entered with NO head_of_record",
          _scenario(_file, _canonical(lambda root: TP.score(
              "P-SYN-1", _TXT, book, SYN12, root=root)))),
         ("RIGHT REGISTRY, WRONG BOOK: a 3-asset foreign panel scored "
          "under P-SYN-1", _scenario(_file, sc(
              book=[t for t in book if t.symbol in SYN12[:3]],
              panel=SYN12[:3]))),
         ("a vs_zero registration scored TWO-SAMPLE against a base",
          _scenario(_file, sc(base=base0, ruler="two_sample"))),
         ("an arm the registration never filed", _scenario(
             _file, sc(arm="P-SYN-1 long side only"))),
         ("the SCORED arm offered as report-only (scored_in_family=False)",
          _scenario(_file, sc(arm="P-SYN-1 vs zero",
                              scored_in_family=False))),
         ("a report-only arm offered as THE scored arm", _scenario(
             p_two_arm, sc(arm="P-SYN-1 view", panel=SYN12[:6],
                           book=[t for t in book if t.symbol in SYN12[:6]]))),
         ("a campaign of an UNFILED lane inside the book", _scenario(
             _file, sc(book=book + _syn(SYN12[0], [9.0], lane="spring",
                                        t0=999)))),
         ("an already-scored arm RE-SCORED on a DIFFERENT book (the winners "
          "only)", _scenario(p_scored, sc(
              book=[t for t in book if t.net_r > -0.5]))),
         ("an already-scored arm RE-SCORED under another SEED", _scenario(
             p_scored, sc(seed=12345))),
         ("a registration that names NO book (arms omitted)", _scenario(
             lambda root: None, lambda root, c: (lambda: TP.register(
                 "P-SYN-1", _TXT, 45, root=root)))),
         ("a registration with TWO scored arms", _scenario(
             lambda root: None, lambda root, c: (lambda: TP.register(
                 "P-SYN-1", _TXT, 45, root=root, arms=[
                     TP.arm_spec("a", SYN12, "vs_zero", loao_line=_LL,
                                 era=_ERA),
                     TP.arm_spec("b", SYN12[:6], "vs_zero", loao_line=_LL,
                                 era=_ERA)])))),
         ("an arm dict EDITED BY HAND after arm_spec built it (panel_name "
          "left saying the old panel)", _scenario(
              lambda root: None, lambda root, c: (lambda: TP.register(
                  "P-SYN-1", _TXT, 45, root=root, arms=[dict(
                      _arms12()[0], panel=list(SYN12[:6]))])))),
         ("MUTATION: score() stops forwarding its seed to loao_n",
          mutated(TP, "loao_n", loao_drops_seed, checks))], checks)


# ═══════════════ F-SCORE · the three rulers + the headline, on SYNTHETIC books
def f_score() -> bool:
    B = books()
    # A "vs card v6" arm is scored ONLY against a Book that says it IS card
    # v6 on the arm's panel.  These journals are SYNTHETIC, so the fixture
    # writes that provenance by hand — and says so here, where a grep finds it.
    v6_on_syn12 = {"ride": TP.CONTROL_RIDE, "panel": list(SYN12),
                   "lo_ms": 0, "hi_ms": 1}
    base_trades = [t for s in SYN12 for t in _syn(s, [0.0] * 10)]
    base = TP.Book(base_trades, spec=v6_on_syn12)
    same_set = [t for s in SYN12 for t in _syn(s, [1.0] * 10)]
    grown = [t for s in SYN12 for t in _syn(s, [1.0] * 12)]
    txt = ("P-SYN-2 [40%] a SYNTHETIC arm vs a SYNTHETIC base. Fixture only."
           + _CL)
    knob_ride = TP.ride_spec(T8.Card(name="x", trail_min_advance_atr=0.0),
                             T9.V6_ROLES)

    def _try(filed_ruler, **kw):
        def leg():
            with tempfile.TemporaryDirectory(prefix="f-score-") as td:
                TP.register("P-SYN-2", txt, 40, root=Path(td),
                            arms=_arms12("P-SYN-2 arm", filed_ruler))
                r, why = refused(lambda: TP.score(
                    "P-SYN-2", txt, panel=SYN12, root=Path(td), **kw))
                return (not r), why
        return leg

    def b_throwaway_in_family():
        with tempfile.TemporaryDirectory(prefix="f-score-") as td:
            TP.register("P-SYN-4", txt, 40, root=Path(td),
                        arms=_arms12("P-SYN-4 vs zero"))
            row = TP.score("P-SYN-4", txt, grown, SYN12, root=Path(td))
            r, why = refused(lambda: TP.finish_family([row]))
            return (not r), why

    def real():
        ok, lines = True, []
        with tempfile.TemporaryDirectory(prefix="f-score-") as td:
            root = Path(td)
            for rid, rul in (("P-SYN-2", "two_sample"),
                             ("P-SYN-3", "set_change"),
                             ("P-SYN-4", "vs_zero")):
                TP.register(rid, txt.replace("P-SYN-2", rid), 40, root=root,
                            arms=_arms12(f"{rid} arm", rul))
            r2 = TP.score("P-SYN-2", txt, grown, SYN12, base=base,
                          ruler="two_sample", root=root)
            r3 = TP.score("P-SYN-3", txt.replace("P-SYN-2", "P-SYN-3"),
                          same_set, SYN12, base=base, ruler="set_change",
                          root=root)
            r4_ = TP.score("P-SYN-4", txt.replace("P-SYN-2", "P-SYN-4"),
                           grown, SYN12, ruler="vs_zero", root=root)
            g = (r2["ruler_is_two_sample"] and r2["set_changes_measured"]
                 and (r2["ci_lo"], r2["ci_hi"]) == (1.0, 1.0)
                 and r2["paired_n"] == 120
                 and r2["unpaired_cell_n"] == 24
                 and r2["whole_book_difference_r"] == 144.0
                 and r2["loao_line"] == "12/12 above"
                 and r2["loao_mode"] == "two_sample"
                 and r2["verdict"] == "SUPPORTED")
            ok &= g
            lines.append(f"[{'OK ' if g else 'BAD'}] two_sample (commissioned)"
                         f": 24 extra campaigns -> set change MEASURED True, "
                         f"CI [{r2['ci_lo']}, {r2['ci_hi']}], paired_n 120, "
                         f"whole-book +144 R, LOAO {r2['loao_line']} on the "
                         f"two-sample ruler")
            g = ((not r3["ruler_is_two_sample"])
                 and r3["set_changes_measured"] is False
                 and r3["ruler"].startswith("PAIRED")
                 and (r3["ci_lo"], r3["ci_hi"]) == (1.0, 1.0)
                 and r3["paired_delta_expectancy_r"] == 1.0
                 and r3["loao_mode"] == "paired")
            ok &= g
            lines.append(f"[{'OK ' if g else 'BAD'}] set_change: identical "
                         f"campaign set -> PAIRED by the set-change law, "
                         f"delta exactly 1.0, D15 paired delta "
                         f"{r3['paired_delta_expectancy_r']}")
            g = (r4_["ruler"].startswith("VS ZERO")
                 and r4_["paired_delta_expectancy_r"] is None
                 and "DEGENERATE" in r4_["d15_note"]
                 and r4_["ear_expectancy_r"] == 1.0
                 and r4_["loao_mode"] == "vs_zero")
            ok &= g
            lines.append(f"[{'OK ' if g else 'BAD'}] vs_zero: D15 trio "
                         f"printed None WITH its reason; EAR co-headline "
                         f"{r4_['ear_expectancy_r']} [{r4_['ear_ci_lo']}, "
                         f"{r4_['ear_ci_hi']}] beside the raw verdict")
            g = (r2["arm"] == "P-SYN-2 arm" and r2["arm_base"] == "card-v6"
                 and r4_["arm_base"] == "zero"
                 and r2["ear_n_finite_draws"] == TP.N_BOOT
                 and (r2["sens_ear_ci_lo"], r2["sens_ear_ci_hi"]) == (1.0, 1.0)
                 and r2["base_sha256"] is not None
                 and r4_["base_sha256"] is None)
            ok &= g
            lines.append(f"[{'OK ' if g else 'BAD'}] every row names its "
                         f"FILED arm and base ('{r2['arm_base']}' / "
                         f"'{r4_['arm_base']}'), binds its book and base "
                         f"shas, counts the finite EAR draws "
                         f"({r2['ear_n_finite_draws']}/{TP.N_BOOT}) and "
                         f"carries the L8 echo of the EAR CI too")
            fam = TP.finish_family([r2, r3, r4_], canonical_only=False)
            put, W, K, SK = TP.make_put(root / "out", B["meta"])
            put(fam, "registrations", ["registration", "arm"])
            put(TP.registration_table(root), "registration_text",
                ["registration"])
            hd = TP.headline_n([t for t in grown if t.symbol != SYN12[11]],
                               "syn", SYN12)
            put(hd, "headline", ["label", "group", "key", "aggregation"])
            g2, kl = TP.check_keys(root / "out", {"keys": K})
            z = hd[(hd["group"] == "asset") & (hd["key"] == SYN12[11])]
            g = (g2 and len(fam) == 3 and len(z) == 2
                 and set(z["n"]) == {0}
                 and len(hd[hd["group"] == "asset"]) == 24
                 and list(fam["fdr_bar_q_over_m"].unique()) == [0.016667]
                 and int(fam["fdr_m_tests_actually_run"].iloc[0]) == 3)
            ok &= g
            lines.append(f"[{'OK ' if g else 'BAD'}] the rows survive the "
                         f"trip to disk: finish_family -> make_put -> "
                         f"parquet -> check_keys GREEN (9 as-of columns); "
                         f"headline_n prints ALL 12 declared assets, the "
                         f"n=0 one included ({len(z)} rows, n={set(z['n'])}); "
                         f"3 of 6 run, bar still 0.016667")
        return ok, lines
    return prove(
        "F-SCORE", "score(): three rulers with hand answers; the rows file "
        "cleanly; the headline is WHOLE",
        "a commissioned two-sample arm that shares the whole campaign set is "
        "scored anyway; vs_zero is given a base (or a twin ruler is not); an "
        "empty book is scored; a 'vs card v6' arm is scored against a bare "
        "list, against v6 on ANOTHER panel, or against a card with a moved "
        "knob; a throwaway-registry row fills a slot in m; a hand-built +1 "
        "arm is not CI [1, 1]; or a declared asset with no campaigns "
        "vanishes from the headline.",
        [("ruler='two_sample' on an arm sharing the WHOLE campaign set",
          _try("two_sample", book=same_set, base=base, ruler="two_sample")),
         ("ruler='vs_zero' handed a base book",
          _try("vs_zero", book=same_set, base=base, ruler="vs_zero")),
         ("ruler='set_change' with NO base book",
          _try("set_change", book=same_set, base=None, ruler="set_change")),
         ("an EMPTY book", _try("vs_zero", book=[], base=None,
                                ruler="vs_zero")),
         ("a 'vs card v6' arm scored against a BARE LIST (no provenance)",
          _try("two_sample", book=grown, base=base_trades,
               ruler="two_sample")),
         ("a 'vs card v6' arm scored against card v6 on ANOTHER panel",
          _try("two_sample", book=grown, ruler="two_sample",
               base=TP.Book(base_trades, spec=dict(
                   v6_on_syn12, panel=list(SYN12[:6]))))),
         ("a 'vs card v6' arm scored against a base with a MOVED KNOB",
          _try("two_sample", book=grown, ruler="two_sample",
               base=TP.Book(base_trades, spec=dict(
                   v6_on_syn12, ride=knob_ride)))),
         ("a row scored under a THROWAWAY registry handed to finish_family "
          "as a slot in m", b_throwaway_in_family)], real)


# ═══════ F-VERDICT · the verdict law and the set-change law, on NOISY books
# [TC10 review r2, BLOCKING 2] Five fatal mutants used to pass every leg of
# this suite: `_verdict` := always SUPPORTED, `_verdict` := point > 0, the two
# two-sample rulers dropping their seed, and set_change keeping the PAIRED
# interval on a CHANGED set.  Cause: every known answer was the degenerate +1
# book, whose CI is [1, 1] and whose verdict is SUPPORTED under any law.  This
# fixture is the answer: NOISY books whose intervals are not points, hand
# answers that differ under each wrong, and a MUTATION leg for each.
_NB_FIX = 1000      # bootstrap draws for the synthetic legs (4000 in anger)


def f_verdict() -> bool:
    N = noisy()
    txt = "P-SYN-V [40%] SYNTHETIC noisy arms, fixture only." + _CL

    def _score(root, rid, book, base=None, ruler="vs_zero"):
        TP.register(rid, txt, 40, root=root,
                    arms=_arms12(f"{rid} arm", ruler))
        return TP.score(rid, txt, book, SYN12, base=base, ruler=ruler,
                        root=root, n_boot=_NB_FIX)

    def checks():
        ok, lines = True, []
        # ── (1) THE LAW ITSELF, hand answers — and it is the LINEAGE's law.
        hand = [({"lo": 0.1, "hi": 0.5, "point": 0.3}, "SUPPORTED"),
                ({"lo": 1e-09, "hi": 2.0, "point": 1.0}, "SUPPORTED"),
                ({"lo": 0.0, "hi": 0.0, "point": 0.0}, "NOT SUPPORTED"),
                ({"lo": 0.0, "hi": 9.0, "point": 4.0}, "NOT SUPPORTED"),
                ({"lo": -1e-09, "hi": 9.0, "point": 4.0}, "NOT SUPPORTED"),
                ({"lo": None, "hi": None, "point": None}, "NOT SUPPORTED"),
                ({"lo": -5.0, "hi": -1.0, "point": -3.0}, "NOT SUPPORTED")]
        got = [TP._verdict(c) for c, _ in hand]
        law = 'good = bool(ci["lo"] is not None and ci["lo"] > 0)'
        g = got == [w for _, w in hand] and law in inspect.getsource(T8.score)
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] _verdict hand answers "
                     f"(lo, hi) -> verdict: [0.1,0.5] and [1e-9,2] SUPPORTED; "
                     f"[0,0], [0,9], [-1e-9,9], [None], [-5,-1] NOT — and "
                     f"the law reproduced is tierc8.score's own line `{law}`, "
                     f"found in its source")
        with tempfile.TemporaryDirectory(prefix="f-verdict-") as td:
            root = Path(td)
            # ── (2) THREE NOISY vs-zero arms: above, straddling, below.
            up = _score(root, "P-SYN-V1", N["winning"])
            st = _score(root, "P-SYN-V2", N["straddle"])
            lo_ = _score(root, "P-SYN-V3", N["losing"])
            g = (up["verdict"] == "SUPPORTED" and up["ci_lo"] > 0
                 and up["loao_line"] == "12/12 above")
            ok &= g
            lines.append(f"[{'OK ' if g else 'BAD'}] mean +1.0 sd 0.3: CI "
                         f"[{up['ci_lo']}, {up['ci_hi']}] wholly above zero "
                         f"-> {up['verdict']}, LOAO {up['loao_line']}")
            g = (st["verdict"] == "NOT SUPPORTED"
                 and st["ci_lo"] < 0 < st["ci_hi"]
                 and st["expectancy_r"] > 0
                 and st["loao_clears_above_half"] is False)
            ok &= g
            lines.append(f"[{'OK ' if g else 'BAD'}] THE STRADDLING ARM — "
                         f"point {st['expectancy_r']} R ABOVE zero, interval "
                         f"[{st['ci_lo']}, {st['ci_hi']}] across it: "
                         f"{st['verdict']} (a verdict that read the POINT "
                         f"would say SUPPORTED), LOAO {st['loao_line']}")
            g = (lo_["verdict"] == "NOT SUPPORTED" and lo_["ci_hi"] < 0
                 and lo_["p_one_sided"] == 1.0
                 and lo_["loao_line"] == "0/12 above, 12/12 BELOW"
                 and lo_["loao_clears_above_half"] is False
                 and lo_["ear_verdict_would_be"] == "NOT SUPPORTED")
            fam = TP.finish_family([up, st, lo_], canonical_only=False)
            bh = dict(zip(fam["registration"], fam["clears_bh_bar"]))
            g &= bh["P-SYN-V3"] is False
            ok &= g
            lines.append(f"[{'OK ' if g else 'BAD'}] THE LOSING ARM — mean "
                         f"-1.0: CI [{lo_['ci_lo']}, {lo_['ci_hi']}] wholly "
                         f"BELOW zero, p {lo_['p_one_sided']}, "
                         f"{lo_['verdict']}, LOAO '{lo_['loao_line']}', "
                         f"clears_bh_bar {bh['P-SYN-V3']}")
            # ── (3) THE SET-CHANGE LAW, on journals with KNOWN overlap.
            sm = _score(root, "P-SYN-V4", N["straddle"], N["base_book"],
                        "set_change")
            gr = _score(root, "P-SYN-V5", N["grown"], N["base_book"],
                        "set_change")
            sh = _score(root, "P-SYN-V6", N["shrunk"], N["base_book"],
                        "set_change")
            # ON A PERFECTLY PAIRED BOOK THE TWO INTERVALS COINCIDE BY
            # CONSTRUCTION — the same cluster draw enters both books and
            # mean(A) - mean(B) over the drawn clusters IS the mean of the
            # per-key deltas.  So on THIS row the set-change law is visible
            # in the ruler it declares, not in the digits; the CHANGED-set
            # rows below carry the digits.  (Which is exactly why the older
            # degenerate legs could not see the law at all.)
            g = (sm["set_changes_measured"] is False
                 and sm["ruler_is_two_sample"] is False
                 and sm["ruler"].startswith("PAIRED")
                 and sm["paired_n"] == N["n_base"] == 240
                 and (sm["ci_lo"], sm["ci_hi"])
                 == (sm["paired_ci_lo"], sm["paired_ci_hi"])
                 == (sm["two_sample_ci_lo"], sm["two_sample_ci_hi"])
                 and sm["loao_mode"] == "paired")
            ok &= g
            lines.append(f"[{'OK ' if g else 'BAD'}] SAME SET (240 keys, 240 "
                         f"paired): the set did NOT change -> the row "
                         f"declares PAIRED ({sm['ruler'][:34]}...) and its "
                         f"LOAO panels ride the paired ruler; the paired and "
                         f"two-sample intervals coincide here "
                         f"([{sm['ci_lo']}, {sm['ci_hi']}]) BY CONSTRUCTION "
                         f"— one cluster draw, identical keys")
            for r_, nm, n_, pn in ((gr, "GROWN", N["n_grown"], 240),
                                   (sh, "SHRUNK", N["n_shrunk"], 180)):
                g = (r_["set_changes_measured"] is True
                     and r_["ruler_is_two_sample"] is True
                     and r_["ruler"].startswith("TWO-SAMPLE")
                     and r_["n"] == n_ and r_["paired_n"] == pn
                     and (r_["ci_lo"], r_["ci_hi"])
                     == (r_["two_sample_ci_lo"], r_["two_sample_ci_hi"])
                     and (r_["ci_lo"], r_["ci_hi"])
                     != (r_["paired_ci_lo"], r_["paired_ci_hi"])
                     and r_["loao_mode"] == "two_sample")
                ok &= g
                lines.append(f"[{'OK ' if g else 'BAD'}] {nm} SET (n {r_['n']}"
                             f" vs base 240, {r_['paired_n']} paired): the "
                             f"set CHANGED -> TWO-SAMPLE, the row's CI "
                             f"[{r_['ci_lo']}, {r_['ci_hi']}] IS the "
                             f"two-sample interval, NOT the paired "
                             f"[{r_['paired_ci_lo']}, {r_['paired_ci_hi']}] "
                             f"— and the LOAO panels ride the SAME ruler")
        return ok, lines

    def _always(ci):
        return "SUPPORTED"

    def _by_point(ci):
        return ("SUPPORTED" if (ci.get("point") is not None
                                and ci["point"] > 0) else "NOT SUPPORTED")

    def _paired_always(ruler, changes):
        return bool(ruler == "two_sample")      # set_change keeps PAIRED

    def _two_always(ruler, changes):
        return bool(ruler != "vs_zero")         # set_change always TWO-SAMPLE

    return prove(
        "F-VERDICT", "the verdict law (tierc8's, reproduced) and the "
        "set-change law — known answers on NOISY books, each with its "
        "mutation",
        "_verdict says SUPPORTED on an interval whose lower bound is not "
        "strictly above zero (or reads the point, the upper bound or p); the "
        "law in tierc8.score is no longer the one reproduced here; a "
        "set_change arm keeps the PAIRED interval although the campaign set "
        "changed, or takes the two-sample interval although it did not; the "
        "LOAO panels are scored by a different ruler than the headline; or "
        "the losing arm clears the BH bar.  Bootstrap draws here are "
        f"{_NB_FIX} (4000 in anger) — the claim is the LAW, not the digit.",
        [("MUTATION: _verdict := 'SUPPORTED' for every CI",
          mutated(TP, "_verdict", _always, checks)),
         ("MUTATION: _verdict := point > 0 (the CI ignored)",
          mutated(TP, "_verdict", _by_point, checks)),
         ("MUTATION: set_change keeps the PAIRED CI on a CHANGED set "
          "(tierc8's law inverted)",
          mutated(TP, "_set_change_law", _paired_always, checks)),
         ("MUTATION: set_change takes the TWO-SAMPLE CI on an UNCHANGED set",
          mutated(TP, "_set_change_law", _two_always, checks))], checks)


# ═══════════════════ F-ERA · the corridor, CUT — and the cut is REGISTERED
def f_era() -> bool:
    cut = TP.ERA_CUT_MS
    post = [t for s in SYN12 for t in _syn(s, [1.0] * 10, t0=cut + 1)]
    pre = [t for s in SYN12 for t in _syn(s, [1.0] * 10, t0=cut - 20)]
    txt = "P-SYN-E [30%] a SYNTHETIC era arm, fixture only." + _CL
    r912 = T9.Roles(name="trigger-9/12", trg_f=9, trg_s=12)

    def _file(root, era="holdout", **kw):
        return TP.register("P-SYN-E", txt, 30, root=root,
                           arms=_arms12("P-SYN-E arm", era=era, **kw))

    def _try(prepare, act):
        def leg():
            with tempfile.TemporaryDirectory(prefix="f-era-") as td:
                root = Path(td)
                carry = prepare(root)
                r, why = refused(act(root, carry))
                return (not r), why
        return leg

    def b_unknown_era():
        r, why = refused(lambda: TP.arm_spec("x", SYN12, "vs_zero",
                                             loao_line=_LL, era="2024H2"))
        return (not r), why

    def p_no_era(root):
        """A record filed BEFORE this law existed: the era law is lifted OFF
        the module for the filing only, so the file, its shas and the chain
        are all consistent and the ONLY thing wrong is the missing era."""
        old = TP._require_era
        TP._require_era = lambda spec, where: {}
        try:
            TP.register("P-SYN-E", txt, 30, root=root, arms=[TP.arm_spec(
                "P-SYN-E arm", SYN12, "vs_zero", loao_line=_LL)])
        finally:
            TP._require_era = old

    def b_run_cell_full_corridor():
        """A run_cell_n arm filed for the HOLDOUT era, handed the WHOLE
        corridor.  The replay is stubbed: if the gate let this through, the
        stub — not a bar — would be what ran."""
        B = books()
        with tempfile.TemporaryDirectory(prefix="f-era-") as td:
            root = Path(td)
            TP.register("X-ERA-1", txt, 30, root=root, arms=[TP.arm_spec(
                "X-ERA-1 holdout", TP.CLASSIC5, "vs_zero",
                card=TP.CONTROL_CARD, roles=r912, loao_line=_LL,
                era="holdout")])
            calls, old = [], T9.replay9
            T9.replay9 = lambda s_, *a, **k: (calls.append(s_), ([], []))[1]
            try:
                r, why = refused(lambda: TP.run_cell_n(
                    TP.CONTROL_CARD, r912, TP.CLASSIC5, B["lo"], B["hi"],
                    reg_id="X-ERA-1", text=txt, reg_root=root))
            finally:
                T9.replay9 = old
        return ((not r) or bool(calls)), (f"refused={r}, replay calls="
                                          f"{len(calls)} — {why[:120]}")

    def b_external_book_pre_cut():
        with tempfile.TemporaryDirectory(prefix="f-era-") as td:
            root = Path(td)
            rec = _file(root, lanes=("brk-s1",))
            gate = TP.require_arm("P-SYN-E", txt, "P-SYN-E arm", SYN12,
                                  lanes=("brk-s1",), root=root,
                                  head_of_record=(rec["registry_len"],
                                                  rec["registry_head"]))
            pre_l = [t for s in SYN12
                     for t in _syn(s, [1.0] * 3, lane="brk-s1", t0=cut - 5)]
            r, why = refused(lambda: TP.external_book(pre_l, gate))
        return (not r), why

    def checks():
        ok, lines = True, []
        # ── (1) THE WINDOWS, hand answers.
        w = {e: TP.era_window(e) for e in TP.ERAS}
        g = (TP.ERAS == ("full", "tuning", "holdout")
             and TP.ERA_CUT_ISO == "2024-06-30T23:59:59Z"
             and w["full"] == (None, None)
             and w["tuning"] == (None, cut)
             and w["holdout"] == (cut + 1, None)
             and TP.in_era(cut, "tuning") and not TP.in_era(cut, "holdout")
             and TP.in_era(cut + 1, "holdout")
             and not TP.in_era(cut + 1, "tuning")
             and TP.in_era(cut, "full") and TP.in_era(0, "full"))
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] the R1 cut {TP.ERA_CUT_ISO} "
                     f"= {cut} ms: the cut INSTANT is the last of the tuning "
                     f"era and is NOT in the holdout era; cut + 1 ms is in "
                     f"the holdout era and not in the tuning era; 'full' "
                     f"holds both")
        # ── (2) THE CORRIDOR, CUT — on the control panel's real bars.
        lo, hi, m = TP.corridor_n(TP.CLASSIC5)
        hl, hh, mh = TP.corridor_era(TP.CLASSIC5, "holdout")
        tl, th, mt = TP.corridor_era(TP.CLASSIC5, "tuning")
        fl, fh, mf = TP.corridor_era(TP.CLASSIC5, "full")
        g = ((fl, fh) == (lo, hi)
             and hl == TP._iso_ms("2024-07-01T00:00:00Z") and hh == hi
             and th + 1 == TP._iso_ms("2024-06-30T20:00:00Z") and tl == lo
             and mh["era_bars_dropped_head"] == (hl - lo) // MS_4H
             and mh["era_bars_dropped_tail"] == 0
             and mt["era_bars_dropped_head"] == 0
             and mt["era_bars_dropped_tail"] == (hi - th) // MS_4H
             and mh["last_closed_4h_close"] == m["last_closed_4h_close"]
             and "R1" in mh["era_note"])
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] corridor_era(CLASSIC5): "
                     f"'full' == corridor_n exactly; 'holdout' starts at the "
                     f"first 4h bar OPENING after the cut "
                     f"({mh['era_window_lo']}, {mh['era_bars_dropped_head']} "
                     f"bars dropped) and keeps the corridor end; 'tuning' "
                     f"ends at the last 4h bar CLOSING at or before it "
                     f"({mt['era_window_hi']}, "
                     f"{mt['era_bars_dropped_tail']} dropped) — and BOTH "
                     f"keep the corridor's own as-of stamp "
                     f"{mh['last_closed_4h_close']}")
        # ── (3) THE ERA IS THE FILING'S, and the campaigns are held to it.
        with tempfile.TemporaryDirectory(prefix="f-era-") as td:
            root = Path(td)
            rec = _file(root, "holdout")
            pin = (rec["registry_len"], rec["registry_head"])
            row = TP.score("P-SYN-E", txt, post, SYN12, root=root,
                           head_of_record=pin, era="holdout",
                           n_boot=_NB_FIX)
            g = (row["arm_era"] == "holdout"
                 and row["era_window_lo_ms"] == cut + 1
                 and row["era_window_hi_ms"] is None
                 and row["era_first_entry_ms"] > cut
                 and row["era_cut_iso"] == TP.ERA_CUT_ISO
                 and "out of sample" in row["era_note"]
                 and row["n"] == 120)
            ok &= g
            lines.append(f"[{'OK ' if g else 'BAD'}] a HOLDOUT-filed arm "
                         f"scored on 120 post-cut campaigns: the row carries "
                         f"the era of record ({row['arm_era']}), its window "
                         f"({row['era_window_lo_ms']}, "
                         f"{row['era_window_hi_ms']}) and the first entry it "
                         f"measured ({row['era_first_entry_ms']} > {cut})")
        with tempfile.TemporaryDirectory(prefix="f-era-") as td:
            root = Path(td)
            _file(root, "full")
            r2 = TP.score("P-SYN-E", txt, pre + post, SYN12, root=root,
                          n_boot=_NB_FIX)
            g = r2["arm_era"] == "full" and r2["n"] == 240 \
                and r2["era_window_lo_ms"] is None
            ok &= g
            lines.append(f"[{'OK ' if g else 'BAD'}] the same campaigns "
                         f"under a 'full'-filed arm ride: the law REFUSES "
                         f"the era that was not registered, it does not "
                         f"refuse campaigns ({r2['n']} scored)")
        # ── (4) THE EXTERNAL DOOR carries the era into the Book.
        with tempfile.TemporaryDirectory(prefix="f-era-") as td:
            root = Path(td)
            rec = _file(root, "holdout", lanes=("brk-s1",))
            pin = (rec["registry_len"], rec["registry_head"])
            gate = TP.require_arm("P-SYN-E", txt, "P-SYN-E arm", SYN12,
                                  lanes=("brk-s1",), root=root,
                                  head_of_record=pin)
            tr = [t for s in SYN12
                  for t in _syn(s, [1.0] * 3, lane="brk-s1", t0=cut + 1)]
            bk = TP.external_book(tr, gate, cut + 1, cut + 9)
            g = (gate["era"] == "holdout"
                 and gate["era_window"] == [cut + 1, None]
                 and bk.spec["era"] == "holdout" and len(bk) == 36)
            ok &= g
            lines.append(f"[{'OK ' if g else 'BAD'}] require_arm hands the "
                         f"external runner its era ({gate['era']}, window "
                         f"{gate['era_window']}) and external_book stamps it "
                         f"on the Book — so score() reads it back from the "
                         f"journal, not from the caller")
        return ok, lines

    return prove(
        "F-ERA", "the ERA a lane rides is REGISTERED [R1]: corridor_era, and "
        "both doors hold the window and every campaign against the filing",
        "an arm is filed without an era or with an unknown one; a record "
        "that names no era opens a door; a book whose campaigns enter "
        "outside the filed era is scored; a caller's era overrides the filed "
        "one; a run_cell_n arm filed for the holdout era rides the whole "
        "corridor; external_book accepts a pre-cut campaign under a holdout "
        "gate; or the era functions stop distinguishing the eras.",
        [("an arm_spec with NO era (register refuses the filing)",
          _try(lambda root: None, lambda root, c: (lambda: TP.register(
              "P-SYN-E", txt, 30, root=root, arms=[TP.arm_spec(
                  "P-SYN-E arm", SYN12, "vs_zero", loao_line=_LL)])))),
         ("an UNKNOWN era at arm_spec ('2024H2')", b_unknown_era),
         ("a filed record whose arms name NO era (filed before the law), "
          "scored", _try(p_no_era, lambda root, c: (lambda: TP.score(
              "P-SYN-E", txt, post, SYN12, root=root, n_boot=_NB_FIX)))),
         ("a HOLDOUT-filed arm scored on PRE-CUT campaigns",
          _try(_file, lambda root, c: (lambda: TP.score(
              "P-SYN-E", txt, pre, SYN12, root=root, n_boot=_NB_FIX)))),
         ("a HOLDOUT-filed arm scored on a MIXED book (one pre-cut campaign "
          "among 120)",
          _try(_file, lambda root, c: (lambda: TP.score(
              "P-SYN-E", txt, post + pre[:1], SYN12, root=root,
              n_boot=_NB_FIX)))),
         ("a TUNING-filed arm scored on POST-cut campaigns",
          _try(lambda root: _file(root, "tuning"),
               lambda root, c: (lambda: TP.score(
                   "P-SYN-E", txt, post, SYN12, root=root, n_boot=_NB_FIX)))),
         ("the caller offers era='full' at a HOLDOUT-filed arm",
          _try(_file, lambda root, c: (lambda: TP.score(
              "P-SYN-E", txt, post, SYN12, root=root, era="full",
              n_boot=_NB_FIX)))),
         ("a run_cell_n arm filed for the HOLDOUT era handed the WHOLE "
          "corridor", b_run_cell_full_corridor),
         ("external_book handed PRE-CUT campaigns through a HOLDOUT gate",
          b_external_book_pre_cut),
         ("MUTATION: in_era := True for every instant",
          mutated(TP, "in_era", lambda ms, era: True, checks)),
         ("MUTATION: era_window := (None, None) for every era",
          mutated(TP, "era_window", lambda era: (None, None), checks))],
        checks)


# ══════════ F-ARM · require_arm — the door the EXTERNAL runners must walk
def f_arm() -> bool:
    txt = "P-SYN-X [35%] a SYNTHETIC external lane, fixture only." + _CL
    lanes = ("brk-s1",)
    trades = [t for s in SYN12 for t in _syn(s, [1.0] * 10, lane="brk-s1")]

    def _file(root, **kw):
        kw.setdefault("lanes", lanes)
        return TP.register("P-SYN-X", txt, 35, root=root,
                           arms=_arms12("P-SYN-X arm", **kw))

    def _pin(rec):
        return (rec["registry_len"], rec["registry_head"])

    def _try(prepare, act):
        def leg():
            with tempfile.TemporaryDirectory(prefix="f-arm-") as td:
                root = Path(td)
                carry = prepare(root)
                r, why = refused(act(root, carry))
                return (not r), why
        return leg

    def _gate(root, carry, **kw):
        kw.setdefault("lanes", lanes)
        kw.setdefault("head_of_record", _pin(carry))
        return lambda: TP.require_arm(
            kw.pop("reg_id", "P-SYN-X"), kw.pop("text", txt),
            kw.pop("arm", "P-SYN-X arm"), kw.pop("panel", SYN12),
            root=root, **kw)

    def p_two(root):
        """The registration files BOTH an external arm and a run_cell_n arm
        (P-GEN-1's shape): the external door must open ONLY on the first."""
        return TP.register("P-SYN-X", txt, 35, root=root, arms=[
            TP.arm_spec("P-SYN-X arm", SYN12, "vs_zero", lanes=lanes,
                        loao_line=_LL, era=_ERA),
            TP.arm_spec("P-SYN-X v6 view", SYN12, "vs_zero",
                        scored_in_family=False, card=TP.CONTROL_CARD,
                        roles=T9.V6_ROLES, loao_line=_LL, era=_ERA)])

    def p_stale(root):
        """Pin taken at the FIRST filing; the arm's own filing comes after."""
        a = TP.register("P-SYN-W", txt.replace("P-SYN-X", "P-SYN-W"), 35,
                        root=root, arms=_arms12("P-SYN-W arm", lanes=lanes))
        _file(root)
        return a                        # the STALE pin (line 1, head of A)

    def b_bare_list_canonical():
        """Under the REGISTRY OF RECORD an external arm is scored only on a
        Book that came through the gate.  The throwaway root stands in AS the
        canonical registry; the real REG_DIR is never touched."""
        with tempfile.TemporaryDirectory(prefix="f-arm-") as td:
            root = Path(td)
            rec = _file(root)
            old = TP.REG_DIR
            TP.REG_DIR = root
            try:
                r, why = refused(lambda: TP.score(
                    "P-SYN-X", txt, trades, SYN12, root=root,
                    head_of_record=_pin(rec), n_boot=_NB_FIX))
            finally:
                TP.REG_DIR = old
        return (not r), why

    def checks():
        ok, lines = True, []
        # THE SIGNATURE IS THE CONTRACT with the other builders' runners.
        sig = list(inspect.signature(TP.require_arm).parameters)
        sig2 = list(inspect.signature(TP.external_book).parameters)
        g = (sig == ["reg_id", "text", "arm", "panel", "lanes",
                     "head_of_record", "root", "family_m"]
             and sig2 == ["trades", "gate", "lo_ms", "hi_ms"])
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] the helper's SIGNATURE, "
                     f"pinned for the external runners (tierc10_lanes.py, "
                     f"tierc10_brk.py): require_arm{tuple(sig)} · "
                     f"external_book{tuple(sig2)}")
        with tempfile.TemporaryDirectory(prefix="f-arm-") as td:
            root = Path(td)
            rec = _file(root)
            gate = TP.require_arm("P-SYN-X", txt, "P-SYN-X arm", SYN12,
                                  lanes=lanes, root=root,
                                  head_of_record=_pin(rec))
            g = (gate["runner"] == "external" and gate["arm"] == "P-SYN-X arm"
                 and gate["panel"] == list(SYN12)
                 and gate["lanes"] == list(lanes)
                 and gate["ruler"] == "vs_zero" and gate["base"] == "zero"
                 and gate["era"] == _ERA and gate["loao_line"] == _LL
                 and gate["scored_in_family"] is True
                 and gate["registration_seq"] == rec["seq"]
                 and gate["registration_sha256"] == rec["sha256"]
                 and gate["registry_head_pinned"] is True
                 and gate["registry_pin_covers_seq"] is True)
            ok &= g
            lines.append(f"[{'OK ' if g else 'BAD'}] require_arm returns THE "
                         f"GATE — arm, panel, lanes, ruler {gate['ruler']!r}, "
                         f"base {gate['base']!r}, era {gate['era']!r}, LOAO "
                         f"line {gate['loao_line']!r}, the registration's seq "
                         f"and sha, and the head PIN it verified")
            bk = TP.external_book(trades, gate, 0, 9)
            row = TP.score("P-SYN-X", txt, bk, SYN12, root=root,
                           arm=gate["arm"], head_of_record=_pin(rec),
                           n_boot=_NB_FIX)
            g = (isinstance(bk, TP.Book) and len(bk) == 120
                 and bk.spec["registration"] == "P-SYN-X"
                 and bk.spec["registration_sha256"] == rec["sha256"]
                 and row["arm_runner"] == "external"
                 and row["book_gate_attested"] is True
                 and row["arm_lanes"] == "brk-s1"
                 and row["arm_era"] == _ERA
                 and row["loao_line_of_record"] == _LL)
            ok &= g
            lines.append(f"[{'OK ' if g else 'BAD'}] external_book(trades, "
                         f"gate) -> a Book wearing the gate, and score() "
                         f"reads it back: arm_runner {row['arm_runner']!r}, "
                         f"book_gate_attested {row['book_gate_attested']}, "
                         f"lanes {row['arm_lanes']!r}, era {row['arm_era']!r}")
        return ok, lines

    return prove(
        "F-ARM", "require_arm + external_book — the door the spring, "
        "breakeven and BRK runners (other files) must enter through",
        "require_arm opens for an arm the registration does not file, for a "
        "run_cell_n arm, on another panel, for a lane the filing does not "
        "name, with no text, or under a STALE head pin; external_book "
        "accepts a hand-built gate or a stray symbol; a bare list is scored "
        "as an external arm under the registry of record; or the helper's "
        "name or signature moves under the runners that must call it.",
        [("require_arm for an arm the registration does NOT file",
          _try(_file, lambda root, c: _gate(root, c, arm="P-SYN-X long"))),
         ("require_arm for a RUN_CELL_N arm (ridden by run_cell_n, never by "
          "an external runner)",
          _try(p_two, lambda root, c: _gate(root, c,
                                            arm="P-SYN-X v6 view"))),
         ("require_arm on ANOTHER panel (six of the twelve)",
          _try(_file, lambda root, c: _gate(root, c, panel=SYN12[:6]))),
         ("require_arm for a lane the filing does not name",
          _try(_file, lambda root, c: _gate(root, c,
                                            lanes=("brk-s1", "spring")))),
         ("require_arm emitting NO lane at all",
          _try(_file, lambda root, c: _gate(root, c, lanes=()))),
         ("require_arm with NO text offered (text=None)",
          _try(_file, lambda root, c: _gate(root, c, text=None))),
         ("require_arm under a STALE pin (taken before this registration's "
          "own line)", _try(p_stale, lambda root, c: _gate(root, c))),
         ("external_book handed a HAND-BUILT gate dict",
          _try(_file, lambda root, c: (lambda: TP.external_book(
              trades, {"runner": "external", "registration": "P-SYN-X",
                       "arm": "P-SYN-X arm", "panel": list(SYN12),
                       "lanes": list(lanes), "era": _ERA})))),
         ("external_book handed a journal with a STRAY symbol",
          _try(_file, lambda root, c: (lambda: TP.external_book(
              trades + _syn("SYN99USDT", [1.0], lane="brk-s1"),
              TP.require_arm("P-SYN-X", txt, "P-SYN-X arm", SYN12,
                             lanes=lanes, root=root,
                             head_of_record=_pin(c)))))),
         ("external_book handed a journal carrying an UNFILED lane",
          _try(_file, lambda root, c: (lambda: TP.external_book(
              trades + _syn(SYN12[0], [1.0], lane="spring", t0=900),
              TP.require_arm("P-SYN-X", txt, "P-SYN-X arm", SYN12,
                             lanes=lanes, root=root,
                             head_of_record=_pin(c)))))),
         ("an EXTERNAL arm scored on a BARE LIST under the registry of "
          "record (no gate)", b_bare_list_canonical)], checks)


# ═══════════════════════════════ F-FDR · one fixed bar, m DECLARED [LEAN L7]
def f_fdr() -> bool:
    def _rows(ps, scored=True):
        return [{"registration": f"P-{i}", "arm": "x",
                 "scored_in_family": scored, "p_one_sided": p}
                for i, p in enumerate(ps)]

    def b_seven():
        r, why = refused(lambda: TP.finish_family(_rows([0.01] * 7)))
        return (not r), why

    def b_two_arms():
        rows = _rows([0.01, 0.01])
        rows[1]["registration"] = "P-0"
        r, why = refused(lambda: TP.finish_family(rows))
        return (not r), why

    def b_m_run():
        # the named wrong: bar = q / (tests actually run).  With 3 of the 6
        # run, p = 0.03 would CLEAR 0.10/3; under the declared m it must not.
        d = TP.finish_family(_rows([0.03, 0.03, 0.03]))
        return bool(d["clears_bh_bar"].any()), (
            f"p=0.03 with 3 of 6 run: clears={list(d['clears_bh_bar'])} "
            f"at bar {d['fdr_bar_q_over_m'].iloc[0]}")

    def real():
        rows = _rows([0.016, 0.017, 0.0002, 0.5, 0.0166, 0.0167]) \
            + [dict(_rows([0.9], scored=False)[0], registration="(reference)")]
        d = TP.finish_family(rows)
        got = list(d["clears_bh_bar"])
        want = [True, False, True, False, True, False, None]
        g1 = got == want
        g2 = (d["fdr_bar_q_over_m"].iloc[0] == 0.016667
              and int(d["fdr_m_declared"].iloc[0]) == 6
              and int(d["fdr_m_tests_actually_run"].iloc[0]) == 6
              and TP.FDR_Q is T7.FDR_Q and TP.FDR_Q == 0.10)
        # independence: moving ONE row's p must not move any OTHER row.
        rows2 = [dict(r_) for r_ in rows]
        rows2[3]["p_one_sided"] = 0.0001
        got2 = list(TP.finish_family(rows2)["clears_bh_bar"])
        g3 = [a for k, a in enumerate(got2) if k != 3] == \
             [a for k, a in enumerate(want) if k != 3] and got2[3] is True
        return g1 and g2 and g3, [
            f"[{'OK ' if g1 else 'BAD'}] p = 0.016 / 0.0166 / 0.0002 CLEAR, "
            f"0.017 / 0.0167 / 0.5 do not, the reference row is None: {got}",
            f"[{'OK ' if g2 else 'BAD'}] bar = tierc7.FDR_Q (the OBJECT) / 6 "
            f"= {d['fdr_bar_q_over_m'].iloc[0]}; m declared 6, run 6",
            f"[{'OK ' if g3 else 'BAD'}] INDEPENDENTLY FAILABLE: moving one "
            f"row's p from 0.5 to 0.0001 flips THAT row and no other — no "
            f"rank coupling, no step-up"]
    return prove(
        "F-FDR", "ONE fixed bar q/m = 0.10/6 per scored row, m DECLARED",
        "the bar is not 0.016667; it loosens when fewer than six tests run; "
        "a seventh scored test or a second scored arm of one registration "
        "is accepted; or one row's p moves another row's verdict.",
        [("SEVEN scored tests against a declared m = 6", b_seven),
         ("TWO scored arms under one registration", b_two_arms),
         ("the bar recomputed from tests RUN (q/3 clears p=0.03)", b_m_run)],
        real)


# ═══════════════════════════════════════ F-SEED · 20260921 threaded [LEAN L8]
def f_seed() -> bool:
    B = books()
    N = noisy()
    rs = [t.net_r for t in B["control"]]
    ac = [t.symbol for t in B["control"]]
    # the TWO-SAMPLE rulers need two NOISY books, and the seed is invisible on
    # the degenerate +1 book the older legs used [TC10 review r2].
    va = [t.net_r for t in N["grown"]]
    ca = [t.symbol for t in N["grown"]]
    vb = [t.net_r for t in N["base"]]
    cb = [t.symbol for t in N["base"]]
    real_diff, real_eard = TP.cluster_boot_diff, TP.cluster_boot_ear_diff
    txt = "P-SYN-S [40%] a SYNTHETIC two-sample arm, fixture only." + _CL

    def _diff_drops(va_, ca_, vb_, cb_, seed=TP.SEED, n_boot=TP.N_BOOT):
        """The named wrong: the ruler takes `seed` and ignores it."""
        return real_diff(va_, ca_, vb_, cb_, seed=TP.SEED_LINEAGE,
                         n_boot=n_boot)

    def _eard_drops(va_, ca_, vb_, cb_, seed=TP.SEED, n_boot=TP.N_BOOT):
        return real_eard(va_, ca_, vb_, cb_, seed=TP.SEED_LINEAGE,
                         n_boot=n_boot)

    def _two_rows(root):
        """ONE noisy two-sample arm, scored at each seed — under TWO
        registrations, because an arm already scored may never be re-scored
        under another seed (.scored.json binds the first)."""
        out = {}
        for rid, sd in (("P-SYN-S1", TP.SEED), ("P-SYN-S2", TP.SEED_LINEAGE)):
            TP.register(rid, txt, 40, root=root,
                        arms=_arms12(f"{rid} arm", "set_change"))
            out[sd] = TP.score(rid, txt, N["grown"], SYN12,
                               base=N["base_book"], ruler="set_change",
                               seed=sd, root=root, n_boot=_NB_FIX)
        return out

    def b_ignored():
        real_cb = TP.cluster_boot
        TP.cluster_boot = lambda v, c, seed=0, n_boot=4000: real_cb(
            v, c, seed=TP.SEED_LINEAGE, n_boot=n_boot)     # seed DROPPED
        try:
            a = TP.reference_row(B["control"], seed=TP.SEED)
        finally:
            TP.cluster_boot = real_cb
        differs = (a["ci_lo"], a["ci_hi"]) != (a["sens_ci_lo"],
                                               a["sens_ci_hi"])
        return differs, ("a ruler that DROPS its seed: the 20260921 row and "
                         "its 20260816 echo come out identical "
                         f"({a['ci_hi']} == {a['sens_ci_hi']})")

    def real():
        ok, lines = True, []
        d1 = TP.cluster_boot(rs, ac, seed=TP.SEED)
        d2 = TP.cluster_boot(rs, ac, seed=TP.SEED)
        d3 = TP.cluster_boot(rs, ac, seed=TP.SEED_LINEAGE)
        g = d1.tobytes() == d2.tobytes() and d1.tobytes() != d3.tobytes() \
            and (TP.SEED, TP.SEED_LINEAGE) == (20260921, 20260816)
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] 4000 draws under 20260921 "
                     f"are byte-identical run to run and differ from "
                     f"20260816's")
        ref = TP.reference_row(B["control"], seed=TP.SEED)
        lin = T7._ci_from(T7.cluster_boot(rs, ac), float(np.mean(rs)))
        g = (ref["seed"] == 20260921 and ref["sens_seed"] == 20260816
             and ref["sens_ci_lo"] == TP.r6(lin["lo"])
             and ref["sens_ci_hi"] == TP.r6(lin["hi"])
             and ref["sens_p_one_sided"] == TP.r6(lin["p_one_sided"])
             and (ref["ci_lo"], ref["ci_hi"]) != (ref["sens_ci_lo"],
                                                  ref["sens_ci_hi"]))
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] (reference) CARD v6 vs "
                     f"zero: seed 20260921 CI [{ref['ci_lo']}, "
                     f"{ref['ci_hi']}] p {ref['p_one_sided']}; the L8 "
                     f"sensitivity block [{ref['sens_ci_lo']}, "
                     f"{ref['sens_ci_hi']}] p {ref['sens_p_one_sided']} IS "
                     f"the lineage's default-seed ruler, digit for digit; "
                     f"verdict stable across seeds = "
                     f"{ref['verdict_stable_across_seeds']}")
        a = TP.loao_n(B["control"], None, TP.CLASSIC5, seed=TP.SEED)
        b = TP.loao_n(B["control"], None, TP.CLASSIC5, seed=TP.SEED_LINEAGE)
        g = a["loao_seed"] == 20260921 and a["loao_detail"] != b["loao_detail"]
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] loao_n threads its seed "
                     f"(tierc7.loao cannot): the control's leave-out "
                     f"intervals move with it — {a['loao_line']} under "
                     f"20260921, {b['loao_line']} under 20260816")
        # ── THE TWO-SAMPLE RULERS, one at a time: same seed identical,
        #    other seed different — on NOISY books, where a seed shows.
        for nm, fn in (("cluster_boot_diff", TP.cluster_boot_diff),
                       ("cluster_boot_ear_diff", TP.cluster_boot_ear_diff)):
            x1 = fn(va, ca, vb, cb, seed=TP.SEED, n_boot=_NB_FIX)
            x2 = fn(va, ca, vb, cb, seed=TP.SEED, n_boot=_NB_FIX)
            x3 = fn(va, ca, vb, cb, seed=TP.SEED_LINEAGE, n_boot=_NB_FIX)
            g = (x1.tobytes() == x2.tobytes()
                 and x1.tobytes() != x3.tobytes()
                 and len(x1) == _NB_FIX)
            ok &= g
            lines.append(f"[{'OK ' if g else 'BAD'}] {nm}: {_NB_FIX} draws "
                         f"byte-identical under 20260921 run to run, and "
                         f"NOT the 20260816 draws")
        # ── AND INSIDE THE ROW: the 20260816-scored row IS the 20260921
        #    row's sensitivity block, raw AND equal-asset-risk.
        with tempfile.TemporaryDirectory(prefix="f-seed-") as td:
            rw = _two_rows(Path(td))
            a2, b2 = rw[TP.SEED], rw[TP.SEED_LINEAGE]
            g = (a2["ruler_is_two_sample"] is True
                 and a2["seed"] == TP.SEED
                 and a2["sens_seed"] == TP.SEED_LINEAGE
                 and b2["seed"] == TP.SEED_LINEAGE
                 and b2["sens_seed"] == TP.SEED
                 and (a2["ci_lo"], a2["ci_hi"])
                 != (a2["sens_ci_lo"], a2["sens_ci_hi"])
                 and (a2["ear_ci_lo"], a2["ear_ci_hi"])
                 != (a2["sens_ear_ci_lo"], a2["sens_ear_ci_hi"])
                 and (b2["ci_lo"], b2["ci_hi"])
                 == (a2["sens_ci_lo"], a2["sens_ci_hi"])
                 and (b2["ear_ci_lo"], b2["ear_ci_hi"])
                 == (a2["sens_ear_ci_lo"], a2["sens_ear_ci_hi"])
                 and (b2["sens_ci_lo"], b2["sens_ci_hi"])
                 == (a2["ci_lo"], a2["ci_hi"]))
            ok &= g
            lines.append(f"[{'OK ' if g else 'BAD'}] a TWO-SAMPLE row and its "
                         f"echo: scored at 20260921 CI [{a2['ci_lo']}, "
                         f"{a2['ci_hi']}] / EAR [{a2['ear_ci_lo']}, "
                         f"{a2['ear_ci_hi']}]; the SAME arm scored at "
                         f"20260816 gives [{b2['ci_lo']}, {b2['ci_hi']}] / "
                         f"EAR [{b2['ear_ci_lo']}, {b2['ear_ci_hi']}] — "
                         f"which is EXACTLY the first row's sensitivity "
                         f"block, raw and EAR, and the pair swaps when the "
                         f"lineage seed scores")
        return ok, lines
    return prove(
        "F-SEED", "seed 20260921 drives EVERY ruler — one-sample, "
        "two-sample and equal-asset-risk; 20260816 rides as the sensitivity "
        "block",
        "two runs under one seed differ; the contract seed and the lineage "
        "seed give identical draws (a dropped seed argument) in ANY of "
        "cluster_boot / cluster_boot_diff / cluster_boot_ear_diff / loao_n; "
        "the sensitivity block is not the lineage's default-seed ruler; or "
        "the row scored at 20260816 is not the 20260921 row's echo, raw and "
        "EAR.",
        [("a ONE-SAMPLE ruler that silently DROPS its seed argument",
          b_ignored),
         ("MUTATION: cluster_boot_diff DROPS its seed (the two-sample "
          "ruler of P-TRG-2 / P-BE-1 / P-SPR-2's union view)",
          mutated(TP, "cluster_boot_diff", _diff_drops, real)),
         ("MUTATION: cluster_boot_ear_diff DROPS its seed (the "
          "equal-asset-risk co-headline's two-sample twin)",
          mutated(TP, "cluster_boot_ear_diff", _eard_drops, real))], real)


# ═══════════════════════════════════════ F-STAMP · the warranty, lens-aware
def f_stamp() -> bool:
    B = books()
    z = TP._iso_ms

    def b_thursday():
        hi = z("2026-09-23T08:00:00Z") - 1
        thu = ((hi + 1) // (7 * MS_1D)) * (7 * MS_1D)     # offset 0 = THURSDAY
        return thu == TP.lens_edge(hi, "1w"), (
            f"epoch(Thursday)-anchored week close = {TP.iso(thu)}; the "
            f"Monday law says {TP.iso(TP.lens_edge(hi, '1w'))}")

    def b_future():
        r, why = refused(lambda: TP.stamp_n(
            pd.DataFrame({"x": [1]}), B["meta"], "1d",
            lens_last_closed_ms=z(B["meta"]["last_closed_4h_close"]) + MS_1D))
        return (not r), why

    def b_lens():
        r, why = refused(lambda: TP.stamp_n(pd.DataFrame({"x": [1]}),
                                            B["meta"], "30m"))
        return (not r), why

    def real():
        ok, lines = True, []
        hi1 = z("2026-09-21T16:00:00Z") - 1
        hi2 = z("2026-09-23T08:00:00Z") - 1
        want = {(hi1, "5m"): "2026-09-21T16:00:00Z",
                (hi1, "1h"): "2026-09-21T16:00:00Z",
                (hi1, "4h"): "2026-09-21T16:00:00Z",
                (hi1, "12h"): "2026-09-21T12:00:00Z",
                (hi1, "1d"): "2026-09-21T00:00:00Z",
                (hi1, "1w"): "2026-09-21T00:00:00Z",
                (hi2, "12h"): "2026-09-23T00:00:00Z",
                (hi2, "1d"): "2026-09-23T00:00:00Z",
                (hi2, "1w"): "2026-09-21T00:00:00Z"}
        got = {k: TP.iso(TP.lens_edge(*k)) for k in want}
        g = got == want and datetime(2026, 9, 21,
                                     tzinfo=timezone.utc).weekday() == 0
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] lens_edge, nine hand "
                     f"answers over two corridor ends: 12h/1d floor to their "
                     f"own grid; 1w closes on MONDAY 2026-09-21 00:00Z "
                     f"(datetime says that date IS a Monday)")
        df = pd.DataFrame({"x": [1, 2]})
        s = TP.stamp_n(df, B["meta"], "1d")
        p = T8.stamp(df, B["meta"])
        g = (all(c in s.columns for c in TP.AS_OF_COLUMNS)
             and all(list(s[c]) == list(p[c]) for c in p.columns)
             and set(s["as_of_lens"]) == {"1d"}
             and s["as_of_last_closed_bar"].iloc[0]
             == TP.iso(TP.lens_edge(B["hi"], "1d"))
             and s["as_of_panel"].iloc[0] == "CLASSIC5"
             and int(s["as_of_n_assets"].iloc[0]) == 5
             and s["as_of_substrate"].iloc[0] == TP.substrate()["substrate"])
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] stamp_n = tierc8.stamp's "
                     f"four columns UNCHANGED + as_of_lens / "
                     f"as_of_last_closed_bar / as_of_panel / as_of_n_assets "
                     f"/ as_of_substrate ({len(TP.AS_OF_COLUMNS)} in all)")
        return ok, lines
    return prove(
        "F-STAMP", "every table says which corridor, which LENS, which "
        "panel, which snapshot",
        "a week closes on the epoch's Thursday; a lens edge after the "
        "corridor end is stamped; an unknown lens is accepted; or any of "
        "tierc8.stamp's four columns is altered or missing.",
        [("the week anchored on the epoch's THURSDAY", b_thursday),
         ("a 1d as-of edge AFTER the corridor end", b_future),
         ("an unknown lens ('30m')", b_lens)], real)


# ═══════════════════════════════════════════ F-GRID · the helper, with teeth
def f_grid() -> bool:
    declared = ("1.50", "1.75", "2.00", "2.25", "2.50", "2.75", "3.00")

    def _tab(cells, promotable=False):
        return pd.DataFrame({"cell": list(cells), "n": range(len(cells)),
                             "loao_line": ["—"] * len(cells),
                             "promotable": [promotable] * len(cells)})

    def _b(tab):
        def leg():
            ok, lines = TP.grid_whole(declared, tab, "cell",
                                      require_cols=("n", "loao_line"),
                                      require_false=("promotable",))
            bad = [ln for ln in lines if ln.startswith("[BAD]")]
            return ok, (bad[0][:140] if bad else "no BAD line")
        return leg

    def real():
        ok, lines = TP.grid_whole(declared, _tab(declared), "cell",
                                  require_cols=("n", "loao_line"),
                                  require_false=("promotable",),
                                  label="synthetic 7-cell grid")
        return ok, lines
    nulls = _tab(declared)
    nulls.loc[2, "loao_line"] = None
    return prove(
        "F-GRID", "grid_whole — every grid WHOLE: declared literal vs "
        "written table, two objects",
        "a declared cell is missing, an undeclared cell is present, a cell "
        "is duplicated, a required column is absent or null on any row, or "
        "any row is promotable.",
        [("one declared cell MISSING from the table", _b(_tab(declared[:-1]))),
         ("one UNDECLARED cell in the table",
          _b(_tab(declared + ("3.25",)))),
         ("one cell DUPLICATED (count right, set wrong)",
          _b(_tab(declared[:-1] + ("1.50",)))),
         ("a required column NULL on one row", _b(nulls)),
         ("a row marked promotable", _b(_tab(declared, promotable=True)))],
        real)


# ═══════════════════════════════════════ F-CLOSURE · two tiers, by subprocess
RANGE_IMPORT_LINE = re.compile(          # OR-1 F-BR-14's regex, verbatim
    r"(?m)^[ \t]*(?:from|import)[ \t]+[^\n#]*\brangefinder\b")
ANALYTICS_HANDLES = {"AN", "AS", "AM", "AV", "AW"}   # tierc5/6/7/8's aliases


def _closure(modname: str, shadow_src: str | None = None) -> set[str]:
    """Modules a CLEAN interpreter loads by importing `modname`.  With
    `shadow_src`, a PLANTED copy is written as <modname>.py into a throwaway
    directory that goes FIRST on the subprocess's path — it shadows the real
    module there and nowhere else.  No file in the repo is touched."""
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
                             text=True, timeout=600)
    if out.returncode != 0:
        raise RuntimeError(out.stderr[-400:])
    return set(json.loads(out.stdout.strip().splitlines()[-1]))


def _range_parts(closure: set[str]) -> list[str]:
    return sorted(m for m in closure
                  if any("rangefinder" in part for part in m.split(".")))


def _analytics_parts(closure: set[str]) -> list[str]:
    return sorted(m for m in closure if "analytics" in m.split("."))


def _static_hits(src: str) -> list[str]:
    """What a runner's SOURCE may not contain: an analytics or range import
    (AST, so prose cannot trip it), a read through a parent's analytics
    alias (`T5.AN....` consults without importing), or a line F-BR-14's own
    regex would flag."""
    hits = []
    for node in ast.walk(ast.parse(src)):
        names = ([al.name for al in node.names]
                 if isinstance(node, ast.Import) else
                 [node.module or ""] + [al.name for al in node.names]
                 if isinstance(node, ast.ImportFrom) else [])
        hits += [f"import {n}" for n in names
                 if "analytics" in n.split(".") or "rangefinder" in n]
        if isinstance(node, ast.Attribute) and node.attr in ANALYTICS_HANDLES:
            hits.append(f"alias read .{node.attr}")
    hits += [f"F-BR-14 line: {m.group(0).strip()}"
             for m in RANGE_IMPORT_LINE.finditer(src)]
    return hits


def f_closure() -> bool:
    panel_src = (ROOT / "scripts" / "tierc10_panel.py").read_text()
    rules_src = (ROOT / "scripts" / "tierc7_rules.py").read_text()

    def b_runner_range():
        c = _closure("tierc10_panel", panel_src.replace(
            "import tierc9 as T9",
            "from engine import rangefinder as RNG\nimport tierc9 as T9", 1))
        return not _range_parts(c), f"planted runner reaches {_range_parts(c)}"

    def b_rules_analytics():
        c = _closure("tierc7_rules", rules_src + "\nimport analytics\n")
        return not _analytics_parts(c), (f"planted rules module reaches "
                                         f"{_analytics_parts(c)[:3]}")

    def b_rules_range():
        c = _closure("tierc7_rules",
                     rules_src + "\nimport engine.rangefinder\n")
        return not _range_parts(c), (f"planted rules module reaches "
                                     f"{_range_parts(c)}")

    def b_static_import():
        h = _static_hits(panel_src
                         + "\nfrom analytics import rangefinder_census\n")
        return not h, f"static scan of the planted source: {h}"

    def b_static_alias():
        h = _static_hits(panel_src + "\n_x = T5.AN.structure\n")
        return not h, f"static scan of the planted source: {h}"

    def real():
        ok, lines = True, []
        dec = _closure("tierc7_rules")
        ra, an = _range_parts(dec), _analytics_parts(dec)
        g = not ra and not an and "tierc2_rules" in dec
        ok &= g
        proj = sorted(m for m in dec if m.split(".")[0] in ("engine",)
                      or m.startswith("tierc"))
        lines.append(f"[{'OK ' if g else 'BAD'}] TIER 1 — THE DECISION "
                     f"CLOSURE (tierc7_rules -> tierc2..6_rules -> engine): "
                     f"{len(dec)} modules, analytics {an or 'NONE'}, "
                     f"rangefinder {ra or 'NONE'}")
        lines.append(f"      project modules: {proj}")
        run_ = _closure("tierc10_panel")
        ra2 = _range_parts(run_)
        an2 = _analytics_parts(run_)
        g = not ra2 and "tierc9" in run_ and "tierc10_panel" in run_
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] TIER 2 — THE RUNNER CLOSURE "
                     f"(tierc10_panel -> tierc9..5): {len(run_)} modules, "
                     f"rangefinder {ra2 or 'NONE'}")
        lines.append(f"      analytics IS loaded here ({an2}) — INHERITED "
                     f"from tierc2_baseline/tierc5..8, whose TAPE code runs "
                     f"after the replay has decided everything "
                     f"[captured-not-consulted, F-C2-6]; printed, not hidden")
        h = _static_hits(panel_src)
        g = not h
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] tierc10_panel.py's OWN "
                     f"source: no analytics import, no rangefinder import, "
                     f"no read through a parent's analytics alias "
                     f"{sorted(ANALYTICS_HANDLES)}, no F-BR-14 line: "
                     f"{h or 'clean'}")
        return ok, lines
    return prove(
        "F-CLOSURE", "the v6 control path holds NO rangefinder component; "
        "its decision tier holds NO analytics — two tiers, measured",
        "any module with a `rangefinder` name component is loaded by "
        "importing the rules chain or this runner; `analytics` is loaded by "
        "the rules chain; or tierc10_panel.py's source imports analytics / "
        "a range module or reads through a parent's analytics alias.",
        [("`from engine import rangefinder` planted in a SHADOW copy of "
          "the runner", b_runner_range),
         ("`import analytics` planted in a SHADOW copy of tierc7_rules",
          b_rules_analytics),
         ("`import engine.rangefinder` planted in a SHADOW copy of "
          "tierc7_rules", b_rules_range),
         ("`from analytics import rangefinder_census` planted in the "
          "runner's source text", b_static_import),
         ("`T5.AN.structure` (consulting through a parent's alias) planted "
          "in the source text", b_static_alias)], real)


# ═══════════════════════════════════ F-DET · two runs, byte-identical
def _build(rerun: bool) -> subprocess.CompletedProcess:
    return subprocess.run(
        [PY, str(ROOT / "scripts" / "tierc10_panel.py")]
        + (["--rerun"] if rerun else []),
        cwd=ROOT, capture_output=True, text=True, timeout=3600)


def _copy_pair(td: str) -> tuple[Path, Path]:
    a, b = Path(td) / "a", Path(td) / "b"
    shutil.copytree(PANEL_OUT, a)
    shutil.copytree(PANEL_RERUN, b)
    return a, b


def f_det() -> bool:
    runs = [_build(False), _build(True)]
    _B["built_this_process"] = True

    def b_value():
        with tempfile.TemporaryDirectory(prefix="f-det-") as td:
            a, b = _copy_pair(td)
            d = pd.read_parquet(b / "control_journal.parquet")
            # THE CONTROL FOR THE PLANT: an UNCHANGED read->write round trip
            # must stay GREEN, or the RED below would be the rewrite's doing
            # and not the planted value's.
            d.to_parquet(b / "control_journal.parquet", index=False)
            if not TP.check_det(a, b)[0]:
                return True, ("an UNCHANGED rewrite already differs in bytes "
                              "— this plant cannot isolate the value")
            d.loc[d.index[7], "net_r"] = float(d["net_r"].iloc[7]) + 1e-6
            d.to_parquet(b / "control_journal.parquet", index=False)
            ok, lines = TP.check_det(a, b)
            return ok, ("unchanged rewrite stays GREEN; then "
                        + [ln for ln in lines
                           if ln.startswith("[BAD]")][0][:120])

    def b_sha():
        with tempfile.TemporaryDirectory(prefix="f-det-") as td:
            a, b = _copy_pair(td)
            m = json.loads((b / "build_manifest.json").read_text())
            m["sha"]["leans"] = "0" * 64
            (b / "build_manifest.json").write_text(json.dumps(m))
            ok, lines = TP.check_det(a, b)
            return ok, [ln for ln in lines if ln.startswith("[BAD]")][0][:140]

    def b_table_lost():
        with tempfile.TemporaryDirectory(prefix="f-det-") as td:
            a, b = _copy_pair(td)
            m = json.loads((b / "build_manifest.json").read_text())
            m["sha"].pop("control_loao")
            (b / "build_manifest.json").write_text(json.dumps(m))
            ok, lines = TP.check_det(a, b)
            return ok, [ln for ln in lines if ln.startswith("[BAD]")][0][:140]

    def real():
        bad = [r for r in runs if r.returncode != 0]
        if bad:
            return False, ["[BAD] a build exited nonzero: "
                           + (bad[0].stderr or bad[0].stdout)[-400:]]
        ok, lines = TP.check_det(PANEL_OUT, PANEL_RERUN)
        m = json.loads((PANEL_OUT / "build_manifest.json").read_text())
        g = "wall_clock_at_run" not in json.dumps(m) \
            and "elapsed" not in json.dumps(m)
        lines.append(f"[{'OK ' if g else 'BAD'}] the manifest carries no "
                     f"wall clock and no elapsed time (seed {m['seed']}, "
                     f"as_of {m['as_of']}, {len(m['sha'])} tables)")
        return ok and g, lines
    if any(r.returncode for r in runs):
        breaks = [("(builds failed — no copies to corrupt)",
                   lambda: (False, "skipped: see the real leg"))]
    else:
        breaks = [("1e-6 added to ONE value in a COPY of the rerun", b_value),
                  ("one content sha altered in a COPY of the rerun manifest",
                   b_sha),
                  ("one table dropped from a COPY of the rerun manifest",
                   b_table_lost)]
    return prove(
        "F-DET", "scripts/tierc10_panel.py and --rerun: byte-identical "
        "artifacts",
        "either build exits nonzero, the table sets differ, a content sha "
        "moves, any parquet pair differs in BYTES, the two runs read "
        "different input bytes, or the manifest carries a wall clock.",
        breaks, real)


# ═══════════ F-KEY · totality: keys declared, unique, ALL as-of columns
def f_key() -> bool:
    if not _B.get("built_this_process"):
        _build(False)       # never judge a STALE build left by older code

    def _b(mutate):
        def leg():
            with tempfile.TemporaryDirectory(prefix="f-key-") as td:
                root = Path(td) / "panel"
                shutil.copytree(PANEL_OUT, root)
                mutate(root)
                ok, lines = TP.check_keys(root)
                bad = [ln for ln in lines if ln.startswith("[BAD]")]
                return ok, (bad[0][:140] if bad else "no BAD line")
        return leg

    def m_dup(root):
        p = root / "control_journal.parquet"
        d = pd.read_parquet(p)
        pd.concat([d, d.iloc[[0]]], ignore_index=True).to_parquet(p, index=False)

    def m_col(col):
        def mut(root):
            p = root / "panel_admission.parquet"
            pd.read_parquet(p).drop(columns=[col]).to_parquet(p, index=False)
        return mut

    def m_undeclared(root):
        pd.DataFrame({"x": [1]}).to_parquet(root / "smuggled.parquet",
                                            index=False)

    def m_null(root):
        p = root / "leans.parquet"
        d = pd.read_parquet(p)
        d.loc[0, "as_of_last_closed_bar"] = None
        d.to_parquet(p, index=False)

    def stamp_truth(root):
        """THE STAMP NAMES THE PANEL ITS ROWS ARE TRUE OF — checked against
        each table's OWN content, never against the stamp's source."""
        def named(symbols):
            # the table is filed SORTED ON ITS KEY, so the panel is
            # recognised by its MEMBERS, not by the order of the rows.
            hit = [nm for nm, pnl in (("CLASSIC5", TP.CLASSIC5),
                                      ("UNSEEN12", TP.UNSEEN12),
                                      ("PANEL17", TP.PANEL17))
                   if sorted(pnl) == sorted(symbols)]
            return hit[0] if hit else TP.panel_name(tuple(symbols))
        adm = pd.read_parquet(root / "panel_admission.parquet")
        fun = pd.read_parquet(root / "panel_funding.parquet")
        cor = pd.read_parquet(root / "panel_corridor.parquet")
        jr = pd.read_parquet(root / "control_journal.parquet")
        g1 = all(set(d["as_of_n_assets"]) == {len(d)}
                 and set(d["as_of_panel"]) == {named(list(d["symbol"]))}
                 for d in (adm, fun))
        g2 = bool((cor["as_of_n_assets"] == cor["n_assets"]).all()) and all(
            set(d["as_of_panel"]) == {named(list(d["symbol"]))}
            and set(d["as_of_last_closed_4h"])
            == set(d["panel_last_closed_4h_close"])
            for _, d in cor.groupby("panel", sort=False))
        g3 = set(jr["as_of_panel"]) == {"CLASSIC5"} \
            and set(jr["asset"]) <= set(TP.CLASSIC5) \
            and set(jr["as_of_n_assets"]) == {5}
        return bool(g1 and g2 and g3), [
            f"[{'OK ' if g1 else 'BAD'}] panel_admission / panel_funding "
            f"({len(adm)} declared assets) are stamped as_of_panel="
            f"{sorted(set(adm['as_of_panel']))} n={sorted(set(adm['as_of_n_assets']))}"
            f" — the panel their ROWS hold, not the build's CLASSIC5",
            f"[{'OK ' if g2 else 'BAD'}] panel_corridor: every row's stamp "
            f"is ITS OWN panel's (name, size, edge) — "
            f"{sorted(set(cor['as_of_panel']))}",
            f"[{'OK ' if g3 else 'BAD'}] control_journal stays CLASSIC5 / 5"]

    def _b_stamp(mutate):
        def leg():
            with tempfile.TemporaryDirectory(prefix="f-key-") as td:
                root = Path(td) / "panel"
                shutil.copytree(PANEL_OUT, root)
                mutate(root)
                ok, lines = stamp_truth(root)
                bad = [ln for ln in lines if ln.startswith("[BAD]")]
                return ok, (bad[0][:140] if bad else "no BAD line")
        return leg

    def m_mislabel(root):
        p = root / "panel_admission.parquet"
        d = pd.read_parquet(p)
        d["as_of_panel"], d["as_of_n_assets"] = "CLASSIC5", 5
        d.to_parquet(p, index=False)

    def m_corridor_one_meta(root):
        p = root / "panel_corridor.parquet"
        d = pd.read_parquet(p)
        d["as_of_panel"], d["as_of_n_assets"] = "CLASSIC5", 5
        d.to_parquet(p, index=False)

    def real():
        ok, lines = TP.check_keys(PANEL_OUT)
        g, ln = stamp_truth(PANEL_OUT)
        return ok and g, lines + ln
    return prove(
        "F-KEY", "every filed parquet: a declared key, no duplicate, all "
        f"{len(TP.AS_OF_COLUMNS)} as-of columns — and a stamp that names "
        "the panel its rows hold",
        "a parquet has no declared key, a key duplicates, a declared table "
        "is missing, ANY table lacks (or nulls) any of the four "
        "tierc8.stamp columns or the five lens-aware ones, or a 17-asset "
        "table is stamped as_of_panel=CLASSIC5 / as_of_n_assets=5.",
        [("a duplicate key row appended to a COPY", _b(m_dup)),
         ("`as_of_last_closed_4h` dropped from a COPY",
          _b(m_col("as_of_last_closed_4h"))),
         ("`as_of_lens` dropped from a COPY", _b(m_col("as_of_lens"))),
         ("an UNDECLARED parquet smuggled into a COPY", _b(m_undeclared)),
         ("one as-of stamp NULLED in a COPY", _b(m_null)),
         ("the 17-asset admission table stamped CLASSIC5 / 5 in a COPY (the "
          "first build's mislabel, replayed)", _b_stamp(m_mislabel)),
         ("every panel_corridor row stamped with ONE meta in a COPY",
          _b_stamp(m_corridor_one_meta))], real)


# ═══════════ F-WORKTREE-ATTEST · the review law, printed with the evidence
def f_worktree_attest() -> bool:
    say("\n--- F-WORKTREE-ATTEST — the review law (an attestation, not a "
        "check)")
    for ln in (
            "review law: reviewers run in READ-ONLY WORKTREES (isolation: "
            "worktree), never on the certified tree",
            "lineage: enacted 2026-08-17 (TIER-C7 sabotage patch, caught by "
            "F-KEY's totality leg); carried by TIER-C8; TIER-C9; carried here",
            "TIER-C10 note: the 28 registered worktrees under "
            ".claude/worktrees/ sit at a6da1b9 (2026-07-09) — a review of "
            "this build needs FRESH worktrees at the TC10 HEAD; and "
            "research_outputs/tierc6|tierc9 are gitignored, so F-CTRL/b's "
            "referees must be carried into one or that leg is RED there",
            "      FAILS IF: never — it is an attestation, and it rides "
            "with the transcript so the evidence and the law travel "
            "together."):
        say("    " + ln)
    RESULTS["F-WORKTREE-ATTEST"] = True
    return True


LEGS = (f_ctrl_a, f_ctrl_b, f_substrate, f_panel, f_admit, f_funding,
        f_law4_gate, f_loao_n, f_ear_boot, f_reg_gate, f_score, f_verdict,
        f_era, f_arm, f_fdr, f_seed, f_stamp, f_grid, f_closure, f_det,
        f_key, f_worktree_attest)


def main() -> int:
    say("=" * 78)
    say("TIER-C10 PANEL FIXTURE TRANSCRIPT — break legs first, RED or void")
    say("=" * 78)
    say(f"substrate {TP.substrate()['substrate']} · seed {TP.SEED} "
        f"(sensitivity {TP.SEED_LINEAGE}) · UNSEEN12 source: "
        f"{TP.UNSEEN12_SOURCE}")
    only = [a.lower().replace("-", "_") for a in sys.argv[1:]
            if a != "--only"]
    for leg in LEGS:
        if only and not any(o in leg.__name__ for o in only):
            continue
        leg()
    n = sum(RESULTS.values())
    say(f"\nFIXTURE SUMMARY  {n}/{len(RESULTS)} PASS  {json.dumps(RESULTS)}")
    # THE TRANSCRIPT IS FILED, NOT JUST PRINTED — as-of stamped.  A partial
    # (filtered) run is filed under its own name so it never overwrites the
    # whole suite's evidence.
    try:
        meta = books()["meta"] if _B else TP.corridor_n(TP.CLASSIC5)[2]
        PANEL_OUT.mkdir(parents=True, exist_ok=True)
        name = "FIXTURES_PANEL.txt" if not only else "FIXTURES_PANEL_partial.txt"
        (PANEL_OUT / name).write_text(
            f"as_of_last_closed_4h: {meta['last_closed_4h_close']}\n"
            + "\n".join(T) + "\n")
    except BaseException as e:                              # noqa: BLE001
        print(f"(transcript filing failed, non-fatal: {e})")
    if n != len(RESULTS):
        print("*** HALT: fixture mismatch. Nothing downstream is "
              "trustworthy. ***")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
