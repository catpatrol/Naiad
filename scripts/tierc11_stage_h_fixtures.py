#!/usr/bin/env python
"""TIER-C11 · STAGE H — F-TP · F-TP-EXPANSION · F-IDENTITY · F-ROW · F-GRID · F-KEY ·
F-DET.  The fixtures of scripts/tierc11_stage_h.py (the P-TP-RNG books) [LEANS
L-H.1, L-1.5, L-1.3, L-R.2; AM-6 (s2), AM-7].

TWO LEGS PER FIXTURE, the BREAK leg first, and it must go RED or the fixture is
VOID — a guard nobody has seen fail is a guard nobody has seen [the prove() law
of scripts/tierc10_rf_fixtures.py / tierc10_resume_fixtures.py].  A break leg is
a set of PLANTS judged one at a time; a plant counts as CAUGHT only if a finding
NAMES THE INTENDED DETECTOR (its expected substring).  A plant that crashes is a
FIXTURE DEFECT, never a catch.  Every plant is made on a COPY (a frame, a dict)
or under a MUTATION of the module (restored in `finally`) built into a scratch
`_det_stage_h/` directory OUTSIDE the repo; no artifact of record moves.

THE REFEREES ARE TYPED HERE (a second object, never the module's): the pin, the
approach 0.25 ATR, the 10 bps guard, ATR length 14, the frozen scale 3.0, the
harvest fraction 0.5, the taker 5.0 bps/side, the charter slippage tiers, the era
cut, the arms, the regbook column commission and dtypes, the grids' declared
cells, the collar, the exit reasons.  THE INDEPENDENT DERIVATION is this file's
own: the RAW 4h and 12h klines read from the TC11 snapshot with pandas; the
as-of 12h bar = the last raw 12h bar with open + 12h <= the 4h bar's open; its
box from the range machine run on the PREFIX of raw 12h bars ending at that bar
(tierc10_census.run_scale + asof_view on tape.head(k + 1) — the machine cannot
see a later bar); ATR_12h by a plain Wilder loop over the raw prefix; the level,
the near side (the raw prior 4h close), the guard, the touch and the fill price
by plain arithmetic; the v6 path (entry, exit bar and reason, harvest) from the
lineage's own v6 book (F-CTRL-proven, not the module under trial).

  F-TP          FAILS IF, for any of the four TP books (scored · tp_post_harvest
                · unguarded · frozen3), any campaign's first fillable bar by this
                file's derivation (12h as-of state IN_RANGE, level = top − 0.25
                ATR / bot + 0.25 ATR, prior raw close on the near side, level >
                10 bps beyond entry [not for 'unguarded'], harvest already fired
                [only 'post_harvest'], the bar reaches the level, not the v6 stop
                bar) is not the book's TP exit bar with fill max(level, open) /
                min(level, open), level, as-of 12h close, gross_r and fee_r
                (_account_chain's arithmetic, typed) exactly — or a book fills
                where no bar is fillable, or an unfilled campaign leaves v6's exit;
                or any TP fill row names a 12h bar closing AFTER the 4h open, a
                level inside 10 bps of entry (not 'unguarded'), a prior close not
                on the near side, a fill that is not max/min(level, open), a bar
                that never reached the level, or mfe outside [fill, v6 mfe]
                (AM-6 s2); or a TP row's funding_r (this file's walk of the RAW
                funding stamps, floored to the hour, over (entry, exit] at 1.0 /
                0.5 + 0.5 around the harvest, the D12 ceiling 1.0 R) or net_r
                (gross − fee − funding) differ; or any tp_bars row's as-of 12h
                close / level / flags differ from this file's; or the tp_fills
                TABLE is not the four books' TP exits, row for row, each column
                equal to this file's derivation (fill bar, as-of close <= the
                fill bar's open, level, fill, harvested, net_r, v6's net_r /
                exit / reason, Δ, bars saved, era, SCALE-IN-SAMPLE).  Three
                fills hand-walked bar by bar (at the 4h level).
                SABOTAGE: the module reading the 12h bar that CONTAINS the 4h
                open (closes after it — look-ahead); the module's scored arm
                without the entry-side guard; a copy with a TP fill whose level
                sits 5 bps beyond entry; a copy whose fill ignores a gap (fill =
                the open's other side); a copy with one TP row's funding bent
                (net kept consistent); a copy of tp_fills with a fill +1%; a
                copy of tp_fills whose as-of 12h close sits 12h later.
  F-TP-EXPANSION FAILS IF any bar of any v6 campaign (entry, v6 exit] is missing
                from tp_bars or extra in it (both scales); or on any bar whose 12h
                as-of state by the prefix run is BULL_EXP / BEAR_EXP / NONE, the
                module carries a level, a live order under any mode, a fill price,
                or another state name; or any TP book fills on such a bar.
                SABOTAGE: the module carrying the last live box (and IN_RANGE)
                through expansion bars (sticky box); a copy of tp_bars with a
                level planted on a BULL_EXP bar; the module carrying the box but
                not the state (its own L-H.1 assertion must HALT).
  F-IDENTITY    FAILS IF a paired arm's key set is not v6's, n != 200, a campaign
                the TP never filled differs from v6 in net_r / gross_r / fee_r /
                funding_r / exit_ms / exit_close_ms / exit_px / exit_reason by ANY
                amount, an entry field differs anywhere, a TP-acted campaign exits
                after v6 or on v6's stop bar, or the tuning / holdout slices do not
                partition the scored arm by the entry CLOSE against the typed cut;
                or the BASE arm differs from the lineage's own v6 book (B.v6_book,
                F-CTRL-proven, not the module) on any required column or exit_ms /
                exit_px / harvested, all 200 campaigns; or on any arm an exit bar
                is not on the RAW 4h grid, exit_close_ms != that raw bar's open +
                4h (its close), lies after the pin or not after the entry bar, or
                exit_stamp_ms breaks L-R.5; or a sidecar's identity counts are not
                ITS OWN parquet's (acted = TP exits, unacted = the rest).
                SABOTAGE (copies): an unacted net_r +1e-12; a key swapped; an
                acted exit moved past v6's; a holdout row in the tuning slice; the
                tuning slice's sidecar carrying the full arm's counts.
                (Mutations): one unacted campaign's net_r bent inside the module's
                ride — its own identity HALT must fire; the module's base net_r
                +0.25 R on BTCUSDT 2025-07-02T12:00Z (TP-acted in all four TP
                books, so no arm-vs-base check can see it), rebuilt; the module
                stamping every exit_close_ms at the exit bar's OPEN, rebuilt.
  F-ROW         FAILS IF the numbers of record differ from this file's: each
                arm's n / ΣR (fsum) / mean in the sidecar and the report row;
                the D15 tail ratio (top-decile MEAN ratio, k = floor(0.1 n)) and
                paired mean Δ on the scored row and every sidecar; haircut_net_r
                != net_r − fee_r × slip/5.0 with the TYPED charter tier on any row;
                era != the typed law on any row; the per-campaign TP order counts
                (live / guard-withheld / far side / pre-harvest / blocked by the
                stop) of the four TP arms or the report's withheld sentence; and
                EVERY STAGE TABLE re-derived by this file: SCALE-IN-SAMPLE (any
                calibrated read at a 4h open <= the typed cut among the bars the
                arm rode, a tuning pick typed from SCALE_PICKS.json; frozen 3.0
                never) on every regbook row, tp_bars row, tp_campaigns cell and
                the report's count; tp_summary (every cell, every statistic, from
                the regbooks); tp_picks and the regbooks' pick columns (from
                SCALE_PICKS.json); tp_withheld (every cell, every count, from this
                file's bars) with the unguarded twin's counts labelled
                WOULD-WITHHOLD (table, tp_campaigns column, sidecar, report);
                tp_reride (this file's own walk of replay9's admission over the
                lineage's candidates with this file's TP exits: the admitted set,
                the counts, ΣR = the scored arm's over it); tp_campaigns (every
                cell); tp_exit_reasons (every count).  SABOTAGE: a sidecar ΣR bent
                1e-9; the module's D15 read as a SUM tail; the module's haircut
                at slip/10; a copy with one era flipped; the module forcing
                scale_in_sample_12h False, rebuilt; copies with a tp_summary mean
                Δ bent 1e-9, a tp_picks pick bent, a guard_withheld_bars_touched
                +1, the unguarded row labelled 'withheld', a sum_net_r_reride
                bent 1e-9, a tp_campaigns net_r bent, an exit-reason count +1.
  F-GRID        FAILS IF a grid is not whole against its TYPED declared cells
                (TP.grid_whole), a stat is NaN without a nan_reason, n == 0
                carries a finite stat, the eras do not partition (full = tuning +
                holdout), ALL != Σ assets, a verdict column appears, a verdict
                WORD (typed: SUPPORTED, PASS, FAIL, ...) sits in any string cell of
                a stage table or a Tier-E regbook or any string of a Tier-E
                sidecar, or the collar is missing.  SABOTAGE: a cell dropped; an
                undeclared cell; a verdict column; the collar removed; a silent
                NaN; the partition broken; the module dropping the holdout era
                from its grid; a copy with 'NOT SUPPORTED' inside a tp_picks
                label cell.
  F-KEY         FAILS IF a regbook parquet lacks a typed required column or has
                another dtype, a null in one, a duplicated (symbol, entry_ms) or
                (symbol, entry_close_ms); a sidecar misses a typed key or carries
                another value, n / ΣR / book_sha256 (this file's canonical CSV)
                differ; a Tier-E arm lacks the collar or a registered arm carries
                it; the as-of stamps are absent; STATUS.json is not the typed
                record; a file set is not the typed one; a stage table's typed key
                repeats, a manifest content sha is not the table's, or a manifest
                file_sha256 is not the sha256 of the file's BYTES.  SABOTAGE
                (copies): a duplicated row; a null net_r; direction as float; a
                required column dropped; a sidecar sha bent; a Tier-E collar
                removed; STATUS missing an arm; a manifest byte sha bent.
                (Mutation): the module's REQ_COLS without 'lane'.
  F-DET         FAILS IF two subprocess builds (PYTHONHASHSEED 1, 20260924) differ
                from each other or from the canonical files (stage_h/ and
                regbooks/P-TP-RNG/) in the file set, any byte or any parquet
                content sha, or either exits nonzero.  SABOTAGE: one byte bent in
                a copy; a parquet copy with one float moved; a hash-order-
                dependent line under the two seeds.  (AM-2: every parquet read
                and write here goes through pandas on a PATH STRING — bytes held
                in memory land in a scratch file first.)
REPAIR (stage-H verifier report): the base arm refereed against the lineage v6
book; exit_close_ms refereed on the raw grid; every stage table and the
SCALE-IN-SAMPLE flag re-derived; verdict words scanned in cells; the slice
sidecars' identity counts and the would-withhold label typed; the manifest's
byte shas checked; parquet I/O on path strings only.
BANNED: self-comparison; one example where cardinality was possible; a tuned
magnitude bound standing in for an identity; a check whose claim is not the
design's claim.  FROZEN SUBSTRATE: HALTs unless NAIAD_CACHE_DIR is the TC11
snapshot (tierc11_env's guard).  Seed 20260924.  The transcript carries no clock
and no temp path.

Run:  export NAIAD_CACHE_DIR=$HOME/.cache/naiad/snapshots/tc11_20260925 PYTHONDONTWRITEBYTECODE=1
      ~/venvs/naiad/bin/python -B scripts/tierc11_stage_h.py            # the canonical build first
      ~/venvs/naiad/bin/python -B scripts/tierc11_stage_h_fixtures.py \\
          [leg-substring ...] [--refile-transcript] [--root=DIR]
      --root=DIR redirects the transcript AND the F-DET twins (DIR/_det_stage_h/).
Exit 0 = every leg GREEN, every break RED · 1 = a RED or VOID fixture, a
transcript finding, or a HALT.
"""
from __future__ import annotations

import contextlib
import copy
import hashlib
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
import tierc11_stage_h as S                                          # noqa: E402  (guards first)

import numpy as np                                                   # noqa: E402
import pandas as pd                                                  # noqa: E402

E, N, RD, B = S.E, S.N, S.RD, S.B
TP, T9, TB = E.TP, E.T9, E.TB
iso = TB.iso

# ── FIXTURE-TYPED LITERALS: the commission, a second object, never S's own ──
TC11_SNAP = Path.home() / ".cache" / "naiad" / "snapshots" / "tc11_20260925"
PIN = 1790294400000                      # 2026-09-25T00:00:00Z [L-0.1]
MS4H, MS12H = 14_400_000, 43_200_000
SEED = 20260924
DET_SEEDS = (1, SEED)
AS_OF_LINE = "as_of_last_closed_4h: 2026-09-25T00:00:00Z"
CLASSIC5_TYPED = ("BTCUSDT", "ETHUSDT", "SOLUSDT", "NEARUSDT", "ZECUSDT")
APPROACH_TYPED = 0.25                    # "the approach (0.25 ATR)"
GUARD_BPS_TYPED = 10.0                   # L-H.1 (ii): the round-trip taker fee
ATR_LEN_TYPED = 14                       # L-R.1
FROZEN_TYPED = 3.0
HARVEST_FRAC_TYPED = 0.5                 # v6's band harvest, 50%
TAKER_BPS_TYPED = 5.0                    # L-1.1
SLIP_TYPED = {"BTCUSDT": ("A", 2.0), "ETHUSDT": ("A", 2.0), "SOLUSDT": ("B", 5.0),
              "NEARUSDT": ("B", 5.0), "ZECUSDT": ("B", 5.0)}      # AM-7 charter tiers
ERA_CUT_TYPED = 1_719_791_999_000        # L-1.3: tuning closes <= 2024-06-30T23:59:59Z
N_V6_TYPED = 200
STATE_NAME_TYPED = {0: "NONE", 1: "BULL_EXP", -1: "BEAR_EXP"}
TP_BOOKS_TYPED = {"scored": ("calibrated", "record"),
                  "tierE__tp_post_harvest": ("calibrated", "post_harvest"),
                  "tierE__unguarded": ("calibrated", "unguarded"),
                  "tierE__frozen3": ("frozen3.0", "record")}
ARMS_TYPED = {"scored": ("scored", "full"), "base": ("base", "full"),
              "tierE__tp_post_harvest": ("tierE", "full"), "tierE__unguarded": ("tierE", "full"),
              "tierE__frozen3": ("tierE", "full"), "tierE__tuning": ("tierE", "tuning"),
              "tierE__holdout": ("tierE", "holdout")}
REQ_TYPED = {"symbol": "object", "entry_ms": "int64", "entry_close_ms": "int64",
             "direction": "int8", "entry_px": "float64", "stop_px": "float64",
             "r_dist": "float64", "exit_close_ms": "int64", "exit_reason": "object",
             "net_r": "float64", "gross_r": "float64", "fee_r": "float64",
             "funding_r": "float64", "haircut_net_r": "float64", "era": "object",
             "lane": "object"}
REQ_FLOAT_T = ("entry_px", "stop_px", "r_dist", "net_r", "gross_r", "fee_r", "funding_r",
               "haircut_net_r")
SIDE_KEYS_TYPED = ("registration", "arm", "kind", "ruler", "panel", "era_scope", "n",
                   "sum_net_r", "book_sha256", "description", "source_script")
COLLAR_TYPED = {"tier": "TIER-E", "selection_not_a_result": "a SELECTION, not a result",
                "gates": "nothing"}
AS_OF_TYPED = ("as_of_last_closed_4h", "as_of_panel_start", "as_of_span_days", "warranty",
               "as_of_lens", "as_of_last_closed_bar", "as_of_panel", "as_of_n_assets",
               "as_of_substrate")
EXIT_REASONS_TYPED = ("stop", "bell_12_89", "bell_89_316", "tp", "corridor_end")
BOOKS_GRID_TYPED = ("base", "scored", "tp_post_harvest", "unguarded", "frozen3")
TPBOOKS_GRID_TYPED = ("scored", "tp_post_harvest", "unguarded", "frozen3")
ERAS_TYPED = ("full", "tuning", "holdout")
ASSETS_ALL_TYPED = CLASSIC5_TYPED + ("ALL",)
VERDICT_COLUMNS_TYPED = ("verdict", "verdict_of_record", "clears_bh_bar", "promotable",
                         "scored_in_family", "p_one_sided", "supported")
# verdict WORDS inside string cells (L-1.4: a non-registered table carries none)
VERDICT_WORDS_RX = re.compile(r"\b(SUPPORTED|PASS(?:ED|ES)?|FAIL(?:ED|S)?|PROMOTED|REFUTED)\b")
FUNDING_CEIL_TYPED = 1.0                 # D12: the chain's funding capped at +1.0 R (card v6)
RAIL_TYPED = 1.0                         # SR-H6: struct_stop_4h railed 1.0 ATR (card v6)
MS1H = 3_600_000
BASE_BENT_KEY = ("BTCUSDT", 1751457600000)   # TP-acted in all four TP books (verifier)
GRID_BOOK_OF_ARM = {"scored": "scored", "tierE__tp_post_harvest": "tp_post_harvest",
                    "tierE__unguarded": "unguarded", "tierE__frozen3": "frozen3"}
WOULD_WITHHOLD_TYPED = "would-withhold"  # the unguarded twin's guard-count label (prefix)
WITHHELD_TYPED = "withheld"              # the guarded books' label (exact)
STAGE_KEYS_TYPED = {"tp_campaigns": ["symbol", "entry_ms"],
                    "tp_bars": ["scale_kind", "symbol", "entry_ms", "bar_open_ms"],
                    "tp_fills": ["book", "symbol", "entry_ms"], "tp_summary": ["cell"],
                    "tp_withheld": ["cell"], "tp_exit_reasons": ["cell"],
                    "tp_reride": ["asset"], "tp_picks": ["asset"]}
STAGE_FILES_TYPED = tuple(sorted([f"{n}.parquet" for n in STAGE_KEYS_TYPED]
                                 + ["STAGE_H.md", "STAGE_H_MANIFEST.json"]))
REG_FILES_TYPED = tuple(sorted([f"{a}.{x}" for a in ARMS_TYPED for x in ("parquet", "json")]
                               + ["STATUS.json"]))
REG_ID_TYPED = "P-TP-RNG"
SOURCE_TYPED = "scripts/tierc11_stage_h.py"

OUT = S.OUT
REGBOOKS = S.REGBOOKS
DET_NAME = S.DET_ROOT.name                # '_det_stage_h'
RUN_ROOT = OUT
TRANSCRIPT = "FIXTURES_STAGE_H.txt"
PY = sys.executable
LINES: list[str] = []
PASSED: list[str] = []
FAILED: list[str] = []
_TMP_RX = re.compile(r"(/private)?/(var/folders|tmp)/[^\s'\"]+")


def say(line: str = "") -> None:            # deterministic -> transcript
    line = _TMP_RX.sub("<tmp>", line)
    print(line)
    LINES.append(line)


def clock(line: str) -> None:               # wall clock, temp paths -> stdout ONLY
    print(f"  [clock · stdout only] {line}")


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def prove(fid: str, title: str, fails_if: str, break_leg, real_leg) -> None:
    """Break first; it must go RED (ok False) or the fixture is VOID."""
    say(f"\n{fid} — {title}")
    say(f"  FAILS IF: {fails_if}")
    try:
        b_ok, b_why = break_leg()
    except BaseException as e:              # a break leg that errors proved nothing
        if isinstance(e, KeyboardInterrupt):
            raise
        b_ok, b_why = True, f"break leg RAISED {type(e).__name__}: {e}"
    say(f"  [BREAK] deliberate violation -> "
        f"{'RED (correct)' if not b_ok else 'GREEN (FIXTURE IS VOID)'}: {b_why}")
    try:
        r_ok, r_why = real_leg()
    except SystemExit as e:                 # a HALT in the real leg is a FAIL
        r_ok, r_why = False, f"HALT {e}"
    except Exception as e:                  # a real leg that errors is a FAIL
        r_ok, r_why = False, f"raised {type(e).__name__}: {e}"
    say(f"  [{'PASS' if r_ok else 'FAIL'}] {fid}: {r_why}")
    if b_ok:
        FAILED.append(f"{fid} (break leg did not go RED — fixture proves nothing)")
    elif not r_ok:
        FAILED.append(fid)
    else:
        PASSED.append(fid)


def plants(rows) -> tuple[bool, str]:
    """rows = (name, expected detector substring, thunk -> list of findings).
    Judged ONE AT A TIME.  CAUGHT only if a finding names the intended detector.
    No finding = the plant PASSED (VOID); a finding without the substring = the
    WRONG detector (VOID); a crash = a FIXTURE DEFECT (VOID).  A SystemExit (a
    module HALT) is a finding."""
    passed, wrong, caught, crashed = [], [], [], []
    for name, want, thunk in rows:
        try:
            found = thunk()
        except SystemExit as e:
            found = [f"HALT: {e}"]
        except Exception as e:
            crashed.append(f"{name} -> RAISED {type(e).__name__}: {e}")
            continue
        if not found:
            passed.append(name)
        elif not any(want in str(f) for f in found):
            wrong.append(f"{name} -> {str(found[0])[:160]} (wanted {want!r})")
        else:
            hit = next(str(f) for f in found if want in str(f))
            i = hit.index(want)
            shown = hit[:190] if i + len(want) <= 190 else (hit[:60] + " … " + hit[i:i + 160])
            caught.append(f"{name} -> {shown}")
    if crashed:
        return True, (f"{len(crashed)} plant(s) CRASHED — a FIXTURE DEFECT, not a "
                      f"finding: " + " · ".join(crashed))
    if passed or wrong:
        return True, (f"{len(passed)} plant(s) PASSED {passed}; {len(wrong)} caught by the "
                      f"WRONG detector {wrong}")
    return False, (f"all {len(caught)} plants caught by their named detector, one at a "
                   f"time: " + " · ".join(caught))


@contextlib.contextmanager
def mutated(*muts):
    """MUTATIONS of the module under trial [(obj, name, value), ...], restored in
    `finally`.  (No mutation here touches the range facts, so their memo stands.)"""
    olds = [(o, n, getattr(o, n)) for o, n, _ in muts]
    for o, n, v in muts:
        setattr(o, n, v)
    try:
        yield
    finally:
        for o, n, v in reversed(olds):
            setattr(o, n, v)


def py(x):
    """A numpy scalar as its Python value (so a finding prints 1.5, not np.float64(1.5))."""
    return x.item() if hasattr(x, "item") else x


def _env() -> dict:
    return dict(os.environ, NAIAD_CACHE_DIR=str(TC11_SNAP), PYTHONDONTWRITEBYTECODE="1")


# ═══════════════════════════════════════════════════ THE WRITTEN BUNDLE (a copy)
def load_bundle(sdir: Path, rdir: Path) -> dict:
    reg = {}
    for a in ARMS_TYPED:
        p, j = rdir / f"{a}.parquet", rdir / f"{a}.json"
        reg[a] = (pd.read_parquet(str(p)) if p.exists() else None,
                  json.loads(j.read_text(encoding="utf-8")) if j.exists() else None)
    st = rdir / "STATUS.json"
    stage = {n: (pd.read_parquet(str(sdir / f"{n}.parquet"))
                 if (sdir / f"{n}.parquet").exists() else None) for n in STAGE_KEYS_TYPED}
    md = (sdir / "STAGE_H.md").read_text(encoding="utf-8") if (sdir / "STAGE_H.md").exists() \
        else ""
    man = (json.loads((sdir / "STAGE_H_MANIFEST.json").read_text(encoding="utf-8"))
           if (sdir / "STAGE_H_MANIFEST.json").exists() else {})
    fsha = {}
    for pre, d in (("stage_h", sdir), ("regbooks", rdir)):
        if d.exists():
            for f in sorted(d.iterdir()):
                if f.is_file() and not f.name.startswith("FIXTURES_STAGE_H"):
                    fsha[f"{pre}/{f.name}"] = sha_bytes(f.read_bytes())
    return {"reg": reg, "status": (json.loads(st.read_text(encoding="utf-8"))
                                   if st.exists() else None),
            "stage": stage, "md": md, "manifest": man, "file_sha": fsha,
            "files_stage": sorted(p.name for p in sdir.iterdir() if p.is_file()
                                  and not p.name.startswith("FIXTURES_STAGE_H"))
            if sdir.exists() else [],
            "files_reg": sorted(p.name for p in rdir.iterdir() if p.is_file())
            if rdir.exists() else []}


_CANON: dict = {}


def canon() -> dict:
    if not _CANON:
        _CANON.update(load_bundle(OUT, REGBOOKS))
    return _CANON


def bcopy(bd: dict) -> dict:
    return {"reg": {a: (None if df is None else df.copy(), copy.deepcopy(sd))
                    for a, (df, sd) in bd["reg"].items()},
            "status": copy.deepcopy(bd["status"]),
            "stage": {n: (None if df is None else df.copy()) for n, df in bd["stage"].items()},
            "md": bd["md"], "manifest": copy.deepcopy(bd["manifest"]),
            "file_sha": dict(bd["file_sha"]),
            "files_stage": list(bd["files_stage"]), "files_reg": list(bd["files_reg"])}


@contextlib.contextmanager
def scratch_build(name: str, *muts):
    """S.build into <tmp>/_det_stage_h/<name> (outside the repo) under MUTATIONS;
    yields the written bundle; the scratch is removed."""
    td = tempfile.mkdtemp(prefix="f-sh-")
    try:
        d = Path(td) / DET_NAME / name
        with mutated(*muts):
            S.build(d)
        yield load_bundle(d / "stage_h", d / "regbooks" / REG_ID_TYPED)
    finally:
        shutil.rmtree(td, ignore_errors=True)


# ═══════════════════════════════════════ INDEPENDENT DERIVATIONS (this file's)
_REF: dict = {}


def raw(sym: str, lens: str) -> dict:
    """The raw closed klines (open_time + step <= PIN), read with pandas."""
    step = MS4H if lens == "4h" else MS12H
    df = pd.read_parquet(str(TC11_SNAP / "klines" / f"{sym}_{lens}.parquet"))
    df = df.sort_values("open_time", kind="mergesort").reset_index(drop=True)
    df = df[df["open_time"].to_numpy(np.int64) + step <= PIN].reset_index(drop=True)
    return {"t": df["open_time"].to_numpy(np.int64), "o": df["open"].to_numpy(float),
            "h": df["high"].to_numpy(float), "l": df["low"].to_numpy(float),
            "c": df["close"].to_numpy(float)}


def atr_loop(h, l, c, n: int = ATR_LEN_TYPED) -> np.ndarray:
    """Wilder's ATR by a plain loop: TR[0] = h − l; RMA seeded at TR[0]."""
    out = np.empty(len(c))
    prev = 0.0
    for i in range(len(c)):
        if i == 0:
            tr = float(h[0] - l[0])
            prev = tr
        else:
            tr = max(float(h[i] - l[i]), abs(float(h[i] - c[i - 1])),
                     abs(float(l[i] - c[i - 1])))
            prev = prev + (1.0 / n) * (tr - prev)
        out[i] = prev
    return out


def pick_cell_typed(sym: str) -> dict:
    """The filed 12h cell of record, read from SCALE_PICKS.json by this file."""
    rec = json.loads((E.OUT / "ranges" / "SCALE_PICKS.json").read_text(encoding="utf-8"))
    return dict(next(c for c in rec["cells"] if c["asset"] == sym and c["lens"] == "12h"))


def pick_typed(sym: str, kind: str) -> float:
    """The filed 12h pick of record, read from SCALE_PICKS.json by this file."""
    if kind == "frozen3.0":
        return FROZEN_TYPED
    return float(pick_cell_typed(sym)["pick_of_record"])


def era_typed(entry_close_ms: int) -> str:
    """L-1.3, typed: tuning iff the entry CLOSE <= the typed cut."""
    return "tuning" if int(entry_close_ms) <= ERA_CUT_TYPED else "holdout"


def insample_typed(kind: str, sym: str, read_opens) -> bool:
    """L-R.2 SCALE-IN-SAMPLE, typed: a calibrated read (a TUNING pick) at a 4h open
    <= the typed cut is in-sample; frozen 3.0 never.  A whole-tape fallback is not
    typed here (none exists on the 12h CLASSIC5 cells) — the referee HALTS."""
    if kind == "frozen3.0":
        return False
    if pick_cell_typed(sym)["pick_window"] != "tuning":
        raise SystemExit(f"HALT: {sym} 12h is not a tuning pick — this referee is not typed "
                         f"for a fallback")
    return any(int(o) <= ERA_CUT_TYPED for o in read_opens)


def ref() -> dict:
    """The fixture's reference: raw tapes, the v6 path, the 12h tapes (checked
    equal to the raw bars), the plain-loop ATR."""
    if _REF:
        return _REF
    lo, hi, _ = B.corridor()
    v6 = B.v6_book(lo, hi)
    R = {"v6": {(t.symbol, int(t.entry_ms)): t for t in v6}, "raw4": {}, "raw12": {},
         "atr12": {}, "tape12": {}, "box": {}, "bars": {}, "exp": {}, "fund": {}}
    for s in CLASSIC5_TYPED:
        fd = pd.read_parquet(str(TC11_SNAP / "funding" / f"{s}.parquet"))
        fu: dict = {}                      # the raw stamps floored to the hour, summed
        for ft, fr in zip(fd["funding_time"].to_numpy(np.int64),
                          fd["funding_rate"].to_numpy(float)):
            k_ = int(ft) // MS1H * MS1H
            fu[k_] = fu.get(k_, 0.0) + float(fr)
        R["fund"][s] = fu
        r4, r12 = raw(s, "4h"), raw(s, "12h")
        R["raw4"][s], R["raw12"][s] = r4, r12
        R["atr12"][s] = atr_loop(r12["h"], r12["l"], r12["c"])
        tp12 = N.load11(s, "12h")
        for k_, a in (("t", tp12.t0), ("o", tp12.o), ("h", tp12.h), ("l", tp12.l),
                      ("c", tp12.c)):
            if not np.array_equal(np.asarray(a), r12[k_]):
                raise SystemExit(f"HALT: {s} 12h tape {k_} != the raw snapshot bars")
        if not np.array_equal(np.asarray(tp12.atr), R["atr12"][s]):
            raise SystemExit(f"HALT: {s} 12h ATR != this file's plain Wilder loop")
        R["tape12"][s] = tp12
    _REF.update(R)
    return _REF


def box_at(sym: str, kind: str, k: int) -> tuple:
    """(in_range, top, bot, state) of 12h bar k from the machine run on the PREFIX
    of raw 12h bars 0..k (it cannot see bar k + 1)."""
    R = ref()
    key = (sym, kind, int(k))
    if key not in R["box"]:
        pre = R["tape12"][sym].head(int(k) + 1)
        v2 = N.C.run_scale(pre, pick_typed(sym, kind))
        vw = N.C.asof_view(pre, v2["macro"], v2["leash"])
        R["box"][key] = (bool(vw["in_range"][k]), float(vw["top"][k]), float(vw["bot"][k]),
                         int(vw["state"][k]))
    return R["box"][key]


def exp_bars(kind: str) -> dict:
    """Every bar of every v6 campaign (entry, v6 exit], this file's derivation:
    {(sym, entry_ms): [bar dicts in order]}."""
    R = ref()
    if kind in R["bars"]:
        return R["bars"][kind]
    out = {}
    g = GUARD_BPS_TYPED / 10_000.0
    for key, t in R["v6"].items():
        s, d, e = t.symbol, int(t.direction), float(t.entry_px)
        r4, r12 = R["raw4"][s], R["raw12"][s]
        ja = int(np.searchsorted(r4["t"], int(t.entry_ms)))
        jb = int(np.searchsorted(r4["t"], int(t.exit_ms)))
        if r4["t"][ja] != int(t.entry_ms) or r4["t"][jb] != int(t.exit_ms):
            raise SystemExit(f"HALT: {key}: the v6 entry/exit bar is not on the raw 4h grid")
        close12 = r12["t"] + MS12H
        rows = []
        for j in range(ja + 1, jb + 1):
            o4 = int(r4["t"][j])
            k = int(np.searchsorted(close12, o4, side="right")) - 1
            if k >= 0:
                inr, top, bot, st = box_at(s, kind, k)
                atr = float(R["atr12"][s][k])
                asof = int(close12[k])
            else:
                inr, top, bot, st, atr, asof = False, np.nan, np.nan, 0, np.nan, -1
            state = "IN_RANGE" if inr else STATE_NAME_TYPED[st]
            lvl = ((top - APPROACH_TYPED * atr) if d == 1 else (bot + APPROACH_TYPED * atr)) \
                if inr else float("nan")
            prior = float(r4["c"][j - 1])
            fin = bool(np.isfinite(lvl))
            near = fin and (lvl - prior) * d > 0.0
            guard = fin and (lvl - e) * d > g * e
            touched = fin and ((float(r4["h"][j]) >= lvl) if d == 1 else (float(r4["l"][j]) <= lvl))
            fill = ((max(lvl, float(r4["o"][j])) if d == 1 else min(lvl, float(r4["o"][j])))
                    if touched else float("nan"))
            hb = t.harvest_ms is not None and int(t.harvest_ms) < o4
            rows.append({"j": j, "open": o4, "asof": asof, "k": k, "state": state, "inr": inr,
                         "top": top, "bot": bot, "atr": atr, "level": lvl, "prior": prior,
                         "near": near, "guard": guard, "touched": touched, "fill": fill,
                         "hb": hb, "stop_bar": (j == jb and t.exit_reason == "stop"),
                         "o4": float(r4["o"][j]), "h4": float(r4["h"][j]),
                         "l4": float(r4["l"][j])})
        out[key] = rows
    R["bars"][kind] = out
    return out


def live_of(b: dict, mode: str) -> bool:
    if mode == "record":
        return b["near"] and b["guard"]
    if mode == "post_harvest":
        return b["near"] and b["guard"] and b["hb"]
    if mode == "unguarded":
        return b["near"]
    raise SystemExit(f"HALT: mode {mode!r}")


def expected(kind: str, mode: str) -> dict:
    """{key: the first fillable bar dict, or None} under the reading."""
    R = ref()
    kk = (kind, mode)
    if kk not in R["exp"]:
        R["exp"][kk] = {key: next((b for b in rows if live_of(b, mode) and b["touched"]
                                   and not b["stop_bar"]), None)
                        for key, rows in exp_bars(kind).items()}
    return R["exp"][kk]


def hand_funding(t, xj: int, harvested: bool) -> float:
    """_account_chain's funding_r for a one-leg campaign exiting at raw 4h bar xj,
    typed: Σ rate × prior raw close × d × qty over bars (entry, exit] whose open
    carries a raw funding stamp (floored to the hour); qty 1.0, or 0.5 to the
    harvest bar and 0.5 to the exit; ÷ R; the D12 ceiling 1.0 R."""
    R = ref()
    s, d = t.symbol, int(t.direction)
    r4, fu = R["raw4"][s], R["fund"][s]
    ja = int(np.searchsorted(r4["t"], int(t.entry_ms)))

    def leg(jb: int, qty: float) -> float:
        acc = 0.0
        for j in range(ja + 1, jb + 1):
            rate = fu.get(int(r4["t"][j]))
            if rate:
                acc += rate * float(r4["c"][j - 1]) * d * qty
        return acc
    if harvested:
        hj = int(np.searchsorted(r4["t"], int(t.harvest_ms)))
        if int(r4["t"][hj]) != int(t.harvest_ms):
            raise SystemExit(f"HALT: {s} {iso(int(t.entry_ms))}: v6's harvest bar is not on the "
                             f"raw 4h grid")
        u = leg(hj, 1.0 * HARVEST_FRAC_TYPED) + leg(xj, 1.0 * (1.0 - HARVEST_FRAC_TYPED))
    else:
        u = leg(xj, 1.0)
    raw_r = (0.0 + u) / float(t.r_dist)
    return min(raw_r, FUNDING_CEIL_TYPED) if raw_r > FUNDING_CEIL_TYPED else raw_r


def exit_ms_derived(kind: str, mode: str) -> dict:
    """{key: the TP book's exit bar open} by this file: the first fillable bar,
    else v6's exit bar (the arm rides v6's path until it fills)."""
    R = ref()
    return {k: (x["open"] if x is not None else int(R["v6"][k].exit_ms))
            for k, x in expected(kind, mode).items()}


def hand_book(t, xpx: float, harvested: bool) -> tuple[float, float]:
    """_account_chain's gross / fee for a one-leg campaign exiting at xpx, typed
    law (harvest 0.5 at v6's harvest price iff it fired BEFORE the fill bar)."""
    d, e, R_ = int(t.direction), float(t.entry_px), float(t.r_dist)
    bps, q, size = TAKER_BPS_TYPED / 10_000.0, HARVEST_FRAC_TYPED, 1.0
    if harvested:
        hpx = float(t.harvest_px)
        g1 = size * q * (hpx - e) * d
        fe1 = bps * size * q * (e + hpx)
        g2 = size * (1.0 - q) * (xpx - e) * d
        fe2 = bps * size * (1.0 - q) * (e + xpx)
        g, fe = g1 + g2, fe1 + fe2
    else:
        g = size * (xpx - e) * d
        fe = bps * size * (e + xpx)
    return (0.0 + g) / R_, (0.0 + fe) / R_


# ═══════════════════════════════════════════════════════════════════ F-TP
def _key_rows(df: pd.DataFrame) -> dict:
    return {(s, int(e)): i for i, (s, e) in enumerate(zip(df["symbol"], df["entry_ms"]))}


def tp_arm_findings(df: pd.DataFrame, arm: str) -> list[str]:
    R = ref()
    kind, mode = TP_BOOKS_TYPED[arm]
    exp = expected(kind, mode)
    out = []
    ix = _key_rows(df)
    col = {c: df[c].to_numpy() for c in df.columns}
    for key, t in R["v6"].items():
        i = ix.get(key)
        tag = f"{arm} {key[0]} {iso(key[1])}"
        if i is None:
            out.append(f"TP-KEYS {tag}: absent from the book")
            continue
        x = exp[key]
        reason = str(col["exit_reason"][i])
        if x is not None:
            if reason != "tp":
                out.append(f"TP-MISSED {tag}: fillable at {iso(x['open'])} (level {x['level']!r}, "
                           f"fill {x['fill']!r}) but the book exits {reason}")
                continue
            if int(col["exit_ms"][i]) != x["open"]:
                out.append(f"TP-BAR {tag}: first fillable bar {iso(x['open'])}, the book fills "
                           f"at {iso(int(col['exit_ms'][i]))}")
                continue
            if float(col["exit_px"][i]) != x["fill"]:
                out.append(f"TP-FILL {tag}: fill {py(col['exit_px'][i])!r} != max/min(level, "
                           f"open) {x['fill']!r}")
            if float(col["tp_level"][i]) != x["level"]:
                out.append(f"TP-LEVEL {tag}: level {py(col['tp_level'][i])!r} != the as-of "
                           f"prefix level {x['level']!r}")
            if int(col["tp_asof12_close_ms"][i]) != x["asof"]:
                out.append(f"TP-ASOF {tag}: the book's 12h bar closes "
                           f"{iso(int(col['tp_asof12_close_ms'][i]))}, the as-of bar closes "
                           f"{iso(x['asof'])}")
            g, fe = hand_book(t, x["fill"], x["hb"])
            if float(col["gross_r"][i]) != g or float(col["fee_r"][i]) != fe:
                out.append(f"TP-BOOK {tag}: gross/fee {py(col['gross_r'][i])!r}/"
                           f"{py(col['fee_r'][i])!r} != the typed accounting {g!r}/{fe!r}")
            fu = hand_funding(t, int(x["j"]), x["hb"])
            if float(col["funding_r"][i]) != fu:
                out.append(f"TP-FUNDING {tag}: funding_r {py(col['funding_r'][i])!r} != this "
                           f"file's walk of the raw funding stamps {fu!r}")
            if float(col["net_r"][i]) != g - fe - fu:
                out.append(f"TP-NET {tag}: net_r {py(col['net_r'][i])!r} != gross − fee − "
                           f"funding {g - fe - fu!r}")
            fr = (x["fill"] - float(t.entry_px)) * int(t.direction) / float(t.r_dist)
            m = float(col["mfe_r"][i])
            if not (fr <= m <= float(t.mfe_r)):
                out.append(f"TP-MFE {tag}: mfe_r {m!r} outside [fill {fr!r}, v6 {t.mfe_r!r}] "
                           f"(AM-6 s2)")
        else:
            if reason == "tp":
                out.append(f"TP-EXTRA {tag}: no fillable bar in (entry, v6 exit] but the book "
                           f"fills at {iso(int(col['exit_ms'][i]))}")
            elif (int(col["exit_ms"][i]), reason, float(col["net_r"][i])) != (
                    int(t.exit_ms), t.exit_reason, float(t.net_r)):
                out.append(f"TP-UNACTED {tag}: never fillable, but the exit is not v6's")
    # every TP fill row, judged directly on the raw bars
    g = GUARD_BPS_TYPED / 10_000.0
    for i in np.flatnonzero(col["exit_reason"] == "tp"):
        s, d = str(col["symbol"][i]), int(col["direction"][i])
        r4 = R["raw4"][s]
        j = int(np.searchsorted(r4["t"], int(col["exit_ms"][i])))
        o4, tag = int(r4["t"][j]), f"{arm} {s} {iso(int(col['entry_ms'][i]))}"
        lvl, e, fx = float(col["tp_level"][i]), float(col["entry_px"][i]), \
            float(col["exit_px"][i])
        if int(col["tp_asof12_close_ms"][i]) > o4:
            out.append(f"TP-ASOF {tag}: LOOK-AHEAD — the level's 12h bar closes "
                       f"{iso(int(col['tp_asof12_close_ms'][i]))}, after the 4h open {iso(o4)}")
        if mode != "unguarded" and not ((lvl - e) * d > g * e):
            out.append(f"TP-GUARD {tag}: level {lvl!r} is not > 10 bps beyond entry {e!r} "
                       f"({(lvl - e) * d / e * 1e4:+.3f} bps)")
        if not ((lvl - float(r4["c"][j - 1])) * d > 0.0):
            out.append(f"TP-NEAR {tag}: prior close {float(r4['c'][j - 1])!r} is not on the near "
                       f"side of {lvl!r}")
        want = max(lvl, float(r4["o"][j])) if d == 1 else min(lvl, float(r4["o"][j]))
        if fx != want:
            out.append(f"TP-FILL {tag}: fill {fx!r} != max/min(level, open) {want!r}")
        if not ((float(r4["h"][j]) >= lvl) if d == 1 else (float(r4["l"][j]) <= lvl)):
            out.append(f"TP-TOUCH {tag}: bar {iso(o4)} never reached {lvl!r}")
    return out


def tp_bars_findings(bars: pd.DataFrame, kind: str) -> list[str]:
    """Every tp_bars row of one scale: as-of 12h close <= the bar open and equal to
    this file's; level and flags equal this file's."""
    out = []
    ex = {(k[0], k[1], b["open"]): b for k, rows in exp_bars(kind).items() for b in rows}
    g = bars[bars["scale_kind"] == kind]
    c = {x: g[x].to_numpy() for x in ("symbol", "entry_ms", "bar_open_ms", "asof12_close_ms",
                                      "level", "near", "guard_ok", "touched", "state12")}
    for i in range(len(g)):
        key = (str(c["symbol"][i]), int(c["entry_ms"][i]), int(c["bar_open_ms"][i]))
        tag = f"{kind} {key[0]} {iso(key[1])} bar {iso(key[2])}"
        a = int(c["asof12_close_ms"][i])
        if a > key[2]:
            out.append(f"TP-ASOF {tag}: LOOK-AHEAD — the 12h bar read closes {iso(a)}, after "
                       f"the 4h open")
        b = ex.get(key)
        if b is None:
            continue                        # coverage is F-TP-EXPANSION's
        if a != b["asof"]:
            out.append(f"TP-ASOF {tag}: 12h bar closing {iso(a)} != the as-of bar {iso(b['asof'])}")
        lv = float(c["level"][i])
        if not (lv == b["level"] or (np.isnan(lv) and np.isnan(b["level"]))):
            out.append(f"TP-LEVEL {tag}: level {lv!r} != {b['level']!r}")
        if (bool(c["near"][i]), bool(c["guard_ok"][i]), bool(c["touched"][i])) != (
                b["near"], b["guard"], b["touched"]):
            out.append(f"TP-FLAGS {tag}: near/guard/touched "
                       f"{(bool(c['near'][i]), bool(c['guard_ok'][i]), bool(c['touched'][i]))} "
                       f"!= {(b['near'], b['guard'], b['touched'])}")
    return out


FILLS_COLS_TYPED = ("direction", "era", "entry_px", "r_dist", "fill_bar_open_ms",
                    "asof12_close_ms", "level", "fill_px", "harvested", "net_r", "v6_net_r",
                    "delta_r", "v6_exit_reason", "v6_exit_ms", "bars_saved",
                    "scale_in_sample_12h")


def _same(a, b) -> bool:
    """Exact equality; NaN equals NaN; <NA> equals None."""
    if a is None or b is None or a is pd.NA or b is pd.NA:
        return (a is None or a is pd.NA) and (b is None or b is pd.NA)
    if isinstance(a, float) and isinstance(b, float) and np.isnan(a) and np.isnan(b):
        return True
    return a == b


def fills_table_findings(bd: dict) -> list[str]:
    """tp_fills, row for row: exactly the TP exits of the four TP regbooks, every
    column this file's (the fill from the raw-bar derivation, v6's fields from the
    lineage book, the regbook's net_r), the as-of close <= the fill bar's open."""
    R = ref()
    out = []
    ft = bd["stage"]["tp_fills"]
    want_keys = set()
    for arm, bk in GRID_BOOK_OF_ARM.items():
        df = bd["reg"][arm][0]
        for s_, e_ in zip(df.loc[df["exit_reason"] == "tp", "symbol"],
                          df.loc[df["exit_reason"] == "tp", "entry_ms"]):
            want_keys.add((bk, str(s_), int(e_)))
    got = [(str(b), str(s_), int(e_)) for b, s_, e_ in zip(ft["book"], ft["symbol"],
                                                         ft["entry_ms"])]
    if set(got) != want_keys or len(got) != len(set(got)):
        out.append(f"TP-FILLS-TABLE: {len(got)} rows != the {len(want_keys)} TP exits of the four "
                   f"TP regbooks ({len(set(got) - want_keys)} extra, "
                   f"{len(want_keys - set(got))} missing)")
    arm_of = {v: k for k, v in GRID_BOOK_OF_ARM.items()}
    for i in range(len(ft)):
        b, s_, em = got[i]
        tag = f"tp_fills {b} {s_} {iso(em)}"
        fo, a12 = int(ft["fill_bar_open_ms"].iloc[i]), int(ft["asof12_close_ms"].iloc[i])
        if a12 > fo:
            out.append(f"TP-ASOF {tag}: LOOK-AHEAD — the level's 12h bar closes {iso(a12)}, "
                       f"after the fill bar's open {iso(fo)}")
        arm = arm_of.get(b)
        t = R["v6"].get((s_, em))
        if arm is None or t is None:
            out.append(f"TP-FILLS-TABLE {tag}: not a (TP book, v6 campaign)")
            continue
        kind, mode = TP_BOOKS_TYPED[arm]
        x = expected(kind, mode)[(s_, em)]
        if x is None:
            out.append(f"TP-FILLS-TABLE {tag}: no fillable bar by this file's derivation")
            continue
        reg = bd["reg"][arm][0]
        ri = _key_rows(reg).get((s_, em))
        net = float(reg["net_r"].iloc[ri]) if ri is not None else float("nan")
        opens = [r["open"] for r in exp_bars(kind)[(s_, em)] if r["open"] <= x["open"]]
        want = {"direction": int(t.direction), "era": era_typed(int(t.entry_ms) + MS4H),
                "entry_px": float(t.entry_px), "r_dist": float(t.r_dist),
                "fill_bar_open_ms": int(x["open"]), "asof12_close_ms": int(x["asof"]),
                "level": float(x["level"]), "fill_px": float(x["fill"]),
                "harvested": bool(x["hb"]), "net_r": net, "v6_net_r": float(t.net_r),
                "delta_r": net - float(t.net_r), "v6_exit_reason": str(t.exit_reason),
                "v6_exit_ms": int(t.exit_ms),
                "bars_saved": (int(t.exit_ms) - int(x["open"])) // MS4H,
                "scale_in_sample_12h": insample_typed(kind, s_, opens)}
        for c in FILLS_COLS_TYPED:
            v = py(ft[c].iloc[i]) if c in ft.columns else None
            if not _same(v, want[c]):
                out.append(f"TP-FILLS-TABLE {tag}: {c} {v!r} != this file's {want[c]!r}")
    return out


def tp_findings(bd: dict) -> list[str]:
    out = []
    for arm in TP_BOOKS_TYPED:
        df = bd["reg"][arm][0]
        if df is None:
            out.append(f"TP-KEYS {arm}: no regbook")
            continue
        out += tp_arm_findings(df, arm)
    bars = bd["stage"]["tp_bars"]
    for kind in ("calibrated", "frozen3.0"):
        out += tp_bars_findings(bars, kind)
    out += fills_table_findings(bd)
    return out


def _lookahead_index(close12_ms, instants_ms):
    """SABOTAGE: the 12h bar CONTAINING the instant (its open <= t) — it closes after."""
    c = np.asarray(close12_ms, dtype=np.int64)
    return np.searchsorted(c - MS12H, np.asarray(instants_ms, dtype=np.int64), side="right") - 1


def tp_break():
    def lookahead():
        with scratch_build("lookahead", (S, "asof_12h_index", _lookahead_index)) as bd:
            return tp_findings(bd)

    def unguarded_scored():
        tb = dict(S.TP_BOOKS)
        tb["scored"] = ("calibrated", "unguarded")
        with scratch_build("noguard", (S, "TP_BOOKS", tb)) as bd:
            return tp_arm_findings(bd["reg"]["scored"][0], "scored")

    def guard_copy():
        df = canon()["reg"]["scored"][0].copy()
        i = int(np.flatnonzero(df["exit_reason"].to_numpy() == "tp")[0])
        d, e = int(df.loc[i, "direction"]), float(df.loc[i, "entry_px"])
        df.loc[i, "tp_level"] = e * (1.0 + 5e-4 * d)
        return tp_arm_findings(df, "scored")

    def gap_copy():
        df = canon()["reg"]["scored"][0].copy()
        i = int(np.flatnonzero(df["exit_reason"].to_numpy() == "tp")[0])
        s = df.loc[i, "symbol"]
        r4 = ref()["raw4"][s]
        j = int(np.searchsorted(r4["t"], int(df.loc[i, "exit_ms"])))
        d = int(df.loc[i, "direction"])
        lvl = float(df.loc[i, "tp_level"])
        other = min(lvl, float(r4["o"][j])) if d == 1 else max(lvl, float(r4["o"][j]))
        df.loc[i, "exit_px"] = other if other != float(df.loc[i, "exit_px"]) else lvl * (1 + 1e-6)
        return tp_arm_findings(df, "scored")

    def funding_copy():
        df = canon()["reg"]["tierE__tp_post_harvest"][0].copy()
        i = int(np.flatnonzero(df["exit_reason"].to_numpy() == "tp")[1])
        df.loc[i, "funding_r"] = float(df.loc[i, "funding_r"]) + 1e-9
        df.loc[i, "net_r"] = (float(df.loc[i, "gross_r"]) - float(df.loc[i, "fee_r"])
                              - float(df.loc[i, "funding_r"]))
        return tp_arm_findings(df, "tierE__tp_post_harvest")

    def fills_px():
        bd = bcopy(canon())
        ft = bd["stage"]["tp_fills"]
        i = int(np.flatnonzero((ft["book"] == "frozen3").to_numpy())[2])
        ft.loc[i, "fill_px"] = float(ft.loc[i, "fill_px"]) * 1.01
        return fills_table_findings(bd)

    def fills_asof():
        bd = bcopy(canon())
        ft = bd["stage"]["tp_fills"]
        i = int(np.flatnonzero((ft["book"] == "unguarded").to_numpy())[4])
        ft.loc[i, "asof12_close_ms"] = int(ft.loc[i, "asof12_close_ms"]) + MS12H
        return fills_table_findings(bd)

    return plants([
        ("the module reads the 12h bar CONTAINING the 4h open (look-ahead), rebuilt",
         "TP-ASOF", lookahead),
        ("the module's scored arm without the entry-side guard, rebuilt", "TP-GUARD",
         unguarded_scored),
        ("a copy: one TP fill's level 5 bps beyond entry", "TP-GUARD", guard_copy),
        ("a copy: one TP fill priced on the wrong side of max/min(level, open)", "TP-FILL",
         gap_copy),
        ("a copy: one post-harvest TP row's funding_r +1e-9 (net_r kept = gross − fee − "
         "funding)", "TP-FUNDING", funding_copy),
        ("a copy of tp_fills: one frozen3 fill +1%", "TP-FILLS-TABLE", fills_px),
        ("a copy of tp_fills: one unguarded fill's as-of 12h close 12h later (look-ahead)",
         "TP-ASOF tp_fills", fills_asof),
    ])


def tp_real():
    bd = canon()
    f = tp_findings(bd)
    R = ref()
    n_fill = {a: int((bd["reg"][a][0]["exit_reason"] == "tp").sum()) for a in TP_BOOKS_TYPED}
    n_bars = {k: sum(len(v) for v in exp_bars(k).values()) for k in ("calibrated", "frozen3.0")}
    # three fills hand-walked bar by bar at the 4h level (a long, a short, a harvested one)
    sc = bd["reg"]["scored"][0]
    tpr = sc[sc["exit_reason"] == "tp"]
    picks = []
    for cond in ((tpr["direction"] == 1) & ~tpr["harvested"], (tpr["direction"] == -1),
                 tpr["harvested"]):
        cand = tpr[cond & ~tpr.index.isin(picks)]
        if len(cand):
            picks.append(cand.index[0])
    for i in tpr.index:
        if len(picks) >= 3:
            break
        if i not in picks:
            picks.append(i)
    for i in picks:
        r = sc.loc[i]
        key = (r["symbol"], int(r["entry_ms"]))
        t = R["v6"][key]
        b = expected("calibrated", "record")[key]
        r12 = R["raw12"][key[0]]
        d = int(r["direction"])
        say(f"    HAND-WALK {key[0]} {'long' if d == 1 else 'short'} entered "
            f"{iso(key[1])} @ {float(r['entry_px'])!r} (R {float(r['r_dist']):.6g}); v6 exit "
            f"{t.exit_reason} {iso(int(t.exit_ms))}; harvested before the fill: {b['hb']}")
        say(f"      fill bar opens {iso(b['open'])}: the as-of 12h bar opens "
            f"{iso(int(r12['t'][b['k']]))} and closes {iso(b['asof'])} <= the 4h open "
            f"({b['asof'] <= b['open']}); the next 12h bar closes "
            f"{iso(int(r12['t'][b['k'] + 1]) + MS12H) if b['k'] + 1 < len(r12['t']) else '—'}")
        say(f"      prefix-run box (bars 0..{b['k']}) state {b['state']} top {b['top']!r} bot "
            f"{b['bot']!r}; ATR_12h (plain Wilder loop) {b['atr']!r}")
        say(f"      level = {'top − 0.25·ATR' if d == 1 else 'bot + 0.25·ATR'} = {b['level']!r} "
            f"== book {float(r['tp_level'])!r}: {b['level'] == float(r['tp_level'])}")
        say(f"      prior 4h close {b['prior']!r} on the near side: {b['near']}; guard "
            f"(level − entry)·d = {(b['level'] - float(r['entry_px'])) * d:.6g} > 10 bps·entry "
            f"= {GUARD_BPS_TYPED / 1e4 * float(r['entry_px']):.6g}: {b['guard']}")
        say(f"      bar o/h/l {b['o4']!r}/{b['h4']!r}/{b['l4']!r} reaches the level: "
            f"{b['touched']}; fill {'max' if d == 1 else 'min'}(level, open) = {b['fill']!r} == "
            f"book {float(r['exit_px'])!r}: {b['fill'] == float(r['exit_px'])}; gross/fee hand "
            f"{hand_book(t, b['fill'], b['hb'])[0]:.6f}/{hand_book(t, b['fill'], b['hb'])[1]:.6f} == book "
            f"{float(r['gross_r']):.6f}/{float(r['fee_r']):.6f}")
        fu = hand_funding(t, int(b["j"]), b["hb"])
        g_, fe_ = hand_book(t, b["fill"], b["hb"])
        say(f"      funding (raw stamps over the bars ridden, D12 ceiling {FUNDING_CEIL_TYPED}) "
            f"{fu:.6f} == book {float(r['funding_r']):.6f}; net = gross − fee − funding = "
            f"{g_ - fe_ - fu:.6f} == book {float(r['net_r']):.6f}: "
            f"{g_ - fe_ - fu == float(r['net_r'])}")
    boxes = len(R["box"])
    ftab = bd["stage"]["tp_fills"]
    return (not f), (f"every campaign of the 4 TP books ({N_V6_TYPED} each) re-derived from raw "
                     f"bars: first fillable bar, fill, level, as-of 12h close, gross/fee exact; "
                     f"funding (raw stamps) and net_r exact; TP fills {n_fill}; every fill "
                     f"row judged directly (as-of <= 4h open, guard, near side, max/min(level, "
                     f"open), touch, mfe in [fill, v6]); tp_bars rows checked vs this file's "
                     f"{n_bars} bars; tp_fills ({len(ftab)} rows) == the four books' TP exits, "
                     f"{len(FILLS_COLS_TYPED)} columns each re-derived; {boxes} prefix runs "
                     f"of the range machine; {len(picks)} fills hand-walked above"
                     + (f"; findings {len(f)}: {f[:4]}" if f else ""))


# ═══════════════════════════════════════════════════════════ F-TP-EXPANSION
def expansion_findings(bd: dict) -> list[str]:
    out = []
    bars = bd["stage"]["tp_bars"]
    for kind in ("calibrated", "frozen3.0"):
        ex = {(k[0], k[1], b["open"]): b for k, rows in exp_bars(kind).items() for b in rows}
        g = bars[bars["scale_kind"] == kind]
        got = list(zip(g["symbol"], g["entry_ms"].astype(np.int64), g["bar_open_ms"]
                       .astype(np.int64)))
        miss, extra = set(ex) - set(got), set(got) - set(ex)
        if miss or extra or len(got) != len(set(got)):
            out.append(f"TP-COVERAGE {kind}: tp_bars misses {len(miss)} bar(s) and holds "
                       f"{len(extra)} extra (every bar of every v6 campaign is the commission)")
        c = {x: g[x].to_numpy() for x in ("level", "live_record", "live_post_harvest",
                                          "live_unguarded", "fill_px", "state12")}
        for i, key in enumerate(got):
            b = ex.get(key)
            if b is None or b["inr"]:
                if b is not None and str(c["state12"][i]) != "IN_RANGE":
                    out.append(f"TP-STATE {kind} {key[0]} bar {iso(key[2])}: "
                               f"{c['state12'][i]} != IN_RANGE")
                continue
            tag = f"{kind} {key[0]} {iso(key[1])} bar {iso(key[2])} (12h as-of {b['state']})"
            if np.isfinite(float(c["level"][i])):
                out.append(f"TP-EXPANSION {tag}: a level {float(c['level'][i])!r} rests")
            if bool(c["live_record"][i]) or bool(c["live_post_harvest"][i]) \
                    or bool(c["live_unguarded"][i]):
                out.append(f"TP-EXPANSION {tag}: an order is live")
            if np.isfinite(float(c["fill_px"][i])):
                out.append(f"TP-EXPANSION {tag}: a fill price")
            if str(c["state12"][i]) != b["state"]:
                out.append(f"TP-STATE {tag}: the module says {c['state12'][i]}")
    for arm, (kind, _) in TP_BOOKS_TYPED.items():
        df = bd["reg"][arm][0]
        ex = {(k[0], k[1], b["open"]): b for k, rows in exp_bars(kind).items() for b in rows}
        tp = df[df["exit_reason"] == "tp"]
        for s, e, x in zip(tp["symbol"], tp["entry_ms"].astype(np.int64),
                           tp["exit_ms"].astype(np.int64)):
            b = ex.get((s, int(e), int(x)))
            if b is not None and not b["inr"]:
                out.append(f"TP-EXPANSION {arm} {s} {iso(int(e))}: a TP fill at {iso(int(x))} "
                           f"on a 12h {b['state']} bar")
    return out


def _sticky_levels(open4_ms, facts):
    """SABOTAGE: the last live box (and IN_RANGE) carried through expansion bars."""
    lv = _TRUE_LEVELS(open4_ms, facts)
    out = {k: np.array(v, copy=True) for k, v in lv.items()}
    last = -1
    for j in range(len(out["level_long"])):
        if lv["in_range"][j]:
            last = j
        elif last >= 0:
            for k in ("top", "bot", "atr", "level_long", "level_short"):
                out[k][j] = lv[k][last]
            out["in_range"][j] = True
            out["state4"][j] = N.STATE4["IN_RANGE"]
    return out


def _sticky_box_only(open4_ms, facts):
    """SABOTAGE: the box carried, the state left honest (the module's own L-H.1
    assertion must refuse it)."""
    lv = _TRUE_LEVELS(open4_ms, facts)
    out = {k: np.array(v, copy=True) for k, v in lv.items()}
    last = -1
    for j in range(len(out["level_long"])):
        if lv["in_range"][j]:
            last = j
        elif last >= 0:
            out["level_long"][j], out["level_short"][j] = lv["level_long"][last], \
                lv["level_short"][last]
    return out


_TRUE_LEVELS = S.levels_from_facts


def expansion_break():
    def sticky():
        with scratch_build("sticky", (S, "levels_from_facts", _sticky_levels)) as bd:
            return expansion_findings(bd)

    def planted():
        bd = bcopy(canon())
        b = bd["stage"]["tp_bars"]
        i = int(np.flatnonzero((b["state12"] == "BULL_EXP").to_numpy()
                               & (b["scale_kind"] == "calibrated").to_numpy())[0])
        b.loc[i, "level"] = float(b.loc[i, "bar_high"])
        return expansion_findings(bd)

    def box_only():
        with scratch_build("boxonly", (S, "levels_from_facts", _sticky_box_only)) as bd:
            return expansion_findings(bd)

    return plants([
        ("the module carries the last live box and IN_RANGE through expansion bars, rebuilt",
         "TP-EXPANSION", sticky),
        ("a copy of tp_bars: a level planted on a BULL_EXP bar", "TP-EXPANSION", planted),
        ("the module carries the box but not the state (its own assertion)",
         "not IN_RANGE", box_only),
    ])


def expansion_real():
    bd = canon()
    f = expansion_findings(bd)
    cnt = {}
    for kind in ("calibrated", "frozen3.0"):
        c = {}
        for rows in exp_bars(kind).values():
            for b in rows:
                c[b["state"]] = c.get(b["state"], 0) + 1
        cnt[kind] = dict(sorted(c.items()))
    return (not f), (f"every bar (entry, v6 exit] of all {N_V6_TYPED} campaigns in tp_bars, both "
                     f"scales, no extra; 12h as-of states by the prefix run {cnt}; on every "
                     f"BULL_EXP / BEAR_EXP / NONE bar: no level, no live order under any mode, "
                     f"no fill price, the same state name; no TP fill of the four TP books on "
                     f"such a bar" + (f"; findings {len(f)}: {f[:4]}" if f else ""))


# ═══════════════════════════════════════════════════════════════ F-IDENTITY
ID_EQ_COLS = ("net_r", "gross_r", "fee_r", "funding_r", "exit_ms", "exit_close_ms", "exit_px",
              "exit_reason")
ID_ENTRY_COLS = ("direction", "entry_close_ms", "entry_px", "stop_px", "r_dist", "lane")


def identity_findings(bd: dict) -> list[str]:
    out = []
    base = bd["reg"]["base"][0]
    bk = _key_rows(base)
    if len(base) != N_V6_TYPED:
        out.append(f"IDENTITY-KEYS base: n {len(base)} != {N_V6_TYPED}")
    for arm in TP_BOOKS_TYPED:
        df = bd["reg"][arm][0]
        dk = _key_rows(df)
        if set(dk) != set(bk) or len(dk) != len(df) or len(df) != len(base):
            out.append(f"IDENTITY-KEYS {arm}: key set != v6's ({len(set(dk) - set(bk))} extra, "
                       f"{len(set(bk) - set(dk))} missing, n {len(df)})")
            continue
        for key, i in dk.items():
            j = bk[key]
            tag = f"{arm} {key[0]} {iso(key[1])}"
            for c in ID_ENTRY_COLS:
                if df[c].iloc[i] != base[c].iloc[j]:
                    out.append(f"IDENTITY-ENTRY {tag}: {c} differs")
            if df["exit_reason"].iloc[i] != "tp":
                for c in ID_EQ_COLS:
                    a, b = df[c].iloc[i], base[c].iloc[j]
                    if a != b:
                        out.append(f"IDENTITY-UNACTED {tag}: {c} {py(a)!r} != v6 {py(b)!r} on "
                                   f"a campaign the TP never filled")
            else:
                if int(df["exit_ms"].iloc[i]) > int(base["exit_ms"].iloc[j]):
                    out.append(f"IDENTITY-LATE {tag}: the TP exit is after v6's")
                if int(df["exit_ms"].iloc[i]) == int(base["exit_ms"].iloc[j]) \
                        and base["exit_reason"].iloc[j] == "stop":
                    out.append(f"IDENTITY-STOPFIRST {tag}: a TP on v6's stop bar")
    sc = bd["reg"]["scored"][0]
    for arm, era in (("tierE__tuning", "tuning"), ("tierE__holdout", "holdout")):
        df = bd["reg"][arm][0]
        want = sc[(sc["entry_close_ms"] <= ERA_CUT_TYPED) == (era == "tuning")]
        cols = [c for c in want.columns if c not in COLLAR_TYPED]
        a = df[cols].reset_index(drop=True)
        b = want[cols].reset_index(drop=True)
        if len(a) != len(b) or not a.equals(b):
            out.append(f"IDENTITY-SLICE {arm}: not the scored arm's rows with entry close "
                       f"{'<=' if era == 'tuning' else '>'} the typed cut ({len(a)} vs {len(b)})")
    out += base_v6_findings(bd)
    out += exit_close_findings(bd)
    out += sidecar_identity_findings(bd)
    return out


def base_v6_findings(bd: dict) -> list[str]:
    """The BASE arm against the lineage's own v6 book (B.v6_book, F-CTRL-proven —
    not the module under trial): every required column + exit_ms / exit_px /
    harvested, all 200 campaigns; the derived columns by the typed laws."""
    R = ref()
    out = []
    base = bd["reg"]["base"][0]
    ix = _key_rows(base)
    if set(ix) != set(R["v6"]) or len(ix) != len(base):
        out.append(f"IDENTITY-BASE: the base key set is not the lineage v6 book's "
                   f"({len(set(ix) - set(R['v6']))} extra, {len(set(R['v6']) - set(ix))} missing)")
    for key, t in R["v6"].items():
        i = ix.get(key)
        if i is None:
            continue
        s_ = t.symbol
        ec = int(t.entry_ms) + MS4H
        want = {"symbol": s_, "entry_ms": int(t.entry_ms), "entry_close_ms": ec,
                "direction": int(t.direction), "entry_px": float(t.entry_px),
                "stop_px": float(t.stop_px), "r_dist": float(t.r_dist),
                "exit_close_ms": int(t.exit_ms) + MS4H, "exit_reason": str(t.exit_reason),
                "net_r": float(t.net_r), "gross_r": float(t.gross_r), "fee_r": float(t.fee_r),
                "funding_r": float(t.funding_r),
                "haircut_net_r": float(t.net_r) - float(t.fee_r) * (SLIP_TYPED[s_][1]
                                                                   / TAKER_BPS_TYPED),
                "era": era_typed(ec), "lane": str(t.lane), "exit_ms": int(t.exit_ms),
                "exit_px": float(t.exit_px), "harvested": bool(t.harvested)}
        for c, v in want.items():
            g = py(base[c].iloc[i]) if c in base.columns else None
            if not _same(g, v):
                out.append(f"IDENTITY-BASE base {s_} {iso(key[1])}: {c} {g!r} != the lineage "
                           f"v6 book's {v!r}")
    return out


def exit_close_findings(bd: dict) -> list[str]:
    """Every arm: the exit bar is on the RAW 4h grid, exit_close_ms == its open +
    4h (its close), <= the pin, after the entry bar; exit_stamp_ms per L-R.5 (an
    intrabar stop / tp at the bar's open, a close event at its close)."""
    R = ref()
    out = []
    for arm in ARMS_TYPED:
        df = bd["reg"][arm][0]
        for s_, em, xm, xc, xr, xs in zip(df["symbol"], df["entry_ms"], df["exit_ms"],
                                          df["exit_close_ms"], df["exit_reason"],
                                          df["exit_stamp_ms"]):
            s_, em, xm, xc, xs = str(s_), int(em), int(xm), int(xc), int(xs)
            tag = f"{arm} {s_} {iso(em)}"
            r4 = R["raw4"][s_]["t"]
            j = int(np.searchsorted(r4, xm))
            if j >= len(r4) or int(r4[j]) != xm:
                out.append(f"EXIT-CLOSE {tag}: the exit bar {xm} is not on the raw 4h grid")
                continue
            if xc != int(r4[j]) + MS4H:
                out.append(f"EXIT-CLOSE {tag}: exit_close_ms {iso(xc)} != the exit 4h bar's "
                           f"close {iso(int(r4[j]) + MS4H)}")
            if xc > PIN or xm <= em:
                out.append(f"EXIT-CLOSE {tag}: exit bar {iso(xm)} not in (entry bar, pin]")
            st = xm if str(xr) in ("stop", "tp") else xm + MS4H
            if xs != st:
                out.append(f"EXIT-CLOSE {tag}: exit_stamp_ms {iso(xs)} != the L-R.5 stamp "
                           f"{iso(st)} ({xr})")
    return out


def sidecar_identity_findings(bd: dict) -> list[str]:
    """Every paired non-base sidecar's identity counts are ITS OWN parquet's (a TP
    book acts only by the TP: acted = the TP exits, unacted = the rest)."""
    out = []
    for arm, (kind, era) in ARMS_TYPED.items():
        if kind == "base":
            continue
        df, sd = bd["reg"][arm]
        il = (sd or {}).get("identity_law") or {}
        acted = int((df["exit_reason"] == "tp").sum())
        if (il.get("acted"), il.get("unacted"), il.get("held"),
                il.get("worst_unacted_abs_diff")) != (acted, len(df) - acted, True, 0.0):
            out.append(f"IDENTITY-SIDECAR {arm}: identity_law acted/unacted "
                       f"{il.get('acted')}/{il.get('unacted')} != its parquet's "
                       f"{acted}/{len(df) - acted} (n {len(df)})")
    return out


def identity_break():
    def unacted():
        bd = bcopy(canon())
        df = bd["reg"]["scored"][0]
        i = int(np.flatnonzero(df["exit_reason"].to_numpy() != "tp")[3])
        df.loc[i, "net_r"] = float(df.loc[i, "net_r"]) + 1e-12
        return identity_findings(bd)

    def keys():
        bd = bcopy(canon())
        df = bd["reg"]["tierE__frozen3"][0]
        df.loc[7, "entry_ms"] = int(df.loc[7, "entry_ms"]) + MS4H
        return identity_findings(bd)

    def late():
        bd = bcopy(canon())
        df = bd["reg"]["scored"][0]
        i = int(np.flatnonzero(df["exit_reason"].to_numpy() == "tp")[0])
        df.loc[i, "exit_ms"] = int(df.loc[i, "v6_exit_ms"]) + MS4H
        return identity_findings(bd)

    def slice_():
        bd = bcopy(canon())
        h = bd["reg"]["tierE__holdout"][0]
        t = bd["reg"]["tierE__tuning"][0]
        bd["reg"]["tierE__tuning"] = (pd.concat([t, h.iloc[[0]]], ignore_index=True),
                                      bd["reg"]["tierE__tuning"][1])
        return identity_findings(bd)

    def base_bent():
        def fn(df, base_by):
            if base_by is None:
                m = ((df["symbol"] == BASE_BENT_KEY[0])
                     & (df["entry_ms"] == BASE_BENT_KEY[1])).to_numpy()
                if m.sum() != 1:
                    raise SystemExit("HALT: the base-bent campaign is not in the base book")
                df.loc[m, "net_r"] = df.loc[m, "net_r"] + 0.25
            return df
        with scratch_build("basebent", (S, "book_rows", _wrap_rows(fn))) as bd:
            return identity_findings(bd)

    def exit_at_open():
        def fn(df, base_by):
            df["exit_close_ms"] = df["exit_ms"].to_numpy(np.int64)
            return df
        with scratch_build("exitopen", (S, "book_rows", _wrap_rows(fn))) as bd:
            return identity_findings(bd)

    def slice_side():
        bd = bcopy(canon())
        full = bd["reg"]["scored"][1]["identity_law"]
        bd["reg"]["tierE__tuning"][1]["identity_law"] = dict(full)
        return identity_findings(bd)

    def module_bent():
        real = S.ride_tp_book

        def bent(base, lo, hi, levels, mode):
            bk = real(base, lo, hi, levels, mode)
            t = next(x for x in bk if not x.acted_by)
            object.__setattr__(t, "net_r", float(t.net_r) + 1e-12)
            return bk
        with mutated((S, "ride_tp_book", bent)):
            S.compute()
        return []

    return plants([
        ("a copy: one unacted scored campaign's net_r +1e-12", "IDENTITY-UNACTED", unacted),
        ("a copy: one frozen3 key moved one bar", "IDENTITY-KEYS", keys),
        ("a copy: one TP exit moved past v6's exit", "IDENTITY-LATE", late),
        ("a copy: a holdout row inside the tuning slice", "IDENTITY-SLICE", slice_),
        ("the module's ride bends one unacted net_r by 1e-12 (its own HALT)",
         "identity law fails", module_bent),
        ("the module's BASE net_r +0.25 R on BTCUSDT 2025-07-02T12:00Z (TP-acted in all four "
         "TP books), rebuilt", "IDENTITY-BASE", base_bent),
        ("the module stamps every exit_close_ms at the exit bar's OPEN, rebuilt",
         "EXIT-CLOSE", exit_at_open),
        ("a copy: tierE__tuning's sidecar carries the full arm's identity counts",
         "IDENTITY-SIDECAR", slice_side),
    ])


_REAL_BOOK_ROWS = S.book_rows


def _wrap_rows(fn):
    """A MUTATION of S.book_rows: fn(the real frame, base_by) -> the planted frame."""
    def w(book, base_by, bars, levels, scale_kind):
        return fn(_REAL_BOOK_ROWS(book, base_by, bars, levels, scale_kind), base_by)
    return w


def identity_real():
    bd = canon()
    f = identity_findings(bd)
    acted = {a: int((bd["reg"][a][0]["exit_reason"] == "tp").sum()) for a in TP_BOOKS_TYPED}
    nt = len(bd["reg"]["tierE__tuning"][0])
    nh = len(bd["reg"]["tierE__holdout"][0])
    sl = {a: (bd["reg"][a][1]["identity_law"]["acted"], bd["reg"][a][1]["identity_law"]["unacted"])
          for a in ("tierE__tuning", "tierE__holdout")}
    return (not f), (f"4 paired arms: key set == v6's ({N_V6_TYPED}); every unacted campaign "
                     f"equals v6 exactly on {list(ID_EQ_COLS)} (0.000e+00); entry fields equal "
                     f"everywhere; acted (TP) campaigns {acted}, none after v6's exit or on its "
                     f"stop bar; slices tuning {nt} + holdout {nh} == the scored arm split by "
                     f"entry close vs the typed cut; the base arm == the lineage v6 book on all "
                     f"16 required columns + exit_ms / exit_px / harvested ({N_V6_TYPED} "
                     f"campaigns, 0 differences); on all 7 arms every exit bar on the raw 4h grid, "
                     f"exit_close_ms == its close, exit_stamp_ms per L-R.5; sidecar identity "
                     f"counts == their own parquet's (slices acted/unacted {sl})"
                     + (f"; findings {len(f)}: {f[:4]}" if f else ""))


# ═══════════════════════════════════════════════════════════════════ F-ROW
def tail_ratio_typed(cell: list, base: list) -> float | None:
    """The D15 tail law, typed: top-decile MEAN (k = floor(0.1 n)) of cell ÷ base."""
    def dm(rs):
        rs = sorted(rs, reverse=True)
        k = int(np.floor(0.10 * len(rs)))
        return (sum(rs[:k]) / k) if k >= 1 else None
    cm, bm = dm(cell), dm(base)
    return round(cm / bm, 4) if (cm is not None and bm not in (None, 0)) else None


def row_findings(bd: dict) -> list[str]:
    out = []
    base = bd["reg"]["base"][0]
    for arm, (kind, era) in ARMS_TYPED.items():
        df, sd = bd["reg"][arm]
        n, sm = len(df), math.fsum(df["net_r"].astype(float))
        if sd["n"] != n or sd["sum_net_r"] != sm:
            out.append(f"ROW-SUM {arm}: sidecar n/ΣR {sd['n']}/{sd['sum_net_r']!r} != {n}/{sm!r}")
        for i in range(n):
            s = df["symbol"].iloc[i]
            hc = float(df["net_r"].iloc[i]) - float(df["fee_r"].iloc[i]) * (
                SLIP_TYPED[s][1] / TAKER_BPS_TYPED)
            if float(df["haircut_net_r"].iloc[i]) != hc:
                out.append(f"ROW-HAIRCUT {arm} {s} {iso(int(df['entry_ms'].iloc[i]))}: "
                           f"{py(df['haircut_net_r'].iloc[i])!r} != net − fee × "
                           f"{SLIP_TYPED[s][1]}/5 = {hc!r}")
                break
            er = "tuning" if int(df["entry_close_ms"].iloc[i]) <= ERA_CUT_TYPED else "holdout"
            if df["era"].iloc[i] != er:
                out.append(f"ROW-ERA {arm} {s} {iso(int(df['entry_ms'].iloc[i]))}: era "
                           f"{df['era'].iloc[i]} != {er} (entry close vs the typed cut)")
        if kind != "base":
            bb = base if era == "full" else base[base["era"] == era]
            tr = tail_ratio_typed(list(df["net_r"].astype(float)), list(bb["net_r"].astype(float)))
            if sd["d15_vs_base"]["tail_exit_ratio"] != tr:
                out.append(f"ROW-D15 {arm}: sidecar tail_exit_ratio "
                           f"{sd['d15_vs_base']['tail_exit_ratio']} != the typed top-decile mean "
                           f"ratio {tr}")
            j = df.merge(bb[["symbol", "entry_ms", "net_r"]], on=["symbol", "entry_ms"],
                         suffixes=("", "_b"))
            md_ = round(float(np.mean((j["net_r"] - j["net_r_b"]).to_numpy(float))), 6)
            if sd["d15_vs_base"]["paired_delta_expectancy_r"] != md_:
                out.append(f"ROW-D15 {arm}: paired_delta_expectancy_r "
                           f"{sd['d15_vs_base']['paired_delta_expectancy_r']} != {md_}")
    md = bd["md"]
    for arm in ("scored", "base"):
        df, sd = bd["reg"][arm]
        n, sm = len(df), math.fsum(df["net_r"].astype(float))
        hc = math.fsum(df["haircut_net_r"].astype(float))
        line = (f"| {arm} | {n} | {sm:+.4f} | {sm / n:+.4f} | {hc:+.4f} | "
                f"{int((df['exit_reason'] == 'tp').sum())} | {sd['book_sha256'][:16]}… | "
                f"book, not a verdict |")
        if line not in md:
            out.append(f"ROW-MD {arm}: the report's row of record is not {line!r}")
    sd = bd["reg"]["scored"][1]
    if f"**tail_exit_ratio {sd['d15_vs_base']['tail_exit_ratio']}**" not in md:
        out.append("ROW-D15 the report does not print the scored row's D15 tail ratio")
    if "P-WALL-1" not in md or "0.9329" not in md or "−0.0331" not in md:
        out.append("ROW-WALL the report does not name the wall-exit lesson (P-WALL-1 Δ −0.0331, "
                   "tail 0.9329)")
    # the TP order counts per campaign of the four TP arms, this file's over the bars rode
    for arm, (kind, mode) in TP_BOOKS_TYPED.items():
        df = bd["reg"][arm][0]
        xd = exit_ms_derived(kind, mode)
        for i in range(len(df)):
            key = (str(df["symbol"].iloc[i]), int(df["entry_ms"].iloc[i]))
            want = order_counts(ridden(kind, key, xd[key]), mode)
            got = {"live": int(df["tp_live_bars"].iloc[i]),
                   "guard_withheld": int(df["tp_guard_withheld"].iloc[i]),
                   "far_side": int(df["tp_far_side"].iloc[i]),
                   "preharvest_withheld": int(df["tp_preharvest_withheld"].iloc[i]),
                   "fill_blocked_by_stop": int(df["tp_fill_blocked_by_stop"].iloc[i])}
            if got != {k: want[k] for k in got}:
                out.append(f"ROW-WITHHELD {arm} {key[0]} {iso(key[1])}: counts {got} != this "
                           f"file's {({k: want[k] for k in got})}")
    sc = bd["reg"]["scored"][0]
    xd = exit_ms_derived("calibrated", "record")
    tot = camps = 0
    for key in zip(sc["symbol"], sc["entry_ms"].astype(np.int64)):
        k = order_counts(ridden("calibrated", (key[0], int(key[1])),
                                xd[(key[0], int(key[1]))]), "record")["guard_withheld"]
        tot += k
        camps += int(k > 0)
    if f"the entry-side guard withheld {tot} bar-orders on {camps} campaigns" not in md:
        out.append(f"ROW-WITHHELD the report's sentence is not 'withheld {tot} bar-orders on "
                   f"{camps} campaigns'")
    out += tables_findings(bd)
    return out


# ─────────────────── the stage tables, re-derived by this file [verifier finding 3]
def ridden(kind: str, key: tuple, exit_open: int) -> list:
    """This file's bars of one campaign that the arm rode: (entry, its exit bar]."""
    return [b for b in exp_bars(kind)[key] if b["open"] <= int(exit_open)]


def order_counts(rows: list, mode: str) -> dict:
    """The TP order counts over ridden bars, typed: far side (a level, the prior
    close beyond it); guard-withheld (near side, level inside 10 bps — counted in
    EVERY mode: on the unguarded twin a would-withhold bar); pre-harvest (post-
    harvest twin: near, guarded, harvest not yet fired); live (under the mode); a
    live touched order on v6's stop bar (the stop wins); the guard-withheld bars
    the price reached."""
    c = dict.fromkeys(("bars", "with_level", "live", "guard_withheld", "far_side",
                       "preharvest_withheld", "fill_blocked_by_stop", "gw_touched"), 0)
    for b in rows:
        c["bars"] += 1
        if not np.isfinite(b["level"]):
            continue
        c["with_level"] += 1
        if not b["near"]:
            c["far_side"] += 1
        elif not b["guard"]:
            c["guard_withheld"] += 1
            c["gw_touched"] += int(b["touched"])
        elif mode == "post_harvest" and not b["hb"]:
            c["preharvest_withheld"] += 1
        if live_of(b, mode):
            c["live"] += 1
            c["fill_blocked_by_stop"] += int(b["touched"] and b["stop_bar"])
    return c


def _frames_by_book(bd: dict) -> dict:
    fr = {"base": bd["reg"]["base"][0]}
    fr.update({bk: bd["reg"][arm][0] for arm, bk in GRID_BOOK_OF_ARM.items()})
    return fr


def summary_findings(bd: dict) -> list[str]:
    """tp_summary: every cell, every statistic, from the regbooks (fsum sums, the
    typed D15 tail law vs the base cell, Δ on the same key)."""
    out = []
    fr = _frames_by_book(bd)
    base = fr["base"]
    sm = bd["stage"]["tp_summary"]
    idx = {c: i for i, c in enumerate(sm["cell"])}
    for b in BOOKS_GRID_TYPED:
        df = fr[b]
        for era in ERAS_TYPED:
            for a in ASSETS_ALL_TYPED:
                def sel(d):
                    m = np.ones(len(d), bool)
                    if era != "full":
                        m &= (d["era"] == era).to_numpy()
                    if a != "ALL":
                        m &= (d["symbol"] == a).to_numpy()
                    return d[m]
                c, cb = sel(df), sel(base)
                cell = f"{b}|{era}|{a}"
                if cell not in idx:
                    continue                # wholeness is F-GRID's
                n = len(c)
                bnet = {(s_, int(e_)): float(r_) for s_, e_, r_ in
                        zip(cb["symbol"], cb["entry_ms"], cb["net_r"])}
                unp = [(s_, int(e_)) for s_, e_ in zip(c["symbol"], c["entry_ms"])
                       if (s_, int(e_)) not in bnet]
                if unp:
                    out.append(f"ROW-SUMMARY {cell}: {len(unp)} campaign(s) without a base row in "
                               f"the same cell (first {unp[0][0]} {iso(unp[0][1])}) — Δ unpaired")
                if n:
                    nets = [float(v) for v in c["net_r"]]
                    dl = [float(r_) - bnet.get((s_, int(e_)), float("nan")) for s_, e_, r_ in
                          zip(c["symbol"], c["entry_ms"], c["net_r"])]
                    tr = tail_ratio_typed(nets, [float(v) for v in cb["net_r"]])
                    want = {"n": n, "n_tp": int((c["exit_reason"] == "tp").sum()),
                            "sum_net_r": math.fsum(nets), "mean_net_r": math.fsum(nets) / n,
                            "win_rate": sum(1 for v in nets if v > 0) / n,
                            "sum_haircut_net_r": math.fsum(c["haircut_net_r"].astype(float)),
                            "mean_haircut_net_r": math.fsum(c["haircut_net_r"].astype(float)) / n,
                            "sum_delta_r": math.fsum(dl), "mean_delta_r": math.fsum(dl) / n,
                            "tail_exit_ratio": float("nan") if tr is None else float(tr)}
                else:
                    want = {"n": 0, "n_tp": 0, **{k: float("nan") for k in SUMMARY_STATS}}
                r = sm.iloc[idx[cell]]
                for k, v in want.items():
                    g = py(r[k])
                    if not _same(float(g) if k not in ("n", "n_tp") else int(g), v):
                        out.append(f"ROW-SUMMARY {cell}: {k} {g!r} != this file's {v!r}")
                has_reason = bool(str(r["nan_reason"]))
                if has_reason != (not np.isfinite(want["tail_exit_ratio"])):
                    out.append(f"ROW-SUMMARY {cell}: nan_reason {str(r['nan_reason'])!r} but the "
                               f"tail is {want['tail_exit_ratio']!r}")
    return out


def picks_findings(bd: dict) -> list[str]:
    """tp_picks and the regbooks' pick columns against SCALE_PICKS.json (typed read)."""
    out = []
    pk = bd["stage"]["tp_picks"]
    ix = {str(a): i for i, a in enumerate(pk["asset"])}
    for s_ in CLASSIC5_TYPED:
        c = pick_cell_typed(s_)
        if s_ not in ix:
            continue                        # wholeness is F-GRID's
        r = pk.iloc[ix[s_]]
        want = {"lens": "12h", "pick_of_record": float(c["pick_of_record"]),
                "pick_window": str(c["pick_window"]),
                "tuning_pick": (float(c["tuning_pick"]) if c["tuning_pick"] is not None
                                else float("nan")),
                "whole_tape_pick": float(c["whole_tape_pick"]),
                "first_half_pick": float(c["first_half_pick"]), "frozen_scale": FROZEN_TYPED,
                "stability_changed": float(c["first_half_pick"]) != float(c["tuning_pick"]),
                "in_sample_holdout": bool(c["in_sample_holdout"]), "label": str(c["label"])}
        for k, v in want.items():
            g = py(r[k]) if k in pk.columns else None
            if not _same(g, v):
                out.append(f"ROW-PICKS tp_picks {s_}: {k} {g!r} != SCALE_PICKS.json's {v!r}")
    for arm, (kind, _) in TP_BOOKS_TYPED.items():
        df = bd["reg"][arm][0]
        for s_, pv, pw, sc_ in zip(df["symbol"], df["scale_pick_12h"], df["pick_window_12h"],
                                   df["stability_changed_12h"]):
            c = pick_cell_typed(str(s_))
            want = ((pick_typed(str(s_), kind), "frozen3.0", None) if kind == "frozen3.0" else
                    (float(c["pick_of_record"]), str(c["pick_window"]),
                     float(c["first_half_pick"]) != float(c["tuning_pick"])))
            got = (float(pv), str(pw), None if sc_ is pd.NA else bool(sc_))
            if got != want:
                out.append(f"ROW-PICKS {arm} {s_}: (pick, window, stability_changed) {got} != "
                           f"{want}")
                break
    return out


def insample_findings(bd: dict) -> list[str]:
    """SCALE-IN-SAMPLE on every TP regbook row (full arms and the slices), every
    tp_bars row, the report's count."""
    out = []
    arms = dict(TP_BOOKS_TYPED)
    arms.update({"tierE__tuning": TP_BOOKS_TYPED["scored"],
                 "tierE__holdout": TP_BOOKS_TYPED["scored"]})
    n_sc = None
    for arm, (kind, mode) in arms.items():
        df = bd["reg"][arm][0]
        xd = exit_ms_derived(kind, mode)
        k_in = 0
        for s_, e_, f_ in zip(df["symbol"], df["entry_ms"], df["scale_in_sample_12h"]):
            key = (str(s_), int(e_))
            w = insample_typed(kind, key[0], [b["open"] for b in ridden(kind, key, xd[key])])
            k_in += int(w)
            if bool(f_) != w:
                out.append(f"ROW-INSAMPLE {arm} {key[0]} {iso(key[1])}: scale_in_sample_12h "
                           f"{bool(f_)} != this file's {w}")
        if arm == "scored":
            n_sc = (k_in, len(df))
    bt = bd["stage"]["tp_bars"]
    for kind in ("calibrated", "frozen3.0"):
        g = bt[bt["scale_kind"] == kind]
        for s_, o_, f_ in zip(g["symbol"], g["bar_open_ms"], g["scale_in_sample"]):
            w = insample_typed(kind, str(s_), [int(o_)])
            if bool(f_) != w:
                out.append(f"ROW-INSAMPLE tp_bars {kind} {s_} bar {iso(int(o_))}: "
                           f"scale_in_sample {bool(f_)} != this file's {w}")
                break
    if n_sc is not None and f"({n_sc[0]} of {n_sc[1]} scored campaigns read one)" not in bd["md"]:
        out.append(f"ROW-INSAMPLE the report does not print '({n_sc[0]} of {n_sc[1]} scored "
                   f"campaigns read one)'")
    return out


WITHHELD_COLS = {"bars_ridden": "bars", "bars_with_level": "with_level", "live_bars": "live",
                 "guard_withheld_bars": "guard_withheld", "far_side_bars": "far_side",
                 "preharvest_withheld_bars": "preharvest_withheld",
                 "fill_blocked_by_stop": "fill_blocked_by_stop",
                 "guard_withheld_bars_touched": "gw_touched"}


def withheld_findings(bd: dict) -> list[str]:
    """tp_withheld: every cell, every count, from this file's bars over the bars
    each arm rode; the unguarded twin labelled WOULD-WITHHOLD everywhere."""
    out = []
    wh = bd["stage"]["tp_withheld"]
    wi = {str(c): i for i, c in enumerate(wh["cell"])}
    for arm, (kind, mode) in TP_BOOKS_TYPED.items():
        b = GRID_BOOK_OF_ARM[arm]
        df = bd["reg"][arm][0]
        xd = exit_ms_derived(kind, mode)
        per = {}
        for key in xd:
            per[key] = order_counts(ridden(kind, key, xd[key]), mode)
        for a in ASSETS_ALL_TYPED:
            cell = f"{b}|{a}"
            if cell not in wi:
                continue                    # wholeness is F-GRID's
            ks = [k for k in per if a == "ALL" or k[0] == a]
            tot = {c: sum(per[k][c] for k in ks) for c in per[ks[0]]} if ks else {}
            want = {col: int(tot.get(src, 0)) for col, src in WITHHELD_COLS.items()}
            want["bars_no_level_expansion_or_none"] = want["bars_ridden"] - want["bars_with_level"]
            want["n_campaigns"] = len(ks)
            want["campaigns_with_guard_withheld"] = sum(1 for k in ks
                                                        if per[k]["guard_withheld"])
            want["fills"] = sum(1 for k in ks if expected(kind, mode)[k] is not None)
            r = wh.iloc[wi[cell]]
            for col, v in want.items():
                if int(r[col]) != v:
                    out.append(f"ROW-WITHHELD tp_withheld {cell}: {col} {int(r[col])} != this "
                               f"file's {v}")
            lab = str(r.get("guard_count_meaning", ""))
            ok = (lab.startswith(WOULD_WITHHOLD_TYPED) if mode == "unguarded"
                  else lab == WITHHELD_TYPED)
            if not ok:
                out.append(f"ROW-WOULD-WITHHOLD tp_withheld {cell}: guard_count_meaning {lab!r} "
                           f"(the {mode} book: "
                           f"{'would-withhold…' if mode == 'unguarded' else 'withheld'})")
        if mode == "unguarded":
            sd = bd["reg"][arm][1]
            if "WOULD-WITHHOLD" not in str(sd.get("tp_guard_withheld_meaning", "")):
                out.append(f"ROW-WOULD-WITHHOLD {arm}: the sidecar does not label its "
                           f"tp_guard_withheld WOULD-WITHHOLD")
    tc = bd["stage"]["tp_campaigns"].columns
    if "unguarded_guard_would_withhold_bars" not in tc or "unguarded_guard_withheld_bars" in tc:
        out.append("ROW-WOULD-WITHHOLD tp_campaigns: the unguarded twin's guard column is not "
                   "unguarded_guard_would_withhold_bars")
    if "WOULD-WITHHOLD" not in bd["md"]:
        out.append("ROW-WOULD-WITHHOLD the report never labels the unguarded twin's counts "
                   "WOULD-WITHHOLD")
    return out


def reride_walk(exit_of: dict) -> dict:
    """THIS FILE's walk of replay9's admission [SR-H6]: per CLASSIC5 asset, the
    lineage's candidates (tierc9.card_candidates9 over tierc11_books.ride_bounds, v6
    roles) in (bar, −direction) order; a candidate at or before the open slot's exit
    bar is skipped; a candidate without a finite ATR or a struct stop railed 1.0 ATR
    is skipped; an admitted v6 campaign holds the slot to exit_of[key].  A non-v6
    admission is returned as NEW and ends that asset's walk (this referee holds no
    price or exit for it).  -> {sym: (admitted v6 keys, new keys)}"""
    lo, hi, _ = B.corridor()
    out = {}
    for s_ in CLASSIC5_TYPED:
        st = T9.frame(s_)
        f = st["f"]
        lo_i, hi_i, _ = B.ride_bounds(s_, T9.V6_ROLES, lo, hi)
        adm, new = [], []
        if hi_i >= lo_i:
            _, cc = T9.card_candidates9(s_, T9.V6_ROLES, lo_i, hi_i)
            open_until_ms = -1
            for ti, d, _a in sorted(cc, key=lambda c: (c[0], -c[1])):
                om = int(f.open_ms[ti])
                if om <= open_until_ms:
                    continue
                px, atr = float(f.c[ti]), float(f.atr[ti])
                if not (np.isfinite(atr) and atr > 0):
                    continue
                stp = T9.RC.struct_stop_4h(st["pv4"], ti, px, d, atr, min_stop_atr=RAIL_TYPED,
                                           forbidden=None)
                if stp is None or not (np.isfinite(stp.r_dist) and stp.r_dist > 0):
                    continue
                if (s_, om) not in exit_of:
                    new.append((s_, om))
                    break
                adm.append((s_, om))
                open_until_ms = int(exit_of[(s_, om)])
        out[s_] = (adm, new)
    return out


def reride_findings(bd: dict) -> list[str]:
    """tp_reride from this file's walk: with v6's exits it must BE v6's book (the
    walk's own proof); with this file's TP exits (calibrated, record) the counts
    follow, and ΣR of an admitted v6 campaign is the scored arm's (the same entry,
    stop, ride and TP levels)."""
    R = ref()
    out = []
    v6w = reride_walk({k: int(t.exit_ms) for k, t in R["v6"].items()})
    v6_keys = {s_: [k for k in R["v6"] if k[0] == s_] for s_ in CLASSIC5_TYPED}
    for s_, (adm, new) in v6w.items():
        if new or sorted(adm) != sorted(v6_keys[s_]):
            raise SystemExit(f"HALT: this file's admission walk with v6's exits is not v6's book "
                             f"on {s_} ({len(adm)} admitted, {len(new)} new, v6 {len(v6_keys[s_])})")
    tpw = reride_walk(exit_ms_derived("calibrated", "record"))
    sc = bd["reg"]["scored"][0]
    net = {(str(s_), int(e_)): float(r_) for s_, e_, r_ in
           zip(sc["symbol"], sc["entry_ms"], sc["net_r"])}
    rr = bd["stage"]["tp_reride"]
    ri = {str(a): i for i, a in enumerate(rr["asset"])}
    for a in ASSETS_ALL_TYPED:
        ss = CLASSIC5_TYPED if a == "ALL" else (a,)
        adm = [k for s_ in ss for k in tpw[s_][0]]
        new = [k for s_ in ss for k in tpw[s_][1]]
        v6k = [k for s_ in ss for k in v6_keys[s_]]
        if new:
            out.append(f"ROW-RERIDE {a}: this file's walk admits a non-v6 campaign at "
                       f"{iso(new[0][1])} into a freed slot — beyond this referee (no price)")
        want = {"n_v6": len(v6k), "n_reride": len(adm) + len(new),
                "n_new_admitted_in_freed_slots": len(new),
                "n_v6_not_taken_by_reride": len(set(v6k) - set(adm)),
                "sum_net_r_reride": math.fsum(net[k] for k in adm)}
        if a not in ri:
            continue                        # wholeness is F-GRID's
        r = rr.iloc[ri[a]]
        for k, v in want.items():
            g = py(r[k])
            if not _same(g, v):
                out.append(f"ROW-RERIDE {a}: {k} {g!r} != this file's walk {v!r}")
    return out


def campaigns_findings(bd: dict) -> list[str]:
    """tp_campaigns: the 200 v6 keys, the v6 columns from the lineage book, every
    per-book column equal to that book's regbook row."""
    R = ref()
    out = []
    tc = bd["stage"]["tp_campaigns"]
    ix = _key_rows(tc)
    if set(ix) != set(R["v6"]) or len(ix) != len(tc):
        out.append(f"ROW-CAMPAIGNS: the key set is not v6's ({len(tc)} rows)")
    regs = {bk: (bd["reg"][arm][0], _key_rows(bd["reg"][arm][0]))
            for arm, bk in GRID_BOOK_OF_ARM.items()}
    for key, t in R["v6"].items():
        i = ix.get(key)
        if i is None:
            continue
        ec = int(t.entry_ms) + MS4H
        want = {"entry_close_ms": ec, "direction": int(t.direction), "era": era_typed(ec),
                "entry_px": float(t.entry_px), "stop_px": float(t.stop_px),
                "r_dist": float(t.r_dist), "v6_exit_reason": str(t.exit_reason),
                "v6_exit_ms": int(t.exit_ms), "v6_net_r": float(t.net_r),
                "v6_harvested": bool(t.harvested)}
        for bk, (df, dix) in regs.items():
            j = dix[key]
            gcol = ("guard_would_withhold_bars" if bk == "unguarded" else "guard_withheld_bars")
            for c, src in (("exit_reason", "exit_reason"), ("exit_ms", "exit_ms"),
                           ("net_r", "net_r"), ("delta_r", "delta_r"), ("tp_level", "tp_level"),
                           (gcol, "tp_guard_withheld"),
                           ("scale_in_sample_12h", "scale_in_sample_12h")):
                want[f"{bk}_{c}"] = py(df[src].iloc[j])
        for c, v in want.items():
            g = py(tc[c].iloc[i]) if c in tc.columns else None
            if not _same(g, v):
                out.append(f"ROW-CAMPAIGNS {key[0]} {iso(key[1])}: {c} {g!r} != {v!r}")
    return out


def exits_findings(bd: dict) -> list[str]:
    out = []
    fr = _frames_by_book(bd)
    er = bd["stage"]["tp_exit_reasons"]
    ei = {str(c): i for i, c in enumerate(er["cell"])}
    for b in BOOKS_GRID_TYPED:
        vc = fr[b]["exit_reason"].value_counts()
        if set(vc.index) - set(EXIT_REASONS_TYPED):
            out.append(f"ROW-EXITS {b}: undeclared exit reasons {sorted(set(vc.index))}")
        for x in EXIT_REASONS_TYPED:
            c = f"{b}|{x}"
            if c in ei and int(er["n"].iloc[ei[c]]) != int(vc.get(x, 0)):
                out.append(f"ROW-EXITS {c}: n {int(er['n'].iloc[ei[c]])} != the regbook's "
                           f"{int(vc.get(x, 0))}")
    return out


def tables_findings(bd: dict) -> list[str]:
    return (insample_findings(bd) + summary_findings(bd) + picks_findings(bd)
            + withheld_findings(bd) + reride_findings(bd) + campaigns_findings(bd)
            + exits_findings(bd))


def row_break():
    def side_sum():
        bd = bcopy(canon())
        bd["reg"]["tierE__frozen3"][1]["sum_net_r"] += 1e-9
        return row_findings(bd)

    def d15_sum():
        def d15_sum_tail(book_df, base_df):
            d = dict(_REAL_D15(book_df, base_df))     # the tail read as a SUM of 2k
            rs = sorted(book_df["net_r"].astype(float), reverse=True)
            bs = sorted(base_df["net_r"].astype(float), reverse=True)
            k, kb = max(int(0.1 * len(rs)), 1), max(int(0.1 * len(bs)), 1)
            d["tail_exit_ratio"] = round(sum(rs[:2 * k]) / sum(bs[:kb]), 4)
            return d
        with scratch_build("d15sum", (S, "d15_of", d15_sum_tail)) as bd:
            return row_findings(bd)

    def haircut10():
        def hc10(net_r, fee_r, stem):
            h, sl, tier = _REAL_HAIRCUT(net_r, fee_r, stem)
            return float(net_r) - float(fee_r) * (sl / 10.0), sl, tier
        with scratch_build("haircut10", (S, "haircut", hc10)) as bd:
            return row_findings(bd)

    def era_flip():
        bd = bcopy(canon())
        df = bd["reg"]["tierE__unguarded"][0]
        df.loc[0, "era"] = "holdout" if df.loc[0, "era"] == "tuning" else "tuning"
        return row_findings(bd)

    def insample_off():
        def fn(df, base_by):
            if "scale_in_sample_12h" in df.columns:
                df["scale_in_sample_12h"] = False
            return df
        with scratch_build("insampleoff", (S, "book_rows", _wrap_rows(fn))) as bd:
            return row_findings(bd)

    def summary_bent():
        bd = bcopy(canon())
        sm = bd["stage"]["tp_summary"]
        i = int(np.flatnonzero((sm["cell"] == "tp_post_harvest|holdout|SOLUSDT").to_numpy())[0])
        sm.loc[i, "mean_delta_r"] = float(sm.loc[i, "mean_delta_r"]) + 1e-9
        return row_findings(bd)

    def picks_bent():
        bd = bcopy(canon())
        pk = bd["stage"]["tp_picks"]
        i = int(np.flatnonzero((pk["asset"] == "NEARUSDT").to_numpy())[0])
        pk.loc[i, "pick_of_record"] = float(pk.loc[i, "pick_of_record"]) + 0.25
        return row_findings(bd)

    def touched_bent():
        bd = bcopy(canon())
        wh = bd["stage"]["tp_withheld"]
        i = int(np.flatnonzero((wh["cell"] == "frozen3|ETHUSDT").to_numpy())[0])
        wh.loc[i, "guard_withheld_bars_touched"] = int(wh.loc[i, "guard_withheld_bars_touched"]) + 1
        return row_findings(bd)

    def would_label():
        bd = bcopy(canon())
        wh = bd["stage"]["tp_withheld"]
        i = int(np.flatnonzero((wh["cell"] == "unguarded|ZECUSDT").to_numpy())[0])
        wh.loc[i, "guard_count_meaning"] = "withheld"
        return row_findings(bd)

    def reride_bent():
        bd = bcopy(canon())
        rr = bd["stage"]["tp_reride"]
        i = int(np.flatnonzero((rr["asset"] == "BTCUSDT").to_numpy())[0])
        rr.loc[i, "sum_net_r_reride"] = float(rr.loc[i, "sum_net_r_reride"]) + 1e-9
        return row_findings(bd)

    def campaigns_bent():
        bd = bcopy(canon())
        tc = bd["stage"]["tp_campaigns"]
        tc.loc[11, "frozen3_net_r"] = float(tc.loc[11, "frozen3_net_r"]) - 0.5
        return row_findings(bd)

    def exits_bent():
        bd = bcopy(canon())
        er = bd["stage"]["tp_exit_reasons"]
        i = int(np.flatnonzero((er["cell"] == "unguarded|bell_12_89").to_numpy())[0])
        er.loc[i, "n"] = int(er.loc[i, "n"]) + 1
        return row_findings(bd)

    return plants([
        ("a copy: tierE__frozen3's sidecar ΣR +1e-9", "ROW-SUM", side_sum),
        ("the module's D15 tail read as a SUM of a doubled decile, rebuilt", "ROW-D15", d15_sum),
        ("the module's haircut at slip/10, rebuilt", "ROW-HAIRCUT", haircut10),
        ("a copy: one unguarded row's era flipped", "ROW-ERA", era_flip),
        ("the module forcing scale_in_sample_12h False on every TP row, rebuilt",
         "ROW-INSAMPLE", insample_off),
        ("a copy: tp_summary tp_post_harvest|holdout|SOLUSDT mean_delta_r +1e-9",
         "ROW-SUMMARY", summary_bent),
        ("a copy: tp_picks NEARUSDT pick_of_record +0.25", "ROW-PICKS", picks_bent),
        ("a copy: tp_withheld frozen3|ETHUSDT guard_withheld_bars_touched +1",
         "ROW-WITHHELD", touched_bent),
        ("a copy: tp_withheld unguarded|ZECUSDT labelled 'withheld'", "ROW-WOULD-WITHHOLD",
         would_label),
        ("a copy: tp_reride BTCUSDT sum_net_r_reride +1e-9", "ROW-RERIDE", reride_bent),
        ("a copy: one tp_campaigns frozen3_net_r −0.5", "ROW-CAMPAIGNS", campaigns_bent),
        ("a copy: tp_exit_reasons unguarded|bell_12_89 n +1", "ROW-EXITS", exits_bent),
    ])


_REAL_D15 = S.d15_of
_REAL_HAIRCUT = S.haircut


def row_real():
    bd = canon()
    f = row_findings(bd)
    sd = bd["reg"]["scored"][1]
    rows = []
    for arm in ARMS_TYPED:
        df = bd["reg"][arm][0]
        rows.append(f"{arm} n {len(df)} ΣR {math.fsum(df['net_r'].astype(float)):+.6f}")
    sc = bd["reg"]["scored"][0]
    rr = bd["stage"]["tp_reride"]
    ra = rr[rr["asset"] == "ALL"].iloc[0]
    tabs = {n: len(bd["stage"][n]) for n in ("tp_summary", "tp_picks", "tp_withheld",
                                              "tp_reride", "tp_campaigns", "tp_exit_reasons")}
    return (not f), (f"every arm's n / ΣR (fsum) equal its sidecar; the report's two rows of "
                     f"record exact; D15 tail ratio (typed top-decile mean law) and paired mean Δ "
                     f"equal on all 6 non-base sidecars (scored tail "
                     f"{sd['d15_vs_base']['tail_exit_ratio']}); haircut_net_r == net − fee × "
                     f"slip/5 (typed tiers) and era by entry close on every row of every arm; "
                     f"the TP order counts per campaign of the 4 TP arms and the report's "
                     f"sentence equal this file's; the wall-exit lesson named; SCALE-IN-SAMPLE "
                     f"re-derived on every TP regbook row, every tp_bars row and the report "
                     f"({int(sc['scale_in_sample_12h'].sum())} of {len(sc)} scored campaigns); "
                     f"every cell of the stage tables re-derived {tabs} (tp_withheld labels: "
                     f"unguarded WOULD-WITHHOLD); this file's admission walk reproduces v6 with "
                     f"v6's exits and, with its TP exits, admits "
                     f"{int(ra['n_new_admitted_in_freed_slots'])} new / drops "
                     f"{int(ra['n_v6_not_taken_by_reride'])} · {' · '.join(rows)}"
                     + (f"; findings {len(f)}: {f[:4]}" if f else ""))


# ═══════════════════════════════════════════════════════════════════ F-GRID
def declared() -> dict:
    return {"tp_summary": [f"{b}|{e}|{a}" for b in BOOKS_GRID_TYPED for e in ERAS_TYPED
                           for a in ASSETS_ALL_TYPED],
            "tp_withheld": [f"{b}|{a}" for b in TPBOOKS_GRID_TYPED for a in ASSETS_ALL_TYPED],
            "tp_exit_reasons": [f"{b}|{x}" for b in BOOKS_GRID_TYPED for x in EXIT_REASONS_TYPED],
            "tp_reride": list(ASSETS_ALL_TYPED), "tp_picks": list(CLASSIC5_TYPED)}


SUMMARY_STATS = ("sum_net_r", "mean_net_r", "win_rate", "sum_haircut_net_r",
                 "mean_haircut_net_r", "sum_delta_r", "mean_delta_r", "tail_exit_ratio")


def grid_findings(bd: dict) -> list[str]:
    out = []
    dec = declared()
    req = {"tp_summary": ("n", "n_tp", "nan_reason"),
           "tp_withheld": ("n_campaigns", "live_bars", "guard_withheld_bars", "fills"),
           "tp_exit_reasons": ("n",), "tp_reride": ("n_v6", "n_reride"),
           "tp_picks": ("pick_of_record", "stability_changed")}
    for name, cells in dec.items():
        df = bd["stage"][name]
        cc = "cell" if "cell" in STAGE_KEYS_TYPED[name] else "asset"
        ok, lines = TP.grid_whole(cells, df, cell_col=cc, require_cols=req[name], label=name)
        out += [f"GRID-WHOLE {x}" for x in lines if x.startswith("[BAD]")]
        vc = [c for c in df.columns if c in VERDICT_COLUMNS_TYPED]
        if vc:
            out.append(f"GRID-VERDICT {name}: verdict column(s) {vc}")
        for k, v in COLLAR_TYPED.items():
            if k not in df.columns or not (df[k] == v).all():
                out.append(f"GRID-COLLAR {name}: `{k}` is not {v!r} on every row")
        miss = [c for c in AS_OF_TYPED if c not in df.columns or df[c].isna().any()]
        if miss:
            out.append(f"GRID-ASOF {name}: as-of stamps absent/null {miss}")
    out += verdict_word_findings(bd)
    sm = bd["stage"]["tp_summary"]
    for i in range(len(sm)):
        r = sm.iloc[i]
        nan = [c for c in SUMMARY_STATS if not np.isfinite(float(r[c]))]
        if nan and not str(r["nan_reason"]):
            out.append(f"GRID-NAN tp_summary {r['cell']}: NaN {nan} without a nan_reason")
        if int(r["n"]) == 0 and len(nan) != len(SUMMARY_STATS):
            out.append(f"GRID-NAN tp_summary {r['cell']}: n = 0 with a finite stat")
    idx = {c: i for i, c in enumerate(sm["cell"])}
    for b in BOOKS_GRID_TYPED:
        for a in ASSETS_ALL_TYPED:
            try:
                f_, t_, h_ = (sm.iloc[idx[f"{b}|{e}|{a}"]] for e in ERAS_TYPED)
            except KeyError:
                continue
            for c in ("n", "n_tp"):
                if int(f_[c]) != int(t_[c]) + int(h_[c]):
                    out.append(f"GRID-PARTITION tp_summary {b}|{a}: {c} full {int(f_[c])} != "
                               f"tuning {int(t_[c])} + holdout {int(h_[c])}")
        for e in ERAS_TYPED:
            try:
                al = sm.iloc[idx[f"{b}|{e}|ALL"]]
                parts = [sm.iloc[idx[f"{b}|{e}|{a}"]] for a in CLASSIC5_TYPED]
            except KeyError:
                continue
            if int(al["n"]) != sum(int(p["n"]) for p in parts):
                out.append(f"GRID-PARTITION tp_summary {b}|{e}: ALL n != Σ assets")
    wh = bd["stage"]["tp_withheld"]
    wi = {c: i for i, c in enumerate(wh["cell"])}
    for b in TPBOOKS_GRID_TYPED:
        try:
            al = wh.iloc[wi[f"{b}|ALL"]]
            parts = [wh.iloc[wi[f"{b}|{a}"]] for a in CLASSIC5_TYPED]
        except KeyError:
            continue
        for c in ("live_bars", "guard_withheld_bars", "far_side_bars", "fills",
                  "bars_ridden"):
            if int(al[c]) != sum(int(p[c]) for p in parts):
                out.append(f"GRID-PARTITION tp_withheld {b}: ALL {c} != Σ assets")
    return out


def _strings(x):
    """Every string inside a JSON value."""
    if isinstance(x, str):
        yield x
    elif isinstance(x, dict):
        for k, v in x.items():
            yield from _strings(k)
            yield from _strings(v)
    elif isinstance(x, (list, tuple)):
        for v in x:
            yield from _strings(v)


def verdict_word_findings(bd: dict) -> list[str]:
    """No verdict WORD (typed) in any string cell of a stage table or a Tier-E
    regbook, nor in any string of a Tier-E sidecar [L-1.4]."""
    out = []
    frames = [(f"stage_h/{n}", df) for n, df in bd["stage"].items() if df is not None]
    frames += [(f"regbooks/{a}", bd["reg"][a][0]) for a, (k, _) in ARMS_TYPED.items()
               if k == "tierE" and bd["reg"][a][0] is not None]
    for name, df in frames:
        for c in df.columns:
            if df[c].dtype != object:
                continue
            for v in pd.unique(df[c].dropna()):
                if isinstance(v, str) and VERDICT_WORDS_RX.search(v):
                    out.append(f"GRID-VERDICT {name}: verdict word "
                               f"{VERDICT_WORDS_RX.search(v).group(0)!r} in a `{c}` cell "
                               f"({v[:60]!r})")
    for a, (k, _) in ARMS_TYPED.items():
        if k == "tierE" and bd["reg"][a][1] is not None:
            for v in _strings(bd["reg"][a][1]):
                if VERDICT_WORDS_RX.search(v):
                    out.append(f"GRID-VERDICT regbooks/{a}.json: verdict word "
                               f"{VERDICT_WORDS_RX.search(v).group(0)!r} ({v[:60]!r})")
    return out


def grid_break():
    def drop():
        bd = bcopy(canon())
        bd["stage"]["tp_summary"] = bd["stage"]["tp_summary"].iloc[1:].reset_index(drop=True)
        return grid_findings(bd)

    def undeclared():
        bd = bcopy(canon())
        w = bd["stage"]["tp_withheld"]
        x = w.iloc[[0]].copy()
        x["cell"] = "scored|DOGEUSDT"
        bd["stage"]["tp_withheld"] = pd.concat([w, x], ignore_index=True)
        return grid_findings(bd)

    def verdict():
        bd = bcopy(canon())
        bd["stage"]["tp_exit_reasons"]["verdict"] = "SUPPORTED"
        return grid_findings(bd)

    def collar():
        bd = bcopy(canon())
        bd["stage"]["tp_reride"] = bd["stage"]["tp_reride"].drop(columns=["selection_not_a_result"])
        return grid_findings(bd)

    def silent_nan():
        bd = bcopy(canon())
        sm = bd["stage"]["tp_summary"]
        i = int(np.flatnonzero((sm["n"] > 0).to_numpy())[0])
        sm.loc[i, "mean_net_r"] = float("nan")
        return grid_findings(bd)

    def partition():
        bd = bcopy(canon())
        sm = bd["stage"]["tp_summary"]
        i = int(np.flatnonzero((sm["cell"] == "scored|tuning|ETHUSDT").to_numpy())[0])
        sm.loc[i, "n"] = int(sm.loc[i, "n"]) + 1
        return grid_findings(bd)

    def module_no_holdout():
        with scratch_build("noholdout", (S, "ERAS", ("full", "tuning"))) as bd:
            return grid_findings(bd)

    def verdict_word():
        bd = bcopy(canon())
        pk = bd["stage"]["tp_picks"]
        pk.loc[2, "label"] = str(pk.loc[2, "label"]) + " — NOT SUPPORTED"
        return grid_findings(bd)

    return plants([
        ("a copy: tp_summary's first cell dropped", "GRID-WHOLE", drop),
        ("a copy: an undeclared tp_withheld cell", "GRID-WHOLE", undeclared),
        ("a copy: a verdict column on tp_exit_reasons", "GRID-VERDICT", verdict),
        ("a copy: the collar removed from tp_reride", "GRID-COLLAR", collar),
        ("a copy: a silent NaN in tp_summary", "GRID-NAN", silent_nan),
        ("a copy: the era partition broken", "GRID-PARTITION", partition),
        ("the module drops the holdout era from its grid, rebuilt", "GRID-WHOLE",
         module_no_holdout),
        ("a copy: 'NOT SUPPORTED' written inside a tp_picks label cell",
         "GRID-VERDICT stage_h/tp_picks", verdict_word),
    ])


def grid_real():
    bd = canon()
    f = grid_findings(bd)
    dec = declared()
    sizes = {n: len(c) for n, c in dec.items()}
    return (not f), (f"every grid whole against the typed cells {sizes} (TP.grid_whole: no "
                     f"missing, undeclared or duplicated cell; required columns non-null); no "
                     f"verdict column and no verdict word in any string cell of the 8 stage "
                     f"tables and 5 Tier-E regbooks or any string of their sidecars; collar and "
                     f"9 as-of stamps on every row; no silent NaN, "
                     f"n = 0 cells all-NaN with a reason; eras partition (full = tuning + holdout) "
                     f"and ALL = Σ assets on tp_summary and tp_withheld"
                     + (f"; findings {len(f)}: {f[:4]}" if f else ""))


# ═══════════════════════════════════════════════════════════════════ F-KEY
def csv_sha_typed(df: pd.DataFrame) -> str:
    """This file's canonical CSV (the interface law, typed here)."""
    cols = list(REQ_TYPED)
    d = df[cols].sort_values(["symbol", "entry_close_ms"], kind="mergesort")
    lines = [",".join(cols)]
    for row in d.itertuples(index=False):
        vals = []
        for c, v in zip(cols, row):
            if c in REQ_FLOAT_T:
                vals.append(repr(float(v)))
            elif REQ_TYPED[c] in ("int64", "int8"):
                vals.append(str(int(v)))
            else:
                vals.append(str(v))
        lines.append(",".join(vals))
    return hashlib.sha256(("\n".join(lines) + "\n").encode("utf-8")).hexdigest()


def key_findings(bd: dict) -> list[str]:
    out = []
    if sorted(bd["files_reg"]) != list(REG_FILES_TYPED):
        out.append(f"KEY-FILES regbooks/{REG_ID_TYPED}: {bd['files_reg']} != typed")
    if sorted(bd["files_stage"]) != list(STAGE_FILES_TYPED):
        out.append(f"KEY-FILES stage_h: {sorted(bd['files_stage'])} != typed")
    for arm, (kind, era) in ARMS_TYPED.items():
        df, sd = bd["reg"][arm]
        if df is None or sd is None:
            out.append(f"KEY-FILES {arm}: parquet or sidecar absent")
            continue
        for c, dt in REQ_TYPED.items():
            if c not in df.columns:
                out.append(f"KEY-COLS {arm}: required column `{c}` absent")
                continue
            if str(df[c].dtype) != dt:
                out.append(f"KEY-DTYPE {arm}: `{c}` is {df[c].dtype}, typed {dt}")
            if df[c].isna().any():
                out.append(f"KEY-NULL {arm}: `{c}` holds {int(df[c].isna().sum())} null(s)")
        for k2 in (["symbol", "entry_ms"], ["symbol", "entry_close_ms"]):
            if all(c in df.columns for c in k2) and df.duplicated(subset=k2).any():
                out.append(f"KEY-DUP {arm}: {k2} repeats")
        miss = [c for c in AS_OF_TYPED if c not in df.columns or df[c].isna().any()]
        if miss:
            out.append(f"KEY-ASOF {arm}: as-of stamps absent/null {miss}")
        has_c = [c for c in COLLAR_TYPED if c in df.columns]
        if kind == "tierE":
            if any(c not in df.columns or not (df[c] == v).all() for c, v in COLLAR_TYPED.items()) \
                    or any(sd.get(c) != v for c, v in COLLAR_TYPED.items()):
                out.append(f"KEY-COLLAR {arm}: a Tier-E arm without the typed collar "
                           f"(parquet or sidecar)")
        elif has_c or any(c in sd for c in COLLAR_TYPED):
            out.append(f"KEY-COLLAR {arm}: a registered arm carries the Tier-E collar")
        lack = [k for k in SIDE_KEYS_TYPED if k not in sd]
        if lack:
            out.append(f"KEY-SIDECAR {arm}: keys absent {lack}")
            continue
        want = {"registration": REG_ID_TYPED, "arm": arm, "kind": kind, "ruler": "paired",
                "panel": list(CLASSIC5_TYPED), "era_scope": era, "source_script": SOURCE_TYPED}
        for k, v in want.items():
            if sd[k] != v:
                out.append(f"KEY-SIDECAR {arm}: {k} {sd[k]!r} != typed {v!r}")
        if not str(sd["description"]).strip():
            out.append(f"KEY-SIDECAR {arm}: empty description")
        if all(c in df.columns for c in REQ_TYPED):
            try:
                sha = csv_sha_typed(df)
            except (TypeError, ValueError) as e:
                sha = f"(unhashable: {e})"
            if sd["book_sha256"] != sha:
                out.append(f"KEY-SHA {arm}: sidecar book_sha256 {str(sd['book_sha256'])[:12]}… "
                           f"!= this file's canonical CSV {sha[:12]}…")
            if sd["n"] != len(df) or sd["sum_net_r"] != math.fsum(df["net_r"].astype(float)):
                out.append(f"KEY-SIDECAR {arm}: n / sum_net_r != the parquet's")
    st = bd["status"]
    if not st or st.get("registration") != REG_ID_TYPED or st.get("status") != "BUILT" \
            or st.get("arms") != list(ARMS_TYPED) or not str(st.get("reason", "")).strip():
        out.append(f"KEY-STATUS STATUS.json is not the typed record (registration, BUILT, arms "
                   f"{list(ARMS_TYPED)}, a reason)")
    man = bd["manifest"].get("stage_tables", {}).get("content_sha", {})
    for name, key in STAGE_KEYS_TYPED.items():
        df = bd["stage"][name]
        if df is None:
            out.append(f"KEY-FILES stage_h/{name}.parquet absent")
            continue
        if any(c not in df.columns for c in key) or df.duplicated(subset=key).any() \
                or df[key].isna().any().any():
            out.append(f"KEY-DUP stage_h/{name}: typed key {key} absent, repeated or null")
        if man.get(f"{name}.parquet") != TB._content_sha(df):
            out.append(f"KEY-SHA stage_h/{name}: manifest content sha != the table read back")
    mf = bd["manifest"]
    for pre, typed, got in (("regbooks", REG_FILES_TYPED,
                             mf.get("regbooks", {}).get("file_sha256", {})),
                            ("stage_h", tuple(sorted([f"{n}.parquet" for n in STAGE_KEYS_TYPED]
                                                     + ["STAGE_H.md"])),
                             mf.get("stage_tables", {}).get("file_sha256", {}))):
        if sorted(got) != list(typed):
            out.append(f"KEY-FILESHA {pre}: manifest file_sha256 names {sorted(got)} != typed")
        for n in typed:
            if got.get(n) != bd["file_sha"].get(f"{pre}/{n}"):
                out.append(f"KEY-FILESHA {pre}/{n}: manifest file_sha256 "
                           f"{str(got.get(n))[:12]}… != the file's bytes "
                           f"{str(bd['file_sha'].get(f'{pre}/{n}'))[:12]}…")
    return out


def key_break():
    def dup():
        bd = bcopy(canon())
        df = bd["reg"]["scored"][0]
        bd["reg"]["scored"] = (pd.concat([df, df.iloc[[4]]], ignore_index=True),
                               bd["reg"]["scored"][1])
        return key_findings(bd)

    def null():
        bd = bcopy(canon())
        bd["reg"]["base"][0].loc[3, "net_r"] = float("nan")
        return key_findings(bd)

    def dtype():
        bd = bcopy(canon())
        df = bd["reg"]["tierE__holdout"][0]
        df["direction"] = df["direction"].astype(float)
        return key_findings(bd)

    def dropcol():
        bd = bcopy(canon())
        bd["reg"]["tierE__tuning"] = (bd["reg"]["tierE__tuning"][0].drop(columns=["haircut_net_r"]),
                                      bd["reg"]["tierE__tuning"][1])
        return key_findings(bd)

    def sha():
        bd = bcopy(canon())
        s = bd["reg"]["base"][1]["book_sha256"]
        bd["reg"]["base"][1]["book_sha256"] = ("0" if s[0] != "0" else "1") + s[1:]
        return key_findings(bd)

    def collar():
        bd = bcopy(canon())
        bd["reg"]["tierE__unguarded"] = (bd["reg"]["tierE__unguarded"][0].drop(columns=["gates"]),
                                         bd["reg"]["tierE__unguarded"][1])
        return key_findings(bd)

    def status():
        bd = bcopy(canon())
        bd["status"]["arms"] = bd["status"]["arms"][:-1]
        return key_findings(bd)

    def filesha():
        bd = bcopy(canon())
        m = bd["manifest"]["stage_tables"]["file_sha256"]
        v = m["tp_fills.parquet"]
        m["tp_fills.parquet"] = ("0" if v[0] != "0" else "1") + v[1:]
        return key_findings(bd)

    def module_no_lane():
        rq = tuple(c for c in S.REQ_COLS if c != "lane")
        with scratch_build("nolane", (S, "REQ_COLS", rq)) as bd:
            return key_findings(bd)

    return plants([
        ("a copy: a duplicated scored row", "KEY-DUP", dup),
        ("a copy: a null net_r in base", "KEY-NULL", null),
        ("a copy: direction stored as float in tierE__holdout", "KEY-DTYPE", dtype),
        ("a copy: haircut_net_r dropped from tierE__tuning", "KEY-COLS", dropcol),
        ("a copy: base's sidecar book_sha256 bent", "KEY-SHA", sha),
        ("a copy: the collar `gates` removed from tierE__unguarded", "KEY-COLLAR", collar),
        ("a copy: STATUS.json missing an arm", "KEY-STATUS", status),
        ("a copy: the manifest's tp_fills.parquet byte sha bent", "KEY-FILESHA", filesha),
        ("the module's REQ_COLS without 'lane', rebuilt", "KEY-SHA", module_no_lane),
    ])


def key_real():
    bd = canon()
    f = key_findings(bd)
    shas = {a: bd["reg"][a][1]["book_sha256"][:12] + "…" for a in ARMS_TYPED}
    return (not f), (f"regbooks/{REG_ID_TYPED}: the typed {len(REG_FILES_TYPED)} files; every arm "
                     f"holds the 16 typed columns at their typed dtypes, no null, unique (symbol, "
                     f"entry_ms) and (symbol, entry_close_ms), 9 as-of stamps; sidecars carry the "
                     f"typed keys/values, n / ΣR / book_sha256 (this file's canonical CSV) equal "
                     f"{shas}; Tier-E arms collared (parquet and sidecar), registered arms not; "
                     f"STATUS.json BUILT with the typed arms; stage_h: the typed "
                     f"{len(STAGE_FILES_TYPED)} files, typed keys unique and non-null, manifest "
                     f"content shas == the tables read back and manifest file_sha256 == the "
                     f"sha256 of every file's bytes ({len(REG_FILES_TYPED)} regbook files + "
                     f"{len(STAGE_KEYS_TYPED) + 1} stage files)"
                     + (f"; findings {len(f)}: {f[:4]}" if f else ""))


# ═══════════════════════════════════════════════════════════════════ F-DET
def _files(d: Path) -> dict:
    return {p.name: p.read_bytes() for p in sorted(d.iterdir()) if p.is_file()} \
        if d.exists() else {}


def det_set(root: Path) -> dict:
    """{'stage_h/<f>': bytes, 'regbooks/<f>': bytes} of one build root."""
    if root == OUT:
        s, r = OUT, REGBOOKS
    else:
        s, r = root / "stage_h", root / "regbooks" / REG_ID_TYPED
    out = {f"stage_h/{k}": v for k, v in _files(s).items() if k in STAGE_FILES_TYPED}
    out.update({f"regbooks/{k}": v for k, v in _files(r).items()})
    return out


def det_findings(a: tuple, b: tuple, canon_: dict) -> list[str]:
    out = []
    for lab, (rc, _) in (("seed 1", a), (f"seed {SEED}", b)):
        if rc != 0:
            out.append(f"{lab} exit {rc}")
    typed = sorted([f"stage_h/{x}" for x in STAGE_FILES_TYPED]
                   + [f"regbooks/{x}" for x in REG_FILES_TYPED])
    for lab, x in (("seed 1", a[1]), (f"seed {SEED}", b[1]), ("canonical", canon_)):
        if sorted(x) != typed:
            out.append(f"{lab}: file set != typed ({len(x)} vs {len(typed)})")
    for lab, x, y in ((f"seed 1 vs seed {SEED}", a[1], b[1]), ("seed 1 vs canonical", a[1], canon_)):
        for name in sorted(set(x) & set(y)):
            if x[name] != y[name]:
                k = next((i for i in range(min(len(x[name]), len(y[name])))
                          if x[name][i] != y[name][i]), min(len(x[name]), len(y[name])))
                out.append(f"{lab}: {name} bytes differ at byte {k}")
            if name.endswith(".parquet"):
                ca = TB._content_sha(pq_from_bytes(x[name]))
                cb = TB._content_sha(pq_from_bytes(y[name]))
                if ca != cb:
                    out.append(f"{lab}: {name} content sha {ca[:12]}… != {cb[:12]}…")
    return out


_PQ_DIR: list = []


def _pq_dir() -> Path:
    """A scratch dir OUTSIDE the repo for parquet bytes held in memory (removed at
    the end of main)."""
    if not _PQ_DIR:
        _PQ_DIR.append(Path(tempfile.mkdtemp(prefix="f-sh-pq-")))
    return _PQ_DIR[0]


def pq_from_bytes(b: bytes) -> pd.DataFrame:
    """AM-2: parquet bytes read through pandas on a PATH STRING (the bytes land in
    a scratch file first; no in-memory buffer reader)."""
    p = _pq_dir() / f"r_{sha_bytes(b)}.parquet"
    if not p.exists():
        p.write_bytes(b)
    return pd.read_parquet(str(p))


def pq_to_bytes(df: pd.DataFrame) -> bytes:
    """AM-2: a frame written through pandas on a PATH STRING, its bytes read back."""
    p = _pq_dir() / f"w_{len(list(_pq_dir().iterdir()))}.parquet"
    df.to_parquet(str(p), index=False)
    return p.read_bytes()


def det_dir() -> Path:
    return RUN_ROOT / DET_NAME


def det_build(d: Path, seed: int, hashorder: bool = False) -> tuple[int, dict]:
    if d.exists():
        shutil.rmtree(d)
    env = dict(_env(), PYTHONHASHSEED=str(seed))
    if not hashorder:
        cmd = [PY, "-B", str(ROOT / "scripts" / "tierc11_stage_h.py"), f"--out-dir={d}"]
    else:                                   # SABOTAGE twin: a set-order line appended
        code = (f"import sys\nsys.dont_write_bytecode = True\n"
                f"sys.path.insert(0, {str(ROOT)!r})\n"
                f"sys.path.insert(0, {str(ROOT / 'scripts')!r})\n"
                f"from pathlib import Path\nimport tierc11_stage_h as S\n"
                f"d = Path({str(d)!r})\nS.build(d)\n"
                f"p = d / 'stage_h' / S.REPORT\n"
                f"p.write_text(p.read_text() + 'set order: ' + ','.join(set(S.E.PANEL17)) "
                f"+ '\\n')\n")
        cmd = [PY, "-B", "-c", code]
    r = subprocess.run(cmd, env=env, capture_output=True, text=True, cwd=str(ROOT),
                       timeout=1800)
    if r.returncode != 0:
        clock(f"det build {d.name} exit {r.returncode}: {r.stderr[-400:]}")
    return r.returncode, det_set(d)


def det_break():
    cn = det_set(OUT)
    bent = dict(cn)
    k = "stage_h/STAGE_H.md"
    md = bytearray(bent[k])
    md[len(md) // 2] ^= 0x01
    bent[k] = bytes(md)

    def float_moved():
        d = pq_from_bytes(cn["regbooks/scored.parquet"])
        d.loc[d.index[0], "net_r"] = float(d["net_r"].iloc[0]) + 1e-6
        c2 = dict(cn)
        c2["regbooks/scored.parquet"] = pq_to_bytes(d)
        return det_findings((0, c2), (0, c2), cn)

    def hashorder():
        o = {s: det_build(det_dir() / f"hashorder_{s}", s, hashorder=True) for s in DET_SEEDS}
        a, b = o[DET_SEEDS[0]], o[DET_SEEDS[1]]
        return [x for x in det_findings(a, b, a[1]) if x.startswith(f"seed 1 vs seed {SEED}")]

    return plants([
        ("one byte bent in a copy of STAGE_H.md", "STAGE_H.md bytes differ",
         lambda: det_findings((0, cn), (0, bent), cn)),
        ("one net_r moved 1e-6 in a regbook parquet copy", "scored.parquet content sha",
         float_moved),
        ("a hash-order-dependent line (set iteration) under the two seeds",
         f"seed 1 vs seed {SEED}: stage_h/STAGE_H.md bytes differ", hashorder),
    ])


def det_real():
    cn = det_set(OUT)
    o = {s: det_build(det_dir() / f"seed_{s}", s) for s in DET_SEEDS}
    a, b = o[DET_SEEDS[0]], o[DET_SEEDS[1]]
    bad = det_findings(a, b, cn)
    shas = ", ".join(f"{k.split('/')[-1]} {sha_bytes(v)[:10]}…" for k, v in sorted(a[1].items())
                     if k.endswith((".json", ".md")))
    return (not bad), (f"exit {a[0]}/{b[0]}; {len(cn)} typed files (stage_h + regbooks) "
                       f"byte-identical seed 1 == seed {SEED} == canonical, every parquet content "
                       f"sha equal: {not bad} ({shas})" + (f"; findings {bad[:4]}" if bad else ""))


# ═══════════════════════════════════════════════════════════════════ LEGS
FIXTURES = (
    ("F-TP", "every take-profit re-derived from raw bars against the 12h boundary AS-OF "
     "[L-H.1, AM-6 s2]",
     "a TP book's fills differ from this file's raw-bar derivation (first fillable bar: 12h "
     "as-of state IN_RANGE at the 4h open, level top − 0.25 ATR / bot + 0.25 ATR from the "
     "prefix-run box and the plain-loop ATR, prior close on the near side, level > 10 bps "
     "beyond entry, harvest fired for the post-harvest twin, bar reaches the level, not v6's "
     "stop bar; fill max/min(level, open); gross/fee by the typed accounting; funding by "
     "this file's walk of the raw funding stamps, D12 ceiling 1.0 R; net = gross − fee − "
     "funding), a fill row names a 12h bar closing after the 4h open / a level inside 10 bps "
     "/ a prior close not on the near side / a wrong fill / no touch / mfe outside [fill, v6], "
     "a tp_bars row's as-of close, level or flags differ, or the tp_fills table is not the "
     "four books' TP exits with every column this file's (as-of close <= the fill bar's "
     "open)",
     tp_break, tp_real),
    ("F-TP-EXPANSION", "no order rests while the 12h lens is in EXPANSION or NONE — every bar "
     "of every campaign [L-H.1]",
     "tp_bars misses or adds a bar of (entry, v6 exit] of any v6 campaign (either scale), or on "
     "a bar whose 12h as-of state (prefix run) is BULL_EXP / BEAR_EXP / NONE the module "
     "carries a level, a live order under any mode, a fill price or another state name, or a "
     "TP book fills on such a bar",
     expansion_break, expansion_real),
    ("F-IDENTITY", "the v6 campaign set, transformed: unacted campaigns are v6 exactly "
     "[L-1.5]",
     "a paired arm's key set is not v6's or n != 200; an unacted campaign differs from v6 by "
     "any amount on net_r / gross_r / fee_r / funding_r / exit_ms / exit_close_ms / exit_px / "
     "exit_reason; an entry field differs; a TP exit falls after v6's exit or on its stop bar; "
     "the era slices do not partition the scored arm by the typed cut; the base arm differs "
     "from the lineage v6 book on any required column (200 campaigns); an exit bar is off the "
     "raw 4h grid, exit_close_ms is not its close (or after the pin), exit_stamp_ms breaks "
     "L-R.5; a sidecar's identity counts are not its own parquet's",
     identity_break, identity_real),
    ("F-ROW", "the numbers of record: n / ΣR / mean, the D15 tail ratio, the haircut, the "
     "eras, the withheld counts [L-H.1, AM-7, L-1.3]",
     "a sidecar or the report's row of record differs from this file's n / ΣR (fsum) / mean; "
     "the D15 tail ratio (typed top-decile mean law) or paired mean Δ differ on any sidecar; "
     "haircut_net_r != net − fee × slip/5.0 (typed tiers) or era != the typed law on any row; "
     "the TP order counts per campaign or the report's sentence differ; the wall-exit lesson "
     "is not named; SCALE-IN-SAMPLE differs on any regbook row / tp_bars row / the report's "
     "count; any cell of tp_summary, tp_picks (+ the regbooks' pick columns), tp_withheld "
     "(+ the WOULD-WITHHOLD label on the unguarded twin), tp_reride (this file's admission "
     "walk), tp_campaigns or tp_exit_reasons differs from this file's derivation",
     row_break, row_real),
    ("F-GRID", "every grid whole, collared, no verdict word",
     "a grid is not whole against its typed cells, a NaN stat has no reason, n = 0 has a "
     "finite stat, eras do not partition, ALL != Σ assets, a verdict column appears, a verdict "
     "word sits in a string cell of a stage table / Tier-E regbook or a Tier-E sidecar string, "
     "or the collar / as-of stamps are missing",
     grid_break, grid_real),
    ("F-KEY", "the regbook interface and the stage tables: typed columns, dtypes, keys, "
     "sidecars, collar, shas",
     "a regbook lacks a typed column or dtype, holds a null or a repeated key, a sidecar "
     "misses a typed key/value or its n / ΣR / book_sha256 (this file's canonical CSV) "
     "differ, the collar is wrong, STATUS.json is not typed, a file set is not typed, a stage "
     "key repeats, a manifest content sha is not the table's or a manifest file_sha256 is not "
     "the file's bytes",
     key_break, key_real),
    ("F-DET", "two subprocess builds under different hash seeds, one set of bytes",
     "the PYTHONHASHSEED 1 and 20260924 builds (under RUN_ROOT/_det_stage_h) differ from each "
     "other or from the canonical stage_h/ + regbooks/P-TP-RNG/ files in the file set, any "
     "byte or any parquet content sha, or either exits nonzero",
     det_break, det_real),
)


def file_transcript(out: Path, body: bytes, refile: bool) -> list[str]:
    """NEVER CLOBBER the transcript of record [tierc10_resume_fixtures.file_transcript]."""
    if not out.exists() and not refile:
        return [f"{out.name} ABSENT — nothing written; re-file with --refile-transcript"]
    if out.exists() and out.read_bytes() == body:
        return []
    if out.exists() and not refile:
        (rr := out.with_name(out.stem + "_rerun.txt")).write_bytes(body)
        return [f"{out.name} NOT byte-identical; this run -> {rr.name}; record untouched"]
    out.write_bytes(body)
    return []


def main() -> int:
    args = sys.argv[1:]
    global RUN_ROOT
    root = RUN_ROOT = Path(next((a.split("=", 1)[1] for a in args if a.startswith("--root=")),
                                OUT)).resolve()
    pick = [a.lower() for a in args if not a.startswith("--")]
    t0 = time.time()
    say(AS_OF_LINE)
    say("=" * 78)
    say("TIER-C11 STAGE H FIXTURES — scripts/tierc11_stage_h.py (P-TP-RNG: take-profit at "
        "the 12h range boundary) — break leg first, RED or void")
    say("=" * 78)
    say(f"seed {SEED} · substrate {TC11_SNAP.name} · pin {PIN} · approach {APPROACH_TYPED} ATR "
        f"· guard {GUARD_BPS_TYPED} bps · frozen {FROZEN_TYPED}")
    for ln in S.READINGS:
        say(ln)
    for fid, title, fails_if, b, r in FIXTURES:
        if not pick or any(q == fid.lower() or q in fid.lower() for q in pick):
            prove(fid, title, fails_if, b, r)
    say(f"\n  {len(PASSED)} GREEN, {len(FAILED)} RED")
    for f in FAILED:
        say(f"    RED: {f}")
    root.mkdir(parents=True, exist_ok=True)
    body = ("\n".join(LINES) + "\n").encode("utf-8")
    name = TRANSCRIPT if not pick else TRANSCRIPT.replace(".txt", "_partial.txt")
    bad = file_transcript(root / name, body, "--refile-transcript" in args or bool(pick))
    for x in bad:
        clock(x)
    for d in _PQ_DIR:
        shutil.rmtree(d, ignore_errors=True)
    clock(f"wall {time.time() - t0:.1f}s · transcript sha {sha_bytes(body)}")
    if FAILED:
        print("*** HALT: fixture mismatch. Nothing downstream is trustworthy. ***")
    return 1 if (FAILED or bad) else 0


if __name__ == "__main__":
    raise SystemExit(main())
