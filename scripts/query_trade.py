"""TIER-C5-Q · STAGE Q2 — THE QUERY TOOL.

RATIFIED operator 2026-08-16: *"instantly queryable for every trade"*.

    python scripts/query_trade.py ETHUSDT:card:20251029T1600
    python scripts/query_trade.py --day 2025-10-29
    python scripts/query_trade.py --random 5
    python scripts/query_trade.py --list ETHUSDT          # ids for one asset

**INSTANTLY MEANS INSTANTLY.**  This tool COMPUTES NOTHING.  Every number it
prints was written by `scripts/tierc5q.py` into `research_outputs/tierc5q/`, and
the tool's whole job is to join seven parquet tables and lay them out on one
screen.  F-Q-4 asserts the budget of 2 s per query and the measured cost is an
order below it; the moment this file starts deriving something, that stops being
true and the derivation belongs upstream.

**AND IT IS DETERMINISTIC.**  `--random` is SEEDED (`--seed`, default 20260816):
a spot-audit that cannot be reproduced is an anecdote, and the estate does not
keep anecdotes.  F-Q-3 runs the tool twice and hashes both outputs.

WHAT ONE SCREEN CARRIES, and why each block is on it:
    IDENTITY        who, which mandate, what it made — plus D15 rendered PER
                    CAMPAIGN and labelled as such (the fleet's D15 columns
                    compare two BOOKS and cannot be reprinted on a row)
    FUNNEL STAMPS   displacement at the arming, the tide state, the window age
                    — the three numbers that decide whether the trade existed
    WALL CONTEXT    at EVERY instant: nearest level per family with a SIGNED
                    ATR distance, the single-wall stamp, the co-location count,
                    and the four league champions each on its own clock
    RIBBONS         the six-ribbon state at each instant, where the estate holds
                    one
    THE AE PATH     how far this campaign went against you before +1R, against
                    the book's own constant
    TRAIL LEDGER    every advance, what bound it, and which one was paid out
    HARVEST         took / would-have / delta — the H1 question, per trade
    SEAL PROVENANCE whether this campaign quotes a price the previous three
                    builds could not have read
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
Q = ROOT / "research_outputs" / "tierc5q"

FAMILIES = ("avwap", "rvwap", "prior_extreme")
CHAMPS = ("1h_ema4618", "4h_ema3618", "12h_ema889", "1d_ema889")
KIND_ORDER = {"sweep": 0, "arming": 1, "trigger": 2, "add": 3, "advance": 4,
              "harvest": 5, "exit": 6, "spine": 7}


def _load() -> dict:
    if not (Q / "campaigns.parquet").exists():
        raise SystemExit(
            f"HALT: {Q} is not built. Run:\n"
            f"    ~/venvs/naiad/bin/python scripts/tierc5q.py")
    d = {n: pd.read_parquet(Q / f"{n}.parquet")
         for n in ("campaigns", "instants", "advances", "harvests", "adds")}
    d["tape"] = pd.read_parquet(Q / "tape_full.parquet")
    d["man"] = json.loads((Q / "build_manifest.json").read_text())
    return d


def _f(v, nd=6, dash="—"):
    if v is None or (isinstance(v, float) and not np.isfinite(v)):
        return dash
    if isinstance(v, (int, np.integer)):
        return str(int(v))
    return f"{float(v):.{nd}f}"


def _sig(v, nd=3):
    """Signed, for a distance where the sign is the information."""
    if v is None or (isinstance(v, float) and not np.isfinite(v)):
        return "   —  "
    return f"{float(v):+.{nd}f}"


def _rule(t: str = "", w: int = 96) -> str:
    if not t:
        return "─" * w
    return f"── {t} " + "─" * max(0, w - len(t) - 4)


# ═══════════════════════════════════════════════════════════ the one screen
def render(cid: str, D: dict) -> list[str]:
    camp = D["campaigns"]
    row = camp[camp["campaign_id"] == cid]
    if not len(row):
        near = [c for c in camp["campaign_id"] if cid.upper() in c.upper()][:8]
        raise SystemExit(f"HALT: no campaign '{cid}'."
                         + (f" Did you mean:\n  " + "\n  ".join(near) if near
                            else "  Try --list <ASSET>."))
    r = row.iloc[0]
    out: list[str] = []
    A = out.append

    A("=" * 96)
    A(f"  {cid}")
    A("=" * 96)

    # ── IDENTITY ──────────────────────────────────────────────────────────
    A(_rule("IDENTITY"))
    A(f"  asset        {r['asset']:<10} direction {r['direction']:<6} "
      f"lane {r['lane']}")
    A(f"  mandate      {r['mandate']}")
    A(f"  armed        {r['arm_ts']}   displacement {_f(r['disp_at_arming'],4)} "
      f"ATR   window age {int(r['window_age_bars'])} bars")
    A(f"  ENTRY        {r['entry_ts']}   px {_f(r['entry_px'])}   "
      f"stop {_f(r['stop_px'])}")
    A(f"  R            {_f(r['r_dist'])}  = {_f(r['r_over_atr'],4)} x ATR "
      f"({_f(r['atr_at_entry'])})")
    A(f"  EXIT         {r['exit_ts']}   px {_f(r['exit_px'])}   "
      f"reason {r['exit_reason']}   held {int(r['bars_held'])} bars")
    A(f"  NET R        {_sig(r['net_r'],6)}"
      f"    = gross {_sig(r['gross_r'],6)} − fee {_f(r['fee_r'])} "
      f"− funding {_sig(r['funding_r'],6)}")
    if bool(r["funding_ceiling_bound"]):
        A(f"               *** D12 FUNDING CEILING BOUND *** uncapped was "
          f"{_sig(r['funding_r_uncapped'],6)}")
    A(f"  MFE          {_sig(r['mfe_r'],4)} R          "
      f"give-back from peak {_sig(float(r['mfe_r']) - float(r['net_r']),4)} R")
    A("")
    A("  D15 (PER CAMPAIGN — the fleet's D15 columns compare two BOOKS and")
    A("       cannot be reprinted on a row; these are the same questions asked")
    A("       of one campaign)")
    A(f"    share of its lane's net R      {_sig(r['share_of_lane_net_r'],6)}"
      f"   (lane total {_f(r['lane_net_r'],4)} R)")
    A(f"    in its lane's top decile       {bool(r['in_lane_top_decile'])}")
    A(f"    slice {r['slice_year']} flagged PROVISIONAL  "
      f"{bool(r['slice_provisional'])}")
    if int(r["adds_n"]) > 0:
        A(f"    adds delta vs card             "
          f"{_sig(r['adds_delta_vs_card'],6)} R over {int(r['adds_n'])} add(s)"
          f"   — the one genuinely PAIRED delta a campaign owns")

    # ── SEAL PROVENANCE ───────────────────────────────────────────────────
    A("")
    A(_rule("SEAL PROVENANCE"))
    adv = D["advances"]
    ma = adv[adv["campaign_id"] == cid]
    lb0, lb1 = "2024-07-01", "2025-10-05T23:59:59Z"
    piv_sealed = ma[(ma["pivot_bar_ts"] >= lb0) & (ma["pivot_bar_ts"] <= lb1)]
    A(f"  entry anchor          {_f(r['anchor'])}  from bar "
      f"{r['anchor_bar_ts'] or '—'}"
      + ("   *** FORMERLY SEALED ***" if bool(r["anchor_was_sealed"]) else ""))
    if len(ma):
        A(f"  ratchet pivots        {len(ma)} advance(s), "
          f"{len(piv_sealed)} quoting a FORMERLY SEALED bar"
          + ("   *** and one of them paid out ***"
             if len(piv_sealed[piv_sealed["paid_out"]]) else ""))
    if not bool(r["anchor_was_sealed"]) and not len(piv_sealed):
        A("  → this campaign quotes no price from the old lockbox; Tier-C2, C3")
        A("    and C4 could have taken it unchanged.")
    else:
        A("  → this campaign COULD NOT HAVE EXISTED as scored before the")
        A("    2026-08-16 seal-open ruling.")

    # ── SPRING (lane-specific) ────────────────────────────────────────────
    if r["lane"] == "spring":
        A("")
        A(_rule("THE SPRING"))
        A(f"  swept the prior 96-bar level  {_f(r['spring_swept_level'])}")
        A(f"  sweep printed                 {_f(r['spring_sweep_extreme'])}  "
          f"at {r['spring_sweep_ts']}")
        A(f"  reclaimed                     {int(r['spring_bars_to_reclaim'])} "
          f"bar(s) later, at the entry close")

    # ── THE AE PATH ───────────────────────────────────────────────────────
    A("")
    A(_rule("THE AE PATH TO +1R"))
    const = D["man"]["counts"]["ae_mean_r_tc_book"]
    if bool(r["reached_1r"]):
        ae = -float(r["mae_to_1r_r"])
        A(f"  reached +1R.  deepest adverse first: {ae:.6f} R")
        A(f"  the book's constant (TC-BOOK winners): {const:.6f} R"
          f"   → this campaign ran {ae/const:.2f}x the mean")
    else:
        A(f"  NEVER reached +1R — so it has no AE and is not in the constant.")
        A(f"  the book's constant (TC-BOOK winners): {const:.6f} R")
        A(f"  (winners that never reach +1R are counted apart, never imputed)")

    # ── TRAIL LEDGER ──────────────────────────────────────────────────────
    A("")
    A(_rule("TRAIL LEDGER"))
    if not len(ma):
        A("  no advance — the campaign resolved on its entry stop.")
    else:
        A(f"  {'#':>2} {'confirmed':21} {'governs from':21} {'pivot':>12} "
          f"{'new stop':>12} {'Δ ATR':>7}  bound  paid")
        for _, a in ma.sort_values("advance_seq").iterrows():
            A(f"  {int(a['advance_seq']):>2} {a['conf_ts']:21} "
              f"{a['governs_from_ts']:21} {_f(a['pivot_val'],4):>12} "
              f"{_f(a['new_stop_px'],4):>12} {_f(a['advance_atr'],3):>7}  "
              f"{a['binding_side']:<6} {'YES' if a['paid_out'] else '.'}")
        A(f"  stop travelled {_f(r['stop_advanced_atr'],4)} ATR in total; "
          f"exit on an advanced stop: {bool(r['ratchet_exit'])}")

    # ── HARVEST ───────────────────────────────────────────────────────────
    A("")
    A(_rule("HARVEST (H1)"))
    hv = D["harvests"]
    mh = hv[hv["campaign_id"] == cid]
    if not len(mh):
        A("  no harvest — the band was never touched from outside, or the "
          "touch fell on the exit bar.")
    else:
        h = mh.iloc[0]
        A(f"  fired {h['harvest_ts']}  (+{int(h['bars_after_entry'])} bars)  "
          f"fill {_f(h['fill_px'])}  unit move "
          f"{_sig(h['unit_move_at_harvest_r'],4)} R")
        A(f"  TOOK {_sig(h['took_r'],6)} R    WOULD-HAVE "
          f"{_sig(h['would_have_r'],6)} R    DELTA {_sig(h['delta_r'],6)} R"
          f"   → {'HELPED' if bool(h['helped']) else 'HURT'}")
        A(f"  runner half {_sig(h['runner_half_r'],6)} R")

    # ── ADDS ──────────────────────────────────────────────────────────────
    ad = D["adds"]
    mad = ad[ad["campaign_id"] == cid]
    if len(mad):
        A("")
        A(_rule("CASCADE ADDS (P-CASC-1)"))
        for _, a in mad.sort_values("add_seq").iterrows():
            A(f"  #{int(a['add_seq'])}  {a['add_ts']}  px {_f(a['add_px'],4)}  "
              f"size {a['size']}x  (+{int(a['bars_after_entry'])} bars)  "
              f"unit move at add {_sig(a['unit_move_at_add_r'],4)} R  "
              f"retrace {a['retrace_ts']}")

    # ── WALL CONTEXT AT EVERY INSTANT ─────────────────────────────────────
    A("")
    A(_rule("WALL CONTEXT AT EVERY INSTANT"))
    inst = D["instants"]
    mi = inst[inst["campaign_id"] == cid].copy()
    mi["ord"] = mi["kind"].map(lambda k: KIND_ORDER.get(k, 9))
    mi = mi.sort_values(["ts", "ord"])
    tp = D["tape"].set_index(["asset", "ts"])
    A(f"  {'instant':21} {'kind':9} {'close':>12} {'tide':5} "
      f"{'wall':>6} {'wallΔ':>7} {'coloc':>5} "
      + " ".join(f"{f[:6]:>7}" for f in FAMILIES) + "   nearest")
    for _, i_ in mi.iterrows():
        key = (i_["asset"], int(i_["ts"]))
        if key not in tp.index:
            A(f"  {i_['ts_iso']:21} {i_['kind']:9}   *** NO TAPE ROW ***")
            continue
        t = tp.loc[key]
        fam = " ".join(_sig(t.get(f"{f}_dist_atr"), 3).rjust(7) for f in FAMILIES)
        A(f"  {i_['ts_iso']:21} {i_['kind']:9} {_f(t['close'],4):>12} "
          f"{str(t['tide_state']):5} {str(t['wall_family']):>6} "
          f"{_sig(t['wall_dist_atr'],2):>7} "
          f"{('' if pd.isna(t['coloc_n']) else int(t['coloc_n'])):>5} "
          f"{fam}   {t['nearest_level'] or '—'} "
          f"{_sig(t['nearest_dist_atr'],2)}")
    A("  (signed distances in ATR; POSITIVE = price ABOVE the level.")
    A("   `close` is the BAR's close at that instant — for a STOP exit it is")
    A("   NOT the fill: the fill is the stop, printed under IDENTITY. wallΔ of")
    A("   0.00 means price sat INSIDE the ribbon band, which is the estate's")
    A("   own single-wall semantics and is why the stamp is `multi` so often.)")

    # ── LEAGUE CHAMPIONS ──────────────────────────────────────────────────
    A("")
    A(_rule("LEAGUE CHAMPION DISTANCE — each on its OWN clock"))
    A(f"  {'instant':21} {'kind':9} " + " ".join(f"{c:>14}" for c in CHAMPS))
    for _, i_ in mi.iterrows():
        key = (i_["asset"], int(i_["ts"]))
        if key not in tp.index:
            continue
        t = tp.loc[key]
        A(f"  {i_['ts_iso']:21} {i_['kind']:9} "
          + " ".join(_sig(t.get(f"champ_{c}_dist_atr"), 3).rjust(14)
                     for c in CHAMPS))
    A("  12h/1d EMA889 · 4h EMA3618 · 1h EMA4618 — the walls TC5's league")
    A("  named champion on each clock. Distance in THAT clock's own ATR.")

    # ── RIBBONS ───────────────────────────────────────────────────────────
    rib = [c for c in D["tape"].columns if c.endswith("_state_v2")]
    if rib:
        A("")
        A(_rule("RIBBON STATE"))
        A(f"  {'instant':21} {'kind':9} "
          + " ".join(f"{c.replace('_state_v2',''):>10}" for c in rib))
        for _, i_ in mi.iterrows():
            key = (i_["asset"], int(i_["ts"]))
            if key not in tp.index:
                continue
            t = tp.loc[key]
            A(f"  {i_['ts_iso']:21} {i_['kind']:9} "
              + " ".join(str(t.get(c, "—"))[:10].rjust(10) for c in rib))
    A("=" * 96)
    return out


def render_day(day: str, D: dict) -> list[str]:
    c = D["campaigns"]
    m = c[(c["entry_ts"].str[:10] == day) | (c["exit_ts"].str[:10] == day)
          | (c["arm_ts"].str[:10] == day)]
    out = [f"THE BOOK ON {day} — {len(m)} campaign(s) armed, entered or exited"]
    if not len(m):
        out.append("  (nothing)")
        return out
    out.append(f"  {'campaign_id':34} {'dir':6} {'entry':21} {'exit':21} "
               f"{'net R':>10}  what happened today")
    for _, r in m.sort_values(["entry_ms", "asset"]).iterrows():
        ev = [k for k, col in (("armed", "arm_ts"), ("entered", "entry_ts"),
                               ("exited", "exit_ts")) if r[col][:10] == day]
        out.append(f"  {r['campaign_id']:34} {r['direction']:6} "
                   f"{r['entry_ts']:21} {r['exit_ts']:21} "
                   f"{_sig(r['net_r'],4):>10}  {', '.join(ev)}")
    out.append(f"  net R of campaigns ENTERED today: "
               f"{_sig(m.loc[m['entry_ts'].str[:10] == day, 'net_r'].astype(float).sum(), 4)}")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Query the TIER-C5 book. Every number is read, none computed.")
    ap.add_argument("campaign_id", nargs="?", help="e.g. ETHUSDT:card:20251029T1600")
    ap.add_argument("--day", help="YYYY-MM-DD — the day's book")
    ap.add_argument("--random", type=int, metavar="N",
                    help="spot-audit N campaigns (SEEDED, reproducible)")
    ap.add_argument("--seed", type=int, default=20260816)
    ap.add_argument("--list", metavar="ASSET", help="list campaign ids")
    ap.add_argument("--timing", action="store_true", help="print elapsed ms")
    a = ap.parse_args()

    t0 = time.time()
    D = _load()
    lines: list[str] = []
    if a.list:
        c = D["campaigns"]
        m = c[c["asset"].str.upper().str.startswith(a.list.upper())]
        lines.append(f"{len(m)} campaign(s) for {a.list.upper()}")
        for _, r in m.iterrows():
            lines.append(f"  {r['campaign_id']:34} {r['direction']:6} "
                         f"{_sig(r['net_r'],4):>10}  {r['exit_reason']}")
    elif a.day:
        lines = render_day(a.day, D)
    elif a.random:
        rng = np.random.default_rng(a.seed)
        ids = sorted(D["campaigns"]["campaign_id"])
        pick = [ids[i] for i in rng.choice(len(ids), size=min(a.random, len(ids)),
                                           replace=False)]
        lines.append(f"SPOT AUDIT — {len(pick)} campaign(s), seed {a.seed} "
                     f"(reproducible; an audit you cannot re-run is an anecdote)")
        for cid in sorted(pick):
            lines += render(cid, D)
    elif a.campaign_id:
        lines = render(a.campaign_id, D)
    else:
        ap.print_help()
        return 0

    print("\n".join(lines))
    if a.timing:
        ms = (time.time() - t0) * 1000
        h = hashlib.sha256("\n".join(lines).encode()).hexdigest()[:16]
        print(f"\n[{ms:.0f} ms · output sha {h} · budget 2000 ms]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
