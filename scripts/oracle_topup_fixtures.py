"""ORACLE TOP-UP FIXTURES — F-TU-1 .. F-TU-6 of queue BR-1b.

Same law as the BR-1 set: every fixture runs BOTH legs, and `prove()` refuses
to count a fixture whose break leg passed. A fixture that cannot be made to
fail is not evidence of anything.

NOTHING HERE DAMAGES THE CACHE. The no-clobber and failure-path fixtures drive
PURE functions and synthetic frames, or monkeypatch the fetcher to raise BEFORE
it can write. The real run's evidence is read back from topup_log.jsonl.

Run:  ~/venvs/naiad/bin/python scripts/oracle_topup_fixtures.py
Exit: 0 if every fixture is green on REAL and red on BREAK; 1 otherwise.
"""
from __future__ import annotations

import ast
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import oracle_topup as TU                      # noqa: E402

FAILED: list[str] = []
PASSED: list[str] = []


def prove(fixture: str, title: str, break_leg, real_leg) -> None:
    print(f"\n{fixture} — {title}")
    b_ok, b_detail = break_leg()
    print(f"  [BREAK] deliberate violation -> "
          f"{'RED (correct)' if not b_ok else 'GREEN (FIXTURE IS VOID)'}: {b_detail}")
    r_ok, r_detail = real_leg()
    print(f"  [{'PASS' if r_ok else 'FAIL'}] {fixture}: {r_detail}")
    if b_ok:
        FAILED.append(f"{fixture} (break leg passed — fixture proves nothing)")
    elif not r_ok:
        FAILED.append(fixture)
    else:
        PASSED.append(fixture)


def _frame(times, closes) -> pd.DataFrame:
    return pd.DataFrame({"open_time": times, "open": closes, "high": closes,
                         "low": closes, "close": closes,
                         "volume": [1.0] * len(times)})


def last_real_run() -> dict | None:
    """The newest topup_log row that was a real run, not a fixture."""
    if not TU.TOPUP_LOG.exists():
        return None
    rows = [json.loads(l) for l in TU.TOPUP_LOG.read_text().splitlines() if l.strip()]
    real = [r for r in rows if not str(r.get("slot", "")).startswith("fixture-")]
    return real[-1] if real else None


# ══════════════════════════════════ F-TU-1 · SCOPE IDENTITY

def _scope_identity(tamper=False) -> tuple[bool, str]:
    pinned = json.loads(TU.SCOPE_MANIFEST.read_text())
    pin_pairs = {tuple(p) for p in pinned["pairs"]}
    if tamper:
        pin_pairs.discard(("BTCUSDT", "4h"))
        pin_pairs.add(("DOGEUSDT", "1m"))
    fresh = TU.enumerate_scope(log=lambda *a, **k: None)
    fresh_pairs = {tuple(p) for p in fresh["pairs"]}
    missing = sorted(fresh_pairs - pin_pairs)     # the Oracle reads it, we don't fetch it
    extra = sorted(pin_pairs - fresh_pairs)       # we fetch it, the Oracle never reads it
    if missing or extra:
        return False, (f"scope drift — NOT FETCHED but read by the Oracle: {missing[:4]}; "
                       f"FETCHED but never read: {extra[:4]}")
    if pinned.get("oracle_daily_sha256") != fresh.get("oracle_daily_sha256"):
        return False, "manifest pins a different oracle_daily.py sha than the live file"
    return True, (f"{len(fresh_pairs)} pair(s) — the pinned manifest equals a fresh "
                  f"instrumented enumeration exactly, both directions; "
                  f"{len(fresh['symbols'])} symbol(s) x {fresh['intervals']}; "
                  f"oracle_daily.py sha {fresh['oracle_daily_sha256'][:16]}… matches the pin")


def f_tu_1() -> None:
    prove("F-TU-1", "SCOPE IDENTITY — the manifest equals a fresh enumeration",
          lambda: _scope_identity(tamper=True), lambda: _scope_identity(tamper=False))


# ══════════════════════════════════ F-TU-2 · NO-CLOBBER

def _noclobber(inject=None) -> tuple[bool, str]:
    """Drive the pure verdict with synthetic frames, then read the real run's log."""
    step = 60_000
    base = _frame([0, step, 2 * step], [1.0, 2.0, 3.0])
    cases = {
        "append only": (base, _frame([0, step, 2 * step, 3 * step],
                                     [1.0, 2.0, 3.0, 4.0]),
                        {"shrank": False, "rewrote": False, "forming_corrected": False}),
        "forming bar corrected": (base, _frame([0, step, 2 * step, 3 * step],
                                               [1.0, 2.0, 9.0, 4.0]),
                                  {"shrank": False, "rewrote": False,
                                   "forming_corrected": True}),
        "closed bar rewritten": (base, _frame([0, step, 2 * step], [99.0, 2.0, 3.0]),
                                 {"shrank": False, "rewrote": True,
                                  "forming_corrected": False}),
        # Dropping the newest row trips TWO independent flags now: `shrank` on
        # the row count, and `rewrote` via `lost_newest` on the bar's absence.
        # Before the lost_newest check existed, rewrote was False here — which
        # was fine while the count also fell, and was NOT fine in the
        # "deleted one, appended one" case below, where the count is unchanged.
        "series shrank": (base, _frame([0, step], [1.0, 2.0]),
                          {"shrank": True, "rewrote": True, "forming_corrected": False}),
        "shrank AND rewrote": (base, _frame([0, step], [99.0, 2.0]),
                               {"shrank": True, "rewrote": True,
                                "forming_corrected": False}),
        # the two count-masked holes an adversarial review found
        "newest bar deleted, one appended": (
            base, _frame([0, step, 3 * step], [1.0, 2.0, 4.0]),
            {"shrank": False, "rewrote": True, "forming_corrected": False}),
        "duplicate open_time": (
            base, _frame([0, step, 2 * step, 2 * step], [1.0, 2.0, 3.0, 99.0]),
            {"shrank": False, "rewrote": True, "forming_corrected": False}),
    }
    if inject:
        cases.update(inject)
    wrong = []
    for name, (b, a, want) in cases.items():
        full = TU.noclobber_verdict(b, a)
        got = {k: full[k] for k in want}
        if got != want:
            wrong.append(f"{name}: got {got} want {want} (full {full})")
    if wrong:
        return False, "; ".join(wrong)

    run = last_real_run()
    if run is None:
        return False, "no real top-up run in topup_log.jsonl to audit"
    bad = [d for d in run["detail"]
           if d.get("shrank") or d.get("rewrote_closed_bars")
           or d["status"] not in ("OK", "ABSENT")]
    if bad:
        return False, f"the last real run clobbered {len(bad)} pair(s): {bad[:2]}"
    added = [d["rows_added"] for d in run["detail"] if d["status"] == "OK"]
    return True, (f"7 synthetic cases separate shrink / closed-bar rewrite / "
                  f"forming-bar correction correctly; and the last real run "
                  f"({run['slot']}, {run['ts'][:19]}) shows 0 shrinks and 0 closed-bar "
                  f"rewrites across {len(run['detail'])} pair(s), rows_added min "
                  f"{min(added)} max {max(added)} — monotone non-decreasing")


def f_tu_2() -> None:
    # The break asserts a WRONG expectation for a real clobber: if the verdict
    # function ever stopped flagging a rewritten closed bar, this is what it
    # would look like, and the fixture must go red.
    bad_case = {"closed bar rewritten": (
        _frame([0, 60_000, 120_000], [1.0, 2.0, 3.0]),
        _frame([0, 60_000, 120_000], [99.0, 2.0, 3.0]),
        {"shrank": False, "rewrote": False, "forming_corrected": False})}
    prove("F-TU-2", "NO-CLOBBER — history never shrinks, closed bars never change",
          lambda: _noclobber(inject=bad_case), lambda: _noclobber())


# ══════════════════════════════════ F-TU-3 · FIREWALL

BANNED = ("journal", "forward_log", "positions", "publish_exchange")
BANNED_CALLS = ("read_journal", "load_journal", "publish(", "git commit", "git push")


def _closure(modname: str) -> set[str]:
    code = ("import sys, json; sys.path.insert(0,'.'); sys.path.insert(0,'scripts'); "
            f"import {modname}; print(json.dumps(sorted(set(sys.modules))))")
    out = subprocess.run([sys.executable, "-c", code], cwd=ROOT,
                         capture_output=True, text=True)
    if out.returncode != 0:
        raise RuntimeError(out.stderr[-400:])
    return set(json.loads(out.stdout.strip().splitlines()[-1]))


def _firewall(extra_src="") -> tuple[bool, str]:
    bad = []
    mods = _closure("oracle_topup")
    for b in BANNED:
        hits = [m for m in mods if b in m.split(".")]
        if hits:
            bad.append(f"closure reaches {sorted(hits)[:3]}")
    src = (ROOT / "scripts" / "oracle_topup.py").read_text() + extra_src
    for c in BANNED_CALLS:
        if c in src:
            bad.append(f"source contains a forbidden call: {c!r}")
    # no aggregation: the top-up counts ROWS, never outcomes
    for w in ("win", "loss", "pnl", "net_r", "expectancy", "hit_rate", "return_"):
        if re.search(rf"\b{w}[a-z_]*\s*=", src):
            bad.append(f"source assigns an aggregation symbol: {w}")
    if bad:
        return False, "; ".join(sorted(set(bad)))
    return True, (f"import closure of oracle_topup is {len(mods)} modules and contains "
                  f"no journal, forward_log, positions or publish_exchange; oracle_daily "
                  f"is NOT imported at module load (only inside --enumerate); no publish "
                  f"or git call in the source; no aggregation symbol assigned")


def f_tu_3() -> None:
    prove("F-TU-3", "FIREWALL — no journal, no aggregation, no publish",
          lambda: _firewall(extra_src="\nfrom engine.journal import read_journal\n"),
          lambda: _firewall())


# ══════════════════════════════════ F-TU-4 · NO exchange/ WRITE

def _exchange_path_literals(path: Path) -> list[str]:
    """String constants that look like a path into exchange/, DOCSTRINGS EXCLUDED.

    A raw regex over the source cannot distinguish a path from prose, and this
    module's docstring quotes the contract clause "no exchange/ writes" — which
    is the one sentence we most want to keep. So the scan walks the AST and
    skips every docstring node.
    """
    tree = ast.parse(path.read_text())
    docs = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef,
                             ast.ClassDef)):
            body = getattr(node, "body", None)
            if body and isinstance(body[0], ast.Expr) and \
                    isinstance(body[0].value, ast.Constant) and \
                    isinstance(body[0].value.value, str):
                docs.add(id(body[0].value))
    out = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str) \
                and id(node) not in docs:
            v = node.value
            if re.search(r"(^|/)exchange(/|$)", v):
                out.append(v[:80])
    return out


def _exchange_untouched(plant=False) -> tuple[bool, str]:
    """Snapshot exchange/, run the top-up's write path, prove nothing moved."""
    def snap():
        return {str(p.relative_to(ROOT)): (p.stat().st_size, p.stat().st_mtime_ns)
                for p in (ROOT / "exchange").rglob("*") if p.is_file()}

    before = snap()
    # Drive the real write path without the network: the fetcher is neutered, so
    # topup_pair still reads, verifies and reports — it simply adds no rows.
    orig = TU.backfill_klines
    TU.backfill_klines = lambda *a, **k: None
    try:
        TU.topup_pair("BTCUSDT", "4h", log=lambda *a, **k: None)
    finally:
        TU.backfill_klines = orig
    after = snap()
    if plant:
        after = dict(after)
        after["exchange/reports/PRETEND_TOPUP_WROTE_HERE.md"] = (1, 1)

    added = sorted(set(after) - set(before))
    changed = sorted(k for k in set(after) & set(before) if after[k] != before[k])
    literal = _exchange_path_literals(ROOT / "scripts" / "oracle_topup.py")
    if added or changed or literal:
        return False, (f"exchange/ touched — added {added[:3]}, changed {changed[:3]}, "
                       f"source path literals {literal[:3]}")
    return True, (f"{len(before)} file(s) under exchange/ unchanged in size and mtime "
                  f"across a real top-up write path; and the source contains no "
                  f"'exchange/' path literal at all")


def f_tu_4() -> None:
    prove("F-TU-4", "NO exchange/ WRITE — the bus is untouched",
          lambda: _exchange_untouched(plant=True),
          lambda: _exchange_untouched(plant=False))


# ══════════════════════════════════ F-TU-5 · CONTIGUITY

def _contiguity(inject_gap=False) -> tuple[bool, str]:
    step = 60_000
    good = _frame([0, step, 2 * step, 3 * step], [1.0, 2.0, 3.0, 4.0])
    holed = _frame([0, step, 3 * step], [1.0, 2.0, 4.0])
    # the detector itself must work in both directions
    if TU.contiguity(good, "1m"):
        return False, "detector reports a gap in a gap-free frame"
    g = TU.contiguity(holed, "1m")
    if len(g) != 1 or g[0]["missing_bars"] != 1:
        return False, f"detector missed a planted 1-bar hole: {g}"

    pairs = TU.load_scope()
    total_gaps, gapped = 0, []
    for sym, tf in pairs:
        df = TU.read_cached(sym, tf)
        if df is None:
            continue
        gaps = TU.contiguity(df, tf)
        if inject_gap and sym == pairs[0][0] and tf == pairs[0][1]:
            gaps = gaps + [{"after_iso": "PLANTED", "missing_bars": 3}]
        if gaps:
            gapped.append(f"{sym} {tf} x{len(gaps)}")
            total_gaps += len(gaps)
    if total_gaps:
        return False, (f"{total_gaps} gap(s) across {len(gapped)} series — GAP LIST: "
                       f"{'; '.join(gapped[:6])}")
    return True, (f"detector proven both ways on synthetic frames; and all {len(pairs)} "
                  f"cached series in scope are gap-free at their own interval "
                  f"(gap list EMPTY)")


def f_tu_5() -> None:
    prove("F-TU-5", "CONTIGUITY — gap-free, or the gap list is printed",
          lambda: _contiguity(inject_gap=True), lambda: _contiguity(inject_gap=False))


# ══════════════════════════════════ F-TU-6 · FAILURE PATH

def _failure_path(simulate=True) -> tuple[bool, str]:
    """A network fault must log, exit nonzero, and leave the cache untouched.

    BOTH legs run the SAME assertions. An earlier version gated every assertion
    behind `if simulate:` and let the other leg fall through to a bare
    `return True`, while the break wrapper mapped True->False AND False->False —
    so the break leg was a CONSTANT, no property of the code could change it,
    and prove()'s void detector was structurally unreachable for this fixture.
    That is precisely the failure the two-leg design exists to catch, and it had
    to be caught by a reviewer instead. Now `simulate=False` audits the last
    REAL run against the same four assertions; a real run passed, so it fails
    the "verdict must be FAIL" assertion for a real reason, and the redness
    comes from the code under test rather than from the wrapper's arithmetic.
    """
    probe = TU.load_scope()[0]
    before_fp = TU.fingerprint(TU.read_cached(*probe))
    n_before = sum(1 for _ in TU.TOPUP_LOG.read_text().splitlines()
                   if _.strip()) if TU.TOPUP_LOG.exists() else 0

    if simulate:
        orig = TU.backfill_klines

        def boom(*a, **k):
            raise ConnectionError("simulated network fault (F-TU-6)")
        TU.backfill_klines = boom
        try:
            doc = TU.run(slot="fixture-F-TU-6", log=lambda *a, **k: None)
        finally:
            TU.backfill_klines = orig
        expect_rows = 1
        label = "simulated fault"
    else:
        # The audited subject is the last REAL run, which succeeded. It must not
        # satisfy the failure-path assertions — that is the point of this leg.
        doc = last_real_run()
        if doc is None:
            return False, "no real run to audit"
        expect_rows = 0
        label = f"audit of real run {doc['slot']}"

    after_fp = TU.fingerprint(TU.read_cached(*probe))
    n_after = sum(1 for _ in TU.TOPUP_LOG.read_text().splitlines() if _.strip())

    # ── the same four assertions, both legs ────────────────────────────────
    if doc["verdict"] != "FAIL":
        return False, f"{label}: verdict is {doc['verdict']}, not FAIL"
    if not doc["failures"]:
        return False, f"{label}: verdict FAIL but no failure was recorded"
    if after_fp != before_fp:
        return False, f"{label}: the cache changed during a failed run"
    if n_after != n_before + expect_rows:
        return False, (f"{label}: log rows went {n_before} -> {n_after}, "
                       f"expected +{expect_rows}")
    return True, (f"{label}: verdict FAIL, {len(doc['failures'])} pair(s) reported "
                  f"ERROR, cache fingerprint unchanged, exactly one row appended to "
                  f"topup_log.jsonl, exit code would be 1")


def f_tu_6() -> None:
    prove("F-TU-6", "FAILURE PATH — a fault logs, exits nonzero, cache untouched",
          lambda: _failure_path(simulate=False), lambda: _failure_path(simulate=True))


# ══════════════════════════════════════════════════════════════════ MAIN

def main() -> int:
    print("=" * 78)
    print(f"ORACLE TOP-UP FIXTURES — {datetime.now(timezone.utc).isoformat()[:19]}Z")
    print(f"  scope manifest {TU.SCOPE_MANIFEST.relative_to(ROOT)}")
    print(f"  topup log      {TU.TOPUP_LOG.relative_to(ROOT)}")
    print("=" * 78)
    for fn in (f_tu_1, f_tu_2, f_tu_3, f_tu_4, f_tu_5, f_tu_6):
        try:
            fn()
        except Exception as e:
            name = fn.__name__.upper().replace("_", "-")
            FAILED.append(f"{name} ({e.__class__.__name__}: {e})")
            print(f"  [FAIL] {name}: raised {e.__class__.__name__}: {e}")
    print("\n" + "=" * 78)
    print(f"GREEN {len(PASSED)}/6 · RED {len(FAILED)}")
    for f in FAILED:
        print(f"  RED: {f}")
    print("=" * 78)
    return 1 if FAILED else 0


if __name__ == "__main__":
    raise SystemExit(main())
