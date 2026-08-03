"""Value-area nesting across window SCALES (Amendment 2 §4).

The operator's request, precisely: extend each value area, see where it
superimposes with the one immediately after; where they do not overlap, watch
price reaction at the VA edges.

This is the classic market-profile value comparison -- normally run across
consecutive DAYS -- applied instead across WINDOW SCALES.  It asks a sharper
question: does this week's business sit inside this month's, or has value
migrated?

WHY THE SHORTER WINDOW IS THE DENOMINATOR.  `overlap_frac` divides by the
SHORTER value area, so it reads as "how much of short-term value has long-term
backing".  Dividing by the union or by the longer VA would answer a different
and much less useful question, and would make a tiny short VA nested inside a
huge long VA look like weak agreement rather than total agreement.

NO SCORE IS COMPUTED HERE.  §4.3 rules that coincident edges MERGE and carry a
badge but do NOT add score, because nested windows share data -- the 30-day
window CONTAINS the 7-day window -- so they are partially dependent voices, and
the project's law is counted-never-weighted.  That merge belongs to the
confluence engine; this module only reports geometry.

Whether price reacts differently at scale-confirmed edges is H-VAN, routed to
APOLLO.  The brief records the states daily; only the census may say whether
they pay.
"""

import numpy as np

__all__ = ["ADJACENT_PAIRS", "STATES", "va_nesting", "price_location",
           "nesting_levels", "describe_nesting"]

# The pairs §4.1 names.  Adjacent scales only: comparing 7d to 365d directly
# would answer a question no one asked and would double-count the intermediate
# windows the confluence engine already sees.
ADJACENT_PAIRS = (("7d", "30d"), ("30d", "90d"), ("90d", "365d"))

STATES = ("nested_inside", "nested_outside", "overlapping",
          "disjoint_above", "disjoint_below")


def _finite(*xs):
    return all(x is not None and np.isfinite(x) for x in xs)


def va_nesting(short_val, short_vah, long_val, long_vah):
    """Geometry of one adjacent window pair (§4.1).

    `short_*` is the shorter window's value area, `long_*` the longer one's.
    Returns state, overlap_frac, consensus_band, gap_band and the facing edges.

    Returns state=None with everything NaN when either value area is undefined
    -- a warming 365d window has no VA, and inventing one would be exactly the
    mislabelling §3.2's warm-up rule forbids.
    """
    out = {"state": None, "overlap_frac": float("nan"),
           "consensus_band": None, "gap_band": None,
           "facing_edges": None, "short_va": None, "long_va": None}
    if not _finite(short_val, short_vah, long_val, long_vah):
        return out

    a_lo, a_hi = (float(min(short_val, short_vah)), float(max(short_val, short_vah)))
    b_lo, b_hi = (float(min(long_val, long_vah)), float(max(long_val, long_vah)))
    out["short_va"] = [a_lo, a_hi]
    out["long_va"] = [b_lo, b_hi]

    lo = max(a_lo, b_lo)
    hi = min(a_hi, b_hi)
    a_width = a_hi - a_lo

    if hi < lo:
        # DISJOINT.  The gap is the unclaimed space between the two areas, and
        # its edges are the FACING edges -- the ones price meets first coming
        # from either side.  Named in §4.2's prose requirement.
        out["overlap_frac"] = 0.0
        if a_lo > b_hi:
            out["state"] = "disjoint_above"
            out["gap_band"] = [b_hi, a_lo]
            out["facing_edges"] = {"short": {"edge": "VAL", "level": a_lo},
                                   "long": {"edge": "VAH", "level": b_hi}}
        else:
            out["state"] = "disjoint_below"
            out["gap_band"] = [a_hi, b_lo]
            out["facing_edges"] = {"short": {"edge": "VAH", "level": a_hi},
                                   "long": {"edge": "VAL", "level": b_lo}}
        return out

    # They intersect.  The consensus band is ground where both timescales of
    # business agree; its edges emit as levels.
    out["consensus_band"] = [lo, hi]
    # A zero-width short VA touching the long VA is total agreement, not zero:
    # dividing by zero width would report nan for the strongest possible case.
    out["overlap_frac"] = 1.0 if a_width <= 0 else float((hi - lo) / a_width)

    if a_lo >= b_lo and a_hi <= b_hi:
        out["state"] = "nested_inside"
    elif a_lo <= b_lo and a_hi >= b_hi:
        out["state"] = "nested_outside"
    else:
        out["state"] = "overlapping"
    return out


def price_location(price, nest):
    """Where price sits relative to one pair's geometry (§4.1).

    'inside_consensus' | 'inside_short_only' | 'inside_long_only' | 'in_gap' |
    'outside_all'.  Display state, never a signal.
    """
    if nest.get("state") is None or price is None or not np.isfinite(price):
        return None
    p = float(price)
    band = nest.get("consensus_band")
    if band and band[0] <= p <= band[1]:
        return "inside_consensus"
    gap = nest.get("gap_band")
    if gap and gap[0] <= p <= gap[1]:
        return "in_gap"
    a, b = nest["short_va"], nest["long_va"]
    in_a = a[0] <= p <= a[1]
    in_b = b[0] <= p <= b[1]
    if in_a and not in_b:
        return "inside_short_only"
    if in_b and not in_a:
        return "inside_long_only"
    if in_a and in_b:
        return "inside_consensus"
    return "outside_all"


def nesting_levels(pair, nest):
    """The levels a pair emits, for the confluence registry (§5.1).

    Consensus and gap band EDGES become levels; gap edges carry facing_edge so
    the report can name them in prose.  Emits nothing when the state is
    undefined -- a warming window contributes no levels.
    """
    short_w, long_w = pair
    out = []
    if nest.get("state") is None:
        return out
    tf = f"{short_w}<->{long_w}"
    band = nest.get("consensus_band")
    if band and band[1] > band[0]:
        for edge, lv in (("consensus_low", band[0]), ("consensus_high", band[1])):
            out.append({"family": "profile_windowed", "label": f"{tf} {edge}",
                        "level": float(lv), "source_layer": "va_nesting",
                        "timeframe": tf, "facing_edge": False})
    gap = nest.get("gap_band")
    if gap:
        fe = nest.get("facing_edges") or {}
        for side in ("short", "long"):
            if side in fe:
                out.append({"family": "profile_windowed",
                            "label": f"{tf} {short_w if side == 'short' else long_w} "
                                     f"{fe[side]['edge']} (facing)",
                            "level": float(fe[side]["level"]),
                            "source_layer": "va_nesting", "timeframe": tf,
                            "facing_edge": True})
    return out


def describe_nesting(pair, nest, dp=2):
    """§4.2 PROSE REQUIREMENT -- the sentence the report must print.

    'When disjoint, the report states it in words, not only in a table.'  A
    table alone does not satisfy §4, so this is a first-class output rather
    than a formatting nicety, and it names the gap and BOTH facing edges.
    """
    short_w, long_w = pair
    st = nest.get("state")
    if st is None:
        return (f"{short_w} vs {long_w}: value-area comparison unavailable "
                f"(a window is still warming).")
    f = lambda x: f"{float(x):,.{dp}f}"

    if st in ("disjoint_above", "disjoint_below"):
        gap = nest["gap_band"]
        fe = nest["facing_edges"]
        where = "entirely above" if st == "disjoint_above" else "entirely below"
        return (f"{short_w} value sits {where} {long_w} value. "
                f"The unclaimed gap runs {f(gap[0])}-{f(gap[1])}. "
                f"The facing edges are the {short_w} {fe['short']['edge']} at "
                f"{f(fe['short']['level'])} and the {long_w} "
                f"{fe['long']['edge']} at {f(fe['long']['level'])}.")

    band = nest["consensus_band"]
    pct = f"{100.0 * nest['overlap_frac']:.0f}%"
    if st == "nested_inside":
        lead = f"{short_w} value sits entirely inside {long_w} value"
    elif st == "nested_outside":
        lead = f"{short_w} value entirely contains {long_w} value"
    else:
        lead = f"{short_w} and {long_w} value overlap in part"
    return (f"{lead} ({pct} of {short_w} value has {long_w} backing). "
            f"Both timescales agree between {f(band[0])} and {f(band[1])}.")
