"""S-1 — fixtures F-BYTE..F-DET, prediction scorecard, measurement tables.

Contract: S1_Instrumented_Replay_Builder_Contract.md §6-§8. Recomputed from
raw bytes: journal_s1 vs journal_pass2 (F-BYTE streams both, row by row, in
order), the sidecar streams, and the runner manifest. HALT (non-zero exit,
no downstream artifacts) on F-BYTE / F-NULL / F-P2REF / any fixture
violation.

First-order caveat (stated on every table): exit/ratchet shadows are
computed on the actual entry stream; entry-filter flags on the actual fill
set. A really-adopted rule changes the trade set. These tables RANK;
Tier-C validates. Candidate exit_r is GROSS (0x); 1x proxies use the row's
actual journaled cost/one_r and are labeled proxies.

Usage: python scripts/s1_fixtures.py
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
sys.path.insert(0, str(ROOT))

from engine.s1 import (ADD_TRIGGERS, ANCHOR_Y, BPS_M, DEADGATE_HOURS,  # noqa: E402
                       RATCHET_IDS, V_VARIANTS)

P2 = ROOT / "research_outputs" / "tc4" / "journal_pass2" / "scored"
S1J = ROOT / "research_outputs" / "s1" / "journal_s1" / "scored"
S1J2 = ROOT / "research_outputs" / "s1" / "journal_s1_run2" / "scored"
S1E = ROOT / "research_outputs" / "s1" / "s1_events"
S1E2 = ROOT / "research_outputs" / "s1" / "s1_events_run2"
MANIFEST = ROOT / "research_outputs" / "s1" / "manifest.json"
RESAMPLE_REPORT = ROOT / "research_outputs" / "s1" / "resampled" / \
    "resample_report.json"
OUT_DIR = ROOT / "research_outputs" / "s1"

SEED = 20260719
N_BOOT = 10_000
P2REF = {"sum_1x": -1796.9930, "sum_0x": 275.9924, "campaigns": 2599,
         "win_rate_pct": 10.8503}
REENTRY_REF_NET_PER_UNIT = -0.7554
NP_COUNT_REF = 69_395
INTERVAL = {"1m": 60_000, "5m": 300_000, "15m": 900_000}
SLIP = {"BTCUSDT": 2.0, "ETHUSDT": 2.0, "SOLUSDT": 5.0, "NEARUSDT": 5.0,
        "ZECUSDT": 5.0, "JTOUSDT": 5.0, "TAOUSDT": 5.0}
ZONE_KEYS = (["z3p_0.25", "z3p_0.35", "z3p_0.5"]
             + [f"asym_{a}_{b}" for a, b in
                [(0.25, 0.5), (0.25, 0.75), (0.25, 1.0),
                 (0.5, 0.5), (0.5, 0.75), (0.5, 1.0)]])
ASYM_KEY = "asym_0.25_0.5"
V_IDS = [v for v, _ in V_VARIANTS]


def r4(x):
    return None if x is None else round(float(x) + 0.0, 4)


def med(vals):
    vals = [v for v in vals if v is not None]
    return r4(float(np.median(vals))) if vals else None


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


def norm_strip(line: str) -> str:
    r = json.loads(line)
    r.pop("s1", None)
    r["run_id"] = r["engine_version"] = r["config_id"] = "-"
    return json.dumps(r, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False)


def cell_lines(root: Path, cell: str):
    for p in sorted((root / cell).glob("*.jsonl")):
        with open(p, encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    yield line


def files_sha(root: Path, cell: str) -> str:
    h = hashlib.sha256()
    for p in sorted((root / cell).glob("*.jsonl"), key=lambda p: p.name):
        h.update(p.read_bytes())
    return h.hexdigest()


def mandate_of(c):
    return c.rpartition("_")[2]


# ═══════════════════════════════════════ pass A: stream, compare, collect
def load_all():
    cells = sorted(p.name for p in S1J.iterdir() if p.is_dir())
    byte_mism = {}
    null_viol = 0
    grid_viol = []
    fills, exits, sigrows = [], [], []
    for cell in cells:
        a_iter = cell_lines(S1J, cell)
        b_iter = cell_lines(P2, cell)
        mism = 0
        for la, lb in zip(a_iter, b_iter):
            if norm_strip(la) != norm_strip(lb):
                mism += 1
        extra_a = sum(1 for _ in a_iter)
        extra_b = sum(1 for _ in b_iter)
        if mism or extra_a or extra_b:
            byte_mism[cell] = {"mismatched": mism, "extra_s1": extra_a,
                               "suppressed": extra_b}
        for line in cell_lines(S1J, cell):
            r = json.loads(line)
            evt = r["evt"]
            s1 = r.get("s1")
            if evt in ("ENTRY_FILL", "ADD_FILL"):
                if s1 is None or "entryflags" not in s1:
                    null_viol += 1
                    continue
                ef = s1["entryflags"]
                want_ef = ({f"rej_struct_{f'{y}'.replace('.', '')}"
                            for y in ANCHOR_Y}
                           | {f"rej_pure_{f'{y}'.replace('.', '')}"
                              for y in ANCHOR_Y}
                           | {f"rej_bps_{f'{m}'.replace('.', '')}"
                              for m in BPS_M}
                           | {"stop_dist_bps", "roundtrip_cost_bps"})
                if set(ef) != want_ef:
                    grid_viol.append((cell, "entryflags", r["ts_open"]))
                fills.append({
                    "cell": cell, "mandate": mandate_of(cell),
                    "ts": r["ts_open"], "tranche_id": r["tranche_id"],
                    "dir": 1 if r["dir"] == "long" else -1,
                    "zone": r["zone"] or "-", "stage": r["stage"],
                    "grade": r["grade"], "retr": r["retr"],
                    "size_r": r["size_r"], "fill_class": r["fill_class"],
                    "conc": r["concurrent_open_at_fill"],
                    "ef": ef, "cluster": s1.get("cluster"),
                })
            elif evt == "EXIT":
                if s1 is None or "ratchet" not in s1:
                    null_viol += 1
                    continue
                if set(s1["ratchet"]) != set(RATCHET_IDS):
                    grid_viol.append((cell, "ratchet_ids", r["ts_open"]))
                cost = (r["fees"] or 0) + (r["funding_cum"] or 0) + \
                    (r["slippage"] or 0)
                one_r = abs(r["px_fill"] - (r["stop"] or r["px_fill"]))
                exits.append({
                    "cell": cell, "mandate": mandate_of(cell),
                    "ts": r["ts_open"], "tranche_id": r["tranche_id"],
                    "dir": 1 if r["dir"] == "long" else -1,
                    "realized_r": r["realized_r"], "size_r": r["size_r"],
                    "cost": cost, "mfe_r": r["mfe_r"],
                    "cohort": r["cohort"], "exit_reason": r["exit_reason"],
                    "s1": s1,
                })
            elif s1 is not None and "zone" in s1:
                if set(s1["zone"]) != set(ZONE_KEYS):
                    grid_viol.append((cell, "zone_keys", r["ts_open"]))
                sigrows.append({
                    "cell": cell, "ts": r["ts_open"], "evt": evt,
                    "dir": (1 if r["dir"] == "long"
                            else -1 if r["dir"] == "short" else 0),
                    "zone": r["zone"] or "-", "stage": r["stage"],
                    "labels": s1["zone"],
                })
    return cells, byte_mism, null_viol, grid_viol, fills, exits, sigrows


def load_sidecar(cells):
    fam_rows = defaultdict(list)
    bad_ref = 0
    for cell in cells:
        p = S1E / f"{cell}.jsonl"
        if not p.exists():
            continue
        for line in open(p, encoding="utf-8"):
            r = json.loads(line)
            if r.get("cell_id") != cell or not r.get("ts_open"):
                bad_ref += 1
            fam_rows[r["family"]].append(r)
    return fam_rows, bad_ref


# ══════════════════════════════════════════════════════════ main
def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    resample = json.loads(RESAMPLE_REPORT.read_text(encoding="utf-8"))
    cells, byte_mism, null_viol, grid_viol, fills, exits, sigrows = load_all()
    fam_rows, bad_ref = load_sidecar(cells)

    # join: exit record per tranche; campaign structures
    exit_by = {(e["cell"], e["tranche_id"]): e for e in exits}
    fill_by = {(f["cell"], f["tranche_id"]): f for f in fills}
    camp_of = {}
    for e in exits + fills:
        tid = e["tranche_id"]
        camp_of[(e["cell"], tid)] = (e["cell"], int(tid[1:].split("t")[0]))
    camp_exits = defaultdict(list)
    for e in exits:
        camp_exits[camp_of[(e["cell"], e["tranche_id"])]].append(e)
    camp_fills = defaultdict(list)
    for f in fills:
        camp_fills[camp_of[(f["cell"], f["tranche_id"])]].append(f)
    seq_of = lambda tid: int(tid.split("t")[1])
    for c in camp_fills:
        camp_fills[c].sort(key=lambda f: (f["ts"], seq_of(f["tranche_id"])))
    camps = sorted(camp_exits)
    camp_r = {c: sum(e["realized_r"] for e in camp_exits[c]) for c in camps}
    print("== S-1 fixtures ==")

    fixtures = {}
    fixtures["F-BYTE"] = {
        "cells": len(cells), "mismatched_cells": byte_mism,
        "match": not byte_mism,
    }
    # F-P2REF
    n_c = len(camps)
    win = sum(1 for c in camps if camp_r[c] > 0)
    sum1 = sum(camp_r.values())
    # 0x needs one_r; rebuild from journal_pass2 fill rows (qty there)
    one_r_usd = {}
    for cell in cells:
        for line in cell_lines(P2, cell):
            if '"ENTRY_FILL"' not in line and '"ADD_FILL"' not in line:
                continue
            r = json.loads(line)
            if r["evt"] in ("ENTRY_FILL", "ADD_FILL"):
                one_r_usd[(cell, r["tranche_id"])] = \
                    abs(r["px_fill"] - r["stop"]) * r["qty"] / r["size_r"]
    sum0 = 0.0
    for e in exits:
        k = (e["cell"], e["tranche_id"])
        e["cost_r"] = e["cost"] / one_r_usd[k]
        e["r_0x"] = e["realized_r"] + e["cost_r"]
        e["unit_1x"] = e["realized_r"] / e["size_r"]
        e["unit_0x"] = e["r_0x"] / e["size_r"]
        sum0 += e["r_0x"]
    fixtures["F-P2REF"] = {
        "sum_1x": r4(sum1), "sum_0x": r4(sum0), "campaigns": n_c,
        "win_rate_pct": pct(win, n_c),
        "expected": P2REF,
        "match": (abs(sum1 - P2REF["sum_1x"]) < 1e-3
                  and abs(sum0 - P2REF["sum_0x"]) < 1e-3
                  and n_c == P2REF["campaigns"]
                  and abs(pct(win, n_c) - P2REF["win_rate_pct"]) < 1e-3),
    }
    # F-NULL: no suppressed rows (F-BYTE covers sets); every emitted
    # fill/EXIT carries its s1; audit edge nulls
    edge_nulls = sum(
        1 for e in exits for cid in RATCHET_IDS
        if e["s1"]["ratchet"][cid]["noise_stopout"] is None)
    fixtures["F-NULL"] = {
        "rows_missing_s1": null_viol,
        "suppressed_rows": sum(v.get("suppressed", 0)
                               for v in byte_mism.values()),
        "edge_null_noise_stopouts": edge_nulls,
        "match": null_viol == 0 and not byte_mism,
    }
    # F-GRID
    v_seen = sorted({r["variant"] for r in fam_rows.get("v_shadow", [])})
    trig_seen = sorted({r["trigger"] for r in fam_rows.get("add_trigger", [])})
    dg_keys_ok = all(
        set(e["s1"]["deadgate"]) == {"actual_campaign_r"} | {
            f"{a}_{n}h" for n in DEADGATE_HOURS for a in ("kill", "halve")}
        for e in exits if e["s1"].get("deadgate"))
    fixtures["F-GRID"] = {
        "schema_violations": len(grid_viol),
        "v_variants_seen": v_seen,
        "triggers_seen": trig_seen,
        "deadgate_keys_ok": dg_keys_ok,
        "match": (not grid_viol and dg_keys_ok
                  and set(v_seen) <= set(V_IDS)
                  and set(trig_seen) <= set(ADD_TRIGGERS)),
    }
    # F-SIDE
    np_count = len(fam_rows.get("reentry_ab", []))
    fixtures["F-SIDE"] = {
        "reentry_ab_rows": np_count, "expected": NP_COUNT_REF,
        "bad_references": bad_ref,
        "families": {k: len(v) for k, v in sorted(fam_rows.items())},
        "match": np_count == NP_COUNT_REF and bad_ref == 0,
    }
    # F-RESAMPLE
    res_ok = all(v["deterministic"] and v["span_ok"]
                 and v["agg_violations"] == 0
                 and v["interior_buckets_wrong_childcount"] == 0
                 for v in resample.values())
    fixtures["F-RESAMPLE"] = {"files": len(resample), "match": res_ok}
    # F-ADV
    adv_viol = sum(1 for e in exits
                   if e["s1"]["advance"]["stop_moved_r"] is not None
                   and e["s1"]["advance"]["stop_moved_r"] < -1e-9)
    fixtures["F-ADV"] = {"violations": adv_viol, "tranches": len(exits),
                         "match": adv_viol == 0}
    # F-DET
    det_mism = []
    for cell in cells:
        if files_sha(S1J, cell) != files_sha(S1J2, cell):
            det_mism.append(cell + ":journal")
        a = (S1E / f"{cell}.jsonl")
        b = (S1E2 / f"{cell}.jsonl")
        if (hashlib.sha256(a.read_bytes()).hexdigest()
                != hashlib.sha256(b.read_bytes()).hexdigest()):
            det_mism.append(cell + ":sidecar")
    fixtures["F-DET"] = {
        "mismatched": det_mism,
        "manifest_flag": manifest["determinism_all_identical"],
        "match": not det_mism and manifest["determinism_all_identical"],
    }
    for k, v in fixtures.items():
        brief = {kk: vv for kk, vv in v.items()
                 if kk not in ("match", "mismatched_cells", "families")}
        print(f"{k:<11} {'MATCH' if v['match'] else '*** VIOLATION ***'}  "
              f"{json.dumps(brief, default=str)[:170]}")
    n_match = sum(1 for v in fixtures.values() if v["match"])
    if n_match < 8:
        print(f"\n*** HALT: {8 - n_match} fixture violation(s). The "
              "instrument moved the experiment or the reader is wrong. ***")
        return 1

    # ══════════════════════════════════════════════ measurements
    caveat = ("FIRST-ORDER: shadows computed on the actual entry stream; "
              "flags on the actual fill set. Tables RANK; Tier-C validates. "
              "Candidate exit_r is GROSS (0x); 1x proxies use journaled "
              "cost/one_r.")
    results = {"caveat": caveat, "seed": SEED, "n_boot": N_BOOT,
               "engine_version": manifest["engine_version"],
               "config_sha256": manifest["config_sha256"],
               "fixtures": fixtures}

    # 1 ── ratchet two-axis scorecard per mandate
    scorecard = {}
    for mand in ("swing", "intraday", "position", "GRID"):
        sel = [e for e in exits if mand == "GRID" or e["mandate"] == mand]
        prot_win = [e for e in sel if e["cohort"] == "PROTECTED"
                    and e["mfe_r"] is not None and e["mfe_r"] >= 1.0]
        rows = {}
        for cid in RATCHET_IDS:
            recs = [e["s1"]["ratchet"][cid] for e in sel]
            caps = [r["capture_pct"] for e, r in zip(prot_win,
                    (e["s1"]["ratchet"][cid] for e in prot_win))]
            ns = [r["noise_stopout"] for r in recs
                  if r["noise_stopout"] is not None]
            ex_r = [r["exit_r"] for r in recs if r["exit_r"] is not None]
            gross = sum(r["exit_r"] * e["size_r"]
                        for e, r in zip(sel, recs) if r["exit_r"] is not None)
            net_proxy = sum(
                r["exit_r"] * e["size_r"] - e["cost_r"]
                for e, r in zip(sel, recs) if r["exit_r"] is not None)
            rows[cid] = {
                "n": len(recs),
                "engagement_pct": pct(sum(1 for r in recs if r["engaged"]),
                                      len(recs)),
                "median_capture_protected_pct":
                    r4(100 * float(np.median([c for c in caps
                                              if c is not None])))
                    if any(c is not None for c in caps) else None,
                "noise_stopout_pct": pct(sum(ns), len(ns)),
                "mean_exit_r_gross": r4(float(np.mean(ex_r)))
                    if ex_r else None,
                "sum_cell_r_0x": r4(gross),
                "sum_cell_r_1x_proxy": r4(net_proxy),
                "mean_adds_would_be_eligible": r4(float(np.mean(
                    [r["adds_would_be_eligible"] for r in recs
                     if r["adds_would_be_eligible"] is not None])))
                    if recs else None,
            }
        base_gross = sum(e["r_0x"] for e in sel)
        base_net = sum(e["realized_r"] for e in sel)
        xa = [e for e in sel]
        scorecard[mand] = {
            "tranches": len(sel), "protected_winners": len(prot_win),
            "baseline_actual": {"sum_cell_r_0x": r4(base_gross),
                                "sum_cell_r_1x": r4(base_net)},
            "candidates": rows,
        }
    results["ratchet_scorecard"] = scorecard

    # two-axis winner rule (pinned in-method): among candidates with GRID
    # noise-stopout <= 20%, max median capture on PROTECTED winners; if
    # none qualifies, the min-noise candidate.
    g = scorecard["GRID"]["candidates"]
    qual = {c: v for c, v in g.items()
            if v["noise_stopout_pct"] is not None
            and v["noise_stopout_pct"] <= 20.0
            and v["median_capture_protected_pct"] is not None}
    if qual:
        winner = max(qual, key=lambda c:
                     qual[c]["median_capture_protected_pct"])
    else:
        winner = min((c for c in g if g[c]["noise_stopout_pct"] is not None),
                     key=lambda c: g[c]["noise_stopout_pct"])
    results["two_axis_winner"] = {"winner": winner, "rule":
                                  "max median PROTECTED capture s.t. "
                                  "noise<=20%, else min noise",
                                  "qualifying": sorted(qual)}

    # 2 ── dead-gate table
    dg_rows = {}
    dg_deltas = {}
    for nh in DEADGATE_HOURS:
        for act in ("kill", "halve"):
            key = f"{act}_{nh}h"
            delta = trig = 0
            n_eval = 0
            for e in exits:
                dg = e["s1"].get("deadgate")
                if not dg or dg.get(key) is None:
                    continue
                n_eval += 1
                d = dg[key]
                if d.get("triggered"):
                    trig += 1
                    delta += d["cf_r"] - dg["actual_campaign_r"]
            dg_rows[key] = {"campaigns_evaluated": n_eval,
                            "triggered": trig,
                            "first_order_delta_1x": r4(delta)}
            dg_deltas[key] = delta
    best_dg = max(dg_deltas, key=lambda k: dg_deltas[k])
    results["deadgate"] = {"table": dg_rows, "best": best_dg,
                           "best_delta": r4(dg_deltas[best_dg])}

    # 3 ── entry-flag first-order books
    books = {}
    flag_names = ([f"rej_struct_{f'{y}'.replace('.', '')}" for y in ANCHOR_Y]
                  + [f"rej_pure_{f'{y}'.replace('.', '')}" for y in ANCHOR_Y]
                  + [f"rej_bps_{f'{m}'.replace('.', '')}" for m in BPS_M])
    grid_1x = sum(e["realized_r"] for e in exits)
    for fl in flag_names:
        rej_ids = {(f["cell"], f["tranche_id"]) for f in fills
                   if f["ef"].get(fl)}
        removed = [e for e in exits if (e["cell"], e["tranche_id"]) in rej_ids]
        r1x = sum(e["realized_r"] for e in removed)
        books[fl] = {
            "fills_flagged": len(rej_ids),
            "resolved_removed": len(removed),
            "removed_sum_1x": r4(r1x),
            "removed_per_unit_1x": r4(r1x / sum(e["size_r"] for e in removed))
                if removed else None,
            "first_order_grid_1x": r4(grid_1x - r1x),
        }
    results["entry_flag_books"] = {"grid_1x_actual": r4(grid_1x),
                                   "flags": books}

    # 4 ── zone tables
    sig_dist = {k: Counter() for k in ZONE_KEYS}
    for s in sigrows:
        for k in ZONE_KEYS:
            sig_dist[k][s["labels"][k]] += 1
    lbl_by_key = {}
    for s in sigrows:
        lbl_by_key[(s["cell"], s["ts"], s["dir"])] = s["labels"]
    zone_fill = {k: Counter() for k in ZONE_KEYS}
    zone_cohort = {k: defaultdict(lambda: [0.0, 0.0, 0])
                   for k in ZONE_KEYS}      # label -> [sum1x, size, n]
    step_of = {"intraday": 60_000, "swing": 300_000, "position": 900_000}
    joined = 0
    for e in exits:
        f = fill_by.get((e["cell"], e["tranche_id"]))
        if f is None:
            continue
        ts_fill = datetime.fromisoformat(f["ts"].replace("Z", "+00:00"))
        sig_ts = (ts_fill.timestamp() * 1000
                  - step_of[f["mandate"]])
        sig_iso = datetime.utcfromtimestamp(sig_ts / 1000) \
            .strftime("%Y-%m-%dT%H:%M:%SZ")
        lab = lbl_by_key.get((e["cell"], sig_iso, f["dir"]))
        e["zone_labels"] = lab
        e["zone_live"] = f["zone"]
        e["stage"] = f["stage"]
        if lab is None:
            continue
        joined += 1
        for k in ZONE_KEYS:
            zone_fill[k][lab[k]] += 1
            b = zone_cohort[k][lab[k]]
            b[0] += e["realized_r"]
            b[1] += e["size_r"]
            b[2] += 1
    zone_tbl = {}
    for k in ZONE_KEYS:
        zone_tbl[k] = {
            "signal_label_dist": dict(sig_dist[k]),
            "fill_label_dist": dict(zone_fill[k]),
            "fill_cohorts": {lbl: {"n": v[2], "per_unit_1x":
                                   r4(v[0] / v[1]) if v[1] else None}
                             for lbl, v in sorted(zone_cohort[k].items())},
        }
    results["zone_tables"] = {"joined_fills": joined, "variants": zone_tbl}

    # 5 ── V table
    v_rows = fam_rows.get("v_shadow", [])
    by_var = defaultdict(list)
    for r in v_rows:
        by_var[r["variant"]].append(r)
    base_n = sum(1 for r in by_var.get("all_loose", []) if not r["incremental"])
    v_tbl = {}
    for vid in V_IDS:
        rs = by_var.get(vid, [])
        inc = [r for r in rs if r["incremental"]]
        bas = [r for r in rs if not r["incremental"]]
        v_tbl[vid] = {
            "firings": len(rs), "incremental": len(inc),
            "x_baseline": r4(len(rs) / base_n) if base_n else None,
            "median_fwd20_r_baseline": med([r["fwd_20_r"] for r in bas]),
            "median_fwd20_r_incremental": med([r["fwd_20_r"] for r in inc]),
            "median_outcome_r": med([r["outcome_r"] for r in rs]),
        }
    results["v_table"] = {"baseline_firings_in_window": base_n,
                          "variants": v_tbl}

    # 6 ── A/B re-entry table
    traded = [e for e in exits
              if fill_by[(e["cell"], e["tranche_id"])]["fill_class"]
              == "re_entry"]
    tr_size = sum(e["size_r"] for e in traded)
    ab_rows = fam_rows.get("reentry_ab", [])
    cf_net = []
    for r in ab_rows:
        if r["outcome_r"] is None or not r["stop_dist_bps"]:
            continue
        cost_bps = 2.0 * (5.0 + SLIP[r["cell_id"].rpartition("_")[0]])
        cf_net.append(r["outcome_r"] - cost_bps / r["stop_dist_bps"])
    ab = {
        "traded_re_entries": {
            "n": len(traded),
            "per_unit_0x": r4(sum(e["r_0x"] for e in traded) / tr_size),
            "per_unit_1x": r4(sum(e["realized_r"] for e in traded) / tr_size),
            "win_rate_pct": pct(sum(1 for e in traded
                                    if e["realized_r"] > 0), len(traded)),
        },
        "confirm_while_flat_counterfactual": {
            "n": len(ab_rows), "n_with_outcome": len(cf_net),
            "per_unit_0x_mean": r4(float(np.mean(
                [r["outcome_r"] for r in ab_rows
                 if r["outcome_r"] is not None]))),
            "per_unit_net_proxy_mean": r4(float(np.mean(cf_net)))
                if cf_net else None,
            "net_proxy_ci95": boot_ci(cf_net),
            "terminal_census": dict(Counter(r["terminal"] for r in ab_rows)),
        },
    }
    results["reentry_ab"] = ab

    # 7 ── drought table
    d_rows = fam_rows.get("add_trigger", [])
    mc2 = {c for c in camps
           if any(f["fill_class"] == "true_add" for f in camp_fills[c])}
    drought = {}
    for trig in ADD_TRIGGERS:
        rs = [r for r in d_rows if r["trigger"] == trig]
        adm_base = [r for r in rs if r["admissible_under"].get("baseline")]
        best_cand, best_avg = None, -1.0
        for cid in RATCHET_IDS:
            per_camp = Counter()
            for r in rs:
                if r["admissible_under"].get(cid):
                    per_camp[(r["cell_id"], r["campaign"])] += 1
            avg = (sum(per_camp[(c[0], c[1])] for c in mc2) / len(mc2)
                   if mc2 else 0.0)
            if avg > best_avg:
                best_avg, best_cand = avg, cid
        drought[trig] = {
            "firings": len(rs),
            "admissible_baseline_pct": pct(len(adm_base), len(rs)),
            "mean_outcome_r": r4(float(np.mean(
                [r["outcome_r"] for r in rs if r["outcome_r"] is not None])))
                if rs else None,
            "best_candidate": best_cand,
            "best_avg_admissible_per_mc2_campaign": r4(best_avg),
        }
    results["drought"] = {"mc2_campaigns": len(mc2), "triggers": drought}

    # 8 ── MTF registered confluences + exploratory annex
    camp_opener_exit = {}
    for c in camps:
        opener = min(camp_exits[c],
                     key=lambda e: int(e["tranche_id"].split("t")[1]))
        camp_opener_exit[c] = opener
    def conf_split(flag_fn):
        a = [camp_r[c] for c in camps if flag_fn(camp_opener_exit[c])]
        b = [camp_r[c] for c in camps if not flag_fn(camp_opener_exit[c])]
        if not a or not b:
            return None
        return {"n_true": len(a), "n_false": len(b),
                "exp_true": r4(float(np.mean(a))),
                "exp_false": r4(float(np.mean(b))),
                "separation_r": r4(float(np.mean(a) - np.mean(b))),
                "ci_true": boot_ci(a), "ci_false": boot_ci(b)}
    def _beyond_1d_e89(e):
        m = e["s1"]["mtf"].get("1d", {})
        v = m.get("entry_d89")
        return v is not None and v * e["dir"] > 0
    def _30m_aligned(e):
        return bool(e["s1"]["mtf"].get("30m", {}).get("s2_aligned_entry"))
    def _1h_e200_frac(e):
        v = e["s1"]["mtf"].get("1h", {}).get("frac_beyond_e200")
        return v is not None and v >= 0.8
    registered = {
        "entry_beyond_1d_e89": conf_split(_beyond_1d_e89),
        "structure_30m_aligned_entry": conf_split(_30m_aligned),
        "frac80_beyond_1h_e200": conf_split(_1h_e200_frac),
    }
    annex = {}
    for tf in ("exec", "15m", "30m", "1h", "4h", "12h", "1d"):
        annex[f"{tf}_s2_aligned_entry"] = conf_split(
            lambda e, tf=tf: bool(e["s1"]["mtf"].get(tf, {})
                                  .get("s2_aligned_entry")))
        annex[f"{tf}_entry_beyond_e200"] = conf_split(
            lambda e, tf=tf: (e["s1"]["mtf"].get(tf, {}).get("entry_d200")
                              or 0) * e["dir"] > 0)
    results["mtf"] = {"registered": registered,
                      "exploratory_annex_vr1": annex}

    # 9 ── advancement table (P-S1b)
    pop = [e for e in exits if e["mfe_r"] is not None and e["mfe_r"] >= 1.0
           and e["r_0x"] < 0]
    nonadv = [e for e in pop
              if e["s1"]["advance"]["advances_before_mfe"] == 0]
    results["advancement"] = {
        "pop_mfe1_gross_loss": len(pop),
        "non_advanced": len(nonadv),
        "share_pct": pct(len(nonadv), len(pop)),
        "grid_advances_median": med([e["s1"]["advance"]["n_stop_advances"]
                                     for e in exits]),
        "bars_to_first_advance_median":
            med([e["s1"]["advance"]["bars_to_first_advance"]
                 for e in exits]),
    }

    # 10 ── cluster table
    cl = [f["cluster"] for f in fills if f["cluster"] is not None
          and f["cluster"]["attempt"] >= 2
          and f["cluster"]["dist_gov_atr"] is not None]
    results["cluster"] = {
        "attempt2plus_openers": len(cl),
        "dist_gov_atr_median": med([c["dist_gov_atr"] for c in cl]),
        "in_cluster_pct": {
            "k025": pct(sum(1 for c in cl if c["in_cluster_025"]), len(cl)),
            "k05": pct(sum(1 for c in cl if c["in_cluster_05"]), len(cl)),
            "k10": pct(sum(1 for c in cl if c["in_cluster_10"]), len(cl)),
        },
    }

    # 11 ── birth-predictor descriptive (mc>=2 / mc=3)
    def compo(camp_set):
        openers = [camp_fills[c][0] for c in camp_set if camp_fills[c]]
        return {
            "n": len(camp_set),
            "by_mandate": dict(Counter(o["mandate"] for o in openers)),
            "by_zone": dict(Counter(o["zone"] for o in openers)),
            "by_grade": dict(Counter(o["grade"] for o in openers)),
            "by_stage": dict(Counter(o["stage"] for o in openers)),
            "30m_aligned_pct": pct(sum(
                1 for c in camp_set
                if _30m_aligned(camp_opener_exit[c])), len(camp_set)),
        }
    mc3 = {c for c in camps
           if any(f["conc"] is not None and f["conc"] >= 2
                  for f in camp_fills[c])}
    results["birth_predictor"] = {"mc2plus": compo(mc2), "mc3": compo(mc3),
                                  "all": compo(set(camps))}

    # ══════════════════════════════════════════════ predictions
    preds = {}
    preds["P-S1b"] = {
        "prior_pct": 75, "share_pct": results["advancement"]["share_pct"],
        "threshold_pct": 33.3333,
        "verdict": "CONFIRMED"
        if (results["advancement"]["share_pct"] or 0) >= 100 / 3 else
        "FALSIFIED",
    }
    sw = scorecard["swing"]["candidates"]
    rat_ok = [c for c, v in sw.items()
              if (v["median_capture_protected_pct"] or 0) >= 25.0
              and v["noise_stopout_pct"] is not None
              and v["noise_stopout_pct"] <= 20.0]
    preds["P-S1-RAT"] = {"prior_pct": 60, "qualifying_swing": rat_ok,
                         "verdict": "CONFIRMED" if rat_ok else "FALSIFIED"}
    preds["P-S1-RAT2"] = {
        "prior_pct": 55, "winner": winner,
        "verdict": "CONFIRMED"
        if not winner.startswith("ema200_exec") else "FALSIFIED",
    }
    preds["P-S1-DG"] = {
        "prior_pct": 55, "best": best_dg,
        "best_delta": r4(dg_deltas[best_dg]),
        "verdict": "CONFIRMED" if dg_deltas[best_dg] >= 200 else "FALSIFIED",
    }
    cfm = ab["confirm_while_flat_counterfactual"]["per_unit_net_proxy_mean"]
    preds["P-S1-AB"] = {
        "prior_pct": 55, "counterfactual_net": cfm,
        "traded_reference": REENTRY_REF_NET_PER_UNIT,
        "verdict": "CONFIRMED"
        if cfm is not None and cfm >= REENTRY_REF_NET_PER_UNIT else
        "FALSIFIED",
    }
    add_ok = [t for t, v in drought.items()
              if (v["best_avg_admissible_per_mc2_campaign"] or 0) >= 2.0]
    preds["P-S1-ADD"] = {"prior_pct": 60, "qualifying_triggers": add_ok,
                         "verdict": "CONFIRMED" if add_ok else "FALSIFIED"}
    vt = v_tbl["all_loose"]
    freq_ok = vt["x_baseline"] is not None and vt["x_baseline"] >= 5.0
    mb = vt["median_fwd20_r_baseline"]
    mi = vt["median_fwd20_r_incremental"]
    qual_ok = not (mi is not None and mb is not None and mi > mb)
    preds["P-S1-V"] = {
        "prior_pct": [70, 55], "x_baseline": vt["x_baseline"],
        "median_fwd20_baseline": mb, "median_fwd20_incremental": mi,
        "verdict_frequency": "CONFIRMED" if freq_ok else "FALSIFIED",
        "verdict_quality": "CONFIRMED" if qual_ok else "FALSIFIED",
    }
    cur_z3 = [e for e in exits if e.get("zone_live") == "Z3"
              and e.get("zone_labels")]
    asym_z3_of_cur = [e for e in cur_z3
                      if e["zone_labels"][ASYM_KEY] == "Z3"]
    asym_all = [e for e in exits if e.get("zone_labels")
                and e["zone_labels"][ASYM_KEY] == "Z3"]
    def per_unit(es):
        s = sum(e["size_r"] for e in es)
        return r4(sum(e["realized_r"] for e in es) / s) if s else None
    share = pct(len(asym_z3_of_cur), len(cur_z3))
    pu_asym, pu_cur = per_unit(asym_all), per_unit(cur_z3)
    preds["P-S1-Z3"] = {
        "prior_pct": 55,
        "share_of_current_z3_pct": share,
        "asym_cohort_per_unit_1x": pu_asym,
        "current_z3_per_unit_1x": pu_cur,
        "verdict": "CONFIRMED"
        if (share is not None and share <= 40.0 and pu_asym is not None
            and pu_cur is not None and pu_asym >= pu_cur) else "FALSIFIED",
    }
    seps = [v["separation_r"] for v in registered.values()
            if v is not None]
    preds["P-S1-MTF"] = {
        "prior_pct": 50,
        "separations": {k: (v or {}).get("separation_r")
                        for k, v in registered.items()},
        "verdict": "CONFIRMED"
        if any(s is not None and abs(s) >= 0.5 for s in seps) else
        "FALSIFIED",
    }
    results["predictions"] = preds
    print("\n== predictions ==")
    for k, v in preds.items():
        vd = v.get("verdict") or \
            f"{v['verdict_frequency']}/{v['verdict_quality']}"
        print(f"{k:<10} {vd}")

    out_json = ROOT / "s1_results.json"
    out_json.write_text(json.dumps(results, indent=1, sort_keys=True,
                                   default=str) + "\n",
                        encoding="utf-8", newline="\n")
    out_md = ROOT / "S1_MEASUREMENT.md"
    out_md.write_text(render_md(results), encoding="utf-8", newline="\n")
    print(f"\n8/8 fixtures MATCH — wrote {out_json.name} and {out_md.name}")
    print("OUTPUT_HASH json:",
          hashlib.sha256(out_json.read_bytes()).hexdigest())
    print("OUTPUT_HASH md:  ",
          hashlib.sha256(out_md.read_bytes()).hexdigest())
    return 0


def render_md(res):
    L = []
    A = L.append
    A("# S-1 MEASUREMENT — instrumented replay on the TC-4 baseline "
      "(engine 1.0.9, measure-only)")
    A("")
    A(f"> **{res['caveat']}**")
    A("")
    A(f"Engine {res['engine_version']} · config sha "
      f"`{res['config_sha256'][:16]}…` · bootstrap seed {res['seed']}, "
      f"{res['n_boot']} resamples. Intraday-era caveat: the five "
      "long-history intraday cells halt (equity floor) in 2022-2023; their "
      "tranches are concentrated pre-halt.")
    A("")
    A("## Fixtures (8/8 MATCH)")
    A("")
    for k, v in res["fixtures"].items():
        brief = {kk: vv for kk, vv in v.items()
                 if kk not in ("match", "mismatched_cells", "families")}
        A(f"- **{k}**: MATCH — `{json.dumps(brief, default=str)[:150]}`")
    A("")
    A("## Prediction scorecard")
    A("")
    A("| # | prior | verdict | measured |")
    A("|---|---|---|---|")
    for k, v in res["predictions"].items():
        vd = v.get("verdict") or \
            f"freq {v['verdict_frequency']} / qual {v['verdict_quality']}"
        keep = {kk: vv for kk, vv in v.items()
                if kk not in ("verdict", "prior_pct", "verdict_frequency",
                              "verdict_quality")}
        A(f"| {k} | {v['prior_pct']} | **{vd}** | "
          f"`{json.dumps(keep, default=str)[:190]}` |")
    A("")
    A("## Ratchet two-axis scorecard (capture% vs noise-stopout%, "
      "per mandate)")
    A("")
    A(f"Two-axis winner (rule: {res['two_axis_winner']['rule']}): "
      f"**{res['two_axis_winner']['winner']}**")
    for mand, tbl in res["ratchet_scorecard"].items():
        A("")
        A(f"### {mand} — {tbl['tranches']} tranches, "
          f"{tbl['protected_winners']} PROTECTED winners · baseline "
          f"0x {tbl['baseline_actual']['sum_cell_r_0x']} / "
          f"1x {tbl['baseline_actual']['sum_cell_r_1x']}")
        A("")
        A("| candidate | engaged% | med capture% (PROT) | noise-stop% | "
          "mean exit_r | Σ0x | Σ1x proxy | adds-elig/tr |")
        A("|---|---|---|---|---|---|---|---|")
        for cid, v in tbl["candidates"].items():
            A(f"| {cid} | {v['engagement_pct']} | "
              f"{v['median_capture_protected_pct']} | "
              f"{v['noise_stopout_pct']} | {v['mean_exit_r_gross']} | "
              f"{v['sum_cell_r_0x']} | {v['sum_cell_r_1x_proxy']} | "
              f"{v['mean_adds_would_be_eligible']} |")
    A("")
    A("## Dead-gate triage (first-order Δ grid 1×)")
    A("")
    A("| gate | evaluated | triggered | Δ 1× |")
    A("|---|---|---|---|")
    for k, v in res["deadgate"]["table"].items():
        A(f"| {k} | {v['campaigns_evaluated']} | {v['triggered']} | "
          f"{v['first_order_delta_1x']} |")
    A(f"\nBest: **{res['deadgate']['best']}** "
      f"(Δ {res['deadgate']['best_delta']})")
    A("")
    A("## Entry-flag first-order books")
    A("")
    A(f"Actual grid 1×: {res['entry_flag_books']['grid_1x_actual']}")
    A("")
    A("| flag | fills flagged | removed Σ1× | removed /unit | "
      "first-order grid 1× |")
    A("|---|---|---|---|---|")
    for fl, v in res["entry_flag_books"]["flags"].items():
        A(f"| {fl} | {v['fills_flagged']} | {v['removed_sum_1x']} | "
          f"{v['removed_per_unit_1x']} | {v['first_order_grid_1x']} |")
    A("")
    A("## Zone-geometry shadow (labels on signal rows; cohorts on fills)")
    A("")
    A(f"Joined fills: {res['zone_tables']['joined_fills']}")
    A("")
    A("| variant | signal dist | fill cohort /unit 1× |")
    A("|---|---|---|")
    for k, v in res["zone_tables"]["variants"].items():
        coh = {lbl: c["per_unit_1x"] for lbl, c in v["fill_cohorts"].items()}
        A(f"| {k} | `{json.dumps(v['signal_label_dist'])}` | "
          f"`{json.dumps(coh)}` |")
    A("")
    A("## V-shadow")
    A("")
    A(f"Baseline firings in window: "
      f"{res['v_table']['baseline_firings_in_window']}")
    A("")
    A("| variant | firings | incremental | ×base | med fwd20 base | "
      "med fwd20 incr | med outcome |")
    A("|---|---|---|---|---|---|---|")
    for vid, v in res["v_table"]["variants"].items():
        A(f"| {vid} | {v['firings']} | {v['incremental']} | "
          f"{v['x_baseline']} | {v['median_fwd20_r_baseline']} | "
          f"{v['median_fwd20_r_incremental']} | {v['median_outcome_r']} |")
    A("")
    A("## Re-entry A/B")
    A("")
    A(f"`{json.dumps(res['reentry_ab'], default=str)}`")
    A("")
    A("## Add-trigger drought")
    A("")
    A(f"mc≥2 campaigns: {res['drought']['mc2_campaigns']}")
    A("")
    A("| trigger | firings | adm base% | mean outcome | best candidate | "
      "adm/mc2-camp |")
    A("|---|---|---|---|---|---|")
    for t, v in res["drought"]["triggers"].items():
        A(f"| {t} | {v['firings']} | {v['admissible_baseline_pct']} | "
          f"{v['mean_outcome_r']} | {v['best_candidate']} | "
          f"{v['best_avg_admissible_per_mc2_campaign']} |")
    A("")
    A("## MTF — three registered confluences")
    A("")
    A(f"`{json.dumps(res['mtf']['registered'], default=str)}`")
    A("")
    A("### Exploratory mining annex — VR-1 EXPLORATION, "
      "hypothesis-generating ONLY (V6)")
    A("")
    A(f"`{json.dumps(res['mtf']['exploratory_annex_vr1'], default=str)}`")
    A("")
    A("## Advancement (P-S1b) · Cluster · Birth predictors")
    A("")
    A(f"- advancement: `{json.dumps(res['advancement'])}`")
    A(f"- cluster (gov-ATR): `{json.dumps(res['cluster'])}`")
    A(f"- birth predictors: `{json.dumps(res['birth_predictor'])}`")
    A("")
    A("*Generated by scripts/s1_fixtures.py from raw journal/sidecar bytes; "
      "measurements only — no rule changed; Tier-C designs follow.*")
    A("")
    return "\n".join(L)


if __name__ == "__main__":
    raise SystemExit(main())
