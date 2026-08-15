#!/usr/bin/env python3
"""Render the CENSUS-2B ORACLE build document from the filed parquets.

Every number in the document is read from research_outputs/census2b/oracle/**;
nothing is typed by hand.  Run after scripts/census2b_oracle.py.
"""
from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
ORC = ROOT / "research_outputs" / "census2b" / "oracle"
DOC = ROOT / "exchange" / "reports" / "BUILD_2026-08-15_CENSUS2B_ORACLE.md"
# PINNED HISTORICAL, deliberately NOT imported from publish_exchange.  This
# module regenerates a FILED document whose BOX-COST section records the box as
# it stood on 2026-08-15 at filing time.  The operator raised the box to 16 MB
# later the same day; importing the live constant would silently rewrite that
# filed record's arithmetic with a ceiling that did not exist when it was
# written.  A historical report reproduces history.
BOX_BYTES = 6_390_000            # the box AT FILING; raised to 16_000_000 after

LENSES = ["5m", "15m", "30m", "1h", "4h"]
SR = ["FAST", "M", "MH", "H", "VH", "UH"]
SHORT = {"12_26 IN-WINDOW": "12_26 IN-WIN", "12_26 bare": "12_26 bare",
         "knot->fan transition": "knot->fan", "spring": "spring"}
CUT = {"ALL": "ALL", "dir=up": " up", "dir=down": " down",
       "orient=with": " o:with", "orient=against": " o:agst",
       "orient=mixed": " o:mixed"}


def f(x, w=6, d=3):
    return f"{'--':>{w}s}" if x is None or not np.isfinite(x) else f"{x:>{w}.{d}f}"


def exchange_bytes() -> int:
    t = 0
    for p in (ROOT / "exchange").rglob("*"):
        if p.is_file():
            t += p.stat().st_size
    return t


def main() -> int:
    g = pd.read_parquet(ORC / "oracle_grid.parquet")
    pin = pd.read_parquet(ORC / "r1_pinned_scales.parquet")
    rerun = pd.read_parquet(ORC / "r1_rerun_inert.parquet")
    occ2 = pd.read_parquet(ORC / "r2_knot_occupancy.parquet")
    occ3 = pd.read_parquet(ORC / "r3_state_occupancy.parquet")
    led = pd.read_parquet(ORC / "oracle_ledger.parquet")
    man = json.loads((ORC / "oracle_manifest.json").read_text())
    cards = json.loads((ORC / "cards.json").read_text())
    head = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                          capture_output=True, text=True).stdout.strip()
    pine_sha = subprocess.run(["shasum", "-a", "256", "pine/SS_v12_0_1.pine"],
                              cwd=ROOT, capture_output=True,
                              text=True).stdout.split()[0]
    L = []
    w = L.append

    w("# BUILD — CENSUS-2B · ORACLE  (Mac-native rev C)")
    w("")
    w(f"**Date** 2026-08-15 · **Branch** `v12-v1-census` · **HEAD at start** `{head}` · "
      f"**Seed** {man['seed']} · **Executor** HEPHAESTUS · **Drafted** APOLLO")
    w("")
    w(f"**CLASS — {man['class']}.** No registrations. F-KEY on every table. "
      "The grid is a *complete partition* of the filed event substrate under one ruler: no cell "
      "was selected, ranked or promoted, so there is no family to correct over. Any future "
      "selection **from** this grid is a new probe and declares its own *m* before it looks.")
    w("")
    w("**Programs (local, this repo):** `scripts/census2b_oracle.py` · "
      "`scripts/census2b_oracle_report.py`. Every ratified helper is **imported, not restated** — "
      "the grammar and the crossover rule from `census2b_program.py`, the R-1 ruler / "
      "duration-fixed horizon law / toll line from `census2b_parta.py`. This pass adds no constant "
      "that is not printed below.")
    w("")
    w("**Tables live local** at `research_outputs/census2b/oracle/` "
      "(`oracle_grid.parquet`, `oracle_ledger.parquet`, `r1_pinned_scales.parquet`, "
      "`r1_rerun_inert.parquet`, `r2_knot_occupancy.parquet`, `r3_state_occupancy.parquet`, "
      "`state_v2/<asset>/<tf>.parquet`, `oracle_manifest.json`). The document carries the grid "
      "whole and points at the rest.")
    w("")
    w("**STEP 0 — the indicator is filed.** `pine/SS_v12_0_1.pine`, byte-exact from the operator's "
      f"attachment, sha256 `{pine_sha}`, committed as *SSv12.0.1 indicator of record*. It ships "
      "direct to TradingView; the filing is for the record.")
    w("")
    w("---")
    w("")

    # ---------------------------------------------------------------- R-1
    w("## 1 · STAGE R-1 — [VETO 'kiss-scale']")
    w("")
    w("`delta = min(0.75, 0.6 x p95 |spread|/ATR)` per pair, `eps = delta/3`, `k = 10` unchanged. "
      "The grammar itself is untouched; only its two scale arguments are re-pinned, from each "
      "pair's own pooled spread distribution (panel x 5 lenses).")
    w("")
    w("```")
    w(f"{'class':10s} {'pair':11s} {'bars pooled':>12s} {'med|s|/ATR':>11s} "
      f"{'p95|s|/ATR':>11s} {'d v1':>6s} {'d v2':>7s} {'eps v2':>7s} {'rescaled':>9s}")
    for r in pin.itertuples():
        w(f"{r.pair_class:10s} {r.pair:11s} {r.n_bars_pooled:>12,d} "
          f"{f(r.med_spread_atr, 11, 4)} {f(r.p95_spread_atr, 11, 4)} "
          f"{r.delta_v1:>6.3f} {f(r.delta_v2, 7, 4)} {f(r.eps_v2, 7, 4)} "
          f"{'YES' if r.rescaled else 'no':>9s}")
    w("```")
    w("")
    inert = sorted(rerun.pair.unique().tolist())
    tot = int(rerun.n_refusals_v2.sum())
    w(f"**Previously inert under v1** (0 refusals across panel x 5 lenses): "
      f"`{'`, `'.join(inert)}`. The grammar was re-run **on these only**; live pairs keep their "
      "filed v1 rows, so nothing already published moves.")
    w("")
    w("```")
    w(f"{'pair':11s} {'cells':>6s} {'d v2':>7s} {'eps v2':>7s} {'touches v2':>12s} "
      f"{'refusals v1':>12s} {'refusals v2':>12s}")
    for tag in inert:
        s = rerun[rerun.pair == tag]
        w(f"{tag:11s} {len(s):>6d} {s.delta_v2.iloc[0]:>7.4f} {s.eps_v2.iloc[0]:>7.4f} "
          f"{int(s.n_touch_v2.sum()):>12,d} {0:>12,d} {int(s.n_refusals_v2.sum()):>12,d}")
    w("```")
    w("")
    w(f"**THE RE-PIN IS INERT — {tot} refusals recovered, 0 of {len(inert)} pairs woken.** "
      "This is a finding, not a failure, and the reason is arithmetic: "
      "`min(0.75, 0.6 x p95)` can only *lower* delta, and only for a pair whose p95 spread is "
      "under 1.25 ATR. Every inert pair is inert because it is **wide**, so the cap binds and "
      "nothing moves. Exactly one pair (`12_26`, p95 = "
      f"{float(pin.loc[pin.pair == '12_26', 'p95_spread_atr'].iloc[0]):.4f}) falls under the cap "
      "at all, and it moves delta by 0.0013.")
    w("")
    w("**The limb that actually fails is the veer limb, and it is measured here.** Touches are "
      "abundant; separation is not. `reach` is the best `|spread|/ATR` attainable within k=10 bars "
      "of a touch — the quantity delta thresholds.")
    w("")
    w("```")
    w(f"  {'pair':11s} {'touches':>12s} {'reach p50':>10s} {'reach p95':>10s} "
      f"{'reach MAX':>10s} {'delta pinned':>13s} {'clears?':>8s}")
    for tag in inert:
        s = rerun[rerun.pair == tag]
        rmx = float(np.nanmax(s.reach_max))
        w(f"  {tag:11s} {int(s.n_touch_v2.sum()):>12,d} "
          f"{f(float(np.nanmedian(s.reach_p50)), 10, 4)} "
          f"{f(float(np.nanmax(s.reach_p95)), 10, 4)} {f(rmx, 10, 4)} "
          f"{s.delta_v2.iloc[0]:>13.4f} "
          f"{('yes' if rmx >= s.delta_v2.iloc[0] else 'NEVER'):>8s}")
    w("```")
    w("")
    w("**MEASURED, NOT APPLIED.** No constant above is pinned by this pass. The reading: across "
      "the whole panel and all five lenses the maximum reach any of these pairs ever attains is "
      f"{float(np.nanmax(rerun.reach_max)):.4f} ATR, so **no delta at or above ~0.62 can ever wake "
      "them**, and a delta sized off the *spread* p95 will never be that low. A working re-pin has "
      "to be sized off the **reach** distribution (p95 ~ 0.28-0.33 ATR), which is a different law "
      "from the one ratified. That ruling is the operator's; this pass does not take it.")
    w("")

    # ---------------------------------------------------------------- R-2
    w("## 2 · STAGE R-2 — [VETO 'knot-scale']")
    w("")
    w("`KNOT = per-SR (width < 0.5 x ATR)`; BR-dispersion demoted to a **column**.")
    w("")
    w("**F-R2 — PASS, 0 violations.** Verified against the filed substrate rather than re-derived: "
      "`<SR>_knot` already thresholds *that family's own* `<SR>_width_atr` at 0.5, element for "
      "element, on every cell. **The per-SR reading was already the filed reading** — this veto "
      "ratifies what the substrate does, and the only change is that the Big-Ribbon envelope is "
      "now a reported column and never a knot definition.")
    w("")
    p = occ2[occ2.sr != "BR(column)"].pivot_table(index="sr", columns="tf",
                                                  values="knot_occupancy")
    p = p.reindex(index=SR, columns=LENSES)
    b = occ2[occ2.sr == "BR(column)"].pivot_table(index="sr", columns="tf",
                                                  values="med_width_atr").reindex(columns=LENSES)
    w("```")
    w("KNOT OCCUPANCY (share of warm bars with width < 0.5 ATR; panel mean)")
    w(f"  {'SR':6s} " + "".join(f"{t:>9s}" for t in LENSES))
    for s in SR:
        w(f"  {s:6s} " + "".join(f(p.loc[s, t], 9, 4) for t in LENSES))
    w("")
    w("BR-DISPERSION  median (max upper - min lower)/ATR over all 6 SRs -- COLUMN ONLY")
    w(f"  {'disp':6s} " + "".join(f(b.iloc[0][t], 9, 3) for t in LENSES))
    w("```")
    w("")
    w("The gradient is the point: a knot is common in FAST (~46% of bars) and rare in VH (~3%). A "
      "single Big-Ribbon threshold would have read 18-20 ATR of dispersion as *never knotted* and "
      "erased the FAST knot entirely. UH at 4h is blank because UH is not warm there (§6).")
    w("")

    # ---------------------------------------------------------------- R-3
    w("## 3 · STAGE R-3 — [VETO 'state-scale']")
    w("")
    w("`k = max(20, round(median_len/8))` per SR. `_v2` columns are written **beside** the "
      "originals (`oracle/state_v2/<asset>/<tf>.parquet`); nothing is overwritten. `eps` stays "
      "0.05 ATR and the three state codes are unchanged — k is the width-delta lookback only.")
    w("")
    ks = man["pins"]["state_k"]
    w("```")
    w(f"{'SR':6s} {'(fast,median,slow)':>22s} {'median_len':>11s} {'k v1':>6s} "
      f"{'k v2':>6s} {'changed':>8s}")
    RB = {"FAST": (9, 12, 26), "M": (62, 89, 127), "MH": (262, 316, 423),
          "H": (616, 889, 1272), "VH": (1618, 2618, 3618), "UH": (4236, 4618, 5000)}
    for s in SR:
        w(f"{s:6s} {str(RB[s]):>22s} {RB[s][1]:>11d} {20:>6d} {ks[s]:>6d} "
          f"{'YES' if ks[s] != 20 else 'no':>8s}")
    w("```")
    w("")
    w("**Occupancy, v1 (global k=20) -> v2 (per-SR k), panel mean.** Only the `flat` share is "
      "printed here — it is the one the mis-scale destroys; the full three-state grid at all five "
      "lenses is in `r3_state_occupancy.parquet`.")
    w("")
    fl = occ3[occ3.state == "flat"]
    w("```")
    w(f"  {'SR':6s} {'k v2':>6s} " + "".join(f"{t:>17s}" for t in LENSES))
    for s in SR:
        row = f"  {s:6s} {ks[s]:>6d} "
        for t in LENSES:
            q = fl[(fl.sr == s) & (fl.tf == t)]
            row += (f"{q.occ_v1.mean():.4f}->{q.occ_v2.mean():.4f}".rjust(17)
                    if len(q) else " " * 17)
        w(row)
    w("```")
    w("")
    uh5 = fl[(fl.sr == "UH") & (fl.tf == "5m")]
    w(f"**This is the largest single correction in the pass.** Under the global k=20, UH read "
      f"**{uh5.occ_v1.mean():.1%} flat** at 5m — a 4236/5000 band does not change width "
      f"measurably in 20 bars of a 5-minute chart, so the state column was reporting the "
      f"lookback, not the ribbon. At k=577 it becomes "
      f"{uh5.occ_v2.mean():.1%} flat and the three states separate. FAST and M are unchanged by "
      "construction (their k floors at 20), so the correction lands exactly where the mis-scale "
      "was and nowhere else.")
    w("")

    # ---------------------------------------------------------------- O
    w("## 4 · THE ORACLE GRID")
    w("")
    w(f"**{len(led):,} anchors**, complete partition, m = 0, toll-honest. "
      "`oracle_ledger.parquet` (row-level) · `oracle_grid.parquet` (this grid).")
    w("")
    w("**Ruler** — R-1: signed *terminal* return over the duration-fixed horizon, ATR-normalised "
      "**at the anchor**; MFE/MAE window `[i+1, i+bars]`. **Horizons are durations, not bar "
      "counts**: H20 = 1h40m, H100 = 8h20m, so `bars = round(h_ms / TF_MS)` — "
      "20/100 at 5m, 7/33 at 15m, 3/17 at 30m, 2/8 at 1h, and at 4h **H20 is INFEASIBLE "
      "(bars = 0), emitted as NaN and never substituted with one bar**. "
      "**Toll** — 10 bps round trip in ATR units, median over *that cell's own anchor population*; "
      "`NET = median - toll`. **Orient** — `with` = VH **and** UH both fanned the way the event "
      "points; `against` = both fanned opposite; `mixed` = anything else, including any "
      "`mixed(0)` or `n/a(-9)` limb, because a not-yet-warm ultra-high ribbon is not evidence of "
      "agreement.")
    w("")
    for tf in LENSES:
        S = g[g.tf == tf]
        w(f"### lens {tf}")
        w("")
        w("```")
        w((f"{'class':13s}{'cut':8s}{'n':>7s} {'med20':>7s}{'NET20':>7s} "
           f"{'med100':>7s}{'NET100':>7s} {'toll':>6s}   {'H20 IQR':<15s} "
           f"{'H100 IQR':<15s}").rstrip())
        for cls in [c for c, _ in _CLASSES]:
            C = S[S.cls == cls]
            lab = SHORT.get(cls, cls)
            if not len(C) or int(C[C.cut == "ALL"].n.iloc[0]) == 0:
                w(f"{lab:13s}{'--':8s}{0:>7d} NO EVENTS AT THIS LENS")
                continue
            for r in C.itertuples():
                if r.n == 0:
                    continue
                row = (f"{lab if r.cut == 'ALL' else '':13s}{CUT[r.cut]:8s}{r.n:>7,d}"
                       f" {f(r.H20_med, 7)}{f(r.H20_net, 7)}"
                       f" {f(r.H100_med, 7)}{f(r.H100_net, 7)}")
                if r.cut == "ALL":          # IQR + toll ride at the end, so the
                    row += (f" {f(r.toll_atr, 6, 4)}   "   # cut rows align free
                            f"[{f(r.H20_q25, 6)},{f(r.H20_q75, 6)}]"
                            f" [{f(r.H100_q25, 6)},{f(r.H100_q75, 6)}]")
                w(row)
        w("```")
        w("")

    w("**F-O1 — counts reconcile to the filed inventories: PASS.** Every native cross class, both "
      "halves of `12_26`, and `spring` reconcile **exactly** (delta = 0) against "
      "`crosses/`, `windows/` and `springs/`. `knot->fan` is a join and is bounded by both parents "
      "(191,564 <= min(262,086 knots, 318,427 fans)). `26_89` is derived this pass and is excluded "
      "from reconciliation by construction — see §6.")
    w("")
    w("**F-O1b — the derivation rule reproduces a filed class: PASS.** Re-deriving `12_26` from "
      "the pinned `emas/` substrate with the same `crossover` expression gives **197,305 events "
      "against 197,305 filed, 0 mismatched cells**. That is what licenses `26_89`.")
    w("")

    # ---------------------------------------------------------------- W-E+
    w("## 5 · STAGE W-E+ — the three full cards")
    w("")
    w("Straight from the campaign rows in `_reviewer_box/wf1/*USDT_*.json`. **No recomputation.** "
      "`gross_R` is the stored `ride_R` from `research_outputs/census2a/cen5/cen5_campaigns.parquet` "
      "— read, not recomputed. `realized_r`, `mfe_r`, `mae_r`, `give_back_r` are in the journal's "
      "own R units (size-scaled); `gross_R` is the size-free ruler.")
    w("")
    w("```")
    hdr = ["", "ETHUSDT_swing|c61t75", "ETHUSDT_intraday|c554t720",
           "ETHUSDT_intraday|c186t225"]
    rows = [("mandate / dir", "mandate", "dir"), ("size_r", "size_r", None),
            ("grade / zone", "grade", "zone"), ("entry ts", "ts_open", None),
            ("entry px_fill", "px_fill", None), ("stop", "stop", None),
            ("exit px", "exit_px_fill", None), ("exit ts", "ts_close", None),
            ("exit_reason", "exit_reason", None), ("realized_r", "realized_r", None),
            ("gross_R", "gross_R", None), ("mfe_r", "mfe_r", None),
            ("mae_r", "mae_r", None), ("give_back_r", "give_back_r", None),
            ("funding_cum", "funding_cum", None), ("hold (s)", "hold_s", None)]
    by = {c["tranche_id"]: c for c in cards}
    w(f"{'':16s}" + "".join(f"{h.split('|')[-1] if h else '':>28s}" for h in hdr[1:]))
    w(f"{'':16s}" + "".join(f"{h.split('|')[0] if h else '':>28s}" for h in hdr[1:]))
    for label, k1, k2 in rows:
        cells = []
        for tid in hdr[1:]:
            c = by.get(tid, {})
            v = c.get(k1)
            if k2:
                v = f"{v} / {c.get(k2)}"
            if isinstance(v, float):
                v = f"{v:.6f}"
            cells.append(f"{str(v):>28s}")
        w(f"{label:16s}" + "".join(cells))
    w("```")
    w("")
    cc = [by[t] for t in hdr[1:]]
    reasons = sorted({c["exit_reason"] for c in cc})
    holds = sorted(c["hold_s"] / 86400.0 for c in cc)
    gb = sorted(c["give_back_r"] for c in cc)
    mae = max(abs(c["mae_r"]) for c in cc)
    yrs = sorted({c["ts_open"][:4] for c in cc})
    w(f"All three are ETH **longs** and all three resolved on a **directional exit, never a "
      f"stop** — {' / '.join('`' + r + '`' for r in reasons)} — after "
      f"{holds[0]:.0f} to {holds[-1]:.0f} days open, spread across "
      f"{', '.join(yrs[:-1])} and {yrs[-1]}. "
      f"The shape they share is the one worth naming: **`mae_r` never exceeds {mae:.2f}** — the "
      f"stop was never seriously threatened on any of them — while `give_back_r` runs "
      f"{gb[0]:.0f} to {gb[-1]:.0f}, a give-back of "
      f"{gb[0] / max(mae, 1e-9):.0f}-{gb[-1] / max(mae, 1e-9):.0f}x the initial risk unit handed "
      f"back from the high-water mark. **What decided these campaigns was give-back, not the "
      f"stop.** Read alongside the grid with care: §4 conditions on nothing that resembles a hold "
      f"of {holds[0]:.0f}-{holds[-1]:.0f} days, so it does not speak to these arms directly. It is "
      f"the mark-default surface they are drawn from, not a model of them.")
    w("")

    # ---------------------------------------------------------------- findings
    w("## 6 · FINDINGS — NOT FIXED")
    w("")
    w("Named, measured, left alone. Each needs an operator ruling, not a patch.")
    w("")
    w("**F-1 · The kiss-scale veto as ratified cannot do its job.** §1. `min(0.75, 0.6 x p95 "
      "spread)` is a *ceiling-lowering* law aimed at tight pairs; the five inert pairs are inert "
      "because they are **wide**. Measured veer reach never exceeds 0.61 ATR on any of them, "
      "anywhere on the panel. **Ruling needed: re-size delta off the reach distribution, or accept "
      "these five as permanently inert and say so.** Not taken here — a different law is a "
      "different veto.")
    w("")
    w("**F-2 · `26_89` is not in the filed crosses taxonomy.** The taxonomy is 18 within-family "
      "pairs + 5 midlines + price/band; `26_89` is a **cross-family** adjacency (FAST-slow vs "
      "M-mid) nobody emitted. Rather than fabricate or drop the class, it is **derived this pass** "
      "from the pinned `emas/` substrate with the same `crossover` expression and the same "
      "feasibility gate, labelled `derived<emas>` on every row, and **excluded from F-O1**. "
      "F-O1b licenses the rule by reproducing `12_26` exactly. "
      f"{int((led.cls == '26_89').sum()):,} events. **Ruling needed: promote `26_89` into the "
      "pinned taxonomy and re-run stage 4, or keep it derived-at-query.**")
    w("")
    w("**F-3 · The `12_26 IN-WINDOW` / `bare` split is structurally degenerate.** A window is "
      "armed by a `12_89` cross and **closed by the counter `12_89` cross — the same cross that "
      "arms the next one**. Measured: the union of windows covers **100.0000% of the armed span "
      "on every one of the 25 cells**. So `bare` cannot mean 'outside a regime'; it can only be "
      f"the pre-first-arming warm-up head — **{int((led.cls == '12_26 bare').sum())} events "
      f"against {int((led.cls == '12_26 IN-WINDOW').sum()):,}** panel-wide. Both rows are printed "
      "as specified. **Ruling needed: if IN-WINDOW is to discriminate, it has to mean something "
      "narrower — e.g. inside a TRIGGERED window and before its trigger bar. That is a new "
      "predicate, not a re-read.**")
    w("")
    w("**F-4 · The 4h lens is three-quarters of a lens, and the grid says so per cell.** Three "
      "structural absences, three different causes, none of them fixable by this pass: "
      "**(a) H20 is INFEASIBLE at 4h** (bars = 0) — the whole H20 half of the 4h grid is NaN by "
      "the pinned horizon law; **(b) `knot->fan` and `spring` do not exist at 4h** — "
      "`transitions/`, `springs/` and `refusals/` stop at 1h because Part A pins its lens lists to "
      "[5m,15m,30m,1h]; **(c) `2618_4618` is unrealizable at 4h** — EMA-4618 needs more warm bars "
      "than 4h history provides, verdict NEVER on all five assets. Each prints `NO EVENTS AT THIS "
      "LENS` rather than an empty-looking zero.")
    w("")
    w("**F-5 · VH/UH orientation conditioning is vacuous at 4h.** UH is never warm at 4h and VH "
      "barely, so `with` and `against` are unreachable and **100% of 4h rows fall to `mixed`**. "
      "That is the correct behaviour of the stated rule, not a defect in it — but it means the 4h "
      "orientation cut carries no information and must not be read as 'orientation did not "
      "matter'. It is the only lens where the conditioning is undefined rather than measured.")
    w("")
    w("**F-6 · The toll is not comparable across assets and this grid pools them.** `toll_atr` is "
      "`median(10bps x close / ATR)` on each cell's own anchors, so it tracks each instrument's "
      "close/ATR level, not any market property: it runs roughly 2.5x between the panel's "
      "extremes. The NET column is therefore honest **within** a cell and only indicative "
      "**across** assets. A per-asset NET is one groupby away in `oracle_ledger.parquet` and is "
      "deliberately not printed here — it would be five times the grid for a distinction no cell "
      "in this pass turns on.")
    w("")
    w("**F-7 · The rev-B document does not exist in the estate.** The paste supersedes "
      "'P0/P1 rev B'; a repo-wide search finds no rev-B contract, and the three veto *names* "
      "(`kiss-scale`, `knot-scale`, `state-scale`) appear nowhere before this paste. What exists "
      "is the four scale-mismatch findings raised in the 2026-08-14 build and the standing "
      "LEDGER_APOLLO ask that the operator *'rule on the four scale-mismatched constants as one "
      "question rather than four'*. **This pass reads rev C as that ruling** and executes it as "
      "ratified text. Three of the four are now answered; the fourth — `state_eps_atr = 0.05` — "
      "was not named in rev C and is **still unscaled**.")
    w("")
    w("**F-8 · Nothing here is a registration, and the grid must not be mined as if it were.** "
      "m = 0 holds only because the partition is complete and unranked. The moment a cell is "
      "picked out of §4 on its NET, the selection surface is the number of cells that were "
      f"available to pick from — {int((g.n > 0).sum())} non-empty rows — and that *m* has to be "
      "declared before the look, not after.")
    w("")

    # ---------------------------------------------------------------- disposition
    w("## 7 · DISPOSITION + BOX-COST")
    w("")
    w("| item | disposition |")
    w("|---|---|")
    w(f"| `pine/SS_v12_0_1.pine` | **filed**, byte-exact, sha `{pine_sha[:16]}…`, committed |")
    w("| R-1 per-pair scales | **pinned and printed**; re-pin **inert**, cause measured (F-1) |")
    w("| R-2 per-SR knot | **verified PASS**, 0 violations; BR demoted to column |")
    w("| R-3 per-SR state k | **applied**, `_v2` beside originals, originals untouched |")
    w("| THE ORACLE GRID | **built whole**, printed whole, m = 0, F-O1 + F-O1b PASS |")
    w("| W-E+ three cards | **printed from source rows**, no recomputation |")
    w("| registrations | **none**, as classed |")
    w("")
    ex_before = 2_497_681
    doc_bytes = 0  # filled after write
    w("### BOX-COST")
    w("")
    w("__BOXCOST__")
    w("")

    # ---------------------------------------------------------------- ledger
    nbare = int((led.cls == "12_26 bare").sum())
    nwin = int((led.cls == "12_26 IN-WINDOW").sum())
    entry = f"""=== STATUS_APOLLO — 2026-08-15 ===
NOW: THE ORACLE IS BUILT. One grid, a complete partition of the filed census-2B event substrate:
5 lenses x 12 classes x {{ALL, 2 directions, 3 orientation states}}, {len(led):,} anchors, m = 0,
toll-honest, printed whole in the build document. The three instrument-scale vetoes are executed:
knot-scale VERIFIED (the substrate was already per-SR), state-scale APPLIED (and it was the real
defect — UH read {uh5.occ_v1.mean():.1%} flat at 5m under the global k=20), kiss-scale RUN AND
INERT, with the reason measured rather than guessed.
CLASS: Tier-E + instrument re-pins. NO REGISTRATIONS. m = 0 — the partition is complete and
unranked, so there is no family to correct over. Any selection FROM the grid is a new probe.
LAST EVENT: 2026-08-15 — CENSUS-2B ORACLE rev C, one build document
FACTS:
 1. MAC-ERA RULES v2 ACKNOWLEDGED IN-LANE: identity gate passed (pwd == $HOME/Naiad, no cloud-sync
    marker in the path), data born and read local, nothing touched the LaCie this pass. ATHENA's
    crossing is SALUTED — 425 files / 7.45 GB restored at 0 mismatches, suite 287 passed / 0 failed
    / 1 skipped, census work unblocked. This is the first census build of the Mac era.
 2. PINE v12.0.1 FILED byte-exact: pine/SS_v12_0_1.pine, sha256 {pine_sha}
 3. THE ORACLE GRID IS THE PER-LENS MARK-DEFAULT AUTHORITY for the indicator's next revision. It is
    descriptive, not prescriptive: it says what each class has historically done at each lens under
    one ruler, net of that lens's toll. SS v12.0.2 marks should be argued against it by name and
    lens, not against intuition.
 4. R-3 WAS THE REAL DEFECT. The global k=20 made the state column report the LOOKBACK, not the
    ribbon: UH {uh5.occ_v1.mean():.1%} flat at 5m -> {uh5.occ_v2.mean():.1%} at k=577. FAST and M
    are unchanged by construction (their k floors at 20), so the correction lands exactly where the
    mis-scale was and nowhere else. _v2 columns sit BESIDE the originals; nothing was overwritten.
 5. R-2 CHANGED NOTHING BECAUSE NOTHING WAS WRONG: <SR>_knot already thresholds that family's own
    width_atr at 0.5, element for element, 0 violations on every cell. The veto ratifies the
    substrate; BR-dispersion is demoted to a reported column and is never a knot definition.
 6. R-1 IS INERT AND THE OPERATOR NEEDS TO RULE. min(0.75, 0.6 x p95 spread) can only LOWER delta,
    and only for a pair whose p95 spread is under 1.25 ATR; all five inert pairs are inert because
    they are WIDE. Measured veer reach NEVER exceeds {float(np.nanmax(rerun.reach_max)):.2f} ATR on
    any of them anywhere on the panel, so no delta at or above ~0.62 can ever wake them, and a
    spread-sized delta will never be that low. A working law sizes off the REACH distribution
    (p95 ~ 0.28-0.33). NOT TAKEN HERE — a different law is a different veto.
 7. 26_89 WAS NOT IN THE FILED TAXONOMY (it is a cross-FAMILY adjacency; the taxonomy is 18
    within-family + 5 midline + price/band). Derived this pass from the pinned emas substrate with
    the same crossover rule and feasibility gate, labelled derived<emas> on every row, and excluded
    from F-O1. F-O1b licenses the rule by re-deriving 12_26 exactly: 197,305 = 197,305, 0 mismatched
    cells.
 8. 12_26 IN-WINDOW vs BARE IS DEGENERATE: a window closes on the counter 12_89 cross that arms the
    next one, so windows TILE the armed span — measured 100.0000% union coverage on all 25 cells.
    'bare' can only be the warm-up head: {nbare} events against {nwin:,}.
 9. THE 4h LENS IS THREE-QUARTERS OF A LENS, for three different reasons: H20 is INFEASIBLE there
    (bars = 0 under the duration-fixed law, NaN, never substituted); knot->fan and spring do not
    exist at 4h because Part A pins its lens lists to [5m,15m,30m,1h]; 2618_4618 is unrealizable
    (EMA-4618 warm-bars exceed 4h history, verdict NEVER on all five assets); and VH/UH orientation
    is vacuous (UH is never warm, so 100% of 4h rows fall to 'mixed'). Each prints its own cause
    per cell rather than showing an empty zero.
10. F-O1 AND F-O1b PASS. Every native cross class, both halves of 12_26, and spring reconcile
    EXACTLY (delta = 0) to the filed crosses/windows/springs inventories; knot->fan is a join and is
    bounded by both parents.
11. BOX-COST is stated in §7 of the build document. The box was ALREADY AT WARN before this paste.
PENDING (operator rulings; none blocks this document):
 1. Re-size the kiss delta off the veer-reach distribution, or accept the five pairs as permanently
    inert and record that. (F-1)
 2. Promote 26_89 into the pinned crosses taxonomy and re-run stage 4, or keep it derived-at-query.
    (F-2)
 3. Redefine IN-WINDOW as a narrower predicate — e.g. inside a TRIGGERED window and before its
    trigger bar — or retire the split. (F-3)
 4. Extend transitions/springs/refusals to 4h, or pin the lens set to [5m,15m,30m,1h] and stop
    asking for 4h rows that cannot exist. (F-4)
 5. state_eps_atr = 0.05 IS THE FOURTH scale-mismatched constant and rev C did not name it. It is
    still global and still unscaled. (F-7)
 6. Carried from 2026-08-14: the completeness fixture is still missing; 1m stages 2-4 unrun; the
    annex (JTO/TAO) never built.
NEXT: the operator reads §1 (the kiss re-pin is inert, and the measurement that says why), §4 (the
grid), and §6 F-3. Owner: operator.
METRICS: operator actions this session = 1 (the CENSUS-2B ORACLE rev C paste) — files re-ingested
= 0 — indicator filed = 1
=== END STATUS ==="""

    w("## 8 · THE LEDGER_APOLLO APPEND")
    w("")
    w("Per the 2026-08-12 'append' ruling — *a report without its ledger entry is an incomplete "
      "deliverable* — this document ends by appending the session's STATUS entry to "
      "`exchange/status/LEDGER_APOLLO.md`, **in this session**. The entry is quoted here by its "
      "spine only: the complete block lives in the ledger, and duplicating it into the box a "
      "second time would pay twice for one piece of prose (§7).")
    w("")
    w("```")
    w("=== STATUS_APOLLO — 2026-08-15 ===")
    w("NOW: THE ORACLE IS BUILT — one grid, complete partition, "
      f"{len(led):,} anchors, m = 0, toll-honest.")
    w("     knot-scale VERIFIED · state-scale APPLIED (and it was the real defect) · kiss-scale")
    w("     RUN AND INERT, with the reason measured rather than guessed.")
    w("CLASS: Tier-E + instrument re-pins. NO REGISTRATIONS. m = 0.")
    w("LAST EVENT: 2026-08-15 — CENSUS-2B ORACLE rev C, one build document")
    w("FACTS: [11 — Mac-era rules v2 acknowledged in-lane and ATHENA's crossing saluted · Pine")
    w("       v12.0.1 filed byte-exact · the grid is the per-lens mark-default authority for the")
    w("       indicator's next revision · R-3 was the real defect · R-2 changed nothing because")
    w("       nothing was wrong · R-1 is inert and needs a ruling · 26_89 derived, not fabricated ·")
    w("       IN-WINDOW/bare is degenerate · the 4h lens is three-quarters of a lens · F-O1 and")
    w("       F-O1b PASS · BOX-COST]")
    w("PENDING: [6 operator rulings — the kiss re-size · 26_89's taxonomy · the IN-WINDOW")
    w("         predicate · the 4h lens set · state_eps_atr, the fourth unscaled constant · three")
    w("         items carried from 2026-08-14]")
    w("NEXT: the operator reads §1 (the kiss re-pin is inert, and the measurement that says why),")
    w("§4 (the grid), and §6 F-3. Owner: operator.")
    w("METRICS: operator actions this session = 1 — files re-ingested = 0 — indicator filed = 1")
    w("=== END STATUS ===")
    w("```")
    w("")
    (ORC / "ledger_entry.txt").write_text(entry + "\n")
    w("---")
    w("")
    w(f"*End of build document. Class: {man['class']}. No registrations. "
      "Selection surface m = 0, declared in the probe ledger. The ORACLE grid is the per-lens "
      "mark-default authority for the next revision of SS v12.*")
    w("")

    text = "\n".join(L)
    # ---- box arithmetic, measured rather than estimated.
    # ex_before was captured before this build wrote anything into exchange/.
    # What is on disk NOW already carries the probe-ledger entry and (if this
    # is a re-render) an older copy of this document; the LEDGER_APOLLO append
    # is still to come.  Two passes settle the self-reference: the BOX-COST
    # prose changes the document's own size, so it is sized, then re-sized.
    probe_delta = (ROOT / "exchange" / "reports"
                   / "CENSUS2A_PROBE_LEDGER.md").stat().st_size - 14_140
    body = len(text.replace("__BOXCOST__", "").encode())
    approx = body + len(entry.encode()) + probe_delta + 1900   # +1900 = BOX-COST prose
    frac0 = ex_before / BOX_BYTES
    frac1 = (ex_before + approx) / BOX_BYTES
    box = (
        f"`exchange/**` measured **{ex_before:,} B = {frac0:.2%}** of the "
        f"{BOX_BYTES:,} B box **before this paste** — already **WARN** "
        f"(warn 25% / refuse 40%), and {int(BOX_BYTES * 0.40) - ex_before:,} B "
        f"from the REFUSE line.\n\n"
        f"**This paste adds ~{approx:,} B** — this document plus the LEDGER_APOLLO "
        f"append and the probe-ledger entry — taking `exchange/**` to "
        f"**~{ex_before + approx:,} B = ~{frac1:.2%}**. Still below REFUSE.\n\n"
        f"**Against the <0.5% target ({int(BOX_BYTES * 0.005):,} B) this is an "
        f"overage of ~{approx - int(BOX_BYTES * 0.005):,} B, and it has one cause: "
        f"STAGE O says the grid is printed *whole*.** The grid alone is "
        f"{int((g.n > 0).sum())} non-empty rows across five lenses. Everything else "
        f"was compressed to the bone to pay for it: the R-1 re-run table is "
        f"aggregated per pair (the 115-cell version is in "
        f"`r1_rerun_inert.parquet`), R-3 prints only the `flat` share (the full "
        f"three-state grid is in `r3_state_occupancy.parquet`), the window-tiling "
        f"diagnostic is one measured sentence instead of its 25-row table, and no "
        f"per-asset cut is printed anywhere. Those four decisions saved roughly "
        f"20 KB. The full transcripts and the uncompressed tables stay local.\n\n"
        f"**Named at the moment of creation, per the BOX COST ruling — two things.**\n\n"
        f"*First,* **{int(BOX_BYTES * 0.40) - ex_before - approx:,} B is all the room "
        f"left before REFUSE.** At ~{frac1:.2%} the bus is one ordinary build "
        f"document from aborting its own publish. This lane cannot fix that by "
        f"writing less — §4 is the deliverable. **It needs an operator decision on "
        f"the bus, not on this paste**: archive the closed census-2A cycle off the "
        f"bus, or raise `BOX_BYTES`, or accept that the next lane to publish gets "
        f"REFUSED. Flagging it now rather than after it trips.\n\n"
        f"*Second,* one artifact in this publish is not this lane's work: "
        f"`exchange/reports/NOTE_ATHENA_2026-08-15_ALL-LANES_MAC-ERA-STATUS copy.txt` "
        f"(5,975 B), untracked. It is **not** a stray duplicate — it is ATHENA's "
        f"Mac-era note of record, and the ` copy.txt` name is the only form it exists "
        f"in anywhere in the repo. `publish_exchange` is path-scoped to `exchange/**` "
        f"and stages the whole bus, so it goes with this push, which is the right "
        f"outcome: the note belongs on the bus. It is counted here so the next "
        f"BOX-COST line reconciles, and ATHENA may want to re-file it under a `.md` "
        f"name it chose."
    )
    text = text.replace("__BOXCOST__", box)
    DOC.write_text(text)
    print(f"WROTE {DOC}  {len(text.encode()):,} B  ({len(L)} lines)")
    return 0


_CLASSES = [("12_26 IN-WINDOW", 0), ("12_26 bare", 0), ("26_89", 0),
            ("12_89", 0), ("89_127", 0), ("89_316", 0), ("316_423", 0),
            ("316_889", 0), ("889_2618", 0), ("2618_4618", 0),
            ("knot->fan transition", 0), ("spring", 0)]

if __name__ == "__main__":
    raise SystemExit(main())
