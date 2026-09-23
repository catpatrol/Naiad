#!/usr/bin/env python
"""TIER-C10 · CLOSE — THE FORWARD STRIP.  REPORT-ONLY — FORWARD STRIP — NEVER SCORED.

Contract of record exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md:114-115
  "FORWARD STRIP (report-only): the 5-asset v6 book from TC9's as-of
   (2026-08-22T00:00Z) to this corridor's end — printed, labeled, never scored."
and :131 "§0 verdicts first: six rows + the admitted list + the forward strip".

WHAT IT DOES
  Reads the PANEL/gate control journal (the v6 card on the five classics over
  THIS corridor, F-CTRL's book), sha-anchored to PROGRESS.json, and prints the
  campaigns that fall in the window from TC9's as-of to this corridor's end:
    ENTERED-IN-STRIP  entry_ms >= tc9_asof_ms
    CONTINUATION      entry_ms <  tc9_asof_ms <= exit_ms  (a campaign TC9 saw
                      open at its as-of — reported as a continuation, never a diff)
  A row whose exit_reason is 'corridor_end' is OPEN-AT-CORRIDOR-END: marked to
  the pin, not realized.  Every journal column carried is VERBATIM (the R
  columns, the stamps and the as_of_* warranty columns).  The charter HAIRCUT
  TWIN is an ADDED column (tierc10_data.haircut_twin_net_r, stem -> contract
  asset read from the filed Stage D manifest, as tierc10_score does); the
  TC-series net_r is untouched.  Counts and sums only: no CI, no p, no
  verdict, no LOAO, no FDR bar.  No registration, score or verdict file is
  READ; scores/ and registrations/ are only HASHED, to prove they did not move.
  No kline file is read at all: every market number is a column of the filed
  journal (so neither tierc10_data.load_asof nor tierc2_baseline.load_klines
  is reached).

INPUTS (each read this run; none typed)
  1 research_outputs/tierc10/panel/control_journal.parquet — sha256 must equal
    PROGRESS.json stage 'PANEL/gate' artifact_shas; HALT otherwise.
  2 TC9's as-of — research_outputs/tierc9/build_manifest.json .as_of AND the
    single distinct value of research_outputs/tierc9/trade_journal_control.parquet
    column as_of_last_closed_4h; HALT unless equal.  The contract literal is
    parsed from the contract of record (sha-checked against PROGRESS.json) and
    only COMPARED against (HALT on disagreement), never used.
  3 this corridor's end — PROGRESS.json as_of_of_record and
    as_of_last_closed_4h_close_ms (cross-checked against AS_OF_PIN.json).
  4 F-CTRL/b's live-only list — the '[OK ] FILED tierc9/trade_journal_control:
    N live-only campaign(s) [...]' line of research_outputs/tierc10/panel/
    FIXTURES_PANEL.txt, whose sha must equal the PANEL/gate record.

OUTPUTS (only under research_outputs/tierc10/close/)
  FORWARD_STRIP.parquet · FORWARD_STRIP.md · FIXTURES_CLOSE_forward_strip.txt
  (--fixtures) · _det_forward_strip/seed_{1,20260921}/ (F-DET's twin runs).

FIXTURE LEGS (--fixtures; each states FAILS IF and carries sabotage that must go RED)
  F-FS-SUBSTRATE  the run HALTs off the frozen snapshot.
  F-FS-WINDOW     membership is exactly the two predicates (+ TC9's own
                  corridor_end rows == the CONTINUATION set, cross-process).
  F-FS-ANCHOR     ENTERED (asset, entry_ts) == F-CTRL/b's live-only list.
  F-FS-VERBATIM   every carried column equals the journal by ANY amount.
  F-FS-ASOF       every row stamped the corridor of record; no exit past the pin.
  F-FS-TWIN       the twin rides on every row and never over net_r.
  F-FS-CLOSURE    no bar loader, no scorer, no registry reachable from here.
  F-DET           two subprocess runs (PYTHONHASHSEED 1, 20260921) byte-identical.
  F-FS-NOSCORE    no verdict/ci_*/p_one_sided/clears_bh_bar/loao_* column, no
                  scored=True row, and not one byte of scores/, registrations/,
                  the registry, PROGRESS.json, FIXTURES_RESUME.txt or an input moved.

Run:  export NAIAD_CACHE_DIR=/Users/luis/.cache/naiad/snapshots/tc10_20260921 PYTHONDONTWRITEBYTECODE=1
      ~/venvs/naiad/bin/python scripts/tierc10_close_forward_strip.py [--fixtures]
Exit: 0 built (and with --fixtures every leg GREEN) · 1 HALT or a RED leg.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import math
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = Path.home() / ".cache" / "naiad" / "snapshots" / "tc10_20260921"
LIVE_CACHE = Path.home() / ".cache" / "naiad" / "data_cache"


def guard_substrate(env: str | None) -> Path:
    """HALTS IF NAIAD_CACHE_DIR is unset, names the live cache, or is not the
    TC10 snapshot.  The live-cache test is on the PATH STRING first, so the
    live cache is never even stat'ed by this guard."""
    if not env:
        raise SystemExit("HALT: NAIAD_CACHE_DIR is unset — the forward strip runs only on "
                         f"the frozen snapshot {SNAPSHOT}")
    norm = Path(os.path.normpath(os.path.expanduser(env)))
    if norm == LIVE_CACHE or LIVE_CACHE in norm.parents:
        raise SystemExit("HALT: NAIAD_CACHE_DIR names the LIVE cache — READ-NEVER, WRITE-NEVER for TC10")
    got = norm.resolve()
    if got == LIVE_CACHE or LIVE_CACHE in got.parents:
        raise SystemExit("HALT: NAIAD_CACHE_DIR resolves into the LIVE cache — READ-NEVER, WRITE-NEVER")
    if got != SNAPSHOT.resolve():
        raise SystemExit(f"HALT: NAIAD_CACHE_DIR={got} is not the TC10 snapshot {SNAPSHOT}")
    return got


guard_substrate(os.environ.get("NAIAD_CACHE_DIR"))

sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import numpy as np                                                   # noqa: E402
import pandas as pd                                                  # noqa: E402

import tierc10_data as D     # its own guard re-checks the substrate  # noqa: E402

# ═══════════════════════════════════════════════════════════════ constants
TC10 = ROOT / "research_outputs" / "tierc10"
OUT = TC10 / "close"
DET_ROOT = OUT / "_det_forward_strip"
PROGRESS = TC10 / "PROGRESS.json"
PROGRESS_REL = "research_outputs/tierc10/PROGRESS.json"
JOURNAL_REL = "research_outputs/tierc10/panel/control_journal.parquet"
PANEL_FIX_REL = "research_outputs/tierc10/panel/FIXTURES_PANEL.txt"
PANEL_STAGE = "PANEL/gate"
TC9_MANIFEST_REL = "research_outputs/tierc9/build_manifest.json"
TC9_JOURNAL_REL = "research_outputs/tierc9/trade_journal_control.parquet"
AS_OF_PIN_REL = "research_outputs/tierc10/data/AS_OF_PIN.json"

PARQUET = "FORWARD_STRIP.parquet"
MD = "FORWARD_STRIP.md"
TRANSCRIPT = "FIXTURES_CLOSE_forward_strip.txt"

TIER = "REPORT-ONLY — FORWARD STRIP — NEVER SCORED"
ENTERED = "ENTERED-IN-STRIP"
CONT = "CONTINUATION"
OPEN = "OPEN-AT-CORRIDOR-END"
OPEN_REASON = "corridor_end"
OPEN_TAIL = f"{OPEN} — marked to the pin, not realized"
CLOSED_TAIL = "CLOSED — realized"

STEP_MS = int(D.STEP_MS["4h"])
SEED = D.SEED
DET_SEEDS = (1, SEED)

CARRY = ["asset", "lane", "direction", "arm_ts", "entry_ms", "entry_ts", "exit_ms",
         "exit_ts", "exit_reason", "bars_held", "entry_px", "exit_px", "r_dist",
         "gross_r", "fee_r", "funding_r", "net_r"]
R_COLS = ["gross_r", "fee_r", "funding_r", "net_r"]
TWIN = "haircut_twin_net_r"
TWIN_COLS = [TWIN, "haircut_twin_tier", "haircut_twin_charter_round_trip_bps"]
HEAD_COLS = ["label", "window", "tier", "scored"]

FORBIDDEN_COL = re.compile(r"^(verdict|ci_|p_one_sided|clears_bh_bar|loao_)", re.I)
BANNED_CALLS = {"load_klines", "score", "finish_family", "register"}
BANNED_MODULES = {"tierc2_baseline", "tierc10_panel", "tierc10_score",
                  "tierc10_file_registrations"}

CONTRACT_RX = re.compile(
    r"FORWARD STRIP \(report-only\): the 5-asset v6 book from TC9's as-of\s+"
    r"\((\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2})?Z)\)")
LIVE_ONLY_RX = re.compile(
    r"^\s*\[OK \] FILED tierc9/trade_journal_control: (\d+) live-only campaign\(s\) "
    r"(\[.*?\]), all entered AFTER the referee's last bar (\S+)")

LINES: list[str] = []


def say(msg: str = "") -> None:
    print(msg, flush=True)
    LINES.append(msg)


def iso(ms) -> str:
    return D.iso(int(ms))


def to_ms(s: str) -> int:
    ts = pd.Timestamp(s)
    if ts.tzinfo is None:
        raise SystemExit(f"HALT: timestamp {s!r} carries no zone — refusing to guess UTC")
    return int(ts.tz_convert("UTC").value // 1_000_000)


def sha(path: Path) -> str:
    return D.file_sha256(path)


def fnum(x) -> str:
    return repr(float(x))


def asof_columns(df: pd.DataFrame) -> list[str]:
    return [c for c in df.columns if c.startswith("as_of_") or c == "warranty"]


# ═══════════════════════════════════════════════════════════ read-only guard
def protected_files(contract_rel: str) -> list[Path]:
    """Everything this build must NEVER move: scores/, registrations/ (the
    registry included), REGISTRY*, PROGRESS.json, FIXTURES_RESUME.txt, and
    every input it reads."""
    fs: list[Path] = []
    for d in (TC10 / "scores", TC10 / "registrations"):
        fs += [p for p in d.rglob("*") if p.is_file()]
    fs += [p for p in TC10.glob("REGISTRY*") if p.is_file()]
    fs += [PROGRESS, TC10 / "FIXTURES_RESUME.txt", ROOT / JOURNAL_REL, ROOT / PANEL_FIX_REL,
           ROOT / TC9_MANIFEST_REL, ROOT / TC9_JOURNAL_REL, ROOT / AS_OF_PIN_REL,
           ROOT / contract_rel]
    return sorted(set(fs))


def bytes_snapshot(contract_rel: str) -> dict[str, str]:
    return {str(p.relative_to(ROOT)): sha(p) for p in protected_files(contract_rel)}


# ═══════════════════════════════════════════════════════════════ inputs
def read_inputs() -> dict:
    prog = json.loads(PROGRESS.read_text())

    # (1) the book, anchored to the PANEL/gate record
    st = [s for s in prog["stages"] if s.get("stage") == PANEL_STAGE]
    if len(st) != 1:
        raise SystemExit(f"HALT: PROGRESS.json holds {len(st)} '{PANEL_STAGE}' stage(s), want 1")
    rec = st[0]["artifact_shas"]
    anchors = {}
    for relp in (JOURNAL_REL, PANEL_FIX_REL):
        if relp not in rec:
            raise SystemExit(f"HALT: PROGRESS.json '{PANEL_STAGE}' records no sha for {relp}")
        p = ROOT / relp
        got, want = sha(p), rec[relp]["sha256"]
        if got != want or p.stat().st_size != rec[relp]["bytes"]:
            raise SystemExit(f"HALT: {relp} sha256 {got} / {p.stat().st_size} B != the "
                             f"'{PANEL_STAGE}' record {want} / {rec[relp]['bytes']} B")
        anchors[relp] = got
    journal = pd.read_parquet(ROOT / JOURNAL_REL)
    missing = [c for c in CARRY if c not in journal.columns]
    if missing:
        raise SystemExit(f"HALT: the journal lacks carried column(s) {missing}")
    panels = sorted(set(journal["as_of_panel"].astype(str)))
    n_assets = sorted(set(int(x) for x in journal["as_of_n_assets"]))
    assets = sorted(set(journal["asset"].astype(str)))
    if panels != ["CLASSIC5"] or n_assets != [5] or len(assets) != 5:
        raise SystemExit(f"HALT: the journal is not the 5-asset book: panel {panels}, "
                         f"n_assets {n_assets}, assets {assets}")
    keys = list(zip(journal["asset"].astype(str), journal["entry_ms"].astype("int64")))
    if len(set(keys)) != len(keys):
        raise SystemExit("HALT: (asset, entry_ms) is not a key of the journal")

    # (2) TC9's as-of, from two files that must agree
    man = json.loads((ROOT / TC9_MANIFEST_REL).read_text())
    m_asof = man.get("as_of")
    t9 = pd.read_parquet(ROOT / TC9_JOURNAL_REL)
    vals = sorted(set(t9["as_of_last_closed_4h"].astype(str)))
    if len(vals) != 1:
        raise SystemExit(f"HALT: {TC9_JOURNAL_REL} as_of_last_closed_4h holds {len(vals)} values {vals}")
    if not isinstance(m_asof, str) or m_asof != vals[0]:
        raise SystemExit(f"HALT: TC9's as-of disagrees: {TC9_MANIFEST_REL} .as_of={m_asof!r} vs "
                         f"{TC9_JOURNAL_REL} as_of_last_closed_4h={vals[0]!r}")
    tc9_iso = m_asof
    tc9_ms = to_ms(tc9_iso)
    if tc9_ms % STEP_MS:
        raise SystemExit(f"HALT: TC9's as-of {tc9_iso} is off the 4h grid")

    # the contract literal — compared, never used
    c = prog["contract_of_record"]
    cpath = ROOT / c["path"]
    csha = sha(cpath)
    if csha != c["sha256"]:
        raise SystemExit(f"HALT: contract {c['path']} sha256 {csha} != PROGRESS record {c['sha256']}")
    text = cpath.read_text()
    mm = CONTRACT_RX.search(text)
    if not mm:
        raise SystemExit(f"HALT: the FORWARD STRIP clause is not in {c['path']}")
    lit = mm.group(1)
    lit_line = text[:mm.start(1)].count("\n") + 1
    clause_line = text[:mm.start()].count("\n") + 1
    if to_ms(lit) != tc9_ms:
        raise SystemExit(f"HALT: contract literal {lit} ({c['path']}:{lit_line}) != TC9's as-of "
                         f"{tc9_iso} read from {TC9_MANIFEST_REL} and {TC9_JOURNAL_REL}")

    # (3) this corridor's end
    end_iso = prog["as_of_of_record"]
    end_ms = int(prog["as_of_last_closed_4h_close_ms"])
    if iso(end_ms) != end_iso:
        raise SystemExit(f"HALT: PROGRESS as_of_of_record {end_iso} != as_of_last_closed_4h_close_ms "
                         f"{end_ms} ({iso(end_ms)})")
    pin = D.load_pin()
    if pin["as_of_last_closed_4h_close_ms"] != end_ms or pin["as_of_last_closed_4h"] != end_iso:
        raise SystemExit(f"HALT: {AS_OF_PIN_REL} ({pin['as_of_last_closed_4h']}) disagrees with "
                         f"PROGRESS.json ({end_iso})")
    if not tc9_ms < end_ms:
        raise SystemExit(f"HALT: TC9's as-of {tc9_iso} is not before this corridor's end {end_iso}")

    # (4) F-CTRL/b's live-only list
    lines = (ROOT / PANEL_FIX_REL).read_text().splitlines()
    hits = [(i + 1, LIVE_ONLY_RX.match(ln)) for i, ln in enumerate(lines)]
    hits = [(n, m) for n, m in hits if m]
    if len(hits) != 1:
        raise SystemExit(f"HALT: {PANEL_FIX_REL} holds {len(hits)} '[OK ] FILED "
                         "tierc9/trade_journal_control: N live-only' line(s), want exactly 1")
    live_line, lm = hits[0]
    live_n = int(lm.group(1))
    live_only = sorted((str(a), str(t)) for a, t in ast.literal_eval(lm.group(2)))
    referee_last = lm.group(3)
    if live_n != len(live_only):
        raise SystemExit(f"HALT: the live-only line says {live_n} but lists {len(live_only)}")

    # stem -> contract asset for the twin: the filed Stage D manifest's venue table
    stem_asset = {v["stem"]: v["asset"] for v in D.load_manifest()["venues"] if v["stem"]}
    unmapped = [a for a in assets if a not in stem_asset]
    if unmapped:
        raise SystemExit(f"HALT: the Stage D venue table maps no contract asset for {unmapped}")

    return {
        "prog": prog, "journal": journal, "t9": t9, "anchors": anchors,
        "panel": panels[0], "n_assets": n_assets[0], "assets": assets,
        "lanes": sorted(set(journal["lane"].astype(str))),
        "tc9_iso": tc9_iso, "tc9_ms": tc9_ms, "t9_rows": len(t9),
        "t9_exit_reasons": {k: int(v) for k, v in
                            sorted(t9["exit_reason"].value_counts().items())},
        "contract_rel": c["path"], "contract_sha": csha, "lit": lit, "lit_line": lit_line,
        "clause_line": clause_line,
        "end_iso": end_iso, "end_ms": end_ms,
        "live_line": live_line, "live_n": live_n, "live_only": live_only,
        "referee_last": referee_last, "stem_asset": stem_asset,
    }


# ═══════════════════════════════════════════════════════════════ the strip
def build_strip(journal: pd.DataFrame, tc9_ms: int, stem_asset: dict) -> pd.DataFrame:
    e = journal["entry_ms"].to_numpy(np.int64)
    x = journal["exit_ms"].to_numpy(np.int64)
    entered = e >= tc9_ms
    cont = (e < tc9_ms) & (tc9_ms <= x)
    keep = entered | cont
    asof = asof_columns(journal)
    s = journal.loc[keep, CARRY + asof].copy()
    win = np.where(entered[keep], ENTERED, CONT)
    is_open = (s["exit_reason"].astype(str) == OPEN_REASON).to_numpy()
    s.insert(0, "label", [f"{w} / {OPEN_TAIL if o else CLOSED_TAIL}" for w, o in zip(win, is_open)])
    s.insert(1, "window", list(win))
    s.insert(2, "tier", TIER)
    s.insert(3, "scored", False)
    tw = [D.haircut_twin_net_r(stem_asset[str(a)], float(g), float(ep), float(xp), float(r))
          for a, g, ep, xp, r in zip(s["asset"], s["gross_r"], s["entry_px"],
                                      s["exit_px"], s["r_dist"])]
    s[TWIN] = [float(t["net_r_twin"]) for t in tw]
    s["haircut_twin_tier"] = [str(t["tier"]) for t in tw]
    s["haircut_twin_charter_round_trip_bps"] = [float(t["charter_round_trip_bps"]) for t in tw]
    s = s[HEAD_COLS + CARRY + TWIN_COLS + asof].copy()
    s["scored"] = s["scored"].astype(bool)
    return s.sort_values(["entry_ms", "asset"], kind="mergesort").reset_index(drop=True)


def render_md(s: pd.DataFrame, ctx: dict) -> str:
    L: list[str] = []
    a = L.append
    n_e = int((s["window"] == ENTERED).sum())
    n_c = int((s["window"] == CONT).sum())
    op = s["exit_reason"].astype(str) == OPEN_REASON
    t9_open = ctx["t9_exit_reasons"].get(OPEN_REASON, 0)
    a("# TIER-C10 · CLOSE · FORWARD STRIP")
    a("")
    a(f"**{TIER}.** TIER-C10 CLOSE item, contract of record `{ctx['contract_rel']}`:"
      f"{ctx['clause_line']}-{ctx['lit_line']}: the 5-asset v6 book from TC9's as-of to this "
      "corridor's end — printed, labelled, never scored. Counts and sums only: no CI, no p, "
      "no verdict, no LOAO, no FDR bar. No registration, score or verdict file was read to "
      "build it, and no kline file: every market number below is a column of the filed journal.")
    a("")
    a("## The two as-ofs, as read from files this run")
    a("")
    a("| as-of | value | read from |")
    a("|---|---|---|")
    a(f"| **TC9's as-of** (strip start) | `{ctx['tc9_iso']}` (ms {ctx['tc9_ms']}) | "
      f"`{TC9_MANIFEST_REL}` field `as_of` **and** `{TC9_JOURNAL_REL}` column "
      f"`as_of_last_closed_4h` ({ctx['t9_rows']} rows, 1 distinct value): equal |")
    a(f"| **this corridor's end** (strip end) | `{ctx['end_iso']}` (last closed 4h bar, close ms "
      f"{ctx['end_ms']}) | `{PROGRESS_REL}` fields `as_of_of_record` and "
      f"`as_of_last_closed_4h_close_ms`: agree with each other and with `{AS_OF_PIN_REL}` |")
    a(f"| contract literal (compared, never used) | `{ctx['lit']}` | `{ctx['contract_rel']}`:"
      f"{ctx['lit_line']} (sha256 `{ctx['contract_sha'][:16]}…` == PROGRESS `contract_of_record`): "
      "equals TC9's as-of |")
    a("")
    a("## Inputs")
    a("")
    a(f"- **The book:** `{JOURNAL_REL}`, sha256 `{ctx['anchors'][JOURNAL_REL]}` == `{PROGRESS_REL}` "
      f"stage `{PANEL_STAGE}` artifact_shas. {len(ctx['journal'])} campaigns, panel "
      f"`{ctx['panel']}`, {ctx['n_assets']} assets ({', '.join(ctx['assets'])}), lane "
      f"{', '.join('`' + x + '`' for x in ctx['lanes'])}.")
    a(f"- **The anchor:** `{PANEL_FIX_REL}` (sha256 `{ctx['anchors'][PANEL_FIX_REL][:16]}…` == the "
      f"`{PANEL_STAGE}` record), line {ctx['live_line']}: F-CTRL/b lists {ctx['live_n']} live-only "
      f"campaign(s) against the filed tierc9 journal, all entered after the referee's last bar "
      f"`{ctx['referee_last']}`.")
    a("")
    a("## Membership")
    a("")
    a(f"- **{ENTERED}**: `entry_ms >= {ctx['tc9_ms']}` ({ctx['tc9_iso']}), {n_e} campaign(s).")
    a(f"- **{CONT}**: `entry_ms < {ctx['tc9_ms']} <= exit_ms`, {n_c} campaign(s). TC9's own "
      f"journal carries {t9_open} `{OPEN_REASON}` row(s) (exit reasons "
      f"{json.dumps(ctx['t9_exit_reasons'], sort_keys=True)}), so "
      + ("no v6 campaign was open at TC9's as-of." if t9_open == 0 else
         f"{t9_open} campaign(s) were open at TC9's as-of."))
    a(f"- **{OPEN}**: exit_reason `{OPEN_REASON}`, marked to the pin, not realized: "
      f"{int(op.sum())} campaign(s).")
    armed_before = np.array([to_ms(str(t)) < ctx["tc9_ms"] for t in s["arm_ts"]], dtype=bool)
    pre = s[armed_before & (s["window"] == ENTERED).to_numpy()]
    for _, r in pre.iterrows():
        a(f"- Note: {r['asset']} {r['direction']} entered {r['entry_ts']} was ARMED {r['arm_ts']}, "
          f"inside TC9's window. It is {ENTERED} by the entry predicate, and it is on F-CTRL/b's "
          "live-only list.")
    a("")
    a(f"## The strip ({TIER})")
    a("")
    a("R columns are verbatim from the journal (shortest round-trip repr). `net_r` is the "
      "TC-series accounting. `twin net_r` is the ADDED haircut twin.")
    a("")
    a("| label | asset | dir | armed | entered | exited | exit_reason | bars | gross_r | fee_r "
      "| funding_r | net_r (TC-series) | twin net_r (ADDED) | twin tier |")
    a("|---|---|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---|")
    for _, r in s.iterrows():
        a(f"| {r['label']} | {r['asset']} | {r['direction']} | {r['arm_ts']} | {r['entry_ts']} | "
          f"{r['exit_ts']} | {r['exit_reason']} | {int(r['bars_held'])} | {fnum(r['gross_r'])} | "
          f"{fnum(r['fee_r'])} | {fnum(r['funding_r'])} | {fnum(r['net_r'])} | {fnum(r[TWIN])} | "
          f"{r['haircut_twin_tier']} |")
    a("")
    a(f"## Footer: counts and sums only ({TIER})")
    a("")
    a("Sums are `math.fsum` over the rows above, printed to 6 dp. The rows are verbatim.")
    a("")
    a("| subset | n | Σ gross_r | Σ fee_r | Σ funding_r | Σ net_r (TC-series) | Σ twin net_r (ADDED) |")
    a("|---|---:|---:|---:|---:|---:|---:|")
    subsets = [("all rows", np.ones(len(s), bool)),
               (f"{ENTERED}", (s["window"] == ENTERED).to_numpy()),
               (f"{CONT}", (s["window"] == CONT).to_numpy()),
               ("CLOSED (realized)", (~op).to_numpy()),
               (f"{OPEN} (marked, not realized)", op.to_numpy())]
    for name, m in subsets:
        sub = s[m]
        a(f"| {name} | {len(sub)} | " + " | ".join(
            f"{math.fsum(float(v) for v in sub[c]):+.6f}" for c in R_COLS + [TWIN]) + " |")
    a("")
    a("| asset | campaigns in strip |")
    a("|---|---:|")
    for asset in ctx["assets"]:
        a(f"| {asset} | {int((s['asset'] == asset).sum())} |")
    a("")
    a("## Notes")
    a("")
    resid = max((abs(float(g) - float(f) - float(fu) - float(n))
                 for g, f, fu, n in zip(s["gross_r"], s["fee_r"], s["funding_r"], s["net_r"])),
                default=0.0)
    six = all(round(float(v), 6) == float(v) for c in R_COLS for v in s[c])
    a(f"- `net_r` is the TC-series row of record, carried verbatim. On these rows "
      f"max |net_r − (gross_r − fee_r − funding_r)| = {resid:.3e}"
      + (". Every R value on these rows is a 6-dp figure, so a residue of up to 1e-6 is "
         "rounding in the journal as filed." if six else "."))
    a("- The haircut twin is `tierc10_data.haircut_twin_net_r(asset, gross_r, entry_px, exit_px, "
      "r_dist)[\"net_r_twin\"]`. It is gross_r less (taker fee + charter slippage per side) × "
      "(entry_px + exit_px) / r_dist, with the stem mapped to the contract asset by the filed "
      "Stage D venue table. The filed function charges NO funding, so twin − net_r is not a pure "
      "slippage delta. It is an ADDED column and gates nothing.")
    a(f"- An {OPEN} row is the journal's own mark at the pinned bar. Its gross_r, fee_r, "
      "funding_r, net_r and twin are not realized.")
    a(f"- Every as_of_* column and `warranty` is carried verbatim from the journal. Every row is "
      f"stamped `as_of_last_closed_4h` = `{ctx['end_iso']}`.")
    a("- This strip is not a verdict. It is a printed window of the control book.")
    return "\n".join(L) + "\n"


def write_outputs(s: pd.DataFrame, ctx: dict, out_dir: Path) -> dict:
    out_dir = out_dir.resolve()
    if out_dir != OUT.resolve() and OUT.resolve() not in out_dir.parents:
        raise SystemExit(f"HALT: output dir {out_dir} is outside {OUT} — this build writes only there")
    out_dir.mkdir(parents=True, exist_ok=True)
    s.to_parquet(out_dir / PARQUET, index=False)
    (out_dir / MD).write_text(render_md(s, ctx), encoding="utf-8")
    return {PARQUET: sha(out_dir / PARQUET), MD: sha(out_dir / MD)}


# ═══════════════════════════════════════════════════════════════ checkers
def _keys(df: pd.DataFrame) -> list[tuple[str, int]]:
    return list(zip(df["asset"].astype(str), (int(x) for x in df["entry_ms"])))


def window_map(s: pd.DataFrame) -> dict:
    return dict(zip(_keys(s), s["window"].astype(str)))


def check_window(s: pd.DataFrame, journal: pd.DataFrame, tc9_ms: int) -> tuple[bool, str]:
    bad: list[str] = []
    jkeys = set(_keys(journal))
    want: dict = {}
    for (a, em), xm in zip(_keys(journal), journal["exit_ms"]):
        if em >= tc9_ms:
            want[(a, em)] = ENTERED
        elif em < tc9_ms <= int(xm):
            want[(a, em)] = CONT
    seen: set = set()
    for (a, em), xm, w in zip(_keys(s), s["exit_ms"], s["window"]):
        xm = int(xm)
        if (a, em) in seen:
            bad.append(f"duplicate strip row {a} {iso(em)}")
        seen.add((a, em))
        if (a, em) not in jkeys:
            bad.append(f"strip row {a} {iso(em)} is not a journal campaign")
        me, mc = em >= tc9_ms, em < tc9_ms <= xm
        if not (me or mc):
            bad.append(f"strip row {a} entry {iso(em)} exit {iso(xm)} fails BOTH predicates")
        elif w != (ENTERED if me else CONT):
            bad.append(f"strip row {a} {iso(em)} labelled {w} but meets {ENTERED if me else CONT}")
    for k in sorted(k for k in want if k not in seen):
        bad.append(f"journal campaign {k[0]} {iso(k[1])} meets {want[k]} but is ABSENT")
    n_e = sum(1 for v in want.values() if v == ENTERED)
    head = (f"{len(s)} strip row(s) vs {len(want)} journal row(s) meeting a predicate at "
            f"tc9 as-of {iso(tc9_ms)} ({n_e} {ENTERED}, {len(want) - n_e} {CONT})")
    return (not bad), head + ("" if not bad else " — " + "; ".join(bad[:4]))


def check_tc9_open(s: pd.DataFrame, t9: pd.DataFrame) -> tuple[bool, str]:
    open9 = sorted(k for k, r in zip(_keys(t9), t9["exit_reason"].astype(str)) if r == OPEN_REASON)
    cont = sorted(k for k, w in zip(_keys(s), s["window"].astype(str)) if w == CONT)
    ok = open9 == cont
    return ok, (f"TC9's journal {OPEN_REASON} rows {[(a, iso(m)) for a, m in open9]} == the strip's "
                f"{CONT} rows {[(a, iso(m)) for a, m in cont]}: {ok}")


def check_anchor(s: pd.DataFrame, live_only: list, referee_last: str, tc9_ms: int) -> tuple[bool, str]:
    ent = sorted((str(a), str(t)) for a, t, w in zip(s["asset"], s["entry_ts"], s["window"])
                 if w == ENTERED)
    ok_set = ent == sorted(live_only)          # a MULTISET comparison: a duplicate is caught
    ok_bar = to_ms(referee_last) + STEP_MS == tc9_ms
    miss = sorted(set(live_only) - set(ent))
    extra = sorted(set(ent) - set(live_only))
    return (ok_set and ok_bar), (
        f"{ENTERED} (asset, entry_ts) x{len(ent)} vs F-CTRL/b live-only x{len(live_only)}: "
        f"equal as multisets {ok_set} (missing {miss}, extra {extra}); referee's last bar "
        f"{referee_last} + one 4h bar == TC9's as-of {iso(tc9_ms)}: {ok_bar}")


def check_verbatim(s: pd.DataFrame, journal: pd.DataFrame) -> tuple[bool, str]:
    cols = CARRY + asof_columns(journal)
    bad: list[str] = []
    for c in cols:
        if c not in s.columns:
            bad.append(f"carried column {c} missing")
        elif s[c].dtype != journal[c].dtype:
            bad.append(f"{c} dtype {s[c].dtype} != journal {journal[c].dtype}")
    if bad:
        return False, "; ".join(bad[:4])
    jpos = {k: i for i, k in enumerate(_keys(journal))}
    worst = 0.0
    for i, k in enumerate(_keys(s)):
        if k not in jpos:
            bad.append(f"strip row {k[0]} {iso(k[1])} is not a journal campaign")
            continue
        j = jpos[k]
        for c in cols:
            x, y = s[c].iat[i], journal[c].iat[j]
            if pd.api.types.is_float_dtype(journal[c].dtype):
                x, y = float(x), float(y)
                same = (x == y) or (math.isnan(x) and math.isnan(y))
                if not same:
                    worst = max(worst, abs(x - y)) if not (math.isnan(x) or math.isnan(y)) else math.inf
            else:
                same = bool(x == y)
            if not same:
                bad.append(f"{k[0]} {iso(k[1])} {c}: strip {x!r} vs journal {y!r}")
    head = (f"{len(s)} row(s) x {len(cols)} carried column(s) (R columns {R_COLS}); "
            f"worst abs diff {worst:.3e} (bar: EXACTLY 0)")
    return (not bad), head + ("" if not bad else " — " + "; ".join(bad[:3]))


def check_asof(s: pd.DataFrame, as_of_record: str, close_ms: int) -> tuple[bool, str]:
    bad: list[str] = []
    for (a, em), stamp, xm in zip(_keys(s), s["as_of_last_closed_4h"].astype(str), s["exit_ms"]):
        xm = int(xm)
        if stamp != as_of_record:
            bad.append(f"{a} {iso(em)} stamped {stamp} != as_of_of_record {as_of_record}")
        if xm > close_ms:
            bad.append(f"{a} {iso(em)} exit_ms {iso(xm)} > the pin's close {iso(close_ms)}")
        elif xm + STEP_MS > close_ms:
            bad.append(f"{a} {iso(em)} exit bar {iso(xm)} closes {iso(xm + STEP_MS)}, after the pin")
    last = max((int(x) for x in s["exit_ms"]), default=None)
    head = (f"{len(s)} row(s) stamped vs {as_of_record}; latest exit bar "
            f"{iso(last) if last is not None else None} (+4h = "
            f"{iso(last + STEP_MS) if last is not None else None}) vs pin close {iso(close_ms)}")
    return (not bad), head + ("" if not bad else " — " + "; ".join(bad[:3]))


def check_twin(s: pd.DataFrame, journal: pd.DataFrame, stem_asset: dict) -> tuple[bool, str]:
    if TWIN not in s.columns:
        return False, f"the twin column {TWIN} is missing"
    if "net_r" not in s.columns:
        return False, "net_r is missing"
    jpos = {k: i for i, k in enumerate(_keys(journal))}
    bad: list[str] = []
    for i, k in enumerate(_keys(s)):
        tw = s[TWIN].iat[i]
        if tw is None or not np.isfinite(float(tw)):
            bad.append(f"{k[0]} {iso(k[1])}: twin missing ({tw!r})")
            continue
        if k not in jpos:
            bad.append(f"{k[0]} {iso(k[1])} not in the journal")
            continue
        j = jpos[k]
        want = D.haircut_twin_net_r(stem_asset[k[0]], float(journal["gross_r"].iat[j]),
                                    float(journal["entry_px"].iat[j]),
                                    float(journal["exit_px"].iat[j]),
                                    float(journal["r_dist"].iat[j]))["net_r_twin"]
        if float(tw) != float(want):
            bad.append(f"{k[0]} {iso(k[1])}: twin {float(tw)!r} != recomputed {float(want)!r}")
        nr, jn = float(s["net_r"].iat[i]), float(journal["net_r"].iat[j])
        if nr != jn:
            bad.append(f"{k[0]} {iso(k[1])}: net_r {nr!r} is not the journal's {jn!r}"
                       + (" (the twin was written over it)" if nr == float(tw) else ""))
    head = (f"{len(s)} row(s): twin present, finite and == tierc10_data.haircut_twin_net_r "
            "recomputed from the JOURNAL's gross_r/entry_px/exit_px/r_dist; net_r == the journal's")
    return (not bad), head + ("" if not bad else " — " + "; ".join(bad[:3]))


def check_noscore(s: pd.DataFrame, before: dict, after: dict) -> tuple[bool, str]:
    bad: list[str] = []
    forb = [c for c in s.columns if FORBIDDEN_COL.match(str(c))]
    if forb:
        bad.append(f"scoring column(s) present: {forb}")
    if "scored" not in s.columns:
        bad.append("no 'scored' column")
    else:
        if s["scored"].dtype != bool:
            bad.append(f"'scored' dtype {s['scored'].dtype} is not bool")
        n_true = int(np.asarray(s["scored"], dtype=bool).sum())
        if n_true:
            bad.append(f"{n_true} row(s) scored=True")
    if "tier" not in s.columns or not (s["tier"].astype(str) == TIER).all():
        bad.append(f"'tier' is not '{TIER}' on every row")
    moved = sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k))
    if moved:
        bad.append(f"{len(moved)} protected file(s) changed bytes: {moved[:3]}")
    n_sc = int(np.asarray(s["scored"], dtype=bool).sum()) if "scored" in s.columns else None
    head = (f"{len(s.columns)} column(s), {len(forb)} scoring-shaped, scored=True rows {n_sc}; "
            f"{len(before)} protected file(s) re-hashed ({sum(1 for k in before if k.startswith('research_outputs/tierc10/scores/'))} "
            f"under scores/, {sum(1 for k in before if k.startswith('research_outputs/tierc10/registrations/'))} "
            f"under registrations/): {len(moved)} moved")
    return (not bad), head + ("" if not bad else " — " + "; ".join(bad[:3]))


def check_closure(src: str, modules: set) -> tuple[bool, str]:
    bad: list[str] = []
    for node in ast.walk(ast.parse(src)):
        if isinstance(node, ast.Call):
            f = node.func
            name = f.attr if isinstance(f, ast.Attribute) else f.id if isinstance(f, ast.Name) else None
            if name in BANNED_CALLS:
                bad.append(f"line {node.lineno}: calls {name}()")
        elif isinstance(node, ast.Import):
            for al in node.names:
                if al.name.split(".")[0] in BANNED_MODULES:
                    bad.append(f"line {node.lineno}: imports {al.name}")
        elif isinstance(node, ast.ImportFrom):
            if (node.module or "").split(".")[0] in BANNED_MODULES:
                bad.append(f"line {node.lineno}: imports from {node.module}")
    loaded = sorted(m for m in BANNED_MODULES if m in modules)
    if loaded:
        bad.append(f"loaded at run time: {loaded}")
    head = (f"AST: no call named {sorted(BANNED_CALLS)}, no import of {sorted(BANNED_MODULES)}; "
            f"sys.modules holds none of them")
    return (not bad), head + ("" if not bad else " — " + "; ".join(bad[:3]))


def compare_bytes(a: dict, b: dict, what: str) -> tuple[bool, str]:
    diff = sorted(k for k in set(a) | set(b) if a.get(k) != b.get(k))
    shas = ", ".join(f"{k} {hashlib.sha256(a[k]).hexdigest()[:16]}" for k in sorted(a) if k in a)
    return (not diff), f"{what}: {shas}" + ("" if not diff else f" — DIFFER: {diff}")


# ═══════════════════════════════════════════════════════════════ leg runner
RESULTS: dict[str, bool] = {}
BREAK_TALLY = [0, 0]      # [red, total]


def _run(fn):
    try:
        return fn()
    except SystemExit as e:
        return False, f"HALT raised: {str(e)[:160]}"
    except Exception as e:                                           # noqa: BLE001
        return False, f"raised {type(e).__name__}: {str(e)[:160]}"


def leg(name: str, title: str, fails_if: str, real: list, breaks: list, notes: list = ()) -> None:
    """real: [(desc, fn -> (ok, detail))]; breaks: [(desc, fn -> (ok, detail))] — a
    break is RED (correct) iff its checker returns ok=False on the sabotaged copy."""
    say(f"--- {name} — {title}")
    good = True
    for desc, fn in breaks:
        ok, detail = _run(fn)
        BREAK_TALLY[1] += 1
        if not ok:
            BREAK_TALLY[0] += 1
            say(f"  [BREAK] {desc} -> RED (correct): {detail}")
        else:
            good = False
            say(f"  [BREAK] {desc} -> GREEN (WRONG: the leg is blind to it): {detail}")
    for desc, fn in real:
        ok, detail = _run(fn)
        good &= bool(ok)
        say(f"    [{'OK ' if ok else 'BAD'}] {desc}: {detail}")
    for n in notes:
        say(f"    [NB ] {n}")
    say(f"      FAILS IF: {fails_if}")
    say(f"  [{'PASS' if good else 'FAIL'}] {name}")
    say()
    RESULTS[name] = good


# ═══════════════════════════════════════════════════════════════ legs
def leg_substrate() -> None:
    probe = DET_ROOT / "_halt_probe"

    def sub(env_val):
        env = {k: v for k, v in os.environ.items() if k != "NAIAD_CACHE_DIR"}
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        if env_val is not None:
            env["NAIAD_CACHE_DIR"] = env_val
        r = subprocess.run([sys.executable, str(Path(__file__).resolve()), "--out", str(probe)],
                           env=env, capture_output=True, text=True, cwd=str(ROOT))
        msg = (r.stderr.strip().splitlines() or [""])[-1]
        halted = r.returncode != 0 and msg.startswith("HALT") and not probe.exists()
        return (not halted), f"exit {r.returncode}, wrote nothing: {not probe.exists()}, '{msg[:110]}'"

    def live():
        try:
            guard_substrate(str(LIVE_CACHE))
        except SystemExit as e:
            return False, f"'{str(e)[:110]}' (decided on the path string; the live cache is not stat'ed)"
        return True, "the guard ACCEPTED the live cache"

    leg("F-FS-SUBSTRATE", "the run HALTs off the frozen snapshot, before it writes anything",
        "the script proceeds (or writes a byte) with NAIAD_CACHE_DIR unset, naming the live cache, "
        "or naming any path but the TC10 snapshot.",
        real=[("this process", lambda: (True, f"NAIAD_CACHE_DIR resolves to {SNAPSHOT}"))],
        breaks=[("a subprocess with NAIAD_CACHE_DIR unset", lambda: sub(None)),
                ("a subprocess with NAIAD_CACHE_DIR at a non-snapshot path",
                 lambda: sub(str(OUT / "_not_a_snapshot"))),
                ("the guard handed the live cache path", live)])


def leg_window(s: pd.DataFrame, ctx: dict) -> None:
    J, t9, tc9, sa = ctx["journal"], ctx["t9"], ctx["tc9_ms"], ctx["stem_asset"]

    def boundary_copy(entry_ms: int, exit_ms: int) -> pd.DataFrame:
        j = J.copy(deep=True)
        i = j[j["entry_ms"] >= tc9].sort_values(["entry_ms", "asset"], kind="mergesort").index[0]
        j.loc[i, ["entry_ms", "exit_ms"]] = [entry_ms, exit_ms]
        j.loc[i, ["entry_ts", "exit_ts"]] = [iso(entry_ms), iso(exit_ms)]
        return j

    def shift(delta: int, entry_ms: int, exit_ms: int, what: str):
        def fn():
            jc = boundary_copy(entry_ms, exit_ms)
            true_m = window_map(build_strip(jc, tc9, sa))
            shifted = build_strip(jc, tc9 + delta, sa)
            changed = window_map(shifted) != true_m
            ok, d = check_window(shifted, jc, tc9)
            if not changed:
                return True, f"VOID: the shift did not change membership on the copy ({what})"
            return ok, f"[{what}; membership changed: {changed}] {d}"
        return fn

    def outside_row():
        before = J[J["exit_ms"] < tc9].sort_values(["exit_ms", "asset"], kind="mergesort").iloc[-1]
        k = (str(before["asset"]), int(before["entry_ms"]))
        planted = build_strip(J, int(before["entry_ms"]), sa)
        planted = planted[[kk == k for kk in _keys(planted)]]
        bad = pd.concat([s, planted], ignore_index=True)
        return check_window(bad, J, tc9)

    def t9_relabel():
        t = t9.copy(deep=True)
        i = t.sort_values(["exit_ms", "asset"], kind="mergesort").index[-1]
        t.loc[i, "exit_reason"] = OPEN_REASON
        return check_tc9_open(s, t)

    # the boundary is NOT stressed by the untouched data — measured and printed
    e = J["entry_ms"].to_numpy(np.int64)
    x = J["exit_ms"].to_numpy(np.int64)
    first_in = int(e[e >= tc9].min())
    last_out = int(x[x < tc9].max())
    real_m = window_map(s)
    same_p = window_map(build_strip(J, tc9 + STEP_MS, sa)) == real_m
    same_m = window_map(build_strip(J, tc9 - STEP_MS, sa)) == real_m
    notes = [f"on the UNTOUCHED journal a one-bar shift leaves membership unchanged (+1 bar: "
             f"{same_p}, -1 bar: {same_m}). The first entry at or after TC9's as-of is "
             f"{iso(first_in)} ({(first_in - tc9) // STEP_MS} bars after it), and the latest exit "
             f"before it is {iso(last_out)} ({(tc9 - last_out) // STEP_MS} bars before it). The data "
             "does not stress the boundary, so each shift sabotage PLANTS one boundary campaign "
             "(the earliest ENTERED row, restamped) in a COPY. The shift must change membership "
             "there, or the break is VOID."]
    leg("F-FS-WINDOW", "membership is exactly ENTERED (entry_ms >= tc9) + CONTINUATION "
        "(entry_ms < tc9 <= exit_ms)",
        "a strip row fails both predicates, carries a window label for a predicate it does not "
        "meet, or is duplicated; or a journal row meeting either predicate is absent; or TC9's own "
        f"'{OPEN_REASON}' rows (the campaigns TC9 saw open at its as-of) are not exactly the "
        f"{CONT} rows.",
        real=[("the strip vs the journal at TC9's as-of", lambda: check_window(s, J, tc9)),
              ("cross-process: TC9's journal vs the CONTINUATION set", lambda: check_tc9_open(s, t9))],
        breaks=[("tc9_asof shifted +1 4h bar in a copy (planted campaign entered AND stopped in "
                 "the first bar after TC9's as-of)", shift(+STEP_MS, tc9, tc9, "planted entry=exit="
                                                          + iso(tc9))),
                ("tc9_asof shifted -1 4h bar in a copy (planted campaign entered AND stopped in "
                 "the referee's last bar)", shift(-STEP_MS, tc9 - STEP_MS, tc9 - STEP_MS,
                                                   "planted entry=exit=" + iso(tc9 - STEP_MS))),
                ("the journal's latest pre-as-of campaign planted into a copy of the strip",
                 outside_row),
                ("a copy of TC9's journal with its last campaign relabelled corridor_end",
                 t9_relabel)],
        notes=notes)


def leg_anchor(s: pd.DataFrame, ctx: dict) -> None:
    lo, rl, tc9 = ctx["live_only"], ctx["referee_last"], ctx["tc9_ms"]

    def drop():
        i = s.index[s["window"] == ENTERED][0]
        return check_anchor(s.drop(index=i), lo, rl, tc9)

    def dup():
        i = s.index[s["window"] == ENTERED][-1]
        return check_anchor(pd.concat([s, s.loc[[i]]], ignore_index=True), lo, rl, tc9)

    def bar():
        return check_anchor(s, lo, iso(to_ms(rl) + STEP_MS), tc9)

    leg("F-FS-ANCHOR", "the ENTERED set is F-CTRL/b's live-only list, parsed from the filed transcript",
        f"the {ENTERED} (asset, entry_ts) multiset differs from the list on {PANEL_FIX_REL}:"
        f"{ctx['live_line']}, or that line's referee's last bar + one 4h bar is not TC9's as-of.",
        real=[(f"{PANEL_FIX_REL}:{ctx['live_line']} ({ctx['live_n']} listed)",
               lambda: check_anchor(s, lo, rl, tc9))],
        breaks=[("one ENTERED row dropped from a copy", drop),
                ("one ENTERED row duplicated in a copy", dup),
                ("the referee's last bar moved one 4h bar in a copy of the parsed line", bar)])


def leg_verbatim(s: pd.DataFrame, ctx: dict) -> None:
    J = ctx["journal"]

    def plus(col: str, eps: float):
        def fn():
            b = s.copy(deep=True)
            b.loc[b.index[-1], col] = float(b.loc[b.index[-1], col]) + eps
            return check_verbatim(b, J)
        return fn

    def relabel():
        b = s.copy(deep=True)
        b.loc[b.index[0], "exit_reason"] = "bell_12_89"
        return check_verbatim(b, J)

    leg("F-FS-VERBATIM", "every carried column is the journal's, read back from the written parquet",
        "any of gross_r/fee_r/funding_r/net_r (or any other carried column: stamps, prices, "
        "exit_reason, bars_held, the as_of_* warranty columns) differs from the journal by ANY "
        "amount or dtype.",
        real=[(f"{OUT.relative_to(ROOT)}/{PARQUET} vs {JOURNAL_REL}", lambda: check_verbatim(s, J))],
        breaks=[("+1e-9 on one net_r in a copy", plus("net_r", 1e-9)),
                ("+1e-12 on one funding_r in a copy", plus("funding_r", 1e-12)),
                ("one exit_reason relabelled in a copy", relabel)])


def leg_asof(s: pd.DataFrame, ctx: dict) -> None:
    rec, cms = ctx["prog"]["as_of_of_record"], int(ctx["prog"]["as_of_last_closed_4h_close_ms"])

    def restamp():
        b = s.copy(deep=True)
        b.loc[b.index[0], "as_of_last_closed_4h"] = ctx["tc9_iso"]
        return check_asof(b, rec, cms)

    def late(ms: int):
        def fn():
            b = s.copy(deep=True)
            b.loc[b.index[-1], "exit_ms"] = ms
            return check_asof(b, rec, cms)
        return fn

    leg("F-FS-ASOF", "every row is stamped the corridor of record, and nothing exits past the pin",
        f"any row's as_of_last_closed_4h != {PROGRESS_REL} as_of_of_record, or any exit_ms > "
        "as_of_last_closed_4h_close_ms, or (stricter) any exit bar closes after the pin "
        "(exit_ms + 4h > close_ms).",
        real=[(f"vs {PROGRESS_REL} ({rec}, close ms {cms})", lambda: check_asof(s, rec, cms))],
        breaks=[("one row restamped to TC9's as-of in a copy", restamp),
                ("one exit_ms moved one bar PAST the pin's close in a copy", late(cms + STEP_MS)),
                ("one exit_ms moved to the pin's close (a bar the pin has not closed) in a copy",
                 late(cms))])


def leg_twin(s: pd.DataFrame, ctx: dict) -> None:
    J, sa = ctx["journal"], ctx["stem_asset"]

    def over():
        b = s.copy(deep=True)
        b["net_r"] = b[TWIN]
        return check_twin(b, J, sa)

    def nan_one():
        b = s.copy(deep=True)
        b.loc[b.index[0], TWIN] = np.nan
        return check_twin(b, J, sa)

    leg("F-FS-TWIN", "the haircut twin is an ADDED column on every row; net_r is untouched",
        f"{TWIN} is missing or non-finite on any row, differs from tierc10_data.haircut_twin_net_r "
        "recomputed from the journal's own columns, or net_r is not the journal's (the twin "
        "written over it).",
        real=[("the written parquet", lambda: check_twin(s, J, sa))],
        breaks=[("net_r overwritten with the twin in a copy", over),
                ("the twin NaN on one row of a copy", nan_one),
                ("the twin column dropped from a copy", lambda: check_twin(s.drop(columns=[TWIN]), J, sa))])


def leg_closure() -> None:
    src = Path(__file__).read_text()

    def inject():
        return check_closure(src + "\nimport tierc2_baseline\ntierc2_baseline.load_klines('BTCUSDT', '5m')\n",
                             set(sys.modules))

    leg("F-FS-CLOSURE", "no bar loader, no scorer, no registry is reachable from this file",
        f"this file's AST calls anything named {sorted(BANNED_CALLS)} or imports "
        f"{sorted(BANNED_MODULES)}, or any of those modules is loaded in this process.",
        real=[("this file + sys.modules", lambda: check_closure(src, set(sys.modules)))],
        breaks=[("tierc2_baseline.load_klines injected into a copy of the source", inject),
                ("tierc10_panel planted in a copy of sys.modules",
                 lambda: check_closure(src, set(sys.modules) | {"tierc10_panel"}))],
        notes=["this build reads NO kline file: every market number is a column of the filed "
               "journal. tierc10_data.load_asof is not reached, and neither is "
               "tierc2_baseline.load_klines."])


def leg_det(canon: dict) -> None:
    runs: dict = {}
    for seed in DET_SEEDS:
        d = DET_ROOT / f"seed_{seed}"
        env = dict(os.environ, PYTHONHASHSEED=str(seed), NAIAD_CACHE_DIR=str(SNAPSHOT),
                   PYTHONDONTWRITEBYTECODE="1")
        r = subprocess.run([sys.executable, str(Path(__file__).resolve()), "--out", str(d)],
                           env=env, capture_output=True, text=True, cwd=str(ROOT))
        runs[seed] = {"rc": r.returncode,
                      "bytes": {n: (d / n).read_bytes() for n in (PARQUET, MD) if (d / n).exists()},
                      "err": (r.stderr.strip().splitlines() or [""])[-1][:120]}
    a, b = (runs[k] for k in DET_SEEDS)

    def rcs():
        ok = all(runs[k]["rc"] == 0 and len(runs[k]["bytes"]) == 2 for k in DET_SEEDS)
        return ok, "; ".join(f"PYTHONHASHSEED={k} exit {runs[k]['rc']} wrote "
                             f"{sorted(runs[k]['bytes'])} {runs[k]['err'] if runs[k]['rc'] else ''}".rstrip()
                             for k in DET_SEEDS)

    def flip(name: str):
        def fn():
            bad = dict(b["bytes"])
            bb = bytearray(bad[name])
            bb[len(bb) // 2] ^= 0x01
            bad[name] = bytes(bb)
            return compare_bytes(a["bytes"], bad, f"seed {DET_SEEDS[0]} vs a byte-flipped copy of seed {DET_SEEDS[1]}")
        return fn

    leg("F-DET", "two subprocess runs, different PYTHONHASHSEED, byte-identical parquet and md",
        f"the runs under PYTHONHASHSEED {DET_SEEDS[0]} and {DET_SEEDS[1]} (written to "
        f"{DET_ROOT.relative_to(ROOT)}/seed_*/) differ by one byte in {PARQUET} or {MD}, from each "
        "other or from the canonical outputs, or either run fails.",
        real=[("both subprocess runs", rcs),
              (f"seed {DET_SEEDS[0]} vs seed {DET_SEEDS[1]}",
               lambda: compare_bytes(a["bytes"], b["bytes"], "twin runs")),
              ("seed runs vs the canonical outputs",
               lambda: compare_bytes(canon, a["bytes"], "canonical vs seed " + str(DET_SEEDS[0])))],
        breaks=[(f"one byte flipped in a copy of the {MD}", flip(MD)),
                (f"one byte flipped in a copy of the {PARQUET}", flip(PARQUET))])


def leg_noscore(s: pd.DataFrame, before: dict, contract_rel: str) -> None:
    after = bytes_snapshot(contract_rel)

    def add(col, val):
        def fn():
            b = s.copy(deep=True)
            b[col] = val
            return check_noscore(b, before, after)
        return fn

    def scored_true():
        b = s.copy(deep=True)
        b.loc[b.index[0], "scored"] = True
        return check_noscore(b, before, after)

    def moved():
        k = sorted(x for x in after if x.startswith("research_outputs/tierc10/scores/"))[0]
        return check_noscore(s, before, {**after, k: "0" * 64})

    leg("F-FS-NOSCORE", "nothing here is scored, and not one protected byte moved",
        "any verdict / ci_* / p_one_sided / clears_bh_bar / loao_* column exists, or a scored=True "
        "row, or a tier other than the report-only label; or any file under scores/ or "
        "registrations/, REGISTRY*, PROGRESS.json, FIXTURES_RESUME.txt or an input changes bytes "
        "between the start of this run and now (after F-DET's subprocesses).",
        real=[("the written parquet + the protected set", lambda: check_noscore(s, before, after))],
        breaks=[("a 'verdict' column added to a copy", add("verdict", "SUPPORTED")),
                ("a 'ci_lo' column added to a copy", add("ci_lo", 0.0)),
                ("one row scored=True in a copy", scored_true),
                ("a scores/ file's sha changed in a copy of the after-snapshot", moved)])


# ═══════════════════════════════════════════════════════════════ main
def describe(ctx: dict, s: pd.DataFrame, shas: dict, out_dir: Path) -> None:
    say(f"TC9 as-of    : {ctx['tc9_iso']}  ({TC9_MANIFEST_REL} .as_of == {TC9_JOURNAL_REL} "
        f"as_of_last_closed_4h, {ctx['t9_rows']} rows)")
    say(f"contract lit : {ctx['lit']}  ({ctx['contract_rel']}:{ctx['lit_line']}, sha "
        f"{ctx['contract_sha'][:16]}) — compared, equal, not used")
    say(f"corridor end : {ctx['end_iso']}  ({PROGRESS_REL} as_of_of_record; close ms {ctx['end_ms']})")
    say(f"book         : {JOURNAL_REL} sha {ctx['anchors'][JOURNAL_REL]} == PROGRESS '{PANEL_STAGE}'; "
        f"{len(ctx['journal'])} campaigns, {ctx['panel']} {ctx['assets']}, lane {ctx['lanes']}")
    say(f"anchor       : {PANEL_FIX_REL}:{ctx['live_line']} (sha {ctx['anchors'][PANEL_FIX_REL][:16]} "
        f"== PROGRESS) — {ctx['live_n']} live-only {ctx['live_only']}, referee's last bar "
        f"{ctx['referee_last']}")
    say(f"strip        : {len(s)} row(s) — {int((s['window'] == ENTERED).sum())} {ENTERED}, "
        f"{int((s['window'] == CONT).sum())} {CONT}, "
        f"{int((s['exit_reason'] == OPEN_REASON).sum())} {OPEN}")
    for _, r in s.iterrows():
        say(f"  {r['label']} | {r['asset']} {r['direction']} armed {r['arm_ts']} entry {r['entry_ts']} "
            f"exit {r['exit_ts']} {r['exit_reason']} bars {int(r['bars_held'])} | gross {fnum(r['gross_r'])} "
            f"fee {fnum(r['fee_r'])} funding {fnum(r['funding_r'])} net {fnum(r['net_r'])} | "
            f"twin {fnum(r[TWIN])} ({r['haircut_twin_tier']})")
    say(f"sum net_r {math.fsum(float(v) for v in s['net_r']):+.6f} (TC-series) · sum twin "
        f"{math.fsum(float(v) for v in s[TWIN]):+.6f} (ADDED) — {TIER}")
    rel = out_dir.resolve().relative_to(ROOT)
    for n in (PARQUET, MD):
        say(f"wrote {rel}/{n}  sha256 {shas[n]}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--fixtures", action="store_true", help="build, then run every fixture leg")
    ap.add_argument("--out", default=None, help="output dir (must sit under research_outputs/tierc10/close/)")
    args = ap.parse_args()
    if args.fixtures and args.out:
        raise SystemExit("HALT: --fixtures writes the canonical outputs; --out is for F-DET's twins")
    out_dir = Path(args.out) if args.out else OUT

    prog0 = json.loads(PROGRESS.read_text())
    contract_rel = prog0["contract_of_record"]["path"]
    before = bytes_snapshot(contract_rel)

    ctx = read_inputs()
    s = build_strip(ctx["journal"], ctx["tc9_ms"], ctx["stem_asset"])
    shas = write_outputs(s, ctx, out_dir)

    say(f"as_of_last_closed_4h: {ctx['end_iso']}")
    say("=" * 78)
    say(f"TIER-C10 CLOSE · FORWARD STRIP TRANSCRIPT · {TIER}")
    say("=" * 78)
    say(f"substrate {SNAPSHOT.name} · seed {SEED} · no kline read · no registration/score read")
    describe(ctx, s, shas, out_dir)
    say()

    if not args.fixtures:
        after = bytes_snapshot(contract_rel)
        moved = sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k))
        if moved:
            raise SystemExit(f"HALT: protected file(s) changed bytes during the build: {moved}")
        return 0

    # the legs judge the ARTIFACT OF RECORD: the parquet as written, read back
    sw = pd.read_parquet(OUT / PARQUET)
    canon = {n: (OUT / n).read_bytes() for n in (PARQUET, MD)}
    say("FIXTURE LEGS — judged on the parquet read back from disk; every sabotage on a COPY")
    say()
    leg_substrate()
    leg_window(sw, ctx)
    leg_anchor(sw, ctx)
    leg_verbatim(sw, ctx)
    leg_asof(sw, ctx)
    leg_twin(sw, ctx)
    leg_closure()
    leg_det(canon)
    leg_noscore(sw, before, contract_rel)

    n_pass = sum(RESULTS.values())
    say(f"FIXTURE SUMMARY  {n_pass}/{len(RESULTS)} PASS  {json.dumps(RESULTS)}")
    say(f"BREAK LEGS  {BREAK_TALLY[0]}/{BREAK_TALLY[1]} RED-as-required")
    say(f"{TIER}")
    (OUT / TRANSCRIPT).write_text("\n".join(LINES) + "\n", encoding="utf-8")
    print(f"transcript {OUT.relative_to(ROOT)}/{TRANSCRIPT}  sha256 {sha(OUT / TRANSCRIPT)}")
    return 0 if n_pass == len(RESULTS) and BREAK_TALLY[0] == BREAK_TALLY[1] else 1


if __name__ == "__main__":
    sys.exit(main())
