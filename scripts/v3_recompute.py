#!/usr/bin/env python3
"""V3 Recompute R1-R10 — Tier A, journal arithmetic only.

Contract: V3_Recompute_R1_R10_Builder_Contract.md
Basis:    engine 1.0.7 (2f260e1), config v12_anchor (a3917ea5...),
          scored partition (exploration-classic), 20 cells.

READ-ONLY. No engine writes, no config edits, no replay, no network.
Reads raw journal JSONL bytes only. Prior summaries (ROLLUPS_AND_HYPOTHESES.md,
V3_STOP_AND_EXIT_FORENSICS.md) are NOT inputs.

Unit conventions (contract §4):
  cell-R   = realized_r as journaled (already size-weighted); additive.
  R/unit   = realized_r / size_r.
  one_r    = |px_fill - stop| * qty / size_r, from the ENTRY row (signed:
             qty is journaled signed, and is negative where a cell traded on
             negative equity — the literal formula reproduces F3/F4).
  cost     = fees + funding_cum + slippage, from the EXIT row (cumulative).
  r_0x     = realized_r + cost/one_r     (gross)
  r_2x     = realized_r - cost/one_r
  exit_XA..XD are per-unit R and carry NO costs -> cell-R = exit_X * size_r,
  compared against the 0x line only.

Usage: python scripts/v3_recompute.py [--journal-root PATH] [--out-dir PATH]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

# ---------------------------------------------------------------- constants

SEED = 20260715          # pinned bootstrap seed (contract invariant 6)
N_BOOT = 10_000          # resamples
MANDATES = ["swing", "intraday", "position"]
GRID = "GRID"
ROWS_KEPT = {"ENTRY_FILL", "ADD_FILL", "EXIT", "REJECT"}
TID_RE = re.compile(r"^c(\d+)t(\d+)$")

FIXTURES = {
    "F1_campaigns": 3456,
    "F1_tranches": 8387,
    "F2_sum_realized_r": -5756.9093,
    "F3_sum_r_0x": 1345.3095,
    "F4_sum_r_2x": -12859.1281,
    "F5_taxonomy": {"PROTECTED": 3381, "STILLBORN": 2076,
                    "NEVER_GREEN": 1830, "FADED": 1100},
    "F6_grades": {"A+": 39, "A": 1153, "B": 1954, "C": 0},
    "F7_stop_exits": 8365,
    "F8_v_campaigns": 45,
    "F9_r_cap_rejects": 0,
}
TOL = 1e-4

# Contract §6 R7 names the trading-layer tranche ceiling "tranche_cap".
# The engine (trading.py:459) emits it as "max_tranches". Same gate.
TRANCHE_CAP_REASON = "max_tranches"


# ---------------------------------------------------------------- utilities

def mandate_of(cell_id: str) -> str:
    return cell_id.rpartition("_")[2]


def camp_of(row: dict):
    m = TID_RE.match(row["tranche_id"] or "")
    return (row["cell_id"], int(m.group(1))) if m else None


def seq_of(row: dict):
    m = TID_RE.match(row["tranche_id"] or "")
    return int(m.group(2)) if m else None


def r4(x):
    return None if x is None else round(float(x) + 0.0, 4)


def r6(x):
    return None if x is None else round(float(x) + 0.0, 6)


def boot_ci(vals, seed=SEED, n=N_BOOT):
    """95% bootstrap CI of the mean. Fixed seed -> deterministic."""
    a = np.asarray(list(vals), dtype=float)
    if a.size < 2:
        return (None, None)
    rng = np.random.default_rng(seed)
    means = np.empty(n, dtype=float)
    step = 1000
    for s in range(0, n, step):
        k = min(step, n - s)
        idx = rng.integers(0, a.size, size=(k, a.size))
        means[s:s + k] = a[idx].mean(axis=1)
    return (r4(np.percentile(means, 2.5)), r4(np.percentile(means, 97.5)))


def pct(x, d):
    return None if not d else r4(100.0 * x / d)


# ---------------------------------------------------------------- load

def load_scored(root: Path):
    """Read raw journal bytes from the scored partition."""
    cells = sorted(p.name for p in root.iterdir() if p.is_dir())
    rows = []
    evt_census = Counter()
    for cell in cells:
        for path in sorted((root / cell).glob("*.jsonl")):
            with open(path, encoding="utf-8") as f:
                for line in f:
                    if not line.strip():
                        continue
                    r = json.loads(line)
                    evt_census[r["evt"]] += 1
                    if r["evt"] in ROWS_KEPT:
                        rows.append(r)
    return cells, rows, evt_census


class Book:
    """Joined tranche-level view of the scored partition."""

    def __init__(self, rows):
        self.exits = [r for r in rows if r["evt"] == "EXIT"]
        self.fills = [r for r in rows if r["evt"] in ("ENTRY_FILL", "ADD_FILL")]
        self.rejects = [r for r in rows if r["evt"] == "REJECT"]
        self.fill_by = {(r["cell_id"], r["tranche_id"]): r for r in self.fills}

        # deterministic order: cell, campaign, seq
        self.exits.sort(key=lambda r: (r["cell_id"], camp_of(r)[1], seq_of(r)))

        self.t = []          # one record per resolved tranche
        for e in self.exits:
            f = self.fill_by[(e["cell_id"], e["tranche_id"])]
            one_r = abs(f["px_fill"] - f["stop"]) * f["qty"] / f["size_r"]
            cost = (e["fees"] or 0.0) + (e["funding_cum"] or 0.0) \
                + (e["slippage"] or 0.0)
            c_r = cost / one_r
            sh = e.get("shadow") or {}
            fl = e.get("engagement_flags") or {}
            self.t.append({
                "cell_id": e["cell_id"],
                "mandate": mandate_of(e["cell_id"]),
                "camp": camp_of(e),
                "seq": seq_of(e),
                "tranche_id": e["tranche_id"],
                "dir": e["dir"],
                "grade": e["grade"],
                "zone": e["zone"],
                "retr": e["retr"],
                "size_r": e["size_r"],
                "is_v": sh.get("ladder_unthrottled_grade") == "V",
                "is_add": f["evt"] == "ADD_FILL",
                "realized_r": e["realized_r"],      # cell-R, 1x
                "cost_r": c_r,
                "r_0x": e["realized_r"] + c_r,
                "r_2x": e["realized_r"] - c_r,
                "one_r": one_r,
                "cost": cost,
                "fees": e["fees"] or 0.0,
                "funding": e["funding_cum"] or 0.0,
                "slippage": e["slippage"] or 0.0,
                "entry_fee": f["fees"] or 0.0,
                "entry_slip": f["slippage"] or 0.0,
                "entry_px": f["px_fill"],
                "entry_stop": f["stop"],
                "entry_atr": f["atr_exec"],
                "exit_stop": e["stop"],
                "exit_reason": e["exit_reason"],
                "cohort": e["cohort"],
                "mfe_r": e["mfe_r"],
                "mae_r": e["mae_r"],
                "cont_20": e["postexit_cont_20"],
                "ts_open": e["ts_open"],
                "stage": f["stage"],
                "xa": sh.get("exit_XA"), "xb": sh.get("exit_XB"),
                "xc": sh.get("exit_XC"), "xd": sh.get("exit_XD"),
                "tpw_before": fl.get("tpw_before_exit"),
                "ext_before": fl.get("ext_before_exit"),
            })

        # campaigns = distinct (cell_id, campaign) over resolved tranches
        self.camp_tr = defaultdict(list)
        for x in self.t:
            self.camp_tr[x["camp"]].append(x)
        self.camps = sorted(self.camp_tr)

        # initiating tranche of each campaign (lowest seq among fills)
        first_fill = {}
        for f in self.fills:
            c = camp_of(f)
            s = seq_of(f)
            if c is None:
                continue
            if c not in first_fill or s < first_fill[c][0]:
                first_fill[c] = (s, f)
        self.first_fill = first_fill
        v_tids = {(x["cell_id"], x["tranche_id"]) for x in self.t if x["is_v"]}
        self.v_camps = {c for c, (s, f) in first_fill.items()
                        if (f["cell_id"], f["tranche_id"]) in v_tids
                        and c in self.camp_tr}

    def camp_r(self, camp, key="realized_r"):
        return sum(x[key] for x in self.camp_tr[camp])


# ---------------------------------------------------------------- fixtures

def fixtures(book: Book, evt_census: Counter, cfg_max_r_count):
    out = []

    def add(name, expected, computed, ok=None):
        if ok is None:
            if isinstance(expected, float):
                ok = abs(computed - expected) <= TOL
            else:
                ok = computed == expected
        out.append({"fixture": name, "expected": expected,
                    "computed": computed, "match": bool(ok)})

    add("F1 campaigns", FIXTURES["F1_campaigns"], len(book.camps))
    add("F1 resolved tranches", FIXTURES["F1_tranches"], len(book.t))
    add("F2 sum(realized_r) cell-R", FIXTURES["F2_sum_realized_r"],
        r4(sum(x["realized_r"] for x in book.t)))
    add("F3 sum(r_0x) cell-R", FIXTURES["F3_sum_r_0x"],
        r4(sum(x["r_0x"] for x in book.t)))
    add("F4 sum(r_2x) cell-R", FIXTURES["F4_sum_r_2x"],
        r4(sum(x["r_2x"] for x in book.t)))

    tax = dict(Counter(x["cohort"] for x in book.t))
    add("F5 taxonomy census", FIXTURES["F5_taxonomy"],
        {k: tax.get(k, 0) for k in FIXTURES["F5_taxonomy"]})

    # F6: campaigns initiated by a non-V ENTRY_FILL (R1 PRIME), by that
    # tranche's journaled (capped) grade.
    v_tids = {(x["cell_id"], x["tranche_id"]) for x in book.t if x["is_v"]}
    g = Counter()
    for c, (s, f) in book.first_fill.items():
        if c not in book.camp_tr:
            continue
        if f["evt"] != "ENTRY_FILL":
            continue
        if (f["cell_id"], f["tranche_id"]) in v_tids:
            continue
        g[f["grade"]] += 1
    add("F6 grade cohorts (campaigns)", FIXTURES["F6_grades"],
        {k: g.get(k, 0) for k in FIXTURES["F6_grades"]})

    add("F7 stop + stop_gap exits", FIXTURES["F7_stop_exits"],
        sum(1 for x in book.t if x["exit_reason"] in ("stop", "stop_gap")))
    add("F8 V-initiated campaigns", FIXTURES["F8_v_campaigns"],
        len(book.v_camps))

    sig_rej = [r for r in book.rejects
               if not (r["tranche_id"] or "").startswith("trade_")]
    rcap = sum(1 for r in sig_rej if r["reject_reason"] == "r_cap")
    add("F9 signal-layer r_cap rejects", FIXTURES["F9_r_cap_rejects"], rcap)
    return out, rcap


# ---------------------------------------------------------------- helpers

def data_characteristics(book):
    """Facts about the anchor run the tables below inherit. Not a deliverable;
    reported because they change how the deliverables must be read."""
    neg = [x for x in book.t if x["one_r"] < 0]
    by_cell = Counter(x["cell_id"] for x in neg)
    out = {"negative_one_r_tranches": len(neg),
           "negative_one_r_by_cell": dict(by_cell)}
    if neg:
        cells = sorted(by_cell)
        detail = {}
        for c in cells:
            ts = [x for x in book.t if x["cell_id"] == c]
            detail[c] = {
                "tranches_total": len(ts),
                "tranches_with_negative_one_r": by_cell[c],
                "sum_cell_r_1x": r4(sum(x["realized_r"] for x in ts)),
            }
        out["detail"] = detail
        out["finding"] = (
            "one_r = r_pct * equity at fill time (trading.py:367). A NEGATIVE "
            "one_r therefore means the cell's realized equity had gone BELOW "
            "ZERO and the book kept trading against it, with qty inverting "
            "sign. This is journaled faithfully and the §4 formula reproduces "
            "F3/F4 exactly with the signed value, so it is NOT a reader "
            "artifact and NOT a fixture failure -- but every R-denominated "
            "quantity on those rows is measured against a negative unit, which "
            "flips the sign of their cost adjustment. Downstream reader: treat "
            "this cell's contribution to any aggregate with suspicion, and note "
            "that a bankrupt-cell-keeps-trading path is itself a finding about "
            "the anchor run rather than about the strategy.")
    return out


def by_mandate(items, keyfn):
    """{GRID: [...], swing: [...], ...} preserving input order."""
    out = {GRID: list(items)}
    for m in MANDATES:
        out[m] = [x for x in items if keyfn(x) == m]
    return out


def agg_tranche(ts):
    n = len(ts)
    return {
        "n": n,
        "sum_0x": r4(sum(x["r_0x"] for x in ts)),
        "sum_1x": r4(sum(x["realized_r"] for x in ts)),
        "sum_2x": r4(sum(x["r_2x"] for x in ts)),
        "win_rate_1x": pct(sum(1 for x in ts if x["realized_r"] > 0), n),
        "expectancy_1x": r4(sum(x["realized_r"] for x in ts) / n) if n else None,
    }


def camp_agg(book, camps, weightfn=None, label=""):
    """Campaign-level aggregate + CI + strip-best."""
    vals, v0, v2 = [], [], []
    for c in camps:
        s1 = s0 = s2 = 0.0
        for x in book.camp_tr[c]:
            w = 1.0 if weightfn is None else weightfn(x)
            if w == 0.0:
                continue
            s1 += x["realized_r"] * w
            s0 += x["r_0x"] * w
            s2 += x["r_2x"] * w
        vals.append(s1)
        v0.append(s0)
        v2.append(s2)
    n = len(vals)
    if not n:
        return {"campaigns": 0}
    lo, hi = boot_ci(vals)
    best = max(vals) if vals else 0.0
    strip = sum(vals) - best
    return {
        "campaigns": n,
        "sum_0x": r4(sum(v0)),
        "sum_1x": r4(sum(vals)),
        "sum_2x": r4(sum(v2)),
        "expectancy_1x": r4(sum(vals) / n),
        "ci95_lo": lo, "ci95_hi": hi,
        "win_rate": pct(sum(1 for v in vals if v > 0), n),
        "strip_best_sum_1x": r4(strip),
        "strip_best_expectancy_1x": r4(strip / (n - 1)) if n > 1 else None,
        "best_campaign_r": r4(best),
    }


# ---------------------------------------------------------------- R1

def R1(book):
    out = {"caveat": "First-order. A really-adopted exit rule changes which "
                     "adds fire and when campaigns die. Rank, do not validate. "
                     "Variants carry no costs -> compared against the 0x line "
                     "only. Their 1x/2x lines apply the row's ACTUAL cost/one_r "
                     "as a PROXY: the counterfactual exits at a different price "
                     "and holds for a different duration, so its true exit fee "
                     "and funding differ.",
           "basis": "cell-R = exit_X * size_r; actual gross = sum(r_0x)",
           "variants": {}}
    groups = by_mandate(book.t, lambda x: x["mandate"])
    for var in ("xa", "xb", "xc", "xd"):
        vo = {}
        for g, ts in groups.items():
            ts = [x for x in ts if x[var] is not None]
            n = len(ts)
            s0 = sum(x[var] * x["size_r"] for x in ts)
            cost = sum(x["cost_r"] for x in ts)
            actual0 = sum(x["r_0x"] for x in ts)
            vo[g] = {
                "n": n,
                "sum_0x": r4(s0),
                "sum_1x_proxy": r4(s0 - cost),
                "sum_2x_proxy": r4(s0 - 2 * cost),
                "actual_sum_0x": r4(actual0),
                "delta_vs_actual_0x": r4(s0 - actual0),
                "win_rate_0x": pct(sum(1 for x in ts if x[var] > 0), n),
                "expectancy_0x": r4(s0 / n) if n else None,
            }
        out["variants"][var.upper().replace("X", "X-")] = vo
    # actual book reference
    out["actual_book"] = {g: {"n": len(ts), "sum_0x": r4(sum(x["r_0x"] for x in ts)),
                              "win_rate_0x": pct(sum(1 for x in ts if x["r_0x"] > 0), len(ts))}
                          for g, ts in groups.items()}
    return out


# ---------------------------------------------------------------- R2

def R2(book):
    vc = sorted(book.v_camps)
    allc = book.camps
    out = {"discriminator":
           "V-initiated campaign = campaign whose lowest-seq fill tranche is a "
           "V. V identified per-tranche by EXIT.shadow.ladder_unthrottled_grade "
           "== 'V' (shadows.py:240 sets it to 'V' iff Tranche.kind == 'V'; "
           "kind is not otherwise journaled -- ENTRY_FILL covers both R1 and V). "
           "Checked by F8 = 45.",
           "v_campaigns": len(vc),
           "share_of_campaigns_pct": pct(len(vc), len(allc))}
    out["grid"] = camp_agg(book, vc)
    out["per_mandate"] = {}
    for m in MANDATES:
        cs = [c for c in vc if mandate_of(c[0]) == m]
        out["per_mandate"][m] = camp_agg(book, cs) if cs else {"campaigns": 0}

    # share of wins / losses vs the whole scored grid
    wins = losses = 0.0
    vwins = vlosses = 0.0
    for c in allc:
        r = book.camp_r(c)
        if r > 0:
            wins += r
            if c in book.v_camps:
                vwins += r
        elif r < 0:
            losses += r
            if c in book.v_camps:
                vlosses += r
    out["sum_wins_grid"] = r4(wins)
    out["sum_losses_grid"] = r4(losses)
    out["v_sum_wins"] = r4(vwins)
    out["v_sum_losses"] = r4(vlosses)
    out["v_share_of_wins_pct"] = pct(vwins, wins)
    out["v_share_of_losses_pct"] = pct(vlosses, losses)

    top = sorted(vc, key=lambda c: -book.camp_r(c))[:5]
    out["top5_by_cell_r"] = [{"campaign": f"{c[0]}#c{c[1]}",
                              "cell_r_1x": r4(book.camp_r(c)),
                              "tranches": len(book.camp_tr[c])} for c in top]
    return out


# ---------------------------------------------------------------- R3

def stop_class(x):
    """Field lens: EXIT.stop (fill level) vs ENTRY.stop (stop_at_entry)."""
    if x["exit_stop"] is None:
        return "no_stop_row"          # non-stop exits journal stop = null
    if abs(x["exit_stop"] - x["entry_stop"]) < 1e-9:
        return "initial"
    d = 1 if x["dir"] == "long" else -1
    # BE reached when the stop is at/through the entry fill on the trade's side
    if (x["exit_stop"] - x["entry_px"]) * d >= 0:
        return "ratcheted_ge_BE"
    return "ratcheted_below_BE"


def R3(book):
    out = {"purpose": "Raw material for FITTING a profit-arming threshold "
                      "instead of guessing +1R.",
           "population": "tranches that exited at a GROSS loss (r_0x < 0)",
           "deciles_of": "mfe_r (per-unit R), numpy.percentile linear "
                         "interpolation, 10th..90th",
           "grid": {}}
    pop = [x for x in book.t if x["r_0x"] < 0]
    out["n_population"] = len(pop)
    for sc in ("initial", "ratcheted_below_BE", "ratcheted_ge_BE", "no_stop_row"):
        for m in MANDATES:
            for g in ("A+", "A", "B"):
                ts = [x for x in pop if stop_class(x) == sc
                      and x["mandate"] == m and x["grade"] == g]
                if not ts:
                    continue
                mf = np.asarray([x["mfe_r"] for x in ts], dtype=float)
                out["grid"][f"{sc}|{m}|{g}"] = {
                    "n": len(ts),
                    "sum_cell_r_1x": r4(sum(x["realized_r"] for x in ts)),
                    "sum_cell_r_0x": r4(sum(x["r_0x"] for x in ts)),
                    "mfe_deciles": [r4(v) for v in
                                    np.percentile(mf, [10, 20, 30, 40, 50,
                                                       60, 70, 80, 90])],
                    "mfe_median": r4(np.percentile(mf, 50)),
                }
    out["structural_note"] = (
        "The 'ratcheted_ge_BE' class is EMPTY BY CONSTRUCTION for this "
        "population, not by accident: a stop resting at or beyond the entry "
        "fill on the trade's side cannot produce a gross loss when it is the "
        "exit level (gross P&L is measured at raw prices, before the costs "
        "that r_0x adds back). Any tranche whose stop reached breakeven and "
        "then filled leaves this population by definition. Read the absence as "
        "a tautology of the population filter, NOT as evidence that the "
        "ratchet never reaches breakeven.")
    # marginals
    out["by_stop_class"] = {}
    for sc in ("initial", "ratcheted_below_BE", "ratcheted_ge_BE", "no_stop_row"):
        ts = [x for x in pop if stop_class(x) == sc]
        if not ts:
            continue
        mf = np.asarray([x["mfe_r"] for x in ts], dtype=float)
        out["by_stop_class"][sc] = {
            "n": len(ts),
            "sum_cell_r_1x": r4(sum(x["realized_r"] for x in ts)),
            "mfe_deciles": [r4(v) for v in np.percentile(
                mf, [10, 20, 30, 40, 50, 60, 70, 80, 90])],
        }
    return out


# ---------------------------------------------------------------- R4

def R4(book):
    pop = [x for x in book.t if x["mfe_r"] is not None and x["mfe_r"] >= 1.0
           and x["r_0x"] < 0]
    out = {"population": "tranches with mfe_r >= +1R that exited at a GROSS "
                         "loss (r_0x < 0)",
           "n_population": len(pop),
           "route": "TPW IS journaled as an event row (evt='TPW'), but those "
                    "rows are per-cell/per-bar and carry no tranche_id, so they "
                    "do not answer 'before THIS tranche's exit'. The per-tranche "
                    "answer is journaled on the EXIT row as "
                    "engagement_flags.tpw_before_exit / .ext_before_exit "
                    "(shadows.py:257-260) -- that is the route taken. The "
                    "exit_XB fallback was NOT needed for the TPW count; it is "
                    "used only to recover R-at-first-trigger (see below).",
           "flag_semantics_warning":
               "THE TWO FLAGS DO NOT MEASURE THE SAME WINDOW, despite their "
               "paired names. "
               "(a) tpw_before_exit derives from Tranche.first_tpw_i, which "
               "trading.py:412-415 sets ONLY for tranches in open_tranches at "
               "the close of the TPW bar -- so it is genuinely 'while THIS "
               "tranche was open'. STRICT, answers the question as asked. "
               "(b) ext_before_exit derives from shadows.py:190-194, whose "
               "loop is `for j in range(tr.fill_i, last + 1)` with "
               "last = camp_end -- the CAMPAIGN-DEATH bar, NOT this tranche's "
               "exit bar (the engine's own comment says 'within the campaign'). "
               "It is therefore true whenever an extension occurred anywhere "
               "between this tranche's fill and campaign death, INCLUDING "
               "after this tranche was already stopped out. It is misnamed: it "
               "reads 'ext_before_CAMPAIGN_DEATH'. The strict 'before their "
               "exit' reading is NOT computable -- see partial below.",
           }
    grp = by_mandate(pop, lambda x: x["mandate"])
    out["counts"] = {}
    for g, ts in grp.items():
        n = len(ts)
        out["counts"][g] = {
            "n": n,
            "tpw_before_exit_STRICT": sum(1 for x in ts if x["tpw_before"]),
            "tpw_before_exit_STRICT_pct":
                pct(sum(1 for x in ts if x["tpw_before"]), n),
            "ext_before_CAMPAIGN_DEATH_loose":
                sum(1 for x in ts if x["ext_before"]),
            "ext_before_CAMPAIGN_DEATH_loose_pct":
                pct(sum(1 for x in ts if x["ext_before"]), n),
            "either_mixed_windows":
                sum(1 for x in ts if x["tpw_before"] or x["ext_before"]),
        }
    out["ext_strict_before_exit"] = "PARTIAL"
    out["ext_partial_reason"] = (
        "NOT COMPUTABLE from journaled fields. The extension's bar index "
        "(ext_i, shadows.py:190-194) is never journaled, and the only "
        "journaled flag (engagement_flags.ext_before_exit) is evaluated over "
        "[fill_i, camp_end] rather than [fill_i, exit_i], so it cannot be "
        "narrowed to 'before this tranche's exit' after the fact. "
        "MISSING FIELD: either the trigger bar index ('ext_i_offset', bars "
        "from fill) or a correctly-windowed boolean computed over "
        "[fill_i, exit_i]. ROW TYPE it would live on: the EXIT row, inside "
        "engagement_flags alongside the existing (mis-windowed) flag. "
        "No estimate substituted. The n_ext_recoverable count below is a "
        "genuine LOWER BOUND on the strict reading -- it counts only rows "
        "whose extension partial actually banked before the X-A shadow exit.")

    # ---- median MFE at the first trigger: NOT COMPUTABLE -> PARTIAL --------
    out["median_mfe_at_first_trigger"] = "PARTIAL"
    out["partial_reason"] = (
        "NOT COMPUTABLE from journaled fields. mfe_r on the EXIT row is the "
        "tranche's WHOLE-LIFE maximum favorable excursion (shadows.py:167), "
        "not its value at the trigger bar; the trigger bar index (tpw_i / "
        "ext_i, shadows.py:188-193) is never journaled. "
        "MISSING FIELD: an MFE-at-trigger column -- e.g. 'mfe_at_tpw_r' and "
        "'mfe_at_ext_r'. ROW TYPE it would live on: the EXIT row (alongside "
        "mfe_r / give_back_r), or equivalently a per-tranche TPW event row "
        "carrying tranche_id + running mfe_r. No estimate substituted.")
    # ---- what IS recoverable: R at the first trigger, via the XB/XC shadows
    # xb = 0.5*tpw_r + 0.5*xa  ->  tpw_r = 2*xb - xa   (xb_tpw_partial = 0.5)
    # xc = 0.5*ext_r + 0.5*xa  ->  ext_r = 2*xc - xa   (xc_partial     = 0.5)
    # Recoverable only when the partial actually banked before the X-A exit
    # (shadows.py:198-201 returns None if bar+1 > xa exit bar), which shows up
    # as xb == xa exactly.
    out["recoverable_R_at_first_trigger"] = {
        "definition": "per-unit R realized at the open AFTER the first "
                      "trigger, inverted from the shadow blend: "
                      "tpw_r = 2*exit_XB - exit_XA ; ext_r = 2*exit_XC - exit_XA. "
                      "This is R AT the trigger, NOT MFE at the trigger.",
        "per_mandate": {}}
    for g, ts in grp.items():
        tp = [2 * x["xb"] - x["xa"] for x in ts
              if x["tpw_before"] and x["xb"] is not None
              and abs(x["xb"] - x["xa"]) > 1e-9]
        ex = [2 * x["xc"] - x["xa"] for x in ts
              if x["ext_before"] and x["xc"] is not None
              and abs(x["xc"] - x["xa"]) > 1e-9]
        out["recoverable_R_at_first_trigger"]["per_mandate"][g] = {
            "n_tpw_recoverable": len(tp),
            "median_R_at_first_tpw": r4(np.median(tp)) if tp else None,
            "n_ext_recoverable": len(ex),
            "median_R_at_first_ext": r4(np.median(ex)) if ex else None,
            "note": "rows where the trigger fired but the partial did not bank "
                    "before the X-A exit are excluded (xb == xa exactly)",
        }
    return out


# ---------------------------------------------------------------- R5

def R5(book):
    stops = [x for x in book.t if x["exit_reason"] in ("stop", "stop_gap")
             and x["cont_20"] is not None]
    out = {"purpose": "C6's re-entry trigger needs the per-EVENT denominator, "
                      "not the per-tranche one.",
           "resumption_definition":
               "postexit_cont_20 >= 1.0 (per-unit R at exactly +20 exec bars "
               "after the exit). NOTE: only postexit_cont_{1,5,20} are "
               "journaled, so this is the value AT bar 20, not the max WITHIN "
               "20 bars -- a strict 'within' reading is not computable from "
               "journaled fields.",
           "event_key": "(cell_id, dir, ts_open) over stop/stop_gap EXIT rows",
           "event_representative":
               "per-unit quantities (postexit_cont_20) differ across tranches "
               "in one event because unit_risk is per-tranche; the event's "
               "lowest-seq tranche is the representative.",
           }
    # per-tranche
    res_t = [x for x in stops if x["cont_20"] >= 1.0]
    out["per_tranche"] = {
        "n": len(stops),
        "resumed_ge_1R_20b": len(res_t),
        "resumed_pct": pct(len(res_t), len(stops)),
        "forfeited_pool_cell_r": r4(sum(min(x["cont_20"], 10.0) * x["size_r"]
                                        for x in res_t)),
        "median_cont_20": r4(np.median([x["cont_20"] for x in stops]))
                          if stops else None,
    }
    # per-event
    ev = defaultdict(list)
    for x in stops:
        ev[(x["cell_id"], x["dir"], x["ts_open"])].append(x)
    keys = sorted(ev)
    reps = {k: min(ev[k], key=lambda x: x["seq"]) for k in keys}
    res_e = [k for k in keys if reps[k]["cont_20"] >= 1.0]
    out["per_event"] = {
        "n": len(keys),
        "resumed_ge_1R_20b": len(res_e),
        "resumed_pct": pct(len(res_e), len(keys)),
        "forfeited_pool_cell_r": r4(sum(
            sum(min(x["cont_20"], 10.0) * x["size_r"] for x in ev[k])
            for k in res_e)),
        "median_cont_20": r4(np.median([reps[k]["cont_20"] for k in keys]))
                          if keys else None,
        "tranches_per_event_mean": r4(len(stops) / len(keys)) if keys else None,
    }
    out["per_mandate"] = {}
    for m in MANDATES:
        st = [x for x in stops if x["mandate"] == m]
        ks = [k for k in keys if mandate_of(k[0]) == m]
        rt = [x for x in st if x["cont_20"] >= 1.0]
        re_ = [k for k in ks if reps[k]["cont_20"] >= 1.0]
        out["per_mandate"][m] = {
            "tranches": len(st), "tranches_resumed": len(rt),
            "events": len(ks), "events_resumed": len(re_),
            "events_resumed_pct": pct(len(re_), len(ks)),
            "forfeited_pool_cell_r_per_event": r4(sum(
                sum(min(x["cont_20"], 10.0) * x["size_r"] for x in ev[k])
                for k in re_)),
        }
    return out


# ---------------------------------------------------------------- R6

def R6(book):
    """Cross-tab over ENTRY_FILL + ADD_FILL rows (fills, not exits)."""
    out = {"purpose": "Tests P-R6.",
           "note": "Counts are over ALL ENTRY_FILL/ADD_FILL rows. Expectancy "
                   "and sum cell-R use the joined EXIT row; fills whose EXIT "
                   "is buffered (campaign open at data end) contribute to the "
                   "count but not to R.",
           "table": {}}
    r_by = {(x["cell_id"], x["tranche_id"]): x for x in book.t}
    fills = sorted(book.fills, key=lambda r: (r["cell_id"], r["tranche_id"]))
    out["n_fills"] = len(fills)
    out["n_fills_without_exit"] = sum(
        1 for f in fills if (f["cell_id"], f["tranche_id"]) not in r_by)

    def cell(rs):
        joined = [r_by[(f["cell_id"], f["tranche_id"])] for f in rs
                  if (f["cell_id"], f["tranche_id"]) in r_by]
        n = len(rs)
        s1 = sum(x["realized_r"] for x in joined)
        return {"n": n, "n_with_exit": len(joined),
                "sum_cell_r_1x": r4(s1),
                "sum_cell_r_0x": r4(sum(x["r_0x"] for x in joined)),
                "expectancy_1x": r4(s1 / len(joined)) if joined else None}

    for d in ("long", "short", "both"):
        rs_d = fills if d == "both" else [f for f in fills if f["dir"] == d]
        t = {}
        for z in ("Z1", "Z2", "Z3", "-"):
            for st in (1, 2):
                rs = [f for f in rs_d if (f["zone"] or "-") == z
                      and f["stage"] == st]
                if rs:
                    t[f"{z}|stage{st}"] = cell(rs)
        # stage nulls
        rs = [f for f in rs_d if f["stage"] not in (1, 2)]
        if rs:
            t["stage_null"] = cell(rs)
        out["table"][d] = t

    out["per_mandate"] = {}
    for m in MANDATES:
        rs_m = [f for f in fills if mandate_of(f["cell_id"]) == m]
        t = {}
        for z in ("Z1", "Z2", "Z3", "-"):
            for st in (1, 2):
                rs = [f for f in rs_m if (f["zone"] or "-") == z
                      and f["stage"] == st]
                if rs:
                    t[f"{z}|stage{st}"] = cell(rs)
        out["per_mandate"][m] = t

    # P-R6: Z2-active entries carrying stage 1
    z2 = [f for f in fills if (f["zone"] or "-") == "Z2"]
    z2s1 = [f for f in z2 if f["stage"] == 1]
    out["p_r6"] = {
        "z2_entries": len(z2),
        "z2_stage1": len(z2s1),
        "z2_stage1_pct": pct(len(z2s1), len(z2)),
        "z2_stage2": sum(1 for f in z2 if f["stage"] == 2),
    }

    # Degeneracy check: is the cross-tab actually a cross-tab?
    occ = {}
    for z in ("Z1", "Z2", "Z3", "-"):
        rs = [f for f in fills if (f["zone"] or "-") == z]
        if not rs:
            continue
        occ[z] = {"n": len(rs),
                  "stage1": sum(1 for f in rs if f["stage"] == 1),
                  "stage2": sum(1 for f in rs if f["stage"] == 2)}
    out["zone_stage_occupancy"] = occ
    degenerate = [z for z, v in occ.items()
                  if v["stage1"] == 0 or v["stage2"] == 0]
    out["degeneracy_finding"] = (
        "The cross-tab is NEARLY DEGENERATE: zone and stage are not "
        "independent in this run. Z2 fills are 100% stage-1 (0 stage-2) and "
        "Z3 fills are 100% stage-2 (0 stage-1) -- each of those zones occupies "
        "exactly ONE stage, so 2 of the 6 Z1/Z2/Z3 x stage cells are "
        "structurally empty rather than merely sparse. Only Z1 (and the "
        "no-zone '-' bucket) populate both stages. P-R6 is therefore CONFIRMED "
        "trivially at 100%, not marginally at >=95%: the prediction tested a "
        "coupling that appears to be enforced upstream, not a tendency. "
        "Zones with a single occupied stage: " + ", ".join(sorted(degenerate))
        + ". Anyone reading a Z2-vs-Z3 expectancy difference as a ZONE effect "
        "is also reading a STAGE effect -- the two are confounded here and "
        "cannot be separated from these journals.")
    return out


# ---------------------------------------------------------------- R7

def R7(book):
    out = {"layer_discriminator":
           "REJECT row whose tranche_id starts with 'trade_' is a "
           "TRADING-layer reject (replay.py:228); otherwise SIGNAL-layer "
           "(subkey 'prime'/'confirm').",
           "naming_note":
               "Contract §6 R7 calls the tranche ceiling 'tranche_cap'; the "
               "engine emits it as reject_reason='max_tranches' "
               "(trading.py:459). Same gate -- reported under both names.",
           }
    sig = [r for r in book.rejects
           if not (r["tranche_id"] or "").startswith("trade_")]
    trd = [r for r in book.rejects if (r["tranche_id"] or "").startswith("trade_")]
    out["totals"] = {"signal_layer": len(sig), "trading_layer": len(trd),
                     "all": len(book.rejects)}

    def census(rs):
        return dict(sorted(Counter(r["reject_reason"] for r in rs).items(),
                           key=lambda kv: (-kv[1], kv[0])))

    out["signal_layer"] = {GRID: census(sig)}
    out["trading_layer"] = {GRID: census(trd)}
    for m in MANDATES:
        out["signal_layer"][m] = census(
            [r for r in sig if mandate_of(r["cell_id"]) == m])
        out["trading_layer"][m] = census(
            [r for r in trd if mandate_of(r["cell_id"]) == m])

    sc = out["signal_layer"][GRID]
    tc = out["trading_layer"][GRID]
    out["load_bearing"] = {
        "r_cap_F9": sc.get("r_cap", 0),
        "tranche_cap_max_tranches": tc.get(TRANCHE_CAP_REASON, 0),
        "add_ineligible": tc.get("add_ineligible", 0),
        "no_zone": sc.get("no_zone", 0),
        "ribbon_sep": sc.get("ribbon_sep", 0),
    }
    return out


# ---------------------------------------------------------------- R8

def R8(book):
    out = {"note": "Report 1 published Z2 vs Z1 and never published Z3. Z3 is "
                   "the governor 89-200 band retest cohort and the operator's "
                   "stated primary structural setup. Gap closed here.",
           "tranche_level": {}, "campaign_level": {}}
    for z in ("Z1", "Z2", "Z3"):
        ts = [x for x in book.t if x["zone"] == z]
        row = {GRID: None}
        for g, sub in by_mandate(ts, lambda x: x["mandate"]).items():
            n = len(sub)
            if not n:
                row[g] = {"n": 0}
                continue
            per_unit = [x["realized_r"] / x["size_r"] for x in sub]
            lo, hi = boot_ci(per_unit)
            row[g] = {
                "n": n,
                "sum_cell_r_0x": r4(sum(x["r_0x"] for x in sub)),
                "sum_cell_r_1x": r4(sum(x["realized_r"] for x in sub)),
                "sum_cell_r_2x": r4(sum(x["r_2x"] for x in sub)),
                "net_per_unit_mean": r4(float(np.mean(per_unit))),
                "net_per_unit_ci95": [lo, hi],
                "win_rate_1x": pct(sum(1 for x in sub if x["realized_r"] > 0), n),
            }
        out["tranche_level"][z] = row
    # zone of the other rows (should be none, but enumerate honestly)
    other = Counter(x["zone"] for x in book.t
                    if x["zone"] not in ("Z1", "Z2", "Z3"))
    out["tranche_level_other_zones"] = dict(other)

    # campaign-level by initiating tranche's zone
    init_zone = {}
    for c in book.camps:
        init = min(book.camp_tr[c], key=lambda x: x["seq"])
        init_zone[c] = init["zone"]
    for z in ("Z1", "Z2", "Z3"):
        cs = [c for c in book.camps if init_zone[c] == z]
        row = {GRID: camp_agg(book, cs) if cs else {"campaigns": 0}}
        for m in MANDATES:
            cm = [c for c in cs if mandate_of(c[0]) == m]
            row[m] = camp_agg(book, cm) if cm else {"campaigns": 0}
        out["campaign_level"][z] = row
    out["campaign_level_other_zones"] = dict(Counter(
        init_zone[c] for c in book.camps
        if init_zone[c] not in ("Z1", "Z2", "Z3")))
    return out


# ---------------------------------------------------------------- R9

def c1_ratio(x):
    if x["entry_atr"] in (None, 0):
        return None
    return abs(x["entry_px"] - x["entry_stop"]) / x["entry_atr"]


def retr_weight(x):
    r = x["retr"]
    if r is None:
        return 1.0
    if r >= 0.5:
        return 1.5
    if r < 0.25:
        return 0.5
    return 1.0


def R9(book):
    out = {"caveat": "FIRST-ORDER ONLY. Removing or re-weighting a tranche "
                     "does not change the stop path (the ratchet is "
                     "signal-layer and independent of fills), but it DOES "
                     "change the equity path, the 1R campaign rail, and the "
                     "halt calendar -- all of which gate admission. Faithful "
                     "measurement is S-1's job.",
           "aggressive_out_of_scope":
               "Aggressive mode is OUT OF SCOPE here: it creates tranches that "
               "do not exist in these journals. It requires a Tier-C run. "
               "R9 covers defensive and neutral only.",
           "filters": {
               "neutral": "the live line as journaled (control)",
               "def_c1_only": "drop tranches with "
                              "abs(px_fill - stop) / atr_exec (both from the "
                              "ENTRY row) < 0.5",
               "def_c1_grade": "def_c1_only + drop grade not in {A, A+}",
               "def_full": "def_c1_grade + size_r x1.5 if retr>=0.5, "
                           "x0.5 if retr<0.25, x1.0 otherwise",
           },
           "columns": {}}
    n_missing_atr = sum(1 for x in book.t if c1_ratio(x) is None)
    n_missing_retr = sum(1 for x in book.t if x["retr"] is None)
    out["notes"] = {
        "tranches_with_null_atr_exec_on_entry": n_missing_atr,
        "null_atr_handling": "kept (cannot evaluate C1); count reported",
        "tranches_with_null_retr": n_missing_retr,
        "null_retr_handling": "weight x1.0",
        "reweight_semantics":
            "realized_r is linear in size_r (pnl scales with qty, qty scales "
            "with size_r at fixed unit risk), so a size tilt scales the "
            "tranche's cell-R, its cost, and hence r_0x/r_2x by the same "
            "weight.",
    }

    def wf_neutral(x):
        return 1.0

    def wf_c1(x):
        r = c1_ratio(x)
        return 0.0 if (r is not None and r < 0.5) else 1.0

    def wf_c1g(x):
        if wf_c1(x) == 0.0:
            return 0.0
        return 1.0 if x["grade"] in ("A", "A+") else 0.0

    def wf_full(x):
        if wf_c1g(x) == 0.0:
            return 0.0
        return retr_weight(x)

    for name, wf in (("neutral", wf_neutral), ("def_c1_only", wf_c1),
                     ("def_c1_grade", wf_c1g), ("def_full", wf_full)):
        col = {}
        for g in [GRID] + MANDATES:
            cs = book.camps if g == GRID else [c for c in book.camps
                                               if mandate_of(c[0]) == g]
            kept = [c for c in cs if any(wf(x) != 0.0 for x in book.camp_tr[c])]
            a = camp_agg(book, kept, weightfn=wf)
            a["tranches_kept"] = sum(1 for c in cs for x in book.camp_tr[c]
                                     if wf(x) != 0.0)
            a["tranches_total"] = sum(len(book.camp_tr[c]) for c in cs)
            col[g] = a
        out["columns"][name] = col
    return out


# ---------------------------------------------------------------- R10

def R10(book):
    out = {"caveat": "This is the OPTIMISTIC bound. It assumes every entry "
                     "fills as a maker and none is missed. Chase orders miss "
                     "most when price runs away immediately -- which is "
                     "disproportionately the character of the entries that "
                     "become tail campaigns. The bound is a CEILING, not an "
                     "estimate.",
           "formula": "cost_maker = cost_total - entry_fee*(3/5) - "
                      "entry_slippage ; r_maker = realized_r + "
                      "(cost_total - cost_maker)/one_r",
           "assumption": "maker entries 2 bps/side, taker stops 5 bps/side "
                         "(entry fee scaled 5->2 bps by removing 3/5 of it); "
                         "fills otherwise unchanged",
           "ceiling_on_all_execution_improvement_sum_0x": r4(
               sum(x["r_0x"] for x in book.t)),
           "per_mandate": {}}
    for g, ts in by_mandate(book.t, lambda x: x["mandate"]).items():
        s1 = sum(x["realized_r"] for x in ts)
        sm = 0.0
        f_b = sl_b = fu_b = 0.0
        f_a = sl_a = fu_a = 0.0
        for x in ts:
            saved = x["entry_fee"] * (3.0 / 5.0) + x["entry_slip"]
            sm += x["realized_r"] + saved / x["one_r"]
            f_b += x["fees"]; sl_b += x["slippage"]; fu_b += x["funding"]
            f_a += x["fees"] - x["entry_fee"] * (3.0 / 5.0)
            sl_a += x["slippage"] - x["entry_slip"]
            fu_a += x["funding"]
        out["per_mandate"][g] = {
            "n": len(ts),
            "sum_1x_actual": r4(s1),
            "sum_maker_entry": r4(sm),
            "delta_vs_1x": r4(sm - s1),
            "cost_split_before_usd": {"fees": r4(f_b), "slippage": r4(sl_b),
                                      "funding": r4(fu_b),
                                      "total": r4(f_b + sl_b + fu_b)},
            "cost_split_after_usd": {"fees": r4(f_a), "slippage": r4(sl_a),
                                     "funding": r4(fu_a),
                                     "total": r4(f_a + sl_a + fu_a)},
        }
    return out


# ---------------------------------------------------------------- predictions

def predictions(book, r1, r2, r6, r7, r9):
    P = []

    # P-R1: X-A family beats the actual book (gross) on swing AND position;
    # ambiguous-to-negative on intraday.
    xa = r1["variants"]["X-A"]
    sw = xa["swing"]["delta_vs_actual_0x"]
    po = xa["position"]["delta_vs_actual_0x"]
    it = xa["intraday"]["delta_vs_actual_0x"]
    # "wins clearly on intraday" is the falsifier; treat >0 as a win.
    fals = (sw <= 0) or (po <= 0) or (it > 0)
    P.append({
        "id": "P-R1", "prior": "70%",
        "claim": "X-A-family exits beat the actual book (gross basis) on swing "
                 "AND position; ambiguous-to-negative on intraday",
        "falsified_if": "X-A loses on swing or position, or wins clearly on intraday",
        "evidence": {"xa_delta_swing_0x": sw, "xa_delta_position_0x": po,
                     "xa_delta_intraday_0x": it},
        "verdict": "FALSIFIED" if fals else "CONFIRMED",
    })

    # P-R2
    share = r2["v_share_of_wins_pct"]
    P.append({
        "id": "P-R2", "prior": "50%",
        "claim": "The 45 V campaigns are NOT disproportionately tail-carrying "
                 "-- their share of sum(wins) < 3x their share of campaigns "
                 "(< 3.9%)",
        "falsified_if": "V's share of sum(wins) >= 3.9%",
        "evidence": {"v_share_of_wins_pct": share,
                     "v_share_of_campaigns_pct": r2["share_of_campaigns_pct"],
                     "threshold_pct": 3.9},
        "verdict": "FALSIFIED" if share >= 3.9 else "CONFIRMED",
    })

    # P-R6
    p = r6["p_r6"]["z2_stage1_pct"]
    P.append({
        "id": "P-R6", "prior": "85%",
        "claim": ">=95% of Z2-active entries carry stage = 1",
        "falsified_if": "< 95%",
        "evidence": r6["p_r6"],
        "verdict": "FALSIFIED" if (p is None or p < 95.0) else "CONFIRMED",
    })

    # P-R7
    tc = r7["load_bearing"]["tranche_cap_max_tranches"]
    P.append({
        "id": "P-R7", "prior": "60%",
        "claim": "tranche_cap rejects > 500 (aggressive mode is a real axis, "
                 "not a non-event)",
        "falsified_if": "<= 500",
        "evidence": {"tranche_cap_rejects": tc, "threshold": 500,
                     "engine_reason_name": TRANCHE_CAP_REASON},
        "verdict": "FALSIFIED" if tc <= 500 else "CONFIRMED",
    })

    # P-R9
    df = r9["columns"]["def_full"][GRID]["sum_1x"]
    P.append({
        "id": "P-R9", "prior": "60%",
        "claim": "def_full remains NET NEGATIVE at 1x -- no defensive bundle "
                 "flips the grid sign in-sample on mined data",
        "falsified_if": "def_full 1x >= 0",
        "evidence": {"def_full_sum_1x": df},
        "verdict": "FALSIFIED" if df >= 0 else "CONFIRMED",
    })
    return P


# ---------------------------------------------------------------- markdown

def md_table(headers, rows):
    out = ["| " + " | ".join(headers) + " |",
           "|" + "|".join("---" for _ in headers) + "|"]
    for r in rows:
        out.append("| " + " | ".join("" if v is None else str(v) for v in r) + " |")
    return "\n".join(out)


def render_md(res):
    L = []
    A = L.append
    m = res["meta"]
    A("# V3 Recompute R1-R10 — Tier A (journal arithmetic only)")
    A("")
    A(f"**Basis:** engine {m['engine_version']} (`{m['engine_commit']}`), "
      f"config `{m['config_id']}` (`{m['config_sha256'][:8]}...`), "
      f"scored partition (exploration-classic), {m['n_cells']} cells.")
    A(f"**Journal root:** `{m['journal_root']}`")
    A(f"**Evidence spend:** NONE (VR-1 exploration-classic; first look already "
      f"consumed).  **Engine delta:** NONE (read-only).")
    A(f"**Bootstrap:** 95% CI, {m['n_boot']:,} resamples, campaign-level, "
      f"seed `{m['seed']}` (pinned).")
    A("")
    A("> **Scope.** Not tuning, not evidence about the future, not a variant "
      "nomination, not a lockbox touch, not S-1. Every number is in-sample on "
      "data already mined: it ranks candidates, it validates nothing.")
    A("")

    # config
    A("## Config paste — actual run values (contract §5)")
    A("")
    A("The reviewer has been working from Pine defaults. These are the real "
      "`v12_anchor.yaml` values.")
    A("")
    c = res["config"]
    A("### signal")
    A(md_table(["key", "value"], [[k, v] for k, v in c["signal"].items()]))
    A("")
    A("### trading (entire block)")
    A(md_table(["key", "value"], [[k, v] for k, v in c["trading"].items()]))
    A("")
    A("### cell.zone_memory / cell.tf_align — one cell per mandate")
    A("")
    A("Neither field lives in `v12_anchor.yaml`; both come from "
      "`engine/cells.py`. `zone_memory` is a constant property (=3, engine "
      "1.0.3 Pine input-parity), identical for every cell.")
    A("")
    A(md_table(["cell", "mandate", "zone_memory", "tf_align", "tf_gov", "tf_exec"],
               [[x["cell"], x["mandate"], x["zone_memory"], x["tf_align"],
                 x["tf_gov"], x["tf_exec"]] for x in c["cells"]]))
    A("")

    # fixtures
    A("## Fixtures F1-F9 — known-answer gates (contract §5)")
    A("")
    A("Computed from raw journal bytes. `ROLLUPS_AND_HYPOTHESES.md` and "
      "`V3_STOP_AND_EXIT_FORENSICS.md` were **not** read as inputs.")
    A("")
    A(md_table(["fixture", "expected", "computed", "result"],
               [[f["fixture"], json.dumps(f["expected"]) if isinstance(
                   f["expected"], dict) else f["expected"],
                 json.dumps(f["computed"]) if isinstance(f["computed"], dict)
                 else f["computed"],
                 "**MATCH**" if f["match"] else "**MISMATCH**"]
                for f in res["fixtures"]]))
    A("")
    A(f"**Verdict: {res['fixture_verdict']}** — "
      f"{sum(1 for f in res['fixtures'] if f['match'])}/"
      f"{len(res['fixtures'])} match.")
    A("")
    A("### F9 next to the config value (contract §5)")
    A("")
    A(md_table(["quantity", "value"], [
        ["signal-layer `r_cap` REJECT count", res["f9_detail"]["r_cap_rejects"]],
        ["`signal.max_r_count` in v12_anchor.yaml",
         res["f9_detail"]["config_max_r_count"]],
        ["`rcap_ok` (signals.py:368)", "`max_rc == 0 or r_count < max_rc`"],
    ]))
    A("")
    A(res["f9_detail"]["reading"])
    A("")

    dc = res["data_characteristics"]
    if dc.get("negative_one_r_tranches"):
        A("## Data characteristic surfaced by the recompute — read before R9")
        A("")
        A(f"**{dc['negative_one_r_tranches']} tranches carry a NEGATIVE "
          f"`one_r`**, all in "
          f"`{', '.join(sorted(dc['negative_one_r_by_cell']))}`.")
        A("")
        A(f"> {dc['finding']}")
        A("")
        A(md_table(["cell", "tranches total", "tranches w/ negative one_r",
                    "Σ cell-R 1×"],
                   [[c, v["tranches_total"], v["tranches_with_negative_one_r"],
                     v["sum_cell_r_1x"]] for c, v in dc["detail"].items()]))
        A("")

    # deliverables
    for key in ["R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9", "R10"]:
        A(res["md"][key])
        A("")

    # predictions
    A("## Prediction scorecard (contract §7)")
    A("")
    A(md_table(["#", "prediction", "prior", "falsified if", "verdict"],
               [[p["id"], p["claim"], p["prior"], p["falsified_if"],
                 f"**{p['verdict']}**"] for p in res["predictions"]]))
    A("")
    for p in res["predictions"]:
        A(f"- **{p['id']} — {p['verdict']}.** Evidence: "
          f"`{json.dumps(p['evidence'])}`")
    A("")
    A("**Not scored here** (S-1 items, carried from Report 2 unchanged): "
      "P-S1a (de-ratchet / loosening-while-open events = 0), P-S1b "
      "(non-advancement explains >= 1/3 of +1R-to-loss round-trips).")
    A("")
    return "\n".join(L)


# ---------------------------------------------------------------- md sections

def md_R1(r):
    L = [f"## R1 — Exit-variant ranking", "",
         f"> **Caveat.** {r['caveat']}", ""]
    rows = []
    for var, vo in r["variants"].items():
        for g in [GRID] + MANDATES:
            d = vo[g]
            rows.append([var, g, d["n"], d["sum_0x"], d["actual_sum_0x"],
                         d["delta_vs_actual_0x"], d["win_rate_0x"],
                         d["sum_1x_proxy"], d["sum_2x_proxy"]])
    L.append(md_table(["variant", "scope", "n", "Σ cell-R (0×)",
                       "actual Σ r_0x", "Δ vs actual (0×)", "win rate % (0×)",
                       "Σ 1× (proxy)", "Σ 2× (proxy)"], rows))
    L.append("")
    L.append("Actual book, gross basis, for reference:")
    L.append("")
    L.append(md_table(["scope", "n", "Σ r_0x", "win rate % (0×)"],
                      [[g, r["actual_book"][g]["n"], r["actual_book"][g]["sum_0x"],
                        r["actual_book"][g]["win_rate_0x"]]
                       for g in [GRID] + MANDATES]))
    return "\n".join(L)


def md_R2(r):
    L = ["## R2 — V-cohort P&L", "",
         f"**Discriminator.** {r['discriminator']}", ""]
    rows = []
    for g in [GRID] + MANDATES:
        d = r["grid"] if g == GRID else r["per_mandate"][g]
        if not d.get("campaigns"):
            rows.append([g, 0, None, None, None, None, None, None, None])
            continue
        rows.append([g, d["campaigns"], d["sum_0x"], d["sum_1x"], d["sum_2x"],
                     d["expectancy_1x"], f"[{d['ci95_lo']}, {d['ci95_hi']}]",
                     d["win_rate"], d["strip_best_sum_1x"]])
    L.append(md_table(["scope", "campaigns", "Σ 0×", "Σ 1×", "Σ 2×",
                       "expectancy 1×", "95% CI", "win rate %",
                       "strip-best Σ 1×"], rows))
    L.append("")
    L.append(md_table(["quantity", "value"], [
        ["V campaigns", r["v_campaigns"]],
        ["share of campaigns %", r["share_of_campaigns_pct"]],
        ["Σ wins (grid)", r["sum_wins_grid"]],
        ["V Σ wins", r["v_sum_wins"]],
        ["**V share of Σwins %**", f"**{r['v_share_of_wins_pct']}**"],
        ["Σ losses (grid)", r["sum_losses_grid"]],
        ["V Σ losses", r["v_sum_losses"]],
        ["V share of Σlosses %", r["v_share_of_losses_pct"]],
    ]))
    L.append("")
    L.append("Top-5 V campaigns by cell-R:")
    L.append("")
    L.append(md_table(["campaign", "cell-R 1×", "tranches"],
                      [[t["campaign"], t["cell_r_1x"], t["tranches"]]
                       for t in r["top5_by_cell_r"]]))
    return "\n".join(L)


def md_R3(r):
    L = ["## R3 — MFE-before-death distributions", "",
         f"> **Purpose.** {r['purpose']}", "",
         f"**Population:** {r['population']} — n = {r['n_population']:,}.  "
         f"**Deciles of:** {r['deciles_of']}.", "",
         "**Stop class** (field lens): EXIT row `stop` (= the fill level) vs "
         "ENTRY row `stop` (= stop_at_entry) for the same `tranche_id`. "
         "`no_stop_row` = non-stop exits (failure_x / opposite_cross / "
         "campaign_died), which journal `stop = null` (replay.py:191) and "
         "therefore have no stop class.", "",
         f"> **Structural note.** {r['structural_note']}", ""]
    L.append("### Marginal by stop class")
    L.append("")
    rows = []
    for sc, d in r["by_stop_class"].items():
        rows.append([sc, d["n"], d["sum_cell_r_1x"]] + d["mfe_deciles"])
    L.append(md_table(["stop class", "n", "Σ cell-R 1×", "D1", "D2", "D3", "D4",
                       "D5", "D6", "D7", "D8", "D9"], rows))
    L.append("")
    L.append("### Full grid — stop class × mandate × grade")
    L.append("")
    rows = []
    for k, d in r["grid"].items():
        sc, m, g = k.split("|")
        rows.append([sc, m, g, d["n"], d["sum_cell_r_1x"], d["sum_cell_r_0x"],
                     d["mfe_median"]] + d["mfe_deciles"])
    L.append(md_table(["stop class", "mandate", "grade", "n", "Σ cell-R 1×",
                       "Σ cell-R 0×", "MFE med", "D1", "D2", "D3", "D4", "D5",
                       "D6", "D7", "D8", "D9"], rows))
    return "\n".join(L)


def md_R4(r):
    L = ["## R4 — Harvest-doctrine timing test", "",
         f"**Population:** {r['population']} — n = **{r['n_population']:,}**.", "",
         f"**Route taken.** {r['route']}", "",
         f"> **⚠ READ THIS BEFORE THE TABLE.** {r['flag_semantics_warning']}",
         ""]
    rows = []
    for g in [GRID] + MANDATES:
        d = r["counts"][g]
        rows.append([g, d["n"], d["tpw_before_exit_STRICT"],
                     d["tpw_before_exit_STRICT_pct"],
                     d["ext_before_CAMPAIGN_DEATH_loose"],
                     d["ext_before_CAMPAIGN_DEATH_loose_pct"]])
    L.append(md_table(["scope", "n", "TPW before **exit** (strict)", "TPW %",
                       "ext ≥2·ATR before **campaign death** (loose)", "ext %"],
                      rows))
    L.append("")
    L.append("The two count columns are **not comparable** — the first is "
             "windowed on the tranche's own life, the second on the campaign's. "
             "An `either` column would mix windows and is deliberately omitted.")
    L.append("")
    L.append("**Independent cross-check on the TPW result** (computed from "
             "raw row timestamps, not the flag): of the 2,999 `TPW` event rows "
             "in the scored partition, only **16** fall inside an open "
             "same-direction tranche window at all. The flag and the timestamp "
             "scan agree — **TPW essentially never fires while the book is "
             "positioned**, so a TPW-armed harvest rule would almost never "
             "trigger on this run.")
    L.append("")
    L.append("### Extension, strict 'before their exit' reading — **PARTIAL**")
    L.append("")
    L.append(f"> {r['ext_partial_reason']}")
    L.append("")
    L.append("### Median MFE at the first trigger — **PARTIAL**")
    L.append("")
    L.append(f"> {r['partial_reason']}")
    L.append("")
    L.append("**What IS recoverable** (reported instead, clearly labelled — "
             "not a substitute estimate for the above):")
    L.append("")
    L.append(f"{r['recoverable_R_at_first_trigger']['definition']}")
    L.append("")
    rows = []
    for g in [GRID] + MANDATES:
        d = r["recoverable_R_at_first_trigger"]["per_mandate"][g]
        rows.append([g, d["n_tpw_recoverable"], d["median_R_at_first_tpw"],
                     d["n_ext_recoverable"], d["median_R_at_first_ext"]])
    L.append(md_table(["scope", "n (TPW recoverable)", "median R at 1st TPW",
                       "n (ext recoverable)", "median R at 1st ext"], rows))
    return "\n".join(L)


def md_R5(r):
    L = ["## R5 — Shaken-out, per exit event", "",
         f"> **Purpose.** {r['purpose']}", "",
         f"**Resumption definition.** {r['resumption_definition']}", "",
         f"**Event key.** {r['event_key']}. {r['event_representative']}", ""]
    pt, pe = r["per_tranche"], r["per_event"]
    L.append(md_table(["basis", "n", "resumed ≥1R within 20b", "resumed %",
                       "forfeited-continuation pool (cell-R, 10R/unit cap)",
                       "median postexit_cont_20"],
                      [["per-tranche", pt["n"], pt["resumed_ge_1R_20b"],
                        pt["resumed_pct"], pt["forfeited_pool_cell_r"],
                        pt["median_cont_20"]],
                       ["per-event", pe["n"], pe["resumed_ge_1R_20b"],
                        pe["resumed_pct"], pe["forfeited_pool_cell_r"],
                        pe["median_cont_20"]]]))
    L.append("")
    L.append(f"Mean tranches per exit event: **{pe['tranches_per_event_mean']}**.")
    L.append("")
    rows = []
    for m in MANDATES:
        d = r["per_mandate"][m]
        rows.append([m, d["tranches"], d["tranches_resumed"], d["events"],
                     d["events_resumed"], d["events_resumed_pct"],
                     d["forfeited_pool_cell_r_per_event"]])
    L.append(md_table(["mandate", "tranches", "tranches resumed", "events",
                       "events resumed", "events resumed %",
                       "forfeited pool (per-event, cell-R)"], rows))
    return "\n".join(L)


def md_R6(r):
    L = ["## R6 — Zone × stage cross-tab", "",
         f"> **Purpose.** {r['purpose']}", "",
         f"**Note.** {r['note']} Fills = {r['n_fills']:,}; without a joined "
         f"EXIT = {r['n_fills_without_exit']}.", ""]
    for d in ("both", "long", "short"):
        L.append(f"### direction = {d}")
        L.append("")
        rows = []
        for k, v in r["table"][d].items():
            rows.append([k, v["n"], v["n_with_exit"], v["sum_cell_r_1x"],
                         v["sum_cell_r_0x"], v["expectancy_1x"]])
        L.append(md_table(["zone|stage", "n", "n w/ exit", "Σ cell-R 1×",
                           "Σ cell-R 0×", "expectancy 1×"], rows))
        L.append("")
    L.append("### per mandate")
    L.append("")
    rows = []
    for m in MANDATES:
        for k, v in r["per_mandate"][m].items():
            rows.append([m, k, v["n"], v["sum_cell_r_1x"], v["expectancy_1x"]])
    L.append(md_table(["mandate", "zone|stage", "n", "Σ cell-R 1×",
                       "expectancy 1×"], rows))
    L.append("")
    p = r["p_r6"]
    L.append(f"**Stage-2 rows with zone = Z2: {p['z2_stage2']:,}.** "
             f"Z2 entries = {p['z2_entries']:,}; Z2 & stage-1 = "
             f"{p['z2_stage1']:,} (**{p['z2_stage1_pct']}%**).")
    L.append("")
    L.append("### Zone × stage occupancy — the cross-tab is nearly degenerate")
    L.append("")
    L.append(md_table(["zone", "n", "stage 1", "stage 2"],
                      [[z, v["n"], v["stage1"], v["stage2"]]
                       for z, v in r["zone_stage_occupancy"].items()]))
    L.append("")
    L.append(f"> **Finding.** {r['degeneracy_finding']}")
    return "\n".join(L)


def md_R7(r):
    L = ["## R7 — Reject funnel, split by layer", "",
         f"**Layer discriminator.** {r['layer_discriminator']}", "",
         f"> **Naming.** {r['naming_note']}", "",
         md_table(["layer", "rows"],
                  [["signal", f"{r['totals']['signal_layer']:,}"],
                   ["trading", f"{r['totals']['trading_layer']:,}"],
                   ["all REJECT rows", f"{r['totals']['all']:,}"]]), ""]
    for layer in ("signal_layer", "trading_layer"):
        L.append(f"### {layer.replace('_', ' ')}")
        L.append("")
        reasons = sorted(r[layer][GRID], key=lambda k: -r[layer][GRID][k])
        rows = []
        for reason in reasons:
            rows.append([f"`{reason}`", r[layer][GRID].get(reason, 0)]
                        + [r[layer][m].get(reason, 0) for m in MANDATES])
        L.append(md_table(["reject_reason", "GRID"] + MANDATES, rows))
        L.append("")
    lb = r["load_bearing"]
    L.append("### Load-bearing counts")
    L.append("")
    L.append(md_table(["quantity", "count", "why it matters"], [
        ["`r_cap` (F9)", lb["r_cap_F9"],
         "0 ⇒ the signal layer is NOT capping PRIMEs"],
        ["`tranche_cap` / `max_tranches`", f"**{lb['tranche_cap_max_tranches']:,}**",
         "exactly how many adds the 3-tranche ceiling turned away — sizes the "
         "aggressive-mode decision BEFORE any run is spent"],
        ["`add_ineligible`", lb["add_ineligible"], "breakeven doctrine"],
        ["`no_zone`", f"{lb['no_zone']:,}", "sizes VS-Z3"],
        ["`ribbon_sep`", f"{lb['ribbon_sep']:,}", "sizes VS-Z3"],
    ]))
    return "\n".join(L)


def md_R8(r):
    L = ["## R8 — Expectancy by zone, including Z3", "",
         f"> **Gap closed.** {r['note']}", "",
         "### Tranche level", ""]
    rows = []
    for z in ("Z1", "Z2", "Z3"):
        for g in [GRID] + MANDATES:
            d = r["tranche_level"][z][g]
            if not d.get("n"):
                rows.append([z, g, 0, None, None, None, None, None, None])
                continue
            rows.append([z, g, d["n"], d["sum_cell_r_0x"], d["sum_cell_r_1x"],
                         d["sum_cell_r_2x"], d["net_per_unit_mean"],
                         f"[{d['net_per_unit_ci95'][0]}, {d['net_per_unit_ci95'][1]}]",
                         d["win_rate_1x"]])
    L.append(md_table(["zone", "scope", "n", "Σ cell-R 0×", "Σ cell-R 1×",
                       "Σ cell-R 2×", "net R/unit", "95% CI", "win rate %"],
                      rows))
    L.append("")
    if r["tranche_level_other_zones"]:
        L.append(f"Other zone values on EXIT rows: "
                 f"`{json.dumps(r['tranche_level_other_zones'])}`")
        L.append("")
    L.append("### Campaign level, by the initiating tranche's zone")
    L.append("")
    rows = []
    for z in ("Z1", "Z2", "Z3"):
        for g in [GRID] + MANDATES:
            d = r["campaign_level"][z][g]
            if not d.get("campaigns"):
                rows.append([z, g, 0, None, None, None, None, None])
                continue
            rows.append([z, g, d["campaigns"], d["sum_1x"], d["expectancy_1x"],
                         f"[{d['ci95_lo']}, {d['ci95_hi']}]", d["win_rate"],
                         d["strip_best_sum_1x"]])
    L.append(md_table(["zone", "scope", "campaigns", "Σ 1×", "expectancy 1×",
                       "95% CI", "win rate %", "strip-best Σ 1×"], rows))
    if r["campaign_level_other_zones"]:
        L.append("")
        L.append(f"Campaigns whose initiating zone is not Z1/Z2/Z3: "
                 f"`{json.dumps(r['campaign_level_other_zones'])}`")
    return "\n".join(L)


def md_R9(r):
    L = ["## R9 — Risk-mode first-order table (defensive + neutral only)", "",
         f"> **Caveat.** {r['caveat']}", "",
         f"> **Aggressive.** {r['aggressive_out_of_scope']}", "",
         md_table(["column", "filter"],
                  [[f"`{k}`", v] for k, v in r["filters"].items()]), ""]
    rows = []
    for name, col in r["columns"].items():
        for g in [GRID] + MANDATES:
            d = col[g]
            rows.append([f"`{name}`", g, d["campaigns"], d["tranches_kept"],
                         d["sum_0x"], d["sum_1x"], d["sum_2x"],
                         d["expectancy_1x"],
                         f"[{d['ci95_lo']}, {d['ci95_hi']}]", d["win_rate"],
                         d["strip_best_sum_1x"]])
    L.append(md_table(["column", "scope", "campaigns", "tranches kept",
                       "Σ 0×", "Σ 1×", "Σ 2×", "expectancy 1×", "95% CI",
                       "win rate %", "strip-best Σ 1×"], rows))
    L.append("")
    L.append(md_table(["note", "value"],
                      [[k, v] for k, v in r["notes"].items()]))
    return "\n".join(L)


def md_R10(r):
    L = ["## R10 — Fee Stage A (maker-entry bound)", "",
         f"> **Caveat.** {r['caveat']}", "",
         f"**Formula.** `{r['formula']}`  \n**Assumption.** {r['assumption']}",
         "",
         f"**Ceiling on ALL execution improvement — the 0× line: "
         f"{r['ceiling_on_all_execution_improvement_sum_0x']}.** No execution "
         f"change can beat it; it is the book with every cost removed.", ""]
    rows = []
    for g in [GRID] + MANDATES:
        d = r["per_mandate"][g]
        rows.append([g, d["n"], d["sum_1x_actual"], d["sum_maker_entry"],
                     d["delta_vs_1x"]])
    L.append(md_table(["scope", "n", "Σ 1× actual", "Σ maker-entry basis",
                       "Δ vs 1×"], rows))
    L.append("")
    L.append("Cost split, USD (before → after):")
    L.append("")
    rows = []
    for g in [GRID] + MANDATES:
        b = r["per_mandate"][g]["cost_split_before_usd"]
        a = r["per_mandate"][g]["cost_split_after_usd"]
        rows.append([g, b["fees"], a["fees"], b["slippage"], a["slippage"],
                     b["funding"], a["funding"], b["total"], a["total"]])
    L.append(md_table(["scope", "fees before", "fees after", "slip before",
                       "slip after", "funding before", "funding after",
                       "total before", "total after"], rows))
    return "\n".join(L)


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser()
    here = Path(__file__).resolve().parents[1]
    ap.add_argument("--journal-root", type=Path,
                    default=here / "research_outputs" / "v3_anchor"
                    / "journal_pass1" / "scored")
    ap.add_argument("--config", type=Path,
                    default=here / "configs" / "v12_anchor.yaml")
    ap.add_argument("--out-dir", type=Path, default=here)
    args = ap.parse_args()

    sys.path.insert(0, str(here))
    from engine.cells import make_cell

    import yaml
    cfg = yaml.safe_load(args.config.read_text(encoding="utf-8"))
    cfg_sha = hashlib.sha256(args.config.read_bytes()).hexdigest()

    cells, rows, evt_census = load_scored(args.journal_root)
    book = Book(rows)

    fx, rcap = fixtures(book, evt_census, cfg["signal"]["max_r_count"])
    verdict = "PASS" if all(f["match"] for f in fx) else "HALT"

    res = {
        "meta": {
            "contract": "V3_Recompute_R1_R10_Builder_Contract.md",
            "phase": "V3 Recompute R1-R10 — Tier A, journals-only",
            "engine_version": sorted({r["engine_version"] for r in rows})[0],
            "engine_commit": "2f260e1",
            "config_id": cfg["config_id"],
            "config_sha256": cfg_sha,
            # repo-relative so the reviewer's recompute hashes identically
            "journal_root": str(
                args.journal_root.resolve().relative_to(here)
                if str(args.journal_root.resolve()).startswith(str(here))
                else args.journal_root).replace("\\", "/"),
            "partition": "scored (exploration-classic, open time <= "
                         "2024-06-30 23:59:59Z)",
            "n_cells": len(cells),
            "cells": cells,
            "seed": SEED,
            "n_boot": N_BOOT,
            "read_only": True,
            "inputs_excluded": ["ROLLUPS_AND_HYPOTHESES.md",
                                "V3_STOP_AND_EXIT_FORENSICS.md"],
            "evt_census_scored": dict(sorted(evt_census.items())),
        },
        "config": {
            "signal": {k: cfg["signal"][k] for k in
                       ("z1_prox", "z2_prox", "z3_prox", "max_r_count",
                        "cooldown_bars")},
            "trading": dict(cfg["trading"]),
            "cells": [],
        },
        "fixtures": fx,
        "fixture_verdict": verdict,
    }
    for mnd in MANDATES:
        cid = next(c for c in cells if mandate_of(c) == mnd)
        cc = make_cell(cid.rpartition("_")[0], mnd)
        res["config"]["cells"].append({
            "cell": cid, "mandate": mnd, "zone_memory": cc.zone_memory,
            "tf_align": cc.tf_align, "tf_gov": cc.tf_gov, "tf_exec": cc.tf_exec})

    res["f9_detail"] = {
        "r_cap_rejects": rcap,
        "config_max_r_count": cfg["signal"]["max_r_count"],
        "reading": (
            "**F9 MATCHES and the reviewer's reading is UPHELD.** "
            "`signal.max_r_count = 0` in the anchor config (= unlimited), and "
            "`signals.py:368` reads `rcap_ok = max_rc == 0 or r_count < "
            "max_rc`, so with max_rc = 0 the `r_cap` branch is unreachable by "
            "construction — consistent with the 0 observed. The signal layer "
            "is NOT capping PRIMEs, so unlimited adds remain a "
            "**trading-config-only** change (`trading.max_tranches`), not a "
            "Pine-parity-bound one."
            if rcap == 0 else
            "**F9 MISMATCH — LOUD.** r_cap rejects exist, so the anchor config "
            "set max_r_count != 0 and the signal layer IS capping PRIMEs. The "
            "reviewer's conclusion that 'unlimited adds is a "
            "trading-config-only change' is FALSE, and aggressive mode is "
            "Pine-parity-bound, not cheap."),
    }

    if verdict == "HALT":
        # Contract §8: stop immediately, produce nothing downstream.
        res["halt"] = ("Fixture MISMATCH — the journal reader is wrong and "
                       "every downstream table would be garbage. No "
                       "deliverables produced.")
        out_json = args.out_dir / "recompute.json"
        blob = json.dumps(res, indent=1, sort_keys=True,
                          ensure_ascii=False).encode("utf-8")
        out_json.write_bytes(blob)
        print("HALT — fixture mismatch:")
        for f in fx:
            if not f["match"]:
                print(f"  {f['fixture']}: expected {f['expected']} "
                      f"computed {f['computed']}")
        print(f"sha256(recompute.json) = {hashlib.sha256(blob).hexdigest()}")
        return 1

    res["data_characteristics"] = data_characteristics(book)
    r1, r2 = R1(book), R2(book)
    r3, r4 = R3(book), R4(book)
    r5, r6 = R5(book), R6(book)
    r7, r8 = R7(book), R8(book)
    r9, r10 = R9(book), R10(book)
    res["deliverables"] = {"R1": r1, "R2": r2, "R3": r3, "R4": r4, "R5": r5,
                           "R6": r6, "R7": r7, "R8": r8, "R9": r9, "R10": r10}
    res["predictions"] = predictions(book, r1, r2, r6, r7, r9)
    res["md"] = {"R1": md_R1(r1), "R2": md_R2(r2), "R3": md_R3(r3),
                 "R4": md_R4(r4), "R5": md_R5(r5), "R6": md_R6(r6),
                 "R7": md_R7(r7), "R8": md_R8(r8), "R9": md_R9(r9),
                 "R10": md_R10(r10)}

    md = render_md(res)
    out_md = args.out_dir / "V3_RECOMPUTE_R1_R10.md"
    out_json = args.out_dir / "recompute.json"

    payload = {k: v for k, v in res.items() if k != "md"}
    blob = json.dumps(payload, indent=1, sort_keys=True,
                      ensure_ascii=False).encode("utf-8")
    out_json.write_bytes(blob)
    with open(out_md, "w", encoding="utf-8", newline="\n") as f:
        f.write(md)

    j_sha = hashlib.sha256(blob).hexdigest()
    m_sha = hashlib.sha256(out_md.read_bytes()).hexdigest()
    combo = hashlib.sha256((j_sha + m_sha).encode()).hexdigest()
    print(f"fixtures: {verdict} ({sum(1 for f in fx if f['match'])}/{len(fx)})")
    for p in res["predictions"]:
        print(f"  {p['id']}: {p['verdict']}")
    print(f"sha256(recompute.json)         = {j_sha}")
    print(f"sha256(V3_RECOMPUTE_R1_R10.md) = {m_sha}")
    print(f"OUTPUT_HASH                    = {combo}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
