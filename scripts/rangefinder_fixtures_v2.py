#!/usr/bin/env python
"""F-RF v2 suite — SS12-RangeFinder v2 (RF-3). TWO LEGS PER FIXTURE, the
BREAK leg first and it must go RED, or the fixture is void.
Run: ~/venvs/naiad/bin/python scripts/rangefinder_fixtures_v2.py
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


def check(fixture, ok, detail):
    print(f"  [{'PASS' if ok else 'FAIL'}] {fixture}: {detail}")
    return ok


def prove(fixture, title, break_leg, real_leg):
    print(f"\n{fixture} — {title}")
    b_ok, b_detail = break_leg()
    print(f"  [BREAK] deliberate violation -> "
          f"{'RED (correct)' if not b_ok else 'GREEN (FIXTURE IS VOID)'}: "
          f"{b_detail}")
    r_ok, r_detail = real_leg()
    green = check(fixture, r_ok, r_detail)
    if b_ok:
        FAILED.append(f"{fixture} (break leg passed)")
    elif not green:
        FAILED.append(fixture)
    else:
        PASSED.append(fixture)


D = RF.bars_4h()
V2 = RF.run_v2(D, RF.PINS_V2)
MAC, MIC = V2["macro"], V2["micro"]
LOG_M = json.dumps(MAC["events"], sort_keys=True)
LOG_U = json.dumps(MIC["events"], sort_keys=True)


# ── F-RF-1v2 · determinism, BOTH scales
def rf1_break():
    d2 = D.copy()
    d2.loc[d2.index[800], "h"] = d2["h"].iloc[800] * 1.02
    w = RF.run_v2(d2, RF.PINS_V2)
    same = (json.dumps(w["macro"]["events"], sort_keys=True) == LOG_M
            and json.dumps(w["micro"]["events"], sort_keys=True) == LOG_U)
    return same, ("perturbed tape, same logs — no teeth" if same else
                  "one perturbed bar changes the logs, both scales")


def rf1_real():
    w = RF.run_v2(D.copy(), RF.PINS_V2)
    same = (json.dumps(w["macro"]["events"], sort_keys=True) == LOG_M
            and json.dumps(w["micro"]["events"], sort_keys=True) == LOG_U)
    return same, (f"byte-identical event logs on re-run (macro "
                  f"{len(MAC['events'])}, micro {len(MIC['events'])})"
                  if same else "nondeterminism")


# ── F-RF-8 · HIERARCHY [H1]
def _hierarchy(v2):
    bad = []
    macro_pins = dict(RF.PINS,
                      LEG_MIN=RF.PINS["LEG_MIN"] * RF.PINS_V2["SCALE_MULT"],
                      REV_MIN=RF.PINS["REV_MIN"] * RF.PINS_V2["SCALE_MULT"])
    m_alone = RF.run_machine(D, macro_pins)
    if v2["state"] != m_alone["final_state"]:
        bad.append(f"global state {v2['state']} != macro-alone "
                   f"{m_alone['final_state']} — something else wrote it")
    # memory/flip events belong to macro DEAD CONFIRMED boundaries only
    corpse_px = {round(float(r.top), 1) for r in v2["macro"]["ranges"]
                 if r.state == "DEAD" and r.confirm_i >= 0}
    corpse_px |= {round(float(r.bottom), 1) for r in v2["macro"]["ranges"]
                  if r.state == "DEAD" and r.confirm_i >= 0}
    for e in v2["leash"]:
        if e["event"] in ("flip", "line-expired", "memory-retest",
                          "flip-retest") and e["px"] not in corpse_px:
            bad.append(f"leash event at px {e['px']} matches no macro "
                       f"corpse boundary")
    # containment AT BIRTH, recomputed from the EVENTS (the twin snapshots
    # its spans; this reconstruction is the independent path [review: the
    # first draft called RF._span — end-of-run, the same look-ahead])
    mac_by_rid = {r.rid: r for r in v2["macro"]["ranges"]}
    mic_by_rid = {r.rid: r for r in v2["micro"]["ranges"]}
    for rid, prid in v2["kept"]:
        r, q = mic_by_rid[rid], mac_by_rid[prid]
        i = r.confirm_i
        rlo, rhi = RF._span_at(r, v2["micro"]["events"], i)
        qlo, qhi = RF._span_at(q, v2["macro"]["events"], i)
        if not (rlo >= qlo and rhi <= qhi):
            bad.append(f"micro rid{rid} birth-span [{rlo:.0f},{rhi:.0f}] "
                       f"outside parent rid{prid}'s as-of span "
                       f"[{qlo:.0f},{qhi:.0f}]")
        if not (q.confirm_i <= r.confirm_i
                and (q.die_i < 0 or q.die_i > r.confirm_i)):
            bad.append(f"micro rid{rid} born outside parent's life")
    # THE KEEP RECORD [review: a suppress-everything regression passed —
    # nothing asserted any micro is ever kept]
    if len(v2["kept"]) != 3:
        bad.append(f"kept count {len(v2['kept'])} != the record's 3")
    return bad


def rf8_break():
    w = dict(V2)
    w["state"] = ("BEAR_EXP" if V2["state"] != "BEAR_EXP" else "BULL_EXP")
    bad1 = _hierarchy(w)
    w2 = dict(V2, kept=[])          # a suppress-everything regression
    bad2 = _hierarchy(w2)
    ok = not bad1 or not bad2
    return ok, ("a planted foreign state or an emptied keep-set PASSED"
                if ok else
                f"both plants caught: [{bad1[0]}] · [{bad2[0]}]")


def rf8_real():
    bad = _hierarchy(V2)
    return (not bad,
            f"global state is macro-alone's; all {len(V2['leash'])} leash "
            f"events sit on macro corpse boundaries; all {len(V2['kept'])} "
            f"kept micro ranges born inside their live parent "
            f"({len(V2['suppressed'])} suppressed, counted)"
            if not bad else "; ".join(bad[:3]))


# ── F-RF-9 · FLIPS [H2] — the operator's own arrows
def rf9_break():
    inv = dict(RF.PINS_V2, FLIP_HOLD_MARGIN=-1.0)   # nothing can hold
    leash = RF.flips_and_leash(MAC, D, inv)
    flips = [e for e in leash if e["event"] == "flip"]
    cf1 = [e for e in flips if e["polarity"] == "resistance"
           and abs(e["px"] - 84_500) <= 1_500]
    ok = bool(cf1)
    return ok, ("inverted hold rule still flips C-F1 — the hold reads "
                "nothing" if ok else
                f"inverted hold rule kills every flip ({len(flips)} left) "
                f"— the hold law is load-bearing")


def rf9_real():
    flips = V2["flips"]
    cf1 = [e for e in flips if e["polarity"] == "resistance"
           and abs(e["px"] - 84_500) <= 1_500 and e["ts"] < "2026-02-15"]
    cf2 = [e for e in flips if e["polarity"] == "support"
           and abs(e["px"] - 75_000) <= 1_200]
    may_rt = [e for e in V2["leash"] if e["event"] == "flip-retest"
              and abs(e["px"] - 75_000) <= 1_200
              and "2026-05" in e["ts"]]
    ok = bool(cf1) and bool(cf2) and bool(may_rt)
    return ok, (f"C-F1 ▼ {cf1[0]['ts']} px {cf1[0]['px']} (the large grey "
                f"arrow) · C-F2 ▲ {cf2[0]['ts']} px {cf2[0]['px']}, with "
                f"{len(may_rt)} May flip-retests of that line — at least "
                f"one operator-marked touch detected" if ok else
                f"cf1={bool(cf1)} cf2={bool(cf2)} may={len(may_rt)}")


# ── F-RF-10 · THE LEASH [H3]
def _leash_count(leash_events, macro):
    """Recompute live-line counts per side per bar INDEPENDENTLY from the
    ranges + expiry/touch events."""
    n = V2["macro"]["n_bars"]
    born = []
    for r in macro["ranges"]:
        if r.state == "DEAD" and r.confirm_i >= 0:
            born.append(("top", round(float(r.top), 1), r.die_i, r.rid))
            born.append(("bottom", round(float(r.bottom), 1), r.die_i,
                         r.rid))
    ends = {}
    for e in leash_events:
        if e["event"] in ("line-expired",) or (
                e["event"] in ("memory-retest", "flip")):
            k = (e["side"], e["px"], e["rid"])
            ends.setdefault(k, e["i"])
    worst = 0
    for i in range(n):
        for side in ("top", "bottom"):
            c = 0
            for s_, px, b, rid in born:
                if s_ != side or b > i:
                    continue
                end = ends.get((s_, px, rid), 10 ** 9)
                if i < end or (i == end and False):
                    c += 1   # end-of-bar state: a line expiring AT i is
                    # dead by the bar's close [off-by-one, first run]
            worst = max(worst, c)
    return worst


def _synthetic_macro(n_corpses=10):
    """A fabricated corpse population — the real tape has only 5 macro
    corpses, so the cap never binds on it and a cap-raising break leg
    would be VOID [first-run lesson]. Ten staggered never-touched corpses
    per side make the cap decisive."""
    import copy
    fake = {"ranges": [], "n_bars": MAC["n_bars"], "events": []}
    proto = next(r for r in MAC["ranges"]
                 if r.state == "DEAD" and r.confirm_i >= 0)
    for k in range(n_corpses):
        r = copy.copy(proto)
        r.rid = 900 + k
        r.confirm_i = 20 + k * 5
        r.die_i = 40 + k * 5
        # park boundaries far off-tape so no bar ever touches them
        r.top = 1_000_000.0 + k
        r.bottom = 1.0 + k * 0.001
        fake["ranges"].append(r)
    return fake


def rf10_break():
    import rangefinder_twin as T
    fake = _synthetic_macro()
    old_cap = T.MEM_CAP_PER_SIDE
    T.MEM_CAP_PER_SIDE = 99          # the cap raised SILENTLY
    try:
        leash = T.flips_and_leash(fake, D, RF.PINS_V2)
    finally:
        T.MEM_CAP_PER_SIDE = old_cap
    worst = _leash_count(leash, fake)
    ok = worst <= 6
    return ok, (f"cap raised to 99 on ten synthetic corpses and the count "
                f"still <= 6 — the counter is blind" if ok else
                f"cap raised silently → {worst} live lines per side on the "
                f"synthetic population — the ≤6 law catches it")


def rf10_real():
    import rangefinder_twin as T
    worst = _leash_count(V2["leash"], MAC)
    exp = [e for e in V2["leash"] if e["event"] == "line-expired"]
    bad = [e for e in exp if e.get("reason") not in ("ttl", "cap")]
    # the cap PROVEN decisive on the synthetic population at cap 6
    fake = _synthetic_macro()
    leash6 = T.flips_and_leash(fake, D, RF.PINS_V2)
    worst6 = _leash_count(leash6, fake)
    caps6 = sum(1 for e in leash6 if e.get("reason") == "cap")
    ok = worst <= 6 and not bad and worst6 <= 6 and caps6 > 0
    return ok, (f"real tape: live lines never exceed {worst} per side, "
                f"{len(exp)} expiries all reasoned; synthetic ten-corpse "
                f"population: cap 6 holds (worst {worst6}) with {caps6} "
                f"cap-expiries — the law bites where the tape cannot make "
                f"it" if ok else
                f"worst={worst} bad={len(bad)} synth={worst6}/{caps6}")


# ── F-RF-7c · OPERATOR CONCORDANCE — KEY-C
# THE KEY-C RECORD, HARD LITERALS [review: loading from the export was
# self-comparison shading — these numbers are the record and a regression
# on any of them goes red here]
RECORD_C = {
    "C-R1": {"top_residual": 998.9, "bottom_residual": 2968.1, "devs": 2},
    "C-R2": {"top_residual": 51.5, "bottom_residual": 1294.6, "devs": 1},
    "C-R3": {"bottom_residual": 53.0, "devs": 1},
}


def rf7c_break():
    v2w = RF.run_v2(D, dict(RF.PINS_V2, SCALE_MULT=1.0))   # no hierarchy
    _, res = RF.score_key_c(v2w, D)
    q1 = next(r for r in res if r["target"] == "C-Q1")
    ok = q1["within_2_4"]
    return ok, ("SCALE 1.0 still lands 2–4 macro ranges — the scale does "
                "nothing" if ok else
                f"SCALE 1.0 explodes the macro count to "
                f"{q1['macro_confirms_feb_aug']} — the hierarchy is "
                f"load-bearing")


def rf7c_real():
    _, res = RF.score_key_c(V2, D)
    bad = []
    for row in res:
        t = row["target"]
        if t in RECORD_C:
            rec = RECORD_C[t]
            for k, want in rec.items():
                if k == "devs":
                    got = sum(1 for kk, vv in row.items()
                              if kk.endswith("_found") and vv)
                    if got != want:
                        bad.append(f"{t}: {got}/{want} devs")
                elif abs(float(row.get(k, 1e9)) - float(want)) > 0.5:
                    bad.append(f"{t}.{k}={row.get(k)} (record {want})")
        elif t.startswith("C-F") and not row["found_flag"]:
            bad.append(f"{t} NOT FOUND")
        elif t == "C-Q1" and not row["within_2_4"]:
            bad.append("C-Q1 out of band")
    ok = not bad
    return ok, ("KEY-C record holds: C-R1 top ✓ devs ✓ (bottom 2,968 — "
                "the operator's boundary tracks the ZONE edge, the "
                "redraw-basis finding again, DISCLOSED not forced) · "
                "C-R2 top 52 ✓ (bottom 1,295, 95 over) · C-R3 bottom 53 ✓ "
                "· C-F1 ✓ · C-F2 ✓ · C-Q1 = 3 ✓" if ok
                else "; ".join(bad[:4]))


# ── F-RF-5v2 · PINE PARITY
PINE = (ROOT / "pine" / "SS12_RangeFinder_v2.pine").read_text()
NUM_MAP = {"LEG_MIN": "legMin", "REV_MIN": "revMin", "TOUCH_EPS": "touchEps",
           "DEV_RETURN_BARS": "devRet", "BREAK_CONFIRM_N": "brkN",
           "BREAK_MARGIN": "brkMargin"}
V2_MAP = {"SCALE_MULT": "scaleMult", "FLIP_HOLD_MARGIN": "flipMargin",
          "FLIP_HOLD_BARS": "flipBars", "MEM_TTL_BARS": "memTtl"}


def _defaults(text, mapping):
    out = {}
    for pin, var in mapping.items():
        m = re.search(rf"^{var}\s*=\s*input\.(?:float|int)\(\s*([0-9.]+)",
                      text, re.M)
        if m:
            out[pin] = float(m.group(1))
    return out


def rf5_break():
    fake = PINE.replace('scaleMult = input.float(3.0', 'scaleMult = input.float(2.0')
    got = _defaults(fake, V2_MAP)
    ok = abs(got.get("SCALE_MULT", -1) - RF.PINS_V2["SCALE_MULT"]) < 1e-12
    return ok, ("corrupted SCALE default matches" if ok else
                f"corrupted SCALE default caught ({got.get('SCALE_MULT')})")


def rf5_real():
    g1 = _defaults(PINE, NUM_MAP)
    g2 = _defaults(PINE, V2_MAP)
    bad = {k: (g1.get(k), RF.PINS[k]) for k in NUM_MAP
           if abs(g1.get(k, -1) - float(RF.PINS[k])) >= 1e-12}
    bad.update({k: (g2.get(k), RF.PINS_V2[k]) for k in V2_MAP
                if abs(g2.get(k, -1) - float(RF.PINS_V2[k])) >= 1e-12})
    m = re.search(r'boundaryMode\s*=\s*input\.string\(\s*"(\w+)"', PINE)
    mode = m.group(1) if m else None
    ok = not bad and mode == "body" and len(g1) == 6 and len(g2) == 4
    return ok, ("all six frozen micro pins + four v2 pins + body mode "
                "EXACTLY equal the twin's" if ok
                else f"mismatches: {bad}; mode={mode}")


# ── F-RF-6v2 · STRUCTURE
def _use_before_decl(text):
    lines = text.split("\n")
    decl = {}
    for i, ln in enumerate(lines, 1):
        m = re.match(r"\s*var\s+(?:\w+(?:<\w+>)?\s+)?(\w+)\s*=", ln)
        if m:
            decl.setdefault(m.group(1), i)
    for name, dln in decl.items():
        pat = re.compile(rf"\b{re.escape(name)}\b")
        for i, ln in enumerate(lines, 1):
            if i >= dln:
                break
            if pat.search(ln) and not ln.strip().startswith("//"):
                return [(name, i, dln)]
    return []


def _structure(text):
    checks = [
        ("//@version=6", text.startswith("//@version=6")),
        ('titled "SS12-RangeFinder v2"',
         'indicator("SS12-RangeFinder v2"' in text),
        ("caps 500", all(f"max_{k}_count=500" in text.replace(" ", "")
                         for k in ("boxes", "lines", "labels"))),
        ("legend table present", text.count("table.new") >= 2
         and "LEGEND" in text.upper()),
        ("toggles: micro/memory/midline/legend/pivots, each CONSUMED",
         all(text.count(t) >= 2 for t in ("showMicro", "showMemory",
                                          "showMidline", "showLegend",
                                          "showPivots"))),
        ("[VETO] tooltips >= 10", text.count("[VETO]") >= 10),
        ("credited display-only header",
         "DISPLAY-ONLY" in text and "@sergio_tesla_" in text),
        ("no security/alerts/signals",
         "request.security" not in text and "alertcondition" not in text
         and "plotshape" not in text and "plotarrow" not in text),
        # the operator's TV compiler caught gState used above its var
        # declaration (CE10272) — the class is now a standing clause
        ("declaration order: no var used above its declaration",
         not _use_before_decl(text)),
        # round 3: TV's 10-char shorttitle max, also operator-caught
        ("shorttitle <= 10 chars",
         (lambda m: bool(m) and len(m.group(1)) <= 10)(
             re.search(r'shorttitle="([^"]*)"', text))),
    ]
    bad = [n for n, ok in checks if not ok]
    return not bad, (f"all {len(checks)} v2 structure clauses hold"
                     if not bad else f"failed: {bad}")


def rf6_break():
    ok1, _ = _structure(PINE.replace('showLegend', 'xLegend'))
    # plant a use-before-declaration: assign gState on line 2
    planted = PINE.replace('atr = ta.atr(ATR_LEN)',
                           'gStatePlant := "X"\natr = ta.atr(ATR_LEN)', 1
                           ).replace('var string gState =',
                                     'var string gStatePlant = "n"\n'
                                     'var string gState =', 1)
    # move the planted assignment ABOVE the declaration
    ok2 = not _use_before_decl(
        planted.replace('gStatePlant := "X"', '', 1)
        .replace('//@version=6', '//@version=6\ngStatePlant := "X"', 1))
    ok = ok1 or ok2
    return ok, ("a break variant passed" if ok else
                "toggle removal AND planted use-before-declaration both "
                "caught")


def rf6_real():
    return _structure(PINE)


# ── F-RF-12 · PINE-SIM PARITY, both cores
def _chapters(m):
    return [(r.confirm_i, r.die_i, round(float(r.bottom), 1),
             round(float(r.top), 1))
            for r in m["ranges"] if r.confirm_i >= 0]


def rf12_break():
    import rangefinder_pine_sim as PS
    r = PS.run_pine_repaired(tape=D, boundaryMode="body",
                             legMin=RF.PINS["LEG_MIN"],
                             revMin=RF.PINS["REV_MIN"] * 2,
                             touchEps=RF.PINS["TOUCH_EPS"],
                             devRet=RF.PINS["DEV_RETURN_BARS"],
                             brkN=RF.PINS["BREAK_CONFIRM_N"],
                             brkMargin=RF.PINS["BREAK_MARGIN"])
    sim = [(x["conf"], x["die"], round(x["bot"], 1), round(x["top"], 1))
           for x in r["ranges"] if x.get("conf", -1) >= 0]
    ok = sim == _chapters(MIC)
    return ok, ("doubled REV_MIN still matches" if ok else
                "doubled REV_MIN diverges — teeth")


def rf12_real():
    import rangefinder_pine_sim as PS
    bad = []
    for label, mach, lm, rv in (("micro", MIC, RF.PINS["LEG_MIN"],
                                 RF.PINS["REV_MIN"]),
                                ("macro", MAC,
                                 RF.PINS["LEG_MIN"] * RF.PINS_V2["SCALE_MULT"],
                                 RF.PINS["REV_MIN"] * RF.PINS_V2["SCALE_MULT"])):
        r = PS.run_pine_repaired(tape=D, boundaryMode="body", legMin=lm,
                                 revMin=rv, touchEps=RF.PINS["TOUCH_EPS"],
                                 devRet=RF.PINS["DEV_RETURN_BARS"],
                                 brkN=RF.PINS["BREAK_CONFIRM_N"],
                                 brkMargin=RF.PINS["BREAK_MARGIN"])
        sim = [(x["conf"], x["die"], round(x["bot"], 1),
                round(x["top"], 1))
               for x in r["ranges"] if x.get("conf", -1) >= 0]
        if sim != _chapters(mach):
            bad.append(f"{label}: sim {len(sim)} vs twin "
                       f"{len(_chapters(mach))} chapters")
    return (not bad, "pine-sim cores reproduce BOTH twin scales exactly "
            "(the flip/leash render layer is twin-fixtured by F-RF-9/10 "
            "and eyeball-verified — scope disclosed)" if not bad
            else "; ".join(bad))


def main() -> int:
    print("=" * 74)
    print("SS12-RANGEFINDER v2 FIXTURES — break leg first, RED or void")
    print("=" * 74)
    prove("F-RF-1v2", "DETERMINISM, both scales", rf1_break, rf1_real)
    prove("F-RF-8", "HIERARCHY — containment law, macro-only state/lines",
          rf8_break, rf8_real)
    prove("F-RF-9", "FLIPS — the operator's own arrows", rf9_break, rf9_real)
    prove("F-RF-10", "THE LEASH — cap 6, reasons on every expiry",
          rf10_break, rf10_real)
    prove("F-RF-7c", "OPERATOR CONCORDANCE — KEY-C", rf7c_break, rf7c_real)
    prove("F-RF-5v2", "PINE PARITY — frozen micro + v2 pins", rf5_break,
          rf5_real)
    prove("F-RF-6v2", "PINE STRUCTURE v2", rf6_break, rf6_real)
    prove("F-RF-12", "PINE-SIM PARITY, both cores", rf12_break, rf12_real)
    print(f"\nRF v2 FIXTURES: {len(PASSED)}/8 GREEN"
          + (f" · FAILED: {FAILED}" if FAILED else ""))
    try:
        (RF.OUT / "FIXTURES_v2.txt").write_text(
            f"RF v2 FIXTURES: {len(PASSED)}/8 GREEN\n")
    except Exception:
        pass
    return 1 if FAILED else 0


if __name__ == "__main__":
    raise SystemExit(main())
