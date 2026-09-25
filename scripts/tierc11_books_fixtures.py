#!/usr/bin/env python
"""TIER-C11 · TC11-BOOKS — F-CTRL-a · F-CTRL-b · F-912-ANCHOR · F-AGE-ANCHOR ·
F-FIELDS · F-WINDOW-ASOF · F-KEY · F-DET.  The fixtures of scripts/tierc11_books.py
(the two frozen books and the campaign table) [LEANS L-1.6, L-1.7, L-1.3, L-G.1,
L-G.2, L-G.3, L-R.5].

TWO LEGS PER FIXTURE, the BREAK leg first, and it must go RED or the fixture is
VOID — a guard nobody has seen fail is a guard nobody has seen [the prove() law
of scripts/tierc10_rf_fixtures.py / tierc10_resume_fixtures.py].  A break leg is
a set of PLANTS judged one at a time; a plant counts as CAUGHT only if a finding
NAMES THE INTENDED DETECTOR (its expected substring).  A plant that crashes is a
FIXTURE DEFECT, never a catch.  Every plant is made on a COPY (a frame, a book,
a temp dir) or under a MUTATION of the module that is restored in `finally`; no
artifact of record moves.  The referees are typed HERE (a second object): the
filed control journal's sha256 and row count, its one corridor_end row, the
P-TRG-2 book sha prefix and n, the P_AGE_1 band counts, the 9/12 roles, the
campaign column set and its null-iff map, the tide / window / lag / era /
structure-distance laws.  The campaign fields are RE-DERIVED here from the raw
4h arrays and the Trade objects by this file's own code (engine.indicators.ema
for the EMAs, numpy for the rest) — never through the module's field code.

  F-CTRL-a      FAILS IF run_cell_n(v6 control, V6_ROLES, CLASSIC5) over the TC11
                corridor differs from tierc6.run_cell(CARD_V6) by ANY amount on
                any of TP's 12 CTRL_COLS, any exit_reason or the count differs,
                the corridor end is not 1790294400000, or corridor_n(CLASSIC5) is
                not TP.control_window().  SABOTAGE: a one-tick stop perturbation
                of ONE campaign inside the run_cell_n path (tierc7_rules.
                struct_stop_4h bent as T9.replay9 reads it); the window clause
                handed a window one bar short; compute() fed an AS_OF_PIN record
                naming another pin (must HALT ASOF-REFEREE).
  F-CTRL-b      FAILS IF the filed TC10 control journal is not the typed bytes
                (sha256 fcbf5db0…fae64c1c, 200 rows) with exactly one corridor_end
                row (ETHUSDT entered 2026-09-18T08:00Z); the module's typed
                referee is not the fixture's; any filed campaign is absent live;
                any campaign it CLOSED differs live on the 12 CTRL_COLS at its
                6 dp or on exit_reason; the continuation's entry/stop/r_dist
                differ, its live exit bar opens before the TC10 pin, or its live
                n_advances / mfe_r fall below the filed; or a live-only campaign
                entered at or before the TC10 pin.  SABOTAGE (on copies of the
                live journal): a dropped filed campaign; the continuation's stop
                one tick off; a closed campaign's net_r +1e-6; an extra campaign
                planted inside the filed window; the continuation's live exit
                moved to a stop on 2026-09-20T00:00Z; its live n_advances 0;
                compute() fed a filed journal with one closed row dropped (must
                HALT CTRL-B-REFEREE).
  F-912-ANCHOR  FAILS IF T9.SWEEP_CELLS[-1] is not the typed 9/12 roles, or
                TP._book_sha of the 9/12 book over the TC10 window differs from
                P-TRG-2.scored.json's full-arm book_sha256 (typed prefix
                b2276fa4, n 198), or the v6 base over the same window hashes
                to anything but that arm's filed base_sha256.  SABOTAGE: one
                campaign dropped; the v6 trigger (12/26) ridden under the 9/12
                name; SWEEP_CELLS[-1] swapped for trigger-9/26 (the module must
                HALT); one campaign dropped from the v6 base; compute() fed a
                P-TRG-2 arm with n 197 (must HALT 912-REFEREE).
  F-AGE-ANCHOR  FAILS IF the trailing-band assignment of the TC10-window v6 book
                does not reproduce the filed P_AGE_1_TIDE_YOUTH.parquet exactly
                (bands 01..04 + ALL, typed n 25/60/56/59/200); a TC10-window
                campaign carries another band in the written TC11 table; or, on
                EVERY campaign of BOTH written TC11 tables (and the TC10-window
                rows), the tide state / streak / left-censoring at the ENTRY bar,
                the written q25/q50/q75 or the band differ from this file's own
                derivation: streak = run length of sign(EMA89 − EMA316) of 4h
                close counted from bar 316, edges = np.quantile(0.25/0.5/0.75) of
                the pooled CLASSIC5 streak over bars with open <= the entry bar's
                open (inclusive prefix, >= 30 bars, else unbanded).  SABOTAGE:
                whole-corridor edges (LR.cuts) for the trailing ones; the
                ABSOLUTE cut (streak > 206) as the OLD edge in place of the
                trailing q75; the ARM-bar age (tierc9.tide_streak_age) for the
                ENTRY-bar one; a ONE-BAR-AHEAD pool (open <= entry + 4h) and a
                STRICT prefix (open < entry) for the inclusive one.
  F-FIELDS      FAILS IF, on EVERY campaign of BOTH written TC11 tables, against
                the Trade objects and the raw 4h arrays: the +1R latch bar is
                not the first bar j in (entry_i, exit_i] whose favourable
                extreme reaches entry ± R (or reached_1r disagrees);
                tide_abs_gt206 is not (streak > 206, typed) or abs_tide_refused
                fails the typed truth table {205: no, 206: no, 207: yes}; lag !=
                entry_i − arm_i or its band is not the typed 0 / 1-6 / 7-15 /
                >=16; r_over_atr / r_over_atr_gt_2p2 are not r_dist/ATR and
                (> 2.2, typed) at full precision; era_of_entry is not by the
                entry bar's CLOSE against 1719791999000; the TC10-pin flags
                disagree with their typed law; or exit_event_ms / _stamp is not
                the bar OPEN for a stop exit and the close otherwise [L-R.5].
                SABOTAGE (module mutations, rows rebuilt in-process): the latch
                returned one bar late; the absolute cut typed 396; the absolute
                cut read as >= 206; the P-WIN-1 lag cut moved to 17; the
                structure-distance cut moved to 2.0; every exit stamped at its
                close.  (Copies of the written table): one row's era flipped;
                the continuation flag flipped.
  F-WINDOW-ASOF FAILS IF, at the TC11 pin AND rebuilt at four earlier pins
                (2026-09-21T16:00Z, 2026-09-01, 2026-06-01, 2025-12-01), for
                either book, any window_end_i is a bar after the as-of (>
                hi_i + 1); an open window's window_end_i is not hi_i + 1, or its
                flag / close stamp disagree; a closed window's close is after
                the pin; window_end_i differs from this file's derivation
                min(first counter 12/89 EMA cross after arm_i, hi_i + 1); or a
                window closed at an earlier pin moves in the TC11 table (open
                ones must end after that pin).  SABOTAGE: the as-of cap removed
                (the module must HALT, look-ahead); a copy of the 2026-09-01
                table carrying armings9's raw (future) index on its open
                windows; the cap one bar short (hi_i); one closed window's end
                +1 in a copy.
  F-KEY         FAILS IF a written table's column list is not the typed one; has
                a duplicated (symbol|asset, entry_ms) key, a null in a key or
                typed-required column, an absent or null as-of stamp, a nullable
                column whose nulls disagree with its typed flag, TP.check_keys
                (books/) is RED, or a manifest content sha is not the table's.
                The commission (columns, required, null-iff) is TYPED HERE.
                SABOTAGE (copies): a duplicated row; a nulled net_r; harvest_i on
                an unharvested row; as_of_last_closed_4h dropped; TP.check_keys
                on a temp root holding a duplicated row; the module dropping
                `lag` from its CAMPAIGN_COLUMNS.
  F-DET         FAILS IF two subprocess builds (PYTHONHASHSEED 1, 20260924) —
                written under RUN_ROOT/_det_books (--root redirects them) —
                differ from each other or from the canonical books/ files of
                record in the file set, any file's bytes or any parquet's
                content sha, or either exits nonzero.  SABOTAGE: one byte bent in
                a copy; a parquet copy with one float moved; a hash-order-
                dependent line emitted under the two seeds.
BANNED: self-comparison; one example where cardinality was possible; a tuned
magnitude bound standing in for an identity; a check whose claim is not the
design's claim.  FROZEN SUBSTRATE: HALTs unless NAIAD_CACHE_DIR is the TC11
snapshot (tierc11_env's guard).  Seed 20260924.  The transcript carries no clock
and no temp path.

Run:  export NAIAD_CACHE_DIR=$HOME/.cache/naiad/snapshots/tc11_20260925 PYTHONDONTWRITEBYTECODE=1
      ~/venvs/naiad/bin/python -B scripts/tierc11_books.py        # the canonical build first
      ~/venvs/naiad/bin/python -B scripts/tierc11_books_fixtures.py \\
          [leg-substring ...] [--refile-transcript] [--root=DIR]
      --root=DIR redirects the transcript AND the F-DET twins (DIR/_det_books/);
      the canonical files compared against are always the record, books/.
Exit 0 = every leg GREEN, every break RED · 1 = a RED or VOID fixture, a
transcript finding, or a HALT.
"""
from __future__ import annotations

import contextlib
import dataclasses
import hashlib
import io
import json
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
import tierc11_books as B                                            # noqa: E402  (guards first)

import numpy as np                                                   # noqa: E402
import pandas as pd                                                  # noqa: E402
import engine.indicators as IND                                      # noqa: E402  (the EMA law, L-R.1)

E = B.E
TP, T9, T6, TB, LR = E.TP, E.T9, E.T6, E.TB, E.LAB
iso = TB.iso

# ── FIXTURE-TYPED LITERALS: the commission, a second object, never B's own ──
TC11_SNAP = Path.home() / ".cache" / "naiad" / "snapshots" / "tc11_20260925"
PIN = 1790294400000                      # 2026-09-25T00:00:00Z [L-0.1]
TC10_PIN = 1790006400000                 # 2026-09-21T16:00:00Z
MS4H = 14_400_000
SEED = 20260924
DET_SEEDS = (1, SEED)
AS_OF_LINE = "as_of_last_closed_4h: 2026-09-25T00:00:00Z"
# L-1.7 "(200 rows, sha fcbf5db0…)"; the full sha from PROGRESS PANEL/gate (scout B §3)
FILED_JOURNAL_SHA = "fcbf5db0480416b0a5c7f704987980aea220650cb0764d5dd4095611fae64c1c"
FILED_JOURNAL_N = 200
FILED_CONTINUATIONS = [("ETHUSDT", "2026-09-18T08:00:00Z")]
CONT_EXIT_PLANT = "2026-09-20T00:00:00Z"  # inside the window the filed journal says was open
CTRL_COLS_TYPED = ("entry_ms", "exit_ms", "entry_px", "exit_px", "stop_px", "r_dist",
                   "net_r", "gross_r", "fee_r", "funding_r", "mfe_r", "n_advances")
TRG2_SHA_PREFIX = "b2276fa4"             # L-1.6 "book_sha256 b2276fa4…"
TRG2_N = 198
ROLES_912 = {"name": "trigger-9/12", "tide_f": 89, "tide_s": 316, "win_f": 12,
             "win_s": 89, "trg_f": 9, "trg_s": 12}
PAGE1_N = {"01": 25, "02": 60, "03": 56, "04": 59, "99-ALL": 200}   # P_AGE_1_TIDE_YOUTH
KEYS_TYPED = {"v6_journal": ["asset", "entry_ms"], "trg912_journal": ["asset", "entry_ms"],
              "v6_campaigns": ["symbol", "entry_ms"], "trg912_campaigns": ["symbol", "entry_ms"]}
FILES_TYPED = ("BOOKS.md", "build_manifest.json", "trg912_campaigns.parquet",
               "trg912_journal.parquet", "v6_campaigns.parquet", "v6_journal.parquet")
CLASSIC5_TYPED = ("BTCUSDT", "ETHUSDT", "SOLUSDT", "NEARUSDT", "ZECUSDT")
# the tide law [L-G.1]: sign(EMA89 − EMA316) of 4h close, counted from warm bar 316
TIDE_F, TIDE_S, TIDE_WARM = 89, 316, 316
STREAK_Q = (0.25, 0.50, 0.75)
POOL_MIN = 30                            # L-G.1 "(tierc9._trailing_edges, >= 30 bars)"
BAND_LABELS_TYPED = {"B1": "B1 YOUNG tide", "B2": "B2 EARLY tide", "B3": "B3 MATURE tide",
                     "B4": "B4 OLD tide"}
ABS_CUT_TYPED = 206                      # L-G.1 "refuse streak > 206, exactly as written"
ABS_TRUTH = {205: False, 206: False, 207: True}
WIN_F, WIN_S = 12, 89                    # the window: EMA12/EMA89 of 4h close; counter cross ends it
LAG_TYPED = (("0", 0, 0), ("1-6", 1, 6), ("7-15", 7, 15), (">=16", 16, None))   # L-G.2
RATR_CUT_TYPED = 2.2                     # L-G.3
ERA_CUT_TYPED = 1_719_791_999_000        # L-1.3: tuning closes <= 2024-06-30T23:59:59Z
EARLY_PINS = ("2026-09-21T16:00:00Z", "2026-09-01T00:00:00Z", "2026-06-01T00:00:00Z",
              "2025-12-01T00:00:00Z")
# the campaign table's commission: every column, in order, then the as-of stamps
CAMPAIGN_COLUMNS_TYPED = (
    "symbol", "entry_ms", "book", "roles_name", "lane", "direction",
    "arm_i", "arm_open_ms", "arm_close_ms",
    "entry_i", "entry_open_ms", "entry_close_ms",
    "exit_i", "exit_ms", "exit_close_ms", "exit_event_ms", "exit_event_stamp",
    "exit_reason", "open_at_asof",
    "entry_px", "stop_px", "r_dist", "atr_at_entry", "r_over_atr", "r_over_atr_gt_2p2",
    "lag", "lag_band", "window_end_i", "window_end_close_ms", "window_open_at_asof",
    "harvested", "harvest_i", "harvest_close_ms",
    "reached_1r", "latch_1r_i", "latch_1r_open_ms",
    "net_r", "gross_r", "fee_r", "funding_r",
    "era_of_entry", "entry_bar_straddles_era_cut",
    "tide_state_entry", "tide_streak_entry", "tide_left_censored",
    "tide_trailing_edge_q25", "tide_trailing_edge_q50", "tide_trailing_edge_q75",
    "tide_band", "tide_band_label",
    "tide_abs_gt206", "tide_streak_age_arm", "tide_streak_age_arm_censored",
    "entered_after_tc10_pin", "continuation",
)
AS_OF_TYPED = ("as_of_last_closed_4h", "as_of_panel_start", "as_of_span_days", "warranty",
               "as_of_lens", "as_of_last_closed_bar", "as_of_panel", "as_of_n_assets",
               "as_of_substrate")
NULL_IFF_TYPED = {                      # column -> (flag column, flag value when null)
    "window_end_close_ms": ("window_open_at_asof", True),
    "harvest_i": ("harvested", False),
    "harvest_close_ms": ("harvested", False),
    "latch_1r_i": ("reached_1r", False),
    "latch_1r_open_ms": ("reached_1r", False),
    "tide_trailing_edge_q25": ("tide_band", None),
    "tide_trailing_edge_q50": ("tide_band", None),
    "tide_trailing_edge_q75": ("tide_band", None),
    "tide_band_label": ("tide_band", None),
}
NULLABLE_TYPED = tuple(NULL_IFF_TYPED) + ("tide_band",)
JOURNAL_REQUIRED_TYPED = ("asset", "lane", "entry_ms", "direction", "arm_ms", "exit_reason",
                          "exit_ts") + CTRL_COLS_TYPED

OUT = B.OUT
DET_ROOT = B.DET_ROOT
RUN_ROOT = OUT
TRANSCRIPT = "FIXTURES_BOOKS.txt"
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
def mutated(obj, name: str, value):
    """A MUTATION of the module under trial, restored in `finally`."""
    old = getattr(obj, name)
    setattr(obj, name, value)
    try:
        yield
    finally:
        setattr(obj, name, old)


def _env() -> dict:
    return dict(os.environ, NAIAD_CACHE_DIR=str(TC11_SNAP), PYTHONDONTWRITEBYTECODE="1")


def price_tick(stem: str) -> float:
    """The venue's price tick from the TC11 record CONTRACT_SPECS.json."""
    spec = json.loads((E.OUT / "data" / "CONTRACT_SPECS.json").read_text(encoding="utf-8"))
    for a in spec["assets"]:
        if a["stem"] == stem:
            return float(a["price_tick"])
    raise RuntimeError(f"no price_tick for {stem}")


_MEMO: dict = {}


def live() -> dict:
    """The in-process books this fixture judges (ridden once, reused)."""
    if not _MEMO:
        lo, hi, meta = B.corridor()
        lo10, hi10, _ = B.tc10_window()
        v6 = B.v6_book(lo, hi)
        b912 = B.trg912_book(lo, hi)
        _MEMO.update({"lo": lo, "hi": hi, "meta": meta, "lo10": lo10, "hi10": hi10,
                      "v6": v6, "trg912": b912, "j_v6": TP.journal_frame(v6),
                      "want_j": TP.journal_frame(T6.run_cell(B.V6RULES.CARD_V6, lo, hi)),
                      "pool": B.tide_pool(lo, hi)})
    return _MEMO


def written() -> dict:
    """The four tables of record, read back from books/."""
    return {s: pd.read_parquet(OUT / f"{s}.parquet") for s in KEYS_TYPED}


def rebuild(name: str, pin_iso: str | None = None) -> pd.DataFrame:
    """B.campaign_rows for one book over the TC11 corridor (or an earlier pin),
    in-process, at full precision — the path a module MUTATION is judged on."""
    L = live()
    if pin_iso is None:
        lo, hi, bk, pool = L["lo"], L["hi"], L[name], L["pool"]
    else:
        lo, hi, _ = B.corridor(pin_iso)
        bk = B.v6_book(lo, hi) if name == "v6" else B.trg912_book(lo, hi)
        pool = B.tide_pool(lo, hi)
    roles = T9.V6_ROLES if name == "v6" else B.r912()
    return B.campaign_rows(bk, roles, lo, hi, pool, name)


# ═══════════════════════════════════════ INDEPENDENT DERIVATIONS (this file's)
_TAPE: dict = {}


def tape(sym: str) -> dict:
    """The raw 4h arrays (the substrate) and this file's own EMAs / tide."""
    if sym not in _TAPE:
        f = T9.frame(sym)["f"]
        c = np.asarray(f.c, float)
        d = {"o": np.asarray(f.open_ms, np.int64), "c": c,
             "h": np.asarray(f.h, float), "l": np.asarray(f.l, float)}
        e89, e316 = IND.ema(c, TIDE_F), IND.ema(c, TIDE_S)
        n = len(c)
        st, run, start = np.zeros(n, int), np.full(n, -1, int), np.full(n, -1, int)
        cur = -1
        for j in range(TIDE_WARM, n):            # a plain loop: not the lab's vectorised form
            s_ = 1 if e89[j] > e316[j] else -1
            if j == TIDE_WARM or s_ != st[j - 1]:
                cur = j
            st[j], start[j], run[j] = s_, cur, j - cur + 1
        d.update({"tide_state": st, "tide_run": run, "tide_start": start})
        e12, e89w = IND.ema(c, WIN_F), IND.ema(c, WIN_S)
        dn = np.zeros(n, bool)
        up = np.zeros(n, bool)
        dn[1:] = (e12[1:] < e89w[1:]) & (e12[:-1] >= e89w[:-1])
        up[1:] = (e12[1:] > e89w[1:]) & (e12[:-1] <= e89w[:-1])
        d.update({"win_dn": dn, "win_up": up})
        _TAPE[sym] = d
    return _TAPE[sym]


def hi_index(sym: str, pin_ms: int) -> int:
    """The last bar CLOSED by the pin (open + 4h <= pin)."""
    return int(np.flatnonzero(tape(sym)["o"] + MS4H <= pin_ms)[-1])


_POOL: dict = {}


def indep_pool(lo: int, hi: int) -> tuple[np.ndarray, np.ndarray]:
    """(values, open times) of the pooled CLASSIC5 streak, bars with lo <= open
    <= hi and a warm streak, sorted by time."""
    k = (lo, hi)
    if k not in _POOL:
        vs, ts = [], []
        for s in CLASSIC5_TYPED:
            t = tape(s)
            m = (t["o"] >= lo) & (t["o"] <= hi) & (t["tide_run"] > 0)
            vs.append(t["tide_run"][m])
            ts.append(t["o"][m])
        v, tm = np.concatenate(vs), np.concatenate(ts)
        o = np.argsort(tm, kind="stable")
        _POOL[k] = (v[o], tm[o])
    return _POOL[k]


def indep_edges(pool: tuple, at_ms: int, shift_ms: int = 0) -> list | None:
    v, tm = pool
    m = tm <= at_ms + shift_ms
    if int(m.sum()) < POOL_MIN:
        return None
    return [float(x) for x in np.quantile(v[m], STREAK_Q)]


def typed_band(run: int, ed) -> str | None:
    if ed is None or run <= 0:
        return None
    return f"B{1 + sum(1 for e in ed if run >= e)}"


def typed_lag_band(lag: int) -> str:
    for name, a, b in LAG_TYPED:
        if lag >= a and (b is None or lag <= b):
            return name
    return "NONE"


def indep_latch(t) -> int | None:
    tp = tape(t.symbol)
    d, px, R = int(t.direction), float(t.entry_px), float(t.r_dist)
    seg = (tp["h"] if d == 1 else tp["l"])[int(t.entry_i) + 1:int(t.exit_i) + 1]
    hit = np.flatnonzero((seg - px) * d / R >= 1.0)
    return int(t.entry_i) + 1 + int(hit[0]) if hit.size else None


def _nul(x) -> bool:
    return x is None or (not isinstance(x, str) and pd.isna(x))


def _r6(x) -> float:
    return round(float(x), 6)


# ═══════════════════════════════════════════════════════════════ F-CTRL-a
def ctrl_a_break():
    L = live()
    lo, hi = L["lo"], L["hi"]
    t0 = L["v6"][0]
    tick = price_tick(t0.symbol)
    orig = T9.RC.struct_stop_4h
    hits = []

    def bent(pv, cur_i, entry_px, direction, atr_sig, *a, **k):
        st = orig(pv, cur_i, entry_px, direction, atr_sig, *a, **k)
        if (st is not None and int(cur_i) == int(t0.entry_i)
                and float(entry_px) == float(t0.entry_px)):
            new = float(st.stop_px) - int(direction) * tick
            st = dataclasses.replace(st, stop_px=new, r_dist=abs(float(entry_px) - new))
            hits.append(int(cur_i))
        return st

    def one_tick():
        with mutated(T9.RC, "struct_stop_4h", bent):
            got = TP.journal_frame(B.v6_book(lo, hi))
        f, _ = B.ctrl_a_findings(got, L["want_j"], lo, hi)
        return [x + f" [bent {len(hits)} stop(s): {t0.symbol} {iso(int(t0.entry_ms))} "
                    f"one tick {tick}]" for x in f]

    def other_pin():
        rec = dict(B.as_of_pin_record())
        rec["as_of_last_closed_4h_close_ms"] = PIN - MS4H
        with mutated(B, "as_of_pin_record", lambda: rec):
            B.compute()
        return []

    return plants([
        ("one-tick stop perturbation of ONE campaign inside run_cell_n "
         "(tierc7_rules.struct_stop_4h as T9.replay9 reads it)", "CTRL-A-DIFF", one_tick),
        ("the window clause handed (lo, hi - 4h)", "CTRL-A-WINDOW",
         lambda: B.ctrl_a_findings(L["j_v6"], L["want_j"], lo, hi - TP.MS_4H)[0]),
        ("compute() fed an AS_OF_PIN record naming the bar before the pin",
         "ASOF-REFEREE", other_pin),
    ])


def ctrl_a_real():
    L = live()
    lo, hi = L["lo"], L["hi"]
    f, info = B.ctrl_a(lo, hi)
    cols = tuple(TP.CTRL_COLS) == CTRL_COLS_TYPED
    rec = B.as_of_pin_record()
    g_pin = int(rec["as_of_last_closed_4h_close_ms"]) == PIN
    ok = (not f and hi + 1 == PIN and info["worst"] == 0.0 and info["n"] > 0
          and info["window_ok"] and cols and g_pin)
    net = sum(float(t.net_r) for t in L["v6"])
    return ok, (f"TC11 corridor {iso(lo)} -> {iso(hi + 1)} (end == pin {PIN}: {hi + 1 == PIN}; "
                f"AS_OF_PIN.json names it: {g_pin}, latest closed 4h at fetch time "
                f"{rec['latest_closed_4h_at_pin_run']}); "
                f"corridor_n(CLASSIC5) == TP.control_window(): {info['window_ok']}; "
                f"TP.CTRL_COLS == the typed 12: {cols}; run_cell_n(v6-control, V6_ROLES, "
                f"CLASSIC5) vs tierc6.run_cell(CARD_V6): {info['why']} — WORST ABS DIFF "
                f"{info['worst']:.3e} (bar EXACTLY 0.000e+00); net ΣR {net:+.6f}"
                + (f"; findings {f}" if f else ""))


# ═══════════════════════════════════════════════════════════════ F-CTRL-b
def ctrl_b_break():
    L = live()
    filed, _, _ = B.filed_control_journal()
    j = L["j_v6"]
    closed = filed[filed["exit_reason"] != "corridor_end"]
    k0 = (closed["asset"].iloc[0], int(closed["entry_ms"].iloc[0]))
    ci = filed[filed["exit_reason"] == "corridor_end"].iloc[0]

    def at_cont(c):
        return (c["asset"] == ci["asset"]) & (c["entry_ms"].astype(int) == int(ci["entry_ms"]))

    def drop():
        c = j[~((j["asset"] == k0[0]) & (j["entry_ms"].astype(int) == k0[1]))]
        return B.ctrl_b_findings(c, filed, TC10_PIN)[0]

    def cont_tick():
        c = j.copy()
        m = at_cont(c)
        c.loc[m, "stop_px"] = c.loc[m, "stop_px"] - price_tick(str(ci["asset"]))
        return B.ctrl_b_findings(c, filed, TC10_PIN)[0]

    def net_nudge():
        c = j.copy()
        m = (c["asset"] == k0[0]) & (c["entry_ms"].astype(int) == k0[1])
        c.loc[m, "net_r"] = c.loc[m, "net_r"] + 1e-6
        return B.ctrl_b_findings(c, filed, TC10_PIN)[0]

    def early():
        c = j.copy()
        extra = c.iloc[[0]].copy()
        extra["entry_ms"] = TC10_PIN - 2 * TP.MS_4H          # entry bar closes before the pin
        return B.ctrl_b_findings(pd.concat([c, extra], ignore_index=True), filed,
                                 TC10_PIN)[0]

    def cont_exit_inside():
        c = j.copy()
        m = at_cont(c)
        c.loc[m, "exit_ms"] = TP._iso_ms(CONT_EXIT_PLANT)
        c.loc[m, "exit_reason"] = "stop"
        return B.ctrl_b_findings(c, filed, TC10_PIN)[0]

    def cont_adv():
        c = j.copy()
        c.loc[at_cont(c), "n_advances"] = 0
        return B.ctrl_b_findings(c, filed, TC10_PIN)[0]

    def referee():
        i = filed.index[filed["exit_reason"] != "corridor_end"][0]
        f2 = filed.drop(index=i).reset_index(drop=True)
        buf = io.BytesIO()
        f2.to_parquet(buf, index=False)
        b = buf.getvalue()
        # without the pin, F-CTRL(b) cannot see this: every row left still matches
        silent = B.ctrl_b_findings(j, f2, TC10_PIN)[0]
        with mutated(B, "filed_control_journal", lambda: (f2, sha_bytes(b), len(b))):
            B.compute()
        return [f"compute() did not HALT (ctrl_b_findings alone: {silent})"]

    return plants([
        (f"a campaign the filed journal CLOSED ({k0[0]} {iso(k0[1])}) dropped from the "
         f"live journal copy", "CTRL-B-MISSING", drop),
        ("the continuation's stop one tick off in the live copy", "CTRL-B-CONTINUATION",
         cont_tick),
        ("one closed campaign's net_r +1e-6 in the live copy", "CTRL-B-CLOSED", net_nudge),
        ("an extra live campaign planted one bar before the TC10 pin", "CTRL-B-EARLY", early),
        (f"the continuation's live exit moved to a stop on {CONT_EXIT_PLANT} (inside the "
         f"filed open window)", "before the filed as-of", cont_exit_inside),
        ("the continuation's live n_advances set to 0 (below the filed 1)",
         "not a prefix of the live one", cont_adv),
        ("compute() fed a filed journal with one CLOSED row dropped (re-serialised)",
         "CTRL-B-REFEREE", referee),
    ])


def ctrl_b_real():
    L = live()
    filed, sha, nbytes = B.filed_control_journal()
    f, info = B.ctrl_b_findings(L["j_v6"], filed, TC10_PIN)
    ce = [(str(r.asset), iso(int(r.entry_ms))) for r in
          filed[filed["exit_reason"] == "corridor_end"].itertuples(index=False)]
    g_sha = sha == FILED_JOURNAL_SHA
    g_n = len(filed) == FILED_JOURNAL_N
    g_ce = ce == FILED_CONTINUATIONS
    g_ref = B.FILED_JOURNAL_SHA == FILED_JOURNAL_SHA and B.FILED_JOURNAL_N == FILED_JOURNAL_N
    g_cov = info["n_closed_compared"] + info["n_continuation"] == len(filed)
    live_after = [(a, m) for a, m in zip(L["j_v6"]["asset"], L["j_v6"]["entry_ms"].astype(int))
                  if m + TP.MS_4H > TC10_PIN]
    new = [(a, iso(m)) for a, m in live_after
           if (a, iso(m)) not in {(x, iso(int(y))) for x, y in
                                  zip(filed["asset"], filed["entry_ms"])}]
    g_new = sorted(new) == sorted(tuple(x) for x in info["new"])
    ok = not f and g_sha and g_n and g_ce and g_cov and g_new and g_ref
    cont = "; ".join(f"{x['asset']} entered {x['entry_ts']}: filed exit {x['filed_exit']} "
                     f"-> live exit {x['live_exit']}" for x in info["continuations"])
    return ok, (f"filed control_journal.parquet sha256 {sha[:16]}… == typed "
                f"{FILED_JOURNAL_SHA[:8]}…: {g_sha} ({nbytes} B); rows {len(filed)} == "
                f"{FILED_JOURNAL_N}: {g_n}; the module's pinned referee == the fixture's: "
                f"{g_ref}; corridor_end rows {ce} == typed "
                f"{FILED_CONTINUATIONS}: {g_ce}; every filed campaign present live "
                f"({info['n_shared']}/{info['n_filed']}); {info['n_closed_compared']} closed "
                f"campaigns EXACT on the 12 CTRL_COLS at 6 dp + exit_reason, "
                f"{info['n_continuation']} continuation(s) exact on entry/stop/r_dist, live "
                f"exit bar at or after the TC10 pin, n_advances and mfe_r no smaller than "
                f"filed (covers every filed row: {g_cov}) — {cont}; live-only (new) campaigns "
                f"{info['new'] or 'none'} (the live entries after the TC10 pin, recounted "
                f"here: {new or 'none'}; agree {g_new})"
                + (f"; findings {f}" if f else ""))


# ═══════════════════════════════════════════════════════════ F-912-ANCHOR
def a912_break():
    L = live()
    lo10, hi10 = L["lo10"], L["hi10"]
    filed = B.filed_trg2()
    b10 = B.trg912_book(lo10, hi10)
    swapped = T9.SWEEP_CELLS[:-1] + (dataclasses.replace(T9.SWEEP_CELLS[-1],
                                                         name="trigger-9/26", trg_s=26),)

    def v6_under_912():
        bk = [t for s in E.CLASSIC5
              for t in T9.replay9(s, TP.CONTROL_CARD, T9.V6_ROLES, lo10, hi10)[1]]
        return B.trg912_anchor_findings(bk, filed)[0]

    def swap():
        with mutated(T9, "SWEEP_CELLS", swapped):
            return B.trg912_anchor_findings(B.trg912_book(lo10, hi10), filed)[0]

    def referee():
        arm = dict(filed)
        arm["n"] = int(arm["n"]) - 1
        with mutated(B, "filed_trg2", lambda: arm):
            B.compute()
        return ["compute() did not HALT"]

    v6_10 = B.v6_book(lo10, hi10)

    return plants([
        ("one campaign dropped from the TC10-window 9/12 book", "912-SHA",
         lambda: B.trg912_anchor_findings(b10[1:], filed)[0]),
        ("the v6 trigger (12/26) ridden under the 9/12 name", "912-SHA", v6_under_912),
        ("T9.SWEEP_CELLS[-1] swapped for trigger-9/26 (a mutated tuple)",
         "T9.SWEEP_CELLS[-1] is", swap),
        ("one campaign dropped from the TC10-window v6 base", "912-BASE",
         lambda: B.trg912_anchor_findings(b10, filed, v6_10[1:])[0]),
        ("compute() fed a P-TRG-2 full arm with n 197", "912-REFEREE", referee),
    ])


def a912_real():
    L = live()
    cell = B.r912()
    g_roles = dataclasses.asdict(cell) == ROLES_912
    filed = B.filed_trg2()
    rec = json.loads(E.tc10_record(B.TRG2_REL).read_text(encoding="utf-8"))
    vz = rec["arms"]["trg-9/12 vs zero · CLASSIC5 · full"]["book_sha256"]
    b10 = B.trg912_book(L["lo10"], L["hi10"])
    v6_10 = B.v6_book(L["lo10"], L["hi10"])
    f, info = B.trg912_anchor_findings(b10, filed, v6_10)
    g_pre = filed["book_sha256"].startswith(TRG2_SHA_PREFIX) and int(filed["n"]) == TRG2_N
    g_ref = B.TRG2_BOOK_SHA.startswith(TRG2_SHA_PREFIX) and B.TRG2_N == TRG2_N
    g_vz = vz == info["sha"]
    b11 = L["trg912"]
    ok = not f and g_roles and g_pre and g_vz and info["n"] == TRG2_N and g_ref
    return ok, (f"T9.SWEEP_CELLS[-1] == the typed roles {ROLES_912}: {g_roles}; the 9/12 book "
                f"over the TC10 window [{iso(L['lo10'])}, {iso(L['hi10'] + 1)}): n "
                f"{info['n']}, TP._book_sha {info['sha']} == P-TRG-2.scored.json full-arm "
                f"book_sha256 {filed['book_sha256'][:16]}… (typed prefix {TRG2_SHA_PREFIX}, "
                f"n {TRG2_N}: {g_pre}; the module's pinned referee agrees: {g_ref}); the "
                f"vs-zero arm binds the same sha: {g_vz}; the v6 "
                f"base over the same window (n {len(v6_10)}) TP._book_sha {info['base_sha']} "
                f"== the arm's filed base_sha256 {filed['base_sha256'][:16]}…: "
                f"{info['base_sha'] == filed['base_sha256']}; beside — the TC11-corridor 9/12 "
                f"book n {len(b11)} sha {B.book_sha(b11)[:16]}…"
                + (f"; findings {f}" if f else ""))


# ═══════════════════════════════════════════════════════════ F-AGE-ANCHOR
def edge_findings(df: pd.DataFrame, pool: tuple, name: str) -> list[str]:
    """Per campaign, this file's derivation vs the table:
      EDGE-STREAK  tide state / streak / left-censoring at the ENTRY bar;
      EDGE-CAUSAL  q25/q50/q75 vs the INCLUSIVE prefix (open <= the entry bar's
                   open) of the pooled CLASSIC5 streak, at the table's 6 dp;
      EDGE-BAND    the band (typed digitize) and its label."""
    out = []
    for r in df.itertuples(index=False):
        tp = tape(r.symbol)
        i = int(r.entry_i)
        run, st, cens = int(tp["tide_run"][i]), int(tp["tide_state"][i]), \
            bool(int(tp["tide_start"][i]) == TIDE_WARM)
        k = f"{name} {r.symbol} {iso(int(r.entry_ms))}"
        if (int(r.tide_streak_entry), int(r.tide_state_entry), bool(r.tide_left_censored)) \
                != (run, st, cens):
            out.append(f"EDGE-STREAK {k}: table (streak {r.tide_streak_entry}, state "
                       f"{r.tide_state_entry}, censored {r.tide_left_censored}) != derived "
                       f"({run}, {st}, {cens})")
        ed = indep_edges(pool, int(tp["o"][i]))
        got = [r.tide_trailing_edge_q25, r.tide_trailing_edge_q50, r.tide_trailing_edge_q75]
        if ed is None:
            if not all(_nul(x) for x in got):
                out.append(f"EDGE-CAUSAL {k}: edges {got} written but the inclusive prefix "
                           f"holds < {POOL_MIN} bars")
        elif any(_nul(x) for x in got) or [_r6(x) for x in got] != [_r6(x) for x in ed]:
            out.append(f"EDGE-CAUSAL {k}: written edges {got} != inclusive-prefix quantiles "
                       f"{ed} (bars with open <= {iso(int(tp['o'][i]))})")
        band = typed_band(run, ed)
        gb = None if _nul(r.tide_band) else str(r.tide_band)
        gl = None if _nul(r.tide_band_label) else str(r.tide_band_label)
        if gb != band or gl != (BAND_LABELS_TYPED[band] if band else None):
            out.append(f"EDGE-BAND {k}: band {gb} / {gl!r} != derived {band}")
    return out


def age_break():
    L = live()
    lo10, hi10 = L["lo10"], L["hi10"]
    v6_10 = B.v6_book(lo10, hi10)
    pool10 = B.tide_pool(lo10, hi10)
    filed = B.filed_page1()
    whole = LR.cuts(lo10, hi10)["streak_bar"]
    ipool = indep_pool(L["lo"], L["hi"])

    def whole_edges():
        return B.age_anchor_findings(B.age_band_rows(v6_10, pool10, edges=lambda t: whole),
                                     filed)

    def absolute_old():
        def ed(t):
            e = B.trailing_edges(t, pool10)
            cut = float(ABS_CUT_TYPED + 1)           # B4 = run >= 207 == run > 206
            return None if e is None else [min(e[0], cut), min(e[1], cut), cut]
        return B.age_anchor_findings(B.age_band_rows(v6_10, pool10, edges=ed), filed)

    def arm_bar():
        return B.age_anchor_findings(
            B.age_band_rows(v6_10, pool10,
                            age=lambda t: T9.tide_streak_age(t, T9.V6_ROLES)), filed)

    def shifted(shift_ms: int):
        def te(t, pool):
            f = T9.frame(t.symbol)["f"]
            return T9._trailing_edges(pool, int(f.open_ms[int(t.entry_i)]) + shift_ms
                                      )["streak_bar"]

        def run():
            with mutated(B, "trailing_edges", te):
                df = rebuild("v6")
            return edge_findings(df, ipool, "v6")
        return run

    return plants([
        (f"whole-corridor edges {whole} (LR.cuts) for the trailing ones", "AGE-ANCHOR",
         whole_edges),
        ("the ABSOLUTE cut (streak > 206) as the OLD edge in place of the trailing q75",
         "AGE-ANCHOR band 04", absolute_old),
        ("the ARM-bar age (tierc9.tide_streak_age) for the ENTRY-bar LR.tide_streak",
         "AGE-ANCHOR", arm_bar),
        ("a ONE-BAR-AHEAD pool (open <= entry + 4h) in the module's trailing_edges, v6 "
         "rows rebuilt", "EDGE-CAUSAL", shifted(MS4H)),
        ("a STRICT prefix (open < entry) in the module's trailing_edges, v6 rows rebuilt",
         "EDGE-CAUSAL", shifted(-1)),
    ])


def age_real():
    L = live()
    lo10, hi10 = L["lo10"], L["hi10"]
    v6_10 = B.v6_book(lo10, hi10)
    pool10 = B.tide_pool(lo10, hi10)
    rows = B.age_band_rows(v6_10, pool10)
    filed = B.filed_page1()
    f = B.age_anchor_findings(rows, filed)
    n_of = {str(b): int(n) for b, n in zip(rows["band"], rows["n"])}
    g_n = n_of == PAGE1_N
    # the written TC11 table carries the same band on every TC10-window campaign
    c10 = B.campaign_rows(v6_10, T9.V6_ROLES, lo10, hi10, pool10, "v6")
    W = written()
    c11 = W["v6_campaigns"]
    m = c10.merge(c11, on=["symbol", "entry_ms"], suffixes=("_10", ""))
    moved = int((m["tide_band_10"] != m["tide_band"]).sum())
    g_pref = len(m) == len(c10) and moved == 0
    # the per-campaign identity on EVERY row of both written tables and the TC10 rows
    ip11, ip10 = indep_pool(L["lo"], L["hi"]), indep_pool(lo10, hi10)
    ef = (edge_findings(W["v6_campaigns"], ip11, "v6") +
          edge_findings(W["trg912_campaigns"], ip11, "trg912") +
          edge_findings(c10, ip10, "v6@tc10"))
    n_id = len(W["v6_campaigns"]) + len(W["trg912_campaigns"]) + len(c10)
    unb = int(W["v6_campaigns"]["tide_band"].isna().sum() +
              W["trg912_campaigns"]["tide_band"].isna().sum())
    ok = not f and g_n and g_pref and not ef
    cells = " · ".join(f"{r.band} n {r.n} ΣR {r.net_r:+.4f} E {r.expectancy_r:+.4f}"
                       for r in rows.itertuples(index=False))
    return ok, (f"TC10-window v6 book n {len(v6_10)}, trailing bands reproduce "
                f"P_AGE_1_TIDE_YOUTH.parquet EXACTLY on {len(B.AGE_COMPARE)} columns x "
                f"{len(rows)} rows ({cells}); band n == typed {PAGE1_N}: {g_n}; the written "
                f"TC11 v6_campaigns.parquet carries the same band on {len(m)}/{len(c10)} "
                f"TC10-window campaigns ({moved} moved); per-campaign identity (streak, "
                f"state, censoring, q25/q50/q75 vs the INCLUSIVE prefix, band, label) "
                f"re-derived by this file on {n_id} rows ({len(W['v6_campaigns'])} v6 + "
                f"{len(W['trg912_campaigns'])} 9/12 + {len(c10)} TC10-window; {unb} unbanded "
                f"in the TC11 tables): {len(ef)} mismatch(es)"
                + (f"; findings {(f + ef)[:4]}" if (f or ef) else ""))


# ═══════════════════════════════════════════════════════════════ F-FIELDS
def fields_findings(df: pd.DataFrame, trades: dict, name: str) -> list[str]:
    """Every campaign's derived fields vs this file's typed laws (see F-FIELDS)."""
    out = []
    for x, want in ABS_TRUTH.items():
        if bool(B.abs_tide_refused(x)) != want:
            out.append(f"FIELD-ABS206 truth table: abs_tide_refused({x}) is "
                       f"{bool(B.abs_tide_refused(x))}, typed {want} (refuse streak > 206)")
    seen = set()
    for r in df.itertuples(index=False):
        key = (str(r.symbol), int(r.entry_ms))
        seen.add(key)
        t = trades.get(key)
        k = f"{name} {key[0]} {iso(key[1])}"
        if t is None:
            out.append(f"FIELD-KEY {k}: no Trade")
            continue
        tp = tape(t.symbol)
        # the +1R latch
        j = indep_latch(t)
        gj = None if _nul(r.latch_1r_i) else int(r.latch_1r_i)
        go = None if _nul(r.latch_1r_open_ms) else int(r.latch_1r_open_ms)
        if gj != j or go != (int(tp["o"][j]) if j is not None else None) \
                or bool(r.reached_1r) != (j is not None) or bool(t.reached_1r) != (j is not None):
            out.append(f"FIELD-LATCH {k}: latch {gj} (open {go}, reached {r.reached_1r}) != "
                       f"derived {j}")
        # the absolute tide shadow
        run = int(tp["tide_run"][int(t.entry_i)])
        if bool(r.tide_abs_gt206) != (run > ABS_CUT_TYPED):
            out.append(f"FIELD-ABS206 {k}: tide_abs_gt206 {r.tide_abs_gt206} but streak {run} "
                       f"(> {ABS_CUT_TYPED}: {run > ABS_CUT_TYPED})")
        # lag
        lag = int(t.entry_i) - int(t.arm_i)
        if int(r.lag) != lag or str(r.lag_band) != typed_lag_band(lag):
            out.append(f"FIELD-LAG {k}: lag {r.lag} / {r.lag_band} != {lag} / "
                       f"{typed_lag_band(lag)}")
        # structure distance
        ra = float(t.r_dist) / float(t.atr_at_entry)
        if bool(r.r_over_atr_gt_2p2) != (ra > RATR_CUT_TYPED) or _r6(r.r_over_atr) != _r6(ra):
            out.append(f"FIELD-RATR {k}: r_over_atr {r.r_over_atr} gt {r.r_over_atr_gt_2p2} != "
                       f"{ra!r} (> {RATR_CUT_TYPED}: {ra > RATR_CUT_TYPED})")
        # era by the entry bar's CLOSE
        ec = int(t.entry_ms) + MS4H
        era = "tuning" if ec <= ERA_CUT_TYPED else "holdout"
        strad = int(t.entry_ms) <= ERA_CUT_TYPED < ec
        if str(r.era_of_entry) != era or bool(r.entry_bar_straddles_era_cut) != strad \
                or int(r.entry_close_ms) != ec:
            out.append(f"FIELD-ERA {k}: era {r.era_of_entry} (straddle "
                       f"{r.entry_bar_straddles_era_cut}) != {era} ({strad})")
        # the TC10-pin flags
        after = ec > TC10_PIN
        cont = ec <= TC10_PIN <= int(t.exit_ms)
        if bool(r.entered_after_tc10_pin) != after or bool(r.continuation) != cont:
            out.append(f"FIELD-TC10 {k}: entered_after {r.entered_after_tc10_pin} / "
                       f"continuation {r.continuation} != {after} / {cont}")
        # the L-R.5 exit stamp
        ev = ((int(t.exit_ms), "intrabar_open") if str(t.exit_reason) == "stop"
              else (int(t.exit_ms) + MS4H, "close"))
        if (int(r.exit_event_ms), str(r.exit_event_stamp)) != ev \
                or int(r.exit_close_ms) != int(t.exit_ms) + MS4H:
            out.append(f"FIELD-EXIT-EVENT {k}: ({r.exit_event_ms}, {r.exit_event_stamp}) != "
                       f"{ev} for exit_reason {t.exit_reason}")
    miss = sorted(set(trades) - seen)
    if miss:
        out.append(f"FIELD-KEY {name}: {len(miss)} Trade(s) with no row, e.g. {miss[0]}")
    return out


def _trades(name: str) -> dict:
    return {(str(t.symbol), int(t.entry_ms)): t for t in live()[name]}


def fields_break():
    W = written()
    tv6 = _trades("v6")
    orig_latch = B.plus_1r_bar

    def late(f, t):
        j = orig_latch(f, t)
        return j + 1 if (j is not None and j + 1 <= int(t.exit_i)) else j

    def mut(attr, value):
        def run():                          # judged INSIDE the mutation: the truth table
            with mutated(B, attr, value):   # asks the module's own abs_tide_refused
                df = rebuild("v6")
                return fields_findings(df, tv6, "v6")
        return run

    def frame_plant(col, fn):
        def run():
            d = W["v6_campaigns"].copy()
            i = d.index[0] if col != "continuation" else d.index[d["continuation"]][0]
            d.loc[i, col] = fn(d.loc[i, col])
            return fields_findings(d, tv6, "v6")
        return run

    lag17 = (("0", 0, 0), ("1-6", 1, 6), ("7-15", 7, 16), (">=16", 17, None))
    return plants([
        ("the +1R latch returned one bar late (plus_1r_bar j+1)", "FIELD-LATCH",
         mut("plus_1r_bar", late)),
        ("the absolute cut typed 396 (ABS_TIDE_CUT)", "FIELD-ABS206 v6",
         mut("ABS_TIDE_CUT", 396)),
        ("the absolute cut read as >= 206 (abs_tide_refused)", "FIELD-ABS206 truth table",
         mut("abs_tide_refused", lambda run: int(run) >= 206)),
        ("the P-WIN-1 lag cut moved to 17 (LAG_BANDS)", "FIELD-LAG", mut("LAG_BANDS", lag17)),
        ("the structure-distance cut moved to 2.0 (R_OVER_ATR_CUT)", "FIELD-RATR",
         mut("R_OVER_ATR_CUT", 2.0)),
        ("every exit stamped at its close (EXIT_INTRABAR emptied)", "FIELD-EXIT-EVENT",
         mut("EXIT_INTRABAR", ())),
        ("one row's era flipped in a copy of the written table", "FIELD-ERA",
         frame_plant("era_of_entry", lambda v: "holdout" if v == "tuning" else "tuning")),
        ("the continuation flag flipped in a copy of the written table", "FIELD-TC10",
         frame_plant("continuation", lambda v: not bool(v))),
    ])


def fields_real():
    W = written()
    fv = fields_findings(W["v6_campaigns"], _trades("v6"), "v6")
    f9 = fields_findings(W["trg912_campaigns"], _trades("trg912"), "trg912")
    bad = fv + f9
    parts = []
    for name in ("v6", "trg912"):
        d = W[f"{name}_campaigns"]
        parts.append(f"{name} {len(d)} rows: latched {int(d['reached_1r'].sum())}, streak > "
                     f"206 {int(d['tide_abs_gt206'].sum())}, r_over_atr > 2.2 "
                     f"{int(d['r_over_atr_gt_2p2'].sum())}, lag >= 16 "
                     f"{int((d['lag_band'] == '>=16').sum())}, tuning/holdout "
                     f"{int((d['era_of_entry'] == 'tuning').sum())}/"
                     f"{int((d['era_of_entry'] == 'holdout').sum())}, straddle "
                     f"{int(d['entry_bar_straddles_era_cut'].sum())}, continuation "
                     f"{int(d['continuation'].sum())}, entered after the TC10 pin "
                     f"{int(d['entered_after_tc10_pin'].sum())}, exits intrabar_open/close "
                     f"{int((d['exit_event_stamp'] == 'intrabar_open').sum())}/"
                     f"{int((d['exit_event_stamp'] == 'close').sum())}")
    return (not bad), (f"every campaign of both written TC11 tables re-derived by this file "
                       f"from the Trade objects and the raw 4h arrays — +1R latch bar and "
                       f"its open, tide_abs_gt206 (typed > 206; truth table {ABS_TRUTH} "
                       f"held), lag + band, r_over_atr + flag (> 2.2), era by close + "
                       f"straddle, TC10-pin flags, L-R.5 exit stamp: {len(bad)} mismatch(es) "
                       f"({'; '.join(parts)})" + (f"; findings {bad[:4]}" if bad else ""))


# ═══════════════════════════════════════════════════════════ F-WINDOW-ASOF
def window_findings(df: pd.DataFrame, pin_ms: int, name: str,
                    full: pd.DataFrame | None = None) -> list[str]:
    """WINDOW-FUTURE a window_end_i after the as-of (> hi_i + 1) · WINDOW-OPEN
    the open flag / close stamp disagree with window_end_i == hi_i + 1, or a
    closed window closes after the pin · WINDOW-DERIVE window_end_i != this
    file's min(first counter 12/89 cross after arm_i, hi_i + 1) · WINDOW-PREFIX
    a window closed at this pin moves in the TC11 table, or one open here ends
    in the TC11 table at or before this pin's hi_i."""
    out = []
    fk = ({(str(a), int(b)): int(w) for a, b, w in
           zip(full["symbol"], full["entry_ms"], full["window_end_i"])}
          if full is not None else {})
    for r in df.itertuples(index=False):
        tp = tape(r.symbol)
        hi_i = hi_index(r.symbol, pin_ms)
        we = int(r.window_end_i)
        k = f"{name}@{iso(pin_ms)} {r.symbol} {iso(int(r.entry_ms))}"
        if we > hi_i + 1:
            out.append(f"WINDOW-FUTURE {k}: window_end_i {we} is {we - hi_i - 1} bar(s) after "
                       f"the as-of (hi_i + 1 = {hi_i + 1}; bar opens {iso(int(tp['o'][we]))})"
                       if we < len(tp["o"]) else
                       f"WINDOW-FUTURE {k}: window_end_i {we} > hi_i + 1 = {hi_i + 1}")
        is_open = we == hi_i + 1
        wc = None if _nul(r.window_end_close_ms) else int(r.window_end_close_ms)
        if bool(r.window_open_at_asof) != is_open or \
                (is_open and wc is not None) or \
                (not is_open and we <= hi_i and (wc != int(tp["o"][we]) + MS4H or wc > pin_ms)):
            out.append(f"WINDOW-OPEN {k}: open flag {r.window_open_at_asof}, close stamp {wc}, "
                       f"window_end_i {we} vs hi_i {hi_i}")
        ctr = tp["win_dn"] if int(r.direction) == 1 else tp["win_up"]
        nx = np.flatnonzero(ctr[int(r.arm_i) + 1:])
        first = int(r.arm_i) + 1 + int(nx[0]) if nx.size else None
        want = first if (first is not None and first <= hi_i) else hi_i + 1
        if we != want:
            out.append(f"WINDOW-DERIVE {k}: window_end_i {we} != derived {want} (first counter "
                       f"12/89 cross after arm_i {r.arm_i}: {first}; hi_i {hi_i})")
        key = (str(r.symbol), int(r.entry_ms))
        if key in fk:
            if not is_open and fk[key] != we:
                out.append(f"WINDOW-PREFIX {k}: closed here at {we}, TC11 table says {fk[key]}")
            if is_open and fk[key] <= hi_i:
                out.append(f"WINDOW-PREFIX {k}: open here, TC11 table ends it at {fk[key]} "
                           f"<= hi_i {hi_i}")
    return out


_EARLY: dict = {}


def early_rows(pin_iso: str) -> dict:
    if pin_iso not in _EARLY:
        _EARLY[pin_iso] = {n: rebuild(n, pin_iso) for n in ("v6", "trg912")}
    return _EARLY[pin_iso]


def raw_future(df: pd.DataFrame, pin_ms: int, roles, lo: int, hi: int) -> tuple[int, int]:
    """(rows whose RAW armings9 index is a counter cross AFTER the as-of, rows
    whose raw index is the tape-end sentinel len(tape) beyond it) — what the
    uncapped column would have written (the verifier's MAJOR, counted)."""
    fut = sent = 0
    for s in sorted(set(df["symbol"])):
        arms, hi_i, n = B.arm_index(s, roles, lo, hi)
        for r in df[df["symbol"] == s].itertuples(index=False):
            e = int(arms[(int(r.arm_i), int(r.direction))].window_end_i)
            if e > hi_i + 1:
                if e < n:
                    fut += 1
                else:
                    sent += 1
    return fut, sent


def window_break():
    W = written()

    def raw_cap():
        out = []
        with mutated(B, "known_window_end", lambda e, h: int(e)):
            for p in EARLY_PINS:
                for n in ("v6", "trg912"):
                    try:
                        rebuild(n, p)
                    except SystemExit as e:
                        out.append(f"{n}@{p[:10]} HALT: {e}")
        return out

    def raw_copy():
        out = []
        for p in EARLY_PINS:
            lo, hi, _ = B.corridor(p)
            for n in ("v6", "trg912"):
                roles = T9.V6_ROLES if n == "v6" else B.r912()
                d = early_rows(p)[n].copy()
                for i in d.index[d["window_open_at_asof"]]:
                    arms, _, _ = B.arm_index(d.at[i, "symbol"], roles, lo, hi)
                    d.at[i, "window_end_i"] = int(arms[(int(d.at[i, "arm_i"]),
                                                        int(d.at[i, "direction"]))].window_end_i)
                out += window_findings(d, TP._iso_ms(p), n)
        return out

    def short_cap():
        with mutated(B, "known_window_end", lambda e, h: int(e) if int(e) <= int(h) else int(h)):
            df = rebuild("v6")
        return window_findings(df, PIN, "v6")

    def plus_one():
        d = W["v6_campaigns"].copy()
        i = d.index[~d["window_open_at_asof"]][0]
        d.loc[i, "window_end_i"] = int(d.loc[i, "window_end_i"]) + 1
        d.loc[i, "window_end_close_ms"] = int(d.loc[i, "window_end_close_ms"]) + MS4H
        return window_findings(d, PIN, "v6")

    return plants([
        ("the as-of cap removed (known_window_end returns armings9's raw index), both books "
         "rebuilt at the four earlier pins", "look-ahead", raw_cap),
        ("copies of the earlier-pin tables carrying armings9's raw (future) index on their "
         "open windows", "WINDOW-FUTURE", raw_copy),
        ("the cap one bar short (hi_i, not hi_i + 1) — open windows posed as closed at the "
         "as-of bar", "WINDOW-DERIVE", short_cap),
        ("one closed window's window_end_i +1 in a copy of the written table",
         "WINDOW-DERIVE", plus_one),
    ])


def window_real():
    W = written()
    bad = []
    parts = []
    for name in ("v6", "trg912"):
        d = W[f"{name}_campaigns"]
        bad += window_findings(d, PIN, name)
        parts.append(f"{name}@{iso(PIN)} {len(d)} rows, open {int(d['window_open_at_asof'].sum())}")
    fut = sent = 0
    for p in EARLY_PINS:
        pm = TP._iso_ms(p)
        lo, hi, _ = B.corridor(p)
        rows = early_rows(p)
        for name in ("v6", "trg912"):
            d = rows[name]
            bad += window_findings(d, pm, name, W[f"{name}_campaigns"])
            roles = T9.V6_ROLES if name == "v6" else B.r912()
            f_, s_ = raw_future(d, pm, roles, lo, hi)
            fut, sent = fut + f_, sent + s_
            parts.append(f"{name}@{p[:10]} {len(d)} rows, open "
                         f"{int(d['window_open_at_asof'].sum())} (raw armings9 index: a counter "
                         f"cross after the as-of on {f_}, the tape-end sentinel on {s_})")
    return (not bad), (f"window_end_i as known at the as-of, re-derived by this file (EMA12/"
                       f"EMA89 counter cross, capped at hi_i + 1), open flag and close stamp, "
                       f"and prefix-stability vs the TC11 tables, at the pin and four earlier "
                       f"pins, both books: {len(bad)} finding(s) — {'; '.join(parts)}; at the "
                       f"earlier pins the uncapped index would have written {fut} future "
                       f"counter-cross bar(s) and {sent} tape-end sentinel(s) past the as-of; "
                       f"the written index writes none"
                       + (f"; findings {bad[:4]}" if bad else ""))


# ═══════════════════════════════════════════════════════════════════ F-KEY
def typed_specs() -> dict:
    """The F-KEY commission, TYPED HERE: {stem: (key, required, null_iff, columns)}."""
    creq = tuple(c for c in CAMPAIGN_COLUMNS_TYPED if c not in NULLABLE_TYPED)
    ccols = CAMPAIGN_COLUMNS_TYPED + AS_OF_TYPED
    return {"v6_journal": (KEYS_TYPED["v6_journal"], JOURNAL_REQUIRED_TYPED, None, None),
            "trg912_journal": (KEYS_TYPED["trg912_journal"], JOURNAL_REQUIRED_TYPED, None,
                               None),
            "v6_campaigns": (KEYS_TYPED["v6_campaigns"], creq, NULL_IFF_TYPED, ccols),
            "trg912_campaigns": (KEYS_TYPED["trg912_campaigns"], creq, NULL_IFF_TYPED, ccols)}


def _all_key_findings(frames: dict) -> list[str]:
    specs = typed_specs()
    out = []
    for s, df in frames.items():
        key, req, nif, cols = specs[s]
        out += B.key_findings(s, df, key, req, nif)
        if cols is not None and tuple(df.columns) != tuple(cols):
            extra = [c for c in df.columns if c not in cols]
            lack = [c for c in cols if c not in df.columns]
            out.append(f"KEY-COLS {s}: column list != typed (absent {lack}, extra {extra}"
                       f"{', order differs' if not lack and not extra else ''})")
    return out


def key_break():
    W = written()
    c = W["v6_campaigns"]

    def with_(name, df):
        d = dict(W)
        d[name] = df
        return _all_key_findings(d)

    def dup():
        return with_("v6_campaigns", pd.concat([c, c.iloc[[5]]], ignore_index=True))

    def null_net():
        d = c.copy()
        d.loc[d.index[7], "net_r"] = None
        return with_("v6_campaigns", d)

    def flag():
        d = c.copy()
        i = d.index[~d["harvested"]][0]
        d.loc[i, "harvest_i"] = int(d.loc[i, "entry_i"]) + 1
        return with_("v6_campaigns", d)

    def asof():
        return with_("trg912_journal", W["trg912_journal"].drop(columns=["as_of_last_closed_4h"]))

    def lineage_dup():
        with tempfile.TemporaryDirectory(prefix="f-key-") as td:
            for s, df in W.items():
                (df if s != "v6_journal" else pd.concat([df, df.iloc[[3]]], ignore_index=True)
                 ).to_parquet(Path(td) / f"{s}.parquet", index=False)
            shutil.copy(OUT / B.MANIFEST, Path(td) / B.MANIFEST)
            ok, lines = TP.check_keys(Path(td))
            return [] if ok else [x for x in lines if x.startswith("[BAD]")]

    def module_drops_lag():
        cols = tuple(x for x in B.CAMPAIGN_COLUMNS if x != "lag")
        with mutated(B, "CAMPAIGN_COLUMNS", cols):
            df = rebuild("v6")
        df = TP.stamp_n(df, live()["meta"], "4h", None)
        return with_("v6_campaigns", df)

    return plants([
        ("a duplicated campaign row in a copy of v6_campaigns", "KEY-DUP", dup),
        ("net_r nulled on one row", "KEY-NULL", null_net),
        ("harvest_i filled on an unharvested row", "KEY-FLAG", flag),
        ("as_of_last_closed_4h dropped from trg912_journal", "KEY-ASOF", asof),
        ("TP.check_keys on a temp root whose v6_journal holds a duplicated row",
         "dupes: ['v6_journal']", lineage_dup),
        ("the module drops `lag` from its CAMPAIGN_COLUMNS (v6 rows rebuilt, stamped)",
         "required column(s) absent ['lag']", module_drops_lag),
    ])


def key_real():
    W = written()
    f = _all_key_findings(W)
    ok_l, lines = TP.check_keys(OUT)
    man = json.loads((OUT / B.MANIFEST).read_text(encoding="utf-8"))
    g_keys = man["keys"] == KEYS_TYPED
    csha = {s: TB._content_sha(df) for s, df in W.items()}
    g_sha = csha == man["sha"]
    g_mod = tuple(B.CAMPAIGN_COLUMNS) == CAMPAIGN_COLUMNS_TYPED
    ok = not f and ok_l and g_keys and g_sha and g_mod
    counts = ", ".join(f"{s} {len(df)}" for s, df in W.items())
    nul = {s: sorted(c for c in df.columns if df[c].isna().any()) for s, df in W.items()
           if s.endswith("_campaigns")}
    return ok, (f"rows: {counts}; keys == typed {KEYS_TYPED}: {g_keys}; campaign column list == "
                f"the typed {len(CAMPAIGN_COLUMNS_TYPED)} + {len(AS_OF_TYPED)} as-of stamps "
                f"(the module's CAMPAIGN_COLUMNS agrees: {g_mod}); unique keys, no null in any "
                f"key/typed-required column, all {len(AS_OF_TYPED)} as-of stamps present and "
                f"non-null, every nullable column null exactly where its TYPED flag says "
                f"(nullable columns holding nulls: {nul}): {not f}; TP.check_keys(books/): "
                f"{' · '.join(lines)}; manifest content shas == TB._content_sha of the tables "
                f"read back: {g_sha}" + (f"; findings {f[:4]}" if f else ""))


# ═══════════════════════════════════════════════════════════════════ F-DET
def _files(d: Path) -> dict:
    return {p.name: p.read_bytes() for p in sorted(d.iterdir()) if p.is_file()}


def det_findings(a: tuple, b: tuple, canon: dict) -> list[str]:
    """(exit, {name: bytes}) x 2 vs the canonical files -> findings."""
    out = []
    for lab, (rc, _) in (("seed 1", a), (f"seed {SEED}", b)):
        if rc != 0:
            out.append(f"{lab} exit {rc}")
    for lab, x in (("seed 1", a[1]), (f"seed {SEED}", b[1]), ("canonical books/", canon)):
        if sorted(x) != sorted(FILES_TYPED):
            out.append(f"{lab}: file set {sorted(x)} != typed {sorted(FILES_TYPED)}")
    for lab, x, y in ((f"seed 1 vs seed {SEED}", a[1], b[1]),
                      ("seed 1 vs canonical", a[1], canon)):
        for name in sorted(set(x) & set(y)):
            if x[name] != y[name]:
                k = next((i for i in range(min(len(x[name]), len(y[name])))
                          if x[name][i] != y[name][i]), min(len(x[name]), len(y[name])))
                out.append(f"{lab}: {name} bytes differ at byte {k}")
            if name.endswith(".parquet"):
                ca = TB._content_sha(pd.read_parquet(io.BytesIO(x[name])))
                cb = TB._content_sha(pd.read_parquet(io.BytesIO(y[name])))
                if ca != cb:
                    out.append(f"{lab}: {name} content sha {ca[:12]}… != {cb[:12]}…")
    return out


def det_dir() -> Path:
    """F-DET's twins live under RUN_ROOT (--root redirects them) [H §8]."""
    return RUN_ROOT / DET_ROOT.name


def det_build(d: Path, seed: int, hashorder: bool = False) -> tuple[int, dict]:
    if d.exists():
        shutil.rmtree(d)
    env = dict(_env(), PYTHONHASHSEED=str(seed))
    if not hashorder:
        cmd = [PY, "-B", str(ROOT / "scripts" / "tierc11_books.py"), f"--out-dir={d}"]
    else:                                   # SABOTAGE twin: a set-order line appended
        code = (f"import sys\nsys.dont_write_bytecode = True\n"
                f"sys.path.insert(0, {str(ROOT)!r})\n"
                f"sys.path.insert(0, {str(ROOT / 'scripts')!r})\n"
                f"from pathlib import Path\nimport tierc11_books as B\n"
                f"d = Path({str(d)!r})\nB.build(d)\n"
                f"p = d / B.REPORT\n"
                f"p.write_text(p.read_text() + 'set order: ' + ','.join(set(B.E.PANEL17)) "
                f"+ '\\n')\n")
        cmd = [PY, "-B", "-c", code]
    r = subprocess.run(cmd, env=env, capture_output=True, text=True, cwd=str(ROOT),
                       timeout=1800)
    return r.returncode, (_files(d) if d.exists() else {})


def _canon() -> dict:
    return {k: v for k, v in (_files(OUT) if OUT.exists() else {}).items() if k in FILES_TYPED}


def det_break():
    canon = _canon()
    bent = dict(canon)
    md = bytearray(bent["BOOKS.md"])
    md[len(md) // 2] ^= 0x01
    bent["BOOKS.md"] = bytes(md)

    def float_moved():
        d = pd.read_parquet(io.BytesIO(canon["v6_campaigns.parquet"]))
        d.loc[d.index[0], "net_r"] = float(d["net_r"].iloc[0]) + 1e-6
        buf = io.BytesIO()
        d.to_parquet(buf, index=False)
        c2 = dict(canon)
        c2["v6_campaigns.parquet"] = buf.getvalue()
        return det_findings((0, c2), (0, c2), canon)

    def hashorder():
        o = {s: det_build(det_dir() / f"hashorder_{s}", s, hashorder=True) for s in DET_SEEDS}
        a, b = o[DET_SEEDS[0]], o[DET_SEEDS[1]]
        return [x for x in det_findings(a, b, a[1]) if x.startswith(f"seed 1 vs seed {SEED}")]

    return plants([
        ("one byte bent in a copy of BOOKS.md", "BOOKS.md bytes differ",
         lambda: det_findings((0, canon), (0, bent), canon)),
        ("one net_r moved 1e-6 in a parquet copy", "v6_campaigns.parquet content sha",
         float_moved),
        ("a hash-order-dependent line (set iteration) under the two seeds",
         f"seed 1 vs seed {SEED}: BOOKS.md bytes differ", hashorder),
    ])


def det_real():
    canon = _canon()
    o = {s: det_build(det_dir() / f"seed_{s}", s) for s in DET_SEEDS}
    a, b = o[DET_SEEDS[0]], o[DET_SEEDS[1]]
    bad = det_findings(a, b, canon)
    man = json.loads(canon["build_manifest.json"]) if "build_manifest.json" in canon else {}
    shas = ", ".join(f"{k} {sha_bytes(v)[:12]}…" for k, v in sorted(a[1].items()))
    return (not bad), (f"exit {a[0]}/{b[0]}; file set == typed {len(FILES_TYPED)} files in both "
                       f"builds and in books/; every file byte-identical seed 1 == seed {SEED} "
                       f"== canonical, every parquet content sha equal: {not bad} ({shas}); "
                       f"book shas v6 {man.get('book_sha', {}).get('v6', '?')[:16]}… trg912 "
                       f"{man.get('book_sha', {}).get('trg912', '?')[:16]}…"
                       + (f"; findings {bad[:4]}" if bad else ""))


FIXTURES = (
    ("F-CTRL-a", "v6 on CLASSIC5 over the TC11 corridor, the N-asset path vs tierc6 — "
     "EXACT ZERO [L-1.7a]",
     "run_cell_n(v6 control) vs tierc6.run_cell(CARD_V6) differs by ANY amount on any of "
     "TP's 12 CTRL_COLS, any exit_reason or the count differs, the corridor end is not "
     "1790294400000 (or AS_OF_PIN.json names another pin), or corridor_n(CLASSIC5) != "
     "TP.control_window()",
     ctrl_a_break, ctrl_a_real),
    ("F-CTRL-b", "cross-process: the live v6 journal vs the FILED TC10 control journal "
     "[L-1.7b]",
     "the filed journal is not sha256 fcbf5db0…fae64c1c / 200 rows with the one typed "
     "corridor_end row, or the module pins another referee; a filed campaign is absent live; "
     "a campaign it closed differs on the 12 CTRL_COLS at 6 dp or on exit_reason; the "
     "continuation's entry/stop/r_dist differ, its live exit bar opens before the TC10 pin, "
     "or its live n_advances / mfe_r fall below the filed; or a live-only campaign entered "
     "at or before the TC10 pin",
     ctrl_b_break, ctrl_b_real),
    ("F-912-ANCHOR", "the 9/12 book over the TC10 window hashes to P-TRG-2's filed "
     "full-arm book [L-1.6]",
     "T9.SWEEP_CELLS[-1] is not the typed 9/12 roles, or TP._book_sha of the TC10-window "
     "9/12 book != P-TRG-2.scored.json full-arm book_sha256 (typed b2276fa4…, n 198), or "
     "the v6 base over the same window != that arm's filed base_sha256, or the module pins "
     "another referee",
     a912_break, a912_real),
    ("F-AGE-ANCHOR", "the trailing tide-age bands reproduce TC10's P_AGE_1_TIDE_YOUTH "
     "table exactly, and every campaign's edges are the INCLUSIVE prefix [L-G.1; part of "
     "F-DEF]",
     "the TC10-window v6 book banded by tide_streak at the ENTRY bar on trailing CLASSIC5 "
     "edges does not reproduce P_AGE_1_TIDE_YOUTH.parquet on every compared column of "
     "bands 01..04 + ALL (typed n 25/60/56/59/200); a TC10-window campaign carries "
     "another band in the written TC11 v6_campaigns.parquet; or on any campaign of either "
     "written TC11 table (or the TC10-window rows) the entry-bar tide state / streak / "
     "left-censoring, the q25/q50/q75 (vs np.quantile over pooled CLASSIC5 bars with open "
     "<= the entry bar, >= 30) or the band differ from this file's derivation",
     age_break, age_real),
    ("F-FIELDS", "every campaign field the later stages read, re-derived from the Trade "
     "objects and the raw 4h arrays [L-G.1 shadow, L-G.2, L-G.3, L-1.3, L-R.5, L-1.7]",
     "on any campaign of either written TC11 table: the +1R latch bar is not the first bar "
     "in (entry_i, exit_i] reaching entry ± R; tide_abs_gt206 != (streak > 206) or "
     "abs_tide_refused fails {205: no, 206: no, 207: yes}; lag / lag band differ from "
     "entry_i − arm_i and 0 / 1-6 / 7-15 / >=16; r_over_atr or its > 2.2 flag differ; era "
     "is not by the entry bar's close; the TC10-pin flags differ; or the exit stamp is not "
     "the bar OPEN for a stop and the close otherwise",
     fields_break, fields_real),
    ("F-WINDOW-ASOF", "window_end_i is the window end AS KNOWN at the as-of — never a later "
     "bar — at the pin and four earlier pins [verifier MAJOR; L-0.1]",
     "for either book, at the TC11 pin or at 2026-09-21T16:00Z / 2026-09-01 / 2026-06-01 / "
     "2025-12-01: a window_end_i > hi_i + 1; an open window whose window_end_i != hi_i + 1 "
     "or whose flag / close stamp disagree; a closed window closing after the pin; a "
     "window_end_i != min(first counter 12/89 cross after arm_i, hi_i + 1); or a window "
     "closed at an earlier pin that moves in the TC11 table",
     window_break, window_real),
    ("F-KEY", "every written table: the typed column list, unique keys, no null in a "
     "typed-required column, the as-of warranty, nulls only where their typed flag says",
     "a column list that is not the typed one, a duplicated key, a null key/required cell, "
     "an absent/null as-of stamp, a nullable column null where its typed flag says it "
     "cannot be (or filled where it must be null), TP.check_keys(books/) RED, or a manifest "
     "content sha that is not the table's",
     key_break, key_real),
    ("F-DET", "two subprocess builds under different hash seeds, one set of bytes",
     "the PYTHONHASHSEED 1 and 20260924 builds (under RUN_ROOT/_det_books) differ from each "
     "other or from the canonical books/ files in the file set, any byte or any parquet "
     "content sha, or either exits nonzero",
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
    say("TIER-C11 TC11-BOOKS FIXTURES — scripts/tierc11_books.py (the two frozen books "
        "and the campaign table) — break leg first, RED or void")
    say("=" * 78)
    say(f"seed {SEED} · substrate {TC11_SNAP.name} · pin {PIN} · TC10 pin {TC10_PIN}")
    for ln in B.READINGS:
        say(ln)
    for fid, title, fails_if, b, r in FIXTURES:
        if not pick or any(q in fid.lower() for q in pick):
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
    clock(f"wall {time.time() - t0:.1f}s · transcript sha {sha_bytes(body)}")
    if FAILED:
        print("*** HALT: fixture mismatch. Nothing downstream is trustworthy. ***")
    return 1 if (FAILED or bad) else 0


if __name__ == "__main__":
    raise SystemExit(main())
