"""TC6-V · THE THREE RIDERS — the supplement, L-LAG, and query_filter v1.

RATIFIED operator 2026-08-17.  CLASS: audit completion — measurement only, NO NEW
CLAIMS.  Nothing here registers anything, nothing here gates anything, and every
table says so on its face.

    (i)   THE SUPPLEMENT   per-trade grouped tables over the v6 book: an
                           MAE-decile x MFE-decile cross-tab, by exit mechanism,
                           by asset, by year, winners and losers separately —
                           HTML beside the report and parquet beside the book.
    (ii)  L-LAG            the arm -> trigger gap per campaign, in BARS and in
                           ATR-TIME: distributions by year and asset, OUTCOME BY
                           LAG DECILE, plus the trigger -> +1R lag and the ride's
                           pivot cadence.
    (iii) query_filter v1  a predicate DSL over a named feature table, emitting
                           the estate's standard paired table with the D15 trio.
                           EVERY INVOCATION LOGS ITS m TO A PROBE LEDGER.

────────────────────────────────────────────────────────────────────────────
TWO EXCURSION COLUMNS, BECAUSE ONE OF THEM IS THE CARD'S OWN STOP
────────────────────────────────────────────────────────────────────────────
A campaign's realised adverse excursion cannot exceed its stop by much, because
the stop ends the campaign — the entry rail is 1.0 ATR = 1R, so a distribution of
realised MAE is CENSORED at about -1R BY CONSTRUCTION and its upper deciles
report the card's own rail rather than the market's behaviour.

So every excursion in this module is published TWICE:

    mae_held_r   what the campaign ENDURED — bars entry+1..exit, with the exit
                 bar clipped to the exit price when the exit was a stop. Once
                 the stop is taken you are out, and the rest of that bar is not
                 your excursion.
    mae_tape_r   the raw bar extremes over the SAME bars, unclipped — what the
                 market did, including the gap through the stop.

They differ by exactly the gap-through, and printing both is the only way a
reader can tell a market statistic from a stop statistic.  Named because the
audit that commissioned this module asked whether any published AE number was
the rail wearing a distribution's clothes.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import tierc6 as T6                                                  # noqa: E402
import tierc6_rules as RC                                            # noqa: E402

iso, r4, r6, pct = T6.iso, T6.r4, T6.r6, T6.pct
MS_4H = T6.MS_4H

OUT = ROOT / "research_outputs" / "tc6v"
HTML = ROOT / "research_outputs" / "tc6v" / "SUPPLEMENT.html"

# THE PROBE LEDGER — every query_filter invocation, with its m.
PROBE_LEDGER: list[dict] = []


# ═══════════════════════════════════════════════ the two excursion readings
def excursions(t) -> tuple[float, float, float]:
    """(mae_held_r, mae_tape_r, mfe_r) for one campaign, from raw 4h bars.

    HELD clips the EXIT bar at the exit price when the exit was a stop; TAPE
    does not.  Both scan bars entry+1 .. exit, which is exactly the range the
    ride scans — a campaign entered at a close owns no part of its entry bar.

    WHAT WOULD MAKE THIS WRONG: including the entry bar (the entry is a close,
    so that bar is over), scanning past the exit, or clipping the tape reading
    (which would make the two columns identical and the comparison pointless).
    """
    f = T6.frame(t.symbol)["f"]
    d, e, R = t.direction, float(t.entry_px), float(t.r_dist)
    lo, hi = t.entry_i + 1, t.exit_i
    if hi < lo:
        return 0.0, 0.0, 0.0
    adv = f.l[lo:hi + 1] if d == 1 else f.h[lo:hi + 1]
    fav = f.h[lo:hi + 1] if d == 1 else f.l[lo:hi + 1]
    tape = float(np.min((adv - e) * d)) / R
    held = tape
    if t.exit_reason == "stop" and hi >= lo:
        adv_h = np.array(adv, dtype=float, copy=True)
        adv_h[-1] = float(t.exit_px)           # the stop took the bar, not its low
        held = float(np.min((adv_h - e) * d)) / R
    mfe = float(np.max((fav - e) * d)) / R
    return r6(min(held, 0.0)), r6(min(tape, 0.0)), r6(max(mfe, 0.0))


def campaign_features(book: list) -> pd.DataFrame:
    """ONE ROW PER CAMPAIGN, every column query_filter may filter on.

    This is the table the DSL is defined OVER, and naming it is the point: a
    predicate language whose vocabulary is "whatever columns happen to exist"
    is a language nobody can pre-register a claim in.
    """
    import tierc6_lab_zec as Z
    rows = []
    for t in book:
        f = T6.frame(t.symbol)["f"]
        held, tape, mfe = excursions(t)
        # ATR-TIME — the estate's own definition, bound not reimplemented.
        at_arm_entry = Z.atr_time(t.symbol, t.arm_i, t.entry_i)
        # trigger -> +1R, in bars, from raw bars
        j1 = None
        for j in range(t.entry_i + 1, t.exit_i + 1):
            fv = float(f.h[j]) if t.direction == 1 else float(f.l[j])
            if (fv - t.entry_px) * t.direction / t.r_dist >= 1.0:
                j1 = j
                break
        adv = list(t.advances)
        rows.append({
            "campaign_id": f"{t.symbol}:{t.lane}:{iso(t.entry_ms)[:13].replace('-','').replace('T','T')}",
            "asset": t.symbol, "lane": t.lane,
            "direction": "long" if t.direction == 1 else "short",
            "year": iso(t.entry_ms)[:4],
            "arm_ts": iso(t.arm_ms), "entry_ts": iso(t.entry_ms),
            "exit_ts": iso(t.exit_ms), "exit_reason": t.exit_reason,
            "entry_ms": int(t.entry_ms),
            # ── the lag family [L-LAG] ───────────────────────────────────
            "lag_arm_to_entry_bars": int(t.entry_i - t.arm_i),
            "lag_arm_to_entry_atr_time": r6(at_arm_entry),
            "lag_entry_to_1r_bars": (int(j1 - t.entry_i) if j1 is not None
                                     else None),
            "reached_1r": bool(t.reached_1r),
            "bars_held": int(t.bars_held),
            "pivot_cadence_bars": (r4((t.exit_i - t.entry_i) / len(adv))
                                   if adv else None),
            "n_advances": len(adv),
            # ── the excursion family, BOTH readings ──────────────────────
            "mae_held_r": held, "mae_tape_r": tape, "mfe_r": mfe,
            "gap_through_r": r6(held - tape),
            # ── context ──────────────────────────────────────────────────
            "disp_at_arming": r6(float(t.disp_at_arming)),
            "atr_at_entry": r6(float(t.atr_at_entry)),
            "r_dist": r6(float(t.r_dist)),
            "r_pct_of_price": r6(100.0 * float(t.r_dist) / float(t.entry_px)),
            "harvested": bool(t.harvested),
            # ── outcome ──────────────────────────────────────────────────
            "net_r": r6(float(t.net_r)), "winner": bool(t.net_r > 0),
        })
    d = pd.DataFrame(rows)
    for c, n in (("disp_at_arming", "disp_decile"),
                 ("lag_arm_to_entry_bars", "lag_decile"),
                 ("mae_held_r", "mae_decile"), ("mfe_r", "mfe_decile")):
        d[n] = _decile(d[c])
    return d.sort_values(["asset", "entry_ms"]).reset_index(drop=True)


def _decile(sr: pd.Series) -> list:
    """Deciles by RANK, ties shared — `qcut` on a column with heavy ties (the
    MFE of every losing campaign is 0) raises or silently drops rows, and a
    decile table that quietly lost its losers would be the whole finding."""
    v = pd.to_numeric(sr, errors="coerce")
    r = v.rank(method="average", pct=True)
    return [None if pd.isna(x) else int(min(9, np.floor(x * 10))) for x in r]


# ═════════════════════════════════════════════════════ (i) THE SUPPLEMENT
def _grp(d: pd.DataFrame, by: list[str], label: str) -> pd.DataFrame:
    g = d.groupby(by, dropna=False)
    out = g.agg(n=("net_r", "size"), net_r=("net_r", "sum"),
                expectancy_r=("net_r", "mean"),
                win_rate_pct=("winner", "mean"),
                mean_mae_held_r=("mae_held_r", "mean"),
                mean_mae_tape_r=("mae_tape_r", "mean"),
                mean_mfe_r=("mfe_r", "mean"),
                mean_bars_held=("bars_held", "mean"),
                reached_1r_pct=("reached_1r", "mean")).reset_index()
    out["win_rate_pct"] = (100.0 * out["win_rate_pct"]).round(4)
    out["reached_1r_pct"] = (100.0 * out["reached_1r_pct"]).round(4)
    for c in ("net_r", "expectancy_r", "mean_mae_held_r", "mean_mae_tape_r",
              "mean_mfe_r", "mean_bars_held"):
        out[c] = out[c].astype(float).round(6)
    out.insert(0, "cut", label)
    out["provisional"] = out["n"] < RC.PROVISIONAL_MIN_N
    out["tier"] = "E — measurement, gates nothing"
    return out


def supplement(feat: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """THE PER-TRADE GROUPED TABLES, and the losers are never dropped."""
    cuts = []
    cuts.append(_grp(feat, ["mae_decile", "mfe_decile"], "MAE x MFE decile"))
    cuts.append(_grp(feat, ["exit_reason"], "exit mechanism"))
    cuts.append(_grp(feat, ["asset"], "asset"))
    cuts.append(_grp(feat, ["year"], "year"))
    cuts.append(_grp(feat, ["direction"], "direction"))
    cuts.append(_grp(feat[feat["winner"]], ["asset"], "WINNERS by asset"))
    cuts.append(_grp(feat[~feat["winner"]], ["asset"], "LOSERS by asset"))
    cuts.append(_grp(feat[feat["winner"]], ["year"], "WINNERS by year"))
    cuts.append(_grp(feat[~feat["winner"]], ["year"], "LOSERS by year"))
    allc = pd.concat(cuts, ignore_index=True)
    # THE CROSS-TAB, as a genuine matrix rather than a long frame
    x = (feat.pivot_table(index="mae_decile", columns="mfe_decile",
                          values="net_r", aggfunc="sum", fill_value=0.0)
         .round(4).reset_index())
    xn = (feat.pivot_table(index="mae_decile", columns="mfe_decile",
                           values="net_r", aggfunc="size", fill_value=0)
          .reset_index())
    return {"supplement_cuts": allc, "supplement_xtab_net_r": x,
            "supplement_xtab_n": xn}


def supplement_html(tabs: dict[str, pd.DataFrame], feat: pd.DataFrame) -> str:
    css = ("body{font:13px/1.5 -apple-system,BlinkMacSystemFont,Segoe UI,sans-serif;"
           "margin:0;padding:32px;background:#0f1115;color:#e6e6e6}"
           "h1{font-size:20px;margin:0 0 4px}h2{font-size:15px;margin:28px 0 8px;"
           "color:#8ab4f8;border-bottom:1px solid #2a2f3a;padding-bottom:4px}"
           "p.note{color:#9aa0aa;margin:4px 0 18px;max-width:70em}"
           "table{border-collapse:collapse;margin:0 0 8px;font-size:12px}"
           "th,td{border:1px solid #262b35;padding:3px 8px;text-align:right}"
           "th{background:#1a1f28;color:#c9d1d9;text-align:left}"
           "td:first-child,th:first-child{text-align:left}"
           "tr:nth-child(even) td{background:#141821}"
           ".neg{color:#f28b82}.pos{color:#81c995}"
           ".wrap{overflow-x:auto;max-width:100%}")

    def tbl(df, n=400):
        d = df.head(n)
        h = "".join(f"<th>{c}</th>" for c in d.columns)
        rows = []
        for _, r in d.iterrows():
            tds = []
            for c in d.columns:
                v = r[c]
                cls = ""
                if isinstance(v, (int, float, np.floating)) and not pd.isna(v):
                    if c in ("net_r", "expectancy_r") and v < 0:
                        cls = ' class="neg"'
                    elif c in ("net_r", "expectancy_r") and v > 0:
                        cls = ' class="pos"'
                    v = f"{v:,.4f}" if isinstance(v, float) else f"{v:,}"
                tds.append(f"<td{cls}>{'' if pd.isna(r[c]) else v}</td>")
            rows.append("<tr>" + "".join(tds) + "</tr>")
        return (f'<div class="wrap"><table><tr>{h}</tr>'
                + "".join(rows) + "</table></div>")

    parts = [f"<style>{css}</style>",
             "<h1>TC6-V · THE SUPPLEMENT — every v6 campaign, grouped</h1>",
             '<p class="note">Tier-E measurement. Nothing here registers or '
             'gates anything. <b>Every adverse excursion is printed twice</b>: '
             '<code>mae_held_r</code> is what the campaign endured, with the '
             'exit bar clipped at the stop; <code>mae_tape_r</code> is the raw '
             'bar extreme over the same bars. They differ by the gap-through, '
             'and the difference is the only way to tell a market statistic '
             "from the card's own 1R rail.</p>"]
    parts.append("<h2>MAE-decile × MFE-decile — net R</h2>")
    parts.append(tbl(tabs["supplement_xtab_net_r"]))
    parts.append("<h2>MAE-decile × MFE-decile — campaign count</h2>")
    parts.append(tbl(tabs["supplement_xtab_n"]))
    for lab in ("exit mechanism", "asset", "year", "direction",
                "WINNERS by asset", "LOSERS by asset",
                "WINNERS by year", "LOSERS by year", "MAE x MFE decile"):
        d = tabs["supplement_cuts"]
        d = d[d["cut"] == lab]
        if len(d):
            parts.append(f"<h2>{lab}</h2>")
            parts.append(tbl(d.drop(columns=["cut"])))
    parts.append(f'<p class="note">{len(feat)} campaigns · '
                 f'{int(feat["winner"].sum())} winners · '
                 f'net {feat["net_r"].sum():+.4f} R</p>')
    return "\n".join(parts)


# ═══════════════════════════════════════════════════════════════ (ii) L-LAG
def l_lag(feat: pd.DataFrame) -> pd.DataFrame:
    """THE ARM -> TRIGGER GAP, and what it costs.

    Reported by year, by asset, and BY LAG DECILE with the outcome attached —
    the last is the one with content: if a long wait predicts a worse campaign,
    the card has a cheap filter available and this table is where it shows.

    WHAT WOULD MAKE THIS WRONG: measuring the lag from the trigger rather than
    the arming (it would be zero by construction), or dropping campaigns with
    no +1R (they are the losers, and a lag study that loses its losers measures
    nothing).
    """
    out = []
    for by, lab in ((["year"], "lag by year"), (["asset"], "lag by asset"),
                    (["lag_decile"], "OUTCOME BY LAG DECILE"),
                    (["direction"], "lag by direction")):
        g = feat.groupby(by, dropna=False)
        d = g.agg(n=("net_r", "size"),
                  lag_bars_median=("lag_arm_to_entry_bars", "median"),
                  lag_bars_p90=("lag_arm_to_entry_bars",
                                lambda s: float(np.percentile(s, 90))),
                  lag_atr_time_median=("lag_arm_to_entry_atr_time", "median"),
                  entry_to_1r_bars_median=("lag_entry_to_1r_bars", "median"),
                  pivot_cadence_median=("pivot_cadence_bars", "median"),
                  net_r=("net_r", "sum"), expectancy_r=("net_r", "mean"),
                  win_rate_pct=("winner", "mean"),
                  reached_1r_pct=("reached_1r", "mean")).reset_index()
        d["win_rate_pct"] = (100.0 * d["win_rate_pct"]).round(4)
        d["reached_1r_pct"] = (100.0 * d["reached_1r_pct"]).round(4)
        d.insert(0, "cut", lab)
        out.append(d)
    d = pd.concat(out, ignore_index=True)
    d["provisional"] = d["n"] < RC.PROVISIONAL_MIN_N
    d["tier"] = "E — measurement, gates nothing"
    for c in d.columns:
        if d[c].dtype.kind == "f":
            d[c] = d[c].round(6)
    return d


def l_lag_gate_evidence(feat: pd.DataFrame) -> dict:
    """P-LAG-1's CONDITION, EVALUATED — and the condition adjudicates itself.

    The commission registers P-LAG-1 only IF the top-versus-bottom lag-decile
    median delta excludes zero at cluster-90%.  This computes exactly that, on
    the asset-cluster bootstrap the estate already uses, and returns the verdict
    so the build document can state it either way without a second look.
    """
    # THRESHOLDS, NOT DECILE LABELS — the lag column is MASSIVELY TIED.
    # 49 of 195 campaigns trigger on the arming bar itself (lag 0), so under
    # average-rank the whole tie block lands in decile 1 and DECILE 0 IS EMPTY.
    # A gate that asked for `lag_decile == 0` was unevaluable for a reason that
    # has nothing to do with the question — and would have silently reported
    # "condition not met", which is the wrong answer rather than no answer.
    # The comparison is therefore bottom-decile-BY-VALUE against top-decile-by
    # -value, with the tie structure printed so the reader can see why the two
    # groups are not the same size.
    v = feat["lag_arm_to_entry_bars"].astype(float)
    q10, q90 = float(np.percentile(v, 10)), float(np.percentile(v, 90))
    bot = feat[v <= q10]
    top = feat[v >= q90]
    if not len(top) or not len(bot):
        return {"evaluable": False, "reason": "a lag group is empty"}
    dr = T6.cluster_boot_diff(list(bot["net_r"].astype(float)),
                              list(bot["asset"]),
                              list(top["net_r"].astype(float)),
                              list(top["asset"]))
    pt = float(bot["net_r"].mean() - top["net_r"].mean())
    ci = T6._ci_from(dr, pt)
    excl = bool(ci["lo"] is not None and (ci["lo"] > 0 or ci["hi"] < 0))
    return {"evaluable": True,
            "threshold_bottom_lag_bars_le": q10,
            "threshold_top_lag_bars_ge": q90,
            "ties_at_lag_zero": int((v == 0).sum()),
            "bottom_decile_n": len(bot), "top_decile_n": len(top),
            "bottom_median_lag_bars": float(bot["lag_arm_to_entry_bars"].median()),
            "top_median_lag_bars": float(top["lag_arm_to_entry_bars"].median()),
            "bottom_expectancy_r": r6(float(bot["net_r"].mean())),
            "top_expectancy_r": r6(float(top["net_r"].mean())),
            "delta_point": r6(pt), "ci_lo": r6(ci["lo"]), "ci_hi": r6(ci["hi"]),
            "p_one_sided": r6(ci["p_one_sided"]),
            "excludes_zero": excl,
            "verdict": ("REGISTER P-LAG-1 — the condition is met"
                        if excl else
                        "REPORT-ONLY — the condition is NOT met, no "
                        "registration, m unchanged")}


# ══════════════════════════════════════════════════════ (iii) query_filter v1
class QueryFilterError(ValueError):
    pass


def query_filter(feat: pd.DataFrame, predicate: str, base: pd.DataFrame | None = None,
                 note: str = "") -> pd.DataFrame:
    """THE PREDICATE DSL — one predicate string over the named feature table.

    THE VOCABULARY IS THE FEATURE TABLE'S COLUMNS AND NOTHING ELSE.  A predicate
    naming a column that does not exist RAISES rather than returning an empty
    selection, because a silent empty is indistinguishable from a true negative
    and this estate has already lost a fixture to a check that could not fail.

    THE m IS LOGGED ON EVERY INVOCATION.  A filter language is a selection
    surface with no natural size — you can always try one more predicate — so
    the probe ledger counts them and the count travels with the build. A probe
    that is not on the ledger did not happen.

    WHAT WOULD MAKE THIS WRONG: evaluating with `eval` over arbitrary Python
    (it would let a predicate reach the outcome columns' future), silently
    returning empty on a typo, or emitting a table without the D15 trio — the
    trio is what stops a selected subset from being read as a result.
    """
    if not isinstance(predicate, str) or not predicate.strip():
        raise QueryFilterError("empty predicate")
    allowed = set(feat.columns)
    import re
    # STRING LITERALS ARE VALUES, NOT NAMES.  The first draft extracted
    # identifiers from the raw predicate, so `direction == 'short'` was rejected
    # because `short` is not a column — the validator was reading the DATA as
    # vocabulary. Quoted spans are stripped before the scan; the strictness is
    # kept, it just stops firing on the one thing a predicate is FOR.
    scan = re.sub(r"'[^']*'|\"[^\"]*\"", " ", predicate)
    names = set(re.findall(r"[A-Za-z_][A-Za-z_0-9]*", scan))
    kw = {"and", "or", "not", "True", "False", "None", "in", "abs"}
    unknown = sorted(n for n in names - kw - allowed
                     if not n.isdigit() and n not in ("index",))
    if unknown:
        raise QueryFilterError(
            f"predicate names column(s) the feature table does not have: "
            f"{unknown}. The vocabulary is {sorted(allowed)}")
    sel = feat.query(predicate, engine="python")
    b = feat if base is None else base
    rows = []
    for lab, d in (("SELECTED", sel), ("BASE (all campaigns)", b)):
        rs = d["net_r"].astype(float)
        rows.append({
            "predicate": predicate, "arm": lab, "n": len(d),
            "net_r": r4(float(rs.sum())) if len(d) else None,
            "expectancy_r": r6(float(rs.mean())) if len(d) else None,
            "win_rate_pct": pct(int((rs > 0).sum()), len(d)),
            "mean_mae_held_r": r6(float(d["mae_held_r"].astype(float).mean()))
            if len(d) else None,
            "mean_mfe_r": r6(float(d["mfe_r"].astype(float).mean()))
            if len(d) else None,
        })
    out = pd.DataFrame(rows)
    # THE D15 TRIO — paired against the base, on the campaigns the two share.
    key = ["campaign_id"]
    j = sel.merge(b[key + ["net_r"]], on=key, suffixes=("", "_base"))
    dv = (j["net_r"].astype(float) - j["net_r_base"].astype(float))
    tot = float(np.abs(dv).sum())
    out["d15_paired_delta_expectancy_r"] = r6(float(dv.mean())) if len(dv) else None
    out["d15_n_paired"] = len(dv)
    out["d15_max_single_trade_delta_share"] = (
        r6(float(np.abs(dv).max()) / tot) if tot > 1e-12 else None)
    bs = b["net_r"].astype(float)
    kb = max(int(np.floor(0.10 * len(bs))), 1) if len(bs) else 1
    ks = max(int(np.floor(0.10 * len(rs))), 1) if len(sel) else 1
    top_b = float(np.sort(bs)[::-1][:kb].sum()) if len(bs) else 0.0
    top_s = (float(np.sort(sel["net_r"].astype(float))[::-1][:ks].sum())
             if len(sel) else 0.0)
    out["d15_tail_exit_ratio"] = (r6(top_s / top_b) if abs(top_b) > 1e-12
                                  else None)
    out["d15_gates_nothing"] = True
    out["provisional"] = out["n"] < RC.PROVISIONAL_MIN_N
    out["tier"] = "E — a SELECTION, not a result"
    out["note"] = note
    PROBE_LEDGER.append({"probe_seq": len(PROBE_LEDGER) + 1,
                         "predicate": predicate, "n_selected": len(sel),
                         "note": note})
    out["probe_seq"] = len(PROBE_LEDGER)
    out["m_probes_run_so_far"] = len(PROBE_LEDGER)
    return out


def probe_ledger() -> pd.DataFrame:
    d = pd.DataFrame(PROBE_LEDGER)
    if not len(d):
        return d
    d["m_total"] = len(PROBE_LEDGER)
    d["note_on_m"] = (
        f"m = {len(PROBE_LEDGER)} predicates were evaluated in this build. A "
        f"filter language has no natural family size — you can always try one "
        f"more — so the count is kept HERE and travels with the build. Nothing "
        f"in this rider is registered; if a predicate is ever promoted to a "
        f"registration, this m is where its correction starts.")
    return d


# ════════════════════════════════════════════════════════════════ the driver
def run(root: Path = OUT) -> dict:
    root.mkdir(parents=True, exist_ok=True)
    man: dict = {"stage": "TC6-V riders", "sha": {}, "counts": {}}
    lo, hi, cmeta = T6.corridor()
    book = T6.run_cell(RC.CARD_V6, lo, hi)
    feat = campaign_features(book)
    T6.log(f"  FEATURES {len(feat)} campaigns x {len(feat.columns)} columns")

    def put(df, name, key):
        if df is None or not len(df):
            T6.log(f"    (skip {name} — empty)")
            return
        df = df.copy()
        df.attrs = {}
        df.columns = [str(c) for c in df.columns]
        man["sha"][name] = T6.write_table(df, name, key, root)

    put(feat, "campaign_features", ["campaign_id"])
    tabs = supplement(feat)
    put(tabs["supplement_cuts"], "supplement_cuts",
        ["cut", "mae_decile", "mfe_decile", "exit_reason", "asset", "year",
         "direction"] if False else ["cut", "n", "net_r", "expectancy_r"])
    put(tabs["supplement_xtab_net_r"], "supplement_xtab_net_r", ["mae_decile"])
    put(tabs["supplement_xtab_n"], "supplement_xtab_n", ["mae_decile"])
    put(l_lag(feat), "l_lag", ["cut", "n", "net_r"])

    gate = l_lag_gate_evidence(feat)
    man["p_lag_1_condition"] = gate
    T6.log(f"  P-LAG-1 CONDITION: {gate.get('verdict')}")

    # THREE PREDICATES, so the DSL ships exercised and F-QF has something to
    # hand-verify against direct pandas.
    probes = [
        ("lag_arm_to_entry_bars <= 2", "the fastest triggers"),
        ("mae_held_r >= -0.30", "campaigns that were never deeply under water"),
        ("disp_decile >= 7 and direction == 'short'",
         "high-displacement shorts"),
    ]
    pr = [query_filter(feat, p, note=n) for p, n in probes]
    put(pd.concat(pr, ignore_index=True), "query_filter_probes",
        ["probe_seq", "arm"])
    put(probe_ledger(), "probe_ledger", ["probe_seq"])

    HTML.parent.mkdir(parents=True, exist_ok=True)
    HTML.write_text(supplement_html(tabs, feat))
    man["html"] = str(HTML)
    man["counts"] = {
        "campaigns": len(feat), "winners": int(feat["winner"].sum()),
        "net_r": r4(float(feat["net_r"].sum())),
        "mean_mae_held_r": r6(float(feat["mae_held_r"].mean())),
        "mean_mae_tape_r": r6(float(feat["mae_tape_r"].mean())),
        # `gap_through_r` = held - tape, and HELD is the LESS negative of the
        # two (the stop clips the exit bar), so the gap is POSITIVE. The first
        # draft counted `< -1e-9` and reported zero on every book — a counter
        # looking for the wrong sign, which reads as "no campaign ever gapped
        # through its stop" when in fact 120 of 196 tape excursions run past
        # -0.95R against 110 held.
        "campaigns_with_gap_through": int((feat["gap_through_r"] > 1e-9).sum()),
        "mae_held_at_the_rail_n": int((feat["mae_held_r"] <= -0.95).sum()),
        "mae_tape_beyond_the_rail_n": int((feat["mae_tape_r"] <= -0.95).sum()),
        "worst_tape_excursion_r": r6(float(feat["mae_tape_r"].min())),
        "mae_held_is_censored_at_the_card_rail": (
            "the entry rail is 1.0 ATR = 1R, so a HELD excursion cannot pass "
            "-1R: min(mae_held_r) is exactly -1.0 and 110 of 196 campaigns sit "
            "at or past -0.95R. Any decile or hazard statistic built on HELD "
            "excursions reports the CARD'S STOP in its tail, not the market's "
            "behaviour. mae_tape_r is the uncensored reading and reaches "
            "-4.5891R. [TC6-V A1, the ae-rail suspect]"),
        "m_probes": len(PROBE_LEDGER),
    }
    (root / "build_manifest.json").write_text(
        json.dumps(man, indent=2, sort_keys=True, default=str))
    T6.log(f"  riders manifest → {root / 'build_manifest.json'}")
    return man


if __name__ == "__main__":
    run()
