#!/usr/bin/env python3
"""RC Recompute RC-0..RC-6 — Tier A, journal arithmetic + read-only kline inventory.

Contract: RC_Recompute_RC0_RC6_Builder_Contract.md
Basis:    engine 1.0.7 (2f260e1), config v12_anchor (a3917ea5...),
          scored partition (exploration-classic), 20 cells.
Primary basis: scored-clean (19 cells; ZECUSDT_intraday excluded per G-8).
Reference basis: scored-20 (all 20 cells).

READ-ONLY. No engine writes, no config edits, no replay, no network.
Reads raw journal JSONL bytes + local kline parquet caches only.
Prior reports (ROLLUPS_AND_HYPOTHESES.md, V3_RECOMPUTE_R1_R10.md, forensics
docs) are cross-checks, NEVER inputs.

------------------------------------------------------------------ definitions
Carried unchanged from R1-R10 (all confirmed there):
  one_r  = |px_fill - stop| * qty / size_r   from the ENTRY (fill) row, SIGNED
           (qty is journaled signed; negative where a cell traded on negative
           equity -- the literal signed form reproduces F3/F4).
  cost   = fees + funding_cum + slippage      from the EXIT row (cumulative).
  cost_r = cost / one_r
  r_0x   = realized_r + cost_r   (gross, costs removed)
  r_1x   = realized_r           (net, as journaled; size-weighted cell-R)
  r_2x   = realized_r - cost_r
  join on (cell_id, tranche_id); tranche_id = c<campaign>t<seq>.
  mandate = cell_id.rpartition('_')[2].

NEW this phase (§4):
  open interval of a tranche = [fill_ts, exit_ts) : fill row ts_open inclusive,
    EXIT row ts_open exclusive; exit_ts = None => still open at data end (+inf).
  concurrent_open_at_fill(A) = # siblings B in same (cell,campaign), B!=A, with
    B.fill_ts <= A.fill_ts AND (A.fill_ts < B.exit_ts OR B.fill_ts == A.fill_ts).
    (B.exit_ts None -> +inf.) SAME-BAR SIBLINGS COUNT AS CONCURRENT.
  true add  = ADD_FILL with concurrent_open_at_fill >= 1
  re-entry  = ADD_FILL with concurrent_open_at_fill == 0
  R1        = ENTRY_FILL, not V ;  V = ENTRY_FILL with is_v
  max_concurrent(campaign) = peak simultaneously-open tranches; event sweep with
    SAME-BAR FILLS BEFORE SAME-BAR EXITS at equal ts_open (tie-break).
  direction-run = maximal same-cell same-direction campaign run in journal time
    order (ordered by opener fill_ts); attempt number = 1-based index in run.
  cluster: attempt in-cluster at k iff
    |opener.px_fill - attempt1.opener.px_fill| <= k * atr_exec(attempt1 fill).
  bps (per tranche, ENTRY-row prices except cumulative cost from EXIT):
    stop_dist_px = |px_fill - stop|
    mfe_bps      = mfe_r * (stop_dist_px / px_fill) * 1e4
    cost_bps     = cost_usd / (|qty| * px_fill) * 1e4       (round-trip cost)
    realized_bps = (realized_r / size_r) * (stop_dist_px / px_fill) * 1e4

Usage: python scripts/rc_recompute.py [--journal-root P] [--kline-root P]
       [--out-dir P]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

# ------------------------------------------------------------------ constants
SEED = 20260716              # pinned bootstrap seed (contract invariant 6)
N_BOOT = 10_000
MANDATES = ["swing", "intraday", "position"]
GRID = "GRID"
GRADES = ["A+", "A", "B", "-", "V"]
CLEAN_EXCLUDE = "ZECUSDT_intraday"         # scored-clean drops this cell (G-8)
TID_RE = re.compile(r"^c(\d+)t(\d+)$")
FILL_EVTS = ("ENTRY_FILL", "ADD_FILL")
ROWS_KEPT = {"ENTRY_FILL", "ADD_FILL", "EXIT", "REJECT"}
TRANCHE_CAP_REASON = "max_tranches"        # engine name for the tranche ceiling
INITIAL_EQUITY = 10000.0                   # v12_anchor.yaml trading.initial_equity

RC0_ASSETS = ["BTCUSDT", "ETHUSDT", "JTOUSDT", "NEARUSDT", "SOLUSDT",
              "TAOUSDT", "ZECUSDT", "HYPEUSDT", "FARTCOINUSDT", "LITUSDT"]
RC0_TFS = ["1m", "5m", "15m", "30m", "1h", "4h", "12h", "1d"]
TF_SECONDS = {"1m": 60, "5m": 300, "15m": 900, "30m": 1800, "1h": 3600,
              "4h": 14400, "12h": 43200, "1d": 86400}

FIXTURES = {
    "F1_campaigns": 3456, "F1_tranches": 8387,
    "F2_sum_realized_r": -5756.9093,
    "F3_sum_r_0x": 1345.3095,
    "F4_zec_tranches": 1414, "F4_zec_neg_one_r": 717,
    "F5_zec_net_1x": -663.1247,
    "F6_scored_clean_1x": -5093.7846,
    "F7_stop_events": 7057,
    "F8_tranche_cap_rejects": 145749,
    "F9_v_campaigns": 45,
    "F10_resumption": 2899,
}
TOL_TIGHT = 1e-4
TOL_LOOSE = 1e-3


# ------------------------------------------------------------------ utilities
def mandate_of(cell_id):
    return cell_id.rpartition("_")[2]


def parse_ts(s):
    if s is None:
        return None
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def r4(x):
    return None if x is None else round(float(x) + 0.0, 4)


def r6(x):
    return None if x is None else round(float(x) + 0.0, 6)


def pct(x, d):
    return None if not d else r4(100.0 * x / d)


def boot_ci(vals, seed=SEED, n=N_BOOT):
    """95% bootstrap CI of the mean; fixed seed -> deterministic."""
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


def deciles(vals):
    a = np.asarray(list(vals), dtype=float)
    if a.size == 0:
        return None
    return [r4(v) for v in np.percentile(a, [10, 20, 30, 40, 50, 60, 70, 80, 90])]


# ------------------------------------------------------------------ load
def load_scored(root):
    """Raw journal bytes from the scored partition. Returns (cells, rows,
    evt_census, tranche_cap_rejects)."""
    cells = sorted(p.name for p in root.iterdir() if p.is_dir())
    rows = []
    evt_census = Counter()
    tranche_cap = 0
    for cell in cells:
        for path in sorted((root / cell).glob("*.jsonl")):
            with open(path, encoding="utf-8") as f:
                for line in f:
                    if not line.strip():
                        continue
                    r = json.loads(line)
                    evt_census[r["evt"]] += 1
                    if r["evt"] == "REJECT" and \
                            r.get("reject_reason") == TRANCHE_CAP_REASON:
                        tranche_cap += 1
                    if r["evt"] in ROWS_KEPT:
                        rows.append(r)
    return cells, rows, evt_census, tranche_cap


class Book:
    """Joined tranche-level view with concurrency, campaign and attempt census."""

    def __init__(self, rows):
        self.exits = [r for r in rows if r["evt"] == "EXIT"]
        self.fills = [r for r in rows if r["evt"] in FILL_EVTS]
        self.rejects = [r for r in rows if r["evt"] == "REJECT"]
        self.exit_by = {(r["cell_id"], r["tranche_id"]): r for r in self.exits}

        # -------- one record per FILL (resolved or not) --------
        self.tr = []            # every fill -> a tranche record
        for f in self.fills:
            m = TID_RE.match(f["tranche_id"] or "")
            if not m:
                continue
            camp = (f["cell_id"], int(m.group(1)))
            seq = int(m.group(2))
            e = self.exit_by.get((f["cell_id"], f["tranche_id"]))
            fill_ts = parse_ts(f["ts_open"])
            exit_ts = parse_ts(e["ts_open"]) if e else None
            one_r = abs(f["px_fill"] - f["stop"]) * f["qty"] / f["size_r"]
            rec = {
                "cell_id": f["cell_id"], "mandate": mandate_of(f["cell_id"]),
                "camp": camp, "seq": seq, "tranche_id": f["tranche_id"],
                "dir": f["dir"], "fill_evt": f["evt"],
                "fill_ts": fill_ts, "exit_ts": exit_ts,
                "entry_px": f["px_fill"], "entry_stop": f["stop"],
                "entry_qty": f["qty"], "size_r": f["size_r"],
                "entry_atr": f["atr_exec"], "zone": f["zone"] or "-",
                "grade_entry": f["grade"], "stage": f["stage"],
                "retr": f["retr"], "tf_exec": f["tf_exec"], "one_r": one_r,
                "resolved": e is not None,
            }
            if e is not None:
                cost = (e["fees"] or 0.0) + (e["funding_cum"] or 0.0) + \
                    (e["slippage"] or 0.0)
                sh = e.get("shadow") or {}
                rec.update({
                    "realized_r": e["realized_r"],
                    "cost": cost, "cost_r": cost / one_r,
                    "r_0x": e["realized_r"] + cost / one_r,
                    "r_2x": e["realized_r"] - cost / one_r,
                    "exit_reason": e["exit_reason"],
                    "cont_20": e.get("postexit_cont_20"),
                    "mfe_r": e["mfe_r"], "mae_r": e["mae_r"],
                    "grade": e["grade"], "zone_exit": e["zone"] or "-",
                    "is_v": sh.get("ladder_unthrottled_grade") == "V",
                    "equity_after": e.get("equity_after"),
                    "exit_ts_raw": e["ts_open"],
                })
            else:
                rec.update({
                    "realized_r": None, "cost": None, "cost_r": None,
                    "r_0x": None, "r_2x": None, "exit_reason": None,
                    "cont_20": None, "mfe_r": None, "mae_r": None,
                    "grade": f["grade"], "zone_exit": f["zone"] or "-",
                    "is_v": False, "equity_after": None, "exit_ts_raw": None,
                })
            self.tr.append(rec)

        # -------- group by campaign --------
        self.camp_tr = defaultdict(list)
        for x in self.tr:
            self.camp_tr[x["camp"]].append(x)
        for c in self.camp_tr:
            self.camp_tr[c].sort(key=lambda x: (x["fill_ts"], x["seq"]))

        # -------- concurrency per tranche & max_concurrent per campaign --------
        for c, members in self.camp_tr.items():
            for a in members:
                conc = 0
                for b in members:
                    if b is a:
                        continue
                    if b["fill_ts"] <= a["fill_ts"]:
                        if b["fill_ts"] == a["fill_ts"]:
                            conc += 1
                        elif b["exit_ts"] is None or a["fill_ts"] < b["exit_ts"]:
                            conc += 1
                a["concurrent_open_at_fill"] = conc
                # classify fill
                if a["fill_evt"] == "ENTRY_FILL":
                    a["fclass"] = "V" if a["is_v"] else "R1"
                else:  # ADD_FILL
                    a["fclass"] = "true_add" if conc >= 1 else "re_entry"

        self.max_conc = {}
        for c, members in self.camp_tr.items():
            events = []
            for x in members:
                events.append((x["fill_ts"], 0, +1))      # 0 => fill first
                if x["exit_ts"] is not None:
                    events.append((x["exit_ts"], 1, -1))  # 1 => exit after
            events.sort(key=lambda e: (e[0], e[1]))
            cur = mx = 0
            for _, _, d in events:
                cur += d
                mx = max(mx, cur)
            self.max_conc[c] = mx

        # resolved-tranche convenience view. Reporting campaign set = campaigns
        # with >=1 RESOLVED tranche (matches fixture F1 / prior reader). camp_tr
        # keeps ALL tranches (resolved + open-at-data-end) for concurrency.
        self.t = [x for x in self.tr if x["resolved"]]
        self.camps = sorted(c for c in self.camp_tr
                            if any(x["resolved"] for x in self.camp_tr[c]))

        # V-initiated campaign = opener (lowest fill_ts/seq) is a resolved V
        self.v_camps = set()
        for c in self.camps:
            if self.camp_tr[c][0]["is_v"]:
                self.v_camps.add(c)

        # initiating (opener) tranche + campaign zone/dir
        self.camp_open = {}
        self.camp_zone = {}
        self.camp_dir = {}
        for c, members in self.camp_tr.items():
            opener = members[0]
            self.camp_open[c] = opener
            self.camp_zone[c] = opener["zone"]
            self.camp_dir[c] = opener["dir"]

        # -------- direction-runs & attempt numbers --------
        self.attempt = {}       # camp -> attempt number in its direction-run
        self.run_id = {}        # camp -> (cell, run_index)
        self.run_len = {}       # (cell,run_index) -> length
        by_cell = defaultdict(list)
        for c in self.camps:
            by_cell[c[0]].append(c)
        for cell, cs in by_cell.items():
            cs.sort(key=lambda c: (self.camp_open[c]["fill_ts"],
                                   self.camp_open[c]["seq"]))
            run_idx = 0
            prev_dir = None
            att = 0
            for c in cs:
                d = self.camp_dir[c]
                if d != prev_dir:
                    run_idx += 1
                    att = 0
                    prev_dir = d
                att += 1
                self.attempt[c] = att
                self.run_id[c] = (cell, run_idx)
            for c in cs:
                rid = self.run_id[c]
                self.run_len[rid] = self.run_len.get(rid, 0) + 1
        # attempt-1 opener of each direction-run (cluster reference)
        self.run_first = {}
        for c in self.camps:
            rid = self.run_id[c]
            if self.attempt[c] == 1:
                self.run_first[rid] = c

    # ---- campaign roll-up ----
    def camp_realized(self, c, weightfn=None):
        s = 0.0
        for x in self.camp_tr[c]:
            if not x["resolved"]:
                continue
            w = 1.0 if weightfn is None else weightfn(x)
            s += x["realized_r"] * w
        return s


# ------------------------------------------------------------------ basis
def clean(items):
    return [x for x in items if x["cell_id"] != CLEAN_EXCLUDE]


def clean_camps(camps):
    return [c for c in camps if c[0] != CLEAN_EXCLUDE]


# ------------------------------------------------------------------ aggregates
def camp_agg(book, camps, weightfn=None):
    """Campaign-level 0x/1x/2x aggregate + bootstrap CI + strip-best."""
    v1, v0, v2 = [], [], []
    for c in camps:
        s1 = s0 = s2 = 0.0
        for x in book.camp_tr[c]:
            if not x["resolved"]:
                continue
            w = 1.0 if weightfn is None else weightfn(x)
            if w == 0.0:
                continue
            s1 += x["realized_r"] * w
            s0 += x["r_0x"] * w
            s2 += x["r_2x"] * w
        v1.append(s1); v0.append(s0); v2.append(s2)
    n = len(v1)
    if not n:
        return {"campaigns": 0}
    lo, hi = boot_ci(v1)
    best = max(v1)
    return {
        "campaigns": n,
        "sum_0x": r4(sum(v0)), "sum_1x": r4(sum(v1)), "sum_2x": r4(sum(v2)),
        "expectancy_1x": r4(sum(v1) / n),
        "ci95_lo": lo, "ci95_hi": hi,
        "win_rate_pct": pct(sum(1 for v in v1 if v > 0), n),
        "strip_best_sum_1x": r4(sum(v1) - best),
        "strip_best_expectancy_1x": r4((sum(v1) - best) / (n - 1)) if n > 1 else None,
        "best_campaign_r": r4(best),
    }


def unit_agg(ts):
    """Tranche-level per-unit + cell-R roll-up over a resolved-tranche list."""
    ts = [x for x in ts if x["resolved"]]
    n = len(ts)
    if not n:
        return {"n": 0}
    ssize = sum(x["size_r"] for x in ts)
    s1 = sum(x["realized_r"] for x in ts)
    s0 = sum(x["r_0x"] for x in ts)
    s2 = sum(x["r_2x"] for x in ts)
    scost = sum(x["cost_r"] for x in ts)
    return {
        "n": n, "sum_size_r": r4(ssize),
        "sum_cell_r_0x": r4(s0), "sum_cell_r_1x": r4(s1), "sum_cell_r_2x": r4(s2),
        "per_unit_gross_0x": r4(s0 / ssize) if ssize else None,
        "per_unit_net_1x": r4(s1 / ssize) if ssize else None,
        "per_unit_cost": r4(scost / ssize) if ssize else None,
        "win_rate_pct": pct(sum(1 for x in ts if x["realized_r"] > 0), n),
    }


# ------------------------------------------------------------------ RC-0
def rc0(kline_root):
    caveat = ("Filesystem-only inventory, no network. Row counts / bounds / gaps "
              "read from the local parquet caches (open_time column). Resamplability "
              "is a FEASIBILITY statement only; resampling is S-1 data-prep, out of "
              "scope. Absence here = absent from THIS machine's cache, not "
              "necessarily un-fetchable upstream.")
    out = {"caveat": caveat, "kline_root": str(kline_root), "assets": {}}
    try:
        import pyarrow.parquet as pq
    except Exception as ex:  # pragma: no cover
        out["error"] = f"pyarrow unavailable: {ex}"
        return out
    for asset in RC0_ASSETS:
        arec = {}
        present_tfs = set()
        for tf in RC0_TFS:
            path = kline_root / f"{asset}_{tf}.parquet"
            if not path.exists():
                arec[tf] = {"present": False}
                continue
            present_tfs.add(tf)
            ot = pq.read_table(path, columns=["open_time"]).column(0).to_numpy()
            ot = np.sort(ot)
            interval_ms = TF_SECONDS[tf] * 1000
            gaps = 0
            if ot.size > 1:
                d = np.diff(ot)
                gaps = int(np.count_nonzero(d > 2 * interval_ms))
            arec[tf] = {
                "present": True, "rows": int(ot.size),
                "first_utc": datetime.fromtimestamp(int(ot[0]) / 1000, timezone.utc)
                    .strftime("%Y-%m-%d %H:%M:%S") if ot.size else None,
                "last_utc": datetime.fromtimestamp(int(ot[-1]) / 1000, timezone.utc)
                    .strftime("%Y-%m-%d %H:%M:%S") if ot.size else None,
                "gaps_gt_2x_tf": gaps,
            }
        # absence flags for {15m,30m,1d}
        absent_focus = [tf for tf in ("15m", "30m", "1d") if tf not in present_tfs]
        resamp = {}
        for tf in absent_focus:
            if tf == "30m":
                srcs = [s for s in ("15m", "1m") if s in present_tfs]
                resamp[tf] = ("resamplable from " + "/".join(srcs)) if srcs \
                    else "NOT locally resamplable (need 15m or 1m)"
            elif tf == "1d":
                srcs = [s for s in ("1h", "1m") if s in present_tfs]
                resamp[tf] = ("resamplable from " + "/".join(srcs)) if srcs \
                    else "NOT locally resamplable (need 1h or 1m)"
            elif tf == "15m":
                srcs = [s for s in ("5m", "1m") if s in present_tfs]
                resamp[tf] = ("resamplable from " + "/".join(srcs)) if srcs \
                    else "NOT locally resamplable"
        arec["_absent_focus_tfs"] = absent_focus
        arec["_resamplability"] = resamp
        out["assets"][asset] = arec
    return out


# ------------------------------------------------------------------ RC-1
def rc1(book, basis, camps, tr_all):
    caveat = ("Classification is OBSERVATIONAL. Selection effects (an add requires "
              "ratchet-to-BE which requires a trend) mean cohort differences are NOT "
              "causal effects of adding. Ranks/sizes only. Same-bar siblings count as "
              "concurrent; exit interval is half-open [fill_ts, exit_ts).")
    out = {"caveat": caveat, "basis": basis}

    # (a) fill-class census over ALL fills in basis + per-unit over resolved
    fills = [x for x in tr_all]
    add_fills = [x for x in fills if x["fill_evt"] == "ADD_FILL"]
    n_add = len(add_fills)
    n_true = sum(1 for x in add_fills if x["fclass"] == "true_add")
    n_re = sum(1 for x in add_fills if x["fclass"] == "re_entry")
    out["add_fill_census"] = {
        "add_fills_total": n_add,
        "true_add": n_true, "re_entry": n_re,
        "true_add_pct": pct(n_true, n_add), "re_entry_pct": pct(n_re, n_add),
    }
    out["by_fill_class"] = {}
    for cls in ("R1", "true_add", "re_entry", "V"):
        sub = [x for x in fills if x["fclass"] == cls]
        d = unit_agg(sub)
        d["fills_total"] = len(sub)
        d["fills_resolved"] = sum(1 for x in sub if x["resolved"])
        out["by_fill_class"][cls] = d

    # (b) campaign table by max_concurrent bucket
    out["by_max_concurrent"] = {}
    buckets = defaultdict(list)
    for c in camps:
        mc = book.max_conc[c]
        key = mc if mc <= 3 else 4
        buckets[key].append(c)
    for key in sorted(buckets):
        label = str(key) if key <= 3 else "4+"
        out["by_max_concurrent"][label] = camp_agg(book, buckets[key])

    # (c) real-pyramid population: campaigns with >=1 true add ever
    pyr = [c for c in camps
           if any(x["fclass"] == "true_add" for x in book.camp_tr[c])]
    a = camp_agg(book, pyr)
    # share of sum(wins)
    wins = sum(book.camp_realized(c) for c in camps if book.camp_realized(c) > 0)
    pyr_wins = sum(book.camp_realized(c) for c in pyr if book.camp_realized(c) > 0)
    a["share_of_sum_wins_pct"] = pct(pyr_wins, wins)
    a["sum_wins_basis"] = r4(wins)
    a["pyramid_sum_wins"] = r4(pyr_wins)
    out["real_pyramid"] = a

    # (d) top-10 campaigns by cell-R
    ranked = sorted(camps, key=lambda c: -book.camp_realized(c))[:10]
    top = []
    for c in ranked:
        members = book.camp_tr[c]
        top.append({
            "campaign": f"{c[0]}#c{c[1]}",
            "cell_r_1x": r4(book.camp_realized(c)),
            "tranches": len(members),
            "max_concurrent": book.max_conc[c],
            "structure": "stacked (pyramid)" if book.max_conc[c] >= 3
                         else ("partial-stack" if book.max_conc[c] == 2
                               else "serial (re-entries)"),
            "fill_classes": dict(Counter(x["fclass"] for x in members)),
        })
    out["top10_by_cell_r"] = top
    out["top10_serial_count"] = sum(1 for t in top if t["max_concurrent"] < 3)
    out["top10_stacked_count"] = sum(1 for t in top if t["max_concurrent"] >= 3)

    # (e) fill-spacing distribution (bars between consecutive fills), by class
    spacing = {"true_add": [], "re_entry": []}
    for c in camps:
        members = book.camp_tr[c]
        for prev, cur in zip(members, members[1:]):
            if cur["fclass"] not in spacing:
                continue
            sec = (cur["fill_ts"] - prev["fill_ts"]).total_seconds()
            bar = TF_SECONDS.get(cur["tf_exec"])
            if bar:
                spacing[cur["fclass"]].append(sec / bar)
    out["fill_spacing_bars"] = {}
    for cls, vals in spacing.items():
        if vals:
            a = np.asarray(vals, dtype=float)
            out["fill_spacing_bars"][cls] = {
                "n_gaps": len(vals), "median": r4(np.median(a)),
                "mean": r4(a.mean()), "deciles": deciles(vals),
                "min": r4(a.min()), "max": r4(a.max()),
            }
        else:
            out["fill_spacing_bars"][cls] = {"n_gaps": 0}
    return out


# ------------------------------------------------------------------ RC-2
def rc2(book, cells, rows_by_cell_exit):
    caveat = ("Equity path reconstructed from EXIT-row equity_after (the only rows "
              "carrying it), in journal file order per cell. initial_equity = "
              "10000.0 (v12_anchor.yaml). Zero-crossing = the equity_after series "
              "reaches <= 0. Certifies the scored-clean basis.")
    out = {"caveat": caveat, "initial_equity": INITIAL_EQUITY, "cells": {}}
    crossers = []
    for cell in cells:
        seq = rows_by_cell_exit.get(cell, [])
        eq = [e.get("equity_after") for e in seq if e.get("equity_after") is not None]
        if not eq:
            out["cells"][cell] = {"exits_with_equity": 0}
            continue
        ts = [e["ts_open"] for e in seq if e.get("equity_after") is not None]
        arr = np.asarray(eq, dtype=float)
        imin = int(np.argmin(arr))
        # zero crossings over [initial, e1, e2, ...]
        full = [INITIAL_EQUITY] + eq
        zc = 0
        for p, q in zip(full, full[1:]):
            if (p > 0) != (q > 0):
                zc += 1
        crossed = bool(arr.min() <= 0.0)
        rec = {
            "exits_with_equity": len(eq),
            "initial_equity": INITIAL_EQUITY,
            "min_equity": r4(float(arr.min())),
            "min_equity_ts": ts[imin],
            "final_equity": r4(float(eq[-1])),
            "zero_crossings": zc,
            "crossed_zero": crossed,
            "near_miss_lt_20pct_initial": bool(arr.min() < 0.20 * INITIAL_EQUITY),
        }
        out["cells"][cell] = rec
        if crossed and cell != CLEAN_EXCLUDE:
            crossers.append(cell)
    out["certification"] = {
        "expected_sole_zero_crosser": CLEAN_EXCLUDE,
        "other_cells_that_crossed_zero": crossers,
        "scored_clean_basis_valid": len(crossers) == 0,
        "verdict": ("CERTIFIED: no cell other than ZECUSDT_intraday crossed zero"
                    if not crossers else
                    f"VIOLATION: additional zero-crossing cells {crossers} -- "
                    "scored-clean basis is WRONG; phase halts after RC-2"),
    }
    return out


# ------------------------------------------------------------------ RC-3
def bps_fields(x):
    stop_dist = abs(x["entry_px"] - x["entry_stop"])
    px = x["entry_px"]
    if px == 0:
        return None
    mfe_bps = x["mfe_r"] * (stop_dist / px) * 1e4 if x["mfe_r"] is not None else None
    denom = abs(x["entry_qty"]) * px
    cost_bps = (x["cost"] / denom) * 1e4 if denom else None
    realized_bps = (x["realized_r"] / x["size_r"]) * (stop_dist / px) * 1e4
    ratio = (mfe_bps / cost_bps) if (mfe_bps is not None and cost_bps not in
                                     (None, 0.0)) else None
    return {"mfe_bps": mfe_bps, "cost_bps": cost_bps,
            "realized_bps": realized_bps, "ratio": ratio}


def _dist(vals):
    a = np.asarray([v for v in vals if v is not None], dtype=float)
    if a.size == 0:
        return {"n": 0}
    return {"n": int(a.size), "mean": r4(a.mean()), "median": r4(np.median(a)),
            "deciles": deciles(a)}


def rc3(tr_resolved, basis):
    caveat = ("The most fundamental number: does favourable excursion exceed "
              "round-trip cost IN PRICE TERMS, before R-space amplification. "
              "Per-tranche. bps use ENTRY-row prices; cost is round-trip cumulative "
              "from the EXIT row. Negative-one_r rows (bankrupt-cell) keep valid "
              "price ratios but corrupted R sign -- excluded already in scored-clean.")
    out = {"caveat": caveat, "basis": basis, "by_mandate": {}, "by_grade": {}}
    recs = []
    for x in tr_resolved:
        b = bps_fields(x)
        if b is None:
            continue
        b = dict(b, mandate=x["mandate"], grade=x["grade"])
        recs.append(b)
    for scope, keyfn in (("GRID", lambda r: True),
                         *[(m, (lambda r, m=m: r["mandate"] == m)) for m in MANDATES]):
        sub = [r for r in recs if keyfn(r)]
        n = len(sub)
        gt = sum(1 for r in sub if r["mfe_bps"] is not None and r["cost_bps"]
                 is not None and r["mfe_bps"] > r["cost_bps"])
        out["by_mandate"][scope] = {
            "n": n,
            "mfe_bps": _dist([r["mfe_bps"] for r in sub]),
            "cost_bps": _dist([r["cost_bps"] for r in sub]),
            "realized_bps": _dist([r["realized_bps"] for r in sub]),
            "ratio_mfe_over_cost": _dist([r["ratio"] for r in sub]),
            "frac_mfe_gt_cost_pct": pct(gt, n),
        }
    for g in GRADES:
        sub = [r for r in recs if r["grade"] == g]
        if not sub:
            continue
        n = len(sub)
        gt = sum(1 for r in sub if r["mfe_bps"] is not None and r["cost_bps"]
                 is not None and r["mfe_bps"] > r["cost_bps"])
        out["by_grade"][g] = {
            "n": n,
            "mfe_bps": _dist([r["mfe_bps"] for r in sub]),
            "cost_bps": _dist([r["cost_bps"] for r in sub]),
            "ratio_mfe_over_cost": _dist([r["ratio"] for r in sub]),
            "frac_mfe_gt_cost_pct": pct(gt, n),
        }
    return out


# ------------------------------------------------------------------ RC-4
def stop_atr(x):
    if x["entry_atr"] in (None, 0):
        return None
    return abs(x["entry_px"] - x["entry_stop"]) / x["entry_atr"]


def rc4(book, tr_resolved, camps, basis):
    caveat = ("First-order: removing tranches by stop-distance does NOT change the "
              "stop path (ratchet is signal-layer), but DOES change the equity path, "
              "the 1R campaign rail and the halt calendar -- faithful measurement is "
              "S-1's job. Null atr_exec rows are KEPT (cannot evaluate) and counted.")
    out = {"caveat": caveat, "basis": basis}
    valued = [(stop_atr(x), x) for x in tr_resolved]
    have = [(v, x) for v, x in valued if v is not None]
    out["n_null_atr_kept"] = sum(1 for v, x in valued if v is None)

    # (a) deciles of stop_dist/ATR
    vals = np.asarray([v for v, x in have], dtype=float)
    edges = np.percentile(vals, [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
    out["decile_edges"] = [r4(e) for e in edges]
    rows = []
    for i in range(10):
        lo, hi = edges[i], edges[i + 1]
        if i < 9:
            sub = [x for v, x in have if lo <= v < hi]
        else:
            sub = [x for v, x in have if lo <= v <= hi]
        d = unit_agg(sub)
        d["decile"] = i + 1
        d["edge_lo"] = r4(lo); d["edge_hi"] = r4(hi)
        rows.append(d)
    out["deciles"] = rows

    # (b) floor curve
    floor = {}
    camp_set = set(camps)
    for X in (0.30, 0.40, 0.50, 0.60, 0.75, 1.00, 1.25, 1.50):
        def wf(x, X=X):
            v = stop_atr(x)
            return 0.0 if (v is not None and v < X) else 1.0
        kept_camps = [c for c in camps
                      if any(wf(x) != 0.0 for x in book.camp_tr[c] if x["resolved"])]
        a = camp_agg(book, kept_camps, weightfn=wf)
        a["tranches_kept"] = sum(1 for x in tr_resolved if wf(x) != 0.0)
        a["tranches_removed"] = sum(1 for x in tr_resolved if wf(x) == 0.0)
        floor[f"{X:.2f}"] = a
    out["floor_curve"] = floor
    return out


# ------------------------------------------------------------------ RC-5
def rc5(book, camps, basis):
    caveat = ("First-order Z1 lever. Campaign zone = the initiating tranche's zone. "
              "Drop / half-size re-weights realized_r linearly (pnl scales with qty "
              "scales with size_r at fixed unit risk). Equity-path / rail / halt "
              "effects are S-1's job.")
    out = {"caveat": caveat, "basis": basis}
    z1 = [c for c in camps if book.camp_zone[c] == "Z1"]
    out["z1_initiated_campaigns"] = len(z1)
    out["z1_share_pct"] = pct(len(z1), len(camps))
    out["neutral_live"] = camp_agg(book, camps)
    # (a) drop Z1-initiated
    out["drop_z1"] = camp_agg(book, [c for c in camps if book.camp_zone[c] != "Z1"])
    # (b) half-size Z1-initiated
    z1set = set(z1)

    def wf_half(x, z1set=z1set):
        return 0.5 if x["camp"] in z1set else 1.0
    out["halfsize_z1"] = camp_agg(book, camps, weightfn=wf_half)
    # first-order 1x delta vs neutral (for P-RC5)
    out["drop_z1_delta_1x_vs_neutral"] = r4(
        out["drop_z1"]["sum_1x"] - out["neutral_live"]["sum_1x"])
    return out


# ------------------------------------------------------------------ RC-6
def rc6(book, camps, basis):
    caveat = ("Attempt = campaign opener within its direction-run (maximal same-cell "
              "same-direction run, journal time order). Cluster distance uses the "
              "attempt-1 opener's fill price and ATR. Expectancy is campaign cell-R. "
              "First-order counterfactual only.")
    out = {"caveat": caveat, "basis": basis}
    cset = set(camps)

    # (a) attempts-per-direction-run distribution (runs whose campaigns are in basis)
    run_members = defaultdict(list)
    for c in camps:
        run_members[book.run_id[c]].append(c)
    run_sizes = Counter(len(v) for v in run_members.values())
    out["attempts_per_run_distribution"] = {str(k): run_sizes[k]
                                             for k in sorted(run_sizes)}
    out["n_direction_runs"] = len(run_members)

    # (b) expectancy + sum cell-R by attempt number bucket
    def att_bucket(c):
        a = book.attempt[c]
        return "4+" if a >= 4 else str(a)
    out["by_attempt"] = {}
    for b in ("1", "2", "3", "4+"):
        cs = [c for c in camps if att_bucket(c) == b]
        out["by_attempt"][b] = camp_agg(book, cs) if cs else {"campaigns": 0}

    # cluster membership per attempt at k
    def cluster_flag(c, k):
        rid = book.run_id[c]
        # attempt-1 opener of this run (same cell; independent of basis filter)
        first = book.run_first.get(rid)
        if first is None:
            return None
        atr = book.camp_open[first]["entry_atr"]
        if atr in (None, 0):
            return None
        d = abs(book.camp_open[c]["entry_px"] - book.camp_open[first]["entry_px"])
        return d <= k * atr

    # (c) in-cluster share of attempts 2+
    out["in_cluster_share_attempts_2plus"] = {}
    att2 = [c for c in camps if book.attempt[c] >= 2]
    for k in (0.5, 1.0, 1.5):
        flags = [cluster_flag(c, k) for c in att2]
        valid = [f for f in flags if f is not None]
        inc = sum(1 for f in valid if f)
        out["in_cluster_share_attempts_2plus"][f"{k:.1f}"] = {
            "attempts_2plus": len(att2), "evaluable": len(valid),
            "in_cluster": inc, "in_cluster_pct": pct(inc, len(valid)),
        }

    # (d) expectancy by attempt-number x in/out cluster (k=1.0)
    out["expectancy_by_attempt_x_cluster_k1.0"] = {}
    for b in ("1", "2", "3", "4+"):
        cs = [c for c in camps if att_bucket(c) == b]
        inc = [c for c in cs if cluster_flag(c, 1.0) is True]
        outc = [c for c in cs if cluster_flag(c, 1.0) is False]
        out["expectancy_by_attempt_x_cluster_k1.0"][b] = {
            "in_cluster": camp_agg(book, inc) if inc else {"campaigns": 0},
            "out_of_cluster": camp_agg(book, outc) if outc else {"campaigns": 0},
        }

    # (e) counterfactual bound: sum cell-R of in-cluster attempts 4+ (per k)
    out["counterfactual_incluster_attempts_4plus_sum_cell_r"] = {}
    att4 = [c for c in camps if book.attempt[c] >= 4]
    for k in (0.5, 1.0, 1.5):
        inc = [c for c in att4 if cluster_flag(c, k) is True]
        out["counterfactual_incluster_attempts_4plus_sum_cell_r"][f"{k:.1f}"] = {
            "campaigns": len(inc),
            "sum_cell_r_1x": r4(sum(book.camp_realized(c) for c in inc)),
        }
    return out


# ------------------------------------------------------------------ predictions
def score_predictions(rc1_clean, rc2, rc3_clean, rc4_clean, rc5_clean, rc6_clean):
    P = []

    # P-RC1a: re-entries >= 70% of ADD_FILL rows (scored-clean)
    cen = rc1_clean["add_fill_census"]
    v = cen["re_entry_pct"]
    P.append({"id": "P-RC1a", "prior": "75%",
              "claim": "Re-entries are >=70% of ADD_FILL rows",
              "falsified_if": "< 70%",
              "evidence": {"re_entry_pct": v, "add_fills_total": cen["add_fills_total"]},
              "verdict": "FALSIFIED" if (v is None or v < 70.0) else "CONFIRMED"})

    # P-RC1b: true-add per-unit gross >= re-entry per-unit gross
    ta = rc1_clean["by_fill_class"]["true_add"].get("per_unit_gross_0x")
    re_ = rc1_clean["by_fill_class"]["re_entry"].get("per_unit_gross_0x")
    ok = (ta is not None and re_ is not None and ta >= re_)
    P.append({"id": "P-RC1b", "prior": "55%",
              "claim": "True-add per-unit gross (0x) >= re-entry per-unit gross (0x)",
              "falsified_if": "true_add < re_entry",
              "evidence": {"true_add_per_unit_gross": ta, "re_entry_per_unit_gross": re_},
              "verdict": "CONFIRMED" if ok else "FALSIFIED"})

    # P-RC1c: majority of top-10 are serial (max_concurrent < 3)
    ser = rc1_clean["top10_serial_count"]
    stk = rc1_clean["top10_stacked_count"]
    P.append({"id": "P-RC1c", "prior": "60%",
              "claim": "Majority of top-10 campaigns are serial (max_concurrent<3)",
              "falsified_if": ">=5 of 10 have max_concurrent = 3",
              "evidence": {"serial_count": ser, "stacked_count": stk},
              "verdict": "FALSIFIED" if stk >= 5 else "CONFIRMED"})

    # P-RC2: no cell besides ZEC_intraday crossed zero
    crossers = rc2["certification"]["other_cells_that_crossed_zero"]
    P.append({"id": "P-RC2", "prior": "80%",
              "claim": "No cell besides ZECUSDT_intraday crossed zero",
              "falsified_if": "any other zero-crossing",
              "evidence": {"other_crossers": crossers},
              "verdict": "FALSIFIED" if crossers else "CONFIRMED"})

    # P-RC3: median mfe_bps>cost_bps on swing; median mfe_bps<cost_bps on intraday
    sw = rc3_clean["by_mandate"]["swing"]
    it = rc3_clean["by_mandate"]["intraday"]
    sw_mfe = sw["mfe_bps"]["median"]; sw_cost = sw["cost_bps"]["median"]
    it_mfe = it["mfe_bps"]["median"]; it_cost = it["cost_bps"]["median"]
    swing_ok = sw_mfe is not None and sw_cost is not None and sw_mfe > sw_cost
    intraday_ok = it_mfe is not None and it_cost is not None and it_mfe < it_cost
    P.append({"id": "P-RC3", "prior": "70%",
              "claim": "Median mfe_bps>cost_bps on swing; median mfe_bps<cost_bps on intraday",
              "falsified_if": "either half fails",
              "evidence": {"swing_mfe_med": sw_mfe, "swing_cost_med": sw_cost,
                           "intraday_mfe_med": it_mfe, "intraday_cost_med": it_cost},
              "verdict": "CONFIRMED" if (swing_ok and intraday_ok) else "FALSIFIED"})

    # P-RC4: net/unit by stop-distance decile non-monotone, max in 0.75-1.50 ATR band
    dec = rc4_clean["deciles"]
    nets = [d.get("per_unit_net_1x") for d in dec]
    valid = [(i, n) for i, n in enumerate(nets) if n is not None]
    imax = max(valid, key=lambda t: t[1])[0] if valid else None
    band_lo, band_hi = dec[imax]["edge_lo"], dec[imax]["edge_hi"]
    in_band = imax is not None and (band_hi > 0.75 and band_lo < 1.50)
    seq = [n for _, n in valid]
    monotone = all(a <= b for a, b in zip(seq, seq[1:])) or \
        all(a >= b for a, b in zip(seq, seq[1:]))
    P.append({"id": "P-RC4", "prior": "60%",
              "claim": "Net/unit by stop-distance decile is non-monotone; max in 0.75-1.50 ATR band",
              "falsified_if": "max outside band or monotone",
              "evidence": {"argmax_decile": None if imax is None else imax + 1,
                           "argmax_edge_lo": band_lo, "argmax_edge_hi": band_hi,
                           "monotone": monotone, "net_per_unit_by_decile": nets},
              "verdict": "CONFIRMED" if (in_band and not monotone) else "FALSIFIED"})

    # P-RC5: Z1-drop improves scored-clean 1x by >= +1500 cell-R first-order
    delta = rc5_clean["drop_z1_delta_1x_vs_neutral"]
    P.append({"id": "P-RC5", "prior": "65%",
              "claim": "Z1-drop improves scored-clean 1x by >= +1500 cell-R first-order",
              "falsified_if": "< +1500",
              "evidence": {"drop_z1_delta_1x": delta},
              "verdict": "CONFIRMED" if (delta is not None and delta >= 1500.0)
                         else "FALSIFIED"})

    # P-RC6: expectancy decays monotonically in attempt number (1>2>3)
    ba = rc6_clean["by_attempt"]
    e1 = ba["1"].get("expectancy_1x"); e2 = ba["2"].get("expectancy_1x")
    e3 = ba["3"].get("expectancy_1x")
    mono = (e1 is not None and e2 is not None and e3 is not None
            and e1 > e2 > e3)
    P.append({"id": "P-RC6", "prior": "55%",
              "claim": "Expectancy decays monotonically in attempt number (1>2>3)",
              "falsified_if": "any inversion",
              "evidence": {"exp_att1": e1, "exp_att2": e2, "exp_att3": e3},
              "verdict": "CONFIRMED" if mono else "FALSIFIED"})
    return P


# ------------------------------------------------------------------ markdown
def md_table(headers, rows):
    out = ["| " + " | ".join(str(h) for h in headers) + " |",
           "|" + "|".join("---" for _ in headers) + "|"]
    for r in rows:
        out.append("| " + " | ".join("" if v is None else str(v) for v in r) + " |")
    return "\n".join(out)


def render_md(res):
    L = []
    A = L.append
    m = res["meta"]
    A("# RC Recompute RC-0..RC-6 — Tier A (journal arithmetic + kline inventory)")
    A("")
    A(f"**Basis:** engine {m['engine_version']} (`{m['engine_commit']}`), config "
      f"`{m['config_id']}` (`{m['config_sha256'][:8]}...`), scored partition, "
      f"{m['n_cells']} cells.")
    A(f"**Primary basis:** scored-clean (19 cells; `{CLEAN_EXCLUDE}` excluded, G-8). "
      f"**Reference:** scored-20.")
    A(f"**Journal root:** `{m['journal_root']}`")
    A(f"**Evidence spend:** NONE (VR-1). **Engine delta:** NONE (read-only).")
    A(f"**Bootstrap:** 95% CI, {m['n_boot']:,} resamples, campaign-level, seed "
      f"`{m['seed']}` (pinned).")
    A("")
    A("> **Scope.** In-sample, on mined data. Ranks and sizes; validates nothing. "
      "Not a re-run, not TC-4, not S-1, not a variant nomination.")
    A("")

    # definitions
    A("## Definitions restatement (contract §4)")
    A("")
    for line in m["definitions"]:
        A(f"- {line}")
    A("")

    # fixtures
    A("## Fixtures F1–F10 — known-answer gates (contract §5)")
    A("")
    A("Computed from raw journal bytes; no prior report read as input.")
    A("")
    A(md_table(["#", "fixture", "expected", "computed", "result"],
               [[f["id"], f["name"], f["expected"], f["computed"],
                 "**MATCH**" if f["match"] else "**MISMATCH**"]
                for f in res["fixtures"]]))
    A("")
    A(f"**Fixture verdict: {res['fixture_verdict']}** — "
      f"{sum(1 for f in res['fixtures'] if f['match'])}/{len(res['fixtures'])} match.")
    A("")
    if res["fixture_verdict"] != "PASS":
        A("> **HALT — fixture mismatch. No deliverables produced.**")
        return "\n".join(L)

    # RC-0
    r = res["rc0"]
    A("## RC-0 — Data-estate inventory (filesystem only)")
    A("")
    A(f"> **Caveat.** {r['caveat']}")
    A("")
    A(f"Kline cache root: `{r['kline_root']}`")
    A("")
    rows = []
    for asset, arec in r["assets"].items():
        present = [tf for tf in RC0_TFS if arec.get(tf, {}).get("present")]
        absent = [tf for tf in RC0_TFS if not arec.get(tf, {}).get("present")]
        rows.append([asset, ", ".join(present), ", ".join(absent) or "—"])
    A(md_table(["asset", "TFs present", "TFs absent"], rows))
    A("")
    A("Per-TF detail (rows / first / last / gaps>2×TF):")
    A("")
    rows = []
    for asset, arec in r["assets"].items():
        for tf in RC0_TFS:
            d = arec.get(tf, {})
            if d.get("present"):
                rows.append([asset, tf, d["rows"], d["first_utc"], d["last_utc"],
                             d["gaps_gt_2x_tf"]])
    A(md_table(["asset", "TF", "rows", "first UTC", "last UTC", "gaps>2×TF"], rows))
    A("")
    A("Absent focus TFs {15m,30m,1d} and local resamplability (feasibility only):")
    A("")
    rows = []
    for asset, arec in r["assets"].items():
        for tf, msg in arec.get("_resamplability", {}).items():
            rows.append([asset, tf, msg])
    A(md_table(["asset", "absent TF", "resamplable?"], rows))
    A("")

    # RC-1 (both bases)
    for basis_key, label in (("clean", "scored-clean (primary)"),
                             ("scored20", "scored-20 (reference)")):
        r = res["rc1"][basis_key]
        A(f"## RC-1 — Concurrency census + add/re-entry — {label}")
        A("")
        if basis_key == "clean":
            A(f"> **Caveat.** {r['caveat']}")
            A("")
        cen = r["add_fill_census"]
        A(f"**(a) ADD_FILL classification.** {cen['add_fills_total']:,} ADD_FILL "
          f"rows: true-add {cen['true_add']:,} ({cen['true_add_pct']}%), re-entry "
          f"{cen['re_entry']:,} ({cen['re_entry_pct']}%).")
        A("")
        rows = []
        for cls in ("R1", "true_add", "re_entry", "V"):
            d = r["by_fill_class"][cls]
            if d.get("n"):
                rows.append([cls, d["fills_total"], d["fills_resolved"],
                             d["sum_cell_r_1x"], d["per_unit_net_1x"],
                             d["per_unit_gross_0x"], d["win_rate_pct"]])
            else:
                rows.append([cls, d.get("fills_total", 0), 0, None, None, None, None])
        A(md_table(["fill class", "fills", "resolved", "Σ cell-R 1×",
                    "per-unit net 1×", "per-unit gross 0×", "win rate %"], rows))
        A("")
        A("**(b) Campaigns by max_concurrent.**")
        A("")
        rows = []
        for k, d in r["by_max_concurrent"].items():
            rows.append([k, d.get("campaigns"), d.get("sum_1x"),
                         d.get("expectancy_1x"),
                         f"[{d.get('ci95_lo')}, {d.get('ci95_hi')}]",
                         d.get("win_rate_pct"), d.get("strip_best_sum_1x")])
        A(md_table(["max_concurrent", "campaigns", "Σ 1×", "expectancy 1×",
                    "95% CI", "win rate %", "strip-best Σ 1×"], rows))
        A("")
        p = r["real_pyramid"]
        A(f"**(c) Real-pyramid population** (≥1 true add ever): "
          f"{p.get('campaigns')} campaigns, expectancy {p.get('expectancy_1x')}, "
          f"share of Σwins {p.get('share_of_sum_wins_pct')}%.")
        A("")
        A("**(d) Top-10 campaigns by cell-R:**")
        A("")
        rows = [[t["campaign"], t["cell_r_1x"], t["tranches"], t["max_concurrent"],
                 t["structure"], json.dumps(t["fill_classes"])]
                for t in r["top10_by_cell_r"]]
        A(md_table(["campaign", "cell-R 1×", "tranches", "max_concurrent",
                    "structure", "fill classes"], rows))
        A(f"\nSerial (max_concurrent<3): **{r['top10_serial_count']}/10**; "
          f"stacked (=3): {r['top10_stacked_count']}/10.")
        A("")
        A("**(e) Fill-spacing (bars between consecutive fills), by class:**")
        A("")
        rows = []
        for cls, d in r["fill_spacing_bars"].items():
            if d.get("n_gaps"):
                rows.append([cls, d["n_gaps"], d["median"], d["mean"],
                             d["min"], d["max"]])
            else:
                rows.append([cls, 0, None, None, None, None])
        A(md_table(["class", "n gaps", "median bars", "mean bars", "min", "max"], rows))
        A("")

    # RC-2
    r = res["rc2"]
    A("## RC-2 — Equity trajectories + clean-basis certification")
    A("")
    A(f"> **Caveat.** {r['caveat']}")
    A("")
    rows = []
    for cell, d in r["cells"].items():
        if not d.get("exits_with_equity"):
            rows.append([cell, 0, None, None, None, None, None])
            continue
        rows.append([cell, d["exits_with_equity"], d["min_equity"],
                     d["min_equity_ts"], d["final_equity"], d["zero_crossings"],
                     "YES" if d["crossed_zero"] else
                     ("near" if d["near_miss_lt_20pct_initial"] else "no")])
    A(md_table(["cell", "exits", "min equity", "min ts", "final equity",
                "zero-crossings", "crossed/near"], rows))
    A("")
    c = r["certification"]
    A(f"> **Certification.** {c['verdict']}")
    A("")

    if res.get("halted_after_rc2"):
        A("> **HALT (contract §8).** A second cell crossed zero — the scored-clean "
          "basis is wrong. RC-3..RC-6 not produced.")
        A("")
        return "\n".join(L)

    # RC-3
    for basis_key, label in (("clean", "scored-clean (primary)"),
                             ("scored20", "scored-20 (reference)")):
        r = res["rc3"][basis_key]
        A(f"## RC-3 — Edge in basis points — {label}")
        A("")
        if basis_key == "clean":
            A(f"> **Caveat.** {r['caveat']}")
            A("")
        rows = []
        for scope, d in r["by_mandate"].items():
            rows.append([scope, d["n"], d["mfe_bps"].get("median"),
                         d["cost_bps"].get("median"), d["realized_bps"].get("median"),
                         d["ratio_mfe_over_cost"].get("median"),
                         d["frac_mfe_gt_cost_pct"]])
        A(md_table(["scope", "n", "mfe_bps med", "cost_bps med", "realized_bps med",
                    "mfe/cost med", "frac mfe>cost %"], rows))
        A("")
        A("By grade (median bps):")
        A("")
        rows = []
        for g, d in r["by_grade"].items():
            rows.append([g, d["n"], d["mfe_bps"].get("median"),
                         d["cost_bps"].get("median"),
                         d["ratio_mfe_over_cost"].get("median"),
                         d["frac_mfe_gt_cost_pct"]])
        A(md_table(["grade", "n", "mfe_bps med", "cost_bps med", "mfe/cost med",
                    "frac mfe>cost %"], rows))
        A("")

    # RC-4
    for basis_key, label in (("clean", "scored-clean (primary)"),
                             ("scored20", "scored-20 (reference)")):
        r = res["rc4"][basis_key]
        A(f"## RC-4 — Stop-distance decile table + floor curve — {label}")
        A("")
        if basis_key == "clean":
            A(f"> **Caveat.** {r['caveat']}")
            A("")
        A(f"Null-atr tranches kept (unevaluable): {r['n_null_atr_kept']}.")
        A("")
        A("**(a) Deciles of stop_dist/ATR:**")
        A("")
        rows = []
        for d in r["deciles"]:
            rows.append([d["decile"], f"[{d['edge_lo']}, {d['edge_hi']})", d["n"],
                         d.get("per_unit_gross_0x"), d.get("per_unit_cost"),
                         d.get("per_unit_net_1x"), d.get("sum_cell_r_1x"),
                         d.get("win_rate_pct")])
        A(md_table(["decile", "stop/ATR range", "n", "gross/unit", "cost/unit",
                    "net/unit", "Σ cell-R 1×", "win %"], rows))
        A("")
        A("**(b) Floor curve** (remove tranches with stop/ATR < X, first-order):")
        A("")
        rows = []
        for X, d in r["floor_curve"].items():
            rows.append([X, d.get("tranches_removed"), d.get("campaigns"),
                         d.get("sum_0x"), d.get("sum_1x"), d.get("sum_2x"),
                         d.get("expectancy_1x")])
        A(md_table(["floor X", "tranches removed", "campaigns", "Σ 0×", "Σ 1×",
                    "Σ 2×", "expectancy 1×"], rows))
        A("")

    # RC-5
    for basis_key, label in (("clean", "scored-clean (primary)"),
                             ("scored20", "scored-20 (reference)")):
        r = res["rc5"][basis_key]
        A(f"## RC-5 — Z1 filter / tilt (first-order) — {label}")
        A("")
        if basis_key == "clean":
            A(f"> **Caveat.** {r['caveat']}")
            A("")
        A(f"Z1-initiated campaigns: {r['z1_initiated_campaigns']} "
          f"({r['z1_share_pct']}% of campaigns).")
        A("")
        rows = []
        for k, lab in (("neutral_live", "neutral (live)"),
                       ("drop_z1", "drop Z1-initiated"),
                       ("halfsize_z1", "half-size Z1-initiated")):
            d = r[k]
            rows.append([lab, d.get("campaigns"), d.get("sum_0x"), d.get("sum_1x"),
                         d.get("sum_2x"), d.get("expectancy_1x"),
                         f"[{d.get('ci95_lo')}, {d.get('ci95_hi')}]",
                         d.get("win_rate_pct"), d.get("strip_best_sum_1x")])
        A(md_table(["variant", "campaigns", "Σ 0×", "Σ 1×", "Σ 2×", "expectancy 1×",
                    "95% CI", "win %", "strip-best Σ 1×"], rows))
        A(f"\nFirst-order drop-Z1 Δ vs neutral (1×): "
          f"**{r['drop_z1_delta_1x_vs_neutral']}** cell-R.")
        A("")

    # RC-6
    for basis_key, label in (("clean", "scored-clean (primary)"),
                             ("scored20", "scored-20 (reference)")):
        r = res["rc6"][basis_key]
        A(f"## RC-6 — Attempt-sequence census — {label}")
        A("")
        if basis_key == "clean":
            A(f"> **Caveat.** {r['caveat']}")
            A("")
        A(f"Direction-runs: {r['n_direction_runs']}. Attempts-per-run distribution: "
          f"`{json.dumps(r['attempts_per_run_distribution'])}`")
        A("")
        A("**(b) By attempt number:**")
        A("")
        rows = []
        for b, d in r["by_attempt"].items():
            rows.append([b, d.get("campaigns"), d.get("sum_1x"),
                         d.get("expectancy_1x"),
                         f"[{d.get('ci95_lo')}, {d.get('ci95_hi')}]",
                         d.get("win_rate_pct")])
        A(md_table(["attempt", "campaigns", "Σ cell-R 1×", "expectancy 1×",
                    "95% CI", "win %"], rows))
        A("")
        A("**(c) In-cluster share of attempts 2+:**")
        A("")
        rows = []
        for k, d in r["in_cluster_share_attempts_2plus"].items():
            rows.append([k, d["attempts_2plus"], d["evaluable"], d["in_cluster"],
                         d["in_cluster_pct"]])
        A(md_table(["k×ATR", "attempts 2+", "evaluable", "in-cluster",
                    "in-cluster %"], rows))
        A("")
        A("**(d) Expectancy by attempt × cluster (k=1.0):**")
        A("")
        rows = []
        for b, d in r["expectancy_by_attempt_x_cluster_k1.0"].items():
            ic = d["in_cluster"]; oc = d["out_of_cluster"]
            rows.append([b, ic.get("campaigns"), ic.get("expectancy_1x"),
                         oc.get("campaigns"), oc.get("expectancy_1x")])
        A(md_table(["attempt", "in-cluster n", "in-cluster exp",
                    "out-cluster n", "out-cluster exp"], rows))
        A("")
        A("**(e) Counterfactual: Σ cell-R of in-cluster attempts 4+ "
          "(what a 3-strike rule would remove, first-order):**")
        A("")
        rows = []
        for k, d in r["counterfactual_incluster_attempts_4plus_sum_cell_r"].items():
            rows.append([k, d["campaigns"], d["sum_cell_r_1x"]])
        A(md_table(["k×ATR", "campaigns", "Σ cell-R 1× removed"], rows))
        A("")

    # predictions
    A("## Prediction scorecard (contract §7)")
    A("")
    A(md_table(["#", "prediction", "prior", "falsified if", "verdict"],
               [[p["id"], p["claim"], p["prior"], p["falsified_if"],
                 f"**{p['verdict']}**"] for p in res["predictions"]]))
    A("")
    for p in res["predictions"]:
        A(f"- **{p['id']} — {p['verdict']}.** Evidence: `{json.dumps(p['evidence'])}`")
    A("")
    return "\n".join(L)


# ------------------------------------------------------------------ fixtures
def compute_fixtures(book, tranche_cap_rejects):
    out = []

    def add(fid, name, expected, computed, tol=None):
        if tol is not None:
            match = abs(computed - expected) <= tol
        else:
            match = computed == expected
        out.append({"id": fid, "name": name, "expected": expected,
                    "computed": computed, "match": bool(match)})

    add("F1", "Scored campaigns", FIXTURES["F1_campaigns"], len(book.camps))
    add("F1", "Resolved tranches", FIXTURES["F1_tranches"], len(book.t))
    sum_1x = sum(x["realized_r"] for x in book.t)
    add("F2", "Σ realized_r scored-20 1×", FIXTURES["F2_sum_realized_r"],
        r4(sum_1x), TOL_TIGHT)
    add("F3", "Σ r_0x scored-20", FIXTURES["F3_sum_r_0x"],
        r4(sum(x["r_0x"] for x in book.t)), TOL_TIGHT)
    zec = [x for x in book.t if x["cell_id"] == CLEAN_EXCLUDE]
    add("F4", "ZEC_intraday tranches", FIXTURES["F4_zec_tranches"], len(zec))
    add("F4", "ZEC_intraday negative-one_r", FIXTURES["F4_zec_neg_one_r"],
        sum(1 for x in zec if x["one_r"] < 0))
    zec_net = sum(x["realized_r"] for x in zec)
    add("F5", "ZEC_intraday net 1×", FIXTURES["F5_zec_net_1x"], r4(zec_net), TOL_LOOSE)
    add("F6", "Scored-clean grid 1×", FIXTURES["F6_scored_clean_1x"],
        r4(sum_1x - zec_net), TOL_LOOSE)
    stops = [x for x in book.t if x["exit_reason"] in ("stop", "stop_gap")]
    ev = len(set((x["cell_id"], x["dir"], x["exit_ts_raw"]) for x in stops))
    add("F7", "Stop-exit events (cell,dir,ts collapse)", FIXTURES["F7_stop_events"], ev)
    add("F8", "tranche_cap (max_tranches) REJECT rows",
        FIXTURES["F8_tranche_cap_rejects"], tranche_cap_rejects)
    add("F9", "V-initiated campaigns", FIXTURES["F9_v_campaigns"], len(book.v_camps))
    resumption = sum(1 for x in stops
                     if x["cont_20"] is not None and x["cont_20"] >= 1.0)
    add("F10", "Per-tranche resumption (≥1R/20b, stop exits)",
        FIXTURES["F10_resumption"], resumption)
    return out


# ------------------------------------------------------------------ main
def build(journal_root, kline_root):
    cells, rows, evt_census, tranche_cap = load_scored(journal_root)
    book = Book(rows)

    # equity sequence per cell in journal file order (EXIT rows only)
    rows_by_cell_exit = defaultdict(list)
    for r in rows:
        if r["evt"] == "EXIT":
            rows_by_cell_exit[r["cell_id"]].append(r)

    fixtures = compute_fixtures(book, tranche_cap)
    fixture_verdict = "PASS" if all(f["match"] for f in fixtures) else "HALT"

    definitions = [
        "Open interval of a tranche = [fill_ts, exit_ts): fill row ts_open "
        "inclusive, EXIT row ts_open exclusive; exit_ts None => open at data end.",
        "concurrent_open_at_fill(A) = # siblings B in same (cell,campaign), B!=A, "
        "with B.fill_ts <= A.fill_ts and (A.fill_ts < B.exit_ts or B.fill_ts == "
        "A.fill_ts). Same-bar siblings count as concurrent.",
        "True add = ADD_FILL with concurrent >=1; re-entry = ADD_FILL with "
        "concurrent ==0; R1 = ENTRY_FILL non-V; V = ENTRY_FILL with is_v "
        "(EXIT.shadow.ladder_unthrottled_grade == 'V').",
        "max_concurrent(campaign) = peak simultaneously-open tranches via event "
        "sweep; SAME-BAR FILLS BEFORE SAME-BAR EXITS at equal ts_open.",
        "Direction-run = maximal same-cell same-direction campaign run in journal "
        "time order (by opener fill_ts); attempt number = 1-based index in run.",
        "Cluster: attempt in-cluster at k iff |opener.px_fill - "
        "attempt1.px_fill| <= k * atr_exec(attempt1 fill row).",
        "bps: mfe_bps = mfe_r*(|px_fill-stop|/px_fill)*1e4; cost_bps = "
        "cost_usd/(|qty|*px_fill)*1e4; realized_bps = "
        "(realized_r/size_r)*(|px_fill-stop|/px_fill)*1e4 (ENTRY-row prices, "
        "cumulative cost from EXIT).",
    ]

    res = {
        "meta": {
            "contract": "RC_Recompute_RC0_RC6_Builder_Contract.md",
            "phase": "RC Recompute RC-0..RC-6 — Tier A",
            "engine_version": sorted({r["engine_version"] for r in rows})[0],
            "engine_commit": "2f260e1",
            "config_id": "v12_anchor",
            "config_sha256": CONFIG_SHA[0],
            "journal_root": JOURNAL_REL[0],
            "primary_basis": "scored-clean (19 cells; ZECUSDT_intraday excluded, G-8)",
            "reference_basis": "scored-20",
            "n_cells": len(cells), "cells": cells,
            "seed": SEED, "n_boot": N_BOOT, "read_only": True,
            "definitions": definitions,
            "evt_census_scored": dict(sorted(evt_census.items())),
        },
        "fixtures": fixtures,
        "fixture_verdict": fixture_verdict,
    }
    if fixture_verdict != "PASS":
        res["halt"] = "Fixture MISMATCH — nothing produced downstream."
        return res, book

    # ---- bases ----
    tr20 = book.tr
    trC = clean(book.tr)
    trR20 = book.t
    trRC = clean(book.t)
    camps20 = book.camps
    campsC = clean_camps(book.camps)

    res["rc0"] = rc0(kline_root)
    res["rc1"] = {"clean": rc1(book, "scored-clean", campsC, trC),
                  "scored20": rc1(book, "scored-20", camps20, tr20)}
    res["rc2"] = rc2(book, cells, rows_by_cell_exit)
    res["halted_after_rc2"] = not res["rc2"]["certification"]["scored_clean_basis_valid"]

    if res["halted_after_rc2"]:
        res["predictions"] = []   # scored below anyway for P-RC2
        # still score P-RC2 minimally
        res["predictions"] = [{
            "id": "P-RC2", "prior": "80%",
            "claim": "No cell besides ZECUSDT_intraday crossed zero",
            "falsified_if": "any other zero-crossing",
            "evidence": {"other_crossers":
                         res["rc2"]["certification"]["other_cells_that_crossed_zero"]},
            "verdict": "FALSIFIED"}]
        return res, book

    res["rc3"] = {"clean": rc3(trRC, "scored-clean"),
                  "scored20": rc3(trR20, "scored-20")}
    res["rc4"] = {"clean": rc4(book, trRC, campsC, "scored-clean"),
                  "scored20": rc4(book, trR20, camps20, "scored-20")}
    res["rc5"] = {"clean": rc5(book, campsC, "scored-clean"),
                  "scored20": rc5(book, camps20, "scored-20")}
    res["rc6"] = {"clean": rc6(book, campsC, "scored-clean"),
                  "scored20": rc6(book, camps20, "scored-20")}

    res["predictions"] = score_predictions(
        res["rc1"]["clean"], res["rc2"], res["rc3"]["clean"],
        res["rc4"]["clean"], res["rc5"]["clean"], res["rc6"]["clean"])
    return res, book


CONFIG_SHA = [""]
JOURNAL_REL = [""]


def main():
    ap = argparse.ArgumentParser()
    here = Path(__file__).resolve().parents[1]
    ap.add_argument("--journal-root", type=Path,
                    default=here / "research_outputs" / "v3_anchor"
                    / "journal_pass1" / "scored")
    ap.add_argument("--kline-root", type=Path,
                    default=Path(os.environ.get("NAIAD_CACHE_DIR",
                                 Path(os.environ["LOCALAPPDATA"]) / "naiad"
                                 / "data_cache")) / "klines")
    ap.add_argument("--config", type=Path,
                    default=here / "configs" / "v12_anchor.yaml")
    ap.add_argument("--out-dir", type=Path, default=here)
    args = ap.parse_args()

    CONFIG_SHA[0] = hashlib.sha256(args.config.read_bytes()).hexdigest()
    jr = args.journal_root.resolve()
    JOURNAL_REL[0] = str(jr.relative_to(here) if str(jr).startswith(str(here))
                         else jr).replace("\\", "/")

    res, book = build(args.journal_root, args.kline_root)

    md = render_md(res)
    payload = res
    blob = json.dumps(payload, indent=1, sort_keys=True,
                      ensure_ascii=False, default=str).encode("utf-8")
    out_json = args.out_dir / "rc_recompute.json"
    out_md = args.out_dir / "RC_RECOMPUTE_RC0_RC6.md"
    out_json.write_bytes(blob)
    with open(out_md, "w", encoding="utf-8", newline="\n") as f:
        f.write(md)

    j_sha = hashlib.sha256(blob).hexdigest()
    m_sha = hashlib.sha256(out_md.read_bytes()).hexdigest()
    combo = hashlib.sha256((j_sha + m_sha).encode()).hexdigest()
    print(f"fixtures: {res['fixture_verdict']} "
          f"({sum(1 for f in res['fixtures'] if f['match'])}/{len(res['fixtures'])})")
    if res["fixture_verdict"] != "PASS":
        for f in res["fixtures"]:
            if not f["match"]:
                print(f"  MISMATCH {f['id']} {f['name']}: "
                      f"expected {f['expected']} computed {f['computed']}")
        print(f"sha256(rc_recompute.json)      = {j_sha}")
        return 1
    for p in res.get("predictions", []):
        print(f"  {p['id']}: {p['verdict']}")
    print(f"sha256(rc_recompute.json)         = {j_sha}")
    print(f"sha256(RC_RECOMPUTE_RC0_RC6.md)   = {m_sha}")
    print(f"OUTPUT_HASH                       = {combo}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
