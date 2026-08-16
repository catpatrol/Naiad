"""TIER-C4 · THE MEAN CARD — THE DECISION PATH, AND NOTHING ELSE.

RATIFIED operator 2026-08-16 ("run tc4 with just the anchor 4H trade; ratchet
and harvest per your lean; a mean for the average trade we can tune later").
Drafted APOLLO · Executor HEPHAESTUS · Seed 20260816.

CLASS: MEASUREMENT, NOT REGISTRATION.  m = 0.  ONE pre-named card — no grid, no
sweep; the selection guard is LOADED and IDLES because there is nothing to
select.  No lockbox read for outcomes.  No estate write.  No live orders.

────────────────────────────────────────────────────────────────────────────
BYTE-INHERITANCE IS BY IMPORT, NOT BY COPY — TWO GENERATIONS DEEP
────────────────────────────────────────────────────────────────────────────
`import tierc3_rules as V3` — which itself binds Tier-C2's objects.  So
`build_4h`, `_crosses`, `armings`, `Frame4h`, `Arming`, `Pivots4h`, `Stop`,
`build_pivots_4h` and `struct_stop_4h` below are not copies that resemble the
v3 card: they ARE the v3 card's objects, and through them Tier-C2's.
`tierc4_fixtures.F-C4-INHERIT` asserts the identities with `is`.

TWO THINGS ARE NEW, AND ONLY TWO.  Both are AMENDMENTS to the ride — neither
touches the tide, the window, the trigger, the entry, the entry anchor, the
entry rail, the bell or the toll:

    RATCHET ["ratchet"]  THE LPS-TRAIL.  When a new FAVOURABLE 4h swing pivot
        CONFIRMS during the ride — fractal (2,2), the pivot bar's low/high
        strictly flanked by 2 bars each side, close-confirmed at pivot bar + 2
        — the stop ADVANCES to beyond that pivot, railed so it is never nearer
        than 1.0 x ATR from the current close.  Stops only advance, never
        retreat.  The bell still exits everything.

    HARVEST ["harvest"]  THE CREEK/ICE TOUCH.  At the FIRST touch of the
        opposing 89/316 band after entry — shorts: price back up into the band
        from below; longs: the mirror — exit 50% of the unit at that bar's
        CLOSE.  The remainder rides to ratchet or bell.  ONE harvest per
        campaign, ever.

THREE NUMBERS ARE GENUINELY NEW: the fractal's 2 and 2, and the harvest's 0.5.
EVERY OTHER CONSTANT THE AMENDMENTS USE IS RE-POINTED INHERITANCE, and each row
of REGISTER_DIFF says which v3 constant it is and where it was re-pointed to.
A new number that is really an old number wearing a new name is how a register
stops being a register.

────────────────────────────────────────────────────────────────────────────
THE SEAL, UNCHANGED AND EXTENDED
────────────────────────────────────────────────────────────────────────────
The entry anchor keeps the v3 seal floor exactly (F-C3-a semantics inherited):
sealed bars are masked out of anchor eligibility, and a tranche with no
admissible anchor is NOT TAKEN.  The RATCHET introduces a SECOND price quoted
from a named bar — the trailing pivot — so it takes the SAME mask.  On this
corridor the mask cannot bind on a ratchet pivot (every ratchet pivot confirms
strictly after an entry that is itself at or after 2025-10-06, the day after
the seal closes), and that is PROVED rather than assumed: F-C4-SEAL resolves
every advance's pivot back to its own bar.  An amendment that quotes a price
and is not masked is exactly the hole F-C3-a found the hard way.

F-C4-6 · CAPTURED-NOT-CONSULTED still holds by construction: this module's
transitive import closure is {numpy, dataclasses, engine.*, tierc2_rules,
tierc3_rules} and contains no `analytics` member.
────────────────────────────────────────────────────────────────────────────
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from engine.s1 import _pivots

# The Tier-C3 decision path.  Analytics-free itself, so importing it cannot
# introduce a registry symbol — F-C4-6 proves that by closure, not by promise.
import tierc3_rules as V3

# ═══════════════════════════════ BYTE-INHERITED — the SAME objects, bound
# Two generations: these are Tier-C3's names, and Tier-C3 bound most of them
# straight from Tier-C2.  Nothing below is transcribed.
Frame4h = V3.Frame4h
Arming = V3.Arming
Pivots4h = V3.Pivots4h
Stop = V3.Stop
build_4h = V3.build_4h
_crosses = V3._crosses
armings = V3.armings
build_pivots_4h = V3.build_pivots_4h
struct_stop_4h = V3.struct_stop_4h

UNIVERSE = V3.UNIVERSE
LENS = V3.LENS
TIDE_FAST, TIDE_SLOW = V3.TIDE_FAST, V3.TIDE_SLOW
WINDOW_FAST, WINDOW_SLOW = V3.WINDOW_FAST, V3.WINDOW_SLOW
TRIGGER_FAST, TRIGGER_SLOW = V3.TRIGGER_FAST, V3.TRIGGER_SLOW
D_DISPLACEMENT, D_STRIP = V3.D_DISPLACEMENT, V3.D_STRIP
ATR_LEN = V3.ATR_LEN
FEE_BPS_SIDE = V3.FEE_BPS_SIDE
FEE_BPS_ROUND_TRIP = V3.FEE_BPS_ROUND_TRIP
PIVOT_L, PIVOT_R = V3.PIVOT_L, V3.PIVOT_R
STOP_BUF_ATR = V3.STOP_BUF_ATR
MS_4H, MS_1H = V3.MS_4H, V3.MS_1H
FUNNEL_STAGES = V3.FUNNEL_STAGES

PIVOT_LOOKBACK_4H = V3.PIVOT_LOOKBACK_4H
PIVOT_LOOKBACK_4H_TIME_EQUIV = V3.PIVOT_LOOKBACK_4H_TIME_EQUIV
MIN_STOP_ATR = V3.MIN_STOP_ATR
LEAD_IN_DAYS = V3.LEAD_IN_DAYS
SEAL_FLOOR_ON_ANCHOR = V3.SEAL_FLOOR_ON_ANCHOR

INHERITED = ("Frame4h", "Arming", "Pivots4h", "Stop", "build_4h", "_crosses",
             "armings", "build_pivots_4h", "struct_stop_4h")

# ════════════════════════════════════════════════ THE CARD DIFFS · registered
# F-C3-3 posture, inherited: no value is invented.  Every row names where the
# number came from, and the rows that are RE-POINTED INHERITANCE say so in
# those words — the amendment reuses a v3 constant at a new site rather than
# introducing a second constant for the same concept (the F-C3-e defect, which
# left the estate holding two rails for one idea).
REGISTER_DIFF: dict[str, dict] = {
    "RATCHET_PIVOT_L": {
        "value": 2,
        "source": "TC-4 card ['pivot'] (operator 2026-08-16): 'fractal 2-2: "
                  "pivot bar's low/high flanked by 2 bars each side, "
                  "close-confirmed'. GENUINELY NEW. Computed by "
                  "engine.s1._pivots — the estate's pivot of record and the "
                  "SAME function the (5,5) entry anchor uses; the card moved "
                  "the SHAPE, not the definition.",
    },
    "RATCHET_PIVOT_R": {
        "value": 2,
        "source": "TC-4 card ['pivot'], as above. GENUINELY NEW. The "
                  "confirmation lag is R bars: a fractal at bar p is knowable "
                  "at the CLOSE of bar p+2, and the advanced stop therefore "
                  "governs bar p+3 onward. Causality is the reason the lag is "
                  "in the register at all.",
    },
    "RATCHET_BUF_ATR": {
        # NOT the literal 0.5 — the v3 constant itself, so the register row
        # cannot drift from the thing it claims to inherit.
        "value": STOP_BUF_ATR,
        "source": "RE-POINTED INHERITANCE of STOP_BUF_ATR (= 0.5, Tier-C2 "
                  "register). The card says 'advance the stop to BEYOND that "
                  "pivot'; 'beyond' is the v3 card's own word for its entry "
                  "anchor ('offset 0.5 x ATR_4h beyond it'), so the trail "
                  "reuses the card's own definition of beyond rather than "
                  "inventing a second one. The alternative reading — offset "
                  "0.0, the stop exactly AT the pivot — is NOT taken and is "
                  "disclosed with COUNTS and no R (finding F-C4-b).",
    },
    "RATCHET_RAIL_ATR": {
        "value": MIN_STOP_ATR,
        "source": "RE-POINTED INHERITANCE of MIN_STOP_ATR (= 1.0, F-3 ruling "
                  "2026-08-15). The card says 'railed at 1.0 ATR from current "
                  "close'. Same rail, same value, new measuring point: v3 "
                  "rails the ENTRY stop against the ENTRY close, the ratchet "
                  "rails an ADVANCED stop against the CONFIRMING BAR's close. "
                  "One constant, two sites — named so it can never become the "
                  "two-rails-for-one-concept defect of F-C3-e.",
    },
    "RATCHET_MONOTONE": {
        "value": True,
        "source": "TC-4 card ['ratchet']: 'stops only advance, never retreat'. "
                  "Enforced arithmetically in `ratchet_step` by max()/min() "
                  "against the standing stop, not by a convention anyone has "
                  "to remember.",
    },
    "HARVEST_FRACTION": {
        "value": 0.5,
        "source": "TC-4 card ['harvest'] (operator 2026-08-16): 'exit 50% of "
                  "the unit at that bar's close'. GENUINELY NEW.",
    },
    "HARVEST_BAND": {
        "value": (TIDE_FAST, TIDE_SLOW),
        "source": "RE-POINTED INHERITANCE of (TIDE_FAST, TIDE_SLOW) = "
                  "(89, 316). The harvest band IS the tide band — the card "
                  "says '89/316' and the estate already has exactly one such "
                  "pair. No new EMA is computed anywhere in this build.",
    },
    "HARVEST_MAX_PER_CAMPAIGN": {
        "value": 1,
        "source": "TC-4 card ['harvest']: 'One harvest per campaign, ever.' "
                  "Enforced by state in the ride, and re-asserted against the "
                  "written ledger by F-C4-HARV.",
    },
    "HARVEST_FILL": {
        "value": "bar_close",
        "source": "TC-4 card ['harvest']: the TOUCH is intrabar (high/low "
                  "against the band edge) and the FILL is 'at that bar's "
                  "close'. The two are deliberately different instants and the "
                  "card names both; no intrabar path is modelled, exactly as "
                  "F-4 rules for the stop.",
    },
}

REGISTER: dict[str, dict] = {**V3.REGISTER, **REGISTER_DIFF}

# Inherited but retired one generation up; carried so a closed register cannot
# quietly resurrect a dead rule.
RETIRED_FROM_V1: tuple[str, ...] = V3.RETIRED_FROM_V1

RATCHET_PIVOT_L: int = REGISTER["RATCHET_PIVOT_L"]["value"]
RATCHET_PIVOT_R: int = REGISTER["RATCHET_PIVOT_R"]["value"]
RATCHET_BUF_ATR: float = REGISTER["RATCHET_BUF_ATR"]["value"]
RATCHET_RAIL_ATR: float = REGISTER["RATCHET_RAIL_ATR"]["value"]
RATCHET_MONOTONE: bool = REGISTER["RATCHET_MONOTONE"]["value"]
HARVEST_FRACTION: float = REGISTER["HARVEST_FRACTION"]["value"]
HARVEST_BAND: tuple[int, int] = REGISTER["HARVEST_BAND"]["value"]
HARVEST_MAX_PER_CAMPAIGN: int = REGISTER["HARVEST_MAX_PER_CAMPAIGN"]["value"]

# THE RE-POINTED ROWS, ASSERTED AT IMPORT.  Their register VALUES are the v3
# objects themselves (see the rows above), so these three assertions can only
# fail if a future edit replaces an inheritance with a typed literal — which is
# precisely the drift F-C3-e recorded when the estate ended up holding two
# rails for one concept.  The module refuses to load rather than ship it.
assert RATCHET_BUF_ATR == STOP_BUF_ATR, \
    "RATCHET_BUF_ATR must BE the v3 STOP_BUF_ATR, not a copy of its value"
assert RATCHET_RAIL_ATR == MIN_STOP_ATR, \
    "RATCHET_RAIL_ATR must BE the v3 MIN_STOP_ATR, not a second rail"
assert HARVEST_BAND == (TIDE_FAST, TIDE_SLOW), \
    "HARVEST_BAND must BE the tide band (89, 316), not a second band"

# AND THE ONE ROW THE CODE CAN READ BUT NOT YET ENACT AT ANY OTHER VALUE.
# The ride counts fills against HARVEST_MAX_PER_CAMPAIGN rather than against a
# literal, which is right — but the ACCOUNTING models exactly one reduction
# (one harvested half, one runner half).  Set the row to 2 and the ride would
# overwrite the first fill and book the second as though it were the first.
# A constant that is read but cannot be honoured is worse than one that is
# ignored, because it looks wired.  So it HALTs here instead.
assert HARVEST_MAX_PER_CAMPAIGN == 1, (
    f"HALT: HARVEST_MAX_PER_CAMPAIGN = {HARVEST_MAX_PER_CAMPAIGN}. The card "
    f"says 'ONE harvest per campaign, ever' and the ACCOUNTING models exactly "
    f"one reduction — a harvested half and a runner half. Any other value "
    f"needs an accounting that carries n legs, which is a new card.")

# ═══════════════════════════════════════════════════ THE RULE CARD v4, verbatim
RULE_CARD_V4 = """\
UNIVERSE ["universe"]: {BTC,ETH,SOL,NEAR,ZEC}USDT · LENS ["lens"]: 4h only
TIDE: long iff e89>e316 AND close>e316 on 4h (mirror short)
WINDOW: 4h 12/89 cross in direction, no counter yet; displacement |close-e89|/ATR
  at the cross >= d=0.75 ["d"]; sensitivity strip {0.50,1.00} printed UNSCORED
TRIGGER: first in-window 4h 12/26 cross -> enter at that bar close
STOP ["stop"] [F-3]: structural anchor BEYOND THE NEAREST REAL 4h SWING PIVOT
  (the system's own lens; 1H pivots are RETIRED from this card), offset 0.5 x
  ATR_4h beyond it; RAIL: stop distance = max(pivot distance, 1.0 x ATR_4h at
  entry); R = entry-stop distance; one unit; one position per asset
STOP EXECUTION [F-4]: THE STOP EXECUTES. A bar touching the stop exits AT the
  stop, ADVERSE-FIRST — if one bar touches both the stop and a bell, the stop
  is taken. No intrabar path is modelled.
RATCHET ["ratchet"] [TC-4]: THE LPS-TRAIL. When a new FAVOURABLE 4h swing pivot
  CONFIRMS — fractal (2,2) ["pivot"], the pivot bar's low/high STRICTLY beyond
  the 2 bars each side, close-confirmed at pivot bar + 2 — the stop ADVANCES to
  beyond that pivot (0.5 x ATR_4h, the card's own 'beyond'), RAILED so it is
  never nearer than 1.0 x ATR_4h from the CONFIRMING BAR's close. Stops only
  advance, never retreat. The advanced stop governs the NEXT bar onward. The
  bell still exits everything. R is NOT re-denominated: R stays the ENTRY stop
  distance for the life of the campaign.
HARVEST ["harvest"] [TC-4]: THE CREEK/ICE TOUCH. At the FIRST touch of the
  opposing 89/316 band after entry — shorts: the bar's HIGH reaches the band's
  near edge FROM BELOW; longs: the mirror — exit 50% of the unit AT THAT BAR'S
  CLOSE. Remainder rides to ratchet or bell. ONE harvest per campaign, ever.
  "FROM BELOW" IS A PRECONDITION, NOT DECORATION: the touch counts only once
  the campaign has CLOSED on its own side of the near edge (at the entry bar,
  or any bar since). A campaign that entered INSIDE the band is not armed until
  it leaves — a position that was never outside cannot cross in. Count of
  entries inside the band is disclosed, and is 0 on this corridor.
  WITHIN A BAR: stop, then bell, then harvest. A stop takes the whole remainder
  adverse-first [F-4]; a bell exits the whole remainder at the close, which
  makes a same-bar harvest economically identical and it is not recorded.
LEAD-IN [F-5]: armings are admitted from scored_start - 30d; a trade is SCORED
  iff its ENTRY bar lies inside the scored window
RIDE: no management other than the ratchet and the harvest named above
BELL: counter 4h 12/89 OR 4h 89/316 against -> exit at close
ACCOUNTING ["accounting"]: net of 10 bps round-trip + journaled funding; R units;
  R = ENTRY stop distance; the halves BOOK THEIR OWN R contributions — entry fee
  splits 50/50, each half pays its own exit fee, funding accrues on the size
  actually held into each bar; one unit, one position per asset
STRIPS [F-7]: every display-only continuity strip truncates at 2026-07-07T23:59Z
SEAL FLOOR [CLASS, not a card diff]: no pivot lying on a SEALED bar may be an
  anchor — AND NONE MAY BE A RATCHET PIVOT EITHER. An anchor is a PRICE that is
  published, denominates R and is paid out on a stop; a ratchet pivot is a PRICE
  that is published and paid out on a stop. Same class, same mask. A trade left
  with no admissible entry anchor is NOT TAKEN. Printed both ways."""


# ══════════════════════════════════════════ THE RATCHET — the card's diff (1)
@dataclass
class Fractals4h:
    """Confirmed 4h (2,2) fractals — the LPS-trail's pivots.

    Deliberately a DIFFERENT SHAPE from `Pivots4h`, and deliberately the SAME
    function: `engine.s1._pivots` is strict on both flanks and confirms at
    p + R, so a (2,2) call is the card's fractal exactly and a (5,5) call is
    the entry anchor exactly.  One definition of a pivot in the estate, two
    shapes named by the card.

    Stored as maps keyed by the CONFIRMATION bar because that is how the ride
    consumes them — "did a favourable pivot confirm on this bar?" — and a map
    keyed by confirmation cannot be read acausally by accident.
    """
    low_by_conf: dict[int, tuple[float, int]]     # conf -> (low value, pivot bar)
    high_by_conf: dict[int, tuple[float, int]]    # conf -> (high value, pivot bar)
    n_low: int
    n_high: int


def build_fractals_4h(h4_high, h4_low) -> Fractals4h:
    """Confirmed strict 4h (2,2) fractals, keyed by the bar they CONFIRM on.

    `_pivots(x, L, R)` returns `(p + R, x[p])` and is strict on both flanks —
    `x[p] < min(x[p-L:p])` and `x[p] < min(x[p+1:p+1+R])` for a low, mirrored
    for a high.  So a pivot BAR p is knowable only at bar p + R, and the ride
    keys on p + R.  `conf` values are unique within a series (p is unique and
    the map p -> p + R is injective), so the dicts cannot collide.
    """
    lc, lv = _pivots(np.asarray(h4_low, float), RATCHET_PIVOT_L,
                     RATCHET_PIVOT_R, low=True)
    hc, hv = _pivots(np.asarray(h4_high, float), RATCHET_PIVOT_L,
                     RATCHET_PIVOT_R, low=False)
    return Fractals4h(
        low_by_conf={int(c): (float(v), int(c) - RATCHET_PIVOT_R)
                     for c, v in zip(lc, lv)},
        high_by_conf={int(c): (float(v), int(c) - RATCHET_PIVOT_R)
                      for c, v in zip(hc, hv)},
        n_low=int(len(lc)), n_high=int(len(hc)))


@dataclass
class Advance:
    """One stop advance, and the arithmetic that produced it — so a trailing
    stop can never be a number that appeared without provenance."""
    conf_i: int              # bar the fractal confirmed on (stop governs conf_i + 1)
    conf_ms: int
    pivot_val: float         # the raw 4h fractal low/high
    pivot_bar: int           # the bar whose low/high that is
    pivot_bar_ms: int
    atr: float               # ATR_4h at the confirming bar
    close: float             # close of the confirming bar — the rail's reference
    cand_px: float           # pivot -/+ 0.5 x ATR — the card's "beyond"
    rail_px: float           # close -/+ 1.0 x ATR — the rail's own limit
    new_stop: float          # the stop actually taken
    prev_stop: float
    rail_binding: bool       # True iff the rail, not the pivot, set the stop
    # |close - new_stop| / ATR at placement — the F-C4-RAIL leg.  Spelled
    # `..._over_atr` and NOT `dist_atr`: `dist_atr` is a TAPE column-family
    # name, and F-C4-6's captured-not-consulted proof is a substring scan of
    # the decision path for tape column names.  A field that merely SHARES a
    # name with a registry column would fail that scan — correctly, because the
    # scan cannot know which one you meant.  Caught by the fixture, not by eye.
    dist_from_close_over_atr: float


def ratchet_step(fr: Fractals4h, j: int, direction: int, cur_stop: float,
                 close: float, atr: float, open_ms: np.ndarray,
                 forbidden: np.ndarray | None = None,
                 buf_atr: float = RATCHET_BUF_ATR,
                 rail_atr: float = RATCHET_RAIL_ATR,
                 monotone: bool = RATCHET_MONOTONE) -> Advance | None:
    """THE LPS-TRAIL, one bar of it.  Returns the Advance, or None.

    Called with `j` = the bar just processed.  If a FAVOURABLE fractal confirms
    on bar j, the stop advances and the returned Advance governs bar j + 1
    onward — the caller applies it after finishing bar j, which is the whole of
    the causality argument: a stop derived from bar j's close cannot be tested
    against bar j's own low.

    FAVOURABLE means the pivot that SUPPORTS the position: a swing LOW for a
    long, a swing HIGH for a short.  The card's word is "favorable" and this is
    the only reading under which a trail trails.

    Three gates, in order:
      1. the fractal exists and confirms on this bar;
      2. its own bar is not SEALED (the CLASS line — a ratchet pivot is a
         published price paid out on a stop, the same class of object as the
         entry anchor, so it takes the same mask);
      3. the railed candidate strictly improves on the standing stop
         (RATCHET_MONOTONE) — otherwise nothing happens and None is returned.

    The rail is a FLOOR ON DISTANCE, not a cap: `min(cand, close - rail)` for a
    long takes whichever stop is FARTHER from price, so the returned stop is
    always at least `rail_atr x ATR` away from the confirming close.  That is
    the leg F-C4-RAIL asserts per advance.
    """
    src = fr.low_by_conf if direction == 1 else fr.high_by_conf
    hit = src.get(int(j))
    if hit is None:
        return None
    pv, pbar = hit
    if forbidden is not None and bool(forbidden[pbar]):
        return None
    if not (np.isfinite(atr) and atr > 0 and np.isfinite(close)):
        return None
    if direction == 1:
        cand = pv - buf_atr * atr
        rail = close - rail_atr * atr
        admitted = min(cand, rail)              # the FARTHER stop below price
        rail_bound = rail < cand                # the rail, not the pivot, set it
        # MONOTONE: advance only. The register row is READ, not remembered —
        # a constant no code consults is a constant that can drift silently,
        # which is the F-C3-e defect in miniature.
        if monotone and not (admitted > cur_stop):
            return None
    else:
        cand = pv + buf_atr * atr
        rail = close + rail_atr * atr
        admitted = max(cand, rail)              # the FARTHER stop above price
        rail_bound = rail > cand
        if monotone and not (admitted < cur_stop):
            return None
    return Advance(
        conf_i=int(j), conf_ms=int(open_ms[j]), pivot_val=float(pv),
        pivot_bar=int(pbar), pivot_bar_ms=int(open_ms[pbar]),
        atr=float(atr), close=float(close), cand_px=float(cand),
        rail_px=float(rail), new_stop=float(admitted),
        prev_stop=float(cur_stop), rail_binding=bool(rail_bound),
        dist_from_close_over_atr=float(abs(close - admitted) / atr))


# ══════════════════════════════════════════ THE HARVEST — the card's diff (2)
def harvest_edge(e89_j: float, e316_j: float, direction: int) -> float:
    """The NEAR edge of the opposing 89/316 band — the price the touch tests.

    A short lives BELOW the band, so the edge it meets coming back up is the
    LOWER of the two EMAs; a long lives above, so its edge is the UPPER.  Taken
    as min/max rather than "e89" so the rule survives an inversion of the pair
    (which is a bell, but a rule that depends on a bell having already fired is
    a rule with a hidden precondition).
    """
    return max(e89_j, e316_j) if direction == 1 else min(e89_j, e316_j)


def harvest_outside(px: float, edge: float, direction: int) -> bool:
    """Is `px` on the trade's OWN side of the band's near edge — i.e. OUTSIDE
    the band, where the campaign has to be for a touch to be a touch?

    THE PRECONDITION THE FIRST DRAFT LEFT UNSTATED.  The card says the touch is
    "price INTO the band FROM BELOW" for a short (mirror for a long), and
    "from below" is a precondition, not decoration: a short whose trigger close
    already sits inside the 89/316 band satisfies `high >= near edge` on the
    very next bar and books 50% out having crossed nothing.  `harvest_edge`
    removed the EMA-ORDERING precondition with its min/max and left this one
    unguarded — found by the post-build adversarial review, which also replayed
    all 153 campaigns across the three windows and found ZERO entries inside
    the band, so the guard changes no number in this build and exists because
    "it did not happen to bind" is not a rule.
    """
    return bool(px < edge) if direction == -1 else bool(px > edge)


def harvest_touched(high_j: float, low_j: float, edge: float,
                    direction: int) -> bool:
    """TOUCH is INTRABAR — the bar's own extreme against the edge.  The caller
    must also hold `harvest_outside` on the LAST CLOSED bar, or this is not a
    touch but a position that was already inside the band."""
    return bool(low_j <= edge) if direction == 1 else bool(high_j >= edge)


def harvest_fill_px(close_j: float, rule: str = REGISTER["HARVEST_FILL"]["value"]
                    ) -> float:
    """THE FILL PRICE, dispatched on the register row rather than assumed.

    The card names the touch instant and the fill instant separately, and the
    register row `HARVEST_FILL` records which one the fill takes.  Reading it
    here — instead of hard-coding `f.c[j]` at the call site and letting the row
    describe the code from a distance — is what stops the row and the code from
    drifting apart.  An unrecognised value HALTs rather than silently falling
    back to the close.
    """
    if rule != "bar_close":
        raise SystemExit(
            f"HALT: HARVEST_FILL = {rule!r} is not a rule this program knows. "
            f"The card names 'bar_close'. A fill rule the code cannot enact "
            f"must stop the build, not be quietly ignored.")
    return float(close_j)


# ═══════════════════════════════════════════════════════════════ the record
@dataclass
class Trade:
    """Tier-C3's Trade, plus the columns the two amendments make meaningful.

    `scored` is the F-5 rule in the record itself: the ENTRY bar lies inside the
    window rather than in its 30-day lead-in.  A trade with `scored = False`
    carries NO outcome — no gross R, no net R, no prices — because an outcome
    computed over a bar the corridor excludes is scored evidence wearing a
    label, and for the SCORED window that bar is sealed.

    THE HALVES BOOK THEIR OWN R.  `net_r_harvest_half + net_r_runner_half ==
    net_r` exactly when a campaign harvested (asserted, 1e-9, F-C4-HARV): the
    entry fee splits 50/50, each half pays its own exit fee, and funding accrues
    on the size actually held into each bar.  Both are None when it did not.
    """
    symbol: str
    direction: int
    arm_i: int
    arm_ms: int
    entry_i: int
    entry_ms: int
    entry_px: float
    stop_px: float                       # the ENTRY stop — R's denominator, forever
    r_dist: float
    pivot_anchor: float
    anchor_bar_ms: int
    anchor_in_lockbox: bool
    n_eligible_anchors: int
    atr_at_entry: float
    disp_at_arming: float
    exit_i: int
    exit_ms: int
    exit_px: float
    exit_reason: str
    bars_held: int
    scored: bool
    armed_in_lead_in: bool
    pivot_stop_px: float
    pivot_dist: float
    rail_dist: float
    rail_binding: bool
    # ── the v4 columns ────────────────────────────────────────────────────
    advances: list = field(default_factory=list)     # list[Advance]
    final_stop_px: float = float("nan")              # the stop at the exit bar
    stop_advanced_atr: float = float("nan")          # (final - entry stop)/ATR, favourable +
    ratchet_exit: bool = False                       # stopped out ON an advanced stop
    harvested: bool = False
    harvest_i: int | None = None
    harvest_ms: int | None = None
    harvest_px: float | None = None
    harvest_edge_px: float | None = None
    harvest_bars_after_entry: int | None = None
    harvest_blocked_by: str = ""                     # "stop" | "bell" | ""
    entered_outside_band: bool = True                # the "from below" precondition
    mfe_px: float = float("nan")                     # best favourable extreme in the ride
    mfe_r: float = float("nan")
    # ── outcome.  None for an unscored lead-in trade, by rule. ────────────
    gross_r: float | None = None
    fee_r: float | None = None
    funding_r: float | None = None
    net_r: float | None = None
    net_r_harvest_half: float | None = None
    net_r_runner_half: float | None = None
    gross_r_bellonly: float | None = None
    net_r_bellonly: float | None = None
    exit_reason_bellonly: str | None = None
    exit_ms_bellonly: int | None = None
