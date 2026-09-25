#!/usr/bin/env python
"""TIER-C11 · TC11-BOOKS — the two frozen books and the campaign table every
later stage reads [LEANS L-1.6, L-1.7, L-1.3; the L-G.1 / L-G.2 / L-G.3 fields].

Contract of record: exchange/queue/2026-09-24_TC11_APOLLO.md (sha256
bb38e016…, STEP Q b9ed953).  Executor HEPHAESTUS; seed 20260924.  Executor
readings: research_outputs/tierc11/LEANS.md (frozen at 4ed4e67).  Substrate and
TC10 code reach this module ONLY through scripts/tierc11_env.py (`E`): the
range-free shim.  This module is in the L-F.2 DECISION set — it imports no
range module (tierc10_census / tierc10_stamps / tierc10_null / rangefinder).

WHAT IT BUILDS (research_outputs/tierc11/books/)
  v6_journal.parquet       TP.journal_frame of BASE v6 [L-1.6]:
                           TP.run_cell_n(TP.CONTROL_CARD, T9.V6_ROLES, CLASSIC5,
                           lo, hi) over the FULL TC11 corridor (lo, hi) =
                           TP.corridor_n(CLASSIC5) — exactly how TC10 rode its
                           full-corridor control (tierc10_panel.py:2847-2858;
                           tierc10_panel_fixtures.py f_ctrl_a :187-225), the pin
                           now TC11's (hi + 1 == 1790294400000).
  trg912_journal.parquet   TP.journal_frame of the 9/12 book [L-1.6]:
                           T9.replay9(s, TP.CONTROL_CARD, T9.SWEEP_CELLS[-1], lo,
                           hi) per CLASSIC5 asset.  SWEEP_CELLS[-1] must be
                           Roles(name='trigger-9/12', trg_f=9, trg_s=12, every
                           other field v6's) or the build HALTs.
  v6_campaigns.parquet /   ONE ROW PER CAMPAIGN keyed (symbol, entry_ms), the
  trg912_campaigns.parquet fields every later stage needs (see CAMPAIGN_COLUMNS).
  build_manifest.json      content shas, keys, input shas, book shas, anchors.
  BOOKS.md                 the control/descriptive numbers (NOT registration
                           scores: no CI, no p, no verdict word).

WHERE EACH CAMPAIGN FIELD COMES FROM (lineage functions called the way TC10
called them; tierc10_close_* scripts HALT at import, so their SOURCE was read
and the functions underneath are called here, cited):
  arm / entry / exit / R / fees / funding   the Trade replay9 built
                           (tierc9.py:334-452); entry_px = close[entry_i];
                           ms fields are bar OPENs; *_close_ms = open + 4h.
  window_end_i             T9.armings9(sym, roles, lo_i, hi_i) with replay9's own
                           (lo_i, hi_i) (tierc9.py:381-383): the index of the
                           FIRST counter 12/89 cross after arm_i (tierc9.py:
                           181-183) — AS KNOWN AT THE AS-OF (known_window_end):
                           armings9 scans the WHOLE tape, so a cross after the
                           ride's hi_i is a FUTURE bar and is never written;
                           such a window (or one with no cross at all) is OPEN
                           at the as-of and carries hi_i + 1, one past the
                           ride's last bar (window_end_close_ms null, flagged)
                           [repair of verifier MAJOR: latent look-ahead].
  exit_event_ms            L-R.5 intrabar stamp: a STOP exit is an intrabar event,
                           stamped at its bar's OPEN (exit_event_stamp
                           'intrabar_open'); a bell / corridor_end exit is a close
                           event (exit_event_stamp 'close').  exit_close_ms on an
                           intrabar exit is the close-stamped twin — POST-EVENT.
  +1R latch bar            transcribed VERBATIM from tierc10_stamps._plus_1r_bar
                           (tierc10_stamps.py:405-422), with campaign_instants'
                           HALT when it disagrees with the ride's reached_1r
                           (tierc10_stamps.py:553-559).  tierc10_stamps is not
                           imported: L-F.2 bars it from the decision set and the
                           shim does not export it.  The latch is an INTRABAR
                           event: stamped at its bar's OPEN [L-R.5].
  harvest bar              Trade.harvest_i; a close event (bar close) [L-R.5].
  tide streak at entry     tierc7_lab_regime.tide_streak(sym)[1][entry_i]
                           [L-G.1], exactly as tierc9.tc7g_tables._tag_trailing
                           reads it (tierc9.py:1353, 1387-1388: left-censored iff
                           start == TIDE_WARM_BARS).
  trailing edges / band    T9._trailing_edges(T9._trailing_pool(lo, hi),
                           open_ms[entry_i])["streak_bar"] and
                           LR._streak_band(run, edges) (tierc9.py:1290, 1318,
                           1356-1361) — the call TC10's P-AGE-1 table made
                           through tc7g_tables (tierc10_close_p_age_1_tide_youth
                           .py:356-392).  B4 OLD = run >= trailing q75.
  tide_abs_gt206           the absolute SHADOW, "refuse streak > 206, exactly as
                           written" [L-G.1] (abs_tide_refused; 206 = the
                           whole-corridor median edge, not the OLD edge; it
                           reads the corridor ahead).
  tide_streak_age_arm      tierc9.tide_streak_age(t, roles) (tierc9.py:537-560):
                           the OTHER tide age on disk (arm bar, three-state) —
                           a disclosure only.
  era_of_entry             E.era_of(entry_close_ms) [L-1.3: era by CLOSE].
  entered_after_tc10_pin   entry_close_ms > 1790006400000.
  continuation             entry_close_ms <= 1790006400000 <= exit_ms (bar open):
                           a campaign TC10 saw OPEN at its as-of
                           (tierc10_close_forward_strip.py:14-15).

PRECISION: every float column of the four parquet tables is rounded to 6 dp at
write (tierc2_baseline._round_floats via TP.make_put / write_table).  Every flag
(r_over_atr_gt_2p2, tide_abs_gt206, bands, latch, eras) is computed at FULL
precision BEFORE rounding; a later identity-law check must read the Trade
objects (v6_book / trg912_book), never re-derive from the 6-dp table.

REFEREES PINNED BY VALUE (compute() HALTs before riding unless they hold):
  the filed TC10 control journal is sha256 FILED_JOURNAL_SHA with FILED_JOURNAL_N
  rows [L-1.7 "(200 rows, sha fcbf5db0…)"]; P-TRG-2's full arm is book_sha256
  TRG2_BOOK_SHA with n TRG2_N [L-1.6 "b2276fa4…"]; AS_OF_PIN.json names PIN_MS.

ANCHORS HELD BEFORE ANYTHING IS WRITTEN (the build HALTs otherwise):
  F-CTRL(a) [L-1.7]  run_cell_n(control) vs tierc6.run_cell(CARD_V6) over the TC11
                     corridor: 0.000e+00 on TP.CTRL_COLS, identical exit reasons
                     and count; (lo, hi) == TP.control_window().
  F-CTRL(b) [L-1.7]  TP.journal_frame(live) vs the filed TC10 control journal on
                     the 12 CTRL_COLS at its 6 dp: every campaign it CLOSED exact;
                     its corridor_end rows are continuations (entry/stop/r_dist
                     exact; the exit may differ but only AFTER the filed as-of:
                     live exit bar opens >= the TC10 pin, and n_advances / mfe_r
                     are no smaller than filed — the filed ride is a prefix of
                     the live one); live-only campaigns entered after the TC10
                     pin (listed).
  F-912-ANCHOR [L-1.6]  TP._book_sha of the 9/12 book over the TC10 window ==
                     the full-arm book_sha256 of P-TRG-2.scored.json (n 198); the
                     v6 book over the same window == that arm's base_sha256.
  F-AGE-ANCHOR [L-G.1]  the trailing-band assignment of the TC10-window v6 book
                     reproduces research_outputs/tierc10/close/P_AGE_1_TIDE_YOUTH
                     .parquet exactly (T5.agg per band, the TC10 table's own law).

WHAT WOULD MAKE THIS WRONG: riding a window whose end is not TC11's pin (the
corridor must end at 1790294400000); reading era by bar OPEN (TP.in_era) instead
of close; taking the tide age at the arm bar or banding it on whole-corridor
edges (both are F-AGE-ANCHOR's sabotages); a second +1R opinion that disagrees
with the ride's latch (HALTs); letting a window_end past the ride's hi pose as
known.

Run:  export NAIAD_CACHE_DIR=$HOME/.cache/naiad/snapshots/tc11_20260925 PYTHONDONTWRITEBYTECODE=1
      ~/venvs/naiad/bin/python -B scripts/tierc11_books.py            # canonical build
      ~/venvs/naiad/bin/python -B scripts/tierc11_books.py --out-dir=DIR  # F-DET twin
      (DIR must be a direct child of research_outputs/tierc11/books/_det_books/,
       or of a `_det_books/` directory OUTSIDE the repo tree — the fixture's
       --root scratch)
"""
from __future__ import annotations

import dataclasses
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
import tierc11_env as E                     # noqa: E402  (substrate guard + shim + hook)

import numpy as np                          # noqa: E402
import pandas as pd                         # noqa: E402

TP, T9, T7, T6, T5, TB, LR = E.TP, E.T9, E.T7, E.T6, E.T5, E.TB, E.LAB
V6RULES = E.R6                              # tierc6_rules (CARD_V6 lives here)
iso, r4, r6 = TB.iso, TB.r4, TB.r6
MS_4H = TP.MS_4H

# ══════════════════════════════════════════════════════════ CONSTANTS OF RECORD
PIN_MS = E.PIN_MS                           # 2026-09-25T00:00:00Z [L-0.1]
PIN_ISO = "2026-09-25T00:00:00Z"
TC10_PIN_MS = 1_790_006_400_000             # 2026-09-21T16:00:00Z [L-1.6, L-1.7, L-T.6]
TC10_PIN_ISO = "2026-09-21T16:00:00Z"
SEED = E.SEED                               # nothing here draws; passed where asked
ERA_CUT_MS = E.ERA_CUT_MS
ABS_TIDE_CUT = 206                          # L-G.1 absolute shadow: refuse streak > 206
R_OVER_ATR_CUT = 2.2                        # L-G.3: refuse r_over_atr > 2.2
LAG_BANDS = (("0", 0, 0), ("1-6", 1, 6), ("7-15", 7, 15), (">=16", 16, None))  # L-G.2
BAND_CODES = ("B1", "B2", "B3", "B4")       # LR.STREAK_LABELS order; B4 = OLD
EXIT_INTRABAR = ("stop",)                   # L-R.5: stamped at the bar OPEN (tierc9.py:296-297)
FLOAT_DP = 6                                # tierc2_baseline._round_floats at write
COLLAR = {"tier": "TIER-E", "selection_not_a_result": "a SELECTION, not a result",
          "gates": "nothing"}               # L-1.4: every non-registered table
ABS_SHADOW_CAVEAT = ("streak > 206 is L-G.1's ABSOLUTE SHADOW, printed as written: 206 is the "
                     "whole-corridor MEDIAN edge, not the OLD edge, and it reads the corridor "
                     "ahead (look-ahead); the OLD cut of record is the trailing q75 (B4)")

# REFEREES PINNED BY VALUE — compute() HALTs before riding unless they hold
FILED_JOURNAL_SHA = "fcbf5db0480416b0a5c7f704987980aea220650cb0764d5dd4095611fae64c1c"
FILED_JOURNAL_N = 200                       # L-1.7 "(200 rows, sha fcbf5db0…)"
TRG2_BOOK_SHA = "b2276fa487119ef12a8e0434e54f9b77efbfb7ee387b3cb35d2955043c371a8f"
TRG2_N = 198                                # L-1.6 "book_sha256 b2276fa4…"
AS_OF_PIN_JSON = E.OUT / "data" / "AS_OF_PIN.json"

OUT = E.OUT / "books"
DET_ROOT = OUT / "_det_books"
BOOKS = ("v6", "trg912")
JOURNAL_KEY = ["asset", "entry_ms"]
CAMPAIGN_KEY = ["symbol", "entry_ms"]
PARQUETS = ("v6_journal", "trg912_journal", "v6_campaigns", "trg912_campaigns")
MANIFEST = "build_manifest.json"
REPORT = "BOOKS.md"
OUTPUT_FILES = tuple(f"{p}.parquet" for p in PARQUETS) + (MANIFEST, REPORT)

# the TC10 records read (each on the L-0.3 allow-list, by absolute main-tree path)
JOURNAL_REL = "research_outputs/tierc10/panel/control_journal.parquet"
TRG2_REL = "research_outputs/tierc10/registrations/P-TRG-2.scored.json"
PAGE1_REL = "research_outputs/tierc10/close/P_AGE_1_TIDE_YOUTH.parquet"
TRG2_FULL_ARM = "trg-9/12 vs card v6 · CLASSIC5 · full"
PAGE1_BAND_ALL = "99-ALL"

# the campaign table: every column, in order; the nullable ones and the flag
# that says WHEN they are null (F-KEY holds both directions)
CAMPAIGN_COLUMNS = (
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
NULL_IFF = {                                # column -> (flag column, flag value when null)
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
JOURNAL_REQUIRED = ("asset", "lane", "entry_ms", "direction", "arm_ms", "exit_reason",
                    "exit_ts") + tuple(TP.CTRL_COLS)

READINGS = (
    "[LEAN-HEPHAESTUS] L-1.6 BASE v6 = TP.run_cell_n(TP.CONTROL_CARD, T9.V6_ROLES, "
    "CLASSIC5, lo, hi) over (lo, hi) = TP.corridor_n(CLASSIC5): the full TC11 corridor, "
    f"hi + 1 == {PIN_MS} ({PIN_ISO}).",
    "[LEAN-HEPHAESTUS] L-1.6 9/12 = T9.replay9(s, TP.CONTROL_CARD, T9.SWEEP_CELLS[-1], lo, "
    "hi) per CLASSIC5 asset; SWEEP_CELLS[-1] must be Roles('trigger-9/12', trg_f=9, "
    "trg_s=12) or HALT; anchored by TP._book_sha over the TC10 window (hi + 1 = "
    f"{TC10_PIN_ISO}) == P-TRG-2.scored.json full-arm book_sha256.",
    "[LEAN-HEPHAESTUS] L-1.7 F-CTRL(a) exact 0.000e+00 vs tierc6.run_cell(CARD_V6); "
    "F-CTRL(b) journal_frame(live) vs the filed TC10 control journal at 6 dp — closed "
    "campaigns exact on the 12 CTRL_COLS, corridor_end rows are continuations, entries "
    "after the TC10 pin listed as new.",
    "[LEAN-HEPHAESTUS] L-1.3 era = the entry bar's CLOSE (E.era_of(entry_close_ms)); "
    "tuning <= 2024-06-30T23:59:59Z; TP.in_era (bar OPEN) is not used; an entry bar "
    "straddling the cut is counted.",
    "[LEAN-HEPHAESTUS] L-G.1 tide age = tierc7_lab_regime.tide_streak at the ENTRY bar; "
    "band of record = trailing CLASSIC5 quartile edges over bars with open <= the entry "
    "bar (T9._trailing_edges, >= 30 bars), B4 OLD = streak >= trailing q75; shadow = "
    "streak > 206 as written; tierc9.tide_streak_age (arm bar) printed as disclosure.",
    "[LEAN-HEPHAESTUS] L-G.2 lag = entry_i - arm_i in 4h bars, bands 0 / 1-6 / 7-15 / >=16; "
    "L-G.3 r_over_atr = r_dist / ATR14_4h(entry), > 2.2 flagged.",
)


def _halt(msg: str) -> None:
    raise SystemExit(f"HALT: {msg}")


# ═══════════════════════════════════════════════════════════════ THE CORRIDORS
def corridor(pin_close_iso: str | None = None) -> tuple[int, int, dict]:
    """(lo, hi, meta) = TP.corridor_n(CLASSIC5[, pin]).  With no pin it is the
    full TC11 corridor and HALTs unless its end is TC11's pin; a pin may only
    look back (TP.corridor_n refuses a forward one)."""
    lo, hi, meta = TP.corridor_n(E.CLASSIC5, pin_close_iso=pin_close_iso)
    want = PIN_MS if pin_close_iso is None else TP._iso_ms(pin_close_iso)
    if hi + 1 != want:
        _halt(f"corridor end {iso(hi + 1)} != {iso(want)}")
    return lo, hi, meta


def tc10_window() -> tuple[int, int, dict]:
    return corridor(TC10_PIN_ISO)


# ══════════════════════════════════════════════════════════════════ THE BOOKS
def r912():
    """T9.SWEEP_CELLS[-1], PROVEN to be the 9/12 trigger cell: exactly
    Roles(name='trigger-9/12', trg_f=9, trg_s=12) with every other field v6's
    (tierc9.py:122-130).  HALTs otherwise."""
    cell = T9.SWEEP_CELLS[-1]
    want = dataclasses.replace(T9.V6_ROLES, name="trigger-9/12", trg_f=9, trg_s=12)
    if type(cell) is not T9.Roles or cell != want:
        _halt(f"T9.SWEEP_CELLS[-1] is {cell!r}, not {want!r} — the 9/12 book would "
              f"ride another trigger under its name [L-1.6]")
    return cell


def _check_window(lo: int, hi: int) -> None:
    lo_c, hi_c, _ = TP.corridor_n(E.CLASSIC5)
    if hi > hi_c or (hi + 1) % MS_4H or lo > hi:
        _halt(f"window [{iso(lo)}, {iso(hi + 1)}) — the end must be a 4h bar close no "
              f"later than the corridor end {iso(hi_c + 1)}")


def v6_book(lo: int, hi: int):
    """BASE v6 [L-1.6]: the known control, unfiled (TP.is_control_book)."""
    return TP.run_cell_n(TP.CONTROL_CARD, T9.V6_ROLES, E.CLASSIC5, lo, hi)


def trg912_book(lo: int, hi: int) -> list:
    """9/12 [L-1.6]: T9.replay9 per CLASSIC5 asset, in CLASSIC5 order (the order
    run_cell_n iterates), with the window run_cell_n would demand."""
    roles = r912()
    _check_window(lo, hi)
    out = []
    for s in E.CLASSIC5:
        _, t = T9.replay9(s, TP.CONTROL_CARD, roles, lo, hi)
        out += t
    return out


def book_sha(book) -> str:
    """TP._book_sha — the hashing P-TRG-2.scored.json binds (tierc10_panel.py:1988:
    sha256 of the sorted [symbol, lane, entry_ms, repr(net_r)] rows)."""
    return TP._book_sha(book)


# ══════════════════════════════════════════════════════ CAMPAIGN-FIELD SOURCES
def ride_bounds(sym: str, roles, lo_ms: int, hi_ms: int) -> tuple[int, int, int]:
    """replay9's own (lo_i, hi_i) (tierc9.py:381-383) and the tape length."""
    f = T9.frame(sym)["f"]
    lo_i, hi_i = T7._idx_range(f.open_ms, lo_ms, hi_ms)
    return max(lo_i, roles.floor_bars), hi_i, len(f.c)


def arm_index(sym: str, roles, lo_ms: int, hi_ms: int) -> tuple[dict, int, int]:
    """{(arm_i, direction): Arming} — the card's armings over the ride's window
    (T9.armings9 with replay9's bounds), plus hi_i and len(tape)."""
    lo_i, hi_i, n = ride_bounds(sym, roles, lo_ms, hi_ms)
    arms = T9.armings9(sym, roles, lo_i, hi_i)
    idx = {}
    for a in arms:
        k = (int(a.arm_i), int(a.direction))
        if k in idx:
            _halt(f"{sym}: two armings at arm_i {k[0]} direction {k[1]}")
        idx[k] = a
    return idx, hi_i, n


def plus_1r_bar(f, t) -> int | None:
    """The card's OWN +1R latch bar — tierc10_stamps._plus_1r_bar
    (tierc10_stamps.py:405-422), transcribed verbatim: the first bar j in
    (entry_i, exit_i] whose favourable extreme is >= +1R, the exit bar counted
    (the ride latches at the TOP of each bar, before the stop test)."""
    d, R = int(t.direction), float(t.r_dist)
    ex = f.h if d == 1 else f.l
    for j in range(int(t.entry_i) + 1, int(t.exit_i) + 1):
        if (float(ex[j]) - float(t.entry_px)) * d / R >= 1.0:
            return j
    return None


def latch_bar(f, t) -> int | None:
    """plus_1r_bar, with campaign_instants' HALT (tierc10_stamps.py:553-559): the
    extractor reads the card's latch, never a second opinion."""
    j1 = plus_1r_bar(f, t)
    if (j1 is not None) != bool(t.reached_1r):
        _halt(f"{t.symbol} {iso(int(t.entry_ms))}: the +1R re-derivation "
              f"({'bar ' + str(j1) if j1 is not None else 'none'}) disagrees with the "
              f"ride's own latch (reached_1r={bool(t.reached_1r)})")
    return j1


def tide_pool(lo: int, hi: int) -> dict:
    """The CLASSIC5 bar pool of the tide streak, WITH TIMES (tierc9.py:1290)."""
    return T9._trailing_pool(lo, hi)


def entry_streak(t) -> tuple[int, bool, int]:
    """(run, left_censored, state) at the ENTRY bar — LR.tide_streak, read as
    tc7g_tables' _tag_trailing reads it (tierc9.py:1353, 1387-1388)."""
    state, run, start = LR.tide_streak(t.symbol)
    i = int(t.entry_i)
    return int(run[i]), bool(int(start[i]) == int(LR.TIDE_WARM_BARS)), int(state[i])


def trailing_edges(t, pool: dict):
    """[q25, q50, q75] over the pool prefix open_ms <= the entry bar's open, or
    None while that prefix holds < 30 bars (tierc9.py:1318, 1356)."""
    f = T9.frame(t.symbol)["f"]
    return T9._trailing_edges(pool, int(f.open_ms[int(t.entry_i)]))["streak_bar"]


def band_of(run: int, edges) -> int | None:
    """LR._streak_band (np.digitize, right=False): 0 B1 … 3 B4 OLD; the lab's
    no-null-under-warm-edges HALT kept (tierc9.py:1360-1368)."""
    if edges is None:
        return None
    sb = LR._streak_band(int(run), edges)
    if sb is None:
        _halt("a campaign has no tide streak band under warm trailing edges")
    return int(sb)


def lag_band(lag: int) -> str:
    for name, a, b in LAG_BANDS:
        if lag >= a and (b is None or lag <= b):
            return name
    _halt(f"lag {lag} is in no band")


def known_window_end(end_i: int, hi_i: int) -> int:
    """The window end AS KNOWN at the ride's as-of.  armings9 scans the whole
    tape (tierc9.py:181-183), so its end_i may be a bar AFTER hi_i — a future
    bar.  Kept only if the counter cross closed by the as-of (end_i <= hi_i);
    otherwise hi_i + 1, one past the ride's last bar: the window is OPEN."""
    return int(end_i) if int(end_i) <= int(hi_i) else int(hi_i) + 1


def abs_tide_refused(run: int) -> bool:
    """L-G.1's absolute shadow, exactly as written: refuse streak > 206."""
    return int(run) > ABS_TIDE_CUT


def exit_event(t) -> tuple[int, str]:
    """(exit_event_ms, exit_event_stamp) [L-R.5]: an intrabar exit (a stop) at
    its bar's OPEN; a close exit (bell, corridor_end) at its bar's close."""
    if str(t.exit_reason) in EXIT_INTRABAR:
        return int(t.exit_ms), "intrabar_open"
    return int(t.exit_ms) + MS_4H, "close"


def campaign_rows(book, roles, lo: int, hi: int, pool: dict, name: str) -> pd.DataFrame:
    """ONE ROW PER CAMPAIGN (CAMPAIGN_COLUMNS), keyed (symbol, entry_ms)."""
    arms_of: dict = {}
    rows = []
    for t in book:
        s = t.symbol
        if s not in arms_of:
            arms_of[s] = arm_index(s, roles, lo, hi)
        arms, hi_i, n = arms_of[s]
        f = T9.frame(s)["f"]
        d = int(t.direction)
        a = arms.get((int(t.arm_i), d))
        if a is None:
            _halt(f"{s} {iso(int(t.entry_ms))}: no arming at arm_i {t.arm_i}")
        if int(f.open_ms[int(t.entry_i)]) != int(t.entry_ms) or \
                int(f.open_ms[int(t.arm_i)]) != int(t.arm_ms) or \
                int(f.open_ms[int(t.exit_i)]) != int(t.exit_ms):
            _halt(f"{s} {iso(int(t.entry_ms))}: an index does not open at its ms")
        if not (int(t.arm_i) <= int(t.entry_i) <= hi_i):
            _halt(f"{s} {iso(int(t.entry_ms))}: entry outside the ride [arm_i, hi_i]")
        we = known_window_end(int(a.window_end_i), hi_i)
        if we > hi_i + 1:
            _halt(f"{s} {iso(int(t.entry_ms))}: window_end_i {we} is a bar after the "
                  f"as-of (hi_i {hi_i}) — look-ahead")
        if not (int(t.entry_i) < we):
            _halt(f"{s} {iso(int(t.entry_ms))}: entry outside its window")
        closed = we <= hi_i
        j1 = latch_bar(f, t)
        ev_ms, ev_stamp = exit_event(t)
        run, cens, state = entry_streak(t)
        ed = trailing_edges(t, pool)
        sb = band_of(run, ed)
        age_arm, age_cens = T9.tide_streak_age(t, roles)
        entry_close = int(t.entry_ms) + MS_4H
        lag = int(t.entry_i) - int(t.arm_i)
        if t.harvested and int(f.open_ms[int(t.harvest_i)]) != int(t.harvest_ms):
            _halt(f"{s} {iso(int(t.entry_ms))}: harvest_i does not open at harvest_ms")
        rows.append({
            "symbol": s, "entry_ms": int(t.entry_ms), "book": name,
            "roles_name": roles.name, "lane": str(t.lane), "direction": d,
            "arm_i": int(t.arm_i), "arm_open_ms": int(t.arm_ms),
            "arm_close_ms": int(t.arm_ms) + MS_4H,
            "entry_i": int(t.entry_i), "entry_open_ms": int(t.entry_ms),
            "entry_close_ms": entry_close,
            "exit_i": int(t.exit_i), "exit_ms": int(t.exit_ms),
            "exit_close_ms": int(t.exit_ms) + MS_4H,
            "exit_event_ms": ev_ms, "exit_event_stamp": ev_stamp,
            "exit_reason": str(t.exit_reason),
            "open_at_asof": str(t.exit_reason) == "corridor_end",
            "entry_px": float(t.entry_px), "stop_px": float(t.stop_px),
            "r_dist": float(t.r_dist), "atr_at_entry": float(t.atr_at_entry),
            "r_over_atr": float(t.r_dist) / float(t.atr_at_entry),
            "r_over_atr_gt_2p2": bool(float(t.r_dist) / float(t.atr_at_entry)
                                      > R_OVER_ATR_CUT),
            "lag": lag, "lag_band": lag_band(lag),
            "window_end_i": we,
            "window_end_close_ms": (int(f.open_ms[we]) + MS_4H if closed else None),
            "window_open_at_asof": not closed,
            "harvested": bool(t.harvested),
            "harvest_i": int(t.harvest_i) if t.harvested else None,
            "harvest_close_ms": (int(t.harvest_ms) + MS_4H if t.harvested else None),
            "reached_1r": bool(t.reached_1r),
            "latch_1r_i": j1,
            "latch_1r_open_ms": (int(f.open_ms[j1]) if j1 is not None else None),
            "net_r": float(t.net_r), "gross_r": float(t.gross_r),
            "fee_r": float(t.fee_r), "funding_r": float(t.funding_r),
            "era_of_entry": str(E.era_of(entry_close)),
            "entry_bar_straddles_era_cut": bool(int(t.entry_ms) <= ERA_CUT_MS < entry_close),
            "tide_state_entry": state, "tide_streak_entry": run,
            "tide_left_censored": cens,
            "tide_trailing_edge_q25": (float(ed[0]) if ed is not None else None),
            "tide_trailing_edge_q50": (float(ed[1]) if ed is not None else None),
            "tide_trailing_edge_q75": (float(ed[2]) if ed is not None else None),
            "tide_band": (BAND_CODES[sb] if sb is not None else None),
            "tide_band_label": (LR.STREAK_LABELS[sb] if sb is not None else None),
            "tide_abs_gt206": bool(abs_tide_refused(run)),
            "tide_streak_age_arm": int(age_arm),
            "tide_streak_age_arm_censored": bool(age_cens),
            "entered_after_tc10_pin": bool(entry_close > TC10_PIN_MS),
            "continuation": bool(entry_close <= TC10_PIN_MS <= int(t.exit_ms)),
        })
    df = pd.DataFrame(rows, columns=list(CAMPAIGN_COLUMNS))
    for c in ("window_end_close_ms", "harvest_i", "harvest_close_ms", "latch_1r_i",
              "latch_1r_open_ms"):
        df[c] = df[c].astype("Int64")
    for c in ("tide_trailing_edge_q25", "tide_trailing_edge_q50", "tide_trailing_edge_q75"):
        df[c] = df[c].astype(float)
    return df


# ═══════════════════════════════════════════════════════════════ F-CTRL (a/b)
def ctrl_a_findings(got_j: pd.DataFrame, want_j: pd.DataFrame, lo: int, hi: int
                    ) -> tuple[list[str], dict]:
    """F-CTRL(a) [L-1.7]: TP.ctrl_diff (sort on (asset, entry_ms); equal n; EXACT
    zero on the 12 CTRL_COLS; identical exit_reason) and (lo, hi) ==
    TP.control_window()."""
    out = []
    win = (lo, hi) == tuple(TP.control_window())
    if not win:
        out.append(f"CTRL-A-WINDOW: corridor_n {(lo, hi)} != control_window "
                   f"{TP.control_window()}")
    ok, worst, why = TP.ctrl_diff(got_j, want_j)
    if not ok:
        out.append(f"CTRL-A-DIFF: run_cell_n vs tierc6.run_cell — {why}")
    return out, {"worst": worst, "why": why, "window_ok": win, "n": len(got_j)}


def ctrl_a(lo: int, hi: int, book=None) -> tuple[list[str], dict]:
    got = TP.journal_frame(book if book is not None else v6_book(lo, hi))
    want = TP.journal_frame(T6.run_cell(V6RULES.CARD_V6, lo, hi))
    return ctrl_a_findings(got, want, lo, hi)


def filed_control_journal() -> tuple[pd.DataFrame, str, int]:
    """The filed TC10 control journal (allow-listed; absolute main-tree path):
    (frame, sha256 of its bytes, bytes)."""
    p = E.tc10_record(JOURNAL_REL)
    b = p.read_bytes()
    return pd.read_parquet(p), hashlib.sha256(b).hexdigest(), len(b)


def ctrl_b_findings(live: pd.DataFrame, filed: pd.DataFrame, tc10_close_ms: int
                    ) -> tuple[list[str], dict]:
    """F-CTRL(b) [L-1.7], cross-process, at the filed journal's 6 dp.
      CTRL-B-MISSING       a filed campaign absent live (on (asset, entry_ms));
      CTRL-B-CLOSED        a campaign the filed journal CLOSED differs live on
                           any of the 12 CTRL_COLS (exact) or on exit_reason;
      CTRL-B-CONTINUATION  a filed corridor_end row differs on entry_ms /
                           entry_px / stop_px / r_dist; or its live exit is not
                           AFTER the filed window (the live exit bar opens before
                           the TC10 pin — inside the window the filed journal
                           says it was open through), or the live n_advances /
                           mfe_r are below the filed ones (the filed ride is a
                           prefix of the live one: both can only grow);
      CTRL-B-EARLY         a live-only campaign whose entry closed at or before
                           the filed as-of (drift inside the filed window);
      CTRL-B-ASOF          the filed as-of is not the TC10 pin."""
    out = []
    asof = sorted(set(str(x) for x in filed["as_of_last_closed_4h"]))
    if asof != [iso(tc10_close_ms)]:
        out.append(f"CTRL-B-ASOF: filed as_of {asof} != {iso(tc10_close_ms)}")
    ks = ["asset", "entry_ms"]
    kl = set(zip(live["asset"], live["entry_ms"].astype(int)))
    kf = set(zip(filed["asset"], filed["entry_ms"].astype(int)))
    for a, m in sorted(kf - kl):
        out.append(f"CTRL-B-MISSING: filed campaign {a} {iso(m)} absent live")
    lv = live.copy()
    fl = filed.copy()
    lv["entry_ms"] = lv["entry_ms"].astype(int)
    fl["entry_ms"] = fl["entry_ms"].astype(int)
    mg = lv.merge(fl, on=ks, suffixes=("", "_filed"))
    closed = mg[mg["exit_reason_filed"] != "corridor_end"]
    cont = mg[mg["exit_reason_filed"] == "corridor_end"]
    # entry_ms is one of the 12 CTRL_COLS and the join key: equal by the join
    cmp_cols = [c for c in TP.CTRL_COLS if c not in ks]
    for r in closed.itertuples(index=False):
        rr = r._asdict()
        bad = [c for c in cmp_cols
               if float(rr[c]) != float(rr[c + "_filed"])]
        if rr["exit_reason"] != rr["exit_reason_filed"]:
            bad.append("exit_reason")
        if bad:
            out.append(f"CTRL-B-CLOSED: {rr['asset']} {iso(rr['entry_ms'])} differs on "
                       f"{bad} (e.g. {bad[0]} live {rr[bad[0]]} vs filed "
                       f"{rr[bad[0] + '_filed']})")
    for r in cont.itertuples(index=False):
        rr = r._asdict()
        bad = [c for c in ("entry_px", "stop_px", "r_dist")
               if float(rr[c]) != float(rr[c + "_filed"])]
        if bad:
            out.append(f"CTRL-B-CONTINUATION: {rr['asset']} {iso(rr['entry_ms'])} differs "
                       f"on {bad} (e.g. {bad[0]} live {rr[bad[0]]} vs filed "
                       f"{rr[bad[0] + '_filed']})")
        if int(rr["exit_ms"]) < int(tc10_close_ms):
            out.append(f"CTRL-B-CONTINUATION: {rr['asset']} {iso(rr['entry_ms'])} live exit "
                       f"bar opens {iso(int(rr['exit_ms']))} ({rr['exit_reason']}), before the "
                       f"filed as-of {iso(tc10_close_ms)} — inside the window the filed "
                       f"journal says it was open through")
        for c in ("n_advances", "mfe_r"):
            if float(rr[c]) < float(rr[c + "_filed"]):
                out.append(f"CTRL-B-CONTINUATION: {rr['asset']} {iso(rr['entry_ms'])} live "
                           f"{c} {rr[c]} < filed {rr[c + '_filed']} — the filed ride is not "
                           f"a prefix of the live one")
    new = sorted(kl - kf)
    for a, m in new:
        if m + MS_4H <= tc10_close_ms:
            out.append(f"CTRL-B-EARLY: live-only campaign {a} {iso(m)} entered at or before "
                       f"the filed as-of {iso(tc10_close_ms)} — drift inside the filed window")
    info = {
        "n_live": len(live), "n_filed": len(filed), "n_shared": len(mg),
        "n_closed_compared": len(closed), "n_continuation": len(cont),
        "continuations": [
            {"asset": r.asset, "entry_ts": iso(int(r.entry_ms)),
             "filed_exit": f"{iso(int(r.exit_ms_filed))} {r.exit_reason_filed} "
                           f"net {float(r.net_r_filed):+.6f}",
             "live_exit": f"{iso(int(r.exit_ms))} {r.exit_reason} net {float(r.net_r):+.6f}"}
            for r in cont.itertuples(index=False)],
        "new": [(a, iso(m)) for a, m in new],
    }
    return out, info


# ═════════════════════════════════════════════════════════════ F-912-ANCHOR
def filed_trg2() -> dict:
    """P-TRG-2.scored.json (allow-listed): the full arm's {book_sha256, n, …}."""
    rec = json.loads(E.tc10_record(TRG2_REL).read_text(encoding="utf-8"))
    return rec["arms"][TRG2_FULL_ARM]


def trg912_anchor_findings(book10: list, filed: dict, base10: list | None = None
                           ) -> tuple[list[str], dict]:
    """912-SHA / 912-N: the 9/12 book over the TC10 window vs the filed full arm;
    912-BASE: the v6 book over the same window vs the SAME arm's filed
    base_sha256 (the base P-TRG-2's two-sample row was scored against)."""
    sha = book_sha(book10)
    out = []
    if sha != filed["book_sha256"]:
        out.append(f"912-SHA: TP._book_sha {sha} != filed full-arm book_sha256 "
                   f"{filed['book_sha256']}")
    if len(book10) != int(filed["n"]):
        out.append(f"912-N: n {len(book10)} != filed {filed['n']}")
    bsha = book_sha(base10) if base10 is not None else None
    if base10 is not None and bsha != filed["base_sha256"]:
        out.append(f"912-BASE: v6 TP._book_sha {bsha} != filed full-arm base_sha256 "
                   f"{filed['base_sha256']}")
    return out, {"sha": sha, "n": len(book10), "base_sha": bsha}


# ═════════════════════════════════════════════════════════════ F-AGE-ANCHOR
def age_band_rows(book, pool: dict, age=None, edges=None) -> pd.DataFrame:
    """The P-AGE-1 table's rows re-derived: each campaign banded by its tide age
    at the entry bar on trailing edges; per band (and ALL) T5.agg — the TC10
    table's own statistic law (tierc5.py:557) — plus the extras TC10's shape()
    added (tierc10_close_p_age_1_tide_youth.py: n_left_censored and streak
    min/median/max).  `age(t) -> (run, left_censored)` and `edges(t) -> [q25,
    q50, q75]` default to the definitions of record; F-AGE-ANCHOR's sabotages
    pass the rivals."""
    age = age or (lambda t: entry_streak(t)[:2])
    edges = edges or (lambda t: trailing_edges(t, pool))
    tagged = []
    for t in book:
        run, cens = age(t)
        sb = band_of(run, edges(t))
        tagged.append((t, sb, run, cens))
    rows = []
    for code, sel in [(f"{b + 1:02d}", b) for b in range(len(BAND_CODES))] + \
            [(PAGE1_BAND_ALL, None)]:
        sub = [x for x in tagged if (x[1] is not None if sel is None else x[1] == sel)]
        a = T5.agg([x[0] for x in sub], "tide_streak_band", code)
        sb_ = np.asarray([x[2] for x in sub], float)
        a.update({"band": code, "n_assets": len({x[0].symbol for x in sub}),
                  "n_left_censored": int(sum(x[3] for x in sub)),
                  "streak_bars_at_entry_min": (int(sb_.min()) if len(sb_) else None),
                  "streak_bars_at_entry_median": (float(np.median(sb_)) if len(sb_) else None),
                  "streak_bars_at_entry_max": (int(sb_.max()) if len(sb_) else None)})
        rows.append(a)
    return pd.DataFrame(rows)


AGE_COMPARE = ("n", "net_r", "expectancy_r", "win_rate_pct", "gross_r", "fee_r",
               "funding_r", "n_assets", "n_left_censored", "streak_bars_at_entry_min",
               "streak_bars_at_entry_median", "streak_bars_at_entry_max")


def filed_page1() -> pd.DataFrame:
    return pd.read_parquet(E.tc10_record(PAGE1_REL))


def age_anchor_findings(live: pd.DataFrame, filed: pd.DataFrame) -> list[str]:
    """AGE-ANCHOR: every filed band row (01..04, 99-ALL; v6 card) reproduced
    exactly on AGE_COMPARE; no band missing or extra."""
    out = []
    f = filed[(filed["dimension"] == "tide_streak_band") & (filed["card"] == "v6")]
    fb, lb = sorted(f["band"].astype(str)), sorted(live["band"].astype(str))
    if fb != lb:
        out.append(f"AGE-ANCHOR bands: live {lb} != filed {fb}")
    fi = f.set_index(f["band"].astype(str))
    for r in live.itertuples(index=False):
        rr = r._asdict()
        if rr["band"] not in fi.index:
            continue
        fr = fi.loc[rr["band"]]
        for c in AGE_COMPARE:
            x, y = rr[c], fr[c]
            same = (x is None and pd.isna(y)) or (x is not None and not pd.isna(y)
                                                   and float(x) == float(y))
            if not same:
                out.append(f"AGE-ANCHOR band {rr['band']} {c}: live {x} != filed {y}")
    return out


# ═══════════════════════════════════════════════════════════════════ F-KEY
def key_findings(name: str, df: pd.DataFrame, key: list, required: tuple,
                 null_iff: dict | None = None) -> list[str]:
    """KEY-DUP a duplicated key · KEY-NULL a null in a key or required column (or
    a required column absent) · KEY-ASOF an as-of stamp absent or null ·
    KEY-FLAG a nullable column null where its flag says it must not be, or
    filled where its flag says it must be null."""
    out = []
    miss = [c for c in list(key) + list(required) if c not in df.columns]
    if miss:
        out.append(f"KEY-NULL {name}: required column(s) absent {miss}")
    dup = int(df.duplicated(subset=[c for c in key if c in df.columns]).sum())
    if dup:
        out.append(f"KEY-DUP {name}: {dup} duplicated {key} row(s)")
    for c in [c for c in list(key) + list(required) if c in df.columns]:
        k = int(df[c].isna().sum())
        if k:
            out.append(f"KEY-NULL {name}: {k} null(s) in required column {c}")
    lack = [c for c in TP.AS_OF_COLUMNS if c not in df.columns]
    nul = [c for c in TP.AS_OF_COLUMNS if c in df.columns and df[c].isna().any()]
    if lack or nul:
        out.append(f"KEY-ASOF {name}: as-of stamp(s) absent {lack} / null {nul}")
    for c, (flag, val) in (null_iff or {}).items():
        if c not in df.columns or flag not in df.columns:
            out.append(f"KEY-FLAG {name}: {c} or its flag {flag} absent")
            continue
        isnull = df[c].isna().to_numpy()
        should = (df[flag].isna().to_numpy() if val is None
                  else (df[flag] == val).to_numpy())
        k = int((isnull != should).sum())
        if k:
            out.append(f"KEY-FLAG {name}: {c} null on {int(isnull.sum())} row(s) but "
                       f"{flag}{' is null' if val is None else ' == ' + repr(val)} on "
                       f"{int(should.sum())} ({k} disagree)")
    return out


def table_specs() -> dict:
    """{parquet stem: (key, required columns, null_iff)} — the F-KEY commission."""
    creq = tuple(c for c in CAMPAIGN_COLUMNS if c not in NULL_IFF and c != "tide_band")
    return {"v6_journal": (JOURNAL_KEY, JOURNAL_REQUIRED, None),
            "trg912_journal": (JOURNAL_KEY, JOURNAL_REQUIRED, None),
            "v6_campaigns": (CAMPAIGN_KEY, creq, NULL_IFF),
            "trg912_campaigns": (CAMPAIGN_KEY, creq, NULL_IFF)}


# ═══════════════════════════════════════════════════════════════ REFEREES
def as_of_pin_record() -> dict:
    """research_outputs/tierc11/data/AS_OF_PIN.json — the pin and the latest
    close at fetch time printed beside it [L-0.1]."""
    return json.loads(AS_OF_PIN_JSON.read_text(encoding="utf-8"))


def referee_findings(filed: pd.DataFrame, fsha: str, trg2: dict, pin_rec: dict) -> list[str]:
    """The referees every anchor compares against, pinned BY VALUE:
      CTRL-B-REFEREE  the filed TC10 control journal is not sha256
                      FILED_JOURNAL_SHA with FILED_JOURNAL_N rows [L-1.7];
      912-REFEREE     P-TRG-2's full arm is not book_sha256 TRG2_BOOK_SHA, n
                      TRG2_N [L-1.6];
      ASOF-REFEREE    AS_OF_PIN.json does not name PIN_MS [L-0.1]."""
    out = []
    if fsha != FILED_JOURNAL_SHA or len(filed) != FILED_JOURNAL_N:
        out.append(f"CTRL-B-REFEREE: the filed control journal is sha256 {fsha[:16]}… with "
                   f"{len(filed)} rows, not the typed {FILED_JOURNAL_SHA[:16]}… / "
                   f"{FILED_JOURNAL_N} rows — F-CTRL(b) would compare against another referee")
    if str(trg2.get("book_sha256")) != TRG2_BOOK_SHA or int(trg2.get("n", -1)) != TRG2_N:
        out.append(f"912-REFEREE: P-TRG-2 full arm is {str(trg2.get('book_sha256'))[:16]}… n "
                   f"{trg2.get('n')}, not the typed {TRG2_BOOK_SHA[:16]}… n {TRG2_N}")
    if int(pin_rec.get("as_of_last_closed_4h_close_ms", -1)) != PIN_MS:
        out.append(f"ASOF-REFEREE: AS_OF_PIN.json names "
                   f"{pin_rec.get('as_of_last_closed_4h_close_ms')}, not {PIN_MS}")
    return out


# ═══════════════════════════════════════════════════════════════════ BUILD
def compute() -> dict:
    """Ride both books over the TC11 corridor and the TC10 window, build the
    tables, and hold every anchor.  HALTs on any referee or anchor finding —
    the referees are checked FIRST, before anything is ridden."""
    filed, fsha, fbytes = filed_control_journal()
    trg2 = filed_trg2()
    pin_rec = as_of_pin_record()
    fr = referee_findings(filed, fsha, trg2, pin_rec)
    if fr:
        _halt("a referee is not the one typed — nothing is compared: " + " | ".join(fr))
    lo, hi, meta = corridor()
    lo10, hi10, _ = tc10_window()
    if lo10 != lo:
        _halt(f"the TC10 window starts {iso(lo10)} != {iso(lo)}")
    r912_ = r912()
    v6 = v6_book(lo, hi)
    b912 = trg912_book(lo, hi)
    # F-CTRL(a)
    fa, ia = ctrl_a(lo, hi, v6)
    # F-CTRL(b)
    jv6 = TP.journal_frame(v6)
    fb, ib = ctrl_b_findings(jv6, filed, TC10_PIN_MS)
    # F-912-ANCHOR (and the v6 base of the same filed arm)
    b912_10 = trg912_book(lo10, hi10)
    v6_10 = v6_book(lo10, hi10)
    f9, i9 = trg912_anchor_findings(b912_10, trg2, v6_10)
    # F-AGE-ANCHOR
    pool10 = tide_pool(lo10, hi10)
    fg = age_anchor_findings(age_band_rows(v6_10, pool10), filed_page1())
    bad = fa + fb + f9 + fg
    if bad:
        _halt("an anchor is RED — nothing is written: " + " | ".join(bad[:6]))
    pool = tide_pool(lo, hi)
    c6 = campaign_rows(v6, T9.V6_ROLES, lo, hi, pool, "v6")
    c9 = campaign_rows(b912, r912_, lo, hi, pool, "trg912")
    # the TC10-window bands equal the TC11 table's on every shared key (prefix)
    c6_10 = campaign_rows(v6_10, T9.V6_ROLES, lo10, hi10, pool10, "v6")
    m = c6_10.merge(c6, on=CAMPAIGN_KEY, suffixes=("_10", ""))
    moved = int((m["tide_band_10"] != m["tide_band"]).sum()) if len(m) else -1
    if len(m) != len(c6_10) or moved:
        _halt(f"trailing band not prefix-stable: {len(m)}/{len(c6_10)} shared, {moved} moved")
    return {"lo": lo, "hi": hi, "meta": meta, "lo10": lo10, "hi10": hi10,
            "v6": v6, "trg912": b912, "roles912": r912_,
            "j_v6": jv6, "j_912": TP.journal_frame(b912),
            "c_v6": c6, "c_912": c9,
            "ctrl_a": ia, "ctrl_b": ib, "filed_sha": fsha, "filed_bytes": fbytes,
            "filed_rows": len(filed),
            "anchor_912": i9, "trg2_filed": trg2, "pin_rec": pin_rec,
            "v6_10_sha": book_sha(v6_10), "n_v6_10": len(v6_10),
            "prefix_band_shared": len(m),
            "whole_edges": {"tc10_window": [float(x) for x in
                                            LR.cuts(lo10, hi10)["streak_bar"]],
                            "tc11_corridor": [float(x) for x in
                                              LR.cuts(lo, hi)["streak_bar"]]}}


def _stats(df: pd.DataFrame) -> tuple[int, float, float, float]:
    n = len(df)
    s = float(df["net_r"].sum()) if n else 0.0
    return n, s, (s / n if n else float("nan")), (100.0 * float((df["net_r"] > 0).sum()) / n
                                                   if n else float("nan"))


def _f(x: float, nd: int = 4) -> str:
    return "—" if x != x else f"{x:+.{nd}f}"


def _collar_head() -> tuple[str, str]:
    """The L-1.4 collar as three trailing markdown columns (header, rule)."""
    return (" tier | selection_not_a_result | gates |", "---|---|---|")


def _collar() -> str:
    return f" {COLLAR['tier']} | {COLLAR['selection_not_a_result']} | {COLLAR['gates']} |"


def render_md(R: dict, shas: dict) -> str:
    """BOOKS.md — deterministic (no clock, no temp path)."""
    c6, c9 = R["c_v6"], R["c_912"]
    ch, cr = _collar_head()
    pr = R["pin_rec"]
    L = ["# TIER-C11 · TC11-BOOKS — the two frozen books (control / descriptive)", "",
         f"as_of_last_closed_4h: {PIN_ISO} · latest closed 4h at fetch time (AS_OF_PIN.json "
         f"latest_closed_4h_at_pin_run): {pr['latest_closed_4h_at_pin_run']} · substrate "
         f"{R['meta']['substrate']} · corridor {iso(R['lo'])} → {iso(R['hi'] + 1)} · CLASSIC5 · "
         f"seed {SEED}", "",
         "**These are CONTROL / DESCRIPTIVE numbers, not registration scores.** No CI, no "
         "p, no verdict word; every cut below is a SELECTION, not a result.  Every "
         "descriptive table carries the L-1.4 collar (tier = 'TIER-E', "
         "selection_not_a_result = 'a SELECTION, not a result', gates = 'nothing'); the "
         "anchor table is a set of control identities that gate this BUILD (a RED anchor "
         "writes nothing), so it carries no collar.", "",
         f"**Precision.** Every float column of the four parquet tables is rounded to "
         f"{FLOAT_DP} dp at write (tierc2_baseline._round_floats via TP.make_put).  Flags "
         f"(r_over_atr_gt_2p2, tide_abs_gt206, bands, latch, eras) were computed at full "
         f"precision before rounding.  An identity-law check must read the Trade objects "
         f"(tierc11_books.v6_book / trg912_book), not re-derive from these tables.", "",
         "**Stamps [L-R.5].** exit_event_ms is the exit's event stamp: a STOP exit is "
         "intrabar, stamped at its bar's OPEN (exit_event_stamp = 'intrabar_open'); a bell "
         "or corridor_end exit is stamped at its bar's close ('close').  exit_close_ms on an "
         "intrabar exit is the close-stamped twin — POST-EVENT.  latch_1r_open_ms (+1R, "
         "intrabar) is at its bar's OPEN.  window_end_i is the window end AS KNOWN at the "
         "as-of: an open window carries hi_i + 1, never a later bar.", "",
         "## Readings built", ""]
    L += [f"- {x}" for x in READINGS]
    L += ["", "## Anchors (held before any file was written)", "",
          "| anchor | result |", "|---|---|",
          f"| referees pinned by value | control_journal.parquet sha256 {R['filed_sha'][:16]}… "
          f"rows {R['filed_rows']} == typed {FILED_JOURNAL_SHA[:16]}… / {FILED_JOURNAL_N}; "
          f"P-TRG-2 full arm {R['trg2_filed']['book_sha256'][:16]}… n {R['trg2_filed']['n']} "
          f"== typed {TRG2_BOOK_SHA[:16]}… / {TRG2_N}; AS_OF_PIN.json close_ms "
          f"{pr['as_of_last_closed_4h_close_ms']} == {PIN_MS} |",
          f"| F-CTRL(a) run_cell_n vs tierc6.run_cell(CARD_V6), TC11 corridor | "
          f"{R['ctrl_a']['why']}; window == TP.control_window(): {R['ctrl_a']['window_ok']} |",
          f"| F-CTRL(b) vs filed TC10 control_journal.parquet (sha256 {R['filed_sha'][:16]}…, "
          f"{R['filed_bytes']} B) | filed {R['ctrl_b']['n_filed']} · live {R['ctrl_b']['n_live']}"
          f" · shared {R['ctrl_b']['n_shared']} · closed compared exact on 12 CTRL_COLS "
          f"{R['ctrl_b']['n_closed_compared']} · continuations {R['ctrl_b']['n_continuation']}"
          f" (entry/stop/r_dist exact; live exit bar opens at or after the TC10 pin; "
          f"n_advances and mfe_r no smaller than filed) · new {len(R['ctrl_b']['new'])} |",
          f"| F-912-ANCHOR 9/12 over the TC10 window | TP._book_sha {R['anchor_912']['sha']} "
          f"n {R['anchor_912']['n']} == P-TRG-2 full arm {R['trg2_filed']['book_sha256'][:16]}… "
          f"n {R['trg2_filed']['n']} |",
          f"| F-912-ANCHOR base: v6 over the TC10 window | TP._book_sha {R['v6_10_sha']} n "
          f"{R['n_v6_10']} == the same arm's filed base_sha256 "
          f"{R['trg2_filed']['base_sha256'][:16]}… |",
          "| F-AGE-ANCHOR trailing bands, TC10 window | P_AGE_1_TIDE_YOUTH.parquet reproduced "
          "exactly (bands 01..04 + ALL) |",
          f"| trailing band prefix-stable | {R['prefix_band_shared']} TC10-window campaigns "
          f"carry the same band in the TC11 table |", ""]
    L += ["## Books", "",
          "| book | n | ΣR (net) | mean R | win % | open at pin | book sha (TP._book_sha) |" + ch,
          "|---|---:|---:|---:|---:|---:|---|" + cr]
    for name, c, bk in (("v6", c6, R["v6"]), ("trg912", c9, R["trg912"])):
        n, s, m, w = _stats(c)
        L.append(f"| {name} | {n} | {_f(s)} | {_f(m)} | {w:.2f} | "
                 f"{int(c['open_at_asof'].sum())} | {shas[name]} |" + _collar())
    L += ["", "### Per asset", "", "| book | asset | n | ΣR | mean R |" + ch,
          "|---|---|---:|---:|---:|" + cr]
    for name, c in (("v6", c6), ("trg912", c9)):
        for s_ in E.CLASSIC5:
            n, s, m, _ = _stats(c[c["symbol"] == s_])
            L.append(f"| {name} | {s_} | {n} | {_f(s)} | {_f(m)} |" + _collar())
    L += ["", "### Per era (by the entry bar's CLOSE, L-1.3)", "",
          "| book | era | n | ΣR | mean R |" + ch, "|---|---|---:|---:|---:|" + cr]
    for name, c in (("v6", c6), ("trg912", c9)):
        for era in ("tuning", "holdout"):
            n, s, m, _ = _stats(c[c["era_of_entry"] == era])
            L.append(f"| {name} | {era} | {n} | {_f(s)} | {_f(m)} |" + _collar())
    L.append("")
    for name, c in (("v6", c6), ("trg912", c9)):
        L.append(f"- {name}: entry bars straddling the era cut (open <= "
                 f"2024-06-30T23:59:59Z < close): {int(c['entry_bar_straddles_era_cut'].sum())}")
    L += ["", "## Entered after the TC10 pin (entry close > 2026-09-21T16:00:00Z)", "",
          "| book | asset | dir | entry (bar open) | exit (bar open) | exit_reason | net R |" + ch,
          "|---|---|---:|---|---|---|---:|" + cr]
    for name, c in (("v6", c6), ("trg912", c9)):
        sub = c[c["entered_after_tc10_pin"]]
        if not len(sub):
            L.append(f"| {name} | (none) | | | | | |" + _collar())
        for r in sub.itertuples(index=False):
            L.append(f"| {name} | {r.symbol} | {r.direction:+d} | {iso(r.entry_ms)} | "
                     f"{iso(r.exit_ms)} | {r.exit_reason} | {r.net_r:+.6f} |" + _collar())
    L += ["", "## Continuations (entered at or before the TC10 pin, still open at it)", "",
          "| book | asset | dir | entry (bar open) | exit now (bar open) | exit_reason | net R |"
          + ch, "|---|---|---:|---|---|---|---:|" + cr]
    for name, c in (("v6", c6), ("trg912", c9)):
        sub = c[c["continuation"]]
        if not len(sub):
            L.append(f"| {name} | (none) | | | | | |" + _collar())
        for r in sub.itertuples(index=False):
            L.append(f"| {name} | {r.symbol} | {r.direction:+d} | {iso(r.entry_ms)} | "
                     f"{iso(r.exit_ms)} | {r.exit_reason} | {r.net_r:+.6f} |" + _collar())
    L.append("")
    for x in R["ctrl_b"]["continuations"]:
        L.append(f"- v6 continuation vs the filed TC10 journal: {x['asset']} entered "
                 f"{x['entry_ts']} — filed exit {x['filed_exit']} · live exit {x['live_exit']}")
    L += ["", "## Counts (L-G.2 lag, L-G.3 structure distance, L-G.1 tide)", "",
          "| book | lag 0 | lag 1-6 | lag 7-15 | lag >=16 | r_over_atr > 2.2 | "
          "B1 | B2 | B3 | B4 OLD | unbanded | streak > 206 (ABSOLUTE SHADOW, look-ahead) | "
          "left-censored | against tide at entry |" + ch,
          "|---|" + "---:|" * 13 + cr]
    for name, c in (("v6", c6), ("trg912", c9)):
        lb = [int((c["lag_band"] == b[0]).sum()) for b in LAG_BANDS]
        tb = [int((c["tide_band"] == b).sum()) for b in BAND_CODES]
        L.append(f"| {name} | " + " | ".join(str(x) for x in lb) + f" | "
                 f"{int(c['r_over_atr_gt_2p2'].sum())} | " + " | ".join(str(x) for x in tb)
                 + f" | {int(c['tide_band'].isna().sum())} | {int(c['tide_abs_gt206'].sum())}"
                 f" | {int(c['tide_left_censored'].sum())} | "
                 f"{int((c['tide_state_entry'] != c['direction']).sum())} |" + _collar())
    L.append("")
    we = R["whole_edges"]
    L.append(f"- **{ABS_SHADOW_CAVEAT}.**  Whole-corridor quartile edges of the pooled "
             f"CLASSIC5 streak (LR.cuts, printed for the caveat only): TC10 window "
             f"{we['tc10_window']}; TC11 corridor {we['tc11_corridor']}.")
    for name, c in (("v6", c6), ("trg912", c9)):
        L.append(f"- {name}: tide streak at ENTRY (L-G.1 of record) median "
                 f"{float(np.median(c['tide_streak_entry'])):.1f} bars; the arm-bar "
                 f"three-state age (tierc9.tide_streak_age, disclosure) median "
                 f"{float(np.median(c['tide_streak_age_arm'])):.1f} bars, > 206 on "
                 f"{int((c['tide_streak_age_arm'] > ABS_TIDE_CUT).sum())}; windows still open "
                 f"at the as-of {int(c['window_open_at_asof'].sum())}; exits stamped "
                 f"intrabar_open {int((c['exit_event_stamp'] == 'intrabar_open').sum())} / close "
                 f"{int((c['exit_event_stamp'] == 'close').sum())}")
    L += ["", "## Files", ""]
    for k in sorted(shas["content"]):
        L.append(f"- `{k}.parquet` content sha {shas['content'][k]} (key "
                 f"{shas['keys'][k]}; floats at {FLOAT_DP} dp)")
    return "\n".join(L) + "\n"


def _inside(p: Path, root: Path) -> bool:
    return p == root or root in p.parents


def _guard_out(out: Path) -> Path:
    """OUT; a direct child of DET_ROOT; or a direct child of a `_det_books/`
    directory OUTSIDE the repo tree (the fixture's --root scratch, so F-DET's
    twins never have to touch the repo) [verifier MINOR 7]."""
    o = Path(out).resolve()
    if o == OUT.resolve() or o.parent == DET_ROOT.resolve():
        return o
    trees = {ROOT.resolve(), Path(E.MAIN_TREE).resolve()}
    if o.parent.name == DET_ROOT.name and not any(_inside(o, t) for t in trees):
        return o
    _halt(f"output dir {o} is neither {OUT}, an F-DET run dir under {DET_ROOT}, nor one "
          f"under a {DET_ROOT.name}/ scratch outside the repo")
    return o  # unreachable


def build(out: Path = OUT) -> dict:
    """Compute, then write the six files into `out` (guarded)."""
    out = _guard_out(out)
    R = compute()
    put, W, K, SK = TP.make_put(out, R["meta"], lens="4h")
    put(R["j_v6"], "v6_journal", JOURNAL_KEY)
    put(R["j_912"], "trg912_journal", JOURNAL_KEY)
    put(R["c_v6"], "v6_campaigns", CAMPAIGN_KEY)
    put(R["c_912"], "trg912_campaigns", CAMPAIGN_KEY)
    if SK:
        _halt(f"an empty table: {SK}")
    shas = {"v6": book_sha(R["v6"]), "trg912": book_sha(R["trg912"]),
            "content": dict(W), "keys": dict(K)}
    man = {
        "tier": "TIER-C11", "stage": "TC11-BOOKS", "seed": SEED,
        "as_of": PIN_ISO, "as_of_close_ms": PIN_MS,
        "as_of_pin_record": {
            "path": "research_outputs/tierc11/data/AS_OF_PIN.json",
            "as_of_last_closed_4h": R["pin_rec"]["as_of_last_closed_4h"],
            "latest_closed_4h_at_pin_run": R["pin_rec"]["latest_closed_4h_at_pin_run"],
            "pin_equals_latest_closed_at_pin_run":
                R["pin_rec"].get("pin_equals_latest_closed_at_pin_run")},
        "float_precision": {
            "dp": FLOAT_DP,
            "law": "every float column of the four parquet tables is rounded to 6 dp at "
                   "write (tierc2_baseline._round_floats via TP.make_put); flags are "
                   "computed at full precision before rounding; identity-law checks read "
                   "the Trade objects (tierc11_books.v6_book / trg912_book)"},
        "collar": {"applies_to": "every descriptive table of BOOKS.md [L-1.4]", **COLLAR},
        "column_notes": {
            "window_end_i": "the window end AS KNOWN at the as-of (known_window_end): "
                            "armings9's first counter 12/89 cross after arm_i if it is <= "
                            "the ride's hi_i, else hi_i + 1 (OPEN; window_end_close_ms null)",
            "exit_event_ms": "L-R.5 event stamp: 'intrabar_open' = the exit bar's OPEN for "
                             "a stop exit; 'close' = the bar close for bell / corridor_end",
            "exit_close_ms": "the exit bar's close; on an intrabar (stop) exit this is the "
                             "close-stamped twin — POST-EVENT [L-R.5]",
            "tide_abs_gt206": ABS_SHADOW_CAVEAT,
            "latch_1r_open_ms": "the +1R latch bar's OPEN (intrabar event) [L-R.5]"},
        "substrate": R["meta"]["substrate"],
        "corridor": {"lo": iso(R["lo"]), "hi_close": iso(R["hi"] + 1),
                     "panel": list(E.CLASSIC5)},
        "sha": W, "keys": K, "skipped_empty": SK,
        "input_sha": TP.input_sha(E.CLASSIC5),
        "book_sha": {"v6": shas["v6"], "trg912": shas["trg912"]},
        "n": {"v6": len(R["v6"]), "trg912": len(R["trg912"])},
        "net_r_sum": {"v6": r6(sum(float(t.net_r) for t in R["v6"])),
                      "trg912": r6(sum(float(t.net_r) for t in R["trg912"]))},
        "roles": {"v6": dataclasses.asdict(T9.V6_ROLES),
                  "trg912": dataclasses.asdict(R["roles912"])},
        "anchors": {
            "referees": {"filed_journal_sha256_typed": FILED_JOURNAL_SHA,
                         "filed_journal_rows_typed": FILED_JOURNAL_N,
                         "filed_journal_rows": R["filed_rows"],
                         "trg2_book_sha256_typed": TRG2_BOOK_SHA, "trg2_n_typed": TRG2_N,
                         "as_of_close_ms_typed": PIN_MS, "held": True},
            "f_ctrl_a": {"worst": R["ctrl_a"]["worst"], "n": R["ctrl_a"]["n"],
                         "window_ok": R["ctrl_a"]["window_ok"]},
            "f_ctrl_b": {"filed": JOURNAL_REL, "filed_sha256": R["filed_sha"],
                         "filed_bytes": R["filed_bytes"],
                         "n_filed": R["ctrl_b"]["n_filed"],
                         "n_closed_compared": R["ctrl_b"]["n_closed_compared"],
                         "continuations": R["ctrl_b"]["continuations"],
                         "new": R["ctrl_b"]["new"]},
            "f_912_anchor": {"filed": TRG2_REL, "arm": TRG2_FULL_ARM,
                             "book_sha256": R["anchor_912"]["sha"],
                             "n": R["anchor_912"]["n"]},
            "v6_tc10_window": {"book_sha256": R["v6_10_sha"], "n": R["n_v6_10"],
                               "filed_base_sha256": R["trg2_filed"]["base_sha256"]},
            "f_age_anchor": {"filed": PAGE1_REL, "reproduced": True,
                             "prefix_band_shared": R["prefix_band_shared"],
                             "whole_corridor_streak_edges_for_the_shadow_caveat":
                                 R["whole_edges"]},
        },
        "readings": list(READINGS),
    }
    (out / MANIFEST).write_text(json.dumps(man, indent=2, sort_keys=True, default=str)
                                + "\n", encoding="utf-8")
    (out / REPORT).write_text(render_md(R, shas), encoding="utf-8")
    R["manifest"] = man
    R["shas"] = shas
    return R


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    od = next((a.split("=", 1)[1] for a in args if a.startswith("--out-dir=")), None)
    R = build(Path(od) if od else OUT)
    for name in BOOKS:
        c = R["c_v6"] if name == "v6" else R["c_912"]
        print(f"{name}: n {len(c)} · ΣR {float(c['net_r'].sum()):+.6f} · book sha "
              f"{R['shas'][name]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
