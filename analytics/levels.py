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

__all__ = ["FAMILIES", "VOLUME_FAMILIES", "SCALE_FAMILIES", "WINDOW_ORDER",
           "COLLAPSE_ATR", "CLUSTER_ATR", "LIS_ATR", "FAMILY_CAP",
           "LevelRegistry", "collapse_same_family", "cluster", "score",
           "lines_in_sand", "sensitivity", "dual_score", "lines_differ"]

# Amendment 2 §5.1.  `profile` becomes `profile_windowed`, and rolling VWAPs are
# split from anchored ones, so that no single TOOL TYPE can dominate the
# diversity term by being prolific.
FAMILIES = ("vwap_anchored", "vwap_rolling", "profile_windowed", "structure", "ss")

# §5.4.  The two families the volume filter adds.  Every capture is scored twice,
# once with them and once without, so the operator can see daily whether volume
# evidence MOVES HIS LINES -- and so the census later inherits months of that
# exact comparison already rehearsed in display-only form.
VOLUME_FAMILIES = ("vwap_rolling", "profile_windowed")

# §4.3.  Families whose members are indexed by WINDOW SCALE, and therefore the
# only ones where two members coinciding means "two timescales agree" rather than
# "one tool fired twice".
SCALE_FAMILIES = VOLUME_FAMILIES

WINDOW_ORDER = ("prior-day", "7d", "30d", "90d", "365d")

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


def _window_key(tf):
    return (WINDOW_ORDER.index(tf) if tf in WINDOW_ORDER else len(WINDOW_ORDER),
            str(tf))


def _merge(group):
    """Collapse a same-family group into one member, badging scale confirmation.

    §4.3, RATIFIED B-10 OPTION (a).  When two WINDOWS' edges land within the
    collapse tolerance the merged level carries `scale_confirmed: [7d, 30d]` and
    displays a badge -- but it does NOT add score, and the mechanism by which it
    does not is structural rather than a special case: the two levels become ONE
    member, so the family's member count is unchanged and `score` cannot see
    them as two voices.

    On the record, because it will look like a lost opportunity later: nested
    windows SHARE DATA -- the 30-day window CONTAINS the 7-day window -- so they
    are partially dependent voices.  Partial dependence deserves fractional
    credit, and the project's law is counted-never-weighted, which forbids
    fractions.  Conservative scoring plus full visibility is the honest
    treatment of a voice we cannot weigh.

    Whether price actually reacts differently at scale-confirmed edges is H-VAN,
    routed to APOLLO.  The badge records the state; it never claims it pays.
    """
    mean = sum(g["level"] for g in group) / len(group)
    out = {"family": group[0]["family"],
           "label": group[0]["label"] if len(group) == 1
                    else " + ".join(sorted({g["label"] for g in group})),
           "level": mean,
           "source_layer": group[0]["source_layer"],
           "timeframe": group[0]["timeframe"],
           "collapsed_from": [g["label"] for g in group],
           "collapsed_count": len(group)}

    if group[0]["family"] in SCALE_FAMILIES:
        windows = {g.get("timeframe") for g in group if g.get("timeframe")}
        if len(windows) > 1:
            out["scale_confirmed"] = sorted(windows, key=_window_key)
    return out


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


def dual_score(levels, atr, price, tol=CLUSTER_ATR):
    """§5.4 -- score every capture TWICE, with and without the volume families.

    BOTH are recorded; the report's toggle switches views.  This is the filter's
    purpose made measurable: the operator sees daily whether volume evidence
    MOVES HIS LINES, and when the census later asks whether volume confluence
    changes outcomes, the live instrument will have been rehearsing that exact
    comparison, in display-only form, for months.

    The excluded set drops `vwap_rolling` and `profile_windowed` at the REGISTRY
    level, before collapse -- not after clustering.  Removing them later would
    leave clusters whose means had already been pulled by volume levels, which
    would not be the without-volume answer at all, merely a relabelled
    with-volume one.
    """
    out = {}
    for view, drop in (("with_volume", ()), ("without_volume", VOLUME_FAMILIES)):
        sel = [lv for lv in levels if lv["family"] not in drop]
        members = collapse_same_family(sel, atr) if sel else []
        clusters = cluster(members, atr, tol=tol) if members else []
        out[view] = {
            "levels_in": len(sel),
            "members": members,
            "clusters": clusters,
            "lines": lines_in_sand(clusters, price, atr) if clusters
                     else {"above": None, "below": None},
            "sensitivity": sensitivity(members, atr, price) if members else None,
            "by_family": {f: sum(1 for lv in sel if lv["family"] == f)
                          for f in FAMILIES},
            "excluded_families": list(drop),
        }
    out["differ"] = lines_differ(out["with_volume"]["lines"],
                                 out["without_volume"]["lines"], atr)
    return out


def lines_differ(lines_a, lines_b, atr):
    """How far apart the two views' lines in the sand are, per side.

    Calibration §9.2 item 6 -- 'the single most interesting number the build will
    produce'.  Distance is reported in daily-ATR as well as price so it is
    comparable across assets; `changed` is True when a side moved at all, which
    is the count the calibration report aggregates.
    """
    out = {}
    for side in ("above", "below"):
        a, b = (lines_a or {}).get(side), (lines_b or {}).get(side)
        if a is None and b is None:
            out[side] = {"changed": False, "delta": 0.0, "delta_atr": 0.0,
                         "with_volume": None, "without_volume": None}
            continue
        if a is None or b is None:
            out[side] = {"changed": True, "delta": None, "delta_atr": None,
                         "with_volume": a["mean"] if a else None,
                         "without_volume": b["mean"] if b else None,
                         "note": "a line exists in one view only"}
            continue
        d = abs(float(a["mean"]) - float(b["mean"]))
        out[side] = {"changed": d > 0.0, "delta": d,
                     "delta_atr": (d / atr) if atr else None,
                     "with_volume": float(a["mean"]),
                     "without_volume": float(b["mean"])}
    out["any_changed"] = any(out[s]["changed"] for s in ("above", "below"))
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
