"""S-2 — fixtures (F-IDENT2 first), 13-row scorecard, family tables.

Contract: S2_Instrumented_Pass_Builder_Contract.md; mechanizations pinned
in the pre-registration (6af174b). Joins journal_s1 by tranche_id (s1 is
not re-emitted). HALT on any fixture MISMATCH — F-IDENT2 and F-REG indict
the fix itself.

Caveats on every table: IN-SAMPLE / FIRST-ORDER / RANKS-ONLY — TC-1
validates; cost PROXY on counterfactual legs; F4 ignores rail/halt/equity
feedback and prints both R-basis and bps-basis; JTO/TAO 1d void, never
false; the five long-history intraday cells floor out 2022-2023.
"""
from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
S2J = ROOT / "research_outputs" / "s2" / "journal_s2" / "scored"
S2J2 = ROOT / "research_outputs" / "s2" / "journal_s2_run2" / "scored"
S2E = ROOT / "research_outputs" / "s2" / "s2_events"
S2E2 = ROOT / "research_outputs" / "s2" / "s2_events_run2"
S1J = ROOT / "research_outputs" / "s1" / "journal_s1" / "scored"
P2 = ROOT / "research_outputs" / "tc4" / "journal_pass2" / "scored"
MAN = ROOT / "research_outputs" / "s2" / "manifest.json"

CANDS = ["ema200_gov_b0.5", "ema200_gov_b0.0", "ema89_gov_b0.0"]
STEP = {"intraday": 60_000, "swing": 300_000, "position": 900_000}
GOV_MS = {"intraday": 3_600_000, "swing": 14_400_000,
          "position": 43_200_000}
SLIP = {"BTCUSDT": 2.0, "ETHUSDT": 2.0}
MANDATES = ["swing", "intraday", "position"]
P2REF = (-1796.9930, 275.9924, 2599, 10.8503)
F1N = 229_963
SD_REF = 584.4963
CTRL_SEED = 20260721
BOOT_SEED = 20260722


def r4(x):
    return None if x is None else round(float(x) + 0.0, 4)


def pct(x, d):
    return None if not d else r4(100.0 * x / d)


def mean(vals):
    vals = [v for v in vals if v is not None]
    return r4(float(np.mean(vals))) if vals else None


def ms_of(ts):
    return int(datetime.fromisoformat(ts.replace("Z", "+00:00"))
               .timestamp() * 1000)


def mand(cell):
    return cell.rpartition("_")[2]


def toll(cell):
    return 2.0 * (5.0 + SLIP.get(cell.rpartition("_")[0], 5.0))


def norm(line):
    r = json.loads(line)
    r.pop("s2", None)
    r["run_id"] = r["engine_version"] = r["config_id"] = "-"
    return json.dumps(r, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False)


def lines(root, cell):
    for p in sorted((root / cell).glob("*.jsonl")):
        with open(p, encoding="utf-8") as f:
            yield from (l for l in f if l.strip())


def sha_root(root, cell):
    h = hashlib.sha256()
    for p in sorted((root / cell).glob("*.jsonl"), key=lambda p: p.name):
        h.update(p.read_bytes())
    return h.hexdigest()


def main() -> int:
    manifest = json.loads(MAN.read_text(encoding="utf-8"))
    cells = sorted(p.name for p in S2J.iterdir() if p.is_dir())

    # ── load s2 journal + byte-compare vs pass2 + s1 join ──
    byte_mism = {}
    fills, exits, sigrows = [], [], []
    for cell in cells:
        a, b = lines(S2J, cell), lines(P2, cell)
        m = sum(1 for la, lb in zip(a, b) if norm(la) != norm(lb))
        ea, eb = sum(1 for _ in a), sum(1 for _ in b)
        if m or ea or eb:
            byte_mism[cell] = (m, ea, eb)
        for line in lines(S2J, cell):
            r = json.loads(line)
            evt, s2 = r["evt"], r.get("s2")
            if evt in ("ENTRY_FILL", "ADD_FILL"):
                fills.append({"cell": cell, "mandate": mand(cell),
                              "tid": r["tranche_id"], "ts": r["ts_open"],
                              "dir": 1 if r["dir"] == "long" else -1,
                              "zone": r["zone"] or "-",
                              "size_r": r["size_r"], "px": r["px_fill"],
                              "stop": r["stop"], "qty": r["qty"],
                              "fill_class": r["fill_class"], "s2": s2})
            elif evt == "EXIT":
                cost = (r["fees"] or 0) + (r["funding_cum"] or 0) + \
                    (r["slippage"] or 0)
                exits.append({"cell": cell, "mandate": mand(cell),
                              "tid": r["tranche_id"], "ts": r["ts_open"],
                              "dir": 1 if r["dir"] == "long" else -1,
                              "realized_r": r["realized_r"],
                              "size_r": r["size_r"], "cost": cost,
                              "mfe_r": r["mfe_r"], "reason":
                              r["exit_reason"], "px_exit": r["px_fill"],
                              "stop_raw": r["stop"], "s2": s2})
            elif evt in ("REGIME", "V", "X") and s2 is None:
                sigrows.append({"cell": cell, "evt": evt,
                                "ts": r["ts_open"],
                                "dir": (1 if r["dir"] == "long" else
                                        -1 if r["dir"] == "short" else 0)})
            elif evt in ("REGIME", "V", "X"):
                sigrows.append({"cell": cell, "evt": evt,
                                "ts": r["ts_open"],
                                "dir": (1 if r["dir"] == "long" else
                                        -1 if r["dir"] == "short" else 0)})
    fill_by = {(f["cell"], f["tid"]): f for f in fills}
    s1adv = {}
    for cell in cells:
        for line in lines(S1J, cell):
            if '"EXIT"' not in line:
                continue
            r = json.loads(line)
            if r["evt"] == "EXIT":
                s1adv[(cell, r["tranche_id"])] = \
                    (r["s1"]["advance"]["n_stop_advances"],
                     r["s1"]["ratchet"])
    for e in exits:
        f = fill_by[(e["cell"], e["tid"])]
        e["f"] = f
        e["unit"] = abs(f["px"] - f["stop"])
        e["one_r"] = e["unit"] * f["qty"] / f["size_r"]
        e["cost_r"] = e["cost"] / e["one_r"]
        e["base_off"] = (ms_of(e["ts"]) - ms_of(f["ts"])) \
            // STEP[e["mandate"]]
        adv, s1r = s1adv[(e["cell"], e["tid"])]
        e["nadv"], e["s1r"] = adv, s1r
        slip = SLIP.get(e["cell"].rpartition("_")[0], 5.0) / 1e4
        raw = e["stop_raw"] if e["reason"] in ("stop", "stop_gap") and \
            e["stop_raw"] else e["px_exit"] / ((1 - slip) if e["dir"] == 1
                                               else (1 + slip))
        e["base_gross"] = (raw - f["px"]) * e["dir"] / e["unit"]
        e["camp"] = (e["cell"], int(e["tid"][1:].split("t")[0]))

    sidecar = defaultdict(list)
    for cell in cells:
        for line in open(S2E / f"{cell}.jsonl", encoding="utf-8"):
            r = json.loads(line)
            sidecar[r["family"]].append(r)

    fx = {}
    # F-IDENT2 — first
    ident = [(cid, e) for e in exits if e["nadv"] == 0 for cid in CANDS
             if not (e["s2"]["tl"][cid]["two_exit_r"] ==
                     e["s2"]["tl"][cid]["fold_exit_r"]
                     and e["s2"]["tl"][cid]["two_off"] ==
                     e["s2"]["tl"][cid]["fold_off"])]
    za_n = sum(1 for e in exits if e["nadv"] == 0)
    fx["F-IDENT2"] = {"zero_advance_tranches": za_n,
                      "violations": len(ident),
                      "detail": [(c, e["cell"], e["tid"])
                                 for c, e in ident[:10]],
                      "match": not ident}
    # F-BYTE
    fx["F-BYTE"] = {"cells": len(cells), "mismatched": byte_mism,
                    "match": not byte_mism}
    # F-P2REF
    camp_r = defaultdict(float)
    for e in exits:
        camp_r[e["camp"]] += e["realized_r"]
    n_c = len(camp_r)
    s1x = sum(camp_r.values())
    s0x = sum(e["realized_r"] + e["cost_r"] for e in exits)
    win = sum(1 for v in camp_r.values() if v > 0)
    fx["F-P2REF"] = {"sum_1x": r4(s1x), "sum_0x": r4(s0x),
                     "campaigns": n_c, "win_rate_pct": pct(win, n_c),
                     "match": abs(s1x - P2REF[0]) < 1e-3
                     and abs(s0x - P2REF[1]) < 1e-3 and n_c == P2REF[2]}
    # F-REG
    reg = next((e for e in exits if e["cell"] == "BTCUSDT_intraday"
                and e["ts"] == "2020-07-18T19:51:00Z"
                and e["reason"] == "campaign_died"), None)
    rr = reg["s2"]["tl"]["ema89_gov_b0.0"] if reg else None
    fx["F-REG"] = {"found": reg is not None,
                   "fold": (rr or {}).get("fold_exit_r"),
                   "kind": (rr or {}).get("fold_kind"),
                   "match": bool(rr and rr["fold_kind"] == "flatten"
                                 and abs(rr["fold_exit_r"] - 0.0739) < 5e-4
                                 and rr["two_exit_r"] == rr["fold_exit_r"])}
    # F-DELTA — pinned set
    fill_bar = [e for e in exits if e["base_off"] == 0]
    ties = [e for e in exits if e["nadv"] == 0 and e["base_off"] >= 1
            and any(e["s1r"][c]["exit_i_offset"] == e["base_off"]
                    for c in CANDS)
            and e["reason"] in ("failure_x", "opposite_cross", "v_reversal",
                                "campaign_died", "equity_floor")]
    rng = np.random.default_rng(CTRL_SEED)
    all_keys = sorted((e["cell"], e["tid"]) for e in exits)
    ctrl_keys = {all_keys[i] for i in
                 rng.choice(len(all_keys), size=200, replace=False)}
    pinned = {(e["cell"], e["tid"]) for e in fill_bar} | \
        {(e["cell"], e["tid"]) for e in ties} | ctrl_keys
    dmism = 0
    for e in exits:
        if (e["cell"], e["tid"]) not in pinned:
            continue
        for c in CANDS:
            if not (e["s2"]["tl"][c]["legacy_exit_r"] ==
                    e["s1r"][c]["exit_r"]
                    and e["s2"]["tl"][c]["legacy_off"] ==
                    e["s1r"][c]["exit_i_offset"]):
                dmism += 1
    fx["F-DELTA"] = {"pinned": len(pinned), "fill_bar": len(fill_bar),
                     "tie_class": len(ties), "controls": 200,
                     "mismatches": dmism, "match": dmism == 0}
    # F-F1N
    fx["F-F1N"] = {"rows": len(sidecar["f1_reject"]),
                   "match": len(sidecar["f1_reject"]) == F1N}
    # F-GRID
    d1k = {r["cell_key"] for r in sidecar["det_d1"]}
    d4k = {r["cell_key"] for r in sidecar["det_d4"]}
    f8k = {(r["step"], r["ema"]) for r in sidecar["f8_reclaim"]}
    f4k = set()
    for e in exits:
        f4k |= set(e["s2"]["f4"].keys())
    fx["F-GRID"] = {
        "d1_cells": sorted(d1k), "d4_cells": sorted(d4k),
        "f8_cells": sorted(map(str, f8k)), "f4_variants": sorted(f4k),
        "match": (d1k <= {"20_2.0", "20_3.0", "40_2.0", "40_3.0",
                          "80_2.0", "80_3.0"}
                  and f4k == {"exec", "30m", "1h"}
                  and all(s in (-1, -2, -3) for s, _ in f8k))}
    # F-EMIT
    miss = sum(1 for e in exits if not e["s2"] or "tl" not in e["s2"]) + \
        sum(1 for f in fills if not f["s2"])
    fx["F-EMIT"] = {"rows_missing_s2": miss, "match": miss == 0}
    # F-DET
    det_m = [c for c in cells
             if sha_root(S2J, c) != sha_root(S2J2, c)
             or hashlib.sha256((S2E / f"{c}.jsonl").read_bytes()).hexdigest()
             != hashlib.sha256((S2E2 / f"{c}.jsonl").read_bytes())
             .hexdigest()]
    fx["F-DET"] = {"mismatched": det_m,
                   "manifest": manifest["determinism_all_identical"],
                   "match": not det_m}

    print("== S-2 fixtures (F-IDENT2 first) ==")
    order = ["F-IDENT2", "F-BYTE", "F-P2REF", "F-REG", "F-DELTA", "F-F1N",
             "F-GRID", "F-EMIT", "F-DET"]
    ok = 0
    for k in order:
        v = fx[k]
        ok += v["match"]
        brief = {kk: vv for kk, vv in v.items()
                 if kk not in ("match", "detail", "mismatched",
                               "d1_cells", "d4_cells", "f8_cells")}
        print(f"{k:<9} {'MATCH' if v['match'] else '*** MISMATCH ***'} "
              f"{json.dumps(brief, default=str)[:150]}")
    if ok < 9:
        print("\n*** HALT: fixture mismatch — F-IDENT2/F-REG would indict "
              "the fix itself. Nothing priced. ***")
        return 1

    # ── R7-1′ two-line table ──
    res = {"fixtures": fx, "seed": BOOT_SEED}
    tl_tbl = {}
    for cid in CANDS:
        per = {}
        for m in ["GRID"] + MANDATES:
            sel = [e for e in exits if m == "GRID" or e["mandate"] == m]
            f0 = sum(e["s2"]["tl"][cid]["fold_exit_r"] * e["size_r"]
                     for e in sel)
            f1p = sum(e["s2"]["tl"][cid]["fold_exit_r"] * e["size_r"]
                      - e["cost_r"] for e in sel)
            t0 = sum(e["s2"]["tl"][cid]["two_exit_r"] * e["size_r"]
                     for e in sel)
            cp = defaultdict(float)
            caps, noise = [], []
            for e in sel:
                pr = e["s2"]["tl"][cid]["two_exit_r"] * e["size_r"] \
                    - e["cost_r"]
                cp[e["camp"]] += pr
                if e["mfe_r"] and e["mfe_r"] >= 1.0:
                    caps.append(e["s2"]["tl"][cid]["two_exit_r"]
                                / e["mfe_r"])
                nz = e["s2"]["tl"][cid]["two_noise"]
                if nz is not None:
                    noise.append(nz)
            vals = list(cp.values())
            t1p = sum(vals)
            per[m] = {"fold_0x": r4(f0), "fold_1x_proxy": r4(f1p),
                      "two_0x": r4(t0), "two_1x_proxy": r4(t1p),
                      "strip_best_two_1x": r4(t1p - max(vals))
                      if vals else None,
                      "win_pct": pct(sum(1 for v in vals if v > 0),
                                     len(vals)),
                      "med_capture_pct":
                          r4(100 * float(np.median(caps))) if caps else None,
                      "noise_pct": pct(sum(noise), len(noise)),
                      "src_census": dict(Counter(
                          e["s2"]["tl"][cid]["two_src"] for e in sel))}
        tl_tbl[cid] = per
    res["R7_1p_two_line"] = {
        "table": tl_tbl,
        "adds_funnel_note": "== baseline by construction: line 1 IS the "
                            "native ratchet the BE-gate tests; an exited "
                            "tranche gates nothing"}

    # ── R7-12′ fill-bar bias ──
    r712 = {}
    for cid in CANDS:
        per = {}
        for m in ["GRID"] + MANDATES:
            sel = [e for e in fill_bar if m == "GRID"
                   or e["mandate"] == m]
            leg = sum(e["s1r"][cid]["exit_r"] * e["size_r"] for e in sel
                      if e["s1r"][cid]["exit_r"] is not None)
            bg = sum(e["base_gross"] * e["size_r"] for e in sel)
            ride = sum(1 for e in sel
                       if e["s1r"][cid]["exit_r"] is not None
                       and e["s1r"][cid]["exit_r"] > e["base_gross"] + 1e-9)
            per[m] = {"n": len(sel), "legacy_0x": r4(leg),
                      "engine_truth_0x": r4(bg),
                      "bias": r4(leg - bg),
                      "recovery_ride_pct": pct(ride, len(sel))}
        r712[cid] = per
    res["R7_12p_fill_bar_bias"] = {
        "table": r712,
        "footnote": "standing correction on every S-1 fold-in figure"}

    # ── F1 reject table ──
    f1 = sidecar["f1_reject"]
    f1o = [r for r in f1 if r["outcome_r"] is not None]
    f1net = [r["outcome_r"] - toll(r["cell_id"]) / r["stop_dist_bps"]
             for r in f1o if r.get("stop_dist_bps")]
    r1s = [e for e in exits if e["f"]["fill_class"] == "r1"]
    r1net = sum(e["realized_r"] for e in r1s) / \
        sum(e["size_r"] for e in r1s)
    res["F1_rejects"] = {
        "n": len(f1), "with_outcome": len(f1o),
        "per_unit_gross_mean": mean([r["outcome_r"] for r in f1o]),
        "per_unit_net_proxy_mean": mean(f1net),
        "admitted_r1_per_unit_net": r4(r1net),
        "terminal_census": dict(Counter(r["terminal"] for r in f1)),
        "per_mandate_net": {m: mean(
            [r["outcome_r"] - toll(r["cell_id"]) / r["stop_dist_bps"]
             for r in f1o if mand(r["cell_id"]) == m
             and r.get("stop_dist_bps")]) for m in MANDATES}}

    # ── F2 headwind split ──
    hw = [e for e in exits if e["f"]["s2"]["levels"]["headwind"]]
    nhw = [e for e in exits if not e["f"]["s2"]["levels"]["headwind"]]
    def pu(es):
        s = sum(e["size_r"] for e in es)
        return r4(sum(e["realized_r"] for e in es) / s) if s else None
    res["F2_headwind"] = {"n_headwind": len(hw), "n_clear": len(nhw),
                          "pu_headwind": pu(hw), "pu_clear": pu(nhw),
                          "separation": r4((pu(hw) or 0) - (pu(nhw) or 0))}

    # ── F4 table ──
    f4t = {}
    for tfv in ("exec", "30m", "1h"):
        book = 0.0
        void = conv = shakeouts = 0
        for e in exits:
            v = e["s2"]["f4"].get(tfv)
            if v is None or v.get("void"):
                void += 1
                book += e["realized_r"]
                continue
            ratio = (e["unit"] / e["f"]["px"] * 1e4) / v["stop_dist_bps"]
            book += v["exit_r_struct"] * e["size_r"] - e["cost_r"] * ratio
            if e["s2"]["baseline_shakeout"]:
                shakeouts += 1
                if v["reach_1r_struct"]:
                    conv += 1
        f4t[tfv] = {"void": void, "grid_1x_struct_book": r4(book),
                    "baseline_shakeouts": shakeouts,
                    "shakeout_conversions": conv}
    res["F4_struct_stop"] = {
        "table": f4t, "baseline_grid_1x": P2REF[0],
        "caveat": "first-order; rail/halt/equity feedback ignored; "
                  "void tranches keep their baseline outcome"}

    # ── detectors ──
    def sgn_mean(rows):
        v = [r["fwd_20_bps"] * r.get("dir", 1) for r in rows
             if r.get("fwd_20_bps") is not None]
        return mean(v), len(v)
    d4_by_cell = defaultdict(list)
    for r in sidecar["det_d4"]:
        d4_by_cell[(r["tf"], r["cell_key"])].append(r)
    d4_cells_sign = {k: sgn_mean(v)[0] for k, v in d4_by_cell.items()}
    pos_cells = sum(1 for v in d4_cells_sign.values()
                    if v is not None and v > 0)
    d4_1h = sgn_mean([r for r in sidecar["det_d4"] if r["tf"] == "1h"])
    d4_4h = sgn_mean([r for r in sidecar["det_d4"] if r["tf"] == "4h"])
    res["detectors"] = {
        "d4_mean_fwd20_signed_bps": sgn_mean(sidecar["det_d4"])[0],
        "d4_events": len(sidecar["det_d4"]),
        "d4_sign_robust_cells": f"{pos_cells}/{len(d4_cells_sign)}",
        "d4_1h_mean": d4_1h[0], "d4_4h_mean": d4_4h[0],
        "d1_events": len(sidecar["det_d1"]),
        "d2_events": len(sidecar["det_d2"]),
        "d3_events": len(sidecar["det_d3"])}
    # entry splits (30m pooled)
    def det30(f):
        d = f["s2"]["det"]
        return d.get("30m") if d else None
    br = [e for e in exits if (det30(e["f"]) or {}).get("break_retest")]
    inr = [e for e in exits if (det30(e["f"]) or {}).get("in_range")
           and not (det30(e["f"]) or {}).get("break_retest")]
    z2i = [e for e in exits if e["f"]["zone"] == "Z2"
           and (det30(e["f"]) or {}).get("in_range")]
    z2o = [e for e in exits if e["f"]["zone"] == "Z2"
           and not (det30(e["f"]) or {}).get("in_range")]
    res["entry_splits"] = {
        "break_retest": {"n": len(br), "pu": pu(br)},
        "mid_range": {"n": len(inr), "pu": pu(inr)},
        "z2_in_range": {"n": len(z2i), "pu": pu(z2i)},
        "z2_out_range": {"n": len(z2o), "pu": pu(z2o)}}

    # ── F7 pockets ──
    d4r = [r for r in sidecar["det_d4"]
           if r.get("depth_frac") is not None
           and r.get("fwd_20_bps") is not None]
    if d4r:
        depths = np.array([r["depth_frac"] for r in d4r])
        rets = np.array([r["fwd_20_bps"] * r["dir"] for r in d4r])
        qs = np.quantile(depths, np.linspace(0, 1, 11))
        decs = []
        for i in range(10):
            m2 = (depths >= qs[i]) & (depths <= qs[i + 1])
            decs.append({"decile": i + 1, "n": int(m2.sum()),
                         "mean_fwd20_bps": r4(float(rets[m2].mean()))
                         if m2.any() else None})
        res["F7_pockets"] = {"deciles": decs}
    else:
        res["F7_pockets"] = {"deciles": []}

    # ── F8 ──
    f8 = sidecar["f8_reclaim"]
    rec12 = [r for r in f8 if r["step"] in (-1, -2) and r["reclaimed_b5"]]
    unr1 = [r for r in f8 if r["step"] == -1 and r["ema"] == "e200"
            and not r["reclaimed_b5"]]
    rec1 = [r for r in f8 if r["step"] == -1 and r["ema"] == "e200"
            and r["reclaimed_b5"]]
    res["F8_reclaim"] = {
        "events": len(f8),
        "reclaim_12_mean_rem_r": mean([r["rem_r_mean"] for r in rec12]),
        "unreclaimed_s1_e200_mean": mean([r["rem_r_mean"] for r in unr1]),
        "reclaimed_s1_e200_mean": mean([r["rem_r_mean"] for r in rec1])}

    # ── FH-4 widened grid ──
    camp_info = defaultdict(lambda: {"t0": None, "t1": None, "dir": 0,
                                     "cell": None})
    for e in exits:
        ci = camp_info[e["camp"]]
        t0, t1 = ms_of(e["f"]["ts"]), ms_of(e["ts"])
        ci["t0"] = t0 if ci["t0"] is None else min(ci["t0"], t0)
        ci["t1"] = t1 if ci["t1"] is None else max(ci["t1"], t1)
        ci["dir"], ci["cell"] = e["dir"], e["cell"]
    nest = {}
    for N in (0, 6, 12, 24):
        wname = "active_at_birth" if N == 0 else f"born_within_{N}"
        wr, wor = [], []
        for c, ci in camp_info.items():
            if mand(ci["cell"]) != "swing":
                continue
            asset = ci["cell"].rpartition("_")[0]
            icamps = [cj for cj, cji in camp_info.items()
                      if cji["cell"] == f"{asset}_intraday"
                      and cji["dir"] == ci["dir"]]
            if N == 0:
                hit = any(cji["t0"] <= ci["t0"] <= cji["t1"]
                          for cj, cji in camp_info.items()
                          if (cj in icamps))
            else:
                w = N * GOV_MS["swing"]
                hit = any(abs(camp_info[cj]["t0"] - ci["t0"]) <= w
                          for cj in icamps)
            (wr if hit else wor).append(camp_r[c])
        nest[wname] = {"n_cond": len(wr),
                       "sep": r4((np.mean(wr) if wr else 0)
                                 - (np.mean(wor) if wor else 0)),
                       "exp_cond": mean(wr), "exp_uncond": mean(wor)}
    res["FH4_grid"] = nest

    # ── predictions (13) ──
    P = {}
    g = tl_tbl["ema200_gov_b0.5"]["GRID"]
    P["P-2L-a"] = {"prior": 55, "two_0x": g["two_0x"],
                   "verdict": "CONFIRMED" if 500 <= g["two_0x"] <= 650
                   else "FALSIFIED"}
    p1 = tl_tbl["ema200_gov_b0.5"]["position"]["two_1x_proxy"]
    P["P-2L-b"] = {"prior": 65, "position_two_1x_proxy": p1,
                   "verdict": "CONFIRMED" if p1 >= 300 else "FALSIFIED"}
    adv = [e for e in exits if e["nadv"] > 0]
    ge = sum(1 for e in adv
             if e["s2"]["tl"]["ema200_gov_b0.5"]["two_exit_r"]
             >= e["s2"]["tl"]["ema200_gov_b0.5"]["fold_exit_r"] - 1e-9)
    P["P-2L-c"] = {"prior": 55, "ge_share_pct": pct(ge, len(adv)),
                   "verdict": "CONFIRMED"
                   if pct(ge, len(adv)) >= 45 else "FALSIFIED"}
    P["P-SD"] = {"prior": 65, "fold_0x_corrected": g["fold_0x"],
                 "pinned": SD_REF,
                 "verdict": "CONFIRMED" if g["fold_0x"] < SD_REF
                 else "FALSIFIED"}
    P["P-F1"] = {"prior": 60,
                 "reject_net": res["F1_rejects"]["per_unit_net_proxy_mean"],
                 "r1_net": r4(r1net),
                 "verdict": "CONFIRMED"
                 if res["F1_rejects"]["per_unit_net_proxy_mean"] < r1net
                 else "FALSIFIED"}
    b30 = f4t["30m"]["grid_1x_struct_book"]
    P["P-F4"] = {"prior": 55, "struct_30m_book": b30,
                 "verdict": "CONFIRMED" if b30 > P2REF[0] else "FALSIFIED"}
    d_pd1 = (pu(br) or 0) - (pu(inr) or 0)
    P["P-PD1"] = {"prior": 60, "sep": r4(d_pd1),
                  "verdict": "CONFIRMED" if d_pd1 >= 0.25
                  else "FALSIFIED"}
    dm = res["detectors"]["d4_mean_fwd20_signed_bps"]
    P["P-PD2"] = {"prior": 60, "d4_mean_bps": dm,
                  "verdict": "CONFIRMED" if (dm or 0) > 0
                  else "FALSIFIED"}
    d_pd3 = (pu(z2i) or 0) - (pu(z2o) or 0)
    P["P-PD3"] = {"prior": 55, "sep": r4(d_pd3),
                  "verdict": "CONFIRMED" if d_pd3 <= -0.3
                  else "FALSIFIED"}
    rob = pos_cells / len(d4_cells_sign) if d4_cells_sign else 0
    repl = (d4_1h[0] is not None and d4_4h[0] is not None
            and (d4_1h[0] > 0) == (d4_4h[0] > 0))
    P["P-PD4"] = {"prior": 60, "d4_robust": r4(100 * rob),
                  "d4_replicates": repl,
                  "verdict": "CONFIRMED"
                  if (rob >= 2 / 3 or rob <= 1 / 3) and repl
                  else "FALSIFIED"}
    rm = res["F8_reclaim"]["reclaim_12_mean_rem_r"]
    fsep = None
    if res["F8_reclaim"]["unreclaimed_s1_e200_mean"] is not None and \
            res["F8_reclaim"]["reclaimed_s1_e200_mean"] is not None:
        fsep = r4(res["F8_reclaim"]["unreclaimed_s1_e200_mean"]
                  - res["F8_reclaim"]["reclaimed_s1_e200_mean"])
    P["P-F8"] = {"prior": [55, 55], "reclaim_mean": rm,
                 "failure_sep": fsep,
                 "verdict_reclaim": "CONFIRMED"
                 if rm is not None and rm >= 0.10 else "FALSIFIED",
                 "verdict_failure": "CONFIRMED"
                 if fsep is not None and fsep <= -0.3 else "FALSIFIED"}
    P["P-F2"] = {"prior": 55, "sep": res["F2_headwind"]["separation"],
                 "verdict": "CONFIRMED"
                 if res["F2_headwind"]["separation"] is not None
                 and res["F2_headwind"]["separation"] <= -0.2
                 else "FALSIFIED"}
    nest_ok = any(v["n_cond"] >= 80 and (v["sep"] or 0) >= 0.5
                  for v in nest.values())
    P["P-NEST"] = {"prior": 50, "grid": nest,
                   "verdict": "CONFIRMED" if nest_ok else "FALSIFIED"}
    res["predictions"] = P
    print("\n== predictions (13) ==")
    for k, v in P.items():
        vd = v.get("verdict") or f"{v['verdict_reclaim']}/" \
            f"{v['verdict_failure']}"
        print(f"{k:<8} {vd}")

    res["caveat"] = ("IN-SAMPLE / FIRST-ORDER / RANKS-ONLY - TC-1 "
                     "validates; cost proxies stated; JTO/TAO 1d void; "
                     "intraday era caveat")
    blob = json.dumps(res, indent=1, sort_keys=True, default=str) + "\n"
    (ROOT / "s2_results.json").write_text(blob, encoding="utf-8",
                                          newline="\n")
    md = ["# S-2 MEASUREMENT — corrected simulator + new families "
          "(engine 1.0.10)", "", f"> **{res['caveat']}**", "",
          "R7-1' delivered — TC-1 registers against this table.", "",
          "## Fixtures (F-IDENT2 first)", ""]
    for k in order:
        v = fx[k]
        md.append(f"- **{k}**: MATCH — `" + json.dumps(
            {kk: vv for kk, vv in v.items()
             if kk not in ('match', 'detail', 'mismatched')},
            default=str)[:150] + "`")
    md += ["", "## Scorecard", "", "| # | verdict | measured |", "|---|---|---|"]
    for k, v in P.items():
        vd = v.get("verdict") or f"{v['verdict_reclaim']}/" \
            f"{v['verdict_failure']}"
        keep = {kk: vv for kk, vv in v.items()
                if not kk.startswith("verdict") and kk not in
                ("prior", "grid")}
        md.append(f"| {k} | **{vd}** | `{json.dumps(keep, default=str)[:170]}` |")
    for sec in ("R7_1p_two_line", "R7_12p_fill_bar_bias", "F1_rejects",
                "F2_headwind", "F4_struct_stop", "detectors",
                "entry_splits", "F7_pockets", "F8_reclaim", "FH4_grid"):
        md += ["", f"## {sec}", "",
               f"`{json.dumps(res[sec], default=str)[:2000]}`"]
    md += ["", "*scripts/s2_fixtures.py; raw bytes only; s1 joined, "
           "not re-emitted.*", ""]
    (ROOT / "S2_MEASUREMENT.md").write_text("\n".join(md),
                                            encoding="utf-8", newline="\n")
    print("\nOUTPUT_HASH json:",
          hashlib.sha256(blob.encode()).hexdigest())
    print("OUTPUT_HASH md:  ", hashlib.sha256(
        (ROOT / "S2_MEASUREMENT.md").read_bytes()).hexdigest())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
