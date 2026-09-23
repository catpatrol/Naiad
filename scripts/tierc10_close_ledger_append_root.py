#!/usr/bin/env python
"""TIER-C10 · CLOSE — F-LAR: THE LEDGER_APOLLO APPEND OF RECORD, CERTIFIED.  REPORT-ONLY.

WHAT IS CERTIFIED
  research_outputs/tierc10/LEDGER_APOLLO_APPEND.md — the WHOLE file is the
  byte block the CLOSE appends to exchange/status/LEDGER_APOLLO.md.  It is a
  hand condensation, not a builder's render, so it gets its own certifier:
  every «cite» in it is re-verified by F-LA's OWN quote verifier
  (scripts/tierc10_close_close_ledger_append.py: parse_quotes / verify_quote,
  imported, not copied), every number in it is TRACED to a file and field read
  this run, and a coverage leg proves no number in the prose escapes a trace.
  close/LEDGER_APOLLO_APPEND.draft.md (F-LA's own render) is a SOURCE-QUOTE
  draft; it is NOT the append of record.

  This module never writes the root file or the ledger.  It writes only
  research_outputs/tierc10/close/FIXTURES_CLOSE_ledger_append_root.txt (and,
  for F-DET, close/_det_ledger_append_root/seed_*/).

HOW A NUMBER IS COVERED (F-LAR-COVER)
  The prose is the block minus its «cite» lines and their '|'/'+' quote lines
  (those are verified byte-for-byte by F-LAR-CITE).  In the prose, a digit is
  covered iff it lies inside (a) a TRACE literal (verified against its source,
  and present exactly its declared number of times), (b) a masked token: an
  identifier that carries a letter (TC9, P-GEN-1, frozen3.0, 5m, H100, a hex
  sha), a JSON selector (rows[2]), a section sign (§2.1), or a PENDING STAMP
  ⟦…⟧, or (c) a listed EXEMPTION with its reason.  An ISO date or timestamp
  standing alone is never masked: it must be traced or exempted.

FIXTURE LEGS (each states FAILS IF; each carries sabotage that must go RED)
  F-LAR-FORMAT  · F-LAR-CITE · F-LAR-REQUIRED · F-LAR-TRACE · F-LAR-COVER ·
  F-LAR-CLAIM   · F-LAR-STAMP · F-LAR-NOWRITE · F-DET

Run:  export NAIAD_CACHE_DIR=/Users/luis/.cache/naiad/snapshots/tc10_20260921 PYTHONDONTWRITEBYTECODE=1
      ~/venvs/naiad/bin/python scripts/tierc10_close_ledger_append_root.py
Exit: 0 every leg GREEN · 1 a RED leg or a HALT.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = Path.home() / ".cache" / "naiad" / "snapshots" / "tc10_20260921"
LIVE_CACHE = Path.home() / ".cache" / "naiad" / "data_cache"


def guard_substrate(env: str | None) -> Path:
    if not env:
        raise SystemExit(f"HALT: NAIAD_CACHE_DIR is unset — F-LAR runs only on {SNAPSHOT}")
    norm = Path(os.path.normpath(os.path.expanduser(env)))
    if norm == LIVE_CACHE or LIVE_CACHE in norm.parents:
        raise SystemExit("HALT: NAIAD_CACHE_DIR names the LIVE cache — READ-NEVER, WRITE-NEVER for TC10")
    if norm.resolve() != SNAPSHOT.resolve():
        raise SystemExit(f"HALT: NAIAD_CACHE_DIR={norm} is not the TC10 snapshot {SNAPSHOT}")
    return norm


guard_substrate(os.environ.get("NAIAD_CACHE_DIR"))
if os.environ.get("PYTHONDONTWRITEBYTECODE") != "1":
    raise SystemExit("HALT: PYTHONDONTWRITEBYTECODE is not 1 (the TC10 run law)")

sys.path.insert(0, str(ROOT / "scripts"))
import pandas as pd                                                  # noqa: E402
import pyarrow.parquet as pq                                         # noqa: E402

import tierc10_close_close_ledger_append as LA   # F-LA's own quote verifier  # noqa: E402

TC10 = ROOT / "research_outputs" / "tierc10"
OUT = TC10 / "close"
ROOT_APPEND = TC10 / "LEDGER_APOLLO_APPEND.md"
SCRIPT_DRAFT = OUT / "LEDGER_APOLLO_APPEND.draft.md"
TRANSCRIPT = OUT / "FIXTURES_CLOSE_ledger_append_root.txt"
DET_ROOT = OUT / "_det_ledger_append_root"
LEDGER_APOLLO = ROOT / "exchange" / "status" / "LEDGER_APOLLO.md"
CONTRACT_REL = "exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md"
DET_SEEDS = (1, 20260921)
REGS = ("P-GEN-1", "P-SPR-2", "P-BE-1", "P-TRG-2", "P-BRK-I1", "P-BRK-S1")
SEP = "\n---\n\n"
STAMP_RE = re.compile(r"⟦[^⟧\n]*⟧")

# Sources F-LA-CITE style quotes may cite (repo-relative → bytes).
CITE_SOURCES = [CONTRACT_REL, "LEDGER.md", "exchange/status/LEDGER_APOLLO.md",
                "research_outputs/tierc10/PROGRESS.json",
                "research_outputs/tierc10/REGISTRATION_TEXTS.json",
                "research_outputs/tierc10/scores/FAMILY.json",
                "research_outputs/tierc10/panel/FIXTURES_PANEL.txt",
                "research_outputs/tierc10/FIXTURES_RESUME.txt",
                "research_outputs/tierc10/data/fee_schedule.json"] + \
               [f"research_outputs/tierc10/scores/{r}.rows.json" for r in REGS]

# Exemptions: (literal, count in prose, reason). Printed in the transcript.
EXEMPT = [("2026-09-22", 1, "the block's own date in its header line (the CLOSE day), not a measured value")]

LINES: list[str] = []


def say(m: str = "") -> None:
    print(m, flush=True)
    LINES.append(m)


def sha_b(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def f6(x) -> str:
    return f"{float(x):+.6f}"


def p6(x) -> str:
    return f"{float(x):.6f}"


def f4(x) -> str:
    return f"{float(x):+.4f}"


def ci(sr) -> str:
    return f"CI [{f6(sr['ci_lo'])}, {f6(sr['ci_hi'])}]"


# ═══════════════════════════════════════════════════════════════ sources
def load() -> dict:
    j = lambda rel: json.loads((ROOT / rel).read_text("utf-8"))          # noqa: E731
    C: dict = {"read": {}}

    def mark(rel):
        b = (ROOT / rel).read_bytes()
        C["read"][rel] = (sha_b(b), len(b))
        return b
    for rel in CITE_SOURCES:
        mark(rel)
    C["src"] = {rel: (ROOT / rel).read_bytes() for rel in CITE_SOURCES}
    T = "research_outputs/tierc10/"
    for rel in [T + "REGISTRY_PIN.json", T + "data/DATA_SPEND_AUDIT.json", T + "data/STAGE_D_MANIFEST.json",
                T + "close/P_TRG_2_SEEN_SHARE.json", T + "close/FIXTURES_CLOSE_p_trg_2_seen_share.txt",
                T + "close/FORWARD_STRIP.parquet", T + "close/S3_STAGE_D.md", T + "close/S2_CENSUS_R.md",
                T + "census/height_toll_verdict.parquet", T + "census/acceptance_head_to_head.parquet",
                T + "census/outcome_grid.parquet", T + "panel/control_reference.parquet",
                T + "close/V6_CONTROL_HAIRCUT_TWIN.parquet", T + "close/S5_FINDINGS_NOT_FIXED.json",
                T + "scores/DRYRUN.json", T + "lanes/BE_LATCH_CENSUS.json", "scripts/tierc10_panel.py",
                T + "OPERATOR_RULINGS.md"]:
        mark(rel)
    C["fam"] = j(T + "scores/FAMILY.json")
    C["rows"] = {r: j(T + f"scores/{r}.rows.json") for r in REGS}
    C["pin"] = j(T + "REGISTRY_PIN.json")
    C["prog"] = j(T + "PROGRESS.json")
    C["dsa"] = j(T + "data/DATA_SPEND_AUDIT.json")
    C["man"] = j(T + "data/STAGE_D_MANIFEST.json")
    C["ss"] = j(T + "close/P_TRG_2_SEEN_SHARE.json")
    C["ss_fix"] = (ROOT / T / "close/FIXTURES_CLOSE_p_trg_2_seen_share.txt").read_text("utf-8")
    C["fs"] = pd.read_parquet(ROOT / T / "close/FORWARD_STRIP.parquet")
    C["s3"] = (ROOT / T / "close/S3_STAGE_D.md").read_text("utf-8")
    C["s2"] = (ROOT / T / "close/S2_CENSUS_R.md").read_text("utf-8")
    C["htv"] = pd.read_parquet(ROOT / T / "census/height_toll_verdict.parquet")
    C["ah"] = pd.read_parquet(ROOT / T / "census/acceptance_head_to_head.parquet")
    C["og_m"] = sorted(set(pq.read_table(ROOT / T / "census/outcome_grid.parquet",
                                         columns=["m_looks_this_table"]).to_pandas()["m_looks_this_table"]))
    C["cr"] = pd.read_parquet(ROOT / T / "panel/control_reference.parquet")
    C["v6"] = pd.read_parquet(ROOT / T / "close/V6_CONTROL_HAIRCUT_TWIN.parquet")
    C["s5"] = j(T + "close/S5_FINDINGS_NOT_FIXED.json")
    C["fee"] = j(T + "data/fee_schedule.json")
    C["dry"] = j(T + "scores/DRYRUN.json")
    C["be"] = j(T + "lanes/BE_LATCH_CENSUS.json")
    C["panel_src"] = (ROOT / "scripts/tierc10_panel.py").read_text("utf-8")
    C["rulings"] = (ROOT / T / "OPERATOR_RULINGS.md").read_text("utf-8")
    C["contract"] = C["src"][CONTRACT_REL].decode("utf-8")
    C["ledger_md"] = C["src"]["LEDGER.md"].decode("utf-8")
    return C


def sr(C, reg, i=0) -> dict:
    return C["rows"][reg]["rows"][i]["score_row"]


def par(C, reg, i, key) -> dict:
    hits = [x for x in C["rows"][reg]["rows"][i]["beside"]["per_asset_rows"]
            if x.get("aggregation") == "raw_panel" and x.get("group") == "asset" and x.get("key") == key]
    if len(hits) != 1:
        raise KeyError(f"{reg} rows[{i}] per_asset_rows {key}: {len(hits)} raw_panel rows")
    return hits[0]


def prior(C, reg) -> str:
    m = re.search(rf"^  {re.escape(reg)} \[(\d+)%\]", C["contract"], re.M)
    return m.group(1) if m else "?"


def htv_row(C, lens, asset, era, scale="frozen3.0"):
    h = C["htv"]
    r = h[(h.lens == lens) & (h.asset == asset) & (h.era == era) & (h.scale_kind == scale)]
    if len(r) != 1:
        raise KeyError(f"height_toll_verdict {lens} {asset} {era} {scale}: {len(r)} rows")
    return r.iloc[0]


def single_passes(C, lens, era, scale):
    h = C["htv"]
    return int(h[(h.lens == lens) & (~h.asset.str.startswith("POOLED")) & (h.era == era)
                 & (h.scale_kind == scale)].verdict_pass.sum())


def era_ms(C) -> tuple:
    iso = re.search(r'^ERA_CUT_ISO = "([^"]+)"', C["panel_src"], re.M).group(1)
    return iso, int(pd.Timestamp(iso).value // 1_000_000)


# ═══════════════════════════════════════════════════════════════ the trace table
def traces(C) -> list:
    """(literal-as-computed-from-source, declared count in prose, source). The
    literal is BUILT from the source; F-LAR-TRACE requires it verbatim in the
    prose exactly `count` times."""
    fam, ss, fs = C["fam"], C["ss"], C["fs"]
    dsa = C["dsa"]["counts"]
    T = []
    t = lambda lit, n, src: T.append((lit, n, src))                      # noqa: E731
    # header · CLASS
    t(f"{dsa['never-touched']} NEVER-TOUCHED", 2, "DATA_SPEND_AUDIT.json counts.never-touched")
    t(f"{dsa['display-only']} DISPLAY-ONLY", 1, "DATA_SPEND_AUDIT.json counts.display-only")
    t(f"seed {C['prog']['seed']}", 1, "PROGRESS.json seed")
    t(f"registry len {C['pin']['registry_len']}", 1, "REGISTRY_PIN.json registry_len")
    t(f"m = {fam['family_m_declared']}", 1, "FAMILY.json family_m_declared")
    t(f"{sum(r['scored_in_family'] for r in fam['rows'])} scored", 1, "FAMILY.json rows[].scored_in_family")
    t(f"{len(fam['scored_slots_halted'])} slot HALTed", 1, "FAMILY.json scored_slots_halted")
    t(f"q/m = {p6(fam['fdr_bar_q_over_m'])}", 1, "FAMILY.json fdr_bar_q_over_m")
    t(f"As-of {C['prog']['as_of_of_record']}", 1, "PROGRESS.json as_of_of_record")
    # priors
    for reg in REGS:
        t(f"{reg.ljust(8)} [{prior(C, reg)}%]", 1, f"{CONTRACT_REL} B list, {reg}'s prior")
    # P-GEN-1
    s = sr(C, "P-GEN-1")
    t(f"n {s['n']}, {f6(s['ci_point'])} R/campaign, {ci(s)},", 1, "P-GEN-1.rows.json rows[0].score_row")
    t(f"p {p6(s['p_one_sided'])}, LOAO {s['loao_line']} (bar {s['loao_bar_above_half']}).", 1,
      "P-GEN-1.rows.json rows[0].score_row p_one_sided, loao_line, loao_bar_above_half")
    t(f"BNB nets {f4(par(C, 'P-GEN-1', 0, 'BNBUSDT')['net_r'])} R of the", 1,
      "P-GEN-1.rows.json rows[0].beside.per_asset_rows BNBUSDT net_r")
    t(f"arm's {f4(s['net_r'])} R", 1, "P-GEN-1.rows.json rows[0].score_row.net_r")
    s2 = sr(C, "P-GEN-1", 2)
    t(f"n {s2['n']}, {f6(s2['ci_point'])}, {ci(s2)}, LOAO {s2['loao_line']}.", 1, "P-GEN-1.rows.json rows[2].score_row")
    for key, lab, tail in (("PUMPUSDT", "PUMP", ","), ("MNTUSDT_BYBIT", "MNT", ","), ("SUIUSDT", "SUI", " R/campaign")):
        t(f"{lab} {f4(par(C, 'P-GEN-1', 2, key)['expectancy_r'])}{tail}", 1,
          f"P-GEN-1.rows.json rows[2].beside.per_asset_rows {key} expectancy_r")
    nt = C["dsa"]["classes"]["never-touched"]
    t(f"{dsa['never-touched']} never-touched ({' '.join(nt)})", 1, "DATA_SPEND_AUDIT.json counts, classes")
    t(f"{dsa['display-only']} display-only", 1, "DATA_SPEND_AUDIT.json counts.display-only")
    # P-SPR-2
    s = sr(C, "P-SPR-2")
    t(f"n {s['n']}, {f6(s['ci_point'])} R,", 1, "P-SPR-2.rows.json rows[0].score_row")
    t(f"{ci(s)}, LOAO {s['loao_line']}.", 1, "P-SPR-2.rows.json rows[0].score_row")
    t(f"arm ({f6(sr(C, 'P-SPR-2', 2)['ci_point'])})", 1, "P-SPR-2.rows.json rows[2].score_row.ci_point")
    txt = json.loads(C["src"]["research_outputs/tierc10/REGISTRATION_TEXTS.json"])
    t("(CI lo > 0)" if "STRICTLY greater than zero" in txt["P-SPR-2"]["text"] else "<no clause>", 1,
      "REGISTRATION_TEXTS.json P-SPR-2 §7 'STRICTLY greater than zero' (the clause's threshold)")
    t("ATTESTED at STEP 0" if any(x["stage"] == "STEP 0" for x in C["prog"]["stages"]) else "<no STEP 0>", 1,
      "PROGRESS.json stages[].stage 'STEP 0' (the stage's name)")
    # P-BE-1
    k = next(a for a in C["dry"]["arms"] if a.get("registration") == "P-BE-1" and a.get("scored_in_family"))["keys"]
    t(f"{k['n_paired']}/{k['n_paired'] + k['n_base_only']} campaign keys paired with v6, {k['n_book_only']} book-only,",
      1, "DRYRUN.json P-BE-1 scored arm .keys")
    t(f"{k['n_base_only']} base-only", 1, "DRYRUN.json P-BE-1 scored arm .keys.n_base_only")
    bc = C["be"]["counts"]["by_class"]
    t(f"dip-before {bc['dip_before']}, dip-after {bc['dip_after']}, tie {bc['tie']}, mismatch {bc['mismatch']}, "
      f"of {C['be']['counts']['n_latch']} latch bars", 1, "BE_LATCH_CENSUS.json counts")
    # P-TRG-2
    s = sr(C, "P-TRG-2")
    tw = C["rows"]["P-TRG-2"]["rows"][0]["beside"]["haircut_twin"]
    arm10 = fam["rows"][10]
    t("9/12" if "9/12" in arm10["arm"] and arm10["registration"] == "P-TRG-2" else "<cell name absent>", 3,
      "FAMILY.json rows[10].arm (the cell's name)")
    t(f"n {s['n']} vs base {tw['base_n']}, Δ {f6(s['ci_point'])} R, {ci(s)},", 1,
      "P-TRG-2.rows.json rows[0].score_row; beside.haircut_twin.base_n")
    t(f"p {p6(s['p_one_sided'])} <= {p6(fam['fdr_bar_q_over_m'])}, LOAO {s['loao_line']} "
      f"({s['sens_loao_line'].split()[0]} at the sensitivity", 1,
      "P-TRG-2.rows.json rows[0].score_row p_one_sided, loao_line, sens_loao_line; FAMILY fdr bar")
    # P-BRK-I1
    s = sr(C, "P-BRK-I1")
    pan = C["rows"]["P-BRK-I1"]["rows"][0]["beside"]["per_asset_n"]
    t(f"n {s['n']} on {sum(1 for v in pan.values() if v)} of {len(pan)} assets, {f6(s['ci_point'])} R, {ci(s)},", 1,
      "P-BRK-I1.rows.json rows[0].score_row; beside.per_asset_n")
    t(f"p {p6(s['p_one_sided'])}, LOAO {s['loao_line']}.", 1, "P-BRK-I1.rows.json rows[0].score_row")
    t(f"({f4(par(C, 'P-BRK-I1', 0, 'ETHUSDT')['best_r'])} R)", 1, "P-BRK-I1.rows.json per_asset_rows ETHUSDT best_r")
    t(f"({f4(s['net_r'])} R)", 1, "P-BRK-I1.rows.json rows[0].score_row.net_r")
    h = htv_row(C, "1d", "POOLED:CLASSIC5", "holdout")
    t(f"edge NET {f4(h.edge_net_h20)}, {int(h.n_ranges)} ranges, {'provisional' if h.provisional else 'firm'}", 1,
      "height_toll_verdict.parquet 1d POOLED:CLASSIC5 frozen3.0 holdout")
    # P-BRK-S1
    s = sr(C, "P-BRK-S1")
    t(f"n {s['n']}, {f6(s['ci_point'])} R,", 1, "P-BRK-S1.rows.json rows[0].score_row")
    t(f"{ci(s)}, LOAO {s['loao_line']}, p {s['p_one_sided']}.", 1, "P-BRK-S1.rows.json rows[0].score_row")
    h = htv_row(C, "5m", "POOLED:CLASSIC5", "holdout")
    t(f"(edge NET {f4(h.edge_net_h20)} ATR)", 1, "height_toll_verdict.parquet 5m POOLED:CLASSIC5 frozen3.0 holdout")
    bs = C["rows"]["P-BRK-S1"]["beside_registration"]["brk_sealed_row"]
    t(f"(median {bs['toll_pct_of_1r_median']:.2f}% of 1R)", 1,
      "P-BRK-S1.rows.json beside_registration.brk_sealed_row.toll_pct_of_1r_median")
    # THE ONE THAT CLEARS
    t(f"{ss['pre']['n']} of its {ss['book']['n']} campaigns", 1, "P_TRG_2_SEEN_SHARE.json pre.n, book.n")
    t(f"({ss['tc9_asof']['iso']})", 1, "P_TRG_2_SEEN_SHARE.json tc9_asof.iso")
    t(f"re-net {f4(ss['pre']['net_r'])} R", 1, "P_TRG_2_SEEN_SHARE.json pre.net_r")
    t(f"({ss['keys_vs_tc9_filed_v6_journal']['shared']} shared)", 1,
      "P_TRG_2_SEEN_SHARE.json keys_vs_tc9_filed_v6_journal.shared")
    m = re.search(r"^FIXTURE SUMMARY (\d+)/(\d+) GREEN", C["ss_fix"], re.M)
    t(f"F-SS {m.group(1)}/{m.group(2)} GREEN" if m else "<no F-SS summary>", 1,
      "close/FIXTURES_CLOSE_p_trg_2_seen_share.txt FIXTURE SUMMARY")
    t(f"holds {ss['post']['n']} of its campaigns", 1, "P_TRG_2_SEEN_SHARE.json post.n")
    t(f"and {len(fs)} of v6's" if len(fs) == ss["v6_base_vs_tc9_filed"]["here_post_n"] else "<strip != seen-share>", 1,
      "FORWARD_STRIP.parquet rows == P_TRG_2_SEEN_SHARE.json v6 here_post_n")
    s = sr(C, "P-TRG-2", 2)
    t(f"Δ {f6(s['ci_point'])},", 1, "P-TRG-2.rows.json rows[2].score_row.ci_point")
    t(f"{ci(s)}, LOAO {s['loao_line']}.", 1, "P-TRG-2.rows.json rows[2].score_row")
    e = ss["era_cut"]
    t(f"{e['book_holdout_inside_tc9']} of the book's {e['book_holdout_n']}", 1, "P_TRG_2_SEEN_SHARE.json era_cut")
    r = C["cr"].iloc[0]
    t(f"(v6 vs zero {ci(r)},", 1, "panel/control_reference.parquet ci_lo, ci_hi")
    t(f"{f4(par(C, 'P-TRG-2', 0, 'ZECUSDT')['net_r'])} of its {f4(sr(C, 'P-TRG-2')['net_r'])} R", 1,
      "P-TRG-2.rows.json per_asset_rows ZECUSDT net_r; score_row.net_r")
    # RS rulings
    d = re.search(r"^## (\d{4}-\d{2}-\d{2}) — Range-and-Structure layer", C["ledger_md"], re.M)
    t(f"THE {d.group(1)} RS RULINGS" if d else "<no RS heading>", 1, "LEDGER.md RS heading")
    eda = sorted(set(C["ah"].engine_default_after))
    t(f'"{eda[0]}"' if len(eda) == 1 else "<engine_default_after not single>", 1,
      "acceptance_head_to_head.parquet engine_default_after (single value)")
    t(f"on all {len(C['ah']):,} rows", 1, "acceptance_head_to_head.parquet rows")
    sh = {L: re.search(rf"^- \*\*{L}\*\*: margin [\d,]+ \((\d+\.\d)%\)", C["s2"], re.M) for L in ("1d", "4h", "5m")}
    t(" / ".join(f"{sh[L].group(1)}%" for L in ("1d", "4h", "5m")) if all(sh.values()) else "<no shares>", 1,
      "close/S2_CENSUS_R.md §2.1 'margin N (x%)' lines")
    ho = {sc: single_passes(C, "5m", "holdout", sc) for sc in ("frozen3.0", "calibrated")}
    al = {sc: single_passes(C, "5m", "ALL", sc) for sc in ("frozen3.0", "calibrated")}
    t(f"pass {ho['frozen3.0']}/17 on the holdout and {al['frozen3.0']}/17 on ALL"
      if len(set(ho.values())) == 1 and len(set(al.values())) == 1 else "<scales disagree>", 1,
      "height_toll_verdict.parquet 5m single-asset, both scales")
    t(f"({single_passes(C, '5m', 'tuning', 'frozen3.0')}/17 frozen3.0, "
      f"{single_passes(C, '5m', 'tuning', 'calibrated')}/17 calibrated)", 1,
      "height_toll_verdict.parquet 5m single-asset tuning")
    hv = C["htv"]
    p4 = hv[(hv.lens == "4h") & (hv.asset.str.startswith("POOLED")) & (hv.verdict_pass)]
    one = p4.iloc[0] if len(p4) == 1 else None
    t(f"({one.asset.split(':')[1]} {one.era}, {one.scale_kind}, {f4(one.edge_net_h20)})" if one is not None
      else "<pooled 4h passes != 1>", 1, "height_toll_verdict.parquet 4h pooled passes")
    s4 = int(hv[(hv.lens == "4h") & (~hv.asset.str.startswith("POOLED")) & (hv.verdict_pass)].shape[0])
    hold = hv[(hv.era == "holdout") & (hv.verdict_pass)]
    t(f"({s4} at 4h; {int((~hold.asset.str.startswith('POOLED')).sum())} of the {len(hold)}", 1,
      "height_toll_verdict.parquet single-asset 4h passes; holdout passes")
    t(f"over {len(hv)} rows", 1, "height_toll_verdict.parquet rows")
    t(f"history ({f4(htv_row(C, '1d', 'POOLED:CLASSIC5', 'ALL').edge_net_h20)})", 1,
      "height_toll_verdict.parquet 1d POOLED:CLASSIC5 frozen3.0 ALL")
    t(f"reverses on the holdout ({f4(htv_row(C, '1d', 'POOLED:CLASSIC5', 'holdout').edge_net_h20)})", 1,
      "height_toll_verdict.parquet 1d POOLED:CLASSIC5 frozen3.0 holdout")
    # slippage twin
    ti = C["fee"]["haircut_twin_tiers"]
    t(f"tier A {ti['A']['bps_per_side']} / B {ti['B']['bps_per_side']} / C {ti['C']['bps_per_side']} bps", 1,
      "fee_schedule.json haircut_twin_tiers")
    rt = sorted({a["haircut_twin_round_trip_bps"] for a in C["fee"]["assets"]})
    t(" / ".join(str(x) for x in rt) + " bps", 1, "fee_schedule.json assets[].haircut_twin_round_trip_bps")
    tc = sorted({a["round_trip_bps_used"] for a in C["fee"]["assets"]})
    t(f"{tc[0]} bps, which is left untouched" if len(tc) == 1 else "<tc toll not single>", 1,
      "fee_schedule.json assets[].round_trip_bps_used")
    v = C["s5"]["measured"]["ii"]["value"]
    t(f"{v['twin_above_tc']} of {v['arms_with_twin']} arms", 1, "S5_FINDINGS_NOT_FIXED.json measured.ii.value")
    t(f"{f6(tw['twin_expectancy_r'])} against {f6(tw['tc_expectancy_r'])}", 1,
      "P-TRG-2.rows.json rows[0].beside.haircut_twin")
    q = C["v6"][(C["v6"].era == "tuning") & (C["v6"].key == "ALL")].iloc[0]
    t(f"TC {f6(q.tc_expectancy_r)}, twin {f6(q.twin_expectancy_r)}, with funding {f6(q.companion_expectancy_r)}", 1,
      "V6_CONTROL_HAIRCUT_TWIN.parquet era tuning, key ALL")
    tws = [x["beside"]["haircut_twin"] for reg in REGS for x in C["rows"][reg]["rows"]
           if x.get("beside") and x["beside"].get("haircut_twin")]
    t(f"({sum(bool(x['sign_disagrees_with_tc']) for x in tws)}/{len(tws)})", 1,
      "rows.json beside.haircut_twin.sign_disagrees_with_tc, every twin row")
    # also filed
    t(f"{C['og_m'][0]:,} outcome cells" if len(C["og_m"]) == 1 else "<m not single>", 1,
      "outcome_grid.parquet m_looks_this_table")
    adm = C["man"]["admission"]
    cls = C["dsa"]["classes"]
    scored = set(cls["scored"])
    unseen = [x for x in adm["rows"] if x["asset"] not in scored]
    classic = [x for x in adm["rows"] if x["asset"] in scored]
    t(f"Admitted {sum(x['admitted'] for x in unseen)}/{len(unseen)} (P-GEN-1's panel) + CLASSIC5 "
      f"{sum(x['admitted'] for x in classic)}/{len(classic)}; " + ("none excluded" if not adm["excluded"] else "SOME EXCLUDED"),
      1, "STAGE_D_MANIFEST.json admission rows, excluded; DATA_SPEND_AUDIT classes")
    t(f"v6 after TC9's as-of, {len(fs)} campaigns.", 1, "FORWARD_STRIP.parquet rows")
    op = fs[fs.exit_reason == "corridor_end"]
    cl = fs[fs.exit_reason != "corridor_end"]
    t(f"{len(cl)} closed for {f6(cl.net_r.sum())} R; {len(op)} open, marked {f6(op.net_r.sum())} R", 1,
      "FORWARD_STRIP.parquet net_r by exit_reason")
    m = re.search(r"F-D-4 RE-MEASURED: cells \*\*(\d+)\*\* · bars before a floor \*\*(\d+)\*\*", C["s3"])
    t(f"F-D-4: {m.group(1)} cells, {m.group(2)} pre-floor bars." if m else "<no F-D-4 tally>", 1,
      "close/S3_STAGE_D.md 'F-D-4 RE-MEASURED'")
    # integrity
    st = [x["status"] for x in C["prog"]["stages"]]
    t(f"{len(st)} stages: {st.count('COMPLETE-VERIFIED')} COMPLETE-VERIFIED, {st.count('PARTIAL')} PARTIAL", 1,
      "PROGRESS.json stages[].status")
    v6 = ss["v6_base_vs_tc9_filed"]
    t(f"re-nets {f4(v6['here_pre_net_r'])} R", 1, "P_TRG_2_SEEN_SHARE.json v6_base_vs_tc9_filed.here_pre_net_r")
    t(f"TC9's filed {f4(v6['tc9_filed_net_r'])} R", 1, "P_TRG_2_SEEN_SHARE.json v6_base_vs_tc9_filed.tc9_filed_net_r")
    t(f"all {C['s5']['measured']['v']['value']['worktrees_besides_main']} review worktrees", 1,
      "S5_FINDINGS_NOT_FIXED.json measured.v.value.worktrees_besides_main")
    iso, ms = era_ms(C)
    t(f"({ms} ms = {iso})", 1, "scripts/tierc10_panel.py ERA_CUT_ISO (and its ms)")
    t(f"(P-TRG-2, {ss['pre']['n']}/{ss['book']['n']} SEEN)", 1,
      "P_TRG_2_SEEN_SHARE.json pre.n, book.n")
    if not C.get("stamp_pending", True):
        n, m = git_counts()
        t(f"{n} tierc10 commits, {m} on a remote", 1,
          "git: commits on HEAD whose subject starts 'tierc10'; of those, the ones some remote-tracking ref contains")
    return T


def git_counts() -> tuple:
    def g(*a):
        return subprocess.run(["git", *a], cwd=str(ROOT), capture_output=True, text=True, check=True).stdout
    tc = [ln.split("\t", 1)[0] for ln in g("log", "--format=%H%x09%s", "HEAD").splitlines()
          if ln.split("\t", 1)[-1].startswith("tierc10")]
    off = set(g("rev-list", "HEAD", "--not", "--remotes").split())
    return len(tc), sum(1 for h in tc if h not in off)


# ═══════════════════════════════════════════════════════════════ claims (words the prose asserts)
def claims(C) -> list:
    fam, ss, hv = C["fam"], C["ss"], C["htv"]
    out = []
    c = lambda name, ok, det: out.append((name, bool(ok), det))           # noqa: E731
    a = C["ah"]
    x = a[(a.asset == "POOLED:ALL") & (a.lens == "5m") & (a.scale_kind == "frozen3.0") & (a.era == "ALL")
          & (a.horizon == "H20")]
    c("At 5m all five rules are net negative", len(x) == 5 and (x.net < 0).all(), f"{len(x)} rules, nets {sorted(x.net.round(4))}")
    nt = [par(C, "P-GEN-1", 2, k)["expectancy_r"] for k in ("PUMPUSDT", "MNTUSDT_BYBIT", "SUIUSDT")]
    c("each never-touched asset negative / ALL SIT BELOW ZERO", all(v < 0 for v in nt)
      and "3/3 BELOW" in sr(C, "P-GEN-1", 2)["loao_line"], f"{nt}")
    c("the unseen month's campaigns both stopped out",
      ss["post"]["campaigns"] and all(p["exit_reason"] == "stop" for p in ss["post"]["campaigns"]),
      [p["exit_reason"] for p in ss["post"]["campaigns"]])
    s = sr(C, "P-BRK-S1")
    c("the time-holdout scalper's CI lies wholly below zero", s["ci_hi"] < 0 and s["arm_era"] == "holdout",
      f"ci_hi {s['ci_hi']} era {s['arm_era']}")
    g = fam["rows"][0]
    c("P-GEN-1 (the out-of-asset test) did not clear", g["registration"] == "P-GEN-1"
      and g["verdict"] != "SUPPORTED" and g["clears_bh_bar"] is False, f"{g['verdict']} bh {g['clears_bh_bar']}")
    sup = [r["registration"] for r in fam["rows"] if r["scored_in_family"] and r["verdict"] == "SUPPORTED"]
    c("ONE cell clears its own bar, and it is P-TRG-2", sup == ["P-TRG-2"], sup)
    t = fam["rows"][10]
    c("P-TRG-2: LOAO and the BH column both clear", t["registration"] == "P-TRG-2"
      and t["loao_clears_line_of_record"] is True and t["clears_bh_bar"] is True,
      f"loao {t['loao_clears_line_of_record']} bh {t['clears_bh_bar']}")
    be = [sr(C, "P-BE-1", i) for i in (1, 2, 3)]
    c("P-BE-1's Tier-E arms all straddle zero", all(b["ci_lo"] < 0 < b["ci_hi"] for b in be),
      [(b["ci_lo"], b["ci_hi"]) for b in be])
    p5 = hv[(hv.lens == "5m") & (hv.asset.str.startswith("POOLED")) & (hv.verdict_pass)]
    c("no range-trading contract at 5m on any pool (0 pooled 5m passes)", len(p5) == 0, len(p5))
    h1a, h1h = htv_row(C, "1d", "POOLED:CLASSIC5", "ALL"), htv_row(C, "1d", "POOLED:CLASSIC5", "holdout")
    c("P-BRK-I1's 1d gate PASSES on ALL and FAILS on the holdout", h1a.verdict_pass and not h1h.verdict_pass,
      f"{h1a.verdict_pass}/{h1h.verdict_pass}")
    h5 = htv_row(C, "5m", "POOLED:CLASSIC5", "holdout")
    c("P-BRK-S1's 5m gate: height PASS, edge-fade FAIL", h5.gate_height_pass and not h5.gate_edge_fade_pass,
      f"{h5.gate_height_pass}/{h5.gate_edge_fade_pass}")
    c("the 1d CLASSIC5 pool pass on ALL is the one 1d pass on full history",
      int(hv[(hv.lens == "1d") & (hv.era == "ALL") & (hv.verdict_pass)].shape[0]) == 1 and h1a.verdict_pass, "")
    head = C["pin"]["registry_head"]
    c("registry head 7621a857… is REGISTRY_PIN's", head.startswith("7621a857"), head[:16])
    wt = C["s5"]["measured"]["v"]["heads_besides_main"]
    c("every review worktree at a6da1b9", len(wt) == 1 and wt[0]["head"].startswith("a6da1b9"), wt[0]["head"][:12])
    r = subprocess.run(["git", "log", "-1", "--format=%s", "371123f"], cwd=str(ROOT), capture_output=True, text=True)
    c("371123f is the filing commit", r.returncode == 0 and "six registrations are FILED" in r.stdout, r.stdout.strip()[:90])
    lean = C["rulings"].split("## Operationalisation (EXECUTOR LEANS")[1].split("\n## ")[0] \
        if "## Operationalisation (EXECUTOR LEANS" in C["rulings"] else ""
    c("the LaCie path is an EXECUTOR LEAN, not the operator's words",
      "/Volumes/LaCie/Repo Clone/naiad-backups" in lean
      and "/Volumes/LaCie" not in C["rulings"].split("## Verbatim")[1].split("## Operationalisation")[0], "")
    ones = {x["stage"]: x["one_line"] for x in C["prog"]["stages"]}
    c("D-CORE and D-5M are PARTIAL on F-D-1 alone", "PARTIAL because F-D-1" in ones.get("D-CORE", "")
      and "PARTIAL only on F-D-1" in ones.get("D-5M", ""), "")
    c("F-SS's seen share reproduces the grid and the key overlap", ss["grid_all_equal"] and ss["keys_all_equal"]
      and ss["book"]["equal_dryrun"] and ss["book"]["equal_rows_json"], "")
    return out


# ═══════════════════════════════════════════════════════════════ text model
def cite_spans(block: str) -> list:
    """Line ranges (0-based, inclusive) of every «cite» line and its quote lines."""
    lines = block.split("\n")
    spans, i = [], 0
    while i < len(lines):
        m = LA.CITE_RE.match(lines[i])
        if not m:
            i += 1
            continue
        qre = re.compile("^" + " " * (len(m.group(1)) + 2) + r"[|+] ")
        j = i + 1
        while j < len(lines) and qre.match(lines[j]):
            j += 1
        spans.append((i, j - 1))
        i = j
    return spans


def prose_of(block: str) -> str:
    """The block with every cite/quote line blanked (same length per line, so
    offsets hold), and every pending stamp blanked."""
    lines = block.split("\n")
    for a, b in cite_spans(block):
        for k in range(a, b + 1):
            lines[k] = " " * len(lines[k])
    out = "\n".join(lines)
    return STAMP_RE.sub(lambda m: " " * len(m.group(0)), out)


DATE_RE = re.compile(r"(?<![\w])\d{4}-\d{2}-\d{2}(?:T\d{2}:\d{2}(?::\d{2})?Z)?")
MASKS = [re.compile(r"§[\d.]+(?:\([a-z]\))?"),                       # section signs
         re.compile(r"[A-Za-z_]\w*\[\d+\]"),                          # JSON selectors
         re.compile(r"(?<![\w.])[A-Za-z0-9_]*[A-Za-z][A-Za-z0-9_]*(?:[-.][A-Za-z0-9_]+)*"),  # identifiers w/ a letter
         re.compile(r"(?<![\w.])[0-9_]+(?:[-.][A-Za-z0-9_]+)*[-.][A-Za-z0-9_]*[A-Za-z][A-Za-z0-9_]*")]  # 8-close, 1d-…


def coverage(block: str, T: list, exempt: list) -> tuple:
    prose = prose_of(block)
    covered = [False] * len(prose)

    def cover(s, e):
        for k in range(s, e):
            covered[k] = True
    for lit, _n, _src in T:
        for m in re.finditer(re.escape(lit), prose):
            cover(m.start(), m.end())
    for lit, _n, _why in exempt:
        for m in re.finditer(re.escape(lit), prose):
            cover(m.start(), m.end())
    dates = [(m.start(), m.end(), m.group(0)) for m in DATE_RE.finditer(prose)]
    undated = list(prose)
    for s, e, _ in dates:
        for k in range(s, e):
            undated[k] = "#"                                   # dates are NOT masked; kept for the digit scan
    masked_text = "".join(undated)
    for rx in MASKS:
        for m in rx.finditer(masked_text):
            if not re.search(r"[A-Za-z§\[]", m.group(0)):
                continue
            cover(m.start(), m.end())
    loose = [f"exemption {lit!r}: in prose {prose.count(lit)}x, declared {n}x"
             for lit, n, _why in exempt if prose.count(lit) != n]
    for m in re.finditer(r"\d+", prose):
        if not all(covered[k] for k in range(m.start(), m.end())):
            ln = prose.count("\n", 0, m.start()) + 1
            ctx = prose.split("\n")[ln - 1].strip()
            loose.append(f"line {ln}: '{m.group(0)}' in «{ctx[:70]}»")
    return (not loose), ("every digit in the prose lies inside a traced literal, a masked token or a listed "
                         "exemption" if not loose else loose)


# ═══════════════════════════════════════════════════════════════ checks
def check_format(block: str) -> tuple:
    probs = []
    if not block.startswith(SEP):
        probs.append(f"does not open with the ledger's separator {SEP!r}")
    body = block[len(SEP):]
    if not re.match(r"=== STATUS_APOLLO — \d{4}-\d{2}-\d{2} — TIER-C\d+ · [^\n]+ ===\n"
                    r"LANE      [^\n]+\nCLASS     ", body):
        probs.append("header / LANE / CLASS lines do not mirror the ledger's blocks")
    if not block.endswith("\n=== END ===\n") or block.count("=== END ===") != 1:
        probs.append("does not END on exactly one '=== END ===' line with nothing after it")
    if "Operator: click Sync now." in block:
        probs.append("the session's final line is inside the appended bytes")
    return (not probs), ("opens on '\\n---\\n\\n'; header / LANE / CLASS mirror the ledger; ends on one "
                         "'=== END ===' with nothing after; no session line inside" if not probs else "; ".join(probs))


def check_cites(block: str, src: dict) -> tuple:
    qs = LA.parse_quotes(block)
    bad = []
    for q in qs:
        ok, why = LA.verify_quote(q, src)
        if not ok:
            bad.append(f"line {q['at']} {LA.cite_of(q)}: {why}")
    return (bool(qs) and not bad), (f"{len(qs)} quote(s) verify through F-LA's verify_quote" if not bad
                                     else f"{len(bad)} bad: {bad[:2]}")


REQUIRED = [("Q6 hold :2-3", CONTRACT_REL, 2, 3), ("Q6 phrase :137", CONTRACT_REL, 137, 137),
            ("RS heading", "LEDGER.md", 829, 829), ("Q-R3", "LEDGER.md", 834, 834),
            ("Q-R4", "LEDGER.md", 835, 835), ("Q-R5", "LEDGER.md", 836, 836),
            ("CENSUS-3 next :139", CONTRACT_REL, 139, 139), ("TC9's last word", "exchange/status/LEDGER_APOLLO.md", 2422, 2423)]


def check_required(block: str, C) -> tuple:
    qs = LA.parse_quotes(block)
    miss = [n for n, p, a, b in REQUIRED if not any(q["path"] == p and q["l1"] == a and q["l2"] == b for q in qs)]
    norm = " ".join(prose_of(block).split())
    if " ".join(LA.QUESTION.split()) not in norm:
        miss.append("the slippage-twin question, verbatim")
    if f"m = {C['fam']['family_m_declared']}" not in block:
        miss.append("m = family_m_declared")
    if "CENSUS-3" not in prose_of(block):
        miss.append("NEXT · CENSUS-3")
    return (not miss), ("the contract's five commissioned items (Q6 verbatim · m · the 07-29 RS rulings · the "
                        "slippage-twin question · CENSUS-3 next) and TC9's last word are present"
                        if not miss else f"missing: {miss}")


def check_trace(block: str, T: list) -> tuple:
    prose = prose_of(block)
    bad = []
    for lit, n, src in T:
        if lit.startswith("<"):
            bad.append(f"{src}: source check failed {lit}")
            continue
        if not re.search(r"\D", lit):
            bad.append(f"{lit!r}: a trace literal must carry context, not a bare number")
            continue
        got = prose.count(lit)
        if got != n:
            bad.append(f"{lit!r} [{src}]: in prose {got}x, declared {n}x")
    return (not bad), (f"{len(T)} traced literals, each equal to its source and present its declared number of times"
                       if not bad else f"{len(bad)} bad: {bad[:3]}")


def check_claims(CL: list) -> tuple:
    bad = [f"{n} ({d})" for n, ok, d in CL if not ok]
    return (not bad), (f"{len(CL)} word claims hold against their sources" if not bad else f"FALSE: {bad[:3]}")


def check_stamps(block: str) -> tuple:
    st = STAMP_RE.findall(block)
    opened = block.count("⟦")
    if len(st) != opened or not all("STAMP AT CLOSE" in s for s in st):
        return False, f"malformed stamp: {opened} opened, {len(st)} well-formed"
    if st:
        return True, (f"{len(st)} PENDING stamp(s), each '⟦STAMP AT CLOSE …⟧', none certified — fill, then re-run: "
                      + "; ".join(s[:60] for s in st))
    return True, "0 pending stamps: every number in the block is traced"


def plant(block, old, new):
    if old not in block:
        raise SystemExit(f"HALT: sabotage anchor {old!r} is not in the block")
    return block.replace(old, new, 1)


# ═══════════════════════════════════════════════════════════════ run
RESULTS: dict = {}


def leg(name, fails_if, real, sabs):
    say(f"{name} · FAILS IF {fails_if}")
    ok, det = real
    say(f"  real      {'GREEN' if ok else 'RED'} — {det}")
    all_red = bool(sabs)
    for d, (sok, sdet) in sabs:
        all_red &= not sok
        say(f"  sabotage  {d}: {'RED (as required)' if not sok else 'GREEN — THE LEG IS BLIND'} — {str(sdet)[:220]}")
    RESULTS[name] = bool(ok and all_red)
    say(f"  => {name} {'GREEN' if RESULTS[name] else 'RED'}")
    say("")


def run(det_only_dir: str | None) -> int:
    block_b = ROOT_APPEND.read_bytes()
    block = block_b.decode("utf-8")
    led_before = sha_b(LEDGER_APOLLO.read_bytes())
    C = load()
    C["stamp_pending"] = bool(STAMP_RE.search(block))
    T = traces(C)
    CL = claims(C)
    say("TIER-C10 · CLOSE · F-LAR — THE LEDGER_APOLLO APPEND OF RECORD, CERTIFIED")
    say("REPORT-ONLY: reads the root append and its sources; writes nothing under exchange/ and never the root file")
    say(f"APPEND OF RECORD (sha256 · bytes): {sha_b(block_b)} · {len(block_b)} · "
        f"{ROOT_APPEND.relative_to(ROOT)}")
    if SCRIPT_DRAFT.exists():
        sd = SCRIPT_DRAFT.read_bytes()
        say(f"NOT THE APPEND: {SCRIPT_DRAFT.relative_to(ROOT)} (F-LA's source-quote render) {sha_b(sd)} · {len(sd)}")
    say("SOURCES READ (sha256[:16] · bytes · path)")
    for rel, (h, n) in sorted(C["read"].items()):
        say(f"  {h[:16]} · {n} · {rel}")
    say("TRACE TABLE (literal ⇐ source)")
    for lit, n, srcd in T:
        say(f"  {lit!r} ×{n} ⇐ {srcd}")
    say("EXEMPTIONS (literal ×count — reason)")
    for lit, n, why in EXEMPT:
        say(f"  {lit!r} ×{n} — {why}")
    say("")
    src = C["src"]

    leg("F-LAR-FORMAT", "the block does not open on the ledger separator, mirror the header / LANE / CLASS lines, "
        "end on exactly one '=== END ===' with nothing after it, or carries the session's final line",
        check_format(block),
        [("the session line appended after END", check_format(block + "Operator: click Sync now.\n")),
         ("the END line dropped", check_format(plant(block, "=== END ===\n", "")))])
    leg("F-LAR-CITE", "any «cite» in the block does not verify against its source (F-LA's own verify_quote)",
        check_cites(block, src),
        [("TC9's last word bent (NINE -> TEN)", check_cites(plant(block, "| NINE TIERS", "| TEN TIERS"), src)),
         ("a cite re-pointed (:2-3 -> :3-4)", check_cites(plant(block, "APOLLO.md:2-3»", "APOLLO.md:3-4»"), src))])
    leg("F-LAR-REQUIRED", "a commissioned item (contract :137-139) or TC9's last word is absent",
        check_required(block, C),
        [("CENSUS-3's cite removed", check_required(plant(block, "«exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md:139»\n"
                                                           "      | CENSUS-3 next.\n", ""), C)),
         ("the question re-worded", check_required(plant(block, "must the twin carry funding?",
                                                         "should the twin carry funding?"), C))])
    leg("F-LAR-TRACE", "a traced literal differs from its source, or is present other than its declared number of times",
        check_trace(block, T),
        [("P-GEN-1's point bent (+0.099777 -> +0.099778)", check_trace(plant(block, "+0.099777", "+0.099778"), T)),
         ("the seen share bent (196 of its 198 -> 197 of its 198)",
          check_trace(plant(block, "196 of its 198", "197 of its 198"), T)),
         ("a traced literal duplicated", check_trace(plant(block, "=== END ===", "(0/20)\n=== END ==="), T))])
    leg("F-LAR-COVER", "any digit in the prose is covered by no trace, mask or exemption",
        coverage(block, T, EXEMPT),
        [("an untraced number planted (n 999)", coverage(plant(block, "Named, not fixed.", "Named, n 999."), T, EXEMPT)),
         ("an untraced date planted", coverage(plant(block, "Named, not fixed.", "Named 2026-09-30."), T, EXEMPT))])
    CLb = claims(dict(C, rows=dict(C["rows"], **{"P-GEN-1": _flip_pump(C["rows"]["P-GEN-1"])})))
    leg("F-LAR-CLAIM", "a word claim of the prose is false against its source",
        check_claims(CL), [("a copy where PUMP's never-touched expectancy is positive", check_claims(CLb))])
    leg("F-LAR-STAMP", "a pending stamp is malformed (unclosed, or not '⟦STAMP AT CLOSE …⟧')",
        check_stamps(block), [("an unclosed stamp", check_stamps(block.replace("then re-run F-LAR⟧", "then re-run F-LAR")))])
    led_after = sha_b(LEDGER_APOLLO.read_bytes())
    root_after = sha_b(ROOT_APPEND.read_bytes())
    g_ok, _ = _guard([TRANSCRIPT])
    s_ok, s_bad = _guard([LEDGER_APOLLO])
    leg("F-LAR-NOWRITE", "LEDGER_APOLLO.md or the root append changes during the run, or an output leaves close/",
        (led_before == led_after and root_after == sha_b(block_b) and g_ok,
         f"LEDGER_APOLLO.md {led_before[:16]}… unchanged; the root append unchanged; output under close/ only"),
        [("an output path under exchange/status/", (s_ok, f"guard refuses {s_bad}"))])
    core = ("\n".join(LINES) + "\n").encode("utf-8")
    if det_only_dir is not None:
        out = Path(det_only_dir) / TRANSCRIPT.name
        ok, bad = _guard([out])
        if not ok:
            raise SystemExit(f"HALT: output outside close/: {bad}")
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(core)
        return 0 if all(RESULTS.values()) else 1
    outs = {}
    for seed in DET_SEEDS:
        d = DET_ROOT / f"seed_{seed}"
        env = dict(os.environ, PYTHONHASHSEED=str(seed), NAIAD_CACHE_DIR=str(SNAPSHOT), PYTHONDONTWRITEBYTECODE="1")
        r = subprocess.run([sys.executable, str(Path(__file__).resolve()), "--det-dir", str(d)], env=env,
                           capture_output=True, text=True, cwd=str(ROOT))
        p = d / TRANSCRIPT.name
        outs[seed] = (r.returncode, p.read_bytes() if p.exists() else b"")
    same = outs[DET_SEEDS[0]][1] == outs[DET_SEEDS[1]][1] == core
    leg("F-DET", "two subprocess runs (PYTHONHASHSEED 1, 20260921) print a different transcript through "
        "F-LAR-NOWRITE, or differ from this run's",
        (same, f"exit {[o[0] for o in outs.values()]}; sha {sha_b(core)[:16]}…; all three byte-identical: {same}"),
        [("a process-dependent salt", (core == core + str(os.getpid()).encode(), "salted transcript differs"))])
    say(f"FIXTURE SUMMARY {sum(RESULTS.values())}/{len(RESULTS)} GREEN " + json.dumps(RESULTS))
    ok, bad = _guard([TRANSCRIPT])
    if not ok:
        raise SystemExit(f"HALT: output outside close/: {bad}")
    TRANSCRIPT.write_bytes(("\n".join(LINES) + "\n").encode("utf-8"))
    return 0 if all(RESULTS.values()) else 1


def _flip_pump(rows_doc: dict) -> dict:
    d = json.loads(json.dumps(rows_doc))
    for x in d["rows"][2]["beside"]["per_asset_rows"]:
        if x.get("key") == "PUMPUSDT":
            x["expectancy_r"] = abs(x["expectancy_r"])
    return d


def _guard(paths) -> tuple:
    bad = [str(p) for p in paths if OUT.resolve() not in Path(p).resolve().parents]
    return (not bad), bad


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--det-dir", default=None)
    a = ap.parse_args()
    if a.det_dir and DET_ROOT.resolve() not in Path(a.det_dir).resolve().parents:
        raise SystemExit(f"HALT: --det-dir must lie under {DET_ROOT}")
    return run(a.det_dir)


if __name__ == "__main__":
    sys.exit(main())
