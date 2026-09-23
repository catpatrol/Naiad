#!/usr/bin/env python
"""TIER-C10 · CLOSE · P-AGE-1 (tide-youth) — TIER-E TABLES ONLY.

Contract of record: exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md:113
    "P-AGE-1 (tide-youth), boundary-fade, regime-prior: Tier-E tables only."

TIER-E MEASUREMENT: UNSCORED, GATES NOTHING.  Every band row is a SELECTION,
not a result.  The build is in-sample.  Nothing here is registered, scored
(no verdict, p, CI or BH bar), filed to the registry, or used as a filter.
The script never calls TP.score, TP.finish_family or TP.register, and it
never reads a registration or its verdict.

THE DEFINITION IS AN EXECUTOR READING AND ADDS NO NEW PIN.  Tide-youth is
the age of the 4h tide a campaign joins at its entry.  It is measured by
`tierc7_lab_regime.tide_streak(sym)`, the run length of sign(e89 - e316) at
the entry bar, counted from the lab's warm floor.  The regime lab's own law
bands it: the quantiles STREAK_BAND_QUANTILES of the panel-pooled bar
distribution, with the labels STREAK_LABELS (B1 = the YOUNG tide).  The band
edges are TRAILING, meaning causal, expanding and panel-pooled over the bars
at or before each campaign's own entry bar.  This is exactly TC9's TC7-g,
`tierc9.tc7g_tables`, run unchanged.  Every constant is read from its module
and never typed here.

METHOD (the auditor's build spec):
  (lo, hi, meta) = tierc10_panel.corridor_n(tierc10_panel.CLASSIC5).
    The corridor edge is asserted to equal PROGRESS.json as_of_of_record.
  frames, _ = tierc9.tc7g_tables(lo, hi).
    · frames['tc7g_regime_cross_trailing'] is kept, restricted to the rows
      with dimension == 'tide_streak_band' AND card == 'v6'.  The hybrid
      rows are not printed.            -> P_AGE_1_TIDE_YOUTH.parquet
    · frames['tc7g_tide_streak_bands'] -> P_AGE_1_BAR_BANDS.parquet
    · frames['tc7g_edge_evolution']    -> P_AGE_1_EDGES.parquet
  Each table is stamped with tierc10_panel.stamp_n(df, meta, '4h') and
  carries the Tier-E collar.  Any verdict/p/ci/clears_bh_bar column is
  dropped.  The D15 trio rides, labelled "gates nothing".

RUN/HALT PREAMBLE: the substrate must be the frozen TC10 snapshot, never the
live cache, with PYTHONDONTWRITEBYTECODE=1.  The corridor edge must equal
PROGRESS.as_of_of_record.  The lab's 4h frames must equal
tierc10_data.load_asof bars exactly.  This script reads its own bars only
through load_asof, and the lab's frames are proven identical to them, so no
bar past the pin enters.  Output goes only to research_outputs/tierc10/close/
(or to an F-DET temp dir).  F-AGE-BOOK is a precondition: if the lab's v6 book
is not the TC10 control journal, the script HALTs before anything is written.

FIXTURE LEGS: each states FAILS IF and carries a sabotage that must go RED:
  F-AGE-BOOK · F-AGE-WHOLE · F-AGE-CAUSAL · F-AGE-COLLAR · F-AGE-ASOF · F-DET

Run (whole; writes the four outputs + FIXTURES_CLOSE_p_age_1.txt):
  export NAIAD_CACHE_DIR=/Users/luis/.cache/naiad/snapshots/tc10_20260921 \\
         PYTHONDONTWRITEBYTECODE=1
  ~/venvs/naiad/bin/python scripts/tierc10_close_p_age_1_tide_youth.py
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = Path.home() / ".cache" / "naiad" / "snapshots" / "tc10_20260921"
LIVE_CACHE = Path.home() / ".cache" / "naiad" / "data_cache"


# ═══════════════════════════ RUN/HALT · THE ENVIRONMENT, BEFORE ANY IMPORT
def _halt(msg: str) -> None:
    raise SystemExit(f"HALT: {msg}")


def _env_gate(environ=None) -> None:
    """THE SAME RUN/HALT GATE AS THE FORWARD STRIP (guard_substrate).  It
    HALTS IF NAIAD_CACHE_DIR is unset, names the live cache, or is not the
    TC10 snapshot, and IF PYTHONDONTWRITEBYTECODE is not '1'.  The live-cache
    test is made on the PATH STRING first, so this guard never stats the live
    cache.  It runs BEFORE any tier module is imported, because those modules
    bind cache paths at import time."""
    environ = os.environ if environ is None else environ
    env = environ.get("NAIAD_CACHE_DIR", "")
    if not env:
        _halt("NAIAD_CACHE_DIR is unset; P-AGE-1 runs only on the frozen "
              f"snapshot {SNAPSHOT}; export it BEFORE python starts.")
    norm = Path(os.path.normpath(os.path.expanduser(env)))
    if norm == LIVE_CACHE or LIVE_CACHE in norm.parents:
        _halt("NAIAD_CACHE_DIR names the LIVE cache: READ-NEVER, WRITE-NEVER.")
    got = norm.resolve()
    if got == LIVE_CACHE or LIVE_CACHE in got.parents:
        _halt("NAIAD_CACHE_DIR resolves into the LIVE cache.")
    if got != SNAPSHOT.resolve():
        _halt(f"NAIAD_CACHE_DIR={got} is not the TC10 snapshot {SNAPSHOT}.")
    if environ.get("PYTHONDONTWRITEBYTECODE") != "1":
        _halt("PYTHONDONTWRITEBYTECODE is not '1'.")


_env_gate()
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import numpy as np                                                   # noqa: E402
import pandas as pd                                                  # noqa: E402

import tierc10_data as D           # its import re-asserts the substrate  # noqa: E402
import tierc10_panel as TP                                           # noqa: E402
import tierc9 as T9                                                  # noqa: E402
import tierc7 as T7                                                  # noqa: E402
import tierc7_rules as RC                                            # noqa: E402
import tierc7_lab_regime as LR                                       # noqa: E402
import tierc2_baseline as TB                                         # noqa: E402

iso, MS_4H = TB.iso, TP.MS_4H

# ═══════════════════════════════════════════════════════════ CONSTANTS
OUT_ROOT = ROOT / "research_outputs" / "tierc10"
CLOSE_DIR = OUT_ROOT / "close"
PROGRESS = OUT_ROOT / "PROGRESS.json"
CONTROL_JOURNAL = OUT_ROOT / "panel" / "control_journal.parquet"
CONTRACT = ROOT / "exchange" / "queue" / "2026-09-22_TC10_RESUME_APOLLO.md"
CONTRACT_LINE_NO = 113
CONTRACT_NEEDLE = "P-AGE-1 (tide-youth)"
TRANSCRIPT_NAME = "FIXTURES_CLOSE_p_age_1.txt"
DET_ROOT = CLOSE_DIR / "_det_p_age_1"
PANEL_STAGE = "PANEL/gate"
JOURNAL_REL = "research_outputs/tierc10/panel/control_journal.parquet"
AS_OF_PIN_REL = "research_outputs/tierc10/data/AS_OF_PIN.json"

T_YOUTH = "P_AGE_1_TIDE_YOUTH"
T_BARS = "P_AGE_1_BAR_BANDS"
T_EDGES = "P_AGE_1_EDGES"
MD_NAME = "P_AGE_1_TIDE_YOUTH.md"
KEYS = {T_YOUTH: ["dimension", "band", "card"],
        T_BARS: ["basis", "band"],
        T_EDGES: ["as_of"]}
OUTPUT_FILES = tuple(f"{n}.parquet" for n in (T_YOUTH, T_BARS, T_EDGES)) \
    + (MD_NAME,)

DIM = "tide_streak_band"
CARD = "v6"
ALL_BAND = "99-ALL"
BOOK_COLS = ("asset", "entry_ms", "direction", "exit_ms", "exit_reason",
             "net_r")

# THE TIER-E COLLAR
TIER = "TIER-E MEASUREMENT — UNSCORED, GATES NOTHING"
SELECTION = ("a SELECTION, not a result: a band row is a cut of an in-sample "
             "book, and the reader chooses it by reading it. No band may be "
             "promoted, gated on or registered from this table. P-AGE-1 is "
             "Tier-E only (contract APOLLO:113).")
COLLAR_COLUMNS = ("tier", "selection_not_a_result", "m_selections_this_table",
                  "in_sample")
BANNED_EXACT = ("verdict", "clears_bh_bar", "p_one_sided")
BANNED_RX = re.compile(r"(^|_)verdict($|_)|clears_bh|^p_|_p$|p_value|"
                       r"(^|_)ci(_|$)")
D15_TRIO = ("paired_delta_expectancy_r", "tail_exit_ratio",
            "max_single_trade_delta_share")
D15_LABEL = ("D15 trio: GATES NOTHING. The v6 rows are self-paired against "
             "the v6 book restricted to the same band, so delta = 0 and the "
             "tail ratio = 1 by construction (the lab asserts this).")


def definition_text() -> str:
    """THE DEFINITION, AN EXECUTOR READING WITH NO NEW PIN.  Every constant is
    read from its module and none is typed here."""
    return (
        "EXECUTOR READING, NO NEW PIN: tide-youth = "
        "tierc7_lab_regime.tide_streak(sym)[1] (the run length of "
        "sign(e89 - e316) on the 4h frame) at the campaign's ENTRY bar, "
        f"counted from TIDE_WARM_BARS = {LR.TIDE_WARM_BARS}. It is banded by "
        f"STREAK_BAND_QUANTILES = {tuple(LR.STREAK_BAND_QUANTILES)} of the "
        f"panel-pooled bar distribution into STREAK_LABELS = "
        f"{tuple(LR.STREAK_LABELS)} (B1 = {LR.STREAK_LABELS[0]!r}). The "
        "edges are TRAILING: causal, expanding and panel-pooled over the bars "
        "with open_ms <= the entry bar, inclusive. The prefix floor is "
        f"n >= RC.PROVISIONAL_MIN_N = {RC.PROVISIONAL_MIN_N}. This is exactly "
        "TC9's TC7-g (tierc9.tc7g_tables)."
    )


# ═══════════════════════════════════════════════════════════ SMALL HELPERS
def sha_file(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def content_sha(df: pd.DataFrame) -> str:
    return TB._content_sha(df)


def _guard_out(out: Path) -> Path:
    """Writes ONLY under research_outputs/tierc10/close/: the close dir
    itself, or an F-DET run dir directly under close/_det_p_age_1/."""
    out = Path(out).resolve()
    if out == CLOSE_DIR.resolve() or out.parent == DET_ROOT.resolve():
        return out
    _halt(f"output dir {out} is neither {CLOSE_DIR} nor an F-DET run dir "
          f"under {DET_ROOT}; this script writes nowhere else.")
    return out  # unreachable


def protected_files() -> list[Path]:
    """Everything this build must NEVER move (the forward strip's list):
    scores/, registrations/ (the registry included), REGISTRY*,
    PROGRESS.json, FIXTURES_RESUME.txt, and every input it reads."""
    fs: list[Path] = []
    for d in (OUT_ROOT / "scores", OUT_ROOT / "registrations"):
        fs += [p for p in d.rglob("*") if p.is_file()]
    fs += [p for p in OUT_ROOT.glob("REGISTRY*") if p.is_file()]
    fs += [PROGRESS, OUT_ROOT / "FIXTURES_RESUME.txt", CONTROL_JOURNAL,
           ROOT / AS_OF_PIN_REL, CONTRACT]
    return sorted(set(fs))


def bytes_snapshot() -> dict:
    return {str(p.relative_to(ROOT)): sha_file(p) for p in protected_files()}


# ═══════════════════════════════════════════════ RUN/HALT · THE PREAMBLE
def preamble(P) -> dict:
    """RUN/HALT.  HALTS IF: the loaders are not bound to the snapshot; the
    contract line 113 does not name P-AGE-1; the corridor edge differs from
    PROGRESS.as_of_of_record; or any CLASSIC5 4h frame the lab reads differs
    from tierc10_data.load_asof bars (count, stamps or OHLC, exact)."""
    sub = TP.substrate()
    prog = json.loads(PROGRESS.read_text())
    as_of = prog["as_of_of_record"]
    as_of_ms = int(prog["as_of_last_closed_4h_close_ms"])
    if iso(as_of_ms) != as_of:
        _halt(f"PROGRESS as_of_of_record {as_of} != "
              f"as_of_last_closed_4h_close_ms {as_of_ms} ({iso(as_of_ms)})")
    pin = D.load_pin()
    if (int(pin["as_of_last_closed_4h_close_ms"]) != as_of_ms
            or pin["as_of_last_closed_4h"] != as_of):
        _halt(f"{AS_OF_PIN_REL} ({pin['as_of_last_closed_4h']}) disagrees "
              f"with PROGRESS.json ({as_of})")
    c = prog["contract_of_record"]
    if (ROOT / c["path"]).resolve() != CONTRACT.resolve():
        _halt(f"PROGRESS contract_of_record {c['path']} is not {CONTRACT}")
    csha = sha_file(CONTRACT)
    if csha != c["sha256"]:
        _halt(f"contract {c['path']} sha256 {csha} != PROGRESS record "
              f"{c['sha256']}")
    st = [x for x in prog["stages"] if x.get("stage") == PANEL_STAGE]
    if len(st) != 1:
        _halt(f"PROGRESS.json holds {len(st)} '{PANEL_STAGE}' stage(s), "
              f"want 1")
    rec = st[0]["artifact_shas"].get(JOURNAL_REL)
    if rec is None:
        _halt(f"PROGRESS '{PANEL_STAGE}' records no sha for {JOURNAL_REL}")
    jsha = sha_file(CONTROL_JOURNAL)
    if jsha != rec["sha256"] or CONTROL_JOURNAL.stat().st_size != rec["bytes"]:
        _halt(f"{JOURNAL_REL} sha256 {jsha} / "
              f"{CONTROL_JOURNAL.stat().st_size} B != the '{PANEL_STAGE}' "
              f"record {rec['sha256']} / {rec['bytes']} B")
    lines = CONTRACT.read_text(encoding="utf-8").splitlines()
    cline = lines[CONTRACT_LINE_NO - 1].strip()
    if CONTRACT_NEEDLE not in cline:
        _halt(f"{CONTRACT.name}:{CONTRACT_LINE_NO} does not name "
              f"{CONTRACT_NEEDLE!r}: {cline!r}")
    if tuple(TP.CLASSIC5) != tuple(RC.UNIVERSE):
        _halt(f"CLASSIC5 {TP.CLASSIC5} != the lab's RC.UNIVERSE "
              f"{RC.UNIVERSE}; the lab would pool a different panel.")
    lo, hi, meta = TP.corridor_n(TP.CLASSIC5)
    if meta["last_closed_4h_close"] != as_of or hi + 1 != as_of_ms:
        _halt(f"corridor edge {meta['last_closed_4h_close']} (hi+1 = "
              f"{hi + 1}) != PROGRESS.as_of_of_record {as_of} "
              f"({as_of_ms}).")
    bars = {}
    for s in TP.CLASSIC5:
        a = D.load_asof(s, "4h")
        k = T7.frame(s)["k4"]
        cols = ["open_time", "open", "high", "low", "close"]
        same = (len(a) == len(k)
                and all(np.array_equal(a[c].to_numpy(), k[c].to_numpy())
                        for c in cols))
        if not same:
            _halt(f"{s}: the lab's 4h frame ({len(k)} bars) is not "
                  f"tierc10_data.load_asof ({len(a)} bars); a bar past the "
                  f"pin, or a different bar, would enter.")
        bars[s] = a
    P(f"as_of_last_closed_4h: {as_of}")
    P("=" * 78)
    P(f"RUN  TIER-C10 · CLOSE · P-AGE-1 (tide-youth) · {TIER}")
    P("=" * 78)
    P(f"  contract of record {CONTRACT.relative_to(ROOT)}:{CONTRACT_LINE_NO}"
      f" — {cline!r} (sha256 {csha[:16]} == PROGRESS contract_of_record)")
    P(f"  substrate {sub['substrate']} (loaders bound to the snapshot; the "
      f"live cache is refused on the path string) · "
      f"PYTHONDONTWRITEBYTECODE=1 · no registration, score or verdict read")
    P(f"  PROGRESS.as_of_of_record {as_of} · as_of_last_closed_4h_close_ms "
      f"{as_of_ms} · {AS_OF_PIN_REL} agrees")
    P(f"  book anchor {JOURNAL_REL} sha256 {jsha} == PROGRESS "
      f"'{PANEL_STAGE}' record")
    P(f"  corridor_n(CLASSIC5): lo {iso(lo)} · hi {iso(hi)} (hi+1 = "
      f"{iso(hi + 1)}) · last_closed_4h_close {meta['last_closed_4h_close']}"
      f" == as_of_of_record: HELD")
    P("  [spec note] the build spec's literal 'iso(hi) == as_of_of_record' "
      f"cannot hold: hi is the close minus 1 ms (iso(hi) = {iso(hi)}). The "
      "assertion taken is meta['last_closed_4h_close'] == as_of_of_record "
      "AND hi + 1 == as_of_last_closed_4h_close_ms.")
    P("  lab 4h frames == tierc10_data.load_asof bars, exact (open_time, "
      "OHLC): " + " · ".join(f"{s} {len(bars[s])}" for s in TP.CLASSIC5)
      + ": HELD")
    P(f"  definition: {definition_text()}")
    P("  HALT conditions: env not the snapshot · PYTHONDONTWRITEBYTECODE "
      "unset · PROGRESS as-of != AS_OF_PIN · contract sha != PROGRESS · "
      "contract line moved · journal sha != PANEL/gate · corridor != "
      "as_of_of_record · lab frame != load_asof · F-AGE-BOOK RED (the lab "
      "card is not the TC10 control) · output dir outside close/")
    return {"lo": lo, "hi": hi, "meta": meta, "as_of": as_of,
            "as_of_ms": as_of_ms, "contract_line": cline, "bars": bars,
            "substrate": sub["substrate"]}


# ═══════════════════════════════════ F-AGE-BOOK's rows (also a precondition)
def book_rows(book: list) -> pd.DataFrame:
    """The lab book's journal rows, filed the way control_journal was filed:
    T7.journal_frame, then write_table's _round_floats."""
    jf = TB._round_floats(T7.journal_frame(book))
    return (jf[list(BOOK_COLS)].sort_values(["asset", "entry_ms"],
                                             kind="mergesort")
            .reset_index(drop=True))


def filed_rows() -> pd.DataFrame:
    d = pd.read_parquet(CONTROL_JOURNAL)
    return (d[list(BOOK_COLS)].sort_values(["asset", "entry_ms"],
                                           kind="mergesort")
            .reset_index(drop=True))


def check_book(lab: pd.DataFrame, filed: pd.DataFrame) -> tuple[bool, list]:
    lines = []
    g_n = len(lab) == len(filed)
    lines.append(f"[{'OK ' if g_n else 'BAD'}] count: lab v6 book {len(lab)}"
                 f" · control_journal.parquet {len(filed)}")
    ok = g_n
    if g_n:
        for c in BOOK_COLS:
            eq = bool((lab[c].to_numpy() == filed[c].to_numpy()).all())
            n_bad = int((lab[c].to_numpy() != filed[c].to_numpy()).sum())
            ok &= eq
            extra = ""
            if c == "net_r":
                extra = (f" · worst |diff| "
                         f"{float(np.max(np.abs(lab[c].to_numpy() - filed[c].to_numpy()))):.3e}")
            lines.append(f"[{'OK ' if eq else 'BAD'}] {c}: exact on every "
                         f"row ({n_bad} differ){extra}")
    return ok, lines


# ═══════════════════════════════════ THE CAPTURE (pure recorders, proven inert)
def capture(lo: int, hi: int) -> dict:
    """Runs tc7g_tables a SECOND time with two pure recorders:
      · T9._trailing_edges records the edges the tagger computed at each
        entry-bar instant;
      · LR.regime_table / LR.candidates wrap the TRAILING tagger that
        tc7g_tables installed and record its per-campaign tag frame.
    Neither recorder changes a return value.  The frames of this spied call
    are held against the plain call's frames by content sha in build()."""
    rec: dict[int, list] = {}
    caps: list = []
    o_edges, o_rt, o_cd = T9._trailing_edges, LR.regime_table, LR.candidates

    def spy_edges(pool, at_ms):
        e = o_edges(pool, at_ms)
        rec.setdefault(int(at_ms), []).append(
            None if e["streak_bar"] is None
            else [float(x) for x in e["streak_bar"]])
        return e

    def wrap(fn):
        def w(lo_, hi_):
            inner = LR._tag_book            # the trailing tagger, installed
            def r(bk, cu):
                d = inner(bk, cu)
                caps.append((bk, d.copy()))
                return d
            LR._tag_book = r
            try:
                return fn(lo_, hi_)
            finally:
                LR._tag_book = inner
        return w

    T9._trailing_edges = spy_edges
    LR.regime_table, LR.candidates = wrap(o_rt), wrap(o_cd)
    try:
        frames, _ = T9.tc7g_tables(lo, hi)
    finally:
        T9._trailing_edges, LR.regime_table, LR.candidates = (o_edges, o_rt,
                                                               o_cd)
    v6 = LR.books(lo, hi)["v6"]
    tags = [d for bk, d in caps if bk is v6]
    if not tags:
        _halt("the recorder saw no v6 tag frame; the lab's call path moved.")
    for t in tags[1:]:
        if content_sha(t) != content_sha(tags[0]):
            _halt("the trailing tagger produced two different v6 tag "
                  "frames within one tc7g_tables call.")
    edges = {}
    for at, lst in rec.items():
        if any(x != lst[0] for x in lst):
            _halt(f"the tagger's edges at {iso(at)} differ between calls.")
        edges[at] = lst[0]
    return {"frames": frames, "tags": tags[0].reset_index(drop=True),
            "edges": edges, "book": v6}


# ═════════════════════════════════════════════════════════ THE COLLAR
def band_rows(df: pd.DataFrame) -> int:
    if "band" not in df.columns:
        return 0
    return int((df["band"].astype(str) != ALL_BAND).sum())


def banned_columns(cols) -> list:
    return sorted(c for c in cols
                  if c in BANNED_EXACT or BANNED_RX.search(str(c)))


def collar(df: pd.DataFrame) -> pd.DataFrame:
    d = df.copy()
    d["tier"] = TIER
    d["selection_not_a_result"] = SELECTION
    d["m_selections_this_table"] = band_rows(d)
    d["in_sample"] = True
    return d


# ═══════════════════════════════════════════════════════════════ BUILD
def shape(frames: dict, cap: dict, pre: dict) -> tuple[dict, dict]:
    """The three tables, selected, labelled, collared and stamped."""
    meta = pre["meta"]
    dropped = {}
    # ── TABLE 1 · the v6 book by tide-youth band, TRAILING edges
    cross = frames["tc7g_regime_cross_trailing"]
    y = cross[(cross["dimension"] == DIM) & (cross["card"] == CARD)].copy()
    want = [f"{b + 1:02d}" for b in range(len(LR.STREAK_LABELS))] + [ALL_BAND]
    if sorted(y["band"].astype(str)) != sorted(want):
        _halt(f"the v6 tide-streak cross is not whole: bands "
              f"{sorted(y['band'].astype(str))} != {want}")
    tg = cap["tags"]
    extra = []
    for b in y["band"].astype(str):
        sel = (tg["streak_band"].notna() if b == ALL_BAND
               else tg["streak_band"] == int(b) - 1)
        sub = tg.loc[sel]
        sb = sub["streak_bars"].to_numpy(float)
        extra.append({
            "n_left_censored": int(sub["left_censored"].sum()),
            "streak_bars_at_entry_min": (int(sb.min()) if len(sb) else None),
            "streak_bars_at_entry_median": (float(np.median(sb))
                                            if len(sb) else None),
            "streak_bars_at_entry_max": (int(sb.max()) if len(sb) else None),
        })
    y = pd.concat([y.reset_index(drop=True), pd.DataFrame(extra)], axis=1)
    y["d15_trio_label"] = D15_LABEL
    y["definition"] = definition_text()
    y["left_censored_note"] = (
        "a left-censored campaign sits in the one streak per asset already "
        "running at the warm floor; its age is a LOWER bound, so it can only "
        "be banded too YOUNG [the lab's law]")
    dropped[T_YOUTH] = banned_columns(y.columns)
    y = y.drop(columns=dropped[T_YOUTH])
    # ── TABLE 2 · the bar distribution (bar-pooled USED, episode-pooled not)
    bb = frames["tc7g_tide_streak_bands"].copy()
    hyb = [c for c in bb.columns if "hybrid" in c]
    bb = bb.drop(columns=hyb)
    bb["n_campaigns_v6_banding"] = (
        "WHOLE-CORRIDOR edges: the TC7 lab's original banding, which is "
        "look-ahead. This is a bar-distribution table. The campaign counts of "
        f"record are the TRAILING ones in {T_YOUTH}.")
    bb["definition"] = definition_text()
    dropped[T_BARS] = hyb + banned_columns(bb.columns)
    bb = bb.drop(columns=banned_columns(bb.columns))
    # ── TABLE 3 · the edge evolution (trailing vs whole corridor, per year)
    ed = frames["tc7g_edge_evolution"].copy()
    ed["what"] = (
        "trailing (causal) vs whole-corridor band edges at each year "
        "boundary: the measured look-ahead that the trailing banding removes. "
        f"The streak edges are bar-pooled STREAK_BAND_QUANTILES = "
        f"{tuple(LR.STREAK_BAND_QUANTILES)}. The vol_rel edges belong to "
        "the lab's other dimension and ride unchanged.")
    dropped[T_EDGES] = banned_columns(ed.columns)
    ed = ed.drop(columns=dropped[T_EDGES])
    out = {}
    for name, df in ((T_YOUTH, y), (T_BARS, bb), (T_EDGES, ed)):
        d = TP.stamp_n(collar(df), meta, "4h")
        d.attrs = {}
        d.columns = [str(c) for c in d.columns]
        out[name] = d
    return out, dropped


def _fmt(x, nd: int = 4, sign: bool = False) -> str:
    if x is None or (isinstance(x, float) and not np.isfinite(x)):
        return "—"
    if isinstance(x, (bool, np.bool_)):
        return "yes" if x else "no"
    if isinstance(x, (int, np.integer)):
        return str(int(x))
    if isinstance(x, (float, np.floating)):
        xf = float(x)
        if xf.is_integer() and nd == 0:
            return str(int(xf))
        return f"{xf:+.{nd}f}" if sign else f"{xf:.{nd}f}"
    if isinstance(x, (list, tuple, np.ndarray)):
        return "[" + ", ".join(_fmt(v, nd) for v in x) + "]"
    return str(x)


def render_md(tbl: dict, shas: dict, pre: dict, dropped: dict,
              prov: dict) -> str:
    """The build note.  Every number is read from the FILED tables (they are
    read back from parquet), and no wall clock appears [F-DET]."""
    y = tbl[T_YOUTH].sort_values("band").reset_index(drop=True)
    bb = tbl[T_BARS]
    ed = tbl[T_EDGES]
    allr = y[y["band"] == ALL_BAND].iloc[0]
    bands = y[y["band"] != ALL_BAND]
    m = {k: int(v["m_selections_this_table"].iloc[0]) for k, v in tbl.items()}
    L = []
    A = L.append
    A("# P-AGE-1 · tide-youth (Tier-E tables)")
    A("")
    A(f"**{TIER}.** A SELECTION, not a result. In-sample. P-AGE-1 has no "
      "registration, no verdict, no p, no CI and no BH bar. "
      f"m selections: {m[T_YOUTH]} ({T_YOUTH} band rows) · {m[T_BARS]} "
      f"({T_BARS} band rows) · {m[T_EDGES]} ({T_EDGES}, an edge table).")
    A("")
    A(f"Contract of record: `{CONTRACT.relative_to(ROOT)}:{CONTRACT_LINE_NO}`"
      f": \"{pre['contract_line']}\"")
    A("")
    A("## Definition (an executor reading, no new pin)")
    A("")
    A(definition_text())
    A("")
    A("Book: the v6 control, `tierc7_lab_regime.books(lo, hi)['v6']`. It "
      "equals `research_outputs/tierc10/panel/control_journal.parquet` "
      f"exactly on {', '.join(BOOK_COLS)} (F-AGE-BOOK).")
    A("")
    A("## Corridor and as-of")
    A("")
    A(f"- panel CLASSIC5 ({', '.join(TP.CLASSIC5)}), lens 4h")
    A(f"- corridor {allr['as_of_panel_start']} → {allr['as_of_last_closed_4h']}"
      f" ({_fmt(allr['as_of_span_days'], 1)} d), substrate "
      f"{allr['as_of_substrate']}")
    A(f"- as_of_last_closed_4h = {allr['as_of_last_closed_4h']}, which "
      f"equals PROGRESS.json as_of_of_record ({pre['as_of']})")
    A("")
    A(f"## Table 1: the v6 book by tide-youth band, TRAILING edges (`{T_YOUTH}.parquet`)")
    A("")
    A("| band | n | assets | net R | expectancy R | win % | max DD R | "
      "top-decile share % | best R | strip-best net R | share of card net "
      "R % | provisional | left-censored | streak bars at entry min / "
      "median / max |")
    A("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|:-:|---:|---:|")
    for r in list(bands.itertuples()) + [allr]:
        g = (lambda k: getattr(r, k) if not isinstance(r, pd.Series)
             else r[k])
        A(f"| {g('band_label')} | {_fmt(g('n'))} | {_fmt(g('n_assets'))} | "
          f"{_fmt(g('net_r'), 4, True)} | {_fmt(g('expectancy_r'), 4, True)}"
          f" | {_fmt(g('win_rate_pct'), 1)} | {_fmt(g('max_dd_r'), 4)} | "
          f"{_fmt(g('top_decile_share_pct'), 1)} | {_fmt(g('best_r'), 4)} | "
          f"{_fmt(g('strip_best_net_r'), 4, True)} | "
          f"{_fmt(g('share_of_card_net_r_pct'), 1)} | "
          f"{_fmt(bool(g('provisional')))} | {_fmt(g('n_left_censored'))} | "
          f"{_fmt(g('streak_bars_at_entry_min'))} / "
          f"{_fmt(g('streak_bars_at_entry_median'), 1)} / "
          f"{_fmt(g('streak_bars_at_entry_max'))} |")
    A("")
    A(f"`provisional` means n < RC.PROVISIONAL_MIN_N = {RC.PROVISIONAL_MIN_N}"
      " (the lineage's law). Band n's sum to "
      f"{_fmt(int(bands['n'].sum()))}; the ALL row holds {_fmt(allr['n'])} "
      "(F-AGE-WHOLE).")
    A("")
    A(f"**{D15_LABEL}**")
    A("")
    A("| band | paired_delta_expectancy_r | tail_exit_ratio | "
      "max_single_trade_delta_share |")
    A("|---|---:|---:|---:|")
    for r in list(bands.itertuples()) + [allr]:
        g = (lambda k: getattr(r, k) if not isinstance(r, pd.Series)
             else r[k])
        A(f"| {g('band_label')} | {_fmt(g('paired_delta_expectancy_r'))} | "
          f"{_fmt(g('tail_exit_ratio'))} | "
          f"{_fmt(g('max_single_trade_delta_share'))} |")
    A("")
    A("## Look-ahead size: campaign counts under trailing edges vs whole-corridor edges")
    A("")
    A("| band | n, TRAILING (of record) | n, WHOLE-CORRIDOR (TC7 original, "
      "look-ahead) |")
    A("|---|---:|---:|")
    used = bb[bb["basis_used"]].sort_values("band")
    for r in bands.itertuples():
        wc = used[used["band_label"] == r.band_label]["n_campaigns_v6"]
        A(f"| {r.band_label} | {_fmt(r.n)} | "
          f"{_fmt(int(wc.iloc[0]) if len(wc) else None)} |")
    A("")
    A(f"## Table 2: the bar distribution (`{T_BARS}.parquet`)")
    A("")
    A("| basis | band | edge lo (bars) | edge hi (bars) | units | unit | "
      "share % | median streak (bars) | median streak (days) | "
      "n v6 campaigns (whole-corridor edges) | left-censored |")
    A("|---|---|---:|---:|---:|---|---:|---:|---:|---:|---:|")
    for r in bb.sort_values(["basis_used", "band"],
                            ascending=[False, True]).itertuples():
        A(f"| {r.basis} | {r.band_label} | {_fmt(r.edge_lo_bars, 1)} | "
          f"{_fmt(r.edge_hi_bars, 1)} | {_fmt(r.n_units)} | {r.unit} | "
          f"{_fmt(r.unit_share_pct, 2)} | {_fmt(r.median_streak_bars, 1)} | "
          f"{_fmt(r.median_streak_days, 2)} | "
          f"{_fmt(r.n_campaigns_v6, 0)} | {_fmt(r.n_left_censored, 0)} |")
    A("")
    A(f"{bb['bar_vs_episode_note'].iloc[0]}")
    A("")
    A(f"Columns dropped: {dropped[T_BARS] or 'none'}. The hybrid is not "
      "printed.")
    A("")
    A(f"## Table 3: edge evolution (`{T_EDGES}.parquet`)")
    A("")
    A("| as of | streak edges, TRAILING | streak edges, WHOLE CORRIDOR | "
      "vol_rel edges, trailing | vol_rel edges, whole corridor |")
    A("|---|---|---|---|---|")
    for r in ed.sort_values("as_of").itertuples():
        A(f"| {r.as_of} | {_fmt(r.streak_edges_trailing, 1)} | "
          f"{_fmt(r.streak_edges_whole_corridor, 1)} | "
          f"{_fmt(r.vol_rel_edges_trailing, 6)} | "
          f"{_fmt(r.vol_rel_edges_whole_corridor, 6)} |")
    A("")
    A("## What these tables are not")
    A("")
    A("- They are not a registration, a score or a verdict. No p, CI or BH "
      "bar is computed, and no registration or its verdict was read.")
    A("- They are not a filter. No campaign is dropped, and every band is "
      "printed whole, including the provisional ones.")
    A("- They are not out of sample. The book, the bands and the edges all "
      "come from the same corridor.")
    A("- The lab's hybrid rows are not printed. Only card v6 is TC10's "
      "control.")
    A("- The dropped verdict/p/ci/clears_bh_bar columns: "
      + "; ".join(f"{k}: {v or 'none'}" for k, v in dropped.items()
                  if k != T_BARS)
      + f"; {T_BARS}: " + (", ".join(banned_columns(dropped[T_BARS]))
                           or "none") + ".")
    A("")
    A("## Provenance")
    A("")
    for k in (T_YOUTH, T_BARS, T_EDGES):
        A(f"- `{k}.parquet` content sha256 {shas[k]}, {len(tbl[k])} rows")
    for k, v in prov.items():
        A(f"- {k}: {v}")
    A("")
    return "\n".join(L)


def build(out: Path, pre: dict, P) -> dict:
    out = _guard_out(out)
    lo, hi = pre["lo"], pre["hi"]
    frames, _ = T9.tc7g_tables(lo, hi)                      # the plain call
    cap = capture(lo, hi)                                   # the spied call
    for k in sorted(frames):
        a, b = content_sha(frames[k]), content_sha(cap["frames"][k])
        if a != b:
            _halt(f"the recorders are not inert: {k} differs between the "
                  f"plain and the spied tc7g_tables call.")
    P(f"  tc7g_tables(lo, hi): {len(frames)} frames · recorders inert (all "
      f"{len(frames)} frames equal by content sha, plain vs spied)")
    tbls, dropped = shape(frames, cap, pre)
    out.mkdir(parents=True, exist_ok=True)
    shas = {}
    for name, df in tbls.items():
        shas[name] = TB.write_table(df, name, KEYS[name], out)
    back = {n: pd.read_parquet(out / f"{n}.parquet") for n in tbls}
    prov = {
        "control_journal.parquet sha256": sha_file(CONTROL_JOURNAL),
        "scripts/tierc7_lab_regime.py sha256":
            sha_file(ROOT / "scripts" / "tierc7_lab_regime.py"),
        "scripts/tierc9.py sha256": sha_file(ROOT / "scripts" / "tierc9.py"),
        "scripts/tierc10_panel.py sha256":
            sha_file(ROOT / "scripts" / "tierc10_panel.py"),
        f"scripts/{Path(__file__).name} sha256": sha_file(Path(__file__)),
    }
    md = render_md(back, shas, pre, dropped, prov)
    tmp = out / (MD_NAME + ".tmp")
    tmp.write_text(md, encoding="utf-8")
    os.replace(tmp, out / MD_NAME)
    for n in tbls:
        P(f"  wrote {n}.parquet rows={len(back[n])} content_sha={shas[n]}"
          f" · dropped {dropped[n] or 'none'}")
    P(f"  wrote {MD_NAME} sha256={sha_file(out / MD_NAME)}")
    return {"tbl": back, "shas": shas, "cap": cap, "dropped": dropped,
            "out": out}


# ═══════════════════════════════════════════════════════════ FIXTURE LEGS
def clean(s: str) -> str:
    """Repo paths print relative, so no machine path reaches the
    transcript."""
    return str(s).replace(str(ROOT) + "/", "")


def leg_substrate(C) -> tuple[bool, list]:
    """The RUN/HALT gate passes on the env handed to it, and, on the REAL
    env only, a subprocess with NAIAD_CACHE_DIR unset exits non-zero with a
    HALT and writes nothing."""
    lines = []
    _env_gate(C["env"])                   # HALTs (-> BAD) on a bad env
    lines.append(f"[OK ] RUN/HALT gate passes: NAIAD_CACHE_DIR -> "
                 f"{SNAPSHOT.name} · PYTHONDONTWRITEBYTECODE=1")
    ok = True
    if C["env"] is C["_real_env"]:
        d = DET_ROOT / "run_halt"
        if d.exists():
            shutil.rmtree(d)
        d.mkdir(parents=True)
        env = {k: v for k, v in os.environ.items() if k != "NAIAD_CACHE_DIR"}
        r = subprocess.run([sys.executable, str(Path(__file__)),
                            "--build-only", "--out", str(d)],
                           capture_output=True, text=True, env=env,
                           cwd=str(ROOT))
        wrote = sorted(x.name for x in d.iterdir())
        g = (r.returncode != 0 and "HALT: NAIAD_CACHE_DIR is unset"
             in (r.stdout + r.stderr) and not wrote)
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] a subprocess with "
                     f"NAIAD_CACHE_DIR unset: exit {r.returncode}, HALT "
                     f"printed, wrote {wrote or 'nothing'}")
        shutil.rmtree(d, ignore_errors=True)
    return ok, lines


def leg_book(C) -> tuple[bool, list]:
    return check_book(C["lab_rows"], C["filed_rows"])


def leg_whole(C) -> tuple[bool, list]:
    y = C["tbl"][T_YOUTH]
    tg = C["tags"]
    lines, ok = [], True
    want = {f"{b + 1:02d}": LR.STREAK_LABELS[b]
            for b in range(len(LR.STREAK_LABELS))}
    got = {r.band: r.band_label for r in y.itertuples() if r.band != ALL_BAND}
    g0 = got == want and int((y["band"] == ALL_BAND).sum()) == 1
    ok &= g0
    lines.append(f"[{'OK ' if g0 else 'BAD'}] grid whole: bands "
                 f"{sorted(got)} labelled from LR.STREAK_LABELS + one ALL row")
    parts = int(y.loc[y["band"] != ALL_BAND, "n"].sum())
    whole = int(y.loc[y["band"] == ALL_BAND, "n"].iloc[0])
    g1 = parts == whole
    ok &= g1
    lines.append(f"[{'OK ' if g1 else 'BAD'}] band n's sum {parts} == ALL "
                 f"row n {whole}")
    nj = len(C["filed_rows"])
    g2 = whole == nj
    ok &= g2
    lines.append(f"[{'OK ' if g2 else 'BAD'}] ALL row n {whole} == "
                 f"control_journal count {nj}")
    at = [int(C["om_of"][t.symbol][t.entry_i]) for t in C["book"]]
    warm = np.array([C["tagger_edges"].get(a) is not None for a in at])
    unb = tg["streak_band"].isna().to_numpy()
    n_uw = int((unb & warm).sum())
    g3 = n_uw == 0 and len(tg) == len(C["book"])
    ok &= g3
    lines.append(f"[{'OK ' if g3 else 'BAD'}] campaigns unbanded under warm "
                 f"edges: {n_uw} (of {len(tg)} tagged; {int(warm.sum())} "
                 f"with warm edges; {int(unb.sum())} unbanded in all)")
    mism = []
    for b in sorted(got):
        n_t = int(y.loc[y["band"] == b, "n"].iloc[0])
        n_c = int((tg["streak_band"] == int(b) - 1).sum())
        if n_t != n_c:
            mism.append(f"{b}: table {n_t} vs campaigns {n_c}")
    g4 = not mism
    ok &= g4
    per = ", ".join(f"{LR.STREAK_LABELS[int(b) - 1]} "
                    f"{int(y.loc[y['band'] == b, 'n'].iloc[0])}"
                    for b in sorted(got))
    lines.append(f"[{'OK ' if g4 else 'BAD'}] per-band table n == "
                 f"per-campaign tag count ({per})"
                 + (f"; MISMATCH {mism}" if mism else ""))
    return ok, lines


def indep_edges(C, at_ms: int, look_ms: int = 0):
    """Edges re-derived HERE from the pooled prefix open_ms <= at_ms: the
    pool is built from tierc10_data.load_asof stamps and the lab's
    tide_streak run.  It never reads T9._trailing_pool."""
    m = C["pool_t"] <= at_ms + look_ms
    if int(m.sum()) < RC.PROVISIONAL_MIN_N:
        return None
    return [float(x) for x in np.quantile(C["pool_v"][m],
                                          LR.STREAK_BAND_QUANTILES)]


def leg_causal(C) -> tuple[bool, list]:
    lines = []
    n_e = n_b = n_miss = n_at = 0
    worst = 0.0
    first_bad = None
    for k, t in enumerate(C["book"]):
        at = int(C["om_of"][t.symbol][t.entry_i])
        n_at += int(at != int(t.entry_ms))
        mine = indep_edges(C, at)
        if at not in C["tagger_edges"]:
            n_miss += 1
            first_bad = first_bad or f"{t.symbol} {iso(at)}: tagger has no edges"
            continue
        theirs = C["tagger_edges"][at]
        if mine != theirs:
            n_e += 1
            if mine is not None and theirs is not None:
                worst = max(worst, max(abs(a - b) for a, b in
                                       zip(mine, theirs)))
            first_bad = first_bad or (f"{t.symbol} {iso(at)}: re-derived "
                                      f"{mine} vs tagger {theirs}")
        run_i = int(C["run_of"][t.symbol][t.entry_i])
        band = (int(np.digitize(float(run_i), mine))
                if mine is not None and run_i > 0 else None)
        tb = C["tags"]["streak_band"].iloc[k]
        tb = None if pd.isna(tb) else int(tb)
        n_b += int(band != tb)
    n = len(C["book"])
    g1 = n_e == 0 and n_miss == 0
    lines.append(f"[{'OK ' if g1 else 'BAD'}] edges re-derived == "
                 f"tagger's on {n - n_e - n_miss}/{n} campaigns ({n_e} "
                 f"differ, {n_miss} missing, worst |diff| {worst:.3e})"
                 + (f"; first: {first_bad}" if first_bad else ""))
    g2 = n_b == 0
    lines.append(f"[{'OK ' if g2 else 'BAD'}] band re-derived "
                 f"(np.digitize(run at entry, re-derived edges)) == tagger's "
                 f"band on {n - n_b}/{n} campaigns")
    g3 = n_at == 0
    lines.append(f"[{'OK ' if g3 else 'BAD'}] entry bar open_ms (load_asof) "
                 f"== campaign entry_ms on {n - n_at}/{n}")
    mid = sorted(int(C['om_of'][t.symbol][t.entry_i]) for t in C["book"])
    mid = mid[len(mid) // 2]
    fut = int((C["pool_t"] > mid).sum())
    g4 = fut > 0
    lines.append(f"[{'OK ' if g4 else 'BAD'}] causality has teeth: at the "
                 f"median entry {iso(mid)} the prefix excludes {fut} future "
                 f"pooled bars of {len(C['pool_t'])}")
    return g1 and g2 and g3 and g4, lines


def leg_collar(C) -> tuple[bool, list]:
    lines, ok = [], True
    for name, df in C["tbl"].items():
        miss = [c for c in COLLAR_COLUMNS if c not in df.columns]
        bad = banned_columns(df.columns)
        g = not miss and not bad
        if g:
            nb = band_rows(df)
            g_t = bool((df["tier"] == TIER).all())
            g_s = bool((df["selection_not_a_result"].astype(str).str.len()
                        > 0).all() and df["selection_not_a_result"].notna().all())
            g_m = bool((df["m_selections_this_table"] == nb).all())
            g_i = bool((df["in_sample"] == True).all())         # noqa: E712
            g = g_t and g_s and g_m and g_i
            det = (f"tier {g_t} · selection {g_s} · m == {nb} band rows "
                   f"{g_m} · in_sample {g_i}")
        else:
            det = f"missing {miss} · banned present {bad}"
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] {name}: {len(df)} rows · "
                     f"{det}")
    return ok, lines


def leg_asof(C) -> tuple[bool, list]:
    lines, ok = [], True
    for name, df in C["tbl"].items():
        n_bad = int((df["as_of_last_closed_4h"] != C["as_of"]).sum())
        n_bar = int((df["as_of_last_closed_bar"] != C["as_of"]).sum())
        n_lens = int((df["as_of_lens"] != "4h").sum())
        n_pan = int((df["as_of_panel"] != "CLASSIC5").sum())
        n_sub = int((df["as_of_substrate"] != C["substrate"]).sum())
        g = n_bad == 0 and n_bar == 0 and n_lens == 0 and n_pan == 0 \
            and n_sub == 0
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] {name}: "
                     f"as_of_last_closed_4h != {C['as_of']} on {n_bad}/"
                     f"{len(df)} rows · last_closed_bar off {n_bar} · lens "
                     f"off {n_lens} · panel off {n_pan} · substrate off "
                     f"{n_sub}")
    return ok, lines


CLOCK_PATCH = (
    "import time as _t; _o = M.render_md; "
    "M.render_md = lambda *a, **k: _o(*a, **k) + "
    "'wall clock at run: %d\\n' % _t.time_ns()")


DET_HASHSEEDS = {"run_a": "1", "run_b": str(TP.SEED),
                 "run_b_sabotage": str(TP.SEED)}


def _det_run(tag: str, patch: str) -> tuple[bool, Path | None, str]:
    d = DET_ROOT / tag
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True)
    code = (f"import sys; sys.path.insert(0, {str(ROOT / 'scripts')!r}); "
            f"import {Path(__file__).stem} as M; {patch}; "
            f"sys.exit(M.main(['--build-only', '--out', {str(d)!r}]))")
    env = dict(os.environ, PYTHONHASHSEED=DET_HASHSEEDS[tag])
    r = subprocess.run([sys.executable, "-c", code], capture_output=True,
                       text=True, env=env, cwd=str(ROOT))
    tail = clean(" | ".join((r.stdout + r.stderr).strip().splitlines()[-2:]))
    return r.returncode == 0, Path(d), tail


def leg_det(C) -> tuple[bool, list]:
    lines = []
    if "det_a" not in C["_cache"]:
        C["_cache"]["det_a"] = _det_run("run_a", "pass")
    ok_a, da, ta = C["_cache"]["det_a"]
    patch = C.get("det_patch_b")
    ok_b, db, tb = _det_run("run_b_sabotage" if patch else "run_b",
                            patch or "pass")
    g0 = ok_a and ok_b
    lines.append(f"[{'OK ' if g0 else 'BAD'}] two subprocess --build-only "
                 f"runs exit 0 (A {ok_a} PYTHONHASHSEED="
                 f"{DET_HASHSEEDS['run_a']}, B {ok_b} PYTHONHASHSEED="
                 f"{DET_HASHSEEDS['run_b']})"
                 + ("" if g0 else f"; tail {ta or tb}"))
    ok = g0
    if g0:
        fa = sorted(p.name for p in da.iterdir())
        fb = sorted(p.name for p in db.iterdir())
        g1 = fa == fb == sorted(OUTPUT_FILES)
        ok &= g1
        lines.append(f"[{'OK ' if g1 else 'BAD'}] file sets equal and "
                     f"exactly the four outputs ({len(fa)} / {len(fb)})")
        for n in OUTPUT_FILES:
            if not ((da / n).exists() and (db / n).exists()):
                continue
            ba, bb_ = (da / n).read_bytes(), (db / n).read_bytes()
            bf = (C["out"] / n).read_bytes()
            g = ba == bb_ == bf
            ok &= g
            lines.append(f"[{'OK ' if g else 'BAD'}] {n}: bytes A==B "
                         f"{ba == bb_} · A==filed {ba == bf}"
                         f" (sha A {hashlib.sha256(ba).hexdigest()[:16]})")
    if patch:
        shutil.rmtree(db, ignore_errors=True)     # the sabotaged run only
    return ok, lines


# ── the sabotages (each returns a MUTATED COPY of the context)
def _cp(C, **kw):
    D_ = dict(C)
    D_.update(kw)
    return D_


def brk_env_unset(C):
    return _cp(C, env={k: v for k, v in C["env"].items()
                       if k != "NAIAD_CACHE_DIR"})


def brk_env_live(C):
    return _cp(C, env=dict(C["env"], NAIAD_CACHE_DIR=str(LIVE_CACHE)))


def brk_env_other(C):
    return _cp(C, env=dict(C["env"], NAIAD_CACHE_DIR=str(CLOSE_DIR)))


def brk_env_bytecode(C):
    return _cp(C, env={k: v for k, v in C["env"].items()
                       if k != "PYTHONDONTWRITEBYTECODE"})


def brk_book_drop(C):
    return _cp(C, lab_rows=C["lab_rows"].drop(index=len(C["lab_rows"]) // 2)
               .reset_index(drop=True))


def brk_book_nudge(C):
    d = C["lab_rows"].copy()
    d.loc[0, "net_r"] = d.loc[0, "net_r"] + 1e-6
    return _cp(C, lab_rows=d)


def brk_whole_relabel(C):
    tg = C["tags"].copy()
    k = int(np.flatnonzero((tg["streak_band"] == 0).to_numpy())[0])
    tg.loc[k, "streak_band"] = 1
    return _cp(C, tags=tg)


def brk_whole_unband(C):
    tg = C["tags"].copy()
    tg["streak_band"] = tg["streak_band"].astype("float")
    tg.loc[len(tg) - 1, "streak_band"] = np.nan
    return _cp(C, tags=tg)


def brk_causal_whole_corridor(C):
    wc = [float(x) for x in LR.cuts(C["lo"], C["hi"])["streak_bar"]]
    return _cp(C, tagger_edges={a: list(wc) for a in C["tagger_edges"]})


def brk_causal_one_bar(C):
    look = {a: indep_edges(C, a, MS_4H) for a in C["tagger_edges"]}
    return _cp(C, tagger_edges=look)


def brk_collar_verdict(C):
    tbl = dict(C["tbl"])
    d = tbl[T_YOUTH].copy()
    d["verdict"] = "SUPPORTED"
    tbl[T_YOUTH] = d
    return _cp(C, tbl=tbl)


def brk_collar_tier(C):
    tbl = dict(C["tbl"])
    d = tbl[T_BARS].copy()
    d.loc[0, "tier"] = ""
    tbl[T_BARS] = d
    return _cp(C, tbl=tbl)


def brk_asof_restamp(C):
    tbl = dict(C["tbl"])
    d = tbl[T_YOUTH].copy()
    d.loc[0, "as_of_last_closed_4h"] = iso(C["as_of_ms"] - MS_4H)
    tbl[T_YOUTH] = d
    return _cp(C, tbl=tbl)


def brk_det_clock(C):
    return _cp(C, det_patch_b=CLOCK_PATCH)


LEGS = [
    ("F-AGE-SUBSTRATE",
     "the RUN/HALT gate passes on an env that is not the frozen TC10 "
     "snapshot with PYTHONDONTWRITEBYTECODE=1, or a run with "
     "NAIAD_CACHE_DIR unset writes a byte (the forward strip's "
     "F-FS-SUBSTRATE, carried)",
     leg_substrate,
     [("NAIAD_CACHE_DIR unset", brk_env_unset),
      ("NAIAD_CACHE_DIR names the live cache (path string, never stat'ed)",
       brk_env_live),
      ("NAIAD_CACHE_DIR at a non-snapshot path", brk_env_other),
      ("PYTHONDONTWRITEBYTECODE unset", brk_env_bytecode)]),
    ("F-AGE-BOOK",
     "tierc7_lab_regime.books(lo,hi)['v6'] differs from research_outputs/"
     "tierc10/panel/control_journal.parquet in count or in any of (asset, "
     "entry_ms, direction, exit_ms, exit_reason, net_r), compared exactly",
     leg_book,
     [("drop one campaign from a copy", brk_book_drop),
      ("nudge one campaign's net_r by 1e-6 in a copy", brk_book_nudge)]),
    ("F-AGE-WHOLE",
     "the band n's do not sum to the ALL row's n, or that n differs from the "
     "journal count, or any campaign is unbanded under warm edges, or a "
     "band's table n differs from its per-campaign tag count",
     leg_whole,
     [("relabel one campaign's band (B1 -> B2) in a copy", brk_whole_relabel),
      ("unband one campaign under warm edges in a copy", brk_whole_unband)]),
    ("F-AGE-CAUSAL",
     "for some campaign, the edges re-derived from the pooled prefix "
     "(open_ms <= its entry bar) differ from the tagger's, or the re-derived "
     "band differs from the tagger's band",
     leg_causal,
     [("substitute the whole-corridor edges LR.cuts(lo,hi)['streak_bar']",
       brk_causal_whole_corridor),
      ("substitute edges that see ONE bar past the entry bar",
       brk_causal_one_bar)]),
    ("F-AGE-COLLAR",
     "a row lacks the Tier-E columns (tier, selection_not_a_result, "
     "m_selections_this_table == its table's band rows, in_sample) or "
     "carries verdict / clears_bh_bar / p_one_sided (or any p/ci column)",
     leg_collar,
     [("add 'verdict' to a copy of the tide-youth table", brk_collar_verdict),
      ("blank one row's tier in a copy of the bar-bands table",
       brk_collar_tier)]),
    ("F-AGE-ASOF",
     "any as_of_last_closed_4h != PROGRESS.as_of_of_record (or the lens/bar/"
     "panel/substrate stamps drift)",
     leg_asof,
     [("restamp one row one 4h bar earlier in a copy", brk_asof_restamp)]),
    ("F-DET",
     "two subprocess --build-only runs are not byte-identical to each other "
     "and to the filed outputs, file for file",
     leg_det,
     [("run B stamps the wall clock into the md", brk_det_clock)]),
]


def run_leg(fn, C) -> tuple[bool, list]:
    try:
        ok, lines = fn(C)
    except SystemExit as e:
        msg = clean(str(e))
        return False, [f"[BAD] {'' if msg.startswith('HALT') else 'HALT: '}"
                       f"{msg[:200]}"]
    except Exception as e:                                  # noqa: BLE001
        return False, [f"[BAD] {type(e).__name__}: {clean(str(e))[:200]}"]
    return bool(ok), [clean(x) for x in lines]


def fixtures(pre: dict, res: dict, lab_rows, frows, P) -> bool:
    cap = res["cap"]
    om_of, run_of, pv, pt = {}, {}, [], []
    lo, hi = pre["lo"], pre["hi"]
    for s in TP.CLASSIC5:
        om = pre["bars"][s]["open_time"].to_numpy(np.int64)
        run = np.asarray(LR.tide_streak(s)[1])
        if len(run) != len(om):
            _halt(f"{s}: tide_streak length {len(run)} != load_asof bars "
                  f"{len(om)}")
        om_of[s], run_of[s] = om, run
        m = (om >= lo) & (om <= hi) & (run > 0)
        pv.append(run[m])
        pt.append(om[m])
    pv, pt = np.concatenate(pv), np.concatenate(pt)
    o = np.argsort(pt, kind="mergesort")
    C = {"lab_rows": lab_rows, "filed_rows": frows, "tbl": res["tbl"],
         "tags": cap["tags"], "tagger_edges": cap["edges"],
         "book": cap["book"], "om_of": om_of, "run_of": run_of,
         "pool_v": pv[o], "pool_t": pt[o], "lo": lo, "hi": hi,
         "as_of": pre["as_of"], "as_of_ms": pre["as_of_ms"],
         "substrate": pre["substrate"], "out": res["out"], "_cache": {}}
    C["env"] = C["_real_env"] = dict(os.environ)
    n_pass = n_legs = n_red = n_breaks = 0
    failed = []
    for name, fails_if, fn, breaks in LEGS:
        n_legs += 1
        P("")
        P(f"── {name}")
        P(f"   FAILS IF: {fails_if}")
        ok, lines = run_leg(fn, C)
        for ln in lines:
            P(f"   {ln}")
        red_all = True
        for title, mk in breaks:
            n_breaks += 1
            bok, blines = run_leg(fn, mk(C))
            red = not bok
            n_red += red
            red_all &= red
            first_bad = re.sub(r"\b[0-9a-f]{16,64}\b", "<sha>", next(
                (x for x in blines if x.startswith("[BAD]")), ""))
            P(f"   [BREAK] {title} -> "
              + ("RED (correct): " + first_bad[:320] if red
                 else "GREEN — VOID: the leg did not see its sabotage"))
        leg_ok = ok and red_all
        n_pass += leg_ok
        if not leg_ok:
            failed.append(name)
        P(f"   {'PASS' if leg_ok else 'FAIL'} {name}")
    P("")
    P(f"FIXTURE SUMMARY  {n_pass}/{n_legs} PASS · {n_red}/{n_breaks} break "
      f"legs RED · failed {failed or []}")
    return n_pass == n_legs and n_red == n_breaks


# ═══════════════════════════════════════════════════════════════ MAIN
def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(CLOSE_DIR))
    ap.add_argument("--build-only", action="store_true")
    a = ap.parse_args(argv)
    out = _guard_out(Path(a.out))
    buf = io.StringIO()

    def P(s=""):
        buf.write(s + "\n")
        print(s, flush=True)

    pre = preamble(P)
    before = None if a.build_only else bytes_snapshot()
    # ═══ F-AGE-BOOK AS A PRECONDITION: nothing is written if it is RED
    lab_rows = book_rows(LR.books(pre["lo"], pre["hi"])["v6"])
    frows = filed_rows()
    ok, lines = check_book(lab_rows, frows)
    P("  F-AGE-BOOK precondition: " + ("HELD" if ok else "RED"))
    for ln in lines:
        P(f"    {ln}")
    if not ok:
        _halt("F-AGE-BOOK is RED on the real run: the lab card "
              "(tierc7_lab_regime.books(lo,hi)['v6']) is NOT the TC10 "
              "control (control_journal.parquet). Nothing is written.")
    res = build(out, pre, P)
    if a.build_only:
        return 0
    all_ok = fixtures(pre, res, lab_rows, frows, P)
    after = bytes_snapshot()
    moved = sorted(k for k in set(before) | set(after)
                   if before.get(k) != after.get(k))
    P(f"UNTOUCHED  {len(before)} protected files (scores/, registrations/, "
      f"REGISTRY*, PROGRESS.json, FIXTURES_RESUME.txt, the inputs) hashed "
      f"before and after: moved {moved or 'none'}")
    src = Path(__file__).read_text(encoding="utf-8")
    calls = re.findall(r"\b(?:TP|tierc10_panel)\.(?:score|finish_family|"
                       r"register|_mark_scored|require_arm)\s*\(", src)
    P(f"NOSCORE    static: calls of TP.score / finish_family / register / "
      f"_mark_scored / require_arm in this source: {len(calls)}")
    all_ok = all_ok and not moved and not calls
    P(f"RESULT {'GREEN' if all_ok else 'RED'} · outputs under "
      f"{out.relative_to(ROOT)}/ · {TIER}")
    tp = out / TRANSCRIPT_NAME
    tp.write_text(buf.getvalue(), encoding="utf-8")
    print(f"transcript {tp.relative_to(ROOT)} sha256={sha_file(tp)}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
