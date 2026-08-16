"""TIER-C3 · THE RAILED BASELINE — THE DECISION PATH, AND NOTHING ELSE.

RATIFIED operator 2026-08-15 ("I rule the seven F's on your lean").  Drafted
APOLLO · Executor HEPHAESTUS · Seed 20260815.

CLASS: MEASUREMENT, NOT REGISTRATION.  m = 0.  No lockbox read for outcomes.
No estate write.  No live orders.

────────────────────────────────────────────────────────────────────────────
BYTE-INHERITANCE IS BY IMPORT, NOT BY COPY
────────────────────────────────────────────────────────────────────────────
The card diffs are the ONLY rule changes.  Everything else does not merely
*look* the same as Tier-C2 — it IS the same object.  `build_4h`, `_crosses`,
`armings`, `Frame4h` and `Arming` below are bound straight to the Tier-C2
module's symbols, so a diff in the inherited half is impossible rather than
unlikely.  `tierc3_fixtures.F-C3-INHERIT` asserts the identity with `is`.

Three things are new, and only three:

    F-3  THE ANCHOR MOVES TO THE SYSTEM'S OWN LENS.  The structural anchor is
         the nearest REAL 4h swing pivot beyond entry; 1H pivots are retired
         from this card.  `struct_stop_4h` replaces `struct_stop`.
    F-3  THE RAIL.  stop distance = max(pivot distance, MIN_STOP_ATR x ATR_4h
         at entry), MIN_STOP_ATR = 1.0.  Every scored trade therefore has
         R >= 1.0 ATR — asserted per trade, F-C3-RAIL.
    F-4  THE STOP EXECUTES, stated as card text rather than left to a reading.
         A bar touching the stop exits AT the stop, adverse-first.  (The rule
         is enacted in the runner's ride; it is written into RULE_CARD_V3 here
         so the card and the code carry the same sentence.)

And one thing that is NOT a card diff and must never be mistaken for one:

    SEAL FLOOR (CLASS).  `struct_stop_4h(..., forbidden=)` masks sealed bars
    out of anchor eligibility.  The CARD does not say this; the ratified CLASS
    LINE does ("NO lockbox read; 462 sealed days untouched"), and executing the
    card literally would quote a sealed bar's low as a scored trade's anchor,
    R denominator and exit price.  Precedent is Tier-C2 §0: the corridor moved,
    the seal did not.  Both numbers are printed — see the attribution table —
    so the operator can overturn this in one line (F-C3-a).

F-C3-6 · CAPTURED-NOT-CONSULTED still holds by construction: this module's
transitive import closure is {numpy, dataclasses, engine.*, tierc2_rules} and
contains no `analytics` member.  Amendment B1's tape is joined downstream, by
timestamp, and is never read back into a decision.
────────────────────────────────────────────────────────────────────────────
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from engine.s1 import _pivots

# The Tier-C2 decision path.  Analytics-free itself, so importing it cannot
# introduce a registry symbol — F-C3-6 proves that by closure, not by promise.
import tierc2_rules as V1

# ═══════════════════════════════════ BYTE-INHERITED — the SAME objects, bound
Frame4h = V1.Frame4h
Arming = V1.Arming
build_4h = V1.build_4h
_crosses = V1._crosses
armings = V1.armings

UNIVERSE = V1.UNIVERSE
LENS = V1.LENS
TIDE_FAST, TIDE_SLOW = V1.TIDE_FAST, V1.TIDE_SLOW
WINDOW_FAST, WINDOW_SLOW = V1.WINDOW_FAST, V1.WINDOW_SLOW
TRIGGER_FAST, TRIGGER_SLOW = V1.TRIGGER_FAST, V1.TRIGGER_SLOW
D_DISPLACEMENT, D_STRIP = V1.D_DISPLACEMENT, V1.D_STRIP
ATR_LEN = V1.ATR_LEN
FEE_BPS_SIDE = V1.FEE_BPS_SIDE
FEE_BPS_ROUND_TRIP = V1.FEE_BPS_ROUND_TRIP
PIVOT_L, PIVOT_R = V1.PIVOT_L, V1.PIVOT_R
STOP_BUF_ATR = V1.STOP_BUF_ATR
MS_4H, MS_1H = V1.MS_4H, V1.MS_1H
FUNNEL_STAGES = V1.FUNNEL_STAGES

INHERITED = ("Frame4h", "Arming", "build_4h", "_crosses", "armings")

# ═══════════════════════════════════════════════ THE CARD DIFFS · registered
# F-C3-3 posture, inherited from F-C2-3: no value is invented.  Each row names
# where the number came from.  The two NEW rows name the RULING that made them,
# because a ruling is a source of record and pretending otherwise would be the
# defect.
REGISTER_DIFF: dict[str, dict] = {
    "PIVOT_LOOKBACK_4H": {
        "value": 200,
        "source": "F-3 ruling (operator 2026-08-15) moves the anchor to the 4h "
                  "lens; the LOOKBACK CONSTANT is byte-inherited from "
                  "engine/trading.py:222 `struct_stop_at` (200 bars in the "
                  "pivot's OWN lens, which was 1h there and is 4h here). The "
                  "time-equivalent reading — 50 bars = the same 200 hours — is "
                  "NOT taken, and the count of trades whose anchor would differ "
                  "under it is printed as a disclosure (unscored).",
    },
    "MIN_STOP_ATR": {
        "value": 1.0,
        "source": "F-3 ruling (operator 2026-08-15, 'I rule the seven F's on "
                  "your lean'): RAIL stop distance = max(pivot distance, 1.0 x "
                  "ATR_4h at entry). Strictly WIDER than the architecture of "
                  "record's own rail `min_stop_atr: 0.5` (configs/tc1_B.yaml:53, "
                  "engine guard G-8c, engine/trading.py:555-560), which is the "
                  "rail Tier-C2's F-3 measured this card against and found absent.",
    },
    "LEAD_IN_DAYS": {
        "value": 30,
        "source": "F-5 ruling (operator 2026-08-15): armings admitted from "
                  "scored_start - 30d. 30 is the span Tier-C2's F-5 MEASURED "
                  "(BUILD_2026-08-15_TIERC2_BASELINE.md §9 F-5: 4 armings passed "
                  "tide+d in the 30 days before the corridor, 2 triggered inside "
                  "it), so the number is the finding's own, not a new choice.",
    },
    "SEAL_FLOOR_ON_ANCHOR": {
        "value": True,
        "source": "NOT A CARD DIFF — THE CLASS LINE, ENACTED. The ratified CLASS "
                  "for this build is 'NO lockbox read (462 sealed days "
                  "untouched)'. The card as written has no seal floor, and "
                  "executing it literally selects the low of the SEALED 4h bar "
                  "2025-09-15T12:00Z as the anchor of a scored trade — a price "
                  "published in the journal, used as the R denominator and paid "
                  "as the exit price. Precedent: BUILD_2026-08-15_TIERC2_BASELINE "
                  "§0 — when the ratified corridor collided with the seal, "
                  "'the corridor moved, the seal did not'. So the seal moves "
                  "nothing here either: sealed bars are masked out of anchor "
                  "eligibility. TAKEN, DISCLOSED, AND PRINTED BOTH WAYS so the "
                  "operator can overturn it in one line (finding F-C3-a).",
    },
    "STRIP_TRUNCATE": {
        "value": "2026-07-07T23:59:59Z",
        "source": "F-7 ruling (operator 2026-08-15): every display-only "
                  "continuity strip truncates at VR-1's forward edge "
                  "(V12_Study_Charter_Addendum_v1.0.md VR-1 — after it is "
                  "'Naiad's domain; the v12 Study never reads it').",
    },
}

REGISTER: dict[str, dict] = {**V1.REGISTER, **REGISTER_DIFF}

# F-3 retired the 1H pivot from this card.  Its register row is INHERITED but
# RETIRED, and is named here so the fixture prints it as retired rather than as
# a live constant nothing reads.  A stale row in a closed register is how a
# retired rule comes back.
RETIRED_FROM_V1: tuple[str, ...] = ("PIVOT_LOOKBACK_1H",)

PIVOT_LOOKBACK_4H: int = REGISTER["PIVOT_LOOKBACK_4H"]["value"]
MIN_STOP_ATR: float = REGISTER["MIN_STOP_ATR"]["value"]
LEAD_IN_DAYS: int = REGISTER["LEAD_IN_DAYS"]["value"]
SEAL_FLOOR_ON_ANCHOR: bool = REGISTER["SEAL_FLOOR_ON_ANCHOR"]["value"]

# The time-equivalent lookback, computed not typed: 200 one-hour bars is 200
# hours, which is 50 four-hour bars.  Used ONLY by the disclosure.
PIVOT_LOOKBACK_4H_TIME_EQUIV: int = int(
    V1.PIVOT_LOOKBACK_1H * V1.MS_1H // MS_4H)

# ═══════════════════════════════════════════════════ THE RULE CARD v3, verbatim
RULE_CARD_V3 = """\
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
LEAD-IN [F-5]: armings are admitted from scored_start - 30d; a trade is SCORED
  iff its ENTRY bar lies inside the scored window
RIDE: no management of any kind
BELL: counter 4h 12/89 OR 4h 89/316 against -> exit at close
ACCOUNTING ["accounting"]: net of 10 bps round-trip + journaled funding; R units
STRIPS [F-7]: every display-only continuity strip truncates at 2026-07-07T23:59Z
SEAL FLOOR [CLASS, not a card diff]: no pivot lying on a SEALED bar may be an
  anchor. An anchor is a PRICE that is published, denominates R and is paid out
  on a stop — not a recursion state — so the CLASS line "NO lockbox read" masks
  it. A trade left with no admissible anchor is NOT TAKEN. Printed both ways."""


# ═══════════════════════════════════════════════ THE STOP — the card's diff
@dataclass
class Pivots4h:
    """Confirmed 4h (5,5) swing pivots — Tier-C2's `Pivots1h` shape on the lens
    F-3 moved the anchor to, plus the one field that shape was missing: the
    index of the PIVOT BAR ITSELF.

    `*_conf` is when the pivot became knowable (pivot bar + R).  `*_bar` is the
    bar whose high or low IS the published anchor price.  Tier-C2 never needed
    the distinction because its 200-bar 1h lookback reached 8.3 days and its
    corridor began 24 days after the seal.  On the 4h lens the same 200 bars
    reach 33.3 days, so the two eras can meet — and an era test that cannot
    name the anchor's own bar cannot see it.  See `forbidden` below.
    """
    low_conf: np.ndarray
    low_val: np.ndarray
    low_bar: np.ndarray
    high_conf: np.ndarray
    high_val: np.ndarray
    high_bar: np.ndarray


def build_pivots_4h(h4_high, h4_low) -> Pivots4h:
    """Confirmed 4h (5,5) swing pivots — the REAL pivots of the system's own
    lens, replacing Tier-C2's 1h grid per F-3.

    `engine.s1._pivots` is the estate's pivot of record and is called with the
    SAME (L, R) the 1h card used: the ruling moved the LENS, not the shape.
    `conf` is the bar index at which the pivot becomes KNOWABLE (pivot bar + R);
    a caller working as-of bar k filters `conf <= k`, and that filter is the
    whole reason this is causal.
    """
    lc, lv = _pivots(np.asarray(h4_low, float), PIVOT_L, PIVOT_R, low=True)
    hc, hv = _pivots(np.asarray(h4_high, float), PIVOT_L, PIVOT_R, low=False)
    # `_pivots` returns (p + R, x[p]); the pivot bar is therefore conf - R.
    return Pivots4h(low_conf=lc, low_val=lv, low_bar=lc - PIVOT_R,
                    high_conf=hc, high_val=hv, high_bar=hc - PIVOT_R)


@dataclass
class Stop:
    """A stop, and the arithmetic that produced it — so neither the rail nor the
    anchor's provenance can ever be invisible in the record."""
    stop_px: float
    anchor: float                # the raw 4h pivot the structure names
    anchor_bar: int              # the INDEX of the bar whose high/low that is
    pivot_stop_px: float         # anchor -/+ 0.5 x ATR — the card before the rail
    pivot_dist: float            # |entry - pivot_stop_px|
    rail_dist: float             # min_stop_atr x ATR_4h at entry
    r_dist: float                # max(pivot_dist, rail_dist) — the card's R
    rail_binding: bool           # True iff the rail widened the stop
    n_eligible: int              # how many anchors the card had to choose from


def struct_stop_4h(pv: Pivots4h, cur_i: int, entry_px: float, direction: int,
                   atr_sig: float, lookback: int = PIVOT_LOOKBACK_4H,
                   min_stop_atr: float = MIN_STOP_ATR,
                   forbidden: np.ndarray | None = None) -> Stop | None:
    """THE v3 STOP.  Nearest confirmed 4h (5,5) pivot strictly beyond entry
    within `lookback` 4h bars, offset -/+ 0.5 x ATR(entry bar), THEN RAILED so
    the distance is never below `min_stop_atr` x ATR.

    Returns None => `no_struct_anchor`, and the tranche is NOT taken — the
    Tier-C2 behaviour byte-for-byte.  The rail does NOT invent a stop where
    structure names none: the card says "anchor beyond the nearest real pivot,
    railed", so with no anchor there is no card stop to rail.

    `cur_i` is the 4h index of the ENTRY bar, so no pivot later than the entry
    instant is ever eligible.

    ── `forbidden` · THE SEAL FLOOR ──────────────────────────────────────────
    A boolean mask over bar indices; a pivot whose OWN BAR is masked may not be
    an anchor.  It exists because the anchor is not a recursion state — it is a
    PRICE, selected by name, published verbatim in the journal, used as the R
    denominator and paid out as the exit price when the stop fires.  The F4-a
    precedent ("traversal is not emission") covers an EMA that swept a sealed
    bar on its way to being warm; it does not cover quoting that bar's low.
    Under a CLASS line that says NO LOCKBOX READ, the sealed bars are masked
    and a trade that has no other anchor is simply not taken.  The mask is
    passed IN rather than known here, because the eras belong to the runner.

    `lookback` and `min_stop_atr` are parameters only so the disclosure and the
    attribution table can re-ask the same question without a second copy of
    this logic.  The card's values are the defaults.
    """
    if not np.isfinite(atr_sig):
        return None
    if direction == 1:
        elig = ((pv.low_conf <= cur_i)
                & (cur_i - pv.low_conf <= lookback)
                & (pv.low_val < entry_px))
        if forbidden is not None:
            elig = elig & ~forbidden[pv.low_bar]
        if not elig.any():
            return None
        k = int(np.flatnonzero(elig)[np.argmax(pv.low_val[elig])])
        anchor, anchor_bar = float(pv.low_val[k]), int(pv.low_bar[k])
        pivot_stop = anchor - STOP_BUF_ATR * atr_sig
        rail_stop = entry_px - min_stop_atr * atr_sig
        stop_px = min(pivot_stop, rail_stop)            # the FARTHER stop below
    else:
        elig = ((pv.high_conf <= cur_i)
                & (cur_i - pv.high_conf <= lookback)
                & (pv.high_val > entry_px))
        if forbidden is not None:
            elig = elig & ~forbidden[pv.high_bar]
        if not elig.any():
            return None
        k = int(np.flatnonzero(elig)[np.argmin(pv.high_val[elig])])
        anchor, anchor_bar = float(pv.high_val[k]), int(pv.high_bar[k])
        pivot_stop = anchor + STOP_BUF_ATR * atr_sig
        rail_stop = entry_px + min_stop_atr * atr_sig
        stop_px = max(pivot_stop, rail_stop)            # the FARTHER stop above
    pivot_dist = abs(entry_px - pivot_stop)
    rail_dist = min_stop_atr * atr_sig
    return Stop(stop_px=float(stop_px), anchor=anchor, anchor_bar=anchor_bar,
                pivot_stop_px=float(pivot_stop), pivot_dist=float(pivot_dist),
                rail_dist=float(rail_dist),
                r_dist=float(abs(entry_px - stop_px)),
                rail_binding=bool(rail_dist > pivot_dist),
                n_eligible=int(elig.sum()))


# ═══════════════════════════════════════════════════════════════ the record
@dataclass
class Trade:
    """Tier-C2's Trade, plus the four columns the v3 card makes meaningful.

    `scored` is the F-5 rule in the record itself: the ENTRY bar lies inside
    the window rather than in its 30-day lead-in.  In the SCORED window that is
    exactly the card's definition of a scored trade.  In a DISPLAY-ONLY window
    it means only "this trade belongs to that strip" — nothing in a display
    window is scored at all, whatever this flag says, and those rows never
    reach `headline.parquet`.

    A trade with `scored = False` carries NO outcome: no gross R, no net R, no
    prices.  An outcome computed over a bar the corridor excludes is scored
    evidence wearing a label, and for the SCORED window that bar is sealed.
    """
    symbol: str
    direction: int
    arm_i: int
    arm_ms: int
    entry_i: int
    entry_ms: int
    entry_px: float
    stop_px: float
    r_dist: float
    pivot_anchor: float
    anchor_bar_ms: int           # the bar the anchor PRICE was quoted from
    anchor_in_lockbox: bool      # ... and whether that bar is sealed
    n_eligible_anchors: int
    atr_at_entry: float
    disp_at_arming: float
    exit_i: int
    exit_ms: int
    exit_px: float
    exit_reason: str
    bars_held: int
    # ── the v3 columns ────────────────────────────────────────────────────
    scored: bool
    armed_in_lead_in: bool
    pivot_stop_px: float
    pivot_dist: float
    rail_dist: float
    rail_binding: bool
    # ── outcome.  None for an unscored lead-in trade, by rule. ────────────
    gross_r: float | None = None
    fee_r: float | None = None
    funding_r: float | None = None
    net_r: float | None = None
    gross_r_bellonly: float | None = None
    net_r_bellonly: float | None = None
    exit_reason_bellonly: str | None = None
    exit_ms_bellonly: int | None = None
