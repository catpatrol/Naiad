#!/usr/bin/env python
"""F-RF-1..7 — SS12-RangeFinder v1 fixtures.  TWO LEGS PER FIXTURE, the
BREAK leg first and it must go RED, or the fixture proves nothing
[oracle_fixtures prove() law, verbatim shape].

Run: ~/venvs/naiad/bin/python scripts/rangefinder_fixtures.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import rangefinder_twin as RF                                        # noqa: E402

FAILED: list[str] = []
PASSED: list[str] = []


def check(fixture: str, ok: bool, detail: str) -> bool:
    tag = "PASS" if ok else "FAIL"
    print(f"  [{tag}] {fixture}: {detail}")
    return ok


def prove(fixture: str, title: str, break_leg, real_leg) -> None:
    """Both legs, in order. The break leg must go red or the fixture is void."""
    print(f"\n{fixture} — {title}")
    b_ok, b_detail = break_leg()
    print(f"  [BREAK] deliberate violation -> "
          f"{'RED (correct)' if not b_ok else 'GREEN (FIXTURE IS VOID)'}: "
          f"{b_detail}")
    r_ok, r_detail = real_leg()
    green = check(fixture, r_ok, r_detail)
    if b_ok:
        FAILED.append(f"{fixture} (break leg passed — fixture proves nothing)")
    elif not green:
        FAILED.append(fixture)
    else:
        PASSED.append(fixture)


D = RF.daily_bars()
M = RF.run_machine(D, RF.PINS)
LOG = json.dumps(M["events"], sort_keys=True)


# ── F-RF-1 · DETERMINISM
def rf1_break():
    d2 = D.copy()
    d2.loc[d2.index[100], "h"] = d2["h"].iloc[100] * 1.02   # one perturbed bar
    m2 = RF.run_machine(d2, RF.PINS)
    same = json.dumps(m2["events"], sort_keys=True) == LOG
    return same, ("perturbed tape produced the SAME log — the comparison "
                  "cannot see input changes" if same else
                  "one perturbed bar changed the event log — the equality "
                  "check has teeth")


def rf1_real():
    m2 = RF.run_machine(D.copy(), RF.PINS)
    same = json.dumps(m2["events"], sort_keys=True) == LOG
    return same, (f"identical input → byte-identical event log "
                  f"({len(M['events'])} events)" if same else
                  "same input produced a DIFFERENT log — nondeterminism")


# ── F-RF-2 · TARGETS (the disclosed subset)
def rf2_break():
    pins = dict(RF.PINS)
    pins["REV_MIN"] = RF.PINS["REV_MIN"] * 3          # tripled, per the queue
    m2 = RF.run_machine(D, pins)
    _, res = RF.score(m2, D)
    drift = [k for k, want in RECORD.items()
             if abs(float(res[k]["value"]) - want) > 0.05]
    ok = not drift
    return ok, (f"REV_MIN×3 still matches the KEY-A record — the record "
                f"does not bind" if ok else
                f"REV_MIN×3 drifts the record on {drift} (pivots fall to "
                f"{m2['n_pivots']}) — the calibration is load-bearing")


# THE CALIBRATION OF RECORD, AS LITERALS [review: comparing to the export
# was a self-comparison — the export is written by the same run_machine;
# these numbers are the RECORD and a regression on any of them goes red].
RECORD = {"Q1_coverage": 71.19, "Q2_pivot_per_bars": 7.78,
          "Q3_conf_per_100": 1.19, "Q4_lifetime": 68.2}


def rf2_real():
    _, res = RF.score(M, D)
    bad = []
    for k, want in RECORD.items():
        got = res[k]["value"]
        if abs(float(got) - want) > 0.05:
            bad.append(f"{k}={got} (record {want})")
    exp = json.loads((RF.OUT / "BTCUSD_1d_ranges_v1.json").read_text())
    fresh = json.dumps(res, sort_keys=True, default=str) == json.dumps(
        exp["modes"]["body"]["key_a_residuals"], sort_keys=True,
        default=str)
    ok = not bad and fresh
    return ok, ("every KEY-A residual equals the HARD-CODED v1 record "
                "(BODY mode, 420 bars: Q4 SATISFIED, Q1/Q3 near-miss, "
                "Q2 resists — filed, not forced); export fresh"
                if ok else
                f"record-drift: {bad or 'none'}; export-fresh={fresh}")


# ── F-RF-3 · LIFECYCLE LEGALITY on the event log
def _legality(events, pins) -> tuple[bool, str]:
    by_rid: dict[int, list] = {}
    for e in events:
        if "rid" in e:
            by_rid.setdefault(e["rid"], []).append(e)
    bad = []
    n_seed = n_conf = n_inval = n_sup = 0
    for rid, evs in by_rid.items():
        kinds = [e["event"] for e in evs]
        n_seed += kinds.count("seed")
        n_conf += kinds.count("confirm")
        n_inval += kinds.count("potential-invalidate")
        n_sup += kinds.count("potential-superseded")
        # every deviation has its breach + in-window return + same-bar redraw
        for k, e in enumerate(evs):
            if e["event"] == "harden":
                opens = [x for x in evs if x["event"] == "breach-open"
                         and x["i"] < e["i"]]
                if not opens:
                    bad.append(f"rid{rid}: harden without breach-open")
                    continue
                b = opens[-1]
                if e["i"] - b["i"] > pins["DEV_RETURN_BARS"]:
                    bad.append(f"rid{rid}: return outside DEV_RETURN_BARS")
                if not any(x["event"] == "redraw" and x["i"] == e["i"]
                           for x in evs):
                    bad.append(f"rid{rid}: harden without same-bar redraw")
            if e["event"] == "breakout-die":
                if e["by"] == "n_closes" and e["closes"] < pins["BREAK_CONFIRM_N"]:
                    bad.append(f"rid{rid}: die by n with {e['closes']} closes")
                if e["by"] not in ("n_closes", "margin"):
                    bad.append(f"rid{rid}: die without evidence")
                # a death needs ITS breach: the last same-rid breach-open
                # before it, same side, with no deviation/lapse between
                # [review: an evidence-free planted die passed the first
                # draft of this leg]
                opens = [x for x in evs if x["event"] == "breach-open"
                         and x["i"] <= e["i"]]
                if not opens:
                    bad.append(f"rid{rid}: die WITHOUT any breach-open")
                else:
                    b = opens[-1]
                    if b.get("side") != e.get("side"):
                        bad.append(f"rid{rid}: die side {e.get('side')} vs "
                                   f"breach side {b.get('side')}")
                    between = [x for x in evs
                               if b["i"] < x["i"] <= e["i"] and x["event"]
                               in ("harden", "breach-lapse")]   # v1 name —
                    # the v0 name left this clause INERT [review]
                    if between:
                        bad.append(f"rid{rid}: die after the breach already "
                                   f"resolved")
        n_dies = sum(1 for x in evs if x["event"] == "breakout-die")
        if n_dies > 1:
            bad.append(f"rid{rid}: {n_dies} deaths on one range")
        # no boundary edit except via redraw: every redraw pairs a HARDEN
        for x in evs:
            if x["event"] == "redraw" and not any(
                    y["event"] == "harden" and y["i"] == x["i"]
                    for y in evs):
                bad.append(f"rid{rid}: redraw WITHOUT a harden")
        # C3: every backdate points to a REAL terminal pivot (a logged
        # pivot event at that bar), and born_at is the confirm bar
        for x in evs:
            if x["event"] == "backdate":
                if not any(y["event"] == "confirm" and y["i"]
                           == x["born_at"] for y in evs):
                    bad.append(f"rid{rid}: backdate born_at is not the "
                               f"confirm bar")
                if not any(e2["event"] == "pivot"
                           and e2["i"] == x["backdated_from"]
                           for e2 in events):
                    bad.append(f"rid{rid}: backdated_from has no pivot")
        # C2: no solid deviation without its harden — every harden carries
        # breach+return evidence (checked above via deviation branch)
        # memory lines freeze at FIRST touch — at most one per side
        for side in ("top", "bottom"):
            n_t = sum(1 for x in evs if x["event"] == "memory-touch"
                      and x["side"] == side)
            if n_t > 1:
                bad.append(f"rid{rid}: {n_t} memory touches on {side}")
    # POTENTIAL is a STOCK: seeds conserve into resolutions + survivors —
    # computed FROM THE LOG so a planted log is judged too [review: the
    # identity check `events is M["events"]` silently skipped plants]
    unresolved_log = n_seed - n_conf - n_inval - n_sup
    if unresolved_log < 0:
        bad.append(f"stock leak: {n_seed} seeds < {n_conf}+{n_inval}+{n_sup}"
                   f" resolutions")
    if events is M["events"] and unresolved_log != M["n_potential_unresolved"]:
        bad.append(f"stock leak: log says {unresolved_log} unresolved, the "
                   f"machine says {M['n_potential_unresolved']}")
    m = M if events is M["events"] else None
    return (not bad,
            f"seeds {n_seed} = confirmed {n_conf} + invalidated {n_inval} + "
            f"superseded {n_sup} + unresolved "
            f"{m['n_potential_unresolved'] if m else '?'}; "
            + ("all lifecycle laws hold on "
               f"{len(events)} events" if not bad else "; ".join(bad[:4])))


def rf3_break():
    ev = [dict(e) for e in M["events"]]
    ev.append({"i": 150, "ts": "x", "event": "redraw", "rid": 5,
               "side": "top", "frm": 1.0, "to": 2.0})   # solid w/o harden
    ev.append({"i": 60, "ts": "x", "event": "breakout-die", "rid": 2,
               "side": "top", "by": "margin", "closes": 1,
               "px": 1.0})                    # planted die WITHOUT a breach
    ok, det = _legality(ev, RF.PINS)
    return ok, ("planted solid-without-harden AND die-without-breach "
                "PASSED legality" if ok else
                "both plants caught: " + det)


def rf3_real():
    ok, det = _legality(M["events"], RF.PINS)
    # THE LAPSE PATH, EXERCISED [review: at the shipped pins a lapse is
    # UNREACHABLE — BREAK_CONFIRM_N(8) <= DEV_RETURN_BARS(7)+1 closes the
    # [devRet+1, brkN-1] window — so the LATE-RETURN law would ship as
    # dead code with no leg touching it].  Run the machine at a lapse-open
    # configuration and demand the law behaves: a lapse occurs, the range
    # SURVIVES it, and no redraw rides the lapse bar.
    m2 = RF.run_machine(D, dict(RF.PINS, DEV_RETURN_BARS=2,
                                BREAK_CONFIRM_N=20, BREAK_MARGIN=6.0))
    lapses = [e for e in m2["events"] if e["event"] == "breach-lapse"]
    bad2 = []
    if not lapses:
        bad2.append("no lapse even at DEV=2/N=20/M=6 — the law is dead")
    for e in lapses:
        if any(x["event"] == "redraw" and x.get("rid") == e["rid"]
               and x["i"] == e["i"] for x in m2["events"]):
            bad2.append(f"rid{e['rid']}: redraw rides the lapse bar")
        r = next(x for x in m2["ranges"] if x.rid == e["rid"])
        if 0 <= r.die_i <= e["i"]:
            bad2.append(f"rid{e['rid']}: dead before its lapse")
    ok2 = not bad2
    det += (f"; LAPSE PATH: {len(lapses)} lapse(s) at DEV=2/N=20/M=6, "
            f"range survives, no redraw — the LATE-RETURN law is alive "
            f"off-defaults (unreachable AT the shipped pins, disclosed)"
            if ok2 else f"; LAPSE PATH: {bad2}")
    return ok and ok2, det


# ── F-RF-4 · SPRING KINSHIP (the census tie)
def _springs_independent(d, look=20):
    """The house spring shape, computed HERE from raw bars and nothing
    else: a bar sweeping BELOW the prior `look`-bar low extreme and body-
    closing back above it."""
    l, c = d["l"].to_numpy(float), d["c"].to_numpy(float)
    out = set()
    for i in range(look, len(d)):
        prior = float(np.min(l[i - look:i]))
        if l[i] < prior and c[i] > prior:
            out.add(i)
    return out


def _kinship(rule_flip=False):
    """THE LAW (asserted): every bottom harden sweeps below the BOUNDARY it
    breached and body-closes back above it — the spring SHAPE against the
    prior extreme the range itself defines, recomputed from raw bars + the
    logged boundary.  THE STATISTIC (reported, both directions): overlap
    with the 20-bar-extreme house spring scan.  Under v0's wick grammar the
    two coincide (1/1); under C1's BODY grammar they SPLIT — the body
    boundary sits above the wick territory, so a deviation need not sweep
    a 20-bar wick extreme.  The split is REPORTED as the red-flag clause
    demands; it is a C1 finding, not a tuning knob."""
    springs = _springs_independent(D)
    c = D["c"].to_numpy(float)
    l = D["l"].to_numpy(float)
    dev_bot, law_ok, spring20 = [], 0, 0
    for e in M["events"]:
        if e["event"] == "harden" and e["side"] == "bottom":
            opens = [x for x in M["events"] if x["event"] == "breach-open"
                     and x["rid"] == e["rid"] and x["i"] <= e["i"]]
            b = opens[-1]["i"]
            boundary = float(opens[-1]["boundary"])
            dev_bot.append((b, e["i"]))
            swept = bool(np.min(l[b:e["i"] + 1]) < boundary)
            ret = ((c[e["i"]] > boundary) if not rule_flip
                   else (c[e["i"]] < boundary))
            if swept and ret:
                law_ok += 1
            prior = float(np.min(l[max(0, b - 20):b]))
            if (np.min(l[b:e["i"] + 1]) < prior
                    and c[e["i"]] > prior):
                spring20 += 1
    n_spring_in_dev = sum(1 for s in springs
                          if any(b <= s <= j for b, j in dev_bot))
    ok = law_ok == len(dev_bot) and len(dev_bot) > 0
    return ok, law_ok, spring20, len(dev_bot), len(springs), n_spring_in_dev


def rf4_break():
    ok, law, s20, n, s, sid = _kinship(rule_flip=True)
    return ok, (f"corrupted reclaim rule still matches {law}/{n}"
                if ok else
                f"corrupted reclaim rule matches {law}/{n} — the shape "
                f"test reads the close for real")


def rf4_real():
    ok, law, s20, n, s, sid = _kinship()
    return ok, (f"INVARIANT (definitional — the sweep is entailed by the "
                f"breach; the RECLAIM close is the content): {law}/{n} "
                f"bottom hardens reclaim their breached boundary. "
                f"STATISTIC both directions: "
                f"{s20}/{n} also sweep the 20-bar wick extreme (the house "
                f"spring scan); {sid}/{s} independent springs fall inside "
                f"a deviation episode. The {n - s20} body-only breaches "
                f"are the C1 SPLIT — reported as the red flag clause "
                f"demands, a finding not a knob." if n else
                "no bottom deviations to test")


# ── F-RF-5 · PINE/TWIN PARITY
PINE = (ROOT / "pine" / "SS12_RangeFinder_v1.pine").read_text()
PIN_MAP = {"LEG_MIN": "legMin", "REV_MIN": "revMin", "TOUCH_EPS": "touchEps",
           "DEV_RETURN_BARS": "devRet", "BREAK_CONFIRM_N": "brkN",
           "BREAK_MARGIN": "brkMargin"}


def _pine_mode_default(text):
    m = re.search(r'boundaryMode\s*=\s*input\.string\(\s*"(\w+)"', text)
    return m.group(1) if m else None


def _pine_defaults(text):
    out = {}
    for pin, var in PIN_MAP.items():
        m = re.search(rf"^{var}\s*=\s*input\.(?:float|int)\(\s*([0-9.]+)",
                      text, re.M)
        if m:
            out[pin] = float(m.group(1))
    return out


def rf5_break():
    fake = PINE.replace("input.float(1.75, \"REV_MIN", "input.float(2.5, \"REV_MIN")
    got = _pine_defaults(fake)
    ok = all(abs(got.get(k, -1) - float(RF.PINS[k])) < 1e-12 for k in PIN_MAP)
    return ok, ("a corrupted default still matches" if ok else
                f"corrupted REV_MIN default caught ({got.get('REV_MIN')} vs "
                f"{RF.PINS['REV_MIN']})")


def rf5_real():
    got = _pine_defaults(PINE)
    bad = {k: (got.get(k), float(RF.PINS[k])) for k in PIN_MAP
           if abs(got.get(k, -1) - float(RF.PINS[k])) >= 1e-12}
    mode = _pine_mode_default(PINE)
    ok = not bad and len(got) == 6 and mode == RF.PINS["BOUNDARY_MODE"]
    return (ok, "all six numeric defaults EXACTLY equal the calibrated "
                f"pins AND BOUNDARY_MODE default '{mode}' == twin "
                f"'{RF.PINS['BOUNDARY_MODE']}'"
            if ok else f"mismatches: {bad}; mode={mode}")


# ── F-RF-6 · PINE STRUCTURE
def _structure(text):
    checks = [
        ("//@version=6", text.startswith("//@version=6")),
        ('titled "SS12-RangeFinder v1"', 'indicator("SS12-RangeFinder v1"' in text),
        ("max_boxes/lines/labels 500", all(
            f"max_{k}_count=500" in text.replace(" ", "")
            for k in ("boxes", "lines", "labels"))),
        ("every pin an input with [VETO] tooltip",
         text.count("[VETO]") >= 6 and text.count("input.") >= 6),
        ("display-only reconstruction header crediting the source",
         "DISPLAY-ONLY RECONSTRUCTION" in text and "@sergio_tesla_" in text),
        ("no request.security", "request.security" not in text),
        ("no alertcondition", "alertcondition" not in text),
        ("no signal plots", "plotshape" not in text and "plotarrow" not in text),
    ]
    bad = [n for n, ok in checks if not ok]
    return not bad, ("all 8 structure clauses hold" if not bad
                     else f"failed: {bad}")


def rf6_break():
    ok, det = _structure(PINE.replace("//@version=6", "//@version=5", 1)
                         .replace("request", "request", 1))
    return ok, ("version corruption passed" if ok
                else "corrupted //@version caught: " + det)


def rf6_real():
    return _structure(PINE)


# ── F-RF-7 · OPERATOR CONCORDANCE — KEY-B, body mode
# The concordance RECORD (body mode, wick redraw law): 4/4 ranges matched;
# among KEY-B's six R1–R3 deviations, FIVE detected (L-R2's Dec bottom is
# the miss); L-R4's bottom deviation detected AND its range resolved by the
# upside breakout. Boundary residuals are transcription+feed-grade and the
# redraw-basis divergence is the FILED FINDING (body-basis redraws lift
# concordance 4/8 → 6/8; the queue's wick law ships).
def _concordance(m):
    rows = RF.verify_key_b(m, D)
    matched = sum(1 for r in rows if r.get("matched_rid"))
    r13 = [k for r in rows[:3] for k, v in r.items()
           if k.endswith("_found")]
    r13_found = sum(1 for r in rows[:3] for k, v in r.items()
                    if k.endswith("_found") and v)
    r4 = rows[3]
    r4_dev = any(v for k, v in r4.items() if k.endswith("_found"))
    r4_break = any(e["event"] == "breakout-die" and e.get("side") == "top"
                   and e.get("rid") == r4.get("matched_rid")
                   for e in m["events"])
    return rows, matched, r13_found, len(r13), r4_dev, r4_break


def rf7_break():
    mw = RF.run_machine(D, dict(RF.PINS, BOUNDARY_MODE="wick"))
    rows = RF.verify_key_b(mw, D)
    # wick mode must FAIL the body-mode concordance record somewhere: the
    # inception-deviation channel does not exist in wick mode, so the
    # spring-birth detections vanish
    _, matched, f13, n13, r4_dev, r4_break = _concordance(mw)
    ok = matched == 4 and f13 >= 5 and r4_dev and r4_break
    incept = sum(1 for e in mw["events"]
                 if e["event"] == "inception-deviation")
    return ok, (f"wick mode STILL meets the body concordance bar "
                f"({f13}/{n13} devs, incept={incept}) — the mode swap "
                f"changes nothing" if ok else
                f"wick mode fails the bar ({f13}/{n13} R1–R3 devs, "
                f"{incept} inception events vs body's) — the body grammar "
                f"is load-bearing; NOTE the margin is ONE event on this "
                f"tape (L-R3's Feb-flush dev, body-inception-only)")


def rf7_real():
    rows, matched, f13, n13, r4_dev, r4_break = _concordance(M)
    ok = matched == 4 and f13 >= 5 and r4_dev and r4_break
    detail = (f"4/4 ranges matched; {f13}/{n13} R1–R3 deviations found "
              f"(L-R2 Dec bottom is the disclosed miss); L-R4 dev found "
              f"and resolved by upside BREAKOUT — per the queue bar")
    if not ok:
        detail = (f"matched={matched}/4 f13={f13}/{n13} r4_dev={r4_dev} "
                  f"r4_break={r4_break}")
    return ok, detail


# ── F-RF-8 · PINE-SIM PARITY — the fixture class that caught the v0 AND
# v1 pine BLOCKERs, made standing: a maintained python port of the pine
# bar loop (scripts/rangefinder_pine_sim.py) must reproduce the TWIN's
# chapters exactly in BOTH modes.  A pine edit without a sim edit, or
# either drifting from the twin, goes red here.
def _sim_chapters(mode):
    import rangefinder_pine_sim as PS
    r = PS.run_pine_repaired(boundaryMode=mode,
                             legMin=RF.PINS["LEG_MIN"],
                             revMin=RF.PINS["REV_MIN"],
                             touchEps=RF.PINS["TOUCH_EPS"],
                             devRet=RF.PINS["DEV_RETURN_BARS"],
                             brkN=RF.PINS["BREAK_CONFIRM_N"],
                             brkMargin=RF.PINS["BREAK_MARGIN"])
    return r


def _twin_chapters(mode):
    m = RF.run_machine(D, dict(RF.PINS, BOUNDARY_MODE=mode))
    return m, [(r.confirm_i, r.die_i,
                round(float(r.bottom), 1), round(float(r.top), 1))
               for r in m["ranges"] if r.confirm_i >= 0]


def rf8_break():
    import rangefinder_pine_sim as PS
    r = PS.run_pine_repaired(boundaryMode="body",
                             revMin=RF.PINS["REV_MIN"] * 2)
    _, tw = _twin_chapters("body")
    sim = [(x["conf"], x["die"], round(x["bot"], 1), round(x["top"], 1))
           for x in r["ranges"] if x.get("conf", -1) >= 0]
    ok = sim == tw
    return ok, ("a doubled REV_MIN sim still matches the twin — parity "
                "cannot fail" if ok else
                f"doubled REV_MIN diverges ({len(sim)} vs {len(tw)} "
                f"chapters) — the parity check has teeth")


def rf8_real():
    bad = []
    for mode in ("body", "wick"):
        r = _sim_chapters(mode)
        m, tw = _twin_chapters(mode)
        sim = [(x["conf"], x["die"], round(x["bot"], 1), round(x["top"], 1))
               for x in r["ranges"] if x.get("conf", -1) >= 0]
        if sim != tw:
            bad.append(f"{mode}: sim {sim} != twin {tw}")
        if abs(r["cov"] - m["coverage_pct"]) > 0.01:
            bad.append(f"{mode}: coverage {r['cov']:.2f} vs "
                       f"{m['coverage_pct']}")
        if r["nPivots"] != m["n_pivots"]:
            bad.append(f"{mode}: pivots {r['nPivots']} vs {m['n_pivots']}")
    ok = not bad
    return ok, ("pine-sim chapters, coverage and pivots EXACTLY equal the "
                "twin's in BOTH modes (body 5 chapters / 71.19% / 54 "
                "pivots; wick 5 / 64.05% / 54)" if ok
                else "; ".join(bad[:3]))


def main() -> int:
    print("=" * 74)
    print("SS12-RANGEFINDER v1 FIXTURES — break leg first, RED or void")
    print("=" * 74)
    prove("F-RF-1", "DETERMINISM — identical input, byte-identical log",
          rf1_break, rf1_real)
    prove("F-RF-2", "TARGETS — the disclosed subset, break = REV_MIN×3",
          rf2_break, rf2_real)
    prove("F-RF-3", "LIFECYCLE LEGALITY — every event carries its evidence",
          rf3_break, rf3_real)
    prove("F-RF-4", "SPRING KINSHIP — deviations vs the house spring shape",
          rf4_break, rf4_real)
    prove("F-RF-7", "OPERATOR CONCORDANCE — KEY-B in body mode",
          rf7_break, rf7_real)
    prove("F-RF-5", "PINE/TWIN PARITY — defaults == calibrated pins",
          rf5_break, rf5_real)
    prove("F-RF-6", "PINE STRUCTURE — v6, caps, tooltips, display-only",
          rf6_break, rf6_real)
    prove("F-RF-8", "PINE-SIM PARITY — the port matches the twin, both modes",
          rf8_break, rf8_real)
    print(f"\nRF FIXTURES: {len(PASSED)}/8 GREEN"
          + (f" · FAILED: {FAILED}" if FAILED else ""))
    return 1 if FAILED else 0


if __name__ == "__main__":
    raise SystemExit(main())
