#!/usr/bin/env python
"""TIER-C10 · CLOSE — P-TRG-2 · THE SEEN SHARE.  REPORT-ONLY — TIER-E — NEVER SCORED.

WHY THIS EXISTS
  The build draft's selection-hazard figure for P-TRG-2 (how much of the
  scored book TIER-C9's grid had already seen) rested on a session-scratchpad
  re-ride that no fixture guarded.  This builder persists that re-ride under
  research_outputs/tierc10/close/, with the per-campaign entry list, the book
  sha, the pre/post-as-of counts and net sums, and fixture legs that each
  state their failure condition and carry a sabotage that must go RED.

WHAT IT DOES (read-only; counts and sums only — no CI, no p, no verdict)
  1 Rides P-TRG-2's SCORED arm ('trg-9/12 vs card v6 · CLASSIC5 · full') to
    its Book through its registration's own door, exactly as the pinned
    dry-run does (tierc10_score.ride_arm, kind run_cell_n): TP.run_cell_n with
    the filed text and the registry head of record.  TP.score,
    TP.finish_family, TP.register and TP._mark_scored are never referenced.
  2 HALTs unless the ridden book's sha equals BOTH the dry-run pin
    (scores/DRYRUN.json, the P-TRG-2 scored arm's book_sha) AND the scored
    row's book_sha256 (scores/P-TRG-2.rows.json rows[0].score_row).
  3 Splits the book at TIER-C9's as-of, read from
    research_outputs/tierc9/build_manifest.json .as_of and HALTed unless equal
    to the grid row's as_of_last_closed_4h:
      AT-OR-BEFORE  entry_ms <= as-of      (TC9's corridor could hold it)
      AFTER         entry_ms >  as-of      (the unseen month)
      OPEN-ACROSS   entry_ms <= as-of < exit_ms
  4 Holds the AT-OR-BEFORE part against TIER-C9's filed grid row for
    trigger-9/12 (research_outputs/tierc9/sweep_grid.parquet) on n, net_r,
    gross_r, fee_r, funding_r, best_r and win_rate_pct at the grid's own
    4-dp precision, and on the key overlap with TIER-C9's FILED v6 journal
    (research_outputs/tierc9/trade_journal_control.parquet): shared /
    cell-only / base-only == the grid's n_shared / n_cell_only / n_base_only.
    TIER-C9 filed NO per-campaign trigger-9/12 journal (the builder lists the
    tierc9 journals it finds), so a key-for-key match against a TC9 9/12 book
    is NOT possible; the claim is worded accordingly.
  5 Holds the v6 base the same way: this corridor's control journal
    (panel/control_journal.parquet, sha-anchored to PROGRESS 'PANEL/gate')
    at or before the as-of against TC9's filed v6 journal, campaign by
    campaign; every net_r difference must be carried by funding_r alone with
    gross_r and fee_r exact (F-CTRL/b's attribution, re-derived here).

OUTPUTS (only under research_outputs/tierc10/close/)
  P_TRG_2_SEEN_SHARE.json · P_TRG_2_SEEN_SHARE.md ·
  FIXTURES_CLOSE_p_trg_2_seen_share.txt (--fixtures) ·
  _det_p_trg_2_seen_share/seed_{1,20260921}/ (F-DET's twin runs)

FIXTURE LEGS (--fixtures)
  F-SS-SUBSTRATE  FAILS IF the guard accepts an unset, live-cache or foreign
                  NAIAD_CACHE_DIR.
  F-SS-BOOK       FAILS IF the ridden book's sha differs from the dry-run pin
                  or the scored row's book_sha256.  Sabotage: one net_r bent
                  1e-9 in a copy.
  F-SS-SPLIT      FAILS IF a campaign sits on the wrong side of the as-of,
                  on both sides, or on neither.  Sabotage: one AFTER campaign
                  relabelled AT-OR-BEFORE; the as-of read one 4h bar early.
  F-SS-GRID       FAILS IF the AT-OR-BEFORE part differs from TC9's grid row
                  on any of the 7 fields.  Sabotage: one campaign dropped;
                  net_r bent +1e-4; the as-of one 4h bar early.
  F-SS-KEYS       FAILS IF the key overlap with TC9's filed v6 journal differs
                  from the grid's shared / cell-only / base-only.  Sabotage:
                  one book key's entry moved one 4h bar.
  F-SS-V6         FAILS IF a v6 campaign is on one side only, or a net_r
                  difference is not carried by funding_r alone (gross_r and
                  fee_r exact), or the attributed set differs from F-CTRL/b's
                  [NB] line.  Sabotage: a TC9 gross_r bent 1e-6 in a copy.
  F-SS-CLOSURE    FAILS IF this module references score / finish_family /
                  register / _mark_scored.  Sabotage: a planted TP.score call.
  F-SS-NOWRITE    FAILS IF one byte of scores/, registrations/, REGISTRY*,
                  PROGRESS.json, FIXTURES_RESUME.txt or an input moves during
                  the run, or an output path leaves close/.  Sabotage: an
                  output path under exchange/status/.
  F-DET           FAILS IF two subprocess builds (PYTHONHASHSEED 1, 20260921)
                  differ from each other or from the files written here.

Run:  export NAIAD_CACHE_DIR=/Users/luis/.cache/naiad/snapshots/tc10_20260921 PYTHONDONTWRITEBYTECODE=1
      ~/venvs/naiad/bin/python scripts/tierc10_close_p_trg_2_seen_share.py [--fixtures]
Exit: 0 built (and with --fixtures every leg GREEN) · 1 HALT or a RED leg.
"""
from __future__ import annotations

import argparse
import ast
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
    """HALTS IF NAIAD_CACHE_DIR is unset, names the live cache, or is not the
    TC10 snapshot.  The live-cache test is on the PATH STRING first."""
    if not env:
        raise SystemExit("HALT: NAIAD_CACHE_DIR is unset — this builder runs only on "
                         f"the frozen snapshot {SNAPSHOT}")
    norm = Path(os.path.normpath(os.path.expanduser(env)))
    if norm == LIVE_CACHE or LIVE_CACHE in norm.parents:
        raise SystemExit("HALT: NAIAD_CACHE_DIR names the LIVE cache — READ-NEVER, WRITE-NEVER for TC10")
    got = norm.resolve()
    if got == LIVE_CACHE or LIVE_CACHE in got.parents:
        raise SystemExit("HALT: NAIAD_CACHE_DIR resolves into the LIVE cache")
    if got != SNAPSHOT.resolve():
        raise SystemExit(f"HALT: NAIAD_CACHE_DIR={got} is not the TC10 snapshot {SNAPSHOT}")
    return got


guard_substrate(os.environ.get("NAIAD_CACHE_DIR"))

sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import pandas as pd                                                  # noqa: E402

import tierc10_panel as TP  # its own guards re-check the substrate  # noqa: E402
import tierc9 as T9                                                  # noqa: E402

# ═══════════════════════════════════════════════════════════════ constants
TC10 = ROOT / "research_outputs" / "tierc10"
OUT = TC10 / "close"
DET_ROOT = OUT / "_det_p_trg_2_seen_share"
REG = "P-TRG-2"
ARM = "trg-9/12 vs card v6 · CLASSIC5 · full"
CELL = "trigger-9/12"

TEXTS_REL = "research_outputs/tierc10/REGISTRATION_TEXTS.json"
PIN_REL = "research_outputs/tierc10/REGISTRY_PIN.json"
DRYRUN_REL = "research_outputs/tierc10/scores/DRYRUN.json"
ROWS_REL = "research_outputs/tierc10/scores/P-TRG-2.rows.json"
PROGRESS_REL = "research_outputs/tierc10/PROGRESS.json"
CTRL_REL = "research_outputs/tierc10/panel/control_journal.parquet"
PANEL_FIX_REL = "research_outputs/tierc10/panel/FIXTURES_PANEL.txt"
TC9_MANIFEST_REL = "research_outputs/tierc9/build_manifest.json"
TC9_GRID_REL = "research_outputs/tierc9/sweep_grid.parquet"
TC9_JOURNAL_REL = "research_outputs/tierc9/trade_journal_control.parquet"
PANEL_STAGE = "PANEL/gate"

JSON_NAME = "P_TRG_2_SEEN_SHARE.json"
MD_NAME = "P_TRG_2_SEEN_SHARE.md"
TRANSCRIPT = "FIXTURES_CLOSE_p_trg_2_seen_share.txt"

TIER = "REPORT-ONLY — TIER-E — NEVER SCORED"
PRE = "AT-OR-BEFORE-TC9-ASOF"
POST = "AFTER-TC9-ASOF"
GRID_FIELDS = ("n", "net_r", "gross_r", "fee_r", "funding_r", "best_r", "win_rate_pct")
KEY_FIELDS = (("shared", "n_shared"), ("cell_only", "n_cell_only"), ("base_only", "n_base_only"))
MS_4H = int(TP.MS_4H)
SEED = 20260921
DET_SEEDS = (1, SEED)
FORBIDDEN_ATTRS = ("score", "finish_family", "register", "_mark_scored")

LINES: list[str] = []


def say(msg: str = "") -> None:
    print(msg, flush=True)
    LINES.append(msg)


def sha_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def iso(ms) -> str:
    return TP.iso(int(ms))


def to_ms(s: str) -> int:
    ts = pd.Timestamp(s)
    if ts.tzinfo is None:
        raise SystemExit(f"HALT: timestamp {s!r} carries no zone — refusing to guess UTC")
    return int(ts.tz_convert("UTC").value // 1_000_000)


def r4(x) -> float:
    return round(float(x), 4)


# ═══════════════════════════════════════════════════════════ read-only guard
def protected_files() -> list[Path]:
    fs: list[Path] = []
    for d in (TC10 / "scores", TC10 / "registrations"):
        fs += [p for p in d.rglob("*") if p.is_file()]
    fs += [p for p in TC10.glob("REGISTRY*") if p.is_file()]
    fs += [TC10 / "PROGRESS.json", TC10 / "FIXTURES_RESUME.txt"]
    fs += [ROOT / r for r in (TEXTS_REL, CTRL_REL, PANEL_FIX_REL, TC9_MANIFEST_REL,
                              TC9_GRID_REL, TC9_JOURNAL_REL)]
    return sorted(set(fs))


def bytes_snapshot() -> dict:
    return {str(p.relative_to(ROOT)): sha_file(p) for p in protected_files()}


def output_guard(paths) -> tuple[bool, list[str]]:
    bad = []
    for p in paths:
        rp = Path(p).resolve()
        if OUT.resolve() not in rp.parents:
            bad.append(str(p))
    return (not bad), bad


def write_out(path: Path, b: bytes) -> None:
    ok, bad = output_guard([path])
    if not ok:
        raise SystemExit(f"HALT: refusing to write outside close/: {bad}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b)


# ═══════════════════════════════════════════════════════════════ inputs
def read_inputs() -> dict:
    I: dict = {"src": {}}

    def rec(rel):
        p = ROOT / rel
        I["src"][rel] = {"sha256": sha_file(p), "bytes": p.stat().st_size}
        return p

    texts = json.loads(rec(TEXTS_REL).read_text("utf-8"))
    I["text"] = texts[REG]["text"]
    pin = json.loads(rec(PIN_REL).read_text("utf-8"))["registrations"][REG]
    I["head"] = (pin["registry_len"], pin["registry_head"])

    dry = json.loads(rec(DRYRUN_REL).read_text("utf-8"))
    arms = [a for a in dry["arms"] if a.get("registration") == REG and a.get("arm") == ARM]
    if len(arms) != 1 or not arms[0].get("scored_in_family"):
        raise SystemExit(f"HALT: DRYRUN.json holds {len(arms)} scored '{ARM}' arm(s), want 1")
    I["dry_idx"] = dry["arms"].index(arms[0])
    I["dry_book_sha"] = arms[0]["book_sha"]
    I["dry_n"] = int(arms[0]["n_campaigns"])
    I["dry_keys"] = arms[0]["keys"]

    rows = json.loads(rec(ROWS_REL).read_text("utf-8"))
    r0 = rows["rows"][0]
    if r0["arm"] != ARM or not r0.get("scored_in_family"):
        raise SystemExit(f"HALT: {ROWS_REL} rows[0] is not the scored '{ARM}' arm")
    I["rows_book_sha"] = r0["score_row"]["book_sha256"]

    prog = json.loads(rec(PROGRESS_REL).read_text("utf-8"))
    st = [s for s in prog["stages"] if s.get("stage") == PANEL_STAGE]
    if len(st) != 1:
        raise SystemExit(f"HALT: PROGRESS.json holds {len(st)} '{PANEL_STAGE}' stage(s)")
    for rel in (CTRL_REL, PANEL_FIX_REL):
        want = st[0]["artifact_shas"][rel]["sha256"]
        got = sha_file(rec(rel))
        if got != want:
            raise SystemExit(f"HALT: {rel} sha {got} != the '{PANEL_STAGE}' record {want}")
    I["ctrl"] = pd.read_parquet(ROOT / CTRL_REL)
    I["panel_fix"] = (ROOT / PANEL_FIX_REL).read_text("utf-8")

    man = json.loads(rec(TC9_MANIFEST_REL).read_text("utf-8"))
    grid = pd.read_parquet(rec(TC9_GRID_REL))
    g = grid[grid["cell"] == CELL]
    if len(g) != 1:
        raise SystemExit(f"HALT: {TC9_GRID_REL} holds {len(g)} '{CELL}' row(s), want 1")
    g = g.iloc[0]
    if str(man["as_of"]) != str(g["as_of_last_closed_4h"]):
        raise SystemExit(f"HALT: TC9 as-of disagrees: manifest {man['as_of']} vs grid "
                         f"{g['as_of_last_closed_4h']}")
    I["asof_iso"] = str(man["as_of"])
    I["asof_ms"] = to_ms(I["asof_iso"])
    I["grid"] = {k: (int(g[k]) if k in ("n",) else float(g[k])) for k in GRID_FIELDS}
    I["grid"].update({k: int(g[k]) for _, k in KEY_FIELDS})
    I["grid"]["as_of_span_days"] = float(g["as_of_span_days"])
    I["tc9_journal"] = pd.read_parquet(rec(TC9_JOURNAL_REL))
    I["tc9_journals_on_disk"] = sorted(p.name for p in (ROOT / "research_outputs/tierc9").glob("*journal*"))
    return I


# ═══════════════════════════════════════════════════════════════ the ride
def ride(I: dict):
    roles = [r for r in T9.SWEEP_CELLS if r.name == CELL]
    if len(roles) != 1:
        raise SystemExit(f"HALT: tierc9.SWEEP_CELLS names {len(roles)} '{CELL}' cell(s)")
    lo, hi, _meta = TP.corridor_era(TP.CLASSIC5, "full")
    book = TP.run_cell_n(TP.CONTROL_CARD, roles[0], TP.CLASSIC5, lo, hi, reg_id=REG,
                         text=I["text"], arm=ARM, head_of_record=I["head"])
    return book, (int(lo), int(hi))


def campaigns_of(book) -> list[dict]:
    out = []
    for t in book:
        ex = getattr(t, "exit_ms", None)
        out.append({"symbol": str(t.symbol), "lane": str(t.lane),
                    "direction": str(getattr(t, "direction", "")),
                    "entry_ms": int(t.entry_ms), "entry_ts": iso(t.entry_ms),
                    "exit_ms": None if ex is None else int(ex),
                    "exit_ts": None if ex is None else iso(ex),
                    "exit_reason": str(getattr(t, "exit_reason", "")),
                    "net_r": float(t.net_r), "gross_r": float(t.gross_r),
                    "fee_r": float(t.fee_r), "funding_r": float(t.funding_r)})
    out.sort(key=lambda c: (c["entry_ms"], c["symbol"], c["lane"]))
    return out


def book_sha_of(cs: list[dict]) -> str:
    """== TP._book_sha: sha256 of sorted (symbol, lane, entry_ms, repr(net_r))."""
    return TP._sha(json.dumps(sorted(
        [c["symbol"], c["lane"], int(c["entry_ms"]), repr(float(c["net_r"]))] for c in cs)))


def label(cs: list[dict], asof_ms: int) -> list[dict]:
    return [dict(c, side=PRE if c["entry_ms"] <= asof_ms else POST,
                 open_across_asof=bool(c["entry_ms"] <= asof_ms and c["exit_ms"] is not None
                                       and c["exit_ms"] > asof_ms)) for c in cs]


def aggregate(cs: list[dict]) -> dict:
    n = len(cs)
    return {"n": n,
            "net_r": r4(sum(c["net_r"] for c in cs)),
            "gross_r": r4(sum(c["gross_r"] for c in cs)),
            "fee_r": r4(sum(c["fee_r"] for c in cs)),
            "funding_r": r4(sum(c["funding_r"] for c in cs)),
            "best_r": r4(max(c["net_r"] for c in cs)) if n else None,
            "win_rate_pct": r4(100.0 * sum(c["net_r"] > 0 for c in cs) / n) if n else None,
            "net_r_full_precision": repr(sum(c["net_r"] for c in cs))}


def grid_compare(agg: dict, grid: dict) -> dict:
    return {k: {"here": agg[k], "grid": grid[k],
                "equal": (agg[k] == grid[k]) if k == "n" else (agg[k] is not None
                                                               and r4(agg[k]) == r4(grid[k]))}
            for k in GRID_FIELDS}


def key_overlap(pre: list[dict], tc9: pd.DataFrame) -> dict:
    bk = {(c["symbol"], c["lane"], c["entry_ms"]) for c in pre}
    jk = {(str(a), str(l), int(e)) for a, l, e in zip(tc9["asset"], tc9["lane"], tc9["entry_ms"])}
    return {"shared": len(bk & jk), "cell_only": len(bk - jk), "base_only": len(jk - bk)}


def keys_compare(ov: dict, grid: dict) -> dict:
    return {k: {"here": ov[k], "grid": grid[g], "equal": ov[k] == grid[g]} for k, g in KEY_FIELDS}


def v6_compare(ctrl: pd.DataFrame, tc9: pd.DataFrame, asof_ms: int) -> dict:
    cpre = ctrl[ctrl["entry_ms"].astype("int64") <= asof_ms]
    m = cpre.merge(tc9, on=["asset", "lane", "entry_ms"], suffixes=("_10", "_9"),
                   how="outer", indicator=True)
    both = int((m["_merge"] == "both").sum())
    one_side = int((m["_merge"] != "both").sum())
    mb = m[m["_merge"] == "both"]
    diffs, unattributed = [], []
    for _, r in mb.iterrows():
        if float(r["net_r_10"]) == float(r["net_r_9"]):
            continue
        row = {"asset": str(r["asset"]), "entry_ts": iso(int(r["entry_ms"])),
               "net_r_tc9": float(r["net_r_9"]), "net_r_here": float(r["net_r_10"]),
               "funding_r_tc9": float(r["funding_r_9"]), "funding_r_here": float(r["funding_r_10"])}
        carried = (float(r["gross_r_10"]) == float(r["gross_r_9"])
                   and float(r["fee_r_10"]) == float(r["fee_r_9"])
                   and round(float(r["net_r_10"]) - float(r["net_r_9"]), 6)
                   == round(-(float(r["funding_r_10"]) - float(r["funding_r_9"])), 6))
        row["carried_by_funding_alone"] = bool(carried)
        (diffs if carried else unattributed).append(row)
    ctrl_cut = ctrl[ctrl["entry_ms"].astype("int64") > TP.ERA_CUT_MS]
    return {"here_pre_n": int(len(cpre)), "here_pre_net_r": r4(cpre["net_r"].sum()),
            "tc9_filed_n": int(len(tc9)), "tc9_filed_net_r": r4(tc9["net_r"].sum()),
            "both": both, "one_side_only": one_side,
            "funding_attributed": diffs, "unattributed": unattributed,
            "here_full_n": int(len(ctrl)),
            "here_post_n": int((ctrl["entry_ms"].astype("int64") > asof_ms).sum()),
            "here_holdout_n": int(len(ctrl_cut)),
            "here_holdout_inside_tc9": int((ctrl_cut["entry_ms"].astype("int64") <= asof_ms).sum())}


def fctrl_b_nb(panel_fix: str) -> tuple[int | None, str | None]:
    for i, ln in enumerate(panel_fix.splitlines(), 1):
        if "[NB ] FILED tierc9/trade_journal_control: funding_r moved on" in ln:
            return i, ln.strip()
    return None, None


# ═══════════════════════════════════════════════════════════════ measure
def measure(I: dict, cs: list[dict], window) -> dict:
    L = label(cs, I["asof_ms"])
    pre = [c for c in L if c["side"] == PRE]
    post = [c for c in L if c["side"] == POST]
    across = [c for c in L if c["open_across_asof"]]
    agg_pre = aggregate(pre)
    gc = grid_compare(agg_pre, I["grid"])
    ov = key_overlap(pre, I["tc9_journal"])
    kc = keys_compare(ov, I["grid"])
    v6 = v6_compare(I["ctrl"], I["tc9_journal"], I["asof_ms"])
    nb_line_no, nb_line = fctrl_b_nb(I["panel_fix"])
    hold = [c for c in L if c["entry_ms"] > TP.ERA_CUT_MS]
    per_asset: dict = {}
    for c in L:
        d = per_asset.setdefault(c["symbol"], {PRE: 0, POST: 0})
        d[c["side"]] += 1
    book_sha = book_sha_of(cs)
    grid_all = all(v["equal"] for v in gc.values())
    keys_all = all(v["equal"] for v in kc.values())
    claim = (f"{agg_pre['n']} of the {len(cs)} campaigns of P-TRG-2's scored book ENTERED AT OR "
             f"BEFORE TIER-C9's as-of ({I['asof_iso']}); "
             + ("their count, net_r, gross_r, fee_r, funding_r, best_r and win rate EQUAL the TIER-C9 "
                "grid row for trigger-9/12 at its 4-dp precision, and their key overlap with TIER-C9's "
                "FILED v6 journal equals the grid's shared / cell-only / base-only. "
                if grid_all and keys_all else
                "they DO NOT reproduce the TIER-C9 grid row (see grid_compare / keys_compare). ")
             + "TIER-C9 filed no per-campaign trigger-9/12 journal, so this is an aggregate-and-overlap "
               "match, not a key-for-key match against a TC9 9/12 book.")
    return {
        "tier": TIER,
        "registration": REG, "arm": ARM,
        "window": {"lo": iso(window[0]), "hi_close": iso(window[1] + 1)},
        "tc9_asof": {"iso": I["asof_iso"], "ms": I["asof_ms"],
                     "source": f"{TC9_MANIFEST_REL} .as_of == {TC9_GRID_REL} as_of_last_closed_4h"},
        "book": {"n": len(cs), "sha256": book_sha, "dryrun_pin": I["dry_book_sha"],
                 "dryrun_arm_index": I["dry_idx"], "rows_json_book_sha256": I["rows_book_sha"],
                 "equal_dryrun": book_sha == I["dry_book_sha"],
                 "equal_rows_json": book_sha == I["rows_book_sha"],
                 "net_r": r4(sum(c["net_r"] for c in cs)),
                 "exit_reasons": dict(sorted(_count(c["exit_reason"] for c in cs).items()))},
        "pre": agg_pre,
        "post": {"n": len(post), "net_r": r4(sum(c["net_r"] for c in post)),
                 "campaigns": [{k: c[k] for k in ("symbol", "direction", "entry_ts", "exit_ts",
                                                  "exit_reason", "net_r")} for c in post]},
        "open_across_asof": len(across),
        "per_asset": dict(sorted(per_asset.items())),
        "grid_row": {"path": TC9_GRID_REL, "cell": CELL, **I["grid"]},
        "grid_compare": gc, "grid_all_equal": grid_all,
        "keys_vs_tc9_filed_v6_journal": {"path": TC9_JOURNAL_REL, **ov},
        "keys_compare": kc, "keys_all_equal": keys_all,
        "tc9_journals_on_disk": I["tc9_journals_on_disk"],
        "era_cut": {"iso": TP.ERA_CUT_ISO, "book_holdout_n": len(hold),
                    "book_holdout_inside_tc9": sum(1 for c in hold if c["side"] == PRE),
                    "base_holdout_n": v6["here_holdout_n"],
                    "base_holdout_inside_tc9": v6["here_holdout_inside_tc9"]},
        "v6_base_vs_tc9_filed": v6,
        "fctrl_b_nb": {"path": PANEL_FIX_REL, "line": nb_line_no, "text": nb_line},
        "claim": claim,
        "sources": I["src"],
        "campaigns": [{k: c[k] for k in ("symbol", "lane", "direction", "entry_ms", "entry_ts",
                                          "exit_ts", "exit_reason", "net_r", "side")} for c in L],
    }


def _count(it) -> dict:
    d: dict = {}
    for x in it:
        d[x] = d.get(x, 0) + 1
    return d


# ═══════════════════════════════════════════════════════════════ render
def render_json(M: dict) -> bytes:
    return (json.dumps(M, indent=1, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


def f4(x) -> str:
    return "None" if x is None else f"{float(x):+.4f}"


def render_md(M: dict) -> bytes:
    L = []
    a = L.append
    a(f"# P-TRG-2 · THE SEEN SHARE — {M['tier']}")
    a("")
    a("*Built by `scripts/tierc10_close_p_trg_2_seen_share.py`. It rides P-TRG-2's scored arm to its Book through the "
      "registration's own door, as the pinned dry-run does, and splits the book at TIER-C9's as-of. It computes counts "
      "and sums only: no CI, no p, no verdict. `TP.score`, `finish_family`, `register` and `_mark_scored` are never "
      "referenced (F-SS-CLOSURE).*")
    a("")
    a("## The claim, as worded by the builder")
    a("")
    a(M["claim"])
    a("")
    b = M["book"]
    a("## The book")
    a("")
    a(f"- Arm: `{M['arm']}` · window {M['window']['lo']} → {M['window']['hi_close']}.")
    a(f"- n {b['n']}, Σ net_r {f4(b['net_r'])} R. Exit reasons: "
      + ", ".join(f"{k} {v}" for k, v in b["exit_reasons"].items()) + ".")
    a(f"- Book sha256 `{b['sha256']}`. Dry-run pin (`scores/DRYRUN.json arms[{b['dryrun_arm_index']}].book_sha`) "
      f"equal: {b['equal_dryrun']}. Scored row (`scores/P-TRG-2.rows.json rows[0].score_row.book_sha256`) "
      f"equal: {b['equal_rows_json']}.")
    a(f"- TIER-C9's as-of: {M['tc9_asof']['iso']} ({M['tc9_asof']['source']}).")
    a("")
    a("## The split at TIER-C9's as-of")
    a("")
    p, q = M["pre"], M["post"]
    a("| side | n | Σ net_r (R) |")
    a("|---|---:|---:|")
    a(f"| {PRE} | {p['n']} | {f4(p['net_r'])} |")
    a(f"| {POST} | {q['n']} | {f4(q['net_r'])} |")
    a(f"| open across the as-of | {M['open_across_asof']} | — |")
    a("")
    a("**The AFTER campaigns (the unseen month):**")
    a("")
    a("| asset | dir | entered | exited | exit | net_r |")
    a("|---|---|---|---|---|---:|")
    for c in q["campaigns"]:
        a(f"| {c['symbol']} | {c['direction']} | {c['entry_ts']} | {c['exit_ts']} | {c['exit_reason']} | "
          f"{c['net_r']:+.6f} |")
    a("")
    a("**Per asset (at-or-before / after):** " + " · ".join(
        f"{s} {d[PRE]}/{d[POST]}" for s, d in M["per_asset"].items()))
    a("")
    a("## Held against TIER-C9's grid row for trigger-9/12 (`research_outputs/tierc9/sweep_grid.parquet`)")
    a("")
    a("| field | at-or-before, here | TC9 grid row | equal at 4 dp |")
    a("|---|---:|---:|---|")
    for k in GRID_FIELDS:
        v = M["grid_compare"][k]
        here = v["here"] if k == "n" else f"{v['here']:.4f}"
        grid = v["grid"] if k == "n" else f"{v['grid']:.4f}"
        a(f"| {k} | {here} | {grid} | {v['equal']} |")
    a("")
    kv = M["keys_vs_tc9_filed_v6_journal"]
    a(f"**Key overlap with TIER-C9's FILED v6 journal** (`{kv['path']}`, key asset · lane · entry_ms):")
    a("")
    a("| count | here | TC9 grid row | equal |")
    a("|---|---:|---:|---|")
    for k, g in KEY_FIELDS:
        v = M["keys_compare"][k]
        a(f"| {k} ({g}) | {v['here']} | {v['grid']} | {v['equal']} |")
    a("")
    a("TIER-C9 journals on disk: " + ", ".join(f"`{x}`" for x in M["tc9_journals_on_disk"])
      + ". None is a trigger-9/12 book, so no key-for-key match against one is possible.")
    a("")
    e = M["era_cut"]
    a(f"## The R1 era cut ({e['iso']})")
    a("")
    a(f"- Book campaigns after the cut: {e['book_holdout_n']}; of those, entered at or before TIER-C9's as-of: "
      f"{e['book_holdout_inside_tc9']}.")
    a(f"- v6 base campaigns after the cut: {e['base_holdout_n']}; of those, at or before TIER-C9's as-of: "
      f"{e['base_holdout_inside_tc9']}.")
    a("")
    v = M["v6_base_vs_tc9_filed"]
    a("## The v6 base, held against TIER-C9's filed v6 journal")
    a("")
    a(f"- Here, at or before the as-of: n {v['here_pre_n']}, Σ net_r {f4(v['here_pre_net_r'])}. TIER-C9 filed: "
      f"n {v['tc9_filed_n']}, Σ net_r {f4(v['tc9_filed_net_r'])}.")
    a(f"- Campaigns on both sides: {v['both']}; on one side only: {v['one_side_only']}.")
    for r in v["funding_attributed"]:
        a(f"- Carried by funding_r alone (gross_r and fee_r exact): {r['asset']} {r['entry_ts']}, funding_r "
          f"{r['funding_r_tc9']} → {r['funding_r_here']}, net_r {r['net_r_tc9']:+.6f} → {r['net_r_here']:+.6f}.")
    a(f"- Unattributed differences: {len(v['unattributed'])}.")
    nb = M["fctrl_b_nb"]
    a(f"- F-CTRL/b's line (`{nb['path']}:{nb['line']}`): `{nb['text']}`")
    a(f"- v6 after the as-of (the forward strip's window): {v['here_post_n']} campaigns.")
    a("")
    a("## Sources read this run (sha256 · bytes)")
    a("")
    for rel, s in sorted(M["sources"].items()):
        a(f"- `{rel}` · `{s['sha256']}` · {s['bytes']}")
    a("")
    a(f"*The per-campaign list (all {M['book']['n']} campaigns: asset, lane, direction, entry_ms, entry_ts, exit, "
      f"exit reason, net_r, side) is in `{JSON_NAME}` under `campaigns`.*")
    a("")
    return "\n".join(L).encode("utf-8")


def build() -> tuple[dict, bytes, bytes, list, dict]:
    I = read_inputs()
    book, window = ride(I)
    ridden_sha = TP._book_sha(book)
    cs = campaigns_of(book)
    if book_sha_of(cs) != ridden_sha:
        raise SystemExit("HALT: the campaign list does not reproduce TP._book_sha")
    if ridden_sha != I["dry_book_sha"] or ridden_sha != I["rows_book_sha"]:
        raise SystemExit(f"HALT: ridden book sha {ridden_sha} != dry-run pin {I['dry_book_sha']} "
                         f"/ scored row {I['rows_book_sha']}")
    M = measure(I, cs, window)
    return M, render_json(M), render_md(M), cs, I


# ═══════════════════════════════════════════════════════════════ fixtures
RESULTS: dict = {}


def leg(name: str, fails_if: str, real: tuple, sabotages: list) -> bool:
    say(f"{name} · FAILS IF {fails_if}")
    ok_real, why_real = real
    say(f"  real      {'GREEN' if ok_real else 'RED'} — {why_real}")
    all_red = True
    for desc, (ok_s, why_s) in sabotages:
        red = not ok_s
        all_red &= red
        say(f"  sabotage  {desc}: {'RED (as required)' if red else 'GREEN — SABOTAGE NOT CAUGHT'} — {why_s}")
    ok = bool(ok_real and all_red)
    say(f"  => {name} {'GREEN' if ok else 'RED'}")
    say("")
    RESULTS[name] = ok
    return ok


def chk_book(cs, I) -> tuple:
    s = book_sha_of(cs)
    ok = s == I["dry_book_sha"] == I["rows_book_sha"]
    return ok, f"book sha {s[:16]}… vs dry-run pin {I['dry_book_sha'][:16]}… and scored row {I['rows_book_sha'][:16]}…"


def chk_split(L, asof_ms, n_book) -> tuple:
    wrong = [c for c in L if (c["side"] == PRE) != (c["entry_ms"] <= asof_ms)]
    sides = {c["side"] for c in L} - {PRE, POST}
    ok = not wrong and not sides and len(L) == n_book
    return ok, (f"{len(L)} campaigns, each on exactly one side; misplaced {len(wrong)}"
                + (f" e.g. {wrong[0]['symbol']} {wrong[0]['entry_ts']} labelled {wrong[0]['side']}" if wrong else ""))


def chk_grid(pre, grid) -> tuple:
    gc = grid_compare(aggregate(pre), grid)
    bad = {k: (v["here"], v["grid"]) for k, v in gc.items() if not v["equal"]}
    return (not bad), ("7/7 fields equal the grid row" if not bad else f"differ: {bad}")


def chk_keys(pre, tc9, grid) -> tuple:
    kc = keys_compare(key_overlap(pre, tc9), grid)
    bad = {k: (v["here"], v["grid"]) for k, v in kc.items() if not v["equal"]}
    return (not bad), ("shared/cell-only/base-only equal the grid row: "
                       + ", ".join(f"{k} {v['here']}" for k, v in kc.items())
                       if not bad else f"differ: {bad}")


def chk_v6(ctrl, tc9, asof_ms, panel_fix) -> tuple:
    v = v6_compare(ctrl, tc9, asof_ms)
    _, nb = fctrl_b_nb(panel_fix)
    names_ok = nb is not None and all(f"{r['asset']} {r['entry_ts']}" in nb for r in v["funding_attributed"]) \
        and f"funding_r moved on {len(v['funding_attributed'])} closed campaign" in nb
    ok = v["one_side_only"] == 0 and not v["unattributed"] and names_ok
    return ok, (f"both {v['both']}, one-side {v['one_side_only']}, funding-attributed "
                f"{[(r['asset'], r['entry_ts']) for r in v['funding_attributed']]}, unattributed "
                f"{len(v['unattributed'])}, matches F-CTRL/b [NB]: {names_ok}")


def chk_closure(source: str) -> tuple:
    tree = ast.parse(source)
    hits = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute) and node.attr in FORBIDDEN_ATTRS:
            hits.append(f".{node.attr}")
        if isinstance(node, ast.Name) and node.id in FORBIDDEN_ATTRS:
            hits.append(node.id)
    return (not hits), ("no score / finish_family / register / _mark_scored reference"
                        if not hits else f"forbidden: {sorted(set(hits))}")


def det_runs() -> tuple:
    outs = {}
    for seed in DET_SEEDS:
        d = DET_ROOT / f"seed_{seed}"
        env = dict(os.environ, PYTHONHASHSEED=str(seed), NAIAD_CACHE_DIR=str(SNAPSHOT),
                   PYTHONDONTWRITEBYTECODE="1")
        r = subprocess.run([sys.executable, str(Path(__file__).resolve()), "--out-dir", str(d)],
                           env=env, capture_output=True, text=True, cwd=str(ROOT))
        outs[seed] = (r.returncode, (d / JSON_NAME).read_bytes() if (d / JSON_NAME).exists() else b"",
                      (d / MD_NAME).read_bytes() if (d / MD_NAME).exists() else b"")
    return outs


def run_fixtures(M, jb, mb, cs, I, before) -> bool:
    asof = I["asof_ms"]
    L = label(cs, asof)
    pre = [c for c in L if c["side"] == PRE]

    # F-SS-SUBSTRATE
    def substrate_check(guard) -> tuple:
        def must_halt(v):
            try:
                guard(v)
                return False
            except SystemExit:
                return True
        reals = {"unset": must_halt(None), "live cache": must_halt(str(LIVE_CACHE)),
                 "foreign dir": must_halt(str(OUT))}
        passes = not must_halt(str(SNAPSHOT))
        return (all(reals.values()) and passes,
                f"HALTs on {sorted(k for k, v in reals.items() if v)} of 3; the snapshot passes: {passes}")
    leg("F-SS-SUBSTRATE", "the guard accepts an unset, live-cache or foreign NAIAD_CACHE_DIR",
        substrate_check(guard_substrate),
        [("a guard that accepts any directory", substrate_check(lambda v: Path(v or ".")))])

    # F-SS-BOOK
    bent = [dict(c) for c in cs]
    bent[0]["net_r"] = bent[0]["net_r"] + 1e-9
    leg("F-SS-BOOK", "the ridden book's sha differs from the dry-run pin or the scored row's book_sha256",
        chk_book(cs, I), [("one net_r bent 1e-9 in a copy", chk_book(bent, I))])

    # F-SS-SPLIT
    mis = [dict(c) for c in L]
    j = next(i for i, c in enumerate(mis) if c["side"] == POST)
    mis[j]["side"] = PRE
    wrong_asof = int(TP.corridor_era(TP.CLASSIC5, "full")[1]) + 1   # TC10's own corridor end
    wrong = label(cs, wrong_asof)
    leg("F-SS-SPLIT", "a campaign sits on the wrong side of TC9's as-of, on both sides, or on neither",
        chk_split(L, asof, len(cs)),
        [("one AFTER campaign relabelled AT-OR-BEFORE", chk_split(mis, asof, len(cs))),
         (f"the split taken at TC10's corridor end {iso(wrong_asof)} instead of TC9's as-of",
          chk_split(wrong, asof, len(cs)))])

    # F-SS-GRID
    drop = pre[1:]
    bentn = [dict(c) for c in pre]
    bentn[0]["net_r"] += 1e-4
    pre_wrong = [c for c in wrong if c["side"] == PRE]
    leg("F-SS-GRID", "the AT-OR-BEFORE part differs from TC9's grid row on n, net_r, gross_r, fee_r, "
        "funding_r, best_r or win_rate_pct (4 dp)",
        chk_grid(pre, I["grid"]),
        [("one campaign dropped", chk_grid(drop, I["grid"])),
         ("one net_r bent +1e-4", chk_grid(bentn, I["grid"])),
         ("the split taken at TC10's corridor end instead of TC9's as-of", chk_grid(pre_wrong, I["grid"]))])

    # F-SS-KEYS
    moved = [dict(c) for c in pre]
    tc9keys = {(str(a), int(e)) for a, e in zip(I["tc9_journal"]["asset"], I["tc9_journal"]["entry_ms"])}
    k = next(i for i, c in enumerate(moved) if (c["symbol"], c["entry_ms"]) in tc9keys)
    moved[k]["entry_ms"] += MS_4H
    leg("F-SS-KEYS", "the key overlap with TC9's filed v6 journal differs from the grid's "
        "n_shared / n_cell_only / n_base_only",
        chk_keys(pre, I["tc9_journal"], I["grid"]),
        [("one shared book key's entry moved one 4h bar", chk_keys(moved, I["tc9_journal"], I["grid"]))])

    # F-SS-V6
    tc9b = I["tc9_journal"].copy()
    tc9b.loc[tc9b.index[0], "gross_r"] = float(tc9b.loc[tc9b.index[0], "gross_r"]) + 1e-6
    tc9b.loc[tc9b.index[0], "net_r"] = float(tc9b.loc[tc9b.index[0], "net_r"]) + 1e-6
    leg("F-SS-V6", "a v6 campaign is on one side only, a net_r difference is not carried by funding_r alone "
        "(gross_r, fee_r exact), or the attributed set differs from F-CTRL/b's [NB] line",
        chk_v6(I["ctrl"], I["tc9_journal"], asof, I["panel_fix"]),
        [("a TC9 gross_r (and net_r) bent 1e-6 in a copy", chk_v6(I["ctrl"], tc9b, asof, I["panel_fix"]))])

    # F-SS-CLOSURE
    src = Path(__file__).read_text("utf-8")
    leg("F-SS-CLOSURE", "this module references score / finish_family / register / _mark_scored",
        chk_closure(src), [("a planted TP.score(book) call", chk_closure(src + "\nTP.score(None)\n"))])

    # F-SS-NOWRITE
    after = bytes_snapshot()
    moved_files = sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k))
    g_ok, g_bad = output_guard([OUT / JSON_NAME, OUT / MD_NAME, OUT / TRANSCRIPT])
    s_ok, s_bad = output_guard([ROOT / "exchange/status/LEDGER_APOLLO.md"])
    leg("F-SS-NOWRITE", "a byte of scores/, registrations/, REGISTRY*, PROGRESS.json, FIXTURES_RESUME.txt "
        "or an input moves during the run, or an output path leaves close/",
        (not moved_files and g_ok, f"{len(before)} protected files unchanged; outputs under close/ only"),
        [("an output path under exchange/status/", (s_ok, f"guard refuses {s_bad}"))])

    # F-DET
    outs = det_runs()
    rc = {s: o[0] for s, o in outs.items()}
    same = outs[DET_SEEDS[0]][1:] == outs[DET_SEEDS[1]][1:]
    disk = outs[DET_SEEDS[0]][1] == jb and outs[DET_SEEDS[0]][2] == mb
    salted = render_json(dict(M, salt=os.getpid()))
    leg("F-DET", "two subprocess builds (PYTHONHASHSEED 1, 20260921) differ from each other or from this run's bytes",
        (all(v == 0 for v in rc.values()) and same and disk,
         f"exit {rc}; json {sha_bytes(outs[DET_SEEDS[0]][1])[:16]}… == {sha_bytes(outs[DET_SEEDS[1]][1])[:16]}…: "
         f"{same}; == this run: {disk}"),
        [("a process-dependent salt in the JSON", (salted == jb, "salted build byte-identical: "
                                                  f"{salted == jb}"))])
    return all(RESULTS.values())


# ═══════════════════════════════════════════════════════════════ main
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fixtures", action="store_true")
    ap.add_argument("--out-dir", default=None, help="F-DET only: a directory under close/_det_*")
    a = ap.parse_args()
    before = bytes_snapshot()
    M, jb, mb, cs, I = build()
    out = Path(a.out_dir) if a.out_dir else OUT
    if a.out_dir and DET_ROOT.resolve() not in Path(a.out_dir).resolve().parents:
        raise SystemExit(f"HALT: --out-dir must lie under {DET_ROOT}")
    write_out(out / JSON_NAME, jb)
    write_out(out / MD_NAME, mb)
    if a.out_dir:
        return 0
    say("TIER-C10 · CLOSE · P-TRG-2 SEEN SHARE — FIXTURES (F-SS)")
    say(f"substrate tc10_20260921 · {TIER} · counts and sums only; no CI, no p, no verdict")
    say(f"OUTPUT (sha256 · bytes)")
    say(f"  {sha_bytes(jb)} · {len(jb)} · research_outputs/tierc10/close/{JSON_NAME}")
    say(f"  {sha_bytes(mb)} · {len(mb)} · research_outputs/tierc10/close/{MD_NAME}")
    say(f"book sha {M['book']['sha256']} · n {M['book']['n']} · pre {M['pre']['n']} "
        f"({M['pre']['net_r']:+.4f} R) · post {M['post']['n']} ({M['post']['net_r']:+.4f} R) · "
        f"open across {M['open_across_asof']}")
    say("")
    if not a.fixtures:
        return 0
    ok = run_fixtures(M, jb, mb, cs, I, before)
    say(f"FIXTURE SUMMARY {sum(RESULTS.values())}/{len(RESULTS)} GREEN "
        + json.dumps(RESULTS, sort_keys=False))
    write_out(OUT / TRANSCRIPT, ("\n".join(LINES) + "\n").encode("utf-8"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
