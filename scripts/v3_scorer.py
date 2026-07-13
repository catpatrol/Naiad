"""V3 anchor run — scorer + deliverables (contract R4/R5/R6 + Amendment A1).

Reads journal_pass1 (raw evidence) + pass results. Produces under
research_outputs/v3_anchor/: manifest.json/md, cards.json + CELL_CARDS.md,
rollups.json/md, hypotheses.json/md, LEDGER_DRAFT.md (never committed here),
and the reviewer packet zip at repo root.

Accounting definitions (stated in manifest):
- tranche accounting from EXIT rows; ENTRY/ADD rows joined by tranche_id for
  one_r_usd = |px_fill - stop| * qty / size_r.
- cost_usd = fees + funding_cum + slippage (funding may be negative).
- cost-stress (VR-3): r_0x = realized_r + cost/one_r ; r_2x = realized_r - cost/one_r.
- campaign = int from tranche_id 'c{N}t{M}'; campaign net R = sum tranche r;
  win = net R (1x) > 0; campaign grade = grade of its first entry fill.
- expectancy = mean campaign net R (1x); 95% CI = percentile bootstrap,
  campaign-level resampling, 10,000 draws, deterministic sha-seeded RNG.
- max drawdown (R): peak-to-trough of exit-ordered cumulative realized_r.
- profit factor = sum positive campaign netR / |sum negative| (1x).
- taxonomy census: per-tranche cohort on EXIT rows (MFE per-unit buckets).
- tranches whose EXIT row is buffered at data end (shadow resolution) are
  disclosed as unresolved; their campaigns are excluded from campaign stats.
- time-in-market = union of [entry ts_open, exit ts_close] / window span.
"""
import hashlib, json, re, sys, zipfile
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

ROOT = Path(r"C:/Users/luisf/OneDrive/Desktop/Midas-Claude Code Resources/naiad")
sys.path.insert(0, str(ROOT))
from engine.journal import read_journal

OUT = ROOT / "research_outputs" / "v3_anchor"
J1 = OUT / "journal_pass1"
CONFIG_SHA = "a3917ea58a1a7e0569eeee85c957914eb0dd08cacc11c6034fcab54053f57727"
N_BOOT = 10_000

p1 = json.loads((OUT / "pass1_results.json").read_text(encoding="utf-8"))
det = json.loads((OUT / "determinism.json").read_text(encoding="utf-8"))

def parse_ts(s): return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc).timestamp()

def boot_ci(vals, seed_key):
    if not vals:
        return None, None
    arr = np.asarray(vals, float)
    seed = int.from_bytes(hashlib.sha256(seed_key.encode()).digest()[:8], "big")
    rng = np.random.default_rng(seed)
    means = rng.choice(arr, size=(N_BOOT, len(arr)), replace=True).mean(axis=1)
    return float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))

def score_cell(key, rec):
    cid, kind = rec["cell_id"], rec["kind"]
    rows = read_journal(J1 / kind, cid)
    ent = {r["tranche_id"]: r for r in rows if r["evt"] in ("ENTRY_FILL", "ADD_FILL")}
    exi = {r["tranche_id"]: r for r in rows if r["evt"] == "EXIT"}
    camp_of = lambda tid: int(re.match(r"c(\d+)t", tid).group(1))

    tr = []  # resolved tranches
    unresolved = [t for t in ent if t not in exi]
    bad_camps = {camp_of(t) for t in unresolved}
    for tid, x in exi.items():
        e = ent.get(tid)
        if e is None:      # EXIT without entry: impossible; flag loudly
            raise AssertionError(f"{cid}: EXIT without ENTRY for {tid}")
        one_r = abs(e["px_fill"] - e["stop"]) * e["qty"] / e["size_r"]
        cost = (x["fees"] or 0) + (x["funding_cum"] or 0) + (x["slippage"] or 0)
        r1 = x["realized_r"]
        tr.append({
            "tid": tid, "camp": camp_of(tid), "kind_t": "ADD" if ent[tid]["evt"] == "ADD_FILL" else "R1V",
            "grade": e["grade"], "tier": e["tier"], "dir": e["dir"],
            "ts_in": e["ts_open"], "ts_out": x["ts_close"],
            "r0": r1 + cost / one_r, "r1": r1, "r2": r1 - cost / one_r,
            "cohort": x["cohort"], "exit_reason": x["exit_reason"],
        })
    # campaigns (resolved only)
    camps = {}
    for t in tr:
        if t["camp"] in bad_camps:
            continue
        c = camps.setdefault(t["camp"], {"r0": 0.0, "r1": 0.0, "r2": 0.0,
                                         "n_tr": 0, "grade": None, "first_ts": None})
        for k in ("r0", "r1", "r2"):
            c[k] += t[k]
        c["n_tr"] += 1
        if t["kind_t"] == "R1V" and (c["first_ts"] is None or t["ts_in"] < c["first_ts"]):
            c["first_ts"], c["grade"] = t["ts_in"], t["grade"]
    cl = list(camps.values())
    netr = {k: round(sum(c[k] for c in cl), 4) for k in ("r0", "r1", "r2")}
    vals = [c["r1"] for c in cl]
    lo, hi = boot_ci(vals, f"{cid}|{kind}")
    wins = sum(1 for c in cl if c["r1"] > 0)
    pos = sum(c["r1"] for c in cl if c["r1"] > 0)
    neg = sum(c["r1"] for c in cl if c["r1"] < 0)
    best_c = max((c["r1"] for c in cl), default=0.0)
    best_t = max((t["r1"] for t in tr if t["camp"] not in bad_camps), default=0.0)
    # max drawdown on exit-ordered cumulative realized r (all resolved tranches)
    seq = sorted((t for t in tr if t["camp"] not in bad_camps),
                 key=lambda t: (t["ts_out"], t["tid"]))
    cum = peak = dd = 0.0
    for t in seq:
        cum += t["r1"]; peak = max(peak, cum); dd = max(dd, peak - cum)
    # taxonomy per tranche
    tax = {}
    for t in tr:
        tax[t["cohort"] or "UNRESOLVED"] = tax.get(t["cohort"] or "UNRESOLVED", 0) + 1
    # time in market: union of tranche intervals / window
    iv = sorted((parse_ts(t["ts_in"]), parse_ts(t["ts_out"])) for t in tr)
    tim, cur_a, cur_b = 0.0, None, None
    for a, b in iv:
        if cur_b is None or a > cur_b:
            if cur_b is not None: tim += cur_b - cur_a
            cur_a, cur_b = a, b
        else:
            cur_b = max(cur_b, b)
    if cur_b is not None: tim += cur_b - cur_a
    span = (parse_ts(rec["end"] + (":00Z" if len(rec["end"]) > 10 else "T23:59:00Z"))
            - parse_ts(rec["start"] + ("T00:00:00Z" if len(rec["start"]) == 10 else ":00Z")))
    evt_n = lambda e: sum(1 for r in rows if r["evt"] == e)
    card = {
        "cell_id": cid, "partition": ("exploration-classic" if kind == "scored"
                        else "spent [CHARACTERIZATION]" if kind == "annex_spent"
                        else "regime-contaminated [CHARACTERIZATION]"),
        "window": f"{rec['start']} -> {rec['end']}",
        "run_id": rec["run_id"], "journal_sha256": rec["journal_sha256"],
        "rows": rec["rows"],
        "campaigns": len(cl), "trades_entries": sum(1 for t in tr if t["kind_t"] == "R1V"),
        "trades_adds": sum(1 for t in tr if t["kind_t"] == "ADD"),
        "campaign_win_rate": round(wins / len(cl), 4) if cl else None,
        "net_r": netr,
        "expectancy_per_campaign_1x": round(float(np.mean(vals)), 4) if vals else None,
        "ci95_1x": [round(lo, 4), round(hi, 4)] if vals else None,
        "max_drawdown_r_1x": round(dd, 4),
        "profit_factor_1x": round(pos / -neg, 4) if neg < 0 else (None if not pos else "inf"),
        "top1_campaign_share": (round(best_c / netr["r1"], 4)
                                if netr["r1"] > 0 and best_c > 0 else None),
        "strip_best_trade_net_r_1x": round(netr["r1"] - best_t, 4),
        "strip_best_campaign_net_r_1x": round(netr["r1"] - best_c, 4),
        "taxonomy": tax,
        "tpw": evt_n("TPW"), "v": evt_n("V"), "x": evt_n("X"),
        "halts": rec["halts"], "final_equity": rec["final_equity"],
        "time_in_market_pct": round(100 * tim / span, 2),
        "unresolved_tranches_at_end": len(unresolved),
        "campaigns_excluded_unresolved": len(bad_camps),
        "insufficient_sample": len(cl) < 10,
        "campaign_r1_list": [round(c["r1"], 4) for c in cl],
        "campaign_grades": [c["grade"] for c in cl],
        "campaign_mandate": cid.rsplit("_", 1)[1],
        "campaign_asset": cid.rsplit("_", 1)[0],
    }
    return card, cl, tr, bad_camps

cards, pools = [], {"scored": [], "annex_spent": [], "annex_contam": []}
tranche_pools = {"scored": [], "annex_spent": [], "annex_contam": []}
for key, rec in sorted(p1.items()):
    if rec["status"] != "ok":
        cards.append({"cell_id": rec["cell_id"], "partition": rec["kind"],
                      "status": rec["status"], "error": rec.get("error")})
        continue
    card, cl, tr, bad = score_cell(key, rec)
    card["kind"] = rec["kind"]
    cards.append(card)
    for c in cl:
        c["cell"] = rec["cell_id"]
        c["mandate"] = rec["cell_id"].rsplit("_", 1)[1]
        c["asset"] = rec["cell_id"].rsplit("_", 1)[0]
    pools[rec["kind"]].extend(cl)
    tranche_pools[rec["kind"]].extend(
        t for t in tr if t["camp"] not in bad)

# ── structural cards (A1) ────────────────────────────────────────────────────
STRUCTURAL = {
    "TAOUSDT_position": "EMPTY scored span: 200x12h warm-up floor lands 2024-07-20, past the exploration-classic edge. Appears only in the regime-contaminated annex (see annex card).",
    **{f"HYPEUSDT_{m}": "EMPTY scored span: lists 2025-05-30, inside the lockbox; zero exploration-classic rows (VR-1 known consequence). See regime-contaminated annex card." for m in ("swing", "intraday", "position")},
    **{f"FARTCOINUSDT_{m}": "EMPTY scored span: lists 2024-12-20, inside the lockbox; zero exploration-classic rows (VR-1 known consequence). See regime-contaminated annex card." for m in ("swing", "intraday", "position")},
    **{f"LITUSDT_{m}": "EMPTY scored span: entire footprint regime-contaminated (VR-1). Annex run DEFERRED under finding G-2: cache holds 31,680 pre-Lighter (Litentry) 1m bars 2025-12-01..2025-12-22 23:59 admissible under the engine 2025-12-01 floor; estate remediation (purge + census --extend) required before any LIT replay." for m in ("swing", "intraday", "position")},
}
for cell, why in STRUCTURAL.items():
    cards.append({"cell_id": cell, "partition": "structural", "status": "STRUCTURAL",
                  "note": why})

# ── rollups (scored only; annex separate, CHARACTERIZATION) ─────────────────
def pool_stats(camps, seed_key):
    vals = [c["r1"] for c in camps]
    lo, hi = boot_ci(vals, seed_key)
    best = max(vals, default=0.0)
    tot = {k: round(sum(c[k] for c in camps), 4) for k in ("r0", "r1", "r2")}
    return {
        "campaigns": len(camps),
        "net_r": tot,
        "expectancy_1x": round(float(np.mean(vals)), 4) if vals else None,
        "ci95_1x": [round(lo, 4), round(hi, 4)] if vals else None,
        "win_rate": round(sum(1 for v in vals if v > 0) / len(vals), 4) if vals else None,
        "strip_best_campaign_net_r_1x": round(tot["r1"] - best, 4),
    }

rollups = {"scored": {}, "annex": {}}
sc = pools["scored"]
rollups["scored"]["grid_total"] = pool_stats(sc, "grid")
for m in ("swing", "intraday", "position"):
    rollups["scored"][f"mandate_{m}"] = pool_stats([c for c in sc if c["mandate"] == m], f"mand|{m}")
for a in sorted({c["asset"] for c in sc}):
    rollups["scored"][f"asset_{a}"] = pool_stats([c for c in sc if c["asset"] == a], f"asset|{a}")
grade_tab = {}
for g in ("A+", "A", "B", "C"):
    gc = [c for c in sc if c["grade"] == g]
    grade_tab[g] = {"campaigns": len(gc),
                    "expectancy_1x": round(float(np.mean([c["r1"] for c in gc])), 4) if gc else None}
rollups["scored"]["grade_cohorts"] = grade_tab
tax_pool = {}
for t in tranche_pools["scored"]:
    tax_pool[t["cohort"] or "UNRESOLVED"] = tax_pool.get(t["cohort"] or "UNRESOLVED", 0) + 1
rollups["scored"]["taxonomy_pooled"] = tax_pool
rollups["annex"]["spent_BTC"] = pool_stats(pools["annex_spent"], "annex_spent")
rollups["annex"]["contaminated"] = pool_stats(pools["annex_contam"], "annex_contam")
rollups["annex"]["label"] = "CHARACTERIZATION — excluded from all scored aggregates and hypothesis scoring"

# ── hypotheses (scored pool, 1x) ─────────────────────────────────────────────
tot1 = rollups["scored"]["grid_total"]["net_r"]["r1"]
best_c_grid = max((c["r1"] for c in sc), default=0.0)
pos_cells = [c for c in cards if c.get("kind") == "scored"
             and c.get("net_r", {}).get("r1", 0) > 0]
maj = [c for c in pos_cells if (c.get("top1_campaign_share") or 0) >= 0.30]
hA1 = {
    "registered": "removing the single best campaign cuts grid total net R by >=25%; AND in a majority of net-positive cell-partitions the top campaign carries >=30% of that cell's net R",
    "grid_net_r_1x": tot1, "best_campaign_r1": round(best_c_grid, 4),
    "cut_pct": round(100 * best_c_grid / tot1, 2) if tot1 > 0 else None,
    "part1": (best_c_grid / tot1 >= 0.25) if tot1 > 0 else "INDETERMINATE (grid net R <= 0; reduction-percentage undefined)",
    "net_positive_cells": len(pos_cells), "of_which_top1_ge_30pct": len(maj),
    "part2": len(maj) > len(pos_cells) / 2 if pos_cells else "INDETERMINATE (no net-positive cells)",
}
hA1["verdict"] = ("PASS" if hA1["part1"] is True and hA1["part2"] is True
                  else "FAIL" if (hA1["part1"] is False or hA1["part2"] is False)
                  else "INDETERMINATE")
eAplus = grade_tab["A+"]["expectancy_1x"]; eA = grade_tab["A"]["expectancy_1x"]
ab = [c for c in sc if c["grade"] in ("A+", "A")]
eAB = round(float(np.mean([c["r1"] for c in ab])), 4) if ab else None
eB = grade_tab["B"]["expectancy_1x"]; eC = grade_tab["C"]["expectancy_1x"]
hA2 = {"registered": "pooled net expectancy per campaign orders A-or-better > B > C",
       "e_A_or_better": eAB, "e_B": eB, "e_C": eC,
       "note": "C-grade never fills by design (engine gate); C cohort structurally empty — 'B > C' leg unevaluable as registered.",
       "verdict": ("PASS (partial: A-or-better > B; C empty by design)"
                   if eAB is not None and eB is not None and eAB > eB
                   else "FAIL (A-or-better <= B)" if eAB is not None and eB is not None
                   else "INDETERMINATE")}
hA3_detail = {}
for a in ("ETHUSDT", "SOLUSDT", "NEARUSDT", "ZECUSDT"):
    hA3_detail[a] = {m: next((c.get("net_r", {}).get("r1") for c in cards
                              if c.get("cell_id") == f"{a}_{m}" and c.get("kind") == "scored"), None)
                     for m in ("swing", "intraday", "position")}
n_pos_swing = sum(1 for a, d in hA3_detail.items() if (d["swing"] or 0) > 0)
hA3 = {"registered": "at least two of {ETH, SOL, NEAR, ZEC} show positive net total R in exploration-classic in their diagonal mandate",
       "reading": "PRIMARY: diagonal = swing (the deployed 4H/5m configuration). AMBIGUITY FLAGGED: 'diagonal mandate' is not defined per-asset anywhere in the charter; per-mandate numbers printed so the reviewer can re-score under any reading without re-running.",
       "per_asset_net_r_1x": hA3_detail,
       "positive_in_swing": n_pos_swing,
       "verdict": "PASS" if n_pos_swing >= 2 else "FAIL"}
exp_m = {m: rollups["scored"][f"mandate_{m}"]["expectancy_1x"] for m in ("position", "swing", "intraday")}
ok_A4 = (exp_m["position"] is not None and exp_m["swing"] is not None and exp_m["intraday"] is not None
         and exp_m["position"] >= exp_m["swing"] >= exp_m["intraday"])
hA4 = {"registered": "pooled per-campaign net expectancy: position >= swing >= intraday",
       "expectancies": exp_m, "verdict": "PASS" if ok_A4 else "FAIL"}
tp = {k: v for k, v in tax_pool.items() if k != "UNRESOLVED"}
biggest = max(tp, key=tp.get) if tp else None
hA5 = {"registered": "STILLBORN is the single largest taxonomy cohort grid-wide",
       "census": tp, "largest": biggest,
       "verdict": "PASS" if biggest == "STILLBORN" and
                  list(tp.values()).count(tp[biggest]) == 1 else
                  ("FAIL" if biggest else "INDETERMINATE")}
hypotheses = {"H-A1": hA1, "H-A2": hA2, "H-A3": hA3, "H-A4": hA4, "H-A5": hA5,
              "basis": "scored partitions only (exploration-classic, 20 cells), 1x costs, campaign-level"}

# ── manifest ────────────────────────────────────────────────────────────────
runner_sha = hashlib.sha256(Path(__file__).with_name("v3_runner.py").read_bytes()).hexdigest()
scorer_sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
manifest = {
    "phase": "v12 V3 anchor run",
    "contract": "prompts/V3_Anchor_Run_Contract.md + Amendment A1 (350b82b)",
    "engine": {"version": "1.0.7", "commit": "2f260e1",
               "lineage": "1.0.3 (parity-signed, 38b3f66) + 1.0.4 G-3 stop-guarantee death-transition exemption (22b6771) + 1.0.5 G-4 wake-time campaign-death net (3828980) + 1.0.6 G-5/G-5b same-wake sibling semantics (cd42c5c) + 1.0.7 G-6 gate tranche-cap sibling projection (2f260e1); all ratified, each parity-byte-identity-proven under pinned stamp (signed SHA 4c734317...ce92de reproduced four consecutive times)",
               "strategy_code_delta_vs_parity_signed": "trading.py only (G-3 assert exemption, G-4 death net, G-5 assert scope, G-5b risk projection, G-6 cap projection); signals/data/journal untouched; sibling family and death-transition family both CLOSED by enumeration (CHANGELOG 1.0.7)"},
    "partial_look": json.loads((OUT / "partial_look_checkpoint.json").read_text(encoding="utf-8")),
    "config": {"id": "v12_anchor", "sha256": CONFIG_SHA,
               "proof_signal_vs_v11_faithful": "EMPTY (byte-identical)",
               "proof_trading_vs_naiad_v0": "EMPTY (byte-identical)",
               "proof_shadows_vs_naiad_v0": "EMPTY (byte-identical)",
               "semantic_delta_vs_naiad_v0": ["config_id", "signal.v_births_provisional: True -> False (Pine v11.0.2 literal)"]},
    "data_source": "census-verified local estate (V1), offline, backfill=False both passes; zero network fetches during the run",
    "partitions": {"lockbox": "2024-07-01T00:00Z .. 2025-10-05T23:59:59Z (sealed)",
                   "scored": "exploration-classic (open time <= 2024-06-30 23:59:59)",
                   "annex_spent": "BTCUSDT 2025-10-06 .. 2026-07-07 [CHARACTERIZATION]",
                   "annex_contam": "non-BTC 2025-10-06 .. 2026-07-07 [CHARACTERIZATION]",
                   "right_edge": "2026-07-07T23:59:59Z (no loaded open time beyond it — see loaded_spans)"},
    "grid": {"scored_cells": 20,
             "annex_runs": sum(1 for r in p1.values() if r['kind'] != 'scored'),
             "structural_cards": 10, "lit_annex": "EXCLUDED (G-2)"},
    "shadows_statement": (
        "The shadows layer journals per-tranche counterfactual COLUMNS, never a separate book: "
        "MFE/MAE/give-back and post-exit continuation (1/5/20 exec bars) in per-unit R; the exit-variant "
        "race X-A (e200-trail survival ratchet) / X-B (X-A + 50% banked at first TPW) / X-C (X-A + 50% at "
        "first 2-ATR extension) / X-D (mechanized Playbook 25/25/trail), each as per-unit R on the EXIT row; "
        "two stop-anchor variants; an alternate rib-cross entry; and ladder counterfactual fields "
        "(size_full_r1 / size_big_adds = realized_r/size_r, ladder_unthrottled_grade/size_r). "
        "It does NOT compute the charter §3.4 1R-adds counterfactual as a ready scored line — per A1 Q-3 "
        "that counterfactual is recorded UNIMPLEMENTED as a scored artifact; the journaled per-unit fields "
        "make it recomputable offline in V5 with no new data. Contract F3's '1R shadow line' maps to "
        "trading.max_open_campaign_risk_r: 1.0 (the open-campaign risk rail, asserted in-path)."),
    "cost_semantics": {
        "modeled": "taker fees 5 bps/side (entry+exit); slippage per side by tier A/B/C = 2/5/10 bps; funding per funding timestamp on qty x last closed price, realized at exit",
        "not_modeled": "book depth/impact; partial fills; maker/taker split; sub-bar stop path (bar-resolution fidelity bound, charter §4); funding on fill bar; margin/liquidation; fee tiers; era-specific microstructure (VR-3 stress rows stand in)",
        "stress_rows": "r_0x = realized_r + cost/one_r; r_2x = realized_r - cost/one_r; cost = fees + funding + slippage per EXIT row; one_r from ENTRY row |px_fill-stop|*qty/size_r"},
    "findings": {
        "G-1": "replay path has no code-level lockbox guard; this run protected by window arithmetic + per-cell loaded-span assertions below; code guard due at next engine touch alongside J-1 (A1 Q-2)",
        "G-2": "LITUSDT cache holds 31,680 pre-Lighter (Litentry) 1m bars [2025-12-01 .. 2025-12-22 23:59] + a 1,050-bar void to the Lighter listing 2025-12-23 17:30; admissible under the engine 2025-12-01 floor, invalid under the census first-valid. LIT annex EXCLUDED from this run; estate remediation (file purge + census --extend) required before any LIT replay."},
    "loaded_spans_and_assertions": {k: {kk: rec[kk] for kk in ("kind", "start", "end", "loaded_spans", "lockbox_warmup_traversal", "first_journal_ts", "status", "violations") if kk in rec}
                                    for k, rec in sorted(p1.items()) if rec["status"] in ("ok", "ASSERTION_VIOLATION")},
    "determinism": {"all_identical": det["all_identical"], "mismatches": det["mismatches"]},
    "scripts": {"v3_runner.py_sha256": runner_sha, "v3_scorer.py_sha256": scorer_sha},
    "journal_hash_formula": "sha256 over byte-concatenation of the cell's monthly JSONL files in filename order (engine/journal.py files_sha256)",
}

# ── write artifacts ─────────────────────────────────────────────────────────
def wj(name, obj):
    (OUT / name).write_text(json.dumps(obj, indent=2, sort_keys=True),
                            encoding="utf-8", newline="\n")
wj("manifest.json", manifest)
wj("cards.json", cards)
wj("rollups.json", rollups)
wj("hypotheses.json", hypotheses)

# human-readable cards
def fmt_card(c):
    if c.get("status") == "STRUCTURAL":
        return f"### {c['cell_id']} — STRUCTURAL\n{c['note']}\n"
    if c.get("status") not in (None, "ok") and "net_r" not in c:
        return f"### {c['cell_id']} — {c['status']}\n{c.get('error','')}\n"
    L = [f"### {c['cell_id']} — {c['partition']}",
         f"window {c['window']} · run_id {c['run_id']} · sha {c['journal_sha256'][:16]}… · {c['rows']} rows",
         f"- campaigns {c['campaigns']}{' **INSUFFICIENT SAMPLE**' if c['insufficient_sample'] else ''} · entries {c['trades_entries']} · adds {c['trades_adds']} · win rate {c['campaign_win_rate']}",
         f"- net R: 0x {c['net_r']['r0']} · **1x {c['net_r']['r1']}** · 2x {c['net_r']['r2']}",
         f"- expectancy/campaign (1x) {c['expectancy_per_campaign_1x']} · 95% CI {c['ci95_1x']} (10k campaign bootstrap)",
         f"- max DD {c['max_drawdown_r_1x']}R · PF {c['profit_factor_1x']} · top-1 share {c['top1_campaign_share']}",
         f"- strip-best-trade {c['strip_best_trade_net_r_1x']} · strip-best-campaign {c['strip_best_campaign_net_r_1x']}",
         f"- taxonomy {c['taxonomy']} · TPW {c['tpw']} · V {c['v']} · X {c['x']} · halts {c['halts']}",
         f"- time-in-market {c['time_in_market_pct']}% · final equity {c['final_equity']} · unresolved@end {c['unresolved_tranches_at_end']} (excl. campaigns {c['campaigns_excluded_unresolved']})",
         ""]
    return "\n".join(L)

md = ["# V3 anchor run — cell cards", "",
      "Scored = exploration-classic. Annex cards are CHARACTERIZATION — excluded from scored aggregates and hypothesis scoring.", ""]
for kind, title in (("scored", "Scored (20)"), ("annex_spent", "Annex: BTC spent [CHARACTERIZATION]"),
                    ("annex_contam", "Annex: regime-contaminated [CHARACTERIZATION]")):
    md.append(f"## {title}\n")
    md += [fmt_card(c) for c in cards if c.get("kind") == kind]
md.append("## Structural (10)\n")
md += [fmt_card(c) for c in cards if c.get("status") == "STRUCTURAL"]
(OUT / "CELL_CARDS.md").write_text("\n".join(md), encoding="utf-8", newline="\n")

# rollups + hypotheses md
rm = ["# V3 anchor run — rollups (scored) + hypotheses", "",
      "```json", json.dumps(rollups, indent=2, sort_keys=True), "```", "",
      "## Hypothesis scorecard", "```json",
      json.dumps(hypotheses, indent=2, sort_keys=True), "```"]
(OUT / "ROLLUPS_AND_HYPOTHESES.md").write_text("\n".join(rm), encoding="utf-8", newline="\n")

# ── ledger draft (NOT committed, NOT appended) ──────────────────────────────
grid_sha = hashlib.sha256("".join(
    p1[k]["journal_sha256"] for k in sorted(p1) if p1[k]["status"] == "ok").encode()).hexdigest()
_pl = json.loads((OUT / "partial_look_checkpoint.json").read_text(encoding="utf-8"))
PARTIAL_LOOK_RESULT = f"{sum(1 for v in _pl.values() if v['match'])}/{len(_pl)} MATCH"
ld = f"""DRAFT — DO NOT COMMIT until reviewer recomputes headline numbers from raw journals.

## 2026-07-13 — v12 V3 anchor run: EXECUTED — evidence spend recorded
- Evidence spend: exploration-classic FIRST LOOK consumed, 20 scored cells (grid per Stage-1 F1 + A1 Q-4 month-aligned starts; TAOUSDT_swing 30d INSUFFICIENT SAMPLE by design).
- Config: v12_anchor (sha256 {CONFIG_SHA[:16]}…), signal byte-identical to v11_faithful, trading/shadows byte-identical to naiad_v0, v_births_provisional=false (Pine literal). Engine 1.0.7 (2f260e1); strategy-code delta vs parity-signed 38b3f66 = the four ratified fixes per the G-3..G-6 bullet below, each pinned-stamp parity-proven.
- Determinism: full double-run, per-cell journal SHA256 {"ALL IDENTICAL" if det['all_identical'] else "MISMATCH — " + str(det['mismatches'])} across {sum(1 for r in p1.values() if r['status']=='ok')} runs.
- Grid evidence hash (sha256 over sorted per-cell journal SHAs): {grid_sha}
- Scored grid net R (1x): {tot1} over {rollups['scored']['grid_total']['campaigns']} campaigns; strip-best-campaign {rollups['scored']['grid_total']['strip_best_campaign_net_r_1x']}. (Headline pending reviewer recomputation.)
- Annex (CHARACTERIZATION only): BTC spent 3 cells; regime-contaminated 24 cells (8 assets). F4-a lockbox warm-up traversal disclosed per cell in manifest; zero journal rows with lockbox open times (first_journal_ts >= window start, all annex cells).
- G-1 registered: no code-level lockbox guard on the replay path; run protected by window arithmetic + manifest loaded-span assertions; code guard due at engine 1.0.8 with J-1 (per the G-6 ruling: first post-anchor-run engine touch).
- G-2 registered: LIT cache contamination (31,680 pre-Lighter bars); LIT annex deferred pending estate remediation.
- G-3/G-4/G-5+G-5b/G-6: four latent trading-layer states surfaced by deep history, each halted, bar-level diagnosed, operator-ratified, shipped as engines 1.0.4/1.0.5/1.0.6/1.0.7 with fail-then-pass fixtures and pinned-stamp parity byte-identity proofs (signed SHA 4c734317...ce92de reproduced four consecutive times). Death-transition family closed at 1.0.5; sibling family closed by enumeration at 1.0.7.
- Partial-consumption record (verbatim per rulings): run-15 halt (G-5) — 7 scored-cell journals written (BTC swing/intraday/position, ETH swing/intraday/position, SOL_swing); run-21 halt (G-6) — 3 more (SOL_intraday, SOL_position, NEAR_swing), 10 total; one-line summaries incl. end equity seen by builder only; values withheld from operator/reviewer.
- G-6 mismatch at the relaunch checkpoint (SOL_position) — ACCEPTED (operator + reviewer, 2026-07-13): one relocated null-valued REJECT row (ts_open 14:00->13:45, reject_reason gap_through_stop->max_tranches, 2023-06-30), the ratified G-6 semantics on a fill-time-rejected sibling pair; zero trading/P&L/equity divergence; four aggregate pairs identical; other 9 cells 9/9 exact; baseline hash updated to 13b84c6b….
- DISCLOSURE: during mismatch verification the reviewer saw two SOL_position aggregates (terminal equity, realized-R total) — bounded, deliberate, recorded; design was frozen pre-run so no hypothesis threshold is affected.
- Final relaunch partial-look checkpoint: {PARTIAL_LOOK_RESULT} (stripped-field canonicalization on record in the manifest).
- Data: census estate, offline, zero fetches. Hypothesis scorecard H-A1..H-A5 in research_outputs/v3_anchor/ (numbers not restated here pending review).
- Operator: Ludwig. Builder: run executed per contract; reviewer recomputation pending.
"""
(OUT / "LEDGER_DRAFT.md").write_text(ld, encoding="utf-8", newline="\n")

# ── packet zip ──────────────────────────────────────────────────────────────
pk = ROOT / "v12_v3_anchor_packet_20260713.zip"
with zipfile.ZipFile(pk, "w", zipfile.ZIP_DEFLATED) as z:
    for f in ["manifest.json", "cards.json", "rollups.json", "hypotheses.json",
              "CELL_CARDS.md", "ROLLUPS_AND_HYPOTHESES.md", "determinism.json",
              "pass1_results.json", "pass2_results.json", "LEDGER_DRAFT.md"]:
        z.write(OUT / f, f"v3_anchor/{f}")
    z.write(Path(__file__).with_name("v3_runner.py"), "v3_anchor/scripts/v3_runner.py")
    z.write(Path(__file__), "v3_anchor/scripts/v3_scorer.py")
    z.write(ROOT / "configs/v12_anchor.yaml", "v3_anchor/configs/v12_anchor.yaml")
    for p in sorted(J1.rglob("*.jsonl")):
        z.write(p, f"v3_anchor/journal_pass1/{p.relative_to(J1)}")
print(f"packet: {pk.name}  {pk.stat().st_size/1e6:.1f} MB")
print(f"grid evidence hash: {grid_sha}")
print("SCORER COMPLETE")
