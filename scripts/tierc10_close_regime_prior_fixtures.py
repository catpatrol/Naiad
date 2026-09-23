#!/usr/bin/env python
"""TIER-C10 · CLOSE · REGIME-PRIOR — THE FIXTURES (Tier-E · report-only).

The twin of scripts/tierc10_close_regime_prior.py.  Every leg reads the FILED
outputs under research_outputs/tierc10/close/ (never a fresh in-memory build),
states what makes it FAIL, and carries a SABOTAGE that must go RED.  A leg is
GREEN only when the real check is GREEN AND its sabotage is RED; a sabotage
that stays GREEN makes the leg RED (the check could not see the breach).

  F-RP-SHA        FAILS IF any input's sha256 differs from its PROGRESS.json
                  stage record, the contract from contract_of_record, or the
                  ARGUS note from its committed blob at HEAD.
                  SABOTAGE: a copy of census/coverage.parquet with one byte
                  appended, offered in its place.
  F-RP-JOIN       FAILS IF a journal campaign lacks exactly one entry stamp and
                  exactly one exit stamp, or an entry/exit stamp joins no
                  campaign, or an exit stamp is off its journal exit_ms.
                  SABOTAGE: one exit stamp duplicated in a copy of the stamps.
  F-RP-ANCHOR     FAILS IF Table 2's entry-state marginal (n, net_r_sum,
                  expectancy_r, win_rate_pct per state, incl. __ALL__) differs
                  by any amount from stamps/control_entry_by_state.parquet.
                  SABOTAGE: one entry stamp's state relabelled in a copy of the
                  stamps, Table 2 rebuilt from the copy.
  F-RP-VERBATIM   FAILS IF any Table 1 value in a verbatim column differs from
                  census/coverage.parquet.
                  SABOTAGE: +0.01 on one bars_in_live_range_pct in a copy.
  F-RP-EXIT-ASOF  FAILS IF any exit stamp's rf4h_bar_close_ms > its
                  instant_close_ms.
                  SABOTAGE: one exit stamp moved one 4h bar later in a copy.
  F-RP-COLLAR     FAILS IF a Tier-E collar column is missing / null / off-law on
                  either table, or a verdict / ci / p column exists.
                  SABOTAGE: a 'verdict' column added to a copy of Table 2.
  F-RP-QUOTE      FAILS IF the ARGUS note's item 2 is not whole in the md and on
                  every Table 1 row, or Table 1's columns are not the declared
                  set (no threshold column parsed out of the quote).
                  SABOTAGE: the quote's last character dropped in a copy of the
                  md.
  F-DET           FAILS IF two whole subprocess runs of the build (each into its
                  own temp dir outside the repo) differ from each other or from
                  the filed outputs by one byte, or either exits non-zero.
                  SABOTAGE: one byte of run 2's Table 2 flipped in a copy.

The transcript (close/FIXTURES_CLOSE_regime_prior.txt) carries no clock and no
temp path, so two whole runs must produce it byte-identically.

Run:
  export NAIAD_CACHE_DIR=/Users/luis/.cache/naiad/snapshots/tc10_20260921 \\
         PYTHONDONTWRITEBYTECODE=1
  ~/venvs/naiad/bin/python scripts/tierc10_close_regime_prior_fixtures.py
"""
from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import tierc10_close_regime_prior as RP                              # noqa: E402  (runs the substrate guard)

import numpy as np                                                   # noqa: E402
import pandas as pd                                                  # noqa: E402

ROOT = RP.ROOT
MODULE = Path(RP.__file__).resolve()
SELF = Path(__file__).resolve()
TRANSCRIPT: list[str] = []


def out(s: str = "") -> None:
    TRANSCRIPT.append(s)
    print(s, flush=True)


def sha(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def read_inputs() -> dict:
    d = {}
    for key, rel, _ in RP.INPUTS:
        p = ROOT / rel
        d[key] = (__import__("json").loads(p.read_text()) if p.suffix == ".json"
                  else pd.read_parquet(p))
    return d


def read_filed() -> dict:
    f = {}
    for n in RP.OUTPUT_NAMES:
        p = RP.OUT / n
        if not p.is_file():
            raise SystemExit(f"HALT: filed output {p.relative_to(ROOT)} is absent "
                             "— run the build first")
    f["t1"] = pd.read_parquet(RP.OUT / RP.T1_NAME)
    f["t2"] = pd.read_parquet(RP.OUT / RP.T2_NAME)
    f["md"] = (RP.OUT / RP.MD_NAME).read_text()
    return f


# ═══════════════════════════════════════════════════════════ THE LEGS
def leg_sha(inp, filed):
    real = RP.check_input_shas()
    with tempfile.TemporaryDirectory(prefix="rp_sha_") as td:
        cp = Path(td) / "coverage.parquet"
        shutil.copyfile(ROOT / RP.INPUTS[0][1], cp)
        with open(cp, "ab") as fh:
            fh.write(b"\0")
        sab = RP.check_input_shas({"coverage": cp})
    return real, sab


def leg_join(inp, filed):
    real = RP.check_join(inp["journal"], inp["stamped"])
    st = inp["stamped"]
    x = st[st["instant_kind"] == "exit"]
    sab_st = pd.concat([st, x.iloc[[0]]], ignore_index=True)
    sab = RP.check_join(inp["journal"], sab_st)
    return real, sab


def leg_anchor(inp, filed):
    real = RP.check_anchor(filed["t2"], inp["anchor"])
    st = inp["stamped"].copy()
    ent_idx = st.index[st["instant_kind"] == "entry"][0]
    was = st.at[ent_idx, "rf4h_macro_state"]
    cand = [s for s in RP.MACRO_STATES if s not in (was, "NONE")]
    st.at[ent_idx, "rf4h_macro_state"] = cand[0]
    j = RP.join_book(inp["journal"], st)
    t2 = RP.build_table2(j, inp["journal"], inp["stamps_manifest"])
    ok, lines = RP.check_anchor(t2, inp["anchor"])
    lines = [f"[info] relabelled entry stamp {st.at[ent_idx, 'unit_id']}: "
             f"{was} -> {cand[0]}"] + lines
    return real, (ok, lines)


def leg_verbatim(inp, filed):
    real = RP.check_verbatim(filed["t1"], inp["coverage"])
    t1 = filed["t1"].copy()
    t1.loc[0, "bars_in_live_range_pct"] = t1.loc[0, "bars_in_live_range_pct"] + 0.01
    sab = RP.check_verbatim(t1, inp["coverage"])
    sab[1].insert(0, f"[info] +0.01 on bars_in_live_range_pct of "
                     f"{t1.loc[0, 'asset']} {t1.loc[0, 'lens']} {t1.loc[0, 'scale_kind']}")
    return real, sab


def leg_exit_asof(inp, filed):
    real = RP.check_exit_asof(inp["stamped"])
    st = inp["stamped"].copy()
    steps = sorted(set((st["rf4h_bar_close_ms"] - st["rf4h_bar_open_ms"]).astype(int)))
    if len(steps) != 1:
        raise SystemExit(f"HALT: the stamps' 4h bar is not one width: {steps}")
    step = steps[0]
    xi = st.index[st["instant_kind"] == "exit"][0]
    st.at[xi, "rf4h_bar_open_ms"] = int(st.at[xi, "rf4h_bar_open_ms"]) + step
    st.at[xi, "rf4h_bar_close_ms"] = int(st.at[xi, "rf4h_bar_close_ms"]) + step
    ok, lines = RP.check_exit_asof(st)
    lines = [f"[info] exit stamp {st.at[xi, 'unit_id']} moved one bar "
             f"({step} ms, the stamps' own bar width) later"] + lines
    return real, (ok, lines)


def leg_collar(inp, filed):
    real = RP.check_collar({"Table 1": filed["t1"], "Table 2": filed["t2"]})
    t2 = filed["t2"].copy()
    t2["verdict"] = None
    sab = RP.check_collar({"Table 1": filed["t1"], "Table 2": t2})
    return real, sab


def leg_quote(inp, filed):
    quote = RP.argus_item_2()
    decl = RP.t1_declared_columns(inp["coverage"])
    real = RP.check_quote(filed["md"], filed["t1"], decl, quote)
    md = filed["md"].replace(quote, quote[:-1])
    sab = RP.check_quote(md, filed["t1"], decl, quote)
    return real, sab


def _compare(a: dict, b: dict, la: str, lb: str) -> tuple[bool, list[str]]:
    ok, lines = True, []
    for n in RP.OUTPUT_NAMES:
        g = a.get(n) is not None and a.get(n) == b.get(n)
        ok &= g
        ha = hashlib.sha256(a[n]).hexdigest() if a.get(n) is not None else None
        hb = hashlib.sha256(b[n]).hexdigest() if b.get(n) is not None else None
        lines.append(f"[{'OK ' if g else 'BAD'}] {n:<38} {la} {ha} · {lb} {hb}")
    return ok, lines


def leg_det(inp, filed):
    runs, codes = [], []
    with tempfile.TemporaryDirectory(prefix="rp_det_") as td:
        for k in ("1", "2"):
            d = Path(td) / f"run{k}"
            r = subprocess.run([sys.executable, str(MODULE), "--out", str(d)],
                               capture_output=True, text=True, env=dict(os.environ),
                               cwd=str(ROOT))
            codes.append(r.returncode)
            runs.append({n: ((d / n).read_bytes() if (d / n).is_file() else None)
                         for n in RP.OUTPUT_NAMES})
    filed_b = {n: (RP.OUT / n).read_bytes() for n in RP.OUTPUT_NAMES}
    ok = all(c == 0 for c in codes)
    lines = [f"[{'OK ' if ok else 'BAD'}] subprocess exit codes {codes}"]
    g, l12 = _compare(runs[0], runs[1], "run1", "run2")
    ok &= g
    lines += l12
    g, l2f = _compare(runs[1], filed_b, "run2", "filed")
    ok &= g
    lines += l2f
    sab_b = dict(runs[1])
    if sab_b.get(RP.T2_NAME) is not None:
        b = bytearray(sab_b[RP.T2_NAME])
        b[len(b) // 2] ^= 0x01
        sab_b[RP.T2_NAME] = bytes(b)
    sok, sl = _compare(runs[0], sab_b, "run1", "run2-flipped")
    return (ok, lines), (sok, ["[info] one byte (the middle one) of run 2's "
                               f"{RP.T2_NAME} flipped"] + sl)


LEGS = (
    ("F-RP-SHA", leg_sha,
     "any input's sha256 differs from its PROGRESS.json stage record, the "
     "contract from contract_of_record, or the ARGUS note from its committed "
     "blob at HEAD",
     "a copy of census/coverage.parquet with one byte appended, offered in its "
     "place"),
    ("F-RP-JOIN", leg_join,
     "a journal campaign lacks exactly one entry stamp and exactly one exit "
     "stamp, or an entry/exit stamp joins no campaign, or an exit stamp is off "
     "its campaign's journal exit_ms",
     "one exit stamp duplicated in a copy of the stamps"),
    ("F-RP-ANCHOR", leg_anchor,
     "Table 2's entry-state marginal (n, net_r_sum, expectancy_r, win_rate_pct "
     "per state, incl. __ALL__) differs by any amount from "
     "stamps/control_entry_by_state.parquet",
     "one entry stamp's state relabelled in a copy of the stamps; Table 2 "
     "rebuilt from the copy"),
    ("F-RP-VERBATIM", leg_verbatim,
     "any Table 1 value in a verbatim column differs from "
     "census/coverage.parquet (exact: dtype and value)",
     "+0.01 on one bars_in_live_range_pct in a copy of the filed Table 1"),
    ("F-RP-EXIT-ASOF", leg_exit_asof,
     "any exit stamp's rf4h_bar_close_ms is later than its instant_close_ms "
     "(or null)",
     "one exit stamp moved one 4h bar later in a copy of the stamps"),
    ("F-RP-COLLAR", leg_collar,
     "a Tier-E collar column (tier / selection_not_a_result / "
     "m_selections_this_table / in_sample / gates='nothing') is missing, null "
     "or off-law on either filed table, or a verdict / ci / p column exists",
     "a 'verdict' column added to a copy of the filed Table 2"),
    ("F-RP-QUOTE", leg_quote,
     "the ARGUS note's item 2 is not whole in the filed md and on every Table 1 "
     "row, or Table 1's columns are not the declared set",
     "the quote's last character dropped in a copy of the filed md"),
    ("F-DET", leg_det,
     "two whole subprocess runs of the build (each into its own temp dir "
     "outside the repo) differ from each other or from the filed outputs by "
     "one byte, or either exits non-zero",
     "one byte of run 2's Table 2 flipped in a copy"),
)


def main() -> int:
    out("=" * 78)
    out("TIER-C10 · CLOSE · REGIME-PRIOR — FIXTURES (Tier-E · report-only)")
    out("=" * 78)
    out(f"  module   {MODULE.relative_to(ROOT)}  sha256 {sha(MODULE)}")
    out(f"  fixtures {SELF.relative_to(ROOT)}  sha256 {sha(SELF)}")
    out("  filed outputs under research_outputs/tierc10/close/:")
    filed = read_filed()
    for n in RP.OUTPUT_NAMES:
        out(f"    {n:<38} sha256 {sha(RP.OUT / n)}")
    out("  inputs (read-only):")
    for key, rel, stage in RP.INPUTS:
        out(f"    {rel}  [{stage}]  sha256 {sha(ROOT / rel)}")
    inp = read_inputs()
    out("")
    results = []
    for name, fn, fails_if, sabotage in LEGS:
        out("-" * 78)
        out(f"LEG {name}")
        out(f"  FAILS IF: {fails_if}")
        out(f"  SABOTAGE: {sabotage} — must go RED")
        (rok, rlines), (sok, slines) = fn(inp, filed)
        out(f"  real: {'GREEN' if rok else 'RED'}")
        for s in rlines:
            out(f"    {s}")
        out(f"  sabotage: {'RED (as required)' if not sok else 'GREEN — THE CHECK IS BLIND'}")
        for s in slines:
            out(f"    {s}")
        g = bool(rok) and not bool(sok)
        results.append((name, g, rok, sok))
        out(f"  => {name} {'GREEN' if g else 'RED'}")
    out("-" * 78)
    n_g = sum(1 for _, g, _, _ in results if g)
    n_sab = sum(1 for _, _, _, s in results if not s)
    out(f"SUMMARY: {len(results)} legs · {n_g} GREEN · {len(results) - n_g} RED · "
        f"{n_sab}/{len(results)} sabotages RED")
    for name, g, rok, sok in results:
        out(f"  {name:<16} {'GREEN' if g else 'RED'}   real "
            f"{'GREEN' if rok else 'RED'} · sabotage {'RED' if not sok else 'GREEN'}")
    code = 0 if n_g == len(results) else 1
    out(f"exit {code}")
    RP.OUT.mkdir(parents=True, exist_ok=True)
    p = RP.OUT / RP.FIX_NAME
    tmp = p.with_name(p.name + ".tmp")
    tmp.write_text("\n".join(TRANSCRIPT) + "\n")
    os.replace(tmp, p)
    return code


if __name__ == "__main__":
    sys.exit(main())
