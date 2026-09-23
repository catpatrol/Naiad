#!/usr/bin/env python
"""TIER-C10 · CLOSE · REGIME-PRIOR — TIER-E TABLES ONLY (report-only).

RATIFIED operator 2026-09-21 (TIER-C10) + 2026-09-22 (RESUME-AND-FINISH,
exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md).  Drafted APOLLO, executed
HEPHAESTUS; seed 20260921 (nothing here draws at random).  The contract names
this item once, and names its form in the same breath:

    P-AGE-1 (tide-youth), boundary-fade, regime-prior: Tier-E tables only.

WHAT THIS FILE BUILDS (and nothing else)
  TABLE 1 · REGIME_PRIOR_TIME_IN_RANGE.parquet — time-in-range per
    asset x lens x scale_kind: the CENSUS-R coverage rows COPIED VERBATIM
    (bars_in_live_range_pct, coverage_pct, n_bars, scale_mult, coverage_law,
    every as_of_* column, warranty, tier, in_sample).  NO NEW POOLING: no value
    is averaged, summed or ranked across assets, lenses or scale kinds.
  TABLE 2 · REGIME_PRIOR_V6_BY_STATE.parquet — the v6 CLASSIC5 book (the KNOWN
    CONTROL, panel/control_journal.parquet) crossed by the Stage-A stamp
    rf4h_macro_state AT ENTRY x AT EXIT, plus rf4h_in_range at each, with n,
    n_assets, net_r_sum, expectancy_r, win_rate_pct.  The declared grid is
    whole (every state x in_range pair at both ends, zeros filed), then the
    entry-state marginal, the exit-state marginal and __ALL__.
  REGIME_PRIOR.md — both tables, labelled, with the ARGUS note's item 2
    QUOTED WHOLE.  It is never parsed: no number in it becomes a threshold,
    and no row of either table is compared with it.

THE JOIN LAW (Table 2).  A journal campaign's ENTRY stamp is the stamp with
  (asset, instant_ms == entry_ms, instant_kind == 'entry'); its EXIT stamp is
  the stamp carrying that entry stamp's campaign_id with instant_kind ==
  'exit'.  Each campaign must have exactly one of each, every entry/exit stamp
  must join a campaign, and each exit stamp must sit on its campaign's journal
  exit_ms (F-RP-JOIN).  The build HALTS on any breach before a row is written.

THE COLLAR (both tables, every row): tier · selection_not_a_result ·
  m_selections_this_table (= the rows of the table: every row is one cut of
  the tape) · m_note · in_sample · gates = 'nothing'.  NO verdict / ci / p
  column exists; F-RP-COLLAR fails the moment one does.

WHAT THIS FILE NEVER DOES
  It never scores, never reads a registration, a .scored.json or scores/*,
  never consults any verdict, never refits a pin, never reads a bar (both
  tables are made from FILED parquet; tierc2_baseline is not imported), and
  never writes outside research_outputs/tierc10/close/ (or a --out directory
  outside the repo, which is what F-DET uses).  Every input is read-only and
  its sha256 is held against its PROGRESS.json stage record BEFORE it is read:
    census/coverage.parquet                   CENSUS-R{4h,1d}
    stamps/control_v6_stamped.parquet         A (stamps)
    stamps/control_entry_by_state.parquet     A (stamps)
    stamps/build_manifest.json                A (stamps)   (lens + SCALE_MULT)
    panel/control_journal.parquet             PANEL/gate
  plus the contract's sha against PROGRESS.json's contract_of_record, and the
  ARGUS note's bytes against its COMMITTED blob at HEAD.

HALTS IF: NAIAD_CACHE_DIR is unset, is the live cache, or is anything but the
  TC10 snapshot; PYTHONDONTWRITEBYTECODE is unset; any input sha differs from
  its record; the note's item 2 is not exactly one line; any gate
  (F-RP-JOIN / -ANCHOR / -VERBATIM / -EXIT-ASOF / -COLLAR / -QUOTE) is RED on
  the tables about to be written.

Run:
  export NAIAD_CACHE_DIR=/Users/luis/.cache/naiad/snapshots/tc10_20260921 \\
         PYTHONDONTWRITEBYTECODE=1
  ~/venvs/naiad/bin/python scripts/tierc10_close_regime_prior.py
  ~/venvs/naiad/bin/python scripts/tierc10_close_regime_prior_fixtures.py
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = Path.home() / ".cache" / "naiad" / "snapshots" / "tc10_20260921"
LIVE_CACHE = Path.home() / ".cache" / "naiad" / "data_cache"


def assert_substrate() -> Path:
    """THE FROZEN-SUBSTRATE GUARD [HARD LAW 3] — before any other import.

    HALTS IF: NAIAD_CACHE_DIR is unset, is the live cache, or is anything but
    the TC10 snapshot; or PYTHONDONTWRITEBYTECODE is unset.  Restated here
    (rather than imported) so this module halts on its own word and not on
    another module's import order.  This build reads no bar; the guard is
    the lineage's preamble and it runs anyway.
    """
    env = os.environ.get("NAIAD_CACHE_DIR", "")
    if not env:
        raise SystemExit("HALT: NAIAD_CACHE_DIR is unset — TC10 reads ONLY the "
                         f"snapshot {SNAPSHOT}")
    got = Path(env).expanduser().resolve()
    if got == LIVE_CACHE.resolve():
        raise SystemExit("HALT: NAIAD_CACHE_DIR is the LIVE cache — READ-NEVER, "
                         "WRITE-NEVER for TC10")
    if got != SNAPSHOT.resolve():
        raise SystemExit(f"HALT: NAIAD_CACHE_DIR={got} is not the TC10 snapshot "
                         f"{SNAPSHOT}")
    if not (got / "klines").is_dir():
        raise SystemExit(f"HALT: snapshot has no klines/ directory: {got}")
    if not os.environ.get("PYTHONDONTWRITEBYTECODE"):
        raise SystemExit("HALT: PYTHONDONTWRITEBYTECODE is unset — export it "
                         "BEFORE python starts")
    return got


assert_substrate()

import numpy as np                                                   # noqa: E402
import pandas as pd                                                  # noqa: E402

# ═══════════════════════════════════════════════════════════ 0 · PATHS
TC10 = ROOT / "research_outputs" / "tierc10"
OUT = TC10 / "close"
PROGRESS = TC10 / "PROGRESS.json"
CONTRACT_REL = "exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md"
ARGUS_REL = "exchange/reports/NOTE_ARGUS_to_APOLLO_2026-08-22_P-RNG_slate.md"
STAMPS_SRC_REL = "scripts/tierc10_stamps.py"
CENSUS_SRC_REL = "scripts/tierc10_census.py"

# (key, repo-relative path, the PROGRESS.json stage whose artifact_shas record it)
INPUTS = (
    ("coverage", "research_outputs/tierc10/census/coverage.parquet",
     "CENSUS-R{4h,1d}"),
    ("stamped", "research_outputs/tierc10/stamps/control_v6_stamped.parquet",
     "A (stamps)"),
    ("anchor", "research_outputs/tierc10/stamps/control_entry_by_state.parquet",
     "A (stamps)"),
    ("stamps_manifest", "research_outputs/tierc10/stamps/build_manifest.json",
     "A (stamps)"),
    ("journal", "research_outputs/tierc10/panel/control_journal.parquet",
     "PANEL/gate"),
)

T1_NAME = "REGIME_PRIOR_TIME_IN_RANGE.parquet"
T2_NAME = "REGIME_PRIOR_V6_BY_STATE.parquet"
MD_NAME = "REGIME_PRIOR.md"
FIX_NAME = "FIXTURES_CLOSE_regime_prior.txt"
OUTPUT_NAMES = (T1_NAME, T2_NAME, MD_NAME)

# ═══════════════════════════════════════════════════════════ 1 · THE COLLAR
T1_LABEL = ("REGIME-PRIOR · TABLE 1 · TIME-IN-RANGE per asset x lens x "
            "scale_kind · TIER-E · REPORT-ONLY")
T2_LABEL = ("REGIME-PRIOR · TABLE 2 · v6 CLASSIC5 BOOK x rf4h MACRO STATE AT "
            "ENTRY x AT EXIT · TIER-E · REPORT-ONLY")
TIER_T2 = "TIER-E MEASUREMENT — UNSCORED, GATES NOTHING"
GATES = "nothing"
SELECTION = ("a SELECTION, not a result — report-only; no row here is a test, "
             "a verdict or a lane, and no cell may be promoted to one")
IN_SAMPLE_T2 = ("IN-SAMPLE: the KNOWN CONTROL (card v6, frozen pins, CLASSIC5) "
                "over the full corridor — ridden by nine tiers; the stamps are "
                "new, the book is not")
COLLAR_COLS = ("tier", "selection_not_a_result", "m_selections_this_table",
               "in_sample", "gates")
# A column carrying any of these would be a verdict wearing a table's clothes.
FORBIDDEN_EXACT = frozenset({
    "verdict", "ci", "ci_lo", "ci_hi", "ci_low", "ci_high", "p", "p_value",
    "pvalue", "p_val", "q_value", "supported", "clears_bh_bar", "bh_bar",
    "significant"})
FORBIDDEN_PREFIX = ("ci_", "p_", "verdict")
FORBIDDEN_SUBSTR = ("verdict",)

# Table 1's verbatim columns: the key, the three values the spec names, the
# law that defines coverage_pct, every as_of_* column (discovered, in the
# census's own order), the warranty, and the census's own tier / in_sample.
T1_KEY = ["asset", "lens", "scale_kind"]
T1_CORE = ["asset", "lens", "scale_kind", "scale_mult", "n_bars", "coverage_pct",
           "bars_in_live_range_pct", "coverage_law"]
T1_TAIL = ["warranty", "tier", "in_sample"]
T1_ADDED = ["time_in_range_law", "argus_note_item_2", "selection_not_a_result",
            "m_selections_this_table", "m_note", "gates"]
TIME_IN_RANGE_LAW = (
    "bars_in_live_range_pct = 100 x the share of ALL bars of the tape at which "
    "a CONFIRMED macro range is alive in the census as-of view (confirm_i <= t "
    "< die_i; `in_range` of tierc10_census.asof_view, written by "
    "tierc10_census.compute_cell). coverage_pct follows its own coverage_law, "
    "copied verbatim on this row. Both are the census's numbers, not this "
    "build's.")

T2_KEY = ["cut", "entry_rf4h_macro_state", "entry_rf4h_in_range",
          "exit_rf4h_macro_state", "exit_rf4h_in_range"]
CUTS = ("CELL", "ENTRY_STATE_MARGINAL", "EXIT_STATE_MARGINAL", "ALL")
IN_RANGE_VOCAB = ("True", "False")
ALL = "__ALL__"
# Modules that read bars.  None may be imported by this build (checked before
# any write); tierc2_baseline.load_klines is the uncut 5m reader.
NO_BAR_MODULES = ("tierc2_baseline", "tierc10_data", "tierc10_census",
                  "tierc10_panel", "engine.data")


# ═══════════════════════════════════════════════════════════ 2 · SMALL LAWS
def log(msg: str = "") -> None:
    print(msg, flush=True)


def r6(x):
    """The lineage's r6 (tierc2_baseline.r6), restated so tierc2_baseline is
    never imported here: None for None / non-finite, else round(x, 6)."""
    return None if x is None or (isinstance(x, float) and not np.isfinite(x)) \
        else round(float(x) + 0.0, 6)


def sha256_path(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def ast_constant(rel: str, name: str):
    """A module-level literal READ from source by `ast` — never imported, so
    the vocabulary is the lineage's own object without pulling its closure."""
    tree = ast.parse((ROOT / rel).read_text())
    hits = [n for n in tree.body if isinstance(n, ast.Assign)
            and any(isinstance(t, ast.Name) and t.id == name for t in n.targets)]
    if len(hits) != 1:
        raise SystemExit(f"HALT: {rel} has {len(hits)} module-level "
                         f"assignment(s) to {name}; expected exactly 1")
    return ast.literal_eval(hits[0].value)


MACRO_STATES = tuple(ast_constant(STAMPS_SRC_REL, "MACRO_STATES"))
PROVISIONAL_MIN_N = int(ast_constant(CENSUS_SRC_REL, "PROVISIONAL_MIN_N"))


def git_blob_ok(rel: str) -> tuple[bool, str, str]:
    """(working bytes == committed blob at HEAD, working blob id, HEAD blob id)."""
    def run(*a):
        r = subprocess.run(["git", "-C", str(ROOT), *a], capture_output=True,
                           text=True)
        return r.returncode, r.stdout.strip()
    c1, head = run("rev-parse", f"HEAD:{rel}")
    c2, work = run("hash-object", rel)
    return (c1 == 0 and c2 == 0 and head == work and len(head) == 40), work, head


def progress_records() -> dict:
    return json.loads(PROGRESS.read_text())


def check_input_shas(overrides: dict | None = None) -> tuple[bool, list[str]]:
    """F-RP-SHA's check.  Each input's sha256 (read at `overrides[key]` when a
    fixture points it at a copy, else at its canonical path) against the
    artifact_shas record of its PROGRESS.json stage; plus the contract against
    contract_of_record and the ARGUS note against its committed blob."""
    overrides = overrides or {}
    prog = progress_records()
    stages = {s["stage"]: s for s in prog["stages"]}
    ok, lines = True, []
    for key, rel, stage in INPUTS:
        p = Path(overrides.get(key, ROOT / rel))
        rec = stages.get(stage, {}).get("artifact_shas", {}).get(rel)
        got = sha256_path(p) if p.is_file() else None
        want = rec.get("sha256") if isinstance(rec, dict) else None
        g = got is not None and want is not None and got == want
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] {rel}  stage {stage!r}  "
                     f"record {want}  disk {got}")
    rec = prog.get("contract_of_record", {})
    got = sha256_path(ROOT / CONTRACT_REL)
    g = rec.get("path") == CONTRACT_REL and rec.get("sha256") == got
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] {CONTRACT_REL}  contract_of_record "
                 f"{rec.get('sha256')}  disk {got}")
    g, work, head = git_blob_ok(ARGUS_REL)
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] {ARGUS_REL}  blob at HEAD {head}  "
                 f"working {work}")
    return ok, lines


def load_inputs() -> dict:
    ok, lines = check_input_shas()
    for s in lines:
        log(f"    {s}")
    if not ok:
        raise SystemExit("HALT (F-RP-SHA): an input differs from its record — "
                         "nothing is read past this line")
    d = {}
    for key, rel, _ in INPUTS:
        p = ROOT / rel
        d[key] = (json.loads(p.read_text()) if p.suffix == ".json"
                  else pd.read_parquet(p))
    return d


def contract_line() -> tuple[int, str]:
    lines = (ROOT / CONTRACT_REL).read_text().splitlines()
    hits = [(i + 1, s) for i, s in enumerate(lines) if "regime-prior" in s]
    if len(hits) != 1:
        raise SystemExit(f"HALT: the contract names 'regime-prior' on "
                         f"{len(hits)} lines; expected exactly 1")
    return hits[0]


def argus_item_2() -> str:
    """The note's item 2, WHOLE, as one line of the committed file.  Never
    parsed: this function returns text and nothing reads a number out of it."""
    lines = (ROOT / ARGUS_REL).read_text().splitlines()
    hits = [s for s in lines if s.startswith("2. ")]
    if len(hits) != 1:
        raise SystemExit(f"HALT: the ARGUS note has {len(hits)} lines starting "
                         "'2. '; expected exactly 1")
    return hits[0]


# ═══════════════════════════════════════════════════════════ 3 · TABLE 1
def t1_declared_columns(cov: pd.DataFrame) -> list[str]:
    as_of = [c for c in cov.columns if c.startswith("as_of_")]
    if not as_of:
        raise SystemExit("HALT: coverage.parquet carries no as_of_* column")
    return ["table"] + T1_CORE + as_of + T1_TAIL + T1_ADDED


def t1_verbatim_columns(cov: pd.DataFrame) -> list[str]:
    return [c for c in t1_declared_columns(cov)
            if c != "table" and c not in T1_ADDED]


def build_table1(cov: pd.DataFrame, quote: str) -> pd.DataFrame:
    """Coverage rows COPIED VERBATIM, in the census's own row order; the collar
    and two text columns are added beside them.  No value is recomputed."""
    miss = [c for c in t1_verbatim_columns(cov) if c not in cov.columns]
    if miss:
        raise SystemExit(f"HALT: coverage.parquet lacks {miss}")
    if int(cov.duplicated(subset=T1_KEY).sum()):
        raise SystemExit(f"HALT: coverage.parquet is not unique on {T1_KEY}")
    t = cov[t1_verbatim_columns(cov)].copy().reset_index(drop=True)
    n = len(t)
    m_cov = sorted({int(x) for x in cov["m_looks_this_table"]})
    t.insert(0, "table", T1_LABEL)
    t["time_in_range_law"] = TIME_IN_RANGE_LAW
    t["argus_note_item_2"] = quote
    t["selection_not_a_result"] = SELECTION
    t["m_selections_this_table"] = n
    t["m_note"] = (
        f"m = {n} selections in this table ({t['asset'].nunique()} asset(s) x "
        f"{t['lens'].nunique()} lens(es) x {t['scale_kind'].nunique()} scale "
        f"kind(s)), each a CENSUS-R coverage row copied verbatim — the census "
        f"logged m_looks_this_table = {m_cov} for the same rows. NO "
        "multiplicity correction is applied and none is needed: NOTHING HERE "
        "IS A TEST.")
    t["gates"] = GATES
    return t[t1_declared_columns(cov)]


# ═══════════════════════════════════════════════════════════ 4 · TABLE 2
def check_join(journal: pd.DataFrame, stamped: pd.DataFrame) -> tuple[bool, list[str]]:
    """F-RP-JOIN's check.  FAILS IF a journal campaign lacks exactly one entry
    stamp and exactly one exit stamp, or an entry/exit stamp joins no
    campaign, or an exit stamp is not on its campaign's journal exit_ms."""
    ok, lines = True, []
    jk = journal[["asset", "entry_ms"]]
    dup = int(jk.duplicated().sum())
    g = dup == 0
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] journal key (asset, entry_ms) unique: "
                 f"{len(jk)} rows, {dup} duplicate(s)")
    ent = stamped[stamped["instant_kind"] == "entry"]
    ext = stamped[stamped["instant_kind"] == "exit"]
    ec = ent.groupby(["asset", "instant_ms"]).size()
    per = [int(ec.get((a, int(m)), 0)) for a, m in zip(jk["asset"], jk["entry_ms"])]
    bad_e = sum(1 for x in per if x != 1)
    g = bad_e == 0
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] every campaign has exactly one entry "
                 f"stamp: {len(per) - bad_e}/{len(per)} "
                 f"(counts seen {sorted(set(per))})")
    jset = set(zip(jk["asset"], jk["entry_ms"].astype(int)))
    stray_e = sum(1 for a, m in zip(ent["asset"], ent["instant_ms"])
                  if (a, int(m)) not in jset)
    g = stray_e == 0
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] every entry stamp joins a campaign: "
                 f"{len(ent) - stray_e}/{len(ent)} ({stray_e} stray)")
    emap = (ent.drop_duplicates(subset=["asset", "instant_ms"], keep=False)
            .set_index(["asset", "instant_ms"])["campaign_id"])
    cids = [emap.get((a, int(m))) for a, m in zip(jk["asset"], jk["entry_ms"])]
    null_c = sum(1 for c in cids if c is None or (isinstance(c, float) and np.isnan(c)))
    dup_c = len(cids) - null_c - len({c for c in cids if isinstance(c, str)})
    g = null_c == 0 and dup_c == 0
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] each campaign's entry stamp names one "
                 f"campaign_id, none shared: {null_c} null, {dup_c} shared")
    xc = ext.groupby("campaign_id").size()
    perx = [int(xc.get(c, 0)) if isinstance(c, str) else 0 for c in cids]
    bad_x = sum(1 for x in perx if x != 1)
    g = bad_x == 0
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] every campaign has exactly one exit "
                 f"stamp (same campaign_id): {len(perx) - bad_x}/{len(perx)} "
                 f"(counts seen {sorted(set(perx))})")
    cset = {c for c in cids if isinstance(c, str)}
    stray_x = int((~ext["campaign_id"].isin(cset)).sum())
    g = stray_x == 0
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] every exit stamp joins a campaign: "
                 f"{len(ext) - stray_x}/{len(ext)} ({stray_x} stray)")
    xone = ext.drop_duplicates(subset=["campaign_id"], keep=False) \
        .set_index("campaign_id")
    off = 0
    for c, a, xm in zip(cids, journal["asset"], journal["exit_ms"]):
        if not isinstance(c, str) or c not in xone.index:
            continue
        r = xone.loc[c]
        off += int(r["asset"] != a or int(r["instant_ms"]) != int(xm))
    g = off == 0
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] each exit stamp sits on its "
                 f"campaign's journal (asset, exit_ms): {off} off")
    return ok, lines


def join_book(journal: pd.DataFrame, stamped: pd.DataFrame) -> pd.DataFrame:
    """One row per journal campaign, in journal order, with its entry and exit
    stamps.  Call only after check_join is GREEN (validate re-asserts 1:1)."""
    cols = ["campaign_id", "instant_ms", "instant_close_ms", "rf4h_macro_state",
            "rf4h_in_range", "rf4h_bar_close_ms", "rf4h_bar_lag"]
    ent = stamped[stamped["instant_kind"] == "entry"][["asset"] + cols]
    ent = ent.rename(columns={c: "entry_" + c for c in cols if c != "campaign_id"})
    ext = stamped[stamped["instant_kind"] == "exit"][cols]
    ext = ext.rename(columns={c: "exit_" + c for c in cols if c != "campaign_id"})
    j = journal.merge(ent, left_on=["asset", "entry_ms"],
                      right_on=["asset", "entry_instant_ms"], how="left",
                      validate="1:1")
    j = j.merge(ext, on="campaign_id", how="left", validate="1:1")
    for end in ("entry", "exit"):
        s = j[f"{end}_rf4h_macro_state"]
        bad = sorted(set(s.dropna()) - set(MACRO_STATES))
        if int(s.isna().sum()) or bad:
            raise SystemExit(f"HALT: {end} macro state outside the vocabulary "
                             f"{MACRO_STATES}: {bad} / nulls {int(s.isna().sum())}")
        ir = j[f"{end}_rf4h_in_range"]
        if int(ir.isna().sum()) or not set(ir.map(type)) <= {bool, np.bool_}:
            raise SystemExit(f"HALT: {end} rf4h_in_range is not a clean bool")
        j[f"{end}_in_range_s"] = ir.map(lambda v: "True" if bool(v) else "False")
    return j


def _agg(g: pd.DataFrame) -> dict:
    net = g["net_r"].astype(float)
    n = int(len(g))
    return {
        "n": n,
        "n_assets": int(g["asset"].nunique()),
        "net_r_sum": r6(float(net.sum())) if n else None,
        "expectancy_r": r6(float(net.mean())) if n else None,
        "win_rate_pct": r6(100.0 * float((net > 0).mean())) if n else None,
        "provisional": bool(n < PROVISIONAL_MIN_N),
        "provisional_note": (f"n below the lineage's PROVISIONAL_MIN_N = "
                             f"{PROVISIONAL_MIN_N}" if n < PROVISIONAL_MIN_N
                             else ""),
    }


def build_table2(j: pd.DataFrame, journal: pd.DataFrame, manifest: dict) -> pd.DataFrame:
    """The declared grid WHOLE (zeros filed), then the two marginals and ALL.
    Rows are built in a fixed loop order — never sorted by an outcome."""
    rows = []
    es, ei = j["entry_rf4h_macro_state"], j["entry_in_range_s"]
    xs, xi = j["exit_rf4h_macro_state"], j["exit_in_range_s"]
    for a in MACRO_STATES:
        for ai in IN_RANGE_VOCAB:
            for b in MACRO_STATES:
                for bi in IN_RANGE_VOCAB:
                    g = j[(es == a) & (ei == ai) & (xs == b) & (xi == bi)]
                    rows.append({"cut": "CELL", "entry_rf4h_macro_state": a,
                                 "entry_rf4h_in_range": ai,
                                 "exit_rf4h_macro_state": b,
                                 "exit_rf4h_in_range": bi, **_agg(g)})
    for a in MACRO_STATES:
        rows.append({"cut": "ENTRY_STATE_MARGINAL", "entry_rf4h_macro_state": a,
                     "entry_rf4h_in_range": ALL, "exit_rf4h_macro_state": ALL,
                     "exit_rf4h_in_range": ALL, **_agg(j[es == a])})
    for b in MACRO_STATES:
        rows.append({"cut": "EXIT_STATE_MARGINAL", "entry_rf4h_macro_state": ALL,
                     "entry_rf4h_in_range": ALL, "exit_rf4h_macro_state": b,
                     "exit_rf4h_in_range": ALL, **_agg(j[xs == b])})
    rows.append({"cut": "ALL", "entry_rf4h_macro_state": ALL,
                 "entry_rf4h_in_range": ALL, "exit_rf4h_macro_state": ALL,
                 "exit_rf4h_in_range": ALL, **_agg(j)})
    t = pd.DataFrame(rows)
    n = len(t)
    n_cell = int((t["cut"] == "CELL").sum())
    t.insert(0, "table", T2_LABEL)
    t["rf_lens"] = str(manifest["lens_of_record"])
    t["rf_scale_mult"] = float(manifest["scale_mult"])
    t["book"] = (f"card v6 · V6_ROLES · {journal['as_of_panel'].iloc[0]} — "
                 f"panel/control_journal.parquet, {len(journal)} campaigns on "
                 f"{', '.join(sorted(journal['asset'].unique()))}")
    t["tier"] = TIER_T2
    t["selection_not_a_result"] = SELECTION
    t["m_selections_this_table"] = n
    t["m_note"] = (
        f"m = {n} selections in this table: {n_cell} declared cells "
        f"({len(MACRO_STATES)} states x {len(IN_RANGE_VOCAB)} in_range values at "
        f"entry x the same at exit, zeros filed) + {len(MACRO_STATES)} "
        f"entry-state + {len(MACRO_STATES)} exit-state marginals + 1 ALL. NO "
        "multiplicity correction is applied and none is needed: NOTHING HERE "
        "IS A TEST.")
    t["in_sample"] = IN_SAMPLE_T2
    t["gates"] = GATES
    for c in [c for c in journal.columns if c.startswith("as_of_")] + ["warranty"]:
        vals = journal[c].unique()
        if len(vals) != 1:
            raise SystemExit(f"HALT: journal {c} is not single-valued: {vals}")
        t[c] = vals[0]
    if int(t.duplicated(subset=T2_KEY).sum()):
        raise SystemExit(f"HALT: Table 2 is not unique on {T2_KEY}")
    return t


# ═══════════════════════════════════════════════════════════ 5 · THE CHECKS
def _same(a, b) -> bool:
    fa = a is None or (isinstance(a, float) and np.isnan(a))
    fb = b is None or (isinstance(b, float) and np.isnan(b))
    if fa or fb:
        return fa and fb
    return a == b


def check_anchor(t2: pd.DataFrame, anchor: pd.DataFrame) -> tuple[bool, list[str]]:
    """F-RP-ANCHOR's check.  FAILS IF Table 2's entry-state marginal (and its
    ALL row) differs by ANY amount from stamps/control_entry_by_state.parquet
    on n, net_r_sum, expectancy_r or win_rate_pct, for any state incl. __ALL__,
    or if the two tables do not name the same states."""
    ok, lines = True, []
    a_states = [s for s in anchor["macro_state_at_entry"] if s != ALL]
    g = sorted(a_states) == sorted(MACRO_STATES)
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] state vocabulary: anchor "
                 f"{sorted(a_states)} vs stamps MACRO_STATES {sorted(MACRO_STATES)}")
    marg = t2[t2["cut"] == "ENTRY_STATE_MARGINAL"]
    extra = sorted(set(marg["entry_rf4h_macro_state"]) - set(a_states))
    g = not extra
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] no Table-2 entry state outside the "
                 f"anchor: {extra or 'none'}")
    for _, ar in anchor.iterrows():
        k = ar["macro_state_at_entry"]
        mine = (t2[t2["cut"] == "ALL"] if k == ALL
                else marg[marg["entry_rf4h_macro_state"] == k])
        if len(mine) != 1:
            ok = False
            lines.append(f"[BAD] {k:<9} Table 2 has {len(mine)} row(s) for it")
            continue
        m = mine.iloc[0]
        parts, g = [], True
        for c in ("n", "net_r_sum", "expectancy_r", "win_rate_pct"):
            av = None if pd.isna(ar[c]) else (int(ar[c]) if c == "n" else float(ar[c]))
            mv = None if pd.isna(m[c]) else (int(m[c]) if c == "n" else float(m[c]))
            same = _same(av, mv)
            g &= same
            parts.append(f"{c} {mv!r}{'==' if same else '!='}{av!r}")
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] {k:<9} " + " · ".join(parts))
    return ok, lines


def check_verbatim(t1: pd.DataFrame, cov: pd.DataFrame) -> tuple[bool, list[str]]:
    """F-RP-VERBATIM's check.  FAILS IF any Table 1 value in a verbatim column
    differs from coverage.parquet (exact: dtype and value, NaN == NaN), or the
    row sets differ."""
    ok, lines = True, []
    cols = t1_verbatim_columns(cov)
    miss = [c for c in cols if c not in t1.columns]
    g = not miss
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] verbatim columns present: "
                 f"{len(cols) - len(miss)}/{len(cols)} (missing {miss or 'none'})")
    if miss:
        return False, lines
    a = t1.sort_values(T1_KEY, kind="mergesort").reset_index(drop=True)
    b = cov.sort_values(T1_KEY, kind="mergesort").reset_index(drop=True)
    ka = list(map(tuple, a[T1_KEY].values.tolist()))
    kb = list(map(tuple, b[T1_KEY].values.tolist()))
    g = ka == kb and len(set(ka)) == len(ka)
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] row set: Table 1 {len(a)} rows vs "
                 f"coverage {len(b)} rows, keys identical and unique: {g}")
    if not g:
        return False, lines
    bad = []
    for c in cols:
        same = bool(a[c].equals(b[c])) and a[c].dtype == b[c].dtype
        if not same:
            if pd.api.types.is_numeric_dtype(a[c]) and pd.api.types.is_numeric_dtype(b[c]):
                d = (a[c].astype(float) - b[c].astype(float)).abs()
                nd = int((d > 0).sum())
                bad.append(f"{c} ({nd} cell(s), worst |diff| {float(d.max()):.6g})")
            else:
                bad.append(f"{c} ({int((a[c].astype(str) != b[c].astype(str)).sum())} cell(s))")
    g = not bad
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] {len(cols)} verbatim column(s) x "
                 f"{len(a)} rows equal to coverage.parquet exactly; differing: "
                 f"{bad or 'none'}")
    return ok, lines


def check_exit_asof(stamped: pd.DataFrame) -> tuple[bool, list[str]]:
    """F-RP-EXIT-ASOF's check.  FAILS IF any exit stamp's rf4h_bar_close_ms is
    null or later than its instant_close_ms (the stamp read a bar that had not
    closed when the exit instant did)."""
    ok, lines = True, []
    x = stamped[stamped["instant_kind"] == "exit"]
    nul = int(x["rf4h_bar_close_ms"].isna().sum())
    late = int((x["rf4h_bar_close_ms"] > x["instant_close_ms"]).sum())
    g = nul == 0 and late == 0 and len(x) > 0
    ok &= g
    lag = (x["instant_close_ms"] - x["rf4h_bar_close_ms"])
    lines.append(f"[{'OK ' if g else 'BAD'}] exit stamps {len(x)}: bar closed "
                 f"AFTER the instant on {late}, null on {nul}; lag ms "
                 f"min {int(lag.min()) if len(x) else None} "
                 f"max {int(lag.max()) if len(x) else None}")
    e = stamped[stamped["instant_kind"] == "entry"]
    e_late = int((e["rf4h_bar_close_ms"] > e["instant_close_ms"]).sum())
    lines.append(f"[info] entry stamps {len(e)}: bar closed AFTER the instant on "
                 f"{e_late} (printed beside; the leg is the exit law)")
    return ok, lines


def forbidden_columns(df: pd.DataFrame) -> list[str]:
    out = []
    for c in df.columns:
        lc = str(c).lower()
        if (lc in FORBIDDEN_EXACT or lc.startswith(FORBIDDEN_PREFIX)
                or any(s in lc for s in FORBIDDEN_SUBSTR)):
            out.append(str(c))
    return out


def check_collar(tables: dict) -> tuple[bool, list[str]]:
    """F-RP-COLLAR's check.  FAILS IF, on any table, a Tier-E collar column is
    missing or null on a row, gates is not 'nothing', tier does not say
    TIER-E, selection_not_a_result does not say 'SELECTION, not a result',
    m_selections_this_table is not the table's row count — or a verdict / ci /
    p column exists."""
    ok, lines = True, []
    for name, df in tables.items():
        miss = [c for c in COLLAR_COLS if c not in df.columns]
        nul = [c for c in COLLAR_COLS if c in df.columns and int(df[c].isna().sum())]
        g = not miss and not nul
        if g:
            g &= bool((df["gates"] == GATES).all())
            g &= bool(df["tier"].astype(str).str.contains("TIER-E").all())
            g &= bool(df["selection_not_a_result"].astype(str)
                      .str.contains("SELECTION, not a result").all())
            g &= bool((df["m_selections_this_table"] == len(df)).all())
        forb = forbidden_columns(df)
        g &= not forb
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] {name}: collar {list(COLLAR_COLS)} "
                     f"missing {miss or 'none'}, null {nul or 'none'}; "
                     f"verdict/ci/p columns {forb or 'none'}")
    return ok, lines


def check_quote(md_text: str, t1: pd.DataFrame, declared: list[str],
                quote: str) -> tuple[bool, list[str]]:
    """F-RP-QUOTE's check.  FAILS IF the ARGUS note's item 2 does not appear
    WHOLE in REGIME_PRIOR.md, or any Table 1 row carries anything but the whole
    line, or Table 1's column set is not the declared one (so no threshold or
    flag column parsed out of the quote can ride in)."""
    ok, lines = True, []
    g = quote in md_text
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] item 2 whole in {MD_NAME} "
                 f"({len(quote)} chars, sha256 {sha256_bytes(quote.encode())[:16]}…)")
    col = t1["argus_note_item_2"] if "argus_note_item_2" in t1.columns else None
    g = col is not None and bool((col == quote).all())
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] item 2 whole on every Table 1 row "
                 f"({0 if col is None else int((col == quote).sum())}/{len(t1)})")
    got = list(t1.columns)
    g = got == declared
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] Table 1 columns == declared "
                 f"({len(got)} vs {len(declared)}; extra "
                 f"{sorted(set(got) - set(declared)) or 'none'}, missing "
                 f"{sorted(set(declared) - set(got)) or 'none'})")
    return ok, lines


# ═══════════════════════════════════════════════════════════ 6 · THE MD
def _v(x) -> str:
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return "—"
    if isinstance(x, (bool, np.bool_)):
        return "yes" if bool(x) else ""
    if isinstance(x, (int, np.integer)):
        return str(int(x))
    if isinstance(x, (float, np.floating)):
        return repr(float(x))
    return str(x)


def _table(df: pd.DataFrame, cols: list[str], heads: list[str] | None = None) -> list[str]:
    heads = heads or cols
    out = ["| " + " | ".join(heads) + " |",
           "|" + "|".join("---" for _ in cols) + "|"]
    for _, r in df.iterrows():
        out.append("| " + " | ".join(_v(r[c]) for c in cols) + " |")
    return out


def render_md(ctx: dict) -> str:
    t1, t2, j = ctx["t1"], ctx["t2"], ctx["joined"]
    cov, anchor = ctx["cov"], ctx["anchor"]
    L: list[str] = []
    A = L.append
    A("# REGIME-PRIOR — Tier-E tables (TIER-C10 · CLOSE)")
    A("")
    A("> **TIER-E · REPORT-ONLY · a SELECTION, not a result · gates: nothing · "
      "in-sample.** No row below is a test. Neither table has a verdict, CI or "
      "p column; no registration and no verdict was read to build them; no cell "
      "may be promoted to a lane. m is logged on every row so a reader who later "
      "turns a cell into a claim can see how many ways the tape was cut first.")
    A("")
    A("## Why this exists")
    A("")
    ln, text = ctx["contract_line"]
    A(f"The contract of record names the item and its form "
      f"(`{CONTRACT_REL}` line {ln}; sha256 `{ctx['contract_sha']}`, equal to "
      f"PROGRESS.json `contract_of_record`):")
    A("")
    A("```")
    A(text)
    A("```")
    A("")
    A("## The prior, quoted whole")
    A("")
    A(f"`{ARGUS_REL}` (sha256 `{ctx['argus_sha']}`; git blob `{ctx['argus_blob']}`, "
      f"equal to the committed blob at HEAD), item 2, verbatim:")
    A("")
    A("> " + ctx["quote"])
    A("")
    A("It is quoted, never parsed: nothing in this build reads a number out of "
      "it, no row of either table is compared with it, and neither table carries "
      "a column derived from it (F-RP-QUOTE holds Table 1's column set to the "
      "declared one).")
    A("")
    A("## Inputs")
    A("")
    A("Read-only. Each sha256 was held against its PROGRESS.json stage record "
      "before the file was read.")
    A("")
    A("| input | PROGRESS stage | sha256 | rows |")
    A("|---|---|---|---|")
    for key, rel, stage in INPUTS:
        obj = ctx["inputs"][key]
        rows = len(obj) if isinstance(obj, pd.DataFrame) else "(json)"
        A(f"| `{rel}` | {stage} | `{ctx['input_shas'][key]}` | {rows} |")
    A("")
    A("No bar is read by this build. Both tables are made from filed parquet; "
      "none of " + ", ".join(f"`{m}`" for m in NO_BAR_MODULES) + " is imported "
      "(the build checks `sys.modules` before it writes) and no kline file is "
      "opened.")
    A("")
    # ─── Table 1
    A("## Table 1 — time-in-range per asset × lens × scale_kind")
    A("")
    A(f"`close/{T1_NAME}` (sha256 `{ctx['out_shas'][T1_NAME]}`): {len(t1)} rows = "
      f"{t1['asset'].nunique()} assets × {t1['lens'].nunique()} lenses × "
      f"{t1['scale_kind'].nunique()} scale kinds, copied verbatim from "
      "`census/coverage.parquet` (F-RP-VERBATIM holds every copied value exact). "
      "No new pooling: nothing is averaged, summed or ranked across assets, "
      "lenses or scale kinds.")
    A("")
    A("Column laws:")
    A("")
    laws = sorted(set(cov["coverage_law"]))
    A(f"- `coverage_pct`: {'; '.join(laws)} (the census's `coverage_law`, verbatim).")
    A(f"- `bars_in_live_range_pct`: {TIME_IN_RANGE_LAW}")
    A("")
    lens_order = [x for x in ("5m", "4h", "1d") if x in set(t1["lens"])] + \
        sorted(set(t1["lens"]) - {"5m", "4h", "1d"})
    for lens in lens_order:
        for sk in sorted(set(t1["scale_kind"])):
            b = t1[(t1["lens"] == lens) & (t1["scale_kind"] == sk)]
            if not len(b):
                continue
            A(f"### {lens} · {sk}")
            A("")
            L.extend(_table(b, ["asset", "scale_mult", "n_bars", "coverage_pct",
                                "bars_in_live_range_pct", "as_of_panel_start",
                                "as_of_last_closed_bar"]))
            A("")
    A("`in_sample`, verbatim from the census, by scale kind:")
    A("")
    for sk in sorted(set(t1["scale_kind"])):
        v = sorted(set(t1.loc[t1["scale_kind"] == sk, "in_sample"]))
        A(f"- {sk}: " + " / ".join(v))
    A("")
    # ─── Table 2
    A("## Table 2 — the v6 CLASSIC5 book by rf4h macro state at entry × at exit")
    A("")
    man = ctx["inputs"]["stamps_manifest"]
    A(f"`close/{T2_NAME}` (sha256 `{ctx['out_shas'][T2_NAME]}`). Book: "
      f"{t2['book'].iloc[0]}. States: the Stage-A stamps "
      f"(`stamps/control_v6_stamped.parquet`) on lens `{man['lens_of_record']}` "
      f"at SCALE_MULT {man['scale_mult']!r} (`stamps/build_manifest.json`). The "
      "entry stamp joins on (asset, instant_ms == entry_ms, instant_kind = "
      "'entry'); the exit stamp joins on the same campaign_id with instant_kind "
      "= 'exit' (F-RP-JOIN). net_r is the journal's.")
    A("")
    cells = t2[t2["cut"] == "CELL"]
    nz = cells[cells["n"] > 0]
    A(f"The declared grid is whole: {len(cells)} cells ({len(MACRO_STATES)} states "
      f"× {len(IN_RANGE_VOCAB)} in_range values at entry × the same at exit) are "
      f"filed, zeros included. {len(nz)} are non-empty and printed here; the "
      f"other {len(cells) - len(nz)} are n = 0. Cells with n < "
      f"{PROVISIONAL_MIN_N} are flagged provisional (the lineage's "
      "PROVISIONAL_MIN_N, read from `scripts/tierc10_census.py`).")
    A("")
    show = ["entry_rf4h_macro_state", "entry_rf4h_in_range", "exit_rf4h_macro_state",
            "exit_rf4h_in_range", "n", "n_assets", "net_r_sum", "expectancy_r",
            "win_rate_pct", "provisional"]
    heads = ["entry state", "entry in_range", "exit state", "exit in_range", "n",
             "n_assets", "net_r_sum", "expectancy_r", "win_rate_pct", "provisional"]
    L.extend(_table(nz, show, heads))
    A("")
    A("Entry-state marginal — equal on n, net_r_sum, expectancy_r and "
      "win_rate_pct to `stamps/control_entry_by_state.parquet` (F-RP-ANCHOR):")
    A("")
    L.extend(_table(t2[t2["cut"].isin(["ENTRY_STATE_MARGINAL", "ALL"])],
                    ["cut", "entry_rf4h_macro_state", "n", "n_assets", "net_r_sum",
                     "expectancy_r", "win_rate_pct", "provisional"],
                    ["cut", "entry state", "n", "n_assets", "net_r_sum",
                     "expectancy_r", "win_rate_pct", "provisional"]))
    A("")
    A("Exit-state marginal:")
    A("")
    L.extend(_table(t2[t2["cut"].isin(["EXIT_STATE_MARGINAL", "ALL"])],
                    ["cut", "exit_rf4h_macro_state", "n", "n_assets", "net_r_sum",
                     "expectancy_r", "win_rate_pct", "provisional"],
                    ["cut", "exit state", "n", "n_assets", "net_r_sum",
                     "expectancy_r", "win_rate_pct", "provisional"]))
    A("")
    A("Disclosures (counted from the joined rows, not assumed):")
    A("")
    for end in ("entry", "exit"):
        agree = int(((j[f"{end}_rf4h_macro_state"] == "NEUTRAL")
                     == j[f"{end}_rf4h_in_range"].astype(bool)).sum())
        A(f"- {end}: rf4h_in_range == (macro_state == 'NEUTRAL') on {agree}/{len(j)} "
          "campaigns — the stamps' four-valued collapse [LEAN S-a] makes NEUTRAL "
          "mean a confirmed range is alive, so the in_range columns repeat the "
          "state here; they are carried as specified.")
    lag = j["exit_rf4h_bar_lag"].value_counts().sort_index()
    A(f"- exit stamp bar lag (4h bars): "
      + ", ".join(f"{int(k)}: {int(v)}" for k, v in lag.items())
      + f"; exit instant_ms == journal exit_ms on "
      f"{int((j['exit_instant_ms'] == j['exit_ms']).sum())}/{len(j)}.")
    diag = int((j["entry_rf4h_macro_state"] == j["exit_rf4h_macro_state"]).sum())
    A(f"- campaigns whose exit state equals their entry state: {diag}/{len(j)} "
      "(a count of the diagonal cells above, not a statistic).")
    A("")
    A("## The collar, as filed on every row of both tables")
    A("")
    A(f"- `tier`: Table 1 carries the census's own, verbatim "
      f"({'; '.join(sorted(set(t1['tier'])))}); Table 2: {TIER_T2}")
    A(f"- `selection_not_a_result`: {SELECTION}")
    A(f"- `m_selections_this_table`: Table 1 {len(t1)}, Table 2 {len(t2)} "
      "(every row is one cut)")
    A(f"- `in_sample`: Table 1 the census's, verbatim (above); Table 2: "
      f"{IN_SAMPLE_T2}")
    A(f"- `gates`: {GATES}")
    A("")
    A("## Fixtures")
    A("")
    A(f"`scripts/tierc10_close_regime_prior_fixtures.py` → `close/{FIX_NAME}`. "
      "Legs: F-RP-SHA · F-RP-JOIN · F-RP-ANCHOR · F-RP-VERBATIM · F-RP-EXIT-ASOF · "
      "F-RP-COLLAR · F-RP-QUOTE · F-DET. Each states FAILS IF and carries a "
      "sabotage that must go RED. The build itself runs the same checks as "
      "HALT gates before it writes a byte.")
    A("")
    return "\n".join(L)


# ═══════════════════════════════════════════════════════════ 7 · THE BUILD
def _write_bytes(p: Path, b: bytes) -> None:
    tmp = p.with_name(p.name + ".tmp")
    tmp.write_bytes(b)
    os.replace(tmp, p)


def _parquet_bytes(df: pd.DataFrame) -> bytes:
    import io
    buf = io.BytesIO()
    d = df.copy()
    d.attrs = {}
    d.columns = [str(c) for c in d.columns]
    d.to_parquet(buf, index=False, engine="pyarrow")
    return buf.getvalue()


def build(out_dir: Path) -> dict:
    log("=" * 78)
    log("TIER-C10 · CLOSE · REGIME-PRIOR — Tier-E tables only (report-only)")
    log("=" * 78)
    log(f"  state vocabulary (ast-read from {STAMPS_SRC_REL}): {MACRO_STATES}")
    log(f"  PROVISIONAL_MIN_N (ast-read from {CENSUS_SRC_REL}): {PROVISIONAL_MIN_N}")
    log("  inputs, each held against its PROGRESS.json record:")
    inp = load_inputs()
    cov, st, anchor = inp["coverage"], inp["stamped"], inp["anchor"]
    journal, man = inp["journal"], inp["stamps_manifest"]
    quote = argus_item_2()
    cline = contract_line()

    # preconditions: one corridor, one lens
    for c in [c for c in journal.columns if c.startswith("as_of_")]:
        jv, sv = set(journal[c].unique()), set(st[c].unique()) if c in st.columns else None
        if sv is None or jv != sv or len(jv) != 1:
            raise SystemExit(f"HALT: journal and stamps disagree on {c}: {jv} vs {sv}")
    if set(st["lane_lens"].unique()) != {man["lens_of_record"]}:
        raise SystemExit("HALT: stamps' lane_lens is not the manifest's lens_of_record")

    gates = []
    ok, lines = check_join(journal, st)
    gates.append(("F-RP-JOIN", ok, lines))
    if not ok:
        for s in lines:
            log(f"    {s}")
        raise SystemExit("HALT (F-RP-JOIN): the book and the stamps do not join")
    j = join_book(journal, st)
    t1 = build_table1(cov, quote)
    t2 = build_table2(j, journal, man)
    if int(t2.loc[t2["cut"] == "CELL", "n"].sum()) != len(journal) or \
            int(t2.loc[t2["cut"] == "ALL", "n"].iloc[0]) != len(journal):
        raise SystemExit("HALT: Table 2's cells do not partition the book")
    gates.append(("F-RP-ANCHOR", *check_anchor(t2, anchor)))
    gates.append(("F-RP-VERBATIM", *check_verbatim(t1, cov)))
    gates.append(("F-RP-EXIT-ASOF", *check_exit_asof(st)))
    gates.append(("F-RP-COLLAR", *check_collar({"Table 1": t1, "Table 2": t2})))

    b1, b2 = _parquet_bytes(t1), _parquet_bytes(t2)
    ctx = {"t1": t1, "t2": t2, "joined": j, "cov": cov, "anchor": anchor,
           "inputs": inp, "quote": quote, "contract_line": cline,
           "contract_sha": sha256_path(ROOT / CONTRACT_REL),
           "argus_sha": sha256_path(ROOT / ARGUS_REL),
           "argus_blob": git_blob_ok(ARGUS_REL)[2],
           "input_shas": {k: sha256_path(ROOT / rel) for k, rel, _ in INPUTS},
           "out_shas": {T1_NAME: sha256_bytes(b1), T2_NAME: sha256_bytes(b2)}}
    md = render_md(ctx)
    gates.append(("F-RP-QUOTE", *check_quote(md, t1, t1_declared_columns(cov), quote)))
    for name, ok, lines in gates:
        log(f"  gate {name}: {'GREEN' if ok else 'RED'}")
        for s in lines:
            log(f"    {s}")
    red = [n for n, ok, _ in gates if not ok]
    if red:
        raise SystemExit(f"HALT: gate(s) RED before any write: {red}")
    # the md says no bar was read: hold that to the interpreter, not to a promise
    bar_mods = sorted(m for m in NO_BAR_MODULES if m in sys.modules)
    if bar_mods:
        raise SystemExit(f"HALT: a bar-reading module was imported: {bar_mods}")
    log(f"  no bar-reading module in sys.modules: {list(NO_BAR_MODULES)}")

    out_dir.mkdir(parents=True, exist_ok=True)
    mb = md.encode()
    _write_bytes(out_dir / T1_NAME, b1)
    _write_bytes(out_dir / T2_NAME, b2)
    _write_bytes(out_dir / MD_NAME, mb)
    shas = {T1_NAME: sha256_bytes(b1), T2_NAME: sha256_bytes(b2),
            MD_NAME: sha256_bytes(mb)}
    log("  wrote:")
    for k in OUTPUT_NAMES:
        log(f"    {k:<38} sha256 {shas[k]}")
    log(f"  Table 1 rows {len(t1)} · Table 2 rows {len(t2)} "
        f"(cells {int((t2['cut'] == 'CELL').sum())}, non-empty "
        f"{int(((t2['cut'] == 'CELL') & (t2['n'] > 0)).sum())})")
    return {"shas": shas, "t1": t1, "t2": t2}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default=None,
                    help="write the three outputs here instead of "
                         "research_outputs/tierc10/close/ (F-DET's subprocess "
                         "runs); refused anywhere else inside the repo")
    a = ap.parse_args(argv)
    out = OUT if a.out is None else Path(a.out).resolve()
    if out != OUT.resolve():
        try:
            out.relative_to(ROOT)
            raise SystemExit(f"HALT: --out {out} is inside the repo but is not "
                             f"{OUT} — this build writes nowhere else in the tree")
        except ValueError:
            pass
    build(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
