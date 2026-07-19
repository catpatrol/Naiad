"""RC-7r — Post-S-1 Recompute, re-scoped (Tier A: journals + sidecars).

Contract: RC7_PostS1_Recompute_Builder_Contract.md as amended by
RC7_Amendment_1.md and RE-SCOPED by RC7_Amendment_2.md after two F3-family
halts (simulator bar-event ordering != engine wake order; three faces, one
defect). RC-7r delivers the simulator-independent tables only: R7-2..R7-11,
fixtures F1/F2/F4-F8, predictions P-STRIP/P-LAT/P-FH1..4/P-PRVW (verbatim,
unseen). Retired to S-2 carrying verbatim-unseen: R7-1' (two-line pricing),
R7-12' (fill-bar bias), P-2L-a/b/c. Read-only arithmetic over
research_outputs/s1/ (engine 1.0.9 run, verified PASS). No engine
execution, no config change, no network, no evidence spend.

Standing caveats printed on every table: IN-SAMPLE · FIRST-ORDER (re-weights
and counterfactual exits ignore rail/halt/equity-path feedback; a really-
adopted rule changes the trade set) · RANKS ONLY, Tier-C validates · cost
PROXY on counterfactual legs (journaled cost/one_r; funding understated on
long holds) · JTO/TAO 1d rows seed-biased -> flagged, excluded from 1d
aggregates · intraday-era caveat (five long-history intraday cells floor out
2022-2023).

Usage: python scripts/rc7_recompute.py
"""
from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
S1J = ROOT / "research_outputs" / "s1" / "journal_s1" / "scored"
S1E = ROOT / "research_outputs" / "s1" / "s1_events"
MANIFEST = ROOT / "research_outputs" / "s1" / "manifest.json"

SEED = 20260720
N_BOOT = 10_000
STEP = {"intraday": 60_000, "swing": 300_000, "position": 900_000}
GOV_MS = {"intraday": 3_600_000, "swing": 14_400_000, "position": 43_200_000}
SLIP = {"BTCUSDT": 2.0, "ETHUSDT": 2.0, "SOLUSDT": 5.0, "NEARUSDT": 5.0,
        "ZECUSDT": 5.0, "JTOUSDT": 5.0, "TAOUSDT": 5.0}
SEED_BIASED = {"JTOUSDT", "TAOUSDT"}          # 1d rows: flag + exclude
LADDER = ["exec", "15m", "30m", "1h", "4h", "12h", "1d"]
GOV_IDX = {"swing": 4, "intraday": 3, "position": 5}
# Trail candidates referenced by R7-11's adds-funnel dual print (fold-in
# journal columns; NOT two-line pricing — that is retired to S-2/R7-1').
TRAIL_CANDS = ["ema200_gov_b0.5", "ema200_gov_b0.0", "ema89_gov_b0.0"]
R72_CAVEAT = ("fold-in pinned-convention numbers; known bar-ordering "
              "infidelity (721-tranche fill-bar class + death-bar class, "
              "quantification deferred to S-2); valid for the concentration "
              "question only - not a TC-1 prediction basis.")
CONF_TIERS = {0: 0.5, 1: 1.0, 2: 1.5, 3: 2.0}   # registered, not fitted
MANDATES = ["swing", "intraday", "position"]
F1_REF = (-1796.9930, 275.9924, 2599, 10.8503)
F2_REF = {"reentry_ab": 69_395, "add_trigger": 29_270, "mtf_cross": 5_267,
          "v_shadow": 3_978}
F4_REF = (-0.549, -0.939, 1650, 949)
F5_REF = {"r1": 2456, "true_add": 888, "re_entry": 2928, "v": 32}
F6_REF = 90.35
CAVEAT = ("IN-SAMPLE / FIRST-ORDER / RANKS-ONLY - Tier-C validates. "
          "Counterfactual legs use the journaled cost/one_r proxy "
          "(funding understated on long holds). JTO/TAO 1d rows are "
          "seed-biased: flagged, excluded from 1d aggregates. The five "
          "long-history intraday cells floor out 2022-2023.")


def r4(x):
    return None if x is None else round(float(x) + 0.0, 4)


def med(vals):
    vals = [v for v in vals if v is not None]
    return r4(float(np.median(vals))) if vals else None


def q(vals, p):
    vals = [v for v in vals if v is not None]
    return r4(float(np.percentile(vals, p))) if vals else None


def pct(x, d):
    return None if not d else r4(100.0 * x / d)


def boot_ci(vals, seed=SEED, n=N_BOOT):
    a = np.asarray([v for v in vals if v is not None], dtype=float)
    if a.size < 2:
        return (None, None)
    rng = np.random.default_rng(seed)
    means = np.empty(n)
    for s in range(0, n, 1000):
        k = min(1000, n - s)
        idx = rng.integers(0, a.size, size=(k, a.size))
        means[s:s + k] = a[idx].mean(axis=1)
    return (r4(np.percentile(means, 2.5)), r4(np.percentile(means, 97.5)))


def ms_of(ts):
    return int(datetime.fromisoformat(ts.replace("Z", "+00:00"))
               .timestamp() * 1000)


def mandate_of(cell):
    return cell.rpartition("_")[2]


def steps_of(tf, mandate):
    return LADDER.index(tf) - GOV_IDX[mandate]


# ─────────────────────────────────────────────────────────────── load
def load():
    cells = sorted(p.name for p in S1J.iterdir() if p.is_dir())
    fills, exits = [], []
    sigstats = {c: {"evt": Counter(), "retr": [], "depth": []}
                for c in cells}
    for cell in cells:
        for p in sorted((S1J / cell).glob("*.jsonl")):
            for line in open(p, encoding="utf-8"):
                if not line.strip():
                    continue
                r = json.loads(line)
                evt = r["evt"]
                sigstats[cell]["evt"][evt] += 1
                if evt == "PRIME":
                    if r["retr"] is not None:
                        sigstats[cell]["retr"].append(r["retr"])
                    if (r["px_signal"] and r["stop"] and r["atr_gov"]
                            and r["atr_gov"] > 0):
                        sigstats[cell]["depth"].append(
                            abs(r["px_signal"] - r["stop"]) / r["atr_gov"])
                if evt in ("ENTRY_FILL", "ADD_FILL"):
                    s1 = r["s1"]
                    fills.append({
                        "cell": cell, "mandate": mandate_of(cell),
                        "asset": cell.rpartition("_")[0],
                        "tid": r["tranche_id"], "ts": r["ts_open"],
                        "dir": 1 if r["dir"] == "long" else -1,
                        "zone": r["zone"] or "-", "grade": r["grade"],
                        "size_r": r["size_r"], "fill_class": r["fill_class"],
                        "px_fill": r["px_fill"], "stop": r["stop"],
                        "qty": r["qty"], "rc": r["rc"],
                        "ef": s1["entryflags"], "cluster": s1["cluster"],
                    })
                elif evt == "EXIT":
                    s1 = r["s1"]
                    cost = (r["fees"] or 0) + (r["funding_cum"] or 0) + \
                        (r["slippage"] or 0)
                    exits.append({
                        "cell": cell, "mandate": mandate_of(cell),
                        "asset": cell.rpartition("_")[0],
                        "tid": r["tranche_id"], "ts": r["ts_open"],
                        "dir": 1 if r["dir"] == "long" else -1,
                        "realized_r": r["realized_r"], "size_r": r["size_r"],
                        "cost": cost, "mfe_r": r["mfe_r"],
                        "mae_r": r["mae_r"], "cohort": r["cohort"],
                        "reason": r["exit_reason"],
                        "px_exit": r["px_fill"], "stop_raw": r["stop"],
                        "ratchet": s1["ratchet"], "advance": s1["advance"],
                        "mtf": s1["mtf"], "deadgate": s1["deadgate"],
                    })
    crosses = []
    fam_counts = Counter()
    for cell in cells:
        for line in open(S1E / f"{cell}.jsonl", encoding="utf-8"):
            r = json.loads(line)
            fam_counts[r["family"]] += 1
            if r["family"] == "mtf_cross":
                crosses.append(r)
    return cells, fills, exits, sigstats, crosses, fam_counts


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    cells, fills, exits, sigstats, crosses, fam_counts = load()
    fill_by = {(f["cell"], f["tid"]): f for f in fills}

    # joins + derived per-tranche fields
    for e in exits:
        f = fill_by[(e["cell"], e["tid"])]
        e["f"] = f
        e["unit"] = abs(f["px_fill"] - f["stop"])
        e["one_r"] = e["unit"] * f["qty"] / f["size_r"]
        e["cost_r"] = e["cost"] / e["one_r"]
        e["unit_1x"] = e["realized_r"] / e["size_r"]
        e["r_0x"] = e["realized_r"] + e["cost_r"]
        e["base_off"] = (ms_of(e["ts"]) - ms_of(f["ts"])) \
            // STEP[e["mandate"]]
        slip = SLIP[e["asset"]] / 1e4
        if e["reason"] in ("stop", "stop_gap") and e["stop_raw"]:
            raw = e["stop_raw"]
        else:
            raw = e["px_exit"] / ((1 - slip) if e["dir"] == 1 else (1 + slip))
        e["base_gross_unit"] = (raw - f["px_fill"]) * e["dir"] / e["unit"]
        e["camp"] = (e["cell"], int(e["tid"][1:].split("t")[0]))
    camp_exits = defaultdict(list)
    for e in exits:
        camp_exits[e["camp"]].append(e)
    camps = sorted(camp_exits)
    for c in camps:
        camp_exits[c].sort(key=lambda e: int(e["tid"].split("t")[1]))
    camp_r = {c: sum(e["realized_r"] for e in camp_exits[c]) for c in camps}
    openers = {c: camp_exits[c][0] for c in camps}

    # campaign condition flags (opener-attributed)
    def beyond(e, tf, ema):
        v = e["mtf"].get(tf, {}).get(f"entry_d{ema}")
        return None if v is None else v * e["dir"] > 0
    for c in camps:
        o = openers[c]
        of = o["f"]
        o["c30"] = bool(o["mtf"]["30m"]["s2_aligned_entry"])
        b = beyond(o, "1d", "200")
        o["c1d"] = (None if o["asset"] in SEED_BIASED or b is None
                    else (not b))
        o["ctoll"] = bool(of["ef"]["stop_dist_bps"]
                          >= 2.0 * of["ef"]["roundtrip_cost_bps"])

    fixtures = {}
    # F1
    n_c = len(camps)
    win = sum(1 for c in camps if camp_r[c] > 0)
    s1x = sum(camp_r.values())
    s0x = sum(e["r_0x"] for e in exits)
    fixtures["F1"] = {
        "sum_1x": r4(s1x), "sum_0x": r4(s0x), "campaigns": n_c,
        "win_rate_pct": pct(win, n_c),
        "match": (abs(s1x - F1_REF[0]) < 1e-3 and abs(s0x - F1_REF[1]) < 1e-3
                  and n_c == F1_REF[2]
                  and abs(pct(win, n_c) - F1_REF[3]) < 1e-3)}
    # F2
    fixtures["F2"] = {"counts": dict(fam_counts),
                      "match": all(fam_counts[k] == v
                                   for k, v in F2_REF.items())}
    # F3 family RETIRED to S-2 (Amendment 2). Standing descriptive line only.
    fill_bar_n = sum(1 for e in exits if e["base_off"] == 0)
    standing_line = (f"{fill_bar_n} of {len(exits)} fills "
                     f"({pct(fill_bar_n, len(exits))}%) exit on the bar "
                     "they are born")
    # F4 — 30m marginal via lattice rows (incl. the 1d-void stratum)
    t = [camp_r[c] for c in camps if openers[c]["c30"]]
    fnc = [camp_r[c] for c in camps if not openers[c]["c30"]]
    fixtures["F4"] = {
        "aligned": {"n": len(t), "exp": r4(np.mean(t))},
        "not_aligned": {"n": len(fnc), "exp": r4(np.mean(fnc))},
        "match": (len(t) == F4_REF[2] and len(fnc) == F4_REF[3]
                  and abs(np.mean(t) - F4_REF[0]) < 5e-4
                  and abs(np.mean(fnc) - F4_REF[1]) < 5e-4)}
    # F5
    census = Counter(f["fill_class"] for f in fills)
    fixtures["F5"] = {"census": dict(census),
                      "match": all(census[k] == v for k, v in F5_REF.items())}
    # F6
    pop = [e for e in exits if e["mfe_r"] is not None and e["mfe_r"] >= 1.0
           and e["r_0x"] < 0]
    za = [e for e in pop if e["advance"]["advances_before_mfe"] == 0]
    share = pct(len(za), len(pop))
    grid_za = pct(sum(1 for e in exits
                      if e["advance"]["n_stop_advances"] == 0), len(exits))
    fixtures["F6"] = {"share_pct": share, "grid_zero_advance_pct": grid_za,
                      "match": share is not None
                      and abs(share - F6_REF) <= 0.01}
    # F7 placeholder (filled after the matrix builds)
    # F8 handled by double execution (hashes printed by the runner harness)

    # ─────────────────────────────────── R7-2 per-candidate strip-best
    strip = {}
    all_cands = sorted(exits[0]["ratchet"].keys())
    for cid in all_cands:
        row = {}
        for m in ["position"] + [x for x in MANDATES if x != "position"] \
                + ["GRID"]:
            sel = [e for e in exits if m == "GRID" or e["mandate"] == m]
            cp = defaultdict(float)
            for e in sel:
                v = e["ratchet"][cid]["exit_r"]
                if v is not None:
                    cp[e["camp"]] += v * e["size_r"] - e["cost_r"]
            vals = [cp[c] for c in sorted(cp)]
            s = sum(vals)
            row[m] = {"sum_1x_proxy": r4(s),
                      "strip_best": r4(s - max(vals)) if vals else None,
                      "best_campaign": r4(max(vals)) if vals else None}
        strip[cid] = row

    # ─────────────────────────────────── R7-3 confluence matrix (+F7)
    conds = {"s2_aligned": lambda e, tf: e["mtf"][tf]["s2_aligned_entry"],
             "beyond_e200": lambda e, tf: beyond(e, tf, "200"),
             "beyond_e89": lambda e, tf: beyond(e, tf, "89")}
    matrix = []
    for tf in LADDER:
        for cname, fn in conds.items():
            pooled_t, pooled_f = [], []
            for m in MANDATES:
                sel = [c for c in camps if openers[c]["mandate"] == m]
                if tf == "1d":
                    excl = [c for c in sel
                            if openers[c]["asset"] in SEED_BIASED]
                    sel = [c for c in sel
                           if openers[c]["asset"] not in SEED_BIASED]
                else:
                    excl = []
                tvals, fvals = [], []
                for c in sel:
                    v = fn(openers[c], tf)
                    if v is None:
                        continue
                    (tvals if v else fvals).append(camp_r[c])
                pooled_t += tvals
                pooled_f += fvals
                matrix.append({
                    "tf": tf, "steps_from_governor": steps_of(tf, m),
                    "condition": cname, "mandate": m,
                    "n_true": len(tvals), "n_false": len(fvals),
                    "exp_true": r4(np.mean(tvals)) if tvals else None,
                    "exp_false": r4(np.mean(fvals)) if fvals else None,
                    "separation_r": r4(np.mean(tvals) - np.mean(fvals))
                    if tvals and fvals else None,
                    "excluded_seed_biased": len(excl),
                })
            matrix.append({
                "tf": tf, "steps_from_governor": "per-mandate",
                "condition": cname, "mandate": "POOLED",
                "n_true": len(pooled_t), "n_false": len(pooled_f),
                "exp_true": r4(np.mean(pooled_t)) if pooled_t else None,
                "exp_false": r4(np.mean(pooled_f)) if pooled_f else None,
                "separation_r": r4(np.mean(pooled_t) - np.mean(pooled_f))
                if pooled_t and pooled_f else None,
                "excluded_seed_biased": None,
            })
    # JTO/TAO 1d rows, separate + flagged
    jt_1d = []
    for cname, fn in conds.items():
        for m in MANDATES:
            sel = [c for c in camps if openers[c]["mandate"] == m
                   and openers[c]["asset"] in SEED_BIASED]
            tvals = [camp_r[c] for c in sel
                     if fn(openers[c], "1d") is True]
            fvals = [camp_r[c] for c in sel
                     if fn(openers[c], "1d") is False]
            jt_1d.append({"flag": "seed_biased", "tf": "1d",
                          "condition": cname, "mandate": m,
                          "n_true": len(tvals), "n_false": len(fvals),
                          "exp_true": r4(np.mean(tvals)) if tvals else None,
                          "exp_false": r4(np.mean(fvals)) if fvals else None})
    mand_rows = [r for r in matrix if r["mandate"] in MANDATES]
    fixtures["F7"] = {
        "mandate_rows": len(mand_rows), "expected": 7 * 3 * 3,
        "dual_coordinates": all("steps_from_governor" in r and "tf" in r
                                for r in matrix),
        "match": len(mand_rows) == 63
        and all("steps_from_governor" in r for r in matrix)}

    # ─────────────────────────────────── R7-4 FH-3 discriminator
    peaks = {}
    for m in MANDATES:
        best_tf, best_sep = None, None
        for r in mand_rows:
            if r["mandate"] != m or r["condition"] != "s2_aligned":
                continue
            if r["separation_r"] is not None and \
                    (best_sep is None or r["separation_r"] > best_sep):
                best_sep, best_tf = r["separation_r"], r["tf"]
        peaks[m] = {"tf": best_tf, "steps": steps_of(best_tf, m),
                    "separation": best_sep}
    if all(p["tf"] == "30m" for p in peaks.values()):
        fh3 = "ABSOLUTE"
    else:
        st = [p["steps"] for p in peaks.values()]
        pairs_close = sum(1 for i in range(3) for j in range(i + 1, 3)
                          if abs(st[i] - st[j]) <= 1)
        fh3 = "RELATIVE" if pairs_close >= 1 else "MIXED"
    fh3_note = ("precedence: ABSOLUTE (30m in all three) evaluated before "
                "the ±1-step RELATIVE test; RELATIVE = ≥2 of 3 mandate "
                "peaks within ±1 step of each other")

    # ─────────────────────────────────── R7-5 joint lattice
    lattice = {}
    def latt(sel_camps, label):
        rows = {}
        wins_total = sum(max(camp_r[c], 0.0) for c in sel_camps)
        for a in (True, False):
            for b in (True, False, None):
                for t2 in (True, False):
                    key = f"30m={int(a)}|1d_room=" \
                          f"{'void' if b is None else int(b)}|toll={int(t2)}"
                    vs = [camp_r[c] for c in sel_camps
                          if openers[c]["c30"] == a
                          and openers[c]["c1d"] == b
                          and openers[c]["ctoll"] == t2]
                    if not vs and b is None:
                        continue
                    lo, hi = boot_ci(vs)
                    rows[key] = {
                        "n": len(vs), "expectancy": r4(np.mean(vs))
                        if vs else None,
                        "ci95": [lo, hi], "sum": r4(sum(vs)),
                        "share_of_sum_wins_pct":
                            pct(sum(max(v, 0.0) for v in vs), wins_total)
                            if wins_total else None,
                    }
        return rows
    lattice["GRID"] = latt(camps, "GRID")
    for m in MANDATES:
        lattice[m] = latt([c for c in camps
                           if openers[c]["mandate"] == m], m)
    # R1-only companion: opener tranche outcome instead of campaign R
    r1_rows = {}
    for a in (True, False):
        for b in (True, False, None):
            for t2 in (True, False):
                key = f"30m={int(a)}|1d_room=" \
                      f"{'void' if b is None else int(b)}|toll={int(t2)}"
                vs = [openers[c]["realized_r"] / openers[c]["size_r"]
                      for c in camps
                      if openers[c]["c30"] == a and openers[c]["c1d"] == b
                      and openers[c]["ctoll"] == t2]
                if not vs and b is None:
                    continue
                r1_rows[key] = {"n": len(vs),
                                "per_unit_1x": r4(np.mean(vs))
                                if vs else None}
    lattice["R1_only_companion"] = r1_rows

    # ─────────────────────────────────── R7-6 FH-1 signal-shape census
    fh1 = {}
    for m in MANDATES:
        mc = [c for c in cells if mandate_of(c) == m]
        gov_bars = sum(
            (ms_of(manifest["cells"][c]["end"] + ":59Z"
                   if len(manifest["cells"][c]["end"]) == 16
                   else manifest["cells"][c]["end"])
             - ms_of(manifest["cells"][c]["start"] + "T00:00:00Z"))
            // GOV_MS[m] for c in mc)
        evt = Counter()
        retr, depth = [], []
        for c in mc:
            evt += sigstats[c]["evt"]
            retr += sigstats[c]["retr"]
            depth += sigstats[c]["depth"]
        fh1[m] = {
            "gov_bars": gov_bars,
            "per_100_gov_bars": {k: r4(100 * evt[k] / gov_bars)
                                 for k in ("REGIME", "TAG", "PRIME",
                                           "CONFIRM", "V", "TPW", "X",
                                           "CLUSTER")},
            "retr_quantiles_p25_50_75": [q(retr, 25), q(retr, 50),
                                         q(retr, 75)],
            "depth_gov_atr_quantiles_p25_50_75": [q(depth, 25),
                                                  q(depth, 50),
                                                  q(depth, 75)],
        }
    fh1["_definition"] = ("depth proxy = |px_signal - stop| / atr_gov on "
                          "PRIME rows (stop anchors at the signal-bar "
                          "extreme + 0.5 ATR_exec buffer); true zone-band "
                          "depth needs engine columns -> S-2")

    # ─────────────────────────────────── R7-7 FH-2 R-space anatomy
    fh2 = {}
    for m in MANDATES:
        sel = [e for e in exits if e["mandate"] == m]
        mfe = [e["mfe_r"] for e in sel if e["mfe_r"] is not None]
        mae = [e["mae_r"] for e in sel if e["mae_r"] is not None]
        winners = [e for e in sel if e["mfe_r"] is not None
                   and e["mfe_r"] >= 1.0]
        caps = [e["unit_1x"] / e["mfe_r"] for e in winners]
        fh2[m] = {
            "n": len(sel),
            "mfe_deciles": [q(mfe, p) for p in range(10, 100, 10)],
            "mae_deciles": [q(mae, p) for p in range(10, 100, 10)],
            "protected_share_pct": pct(
                sum(1 for e in sel if e["cohort"] == "PROTECTED"), len(sel)),
            "winner_capture_p25_50_75": [q(caps, 25), q(caps, 50),
                                         q(caps, 75)],
        }

    # ─────────────────────────────────── R7-8 FH-4 nesting census
    intervals = defaultdict(list)   # (asset, mandate, dir) -> [(t0, t1)]
    for c in camps:
        es = camp_exits[c]
        t0 = min(ms_of(e["f"]["ts"]) for e in es)
        t1 = max(ms_of(e["ts"]) for e in es)
        intervals[(es[0]["asset"], es[0]["mandate"], es[0]["dir"])] \
            .append((t0, t1))
    def active_at(asset, mand, d, t):
        return any(a <= t <= b for a, b in intervals[(asset, mand, d)])
    def active_span(asset, mand, d):
        iv = sorted(intervals[(asset, mand, d)])
        merged, total = [], 0
        for a, b in iv:
            if merged and a <= merged[-1][1]:
                merged[-1] = (merged[-1][0], max(merged[-1][1], b))
            else:
                merged.append((a, b))
        return merged, sum(b - a for a, b in merged)
    def nest(hi_m, lo_m):
        per_asset = {}
        obs_n = obs_hit = 0
        exp_sum = 0.0
        with_r, without_r = [], []
        for asset in sorted({c[0] for c in
                             {(openers[c]["asset"],) for c in camps}}):
            lo_all = sorted(sum((intervals[(asset, lo_m, d)]
                                 for d in (1, -1)), []))
            if not lo_all:
                continue
            lo_end = max(b for _, b in lo_all)
            lo_start = min(a for a, _ in lo_all)
            births = [c for c in camps
                      if openers[c]["asset"] == asset
                      and openers[c]["mandate"] == hi_m
                      and lo_start <= ms_of(openers[c]["f"]["ts"])
                      <= lo_end]
            hits = 0
            for c in births:
                t = ms_of(openers[c]["f"]["ts"])
                d = openers[c]["dir"]
                on = active_at(asset, lo_m, d, t)
                if on:
                    hits += 1
                    with_r.append(camp_r[c])
                else:
                    without_r.append(camp_r[c])
                _, dur = active_span(asset, lo_m, d)
                exp_sum += dur / (lo_end - lo_start) \
                    if lo_end > lo_start else 0.0
            obs_n += len(births)
            obs_hit += hits
            per_asset[asset] = {"births_in_overlap": len(births),
                                "same_dir_active": hits}
        enrich = (obs_hit / exp_sum) if exp_sum > 0 else None
        return {
            "births_in_overlap_era": obs_n,
            "same_dir_active_at_birth": obs_hit,
            "observed_rate_pct": pct(obs_hit, obs_n),
            "expected_rate_pct": pct(exp_sum, obs_n),
            "enrichment_x": r4(enrich),
            "exp_conditioned": r4(np.mean(with_r)) if with_r else None,
            "exp_unconditioned": r4(np.mean(without_r))
            if without_r else None,
            "separation_r": r4(np.mean(with_r) - np.mean(without_r))
            if with_r and without_r else None,
            "per_asset": per_asset,
            "caveat": "same tape - co-movement is not causality; "
                      "overlap era only (intraday cells floor out "
                      "2022-2023)",
        }
    fh4 = {"swing_given_intraday": nest("swing", "intraday"),
           "position_given_swing": nest("position", "swing")}

    # ─────────────────────────────────── R7-9 sizing sweeps
    sweeps = {"mandate_multipliers": [], "confluence_tiers": {}}
    for mi in (0.25, 0.5, 1.0):
        for mp in (1.0, 1.5, 2.0):
            mult = {"swing": 1.0, "intraday": mi, "position": mp}
            tot = sum(camp_r[c] * mult[openers[c]["mandate"]]
                      for c in camps)
            half_adds = sum(
                (sum(e["realized_r"] if e["f"]["fill_class"] in ("r1", "v")
                     else 0.5 * e["realized_r"] for e in camp_exits[c]))
                * mult[openers[c]["mandate"]] for c in camps)
            sweeps["mandate_multipliers"].append({
                "m_intraday": mi, "m_position": mp,
                "grid_1x": r4(tot),
                "grid_1x_adds_x0.5": r4(half_adds)})
    conf_w = {}
    tier_census = Counter()
    tot = per_m = None
    tot = 0.0
    per_m = defaultdict(float)
    for e in exits:
        f = e["f"]
        c30 = bool(e["mtf"]["30m"]["s2_aligned_entry"])
        b = beyond(e, "1d", "200")
        c1d = None if e["asset"] in SEED_BIASED or b is None else (not b)
        ct = bool(f["ef"]["stop_dist_bps"]
                  >= 2.0 * f["ef"]["roundtrip_cost_bps"])
        cnt = int(c30) + int(bool(c1d)) + int(ct)
        w = CONF_TIERS[cnt]
        tier_census[cnt] += 1
        tot += e["realized_r"] * w
        per_m[e["mandate"]] += e["realized_r"] * w
    sweeps["confluence_tiers"] = {
        "tier_census": dict(sorted(tier_census.items())),
        "grid_1x_reweighted": r4(tot),
        "per_mandate": {m: r4(per_m[m]) for m in MANDATES},
        "note": "1d condition VOID (not false) for JTO/TAO -> their max "
                "count is 2; weights registered {0.5,1.0,1.5,2.0}",
    }

    # ─────────────────────────────────── R7-10 trigger previews (PROXY)
    open_iv = defaultdict(list)
    for e in exits:
        open_iv[(e["cell"], e["tid"])] = (ms_of(e["f"]["ts"]),
                                          ms_of(e["ts"]))
    prev = {}
    def flip_rows(tfs, pair, with_trend):
        sel = [r for r in crosses if r["tf"] in tfs and r["pair"] == pair
               and r["with_trend"] == with_trend]
        vals = [r["remaining_life_r"] for r in sel
                if r["remaining_life_r"] is not None]
        by_m = defaultdict(list)
        for r in sel:
            if r["remaining_life_r"] is not None:
                by_m[mandate_of(r["cell_id"])].append(r["remaining_life_r"])
        return {"n": len(sel), "mean_remaining_r": r4(np.mean(vals))
                if vals else None,
                "per_mandate": {m: {"n": len(by_m[m]),
                                    "mean": r4(np.mean(by_m[m]))
                                    if by_m[m] else None,
                                    "steps": [steps_of(t, m) for t in tfs]}
                                for m in MANDATES}}
    prev["30m_flip_with_trend_e9e89"] = flip_rows(["30m"], "e9_e89", True)
    prev["15m30m_flip_with_trend_e9e89"] = flip_rows(["15m", "30m"],
                                                     "e9_e89", True)
    prev["1h_flip_against_e9e89"] = flip_rows(["1h"], "e9_e89", False)
    prev["1h_flip_with_e9e89"] = flip_rows(["1h"], "e9_e89", True)
    prev["_label"] = ("PROXY - a cross is not a test-and-reclaim; "
                      "S-2 F8 measures the real thing")

    # ─────────────────────────────────── R7-11 adds funnel dual print
    sig_adds = []
    for cell in cells:
        step = STEP[mandate_of(cell)]
        opens = sorted((ms_of(e["f"]["ts"]), ms_of(e["ts"]))
                       for e in exits if e["cell"] == cell)
        fills_at = {(ms_of(f["ts"]), f["dir"]): f for f in fills
                    if f["cell"] == cell
                    and f["fill_class"] in ("true_add", "re_entry")}
        for p in sorted((S1J / cell).glob("*.jsonl")):
            for line in open(p, encoding="utf-8"):
                if '"PRIME"' not in line and '"CONFIRM"' not in line \
                        and '"REJECT"' not in line:
                    continue
                r = json.loads(line)
                if r["evt"] == "PRIME":
                    if r["rc"] < 2:
                        continue
                elif r["evt"] == "CONFIRM":
                    if r["grade"] == "C":
                        continue
                elif not (r["evt"] == "REJECT"
                          and str(r["tranche_id"]).startswith("trade_ADD")):
                    continue
                ts = ms_of(r["ts_open"])
                if not any(a <= ts < b for a, b in opens):
                    continue
                d = 1 if r["dir"] == "long" else -1
                if r["evt"] == "REJECT":
                    sig_adds.append(("reject", r["reject_reason"]))
                elif (ts + step, d) in fills_at:
                    sig_adds.append(("filled", "-"))
                else:
                    sig_adds.append(("signal_no_fill", "-"))
    funnel = Counter(k for k, _ in sig_adds)
    rej_reasons = Counter(rr for k, rr in sig_adds if k == "reject")
    funnel_tbl = {
        "while_positioned_add_signal_rows": sum(funnel.values()),
        "filled": funnel["filled"],
        "gate_or_fill_rejected": funnel["reject"],
        "signal_no_fill_row": funnel["signal_no_fill"],
        "reject_reasons": dict(rej_reasons),
        "contract_reference": {"admitted": 984, "rejected": 716,
                               "note": "Report-4 derivation; definitional "
                                       "differences reported, not forced"},
        "per_candidate_adds_would_be_eligible_mean": {
            cid: r4(np.mean([e["ratchet"][cid]["adds_would_be_eligible"]
                             for e in exits
                             if e["ratchet"][cid]["adds_would_be_eligible"]
                             is not None]))
            for cid in TRAIL_CANDS},
        "two_line_column": "== baseline by construction: line 1 IS the "
                           "native ratchet the BE-gate tests against; the "
                           "trail only adds an exit, and an exited tranche "
                           "gates nothing",
    }

    # ─────────────────────────────────── predictions (RC-7r: seven rows)
    preds = {}
    best_pos = max(strip, key=lambda c:
                   strip[c]["position"]["sum_1x_proxy"] or -1e9)
    sb = strip[best_pos]["position"]["strip_best"]
    preds["P-STRIP"] = {"prior": 60, "best_position_candidate": best_pos,
                        "sum_1x_proxy":
                            strip[best_pos]["position"]["sum_1x_proxy"],
                        "strip_best": sb,
                        "verdict": "CONFIRMED" if (sb or -1) > 0
                        else "FALSIFIED"}
    ttt = lattice["GRID"].get("30m=1|1d_room=1|toll=1", {})
    fff = lattice["GRID"].get("30m=0|1d_room=0|toll=0", {})
    sep = (ttt.get("expectancy") - fff.get("expectancy")) \
        if ttt.get("expectancy") is not None \
        and fff.get("expectancy") is not None else None
    lat_sep_ok = sep is not None and sep >= 0.8
    lat_exp_ok = (ttt.get("expectancy") is not None
                  and ttt["expectancy"] >= -0.2)
    preds["P-LAT"] = {
        "prior": 60, "triple_true": ttt, "triple_false": fff,
        "separation": r4(sep),
        "halves": {
            "separation_ge_0.8": f"{'PASS' if lat_sep_ok else 'FAIL'} "
                                 f"({r4(sep)})",
            "triple_true_expectancy_ge_-0.2":
                f"{'PASS' if lat_exp_ok else 'FAIL'} "
                f"({ttt.get('expectancy')})",
        },
        "verdict": "CONFIRMED" if lat_sep_ok and lat_exp_ok
        else "FALSIFIED"}
    def max_shift(key, idx):
        """Max deviation from the cross-mandate mean, in magnitudes —
        sign-safe (retr medians are negative). Mechanization stated in the
        report; the original registration pinned only the 25% bar."""
        vals = [fh1[m][key][idx] for m in MANDATES]
        vals = [v for v in vals if v is not None]
        if len(vals) < 3:
            return None
        mu = float(np.mean(vals))
        if abs(mu) < 1e-12:
            return None
        return r4(100 * max(abs(v - mu) for v in vals) / abs(mu))
    sh_retr = max_shift("retr_quantiles_p25_50_75", 1)
    sh_depth = max_shift("depth_gov_atr_quantiles_p25_50_75", 1)
    preds["P-FH1"] = {
        "prior": 65, "median_shift_retr_pct": sh_retr,
        "median_shift_depth_pct": sh_depth,
        "verdict": "CONFIRMED"
        if all(s is not None and s <= 25 for s in (sh_retr, sh_depth))
        else "FALSIFIED"}
    def fh2_dev(pidx):
        """Same mechanization as P-FH1: max |v - mean| / |mean|."""
        vals = [fh2[m]["mfe_deciles"][pidx] for m in MANDATES]
        if not all(v is not None for v in vals):
            return None
        mu = float(np.mean(vals))
        return r4(100 * max(abs(v - mu) for v in vals) / abs(mu)) \
            if abs(mu) > 1e-12 else None
    d50, d75 = fh2_dev(4), fh2_dev(6)
    preds["P-FH2"] = {
        "prior": 60, "mfe_p50_dev_pct": d50, "mfe_p75_dev_pct": d75,
        "verdict": "CONFIRMED"
        if all(d is not None and d <= 20 for d in (d50, d75))
        else "FALSIFIED"}
    preds["P-FH3"] = {"prior": 55, "verdict_value": fh3, "peaks": peaks,
                      "verdict": "CONFIRMED" if fh3 == "RELATIVE"
                      else "FALSIFIED"}
    sgi = fh4["swing_given_intraday"]
    preds["P-FH4"] = {
        "prior": [75, 55], "enrichment_x": sgi["enrichment_x"],
        "separation_r": sgi["separation_r"],
        "verdict_enrichment": "CONFIRMED"
        if (sgi["enrichment_x"] or 0) >= 2.0 else "FALSIFIED",
        "verdict_separation": "CONFIRMED"
        if (sgi["separation_r"] or -1) >= 0.3 else "FALSIFIED"}
    m1530 = prev["15m30m_flip_with_trend_e9e89"]["mean_remaining_r"]
    sep1h = None
    a1, w1 = (prev["1h_flip_against_e9e89"]["mean_remaining_r"],
              prev["1h_flip_with_e9e89"]["mean_remaining_r"])
    if a1 is not None and w1 is not None:
        sep1h = r4(a1 - w1)
    preds["P-PRVW"] = {
        "prior": [60, 55], "mean_15m30m_with": m1530,
        "sep_1h_against_minus_with": sep1h,
        "verdict_reclaim": "CONFIRMED" if (m1530 or -1) > 0
        else "FALSIFIED",
        "verdict_failure_depth": "CONFIRMED"
        if sep1h is not None and sep1h <= -0.2 else "FALSIFIED"}

    results = {
        "caveat": CAVEAT, "seed": SEED, "n_boot": N_BOOT,
        "basis": "S-1 journals engine 1.0.9; baseline = TC-4 pass2",
        "fixtures": fixtures,
        "R7_2_strip_best": {"caveat_header": R72_CAVEAT,
                            "candidates": strip},
        "R7_3_confluence_matrix": {"rows": matrix,
                                   "jto_tao_1d_seed_biased": jt_1d,
                                   "ladder": LADDER,
                                   "gov_index": GOV_IDX},
        "R7_4_fh3": {"peaks": peaks, "verdict": fh3, "rule_note": fh3_note},
        "R7_5_lattice": lattice,
        "R7_6_fh1": fh1,
        "R7_7_fh2": fh2,
        "R7_8_fh4": fh4,
        "R7_9_sizing": sweeps,
        "R7_10_previews": prev,
        "R7_11_adds_funnel": funnel_tbl,
        "standing_line": standing_line,
        "amendments": "Amendment 1 applied, then Amendment 2 re-scope: "
                      "F3 family, R7-1 and R7-12 retired to S-2 as R7-1'/"
                      "R7-12' with P-2L-a/b/c verbatim-unseen",
        "predictions": preds,
    }
    blob = json.dumps(results, indent=1, sort_keys=True, default=str) + "\n"
    print("== RC-7 fixtures ==")
    ok = 0
    for k in ("F1", "F2", "F4", "F5", "F6", "F7"):
        v = fixtures[k]
        ok += v["match"]
        brief = {kk: vv for kk, vv in v.items()
                 if kk not in ("match", "detail")}
        print(f"{k:<4} {'MATCH' if v['match'] else '*** MISMATCH ***'} "
              f"{json.dumps(brief, default=str)[:200]}")
    if ok < 6:
        print("\n*** HALT: fixture mismatch. Report, deliver nothing. ***")
        return 1
    print("\n" + standing_line)
    (ROOT / "rc7_results.json").write_text(blob, encoding="utf-8",
                                           newline="\n")
    (ROOT / "RC7_RESULTS.md").write_text(render_md(results),
                                         encoding="utf-8", newline="\n")
    print("\n== predictions ==")
    for k, v in preds.items():
        vd = v.get("verdict") or " / ".join(
            f"{kk.split('_', 1)[1]}:{vv}" for kk, vv in v.items()
            if kk.startswith("verdict_"))
        print(f"{k:<9} {vd}")
    print("\nOUTPUT_HASH json:",
          hashlib.sha256(blob.encode("utf-8")).hexdigest())
    print("OUTPUT_HASH md:  ", hashlib.sha256(
        (ROOT / "RC7_RESULTS.md").read_bytes()).hexdigest())
    return 0


def render_md(res):
    L = []
    A = L.append
    A("# RC-7r RESULTS — post-S-1 recompute, re-scoped under Amendment 2")
    A("")
    A(f"> **{res['caveat']}**")
    A("")
    A(f"Basis: {res['basis']} · seed {res['seed']}, {res['n_boot']} "
      "resamples · " + res["amendments"] + ".")
    A("")
    A(f"**{res['standing_line']}.**")
    A("")
    A("## Fixtures")
    A("")
    for k in ("F1", "F2", "F4", "F5", "F6", "F7"):
        v = res["fixtures"][k]
        brief = {kk: vv for kk, vv in v.items()
                 if kk not in ("match", "detail")}
        A(f"- **{k}**: {'MATCH' if v['match'] else 'MISMATCH'} — "
          f"`{json.dumps(brief, default=str)[:170]}`")
    A("- **F8**: determinism — double run, hashes printed by the runner "
      "(see ledger).")
    A("")
    A("## Prediction scorecard (7 rows; falsifications first in prose)")
    A("")
    A("| # | prior | verdict | measured |")
    A("|---|---|---|---|")
    for k, v in res["predictions"].items():
        vd = v.get("verdict") or " / ".join(
            f"{kk.split('_', 1)[1]}:{vv}" for kk, vv in v.items()
            if kk.startswith("verdict_"))
        keep = {kk: v[kk] for kk in
                (["halves"] if "halves" in v else [])
                + [kk for kk in v
                   if not kk.startswith("verdict")
                   and kk not in ("prior", "halves")]}
        A(f"| {k} | {v['prior']} | **{vd}** | "
          f"`{json.dumps(keep, default=str)[:180]}` |")
    A("")
    A("## R7-2 — per-candidate strip-best (position rows first)")
    A("")
    A(f"> **CAVEAT (mandatory):** {res['R7_2_strip_best']['caveat_header']}")
    A("")
    A("| candidate | position Σ1×p | pos strip-best | swing Σ1×p | "
      "intraday Σ1×p | GRID Σ1×p | GRID strip-best |")
    A("|---|---|---|---|---|---|---|")
    for cid, row in res["R7_2_strip_best"]["candidates"].items():
        A(f"| {cid} | {row['position']['sum_1x_proxy']} | "
          f"{row['position']['strip_best']} | "
          f"{row['swing']['sum_1x_proxy']} | "
          f"{row['intraday']['sum_1x_proxy']} | "
          f"{row['GRID']['sum_1x_proxy']} | {row['GRID']['strip_best']} |")
    A("")
    A("## R7-3 — full symmetric confluence matrix (dual coordinates)")
    A("")
    A(f"Ladder {res['R7_3_confluence_matrix']['ladder']} · governor index "
      f"{json.dumps(res['R7_3_confluence_matrix']['gov_index'])}")
    A("")
    A("| tf | steps | condition | mandate | n T/F | exp T | exp F | sep |")
    A("|---|---|---|---|---|---|---|---|")
    for r in res["R7_3_confluence_matrix"]["rows"]:
        A(f"| {r['tf']} | {r['steps_from_governor']} | {r['condition']} | "
          f"{r['mandate']} | {r['n_true']}/{r['n_false']} | "
          f"{r['exp_true']} | {r['exp_false']} | {r['separation_r']} |")
    A("")
    A("JTO/TAO 1d rows (flag `seed_biased`, EXCLUDED from aggregates): "
      f"`{json.dumps(res['R7_3_confluence_matrix']['jto_tao_1d_seed_biased'], default=str)[:600]}`")
    A("")
    A("## R7-4 — FH-3 discriminator")
    A("")
    A(f"`{json.dumps(res['R7_4_fh3'], default=str)}`")
    A("")
    A("## R7-5 — joint lattice")
    A("")
    for slice_name, rows in res["R7_5_lattice"].items():
        A(f"### {slice_name}")
        A("")
        A("| cell | n | expectancy | CI95 | Σ | share of Σwins |")
        A("|---|---|---|---|---|---|")
        for key, v in rows.items():
            if "per_unit_1x" in v:
                A(f"| {key} | {v['n']} | {v['per_unit_1x']} (per-unit) | "
                  "— | — | — |")
            else:
                A(f"| {key} | {v['n']} | {v['expectancy']} | {v['ci95']} | "
                  f"{v['sum']} | {v['share_of_sum_wins_pct']} |")
        A("")
    A("## R7-6 — FH-1 signal-shape census")
    A("")
    A(f"`{json.dumps(res['R7_6_fh1'], default=str)}`")
    A("")
    A("## R7-7 — FH-2 R-space anatomy")
    A("")
    A(f"`{json.dumps(res['R7_7_fh2'], default=str)}`")
    A("")
    A("## R7-8 — FH-4 nesting census")
    A("")
    A(f"`{json.dumps(res['R7_8_fh4'], default=str)}`")
    A("")
    A("## R7-9 — sizing sweeps (first-order re-weights only)")
    A("")
    A("> CAVEAT: re-weighting ignores rail/halt/equity-path feedback; the "
      "modes interview and a config-only Tier-C own adoption.")
    A("")
    A(f"`{json.dumps(res['R7_9_sizing'], default=str)}`")
    A("")
    A("## R7-10 — trigger previews (PROXY)")
    A("")
    A(f"`{json.dumps(res['R7_10_previews'], default=str)}`")
    A("")
    A("## R7-11 — adds-funnel dual print")
    A("")
    A(f"`{json.dumps(res['R7_11_adds_funnel'], default=str)}`")
    A("")
    A("*Generated by scripts/rc7_recompute.py from raw journal/sidecar "
      "bytes. R7-1'/R7-12'/P-2L-a/b/c retired to S-2, verbatim-unseen.*")
    A("")
    return "\n".join(L)


if __name__ == "__main__":
    raise SystemExit(main())
