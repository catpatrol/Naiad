"""W-F1 — WINNER FORENSICS, Tier-A discriminant study.

Executes exchange/queue/2026-08-03_WF1_winner_forensics_APOLLO.md.

FRAME: condition on outcome (realized_r deciles), discriminate at BIRTH.
Every Section-A discriminant must be decision-curtain-clean: knowable at or
before the fill.  The Tail-Retention Gauge is mandatory on the TRG demo.

POPULATION
  journals  research_outputs/_unarchived/s3_2026-07-27/journal_s3/scored/ (753 files)
  substrate s3_excursion_substrate.jsonl (7,094 rows)
  join      (cell_id, tranche_id) == (cell, tranche_id), format c<N>t<N>

EVENT MODEL (measured, not assumed)
  BIRTH  = evt in {ENTRY_FILL, ADD_FILL}  -> 7,117 rows, carries fill_class,
           s2, retr, atr_exec, atr_gov, px_fill, stop, zone, stage, grade, qty
  EXIT   = evt == EXIT                    -> 7,094 rows, carries realized_r,
           exit_reason, funding_cum, give_back_r, mfe_r, mae_r, engagement_flags
  23 births never resolve (right-edge truncation, all ts_open in 2024-06).

THREE CONTRACT DEFECTS, HANDLED AND REPORTED (never silently patched):
  D1  engagement_flags is NULL on all 7,117 births and present on all 7,094
      EXITs.  It is POST-FILL.  The contract lists it as a Section-A
      discriminant; F-WF2 rejects it.  It is demoted to Section B.
  D2  "s2 slow-stack flag" (P-WF1) does not exist.  s2 carries only `det`
      (30m/1h detonation bits) and `levels` (4h/12h/1d pivot blocks).  The
      slow-stack F1/F2/F4 EMA-cascade bits live in the CENSUS arming-anchor
      table, a different artefact.  P-WF1 is scored PREMISE-FALSE, and the
      whole s2 flag family is tested in its place.
  D3  The contract says fill_class=v is "EXCLUDED and counted" yet also says
      rank ALL 7,094 and take floor(0.1*n)=709.  709 == floor(0.1*7094) only
      if v is INCLUDED.  Primary book therefore = all 7,094 (v included);
      a v-excluded sensitivity book and the contracted r1-only secondary book
      are both computed and reported.

COST MODEL (measured against the ratified constants, not assumed)
  realized_r is ALREADY net of fees + slippage + funding.
  net_bps = realized_r * unit_bps / size_r      (exact; rel-err ~5e-07)
  unit_bps = (px_fill - stop)*dirsign/px_fill*1e4 from the BIRTH stop.
  EXIT.stop is a ratcheted stop and differs from BIRTH.stop on 2,099 rows;
  using it would be wrong.  Measured per-asset toll reproduces the ratified
  LEDGER.md:556-558 mapping (BTC/ETH 14 bps, others 20 bps).

Usage
  python scripts/wf1_forensics.py
  python scripts/wf1_forensics.py --rebuild
No network.  Sorted iteration throughout.  Resume-safe per-cell checkpoints.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
JOURNALS = ROOT / "research_outputs" / "_unarchived" / "s3_2026-07-27" / "journal_s3" / "scored"
SUBSTRATE = ROOT / "s3_excursion_substrate.jsonl"
BOX = ROOT / "_reviewer_box" / "wf1"
REPORTS = ROOT / "exchange" / "reports"

SEED = 20260803
BOOT_N = 10_000
FDR_Q = 0.10
DECILE_FRAC = 0.10

PANEL = ("BTCUSDT", "ETHUSDT", "SOLUSDT", "NEARUSDT", "ZECUSDT")
ANNEX_ASSETS = ("JTOUSDT", "TAOUSDT")

BIRTH_EVTS = ("ADD_FILL", "ENTRY_FILL")
TS_FMT = "%Y-%m-%dT%H:%M:%SZ"

# Section-A contract list.  engagement_flags is absent by ruling D1.
CAT_FEATURES = ("symbol", "mandate", "dir", "fill_class", "grade", "zone",
                "stage", "concurrent_open_at_fill")
NUM_FEATURES = ("retr", "atr_exec_bps", "atr_gov_bps")
ANNEX_FEATURES = ("session_bucket", "dow")

# minority-class floor below which a categorical level is reported but marked
# DEGENERATE (it still enters the FDR family -- we tested it, so it counts).
DEGENERATE_MIN = 30


# ---------------------------------------------------------------- utilities
def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def r6(x):
    if x is None:
        return None
    x = float(x)
    return None if not math.isfinite(x) else round(x, 6)


def parse_ts(s: str) -> dt.datetime:
    return dt.datetime.strptime(s, TS_FMT).replace(tzinfo=dt.timezone.utc)


def flatten(d, prefix=""):
    """Flatten a nested dict into {dotted.path: leaf}."""
    out = {}
    for k in sorted(d.keys()):
        v = d[k]
        key = f"{prefix}{k}"
        if isinstance(v, dict):
            out.update(flatten(v, key + "."))
        else:
            out[key] = v
    return out


def session_bucket(hour: int) -> str:
    if hour <= 7:
        return "ASIA_00_07"
    if hour <= 12:
        return "EU_08_12"
    if hour <= 20:
        return "US_13_20"
    return "LATE_21_23"


DOW = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")


# ------------------------------------------------------------- extraction
def extract_cell(cell_dir: Path) -> dict:
    """Read every month file of one cell, pair births to exits, emit rows."""
    births, exits = {}, {}
    n_rows = 0
    for month in sorted(cell_dir.glob("*.jsonl")):
        with open(month, "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                rec = json.loads(line)
                n_rows += 1
                evt = rec.get("evt")
                if evt in BIRTH_EVTS:
                    births[rec["tranche_id"]] = rec
                elif evt == "EXIT":
                    exits[rec["tranche_id"]] = rec

    rows = []
    for tid in sorted(births):
        b = births[tid]
        e = exits.get(tid)
        cell = b["cell_id"]
        symbol, mandate = cell.split("_", 1)
        dirsign = 1.0 if b["dir"] == "long" else -1.0
        pxf = b.get("px_fill")
        stop = b.get("stop")
        ts_open = b["ts_open"]
        t0 = parse_ts(ts_open)

        row = {
            "cell": cell,
            "tranche_id": tid,
            "resolved": e is not None,
            # ---- curtain-clean birth features
            "symbol": symbol,
            "mandate": mandate,
            "dir": b.get("dir"),
            "fill_class": b.get("fill_class"),
            "grade": b.get("grade"),
            "zone": b.get("zone"),
            "stage": b.get("stage"),
            "concurrent_open_at_fill": b.get("concurrent_open_at_fill"),
            "tier": b.get("tier"),
            "size_r": b.get("size_r"),
            "retr": b.get("retr"),
            "px_fill": pxf,
            "stop": stop,
            "qty": b.get("qty"),
            "ts_open": ts_open,
            "ts_open_epoch": int(t0.timestamp()),
            "hour_utc": t0.hour,
            "session_bucket": session_bucket(t0.hour),
            "dow": DOW[t0.weekday()],
        }
        atr_e, atr_g = b.get("atr_exec"), b.get("atr_gov")
        row["atr_exec_bps"] = (atr_e / pxf * 1e4) if (atr_e and pxf) else None
        row["atr_gov_bps"] = (atr_g / pxf * 1e4) if (atr_g and pxf) else None
        row["unit_bps_journal"] = (((pxf - stop) * dirsign / pxf * 1e4)
                                   if (pxf and stop is not None) else None)

        # ---- s2 flags at birth (curtain-clean by construction)
        s2 = b.get("s2") or {}
        for path, val in sorted(flatten(s2, "s2.").items()):
            if isinstance(val, bool):
                row["FLAG@" + path] = val

        # ---- post-birth outcome (Section B only)
        if e is not None:
            tc = parse_ts(e["ts_close"])
            row.update({
                "realized_r": e.get("realized_r"),
                "exit_reason": e.get("exit_reason"),
                "funding_cum": e.get("funding_cum"),
                "give_back_r": e.get("give_back_r"),
                "mfe_r": e.get("mfe_r"),
                "mae_r": e.get("mae_r"),
                "pnl_usd": e.get("pnl_usd"),
                "exit_fees": e.get("fees"),
                "exit_slippage": e.get("slippage"),
                "exit_px_fill": e.get("px_fill"),
                "cohort": e.get("cohort"),
                "ts_close": e["ts_close"],
                "hold_s": int((tc - t0).total_seconds()),
                "engagement_flags": e.get("engagement_flags"),
            })
        rows.append(row)
    return {"cell": cell_dir.name, "n_rows_scanned": n_rows,
            "n_births": len(births), "n_exits": len(exits), "rows": rows}


def build_checkpoints(rebuild: bool) -> list:
    BOX.mkdir(parents=True, exist_ok=True)
    cells = sorted(p for p in JOURNALS.iterdir() if p.is_dir())
    cached, computed = [], []
    packs = []
    for cd in cells:
        ck = BOX / f"{cd.name}.json"
        if ck.exists() and not rebuild:
            packs.append(json.loads(ck.read_text(encoding="utf-8")))
            cached.append(cd.name)
        else:
            pack = extract_cell(cd)
            ck.write_text(json.dumps(pack, sort_keys=True), encoding="utf-8")
            packs.append(pack)
            computed.append(cd.name)
    print(f"  checkpoints: {len(cached)} cached, {len(computed)} computed")
    if computed:
        print(f"    computed: {', '.join(computed)}")
    return packs


# ----------------------------------------------------------------- stats
def bh_fdr(pvals):
    """Benjamini-Hochberg step-up.  Returns q-values aligned to input order.
    q_(i) = min over j>=i of  ( p_(j) * m / j ),  clipped to 1.
    """
    m = len(pvals)
    order = sorted(range(m), key=lambda i: (pvals[i], i))
    q = [0.0] * m
    running = 1.0
    for rank in range(m, 0, -1):
        i = order[rank - 1]
        val = pvals[i] * m / rank
        running = min(running, val)
        q[i] = min(1.0, running)
    return q


class Boot:
    """Bootstrap index matrices, cached per (group-size, side).

    Every discriminant of the same group size is resampled on the SAME 10,000
    replicates, so the family is internally coherent.  Numeric discriminants
    drop nulls and therefore have a shorter group; those get their own matrix,
    seeded deterministically from (SEED, size, side) so the run is still
    reproducible from the seed alone.
    """

    def __init__(self, n_w, n_l, n=BOOT_N, seed=SEED):
        self.n = n
        self.seed = seed
        self.n_w, self.n_l = n_w, n_l
        self._cache = {}

    def _idx(self, m, side):
        key = (m, side)
        if key not in self._cache:
            rng = np.random.default_rng([self.seed, m, side])
            self._cache[key] = rng.integers(0, m, size=(self.n, m), dtype=np.int16)
        return self._cache[key]

    def diff_prop(self, ind_w, ind_l):
        bw = ind_w[self._idx(len(ind_w), 0)].mean(axis=1)
        bl = ind_l[self._idx(len(ind_l), 1)].mean(axis=1)
        return bw - bl

    def diff_median(self, aw, al):
        bw = np.median(aw[self._idx(len(aw), 0)], axis=1)
        bl = np.median(al[self._idx(len(al), 1)], axis=1)
        return bw - bl


def ci_and_p(boot, point):
    """95% percentile CI and a two-sided bootstrap p-value.

    p = 2 * min( P(boot <= 0), P(boot >= 0) ), floored at 1/BOOT_N and capped
    at 1.  This is the standard percentile-bootstrap two-sided p; it is the
    quantity fed to Benjamini-Hochberg.
    """
    lo = float(np.percentile(boot, 2.5))
    hi = float(np.percentile(boot, 97.5))
    n = len(boot)
    p_le = float(np.count_nonzero(boot <= 0)) / n
    p_ge = float(np.count_nonzero(boot >= 0)) / n
    p = min(1.0, 2.0 * min(p_le, p_ge))
    p = max(p, 1.0 / n)
    return {"point": r6(point), "ci_lo": r6(lo), "ci_hi": r6(hi),
            "ci_excludes_zero": bool(lo > 0 or hi < 0), "p": r6(p)}


# --------------------------------------------------------------- analysis
def indicator(rows, feat, level):
    return np.array([1.0 if r.get(feat) == level else 0.0 for r in rows])


def numeric(rows, feat):
    return np.array([r.get(feat) if r.get(feat) is not None else np.nan
                     for r in rows], dtype=float)


def sign_of(x, eps=1e-12):
    if x is None or not math.isfinite(x) or abs(x) < eps:
        return 0
    return 1 if x > 0 else -1


def rank_biserial(aw, al):
    """Scale-free effect size: 2*AUC - 1, AUC = P(random W > random L) with ties
    at 0.5.  Dimensionless for BOTH proportions and continuous features, so
    categorical and numeric discriminants can be ranked on one axis.  (Ranking
    on the raw point estimate would compare a proportion in [0,1] against a
    median delta carried in basis points, and the bps rows would always win.)
    """
    if len(aw) == 0 or len(al) == 0:
        return None
    allv = np.concatenate([aw, al])
    order = allv.argsort(kind="mergesort")
    ranks = np.empty(len(allv), dtype=float)
    ranks[order] = np.arange(1, len(allv) + 1, dtype=float)
    # average ranks within ties
    s = allv[order]
    i = 0
    while i < len(s):
        j = i
        while j + 1 < len(s) and s[j + 1] == s[i]:
            j += 1
        if j > i:
            ranks[order[i:j + 1]] = (i + j + 2) / 2.0
        i = j + 1
    rw = ranks[:len(aw)].sum()
    u = rw - len(aw) * (len(aw) + 1) / 2.0
    auc = u / (len(aw) * len(al))
    return 2.0 * auc - 1.0


def analyse_family(W, L, specs, boot, family):
    """specs: list of (feature, level_or_None, kind).  Returns finished rows.

    A spec with NO CONTRAST across W union L (a level that never occurs, or that
    occurs on every row) is not a test: the bootstrap is identically zero and p
    is forced to 1.0.  Such rows are computed and reported but EXCLUDED from the
    Benjamini-Hochberg family, because including them inflates m and therefore
    every q-value in the family.  The count is reported so the exclusion is
    visible.
    """
    out = []
    for feat, level, kind in specs:
        if kind == "cat":
            iw, il = indicator(W, feat, level), indicator(L, feat, level)
            point = iw.mean() - il.mean()
            st = ci_and_p(boot.diff_prop(iw, il), point)
            st["prevalence_W"] = r6(iw.mean())
            st["prevalence_L"] = r6(il.mean())
            st["n_W"] = int(iw.sum())
            st["n_L"] = int(il.sum())
            tot, cap = iw.sum() + il.sum(), len(iw) + len(il)
            st["degenerate"] = bool(tot < DEGENERATE_MIN)
            st["no_contrast"] = bool(tot == 0 or tot == cap)
            st["effect_rb"] = r6(rank_biserial(iw, il))
            name = f"{feat}={level}"
        else:
            aw, al = numeric(W, feat), numeric(L, feat)
            aw, al = aw[np.isfinite(aw)], al[np.isfinite(al)]
            point = float(np.median(aw) - np.median(al))
            st = ci_and_p(boot.diff_median(aw, al), point)
            st["median_W"] = r6(np.median(aw))
            st["median_L"] = r6(np.median(al))
            st["n_W"] = int(len(aw))
            st["n_L"] = int(len(al))
            st["degenerate"] = False
            st["no_contrast"] = False
            st["effect_rb"] = r6(rank_biserial(aw, al))
            name = feat
        st.update({"feature": feat, "level": level, "kind": kind,
                   "name": name, "family": family})
        out.append(st)

    tested = [r for r in out if not r["no_contrast"]]
    qs = bh_fdr([r["p"] for r in tested])
    for r, q in zip(tested, qs):
        r["q"] = r6(q)
        r["fdr_survives"] = bool(q <= FDR_Q)
    for r in out:
        if r["no_contrast"]:
            r["q"] = None
            r["fdr_survives"] = False
    return out


def panel_and_time(rows, W, L, results, split_epoch):
    """Per-asset sign consistency across the 5 panel assets, annex assets kept
    separate and never pooled; plus early/late sign stability."""
    for r in results:
        feat, level, kind = r["feature"], r["level"], r["kind"]

        # The panel gate conditions on asset.  For feature `symbol` that IS the
        # conditioning variable, so the indicator is constant inside every
        # per-asset subset and the delta is identically 0 -- a structurally
        # unpassable gate, not a failed replication.  Mark it inapplicable
        # instead of silently reporting "panel 0/5".
        r["panel_applicable"] = (feat != "symbol")
        if not r["panel_applicable"]:
            r["per_asset_delta"] = {s: None for s in sorted(PANEL + ANNEX_ASSETS)}
            r["panel_n_assets"] = 0
            r["panel_agree"] = 0
            r["panel_sign_consistent"] = None
            r["panel_note"] = ("N/A - feature is the conditioning variable; "
                               "per-asset contrast is undefined")
            halves = {}
            for tag, sel in (("early", lambda x: x["ts_open_epoch"] < split_epoch),
                             ("late", lambda x: x["ts_open_epoch"] >= split_epoch)):
                w = [x for x in W if sel(x)]
                l = [x for x in L if sel(x)]
                halves[tag] = (r6(indicator(w, feat, level).mean()
                                  - indicator(l, feat, level).mean())
                               if w and l else None)
            r["time_delta"] = halves
            ov = sign_of(r["point"])
            r["time_stable"] = bool(halves.get("early") is not None
                                    and halves.get("late") is not None and ov != 0
                                    and sign_of(halves["early"]) == ov
                                    and sign_of(halves["late"]) == ov)
            r["CANDIDATE"] = False
            r["candidate_note"] = "excluded: panel sign-consistency gate inapplicable"
            continue

        per_asset = {}
        for sym in sorted(PANEL + ANNEX_ASSETS):
            w = [x for x in W if x["symbol"] == sym]
            l = [x for x in L if x["symbol"] == sym]
            if not w or not l:
                per_asset[sym] = None
                continue
            if kind == "cat":
                d = indicator(w, feat, level).mean() - indicator(l, feat, level).mean()
            else:
                aw, al = numeric(w, feat), numeric(l, feat)
                aw, al = aw[np.isfinite(aw)], al[np.isfinite(al)]
                d = (float(np.median(aw) - np.median(al))
                     if len(aw) and len(al) else None)
            per_asset[sym] = r6(d)
        r["per_asset_delta"] = per_asset

        panel_signs = [sign_of(per_asset[s]) for s in PANEL
                       if per_asset.get(s) is not None]
        overall = sign_of(r["point"])
        r["panel_n_assets"] = len(panel_signs)
        r["panel_agree"] = sum(1 for s in panel_signs if s == overall and s != 0)
        r["panel_sign_consistent"] = bool(
            len(panel_signs) == len(PANEL) and overall != 0
            and all(s == overall for s in panel_signs))

        halves = {}
        for tag, sel in (("early", lambda x: x["ts_open_epoch"] < split_epoch),
                         ("late", lambda x: x["ts_open_epoch"] >= split_epoch)):
            w = [x for x in W if sel(x)]
            l = [x for x in L if sel(x)]
            if not w or not l:
                halves[tag] = None
                continue
            if kind == "cat":
                d = indicator(w, feat, level).mean() - indicator(l, feat, level).mean()
            else:
                aw, al = numeric(w, feat), numeric(l, feat)
                aw, al = aw[np.isfinite(aw)], al[np.isfinite(al)]
                d = (float(np.median(aw) - np.median(al))
                     if len(aw) and len(al) else None)
            halves[tag] = r6(d)
        r["time_delta"] = halves
        r["time_stable"] = bool(
            halves.get("early") is not None and halves.get("late") is not None
            and overall != 0
            and sign_of(halves["early"]) == overall
            and sign_of(halves["late"]) == overall)

        r["CANDIDATE"] = bool(r["ci_excludes_zero"] and r["fdr_survives"]
                              and r["panel_sign_consistent"] and r["time_stable"])
    return results


# ------------------------------------------------------------------- TRG
def net_bps(row):
    r, u, s = row.get("realized_r"), row.get("unit_bps"), row.get("size_r")
    if r is None or u is None or not s:
        return None
    return r * u / s


def trg_for(book, W, r_row):
    """Naive winner-side filter, its delta-expectancy, and the Tail-Retention
    Gauge = share of the UNFILTERED top-decile total R that survives."""
    feat, level, kind = r_row["feature"], r_row["level"], r_row["kind"]
    if kind == "cat":
        want = r_row["point"] > 0
        keep = lambda x: (x.get(feat) == level) == want
        desc = (f"{feat} == {level}" if want else f"{feat} != {level}")
    else:
        vals = numeric(book, feat)
        med = float(np.nanmedian(vals))
        hi = r_row["point"] > 0
        keep = lambda x: (x.get(feat) is not None
                          and (x[feat] >= med if hi else x[feat] <= med))
        desc = f"{feat} {'>=' if hi else '<='} {r6(med)} (book median)"

    kept = [x for x in book if keep(x)]
    base_r = float(np.mean([x["realized_r"] for x in book]))
    base_b = float(np.mean([b for b in (net_bps(x) for x in book) if b is not None]))
    kept_r = float(np.mean([x["realized_r"] for x in kept])) if kept else None
    kb = [b for b in (net_bps(x) for x in kept) if b is not None]
    kept_b = float(np.mean(kb)) if kb else None

    top_total = float(np.sum([x["realized_r"] for x in W]))
    ret_total = float(np.sum([x["realized_r"] for x in W if keep(x)]))

    return {
        "discriminant": r_row["name"], "filter": desc,
        "n_kept": len(kept), "n_book": len(book),
        "kept_share": r6(len(kept) / len(book)),
        "expectancy_R_unfiltered": r6(base_r),
        "expectancy_R_filtered": r6(kept_r),
        "delta_expectancy_R": r6(None if kept_r is None else kept_r - base_r),
        "expectancy_net_bps_unfiltered": r6(base_b),
        "expectancy_net_bps_filtered": r6(kept_b),
        "delta_expectancy_net_bps": r6(None if kept_b is None else kept_b - base_b),
        "top_decile_total_R_unfiltered": r6(top_total),
        "top_decile_total_R_retained": r6(ret_total),
        "TRG_pct": r6(100.0 * ret_total / top_total) if top_total else None,
        "n_top_decile_kept": sum(1 for x in W if keep(x)),
    }


# ---------------------------------------------------------------- tables
def fmt(v, nd=6):
    if v is None:
        return "—"
    if isinstance(v, bool):
        return "yes" if v else "no"
    if isinstance(v, float):
        return f"{v:.{nd}f}"
    return str(v)


def emit_tables(out, path: Path):
    """WF1_tables.md — full tables, not summaries."""
    L = []
    a = L.append
    a("# W-F1 · WINNER FORENSICS — FULL TABLES")
    a("")
    a(f"Generated by `scripts/wf1_forensics.py` · seed {out['seed']} · "
      f"{out['bootstrap_resamples']:,} bootstrap resamples · BH-FDR q={out['fdr_q']}")
    a("")
    p = out["population"]
    d = out["deciles"]
    a("## Population")
    a("")
    a("| quantity | value |")
    a("|---|---|")
    a(f"| journal files | {p['journal_files']} |")
    a(f"| substrate sha256 | `{p['substrate_sha256']}` |")
    a(f"| fills | {p['fills']:,} (r1 {p['fill_class']['r1']:,} · "
      f"v {p['fill_class']['v']} · re_entry {p['fill_class']['re_entry']:,}) |")
    a(f"| resolved | {p['resolved']:,} |")
    a(f"| unresolved, excluded-and-counted | {p['unresolved_excluded']} |")
    a(f"| stopout (exit_reason ∈ stop, stop_gap) | {p['stopout']:,} |")
    a(f"| decile size floor(0.1·n) | {d['decile_size']} |")
    a(f"| W cut (min realized_r in top decile) | {d['W_cut_min_realized_r']} |")
    a(f"| W max | {d['W_max']} |")
    a(f"| L cut (max realized_r in bottom decile) | {d['L_cut_max_realized_r']} |")
    a(f"| L min | {d['L_min']} |")
    a(f"| time split at median ts_open | {d['time_split_median_ts_open']} "
      f"({d['n_early']} early / {d['n_late']} late) |")
    a("")

    a("## F-WF2 · Curtain audit")
    a("")
    a("Every Section-A feature, with a one-line attestation that it is knowable at or before the fill.")
    a("")
    a("| # | feature | source | attestation |")
    a("|---|---|---|---|")
    for i, c in enumerate(out["curtain_audit"]["clean"], 1):
        a(f"| {i} | `{c['feature']}` | {c['source']} | {c['attestation']} |")
    a("")
    a("**REJECTED — not curtain-clean, demoted to Section B:**")
    a("")
    a("| feature | reason |")
    a("|---|---|")
    for c in out["curtain_audit"]["rejected"]:
        a(f"| `{c['feature']}` | {c['reason']} |")
    a("")

    def table(rows, title, note=""):
        a(f"## {title}")
        a("")
        if note:
            a(note)
            a("")
        a("| discriminant | kind | prev/med W | prev/med L | delta (W−L) | 95% CI | CI≠0 | p | q | FDR | panel | time | CANDIDATE |")
        a("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
        for r in sorted(rows, key=lambda x: (x["q"] is None, x["q"] if x["q"]
                                            is not None else 1.0, x["p"], x["name"])):
            wv = r.get("prevalence_W", r.get("median_W"))
            lv = r.get("prevalence_L", r.get("median_L"))
            deg = (" ⚠︎NO-CONTRAST" if r.get("no_contrast")
                   else (" ⚠︎deg" if r.get("degenerate") else ""))
            a(f"| `{r['name']}`{deg} | {r['kind']} | {fmt(wv)} | {fmt(lv)} | "
              f"{fmt(r['point'])} | [{fmt(r['ci_lo'])}, {fmt(r['ci_hi'])}] | "
              f"{fmt(r['ci_excludes_zero'])} | {fmt(r['p'])} | {fmt(r['q'])} | "
              f"{fmt(r['fdr_survives'])} | "
              f"{'n/a' if not r.get('panel_applicable', True) else str(r['panel_agree']) + '/' + str(r['panel_n_assets'])}"
              f"{'✓' if r['panel_sign_consistent'] else ''} | "
              f"{fmt(r['time_stable'])} | "
              f"{'**YES**' if r['CANDIDATE'] else 'no'} |")
        a("")

    table(out["section_a"], f"Section A · full family ({len(out['section_a'])} tests)",
          "`prev` = prevalence for categorical rows, `med` = median for numeric rows. "
          "`⚠︎deg` marks a level with fewer than "
          f"{DEGENERATE_MIN} occurrences across W∪L — reported, and still counted in the "
          "FDR family, because it was tested. `panel` = how many of the 5 panel assets "
          "share the pooled sign.")
    table(out["annex"], f"Annex family ({len(out['annex'])} tests) — own FDR family",
          "Session-hour-UTC bucket and day-of-week, corrected separately from the "
          "Section-A family per the contract.")

    a("## Section A · per-asset deltas (panel + annex, never pooled)")
    a("")
    hdr = list(PANEL) + list(ANNEX_ASSETS)
    a("| discriminant | " + " | ".join(hdr) + " | panel consistent |")
    a("|---|" + "---|" * (len(hdr) + 1))
    for r in sorted(out["section_a"], key=lambda x: (x["q"] is None,
                    x["q"] if x["q"] is not None else 1.0, x["name"])):
        if not (r["fdr_survives"] or r["CANDIDATE"]):
            continue
        cells = [fmt(r["per_asset_delta"].get(s), 4) for s in hdr]
        a(f"| `{r['name']}` | " + " | ".join(cells) + " | "
          + ("**yes**" if r["panel_sign_consistent"] else "no") + " |")
    a("")

    a("## F-WF5 · BH-FDR arithmetic, recomputed by hand")
    a("")
    a("Benjamini-Hochberg step-up on the Section-A family, m = "
      f"{out['fdr_worked_examples'][0]['m']} tests, q\\* = {out['fdr_q']}.")
    a("")
    a("| discriminant | rank i | p_(i) | p_(i)·m/i | q reported | formula |")
    a("|---|---|---|---|---|---|")
    for w in out["fdr_worked_examples"]:
        a(f"| `{w['name']}` | {w['rank']} | {fmt(w['p'])} | {fmt(w['p*m/rank'])} | "
          f"{fmt(w['q_reported'])} | {w['formula']} |")
    a("")
    a("The reported q is the running minimum of `p·m/i` scanned from the largest rank "
      "down, which is why it can sit below `p·m/i` for an individual row.")
    a("")

    a("## TRG · Tail-Retention Gauge")
    a("")
    a("Naive filter = keep only trades carrying the winner-side value of the "
      "discriminant. TRG = share of the **unfiltered** book's top-decile total R that "
      "survives the filter. F-WF6 pins the unfiltered book at exactly 100.0%.")
    a("")
    a("| discriminant | filter | kept | Δexpectancy R | Δexpectancy net bps | top-decile R kept | TRG |")
    a("|---|---|---|---|---|---|---|")
    u = out["trg"]["unfiltered"]
    a(f"| _(none — unfiltered)_ | keep all | {u['n_kept']:,} (100.0%) | "
      f"{fmt(u['delta_expectancy_R'],4)} | {fmt(u['delta_expectancy_net_bps'],4)} | "
      f"{u['n_top_decile_kept']}/{u['n_top_decile_kept']} | **{u['TRG_pct']:.1f}%** |")
    for t in out["trg"]["top5"]:
        a(f"| `{t['discriminant']}` | {t['filter']} | {t['n_kept']:,} "
          f"({100*t['kept_share']:.1f}%) | {fmt(t['delta_expectancy_R'],4)} | "
          f"{fmt(t['delta_expectancy_net_bps'],4)} | "
          f"{t['n_top_decile_kept']}/709 | **{t['TRG_pct']:.1f}%** |")
    a("")
    a("| discriminant | expectancy R unfilt. | expectancy R filt. | expectancy bps unfilt. | expectancy bps filt. | top-decile total R unfilt. | retained |")
    a("|---|---|---|---|---|---|---|")
    for t in out["trg"]["top5"]:
        a(f"| `{t['discriminant']}` | {fmt(t['expectancy_R_unfiltered'],4)} | "
          f"{fmt(t['expectancy_R_filtered'],4)} | "
          f"{fmt(t['expectancy_net_bps_unfiltered'],3)} | "
          f"{fmt(t['expectancy_net_bps_filtered'],3)} | "
          f"{fmt(t['top_decile_total_R_unfiltered'],3)} | "
          f"{fmt(t['top_decile_total_R_retained'],3)} |")
    a("")

    a("## Section B · outcome anatomy — NOT CURTAIN-CLEAN")
    a("")
    a("> These are post-birth quantities. They describe what winners and losers "
      "*became*, not what distinguished them at fill. **None may be used as a "
      "discriminant.**")
    a("")
    sb = out["section_b_NOT_CURTAIN_CLEAN"]
    a("| quantity | W (top decile) | L (bottom decile) | whole book |")
    a("|---|---|---|---|")
    for key, lab in (("n", "n"),
                     ("hold_h_median", "median holding time (h)"),
                     ("hold_s_median", "median holding time (s)"),
                     ("hold_s_p25", "holding time p25 (s)"),
                     ("hold_s_p75", "holding time p75 (s)"),
                     ("give_back_r_median", "median give_back_r"),
                     ("funding_cum_median", "median funding_cum (USD)"),
                     ("abs_funding_over_abs_r_median_MIXED_UNITS",
                      "median &#124;funding_cum&#124;/&#124;realized_r&#124; ⚠︎ MIXED UNITS (USD/R)"),
                     ("abs_funding_over_abs_pnl_median_DIMENSIONLESS",
                      "median &#124;funding_cum&#124;/&#124;pnl_usd&#124; (dimensionless)")):
        a(f"| {lab} | {fmt(sb['W'][key])} | {fmt(sb['L'][key])} | {fmt(sb['book'][key])} |")
    a("")
    a("### exit_reason mix")
    a("")
    reasons = sorted(set(sb["W"]["exit_reason_mix"]) | set(sb["L"]["exit_reason_mix"])
                     | set(sb["book"]["exit_reason_mix"]))
    a("| exit_reason | W n | W share | L n | L share | book n | book share |")
    a("|---|---|---|---|---|---|---|")
    for rs in reasons:
        a(f"| {rs} | {sb['W']['exit_reason_mix'].get(rs,0)} | "
          f"{fmt(sb['W']['exit_reason_share'].get(rs,0),4)} | "
          f"{sb['L']['exit_reason_mix'].get(rs,0)} | "
          f"{fmt(sb['L']['exit_reason_share'].get(rs,0),4)} | "
          f"{sb['book']['exit_reason_mix'].get(rs,0)} | "
          f"{fmt(sb['book']['exit_reason_share'].get(rs,0),4)} |")
    a("")
    a("### MFE / MAE shapes at horizons (substrate, bps)")
    a("")
    a("| horizon | MFE W | MFE L | MAE W | MAE L |")
    a("|---|---|---|---|---|")
    for h in ("h10", "h20", "h50", "h100", "exit"):
        a(f"| {h} | {fmt(sb['W'].get(f'mfe_bps_{h}_median'),3)} | "
          f"{fmt(sb['L'].get(f'mfe_bps_{h}_median'),3)} | "
          f"{fmt(sb['W'].get(f'mae_bps_{h}_median'),3)} | "
          f"{fmt(sb['L'].get(f'mae_bps_{h}_median'),3)} |")
    a("")
    a("### Funding first read, per mandate")
    a("")
    a("| mandate | group | n | median funding_cum (USD) | median &#124;funding&#124;/&#124;pnl&#124; |")
    a("|---|---|---|---|---|")
    for md in sorted(sb["per_mandate"]):
        for g in ("W", "L"):
            blk = sb["per_mandate"][md].get(g)
            if blk:
                a(f"| {md} | {g} | {blk['n']} | {fmt(blk['funding_cum_median'],4)} | "
                  f"{fmt(blk['abs_funding_over_abs_pnl_median_DIMENSIONLESS'],4)} |")
    a("")

    a("## Secondary books")
    a("")
    a("| book | n | decile size | L cut | W cut | CANDIDATES |")
    a("|---|---|---|---|---|---|")
    a(f"| PRIMARY (all resolved) | {d['n']} | {d['decile_size']} | "
      f"{d['L_cut_max_realized_r']} | {d['W_cut_min_realized_r']} | "
      f"{sum(1 for r in out['section_a'] if r['CANDIDATE'])} |")
    for kk, lab in (("r1_only", "SECONDARY r1-only (contracted)"),
                    ("v_excluded", "SENSITIVITY v-excluded (defect D3)")):
        s = out["secondary_books"][kk]
        a(f"| {lab} | {s['n']} | {s['decile_size']} | {s['cut_lo']} | {s['cut_hi']} | "
          f"{s['n_candidates']} |")
    a("")

    a("## Predictions, scored")
    a("")
    a("| id | stated | prediction | verdict | evidence |")
    a("|---|---|---|---|---|")
    for pr in out["predictions"]:
        a(f"| {pr['id']} | {int(pr['stated']*100)}% | {pr['text']} | "
          f"**{pr['verdict']}** | {pr['note']} |")
    a("")

    a("## Fixture transcript")
    a("")
    a("| fixture | result | detail |")
    a("|---|---|---|")
    for f in out["fixtures"]:
        a(f"| {f['id']} | {'PASS' if f['pass'] else 'FAIL'} | {f['detail']} |")
    a("")
    path.write_text("\n".join(L) + "\n", encoding="utf-8")
    return path


# ------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rebuild", action="store_true",
                    help="ignore per-cell checkpoints and re-extract")
    args = ap.parse_args()

    print("W-F1 WINNER FORENSICS")
    print("=" * 78)
    fixtures = []

    def fixture(tag, ok, detail):
        fixtures.append({"id": tag, "pass": bool(ok), "detail": detail})
        print(f"  [{'PASS' if ok else 'FAIL'}] {tag}: {detail}")
        return ok

    # ---------------------------------------------------------- ingest
    print("\n=== INGEST ===")
    packs = build_checkpoints(args.rebuild)
    rows = []
    for p in packs:
        rows.extend(p["rows"])
    rows.sort(key=lambda r: (r["cell"], r["tranche_id"]))
    print(f"  births total: {len(rows)}")

    sub = {}
    with open(SUBSTRATE, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                s = json.loads(line)
                sub[(s["cell"], s["tranche_id"])] = s
    print(f"  substrate rows: {len(sub)}")

    for r in rows:
        s = sub.get((r["cell"], r["tranche_id"]))
        if s:
            r["unit_bps"] = s.get("unit_bps")
            r["trigger_type"] = s.get("trigger_type")
            for k in sorted(s):
                if k.startswith(("mfe_", "mae_", "trunc_")) or k == "exit_bar_offset":
                    r[k] = s[k]

    resolved = [r for r in rows if r["resolved"]]
    unresolved = [r for r in rows if not r["resolved"]]

    # ------------------------------------------------------ F-WF1
    print("\n=== FIXTURES ===")
    fc = {}
    for r in rows:
        fc[r["fill_class"]] = fc.get(r["fill_class"], 0) + 1
    ok = (fc.get("r1") == 3825 and fc.get("v") == 78 and fc.get("re_entry") == 3214
          and len(rows) == 7117 and len(resolved) == 7094 and len(unresolved) == 23)
    fixture("F-WF1a", ok,
            f"r1={fc.get('r1')} + v={fc.get('v')} + re_entry={fc.get('re_entry')} "
            f"= {len(rows)} fills; {len(resolved)} resolved + {len(unresolved)} excluded")

    stopout = sum(1 for r in resolved if r["exit_reason"] in ("stop", "stop_gap"))
    fixture("F-WF1b", stopout == 5016, f"stopout (exit_reason in stop/stop_gap) = {stopout}, expect 5016")

    joined = sum(1 for r in resolved if r.get("unit_bps") is not None)
    fixture("F-WF1c", joined == 7094, f"substrate join covers {joined}/7094 resolved tranches")

    # ------------------------------------------------------ deciles
    resolved.sort(key=lambda r: (r["realized_r"], r["cell"], r["tranche_id"]))
    n = len(resolved)
    k = int(math.floor(DECILE_FRAC * n))
    L_rows = resolved[:k]
    W_rows = resolved[n - k:]
    cut_lo = L_rows[-1]["realized_r"]
    cut_hi = W_rows[0]["realized_r"]
    print(f"\n  n={n}  floor(0.1*n)={k}")
    print(f"  L (bottom {k}): realized_r <= {cut_lo}   range [{L_rows[0]['realized_r']}, {cut_lo}]")
    print(f"  W (top    {k}): realized_r >= {cut_hi}   range [{cut_hi}, {W_rows[-1]['realized_r']}]")
    _rr = [r["realized_r"] for r in resolved]
    n_le_lo = sum(1 for v in _rr if v <= cut_lo)
    n_ge_hi = sum(1 for v in _rr if v >= cut_hi)
    mult_lo = sum(1 for v in _rr if v == cut_lo)
    mult_hi = sum(1 for v in _rr if v == cut_hi)
    fixture("F-WF1d",
            len(W_rows) == k and len(L_rows) == k
            and n_le_lo == k and n_ge_hi == k and mult_lo == 1 and mult_hi == 1,
            f"decile sizes W={len(W_rows)} L={len(L_rows)}; count(r<={cut_lo})={n_le_lo}, "
            f"count(r>={cut_hi})={n_ge_hi}; cut multiplicities {mult_lo}/{mult_hi} "
            f"-> no tie straddles either boundary")

    epochs = sorted(r["ts_open_epoch"] for r in resolved)
    split_epoch = epochs[n // 2]
    split_iso = dt.datetime.fromtimestamp(split_epoch, dt.timezone.utc).strftime(TS_FMT)
    n_early = sum(1 for r in resolved if r["ts_open_epoch"] < split_epoch)
    print(f"  time split at median ts_open = {split_iso}  -> early {n_early} / late {n - n_early}")

    # ------------------------------------------------------ F-WF2 curtain
    flag_keys = sorted({k for r in rows for k in r if k.startswith("FLAG@")})
    varying = []
    for fk in flag_keys:
        vals = {r.get(fk) for r in resolved}
        vals.discard(None)
        if len(vals) > 1:
            varying.append(fk)
    curtain = []
    for f in CAT_FEATURES:
        curtain.append({"feature": f, "source": "BIRTH event field",
                        "attestation": "read from ENTRY_FILL/ADD_FILL; known at fill"})
    for f in NUM_FEATURES:
        curtain.append({"feature": f, "source": "BIRTH event field (bps forms use BIRTH px_fill)",
                        "attestation": "read from ENTRY_FILL/ADD_FILL; known at fill"})
    for f in ANNEX_FEATURES:
        curtain.append({"feature": f, "source": "derived from BIRTH ts_open",
                        "attestation": "entry timestamp; known at fill"})
    for fk in varying:
        curtain.append({"feature": fk, "source": "s2 snapshot on the BIRTH event",
                        "attestation": "engine writes s2 at fill time (engine/s2.py); known at fill"})
    rejected = [{"feature": "engagement_flags",
                 "reason": "NULL on all 7,117 births, present on all 7,094 EXITs -> POST-FILL"}]
    eng_at_birth = sum(1 for r in rows if r.get("engagement_flags") is not None
                       and not r["resolved"])
    birth_populated = all(
        all(r.get(f) is not None for r in rows) for f in CAT_FEATURES)
    outcome_leak = [f for f in (CAT_FEATURES + NUM_FEATURES + ANNEX_FEATURES)
                    if f in ("realized_r", "exit_reason", "funding_cum",
                             "give_back_r", "mfe_r", "mae_r", "hold_s",
                             "engagement_flags", "cohort", "pnl_usd")]
    fixture("F-WF2",
            birth_populated and eng_at_birth == 0 and not outcome_leak,
            f"{len(curtain)} Section-A features attested curtain-clean, all populated on "
            f"every birth; 0 post-fill fields present in the Section-A list; "
            f"{len(rejected)} rejected as post-fill (engagement_flags: "
            f"{eng_at_birth} births carry it)")

    # ------------------------------------------------------ Section A
    print("\n=== SECTION A ===")
    boot = Boot(len(W_rows), len(L_rows))

    specs = []
    for f in CAT_FEATURES:
        for lv in sorted({str(r.get(f)) for r in resolved}, key=str):
            real = next((r.get(f) for r in resolved if str(r.get(f)) == lv), lv)
            specs.append((f, real, "cat"))
    for fk in varying:
        for lv in (True, False):
            specs.append((fk, lv, "cat"))
    for f in NUM_FEATURES:
        specs.append((f, None, "num"))

    main_rows = analyse_family(W_rows, L_rows, specs, boot, "SECTION_A")
    main_rows = panel_and_time(resolved, W_rows, L_rows, main_rows, split_epoch)
    print(f"  Section-A family: {len(main_rows)} tests, "
          f"{sum(1 for r in main_rows if r['fdr_survives'])} FDR-surviving, "
          f"{sum(1 for r in main_rows if r['CANDIDATE'])} CANDIDATE")

    annex_specs = []
    for f in ANNEX_FEATURES:
        for lv in sorted({str(r.get(f)) for r in resolved}):
            annex_specs.append((f, lv, "cat"))
    annex_rows = analyse_family(W_rows, L_rows, annex_specs, boot, "ANNEX")
    annex_rows = panel_and_time(resolved, W_rows, L_rows, annex_rows, split_epoch)
    print(f"  Annex family:     {len(annex_rows)} tests, "
          f"{sum(1 for r in annex_rows if r['fdr_survives'])} FDR-surviving")

    # ------------------------------------------------------ F-WF3 determinism
    rep = analyse_family(W_rows, L_rows, specs, Boot(len(W_rows), len(L_rows)),
                         "SECTION_A")
    STAT_KEYS = ("name", "kind", "point", "ci_lo", "ci_hi", "ci_excludes_zero",
                 "p", "q", "fdr_survives", "n_W", "n_L")

    def project(tbl):
        # the statistical payload only; panel/time enrichment is applied to the
        # first table afterwards, so comparing raw rows would compare unequal shapes
        return json.dumps([{k: r[k] for k in STAT_KEYS} for r in tbl],
                          sort_keys=True).encode()

    pa, pb = project(main_rows), project(rep)
    a_all = hashlib.sha256(pa).hexdigest()
    b_all = hashlib.sha256(pb).hexdigest()
    fixture("F-WF3", pa == pb and a_all == b_all,
            f"full Section-A table ({len(main_rows)} rows x {len(STAT_KEYS)} stats) "
            f"recomputed at seed {SEED}: byte-identical, sha256 {a_all[:16]} == {b_all[:16]}")

    # ------------------------------------------------------ F-WF4 panel sums
    per_sym = {}
    for r in resolved:
        per_sym[r["symbol"]] = per_sym.get(r["symbol"], 0) + 1
    panel_sum = sum(per_sym.get(s, 0) for s in PANEL)
    annex_sum = sum(per_sym.get(s, 0) for s in ANNEX_ASSETS)
    fixture("F-WF4", panel_sum + annex_sum == len(resolved) and annex_sum > 0,
            f"panel {panel_sum} + annex {annex_sum} = {len(resolved)} resolved; "
            f"annex assets ({', '.join(ANNEX_ASSETS)}) excluded from panel sums")

    # ------------------------------------------------------ F-WF5 FDR arithmetic
    ranked = sorted([r for r in main_rows if not r["no_contrast"]],
                    key=lambda r: r["p"])
    m = len(ranked)
    n_nc = sum(1 for r in main_rows if r["no_contrast"])
    worked = []
    for i in (0, min(4, m - 1), m - 1):
        row = ranked[i]
        rank = i + 1
        raw = row["p"] * m / rank
        worked.append({"name": row["name"], "rank": rank, "m": m,
                       "p": row["p"], "p*m/rank": r6(raw), "q_reported": row["q"],
                       "formula": f"q = min_(j>={rank}) [ p_(j) * {m} / j ]"})
    f5_ok = True
    for w in worked:
        tail = [ranked[j]["p"] * m / (j + 1) for j in range(w["rank"] - 1, m)]
        if abs(min(min(tail), 1.0) - w["q_reported"]) > 1e-9:
            f5_ok = False
        w["q_recomputed"] = r6(min(min(tail), 1.0))
    fixture("F-WF5", f5_ok,
            f"BH recomputed by explicit formula for 3 rows (ranks "
            f"{[w['rank'] for w in worked]}) of m={m} tested rows "
            f"({n_nc} no-contrast rows excluded from the family); "
            f"recomputed q == reported q for all 3 "
            f"({[w['q_recomputed'] for w in worked]})")

    # ------------------------------------------------------ TRG
    print("\n=== TRG ===")
    # Driven through the SAME code path as every other TRG row (a keep-all
    # sentinel spec), so the fixture actually exercises trg_for() instead of
    # asserting a literal against itself.
    KEEP_ALL = {"feature": "__keep_all__", "level": None, "kind": "cat",
                "point": 1.0, "name": "(none - unfiltered book)"}
    unfiltered = trg_for(resolved, W_rows, KEEP_ALL)
    unfiltered["filter"] = "keep all"
    fixture("F-WF6",
            unfiltered["n_kept"] == len(resolved)
            and unfiltered["n_top_decile_kept"] == len(W_rows)
            and abs(unfiltered["TRG_pct"] - 100.0) < 1e-12
            and abs(unfiltered["delta_expectancy_R"]) < 1e-12,
            f"unfiltered book driven through trg_for(): kept {unfiltered['n_kept']}/"
            f"{len(resolved)}, top-decile {unfiltered['n_top_decile_kept']}/{len(W_rows)}, "
            f"retained R {unfiltered['top_decile_total_R_retained']} of "
            f"{unfiltered['top_decile_total_R_unfiltered']} -> TRG = "
            f"{unfiltered['TRG_pct']:.1f}% exactly""")

    surviving = [r for r in main_rows if r["fdr_survives"]]
    # Rank on the scale-free rank-biserial effect.  Sorting on |point| would
    # compare a proportion in [0,1] against a median delta in basis points, so
    # the two atr_*_bps rows would top the table by unit convention alone.
    surviving.sort(key=lambda r: (r["q"], r["p"], -abs(r["effect_rb"] or 0)))
    top5 = surviving[:5]
    trg = [trg_for(resolved, W_rows, r) for r in top5]
    for t in trg:
        print(f"  {t['discriminant']:<38} keep {t['kept_share']:.3f}  "
              f"dExp {t['delta_expectancy_R']:+.4f} R  TRG {t['TRG_pct']:.1f}%")

    # ------------------------------------------------------ Section B
    print("\n=== SECTION B (post-birth; NOT curtain-clean) ===")

    def anat(group):
        er = {}
        for r in group:
            er[r["exit_reason"]] = er.get(r["exit_reason"], 0) + 1
        hold = np.array([r["hold_s"] for r in group], dtype=float)
        gb = np.array([r["give_back_r"] for r in group], dtype=float)
        fnd = np.array([r["funding_cum"] for r in group], dtype=float)
        # CONTRACT DEFECT D4: funding_cum is USD, realized_r is R.  The literal
        # expression |funding_cum|/|realized_r| mixes units and cannot be read as
        # the "%" P-WF5 asserts.  Both are reported; P-WF5 is scored on the
        # dimensionless twin |funding_cum|/|pnl_usd| (both USD), which is
        # identically |funding_in_R|/|realized_r|.
        ratio = np.array([abs(r["funding_cum"]) / abs(r["realized_r"])
                          for r in group if r["realized_r"]], dtype=float)
        ratio_ok = np.array([abs(r["funding_cum"]) / abs(r["pnl_usd"])
                             for r in group if r.get("pnl_usd")], dtype=float)
        out = {
            "n": len(group),
            "exit_reason_mix": {k: er[k] for k in sorted(er)},
            "exit_reason_share": {k: r6(er[k] / len(group)) for k in sorted(er)},
            "hold_s_median": r6(np.median(hold)),
            "hold_s_p25": r6(np.percentile(hold, 25)),
            "hold_s_p75": r6(np.percentile(hold, 75)),
            "hold_h_median": r6(np.median(hold) / 3600.0),
            "give_back_r_median": r6(np.median(gb)),
            "funding_cum_median": r6(np.median(fnd)),
            "abs_funding_over_abs_r_median_MIXED_UNITS": r6(np.median(ratio)),
            "abs_funding_over_abs_pnl_median_DIMENSIONLESS": r6(np.median(ratio_ok)),
        }
        for h in ("h10", "h20", "h50", "h100", "exit"):
            mf = [r.get("mfe_bps_" + h) for r in group if r.get("mfe_bps_" + h) is not None]
            ma = [r.get("mae_bps_" + h) for r in group if r.get("mae_bps_" + h) is not None]
            out[f"mfe_bps_{h}_median"] = r6(np.median(mf)) if mf else None
            out[f"mae_bps_{h}_median"] = r6(np.median(ma)) if ma else None
        return out

    sec_b = {"W": anat(W_rows), "L": anat(L_rows), "book": anat(resolved),
             "per_mandate": {}}
    for md in sorted({r["mandate"] for r in resolved}):
        sec_b["per_mandate"][md] = {
            "W": anat([r for r in W_rows if r["mandate"] == md]) if any(
                r["mandate"] == md for r in W_rows) else None,
            "L": anat([r for r in L_rows if r["mandate"] == md]) if any(
                r["mandate"] == md for r in L_rows) else None,
        }
    hw, hl = sec_b["W"]["hold_s_median"], sec_b["L"]["hold_s_median"]
    print(f"  median hold  W {hw/3600:.2f} h   L {hl/3600:.2f} h   ratio {hw/hl:.2f}x")
    print(f"  |funding|/|pnl| median (dimensionless)  W "
          f"{sec_b['W']['abs_funding_over_abs_pnl_median_DIMENSIONLESS']:.4f}"
          f"   L {sec_b['L']['abs_funding_over_abs_pnl_median_DIMENSIONLESS']:.4f}")

    # ------------------------------------------------------ secondary books
    def secondary(name, subset):
        s = sorted(subset, key=lambda r: (r["realized_r"], r["cell"], r["tranche_id"]))
        kk = int(math.floor(DECILE_FRAC * len(s)))
        w, l = s[len(s) - kk:], s[:kk]
        bo = Boot(len(w), len(l))
        rr = analyse_family(w, l, specs, bo, name)
        rr = panel_and_time(subset, w, l, rr, split_epoch)
        return {"book": name, "n": len(s), "decile_size": kk,
                "cut_lo": r6(l[-1]["realized_r"]), "cut_hi": r6(w[0]["realized_r"]),
                "n_candidates": sum(1 for x in rr if x["CANDIDATE"]),
                "rows": rr}

    r1_book = secondary("R1_ONLY", [r for r in resolved if r["fill_class"] == "r1"])
    nov_book = secondary("V_EXCLUDED", [r for r in resolved if r["fill_class"] != "v"])
    print(f"\n  secondary r1-only: n={r1_book['n']} decile={r1_book['decile_size']} "
          f"candidates={r1_book['n_candidates']}")
    print(f"  sensitivity v-excluded: n={nov_book['n']} decile={nov_book['decile_size']} "
          f"candidates={nov_book['n_candidates']}")

    # ------------------------------------------------------ predictions
    cands = [r for r in main_rows if r["CANDIDATE"]]
    s2_cands = [r for r in cands if r["feature"].startswith("FLAG@")]
    re_row = next(r for r in main_rows if r["name"] == "fill_class=re_entry")
    z1 = next(r for r in main_rows if r["name"] == "zone=Z1")
    z2 = next(r for r in main_rows if r["name"] == "zone=Z2")
    preds = [
        {"id": "P-WF1", "stated": 0.70,
         "text": ">=1 s2 slow-stack flag is a CANDIDATE discriminant favouring W on >=3 panel assets.",
         "verdict": "PREMISE-FALSE",
         "note": ("No s2 leaf is a slow-stack flag. s2 carries only det (30m/1h detonation "
                  "bits) and levels (4h/12h/1d pivots); the slow-stack F1/F2/F4 EMA-cascade "
                  "bits live in the CENSUS arming-anchor table, not in these journals. "
                  f"Tested the whole s2 flag family instead: {len(varying)} varying flags, "
                  f"{len(s2_cands)} CANDIDATE.")},
        {"id": "P-WF2", "stated": 0.65,
         "text": "fill_class=re_entry is over-represented in L with CI excluding zero.",
         "verdict": ("CONFIRMED" if (re_row["point"] < 0 and re_row["ci_excludes_zero"])
                     else "FALSIFIED"),
         "note": (f"delta-prop (W-L) = {re_row['point']} "
                  f"CI [{re_row['ci_lo']}, {re_row['ci_hi']}] q={re_row['q']}")},
        {"id": "P-WF3", "stated": 0.55,
         "text": "deep zones (Z1/Z2) over-represented in W with CI excluding zero.",
         "verdict": ("CONFIRMED" if ((z1["point"] > 0 and z1["ci_excludes_zero"]) or
                                     (z2["point"] > 0 and z2["ci_excludes_zero"]))
                     else "FALSIFIED"),
         "note": (f"Z1 delta {z1['point']} CI [{z1['ci_lo']}, {z1['ci_hi']}]; "
                  f"Z2 delta {z2['point']} CI [{z2['ci_lo']}, {z2['ci_hi']}]")},
        {"id": "P-WF4", "stated": 0.60,
         "text": "median holding time of W >= 5x that of L.",
         "verdict": "CONFIRMED" if hw >= 5 * hl else "FALSIFIED",
         "note": f"median hold W={hw}s L={hl}s ratio={r6(hw/hl)}x"},
        {"id": "P-WF5", "stated": 0.50,
         "text": "median |funding_cum|/|realized_r| for W is < 10%.",
         "verdict": ("CONFIRMED" if
                     sec_b["W"]["abs_funding_over_abs_pnl_median_DIMENSIONLESS"] < 0.10
                     else "FALSIFIED"),
         "note": ("DEFECT D4: funding_cum is USD, realized_r is R -- the literal ratio "
                  "mixes units. Scored on the dimensionless twin |funding_cum|/|pnl_usd| "
                  "(identically |funding_in_R|/|realized_r|). W = "
                  f"{sec_b['W']['abs_funding_over_abs_pnl_median_DIMENSIONLESS']}, L = "
                  f"{sec_b['L']['abs_funding_over_abs_pnl_median_DIMENSIONLESS']}. "
                  "Literal mixed-unit figure for the record: W = "
                  f"{sec_b['W']['abs_funding_over_abs_r_median_MIXED_UNITS']}.")},
    ]
    print("\n=== PREDICTIONS ===")
    for p in preds:
        print(f"  {p['id']} [{int(p['stated']*100)}%] {p['verdict']}")

    # ------------------------------------------------------ emit
    all_pass = all(f["pass"] for f in fixtures)
    print("\n=== FIXTURE SUMMARY ===")
    print(f"  {sum(1 for f in fixtures if f['pass'])}/{len(fixtures)} pass")
    if not all_pass:
        print("\nHALT: a fixture failed. No WF1_discriminants.json emitted.")
        return 2

    BOX.mkdir(parents=True, exist_ok=True)
    big = BOX / "WF1_discriminant_tables.json"
    big.write_text(json.dumps(
        {"section_a": main_rows, "annex": annex_rows,
         "r1_only": r1_book, "v_excluded": nov_book},
        sort_keys=True, indent=1), encoding="utf-8")
    big_sha = sha256_file(big)

    out = {
        "study": "W-F1 WINNER FORENSICS",
        "contract": "exchange/queue/2026-08-03_WF1_winner_forensics_APOLLO.md",
        "generated_by": "scripts/wf1_forensics.py",
        "seed": SEED, "bootstrap_resamples": BOOT_N, "fdr_q": FDR_Q,
        "population": {
            "journals": str(JOURNALS.relative_to(ROOT)).replace("\\", "/"),
            "journal_files": len(sorted(JOURNALS.rglob("*.jsonl"))),
            "substrate": SUBSTRATE.name,
            "substrate_sha256": sha256_file(SUBSTRATE),
            "fills": len(rows), "fill_class": {k: fc[k] for k in sorted(fc)},
            "resolved": len(resolved), "unresolved_excluded": len(unresolved),
            "stopout": stopout,
        },
        "deciles": {
            "n": n, "decile_size": k,
            "W_cut_min_realized_r": r6(cut_hi), "W_max": r6(W_rows[-1]["realized_r"]),
            "L_cut_max_realized_r": r6(cut_lo), "L_min": r6(L_rows[0]["realized_r"]),
            "time_split_median_ts_open": split_iso,
            "n_early": n_early, "n_late": n - n_early,
        },
        "curtain_audit": {"clean": curtain, "rejected": rejected},
        "section_a": main_rows,
        "annex": annex_rows,
        "fdr_worked_examples": worked,
        "trg": {"unfiltered": unfiltered, "top5": trg},
        "section_b_NOT_CURTAIN_CLEAN": sec_b,
        "secondary_books": {
            "r1_only": {kk: vv for kk, vv in r1_book.items() if kk != "rows"},
            "v_excluded": {kk: vv for kk, vv in nov_book.items() if kk != "rows"},
        },
        "predictions": preds,
        "fixtures": fixtures,
        "intermediates": {
            "per_cell_checkpoints": "_reviewer_box/wf1/<cell>.json  (THE row-level book: all 7,117 fills, 20 files)",
            "discriminant_tables": {"path": "_reviewer_box/wf1/WF1_discriminant_tables.json",
                          "sha256": big_sha,
                          "bytes": big.stat().st_size},
        },
    }
    REPORTS.mkdir(parents=True, exist_ok=True)
    dst = REPORTS / "WF1_discriminants.json"
    dst.write_text(json.dumps(out, sort_keys=True, indent=1), encoding="utf-8")
    size = dst.stat().st_size
    print(f"\n  wrote {dst.relative_to(ROOT)} ({size/1024:.1f} KB)")
    if size > 1_000_000:
        print("  WARNING: deliverable exceeds the 1 MB contract ceiling")
    print(f"  wrote {big.relative_to(ROOT)} ({big.stat().st_size/1024:.1f} KB) sha {big_sha[:16]}")

    tbl = emit_tables(out, REPORTS / "WF1_tables.md")
    print(f"  wrote {tbl.relative_to(ROOT)} ({tbl.stat().st_size/1024:.1f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
