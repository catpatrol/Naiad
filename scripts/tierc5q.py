"""TIER-C5-Q · STAGE Q1 — THE QUERYABLE BOOK.

RATIFIED operator 2026-08-16: *"projecting the analytics package… instantly
queryable for every trade… ≥3 years"*.  Drafted APOLLO · Executor HEPHAESTUS ·
Seed 20260816.

CLASS: ADDITIVE TOOLING.  **NO SCORED NUMBER MAY CHANGE.**  Nothing here writes
into `research_outputs/tierc5/`; the TC5 tables stay exactly as filed, because
they are the record of what that build captured and a record that moves when a
tool is added is not a record.  `F-Q-0` asserts the headline, registration and
fleet tables are byte-identical to the manifest committed at HEAD — not argued
from the fact that this module does not touch them, but checked against git.

────────────────────────────────────────────────────────────────────────────
WHAT THIS BUILDS, AND WHY IT IS A SUPERSET RATHER THAN A REPLACEMENT
────────────────────────────────────────────────────────────────────────────
TC5's own tape was a WEEKLY spine plus arming/trigger/exit/harvest instants —
3,118 rows, sized for a build document.  A tape you can *interrogate* is a
different object: it has to answer "what did the registry look like at THIS
campaign's third trail advance" without a rebuild, for every campaign, over the
whole corridor.  So Q1 emits:

    tape_full        one row per (asset, ts) at EVERY instant the book touches
                     — arming · trigger · every add · every harvest · every
                     trail advance · exit — PLUS the DAILY 00:00Z spine over
                     the full corridor (2019-09-08 → the latest closed 4h bar,
                     ~6.9 y, comfortably the ruled 3 y and then some).
    campaigns        one row per campaign across BOTH lanes, with a stable
                     `campaign_id` a human can type.
    instants         the (campaign_id, kind, ts) ledger the tool joins on.
    advances / harvests / adds   the per-campaign ledgers, keyed the same way.
    coverage         F-Q-1's own evidence: zero campaigns and zero instants
                     missing, counted per lane and per kind.

LEVEL FAMILIES, as ruled: the **AVWAP set** (week/month/year anchors), **RVWAP
±1σ and ±2σ** (7/30/90/365-day windows), **period extremes** (prior day/week/
month high and low) — all three inherited wholesale from
`tierc2_baseline.build_level_series`, the estate's own object — plus, NEW here,
**the league champion EMA distances**.

THE CHAMPIONS ARE READ ON THEIR OWN CLOCKS.  TC5's league named EMA 889 on 12h
AND 1d, EMA 3618 on 4h, EMA 4618 on 1h.  Measuring all of them on the 4h lens
would be a different quantity from the one the league scored, so each is read
as-of the LAST CLOSED bar of ITS OWN timeframe.  That is the only reading under
which "the league champion distance" means what the league meant.

CAPTURED-NOT-CONSULTED IS UNCHANGED.  This module imports `analytics`; the
DECISION PATH (`tierc5_rules` and its parents) does not, and F-Q-6 re-runs the
closure proof.  Nothing here is read back into a decision — there are no
decisions here to read it back into.

USAGE
    ~/venvs/naiad/bin/python scripts/tierc5q.py
    ~/venvs/naiad/bin/python scripts/tierc5q.py --rerun
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import tierc5 as T5                                                 # noqa: E402
import tierc5_rules as RC                                           # noqa: E402
import tierc2_baseline as TB                                        # noqa: E402
import analytics as AN                                              # noqa: E402
from analytics import structure as AS                               # noqa: E402
from engine import indicators as ind                                # noqa: E402

_ms, iso, r4, r6, pct = TB._ms, TB.iso, TB.r4, TB.r6, TB.pct
write_table, assert_key = TB.write_table, TB.assert_key
load_klines = TB.load_klines
MS_4H, MS_1H, MS_1D = TB.MS_4H, TB.MS_1H, TB.MS_1D
log = TB.log

SEED = 20260816
OUT = ROOT / "research_outputs" / "tierc5q"
OUT_RERUN = ROOT / "research_outputs" / "tierc5q_run2"
TC5 = ROOT / "research_outputs" / "tierc5"

# THE LEAGUE CHAMPIONS, each on its own clock — TC5 §6.2.
CHAMPIONS = (("1h", 4618), ("4h", 3618), ("12h", 889), ("1d", 889))

# THE SCORED TABLES F-Q-0 GUARDS.  Named here so the guarantee is a list, not
# a sentence: these three may not move, whatever else this tooling does.
FROZEN = ("headline", "registrations", "fleet")

# THE COMPLETENESS CONTRACT — DERIVED, NOT LISTED.
# `coverage` checks that every instant in the ledger has a tape row, and that is
# CIRCULAR: the tape is built FROM the ledger, so of course it is covered. The
# check with content is the other one — does the LEDGER hold every timestamped
# bar the decision path names? Every `_ms` field on the record types is mapped
# to an instant kind here, and F-Q-1 walks the dataclasses and asserts the map
# is TOTAL. Add a timestamped event to `Trade` and forget a kind, and that leg
# fails. Found by the builder's own audit, before the review returned.
MS_FIELD_MAP = {
    "Trade.arm_ms": "arming",
    "Trade.entry_ms": "trigger",
    "Trade.exit_ms": "exit",
    "Trade.harvest_ms": "harvest",
    "Trade.anchor_bar_ms": "anchor_bar",
    "Advance.conf_ms": "advance",
    "Advance.pivot_bar_ms": "pivot_bar",
    "Add.ms": "add",
    "Add.retrace_ms": "retrace",
    "Spring.sweep_ms": "sweep",
    # `Spring.reclaim_ms` IS the entry bar by construction — the reclaim close
    # is the entry — so it is covered by `trigger`. Named here rather than left
    # to look like an omission.
    "Spring.reclaim_ms": "trigger",
}


# ═══════════════════════════════════════════════════ identity, once and stable
def campaign_id(asset: str, lane: str, entry_ms: int) -> str:
    """A human-TYPABLE, sortable, collision-free id.

    `ETHUSDT:card:20251029T1600`.  Asset first because that is how a reader
    thinks; lane second because the same asset can hold a card campaign and a
    spring campaign at different instants; the entry instant last because it is
    what makes it unique.  A hash would be shorter and nobody could type it
    from a table they are looking at.
    """
    t = iso(entry_ms)
    return f"{asset}:{lane}:{t[:4]}{t[5:7]}{t[8:10]}T{t[11:13]}{t[14:16]}"


# ═══════════════════════════════════════════════ the champion EMA, on its clock
def champion_series(sym: str) -> dict[str, dict]:
    """Per champion (tf, ema): the EMA series on its OWN timeframe, plus that
    timeframe's ATR and the bar-CLOSE timestamps needed to read it as-of an
    arbitrary instant without look-ahead.

    `close_ms = open_ms + step` is the instant the bar became knowable, so a
    caller at instant `t` takes the last bar with `close_ms <= t`.  That is the
    whole causality argument and it is one line.
    """
    out = {}
    for tf, L in CHAMPIONS:
        d = T5._tf_frame(sym, tf)
        step = {"1h": MS_1H, "4h": MS_4H, "12h": 12 * MS_1H, "1d": MS_1D}[tf]
        out[f"{tf}_ema{L}"] = {
            "close_ms": d["t"] + step,
            "ema": ind.ema(d["c"], L),
            "atr": ind.atr(d["h"], d["l"], d["c"], RC.ATR_LEN),
            "tf": tf, "ema_len": L,
        }
    return out


def champion_cols(ch: dict, close_px: np.ndarray, ts: np.ndarray,
                  as_of_step: int = MS_4H) -> dict:
    """Signed distance in that timeframe's OWN ATR, positive = price ABOVE the
    wall.  Same sign convention as `tape_rows`.

    TWO THINGS HERE ARE NOT OBVIOUS AND BOTH WERE WRONG IN THE FIRST DRAFT.

    (1) THE AS-OF INSTANT IS THE BAR'S **CLOSE**, NOT ITS OPEN.  A tape row is
    keyed on the 4h bar's OPEN time, but every other column in it — the close,
    the ATR, the level families, the EMAs — is the value AT THAT BAR'S CLOSE,
    which is the instant the card actually decided.  Selecting champion bars
    with `close_ms <= open_ts` made the champion four hours staler than the
    price it is differenced against.  The as-of is `ts + as_of_step`.  This is
    not look-ahead: the row's own close is knowable at exactly that instant.

    (2) THE EMA MUST BE WARM.  `engine.indicators.ema` SEEDS at the series
    start and never returns NaN, so `isfinite` is true from bar 0 and a
    4,618-length EMA would publish the first close of the series as a "wall".
    TC5 had to add `WARMUP_BARS = 316` to the decision path for exactly this,
    and the first draft of this module reintroduced it with EMAs three to
    fifteen times longer.  A champion is emitted only from bar index >= its own
    length; before that the columns are NULL and the count is disclosed.
    Found by the post-build adversarial review, which called it verbatim.
    """
    cols: dict[str, list] = {}
    as_of = ts + as_of_step
    for name, s in ch.items():
        k = np.searchsorted(s["close_ms"], as_of, "right") - 1
        L = s["ema_len"]
        warm = k >= L                       # the EMA has seen its own length
        ok = (k >= 0) & warm
        val = np.full(len(ts), np.nan)
        dist = np.full(len(ts), np.nan)
        a = np.full(len(ts), np.nan)
        val[ok] = s["ema"][k[ok]]
        a[ok] = s["atr"][k[ok]]
        good = ok & np.isfinite(val) & np.isfinite(a) & (a > 0)
        dist[good] = (close_px[good] - val[good]) / a[good]
        cols[f"champ_{name}"] = [r6(v) for v in val]
        cols[f"champ_{name}_dist_atr"] = [r6(v) for v in dist]
        cols[f"champ_{name}_warm"] = [bool(v) for v in ok]
    return cols


# ═════════════════════════════════════════════════════ the books, re-derived
def books(lo_ms: int, hi_ms: int) -> tuple[list, list, list]:
    """The three TC5 books, from the SAME code path that scored them.

    Re-derived rather than read from parquet because the query tool needs the
    live objects — advances, adds, spring records — and the filed tables carry
    summaries of them.  F-Q-0 then asserts the re-derivation did not move a
    scored number, which is the check that makes re-deriving safe.
    """
    card = T5.run_cell(RC.V5, lo_ms, hi_ms)
    spring = T5.run_cell(RC.Card(name="spring", grid="P-SPR-1", lane="spring"),
                         lo_ms, hi_ms)
    adds = T5.run_cell(RC.Card(name="adds", grid="P-CASC-1",
                               adds_max=RC.ADDS_MAX), lo_ms, hi_ms)
    return card, spring, adds


def campaign_rows(card: list, spring: list, adds: list) -> pd.DataFrame:
    """One row per campaign, both lanes, with the ADD ledger folded onto its
    card twin.

    The adds book is NOT a third population: an add rides inside a campaign and
    cannot create or destroy one, so the adds run yields the same 195 campaigns
    with the same entries and the same exits — only the accounting differs.
    Modelling it as a third book would have invented 195 campaigns that do not
    exist. The add columns are therefore carried on the card row and named
    `adds_*` so nobody reads them as the campaign's own R.
    """
    ak = {(t.symbol, t.entry_ms): t for t in adds}
    rows = []
    for lane, book in (("card", card), ("spring", spring)):
        for t in book:
            a = ak.get((t.symbol, t.entry_ms)) if lane == "card" else None
            rows.append({
                "campaign_id": campaign_id(t.symbol, lane, t.entry_ms),
                "asset": t.symbol, "lane": lane,
                "direction": "long" if t.direction == 1 else "short",
                "mandate": ("CARD v5 — 12/89 arming, tide, d>=0.75, 12/26 trigger"
                            if lane == "card" else
                            "SPRING LANE P-SPR-1 — 96-bar sweep, reclaim <=3 bars"),
                "arm_ms": t.arm_ms, "arm_ts": iso(t.arm_ms),
                "entry_ms": t.entry_ms, "entry_ts": iso(t.entry_ms),
                "entry_px": r6(t.entry_px), "stop_px": r6(t.stop_px),
                "r_dist": r6(t.r_dist), "atr_at_entry": r6(t.atr_at_entry),
                "r_over_atr": r6(t.r_dist / t.atr_at_entry if t.atr_at_entry else None),
                "anchor": r6(t.anchor),
                "anchor_bar_ts": iso(t.anchor_bar_ms) if t.anchor_bar_ms > 0 else None,
                "anchor_was_sealed": bool(t.anchor_was_sealed),
                "disp_at_arming": r6(t.disp_at_arming),
                "window_age_bars": int(t.entry_i - t.arm_i),
                "exit_ms": t.exit_ms, "exit_ts": iso(t.exit_ms),
                "exit_px": r6(t.exit_px), "exit_reason": t.exit_reason,
                "bars_held": int(t.bars_held),
                "n_advances": len(t.advances),
                "final_stop_px": r6(t.final_stop_px),
                "stop_advanced_atr": r6(t.stop_advanced_atr),
                "ratchet_exit": bool(t.ratchet_exit),
                "harvested": bool(t.harvested),
                "harvest_ts": iso(int(t.harvest_ms)) if t.harvest_ms else None,
                "net_r_harvest_half": r6(t.net_r_harvest_half),
                "net_r_runner_half": r6(t.net_r_runner_half),
                "harvest_ride_would_have_r": r6(t.harvest_ride_would_have_r),
                "mfe_r": r6(t.mfe_r), "mae_to_1r_r": r6(t.mae_to_1r_r),
                "reached_1r": bool(t.reached_1r),
                "spring_sweep_ts": iso(t.spring.sweep_ms) if t.spring else None,
                "spring_swept_level": r6(t.spring.swept_level) if t.spring else None,
                "spring_sweep_extreme": r6(t.spring.sweep_extreme) if t.spring else None,
                "spring_bars_to_reclaim": (t.spring.bars_to_reclaim if t.spring
                                           else None),
                "gross_r": r6(t.gross_r), "fee_r": r6(t.fee_r),
                "funding_r": r6(t.funding_r),
                "funding_r_uncapped": r6(t.funding_r_uncapped),
                "funding_ceiling_bound": bool(t.funding_ceiling_bound),
                "net_r": r6(t.net_r),
                # ── the adds overlay, on the card row only ──────────────────
                "adds_n": (len(a.adds) if a else 0),
                "adds_r": (r6(a.add_r) if a and a.add_r is not None else None),
                "adds_net_r_of_campaign": (r6(a.net_r) if a else None),
                "adds_delta_vs_card": (r6(a.net_r - t.net_r) if a else None),
            })
    d = pd.DataFrame(rows)
    return d.sort_values(["entry_ms", "asset", "lane"]).reset_index(drop=True)


def ledger_rows(card: list, spring: list, adds: list
                ) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """The instant ledger and the three per-campaign ledgers.

    THE INSTANT LEDGER IS THE COVERAGE CONTRACT.  Every row here is a
    (campaign_id, kind, ts) the tape MUST hold a snapshot for, and F-Q-1
    asserts the join is total. If a kind were ever added to the ride and not
    added here, the coverage assert would still pass — so the kinds are
    enumerated from the campaign objects themselves, not from a literal list.
    """
    inst, advs, harv, addr = [], [], [], []
    ak = {(t.symbol, t.entry_ms): t for t in adds}
    for lane, book in (("card", card), ("spring", spring)):
        for t in book:
            cid = campaign_id(t.symbol, lane, t.entry_ms)
            inst.append((cid, t.symbol, "arming", t.arm_ms))
            inst.append((cid, t.symbol, "trigger", t.entry_ms))
            inst.append((cid, t.symbol, "exit", t.exit_ms))
            # THE THREE BARS THE CARD'S LIST DID NOT NAME, AND A QUERYABLE BOOK
            # NEEDS ANYWAY. The commission named arming/trigger/add/harvest/
            # advance/exit. But `anchor_bar` is where the ENTRY STOP's price was
            # quoted from — a published price that gets paid out — and
            # `pivot_bar` is the same for every advance. A book that prints
            # those prices and cannot say what the walls looked like at the bar
            # they came from is not queryable, it is nearly queryable. Added on
            # the builder's own audit, not on the card's list.
            if t.anchor_bar_ms > 0:
                inst.append((cid, t.symbol, "anchor_bar", t.anchor_bar_ms))
            if t.spring is not None:
                inst.append((cid, t.symbol, "sweep", t.spring.sweep_ms))
            for k, a in enumerate(t.advances):
                inst.append((cid, t.symbol, "advance", a.conf_ms))
                inst.append((cid, t.symbol, "pivot_bar", a.pivot_bar_ms))
                advs.append({
                    "campaign_id": cid, "asset": t.symbol, "advance_seq": k + 1,
                    "conf_ts": iso(a.conf_ms),
                    "governs_from_ts": iso(a.conf_ms + MS_4H),
                    "pivot_val": r6(a.pivot_val),
                    "pivot_bar_ts": iso(a.pivot_bar_ms),
                    "atr_at_conf": r6(a.atr), "close_at_conf": r6(a.close),
                    "cand_px": r6(a.cand_px), "rail_px": r6(a.rail_px),
                    "prev_stop_px": r6(a.prev_stop), "new_stop_px": r6(a.new_stop),
                    "advance_atr": r6(abs(a.new_stop - a.prev_stop) / a.atr),
                    "binding_side": "RAIL" if a.rail_binding else "PIVOT",
                    "dist_from_close_atr": r6(a.dist_from_close_over_atr),
                    "bars_after_entry": int(a.conf_i - t.entry_i),
                    "is_final_stop": bool(k == len(t.advances) - 1),
                    "paid_out": bool(k == len(t.advances) - 1
                                     and t.exit_reason == "stop"),
                })
            if t.harvested:
                inst.append((cid, t.symbol, "harvest", int(t.harvest_ms)))
                harv.append({
                    "campaign_id": cid, "asset": t.symbol,
                    "harvest_ts": iso(int(t.harvest_ms)),
                    "bars_after_entry": int(t.harvest_i - t.entry_i),
                    "fill_px": r6(t.harvest_px),
                    "unit_move_at_harvest_r": r6(t.harvest_unit_move_r),
                    "took_r": r6(t.net_r_harvest_half),
                    "would_have_r": r6(t.harvest_ride_would_have_r),
                    "delta_r": r6(float(t.net_r_harvest_half)
                                  - float(t.harvest_ride_would_have_r)),
                    "helped": bool(float(t.net_r_harvest_half)
                                   > float(t.harvest_ride_would_have_r)),
                    "runner_half_r": r6(t.net_r_runner_half),
                })
            a5 = ak.get((t.symbol, t.entry_ms)) if lane == "card" else None
            if a5:
                for k, ad in enumerate(a5.adds):
                    inst.append((cid, t.symbol, "add", ad.ms))
                    inst.append((cid, t.symbol, "retrace", ad.retrace_ms))
                    addr.append({
                        "campaign_id": cid, "asset": t.symbol, "add_seq": k + 1,
                        "add_ts": iso(ad.ms), "add_px": r6(ad.px),
                        "size": ad.size,
                        "retrace_ts": iso(ad.retrace_ms),
                        "bars_after_entry": int(ad.i - t.entry_i),
                        "unit_move_at_add_r": r6((ad.px - t.entry_px)
                                                 * t.direction / t.r_dist),
                    })
    di = pd.DataFrame(inst, columns=["campaign_id", "asset", "kind", "ts"])
    di["ts_iso"] = di["ts"].map(lambda m: iso(int(m)))
    di = di.drop_duplicates(subset=["campaign_id", "kind", "ts"])
    return (di.sort_values(["ts", "campaign_id", "kind"]).reset_index(drop=True),
            pd.DataFrame(advs), pd.DataFrame(harv), pd.DataFrame(addr))


def d15_per_campaign(camp: pd.DataFrame) -> pd.DataFrame:
    """D15, RENDERED PER CAMPAIGN — and the rendering is NAMED, because the
    fleet's D15 columns are CELL-level by construction and cannot simply be
    reprinted on a row.

    `paired_delta_expectancy`, `tail_exit_ratio` and
    `max_single_trade_delta_share` compare two BOOKS; a single campaign has no
    counterpart book.  What a single campaign CAN carry is the same three
    questions asked of it:
        share_of_lane_net_r   how much of its own lane's result IS this trade
        in_lane_top_decile    is it in the tail the ratio measures
        slice_provisional     does it sit in a slice the build flags thin
        adds_delta_vs_card    the one genuinely paired delta a campaign owns
    Printed under the heading "D15 (per campaign)" so nobody reads them as the
    fleet columns of the same name.
    """
    out = []
    for lane, g in camp.groupby("lane"):
        g = g.copy()
        tot = float(g["net_r"].astype(float).sum())
        rs = sorted(g["net_r"].astype(float), reverse=True)
        k = max(int(np.floor(0.10 * len(rs))), 1)
        cut = rs[k - 1] if rs else None
        g["lane_net_r"] = r4(tot)
        g["share_of_lane_net_r"] = [
            (r6(v / tot) if abs(tot) > 1e-12 else None)
            for v in g["net_r"].astype(float)]
        g["in_lane_top_decile"] = [bool(cut is not None and v >= cut)
                                   for v in g["net_r"].astype(float)]
        out.append(g)
    d = pd.concat(out, ignore_index=True)
    d["slice_year"] = d["entry_ts"].str[:4]
    n_by_year = d[d["lane"] == "card"].groupby("slice_year").size().to_dict()
    d["slice_provisional"] = [
        bool(n_by_year.get(y, 0) < RC.PROVISIONAL_MIN_N) for y in d["slice_year"]]
    return d.sort_values(["entry_ms", "asset", "lane"]).reset_index(drop=True)


# ═══════════════════════════════════════════════════════ the enriched tape
def build_tape(inst: pd.DataFrame, lo_ms: int, hi_ms: int) -> pd.DataFrame:
    """One row per (asset, ts): every book instant PLUS the daily 00:00Z spine.

    `TB.tape_rows` and `TB.build_level_series` are the estate's own objects and
    are BOUND, not reimplemented — the AVWAP set, the RVWAP ±1σ/±2σ bands, the
    prior period extremes, the single-wall stamp and the co-location count all
    come out of them unchanged.  What is added here is the league champion
    block and the funnel state (tide, ribbon).

    THE SPINE IS DAILY, NOT WEEKLY.  TC5 used weekly because a build document
    does not read a tape back; a query tool does, and "what did the walls look
    like on the day before this trade" is the first question anyone asks.
    """
    frames = []
    for sym in RC.UNIVERSE:
        st = T5.frame(sym)
        k4, f = st["k4"], st["f"]
        ot = f.open_ms
        want = set(int(v) for v in inst.loc[inst["asset"] == sym, "ts"])
        spine = [int(v) for v in ot if lo_ms <= v <= hi_ms and v % MS_1D == 0]
        want |= set(spine)
        kinds = (inst[inst["asset"] == sym].groupby("ts")["kind"]
                 .apply(lambda s: "+".join(sorted(set(s)))).to_dict())
        rows = sorted(want)
        labelled = [(t, kinds.get(t, "spine")) for t in rows]
        tp = TB.tape_rows(sym, k4, load_klines(sym, "1h"), labelled, "FULL_WATER")
        if not len(tp):
            continue
        ts = tp["ts"].to_numpy(np.int64)
        idx = np.searchsorted(ot, ts)
        idx = np.clip(idx, 0, len(ot) - 1)
        # ── the league champions, each on its own clock ────────────────────
        for c, v in champion_cols(champion_series(sym), f.c[idx], ts).items():
            tp[c] = v
        # ── the funnel state at the instant ───────────────────────────────
        e89, e316, cl = f.e89[idx], f.e316[idx], f.c[idx]
        up = (e89 > e316) & (cl > e316)
        dn = (e89 < e316) & (cl < e316)
        tp["tide_state"] = np.where(up, "up", np.where(dn, "down", "none"))
        tp["e89"] = [r6(v) for v in e89]
        tp["e316"] = [r6(v) for v in e316]
        tp["e12"] = [r6(v) for v in f.e12[idx]]
        tp["e26"] = [r6(v) for v in f.e26[idx]]
        tp["disp_atr"] = [r6(v) for v in
                          np.abs(cl - e89) / np.where(f.atr[idx] > 0,
                                                      f.atr[idx], np.nan)]
        rs = TB.ribbon_state(sym)
        if len(rs):
            assert_key(rs, ["ts"], f"ribbon_state[{sym}]")
            tp = tp.merge(rs, on="ts", how="left", validate="1:1")
        frames.append(tp)
    return pd.concat(frames, ignore_index=True)


def coverage(inst: pd.DataFrame, tape: pd.DataFrame,
             camp: pd.DataFrame) -> pd.DataFrame:
    """F-Q-1's OWN EVIDENCE — per lane and per kind, how many instants were
    demanded and how many the tape holds.

    WHAT WOULD MAKE THIS FAIL: one instant in the ledger with no (asset, ts)
    row in the tape, or one campaign with no instants at all.  Both are counted
    here and asserted in the fixture; a coverage table that only prints totals
    would hide a whole missing KIND behind a large number.
    """
    have = set(map(tuple, tape[["asset", "ts"]].astype({"ts": "int64"}).values))
    inst = inst.copy()
    inst["covered"] = [(a, int(t)) in have
                       for a, t in zip(inst["asset"], inst["ts"])]
    lane = dict(zip(camp["campaign_id"], camp["lane"]))
    inst["lane"] = inst["campaign_id"].map(lane)
    g = (inst.groupby(["lane", "kind"], as_index=False)
         .agg(instants=("covered", "size"), covered=("covered", "sum")))
    g["missing"] = g["instants"] - g["covered"]
    tot = pd.DataFrame([{
        "lane": "__ALL__", "kind": "__ALL__", "instants": len(inst),
        "covered": int(inst["covered"].sum()),
        "missing": int(len(inst) - inst["covered"].sum())}])
    camps = pd.DataFrame([{
        "lane": "__CAMPAIGNS__", "kind": ln,
        "instants": int((camp["lane"] == ln).sum()),
        "covered": int(camp.loc[camp["lane"] == ln, "campaign_id"]
                       .isin(inst["campaign_id"]).sum()),
        "missing": int((camp["lane"] == ln).sum()
                       - camp.loc[camp["lane"] == ln, "campaign_id"]
                       .isin(inst["campaign_id"]).sum())}
        for ln in sorted(camp["lane"].unique())])
    return pd.concat([g, camps, tot], ignore_index=True)


# ═══════════════════════════════════════════════════════════════ the driver
def run(root: Path) -> dict:
    t0 = time.time()
    man: dict = {"seed": SEED, "stage": "TIER-C5-Q · Q1 the queryable book",
                 "sha": {}, "counts": {}}
    log("=" * 78)
    log("TIER-C5-Q · STAGE Q1 — the queryable book")
    log("=" * 78)
    log(f"  analytics {AN.ANALYTICS_VERSION}  sha {AN.analytics_sha()[:16]}…")

    lo_ms, hi_ms, cmeta = T5.corridor()
    man["corridor"] = {k: v for k, v in cmeta.items()
                       if k not in ("wall_clock_at_run", "cache_lag_hours")}
    log(f"  CORRIDOR {cmeta['panel_start']} -> {cmeta['last_closed_4h_close']} "
        f"({cmeta['span_days']} d = {cmeta['span_days']/365.25:.2f} y)")

    card, spring, adds = books(lo_ms, hi_ms)
    log(f"  BOOKS  card {len(card)} · spring {len(spring)} · "
        f"add-carrying {sum(1 for t in adds if t.adds)}")

    camp = d15_per_campaign(campaign_rows(card, spring, adds))
    inst, advs, harv, addr = ledger_rows(card, spring, adds)
    log(f"  INSTANTS demanded: {len(inst):,} across {len(camp)} campaigns "
        f"({inst['kind'].value_counts().to_dict()})")

    tape = build_tape(inst, lo_ms, hi_ms)
    log(f"  TAPE {len(tape):,} rows over {tape['asset'].nunique()} assets")

    cov = coverage(inst, tape, camp)
    miss = int(cov.loc[cov["lane"] == "__ALL__", "missing"].iloc[0])
    if miss:
        raise SystemExit(f"HALT (F-Q-1): {miss} instants have no tape snapshot. "
                         f"A queryable book with holes is a book that lies by "
                         f"omission.")
    log(f"  COVERAGE  {len(inst):,} / {len(inst):,} instants · 0 missing")

    root.mkdir(parents=True, exist_ok=True)
    man["sha"]["campaigns"] = write_table(camp, "campaigns", ["campaign_id"], root)
    man["sha"]["instants"] = write_table(
        inst, "instants", ["campaign_id", "kind", "ts"], root)
    man["sha"]["advances"] = write_table(
        advs, "advances", ["campaign_id", "advance_seq"] if len(advs) else [], root)
    man["sha"]["harvests"] = write_table(
        harv, "harvests", ["campaign_id"] if len(harv) else [], root)
    man["sha"]["adds"] = write_table(
        addr, "adds", ["campaign_id", "add_seq"] if len(addr) else [], root)
    man["sha"]["tape_full"] = write_table(tape, "tape_full", ["asset", "ts"], root)
    man["sha"]["coverage"] = write_table(cov, "coverage", ["lane", "kind"], root)

    man["counts"] = {
        "campaigns": len(camp),
        "campaigns_card": int((camp["lane"] == "card").sum()),
        "campaigns_spring": int((camp["lane"] == "spring").sum()),
        "campaigns_add_carrying": int((camp["adds_n"] > 0).sum()),
        "instants": len(inst),
        "instants_by_kind": inst["kind"].value_counts().to_dict(),
        "tape_rows": len(tape),
        "tape_instant_labels": tape["instant"].value_counts().to_dict(),
        "spine_rows": int((tape["instant"] == "spine").sum()),
        "advances": len(advs), "harvests": len(harv), "adds": len(addr),
        "missing_instants": miss,
        "corridor_years": round(cmeta["span_days"] / 365.25, 3),
        "champion_blocks": [f"{tf}_ema{L}" for tf, L in CHAMPIONS],
        # THE WARM-UP DISCLOSURE, FILED RATHER THAN ASSUMED.
        # `engine.indicators.ema` SEEDS at the series start, so a champion
        # is emitted only from bar index >= its own length and is NULL
        # before. A 889-length daily EMA does not exist for the first 889
        # days of an asset's history, and the share of rows on which it
        # does is a number the operator should see rather than infer.
        "champion_warm_pct": {
            c.replace("champ_", "").replace("_warm", ""):
                round(100.0 * float(tape[c].mean()), 2)
            for c in tape.columns if c.endswith("_warm")},
        # THE AE CONSTANT, carried so the query tool prints a per-trade AE
        # against the book's own number rather than a literal typed twice.
        "ae_mean_r_tc_book": float(
            json.loads((TC5 / "build_manifest.json").read_text())
            ["counts"]["avg_ae_r"]),
    }
    man["elapsed_s"] = round(time.time() - t0, 1)
    (root / "build_manifest.json").write_text(
        json.dumps(man, indent=2, sort_keys=True, default=str))
    log(f"\n  manifest → {root / 'build_manifest.json'}  ({man['elapsed_s']}s)")
    return man


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rerun", action="store_true")
    a = ap.parse_args()
    run(OUT_RERUN if a.rerun else OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
