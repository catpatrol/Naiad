#!/usr/bin/env python
"""F-RF-1..6 — SS12-RangeFinder v0 fixtures.  TWO LEGS PER FIXTURE, the
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
    ok = bool(res["Q5_junjul_deviation_survived"]["value"])
    return ok, (f"REV_MIN×3 still hits Q5 — the target does not bind"
                if ok else
                f"REV_MIN×3 loses Q5 (and pivots fall to {m2['n_pivots']}) "
                f"— the calibration is load-bearing")


# THE CALIBRATION OF RECORD, AS LITERALS [review: comparing to the export
# was a self-comparison — the export is written by the same run_machine;
# these numbers are the RECORD and a regression on any of them goes red].
RECORD = {"Q1_coverage": 60.0, "Q2_pivot_per_bars": 9.09,
          "Q3_conf_per_100": 1.5, "Q4_lifetime": 45.7,
          "Q5_junjul_deviation_survived": True}


def rf2_real():
    _, res = RF.score(M, D)
    bad = []
    for k, want in RECORD.items():
        got = res[k]["value"]
        if isinstance(want, bool):
            if bool(got) is not want:
                bad.append(f"{k}={got}")
        elif abs(float(got) - want) > 0.05:
            bad.append(f"{k}={got} (record {want})")
    exp = json.loads((RF.OUT / "BTCUSD_1d_ranges.json").read_text())
    fresh = json.dumps(res, sort_keys=True, default=str) == json.dumps(
        exp["residuals"], sort_keys=True, default=str)
    ok = not bad and fresh
    return ok, ("Q5 SATISFIED and every residual equals the HARD-CODED "
                "calibration-of-record (the DISCLOSED subset: Q5 hit, Q4 "
                "near-miss, Q1–Q3 resist — filed, not forced); export "
                "fresh" if ok else
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
            if e["event"] == "deviation-confirm":
                opens = [x for x in evs if x["event"] == "breach-open"
                         and x["i"] < e["i"]]
                if not opens:
                    bad.append(f"rid{rid}: deviation without breach-open")
                    continue
                b = opens[-1]
                if e["i"] - b["i"] > pins["DEV_RETURN_BARS"]:
                    bad.append(f"rid{rid}: return outside DEV_RETURN_BARS")
                if not any(x["event"] == "redraw" and x["i"] == e["i"]
                           for x in evs):
                    bad.append(f"rid{rid}: deviation without same-bar redraw")
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
                               in ("deviation-confirm", "breach-lapse")]
                    if between:
                        bad.append(f"rid{rid}: die after the breach already "
                                   f"resolved")
        n_dies = sum(1 for x in evs if x["event"] == "breakout-die")
        if n_dies > 1:
            bad.append(f"rid{rid}: {n_dies} deaths on one range")
        # no boundary edit except via redraw: every redraw pairs a deviation
        for x in evs:
            if x["event"] == "redraw" and not any(
                    y["event"] == "deviation-confirm" and y["i"] == x["i"]
                    for y in evs):
                bad.append(f"rid{rid}: redraw WITHOUT a confirmed deviation")
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
               "side": "top", "frm": 1.0, "to": 2.0})   # planted, no deviation
    ev.append({"i": 60, "ts": "x", "event": "breakout-die", "rid": 2,
               "side": "top", "by": "margin", "closes": 1,
               "px": 1.0})                    # planted die WITHOUT a breach
    ok, det = _legality(ev, RF.PINS)
    return ok, ("planted redraw-without-deviation AND die-without-breach "
                "PASSED legality" if ok else
                "both plants caught: " + det)


def rf3_real():
    return _legality(M["events"], RF.PINS)


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
    springs = _springs_independent(D)
    dev_bot, matched = [], 0
    for e in M["events"]:
        if e["event"] == "deviation-confirm" and e["side"] == "bottom":
            # the deviation EPISODE: breach-open .. confirm bar
            opens = [x for x in M["events"] if x["event"] == "breach-open"
                     and x["rid"] == e["rid"] and x["i"] <= e["i"]]
            b = opens[-1]["i"]
            dev_bot.append((b, e["i"]))
            c = D["c"].to_numpy(float)
            l = D["l"].to_numpy(float)
            boundary = opens[-1]["px"]      # close that breached; the
            # independent shape test uses the episode's own geometry:
            # a sweep below the pre-breach 20-bar extreme with a close back
            # above it anywhere in the episode
            prior = float(np.min(l[max(0, b - 20):b]))
            swept = bool(np.min(l[b:e["i"] + 1]) < prior)
            ret = (c[e["i"]] > prior) if not rule_flip else (c[e["i"]] < prior)
            if swept and ret:
                matched += 1
    n_spring_in_dev = sum(1 for s in springs
                          if any(b <= s <= j for b, j in dev_bot))
    ok = matched == len(dev_bot) and len(dev_bot) > 0
    return ok, matched, len(dev_bot), len(springs), n_spring_in_dev


def rf4_break():
    ok, m, n, s, sid = _kinship(rule_flip=True)
    return ok, (f"corrupted return-close rule still matches {m}/{n}"
                if ok else
                f"corrupted return-close rule matches {m}/{n} — the shape "
                f"test reads the close for real")


def rf4_real():
    ok, m, n, s, sid = _kinship()
    return ok, (f"OVERLAP both directions: {m}/{n} twin bottom-deviations "
                f"satisfy the independent house spring shape; {sid}/{s} "
                f"independent springs fall inside a deviation episode. "
                f"Non-overlap would be a red flag on the reconstruction, "
                f"not a tuning knob." if n else
                "no bottom deviations to test")


# ── F-RF-5 · PINE/TWIN PARITY
PINE = (ROOT / "pine" / "SS12_RangeFinder_v0.pine").read_text()
PIN_MAP = {"LEG_MIN": "legMin", "REV_MIN": "revMin", "TOUCH_EPS": "touchEps",
           "DEV_RETURN_BARS": "devRet", "BREAK_CONFIRM_N": "brkN",
           "BREAK_MARGIN": "brkMargin"}


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
    return (not bad and len(got) == 6,
            "all six pine input defaults EXACTLY equal the calibrated pins"
            if not bad else f"mismatches: {bad}")


# ── F-RF-6 · PINE STRUCTURE
def _structure(text):
    checks = [
        ("//@version=6", text.startswith("//@version=6")),
        ('titled "SS12-RangeFinder v0"', 'indicator("SS12-RangeFinder v0"' in text),
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


def main() -> int:
    print("=" * 74)
    print("SS12-RANGEFINDER v0 FIXTURES — break leg first, RED or void")
    print("=" * 74)
    prove("F-RF-1", "DETERMINISM — identical input, byte-identical log",
          rf1_break, rf1_real)
    prove("F-RF-2", "TARGETS — the disclosed subset, break = REV_MIN×3",
          rf2_break, rf2_real)
    prove("F-RF-3", "LIFECYCLE LEGALITY — every event carries its evidence",
          rf3_break, rf3_real)
    prove("F-RF-4", "SPRING KINSHIP — deviations vs the house spring shape",
          rf4_break, rf4_real)
    prove("F-RF-5", "PINE/TWIN PARITY — defaults == calibrated pins",
          rf5_break, rf5_real)
    prove("F-RF-6", "PINE STRUCTURE — v6, caps, tooltips, display-only",
          rf6_break, rf6_real)
    print(f"\nRF FIXTURES: {len(PASSED)}/6 GREEN"
          + (f" · FAILED: {FAILED}" if FAILED else ""))
    return 1 if FAILED else 0


if __name__ == "__main__":
    raise SystemExit(main())
