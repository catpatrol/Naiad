#!/usr/bin/env python
"""TIER-C10 · STAGE A — THE FIXTURES FOR THE TAPE AND THE STAMPS.

Seed 20260921 (threaded explicitly; nothing here draws at random except the
seeded cut sampler, which is `numpy.random.default_rng(SEED)` and prints its
draws).  Every leg states its FAILURE CONDITION.  Every guard has a BREAK LEG
that plants a deliberate violation and must go RED — judged on the PLANTED
item alone, always on a COPY: no file of the repo is edited, no filed table is
written by a break leg, every in-memory mutation is restored in `finally`.

  F-STAMP-ASOF     the stamps are AS-OF, proved by PREFIX RECOMPUTE: rebuild
                   the whole census layer from `tape[:t]` and demand every
                   instant at or before the cut carries the stamp on file.
                   Four leaks are planted — a leaked redraw, a leaked flip, a
                   leaked state latch, a one-bar-late index — and each must be
                   caught. Includes an INDEPENDENT guard on the census layer
                   itself (the knowable_at = -1 pivots on NEARUSDT/SOLUSDT).
  F-STAMP-JOIN     the stamps are a PURE LEFT-JOIN: the journal comes back
                   byte-identical to the unstamped book, no row is dropped,
                   none is multiplied. Planted: a dropped stamp, a duplicated
                   stamp, a campaign silently mutated by "stamping".
  F-STAMP-NULLS    no dead range is ever forward-filled; the two leash fields
                   are the one stated exception; macro_state reads NONE where
                   nothing is known. Planted: a forward-filled twin, a
                   neighbour-reading stamp at idx = -1.
  F-STAMP-FUNNEL   the funnel is a PARTITION, the +1R instant is the card's
                   own latch, the reject ladder places each reason where it
                   became knowable. Planted: a flipped latch, an unknown
                   reject reason, an out-of-window arming, a lens mismatch.
  F-STAMP-CLOSURE  CAPTURED-NOT-CONSULTED, extended: the v6 decision closure
                   reaches no stamp, no census, nothing named rangefinder —
                   by subprocess closure AND by an AST scan that sees a LAZY
                   in-function import a closure never would.
  F-DET            two output roots, byte-identical.
  F-KEY            every table keyed, unique, and carrying all nine as-of
                   columns.

Run: NAIAD_CACHE_DIR=~/.cache/naiad/snapshots/tc10_20260921 \\
     ~/venvs/naiad/bin/python -B scripts/tierc10_stamps_fixtures.py [leg ...]
"""
from __future__ import annotations

import ast
import copy
import dataclasses
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import tierc10_stamps as S                                           # noqa: E402
import tierc10_census as C                                           # noqa: E402
import tierc10_panel as TP                                           # noqa: E402
import tierc9 as T9                                                  # noqa: E402
import tierc7 as T7                                                  # noqa: E402

import numpy as np                                                   # noqa: E402
import pandas as pd                                                  # noqa: E402

SEED = S.SEED                   # 20260921 — threaded, never defaulted
SEED_LINEAGE = S.SEED_LINEAGE   # 20260816 — the sensitivity echo
PY = sys.executable
OUT = S.OUT
OUT_RERUN = S.OUT_RERUN
TRANSCRIPT = "FIXTURES_STAMPS.txt"

LINES: list[str] = []
PASSED: list[str] = []
FAILED: list[str] = []


def say(line: str = "") -> None:
    print(line)
    LINES.append(line)


def clock(line: str) -> None:
    """Wall clock goes to stdout ONLY — a transcript that carries it cannot be
    diffed byte for byte across two runs, and F-DET compares transcripts."""
    print(line)


def check(fixture: str, ok: bool, detail: str) -> bool:
    say(f"  [{'PASS' if ok else 'FAIL'}] {fixture}: {detail}")
    return ok


def prove(fixture: str, title: str, fails_if: str, break_leg, real_leg) -> None:
    """Both legs, in order.  The break leg must go RED or the fixture is void
    — a guard nobody has seen fail is a guard nobody has seen."""
    say(f"\n{fixture} — {title}")
    say(f"  FAILS IF: {fails_if}")
    try:
        b_ok, b_detail = break_leg()
    except Exception as e:                  # a break leg that errors proved nothing
        b_ok, b_detail = True, f"break leg RAISED {e.__class__.__name__}: {e}"
    say(f"  [BREAK] deliberate violation -> "
        f"{'RED (correct)' if not b_ok else 'GREEN (FIXTURE IS VOID)'}: {b_detail}")
    try:
        r_ok, r_detail = real_leg()
    except Exception as e:                  # a fixture that errors is a fail
        r_ok, r_detail = False, f"raised {e.__class__.__name__}: {e}"
    green = check(fixture, r_ok, r_detail)
    if b_ok:
        FAILED.append(f"{fixture} (break leg passed — fixture proves nothing)")
    elif not green:
        FAILED.append(fixture)
    else:
        PASSED.append(fixture)


def plants(rows) -> tuple[bool, str]:
    """One plant per guard, judged ONE AT A TIME [F-BR-13/14 idiom].  `rows` =
    (name, thunk -> list of findings).  A plant that yields NO finding PASSED
    — the break leg is then GREEN and the fixture void."""
    passed, caught = [], []
    for name, thunk in rows:
        try:
            found = thunk()
        except SystemExit as e:             # a HALT is a finding, and the best kind
            found = [f"HALT: {e}"]
        except Exception as e:              # so is a crash — but it is NAMED, so a
            found = [f"RAISED {e.__class__.__name__}: {e}"]   # reader can judge it
        (caught if found else passed).append(
            f"{name} -> {str(found[0])[:130]}" if found else name)
    if passed:
        return True, f"{len(passed)} plant(s) PASSED: {passed}"
    return False, (f"all {len(caught)} plants caught, one at a time: "
                   + " · ".join(caught))


def sha_df(df: pd.DataFrame) -> str:
    """Content sha of a frame, independent of parquet's own encoding: the
    lineage's CSV canonicalisation, hashed here rather than trusted."""
    d = df.copy()
    d.columns = [str(c) for c in d.columns]
    return hashlib.sha256(
        d.to_csv(index=False, float_format="%.10g").encode()).hexdigest()


# ═══════════════════════════════════════════════ the control, built ONCE
_CTRL: dict = {}


def ctrl() -> dict:
    """The known control, its funnel and its stamps — built once, shared by
    every fixture.  Card v6, all pins frozen, CLASSIC5: the ONE book Stage A
    rides, and the only book any leg here touches."""
    if not _CTRL:
        cb = S.control_book()
        out = S.stamp_book(cb["book"], TP.CLASSIC5, lens=S.LENS_OF_RECORD,
                           arms=cb["arms"], lo_ms=cb["lo_ms"], hi_ms=cb["hi_ms"])
        _CTRL.update(cb)
        _CTRL["out"] = out
        _CTRL["journal_before"] = T7.journal_frame(list(cb["book"]))
    return _CTRL


def p4() -> str:
    return S.prefix(S.LENS_OF_RECORD)


# ═══════════════════════════════════════════ F-STAMP-ASOF · prefix recompute
def _cuts(inst: pd.DataFrame, asset: str, k: int = 8,
          seed: int = SEED) -> list[int]:
    """Cut points, SEEDED and AIMED.  Random cuts would almost never land on
    an interesting bar, so the cuts are drawn from the asset's OWN instant
    bars (seeded RNG, draws printed) and one cut is forced at the very last
    instant — the end of a prefix is where a machine's state is least settled
    and a leak is most likely to hide."""
    bars = sorted(set(int(v) for v in
                      inst.loc[inst["asset"] == asset, "instant_i"]))
    if not bars:
        return []
    rng = np.random.default_rng(int(seed) + sum(ord(ch) for ch in asset))
    pick = sorted(set(rng.choice(bars, size=min(k - 1, len(bars)),
                                 replace=False).tolist() + [bars[-1]]))
    return [int(b) for b in pick]


def _prefix_stamps(asset: str, inst: pd.DataFrame, cut_i: int,
                   view_edit=None, index_edit=None) -> pd.DataFrame:
    """Every stamp for `asset`'s instants at or before bar `cut_i`, recomputed
    from the PREFIX `tape[:cut_i + 1]` and NOTHING ELSE.

    This is the honest form of an as-of proof: no information after the cut
    exists in the process at all, so a stamp that matches cannot have used
    one.  `view_edit` / `index_edit` are the break legs' handles and are None
    on the real leg.
    """
    tape = C.load_tape(asset, S.LENS_OF_RECORD)
    pre = tape.head(int(cut_i) + 1)
    rv = C.run_scale(pre, S.FROZEN_SCALE)
    view = C.asof_view(pre, rv["macro"], rv["leash"])
    if view_edit is not None:
        view = view_edit(pre, rv, view)
    sub = (inst[(inst["asset"] == asset) & (inst["instant_i"] <= int(cut_i))]
           [["instant_ms", "instant_kind", "instant_close_ms"]]
           .drop_duplicates(subset=["instant_ms", "instant_kind"])
           .sort_values(["instant_ms", "instant_kind"], kind="mergesort"))
    if not len(sub):
        return pd.DataFrame()
    idx = C.asof_index(pre, sub["instant_close_ms"].to_numpy(np.int64))
    if index_edit is not None:
        idx = index_edit(idx, pre.n)
    recs = []
    for i, m in zip(idx, sub["instant_close_ms"]):
        try:
            recs.append(S.stamps_at(pre, view, int(i), int(m)))
        except SystemExit as e:             # the warranty fired — that IS a finding
            recs.append({f: f"HALT {e}" for f in S.STAMP_FIELDS})
    d = pd.DataFrame(recs, columns=list(S.STAMP_FIELDS))
    d.insert(0, "instant_kind", sub["instant_kind"].to_numpy())
    d.insert(0, "instant_ms", sub["instant_ms"].to_numpy(np.int64))
    return d.reset_index(drop=True)


def _same(a, b) -> bool:
    if a is None or (isinstance(a, float) and np.isnan(a)):
        return b is None or (isinstance(b, float) and np.isnan(b))
    if isinstance(a, float) or isinstance(b, float):
        try:
            return float(a) == float(b)
        except (TypeError, ValueError):
            return False
    return a == b


def _asof_findings(assets, view_edit=None, index_edit=None,
                   n_cuts: int = 8, seed: int = SEED) -> list[str]:
    """Compare every prefix-recomputed stamp with the FILED one.  The filed
    frame is the artifact a reader opens; if a prefix and the file disagree,
    the file saw something the prefix could not."""
    o = ctrl()["out"]
    inst = o["instants"]
    p = p4()
    found = []
    for asset in assets:
        for cut in _cuts(inst, asset, n_cuts, seed):
            pre = _prefix_stamps(asset, inst, cut, view_edit, index_edit)
            if not len(pre):
                continue
            filed = (inst[(inst["asset"] == asset)
                          & (inst["instant_i"] <= cut)]
                     .drop_duplicates(subset=["instant_ms", "instant_kind"])
                     .set_index(["instant_ms", "instant_kind"]))
            for _, r in pre.iterrows():
                key = (int(r["instant_ms"]), r["instant_kind"])
                if key not in filed.index:
                    found.append(f"{asset} cut@{cut}: {key} absent from the file")
                    continue
                fr = filed.loc[key]
                for fld in S.STAMP_FIELDS:
                    if not _same(r[fld], fr[p + fld]):
                        found.append(
                            f"{asset} cut@{cut} {key[1]}@{S.iso(key[0])}: "
                            f"{fld} prefix={r[fld]!r} filed={fr[p + fld]!r}")
                        break
            if found:
                return found
    return found


# ── the four planted leaks, each a COPY of an honest view ──────────────────
def _leak_redraw(pre, rv, view):
    """A LEAKED REDRAW: the as-of top/bottom replaced by the range's
    END-OF-LIFE bounds — the post-redraw values, knowable only after the
    hardens that produced them.  This is the exact leak the census as-of layer
    exists to avoid, planted here on a copy of its output."""
    v = dict(view)
    top, bot = view["top"].copy(), view["bot"].copy()
    for r in rv["macro"]["ranges"]:
        if r.confirm_i is None or int(r.confirm_i) < 0:
            continue
        a = int(r.confirm_i)
        b = int(r.die_i) if (r.die_i is not None and int(r.die_i) >= 0) else len(top)
        top[a:b], bot[a:b] = float(r.top), float(r.bottom)
    v["top"], v["bot"] = top, bot
    c = pre.c
    with np.errstate(invalid="ignore", divide="ignore"):
        v["pct"] = 100.0 * (c - bot) / (top - bot)
        v["dist_atr"] = np.minimum(np.abs(top - c), np.abs(c - bot)) / pre.atr
    return v


def _leak_flip(pre, rv, view):
    """A LEAKED FLIP: the last flip known at its TOUCH bar instead of at touch
    + FLIP_HOLD_BARS — six bars of hindsight on every flip stamp."""
    v = dict(view)
    lf = view["_leash_frame"]
    fl = lf[lf["event"] == "flip"].sort_values(["i", "pos"], kind="mergesort")
    n = pre.n
    pol = [1 if s == "top" else -1 for s in fl["side"]]
    cps = list(zip(fl["i"].tolist(), pol))
    v["flip_pol"] = C._step_fill(n, cps, 0, np.int8)
    kn = C._step_fill(n, list(zip(fl["i"].tolist(), fl["i"].tolist())), -1,
                      np.int64)
    v["flip_age"] = np.where(kn >= 0, np.arange(n, dtype=np.int64) - kn, -1)
    return v


CONFIRM_LEAK_BARS = 50          # how early the planted confirm/die is latched


def _wick_state(pre, rv, view) -> np.ndarray:
    """THE STATE LATCH AS A NAIVE READER WOULD BUILD IT: the machine's first
    pivot taken at its own WICK bar instead of at its SEAL — the engine's
    `knowable_at = -1` quirk, let through.  Used by the real leg to show that
    on NEARUSDT and SOLUSDT (which carry such pivots) the two readings really
    do differ, and that the FILED stamps follow the sealed one."""
    m = rv["macro"]
    if not m["pivots"]:
        return view["state"]
    k0 = min(range(len(m["pivots"])), key=lambda k: (m["pivots"][k][0],))
    cp = [(int(m["pivots"][k0][0]), 1 if m["pivots"][k0][2] == -1 else -1)]
    life = [(e["i"], 0 if e["event"] == "confirm"
             else (1 if e["side"] == "top" else -1))
            for e in m["events"] if e["event"] in ("confirm", "breakout-die")]
    return C._step_fill(pre.n, sorted(cp + life, key=lambda x: x[0]), 0, np.int8)


def _leak_confirm_early(pre, rv, view):
    """A LEAKED CONFIRM: every macro `confirm` and `breakout-die` latched
    CONFIRM_LEAK_BARS bars BEFORE the bar that produced it.  This is the leak
    F-RNG-ASOF names in one sentence — a feature reading a confirm stamped
    after its own bar — planted here on a copy of the honest view, and it must
    move the stamps."""
    v = dict(view)
    m = rv["macro"]
    cp = []
    if m["pivots"]:
        k0 = min(range(len(m["pivots"])),
                 key=lambda k: (m["seals"][k], m["pivots"][k][0]))
        cp.append((int(m["seals"][k0]),
                   1 if m["pivots"][k0][2] == -1 else -1))
    cp += [(max(0, int(e["i"]) - CONFIRM_LEAK_BARS),
            0 if e["event"] == "confirm" else (1 if e["side"] == "top" else -1))
           for e in m["events"] if e["event"] in ("confirm", "breakout-die")]
    v["state"] = C._step_fill(pre.n, sorted(cp, key=lambda x: x[0]), 0, np.int8)
    return v


def _late_index(idx, n: int):
    """A ONE-BAR-LATE READ: the stamp taken from the bar that closes AFTER the
    instant.  The as-of warranty on the row must fire on its own — this is the
    plant that proves `bar_close_ms <= instant_close_ms` is a GUARD and not a
    comment.  Clipped at the prefix's last bar so the plant tests the warranty
    and not numpy's bounds checking."""
    return np.minimum(np.asarray(idx) + 1, int(n) - 1)


def asof_break():
    return plants([
        ("leaked redraw (end-of-life top/bottom)",
         lambda: _asof_findings(("BTCUSDT",), view_edit=_leak_redraw, n_cuts=4)),
        ("leaked flip (known at the touch bar, not touch+HOLD)",
         lambda: _asof_findings(("BTCUSDT",), view_edit=_leak_flip, n_cuts=4)),
        (f"leaked confirm (every confirm / die latched {CONFIRM_LEAK_BARS} "
         f"bars early)",
         lambda: _asof_findings(("NEARUSDT",), view_edit=_leak_confirm_early,
                                n_cuts=4)),
        ("one-bar-late index (reads the bar closing after the instant)",
         lambda: _asof_findings(("BTCUSDT",), index_edit=_late_index, n_cuts=3)),
    ])


def asof_real():
    o = ctrl()["out"]
    inst = o["instants"]
    p = p4()
    ok, lines = True, []

    # (1) the warranty, on the filed rows themselves
    late = int((inst[p + "bar_close_ms"] > inst["instant_close_ms"]).sum())
    neg = int((inst[p + "bar_lag"] < 0).sum())
    g = (late == 0 and neg == 0)
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] WARRANTY on {len(inst):,} filed "
                 f"rows: bar_close_ms > instant_close_ms on {late}, negative "
                 f"lag on {neg}")

    # (2) the census layer, guarded INDEPENDENTLY — the knowable_at quirk
    quirk = []
    for a in TP.CLASSIC5:
        tape, _ = S.asof_layer(a, S.LENS_OF_RECORD)
        rv = C.run_scale(tape, S.FROZEN_SCALE)
        m = rv["macro"]
        neg_k = sum(1 for e in m["events"]
                    if e["event"] == "pivot" and int(e.get("knowable_at", 0)) < 0)
        bad_seal = [k for k in range(len(m["pivots"]))
                    if int(m["seals"][k]) <= int(m["pivots"][k][0])]
        quirk.append(f"{a}: knowable_at<0 pivots={neg_k}, seals not after "
                     f"their wick={len(bad_seal)}")
        if bad_seal:
            ok = False
    g = all("their wick=0" in q for q in quirk)
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] CENSUS LAYER, checked here and "
                 f"not taken on trust — every pivot's SEAL is strictly after "
                 f"its wick bar, on every asset: {'; '.join(quirk)}")
    if not g:
        lines.append("      *** THE CENSUS AS-OF LAYER LOOKS LEAKY — a pivot "
                     "is sealed at or before its own bar. STOP AND READ IT.")

    # (2b) and the seal LAW is doing work, on exactly the two assets whose
    # pivots carry the engine's knowable_at = -1: the naive wick reading and
    # the sealed reading DIFFER, and the filed stamps follow the sealed one.
    seal_lines = []
    for a in ("NEARUSDT", "SOLUSDT"):
        tape, view = S.asof_layer(a, S.LENS_OF_RECORD)
        rv = C.run_scale(tape, S.FROZEN_SCALE)
        wick = _wick_state(tape, rv, view)
        diff = int((wick != view["state"]).sum())
        first = int(np.flatnonzero(wick != view["state"])[0]) if diff else -1
        seal_lines.append(f"{a}: {diff} bar(s) differ, first at bar {first} "
                          f"(seal {min(rv['macro']['seals'])})")
        ok &= diff > 0
    lines.append(f"[{'OK ' if all('0 bar' not in s for s in seal_lines) else 'BAD'}"
                 f"] the SEAL law is load-bearing, not decorative: reading the "
                 f"first pivot at its WICK instead of its SEAL moves the state "
                 f"latch on both knowable_at = -1 assets — {'; '.join(seal_lines)} "
                 f"— and the filed stamps follow the SEALED reading (the "
                 f"prefix recompute below re-derives it from scratch)")

    # (3) THE PREFIX RECOMPUTE — the proof proper
    found = _asof_findings(TP.CLASSIC5)
    g = not found
    ok &= g
    n_cuts = sum(len(_cuts(inst, a)) for a in TP.CLASSIC5)
    lines.append(f"[{'OK ' if g else 'BAD'}] PREFIX RECOMPUTE over "
                 f"{len(TP.CLASSIC5)} assets x {n_cuts} seeded cuts "
                 f"(seed {SEED}): every stamp at or before each cut equals "
                 f"the filed stamp; disagreements: {found[:2] or 'none'}")

    # (4) the same, on the sensitivity seed — different cuts, same law [L8]
    found2 = _asof_findings(("NEARUSDT", "SOLUSDT"), n_cuts=5,
                            seed=SEED_LINEAGE)
    g = not found2
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] the same, on the lineage seed "
                 f"{SEED_LINEAGE}, over the two assets whose pivots carry the "
                 f"engine's knowable_at = -1: {found2[:2] or 'none'}")
    return ok, "\n".join(["", *[f"      {x}" for x in lines]])


# ═══════════════════════════════════════════════════ F-STAMP-JOIN · purity
def _join_findings(drop: int = 0, dup: int = 0, mutate: bool = False) -> list[str]:
    """Re-run the join on COPIES of the filed instants and stamp table, with a
    planted defect, and report what the purity checks see."""
    o = ctrl()["out"]
    inst = o["instants"]
    st = o["stamp_tables"][S.LENS_OF_RECORD].copy()
    base = inst[[c for c in inst.columns
                 if not c.startswith(S.prefix(S.LENS_OF_RECORD))]].copy()
    if drop:
        st = st.iloc[drop:].reset_index(drop=True)
    if dup:
        st = pd.concat([st, st.head(dup)], ignore_index=True)
    found = []
    try:
        j = S.join_stamps(base, st, S.LENS_OF_RECORD)
    except SystemExit as e:
        return [f"HALT: {e}"]
    except Exception as e:
        return [f"{e.__class__.__name__}: {e}"]
    if len(j) != len(base):
        found.append(f"row count {len(base)} -> {len(j)}")
    jr = o["trades"].copy()
    if mutate:
        jr.loc[0, "net_r"] = float(jr.loc[0, "net_r"]) + 1e-9
    if sha_df(jr) != sha_df(ctrl()["journal_before"]):
        found.append("the journal is not byte-identical to the unstamped book")
    return found


def join_break():
    return plants([
        ("a stamp row DROPPED (one campaign left unstamped)",
         lambda: _join_findings(drop=1)),
        ("a stamp row DUPLICATED (the join would multiply instants)",
         lambda: _join_findings(dup=1)),
        ("'stamping' MUTATES the book (net_r moved by 1e-9)",
         lambda: _join_findings(mutate=True)),
    ])


def join_real():
    o = ctrl()["out"]
    inst, jr = o["instants"], o["trades"]
    before = ctrl()["journal_before"]
    p = p4()
    ok, lines = True, []

    same_sha = sha_df(jr) == sha_df(before)
    same_cols = list(jr.columns) == list(before.columns)
    same_frame = bool(jr.equals(before))
    g = same_sha and same_cols and same_frame
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] THE BOOK IS UNTOUCHED: the "
                 f"stamped book's journal ({len(jr)} campaigns, "
                 f"{len(jr.columns)} columns) hashes to "
                 f"{sha_df(jr)[:16]}… — the unstamped book hashes to "
                 f"{sha_df(before)[:16]}… (columns identical={same_cols}, "
                 f"cell-for-cell equal={same_frame})")

    st = o["stamp_tables"][S.LENS_OF_RECORD]
    dup = int(st.duplicated(subset=["asset", "instant_ms", "instant_kind"]).sum())
    g = dup == 0
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] the stamp table is UNIQUE on "
                 f"[asset, instant_ms, instant_kind] ({len(st):,} rows, "
                 f"{dup} duplicate) — the m:1 side of a pure left-join")

    n_un = int(inst[p + "macro_state"].isna().sum())
    g = n_un == 0
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] every one of {len(inst):,} "
                 f"instants carries a stamp ({n_un} unstamped)")

    cids = set(inst.loc[inst["campaign_id"].notna(), "campaign_id"])
    want = {S.campaign_id(a, "card", int(m))
            for a, m in zip(jr["asset"], jr["entry_ms"])}
    g = cids == want and len(cids) == len(jr)
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] every campaign of the book is a "
                 f"unit of the funnel and no other is: {len(cids)} ids vs "
                 f"{len(jr)} campaigns, symmetric difference "
                 f"{len(cids ^ want)}")

    ent = inst[inst["instant_kind"] == "entry"]
    ex = inst[inst["instant_kind"] == "exit"]
    g = len(ent) == len(jr) and len(ex) == len(jr)
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] exactly one `entry` and one "
                 f"`exit` per campaign: {len(ent)} / {len(ex)} vs {len(jr)}")
    return ok, "\n".join(["", *[f"      {x}" for x in lines]])


# ═══════════════════════════════════════════════ F-STAMP-NULLS · no corpses
def _fill_forward(d: pd.DataFrame) -> pd.DataFrame:
    """THE PLANT: a stamp table whose geometry is forward-filled across the
    bars where no range is alive — the last corpse's box, carried forward."""
    e = d.copy()
    for f in S.GEOMETRY_FIELDS:
        e[f] = e[f].ffill()
    e["in_range"] = True
    return e


def mutated(name: str, value, real_leg) -> list[str]:
    """PLANT THE NAMED WRONG INTO THE MODULE and require the REAL LEG's own
    checks to go RED [the panel builder's `mutated()` idiom].  A break leg that
    re-implements the check locally proves the local copy works; this one
    proves the leg that is actually filed does.  Restored in `finally`, always.
    """
    orig = getattr(S, name)
    try:
        setattr(S, name, value)
        ok, detail = real_leg()
        # A FINDING here means the guard WORKED: the filed leg went RED under
        # the plant.  An empty list means it did not notice, and `plants` then
        # reports the fixture void — which is the only outcome worth fearing.
        return ([] if ok else
                [f"the REAL leg went RED with {name} planted (as it must)"])
    finally:
        setattr(S, name, orig)


def nulls_break():
    o = ctrl()["out"]

    def forward_filled():
        st = _fill_forward(o["stamp_tables"][S.LENS_OF_RECORD])
        base = o["instants"][[c for c in o["instants"].columns
                              if not c.startswith(p4())]].copy()
        j = base.merge(st.rename(columns={c: p4() + c for c in S.STAMP_FIELDS}),
                       on=["asset", "instant_ms", "instant_kind"], how="left")
        # in_range is forced True by the plant, so the audit is run against the
        # HONEST in-range mask: the question is whether a value survives a dead
        # range, not whether the liar admits the range is dead.
        j[p4() + "in_range"] = o["instants"][p4() + "in_range"].to_numpy()
        a = S.null_audit(j, S.LENS_OF_RECORD)
        return [f"{r['field']}: {r['n_nonnull_out_of_range']} non-null on "
                f"out-of-range rows" for _, r in a[a["violates"]].iterrows()]

    def state_forward_filled():
        """A `macro_state_of` that never says NONE — the corpse's state,
        carried into the warm-up.  The REAL leg must catch it."""
        return mutated("macro_state_of", lambda view, idx: "NEUTRAL", nulls_real)

    def geometry_survives_death():
        """A `stamps_at` that hands back a box on an OUT-OF-RANGE bar — the
        corpse, carried forward.  Planted in the module, the WHOLE door
        (`stamp_book`) is re-walked on a one-asset book and must HALT."""
        honest = S.stamps_at

        def leaky(tape, view, idx, close_ms):
            d = honest(tape, view, idx, close_ms)
            if idx >= 0 and not bool(view["in_range"][idx]):
                d["pct_of_range"], d["dev_top"] = 50.0, 1
            return d

        one = [t for t in ctrl()["book"] if t.symbol == "BTCUSDT"]
        return mutated("stamps_at", leaky,
                       lambda: (True, "stamp_book returned without a HALT")
                       if S.stamp_book(one, ("BTCUSDT",)) else (True, "?"))

    return plants([("geometry FORWARD-FILLED across dead ranges", forward_filled),
                   ("a macro_state that never says NONE (planted in the module)",
                    state_forward_filled),
                   ("a stamps_at that keeps the corpse's geometry",
                    geometry_survives_death)])


def nulls_real():
    o = ctrl()["out"]
    inst, nulls = o["instants"], o["nulls"]
    p = p4()
    ok, lines = True, []
    inr = inst[p + "in_range"].fillna(False).astype(bool)

    bad = nulls[nulls["violates"]]
    g = len(bad) == 0
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] THE FORWARD-FILL BAN: of "
                 f"{len(S.GEOMETRY_FIELDS)} geometry fields, "
                 f"{len(bad)} carry a value on an out-of-range row "
                 f"({int((~inr).sum()):,} such rows)")

    holes = [f for f in ("pct_of_range", "dist_boundary_atr", "boundary_age",
                         "dev_top", "dev_bot", "range_id")
             if int(inst.loc[inr, p + f].isna().sum())]
    g = not holes
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] and the other side of it: every "
                 f"in-range row ({int(inr.sum()):,}) carries every geometry "
                 f"field; holes: {holes or 'none'}")

    lf = int(inst.loc[~inr, p + "last_flip"].notna().sum())
    g = lf > 0
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] THE ONE STATED EXCEPTION: "
                 f"last_flip / last_flip_age survive a dead range by "
                 f"definition — {lf:,} out-of-range rows carry one, which is "
                 f"the leash outliving its box, not a forward fill")

    # the NONE branch, exercised where the control cannot reach it
    none_seen = []
    for a in TP.CLASSIC5:
        tape, view = S.asof_layer(a, S.LENS_OF_RECORD)
        st0 = S.stamps_at(tape, view, 0, int(tape.t0[0]) + tape.step)
        stm1 = S.stamps_at(tape, view, -1, int(tape.t0[0]))
        none_seen.append(st0["macro_state"] == "NONE"
                         and stm1["macro_state"] == "NONE"
                         and all(st0[f] is None for f in S.GEOMETRY_FIELDS)
                         and all(stm1[f] is None for f in S.GEOMETRY_FIELDS))
    g = all(none_seen)
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] macro_state = 'NONE' with every "
                 f"geometry field null before the machine's first seal, and "
                 f"at idx = -1 (no bar closed yet), on "
                 f"{sum(none_seen)}/{len(none_seen)} assets — the branch the "
                 f"control's own corridor never reaches (it starts at bar 316)")

    vals = set(inst[p + "macro_state"])
    g = vals <= set(S.MACRO_STATES)
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] macro_state takes only the four "
                 f"declared values; seen: {sorted(vals)}")

    odd = int((inr & (inst[p + "state_latch"] != "NEUTRAL")).sum())
    lines.append(f"[   ] DISCLOSURE: rows inside a live range whose RAW latch "
                 f"is not NEUTRAL: {odd} (the four-valued collapse [LEAN S-a] "
                 f"is auditable from `state_latch`, not assumed)")
    return ok, "\n".join(["", *[f"      {x}" for x in lines]])


# ═══════════════════════════════════════════ F-STAMP-FUNNEL · the extractor
def _copy_trade(t, **kw):
    """A COPY of a campaign record with fields moved — the original book is
    never touched by a break leg."""
    c = copy.copy(t)
    for k, v in kw.items():
        object.__setattr__(c, k, v)
    return c


def _copy_arm(a, **kw):
    c = copy.copy(a)
    for k, v in kw.items():
        setattr(c, k, v)
    return c


def funnel_break():
    c = ctrl()
    asset = "BTCUSDT"
    arms = list(c["arms"][asset])
    trades = [t for t in c["book"] if t.symbol == asset]
    f = S.LaneBars(asset, S.LENS_OF_RECORD)
    lo_i, hi_i = T7._idx_range(f.open_ms, int(c["lo_ms"]), int(c["hi_ms"]))
    lo_i = max(lo_i, T9.V6_ROLES.floor_bars)

    def flipped_latch():
        t = _copy_trade(trades[0], reached_1r=not bool(trades[0].reached_1r))
        S.campaign_instants(t, f)
        return []

    def unknown_reason():
        bad = [_copy_arm(a, reject="vibes") for a in arms]
        S.funnel_instants_asset(asset, bad, trades, f, lo_i, hi_i)
        return []

    def arm_out_of_window():
        bad = [_copy_arm(arms[0], arm_i=lo_i - 1)] + arms[1:]
        S.funnel_instants_asset(asset, bad, trades, f, lo_i, hi_i)
        return []

    def lens_mismatch():
        t = _copy_trade(trades[0], entry_i=int(trades[0].entry_i) + 3)
        S.campaign_instants(t, f)
        return []

    def orphan_campaign():
        S.funnel_instants_asset(asset, [a for a in arms if not a.entered],
                                trades, f, lo_i, hi_i)
        return []

    return plants([("a campaign whose +1R latch is flipped", flipped_latch),
                   ("an arming with a reject reason the ladder has no bar for",
                    unknown_reason),
                   ("an arming outside the book's own window", arm_out_of_window),
                   ("a campaign whose entry_i does not open at entry_ms",
                    lens_mismatch),
                   ("a campaign with no arming in the funnel", orphan_campaign)])


def funnel_real():
    c = ctrl()
    o = c["out"]
    inst = o["instants"]
    ok, lines = True, []

    tally = S.funnel_tally(o)
    g = bool(tally["partition_holds"].all())
    ok &= g
    row = tally[tally["asset"] == "__ALL__"].iloc[0]
    lines.append(f"[{'OK ' if g else 'BAD'}] THE FUNNEL IS A PARTITION: "
                 f"{int(row['armings'])} armings = {int(row['entered'])} "
                 f"entered + tide {int(row['reject_tide'])} + d "
                 f"{int(row['reject_d'])} + no_trigger "
                 f"{int(row['reject_no_trigger'])} + position_open "
                 f"{int(row['reject_position_open'])} + unset "
                 f"{int(row['reject_unset'])}")

    kinds = set(inst["instant_kind"])
    missing = [k for k in S.INSTANT_KINDS if k not in kinds]
    stray = sorted(kinds - set(S.INSTANT_KINDS))
    g = not missing and not stray
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] the vocabulary is exercised and "
                 f"closed: {len(kinds)}/{len(S.INSTANT_KINDS)} declared kinds "
                 f"present (absent: {missing or 'none'}), kinds outside the "
                 f"vocabulary: {stray or 'none'}")

    # window_open IS the arming bar on card v6 [LEAN S-d]
    a_ = inst[inst["instant_kind"] == "arming"][["unit_id", "instant_ms"]]
    w_ = inst[inst["instant_kind"] == "window_open"][["unit_id", "instant_ms"]]
    m = a_.merge(w_, on="unit_id", suffixes=("_a", "_w"))
    g = len(m) == len(a_) and bool((m["instant_ms_a"] == m["instant_ms_w"]).all())
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] [LEAN S-d] `window_open` sits on "
                 f"the arming bar on all {len(m)} armings — equal BY "
                 f"CONSTRUCTION on card v6, kept as its own kind so a later "
                 f"card needs no new vocabulary")

    # the +1R instant IS the card's own latch, on every campaign
    jr = o["trades"]
    n1 = int(jr["reached_1r"].astype(bool).sum())
    got = int((inst["instant_kind"] == "plus_1r").sum())
    g = n1 == got
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] [LEAN S-b] one `plus_1r` instant "
                 f"per campaign the ride latched and none else: {got} vs "
                 f"{n1} campaigns with reached_1r")

    # the reject ladder: each reason where it became knowable
    rj = inst[inst["instant_kind"] == "reject"]
    tide_d = rj[rj["reject_reason"].isin(("tide", "d"))]
    arm_ms = dict(zip(a_["unit_id"], a_["instant_ms"]))
    g = bool(all(int(r["instant_ms"]) == int(arm_ms[r["unit_id"]])
                 for _, r in tide_d.iterrows()))
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] [LEAN S-c] every tide/d reject "
                 f"({len(tide_d)}) is stamped AT its arming bar, and every "
                 f"no_trigger reject ({int((rj['reject_reason'] == 'no_trigger').sum())}) "
                 f"strictly after it "
                 f"({int(sum(int(r['instant_ms']) > int(arm_ms[r['unit_id']]) for _, r in rj[rj['reject_reason'] == 'no_trigger'].iterrows()))} "
                 f"of them)")

    # nothing is stamped past the corridor end
    late = int((inst["instant_close_ms"] > int(c["hi_ms"]) + 1).sum())
    g = late == 0
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] no instant closes after the "
                 f"book's corridor end {S.iso(int(c['hi_ms']) + 1)}: {late}")

    # every reject row carries the law that placed it
    g = bool(rj["reject_bar_law"].notna().all())
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] every one of {len(rj)} reject "
                 f"rows carries REJECT_BAR_LAW in a column, not in a caption")
    return ok, "\n".join(["", *[f"      {x}" for x in lines]])


# ═══════════════════════════════ F-STAMP-CLOSURE · captured, not consulted
RANGE_IMPORT_LINE = re.compile(          # OR-1 F-BR-14's regex, verbatim
    r"(?m)^[ \t]*(?:from|import)[ \t]+[^\n#]*\brangefinder\b")


def _closure(modname: str, shadow_src: str | None = None) -> set[str]:
    """Modules a CLEAN interpreter loads by importing `modname`.  With
    `shadow_src` a PLANTED copy is written as <modname>.py into a throwaway
    directory that goes FIRST on the subprocess's path — it shadows the real
    module there and nowhere else.  NO FILE IN THE REPO IS TOUCHED."""
    env = dict(os.environ)
    with tempfile.TemporaryDirectory(prefix="f-stamp-closure-") as td:
        if shadow_src is not None:
            (Path(td) / f"{modname}.py").write_text(shadow_src, encoding="utf-8")
        code = ("import sys, json; sys.dont_write_bytecode = True; "
                f"sys.path.insert(0, {str(ROOT)!r}); "
                f"sys.path.insert(0, {str(ROOT / 'scripts')!r}); "
                + (f"sys.path.insert(0, {td!r}); " if shadow_src is not None
                   else "")
                + "before = set(sys.modules); "
                f"import {modname}; "
                "print(json.dumps(sorted(set(sys.modules) - before)))")
        out = subprocess.run([PY, "-c", code], cwd=ROOT, capture_output=True,
                             text=True, timeout=900, env=env)
    if out.returncode != 0:
        raise RuntimeError(out.stderr[-400:])
    return set(json.loads(out.stdout.strip().splitlines()[-1]))


def _reach(closure: set[str]) -> list[str]:
    """Every module of a closure that matches a forbidden name, on any dotted
    part — `analytics.rangefinder_census` and `engine.rangefinder` alike."""
    hits = []
    for m in sorted(closure):
        parts = m.split(".")
        for bad in S.FORBIDDEN_IN_DECISION:
            if any(bad in p for p in parts):
                hits.append(m)
                break
    return hits


def _static_hits(src: str) -> list[str]:
    """What a DECISION module's source may not contain.  AST, so prose and
    docstrings cannot trip it — and `ast.walk` descends into function bodies,
    which is the whole point: a LAZY `import tierc10_stamps` inside a rule
    function never appears in an import closure, and would be invisible to the
    subprocess leg above."""
    hits = []
    tree = ast.parse(src)
    for node in ast.walk(tree):
        names = ([al.name for al in node.names]
                 if isinstance(node, ast.Import) else
                 [node.module or ""] + [al.name for al in node.names]
                 if isinstance(node, ast.ImportFrom) else [])
        for n in names:
            for bad in S.FORBIDDEN_IN_DECISION:
                if bad in n:
                    hits.append(f"import {n}")
        # a stamp column, read by name, is the wall breached from the inside
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            for lens in S.LENS_MS:
                if node.value.startswith(S.STAMP_COLUMN_PREFIX + lens + "_"):
                    hits.append(f"stamp column literal {node.value!r}")
    hits += [f"F-BR-14 line: {m.group(0).strip()}"
             for m in RANGE_IMPORT_LINE.finditer(src)]
    return hits


def closure_break():
    t9 = (ROOT / "scripts" / "tierc9.py").read_text()
    r7 = (ROOT / "scripts" / "tierc7_rules.py").read_text()

    def _after_future(src: str, line: str) -> str:
        """A planted import goes AFTER `from __future__`, which must be the
        first statement of a module — otherwise the plant proves only that
        Python enforces its own grammar."""
        anchor = "from __future__ import annotations"
        if anchor not in src:
            return line + "\n" + src
        return src.replace(anchor, anchor + "\n" + line, 1)

    def top_level_range():
        c = _closure("tierc9", _after_future(
            t9, "from analytics import rangefinder_census as _X"))
        return _reach(c)

    def rules_census():
        c = _closure("tierc7_rules", r7 + "\nimport tierc10_census\n")
        return _reach(c)

    def lazy_in_function():
        # THE LEG THAT EARNS THE AST SCAN: a lazy import is loaded only when
        # the function runs, so an import CLOSURE never sees it.  The plant is
        # caught by the static scan alone, and the closure's silence is
        # reported beside it as the reason the scan exists.
        src = (t9 + "\n\ndef _late_look(row):\n    import tierc10_stamps\n"
                    "    return tierc10_stamps.stamps_at\n")
        seen_by_closure = _reach(_closure("tierc9", src))
        hits = _static_hits(src)
        return ([f"{hits[0]} (the import CLOSURE saw "
                 f"{seen_by_closure or 'NOTHING'} — which is why the scan is "
                 f"here)"] if hits else [])

    def stamp_column_read():
        src = r7 + "\n\ndef _gate(row):\n    return row['rf4h_macro_state']\n"
        return _static_hits(src)

    def range_import_line():
        return _static_hits(r7 + "\n    from engine import rangefinder\n")

    return plants([("a TOP-LEVEL range import in the runner", top_level_range),
                   ("a census import in a *_rules module", rules_census),
                   ("a LAZY in-function stamp import (a closure cannot see it)",
                    lazy_in_function),
                   ("a decision function reading a STAMP COLUMN by name",
                    stamp_column_read),
                   ("an indented range import (F-BR-14's own regex)",
                    range_import_line)])


def closure_real():
    ok, lines = True, []
    for mod in ("tierc7_rules", "tierc9"):
        c = _closure(mod)
        hits = _reach(c)
        g = not hits
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] CLOSURE of `{mod}` (the v6 "
                     f"{'rules chain' if mod.endswith('_rules') else 'control path'}): "
                     f"{len(c)} modules, forbidden reached: {hits or 'NONE'}")
    for name in S.DECISION_MODULES:
        src = (ROOT / "scripts" / f"{name}.py").read_text()
        hits = _static_hits(src)
        g = not hits
        ok &= g
        clean = "no forbidden import, no stamp column read"
        lines.append(f"[{'OK ' if g else 'BAD'}] AST SCAN of {name}.py "
                     f"(function bodies included — a lazy import is invisible "
                     f"to a closure): {hits or clean}")
    c = _closure("tierc10_stamps")
    has = sorted(m for m in c if "rangefinder" in m or m.startswith("tierc10_"))
    g = "tierc10_census" in c and any("rangefinder" in m for m in c)
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] AND THE OTHER SIDE OF THE WALL: "
                 f"`tierc10_stamps` DOES reach the census and the port "
                 f"({has}) — it is meant to. The law is one-directional: the "
                 f"capture may read the range machinery, the decision may not "
                 f"read the capture.")
    lines.append(f"[   ] the order is the law: `stamp_book` takes a book that "
                 f"has ALREADY been ridden and returns no object a rule card "
                 f"can read; the spring/BRK lanes consume range EVENTS as "
                 f"precomputed ARGUMENTS in their own harness, and no stamp "
                 f"is an input to any decision.")
    return ok, "\n".join(["", *[f"      {x}" for x in lines]])


# ═══════════════════ F-STAMP-JOURNAL · the same stamps from the smaller record
SHARED_KINDS = ("arming", "entry", "anchor_bar", "harvest", "bell", "exit")


def journal_break():
    jr = ctrl()["journal_before"]

    def blind_kinds_claimed():
        """A journal path that CLAIMS the kinds a journal cannot carry.  The
        REAL leg must catch the lie."""
        honest = S.journal_instants

        def liar(row, f):
            out = honest(row, f)
            ei = f.bar_of(int(row["entry_ms"]), "entry_ms")
            out.append(S._row(S.campaign_id(str(row["asset"]),
                                            str(row["lane"]),
                                            int(row["entry_ms"])),
                              "campaign", str(row["asset"]), str(row["lane"]),
                              1, "advance", ei, int(row["entry_ms"]), seq=1))
            return out
        return mutated("journal_instants", liar, journal_real)

    def moved_entry():
        bad = jr.copy()
        bad.loc[0, "entry_ms"] = int(bad.loc[0, "entry_ms"]) + 1
        S.stamp_book(bad, TP.CLASSIC5)
        return []

    def asset_outside_panel():
        bad = jr.copy()
        bad.loc[0, "asset"] = "DOGEUSDT"
        S.stamp_book(bad, TP.CLASSIC5)
        return []

    return plants([("a journal path claiming an `advance` it cannot know",
                    blind_kinds_claimed),
                   ("a journal row whose entry_ms is not a bar open",
                    moved_entry),
                   ("a journal row on an asset outside the declared panel",
                    asset_outside_panel)])


def journal_real():
    c = ctrl()
    o = c["out"]
    oj = S.stamp_book(c["journal_before"], TP.CLASSIC5)
    ji, bi = oj["instants"], o["instants"]
    p = p4()
    ok, lines = True, []

    g = set(oj["meta"]["kinds_unavailable"]) == set(S.JOURNAL_BLIND)
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] the journal path SAYS WHAT IT "
                 f"CANNOT SEE: {sorted(oj['meta']['kinds_unavailable'])} — "
                 f"declared in meta, counted in coverage, never faked")

    kinds = set(ji["instant_kind"])
    g = kinds <= set(SHARED_KINDS) and not (kinds & set(S.JOURNAL_BLIND))
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] and it emits only those: "
                 f"{sorted(kinds)}")

    # THE CROSS-CHECK: where both paths CAN speak, they must say the same thing
    keep = [c_ for c_ in (p + f for f in S.STAMP_FIELDS)]
    a = (bi[bi["instant_kind"].isin(SHARED_KINDS) & bi["campaign_id"].notna()]
         .set_index(["campaign_id", "instant_kind"])[keep].sort_index())
    b = (ji[ji["instant_kind"].isin(SHARED_KINDS)]
         .set_index(["campaign_id", "instant_kind"])[keep].sort_index())
    # the Book path also emits `arming` rows for armings that never entered —
    # those have no campaign_id and are excluded above, by construction.
    common = a.index.intersection(b.index)
    bad = 0
    for k in common:
        ra, rb = a.loc[k], b.loc[k]
        if not all(_same(ra[c_], rb[c_]) for c_ in keep):
            bad += 1
    g = bad == 0 and len(common) == len(b) and len(b) > 0
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] THE TWO PATHS AGREE: of "
                 f"{len(b):,} journal instants, {len(common):,} match a Book "
                 f"instant on (campaign_id, kind) and {bad} disagree on any "
                 f"of the {len(keep)} stamp fields")

    miss = sorted(set(b.index) - set(a.index))
    g = not miss
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] and the journal invents nothing "
                 f"the Book did not have: {miss[:2] or 'none'}")
    return ok, "\n".join(["", *[f"      {x}" for x in lines]])


# ══════════════════════════ F-STAMP-LENS · a lane on another lens, both ways
SYNTH_NOTE = ("SYNTHETIC CAMPAIGNS — no rule was evaluated, no stop, no cost, "
              "no accounting, no number scored. They are index carriers whose "
              "only job is to drive the two-lens join, laid on REAL BTCUSDT 5m "
              "bars (a Tier-E read of the frozen snapshot, which LAW 4 allows "
              "and which no lane rides).")
SYNTH_N = 24                    # campaigns; bars drawn by a SEEDED rng, printed


def _synth_5m_book():
    """A book on the 5m lens, built by moving a real campaign's INDICES only.

    Every field that could carry a result is neutralised: R is set enormous so
    the +1R latch can never fire (and `reached_1r` is False, so the extractor's
    own agreement check has something to agree with), there are no advances, no
    harvest, no anchor bar.  What survives is exactly what the join needs: an
    asset, a lens, and bars.
    """
    tape = C.load_tape("BTCUSDT", "5m")
    rng = np.random.default_rng(SEED)
    base = ctrl()["book"][0]
    lo, hi = 400, tape.n - 400
    starts = sorted(set(int(v) for v in rng.integers(lo, hi, size=SYNTH_N)))
    out = []
    for i in starts:
        j = min(i + 60, tape.n - 1)
        out.append(dataclasses.replace(
            base, symbol="BTCUSDT", lane="synthetic-5m",
            arm_i=i, arm_ms=int(tape.t0[i]),
            entry_i=i, entry_ms=int(tape.t0[i]), entry_px=float(tape.c[i]),
            r_dist=1e12, atr_at_entry=1e12, anchor=0.0, anchor_bar_ms=-1,
            stop_px=float(tape.c[i]), final_stop_px=float(tape.c[i]),
            stop_advanced_atr=0.0, ratchet_exit=False,
            exit_i=j, exit_ms=int(tape.t0[j]), exit_px=float(tape.c[j]),
            exit_reason="corridor_end", bars_held=j - i,
            advances=[], harvested=False, harvest_i=None, harvest_ms=None,
            harvest_px=None, harvest_unit_move_r=None,
            harvest_ride_would_have_r=None, harvest_blocked_by="",
            reached_1r=False, mae_to_1r_r=None, mfe_r=0.0,
            # EVERY RESULT-SHAPED FIELD IS ZEROED.  Nothing here is a number
            # anyone could mistake for an outcome, and nothing is scored.
            gross_r=0.0, fee_r=0.0, funding_r=0.0, funding_r_uncapped=0.0,
            funding_ceiling_bound=False, net_r=0.0,
            net_r_harvest_half=None, net_r_runner_half=None,
            net_r_bellonly=None, adds=[], add_r=None, spring=None))
    return out, tape, starts


def lens_break():
    syn, tape, _ = _synth_5m_book()

    def arms_on_a_5m_lane():
        S.stamp_book(syn, ("BTCUSDT",), lens="5m",
                     arms={"BTCUSDT": list(ctrl()["arms"]["BTCUSDT"])},
                     lo_ms=ctrl()["lo_ms"], hi_ms=ctrl()["hi_ms"])
        return []

    def five_minute_index_on_a_4h_frame():
        bad = [dataclasses.replace(syn[0], entry_i=int(syn[0].entry_i))]
        S.stamp_book(bad, ("BTCUSDT",), lens="4h")      # 5m indices, 4h frame
        return []

    def reads_the_forming_4h_bar():
        """THE PLANT THE CROSS-LENS LAW EXISTS FOR: anchor a 5m instant a full
        4h bar LATER, so the stamp reads the bar that is still forming at the
        instant.  The warranty in `stamps_at` must fire."""
        t4, v4 = S.asof_layer("BTCUSDT", "4h")
        ms = int(tape.t0[syn[0].entry_i]) + S.LENS_MS["5m"]
        idx = int(C.asof_index(t4, np.int64(ms + S.LENS_MS["4h"])))
        S.stamps_at(t4, v4, idx, ms)
        return []

    def unknown_lens():
        S.stamp_book(syn, ("BTCUSDT",), lens="3h")
        return []

    return plants([("armings offered for a 5m lane", arms_on_a_5m_lane),
                   ("5m bar indices read off the 4h frame",
                    five_minute_index_on_a_4h_frame),
                   ("a 5m instant stamped from the FORMING 4h bar",
                    reads_the_forming_4h_bar),
                   ("a lens the census does not carry", unknown_lens)])


def lens_real():
    syn, tape, starts = _synth_5m_book()
    o = S.stamp_book(syn, ("BTCUSDT",), lens="5m")
    inst = o["instants"]
    ok, lines = True, []
    lines.append(f"[   ] {SYNTH_NOTE}")
    lines.append(f"      seed {SEED} drew {len(starts)} 5m start bars, first "
                 f"{starts[0]} last {starts[-1]} of {tape.n:,}")

    g = o["meta"]["stamp_lenses"] == ["4h", "5m"]
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] a lane on another lens is stamped "
                 f"on BOTH: {o['meta']['stamp_lenses']} — the 4h lens of "
                 f"record AND the lane's own")

    have4 = [c for c in inst.columns if c.startswith("rf4h_")]
    have5 = [c for c in inst.columns if c.startswith("rf5m_")]
    g = (len(have4) == len(S.STAMP_FIELDS) == len(have5)
         and not set(have4) & set(have5))
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] the two lenses' columns are "
                 f"prefixed and disjoint: {len(have4)} rf4h_* + {len(have5)} "
                 f"rf5m_*, overlap {len(set(have4) & set(have5))}")

    late4 = int((inst["rf4h_bar_close_ms"] > inst["instant_close_ms"]).sum())
    late5 = int((inst["rf5m_bar_close_ms"] > inst["instant_close_ms"]).sum())
    g = late4 == 0 and late5 == 0
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] NO FORMING BAR IS EVER READ: 4h "
                 f"stamps ahead of their instant {late4}, 5m stamps ahead "
                 f"{late5}, over {len(inst)} instants")

    lag4, lag5 = inst["rf4h_bar_lag"].astype(int), inst["rf5m_bar_lag"].astype(int)
    ms4 = inst["rf4h_bar_lag_ms"].astype(int)
    ms5 = inst["rf5m_bar_lag_ms"].astype(int)
    g = (bool((lag5 == 0).all()) and bool((ms5 == 0).all())
         and bool((lag4 == 0).all())
         and bool((ms4 >= 0).all()) and int(ms4.max()) < S.LENS_MS["4h"]
         and int((ms4 > 0).sum()) > 0)
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] AND THE LAG SAYS WHICH BAR IT "
                 f"READ: the 5m stamp is the instant's OWN bar (lag 0 bars, "
                 f"0 ms on every row); the 4h stamp is the 4h bar that had "
                 f"JUST closed (lag 0 whole bars on every row, "
                 f"{int(ms4.min())}..{int(ms4.max())} ms — "
                 f"{int((ms4 > 0).sum())}/{len(inst)} instants stood strictly "
                 f"INSIDE a forming 4h bar and read the one before it, which "
                 f"is what as-of on a coarser lens MEANS)")

    # the 4h stamp of a 5m instant IS the stamp of the last closed 4h bar,
    # recomputed here from the 4h tape and not taken from the join
    t4, v4 = S.asof_layer("BTCUSDT", "4h")
    bad = 0
    for _, r in inst.head(200).iterrows():
        k = int(C.asof_index(t4, np.int64(int(r["instant_close_ms"]))))
        want = S.stamps_at(t4, v4, k, int(r["instant_close_ms"]))
        if not all(_same(want[f], r["rf4h_" + f]) for f in S.STAMP_FIELDS):
            bad += 1
    g = bad == 0
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] the 4h stamp on a 5m instant, "
                 f"recomputed independently from the 4h tape: {bad} "
                 f"disagreement(s) over the first 200 instants")
    return ok, "\n".join(["", *[f"      {x}" for x in lines]])


# ═══════════════════════════════════════════════════════ F-DET and F-KEY
def det_break():
    def perturbed():
        if not (OUT / "build_manifest.json").exists():
            return ["no filed root to compare"]
        with tempfile.TemporaryDirectory(prefix="f-stamp-det-") as td:
            a, b = Path(td) / "a", Path(td) / "b"
            shutil.copytree(OUT, a)
            shutil.copytree(OUT_RERUN, b)
            d = pd.read_parquet(b / "stamp_coverage.parquet")
            d.loc[0, "stamped"] = int(d.loc[0, "stamped"]) + 1
            d.to_parquet(b / "stamp_coverage.parquet", index=False)
            okd, ls = TP.check_det(a, b)
            return [] if okd else [l for l in ls if "BAD" in l]

    return plants([("one number moved in a COPY of the twin root", perturbed)])


def det_real():
    if not (OUT_RERUN / "build_manifest.json").exists():
        return False, (f"the F-DET twin is missing — run "
                       f"`tierc10_stamps.py --rerun` first ({OUT_RERUN})")
    okd, lines = TP.check_det(OUT, OUT_RERUN)
    man = json.loads((OUT / "build_manifest.json").read_text())
    lines.append(f"[   ] seed {man['seed']} · echo {man['seed_lineage']} · "
                 f"SCALE {man['scale_mult']} · code sha "
                 f"{man['code_sha'][:16]}… · census sha "
                 f"{man['census_code_sha'][:16]}…")
    return okd, "\n".join(["", *[f"      {x}" for x in lines]])


def key_break():
    def missing_asof():
        with tempfile.TemporaryDirectory(prefix="f-stamp-key-") as td:
            r = Path(td) / "r"
            shutil.copytree(OUT, r)
            d = pd.read_parquet(r / "stamp_defs.parquet").drop(
                columns=["as_of_lens"])
            d.to_parquet(r / "stamp_defs.parquet", index=False)
            okk, ls = TP.check_keys(r)
            return [] if okk else [l for l in ls if "BAD" in l]

    def duplicate_key():
        with tempfile.TemporaryDirectory(prefix="f-stamp-key2-") as td:
            r = Path(td) / "r"
            shutil.copytree(OUT, r)
            d = pd.read_parquet(r / "stamp_defs.parquet")
            pd.concat([d, d.head(1)], ignore_index=True).to_parquet(
                r / "stamp_defs.parquet", index=False)
            okk, ls = TP.check_keys(r)
            return [] if okk else [l for l in ls if "BAD" in l]

    return plants([("an as-of column removed from a COPY of a filed table",
                    missing_asof),
                   ("a duplicate key row in a COPY of a filed table",
                    duplicate_key)])


def key_real():
    okk, lines = TP.check_keys(OUT)
    return okk, "\n".join(["", *[f"      {x}" for x in lines]])


# ═══════════════════════════════════════════════════════════════ the driver
FIXTURES = (
    ("F-STAMP-ASOF", "the stamps are AS-OF — proved by PREFIX RECOMPUTE",
     "any stamp recomputed from tape[:t] differs from the filed stamp for an "
     "instant at or before t; or a filed row reads a bar that closed after its "
     "own instant; or a pivot's seal is not strictly after its wick bar",
     asof_break, asof_real),
    ("F-STAMP-JOIN", "the stamps are a PURE LEFT-JOIN and the book is untouched",
     "the stamped book's journal is not byte-identical to the unstamped book; "
     "or the join drops, multiplies or fails to stamp one instant; or a "
     "campaign of the book is not a unit of the funnel",
     join_break, join_real),
    ("F-STAMP-NULLS", "no dead range is ever forward-filled",
     "one geometry field carries a value on a row where no macro range was "
     "alive; or an in-range row is missing one; or macro_state is not 'NONE' "
     "where nothing was knowable",
     nulls_break, nulls_real),
    ("F-STAMP-FUNNEL", "the funnel is a partition and every instant is the "
     "card's own",
     "the armings do not partition into their terminal reasons; or the +1R "
     "instant count differs from the ride's own latch; or a reject is stamped "
     "anywhere but where it became knowable; or an instant closes after the "
     "book's corridor end",
     funnel_break, funnel_real),
    ("F-STAMP-CLOSURE", "CAPTURED, NOT CONSULTED — extended to the stamps",
     "the v6 decision closure reaches tierc10_stamps, tierc10_census or "
     "anything named rangefinder; or a decision module's source holds such an "
     "import ANYWHERE (function bodies included) or reads a stamp column by "
     "name",
     closure_break, closure_real),
    ("F-STAMP-JOURNAL", "the same door on the smaller record — and it says "
     "what it cannot see",
     "the journal path emits an instant kind a journal row cannot know; or a "
     "stamp taken through the journal differs from the one taken through the "
     "Book on the same (campaign, kind); or the shortfall is not declared",
     journal_break, journal_real),
    ("F-STAMP-LENS", "a lane on another lens is stamped on BOTH, and never "
     "reads a forming bar",
     "a lane on a lens other than 4h is not also stamped on the 4h lens of "
     "record; or the two lenses' columns collide; or a coarse-lens stamp reads "
     "a bar that was still forming at the instant; or the 4h stamp of a 5m "
     "instant differs from the 4h tape's own",
     lens_break, lens_real),
    ("F-DET", "two runs, byte-identical",
     "a content sha moves between the two roots, or an independent byte "
     "re-hash of any parquet pair differs",
     det_break, det_real),
    ("F-KEY", "every table keyed, unique, and warranted",
     "a filed table has no declared key, a duplicate key row, or is missing "
     "one of the nine as-of columns",
     key_break, key_real),
)


def main() -> int:
    pick = [a for a in sys.argv[1:] if not a.startswith("--")]
    root = OUT
    for a in sys.argv[1:]:
        if a.startswith("--root="):
            root = Path(a.split("=", 1)[1])
    man_p = root / "build_manifest.json"
    if not man_p.exists():
        raise SystemExit(f"HALT: no build at {root} — run "
                         f"`~/venvs/naiad/bin/python -B scripts/"
                         f"tierc10_stamps.py` first")
    man = json.loads(man_p.read_text())
    say("=" * 78)
    say("TIER-C10 · STAGE A — FIXTURES FOR THE TAPE AND THE STAMPS")
    say("=" * 78)
    say(f"  as_of_last_closed_4h {man['as_of_last_closed_4h']}  ·  substrate "
        f"{man['substrate']}")
    say(f"  seed {SEED} · sensitivity echo {SEED_LINEAGE} · SCALE_MULT "
        f"{man['scale_mult']} (FROZEN) · lens of record {man['lens_of_record']}")
    say(f"  book {man['book']}")
    say(f"  {man['counts']['instants']:,} instants · "
        f"{man['counts']['units']:,} units · "
        f"{man['counts']['campaigns']} campaigns · "
        f"{man['counts']['armings']:,} armings")
    say("")
    for s in S.LEANS:
        say(f"  {s}")

    chosen = [f for f in FIXTURES
              if not pick or any(q.lower() in f[0].lower() for q in pick)]
    for name, title, fails_if, b, r in chosen:
        prove(name, title, fails_if, b, r)

    say("")
    say("=" * 78)
    say(f"  {len(PASSED)} GREEN, {len(FAILED)} RED "
        f"({len(chosen)} fixture(s) run)")
    for f in FAILED:
        say(f"    RED: {f}")
    say("=" * 78)
    name = TRANSCRIPT if not pick else TRANSCRIPT.replace(".txt", "_partial.txt")
    (root / name).write_text("\n".join(LINES) + "\n")
    print(f"\n  transcript -> {root / name}")
    return 1 if FAILED else 0


if __name__ == "__main__":
    raise SystemExit(main())
