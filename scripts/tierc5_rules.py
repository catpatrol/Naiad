"""TIER-C5 · FULL-WATER — THE DECISION PATH, AND NOTHING ELSE.

RATIFIED operator 2026-08-16.  THE RULING, VERBATIM AND OF RECORD:

    "open the sealed box, we lose continuity otherwise… we will put it to paper
     trade the Prometheus route… another data stream"
    "D15 caveats not hard gates"

Drafted APOLLO · Executor HEPHAESTUS · Seed 20260816.

CLASS: measurement + PRE-REGISTERED CLAIMS + PRE-NAMED SHADOW GRIDS.  Every grid
is reported WHOLE — no cell dropped, none promoted.  The estate's selection guard
is LOADED and IDLES, and the SELECTION SURFACE IS LOGGED: m per grid and m in
total, so that any future promotion out of these tables starts from a number that
was written down before the look.

────────────────────────────────────────────────────────────────────────────
THE SEAL IS OPEN.  THIS IS THE ONE THING THAT MAKES v5 A DIFFERENT ANIMAL.
────────────────────────────────────────────────────────────────────────────
Tier-C2 through Tier-C4 all ran under a CLASS line that said NO LOCKBOX READ,
and Tier-C3 discovered the hard way (F-C3-a) that the line had to be enforced on
prices, not only on timestamps.  The operator has now ruled the box OPEN, and
the reason is in the ruling itself: *we lose continuity otherwise*.  462 sealed
days sat between the census era and the live corridor, and a yardstick that
cannot cross them cannot be one yardstick.

So `sealed_mask` here returns FALSE EVERYWHERE.  It is not deleted — it is
answered, in the same shape, so that every call site that used to consult it
still does and the diff is one function rather than a scatter of removals.
`F-C5-OPEN` records the ruling verbatim and NAMES THE FIRST SEALED BAR READ:
the earliest formerly-sealed bar whose price this build actually quotes.

THE OUT-OF-SAMPLE ROLE TRANSFERS.  It does not vanish.  With the box open there
is no held-out span left in the cache, so the reserve moves FORWARD: the
Prometheus route, live paper, Stage-B interim.  Everything in this build is
therefore IN-SAMPLE BY CONSTRUCTION and is labelled so on every headline row.

────────────────────────────────────────────────────────────────────────────
THE CARD v5 = THE CARD v4, PLUS ONE ACCOUNTING RULE
────────────────────────────────────────────────────────────────────────────
4h anchor (800h pin) · rail 1.0 · tide 89/316 · d = 0.75 · 12/26 trigger ·
LPS-trail ratchet (2,2) · creek/ice 50% de-risk harvest · bell ·
**FUNDING CEILING 1R [D12]** · net of 10 bps + funding.

The funding ceiling is the only card diff, and it is an ACCOUNTING rule, not a
decision rule: it cannot move an entry, an exit, a stop or a fill.  It caps what
a campaign can be charged in funding at 1R.  With the box open the corridor now
spans 2,530 days instead of 118, and a campaign held across a funding regime can
accrue a cost unbounded in R while the price path is unchanged — the ceiling is
the operator's ruling that the book will not be scored on that.  It binds
upward only (a funding CREDIT is never capped) and every trade records whether
it bound.

────────────────────────────────────────────────────────────────────────────
BYTE-INHERITANCE IS BY IMPORT, THREE GENERATIONS DEEP
────────────────────────────────────────────────────────────────────────────
`import tierc4_rules as V4` — which binds Tier-C3's, which binds Tier-C2's.
`build_4h`, `_crosses`, `armings`, `Frame4h`, `Arming`, `build_pivots_4h`,
`struct_stop_4h`, `harvest_edge`, `harvest_touched`, `harvest_outside` are the
same objects, not copies.  What is NEW here is: the open seal, the funding
ceiling, a PARAMETERISED fractal builder (the trail lab needs (3,3) as well as
(2,2)), the SPRING lane, the CASCADE ADD, and a `Card` record that carries every
knob the shadow fleet turns.

F-C4-h CONVENTION ADOPTED: every fixture leg in this build states what would
have to be true for it to FAIL.

F-C5-6 · captured-not-consulted: this module's transitive import closure is
{numpy, dataclasses, engine.*, tierc2_rules, tierc3_rules, tierc4_rules} and
contains no `analytics` member.  The card named ONE file, `scripts/tierc5.py`;
the decision path is split out HERE precisely so that closure proof stays alive,
because the program must import `analytics` for the tape and the labs' resampling
and a single file could not be both.  The deviation is named rather than taken
quietly.
────────────────────────────────────────────────────────────────────────────
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from engine.s1 import _pivots

import tierc4_rules as V4

# ═══════════════════════════════ BYTE-INHERITED — the SAME objects, bound
Frame4h = V4.Frame4h
Arming = V4.Arming
Pivots4h = V4.Pivots4h
Stop = V4.Stop
Fractals4h = V4.Fractals4h
Advance = V4.Advance
build_4h = V4.build_4h
_crosses = V4._crosses
armings = V4.armings
build_pivots_4h = V4.build_pivots_4h
struct_stop_4h = V4.struct_stop_4h
harvest_edge = V4.harvest_edge
harvest_touched = V4.harvest_touched
harvest_outside = V4.harvest_outside
harvest_fill_px = V4.harvest_fill_px
ratchet_step = V4.ratchet_step

UNIVERSE = V4.UNIVERSE
LENS = V4.LENS
TIDE_FAST, TIDE_SLOW = V4.TIDE_FAST, V4.TIDE_SLOW
WINDOW_FAST, WINDOW_SLOW = V4.WINDOW_FAST, V4.WINDOW_SLOW
TRIGGER_FAST, TRIGGER_SLOW = V4.TRIGGER_FAST, V4.TRIGGER_SLOW
D_DISPLACEMENT, D_STRIP = V4.D_DISPLACEMENT, V4.D_STRIP
ATR_LEN = V4.ATR_LEN
FEE_BPS_SIDE = V4.FEE_BPS_SIDE
FEE_BPS_ROUND_TRIP = V4.FEE_BPS_ROUND_TRIP
PIVOT_L, PIVOT_R = V4.PIVOT_L, V4.PIVOT_R
STOP_BUF_ATR = V4.STOP_BUF_ATR
MIN_STOP_ATR = V4.MIN_STOP_ATR
PIVOT_LOOKBACK_4H = V4.PIVOT_LOOKBACK_4H
LEAD_IN_DAYS = V4.LEAD_IN_DAYS
RATCHET_PIVOT_L, RATCHET_PIVOT_R = V4.RATCHET_PIVOT_L, V4.RATCHET_PIVOT_R
RATCHET_BUF_ATR, RATCHET_RAIL_ATR = V4.RATCHET_BUF_ATR, V4.RATCHET_RAIL_ATR
RATCHET_MONOTONE = V4.RATCHET_MONOTONE
HARVEST_FRACTION = V4.HARVEST_FRACTION
HARVEST_BAND = V4.HARVEST_BAND
HARVEST_MAX_PER_CAMPAIGN = V4.HARVEST_MAX_PER_CAMPAIGN
MS_4H, MS_1H = V4.MS_4H, V4.MS_1H
MS_1D = 86_400_000

INHERITED = ("Frame4h", "Arming", "Pivots4h", "Stop", "Fractals4h", "Advance",
             "build_4h", "_crosses", "armings", "build_pivots_4h",
             "struct_stop_4h", "harvest_edge", "harvest_touched",
             "harvest_outside", "harvest_fill_px", "ratchet_step")

# The six ribbons — the estate's own, quoted by value from
# `scripts/census2b_program.py:76-84` via `tierc2_baseline.RIBBONS`.  Repeated
# here rather than imported because `tierc2_baseline` imports `analytics` and
# the decision path may not.  F-C5-INHERIT asserts the two are equal.
RIBBONS = {"FAST": (9, 12, 26), "M": (62, 89, 127), "MH": (262, 316, 423),
           "H": (616, 889, 1272), "VH": (1618, 2618, 3618),
           "UH": (4236, 4618, 5000)}
MH_OR_HEAVIER = ("MH", "H", "VH", "UH")

# ═══════════════════════════════════════════════ THE CARD DIFFS · registered
THE_RULING = (
    '"open the sealed box, we lose continuity otherwise… we will put it to '
    'paper trade the Prometheus route… another data stream"  ·  '
    '"D15 caveats not hard gates"'
)

REGISTER_DIFF: dict[str, dict] = {
    "SEAL_OPEN": {
        "value": True,
        "source": "OPERATOR RULING 2026-08-16, verbatim: " + THE_RULING +
                  ". This REVERSES the CLASS line that governed Tier-C2, C3 and "
                  "C4 ('NO lockbox read; 462 sealed days untouched') and closes "
                  "F-C3-a by ruling rather than by argument — the operator did "
                  "not ratify the seal floor, they removed the seal. Every mask "
                  "is answered False; F-C5-OPEN names the first formerly-sealed "
                  "bar this build actually quotes.",
    },
    "FUNDING_CEILING_R": {
        "value": 1.0,
        "source": "D12, enacted by the 2026-08-16 paste. An ACCOUNTING rule, "
                  "not a decision rule: it caps a campaign's funding COST at 1R "
                  "and cannot move an entry, exit, stop or fill. It binds upward "
                  "only — a funding CREDIT is never capped. Needed because the "
                  "open box takes the corridor from 118 days to ~2,530, and a "
                  "campaign carried across a funding regime accrues a cost "
                  "unbounded in R on an unchanged price path.",
    },
    "SPRING_LOOKBACK_BARS": {
        "value": 96,
        "source": "P-SPR-1 registration text (operator paste 2026-08-16): "
                  "'sweep of prior 96×4h-bar extreme'. GENUINELY NEW. 96 4h bars "
                  "= 16 days.",
    },
    "SPRING_RECLAIM_BARS": {
        "value": 3,
        "source": "P-SPR-1: 'closing back inside ≤3 bars'. GENUINELY NEW. The "
                  "sweep bar itself counts as bar 0, so the reclaim may land on "
                  "the sweep bar or on either of the next three.",
    },
    "ADDS_MAX": {
        "value": 2,
        "source": "P-CASC-1: '≤2 adds/campaign'. GENUINELY NEW.",
    },
    "ADD_BAND_SET": {
        "value": MH_OR_HEAVIER,
        "source": "P-CASC-1: 'retrace into MH-or-heavier band'. RE-POINTED "
                  "INHERITANCE of the estate's six-ribbon map "
                  "(census2b_program.py:76-84 via tierc2_baseline.RIBBONS): MH "
                  "is (262,316,423) and 'heavier' is H, VH, UH. No new EMA is "
                  "defined anywhere in this build's decision path.",
    },
    "ADD_TRIGGER_RIBBON": {
        "value": "FAST",
        "source": "P-CASC-1: 'THEN close back beyond the fast ribbon'. "
                  "RE-POINTED INHERITANCE — FAST is (9,12,26) in the same map.",
    },
    "WARMUP_BARS": {
        "value": V4.TIDE_SLOW,
        "source": "RE-POINTED INHERITANCE of TIDE_SLOW (= 316). NEW TO v5 AND "
                  "NEEDED ONLY BECAUSE OF v5. Every parent corridor began "
                  "hundreds of bars after its data did, so the slow EMAs were "
                  "warm by traversal and nobody had to say so. The full-water "
                  "corridor starts at each asset's FIRST BAR, and "
                  "`engine.indicators.ema` SEEDS at the series start rather "
                  "than returning NaN — so at bar 1 e12 = e26 = e89 = e316 and "
                  "the tide and window gates are evaluable, and wrong. No "
                  "arming is admitted before bar 316. Counted and disclosed; "
                  "found by the post-build adversarial review.",
    },
    "PROVISIONAL_MIN_N": {
        "value": 30,
        "source": "D15 diagnostic, PINNED BEFORE THE LOOK. A slice with fewer "
                  "than 30 scored campaigns carries PROVISIONAL on its face. 30 "
                  "is a convention, not a test, and is named as one — the estate "
                  "prints no confidence interval on these books by standing "
                  "practice (Tier-C3 §3: 'a bootstrap CI on eleven campaigns "
                  "would dress an anecdote as a measurement').",
    },
}

REGISTER: dict[str, dict] = {**V4.REGISTER, **REGISTER_DIFF}

SEAL_OPEN: bool = REGISTER["SEAL_OPEN"]["value"]
FUNDING_CEILING_R: float = REGISTER["FUNDING_CEILING_R"]["value"]
SPRING_LOOKBACK_BARS: int = REGISTER["SPRING_LOOKBACK_BARS"]["value"]
SPRING_RECLAIM_BARS: int = REGISTER["SPRING_RECLAIM_BARS"]["value"]
ADDS_MAX: int = REGISTER["ADDS_MAX"]["value"]
ADD_BAND_SET: tuple = REGISTER["ADD_BAND_SET"]["value"]
ADD_TRIGGER_RIBBON: str = REGISTER["ADD_TRIGGER_RIBBON"]["value"]
PROVISIONAL_MIN_N: int = REGISTER["PROVISIONAL_MIN_N"]["value"]
WARMUP_BARS: int = REGISTER["WARMUP_BARS"]["value"]

assert ADD_BAND_SET == MH_OR_HEAVIER and all(b in RIBBONS for b in ADD_BAND_SET)
assert ADD_TRIGGER_RIBBON in RIBBONS

RULE_CARD_V5 = """\
SEAL ["seal"] [OPERATOR 2026-08-16]: THE BOX IS OPEN. No lockbox mask anywhere.
  The corridor is panel start -> latest CLOSED 4h bar, one unbroken window.
  OUT-OF-SAMPLE TRANSFERS FORWARD to live paper (Prometheus route, Stage-B
  interim). EVERYTHING HERE IS IN-SAMPLE BY CONSTRUCTION and says so.
UNIVERSE ["universe"]: {BTC,ETH,SOL,NEAR,ZEC}USDT · LENS ["lens"]: 4h only
TIDE: long iff e89>e316 AND close>e316 on 4h (mirror short)
WINDOW: 4h 12/89 cross in direction, no counter yet; displacement |close-e89|/ATR
  at the cross >= d=0.75 ["d"]
TRIGGER: first in-window 4h 12/26 cross -> enter at that bar close
STOP [F-3]: anchor beyond the nearest real 4h (5,5) swing pivot within 200 bars
  (the 800h pin), offset 0.5 x ATR beyond it; RAIL max(pivot, 1.0 x ATR at entry)
STOP EXECUTION [F-4]: adverse-first. A bar touching the stop exits AT the stop.
RATCHET ["ratchet"]: LPS-trail on confirmed (2,2) fractals, beyond 0.5 x ATR,
  railed 1.0 x ATR from the confirming close, monotone, governs the NEXT bar
HARVEST ["harvest"]: 50% off at the FIRST armed touch of the opposing 89/316
  band, filled at that bar's close, once per campaign; "from below" is a
  precondition
BELL: counter 4h 12/89 OR 4h 89/316 against -> exit at close
ACCOUNTING: net of 10 bps round trip + journaled funding; R = ENTRY stop
  distance; the halves book their own R; one unit, one position per asset;
  FUNDING CEILING 1R [D12] — a campaign's funding COST is capped at 1R, credits
  are never capped, and the cap can move no price
LEAD-IN [D13(c)]: lead-in armings are COUNTED, never SCORED. Both books printed."""


# ═══════════════════════════════════════════════════════ THE SEAL, ANSWERED
def sealed_mask(open_ms: np.ndarray) -> np.ndarray:
    """FALSE EVERYWHERE — the box is open.

    Deliberately the same SHAPE as `tierc3_baseline.sealed_mask`, and
    deliberately not deleted.  Every call site that used to consult a mask still
    consults one; the ruling is a single function, not a scatter of removals,
    so "the seal is open" is one auditable object rather than an argument about
    what was taken out.

    WHAT WOULD MAKE THIS WRONG: if it returned True anywhere.  F-C5-OPEN asserts
    `not sealed_mask(...).any()` over every panel asset's full history AND names
    the first formerly-sealed bar whose price the build quotes — a mask that
    silently kept masking would show up as zero such bars.
    """
    return np.zeros(len(open_ms), dtype=bool)


LOCKBOX_WAS = ("2024-07-01", "2025-10-05")     # what the seal used to cover


# ══════════════════════════════════════════════ THE CARD, AND EVERY KNOB
@dataclass(frozen=True)
class Card:
    """One row of the fleet.  The DEFAULTS ARE THE RATIFIED v5 CARD.

    Every shadow cell is this record with one field changed, ridden through the
    one code path — so a cell can differ from the card in exactly the way its
    name says and in no other way.  `name` is the cell's label in every table.
    """
    name: str = "v5"
    grid: str = "card"                  # which pre-named grid this cell belongs to
    # ── entry ────────────────────────────────────────────────────────────
    entry_rail_atr: float = MIN_STOP_ATR            # S-RAIL {1.25, 1.5}
    lane: str = "card"                              # card | spring | union
    limit_ae_mult: float | None = None              # S-LIMIT {0.5..2.0} x avg AE
    # ── the trail ────────────────────────────────────────────────────────
    trail: bool = True
    trail_l: int = RATCHET_PIVOT_L                  # S-TRAIL {(3,3)}
    trail_r: int = RATCHET_PIVOT_R
    trail_extra_buf_atr: float = 0.0                # S-TRAIL {+0.25 ATR}
    trail_arm_after_r: float = 0.0                  # S-TRAIL {+1R}
    # ── the harvest ──────────────────────────────────────────────────────
    harvest: str = "band"                           # band | fixed_r | off
    harvest_fixed_r: float = 2.0                    # S-HARV {fixed +2R}
    # -inf, NOT 0.0: the card imposes NO minimum, and a 0.0 default would
    # silently add an in-profit condition the card never carried — which is
    # exactly the drift F-C5-CTRL caught on its first run.
    harvest_min_unit_r: float = float("-inf")       # S-HARV {in-profit-only 1R}
    # ── the clock and the toll ───────────────────────────────────────────
    time_stop_bars: int | None = None               # S-CLOCK {60}
    funding_ceiling_r: float | None = FUNDING_CEILING_R   # S-CLOCK {None}
    # ── adds ─────────────────────────────────────────────────────────────
    adds_max: int = 0                               # P-CASC-1 -> ADDS_MAX
    add_size: float = 1.0                           # S-ADDSIZE {1,1.5,2,3}
    # ── the seal ─────────────────────────────────────────────────────────
    seal_open: bool = True                          # F-C5-CTRL rides False

    def diff_from_v5(self) -> str:
        """What this cell changes, in words, for the table's own face."""
        base = Card()
        out = []
        for f_ in ("entry_rail_atr", "lane", "limit_ae_mult", "trail",
                   "trail_l", "trail_r", "trail_extra_buf_atr",
                   "trail_arm_after_r", "harvest", "harvest_fixed_r",
                   "harvest_min_unit_r", "time_stop_bars",
                   "funding_ceiling_r", "adds_max", "add_size", "seal_open"):
            a, b = getattr(base, f_), getattr(self, f_)
            if a != b:
                out.append(f"{f_}={b}")
        return " · ".join(out) or "(the ratified card)"


V5 = Card()


# ══════════════════════════════════════ THE TRAIL — parameterised for the lab
def build_fractals(h4_high, h4_low, L: int, R: int) -> Fractals4h:
    """Confirmed strict (L,R) fractals keyed by CONFIRMATION bar.

    Tier-C4's `build_fractals_4h` with (L, R) opened up, because the S-TRAIL lab
    is commissioned to ride (3,3) as well as the card's (2,2).  When called with
    the card's shape it must return the card's object — `F-C5-INHERIT` asserts
    the two agree bar for bar, and that is the leg that would FAIL if this
    generalisation had drifted from its parent.
    """
    lc, lv = _pivots(np.asarray(h4_low, float), L, R, low=True)
    hc, hv = _pivots(np.asarray(h4_high, float), L, R, low=False)
    return Fractals4h(
        low_by_conf={int(c): (float(v), int(c) - R) for c, v in zip(lc, lv)},
        high_by_conf={int(c): (float(v), int(c) - R) for c, v in zip(hc, hv)},
        n_low=int(len(lc)), n_high=int(len(hc)))


def trail_step(fr: Fractals4h, j: int, direction: int, cur_stop: float,
               close: float, atr: float, open_ms: np.ndarray,
               buf_atr: float, rail_atr: float,
               forbidden: np.ndarray | None = None) -> Advance | None:
    """Tier-C4's `ratchet_step` with the lab's extra buffer folded into the
    card's own 'beyond'.  With `buf_atr = RATCHET_BUF_ATR` it IS the card.

    `forbidden` IS THREADED, NOT DROPPED.  Tier-C4 masked TWO published prices —
    the entry anchor and the ratchet pivot — and its manifest recorded
    `seal_floor_on_ratchet_pivot = True`.  The first draft of this module
    hardcoded `forbidden=None` here, which meant `seal_open=False` could only
    put HALF the mask back and the module's own claim that "every call site that
    used to consult it still does" was false.  Found by the post-build
    adversarial review.  The box being open makes the argument None in every
    shipped cell; it does not make the argument unnecessary.
    """
    return ratchet_step(fr, j, direction, cur_stop, close, atr, open_ms,
                        forbidden=forbidden, buf_atr=buf_atr, rail_atr=rail_atr,
                        monotone=RATCHET_MONOTONE)


# ══════════════════════════════════════════════════ THE SPRING LANE · P-SPR-1
@dataclass
class Spring:
    """One spring signal: the sweep, the reclaim, and the extreme that anchors
    the stop.  Kept as a record so the journal can publish the provenance of a
    price that gets paid out, exactly as the entry anchor does."""
    direction: int
    sweep_i: int                 # the bar that took out the prior extreme
    sweep_ms: int
    sweep_extreme: float         # the low (long) / high (short) it printed
    # `swept_level`, NOT `prior_extreme`: `prior_extreme` is a TAPE
    # column-family name and F-C5-6's captured-not-consulted proof is a
    # substring scan of the decision path for tape column names. A field
    # that merely SHARES a name with a registry column fails that scan,
    # correctly, because the scan cannot know which one you meant. Caught
    # by the fixture, not by eye — the same way Tier-C4 caught `dist_atr`.
    swept_level: float           # the 96-bar level it swept
    reclaim_i: int               # the bar that closed back inside
    reclaim_ms: int
    bars_to_reclaim: int


def spring_signals(f: Frame4h, lo_i: int, hi_i: int,
                   lookback: int = SPRING_LOOKBACK_BARS,
                   reclaim_bars: int = SPRING_RECLAIM_BARS) -> list[Spring]:
    """THE SPRING LANE, as registered.

        a bar SWEEPS the prior `lookback`-bar extreme (its low prints below the
        prior 96-bar minimum low, mirrored for a short), price CLOSES BACK
        INSIDE that level within `reclaim_bars` bars, and the TIDE at the
        reclaim bar agrees with the direction.  Entry is the reclaim close.

    CAUSALITY.  The prior extreme is computed over the `lookback` bars STRICTLY
    BEFORE the sweep bar, so the sweep bar cannot be its own reference.  The
    reclaim is a CLOSE, known at the reclaim bar's close, and entry is that same
    close — the instant the card names.  A signal is emitted at most once per
    sweep, and a sweep that reclaims on its own bar is `bars_to_reclaim = 0`.

    WHAT WOULD MAKE THIS WRONG: an extreme computed inclusive of the sweep bar
    (the sweep could then never take it out), a reclaim tested on a high/low
    rather than a close, or a signal whose reclaim precedes its sweep.
    F-C5-SPRING re-derives all three from raw bars on hand-picked signals.
    """
    n = len(f.c)
    hi_i = min(hi_i, n - 1)
    out: list[Spring] = []
    rejected: list[tuple[int, int]] = []   # sweeps whose first reclaim's tide disagreed
    lows, highs, closes = f.l, f.h, f.c
    for i in range(max(lo_i, lookback), hi_i + 1):
        prior_lo = float(np.min(lows[i - lookback:i]))
        prior_hi = float(np.max(highs[i - lookback:i]))
        for direction in (1, -1):
            swept = (lows[i] < prior_lo) if direction == 1 else (highs[i] > prior_hi)
            if not swept:
                continue
            level = prior_lo if direction == 1 else prior_hi
            ext = float(lows[i]) if direction == 1 else float(highs[i])
            for k in range(0, reclaim_bars + 1):
                j = i + k
                if j > hi_i:
                    break
                inside = (closes[j] > level) if direction == 1 else (closes[j] < level)
                if not inside:
                    ext = (min(ext, float(lows[j])) if direction == 1
                           else max(ext, float(highs[j])))
                    continue
                # THE RECLAIM BAR'S OWN EXTREME IS PART OF THE LEG.
                # The stop goes "beyond the sweep extreme", and the sweep leg
                # ends at the bar the position is opened on — so that bar's own
                # adverse extreme belongs in the anchor. Leaving it out put the
                # stop INSIDE a price the entry bar had already traded on 8 of
                # 246 campaigns. Found by the post-build adversarial review.
                ext = (min(ext, float(lows[j])) if direction == 1
                       else max(ext, float(highs[j])))
                tide = ((f.e89[j] > f.e316[j] and closes[j] > f.e316[j])
                        if direction == 1 else
                        (f.e89[j] < f.e316[j] and closes[j] < f.e316[j]))
                if not tide:
                    # A NAMED READING, AND IT IS COUNTED. "closing back inside
                    # <=3 bars, tide-aligned" is read as: THE reclaim is the
                    # FIRST close back inside, and the tide must agree AT IT.
                    # The alternative — keep looking through the window for a
                    # later inside close whose tide does agree — is a different
                    # lane and is NOT taken. The refusals are counted so the
                    # reading costs a number the operator can rule on rather
                    # than a silence (finding F-C5-m).
                    rejected.append((i, direction))
                    break
                out.append(Spring(
                    direction=direction, sweep_i=i, sweep_ms=int(f.open_ms[i]),
                    sweep_extreme=ext, swept_level=level,
                    reclaim_i=j, reclaim_ms=int(f.open_ms[j]),
                    bars_to_reclaim=k))
                break
    out.sort(key=lambda s: (s.reclaim_ms, -s.direction))
    spring_signals.last_tide_rejected = len(rejected)     # type: ignore[attr-defined]
    return out


spring_signals.last_tide_rejected = 0                      # type: ignore[attr-defined]


def spring_stop(sp: Spring, entry_px: float, atr_sig: float,
                rail_atr: float = MIN_STOP_ATR) -> Stop | None:
    """Stop BEYOND THE SWEEP EXTREME, railed — the card's own geometry applied
    to the spring's own anchor.  `STOP_BUF_ATR` is the card's word for 'beyond'
    and is re-pointed here rather than re-chosen."""
    if not (np.isfinite(atr_sig) and atr_sig > 0):
        return None
    if sp.direction == 1:
        pivot_stop = sp.sweep_extreme - STOP_BUF_ATR * atr_sig
        rail = entry_px - rail_atr * atr_sig
        stop_px = min(pivot_stop, rail)
    else:
        pivot_stop = sp.sweep_extreme + STOP_BUF_ATR * atr_sig
        rail = entry_px + rail_atr * atr_sig
        stop_px = max(pivot_stop, rail)
    pivot_dist = abs(entry_px - pivot_stop)
    rail_dist = rail_atr * atr_sig
    return Stop(stop_px=float(stop_px), anchor=float(sp.sweep_extreme),
                anchor_bar=int(sp.sweep_i), pivot_stop_px=float(pivot_stop),
                pivot_dist=float(pivot_dist), rail_dist=float(rail_dist),
                r_dist=float(abs(entry_px - stop_px)),
                rail_binding=bool(rail_dist > pivot_dist), n_eligible=1)


# ═══════════════════════════════════════════════ THE CASCADE ADD · P-CASC-1
def ribbon_band(c: np.ndarray, name: str) -> tuple[np.ndarray, np.ndarray]:
    """[min, max] of a ribbon's three EMAs on the 4h close — the estate's own
    band shape (`tierc2_baseline._ribbon_bands`), computed with the ENGINE's
    ema here because this one is a DECISION and the decision path rides the
    engine's Pine-parity recipe, not the analytics one."""
    from engine import indicators as ind
    a, b, d = RIBBONS[name]
    e = np.vstack([ind.ema(c, a), ind.ema(c, b), ind.ema(c, d)])
    return np.nanmin(e, axis=0), np.nanmax(e, axis=0)


def add_context(f: Frame4h) -> dict:
    """Everything the add rule reads, precomputed once per asset.

    `heavy_lo/hi` is the union band of MH-or-heavier: a retrace is INTO it when
    the bar's adverse extreme enters [min over the set, max over the set].
    `fast_lo/hi` is the FAST ribbon the reclaim must close BEYOND.
    """
    lo_stack, hi_stack = [], []
    for nm in ADD_BAND_SET:
        a, b = ribbon_band(f.c, nm)
        lo_stack.append(a)
        hi_stack.append(b)
    fast_lo, fast_hi = ribbon_band(f.c, ADD_TRIGGER_RIBBON)
    return {"heavy_lo": np.nanmin(np.vstack(lo_stack), axis=0),
            "heavy_hi": np.nanmax(np.vstack(hi_stack), axis=0),
            "fast_lo": fast_lo, "fast_hi": fast_hi}


def add_retraced(ctx: dict, j: int, direction: int, high_j: float,
                 low_j: float) -> bool:
    """Did bar j retrace INTO the MH-or-heavier band?  For a long that means the
    bar's LOW reached the band's upper edge from above; mirrored for a short."""
    lo, hi = float(ctx["heavy_lo"][j]), float(ctx["heavy_hi"][j])
    if not (np.isfinite(lo) and np.isfinite(hi)):
        return False
    return bool(low_j <= hi) if direction == 1 else bool(high_j >= lo)


def add_reclaimed(ctx: dict, j: int, direction: int, close_j: float) -> bool:
    """Did bar j CLOSE back beyond the FAST ribbon in the campaign's direction?"""
    lo, hi = float(ctx["fast_lo"][j]), float(ctx["fast_hi"][j])
    if not (np.isfinite(lo) and np.isfinite(hi)):
        return False
    return bool(close_j > hi) if direction == 1 else bool(close_j < lo)


@dataclass
class Add:
    """One add tranche — entered at a close, exiting with the campaign."""
    i: int
    ms: int
    px: float
    size: float
    retrace_i: int
    retrace_ms: int


# ═══════════════════════════════════════════════════════════════ the record
@dataclass
class Trade:
    """Tier-C4's Trade, plus what the open box, the ceiling, the lanes and the
    adds make meaningful.  A campaign that is COUNTED but not SCORED [D13(c)]
    carries no outcome at all."""
    symbol: str
    lane: str
    direction: int
    arm_i: int
    arm_ms: int
    entry_i: int
    entry_ms: int
    entry_px: float
    stop_px: float
    r_dist: float
    anchor: float
    anchor_bar_ms: int
    anchor_was_sealed: bool          # under the OLD lockbox — a disclosure, not a gate
    atr_at_entry: float
    disp_at_arming: float
    exit_i: int
    exit_ms: int
    exit_px: float
    exit_reason: str
    bars_held: int
    scored: bool
    # ── the trail ────────────────────────────────────────────────────────
    advances: list = field(default_factory=list)
    final_stop_px: float = float("nan")
    stop_advanced_atr: float = float("nan")
    ratchet_exit: bool = False
    # ── the harvest ──────────────────────────────────────────────────────
    harvested: bool = False
    harvest_i: int | None = None
    harvest_ms: int | None = None
    harvest_px: float | None = None
    harvest_unit_move_r: float | None = None
    harvest_blocked_by: str = ""
    harvest_ride_would_have_r: float | None = None   # THE HARVEST-LAB column
    # ── adds ─────────────────────────────────────────────────────────────
    adds: list = field(default_factory=list)
    add_r: float | None = None
    # ── the spring ───────────────────────────────────────────────────────
    spring: Spring | None = None
    # ── limit entry (S-LIMIT) ────────────────────────────────────────────
    limit_px: float | None = None
    limit_filled: bool = True
    limit_fill_i: int | None = None
    # ── the ride ─────────────────────────────────────────────────────────
    mfe_r: float = float("nan")
    mae_to_1r_r: float | None = None                 # THE AE STUDY column
    reached_1r: bool = False
    # ── outcome ──────────────────────────────────────────────────────────
    gross_r: float | None = None
    fee_r: float | None = None
    funding_r: float | None = None
    funding_r_uncapped: float | None = None
    funding_ceiling_bound: bool = False
    net_r: float | None = None
    net_r_harvest_half: float | None = None
    net_r_runner_half: float | None = None
    net_r_bellonly: float | None = None
