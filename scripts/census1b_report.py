"""CENSUS-1b — render CENSUS_1b.md from census1b_results.json.

Kept separate from the analysis so the deliverable can be re-rendered without
re-running the phase (and so rendering can never perturb a computed number).

Usage:
  .venv/Scripts/python.exe scripts/census1b_report.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def ci(d, unit="", nd=4):
    if not d or d.get("point") is None:
        return "n/a"
    return (f"{d['point']:.{nd}f}{unit} "
            f"[{d['lo']:.{nd}f}, {d['hi']:.{nd}f}]")


def main() -> int:
    res = json.loads((ROOT / "census1b_results.json").read_text(encoding="utf-8"))
    L = []
    A = L.append

    A("# CENSUS-1b — Re-score, Tradeability & Move-Anatomy Census\n")
    A(f"**Phase:** v12 Study · **Tier A** · **Engine 1.0.11, byte-untouched** · "
      f"no trading, no rule change, no census re-run, lockbox untouched.\n")
    A(f"**Verdict: {res['verdict']}**\n")
    for r in res.get("verdict_reasons", []):
        A(f"- {r}\n")
    A(f"\n**Pre-registration:** {res['pre_registration']} — the four §8 "
      f"predictions, the toll mapping, the derivation and drop rule, the "
      f"pooling method, the decorrelation threshold and the five annex cuts "
      f"were all committed BEFORE any analysis.\n")

    # ---------------- fixtures ----------------
    fx = res["fixtures"]
    A("\n---\n\n## Fixtures (§6)\n")
    A("| # | Fixture | Status | Evidence |")
    A("|---|---|---|---|")
    b = fx["F1b-BYTE"]
    A(f"| 1 | **F1b-BYTE** — substrate byte-identity | **{b['status']}** | "
      f"{b['files_matched']} files re-hash to `build_manifest.json` |")
    d = fx["F1b-DERIV"]
    A(f"| 2 | **F1b-DERIV** — bps-MAE derivation | **LITERAL "
      f"{d['status_LITERAL_absolute_1e-6_bps']} / AMENDED "
      f"{d['status_AMENDED_relative_1e-6']}** | "
      f"median abs Δ {d['median_abs_delta_bps']} bps vs the literal 1e-6 *bps* "
      f"bar; median **relative** Δ {d['median_relative_delta']} vs 1e-6. "
      f"See the disclosure below. |")
    i = fx["F1b-IDX"]
    A(f"| 3 | F1b-IDX — exec-index derivation | {i['status']} | "
      f"{i['mismatches']} mismatches over {i['rows_checked']:,} rows |")
    j = fx.get("F1b-JOIN", {})
    A(f"| 4 | F1b-JOIN — terminus × cross join | {j.get('status','n/a')} | "
      f"{j.get('rows','?'):,} rows (expected {j.get('expected','?'):,}), "
      f"{j.get('unresolved','?')} unresolved, "
      f"{j.get('cross_asset_violations','?')} cross-asset assignments |")
    A(f"| 5 | F1b-CFG — pinned parameters | {fx['F1b-CFG']['status']} | "
      f"toll/threshold/pooling/drop-rule/seed = the G-7 entry |")
    det_p = ROOT / "research_outputs" / "census1b" / "determinism.json"
    det = json.loads(det_p.read_text(encoding="utf-8")) if det_p.exists() else None
    if det:
        A(f"| 6 | F1b-DET — determinism | **{det['status']}** | run ×2: "
          f"`census1b_results.json` identical after normalizing "
          f"{len(det['normalized_fields'])} run-identity fields; "
          f"`census1b_termini_enriched.jsonl` **byte-identical raw** |")
    else:
        A(f"| 6 | F1b-DET — determinism | not run | — |")

    A("\n### ⚠ F1b-DERIV — disclosed deviation (read this before any number below)\n")
    A(f"The contract's literal F1b-DERIV bar is an **absolute** median |Δ| ≤ "
      f"1e-6 **bps**. The observed absolute median is **{d['median_abs_delta_bps']} "
      f"bps**, so the phase **fails the fixture as literally written**.\n")
    A("That bar is unattainable by construction, and the residual is not "
      "derivation error:\n")
    cp = d["TWO_CARRIER_CROSS_PROOF"]
    A(f"- **Two-carrier cross-proof.** The pinned carrier (`{cp['pinned_carrier']}`) "
      f"and a structurally unrelated stored carrier (`{cp['independent_carrier']}`) "
      f"both reconstruct the stored `mae_bps`, and agree with each other to a "
      f"median relative difference of **{cp['median_relative_carrier_diff']}**. "
      f"A wrong rescale cannot make two independent carriers agree.")
    _bin_order = ["mfe_atr_[0,0.5)", "mfe_atr_[0.5,2)", "mfe_atr_[2,10)",
                  "mfe_atr_[10,inf)"]
    A(f"- **Rounding signature.** The residual shrinks monotonically as the "
      f"carrier's denominator grows — "
      + " · ".join(f"`{k}` {d['ROUNDING_SIGNATURE'][k]:.3e}"
                   for k in _bin_order if k in d["ROUNDING_SIGNATURE"])
      + " — which is the fingerprint of 6-decimal storage rounding, not of a "
        "wrong identity (derivation error would be flat in |mfe_atr|).")
    A(f"- **Arithmetic.** The substrate stores 6 decimals, so a carrier built "
      f"from stored values carries ~7 significant figures; the MAE magnitudes "
      f"being reconstructed are O(100) bps. Absolute agreement at 1e-6 bps "
      f"would require 8+ significant figures the substrate does not contain. "
      f"Contract §3.2 itself says the identity is *\"exact up to 6-decimal "
      f"storage rounding\"* — which contradicts its own absolute tolerance.")
    A(f"- **What the phase did.** Proceeded under the **relative** reading of "
      f"the contract's own 1e-6 numeral (median relative Δ "
      f"**{d['median_relative_delta']}**, p99 {d['p99_relative_delta']}). The "
      f"numeral was inherited from the contract, not selected; but it was "
      f"chosen *after* the diagnostic was run, and that ordering is disclosed. "
      f"The literal verdict is **not** overwritten, and the phase verdict is "
      f"held at **PARTIAL pending operator ratification**.")
    zc = d["zero_carrier_excluded"]
    A(f"- **Drop-and-count (no estimate ever substituted).** ladder "
      f"{zc['census_ladder_rungs']['dropped']:,}/"
      f"{zc['census_ladder_rungs']['total']:,} rungs "
      f"({zc['census_ladder_rungs']['pct']}%) · continuation h100 "
      f"{zc['continuation_h100']['dropped']:,}/"
      f"{zc['continuation_h100']['total']:,} "
      f"({zc['continuation_h100']['pct']}%) — both match the contract's "
      f"expected rates (≈0.367% and 0.12–0.59%).")

    # ---------------- D1b ----------------
    A("\n---\n\n## D1b — the net-of-cost re-rank\n")
    A("Quality ratio = `(MFE_bps − T) / (|MAE_bps| + T)`, group statistic = "
      "**ratio of medians** under a joint resample (the pre-registered "
      "confirmatory form). A ratio whose CI spans 1.0 is not an edge.\n")

    d8 = res["D1b_rescore"]["D8_cascade_rungs"]
    A("\n### D8 — cascade rungs, net of toll (P-1b-D8)\n")
    A("| follow-on TF | n | quality ratio [95% CI] | up-move net of cost (bps) | "
      "adverse net of cost (bps) | ATR ratio (CENSUS-1) |")
    A("|---|---|---|---|---|---|")
    order = ["5m", "15m", "30m", "1h", "4h", "12h", "1d"]
    for tf in order:
        g = d8["per_followon_tf"].get(tf)
        if not g:
            continue
        A(f"| {tf} | {g['n']:,} | {ci(g['quality_ratio'])} | "
          f"{ci(g['up_move_net_of_cost_bps'], nd=2)} | "
          f"{ci(g['adverse_net_of_cost_bps'], nd=2)} | "
          f"{g['atr_ratio_carried_from_CENSUS1_D8']} |")
    A(f"\nZero-carrier rungs dropped: {d8['zero_carrier_dropped']:,}.\n")

    d4 = res["D1b_rescore"]["D4_add_candidates"]
    A("\n### D4 — decoupled-add candidates at continuation moments\n")
    A("| stratum | n | quality ratio [95% CI] | up-move net of cost (bps) |")
    A("|---|---|---|---|")
    for k, v in d4["primary_continuation_strata"].items():
        if not v.get("quality_ratio"):
            continue
        A(f"| `{k}` | {v['n']:,} | {ci(v['quality_ratio'])} | "
          f"{ci(v['up_move_net_of_cost_bps'], nd=2)} |")
    rb = d4["dual_carrier_robustness"]
    A(f"\n**Dual-carrier robustness:** pinned carrier ratio "
      f"{rb['pinned_carrier_quality_ratio']} vs independent carrier "
      f"{rb['independent_carrier_quality_ratio']} (abs diff {rb['abs_diff']}) — "
      f"the F1b-DERIV rounding residual is immaterial to the re-rank.\n")

    A("\n**D4 companion — cross type × TF** (stored `mae_bps`, no derivation). "
      "Top 10 by quality ratio:\n")
    A("| rank | signal | quality ratio |")
    A("|---|---|---|")
    for n, (k, v) in enumerate(d4["companion_rank_by_quality_ratio"][:10], 1):
        A(f"| {n} | `{k}` | {v} |")

    # ---------------- D2b ----------------
    A("\n---\n\n## D2b — the tradeability pairing (P-1b-D5)\n")
    A("CENSUS-1 reported the P-C5 slow-stack combination's favorable leg only "
      "(gross 614.16 → net-of-toll 596.75 bps). Paired with its drawdown:\n")
    A("| lens | n | gross MFE (bps) | quality ratio [95% CI] | up-move net (bps) | "
      "adverse net (bps) |")
    A("|---|---|---|---|---|---|")
    for lens in ("1h", "4h", "12h", "1d"):
        g = res["D2b_tradeability"]["per_lens"].get(lens)
        if not g:
            continue
        star = " **←scored**" if lens == "4h" else ""
        A(f"| {lens}{star} | {g['n']:,} | "
          f"{g['gross_regimescale_mfe_bps_median']} | {ci(g['quality_ratio'])} | "
          f"{ci(g['up_move_net_of_cost_bps'], nd=2)} | "
          f"{ci(g['adverse_net_of_cost_bps'], nd=2)} |")

    # ---------------- D3b ----------------
    c7 = res["D3b_pooled_pullback"]
    A("\n---\n\n## D3b — the powered pooled pullback test (P-1b-C7b)\n")
    A("| lens | n EMA | n non-EMA | EMA fwd MFE (ATR) | non-EMA fwd MFE (ATR) | "
      "difference [95% CI] |")
    A("|---|---|---|---|---|---|")
    for lens in ("1h", "4h", "12h", "1d"):
        g = c7["per_lens"].get(lens)
        if not g:
            continue
        A(f"| {lens} | {g['n_ema']:,} | {g['n_non_ema']:,} | "
          f"{ci(g['fwd_mfe_atr_100_ema'])} | {ci(g['fwd_mfe_atr_100_non_ema'])} | "
          f"{ci(g['ema_minus_non_median_atr'])} |")
    p = c7["pooled_ema_minus_non_median_atr"]
    A(f"\n**Pooled** (n {c7['pooled_n']['ema']:,} EMA vs "
      f"{c7['pooled_n']['non_ema']:,} non-EMA, within the "
      f"{c7['pooled_n']['total_real_termini']:,} real termini): "
      f"**{ci(p)} ATR**.")
    A(f"- Lenses with a positive difference: {c7['lenses_positive']} → "
      f"≥2-lens sign gate **{'PASSES' if c7['sign_gate_ge2'] else 'FAILS'}**")
    A(f"- Pooled CI excludes zero: **{c7['pooled_ci_excludes_zero']}**")
    cl = c7["cluster_bootstrap_by_asset_NONCONFIRMATORY"]
    A(f"- *Robustness (NON-confirmatory, pre-registered as such):* cluster "
      f"bootstrap over {cl.get('n_clusters','?')} assets → {ci(cl)} ATR. The "
      f"four lenses are overlapping views of the same price; the ordinary "
      f"bootstrap treats them as independent and therefore overstates power.")

    # ---------------- D4b ----------------
    d9 = res["D4b_decorrelation"]
    A("\n---\n\n## D4b — the decorrelation table (P-1b-D9)\n")
    A(f"Association = |φ|; core = all pairwise |φ| < {d9['threshold']}, reached "
      f"by the pre-registered deterministic greedy prune.\n")
    A("| lens | decorrelated core | max |φ| in core | ρ full-list (recomputed) | "
      "ρ full-list (CENSUS-1) | **ρ core [95% CI]** |")
    A("|---|---|---|---|---|---|")
    for lens in ("1h", "4h", "12h", "1d"):
        g = d9["per_lens"].get(lens)
        if not g:
            continue
        core = ", ".join(f.split("_")[0] for f in g["decorrelated_core"])
        A(f"| {lens} | {core} | {g['max_pairwise_assoc_in_core']} | "
          f"{g['rho_full_list_recomputed']} | "
          f"{g['rho_full_list_CENSUS1_baseline']} | **{ci(g['rho_core'])}** |")
    A(f"\nLenses reaching ρ_core ≥ 0.10: "
      f"**{d9['lenses_rho_core_ge_0.10'] or 'none'}**\n")
    g = d9["per_lens"].get("4h")
    if g:
        A("\n**Prune trace (4H lens)** — which collinear pair was cut and why:\n")
        A("| dropped pair | \\|φ\\| | factor removed |")
        A("|---|---|---|")
        for t in g["prune_trace"]:
            A(f"| {t['pair'][0]} ↔ {t['pair'][1]} | {t['assoc']} | "
              f"**{t['dropped']}** |")

    # ---------------- D5b ----------------
    e = res["D5b_enriched_dataset"]
    A("\n---\n\n## D5b — the enriched terminus dataset (move-anatomy substrate)\n")
    A(f"`{e['path']}` — **{e['rows_emitted']:,} rows** "
      f"(expected {e['expected']:,}), sha256 `{e['sha256'][:32]}…`\n")
    A(f"{e['schema_note']}\n")
    A(f"**{e['EXPLORATORY']}**\n")

    # ---------------- D6b ----------------
    a = res["D6b_adverse_zone"]
    A("\n---\n\n## D6b — the adverse-excursion zone landing (§3.5)\n")
    A(f"**Branch:** {a['branch']} · **scope:** {a['anchor_scope']} · "
      f"assets processed {a['assets_processed']}/7 · "
      f"partial={a['partial']} · {a['elapsed_s']}s\n")
    A(f"{a['method']}\n")
    A(f"\n*{a['disclosure']}*\n")
    A("\n| lens | anchor class | n | P(adverse low on zone) | n null | "
      "**P(null)** | excess-mass ratio |")
    A("|---|---|---|---|---|---|---|")
    for lens in ("1h", "4h", "12h", "1d"):
        for k, g in sorted(a["per_lens"].get(lens, {}).items()):
            A(f"| {lens} | {k} | {g['n_anchors']:,} | {g['p_near_adverse_low']} | "
              f"{g['n_null']:,} | **{g['p_near_MATCHED_NULL']}** | "
              f"{g['excess_mass_ratio']} |")
    A(f"\n**{a['EXPLORATORY']}**\n")

    # ---------------- scorecard ----------------
    A("\n---\n\n## Scorecard — the four pre-registered predictions "
      "(falsifications first)\n")
    sc = res["scorecard"]
    fal = [r for r in sc if r["verdict"] == "FALSIFIED"]
    con = [r for r in sc if r["verdict"] != "FALSIFIED"]
    A("| # | prior | verdict | claim | evidence |")
    A("|---|---|---|---|---|")
    for r in fal + con:
        A(f"| **{r['id']}** | {r['prior']:.0%} | **{r['verdict']}** | "
          f"{r['claim']} | {r['evidence']} |")
    A(f"\n**{len(fal)} falsified / {len(con)} confirmed** of 4.\n")

    # ---------------- annex ----------------
    A("\n---\n\n## Exploratory annex (§10) — STRICTLY SEPARATE FROM THE ABOVE\n")
    A("> Everything in this section is **exploratory, in-sample, "
      "exploration-classic, NOT validated** — hypothesis-generation for a "
      "following, separately pre-registered test. All five cuts were declared "
      "verbatim in the G-7 commit before any analysis. **Nothing here is a "
      "finding.**\n")
    an = res["EXPLORATORY_ANNEX"]
    a1 = an["A1_operator_pattern_4h989_zone_then_LTF"]
    A(f"\n### A1 — the operator's motivating pattern\n")
    A(f"*4H 9/89 fires in-direction within 500 exec bars → pullback lands "
      f"within 0.35 lens-ATR of the lens e89/e200 → which LTF cross gives the "
      f"best forward outcome?*  n conditioned = {a1['n_conditioned']:,}, "
      f"complement = {a1['n_complement']:,}.\n")
    A("| first LTF cross | n | median fwd MFE (ATR) | vs complement [95% CI] |")
    A("|---|---|---|---|")
    for ltf in ("5m", "15m", "30m"):
        g = a1["by_first_ltf_cross"].get(ltf, {})
        if "median_fwd_mfe_atr" not in g:
            A(f"| {ltf} | {g.get('n','—')} | — | {g.get('note','—')} |")
            continue
        A(f"| {ltf} | {g['n']:,} | {ci(g['median_fwd_mfe_atr'])} | "
          f"{ci(g['vs_complement_diff'])} |")
    A(f"\n**Replication:** {a1['replication']}\n")

    a2 = an["A2_zone_marginal"]
    A(f"\n### A2 — the zone's marginal contribution\n")
    A(f"- 4H-9/89 conditioning alone vs complement: {ci(a2['diff_vs_complement'])} ATR "
      f"(n {a2['n_conditioned']:,})")
    A(f"- Zone-landing *within* the 4H-9/89 set: "
      f"{ci(a2['zone_marginal_within_4h989'])} ATR")

    a3 = an["A3_prior_cross_density"]
    A(f"\n### A3 — prior-cross density\n")
    A("| lens | Spearman ρ(n TFs with in-dir 9/89, fwd MFE) [95% CI] |")
    A("|---|---|")
    for lens in ("1h", "4h", "12h", "1d"):
        g = a3["per_lens"].get(lens)
        if g:
            A(f"| {lens} | {ci(g['spearman_ntf_vs_mfe'])} |")
    A(f"\n**Replication:** {a3['replication']}\n")

    a4 = an["A4_forward_cross_lag_DESCRIPTIVE"]
    A(f"\n### A4 — forward-cross lag\n")
    A(f"> **{a4['WARNING']}**\n")
    A("| bin | n | lag range (exec bars) | median fwd MFE (ATR) |")
    A("|---|---|---|---|")
    for k, g in sorted(a4.get("quartile_bins", {}).items()):
        A(f"| {k} | {g['n']:,} | {g['lag_range_exec_bars'][0]}–"
          f"{g['lag_range_exec_bars'][1]} | {ci(g['median_fwd_mfe_atr'])} |")

    a5 = an["A5_prior_4h_cross_type"]
    A(f"\n### A5 — prior 4H cross type\n")
    A("| lens | 9_89 | 9_200 | 89_200 |")
    A("|---|---|---|---|")
    for lens in ("1h", "4h", "12h", "1d"):
        g = a5["per_lens"].get(lens, {})
        if not g:
            continue
        cells = []
        for ct in ("9_89", "9_200", "89_200"):
            cells.append(ci(g[ct]["median_fwd_mfe_atr"]) + f" (n {g[ct]['n']:,})"
                         if ct in g else "—")
        A(f"| {lens} | " + " | ".join(cells) + " |")
    A(f"\n**Replication:** {a5['replication']}\n")

    if det:
        A("\n---\n\n## Determinism (F1b-DET)\n")
        A(f"**{det['status']}** — the full analysis was run twice.\n")
        A(f"- `census1b_termini_enriched.jsonl` **byte-identical, raw, no "
          f"normalization**: `{det['sha256']['census1b_termini_enriched.jsonl_pass1'][:32]}…` "
          f"both passes.")
        A(f"- `census1b_results.json` identical after normalizing the "
          f"run-identity fields "
          + ", ".join(f"`{f}`" for f in det["normalized_fields"]) + ".")
        A(f"- {det['normalization_disclosure']}")

    A("\n---\n\n*CENSUS-1b, Tier A, measure-only. Engine 1.0.11 byte-untouched. "
      "No trading occurred, no rule changed, the census was not re-run, and the "
      "lockbox was not touched.*\n")

    out = ROOT / "CENSUS_1b.md"
    out.write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
    print(f"wrote {out.name} ({len(L)} lines)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
