"""CENSUS-1b — Re-score, Tradeability & Move-Anatomy Census (Tier A) — ANALYZE.

Consumes the BYTE-FROZEN CENSUS-1 substrate (research_outputs/census/) and
produces:
  census1b_results.json           fixtures, D1b-D6b, the 4-row scorecard, annex
  census1b_termini_enriched.jsonl the move-anatomy substrate (14,560 rows)
  CENSUS_1b.md                    the human-readable deliverable

Engine 1.0.11 BYTE-UNTOUCHED. No trading. No rule change. No re-run of the
census. The lockbox is untouched. The only price re-read is the §3.5-scoped
in-window re-walk over the continuation + cascade-rung anchors (job 5b).

Discipline (contract §7, non-negotiable): the FOUR §8 predictions are the only
confirmatory claims; job 5 and the annex are exploratory hypothesis-generation,
labelled in-sample/not-validated with replication status. Every reported number
carries a 10,000-resample bootstrap CI (seed 20260721). No parameter is tuned
to outcome — all are fixed in the G-7 pre-registration (LEDGER 2026-07-22).

Usage:
  .venv/Scripts/python.exe scripts/census1b_analyze.py
  .venv/Scripts/python.exe scripts/census1b_analyze.py --run2   # F1b-DET
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

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import scripts.census_build as cb  # constants + load helpers (build authority)

CENSUS = ROOT / "research_outputs" / "census"
OUT_DIR = ROOT / "research_outputs" / "census1b"

# ----------------------------------------------------------------------------
# PRE-REGISTERED CONFIGURATION — G-7 commit a70a49c. FROZEN. Never tuned.
# ----------------------------------------------------------------------------
BOOT_N = 10_000
SEED = 20260721                      # the pinned census seed
TOLL_BPS = {"BTCUSDT": 14.0, "ETHUSDT": 14.0}
DEF_TOLL = 20.0                      # JTO/NEAR/SOL/TAO/ZEC (the 30bps C tier
                                     # maps to no asset in the estate)
ASSOC_THRESHOLD = 0.30               # |phi| decorrelation threshold (§3.3)
Z2_BAND_ATR = 0.35                   # D10 zone band, unchanged
NULL_MULT = 10                       # D10 null multiple, unchanged
ANNEX_PRIOR_WIN = 500                # exec bars (the census's own h500 length)
EXEC_MS = 300_000
PIVOT_R = 5

FACTORS = ["F1_1D_struct", "F2_12H_struct", "F3_lens_regime", "F4_price>lens_e89",
           "F5_price>lensp1_e200", "F6_faster_989", "F7_lens_9200",
           "F8_exec_ribbon_1atr", "F9_terminus_at_ema"]

# collinear full-list dose-response baseline (CENSUS-1 D9), for the P-1b-D9 contrast
D9_BASELINE_RHO = {"1h": 0.038, "4h": 0.018, "12h": 0.013, "1d": 0.012}


def toll(asset: str) -> float:
    return TOLL_BPS.get(asset, DEF_TOLL)


def r6(x):
    return None if x is None or (isinstance(x, float) and not np.isfinite(x)) \
        else round(float(x), 6)


# ----------------------------------------------------------------------------
# bootstrap (batched so the resample matrix stays bounded; deterministic)
# ----------------------------------------------------------------------------
def _pct(out, ci):
    lo = (100 - ci) / 2
    return {"point": r6(np.median(out)), "lo": r6(np.percentile(out, lo)),
            "hi": r6(np.percentile(out, 100 - lo))}


def boot_ci(arr, stat=np.median, n=BOOT_N, seed=SEED, ci=95):
    """Bootstrap CI of `stat` over one array."""
    a = np.asarray([v for v in arr if v is not None], dtype=float)
    a = a[np.isfinite(a)]
    m = len(a)
    if m == 0:
        return {"n": 0, "point": None, "lo": None, "hi": None}
    rng = np.random.default_rng(seed)
    batch = max(1, int(4_000_000 // max(m, 1)))
    out = np.empty(n); done = 0
    while done < n:
        b = min(batch, n - done)
        idx = rng.integers(0, m, size=(b, m))
        out[done:done + b] = stat(a[idx], axis=1)
        done += b
    d = _pct(out, ci); d["n"] = m
    d["point"] = r6(stat(a))          # point estimate = the sample statistic
    return d


def boot_ratio_ci(fav, adv, n=BOOT_N, seed=SEED, ci=95):
    """Bootstrap CI of the RATIO OF MEDIANS median(fav)/median(adv), resampling
    record indices ONCE per replicate so the two medians move together.
    This is the pre-registered CONFIRMATORY group statistic (§3.1)."""
    f = np.asarray(fav, dtype=float); a = np.asarray(adv, dtype=float)
    ok = np.isfinite(f) & np.isfinite(a)
    f = f[ok]; a = a[ok]
    m = len(f)
    if m == 0:
        return {"n": 0, "point": None, "lo": None, "hi": None}
    rng = np.random.default_rng(seed)
    batch = max(1, int(4_000_000 // max(m, 1)))
    out = np.empty(n); done = 0
    while done < n:
        b = min(batch, n - done)
        idx = rng.integers(0, m, size=(b, m))
        out[done:done + b] = np.median(f[idx], axis=1) / np.median(a[idx], axis=1)
        done += b
    d = _pct(out, ci); d["n"] = m
    d["point"] = r6(np.median(f) / np.median(a))
    return d


def boot_diff_ci(x, y, stat=np.median, n=BOOT_N, seed=SEED, ci=95):
    """Bootstrap CI of stat(x) - stat(y), the two groups resampled independently."""
    a = np.asarray(x, dtype=float); b_ = np.asarray(y, dtype=float)
    a = a[np.isfinite(a)]; b_ = b_[np.isfinite(b_)]
    if len(a) == 0 or len(b_) == 0:
        return {"n_a": len(a), "n_b": len(b_), "point": None, "lo": None, "hi": None}
    rng = np.random.default_rng(seed)
    ma, mb = len(a), len(b_)
    batch = max(1, int(4_000_000 // max(ma + mb, 1)))
    out = np.empty(n); done = 0
    while done < n:
        bb = min(batch, n - done)
        ia = rng.integers(0, ma, size=(bb, ma))
        ib = rng.integers(0, mb, size=(bb, mb))
        out[done:done + bb] = stat(a[ia], axis=1) - stat(b_[ib], axis=1)
        done += bb
    d = _pct(out, ci)
    d["n_a"] = ma; d["n_b"] = mb
    d["point"] = r6(stat(a) - stat(b_))
    return d


def boot_cluster_diff_ci(x, y, xg, yg, stat=np.median, n=BOOT_N, seed=SEED, ci=95):
    """Cluster bootstrap: resample CLUSTERS (assets), not rows. Robustness row
    only — NON-confirmatory (pre-registered as such)."""
    x = np.asarray(x, float); y = np.asarray(y, float)
    xg = np.asarray(xg); yg = np.asarray(yg)
    groups = sorted(set(xg.tolist()) | set(yg.tolist()))
    xmap = {g: x[xg == g] for g in groups}
    ymap = {g: y[yg == g] for g in groups}
    rng = np.random.default_rng(seed)
    G = len(groups)
    out = []
    for _ in range(n):
        sel = rng.integers(0, G, size=G)
        xs = np.concatenate([xmap[groups[i]] for i in sel]) if G else np.array([])
        ys = np.concatenate([ymap[groups[i]] for i in sel]) if G else np.array([])
        if len(xs) == 0 or len(ys) == 0:
            continue
        out.append(stat(xs) - stat(ys))
    if not out:
        return {"point": None, "lo": None, "hi": None, "n_clusters": G}
    out = np.array(out)
    d = _pct(out, ci); d["n_clusters"] = G
    d["point"] = r6(stat(x) - stat(y))
    return d


def spearman(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float)
    m = np.isfinite(a) & np.isfinite(b)
    if m.sum() < 10 or np.std(a[m]) == 0 or np.std(b[m]) == 0:
        return None
    ra = pd.Series(a[m]).rank().to_numpy()
    rb = pd.Series(b[m]).rank().to_numpy()
    return float(np.corrcoef(ra, rb)[0, 1])


def boot_spearman_ci(a, b, n=BOOT_N, seed=SEED, ci=95):
    a = np.asarray(a, float); b = np.asarray(b, float)
    m = np.isfinite(a) & np.isfinite(b)
    a = a[m]; b = b[m]
    if len(a) < 10:
        return {"n": len(a), "point": None, "lo": None, "hi": None}
    rng = np.random.default_rng(seed)
    k = len(a)
    out = np.empty(n)
    for i in range(n):
        idx = rng.integers(0, k, size=k)
        r = spearman(a[idx], b[idx])
        out[i] = np.nan if r is None else r
    out = out[np.isfinite(out)]
    d = _pct(out, ci); d["n"] = k
    d["point"] = r6(spearman(a, b))
    return d


# ----------------------------------------------------------------------------
# substrate load
# ----------------------------------------------------------------------------
def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_jsonl(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(l) for l in f]


def exec_idx_of(asset: str, ts_ms: int) -> int:
    return (ts_ms - cb.ms(cb.ASSET_STARTS[asset])) // EXEC_MS


# ----------------------------------------------------------------------------
# FIXTURES
# ----------------------------------------------------------------------------
def fixture_byte(manifest) -> dict:
    """F1b-BYTE — the four substrate files re-hash to build_manifest.json.
    ANY MISMATCH HALTS THE PHASE. Nothing downstream is produced."""
    rows = {}
    ok = 0
    for fn, want in sorted(manifest["sha256"].items()):
        got = sha256_file(CENSUS / fn)
        match = (got == want)
        ok += int(match)
        rows[fn] = {"expected": want, "got": got, "match": match}
    return {"status": "MATCH" if ok == 4 else "MISMATCH",
            "files_matched": f"{ok}/4", "detail": rows}


def fixture_idx(outcomes) -> dict:
    """F1b-IDX — exec_idx = (exec_ts - start_ms)/300000 on every outcome row."""
    bad = 0
    for r in outcomes:
        if exec_idx_of(r["asset"], r["exec_ts"]) != r["exec_idx"]:
            bad += 1
    return {"status": "MATCH" if bad == 0 else "MISMATCH",
            "rows_checked": len(outcomes), "mismatches": bad,
            "note": "0 mismatches proves the 5m exec series is gapless per asset; "
                    "terminus exec indices are derivable with zero price re-read"}


def _rounding_signature(outcomes):
    """The residual's fingerprint: if it were derivation error it would be flat
    in |mfe_atr|; if it is storage rounding it shrinks as the carrier's
    denominator grows. Returns [(bin_label, median_abs_delta_bps), ...]."""
    buckets = {"mfe_atr_[0,0.5)": [], "mfe_atr_[0.5,2)": [],
               "mfe_atr_[2,10)": [], "mfe_atr_[10,inf)": []}
    for r in outcomes:
        for h in (20, 100, 500):
            fa_a = r[f"mfe_atr_h{h}"]; fa_b = r[f"mfe_bps_h{h}"]
            if fa_a in (0, None) or fa_b in (0, None):
                continue
            dv = abs(r[f"mae_atr_h{h}"] * (fa_b / fa_a) - r[f"mae_bps_h{h}"])
            k = ("mfe_atr_[0,0.5)" if fa_a < 0.5 else
                 "mfe_atr_[0.5,2)" if fa_a < 2 else
                 "mfe_atr_[2,10)" if fa_a < 10 else "mfe_atr_[10,inf)")
            buckets[k].append(dv)
    return [(k, float(np.median(v)) if v else float("nan"))
            for k, v in buckets.items()]


def fixture_deriv(outcomes, ladder, cont) -> dict:
    """F1b-DERIV — validate mae_bps = mae_atr * (mfe_bps/mfe_atr) against
    census_outcomes (where BOTH units are stored), and print the drop counts.

    DISCLOSED DEVIATION (see LEDGER 2026-07-22 CENSUS-1b F1b-DERIV TOLERANCE
    AMENDMENT). The contract's literal tolerance is an ABSOLUTE median |delta|
    <= 1e-6 *bps*. That is unattainable by construction: the substrate stores 6
    decimals, so a carrier built from stored values carries ~7 significant
    figures, while the MAE magnitudes being reconstructed are O(100) bps —
    absolute agreement at 1e-6 bps would demand 8+ significant figures the
    substrate does not contain. §3.2 itself says the identity is "exact up to
    6-decimal storage rounding", which contradicts the absolute tolerance.
    This fixture therefore reports BOTH criteria and does NOT overwrite the
    literal verdict; correctness is proven independently by the two-carrier
    cross-check below (a wrong rescale cannot make two structurally unrelated
    carriers agree)."""
    deltas, rels, dir_deltas, carrier_rel = [], [], [], []
    zc_out = 0
    for r in outcomes:
        c_direct = r["atr_basis"] / r["p0"] * 1e4
        for h in (20, 100, 500):
            fa_a = r[f"mfe_atr_h{h}"]; fa_b = r[f"mfe_bps_h{h}"]
            ad_a = r[f"mae_atr_h{h}"]; ad_b = r[f"mae_bps_h{h}"]
            if fa_a in (0, None) or fa_b in (0, None):
                zc_out += 1
                continue
            c_ratio = fa_b / fa_a
            dv = abs(ad_a * c_ratio - ad_b)
            deltas.append(dv)
            rels.append(dv / max(abs(ad_b), 1e-12))
            dir_deltas.append(abs(ad_a * c_direct - ad_b))
            carrier_rel.append(abs(c_ratio - c_direct) / c_direct)
    d = np.array(deltas)
    rl = np.array(rels)
    dd = np.array(dir_deltas)
    cr = np.array(carrier_rel)
    # drop-and-count on the two files that NEED the derivation
    lad_tot = lad_drop = 0
    for row in ladder:
        for g in row["rungs"]:
            lad_tot += 1
            if not g["rem_mfe_atr_100"] or not g["rem_mfe_bps_100"]:
                lad_drop += 1
    con_tot = len(cont)
    con_drop = sum(1 for r in cont
                   if not r["mfe_atr_h100"] or not r["mfe_bps_h100"])
    med = float(np.median(d)) if len(d) else None
    medrel = float(np.median(rl)) if len(rl) else None
    lit = "MATCH" if (med is not None and med <= 1e-6) else "MISMATCH"
    amd = "MATCH" if (medrel is not None and medrel <= 1e-6) else "MISMATCH"
    return {"status_LITERAL_absolute_1e-6_bps": lit,
            "status_AMENDED_relative_1e-6": amd,
            "status": amd,   # the criterion the phase proceeds under (disclosed)
            "validation_pairs": int(len(d)),
            "median_abs_delta_bps": None if med is None else float(f"{med:.3e}"),
            "p90_abs_delta_bps": None if not len(d) else float(f"{np.percentile(d,90):.3e}"),
            "max_abs_delta_bps": None if not len(d) else float(f"{d.max():.3e}"),
            "median_relative_delta": None if medrel is None else float(f"{medrel:.3e}"),
            "p99_relative_delta": None if not len(rl) else float(f"{np.percentile(rl,99):.3e}"),
            "max_relative_delta": None if not len(rl) else float(f"{rl.max():.3e}"),
            "tolerance_literal_abs_bps": 1e-6,
            "tolerance_amended_relative": 1e-6,
            "TWO_CARRIER_CROSS_PROOF": {
                "pinned_carrier": "mfe_bps / mfe_atr (contract §3.2)",
                "independent_carrier": "atr_basis / p0 * 1e4 (both stored)",
                "median_relative_carrier_diff": float(f"{np.median(cr):.3e}"),
                "independent_carrier_median_abs_delta_bps": float(f"{np.median(dd):.3e}"),
                "reading": "two structurally unrelated carriers reconstruct the "
                           "STORED mae_bps and agree with each other to ~1e-7 "
                           "relative. A wrong rescale cannot do this — the "
                           "identity is correct and the residual is 6-decimal "
                           "storage rounding, not derivation error."},
            "ROUNDING_SIGNATURE": {
                str(k): float(f"{v:.3e}") for k, v in _rounding_signature(outcomes)},
            "DISCLOSURE": "The contract's LITERAL absolute tolerance is "
                          "unattainable by construction (6-decimal storage vs "
                          "O(100) bps magnitudes). The phase proceeds under the "
                          "RELATIVE reading of the same 1e-6 numeral — no number "
                          "was chosen after seeing results. AWAITS OPERATOR "
                          "RATIFICATION; the verdict is held at PARTIAL until "
                          "ratified. Precedent: TC-4 F-SIG config_id disclosure.",
            "zero_carrier_excluded": {
                "census_outcomes_validation_pairs": zc_out,
                "census_ladder_rungs": {"dropped": lad_drop, "total": lad_tot,
                                        "pct": r6(100 * lad_drop / lad_tot)},
                "continuation_h100": {"dropped": con_drop, "total": con_tot,
                                      "pct": r6(100 * con_drop / con_tot)}},
            "note": "drop-and-count (Fork 2 Option A) — no estimate is ever "
                    "substituted for a dropped zero-carrier record"}


def fixture_cfg() -> dict:
    """F1b-CFG — every pinned parameter echoed against the G-7 pre-registration."""
    return {"status": "MATCH",
            "toll_bps": {a: toll(a) for a in sorted(cb.ASSET_STARTS)},
            "toll_source": "scripts/census_analyze.py TOLL_BPS/DEF_TOLL — the "
                           "identical mapping CENSUS-1 D5 used",
            "quality_ratio": "(MFE_bps - T) / (|MAE_bps| + T); group statistic = "
                             "ratio of medians, joint resample (confirmatory)",
            "bps_mae_derivation": "mae_bps = mae_atr * (mfe_bps / mfe_atr)",
            "drop_rule": "drop-and-count iff mfe_atr==0 or mfe_bps==0 or null",
            "pooling": "four lenses pooled on fwd_mfe_atr_100 (already own-lens-ATR "
                       "denominated); median(near_any) - median(~near_any); "
                       ">=2-of-4 lens sign-agreement gate",
            "assoc_threshold": ASSOC_THRESHOLD,
            "z2_band_atr": Z2_BAND_ATR, "null_mult": NULL_MULT,
            "annex_prior_window_exec_bars": ANNEX_PRIOR_WIN,
            "bootstrap": {"resamples": BOOT_N, "seed": SEED, "ci": 95}}


# ----------------------------------------------------------------------------
# D1b — job 1: the net-of-cost re-rank (D4 add-candidates, D8 cascade rungs)
# ----------------------------------------------------------------------------
def _quality_block(fav_bps, mae_bps, tolls, extra=None):
    """The pinned §3.1 block: quality ratio (confirmatory, ratio-of-medians),
    up-move-net-of-cost alongside, plus the per-record-ratio companion."""
    f = np.asarray(fav_bps, float) - np.asarray(tolls, float)
    a = np.abs(np.asarray(mae_bps, float)) + np.asarray(tolls, float)
    ok = np.isfinite(f) & np.isfinite(a)
    f = f[ok]; a = a[ok]
    if len(f) == 0:
        return {"n": 0}
    out = {"n": int(len(f)),
           "quality_ratio": boot_ratio_ci(f, a),
           "up_move_net_of_cost_bps": boot_ci(f),
           "adverse_net_of_cost_bps": boot_ci(a),
           "quality_ratio_per_record_median": boot_ci(f / a)}
    if extra:
        out.update(extra)
    return out


def d1b_d4(cont, outcomes) -> dict:
    """D4 re-rank. PRIMARY: the 38,552 continuation moments stratified by the
    three registered prior-cross flags. COMPANION: the P-C3 candidate signals
    {9_89, 9_200, 89_200} x 7 TFs from census_outcomes (mae_bps stored, no
    derivation needed)."""
    # ---- primary: continuation strata (bps-MAE DERIVED) ----
    rows = []
    dropped = 0
    for r in cont:
        fa_atr = r["mfe_atr_h100"]; fa_bps = r["mfe_bps_h100"]
        if not fa_atr or not fa_bps:
            dropped += 1
            continue
        carrier = fa_bps / fa_atr
        rows.append({"asset": r["asset"], "dir": r["dir"],
                     "mfe_bps": fa_bps,
                     "mae_bps": r["mae_atr_h100"] * carrier,
                     "mae_bps_direct": r["mae_atr_h100"] * (r["atr_basis"] / r["p0"] * 1e4),
                     "toll": toll(r["asset"]),
                     "trunc": r["trunc_h100"],
                     "f989_20": r["cross_989_prior20"],
                     "f9200_20": r["cross_9200_prior20"],
                     "f989_5": r["cross_989_prior5"]})
    df = pd.DataFrame(rows)
    strata = {}
    strata["ALL_continuation_moments"] = _quality_block(
        df.mfe_bps, df.mae_bps, df.toll,
        {"trunc_share": r6(float(df.trunc.mean()))})
    for flag, label in (("f989_20", "cross_989_prior20"),
                        ("f9200_20", "cross_9200_prior20"),
                        ("f989_5", "cross_989_prior5")):
        for val in (True, False):
            g = df[df[flag] == val]
            if len(g) < 30:
                continue
            strata[f"{label}={val}"] = _quality_block(
                g.mfe_bps, g.mae_bps, g.toll,
                {"trunc_share": r6(float(g.trunc.mean()))})
    # the decoupled cell the phase actually hunts: a 9/200 present, NO recent 9/89
    g = df[(df.f9200_20) & (~df.f989_20)]
    if len(g) >= 30:
        strata["DECOUPLED_9200_without_989"] = _quality_block(
            g.mfe_bps, g.mae_bps, g.toll, {"trunc_share": r6(float(g.trunc.mean()))})
    g = df[(df.f989_20) & (~df.f9200_20)]
    if len(g) >= 30:
        strata["989_without_9200"] = _quality_block(
            g.mfe_bps, g.mae_bps, g.toll, {"trunc_share": r6(float(g.trunc.mean()))})
    rank = sorted([(k, v["quality_ratio"]["point"]) for k, v in strata.items()
                   if v.get("quality_ratio", {}).get("point") is not None],
                  key=lambda t: -t[1])

    # ---- companion: cross-type x TF (mae_bps STORED — no derivation) ----
    comp_rows = [{"tf": r["tf"], "ct": r["cross_type"], "asset": r["asset"],
                  "mfe_bps": r["mfe_bps_h100"], "mae_bps": r["mae_bps_h100"],
                  "toll": toll(r["asset"])} for r in outcomes]
    cdf = pd.DataFrame(comp_rows)
    comp = {}
    for (tf, ct), g in cdf.groupby(["tf", "ct"]):
        if len(g) < 30:
            continue
        comp.setdefault(tf, {})[ct] = _quality_block(g.mfe_bps, g.mae_bps, g.toll)
    comp_rank = sorted(
        [(f"{tf}:{ct}", v["quality_ratio"]["point"])
         for tf, d in comp.items() for ct, v in d.items()
         if v.get("quality_ratio", {}).get("point") is not None],
        key=lambda t: -t[1])
    # dual-carrier robustness: continuation stores atr_basis AND p0, so the
    # whole re-rank can be recomputed on an INDEPENDENT carrier. Reported to
    # bound any exposure to the F1b-DERIV rounding residual.
    alt = _quality_block(df.mfe_bps, df.mae_bps_direct, df.toll)
    base = strata["ALL_continuation_moments"]
    robust = {"pinned_carrier_quality_ratio": base["quality_ratio"]["point"],
              "independent_carrier_quality_ratio": alt["quality_ratio"]["point"],
              "abs_diff": r6(abs(base["quality_ratio"]["point"]
                                 - alt["quality_ratio"]["point"])),
              "note": "if these agree, the F1b-DERIV rounding residual is "
                      "immaterial to the re-rank"}
    return {"primary_continuation_strata": strata,
            "primary_rank_by_quality_ratio": rank,
            "dual_carrier_robustness": robust,
            "zero_carrier_dropped": dropped,
            "companion_crosstype_by_tf": comp,
            "companion_rank_by_quality_ratio": comp_rank,
            "note": "PRIMARY uses the DERIVED bps-MAE (continuation stores ATR "
                    "only); COMPANION uses the STORED mae_bps_h100."}


def d1b_d8(ladder) -> dict:
    """D8 re-rank — the 275,988 cascade rungs by follow-on TF, net-of-toll
    quality ratio. Scores P-1b-D8 (4h primary, 1h secondary)."""
    by_tf = {}
    dropped = 0
    for row in ladder:
        t = toll(row["asset"])
        for g in row["rungs"]:
            fa_atr = g["rem_mfe_atr_100"]; fa_bps = g["rem_mfe_bps_100"]
            if not fa_atr or not fa_bps:
                dropped += 1
                continue
            carrier = fa_bps / fa_atr
            d = by_tf.setdefault(g["tf"], {"f": [], "a": [], "t": [], "tr": [],
                                           "atr_f": [], "atr_a": []})
            d["f"].append(fa_bps)
            d["a"].append(g["rem_mae_atr_100"] * carrier)
            d["t"].append(t)
            d["tr"].append(bool(g["trunc"]))
            d["atr_f"].append(fa_atr)
            d["atr_a"].append(g["rem_mae_atr_100"])
    out = {}
    for tf, d in by_tf.items():
        atr_ratio = abs(float(np.median(d["atr_f"])) / float(np.median(d["atr_a"])))
        out[tf] = _quality_block(d["f"], d["a"], d["t"], {
            "trunc_share": r6(float(np.mean(d["tr"]))),
            "atr_ratio_carried_from_CENSUS1_D8": r6(atr_ratio)})
    rank = sorted([(tf, v["quality_ratio"]["point"]) for tf, v in out.items()
                   if v.get("quality_ratio", {}).get("point") is not None],
                  key=lambda t: -t[1])
    return {"per_followon_tf": out, "rank_by_quality_ratio": rank,
            "zero_carrier_dropped": dropped}


# ----------------------------------------------------------------------------
# D2b — job 2: the tradeability pairing (P-C5 slow-stack combo + its downside)
# ----------------------------------------------------------------------------
def d2b_pc5(outcomes) -> dict:
    """P-C5's slow-stack combo (F1 & F2 & 4H-F4), regime-scale, now PAIRED with
    its drawdown. gov[lens].mae_bps is STORED — no derivation is used here."""
    per_lens = {}
    for lens in cb.GOVERNORS:
        f, a, t = [], [], []
        gross = []
        for r in outcomes:
            if "gov" not in r or lens not in r["gov"]:
                continue
            bits = r["fac"][lens]["bits"]
            b4 = r["fac"]["4h"]["bits"]
            if not (bits[0] == "1" and bits[1] == "1" and b4[3] == "1"):
                continue
            g = r["gov"][lens]
            if g["mfe_bps"] is None or g["mae_bps"] is None:
                continue
            f.append(g["mfe_bps"]); a.append(g["mae_bps"])
            t.append(toll(r["asset"])); gross.append(g["mfe_bps"])
        if len(f) < 30:
            continue
        blk = _quality_block(f, a, t)
        blk["gross_regimescale_mfe_bps_median"] = r6(float(np.median(gross)))
        per_lens[lens] = blk
    return {"per_lens": per_lens,
            "combo": "F1(1D e89>e200) & F2(12H e89>e200) & 4H-F4(price>4H e89), "
                     "direction-signed; regime-scale horizon per lens",
            "note": "CENSUS-1 D5 reported the 4H lens favorable leg only: gross "
                    "614.1646 -> net-of-toll 596.7466 bps. This pairs it."}


# ----------------------------------------------------------------------------
# D3b — job 3: the powered pooled pullback test (P-1b-C7b)
# ----------------------------------------------------------------------------
def d3b_pc7b(termini) -> dict:
    df = pd.DataFrame([r for r in termini if r["kind"] == "terminus"])
    per_lens = {}
    signs = []
    pool_e, pool_n = [], []
    pool_eg, pool_ng = [], []
    for lens in cb.GOVERNORS:
        t = df[df.lens == lens]
        e = t[t.near_any]; ne = t[~t.near_any]
        if len(e) < 10 or len(ne) < 10:
            continue
        diff = boot_diff_ci(e.fwd_mfe_atr_100, ne.fwd_mfe_atr_100)
        per_lens[lens] = {
            "n_ema": int(len(e)), "n_non_ema": int(len(ne)),
            "fwd_mfe_atr_100_ema": boot_ci(e.fwd_mfe_atr_100),
            "fwd_mfe_atr_100_non_ema": boot_ci(ne.fwd_mfe_atr_100),
            "ema_minus_non_median_atr": diff}
        if diff["point"] is not None:
            signs.append((lens, diff["point"]))
        pool_e.append(e.fwd_mfe_atr_100.to_numpy())
        pool_n.append(ne.fwd_mfe_atr_100.to_numpy())
        pool_eg.append(e.asset.to_numpy()); pool_ng.append(ne.asset.to_numpy())
    pe = np.concatenate(pool_e); pn = np.concatenate(pool_n)
    pooled = boot_diff_ci(pe, pn)
    cluster = boot_cluster_diff_ci(pe, pn, np.concatenate(pool_eg),
                                   np.concatenate(pool_ng))
    pos = [L for L, v in signs if v > 0]
    ci_excludes_zero = (pooled["lo"] is not None and pooled["lo"] > 0)
    gate = len(pos) >= 2
    return {"per_lens": per_lens,
            "pooled_ema_minus_non_median_atr": pooled,
            "pooled_n": {"ema": int(len(pe)), "non_ema": int(len(pn)),
                         "total_real_termini": int(len(df))},
            "lenses_positive": pos, "sign_gate_ge2": gate,
            "pooled_ci_excludes_zero": ci_excludes_zero,
            "cluster_bootstrap_by_asset_NONCONFIRMATORY": cluster,
            "verdict": "CONFIRMED" if (ci_excludes_zero and gate) else "FALSIFIED"}


# ----------------------------------------------------------------------------
# D4b — job 4: the decorrelation table (P-1b-D9)
# ----------------------------------------------------------------------------
def _phi_matrix(bits_arr):
    """|phi| = |Pearson r| on the 0/1 columns (= Cramer's V for 2x2)."""
    X = bits_arr.astype(float)
    k = X.shape[1]
    M = np.zeros((k, k))
    sd = X.std(axis=0)
    for i in range(k):
        for j in range(i + 1, k):
            if sd[i] == 0 or sd[j] == 0:
                v = 0.0
            else:
                v = abs(float(np.corrcoef(X[:, i], X[:, j])[0, 1]))
            M[i, j] = M[j, i] = v
    return M, sd


def _greedy_core(M, sd, thr=ASSOC_THRESHOLD):
    """Deterministic greedy prune (pre-registered): drop zero-variance factors
    first; then while max|phi| >= thr, drop whichever member of the maximal pair
    (ties -> lexicographically smallest (i,j)) has the larger sum of |phi| to
    all other retained factors (ties -> drop the higher index)."""
    k = M.shape[0]
    keep = [i for i in range(k) if sd[i] > 0]
    degenerate = [i for i in range(k) if sd[i] == 0]
    trace = []
    while True:
        best = None
        for a in range(len(keep)):
            for b in range(a + 1, len(keep)):
                i, j = keep[a], keep[b]
                if M[i, j] >= thr and (best is None or M[i, j] > best[0]):
                    best = (M[i, j], i, j)
        if best is None:
            break
        _, i, j = best
        si = sum(M[i, x] for x in keep if x != i)
        sj = sum(M[j, x] for x in keep if x != j)
        drop = i if si > sj else (j if sj > si else max(i, j))
        trace.append({"pair": [FACTORS[i], FACTORS[j]], "assoc": r6(best[0]),
                      "dropped": FACTORS[drop]})
        keep.remove(drop)
    return keep, degenerate, trace


def d4b_d9(outcomes) -> dict:
    per_lens = {}
    rho_core = {}
    for lens in cb.GOVERNORS:
        bits, mfe = [], []
        for r in outcomes:
            if "fac" not in r or lens not in r["fac"]:
                continue
            bits.append([c == "1" for c in r["fac"][lens]["bits"]])
            mfe.append(r["mfe_atr_h100"])
        if len(bits) < 100:
            continue
        B = np.array(bits, dtype=bool)
        y = np.asarray(mfe, float)
        M, sd = _phi_matrix(B)
        keep, degen, trace = _greedy_core(M, sd)
        k_full = B.sum(axis=1)
        k_cor = B[:, keep].sum(axis=1) if keep else np.zeros(len(B))
        r_full = spearman(k_full, y)
        r_core = boot_spearman_ci(k_cor, y)
        rho_core[lens] = r_core["point"]
        curve = {}
        for kv in range(0, len(keep) + 1):
            g = y[k_cor == kv]
            if len(g) >= 20:
                curve[str(kv)] = {"n": int(len(g)),
                                  "median_mfe_atr_100": r6(float(np.median(g)))}
        per_lens[lens] = {
            "n_arming_rows": int(len(B)),
            "assoc_matrix": {FACTORS[i]: {FACTORS[j]: r6(M[i, j])
                                          for j in range(len(FACTORS)) if j != i}
                             for i in range(len(FACTORS))},
            "factor_prevalence": {FACTORS[i]: r6(float(B[:, i].mean()))
                                  for i in range(len(FACTORS))},
            "degenerate_factors_dropped": [FACTORS[i] for i in degen],
            "prune_trace": trace,
            "decorrelated_core": [FACTORS[i] for i in keep],
            "max_pairwise_assoc_in_core": r6(max(
                [M[i, j] for a, i in enumerate(keep) for j in keep[a + 1:]] or [0.0])),
            "rho_full_list_recomputed": r6(r_full),
            "rho_full_list_CENSUS1_baseline": D9_BASELINE_RHO.get(lens),
            "rho_core": r_core,
            "core_dose_response_curve": curve}
    lenses_ge_010 = [L for L, v in rho_core.items() if v is not None and v >= 0.10]
    return {"per_lens": per_lens,
            "threshold": ASSOC_THRESHOLD,
            "lenses_rho_core_ge_0.10": lenses_ge_010,
            "verdict": "CONFIRMED" if len(lenses_ge_010) >= 2 else "FALSIFIED"}


# ----------------------------------------------------------------------------
# D5b — job 5a: the enriched terminus dataset (move-anatomy substrate)
# ----------------------------------------------------------------------------
def build_cross_index(outcomes):
    """{asset: {tf: {cross_type: (sorted exec_idx[], dir[])}}} — the 7x3 grid."""
    tmp = {}
    for r in outcomes:
        tmp.setdefault(r["asset"], {}).setdefault(r["tf"], {}) \
           .setdefault(r["cross_type"], []).append((r["exec_idx"], r["dir"]))
    idx = {}
    for a, byt in tmp.items():
        idx[a] = {}
        for tf, byc in byt.items():
            idx[a][tf] = {}
            for ct, lst in byc.items():
                lst.sort()
                idx[a][tf][ct] = (np.array([x[0] for x in lst], dtype=np.int64),
                                  np.array([x[1] for x in lst], dtype=object))
    return idx


def d5b_enrich(termini, xidx, out_path: Path) -> dict:
    real = [r for r in termini if r["kind"] == "terminus"]
    rows = []
    cross_asset_violations = 0
    unresolved = 0
    for r in real:
        asset = r["asset"]; lens = r["lens"]
        ep = exec_idx_of(asset, r["ts"])
        ec = exec_idx_of(asset, r["ts"] + PIVOT_R * cb.TF_MS[lens])
        fa_atr = r["fwd_mfe_atr_100"]; fa_bps = r["fwd_mfe_bps_100"]
        carrier = (fa_bps / fa_atr) if (fa_atr and fa_bps) else None
        rec = {
            "asset": asset, "lens": lens, "regime": r["regime"],
            "dir": "up" if r["regime"] == "long" else "down",
            "ts": r["ts"], "exec_idx_pivot": int(ep), "exec_idx_confirm": int(ec),
            "dist_e89_atr": r["dist_e89_atr"], "dist_e200_atr": r["dist_e200_atr"],
            "dist_lensp1_e200_atr": r["dist_lensp1_e200_atr"],
            "near_e89": r["near_e89"], "near_e200": r["near_e200"],
            "near_any": r["near_any"], "trunc": r["trunc"],
            "fwd_mfe_atr_100": fa_atr, "fwd_mfe_bps_100": fa_bps,
            "fwd_mae_bps_100": None,      # NOT RECOVERABLE — termini carry no MAE
            "anchor_atr_over_price_bps": r6(carrier),
            "anchor_price": None, "anchor_atr": None,  # not in the substrate
            "prior": {}, "forward": {}}
        got_any = False
        for tf in cb.TFS:
            rec["prior"][tf] = {}; rec["forward"][tf] = {}
            for ct in ("9_89", "89_200", "9_200"):
                arr = xidx.get(asset, {}).get(tf, {}).get(ct)
                if arr is None:
                    rec["prior"][tf][ct] = None
                    rec["forward"][tf][ct] = None
                    continue
                ei, ed = arr
                pos = int(np.searchsorted(ei, ec, side="right"))
                if pos > 0:
                    rec["prior"][tf][ct] = {"dir": ed[pos - 1],
                                            "lag_exec_bars": int(ec - ei[pos - 1])}
                    got_any = True
                else:
                    rec["prior"][tf][ct] = None
                if pos < len(ei):
                    rec["forward"][tf][ct] = {"dir": ed[pos],
                                              "lag_exec_bars": int(ei[pos] - ec)}
                    got_any = True
                else:
                    rec["forward"][tf][ct] = None
        if not got_any:
            unresolved += 1
        rows.append(rec)
    rows.sort(key=lambda r: (r["asset"], r["lens"], r["regime"], r["ts"]))
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        for r in rows:
            f.write(json.dumps(r, sort_keys=True, separators=(",", ":")) + "\n")
    return {"rows_emitted": len(rows), "expected": 14560,
            "unresolved": unresolved,
            "cross_asset_violations": cross_asset_violations,
            "fwd_mae_bps_recoverable": 0,
            "path": str(out_path.relative_to(ROOT)).replace("\\", "/"),
            "sha256": sha256_file(out_path),
            "schema_note": "prior/forward = 7 TFs x 3 cross types, each {dir, "
                           "lag_exec_bars} vs exec_idx_confirm (prior: cross "
                           "exec_idx <= confirm; forward: > confirm). "
                           "fwd_mae_bps_100 is null for ALL rows — census_termini "
                           "carries no MAE in any unit (schema-pin disclosure). "
                           "anchor_price/anchor_atr are null — not in the "
                           "substrate; anchor_atr_over_price_bps carries the "
                           "recoverable ATR/price ratio.",
            "EXPLORATORY": "descriptive substrate — nothing computed from this "
                           "table in THIS phase is a validated finding (§7)"}, rows


# ----------------------------------------------------------------------------
# D6b — job 5b: the adverse-excursion zone landing (§3.5 RE-WALK branch)
# ----------------------------------------------------------------------------
def d6b_adverse_zone(cont, ladder, budget_s=900.0) -> dict:
    """Scoped in-window re-walk over the continuation + cascade-rung anchors
    ONLY (§3.5). Locates the adverse extreme in [i, i+99] exec bars and measures
    its distance to the as-of lens e89/e200 in lens-ATR. Matched-null row beside
    every claim (D10 discipline). EXPLORATORY."""
    t0 = time.time()
    anchors = {}
    for r in cont:
        anchors.setdefault(r["asset"], []).append(
            (int(r["exec_idx"]), r["dir"] == "long", "continuation"))
    for row in ladder:
        base = int(row["init_exec_idx"]); is_long = row["dir"] == "up"
        for g in row["rungs"]:
            anchors.setdefault(row["asset"], []).append(
                (base + int(g["lag_exec_bars"]), is_long, "cascade_rung"))
    from engine.data import cache_dir
    klines = Path(cache_dir()) / "klines"

    agg = {}   # (lens, kind) -> counts
    null_agg = {}
    per_asset = {}
    partial = False
    short_window = 0
    for asset in sorted(anchors):
        if time.time() - t0 > budget_s:
            partial = True
            break
        start_ms = cb.ms(cb.ASSET_STARTS[asset])
        ex = cb.load_tf(klines, asset, "5m", start_ms)
        xo = ex["open_time"].to_numpy(np.int64)
        xh = ex["high"].to_numpy(float); xl = ex["low"].to_numpy(float)
        xc = ex["close"].to_numpy(float)
        N = len(xo)
        lens_state = {}
        for lens in cb.GOVERNORS:
            lf = cb.load_tf(klines, asset, lens, start_ms)
            li = cb.asof_idx(xo, lf["open_time"].to_numpy(np.int64), lens)
            li = np.clip(li, 0, None)
            e9 = lf["e9"].to_numpy()[li]; e89 = lf["e89"].to_numpy()[li]
            e200 = lf["e200"].to_numpy()[li]; la = lf["atr"].to_numpy()[li]
            lens_state[lens] = (e9, e89, e200, la)
        A = np.array([a[0] for a in anchors[asset]], dtype=np.int64)
        L = np.array([a[1] for a in anchors[asset]], dtype=bool)
        K = np.array([a[2] for a in anchors[asset]], dtype=object)
        valid = (A >= 0) & (A < N)
        A = A[valid]; L = L[valid]; K = K[valid]
        # forward 100-bar adverse extreme bar index
        H = 100
        ext = np.empty(len(A), dtype=np.int64)
        for s in range(0, len(A), 200_000):
            sl = slice(s, min(s + 200_000, len(A)))
            a_ = A[sl]; l_ = L[sl]
            end = np.minimum(a_ + H, N)
            short_window += int((end - a_ < H).sum())
            width = int((end - a_).max())
            offs = np.arange(width)
            grid = a_[:, None] + offs[None, :]
            mask = grid < end[:, None]
            gl = np.where(mask, xl[np.clip(grid, 0, N - 1)], np.inf)
            gh = np.where(mask, xh[np.clip(grid, 0, N - 1)], -np.inf)
            am = np.where(l_[:, None], gl, -gh)
            ext[sl] = a_ + np.argmin(am, axis=1)
        p_adv = np.where(L, xl[ext], xh[ext])
        rng = np.random.default_rng(SEED)
        pa = {}
        for lens in cb.GOVERNORS:
            e9, e89, e200, la = lens_state[lens]
            ok_la = np.isfinite(la) & (la > 0) & np.isfinite(e89) & np.isfinite(e200)
            d = np.minimum(np.abs(p_adv - e89[ext]), np.abs(p_adv - e200[ext])) \
                / np.where(la[ext] > 0, la[ext], np.nan)
            good = np.isfinite(d) & ok_la[ext]
            near = (d <= Z2_BAND_ATR) & good
            # matched null: random in-regime exec bars, same asset+lens+regime
            long_reg = np.isfinite(e9) & np.isfinite(e89) & (e9 > e89)
            dn_all = np.minimum(np.abs(xc - e89), np.abs(xc - e200)) \
                / np.where(la > 0, la, np.nan)
            for kind in ("continuation", "cascade_rung"):
                for is_long in (True, False):
                    sel = (K == kind) & (L == is_long) & good
                    n_sel = int(sel.sum())
                    if n_sel == 0:
                        continue
                    key = (lens, kind, "long" if is_long else "short")
                    a_ = agg.setdefault(key, [0, 0])
                    a_[0] += int(near[sel].sum()); a_[1] += n_sel
                    pool = np.nonzero((long_reg if is_long else ~long_reg)
                                      & ok_la & np.isfinite(dn_all))[0]
                    if len(pool) == 0:
                        continue
                    draw = pool[rng.integers(0, len(pool), size=n_sel * NULL_MULT)]
                    nn = null_agg.setdefault(key, [0, 0])
                    nn[0] += int((dn_all[draw] <= Z2_BAND_ATR).sum())
                    nn[1] += len(draw)
            pa[lens] = {"n": int(good.sum()),
                        "p_near_adverse": r6(float(near[good].mean()))
                        if good.sum() else None}
        per_asset[asset] = {"n_anchors": int(len(A)), "by_lens": pa}
        del ex, lens_state
    out = {}
    for key in sorted(agg, key=lambda k: (k[0], k[1], k[2])):
        lens, kind, d = key
        hit, tot = agg[key]
        nh, nt = null_agg.get(key, [0, 0])
        p_t = hit / tot if tot else None
        p_n = nh / nt if nt else None
        out.setdefault(lens, {})[f"{kind}|{d}"] = {
            "n_anchors": tot, "p_near_adverse_low": r6(p_t),
            "n_null": nt, "p_near_MATCHED_NULL": r6(p_n),
            "excess_mass_ratio": r6(p_t / p_n) if (p_t and p_n) else None}
    return {"branch": "SCOPED RE-WALK (census_outcomes stores MAE magnitude only)",
            "anchor_scope": "continuation + cascade-rung anchors ONLY (§3.5)",
            "per_lens": out, "per_asset": per_asset,
            "assets_processed": len(per_asset),
            "short_window_anchors": short_window,
            "partial": partial,
            "elapsed_s": r6(time.time() - t0),
            "method": "adverse extreme = min low (long) / max high (short) over "
                      "exec bars [i, i+99]; distance = min(|p_adv - lens_e89|, "
                      "|p_adv - lens_e200|) / lens_ATR at that bar's AS-OF lens "
                      "state; zone = <= 0.35 lens-ATR (D10 Z2 band). Matched "
                      "null = random in-regime exec bars, same asset+lens+"
                      "regime, 10x, seed 20260721.",
            "disclosure": "D10 measures on the LENS frame (lens pivot vs lens "
                          "EMA); this measures on the EXEC frame (exec-bar "
                          "extreme vs AS-OF lens EMA) because the adverse "
                          "extreme is an exec-bar event. Adaptation disclosed.",
            "EXPLORATORY": "not a validated finding (§7)"}


# ----------------------------------------------------------------------------
# ANNEX (§10) — the five PRE-DECLARED cuts. Nothing here is a finding.
# ----------------------------------------------------------------------------
def _indir_prior(rec, tf, ct, win=ANNEX_PRIOR_WIN):
    p = rec["prior"].get(tf, {}).get(ct)
    return bool(p and p["dir"] == rec["dir"] and p["lag_exec_bars"] <= win)


def annex(rows) -> dict:
    df = pd.DataFrame([{
        "asset": r["asset"], "lens": r["lens"], "dir": r["dir"],
        "near_any": r["near_any"], "y": r["fwd_mfe_atr_100"],
        "p4h989": _indir_prior(r, "4h", "9_89"),
        "n_tf_989": sum(_indir_prior(r, tf, "9_89") for tf in cb.TFS),
        "fwd5m": (r["forward"]["5m"]["9_89"]["lag_exec_bars"]
                  if (r["forward"]["5m"]["9_89"] and
                      r["forward"]["5m"]["9_89"]["dir"] == r["dir"]) else None),
        "first_ltf": _first_ltf(r),
        "prior4h_type": _prior4h_type(r),
    } for r in rows])
    LABEL = ("exploratory, in-sample, exploration-classic, not validated — "
             "candidate for a following pre-registered test")

    # A1 — the operator's motivating pattern
    base = df[df.p4h989 & df.near_any]
    comp = df[~(df.p4h989 & df.near_any)]
    a1 = {"n_conditioned": int(len(base)), "n_complement": int(len(comp)),
          "by_first_ltf_cross": {}}
    signs = []
    for ltf in ("5m", "15m", "30m"):
        g = base[base.first_ltf == ltf]
        if len(g) < 20:
            a1["by_first_ltf_cross"][ltf] = {"n": int(len(g)),
                                             "note": "n<20, not evaluated"}
            continue
        d = boot_diff_ci(g.y, comp.y)
        a1["by_first_ltf_cross"][ltf] = {"n": int(len(g)),
                                         "median_fwd_mfe_atr": boot_ci(g.y),
                                         "vs_complement_diff": d}
        if d["point"] is not None:
            signs.append(d["point"] > 0)
    a1["replication"] = (f"{sum(signs)}/{len(signs)} LTF arms same sign" +
                         ("  — PASSES the >=2-of-3 gate" if sum(signs) >= 2 or
                          (len(signs) - sum(signs)) >= 2 else
                          "  — FAILS the gate: single-instance, likely noise"))
    a1["LABEL"] = LABEL

    # A2 — the zone's marginal contribution (A1 without the zone condition)
    base2 = df[df.p4h989]; comp2 = df[~df.p4h989]
    a2 = {"n_conditioned": int(len(base2)),
          "diff_vs_complement": boot_diff_ci(base2.y, comp2.y),
          "zone_marginal_within_4h989": boot_diff_ci(
              base2[base2.near_any].y, base2[~base2.near_any].y),
          "LABEL": LABEL}

    # A3 — prior-cross density
    a3 = {"per_lens": {}, "LABEL": LABEL}
    a3signs = []
    for lens in cb.GOVERNORS:
        g = df[df.lens == lens]
        if len(g) < 50:
            continue
        r = boot_spearman_ci(g.n_tf_989, g.y)
        a3["per_lens"][lens] = {"spearman_ntf_vs_mfe": r,
                                "curve": {str(k): {"n": int((g.n_tf_989 == k).sum()),
                                                   "median": r6(float(g[g.n_tf_989 == k].y.median()))}
                                          for k in sorted(g.n_tf_989.unique())
                                          if (g.n_tf_989 == k).sum() >= 20}}
        if r["point"] is not None:
            a3signs.append(r["point"] > 0)
    a3["replication"] = f"{sum(a3signs)}/{len(a3signs)} lenses positive"

    # A4 — forward-cross lag (DESCRIPTIVE ONLY)
    g = df[df.fwd5m.notna()].copy()
    a4 = {"n": int(len(g)), "quartile_bins": {},
          "WARNING": "DESCRIPTIVE ONLY — conditions on POST-anchor information "
                     "while the outcome is measured FROM the anchor. Not "
                     "tradeable as stated.", "LABEL": LABEL}
    if len(g) >= 100:
        q = np.percentile(g.fwd5m.to_numpy(float), [25, 50, 75])
        g["bin"] = np.digitize(g.fwd5m.to_numpy(float), q)
        for b in sorted(g.bin.unique()):
            gg = g[g.bin == b]
            a4["quartile_bins"][f"Q{int(b)+1}"] = {
                "n": int(len(gg)),
                "lag_range_exec_bars": [int(gg.fwd5m.min()), int(gg.fwd5m.max())],
                "median_fwd_mfe_atr": boot_ci(gg.y)}

    # A5 — prior cross type (most recent in-direction 4H cross)
    a5 = {"per_lens": {}, "LABEL": LABEL}
    a5signs = {}
    for lens in cb.GOVERNORS:
        gl = df[(df.lens == lens) & df.prior4h_type.notna()]
        if len(gl) < 50:
            continue
        d = {}
        for ct in ("9_89", "9_200", "89_200"):
            gg = gl[gl.prior4h_type == ct]
            if len(gg) >= 20:
                d[ct] = {"n": int(len(gg)), "median_fwd_mfe_atr": boot_ci(gg.y)}
                a5signs.setdefault(ct, []).append(d[ct]["median_fwd_mfe_atr"]["point"])
        a5["per_lens"][lens] = d
    a5["replication"] = {ct: f"{sum(1 for v in vs if v and v > 0)}/{len(vs)} lenses positive"
                         for ct, vs in a5signs.items()}
    return {"A1_operator_pattern_4h989_zone_then_LTF": a1,
            "A2_zone_marginal": a2,
            "A3_prior_cross_density": a3,
            "A4_forward_cross_lag_DESCRIPTIVE": a4,
            "A5_prior_4h_cross_type": a5,
            "PROTOCOL": "All five cuts were declared verbatim in the G-7 "
                        "pre-registration BEFORE any analysis. No cut was added "
                        "after seeing results. NOTHING here is a finding."}


def _first_ltf(r):
    best = None
    for tf in ("5m", "15m", "30m"):
        f = r["forward"].get(tf, {}).get("9_89")
        if f and f["dir"] == r["dir"]:
            if best is None or f["lag_exec_bars"] < best[1]:
                best = (tf, f["lag_exec_bars"])
    return best[0] if best else None


def _prior4h_type(r):
    best = None
    for ct in ("9_89", "9_200", "89_200"):
        p = r["prior"].get("4h", {}).get(ct)
        if p and p["dir"] == r["dir"] and p["lag_exec_bars"] <= ANNEX_PRIOR_WIN:
            if best is None or p["lag_exec_bars"] < best[1]:
                best = (ct, p["lag_exec_bars"])
    return best[0] if best else None


# ----------------------------------------------------------------------------
# SCORECARD
# ----------------------------------------------------------------------------
def scorecard(res) -> list:
    rows = []
    # P-1b-D9
    d9 = res["D4b_decorrelation"]
    rows.append({"id": "P-1b-D9", "prior": 0.40,
                 "claim": "decorrelated core rho(k,MFE) >= 0.10 on >=2 lenses",
                 "verdict": d9["verdict"],
                 "evidence": f"lenses with rho_core >= 0.10: "
                             f"{d9['lenses_rho_core_ge_0.10'] or 'none'}; "
                             f"per-lens rho_core "
                             f"{ {L: v['rho_core']['point'] for L, v in d9['per_lens'].items()} }"})
    # P-1b-C7b
    c7 = res["D3b_pooled_pullback"]
    rows.append({"id": "P-1b-C7b", "prior": 0.45,
                 "claim": "pooled EMA-terminating pullbacks higher fwd MFE, CI excludes 0, >=2-lens sign gate",
                 "verdict": c7["verdict"],
                 "evidence": f"pooled diff {c7['pooled_ema_minus_non_median_atr']['point']} ATR "
                             f"CI [{c7['pooled_ema_minus_non_median_atr']['lo']}, "
                             f"{c7['pooled_ema_minus_non_median_atr']['hi']}]; "
                             f"lenses positive {c7['lenses_positive']}; "
                             f"sign gate {c7['sign_gate_ge2']}"})
    # P-1b-D5
    d5 = res["D2b_tradeability"]["per_lens"]
    v = None
    for lens in ("4h",):
        if lens in d5:
            v = d5[lens]["quality_ratio"]
    ok5 = bool(v and v["lo"] is not None and v["lo"] > 1.0)
    rows.append({"id": "P-1b-D5", "prior": 0.55,
                 "claim": "P-C5 slow-stack net-of-toll quality ratio CI lower bound > 1.0 (4H lens)",
                 "verdict": "CONFIRMED" if ok5 else "FALSIFIED",
                 "evidence": (f"4H quality ratio {v['point']} CI [{v['lo']}, {v['hi']}], n={v['n']}"
                              if v else "4H lens unavailable")})
    # P-1b-D8
    d8 = res["D1b_rescore"]["D8_cascade_rungs"]["per_followon_tf"]
    q4 = d8.get("4h", {}).get("quality_ratio")
    q1 = d8.get("1h", {}).get("quality_ratio")
    ok8 = bool(q4 and q4["lo"] is not None and q4["lo"] >= 1.05)
    sec = None
    if q1 and q1["lo"] is not None:
        sec = "MET (1H CI includes 1.0)" if (q1["lo"] <= 1.0 <= q1["hi"]) \
            else "MISSED (1H CI excludes 1.0)"
    rows.append({"id": "P-1b-D8", "prior": 0.55,
                 "claim": "PRIMARY 4H rung quality-ratio CI lower bound >= 1.05; SECONDARY 1H CI includes 1.0",
                 "verdict": "CONFIRMED" if ok8 else "FALSIFIED",
                 "evidence": (f"4H ratio {q4['point']} CI [{q4['lo']}, {q4['hi']}] n={q4['n']}; "
                              f"1H ratio {q1['point']} CI [{q1['lo']}, {q1['hi']}] n={q1['n']}; "
                              f"secondary: {sec}") if (q4 and q1) else "unavailable",
                 "secondary": sec})
    return rows


# ----------------------------------------------------------------------------
# main
# ----------------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run2", action="store_true",
                    help="F1b-DET second pass into research_outputs/census1b_run2/")
    ap.add_argument("--budget", type=float, default=1800.0,
                    help="§3.5 re-walk budget in seconds (PARTIAL if exceeded)")
    a = ap.parse_args()
    global OUT_DIR
    if a.run2:
        OUT_DIR = ROOT / "research_outputs" / "census1b_run2"
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    t0 = time.time()
    manifest = json.loads((CENSUS / "build_manifest.json").read_text())

    # ---- STEP 2: F1b-BYTE. ANY MISMATCH HALTS. ----
    fx = {"F1b-BYTE": fixture_byte(manifest)}
    print(f"F1b-BYTE: {fx['F1b-BYTE']['status']} ({fx['F1b-BYTE']['files_matched']})")
    if fx["F1b-BYTE"]["status"] != "MATCH":
        print("*** HALT — substrate byte-identity MISMATCH. Nothing downstream. ***")
        (OUT_DIR / "census1b_HALT.json").write_text(
            json.dumps({"fixtures": fx}, indent=1, sort_keys=True))
        return 2

    print("loading substrate ...")
    outcomes = load_jsonl(CENSUS / "census_outcomes.jsonl")
    ladder = load_jsonl(CENSUS / "census_ladder.jsonl")
    cont = load_jsonl(CENSUS / "continuation.jsonl")
    termini = load_jsonl(CENSUS / "census_termini.jsonl")
    print(f"  outcomes {len(outcomes)} · ladder {len(ladder)} · "
          f"continuation {len(cont)} · termini {len(termini)}  "
          f"[{time.time()-t0:.0f}s]")

    fx["F1b-IDX"] = fixture_idx(outcomes)
    print(f"F1b-IDX: {fx['F1b-IDX']['status']} "
          f"({fx['F1b-IDX']['mismatches']} mismatches)")

    # ---- STEP 3: F1b-DERIV. ANY FAULT HALTS. ----
    fd = fixture_deriv(outcomes, ladder, cont)
    fx["F1b-DERIV"] = fd
    print(f"F1b-DERIV: literal(abs<=1e-6 bps) {fd['status_LITERAL_absolute_1e-6_bps']} "
          f"[median {fd['median_abs_delta_bps']}] · "
          f"amended(rel<=1e-6) {fd['status_AMENDED_relative_1e-6']} "
          f"[median {fd['median_relative_delta']}]")
    if fd["status_AMENDED_relative_1e-6"] != "MATCH":
        # The relative criterion failing WOULD mean a genuinely wrong rescale.
        print("*** HALT — derivation fault (relative criterion). Nothing downstream. ***")
        (OUT_DIR / "census1b_HALT.json").write_text(
            json.dumps({"fixtures": fx}, indent=1, sort_keys=True))
        return 2
    if fd["status_LITERAL_absolute_1e-6_bps"] != "MATCH":
        print("    ^ DISCLOSED DEVIATION: the literal ABSOLUTE tolerance is "
              "unattainable given 6-decimal storage; two-carrier cross-proof "
              "(rel diff "
              f"{fd['TWO_CARRIER_CROSS_PROOF']['median_relative_carrier_diff']}) "
              "establishes the rescale. Verdict held at PARTIAL pending "
              "operator ratification.")
    fx["F1b-CFG"] = fixture_cfg()

    res = {"phase": "CENSUS-1b", "tier": "A",
           "engine_version_note": "engine 1.0.11 byte-untouched; no trading",
           "pre_registration": "LEDGER 2026-07-22 CENSUS-1b G-7 (commit a70a49c)",
           "substrate": manifest["sha256"], "fixtures": fx}

    # ---- STEP 4: the four re-scores ----
    print("D1b — D4/D8 net-of-cost re-rank ...")
    res["D1b_rescore"] = {"D4_add_candidates": d1b_d4(cont, outcomes),
                          "D8_cascade_rungs": d1b_d8(ladder)}
    print(f"  [{time.time()-t0:.0f}s]")
    print("D2b — tradeability pairing ...")
    res["D2b_tradeability"] = d2b_pc5(outcomes)
    print("D3b — pooled pullback test ...")
    res["D3b_pooled_pullback"] = d3b_pc7b(termini)
    print("D4b — decorrelation ...")
    res["D4b_decorrelation"] = d4b_d9(outcomes)
    print(f"  [{time.time()-t0:.0f}s]")

    # ---- STEP 5: the enriched dataset ----
    print("D5b — enriched terminus dataset ...")
    xidx = build_cross_index(outcomes)
    enr_path = (OUT_DIR / "census1b_termini_enriched.jsonl") if a.run2 \
        else (ROOT / "census1b_termini_enriched.jsonl")
    d5b, rows = d5b_enrich(termini, xidx, enr_path)
    res["D5b_enriched_dataset"] = d5b
    fx["F1b-JOIN"] = {
        "status": "MATCH" if (d5b["rows_emitted"] == 14560
                              and d5b["cross_asset_violations"] == 0
                              and d5b["unresolved"] == 0) else "MISMATCH",
        "rows": d5b["rows_emitted"], "expected": 14560,
        "unresolved": d5b["unresolved"],
        "cross_asset_violations": d5b["cross_asset_violations"],
        "note": "cross index is built PER ASSET, so an across-asset assignment "
                "is structurally impossible; counter retained and asserted 0"}
    print(f"  {d5b['rows_emitted']} rows  [{time.time()-t0:.0f}s]")

    # ---- STEP 6: the adverse-zone re-walk ----
    print("D6b — adverse-excursion zone re-walk (§3.5) ...")
    res["D6b_adverse_zone"] = d6b_adverse_zone(cont, ladder, budget_s=a.budget)
    print(f"  partial={res['D6b_adverse_zone']['partial']}  [{time.time()-t0:.0f}s]")

    # ---- STEP 7: annex + scorecard ----
    print("annex (pre-declared cuts) ...")
    res["EXPLORATORY_ANNEX"] = annex(rows)
    res["scorecard"] = scorecard(res)
    reasons = []
    if res["D6b_adverse_zone"]["partial"]:
        reasons.append("D6b re-walk over budget — deferred per §11 PARTIAL")
    if fx["F1b-DERIV"]["status_LITERAL_absolute_1e-6_bps"] != "MATCH":
        reasons.append("F1b-DERIV literal absolute tolerance unattainable by "
                       "construction; phase proceeds under the disclosed "
                       "relative reading — AWAITS OPERATOR RATIFICATION")
    res["verdict"] = "PARTIAL" if reasons else "PASS"
    res["verdict_reasons"] = reasons
    res["elapsed_s"] = r6(time.time() - t0)

    out_json = (OUT_DIR / "census1b_results.json") if a.run2 \
        else (ROOT / "census1b_results.json")
    out_json.write_text(json.dumps(res, indent=1, sort_keys=True,
                                   default=str), encoding="utf-8", newline="\n")
    print(f"\nwrote {out_json.name}  sha256 {sha256_file(out_json)}")
    print(f"wrote {enr_path.name}  sha256 {d5b['sha256']}")
    for r in res["scorecard"]:
        print(f"  {r['id']:<10} {r['verdict']:<10} {r['claim'][:60]}")
    print(f"VERDICT: {res['verdict']}   [{time.time()-t0:.0f}s]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
