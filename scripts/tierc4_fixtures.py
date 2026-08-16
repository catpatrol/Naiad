"""TIER-C4 fixtures — the transcript, printed.  HALTs non-zero on any failure.

    F-C4-1        gates transcript + ESTATE READY over the corridor AND its
                  F-5 lead-in AND the F-7-truncated strip
    F-C4-INHERIT  the two amendments are the ONLY diffs — the unchanged half is
                  the SAME OBJECT two generations deep, asserted with `is`; and
                  where the code is TRANSCRIBED rather than imported (the entry
                  half of the ride), the claim is made as an OUTCOME: five
                  Tier-C3 tables must come out content-hash-identical
    F-C4-RAIL     EVERY stop is >= 1.0 x ATR at placement — the ENTRY stop
                  against the entry close (inherited) AND EVERY ADVANCED stop
                  against its own confirming close (new)
    F-C4-PIVOT    three RATCHET fractals hand-verified on RAW 4h bars: strict
                  (2,2), the close-confirmation lag, the causal governs-next-bar
                  rule, the buffer, the rail, monotonicity, and the payout
    F-C4-HARV     the harvest rule RE-DERIVED from raw bars on EVERY campaign
                  (first-touch / blocked-by-exit-bar / never-touched, asserted
                  exhaustive), and EVERY fill hand-reconciled from raw prices,
                  the register's toll and journaled funding
    F-C4-SEAL     the sealed mask over BOTH published prices — the entry anchor
                  and every ratchet pivot — plus every ms column of every table
    F-C4-ABLATE   the V3 cell reproduces Tier-C3's FILED net R trade by trade,
                  so every marginal is the AMENDMENT and not the fork; five
                  cells, including the seal floor "printed both ways"
    F-C4-DET      determinism: full re-run hash-identical
    F-C4-6        import closure: the decision path reads no registry symbol
    F-KEY         on every join, re-asserted against the WRITTEN tables

House idiom inherited from `tierc3_fixtures.py`: one `--- F-ID : PASS ---`
header per fixture with indented evidence beneath, because a fixture that
prints only a verdict cannot be audited.

USAGE  ~/venvs/naiad/bin/python scripts/tierc4_fixtures.py
"""
from __future__ import annotations

import ast
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import tierc4_baseline as TC                                        # noqa: E402
import tierc4_rules as RC                                           # noqa: E402
import tierc3_baseline as T3                                        # noqa: E402
import tierc3_rules as V3                                           # noqa: E402
import tierc2_baseline as TB                                        # noqa: E402
import tierc2_rules as V1                                           # noqa: E402
import analytics as AN                                              # noqa: E402

T: list[str] = []
RESULTS: dict[str, bool] = {}


def rec(fid: str, ok: bool, lines: list[str]) -> bool:
    RESULTS[fid] = bool(ok)
    T.append(f"--- {fid} : {'PASS' if ok else 'FAIL'} ---")
    T.extend("    " + x for x in lines)
    return bool(ok)


def sh(cmd: str) -> str:
    return subprocess.run(cmd, shell=True, capture_output=True, text=True,
                          cwd=ROOT).stdout.strip()


def tbl(name: str, root: Path | None = None) -> pd.DataFrame:
    return pd.read_parquet((root or TC.OUT) / f"{name}.parquet")


def code_only(src: str) -> str:
    """The module's CODE, with comments and docstrings removed.

    F-C4-6's tape-column leg is a name scan, and a scan over raw TEXT
    false-positives on the module's own prose — Tier-C3's fixture already
    recorded that failure mode for the import leg ("a line-grep gives false
    positives on this module's own prose about not importing") and fixed the
    import leg with an AST walk while leaving the column leg on raw text.  It
    duly fired: a COMMENT in `tierc4_rules.py` explaining why a field was
    renamed away from a tape-column name was itself flagged as a tape-column
    name.  So the column leg gets the same treatment as the import leg.

    An AST round-trip drops comments; docstrings are stripped explicitly.
    Ordinary string literals are KEPT, deliberately — `tape["wall_family"]` is
    a subscript and a real consultation, and a scan that dropped it would be
    weaker, not cleaner.
    """
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if not isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef,
                                 ast.AsyncFunctionDef)):
            continue
        b = node.body
        if (b and isinstance(b[0], ast.Expr)
                and isinstance(b[0].value, ast.Constant)
                and isinstance(b[0].value.value, str)):
            node.body = b[1:] or [ast.Pass()]
    return ast.unparse(tree)


# ═══════════════════════════════════════════════════════ F-C4-1 · the gates
def f_gates() -> bool:
    lines, ok = [], True
    head, remote = sh("git rev-parse --short HEAD"), sh("git remote -v")
    branch, pwd, home = sh("git branch --show-current"), str(ROOT), str(Path.home())
    checks = [
        ("HEAD", head, bool(head)),
        ("remote catpatrol/Naiad", "yes" if "catpatrol/Naiad" in remote else "NO",
         "catpatrol/Naiad" in remote),
        ("pwd", pwd, pwd == f"{home}/Naiad"),
        ("IDENTITY v2 · no cloud-sync token", "clean",
         not any(t in pwd for t in ("OneDrive", "com~apple~CloudDocs",
                                    "Mobile Documents", "GoogleDrive", "My Drive"))),
        ("branch", branch, branch == "v12-v1-census"),
        ("venv python", str(Path.home() / "venvs/naiad/bin/python"),
         (Path.home() / "venvs/naiad/bin/python").exists()),
    ]
    for name, val, good in checks:
        ok &= good
        lines.append(f"{'OK ' if good else 'HALT'}  {name:34} {val}")

    lead = TC._ms(TC.SCORED[0]) - RC.LEAD_IN_DAYS * TC.MS_1D
    spans = [("SCORED corridor", TC._ms(TC.SCORED[0]),
              TC._ms(TC.SCORED[1]) + TC.MS_1D - 1),
             (f"F-5 lead-in ({RC.LEAD_IN_DAYS}d)", lead, TC._ms(TC.SCORED[0]) - 1),
             ("F-7 truncated PINNING", TC._ms(TC.PINNING[0]),
              TC._ms(TC.PINNING[1]) + TC.MS_1D - 1)]
    for label, lo, hi in spans:
        lines.append(f"ESTATE READY (read-only) {label}: "
                     f"{TC.iso(lo)} -> {TC.iso(hi)}")
        for sym in RC.UNIVERSE:
            for tf, step in (("1h", TC.MS_1H), ("4h", TC.MS_4H)):
                d = TC.load_klines(sym, tf)
                o = d["open_time"].to_numpy(np.int64)
                w = o[(o >= lo) & (o <= hi)]
                if not len(w):
                    ok = False
                    lines.append(f"  HALT  {sym:9} {tf:3} NO ROWS")
                    continue
                diffs = np.diff(w)
                gaps = int((diffs != step).sum())
                good = gaps == 0 and bool((diffs > 0).all())
                ok &= good
                lines.append(f"  {'OK ' if good else 'HALT'}  {sym:9} {tf:3} "
                             f"rows={len(w):6d} gaps={gaps} "
                             f"{TC.iso(w[0])} -> {TC.iso(w[-1])}")
    # THE GUARD, LOADED AND IDLE — a CLASS claim proved as a record.
    man = json.loads((TC.OUT / "build_manifest.json").read_text())
    g = man.get("selection_guard", {})
    good = bool(g.get("loaded") and g.get("called")
                and g.get("candidates") == 0 and g["verdict"]["m"] == 0)
    ok &= good
    lines.append(f"{'OK ' if good else 'HALT'}  SELECTION GUARD loaded={g.get('loaded')} "
                 f"called={g.get('called')} candidates={g.get('candidates')} "
                 f"-> m={g.get('verdict', {}).get('m')} "
                 f"({g.get('verdict', {}).get('reason')}) — IDLE, as classed. "
                 f"ONE pre-named card, no grid, no sweep.")
    return rec("F-C4-1", ok, lines)


# ═════════════════════ F-C4-INHERIT · the amendments are the only diffs
def f_inherit() -> bool:
    """The unchanged half of the card is not a copy that resembles Tier-C3's —
    it IS Tier-C3's, and through it Tier-C2's.  `is` is the strongest statement
    available, so it is the one made."""
    lines, ok = [], True
    ident = [
        # ── the decision path, inherited from v3 (which inherits from v1) ──
        ("RC.build_4h", RC.build_4h, V1.build_4h),
        ("RC._crosses", RC._crosses, V1._crosses),
        ("RC.armings", RC.armings, V1.armings),
        ("RC.Frame4h", RC.Frame4h, V1.Frame4h),
        ("RC.Arming", RC.Arming, V1.Arming),
        ("RC.build_pivots_4h", RC.build_pivots_4h, V3.build_pivots_4h),
        ("RC.struct_stop_4h", RC.struct_stop_4h, V3.struct_stop_4h),
        ("RC.Pivots4h", RC.Pivots4h, V3.Pivots4h),
        ("RC.Stop", RC.Stop, V3.Stop),
        # ── the program, inherited from v3 and v2 ──
        ("TC.sealed_mask", TC.sealed_mask, T3.sealed_mask),
        ("TC.funnel_table", TC.funnel_table, T3.funnel_table),
        ("TC.lead_in_census", TC.lead_in_census, T3.lead_in_census),
        ("TC.lead_in_table", TC.lead_in_table, T3.lead_in_table),
        ("TC.anchor_lookback_disclosure", TC.anchor_lookback_disclosure,
         T3.anchor_lookback_disclosure),
        ("TC.WINDOWS", TC.WINDOWS, T3.WINDOWS),
        ("TC.write_table", TC.write_table, TB.write_table),
        ("TC.assert_key", TC.assert_key, TB.assert_key),
        ("TC.load_klines", TC.load_klines, TB.load_klines),
        ("TC.load_funding", TC.load_funding, TB.load_funding),
    ]
    for name, a, b in ident:
        good = a is b
        ok &= good
        lines.append(f"[{'OK ' if good else 'BAD'}] {name:32} is the inherited "
                     f"object")
    lines.append("")
    # ── THE NAMES THE PROGRAM CALLS THROUGH ITS PARENT, not through a local
    #    binding. `TB.headline_rows is TB.headline_rows` is x is x and proves
    #    nothing, so the claim that has content is stated instead: the v4
    #    program must not DEFINE any of these names itself. Driven from the
    #    program's own INHERITED_* tuples so those tuples stop being decoration.
    #    (Both defects — the self-identities and the dead tuples — were found by
    #    the post-build adversarial review.)
    prog_src = (ROOT / "scripts" / "tierc4_baseline.py").read_text()
    own_defs = {n.name for n in ast.parse(prog_src).body
                if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef,
                                  ast.ClassDef))}
    for tup, parent, pname in ((TC.INHERITED_FROM_TIERC3, T3, "tierc3_baseline"),
                               (TC.INHERITED_FROM_TIERC2, TB, "tierc2_baseline")):
        for n in tup:
            has = hasattr(parent, n)
            bound = getattr(TC, n, None)
            same = (bound is getattr(parent, n)) if (has and bound is not None) else None
            redefined = n in own_defs
            good = has and not redefined and (same is not False)
            ok &= good
            how = ("bound locally and IS the parent's object" if same
                   else "called through the parent, and NOT redefined here")
            lines.append(f"[{'OK ' if good else 'BAD'}] {pname}.{n:26} {how}"
                         f"{'  *** REDEFINED IN tierc4_baseline ***' if redefined else ''}")
    lines.append("")
    lines.append("THE AMENDMENTS — the only rule changes, each cited to the card:")
    for k, v in RC.REGISTER_DIFF.items():
        lines.append(f"  {k:26} = {v['value']}")
        lines.append(f"      {v['source'][:170]}")
    lines.append("")
    lines.append("THE RE-POINTED ROWS — one constant, two sites, asserted:")
    rep = [("RATCHET_BUF_ATR", RC.RATCHET_BUF_ATR, "STOP_BUF_ATR",
            RC.STOP_BUF_ATR),
           ("RATCHET_RAIL_ATR", RC.RATCHET_RAIL_ATR, "MIN_STOP_ATR",
            RC.MIN_STOP_ATR),
           ("HARVEST_BAND", RC.HARVEST_BAND, "(TIDE_FAST, TIDE_SLOW)",
            (RC.TIDE_FAST, RC.TIDE_SLOW))]
    for name, got, src, want in rep:
        good = got == want
        ok &= good
        lines.append(f"[{'OK ' if good else 'BAD'}] {name:20} {got} IS "
                     f"{src} — re-pointed inheritance, NOT a second constant "
                     f"for the same concept (the F-C3-e defect)")
    lines.append("")
    # THE PARTITION IS DERIVED FROM THE REGISTER, NOT TYPED BESIDE IT.
    # The first draft iterated a hand-written 3-tuple and printed "exactly
    # three new numbers" whatever the register held — a test that passes by
    # construction, which the sibling leg in F-C4-SEAL explicitly condemns. It
    # also mis-stated the count: HARVEST_MAX_PER_CAMPAIGN = 1 is a new number
    # too. Found by the post-build adversarial review.
    # The RE-POINTED rows are named by the CLAIM each makes, and the claim is
    # then checked — a value match alone would mis-classify HARVEST_FRACTION
    # (0.5) as STOP_BUF_ATR (0.5), which is exactly the kind of accident this
    # partition exists to prevent.
    REPOINT = {"RATCHET_BUF_ATR": ("STOP_BUF_ATR", V3.STOP_BUF_ATR),
               "RATCHET_RAIL_ATR": ("MIN_STOP_ATR", V3.MIN_STOP_ATR),
               "HARVEST_BAND": ("(TIDE_FAST, TIDE_SLOW)",
                                (V3.TIDE_FAST, V3.TIDE_SLOW))}
    new_nums, new_rules, repointed = [], [], []
    for k, v in RC.REGISTER_DIFF.items():
        val = v["value"]
        if k in REPOINT:
            src, want = REPOINT[k]
            good = val == want
            ok &= good
            repointed.append((k, val, src if good else f"{src} *** MISMATCH ***"))
        elif isinstance(val, (bool, str)):
            new_rules.append((k, val))
        elif isinstance(val, (int, float)):
            new_nums.append((k, val))
        else:
            new_rules.append((k, val))
    covered = len(new_nums) + len(new_rules) + len(repointed)
    good = covered == len(RC.REGISTER_DIFF)
    ok &= good
    lines.append(f"[{'OK ' if good else 'BAD'}] REGISTER_DIFF partitions "
                 f"EXHAUSTIVELY, derived from the register itself: "
                 f"{len(new_nums)} new numbers + {len(new_rules)} new named "
                 f"rules + {len(repointed)} re-pointed = {covered} of "
                 f"{len(RC.REGISTER_DIFF)} rows")
    for k, val in new_nums:
        lines.append(f"      NEW NUMBER   {k:26} = {val}")
    for k, val in new_rules:
        lines.append(f"      NEW RULE     {k:26} = {val!r}")
    for k, val, src in repointed:
        lines.append(f"      RE-POINTED   {k:26} = {val}  IS {src}")
    # AND EVERY ROW MUST BE READ BY THE DECISION PATH OR THE PROGRAM.
    # A register row nothing consults can drift from the code it claims to
    # govern with no fixture able to see it — the F-C3-e defect exactly. The
    # scan is over CODE (comments and docstrings stripped), because a row
    # mentioned only in a comment is a row nothing reads.
    dec = code_only((ROOT / "scripts" / "tierc4_rules.py").read_text())
    prg = code_only(prog_src)
    for k in RC.REGISTER_DIFF:
        used = (k in dec) or (k in prg)
        ok &= used
        lines.append(f"[{'OK ' if used else 'BAD'}] {k:26} is READ by the "
                     f"decision path or the program (not a row that governs "
                     f"nothing)")
    lines.append("")
    lines.append("UNCHANGED constants, re-read from the Tier-C3 register:")
    for k in ("UNIVERSE", "LENS", "TIDE_FAST", "TIDE_SLOW", "WINDOW_FAST",
              "WINDOW_SLOW", "TRIGGER_FAST", "TRIGGER_SLOW", "D_DISPLACEMENT",
              "D_STRIP", "ATR_LEN", "FEE_BPS_SIDE", "PIVOT_L", "PIVOT_R",
              "STOP_BUF_ATR", "MIN_STOP_ATR", "PIVOT_LOOKBACK_4H",
              "LEAD_IN_DAYS", "SEAL_FLOOR_ON_ANCHOR", "STRIP_TRUNCATE"):
        same = RC.REGISTER[k]["value"] == V3.REGISTER[k]["value"]
        ok &= same
        lines.append(f"[{'OK ' if same else 'BAD'}] {k:22} "
                     f"{RC.REGISTER[k]['value']}")
    # the (5,5) anchor shape and the (2,2) trail shape are DIFFERENT and both
    # come from the estate's ONE pivot function.
    good = (RC.PIVOT_L, RC.PIVOT_R) != (RC.RATCHET_PIVOT_L, RC.RATCHET_PIVOT_R)
    ok &= good
    lines.append(f"[{'OK ' if good else 'BAD'}] anchor shape "
                 f"({RC.PIVOT_L},{RC.PIVOT_R}) != trail shape "
                 f"({RC.RATCHET_PIVOT_L},{RC.RATCHET_PIVOT_R}) — two shapes, "
                 f"ONE definition: engine.s1._pivots on both")
    import inspect
    good = "_pivots" in inspect.getsource(RC.build_fractals_4h)
    ok &= good
    lines.append(f"[{'OK ' if good else 'BAD'}] build_fractals_4h calls "
                 f"engine.s1._pivots — the estate's pivot of record, not a "
                 f"second fractal implementation")
    # RETIRED rows stay retired one generation on
    dsrc = (inspect.getsource(V3.struct_stop_4h)
            + inspect.getsource(V3.build_pivots_4h)
            + inspect.getsource(RC.build_fractals_4h)
            + inspect.getsource(RC.ratchet_step))
    for k in RC.RETIRED_FROM_V1:
        dead = k not in dsrc
        ok &= dead
        lines.append(f"[{'OK ' if dead else 'BAD'}] {k:22} still RETIRED — "
                     f"absent from the v4 stop AND trail functions")
    # the 1H lens is not reachable from the v4 PROGRAM at all
    prog = (ROOT / "scripts" / "tierc4_baseline.py").read_text()
    good = "anchor_lens" not in prog and "build_pivots_1h" not in prog
    ok &= good
    lines.append(f"[{'OK ' if good else 'BAD'}] the retired 1H lens is not "
                 f"reachable from tierc4_baseline.py — v1's number is READ "
                 f"from its filed headline, never recomputed")
    # the toll is still DERIVED, never typed
    good = RC.FEE_BPS_ROUND_TRIP == 2 * RC.FEE_BPS_SIDE == 10.0
    ok &= good
    lines.append(f"[{'OK ' if good else 'BAD'}] toll = 2 x fee_bps_side = "
                 f"{RC.FEE_BPS_ROUND_TRIP} bps round trip — derived, not typed")
    # the corridor is HELD IDENTICAL two generations back
    good = TC.SCORED == T3.SCORED == TB.SCORED
    ok &= good
    lines.append(f"[{'OK ' if good else 'BAD'}] scored corridor held identical "
                 f"across v1/v3/v4: {TC.SCORED} — every cross-version delta is "
                 f"a delta in the CARD, not in the corridor")
    good = TC.PINNING[1] == "2026-07-07"
    ok &= good
    lines.append(f"[{'OK ' if good else 'BAD'}] F-7 truncation carried: "
                 f"PINNING -> {TC.PINNING[1]}")
    # ── RIDE-ONLY, PROVED AS AN OUTCOME AND NOT ONLY AS A CODE CLAIM ────────
    # The ENTRY half of `replay_asset` is a hand transcription of Tier-C3's,
    # not an import — the two amendments live inside the ride and the loop
    # around them had to be rewritten to carry them. An `is` check cannot reach
    # transcribed code, so the claim is made where it can be falsified: every
    # table this build produces that the ride cannot touch must come out
    # CONTENT-HASH-IDENTICAL to Tier-C3's filed one. If a single arming, tide
    # test, displacement, trigger, occupancy decision, anchor or entry stop had
    # drifted, one of these five hashes would move.
    lines.append("")
    lines.append("RIDE-ONLY, proved as an OUTCOME (the entry half is "
                 "transcribed, not imported — `is` cannot reach it):")
    m4 = json.loads((TC.OUT / "build_manifest.json").read_text())
    m3 = json.loads((TC.V3_TABLES / "build_manifest.json").read_text())
    for k in ("funnel", "lead_in_census", "lead_in_trades", "strip_d",
              "anchor_lookback"):
        a4, a3 = m4["sha"].get(k), m3["sha"].get(k)
        same = bool(a4) and a4 == a3
        ok &= same
        lines.append(f"[{'OK ' if same else 'BAD'}] {k:20} v4 {str(a4)[:16]} "
                     f"== v3 {str(a3)[:16]} — the ride cannot reach this table")
    lines.append("")
    lines.append("RULE CARD v4, verbatim:")
    lines += ["  " + x for x in RC.RULE_CARD_V4.splitlines()]
    return rec("F-C4-INHERIT", ok, lines)


# ══════════════════════ F-C4-RAIL · every stop, entry AND advanced
def f_rail() -> bool:
    """THE RAIL, ASSERTED PER STOP — entry stops against the entry close (the
    inherited v3 leg) and EVERY ADVANCED stop against its OWN confirming close
    (the new leg).  A trailing stop that quietly tightened inside the rail
    would be a card change nobody voted for."""
    lines, ok = [], True
    j = tbl("trade_journal")
    sg = tbl("stop_geometry")
    rl = tbl("ratchet_ledger")
    if not len(j):
        return rec("F-C4-RAIL", False, ["no scored trades"])

    lines.append(f"LEG 1 · THE ENTRY STOP (inherited, F-C3-RAIL). "
                 f"MIN_STOP_ATR = {RC.MIN_STOP_ATR}; {len(j)} scored trades, "
                 f"EVERY ONE asserted")
    lines.append(f"{'asset':9} {'entry':21} {'R':>14} {'ATR':>14} {'R/ATR':>9} "
                 f"{'pivot/ATR':>10} rail")
    for _, r in j.iterrows():
        atr, rd = float(r["atr_at_entry"]), float(r["r_dist"])
        ratio = rd / atr
        floor_ok = ratio >= RC.MIN_STOP_ATR - 1e-9
        d = 1 if r["direction"] == "long" else -1
        rail_stop = float(r["entry_px"]) - d * RC.MIN_STOP_ATR * atr
        pivot_stop = float(r["pivot_stop_px"])
        want = min(pivot_stop, rail_stop) if d == 1 else max(pivot_stop, rail_stop)
        stop_ok = abs(want - float(r["stop_px"])) < 1e-6
        rmax = max(float(r["pivot_dist"]), float(r["rail_dist"]))
        rmax_ok = abs(rmax - rd) < 1e-6
        bind_ok = bool(r["rail_binding"]) == (float(r["rail_dist"])
                                              > float(r["pivot_dist"]))
        good = floor_ok and stop_ok and rmax_ok and bind_ok
        ok &= good
        lines.append(f"[{'OK ' if good else 'BAD'}] {r['asset']:9} "
                     f"{r['entry_ts']:21} {rd:14.6f} {atr:14.6f} {ratio:9.6f} "
                     f"{float(r['pivot_dist'])/atr:10.6f} "
                     f"{'BINDING' if r['rail_binding'] else '-'}")
    mn = float(j["r_dist"].astype(float).div(j["atr_at_entry"].astype(float)).min())
    mx = float(j["r_dist"].astype(float).div(j["atr_at_entry"].astype(float)).max())
    lines.append(f"R/ATR range {mn:.6f} -> {mx:.6f}; floor {RC.MIN_STOP_ATR} "
                 f"MET BY EVERY TRADE. R is the ENTRY stop distance and the "
                 f"ratchet does NOT re-denominate it.")
    g1 = not bool(sg["under_c3_rail"].any())
    g2 = not bool(sg["under_g8c_rail"].any())
    ok &= g1 and g2
    lines.append(f"[{'OK ' if g1 else 'BAD'}] stop_geometry.under_c3_rail: "
                 f"{int(sg['under_c3_rail'].sum())} rows")
    lines.append(f"[{'OK ' if g2 else 'BAD'}] stop_geometry.under_g8c_rail: "
                 f"{int(sg['under_g8c_rail'].sum())} rows")

    lines.append("")
    lines.append(f"LEG 2 · EVERY ADVANCED STOP (new). RATCHET_RAIL_ATR = "
                 f"{RC.RATCHET_RAIL_ATR}; {len(rl)} advances, EVERY ONE "
                 f"asserted at PLACEMENT against its own confirming close.")
    if not len(rl):
        lines.append("     NO ADVANCES — the ratchet never fired on this "
                     "corridor. That is a finding, not a pass by vacuity, and "
                     "the build document states it as one.")
    else:
        lines.append(f"{'asset':9} {'conf':21} {'close':>13} {'ATR':>11} "
                     f"{'new stop':>13} {'dist/ATR':>9} bound")
        for _, r in rl.iterrows():
            d = 1 if r["direction"] == "long" else -1
            atr, cl = float(r["atr_at_conf"]), float(r["close_at_conf"])
            new = float(r["new_stop_px"])
            cand = float(r["cand_px"])
            rail = float(r["rail_px"])
            # (a) the rail floor is met at placement
            dist_ok = abs(cl - new) / atr >= RC.RATCHET_RAIL_ATR - 1e-9
            # (b) the candidate is the pivot offset by the card's own "beyond"
            cand_ok = abs(cand - (float(r["pivot_val"])
                                  - d * RC.RATCHET_BUF_ATR * atr)) < 1e-6
            # (c) the rail price is the close offset by the rail
            rail_ok = abs(rail - (cl - d * RC.RATCHET_RAIL_ATR * atr)) < 1e-6
            # (d) the stop taken is the FARTHER of the two
            want = min(cand, rail) if d == 1 else max(cand, rail)
            take_ok = abs(want - new) < 1e-6
            # (e) MONOTONE — it strictly improved on the standing stop
            mono_ok = (new > float(r["prev_stop_px"]) if d == 1
                       else new < float(r["prev_stop_px"]))
            # (f) rail_binding is arithmetic, not a label
            bind_ok = bool(r["rail_binding"]) == ((rail < cand) if d == 1
                                                  else (rail > cand))
            # (g) the stop is on the correct side of price at placement
            side_ok = (new < cl) if d == 1 else (new > cl)
            good = all((dist_ok, cand_ok, rail_ok, take_ok, mono_ok, bind_ok,
                        side_ok))
            ok &= good
            lines.append(f"[{'OK ' if good else 'BAD'}] {r['asset']:9} "
                         f"{r['conf_ts']:21} {cl:13.6f} {atr:11.6f} "
                         f"{new:13.6f} {abs(cl-new)/atr:9.6f} "
                         f"{'RAIL' if r['rail_binding'] else 'PIVOT'}")
            if not good:
                lines.append(f"        dist={dist_ok} cand={cand_ok} "
                             f"rail={rail_ok} taken={take_ok} mono={mono_ok} "
                             f"binding={bind_ok} side={side_ok}")
        dmin = float(rl["dist_from_close_atr"].astype(float).min())
        lines.append(f"advance distance from close, min {dmin:.6f} x ATR — "
                     f"floor {RC.RATCHET_RAIL_ATR} MET BY EVERY ADVANCE. "
                     f"rail bound on {int(rl['rail_binding'].sum())} of "
                     f"{len(rl)}; the pivot buffer bound on "
                     f"{int(rl['buffer_binding'].sum())}.")
        # MONOTONICITY ACROSS A CAMPAIGN, not only per advance
        bad = 0
        for (a_, e_), g in rl.groupby(["asset", "entry_ms"]):
            g = g.sort_values("advance_seq")
            d = 1 if g.iloc[0]["direction"] == "long" else -1
            s = g["new_stop_px"].astype(float).to_numpy()
            if len(s) > 1 and not ((np.diff(s) > 0).all() if d == 1
                                   else (np.diff(s) < 0).all()):
                bad += 1
        ok &= (bad == 0)
        lines.append(f"[{'OK ' if bad == 0 else 'BAD'}] RATCHET_MONOTONE across "
                     f"whole campaigns: {bad} campaign(s) where a stop "
                     f"retreated. Stops only advance, never retreat.")
    return rec("F-C4-RAIL", ok, lines)


# ═════════════ F-C4-PIVOT · three RATCHET fractals hand-verified on RAW bars
def f_pivot() -> bool:
    """THREE ADVANCES, END TO END, FROM RAW 4h BARS — chosen adversarially.

    The picks are: the advance that was PAID OUT (a stop that actually took a
    campaign's money), the LARGEST advance in ATR, and the advance on the trade
    carrying the most R — then the earliest as a filler, taken in that order
    until three DISTINCT advances are held.  Three is the contract.

    Each leg is re-derived from the raw 4h series: that the pivot IS a strict
    (2,2) fractal by the estate's own definition; that it confirmed at pivot
    bar + 2 and NOT before; that the advanced stop governs the NEXT bar (the
    causality leg — the stop derived from bar j's close is never tested against
    bar j's own low); the buffer; the rail; monotonicity; and, when the stop
    was paid out, that the exit bar really reached it.
    """
    lines, ok = [], True
    rl = tbl("ratchet_ledger")
    j = tbl("trade_journal")
    if not len(rl):
        return rec("F-C4-PIVOT", False,
                   ["NO ADVANCES to verify. The contract asks for three "
                    "hand-verified ratchet pivots and the corridor produced "
                    "none — the fixture FAILS rather than passing vacuously."])

    # THE PICKS — ONE PER CRITERION, IN TURN, NOT THREE DRAWS FROM ONE BUCKET.
    # The first draft appended EVERY paid-out advance before reaching the second
    # criterion, so with 8 paid-out rows the "largest advance" and "earliest"
    # criteria were unreachable dead code and the largest advance in the book
    # (a SUPERSEDED one, never paid out) was never verified. Found by the
    # post-build adversarial review. Now each criterion contributes its best
    # candidate first, so a SUPERSEDED advance is verified whenever one is the
    # largest — which exercises the branch that a paid-out-only sample cannot.
    def _key(r):
        return (r["asset"], int(r["entry_ms"]), int(r["advance_seq"]))

    paid = rl[rl["paid_out"]].sort_values("advance_atr", ascending=False)
    biggest = rl.sort_values("advance_atr", ascending=False)
    earliest = rl.sort_values("conf_ms")
    best_trade = j.sort_values("net_r", ascending=False)
    by_trade = pd.concat(
        [rl[(rl["asset"] == t["asset"]) & (rl["entry_ms"] == t["entry_ms"])]
         for _, t in best_trade.iterrows()]) if len(best_trade) else rl.iloc[0:0]
    criteria = [("PAID OUT, largest", paid), ("LARGEST advance", biggest),
                ("advance on the biggest-R trade", by_trade),
                ("EARLIEST advance", earliest)]
    picks: list[tuple] = []
    why: dict[tuple, str] = {}
    for label, frame in criteria:                 # one from each, in turn
        for _, r in frame.iterrows():
            k = _key(r)
            if k not in picks:
                picks.append(k)
                why[k] = label
                break
        if len(picks) == 3:
            break
    for _, r in rl.sort_values("conf_ms").iterrows():   # fillers, if needed
        if len(picks) == 3:
            break
        k = _key(r)
        if k not in picks:
            picks.append(k)
            why[k] = "filler (earliest unused)"
    n_want = min(3, len(rl))
    if len(picks) < n_want:
        return rec("F-C4-PIVOT", False,
                   [f"only {len(picks)} distinct advances; wanted {n_want}"])

    for sym, em, seq in picks:
        r = rl[(rl["asset"] == sym) & (rl["entry_ms"] == em)
               & (rl["advance_seq"] == seq)].iloc[0]
        t = j[(j["asset"] == sym) & (j["entry_ms"] == em)].iloc[0]
        dirn = 1 if r["direction"] == "long" else -1
        k4 = TC.load_klines(sym, "4h")
        hi = k4["high"].to_numpy(float)
        lo = k4["low"].to_numpy(float)
        f = RC.build_4h(k4["open_time"].to_numpy(np.int64),
                        k4["open"].to_numpy(float), hi, lo,
                        k4["close"].to_numpy(float))
        ot = f.open_ms
        ti = int(np.searchsorted(ot, int(em)))
        cj = int(np.searchsorted(ot, int(r["conf_ms"])))
        pb = int(np.searchsorted(ot, int(r["pivot_bar_ms"])))
        xi = int(np.searchsorted(ot, int(t["exit_ms"])))
        lines.append("")
        lines.append(f"ADVANCE  {sym} {r['direction']} #{int(seq)}  entry "
                     f"{t['entry_ts']}  confirm {r['conf_ts']}  "
                     f"{'PAID OUT' if r['paid_out'] else 'SUPERSEDED (never paid out)'}"
                     f"   [picked as: {why[(sym, em, seq)]}]")

        # 1 · THE FRACTAL IS STRICT (2,2) ON RAW BARS
        series = lo if dirn == 1 else hi
        L = series[pb - RC.RATCHET_PIVOT_L:pb]
        Rr = series[pb + 1:pb + 1 + RC.RATCHET_PIVOT_R]
        real = ((series[pb] < L.min() and series[pb] < Rr.min()) if dirn == 1
                else (series[pb] > L.max() and series[pb] > Rr.max()))
        val_ok = abs(float(series[pb]) - float(r["pivot_val"])) < 1e-9
        ok &= bool(real and val_ok)
        lines.append(f"  [{'OK ' if (real and val_ok) else 'BAD'}] pivot "
                     f"{float(r['pivot_val']):.6f} is a STRICT 4h "
                     f"({RC.RATCHET_PIVOT_L},{RC.RATCHET_PIVOT_R}) swing "
                     f"{'low' if dirn == 1 else 'high'} at "
                     f"{TC.iso(ot[pb])}")
        lines.append(f"        raw bars: prev2 {np.round(L, 6).tolist()}")
        lines.append(f"                  PIVOT {series[pb]:.6f}")
        lines.append(f"                  next2 {np.round(Rr, 6).tolist()}")

        # 2 · CONFIRMATION LAG — knowable at pivot bar + R, and NOT BEFORE.
        #     `cj == pb + R` alone is structural (the ledger DEFINES pivot_bar
        #     as conf - R), so the leg that carries the content is the second
        #     one: at every earlier as-of bar the right flank is incomplete, so
        #     the fractal literally does not exist yet. That is re-derived from
        #     raw bars and is falsifiable.
        conf_ok = cj == pb + RC.RATCHET_PIVOT_R
        early_ok = True
        for asof in range(pb, pb + RC.RATCHET_PIVOT_R):
            flank = series[pb + 1:asof + 1]          # what had closed by `asof`
            knowable = len(flank) >= RC.RATCHET_PIVOT_R
            early_ok &= not knowable
        ok &= bool(conf_ok and early_ok)
        lines.append(f"  [{'OK ' if conf_ok else 'BAD'}] close-confirmed at "
                     f"bar {pb} + {RC.RATCHET_PIVOT_R} = {cj} "
                     f"({TC.iso(ot[cj])})")
        lines.append(f"  [{'OK ' if early_ok else 'BAD'}] and NOT before: "
                     f"as of bars {pb}..{cj - 1} the right flank holds "
                     f"{[len(series[pb+1:a+1]) for a in range(pb, cj)]} of "
                     f"{RC.RATCHET_PIVOT_R} closed bars — the fractal does not "
                     f"exist yet at any of them")

        # 3 · IT IS A *NEW* PIVOT — the gate is on the CONFIRMATION bar, and the
        #     pivot BAR's position relative to entry is a NAMED READING (F-C4-i),
        #     measured here rather than assumed away.
        new_ok = cj > ti
        ok &= new_ok
        lines.append(f"  [{'OK ' if new_ok else 'BAD'}] confirmation bar {cj} > "
                     f"entry bar {ti} — the gate the card's word 'CONFIRMS' "
                     f"names. Its PIVOT BAR sits at {pb} = entry {'+' if pb >= ti else '-'}"
                     f"{abs(pb - ti)} bars; the gate would admit a pivot bar as "
                     f"early as entry - {RC.RATCHET_PIVOT_R} and NONE in this "
                     f"book is even at the entry (F-C4-i, disclosed, no ruling "
                     f"taken).")

        # 4 · CAUSALITY — RE-DERIVED, NOT RESTATED.
        #     The first draft of this leg compared `governs_from_ts` with
        #     `iso(conf_ms + 4h)`, which is how the column is WRITTEN: an
        #     identity that cannot fail for any implementation, acausal ones
        #     included. The post-build adversarial review called it, correctly.
        #     So the property is tested where it lives: replay the campaign's
        #     WHOLE stop schedule from the ledger over raw bars, applying each
        #     advance from conf + 1, and assert the exit bar and price come out
        #     as filed. Then replay it ACAUSALLY — each advance applied on its
        #     own confirming bar — and report whether that changes the exit.
        #     The second replay is the falsifier: if the two ever agree by
        #     construction rather than by data, this leg says so.
        sched = rl[(rl["asset"] == sym) & (rl["entry_ms"] == em)] \
            .sort_values("advance_seq")

        def _replay(offset: int):
            """offset=1 -> governs from conf+1 (causal, the card).
               offset=0 -> governs from conf   (acausal, the counterfactual)."""
            stop_c = float(t["stop_px"])
            nxt = [(int(np.searchsorted(ot, int(q["conf_ms"]))) + offset,
                    float(q["new_stop_px"])) for _, q in sched.iterrows()]
            for q in range(ti + 1, len(ot)):
                for gb, sp in nxt:
                    if q >= gb:
                        stop_c = sp
                if (lo[q] <= stop_c) if dirn == 1 else (hi[q] >= stop_c):
                    return q, stop_c
                if q >= xi:
                    return None, stop_c
            return None, stop_c

        c_bar, c_px = _replay(1)
        a_bar, a_px = _replay(0)
        causal_ok = (t["exit_reason"] != "stop"
                     or (c_bar == xi
                         and abs(c_px - float(t["exit_px"])) < 1e-6))
        ok &= bool(causal_ok)
        lines.append(f"  [{'OK ' if causal_ok else 'BAD'}] CAUSAL REPLAY from "
                     f"raw bars, advances applied from conf+1: exit bar "
                     f"{c_bar} @ {c_px:.6f} vs filed bar {xi} @ "
                     f"{float(t['exit_px']):.6f} ({t['exit_reason']})")
        differs = (a_bar != c_bar) or (abs((a_px or 0) - (c_px or 0)) > 1e-9)
        lines.append(f"       ACAUSAL counterfactual, same advances applied one "
                     f"bar EARLIER: exit bar {a_bar} @ {a_px:.6f} — "
                     f"{'DIFFERENT, so this leg can distinguish the two' if differs else 'IDENTICAL on this campaign, so this leg is not falsifying HERE; the discrimination it offers is data-dependent and is named rather than claimed'}")

        # 5 · THE BUFFER, THE RAIL, AND WHICH ONE THE CARD TOOK
        atr, cl = float(f.atr[cj]), float(f.c[cj])
        atr_ok = abs(atr - float(r["atr_at_conf"])) < 1e-6
        cl_ok = abs(cl - float(r["close_at_conf"])) < 1e-6
        cand = float(r["pivot_val"]) - dirn * RC.RATCHET_BUF_ATR * atr
        rail = cl - dirn * RC.RATCHET_RAIL_ATR * atr
        take = min(cand, rail) if dirn == 1 else max(cand, rail)
        take_ok = abs(take - float(r["new_stop_px"])) < 1e-6
        ok &= bool(atr_ok and cl_ok and take_ok)
        lines.append(f"  [{'OK ' if (atr_ok and cl_ok) else 'BAD'}] confirming "
                     f"bar close {cl:.6f}, ATR {atr:.6f} (ledger "
                     f"{r['close_at_conf']}, {r['atr_at_conf']})")
        lines.append(f"  [{'OK ' if take_ok else 'BAD'}] beyond = pivot "
                     f"{'-' if dirn == 1 else '+'} {RC.RATCHET_BUF_ATR}xATR = "
                     f"{cand:.6f}  |  rail = close "
                     f"{'-' if dirn == 1 else '+'} {RC.RATCHET_RAIL_ATR}xATR = "
                     f"{rail:.6f}  ->  TAKEN {take:.6f} "
                     f"({'RAIL' if r['rail_binding'] else 'PIVOT'})")

        # 6 · MONOTONE
        mono = (take > float(r["prev_stop_px"]) if dirn == 1
                else take < float(r["prev_stop_px"]))
        ok &= bool(mono)
        lines.append(f"  [{'OK ' if mono else 'BAD'}] advanced from "
                     f"{float(r['prev_stop_px']):.6f} -> {take:.6f} "
                     f"({float(r['advance_atr']):.6f} x ATR, favourable)")

        # 7 · IF IT WAS PAID OUT, THE EXIT BAR REALLY REACHED IT
        if bool(r["paid_out"]):
            hitv = lo[xi] if dirn == 1 else hi[xi]
            hit = (hitv <= take) if dirn == 1 else (hitv >= take)
            px_ok = abs(float(t["exit_px"]) - take) < 1e-6
            ok &= bool(hit and px_ok)
            lines.append(f"  [{'OK ' if (hit and px_ok) else 'BAD'}] PAID OUT: "
                         f"exit bar {TC.iso(ot[xi])} "
                         f"{'low' if dirn == 1 else 'high'} {hitv:.6f} reached "
                         f"the advanced stop {take:.6f}; journal exit px "
                         f"{t['exit_px']}")
            # and no EARLIER bar of the ride breached it while it governed
            seg = (lo[cj + 1:xi] if dirn == 1 else hi[cj + 1:xi])
            early = bool((seg <= take).any()) if dirn == 1 else bool((seg >= take).any())
            ok &= (not early)
            lines.append(f"  [{'OK ' if not early else 'BAD'}] no bar between "
                         f"the advance and the exit breached it first — the "
                         f"stop fired on the FIRST bar that reached it")
    return rec("F-C4-PIVOT", ok, lines)


# ══════════════════ F-C4-HARV · one harvest fill hand-reconciled
def f_harvest() -> bool:
    """ONE HARVEST, RECONCILED FROM RAW BARS AND RAW EMAs — plus the two
    campaign-wide invariants the card states: at most ONE harvest per campaign,
    and the halves summing to the campaign exactly."""
    lines, ok = [], True
    hl = tbl("harvest_ledger")
    j = tbl("trade_journal")
    lines.append(f"HARVEST_FRACTION = {RC.HARVEST_FRACTION} · band = "
                 f"{RC.HARVEST_BAND[0]}/{RC.HARVEST_BAND[1]} (the tide band, "
                 f"re-pointed) · fill = "
                 f"{RC.REGISTER['HARVEST_FILL']['value']} · max "
                 f"{RC.HARVEST_MAX_PER_CAMPAIGN} per campaign")
    if not len(hl):
        return rec("F-C4-HARV", False,
                   ["NO HARVEST FILLS to reconcile. The contract asks for one "
                    "hand-reconciled fill and the corridor produced none — the "
                    "fixture FAILS rather than passing vacuously."])

    # (1) THE HARVEST RULE, RE-DERIVED FROM RAW BARS ON EVERY CAMPAIGN.
    #
    # The obvious leg here — "`harvest_ledger` has no duplicate (asset,
    # entry_ms)" — CANNOT FAIL: the ledger emits at most one row per Trade, so
    # it is one-per-campaign by the shape of the writer and not by the ride
    # obeying the card. That tautology was the first draft of this fixture and
    # the post-build adversarial review called it a blocker, correctly.
    #
    # So the once-only and first-touch rules are tested where they live: for
    # EVERY scored campaign, rescan the ride bar by bar from the raw 4h series
    # and the raw EMAs, find the first bar whose own extreme reaches the band's
    # near edge, and assert the campaign's recorded fate matches:
    #     first touch strictly inside the ride  -> harvested THERE, once
    #     first touch on the exit bar           -> blocked_by = stop | bell
    #     no touch at all                       -> neither
    # A broken first-touch rule cannot survive this leg, and the partition is
    # asserted to be exhaustive rather than merely printed.
    hj = j[j["harvested"]]
    n_h = n_bs = n_bb = n_none = 0
    for _, r in j.iterrows():
        sym, dirn = r["asset"], (1 if r["direction"] == "long" else -1)
        k4 = TC.load_klines(sym, "4h")
        fr = RC.build_4h(k4["open_time"].to_numpy(np.int64),
                         k4["open"].to_numpy(float), k4["high"].to_numpy(float),
                         k4["low"].to_numpy(float), k4["close"].to_numpy(float))
        ot = fr.open_ms
        ti = int(np.searchsorted(ot, int(r["entry_ms"])))
        xi = int(np.searchsorted(ot, int(r["exit_ms"])))
        # the rescan mirrors the card INCLUDING its "from below" precondition:
        # a touch counts only once the campaign has closed on its own side of
        # the near edge. At bar ti+1 the last closed bar is the entry bar.
        first, armed = None, False
        for q in range(ti + 1, xi + 1):
            pe = RC.harvest_edge(float(fr.e89[q - 1]), float(fr.e316[q - 1]),
                                 dirn)
            if not armed and RC.harvest_outside(float(fr.c[q - 1]), pe, dirn):
                armed = True
            e = RC.harvest_edge(float(fr.e89[q]), float(fr.e316[q]), dirn)
            if armed and RC.harvest_touched(float(fr.h[q]), float(fr.l[q]),
                                            e, dirn):
                first = q
                break
        blocked = (r["harvest_blocked_by"]
                   if isinstance(r["harvest_blocked_by"], str) else None)
        if bool(r["harvested"]):
            n_h += 1
            led = hl[(hl["asset"] == sym)
                     & (hl["entry_ms"] == int(r["entry_ms"]))]
            want = (int(np.searchsorted(ot, int(led["harvest_ms"].iloc[0])))
                    if len(led) == 1 else -1)
            good = (len(led) == 1 and first is not None and first == want
                    and first < xi and blocked is None
                    and abs(float(fr.c[first])
                            - float(led["fill_px"].iloc[0])) < 1e-9)
            verdict = (f"harvested at the FIRST touch, bar {first} "
                       f"({TC.iso(ot[first]) if first is not None else '—'}), "
                       f"fill = that bar's close, exactly one ledger row")
        elif blocked in ("stop", "bell"):
            n_bs += int(blocked == "stop")
            n_bb += int(blocked == "bell")
            good = first is not None and first == xi
            verdict = (f"first touch fell on the EXIT bar {xi} "
                       f"({TC.iso(ot[xi])}) -> blocked_by={blocked}, no fill")
        else:
            n_none += 1
            good = first is None
            verdict = ("no ARMED bar of the ride reached the band -> no fill, "
                       "no block"
                       + ("" if bool(r["entered_outside_band"]) else
                          "  [entry was INSIDE the band: never armed]"))
        ok &= good
        lines.append(f"[{'OK ' if good else 'BAD'}] {sym:9} {r['entry_ts']:21} "
                     f"{verdict}")
    part_ok = (n_h + n_bs + n_bb + n_none) == len(j)
    ok &= part_ok
    lines.append(f"[{'OK ' if part_ok else 'BAD'}] the partition is EXHAUSTIVE "
                 f"and disjoint: {n_h} harvested + {n_bs} blocked-by-stop + "
                 f"{n_bb} blocked-by-bell + {n_none} never-touched == "
                 f"{len(j)} scored campaigns")
    good = len(hj) == len(hl) and n_h == len(hl)
    ok &= good
    lines.append(f"[{'OK ' if good else 'BAD'}] journal.harvested = {len(hj)} "
                 f"== harvest_ledger rows {len(hl)} == re-derived fills {n_h}")

    # (2) THE HALVES SUM TO THE CAMPAIGN, every harvested trade.
    #     TOLERANCE, STATED RATHER THAN CHOSEN: the three columns are written
    #     independently rounded to 6 dp, so their identity can only hold here to
    #     3 x 0.5e-6 = 1.5e-6 — and one campaign really does sit at 1.0e-6,
    #     which is rounding and nothing else. The EXACT identity is asserted at
    #     full float precision INSIDE the program (tierc4_baseline.account
    #     HALTs at 1e-9), so this leg tests the WRITTEN record against the
    #     precision it was written at, and the arithmetic is tested where the
    #     arithmetic happens.
    TOL = 2e-6
    bad, worst = 0, 0.0
    for _, r in hj.iterrows():
        s = float(r["net_r_harvest_half"]) + float(r["net_r_runner_half"])
        worst = max(worst, abs(s - float(r["net_r"])))
        if abs(s - float(r["net_r"])) > TOL:
            bad += 1
    ok &= (bad == 0)
    lines.append(f"[{'OK ' if bad == 0 else 'BAD'}] halves sum to the campaign: "
                 f"net_r_harvest_half + net_r_runner_half == net_r on all "
                 f"{len(hj)} harvested campaigns ({bad} outside {TOL:.0e}; "
                 f"worst |err| {worst:.2e} = 6-dp write rounding).")
    lines.append("     AND WHAT THAT DOES *NOT* SHOW, said plainly: the sum is "
                 "an ALGEBRAIC IDENTITY of how the program computes the three "
                 "columns (net is built from the same g/f/u terms the halves "
                 "are), so neither this leg nor the in-program 1e-9 HALT can "
                 "detect a WRONG SPLIT — they catch a wiring error and float "
                 "associativity, nothing more. The substantive claims — the "
                 "entry fee splits 50/50, each half pays its own exit fee, "
                 "funding accrues on the size actually held — are established "
                 "by the raw-bar reconciliation below, which recomputes both "
                 "halves from prices and funding stamps and is run on EVERY "
                 "fill. (Named after the post-build adversarial review pointed "
                 "out that the first draft presented the tautology as the "
                 "guarantee.)")
    # and an UNHARVESTED trade must carry NO half columns at all
    uj = j[~j["harvested"]]
    good = bool(uj["net_r_harvest_half"].isna().all()
                and uj["net_r_runner_half"].isna().all()) if len(uj) else True
    ok &= good
    lines.append(f"[{'OK ' if good else 'BAD'}] {len(uj)} unharvested campaigns "
                 f"carry NULL half columns — a half that did not happen is not "
                 f"booked as zero")

    # (3) THE HAND RECONCILIATION — EVERY fill, from raw bars.
    #     The first draft reconciled ONE fill (the largest by half move) and
    #     leaned on the halves-sum tautology for the rest. Since that tautology
    #     establishes nothing about the SPLIT, the raw-bar reconciliation is the
    #     only leg that does — so it runs on all of them. Named after the
    #     post-build adversarial review.
    for _, pick in hl.sort_values(
            "unit_move_at_harvest_r", key=lambda s: s.abs(),
            ascending=False).iterrows():
        sym, em = pick["asset"], int(pick["entry_ms"])
        t = j[(j["asset"] == sym) & (j["entry_ms"] == em)].iloc[0]
        dirn = 1 if pick["direction"] == "long" else -1
        k4 = TC.load_klines(sym, "4h")
        f = RC.build_4h(k4["open_time"].to_numpy(np.int64),
                        k4["open"].to_numpy(float), k4["high"].to_numpy(float),
                        k4["low"].to_numpy(float), k4["close"].to_numpy(float))
        ot = f.open_ms
        ti = int(np.searchsorted(ot, em))
        hj_i = int(np.searchsorted(ot, int(pick["harvest_ms"])))
        xi = int(np.searchsorted(ot, int(t["exit_ms"])))
        lines.append("")
        lines.append(f"HAND-RECONCILED FILL  {sym} {pick['direction']}  entry "
                     f"{t['entry_ts']}  harvest {pick['harvest_ts']} "
                     f"(+{int(pick['bars_after_entry'])} bars)  runner exit "
                     f"{pick['runner_exit_ts']} ({pick['runner_exit_reason']})")

        # (a) the band edge, from raw EMAs
        edge = RC.harvest_edge(float(f.e89[hj_i]), float(f.e316[hj_i]), dirn)
        e_ok = abs(edge - float(pick["band_edge_px"])) < 1e-6
        ok &= e_ok
        lines.append(f"  [{'OK ' if e_ok else 'BAD'}] band at the touch bar: "
                     f"e89={float(f.e89[hj_i]):.6f} e316={float(f.e316[hj_i]):.6f} "
                     f"-> NEAR edge ({'upper' if dirn == 1 else 'lower'}) = "
                     f"{edge:.6f} (ledger {pick['band_edge_px']})")
        # (b) the TOUCH is intrabar
        ext = float(f.l[hj_i]) if dirn == 1 else float(f.h[hj_i])
        t_ok = (ext <= edge) if dirn == 1 else (ext >= edge)
        ok &= bool(t_ok)
        lines.append(f"  [{'OK ' if t_ok else 'BAD'}] TOUCH is INTRABAR: bar "
                     f"{'low' if dirn == 1 else 'high'} {ext:.6f} "
                     f"{'<=' if dirn == 1 else '>='} edge {edge:.6f}")
        # (c) it is the FIRST such bar after entry
        first = None
        for q in range(ti + 1, hj_i + 1):
            e2 = RC.harvest_edge(float(f.e89[q]), float(f.e316[q]), dirn)
            x2 = float(f.l[q]) if dirn == 1 else float(f.h[q])
            if (x2 <= e2) if dirn == 1 else (x2 >= e2):
                first = q
                break
        f_ok = first == hj_i
        ok &= bool(f_ok)
        lines.append(f"  [{'OK ' if f_ok else 'BAD'}] it is the FIRST touch after "
                     f"entry: scanning bars {ti+1}..{hj_i} the first is "
                     f"{first} ({TC.iso(ot[first]) if first is not None else '—'})")
        # (d) the FILL is that bar's CLOSE — a different instant, and the card says so
        p_ok = abs(float(f.c[hj_i]) - float(pick["fill_px"])) < 1e-9
        ok &= p_ok
        lines.append(f"  [{'OK ' if p_ok else 'BAD'}] FILL is that bar's CLOSE "
                     f"{float(f.c[hj_i]):.6f} (ledger {pick['fill_px']}) — the "
                     f"touch and the fill are deliberately different instants")
        # (e) THE HALF'S OWN R, from raw prices + the register's toll + funding
        q = RC.HARVEST_FRACTION
        bps = RC.FEE_BPS_SIDE / 10_000.0
        entry_px, rd = float(t["entry_px"]), float(t["r_dist"])
        fill = float(f.c[hj_i])
        g1 = q * (fill - entry_px) * dirn
        fee1 = bps * q * (entry_px + fill)
        fund = TC.load_funding(sym)
        u1 = 0.0
        for jj in range(ti + 1, hj_i + 1):
            rate = fund.get(int(ot[jj]))
            if rate:
                u1 += rate * float(f.c[jj - 1]) * dirn * q
        n1 = (g1 - fee1 - u1) / rd
        n1_ok = abs(n1 - float(pick["net_r_harvest_half"])) < 1e-6
        ok &= n1_ok
        lines.append(f"  [{'OK ' if n1_ok else 'BAD'}] HARVEST HALF net R = "
                     f"[{q} x ({fill:.6f} - {entry_px:.6f}) x {dirn} = {g1:+.6f}] "
                     f"- fee {fee1:.6f} - funding {u1:+.6f}, all / R {rd:.6f} = "
                     f"{n1:+.6f}  (ledger {pick['net_r_harvest_half']})")
        # (f) THE RUNNER HALF, same treatment, and the two must sum to the campaign
        exit_px = float(t["exit_px"])
        g2 = (1 - q) * (exit_px - entry_px) * dirn
        fee2 = bps * (1 - q) * (entry_px + exit_px)
        u2 = 0.0
        for jj in range(ti + 1, xi + 1):
            rate = fund.get(int(ot[jj]))
            if rate:
                u2 += rate * float(f.c[jj - 1]) * dirn * (1 - q)
        n2 = (g2 - fee2 - u2) / rd
        n2_ok = abs(n2 - float(pick["net_r_runner_half"])) < 1e-6
        sum_ok = abs((n1 + n2) - float(t["net_r"])) < 1e-6
        ok &= bool(n2_ok and sum_ok)
        lines.append(f"  [{'OK ' if n2_ok else 'BAD'}] RUNNER HALF net R = "
                     f"[{1-q} x ({exit_px:.6f} - {entry_px:.6f}) x {dirn} = "
                     f"{g2:+.6f}] - fee {fee2:.6f} - funding {u2:+.6f}, / R = "
                     f"{n2:+.6f}  (ledger {pick['net_r_runner_half']})")
        lines.append(f"  [{'OK ' if sum_ok else 'BAD'}] {n1:+.6f} + {n2:+.6f} = "
                     f"{n1+n2:+.6f} == campaign net R {t['net_r']}")
    # (g) the blocked cases are NAMED, not lost
    man = json.loads((TC.OUT / "build_manifest.json").read_text())
    c = man["counts"]
    lines.append("")
    lines.append(f"     WITHIN-BAR ORDER, accounted: {c.get('harvests', 0)} "
                 f"fills · {c.get('harvest_blocked_by_stop', 0)} campaigns "
                 f"whose FIRST band touch fell on their STOP bar (adverse-first "
                 f"[F-4] takes the whole remainder) · "
                 f"{c.get('harvest_blocked_by_bell', 0)} on their BELL bar (a "
                 f"same-bar harvest is economically identical to the bell and "
                 f"is not recorded) · {c.get('never_touched_band', 0)} that "
                 f"never touched the band at all.")
    return rec("F-C4-HARV", ok, lines)


# ═══════ F-C4-SEAL · the mask over BOTH published prices, and every ms column
def f_seal() -> bool:
    """F-C3-a's semantics, INHERITED AND EXTENDED.

    v3 learned the hard way that a min/max-of-timestamps era test cannot see a
    sealed PRICE: the structural anchor is a price selected by name from one
    bar, published, used as the R denominator and paid out on a stop.  The
    RATCHET introduces a SECOND price of exactly that kind — the trailing pivot,
    published in `ratchet_ledger` and paid out when the advanced stop fires.  So
    it takes the same mask and gets the same fixture.
    """
    lines, ok = [], True
    j = tbl("trade_journal")
    rl = tbl("ratchet_ledger")
    lb0 = TC._ms(TC.LOCKBOX[0])
    lb1 = TC._ms(TC.LOCKBOX[1]) + TC.MS_1D - 1
    lo_s = TC._ms(TC.SCORED[0])
    hi_s = TC._ms(TC.SCORED[1]) + TC.MS_1D - 1
    lead_lo = lo_s - RC.LEAD_IN_DAYS * TC.MS_1D
    ceil_census = TC._ms("2024-07-01")
    lines.append(f"SEAL {TC.iso(lb0)} -> {TC.iso(lb1)} · floor on the ENTRY "
                 f"ANCHOR = {RC.SEAL_FLOOR_ON_ANCHOR} · floor on every RATCHET "
                 f"PIVOT = True (both are published prices paid out on a stop)")

    # (a) EVERY ENTRY ANCHOR, re-derived from raw bars and asserted unsealed
    lines.append("")
    lines.append("LEG 1 · THE ENTRY ANCHOR (inherited, F-C3-SEAL)")
    for _, r in j.iterrows():
        sym, anc = r["asset"], float(r["pivot_anchor"])
        k4 = TC.load_klines(sym, "4h")
        ot = k4["open_time"].to_numpy(np.int64)
        series = (k4["low"] if r["direction"] == "long"
                  else k4["high"]).to_numpy(float)
        ti = int(np.searchsorted(ot, int(r["entry_ms"])))
        cand = [int(p) for p in np.flatnonzero(
            np.isclose(series, anc, rtol=0, atol=1e-9)) if p + RC.PIVOT_R <= ti]
        bar = max(cand) if cand else -1
        stored = int(r["anchor_bar_ms"])
        agree = bar >= 0 and int(ot[bar]) == stored
        sealed = bool(lb0 <= stored <= lb1)
        good = agree and (not sealed) and (not bool(r["anchor_in_lockbox"]))
        ok &= good
        lines.append(f"  [{'OK ' if good else 'BAD'}] {sym:9} {r['entry_ts']:21} "
                     f"anchor {anc:14.6f} from {TC.iso(stored):21} "
                     f"{'SEALED' if sealed else 'no'}"
                     f"{'' if agree else '  (STORED BAR DISAGREES WITH RAW)'}")
    n_sealed = int(j["anchor_in_lockbox"].sum())
    ok &= (n_sealed == 0)
    lines.append(f"  [{'OK ' if n_sealed == 0 else 'BAD'}] anchors quoted from "
                 f"a sealed bar: {n_sealed} of {len(j)}")
    man = json.loads((TC.OUT / "build_manifest.json").read_text())
    lines.append(f"     armings refused because EVERY reachable anchor was "
                 f"sealed: {man['counts'].get('armings_refused_anchor_sealed', 0)}")

    # (b) EVERY RATCHET PIVOT, resolved back to its own bar from raw bars
    lines.append("")
    lines.append(f"LEG 2 · EVERY RATCHET PIVOT ({len(rl)} advances) — NEW")
    n_bad = 0
    for _, r in rl.iterrows():
        sym = r["asset"]
        k4 = TC.load_klines(sym, "4h")
        ot = k4["open_time"].to_numpy(np.int64)
        series = (k4["low"] if r["direction"] == "long"
                  else k4["high"]).to_numpy(float)
        pb = int(np.searchsorted(ot, int(r["pivot_bar_ms"])))
        val_ok = abs(float(series[pb]) - float(r["pivot_val"])) < 1e-9
        sealed = bool(lb0 <= int(r["pivot_bar_ms"]) <= lb1)
        good = val_ok and not sealed and not bool(r["pivot_bar_in_lockbox"])
        if not good:
            n_bad += 1
            lines.append(f"  [BAD] {sym} {r['conf_ts']} pivot "
                         f"{r['pivot_val']} bar {r['pivot_bar_ts']} "
                         f"val_ok={val_ok} sealed={sealed}")
    ok &= (n_bad == 0)
    lines.append(f"  [{'OK ' if n_bad == 0 else 'BAD'}] every advance's pivot "
                 f"resolved to its own raw bar and NONE is sealed "
                 f"({n_bad} bad of {len(rl)}).")
    if len(rl):
        lines.append(f"     earliest ratchet pivot bar {rl['pivot_bar_ts'].min()}; "
                     f"the seal closes {TC.iso(lb1)}. The mask CANNOT bind here "
                     f"— every ratchet pivot confirms strictly after an entry "
                     f"that is itself at or after {TC.SCORED[0]} — and the mask "
                     f"is applied anyway, because a rule that is safe only by "
                     f"arithmetic accident is the F-C3-a defect exactly.")

    # (c) EVERY ms COLUMN OF EVERY FILED TABLE — enumerated, not curated
    lines.append("")
    lines.append("LEG 3 · EVERY ms/ts COLUMN OF EVERY FILED TABLE, DISCOVERED "
                 "(not a hand-written tuple — that is a test that passes by "
                 "construction)")
    LEAD_OK = {"arm_ms", "arm_time", "v3_arm_ts", "v4_arm_ts"}
    ANCHOR = {"anchor_bar_ms", "pivot_bar_ms"}
    for p in sorted(TC.OUT.glob("*.parquet")):
        d = pd.read_parquet(p)
        if not len(d):
            lines.append(f"      {p.stem:28} EMPTY — no timestamp to place")
            continue
        for c in d.columns:
            if not (c.endswith("_ms") or c == "ts"):
                continue
            v = pd.to_numeric(d[c], errors="coerce").dropna()
            v = v[v > 0]
            if not len(v):
                continue
            mn, mx = int(v.min()), int(v.max())
            in_lb = bool(((v >= lb0) & (v <= lb1)).any())
            n_lb = int(((v >= lb0) & (v <= lb1)).sum())
            pre = int((v < lo_s).sum())
            if c in LEAD_OK:
                good = not (v < lead_lo).any()
                verdict = (f"LEAD-IN LICENSED (F-5): {pre} row(s) pre-corridor, "
                           f"{n_lb} inside the SEAL — arming state, no outcome "
                           f"is computed there")
            elif c in ANCHOR:
                good = not in_lb
                verdict = (f"PUBLISHED-PRICE PROVENANCE: {n_lb} sealed — the "
                           f"seal floor forbids any")
            else:
                good = (lo_s <= mn and mx <= hi_s and not in_lb
                        and mn >= ceil_census)
                verdict = (f"in-scored={lo_s <= mn and mx <= hi_s} "
                           f"lockbox-free={not in_lb} "
                           f"after-census-ceiling={mn >= ceil_census}")
            ok &= good
            lines.append(f"  [{'OK ' if good else 'BAD'}] {p.stem}.{c:22} "
                         f"min={TC.iso(mn)} max={TC.iso(mx)}  {verdict}")

    # (d) the lead-in table carries NO outcome, whatever else it carries
    li = tbl("lead_in_trades")
    banned = [c for c in li.columns
              if any(t in c for t in ("net_r", "gross_r", "_px", "r_dist",
                                      "fee", "funding", "atr"))]
    good = not banned
    ok &= good
    lines.append("")
    lines.append(f"  [{'OK ' if good else 'BAD'}] lead_in_trades: {len(li)} "
                 f"row(s), NO outcome column — banned-name scan "
                 f"{banned or 'none'}")

    # (e) F-7 — the display-only strips truncate at VR-1's forward edge
    edge = TC._ms("2026-07-07") + TC.MS_1D - 1
    for w in ("CENSUS_ERA", "PINNING"):
        b = man["windows"][w].get("trade_ts_bounds")
        if not b:
            continue
        good = int(b["max_exit_ms"]) <= edge
        ok &= good
        lines.append(f"  [{'OK ' if good else 'BAD'}] F-7 {w}: entries "
                     f"{b['min_entry']} -> {b['max_entry']}, last exit "
                     f"{b['max_exit']} <= {TC.iso(edge)} (VR-1 forward edge)")
    # (f) THE ONE DELIBERATE SEAL READ, NAMED — because the blanket sentence
    #     this fixture used to print was FALSE, and false in the one way a
    #     timestamp test can never catch: the ablation table has no timestamp
    #     column, so LEG 3 above is structurally blind to it. The BOTH_NOSEAL
    #     cell runs the card WITHOUT the mask (that is its whole purpose — the
    #     "printed both ways" the card promises) and therefore quotes a sealed
    #     bar. Found by the post-build adversarial review.
    ab = tbl("ablation_unscored").set_index("cell")
    masked = [c for c in ab.index if bool(ab.loc[c, "seal_floor"])]
    unmasked = [c for c in ab.index if not bool(ab.loc[c, "seal_floor"])]
    g1 = all(int(ab.loc[c, "anchors_in_lockbox"]) == 0 for c in masked)
    g2 = unmasked == ["BOTH_NOSEAL"]
    g3 = int(ab.loc["BOTH_NOSEAL", "anchors_in_lockbox"]) > 0
    ok &= bool(g1 and g2 and g3)
    lines.append("")
    lines.append(f"  [{'OK ' if g1 else 'BAD'}] every MASKED ablation cell "
                 f"{masked} has anchors_in_lockbox = 0")
    lines.append(f"  [{'OK ' if g2 else 'BAD'}] exactly ONE cell is deliberately "
                 f"unmasked: {unmasked}")
    lines.append(f"  [{'OK ' if g3 else 'BAD'}] and it DOES read the seal — "
                 f"{int(ab.loc['BOTH_NOSEAL','anchors_in_lockbox'])} anchor(s) "
                 f"quoted from a sealed bar, {int(ab.loc['BOTH_NOSEAL','n'])} "
                 f"campaigns vs {int(ab.loc['BOTH','n'])} shipped. A cell that "
                 f"is supposed to show the unmasked card and reads nothing "
                 f"sealed would be showing nothing.")
    lines.append(f"      SEALED LOCKBOX {TC.iso(lb0)} -> {TC.iso(lb1)} — NOT "
                 f"COMPUTED. NO OUTCOME AND NO PUBLISHED PRICE IN THE SHIPPED "
                 f"CARD is drawn from a bar inside it. THE ONE EXCEPTION IN "
                 f"THIS BUILD is the BOTH_NOSEAL ablation cell above, which "
                 f"exists to print the seal floor BOTH WAYS (F-C3-a), is "
                 f"UNSCORED, is named in the manifest under `seal_read`, and is "
                 f"the number the operator gets if they overturn the floor.")
    return rec("F-C4-SEAL", ok, lines)


# ═══════════════ F-C4-ABLATE · the fork reproduces its parent, exactly
def f_ablate() -> bool:
    """THE ABLATION, AND THE REPRODUCTION THAT MAKES IT TRUSTWORTHY.

    The V3 cell rides Tier-C3's card through the Tier-C4 program.  If it does
    not reproduce Tier-C3's FILED net R to the last decimal, every other cell's
    difference is measuring the fork rather than the amendment, and the whole
    ablation is worthless.
    """
    lines, ok = [], True
    a = tbl("ablation_unscored").set_index("cell")
    v3j = pd.read_parquet(TC.V3_TABLES / "trade_journal.parquet")
    filed = float(v3j["net_r"].astype(float).sum())
    mine = float(a.loc["V3", "net_r"])
    good = abs(filed - mine) < 1e-3 and int(a.loc["V3", "n"]) == len(v3j)
    ok &= good
    lines.append(f"[{'OK ' if good else 'BAD'}] THE V3 CELL REPRODUCES TIER-C3 "
                 f"IN AGGREGATE: filed net R {filed:+.4f} over {len(v3j)} "
                 f"trades vs this program's {mine:+.4f} over "
                 f"{int(a.loc['V3','n'])} — |diff| = {abs(filed - mine):.2e}")
    # AND PER TRADE — because an aggregate check with a 1e-3 tolerance passes
    # on offsetting per-trade drift, and the sentence that follows it ("so
    # every marginal is the amendment, not the fork") would then be false while
    # the fixture printed PASS. The program HALTs on this join; the fixture
    # re-asserts it against the WRITTEN delta table, where `v3_cell_net_r` is
    # the cell's per-trade figure and `v3_net_r` is Tier-C3's filed one.
    # Found by the post-build adversarial review.
    d = tbl("delta_v3_v4")
    have = d[d["v3_cell_net_r"].notna() & d["v3_net_r"].notna()]
    nulls = int(d["v3_cell_net_r"].isna().sum())
    worst = (float((have["v3_cell_net_r"].astype(float)
                    - have["v3_net_r"].astype(float)).abs().max())
             if len(have) else float("inf"))
    per_ok = (len(have) == len(v3j)) and nulls == 0 and worst < 1e-4
    ok &= per_ok
    lines.append(f"[{'OK ' if per_ok else 'BAD'}] AND TRADE BY TRADE: "
                 f"{len(have)} of {len(v3j)} filed campaigns joined 1:1 with "
                 f"the cell, {nulls} null, max |per-trade diff| "
                 f"{worst:.2e} < 1e-4")
    lines.append("     so every marginal below is the AMENDMENT, not the fork.")
    lines.append("")
    lines.append(f"{'cell':9} {'ratch':>6} {'harv':>5} {'n':>3} {'net R':>9} "
                 f"{'exp':>8} {'win%':>7} {'maxDD':>8} {'adv':>4} {'hv':>3} "
                 f" marginal vs V3")
    for c in ("V3", "RATCHET", "HARVEST", "BOTH", "BOTH_NOSEAL"):
        r = a.loc[c]
        m = "" if pd.isna(r["marginal_net_r"]) else f"{r['marginal_net_r']:+.4f}"
        lines.append(f"{c:9} {str(r['ratchet']):>6} {str(r['harvest']):>5} "
                     f"{int(r['n']):3} {r['net_r']:+9.4f} "
                     f"{r['expectancy_r']:+8.4f} {r['win_rate_pct']:7.2f} "
                     f"{r['max_dd_r']:8.4f} {int(r['n_advances']):4} "
                     f"{int(r['n_harvests']):3}  {m}")
    inter = a.loc["BOTH", "interaction_net_r"]
    lines.append("")
    lines.append(f"NOT ADDITIVE, AND THE TABLE SAYS SO: BOTH - RATCHET - "
                 f"HARVEST + V3 = {float(inter):+.4f} R. The two amendments "
                 f"share one ride — a ratchet stop can end a campaign BEFORE "
                 f"its band touch, so the harvest's contribution is not the "
                 f"same number in the presence of the trail.")
    lines.append("UNSCORED. This is the 'tune later' substrate the operator "
                 "asked for, and the sentence that rides with it is: TUNING "
                 "LATER MEANS DECLARING m FIRST. No cell here may be promoted; "
                 "the ratified card is BOTH and was chosen before this table "
                 "existed.")
    # the shipped cell must BE the shipped run
    h = tbl("headline")
    hr = h[(h["group"] == "ALL") & (h["key"] == "ALL")].iloc[0]
    good = (abs(float(a.loc["BOTH", "net_r"]) - float(hr["net_r"])) < 1e-4
            and int(a.loc["BOTH", "n"]) == int(hr["n"]))
    ok &= good
    lines.append("")
    lines.append(f"[{'OK ' if good else 'BAD'}] the BOTH cell IS the shipped "
                 f"run: {a.loc['BOTH','net_r']:+.4f} / {int(a.loc['BOTH','n'])} "
                 f"== headline {float(hr['net_r']):+.4f} / {int(hr['n'])}")
    return rec("F-C4-ABLATE", ok, lines)


# ════════════════════════════════════════════════════ F-C4-DET · determinism
def f_determinism() -> bool:
    lines = []
    a = json.loads((TC.OUT / "build_manifest.json").read_text())
    p2 = TC.OUT_RERUN / "build_manifest.json"
    if not p2.exists():
        return rec("F-C4-DET", False, ["re-run manifest absent — run --rerun first"])
    b = json.loads(p2.read_text())
    ok = True
    for k in sorted(a["sha"]):
        same = a["sha"][k] == b["sha"].get(k)
        ok &= same
        lines.append(f"[{'OK ' if same else 'BAD'}] {k:22} {a['sha'][k][:32]}")
    same = a["counts"] == b["counts"]
    ok &= same
    lines.append(f"[{'OK ' if same else 'BAD'}] counts block identical: "
                 f"{json.dumps(a['counts'], sort_keys=True)}")
    same = a.get("selection_guard") == b.get("selection_guard")
    ok &= same
    lines.append(f"[{'OK ' if same else 'BAD'}] selection-guard verdict "
                 f"identical across runs")
    lines.append("")
    lines.append("NORMALIZATION DISCLOSURE — normalized fields: ['elapsed_s'] "
                 "(wall clock) and the output ROOT path. NO computed value is "
                 "normalized: every table, count, hash and R figure is compared "
                 "content-for-content.")
    lines.append(f"seed {TC.SEED} is printed and unused — no stochastic step "
                 f"exists in this program, so determinism is structural.")
    return rec("F-C4-DET", ok, lines)


# ═══════════════════════════ F-C4-6 · captured-not-consulted (Amendment B1)
def f_no_consultation() -> bool:
    """The decision path imports no registry symbol — proven four ways, over
    the v4 module AND the two it inherits from."""
    lines, ok = [], True
    srcs = {f"scripts/{n}.py": (ROOT / "scripts" / f"{n}.py").read_text()
            for n in ("tierc4_rules", "tierc3_rules", "tierc2_rules")}

    for name, src in srcs.items():
        imported: list[str] = []
        for node in ast.walk(ast.parse(src)):
            if isinstance(node, ast.Import):
                imported += [al.name for al in node.names]
            elif isinstance(node, ast.ImportFrom):
                imported.append(node.module or "")
        hits = [m for m in imported if m == "analytics" or m.startswith("analytics.")]
        g = not hits
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] AST import scan of {name}: "
                     f"{sorted(set(imported))} — analytics hits = {hits}")

    import tierc4_rules  # noqa: F401
    seen, stack = set(), ["tierc4_rules"]
    while stack:
        m = stack.pop()
        if m in seen:
            continue
        seen.add(m)
        mod = sys.modules.get(m)
        if mod is None:
            continue
        for v in vars(mod).values():
            n = getattr(v, "__name__", None) if isinstance(v, type(sys)) else None
            if n and n not in seen:
                stack.append(n)
    bad = sorted(m for m in seen if m == "analytics" or m.startswith("analytics."))
    g2 = not bad
    ok &= g2
    lines.append(f"[{'OK ' if g2 else 'BAD'}] transitive import closure of "
                 f"tierc4_rules: {len(seen)} modules, analytics members = {bad}")
    proj = {"engine", "tierc4_rules", "tierc3_rules", "tierc2_rules"}
    lines.append(f"    closure (project modules only): "
                 f"{sorted(m for m in seen if m.split('.')[0] in proj)}")

    eng = [p.name for p in (ROOT / "engine").glob("*.py")
           if "import analytics" in p.read_text() or "from analytics" in p.read_text()]
    g3 = not eng
    ok &= g3
    lines.append(f"[{'OK ' if g3 else 'BAD'}] engine/ modules importing "
                 f"analytics: {eng}  (invariant I-B, analytics/INTERFACE.md — "
                 f"so the closure cannot reach a registry symbol by any path)")

    tape_cols = ["wall_family", "dist_atr", "coloc_n", "nearest_level",
                 "rvwap", "avwap", "prior_extreme"]
    code = {n: code_only(s) for n, s in srcs.items()}
    named = {n: [c for c in tape_cols if c in s] for n, s in code.items()}
    g4 = not any(named.values())
    ok &= g4
    lines.append(f"[{'OK ' if g4 else 'BAD'}] tape column names appearing in "
                 f"the decision path's CODE (comments and docstrings stripped "
                 f"by AST round-trip, ordinary string literals KEPT): {named}")
    raw = {n: [c for c in tape_cols if c in s] for n, s in srcs.items()}
    lines.append(f"     the same scan over RAW TEXT would report {raw} — prose "
                 f"about a tape column is not a read of one, and Tier-C3's "
                 f"fixture already recorded that failure mode for the IMPORT "
                 f"leg while leaving this leg on raw text. It duly fired on "
                 f"this build's own explanatory comment. Hardened here.")

    tp = tbl("analytics_tape")
    lines.append(f"    tape CAPTURED: {len(tp):,} rows over "
                 f"{TC.iso(int(tp['ts'].min()))} -> {TC.iso(int(tp['ts'].max()))}, "
                 f"instants {tp['instant'].value_counts().to_dict()}")
    lines.append(f"    Q6c: this is now a THIRD unconditioned population of "
                 f"fills over the same corridor, and the harvest adds a new "
                 f"instant class to the location record. Nothing here "
                 f"conditions on a tape column.")
    return rec("F-C4-6", ok, lines)


# ════════════════════════════════════════════════════════ F-KEY · every join
def f_keys() -> bool:
    """Re-asserted against the WRITTEN tables, not only inside the program."""
    lines, ok = [], True
    keys = {"funnel": ["asset", "direction"],
            "headline": ["group", "key"],
            "headline_triptych": ["version"],
            "monthly_equity": ["month"],
            "stop_geometry": ["asset", "entry_ms"],
            "trade_journal": ["asset", "entry_ms"],
            "ratchet_ledger": ["asset", "entry_ms", "advance_seq"],
            "harvest_ledger": ["asset", "entry_ms"],
            "delta_v3_v4": ["asset", "direction", "arm_ms"],
            "ablation_unscored": ["cell"],
            "anchor_lookback_disclosure": ["asset", "entry_ms"],
            "lead_in_trades": ["asset", "entry_ms"],
            "strip_d_unscored": ["population", "d"],
            "display_only_strips": ["window", "group", "key"],
            "analytics_tape": ["asset", "ts"],
            "tape_inventory": ["instant", "column"]}
    for name, k in keys.items():
        d = tbl(name)
        dup = int(d.duplicated(subset=k).sum()) if len(d) else 0
        good = dup == 0
        ok &= good
        lines.append(f"[{'OK ' if good else 'BAD'}] {name:28} key={k} "
                     f"rows={len(d):,} dup={dup}")
    f = tbl("funnel")
    checks = [
        ("armings_seen == in_window + lead_in",
         (f["armings_seen"] == f["armings_in_window"] + f["armings_lead_in"]).all()),
        ("passed_tide == seen - leak_tide",
         (f["passed_tide"] == f["armings_seen"] - f["leak_tide"]).all()),
        ("passed_d == passed_tide - leak_d",
         (f["passed_d"] == f["passed_tide"] - f["leak_d"]).all()),
        ("triggered == passed_d - leak_no_trigger",
         (f["triggered"] == f["passed_d"] - f["leak_no_trigger"]).all()),
        ("entered == triggered - (open+anchor+sealed+degenerate)",
         (f["entered"] == f["triggered"] - f["leak_position_open"]
          - f["leak_no_struct_anchor"] - f["leak_anchor_sealed"]
          - f["leak_degenerate_R"]).all()),
        ("entered == entered_scored + entered_lead_in",
         (f["entered"] == f["entered_scored"] + f["entered_lead_in"]).all()),
    ]
    for name, good in checks:
        ok &= bool(good)
        lines.append(f"[{'OK ' if good else 'BAD'}] funnel reconciles: {name}")
    j, li = tbl("trade_journal"), tbl("lead_in_trades")
    good = int(f["entered"].sum()) == len(j) + len(li)
    ok &= good
    lines.append(f"[{'OK ' if good else 'BAD'}] entered {int(f['entered'].sum())} "
                 f"== scored trades {len(j)} + unscored lead-in trades {len(li)}")
    h = tbl("headline")
    a = h[(h["group"] == "ALL") & (h["key"] == "ALL")].iloc[0]
    good = abs(float(a["net_r"]) - float(j["net_r"].astype(float).sum())) < 1e-4
    ok &= good
    lines.append(f"[{'OK ' if good else 'BAD'}] headline net_r "
                 f"{float(a['net_r']):.4f} == sum(journal.net_r) "
                 f"{float(j['net_r'].astype(float).sum()):.4f}; n={int(a['n'])} "
                 f"== {len(j)}")
    # ── THE v4 LEDGER IDENTITIES ──────────────────────────────────────────
    rl, hl = tbl("ratchet_ledger"), tbl("harvest_ledger")
    good = len(rl) == int(j["n_advances"].astype(int).sum())
    ok &= good
    lines.append(f"[{'OK ' if good else 'BAD'}] ratchet_ledger rows {len(rl)} "
                 f"== sum(journal.n_advances) "
                 f"{int(j['n_advances'].astype(int).sum())}")
    good = len(hl) == int(j["harvested"].sum())
    ok &= good
    lines.append(f"[{'OK ' if good else 'BAD'}] harvest_ledger rows {len(hl)} "
                 f"== journal.harvested {int(j['harvested'].sum())}")
    if len(rl):
        # the final advance of a campaign must BE the journal's final stop
        fin = rl[rl["is_final_stop"]].set_index(["asset", "entry_ms"])
        bad = 0
        for _, r in j.iterrows():
            k = (r["asset"], int(r["entry_ms"]))
            if int(r["n_advances"]) == 0:
                if abs(float(r["final_stop_px"]) - float(r["stop_px"])) > 1e-9:
                    bad += 1
            elif k in fin.index:
                if abs(float(fin.loc[k, "new_stop_px"])
                       - float(r["final_stop_px"])) > 1e-9:
                    bad += 1
            else:
                bad += 1
        ok &= (bad == 0)
        lines.append(f"[{'OK ' if bad == 0 else 'BAD'}] journal.final_stop_px "
                     f"== the campaign's LAST advance (or its entry stop when "
                     f"there was none): {bad} mismatch")
    # the delta table's give-back decomposition is an identity, not an opinion
    d = tbl("delta_v3_v4")
    both = d[(d["present"] == "both") & d["giveback_v3_r"].notna()]
    if len(both):
        err = (both["captured_r"].astype(float)
               + both["surrendered_r"].astype(float)
               - both["giveback_v3_r"].astype(float)).abs().max()
        good = err < 1e-5
        ok &= good
        lines.append(f"[{'OK ' if good else 'BAD'}] give-back columns are "
                     f"self-consistent on all {len(both)} shared armings: "
                     f"captured_r + surrendered_r == giveback_v3_r "
                     f"(max |err| {err:.2e})")
        lines.append("     THIS IS A TAUTOLOGY AND IS LABELLED AS ONE. "
                     "captured = v4 - v3 and surrendered = mfe3 - v4, so v4 "
                     "cancels and the sum is mfe3 - v3 = giveback for ANY v4 "
                     "whatsoever. It catches a wiring or rounding error and "
                     "nothing else; it is NOT evidence about the amendments. "
                     "The only one of the three columns that carries "
                     "information about v4 is captured_r. (Labelled after the "
                     "post-build adversarial review found the first draft "
                     "presenting it as a verified identity.)")
    # the triptych's v4 row must be this build's own headline
    tp = tbl("headline_triptych").set_index("version")
    good = (abs(float(tp.loc["v4", "net_r"]) - float(a["net_r"])) < 1e-4
            and int(tp.loc["v4", "n"]) == int(a["n"]))
    ok &= good
    lines.append(f"[{'OK ' if good else 'BAD'}] triptych v4 row "
                 f"{tp.loc['v4','net_r']:+.4f}/{int(tp.loc['v4','n'])} == this "
                 f"build's headline; v1 and v3 rows are READ from "
                 f"{tp.loc['v1','source']} and {tp.loc['v3','source']}, never "
                 f"recomputed")
    return rec("F-KEY", ok, lines)


# ════════════════════════════════════════════════════════════════ main
def main() -> int:
    print("=" * 78)
    print("TIER-C4 FIXTURE TRANSCRIPT — THE MEAN CARD")
    print("=" * 78)
    f_gates()
    f_inherit()
    f_rail()
    f_pivot()
    f_harvest()
    f_seal()
    f_ablate()
    f_determinism()
    f_no_consultation()
    f_keys()

    print("\n".join(T))
    n_ok = sum(RESULTS.values())
    print()
    print("=" * 78)
    print(f"FIXTURE SUMMARY  {n_ok}/{len(RESULTS)} PASS  {json.dumps(RESULTS)}")
    print(f"  I9: ANALYTICS_VERSION {AN.ANALYTICS_VERSION} · analytics_sha "
          f"{AN.analytics_sha()}")
    print("=" * 78)
    if n_ok < len(RESULTS):
        print("*** HALT: fixture mismatch. Nothing downstream is trustworthy. ***")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
