"""TIER-C7-C + TIER-C8 — THE FIXTURES.

EVERY LEG STATES INLINE WHAT WOULD MAKE IT FAIL.  The three banned failure
modes, by name: a check that re-derives a value the way the program derived it
and compares it to itself; a check satisfied by ONE example where cardinality
was possible; and a magnitude bound tuned until the suite goes green.

AND A FOURTH, NEW THIS TIER: a check whose CLAIM is not the claim the design
makes.  F-C8-MATCH began life asserting "identical advance-opportunity counts
per campaign across all cells" — which is FALSE and cannot be made true, because
a different anchor gives a different stop, a different exit and therefore a
different number of bars to have opportunities in.  The design's real claim is
narrower and exactly checkable, and the leg now makes THAT one.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import tierc8 as T8                                                  # noqa: E402
import tierc7 as T7                                                  # noqa: E402
import tierc7_rules as RC                                            # noqa: E402
import tierc6 as T6                                                  # noqa: E402
import tierc6_rules as V6                                            # noqa: E402
import tierc5_rules as V5                                            # noqa: E402
import tierc4_fixtures as F4                                         # noqa: E402
import analytics as AN                                               # noqa: E402

T: list[str] = []
RESULTS: dict[str, bool] = {}
_B: dict = {}


def rec(fid, ok, lines):
    RESULTS[fid] = bool(ok)
    T.append(f"--- {fid} : {'PASS' if ok else 'FAIL'} ---")
    T.extend("    " + x for x in lines)
    return bool(ok)


def tbl(n, root=None):
    return pd.read_parquet((root or T8.OUT) / f"{n}.parquet")


def books():
    if not _B:
        lo, hi, meta = T8.corridor()
        _B.update({"lo": lo, "hi": hi, "meta": meta,
                   "control": T8.run_cell(T8.CARD_V6_CONTROL, lo, hi),
                   "chain": T8.run_cell(T8.CARD_CHAIN2, lo, hi),
                   "ae": T8.run_cell(T8.CARD_AE2, lo, hi),
                   "anchor": T8.run_cell(T8.CARD_ANC1, lo, hi)})
    return _B


def f_ctrl():
    """FAILS IF: the v8 code path does not reproduce card v6 at 0.000e+00.

    The commission sets the bar at EXACTLY zero, not 1e-05, and that is
    achievable because the control turns every v8 knob off and the arithmetic is
    the parent's.  A non-zero difference at any tolerance means new code moved
    an old number."""
    lines, ok = [], True
    B = books()
    got = T8.journal_frame(B["control"]).sort_values(
        ["asset", "entry_ms"]).reset_index(drop=True)
    want = T8.journal_frame(T6.run_cell(V6.CARD_V6, B["lo"], B["hi"])
                            ).sort_values(["asset", "entry_ms"]
                                          ).reset_index(drop=True)
    g = len(got) == len(want)
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] {len(got)} == {len(want)} campaigns")
    if g:
        cols = [c for c in ("entry_ms", "exit_ms", "entry_px", "exit_px",
                            "stop_px", "r_dist", "net_r", "gross_r", "fee_r",
                            "funding_r", "mfe_r", "n_advances")
                if c in got.columns and c in want.columns]
        worst = max(float(np.nanmax(np.abs(
            pd.to_numeric(got[c], errors="coerce").astype(float)
            - pd.to_numeric(want[c], errors="coerce").astype(float))))
            for c in cols)
        g2 = worst == 0.0
        ok &= g2
        lines.append(f"[{'OK ' if g2 else 'BAD'}] {len(cols)} columns "
                     f"trade-for-trade: WORST ABS DIFF = {worst:.3e} "
                     f"(bar EXACTLY 0.000e+00, as commissioned)")
        g3 = got["exit_reason"].tolist() == want["exit_reason"].tolist()
        ok &= g3
        lines.append(f"[{'OK ' if g3 else 'BAD'}] and every exit_reason matches")
    lines.append("      FAILS IF: anything moves at all. The control turns "
                 "every v8 knob off, so the arithmetic is the parent's and the "
                 "answer must be the parent's.")
    return rec("F-CTRL", ok, lines)


def f_jrn():
    """FAILS IF: the two-position journal loses or mis-states a leg.

    THE TC7-a CLASS IS RETIRED BY SCHEMA, and this proves the schema rather
    than the four repairs: every leg has a row, the rollup counts them, the
    sized excursions on the legs reconcile to the rollup's, and the flags read
    ALL legs.  Three chains are hand-walked from raw bars."""
    lines, ok = [], True
    B = books()
    legs, roll = tbl("chain_legs"), tbl("chain_rollup")
    want_legs = sum(len(t.chain["legs"]) for t in B["chain"])
    g = len(legs) == want_legs and len(roll) == len(B["chain"])
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] CARDINALITY: {len(legs)} leg rows "
                 f"== {want_legs} legs, and {len(roll)} rollups == "
                 f"{len(B['chain'])} campaigns")
    # every rollup's leg count matches the rows filed for it
    m = legs.groupby(["asset", "entry_ms"]).size().rename("k").reset_index()
    j = roll.merge(m, on=["asset", "entry_ms"])
    bad = int((j["n_legs"] != j["k"]).sum())
    ok &= bad == 0
    lines.append(f"[{'OK ' if not bad else 'BAD'}] and every rollup's n_legs "
                 f"equals the leg rows filed for it: {bad} disagree")
    # the flags read ALL legs
    # THE FLAGS-READ-ALL-LEGS LEG WAS DEAD CODE — `hb` was computed and never
    # asserted on. It is now a join, and it is asserted.
    anyleg = (legs.groupby(["asset", "entry_ms"])["leg_harvested"].any()
              .rename("any_leg").reset_index())
    jj = roll.merge(anyleg, on=["asset", "entry_ms"], how="left")
    hb = int((jj["harvested_any_leg"].astype(bool)
              != jj["any_leg"].fillna(False).astype(bool)).sum())
    ok &= hb == 0
    lines.append(f"[{'OK ' if not hb else 'BAD'}] `harvested_any_leg` equals "
                 f"the OR over that chain's filed leg rows on all {len(jj)} "
                 f"rollups: {hb} disagree")
    multi = int((roll["n_harvests"] > 1).sum())
    lines.append(f"[OK ] {multi} chains harvest on MORE THAN ONE leg — under "
                 f"TIER-C7's single-campaign schema they filed harvested from "
                 f"leg 1 alone and 14 read False while having harvested")
    for t in [x for x in B["chain"] if x.n_reentries][:3]:
        f = T8.frame(t.symbol)["f"]
        d = t.direction
        hand_mfe = max(sz * (lg["mfe"] - lg["entry_px"]) * d / t.r_dist
                       for sz, lg in zip(t.leg_sizes, t.chain["legs"]))
        g2 = abs(hand_mfe - t.mfe_r) <= 1e-12
        ok &= g2
        lines.append(f"[{'OK ' if g2 else 'BAD'}] {t.symbol} "
                     f"{T8.iso(t.entry_ms)} · legs {len(t.chain['legs'])} "
                     f"sizes {tuple(round(s,4) for s in t.leg_sizes)} · "
                     f"size-weighted MFE {hand_mfe:+.6f} == filed {t.mfe_r:+.6f}")
    lines.append("      FAILS IF: a leg has no row, a rollup miscounts, or an "
                 "excursion is computed without its leg's size — which is the "
                 "TC7-a defect that published 57.31 R of reach no position had.")
    return rec("F-C7C-JRN", ok, lines)


def f_tide():
    """FAILS IF: the re-entry gate does not implement BOTH of the card's tide
    clauses [TC7-i].

    THE LEG WITH CONTENT IS A CASE THAT FAILS THE OLD GATE.  Asserting the new
    gate against itself proves nothing; the check is that there EXIST bars where
    the ribbons agree (`e89 vs e316`) while price does NOT (`close vs e316`), and
    that the gate refuses them.  If no such bar exists the clause is inert and
    the leg says so instead of passing."""
    lines, ok = [], True
    B = books()
    split = 0
    both = 0
    for sym in RC.UNIVERSE:
        f = T8.frame(sym)["f"]
        for d in (1, -1):
            e = (np.asarray(f.e89, float) - np.asarray(f.e316, float)) * d
            c = (np.asarray(f.c, float) - np.asarray(f.e316, float)) * d
            ok_old = e > 0
            ok_new = (e > 0) & (c > 0)
            split += int((ok_old & ~ok_new).sum())
            both += int(ok_new.sum())
    g = split > 0
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] THE CLAUSE BITES: {split:,} bars "
                 f"pass the ribbon clause and FAIL the price clause — bars the "
                 f"old gate admitted and the corrected one refuses "
                 f"({both:,} pass both)")
    lines.append("      FAILS IF: zero. Then the second clause is inert, the "
                 "old gate and the new one are the same rule, and TC7-i was a "
                 "documentation defect rather than a behavioural one.")
    # and the gate must actually use both
    f0 = T8.frame("BTCUSDT")["f"]
    hits = [j for j in range(400, len(f0.c))
            if ((float(f0.e89[j]) - float(f0.e316[j])) > 0
                and (float(f0.c[j]) - float(f0.e316[j])) <= 0)]
    if hits:
        j = hits[0]
        g2 = not T8.tide_ok(f0, j, 1)
        ok &= g2
        lines.append(f"[{'OK ' if g2 else 'BAD'}] and `tide_ok` REFUSES bar "
                     f"{T8.iso(int(f0.open_ms[j]))} on BTCUSDT long, where the "
                     f"ribbons agree and price does not")
    return rec("F-C7C-TIDE", ok, lines)


def f_match():
    """FAILS IF: any anchor advanced on a bar with no confirming (2,2) pivot.

    THE CLAIM THIS LEG MAKES IS NOT THE ONE THE COMMISSION FIRST WROTE, AND
    THAT IS DELIBERATE.  "Identical advance-opportunity counts per campaign
    across all cells" is FALSE and unfixable: a different anchor gives a
    different stop, a different exit, and therefore a different number of bars
    in which to have an opportunity. Measured: the M-edge cell has 847
    opportunities against the pivot cell's 293 — because its campaigns live
    41.9 bars on average against 21.2, not because its clock runs faster.

    THE DESIGN'S REAL CLAIM IS THE TIMING ONE AND IT IS EXACTLY CHECKABLE:
    a (2,2) confirmation is the ONLY moment any anchor may advance. Every
    advance in every cell is verified to sit on a confirming-pivot bar, against
    the fractal set rebuilt independently. The opportunity counts are REPORTED,
    with the lifetime that explains them, rather than asserted equal.
    """
    lines, ok = [], True
    B = books()
    lo, hi = B["lo"], B["hi"]
    # THE FRACTAL SET IS REBUILT FROM RAW BARS, AND THE FIRST DRAFT DID NOT.
    # It called `T8.fractals(sym, 2, 2)` — which returns the IDENTICAL MEMOISED
    # OBJECT `_ride_leg` handed to `matched_step`, because `card.trail_l/r` ARE
    # (2,2). `a is b` was True. The docstring claimed "rebuilt independently"
    # and the build document repeated it; both were false.
    #
    # A reviewer shifted every confirmation key by +3 bars in the SHARED
    # builder and this leg reported "all 2,087 advances ... 0 do not -> PASS"
    # while 1,875 of them (89.8%) sat on a bar with no (2,2) pivot. Five legs
    # stayed green, F-CTRL included, because v6 and v8 read the same poisoned
    # cache. The leg could see a broken ANCHOR (a reviewer deleted the pivot
    # gate and it failed correctly, 7,655 of 9,321) but not a broken CLOCK.
    #
    # A strict (2,2) fractal low at bar i is l[i] < l[i±1] and l[i] < l[i±2],
    # confirmed at i+2. That is nine lines of numpy and it shares nothing with
    # the estate's builder.
    def raw_conf(sym: str, low: bool) -> set:
        f = T8.frame(sym)["f"]
        v = np.asarray(f.l if low else f.h, float)
        n = len(v)
        out = set()
        for i in range(2, n - 2):
            a1, b1, c1 = v[i - 2], v[i - 1], v[i]
            d1, e1 = v[i + 1], v[i + 2]
            if low:
                if c1 < a1 and c1 < b1 and c1 < d1 and c1 < e1:
                    out.add(i + 2)
            else:
                if c1 > a1 and c1 > b1 and c1 > d1 and c1 > e1:
                    out.add(i + 2)
        return out

    RAW: dict = {}
    tot = badbar = 0
    for kind in ("pivot", "e26", "e89", "m_edge", "max_pivot_e89"):
        bk = T8.run_cell(T8.Card(name=kind, anchor_kind=kind,
                                 anchor_offset=0.50), lo, hi)
        for t in bk:
            key = (t.symbol, t.direction == 1)
            if key not in RAW:
                RAW[key] = raw_conf(t.symbol, t.direction == 1)
            src = RAW[key]
            for a in t.advances:
                tot += 1
                if int(a.conf_i) not in src:
                    badbar += 1
    g = badbar == 0 and tot > 0
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] TIMING IS MATCHED: all {tot:,} "
                 f"advances across 5 anchor cells sit on a bar where a (2,2) "
                 f"fractal confirmed IN A SET REBUILT FROM RAW BARS by a scan "
                 f"that shares no code with the estate's builder — {badbar} "
                 f"do not")
    lines.append("      FAILS IF: one does not. That is the confound this "
                 "phase exists to remove: TIER-C7's bake-off let a smooth "
                 "anchor advance off the pivot clock and then compared the "
                 "results.")
    grid = tbl("anchor_grid")
    lines.append("      OPPORTUNITY COUNTS ARE REPORTED, NOT ASSERTED EQUAL:")
    for _, r_ in grid[grid["offset_atr"] == 0.50].iterrows():
        lines.append(f"        {r_['cell']:26} opportunities "
                     f"{int(r_['advance_opportunities']):5,}  advances "
                     f"{int(r_['advances_taken']):5,}  n {int(r_['n'])}")
    lines.append("      they differ because CAMPAIGN LIFETIMES differ — a "
                 "looser anchor keeps campaigns alive longer and so meets more "
                 "pivots. That is a property of the anchor, not of the clock, "
                 "and it is the honest reading of this grid.")
    return rec("F-C8-MATCH", ok, lines)


def f_val():
    """FAILS IF: an advance's VALUE is not the anchor's level at the confirming
    bar, offset and railed.

    Three advances hand-verified: the level re-read from an independently
    rebuilt series, the offset applied, the rail imposed, and the published
    `new_stop` reproduced."""
    lines, ok = [], True
    B = books()
    from engine import indicators as ind
    n = 0
    for t in B["anchor"]:
        if n >= 3 or not t.advances:
            continue
        f = T8.frame(t.symbol)["f"]
        c = f.c
        idx = np.arange(len(c))
        m_lo, m_hi = RC.ribbon_band(c, "M")
        warm = idx >= max(RC.RIBBONS["M"])
        m_lo = np.where(warm, m_lo, np.nan)
        m_hi = np.where(warm, m_hi, np.nan)
        for a in t.advances[:1]:
            j, d = int(a.conf_i), t.direction
            lvl = float(m_lo[j] if d == 1 else m_hi[j])
            atr = float(f.atr[j])
            cand = lvl - d * 0.50 * atr
            rail = float(f.c[j]) - d * RC.MIN_STOP_ATR * atr
            adm = min(cand, rail) if d == 1 else max(cand, rail)
            g = abs(adm - a.new_stop) <= 1e-9 and abs(lvl - a.pivot_val) <= 1e-9
            ok &= g
            n += 1
            lines.append(f"[{'OK ' if g else 'BAD'}] {t.symbol} "
                         f"{T8.iso(int(f.open_ms[j]))} · M-edge {lvl:.6f} "
                         f"(filed {a.pivot_val:.6f}) − 0.50 ATR → cand "
                         f"{cand:.6f}, rail {rail:.6f} → stop {adm:.6f} "
                         f"(filed {a.new_stop:.6f})")
    lines.append("      FAILS IF: the value is not the anchor's own level at "
                 "that bar, or the rail was not imposed. The series is rebuilt "
                 "here with its own warm-up floor, not fetched from the "
                 "program's cache.")
    return rec("F-C8-VAL", ok, lines)


def f_loao():
    """FAILS IF: the LOAO leg cannot fail [TC7-e].

    TIER-C7's LOAO fixture asserted the column was a STRING. This one feeds
    `loao` a SYNTHETIC book engineered to clear on exactly two panels and
    demands the 3/5 line REFUSE it — a falsification, run every time."""
    lines, ok = [], True
    B = books()
    base = B["control"]
    rng = np.random.default_rng(20260818)

    class Fake:
        __slots__ = ("symbol", "lane", "entry_ms", "net_r")

        def __init__(self, s, l, e, n):
            self.symbol, self.lane, self.entry_ms, self.net_r = s, l, e, n

    # two assets get a large positive delta, three get noise around zero
    lift = {"BTCUSDT": 3.0, "ETHUSDT": 3.0}
    fake = [Fake(t.symbol, t.lane, t.entry_ms,
                 t.net_r + lift.get(t.symbol, 0.0)
                 + float(rng.normal(0, 0.01)))
            for t in base]
    r = T7.loao(fake, base, "SYNTHETIC", two_sample=False)
    n_ab = r["loao_excluding_above"]
    # NO ESCAPE DISJUNCT. The first draft was
    #     `not r["loao_clears_3_of_5"] or n_ab < 3`
    # and the second half could satisfy it without the 3/5 line ever being
    # consulted — a falsification test with a way out is not one. The leg now
    # demands BOTH: the line refuses, AND it refuses for the stated reason.
    g = (not r["loao_clears_3_of_5"]) and n_ab < 3
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] SYNTHETIC BOOK lifted on 2 of 5 "
                 f"assets → loao {r['loao_line']}, clears_3_of_5="
                 f"{r['loao_clears_3_of_5']} — the 3/5 line must REFUSE it")
    lines.append("      FAILS IF: it clears. A LOAO leg that cannot fail is a "
                 "column check wearing a robustness claim [TC7-e].")
    # and a book lifted on ALL five must clear, or the leg is vacuous the other way
    fake2 = [Fake(t.symbol, t.lane, t.entry_ms, t.net_r + 3.0) for t in base]
    r2 = T7.loao(fake2, base, "SYNTHETIC-ALL", two_sample=False)
    g2 = bool(r2["loao_clears_3_of_5"])
    ok &= g2
    lines.append(f"[{'OK ' if g2 else 'BAD'}] and a book lifted on ALL FIVE "
                 f"clears: {r2['loao_line']} — so the leg is not simply "
                 f"refusing everything")
    return rec("F-LOAO-FALSIFIABLE", ok, lines)


def f_keys():
    """FAILS IF: a filed table has a duplicate on its key, or a filed parquet
    has no declared key, or a table lacks its as-of warranty [TC6V-a]."""
    lines, ok = [], True
    man = json.loads((T8.OUT / "build_manifest.json").read_text())
    keys = {k: list(v) for k, v in man["keys"].items()}
    filed = sorted(p.stem for p in T8.OUT.glob("*.parquet"))
    miss = sorted(set(filed) - set(keys))
    ok &= not miss
    lines.append(f"[{'OK ' if not miss else 'BAD'}] TOTALITY: {len(keys)} keys "
                 f"cover all {len(filed)} filed parquets — unkeyed {miss}")
    nostamp = []
    for n, k in sorted(keys.items()):
        d = tbl(n)
        dup = int(d.duplicated(subset=k).sum()) if len(d) else 0
        ok &= dup == 0
        if "as_of_last_closed_4h" not in d.columns:
            nostamp.append(n)
        lines.append(f"[{'OK ' if not dup else 'BAD'}] {n:22} key={k} "
                     f"rows={len(d):,} dup={dup}")
    ok &= not nostamp
    lines.append(f"[{'OK ' if not nostamp else 'BAD'}] THE WARRANTY [TC6V-a]: "
                 f"every filed table carries its as-of corridor: {nostamp or 'all stamped'}")
    lines.append("      FAILS IF: a table ships without the corridor it is "
                 "true of. A number with no shelf life reads as a number with "
                 "no expiry.")
    return rec("F-KEY", ok, lines)


def f_closure():
    """FAILS IF: a decision module imports analytics or names a tape column."""
    lines, ok = [], True
    mods = ["scripts/tierc7_rules.py", "scripts/tierc6_rules.py",
            "scripts/tierc5_rules.py", "scripts/tierc4_rules.py",
            "scripts/tierc3_rules.py", "scripts/tierc2_rules.py"]
    for m in mods:
        src = F4.code_only((ROOT / m).read_text())
        hits = [w for w in ("import analytics", "from analytics",
                            "analytics.") if w in src]
        ok &= not hits
        lines.append(f"[{'OK ' if not hits else 'BAD'}] {m}: {hits}")
    lines.append("      FAILS IF: a decision module gains an analytics import.")
    return rec("F-CLOSURE", ok, lines)


def f_det():
    """FAILS IF: a second run writes a different byte."""
    lines, ok = [], True
    r = subprocess.run([str(Path.home() / "venvs/naiad/bin/python"),
                        "scripts/tierc8.py", "--rerun"], cwd=ROOT,
                       capture_output=True, text=True)
    if r.returncode != 0:
        return rec("F-DET", False, [f"[BAD] re-run failed: {r.stderr[-300:]}"])
    a = json.loads((T8.OUT / "build_manifest.json").read_text())
    b = json.loads((T8.OUT_RERUN / "build_manifest.json").read_text())
    moved = sorted(k for k in set(a["sha"]) & set(b["sha"])
                   if a["sha"][k] != b["sha"][k])
    ok &= not moved and set(a["sha"]) == set(b["sha"])
    lines.append(f"[{'OK ' if ok else 'BAD'}] {len(a['sha'])} tables, "
                 f"{len(moved)} build-sha moved {moved}")

    def h(p):
        return hashlib.sha256(p.read_bytes()).hexdigest()

    fm = [k for k in sorted(set(a["sha"]) & set(b["sha"]))
          if (T8.OUT / f"{k}.parquet").exists()
          and (T8.OUT_RERUN / f"{k}.parquet").exists()
          and h(T8.OUT / f"{k}.parquet") != h(T8.OUT_RERUN / f"{k}.parquet")]
    ok &= not fm
    lines.append(f"[{'OK ' if not fm else 'BAD'}] and the PARQUET FILES "
                 f"re-hash equal on disk: {len(fm)} differ {fm[:4]}")
    return rec("F-DET", ok, lines)


def f_worktree():
    """THE READ-ONLY WORKTREE ATTESTATION [REVIEW LAW, enacted 2026-08-17].

    Not a pass/fail on the code — a printed statement of the law and of how
    this build's review was run, so the attestation travels with the fixtures
    rather than living only in a commission nobody re-reads."""
    lines = [
        "[OK ] REVIEW LAW: all review and verifier agents run against a "
        "READ-ONLY worktree, enacted by the operator 2026-08-17 after a review "
        "agent left a sabotage patch (`return pd.DataFrame()`) in "
        "`tierc7_lab_regime.regime_table` during the TIER-C7 review.",
        "      The patch was caught by F-KEY's totality leg — a stale parquet "
        "with no declared key — removed, and the tree re-verified. But a review "
        "that edits what it reviews can invalidate its own result, and the law "
        "exists so the next one cannot.",
        "      THIS BUILD'S REVIEW RAN WITH `isolation: worktree`: every "
        "reviewer saw its own checkout, and no reviewer could write to the "
        "tree these fixtures run against.",
    ]
    return rec("F-WORKTREE-ATTEST", True, lines)



def f_weave_all():
    """FAILS IF: the weave predicate is not D-R3's, checked on EVERY firing
    rather than on three [TC7-d] — and if the register's reading cannot be told
    from the alternative the register says is NOT taken.

    TIER-C7's F-C7-WEV sampled 3 of 42 events, and both the strict-containment
    reading and a different k-window passed those three. This leg evaluates the
    predicate over the WHOLE panel, and separately evaluates the alternative,
    and demands they DISAGREE somewhere — otherwise the register's careful
    naming of a reading-not-taken describes a distinction the code cannot make.
    """
    lines, ok = [], True
    from engine import indicators as ind
    k = RC.WEAVE_K
    agree = disagree = fires = 0
    for sym in RC.UNIVERSE:
        c = T8.frame(sym)["f"].c
        n = len(c)
        idx = np.arange(n)
        m_lo, m_hi = RC.ribbon_band(c, "M")
        f_lo, f_hi = RC.ribbon_band(c, "FAST")
        for arr, fam in ((m_lo, "M"), (m_hi, "M"), (f_lo, "FAST"),
                         (f_hi, "FAST")):
            arr[idx < max(RC.RIBBONS[fam])] = np.nan
        med = np.where(idx >= RC.RIBBONS["M"][1],
                       ind.ema(c, RC.RIBBONS["M"][1]), np.nan)
        width = m_hi - m_lo
        wv = T7.weave_of(sym)
        for d in (1, -1):
            for j in range(k + 1, n):
                prog = RC.weave_fires(wv, j, d, k)
                vals = (width[j], width[j - k], med[j], med[j - 1],
                        f_lo[j], f_hi[j], m_lo[j], m_hi[j])
                if not all(np.isfinite(v) for v in vals):
                    hand = False
                    alt = False
                else:
                    c1 = (width[j] < width[j - k]
                          and (med[j] - med[j - 1]) * d <= 0.0)
                    # THE REGISTER'S READING: inside-OR-BEYOND, an inequality
                    hand = bool(c1 and ((f_lo[j] <= m_hi[j]) if d == 1
                                        else (f_hi[j] >= m_lo[j])))
                    # THE ALTERNATIVE NOT TAKEN: strict CONTAINMENT
                    alt = bool(c1 and (m_lo[j] <= f_lo[j] <= m_hi[j] if d == 1
                                       else m_lo[j] <= f_hi[j] <= m_hi[j]))
                if prog != hand:
                    ok = False
                fires += int(prog)
                agree += int(hand == alt)
                disagree += int(hand != alt)
    lines.append(f"[{'OK ' if ok else 'BAD'}] the program's weave predicate "
                 f"equals D-R3 re-derived from raw closes on EVERY bar of the "
                 f"panel — {fires:,} firings across 5 assets x 2 directions "
                 f"[TC7-d: TIER-C7 checked 3 of 42]")
    g = disagree > 0
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] AND THE READING IS "
                 f"DISTINGUISHABLE: the register's inside-OR-BEYOND reading "
                 f"and the strict-CONTAINMENT alternative disagree on "
                 f"{disagree:,} bars (agree on {agree:,})")
    lines.append("      FAILS IF: they never disagree. Then the register's "
                 "careful naming of a reading-not-taken describes a "
                 "distinction the code cannot make, and the alternative was "
                 "never really refused.")
    return rec("F-WEAVE-ALL", ok, lines)


def main() -> int:
    print("=" * 78)
    print("TIER-C7-C + TIER-C8 FIXTURE TRANSCRIPT")
    print("=" * 78)
    f_ctrl(); f_jrn(); f_tide(); f_match(); f_val()
    f_weave_all(); f_loao(); f_keys(); f_closure(); f_worktree(); f_det()
    print("\n".join(T))
    n = sum(RESULTS.values())
    print()
    print("=" * 78)
    print(f"FIXTURE SUMMARY  {n}/{len(RESULTS)} PASS  {json.dumps(RESULTS)}")
    print(f"  I9: ANALYTICS_VERSION {AN.ANALYTICS_VERSION} · analytics_sha "
          f"{AN.analytics_sha()}")
    print("=" * 78)
    if n != len(RESULTS):
        print("*** HALT: fixture mismatch. Nothing downstream is trustworthy. ***")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
