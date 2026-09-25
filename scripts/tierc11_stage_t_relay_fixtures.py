#!/usr/bin/env python
"""TIER-C11 · STAGE T-relay + THE FORWARD LEDGER — F-RELAY · F-RELAY-MISS · F-FWD ·
F-RELAY-INSTANTS · F-KEY · F-GRID · F-DET.  The fixtures of scripts/tierc11_stage_t_relay.py (P-RELAY-1,
L-T.2 / L-T.3 / L-W.0) and scripts/tierc11_forward_ledger.py (L-T.6).

TWO LEGS PER FIXTURE, the BREAK leg first, and it must go RED or the fixture is VOID
— a guard nobody has seen fail is a guard nobody has seen [the prove() law of
scripts/tierc10_rf_fixtures.py / tierc11_books_fixtures.py].  A break leg is a set
of PLANTS judged one at a time; a plant counts as CAUGHT only if a finding NAMES THE
INTENDED DETECTOR (its expected substring).  A plant that crashes is a FIXTURE
DEFECT, never a catch.  A plant is a corrupted COPY (a book, a table, a ledger) or
a MUTATION of the module under trial restored in `finally`; no artifact of record
moves.  The referees are TYPED HERE (a second object): the pin, the opening, the
EMA pairs, the tide / d / pivot / rail laws, the disposition codes, the regbook
schema, the charter slippage tiers, the forward ledger's expected continuation and
OPEN rows.  Windows, 1h crosses, mismatch bars and structural stops are RE-DERIVED
here from the RAW snapshot parquet files (plain-loop EMA / ATR / pivots) — never
through the module's code.

  F-RELAY       FAILS IF any relay of the scored regbook of record (or a rebuild)
                closes at or after its window's v6 4h trigger close (own EMA12/26),
                at or after its counter-12/89 or 89/316-against close, not after
                its arm close, or after the pin; its 1h bar is not an own with-trend
                EMA9/12 cross, or is not the FIRST in the armed interval; its entry
                instant / price is not the own resolution (1h close; a 4h close; the
                parent's close on an own L-W.0 mismatch bar); its stop / R is not
                the own struct stop (strict (5,5) pivot, 0.5 ATR offset, 1.0 ATR
                rail) as of the last CLOSED 4h bar; a window holds two relays; or
                an asset holds two positions at once.  >= 3 relays are hand-walked
                from the raw 1h/4h bars: the arm, the cross, the stop at the last
                closed 4h bar, and the entry bar's close slot (stop / +1R on the
                post-entry children, BELL, HARVEST armed per close[J-1], TRAIL).
                THE LATE TWIN (tierE__late_relay, SR-6) is judged by the same law
                with the trigger bound removed: every late relay after its arm close,
                before its counter 12/89 / 89/316-against close, the FIRST own cross
                in that interval, own price / stop / R, one per window and one
                position per asset; the in-process rebuild == its regbook of record.
                SABOTAGE: a planted post-trigger relay (copy); [mutants] the trigger
                bound dropped; the 1h pair 12/26; the stop read as of J (look-ahead);
                the SECOND cross taken; a late relay moved onto its counter 12/89
                close (copy).
  F-RELAY-MISS  FAILS IF the windows table is not exactly this file's own window
                set (every card arming: own 4h 12/89 cross, tide, d >= 0.75), a
                window is listed twice or carries a code outside the typed set, the
                own disposition (relayed / trigger first (lag 0 split) / closed
                unrelayed (counter 12/89 | 89/316 against) / open at the as-of /
                refused: moved onto a bound, position open, no stop) differs, the
                RELAYED windows are not 1:1 the relay book, a lag-0 window is not a
                miss, or what v6 did in a window is not the v6 book's.  EVERY window
                row's bound columns (trigger / counter 12/89 / 89/316-against close,
                lag, the earliest bound and its tied kinds) and entry columns (first
                cross, resolved entry instant / kind / moved, the relay's 4h bar, net
                R and exit reason) are this file's own; the LATE columns are the own
                late derivation (trigger bound removed: bound, cross, entry,
                disposition, net R, after-trigger) and the late RELAYED windows are
                1:1 the late regbook; the v6 label of EVERY window is v6's slot law
                re-derived here (own trigger, (trigger bar, long first) order,
                position open while the base campaign's exit bar is not passed, then
                the own stop) at the typed label; tierE__miss_v6 is exactly the base
                campaigns whose own window is not RELAYED; on planted replay9 codes
                (position_open, stop-less) the module's label is the typed one.
                SABOTAGE (copies): a relayed window double-counted as a miss; a window
                dropped; a reason flipped; a relay counted twice in the book; a v6
                net R bent; the 89/316-against close nulled; the late columns copied
                from the record; a v6 label swapped; a relayed window's v6 campaign
                added to miss_v6; [mutants] the lag-0 split removed; the late twin
                built on the record bounds; the position-open label swapped.
  F-FWD         FAILS IF the ledger of record does not verify, does not open at
                2026-09-21T16:00Z, appends anything at the TC11 pin, or its OPEN /
                continuation lists are not the typed ones (v6: ETH long entered
                2026-09-18T08:00Z listed, not counted; 9/12: SOL long entered
                2026-09-24T16:00Z OPEN); a fresh refresh differs from it by a byte;
                or, on a planted opening refreshed at three pins (one chosen so a
                campaign is OPEN, then closed): a campaign is appended twice, an
                OPEN campaign is appended, a continuation is counted, the appended
                set / rows differ from the frozen books' own, the OPEN-then-closed
                campaign is not appended exactly at the pin that first sees it
                closed, a same-pin refresh changes a byte, or the chain breaks; a row
                planted at lag 6 / 7 / 15 / 16 / 17 and band B3 / B4 is not stamped
                by the typed P-WIN-1 cut (>= 16), shadow (7-15) and P-AGE-1 OLD (B4);
                an OPEN entry or a continuation still open at the pin is not marked
                to the pin (net_r_marked_to_pin, never net_r), or a closed one is —
                checked on the record, on the planted sequence and on a planted
                opening at the 9/12 SOL campaign's entry close (a continuation still
                open at the pin).  SABOTAGE: [mutants] OPEN treated as closed;
                continuations admitted; append-once removed; the P-WIN-1 cut read as
                > 16; the shadow read as 8-15; a planted re-ride changing an appended
                row (must HALT REFRESH-CHANGED); a planted same-pin refresh whose
                re-ride closes the OPEN campaign (must HALT: SAME pin); a tampered
                line and a deleted line (must FAIL the chain); an open continuation
                relabelled net_r (copy).
  F-RELAY-INSTANTS  FAILS IF, on ANY row of ANY of the six arms of record (the relay
                arms scored / late / tuning / holdout slices and the v6 arms base /
                miss_v6), the extra column harvest_close_ms [SR-9; L-R.5, AM-6 — the
                lanes pass] is absent, not Int64, set on a row that did not harvest or
                NA on one that did, or differs from THIS FILE'S hand harvest law on
                the raw 4h / 1h bars: the band edge max/min(own EMA89, EMA316); a
                1h relay's entry bar J armed per close[J-1] and touched on its
                POST-ENTRY 1h children only, then every later 4h bar j (a 4h-close
                or moved entry: from J+1 on a fresh state) armed once any close[j-1]
                sat outside the edge and touched on the whole bar; the first such bar
                strictly before the exit bar (the exit bar itself only at
                corridor_end) — its CLOSE is the instant (a close event); or a v6 row's
                instant differs from books/v6_campaigns.parquet's harvest_close_ms;
                or the in-process rebuild of the scored arm differs from its record
                on the column.  SABOTAGE: (copies) one harvest one 4h bar late; one
                harvest instant dropped (nulled on a harvested row); [mutant] the
                writer's harvest_close_of stamping the harvest bar's OPEN.
  F-KEY         FAILS IF a regbook parquet lacks a required column, carries the
                wrong dtype, a null in a required column, a duplicated (symbol,
                entry_close_ms) key (or (symbol, entry_ms) on scored / base); its
                sidecar lacks a typed key or its n / sum_net_r / book_sha256 (own
                canonical CSV) disagree with the parquet; era / haircut / lane differ
                from the typed laws; a Tier-E sidecar lacks the collar; STATUS.json
                is not the typed arms; a stage table fails TP.check_keys, lacks the
                collar or carries a verdict column.  SABOTAGE (copies): a duplicated
                row; a nulled net_r; direction as int64; the sidecar sum +1e-9; one
                float bent (sha); a Tier-E collar dropped; a verdict column; the
                haircut at the wrong tier.
  F-GRID        FAILS IF the disposition grid, the lead bins or the era slices are
                not WHOLE against the typed cells (TP.grid_whole), a NaN statistic
                has no nan_reason, or the disposition counts do not partition ALL;
                or a VALUE differs from this file's own: every grid cell's n windows /
                n lag 0 / relay n / relay ΣR / v6 entered n / v6 ΣR / v6 mean from the
                own record and late dispositions (the books' net R, the base book's
                v6 campaigns); every relay's lead_4h (own trigger bar − own entry bar
                J) and lead_1h ((own trigger close − own entry instant) / 1h), the
                lead values table and the typed lead bins; every era slice (n, ΣR,
                mean, Σ haircut at the typed tier, win %) from the regbooks by the
                own era law — at the writer's 6 dp.  SABOTAGE (copies): a cell
                dropped; an undeclared cell; a silent NaN; a verdict column; the
                collar removed; the partition broken; the 4h lead read from the arm
                bar; a lead value's count moved; the record relay ΣR x 1.01; a v6 ΣR
                bent 1e-6; an era slice's haircut ΣR bent 1e-6.
  F-DET         FAILS IF two subprocess builds of the runner and of the ledger
                (PYTHONHASHSEED 1, 20260924) differ from each other or from the
                files of record in the file set, any byte or any parquet content
                sha, or either exits nonzero.  SABOTAGE: one byte bent in a copy; a
                parquet float moved 1e-6; a hash-order-dependent line under the two
                seeds.
BANNED: self-comparison; one example where cardinality was possible; a tuned
magnitude bound standing in for an identity; a check whose claim is not the
design's claim.  FROZEN SUBSTRATE: HALTs unless NAIAD_CACHE_DIR is the TC11 snapshot
(tierc11_env's guard).  Seed 20260924.  The transcript carries no clock and no temp
path.  No registered rule's CI, p or verdict is computed or printed here.

Run:  export NAIAD_CACHE_DIR=$HOME/.cache/naiad/snapshots/tc11_20260925 PYTHONDONTWRITEBYTECODE=1
      ~/venvs/naiad/bin/python -B scripts/tierc11_forward_ledger.py --refresh --snapshot $NAIAD_CACHE_DIR
      ~/venvs/naiad/bin/python -B scripts/tierc11_stage_t_relay.py              # the build (embeds the ledger)
      ~/venvs/naiad/bin/python -B scripts/tierc11_stage_t_relay_fixtures.py \\
          [leg-substring ...] [--refile-transcript] [--root=DIR]
      --root=DIR redirects the transcript AND the F-DET twins; the files compared
      against are always the record.
Exit 0 = every leg GREEN, every break RED · 1 = a RED or VOID fixture, a transcript
finding, or a HALT.
"""
from __future__ import annotations

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
import tempfile
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
import tierc11_stage_t_relay as S                                    # noqa: E402  (guards first)
import tierc11_forward_ledger as F                                   # noqa: E402

import numpy as np                                                   # noqa: E402
import pandas as pd                                                  # noqa: E402

B, E, RD = S.B, S.E, S.RD
TP, T9, T8, TB = E.TP, E.T9, E.T8, E.TB
iso = TB.iso

# ── FIXTURE-TYPED LITERALS: the commission, a second object, never the module's ──
SNAP = Path.home() / ".cache" / "naiad" / "snapshots" / "tc11_20260925"
PIN = 1_790_294_400_000                  # 2026-09-25T00:00:00Z [L-0.1]
OPENING = 1_790_006_400_000              # 2026-09-21T16:00:00Z [L-T.6]
CORRIDOR_LO = 1_567_958_400_000          # 2019-09-08T16:00:00Z, the CLASSIC5 panel start
SEED = 20260924
DET_SEEDS = (1, SEED)
AS_OF_LINE = "as_of_last_closed_4h: 2026-09-25T00:00:00Z"
H1, H4 = 3_600_000, 14_400_000
CLASSIC5_TYPED = ("BTCUSDT", "ETHUSDT", "SOLUSDT", "NEARUSDT", "ZECUSDT")
RELAY_PAIR = (9, 12)                     # "ENTRY on the 1h 9/12 with-trend close"
WIN_PAIR, TRIG_PAIR, TIDE_PAIR = (12, 89), (12, 26), (89, 316)
WARM = 316                               # the estate's warm-up floor
D_MIN = 0.75                             # displacement |c - e89| / ATR at the arm bar
ATR_LEN = 14
PIV_L, PIV_R, PIV_LOOKBACK = 5, 5, 200   # the (5,5) structural pivot, 200-bar lookback
STOP_BUF_ATR, RAIL_ATR = 0.5, 1.0        # offset beyond the pivot; the 1.0 ATR rail
TRAIL_LR = (2, 2)
ANCHOR_KIND, ANCHOR_OFF, MIN_ADV_ATR = "pivot", 0.5, 0.05
REPR_TOL = 1e-9                          # L-W.0: 1e-9 x max(1, |a|, |b|)
ERA_CUT = 1_719_791_999_000              # L-1.3: tuning closes <= 2024-06-30T23:59:59Z
SLIP_TYPED = {"BTCUSDT": 2.0, "ETHUSDT": 2.0, "SOLUSDT": 5.0, "NEARUSDT": 5.0,
              "ZECUSDT": 5.0}            # charter tiers A 2 / B 5 (AM-7)
TAKER_TYPED = 5.0
# the corridor's L-W.0 mismatch bars (the ride builder's and verifier's list: 16)
MISMATCH_TYPED = {
    "BTCUSDT": ("2019-09-08T16:00:00Z", "2019-09-09T00:00:00Z", "2019-09-24T16:00:00Z",
                "2023-11-10T12:00:00Z", "2024-10-28T20:00:00Z"),
    "ETHUSDT": ("2019-11-27T04:00:00Z", "2019-12-11T16:00:00Z", "2023-11-10T12:00:00Z",
                "2024-10-28T20:00:00Z"),
    "SOLUSDT": ("2020-09-14T04:00:00Z", "2023-11-10T12:00:00Z", "2024-10-28T20:00:00Z"),
    "NEARUSDT": ("2023-11-10T12:00:00Z", "2024-10-28T20:00:00Z"),
    "ZECUSDT": ("2023-11-10T12:00:00Z", "2024-10-28T20:00:00Z"),
}
CODES_TYPED = ("RELAYED", "MISS_TRIGGER_FIRST_LAG0", "MISS_TRIGGER_FIRST",
               "MISS_CLOSED_COUNTER_12_89", "MISS_CLOSED_TIDE_AGAINST", "MISS_OPEN_AT_ASOF",
               "MISS_REFUSED_MOVED_ONTO_BOUND", "MISS_REFUSED_POSITION_OPEN",
               "MISS_REFUSED_NO_STOP")
REQUIRED_TYPED = {"symbol": "str", "entry_ms": "int64", "entry_close_ms": "int64",
                  "direction": "int8", "entry_px": "float64", "stop_px": "float64",
                  "r_dist": "float64", "exit_close_ms": "int64", "exit_reason": "str",
                  "net_r": "float64", "gross_r": "float64", "fee_r": "float64",
                  "funding_r": "float64", "haircut_net_r": "float64", "era": "str",
                  "lane": "str"}
REQ_ORDER = tuple(REQUIRED_TYPED)
SIDECAR_TYPED = ("registration", "arm", "kind", "ruler", "panel", "era_scope", "n",
                 "sum_net_r", "book_sha256", "description", "source_script")
ARMS_TYPED = {"scored": ("scored", "two_sample", "full", "relay"),
              "base": ("base", "two_sample", "full", "card"),
              "tierE__late_relay": ("tierE", "two_sample", "full", "relay"),
              "tierE__tuning_slice": ("tierE", "two_sample", "tuning", "relay"),
              "tierE__holdout_slice": ("tierE", "two_sample", "holdout", "relay"),
              "tierE__miss_v6": ("tierE", "vs_zero", "full", "card")}
COLLAR_TYPED = {"tier": "TIER-E", "selection_not_a_result": "a SELECTION, not a result",
                "gates": "nothing"}
VERDICT_COLUMNS = ("verdict", "verdict_of_record", "clears_bh_bar", "promotable",
                   "scored_in_family", "p_one_sided", "is_the_registered_cell", "supported")
AS_OF_TYPED = ("as_of_last_closed_4h", "as_of_panel_start", "as_of_span_days", "warranty",
               "as_of_lens", "as_of_last_closed_bar", "as_of_panel", "as_of_n_assets",
               "as_of_substrate")
STAGE_KEYS_TYPED = {"relay_windows": ["symbol", "arm_ms", "direction"],
                    "relay_disposition_grid": ["variant", "disposition"],
                    "relay_era_slices": ["arm", "era"],
                    "relay_lead_values": ["lead_kind", "lead_value"],
                    "relay_lead_bins": ["lead_kind", "bin"]}
LEAD_EDGES_TYPED = {"lead_4h_bars": (("0", 0, 0), ("1", 1, 1), ("2", 2, 2), ("3", 3, 3),
                                     ("4", 4, 4), ("5-9", 5, 9), ("10-19", 10, 19),
                                     (">=20", 20, None)),
                    "lead_1h_bars": (("1-3", 1, 3), ("4-7", 4, 7), ("8-15", 8, 15),
                                     ("16-31", 16, 31), ("32-63", 32, 63), (">=64", 64, None))}
LEAD_NA_TYPED = "no trigger (NA)"
LEAD_BINS_TYPED = {k: tuple(n for n, _, _ in v) + (LEAD_NA_TYPED,)
                   for k, v in LEAD_EDGES_TYPED.items()}
LEAD_COL_TYPED = {"lead_4h_bars": "lead_4h", "lead_1h_bars": "lead_1h"}
# what v6 did, by v6's own slot law (tierc9.replay9's reject codes) -> the typed label
V6_LABEL_TYPED = {"entered": "ENTERED", "position_open": "NOT ENTERED: position open",
                  "no_trigger": "NOT ENTERED: no trigger by the window close / as-of",
                  "no_stop": "NOT ENTERED: no structural stop / ATR"}
V6_REPLAY_CODE_TYPED = {"entered": "entered", "position_open": "position_open",
                        "no_trigger": "no_trigger", "": "no_stop"}   # replay9 reject -> own code
ENTRY_KIND_TYPED = {"1h": "1h", "4h-close": "4h-close", "moved": "parent-close"}  # (prefix)
P_WIN_1_SHADOW_TYPED = (7, 15)
STAMP_PLANT = ((6, "B3"), (7, "B4"), (15, "B3"), (16, "B4"), (17, "B2"))  # (lag, tide band)
FWD_CONT_PLANT_OPENING = "2026-09-24T20:00:00Z"   # the 9/12 SOL campaign's entry close
SNAP_PLANT = "/nonexistent/not_the_substrate"      # a fixed path: no temp dir in the transcript
ERA_CELLS_TYPED = tuple(f"{a}|{e}" for a in ("scored (relay)", "base (v6)", "tierE__late_relay")
                        for e in ("tuning", "holdout", "full"))
STAGE_FILES_TYPED = ("STAGE_T_RELAY.md", "build_manifest.json",
                     "relay_disposition_grid.parquet", "relay_era_slices.parquet",
                     "relay_lead_bins.parquet", "relay_lead_values.parquet",
                     "relay_windows.parquet")
REG_FILES_TYPED = ("STATUS.json",) + tuple(f"{a}.{x}" for a in ARMS_TYPED
                                          for x in ("json", "parquet"))
FWD_FILES_TYPED = ("FORWARD_LEDGER.jsonl", "FORWARD_LEDGER.md")
# L-T.6 at the TC11 pin, the task's expectation typed (verified, never assumed)
FWD_V6_CONTINUATIONS = (("ETHUSDT", "2026-09-18T08:00:00Z", 1),)
FWD_912_OPEN = (("SOLUSDT", "2026-09-24T16:00:00Z", 1),)
FWD_PLANT_OPENING = "2026-01-01T00:00:00Z"
P_WIN_1_TYPED, P_AGE_1_OLD_TYPED = 16, "B4"
TABLE_DP = 6                             # the lineage writer rounds Tier-E stage tables (TB.write_table)

OUT = S.OUT                              # research_outputs/tierc11/stage_t_relay
REGDIR = E.OUT / "regbooks" / S.REG_ID
FWD = F.OUT
RUN_ROOT = OUT
TRANSCRIPT = "FIXTURES_STAGE_T_RELAY.txt"
PY = sys.executable
LINES: list[str] = []
PASSED: list[str] = []
FAILED: list[str] = []
_TMP_RX = re.compile(r"(/private)?/(var/folders|tmp)/[^\s'\"]+")
# the process's own temp root too (TMPDIR may be anywhere), longest first, whole path token
_TMP_ROOTS = tuple(re.compile(re.escape(t) + r"[^\s'\"]*") for t in sorted(
    {str(Path(tempfile.gettempdir())), str(Path(tempfile.gettempdir()).resolve())},
    key=len, reverse=True) if len(t) > 1)


def scrub(s: str) -> str:
    """Every temp path token -> <tmp>, BEFORE any shortening (verifier m1)."""
    for rx in _TMP_ROOTS:
        s = rx.sub("<tmp>", s)
    return _TMP_RX.sub("<tmp>", s)


def say(line: str = "") -> None:            # deterministic -> transcript
    line = scrub(line)
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
    if isinstance(r_why, list):
        for ln in r_why[:-1]:
            say(f"    {ln}")
        r_why = r_why[-1]
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
            found = [str(e) if str(e).startswith("HALT") else f"HALT: {e}"]
        except Exception as e:
            crashed.append(scrub(f"{name} -> RAISED {type(e).__name__}: {e}"))
            continue
        found = [scrub(str(f)) for f in found]   # temp paths out BEFORE the cut (m1)
        if not found:
            passed.append(name)
        elif not any(want in str(f) for f in found):
            wrong.append(f"{name} -> {str(found[0])[:160]} (wanted {want!r})")
        else:
            hit = next(str(f) for f in found if want in str(f))
            i = hit.index(want)
            shown = hit[:170] if i + len(want) <= 170 else (hit[:50] + " … " + hit[i:i + 140])
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
    return dict(os.environ, NAIAD_CACHE_DIR=str(SNAP), PYTHONDONTWRITEBYTECODE="1")


def _ms(s: str) -> int:
    return int(pd.Timestamp(s).value // 1_000_000)


# ═══════════════════════════════════════ INDEPENDENT DERIVATIONS (this file's)
def ema(x: np.ndarray, n: int) -> np.ndarray:
    """A plain-loop EMA seeded at the first value (the engine's law, this file's code)."""
    a = 2.0 / (n + 1.0)
    out = np.empty(len(x))
    prev = float("nan")
    for i, v in enumerate(x):
        prev = float(v) if i == 0 else prev + a * (float(v) - prev)
        out[i] = prev
    return out


def atr(h: np.ndarray, l_: np.ndarray, c: np.ndarray, n: int = ATR_LEN) -> np.ndarray:
    """Wilder ATR, plain loop: TR[0] = h-l, then max of the three ranges; rma seeded."""
    out = np.empty(len(c))
    prev = float("nan")
    for i in range(len(c)):
        if i == 0:
            tr = float(h[0]) - float(l_[0])
        else:
            pc = float(c[i - 1])
            tr = max(float(h[i]) - float(l_[i]), max(abs(float(h[i]) - pc),
                                                      abs(float(l_[i]) - pc)))
        prev = tr if i == 0 else prev + (1.0 / n) * (tr - prev)
        out[i] = prev
    return out


def xup(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    out = np.zeros(len(a), dtype=bool)
    out[1:] = (a[1:] > b[1:]) & (a[:-1] <= b[:-1])
    return out


def xdn(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    out = np.zeros(len(a), dtype=bool)
    out[1:] = (a[1:] < b[1:]) & (a[:-1] >= b[:-1])
    return out


def pivots(x: np.ndarray, low: bool) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Strict (5,5) pivots, plain loop: (conf index = p + 5, value, pivot bar p)."""
    conf, val, bar = [], [], []
    n = len(x)
    for p in range(PIV_L, n - PIV_R):
        v = float(x[p])
        left, right = x[p - PIV_L:p], x[p + 1:p + 1 + PIV_R]
        ok = (v < float(left.min()) and v < float(right.min())) if low else \
            (v > float(left.max()) and v > float(right.max()))
        if ok:
            conf.append(p + PIV_R)
            val.append(v)
            bar.append(p)
    return np.array(conf, int), np.array(val, float), np.array(bar, int)


def same_px(a: float, b: float) -> bool:
    return abs(float(a) - float(b)) <= REPR_TOL * max(1.0, abs(float(a)), abs(float(b)))


_OWN: dict = {}


def raw(sym: str, tf: str) -> pd.DataFrame:
    """The snapshot's own kline file, bars CLOSED at the pin, ascending."""
    step = H1 if tf == "1h" else H4
    d = pd.read_parquet(str(SNAP / "klines" / f"{sym}_{tf}.parquet"))
    d = d.sort_values("open_time", kind="mergesort").reset_index(drop=True)
    return d[d["open_time"].to_numpy(np.int64) + step <= PIN].reset_index(drop=True)


def own(sym: str) -> dict:
    """This file's own 4h / 1h arrays, EMAs, crosses, ATR and pivots for one asset."""
    if sym in _OWN:
        return _OWN[sym]
    r4, r1 = raw(sym, "4h"), raw(sym, "1h")
    o4 = r4["open_time"].to_numpy(np.int64)
    c4, h4, l4 = (r4[k].to_numpy(float) for k in ("close", "high", "low"))
    o1 = r1["open_time"].to_numpy(np.int64)
    c1, h1, l1 = (r1[k].to_numpy(float) for k in ("close", "high", "low"))
    e = {n: ema(c4, n) for n in {WIN_PAIR[0], WIN_PAIR[1], TRIG_PAIR[1], TIDE_PAIR[1]}}
    X = {"o4": o4, "c4": c4, "h4": h4, "l4": l4, "atr": atr(h4, l4, c4),
         "e12": e[12], "e26": e[26], "e89": e[89], "e316": e[316],
         "o1": o1, "c1": c1, "h1": h1, "l1": l1, "close1": o1 + H1,
         "hi_i": len(c4) - 1,
         "lo_i": max(int(np.searchsorted(o4, CORRIDOR_LO, "left")), WARM)}
    X["wup"], X["wdn"] = xup(X["e12"], X["e89"]), xdn(X["e12"], X["e89"])
    X["tup"], X["tdn"] = xup(X["e12"], X["e26"]), xdn(X["e12"], X["e26"])
    X["bup"], X["bdn"] = xup(X["e89"], X["e316"]), xdn(X["e89"], X["e316"])
    r9, r12 = ema(c1, RELAY_PAIR[0]), ema(c1, RELAY_PAIR[1])
    X["r9"], X["r12"] = r9, r12
    X["rup"], X["rdn"] = xup(r9, r12), xdn(r9, r12)
    X["pl"], X["ph"] = pivots(l4, True), pivots(h4, False)
    _OWN[sym] = X
    return X


def own_windows(sym: str) -> list[dict]:
    """Every card arming of the asset, from this file's own arrays [L-T.2]."""
    X = own(sym)
    lo_i, hi_i, o4, c4 = X["lo_i"], X["hi_i"], X["o4"], X["c4"]
    out = []
    for d, opens, counter, trig, against in ((1, X["wup"], X["wdn"], X["tup"], X["bdn"]),
                                             (-1, X["wdn"], X["wup"], X["tdn"], X["bup"])):
        for i in np.flatnonzero(opens):
            i = int(i)
            if not (lo_i <= i <= hi_i):
                continue
            if d == 1:
                tide = X["e89"][i] > X["e316"][i] and c4[i] > X["e316"][i]
            else:
                tide = X["e89"][i] < X["e316"][i] and c4[i] < X["e316"][i]
            a_ = X["atr"][i]
            disp = abs(c4[i] - X["e89"][i]) / a_ if (np.isfinite(a_) and a_ > 0) else np.nan
            if not (tide and np.isfinite(disp) and disp >= D_MIN):
                continue
            lat = np.flatnonzero(counter[i + 1:hi_i + 1])
            we = int(i + 1 + lat[0]) if lat.size else None
            end = we if we is not None else hi_i + 1
            tg = np.flatnonzero(trig[i:end])
            ti = int(i + tg[0]) if tg.size else None
            ta = np.flatnonzero(against[i + 1:hi_i + 1])
            tai = int(i + 1 + ta[0]) if ta.size else None
            w = {"symbol": sym, "direction": d, "arm_i": i, "arm_ms": int(o4[i]),
                 "arm_close": int(o4[i]) + H4, "disp": float(disp),
                 "trigger_i": ti, "trigger_close": None if ti is None else int(o4[ti]) + H4,
                 "lag": None if ti is None else ti - i,
                 "window_close": None if we is None else int(o4[we]) + H4,
                 "against_close": None if tai is None else int(o4[tai]) + H4}
            out.append(w)
    return out


def own_bound_all(w: dict, late: bool = False) -> tuple[int | None, str]:
    """(earliest bound, every kind binding at it '+'-joined in the tie order trigger ->
    counter 12/89 -> 89/316-against; 'none' when unbounded) [L-T.2, SR-2].  `late`
    removes the trigger bound (the late twin, SR-6)."""
    cand = [(k, w[f]) for k, f in (("trigger", "trigger_close"),
                                   ("counter_12_89", "window_close"),
                                   ("tide_against", "against_close"))
            if w[f] is not None and not (late and k == "trigger")]
    if not cand:
        return None, "none"
    b = min(v for _, v in cand)
    return b, "+".join(k for k, v in cand if v == b)


def own_bound(w: dict, late: bool = False) -> tuple[int | None, str]:
    """(earliest bound, its first kind in the order trigger -> counter 12/89 -> 89/316)."""
    b, kinds = own_bound_all(w, late)
    return b, kinds.split("+")[0]


def own_first_cross(sym: str, d: int, after: int, before: int | None) -> int | None:
    X = own(sym)
    m = X["rup"] if d == 1 else X["rdn"]
    cl = X["close1"]
    sel = (cl > after) & (cl <= PIN) & m
    if before is not None:
        sel &= cl < before
    k = np.flatnonzero(sel)
    return int(k[0]) if k.size else None


def own_is_cross(sym: str, d: int, close_ms: int) -> bool:
    X = own(sym)
    k = int(np.searchsorted(X["close1"], int(close_ms)))
    return bool(k < len(X["close1"]) and int(X["close1"][k]) == int(close_ms)
                and (X["rup"] if d == 1 else X["rdn"])[k])


def own_mismatch(sym: str, J: int) -> bool:
    """L-W.0 by this file's law: the 4h bar J's native 1h children are 4 on the grid
    and reproduce its high, low and close to 1e-9 x max(1, |a|, |b|)."""
    X = own(sym)
    a = int(np.searchsorted(X["o1"], int(X["o4"][J]), "left"))
    b = int(np.searchsorted(X["o1"], int(X["o4"][J]) + H4, "left"))
    if b - a != 4 or not np.array_equal(X["o1"][a:b] - int(X["o4"][J]),
                                        np.array([0, H1, 2 * H1, 3 * H1], np.int64)):
        return True
    return not (same_px(X["h1"][a:b].max(), X["h4"][J]) and same_px(X["l1"][a:b].min(),
                                                                   X["l4"][J])
                and same_px(X["c1"][b - 1], X["c4"][J]))


def own_resolve(sym: str, close_ms: int, planted_mismatch: frozenset = frozenset()) -> dict:
    """The entry instant / price / as-of of a 1h close [L-T.2, L-W.0], this file's law
    (`planted_mismatch`: 4h indices a planted leg declares mismatch bars)."""
    X = own(sym)
    J = int(np.searchsorted(X["o4"], int(close_ms), "left")) - 1
    close_J = int(X["o4"][J]) + H4
    if int(close_ms) == close_J:
        return {"J": J, "kind": "4h-close", "t": close_J, "px": float(X["c4"][J]), "asof": J}
    if J in planted_mismatch or own_mismatch(sym, J):
        return {"J": J, "kind": "moved", "t": close_J, "px": float(X["c4"][J]), "asof": J}
    k = int(np.searchsorted(X["close1"], int(close_ms)))
    return {"J": J, "kind": "1h", "t": int(close_ms), "px": float(X["c1"][k]), "asof": J - 1,
            "k": k}


def own_stop(sym: str, asof: int, e: float, d: int) -> dict | None:
    """struct_stop_4h's law by this file's code: the nearest confirmed strict (5,5)
    pivot beyond entry with conf <= asof within 200 bars, 0.5 ATR beyond it, railed
    so R >= 1.0 ATR (ATR of the as-of bar)."""
    X = own(sym)
    a = float(X["atr"][asof])
    if not (np.isfinite(a) and a > 0):
        return None
    conf, val, bar = X["pl"] if d == 1 else X["ph"]
    el = (conf <= asof) & (asof - conf <= PIV_LOOKBACK) & ((val < e) if d == 1 else (val > e))
    if not el.any():
        return None
    idx = np.flatnonzero(el)
    k = int(idx[np.argmax(val[el])] if d == 1 else idx[np.argmin(val[el])])
    anchor = float(val[k])
    if d == 1:
        piv, rail = anchor - STOP_BUF_ATR * a, e - RAIL_ATR * a
        stop = min(piv, rail)
    else:
        piv, rail = anchor + STOP_BUF_ATR * a, e + RAIL_ATR * a
        stop = max(piv, rail)
    return {"stop": stop, "r": abs(e - stop), "atr": a, "anchor": anchor,
            "anchor_bar": int(bar[k]), "conf": int(conf[k]), "pivot_stop": piv,
            "rail_stop": rail}


def own_windows_all() -> dict:
    return {(w["symbol"], w["direction"], w["arm_ms"]): w
            for s in CLASSIC5_TYPED for w in own_windows(s)}


# ═══════════════════════════════════════════════════════════ THE MODULE'S BOOKS
_MEMO: dict = {}


def live() -> dict:
    """The in-process build the fixture judges beside the files of record."""
    if not _MEMO:
        R = S.compute()
        _MEMO.update({"R": R, "trades": {(t.symbol, int(getattr(t, "entry_close_ms"))): t
                                         for t in R["relay"]}})
    return _MEMO


def reg(arm: str) -> pd.DataFrame:
    return pd.read_parquet(str(REGDIR / f"{arm}.parquet"))


def side(arm: str) -> dict:
    return json.loads((REGDIR / f"{arm}.json").read_text(encoding="utf-8"))


def rebuilt_scored() -> pd.DataFrame:
    """The module's scored book rebuilt in-process (the path a MUTATION is judged on)."""
    lo, hi, _ = B.corridor()
    trades, _ = S.relay_book(lo, hi, late=False)
    return S.regbook_frame(trades, "relay")


# ════════════════════════════════════════════════════════════════════ F-RELAY
def relay_findings(book: pd.DataFrame, late: bool = False) -> list[str]:
    """Every relay of `book` (scored-regbook shaped) against this file's own windows,
    crosses, resolution and stops [L-T.2, L-T.3, L-W.0].  `late`: the late twin's law
    (SR-6) — the trigger bound removed, everything else the record's."""
    W = own_windows_all()
    out = []
    seen = {}
    last_exit: dict = {}
    for r in book.sort_values(["symbol", "entry_close_ms"], kind="mergesort").itertuples():
        sym, d, t_e = str(r.symbol), int(r.direction), int(r.entry_close_ms)
        lab = f"{sym} {d:+d} entry {iso(t_e)}"
        key = (sym, d, int(r.arm_ms))
        w = W.get(key)
        if w is None:
            out.append(f"RELAY-WINDOW {lab}: arm {iso(int(r.arm_ms))} is no own card arming")
            continue
        if key in seen:
            out.append(f"RELAY-WINDOW {lab}: a second relay in the window armed "
                       f"{iso(w['arm_ms'])} (first entered {iso(seen[key])})")
        seen[key] = t_e
        if not late and w["trigger_close"] is not None and t_e >= w["trigger_close"]:
            out.append(f"RELAY-AFTER-TRIGGER {lab}: not strictly before the window's v6 4h "
                       f"trigger close {iso(w['trigger_close'])}")
        if not t_e > w["arm_close"]:
            out.append(f"RELAY-BOUND {lab}: not after the arm close {iso(w['arm_close'])}")
        for f_, nm in (("window_close", "counter 12/89"), ("against_close", "89/316-against")):
            if w[f_] is not None and t_e >= w[f_]:
                out.append(f"RELAY-BOUND {lab}: not before the {nm} close {iso(w[f_])}")
        if t_e > PIN:
            out.append(f"RELAY-BOUND {lab}: after the pin")
        rc = int(r.cross_close_ms)
        if not own_is_cross(sym, d, rc):
            out.append(f"RELAY-CROSS {lab}: the 1h bar closing {iso(rc)} is no own with-trend "
                       f"EMA{RELAY_PAIR[0]}/{RELAY_PAIR[1]} cross")
        b, _ = own_bound(w, late)
        k1 = own_first_cross(sym, d, w["arm_close"], b)
        if k1 is None:
            out.append(f"RELAY-CROSS {lab}: no own qualifying cross in the armed interval")
        elif int(own(sym)["close1"][k1]) != rc:
            out.append(f"RELAY-NOT-FIRST {lab}: the book's cross {iso(rc)} is not the first "
                       f"own qualifying cross {iso(int(own(sym)['close1'][k1]))}")
        res = own_resolve(sym, rc)
        if t_e != res["t"]:
            out.append(f"RELAY-ENTRY {lab}: the own resolution of the cross {iso(rc)} is "
                       f"{res['kind']} at {iso(res['t'])}")
        if float(r.entry_px) != res["px"]:
            out.append(f"RELAY-PRICE {lab}: entry_px {r.entry_px!r} != own {res['px']!r}")
        st = own_stop(sym, res["asof"], res["px"], d)
        if st is None:
            out.append(f"RELAY-STOP {lab}: the own struct stop as of {iso(int(own(sym)['o4'][res['asof']]) + H4)} "
                       f"is None, yet the book entered")
        elif float(r.stop_px) != st["stop"] or float(r.r_dist) != st["r"]:
            out.append(f"RELAY-STOP {lab}: stop {r.stop_px!r} / R {r.r_dist!r} != own "
                       f"{st['stop']!r} / {st['r']!r} as of the last closed 4h bar "
                       f"{iso(int(own(sym)['o4'][res['asof']]) + H4)}")
        if sym in last_exit and t_e <= last_exit[sym]:
            out.append(f"RELAY-POSITION {lab}: entered while the previous relay on {sym} was "
                       f"open (exit {iso(last_exit[sym])})")
        last_exit[sym] = int(r.exit_close_ms)
    return out


def hand_walk(t, row) -> tuple[list[str], list[str]]:
    """One relay hand-walked from the raw bars: (lines to print, findings)."""
    sym, d = str(row.symbol), int(row.direction)
    X = own(sym)
    W = own_windows_all()[(sym, d, int(row.arm_ms))]
    i, lines, bad = W["arm_i"], [], []
    fast = X["wup"] if d == 1 else X["wdn"]
    lines.append(f"HAND {sym} {'long' if d == 1 else 'short'} — arm bar close {iso(W['arm_close'])}: "
                 f"own EMA12 {X['e12'][i - 1]:.6g}->{X['e12'][i]:.6g} vs EMA89 "
                 f"{X['e89'][i - 1]:.6g}->{X['e89'][i]:.6g} (cross {bool(fast[i])}); tide EMA89 "
                 f"{X['e89'][i]:.6g} vs EMA316 {X['e316'][i]:.6g}, close {X['c4'][i]:.6g}; d "
                 f"{W['disp']:.4f} >= {D_MIN}; trigger close "
                 f"{iso(W['trigger_close']) if W['trigger_close'] else 'none'} · window close "
                 f"{iso(W['window_close']) if W['window_close'] else 'open'}")
    rc = int(row.cross_close_ms)
    k = int(np.searchsorted(X["close1"], rc))
    lines.append(f"  1h cross closing {iso(rc)}: own EMA9 {X['r9'][k - 1]:.6g}->{X['r9'][k]:.6g} "
                 f"vs EMA12 {X['r12'][k - 1]:.6g}->{X['r12'][k]:.6g}; first after the arm close: "
                 f"{own_first_cross(sym, d, W['arm_close'], own_bound(W)[0]) == k}")
    res = own_resolve(sym, rc)
    st = own_stop(sym, res["asof"], res["px"], d)
    lines.append(f"  entry {res['kind']} at {iso(res['t'])} px {res['px']:.8g}; stop as of the last "
                 f"CLOSED 4h bar (close {iso(int(X['o4'][res['asof']]) + H4)}): ATR "
                 f"{st['atr']:.6g}, pivot {st['anchor']:.8g} (bar {iso(int(X['o4'][st['anchor_bar']]))}, "
                 f"confirmed {iso(int(X['o4'][st['conf']]) + H4)}), pivot stop {st['pivot_stop']:.8g}, "
                 f"rail {st['rail_stop']:.8g} -> stop {st['stop']:.8g} R {st['r']:.8g} · module "
                 f"{float(row.stop_px):.8g} / {float(row.r_dist):.8g}")
    if float(row.stop_px) != st["stop"] or float(row.r_dist) != st["r"]:
        bad.append(f"HAND {sym} {iso(res['t'])}: stop/R differ from the hand walk")
    J = res["J"]
    if res["kind"] != "1h":
        lines.append(f"  entry at J's close ({iso(int(X['o4'][J]) + H4)}): no post-entry child in J; "
                     f"the ride starts at J+1 (module entry_i {int(t.entry_i)}, first exit bar "
                     f">= J+1: {int(t.exit_i) >= J + 1})")
        if int(t.entry_i) != J or int(t.exit_i) < J + 1:
            bad.append(f"HAND {sym} {iso(res['t'])}: a 4h-close relay not ridden from J+1")
        return lines, bad
    e, stop, R = res["px"], st["stop"], st["r"]
    a1 = int(np.searchsorted(X["o1"], int(X["o4"][J]), "left"))
    kids = list(range(res["k"] + 1, a1 + 4))
    x_k = latch_k = None
    parts = []
    for kk in kids:
        hi_, lo_ = float(X["h1"][kk]), float(X["l1"][kk])
        stop_hit = (lo_ <= stop) if d == 1 else (hi_ >= stop)
        plus = ((hi_ - e) if d == 1 else (e - lo_)) / R >= 1.0
        parts.append(f"{iso(int(X['close1'][kk]))} H {hi_:.6g} L {lo_:.6g}"
                     f"{' STOP' if stop_hit else ''}{' +1R' if plus and not stop_hit else ''}")
        if stop_hit:
            x_k = kk
            break
        if latch_k is None and plus:
            latch_k = kk
    lines.append(f"  J = 4h bar closing {iso(int(X['o4'][J]) + H4)}; post-entry children: "
                 + (" · ".join(parts) if parts else "none (entry at child 3's close)"))
    if x_k is not None:
        ok = (int(t.exit_i) == J and str(t.exit_reason) == "stop"
              and int(getattr(t, "exit_close_ms")) == int(X["close1"][x_k]))
        lines.append(f"  close slot: stopped inside J at the child closing {iso(int(X['close1'][x_k]))} "
                     f"-> module exit {t.exit_reason} at {iso(int(getattr(t, 'exit_close_ms')))}: {ok}")
        if not ok:
            bad.append(f"HAND {sym} {iso(res['t'])}: stop inside J not the module's exit")
        return lines, bad
    bell_w = (X["wdn"] if d == 1 else X["wup"])[J]
    bell_t = (X["bdn"] if d == 1 else X["bup"])[J]
    edge_p = max(X["e89"][J - 1], X["e316"][J - 1]) if d == 1 else min(X["e89"][J - 1],
                                                                        X["e316"][J - 1])
    armed = (X["c4"][J - 1] > edge_p) if d == 1 else (X["c4"][J - 1] < edge_p)
    edge = max(X["e89"][J], X["e316"][J]) if d == 1 else min(X["e89"][J], X["e316"][J])
    post_ext = (min(float(X["l1"][kk]) for kk in kids) if d == 1
                else max(float(X["h1"][kk]) for kk in kids)) if kids else None
    touch = bool(armed and post_ext is not None
                 and ((post_ext <= edge) if d == 1 else (post_ext >= edge)))
    lines.append(f"  close slot at J: BELL (counter 12/89 {bool(bell_w)}, 89/316 against "
                 f"{bool(bell_t)}); HARVEST armed per close[J-1] {X['c4'][J - 1]:.6g} vs edge "
                 f"{edge_p:.6g}: {bool(armed)}, touched on the post-entry children (extreme "
                 f"{post_ext if post_ext is None else format(post_ext, '.6g')} vs edge "
                 f"{edge:.6g}): {touch}; +1R latch in J: "
                 f"{iso(int(X['close1'][latch_k])) if latch_k is not None else 'none'}; TRAIL "
                 f"armed {latch_k is not None}")
    if bell_w or bell_t:
        ok = int(t.exit_i) == J and str(t.exit_reason).startswith("bell")
        lines.append(f"  -> module belled at J: {ok}")
        if not ok:
            bad.append(f"HAND {sym} {iso(res['t'])}: bell at J not the module's")
        return lines, bad
    m_harv = t.harvest_i is not None and int(t.harvest_i) == J
    m_latch = getattr(t, "latch_1h_ms")
    want_latch = int(X["close1"][latch_k]) if latch_k is not None else None
    latch_ok = (m_latch == want_latch) if want_latch is not None else (
        m_latch is None or int(m_latch) > int(X["o4"][J]) + H4)
    trail_ok, trail_txt = True, "no trail at J (not latched)"
    if latch_k is not None:
        fr = T9.fractals(sym, *TRAIL_LR)
        adv, _ = T8.matched_step(fr, J, d, stop, float(X["c4"][J]), float(X["atr"][J]),
                                 T8.anchor_series(sym), ANCHOR_KIND, ANCHOR_OFF, X["o4"],
                                 min_advance_atr=MIN_ADV_ATR)
        madv = [a for a in t.advances if int(a.conf_i) == J]
        trail_ok = ((adv is None and not madv) or (adv is not None and len(madv) == 1
                                                     and float(madv[0].new_stop)
                                                     == float(adv.new_stop)))
        trail_txt = (f"trail at J (v6's matched_step on the hand stop): "
                     f"{'no advance' if adv is None else format(float(adv.new_stop), '.8g')}")
    elif any(int(a.conf_i) == J for a in t.advances):
        trail_ok = False
    lines.append(f"  -> module: harvest at J {m_harv} (hand {touch}); latch "
                 f"{iso(int(m_latch)) if m_latch is not None else 'none'} (hand "
                 f"{iso(want_latch) if want_latch else 'none in J'}); {trail_txt}; agree: "
                 f"{m_harv == touch and latch_ok and trail_ok}")
    if not (m_harv == touch and latch_ok and trail_ok):
        bad.append(f"HAND {sym} {iso(res['t'])}: close slot differs (harvest {m_harv}/{touch}, "
                   f"latch {latch_ok}, trail {trail_ok})")
    return lines, bad


def hand_pick(book: pd.DataFrame) -> list:
    """>= 3 relays, deterministically: the first 1h long, 1h short, 4h-close, a relay
    stopped inside J, and one latched inside J (when they exist)."""
    rows = list(book.sort_values(["symbol", "entry_close_ms"], kind="mergesort").itertuples())
    T = live()["trades"]
    picks, seen = [], set()

    def take(pred, label):
        for r in rows:
            k = (str(r.symbol), int(r.entry_close_ms))
            if k not in seen and pred(r, T[k]):
                seen.add(k)
                picks.append((label, r, T[k]))
                return

    take(lambda r, t: r.entry_kind == "1h" and int(r.direction) == 1
         and not (int(t.exit_i) == int(r.relay_J)), "1h long")
    take(lambda r, t: r.entry_kind == "1h" and int(r.direction) == -1
         and not (int(t.exit_i) == int(r.relay_J)), "1h short")
    take(lambda r, t: r.entry_kind == "4h-close", "4h-close")
    take(lambda r, t: r.entry_kind == "1h" and int(t.exit_i) == int(r.relay_J)
         and str(t.exit_reason) == "stop", "stopped inside J")
    take(lambda r, t: r.entry_kind == "1h" and getattr(t, "latch_1h_ms") is not None
         and int(getattr(t, "latch_1h_ms")) <= int(r.entry_ms) + H4,
         "latched inside J")
    return picks


def relay_break():
    rec = reg("scored")

    def planted():
        d = rec.copy()
        i = int(np.flatnonzero(d["trigger_close_ms"].notna().to_numpy())[0])
        d.loc[d.index[i], "entry_close_ms"] = int(d["trigger_close_ms"].iloc[i])
        return relay_findings(d)

    def late_bound():
        ob, oe = S.bound_of, RD.relay_entry

        def entry_no_trigger(sym, t, walk=None, trigger_close_ms=None):
            return oe(sym, t, walk=walk, trigger_close_ms=None)
        with mutated(S, "bound_of", lambda w, late: ob(w, True)), \
                mutated(RD, "relay_entry", entry_no_trigger):
            return relay_findings(rebuilt_scored())

    def pair_1226():
        with mutated(S, "relay_pair", lambda: (12, 26)):
            return relay_findings(rebuilt_scored())

    def asof_J():
        with mutated(S, "relay_asof", lambda re_: int(re_["J"])):
            return relay_findings(rebuilt_scored())

    def second_cross():
        orig = S.first_index

        def second(mask, close_ms, after_ms, before_ms, edge_ms):
            k = orig(mask, close_ms, after_ms, before_ms, edge_ms)
            if k is None:
                return None
            k2 = orig(mask, close_ms, int(close_ms[k]), before_ms, edge_ms)
            return k2 if k2 is not None else k
        with mutated(S, "first_index", second):
            return relay_findings(rebuilt_scored())

    def late_past_counter():
        d = reg("tierE__late_relay").copy()
        i = int(np.flatnonzero(d["window_close_ms"].notna().to_numpy())[0])
        d.loc[d.index[i], "entry_close_ms"] = int(d["window_close_ms"].iloc[i])
        return late_relay_findings(d)

    return plants([
        ("a planted post-trigger relay (a copy of the book, one entry moved onto its "
         "trigger close)", "RELAY-AFTER-TRIGGER", planted),
        ("[mutant] the trigger law dropped (bound_of without the trigger AND relay_entry "
         "handed no trigger: the late reading ridden as the record)", "RELAY-AFTER-TRIGGER",
         late_bound),
        ("[mutant] the 1h pair 12/26 in place of 9/12", "RELAY-CROSS", pair_1226),
        ("[mutant] the stop read as of J, the unclosed bar (look-ahead)", "RELAY-STOP",
         asof_J),
        ("[mutant] the SECOND qualifying cross taken", "RELAY-NOT-FIRST", second_cross),
        ("a late-twin relay moved onto its window's counter 12/89 close (copy of "
         "tierE__late_relay)", "LATE RELAY-BOUND", late_past_counter),
    ])


def late_relay_findings(book: pd.DataFrame) -> list[str]:
    """The late twin (SR-6) under this file's law, every finding prefixed LATE."""
    return [f"LATE {x}" for x in relay_findings(book, late=True)]


def relay_real():
    rec = reg("scored")
    lines = []
    L = live()
    got = S.book_sha256(S.regbook_frame(L["R"]["relay"], "relay"))
    same = got == side("scored")["book_sha256"] == S.book_sha256(rec)
    bad = relay_findings(rec)
    if not same:
        bad.append("RELAY-RECORD: the in-process rebuild is not the scored regbook of record")
    lrec = reg("tierE__late_relay")
    lgot = S.book_sha256(S.regbook_frame(L["R"]["late"], "relay"))
    lsame = lgot == side("tierE__late_relay")["book_sha256"] == S.book_sha256(lrec)
    lbad = late_relay_findings(lrec)
    if not lsame:
        lbad.append("LATE RELAY-RECORD: the in-process late rebuild is not tierE__late_relay "
                    "of record")
    picks = hand_pick(rec)
    hb = []
    for label, r, t in picks:
        ln, b = hand_walk(t, r)
        lines.append(f"[{label}]")
        lines += ln
        hb += b
    bad += hb
    if len(picks) < 3:
        bad.append(f"HAND: only {len(picks)} relays hand-walked (< 3)")
    trig = rec[rec["trigger_close_ms"].notna()]
    kinds = rec["entry_kind"].value_counts().to_dict()
    lat = lrec[lrec["trigger_close_ms"].notna()]
    n_after = int((lat["entry_close_ms"].to_numpy(np.int64)
                   >= lat["trigger_close_ms"].astype("int64").to_numpy(np.int64)).sum())
    lines.append(f"(c) EVERY relay of the late twin tierE__late_relay ({len(lrec)}; entry kinds "
                 f"{dict(sorted(lrec['entry_kind'].value_counts().to_dict().items()))}; "
                 f"{n_after} at/after their v6 4h trigger close) against this file's own "
                 f"windows with the trigger bound removed (SR-6): after its arm close, before "
                 f"its counter 12/89 / 89/316-against close and the pin, the FIRST own "
                 f"with-trend EMA9/12 cross of that interval, own price / stop / R, one per "
                 f"window, one position per asset: {not lbad}; late rebuild == record "
                 f"(book_sha256 {lgot[:16]}…): {lsame}" + (f"; findings {lbad[:3]}" if lbad else ""))
    lines.append(f"(a) EVERY relay of the scored regbook of record ({len(rec)}; entry kinds "
                 f"{dict(sorted(kinds.items()))}) against this file's own windows / crosses / "
                 f"resolution / stops: {len(trig)} relays in windows that triggered, each "
                 f"closes strictly before its v6 4h trigger close; every entry after its arm "
                 f"close and before its counter 12/89 / 89/316-against close and the pin; each "
                 f"the FIRST own with-trend EMA9/12 cross; price, stop and R the own values; one "
                 f"per window and one position per asset: {not bad}; rebuild == record "
                 f"(book_sha256 {got[:16]}…): {same}; (b) {len(picks)} relays hand-walked from "
                 f"the raw 1h/4h bars ({', '.join(p[0] for p in picks)})"
                 + (f"; findings {bad[:4]}" if bad else ""))
    return (not bad and not lbad), lines


# ═══════════════════════════════════════════════════════════════ F-RELAY-MISS
def own_asset_dispositions(sym: str, wins: list, exits: dict,
                           planted_mismatch: frozenset = frozenset(),
                           planted_nostop: frozenset = frozenset(),
                           late: bool = False) -> tuple[dict, list[str]]:
    """This file's disposition of every window of one asset [L-T.2, SR-2..SR-5]; the
    position law reads the book's own exit instants (the ride is the module's; the
    ORDER is judged here).  `planted_nostop` holds (asof, entry px) pairs a planted
    leg declares stop-less.  `late`: the late twin's law (the trigger bound removed)."""
    out, bad, cands = {}, [], []
    for w in wins:
        key = (sym, w["direction"], w["arm_ms"])
        b, kind = own_bound(w, late)
        k = own_first_cross(sym, w["direction"], w["arm_close"], b)
        if k is None:
            out[key] = ("MISS_OPEN_AT_ASOF" if b is None else
                        ("MISS_TRIGGER_FIRST_LAG0" if w["lag"] == 0 else "MISS_TRIGGER_FIRST")
                        if kind == "trigger" else
                        "MISS_CLOSED_COUNTER_12_89" if kind == "counter_12_89" else
                        "MISS_CLOSED_TIDE_AGAINST")
            continue
        res = own_resolve(sym, int(own(sym)["close1"][k]), planted_mismatch)
        if b is not None and res["t"] >= b:
            out[key] = "MISS_REFUSED_MOVED_ONTO_BOUND"
            continue
        cands.append((res["t"], w["arm_i"], key, res, w))
    cands.sort(key=lambda c: (c[0], c[1]))
    open_until = None
    for t_e, _, key, res, w in cands:
        if open_until is not None and t_e <= open_until:
            out[key] = "MISS_REFUSED_POSITION_OPEN"
            continue
        if (res["asof"], res["px"]) in planted_nostop or \
                own_stop(sym, res["asof"], res["px"], w["direction"]) is None:
            out[key] = "MISS_REFUSED_NO_STOP"
            continue
        out[key] = "RELAYED"
        x = exits.get((sym, t_e))
        if x is None:
            bad.append(f"MISS-COUNT {sym} {iso(t_e)}: an own relay the book does not hold")
            continue
        open_until = x
    return out, bad


def own_dispositions(book: pd.DataFrame, late: bool = False) -> tuple[dict, list[str]]:
    exits = {(str(r.symbol), int(r.entry_close_ms)): int(r.exit_close_ms)
             for r in book.itertuples()}
    out, bad = {}, []
    for sym in CLASSIC5_TYPED:
        o, b = own_asset_dispositions(sym, own_windows(sym), exits, late=late)
        out.update(o)
        bad += b
    return out, bad


def _nz(v):
    """A table cell as a plain value: None for NA / NaN, numpy scalars unwrapped."""
    if v is None or v is pd.NA:
        return None
    if isinstance(v, (float, np.floating)) and v != v:
        return None
    if isinstance(v, np.integer):
        return int(v)
    if isinstance(v, np.floating):
        return float(v)
    if isinstance(v, np.bool_):
        return bool(v)
    return v


def _r6(x):
    """The stage writer's law on a float statistic: rounded to the table's 6 dp."""
    return None if x is None else float(np.round(float(x), TABLE_DP))


def own_rows(book: pd.DataFrame, late: bool) -> tuple[dict, list[str]]:
    """EVERY window's own row for one variant (record or late): the disposition, the
    earliest bound and its tied kinds, the first qualifying cross, the resolved entry
    instant / kind, and — for a RELAYED window — the relay's 4h bar J, the book's net R
    and exit reason (the ride is the module's, keyed by the OWN entry instant), and
    the lead over the own trigger (4h bars: trigger bar − J; 1h bars: (trigger close −
    entry instant) / 1h) and whether the entry is at/after the trigger close."""
    disp, bad = own_dispositions(book, late)
    W = own_windows_all()
    bk = {(str(r.symbol), int(r.entry_close_ms)): r for r in book.itertuples()}
    out = {}
    for key in sorted(disp):
        code, w = disp[key], W[key]
        sym, d = key[0], key[1]
        b, kinds = own_bound_all(w, late)
        k = own_first_cross(sym, d, w["arm_close"], b)
        row = {"disposition": code, "bound_ms": b, "bound_kind": kinds, "cross_close_ms": None,
               "entry_close_ms": None, "entry_kind": None, "moved": None,
               "relay_entry_ms": None, "relay_net_r": None, "relay_exit_reason": None,
               "lead_1h": None, "lead_4h": None, "after_trigger": None}
        if k is not None:
            X = own(sym)
            res = own_resolve(sym, int(X["close1"][k]))
            row.update(cross_close_ms=int(X["close1"][k]), entry_close_ms=int(res["t"]),
                       entry_kind=res["kind"], moved=res["kind"] == "moved")
            if code == "RELAYED":
                row["relay_entry_ms"] = int(X["o4"][res["J"]])
                t = bk.get((sym, int(res["t"])))
                if t is not None:
                    row["relay_net_r"] = float(t.net_r)
                    row["relay_exit_reason"] = str(t.exit_reason)
                if w["trigger_i"] is not None:
                    row["lead_4h"] = int(w["trigger_i"]) - int(res["J"])
                    row["lead_1h"] = (int(w["trigger_close"]) - int(res["t"])) // H1
                    row["after_trigger"] = int(res["t"]) >= int(w["trigger_close"])
        out[key] = row
    return out, bad


def own_v6(base: pd.DataFrame) -> tuple[dict, list[str]]:
    """What v6 did in EVERY own window, by v6's slot law re-derived here
    [tierc9.replay9]: a window with no own trigger is 'no_trigger'; the triggered ones,
    per asset in (trigger bar, long first) order, are 'position_open' while the
    previous v6 campaign's exit bar (the base book's ride) is not passed, then
    'no_stop' without an own struct stop at the trigger bar's close, else 'entered' —
    and the base book must hold that campaign at the own trigger bar."""
    out, bad = {}, []
    camp = {(str(r.symbol), int(r.direction), int(r.arm_ms)): r for r in base.itertuples()}
    for sym in CLASSIC5_TYPED:
        X = own(sym)
        cands = []
        for w in own_windows(sym):
            key = (sym, w["direction"], w["arm_ms"])
            if w["trigger_i"] is None:
                out[key] = "no_trigger"
                continue
            cands.append((int(w["trigger_i"]), -int(w["direction"]), key, w))
        cands.sort(key=lambda c: (c[0], c[1]))
        open_until = -1
        for ti, _, key, w in cands:
            if ti <= open_until:
                out[key] = "position_open"
                continue
            if own_stop(sym, ti, float(X["c4"][ti]), w["direction"]) is None:
                out[key] = "no_stop"
                continue
            out[key] = "entered"
            c = camp.get(key)
            if c is None:
                bad.append(f"MISS-V6 {sym} armed {iso(key[2])}: v6's slot law enters at "
                           f"{iso(int(X['o4'][ti]))}; the base book holds no campaign on that "
                           f"arming")
                continue
            if int(c.entry_ms) != int(X["o4"][ti]):
                bad.append(f"MISS-V6 {sym} armed {iso(key[2])}: the base campaign enters "
                           f"{iso(int(c.entry_ms))}, the own trigger bar opens "
                           f"{iso(int(X['o4'][ti]))}")
            open_until = int(np.searchsorted(X["o4"], int(c.exit_ms), "left"))
    extra = sorted(set(camp) - {k for k, v in out.items() if v == "entered"})
    if extra:
        bad.append(f"MISS-V6: {len(extra)} base campaign(s) on no own-entered window (e.g. "
                   f"{extra[0][0]} armed {iso(extra[0][2])})")
    return out, bad


# ── (b) THE CLASSES THE CORRIDOR LEAVES EMPTY, PLANTED ─────────────────────────
PLANT_CLASSES = (
    ("P1 trigger planted at J, J a mismatch bar", "MISS_REFUSED_MOVED_ONTO_BOUND"),
    ("P1c trigger planted at J, J walkable (control)", "RELAYED"),
    ("P2 window close planted at J, J a mismatch bar", "MISS_REFUSED_MOVED_ONTO_BOUND"),
    ("P3 J a mismatch bar, bounds later", "RELAYED"),
    ("P4 a clone window armed at a relay's entry, its cross inside that relay",
     "MISS_REFUSED_POSITION_OPEN"),
    ("P5 the relay's structural stop planted None", "MISS_REFUSED_NO_STOP"),
    ("P6 an 89/316-against planted one bar after the arm, before the first cross",
     "MISS_CLOSED_TIDE_AGAINST"),
    ("P7 a clone window armed AT the pin, no bound", "MISS_OPEN_AT_ASOF"),
)
CLONES = ("P4", "P7")


def _mod_plant(w: dict, cls: str, J: int, om) -> list[dict]:
    """The planted copy of one module window (plus a clone for P4)."""
    w = dict(w)
    if cls.startswith("P1"):
        w.update(trigger_i=J, trigger_close_ms=int(om[J]) + H4, lag=J - int(w["arm_i"]))
    elif cls.startswith("P2"):
        if w["trigger_i"] is not None and int(w["trigger_i"]) >= J:
            w.update(trigger_i=None, trigger_close_ms=None, lag=None)
        w.update(window_end_i=J, window_close_ms=int(om[J]) + H4)
    elif cls.startswith("P6"):
        w.update(tide_against_i=int(w["arm_i"]) + 1,
                 tide_against_close_ms=int(w["arm_close_ms"]) + H4)
    return [w]


def _own_plant(w: dict, cls: str, J: int, o4) -> dict:
    w = dict(w)
    if cls.startswith("P1"):
        w.update(trigger_i=J, trigger_close=int(o4[J]) + H4, lag=J - int(w["arm_i"]))
    elif cls.startswith("P2"):
        if w["trigger_i"] is not None and int(w["trigger_i"]) >= J:
            w.update(trigger_i=None, trigger_close=None, lag=None)
        w.update(window_close=int(o4[J]) + H4)
    elif cls.startswith("P6"):
        w.update(against_close=int(w["arm_close"]) + H4)
    return w


def plant_cases(rec: pd.DataFrame) -> list[tuple]:
    """Per class, up to one relay per asset (the first that fits), from the record."""
    cases = []
    for cls, want in PLANT_CLASSES:
        for sym in CLASSIC5_TYPED:
            g = rec[(rec["symbol"] == sym) & (rec["entry_kind"] == "1h")].sort_values(
                "entry_close_ms", kind="mergesort")
            for r in g.itertuples():
                J = int(r.relay_J)
                if cls.startswith(("P1", "P2")) and not (int(r.exit_i) > J):
                    continue
                if cls.startswith("P6"):
                    w_ = own_windows_all()[(sym, int(r.direction), int(r.arm_ms))]
                    a6 = w_["arm_close"] + H4
                    if not (int(r.cross_close_ms) > a6
                            and (w_["trigger_close"] is None or w_["trigger_close"] > a6)
                            and (w_["window_close"] is None or w_["window_close"] > a6)):
                        continue
                if cls.startswith("P4"):
                    b, _ = own_bound(own_windows_all()[(sym, int(r.direction), int(r.arm_ms))])
                    k = own_first_cross(sym, int(r.direction), int(r.entry_close_ms), b)
                    if k is None or int(own(sym)["close1"][k]) > int(r.exit_close_ms):
                        continue
                cases.append((cls, want, sym, r))
                break
    return cases


def run_plant(cls: str, sym: str, r, lo: int, hi: int, mutate=None) -> tuple[dict, dict, list]:
    """The module's dispositions (planted run) and this file's, for one asset."""
    ctx = S.asset_ctx(sym, lo, hi)
    om = ctx["om"]
    J, d, key = int(r.relay_J), int(r.direction), (sym, int(r.direction), int(r.arm_ms))
    real = [dict(w) for w in S.windows_of(ctx)]
    mw, ow = [], []
    X = own(sym)
    own_by = {(sym, w["direction"], w["arm_ms"]): w for w in own_windows(sym)}
    for w in real:
        k = (sym, int(w["direction"]), int(w["arm_ms"]))
        if k == key and cls.startswith(("P1", "P2", "P6")):
            mw += _mod_plant(w, cls, J, om)
            ow.append(_own_plant(own_by[k], cls, J, X["o4"]))
        else:
            mw.append(w)
            ow.append(own_by[k])
    if cls.startswith(CLONES):
        t_e = int(r.entry_close_ms) if cls.startswith("P4") else PIN
        c = dict(next(w for w in real if (sym, int(w["direction"]), int(w["arm_ms"])) == key))
        c.update(arm_ms=t_e - H4, arm_close_ms=t_e)
        oc = dict(own_by[key])
        oc.update(arm_ms=t_e - H4, arm_close=t_e)
        if cls.startswith("P7"):
            c.update(trigger_i=None, trigger_close_ms=None, lag=None,
                     window_end_i=ctx["hi_i"] + 1, window_close_ms=None, tide_against_i=None,
                     tide_against_close_ms=None)
            oc.update(trigger_i=None, trigger_close=None, lag=None, window_close=None,
                      against_close=None)
        mw.append(c)
        ow.append(oc)
    W = ctx["W"]
    mism = frozenset()
    if cls.startswith(("P1 ", "P2", "P3")):
        ok2 = W.ok.copy()
        ok2[J] = False
        why2 = dict(W.why)
        why2[J] = "PLANTED mismatch (fixture)"
        W = dataclasses.replace(W, ok=ok2, why=why2)
        mism = frozenset({J})
    nostop = frozenset()
    stack = contextlib.ExitStack()
    with stack:
        stack.enter_context(mutated(S, "windows_of", lambda c_: [dict(x) for x in mw]))
        if cls.startswith("P5"):
            orig = RD.relay_stop
            tgt = (sym, int(r.asof_i), float(r.entry_px), d)

            def rs(s_, asof_i, px, d_, card):
                if (s_, int(asof_i), float(px), int(d_)) == tgt:
                    return None, float("nan")
                return orig(s_, asof_i, px, d_, card)
            stack.enter_context(mutated(RD, "relay_stop", rs))
            nostop = frozenset({(int(r.asof_i), float(r.entry_px))})
        if mutate is not None:
            stack.enter_context(mutate())
        trades, rows = S.relay_asset(dict(ctx, W=W), late=False)
    mod = {(sym, int(x["direction"]), int(x["arm_ms"])): x for x in rows}
    exits = {(sym, int(getattr(t, "entry_close_ms"))): int(getattr(t, "exit_close_ms"))
             for t in trades}
    od, bad = own_asset_dispositions(sym, ow, exits, mism, nostop)
    return mod, od, bad + [{"trades": trades, "key": key, "J": J}]


def plant_findings(mutate=None) -> tuple[list[str], dict]:
    lo, hi, _ = B.corridor()
    rec = reg("scored")
    out, tally = [], {c: 0 for c, _ in PLANT_CLASSES}
    for cls, want, sym, r in plant_cases(rec):
        mod, od, extra = run_plant(cls, sym, r, lo, hi, mutate)
        info = extra.pop()
        out += extra
        tally[cls] += 1
        lab = f"{cls.split()[0]} {sym} relay {iso(int(r.entry_close_ms))}"
        for k in sorted(set(mod) | set(od)):
            if mod.get(k, {}).get("disposition") != od.get(k):
                out.append(f"MISS-PLANT {lab}: window {iso(k[2])} module "
                           f"{mod.get(k, {}).get('disposition')} != own {od.get(k)}")
        tk = (info["key"] if not cls.startswith(CLONES) else
              (sym, int(r.direction), (int(r.entry_close_ms) if cls.startswith("P4") else PIN)
               - H4))
        got = mod.get(tk, {}).get("disposition")
        if got != want:
            out.append(f"MISS-PLANT {lab}: the planted window is {got}, the class says {want}")
        X, J = own(sym), info["J"]
        if cls.startswith("P3") and got == "RELAYED":
            t = next(t for t in info["trades"] if int(t.arm_ms) == int(r.arm_ms))
            ok = (int(getattr(t, "entry_close_ms")) == int(X["o4"][J]) + H4
                  and float(t.entry_px) == float(X["c4"][J])
                  and "parent-close" in str(getattr(t, "entry_kind"))
                  and int(X["o4"][J]) in [int(x) for x in getattr(t, "walk_mismatch_ms")])
            if not ok:
                out.append(f"MISS-PLANT {lab}: the moved relay is not at the parent's close / "
                           f"price, or the bar is not counted")
        if cls.startswith("P1c") and got == "RELAYED":
            t = next(t for t in info["trades"] if int(t.arm_ms) == int(r.arm_ms))
            if int(getattr(t, "entry_close_ms")) != int(r.entry_close_ms) or int(t.entry_i) != J:
                out.append(f"MISS-PLANT {lab}: the walkable control did not relay at its 1h close "
                           f"inside the trigger bar")
    return out, tally


REC_BOUND_COLS = (("trigger_close_ms", "trigger_close"), ("window_close_ms", "window_close"),
                  ("tide_against_close_ms", "against_close"), ("lag", "lag"),
                  ("arm_close_ms", "arm_close"))


def _kind_ok(table_kind, own_kind) -> bool:
    """The table's entry_kind against the own resolution kind (typed prefixes)."""
    if own_kind is None:
        return table_kind is None
    return table_kind is not None and str(table_kind).startswith(ENTRY_KIND_TYPED[own_kind])


def window_col_findings(win: pd.DataFrame, rec: dict, lat: dict) -> list[str]:
    """EVERY window row's bound / entry columns (MISS-BOUNDS, MISS-ENTRY) and late
    columns (MISS-LATE) against this file's own rows [L-T.2, SR-2, SR-6]."""
    out = []
    W = own_windows_all()
    for r in win.itertuples():
        k = (str(r.symbol), int(r.direction), int(r.arm_ms))
        w, o, ol = W.get(k), rec.get(k), lat.get(k)
        if w is None or o is None or ol is None:
            continue                       # MISS-PARTITION names it
        lab = f"{k[0]} {k[1]:+d} armed {iso(k[2])}"
        for c, f_ in REC_BOUND_COLS:
            if _nz(getattr(r, c)) != w[f_]:
                out.append(f"MISS-BOUNDS {lab}: {c} {_nz(getattr(r, c))} != own {w[f_]}")
        if _nz(r.bound_ms) != o["bound_ms"] or str(r.bound_kind) != o["bound_kind"]:
            out.append(f"MISS-BOUNDS {lab}: bound {_nz(r.bound_ms)} / {r.bound_kind} != own "
                       f"{o['bound_ms']} / {o['bound_kind']}")
        for c in ("cross_close_ms", "entry_close_ms", "relay_entry_ms", "relay_exit_reason",
                  "moved"):
            if _nz(getattr(r, c)) != o[c]:
                out.append(f"MISS-ENTRY {lab}: {c} {_nz(getattr(r, c))} != own {o[c]}")
        if not _kind_ok(_nz(r.entry_kind), o["entry_kind"]):
            out.append(f"MISS-ENTRY {lab}: entry_kind {r.entry_kind} != own {o['entry_kind']}")
        if _nz(r.relay_net_r) != _r6(o["relay_net_r"]):
            out.append(f"MISS-ENTRY {lab}: relay_net_r {_nz(r.relay_net_r)} != the book's "
                       f"{_r6(o['relay_net_r'])}")
        for c, oc in (("late_bound_ms", "bound_ms"), ("late_bound_kind", "bound_kind"),
                      ("late_cross_close_ms", "cross_close_ms"),
                      ("late_entry_close_ms", "entry_close_ms"),
                      ("late_disposition", "disposition"),
                      ("late_after_trigger", "after_trigger")):
            if _nz(getattr(r, c)) != ol[oc]:
                out.append(f"MISS-LATE {lab}: {c} {_nz(getattr(r, c))} != own late {ol[oc]}")
        if _nz(r.late_relay_net_r) != _r6(ol["relay_net_r"]):
            out.append(f"MISS-LATE {lab}: late_relay_net_r {_nz(r.late_relay_net_r)} != the "
                       f"late book's {_r6(ol['relay_net_r'])}")
    return out


def v6_col_findings(win: pd.DataFrame, v6: dict, base: pd.DataFrame) -> list[str]:
    """EVERY window's v6 columns against v6's slot law re-derived here (own_v6) and the
    base book's campaign: label (typed), entered flag, entry, net R (6 dp), exit."""
    out = []
    camp = {(str(r.symbol), int(r.direction), int(r.arm_ms)): r for r in base.itertuples()}
    for r in win.itertuples():
        k = (str(r.symbol), int(r.direction), int(r.arm_ms))
        code = v6.get(k)
        if code is None:
            continue                       # MISS-PARTITION names it
        lab = f"{k[0]} armed {iso(k[2])}"
        if r.v6_disposition != V6_LABEL_TYPED[code]:
            out.append(f"MISS-V6 {lab}: label {r.v6_disposition!r} != v6's slot law "
                       f"{V6_LABEL_TYPED[code]!r}")
        if bool(r.v6_entered) != (code == "entered"):
            out.append(f"MISS-V6 {lab}: v6_entered {bool(r.v6_entered)} != v6's slot law "
                       f"({code})")
        t = camp.get(k) if code == "entered" else None
        want = ((None, None, None, None) if t is None else
                (int(t.entry_ms), int(t.entry_ms) + H4, _r6(float(t.net_r)), str(t.exit_reason)))
        got = (_nz(r.v6_entry_ms), _nz(r.v6_entry_close_ms), _nz(r.v6_net_r),
               _nz(r.v6_exit_reason))
        if got != want:
            out.append(f"MISS-V6 {lab}: v6 columns {got} != the base book's campaign {want}")
    return out


def miss_v6_findings(miss_book: pd.DataFrame, base: pd.DataFrame, rec: dict) -> list[str]:
    """tierE__miss_v6 == the base campaigns whose OWN window is not RELAYED, row for row."""
    out = []
    want = {(str(r.symbol), int(r.entry_ms)): float(r.net_r) for r in base.itertuples()
            if rec.get((str(r.symbol), int(r.direction), int(r.arm_ms)), {}).get(
                "disposition") not in (None, "RELAYED")}
    got = [(str(r.symbol), int(r.entry_ms)) for r in miss_book.itertuples()]
    if len(set(got)) != len(got) or set(got) != set(want):
        out.append(f"MISS-V6BOOK: tierE__miss_v6 holds {len(got)} campaign(s), the base "
                   f"campaigns in own non-RELAYED windows are {len(want)} (absent "
                   f"{len(set(want) - set(got))}, extra {len(set(got) - set(want))})")
    for r in miss_book.itertuples():
        k = (str(r.symbol), int(r.entry_ms))
        if k in want and float(r.net_r) != want[k]:
            out.append(f"MISS-V6BOOK {k[0]} {iso(k[1])}: net_r {r.net_r!r} != the base "
                       f"book's {want[k]!r}")
    return out


def miss_findings(win: pd.DataFrame, book: pd.DataFrame, late_book: pd.DataFrame,
                  base: pd.DataFrame, miss_book: pd.DataFrame) -> list[str]:
    out = []
    own_d, bad = own_dispositions(book)
    out += bad
    keys = [(str(r.symbol), int(r.direction), int(r.arm_ms)) for r in win.itertuples()]
    if len(set(keys)) != len(keys):
        dup = sorted({k for k in keys if keys.count(k) > 1})
        out.append(f"MISS-PARTITION: {len(keys) - len(set(keys))} window(s) listed twice "
                   f"(e.g. {dup[0][0]} {iso(dup[0][2])})")
    if set(keys) != set(own_d):
        out.append(f"MISS-PARTITION: the windows table holds {len(set(keys))} windows, this "
                   f"file's own set {len(own_d)} (absent {len(set(own_d) - set(keys))}, extra "
                   f"{len(set(keys) - set(own_d))})")
    bad_code = sorted(set(win["disposition"]) - set(CODES_TYPED))
    if bad_code:
        out.append(f"MISS-PARTITION: codes outside the typed set {bad_code}")
    for r in win.itertuples():
        k = (str(r.symbol), int(r.direction), int(r.arm_ms))
        if k in own_d and own_d[k] != r.disposition:
            out.append(f"MISS-REASON {k[0]} {k[1]:+d} armed {iso(k[2])}: table "
                       f"{r.disposition} != own {own_d[k]}")
        if not pd.isna(r.lag) and int(r.lag) == 0 and r.disposition == "RELAYED":
            out.append(f"MISS-REASON {k[0]} armed {iso(k[2])}: a lag-0 window relayed")
    rel_w = sorted(k for k, r in zip(keys, win["disposition"]) if r == "RELAYED")
    bk = sorted((str(r.symbol), int(r.direction), int(r.arm_ms)) for r in book.itertuples())
    if rel_w != bk:
        out.append(f"MISS-COUNT: {len(rel_w)} RELAYED windows vs {len(bk)} relays in the book "
                   f"(not one to one)")
    # the bound / entry / late columns of EVERY row (verifier m2, m5)
    rec, _ = own_rows(book, late=False)
    lat, lbad = own_rows(late_book, late=True)
    out += [f"MISS-LATE {x}" for x in lbad]
    lrel = sorted(k for k, o in lat.items() if o["disposition"] == "RELAYED")
    lbk = sorted((str(r.symbol), int(r.direction), int(r.arm_ms))
                 for r in late_book.itertuples())
    if lrel != lbk:
        out.append(f"MISS-LATE: {len(lrel)} own late RELAYED windows vs {len(lbk)} relays in "
                   f"tierE__late_relay (not one to one)")
    out += window_col_findings(win, rec, lat)
    # what v6 did in EVERY window, by v6's slot law (verifier m4)
    v6, vbad = own_v6(base)
    out += vbad
    out += v6_col_findings(win, v6, base)
    out += miss_v6_findings(miss_book, base, rec)
    return out


def v6_label_plants(mutate=None) -> tuple[list[str], dict]:
    """The v6 labels the corridor leaves EMPTY, planted: per asset, the first entered
    arming's replay9 code planted 'position_open' / '' (stop-less) and its v6 trade
    removed; the module's windows_of must label EVERY window of the asset by the typed
    label of its (planted) replay9 code, and the planted window not entered."""
    lo, hi, _ = B.corridor()
    out, tally = [], {"position_open": 0, "": 0}
    for code in ("position_open", ""):
        for sym in CLASSIC5_TYPED:
            ctx = S.asset_ctx(sym, lo, hi)
            arms = [copy.copy(a) for a in ctx["arms"]]
            idx = next((i for i, a in enumerate(arms) if a.tide_ok and a.d_ok
                        and str(a.reject) == "entered"), None)
            if idx is None:
                continue
            arms[idx].reject = code
            tgt = (int(arms[idx].arm_i), int(arms[idx].direction))
            trades = [t for t in ctx["trades"] if (int(t.arm_i), int(t.direction)) != tgt]
            with (mutate() if mutate is not None else contextlib.nullcontext()):
                rows = S.windows_of(dict(ctx, arms=arms, trades=trades))
            tally[code] += 1
            by = {(int(a.arm_i), int(a.direction)): str(a.reject) for a in arms
                  if a.tide_ok and a.d_ok}
            for r in rows:
                rc = by.get((int(r["arm_i"]), int(r["direction"])))
                want = V6_LABEL_TYPED[V6_REPLAY_CODE_TYPED[rc]] if rc in V6_REPLAY_CODE_TYPED \
                    else None
                if r["v6_disposition"] != want:
                    out.append(f"MISS-V6LABEL {sym} armed {iso(int(r['arm_ms']))} (replay9 code "
                               f"{rc!r}{', PLANTED' if (int(r['arm_i']), int(r['direction'])) == tgt else ''}): "
                               f"module label {r['v6_disposition']!r} != typed {want!r}")
            pr = [r for r in rows if (int(r["arm_i"]), int(r["direction"])) == tgt]
            if len(pr) != 1 or bool(pr[0]["v6_entered"]):
                out.append(f"MISS-V6LABEL {sym}: the planted window is not listed once, "
                           f"not entered")
    return out, tally


def _miss_inputs() -> tuple:
    return (pd.read_parquet(str(OUT / "relay_windows.parquet")), reg("scored"),
            reg("tierE__late_relay"), reg("base"), reg("tierE__miss_v6"))


def _rebuilt_miss() -> list[str]:
    """The module's windows table and both books rebuilt in-process (the path a
    MUTATION is judged on), judged by miss_findings against the base of record."""
    lo, hi, _ = B.corridor()
    tr, w0 = S.relay_book(lo, hi, late=False)
    tl, wl = S.relay_book(lo, hi, late=True)
    return miss_findings(S.window_table(w0, wl), S.regbook_frame(tr, "relay"),
                         S.regbook_frame(tl, "relay"), reg("base"), reg("tierE__miss_v6"))


def miss_break():
    win, book, late_book, base, miss_book = _miss_inputs()

    def mf(w=win, b=book, lb=late_book, mb=miss_book):
        return miss_findings(w, b, lb, base, mb)

    def double():
        r = win[win["disposition"] == "RELAYED"].iloc[[0]].copy()
        r["disposition"] = "MISS_TRIGGER_FIRST"
        return mf(w=pd.concat([win, r], ignore_index=True))

    def dropped():
        return mf(w=win.drop(index=win.index[3]).reset_index(drop=True))

    def flipped():
        d = win.copy()
        i = d.index[d["disposition"] == "MISS_TRIGGER_FIRST"][0]
        d.loc[i, "disposition"] = "MISS_CLOSED_COUNTER_12_89"
        return mf(w=d)

    def twice():
        return mf(b=pd.concat([book, book.iloc[[2]]], ignore_index=True))

    def v6_bent():
        d = win.copy()
        i = d.index[d["v6_entered"].astype(bool)][0]
        d.loc[i, "v6_net_r"] = float(d.loc[i, "v6_net_r"]) + 1e-9
        return mf(w=d)

    def against_nulled():
        d = win.copy()
        d["tide_against_close_ms"] = pd.array([pd.NA] * len(d), dtype="Int64")
        return mf(w=d)

    def late_is_record():
        d = win.copy()
        for c in ("bound_ms", "bound_kind", "cross_close_ms", "entry_close_ms", "disposition",
                  "relay_net_r"):
            d[f"late_{c}"] = d[c]
        return mf(w=d)

    def v6_label():
        d = win.copy()
        i = d.index[~d["v6_entered"].astype(bool)][0]
        d.loc[i, "v6_disposition"] = V6_LABEL_TYPED["position_open"]
        return mf(w=d)

    def miss_v6_plus():
        rel = {(str(r.symbol), int(r.direction), int(r.arm_ms)) for r in book.itertuples()}
        extra = base[[(s, int(dd), int(a)) in rel for s, dd, a in
                      zip(base["symbol"], base["direction"], base["arm_ms"])]].iloc[[0]]
        return mf(mb=pd.concat([miss_book, extra], ignore_index=True))

    def no_lag0():
        orig = S._miss_code

        def m(w, kinds):
            c = orig(w, kinds)
            return "MISS_TRIGGER_FIRST" if c == "MISS_TRIGGER_FIRST_LAG0" else c
        with mutated(S, "_miss_code", m):
            return _rebuilt_miss()

    def no_moved():
        orig = RD.relay11

        def r11(*a, **k):
            k["moved"] = False
            return orig(*a, **k)
        return plant_findings(lambda: mutated(RD, "relay11", r11))[0]

    def bound_only():
        ob = S.bound_of
        with mutated(S, "bound_of", lambda w, late: ob(w, True)):
            return _rebuilt_miss()

    def late_on_record_bounds():
        ob = S.bound_of
        with mutated(S, "bound_of", lambda w, late: ob(w, False)):
            return _rebuilt_miss()

    def label_swapped():
        sw = dict(S.V6_DISPOSITION)
        sw["position_open"] = S.V6_DISPOSITION["no_trigger"]
        return v6_label_plants(lambda: mutated(S, "V6_DISPOSITION", sw))[0]

    return plants([
        ("a RELAYED window double-counted as a trigger-first miss (copy)", "MISS-PARTITION",
         double),
        ("a window dropped from the table (copy)", "MISS-PARTITION", dropped),
        ("a trigger-first miss relabelled closed-unrelayed (copy)", "MISS-REASON", flipped),
        ("a relay counted twice in the book (copy)", "MISS-COUNT", twice),
        ("what v6 did bent by 1e-9 R in one window (copy)", "MISS-V6", v6_bent),
        ("the 89/316-against close nulled on every window (copy)", "MISS-BOUNDS",
         against_nulled),
        ("the late columns copied from the record's (copy)", "MISS-LATE", late_is_record),
        ("a no-trigger window's v6 label swapped to position open (copy)", "MISS-V6",
         v6_label),
        ("a RELAYED window's v6 campaign added to tierE__miss_v6 (copy)", "MISS-V6BOOK",
         miss_v6_plus),
        ("[mutant] the lag-0 split removed from the module's miss code", "MISS-REASON",
         no_lag0),
        ("[mutant] the trigger bound alone dropped (relay_entry still refuses at the trigger: "
         "the trigger-first windows turn into refusals)", "MISS-REASON", bound_only),
        ("[mutant] the late twin built on the record's bounds (bound_of ignores `late`)",
         "MISS-LATE", late_on_record_bounds),
        ("[mutant] SR-4's bound check removed from the runner (planted classes)", "MISS-PLANT",
         lambda: plant_findings(lambda: mutated(S, "moved_refused", lambda t, b: False))[0]),
        ("[mutant] the one-position law removed from the runner (planted classes)",
         "MISS-PLANT",
         lambda: plant_findings(lambda: mutated(S, "position_open", lambda t, o: False))[0]),
        ("[mutant] the runner does not pass relay_entry's `moved` to relay11 (planted "
         "classes: the mismatch bar goes uncounted)", "MISS-PLANT", no_moved),
        ("[mutant] the position-open v6 label swapped for the no-trigger label (planted "
         "replay9 codes)", "MISS-V6LABEL", label_swapped),
    ])


def miss_real():
    win, book, late_book, base, miss_book = _miss_inputs()
    bad = miss_findings(win, book, late_book, base, miss_book)
    c = win["disposition"].value_counts().to_dict()
    lc = win["late_disposition"].value_counts().to_dict()
    vc = win["v6_disposition"].value_counts().to_dict()
    lag0 = win[win["lag"] == 0]
    own_n = len(own_windows_all())
    pb, tally = plant_findings()
    lb, ltally = v6_label_plants()
    empty = sorted(set(CODES_TYPED) - set(c))
    line_b = (f"(b) the classes the corridor leaves EMPTY ({empty}) planted on real relays "
              f"(a planted mismatch Walk, a planted trigger / window close / 89/316-against, "
              f"clone windows, a stop planted None — one asset at a time, the module's relay_asset vs this "
              f"file's derivation on EVERY window of the asset): "
              + "; ".join(f"{k.split()[0]} x{v} -> {w}" for (k, w), v in
                          zip(PLANT_CLASSES, tally.values()))
              + f": {not pb}" + (f"; findings {pb[:3]}" if pb else ""))
    line_v = (f"(d) the v6 labels the corridor leaves EMPTY planted (per asset the first "
              f"entered arming's replay9 code set to 'position_open' x{ltally['position_open']} "
              f"/ '' stop-less x{ltally['']}, its v6 trade removed): the module's windows_of "
              f"labels EVERY window of the asset by the typed label of its replay9 code and "
              f"the planted window is not entered: {not lb}"
              + (f"; findings {lb[:3]}" if lb else ""))
    thin = [k.split()[0] for k, v in tally.items() if v < 3]
    if thin:
        pb.append(f"MISS-PLANT: classes with fewer than 3 planted cases {thin}")
    if min(ltally.values()) < 3:
        lb.append(f"MISS-V6LABEL: fewer than 3 planted cases per code {ltally}")
    n_against = int(win["tide_against_close_ms"].notna().sum())
    line_c = (f"(c) EVERY row's columns re-derived here: the bounds (trigger / counter 12/89 / "
              f"89/316-against closes — {n_against} windows with an 89/316-against by the pin "
              f"— lag, arm close, the earliest bound and its tied kinds), the entry (first "
              f"own cross, resolved instant / kind / moved, the relay's 4h bar, the book's net "
              f"R at {TABLE_DP} dp and exit reason), the LATE columns by the own late law "
              f"(late dispositions {dict(sorted(lc.items()))}; the late RELAYED windows 1:1 "
              f"the {len(late_book)} relays of tierE__late_relay); the v6 label of EVERY "
              f"window by v6's slot law re-derived here ({dict(sorted(vc.items()))}); "
              f"tierE__miss_v6 ({len(miss_book)}) == the base campaigns in own non-RELAYED "
              f"windows: {not bad}")
    bad = bad + pb + lb
    return (not bad), [line_b, line_v, line_c,
                       (f"(a) {len(win)} windows == this file's own card armings ({own_n}; own 4h "
                       f"EMA12/89 cross, tide, d >= {D_MIN}), each listed once with one typed "
                       f"code: {dict(sorted(c.items()))}; every code re-derived by this file "
                       f"(own bounds, own first 1h 9/12 cross, own L-W.0 resolution, own stop, "
                       f"the book's exit instants for the position law); {len(lag0)} lag-0 "
                       f"windows, all misses ({sorted(set(lag0['disposition']))}); RELAYED "
                       f"windows 1:1 the {len(book)} relays; what v6 did == the base book's "
                       f"campaign (net R at the table's {TABLE_DP} dp) on every one of the "
                       f"{int(win['v6_entered'].astype(bool).sum())} entered windows: {not bad}"
                       + (f"; findings {bad[:4]}" if bad else ""))]


# ════════════════════════════════════════════════════════════════════ F-FWD
_TEMPS: list[Path] = []


def fwd_dir(tag: str) -> Path:
    """A temp dir outside the repo whose parent is `_det_forward` (the ledger's guard);
    removed when the run ends."""
    t = Path(tempfile.mkdtemp(prefix=f"f-fwd-{tag}-"))
    _TEMPS.append(t)
    d = t / F.DET_ROOT.name / "plant"
    d.parent.mkdir(parents=True, exist_ok=True)
    return d


def referee_books(pin_ms: int) -> dict:
    """The frozen books at a pin, straight from tierc11_books (the referee path)."""
    lo, hi, _ = B.corridor(None if pin_ms == PIN else iso(pin_ms))
    return {"v6": B.v6_book(lo, hi), "trg912": B.trg912_book(lo, hi)}


def fwd_checks(path: Path, opening: int, pin_ms: int) -> list[str]:
    """This file's claims about a ledger after a refresh at `pin_ms`."""
    out = []
    raw_ = path.read_bytes()
    cb, objs = F.verify_chain(raw_)
    out += cb
    camps = [o for o in objs if o.get("kind") == "CAMPAIGN"]
    keys = [(o["book"], o["key"][0], int(o["key"][1])) for o in camps]
    for k in sorted({k for k in keys if keys.count(k) > 1}):
        out.append(f"FWD-APPEND-TWICE {k[0]} {k[1]} {iso(k[2])}: appended {keys.count(k)} times")
    for o in camps:
        r = o["row"]
        if r["exit_reason"] == "corridor_end":
            out.append(f"FWD-OPEN-APPENDED {o['book']} {r['symbol']} {iso(int(r['entry_ms']))}: an "
                       f"OPEN campaign appended")
        if not int(r["entry_close_ms"]) > opening:
            out.append(f"FWD-CONTINUATION-COUNTED {o['book']} {r['symbol']} "
                       f"{iso(int(r['entry_ms']))}: entered at/before the opening, counted")
    bk = referee_books(pin_ms)
    want = set()
    for b, book in bk.items():
        for t in book:
            if int(t.entry_ms) + H4 > opening and str(t.exit_reason) != "corridor_end":
                want.add((b, t.symbol, int(t.entry_ms)))
    if set(keys) != want:
        out.append(f"FWD-SET: appended {len(set(keys))} != the frozen books' closed-after-opening "
                   f"{len(want)} (absent {sorted(want - set(keys))[:2]}, extra "
                   f"{sorted(set(keys) - want)[:2]})")
    tr = {(b, t.symbol, int(t.entry_ms)): t for b, book in bk.items() for t in book}
    for o in camps:
        k = (o["book"], o["key"][0], int(o["key"][1]))
        t, r = tr.get(k), o["row"]
        if t is None:
            continue
        lag = int(t.entry_i) - int(t.arm_i)
        hc = float(t.net_r) - float(t.fee_r) * SLIP_TYPED[t.symbol] / TAKER_TYPED
        ok = (float(r["net_r"]) == float(t.net_r) and r["exit_reason"] == str(t.exit_reason)
              and float(r["entry_px"]) == float(t.entry_px)
              and float(r["stop_px"]) == float(t.stop_px)
              and float(r["r_dist"]) == float(t.r_dist)
              and int(r["exit_ms"]) == int(t.exit_ms) and int(r["p_win_1_lag"]) == lag
              and bool(r["p_win_1_refuses"]) == (lag >= P_WIN_1_TYPED)
              and bool(r["p_age_1_refuses"]) == (r["tide_band"] == P_AGE_1_OLD_TYPED)
              and float(r["haircut_net_r"]) == hc)
        if not ok:
            out.append(f"FWD-ROW {k[0]} {k[1]} {iso(k[2])}: the appended row is not the frozen "
                       f"book's campaign (net/exit/prices/stamps)")
    return out


def plant_pins(opening: int) -> tuple[int, int, tuple]:
    """P1 inside the life of the longest-held campaign closed after the opening (so it
    is OPEN at P1), P2 its exit bar's close (closed at P2)."""
    bk = referee_books(PIN)
    best = None
    for b in ("v6", "trg912"):
        for t in bk[b]:
            if int(t.entry_ms) + H4 > opening and str(t.exit_reason) != "corridor_end":
                span = int(t.exit_ms) - (int(t.entry_ms) + H4)
                k = (span, b, t.symbol, int(t.entry_ms))
                if best is None or k > best[0]:
                    best = (k, t, b)
    (_, b, sym, ems), t, _ = best
    ecl = ems + H4
    p1 = ecl + ((int(t.exit_ms) - ecl) // 2 // H4) * H4
    if not (ecl < p1 <= int(t.exit_ms)):
        raise RuntimeError("no interior pin")
    return p1, int(t.exit_ms) + H4, (b, sym, ems)


def fwd_sequence(d: Path, opening: int, pins: tuple) -> list[str]:
    """Refresh at each pin; after each, this file's checks.  A HALT is a finding."""
    out = []
    for p in pins:
        try:
            F.refresh(d, p, opening)
        except SystemExit as e:
            out.append(str(e) if str(e).startswith("HALT") else f"HALT: {e}")
            break
        out += [f"[after {iso(p)}] {x}" for x in fwd_checks(d / F.LEDGER, opening, p)]
    return out


def stamp_findings(rows: dict, planted: dict) -> list[str]:
    """The planted rows' gate stamps against the TYPED laws: P-WIN-1 refuses lag >= 16,
    its shadow 7-15; P-AGE-1 refuses the OLD band B4."""
    out = []
    for k, (lag, band) in sorted(planted.items()):
        r = rows.get(k)
        if r is None:
            out.append(f"FWD-STAMP {k[0]} {iso(k[1])}: the planted row is absent")
            continue
        want = {"p_win_1_lag": lag, "p_win_1_refuses": lag >= P_WIN_1_TYPED,
                "p_win_1_shadow_refuses": P_WIN_1_SHADOW_TYPED[0] <= lag
                <= P_WIN_1_SHADOW_TYPED[1],
                "p_age_1_band": band, "p_age_1_refuses": band == P_AGE_1_OLD_TYPED}
        diff = {f: r.get(f) for f in want if r.get(f) != want[f]}
        if diff:
            out.append(f"FWD-STAMP {k[0]} {iso(k[1])} (planted lag {lag}, band {band}): stamps "
                       f"{diff} != the typed law")
    return out


def stamp_plant(mutate=None) -> tuple[list[str], dict]:
    """F.book_rows on the frozen v6 book at the TC11 pin, B.campaign_rows planted so
    five rows carry the boundary lags 6 / 7 / 15 / 16 / 17 and bands (STAMP_PLANT) —
    the cut the corridor never exercises (no appended campaign has lag 16)."""
    lo, hi, _ = B.corridor()
    v6 = B.v6_book(lo, hi)
    pool = B.tide_pool(lo, hi)
    orig = B.campaign_rows
    planted: dict = {}

    def camp(book, roles, lo_, hi_, pool_, name):
        df = orig(book, roles, lo_, hi_, pool_, name).copy()
        df = df.sort_values(["symbol", "entry_ms"], kind="mergesort").reset_index(drop=True)
        df["tide_band"] = df["tide_band"].astype(object)
        for j, (lag, band) in enumerate(STAMP_PLANT):
            df.loc[j, "lag"] = lag
            df.loc[j, "tide_band"] = band
            planted[(str(df.loc[j, "symbol"]), int(df.loc[j, "entry_ms"]))] = (lag, band)
        return df
    with mutated(B, "campaign_rows", camp), \
            (mutate() if mutate is not None else contextlib.nullcontext()):
        rows = F.book_rows("v6", v6, T9.V6_ROLES, lo, hi, pool)
    return stamp_findings(rows, planted), planted


def mark_findings(objs: list[dict]) -> list[str]:
    """Every OPEN entry and continuation of every REFRESH line: still open at the pin
    (exit_reason corridor_end) <=> marked to the pin (net_r_marked_to_pin, no net_r)."""
    out = []
    for o in objs:
        if o.get("kind") != "REFRESH":
            continue
        for b in sorted(o.get("books", {})):
            bk = o["books"][b]
            for name, xs in (("OPEN", bk.get("open", [])),
                             ("continuation", bk.get("continuations_not_admitted", []))):
                for x in xs:
                    still = x.get("exit_reason") == "corridor_end"
                    ok = (("net_r_marked_to_pin" in x and "net_r" not in x) if still
                          else ("net_r" in x and "net_r_marked_to_pin" not in x))
                    if name == "OPEN" and not still:
                        ok = False
                    if not ok:
                        out.append(f"FWD-MARK {b} {name} {x['key'][0]} {iso(int(x['key'][1]))}: "
                                   f"exit {x.get('exit_reason')} labelled "
                                   f"{sorted(k for k in x if k.startswith('net_r'))}")
    return out


def cont_plant() -> tuple[Path, list]:
    """A planted opening at the 9/12 SOL campaign's entry close, refreshed at the TC11
    pin: that campaign is a continuation STILL OPEN at the pin."""
    d = fwd_dir("cont-open")
    F.refresh(d, PIN, _ms(FWD_CONT_PLANT_OPENING))
    objs = F.verify_chain((d / F.LEDGER).read_bytes())[1]
    still = [(b, x["key"][0], iso(int(x["key"][1])))
             for o in objs if o.get("kind") == "REFRESH" for b in sorted(o["books"])
             for x in o["books"][b]["continuations_not_admitted"]
             if x["exit_reason"] == "corridor_end"]
    return d, still


def fwd_break():
    op = _ms(FWD_PLANT_OPENING)
    p1, p2, tgt = plant_pins(op)
    seq = (p1, p2, PIN)

    def m_closed():
        with mutated(F, "is_closed", lambda row: True):
            return fwd_sequence(fwd_dir("open"), op, seq)

    def m_admit():
        with mutated(F, "admitted", lambda row, o: int(row["exit_ms"]) >= int(o)):
            return fwd_sequence(fwd_dir("cont"), op, seq)

    def m_twice():
        with mutated(F, "already", lambda appended, b, k: False):
            return fwd_sequence(fwd_dir("twice"), op, seq)

    def m_changed():
        d = fwd_dir("changed")
        F.refresh(d, p1, op)
        objs = F.verify_chain((d / F.LEDGER).read_bytes())[1]
        first = next(o for o in objs if o["kind"] == "CAMPAIGN")
        tgt = (first["key"][0], int(first["key"][1]))
        book_fn = B.v6_book if first["book"] == "v6" else B.trg912_book
        name = "v6_book" if first["book"] == "v6" else "trg912_book"

        def bent(lo, hi):
            out = []
            for t in book_fn(lo, hi):
                if (t.symbol, int(t.entry_ms)) == tgt:
                    t = copy.copy(t)
                    object.__setattr__(t, "net_r", float(t.net_r) + 1e-9)
                out.append(t)
            return out
        with mutated(B, name, bent):
            try:
                F.refresh(d, p2, op)
            except SystemExit as e:
                return [str(e) if str(e).startswith("HALT") else f"HALT: {e}"]
        return []

    def tampered():
        raw_ = (FWD / F.LEDGER).read_bytes()
        s_ = raw_.decode("utf-8")
        i = s_.index('"opening_ms":') + len('"opening_ms":') + 3
        bent = (s_[:i] + ("7" if s_[i] != "7" else "8") + s_[i + 1:]).encode("utf-8")
        return F.verify_chain(bent)[0]

    def backwards():
        d = fwd_dir("back")
        F.refresh(d, p2, op)
        F.refresh(d, p1, op)
        return []

    def other_snapshot():
        F.check_snapshot(SNAP_PLANT)
        return []

    def same_pin_closes():
        b, sym, ems = tgt
        d = fwd_dir("samepin")
        F.refresh(d, p1, op)
        name = "v6_book" if b == "v6" else "trg912_book"
        orig = getattr(B, name)

        def closed(lo, hi):
            out = []
            for t in orig(lo, hi):
                if (t.symbol, int(t.entry_ms)) == (sym, ems):
                    t = copy.copy(t)
                    object.__setattr__(t, "exit_reason", "stop")
                out.append(t)
            return out
        with mutated(B, name, closed):
            F.refresh(d, p1, op)
        return []

    def cont_relabelled():
        d, _ = cont_plant()
        objs = F.verify_chain((d / F.LEDGER).read_bytes())[1]
        bent = copy.deepcopy(objs)
        for o in bent:
            if o.get("kind") == "REFRESH":
                for bk in o["books"].values():
                    for x in bk["continuations_not_admitted"]:
                        if "net_r_marked_to_pin" in x:
                            x["net_r"] = x.pop("net_r_marked_to_pin")
        return mark_findings(bent)

    def deleted():
        d = fwd_dir("del")
        fwd_sequence(d, op, (p1,))
        lines_ = (d / F.LEDGER).read_bytes().split(b"\n")
        return F.verify_chain(b"\n".join(lines_[:2] + lines_[3:]))[0]

    return plants([
        ("[mutant] an OPEN campaign treated as closed", "FWD-OPEN-APPENDED", m_closed),
        ("[mutant] continuations admitted (exit after the opening)",
         "FWD-CONTINUATION-COUNTED", m_admit),
        ("[mutant] append-once removed", "FWD-APPEND-TWICE", m_twice),
        ("a planted re-ride bending an appended row by 1e-9 R at the next refresh",
         "REFRESH-CHANGED", m_changed),
        ("a refresh at a pin before the last refresh", "only moves forward", backwards),
        ("a planted same-pin refresh whose re-ride closes the campaign OPEN at P1 (it would "
         "append at a pin already refreshed)", "SAME pin", same_pin_closes),
        ("[mutant] the P-WIN-1 cut read as lag > 16 (planted boundary rows)", "FWD-STAMP",
         lambda: stamp_plant(lambda: mutated(F, "P_WIN_1_CUT", P_WIN_1_TYPED + 1))[0]),
        ("[mutant] the P-WIN-1 shadow read as 8-15 (planted boundary rows)", "FWD-STAMP",
         lambda: stamp_plant(lambda: mutated(F, "P_WIN_1_SHADOW",
                                             (P_WIN_1_SHADOW_TYPED[0] + 1,
                                              P_WIN_1_SHADOW_TYPED[1])))[0]),
        ("[mutant] the P-AGE-1 OLD band read as B3 (planted boundary rows)", "FWD-STAMP",
         lambda: stamp_plant(lambda: mutated(F, "P_AGE_1_OLD", "B3"))[0]),
        ("a continuation still open at the pin relabelled net_r (copy of a planted ledger)",
         "FWD-MARK", cont_relabelled),
        ("--snapshot naming another substrate than the process's", "is not NAIAD_CACHE_DIR",
         other_snapshot),
        ("one digit of the record ledger's genesis tampered (copy)", "CHAIN", tampered),
        ("a middle line deleted from a planted ledger (copy)", "CHAIN", deleted),
    ])


def fwd_real():
    bad, lines = [], []
    raw_ = (FWD / F.LEDGER).read_bytes()
    cb, objs = F.verify_chain(raw_)
    bad += cb
    g = objs[0] if objs else {}
    if int(g.get("opening_ms", -1)) != OPENING:
        bad.append(f"FWD-OPENING: genesis opens {g.get('opening_iso')}, not 2026-09-21T16:00:00Z")
    refs = [o for o in objs if o.get("kind") == "REFRESH"]
    camps = [o for o in objs if o.get("kind") == "CAMPAIGN"]
    last = refs[-1] if refs else {}
    if int(last.get("pin_ms", -1)) != PIN:
        bad.append("FWD-PIN: the last refresh is not at the TC11 pin")
    if camps:
        bad.append(f"FWD-RECORD: {len(camps)} campaign(s) appended at the TC11 pin (expected 0)")
    bk = last.get("books", {})
    v6c = tuple((x["key"][0], iso(int(x["key"][1])), int(x["direction"]))
                for x in bk.get("v6", {}).get("continuations_not_admitted", []))
    v6o = bk.get("v6", {}).get("open", [])
    o9 = tuple((x["key"][0], iso(int(x["key"][1])), int(x["direction"]))
               for x in bk.get("trg912", {}).get("open", []))
    c9 = bk.get("trg912", {}).get("continuations_not_admitted", [])
    if v6c != FWD_V6_CONTINUATIONS or v6o:
        bad.append(f"FWD-RECORD v6: continuations {v6c} / open {len(v6o)} != typed "
                   f"{FWD_V6_CONTINUATIONS} / 0")
    if o9 != FWD_912_OPEN or c9:
        bad.append(f"FWD-RECORD 9/12: open {o9} / continuations {len(c9)} != typed "
                   f"{FWD_912_OPEN} / 0")
    for b in ("v6", "trg912"):
        if bk.get(b, {}).get("n_appended_total") != 0 or \
                bk.get(b, {}).get("status") != "UNSCORED (n 0 < 30)":
            bad.append(f"FWD-RECORD {b}: n / status {bk.get(b, {}).get('n_appended_total')} / "
                       f"{bk.get(b, {}).get('status')}")
    fresh = fwd_dir("fresh")
    F.refresh(fresh, PIN, OPENING)
    same = (fresh / F.LEDGER).read_bytes() == raw_ and \
        (fresh / F.REPORT).read_bytes() == (FWD / F.REPORT).read_bytes()
    if not same:
        bad.append("FWD-FRESH: a fresh refresh at the TC11 pin is not the ledger of record")
    lines.append(f"(a) the ledger of record: {len(objs)} lines, chain verifies {not cb}; opens "
                 f"2026-09-21T16:00Z; last refresh at the TC11 pin; 0 appended; v6 continuation "
                 f"{v6c} listed, not counted; 9/12 OPEN {o9} (marked "
                 f"{[x.get('net_r_marked_to_pin') for x in bk.get('trg912', {}).get('open', [])]}"
                 f"), not appended; both UNSCORED (n 0 < 30); a fresh refresh == the record byte "
                 f"for byte: {same}")
    op = _ms(FWD_PLANT_OPENING)
    p1, p2, tgt = plant_pins(op)
    d = fwd_dir("plant")
    seq_bad = fwd_sequence(d, op, (p1, p2, PIN))
    bad += seq_bad
    objs2 = F.verify_chain((d / F.LEDGER).read_bytes())[1]
    refs2 = [o for o in objs2 if o["kind"] == "REFRESH"]
    tg_open = any([x["key"][0], int(x["key"][1])] == [tgt[1], tgt[2]]
                  for x in refs2[0]["books"][tgt[0]]["open"]) if refs2 else False
    tg_app = [o for o in objs2 if o["kind"] == "CAMPAIGN" and o["book"] == tgt[0]
              and [o["key"][0], int(o["key"][1])] == [tgt[1], tgt[2]]]
    once = len(tg_app) == 1 and int(tg_app[0]["appended_at_pin_ms"]) == p2
    if not (tg_open and once):
        bad.append(f"FWD-ONCE-WHEN-CLOSED {tgt}: OPEN at P1 {tg_open}, appended once at P2 {once}")
    before = (d / F.LEDGER).read_bytes()
    R2 = F.refresh(d, PIN, op)
    idem = (not R2["written"]) and (d / F.LEDGER).read_bytes() == before
    if not idem:
        bad.append("FWD-IDEMPOTENT: a same-pin refresh changed the ledger")
    # the gate stamps at their boundaries (verifier m6) and the marks (verifier m8)
    sb, planted = stamp_plant()
    bad += sb
    mk = mark_findings(objs) + mark_findings(objs2)
    dc, still = cont_plant()
    cobjs = F.verify_chain((dc / F.LEDGER).read_bytes())
    mk += cobjs[0] + mark_findings(cobjs[1])
    want_c = ("trg912",) + (FWD_912_OPEN[0][0], FWD_912_OPEN[0][1])
    if want_c not in still:
        mk.append(f"FWD-MARK: the planted opening {FWD_CONT_PLANT_OPENING} does not list the 9/12 "
                  f"{FWD_912_OPEN[0][0]} campaign as a continuation still open at the pin "
                  f"({still}) — the check would be vacuous")
    row_c = [ln for ln in (dc / F.REPORT).read_text(encoding="utf-8").split("\n")
             if ln.startswith("| continuations entered at/before the opening")]
    if len(row_c) != 1 or "marked to the pin" not in row_c[0]:
        mk.append("FWD-MARK: the planted ledger's report does not print the open continuation "
                  "as marked to the pin")
    bad += mk
    n_app = {b: sum(1 for o in objs2 if o["kind"] == "CAMPAIGN" and o["book"] == b)
             for b in ("v6", "trg912")}
    per_pin = [(iso(o["pin_ms"]), len(o["books"]["v6"]["appended_now"]),
                len(o["books"]["trg912"]["appended_now"]),
                len(o["books"]["v6"]["open"]) + len(o["books"]["trg912"]["open"])) for o in refs2]
    lines.append(f"(b) planted opening {FWD_PLANT_OPENING} refreshed at {iso(p1)} / {iso(p2)} / "
                 f"the TC11 pin (P1 chosen inside {tgt[0]} {tgt[1]} {iso(tgt[2])}'s life): "
                 f"(pin, v6 appended now, 9/12 appended now, OPEN) {per_pin}; appended "
                 f"{n_app}, each exactly once, none OPEN, none entered at/before the opening, "
                 f"the set and every row == the frozen books' own (net, exit, prices, P-AGE-1 "
                 f"band / P-WIN-1 lag stamps, haircut at the typed tier), chain verified after "
                 f"every refresh: {not seq_bad}; the OPEN-at-P1 campaign appended exactly once, "
                 f"at P2: {tg_open and once}; a same-pin refresh writes nothing: {idem}")
    lines.append(f"(c) gate stamps on {len(planted)} planted v6 rows (lag, band) "
                 f"{list(STAMP_PLANT)}: P-WIN-1 refuses iff lag >= {P_WIN_1_TYPED}, shadow iff "
                 f"{P_WIN_1_SHADOW_TYPED[0]}-{P_WIN_1_SHADOW_TYPED[1]}, P-AGE-1 refuses iff "
                 f"{P_AGE_1_OLD_TYPED}: {not sb}; (d) every OPEN entry and continuation on the "
                 f"record, the planted sequence and a planted opening {FWD_CONT_PLANT_OPENING} "
                 f"(continuations still open at the pin: {still}) is marked to the pin iff "
                 f"still open (net_r_marked_to_pin, never net_r), the report prints it so, "
                 f"chain verifies: {not mk}" + (f"; findings {(sb + mk)[:3]}" if sb or mk else ""))
    lines.append(f"record ledger {len(raw_)} B sha {sha_bytes(raw_)[:16]}…, head "
                 f"{objs[-1]['line_sha256'][:16] if objs else '?'}…" + (f"; findings {bad[:4]}"
                                                                       if bad else ""))
    return (not bad), lines


# ════════════════════════════════════════════════════════════════════ F-KEY
def canon_csv(df: pd.DataFrame) -> bytes:
    """THIS file's canonical CSV (the recipe typed in the interface), own code."""
    d = df.sort_values(["symbol", "entry_close_ms"], kind="mergesort")
    rows = [",".join(REQ_ORDER)]
    for rec in d[list(REQ_ORDER)].to_dict("records"):
        vals = []
        for c in REQ_ORDER:
            v = rec[c]
            t = REQUIRED_TYPED[c]
            vals.append(repr(float(v)) if t == "float64" else str(int(v)) if t in ("int64", "int8")
                        else str(v))
        rows.append(",".join(vals))
    return ("\n".join(rows) + "\n").encode("utf-8")


def _dtype_ok(s: pd.Series, t: str) -> bool:
    if t == "str":
        return s.dtype == object and all(isinstance(x, str) for x in s)
    return str(s.dtype) == t


def regbook_findings(arm: str, df: pd.DataFrame, sc: dict) -> list[str]:
    out = []
    kind, ruler, era_scope, lane = ARMS_TYPED[arm]
    for c, t in REQUIRED_TYPED.items():
        if c not in df.columns:
            out.append(f"KEY-COL {arm}: required column {c} absent")
        elif not _dtype_ok(df[c], t):
            out.append(f"KEY-DTYPE {arm}: {c} is {df[c].dtype}, not {t}")
        elif df[c].isna().any():
            out.append(f"KEY-NULL {arm}: {int(df[c].isna().sum())} null(s) in {c}")
    if out:
        return out
    if df.duplicated(["symbol", "entry_close_ms"]).any():
        out.append(f"KEY-DUP {arm}: a duplicated (symbol, entry_close_ms)")
    if arm in ("scored", "base") and df.duplicated(["symbol", "entry_ms"]).any():
        out.append(f"KEY-DUP {arm}: a duplicated (symbol, entry_ms)")
    miss = [k for k in SIDECAR_TYPED if k not in sc]
    if miss:
        out.append(f"KEY-SIDECAR {arm}: keys absent {miss}")
    if sc.get("n") != len(df) or sc.get("sum_net_r") != float(df["net_r"].sum()) \
            or sc.get("book_sha256") != sha_bytes(canon_csv(df)):
        out.append(f"KEY-SIDECAR {arm}: n / sum_net_r / book_sha256 disagree with the parquet "
                   f"({sc.get('n')}/{len(df)}; {sc.get('sum_net_r')!r}/"
                   f"{float(df['net_r'].sum())!r}; {str(sc.get('book_sha256'))[:12]}…/"
                   f"{sha_bytes(canon_csv(df))[:12]}…)")
    if (sc.get("registration"), sc.get("arm"), sc.get("kind"), sc.get("ruler"),
            sc.get("era_scope"), tuple(sc.get("panel", ()))) != \
            ("P-RELAY-1", arm, kind, ruler, era_scope, CLASSIC5_TYPED):
        out.append(f"KEY-SIDECAR {arm}: identity fields are not the typed ones")
    if kind == "tierE" and any(sc.get(k) != v for k, v in COLLAR_TYPED.items()):
        out.append(f"KEY-COLLAR {arm}: the Tier-E sidecar lacks the collar")
    era = np.where(df["entry_close_ms"].to_numpy(np.int64) <= ERA_CUT, "tuning", "holdout")
    if not np.array_equal(era, df["era"].to_numpy(str)):
        out.append(f"KEY-ERA {arm}: era is not by the entry close against {ERA_CUT}")
    if era_scope != "full" and set(df["era"]) - {era_scope}:
        out.append(f"KEY-ERA {arm}: rows outside the {era_scope} slice")
    hc = df["net_r"].to_numpy(float) - df["fee_r"].to_numpy(float) * np.array(
        [SLIP_TYPED[s] for s in df["symbol"]]) / TAKER_TYPED
    if not np.array_equal(hc, df["haircut_net_r"].to_numpy(float)):
        out.append(f"KEY-HAIRCUT {arm}: haircut_net_r != net_r - fee_r x slip(typed tier) / 5")
    if set(df["lane"]) != {lane}:
        out.append(f"KEY-LANE {arm}: lanes {sorted(set(df['lane']))} != {{'{lane}'}}")
    lack = [c for c in AS_OF_TYPED if c not in df.columns or df[c].isna().any()]
    if lack:
        out.append(f"KEY-ASOF {arm}: as-of stamp(s) absent/null {lack}")
    return out


def stage_findings(frames: dict, root: Path) -> list[str]:
    out = []
    for name, df in frames.items():
        for k, v in COLLAR_TYPED.items():
            if k not in df.columns or set(df[k]) != {v}:
                out.append(f"KEY-COLLAR {name}: collar column {k} absent or not {v!r}")
        vc = [c for c in df.columns if c in VERDICT_COLUMNS]
        if vc:
            out.append(f"KEY-VERDICT {name}: a verdict column {vc} on a Tier-E table")
        if df.duplicated(STAGE_KEYS_TYPED[name]).any():
            out.append(f"KEY-DUP {name}: duplicated {STAGE_KEYS_TYPED[name]}")
    ok, lines = TP.check_keys(root)
    if not ok:
        out += [f"KEY-CHECK {x}" for x in lines if x.startswith("[BAD]")]
    return out


def _regs() -> dict:
    return {a: (reg(a), side(a)) for a in ARMS_TYPED}


def _stage_frames() -> dict:
    return {n: pd.read_parquet(str(OUT / f"{n}.parquet")) for n in STAGE_KEYS_TYPED}


def key_break():
    R = _regs()
    sc, sd = R["scored"]
    tl, tls = R["tierE__late_relay"]

    def dup():
        return regbook_findings("scored", pd.concat([sc, sc.iloc[[4]]], ignore_index=True), sd)

    def nul():
        d = sc.copy()
        d.loc[d.index[5], "net_r"] = np.nan
        return regbook_findings("scored", d, sd)

    def dt():
        d = sc.copy()
        d["direction"] = d["direction"].astype("int64")
        return regbook_findings("scored", d, sd)

    def sum_off():
        s2 = dict(sd)
        s2["sum_net_r"] = float(sd["sum_net_r"]) + 1e-9
        return regbook_findings("scored", sc, s2)

    def bent():
        d = sc.copy()
        d.loc[d.index[6], "gross_r"] = float(d.loc[d.index[6], "gross_r"]) + 1e-12
        return regbook_findings("scored", d, sd)

    def collar():
        s2 = {k: v for k, v in tls.items() if k != "selection_not_a_result"}
        return regbook_findings("tierE__late_relay", tl, s2)

    def verdict():
        fr = _stage_frames()
        fr["relay_era_slices"] = fr["relay_era_slices"].assign(verdict="SUPPORTED")
        with tempfile.TemporaryDirectory(prefix="f-key-") as td:
            for n, df in fr.items():
                df.to_parquet(str(Path(td) / f"{n}.parquet"), index=False)
            shutil.copy(str(OUT / S.MANIFEST), str(Path(td) / S.MANIFEST))
            return stage_findings(fr, Path(td))

    def tier():
        d = sc.copy()
        m = d["symbol"] == "SOLUSDT"
        d.loc[m, "haircut_net_r"] = d.loc[m, "net_r"] - d.loc[m, "fee_r"] * 2.0 / 5.0
        return regbook_findings("scored", d, sd)

    return plants([
        ("a duplicated relay row (copy)", "KEY-DUP", dup),
        ("net_r nulled on one row (copy)", "KEY-NULL", nul),
        ("direction widened to int64 (copy)", "KEY-DTYPE", dt),
        ("the sidecar's sum_net_r moved 1e-9 (copy)", "KEY-SIDECAR", sum_off),
        ("one gross_r bent 1e-12 — the book sha must move (copy)", "KEY-SIDECAR", bent),
        ("the collar dropped from a Tier-E sidecar (copy)", "KEY-COLLAR", collar),
        ("a verdict column on a stage table (temp root)", "KEY-VERDICT", verdict),
        ("SOL's haircut charged at tier A (copy)", "KEY-HAIRCUT", tier),
    ])


def key_real():
    R = _regs()
    bad = []
    for a, (df, sc) in R.items():
        bad += regbook_findings(a, df, sc)
    st = json.loads((REGDIR / "STATUS.json").read_text(encoding="utf-8"))
    if (st.get("registration"), st.get("status"), tuple(st.get("arms", ()))) != \
            ("P-RELAY-1", "BUILT", tuple(ARMS_TYPED)):
        bad.append(f"KEY-STATUS: {st.get('status')} arms {st.get('arms')}")
    fr = _stage_frames()
    bad += stage_findings(fr, OUT)
    man = json.loads((OUT / S.MANIFEST).read_text(encoding="utf-8"))
    csha = {n: TB._content_sha(df) for n, df in fr.items()}
    if csha != man.get("sha") or man.get("keys") != STAGE_KEYS_TYPED:
        bad.append("KEY-MANIFEST: stage content shas / keys disagree with the manifest")
    counts = ", ".join(f"{a} {len(R[a][0])}" for a in ARMS_TYPED)
    return (not bad), (f"regbooks ({counts}): the 16 required columns at the typed dtypes, no "
                       f"null, unique (symbol, entry_close_ms) (and (symbol, entry_ms) on "
                       f"scored/base), sidecars carry every typed key with n / sum_net_r / "
                       f"book_sha256 == this file's own canonical CSV, era by the entry close, "
                       f"haircut at the typed tiers, lanes typed, the Tier-E collar, 9 as-of "
                       f"stamps; STATUS.json BUILT with the typed arms; the 5 stage tables "
                       f"collared, no verdict column, TP.check_keys GREEN, manifest shas == "
                       f"content: {not bad}" + (f"; findings {bad[:4]}" if bad else ""))


# ═══════════════════════════════════════════════════════════════════ F-GRID
_REF: dict = {}


def grid_ref() -> dict:
    """This file's referee for the grid VALUES, once: the own record and late rows of
    every window (against the regbooks of record), v6's slot law, and the books."""
    if not _REF:
        sc, lt, base = reg("scored"), reg("tierE__late_relay"), reg("base")
        rec, _ = own_rows(sc, late=False)
        lat, _ = own_rows(lt, late=True)
        v6, _ = own_v6(base)
        camp = {(str(r.symbol), int(r.direction), int(r.arm_ms)): float(r.net_r)
                for r in base.itertuples()}
        _REF.update({"rec": rec, "late": lat, "v6_net": {k: camp[k] for k, c in v6.items()
                                                         if c == "entered" and k in camp},
                     "books": {"scored (relay)": sc, "base (v6)": base,
                               "tierE__late_relay": lt}})
    return _REF


def _cell(v):
    """A grid cell as a plain value, NA / NaN -> NaN."""
    v = _nz(v)
    return float("nan") if v is None else v


def _same(a, b) -> bool:
    """Equal, NaN == NaN (a declared empty statistic)."""
    fa = isinstance(a, float) and a != a
    fb = isinstance(b, float) and b != b
    return (fa and fb) or (not fa and not fb and a == b)


def grid_value_findings(fr: dict, ref: dict) -> list[str]:
    """GRID-STAT / GRID-LEAD / GRID-ERA: every value re-derived here (verifier m3)."""
    out = []
    W = own_windows_all()
    g = fr["relay_disposition_grid"]
    tab = {str(r["cell"]): r for r in g.to_dict("records")}
    for var, rows in (("record", ref["rec"]), ("late", ref["late"])):
        for code in CODES_TYPED + ("ALL",):
            ks = [k for k, o in rows.items() if code == "ALL" or o["disposition"] == code]
            rel = [rows[k]["relay_net_r"] for k in ks if rows[k]["disposition"] == "RELAYED"]
            if any(x is None for x in rel):
                out.append(f"GRID-STAT {var}|{code}: a relayed window with no book row")
                rel = [x for x in rel if x is not None]
            v = [ref["v6_net"][k] for k in ks if k in ref["v6_net"]]
            own_c = {"n_windows": len(ks),
                     "n_lag0": sum(1 for k in ks if W[k]["lag"] == 0),
                     "relay_n": sum(1 for k in ks if rows[k]["disposition"] == "RELAYED"),
                     "relay_sum_net_r": _r6(math.fsum(rel)) if rel else 0.0,
                     "v6_entered_n": len(v),
                     "v6_sum_net_r": _r6(math.fsum(v)) if v else 0.0,
                     "v6_mean_net_r": _r6(math.fsum(v) / len(v)) if v else float("nan")}
            t = tab.get(f"{var}|{code}")
            if t is None:
                continue                   # GRID-WHOLE names it
            diff = {c: (_cell(t[c]), own_c[c]) for c in own_c
                    if not _same(_cell(t[c]), own_c[c])}
            if diff:
                out.append(f"GRID-STAT {var}|{code}: (table, own) {diff}")
    # the lead of every relay over its own trigger, the values table and the typed bins
    win = fr["relay_windows"]
    for r in win.itertuples():
        k = (str(r.symbol), int(r.direction), int(r.arm_ms))
        o = ref["rec"].get(k)
        if o is None:
            continue
        for c in ("lead_1h", "lead_4h"):
            if _nz(getattr(r, c)) != o[c]:
                out.append(f"GRID-LEAD {k[0]} {k[1]:+d} armed {iso(k[2])}: table {c} "
                           f"{_nz(getattr(r, c))} != own {o[c]}")
    vals, na = Counter(), 0
    for k, o in ref["rec"].items():
        if o["disposition"] != "RELAYED":
            continue
        if o["lead_4h"] is None:
            na += 1
            continue
        for kind, col in LEAD_COL_TYPED.items():
            vals[(kind, int(o[col]))] += 1
    lv = fr["relay_lead_values"]
    tv = {(str(a), int(b)): int(n) for a, b, n in zip(lv["lead_kind"], lv["lead_value"], lv["n"])}
    if tv != dict(vals):
        dk = sorted(set(tv) ^ set(vals) | {x for x in set(tv) & set(vals) if tv[x] != vals[x]})
        out.append(f"GRID-LEAD values: the table's {len(tv)} (kind, value) counts != own "
                   f"{len(vals)} (differ at {dk[:3]})")
    ob = {(kind, nm): 0 for kind, edges in LEAD_EDGES_TYPED.items() for nm, _, _ in edges}
    ob.update({(kind, LEAD_NA_TYPED): na for kind in LEAD_EDGES_TYPED})
    for (kind, val), n in vals.items():
        nm = next((nm for nm, a, b in LEAD_EDGES_TYPED[kind]
                   if val >= a and (b is None or val <= b)), None)
        if nm is None:
            out.append(f"GRID-LEAD bins: {kind} value {val} lies in no typed bin")
            continue
        ob[(kind, nm)] += n
    lb = fr["relay_lead_bins"]
    tb = {(str(a), str(b)): int(n) for a, b, n in zip(lb["lead_kind"], lb["bin"], lb["n"])}
    if tb != ob:
        dk = sorted(x for x in set(tb) | set(ob) if tb.get(x) != ob.get(x))
        out.append(f"GRID-LEAD bins: (table, own) differ at "
                   f"{[(x, tb.get(x), ob.get(x)) for x in dk[:3]]}")
    # the era slices from the regbooks, by the own era law and the typed haircut tier
    es = {str(r["cell"]): r for r in fr["relay_era_slices"].to_dict("records")}
    for arm, df in ref["books"].items():
        era = np.where(df["entry_close_ms"].to_numpy(np.int64) <= ERA_CUT, "tuning", "holdout")
        net = df["net_r"].to_numpy(float)
        hc = net - df["fee_r"].to_numpy(float) * np.array(
            [SLIP_TYPED[x] for x in df["symbol"]]) / TAKER_TYPED
        for e in ("tuning", "holdout", "full"):
            m = np.ones(len(df), bool) if e == "full" else (era == e)
            n = int(m.sum())
            own_e = {"n": n,
                     "sum_net_r": _r6(math.fsum(net[m])) if n else 0.0,
                     "mean_net_r": _r6(math.fsum(net[m]) / n) if n else float("nan"),
                     "sum_haircut_net_r": _r6(math.fsum(hc[m])) if n else 0.0,
                     "win_pct": _r6(100.0 * float((net[m] > 0).sum()) / n) if n
                     else float("nan")}
            t = es.get(f"{arm}|{e}")
            if t is None:
                continue                   # GRID-WHOLE names it
            diff = {c: (_cell(t[c]), own_e[c]) for c in own_e
                    if not _same(_cell(t[c]), own_e[c])}
            if diff:
                out.append(f"GRID-ERA {arm}|{e}: (table, own) {diff}")
    return out


def grid_findings(fr: dict, ref: dict | None = None) -> list[str]:
    out = grid_value_findings(fr, grid_ref() if ref is None else ref)
    g = fr["relay_disposition_grid"]
    decl = [f"{v}|{c}" for v in ("record", "late") for c in CODES_TYPED + ("ALL",)]
    ok, lines = TP.grid_whole(decl, g, "cell", require_cols=("n_windows",),
                              label="disposition grid")
    if not ok:
        out += [f"GRID-WHOLE disposition: {x}" for x in lines if "[BAD]" in x or "BAD" in x] \
            or ["GRID-WHOLE disposition: not whole"]
    for v in ("record", "late"):
        x = g[g["variant"] == v]
        if int(x.loc[x["disposition"] != "ALL", "n_windows"].sum()) != \
                int(x.loc[x["disposition"] == "ALL", "n_windows"].sum()):
            out.append(f"GRID-PARTITION {v}: the codes do not sum to ALL")
    nan_bad = g[g["v6_mean_net_r"].isna() & (g["nan_reason"].fillna("") == "")]
    nan_bad2 = g[g["v6_mean_net_r"].isna() != (g["v6_entered_n"] == 0)]
    if len(nan_bad) or len(nan_bad2):
        out.append(f"GRID-NAN: {len(nan_bad)} silent NaN(s), {len(nan_bad2)} NaN not iff n == 0")
    lb = fr["relay_lead_bins"]
    decl_l = [f"{k}|{b}" for k, bs in LEAD_BINS_TYPED.items() for b in bs]
    ok, lines = TP.grid_whole(decl_l, lb, "cell", require_cols=("n",), label="lead bins")
    if not ok:
        out.append("GRID-WHOLE lead bins: " + " · ".join(lines[:3]))
    es = fr["relay_era_slices"]
    ok, lines = TP.grid_whole(list(ERA_CELLS_TYPED), es, "cell", require_cols=("n",),
                              label="era slices")
    if not ok:
        out.append("GRID-WHOLE era slices: " + " · ".join(lines[:3]))
    if len(es[es["mean_net_r"].isna() != (es["n"] == 0)]):
        out.append("GRID-NAN era slices: a NaN mean not iff n == 0")
    for name, df in fr.items():
        if [c for c in df.columns if c in VERDICT_COLUMNS]:
            out.append(f"GRID-VERDICT {name}: a verdict column")
        if any(k not in df.columns for k in COLLAR_TYPED):
            out.append(f"GRID-COLLAR {name}: the collar is absent")
    return out


def grid_break():
    fr = _stage_frames()

    def w(name, df):
        d = dict(fr)
        d[name] = df
        return grid_findings(d)

    g = fr["relay_disposition_grid"]
    lv, es = fr["relay_lead_values"], fr["relay_era_slices"]

    def lead_from_arm():
        d = fr["relay_windows"].copy()
        m = (d["disposition"] == "RELAYED") & d["trigger_i"].notna()
        d.loc[m, "lead_4h"] = (d.loc[m, "trigger_i"] - d.loc[m, "arm_i"]).astype("Int64")
        return d
    return plants([
        ("a zero-count disposition cell dropped", "GRID-WHOLE",
         lambda: w("relay_disposition_grid",
                   g.drop(index=g.index[g["n_windows"] == 0][0]).reset_index(drop=True))),
        ("an undeclared lead bin added", "GRID-WHOLE",
         lambda: w("relay_lead_bins", pd.concat([fr["relay_lead_bins"], fr["relay_lead_bins"]
                                                .iloc[[0]].assign(cell="lead_4h_bars|99")],
                                               ignore_index=True))),
        ("a silent NaN (nan_reason emptied)", "GRID-NAN",
         lambda: w("relay_disposition_grid", g.assign(nan_reason=""))),
        ("a verdict column on the era slices", "GRID-VERDICT",
         lambda: w("relay_era_slices", fr["relay_era_slices"].assign(verdict="SUPPORTED"))),
        ("the collar removed from the lead values", "GRID-COLLAR",
         lambda: w("relay_lead_values", fr["relay_lead_values"].drop(columns=["tier"]))),
        ("the partition broken (a code's count +1)", "GRID-PARTITION",
         lambda: w("relay_disposition_grid", g.assign(n_windows=np.where(
             g["cell"] == "record|RELAYED", g["n_windows"] + 1, g["n_windows"])))),
        ("the relay's 4h lead read from the arm bar, not its entry bar J (copy of the "
         "windows table)", "GRID-LEAD", lambda: w("relay_windows", lead_from_arm())),
        ("one lead value's count moved to the next value (copy)", "GRID-LEAD",
         lambda: w("relay_lead_values", lv.assign(lead_value=np.where(
             lv.index == lv.index[0], lv["lead_value"] + 1, lv["lead_value"])))),
        ("the record|RELAYED relay ΣR x 1.01 (copy)", "GRID-STAT",
         lambda: w("relay_disposition_grid", g.assign(relay_sum_net_r=np.where(
             g["cell"] == "record|RELAYED", g["relay_sum_net_r"] * 1.01,
             g["relay_sum_net_r"])))),
        ("the v6 ΣR of record|MISS_TRIGGER_FIRST bent 1e-6 (copy)", "GRID-STAT",
         lambda: w("relay_disposition_grid", g.assign(v6_sum_net_r=np.where(
             g["cell"] == "record|MISS_TRIGGER_FIRST", g["v6_sum_net_r"] + 1e-6,
             g["v6_sum_net_r"])))),
        ("an era slice's Σ haircut R bent 1e-6 (copy)", "GRID-ERA",
         lambda: w("relay_era_slices", es.assign(sum_haircut_net_r=np.where(
             es.index == es.index[0], es["sum_haircut_net_r"] + 1e-6,
             es["sum_haircut_net_r"])))),
    ])


def grid_real():
    fr = _stage_frames()
    bad = grid_findings(fr)
    g = fr["relay_disposition_grid"]
    ref = grid_ref()
    rel = [o for o in ref["rec"].values() if o["disposition"] == "RELAYED"]
    trig = [o for o in rel if o["lead_4h"] is not None]
    return (not bad), (f"disposition grid {len(g)} cells == typed 2 x ({len(CODES_TYPED)} codes "
                       f"+ ALL), zero cells included, codes partition ALL in both variants; lead "
                       f"bins {len(fr['relay_lead_bins'])} == typed; era slices "
                       f"{len(fr['relay_era_slices'])} == typed; every NaN statistic iff n == 0 "
                       f"and carries its nan_reason; collared, no verdict column; VALUES re-derived "
                       f"here at {TABLE_DP} dp — every grid cell's n / lag-0 n / relay n / relay ΣR "
                       f"/ v6 n / v6 ΣR / v6 mean from the own record and late dispositions (the "
                       f"books' net R, v6's slot law on the base book), the lead of the "
                       f"{len(trig)} triggered relays over the own trigger (4h: trigger bar − J; "
                       f"1h: (trigger close − entry) / 1h; {sum(1 for o in trig if o['lead_4h'] >= 20)} "
                       f"lead by >= 20 4h bars; {len(rel) - len(trig)} relays with no trigger), "
                       f"the lead values ({len(fr['relay_lead_values'])} rows) and typed bins, "
                       f"every era slice from the regbooks (own era law, typed haircut tier): "
                       f"{not bad}" + (f"; findings {bad[:4]}" if bad else ""))


# ════════════════════════════════════════════════════════════════════ F-DET
def _files(d: Path, names) -> dict:
    return {n: (d / n).read_bytes() for n in names if (d / n).is_file()}


def det_dirs() -> tuple[Path, Path]:
    if RUN_ROOT.resolve() == OUT.resolve():
        return S.DET_ROOT, F.DET_ROOT
    return RUN_ROOT / S.DET_ROOT.name, RUN_ROOT / F.DET_ROOT.name


def canon() -> dict:
    return {"stage": _files(OUT, STAGE_FILES_TYPED), "reg": _files(REGDIR, REG_FILES_TYPED),
            "fwd": _files(FWD, FWD_FILES_TYPED)}


def det_build(seed: int, hashorder: bool = False) -> tuple[int, dict]:
    ds, dfw = det_dirs()
    tag = f"{'hashorder' if hashorder else 'seed'}_{seed}"
    a, b = ds / tag, dfw / tag
    for p in (a, b):
        if p.exists():
            shutil.rmtree(p)
        p.parent.mkdir(parents=True, exist_ok=True)
    env = dict(_env(), PYTHONHASHSEED=str(seed))
    if not hashorder:
        c1 = [PY, "-B", str(ROOT / "scripts" / "tierc11_stage_t_relay.py"), f"--out-dir={a}"]
    else:
        code = (f"import sys\nsys.dont_write_bytecode = True\n"
                f"sys.path.insert(0, {str(ROOT)!r})\nsys.path.insert(0, {str(ROOT / 'scripts')!r})\n"
                f"from pathlib import Path\nimport tierc11_stage_t_relay as S\n"
                f"d = Path({str(a)!r})\nS.build(d)\np = d / 'stage_t_relay' / S.REPORT\n"
                f"p.write_text(p.read_text() + 'set order: ' + ','.join(set(S.E.PANEL17)) + '\\n')\n")
        c1 = [PY, "-B", "-c", code]
    r1 = subprocess.run(c1, env=env, capture_output=True, text=True, cwd=str(ROOT), timeout=1800)
    rc = r1.returncode
    if not hashorder:
        r2 = subprocess.run([PY, "-B", str(ROOT / "scripts" / "tierc11_forward_ledger.py"),
                             "--refresh", "--snapshot", str(SNAP), f"--out-dir={b}"],
                            env=env, capture_output=True, text=True, cwd=str(ROOT), timeout=1800)
        rc = rc or r2.returncode
    return rc, {"stage": _files(a / "stage_t_relay", STAGE_FILES_TYPED),
                "reg": _files(a / "regbooks" / S.REG_ID, REG_FILES_TYPED),
                "fwd": _files(b, FWD_FILES_TYPED) if not hashorder else {}}


def det_findings(x: tuple, y: tuple, can: dict, parts=("stage", "reg", "fwd")) -> list[str]:
    out = []
    for lab, (rc, _) in (("seed 1", x), (f"seed {SEED}", y)):
        if rc != 0:
            out.append(f"{lab} exit {rc}")
    typed = {"stage": STAGE_FILES_TYPED, "reg": REG_FILES_TYPED, "fwd": FWD_FILES_TYPED}
    for part in parts:
        for lab, fs in (("seed 1", x[1][part]), (f"seed {SEED}", y[1][part]),
                        ("record", can[part])):
            if sorted(fs) != sorted(typed[part]):
                out.append(f"{lab} {part}: file set {len(fs)} != typed {len(typed[part])}")
        for lab, p, q in ((f"seed 1 vs seed {SEED}", x[1][part], y[1][part]),
                          ("seed 1 vs record", x[1][part], can[part])):
            for n in sorted(set(p) & set(q)):
                if p[n] != q[n]:
                    out.append(f"{lab}: {part}/{n} bytes differ")
                if n.endswith(".parquet"):
                    ca = TB._content_sha(pd.read_parquet(io.BytesIO(p[n])))
                    cb = TB._content_sha(pd.read_parquet(io.BytesIO(q[n])))
                    if ca != cb:
                        out.append(f"{lab}: {part}/{n} content sha differs")
    return out


def det_break():
    can = canon()
    bent = copy.deepcopy(can)
    md = bytearray(bent["stage"]["STAGE_T_RELAY.md"])
    md[len(md) // 2] ^= 0x01
    bent["stage"]["STAGE_T_RELAY.md"] = bytes(md)

    def float_moved():
        d = pd.read_parquet(io.BytesIO(can["reg"]["scored.parquet"]))
        d.loc[d.index[0], "net_r"] = float(d["net_r"].iloc[0]) + 1e-6
        buf = io.BytesIO()
        d.to_parquet(buf, index=False)
        c2 = copy.deepcopy(can)
        c2["reg"]["scored.parquet"] = buf.getvalue()
        return det_findings((0, c2), (0, c2), can)

    def hashorder():
        o = {s: det_build(s, hashorder=True) for s in DET_SEEDS}
        return [x for x in det_findings(o[1], o[SEED], o[1][1], parts=("stage",))
                if x.startswith(f"seed 1 vs seed {SEED}")]

    return plants([
        ("one byte bent in a copy of STAGE_T_RELAY.md", "STAGE_T_RELAY.md bytes differ",
         lambda: det_findings((0, can), (0, bent), can)),
        ("one net_r moved 1e-6 in a regbook parquet copy", "scored.parquet content sha",
         float_moved),
        ("a hash-order-dependent line (set iteration) under the two seeds",
         f"seed 1 vs seed {SEED}: stage/STAGE_T_RELAY.md bytes differ", hashorder),
    ])


def det_real():
    can = canon()
    o = {s: det_build(s) for s in DET_SEEDS}
    bad = det_findings(o[1], o[SEED], can)
    n = sum(len(v) for v in o[1][1].values())
    shas = sha_bytes(b"".join(v for part in ("stage", "reg", "fwd")
                              for _, v in sorted(o[1][1][part].items())))
    return (not bad), (f"exit {o[1][0]}/{o[SEED][0]}; {n} files (stage {len(STAGE_FILES_TYPED)}, "
                       f"regbooks {len(REG_FILES_TYPED)}, forward {len(FWD_FILES_TYPED)}) == the "
                       f"typed sets in both builds and in the record; every file byte-identical "
                       f"seed 1 == seed {SEED} == record, every parquet content sha equal: "
                       f"{not bad} (concatenated sha {shas[:16]}…)"
                       + (f"; findings {bad[:4]}" if bad else ""))


# ══════════════════════════════════════════════════════════ F-RELAY-INSTANTS
INSTANT_ARMS_TYPED = {"scored": "relay", "tierE__late_relay": "relay",
                      "tierE__tuning_slice": "relay", "tierE__holdout_slice": "relay",
                      "base": "v6", "tierE__miss_v6": "v6"}


def own_harvest_close(row) -> int | None:
    """THIS FILE'S hand harvest law [v6's band harvest; L-T.2 for the relay's J]: the
    CLOSE of the first 4h bar whose close slot fires the harvest, from the raw bars and
    this file's own EMA89 / EMA316 — None when none fires before the exit."""
    sym, d = str(row.symbol), int(row.direction)
    X = own(sym)
    o4, c4, h4, l4, e89, e316 = X["o4"], X["c4"], X["h4"], X["l4"], X["e89"], X["e316"]

    def edge(j: int) -> float:
        return max(e89[j], e316[j]) if d == 1 else min(e89[j], e316[j])

    def outside(px: float, e: float) -> bool:
        return bool(px > e) if d == 1 else bool(px < e)

    ecl, xcl = int(row.entry_close_ms), int(row.exit_close_ms)
    J = int(np.searchsorted(o4, ecl, "left")) - 1          # the 4h bar holding the entry
    xi = int(np.searchsorted(o4, xcl, "left")) - 1         # the 4h bar holding the exit
    last = xi if str(row.exit_reason) == "corridor_end" else xi - 1
    armed = False
    if ecl != int(o4[J]) + H4:                             # a 1h entry strictly inside J
        armed = outside(float(c4[J - 1]), edge(J - 1))
        if J <= last:
            post = np.flatnonzero((X["close1"] > ecl) & (X["close1"] <= int(o4[J]) + H4))
            if post.size:
                ext = float(X["l1"][post].min()) if d == 1 else float(X["h1"][post].max())
                if armed and ((ext <= edge(J)) if d == 1 else (ext >= edge(J))):
                    return int(o4[J]) + H4
    for j in range(J + 1, last + 1):
        if not armed and outside(float(c4[j - 1]), edge(j - 1)):
            armed = True
        if armed and ((float(l4[j]) <= edge(j)) if d == 1 else (float(h4[j]) >= edge(j))):
            return int(o4[j]) + H4
    return None


def instant_findings(arm: str, df: pd.DataFrame, v6hc: dict | None = None) -> tuple[list, dict]:
    """Every row's harvest_close_ms against the hand law (and books/ for v6 rows)."""
    out, tally = [], {"rows": len(df), "harvested": 0, "stamped": 0}
    if "harvest_close_ms" not in df.columns:
        return [f"INSTANT-HARVEST: {arm} carries no harvest_close_ms column"], tally
    if str(df["harvest_close_ms"].dtype) != "Int64":
        out.append(f"INSTANT-HARVEST: {arm}.harvest_close_ms dtype {df['harvest_close_ms'].dtype}"
                   f" != Int64")
    for r in df.itertuples(index=False):
        got = None if pd.isna(r.harvest_close_ms) else int(r.harvest_close_ms)
        want = own_harvest_close(r)
        tag = f"{arm} {r.symbol} {iso(int(r.entry_close_ms))}"
        tally["harvested"] += int(bool(r.harvested))
        tally["stamped"] += int(got is not None)
        if (got is not None) != bool(r.harvested):
            out.append(f"INSTANT-HARVEST: {tag}: harvested {bool(r.harvested)} but "
                       f"harvest_close_ms {got}")
        if got != want:
            out.append(f"INSTANT-HARVEST: {tag}: harvest_close_ms "
                       f"{iso(got) if got else None} != the hand law's "
                       f"{iso(want) if want else None}")
        if v6hc is not None:
            ref = v6hc.get((str(r.symbol), int(r.entry_ms)), "absent")
            if ref != got:
                out.append(f"INSTANT-HARVEST: {tag}: harvest_close_ms {got} != books/"
                           f"v6_campaigns' {ref}")
    return out, tally


def _v6_harvests() -> dict:
    v = pd.read_parquet(str(E.OUT / "books" / "v6_campaigns.parquet"))
    return {(str(a), int(b)): (None if pd.isna(c) else int(c))
            for a, b, c in zip(v["symbol"], v["entry_ms"], v["harvest_close_ms"])}


def instants_break():
    rec = reg("scored")
    hv = np.flatnonzero(rec["harvested"].astype(bool).to_numpy())

    def late():
        d = rec.copy()
        i = d.index[hv[0]]
        d.loc[i, "harvest_close_ms"] = int(d.loc[i, "harvest_close_ms"]) + H4
        return instant_findings("scored (copy)", d)[0]

    def dropped():
        d = rec.copy()
        d.loc[d.index[hv[1]], "harvest_close_ms"] = pd.NA
        return instant_findings("scored (copy)", d)[0]

    def open_stamped():
        orig = S.harvest_close_of

        def at_open(t):
            x = orig(t)
            return None if x is None else x - H4
        with mutated(S, "harvest_close_of", at_open):
            return instant_findings("scored (rebuilt, mutant)", rebuilt_scored())[0]

    return plants([
        ("one harvest instant moved one 4h bar late (a copy of scored)", "INSTANT-HARVEST",
         late),
        ("one harvest instant dropped — nulled on a harvested row (a copy of scored)",
         "INSTANT-HARVEST", dropped),
        ("[mutant] the writer's harvest_close_of stamping the harvest bar's OPEN (a close "
         "event stamped as if intrabar)", "INSTANT-HARVEST", open_stamped),
    ])


def instants_real():
    bad, lines = [], []
    v6hc = _v6_harvests()
    for arm, k in INSTANT_ARMS_TYPED.items():
        f, t = instant_findings(arm, reg(arm), v6hc if k == "v6" else None)
        bad += f
        lines.append(f"{arm} ({k}): {t['rows']} rows, {t['harvested']} harvested, "
                     f"{t['stamped']} stamped")
    rb = rebuilt_scored()
    same = (rb["harvest_close_ms"].astype("Int64").fillna(-1).to_numpy(np.int64).tolist()
            == reg("scored")["harvest_close_ms"].fillna(-1).to_numpy(np.int64).tolist())
    if not same:
        bad.append("INSTANT-HARVEST: the in-process rebuild of scored differs from its record "
                   "on harvest_close_ms")
    return (not bad), lines + [
        f"harvest_close_ms on EVERY row of the six arms == this file's hand harvest law on the "
        f"raw bars (J armed per close[J-1] and touched on the post-entry 1h children for a 1h "
        f"relay; later bars armed by a close outside the own EMA89/316 edge, touched on the "
        f"whole bar; strictly before the exit bar, corridor_end excepted; the bar's CLOSE), NA "
        f"iff not harvested, Int64; the v6 arms == books/v6_campaigns.parquet; rebuild == "
        f"record: {same}" + (f"; findings {bad[:4]}" if bad else "")]


# ═══════════════════════════════════════════════════════════════════ THE TABLE
FIXTURES = (
    ("F-RELAY", "every relay strictly inside its armed window, the first 1h 9/12 cross, "
     "the own stop; >= 3 hand-walked from the raw bars [L-T.2, L-T.3, L-W.0]",
     "a relay closes at/after its window's v6 4h trigger close (or its counter 12/89 / "
     "89/316-against close, or not after its arm close, or after the pin); its 1h bar is not "
     "an own with-trend EMA9/12 cross or not the first; its entry instant / price / stop / R "
     "differ from the own resolution and struct stop as of the last closed 4h bar; a window "
     "holds two relays or an asset two positions; or a hand-walked relay's arm, cross, stop or "
     "entry-bar close slot differs from the module's; or a relay of the late twin breaks the "
     "same law with the trigger bound removed, or either rebuild is not its regbook of record",
     relay_break, relay_real),
    ("F-RELAY-MISS", "every window is exactly one of relayed / missed, with its reason and "
     "what v6 did [L-T.2 miss column]",
     "the windows table is not the own window set (twice-listed, absent, extra), a code is "
     "outside the typed set or differs from the own derivation, a lag-0 window is relayed, "
     "RELAYED windows are not 1:1 the relay book; a row's bound columns (trigger / counter "
     "12/89 / 89/316-against close, lag, earliest bound and kinds), entry columns or LATE "
     "columns differ from the own derivation, or the late RELAYED windows are not 1:1 the late "
     "regbook; a v6 label / column differs from v6's slot law re-derived here and the base "
     "book; tierE__miss_v6 is not the base campaigns in own non-RELAYED windows; or a planted "
     "replay9 code (position open, stop-less) is not labelled by the typed label",
     miss_break, miss_real),
    ("F-FWD", "the forward ledger: append once when closed, OPEN listed, continuation not "
     "counted, a changed re-ride HALTs, the chain verifies [L-T.6]",
     "the record ledger's chain / opening / pin / appended count / OPEN and continuation lists "
     "are not the typed ones or a fresh refresh differs by a byte; on the planted sequence a "
     "campaign is appended twice, an OPEN one appended, a continuation counted, the appended "
     "set or rows differ from the frozen books, the OPEN-then-closed campaign is not appended "
     "exactly at P2, a same-pin refresh writes, or the chain breaks; a planted boundary row "
     "(lag 6/7/15/16/17, band B3/B4) is not stamped by the typed P-WIN-1 / shadow / P-AGE-1 "
     "laws; or an OPEN entry or a continuation still open at the pin is not marked to the pin "
     "(or a closed one is) — on the record, the planted sequence or a planted opening at the "
     "9/12 SOL entry close",
     fwd_break, fwd_real),
    ("F-RELAY-INSTANTS", "the harvest's named-event instant on every arm == this file's "
     "hand harvest law on the raw bars [SR-9; L-R.5, AM-6 — the lanes pass]",
     "an arm lacks harvest_close_ms (Int64), stamps a row that did not harvest or leaves a "
     "harvested row NA, or an instant differs from the hand harvest law (own EMA89/316 edge; "
     "J armed per close[J-1], touched on post-entry children; later bars armed once a close "
     "sat outside, touched on the whole bar; before the exit bar; the bar's CLOSE); a v6 "
     "row differs from books/v6_campaigns; or the rebuild differs from the record",
     instants_break, instants_real),
    ("F-KEY", "the regbook interface and the stage tables: typed columns and dtypes, unique "
     "keys, no nulls, sidecars that re-derive, collars, as-of stamps",
     "a required column absent / mistyped / null, a duplicated key, a sidecar whose typed "
     "keys, n, sum_net_r or book_sha256 (own canonical CSV) disagree, era / haircut / lane "
     "off their typed laws, a Tier-E sidecar without the collar, STATUS.json not the typed "
     "arms, a stage table without the collar, with a verdict column or failing "
     "TP.check_keys, or manifest shas not the content",
     key_break, key_real),
    ("F-GRID", "every grid whole (TP.grid_whole against typed cells) and every value "
     "re-derived here",
     "the disposition grid, lead bins or era slices are not whole against the typed cells, a "
     "NaN statistic is not iff n == 0 or lacks its nan_reason, the codes do not partition "
     "ALL, or a table carries a verdict column / lacks the collar; or a grid cell's counts / "
     "ΣR / v6 sums, a relay's lead (own trigger − own entry bar / instant), the lead values or "
     "bins, or an era slice's n / ΣR / mean / haircut / win % differ from this file's own at "
     "the writer's 6 dp",
     grid_break, grid_real),
    ("F-DET", "two subprocess builds (runner + ledger) under different hash seeds, one set "
     "of bytes",
     "the PYTHONHASHSEED 1 and 20260924 builds differ from each other or from the files of "
     "record in the file set, any byte or any parquet content sha, or either exits nonzero",
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
    say("TIER-C11 STAGE T-relay + FORWARD LEDGER FIXTURES — scripts/tierc11_stage_t_relay.py "
        "and scripts/tierc11_forward_ledger.py — break leg first, RED or void")
    say("=" * 78)
    say(f"seed {SEED} · substrate {SNAP.name} · pin {PIN} · opening {OPENING}")
    for ln in S.READINGS:
        say(ln)
    for fid, title, fails_if, b, r in FIXTURES:
        if not pick or any(q == fid.lower() for q in pick):
            prove(fid, title, fails_if, b, r)
    for t in _TEMPS:
        shutil.rmtree(t, ignore_errors=True)
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
