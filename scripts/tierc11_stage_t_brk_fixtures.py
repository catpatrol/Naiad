#!/usr/bin/env python
"""TIER-C11 · STAGE T-brk — F-BRK-HOLD · F-BRK-RIDE · F-BRK-TIDE · F-BRK-ENTRY ·
F-BRK-EXIT · F-BLIND · F-GRID · F-KEY · F-DET.  The fixtures of scripts/tierc11_stage_t_brk.py
(P-BRK-4H, the 4h breakout-retest lane, and its Tier-E arms) [LEANS L-T.1,
L-R.6(a), L-R.2, L-1.3, L-1.4, L-F.1, L-F.2, AM-2, AM-7].

TWO LEGS PER FIXTURE, the BREAK leg first, and it must go RED or the fixture is
VOID — a guard nobody has seen fail is a guard nobody has seen.  A break leg is a
set of PLANTS judged one at a time; a plant counts as CAUGHT only if a finding
NAMES THE INTENDED DETECTOR (its expected substring); a plant that crashes is a
FIXTURE DEFECT, never a catch.  Every plant is made on a COPY (a frame, a book, a
source text, a temp dir) or under a MUTATION of the module that is restored in
`finally`; no artifact of record moves.  The referees are typed HERE (a second
object): the pins (EMA 89, 1.0 ATR, 3 bars, ttl 400, memory 6 bars), the tide law
(EMA89/EMA316 of 4h close, both clauses), the floor (bar 316), the era cut, the
panels, the arms, the grids' declared cells, the regbook interface (columns,
dtypes, sidecar keys, the canonical-CSV sha law), the charter slippage tiers.
Raw 4h bars are read by this file from the snapshot's kline parquet (pandas on a
path string), and EMA / ATR are this file's own plain loops.

  F-BRK-HOLD   FAILS IF, on any CLASSIC5 asset at the calibrated pick or at frozen
               3.0, the module's tap-89 scan rows (every evaluated touch: die,
               sequence, touch bar, known bar, outcome) differ from a plain-loop
               hand walk on RAW bars with this file's own EMA89 / ATR14 (window
               min(die + 400, next die - 1, n - 1); a touch = the bar meets the
               band with the prior close beyond it on the die side; failed = a
               close through by 1.0 x ATR over touch..touch + 3; truncated past
               the tape; the first hold ends the scan); the module's candidates
               are not exactly the hand holds (entry = touch + 3, direction = the
               death's, extreme = min low / max high over touch..entry); or fewer
               than 3 holds, 1 failed retest and 1 hold after a failed touch are
               hand-verified per scale.  SABOTAGE: every retest relabelled a
               hold; the one-shot law run under the scan's name; the entry moved
               to the touch bar.
  F-BRK-RIDE   FAILS IF any of the 200 CLASSIC5 v6 campaigns, re-entered through
               the BRK path (the module's window + ride: BK.brk_campaigns ->
               ride_leg_l(ribbon=None) + account_l) with v6's own entry and stop,
               differs from v6's _ride_leg9 book by ANY amount on the 12
               CTRL_COLS, on exit_reason or on entry_i / exit_i / harvested /
               harvest_i / bars_held, or the count differs.  SABOTAGE: the 12/25
               ribbon bell switched on (RIBBON = (12, 25)); the taker fee doubled;
               one leg's stop one tick off; one net_r +1e-12 in a copy.
  F-BRK-TIDE   FAILS IF, on any candidate of any ridden arm that reaches the
               permission test, the module admits (refuses) it where this file's
               tide at the ENTRY bar's own close (EMA89 > EMA316 AND close >
               EMA316 for a long; mirror) says the opposite; or on the PLANTED
               candidates (per CLASSIC5 asset: tide flipping in / out at the entry
               bar, both sides; and bars where EMA89 > EMA316 but close <= EMA316)
               the same.  SABOTAGE: the previous 4h bar's tide
               (BK.tide_4h_for_exec on the 4h frame); the permission ignored; the
               close clause dropped.
  F-BRK-ENTRY  FAILS IF, in any WRITTEN ridden-arm regbook, a campaign's entry is
               not the known_at close of a 'hold' row of the arm's own scan (N's
               event frames), its direction is not that row's and its death's,
               its entry_px is not the raw close there, two campaigns of one asset
               overlap (next entry bar <= the previous exit bar), or the book is
               not exactly the greedy one-position walk over the in-window holds
               whose entry-bar tide is aligned.  SABOTAGE (copies of the written
               book): a direction flipped; an entry moved to its touch bar; a
               position-open candidate inserted; a failed retest entered; a
               tide-refused hold entered; a campaign dropped; a rail-bound stop
               railed at 0.5 ATR.  Each plant takes a real qualifying row when
               the build has one and is BUILT BY CONSTRUCTION when it has none
               (never an index past the end: a plant that crashes proves nothing).
  F-BRK-EXIT   FAILS IF any campaign of any WRITTEN ridden-arm regbook carries an
               exit or an economics figure that differs by ANY amount from
               (a) the engine's re-ride of that campaign's written entry and stop
               (BK.brk_campaigns, TP.CONTROL_CARD, T9.V6_ROLES, ribbon None) on
               exit_close_ms, exit_reason, gross_r, fee_r, funding_r, net_r, or
               (b) THIS FILE'S OWN hand ride and accounting from raw 4h bars and
               raw funding — per bar STOP (adverse extreme, fills at the stop) ->
               BELL counter 12/89 then counter 89/316 (fills at the close) ->
               HARVEST 50% at the close of the bar whose extreme meets the 89/316
               near edge, armed by a prior close outside it -> strict (2,2) pivot
               TRAIL (pivot -/+ 0.5 ATR, railed 1.0 ATR from the confirming close,
               advance-only, >= 0.05 ATR, armed once +1R is seen); taker 5 bps a
               side on every fill; funding = every hourly print with entry open <
               hour <= the fill bar's open, priced at the last closed bar, D12
               cap 1.0 R once; net = gross - fee - funding — on the exit bar,
               exit_close_ms, exit_reason, exit_px, harvested, trail advances,
               gross, fee, funding, net; or fewer than 3 stop exits without a
               trail advance, 3 bell exits after a harvest and 3 stop exits after
               a trail advance are hand-walked in the scored book.  SABOTAGE:
               (copies) net_r = gross - fee + funding; exit_close_ms one bar late;
               fee_r halved; an exit_reason relabelled; (module mutations, a
               fresh T.run_arm) the 12/25 bell on; the harvest switched off.
  F-BLIND      FAILS IF a DECISION function of the runner (typed list) names the
               range layer (N / tierc11_nest / C / ST / NL), reads .top / .bottom /
               .n_deviations, or imports anything, or E.hook_escapes finds I/O the
               audit hook cannot see in the runner.  SABOTAGE (source copies): a
               range_facts call inside candidates; a .top read inside dispose; an
               import inside ride; `import subprocess`.
  F-GRID       FAILS IF a written Tier-E grid is not WHOLE against this file's
               typed declared cells (TP.grid_whole), a row lacks the typed collar
               or the typed row_kind (the scored arm's rows 'registered book
               (reference)', every other arm's 'Tier-E arm'), a verdict word or a
               'verdict' column appears, a cell's n / sum_net_r differ from this
               file's own re-derivation from the regbooks (the holdout-on-a-
               pre-cut-death disclosure cells included; or a tally does not add
               up), or the report omits a declared cell row, a registered-book
               row (§11), a candidate (Appendix A), an evaluated retest (Appendix
               B) or a Tier-E regbook row (Appendix C).  SABOTAGE: a cell dropped;
               a cell duplicated; the collar removed; a 'verdict' column; a cell's
               n bent; a report row dropped; the scored arm's row labelled a
               Tier-E arm; an Appendix A row dropped; an Appendix C row dropped.
  F-KEY        FAILS IF a regbook lacks a typed required column or dtype, carries a
               null in one, a duplicated (symbol, entry_ms), a sidecar whose keys /
               kind / ruler / panel / era_scope / n / sum_net_r / book_sha256 (this
               file's own canonical CSV) disagree, a tier-E arm without its
               collar, an era not by the entry close, a slice that is not the
               scored book's era cut, a haircut_net_r off AM-7 (slip from the fee
               schedule's charter tier, typed A 2 / B 5 / C 10), an as-of stamp
               off the pin; STATUS.json is not the typed record; a stage table key
               is duplicated; a manifest content sha is not the table's; a row's
               net_r is not EXACTLY gross_r - fee_r - funding_r; or the module's
               WRITER (T.ride + T.trade_rows on a typed synthetic leg) stamps the
               entry bar that STRADDLES the cut (open 2024-06-30T20:00Z, close
               2024-07-01T00:00Z) anything but 'holdout', or the bar before it
               anything but 'tuning'.  SABOTAGE (copies): a duplicated row; a
               nulled net_r; direction as float; a bent sidecar sha; sidecar n + 1;
               BTC's haircut at 5 bps; a dropped 'lane'; an era flipped; STATUS
               'CLOSED'; a bent manifest sha; net_r = gross - fee + funding; fee_r
               halved; (mutation) E.era_of read at the bar OPEN.
  F-DET        FAILS IF two subprocess builds (PYTHONHASHSEED 1, 20260924) differ
               from each other or from the canonical files of record in the file
               set, any byte or any parquet content sha, or either exits nonzero.
               SABOTAGE: one byte bent in a copy; one float moved in a parquet
               copy; a hash-order-dependent line under the two seeds.
BANNED: self-comparison; one example where cardinality was possible; a tuned
magnitude bound standing in for an identity; a check whose claim is not the
design's claim.  FROZEN SUBSTRATE: HALTs unless NAIAD_CACHE_DIR is the TC11
snapshot (tierc11_env's guard).  Seed 20260924.  The transcript carries no clock
and no temp path.

Run:  export NAIAD_CACHE_DIR=$HOME/.cache/naiad/snapshots/tc11_20260925 PYTHONDONTWRITEBYTECODE=1
      ~/venvs/naiad/bin/python -B scripts/tierc11_stage_t_brk.py          # the canonical build first
      ~/venvs/naiad/bin/python -B scripts/tierc11_stage_t_brk_fixtures.py \\
          [leg-substring ...] [--refile-transcript] [--root=DIR]
Exit 0 = every leg GREEN, every break RED · 1 = a RED or VOID fixture, a
transcript finding, or a HALT.
"""
from __future__ import annotations

import ast
import contextlib
import copy
import dataclasses
import hashlib
import io
import json
import math
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
import tierc11_stage_t_brk as T                                     # noqa: E402  (guards first)

import numpy as np                                                   # noqa: E402
import pandas as pd                                                  # noqa: E402

N, E = T.N, T.E
TP, T9, BK, TB = E.TP, E.T9, E.BK, E.TB

# ── FIXTURE-TYPED LITERALS: the commission, a second object, never T's own ──
TC11_SNAP = Path.home() / ".cache" / "naiad" / "snapshots" / "tc11_20260925"
PIN = 1790294400000                      # 2026-09-25T00:00:00Z [L-0.1]
PIN_ISO_T = "2026-09-25T00:00:00Z"
MS4H = 14_400_000
SEED = 20260924
DET_SEEDS = (1, SEED)
AS_OF_LINE = "as_of_last_closed_4h: 2026-09-25T00:00:00Z"
CLASSIC5_T = ("BTCUSDT", "ETHUSDT", "SOLUSDT", "NEARUSDT", "ZECUSDT")
UNSEEN12_T = ("ENAUSDT", "PUMPUSDT", "HYPEUSDT", "MNTUSDT_BYBIT", "SUIUSDT", "LTCUSDT",
              "XMRUSDT", "BNBUSDT", "UNIUSDT", "1000PEPEUSDT", "DOGEUSDT", "1000BONKUSDT")
PANEL17_T = CLASSIC5_T + UNSEEN12_T
PANEL_T = {"CLASSIC5": CLASSIC5_T, "PANEL17": PANEL17_T}
BAND_P, MARGIN_T, HOLD_T, TTL_T = 89, 1.0, 3, 400          # L-T.1 / L-R.6(a)
MEM_HOLD_T = 6                                              # the memory line, touch + 6
ATR_N = 14
TIDE_F, TIDE_S = 89, 316                                    # the tide, both clauses
FLOOR_T = 316                                               # the warm-up floor [L-0.1]
STOP_BUF_T, RAIL_T = 0.5, 1.0
ERA_CUT_T = 1_719_791_999_000                               # tuning closes <= this [L-1.3]
SIDE_DIR_T = {"top": 1, "bottom": -1}
SLIP_TIER_BPS_T = {"A": 2.0, "B": 5.0, "C": 10.0}           # AM-7 / L-1.1 charter tiers
TAKER_T = 5.0
CTRL_COLS_T = ("entry_ms", "exit_ms", "entry_px", "exit_px", "stop_px", "r_dist", "net_r",
               "gross_r", "fee_r", "funding_r", "mfe_r", "n_advances")
CMP_EXACT_T = ("entry_i", "exit_i", "exit_reason", "harvested", "harvest_i", "bars_held")
V6_N_T = 200
ARMS_T = ("scored", "tierE__panel17", "tierE__memline_first_hold",
          "tierE__memline_oneshot_flip", "tierE__frozen3", "tierE__oneshot_first_touch",
          "tierE__tuning", "tierE__holdout")
RIDDEN_T = ARMS_T[:6]
ARM_PANEL_T = {a: ("PANEL17" if a == "tierE__panel17" else "CLASSIC5") for a in ARMS_T}
ARM_ERA_T = {a: ("tuning" if a == "tierE__tuning" else "holdout" if a == "tierE__holdout"
                 else "full") for a in ARMS_T}
# arm -> (scale, N event frame, band filter, hold length)
ARM_EVENT_T = {"scored": ("calibrated", "scan", "tap89", 3),
               "tierE__panel17": ("calibrated", "scan", "tap89", 3),
               "tierE__memline_first_hold": ("calibrated", "scan_mem", "memory-line", 6),
               "tierE__memline_oneshot_flip": ("calibrated", "oneshot_mem", "memory-line", 6),
               "tierE__frozen3": ("frozen3.0", "scan", "tap89", 3),
               "tierE__oneshot_first_touch": ("calibrated", "oneshot", "tap89", 3)}
REQUIRED_T = {"symbol": "object", "entry_ms": "int64", "entry_close_ms": "int64",
              "direction": "int8", "entry_px": "float64", "stop_px": "float64",
              "r_dist": "float64", "exit_close_ms": "int64", "exit_reason": "object",
              "net_r": "float64", "gross_r": "float64", "fee_r": "float64",
              "funding_r": "float64", "haircut_net_r": "float64", "era": "object",
              "lane": "object"}
REQ_ORDER_T = tuple(REQUIRED_T)
SIDECAR_KEYS_T = ("registration", "arm", "kind", "ruler", "panel", "era_scope", "n",
                  "sum_net_r", "book_sha256", "description", "source_script")
COLLAR_T = {"tier": "TIER-E", "selection_not_a_result": "a SELECTION, not a result",
            "gates": "nothing"}
EXIT_REASONS_T = ("stop", "bell_12_89", "bell_89_316", "corridor_end")
STAGE_FILES_T = ("T_BRK_ARMS.parquet", "T_BRK_ASSET_GRID.parquet", "T_BRK_ERA_GRID.parquet",
                 "T_BRK_EXIT_GRID.parquet", "T_BRK_DIR_GRID.parquet", "T_BRK_TALLY.parquet",
                 "T_BRK_CANDIDATES.parquet", "T_BRK_SCAN.parquet", "T_BRK_HAZARD.parquet",
                 "T_BRK_PICKS.parquet", "T_BRK_INSAMPLE.parquet", "STAGE_T_BRK.md",
                 "build_manifest.json")
REGBOOK_FILES_T = tuple(f"{a}.{x}" for a in ARMS_T for x in ("parquet", "json")) + ("STATUS.json",)
TABLE_KEYS_T = {"T_BRK_ARMS": ["cell"], "T_BRK_ASSET_GRID": ["cell"], "T_BRK_ERA_GRID": ["cell"],
                "T_BRK_EXIT_GRID": ["cell"], "T_BRK_DIR_GRID": ["cell"], "T_BRK_TALLY": ["cell"],
                "T_BRK_CANDIDATES": ["arm", "symbol", "die_i", "touch_i"],
                "T_BRK_SCAN": ["arm", "symbol", "die_i", "seq"], "T_BRK_HAZARD": ["cell"],
                "T_BRK_PICKS": ["cell"], "T_BRK_INSAMPLE": ["cell"]}
DECLARED_T = {
    "T_BRK_ARMS": list(ARMS_T),
    "T_BRK_ASSET_GRID": [f"{a}|{s}" for a in RIDDEN_T for s in PANEL_T[ARM_PANEL_T[a]]],
    "T_BRK_ERA_GRID": [f"{a}|{e}" for a in RIDDEN_T for e in ("tuning", "holdout")],
    "T_BRK_EXIT_GRID": [f"{a}|{x}" for a in RIDDEN_T for x in EXIT_REASONS_T],
    "T_BRK_DIR_GRID": [f"{a}|{d}" for a in RIDDEN_T for d in ("long", "short")],
    "T_BRK_TALLY": [f"{a}|{s}" for a in RIDDEN_T for s in PANEL_T[ARM_PANEL_T[a]]],
    "T_BRK_INSAMPLE": [f"scored|in_sample={f}|{e}" for f in (True, False)
                       for e in ("tuning", "holdout")] + ["tierE__holdout|beside",
                                                          "tierE__frozen3|beside"]
                      + [f"{a}|holdout|death_close<=cut" for a in RIDDEN_T],
    "T_BRK_HAZARD": [f"{p}|{e}" for p in ("POOLED:CLASSIC5", "POOLED:UNSEEN12")
                     for e in ("ALL", "tuning", "holdout")],
    "T_BRK_PICKS": list(PANEL17_T),
}
DECISION_FUNCS_T = ("scan_rows", "candidates", "tide_series", "permit_of", "dispose", "ride",
                    "haircut")
RANGE_NAMES_T = {"N", "tierc11_nest", "C", "ST", "NL"}
LEAK_ATTRS_T = {"top", "bottom", "n_deviations"}
VERDICT_RX = re.compile(r"\b(SUPPORTED|PASS|FAIL)\b")
BOOK_KEY_T = ["symbol", "entry_ms"]
MIN_HOLDS_T, MIN_FAILED_T, MIN_RESCUED_T = 3, 1, 1
# L-T.1 selection_hazard, typed from the frozen text: "CLASSIC5 NET H20 +0.681 ALL n 236 /
# +0.706 holdout n 88; UNSEEN12 +0.064 / +0.272" (3 dp)
HAZARD_T = {"POOLED:CLASSIC5|ALL": (236, 0.681), "POOLED:CLASSIC5|holdout": (88, 0.706),
            "POOLED:UNSEEN12|ALL": (None, 0.064), "POOLED:UNSEEN12|holdout": (None, 0.272)}
REGS_PATH_T = E.OUT / "registrations" / "REGISTRATIONS.json"
# row_kind, typed: which rows are the registered book's reference rows
ROW_KIND_REG_T = "registered book (reference)"
ROW_KIND_E_T = "Tier-E arm"
ROW_KIND_TABLE_T = {"T_BRK_HAZARD": "TC10 census cell (the selection hazard's source)",
                    "T_BRK_PICKS": "scale pick of record (SCALE_PICKS.json)"}
# the bar that STRADDLES the era cut, and the bar before it: (open, close, era by CLOSE)
STRADDLE_T = ((1_719_777_600_000, 1_719_792_000_000, "holdout"),    # 2024-06-30T20:00Z
              (1_719_763_200_000, 1_719_777_600_000, "tuning"))     # 2024-06-30T16:00Z
# the v6 management, typed HERE (the referee of F-BRK-EXIT's hand ride) [L-T.1]
MS1H = 3_600_000
WIN_F_T, WIN_S_T = 12, 89                    # the window bell: counter 12/89 cross
HARV_Q_T, HARV_MIN_T = 0.5, -math.inf        # 50% at the 89/316 near edge; no unit floor
TRAIL_BUF_T, TRAIL_RAIL_T = 0.5, 1.0         # pivot -/+ 0.5 ATR, railed 1.0 ATR from close
TRAIL_MIN_ADV_T, TRAIL_ARM_R_T = 0.05, 1.0   # advance >= 0.05 ATR; armed once +1R is seen
FEE_BPS_T = 5.0                              # taker, a side, every fill [L-1.1]
FUND_CAP_T = 1.0                             # D12: a funding COST capped at 1R, once
EXIT_KINDS_T = ("stop, no trail advance", "bell after a harvest", "stop after a trail advance")
MIN_EXIT_KIND_T = 3

OUT = E.OUT / T.STAGE_DIR                # research_outputs/tierc11/stage_t_brk
REG_OUT = E.OUT.joinpath(*T.REGBOOK_DIR)  # research_outputs/tierc11/regbooks/P-BRK-4H
RUN_ROOT = OUT
TRANSCRIPT = "FIXTURES_T_BRK.txt"
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


def under(obj, name: str, value, thunk):
    def run():
        with mutated(obj, name, value):
            return thunk()
    return run


def _env() -> dict:
    return dict(os.environ, NAIAD_CACHE_DIR=str(TC11_SNAP), PYTHONDONTWRITEBYTECODE="1")


def iso(ms: int) -> str:
    return pd.Timestamp(int(ms), unit="ms", tz="UTC").strftime("%Y-%m-%dT%H:%MZ")


def fsum(x) -> float:
    return float(math.fsum(float(v) for v in x))


# ══════════════════════════════════════════════ RAW BARS + THIS FILE'S OWN EMA / ATR
_RAW: dict = {}


def hand_ema(c, p: int) -> np.ndarray:
    a = 2.0 / (p + 1.0)
    out, prev = np.empty(len(c)), None
    for k in range(len(c)):
        v = float(c[k])
        prev = v if prev is None else prev + a * (v - prev)
        out[k] = prev
    return out


def hand_atr(h, l, c, n: int) -> np.ndarray:
    out, prev = np.empty(len(c)), None
    a = 1.0 / n
    for k in range(len(c)):
        hk, lk = float(h[k]), float(l[k])
        if k == 0:
            tr = hk - lk
        else:
            pc = float(c[k - 1])
            tr = max(hk - lk, max(abs(hk - pc), abs(lk - pc)))
        prev = tr if prev is None else prev + a * (tr - prev)
        out[k] = prev
    return out


def raw(sym: str) -> dict:
    """The snapshot's 4h kline parquet (pandas on a path string), closed <= the
    pin, with this file's own EMA89 band (NaN before bar 89), ATR14, tide."""
    if sym in _RAW:
        return _RAW[sym]
    k = pd.read_parquet(str(TC11_SNAP / "klines" / f"{sym}_4h.parquet"))
    k = k.sort_values("open_time").reset_index(drop=True)
    k = k[k["open_time"].to_numpy(np.int64) + MS4H <= PIN].reset_index(drop=True)
    om = k["open_time"].to_numpy(np.int64)
    o, h, l, c = (k[x].to_numpy(float) for x in ("open", "high", "low", "close"))
    atr = hand_atr(h, l, c, ATR_N)
    e89, e316 = hand_ema(c, TIDE_F), hand_ema(c, TIDE_S)
    band = hand_ema(c, BAND_P)
    band[:BAND_P] = np.nan
    tide = np.where((e89 > e316) & (c > e316), 1, np.where((e89 < e316) & (c < e316), -1, 0))
    _RAW[sym] = {"om": om, "o": o, "h": h, "l": l, "c": c, "atr": atr, "e89": e89,
                 "e316": e316, "band": band, "tide": tide.astype(np.int64), "n": len(c)}
    return _RAW[sym]


def same_bars(sym: str) -> list[str]:
    """Indices may be shared only if the raw bars ARE the range tape's and BK's."""
    rb, tp, lf = raw(sym), N.load11(sym, "4h"), BK.frame_l(sym, "4h")
    out = []
    for nm, om, h, l, c in (("N.load11", tp.t0, tp.h, tp.l, tp.c),
                            ("BK.frame_l", lf.open_ms, lf.h, lf.l, lf.c)):
        if not (np.array_equal(rb["om"], om) and np.array_equal(rb["h"], h)
                and np.array_equal(rb["l"], l) and np.array_equal(rb["c"], c)):
            out.append(f"BARS {sym}: raw 4h bars != {nm}")
    return out


# ═══════════════════════════════════════════════════════════════ F-BRK-HOLD
def hand_scan(rb: dict, dies: list, margin: float, hold: int, ttl: int) -> dict:
    """The first-retest-that-holds law, walked by hand: {(die_i, seq): (touch,
    known, outcome)}.  The window is the law as written (not the module's)."""
    h, l, c, atr, b, n = rb["h"], rb["l"], rb["c"], rb["atr"], rb["band"], rb["n"]
    out = {}
    for q, (d, side) in enumerate(dies):
        nxt = dies[q + 1][0] if q + 1 < len(dies) else n
        end = min(d + ttl, nxt - 1, n - 1)
        seq = 0
        for k in range(d + 1, end + 1):
            if not (l[k] <= b[k] and h[k] >= b[k]):
                continue
            beyond = (c[k - 1] > b[k - 1]) if side == "top" else (c[k - 1] < b[k - 1])
            if not beyond:
                continue
            if k + hold >= n:
                out[(d, seq)] = (k, k + hold, "truncated")
                break
            bad = False
            for j in range(k, k + hold + 1):
                if not np.isfinite(b[j]):
                    bad = True
                    break
                if side == "top" and c[j] < b[j] - margin * atr[j]:
                    bad = True
                    break
                if side == "bottom" and c[j] > b[j] + margin * atr[j]:
                    bad = True
                    break
            out[(d, seq)] = (k, k + hold, "failed" if bad else "hold")
            seq += 1
            if not bad:
                break
    return out


def hold_findings(sym: str, scale: str, tally: dict | None = None) -> list[str]:
    rb = raw(sym)
    bad = same_bars(sym)
    dz = N.deaths(sym, "4h", scale)                  # the death detector is NOT on trial here
    dies = [(int(r.die_i), str(r.side)) for r in dz.itertuples(index=False)]
    hand = hand_scan(rb, dies, MARGIN_T, HOLD_T, TTL_T)
    fx = T.facts(sym, scale)
    mr = T.scan_rows(fx, "scan_tap89")
    mod = {(int(r.die_i), int(r.seq)): (int(r.touch_i), int(r.known_at), str(r.retest_outcome))
           for r in mr.itertuples(index=False)}
    for k in sorted(set(hand) | set(mod)):
        if k not in hand or k not in mod:
            bad.append(f"HOLD-ROWS {sym} {scale} die {k[0]} seq {k[1]}: hand "
                       f"{hand.get(k)} vs module {mod.get(k)}")
        elif hand[k][:2] != mod[k][:2]:
            bad.append(f"HOLD-TOUCH {sym} {scale} die {k[0]} seq {k[1]}: hand {hand[k]} vs "
                       f"module {mod[k]}")
        elif hand[k][2] != mod[k][2]:
            bad.append(f"HOLD-VERDICT {sym} {scale} die {k[0]} seq {k[1]} touch "
                       f"{iso(rb['om'][hand[k][0]])}: hand {hand[k][2]} vs module {mod[k][2]}")
    side_of = dict(dies)
    want = sorted((d, v[0], v[1], SIDE_DIR_T[side_of[d]],
                   float(np.min(rb["l"][v[0]:v[1] + 1])) if SIDE_DIR_T[side_of[d]] == 1
                   else float(np.max(rb["h"][v[0]:v[1] + 1])))
                  for (d, _), v in hand.items() if v[2] == "hold")
    lf = BK.frame_l(sym, "4h")
    got = sorted((int(c_.die_i), int(c_.touch_i), int(c_.known_i), int(c_.direction),
                  float(c_.extreme)) for c_ in T.candidates(lf, fx, "scan_tap89"))
    if got != want:
        diff = sorted(set(got) ^ set(want))[:3]
        bad.append(f"HOLD-ENTRY {sym} {scale}: the module's {len(got)} candidates are not the "
                   f"{len(want)} hand holds (die, touch, entry, dir, extreme); symmetric "
                   f"difference e.g. {diff}")
    if tally is not None:
        vals = list(hand.values())
        tally["dies"] += len(dies)
        tally["rows"] += len(vals)
        tally["hold"] += sum(1 for v in vals if v[2] == "hold")
        tally["failed"] += sum(1 for v in vals if v[2] == "failed")
        tally["truncated"] += sum(1 for v in vals if v[2] == "truncated")
        tally["rescued"] += sum(1 for (d, s), v in hand.items() if v[2] == "hold" and s > 0)
        ex = tally.setdefault("examples", {})
        for (d, sq), v in sorted(hand.items()):
            cat = ("rescued hold" if v[2] == "hold" and sq > 0 else "hold" if v[2] == "hold"
                   else v[2])
            if len(ex.get(cat, [])) >= (2 if cat == "hold" else 1):
                continue
            j, sd = v[0], side_of[d]
            sg = -1 if sd == "top" else 1
            ex.setdefault(cat, []).append(
                f"{cat}: {sym} {scale} death {iso(rb['om'][d])} ({sd}) touch #{sq} at "
                f"{iso(rb['om'][j])}: low {rb['l'][j]:.10g} high {rb['h'][j]:.10g} EMA89 "
                f"{rb['band'][j]:.10g} prior close {rb['c'][j - 1]:.10g} vs prior EMA89 "
                f"{rb['band'][j - 1]:.10g}; closes touch..+3 "
                f"{[float(f'{x:.10g}') for x in rb['c'][j:j + 4]]} vs far edge EMA89 "
                f"{'-' if sg < 0 else '+'} 1.0 x ATR "
                f"{[float(f'{rb['band'][x] + sg * MARGIN_T * rb['atr'][x]:.10g}') for x in range(j, min(j + 4, rb['n']))]} "
                f"-> {v[2]} (known {iso(rb['om'][min(j + HOLD_T, rb['n'] - 1)])})")
    return bad


def hold_break():
    orig_rows, orig_cands = T.scan_rows, T.candidates

    def relabel(fx, source):
        r = orig_rows(fx, source)
        r["retest_outcome"] = "hold"
        return r

    def oneshot(fx, source):
        return orig_rows(fx, source.replace("scan_", "oneshot_"))

    def at_touch(lf, fx, source):
        return [dataclasses.replace(c, known_i=c.touch_i) for c in orig_cands(lf, fx, source)]

    return plants([
        ("every retest relabelled a HOLD (the module's scan rows)", "HOLD-VERDICT",
         under(T, "scan_rows", relabel, lambda: hold_findings("ETHUSDT", "calibrated"))),
        ("the one-shot law (C.retest_holds) under the scan's name", "HOLD-ROWS",
         under(T, "scan_rows", oneshot, lambda: hold_findings("ETHUSDT", "calibrated"))),
        ("the entry moved to the TOUCH bar (a 3-bar look-ahead)", "HOLD-ENTRY",
         under(T, "candidates", at_touch, lambda: hold_findings("ETHUSDT", "calibrated"))),
    ])


def hold_real():
    lines, bad = [], []
    for scale in ("calibrated", "frozen3.0"):
        t = {"dies": 0, "rows": 0, "hold": 0, "failed": 0, "truncated": 0, "rescued": 0}
        for s in CLASSIC5_T:
            bad += hold_findings(s, scale, t)
        ok_n = (t["hold"] >= MIN_HOLDS_T and t["failed"] >= MIN_FAILED_T
                and t["rescued"] >= MIN_RESCUED_T)
        if not ok_n:
            bad.append(f"HOLD-CARDINALITY {scale}: {t}")
        lines.append(f"{scale}: {t['dies']} deaths, {t['rows']} evaluated touches walked by "
                     f"hand = module ({t['hold']} holds, {t['failed']} failed, "
                     f"{t['truncated']} truncated, {t['rescued']} holds after a failed touch)")
        for cat in ("hold", "rescued hold", "failed"):
            for ex in t.get("examples", {}).get(cat, []):
                say(f"      hand-walked {ex}")
    return (not bad), (" · ".join(lines) + "; deaths are N's (the death detector is not on "
                       "trial here: F-NEST-ASOF / F-EQ-SCAN); raw bars == N.load11 == BK.frame_l "
                       "on all five; "
                       "every module candidate == a hand hold (entry = touch + 3, dir = the "
                       "death's, extreme over touch..entry)"
                       + (f"; findings {bad[:3]}" if bad else ""))


# ═══════════════════════════════════════════════════════════════ F-BRK-RIDE
_V6: dict = {}


def v6_book() -> list:
    if "book" not in _V6:
        lo, hi, _ = TP.corridor_n(CLASSIC5_T)
        _V6["book"] = list(TP.run_cell_n(TP.CONTROL_CARD, T9.V6_ROLES, CLASSIC5_T, lo, hi))
    return _V6["book"]


def reride(bend=None) -> list:
    """v6's own entries and stops, re-entered through the module's BRK path."""
    out = []
    for sym in CLASSIC5_T:
        lf = BK.frame_l(sym, "4h")
        lo_i, hi_i, _ = T.window(sym, "CLASSIC5")
        legs = [BK.Leg(direction=t.direction, entry_i=t.entry_i, stop_px=t.stop_px,
                       r_dist=t.r_dist, anchor=t.anchor)
                for t in v6_book() if t.symbol == sym]
        if bend is not None:
            legs = bend(sym, legs)
        out += T.ride(lf, legs, lo_i, hi_i, "card")
    return out


def ctrl_vec(t) -> dict:
    v = {c: getattr(t, c) for c in CTRL_COLS_T if c != "n_advances"}
    v["n_advances"] = len(t.advances)
    return v


def ride_findings(got: list, want: list) -> tuple[list[str], float]:
    out, worst = [], 0.0
    if len(got) != len(want):
        return [f"RIDE-CTRL count {len(got)} != v6 {len(want)}"], float("inf")
    g = sorted(got, key=lambda t: (t.symbol, t.entry_i))
    w = sorted(want, key=lambda t: (t.symbol, t.entry_i))
    for a, b in zip(g, w):
        if a.symbol != b.symbol or a.entry_i != b.entry_i:
            out.append(f"RIDE-CTRL key {a.symbol}@{a.entry_i} vs {b.symbol}@{b.entry_i}")
            continue
        for f_ in CMP_EXACT_T:
            if getattr(a, f_) != getattr(b, f_):
                out.append(f"RIDE-CTRL {a.symbol} {iso(a.entry_ms)} {f_}: {getattr(a, f_)!r} "
                           f"vs v6 {getattr(b, f_)!r}")
        va, vb = ctrl_vec(a), ctrl_vec(b)
        for c in CTRL_COLS_T:
            d = abs(float(va[c]) - float(vb[c]))
            worst = max(worst, d)
            if d != 0.0:
                out.append(f"RIDE-CTRL {a.symbol} {iso(a.entry_ms)} {c}: {va[c]!r} vs v6 "
                           f"{vb[c]!r} (|d| {d:.3e})")
    return out, worst


def ride_break():
    def stop_tick(sym, legs):
        if sym != "BTCUSDT":
            return legs
        L0 = legs[0]
        return [dataclasses.replace(L0, stop_px=L0.stop_px - 0.1 * L0.direction,
                                    r_dist=L0.r_dist + 0.1)] + legs[1:]

    def corrupt():
        got = reride()
        bad = copy.copy(got[0])
        object.__setattr__(bad, "net_r", float(got[0].net_r) + 1e-12)
        return ride_findings([bad] + got[1:], v6_book())[0]

    return plants([
        ("the 12/25 ribbon bell switched on (RIBBON = (12, 25), TC10's BRK bell)", "RIDE-CTRL",
         under(T, "RIBBON", (12, 25), lambda: ride_findings(reride(), v6_book())[0])),
        ("the taker fee doubled (BK.FEE_BPS_SIDE 10)", "RIDE-CTRL",
         under(BK, "FEE_BPS_SIDE", 10.0, lambda: ride_findings(reride(), v6_book())[0])),
        ("BTC's first leg's stop one tick (0.1) further", "RIDE-CTRL",
         lambda: ride_findings(reride(stop_tick), v6_book())[0]),
        ("one net_r +1e-12 in a COPY of the re-ridden book", "RIDE-CTRL", corrupt),
    ])


def ride_real():
    got, want = reride(), v6_book()
    bad, worst = ride_findings(got, want)
    if len(want) != V6_N_T:
        bad.append(f"RIDE-CTRL v6 n {len(want)} != typed {V6_N_T}")
    ok_j, w_j, why_j = TP.ctrl_diff(TP.journal_frame(got), TP.journal_frame(want))
    if not ok_j:
        bad.append(f"RIDE-CTRL journal_frame ctrl_diff: {why_j}")
    n_fund = sum(1 for t in want if t.funding_r)
    n_harv = sum(1 for t in want if t.harvested)
    n_adv = sum(len(t.advances) for t in want)
    reasons = sorted({t.exit_reason for t in want})
    return (not bad), (f"{len(got)} v6 campaigns re-entered through T.window + T.ride "
                       f"(BK.brk_campaigns, ribbon None): worst |d| on the 12 CTRL_COLS "
                       f"{worst:.3e}; exit reasons and entry_i/exit_i/harvested/harvest_i/"
                       f"bars_held identical; TP.ctrl_diff on the journals: {why_j}; exercised: "
                       f"{n_fund} campaigns carry funding, {n_harv} harvested, {n_adv} trail "
                       f"advances, exit reasons {reasons}"
                       + (f"; findings {bad[:3]}" if bad else ""))


# ═══════════════════════════════════════════════════════════════ F-BRK-TIDE
def _arm(name: str):
    return next(a for a in T.ARMS if a.name == name)


def tide_real_findings(arms=RIDDEN_T, count: dict | None = None) -> list[str]:
    out = []
    for an in arms:
        a = _arm(an)
        for sym in PANEL_T[ARM_PANEL_T[an]]:
            lf = BK.frame_l(sym, "4h")
            rb = raw(sym)
            lo_i, hi_i, _ = T.window(sym, a.panel)
            fx = T.facts(sym, ARM_EVENT_T[an][0])
            cands = T.candidates(lf, fx, a.source)
            _, disp = T.dispose(lf, cands, a.lane, lo_i, hi_i, T.tide_series(lf))
            for c, x in zip(cands, disp):
                if x in ("out_of_window", "out_of_tape", "no_atr"):
                    continue
                i, d = int(c.known_i), int(c.direction)
                want_ok = int(rb["tide"][i]) == d
                got_ok = x != "tide"
                if count is not None:
                    count["tested"] += 1
                    count["flip"] += int(rb["tide"][i] != rb["tide"][i - 1])
                if want_ok != got_ok:
                    out.append(f"TIDE-BAR {an} {sym} entry {iso(rb['om'][i])} dir {d}: hand "
                               f"tide {int(rb['tide'][i])} (prev bar {int(rb['tide'][i - 1])}) "
                               f"-> {'admit' if want_ok else 'refuse'}, module {x}")
    return out


def planted(sym: str) -> list:
    """Per asset, the first two bars of each kind inside the ride window:
    flip-in long/short (tide == d at the entry bar, != d at the bar before),
    flip-out long/short (the reverse), clause long/short (EMA89 beyond EMA316
    but the close not beyond EMA316: tide 0)."""
    rb = raw(sym)
    lo_i, hi_i, _ = T.window(sym, "CLASSIC5")
    td, e89, e316, c = rb["tide"], rb["e89"], rb["e316"], rb["c"]
    kinds = {"flip-in long": [], "flip-in short": [], "flip-out long": [],
             "flip-out short": [], "clause long": [], "clause short": []}
    # the planted touch sits at i - 3 and the flip test reads i - 1: start at lo_i + 3
    # so neither index can leave the window (or wrap below bar 0 under a mutated floor)
    for i in range(max(int(lo_i), 1) + 3, hi_i + 1):
        for d, nm in ((1, "long"), (-1, "short")):
            if td[i] == d and td[i - 1] != d:
                kinds[f"flip-in {nm}"].append((i, d))
            if td[i - 1] == d and td[i] != d:
                kinds[f"flip-out {nm}"].append((i, d))
        if e89[i] > e316[i] and c[i] <= e316[i]:
            kinds["clause long"].append((i, 1))
        if e89[i] < e316[i] and c[i] >= e316[i]:
            kinds["clause short"].append((i, -1))
    out = []
    for k, v in kinds.items():
        for i, d in v[:2]:
            seg = slice(i - 3, i + 1)
            ext = float(np.min(rb["l"][seg])) if d == 1 else float(np.max(rb["h"][seg]))
            out.append((k, BK.Candidate(direction=d, anchor="tap89", die_i=-i, touch_i=i - 3,
                                        known_i=i, extreme=ext, rid=-1, verdict="hold",
                                        note=f"PLANTED {k}")))
    return out


def tide_planted_findings(count: dict | None = None) -> list[str]:
    out = []
    for sym in CLASSIC5_T:
        lf = BK.frame_l(sym, "4h")
        rb = raw(sym)
        lo_i, hi_i, _ = T.window(sym, "CLASSIC5")
        pl = planted(sym)
        _, disp = T.dispose(lf, [c for _, c in pl], T.LANE, lo_i, hi_i, T.tide_series(lf))
        for (k, c), x in zip(pl, disp):
            i, d = int(c.known_i), int(c.direction)
            want_ok = int(rb["tide"][i]) == d
            got_ok = x != "tide"
            if count is not None:
                count[k] = count.get(k, 0) + 1
            if want_ok != got_ok:
                out.append(f"TIDE-BAR planted {k} {sym} {iso(rb['om'][i])}: hand tide "
                           f"{int(rb['tide'][i])} (prev {int(rb['tide'][i - 1])}) -> "
                           f"{'admit' if want_ok else 'refuse'}, module {x}")
    return out


def tide_break():
    def prev_bar(lf):
        return BK.tide_4h_for_exec(lf.open_ms, lf)[0]

    def one_clause(lf):
        ra = BK.roles_l(lf, T.ROLES)
        return np.sign(ra["tide_f"] - ra["tide_s"]).astype(np.int64)

    return plants([
        ("the PREVIOUS 4h bar's tide (BK.tide_4h_for_exec on the 4h frame)", "TIDE-BAR",
         under(T, "tide_series", prev_bar, lambda: tide_planted_findings())),
        ("the permission ignored (every candidate admitted)", "TIDE-BAR",
         under(T, "permit_of", lambda tide: (lambda i, d: {"ok": True}),
               lambda: tide_real_findings(("scored",)))),
        ("the close clause dropped (sign(EMA89 - EMA316) only)", "TIDE-BAR",
         under(T, "tide_series", one_clause, lambda: tide_planted_findings())),
    ])


def tide_real():
    cnt = {"tested": 0, "flip": 0}
    bad = tide_real_findings(RIDDEN_T, cnt)
    pc: dict = {}
    bad += tide_planted_findings(pc)
    prev_ok = 0
    for sym in CLASSIC5_T:
        lf = BK.frame_l(sym, "4h")
        pb = BK.tide_4h_for_exec(lf.open_ms, lf)[0]
        prev_ok += int(np.array_equal(pb[1:], T.tide_series(lf)[:-1]))
    return (not bad), (f"{cnt['tested']} real candidates (6 ridden arms) reached the permission "
                       f"test; the module agrees with this file's entry-bar tide on every one "
                       f"({cnt['flip']} of them sit on a bar where the tide differs from the "
                       f"bar before); planted {sum(pc.values())} candidates {pc} agree; "
                       f"disclosure: BK.tide_4h_for_exec on a 4h frame IS the previous bar's "
                       f"tide on {prev_ok}/5 assets"
                       + (f"; findings {bad[:3]}" if bad else ""))


# ═══════════════════════════════════════════════════════════════ F-BRK-ENTRY
def written_book(arm: str) -> pd.DataFrame:
    return pd.read_parquet(str(REG_OUT / f"{arm}.parquet"))


def entry_findings(book: pd.DataFrame, arm: str) -> list[str]:
    scale, frame_key, band, H = ARM_EVENT_T[arm]
    out = []
    for sym in PANEL_T[ARM_PANEL_T[arm]]:
        rb = raw(sym)
        ev = N.events(sym, "4h", scale)
        fr = ev[frame_key]
        fr = fr[fr["band"] == band]
        holds = fr[fr["verdict"] == "hold"]
        side_of = {int(r.die_i): str(r.side) for r in ev["deaths"].itertuples(index=False)}
        by_close = {int(r.known_close_ms): r for r in holds.itertuples(index=False)}
        close_to_i = {int(m) + MS4H: i for i, m in enumerate(rb["om"])}
        b = book[book["symbol"] == sym].sort_values("entry_close_ms", kind="mergesort")
        prev = None
        for r in b.itertuples(index=False):
            h_ = by_close.get(int(r.entry_close_ms))
            if h_ is None:
                out.append(f"ENTRY-NOT-HOLD {arm} {sym} {iso(r.entry_close_ms - MS4H)}: no "
                           f"{frame_key}/{band} hold row is known at that close")
            else:
                if int(h_.dir) != int(r.direction) or \
                        SIDE_DIR_T[side_of[int(h_.die_i)]] != int(r.direction):
                    out.append(f"ENTRY-DIR {arm} {sym} {iso(r.entry_ms)}: book dir "
                               f"{int(r.direction)}, hold row {int(h_.dir)}, death "
                               f"{side_of[int(h_.die_i)]}")
                if int(h_.known_at) - int(h_.touch_i) != H:
                    out.append(f"ENTRY-NOT-HOLD {arm} {sym}: known_at - touch != {H}")
            i = close_to_i.get(int(r.entry_close_ms))
            if i is None or int(r.entry_close_ms) - int(r.entry_ms) != MS4H \
                    or float(r.entry_px) != float(rb["c"][i]):
                out.append(f"ENTRY-PX {arm} {sym} {iso(r.entry_ms)}: stamp/price is not the "
                           f"raw close of the entry bar")
            elif h_ is not None:
                d, j, a_ = int(r.direction), int(h_.touch_i), float(rb["atr"][i])
                ext = float(np.min(rb["l"][j:i + 1])) if d == 1 else float(np.max(rb["h"][j:i + 1]))
                piv, rail = ext - d * STOP_BUF_T * a_, float(rb["c"][i]) - d * RAIL_T * a_
                stop = min(piv, rail) if d == 1 else max(piv, rail)
                # the rail is IN the farther-of law (R >= 1.0 ATR in exact arithmetic; a
                # rail-bound R = |entry - (entry - ATR)| carries float rounding, so R is held
                # to the law's own arithmetic, never to a bound)
                if float(r.stop_px) != stop or float(r.r_dist) != abs(float(rb["c"][i]) - stop):
                    out.append(f"ENTRY-STOP {arm} {sym} {iso(r.entry_ms)}: stop {r.stop_px!r} / R "
                               f"{r.r_dist!r} vs hand {stop!r} / {abs(float(rb['c'][i]) - stop)!r} "
                               f"(extreme {ext!r} over touch..entry -/+ {STOP_BUF_T} ATR, rail "
                               f"{RAIL_T} ATR {a_!r})")
            if prev is not None and int(r.entry_ms) < int(prev.exit_close_ms):
                out.append(f"ENTRY-OVERLAP {arm} {sym}: entry {iso(r.entry_ms)} while the "
                           f"campaign entered {iso(prev.entry_ms)} is open until "
                           f"{iso(int(prev.exit_close_ms) - MS4H)}")
            prev = r
        # the greedy one-position walk over the in-window, tide-aligned holds
        exits = {int(r.entry_close_ms): close_to_i.get(int(r.exit_close_ms))
                 for r in b.itertuples(index=False)}
        want, last_exit = set(), -1
        n = rb["n"]
        for h_ in holds.sort_values("known_at", kind="mergesort").itertuples(index=False):
            i, d = int(h_.known_at), int(h_.dir)
            if not (FLOOR_T <= i <= n - 1) or int(rb["tide"][i]) != d or i <= last_exit:
                continue
            ce = int(rb["om"][i]) + MS4H
            want.add(ce)
            if ce not in exits:
                out.append(f"ENTRY-MISSING {arm} {sym} {iso(rb['om'][i])}: an aligned "
                           f"in-window hold with the asset flat is not in the book")
                break
            last_exit = exits[ce] if exits[ce] is not None else n
        extra = sorted(set(exits) - want)
        for ce in extra[:3]:
            out.append(f"ENTRY-EXTRA {arm} {sym} {iso(ce - MS4H)}: in the book but not in the "
                       f"greedy walk (refused, overlapped or not a hold)")
    return out


def entry_break():
    """Each plant takes a REAL qualifying row of the build when there is one and is
    BUILT BY CONSTRUCTION when there is none — a plant never indexes past the end
    (a crashed plant is a fixture defect, not a catch).  The plant's name says
    which it was."""
    arm = "scored"
    bk = written_book(arm)
    cands = pd.read_parquet(str(OUT / "T_BRK_CANDIDATES.parquet"))
    cs = cands[cands["arm"] == arm]
    scan = pd.read_parquet(str(OUT / "T_BRK_SCAN.parquet"))
    sa = scan[scan["arm"] == arm]
    hold_close = {(str(x), int(m)) for x, m, o in zip(sa["symbol"], sa["known_close_ms"],
                                                      sa["retest_outcome"]) if o == "hold"}
    first = bk.sort_values(["symbol", "entry_close_ms"], kind="mergesort").iloc[0]

    def nth(df: pd.DataFrame, k: int):
        return df.iloc[min(int(k), len(df) - 1)]

    def with_row(sym: str, close_ms: int, d: int) -> pd.DataFrame:
        b = bk.copy()
        tm = b[b["symbol"] == sym]
        r = (tm if len(tm) else b).iloc[0].copy()
        rb = raw(sym)
        i = int(np.searchsorted(rb["om"], close_ms - MS4H))
        r["symbol"] = sym
        r["entry_ms"], r["entry_close_ms"] = close_ms - MS4H, close_ms
        r["exit_close_ms"], r["direction"], r["entry_px"] = close_ms + MS4H, d, float(rb["c"][i])
        return pd.concat([b, r.to_frame().T.astype(b.dtypes.to_dict())], ignore_index=True)

    # ── the picks, decided once: real if the build has one, else constructed ──
    po = cs[cs["disposition"] == "position_open"]
    if len(po):
        r_ = po.iloc[0]
        po_name, po_args = "a real position-open candidate inserted", (
            str(r_["symbol"]), int(r_["entry_close_ms"]), int(r_["direction"]))
    else:
        po_name, po_args = ("constructed: the first campaign re-entered on the next bar while "
                            "it is open"), (str(first["symbol"]),
                                            int(first["entry_close_ms"]) + MS4H,
                                            int(first["direction"]))
    fl = sa[(sa["retest_outcome"] == "failed") & (sa["known_at"] >= FLOOR_T)
            & (sa["known_close_ms"] > 0)]
    fl = fl[[(str(x), int(m)) not in hold_close for x, m in zip(fl["symbol"], fl["known_close_ms"])]]
    if len(fl):
        r_ = nth(fl, 3)
        fe_name, fe_args = "a real FAILED retest entered", (
            str(r_["symbol"]), int(r_["known_close_ms"]), int(r_["dir"]))
    else:
        k, c0 = 2, int(first["entry_close_ms"])
        while (str(first["symbol"]), c0 + k * MS4H) in hold_close:
            k += 1
        fe_name, fe_args = ("constructed: an entry at a close no hold row is known at"), (
            str(first["symbol"]), c0 + k * MS4H, int(first["direction"]))
    td = cs[(cs["disposition"] == "tide")]
    if len(td):
        r_ = nth(td, 2)
        td_name, td_args = "a real tide-refused hold entered", (
            str(r_["symbol"]), int(r_["entry_close_ms"]), int(r_["direction"]))
    else:
        td_name, td_args = "constructed: a hold whose entry-bar tide (this file's) is not aligned", None
        for r_ in sa[(sa["retest_outcome"] == "hold") & (sa["known_at"] >= FLOOR_T)].itertuples(
                index=False):
            rb = raw(str(r_.symbol))
            if int(r_.known_at) < rb["n"] and int(rb["tide"][int(r_.known_at)]) != int(r_.dir):
                td_args = (str(r_.symbol), int(r_.known_close_ms), int(r_.dir))
                break
    rails = np.flatnonzero(bk["rail_binding"].to_numpy(bool))
    rl_name = ("a rail-bound stop railed at 0.5 ATR instead of 1.0" if len(rails) else
               "constructed: the first campaign's stop set at 0.5 ATR (no rail-bound stop)")
    rl_k = bk.index[int(rails[0])] if len(rails) else bk.index[0]

    def flipped():
        b = bk.copy()
        k = b.index[min(5, len(b) - 1)]
        b.loc[k, "direction"] = -int(b.loc[k, "direction"])
        return entry_findings(b, arm)

    def at_touch():
        b = bk.copy()
        k = b.index[min(7, len(b) - 1)]
        sh = int(b.loc[k, "entry_close_ms"]) - int(b.loc[k, "touch_close_ms"])
        b.loc[k, "entry_ms"] = int(b.loc[k, "entry_ms"]) - sh
        b.loc[k, "entry_close_ms"] = int(b.loc[k, "touch_close_ms"])
        return entry_findings(b, arm)

    def tide_refused():
        if td_args is None:
            return ["PLANT-UNBUILDABLE: no hold of the build has a misaligned entry-bar tide"]
        return entry_findings(with_row(*td_args), arm)

    def dropped():
        return entry_findings(bk.drop(index=bk.index[min(11, len(bk) - 1)]).reset_index(drop=True),
                              arm)

    def rail_half():
        b = bk.copy()
        d, a_ = int(b.loc[rl_k, "direction"]), float(b.loc[rl_k, "atr_at_entry"])
        b.loc[rl_k, "stop_px"] = float(b.loc[rl_k, "entry_px"]) - d * 0.5 * a_
        b.loc[rl_k, "r_dist"] = 0.5 * a_
        return entry_findings(b, arm)

    return plants([
        ("a campaign's direction flipped", "ENTRY-DIR", flipped),
        ("an entry moved to its touch bar", "ENTRY-NOT-HOLD", at_touch),
        (po_name, "ENTRY-OVERLAP", lambda: entry_findings(with_row(*po_args), arm)),
        (fe_name, "ENTRY-NOT-HOLD", lambda: entry_findings(with_row(*fe_args), arm)),
        (td_name, "ENTRY-EXTRA", tide_refused),
        ("a campaign dropped", "ENTRY-MISSING", dropped),
        (rl_name, "ENTRY-STOP", rail_half),
    ])


def entry_real():
    bad, parts = [], []
    for arm in RIDDEN_T:
        b = written_book(arm)
        bad += entry_findings(b, arm)
        parts.append(f"{arm} {len(b)}")
    return (not bad), (f"every campaign of the six WRITTEN ridden-arm regbooks ({', '.join(parts)}) "
                       f"enters at the known_at close of its own scan's hold row, direction = "
                       f"the row's = its death's, entry_px = the raw close, stop = the farther of "
                       f"(retest extreme over touch..entry -/+ 0.5 ATR, entry -/+ 1.0 ATR) with "
                       f"this file's ATR14 — exact, R = |entry - stop|; no two campaigns of "
                       f"one asset overlap; each book IS the greedy one-position walk over the "
                       f"in-window (bar >= 316) holds whose entry-bar tide is aligned"
                       + (f"; findings {bad[:3]}" if bad else ""))


# ═══════════════════════════════════════════════════════════════ F-BRK-EXIT
_HF: dict = {}


def hand_frame(sym: str) -> dict:
    """raw() plus what the hand ride reads, all this file's own: EMA12, the counter
    crosses 12/89 and 89/316 (a > b now, a <= b the bar before; mirror), the strict
    (2,2) pivots keyed at their CONFIRMATION bar (p + 2), and the funding prints
    floored to their hour, kept at hour <= the pin, summed per hour, ascending."""
    if sym in _HF:
        return _HF[sym]
    rb = raw(sym)
    c, h, l = rb["c"], rb["h"], rb["l"]
    e12 = hand_ema(c, WIN_F_T)
    e89, e316 = rb["e89"], rb["e316"]

    def up(a, b):
        o = np.zeros(len(a), bool)
        o[1:] = (a[1:] > b[1:]) & (a[:-1] <= b[:-1])
        return o

    def dn(a, b):
        o = np.zeros(len(a), bool)
        o[1:] = (a[1:] < b[1:]) & (a[:-1] >= b[:-1])
        return o

    lowp, highp = {}, {}
    for q in range(2, len(c) - 2):
        if l[q] < min(l[q - 2], l[q - 1]) and l[q] < min(l[q + 1], l[q + 2]):
            lowp[q + 2] = (float(l[q]), q)
        if h[q] > max(h[q - 2], h[q - 1]) and h[q] > max(h[q + 1], h[q + 2]):
            highp[q + 2] = (float(h[q]), q)
    f = pd.read_parquet(str(TC11_SNAP / "funding" / f"{sym}.parquet"))
    hour = f["funding_time"].to_numpy(np.int64) // MS1H * MS1H
    fd = pd.DataFrame({"hour": hour, "rate": f["funding_rate"].to_numpy(float)})
    g = fd[fd["hour"] <= PIN].groupby("hour", sort=True)["rate"].sum()
    _HF[sym] = dict(rb, e12=e12, w_up=up(e12, e89), w_dn=dn(e12, e89), b_up=up(e89, e316),
                    b_dn=dn(e89, e316), lowp=lowp, highp=highp,
                    fh=g.index.to_numpy(np.int64), fr=g.to_numpy(float),
                    closes=rb["om"] + MS4H)
    return _HF[sym]


def hand_funding(hf: dict, t_entry: int, t_fill_open: int, d: int, qty: float) -> tuple:
    """Every print with t_entry < hour <= t_fill_open, priced at the close of the
    last bar CLOSED at or before it, added one at a time in hour order."""
    fh, fr = hf["fh"], hf["fr"]
    lo = int(np.searchsorted(fh, t_entry, side="right"))
    hi = int(np.searchsorted(fh, t_fill_open, side="right"))
    amt, n = 0.0, 0
    for q in range(lo, hi):
        k = int(np.searchsorted(hf["closes"], fh[q], side="right")) - 1
        if k < 0:
            continue
        amt += float(fr[q]) * float(hf["c"][k]) * d * qty
        n += 1
    return amt, n


def hand_ride(sym: str, d: int, ti: int, stop0: float, R: float) -> dict:
    """THIS FILE'S v6 ride + accounting, bar by bar from the entry bar + 1 to the
    last bar closed at the pin: STOP (the adverse extreme reaches the stop; fills AT
    the stop) -> BELL (counter 12/89, then counter 89/316; fills at the close) ->
    HARVEST (first touch only: armed once a prior close sits outside the 89/316 near
    edge; the bar's extreme meets the near edge; 50% at that bar's close) -> TRAIL
    (armed once the favourable extreme has reached +1R; on a pivot confirmation bar,
    candidate = pivot -/+ 0.5 ATR, rail = close -/+ 1.0 ATR, admitted = the farther;
    advance-only and >= 0.05 ATR; governs the NEXT bar)."""
    hf = hand_frame(sym)
    h, l, c, atr, e89, e316 = hf["h"], hf["l"], hf["c"], hf["atr"], hf["e89"], hf["e316"]
    hi = hf["n"] - 1
    e, stop = float(c[ti]), float(stop0)
    harv, h_armed, t_armed, adv = None, False, False, []
    xi, xpx, why = hi, float(c[hi]), "corridor_end"
    trace = []
    for j in range(ti + 1, hi + 1):
        fav = float(h[j]) if d == 1 else float(l[j])
        if not t_armed and (fav - e) * d / R >= TRAIL_ARM_R_T:
            t_armed = True
        pe = max(e89[j - 1], e316[j - 1]) if d == 1 else min(e89[j - 1], e316[j - 1])
        if not h_armed and ((c[j - 1] > pe) if d == 1 else (c[j - 1] < pe)):
            h_armed = True
        edge = max(e89[j], e316[j]) if d == 1 else min(e89[j], e316[j])
        touch = (harv is None and h_armed and ((l[j] <= edge) if d == 1 else (h[j] >= edge))
                 and (float(c[j]) - e) * d / R >= HARV_MIN_T)
        if (d == 1 and l[j] <= stop) or (d == -1 and h[j] >= stop):
            xi, xpx, why = j, stop, "stop"
            trace.append(f"stop on the bar closing {iso(hf['closes'][j])} ({'low' if d == 1 else 'high'} "
                         f"{float(l[j] if d == 1 else h[j]):.10g} vs stop {stop:.10g})")
            break
        if d == 1:
            bell = (f"bell_{WIN_F_T}_{WIN_S_T}" if hf["w_dn"][j] else
                    f"bell_{TIDE_F}_{TIDE_S}" if hf["b_dn"][j] else None)
        else:
            bell = (f"bell_{WIN_F_T}_{WIN_S_T}" if hf["w_up"][j] else
                    f"bell_{TIDE_F}_{TIDE_S}" if hf["b_up"][j] else None)
        if bell:
            xi, xpx, why = j, float(c[j]), bell
            trace.append(f"{bell} on the bar closing {iso(hf['closes'][j])} (EMA{WIN_F_T} {hf['e12'][j]:.10g}, "
                         f"EMA89 {e89[j]:.10g}, EMA316 {e316[j]:.10g}) -> close {float(c[j]):.10g}")
            break
        if touch:
            harv = (j, float(c[j]))
            trace.append(f"harvest on the bar closing {iso(hf['closes'][j])} ({'low' if d == 1 else 'high'} "
                         f"{float(l[j] if d == 1 else h[j]):.10g} meets the near edge "
                         f"{float(edge):.10g}) -> {HARV_Q_T} at close {float(c[j]):.10g}")
        if t_armed:
            pv = (hf["lowp"] if d == 1 else hf["highp"]).get(j)
            if pv is not None:
                a_ = float(atr[j])
                if d == 1:
                    adm = min(pv[0] - TRAIL_BUF_T * a_, float(c[j]) - TRAIL_RAIL_T * a_)
                    ok = adm > stop
                else:
                    adm = max(pv[0] + TRAIL_BUF_T * a_, float(c[j]) + TRAIL_RAIL_T * a_)
                    ok = adm < stop
                if ok and abs(adm - stop) / a_ >= TRAIL_MIN_ADV_T:
                    adv.append((j, float(adm)))
                    trace.append(f"trail on the bar closing {iso(hf['closes'][j])} (pivot "
                                 f"{pv[0]:.10g}, bar closing {iso(hf['closes'][pv[1]])}) "
                                 f"{stop:.10g} -> {float(adm):.10g}")
                    stop = float(adm)
    bps = FEE_BPS_T / 10_000.0
    t0 = int(hf["om"][ti])
    if harv is None:
        g, fe = (xpx - e) * d, bps * (e + xpx)
        u, nf = hand_funding(hf, t0, int(hf["om"][xi]), d, 1.0)
    else:
        hj, hpx = harv
        q = HARV_Q_T
        g1, fe1 = q * (hpx - e) * d, bps * q * (e + hpx)
        u1, n1 = hand_funding(hf, t0, int(hf["om"][hj]), d, q)
        g2, fe2 = (1.0 - q) * (xpx - e) * d, bps * (1.0 - q) * (e + xpx)
        u2, n2 = hand_funding(hf, t0, int(hf["om"][xi]), d, 1.0 - q)
        g, fe, u, nf = g1 + g2, fe1 + fe2, u1 + u2, n1 + n2
    gross, fee, fund_raw = g / R, fe / R, u / R
    fund = FUND_CAP_T if fund_raw > FUND_CAP_T else fund_raw
    return {"exit_i": xi, "exit_close_ms": int(hf["closes"][xi]), "exit_px": xpx,
            "exit_reason": why, "harvest": harv, "adv": adv, "gross_r": gross, "fee_r": fee,
            "funding_r": fund, "funding_capped": bool(fund_raw > FUND_CAP_T), "net_r": gross - fee - fund,
            "n_fund": nf, "trace": trace}


ECON_T = ("gross_r", "fee_r", "funding_r", "net_r")


def exit_kind(x: dict) -> str | None:
    if x["exit_reason"] == "stop" and not x["adv"]:
        return EXIT_KINDS_T[0]
    if x["exit_reason"].startswith("bell_") and x["harvest"] is not None:
        return EXIT_KINDS_T[1]
    if x["exit_reason"] == "stop" and x["adv"]:
        return EXIT_KINDS_T[2]
    return None


def exit_findings(book: pd.DataFrame, arm: str, tally: dict | None = None) -> list[str]:
    """(a) the engine's re-ride of every written campaign, (b) this file's hand
    ride, both against the WRITTEN row; exact."""
    out = []
    panel = PANEL_T[ARM_PANEL_T[arm]]
    for sym in panel:
        b = book[book["symbol"] == sym].sort_values("entry_close_ms", kind="mergesort")
        if not len(b):
            continue
        hf = hand_frame(sym)
        lf = BK.frame_l(sym, "4h")
        if not (np.array_equal(lf.open_ms, hf["om"]) and np.array_equal(lf.c, hf["c"])
                and np.array_equal(lf.h, hf["h"]) and np.array_equal(lf.l, hf["l"])):
            out.append(f"EXIT-BARS {sym}: raw 4h bars != BK.frame_l")
            continue
        if int(hf["closes"][-1]) != PIN:
            out.append(f"EXIT-BARS {sym}: the last raw bar closes {iso(hf['closes'][-1])}, not the pin")
        tis = np.searchsorted(hf["om"], b["entry_ms"].to_numpy(np.int64))
        if np.any(tis >= hf["n"]) or not np.array_equal(hf["om"][np.minimum(tis, hf["n"] - 1)],
                                                         b["entry_ms"].to_numpy(np.int64)):
            out.append(f"EXIT-BARS {arm} {sym}: an entry_ms is not a raw bar open")
            continue
        # (a) the engine's re-ride of the WRITTEN entries and stops
        legs = [BK.Leg(direction=int(r.direction), entry_i=int(ti), stop_px=float(r.stop_px),
                       r_dist=float(r.r_dist)) for r, ti in zip(b.itertuples(index=False), tis)]
        eng = BK.brk_campaigns(lf, legs, TP.CONTROL_CARD, T9.V6_ROLES, str(b["lane"].iloc[0]), 0,
                               lf.n - 1, ribbon=None, active=BK.COMPONENTS, era=None, account=True)
        if len(eng) != len(b):
            out.append(f"EXIT-RIDE {arm} {sym}: the engine rides {len(eng)} of the {len(b)} written "
                       f"campaigns (an overlap the one-position law refuses)")
        else:
            for r, t in zip(b.itertuples(index=False), eng):
                got = {"exit_close_ms": int(r.exit_close_ms), "exit_reason": str(r.exit_reason),
                       **{k: float(getattr(r, k)) for k in ECON_T}}
                want = {"exit_close_ms": int(lf.close_ms[int(t.exit_i)]),
                        "exit_reason": str(t.exit_reason),
                        **{k: float(getattr(t, k)) for k in ECON_T}}
                for k in got:
                    if got[k] != want[k]:
                        out.append(f"EXIT-RIDE {k} {arm} {sym} {iso(r.entry_ms)}: book {got[k]!r} "
                                   f"vs engine {want[k]!r}")
        # (b) this file's hand ride
        for r, ti in zip(b.itertuples(index=False), tis):
            ti = int(ti)
            if ti < FLOOR_T:
                out.append(f"EXIT-WARM {arm} {sym} {iso(r.entry_ms)}: entry bar {ti} < {FLOOR_T}")
                continue
            x = hand_ride(sym, int(r.direction), ti, float(r.stop_px), float(r.r_dist))
            chk = [("exit_close_ms", int(r.exit_close_ms), x["exit_close_ms"]),
                   ("exit_reason", str(r.exit_reason), x["exit_reason"])]
            chk += [(k, float(getattr(r, k)), x[k]) for k in ECON_T]
            if "exit_i" in b.columns:
                chk += [("exit_i", int(r.exit_i), x["exit_i"]),
                        ("exit_px", float(r.exit_px), x["exit_px"]),
                        ("harvested", bool(r.harvested), x["harvest"] is not None),
                        ("n_advances", int(r.n_advances), len(x["adv"]))]
            for k, g_, w_ in chk:
                if g_ != w_:
                    out.append(f"EXIT-HAND {k} {arm} {sym} {iso(r.entry_ms)}: book {g_!r} vs "
                               f"hand {w_!r}")
            if tally is not None:
                tally["n"] += 1
                tally["harvested"] += int(x["harvest"] is not None)
                tally["advances"] += len(x["adv"])
                tally["funding_prints"] += x["n_fund"]
                tally["capped"] += int(x["funding_capped"])
                tally["reasons"][x["exit_reason"]] = tally["reasons"].get(x["exit_reason"], 0) + 1
                kd = exit_kind(x)
                if kd is not None:
                    tally["kinds"][kd] = tally["kinds"].get(kd, 0) + 1
                    ex = tally.setdefault("examples", {})
                    if kd not in ex:
                        ex[kd] = (f"{kd}: {sym} {'long' if int(r.direction) == 1 else 'short'} "
                                  f"entered at the close {iso(r.entry_close_ms)} at "
                                  f"{float(r.entry_px)!r}, stop "
                                  f"{float(r.stop_px):.10g} (R {float(r.r_dist):.10g}); "
                                  + "; ".join(x["trace"])
                                  + f"; gross {x['gross_r']:+.6f} fee {x['fee_r']:+.6f} funding "
                                  f"{x['funding_r']:+.6f} ({x['n_fund']} prints) net "
                                  f"{x['net_r']:+.6f} = book {float(r.net_r):+.6f}")
    return out


def exit_break():
    bk = written_book("scored")

    def bent(fn):
        return exit_findings(fn(bk.copy()), "scored")

    def fund_sign(d):
        d["net_r"] = d["gross_r"] - d["fee_r"] + d["funding_r"]
        return d

    def stamp_late(d):
        d["exit_close_ms"] = d["exit_close_ms"] + MS4H
        return d

    def fee_half(d):
        d["fee_r"] = d["fee_r"] * 0.5
        return d

    def relabel(d):
        m = d["exit_reason"] == "bell_12_89"
        k = d.index[m][0] if m.any() else d.index[0]
        d.loc[k, "exit_reason"] = "bell_89_316" if d.loc[k, "exit_reason"] != "bell_89_316" else "stop"
        return d

    def fresh(**mut):
        """a FRESH T.run_arm of the scored arm under a module mutation"""
        def run():
            with contextlib.ExitStack() as st:
                for k, v in mut.items():
                    st.enter_context(mutated(T, k, v))
                return exit_findings(T.run_arm(_arm("scored"), E.fees())["book"], "scored")
        return run

    def no_harvest_ride(lf, legs, lo_i, hi_i, lane):
        return BK.brk_campaigns(lf, legs, T.CARD, T.ROLES, lane, lo_i, hi_i, ribbon=T.RIBBON,
                                active=tuple(x for x in BK.COMPONENTS if x != "harvest"),
                                era=None, account=True)

    return plants([
        ("net_r written as gross - fee + funding (a copy)", "EXIT-RIDE net_r",
         lambda: bent(fund_sign)),
        ("exit_close_ms one bar late (a copy)", "EXIT-HAND exit_close_ms",
         lambda: bent(stamp_late)),
        ("fee_r halved (a copy)", "EXIT-HAND fee_r", lambda: bent(fee_half)),
        ("an exit_reason relabelled (a copy)", "EXIT-RIDE exit_reason", lambda: bent(relabel)),
        ("the 12/25 ribbon bell switched on in a fresh module build (RIBBON = (12, 25))",
         "EXIT-HAND", fresh(RIBBON=(12, 25))),
        ("the harvest switched off in a fresh module build (T.ride without 'harvest')",
         "EXIT-HAND", fresh(ride=no_harvest_ride)),
    ])


def exit_real():
    bad, parts, tl = [], [], {}
    for arm in RIDDEN_T:
        t = {"n": 0, "harvested": 0, "advances": 0, "funding_prints": 0, "capped": 0,
             "reasons": {}, "kinds": {}}
        b = written_book(arm)
        bad += exit_findings(b, arm, t)
        tl[arm] = t
        parts.append(f"{arm} {t['n']}")
    sc = tl["scored"]
    for kd in EXIT_KINDS_T:
        if sc["kinds"].get(kd, 0) < MIN_EXIT_KIND_T:
            bad.append(f"EXIT-CARDINALITY scored: {kd} walked {sc['kinds'].get(kd, 0)} < "
                       f"{MIN_EXIT_KIND_T}")
    for kd in EXIT_KINDS_T:
        ex = sc.get("examples", {}).get(kd)
        if ex:
            say(f"      hand-walked {ex}")
    tot = sum(t["n"] for t in tl.values())
    return (not bad), (f"every campaign of the six WRITTEN ridden-arm regbooks ({', '.join(parts)}; "
                       f"{tot} in all) re-ridden by the engine (BK.brk_campaigns, v6 card, ribbon "
                       f"None) AND walked by this file's own ride + accounting on raw bars and raw "
                       f"funding: exit_close_ms, exit_reason, gross_r, fee_r, funding_r, net_r "
                       f"(and exit bar, exit_px, harvested, trail advances) equal at 0.000e+00 on "
                       f"every one; scored book walked: exits {dict(sorted(sc['reasons'].items()))}, "
                       f"{sc['harvested']} harvested, {sc['advances']} trail advances, "
                       f"{sc['funding_prints']} funding prints priced, {sc['capped']} at the D12 "
                       f"cap; kinds {dict((k, sc['kinds'].get(k, 0)) for k in EXIT_KINDS_T)} "
                       f"(>= {MIN_EXIT_KIND_T} each)"
                       + (f"; findings {bad[:3]}" if bad else ""))


# ═══════════════════════════════════════════════════════════════ F-BLIND
def blind_findings(src: str) -> list[str]:
    out = []
    tree = ast.parse(src)
    fns = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    for name in DECISION_FUNCS_T:
        fn = fns.get(name)
        if fn is None:
            out.append(f"BLIND {name}: the decision function is absent")
            continue
        for n in ast.walk(fn):
            if isinstance(n, (ast.Import, ast.ImportFrom)):
                out.append(f"BLIND {name} line {n.lineno}: an import inside a decision function")
            elif isinstance(n, ast.Name) and n.id in RANGE_NAMES_T:
                out.append(f"BLIND {name} line {n.lineno}: names the range layer ({n.id})")
            elif isinstance(n, ast.Attribute) and n.attr in LEAK_ATTRS_T:
                out.append(f"BLIND {name} line {n.lineno}: reads .{n.attr}")
    if tuple(getattr(T, "DECISION_FUNCS", ())) != DECISION_FUNCS_T:
        out.append(f"BLIND the module's DECISION_FUNCS {getattr(T, 'DECISION_FUNCS', None)} != "
                   f"typed {DECISION_FUNCS_T}")
    out += [f"BLIND {x}" for x in E.hook_escapes(src)]
    return out


def _src() -> str:
    return (ROOT / T.SOURCE_SCRIPT).read_text(encoding="utf-8")


def blind_break():
    s = _src()
    a1 = s.replace('    anchor, _, H = SOURCES[source]\n    rows = scan_rows(fx, source)',
                   '    anchor, _, H = SOURCES[source]\n    fx = N.range_facts(lf.sym, "4h")\n'
                   '    rows = scan_rows(fx, source)', 1)
    a2 = s.replace('    permit = permit_of(tide)\n    legs, disp, inwin = [], [], []',
                   '    permit = permit_of(tide)\n    _leak = cands[0].top if cands else None\n'
                   '    legs, disp, inwin = [], [], []', 1)
    a3 = s.replace('    return BK.brk_campaigns(lf, legs, CARD, ROLES, lane,',
                   '    from tierc11_nest import events  # noqa\n'
                   '    return BK.brk_campaigns(lf, legs, CARD, ROLES, lane,', 1)
    a4 = s.replace("import dataclasses\n", "import dataclasses\nimport subprocess\n", 1)
    for x in (a1, a2, a3, a4):
        if x == s:
            return True, "a source plant did not apply (FIXTURE DEFECT)"
    return plants([
        ("N.range_facts called inside candidates()", "names the range layer",
         lambda: blind_findings(a1)),
        ("a .top read inside dispose()", "reads .top", lambda: blind_findings(a2)),
        ("an import of tierc11_nest inside ride()", "an import inside a decision function",
         lambda: blind_findings(a3)),
        ("`import subprocess` in the runner", "HOOK-ESCAPE", lambda: blind_findings(a4)),
    ])


def blind_real():
    bad = blind_findings(_src())
    imps = sorted(x for x in E.static_imports(_src()) if "tierc10" in x or "nest" in x
                  or "rangefinder" in x)
    return (not bad), (f"the {len(DECISION_FUNCS_T)} typed decision functions "
                       f"{list(DECISION_FUNCS_T)} name no range object, read no .top/.bottom/"
                       f".n_deviations and import nothing; E.hook_escapes(runner) == []; the "
                       f"runner's range imports {imps} (a RUNNER may import tierc11_nest, L-F.2)"
                       + (f"; findings {bad[:3]}" if bad else ""))


# ═══════════════════════════════════════════════════════════════ F-GRID
def stage_tables() -> dict:
    return {f[:-8]: pd.read_parquet(str(OUT / f)) for f in STAGE_FILES_T if f.endswith(".parquet")}


def all_books() -> dict:
    return {a: written_book(a) for a in ARMS_T}


def _stats(b: pd.DataFrame) -> tuple:
    return int(len(b)), (fsum(b["net_r"]) if len(b) else 0.0)


def reg_brk() -> dict:
    return next(r for r in json.loads(REGS_PATH_T.read_text(encoding="utf-8"))["registrations"]
                if r["registration"] == "P-BRK-4H")


def grid_findings(tabs: dict, books: dict, md: str) -> list[str]:
    out = []
    for name, dec in DECLARED_T.items():
        w = tabs[name]
        ok, lines = TP.grid_whole(dec, w, "cell", require_cols=tuple(COLLAR_T), label=name)
        out += [f"GRID-WHOLE {x}" for x in lines if x.startswith("[BAD]")]
    for name, w in tabs.items():
        for k, v in COLLAR_T.items():
            if k not in w.columns or not bool((w[k] == v).all()):
                out.append(f"GRID-COLLAR {name}: column {k} is not {v!r} on every row")
        cols_v = [c for c in w.columns if "verdict" in str(c).lower()]
        if cols_v:
            out.append(f"GRID-VERDICT {name}: column(s) {cols_v}")
        for c in w.columns:
            if w[c].dtype == object:
                hit = [x for x in w[c].dropna().astype(str).unique() if VERDICT_RX.search(x)]
                if hit:
                    out.append(f"GRID-VERDICT {name}.{c}: {hit[:2]}")
    # numbers re-derived from the regbooks, this file's own grouping
    for a in ARMS_T:
        r = tabs["T_BRK_ARMS"].set_index("cell").loc[a] if a in set(
            tabs["T_BRK_ARMS"]["cell"]) else None
        if r is not None and (int(r["n"]), float(r["sum_net_r"])) != _stats(books[a]):
            out.append(f"GRID-NUM T_BRK_ARMS {a}: ({r['n']}, {r['sum_net_r']}) vs regbook "
                       f"{_stats(books[a])}")
    for name, col, fn in (("T_BRK_ASSET_GRID", "symbol", lambda b, v: b[b["symbol"] == v]),
                          ("T_BRK_ERA_GRID", "era", lambda b, v: b[b["era"] == v]),
                          ("T_BRK_EXIT_GRID", "exit_reason", lambda b, v: b[b["exit_reason"] == v]),
                          ("T_BRK_DIR_GRID", "side",
                           lambda b, v: b[b["direction"] == (1 if v == "long" else -1)])):
        for r in tabs[name].itertuples(index=False):
            got = (int(r.n), float(r.sum_net_r))
            want = _stats(fn(books[r.arm], getattr(r, col)))
            if got != want:
                out.append(f"GRID-NUM {name} {r.cell}: {got} vs regbook {want}")
    for r in tabs["T_BRK_TALLY"].itertuples(index=False):
        b = books[r.arm]
        disp = (r.n_out_of_window + r.n_out_of_tape + r.n_no_atr + r.n_tide + r.n_no_stop
                + r.n_position_open + r.n_entered)
        if int(r.n_trades) != int((b["symbol"] == r.symbol).sum()) or disp != r.n_candidates \
                or r.n_candidates != r.n_hold or r.n_entered != r.n_trades \
                or r.n_hold + r.n_failed + r.n_truncated != r.n_rows_evaluated:
            out.append(f"GRID-NUM T_BRK_TALLY {r.cell}: the tally does not add up")
    hz = tabs["T_BRK_HAZARD"].set_index("cell")
    for cell, (n_, net_) in HAZARD_T.items():
        if cell not in hz.index or round(float(hz.loc[cell, "net"]), 3) != net_ \
                or (n_ is not None and int(hz.loc[cell, "n"]) != n_):
            out.append(f"GRID-HAZARD {cell}: the grid row is not the registration's typed "
                       f"figure (n {n_}, NET {net_:+.3f})")
    ins = tabs["T_BRK_INSAMPLE"].set_index("cell")
    sb = books["scored"]
    for f_ in (True, False):
        for e in ("tuning", "holdout"):
            c = f"scored|in_sample={f_}|{e}"
            want = _stats(sb[(sb["scale_in_sample"] == f_) & (sb["era"] == e)])
            if c in ins.index and (int(ins.loc[c, "n"]), float(ins.loc[c, "sum_net_r"])) != want:
                out.append(f"GRID-NUM T_BRK_INSAMPLE {c}: vs regbook {want}")
    for a in ("tierE__holdout", "tierE__frozen3"):
        c = f"{a}|beside"
        if c in ins.index and (int(ins.loc[c, "n"]), float(ins.loc[c, "sum_net_r"])) != _stats(books[a]):
            out.append(f"GRID-NUM T_BRK_INSAMPLE {c}: vs regbook {_stats(books[a])}")
    for a in RIDDEN_T:                  # the disclosure: holdout rows acting on a pre-cut death
        c, b = f"{a}|holdout|death_close<=cut", books[a]
        want = _stats(b[(b["entry_close_ms"] > ERA_CUT_T) & (b["die_close_ms"] <= ERA_CUT_T)])
        if c in ins.index and (int(ins.loc[c, "n"]), float(ins.loc[c, "sum_net_r"])) != want:
            out.append(f"GRID-NUM T_BRK_INSAMPLE {c}: {(int(ins.loc[c, 'n']), float(ins.loc[c, 'sum_net_r']))} "
                       f"vs regbook {want}")
    # row_kind, typed: the scored arm's rows are the registered book's reference rows
    for name, w in tabs.items():
        if "row_kind" not in w.columns:
            out.append(f"GRID-ROWKIND {name}: no row_kind column")
            continue
        if name in ROW_KIND_TABLE_T:
            want_k = np.full(len(w), ROW_KIND_TABLE_T[name], dtype=object)
        else:
            want_k = np.where(w["arm"].to_numpy(object) == "scored", ROW_KIND_REG_T, ROW_KIND_E_T)
        bad_k = int((w["row_kind"].to_numpy(object) != want_k).sum())
        if bad_k:
            out.append(f"GRID-ROWKIND {name}: {bad_k} row(s) carry a row_kind that is not the "
                       f"typed one (scored -> {ROW_KIND_REG_T!r}, other arms -> {ROW_KIND_E_T!r})")
    reg = reg_brk()
    for k in ("selection_hazard", "scale_in_sample"):
        if reg["operative_spec"][k] not in md:
            out.append(f"GRID-MD the report does not print the registration's {k} verbatim")
    if reg["text_of_record"] not in md:
        out.append("GRID-MD the report does not print the text of record verbatim")
    for c in DECLARED_T["T_BRK_ASSET_GRID"]:          # printed in 5a AND in the tally (6)
        a, s = c.split("|")
        if len(re.findall(rf"^\| {re.escape(a)} \| {re.escape(s)} \|", md, flags=re.M)) < 2:
            out.append(f"GRID-MD the report lacks the grid or tally row for {c}")
    out += report_rows_findings(tabs, books, md)
    return out


def _ms(x: str) -> int:
    return int(pd.Timestamp(x).value // 1_000_000)


def report_rows_findings(tabs: dict, books: dict, md: str) -> list[str]:
    """EVERY ROW WHOLE: §11 prints every registered-book row; Appendix A every
    candidate; Appendix B every evaluated retest; Appendix C every Tier-E regbook
    row — each row found by its key, the tags consecutive, no row twice."""
    out = []
    ca, sc = tabs["T_BRK_CANDIDATES"], tabs["T_BRK_SCAN"]
    specs = (
        ("§11 registered book", r"^\| (\d+) \| ([A-Z0-9_]+) \| (\d{4}-\d\d-\d\dT[0-9:]+Z) \|",
         lambda m: ("scored", m.group(2), _ms(m.group(3))),
         {("scored", str(x), int(y)) for x, y in zip(books["scored"]["symbol"],
                                                     books["scored"]["entry_close_ms"])},
         len(books["scored"])),
        ("Appendix A", r"^\| A\.(\d+) \| ([^|]+?) \| ([^|]+?) \| (-?\d+) \| (-?\d+) \|",
         lambda m: (m.group(2), m.group(3), int(m.group(4)), int(m.group(5))),
         {(str(a), str(s_), int(d), int(t)) for a, s_, d, t in
          zip(ca["arm"], ca["symbol"], ca["die_i"], ca["touch_i"])}, len(ca)),
        ("Appendix B", r"^\| B\.(\d+) \| ([^|]+?) \| ([^|]+?) \| (-?\d+) \| (-?\d+) \|",
         lambda m: (m.group(2), m.group(3), int(m.group(4)), int(m.group(5))),
         {(str(a), str(s_), int(d), int(q)) for a, s_, d, q in
          zip(sc["arm"], sc["symbol"], sc["die_i"], sc["seq"])}, len(sc)),
        ("Appendix C", r"^\| C\.(\d+) \| ([^|]+?) \| ([^|]+?) \| (\d{4}-\d\d-\d\dT[0-9:]+Z) \|",
         lambda m: (m.group(2), m.group(3), _ms(m.group(4))),
         {(a, str(x), int(y)) for a in ARMS_T if a != "scored"
          for x, y in zip(books[a]["symbol"], books[a]["entry_close_ms"])},
         sum(len(books[a]) for a in ARMS_T if a != "scored")),
    )
    for lab, rx, key, want, n_want in specs:
        ms = list(re.finditer(rx, md, flags=re.M))
        got = [key(m) for m in ms]
        tags = [int(m.group(1)) for m in ms]
        if len(got) != n_want or set(got) != want or len(set(got)) != len(got) \
                or tags != list(range(1, len(tags) + 1)):
            miss = sorted(want - set(got), key=str)[:2]
            out.append(f"GRID-MD {lab}: the report prints {len(got)} row(s) ({len(set(got))} "
                       f"distinct) for the {n_want} of the table; missing e.g. {miss}")
    return out


def grid_break():
    tabs, books = stage_tables(), all_books()
    md = (OUT / "STAGE_T_BRK.md").read_text(encoding="utf-8")

    def bent(name, fn):
        t2 = dict(tabs)
        t2[name] = fn(tabs[name].copy())
        return grid_findings(t2, books, md)

    return plants([
        ("a zero-n cell dropped (scored|in_sample=True|holdout)", "GRID-WHOLE",
         lambda: bent("T_BRK_INSAMPLE", lambda d: d[d["cell"] != "scored|in_sample=True|holdout"])),
        ("an asset cell duplicated", "GRID-WHOLE",
         lambda: bent("T_BRK_ASSET_GRID", lambda d: pd.concat([d, d.iloc[[3]]], ignore_index=True))),
        ("the collar removed from the era grid", "GRID-COLLAR",
         lambda: bent("T_BRK_ERA_GRID", lambda d: d.drop(columns=["selection_not_a_result"]))),
        ("a 'verdict' column reading SUPPORTED", "GRID-VERDICT",
         lambda: bent("T_BRK_ARMS", lambda d: d.assign(verdict="SUPPORTED"))),
        ("a cell's n bent +1", "GRID-NUM",
         lambda: bent("T_BRK_EXIT_GRID", lambda d: d.assign(n=d["n"] + (d.index == 2)))),
        ("the hazard's CLASSIC5 holdout NET bent to +0.690", "GRID-HAZARD",
         lambda: bent("T_BRK_HAZARD", lambda d: d.assign(net=np.where(
             d["cell"] == "POOLED:CLASSIC5|holdout", 0.69, d["net"])))),
        ("an in-sample cell's ΣR bent", "GRID-NUM",
         lambda: bent("T_BRK_INSAMPLE", lambda d: d.assign(sum_net_r=d["sum_net_r"]
                                                           + 1e-9 * (d.index == 0)))),
        ("the SCALE-IN-SAMPLE text dropped from the report", "GRID-MD",
         lambda: grid_findings(tabs, books, md.replace("> scale_in_sample (registration text)",
                                                       "> (dropped)", 1).replace(
             reg_brk()["operative_spec"]["scale_in_sample"], "", 1))),
        ("a report row dropped", "GRID-MD",
         lambda: grid_findings(tabs, books, re.sub(r"^\| tierE__frozen3 \| SOLUSDT \|.*\n", "",
                                                   md, flags=re.M))),
        ("the scored arm's T_BRK_ARMS row labelled a Tier-E arm", "GRID-ROWKIND",
         lambda: bent("T_BRK_ARMS", lambda d: d.assign(row_kind="Tier-E arm"))),
        ("an Appendix A row (a candidate) dropped from the report", "GRID-MD Appendix A",
         lambda: grid_findings(tabs, books, re.sub(r"^\| A\.17 \|.*\n", "", md, count=1,
                                                   flags=re.M))),
        ("an Appendix C row (a Tier-E campaign) dropped from the report", "GRID-MD Appendix C",
         lambda: grid_findings(tabs, books, re.sub(r"^\| C\.5 \|.*\n", "", md, count=1,
                                                   flags=re.M))),
    ])


def grid_real():
    tabs, books = stage_tables(), all_books()
    md = (OUT / "STAGE_T_BRK.md").read_text(encoding="utf-8")
    bad = grid_findings(tabs, books, md)
    sizes = {k: len(v) for k, v in DECLARED_T.items()}
    return (not bad), (f"{len(DECLARED_T)} grids whole against the typed cells {sizes}; the "
                       f"typed collar on every row of all {len(tabs)} stage tables; the "
                       f"hazard rows == the registration's typed figures (CLASSIC5 +0.681 n 236 / "
                       f"+0.706 n 88; UNSEEN12 +0.064 / +0.272); the report prints the text of "
                       f"record, selection_hazard and scale_in_sample verbatim; no verdict "
                       f"word or 'verdict' column; every grid cell's n and ΣR re-derived from "
                       f"the regbooks exactly (the {len(RIDDEN_T)} holdout-on-a-pre-cut-death "
                       f"disclosure cells included); the typed row_kind on every row (scored -> "
                       f"'{ROW_KIND_REG_T}'); the tallies add up; the report prints every arm × "
                       f"asset cell, every registered-book row (§11, {len(books['scored'])}), every "
                       f"candidate (App. A, {len(tabs['T_BRK_CANDIDATES'])}), every evaluated retest "
                       f"(App. B, {len(tabs['T_BRK_SCAN'])}) and every Tier-E regbook row (App. C, "
                       f"{sum(len(books[a]) for a in ARMS_T if a != 'scored')})"
                       + (f"; findings {bad[:3]}" if bad else ""))


# ═══════════════════════════════════════════════════════════════ F-KEY
def canon_csv_sha(df: pd.DataFrame) -> str:
    """This file's own canonical CSV (the interface's law, re-implemented)."""
    d = df.sort_values(["symbol", "entry_close_ms"], kind="mergesort")
    lines = [",".join(REQ_ORDER_T)]
    for rec in d[list(REQ_ORDER_T)].to_dict("records"):
        vals = []
        for c in REQ_ORDER_T:
            v = rec[c]
            if REQUIRED_T[c] == "float64":
                vals.append(repr(float(v)))
            elif REQUIRED_T[c] in ("int64", "int8"):
                vals.append(str(int(v)))
            else:
                vals.append(str(v))
        lines.append(",".join(vals))
    return sha_bytes(("\n".join(lines) + "\n").encode("utf-8"))


def fee_slip() -> dict:
    fs = json.loads((E.OUT / "data" / "fee_schedule.json").read_text(encoding="utf-8"))
    out = {}
    for a in fs["assets"]:
        tier = a["charter_slippage_tier"]
        out[a["stem"]] = (tier, SLIP_TIER_BPS_T[tier], float(a["charter_slippage_bps_per_side"]),
                          float(a["taker_bps_side_used"]))
    return out


def key_findings(books: dict, sides: dict, status: dict, tabs: dict, man: dict) -> list[str]:
    out = []
    slip = fee_slip()
    for s, (tier, typed_bps, filed_bps, taker) in slip.items():
        if typed_bps != filed_bps or taker != TAKER_T:
            out.append(f"KEY-HAIRCUT fee schedule {s}: tier {tier} typed {typed_bps} bps, filed "
                       f"{filed_bps}; taker {taker}")
    for a in ARMS_T:
        b, sc = books[a], sides[a]
        miss = [c for c in REQUIRED_T if c not in b.columns]
        if miss:
            out.append(f"KEY-COLS {a}: missing {miss}")
            continue
        for c, dt in REQUIRED_T.items():
            if str(b[c].dtype) != dt:
                out.append(f"KEY-DTYPE {a}.{c}: {b[c].dtype} != {dt}")
        if b[list(REQUIRED_T)].isna().any().any():
            out.append(f"KEY-NULL {a}: a null in a required column")
        dup = int(b.duplicated(subset=BOOK_KEY_T).sum())
        if dup:
            out.append(f"KEY-DUP {a}: {dup} duplicated (symbol, entry_ms)")
        want_keys = set(SIDECAR_KEYS_T) | ({"tier", "selection_not_a_result", "gates"}
                                            if a != "scored" else set())
        if not want_keys <= set(sc):
            out.append(f"KEY-SIDECAR {a}: missing keys {sorted(want_keys - set(sc))}")
        exp = {"registration": "P-BRK-4H", "arm": a, "kind": "scored" if a == "scored" else "tierE",
               "ruler": "vs_zero", "panel": list(PANEL_T[ARM_PANEL_T[a]]),
               "era_scope": ARM_ERA_T[a], "n": int(len(b)),
               "source_script": "scripts/tierc11_stage_t_brk.py"}
        for k, v in exp.items():
            if sc.get(k) != v:
                out.append(f"KEY-SIDECAR {a}.{k}: {sc.get(k)!r} != {v!r}")
        if sc.get("sum_net_r") != fsum(b["net_r"]):
            out.append(f"KEY-SIDECAR {a}.sum_net_r {sc.get('sum_net_r')!r} != {fsum(b['net_r'])!r}")
        if sc.get("book_sha256") != canon_csv_sha(b):
            out.append(f"KEY-SHA {a}: sidecar {str(sc.get('book_sha256'))[:16]}… != this file's "
                       f"canonical CSV {canon_csv_sha(b)[:16]}…")
        if a != "scored":
            for k, v in COLLAR_T.items():
                if sc.get(k) != v or k not in b.columns or not bool((b[k] == v).all()):
                    out.append(f"KEY-COLLAR {a}: {k} is not {v!r} on the sidecar and every row")
        era = np.where(b["entry_close_ms"].to_numpy(np.int64) <= ERA_CUT_T, "tuning", "holdout")
        if not np.array_equal(era, b["era"].to_numpy(str)):
            out.append(f"KEY-ERA {a}: {int((era != b['era'].to_numpy(str)).sum())} row(s) not by "
                       f"the entry close")
        if ARM_ERA_T[a] != "full" and set(b["era"]) != {ARM_ERA_T[a]}:
            out.append(f"KEY-SLICE {a}: eras {sorted(set(b['era']))}")
        if (b["entry_close_ms"] - b["entry_ms"] != MS4H).any() or (b["exit_close_ms"] % MS4H).any():
            out.append(f"KEY-STAMP {a}: entry_close_ms - entry_ms != 4h or an off-grid exit")
        net_law = (b["gross_r"].to_numpy(float) - b["fee_r"].to_numpy(float)
                   - b["funding_r"].to_numpy(float))
        off = np.flatnonzero(b["net_r"].to_numpy(float) != net_law)
        if len(off):
            r0 = b.iloc[int(off[0])]
            out.append(f"KEY-NET {a}: {len(off)} row(s) where net_r != gross_r - fee_r - funding_r "
                       f"EXACTLY (e.g. {r0['symbol']} {iso(int(r0['entry_ms']))}: net "
                       f"{float(r0['net_r'])!r} vs {float(net_law[int(off[0])])!r})")
        for r in b.itertuples(index=False):
            want_h = float(r.net_r) - float(r.fee_r) * (slip[r.symbol][1] / TAKER_T)
            if float(r.haircut_net_r) != want_h:
                out.append(f"KEY-HAIRCUT {a} {r.symbol} {iso(r.entry_ms)}: {r.haircut_net_r!r} != "
                           f"{want_h!r} (AM-7, tier {slip[r.symbol][0]})")
                break
        if "as_of_last_closed_4h" not in b.columns or \
                not bool((b["as_of_last_closed_4h"] == PIN_ISO_T).all()):
            out.append(f"KEY-ASOF {a}: as_of_last_closed_4h is not {PIN_ISO_T} on every row")
    sc_b = books["scored"]
    for a in ("tierE__tuning", "tierE__holdout"):
        e = ARM_ERA_T[a]
        cut = sc_b[sc_b["era"] == e]
        if canon_csv_sha(cut) != canon_csv_sha(books[a]):
            out.append(f"KEY-SLICE {a}: not the scored book's {e} rows")
    st_want = {"registration": "P-BRK-4H", "status": "BUILT", "arms": list(ARMS_T)}
    for k, v in st_want.items():
        if status.get(k) != v:
            out.append(f"KEY-STATUS {k}: {status.get(k)!r} != {v!r}")
    if not status.get("reason"):
        out.append("KEY-STATUS reason: empty")
    for name, key in TABLE_KEYS_T.items():
        w = tabs[name]
        if int(w.duplicated(subset=key).sum()) or w[key].isna().any().any():
            out.append(f"KEY-DUP stage table {name}: key {key} duplicated or null")
        if "as_of_last_closed_4h" not in w.columns or w["as_of_last_closed_4h"].isna().any():
            out.append(f"KEY-ASOF stage table {name}")
    cs = man.get("content_sha", {})
    for a in ARMS_T:
        if cs.get(f"regbooks/P-BRK-4H/{a}.parquet") != TB._content_sha(books[a]):
            out.append(f"KEY-MANIFEST regbooks/P-BRK-4H/{a}.parquet content sha")
    for name in TABLE_KEYS_T:
        if cs.get(f"stage_t_brk/{name}.parquet") != TB._content_sha(tabs[name]):
            out.append(f"KEY-MANIFEST stage_t_brk/{name}.parquet content sha")
    return out


def straddle_findings() -> list[str]:
    """THE MODULE'S WRITER on the two typed bars either side of the era cut: a typed
    synthetic long leg (stop = entry - 1.0 ATR) at each bar, ridden by T.ride and
    written by T.trade_rows exactly as a real campaign is; its era must be the
    typed era by the CLOSE [L-1.3] and its stamps the typed open / close."""
    out = []
    sym = "BTCUSDT"
    lf = BK.frame_l(sym, "4h")
    arm = _arm("scored")
    fees = E.fees()
    for om, cm, want in STRADDLE_T:
        ti = int(np.searchsorted(lf.open_ms, om))
        if ti >= lf.n or int(lf.open_ms[ti]) != om:
            out.append(f"KEY-ERA-STRADDLE {sym}: no 4h bar opens at {iso(om)}")
            continue
        a_ = float(lf.atr[ti])
        leg = BK.Leg(direction=1, entry_i=ti, stop_px=float(lf.c[ti]) - a_, r_dist=a_,
                     touch_i=ti - 3, die_i=ti - 10)
        tr = T.ride(lf, [leg], 0, lf.n - 1, T.LANE)
        info = {(ti, 1, ti - 10): {"anchor": "tap89", "scale_mult": float("nan"),
                                   "pick_window": "synthetic", "scale_in_sample": False,
                                   "stability_changed": None, "die_i": ti - 10, "rid": -1,
                                   "seq": 0, "touch_i": ti - 3, "extreme": float("nan"),
                                   "rail_binding": True, "tide": 0, "tide_prev": 0}}
        row = T.trade_rows(tr, lf, arm, info, fees)
        if len(row) != 1:
            out.append(f"KEY-ERA-STRADDLE {sym} {iso(om)}: the writer returned {len(row)} rows")
            continue
        r = row.iloc[0]
        if (int(r["entry_ms"]), int(r["entry_close_ms"])) != (om, cm):
            out.append(f"KEY-ERA-STRADDLE {sym}: stamps ({int(r['entry_ms'])}, "
                       f"{int(r['entry_close_ms'])}) != typed ({om}, {cm})")
        if str(r["era"]) != want:
            out.append(f"KEY-ERA-STRADDLE {sym} entry bar open {iso(om)} close {iso(cm)}: the "
                       f"module's writer stamps era {str(r['era'])!r}; by the CLOSE (cut "
                       f"{ERA_CUT_T}) it is {want!r}")
    return out


def key_inputs() -> tuple:
    books = all_books()
    sides = {a: json.loads((REG_OUT / f"{a}.json").read_text(encoding="utf-8")) for a in ARMS_T}
    status = json.loads((REG_OUT / "STATUS.json").read_text(encoding="utf-8"))
    man = json.loads((OUT / "build_manifest.json").read_text(encoding="utf-8"))
    return books, sides, status, stage_tables(), man


def key_break():
    books, sides, status, tabs, man = key_inputs()

    def with_book(a, fn):
        b2 = dict(books)
        b2[a] = fn(books[a].copy())
        return key_findings(b2, sides, status, tabs, man)

    def with_side(a, k, v):
        s2 = copy.deepcopy(sides)
        s2[a][k] = v
        return key_findings(books, s2, status, tabs, man)

    def btc_haircut(d):
        m = d["symbol"] == "BTCUSDT"
        d.loc[m, "haircut_net_r"] = d.loc[m, "net_r"] - d.loc[m, "fee_r"] * (5.0 / 5.0)
        return d

    def era_flip(d):
        d.loc[d.index[0], "era"] = "holdout" if d.loc[d.index[0], "era"] == "tuning" else "tuning"
        return d

    def null_net(d):
        d["net_r"] = d["net_r"].astype(float)
        d.loc[d.index[min(4, len(d) - 1)], "net_r"] = np.nan
        return d

    def fund_sign(d):
        d["net_r"] = d["gross_r"] - d["fee_r"] + d["funding_r"]
        return d

    def fee_half(d):
        d["fee_r"] = d["fee_r"] * 0.5
        return d

    era_of0 = E.era_of

    def era_by_open(ms):
        return era_of0(int(ms) - MS4H)

    def man_bent():
        m2 = copy.deepcopy(man)
        m2["content_sha"]["stage_t_brk/T_BRK_ERA_GRID.parquet"] = "0" * 64
        return key_findings(books, sides, status, tabs, m2)

    return plants([
        ("a duplicated row", "KEY-DUP",
         lambda: with_book("scored", lambda d: pd.concat([d, d.iloc[[min(9, len(d) - 1)]]],
                                                         ignore_index=True))),
        ("a nulled net_r", "KEY-NULL", lambda: with_book("tierE__frozen3", null_net)),
        ("direction written as float", "KEY-DTYPE",
         lambda: with_book("scored", lambda d: d.assign(direction=d["direction"].astype(float)))),
        ("a bent sidecar book_sha256", "KEY-SHA", lambda: with_side("tierE__panel17",
                                                                    "book_sha256", "0" * 64)),
        ("sidecar n + 1", "KEY-SIDECAR", lambda: with_side("scored", "n", int(sides["scored"]["n"]) + 1)),
        ("BTC's haircut at 5 bps (tier A is 2)", "KEY-HAIRCUT",
         lambda: with_book("scored", btc_haircut)),
        ("a dropped 'lane' column", "KEY-COLS",
         lambda: with_book("tierE__memline_first_hold", lambda d: d.drop(columns=["lane"]))),
        ("one era flipped", "KEY-ERA", lambda: with_book("tierE__oneshot_first_touch", era_flip)),
        ("STATUS.json status 'CLOSED_BY_PRECONDITION'", "KEY-STATUS",
         lambda: key_findings(books, sides, dict(status, status="CLOSED_BY_PRECONDITION"), tabs,
                              man)),
        ("a bent manifest content sha", "KEY-MANIFEST", man_bent),
        ("net_r written as gross - fee + funding (tierE__panel17 copy)", "KEY-NET",
         lambda: with_book("tierE__panel17", fund_sign)),
        ("fee_r halved (scored copy)", "KEY-NET", lambda: with_book("scored", fee_half)),
        ("the writer's era read at the bar OPEN (E.era_of on entry_close - 4h)",
         "KEY-ERA-STRADDLE", under(E, "era_of", era_by_open, straddle_findings)),
    ])


def key_real():
    books, sides, status, tabs, man = key_inputs()
    bad = key_findings(books, sides, status, tabs, man)
    bad += straddle_findings()
    ns = ", ".join(f"{a} {len(books[a])}" for a in ARMS_T)
    return (not bad), (f"8 regbooks ({ns}): the 16 typed required columns at their typed dtypes, "
                       f"no null, unique (symbol, entry_ms); sidecars carry the typed keys / kind "
                       f"/ ruler / panel / era_scope, n, ΣR (fsum) and a book_sha256 equal to this "
                       f"file's own canonical CSV; tier-E collars on sidecar and rows; era by the "
                       f"entry close; the slices ARE the scored book's era cuts; haircut_net_r == "
                       f"AM-7 on every row; net_r == gross_r - fee_r - funding_r EXACTLY on every "
                       f"row; the module's writer stamps the straddle bar (open "
                       f"{iso(STRADDLE_T[0][0])}, close {iso(STRADDLE_T[0][1])}) 'holdout' and the "
                       f"bar before 'tuning'; STATUS.json typed; 11 stage tables keyed and "
                       f"stamped; every manifest content sha == the table read back"
                       + (f"; findings {bad[:3]}" if bad else ""))


# ═══════════════════════════════════════════════════════════════ F-DET
def _files(root: Path) -> dict:
    out = {}
    for sub, names in (("stage_t_brk", STAGE_FILES_T), ("regbooks/P-BRK-4H", REGBOOK_FILES_T)):
        d = root / sub
        if d.exists():
            for p in sorted(d.iterdir()):
                if p.is_file() and not p.name.startswith("FIXTURES_"):
                    out[f"{sub}/{p.name}"] = p.read_bytes()
    return out


TYPED_SET = sorted([f"stage_t_brk/{x}" for x in STAGE_FILES_T]
                   + [f"regbooks/P-BRK-4H/{x}" for x in REGBOOK_FILES_T])


def det_findings(a: tuple, b: tuple, canon: dict) -> list[str]:
    out = []
    for lab, (rc, _) in (("seed 1", a), (f"seed {SEED}", b)):
        if rc != 0:
            out.append(f"{lab} exit {rc}")
    for lab, x in (("seed 1", a[1]), (f"seed {SEED}", b[1]), ("canonical", canon)):
        if sorted(x) != TYPED_SET:
            out.append(f"{lab}: file set {len(x)} != typed {len(TYPED_SET)} "
                       f"({sorted(set(x) ^ set(TYPED_SET))[:3]})")
    for lab, x, y in ((f"seed 1 vs seed {SEED}", a[1], b[1]), ("seed 1 vs canonical", a[1], canon)):
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
    return RUN_ROOT / T.DET_NAME


def det_build(d: Path, seed: int, hashorder: bool = False) -> tuple[int, dict]:
    if d.exists():
        shutil.rmtree(d)
    env = dict(_env(), PYTHONHASHSEED=str(seed))
    if not hashorder:
        cmd = [PY, "-B", str(ROOT / T.SOURCE_SCRIPT), f"--out-root={d}"]
    else:                                   # SABOTAGE twin: a set-order line appended
        code = (f"import sys\nsys.dont_write_bytecode = True\n"
                f"sys.path.insert(0, {str(ROOT)!r})\n"
                f"sys.path.insert(0, {str(ROOT / 'scripts')!r})\n"
                f"from pathlib import Path\nimport tierc11_stage_t_brk as T\n"
                f"d = Path({str(d)!r})\nT.build(d)\n"
                f"p = d / T.STAGE_DIR / T.REPORT\n"
                f"p.write_text(p.read_text() + 'set order: ' + ','.join(set(T.PANEL17)) + '\\n')\n")
        cmd = [PY, "-B", "-c", code]
    r = subprocess.run(cmd, env=env, capture_output=True, text=True, cwd=str(ROOT), timeout=1800)
    if r.returncode != 0:
        clock(f"det build {d.name} exit {r.returncode}: {r.stderr[-400:]}")
    return r.returncode, (_files(d) if d.exists() else {})


def _canon() -> dict:
    return _files(E.OUT)


def det_break():
    canon = _canon()
    bent = dict(canon)
    md = bytearray(bent["stage_t_brk/STAGE_T_BRK.md"])
    md[len(md) // 2] ^= 0x01
    bent["stage_t_brk/STAGE_T_BRK.md"] = bytes(md)

    def float_moved():
        d = pd.read_parquet(io.BytesIO(canon["regbooks/P-BRK-4H/scored.parquet"]))
        d.loc[d.index[0], "net_r"] = float(d["net_r"].iloc[0]) + 1e-6
        buf = io.BytesIO()
        d.to_parquet(buf, index=False)
        c2 = dict(canon)
        c2["regbooks/P-BRK-4H/scored.parquet"] = buf.getvalue()
        return det_findings((0, c2), (0, c2), canon)

    def hashorder():
        o = {s: det_build(det_dir() / f"hashorder_{s}", s, hashorder=True) for s in DET_SEEDS}
        a, b = o[DET_SEEDS[0]], o[DET_SEEDS[1]]
        return [x for x in det_findings(a, b, a[1]) if x.startswith(f"seed 1 vs seed {SEED}")]

    return plants([
        ("one byte bent in a copy of STAGE_T_BRK.md", "STAGE_T_BRK.md bytes differ",
         lambda: det_findings((0, canon), (0, bent), canon)),
        ("one net_r moved 1e-6 in a regbook parquet copy", "scored.parquet content sha",
         float_moved),
        ("a hash-order-dependent line (set iteration) under the two seeds",
         f"seed 1 vs seed {SEED}: stage_t_brk/STAGE_T_BRK.md bytes differ", hashorder),
    ])


def det_real():
    canon = _canon()
    o = {s: det_build(det_dir() / f"seed_{s}", s) for s in DET_SEEDS}
    a, b = o[DET_SEEDS[0]], o[DET_SEEDS[1]]
    bad = det_findings(a, b, canon)
    man = json.loads(canon.get("stage_t_brk/build_manifest.json", b"{}"))
    sc = man.get("arms", {}).get("scored", {})
    return (not bad), (f"exit {a[0]}/{b[0]}; file set == typed {len(TYPED_SET)} files in both "
                       f"builds and in the record; every file byte-identical seed 1 == seed "
                       f"{SEED} == canonical, every parquet content sha equal: {not bad}; scored "
                       f"book sha {str(sc.get('book_sha256', '?'))[:16]}…"
                       + (f"; findings {bad[:4]}" if bad else ""))


FIXTURES = (
    ("F-BRK-HOLD", "the first retest that HOLDS on tap-89, hand-walked on raw bars with this "
     "file's own EMA89 / ATR14 [L-R.6(a), L-T.1]",
     "on any CLASSIC5 asset (calibrated and frozen 3.0) the module's tap-89 scan rows differ "
     "from the hand walk (window min(die + 400, next die - 1, n - 1); touch = band met with "
     "the prior close beyond it; failed = a close through by 1.0 ATR over touch..touch + 3; "
     "first hold ends the scan), the module's candidates are not the hand holds (entry touch "
     "+ 3, the death's direction, extreme over touch..entry), or fewer than 3 holds / 1 "
     "failed / 1 hold-after-a-failed-touch are hand-verified per scale",
     hold_break, hold_real),
    ("F-BRK-RIDE", "ride_leg_l(ribbon=None) through the module's BRK path IS v6's "
     "_ride_leg9 — exact zero on every v6 campaign [L-T.1 'v6 management']",
     "any of the 200 CLASSIC5 v6 campaigns re-entered through T.window + T.ride with v6's "
     "own entry and stop differs from v6 by ANY amount on the 12 CTRL_COLS, on exit_reason, "
     "entry_i, exit_i, harvested, harvest_i or bars_held, or the count differs",
     ride_break, ride_real),
    ("F-BRK-TIDE", "the tide is read at the ENTRY bar's own close on the 4h frame, both "
     "clauses [L-T.1 'tide aligned at the entry bar's close']",
     "on any real candidate of any ridden arm that reaches the permission test, or on the "
     "planted flip-in / flip-out / clause candidates, the module's admit/refuse disagrees "
     "with this file's tide (EMA89 > EMA316 AND close > EMA316 for a long; mirror) at the "
     "entry bar",
     tide_break, tide_real),
    ("F-BRK-ENTRY", "every written campaign enters at a scan hold's known_at close, in the "
     "death's direction, one position per asset, and the book is the whole greedy walk "
     "[L-T.1]",
     "a written ridden-arm regbook holds a campaign whose entry is not a hold row's known_at "
     "close of its own scan, whose direction is not the row's and the death's, whose "
     "entry_px is not the raw close; two campaigns of one asset overlap; or the book is not "
     "exactly the greedy one-position walk over the in-window, tide-aligned holds",
     entry_break, entry_real),
    ("F-BRK-EXIT", "every written campaign's exit and economics ARE the v6 ride and the "
     "accounting — the engine's re-ride and this file's own hand ride, exact [L-T.1 'v6 "
     "management'; L-1.1; the regbook interface's net law]",
     "any campaign of a written ridden-arm regbook differs by ANY amount from the engine's "
     "re-ride of its written entry and stop (BK.brk_campaigns, v6 card, ribbon None) or from "
     "this file's hand ride + accounting on raw bars and raw funding (stop -> bell 12/89 -> "
     "bell 89/316 -> 50% harvest at the 89/316 near edge -> strict (2,2) pivot trail; 5 bps a "
     "side every fill; interval-sum funding, D12 cap 1R) on exit_close_ms, exit_reason, "
     "gross_r, fee_r, funding_r, net_r (and exit bar, exit_px, harvested, advances); or fewer "
     "than 3 of each of stop-without-advance / bell-after-harvest / stop-after-advance are "
     "hand-walked in the scored book",
     exit_break, exit_real),
    ("F-BLIND", "the runner's decision functions are range-blind; no hook escape [L-F.2, AM-2]",
     "a typed decision function names N / tierc11_nest / C / ST / NL, reads .top / .bottom / "
     ".n_deviations or imports anything, the module's DECISION_FUNCS is not the typed list, "
     "or E.hook_escapes finds I/O the audit hook cannot see in the runner",
     blind_break, blind_real),
    ("F-GRID", "every Tier-E grid WHOLE, collared, verdict-free, and re-derived from the "
     "regbooks [LAWS: every grid whole; L-1.4 collars]",
     "a written grid is not whole against the typed declared cells (TP.grid_whole), a row "
     "lacks the typed collar, a verdict word or 'verdict' column appears, a cell's n / ΣR "
     "differs from this file's re-derivation from the regbooks (disclosure cells included), a "
     "row's row_kind is not the typed one (scored -> 'registered book (reference)'), a tally "
     "does not add up, or the report omits a declared arm × asset row, a registered-book row "
     "(§11), a candidate (App. A), an evaluated retest (App. B) or a Tier-E regbook row "
     "(App. C)",
     grid_break, grid_real),
    ("F-KEY", "the regbook interface: columns, dtypes, keys, sidecars, the canonical sha, "
     "eras, slices, AM-7, STATUS, stage keys, manifest",
     "a regbook lacks a typed required column / dtype, holds a null in one or a duplicated "
     "(symbol, entry_ms); a sidecar's keys / kind / ruler / panel / era_scope / n / ΣR / "
     "book_sha256 (this file's canonical CSV) disagree; a tier-E arm lacks its collar; an era "
     "is not by the entry close; a slice is not the scored book's era cut; haircut_net_r is "
     "off AM-7; the as-of stamp is off the pin; STATUS.json is not typed; a stage-table key "
     "is duplicated; a manifest content sha is not the table's; net_r is not EXACTLY gross_r "
     "- fee_r - funding_r; or the module's writer stamps the bar straddling the cut (open "
     "2024-06-30T20:00Z, close 2024-07-01T00:00Z) anything but 'holdout' or the bar before "
     "anything but 'tuning'",
     key_break, key_real),
    ("F-DET", "two subprocess builds under different hash seeds, one set of bytes [L-F.1]",
     "the PYTHONHASHSEED 1 and 20260924 builds differ from each other or from the canonical "
     "files (stage_t_brk/ + regbooks/P-BRK-4H/) in the file set, any byte or any parquet "
     "content sha, or either exits nonzero",
     det_break, det_real),
)


def file_transcript(out: Path, body: bytes, refile: bool) -> list[str]:
    """NEVER CLOBBER the transcript of record."""
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
    say("TIER-C11 STAGE T-brk FIXTURES — scripts/tierc11_stage_t_brk.py (P-BRK-4H and its "
        "Tier-E arms) — break leg first, RED or void")
    say("=" * 78)
    say(f"seed {SEED} · substrate {TC11_SNAP.name} · pin {PIN} · registration P-BRK-4H")
    for ln in T.READINGS:
        say(ln)
    for fid, title, fails_if, b, r in FIXTURES:
        if not pick or any(q in fid.lower() for q in pick):
            t1 = time.time()
            prove(fid, title, fails_if, b, r)
            clock(f"{fid} {time.time() - t1:.1f}s")
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
