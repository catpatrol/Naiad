"""TC-4 — fixtures F-SIG..F-DET, prediction scorecard, new-baseline rollup.

Contract: TC4_Engine_1_0_8_Builder_Contract.md §6-§8. Everything below is
recomputed from raw journal bytes (journal_pass1 = the superseded anchor
baseline, read-only; journal_pass2 = the TC-4 re-run) plus the runner's
manifest for the double-run identity. Any fixture violation prints HALT and
exits non-zero; artifacts (tc4_baseline.json / TC4_BASELINE.md) are written
only on 9/9 MATCH.

F-SIG normalization, DISCLOSED: the contract says "normalizing run_id and
engine_version fields only", but it also mandates config v12_anchor_g8 — and
config_id is stamped on every row, so a literal two-field normalization
cannot match. F-SIG here proves BOTH: (a) rows byte-identical after
normalizing the three run-identity stamps {run_id, engine_version,
config_id}; (b) the residual under the contract's two-field normalization is
confined to the config_id field (old rows all v12_anchor, new rows all
v12_anchor_g8). The strategy brain moved iff (a) fails.

Usage: python scripts/tc4_fixtures.py
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
PASS1 = ROOT / "research_outputs" / "v3_anchor" / "journal_pass1" / "scored"
PASS2 = ROOT / "research_outputs" / "tc4" / "journal_pass2" / "scored"
RUN2 = ROOT / "research_outputs" / "tc4" / "journal_pass2_run2" / "scored"
OUT_DIR = ROOT / "research_outputs" / "tc4"
MANIFEST = OUT_DIR / "manifest.json"
EXPECT = OUT_DIR / "expectation_table.json"

SEED = 20260718              # pinned bootstrap seed for the baseline CIs
N_BOOT = 10_000
INITIAL_EQUITY = 10000.0
FLOOR = 0.25 * INITIAL_EQUITY
MAX_LEV = 10.0
MIN_STOP_ATR = 0.5
TID_RE = re.compile(r"^c(\d+)t(\d+)$")
FILL_EVTS = ("ENTRY_FILL", "ADD_FILL")
SIG_EVTS = {"REGIME", "STAGE", "TAG", "PRIME", "CONFIRM", "V", "TPW",
            "CLUSTER", "X"}
INTERVAL_MS = {"1m": 60_000, "5m": 300_000, "15m": 900_000}
# engine wake order: flatten/gap exits BEFORE fills, intra-bar stops AFTER
PRE_FILL_EXITS = {"failure_x", "opposite_cross", "v_reversal",
                  "campaign_died", "stop_gap", "equity_floor"}
FIVE_INTRADAY = {"BTCUSDT_intraday", "ETHUSDT_intraday", "SOLUSDT_intraday",
                 "NEARUSDT_intraday", "ZECUSDT_intraday"}
COIN_FLIP_CELL = "ZECUSDT_swing"


def parse_ms(s):
    return int(datetime.fromisoformat(s.replace("Z", "+00:00"))
               .timestamp() * 1000)


def r4(x):
    return None if x is None else round(float(x) + 0.0, 4)


def r6(x):
    return None if x is None else round(float(x) + 0.0, 6)


def pct(x, d):
    return None if not d else r4(100.0 * x / d)


def boot_ci(vals, seed=SEED, n=N_BOOT):
    a = np.asarray(list(vals), dtype=float)
    if a.size < 2:
        return (None, None)
    rng = np.random.default_rng(seed)
    means = np.empty(n, dtype=float)
    for s in range(0, n, 1000):
        k = min(1000, n - s)
        idx = rng.integers(0, a.size, size=(k, a.size))
        means[s:s + k] = a[idx].mean(axis=1)
    return (r4(np.percentile(means, 2.5)), r4(np.percentile(means, 97.5)))


def load_cells(root):
    """cell -> rows in journal (file) order."""
    out = {}
    for d in sorted(p for p in root.iterdir() if p.is_dir()):
        rows = []
        for path in sorted(d.glob("*.jsonl")):
            with open(path, encoding="utf-8") as f:
                rows.extend(json.loads(l) for l in f if l.strip())
        out[d.name] = rows
    return out


def files_sha256(cell_dir):
    h = hashlib.sha256()
    for p in sorted(cell_dir.glob("*.jsonl"), key=lambda p: p.name):
        h.update(p.read_bytes())
    return h.hexdigest()


# ------------------------------------------------------------------ fixtures
def f_sig(p1, p2):
    def is_sig(r):
        return r["evt"] in SIG_EVTS or (
            r["evt"] == "REJECT" and not (r["tranche_id"] or "").startswith("trade_"))

    def norm3(r):
        r = dict(r)
        r["run_id"] = r["engine_version"] = r["config_id"] = "-"
        return json.dumps(r, sort_keys=True, separators=(",", ":"))

    mism, n_old, n_new = [], 0, 0
    cfg_ok = True
    for cell in sorted(set(p1) | set(p2)):
        old = [r for r in p1.get(cell, []) if is_sig(r)]
        new = [r for r in p2.get(cell, []) if is_sig(r)]
        n_old += len(old)
        n_new += len(new)
        cfg_ok &= all(r["config_id"] == "v12_anchor" for r in old)
        cfg_ok &= all(r["config_id"] == "v12_anchor_g8" for r in new)
        if sorted(map(norm3, old)) != sorted(map(norm3, new)):
            mism.append(cell)
    return {
        "rows_pass1": n_old, "rows_pass2": n_new,
        "mismatched_cells": mism,
        "residual_is_config_id_only": cfg_ok,
        "match": not mism and n_old == n_new and cfg_ok,
    }


def f_g8a(p2):
    viol, halt_table = [], {}
    for cell, rows in p2.items():
        floored_at = None
        for r in rows:      # journal order = chronological + wake order
            if r["evt"] == "HALT" and r["tranche_id"] == "equity_floor":
                floored_at = r["ts_open"]
                halt_table[cell] = {"ts": r["ts_open"],
                                    "equity_at_breach": r["size_r"]}
            elif floored_at and r["evt"] in FILL_EVTS:
                viol.append((cell, r["ts_open"], r["tranche_id"]))
    return {"violations": len(viol), "detail": viol[:10],
            "halt_table": halt_table, "match": not viol}


def f_g8b(p2):
    max_lev, worst, unresolved = 0.0, None, 0
    for cell, rows in p2.items():
        events = []
        exit_ts = {r["tranche_id"] for r in rows if r["evt"] == "EXIT"}
        for r in rows:
            if r["evt"] == "EXIT":
                ph = 2 if r["exit_reason"] == "stop" else 0
                events.append((parse_ms(r["ts_open"]), ph, "x",
                               r["pnl_usd"] or 0.0))
            elif r["evt"] in FILL_EVTS:
                if r["tranche_id"] not in exit_ts:
                    unresolved += 1
                events.append((parse_ms(r["ts_open"]), 1, "f",
                               abs(r["qty"]) * r["px_fill"]))
        events.sort(key=lambda e: (e[0], e[1]))
        eq = INITIAL_EQUITY
        for _, _, kind, val in events:
            if kind == "x":
                eq += val
            else:
                lev = val / eq
                if lev > max_lev:
                    max_lev, worst = lev, cell
    return {"max_notional_leverage": r6(max_lev), "worst_cell": worst,
            "fills_without_exit_row": unresolved,
            "match": max_lev <= MAX_LEV + 1e-6}


def f_g8c(p2):
    lo, worst, n = None, None, 0
    for cell, rows in p2.items():
        for r in rows:
            if r["evt"] in FILL_EVTS and r["atr_exec"]:
                n += 1
                ratio = abs(r["px_fill"] - r["stop"]) / r["atr_exec"]
                if lo is None or ratio < lo:
                    lo, worst = ratio, (cell, r["ts_open"])
    return {"fills": n, "min_stop_dist_atr": r6(lo), "worst": worst,
            "match": lo is not None and lo >= MIN_STOP_ATR - 1e-9}


def f_g8d(p2):
    bad = 0
    for rows in p2.values():
        for r in rows:
            if r["evt"] in FILL_EVTS:
                one_r = abs(r["px_fill"] - r["stop"]) * r["qty"] / r["size_r"]
                if one_r <= 0:
                    bad += 1
    return {"tranches_one_r_le_0": bad, "pass1_reference": 717,
            "match": bad == 0}


def f_eq(p2):
    lo, worst = INITIAL_EQUITY, None
    for cell, rows in p2.items():
        for r in rows:
            if r["evt"] == "EXIT" and r["equity_after"] is not None:
                if r["equity_after"] < lo:
                    lo, worst = r["equity_after"], (cell, r["ts_open"])
    return {"min_equity": lo, "worst": worst, "pass1_reference": -2732.24,
            "match": lo >= 0.0}


def f_cls(p2):
    census, viol = Counter(), 0
    fills = 0
    for rows in p2.values():
        for r in rows:
            has = "fill_class" in r and "concurrent_open_at_fill" in r
            if r["evt"] in FILL_EVTS:
                fills += 1
                if not has:
                    viol += 1
                    continue
                census[r["fill_class"]] += 1
                if r["evt"] == "ADD_FILL":
                    if (r["fill_class"] == "re_entry") != \
                            (r["concurrent_open_at_fill"] == 0):
                        viol += 1
                    if r["fill_class"] not in ("true_add", "re_entry"):
                        viol += 1
                elif r["fill_class"] not in ("r1", "v"):
                    viol += 1
            elif has:
                viol += 1        # additive fields must stay fill-only
    return {"census": dict(census), "total_fills": fills,
            "census_sum": sum(census.values()), "violations": viol,
            "match": viol == 0 and sum(census.values()) == fills}


def f_ext(p2):
    viol, flagged = 0, 0
    for rows in p2.values():
        fill_ms = {r["tranche_id"]: parse_ms(r["ts_open"])
                   for r in rows if r["evt"] in FILL_EVTS}
        for r in rows:
            if r["evt"] != "EXIT" or not r.get("engagement_flags"):
                continue
            fl = r["engagement_flags"]
            if "ext_i_offset" not in fl or "mfe_at_ext_r" not in fl:
                viol += 1
                continue
            if fl["ext_before_exit"]:
                flagged += 1
                if r["tranche_id"] not in fill_ms:
                    viol += 1
                    continue
                bars = (parse_ms(r["ts_open"]) - fill_ms[r["tranche_id"]]) \
                    // INTERVAL_MS[r["tf_exec"]]
                if fl["ext_i_offset"] is None or fl["mfe_at_ext_r"] is None \
                        or fl["ext_i_offset"] > bars:
                    viol += 1
            else:
                if fl["ext_i_offset"] is not None or \
                        fl["mfe_at_ext_r"] is not None:
                    viol += 1
    return {"exit_rows_flagged": flagged, "violations": viol,
            "match": viol == 0}


def f_det(manifest):
    mism = []
    for cell, t in manifest["cells"].items():
        a = files_sha256(PASS2 / cell)
        b = files_sha256(RUN2 / cell)
        if not (a == b == t["sha256"] == t["rerun_sha256"]):
            mism.append(cell)
    return {"cells": len(manifest["cells"]), "mismatched": mism,
            "manifest_flag": manifest["determinism_all_identical"],
            "match": not mism and manifest["determinism_all_identical"]}


# ------------------------------------------------------------------ book
class Book:
    """Tranche/campaign view of journal_pass2 (trimmed rc_recompute.Book)."""

    def __init__(self, cells_rows):
        self.tr = []
        self.rejects = Counter()
        self.halts = defaultdict(list)
        for cell, rows in cells_rows.items():
            exit_by = {r["tranche_id"]: r for r in rows if r["evt"] == "EXIT"}
            for r in rows:
                if r["evt"] == "REJECT":
                    self.rejects[r["reject_reason"]] += 1
                elif r["evt"] == "HALT":
                    self.halts[cell].append(r)
                if r["evt"] not in FILL_EVTS:
                    continue
                m = TID_RE.match(r["tranche_id"] or "")
                if not m:
                    continue
                e = exit_by.get(r["tranche_id"])
                one_r = abs(r["px_fill"] - r["stop"]) * r["qty"] / r["size_r"]
                rec = {
                    "cell_id": cell, "mandate": cell.rpartition("_")[2],
                    "asset": cell.rpartition("_")[0],
                    "camp": (cell, int(m.group(1))), "seq": int(m.group(2)),
                    "fill_ts": r["ts_open"], "size_r": r["size_r"],
                    "one_r": one_r, "fill_class": r.get("fill_class"),
                    "conc": r.get("concurrent_open_at_fill"),
                    "grade": r["grade"], "zone": r["zone"] or "-",
                    "resolved": e is not None,
                }
                if e:
                    cost = (e["fees"] or 0.0) + (e["funding_cum"] or 0.0) + \
                        (e["slippage"] or 0.0)
                    rec.update({
                        "realized_r": e["realized_r"],
                        "cost_r": cost / one_r,
                        "r_0x": e["realized_r"] + cost / one_r,
                        "r_2x": e["realized_r"] - cost / one_r,
                        "cohort": e.get("cohort"),
                        "exit_reason": e["exit_reason"],
                    })
                self.tr.append(rec)
        self.camp_tr = defaultdict(list)
        for x in self.tr:
            self.camp_tr[x["camp"]].append(x)
        for c in self.camp_tr:
            self.camp_tr[c].sort(key=lambda x: (x["fill_ts"], x["seq"]))
        self.camps = sorted(c for c in self.camp_tr
                            if any(x["resolved"] for x in self.camp_tr[c]))
        self.t = [x for x in self.tr if x["resolved"]]


def camp_agg(book, camps):
    v1, v0, v2 = [], [], []
    for c in camps:
        s1 = s0 = s2 = 0.0
        for x in book.camp_tr[c]:
            if x["resolved"]:
                s1 += x["realized_r"]
                s0 += x["r_0x"]
                s2 += x["r_2x"]
        v1.append(s1)
        v0.append(s0)
        v2.append(s2)
    n = len(v1)
    if not n:
        return {"campaigns": 0}
    lo, hi = boot_ci(v1)
    best = max(v1)
    return {
        "campaigns": n,
        "sum_0x": r4(sum(v0)), "sum_1x": r4(sum(v1)), "sum_2x": r4(sum(v2)),
        "expectancy_1x": r4(sum(v1) / n), "ci95_lo": lo, "ci95_hi": hi,
        "win_rate_pct": pct(sum(1 for v in v1 if v > 0), n),
        "strip_best_sum_1x": r4(sum(v1) - best),
        "strip_best_expectancy_1x": r4((sum(v1) - best) / (n - 1)) if n > 1 else None,
        "best_campaign_r": r4(best),
    }


def unit_agg(ts):
    ts = [x for x in ts if x["resolved"]]
    n = len(ts)
    if not n:
        return {"n": 0}
    ssize = sum(x["size_r"] for x in ts)
    return {
        "n": n, "sum_size_r": r4(ssize),
        "sum_cell_r_0x": r4(sum(x["r_0x"] for x in ts)),
        "sum_cell_r_1x": r4(sum(x["realized_r"] for x in ts)),
        "sum_cell_r_2x": r4(sum(x["r_2x"] for x in ts)),
        "per_unit_gross_0x": r4(sum(x["r_0x"] for x in ts) / ssize),
        "per_unit_net_1x": r4(sum(x["realized_r"] for x in ts) / ssize),
        "per_unit_cost": r4(sum(x["cost_r"] for x in ts) / ssize),
        "win_rate_pct": pct(sum(1 for x in ts if x["realized_r"] > 0), n),
    }


# ------------------------------------------------------------------ main
def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    expect = json.loads(EXPECT.read_text(encoding="utf-8"))
    p1 = load_cells(PASS1)
    p2 = load_cells(PASS2)

    fixtures = {
        "F-SIG": f_sig(p1, p2),
        "F-G8a": f_g8a(p2),
        "F-G8b": f_g8b(p2),
        "F-G8c": f_g8c(p2),
        "F-G8d": f_g8d(p2),
        "F-EQ": f_eq(p2),
        "F-CLS": f_cls(p2),
        "F-EXT": f_ext(p2),
        "F-DET": f_det(manifest),
    }
    print("== TC-4 fixtures ==")
    for k, v in fixtures.items():
        print(f"{k:<6} {'MATCH' if v['match'] else '*** VIOLATION ***'}  "
              + json.dumps({kk: vv for kk, vv in v.items()
                            if kk not in ("match", "halt_table", "detail")},
                           default=str)[:200])
    n_match = sum(1 for v in fixtures.values() if v["match"])
    if n_match < 9:
        print(f"\n*** HALT: {9 - n_match} fixture violation(s). "
              "A guard that does not provably hold does not exist. ***")
        return 1

    # -------- predictions --------
    halt_cells = set(fixtures["F-G8a"]["halt_table"])
    halt_dates = {c: v["ts"][:10] for c, v in
                  fixtures["F-G8a"]["halt_table"].items()}
    date_delta = {}
    for c in halt_cells:
        exp = expect.get(c, {}).get("first_floor_cross")
        if exp:
            d = (datetime.fromisoformat(halt_dates[c])
                 - datetime.fromisoformat(exp[:10])).days
            date_delta[c] = d
    a_ok = FIVE_INTRADAY <= halt_cells and \
        halt_cells <= FIVE_INTRADAY | {COIN_FLIP_CELL}
    early = {c: d for c, d in date_delta.items() if d < -90}
    book = Book(p2)
    grid = camp_agg(book, book.camps)
    predictions = {
        "P-TC4a": {
            "prior_pct": 85,
            "halt_set": sorted(halt_cells),
            "halt_dates": halt_dates,
            "days_vs_expectation": date_delta,
            "halts_more_than_90d_early": early,
            "verdict": "CONFIRMED" if a_ok else "FALSIFIED",
        },
        "P-TC4a'": {
            "prior_pct": 50,
            "zec_swing_halted": COIN_FLIP_CELL in halt_cells,
            "verdict": ("CONFIRMED" if COIN_FLIP_CELL in halt_cells
                        else "FALSIFIED"),
            "note": "registered as a genuine coin flip",
        },
        "P-TC4b": {
            "prior_pct": 65, "band": [-2400.0, -800.0],
            "grid_sum_1x": grid["sum_1x"],
            "verdict": ("CONFIRMED" if -2400.0 <= grid["sum_1x"] <= -800.0
                        else "FALSIFIED"),
        },
        "P-TC4c": {
            "prior_pct": 60, "band": [1900, 2700],
            "campaigns": grid["campaigns"],
            "verdict": ("CONFIRMED" if 1900 <= grid["campaigns"] <= 2700
                        else "FALSIFIED"),
        },
        "P-TC4d": {
            "prior_pct": 65, "threshold_pct": 11.0,
            "win_rate_pct": grid["win_rate_pct"],
            "verdict": ("CONFIRMED" if grid["win_rate_pct"] >= 11.0
                        else "FALSIFIED"),
        },
    }
    print("\n== predictions ==")
    for k, v in predictions.items():
        print(f"{k:<8} {v['verdict']}")

    # -------- rollup --------
    by_mandate = {m: camp_agg(book, [c for c in book.camps
                                     if c[0].endswith("_" + m)])
                  for m in ("swing", "intraday", "position")}
    assets = sorted({x["asset"] for x in book.tr})
    by_asset = {a: camp_agg(book, [c for c in book.camps
                                   if c[0].startswith(a + "_")])
                for a in assets}
    by_class = {fc: unit_agg([x for x in book.t if x["fill_class"] == fc])
                for fc in ("r1", "v", "true_add", "re_entry")}
    cohorts = Counter(x["cohort"] for x in book.t if x.get("cohort"))
    grades = Counter(x["grade"] if x["grade"] in ("A+", "A", "B") else "-"
                     for x in book.t)
    fill_census = Counter(x["fill_class"] for x in book.tr)
    per_cell = {}
    for cell in sorted(manifest["cells"]):
        rows = p2[cell]
        eqs = [r["equity_after"] for r in rows
               if r["evt"] == "EXIT" and r["equity_after"] is not None]
        halts = Counter(r["tranche_id"] for r in rows if r["evt"] == "HALT")
        per_cell[cell] = {
            "final_equity": manifest["cells"][cell]["final_equity"],
            "min_equity": min(eqs, default=INITIAL_EQUITY),
            "floor_halt": halt_dates.get(cell),
            "halt_rows": dict(halts),
            "tranches": sum(1 for x in book.tr if x["cell_id"] == cell),
            "campaigns": sum(1 for c in book.camps if c[0] == cell),
        }
    baseline = {
        "phase": "TC-4 engine 1.0.8 re-anchor (new baseline)",
        "supersedes": "journal_pass1 (engine 1.0.7 / v12_anchor); "
                      "pass 1 retained read-only",
        "engine_version": manifest["engine_version"],
        "config_id": manifest["config_id"],
        "config_sha256": manifest["config_sha256"],
        "grid_evidence_hash": manifest["grid_evidence_hash"],
        "determinism_all_identical": manifest["determinism_all_identical"],
        "seed": SEED, "n_boot": N_BOOT,
        "fixtures": fixtures,
        "predictions": predictions,
        "headline_grid": grid,
        "tranches_total": len(book.tr),
        "tranches_resolved": len(book.t),
        "by_mandate": by_mandate,
        "by_asset": by_asset,
        "fill_class_census": dict(fill_census),
        "fill_class_agg": by_class,
        "cohort_census": dict(cohorts),
        "grade_census": dict(grades),
        "reject_census": dict(book.rejects),
        "per_cell": per_cell,
        "pass1_reference": {"grid_1x": -5756.9093,
                            "scored_clean_1x": -5093.7846,
                            "campaigns": 3456, "tranches": 8387,
                            "win_rate_pct": 11.28},
    }
    out_json = OUT_DIR.parent.parent / "tc4_baseline.json"
    out_json.write_text(json.dumps(baseline, indent=1, sort_keys=True) + "\n",
                        encoding="utf-8", newline="\n")
    out_md = OUT_DIR.parent.parent / "TC4_BASELINE.md"
    out_md.write_text(render_md(baseline), encoding="utf-8", newline="\n")
    print(f"\n9/9 fixtures MATCH — wrote {out_json} and {out_md}")
    print("grid:", json.dumps(grid))
    print("OUTPUT_HASH json:",
          hashlib.sha256(out_json.read_bytes()).hexdigest())
    print("OUTPUT_HASH md:  ",
          hashlib.sha256(out_md.read_bytes()).hexdigest())
    return 0


def _agg_row(name, a):
    if a.get("campaigns", 0) == 0:
        return f"| {name} | 0 | — | — | — | — | — | — | — |"
    return (f"| {name} | {a['campaigns']} | {a['sum_0x']} | {a['sum_1x']} | "
            f"{a['sum_2x']} | {a['expectancy_1x']} "
            f"[{a['ci95_lo']}, {a['ci95_hi']}] | {a['win_rate_pct']}% | "
            f"{a['strip_best_sum_1x']} | {a['best_campaign_r']} |")


def _unit_row(name, u):
    if u.get("n", 0) == 0:
        return f"| {name} | 0 | — | — | — | — | — | — |"
    return (f"| {name} | {u['n']} | {u['sum_size_r']} | "
            f"{u['sum_cell_r_1x']} | {u['per_unit_gross_0x']} | "
            f"{u['per_unit_net_1x']} | {u['per_unit_cost']} | "
            f"{u['win_rate_pct']}% |")


def render_md(b):
    g = b["headline_grid"]
    L = []
    A = L.append
    A("# TC-4 BASELINE — engine 1.0.8 re-anchor (v12 study, new baseline)")
    A("")
    A(f"Engine **{b['engine_version']}** · config **{b['config_id']}** "
      f"(sha256 `{b['config_sha256'][:16]}…`) · grid evidence hash "
      f"`{b['grid_evidence_hash'][:16]}…` · determinism double-run "
      f"{'ALL IDENTICAL' if b['determinism_all_identical'] else 'MISMATCH'} "
      f"· bootstrap seed {b['seed']}, {b['n_boot']} resamples, "
      "campaign-level.")
    A("")
    A(f"**Supersedes** {b['supersedes']}.")
    A("")
    A("## Headline (scored 20-cell grid)")
    A("")
    A(f"- Grid net R (1×): **{g['sum_1x']}** over {g['campaigns']} campaigns "
      f"(pass 1: {b['pass1_reference']['grid_1x']} over "
      f"{b['pass1_reference']['campaigns']})")
    A(f"- Expectancy (1×): **{g['expectancy_1x']} R/campaign**, "
      f"CI95 [{g['ci95_lo']}, {g['ci95_hi']}]")
    A(f"- 0× (gross) {g['sum_0x']} · 2× (stress) {g['sum_2x']} — "
      "the cost stack still decides the sign" if g['sum_0x'] > 0 > g['sum_1x']
      else f"- 0× (gross) {g['sum_0x']} · 2× (stress) {g['sum_2x']}")
    A(f"- Win rate: **{g['win_rate_pct']}%** (pass-1 clean reference "
      f"{b['pass1_reference']['win_rate_pct']}%)")
    A(f"- Strip-best: {g['strip_best_sum_1x']} "
      f"(best campaign +{g['best_campaign_r']})")
    A(f"- Tranches: {b['tranches_total']} total / "
      f"{b['tranches_resolved']} resolved "
      f"(pass 1: {b['pass1_reference']['tranches']})")
    A("")
    A("## Fixtures (9/9 MATCH)")
    A("")
    A("| # | result |")
    A("|---|---|")
    for k, v in b["fixtures"].items():
        keep = {kk: vv for kk, vv in v.items()
                if kk not in ("match", "halt_table", "detail")}
        A(f"| {k} | MATCH — `{json.dumps(keep, default=str)[:160]}` |")
    A("")
    A("## Prediction scorecard")
    A("")
    A("| # | prior | verdict | measured |")
    A("|---|---|---|---|")
    for k, v in b["predictions"].items():
        keep = {kk: vv for kk, vv in v.items()
                if kk not in ("verdict", "prior_pct")}
        A(f"| {k} | {v['prior_pct']}% | **{v['verdict']}** | "
          f"`{json.dumps(keep, default=str)[:200]}` |")
    A("")
    A("## Halt table (equity floor, permanent)")
    A("")
    A("| cell | floor halt | equity at breach | final equity |")
    A("|---|---|---|---|")
    ht = b["fixtures"]["F-G8a"]["halt_table"]
    for c in sorted(b["per_cell"]):
        pc = b["per_cell"][c]
        if pc["floor_halt"]:
            A(f"| {c} | {ht[c]['ts']} | {ht[c]['equity_at_breach']} | "
              f"{pc['final_equity']} |")
    A("")
    A("## 0×/1×/2× by mandate and asset (campaign-level)")
    A("")
    A("| slice | campaigns | 0× | 1× | 2× | expectancy 1× [CI95] | win | "
      "strip-best 1× | best |")
    A("|---|---|---|---|---|---|---|---|---|")
    A(_agg_row("GRID", g))
    for m, a in b["by_mandate"].items():
        A(_agg_row(m, a))
    for s, a in b["by_asset"].items():
        A(_agg_row(s, a))
    A("")
    A("## fill_class census (first baseline to carry one)")
    A("")
    A(f"Census over ALL fills: `{json.dumps(b['fill_class_census'])}` "
      f"(Σ = {sum(b['fill_class_census'].values())} = total fills; F-CLS).")
    A("")
    A("| class | n (resolved) | Σsize_r | Σcell-R 1× | per-unit 0× | "
      "per-unit 1× | per-unit cost | win |")
    A("|---|---|---|---|---|---|---|---|")
    for fc, u in b["fill_class_agg"].items():
        A(_unit_row(fc, u))
    A("")
    A("## Taxonomy")
    A("")
    A(f"- Cohorts (resolved tranches): `{json.dumps(b['cohort_census'])}`")
    A(f"- Grades (resolved tranches; '-' = ungraded/V): "
      f"`{json.dumps(b['grade_census'])}`")
    A(f"- Rejects: `{json.dumps(b['reject_census'])}`")
    A("")
    A("## Per-cell")
    A("")
    A("| cell | campaigns | tranches | min equity | final equity | "
      "floor halt |")
    A("|---|---|---|---|---|---|")
    for c, pc in b["per_cell"].items():
        A(f"| {c} | {pc['campaigns']} | {pc['tranches']} | "
          f"{pc['min_equity']} | {pc['final_equity']} | "
          f"{pc['floor_halt'] or '—'} |")
    A("")
    A("*Generated by scripts/tc4_fixtures.py from journal_pass2 raw bytes; "
      "journal_pass1 remains on disk, read-only — falsifiable history, not "
      "erased history.*")
    A("")
    return "\n".join(L)


if __name__ == "__main__":
    raise SystemExit(main())
