#!/usr/bin/env python
"""TIER-C10 · STAGE A — THE TAPE AND THE STAMPS.

RATIFIED operator 2026-09-21 (contract TIER-C10 · TWELVE UNSEEN ASSETS + THE
RANGE CENSUS + THREE SETUPS ON TRIAL; Stage A "TAPE + STAMPS").  Drafted
APOLLO, executed HEPHAESTUS; seed 20260921.

WHAT THIS IS.  Two objects, and the wall between them is the point of the
whole stage:

  1. THE FUNNEL EXTRACTOR — an N-ASSET reading of a card's own life.  Every
     funnel instant of every card: `arming` · `window_open` · `window_close` ·
     `reject` (with its reason) · `trigger` · `entry` · `anchor_bar` ·
     `plus_1r` · `harvest` · `advance` · `pivot_bar` · `bell` · `exit`.  It is
     written HERE rather than in `tierc5q.build_tape` because that function is
     hardwired to `RC.UNIVERSE` and a DAILY spine, and a TIER-C10 panel is
     neither; no tierc2..tierc9 file is edited to get this.
  2. THE STAMPS — the six as-of RangeFinder features the contract names, read
     off the census as-of layer (`tierc10_census.asof_view` / `stamps_at`) at
     the FROZEN SCALE 3.0 [LEAN L2], at the 4h lens of record and — for a lane
     that rides another lens — at that lane's own lens too.

CAPTURED, NEVER CONSULTED.  THE WALL, STATED AS CODE RATHER THAN AS A PROMISE:

  · stamping runs strictly AFTER and OUTSIDE the book.  `stamp_book` takes a
    book that has ALREADY been ridden; nothing here is reachable from a
    decision.  The v6 decision closure (`tierc7_rules` -> tierc2..6_rules ->
    engine) contains no `tierc10_stamps`, no `tierc10_census`, no
    `analytics.rangefinder_census` and nothing named `rangefinder` —
    F-STAMP-CLOSURE proves it by subprocess closure AND by an AST scan that
    sees a LAZY in-function import, which a closure alone would not.
  · the stamps are a PURE LEFT-JOIN on `[asset, instant_ms, instant_kind]`.
    The book's trades come back byte-identical to the unstamped book — proved,
    not asserted, by re-hashing the journal (F-STAMP-JOIN).
  · the spring and BRK lanes DO consume range EVENTS; that is by design and
    happens in their own harness, as precomputed ARGUMENTS.  The law for them
    is the same wall from the other side: their `*_rules`-style decision
    functions import no range code, and NO STAMP IS EVER AN INPUT TO A
    DECISION.  Nothing in this module returns a value a rule card can read.

THE AS-OF LAW.  An instant is stamped with the view AT THE CLOSE OF ITS OWN
BAR, never later: `instant_close_ms = instant_ms + LENS_MS[lane_lens]`, and
`asof_index` takes the LAST bar of the stamp lens CLOSED at or before that
instant.  A 4h instant on the 4h lens therefore reads its own bar; a 5m
instant reads the last 4h bar that had already closed — never the forming one.
F-STAMP-ASOF proves it the only way worth proving: by RECOMPUTING the whole
census layer on a prefix of the tape and demanding the stamps of every instant
at or before the cut are the ones on file.

WHEN NO RANGE IS ALIVE the geometry stamps are EXPLICIT NULLS — never the last
corpse's box (census [LEAN C-b], and F-STAMP-NULLS re-proves it at this layer
against a deliberately forward-filled twin).

Run: NAIAD_CACHE_DIR=~/.cache/naiad/snapshots/tc10_20260921 \\
     ~/venvs/naiad/bin/python -B scripts/tierc10_stamps.py [--rerun]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = Path.home() / ".cache" / "naiad" / "snapshots" / "tc10_20260921"
LIVE_CACHE = Path.home() / ".cache" / "naiad" / "data_cache"


def assert_substrate() -> Path:
    """THE FROZEN-SUBSTRATE GUARD [HARD LAW 3] — before any engine import.

    HALTS IF: NAIAD_CACHE_DIR is unset, is the live cache, or is anything but
    the TC10 snapshot.  Restated here (rather than imported) so this module
    halts on its own word and not on another module's import order.
    """
    env = os.environ.get("NAIAD_CACHE_DIR", "")
    if not env:
        raise SystemExit("HALT: NAIAD_CACHE_DIR is unset — TC10 reads ONLY the "
                         f"snapshot {SNAPSHOT}")
    got = Path(env).expanduser().resolve()
    if got == LIVE_CACHE.resolve():
        raise SystemExit("HALT: NAIAD_CACHE_DIR is the LIVE cache — READ-NEVER, "
                         "WRITE-NEVER for TC10")
    if got != SNAPSHOT.resolve():
        raise SystemExit(f"HALT: NAIAD_CACHE_DIR={got} is not the TC10 snapshot "
                         f"{SNAPSHOT}")
    if not (got / "klines").is_dir():
        raise SystemExit(f"HALT: snapshot has no klines/ directory: {got}")
    return got


assert_substrate()

import numpy as np                                                   # noqa: E402
import pandas as pd                                                  # noqa: E402

sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import tierc10_census as C                                           # noqa: E402
import tierc10_panel as TP                                           # noqa: E402
import tierc9 as T9                                                  # noqa: E402
import tierc7 as T7                                                  # noqa: E402
import tierc2_baseline as TB                                         # noqa: E402

iso, r6, assert_key = TB.iso, TB.r6, TB.assert_key

SEED = 20260921                 # this module draws nothing at random; the seed
                                # is threaded so a later consumer cannot invent
                                # one (F-DET / LEAN L8)
SEED_LINEAGE = 20260816         # the sensitivity echo [LEAN L8]
OUT = ROOT / "research_outputs" / "tierc10" / "stamps"
OUT_RERUN = ROOT / "research_outputs" / "tierc10_run2" / "stamps"

LENS_MS = dict(C.LENS_MS)       # 5m · 4h · 1d — the census's own object
LENS_OF_RECORD = "4h"           # the Stage-A lens every instant is stamped on
FROZEN_SCALE = C.FROZEN_SCALE   # 3.0, BY OBJECT [LEAN L2] — never a literal

# ═══════════════════════════════════════════════════════ 0 · THE VOCABULARY
# THE FUNNEL, IN ORDER.  This tuple IS the contract's list ("arming,
# window-open, trigger/entry, rejects with reason, +1R, harvest, ratchet
# advances, bell, exit") plus the three bars the lineage's own tape already
# carried because they are bars a PRICE was quoted from (`anchor_bar`,
# `pivot_bar`) or a window closed at (`window_close`) — tierc5q.ledger_rows
# added the first two on the same reasoning: "a book that prints those prices
# and cannot say what the walls looked like at the bar they came from is not
# queryable, it is nearly queryable".
INSTANT_KINDS = (
    "arming",        # the 12/89 cross in direction — the unit the funnel counts
    "window_open",   # the bar the entry window opens (card v6: the arming bar)
    "window_close",  # the counter 12/89 cross that shuts it (exclusive)
    "reject",        # the bar the arming's terminal reason became knowable
    "trigger",       # the first in-window 12/26 cross
    "entry",         # the fill (card v6: the trigger bar's close)
    "anchor_bar",    # the (5,5) pivot bar the ENTRY STOP was quoted from
    "plus_1r",       # first bar whose FAVOURABLE extreme reaches +1R (v6 latch)
    "harvest",       # 50% off at the first armed band-edge touch
    "advance",       # one ratchet advance (the confirming bar)
    "pivot_bar",     # the (2,2) pivot bar that advance's stop was quoted from
    "bell",          # a counter 12/89 or 89/316 cross that ended the campaign
    "exit",          # every campaign ends here, whatever the reason
)
ENTERED = "entered"

# THE REJECT LADDER — where each terminal reason becomes KNOWABLE.  A reject
# stamped at the arming bar when it was only decided sixty bars later would be
# a look-ahead in the opposite direction: it would claim the walls of a bar
# nobody was standing on when the funnel closed.
REJECT_BAR_LAW = {
    "tide":          "arm_i — the tide is evaluated AT the arming bar (card law)",
    "d":             "arm_i — displacement is measured AT the arming bar",
    "no_trigger":    "the LAST bar the window searched, min(window_end_i, hi_i+1) - 1",
    "position_open": "trigger_i — the candidate is refused when it is offered",
    "unset":         "trigger_i — tierc9.replay9 leaves `reject` EMPTY on the "
                     "degenerate-R and no-struct-anchor paths (see FINDINGS)",
}

# ═══════════════════════════════════════════════════ THE STAMPS, DEFINED
# Printed as a table on every run and filed as `stamp_defs.parquet`: a column
# whose meaning lives only in a build document is a column somebody will read
# wrong.  `feature` names the SIX the contract asks for; `role` says whether a
# column IS one of the six or rides beside it.
STAMP_DEFS = (
    ("macro_state", "THE SIX · 1",
     "The RangeFinder's macro state as-of this bar's close, four-valued: "
     "'NEUTRAL' a CONFIRMED macro range is alive (confirm_i <= t < die_i) · "
     "'BULL_EXP' / 'BEAR_EXP' no range is alive and the machine's latch holds "
     "an expansion after a breakout-die on the top / bottom side · 'NONE' no "
     "range is alive AND the machine has sealed no pivot yet (nothing is "
     "known). See [LEAN S-a]."),
    ("in_range", "beside",
     "True iff a CONFIRMED macro range is alive as-of this bar's close. It is "
     "the switch every geometry stamp below is nulled by; a reader who wants "
     "the strict two-valued state takes `macro_state if in_range else NONE`."),
    ("range_id", "beside",
     "The machine's `rid` of the live range, or null. Two instants carrying "
     "the same rid stood inside the same box."),
    ("pct_of_range", "THE SIX · 2",
     "100 * (close - bottom) / (top - bottom) at this bar, on the AS-OF box "
     "(top0/bottom0 moved by each harden already KNOWN, never a later "
     "redraw). UNCLAMPED: a body outside the box reads <0 or >100."),
    ("dist_boundary_atr", "THE SIX · 3",
     "min(|top - close|, |close - bottom|) / ATR14 at this bar — the distance "
     "to the NEAREST as-of boundary in ATR units."),
    ("nearest_side", "THE SIX · 3 (side)",
     "'top' or 'bottom': which boundary `dist_boundary_atr` measured. A tie "
     "reads 'top' (the snapshot's own law)."),
    ("boundary_age", "THE SIX · 4",
     "Bars since the NEAREST boundary's as-of VALUE last changed: set at the "
     "confirm bar, moved by each same-side harden FROM the harden bar; 0 on "
     "the bar it changes [census LEAN C-a]. Never from `backdated_from`."),
    ("range_age", "beside",
     "Bars since the range's CONFIRM bar (t - confirm_i). Rides beside "
     "boundary_age because the two answer different questions."),
    ("dev_top", "THE SIX · 5 (top)",
     "Deviations SO FAR on the top side: hardens of this range on that side "
     "with a harden bar at or before t. 0 inside a range that has had none."),
    ("dev_bot", "THE SIX · 5 (bottom)",
     "The same on the bottom side."),
    ("inception_top", "beside",
     "1 if the range's DEFINING wick on the top side already lay beyond the "
     "body boundary at confirm (the inception zone), else 0."),
    ("inception_bot", "beside", "The same on the bottom side."),
    ("last_flip", "THE SIX · 6 (polarity)",
     "Polarity of the last memory-line flip KNOWN at this bar (touch + "
     "FLIP_HOLD_BARS <= t): 'support' or 'resistance', null if none is known "
     "yet. THIS FIELD SURVIVES A DEAD RANGE BY DEFINITION — the leash outlives "
     "the box it came from — and is the one exception to the null law."),
    ("last_flip_age", "THE SIX · 6 (age)",
     "Bars since that flip became KNOWN (not since its touch bar). Null when "
     "no flip is known. Survives a dead range, as above."),
    ("state_latch", "disclosure",
     "The census layer's RAW latch name at this bar, before the four-valued "
     "collapse above. Filed so the collapse is auditable rather than trusted."),
    ("bar_open_ms", "as-of warranty",
     "OPEN ms of the stamp lens bar the view was read at — the bar the "
     "instant could actually see."),
    ("bar_close_ms", "as-of warranty",
     "Its CLOSE ms. THE WARRANTY: bar_close_ms <= instant_close_ms on every "
     "row of every table, always. F-STAMP-ASOF fails if one row breaks it."),
    ("bar_lag", "as-of warranty",
     "Whole bars of the STAMP lens between the stamp bar's close and the "
     "instant's own close. 0 on a same-lens instant, and 0 on a finer-lens "
     "instant too (the coarse bar it reads is the one that had just closed); "
     ">= 0 always, never negative."),
    ("bar_lag_ms", "as-of warranty",
     "The same gap in MILLISECONDS, exact and lens-agnostic — the column that "
     "shows HOW STALE a coarse-lens view was at a fine-lens instant, which "
     "`bar_lag` in whole bars rounds to zero. Always in [0, one stamp-lens "
     "bar) on a gapless tape."),
)
STAMP_FIELDS = tuple(d[0] for d in STAMP_DEFS)
# The six the contract names, as the columns that carry them.
THE_SIX = ("macro_state", "pct_of_range", "dist_boundary_atr", "boundary_age",
           ("dev_top", "dev_bot"), ("last_flip", "last_flip_age"))
# Nulled the moment no range is alive — the forward-fill ban, as a list.
GEOMETRY_FIELDS = ("range_id", "pct_of_range", "dist_boundary_atr", "nearest_side",
                   "boundary_age", "range_age", "dev_top", "dev_bot",
                   "inception_top", "inception_bot")
# Survive a dead range by definition (the stated exception).
LEASH_FIELDS = ("last_flip", "last_flip_age")

MACRO_STATES = ("NONE", "NEUTRAL", "BULL_EXP", "BEAR_EXP")

# CAPTURED-NOT-CONSULTED, AS A LIST F-STAMP-CLOSURE READS.  No module of the v6
# decision path may reach any of these — by import closure OR by a lazy import
# a closure would never see.  `rangefinder` is matched on any dotted part, which
# is what catches `analytics.rangefinder_census` and `engine.rangefinder` alike
# (OR-1's F-BR-14 regex, same word, same reason).
FORBIDDEN_IN_DECISION = ("tierc10_stamps", "tierc10_census", "rangefinder")
# The modules that ARE the v6 decision path: the rules chain and the de-aliased
# runner that rides it.  Named here so the fixture cannot quietly check a
# smaller set than the one the control actually decided with.
DECISION_MODULES = ("tierc7_rules", "tierc6_rules", "tierc5_rules",
                    "tierc4_rules", "tierc3_rules", "tierc2_rules", "tierc9")
# A stamp column, read anywhere in the decision path, would be the wall
# breached from the inside: the prefix is scanned for as a literal.
STAMP_COLUMN_PREFIX = "rf"

LEANS = (
    "[LEAN-HEPHAESTUS] L2 SCALE_MULT: every Stage-A stamp uses the FROZEN 3.0 "
    "(Pine/twin pin of record), read BY OBJECT from tierc10_census.FROZEN_SCALE. "
    "The self-calibrated SCALE is a CENSUS-R report-only object and may not reach "
    "a stamp.",
    "[LEAN-HEPHAESTUS] L4 as-of anchoring: an instant is stamped at the close of "
    "ITS OWN bar (instant_ms + the LANE lens's step), and the stamp bar is the "
    "last bar of the STAMP lens closed at or before that instant. A bar still "
    "forming at the instant is never read.",
    "[LEAN-HEPHAESTUS] L6 Panels: the control is card v6 on CLASSIC5 = BTC ETH "
    "SOL NEAR ZEC; the twelve unseen assets are NOT ridden here and no lane but "
    "the known control is ridden anywhere in this module.",
    "[LEAN-HEPHAESTUS] L8 seed 20260921 threaded explicitly; sensitivity echo "
    "20260816. Nothing in Stage A draws at random — the seeds ride the manifest "
    "so a later consumer cannot invent one.",
    "[LEAN-HEPHAESTUS] S-a MACRO STATE IS FOUR-VALUED. The contract says the "
    "stamps are explicit nulls with macro_state='NONE' when no macro range is "
    "alive. Taken to the letter that would collapse BULL_EXP and BEAR_EXP — the "
    "machine's post-DIE expansion latch, a genuine as-of fact and the most "
    "useful half of the column — into 'NONE', because at SCALE 3.0 the latch is "
    "non-zero on exactly the bars where no range is alive. So: every GEOMETRY "
    "stamp is null the moment no range is alive (the forward-fill ban in full), "
    "and macro_state reads 'NONE' only when no range is alive AND the machine "
    "has sealed no pivot — nothing known. `in_range` is filed beside it, so the "
    "strict two-valued reading is one filter away and nothing is lost either "
    "way.",
    "[LEAN-HEPHAESTUS] S-b THE +1R INSTANT is the card's OWN latch bar, not a "
    "breakeven floor: the first bar j in (entry_i, exit_i] whose FAVOURABLE "
    "extreme reaches entry + 1R — the bar `trail_arm_after_r = 1.0` arms the "
    "ratchet on. It is re-derived from the raw 4h bars because the ride records "
    "the latch (`reached_1r`) and not its bar, and the extractor HALTS if its "
    "re-derivation and the ride's latch ever disagree on one campaign.",
    "[LEAN-HEPHAESTUS] S-c A REJECT IS STAMPED WHERE IT BECAME KNOWABLE, not at "
    "the arming bar: tide/d at the arming bar, no_trigger at the last bar the "
    "window searched, position_open at the trigger bar. REJECT_BAR_LAW carries "
    "the rule per reason and rides every reject row.",
    "[LEAN-HEPHAESTUS] S-d `window_open` is emitted as its own instant although "
    "card v6 opens the window AT the arming bar (the 12/89 cross is both). The "
    "two rows are equal BY CONSTRUCTION on v6 and a fixture leg demands it; they "
    "are kept apart so a later card whose arming and window differ needs no new "
    "vocabulary.",
)
LEAN_TAG = "[LEAN-HEPHAESTUS]"

TIER = "TIER-E MEASUREMENT — UNSCORED, GATES NOTHING"
GATES = ("NOTHING. Stage A CAPTURES; it consults nothing and decides nothing. No "
         "registration rests on any row here, none is implied, and no cell of the "
         "cross-tab may be promoted to a claim.")
WARRANTY = ("these stamps are true AS OF the bar named on the row and of no other; "
            "the corridor advances with the cache [TC6V-a, carried by TIER-C10]. "
            "RangeFinder pins are the frozen pins of record at SCALE 3.0, "
            "calibrated on BTC only: every other asset is an extrapolation.")

LOG_LINES: list[str] = []


def log(msg: str = "") -> None:
    print(msg)
    LOG_LINES.append(msg)


def clock(msg: str) -> None:
    """Timing goes to stdout ONLY — never into a filed artifact, or F-DET
    would compare two wall clocks and call the code non-deterministic."""
    print(msg)


def file_sha256(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def code_sha() -> str:
    return file_sha256(Path(__file__))


def _iso_ms(s: str) -> int:
    """An ISO instant back to epoch ms.  `tierc2_baseline._ms` parses the
    estate's DATE form ('2020-01-21') and not the journal's full stamp
    ('2020-01-21T16:00:00Z'), so the journal path parses its own."""
    return int(pd.Timestamp(str(s)).tz_convert("UTC").value // 1_000_000)


def _ms_to_id(ms: int) -> str:
    t = iso(int(ms))
    return f"{t[:4]}{t[5:7]}{t[8:10]}T{t[11:13]}{t[14:16]}"


def campaign_id(asset: str, lane: str, entry_ms: int) -> str:
    """`ETHUSDT:card:20251029T1600` — tierc5q.campaign_id's form, verbatim, so
    a TC10 row joins a TC5-Q row by eye and by key."""
    return f"{asset}:{lane}:{_ms_to_id(entry_ms)}"


def arm_id(asset: str, arm_ms: int, direction: int) -> str:
    """`ETHUSDT:arm:20251029T1600:L` — the unit id of an arming that never
    became a campaign. The direction rides it because the funnel counts an
    arming per direction, and two directions may not share an id."""
    return f"{asset}:arm:{_ms_to_id(arm_ms)}:{'L' if direction > 0 else 'S'}"


# ══════════════════════════════════════ 1 · THE FUNNEL EXTRACTOR (N-ASSET)
class LaneBars:
    """The RAW bars a lane's `*_i` indices point into, on the lane's OWN lens.

    A `Trade`'s indices are indices into the frame its runner rode: the shared
    4h frame for a card lane, a 5m or 1d tape for a BRK lane.  Reading a 5m
    campaign's `entry_i` off a 4h frame would silently name a bar six years
    away, so the frame is chosen by the lane's lens and then CHECKED against
    the record's own timestamps (`open_ms[entry_i] == entry_ms`) on every
    campaign.  That check is what makes `stamp_book` safe to point at a lane
    nobody has written yet.
    """

    def __init__(self, asset: str, lens: str):
        self.asset, self.lens = asset, lens
        if lens == LENS_OF_RECORD:
            f = T9.frame(asset)["f"]            # the indices' native home
            self.open_ms, self.h, self.l, self.c = f.open_ms, f.h, f.l, f.c
        else:
            tp = C.load_tape(asset, lens)
            self.open_ms, self.h, self.l, self.c = tp.t0, tp.h, tp.l, tp.c

    def bar_of(self, ms: int, what: str) -> int:
        """The index of the bar OPENING at `ms` — exact, never nearest."""
        i = int(np.searchsorted(self.open_ms, int(ms)))
        if i >= len(self.open_ms) or int(self.open_ms[i]) != int(ms):
            raise SystemExit(f"HALT: {self.asset} {self.lens}: {what} names "
                             f"{iso(int(ms))}, which is not a bar of this lens")
        return i

    def check(self, t) -> None:
        for name in ("arm", "entry", "exit"):
            i, ms = getattr(t, f"{name}_i", None), getattr(t, f"{name}_ms", None)
            if i is None or ms is None or int(i) < 0:
                continue
            if int(i) >= len(self.open_ms) or int(self.open_ms[int(i)]) != int(ms):
                raise SystemExit(
                    f"HALT: {t.symbol}: the campaign's {name}_i={i} does not "
                    f"open at {name}_ms={iso(int(ms))} on the {self.lens} lens "
                    "— the book was ridden on a different lens than `lens` says")


def _plus_1r_bar(f, t) -> int | None:
    """The card's OWN +1R latch bar [LEAN S-b].

    `tierc6._ride` / `tierc9._ride_leg9` update the latch at the TOP of each
    bar j in (entry_i, exit_i], BEFORE the stop test, so the exit bar counts.
    `fav` is the high on a long and the low on a short; the comparison is
    `(fav - entry_px) * d / R >= 1.0`, R fixed for the campaign's life.

    WHAT WOULD MAKE THIS WRONG: starting at entry_i (the entry bar's own
    extreme is not a post-entry excursion), stopping before exit_i (the ride
    does not), or re-denominating R.
    """
    d, R = int(t.direction), float(t.r_dist)
    ex = f.h if d == 1 else f.l
    for j in range(int(t.entry_i) + 1, int(t.exit_i) + 1):
        if (float(ex[j]) - float(t.entry_px)) * d / R >= 1.0:
            return j
    return None


def _row(unit_id, unit_kind, asset, lane, direction, kind, i, ms, **extra) -> dict:
    r = {"unit_id": unit_id, "unit_kind": unit_kind, "asset": asset, "lane": lane,
         "direction": ("long" if direction > 0 else "short"),
         "instant_kind": kind, "instant_i": int(i), "instant_ms": int(ms),
         "campaign_id": None, "arm_id": None, "seq": 0, "reject_reason": None,
         "reject_bar_law": None, "detail": None}
    r.update(extra)
    return r


def funnel_instants_asset(asset: str, arms: list, trades: list, f: "LaneBars",
                          lo_i: int, hi_i: int) -> list[dict]:
    """EVERY FUNNEL INSTANT OF EVERY CARD, for ONE asset.

    `arms` are the `Arming` records the decision path already produced and
    `trades` the campaigns it already rode — this function REPLAYS NOTHING and
    DECIDES NOTHING.  It reads bar indices off records that exist and turns
    them into (unit, kind, bar) rows.  The single number it re-derives is the
    +1R latch bar, which the ride computes and does not store, and it is held
    against the ride's own latch on every campaign.

    UNITS.  An arming that entered carries its CAMPAIGN's id, so one campaign
    is one timeline; an arming that did not carries its own `arm_id`.  Every
    row says which, in `unit_kind`.

    WHAT WOULD MAKE THIS WRONG: emitting an instant for a bar outside
    [lo_i, hi_i] (the book could not see it), stamping a reject at the arming
    bar when it was decided later [LEAN S-c], or inventing an instant no
    record carries.
    """
    by_entry = {int(t.entry_ms): t for t in trades}
    if len(by_entry) != len(trades):
        raise SystemExit(f"HALT: {asset}: two campaigns share an entry bar — "
                         "one position per asset is the card's law")
    n = len(f.c)
    out: list[dict] = []
    seen_arm_entry: set[int] = set()

    for a in arms:
        d = int(a.direction)
        ai = int(a.arm_i)
        if not (lo_i <= ai <= hi_i):
            raise SystemExit(f"HALT: {asset}: arming at bar {ai} lies outside the "
                             f"book's window [{lo_i}, {hi_i}]")
        entered = bool(a.entered)
        t = by_entry.get(int(a.trigger_ms)) if (entered and a.trigger_ms) else None
        if entered and t is None:
            raise SystemExit(f"HALT: {asset}: arming at bar {ai} says entered but no "
                             "campaign carries its trigger bar")
        aid = arm_id(asset, int(a.arm_ms), d)
        cid = campaign_id(asset, t.lane, int(t.entry_ms)) if t is not None else None
        uid = cid if cid is not None else aid
        ukind = "campaign" if cid is not None else "arming"
        base = dict(campaign_id=cid, arm_id=aid)

        out.append(_row(uid, ukind, asset, "card", d, "arming", ai, int(a.arm_ms),
                        detail=f"disp={a.disp:.6f} tide_ok={bool(a.tide_ok)} "
                               f"d_ok={bool(a.d_ok)}", **base))
        # [LEAN S-d] card v6 opens the window AT the arming cross; kept apart.
        out.append(_row(uid, ukind, asset, "card", d, "window_open", ai,
                        int(a.arm_ms), detail="card v6: the 12/89 cross that "
                        "arms IS the bar the window opens", **base))
        we = int(a.window_end_i)
        # A window that shuts AFTER the book's corridor end never touched the
        # book — the trigger search is bounded by min(window_end_i, hi_i + 1) —
        # and stamping it would read a bar past the as-of pin.  Not emitted.
        if we < n and we <= hi_i:
            out.append(_row(uid, ukind, asset, "card", d, "window_close", we,
                            int(f.open_ms[we]),
                            detail="the counter 12/89 cross; the window is "
                                   "exclusive of this bar", **base))
        reason = str(a.reject or "")
        if reason != ENTERED:
            if reason in ("tide", "d"):
                ri = ai
            elif reason == "no_trigger":
                ri = min(we, hi_i + 1) - 1
            elif reason in ("position_open", ""):
                if a.trigger_i is None:
                    raise SystemExit(
                        f"HALT: {asset}: arming at bar {ai} rejects "
                        f"{reason or 'UNSET'} with no trigger bar — the reject "
                        "ladder cannot place it")
                ri = int(a.trigger_i)
            else:
                raise SystemExit(f"HALT: {asset}: unknown reject reason {reason!r} "
                                 f"— the reject ladder has no bar for it")
            key = reason if reason else "unset"
            out.append(_row(uid, ukind, asset, "card", d, "reject", ri,
                            int(f.open_ms[ri]), reject_reason=key,
                            reject_bar_law=REJECT_BAR_LAW[key], **base))
        if a.trigger_i is not None:
            out.append(_row(uid, ukind, asset, "card", d, "trigger",
                            int(a.trigger_i), int(a.trigger_ms), **base))
        if t is not None:
            seen_arm_entry.add(int(t.entry_ms))
            out += campaign_instants(t, f, cid, aid)

    orphan = sorted(set(by_entry) - seen_arm_entry)
    if orphan:
        raise SystemExit(f"HALT: {asset}: {len(orphan)} campaign(s) have no arming "
                         f"in the funnel, e.g. {iso(orphan[0])}")
    return out


def campaign_instants(t, f: "LaneBars", cid: str | None = None,
                      aid: str | None = None) -> list[dict]:
    """The instants a CAMPAIGN owns, from the `Trade` record alone.

    Split out from the arming walk because a lane with no arming concept — the
    spring lane, either BRK lane — still has entry / +1R / harvest / advances /
    bell / exit, and `stamp_book` must be able to read a book of such trades
    with no `arms` at all.
    """
    d = int(t.direction)
    cid = cid or campaign_id(t.symbol, t.lane, int(t.entry_ms))
    base = dict(campaign_id=cid, arm_id=aid)
    lane = str(t.lane)
    f.check(t)
    out = [_row(cid, "campaign", t.symbol, lane, d, "entry", int(t.entry_i),
                int(t.entry_ms),
                detail=f"r_dist={r6(t.r_dist)} atr={r6(t.atr_at_entry)}", **base)]
    if int(getattr(t, "anchor_bar_ms", -1) or -1) > 0:
        ab = f.bar_of(int(t.anchor_bar_ms), "anchor_bar_ms")
        out.append(_row(cid, "campaign", t.symbol, lane, d, "anchor_bar", ab,
                        int(t.anchor_bar_ms),
                        detail=f"entry stop quoted from this pivot "
                               f"(anchor={r6(t.anchor)})", **base))
    j1 = _plus_1r_bar(f, t)
    if (j1 is not None) != bool(t.reached_1r):
        raise SystemExit(
            f"HALT: {t.symbol} {iso(int(t.entry_ms))}: the +1R re-derivation "
            f"({'found bar ' + str(j1) if j1 is not None else 'found none'}) "
            f"disagrees with the ride's own latch (reached_1r={bool(t.reached_1r)}). "
            "The extractor must read the card's latch, never a second opinion.")
    if j1 is not None:
        out.append(_row(cid, "campaign", t.symbol, lane, d, "plus_1r", j1,
                        int(f.open_ms[j1]),
                        detail="first FAVOURABLE extreme at or beyond +1R — the "
                               "bar the v6 ratchet arms on", **base))
    if bool(t.harvested):
        out.append(_row(cid, "campaign", t.symbol, lane, d, "harvest",
                        int(t.harvest_i), int(t.harvest_ms),
                        detail=f"unit_move_r={r6(t.harvest_unit_move_r)}", **base))
    for k, adv in enumerate(t.advances):
        out.append(_row(cid, "campaign", t.symbol, lane, d, "advance",
                        int(adv.conf_i), int(adv.conf_ms), seq=k + 1,
                        detail=f"stop {r6(adv.prev_stop)} -> {r6(adv.new_stop)} "
                               f"({'RAIL' if adv.rail_binding else 'PIVOT'})",
                        **base))
        out.append(_row(cid, "campaign", t.symbol, lane, d, "pivot_bar",
                        f.bar_of(int(adv.pivot_bar_ms), "pivot_bar_ms"),
                        int(adv.pivot_bar_ms), seq=k + 1,
                        detail=f"advance {k + 1}'s pivot (val={r6(adv.pivot_val)})",
                        **base))
    if str(t.exit_reason).startswith("bell"):
        out.append(_row(cid, "campaign", t.symbol, lane, d, "bell", int(t.exit_i),
                        int(t.exit_ms), detail=str(t.exit_reason), **base))
    out.append(_row(cid, "campaign", t.symbol, lane, d, "exit", int(t.exit_i),
                    int(t.exit_ms), detail=str(t.exit_reason), **base))
    return out


# THE KINDS A JOURNAL FRAME CANNOT CARRY.  A journal is one row per campaign:
# it holds the bars a campaign ARRIVED at and left, not the bars it passed
# through, and it holds nothing at all about the armings that never became
# campaigns.  Named here rather than left to be discovered as a gap in a
# coverage table somebody skims.
JOURNAL_BLIND = ("window_open", "window_close", "reject", "trigger",
                 "plus_1r", "advance", "pivot_bar")


def journal_instants(row, f: "LaneBars") -> list[dict]:
    """The instants a JOURNAL ROW can honestly carry: arming · entry ·
    anchor_bar · harvest · bell · exit.

    NOT a second implementation of `campaign_instants` — a STRICTLY SMALLER
    one, because a journal row is a strictly smaller record.  The seven kinds
    it cannot reach are named in `JOURNAL_BLIND`, counted in the coverage table
    and flagged in the returned meta; a caller who needs them must hand over
    the `Trade` records.  F-STAMP-JOURNAL demands that the instants this path
    DOES produce are identical, stamp for stamp, to the Book path's.
    """
    asset, lane = str(row["asset"]), str(row["lane"])
    d = 1 if str(row["direction"]) == "long" else -1
    cid = campaign_id(asset, lane, int(row["entry_ms"]))
    base = dict(campaign_id=cid, arm_id=None)
    out = []
    if row.get("arm_ms") is not None and int(row["arm_ms"]) > 0:
        i = f.bar_of(int(row["arm_ms"]), "arm_ms")
        out.append(_row(cid, "campaign", asset, lane, d, "arming", i,
                        int(row["arm_ms"]), detail="from the journal frame",
                        **base))
    ei = f.bar_of(int(row["entry_ms"]), "entry_ms")
    out.append(_row(cid, "campaign", asset, lane, d, "entry", ei,
                    int(row["entry_ms"]),
                    detail=f"r_dist={r6(row['r_dist'])} "
                           f"atr={r6(row['atr_at_entry'])}", **base))
    for col, kind, note in (("anchor_bar_ts", "anchor_bar",
                             "entry stop quoted from this pivot"),
                            ("harvest_ts", "harvest", "from the journal frame")):
        v = row.get(col)
        if v is None or (isinstance(v, float) and np.isnan(v)) or not str(v):
            continue
        ms = _iso_ms(str(v))
        out.append(_row(cid, "campaign", asset, lane, d, kind,
                        f.bar_of(ms, col), ms, detail=note, **base))
    xi = f.bar_of(int(row["exit_ms"]), "exit_ms")
    if str(row["exit_reason"]).startswith("bell"):
        out.append(_row(cid, "campaign", asset, lane, d, "bell", xi,
                        int(row["exit_ms"]), detail=str(row["exit_reason"]),
                        **base))
    out.append(_row(cid, "campaign", asset, lane, d, "exit", xi,
                    int(row["exit_ms"]), detail=str(row["exit_reason"]), **base))
    return out


def funnel_frame(rows: list[dict], lane_lens: str) -> pd.DataFrame:
    """The instants, as a keyed frame.  `instant_close_ms` is the instant's own
    bar CLOSE — the only timestamp a stamp may be taken at."""
    d = pd.DataFrame(rows, columns=["unit_id", "unit_kind", "asset", "lane",
                                    "direction", "instant_kind", "instant_i",
                                    "instant_ms", "campaign_id", "arm_id", "seq",
                                    "reject_reason", "reject_bar_law", "detail"])
    if not len(d):
        return d
    d["lane_lens"] = lane_lens
    d["instant_close_ms"] = d["instant_ms"].astype("int64") + LENS_MS[lane_lens]
    d["instant_ts"] = [iso(int(v)) for v in d["instant_ms"]]
    order = {k: i for i, k in enumerate(INSTANT_KINDS)}
    d["_k"] = d["instant_kind"].map(order)
    if d["_k"].isna().any():
        bad = sorted(set(d.loc[d["_k"].isna(), "instant_kind"]))
        raise SystemExit(f"HALT: instant kind(s) outside the vocabulary: {bad}")
    d = (d.sort_values(["asset", "instant_ms", "_k", "unit_id", "seq"],
                       kind="mergesort").drop(columns="_k").reset_index(drop=True))
    return d


# ═══════════════════════════════════════════════ 2 · THE STAMP LAYER
_VIEWS: dict = {}


def asof_layer(asset: str, lens: str) -> tuple:
    """(tape, view) for one (asset, lens) at the FROZEN SCALE [LEAN L2].

    Memoised per process because a five-asset control stamps the same five
    views many times over; the memo is keyed on (asset, lens) AND the scale is
    a module constant, so no caller can slip a different SCALE past it — the
    poisoned-cache lesson of F-C8-MATCH, one tier later.
    """
    k = (asset, lens)
    if k not in _VIEWS:
        tape = C.load_tape(asset, lens)
        rv = C.run_scale(tape, FROZEN_SCALE)
        _VIEWS[k] = (tape, C.asof_view(tape, rv["macro"], rv["leash"]))
    return _VIEWS[k]


def macro_state_of(view: dict, idx: int) -> str:
    """THE FOUR-VALUED COLLAPSE [LEAN S-a].  `idx < 0` (no bar of this lens has
    closed at the instant) reads 'NONE': nothing was knowable, which is exactly
    what 'NONE' says."""
    if idx < 0:
        return "NONE"
    if bool(view["in_range"][idx]):
        return "NEUTRAL"
    s = int(view["state"][idx])
    return C.STATE_NAME[s] if s else "NONE"


def stamps_at(tape, view: dict, idx: int, instant_close_ms: int) -> dict:
    """ONE STAMP RECORD, from the census as-of layer.

    The geometry comes straight out of `tierc10_census.stamps_at` — the same
    function CENSUS-R anchors its own outcome ledger with, so a Stage-A stamp
    and a census row can never disagree about a bar.  What this adds is the
    four-valued macro state, the range id, and the three warranty columns that
    make the as-of claim checkable on the row: which bar was read, when it
    closed, and how many bars of lag that was.

    RAISES IF: the bar read closed AFTER the instant did. That is the whole
    warranty, and it is cheaper to assert than to audit.
    """
    s = C.stamps_at(tape, view, idx)
    out = {
        "macro_state": macro_state_of(view, idx),
        "in_range": (bool(s["rf_in_range"]) if s["rf_in_range"] is not None
                     else None),
        "range_id": (int(view["rid"][idx]) if idx >= 0
                     and bool(view["in_range"][idx]) else None),
        "pct_of_range": s["rf_pct_of_range"],
        "dist_boundary_atr": s["rf_dist_boundary_atr"],
        "nearest_side": s["rf_nearest_side"],
        "boundary_age": s["rf_boundary_age"],
        "range_age": s["rf_range_age"],
        "dev_top": s["rf_dev_top"],
        "dev_bot": s["rf_dev_bot"],
        "inception_top": s["rf_inception_top"],
        "inception_bot": s["rf_inception_bot"],
        "last_flip": s["rf_last_flip"],
        "last_flip_age": s["rf_last_flip_age"],
        "state_latch": (C.STATE_NAME[int(view["state"][idx])] if idx >= 0
                        else None),
        "bar_open_ms": (int(tape.t0[idx]) if idx >= 0 else None),
        "bar_close_ms": s["rf_bar_close_ms"],
        "bar_lag": (int((int(instant_close_ms) - int(s["rf_bar_close_ms"]))
                        // tape.step) if idx >= 0 else None),
        "bar_lag_ms": (int(int(instant_close_ms) - int(s["rf_bar_close_ms"]))
                       if idx >= 0 else None),
    }
    if out["bar_close_ms"] is not None and out["bar_close_ms"] > int(instant_close_ms):
        raise SystemExit(
            f"HALT (as-of): {tape.sym} {tape.lens}: a stamp read the bar closing "
            f"{iso(out['bar_close_ms'])} for an instant that closed "
            f"{iso(int(instant_close_ms))} — the view ran ahead of the tape")
    if out["bar_lag"] is not None and out["bar_lag"] < 0:
        raise SystemExit(f"HALT (as-of): negative bar lag on {tape.sym} {tape.lens}")
    return out


def stamp_table(asset: str, instants: pd.DataFrame, lens: str) -> pd.DataFrame:
    """The stamp frame for one asset on one lens, keyed
    `[asset, instant_ms, instant_kind]` — the join key of record.

    ONE STAMP PER DISTINCT INSTANT.  Two campaigns rejected on the same bar
    read the same walls, so the key is deduplicated here and the join is m:1.
    Building it distinct (rather than row-by-row) is what makes the join
    PROVABLY pure: a left-join onto a frame that is unique on the key can
    neither drop a row nor multiply one, and F-STAMP-JOIN re-checks the count
    on both sides anyway.
    """
    sub = instants[instants["asset"] == asset]
    keys = (sub[["instant_ms", "instant_kind", "instant_close_ms"]]
            .drop_duplicates(subset=["instant_ms", "instant_kind"])
            .sort_values(["instant_ms", "instant_kind"], kind="mergesort"))
    if not len(keys):
        return pd.DataFrame()
    tape, view = asof_layer(asset, lens)
    idx = C.asof_index(tape, keys["instant_close_ms"].to_numpy(np.int64))
    recs = [stamps_at(tape, view, int(i), int(m))
            for i, m in zip(idx, keys["instant_close_ms"])]
    d = pd.DataFrame(recs, columns=list(STAMP_FIELDS))
    d.insert(0, "instant_kind", keys["instant_kind"].to_numpy())
    d.insert(0, "instant_ms", keys["instant_ms"].to_numpy(np.int64))
    d.insert(0, "asset", asset)
    return d.reset_index(drop=True)


def prefix(lens: str) -> str:
    return f"rf{lens}_"


def join_stamps(instants: pd.DataFrame, stamps: pd.DataFrame,
                lens: str) -> pd.DataFrame:
    """THE PURE LEFT-JOIN, and nothing else.

    `[asset, instant_ms, instant_kind]`, validated `m:1`, column-prefixed by
    lens so two lenses never collide.  No row is added, none is dropped, and
    not one column of the book is touched — which is the property F-STAMP-JOIN
    and the closure fixture exist to hold.
    """
    p = prefix(lens)
    s = stamps.rename(columns={c: p + c for c in STAMP_FIELDS})
    assert_key(s, ["asset", "instant_ms", "instant_kind"], f"stamps[{lens}]")
    n0 = len(instants)
    out = instants.merge(s, on=["asset", "instant_ms", "instant_kind"],
                         how="left", validate="m:1")
    if len(out) != n0:
        raise SystemExit(f"HALT (F-STAMP-JOIN): the {lens} join moved the row "
                         f"count {n0} -> {len(out)}; a stamp join is a left-join "
                         "and nothing else")
    miss = int(out[p + "macro_state"].isna().sum())
    if miss:
        raise SystemExit(f"HALT (F-STAMP-JOIN): {miss} instant(s) came back "
                         f"unstamped on the {lens} lens")
    return out


def null_audit(stamped: pd.DataFrame, lens: str) -> pd.DataFrame:
    """F-STAMP-NULLS' OWN EVIDENCE, as a table: per (lens, field), how many
    rows are in range, how many are not, and how many NON-NULL values each
    field carries on the out-of-range rows.

    THE LAW THIS COUNTS: a geometry field must be non-null on ZERO out-of-range
    rows (never the last corpse's box) and non-null on EVERY in-range row; the
    two leash fields are exempt BY DEFINITION and their out-of-range non-nulls
    are counted, printed and expected.
    """
    p = prefix(lens)
    inr = stamped[p + "in_range"].fillna(False).astype(bool)
    rows = []
    for fld in STAMP_FIELDS:
        col = stamped[p + fld]
        nn = col.notna()
        rows.append({
            "lens": lens, "field": fld,
            "law": ("GEOMETRY — null whenever no range is alive"
                    if fld in GEOMETRY_FIELDS else
                    "LEASH — survives a dead range BY DEFINITION"
                    if fld in LEASH_FIELDS else "always present"),
            "n_rows": int(len(stamped)), "n_in_range": int(inr.sum()),
            "n_out_of_range": int((~inr).sum()),
            "n_nonnull_in_range": int((nn & inr).sum()),
            "n_nonnull_out_of_range": int((nn & ~inr).sum()),
            "violates": bool(fld in GEOMETRY_FIELDS and int((nn & ~inr).sum())),
        })
    return pd.DataFrame(rows)


def coverage(instants: pd.DataFrame, stamped: pd.DataFrame,
             lenses: tuple) -> pd.DataFrame:
    """Per instant kind: demanded, stamped, and — per lens — how many stamps
    sit on the instant's OWN bar (lag 0) versus an earlier one.

    WHAT WOULD MAKE THIS FAIL: one instant with no stamp row, or one kind
    present in the vocabulary and absent from the book without the count
    saying zero.  A coverage table that printed only totals would hide a whole
    missing KIND behind a large number.
    """
    rows = []
    for kind in INSTANT_KINDS:
        sub = stamped[stamped["instant_kind"] == kind]
        r = {"instant_kind": kind, "demanded": int((instants["instant_kind"]
                                                    == kind).sum()),
             "stamped": int(len(sub)),
             "units": int(sub["unit_id"].nunique()) if len(sub) else 0}
        for lens in lenses:
            p = prefix(lens)
            r[f"{lens}_unstamped"] = (int(sub[p + "macro_state"].isna().sum())
                                      if len(sub) else 0)
            r[f"{lens}_lag0"] = (int((sub[p + "bar_lag"] == 0).sum())
                                 if len(sub) else 0)
            r[f"{lens}_in_range"] = (int(sub[p + "in_range"].fillna(False)
                                         .astype(bool).sum()) if len(sub) else 0)
        rows.append(r)
    tot = {"instant_kind": "__ALL__", "demanded": int(len(instants)),
           "stamped": int(len(stamped)),
           "units": int(stamped["unit_id"].nunique()) if len(stamped) else 0}
    for lens in lenses:
        p = prefix(lens)
        tot[f"{lens}_unstamped"] = int(stamped[p + "macro_state"].isna().sum())
        tot[f"{lens}_lag0"] = int((stamped[p + "bar_lag"] == 0).sum())
        tot[f"{lens}_in_range"] = int(stamped[p + "in_range"].fillna(False)
                                      .astype(bool).sum())
    return pd.DataFrame(rows + [tot])


# ═══════════════════════════════════════════════════ 3 · THE PUBLIC DOOR
def journal_of(book_or_journal) -> pd.DataFrame:
    """The book's journal, whatever form the book arrived in."""
    if isinstance(book_or_journal, pd.DataFrame):
        return book_or_journal.copy()
    return T7.journal_frame(list(book_or_journal))


def stamp_book(book_or_journal, panel, lens: str = LENS_OF_RECORD,
               arms=None, lo_ms: int | None = None, hi_ms: int | None = None):
    """STAGE A'S ONE DOOR — usable unchanged on any registered book later.

        out = stamp_book(book, TP.CLASSIC5)                     # a 4h lane
        out = stamp_book(book, TP.PANEL17, lens='5m', arms=...) # a 5m lane

    `book_or_journal` is a book that has ALREADY BEEN RIDDEN: a list of
    `tierc5_rules.Trade` records (a `tierc10_panel.Book` is one), or the
    JOURNAL FRAME of one — which carries fewer instant kinds, says which in
    `meta['kinds_unavailable']`, and never pretends otherwise.  `panel` is the
    declared panel the book rode.
    `lens` is THE LANE'S OWN lens: the stamps are always taken on 4h, the lens
    of record, and — when the lane rides another one — on that lens as well.
    `arms` (optional) is the `Arming` list the decision path produced, per
    asset or flat; give it and the funnel carries armings, windows and rejects
    as well as campaigns, which is the difference between "every funnel
    instant" and "every campaign instant".

    Returns a dict:
        instants   the stamped funnel — one row per (unit, kind, bar), with
                   `rf4h_*` (and `rf<lens>_*`) stamp columns
        trades     the journal, BYTE-IDENTICAL to the unstamped book
        coverage · nulls · defs · leans · meta

    THE ORDER IS THE LAW.  The book is ridden by its own runner, BEFORE this
    call; `stamp_book` neither replays a bar nor reads a rule card.  Handing a
    stamp back into a decision would break the wall — no return value here is
    shaped to be read by one, and F-STAMP-CLOSURE proves the decision closure
    cannot reach this module at all.
    """
    if lens not in LENS_MS:
        raise SystemExit(f"HALT: unknown lens {lens!r}; one of {sorted(LENS_MS)}")
    panel = tuple(panel)
    lenses = (LENS_OF_RECORD,) if lens == LENS_OF_RECORD else (LENS_OF_RECORD, lens)
    jr = journal_of(book_or_journal)
    trades = (list(book_or_journal)
              if not isinstance(book_or_journal, pd.DataFrame) else [])

    by_asset: dict = {}
    if arms is not None:
        if isinstance(arms, dict):
            by_asset = {k: list(v) for k, v in arms.items()}
        else:
            for a in arms:
                by_asset.setdefault(a.symbol, []).append(a)

    rows: list[dict] = []
    bars: dict = {}

    def lane_bars(asset: str) -> LaneBars:
        if asset not in bars:
            bars[asset] = LaneBars(asset, lens)
        return bars[asset]

    if by_asset:
        if lens != LENS_OF_RECORD:
            raise SystemExit(
                f"HALT: `arms` are a 4h CARD concept (the 12/89 window); a "
                f"{lens} lane has no Arming records and must be stamped from "
                "its campaigns alone")
        if not trades:
            raise SystemExit("HALT: `arms` needs the Trade records too — an "
                             "arming is matched to its campaign by trigger bar, "
                             "and a journal frame has no arming link")
        if lo_ms is None or hi_ms is None:
            raise SystemExit("HALT: `arms` needs (lo_ms, hi_ms) — the reject "
                             "ladder places `no_trigger` at the last bar the "
                             "window searched, which is the BOOK's window end")
        stray = sorted(set(by_asset) - set(panel))
        if stray:
            raise SystemExit(f"HALT: arms for asset(s) outside the panel: {stray}")
        for asset in panel:
            aa = by_asset.get(asset, [])
            tt = [t for t in trades if t.symbol == asset]
            if not aa and not tt:
                continue
            f = lane_bars(asset)
            lo_i, hi_i = T7._idx_range(f.open_ms, int(lo_ms), int(hi_ms))
            lo_i = max(lo_i, T9.V6_ROLES.floor_bars)
            rows += funnel_instants_asset(asset, aa, tt, f, lo_i, hi_i)
    elif trades:
        stray = sorted({t.symbol for t in trades} - set(panel))
        if stray:
            raise SystemExit(f"HALT: campaign(s) on asset(s) outside the "
                             f"declared panel: {stray}")
        for t in trades:
            rows += campaign_instants(t, lane_bars(t.symbol))
    else:
        stray = sorted(set(jr["asset"]) - set(panel))
        if stray:
            raise SystemExit(f"HALT: journal row(s) on asset(s) outside the "
                             f"declared panel: {stray}")
        for _, r in jr.iterrows():
            rows += journal_instants(r, lane_bars(str(r["asset"])))

    inst = funnel_frame(rows, lens)
    if not len(inst):
        raise SystemExit("HALT: the book yielded no funnel instant — an empty "
                         "tape is not a stamped book")
    assert_key(inst, ["unit_id", "instant_kind", "instant_ms"], "funnel_instants")

    stamped = inst
    stamp_tables = {}
    for ln in lenses:
        parts = [stamp_table(a, inst, ln) for a in panel
                 if (inst["asset"] == a).any()]
        st = pd.concat([p for p in parts if len(p)], ignore_index=True)
        stamp_tables[ln] = st
        stamped = join_stamps(stamped, st, ln)

    nulls = pd.concat([null_audit(stamped, ln) for ln in lenses],
                      ignore_index=True)
    bad = nulls[nulls["violates"]]
    if len(bad):
        raise SystemExit(
            f"HALT (F-STAMP-NULLS): {len(bad)} field(s) carry a value on an "
            f"out-of-range row — a dead range was forward-filled: "
            f"{sorted(set(bad['field']))}")
    return {
        "instants": stamped, "trades": jr,
        "coverage": coverage(inst, stamped, lenses),
        "nulls": nulls, "stamp_tables": stamp_tables,
        "defs": defs_frame(), "leans": leans_frame(),
        "meta": {"panel": list(panel), "panel_name": TP.panel_name(panel),
                 "lane_lens": lens, "stamp_lenses": list(lenses),
                 "source": ("book+arms" if by_asset else
                            "book" if trades else "journal"),
                 "kinds_unavailable": ([] if trades else list(JOURNAL_BLIND)),
                 "kinds_unavailable_note": (
                     "" if trades else
                     "a JOURNAL frame is one row per campaign: it carries the "
                     "bars a campaign arrived at and left, not the bars it "
                     "passed through, and nothing about armings that never "
                     "became campaigns. Hand over the Trade records for those."),
                 "scale_mult": float(FROZEN_SCALE), "seed": SEED,
                 "seed_lineage": SEED_LINEAGE,
                 "n_instants": int(len(stamped)),
                 "n_units": int(stamped["unit_id"].nunique()),
                 "n_campaigns": int(len(jr)),
                 "lo_ms": None if lo_ms is None else int(lo_ms),
                 "hi_ms": None if hi_ms is None else int(hi_ms)},
    }


def defs_frame() -> pd.DataFrame:
    return pd.DataFrame([{"field": f, "role": r, "definition": t,
                          "scale_mult": float(FROZEN_SCALE),
                          "lens_of_record": LENS_OF_RECORD}
                         for f, r, t in STAMP_DEFS])


def leans_frame() -> pd.DataFrame:
    return pd.DataFrame([{"n": i + 1, "lean": s} for i, s in enumerate(LEANS)])


def collar(df: pd.DataFrame, surface: str) -> pd.DataFrame:
    """THE TIER-E COLLAR, in columns — a caption does not survive a copy of the
    row.  `m` is the number of LOOKS this table holds, logged and not
    corrected: nothing here is a test, and there is no verdict column."""
    d = df.copy()
    m = int(len(d))
    d["tier"] = TIER
    d["gates"] = GATES
    d["m_looks_this_table"] = m
    d["m_note"] = (f"m = {m} looks in this table ({surface}). NO multiplicity "
                   "correction is applied and none is needed: NOTHING HERE IS A "
                   "TEST. m is logged so a reader who later turns a cell into a "
                   "claim can see how many ways the tape was cut first.")
    d["in_sample"] = ("the KNOWN CONTROL (card v6, frozen pins, CLASSIC5) — "
                      "ridden by nine tiers; the stamps are new, the book is not")
    d["scored_in_family"] = False
    return d


# ═══════════════════════════════════════ 4 · THE CONTROL, AND ONLY THE CONTROL
def control_book() -> dict:
    """CARD v6, ALL PINS FROZEN, ON CLASSIC5 — the one book this module rides.

    The trades come from `tierc10_panel.run_cell_n`, which is the gated door;
    the armings come from `tierc9.replay9` per asset, because `run_cell_n`
    returns campaigns and the funnel needs the arms that never became one.  The
    two are held together: every campaign of the panel's Book must be the
    campaign `replay9` produced, entry bar for entry bar (F-STAMP-JOIN's first
    leg) — otherwise the funnel would describe a book nobody rode.

    THIS IS THE ONLY BOOK RIDDEN ANYWHERE IN STAGE A.  No unseen asset, no
    swapped trigger, no floor, no lane.  `is_control_book` is what lets it ride
    unregistered, and it is asserted here rather than assumed.
    """
    lo, hi, meta = TP.corridor_n(TP.CLASSIC5)
    if not TP.is_control_book(TP.CONTROL_CARD, T9.V6_ROLES, TP.CLASSIC5):
        raise SystemExit("HALT: the book Stage A is about to ride is not the "
                         "KNOWN CONTROL — Stage A rides nothing else")
    book = TP.run_cell_n(TP.CONTROL_CARD, T9.V6_ROLES, TP.CLASSIC5, lo, hi)
    arms: dict = {}
    trades: list = []
    for s in TP.CLASSIC5:
        a, t = T9.replay9(s, TP.CONTROL_CARD, T9.V6_ROLES, lo, hi)
        arms[s] = a
        trades += t
    same, worst, detail = TP.ctrl_diff(T7.journal_frame(list(book)),
                                       T7.journal_frame(trades))
    if not same:
        raise SystemExit(f"HALT: the panel's Book and the per-asset replay that "
                         f"carries the armings are not the same book — {detail}. "
                         "The funnel would then describe a book nobody rode.")
    log(f"  book identity  panel Book vs the arming replay: {detail}")
    return {"book": book, "arms": arms, "lo_ms": lo, "hi_ms": hi, "meta": meta,
            "book_identity": detail}


def entry_state_crosstab(out: dict) -> pd.DataFrame:
    """TIER-E · THE CONTROL'S OUTCOMES BY MACRO STATE AT ENTRY — report-only.

    One row per macro state the control's entries stood in, plus `__ALL__`.
    Raw per-campaign arithmetic only: n, net R, expectancy, win rate, median
    MFE/MAE.  NO bootstrap, NO CI, NO verdict, NO comparison to zero — this is
    a CROSS-TAB of a book nine tiers have already scored, cut a new way, and a
    cut is not a test.  The collar rides in columns.

    WHAT WOULD MAKE THIS A BREACH: attaching a p-value, ranking the states, or
    reading one cell as a lane.
    """
    inst = out["instants"]
    jr = out["trades"]
    p = prefix(LENS_OF_RECORD)
    ent = inst[inst["instant_kind"] == "entry"][
        ["asset", "instant_ms", p + "macro_state", p + "in_range",
         p + "pct_of_range", p + "dist_boundary_atr"]]
    ent = ent.rename(columns={"instant_ms": "entry_ms"})
    j = jr.merge(ent, on=["asset", "entry_ms"], how="left", validate="1:1")
    if int(j[p + "macro_state"].isna().sum()):
        raise SystemExit("HALT: a campaign's entry instant carries no stamp")
    rows = []
    for key in list(MACRO_STATES) + ["__ALL__"]:
        g = j if key == "__ALL__" else j[j[p + "macro_state"] == key]
        net = g["net_r"].astype(float)
        rows.append({
            "macro_state_at_entry": key, "n": int(len(g)),
            "n_assets": int(g["asset"].nunique()),
            "net_r_sum": r6(float(net.sum())) if len(g) else None,
            "expectancy_r": r6(float(net.mean())) if len(g) else None,
            "median_net_r": r6(float(net.median())) if len(g) else None,
            "win_rate_pct": (r6(100.0 * float((net > 0).mean()))
                             if len(g) else None),
            "median_mfe_r": (r6(float(g["mfe_r"].astype(float).median()))
                             if len(g) else None),
            "median_pct_of_range": (r6(float(g[p + "pct_of_range"]
                                             .astype(float).median()))
                                    if len(g) and g[p + "pct_of_range"].notna().any()
                                    else None),
            "median_dist_boundary_atr": (
                r6(float(g[p + "dist_boundary_atr"].astype(float).median()))
                if len(g) and g[p + "dist_boundary_atr"].notna().any() else None),
            "n_in_range": int(g[p + "in_range"].fillna(False).astype(bool).sum())
            if len(g) else 0,
            "provisional": bool(len(g) < 30),
            "provisional_note": ("n below the lineage's PROVISIONAL_MIN_N = 30"
                                 if len(g) < 30 else ""),
        })
    return collar(pd.DataFrame(rows), "control outcomes by macro state at entry")


def unit_frame(out: dict) -> pd.DataFrame:
    """One row per FUNNEL UNIT — campaign or arming — with the stamp it carried
    at the bar its life turned: the entry bar for a campaign, the reject bar
    for an arming that never became one.  The funnel, as a partition."""
    inst = out["instants"]
    p = prefix(LENS_OF_RECORD)
    turn = inst[inst["instant_kind"].isin(("entry", "reject"))]
    keep = ["unit_id", "unit_kind", "asset", "lane", "direction", "instant_kind",
            "instant_ms", "instant_ts", "campaign_id", "arm_id", "reject_reason"]
    cols = keep + [p + f for f in ("macro_state", "in_range", "pct_of_range",
                                   "dist_boundary_atr", "boundary_age",
                                   "dev_top", "dev_bot", "last_flip",
                                   "last_flip_age", "bar_lag")]
    d = turn[cols].rename(columns={"instant_kind": "turn_kind",
                                   "instant_ms": "turn_ms",
                                   "instant_ts": "turn_ts"})
    return d.sort_values(["asset", "turn_ms", "unit_id"],
                         kind="mergesort").reset_index(drop=True)


def funnel_tally(out: dict) -> pd.DataFrame:
    """The funnel as counts, per asset and per terminal reason — the partition
    `tierc2_rules.Arming` was designed to make checkable: every arming has
    exactly one terminal reason, so the reasons must sum to the armings."""
    u = unit_frame(out)
    rows = []
    for asset, g in u.groupby("asset", sort=True):
        r = {"asset": asset, "armings": int(len(g)),
             "entered": int((g["turn_kind"] == "entry").sum())}
        for reason in ("tide", "d", "no_trigger", "position_open", "unset"):
            r[f"reject_{reason}"] = int((g["reject_reason"] == reason).sum())
        r["partition_holds"] = bool(
            r["armings"] == r["entered"] + sum(r[f"reject_{x}"] for x in
                                               ("tide", "d", "no_trigger",
                                                "position_open", "unset")))
        rows.append(r)
    d = pd.DataFrame(rows)
    tot = {"asset": "__ALL__"}
    for c in d.columns:
        if c == "asset":
            continue
        tot[c] = (bool(d[c].all()) if c == "partition_holds"
                  else int(d[c].sum()))
    return pd.concat([d, pd.DataFrame([tot])], ignore_index=True)


# ═══════════════════════════════════════════════════════════════ THE RUN
def run(root: Path) -> dict:
    t0 = time.time()
    log("=" * 78)
    log("TIER-C10 · STAGE A — the tape and the stamps")
    log("=" * 78)
    sub = TP.substrate()
    log(f"  substrate  {sub['substrate']}  (live cache never read [LAW 3])")
    log(f"  seed {SEED} · sensitivity echo {SEED_LINEAGE} · "
        f"SCALE_MULT {FROZEN_SCALE} (FROZEN, by object) [LEAN L2]")
    log(f"  census code sha {C.code_sha()[:16]}…  stamps code sha "
        f"{code_sha()[:16]}…")
    log("")
    for s in LEANS:
        log(f"  {s}")
    log("")
    log("  THE STAMPS, DEFINED (filed as stamp_defs.parquet):")
    for f_, role, text in STAMP_DEFS:
        log(f"    {f_:<20} [{role}]")
        for line in _wrap(text, 68):
            log(f"      {line}")
    log("")

    ctrl = control_book()
    lo, hi, meta = ctrl["lo_ms"], ctrl["hi_ms"], ctrl["meta"]
    log(f"  CONTROL  card v6 · CLASSIC5 · [{iso(lo)}, {iso(hi + 1)}) — "
        f"{len(ctrl['book'])} campaigns, "
        f"{sum(len(a) for a in ctrl['arms'].values())} armings")
    clock(f"    ... book ridden in {time.time() - t0:.1f}s")

    t1 = time.time()
    out = stamp_book(ctrl["book"], TP.CLASSIC5, lens=LENS_OF_RECORD,
                     arms=ctrl["arms"], lo_ms=lo, hi_ms=hi)
    clock(f"    ... {out['meta']['n_instants']:,} instants stamped in "
          f"{time.time() - t1:.1f}s")

    inst = out["instants"]
    p = prefix(LENS_OF_RECORD)
    log(f"  instants {len(inst):,} over {out['meta']['n_units']:,} units "
        f"({out['meta']['n_campaigns']} campaigns)")
    log(f"  stamp lenses {out['meta']['stamp_lenses']}  ·  lag 0 on "
        f"{int((inst[p + 'bar_lag'] == 0).sum()):,}/{len(inst):,} rows "
        f"(a 4h instant reads its OWN 4h bar)")
    nr = int(inst[p + "in_range"].fillna(False).astype(bool).sum())
    log(f"  in a live macro range at the instant: {nr:,}/{len(inst):,} "
        f"({100.0 * nr / len(inst):.1f}%)")
    log("")
    log("  MACRO STATE AT EVERY INSTANT (four-valued, [LEAN S-a]):")
    vc = inst[p + "macro_state"].value_counts()
    for k in MACRO_STATES:
        log(f"    {k:<10} {int(vc.get(k, 0)):>7,}")
    odd = int((inst[p + "in_range"].fillna(False).astype(bool)
               & (inst[p + "state_latch"] != "NEUTRAL")).sum())
    log(f"    rows in a live range whose RAW latch is not NEUTRAL: {odd} "
        f"(disclosure — the collapse is auditable, not assumed)")

    tally = funnel_tally(out)
    log("")
    log("  THE FUNNEL, AS A PARTITION (every arming has exactly one end):")
    log(f"    {tally.to_string(index=False)}")
    if not bool(tally["partition_holds"].all()):
        raise SystemExit("HALT: the funnel is not a partition — an arming ended "
                         "twice or not at all")

    xt = entry_state_crosstab(out)
    log("")
    log("  TIER-E · CONTROL OUTCOMES BY MACRO STATE AT ENTRY (report-only, "
        "gates nothing):")
    show = ["macro_state_at_entry", "n", "n_assets", "net_r_sum",
            "expectancy_r", "win_rate_pct", "median_mfe_r",
            "median_pct_of_range", "provisional"]
    log(f"    {xt[show].to_string(index=False)}")

    units = unit_frame(out)
    put, W, K, SK = TP.make_put(root, meta, LENS_OF_RECORD)
    log("")
    put(inst, "control_v6_stamped", ["unit_id", "instant_kind", "instant_ms"])
    put(units, "control_v6_units", ["unit_id", "turn_kind", "turn_ms"])
    put(out["coverage"], "stamp_coverage", ["instant_kind"])
    put(out["nulls"], "stamp_nulls", ["lens", "field"])
    put(out["defs"], "stamp_defs", ["field"])
    put(tally, "funnel_tally", ["asset"])
    put(xt, "control_entry_by_state", ["macro_state_at_entry"])
    put(out["leans"], "leans", ["n"])

    man = {
        "tier": "TIER-C10", "stage": "A", "seed": SEED,
        "seed_lineage": SEED_LINEAGE, "scale_mult": float(FROZEN_SCALE),
        "lens_of_record": LENS_OF_RECORD,
        "stamp_lenses": out["meta"]["stamp_lenses"],
        "panel": out["meta"]["panel"], "panel_name": out["meta"]["panel_name"],
        "book": "card v6 · V6_ROLES · CLASSIC5 — the KNOWN CONTROL, ridden "
                "unregistered by tierc10_panel.run_cell_n's own gate",
        "window": {"lo_ms": int(lo), "hi_ms": int(hi), "lo": iso(lo),
                   "hi_close": iso(hi + 1)},
        "counts": {"campaigns": out["meta"]["n_campaigns"],
                   "units": out["meta"]["n_units"],
                   "instants": out["meta"]["n_instants"],
                   "armings": int(sum(len(a) for a in ctrl["arms"].values()))},
        "instant_kinds": list(INSTANT_KINDS),
        "stamp_fields": list(STAMP_FIELDS),
        "the_six": [f if isinstance(f, str) else list(f) for f in THE_SIX],
        "geometry_fields": list(GEOMETRY_FIELDS),
        "leash_fields": list(LEASH_FIELDS),
        "reject_bar_law": REJECT_BAR_LAW,
        "leans": list(LEANS), "lean_tag": LEAN_TAG,
        "tier_collar": TIER, "gates": GATES, "warranty": WARRANTY,
        "as_of_last_closed_4h": meta["last_closed_4h_close"],
        "substrate": sub["substrate"],
        "code_sha": code_sha(), "census_code_sha": C.code_sha(),
        "panel_code_sha": file_sha256(ROOT / "scripts" / "tierc10_panel.py"),
        "input_sha": TP.input_sha(TP.CLASSIC5),
        "sha": W, "keys": K, "skipped_empty": SK,
        "captured_not_consulted": (
            "the v6 decision closure reaches no module named in `forbidden`; "
            "the stamps are a left-join on [asset, instant_ms, instant_kind] "
            "and the journal is byte-identical to the unstamped book "
            "(F-STAMP-CLOSURE, F-STAMP-JOIN)"),
        "forbidden_in_decision_closure": ["tierc10_stamps", "tierc10_census",
                                          "analytics.rangefinder_census",
                                          "*rangefinder*"],
    }
    (root / "build_manifest.json").write_text(
        json.dumps(man, indent=2, sort_keys=True, default=str) + "\n")
    log("")
    log(f"  wrote {len(W)} tables + build_manifest.json -> {root}")
    clock(f"  total {time.time() - t0:.1f}s")
    return man


def _wrap(text: str, width: int) -> list[str]:
    words, line, out = text.split(), "", []
    for w in words:
        if len(line) + len(w) + 1 > width:
            out.append(line)
            line = w
        else:
            line = f"{line} {w}".strip()
    if line:
        out.append(line)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="TIER-C10 Stage A — tape + stamps")
    ap.add_argument("--rerun", action="store_true",
                    help="write the F-DET twin under research_outputs/"
                         "tierc10_run2/stamps")
    ap.add_argument("--out", default=None, help="output root (default "
                                                "research_outputs/tierc10/stamps)")
    a = ap.parse_args()
    root = Path(a.out) if a.out else (OUT_RERUN if a.rerun else OUT)
    root.mkdir(parents=True, exist_ok=True)
    run(root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
