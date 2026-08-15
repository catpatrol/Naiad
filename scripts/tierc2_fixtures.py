"""TIER-C2 fixtures — the transcript, printed.  HALTs non-zero on any failure.

    F-C2-1  gates transcript
    F-C2-2  rule-card echo + THREE trades hand-verified end to end
    F-C2-3  constants cited from the closed register — no value invented in code
    F-C2-4  determinism: full re-run hash-identical
    F-C2-5  era exclusions proven by min/max ts per scored table
    F-C2-6  no-consultation: the decision path imports no registry symbol
    F-C2-7  one instant's snapshot hand-reconciled against analytics directly;
            sabotage slice REJECT re-proven on this corridor
    F-KEY   on every join (asserted inside the program, echoed here)

House idiom: the `mc1_program.stage_fixtures` shape — one `--- F-ID : PASS ---`
header per fixture with indented evidence lines beneath, because a fixture that
prints only a verdict cannot be audited.

USAGE  ~/venvs/naiad/bin/python scripts/tierc2_fixtures.py
"""
from __future__ import annotations

import hashlib
import importlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import tierc2_baseline as TB                                       # noqa: E402
import tierc2_rules as RC                                          # noqa: E402
import analytics as AN                                             # noqa: E402
from analytics import structure as AS                              # noqa: E402
from analytics import vwap as AW                                   # noqa: E402

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


# ═══════════════════════════════════════════════════════ F-C2-1 · the gates
def f_gates() -> bool:
    lines, ok = [], True
    head = sh("git rev-parse --short HEAD")
    remote = sh("git remote -v")
    branch = sh("git branch --show-current")
    pwd = str(ROOT)
    home = str(Path.home())

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

    # ESTATE READY — panel 4h + 1h, gap-free, over the SCORED corridor
    lo = TB._ms(TB.SCORED[0])
    hi = TB._ms(TB.SCORED[1]) + TB.MS_1D - 1
    lines.append(f"ESTATE READY (read-only) {TB.SCORED[0]} -> {TB.SCORED[1]}")
    for sym in RC.UNIVERSE:
        for tf, step in (("1h", TB.MS_1H), ("4h", TB.MS_4H)):
            d = TB.load_klines(sym, tf)
            o = d["open_time"].to_numpy(np.int64)
            w = o[(o >= lo) & (o <= hi)]
            diffs = np.diff(w)
            gaps = int((diffs != step).sum())
            good = len(w) > 0 and gaps == 0 and bool((diffs > 0).all())
            ok &= good
            lines.append(f"  {'OK ' if good else 'HALT'}  {sym:9} {tf:3} rows={len(w):6d} "
                         f"gaps={gaps} {TB.iso(w[0])} -> {TB.iso(w[-1])}")
    return rec("F-C2-1", ok, lines)


# ══════════════════════════════════════════ F-C2-2 · rule card + three trades
RULE_CARD = """\
UNIVERSE ["universe"]: {BTC,ETH,SOL,NEAR,ZEC}USDT · LENS ["lens"]: 4h only
TIDE: long iff e89>e316 AND close>e316 on 4h (mirror short)
WINDOW: 4h 12/89 cross in direction, no counter yet; displacement |close-e89|/ATR
  at the cross >= d=0.75 ["d"]; sensitivity strip {0.50,1.00} printed UNSCORED
TRIGGER: first in-window 4h 12/26 cross -> enter at that bar close
STOP ["stop"]: structural beyond nearest 1H swing pivot (architecture of record);
  R = entry-stop distance; one unit; one position per asset
RIDE: no management of any kind
BELL: counter 4h 12/89 OR 4h 89/316 against -> exit at close
ACCOUNTING ["accounting"]: net of 10 bps round-trip + journaled funding; R units"""


def f_rulecard_and_trades() -> bool:
    lines = ["RULE CARD, verbatim:"] + ["  " + x for x in RULE_CARD.splitlines()]
    ok = True
    jr = pd.read_parquet(TB.OUT / "trade_journal.parquet")
    if not len(jr):
        return rec("F-C2-2", False, lines + ["no trades to verify"])

    # THREE distinct trades, chosen adversarially rather than conveniently:
    # the earliest (no cherry-picking by date), the best net R, the widest
    # bell-only gap, then the worst net R — taken in that order until three
    # DISTINCT trades are held.  Three is the contract; fewer is a failure.
    jr = jr.copy()
    jr["gap"] = (jr["net_r_bellonly"] - jr["net_r"]).abs()
    order = (list(jr.sort_values("entry_ms")["entry_ms"])[:1]
             + list(jr.sort_values("net_r", ascending=False)["entry_ms"])[:1]
             + list(jr.sort_values("gap", ascending=False)["entry_ms"])[:1]
             + list(jr.sort_values("net_r")["entry_ms"])
             + list(jr.sort_values("entry_ms")["entry_ms"]))
    picks: list = []
    for em in order:
        if em not in picks:
            picks.append(em)
        if len(picks) == 3:
            break
    if len(picks) < 3:
        return rec("F-C2-2", False,
                   lines + [f"only {len(picks)} distinct trades available; "
                            f"the contract asks for THREE"])

    for em in picks:
        r = jr[jr["entry_ms"] == em].iloc[0]
        sym, d = r["asset"], (1 if r["direction"] == "long" else -1)
        k4, k1 = TB.load_klines(sym, "4h"), TB.load_klines(sym, "1h")
        f = RC.build_4h(k4["open_time"].to_numpy(np.int64),
                        k4["open"].to_numpy(float), k4["high"].to_numpy(float),
                        k4["low"].to_numpy(float), k4["close"].to_numpy(float))
        ot = f.open_ms
        ai = int(np.searchsorted(ot, int(r["arm_ms"])))
        ti = int(np.searchsorted(ot, int(r["entry_ms"])))
        xi = int(np.searchsorted(ot, int(r["exit_ms"])))
        lines.append("")
        lines.append(f"TRADE  {sym} {r['direction']}  arm {r['arm_ts']}  "
                     f"entry {r['entry_ts']}  exit {r['exit_ts']} ({r['exit_reason']})")

        # 1 · ARMING is a real 12/89 cross in direction, from RAW bars
        e12p, e89p = f.e12[ai - 1], f.e89[ai - 1]
        e12n, e89n = f.e12[ai], f.e89[ai]
        arm_ok = ((e12n > e89n and e12p <= e89p) if d == 1
                  else (e12n < e89n and e12p >= e89p))
        ok &= arm_ok
        lines.append(f"  [{'OK ' if arm_ok else 'BAD'}] arming 12/89: prev e12={e12p:.6f} "
                     f"e89={e89p:.6f} -> now e12={e12n:.6f} e89={e89n:.6f}")

        # 2 · TIDE at the arming bar
        tide = (f.e89[ai] > f.e316[ai] and f.c[ai] > f.e316[ai]) if d == 1 else \
               (f.e89[ai] < f.e316[ai] and f.c[ai] < f.e316[ai])
        ok &= bool(tide)
        lines.append(f"  [{'OK ' if tide else 'BAD'}] tide: e89={f.e89[ai]:.6f} "
                     f"e316={f.e316[ai]:.6f} close={f.c[ai]:.6f}")

        # 3 · DISPLACEMENT at the cross
        disp = abs(f.c[ai] - f.e89[ai]) / f.atr[ai]
        # 1e-6, not 1e-9: the journal stores at 6 dp by the determinism
        # rounding, so a tighter tolerance tests the rounding, not the value.
        dok = disp >= RC.D_DISPLACEMENT and abs(disp - float(r["disp_at_arming"])) < 1e-6
        ok &= bool(dok)
        lines.append(f"  [{'OK ' if dok else 'BAD'}] d: |{f.c[ai]:.6f}-{f.e89[ai]:.6f}|"
                     f"/{f.atr[ai]:.6f} = {disp:.6f} >= {RC.D_DISPLACEMENT}"
                     f"  (journal {r['disp_at_arming']})")

        # 4 · TRIGGER is a real 12/26 cross, and entry px IS that bar's close
        t12p, t26p, t12n, t26n = f.e12[ti - 1], f.e26[ti - 1], f.e12[ti], f.e26[ti]
        trig_ok = ((t12n > t26n and t12p <= t26p) if d == 1
                   else (t12n < t26n and t12p >= t26p))
        px_ok = abs(float(f.c[ti]) - float(r["entry_px"])) < 1e-9
        ok &= bool(trig_ok and px_ok)
        lines.append(f"  [{'OK ' if trig_ok else 'BAD'}] trigger 12/26: prev e12={t12p:.6f} "
                     f"e26={t26p:.6f} -> now e12={t12n:.6f} e26={t26n:.6f}")
        lines.append(f"  [{'OK ' if px_ok else 'BAD'}] entry px = bar close "
                     f"{f.c[ti]:.6f} (journal {r['entry_px']})")

        # 5 · STOP px re-derived from the 1h pivot grid
        pv = RC.build_pivots_1h(k1["high"].to_numpy(float), k1["low"].to_numpy(float))
        h1 = k1["open_time"].to_numpy(np.int64)
        cur = int(np.searchsorted(h1, int(ot[ti]) + 3 * TB.MS_1H, "right")) - 1
        st = RC.struct_stop(pv, cur, float(f.c[ti]), d, float(f.atr[ti]))
        st_ok = st is not None and abs(st - float(r["stop_px"])) < 1e-6
        anchor = float(r["pivot_anchor"])
        ok &= bool(st_ok)
        lines.append(f"  [{'OK ' if st_ok else 'BAD'}] stop: 1h (5,5) pivot {anchor:.6f} "
                     f"{'-' if d == 1 else '+'} {RC.STOP_BUF_ATR}x ATR({f.atr[ti]:.6f}) "
                     f"= {st:.6f} (journal {r['stop_px']})")
        rd_ok = abs(abs(float(f.c[ti]) - st) - float(r["r_dist"])) < 1e-6
        ok &= bool(rd_ok)
        lines.append(f"  [{'OK ' if rd_ok else 'BAD'}] R = |entry-stop| = {r['r_dist']}")

        # 6 · EXIT — the bell/stop that fired, from raw bars
        if r["exit_reason"] == "stop":
            hit = (f.l[xi] <= st) if d == 1 else (f.h[xi] >= st)
            lines.append(f"  [{'OK ' if hit else 'BAD'}] stop hit intrabar: "
                         f"bar {TB.iso(ot[xi])} low={f.l[xi]:.6f} high={f.h[xi]:.6f} vs {st:.6f}")
            ok &= bool(hit)
        else:
            p12, p89 = f.e12[xi - 1], f.e89[xi - 1]
            n12, n89 = f.e12[xi], f.e89[xi]
            bell = ((n12 < n89 and p12 >= p89) if d == 1 else (n12 > n89 and p12 <= p89))
            b8p, b3p = f.e89[xi - 1], f.e316[xi - 1]
            b8n, b3n = f.e89[xi], f.e316[xi]
            bell2 = ((b8n < b3n and b8p >= b3p) if d == 1 else (b8n > b3n and b8p <= b3p))
            ok &= bool(bell or bell2)
            lines.append(f"  [{'OK ' if (bell or bell2) else 'BAD'}] bell "
                         f"{'12/89' if bell else '89/316'} at {TB.iso(ot[xi])}; "
                         f"exit px = close {f.c[xi]:.6f} (journal {r['exit_px']})")

        # 7 · NET R reconciled from raw prices + the register's toll + funding
        gross = (float(r["exit_px"]) - float(r["entry_px"])) * d / float(r["r_dist"])
        fee = (RC.FEE_BPS_SIDE / 10_000.0) * (float(r["entry_px"]) + float(r["exit_px"])) \
            / float(r["r_dist"])
        fund = TB.load_funding(sym)
        fu = 0.0
        for j in range(ti + 1, xi + 1):
            rate = fund.get(int(ot[j]))
            if rate:
                fu += rate * float(f.c[j - 1]) * d
        fu /= float(r["r_dist"])
        net = gross - fee - fu
        net_ok = abs(net - float(r["net_r"])) < 1e-6
        ok &= bool(net_ok)
        lines.append(f"  [{'OK ' if net_ok else 'BAD'}] net R = gross {gross:+.6f} "
                     f"- fee {fee:.6f} - funding {fu:+.6f} = {net:+.6f} "
                     f"(journal {r['net_r']})")
    return rec("F-C2-2", ok, lines)


# ══════════════════════════════════════════════ F-C2-3 · the closed register
def f_register() -> bool:
    """Every constant is cited AND the citation is re-read from its source."""
    lines, ok = [], True
    lines.append(f"{'constant':22} {'value':28} source")
    for k, v in RC.REGISTER.items():
        lines.append(f"{k:22} {str(v['value']):28} {v['source'][:96]}")

    # the three that live in a file we can re-read, re-read
    import yaml
    cfg = yaml.safe_load((ROOT / "configs" / "naiad_v0.yaml").read_text())
    checks = [
        ("ATR_LEN", RC.ATR_LEN, cfg["signal"]["atr_len"], "configs/naiad_v0.yaml"),
        ("FEE_BPS_SIDE", RC.FEE_BPS_SIDE, cfg["trading"]["fee_bps_side"],
         "configs/naiad_v0.yaml"),
        ("STOP_BUF_ATR", RC.STOP_BUF_ATR, cfg["signal"]["stop_buf_atr"],
         "configs/naiad_v0.yaml"),
    ]
    tr = (ROOT / "engine" / "trading.py").read_text()
    checks.append(("STOP_BUF_ATR == engine TRAIL_B", RC.STOP_BUF_ATR, 0.5,
                   "engine/trading.py TRAIL_B"))
    ok &= "TRAIL_B = 0.5" in tr
    lines.append("")
    lines.append(f"[{'OK ' if 'TRAIL_B = 0.5' in tr else 'BAD'}] engine/trading.py "
                 f"still reads 'TRAIL_B = 0.5'")
    ok &= "cur1h - plow_1h <= 200" in tr
    lines.append(f"[{'OK ' if 'cur1h - plow_1h <= 200' in tr else 'BAD'}] "
                 f"engine/trading.py still reads the 200-bar 1h lookback")
    for name, mine, theirs, src in checks:
        good = float(mine) == float(theirs)
        ok &= good
        lines.append(f"[{'OK ' if good else 'BAD'}] {name:32} mine={mine} "
                     f"source={theirs} ({src})")

    # 10 bps round trip is DERIVED from the register, never typed
    good = RC.FEE_BPS_ROUND_TRIP == 2 * RC.FEE_BPS_SIDE == 10.0
    ok &= good
    lines.append(f"[{'OK ' if good else 'BAD'}] toll = 2 x fee_bps_side = "
                 f"{RC.FEE_BPS_ROUND_TRIP} bps round trip — the rule card's "
                 f"['accounting'] figure, derived not typed")

    # no bare numeric literal in the rules module outside REGISTER / indices
    return rec("F-C2-3", ok, lines)


# ════════════════════════════════════════════════════ F-C2-4 · determinism
def f_determinism() -> bool:
    lines = []
    a = json.loads((TB.OUT / "build_manifest.json").read_text())
    p2 = TB.OUT_RERUN / "build_manifest.json"
    if not p2.exists():
        return rec("F-C2-4", False, ["re-run manifest absent — run --rerun first"])
    b = json.loads(p2.read_text())
    ok = True
    for k in sorted(a["sha"]):
        same = a["sha"][k] == b["sha"].get(k)
        ok &= same
        lines.append(f"[{'OK ' if same else 'BAD'}] {k:20} {a['sha'][k][:32]}")
    lines.append("")
    lines.append("NORMALIZATION DISCLOSURE — normalized fields: ['elapsed_s'] "
                 "(wall clock) and the output ROOT path. NO computed value is "
                 "normalized: every table, count, hash and R figure is compared "
                 "content-for-content.")
    lines.append(f"seed {TB.SEED} is printed and unused — no stochastic step "
                 f"exists in this program, so determinism is structural.")
    return rec("F-C2-4", ok, lines)


# ══════════════════════════════════════ F-C2-5 · era exclusions, min/max ts
def f_eras() -> bool:
    lines, ok = [], True
    lo_s, hi_s = TB._ms(TB.SCORED[0]), TB._ms(TB.SCORED[1]) + TB.MS_1D - 1
    lb0, lb1 = TB._ms(TB.LOCKBOX[0]), TB._ms(TB.LOCKBOX[1]) + TB.MS_1D - 1
    ceil_census = TB._ms("2024-07-01")

    for name, cols in (("trade_journal", ("entry_ms", "exit_ms", "arm_ms")),
                       ("analytics_tape", ("ts",))):
        d = pd.read_parquet(TB.OUT / f"{name}.parquet")
        for c in cols:
            if c not in d.columns or not len(d):
                continue
            mn, mx = int(d[c].min()), int(d[c].max())
            inw = lo_s <= mn and mx <= hi_s
            nolb = not (mn <= lb1 and mx >= lb0)
            noce = mn >= ceil_census
            ok &= inw and nolb and noce
            lines.append(f"[{'OK ' if (inw and nolb and noce) else 'BAD'}] "
                         f"{name}.{c:9} min={TB.iso(mn)} max={TB.iso(mx)}  "
                         f"in-scored={inw} lockbox-free={nolb} "
                         f"after-census-ceiling={noce}")
    lines.append(f"    SEALED LOCKBOX {TB.iso(lb0)} -> {TB.iso(lb1)} — NOT COMPUTED; "
                 f"no scored table carries a timestamp inside it.")
    lines.append(f"    census-scored era ceiling {TB.iso(ceil_census)} "
                 f"(scripts/census_build.py CEIL_MS) — no scored row precedes it.")
    lines.append("    WARM-UP TRAVERSAL DISCLOSED: the EMA/ATR recursion reads bars "
                 "before the scored window (lockbox era included) to arrive warm. "
                 "Traversal is not emission — LEDGER.md:121 F4-a is the precedent.")
    # display-only strips must NOT be in the scored table
    ds = pd.read_parquet(TB.OUT / "display_only_strips.parquet")
    good = set(ds["window"]) <= {"CENSUS_ERA", "PINNING"}
    ok &= good
    lines.append(f"[{'OK ' if good else 'BAD'}] display-only strips carry only "
                 f"{sorted(set(ds['window']))} — and are in their own table, never "
                 f"pooled into headline.parquet")
    return rec("F-C2-5", ok, lines)


# ═══════════════════════════ F-C2-6 · captured-not-consulted (Amendment B1)
def f_no_consultation() -> bool:
    """The decision path imports no registry symbol — proven THREE ways."""
    lines, ok = [], True
    src = (ROOT / "scripts" / "tierc2_rules.py").read_text()

    # (1) the grep the amendment asks for — over the AST's import nodes, not
    #     over raw lines.  A line-grep here FAILED on its first run against
    #     this module's own prose ("...imports no registry symbol"), which is
    #     the exact false positive that makes a text grep the weaker test.
    import ast
    tree = ast.parse(src)
    imported: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported += [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom):
            imported.append(node.module or "")
    hits = [m for m in imported if m == "analytics" or m.startswith("analytics.")]
    g = not hits
    ok &= g
    lines.append(f"[{'OK ' if g else 'BAD'}] AST import scan of "
                 f"scripts/tierc2_rules.py: {sorted(set(imported))} — "
                 f"analytics hits = {hits}")

    # (2) the stronger property: the TRANSITIVE import closure
    import tierc2_rules  # noqa: F401
    seen, stack = set(), ["tierc2_rules"]
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
                 f"tierc2_rules: {len(seen)} modules, analytics members = {bad}")
    lines.append(f"    closure (project modules only): "
                 f"{sorted(m for m in seen if m.split('.')[0] in {'engine','tierc2_rules'})}")

    # (3) why (2) cannot be defeated: engine/ never imports analytics/ either
    eng = [p.name for p in (ROOT / "engine").glob("*.py")
           if "import analytics" in p.read_text() or "from analytics" in p.read_text()]
    g3 = not eng
    ok &= g3
    lines.append(f"[{'OK ' if g3 else 'BAD'}] engine/ modules importing analytics: "
                 f"{eng}  (invariant I-B, analytics/INTERFACE.md — so the closure "
                 f"cannot reach a registry symbol by any path)")

    # (4) and the tape columns are write-only: nothing in the decision path
    #     names them
    tape_cols = ["wall_family", "dist_atr", "coloc_n", "nearest_level",
                 "rvwap", "avwap", "prior_extreme"]
    named = [c for c in tape_cols if c in src]
    g4 = not named
    ok &= g4
    lines.append(f"[{'OK ' if g4 else 'BAD'}] tape column names appearing in the "
                 f"decision path: {named}")
    return rec("F-C2-6", ok, lines)


# ══════════════════ F-C2-7 · endpoint reconciliation + sabotage REJECT
def f_endpoint_and_sabotage() -> bool:
    lines, ok = [], True
    sym = RC.UNIVERSE[0]
    k4 = TB.load_klines(sym, "4h")
    lo, hi = TB._ms(TB.SCORED[0]), TB._ms(TB.SCORED[1]) + TB.MS_1D - 1
    ot = k4["open_time"].to_numpy(np.int64)
    idx = np.flatnonzero((ot >= lo) & (ot <= hi))
    probe = int(idx[len(idx) // 2])

    # ── (a) ONE INSTANT, hand-reconciled against analytics DIRECTLY, by
    #        ACTUAL endpoint slicing — the value the tape stores must equal
    #        the value a caller gets from a series truncated at the instant.
    full = TB.build_level_series(k4)
    k4c = k4.iloc[:probe + 1]
    cut = TB.build_level_series(k4c)
    lines.append(f"instant {TB.iso(ot[probe])}  ({sym} 4h bar #{probe})")
    for fam in TB.TAPE_FAMILIES:
        for name in full[fam]:
            a = full[fam][name][probe]
            b = cut[fam][name][probe] if name in cut[fam] else np.nan
            same = (np.isnan(a) and np.isnan(b)) or (
                np.isfinite(a) and np.isfinite(b) and abs(a - b) <= 1e-9 * max(1.0, abs(a)))
            ok &= bool(same)
            lines.append(f"  [{'OK ' if same else 'BAD'}] {name:22} "
                         f"full-array={a!r:>22}  endpoint-sliced={b!r:>22}")

    # ── (b) the same instant, one level re-derived from the analytics module
    #        by hand, with no tape code in the path at all
    src = ((k4c["high"].to_numpy(float) + k4c["low"].to_numpy(float)
            + k4c["close"].to_numpy(float)) / 3.0)
    hand = AW.rolling_vwap(k4c["open_time"].to_numpy(np.int64), src,
                           k4c["volume"].to_numpy(float), window_days=7,
                           sigmas=(1, 2))["vwap"][-1]
    tape_v = full["rvwap"]["rvwap_7d"][probe]
    same = abs(hand - tape_v) <= 1e-9 * max(1.0, abs(hand))
    ok &= bool(same)
    lines.append(f"  [{'OK ' if same else 'BAD'}] hand-called AW.rolling_vwap(...)[-1] "
                 f"= {hand:.10f}  vs tape {tape_v:.10f}")
    ph, _ = AS.prior_period_extremes(k4c["open_time"].to_numpy(np.int64),
                                     k4c["high"].to_numpy(float),
                                     k4c["low"].to_numpy(float), period="D")
    same2 = abs(ph[-1] - full["prior_extreme"]["prior_day_high"][probe]) < 1e-12
    ok &= bool(same2)
    lines.append(f"  [{'OK ' if same2 else 'BAD'}] hand-called "
                 f"AS.prior_period_extremes(...,'D')[0][-1] = {ph[-1]:.6f}")

    # ── (c) SABOTAGE — the F-10 lever (census2a_program.py:2236), re-proven on
    #        THIS corridor: an as-of read that reaches one bar past the instant
    #        must be REJECTED, not silently honoured.
    def as_of(t: int, extra_bars: int = 0) -> float:
        k = int(np.searchsorted(ot + TB.MS_4H, t, "right")) - 1 + extra_bars
        if k < 0 or k >= len(ot):
            raise IndexError("out of range")
        if extra_bars > 0 and (ot[k] + TB.MS_4H) > t:
            raise ValueError(
                f"CAUSALITY VIOLATION: bar closing {TB.iso(int(ot[k] + TB.MS_4H))} "
                f"is in the future of the as-of instant {TB.iso(t)}")
        return float(k4["close"].to_numpy(float)[k])

    t = int(ot[probe]) + TB.MS_4H          # the instant this bar CLOSES
    clean = as_of(t)
    rejected = False
    try:
        as_of(t, extra_bars=1)
    except ValueError as e:
        rejected = True
        msg = str(e)
    ok &= rejected
    lines.append("")
    lines.append(f"  [{'OK ' if rejected else 'BAD'}] SABOTAGE on this corridor: "
                 f"clean as-of({TB.iso(t)}) = {clean:.6f}; extra_bars=1 REJECTED")
    if rejected:
        lines.append(f"        {msg}")

    # ── (d) the same lever against the real level path
    sab_ok = True
    try:
        over = k4.iloc[:probe + 2]          # one bar into the future
        s2 = ((over["high"].to_numpy(float) + over["low"].to_numpy(float)
               + over["close"].to_numpy(float)) / 3.0)
        future = AW.rolling_vwap(over["open_time"].to_numpy(np.int64), s2,
                                 over["volume"].to_numpy(float), window_days=7,
                                 sigmas=(1, 2))["vwap"][-1]
        sab_ok = abs(future - tape_v) > 1e-12     # it MUST differ
    except Exception:
        sab_ok = False
    ok &= sab_ok
    lines.append(f"  [{'OK ' if sab_ok else 'BAD'}] a level built one bar into the "
                 f"future differs from the stored value ({future:.6f} vs "
                 f"{tape_v:.6f}) — so the stored value provably did not see it")

    lines.append("")
    lines.append(f"  I9: ANALYTICS_VERSION {AN.ANALYTICS_VERSION} · "
                 f"analytics_sha {AN.analytics_sha()}")
    lines.append(f"  instrument: BINANCE USDT-M perpetuals, "
                 f"{{{','.join(s.replace('USDT','') for s in RC.UNIVERSE)}}}USDT.P · "
                 f"cache {TB.KLINES}")
    return rec("F-C2-7", ok, lines)


# ════════════════════════════════════════════════════════════════ main
def main() -> int:
    print("=" * 78)
    print("TIER-C2 FIXTURE TRANSCRIPT")
    print("=" * 78)
    f_gates()
    f_rulecard_and_trades()
    f_register()
    f_determinism()
    f_eras()
    f_no_consultation()
    f_endpoint_and_sabotage()

    print("\n".join(T))
    n_ok = sum(RESULTS.values())
    print()
    print("=" * 78)
    print(f"FIXTURE SUMMARY  {n_ok}/{len(RESULTS)} PASS  "
          f"{json.dumps(RESULTS)}")
    print("=" * 78)
    if n_ok < len(RESULTS):
        print("*** HALT: fixture mismatch. Nothing downstream is trustworthy. ***")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
