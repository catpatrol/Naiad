#!/usr/bin/env python
"""TIER-C10 · CLOSE · THE 5-ASSET v6 CONTROL'S HAIRCUT TWIN — AN ADDED COLUMN (BOOK LEVEL).

REPORT-ONLY · Tier-E.  Nothing here is scored.  No CI, no p, no verdict is
computed, filed or printed, and no registration is read for its verdict.

THE CLAUSE (contract of record exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md,
lines 53-55 — QUOTED AT RUN TIME from the file, whose sha is held against
PROGRESS.json's contract_of_record before anything else happens):
    "The 5-asset control's TC-series accounting stays untouched; its twin is an
     ADDED column."

WHAT IT DOES
  For each campaign of the FILED v6 control (panel/control_journal.parquet):
      twin      = tierc10_data.haircut_twin_net_r(asset, gross_r, entry_px,
                                                  exit_px, r_dist)['net_r_twin']
      companion = twin - funding_r   — labelled NOT the filed twin: the filed
                  twin charges fee + charter slippage and NO funding, while the
                  TC-series net_r charges funding.
  The TC-series net_r is read and NEVER written.  Rows: every CLASSIC5 asset
  and CLASSIC5 ALL, for each era of tierc10_panel.era_window ('full',
  'tuning', 'holdout'; a campaign is in an era iff its entry_ms is).  Columns:
  n · tc_expectancy_r (mean of the journal's net_r, verbatim) ·
  twin_expectancy_r · companion_expectancy_r · sign_disagrees (twin vs TC) ·
  companion_sign_disagrees · tier (tierc10_data.tier_of, as filed) · charter
  bps/side (READ from data/fee_schedule.json haircut_twin_* keys) · the
  untouched TC-series toll (fee_schedule.json round_trip_bps_used) beside it.

INPUTS (every sha held against its PROGRESS.json stage record; HALT on drift)
  panel/control_journal.parquet   PANEL/gate   the control's campaigns
  panel/control_headline.parquet  PANEL/gate   F-VT-TC's referee
  data/fee_schedule.json          D-CORE       the charter rate per asset
  data/STAGE_D_MANIFEST.json      D-CORE       stem -> contract asset (read by
                                               the scorer the same way)
  scores/P-TRG-2.rows.json        B-CORE       F-VT-REUSE's referee.  READ-ONLY;
                                  fields read: arm, score_row.arm_era,
                                  score_row.arm_base, beside.haircut_twin.* —
                                  no verdict / CI / p / LOAO field is read.
  Bars are NOT read by this file (the book is the filed journal).

OUTPUTS (research_outputs/tierc10/close/, nothing else is written)
  V6_CONTROL_HAIRCUT_TWIN.parquet · V6_CONTROL_HAIRCUT_TWIN.md ·
  FIXTURES_CLOSE_v6_control_twin.txt (this run's transcript; no wall clock, no
  temp path in it, so two whole runs are byte-identical).

THE LEGS — each states FAILS IF, runs GREEN on the real inputs, then re-runs
under each of its SABOTAGES, where it must go RED.  A sabotage that leaves its
leg GREEN is VOID and fails the leg.
  F-VT-TC         tc_expectancy_r is the TC-series number, verbatim.
  F-VT-REUSE      the ALL twin is the twin already filed beside P-TRG-2's row
                  (its v6 base), at a tolerance DERIVED from the journal's
                  measured filing precision — see [FINDING F-VT-REUSE-TOL].
  F-VT-UNTOUCHED  net_r is never overwritten; fee_schedule.json's bytes never
                  change.
  F-VT-LABEL      every row REPORT-ONLY; no ci / p / verdict column.
  F-DET           two in-process builds from fresh reads are byte-identical to
                  each other and to the filed outputs.

[FINDING F-VT-REUSE-TOL] The build spec asked |ALL twin - P-TRG-2 base twin|
<= 1e-12.  That is unattainable from the filed journal and is MEASURED, not
assumed: tierc5.journal_frame files every price/R column at 6 dp (r6), while
P-TRG-2's base book rode at full precision in memory.  The leg therefore
asserts a bound DERIVED from the measured precision (half a unit in the last
filed place, propagated through the filed cost law, plus the 1e-12 float floor)
and prints the literal 1e-12 comparison beside it, un-asserted.  Likewise the
headline is filed at 4 dp (r4), so F-VT-TC's headline clause compares at 4 dp
and the 1e-9 sabotage is caught by its EXACT clause (the sha-verified journal),
which the transcript names.

Run (the RUN/HALT preamble — same as every TIER-C10 script):
  export NAIAD_CACHE_DIR=/Users/luis/.cache/naiad/snapshots/tc10_20260921 \\
         PYTHONDONTWRITEBYTECODE=1
  ~/venvs/naiad/bin/python scripts/tierc10_close_v6_control_twin.py
HALTS IF: PYTHONDONTWRITEBYTECODE != 1; NAIAD_CACHE_DIR is unset / the live
cache / not the TC10 snapshot (tierc10_data.assert_substrate, at import); any
input's sha differs from its PROGRESS.json record; the contract clause is not
on lines 53-55; the fee schedule's tier/rate disagrees with tierc10_data's;
an input column is missing or non-finite; a journal stem is not CLASSIC5.
Exit: 0 every leg GREEN · 1 a leg RED or a HALT.
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import json
import math
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

# ═══════════════════════════════════════════ THE RUN/HALT PREAMBLE
if os.environ.get("PYTHONDONTWRITEBYTECODE") != "1":
    raise SystemExit("HALT: PYTHONDONTWRITEBYTECODE is not 1 — export it with "
                     "NAIAD_CACHE_DIR before python starts")

import tierc10_data as D          # noqa: E402  — import runs assert_substrate()

import numpy as np                # noqa: E402
import pandas as pd               # noqa: E402

import tierc10_panel as TP        # noqa: E402  — era_window / in_era / r4 / CLASSIC5

OUT = ROOT / "research_outputs" / "tierc10"
CLOSE = OUT / "close"
PROGRESS = OUT / "PROGRESS.json"
CONTRACT = ROOT / "exchange" / "queue" / "2026-09-22_TC10_RESUME_APOLLO.md"
CONTRACT_LINES = (53, 55)                   # the clause, 1-indexed inclusive
CONTRACT_NEEDLE = "The 5-asset control's TC-series accounting stays untouched"

JOURNAL = OUT / "panel" / "control_journal.parquet"
HEADLINE = OUT / "panel" / "control_headline.parquet"
FEES = OUT / "data" / "fee_schedule.json"
MANIFEST = OUT / "data" / "STAGE_D_MANIFEST.json"
TRG2 = OUT / "scores" / "P-TRG-2.rows.json"
INPUT_STAGE = {JOURNAL: "PANEL/gate", HEADLINE: "PANEL/gate", FEES: "D-CORE",
               MANIFEST: "D-CORE", TRG2: "B-CORE"}

OUT_PARQUET = CLOSE / "V6_CONTROL_HAIRCUT_TWIN.parquet"
OUT_MD = CLOSE / "V6_CONTROL_HAIRCUT_TWIN.md"
OUT_TRANSCRIPT = CLOSE / "FIXTURES_CLOSE_v6_control_twin.txt"

TABLE = "V6_CONTROL_HAIRCUT_TWIN"
LABEL = "REPORT-ONLY · Tier-E · v6 control haircut twin (ADDED column)"
TWIN_FUNCTION = "tierc10_data.haircut_twin_net_r (as filed)"
COMPANION_LABEL = "twin - funding_r — NOT the filed twin"
TC_SOURCE = ("panel/control_journal.parquet net_r, mean, verbatim — the "
             "TC-series accounting of record, untouched")
FLOAT_FLOOR = 1e-12            # the auditor's figure, kept as the float floor
NUM_COLS = ("gross_r", "entry_px", "exit_px", "r_dist", "funding_r", "net_r")
WORK_COLS = ("asset", "entry_ms", "exit_ms", "direction", "exit_reason",
             "entry_px", "exit_px", "r_dist", "gross_r", "fee_r", "funding_r",
             "net_r")
FORBIDDEN_COL = re.compile(r"(^|_)(ci|p|verdict|loao|pvalue|p_one_sided)(_|$)")
KEY_ALL = "ALL"


# ═══════════════════════════════════════════ small helpers
def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha256_file(p: Path) -> str:
    return sha256_bytes(p.read_bytes())


def rel(p: Path) -> str:
    return str(Path(p).resolve().relative_to(ROOT))


class Printer:
    def __init__(self):
        self.buf = io.StringIO()

    def __call__(self, s: str = "") -> None:
        self.buf.write(s + "\n")
        print(s, flush=True)

    def text(self) -> str:
        return self.buf.getvalue()


# ═══════════════════════════════════════════ 1 · PREAMBLE: inputs vs PROGRESS
def progress_record(progress: dict, stage: str, path: Path) -> dict:
    for s in progress["stages"]:
        if s["stage"] == stage:
            r = s["artifact_shas"].get(rel(path))
            if r is None:
                raise SystemExit(f"HALT: PROGRESS.json stage {stage!r} records "
                                 f"no artifact {rel(path)}")
            return r
    raise SystemExit(f"HALT: PROGRESS.json has no stage {stage!r}")


def contract_clause(progress: dict) -> dict:
    want = progress["contract_of_record"]
    if want["path"] != rel(CONTRACT):
        raise SystemExit(f"HALT: PROGRESS contract_of_record is {want['path']}, "
                         f"not {rel(CONTRACT)}")
    got = sha256_file(CONTRACT)
    if got != want["sha256"]:
        raise SystemExit(f"HALT: contract sha {got} != PROGRESS record "
                         f"{want['sha256']}")
    lines = CONTRACT.read_text(encoding="utf-8").splitlines()
    lo, hi = CONTRACT_LINES
    joined = " ".join(x.strip() for x in lines[lo - 1:hi])
    at = joined.find(CONTRACT_NEEDLE)
    if at < 0:
        raise SystemExit(f"HALT: the clause is not on contract lines {lo}-{hi}")
    return {"path": rel(CONTRACT), "sha256": got, "lines": f"{lo}-{hi}",
            "clause": joined[at:]}


def verify_inputs(progress: dict) -> list[dict]:
    out = []
    for p, stage in INPUT_STAGE.items():
        rec = progress_record(progress, stage, p)
        if not p.exists():
            raise SystemExit(f"HALT: input {rel(p)} is absent")
        b = p.read_bytes()
        got = sha256_bytes(b)
        if got != rec["sha256"] or len(b) != rec["bytes"]:
            raise SystemExit(f"HALT: {rel(p)} sha {got} / {len(b)} B != "
                             f"PROGRESS {stage} record {rec['sha256']} / "
                             f"{rec['bytes']} B")
        out.append({"path": rel(p), "stage": stage, "sha256": got,
                    "bytes": len(b)})
    return out


# ═══════════════════════════════════════════ 2 · READ (fresh, every call)
def read_inputs() -> dict:
    """Every input read fresh from disk.  Nothing cached between calls, so
    F-DET's two builds are two independent reads."""
    journal = pd.read_parquet(JOURNAL)
    headline = pd.read_parquet(HEADLINE)
    fee_bytes = FEES.read_bytes()
    fees = json.loads(fee_bytes)
    manifest = json.loads(MANIFEST.read_text())
    trg2 = json.loads(TRG2.read_text())
    stem_asset = {v["stem"]: v["asset"] for v in manifest["venues"] if v["stem"]}
    fees_by_stem = {r["stem"]: r for r in fees["assets"]}
    return {"journal": journal, "headline": headline, "fee_bytes": fee_bytes,
            "fees": fees, "fees_by_stem": fees_by_stem,
            "stem_asset": stem_asset, "trg2": trg2,
            "journal_sha": sha256_file(JOURNAL)}


def check_schema(inp: dict) -> None:
    """HALTS IF a column is missing, a number is non-finite, a stem is not
    CLASSIC5, the manifest and fee schedule disagree on a stem's contract
    asset, or the fee schedule's tier / rate disagrees with tierc10_data's."""
    j = inp["journal"]
    miss = [c for c in WORK_COLS + ("as_of_last_closed_4h",) if c not in j.columns]
    if miss:
        raise SystemExit(f"HALT: control_journal lacks {miss}")
    for c in NUM_COLS:
        x = j[c].to_numpy(dtype=float)
        if not np.all(np.isfinite(x)):
            raise SystemExit(f"HALT: control_journal.{c} carries a non-finite value")
    stray = sorted(set(j["asset"]) - set(TP.CLASSIC5))
    if stray:
        raise SystemExit(f"HALT: journal stems outside CLASSIC5: {stray}")
    for s in TP.CLASSIC5:
        a = inp["stem_asset"].get(s)
        f = inp["fees_by_stem"].get(s)
        if a is None or f is None or f["asset"] != a:
            raise SystemExit(f"HALT: stem {s}: manifest asset {a!r} vs fee "
                             f"schedule {None if f is None else f['asset']!r}")
        if f["haircut_twin_tier"] != D.tier_of(a) \
                or float(f["haircut_twin_bps_side"]) != D.charter_bps_side(a):
            raise SystemExit(f"HALT: {s}: fee_schedule tier/rate "
                             f"{f['haircut_twin_tier']}/{f['haircut_twin_bps_side']} "
                             f"!= tierc10_data {D.tier_of(a)}/{D.charter_bps_side(a)}")


# ═══════════════════════════════════════════ 3 · BUILD
def campaign_frame(journal: pd.DataFrame, stem_asset: dict) -> pd.DataFrame:
    """Per campaign: the filed twin and its funding companion, in NEW columns.
    The journal is copied; its net_r is carried and never written."""
    w = journal.loc[:, list(WORK_COLS)].copy(deep=True).reset_index(drop=True)
    tw, comp, cost, tier, bps, ca = [], [], [], [], [], []
    for r in w.itertuples(index=False):
        a = stem_asset.get(str(r.asset))
        if a is None:
            raise SystemExit(f"HALT: the Stage D manifest names no stem {r.asset}")
        h = D.haircut_twin_net_r(a, float(r.gross_r), float(r.entry_px),
                                 float(r.exit_px), float(r.r_dist))
        tw.append(h["net_r_twin"])
        comp.append(h["net_r_twin"] - float(r.funding_r or 0.0))
        cost.append(h["cost_r"])
        tier.append(h["tier"])
        bps.append(h["charter_bps_side"])
        ca.append(a)
    w["contract_asset"] = ca
    w["tier"] = tier
    w["charter_bps_side_fn"] = bps
    w["cost_r_twin"] = cost
    w["net_r_twin"] = tw
    w["net_r_twin_companion"] = comp
    return w


def _sign_flag(a: float, b: float):
    return bool(np.sign(a) != np.sign(b))


def aggregate(work: pd.DataFrame, fees_by_stem: dict, as_of: str,
              journal_sha: str) -> pd.DataFrame:
    rows = []
    stems = sorted(TP.CLASSIC5)
    toll = sorted({float(fees_by_stem[s]["round_trip_bps_used"]) for s in stems})
    for era in TP.ERAS:
        lo, hi = TP.era_window(era)
        in_e = np.array([TP.in_era(int(m), era) for m in work["entry_ms"]],
                        dtype=bool)
        for key in stems + [KEY_ALL]:
            sel = in_e if key == KEY_ALL else in_e & (work["asset"].to_numpy() == key)
            n = int(sel.sum())
            tc = float(np.mean(work["net_r"].to_numpy(dtype=float)[sel])) if n else math.nan
            twv = float(np.mean(work["net_r_twin"].to_numpy(dtype=float)[sel])) if n else math.nan
            cpv = float(np.mean(work["net_r_twin_companion"].to_numpy(dtype=float)[sel])) if n else math.nan
            if key == KEY_ALL:
                tiers = sorted(set(work.loc[in_e, "tier"])) if n else []
                mix = " · ".join(
                    f"{t}:" + ",".join(sorted(set(work.loc[in_e & (work['tier'] == t).to_numpy(), 'contract_asset'])))
                    for t in tiers)
                f = None
                asset = " ".join(sorted(fees_by_stem[s]["asset"] for s in stems))
                tier = "|".join(tiers)
            else:
                f = fees_by_stem[key]
                asset = f["asset"]
                tier = D.tier_of(asset)
                mix = f"{tier}:{asset}"
            rows.append({
                "table": TABLE, "report_only": True, "label": LABEL,
                "era": era, "era_first_entry_ms": lo, "era_last_entry_ms": hi,
                "era_cut_iso": TP.ERA_CUT_ISO, "panel": "CLASSIC5",
                "group": "ALL" if key == KEY_ALL else "asset", "key": key,
                "contract_asset": asset, "n": n,
                "tc_expectancy_r": tc, "twin_expectancy_r": twv,
                "companion_expectancy_r": cpv,
                "twin_minus_tc_r": (twv - tc) if n else math.nan,
                "sign_disagrees": _sign_flag(tc, twv) if n else None,
                "companion_sign_disagrees": _sign_flag(tc, cpv) if n else None,
                "tier": tier, "tier_mix": mix,
                "charter_bps_side": math.nan if f is None else float(f["haircut_twin_bps_side"]),
                "charter_slippage_bps_side": math.nan if f is None else float(f["haircut_twin_slippage_bps_side"]),
                "charter_round_trip_bps": math.nan if f is None else float(f["haircut_twin_round_trip_bps"]),
                "tc_round_trip_bps_used": (float(f["round_trip_bps_used"]) if f is not None
                                           else (toll[0] if len(toll) == 1 else math.nan)),
                "twin_function": TWIN_FUNCTION, "companion_label": COMPANION_LABEL,
                "tc_source": TC_SOURCE, "as_of_last_closed_4h": as_of,
                "source_journal_sha256": journal_sha,
            })
    df = pd.DataFrame(rows)
    df["era_first_entry_ms"] = df["era_first_entry_ms"].astype("Int64")
    df["era_last_entry_ms"] = df["era_last_entry_ms"].astype("Int64")
    df["sign_disagrees"] = df["sign_disagrees"].astype("boolean")
    df["companion_sign_disagrees"] = df["companion_sign_disagrees"].astype("boolean")
    return df


def as_of_of(journal: pd.DataFrame) -> str:
    v = sorted(set(journal["as_of_last_closed_4h"]))
    if len(v) != 1:
        raise SystemExit(f"HALT: the journal carries {len(v)} as-of stamps {v}")
    return str(v[0])


def parquet_bytes(df: pd.DataFrame) -> bytes:
    buf = io.BytesIO()
    df.to_parquet(buf, index=False, engine="pyarrow")
    return buf.getvalue()


# ═══════════════════════════════════════════ 4 · THE REUSE COMPARATOR
def trg2_bases(doc: dict) -> dict:
    """P-TRG-2's filed v6-base twin, per era: twin_expectancy_r -
    twin_difference_r (and the tc / companion analogues).  Fields read: arm,
    score_row.arm_era, score_row.arm_base, beside.haircut_twin.* ONLY."""
    out = {}
    for row in doc["rows"]:
        ht = (row.get("beside") or {}).get("haircut_twin")
        if not ht or ht.get("base_n") is None:
            continue
        sr = row.get("score_row") or {}
        era, base = sr.get("arm_era"), sr.get("arm_base")
        if base != "card-v6":
            continue
        if era in out:
            raise SystemExit(f"HALT: P-TRG-2 carries two card-v6 rows for era {era}")
        out[era] = {
            "arm": row["arm"], "base_n": int(ht["base_n"]),
            "function": ht.get("function"),
            "twin_base": float(ht["twin_expectancy_r"]) - float(ht["twin_difference_r"]),
            "tc_base": float(ht["tc_expectancy_r"]) - float(ht["tc_difference_r"]),
            "comp_base": (float(ht["twin_with_funding_companion_expectancy_r"])
                          - float(ht["twin_with_funding_companion_difference_r"])),
        }
    if "full" not in out:
        raise SystemExit("HALT: P-TRG-2 rows carry no full-era card-v6 haircut twin")
    return out


def filed_dp(journal: pd.DataFrame) -> int | None:
    """The journal's filing precision, MEASURED: the smallest d <= 12 at which
    every value of every input column is a fixed point of round(., d)."""
    xs = np.concatenate([journal[c].to_numpy(dtype=float) for c in NUM_COLS])
    for d in range(0, 13):
        if all(round(float(x), d) == float(x) for x in xs):
            return d
    return None


def reuse_bounds(journal: pd.DataFrame, fees_by_stem: dict, stem_asset: dict,
                 dp: int) -> pd.DataFrame:
    """Per-campaign worst-case |f(filed inputs) - f(full-precision inputs)| for
    f in {twin, companion, tc}, with h = half a unit in the last filed place:
      twin = gross_r - k (entry + exit) / r_dist,  k = charter bps/side / 1e4
      |d twin| <= h + k [ 2h / r + (e + x + 2h) h / (r (r - h)) ]
      |d comp| <= |d twin| + h        (funding_r filed at the same dp)
      |d tc|   <= h                   (net_r filed at the same dp)
    k is READ from fee_schedule.json, never from the function under test."""
    h = 0.5 * 10.0 ** (-dp)
    k = np.array([float(fees_by_stem[s]["haircut_twin_bps_side"]) / 1e4
                  for s in journal["asset"]])
    e = journal["entry_px"].to_numpy(float)
    x = journal["exit_px"].to_numpy(float)
    r = journal["r_dist"].to_numpy(float)
    if not np.all(r > h):
        raise SystemExit("HALT: an r_dist is not above the rounding half-unit")
    bt = h + k * (2 * h / r + (e + x + 2 * h) * h / (r * (r - h)))
    return pd.DataFrame({"asset": journal["asset"].to_numpy(),
                         "entry_ms": journal["entry_ms"].to_numpy(),
                         "b_twin": bt, "b_comp": bt + h,
                         "b_tc": np.full(len(r), h)})


def reuse_eval(table: pd.DataFrame, work: pd.DataFrame, disk_journal: pd.DataFrame,
               fees_by_stem: dict, stem_asset: dict, bases: dict) -> dict:
    """The comparator F-VT-REUSE asserts (and the .md prints).  Pure."""
    dp = filed_dp(disk_journal)
    res = {"dp": dp, "eras": {}, "rate_mismatch": []}
    if dp is None:
        return res
    b = reuse_bounds(disk_journal, fees_by_stem, stem_asset, dp)
    for era, base in bases.items():
        row = table[(table["era"] == era) & (table["key"] == KEY_ALL)]
        if len(row) != 1:
            res["eras"][era] = {"missing_row": True}
            continue
        row = row.iloc[0]
        in_e = np.array([TP.in_era(int(m), era) for m in b["entry_ms"]], dtype=bool)
        tol_tw = float(np.mean(b["b_twin"].to_numpy()[in_e])) + FLOAT_FLOOR
        tol_cp = float(np.mean(b["b_comp"].to_numpy()[in_e])) + FLOAT_FLOOR
        tol_tc = float(np.mean(b["b_tc"].to_numpy()[in_e])) + FLOAT_FLOOR
        d_tw = abs(float(row["twin_expectancy_r"]) - base["twin_base"])
        d_cp = abs(float(row["companion_expectancy_r"]) - base["comp_base"])
        d_tc = abs(float(row["tc_expectancy_r"]) - base["tc_base"])
        res["eras"][era] = {
            "arm": base["arm"], "n": int(row["n"]), "base_n": base["base_n"],
            "twin": float(row["twin_expectancy_r"]), "twin_base": base["twin_base"],
            "d_twin": d_tw, "tol_twin": tol_tw,
            "comp": float(row["companion_expectancy_r"]), "comp_base": base["comp_base"],
            "d_comp": d_cp, "tol_comp": tol_cp,
            "tc": float(row["tc_expectancy_r"]), "tc_base": base["tc_base"],
            "d_tc": d_tc, "tol_tc": tol_tc,
            "literal_1e12_holds": d_tw <= FLOAT_FLOOR,
            "ok": (int(row["n"]) == base["base_n"] and d_tw <= tol_tw
                   and d_cp <= tol_cp and d_tc <= tol_tc),
        }
    for s in sorted(TP.CLASSIC5):
        got = sorted(set(work.loc[work["asset"] == s, "charter_bps_side_fn"]))
        filed = float(fees_by_stem[s]["haircut_twin_bps_side"])
        tiers = sorted(set(work.loc[work["asset"] == s, "tier"]))
        if got != [filed] or tiers != [fees_by_stem[s]["haircut_twin_tier"]]:
            res["rate_mismatch"].append(
                f"{s}: function rate {got} tier {tiers} vs fee_schedule "
                f"{filed} tier {fees_by_stem[s]['haircut_twin_tier']}")
    return res


# ═══════════════════════════════════════════ 5 · THE REPORT
def _f(x, d=6) -> str:
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "—"
    return f"{x:+.{d}f}"


def _flag(x) -> str:
    return "—" if x is None or x is pd.NA else ("YES" if bool(x) else "no")


def render_md(table: pd.DataFrame, inp: dict, clause: dict, inputs: list[dict],
              reuse: dict) -> str:
    fees = inp["fees"]
    L = []
    L.append("# V6 CONTROL · HAIRCUT TWIN — an ADDED column (book level)")
    L.append("")
    L.append(f"**{LABEL}.** No CI, no p, no verdict is computed or printed here; "
             "nothing on this page is scored and no registration's verdict is read.")
    L.append("")
    L.append(f"**Clause of record** — `{clause['path']}`:{clause['lines']} "
             f"(sha256 `{clause['sha256']}`): *\"{clause['clause']}\"*")
    L.append("")
    L.append(f"**As of** {table['as_of_last_closed_4h'].iloc[0]} (the journal's own "
             "stamp; bars stamped after it are not read — this file reads no bars).")
    L.append("")
    L.append("## Law")
    L.append("")
    L.append(f"- **TC-series (untouched):** {TC_SOURCE}. The toll it carries, "
             "`round_trip_bps_used`, is printed beside every row from "
             "`data/fee_schedule.json`, unchanged.")
    L.append(f"- **Haircut twin (ADDED):** per campaign `{TWIN_FUNCTION}` with "
             "`risk_px = r_dist`. Cost law, quoted from `data/fee_schedule.json` "
             f"`haircut_twin_law`: *{fees['haircut_twin_law']}*")
    L.append(f"- **Companion:** `{COMPANION_LABEL}`. The filed twin charges fee + "
             "charter slippage and NO funding; the TC-series net_r charges funding. "
             "The companion is printed so the two can be read on one footing; it is "
             "NOT the filed twin.")
    L.append("- **Eras:** `tierc10_panel.era_window` — a campaign is in an era iff its "
             f"`entry_ms` is (cut `{TP.ERA_CUT_ISO}`). The era rows split the ONE "
             "full-corridor control book; they are not separate rides.")
    L.append("- **Sign flags:** `sign_disagrees` = sign(twin) ≠ sign(TC); "
             "`companion_sign_disagrees` = sign(companion) ≠ sign(TC).")
    L.append("")
    L.append("## Tiers (read from `data/fee_schedule.json`)")
    L.append("")
    L.append("| stem | asset | tier | slippage bps/side | charter bps/side | "
             "charter round trip bps | TC-series round trip bps (untouched) |")
    L.append("|---|---|---|---:|---:|---:|---:|")
    for s in sorted(TP.CLASSIC5):
        f = inp["fees_by_stem"][s]
        L.append(f"| {s} | {f['asset']} | {f['haircut_twin_tier']} | "
                 f"{float(f['haircut_twin_slippage_bps_side']):g} | "
                 f"{float(f['haircut_twin_bps_side']):g} | "
                 f"{float(f['haircut_twin_round_trip_bps']):g} | "
                 f"{float(f['round_trip_bps_used']):g} |")
    L.append("")
    for era in TP.ERAS:
        t = table[table["era"] == era]
        lo, hi = TP.era_window(era)
        win = ("the full corridor" if lo is None and hi is None else
               f"entries <= `{TP.ERA_CUT_ISO}`" if lo is None else
               f"entries > `{TP.ERA_CUT_ISO}`")
        L.append(f"## Era `{era}` — {win}")
        L.append("")
        L.append(f"*{LABEL} · CLASSIC5 · era {era}.* R units, per campaign.")
        L.append("")
        L.append("| key | asset | tier | charter bps/side | n | TC-series expectancy R "
                 "(untouched) | haircut twin R (ADDED) | twin − TC R | companion R "
                 "(NOT the filed twin) | twin sign ≠ TC | companion sign ≠ TC |")
        L.append("|---|---|---|---:|---:|---:|---:|---:|---:|:-:|:-:|")
        for r in t.itertuples(index=False):
            bps = "mixed" if r.key == KEY_ALL else f"{r.charter_bps_side:g}"
            asset = r.tier_mix if r.key == KEY_ALL else r.contract_asset
            L.append(f"| {r.key} | {asset} | {str(r.tier).replace('|', chr(92) + '|')} | {bps} | {r.n} | "
                     f"{_f(r.tc_expectancy_r)} | {_f(r.twin_expectancy_r)} | "
                     f"{_f(r.twin_minus_tc_r)} | {_f(r.companion_expectancy_r)} | "
                     f"{_flag(r.sign_disagrees)} | {_flag(r.companion_sign_disagrees)} |")
        L.append("")
    L.append("## Cross-check beside — the twin already filed on P-TRG-2's row")
    L.append("")
    L.append("`scores/P-TRG-2.rows.json` carries `beside.haircut_twin` with the v6 "
             "base's twin as `twin_expectancy_r − twin_difference_r` (fields read: "
             "`arm`, `score_row.arm_era`, `score_row.arm_base`, `beside.haircut_twin.*`; "
             "no verdict, CI, p or LOAO field). The ALL rows here must reproduce it. "
             f"The journal is filed at **{reuse['dp']} dp** (measured), so the "
             "tolerance is the propagated half-unit bound, not 1e-12 — see the finding "
             "below. P-TRG-2's era bases were ridden over their own era windows "
             "(tierc10_score: 'never a full-corridor control filtered afterwards'); "
             "the n and residual columns below show whether the split of the one "
             "book reproduces them.")
    L.append("")
    L.append("| era | n here | P-TRG-2 base_n | twin here | P-TRG-2 base twin | abs(Δ) | "
             "bound | abs(Δ) ≤ 1e-12 (literal) |")
    L.append("|---|---:|---:|---:|---:|---:|---:|:-:|")
    for era in TP.ERAS:
        e = reuse["eras"].get(era)
        if not e or e.get("missing_row"):
            continue
        L.append(f"| {era} | {e['n']} | {e['base_n']} | {e['twin']:+.12f} | "
                 f"{e['twin_base']:+.12f} | {e['d_twin']:.3e} | {e['tol_twin']:.3e} | "
                 f"{'yes' if e['literal_1e12_holds'] else 'no'} |")
    L.append("")
    L.append("Same residual on the untouched TC-series column and on the companion "
             "(the rounding is in the journal, not in the twin):")
    L.append("")
    L.append("| era | TC here | P-TRG-2 base TC | abs(Δ) | bound | companion here | "
             "P-TRG-2 base companion | abs(Δ) | bound |")
    L.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    for era in TP.ERAS:
        e = reuse["eras"].get(era)
        if not e or e.get("missing_row"):
            continue
        L.append(f"| {era} | {e['tc']:+.12f} | {e['tc_base']:+.12f} | {e['d_tc']:.3e} | "
                 f"{e['tol_tc']:.3e} | {e['comp']:+.12f} | {e['comp_base']:+.12f} | "
                 f"{e['d_comp']:.3e} | {e['tol_comp']:.3e} |")
    L.append("")
    L.append("## Findings (not fixed here)")
    L.append("")
    L.append("- **F-VT-REUSE-TOL.** The build spec's reuse tolerance, 1e-12, cannot be "
             "met from the filed journal: `tierc5.journal_frame` files price and R "
             "columns at 6 dp (`r6`), while P-TRG-2's base rode at full precision in "
             "memory. The leg asserts the derived bound and prints the literal "
             "comparison beside it, un-asserted. For the auditor to ratify.")
    L.append("- **F-VT-TC-PRECISION.** `panel/control_headline.parquet` files "
             "`expectancy_r` at 4 dp (`r4`, `scripts/tierc5.py:562`). F-VT-TC compares "
             "to it at that precision and holds the exact figure against the "
             "sha-verified journal instead; the transcript names which clause catches "
             "the 1e-9 sabotage.")
    L.append("")
    L.append("## Inputs (sha held against PROGRESS.json)")
    L.append("")
    L.append("| input | PROGRESS stage | bytes | sha256 |")
    L.append("|---|---|---:|---|")
    for i in inputs:
        L.append(f"| `{i['path']}` | {i['stage']} | {i['bytes']} | `{i['sha256']}` |")
    L.append("")
    L.append("Fixtures: `research_outputs/tierc10/close/FIXTURES_CLOSE_v6_control_twin.txt` "
             "(script `scripts/tierc10_close_v6_control_twin.py`).")
    L.append("")
    return "\n".join(L)


def build(inp: dict, clause: dict, inputs: list[dict]) -> dict:
    as_of = as_of_of(inp["journal"])
    work = campaign_frame(inp["journal"], inp["stem_asset"])
    table = aggregate(work, inp["fees_by_stem"], as_of, inp["journal_sha"])
    bases = trg2_bases(inp["trg2"])
    reuse = reuse_eval(table, work, inp["journal"], inp["fees_by_stem"],
                       inp["stem_asset"], bases)
    md = render_md(table, inp, clause, inputs, reuse)
    return {"work": work, "table": table, "bases": bases, "reuse": reuse,
            "md": md, "pq_bytes": parquet_bytes(table), "md_bytes": md.encode("utf-8")}


# ═══════════════════════════════════════════ 6 · THE LEGS (pure comparators)
def check_tc(table: pd.DataFrame, disk_journal: pd.DataFrame,
             headline: pd.DataFrame) -> tuple[bool, list[str], dict]:
    """(a) EXACT: every row's n and tc_expectancy_r equal the count and
    np.mean of the sha-verified journal's net_r over the same era/key — the
    mask built HERE, not by the build.  (b) HEADLINE: every full-era row's n
    equals the headline's and r4(tc_expectancy_r) equals its expectancy_r
    (aggregation raw_panel, same key) — r4 being the rounder that filed it."""
    lines, bad_a, bad_b = [], [], []
    net = disk_journal["net_r"].to_numpy(dtype=float)
    stems = disk_journal["asset"].to_numpy()
    ent = disk_journal["entry_ms"].to_numpy()
    for r in table.itertuples(index=False):
        m = np.array([TP.in_era(int(x), r.era) for x in ent], dtype=bool)
        if r.key != KEY_ALL:
            m &= stems == r.key
        n = int(m.sum())
        want = float(np.mean(net[m])) if n else math.nan
        got = float(r.tc_expectancy_r)
        same = (n == int(r.n)) and ((got == want) or (n == 0 and math.isnan(got)))
        if not same:
            bad_a.append(f"{r.era}/{r.key}: n {r.n} vs {n}, tc {got!r} vs journal {want!r}")
    hl = headline[(headline["aggregation"] == "raw_panel")
                  & (headline["label"] == "v6-control")
                  & (headline["window"] == "full_corridor")]
    full = table[table["era"] == "full"]
    for r in full.itertuples(index=False):
        grp = "ALL" if r.key == KEY_ALL else "asset"
        h = hl[(hl["group"] == grp) & (hl["key"] == r.key)]
        if len(h) != 1:
            bad_b.append(f"full/{r.key}: {len(h)} headline rows (want exactly 1)")
            continue
        h = h.iloc[0]
        r4 = TP.r4(float(r.tc_expectancy_r))
        if int(h["n"]) != int(r.n) or r4 != float(h["expectancy_r"]):
            bad_b.append(f"full/{r.key}: n {r.n} vs headline {int(h['n'])}; "
                         f"r4(tc) {r4!r} vs headline {float(h['expectancy_r'])!r}")
        else:
            lines.append(f"    full/{r.key:<8} n {r.n:>3} = headline {int(h['n']):>3} · "
                         f"r4(tc {float(r.tc_expectancy_r)!r}) = {r4!r} = headline "
                         f"{float(h['expectancy_r'])!r}")
    lines.append(f"    (a) EXACT vs sha-verified journal: {len(table) - len(bad_a)}/"
                 f"{len(table)} rows bit-equal (n and mean)")
    lines.append(f"    (b) HEADLINE at its filed 4 dp: {len(full) - len(bad_b)}/"
                 f"{len(full)} full-era rows agree")
    for x in bad_a[:6]:
        lines.append(f"    [BAD a] {x}")
    for x in bad_b[:6]:
        lines.append(f"    [BAD b] {x}")
    return (not bad_a and not bad_b), lines, {"a": len(bad_a), "b": len(bad_b)}


def check_reuse(res: dict) -> tuple[bool, list[str]]:
    lines = []
    if res["dp"] is None:
        return False, ["    [BAD] the journal's filing precision could not be measured "
                       "(no d <= 12 fixes every input) — the tolerance has no basis"]
    lines.append(f"    filed precision MEASURED: every {'/'.join(NUM_COLS)} value is a "
                 f"fixed point of round(., {res['dp']}) -> half-unit "
                 f"{0.5 * 10.0 ** (-res['dp']):.1e}")
    ok = True
    for era in TP.ERAS:
        e = res["eras"].get(era)
        if e is None:
            continue
        if e.get("missing_row"):
            ok = False
            lines.append(f"    [BAD] {era}: no ALL row")
            continue
        tag = "AUDITOR'S LEG" if era == "full" else "extension"
        ok &= e["ok"]
        lines.append(
            f"    [{'OK ' if e['ok'] else 'BAD'}] {era:<7} ({tag}) n {e['n']} vs base_n "
            f"{e['base_n']} · twin {e['twin']!r} vs P-TRG-2 base {e['twin_base']!r} "
            f"|Δ| {e['d_twin']:.3e} <= bound {e['tol_twin']:.3e}: {e['d_twin'] <= e['tol_twin']}")
        lines.append(
            f"          tc |Δ| {e['d_tc']:.3e} <= {e['tol_tc']:.3e}: {e['d_tc'] <= e['tol_tc']} · "
            f"companion |Δ| {e['d_comp']:.3e} <= {e['tol_comp']:.3e}: "
            f"{e['d_comp'] <= e['tol_comp']}")
        lines.append(
            f"          literal 1e-12 (NOT asserted, [FINDING F-VT-REUSE-TOL]): "
            f"{'holds' if e['literal_1e12_holds'] else 'does not hold'} "
            f"(|Δ| {e['d_twin']:.3e})")
    if res["rate_mismatch"]:
        ok = False
        for x in res["rate_mismatch"]:
            lines.append(f"    [BAD] rate/tier: {x}")
    else:
        lines.append("    [OK ] per asset, the twin's rate and tier == fee_schedule.json's "
                     "haircut_twin_bps_side / haircut_twin_tier")
    return ok, lines


def check_untouched(work: pd.DataFrame, disk_journal: pd.DataFrame, fee_bytes: bytes,
                    fee_sha_record: str, fee_sha_before: str, table: pd.DataFrame,
                    fees_by_stem: dict, journal_sha_now: str,
                    journal_sha_record: str) -> tuple[bool, list[str]]:
    lines, ok = [], True
    k_w = list(zip(work["asset"], work["entry_ms"]))
    k_d = list(zip(disk_journal["asset"], disk_journal["entry_ms"]))
    g = k_w == k_d and np.array_equal(work["net_r"].to_numpy(float),
                                      disk_journal["net_r"].to_numpy(float))
    ok &= g
    lines.append(f"    [{'OK ' if g else 'BAD'}] net_r carried bit-for-bit from the "
                 f"sha-verified journal on all {len(k_d)} campaigns, same keys, same order")
    g = ("net_r_twin" in work.columns and not np.array_equal(
        work["net_r_twin"].to_numpy(float), work["net_r"].to_numpy(float)))
    ok &= g
    lines.append(f"    [{'OK ' if g else 'BAD'}] the twin lives in its OWN column "
                 f"net_r_twin (not equal to net_r)")
    fs = sha256_bytes(fee_bytes)
    g = fs == fee_sha_record == fee_sha_before
    ok &= g
    lines.append(f"    [{'OK ' if g else 'BAD'}] fee_schedule.json sha now {fs[:16]}… vs "
                 f"before the build {fee_sha_before[:16]}… vs PROGRESS D-CORE "
                 f"{fee_sha_record[:16]}… (must be one value)")
    g = journal_sha_now == journal_sha_record
    ok &= g
    lines.append(f"    [{'OK ' if g else 'BAD'}] control_journal.parquet sha now "
                 f"{journal_sha_now[:16]}… vs PROGRESS PANEL/gate {journal_sha_record[:16]}… "
                 f"(must be equal)")
    want = {float(fees_by_stem[s]["round_trip_bps_used"]) for s in TP.CLASSIC5}
    got = set(table["tc_round_trip_bps_used"].astype(float))
    g = got == want and len(want) == 1
    ok &= g
    lines.append(f"    [{'OK ' if g else 'BAD'}] the TC-series toll printed beside every "
                 f"row {sorted(got)} == fee_schedule round_trip_bps_used {sorted(want)}")
    return ok, lines


def check_label(table: pd.DataFrame, md: str) -> tuple[bool, list[str]]:
    lines, ok = [], True
    bad_rows = int((~table["report_only"].astype(bool)).sum()
                   + (table["label"] != LABEL).sum())
    g = bad_rows == 0
    ok &= g
    lines.append(f"    [{'OK ' if g else 'BAD'}] every row report_only True and labelled "
                 f"{LABEL!r} ({len(table) - bad_rows}/{len(table)})")
    bad_cols = [c for c in table.columns if FORBIDDEN_COL.search(str(c))]
    g = not bad_cols
    ok &= g
    lines.append(f"    [{'OK ' if g else 'BAD'}] no ci / p / verdict / loao column "
                 f"(offenders: {bad_cols or 'none'})")
    n_tab = sum(1 for x in md.splitlines() if x.startswith("## Era "))
    n_cap = sum(1 for x in md.splitlines() if x.startswith(f"*{LABEL} · CLASSIC5 · era "))
    g = n_tab == len(TP.ERAS) and n_cap == n_tab
    ok &= g
    lines.append(f"    [{'OK ' if g else 'BAD'}] every era table in the .md carries the "
                 f"REPORT-ONLY caption ({n_cap}/{n_tab} tables, {len(TP.ERAS)} eras)")
    return ok, lines


def check_det(a: dict, b: dict, disk_pq: bytes, disk_md: bytes) -> tuple[bool, list[str]]:
    lines, ok = [], True
    for what, x, y in (("parquet", a["pq_bytes"], b["pq_bytes"]),
                       ("md", a["md_bytes"], b["md_bytes"])):
        g = x == y
        ok &= g
        lines.append(f"    [{'OK ' if g else 'BAD'}] {what}: build 1 {sha256_bytes(x)[:16]}… "
                     f"vs build 2 {sha256_bytes(y)[:16]}… (must be equal)")
    for what, x, y in (("parquet", a["pq_bytes"], disk_pq), ("md", a["md_bytes"], disk_md)):
        g = x == y
        ok &= g
        lines.append(f"    [{'OK ' if g else 'BAD'}] filed {what} {sha256_bytes(y)[:16]}… vs fresh "
                     f"build {sha256_bytes(x)[:16]}… (must be equal)")
    return ok, lines


@contextlib.contextmanager
def tier_map_copy_with(asset: str, tier: str):
    """A COPY of tierc10_data's tier map with one asset moved; the original
    object is restored (and never mutated) on exit."""
    orig = D.TIER_OF_ASSET
    snap = dict(orig)
    D.TIER_OF_ASSET = dict(orig, **{asset: tier})
    try:
        yield
    finally:
        D.TIER_OF_ASSET = orig
        if D.TIER_OF_ASSET is not orig or dict(orig) != snap:
            raise SystemExit("HALT: the tier map was not restored intact")


# ═══════════════════════════════════════════ 7 · THE RUN
def run_leg(P: Printer, name: str, fails_if: str, real, sabotages) -> bool:
    P("")
    P(f"── {name} " + "─" * max(4, 66 - len(name)))
    P(f"FAILS IF: {fails_if}")
    ok, lines = real()
    P(f"[REAL] {'GREEN' if ok else 'RED'}")
    for x in lines:
        P(x)
    all_red = True
    for sname, fn in sabotages:
        s_ok, s_lines = fn()
        red = not s_ok
        all_red &= red
        P(f"[SABOTAGE] {sname}: {'RED (as required)' if red else 'GREEN — VOID: the leg cannot see its sabotage'}")
        for x in s_lines:
            P(x)
    green = ok and all_red
    P(f"LEG {name}: {'GREEN' if green else 'RED'} (real {'pass' if ok else 'FAIL'}; "
      f"{sum(1 for _ in sabotages)} sabotage(s), all RED: {all_red})")
    return green


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(OUT_TRANSCRIPT))
    a = ap.parse_args()
    P = Printer()
    P("TIER-C10 · CLOSE · v6 CONTROL HAIRCUT TWIN (ADDED column, book level) — FIXTURES")
    P(f"{LABEL} · no CI / p / verdict · no registration scored or read for its verdict")
    P(f"script: scripts/{Path(__file__).name}")
    sub = D.assert_substrate()
    P(f"substrate: {sub.name} (NAIAD_CACHE_DIR guard held at import) · "
      f"PYTHONDONTWRITEBYTECODE=1")

    progress = json.loads(PROGRESS.read_text())
    clause = contract_clause(progress)
    P(f"contract: {clause['path']} sha {clause['sha256']} == PROGRESS contract_of_record")
    P(f"clause ({clause['path']}:{clause['lines']}): \"{clause['clause']}\"")
    P(f"as_of_of_record (PROGRESS): {progress['as_of_of_record']}")
    inputs = verify_inputs(progress)
    P("INPUTS — every sha == its PROGRESS.json stage record:")
    for i in inputs:
        P(f"  {i['path']:<48} {i['stage']:<11} {i['bytes']:>7} B  {i['sha256']}")
    fee_sha_before = sha256_file(FEES)

    inp = read_inputs()
    check_schema(inp)
    as_of = as_of_of(inp["journal"])
    if as_of != progress["as_of_of_record"]:
        raise SystemExit(f"HALT: journal as-of {as_of} != PROGRESS as_of_of_record "
                         f"{progress['as_of_of_record']}")
    P(f"journal as-of {as_of} == as_of_of_record · schema/tier/rate preamble held")

    # ═══ BUILD + FILE
    B1 = build(inp, clause, inputs)
    CLOSE.mkdir(parents=True, exist_ok=True)
    OUT_PARQUET.write_bytes(B1["pq_bytes"])
    OUT_MD.write_bytes(B1["md_bytes"])
    P("")
    P("OUTPUTS (written):")
    for p in (OUT_PARQUET, OUT_MD):
        P(f"  {rel(p):<60} {p.stat().st_size:>7} B  {sha256_file(p)}")
    P("")
    P(f"TABLE ({LABEL}) — {len(B1['table'])} rows = {len(TP.ERAS)} eras x "
      f"({len(TP.CLASSIC5)} assets + ALL):")
    for r in B1["table"].itertuples(index=False):
        P(f"  {r.era:<7} {r.key:<8} {r.tier:<3} n {r.n:>3} · tc {r.tc_expectancy_r:+.6f} · "
          f"twin {r.twin_expectancy_r:+.6f} · companion {r.companion_expectancy_r:+.6f} · "
          f"sign≠ {bool(r.sign_disagrees)} / companion sign≠ {bool(r.companion_sign_disagrees)}")

    rec = {p: progress_record(progress, s, p) for p, s in INPUT_STAGE.items()}
    results = []

    # ── F-VT-TC
    def tc_real():
        ok, ln, _ = check_tc(B1["table"], pd.read_parquet(JOURNAL), pd.read_parquet(HEADLINE))
        return ok, ln

    def tc_sab(delta, why):
        def f():
            j2 = inp["journal"].copy(deep=True)
            i = int(np.flatnonzero(j2["asset"].to_numpy() == sorted(TP.CLASSIC5)[0])[0])
            j2.loc[i, "net_r"] = float(j2.loc[i, "net_r"]) + delta
            t2 = aggregate(campaign_frame(j2, inp["stem_asset"]), inp["fees_by_stem"],
                           as_of, inp["journal_sha"])
            ok, ln, c = check_tc(t2, pd.read_parquet(JOURNAL), pd.read_parquet(HEADLINE))
            ln = [x for x in ln if not x.startswith("    full/")]
            ln.append(f"    caught by: (a) EXACT {'YES' if c['a'] else 'no'} · (b) "
                      f"HEADLINE {'YES' if c['b'] else 'no'} — {why}")
            return ok, ln
        return f

    results.append(run_leg(
        P, "F-VT-TC",
        "tc_expectancy_r for any asset / ALL row differs from "
        "panel/control_headline.parquet expectancy_r (aggregation 'raw_panel', same "
        "key) at the headline's filed precision (r4), or any row's n differs from the "
        "headline's; OR any row's n / tc_expectancy_r differs, bit for bit, from the "
        "count / np.mean of the sha-verified journal's net_r over the same era and key.",
        tc_real,
        [("+1e-9 on one net_r (first BTCUSDT campaign), build re-run", tc_sab(
            1e-9, "the headline is filed at 4 dp and cannot see 1e-9; the exact clause does")),
         ("+1e-2 on one net_r (first BTCUSDT campaign) — proves the headline clause is live",
          tc_sab(1e-2, "the BTCUSDT mean moves by more than one 4-dp step"))]))

    # ── F-VT-REUSE
    def reuse_real():
        res = reuse_eval(B1["table"], B1["work"], pd.read_parquet(JOURNAL),
                         inp["fees_by_stem"], inp["stem_asset"],
                         trg2_bases(json.loads(TRG2.read_text())))
        ok, ln = check_reuse(res)
        fn = {e: b["function"] for e, b in B1["bases"].items()}
        ln.insert(0, f"    P-TRG-2 twin function per era: {fn}")
        return ok, ln

    def reuse_tier_c():
        with tier_map_copy_with("BTC", "C"):
            w2 = campaign_frame(inp["journal"], inp["stem_asset"])
            t2 = aggregate(w2, inp["fees_by_stem"], as_of, inp["journal_sha"])
        res = reuse_eval(t2, w2, pd.read_parquet(JOURNAL), inp["fees_by_stem"],
                         inp["stem_asset"], B1["bases"])
        ok, ln = check_reuse(res)
        ln.append(f"    tier map restored: BTC -> {D.tier_of('BTC')}")
        return ok, ln

    def reuse_drop_one():
        j2 = inp["journal"].iloc[1:].reset_index(drop=True)
        w2 = campaign_frame(j2, inp["stem_asset"])
        t2 = aggregate(w2, inp["fees_by_stem"], as_of, inp["journal_sha"])
        res = reuse_eval(t2, w2, pd.read_parquet(JOURNAL), inp["fees_by_stem"],
                         inp["stem_asset"], B1["bases"])
        return check_reuse(res)

    results.append(run_leg(
        P, "F-VT-REUSE",
        "for the full era (the auditor's leg; tuning and holdout are extensions): "
        "|ALL twin_expectancy_r - (P-TRG-2 beside.haircut_twin.twin_expectancy_r - "
        "twin_difference_r)| exceeds the bound DERIVED from the journal's measured "
        "filing precision (mean per-campaign half-unit propagation + 1e-12), or the n "
        "differs from base_n; or the TC / companion residual exceeds its bound; or any "
        "asset's twin rate / tier differs from fee_schedule.json's; or the precision "
        "cannot be measured. [FINDING F-VT-REUSE-TOL: the literal 1e-12 is printed, "
        "not asserted]",
        reuse_real,
        [("BTC moved to tier C in a COPY of the tier map", reuse_tier_c),
         ("one campaign dropped from the book", reuse_drop_one)]))

    # ── F-VT-UNTOUCHED
    def unt_real():
        return check_untouched(B1["work"], pd.read_parquet(JOURNAL), FEES.read_bytes(),
                               rec[FEES]["sha256"], fee_sha_before, B1["table"],
                               inp["fees_by_stem"], sha256_file(JOURNAL),
                               rec[JOURNAL]["sha256"])

    def unt_twin_over_net():
        w2 = campaign_frame(inp["journal"], inp["stem_asset"])
        w2["net_r"] = w2["net_r_twin"]                       # THE PLANTED BUG
        t2 = aggregate(w2, inp["fees_by_stem"], as_of, inp["journal_sha"])
        return check_untouched(w2, pd.read_parquet(JOURNAL), FEES.read_bytes(),
                               rec[FEES]["sha256"], fee_sha_before, t2,
                               inp["fees_by_stem"], sha256_file(JOURNAL),
                               rec[JOURNAL]["sha256"])

    def unt_fee_bytes():
        b = bytearray(FEES.read_bytes())                     # an in-memory COPY
        b[len(b) // 2] ^= 0x01
        return check_untouched(B1["work"], pd.read_parquet(JOURNAL), bytes(b),
                               rec[FEES]["sha256"], fee_sha_before, B1["table"],
                               inp["fees_by_stem"], sha256_file(JOURNAL),
                               rec[JOURNAL]["sha256"])

    results.append(run_leg(
        P, "F-VT-UNTOUCHED",
        "net_r in the build's campaign frame is not bit-identical (same keys, same "
        "order) to the sha-verified journal's, or the twin is not in its own column; "
        "or fee_schedule.json's bytes hash to anything but the sha taken before the "
        "build AND its PROGRESS D-CORE record; or control_journal.parquet's sha left "
        "its PANEL/gate record; or the TC-series toll printed beside a row is not "
        "fee_schedule's round_trip_bps_used.",
        unt_real,
        [("the twin written over net_r", unt_twin_over_net),
         ("one byte of (an in-memory copy of) fee_schedule.json flipped", unt_fee_bytes)]))

    # ── F-VT-LABEL (extension)
    def lab_real():
        return check_label(B1["table"], B1["md"])

    def lab_verdict_col():
        t2 = B1["table"].copy()
        t2["verdict"] = "n/a"
        return check_label(t2, B1["md"])

    def lab_row_unlabelled():
        t2 = B1["table"].copy()
        t2.loc[0, "report_only"] = False
        return check_label(t2, B1["md"])

    results.append(run_leg(
        P, "F-VT-LABEL",
        "any row is not report_only / not labelled REPORT-ONLY, any column name is a "
        "ci / p / verdict / loao column, or an era table in the .md lacks the "
        "REPORT-ONLY caption.",
        lab_real,
        [("a 'verdict' column added", lab_verdict_col),
         ("one row un-marked report_only", lab_row_unlabelled)]))

    # ── F-DET
    def det_real():
        B2 = build(read_inputs(), clause, inputs)
        B3 = build(read_inputs(), clause, inputs)
        return check_det(B2, B3, OUT_PARQUET.read_bytes(), OUT_MD.read_bytes())

    def det_shuffled():
        B2 = build(read_inputs(), clause, inputs)
        t = B2["table"].iloc[::-1].reset_index(drop=True)    # an unordered emit
        B3 = dict(B2, pq_bytes=parquet_bytes(t))
        return check_det(B2, B3, OUT_PARQUET.read_bytes(), OUT_MD.read_bytes())

    results.append(run_leg(
        P, "F-DET",
        "two in-process builds, each from a fresh read of every input, are not "
        "byte-identical to each other (parquet and md), or the filed outputs are not "
        "byte-identical to them.",
        det_real,
        [("second build emits its rows in reverse order", det_shuffled)]))

    # ═══ POST: nothing moved
    post = verify_inputs(progress)
    moved = [i["path"] for i, j in zip(inputs, post) if i["sha256"] != j["sha256"]]
    P("")
    P(f"POST: every input re-hashes to its PROGRESS record after the run "
      f"(moved: {moved or 'none'})")
    n_g = sum(results)
    P("")
    P(f"TALLY: {len(results)} legs · {n_g} GREEN · {len(results) - n_g} RED")
    P("EXIT " + ("0" if n_g == len(results) and not moved else "1"))
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(P.text(), encoding="utf-8")
    print(f"[transcript] {a.out} sha256 {sha256_file(Path(a.out))}", flush=True)
    return 0 if n_g == len(results) and not moved else 1


if __name__ == "__main__":
    sys.exit(main())
