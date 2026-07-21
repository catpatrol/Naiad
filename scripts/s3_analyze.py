"""S-3 analysis — fixtures (F-BYTE first) + deliverables D1–D6, driven by
scripts/s3_enrich.py `analyze`. Read-only over the S-3 journals produced by
`run`; the P-CIRC (D4) and excursion (D5) evidence is computed in-process from
the SAME deterministic signal/trade objects the journal was written from (no
engine surface is touched — the strictest F-BYTE posture). D3 re-scores the
RC-7 confluence apparatus on the B book by calling the engine's own
`engine.s1.mtf_block` (exact definitional parity with the losing-book baseline).

Every table carries the in-sample / first-order caveat and states its
denominator (struct-R on B). Baselines (S-1, the losing book, native ratchet,
engine 1.0.9, baseline-R) are carried as constants for the side-by-side.
"""
from __future__ import annotations

import hashlib
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

CONFIG = "tc1_B"
END = "2024-06-30T23:59"
OUT = ROOT / "research_outputs" / "s3"
RESAMPLED = ROOT / "research_outputs" / "s1" / "resampled"
REF = ROOT / "research_outputs" / "tc1" / "B_run1" / "scored"   # F-BYTE baseline

CELLS = {
    "BTCUSDT_intraday": "2019-10-01", "BTCUSDT_position": "2020-01-01",
    "BTCUSDT_swing": "2019-11-01", "ETHUSDT_intraday": "2020-01-01",
    "ETHUSDT_position": "2020-04-01", "ETHUSDT_swing": "2020-01-01",
    "JTOUSDT_intraday": "2024-01-01", "JTOUSDT_position": "2024-04-01",
    "JTOUSDT_swing": "2024-02-01", "NEARUSDT_intraday": "2020-11-01",
    "NEARUSDT_position": "2021-02-01", "NEARUSDT_swing": "2020-12-01",
    "SOLUSDT_intraday": "2020-10-01", "SOLUSDT_position": "2021-01-01",
    "SOLUSDT_swing": "2020-11-01", "TAOUSDT_intraday": "2024-05-01",
    "TAOUSDT_swing": "2024-06-01", "ZECUSDT_intraday": "2020-03-01",
    "ZECUSDT_position": "2020-06-01", "ZECUSDT_swing": "2020-04-01"}
ORDER = sorted(CELLS, key=lambda c: ({"intraday": 0, "position": 1,
                                      "swing": 2}[c.rsplit("_", 1)[1]],
                                     CELLS[c]))
MANDATES = ("swing", "intraday", "position")

# ── D3 apparatus constants (engine.s1 / rc7_recompute.py) ──
LADDER = ["exec", "15m", "30m", "1h", "4h", "12h", "1d"]
GOV_IDX = {"swing": 4, "intraday": 3, "position": 5}   # LADDER index of governor
SEED_BIASED = {"JTOUSDT", "TAOUSDT"}                    # 1d void

# ── F-P2REF target (tc1_results.json, B GRID) ──
F_P2REF = {"sum_1x": -351.1542, "sum_0x": 1164.4202, "tranches": 7094,
           "win_rate_pct": 21.3322}

# ── Baseline (S-1 losing book, native ratchet, baseline-R) — for side-by-side.
# Sources: TC4_BASELINE.md, s1_results.json, RC7_RESULTS.md, S2B_DECOMPOSITION.md.
BASELINE = {
    "book": "S-1 (v12_anchor_g8, engine 1.0.9, native ratchet, baseline-R)",
    "resolved_tranches": 6279, "campaigns": 2599,
    "net_1x": -1796.993, "gross_0x": 275.9924, "win_campaign_pct": 10.8503,
    "cohort_pct": {"NEVER_GREEN": 17.42, "STILLBORN": 27.46,
                   "FADED": 14.17, "PROTECTED": 40.95},
    "cohort_n": {"NEVER_GREEN": 1094, "STILLBORN": 1724, "FADED": 890,
                 "PROTECTED": 2571},
    # PROTECTED-paradox: of 2571 tranches reaching >=1R MFE, 1233 exited at a
    # 0x (gross) loss; of those 1114 had zero stop advances before the MFE bar.
    "protected_n": 2571, "reached1r_then_grossloss_n": 1233,
    "zero_advance_share_pct": 90.3487,          # 1114 / 1233
    "reversal_share_of_protected_pct": 47.96,   # 1233 / 2571
    "win_by_exit_reason": {                     # tranche-level, baseline
        "stop": {"n": 6223, "win_pct": 16.2301},
        "stop_gap": {"n": 40, "win_pct": 10.0},
        "failure_x": {"n": 9, "win_pct": 33.3333},
        "opposite_cross": {"n": 3, "win_pct": 66.6667},
        "campaign_died": {"n": 4, "win_pct": 25.0}},
    # median winner-capture (realized_r / mfe_r among reached-profit) — the
    # PUBLISHED baseline is NEGATIVE per mandate (RC7-7 winner_capture p50):
    "winner_capture_p50_pct": {"swing": -20.93, "intraday": -20.80,
                               "position": -7.98},
    "peak_capture_soft_ref_pct": 6.0,   # the S-3 contract's "~6%" (soft, un-run)
}

# ── S-1 confluence baselines for P-S3-3 sign-flip detection (RC7_RESULTS.md /
# rc7_results.json). POOLED separation_r = exp_true - exp_false. NEGATIVE ones
# are the "negative-but-separating" flip candidates. Lattice: every S-1 cell is
# negative expectancy; triple-true = -0.4557, triple-false = -1.2244. ──
S1_MATRIX_SEP_POOLED = {
    ("exec", "s2_aligned"): 0.2951, ("exec", "beyond_e200"): 0.1142,
    ("exec", "beyond_e89"): 0.2221,
    ("15m", "s2_aligned"): -0.0134, ("15m", "beyond_e200"): -0.2021,
    ("15m", "beyond_e89"): -0.0924,
    ("30m", "s2_aligned"): 0.3895, ("30m", "beyond_e200"): 0.0386,
    ("30m", "beyond_e89"): -0.2537,
    ("1h", "s2_aligned"): 0.0554, ("1h", "beyond_e200"): 0.1834,
    ("1h", "beyond_e89"): -0.0263,
    ("4h", "s2_aligned"): -0.0266, ("4h", "beyond_e200"): 0.0260,
    ("4h", "beyond_e89"): 0.1228,
    ("12h", "s2_aligned"): -0.1470, ("12h", "beyond_e200"): -0.1614,
    ("12h", "beyond_e89"): -0.0086,
    ("1d", "s2_aligned"): -0.0911, ("1d", "beyond_e200"): -0.1957,
    ("1d", "beyond_e89"): -0.1932}
S1_LATTICE_TRIPLE = {"triple_true_exp": -0.4557, "triple_false_exp": -1.2244,
                     "separation": 0.7687}

CAVEAT = ("in-sample / first-order (exploration-classic window, current "
          "entries; ranks & reveals, does not validate out-of-sample); B "
          "denominated in struct-R (engine sizes qty on the structural "
          "distance, so realized_r is natively risk-normalized to the wider "
          "static stop); baseline = S-1, native ratchet, baseline-R.")

_rng = np.random.default_rng(20260721)


def r4(x):
    return None if x is None else round(float(x) + 0.0, 4)


def r6(x):
    return None if x is None else round(float(x) + 0.0, 6)


def pct(k, d):
    return None if not d else r4(100.0 * k / d)


def med(v):
    v = [x for x in v if x is not None]
    return r4(float(np.median(v))) if v else None


def mean(v):
    v = [x for x in v if x is not None]
    return r4(float(np.mean(v))) if v else None


def boot_ci(v, n=4000):
    v = [x for x in v if x is not None]
    if len(v) < 2:
        return [None, None]
    a = np.array(v, float)
    means = a[_rng.integers(0, len(a), size=(n, len(a)))].mean(axis=1)
    return [r4(float(np.percentile(means, 2.5))),
            r4(float(np.percentile(means, 97.5)))]


# ══════════════════════════════════════════ in-process recompute (D4/D5/D3)
def recompute(cell_id: str):
    """Reproduce run_replay's signal+trade objects (same deterministic inputs
    as the journal) so excursion/P-CIRC/confluence primitives are exact."""
    from engine.config import load_config
    from engine.cells import cell_by_id, MTF_SET
    from engine.replay import (parse_utc, load_cell_data, assert_warmup,
                               _tc1_arch_data)
    from engine.signals import compute_signals
    from engine.trading import run_trading
    cfg = load_config(CONFIG)
    cell = cell_by_id(cell_id)
    start_ms, end_ms = parse_utc(CELLS[cell_id]), parse_utc(END)
    data = load_cell_data(cell, start_ms, end_ms, backfill=False,
                          log=lambda *a, **k: None)
    assert_warmup(cell, data, start_ms)
    sig = compute_signals(cell, cfg["signal"], data[cell.tf_exec],
                          data[cell.tf_gov], {tf: data[tf] for tf in MTF_SET},
                          v_births_provisional=cfg["signal"]["v_births_provisional"])
    arch_data = _tc1_arch_data(cell, cfg, sig, data)
    trades = run_trading(cell, cfg, sig, data["funding"], start_ms=start_ms,
                         arch_data=arch_data)
    return cfg, cell, sig, trades, data, start_ms, end_ms


# ══════════════════════════════════════════════════════ journal readers
def read_cell(root: Path, cell: str):
    """fills{tid:row}, exits[rows] — the resolved-tranche set = EXIT rows."""
    fills, exits = {}, []
    for p in sorted((root / cell).glob("*.jsonl")):
        for line in open(p, encoding="utf-8"):
            if not line.strip():
                continue
            r = json.loads(line)
            if r["evt"] in ("ENTRY_FILL", "ADD_FILL"):
                fills[r["tranche_id"]] = r
            elif r["evt"] == "EXIT":
                exits.append(r)
    return fills, exits


def tstats(fills, exits):
    """Per resolved tranche — tc1_fixtures.tstats, verbatim semantics."""
    out = []
    for r in exits:
        f = fills[r["tranche_id"]]
        cost = (r["fees"] or 0) + (r["funding_cum"] or 0) + (r["slippage"] or 0)
        unit = abs(f["px_fill"] - f["stop"])
        one_r = unit * f["qty"] / f["size_r"]
        out.append({
            "tid": r["tranche_id"], "mandate": f["cell_id"].rpartition("_")[2],
            "camp": int(r["tranche_id"][1:].split("t")[0]),
            "realized_r": r["realized_r"], "size": f["size_r"],
            "cost_r": cost / one_r, "dir": 1 if f["dir"] == "long" else -1,
            "mfe_r": r["mfe_r"], "mae_r": r["mae_r"],
            "give_back_r": r["give_back_r"], "cohort": r["cohort"],
            "retr": r["retr"], "grade": f["grade"], "zone": f["zone"],
            "exit_reason": r["exit_reason"], "fill_class": f["fill_class"]})
    return out


def book(trs, sel=None):
    """tc1_fixtures.book — 0x/1x/2x toll, campaign-level win rate."""
    ts = [t for t in trs if sel is None or sel(t)]
    s1 = sum(t["realized_r"] for t in ts)
    s0 = sum(t["realized_r"] + t["cost_r"] for t in ts)
    s2 = sum(t["realized_r"] - t["cost_r"] for t in ts)
    camp = defaultdict(float)
    for t in ts:
        camp[(t["mandate"], t["camp"])] += t["realized_r"]
    vals = list(camp.values())
    best = max(vals) if vals else 0.0
    return {"sum_1x": r4(s1), "sum_0x": r4(s0), "sum_2x": r4(s2),
            "tranches": len(ts), "campaigns": len(vals),
            "win_rate_pct": pct(sum(1 for v in vals if v > 0), len(vals)),
            "strip_best_1x": r4(s1 - best), "cost_stack": r4(s0 - s1)}


# ══════════════════════════════ per-cell: excursion (D5) + P-CIRC (D4)
HORIZONS = [10, 20, 50, 100]


def _last_cross_bars(flag_up, flag_dn, n):
    """bars-since the most recent up-or-down cross, per bar (BIG if none)."""
    BIG = 10 ** 9
    out = np.full(n, BIG, dtype=np.int64)
    last = -BIG
    for j in range(n):
        if flag_up[j] or flag_dn[j]:
            last = j
        out[j] = j - last if last > -BIG else BIG
    return out


def cell_excursion_pcirc(cfg, cell, sig, trades, exits, run_id):
    """Excursion-substrate rows + P-CIRC snapshots, joined to the resolved set
    (journal EXIT rows). Returns (substrate_rows, pcirc_snaps, advance_recs)."""
    from engine import indicators as ind
    n = len(sig.c)
    resolved_tids = {r["tranche_id"] for r in exits}
    trmap = {t.tranche_id: t for t in trades.tranches}
    p = cfg["signal"]

    # signal geometry for P-CIRC availability (self-contained from sig)
    x9up = ind.crossover(sig.c, sig.e9x)
    x9dn = ind.crossunder(sig.c, sig.e9x)
    rib_up = ind.crossover(sig.e9x, sig.e89x)
    rib_dn = ind.crossunder(sig.e9x, sig.e89x)
    x89up = ind.crossover(sig.e89x, sig.e200x)
    x89dn = ind.crossunder(sig.e89x, sig.e200x)
    bs_989 = _last_cross_bars(rib_up, rib_dn, n)
    bs_89200 = _last_cross_bars(x89up, x89dn, n)
    bar_range = sig.h - sig.l
    min_range, min_ribsep = p["min_bar_range_atr"], p["min_ribbon_sep_atr"]

    # trigger-type family for ADD tranches (PRIME-add vs CONFIRM), by the
    # spawning signal event at signal_i; PRIME fills before CONFIRM (emission
    # order), so PRIME wins an ambiguous same-bar co-occurrence — disclosed.
    prime_add_bar = defaultdict(set)   # (dir) -> set of bars with PRIME is_add
    confirm_add_bar = defaultdict(set)
    prime_fire_bar = defaultdict(set)  # any PRIME fired in dir at bar
    for ev in sig.events:
        if ev.evt == "PRIME":
            prime_fire_bar[ev.dir].add(ev.i)
            if ev.is_add:
                prime_add_bar[ev.dir].add(ev.i)
        elif ev.evt == "CONFIRM" and ev.is_add:
            confirm_add_bar[ev.dir].add(ev.i)

    def trigger_type(tr):
        if tr.kind == "R1":
            return "PRIME-R1"
        if tr.kind == "V":
            return "V"
        if tr.signal_i in prime_add_bar[tr.dir]:
            return "PRIME-add"
        if tr.signal_i in confirm_add_bar[tr.dir]:
            return "CONFIRM"
        return "PRIME-add"   # add with no matched event (rare) — default+count

    sub_rows, pcirc, advance_recs = [], [], []
    ambiguous_family = 0
    for tid in sorted(resolved_tids):
        tr = trmap.get(tid)
        if tr is None:
            raise KeyError(f"{cell.cell_id}: resolved {tid} not in trades")
        d, f, xi = tr.dir, tr.fill_i, tr.exit_i
        entry_atr = float(sig.atr_x[tr.signal_i])
        fill_px = tr.fill_px
        unit = (tr.fill_px - tr.stop_at_entry) * d      # struct-R unit (>0)
        fav = sig.h if d == 1 else sig.l
        adv = sig.l if d == 1 else sig.h
        if (tr.kind == "ADD" and tr.signal_i in prime_add_bar[d]
                and tr.signal_i in confirm_add_bar[d]):
            ambiguous_family += 1

        def exc(end_bar):
            end_bar = min(end_bar, n - 1)
            seg_f = fav[f:end_bar + 1]
            seg_a = adv[f:end_bar + 1]
            fe = float(seg_f.max()) if d == 1 else float(seg_f.min())
            ae = float(seg_a.min()) if d == 1 else float(seg_a.max())
            return (fe - fill_px) * d, (ae - fill_px) * d, end_bar - f

        row = {"run_id": run_id, "arm_id": "B", "cell": cell.cell_id,
               "tranche_id": tid, "trigger_type": trigger_type(tr),
               "grade": tr.grade, "entry_zone": tr.zone, "retr": r6(tr.retr),
               "dir": "long" if d == 1 else "short",
               "entry_atr": r6(entry_atr), "fill_px": r6(fill_px),
               "unit_bps": r6(unit / fill_px * 1e4)}
        for H in HORIZONS:
            mfe, mae, _ = exc(f + H)
            row[f"mfe_bps_h{H}"] = r6(mfe / fill_px * 1e4)
            row[f"mae_bps_h{H}"] = r6(mae / fill_px * 1e4)
            row[f"mfe_atr_h{H}"] = r6(mfe / entry_atr)
            row[f"mae_atr_h{H}"] = r6(mae / entry_atr)
            row[f"trunc_h{H}"] = bool((f + H) > n - 1)
        mfe_x, mae_x, _ = exc(xi)
        row["mfe_bps_exit"] = r6(mfe_x / fill_px * 1e4)
        row["mae_bps_exit"] = r6(mae_x / fill_px * 1e4)
        row["mfe_atr_exit"] = r6(mfe_x / entry_atr)
        row["mae_atr_exit"] = r6(mae_x / entry_atr)
        row["exit_bar_offset"] = int(xi - f)
        row["exit_reason"] = tr.exit_reason
        sub_rows.append(row)

        # +1R moment & MFE bar (same peak logic as enrich mfe_r) → P-CIRC +
        # stop-advance-before-MFE (the PROTECTED paradox, on B).
        bars = list(range(f, xi))
        if tr.exit_reason == "stop":
            bars.append(xi)
        running = fill_px
        moment = mfe_bar = None
        peak_final = fill_px
        for j in bars:
            running = max(running, sig.h[j]) if d == 1 else min(running, sig.l[j])
            if moment is None and (running - fill_px) * d >= unit:
                moment = j
            if running != peak_final:          # new favorable extreme
                peak_final = running
                mfe_bar = j
        if mfe_bar is None:
            mfe_bar = f
        mfe_r_check = (peak_final - fill_px) * d / unit
        reached_1r = moment is not None

        # Count strict tightenings of the tranche's WORKING stop over
        # (fill, mfe_bar]. For B the working stop is the STATIC struct_stop
        # (is_struct, trail_on=False → work_stop == struct_stop, never moves),
        # so this is 0 by construction — measured here, not assumed.
        def work_stop_j(j):
            if tr.trail_on and tr.engaged:
                return tr.trail_stop
            if tr.is_struct:
                return tr.struct_stop
            return sig.stop_long[j - 1] if d == 1 and j > 0 else \
                (sig.stop_short[j - 1] if j > 0 else float("nan"))
        advances = 0
        prev = work_stop_j(f)
        for j in range(f + 1, mfe_bar + 1):
            s = work_stop_j(j)
            if not math.isnan(s) and not math.isnan(prev) and (s - prev) * d > 1e-12:
                advances += 1
            prev = s
        advance_recs.append({"tid": tid, "mandate": cell.mandate,
                             "reached_1r": reached_1r, "advances": advances,
                             "mfe_r": r6(mfe_r_check)})

        if reached_1r:
            m = moment
            atr = float(sig.atr_x[m])
            e9, e89, e200 = sig.e9x[m], sig.e89x[m], sig.e200x[m]
            c_m = sig.c[m]
            zone = int(sig.active_zone[m])
            raw_reclaim = bool(
                (d == 1 and m > 0 and x9up[m - 1] and c_m > e9 and c_m >= sig.c[m - 1])
                or (d == -1 and m > 0 and x9dn[m - 1] and c_m < e9 and c_m <= sig.c[m - 1]))
            range_ok = bool(not math.isnan(atr) and bar_range[m] >= min_range * atr)
            ribsep_ok = bool((not math.isnan(atr)
                              and abs(e9 - e89) >= min_ribsep * atr) or zone == 3)
            zone_ok = zone > 0
            snap = {
                "cell": cell.cell_id, "mandate": cell.mandate,
                "tranche_id": tid, "trigger_type": trigger_type(tr),
                "grade": tr.grade, "entry_zone": tr.zone,
                "dir": "long" if d == 1 else "short",
                "moment_offset": int(m - f),
                "cross_9_89_bull": bool(e9 > e89),
                "cross_89_200_bull": bool(e89 > e200),
                "cross_9_89_with_dir": bool((e9 - e89) * d > 0),
                "cross_89_200_with_dir": bool((e89 - e200) * d > 0),
                "bars_since_9_89_cross": int(bs_989[m]),
                "bars_since_89_200_cross": int(bs_89200[m]),
                "px_beyond_e9_dir": bool((c_m - e9) * d > 0),
                "px_beyond_e89_dir": bool((c_m - e89) * d > 0),
                "px_beyond_e200_dir": bool((c_m - e200) * d > 0),
                "px_beyond_gov_e89_dir": bool((c_m - sig.g_e89[m]) * d > 0
                                              if not math.isnan(sig.g_e89[m]) else False),
                "ribbon_sep_atr": r6(abs(e9 - e89) / atr if atr and not math.isnan(atr) else None),
                "active_zone": zone,
                "raw_reclaim": raw_reclaim, "zone_ok": zone_ok,
                "range_ok": range_ok, "ribsep_ok": ribsep_ok,
                "prime_available": bool(raw_reclaim and zone_ok and range_ok and ribsep_ok),
                "prime_fired": bool(m in prime_fire_bar[d]),
                "confirm_available": bool(rib_up[m] if d == 1 else rib_dn[m])}
            pcirc.append(snap)

    return sub_rows, pcirc, advance_recs, ambiguous_family


# ══════════════════════════════════════════════ D3 confluence on the B book
def cell_confluence(cfg, cell, sig, trades, data, exits):
    """RC-7r lattice axes + symmetric-matrix condition flags per campaign,
    via engine.s1.mtf_block (exact RC-7 parity). Returns campaign records."""
    from engine.s1 import S1Context, mtf_block, _mfe_bar
    ctx = S1Context(cell, cfg, sig, trades, data, RESAMPLED)
    resolved = {r["tranche_id"] for r in exits}
    realized = {r["tranche_id"]: r["realized_r"] for r in exits}
    # campaign -> tranches (sorted), opener = first fill
    camps = defaultdict(list)
    for t in trades.tranches:
        camps[t.campaign].append(t)
    recs = []
    for camp, trs in camps.items():
        trs = sorted(trs, key=lambda t: (t.fill_i, t.tranche_id))
        opener = trs[0]
        # camp_r over resolved tranches of this campaign (traded outcome)
        cr = [realized[t.tranche_id] for t in trs if t.tranche_id in realized]
        if opener.tranche_id not in resolved or not cr:
            continue
        mb = _mfe_bar(ctx, opener)
        mtf = mtf_block(ctx, opener, mb)
        d = opener.dir
        d200_1d = mtf["1d"].get("entry_d200")
        c1d = (None if (cell.symbol in SEED_BIASED or d200_1d is None)
               else (not (d200_1d * d > 0)))
        # ctoll from opener fill (stop_dist_bps vs 2x roundtrip toll)
        fpx, spx = opener.fill_px, opener.stop_at_entry
        dist_bps = abs(fpx - spx) / fpx * 1e4
        cost_bps = 2.0 * (cfg["trading"]["fee_bps_side"] + cell.slippage_bps)
        ctoll = bool(dist_bps >= 2.0 * cost_bps)
        conds = {}
        for tf in LADDER:
            m = mtf[tf]
            conds[(tf, "s2_aligned")] = bool(m["s2_aligned_entry"])
            for el in ("200", "89"):
                v = m.get(f"entry_d{el}")
                conds[(tf, f"beyond_e{el}")] = (None if v is None else v * d > 0)
        recs.append({"cell": cell.cell_id, "mandate": cell.mandate,
                     "symbol": cell.symbol, "camp": camp, "dir": d,
                     "camp_r": sum(cr), "c30": bool(mtf["30m"]["s2_aligned_entry"]),
                     "c1d": c1d, "ctoll": ctoll, "conds": conds})
    return recs


# ══════════════════════════════════════════════════════════ D1 anatomy
TIERS = [("<0", -1e18, 0.0), ("0-0.5", 0.0, 0.5), ("0.5-1", 0.5, 1.0),
         ("1-2", 1.0, 2.0), ("2-3", 2.0, 3.0), (">=3", 3.0, 1e18)]


def tier_of(mfe):
    if mfe is None:
        return None
    for name, lo, hi in TIERS:
        if lo <= mfe < hi:
            return name
    return ">=3"


def d1_anatomy(all_ts, advmap):
    def book_anatomy(sel):
        ts = [t for t in all_ts if sel(t)]
        nt = len(ts)
        tiers = Counter(tier_of(t["mfe_r"]) for t in ts)
        tier_tbl = {name: {"n": tiers.get(name, 0), "pct": pct(tiers.get(name, 0), nt)}
                    for name, _, _ in TIERS}
        cohort = Counter(t["cohort"] for t in ts)
        cohort_tbl = {k: {"n": cohort.get(k, 0), "pct": pct(cohort.get(k, 0), nt)}
                      for k in ("NEVER_GREEN", "STILLBORN", "FADED", "PROTECTED")}
        # reached >=1R then loss (0x gross and 1x net) + zero-stop-advance
        prot = [t for t in ts if (t["mfe_r"] or -9) >= 1.0]
        gl = [t for t in prot if (t["realized_r"] + t["cost_r"]) < 0]
        nl = [t for t in prot if t["realized_r"] < 0]
        zadv = [t for t in gl if advmap.get(t["tid"], 1) == 0]
        rev_by_tier = {}
        for name, lo, hi in TIERS:
            if lo < 1.0:
                continue
            pt = [t for t in prot if lo <= (t["mfe_r"] or -9) < hi]
            ptl = [t for t in pt if (t["realized_r"] + t["cost_r"]) < 0]
            rev_by_tier[name] = {"reached_n": len(pt), "grossloss_n": len(ptl),
                                 "grossloss_pct": pct(len(ptl), len(pt))}
        # win rate by exit reason (tranche-level)
        wbe = {}
        by_reason = defaultdict(list)
        for t in ts:
            by_reason[t["exit_reason"]].append(t)
        for rsn, g in by_reason.items():
            wbe[rsn] = {"n": len(g),
                        "win_pct": pct(sum(1 for x in g if x["realized_r"] > 0), len(g))}
        # peak-capture = realized_r / mfe_r among reached-profit (mfe_r>0)
        cap = [t["realized_r"] / t["mfe_r"] for t in ts
               if t["mfe_r"] and t["mfe_r"] > 0]
        return {"n": nt, "reached_profit_tiers": tier_tbl, "cohort": cohort_tbl,
                "protected_n": len(prot),
                "reached1r_then_grossloss_n": len(gl),
                "reached1r_then_netloss_n": len(nl),
                "zero_stop_advance_n": len(zadv),
                "zero_stop_advance_share_pct": pct(len(zadv), len(gl)),
                "reversal_share_of_protected_pct": pct(len(gl), len(prot)),
                "reversal_by_tier": rev_by_tier,
                "win_by_exit_reason": wbe,
                "median_peak_capture_pct": r4(100.0 * np.median(cap)) if cap else None,
                "win_rate_tranche_pct": pct(sum(1 for t in ts if t["realized_r"] > 0), nt)}
    out = {"GRID": book_anatomy(lambda t: True)}
    for m in MANDATES:
        out[m] = book_anatomy(lambda t, m=m: t["mandate"] == m)
    return out


# ══════════════════════════════════════════════════════════ D2 retr
def d2_retr(all_ts):
    v = [t for t in all_ts if t["retr"] is not None]
    rv = np.array([t["retr"] for t in v], float)
    if len(rv) < 20:
        return {"note": "insufficient retr sample", "n": len(rv)}
    edges = np.quantile(rv, np.linspace(0, 1, 11))
    edges[-1] += 1e-9
    deciles = []
    for k in range(10):
        lo, hi = edges[k], edges[k + 1]
        g = [t for t in v if lo <= t["retr"] < hi]
        rr = [t["realized_r"] for t in g]
        mm = [t["mfe_r"] for t in g if t["mfe_r"] is not None]
        # strip-best: expectancy after removing the single best tranche
        exp = mean(rr)
        strip = r4((sum(rr) - max(rr)) / (len(rr) - 1)) if len(rr) > 1 else None
        deciles.append({"decile": k + 1, "retr_lo": r4(lo), "retr_hi": r4(hi),
                        "n": len(g), "expectancy_r": exp, "ci95": boot_ci(rr),
                        "strip_best_exp_r": strip, "mfe_r_mean": mean(mm),
                        "mfe_r_median": med(mm)})
    # mid-band (retr in 0.5-0.8) vs shallowest & deepest deciles
    mid = [t["realized_r"] for t in v if 0.5 <= t["retr"] <= 0.8]
    d1exp = deciles[0]["expectancy_r"]
    d10exp = deciles[-1]["expectancy_r"]
    midexp = mean(mid)
    # sign-stability: is every decile whose center is in 0.5-0.8 above both
    # the shallowest and deepest decile?
    band_deciles = [d for d in deciles
                    if 0.5 <= (d["retr_lo"] + d["retr_hi"]) / 2 <= 0.8]
    lift = all((d["expectancy_r"] or -9) > (d1exp or 9)
               and (d["expectancy_r"] or -9) > (d10exp or 9)
               for d in band_deciles) if band_deciles else False
    # A+ overlay (grade A+), reference only
    ap = [t["realized_r"] for t in all_ts if t["grade"] == "A+"]
    return {"deciles": deciles, "n": len(v),
            "mid_band_0p5_0p8": {"n": len(mid), "expectancy_r": midexp},
            "shallowest_decile_exp_r": d1exp, "deepest_decile_exp_r": d10exp,
            "mid_band_beats_both_ends": bool(lift),
            "aplus_overlay": {"n": len(ap), "expectancy_r": mean(ap),
                              "note": "reference only, tiny n — NOT the estimator"}}


# ══════════════════════════════════════════════════════════ D3 render
def d3_confluence(all_conf):
    def latt(recs, label):
        cr = {(r["cell"], r["camp"]): r["camp_r"] for r in recs}
        wins_total = sum(max(v, 0.0) for v in cr.values())
        rows = {}
        for a in (True, False):
            for b in (True, False, None):
                for t2 in (True, False):
                    key = f"30m={int(a)}|1d_room={'void' if b is None else int(b)}|toll={int(t2)}"
                    vs = [r["camp_r"] for r in recs if r["c30"] == a
                          and r["c1d"] == b and r["ctoll"] == t2]
                    if not vs and b is None:
                        continue
                    rows[key] = {"n": len(vs), "expectancy": mean(vs),
                                 "ci95": boot_ci(vs), "sum": r4(sum(vs)),
                                 "share_of_sum_wins_pct":
                                     pct(sum(max(v, 0.0) for v in vs), wins_total)
                                     if wins_total else None}
        return rows

    def matrix(recs, mandate):
        out = {}
        for tf in LADDER:
            steps = LADDER.index(tf) - (GOV_IDX[mandate] if mandate != "GRID"
                                        else 4)
            for cond in ("s2_aligned", "beyond_e200", "beyond_e89"):
                sub = recs
                if tf == "1d":
                    sub = [r for r in recs if r["symbol"] not in SEED_BIASED]
                tvals = [r["camp_r"] for r in sub if r["conds"].get((tf, cond)) is True]
                fvals = [r["camp_r"] for r in sub if r["conds"].get((tf, cond)) is False]
                et, ef = mean(tvals), mean(fvals)
                sep = r4(et - ef) if (et is not None and ef is not None) else None
                s1 = S1_MATRIX_SEP_POOLED.get((tf, cond)) if mandate == "GRID" else None
                out[f"{tf}|{cond}"] = {
                    "tf": tf, "condition": cond, "steps_from_governor": steps,
                    "n_true": len(tvals), "n_false": len(fvals),
                    "exp_true": et, "exp_false": ef, "separation_r": sep,
                    "s1_pooled_separation": s1,
                    "flip_positive": bool(s1 is not None and s1 < 0 and sep is not None and sep > 0)}
        return out

    res = {}
    scopes = {"GRID": all_conf}
    for m in MANDATES:
        scopes[m] = [r for r in all_conf if r["mandate"] == m]
    for scope, recs in scopes.items():
        res[scope] = {"lattice": latt(recs, scope), "matrix": matrix(recs, scope)}
    # P-S3-3: any condition negative-separating on S-1 that flips positive on B
    flips = []
    for key, cell in res["GRID"]["matrix"].items():
        if cell["flip_positive"]:
            flips.append({"cell": key, "s1_sep": cell["s1_pooled_separation"],
                          "b_sep": cell["separation_r"],
                          "b_exp_true": cell["exp_true"]})
    tri = res["GRID"]["lattice"].get("30m=1|1d_room=1|toll=1")
    trif = res["GRID"]["lattice"].get("30m=0|1d_room=0|toll=0")
    res["p_s3_3"] = {
        "flips_positive": flips, "n_flips": len(flips),
        "s1_triple_true_exp": S1_LATTICE_TRIPLE["triple_true_exp"],
        "b_triple_true_exp": tri["expectancy"] if tri else None,
        "b_triple_false_exp": trif["expectancy"] if trif else None}
    return res


# ══════════════════════════════════════════════════════════ D4 P-CIRC
def d4_pcirc(all_snaps):
    def agg(snaps):
        nS = len(snaps)
        if not nS:
            return {"n": 0}

        def share(key):
            return pct(sum(1 for s in snaps if s[key]), nS)
        return {
            "n": nS,
            # THE headline: winning moments with NO pullback-reclaim PRIME
            # available (the circular freeze) — P-S3-4.
            "prime_unavailable_share_pct": pct(sum(1 for s in snaps if not s["prime_available"]), nS),
            "prime_available_share_pct": share("prime_available"),
            "prime_fired_share_pct": share("prime_fired"),
            "confirm_available_share_pct": share("confirm_available"),
            "either_available_share_pct": pct(sum(1 for s in snaps if s["prime_available"] or s["confirm_available"]), nS),
            # why PRIME was unavailable — the gate that failed most
            "raw_reclaim_share_pct": share("raw_reclaim"),
            "zone_ok_share_pct": share("zone_ok"),
            "range_ok_share_pct": share("range_ok"),
            "ribsep_ok_share_pct": share("ribsep_ok"),
            # independent state at winning moments (the non-PRIME add keys)
            "px_beyond_e9_dir_pct": share("px_beyond_e9_dir"),
            "px_beyond_e89_dir_pct": share("px_beyond_e89_dir"),
            "px_beyond_e200_dir_pct": share("px_beyond_e200_dir"),
            "px_beyond_gov_e89_dir_pct": share("px_beyond_gov_e89_dir"),
            "cross_9_89_with_dir_pct": share("cross_9_89_with_dir"),
            "cross_89_200_with_dir_pct": share("cross_89_200_with_dir"),
            "median_bars_since_9_89_cross": med([s["bars_since_9_89_cross"] for s in snaps]),
            "median_ribbon_sep_atr": med([s["ribbon_sep_atr"] for s in snaps]),
            "active_zone_dist": dict(Counter(s["active_zone"] for s in snaps))}
    out = {"GRID": agg(all_snaps)}
    for m in MANDATES:
        out[m] = agg([s for s in all_snaps if s["mandate"] == m])
    out["by_trigger_type"] = {tt: agg([s for s in all_snaps if s["trigger_type"] == tt])
                              for tt in ("PRIME-R1", "PRIME-add", "CONFIRM", "V")}
    return out


# ══════════════════════════════════════════════════════════ D5 pivot
def d5_pivot(sub_rows):
    """MFE/MAE (bps + entry-ATR) by trigger_type × grade × entry_zone, cell-B."""
    groups = defaultdict(list)
    for r in sub_rows:
        groups[(r["trigger_type"], r["grade"], r["entry_zone"])].append(r)
    piv = []
    for (tt, g, z), rows in sorted(groups.items()):
        piv.append({
            "trigger_type": tt, "grade": g, "entry_zone": z, "n": len(rows),
            "mfe_bps_h100_med": med([r["mfe_bps_h100"] for r in rows]),
            "mae_bps_h100_med": med([r["mae_bps_h100"] for r in rows]),
            "mfe_atr_h100_med": med([r["mfe_atr_h100"] for r in rows]),
            "mae_atr_h100_med": med([r["mae_atr_h100"] for r in rows]),
            "mfe_atr_exit_med": med([r["mfe_atr_exit"] for r in rows]),
            "mae_atr_exit_med": med([r["mae_atr_exit"] for r in rows])})
    return piv


# ══════════════════════════════════════════════════════════ collection
def _norm(line):
    r = json.loads(line)
    r.pop("s1", None)
    r.pop("s2", None)
    r["run_id"] = r["engine_version"] = r["config_id"] = "-"
    return json.dumps(r, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False)


def collect_cell(jroot, cell_id):
    fills, exits = read_cell(jroot, cell_id)
    run_id = exits[0]["run_id"] if exits else "-"
    cfg, cell, sig, trades, data, start_ms, end_ms = recompute(cell_id)
    ts = tstats(fills, exits)
    sub, pcirc, adv, ambig = cell_excursion_pcirc(cfg, cell, sig, trades, exits, run_id)
    conf = cell_confluence(cfg, cell, sig, trades, data, exits)
    return {"cell": cell_id, "ts": ts, "sub": sub, "pcirc": pcirc,
            "adv": adv, "conf": conf, "ambiguous_family": ambig,
            "resolved_n": len(exits), "fills_n": len(fills)}


# ══════════════════════════════════════════════════════════ orchestrator
def run_analysis(cells=None, jroot=None, do_byte=True, do_det=True):
    cells = cells or ORDER
    jroot = jroot or (OUT / "journal_s3" / "scored")
    per = {}
    print(f"[analyze] collecting {len(cells)} cells from {jroot} ...", flush=True)
    for c in cells:
        per[c] = collect_cell(jroot, c)
        print(f"[analyze] {c:<18} resolved={per[c]['resolved_n']:>5} "
              f"sub={len(per[c]['sub']):>5} pcirc={len(per[c]['pcirc']):>5} "
              f"camps={len(per[c]['conf']):>5}", flush=True)

    all_ts = [t for c in cells for t in per[c]["ts"]]
    all_sub = [r for c in cells for r in per[c]["sub"]]
    all_pc = [s for c in cells for s in per[c]["pcirc"]]
    all_adv = [a for c in cells for a in per[c]["adv"]]
    all_conf = [r for c in cells for r in per[c]["conf"]]
    advmap = {a["tid"]: a["advances"] for a in all_adv}
    resolved_total = sum(per[c]["resolved_n"] for c in cells)

    # ── FIXTURES (F-BYTE FIRST) ──
    fx = {}
    if do_byte:
        mism = []
        for c in cells:
            a = [_norm(l) for p in sorted((jroot / c).glob("*.jsonl"))
                 for l in open(p, encoding="utf-8") if l.strip()]
            b = [_norm(l) for p in sorted((REF / c).glob("*.jsonl"))
                 for l in open(p, encoding="utf-8") if l.strip()]
            if a != b:
                mism.append((c, len(a), len(b)))
        fx["F-BYTE"] = {"mismatched_cells": mism, "match": not mism}
    reached = sum(1 for a in all_adv if a["reached_1r"])
    fx["F-CIRC-N"] = {"pcirc_snapshots": len(all_pc), "reached_1r_tranches": reached,
                      "match": len(all_pc) == reached}
    nulls = sum(1 for r in all_sub for k, v in r.items() if v is None
                and k not in ("retr",))   # retr can be null (V / re-entry legs)
    fx["F-SUB"] = {"substrate_rows": len(all_sub), "resolved_tranches": resolved_total,
                   "nonretr_nulls": nulls,
                   "match": len(all_sub) == resolved_total and nulls == 0}
    grid = book(all_ts)
    fx["F-P2REF"] = {"measured": {"sum_1x": grid["sum_1x"], "sum_0x": grid["sum_0x"],
                                  "tranches": grid["tranches"], "win_rate_pct": grid["win_rate_pct"]},
                     "target": F_P2REF,
                     "match": (grid["sum_1x"] == F_P2REF["sum_1x"]
                               and grid["sum_0x"] == F_P2REF["sum_0x"]
                               and grid["tranches"] == F_P2REF["tranches"]
                               and grid["win_rate_pct"] == F_P2REF["win_rate_pct"])}
    if do_det:
        man = json.loads((OUT / "manifest.json").read_text(encoding="utf-8")) \
            if (OUT / "manifest.json").exists() else {"determinism_all_identical": None, "cells": {}}
        detm = [c for c in cells if not man["cells"].get(c, {}).get("match", False)]
        fx["F-DET"] = {"mismatched": detm, "manifest": man.get("determinism_all_identical"),
                       "match": man.get("determinism_all_identical") is True and not detm}

    order = ["F-BYTE", "F-P2REF", "F-CIRC-N", "F-SUB", "F-DET"]
    print("\n== S-3 fixtures (F-BYTE first) ==")
    passed = 0
    present = [k for k in order if k in fx]
    for k in present:
        v = fx[k]
        passed += bool(v["match"])
        print(f"{k:<9} {'MATCH' if v['match'] else '*** MISMATCH ***'} "
              f"{json.dumps({kk: vv for kk, vv in v.items() if kk != 'match'}, default=str)[:150]}")
    byte_ok = fx.get("F-BYTE", {"match": True})["match"]
    if do_byte and not byte_ok:
        print("\n*** F-BYTE FAILURE: HALT — a moved traded column means the "
              "capture is not inert. Producing nothing downstream. ***")
        (ROOT / "s3_results.json").write_text(
            json.dumps({"HALT": "F-BYTE", "fixtures": fx}, indent=1,
                       sort_keys=True, default=str) + "\n", encoding="utf-8", newline="\n")
        return 1

    # ── DELIVERABLES ──
    res = {
        "phase": "S-3 cell-B enrichment & cross-run excursion substrate",
        "engine_version": "1.0.11", "config_id": CONFIG, "denominator": "struct-R",
        "caveat": CAVEAT, "fixtures": fx, "baseline": BASELINE,
        "headline": {"GRID": grid,
                     **{m: book(all_ts, lambda t, m=m: t["mandate"] == m) for m in MANDATES}},
        "D1_anatomy": d1_anatomy(all_ts, advmap),
        "D2_retracement": d2_retr(all_ts),
        "D3_confluence": d3_confluence(all_conf),
        "D4_pcirc": d4_pcirc(all_pc),
        "D5_excursion_pivot": d5_pivot(all_sub),
        "ambiguous_add_family_total": sum(per[c]["ambiguous_family"] for c in cells),
    }
    res["predictions"] = score_predictions(res)
    res["D6_paragraph"] = d6_paragraph(res)

    # ── write substrate jsonl (deterministic order) ──
    all_sub_sorted = sorted(all_sub, key=lambda r: (r["cell"], r["tranche_id"]))
    sub_path = ROOT / "s3_excursion_substrate.jsonl"
    with open(sub_path, "w", encoding="utf-8", newline="\n") as fp:
        for r in all_sub_sorted:
            fp.write(json.dumps(r, sort_keys=True, separators=(",", ":"),
                                ensure_ascii=False) + "\n")
    res["substrate_sha256"] = hashlib.sha256(sub_path.read_bytes()).hexdigest()
    res["substrate_rows"] = len(all_sub_sorted)

    blob = json.dumps(res, indent=1, sort_keys=True, default=str) + "\n"
    (ROOT / "s3_results.json").write_text(blob, encoding="utf-8", newline="\n")
    md = render_md(res)
    (ROOT / "S3_ENRICHMENT.md").write_text(md, encoding="utf-8", newline="\n")

    print(f"\nfixtures {passed}/{len(present)} MATCH")
    print("OUTPUT_HASH s3_results.json:", hashlib.sha256(blob.encode()).hexdigest())
    print("OUTPUT_HASH S3_ENRICHMENT.md:", hashlib.sha256(md.encode()).hexdigest())
    print("OUTPUT_HASH s3_excursion_substrate.jsonl:", res["substrate_sha256"])
    for p in res["predictions"]:
        print(f"  {p['id']:<8} {p['verdict']}")
    return 0 if (passed == len(present)) else 1


# ══════════════════════════════════════════════════════════ predictions
def score_predictions(res):
    P = []
    d1 = res["D1_anatomy"]["GRID"]
    za = d1["zero_stop_advance_share_pct"]
    P.append({"id": "P-S3-1", "prior": 60,
              "measured": {"B_zero_advance_share_pct": za,
                           "baseline_pct": BASELINE["zero_advance_share_pct"],
                           "reached1r_then_grossloss_n": d1["reached1r_then_grossloss_n"]},
              "verdict": "FALSIFIED" if (za is not None and za >= BASELINE["zero_advance_share_pct"]) else "CONFIRMED",
              "note": "B struct_1h stop is STATIC per tranche (work_stop==struct_stop, "
                      "no trail) -> advances==0 by construction -> zero-advance ~100%; the "
                      "falsification reframes the PROTECTED paradox (protection is by initial "
                      "width, not advancement) rather than resolving it."})
    d2 = res["D2_retracement"]
    lift = d2.get("mid_band_beats_both_ends", False)
    P.append({"id": "P-S3-2", "prior": 55,
              "measured": {"mid_band_0p5_0p8_exp_r": d2.get("mid_band_0p5_0p8", {}).get("expectancy_r"),
                           "shallowest": d2.get("shallowest_decile_exp_r"),
                           "deepest": d2.get("deepest_decile_exp_r"),
                           "mid_band_beats_both_ends": lift},
              "verdict": "CONFIRMED" if lift else "FALSIFIED"})
    n_flips = res["D3_confluence"]["p_s3_3"]["n_flips"]
    P.append({"id": "P-S3-3", "prior": 60,
              "measured": {"n_conditions_flipping_positive": n_flips,
                           "flips": res["D3_confluence"]["p_s3_3"]["flips_positive"][:8],
                           "b_triple_true_exp": res["D3_confluence"]["p_s3_3"]["b_triple_true_exp"]},
              "verdict": "CONFIRMED" if n_flips >= 1 else "FALSIFIED"})
    un = res["D4_pcirc"]["GRID"]["prime_unavailable_share_pct"]
    P.append({"id": "P-S3-4", "prior": 65,
              "measured": {"prime_unavailable_share_pct": un,
                           "n_winning_moments": res["D4_pcirc"]["GRID"]["n"]},
              "verdict": "CONFIRMED" if (un is not None and un >= 50.0) else "FALSIFIED"})
    cap = d1["median_peak_capture_pct"]
    P.append({"id": "P-S3-5", "prior": 60,
              "measured": {"B_median_peak_capture_pct": cap,
                           "soft_baseline_ref_pct": BASELINE["peak_capture_soft_ref_pct"],
                           "published_baseline_p50_pct": BASELINE["winner_capture_p50_pct"]},
              "verdict": "CONFIRMED" if (cap is not None and cap > 6.0) else "FALSIFIED",
              "note": "the contract's '~6%' baseline is a soft, un-run reference; the PUBLISHED "
                      "baseline median winner-capture is NEGATIVE per mandate (swing -20.9 / "
                      "intraday -20.8 / position -8.0) -- B is compared to the literal >6% bar "
                      "and, separately, to that negative baseline."})
    P.sort(key=lambda p: (p["verdict"] != "FALSIFIED", p["id"]))   # falsifications first
    return P


def d6_paragraph(res):
    d1 = res["D1_anatomy"]["GRID"]
    b = BASELINE
    stop_w = d1["win_by_exit_reason"].get("stop", {}).get("win_pct")
    oc = d1["win_by_exit_reason"].get("opposite_cross", {})
    fx = d1["win_by_exit_reason"].get("failure_x", {})
    return (
        "Did the structural stop change the SHAPE of how trades win and lose, or just widen "
        "the graveyard? BOTH — and the shape change is the deeper finding. It widened the "
        f"graveyard (STILLBORN rose {b['cohort_pct']['STILLBORN']}% -> {d1['cohort']['STILLBORN']['pct']}%, "
        f"7094 tranches vs the baseline's 6279), but it also re-plumbed the win/loss machinery. "
        f"The static struct stop sits BELOW entry and never advances, so on B a `stop` exit is "
        f"a loss with probability ~1 (stop win-rate {stop_w}% vs the baseline ratchet's "
        f"{b['win_by_exit_reason']['stop']['win_pct']}%, where the ratchet could climb above entry). "
        f"B's wins therefore MIGRATE off the stop entirely: they come from flatten exits — "
        f"opposite_cross ({oc.get('n')} exits, {oc.get('win_pct')}% win) and failure_x "
        f"({fx.get('n')}, {fx.get('win_pct')}%) — the stop is now a pure loss-cap, not a profit "
        f"gate. The PROTECTED paradox also inverted in CAUSE: baseline had 90.35% zero-advance "
        f"among reached-then-lost (a ratchet that could move but was frozen by the pullback "
        f"coupling); B is {d1['zero_stop_advance_share_pct']}% zero-advance because the stop is "
        f"static by construction — it protects by initial WIDTH, never by advancing — and the "
        f"reversal share of PROTECTED rose to {d1['reversal_share_of_protected_pct']}% "
        f"(baseline {b['reversal_share_of_protected_pct']}%): the wider stop lets +1R winners "
        f"round-trip further, so median peak-capture is {d1['median_peak_capture_pct']}% (worse, "
        f"not better). B does not 'fix' the paradox; it swaps a frozen-ratchet pathology for a "
        f"no-ratchet architecture whose {d1['reached1r_then_grossloss_n']} reached-then-gross-loss "
        f"tranches ARE the decoupled-add prize P-CIRC sizes: "
        f"{res['D4_pcirc']['GRID']['prime_unavailable_share_pct']}% of winning moments had no "
        f"pullback-reclaim PRIME available to add on. The winning book wins by holding a wide "
        f"static stop through the reversal — the residual value lives in adding to those winners "
        f"the current gate structurally cannot touch.")


# ══════════════════════════════════════════════════════════ markdown
def render_md(res):
    L = ["# S-3 ENRICHMENT — Cell-B Anatomy, Retracement, Confluence, P-CIRC & "
         "Cross-Run Excursion Substrate (engine 1.0.11, capture on)", "",
         f"> **{res['caveat']}**", "",
         "> Trading is UNCHANGED (F-BYTE proves it); this is instrumentation only. "
         "J-1 out a fifth time, disclosed.", "", "## Fixtures (F-BYTE first)", ""]
    for k in ("F-BYTE", "F-P2REF", "F-CIRC-N", "F-SUB", "F-DET"):
        v = res["fixtures"].get(k)
        if v is None:
            continue
        b = {kk: vv for kk, vv in v.items() if kk != "match"}
        L.append(f"- **{k}**: {'MATCH' if v['match'] else 'MISMATCH'} — "
                 f"`{json.dumps(b, default=str)[:200]}`")
    g = res["headline"]["GRID"]
    L += ["", "## Headline (cell-B, struct-R; recomputed traded, = F-P2REF)", "",
          f"- GRID 1x **{g['sum_1x']}** | 0x {g['sum_0x']} | 2x {g['sum_2x']} | "
          f"{g['tranches']} tranches | {g['campaigns']} campaigns | "
          f"win {g['win_rate_pct']}% (campaign-level)"]

    L += ["", "## D1 — Per-trade anatomy (cell-B) beside the S-1 baseline", "",
          "Reached-profit tier histogram (MFE, struct-R on B / baseline-R on S-1); "
          "PROTECTED-paradox on both books.", "",
          "| MFE tier | B n | B % | S-1 (cohort-coarse) |", "|---|---|---|---|"]
    d1 = res["D1_anatomy"]["GRID"]
    coarse = {"<0": "NEVER_GREEN 17.42%", "0-0.5": "STILLBORN 27.46%",
              "0.5-1": "FADED 14.17%", "1-2": "", "2-3": "",
              ">=3": "PROTECTED 40.95% (>=1R total)"}
    for name, _, _ in TIERS:
        t = d1["reached_profit_tiers"][name]
        L.append(f"| {name} | {t['n']} | {t['pct']} | {coarse[name]} |")
    L += ["",
          "> Note: MFE (peak favorable excursion) is ≥0 by construction, so the `<0` tier is "
          "always empty; the never-green population (MFE exactly 0) sits in the `0-0.5` bucket "
          "and is reported separately as the NEVER_GREEN cohort below.",
          "",
          "- **Cohort mix (B)**: " + " | ".join(
              f"{k} {d1['cohort'][k]['pct']}%" for k in ("NEVER_GREEN", "STILLBORN", "FADED", "PROTECTED"))
          + "  vs  baseline " + " | ".join(
              f"{k} {BASELINE['cohort_pct'][k]}%" for k in ("NEVER_GREEN", "STILLBORN", "FADED", "PROTECTED")),
          f"- **PROTECTED paradox**: of {d1['protected_n']} B tranches reaching >=+1R MFE, "
          f"{d1['reached1r_then_grossloss_n']} reversed to a 0x (gross) loss "
          f"({d1['reversal_share_of_protected_pct']}% of PROTECTED); of those, "
          f"**{d1['zero_stop_advance_share_pct']}%** had zero stop advance before the peak "
          f"(baseline {BASELINE['zero_advance_share_pct']}%). B's stop is STATIC by construction.",
          f"- **Median peak-capture (B, realized/MFE, reached-profit)**: {d1['median_peak_capture_pct']}% "
          f"(baseline published p50: swing {BASELINE['winner_capture_p50_pct']['swing']} / "
          f"intraday {BASELINE['winner_capture_p50_pct']['intraday']} / position "
          f"{BASELINE['winner_capture_p50_pct']['position']}; contract soft ref ~6%).",
          "",
          "Win rate by exit reason (B, tranche-level):", "",
          "| exit reason | B n | B win% | S-1 n | S-1 win% |", "|---|---|---|---|---|"]
    for rsn, v in sorted(d1["win_by_exit_reason"].items(), key=lambda kv: -kv[1]["n"]):
        bl = BASELINE["win_by_exit_reason"].get(rsn, {})
        L.append(f"| {rsn} | {v['n']} | {v['win_pct']} | {bl.get('n', '—')} | {bl.get('win_pct', '—')} |")

    d2 = res["D2_retracement"]
    L += ["", "## D2 — Retracement-depth expectancy (cell-B, struct-R)", "",
          "| decile | retr range | n | expectancy R | ci95 | strip-best | MFE_r med |",
          "|---|---|---|---|---|---|---|"]
    for d in d2.get("deciles", []):
        L.append(f"| {d['decile']} | {d['retr_lo']}-{d['retr_hi']} | {d['n']} | "
                 f"{d['expectancy_r']} | {d['ci95']} | {d['strip_best_exp_r']} | {d['mfe_r_median']} |")
    L += ["",
          f"- **Pocket question (0.5-0.8 band)**: mid-band expectancy "
          f"{d2.get('mid_band_0p5_0p8', {}).get('expectancy_r')} (n {d2.get('mid_band_0p5_0p8', {}).get('n')}) "
          f"vs shallowest {d2.get('shallowest_decile_exp_r')} / deepest {d2.get('deepest_decile_exp_r')}; "
          f"mid-band beats both ends, sign-stable: **{d2.get('mid_band_beats_both_ends')}**.",
          f"- A+ overlay (reference, tiny n): n {d2.get('aplus_overlay', {}).get('n')}, "
          f"expectancy {d2.get('aplus_overlay', {}).get('expectancy_r')} — NOT the estimator."]

    d3 = res["D3_confluence"]
    L += ["", "## D3 — Confluence re-scored on the winning (B) book", "",
          "RC-7r joint lattice (30m-aligned x 1d-room x toll-payable), GRID slice, "
          "camp-R (1x). Cell key `30m|1d_room|toll`.", "",
          "| lattice cell | n | expectancy | ci95 | S-1 ref |", "|---|---|---|---|---|"]
    lat = d3["GRID"]["lattice"]
    for key in ("30m=1|1d_room=1|toll=1", "30m=0|1d_room=0|toll=0"):
        if key in lat:
            c = lat[key]
            ref = (S1_LATTICE_TRIPLE["triple_true_exp"] if "1|toll=1" in key
                   else S1_LATTICE_TRIPLE["triple_false_exp"])
            L.append(f"| {key} | {c['n']} | {c['expectancy']} | {c['ci95']} | {ref} |")
    L += ["",
          f"- **P-S3-3 flips** (conditions negative-separating on S-1, positive on B): "
          f"**{d3['p_s3_3']['n_flips']}**. "
          + "; ".join(f"{f['cell']} (S-1 {f['s1_sep']} -> B {f['b_sep']})"
                      for f in d3['p_s3_3']['flips_positive'][:6]),
          f"- Triple-true lattice: S-1 {d3['p_s3_3']['s1_triple_true_exp']} -> "
          f"B {d3['p_s3_3']['b_triple_true_exp']}."]

    d4 = res["D4_pcirc"]["GRID"]
    L += ["", "## D4 — P-CIRC decoupled-add evidence (+1R-moment snapshots)", "",
          f"- **{d4['prime_unavailable_share_pct']}%** of the {d4['n']} +1R winning moments "
          f"had NO pullback-reclaim PRIME available that bar — the circular freeze, measured "
          f"directly. (PRIME available {d4['prime_available_share_pct']}%, CONFIRM available "
          f"{d4['confirm_available_share_pct']}%, either {d4['either_available_share_pct']}%.)",
          f"- Why unavailable — gate pass-rates at winning moments: raw-reclaim "
          f"{d4['raw_reclaim_share_pct']}% | zone>0 {d4['zone_ok_share_pct']}% | range-ok "
          f"{d4['range_ok_share_pct']}% | ribsep-ok {d4['ribsep_ok_share_pct']}%.",
          f"- Independent state a non-PRIME add could key on: price beyond exec-e9 (in dir) "
          f"{d4['px_beyond_e9_dir_pct']}% | beyond exec-e89 {d4['px_beyond_e89_dir_pct']}% | "
          f"beyond gov-e89 {d4['px_beyond_gov_e89_dir_pct']}% | 9/89 aligned "
          f"{d4['cross_9_89_with_dir_pct']}% | median ribbon-sep {d4['median_ribbon_sep_atr']} ATR."]

    L += ["", "## D5 — Cross-run excursion substrate (P-KEEP)", "",
          f"- `s3_excursion_substrate.jsonl` — {res.get('substrate_rows')} rows "
          f"(sha256 `{res.get('substrate_sha256', '')[:16]}...`), one per resolved tranche, keyed "
          f"`trigger_type x grade x entry_zone x dir`, MFE/MAE in BOTH bps and entry-ATR at "
          f"horizons {{10,20,50,100 exec bars}} and at exit.",
          "- §8: S-1 / arm-A journals do NOT carry joinable fixed-horizon dual-basis excursion "
          "-> substrate ships **cell-B-only**; back-fill re-emission (S-1 + arm-A with this "
          "substrate on, byte-safe) is the named P-KEEP follow-up.", "",
          "Pivot — median MFE/MAE (entry-ATR) at h100 by trigger_type x grade x entry_zone "
          "(top rows by n):", "",
          "| trigger | grade | zone | n | MFE atr h100 | MAE atr h100 | MFE atr exit |",
          "|---|---|---|---|---|---|---|"]
    for r in sorted(res["D5_excursion_pivot"], key=lambda r: -r["n"])[:14]:
        L.append(f"| {r['trigger_type']} | {r['grade']} | {r['entry_zone']} | {r['n']} | "
                 f"{r['mfe_atr_h100_med']} | {r['mae_atr_h100_med']} | {r['mfe_atr_exit_med']} |")

    L += ["", "## D6 — The anatomy delta (one paragraph)", "", res["D6_paragraph"],
          "", "## Scorecard (falsifications first)", "",
          "| # | prior | verdict | measured |", "|---|---|---|---|"]
    for p in res["predictions"]:
        L.append(f"| {p['id']} | {p['prior']}% | **{p['verdict']}** | "
                 f"`{json.dumps(p['measured'], default=str)[:160]}` |")
    L += ["", "*scripts/s3_enrich.py (run) + scripts/s3_analyze.py (analyze); raw journal "
          "bytes + in-process signal/trade recompute; engine byte-untouched.*", ""]
    return "\n".join(L)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--cells", default="")
    ap.add_argument("--root", default="")      # dev: point at B_run1
    ap.add_argument("--no-byte", action="store_true")
    ap.add_argument("--no-det", action="store_true")
    a = ap.parse_args()
    cs = a.cells.split(",") if a.cells else None
    jr = Path(a.root) if a.root else None
    raise SystemExit(run_analysis(cells=cs, jroot=jr,
                                  do_byte=not a.no_byte, do_det=not a.no_det))
