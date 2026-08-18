"""TIER-C7 · THE HYBRID R&H PROGRAM — THE DECISION PATH, AND NOTHING ELSE.

RATIFIED operator 2026-08-17.  Resume word "TC7 GO" given after TC6-V closed the
audit; P-AE-1 ruled **CARD-CONDITIONAL, arm kept**.

THE PINS, OPERATOR-RATIFIED AND VERBATIM-LOCKED:

    D-R1  ARM            ladder/trail arms only after a +1R unit move
    D-R2  HYBRID ANCHOR  stop = max(4h pivot(2,2), e89) - 0.5 ATR in the trade
                         direction, rail 1.0, advance-only, min-advance 0.05
    D-R3  WEAVE          on 4h: (i) M-ribbon width contracting over its
                         k-window AND M-median slope <= 0, AND (ii) the fast
                         ribbon closes back inside-or-beyond the M-band against
                         the trade.  Close-confirmed, TWO CLAUSES ONLY.
    D-R4  WEAVE ACTION   exit the remainder to FLAT
    D-R5  RE-ENTRY       after any weave-exit or ladder-out, the first close
                         back beyond the fast ribbon in the trend direction
                         within 24 bars, tide still agreeing -> re-enter, with a
                         fresh structural stop (new pivot, railed).
                         MAX ONE re-entry per chain.
    D-R6  CHAIN          exit + re-entry is ONE campaign for ALL accounting:
                         D15, concentration and the funding ceiling accumulate
                         across the chain; the journal shows both legs.

Drafted APOLLO · Executor HEPHAESTUS · Seed 20260817.

CLASS: measurement + FOUR pre-registered claims + pre-named labs.  D15 columns
everywhere, gates nowhere.  LOAO-3/5 on every registration table [E1 law].

────────────────────────────────────────────────────────────────────────────
THREE READINGS THE PINS DID NOT SETTLE, SETTLED HERE AND NAMED
────────────────────────────────────────────────────────────────────────────
A verbatim-locked pin still has to become code, and three of these have more
than one faithful reading.  Each is decided here, in the decision path, with the
alternative stated so a reader can see that a choice was made.

(1) "M-MEDIAN SLOPE <= 0" IS READ AS **AGAINST THE TRADE**.
    Taken literally the clause would fire on a falling M-median whatever the
    position — which for a SHORT is momentum running IN ITS FAVOUR, so the weave
    would exit winning shorts and never fire on losing ones.  The clause is
    therefore read as `slope * direction <= 0`: the M-median is no longer moving
    the way the position needs.  For a long that IS the literal text; for a
    short it is its mirror.  THE ALTERNATIVE — a literal direction-agnostic
    `slope <= 0` — is NOT taken, and it is not taken because it makes the rule
    asymmetric in a way nothing in the commission asks for.

(2) "THE FAST RIBBON CLOSES BACK INSIDE-OR-BEYOND THE M-BAND" IS READ ON THE
    RIBBON'S TRADE-SIDE EDGE.  The fast ribbon is a BAND, not a price, so
    "closes back inside" needs an edge.  For a long the edge that matters is the
    ribbon's LOW (`fast_lo <= m_hi`: the fast ribbon has fallen back to or into
    the M band).  For a short it is the ribbon's HIGH (`fast_hi >= m_lo`).
    "Inside-OR-BEYOND" is why the test is an inequality and not a containment:
    a fast ribbon that has punched clean through the M band has certainly come
    back.  THE ALTERNATIVE — requiring the ribbon to be strictly INSIDE the band
    — is NOT taken; it would refuse the most decisive version of the signal.

(3) THE WEAVE'S k-WINDOW IS PINNED AT 6 BARS AND IS NOT SWEPT.
    The commission says "over its k-window" and does not give k.  Six 4h bars is
    one day, which is the shortest window over which "contracting" is a claim
    about structure rather than about two bars of noise.  It is pinned HERE,
    before the look, as a register row.  IT IS NOT SWEPT AND NO GRID IS BUILT
    OVER IT — so it is an assumption, not a comparison, and the build document
    says so on the registration's face rather than leaving a reader to assume it
    was tuned.

────────────────────────────────────────────────────────────────────────────
INHERITANCE: FIVE GENERATIONS, BY IMPORT, AND THE CARD SUBCLASSES AGAIN
────────────────────────────────────────────────────────────────────────────
`import tierc6_rules as V6` -> V5 -> V4 -> V3 -> V2.  `Card` subclasses
`V6.Card`, which subclasses `V5.Card`, so `isinstance(v7_card, V5.Card)` holds
and every knob from every ancestor arrives untyped.  F-C7-INHERIT asserts the
chain with `is`.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import tierc6_rules as V6                                            # noqa: E402
import tierc5_rules as V5                                            # noqa: E402
from engine import indicators as ind                                 # noqa: E402

# ═══════════════════════════════════════════ BOUND, NOT COPIED — five deep
UNIVERSE = V6.UNIVERSE
TIDE_FAST, TIDE_SLOW = V6.TIDE_FAST, V6.TIDE_SLOW
STOP_BUF_ATR, MIN_STOP_ATR = V6.STOP_BUF_ATR, V6.MIN_STOP_ATR
RATCHET_PIVOT_L, RATCHET_PIVOT_R = V6.RATCHET_PIVOT_L, V6.RATCHET_PIVOT_R
RATCHET_BUF_ATR, RATCHET_RAIL_ATR = V6.RATCHET_BUF_ATR, V6.RATCHET_RAIL_ATR
RATCHET_MONOTONE = V6.RATCHET_MONOTONE
HARVEST_FRACTION, ATR_LEN = V6.HARVEST_FRACTION, V6.ATR_LEN
FEE_BPS_SIDE, FUNDING_CEILING_R = V6.FEE_BPS_SIDE, V6.FUNDING_CEILING_R
WARMUP_BARS, PROVISIONAL_MIN_N = V6.WARMUP_BARS, V6.PROVISIONAL_MIN_N
SPRING_LOOKBACK_BARS, SPRING_RECLAIM_BARS = (V6.SPRING_LOOKBACK_BARS,
                                             V6.SPRING_RECLAIM_BARS)
ADDS_MAX, LOCKBOX_WAS = V6.ADDS_MAX, V6.LOCKBOX_WAS
RIBBONS = V5.RIBBONS
MS_4H, MS_12H = V6.MS_4H, V6.MS_12H

build_4h, Frame4h, Arming = V6.build_4h, V6.Frame4h, V6.Arming
armings, struct_stop_4h = V6.armings, V6.struct_stop_4h
build_pivots_4h, build_fractals = V6.build_pivots_4h, V6.build_fractals
Fractals4h, Advance = V6.Fractals4h, V6.Advance
harvest_edge, harvest_touched = V6.harvest_edge, V6.harvest_touched
harvest_outside, harvest_fill_px = V6.harvest_outside, V6.harvest_fill_px
Spring, spring_signals, spring_stop = (V6.Spring, V6.spring_signals,
                                       V6.spring_stop)
Add, add_context = V6.Add, V6.add_context
add_retraced, add_reclaimed = V6.add_retraced, V6.add_reclaimed
sealed_mask, Trade = V6.sealed_mask, V6.Trade
ribbon_band = V5.ribbon_band
trail_step = V6.trail_step                       # the v6 ladder, unchanged
wall_series_12h, wall_touch = V6.wall_series_12h, V6.wall_touch
wall_alignment = V6.wall_alignment

# ═══════════════════════════════════════════════════════════ THE REGISTER, v7
REGISTER: dict[str, dict] = {
    "ARM_AFTER_R": {
        "value": 1.0, "ruling": "D-R1",
        "text": "the ladder does not advance until the campaign's favourable "
                "excursion has reached +1R at least once — a high-water latch",
        "was": "v6: the same, carded under H5",
    },
    "HYBRID_ANCHOR": {
        "value": "max(pivot(2,2), e89)", "ruling": "D-R2 (pre-named prior)",
        "text": "the ladder's anchor is the TIGHTER of the confirming 4h "
                "fractal pivot and the tide-fast EMA, offset 0.5 ATR into the "
                "trade direction, railed 1.0 ATR from the confirming close, "
                "advance-only, minimum advance 0.05 ATR",
        "was": "v6: the pivot alone",
    },
    "LADDER_OFFSET_ATR": {
        "value": STOP_BUF_ATR, "ruling": "D-R2 / F-C4-b",
        "text": "how far beyond the anchor the ladder sets its stop",
        "was": "unchanged since v4",
    },
    "LADDER_RAIL_ATR": {
        "value": MIN_STOP_ATR, "ruling": "D-R2 / card",
        "text": "and never closer than this to the confirming close",
        "was": "unchanged since v4",
    },
    "LADDER_MIN_ADVANCE_ATR": {
        "value": 0.05, "ruling": "D-R2 / F-C4-d",
        "text": "a candidate advance smaller than this, measured as "
                "abs(new_stop - prev_stop) / ATR, is NOT taken",
        "was": "v6: the same",
    },
    "WEAVE_K": {
        "value": 6, "ruling": "D-R3 (pinned here; the commission gives no k)",
        "text": "the window over which the M-ribbon width must be contracting. "
                "Six 4h bars is one day — the shortest window over which "
                "'contracting' is a claim about structure rather than about "
                "two bars of noise. PINNED BEFORE THE LOOK AND NOT SWEPT: it "
                "is an assumption, not a comparison, and the registration says "
                "so on its face.",
        "was": "not present in any prior tier",
    },
    "WEAVE_SLOPE_READING": {
        "value": "slope * direction <= 0", "ruling": "D-R3, read",
        "text": "'M-median slope <= 0' is read AGAINST THE TRADE. Taken "
                "literally the clause fires on a falling M-median whatever the "
                "position, which for a SHORT is momentum in its favour — the "
                "weave would exit winning shorts and never fire on losing "
                "ones. The literal direction-agnostic reading is NOT taken.",
        "was": "not present in any prior tier",
    },
    "WEAVE_EDGE_READING": {
        "value": "the ribbon's TRADE-SIDE edge", "ruling": "D-R3, read",
        "text": "'the fast ribbon closes back inside-or-beyond the M-band' is "
                "tested on the fast ribbon's LOW for a long and its HIGH for a "
                "short, against the M band's near edge. 'inside-OR-BEYOND' is "
                "why it is an inequality and not a containment. Requiring the "
                "ribbon to be strictly INSIDE the band is NOT taken.",
        "was": "not present in any prior tier",
    },
    "REENTRY_WINDOW_BARS": {
        "value": 24, "ruling": "D-R5",
        "text": "after a weave-exit or ladder-out, the first close back beyond "
                "the fast ribbon in the trend direction within this many bars, "
                "with the tide still agreeing, re-enters the chain",
        "was": "not present in any prior tier",
    },
    "REENTRIES_MAX_PER_CHAIN": {
        "value": 1, "ruling": "D-R5",
        "text": "MAX ONE re-entry per chain. A chain is a round trip, not a "
                "strategy for repeatedly buying the same idea.",
        "was": "not present in any prior tier",
    },
    "CHAIN_IS_ONE_CAMPAIGN": {
        "value": True, "ruling": "D-R6",
        "text": "exit + re-entry is ONE campaign for ALL accounting — D15, "
                "concentration and the D12 funding ceiling accumulate ACROSS "
                "the chain. The journal shows both legs. Accounting a chain as "
                "two campaigns would halve its concentration and double-count "
                "the funding ceiling's headroom.",
        "was": "not present in any prior tier",
    },
    "AE_ABORT_R": {
        "value": 0.60, "ruling": "P-AE-1, operator 2026-08-17",
        "text": "exit any campaign whose maximum adverse excursion reaches "
                "0.60R. PRE-NAMED FROM TIER-C6's HAZARD CURVE, where "
                "P(win | MAE >= 0.60R) = 7.03%. RULED CARD-CONDITIONAL: the "
                "TC6-V audit established that the held-excursion distribution "
                "is CENSORED AT THE CARD'S OWN 1R RAIL (110 of 196 campaigns "
                "sit at exactly -1.0R; the uncensored tape reaches -4.59R), so "
                "the 7.03% is a fact about campaigns UNDER THIS CARD and not "
                "about the market. The arm is kept and scored on that reading, "
                "and the reading rides the registration row.",
        "was": "not present in any prior tier",
    },
}

ARM_AFTER_R: float = REGISTER["ARM_AFTER_R"]["value"]
WEAVE_K: int = REGISTER["WEAVE_K"]["value"]
REENTRY_WINDOW_BARS: int = REGISTER["REENTRY_WINDOW_BARS"]["value"]
REENTRIES_MAX_PER_CHAIN: int = REGISTER["REENTRIES_MAX_PER_CHAIN"]["value"]
AE_ABORT_R: float = REGISTER["AE_ABORT_R"]["value"]


# ═════════════════════════════════════════════════════════════ THE CARD, v7
@dataclass(frozen=True)
class Card(V6.Card):
    """v6's card, six fields wider — and every one of them OFF by default.

    THE DEFAULTS ARE v6.  `Card()` with no arguments IS card v6, which is what
    makes F-C7-CTRL a control rather than a coincidence: the v6 book is
    reproduced by this module's own code path with every v7 knob at its default,
    so "v7 with its knobs off IS v6" is a claim the fixture can check.

    Each arm of the program turns exactly one knob, and the FULL HYBRID turns
    all four — which is what makes the ablation ladder an attribution rather
    than a list of separate programs.
    """
    name: str = "v7-default(=v6)"
    hybrid_anchor: bool = False        # D-R2  the ladder anchor
    weave: bool = False                # D-R3/D-R4  exit remainder to flat
    reentry: bool = False              # D-R5  one re-entry per chain
    ae_abort_r: float | None = None    # P-AE-1  early invalidation
    weave_k: int = WEAVE_K             # D-R3  the contraction window
    stop_grid_offset_atr: float = 0.0  # S-STOPGRID  initial stop offset


CARD_V6_CONTROL = Card(name="v6-control")
CARD_HYBRID = Card(name="v7-hybrid", hybrid_anchor=True, weave=True,
                   reentry=True)
CARD_LADDER_ONLY = Card(name="v7-ladder-only", hybrid_anchor=True)
CARD_WEAVE_ONLY = Card(name="v7-weave-only", weave=True)
CARD_WEAVE_RE = Card(name="v7-weave+reentry", weave=True, reentry=True)
CARD_AE = Card(name="v7-ae-abort", ae_abort_r=AE_ABORT_R)


# ═══════════════════════════════════════════ D-R2 · THE HYBRID LADDER ANCHOR
def ladder_step(fr: Fractals4h, j: int, direction: int, cur_stop: float,
                close: float, atr: float, e89: float, open_ms: np.ndarray,
                buf_atr: float = STOP_BUF_ATR,
                rail_atr: float = MIN_STOP_ATR,
                min_advance_atr: float = 0.05,
                forbidden: np.ndarray | None = None) -> Advance | None:
    """THE HYBRID ANCHOR, one bar of it.  Returns the Advance, or None.

    THE ANCHOR IS THE TIGHTER OF THE TWO, AND "TIGHTER" IS WHAT `max` MEANS FOR
    A LONG.  D-R2 reads `max(pivot(2,2), e89)`; for a long the higher of the
    two is the closer to price, so the ladder tracks whichever of structure and
    tide is currently doing more work.  For a SHORT the mirror is `min` — the
    lower of the two — and writing `max` there would take the anchor FARTHER
    from price on every short, which is the opposite rule.

    THE PIVOT MUST STILL CONFIRM.  e89 exists on every bar; the pivot does not.
    The anchor is only formed on a bar where a FAVOURABLE fractal confirms,
    exactly as the v6 ladder is — otherwise the tide alone would advance the
    stop every bar and this would be a different rule with the same name.
    That reading is why `fr` is still the first argument.

    Then, unchanged from v6: railed at `rail_atr` from the confirming close,
    ADVANCE-ONLY, and refused if the stop would move less than
    `min_advance_atr` — measured on `abs(new_stop - prev_stop) / atr`, which is
    exactly the quantity the ratchet ledger publishes as `advance_atr`.

    WHAT WOULD MAKE THIS WRONG: advancing on a bar with no confirming pivot;
    using `max` for both directions; measuring the minimum advance on the ANCHOR
    move rather than the STOP move (a large anchor move can leave a railed stop
    unchanged); or letting the stop retreat.
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
    if not np.isfinite(e89):
        return None
    if direction == 1:
        anchor = max(float(pv), float(e89))          # the TIGHTER of the two
        cand = anchor - buf_atr * atr
        rail = close - rail_atr * atr
        admitted = min(cand, rail)                   # the FARTHER stop below
        rail_bound = rail < cand
        if RATCHET_MONOTONE and not (admitted > cur_stop):
            return None
    else:
        anchor = min(float(pv), float(e89))          # the mirror
        cand = anchor + buf_atr * atr
        rail = close + rail_atr * atr
        admitted = max(cand, rail)
        rail_bound = rail > cand
        if RATCHET_MONOTONE and not (admitted < cur_stop):
            return None
    if min_advance_atr > 0.0:
        if abs(admitted - cur_stop) / atr < min_advance_atr:
            return None
    return Advance(
        conf_i=int(j), conf_ms=int(open_ms[j]), pivot_val=float(anchor),
        pivot_bar=int(pbar), pivot_bar_ms=int(open_ms[pbar]),
        atr=float(atr), close=float(close), cand_px=float(cand),
        rail_px=float(rail), new_stop=float(admitted),
        prev_stop=float(cur_stop), rail_binding=bool(rail_bound),
        dist_from_close_over_atr=float(abs(close - admitted) / atr))


# ══════════════════════════════════════════════════ D-R3 · THE WEAVE, 2 CLAUSES
class Weave:
    """The weave's series, built once per asset.  Not a dataclass — it is a
    cache of four arrays and a constructor that names what each one is."""

    __slots__ = ("m_lo", "m_hi", "m_med", "f_lo", "f_hi", "width")

    def __init__(self, c: np.ndarray):
        self.m_lo, self.m_hi = ribbon_band(c, "M")
        self.f_lo, self.f_hi = ribbon_band(c, "FAST")
        # THE M-MEDIAN IS THE FAMILY'S MIDDLE MEMBER, EMA 89 — not the midpoint
        # of the band. A band midpoint is (min+max)/2 of three EMAs and moves
        # with the OUTER two; the median is the middle EMA and is the line the
        # commission's "M-median" names.
        self.m_med = ind.ema(c, RIBBONS["M"][1])
        self.width = self.m_hi - self.m_lo
        # THE WARM-UP FLOOR. `ind.ema` seeds at the series start and never
        # returns NaN. This estate has repaired that defect THREE times; the
        # fourth is prevented here. Every M and FAST series is NULL until the
        # family's LONGEST member has seen its own length, because a band is not
        # defined while only some of its members are warm.
        n = len(c)
        idx = np.arange(n)
        for arr, fam in ((self.m_lo, "M"), (self.m_hi, "M"),
                         (self.f_lo, "FAST"), (self.f_hi, "FAST")):
            arr[idx < max(RIBBONS[fam])] = np.nan
        self.m_med = np.where(idx >= RIBBONS["M"][1], self.m_med, np.nan)
        self.width = self.m_hi - self.m_lo


def weave_fires(w: Weave, j: int, direction: int, k: int = WEAVE_K) -> bool:
    """D-R3, CLOSE-CONFIRMED, TWO CLAUSES AND NOT A THIRD.

    (i)  the M-ribbon WIDTH is contracting over its k-window — `width[j] <
         width[j-k]` — AND the M-median's slope is against the trade,
         `(m_med[j] - m_med[j-1]) * direction <= 0`;
    (ii) the fast ribbon has closed back inside-or-beyond the M band against
         the trade: for a long `f_lo[j] <= m_hi[j]`, for a short
         `f_hi[j] >= m_lo[j]`.

    BOTH clauses, on the same bar, on CLOSES.  The commission says "two clauses
    only" and that is enforced by there being two `and`ed tests here and no
    others — a third condition, however sensible, would make the registered
    rule a different rule from the one whose text was written down first.

    WHAT WOULD MAKE THIS WRONG: reading the slope direction-agnostically (it
    would exit winning shorts — see the module docstring); testing containment
    rather than the inequality; evaluating on an unwarm bar; or comparing
    `width[j]` against `width[j-1]` instead of the k-window, which would make
    "contracting" mean "one bar narrower".
    """
    if j - k < 0 or j - 1 < 0:
        return False
    vals = (w.width[j], w.width[j - k], w.m_med[j], w.m_med[j - 1],
            w.f_lo[j], w.f_hi[j], w.m_lo[j], w.m_hi[j])
    if not all(np.isfinite(v) for v in vals):
        return False
    contracting = bool(w.width[j] < w.width[j - k])
    slope_against = bool((w.m_med[j] - w.m_med[j - 1]) * direction <= 0.0)
    clause_i = contracting and slope_against
    if not clause_i:
        return False
    if direction == 1:
        return bool(w.f_lo[j] <= w.m_hi[j])
    return bool(w.f_hi[j] >= w.m_lo[j])


# ═════════════════════════════════════════════════════════ D-R5 · THE RE-ENTRY
def reentry_close(w: Weave, j: int, direction: int, close_px: float,
                  tide_ok: bool) -> bool:
    """D-R5's trigger: the first CLOSE back beyond the fast ribbon in the TREND
    direction, with the tide still agreeing.

    "BEYOND THE FAST RIBBON" IS THE FAR EDGE, NOT THE NEAR ONE.  Re-entering a
    long asks price to have climbed back ABOVE the whole fast ribbon
    (`close > f_hi`), not merely to have touched its underside — the weave
    exited because the fast ribbon came back against the trade, so the
    symmetric re-entry is the ribbon being CLEARED again.  The caller supplies
    the CLOSE; this function does not fetch it, so the bar being tested is
    always the caller's and never one off.

    THE TIDE IS THE CALLER'S TO ESTABLISH, and it is passed in rather than
    recomputed, because the tide gate is the card's own object and re-deriving
    it here would be a second implementation of a rule that already exists.

    WHAT WOULD MAKE THIS WRONG: using the near edge; dropping the tide clause;
    allowing more than one re-entry (D-R5's cap, enforced by the caller because
    only the caller knows how many the chain has had); or firing on an unwarm
    bar, which the finiteness test below refuses.
    """
    if not tide_ok:
        return False
    edge = w.f_hi[j] if direction == 1 else w.f_lo[j]
    if not (np.isfinite(edge) and np.isfinite(close_px)):
        return False
    return bool((close_px - edge) * direction > 0.0)


def register_rows() -> list[dict]:
    return [{"key": k, "value": str(v["value"]), "ruling": v["ruling"],
             "text": v["text"], "was": v["was"]}
            for k, v in sorted(REGISTER.items())]
