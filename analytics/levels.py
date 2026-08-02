"""Level registry, clustering and scoring -- the confluence engine.

This is a mechanical implementation of the operator's oldest discretionary
instinct: several independent tools naming the same price is more interesting
than one tool naming it loudly.

WHAT A SCORE IS AND IS NOT (§1.2, non-negotiable).  A confluence score measures
AGREEMENT BETWEEN TOOLS.  It is not evidence of edge, and no output of this
module may be phrased predictively.  Whether agreement predicts anything is a
study question that lives on scorable data under G-7, not here.

AS-OF.  Every function is a pure function of the registry it is handed.  It has
no time axis and cannot police one: if the caller puts an unconfirmed pivot or a
future POC into the registry, the arithmetic will faithfully cluster the future.
Causality is established upstream, by slicing to the decision bar -- see
`structure.confirmed_pivots`.

Thresholds (0.02 / 0.15 / 1.5 ATR, family cap 3) are v1 PLACEHOLDERS to be
re-ratified against the calibration report. They are count-based with equal
weights and were never fitted, per D9 discipline.
"""

from collections import Counter, defaultdict

__all__ = ["FAMILIES", "COLLAPSE_ATR", "CLUSTER_ATR", "LIS_ATR", "FAMILY_CAP",
           "LevelRegistry", "collapse_same_family", "cluster", "score",
           "lines_in_sand", "sensitivity"]

FAMILIES = ("vwap_anchored", "vwap_rolling", "profile", "structure", "ss")

COLLAPSE_ATR = 0.02
CLUSTER_ATR = 0.15
LIS_ATR = 1.5
FAMILY_CAP = 3


class LevelRegistry:
    """An ordered pool of {family, label, level, source_layer, timeframe}."""

    def __init__(self, levels=None):
        self.levels = []
        for lv in (levels or []):
            self.add(**lv)

    def add(self, family, label, level, source_layer, timeframe=None):
        if family not in FAMILIES:
            raise ValueError(f"unknown family {family!r}; expected one of {FAMILIES}")
        if level is None or level != level:          # NaN guard
            return self
        self.levels.append({"family": family, "label": str(label),
                            "level": float(level), "source_layer": str(source_layer),
                            "timeframe": timeframe})
        return self

    def __len__(self):
        return len(self.levels)

    def by_family(self):
        out = Counter(lv["family"] for lv in self.levels)
        return {f: out.get(f, 0) for f in FAMILIES}

    def as_list(self):
        return list(self.levels)


def collapse_same_family(levels, atr, tol=COLLAPSE_ATR):
    """Rule 1 -- merge same-family levels within `tol` daily-ATR into one member.

    This is where a July M-anchor that coincides with the Q-anchor merges instead
    of double-counting: a degeneracy of the calendar, not agreement between tools.
    Merged members keep every contributing label so the collapse stays auditable.
    """
    if atr is None or atr <= 0:
        raise ValueError("collapse_same_family needs a positive daily ATR")
    width = tol * atr
    out = []
    for fam in FAMILIES:
        fam_levels = sorted([lv for lv in levels if lv["family"] == fam],
                            key=lambda d: d["level"])
        group = []
        for lv in fam_levels:
            if group and abs(lv["level"] - (sum(g["level"] for g in group) / len(group))) <= width:
                group.append(lv)
            else:
                if group:
                    out.append(_merge(group))
                group = [lv]
        if group:
            out.append(_merge(group))
    return sorted(out, key=lambda d: d["level"])


def _merge(group):
    mean = sum(g["level"] for g in group) / len(group)
    return {"family": group[0]["family"],
            "label": group[0]["label"] if len(group) == 1
                     else " + ".join(sorted({g["label"] for g in group})),
            "level": mean,
            "source_layer": group[0]["source_layer"],
            "timeframe": group[0]["timeframe"],
            "collapsed_from": [g["label"] for g in group],
            "collapsed_count": len(group)}


def cluster(members, atr, tol=CLUSTER_ATR):
    """Rule 2 -- group members within `tol` daily-ATR of the RUNNING cluster mean.

    The running mean (not the seed level) is what the rule says, and it matters:
    a chain of levels each within tolerance of its predecessor would otherwise
    smear one 'cluster' across an arbitrarily wide band.
    """
    if atr is None or atr <= 0:
        raise ValueError("cluster needs a positive daily ATR")
    width = tol * atr
    clusters = []
    for lv in sorted(members, key=lambda d: d["level"]):
        if clusters:
            cur = clusters[-1]
            mean = sum(m["level"] for m in cur) / len(cur)
            if abs(lv["level"] - mean) <= width:
                cur.append(lv)
                continue
        clusters.append([lv])

    out = []
    for i, c in enumerate(clusters):
        mean = sum(m["level"] for m in c) / len(c)
        out.append({"cluster_id": i, "mean": mean, "members": c,
                    "member_count": len(c), "score": score(c),
                    "families": sorted({m["family"] for m in c})})
    return out


def score(members):
    """Rule 3 -- sum over families of min(count, FAMILY_CAP), plus the number of
    distinct families.

    The cap is what stops one prolific tool type from manufacturing agreement
    with itself; the diversity term is what rewards genuinely independent
    confirmation. Equal weights, never fitted.
    """
    per = defaultdict(int)
    for m in members:
        per[m["family"]] += 1
    capped = sum(min(n, FAMILY_CAP) for n in per.values())
    return capped + len(per)


def lines_in_sand(clusters, price, atr, reach=LIS_ATR, fallback_score=4):
    """Rule 4 -- the highest-scoring cluster within `reach` daily-ATR on each side.

    Ties break by proximity to price.  If nothing scores inside the reach, fall
    back to the NEAREST cluster scoring at least `fallback_score`, flagged so the
    report can say the line came from the fallback rather than the primary rule.
    """
    if atr is None or atr <= 0:
        raise ValueError("lines_in_sand needs a positive daily ATR")
    span = reach * atr
    out = {}
    for side, keep in (("above", lambda c: c["mean"] > price),
                       ("below", lambda c: c["mean"] < price)):
        near = [c for c in clusters if keep(c) and abs(c["mean"] - price) <= span]
        if near:
            best = sorted(near, key=lambda c: (-c["score"], abs(c["mean"] - price)))[0]
            out[side] = dict(best, source="primary")
            continue
        far = [c for c in clusters if keep(c) and c["score"] >= fallback_score]
        if far:
            best = sorted(far, key=lambda c: abs(c["mean"] - price))[0]
            out[side] = dict(best, source="fallback")
        else:
            out[side] = None
    return out


def sensitivity(members, atr, price, tolerances=(0.10, CLUSTER_ATR, 0.20)):
    """Rule 5 -- recompute rankings at each tolerance and report instability.

    An engine that cannot announce its own fragility is a machine for producing
    false confidence, so the instability chip is a first-class output rather than
    a diagnostic someone might remember to run.
    """
    per_tol, tops = {}, {}
    for t in tolerances:
        cl = cluster(members, atr, tol=t)
        ranked = sorted(cl, key=lambda c: (-c["score"], abs(c["mean"] - price)))
        per_tol[t] = ranked
        tops[t] = [round(c["mean"], 8) for c in ranked[:3]]

    base = tops.get(CLUSTER_ATR, [])
    unstable = any(v != base for k, v in tops.items() if k != CLUSTER_ATR)
    return {"tolerances": list(tolerances),
            "top3_by_tolerance": {str(k): v for k, v in tops.items()},
            "instability_chip": bool(unstable),
            "clusters_by_tolerance": {str(k): len(v) for k, v in per_tol.items()}}
