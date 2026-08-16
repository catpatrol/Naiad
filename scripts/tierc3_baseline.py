"""TIER-C3 · THE RAILED BASELINE — the seven F's enacted.

RATIFIED operator 2026-08-15 ("I rule the seven F's on your lean").  Drafted
APOLLO · Executor HEPHAESTUS · Seed 20260815.

CLASS: MEASUREMENT, NOT REGISTRATION.  m = 0.  NO lockbox read for outcomes
(the 462 sealed days stay unspent).  No estate write.  No live orders.

────────────────────────────────────────────────────────────────────────────
THIS FILE IS A FORK OF `tierc2_baseline.py`, AND THE FORK IS AN IMPORT
────────────────────────────────────────────────────────────────────────────
`import tierc2_baseline as TB` — then every unchanged part of the program is
USED, not copied: the loaders, the atomic table writer, F-KEY, the headline
aggregation, the monthly equity, and the WHOLE Amendment-B1 analytics tape
(`build_level_series`, `tape_rows`, `ribbon_state`, `tape_inventory`, the
daily spine).  A copied function can drift from its original; a bound one
cannot.  `tierc3_fixtures.F-C3-INHERIT` asserts the identities with `is`.

WHAT IS REDEFINED HERE, AND WHY — the card diffs, and nothing else:

    WINDOWS         F-7: every display-only continuity strip truncates at
                    2026-07-07T23:59Z (VR-1's forward edge).
    replay_asset    F-5: armings admitted from a window's start - 30d;
                    F-3: the 4h anchor + the 1.0-ATR rail;
                    F-4: the stop executes, adverse-first, as card text.
    funnel_table    F-5: the lead-in columns — in-window armings vs lead-in
                    armings vs scored trades, the edge bias MEASURED.
    journal/stop_geometry   the rail's own arithmetic, per trade.
    lead_in_table   NEW.  A trade whose ENTRY is in the lead-in is NOT SCORED
                    and carries NO OUTCOME COLUMN AT ALL — see §THE SEAL.
    delta_table     NEW.  v1 vs v3, per arming, side by side.

────────────────────────────────────────────────────────────────────────────
THE SEAL, AND WHY THE LEAD-IN DOES NOT BREAK IT
────────────────────────────────────────────────────────────────────────────
The scored corridor starts 2025-10-06 — the day AFTER the sealed lockbox ends
(VR-1: 2024-07-01T00:00:00Z -> 2025-10-05T23:59:59Z).  So F-5's 30-day lead-in
reaches EXACTLY 30 days into the sealed span: 2025-09-06 -> 2025-10-05.

That is disclosed, not hidden, and it is bounded by three rules enforced in
code below:

  1. An arming may be SEEN in the lead-in.  Seeing a 12/89 cross is reading
     EMA state, the same class of act as the warm-up traversal already on the
     record — LEDGER.md, the F4-a annex line: "lockbox warm-up traversal
     disclosed per cell in manifest; zero journal rows with lockbox open times".
     (CITED BY QUOTE, NOT BY LINE.  Both of this section's citations were line
     numbers until the 2026-08-15 collapse commit moved them ~50 lines, which
     is precisely the failure the estate's own "cite by section, not line"
     ruling exists to prevent.)
  2. A trade is SCORED iff its ENTRY bar lies inside the scored window.  Every
     scored ENTRY, EXIT and OUTCOME in this build is therefore computed from
     post-lockbox bars only — LEDGER.md, STANDING VERDICTS: "the seal governs
     scored outcome evidence, not raw price in a display-only trailing window".
     NOTE THE LIMIT OF THAT RULING: it licenses raw price in a DISPLAY-ONLY
     window.  A structural anchor in a SCORED window is not display — hence
     rule 5 below.
  3. A trade whose ENTRY is in the lead-in gets NO outcome: no gross R, no net
     R, no prices.  It appears ONLY in `lead_in_trades.parquet`, as the
     occupancy fact it is — because a position open across the corridor's left
     edge blocks in-window triggers, and dropping it would silently invent
     trades the rule card would not have taken.
  4. Pre-corridor timestamps are NOT confined to that one table, and saying so
     would be false: `trade_journal.arm_ms` and `delta_v1_v3.arm_ms` also reach
     into the lead-in, on rows that carry full outcomes.  What IS confined is
     the pairing — no row anywhere pairs a pre-corridor stamp in an ENTRY, EXIT
     or ANCHOR column with an outcome.  F-C3-5 enumerates every ms column of
     every filed table and states which ones reach back, rather than passing on
     a curated subset.
  5. And the anchor is a price, not a state, so the CLASS line masks the sealed
     bars out of anchor eligibility entirely — see `sealed_mask` and
     `RC.struct_stop_4h(..., forbidden=)`.  Executing the card WITHOUT that
     mask quotes the low of the sealed bar 2025-09-15T12:00Z as a scored
     trade's anchor, R denominator and exit price.  Both numbers are printed
     (`attribution_unscored`, and F-C3-a in the build document).

USAGE
    ~/venvs/naiad/bin/python scripts/tierc3_baseline.py --stage all
    ~/venvs/naiad/bin/python scripts/tierc3_baseline.py --stage all --rerun
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

# THE FORK, AS AN IMPORT.  Tier-C2's program, used rather than transcribed.
import tierc2_baseline as TB                                        # noqa: E402
import tierc3_rules as RC                                           # noqa: E402
import analytics as AN                                              # noqa: E402

# ── byte-inherited helpers, bound so the call sites read like the original ──
_ms, iso, r4, r6, pct = TB._ms, TB.iso, TB.r4, TB.r6, TB.pct
write_table, assert_key = TB.write_table, TB.assert_key
load_klines, load_funding = TB.load_klines, TB.load_funding
_idx_range = TB._idx_range
MS_4H, MS_1H, MS_1D = TB.MS_4H, TB.MS_1H, TB.MS_1D
KLINES = TB.KLINES
CENSUS_RIDE_ONLY = TB.CENSUS_RIDE_ONLY
DISPLAY_ONLY_HEADER = TB.DISPLAY_ONLY_HEADER

INHERITED_FROM_TIERC2 = (
    "_ms", "iso", "r4", "r6", "pct", "_content_sha", "_round_floats",
    "write_table", "assert_key", "load_klines", "load_funding", "_idx_range",
    "headline_rows", "monthly_equity", "_maxdd_r", "_top_decile_share",
    "strip_d_table", "daily_spine", "build_level_series", "tape_rows",
    "ribbon_state", "tape_inventory", "_daily_atr_map", "_ribbon_bands",
    "_single_wall",
)

SEED = 20260815                 # printed and unused — no stochastic step exists
OUT = ROOT / "research_outputs" / "tierc3"
OUT_RERUN = ROOT / "research_outputs" / "tierc3_run2"
V1_TABLES = ROOT / "research_outputs" / "tierc2"

log = TB.log
LOG_LINES = TB.LOG_LINES

# ── the windows, as ruled ─────────────────────────────────────────────────
# CORRIDOR [F-1/F-2]: the scored window is UNCHANGED — held identical to v1 so
# the v1<->v3 delta is a delta in the CARD and not in the corridor.
SCORED = TB.SCORED                              # 2025-10-06 -> 2026-01-31
LOCKBOX = TB.LOCKBOX                            # NOT COMPUTED — sealed
CENSUS_ERA = TB.CENSUS_ERA                      # display-only
# STRIPS [F-7]: truncated at VR-1's forward edge.
PINNING = (TB.PINNING[0], "2026-07-07")         # was -> 2026-08-11 in v1

YARDSTICK_LABEL = "YARDSTICK v3 — PROVISIONAL (one regime, n small)"

WINDOWS = {
    "SCORED":      {"span": SCORED,     "scored": True,
                    "note": "the yardstick — " + YARDSTICK_LABEL},
    "CENSUS_ERA":  {"span": CENSUS_ERA, "scored": False,
                    "note": "exploration-classic — the census-scored era"},
    "PINNING":     {"span": PINNING,    "scored": False,
                    "note": "the pinning window, TRUNCATED at VR-1's forward "
                            "edge per F-7"},
}


# ═══════════════════════════════════════════════════════ STAGE A · replay v3
def sealed_mask(open_ms: np.ndarray) -> np.ndarray:
    """True on every bar INSIDE the sealed lockbox — the mask `struct_stop_4h`
    refuses to take an anchor from.

    Not "before the corridor": *inside the seal*.  The census-era strip lives
    entirely before the lockbox opens and must keep its anchors; only bars in
    [2024-07-01, 2025-10-05] are refused, which is exactly what the CLASS line
    protects and nothing more.
    """
    lo, hi = _ms(LOCKBOX[0]), _ms(LOCKBOX[1]) + MS_1D - 1
    return (open_ms >= lo) & (open_ms <= hi)


def replay_asset(sym: str, win_name: str, k4: pd.DataFrame, k1: pd.DataFrame,
                 funding: dict[int, float], *,
                 min_stop_atr: float | None = None,
                 lead_in_days: int | None = None,
                 anchor_lens: str = "4h",
                 seal_floor: bool = True) -> tuple[list, list]:
    """The v3 rule card, ridden bar by bar.  Returns (armings, trades).

    Tier-C2's `replay_asset` with exactly three changes, each cited:

      [F-5]  armings are admitted from `span[0] - LEAD_IN_DAYS`; a trade is
             SCORED iff its ENTRY bar lies inside the window itself.  An
             unscored lead-in trade is ridden — because its position really
             does block in-window triggers — but NOTHING is accounted for it.
      [F-3]  the anchor is a 4h pivot and the distance is railed at 1.0 ATR.
      [F-4]  the stop executes, adverse-first: the ride tests the stop BEFORE
             either bell on every bar, so a bar carrying both resolves to the
             stop.  (This is Tier-C2's behaviour unchanged — F-4 makes it card
             text rather than a reading, and the fixture asserts it.)

    EMAs, ATR and the 4h pivot grid are computed over the FULL loaded history
    and only then restricted to the window, so a window edge can never move an
    indicator or an anchor.

    The four keyword arguments exist ONLY so `attribution_table` can re-ask this
    same question with one diff switched off at a time, through this one code
    path rather than a second copy.  Their defaults ARE the ratified card plus
    the CLASS line's seal floor; nothing in the shipped run passes them.
    """
    min_stop_atr = RC.MIN_STOP_ATR if min_stop_atr is None else min_stop_atr
    lead_in_days = RC.LEAD_IN_DAYS if lead_in_days is None else lead_in_days
    span = WINDOWS[win_name]["span"]
    win_lo, win_hi = _ms(span[0]), _ms(span[1]) + MS_1D - 1
    lead_lo = win_lo - lead_in_days * MS_1D

    f = RC.build_4h(k4["open_time"].to_numpy(np.int64),
                    k4["open"].to_numpy(float), k4["high"].to_numpy(float),
                    k4["low"].to_numpy(float), k4["close"].to_numpy(float))
    pv4 = RC.build_pivots_4h(k4["high"].to_numpy(float),
                             k4["low"].to_numpy(float))
    forbid4 = sealed_mask(f.open_ms) if seal_floor else None
    # the retired 1H grid, built ONLY for the attribution table's v1 cell
    pv1 = h1_open = None
    if anchor_lens == "1h":
        pv1 = RC.V1.build_pivots_1h(k1["high"].to_numpy(float),
                                    k1["low"].to_numpy(float))
        h1_open = k1["open_time"].to_numpy(np.int64)

    lead_i, hi_i = _idx_range(f.open_ms, lead_lo, win_hi)
    if hi_i < lead_i:
        return [], []

    arms = RC.armings(sym, f, lead_i, hi_i)
    trades: list[RC.Trade] = []
    open_until = -1              # 4h index the open position releases at
    x = RC._crosses(f)

    for a in arms:
        a.in_window = bool(a.arm_ms >= win_lo)          # F-5 bookkeeping
        a.entry_scored = False
        if not a.tide_ok:
            a.reject = "tide"
            continue
        if not a.d_ok:
            a.reject = "d"
            continue

        trig_flags = x["t_up"] if a.direction == 1 else x["t_dn"]
        end = min(a.window_end_i, hi_i + 1)
        cand = np.flatnonzero(trig_flags[a.arm_i:end])
        if cand.size == 0:
            a.reject = "no_trigger"
            continue
        ti = int(a.arm_i + cand[0])
        a.trigger_i, a.trigger_ms = ti, int(f.open_ms[ti])

        # ONE POSITION PER ASSET.  A trigger arriving while a position is open
        # is a real leak and is counted as one — including when the position
        # was opened by a LEAD-IN trade, which is the whole point of F-5.
        if ti <= open_until:
            a.reject = "position_open"
            continue

        entry_px = float(f.c[ti])
        atr_sig = float(f.atr[ti])
        if anchor_lens == "1h":
            # the RETIRED path, reachable only from the attribution table: the
            # Tier-C2 stop, called as Tier-C2 called it. No rail, no seal floor
            # — this cell exists to REPRODUCE v1, and a cell that improves on
            # its target is not a reproduction.
            cur1 = int(np.searchsorted(h1_open, int(f.open_ms[ti])
                                       + 3 * MS_1H, "right")) - 1
            sp = RC.V1.struct_stop(pv1, cur1, entry_px, a.direction, atr_sig)
            st = None if sp is None else RC.Stop(
                stop_px=float(sp), anchor=float(
                    sp + RC.STOP_BUF_ATR * atr_sig * a.direction),
                anchor_bar=-1, pivot_stop_px=float(sp),
                pivot_dist=abs(entry_px - float(sp)), rail_dist=0.0,
                r_dist=abs(entry_px - float(sp)), rail_binding=False,
                n_eligible=-1)
        else:
            st = RC.struct_stop_4h(pv4, ti, entry_px, a.direction, atr_sig,
                                   min_stop_atr=min_stop_atr,
                                   forbidden=forbid4)
        if st is None:
            # NAME THE REASON. "no anchor at all" and "every anchor the card
            # could reach is sealed" are different facts about the estate, and
            # the funnel counts them apart.
            a.reject = "no_struct_anchor"
            if seal_floor and anchor_lens == "4h" and RC.struct_stop_4h(
                    pv4, ti, entry_px, a.direction, atr_sig,
                    min_stop_atr=min_stop_atr, forbidden=None) is not None:
                a.reject = "anchor_sealed"
            continue
        if not (np.isfinite(st.r_dist) and st.r_dist > 0):
            a.reject = "degenerate_R"
            continue
        stop_px, r_dist = st.stop_px, st.r_dist

        a.entered = True
        a.reject = "entered"
        scored = bool(f.open_ms[ti] >= win_lo)
        a.entry_scored = scored

        # ── RIDE.  No management of any kind.  [F-4] stop first, every bar. ──
        def ride(honour_stop: bool):
            for j in range(ti + 1, hi_i + 1):
                if honour_stop:
                    if a.direction == 1 and f.l[j] <= stop_px:
                        return j, stop_px, "stop"
                    if a.direction == -1 and f.h[j] >= stop_px:
                        return j, stop_px, "stop"
                if a.direction == 1:
                    if bool(x["w_dn"][j]):
                        return j, float(f.c[j]), "bell_12_89"
                    if bool(x["b_dn"][j]):
                        return j, float(f.c[j]), "bell_89_316"
                else:
                    if bool(x["w_up"][j]):
                        return j, float(f.c[j]), "bell_12_89"
                    if bool(x["b_up"][j]):
                        return j, float(f.c[j]), "bell_89_316"
            return hi_i, float(f.c[hi_i]), "corridor_end"

        xi, xpx, xreason = ride(True)
        open_until = xi

        def account(exit_i, exit_px):
            gross = (exit_px - entry_px) * a.direction
            fee = (RC.FEE_BPS_SIDE / 10_000.0) * (entry_px + exit_px)
            fund = 0.0
            for j in range(ti + 1, exit_i + 1):
                rate = funding.get(int(f.open_ms[j]))
                if rate:                      # qty = 1 unit, on last closed px
                    fund += rate * float(f.c[j - 1]) * a.direction
            return gross / r_dist, fee / r_dist, fund / r_dist

        tr = RC.Trade(
            symbol=sym, direction=a.direction, arm_i=a.arm_i, arm_ms=a.arm_ms,
            entry_i=ti, entry_ms=int(f.open_ms[ti]),
            entry_px=entry_px if scored else float("nan"),
            stop_px=stop_px if scored else float("nan"),
            r_dist=r_dist if scored else float("nan"),
            pivot_anchor=st.anchor if scored else float("nan"),
            anchor_bar_ms=(int(f.open_ms[st.anchor_bar])
                           if st.anchor_bar >= 0 else -1),
            anchor_in_lockbox=bool(st.anchor_bar >= 0
                                   and sealed_mask(f.open_ms)[st.anchor_bar]),
            n_eligible_anchors=st.n_eligible,
            atr_at_entry=atr_sig if scored else float("nan"),
            disp_at_arming=a.disp,
            exit_i=xi, exit_ms=int(f.open_ms[xi]),
            exit_px=xpx if scored else float("nan"),
            exit_reason=xreason, bars_held=xi - ti,
            scored=scored, armed_in_lead_in=not a.in_window,
            pivot_stop_px=st.pivot_stop_px if scored else float("nan"),
            pivot_dist=st.pivot_dist if scored else float("nan"),
            rail_dist=st.rail_dist if scored else float("nan"),
            rail_binding=st.rail_binding,
        )

        # THE SEAL.  An unscored lead-in trade is ridden for occupancy and is
        # accounted for NOTHING — no gross, no net, no bell-only, no prices.
        if scored:
            bi, bpx, breason = ride(False)
            g_r, fee_r, fund_r = account(xi, xpx)
            gb_r, feeb_r, fundb_r = account(bi, bpx)
            tr.gross_r, tr.fee_r, tr.funding_r = g_r, fee_r, fund_r
            tr.net_r = g_r - fee_r - fund_r
            tr.gross_r_bellonly = gb_r
            tr.net_r_bellonly = gb_r - feeb_r - fundb_r
            tr.exit_reason_bellonly = breason
            tr.exit_ms_bellonly = int(f.open_ms[bi])
        trades.append(tr)

    return arms, trades


# ═══════════════════════════════════════════════════════ THE FUNNEL v3
def funnel_table(arms: list) -> pd.DataFrame:
    """Per stone, with the F-5 lead-in columns added.

    Cumulative by construction, as in v1: each stage is a subset of the one
    before it.  The NEW columns are the edge bias MEASURED rather than assumed:
    `armings_in_window` / `armings_lead_in` split the population, `entered`
    is split into `entered_scored` / `entered_lead_in` so the terminal column
    never pools a scored trade with an unscored one, and `leak_anchor_sealed`
    counts the tranches the CLASS line's seal floor refused.
    """
    rows = []
    for sym in RC.UNIVERSE:
        for d, dname in ((1, "long"), (-1, "short")):
            a = [x for x in arms if x.symbol == sym and x.direction == d]
            seen = len(a)
            inw = [x for x in a if x.in_window]
            lead = [x for x in a if not x.in_window]
            tide = [x for x in a if x.tide_ok]
            dd = [x for x in tide if x.d_ok]
            trig = [x for x in dd if x.trigger_i is not None]
            ent = [x for x in trig if x.entered]
            ent_s = [x for x in ent if x.entry_scored]
            rows.append({
                "asset": sym, "direction": dname,
                "armings_seen": seen,
                "armings_in_window": len(inw), "armings_lead_in": len(lead),
                "passed_tide": len(tide), "passed_d": len(dd),
                "triggered": len(trig), "entered": len(ent),
                "entered_scored": len(ent_s),
                "entered_lead_in": len(ent) - len(ent_s),
                "leak_tide": seen - len(tide),
                "leak_d": len(tide) - len(dd),
                "leak_no_trigger": len(dd) - len(trig),
                "leak_position_open": sum(1 for x in trig if x.reject == "position_open"),
                "leak_no_struct_anchor": sum(1 for x in trig if x.reject == "no_struct_anchor"),
                "leak_anchor_sealed": sum(1 for x in trig if x.reject == "anchor_sealed"),
                "leak_degenerate_R": sum(1 for x in trig if x.reject == "degenerate_R"),
            })
    return pd.DataFrame(rows)


def lead_in_census(arms: list, trades: list) -> pd.DataFrame:
    """THE F-5 TRIPLE, printed: in-window armings vs lead-in armings vs scored
    trades — and, the number the finding actually turns on, how many SCORED
    trades were ARMED in the lead-in and would not exist without the ruling."""
    inw = [a for a in arms if a.in_window]
    lead = [a for a in arms if not a.in_window]
    sc = [t for t in trades if t.scored]
    return pd.DataFrame([{
        "armings_in_window": len(inw),
        "armings_lead_in": len(lead),
        "lead_in_passed_tide_and_d": sum(1 for a in lead if a.tide_ok and a.d_ok),
        "scored_trades": len(sc),
        "scored_trades_armed_in_lead_in": sum(1 for t in sc if t.armed_in_lead_in),
        "lead_in_trades_unscored": sum(1 for t in trades if not t.scored),
        "in_window_triggers_blocked_by_open_position":
            sum(1 for a in arms if a.reject == "position_open" and a.in_window),
    }])


def lead_in_table(trades: list) -> pd.DataFrame:
    """The unscored lead-in trades — OCCUPANCY ONLY, NO OUTCOME.

    Every column here is a state fact: when the position opened, when it
    released, and why.  There is deliberately no price, no R and no net R:
    an outcome computed over a sealed bar is scored evidence wearing a label
    (LEDGER.md:865), and this is the one table in the build whose timestamps
    precede the corridor.
    """
    rows = []
    for t in trades:
        if t.scored:
            continue
        rows.append({
            "asset": t.symbol, "entry_ms": t.entry_ms,
            "entry_ts": iso(t.entry_ms),
            "direction": "long" if t.direction == 1 else "short",
            "arm_ms": t.arm_ms, "arm_ts": iso(t.arm_ms),
            "released_ms": t.exit_ms, "released_ts": iso(t.exit_ms),
            "release_reason": t.exit_reason, "bars_held": t.bars_held,
            "outcome": "NOT COMPUTED — entry bar precedes the scored corridor "
                       "(sealed lockbox); occupancy only",
        })
    return pd.DataFrame(rows)


# ═══════════════════════════════════════════════════════ the v3 record
def journal_frame(trades: list) -> pd.DataFrame:
    """Tier-C2's journal, plus the rail's arithmetic per trade."""
    rows = []
    for t in trades:
        if not t.scored:
            continue
        rows.append({
            "asset": t.symbol, "entry_ms": t.entry_ms,
            "entry_ts": iso(t.entry_ms),
            "direction": "long" if t.direction == 1 else "short",
            "arm_ms": t.arm_ms, "arm_ts": iso(t.arm_ms),
            "armed_in_lead_in": bool(t.armed_in_lead_in),
            "disp_at_arming": r6(t.disp_at_arming),
            "entry_px": r6(t.entry_px), "stop_px": r6(t.stop_px),
            "pivot_anchor": r6(t.pivot_anchor),
            # PROVENANCE OF THE ANCHOR PRICE. Without these two columns the only
            # way to learn which bar a published anchor was quoted from is to
            # rebuild the pivot grid by hand — which is how a sealed anchor
            # stays invisible to every timestamp-based era test.
            "anchor_bar_ms": int(t.anchor_bar_ms),
            "anchor_bar_ts": iso(t.anchor_bar_ms) if t.anchor_bar_ms > 0 else None,
            "anchor_in_lockbox": bool(t.anchor_in_lockbox),
            "n_eligible_anchors": int(t.n_eligible_anchors),
            "pivot_stop_px": r6(t.pivot_stop_px),
            "pivot_dist": r6(t.pivot_dist), "rail_dist": r6(t.rail_dist),
            "rail_binding": bool(t.rail_binding),
            "r_dist": r6(t.r_dist), "atr_at_entry": r6(t.atr_at_entry),
            "r_over_atr": r6(t.r_dist / t.atr_at_entry if t.atr_at_entry else None),
            "exit_ms": t.exit_ms, "exit_ts": iso(t.exit_ms),
            "exit_px": r6(t.exit_px), "exit_reason": t.exit_reason,
            "bars_held": t.bars_held,
            "gross_r": r6(t.gross_r), "fee_r": r6(t.fee_r),
            "funding_r": r6(t.funding_r), "net_r": r6(t.net_r),
            "net_r_bellonly": r6(t.net_r_bellonly),
            "exit_reason_bellonly": t.exit_reason_bellonly,
            # ── Amendment B1 · RECORDED ONLY.  Nothing reads these back. ──
            "wall_family_at_arming": None, "dist_atr_at_arming": None,
            "dist_atr_at_trigger": None, "coloc_n": None,
        })
    return pd.DataFrame(rows)


def stop_geometry(trades: list) -> pd.DataFrame:
    """R in ATR and the toll in R — with the rail's own columns beside them.

    In v1 this table's purpose was to show that R/ATR ranged 0.52 -> 2.16 and
    that the toll ate up to 19.4% of R when R was small.  In v3 it exists to
    PROVE the rail: `r_over_atr` has a floor of MIN_STOP_ATR by construction,
    `rail_binding` says which trades the rail actually moved, and
    `widening_atr` says by how much.
    """
    rows = []
    for t in trades:
        if not t.scored:
            continue
        atr = t.atr_at_entry
        rows.append({
            "asset": t.symbol, "entry_ms": t.entry_ms,
            "entry_ts": iso(t.entry_ms),
            "direction": "long" if t.direction == 1 else "short",
            "r_dist": r6(t.r_dist), "atr_at_entry": r6(atr),
            "r_over_atr": r6(t.r_dist / atr if atr else None),
            "anchor_bar_ts": iso(t.anchor_bar_ms) if t.anchor_bar_ms > 0 else None,
            "anchor_in_lockbox": bool(t.anchor_in_lockbox),
            "pivot_dist_over_atr": r6(t.pivot_dist / atr if atr else None),
            "rail_binding": bool(t.rail_binding),
            "widening_atr": r6((t.r_dist - t.pivot_dist) / atr if atr else None),
            "under_g8c_rail": bool(atr and t.r_dist < 0.5 * atr),
            "under_c3_rail": bool(atr and t.r_dist < RC.MIN_STOP_ATR * atr
                                  - 1e-12),
            "toll_share_of_r_pct": r4(100.0 * t.fee_r),
            "bars_held": t.bars_held, "exit_reason": t.exit_reason,
            "net_r": r6(t.net_r), "net_r_bellonly": r6(t.net_r_bellonly),
            "stop_cost_r": r6(t.net_r_bellonly - t.net_r),
        })
    return pd.DataFrame(rows)


# ═══════════════════════════════════════════════ THE DELTA TABLE · v1 vs v3
def delta_table(trades: list) -> pd.DataFrame:
    """v1 vs v3, PER ARMING, side by side.

    The join key is the arming itself — `(asset, direction, arm_ms)` — and the
    join is OUTER, because the two card versions do not agree on which armings
    become trades: the rail changes where stops fire, which changes when the
    one-position-per-asset slot frees, which changes what can enter next.  A
    row present on one side only is the finding, not an error, so it is kept
    and labelled rather than dropped.

    v1's side is read from the FILED Tier-C2 table
    (`research_outputs/tierc2/trade_journal.parquet`), never recomputed: this
    build must not be able to move v1's number while comparing itself to it.
    """
    p = V1_TABLES / "trade_journal.parquet"
    if not p.exists():
        raise SystemExit(f"HALT: v1 journal absent at {p} — the DELTA TABLE is "
                         f"a deliverable and may not be faked. Re-run "
                         f"scripts/tierc2_baseline.py --stage all first.")
    v1 = pd.read_parquet(p)
    v1 = v1.assign(r_over_atr=v1["r_dist"] / v1["atr_at_entry"])
    keep = ["asset", "direction", "arm_ms", "arm_ts", "r_over_atr", "entry_ts",
            "entry_px", "stop_px", "exit_ts", "exit_reason", "net_r",
            "net_r_bellonly"]
    v1 = v1[keep].add_prefix("v1_").rename(
        columns={"v1_asset": "asset", "v1_direction": "direction",
                 "v1_arm_ms": "arm_ms"})

    v3 = journal_frame(trades)
    if len(v3):
        v3 = v3[["asset", "direction", "arm_ms", "arm_ts", "r_over_atr",
                 "entry_ts", "entry_px", "stop_px", "exit_ts", "exit_reason",
                 "net_r", "net_r_bellonly", "rail_binding",
                 "armed_in_lead_in"]].add_prefix("v3_").rename(
            columns={"v3_asset": "asset", "v3_direction": "direction",
                     "v3_arm_ms": "arm_ms"})
    else:
        v3 = pd.DataFrame(columns=["asset", "direction", "arm_ms"])

    assert_key(v1, ["asset", "direction", "arm_ms"], "delta.v1")
    assert_key(v3, ["asset", "direction", "arm_ms"], "delta.v3")
    d = v1.merge(v3, on=["asset", "direction", "arm_ms"], how="outer",
                 indicator=True, validate="1:1")
    d["present"] = d["_merge"].map({"both": "both", "left_only": "v1_only",
                                    "right_only": "v3_only"})
    d = d.drop(columns=["_merge"])
    d["arm_ts"] = d["arm_ms"].map(lambda m: iso(int(m)))
    d["delta_net_r"] = [
        None if (pd.isna(a) or pd.isna(b)) else r6(float(b) - float(a))
        for a, b in zip(d["v1_net_r"], d["v3_net_r"])]
    d["delta_r_over_atr"] = [
        None if (pd.isna(a) or pd.isna(b)) else r6(float(b) - float(a))
        for a, b in zip(d["v1_r_over_atr"], d["v3_r_over_atr"])]

    # THE FLAGGED ROW.  v1's F-3 finding is one specific arming — the tightest
    # R in the v1 book, ETHUSDT 2025-10-29, R = 0.52 ATR.  It is identified by
    # ARITHMETIC (the minimum v1 r_over_atr), then ASSERTED to be that arming,
    # so the flag cannot quietly land on a different row in a re-run.
    d["flag"] = ""
    have_v1 = d[d["v1_r_over_atr"].notna()]
    if len(have_v1):
        k = have_v1["v1_r_over_atr"].astype(float).idxmin()
        row = d.loc[k]
        expect = ("ETHUSDT", "short", "2025-10-29T16:00:00Z")
        got = (row["asset"], row["direction"], iso(int(row["arm_ms"])))
        if got != expect:
            raise SystemExit(
                f"HALT: the F-3 row moved. The tightest v1 R is {got} "
                f"(R/ATR={row['v1_r_over_atr']:.4f}), expected {expect}. The "
                f"delta table's flag is pinned to the finding it explains.")
        d.loc[k, "flag"] = ("F-3 ROW — v1 R = 0.52 ATR, the trade that carried "
                            "89.5% of v1's bell-only gap")
    for c in ("v1_r_over_atr", "v1_net_r", "v1_net_r_bellonly", "v1_entry_px",
              "v1_stop_px"):
        d[c] = d[c].map(r6)
    return d


def attribution_table() -> pd.DataFrame:
    """UNSCORED ATTRIBUTION — which card diff actually moved the number.

    The build is *named* for the rail.  Before that name is allowed to stand,
    the diffs are switched off one at a time and the corridor re-ridden, so the
    credit lands where the arithmetic puts it rather than where the title does.

    Five cells, each the SAME `replay_asset` with different keywords — one code
    path, not five copies:

        V1   1H anchor, no rail, no lead-in, no seal floor   -> must REPRODUCE
                                                                Tier-C2's filed
                                                                net R exactly
        D    4h anchor, no rail, no lead-in
        C    4h anchor, RAIL,    no lead-in
        B    4h anchor, no rail, LEAD-IN
        A    4h anchor, RAIL,    LEAD-IN     = THE SHIPPED CARD

    THIS IS NOT A SWEEP AND NOTHING HERE IS SCORED.  A sweep searches a space
    for the best cell and then reports it; this decomposes ONE ratified result
    into the contributions of its OWN ratified parts, every cell printed, the
    ratified one already chosen before the table existed.  Same class as the
    bell-only counterfactual: printed because the ambiguity is real, scored
    never.  m = 0 is unaffected — no cell may be promoted, and picking one out
    of this table on its R is a new probe that declares its own m first.
    """
    cells = [
        ("V1", "1h", 0.0, 0, False, "Tier-C2's card, re-ridden here"),
        ("D", "4h", 0.0, 0, True, "F-3 anchor lens only"),
        ("C", "4h", RC.MIN_STOP_ATR, 0, True, "F-3 anchor + rail"),
        ("B", "4h", 0.0, RC.LEAD_IN_DAYS, True, "F-3 anchor + F-5 lead-in"),
        ("A", "4h", RC.MIN_STOP_ATR, RC.LEAD_IN_DAYS, True, "THE SHIPPED CARD"),
        ("A0", "4h", RC.MIN_STOP_ATR, RC.LEAD_IN_DAYS, False,
         "the card LITERALLY — no seal floor; F-C3-a"),
    ]
    rows = []
    for cell, lens, rail, lead, floor in [(c[0], c[1], c[2], c[3], c[4]) for c in cells]:
        note = [c[5] for c in cells if c[0] == cell][0]
        ts: list = []
        for sym in RC.UNIVERSE:
            k4, k1 = load_klines(sym, "4h"), load_klines(sym, "1h")
            _, t = replay_asset(sym, "SCORED", k4, k1, load_funding(sym),
                                min_stop_atr=rail, lead_in_days=lead,
                                anchor_lens=lens, seal_floor=floor)
            ts += [x for x in t if x.scored]
        rs = [x.net_r for x in ts]
        rows.append({
            "cell": cell, "anchor_lens": lens,
            "rail_atr": rail, "lead_in_days": lead, "seal_floor": floor,
            "n": len(ts), "net_r": r4(sum(rs)) if rs else None,
            "expectancy_r": r4(float(np.mean(rs))) if rs else None,
            "win_rate_pct": pct(sum(1 for v in rs if v > 0), len(rs)),
            "note": note,
        })
    d = pd.DataFrame(rows)
    # the marginal contributions, as differences between named cells
    g = {r["cell"]: r["net_r"] for _, r in d.iterrows()}
    d["marginal_vs"] = ["", "V1", "D", "D", "B", "A"]
    d["marginal_net_r"] = [None,
                           r4(g["D"] - g["V1"]), r4(g["C"] - g["D"]),
                           r4(g["B"] - g["D"]), r4(g["A"] - g["B"]),
                           r4(g["A0"] - g["A"])]
    return d


def anchor_lookback_disclosure(trades: list) -> pd.DataFrame:
    """DISCLOSURE, UNSCORED — the interpretive fork in the lookback, counted.

    Tier-C2's lookback was 200 bars in the 1h lens, which is 200 HOURS.  F-3
    moved the anchor to the 4h lens and said nothing about the lookback, so the
    inherited constant admits two readings: 200 BARS-IN-LENS (byte-inherited,
    TAKEN) or 200 hours = 50 4h bars (the time-equivalent, NOT TAKEN).

    Per scored trade, this asks whether the two readings name the SAME anchor.
    COUNTS ONLY — no R is attached to either reading. A swept parameter with an
    outcome beside it is a selection surface, and this build is m = 0.
    """
    rows = []
    for sym in RC.UNIVERSE:
        ts = [t for t in trades if t.symbol == sym and t.scored]
        if not ts:
            continue
        k4 = load_klines(sym, "4h")
        pv4 = RC.build_pivots_4h(k4["high"].to_numpy(float),
                                 k4["low"].to_numpy(float))
        for t in ts:
            alt = RC.struct_stop_4h(pv4, t.entry_i, t.entry_px, t.direction,
                                    t.atr_at_entry,
                                    lookback=RC.PIVOT_LOOKBACK_4H_TIME_EQUIV)
            same_anchor = bool(alt is not None
                               and abs(alt.anchor - t.pivot_anchor) < 1e-9)
            rows.append({
                "asset": sym, "entry_ms": t.entry_ms,
                "entry_ts": iso(t.entry_ms),
                "lookback_taken_bars": RC.PIVOT_LOOKBACK_4H,
                "lookback_time_equiv_bars": RC.PIVOT_LOOKBACK_4H_TIME_EQUIV,
                "anchor_taken": r6(t.pivot_anchor),
                "anchor_time_equiv": r6(alt.anchor) if alt else None,
                "time_equiv_has_anchor": bool(alt is not None),
                "same_anchor": same_anchor,
                "same_stop": bool(alt is not None
                                  and abs(alt.stop_px - t.stop_px) < 1e-9),
            })
    return pd.DataFrame(rows)


# ═══════════════════════════════════════════════════════════════ the driver
def run(root: Path, do_tape: bool = True) -> dict:
    t0 = time.time()
    man: dict = {"seed": SEED, "windows": {}, "sha": {}, "counts": {},
                 "card": "TIER-C3 · THE RAILED BASELINE",
                 "yardstick_label": YARDSTICK_LABEL}

    log("=" * 78)
    log("TIER-C3 · THE RAILED BASELINE — the seven F's enacted")
    log("=" * 78)
    log(f"  analytics {AN.ANALYTICS_VERSION}  sha {AN.analytics_sha()[:16]}…")
    log(f"  seed {SEED} · universe {', '.join(RC.UNIVERSE)} · lens {RC.LENS}")
    log(f"  klines {KLINES}")
    log(f"  CARD DIFFS: anchor=4h ({RC.PIVOT_L},{RC.PIVOT_R}) pivots, lookback "
        f"{RC.PIVOT_LOOKBACK_4H} bars · RAIL min {RC.MIN_STOP_ATR} x ATR_4h · "
        f"lead-in {RC.LEAD_IN_DAYS}d · strips truncate "
        f"{RC.REGISTER['STRIP_TRUNCATE']['value']}")
    log("")
    log("  WINDOWS")
    for n, w in WINDOWS.items():
        lead = _ms(w["span"][0]) - RC.LEAD_IN_DAYS * MS_1D
        log(f"    {n:12} {w['span'][0]} -> {w['span'][1]}   "
            f"{'SCORED' if w['scored'] else 'DISPLAY-ONLY'}  "
            f"(armings from {iso(lead)[:10]}; {w['note']})")
    # THE OVERLAP DISCLOSURE, MEASURED AGAINST WHAT THIS BUILD ACTUALLY READS.
    # Handing `lockbox_overlap` the lockbox's own bounds (as v1 did) can only
    # ever return 462 days and measures nothing. The span this build reads for
    # armings is scored_start - 30d -> scored_end, and its overlap with the seal
    # is the F-5 fact itself.
    read_lo = _ms(SCORED[0]) - RC.LEAD_IN_DAYS * MS_1D
    lo = AN.lockbox_overlap(read_lo, _ms(SCORED[1]) + MS_1D - 1)
    log(f"    {'LOCKBOX':12} {LOCKBOX[0]} -> {LOCKBOX[1]}   NOT COMPUTED (sealed)")
    log(f"    {'':12} the span this build READS for armings, "
        f"{iso(read_lo)[:10]} -> {SCORED[1]}, overlaps the seal by "
        f"{lo['overlap_days']:.3f} d  [F-5, disclosed]")
    log(f"    {'':12} SEAL FLOOR ON ANCHORS: {RC.SEAL_FLOOR_ON_ANCHOR} — no "
        f"pivot on a sealed bar may be an anchor (CLASS line, not a card diff)")
    log("")

    all_arms: dict[str, list] = {}
    all_trades: dict[str, list] = {}
    tape_frames: list[pd.DataFrame] = []

    for win_name in WINDOWS:
        span = WINDOWS[win_name]["span"]
        win_lo, win_hi = _ms(span[0]), _ms(span[1]) + MS_1D - 1
        log(f"  ── {win_name} {span[0]} -> {span[1]} "
            f"{'(SCORED)' if WINDOWS[win_name]['scored'] else '(DISPLAY-ONLY)'}")
        arms_w, trades_w = [], []
        for sym in RC.UNIVERSE:
            k4, k1 = load_klines(sym, "4h"), load_klines(sym, "1h")
            fund = load_funding(sym)
            a, t = replay_asset(sym, win_name, k4, k1, fund)
            arms_w += a
            trades_w += t
            sc = sum(1 for x in t if x.scored)
            log(f"    {sym:9} armings={len(a):5d} "
                f"(in-window {sum(1 for x in a if x.in_window):5d} / lead-in "
                f"{sum(1 for x in a if not x.in_window):3d})  "
                f"trades={sc:4d} (+{len(t) - sc} unscored lead-in)")

            if do_tape and WINDOWS[win_name]["scored"]:
                # THE SEAL: no tape instant precedes the corridor.  A trade
                # armed in the lead-in therefore has NULL arming-instant tape
                # columns, by construction — disclosed, never back-filled.
                inst: list[tuple[int, str]] = []
                for xa in a:
                    if xa.arm_ms >= win_lo:
                        inst.append((xa.arm_ms, "arming"))
                    if xa.trigger_ms is not None and xa.trigger_ms >= win_lo:
                        inst.append((xa.trigger_ms, "trigger"))
                for tr in t:
                    if tr.scored:
                        inst.append((tr.exit_ms, "exit"))
                for dsp in TB.daily_spine(k4, win_lo, win_hi):
                    inst.append((dsp, "spine"))
                order = {"arming": 0, "trigger": 1, "exit": 2, "spine": 3}
                seen: dict[int, str] = {}
                for ts, kind in sorted(inst, key=lambda p: (p[0], order[p[1]])):
                    seen.setdefault(int(ts), kind)
                tp = TB.tape_rows(sym, k4, k1, sorted(seen.items()), win_name)
                if len(tp):
                    rs = TB.ribbon_state(sym)
                    if len(rs):
                        assert_key(rs, ["ts"], f"ribbon_state[{sym}]")
                        tp = tp.merge(rs, on="ts", how="left", validate="1:1")
                    tape_frames.append(tp)
        all_arms[win_name] = arms_w
        all_trades[win_name] = trades_w
        man["windows"][win_name] = {
            "span": list(span), "scored": WINDOWS[win_name]["scored"],
            "lead_in_from": iso(_ms(span[0]) - RC.LEAD_IN_DAYS * MS_1D)[:10],
            "armings": len(arms_w),
            "armings_in_window": sum(1 for x in arms_w if x.in_window),
            "armings_lead_in": sum(1 for x in arms_w if not x.in_window),
            "trades_scored": sum(1 for x in trades_w if x.scored),
            "trades_lead_in_unscored": sum(1 for x in trades_w if not x.scored)}
        # per-window TRADE TIME BOUNDS — so F-C3-5 can prove the F-7 truncation
        # on the display strips too, not only on the scored tables.
        sc_w = [x for x in trades_w if x.scored]
        if sc_w:
            man["windows"][win_name]["trade_ts_bounds"] = {
                "min_entry": iso(min(x.entry_ms for x in sc_w)),
                "max_entry": iso(max(x.entry_ms for x in sc_w)),
                "min_exit": iso(min(x.exit_ms for x in sc_w)),
                "max_exit": iso(max(x.exit_ms for x in sc_w)),
                "max_exit_ms": int(max(x.exit_ms for x in sc_w))}
        log("")

    # ── tables ────────────────────────────────────────────────────────────
    log("  ── TABLES")
    scored_arms = all_arms["SCORED"]
    all_scored_win_trades = all_trades["SCORED"]
    scored_trades = [t for t in all_scored_win_trades if t.scored]

    man["sha"]["funnel"] = write_table(funnel_table(scored_arms), "funnel",
                                       ["asset", "direction"], root)
    man["sha"]["lead_in_census"] = write_table(
        lead_in_census(scored_arms, all_scored_win_trades), "lead_in_census",
        [], root)
    li = lead_in_table(all_scored_win_trades)
    man["sha"]["lead_in_trades"] = write_table(
        li, "lead_in_trades", ["asset", "entry_ms"] if len(li) else [], root)

    # the d-strip, UNSCORED — printed over BOTH populations so the lead-in
    # cannot silently change a number that v1 also reported.
    sd = []
    for pop, subset in (("in_window", [a for a in scored_arms if a.in_window]),
                        ("in_window+lead_in", scored_arms)):
        s = TB.strip_d_table(subset)
        s.insert(0, "population", pop)
        sd.append(s)
    man["sha"]["strip_d"] = write_table(pd.concat(sd, ignore_index=True),
                                        "strip_d_unscored",
                                        ["population", "d"], root)

    head = pd.concat([TB.headline_rows(scored_trades, g)
                      for g in ("ALL", "asset", "direction", "exit_reason")],
                     ignore_index=True)
    head.insert(0, "label", YARDSTICK_LABEL)
    man["sha"]["headline"] = write_table(head, "headline",
                                         ["group", "key"], root)
    man["sha"]["monthly"] = write_table(TB.monthly_equity(scored_trades),
                                        "monthly_equity", ["month"], root)
    sg = stop_geometry(scored_trades)
    man["sha"]["stop_geometry"] = write_table(
        sg, "stop_geometry", ["asset", "entry_ms"] if len(sg) else [], root)
    dl = delta_table(scored_trades)
    man["sha"]["delta"] = write_table(
        dl, "delta_v1_v3", ["asset", "direction", "arm_ms"] if len(dl) else [],
        root)
    at = attribution_table()
    man["sha"]["attribution"] = write_table(at, "attribution_unscored",
                                            ["cell"], root)
    al = anchor_lookback_disclosure(scored_trades)
    man["sha"]["anchor_lookback"] = write_table(
        al, "anchor_lookback_disclosure",
        ["asset", "entry_ms"] if len(al) else [], root)
    if len(al):
        man["counts"]["anchor_same_under_time_equiv_lookback"] = int(
            al["same_anchor"].sum())
        man["counts"]["anchor_rows"] = len(al)

    jr = journal_frame(scored_trades)
    if len(jr):
        tp = pd.concat(tape_frames, ignore_index=True) if tape_frames else pd.DataFrame()
        if len(tp):
            am = tp.set_index(["asset", "ts"])
            for i, row in jr.iterrows():
                ka, kt = (row["asset"], row["arm_ms"]), (row["asset"], row["entry_ms"])
                if ka in am.index:
                    jr.at[i, "wall_family_at_arming"] = am.loc[ka, "wall_family"]
                    jr.at[i, "dist_atr_at_arming"] = am.loc[ka, "nearest_dist_atr"]
                    jr.at[i, "coloc_n"] = am.loc[ka, "coloc_n"]
                if kt in am.index:
                    jr.at[i, "dist_atr_at_trigger"] = am.loc[kt, "nearest_dist_atr"]
    man["sha"]["journal"] = write_table(jr, "trade_journal",
                                        ["asset", "entry_ms"] if len(jr) else [],
                                        root)

    # display-only strips — outcomes, clearly headed, F-7 truncated
    ds = []
    for win_name in ("CENSUS_ERA", "PINNING"):
        h = TB.headline_rows([t for t in all_trades[win_name] if t.scored], "ALL")
        h["window"] = win_name
        h["span"] = f"{WINDOWS[win_name]['span'][0]} -> {WINDOWS[win_name]['span'][1]}"
        h["class"] = DISPLAY_ONLY_HEADER
        ds.append(h)
    man["sha"]["display_only"] = write_table(pd.concat(ds, ignore_index=True),
                                             "display_only_strips",
                                             ["window", "group", "key"], root)

    if tape_frames:
        tape = pd.concat(tape_frames, ignore_index=True)
        man["sha"]["tape"] = write_table(tape, "analytics_tape",
                                         ["asset", "ts"], root)
        man["counts"]["tape_rows"] = len(tape)
        man["counts"]["tape_instants"] = tape["instant"].value_counts().to_dict()
        man["sha"]["tape_inventory"] = write_table(
            TB.tape_inventory(tape), "tape_inventory", ["instant", "column"],
            root)

    man["counts"]["scored_trades"] = len(scored_trades)
    man["counts"]["scored_armings"] = sum(1 for a in scored_arms if a.in_window)
    man["counts"]["lead_in_armings"] = sum(1 for a in scored_arms if not a.in_window)
    man["counts"]["lead_in_trades_unscored"] = sum(
        1 for t in all_scored_win_trades if not t.scored)
    man["counts"]["scored_trades_armed_in_lead_in"] = sum(
        1 for t in scored_trades if t.armed_in_lead_in)
    man["counts"]["rail_binding"] = sum(1 for t in scored_trades if t.rail_binding)
    man["counts"]["anchors_in_lockbox"] = sum(
        1 for t in scored_trades if t.anchor_in_lockbox)
    man["counts"]["armings_refused_anchor_sealed"] = sum(
        1 for a in scored_arms if a.reject == "anchor_sealed")
    man["seal_floor_on_anchor"] = bool(RC.SEAL_FLOOR_ON_ANCHOR)
    man["elapsed_s"] = round(time.time() - t0, 1)

    root.mkdir(parents=True, exist_ok=True)
    (root / "build_manifest.json").write_text(
        json.dumps(man, indent=2, sort_keys=True, default=str))
    log(f"\n  manifest → {root / 'build_manifest.json'}   ({man['elapsed_s']}s)")
    return man


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", default="all", choices=["all", "replay", "tape"])
    ap.add_argument("--rerun", action="store_true",
                    help="write to research_outputs/tierc3_run2 (F-C3-4)")
    a = ap.parse_args()
    root = OUT_RERUN if a.rerun else OUT
    run(root, do_tape=(a.stage in ("all", "tape")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
