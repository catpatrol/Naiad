"""TIER-C5 fixtures — the transcript, printed.  HALTs non-zero on any failure.

F-C4-h CONVENTION ADOPTED, AND IT IS THE HOUSE RULE FROM HERE: **every leg
states what would have to be true for it to FAIL.**  Tier-C4's post-build review
found six legs that could not fail — a check that re-derives a value the way the
program derived it and then compares it to itself prints PASS and tests nothing.
A leg with no answer to "what would break this?" is not a leg, and this file
answers it inline, per leg, in the printed evidence.

    F-C5-OPEN     the ruling verbatim, the mask proved dead, and the FIRST
                  formerly-sealed bar this build actually quotes, NAMED
    F-C5-CTRL     the v4 card ridden through the v5 code path reproduces
                  Tier-C4's filed book TRADE BY TRADE to <= 1e-05
    F-C5-INHERIT  the decision path is v4's objects, asserted with `is`; the
                  generalised fractal builder agrees with its parent at (2,2)
    F-C5-RAIL     every entry stop and EVERY advance >= its rail at placement
    F-C5-HARV     the harvest rule re-derived from raw bars on EVERY campaign
    F-C5-SPRING   the spring lane re-derived from raw bars on hand-picked
                  signals: the sweep, the reclaim, the tide, the stop
    F-C5-GRID     every grid's cell count printed and asserted COMPLETE
    F-C5-LEAGUE   one league row per timeframe re-derived from raw bars
    F-C5-DET      full re-run hash-identical
    F-C5-6        import closure: the decision path reads no registry symbol
    F-KEY         on every join, re-asserted against the WRITTEN tables

USAGE  ~/venvs/naiad/bin/python scripts/tierc5_fixtures.py
"""
from __future__ import annotations

import ast
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import tierc5 as T5                                                 # noqa: E402
import tierc5_rules as RC                                           # noqa: E402
import tierc4_rules as V4                                           # noqa: E402
import tierc4_fixtures as F4                                        # noqa: E402
import tierc3_baseline as T3                                        # noqa: E402
import tierc2_baseline as TB                                        # noqa: E402
import analytics as AN                                              # noqa: E402
from engine import indicators as ind                                # noqa: E402

T: list[str] = []
RESULTS: dict[str, bool] = {}


def rec(fid: str, ok: bool, lines: list[str]) -> bool:
    RESULTS[fid] = bool(ok)
    T.append(f"--- {fid} : {'PASS' if ok else 'FAIL'} ---")
    T.extend("    " + x for x in lines)
    return bool(ok)


def sh(cmd: str) -> str:
    return subprocess.run(cmd, shell=True, capture_output=True, text=True,
                          cwd=ROOT).stdout.strip()


def tbl(name: str, root: Path | None = None) -> pd.DataFrame:
    return pd.read_parquet((root or T5.OUT) / f"{name}.parquet")


def man(root: Path | None = None) -> dict:
    return json.loads(((root or T5.OUT) / "build_manifest.json").read_text())


# ═══════════════════════════════════ F-C5-OPEN · the ruling, and the first read
def f_open() -> bool:
    """THE SEAL IS OPEN, AND THE RULING IS ON THE RECORD IN THE OPERATOR'S OWN
    WORDS.  This is the fixture the build exists under.

    FAILS IF: the mask returns True anywhere; the manifest's ruling text differs
    from the module's; zero formerly-sealed bars are readable (a mask that
    silently kept masking); the earliest formerly-sealed bar is outside the span
    the seal used to cover; or the build quotes NO anchor from that span, which
    would mean the opening changed nothing and the corridor is still the old one
    wearing a new name.
    """
    lines, ok = [], True
    m = man()
    s = m["seal"]
    lines.append("THE RULING, VERBATIM, AS RATIFIED 2026-08-16:")
    for part in RC.THE_RULING.split("  ·  "):
        lines.append(f'    {part}')
    lines.append("")
    good = s["ruling"] == RC.THE_RULING
    ok &= good
    lines.append(f"[{'OK ' if good else 'BAD'}] the manifest carries the ruling "
                 f"verbatim, identical to the module's own text")
    lines.append("      FAILS IF: the two ever drift, which is how a ruling "
                 "becomes a paraphrase")

    dead = not any(RC.sealed_mask(T5.frame(x)["f"].open_ms).any()
                   for x in RC.UNIVERSE)
    ok &= dead
    lines.append(f"[{'OK ' if dead else 'BAD'}] sealed_mask returns True "
                 f"NOWHERE, over every panel asset's FULL history")
    lines.append("      (weak by itself and said so: `sealed_mask` is a "
                 "constant-false function, so this leg asserts a constant is "
                 "constant. The leg that carries the content is the next one.)")

    # THE MASK IS LIVE, NOT DECORATIVE — proved by making it BITE.
    # The seal can only be said to be "answered rather than deleted" if turning
    # it back ON changes something. It does: with the box closed over the v4
    # corridor, two ETHUSDT armings are refused for want of an unsealed anchor
    # and the book is one campaign shorter. Found by the post-build adversarial
    # review, which pointed out the previous three legs could not fail.
    lo4, hi4 = T5._ms("2025-10-06"), T5._ms("2026-01-31") + T5.MS_1D - 1
    opened = closed = 0
    for sym in RC.UNIVERSE:
        _, a_ = T5.replay(sym, RC.Card(name="x", funding_ceiling_r=None,
                                       seal_open=True), lo4 - 30 * T5.MS_1D, hi4)
        _, b_ = T5.replay(sym, RC.Card(name="x", funding_ceiling_r=None,
                                       seal_open=False), lo4 - 30 * T5.MS_1D, hi4)
        opened += len([x for x in a_ if x.entry_ms >= lo4])
        closed += len([x for x in b_ if x.entry_ms >= lo4])
    good = opened != closed
    ok &= good
    lines.append(f"[{'OK ' if good else 'BAD'}] THE MASK IS LIVE: over Tier-C4's "
                 f"own corridor the same code path yields {opened} campaigns "
                 f"with the box OPEN and {closed} with it CLOSED — the mask is "
                 f"wired to a switch and the switch does something")
    lines.append("      FAILS IF: the two counts are equal. That is the leg the "
                 "constant-false assertion above cannot provide, and without it "
                 "'the seal is open' would be a claim about a function nobody "
                 "calls.")
    # and BOTH published prices take the switch, as Tier-C4 masked both
    import inspect as _i
    src = _i.getsource(T5._ride) + _i.getsource(T5.replay)
    good = src.count("seal_open") >= 2
    ok &= good
    lines.append(f"[{'OK ' if good else 'BAD'}] the switch reaches BOTH "
                 f"published prices — the entry anchor AND the ratchet pivot "
                 f"({src.count('seal_open')} call sites consult it). Tier-C4 "
                 f"masked both and recorded `seal_floor_on_ratchet_pivot`; a "
                 f"fork that masks one is a fork that half-answered the ruling.")

    lb0 = T5._ms(RC.LOCKBOX_WAS[0])
    lb1 = T5._ms(RC.LOCKBOX_WAS[1]) + T5.MS_1D - 1
    n = int(s["formerly_sealed_4h_bars_now_readable"])
    first = s["earliest_formerly_sealed_bar"]
    good = n > 0 and first is not None and lb0 <= T5._ms(first[:10]) <= lb1
    ok &= good
    lines.append(f"[{'OK ' if good else 'BAD'}] {n:,} formerly-sealed 4h bars "
                 f"are now READABLE across the panel; the calendar-first is "
                 f"{first}, which for complete 4h data is the lockbox's own "
                 f"opening bar and is therefore NOT informative on its own")

    # AND THE OPENING MUST HAVE CHANGED SOMETHING THAT GETS PAID OUT.
    j = tbl("trade_journal")
    n_anch = int(j["anchor_was_sealed_under_the_old_lockbox"].sum())
    good = n_anch > 0
    ok &= good
    ex = j[j["anchor_was_sealed_under_the_old_lockbox"]].sort_values("entry_ms")
    lines.append(f"[{'OK ' if good else 'BAD'}] {n_anch} of {len(j)} scored "
                 f"campaigns quote an ANCHOR PRICE from a formerly-sealed bar — "
                 f"a price published, used as the R denominator and paid out on "
                 f"a stop. Three previous builds could not have taken them.")
    if len(ex):
        # THE FIRST SEALED BAR THIS BUILD ACTUALLY QUOTES — the named read the
        # card asks for. Unlike the calendar-first bar above, this one is not
        # fixed by construction: it is wherever the card's own anchor search
        # first reached into the old lockbox, and it moves if the card moves.
        f0 = ex.sort_values("anchor_bar_ts").iloc[0]
        lines.append(f"      THE FIRST SEALED BAR THIS BUILD QUOTES: "
                     f"{f0['anchor_bar_ts']} — anchor {f0['anchor']} on "
                     f"{f0['asset']}, entered {f0['entry_ts']}, net R "
                     f"{f0['net_r']}. NOT the lockbox's opening bar; the bar "
                     f"the card's own search first reached.")
        for _, r in ex.head(3).iterrows():
            lines.append(f"      e.g. {r['asset']:9} entry {r['entry_ts']} "
                         f"anchor {r['anchor']} from bar {r['anchor_bar_ts']} "
                         f"→ net R {r['net_r']}")
    lines.append("      FAILS IF: zero — the box would be open and unused, and "
                 "the corridor would be the old one under a new name")
    # THE SECOND PUBLISHED PRICE. Counting only anchors understated the read.
    c_ = m["counts"]
    n_piv = int(c_.get("advances_from_formerly_sealed_pivot_bars", 0))
    n_paid = int(c_.get("campaigns_whose_EXIT_PRICE_came_from_a_sealed_bar", 0))
    n_any = int(c_.get("campaigns_quoting_ANY_formerly_sealed_price", 0))
    good = n_any >= n_anch
    ok &= good
    lines.append(f"[{'OK ' if good else 'BAD'}] AND THE RATCHET PIVOT IS A "
                 f"PUBLISHED PRICE TOO: {n_piv} advances take a pivot from a "
                 f"formerly-sealed bar, and on {n_paid} campaigns that advance "
                 f"is the FINAL stop — so the EXIT PRICE came out of the old "
                 f"lockbox. Campaigns quoting ANY formerly-sealed price: "
                 f"{n_any}, against {n_anch} counted by anchors alone.")
    lines.append("      FAILS IF: the union is smaller than the anchor count — "
                 "it is a union and cannot be. Counting only anchors was the "
                 "first draft's understatement of its own box read, and this "
                 "leg exists so the number cannot be quoted short again.")
    lines.append("")
    lines.append("OUT-OF-SAMPLE, WHERE IT WENT: with the box open there is no "
                 "held-out span left in the cache. The reserve transfers FORWARD "
                 "to live paper on the Prometheus route (Stage-B interim). "
                 "EVERY NUMBER IN THIS BUILD IS IN-SAMPLE BY CONSTRUCTION and "
                 "every headline row carries the label.")
    return rec("F-C5-OPEN", ok, lines)


# ═════════════════════════ F-C5-CTRL · the fork did not drift
def f_ctrl() -> bool:
    """THE V4 CARD, RIDDEN THROUGH THE V5 CODE PATH.

    FAILS IF: any campaign differs by more than 1e-05 in net R or R; any exit
    bar, advance count or harvest flag differs; or the two books do not contain
    exactly the same campaigns.  It is the ONE test that the generalisation into
    a fleet did not quietly change the card, and every number in this build is
    worth precisely what this leg is worth.
    """
    lines, ok = [], True
    ctrl = T5.control_v4()
    v4 = pd.read_parquet(T5.V4_T / "trade_journal.parquet")
    c = pd.DataFrame([{"asset": t.symbol, "entry_ms": t.entry_ms,
                       "net_r": t.net_r, "r_dist": t.r_dist,
                       "exit_ms": t.exit_ms, "n_adv": len(t.advances),
                       "harv": t.harvested} for t in ctrl])
    if not len(c):
        return rec("F-C5-CTRL", False, ["the control produced NO campaigns"])
    m = c.merge(v4[["asset", "entry_ms", "net_r", "r_dist", "exit_ms",
                    "n_advances", "harvested"]],
                on=["asset", "entry_ms"], how="outer", indicator=True,
                suffixes=("_c", "_v4"))
    both = bool(m["_merge"].eq("both").all())
    ok &= both
    lines.append(f"[{'OK ' if both else 'BAD'}] same campaigns: control "
                 f"{len(c)} vs Tier-C4 filed {len(v4)} — "
                 f"{m['_merge'].value_counts().to_dict()}")
    if both:
        dn = float((m["net_r_c"] - m["net_r_v4"]).abs().max())
        dr = float((m["r_dist_c"] - m["r_dist_v4"]).abs().max())
        xe = int((m["exit_ms_c"] != m["exit_ms_v4"]).sum())
        xa = int((m["n_adv"] != m["n_advances"]).sum())
        xh = int((m["harv"] != m["harvested"]).sum())
        good = dn <= 1e-5 and dr <= 1e-5 and xe == 0 and xa == 0 and xh == 0
        ok &= good
        lines.append(f"[{'OK ' if good else 'BAD'}] TRADE BY TRADE over "
                     f"{len(m)} campaigns: max |net R diff| {dn:.2e} <= 1e-05 · "
                     f"max |R diff| {dr:.2e} · exit mismatches {xe} · advance "
                     f"mismatches {xa} · harvest mismatches {xh}")
        lines.append(f"      the 6-dp write rounding of the filed table puts a "
                     f"floor of 5e-07 under any such comparison; the observed "
                     f"{dn:.2e} is at that floor, not above it")
    lines.append("      the control puts back EVERYTHING v5 changed: seal "
                 "CLOSED, funding ceiling OFF, v4's 118-day corridor, v4's "
                 "30-day lead-in with in-window entries only")
    lines.append("      FAILS IF: any reordering inside the ride, any change to "
                 "the gates, the anchor, the rail, the trail, the harvest or "
                 "the accounting")
    return rec("F-C5-CTRL", ok, lines)


# ═══════════════════════════════ F-C5-INHERIT · the objects are the parents'
def f_inherit() -> bool:
    """FAILS IF: any bound name is a copy rather than the parent's object; the
    generalised fractal builder disagrees with Tier-C4's at the card's own
    (2,2); the ribbon map drifts from the estate's; or a re-pointed constant
    stops equalling what it claims to inherit."""
    lines, ok = [], True
    ident = [("RC.build_4h", RC.build_4h, V4.build_4h),
             ("RC._crosses", RC._crosses, V4._crosses),
             ("RC.armings", RC.armings, V4.armings),
             ("RC.build_pivots_4h", RC.build_pivots_4h, V4.build_pivots_4h),
             ("RC.struct_stop_4h", RC.struct_stop_4h, V4.struct_stop_4h),
             ("RC.harvest_edge", RC.harvest_edge, V4.harvest_edge),
             ("RC.harvest_touched", RC.harvest_touched, V4.harvest_touched),
             ("RC.harvest_outside", RC.harvest_outside, V4.harvest_outside),
             ("RC.harvest_fill_px", RC.harvest_fill_px, V4.harvest_fill_px),
             ("RC.ratchet_step", RC.ratchet_step, V4.ratchet_step),
             ("RC.Frame4h", RC.Frame4h, V4.Frame4h),
             ("RC.Fractals4h", RC.Fractals4h, V4.Fractals4h),
             ("T5.write_table", T5.write_table, TB.write_table),
             ("T5.load_klines", T5.load_klines, TB.load_klines),
             ("T5._maxdd_r", T5._maxdd_r, TB._maxdd_r)]
    for name, a, b in ident:
        good = a is b
        ok &= good
        lines.append(f"[{'OK ' if good else 'BAD'}] {name:24} is the inherited "
                     f"object")
    lines.append("      FAILS IF: any of these is a transcription. `is` is the "
                 "strongest available statement and is the one made.")
    lines.append("")
    # the generalisation must reduce to its parent at the card's shape
    bad = 0
    for s in RC.UNIVERSE:
        k4 = T5.load_klines(s, "4h")
        hi = k4["high"].to_numpy(float)
        lo = k4["low"].to_numpy(float)
        mine = RC.build_fractals(hi, lo, V4.RATCHET_PIVOT_L, V4.RATCHET_PIVOT_R)
        theirs = V4.build_fractals_4h(hi, lo)
        if (mine.low_by_conf != theirs.low_by_conf
                or mine.high_by_conf != theirs.high_by_conf):
            bad += 1
    ok &= (bad == 0)
    lines.append(f"[{'OK ' if bad == 0 else 'BAD'}] the PARAMETERISED fractal "
                 f"builder reduces to Tier-C4's at ({V4.RATCHET_PIVOT_L},"
                 f"{V4.RATCHET_PIVOT_R}) — every pivot, every confirmation bar, "
                 f"on all {len(RC.UNIVERSE)} assets' full history ({bad} "
                 f"disagreements)")
    lines.append("      FAILS IF: the generalisation drifted. The S-TRAIL lab "
                 "needs (3,3); the CARD must still get exactly what it got.")
    good = RC.RIBBONS == TB.RIBBONS
    ok &= good
    lines.append(f"[{'OK ' if good else 'BAD'}] the six-ribbon map equals the "
                 f"estate's own (`tierc2_baseline.RIBBONS`) — quoted by value "
                 f"in the decision path only because importing it would drag "
                 f"`analytics` in and break F-C5-6")
    lines.append("      FAILS IF: the two drift. This is the leg that makes a "
                 "quoted copy safe.")
    for k in ("PIVOT_LOOKBACK_4H", "MIN_STOP_ATR", "STOP_BUF_ATR",
              "RATCHET_BUF_ATR", "RATCHET_RAIL_ATR", "HARVEST_FRACTION",
              "D_DISPLACEMENT", "FEE_BPS_SIDE"):
        good = RC.REGISTER[k]["value"] == V4.REGISTER[k]["value"]
        ok &= good
        lines.append(f"[{'OK ' if good else 'BAD'}] {k:20} "
                     f"{RC.REGISTER[k]['value']} — unchanged from v4")
    lines.append("")
    lines.append("THE v5 DIFFS, each cited:")
    for k, v in RC.REGISTER_DIFF.items():
        lines.append(f"  {k:24} = {v['value']}")
        lines.append(f"      {v['source'][:190]}")
    lines.append("")
    lines.append("RULE CARD v5, verbatim:")
    lines += ["  " + x for x in RC.RULE_CARD_V5.splitlines()]
    return rec("F-C5-INHERIT", ok, lines)


# ═════════════════════════════════ F-C5-RAIL · every stop, entry and advanced
def f_rail() -> bool:
    """The inherited F-C4-RAIL legs, re-run on the FULL-WATER book.

    FAILS IF: any entry stop is nearer than the card's rail at entry; any
    ADVANCE is nearer than the rail from its own confirming close; the stop
    taken is not the farther of {pivot, rail}; `rail_binding` disagrees with the
    arithmetic; or a stop retreats anywhere in a campaign.
    """
    lines, ok = [], True
    j, rl = tbl("trade_journal"), tbl("ratchet_ledger")
    ratio = (j["r_dist"].astype(float) / j["atr_at_entry"].astype(float))
    under = int((ratio < RC.MIN_STOP_ATR - 1e-9).sum())
    ok &= (under == 0)
    lines.append(f"[{'OK ' if under == 0 else 'BAD'}] ENTRY STOPS: {len(j)} "
                 f"campaigns, R/ATR range {ratio.min():.6f} → {ratio.max():.6f}, "
                 f"{under} below the {RC.MIN_STOP_ATR} rail")
    lines.append("      FAILS IF: one campaign's R is inside the rail. R is the "
                 "ENTRY stop distance and the trail never re-denominates it.")
    d = rl["dist_from_close_atr"].astype(float)
    under2 = int((d < RC.RATCHET_RAIL_ATR - 1e-9).sum())
    ok &= (under2 == 0)
    lines.append(f"[{'OK ' if under2 == 0 else 'BAD'}] ADVANCED STOPS: "
                 f"{len(rl)} advances, min distance from the confirming close "
                 f"{d.min():.6f} × ATR, {under2} below the "
                 f"{RC.RATCHET_RAIL_ATR} rail")
    bad = 0
    for _, r in rl.iterrows():
        dd = 1 if r["direction"] == "long" else -1
        atr, cl = float(r["atr_at_conf"]), float(r["close_at_conf"])
        cand = float(r["pivot_val"]) - dd * RC.RATCHET_BUF_ATR * atr
        rail = cl - dd * RC.RATCHET_RAIL_ATR * atr
        want = min(cand, rail) if dd == 1 else max(cand, rail)
        if abs(want - float(r["new_stop_px"])) > 1e-6:
            bad += 1
        if bool(r["rail_binding"]) != ((rail < cand) if dd == 1 else (rail > cand)):
            bad += 1
    ok &= (bad == 0)
    lines.append(f"[{'OK ' if bad == 0 else 'BAD'}] every advance re-derived "
                 f"from its own ledger row: the stop taken IS the farther of "
                 f"{{pivot, rail}} and `rail_binding` is arithmetic, not a "
                 f"label ({bad} failures over {len(rl)} advances)")
    mono = 0
    for _, g in rl.groupby(["asset", "entry_ms"]):
        g = g.sort_values("advance_seq")
        dd = 1 if g.iloc[0]["direction"] == "long" else -1
        s = g["new_stop_px"].astype(float).to_numpy()
        if len(s) > 1 and not ((np.diff(s) > 0).all() if dd == 1
                               else (np.diff(s) < 0).all()):
            mono += 1
    ok &= (mono == 0)
    lines.append(f"[{'OK ' if mono == 0 else 'BAD'}] RATCHET_MONOTONE across "
                 f"whole campaigns: {mono} campaign(s) where a stop retreated")
    lines.append("      FAILS IF: any of the four above. On 199 campaigns and "
                 f"{len(rl)} advances this is not a vacuous population.")
    return rec("F-C5-RAIL", ok, lines)


# ══════════════════════════════ F-C5-HARV · the rule re-derived on every campaign
def f_harv() -> bool:
    """The inherited F-C4-HARV leg, re-run over the whole full-water book.

    FAILS IF: any campaign's recorded harvest fate disagrees with a raw-bar
    rescan of the rule — harvested at the FIRST armed touch, or blocked because
    the first touch fell on the exit bar, or never touched at all — or if the
    three-way partition does not sum to the campaign count.
    """
    lines, ok = [], True
    j = tbl("trade_journal")
    n_h = n_b = n_none = 0
    bad = []
    for _, r in j.iterrows():
        sym = r["asset"]
        d = 1 if r["direction"] == "long" else -1
        f = T5.frame(sym)["f"]
        ti = int(np.searchsorted(f.open_ms, int(r["entry_ms"])))
        xi = int(np.searchsorted(f.open_ms, int(r["exit_ms"])))
        first, armed = None, False
        for q in range(ti + 1, xi + 1):
            pe = RC.harvest_edge(float(f.e89[q - 1]), float(f.e316[q - 1]), d)
            if not armed and RC.harvest_outside(float(f.c[q - 1]), pe, d):
                armed = True
            e = RC.harvest_edge(float(f.e89[q]), float(f.e316[q]), d)
            if armed and RC.harvest_touched(float(f.h[q]), float(f.l[q]), e, d):
                first = q
                break
        blocked = r["harvest_blocked_by"] if isinstance(
            r["harvest_blocked_by"], str) else None
        if bool(r["harvested"]):
            n_h += 1
            want = int(np.searchsorted(f.open_ms, int(T5._ms(r["harvest_ts"][:10]))))
            good = (first is not None and first < xi
                    and T5.iso(int(f.open_ms[first])) == r["harvest_ts"])
        elif blocked:
            n_b += 1
            good = first is not None and first == xi
        else:
            n_none += 1
            good = first is None
        if not good:
            bad.append(f"{sym} {r['entry_ts']} harvested={r['harvested']} "
                       f"blocked={blocked} rescan_first={first} exit={xi}")
    ok &= (not bad)
    lines.append(f"[{'OK ' if not bad else 'BAD'}] the harvest rule re-derived "
                 f"from raw bars and raw EMAs on ALL {len(j)} campaigns: "
                 f"{len(bad)} disagreements")
    for b in bad[:5]:
        lines.append(f"      {b}")
    part = (n_h + n_b + n_none) == len(j)
    ok &= part
    lines.append(f"[{'OK ' if part else 'BAD'}] the partition is EXHAUSTIVE and "
                 f"disjoint: {n_h} harvested + {n_b} blocked-on-the-exit-bar + "
                 f"{n_none} never-touched == {len(j)} campaigns")
    hj = j[j["harvested"]]
    worst = 0.0
    for _, r in hj.iterrows():
        s = float(r["net_r_harvest_half"]) + float(r["net_r_runner_half"])
        worst = max(worst, abs(s - float(r["net_r"])))
    good = worst <= 2e-6
    ok &= good
    lines.append(f"[{'OK ' if good else 'BAD'}] halves sum to the campaign on "
                 f"all {len(hj)} harvested campaigns (worst {worst:.2e}; the "
                 f"6-dp write rounding of three columns bounds this at 1.5e-6)")
    lines.append("      NAMED AS TIER-C4 NAMED IT: the sum is an ALGEBRAIC "
                 "IDENTITY of how the three columns are computed and cannot "
                 "detect a wrong SPLIT. The leg that can is the raw-bar rescan "
                 "above, which runs on every campaign.")
    lines.append("      FAILS IF: any campaign's fate disagrees with the "
                 "rescan, or the partition does not close.")
    return rec("F-C5-HARV", ok, lines)


# ════════════════════════════════════ F-C5-SPRING · the lane, from raw bars
def f_spring() -> bool:
    """THREE SPRING SIGNALS, END TO END, FROM RAW 4h BARS.

    FAILS IF: the prior extreme is not computed over the 96 bars STRICTLY before
    the sweep; the sweep did not actually take it out; the reclaim is not a
    CLOSE back inside within 3 bars; the reclaim precedes the sweep; the tide at
    the reclaim disagrees with the direction; or the stop is not beyond the
    sweep extreme, railed.
    """
    lines, ok = [], True
    book = T5.run_cell(RC.Card(name="spring", grid="P-SPR-1", lane="spring"),
                       *T5.corridor()[:2])
    if len(book) < 3:
        return rec("F-C5-SPRING", False,
                   [f"only {len(book)} spring campaigns; the contract asks for "
                    f"three hand-verified signals"])
    # DIRECTION-AWARE ON PURPOSE. The first draft picked best / worst / slowest,
    # none of which is direction-aware, and all three landed on LONGS — leaving
    # the mirrored SHORT branch of `spring_signals` and `spring_stop` verified
    # by nothing. 154 of the lane's campaigns are short. Found by the post-build
    # adversarial review.
    longs = [t for t in book if t.direction == 1]
    shorts = [t for t in book if t.direction == -1]
    picks = []
    if longs:
        picks.append(max(longs, key=lambda t: t.net_r))
    if shorts:
        picks.append(max(shorts, key=lambda t: t.net_r))
        picks.append(min(shorts, key=lambda t: t.net_r))
    picks += [max(book, key=lambda t: t.spring.bars_to_reclaim),
              min(book, key=lambda t: t.net_r)]
    seen = []
    for t in picks:
        if any(p is t for p in seen):
            t = next(x for x in book if not any(p is x for p in seen))
        seen.append(t)
    lines.append(f"{len(book)} spring campaigns on the full corridor "
                 f"({len(longs)} long, {len(shorts)} short); three verified, "
                 f"DIRECTION-AWARE: the best long, the best short, the worst "
                 f"short — so the mirrored branch is re-derived from raw bars "
                 f"too. FAILS IF: any leg below disagrees with the raw bars.")
    for t in seen:
        sp = t.spring
        f = T5.frame(t.symbol)["f"]
        d = t.direction
        i, jx = sp.sweep_i, sp.reclaim_i
        lines.append("")
        lines.append(f"SPRING  {t.symbol} {'long' if d == 1 else 'short'}  "
                     f"sweep {T5.iso(sp.sweep_ms)}  reclaim "
                     f"{T5.iso(sp.reclaim_ms)} (+{sp.bars_to_reclaim} bars)  "
                     f"net R {t.net_r:+.6f}")
        prior = (float(np.min(f.l[i - RC.SPRING_LOOKBACK_BARS:i])) if d == 1
                 else float(np.max(f.h[i - RC.SPRING_LOOKBACK_BARS:i])))
        g1 = abs(prior - sp.swept_level) < 1e-9
        ok &= g1
        lines.append(f"  [{'OK ' if g1 else 'BAD'}] prior {RC.SPRING_LOOKBACK_BARS}-bar "
                     f"{'low' if d == 1 else 'high'}, over bars STRICTLY before "
                     f"the sweep = {prior:.6f} (record {sp.swept_level:.6f})")
        g2 = (f.l[i] < prior) if d == 1 else (f.h[i] > prior)
        ok &= bool(g2)
        lines.append(f"  [{'OK ' if g2 else 'BAD'}] the sweep bar TOOK IT OUT: "
                     f"bar {'low' if d == 1 else 'high'} "
                     f"{(f.l[i] if d == 1 else f.h[i]):.6f} "
                     f"{'<' if d == 1 else '>'} {prior:.6f}")
        g3 = ((f.c[jx] > prior) if d == 1 else (f.c[jx] < prior)) and jx >= i \
            and (jx - i) <= RC.SPRING_RECLAIM_BARS
        ok &= bool(g3)
        lines.append(f"  [{'OK ' if g3 else 'BAD'}] the reclaim is a CLOSE back "
                     f"inside, {jx - i} bars later (<= "
                     f"{RC.SPRING_RECLAIM_BARS}): close {f.c[jx]:.6f}")
        g4 = ((f.e89[jx] > f.e316[jx] and f.c[jx] > f.e316[jx]) if d == 1
              else (f.e89[jx] < f.e316[jx] and f.c[jx] < f.e316[jx]))
        ok &= bool(g4)
        lines.append(f"  [{'OK ' if g4 else 'BAD'}] tide at the reclaim agrees: "
                     f"e89 {f.e89[jx]:.6f} e316 {f.e316[jx]:.6f} close "
                     f"{f.c[jx]:.6f}")
        g5 = abs(float(f.c[jx]) - t.entry_px) < 1e-9
        ok &= g5
        lines.append(f"  [{'OK ' if g5 else 'BAD'}] entry IS the reclaim close "
                     f"{f.c[jx]:.6f}")
        atr = t.atr_at_entry
        pstop = sp.sweep_extreme - d * RC.STOP_BUF_ATR * atr
        rail = t.entry_px - d * RC.MIN_STOP_ATR * atr
        want = min(pstop, rail) if d == 1 else max(pstop, rail)
        g6 = abs(want - t.stop_px) < 1e-6
        ok &= g6
        lines.append(f"  [{'OK ' if g6 else 'BAD'}] stop = beyond the sweep "
                     f"extreme {sp.sweep_extreme:.6f} "
                     f"{'-' if d == 1 else '+'} {RC.STOP_BUF_ATR}×ATR = "
                     f"{pstop:.6f} | rail {rail:.6f} → TAKEN {want:.6f} "
                     f"(R/ATR {t.r_dist / atr:.6f})")
    return rec("F-C5-SPRING", ok, lines)


# ═════════════════════════════════ F-C5-GRID · every cell printed, none dropped
def f_grid() -> bool:
    """FAILS IF: a grid's written table holds fewer cells than the grid declares;
    a declared cell is missing from the fleet table; the selection surface in the
    manifest does not equal the cells actually written; or any cell is marked
    promoted."""
    lines, ok = [], True
    m = man()
    surf = m["selection_surface"]["per_grid"]
    fl = tbl("fleet_unscored")
    lit = {k: v for k, v in T5.GRID_SIZES.items() if k in set(fl["grid"])}
    good = lit == {k: v for k, v in surf.items() if k in set(fl["grid"])}
    ok &= good
    lines.append(f"[{'OK ' if good else 'BAD'}] the manifest's surface equals "
                 f"the INDEPENDENT literal `T5.GRID_SIZES` — declared and "
                 f"written are now two objects, not one counted twice")
    lines.append("      FAILS IF: the literal and the manifest disagree. The "
                 "first draft compared the built cards with the table written "
                 "FROM the built cards and could not fail; this compares a "
                 "hand-declared literal with both.")
    checks = [("fleet grids", lit, fl["grid"].value_counts().to_dict()),
              ("S-SIZE", {"S-SIZE": T5.GRID_SIZES["S-SIZE"]},
               {"S-SIZE": len(tbl("size_grid"))}),
              ("S-ADDSIZE", {"S-ADDSIZE": T5.GRID_SIZES["S-ADDSIZE"]},
               {"S-ADDSIZE": len(tbl("addsize_grid"))}),
              ("S-LIMIT", {"S-LIMIT": T5.GRID_SIZES["S-LIMIT"]},
               {"S-LIMIT": len(tbl("limit_grid"))}),
              # the registrations table carries ONE EXTRA ROW that is not a
              # cell: the card itself, scored through the same ruler as a
              # printed benchmark. It is excluded from the surface because a
              # reference is not something anyone could promote.
              ("registration arms", {"registration arms": T5.GRID_SIZES["registration arms"]},
               {"registration arms": int(
                   (tbl("registrations")["registration"] != "(reference)").sum())})]
    for label, declared, written in checks:
        good = declared == written
        ok &= good
        lines.append(f"[{'OK ' if good else 'BAD'}] {label:20} declared "
                     f"{declared} == written {written}")
    lg_elig = int(((tbl("resistance_league")["asset"] == "__PANEL__")
                   & tbl("resistance_league")["eligible_for_champion"]).sum())
    total = m["selection_surface"]["total_cells_excluding_the_card"]
    recount = (len(fl) - 1 + len(tbl("size_grid")) + len(tbl("addsize_grid"))
               + len(tbl("limit_grid"))
               + int((tbl("registrations")["registration"] != "(reference)").sum())
               + lg_elig)
    good = total == recount
    ok &= good
    lines.append(f"[{'OK ' if good else 'BAD'}] THE SELECTION SURFACE: "
                 f"{total} cells declared before the run == {recount} written")
    lines.append(f"      per grid: {json.dumps(surf)}")
    lines.append("      EVERY CELL IS REPORTED AND NONE IS PROMOTED. The number "
                 "is written down so a future promotion out of these tables "
                 "starts from an m that existed BEFORE the look — which is the "
                 "only thing that makes a later correction mean anything.")
    lines.append("      FAILS IF: a declared cell is absent from its table, or "
                 "a table holds a cell nobody declared. Either way a grid would "
                 "have been reported in part, which is the thing the card "
                 "forbids.")
    rb = tbl("registration_robustness")
    reg_t = tbl("registrations")
    arms = reg_t[reg_t["registration"] != "(reference)"][
        ["registration", "arm"]].drop_duplicates()
    good = len(rb[["registration", "arm"]].drop_duplicates()) == len(arms)
    ok &= good
    lines.append(f"[{'OK ' if good else 'BAD'}] every registration arm carries "
                 f"a ROBUSTNESS block: {len(rb[['registration','arm']].drop_duplicates())} "
                 f"== {len(arms)} arms, each with a full-panel row, 5 "
                 f"leave-one-asset-out rows, a summary and 5 seeds")
    lines.append("      FAILS IF: an arm is scored and not stress-tested. A "
                 "verdict on an interval that is never checked against its own "
                 "panel or its own seed is a verdict about neither.")
    g = m["selection_guard"]
    good = bool(g["loaded"] and g["called"] and g["verdict"]["m"] == 0)
    ok &= good
    lines.append(f"[{'OK ' if good else 'BAD'}] the guard is LOADED and CALLED "
                 f"and IDLES at m={g['verdict']['m']} — nothing was selected, "
                 f"so it has nothing to correct")
    return rec("F-C5-GRID", ok, lines)


# ═══════════════════════════════ F-C5-LEAGUE · the league, from raw bars
def f_league() -> bool:
    """One league row per timeframe, re-derived independently from raw bars.

    FAILS IF: the approach/rejection/penetration counts disagree with an
    independent rescan; an approach is counted from ABOVE (that would measure
    support, not resistance); or the champion named for a timeframe is not the
    highest rejection rate among eligible rows.
    """
    lines, ok = [], True
    lg = tbl("resistance_league")
    per = lg[lg["asset"] != "__PANEL__"]
    # RESCAN THE CHAMPION'S OWN EMA, NOT THE BIGGEST-POPULATION ROW.
    # The first draft re-derived whichever row had the most approaches, which on
    # this table is never a champion — so the four numbers the build actually
    # publishes were verified by nothing. Found by the post-build adversarial
    # review. Each timeframe's CHAMPION EMA is now rescanned, on the asset that
    # contributes most of its approaches.
    champs = {r_["tf"]: int(r_["ema"]) for _, r_ in lg[lg["is_champion_wall"]].iterrows()}
    for tf in T5.LEAGUE_TFS:
        m = per[(per["tf"] == tf) & (per["ema"] == champs.get(tf, -1))]
        if not len(m):
            continue
        r = m.sort_values("approaches", ascending=False).iloc[0]
        sym, L = r["asset"], int(r["ema"])
        d = T5._tf_frame(sym, tf)
        t, h, l_, c = d["t"], d["h"], d["l"], d["c"]
        a = ind.atr(h, l_, c, RC.ATR_LEN)
        e = ind.ema(c, L)
        lo = T5._ms(T5.TIER_E_FROM)
        hi = T5.corridor()[1]
        msk = (t >= lo) & (t <= hi)
        i0 = int(np.argmax(msk))
        i1 = int(len(t) - 1 - np.argmax(msk[::-1]))
        app = rej = 0
        for i in range(max(i0, L + 1), i1 + 1):
            if not (np.isfinite(e[i]) and np.isfinite(a[i]) and a[i] > 0):
                continue
            if not (c[i - 1] < e[i - 1]):
                continue
            if h[i] < e[i] - T5.LEAGUE_APPROACH_ATR * a[i]:
                continue
            app += 1
            w = slice(i, min(i + T5.LEAGUE_RESOLVE_BARS + 1, i1 + 1))
            if not (c[w] > e[w]).any():
                rej += 1
        good = app == int(r["approaches"]) and rej == int(r["rejections"])
        ok &= good
        lines.append(f"[{'OK ' if good else 'BAD'}] {tf:3} CHAMPION EMA{L:<5} "
                     f"on {sym:9} (its largest contributor) — rescan approaches "
                     f"{app} (table {int(r['approaches'])}) · rejections {rej} "
                     f"(table {int(r['rejections'])}) · rate "
                     f"{r['rejection_rate_pct']}%")
        lines.append("      FAILS IF: the raw-bar rescan disagrees. This is the "
                     "leg that reaches the numbers the build PUBLISHES.")
    ch = lg[lg["is_champion_wall"]]
    for _, r in ch.iterrows():
        pool = lg[(lg["tf"] == r["tf"]) & lg["eligible_for_champion"]]
        good = float(r["rejection_rate_pct"]) >= float(
            pool["rejection_rate_pct"].max()) - 1e-9
        ok &= good
        lines.append(f"     CHAMPION WALL {r['tf']:3} = EMA{int(r['ema'])} at "
                     f"{r['rejection_rate_pct']}% over {int(r['approaches'])} "
                     f"approaches — the argmax over {len(pool)} eligible "
                     f"panel cells. THIS RE-CHECK IS AN ARGMAX COMPARED WITH "
                     f"ITS OWN MAX AND CANNOT FAIL; it is printed for the "
                     f"reader, not as evidence.")
    lines.append(f"     THE CHAMPION IS A NAMED MAXIMUM, NOT A PROMOTION: no "
                 f"acceptance bar, no interval, no multiplicity correction, and "
                 f"the {int(((lg['asset'] == '__PANEL__') & lg['eligible_for_champion']).sum())} "
                 f"eligible cells it is chosen from are in the LOGGED SELECTION "
                 f"SURFACE. Found by the post-build adversarial review, which "
                 f"noted an argmax over 54 uncounted cells was being called the "
                 f"build's strongest Tier-E result.")
    lines.append("      APPROACH is FROM BELOW by construction — the previous "
                 "bar must have CLOSED below the EMA. FAILS IF that condition "
                 "is dropped: the table would then measure support and "
                 "resistance together and mean neither.")
    return rec("F-C5-LEAGUE", ok, lines)


# ══════════════════════════════════════════════════════ F-C5-DET · determinism
def f_det() -> bool:
    """FAILS IF: any table's content hash, or the counts block, or the seal
    record, differs between two full runs.  Normalised: wall clock only."""
    lines = []
    a = man()
    p2 = T5.OUT_RERUN / "build_manifest.json"
    if not p2.exists():
        return rec("F-C5-DET", False, ["re-run manifest absent — run --rerun"])
    b = json.loads(p2.read_text())
    ok = True
    for k in sorted(a["sha"]):
        same = a["sha"][k] == b["sha"].get(k)
        ok &= same
        lines.append(f"[{'OK ' if same else 'BAD'}] {k:16} {a['sha'][k][:32]}")
    same = a["counts"] == b["counts"]
    ok &= same
    lines.append(f"[{'OK ' if same else 'BAD'}] counts block identical")
    sa = {k: v for k, v in a["seal"].items()}
    sb = {k: v for k, v in b["seal"].items()}
    same = sa == sb
    ok &= same
    lines.append(f"[{'OK ' if same else 'BAD'}] seal record identical")
    lines.append("")
    lines.append("NORMALISATION DISCLOSURE — normalised fields: 'elapsed_s' and "
                 "'wall_clock_at_run'/'cache_lag_hours' inside the corridor "
                 "block, which are wall clock by definition. NO COMPUTED VALUE "
                 "IS NORMALISED. The corridor's own EDGES are compared and must "
                 "match, so a cache that moved between runs would FAIL this leg "
                 "rather than be excused by it.")
    good = (a["corridor"]["panel_start"] == b["corridor"]["panel_start"]
            and a["corridor"]["last_closed_4h_open"]
            == b["corridor"]["last_closed_4h_open"])
    ok &= good
    lines.append(f"[{'OK ' if good else 'BAD'}] corridor edges identical across "
                 f"runs: {a['corridor']['panel_start']} → "
                 f"{a['corridor']['last_closed_4h_open']}")
    lines.append(f"seed {T5.SEED} is printed and used ONLY by the asset-cluster "
                 f"bootstrap in the registrations; every other number in this "
                 f"build is structural, and the bootstrap is seeded so it is "
                 f"reproducible rather than merely stable.")
    return rec("F-C5-DET", ok, lines)


# ═════════════════════════════ F-C5-6 · captured-not-consulted, on the tape
def f_closure() -> bool:
    """FAILS IF: the decision path imports `analytics` anywhere in its transitive
    closure, or names a tape column in its CODE (comments and docstrings are
    stripped — Tier-C4 learned that a raw-text scan false-positives on a
    module's own prose)."""
    lines, ok = [], True
    names = ("tierc5_rules", "tierc4_rules", "tierc3_rules", "tierc2_rules")
    srcs = {f"scripts/{n}.py": (ROOT / "scripts" / f"{n}.py").read_text()
            for n in names}
    for name, src in srcs.items():
        imported = []
        for node in ast.walk(ast.parse(src)):
            if isinstance(node, ast.Import):
                imported += [a.name for a in node.names]
            elif isinstance(node, ast.ImportFrom):
                imported.append(node.module or "")
        hits = [m for m in imported if m == "analytics"
                or m.startswith("analytics.")]
        g = not hits
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] AST import scan of {name}: "
                     f"{sorted(set(imported))} — analytics hits = {hits}")
    import tierc5_rules  # noqa: F401
    seen, stack = set(), ["tierc5_rules"]
    while stack:
        mm = stack.pop()
        if mm in seen:
            continue
        seen.add(mm)
        mod = sys.modules.get(mm)
        if mod is None:
            continue
        for v in vars(mod).values():
            n = getattr(v, "__name__", None) if isinstance(v, type(sys)) else None
            if n and n not in seen:
                stack.append(n)
    bad = sorted(m for m in seen if m == "analytics" or m.startswith("analytics."))
    g = not bad
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] transitive closure of "
                 f"tierc5_rules: {len(seen)} modules, analytics members = {bad}")
    proj = {"engine", "tierc5_rules", "tierc4_rules", "tierc3_rules",
            "tierc2_rules"}
    lines.append(f"    project members: "
                 f"{sorted(m for m in seen if m.split('.')[0] in proj)}")
    tape_cols = ["wall_family", "dist_atr", "coloc_n", "nearest_level",
                 "rvwap", "avwap", "prior_extreme"]
    code = {n: F4.code_only(s) for n, s in srcs.items()}
    named = {n: [c for c in tape_cols if c in s] for n, s in code.items()}
    g = not any(named.values())
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] tape column names in the decision "
                 f"path's CODE (comments/docstrings stripped by AST round-trip, "
                 f"string literals KEPT): {named}")
    tp = tbl("analytics_tape")
    lines.append(f"    tape CAPTURED: {len(tp):,} rows, instants "
                 f"{tp['instant'].value_counts().to_dict()}")
    lines.append(f"    the spine is WEEKLY, not daily: the corridor is ~21x "
                 f"Tier-C4's, and a daily spine would put ~63k rows on a table "
                 f"nothing reads back. One rule, stated, not tuned.")
    lines.append("      FAILS IF: any decision module imports analytics, or "
                 "names a tape column in code. The tape is joined by timestamp "
                 "AFTER the fact and never read back into a decision.")
    return rec("F-C5-6", ok, lines)


# ════════════════════════════════════════════════════════ F-KEY · every join
def f_keys() -> bool:
    """FAILS IF: any written table has a duplicate on its declared key; the
    headline does not reconcile to the journal; the ratchet ledger does not
    reconcile to the journal's advance counts; or a slice's book does not sum
    to the whole."""
    lines, ok = [], True
    keys = {"corridor_and_seal": [], "funnel": ["asset", "direction"],
            "headline": ["group", "key"], "headline_by_slice": ["group", "key"],
            "trade_journal": ["asset", "entry_ms"],
            "ratchet_ledger": ["asset", "entry_ms", "advance_seq"],
            "registrations": ["registration", "arm"],
            "registration_text": ["registration"],
            "registration_robustness": ["registration", "arm", "check",
                                        "variant"],
            "fleet_unscored": ["grid", "cell"],
            "harvest_lab": ["asset", "entry_ms", "entry_ts"],
            "ae_study": ["population"], "limit_grid": ["level_x_avg_ae"],
            "size_grid": ["unit"], "addsize_grid": ["add_tranche_x_base"],
            "resistance_league": ["asset", "tf", "ema"],
            "midband_confluence": ["asset", "tf", "event"],
            "analytics_tape": ["asset", "ts"],
            "tape_inventory": ["instant", "column"], "lineage": ["version"],
            "d13c_counted_not_scored": ["slice", "asset", "entry_ts"]}
    for name, k in keys.items():
        d = tbl(name)
        dup = int(d.duplicated(subset=k).sum()) if (len(d) and k) else 0
        good = dup == 0
        ok &= good
        lines.append(f"[{'OK ' if good else 'BAD'}] {name:26} key={k} "
                     f"rows={len(d):,} dup={dup}")
    j = tbl("trade_journal")
    h = tbl("headline")
    a = h[(h["group"] == "ALL") & (h["key"] == "ALL")].iloc[0]
    good = abs(float(a["net_r"]) - float(j["net_r"].astype(float).sum())) < 1e-3
    ok &= good
    lines.append(f"[{'OK ' if good else 'BAD'}] headline net_r "
                 f"{float(a['net_r']):.4f} == sum(journal.net_r) "
                 f"{float(j['net_r'].astype(float).sum()):.4f}; n={int(a['n'])}"
                 f" == {len(j)}")
    rl = tbl("ratchet_ledger")
    good = len(rl) == int(j["n_advances"].astype(int).sum())
    ok &= good
    lines.append(f"[{'OK ' if good else 'BAD'}] ratchet_ledger {len(rl)} == "
                 f"sum(journal.n_advances) {int(j['n_advances'].astype(int).sum())}")
    # per-asset and per-direction cuts must sum to ALL
    for grp in ("asset", "direction"):
        s = h[h["group"] == grp]["net_r"].astype(float).sum()
        good = abs(s - float(a["net_r"])) < 1e-3
        ok &= good
        lines.append(f"[{'OK ' if good else 'BAD'}] the {grp} cut sums to ALL: "
                     f"{s:.4f} == {float(a['net_r']):.4f}")
    # the YEAR slices must partition the book
    bs = tbl("headline_by_slice")
    yr = bs[bs["group"] == "year"]
    good = int(yr["n"].sum()) == len(j)
    ok &= good
    lines.append(f"[{'OK ' if good else 'BAD'}] the YEAR slices PARTITION the "
                 f"book by entry: {int(yr['n'].sum())} == {len(j)} campaigns")
    lines.append("      FAILS IF: a campaign falls in two years or none — the "
                 "slices are reported, never gated, but a slice set that does "
                 "not partition would double-count the book.")
    era = bs[bs["group"] == "era"]
    good = int(era["n"].sum()) == len(j)
    ok &= good
    lines.append(f"[{'OK ' if good else 'BAD'}] the pre/post-2024-07-01 split "
                 f"partitions the book: {int(era['n'].sum())} == {len(j)}")
    return rec("F-KEY", ok, lines)


def main() -> int:
    print("=" * 78)
    print("TIER-C5 FIXTURE TRANSCRIPT — FULL WATER, THE BOX OPEN")
    print("=" * 78)
    f_open()
    f_ctrl()
    f_inherit()
    f_rail()
    f_harv()
    f_spring()
    f_grid()
    f_league()
    f_det()
    f_closure()
    f_keys()
    print("\n".join(T))
    n_ok = sum(RESULTS.values())
    print()
    print("=" * 78)
    print(f"FIXTURE SUMMARY  {n_ok}/{len(RESULTS)} PASS  {json.dumps(RESULTS)}")
    print(f"  I9: ANALYTICS_VERSION {AN.ANALYTICS_VERSION} · analytics_sha "
          f"{AN.analytics_sha()}")
    print("=" * 78)
    if n_ok < len(RESULTS):
        print("*** HALT: fixture mismatch. Nothing downstream is trustworthy. ***")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
