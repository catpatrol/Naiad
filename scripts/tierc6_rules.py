"""TIER-C6 rev B · ARMED TRAIL + WALLS — THE DECISION PATH, AND NOTHING ELSE.

RATIFIED operator 2026-08-16.  THE RULINGS THIS CARD ENACTS, EACH CITED:

    H5        the trail ARMS AFTER +1R
    F-C4-b    the trail offset is RATIFIED at 0.5 ATR
    F-C4-d    a MINIMUM ADVANCE is adopted — 0.05 ATR
    F-C4-c    the bell is KEPT AS A BACKSTOP (a disposition; no code moves)
    F-C5-e    same ruling, from the other side of the same question
    F-C5-d    D12 the funding ceiling is KEPT as insurance
    F-C5-a    the YARDSTICK is the current card's FULL-CORRIDOR expectancy

Drafted APOLLO · Executor HEPHAESTUS · Seed 20260816.

CLASS: measurement + registrations + pre-named labs.  D15 columns everywhere and
gates nowhere.  Every grid reported WHOLE.  Every fixture leg states what would
make it FAIL.

────────────────────────────────────────────────────────────────────────────
BYTE-INHERITANCE IS BY IMPORT, FOUR GENERATIONS DEEP — AND THE CARD SUBCLASSES
────────────────────────────────────────────────────────────────────────────
`import tierc5_rules as V5` — which binds Tier-C4's, which binds Tier-C3's,
which binds Tier-C2's.  Every gate, every frame builder, every pivot, the
spring lane, the adds and the harvest are the SAME OBJECTS, not copies, and
F-C6-INHERIT asserts it with `is`.

`Card` here SUBCLASSES `V5.Card` rather than restating its fields.  That is a
stronger inheritance claim than the previous tiers could make: a v6 card IS a v5
card (`isinstance` holds), every v5 default arrives unretyped, and the diff a
reader has to audit is exactly the four fields declared below.  If someone adds
a knob to v5 it appears here automatically instead of silently diverging — which
is the failure mode a copied dataclass has and this one cannot.

────────────────────────────────────────────────────────────────────────────
THE CARD v6 = THE CARD v5, PLUS AN ARMED TRAIL AND A MINIMUM ADVANCE
────────────────────────────────────────────────────────────────────────────
THE ARMED TRAIL [H5].  v5's trail begins advancing the moment a favourable
fractal confirms, which can be while the campaign is still under water.  v6 does
not advance until the campaign's favourable excursion has reached +1R AT LEAST
ONCE.  It is a HIGH-WATER LATCH, not a state test: once +1R has been touched the
trail stays armed even if price falls back, because the question the ruling asks
is "has this campaign proved itself", and a campaign does not un-prove itself.

The knob `trail_arm_after_r` ALREADY EXISTS on v5's card as a shadow dimension
(S-TRAIL {+1R}) and `_ride` already honours it.  So H5 is enacted by RAISING A
SHADOW TO THE CARD, not by writing new machinery — the shadow lane is what a
shadow lane is for, and the code path that scores it is the code path that
scored it as a shadow.  What is new in v6 is that the DEFAULT moves.

THE MINIMUM ADVANCE [F-C4-d].  A candidate advance smaller than 0.05 ATR is not
taken.  The lean of record was "adopt a minimum advance but pin it from outside
this book"; 0.05 ATR is a twentieth of the rail and a tenth of the offset, and it
is pinned HERE, before the look, as a register row rather than a literal.

A REFUSED ADVANCE DOES NOT PERSIST, AND THAT IS A CHOICE.  `trail_step` is asked
once per bar for the fractal confirming on that bar.  A refused candidate is
simply not taken; the pivot is not remembered and no later bar reconsiders it.
The alternative — hold the refused pivot and advance when the gap has grown —
is a DIFFERENT rule (it would let a stop advance on a bar where nothing
confirmed) and it is not taken.  Stated because the two readings differ and only
one of them is in the code.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import tierc5_rules as V5                                            # noqa: E402
from engine import indicators as ind                                 # noqa: E402

# ═══════════════════════════════════════════════ BOUND, NOT COPIED — four deep
UNIVERSE = V5.UNIVERSE
TIDE_FAST, TIDE_SLOW = V5.TIDE_FAST, V5.TIDE_SLOW
STOP_BUF_ATR = V5.STOP_BUF_ATR
MIN_STOP_ATR = V5.MIN_STOP_ATR
RATCHET_PIVOT_L, RATCHET_PIVOT_R = V5.RATCHET_PIVOT_L, V5.RATCHET_PIVOT_R
RATCHET_BUF_ATR, RATCHET_RAIL_ATR = V5.RATCHET_BUF_ATR, V5.RATCHET_RAIL_ATR
RATCHET_MONOTONE = V5.RATCHET_MONOTONE
HARVEST_FRACTION = V5.HARVEST_FRACTION
ATR_LEN = V5.ATR_LEN
FEE_BPS_SIDE = V5.FEE_BPS_SIDE
FUNDING_CEILING_R = V5.FUNDING_CEILING_R
WARMUP_BARS = V5.WARMUP_BARS
PROVISIONAL_MIN_N = V5.PROVISIONAL_MIN_N
SPRING_LOOKBACK_BARS = V5.SPRING_LOOKBACK_BARS
SPRING_RECLAIM_BARS = V5.SPRING_RECLAIM_BARS
ADDS_MAX = V5.ADDS_MAX
LOCKBOX_WAS = V5.LOCKBOX_WAS

# the frame, the gates, the lanes — the same objects, asserted by F-C6-INHERIT
build_4h = V5.build_4h
Frame4h, Arming = V5.Frame4h, V5.Arming
armings = V5.armings
struct_stop_4h = V5.struct_stop_4h
build_pivots_4h = V5.build_pivots_4h
build_fractals = V5.build_fractals
Fractals4h, Advance = V5.Fractals4h, V5.Advance
harvest_edge, harvest_touched = V5.harvest_edge, V5.harvest_touched
harvest_outside, harvest_fill_px = V5.harvest_outside, V5.harvest_fill_px
Spring, spring_signals, spring_stop = V5.Spring, V5.spring_signals, V5.spring_stop
Add, add_context = V5.Add, V5.add_context
add_retraced, add_reclaimed = V5.add_retraced, V5.add_reclaimed
sealed_mask = V5.sealed_mask
Trade = V5.Trade

MS_4H = 4 * 3600 * 1000
MS_12H = 12 * 3600 * 1000

# ═══════════════════════════════════════════════════════════ THE REGISTER, v6
# Every number the card decides on, PINNED BEFORE THE LOOK, with the ruling that
# put it there.  Rows that merely re-point an inherited object carry the object,
# not a fresh literal — a constant no code consults is a constant that can drift
# silently (the F-C3-e defect in miniature).
REGISTER: dict[str, dict] = {
    "TRAIL_ARM_AFTER_R": {
        "value": 1.0,
        "ruling": "H5",
        "text": "the trail does not advance until the campaign's favourable "
                "excursion has reached +1R at least once — a high-water latch",
        "was": "v5: 0.0 (the trail advances from the first confirming fractal)",
    },
    "TRAIL_MIN_ADVANCE_ATR": {
        "value": 0.05,
        "ruling": "F-C4-d",
        "text": "a candidate advance smaller than this, measured as "
                "abs(new_stop - prev_stop) / ATR, is NOT taken",
        "was": "v5: no minimum — every improving candidate was taken",
    },
    "TRAIL_OFFSET_ATR": {
        "value": STOP_BUF_ATR,           # the OBJECT, not the literal 0.5
        "ruling": "F-C4-b (ratified)",
        "text": "the trail sets its stop this far beyond the confirming pivot",
        "was": "v5: the same value, held open pending this ruling",
    },
    "TRAIL_RAIL_ATR": {
        "value": MIN_STOP_ATR,           # the OBJECT, not the literal 1.0
        "ruling": "F-C4-b / card",
        "text": "and never closer than this to the confirming close",
        "was": "unchanged since v4",
    },
    "WALL_EXIT_ATR": {
        "value": 0.25,
        "ruling": "P-WALL-1 (registered, not carded)",
        "text": "the remainder exits on a CLOSE within this many ATR of the "
                "profit-side 12h champion wall",
        "was": "not present in any prior tier",
    },
    "BELL_DISPOSITION": {
        "value": "backstop",
        "ruling": "F-C4-c / F-C5-e",
        "text": "KEPT. It fired once in seven years (194 of 195 exits are "
                "stops). It fires rarely because the trail is faster, not "
                "because the bell is wrong, and a regime in which no favourable "
                "fractal ever confirms would leave a campaign with no exit but "
                "its entry stop. Recorded as a backstop EXPECTED NEVER TO FIRE "
                "so nobody later mistakes its silence for evidence it works.",
        "was": "v5: same code, no ruling",
    },
    "FUNDING_CEILING_R": {
        "value": FUNDING_CEILING_R,
        "ruling": "F-C5-d",
        "text": "KEPT as insurance. It bound 0 of 195 campaigns at unit size, "
                "2 at 2x and 4 at 3x — a rule that costs nothing and buys "
                "nothing at the size the card is scored at, which is precisely "
                "the profile of insurance.",
        "was": "v5: present, unruled",
    },
    "YARDSTICK": {
        "value": "full_corridor_expectancy_of_the_current_card",
        "ruling": "F-C5-a",
        "text": "the yardstick a multiplier must beat is the CURRENT CARD's "
                "FULL-CORRIDOR expectancy. Every slice number carries its "
                "window label so no reader can mistake a quarter for the book.",
        "was": "three candidates 7x apart: +0.6907 (118 sealed days), +0.1724 "
               "(2,534 open ones), +1.1964 (the operator's 29)",
    },
}

TRAIL_ARM_AFTER_R: float = REGISTER["TRAIL_ARM_AFTER_R"]["value"]
TRAIL_MIN_ADVANCE_ATR: float = REGISTER["TRAIL_MIN_ADVANCE_ATR"]["value"]
WALL_EXIT_ATR: float = REGISTER["WALL_EXIT_ATR"]["value"]


# ═════════════════════════════════════════════════════════════ THE CARD, v6
@dataclass(frozen=True)
class Card(V5.Card):
    """v5's card, four fields wider.

    SUBCLASSING IS THE INHERITANCE CLAIM.  `isinstance(v6_card, V5.Card)` holds,
    so every v5 function that types its argument as a v5 card accepts this one
    unchanged, and every v5 default arrives without being retyped here.  The
    audit surface is the four fields below and nothing else.

    THE THREE NEW KNOBS ARE ALL SHADOW DIMENSIONS TOO.  `trail_min_advance_atr`
    is S-MINADV {0, 0.05, 0.10}, `harvest_frac` is S-HFRAC {33, 50, 67} and
    `wall_exit_atr` carries P-WALL-1.  The card is one cell of each grid, and it
    is scored by the same function that scores the rest — which is what makes
    the grid a comparison rather than a display.
    """
    name: str = "v6"
    trail_arm_after_r: float = TRAIL_ARM_AFTER_R      # H5 — THE CARD DIFF
    trail_min_advance_atr: float = TRAIL_MIN_ADVANCE_ATR   # F-C4-d — THE OTHER
    harvest_frac: float = HARVEST_FRACTION            # S-HFRAC {0.33, 0.67}
    wall_exit_atr: float | None = None                # P-WALL-1 sets 0.25
    wall_tf: str = "12h"                              # the clock the league won on


CARD_V6 = Card()

# THE PAIRED CONTROL — v5, EXPRESSED IN THE v6 TYPE.
# Not `V5.Card(...)`.  The control must ride the CHILD's code path, and a parent
# card handed to the child's `_ride` would fail on the first v6 knob it read —
# which is a type error masquerading as a control.  Every v6 knob is set to the
# value that makes the v6 code path do what v5 did: the trail unarmed (advance
# from the first confirming fractal), no minimum advance, no wall, the ruled
# harvest fraction.  F-C6-CTRL's whole claim is that THIS card, through THIS
# module, reproduces Tier-C5's filed book trade for trade — which is the same
# sentence as "v6 with its knobs off IS v5", made checkable.
CARD_V5_CONTROL = Card(
    name="v5-control",
    trail_arm_after_r=0.0,            # v5: the trail advances from bar one
    trail_min_advance_atr=0.0,        # v5: every improving candidate is taken
    wall_exit_atr=None,               # v5: no wall exit exists
    harvest_frac=HARVEST_FRACTION,    # v5: the module constant, now on the card
)


# ══════════════════════════════════ THE TRAIL — v5's, with one gate on top
def trail_step(fr: Fractals4h, j: int, direction: int, cur_stop: float,
               close: float, atr: float, open_ms: np.ndarray,
               buf_atr: float, rail_atr: float,
               forbidden: np.ndarray | None = None,
               min_advance_atr: float = 0.0) -> Advance | None:
    """v5's `trail_step`, then F-C4-d's minimum advance.

    THE GATE IS APPLIED ON TOP OF THE PARENT'S DECISION, NOT WOVEN INTO IT.
    `V5.trail_step` is CALLED — not reimplemented — so the pivot lookup, the
    seal mask threading, the rail, the sign handling and the monotone test are
    the parent's objects running the parent's code.  What v6 adds is one
    predicate on the returned Advance, and the quantity it tests is EXACTLY the
    one the tape publishes as `advance_atr`:

        abs(new_stop - prev_stop) / atr

    That identity is deliberate.  A gate measured on one quantity and reported
    on another is a gate no reader can check, and this estate has already lost a
    fixture to a name that was almost right.

    WHAT WOULD MAKE THIS WRONG: testing the gate against the PIVOT distance
    rather than the STOP movement (a large pivot gap can still move the railed
    stop by nothing), applying it when `min_advance_atr` is 0 (v5 must be
    reproduced EXACTLY by F-C6-CTRL, and `>` on a zero threshold would refuse a
    zero-length advance the parent took), or remembering the refused pivot.
    """
    adv = V5.trail_step(fr, j, direction, cur_stop, close, atr, open_ms,
                        buf_atr=buf_atr, rail_atr=rail_atr, forbidden=forbidden)
    if adv is None or min_advance_atr <= 0.0:
        return adv                    # v5 EXACTLY when the knob is off
    if not (np.isfinite(atr) and atr > 0):
        return None
    moved = abs(float(adv.new_stop) - float(adv.prev_stop)) / float(atr)
    return adv if moved >= float(min_advance_atr) else None


# ═══════════════════════════════════════ THE WALL — P-WALL-1's decision input
def wall_series_12h(open_ms: np.ndarray, high: np.ndarray, low: np.ndarray,
                    close: np.ndarray, length: int) -> np.ndarray:
    """The 12h champion EMA, read on every 4h bar, AS OF THE LAST CLOSED 12h BAR.

    CAPTURED-NOT-CONSULTED IS WHY THIS IS HERE AND NOT IN THE PROGRAM.
    The resistance league is a Tier-E MEASUREMENT and may use `analytics`
    freely — `_tf_frame` resamples through `analytics.structure`.  P-WALL-1 is
    a DECISION, and a decision may not consult the analytics estate.  So the 12h
    series a decision reads is built HERE, in the decision path, out of raw 4h
    bars and `engine.indicators` alone.  The league still names the LENGTH; it
    does not supply the series.

    THE BUCKETING IS ARITHMETIC, NOT A LIBRARY CALL.  4h bars open at
    00/04/08/12/16/20 UTC, so a 12h bucket is exactly three of them and
    `open_ms // MS_12H` labels it.  The FORMING bucket is dropped (the estate's
    AMENDMENT FAN8 convention): a 12h bar counts only once all three of its 4h
    bars have closed.

    THE AS-OF IS THE 4h BAR'S CLOSE, NOT ITS OPEN.  Bar j's decision is taken at
    `open_ms[j] + 4h`; the wall it may consult is the newest 12h bar that had
    already closed by then.  Reading the bucket bar j is IN would quote a level
    built partly from bar j itself.

    AND THE EMA IS NULL UNTIL WARM.  `engine.indicators.ema` seeds at the series
    start and NEVER returns NaN, so without an explicit floor an EMA of length
    889 publishes the first 12h close in the panel as a "wall".  That defect has
    now been repaired twice in this estate — once in the TC5 decision path, once
    on the TC5-Q champion columns — and it is not going to be introduced a third
    time.  Bars before the floor return NaN, and every caller must test.

    WHAT WOULD MAKE THIS WRONG: including the forming bucket, reading as-of the
    bar's open, or emitting a seeded value as a level.  F-C6-WALL re-derives
    three exits per side from raw bars against this function.
    """
    om = np.asarray(open_ms, dtype=np.int64)
    buck = om // MS_12H
    # the last 4h bar of each bucket — the bucket is CLOSED after it
    last_of = {}
    for i, b in enumerate(buck):
        last_of[int(b)] = i
    order = sorted(last_of)
    # a bucket is complete only if its final 4h bar is the third one
    closed = [b for b in order
              if (om[last_of[b]] - b * MS_12H) == 2 * MS_4H]
    if not closed:
        return np.full(len(om), np.nan)
    idx = np.array([last_of[b] for b in closed], dtype=np.int64)
    c12 = np.asarray(close, dtype=float)[idx]
    h12 = np.array([float(np.max(high[max(0, i - 2):i + 1])) for i in idx])
    l12 = np.array([float(np.min(low[max(0, i - 2):i + 1])) for i in idx])
    e12 = ind.ema(c12, int(length))
    a12 = ind.atr(h12, l12, c12, 14)
    warm = np.arange(len(c12)) >= int(length)          # THE FLOOR
    e12 = np.where(warm, e12, np.nan)
    a12 = np.where(warm, a12, np.nan)
    # map back to 4h bars: bar j sees the newest bucket CLOSED at or before
    # open_ms[j] + 4h, i.e. whose own last 4h bar closed no later than that.
    close_ms = om[idx] + MS_4H
    k = np.searchsorted(close_ms, om + MS_4H, side="right") - 1
    out_e = np.full(len(om), np.nan)
    out_a = np.full(len(om), np.nan)
    ok = k >= 0
    out_e[ok] = e12[k[ok]]
    out_a[ok] = a12[k[ok]]
    return np.vstack([out_e, out_a])


def wall_touch(close_px: float, wall_px: float, atr: float,
               tol_atr: float) -> bool:
    """Is this CLOSE within `tol_atr` ATR of the wall, ON THE PROFIT SIDE?

    THE PROFIT SIDE IS THE SIDE THE CAMPAIGN IS TRYING TO REACH.  A long makes
    money upward, so the wall in its way is RESISTANCE — above.  A short makes
    money downward, so its wall is SUPPORT — below.  That is why the league had
    to grow a second side before this registration could be written: scoring a
    short against a resistance champion would measure the wall behind it.

    APPROACHED, NOT CROSSED.  The test is on DISTANCE, and it fires whether the
    close is just short of the wall or just past it — a close that has punched
    through by 0.1 ATR is still "within 0.25 ATR of" it.  The alternative
    reading (only from the near side) is a different rule and is not taken;
    stated because the two differ on exactly the bars that matter most.

    AND `direction` IS GONE — ADVERSARIAL REPAIR C6-5.  It was a parameter of
    this function, threaded from every call site, and NEVER READ.  A docstring
    two paragraphs long about which side the wall is on, over a signature that
    accepts the side and ignores it, is a name that is almost right: a reader
    checking whether the profit side is enforced HERE would conclude it is.
    It is not, and it is not meant to be — the side is carried entirely by
    WHICH champion length the caller passes (`profit_side` picks it), and the
    geometry test is deliberately symmetric.  The parameter is removed so the
    signature stops implying a test the body does not perform.

    WHAT WOULD MAKE THIS WRONG: firing on a wall the campaign has already left
    far behind (the distance test prevents it), or firing on a NaN wall — an
    unwarm EMA must never be a level, so a non-finite wall answers False.
    """
    if not (np.isfinite(wall_px) and np.isfinite(atr) and atr > 0):
        return False
    if not np.isfinite(close_px):
        return False
    return abs(float(close_px) - float(wall_px)) <= float(tol_atr) * float(atr)


def wall_alignment(entry_px: float, stop_px: float, r_dist: float,
                   wall_px: float, direction: int) -> str:
    """L-WALLQ's four buckets, read AT THE ARMING, from quantities known then.

    beyond_stop   the wall sits behind the position, past its stop — the
                  campaign is trading AWAY from it and it can only help
    blocks_2r     the wall sits between entry and the first +2R — the campaign
                  must get THROUGH it to pay
    both          a wall on each side (this is possible only when two walls are
                  read; with ONE champion per side it is the degenerate case and
                  is reported so the bucket is never silently empty)
    neither       no wall within the campaign's working range

    WHAT WOULD MAKE THIS WRONG: computing it from the EXIT (it would be an
    outcome, not a context), or reading a wall the arming bar had not yet seen.
    """
    if not np.isfinite(wall_px):
        return "no_wall"
    d = direction
    tgt2 = entry_px + d * 2.0 * r_dist
    beyond = (wall_px - stop_px) * d <= 0.0
    blocks = ((wall_px - entry_px) * d > 0.0) and ((wall_px - tgt2) * d <= 0.0)
    if beyond and blocks:
        return "both"
    if beyond:
        return "beyond_stop"
    if blocks:
        return "blocks_2r"
    return "neither"


def register_rows() -> list[dict]:
    """The register, as a table — so the build document quotes the code rather
    than a transcription of it."""
    return [{"key": k, "value": str(v["value"]), "ruling": v["ruling"],
             "text": v["text"], "was": v["was"]}
            for k, v in sorted(REGISTER.items())]
