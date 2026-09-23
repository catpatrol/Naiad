"""ORACLE ON-DEMAND FIXTURES — F-SK-1, F-SK-2a..2i, F-SK-3 of queue OR-1, STEP A;
F-SK-4 of queue OR-2, STEP 2 (R-4, the stray arming command).

Same law as the BR-1 and BR-1b sets: every fixture runs BOTH legs, and `prove()`
refuses to count a fixture whose break leg passed. A fixture that cannot be made
to fail is not evidence of anything.

WHAT IS UNDER TEST IS THE WIRING, NOT THE PARTS. F-SK-2 and F-SK-3 drive the REAL
oracle_wrapper.main() — argv in, exit code out, stdout captured, the flag and the
selfcheck row read back OFF DISK. Only the organs at the far end are replaced:
run_topup (a stub that returns the rc the scenario asks for), the movers organ (a
real subprocess, pointed at a three-line script in the sandbox) and oracle_daily
(a stand-in module that logs the Oracle's real line formats and writes a small
render). run_oracle itself is NOT stubbed: the row F-SK-2b reads is written by the
wrapper's own append_selfcheck.

NOTHING HERE REACHES THE LIVE LANE. FLAG, LOCK, SELFCHECK, MOVERS_SCRIPT and
MOVERS_DIR are redirected into a TemporaryDirectory (the F-BR-12 pattern), and
reschedule_if_drifted, arm and write_plist are replaced by recorders — so no fixture
run calls launchctl, touches ~/Library/LaunchAgents, fetches, renders into
briefs/oracle, or drops a flag in the repo. The five com.naiad.oracle-* agents are
suspended by operator ruling 2026-09-21 and this suite cannot re-arm one. (F-SK-2e
DOES hand main() an argv carrying --install — that is the fault it exists to catch —
and Sandbox.main refuses to do so unless arm and write_plist are its own recorders.)

F-SK-2h STARTS A CHILD: this file, run as `--child-cutoff <dir>`, is the same
sandbox in its own process with a top-up stub that hangs, so the parent can send it
a real SIGTERM / SIGKILL and read what is left in <dir>. It is not a test mode of
the wrapper; the wrapper it drives is the real module.

F-SK-4 STARTS CHILDREN TOO (`--child-install <dir> [plants] -- <argv>`), and it is
the one fixture that lets the REAL arm() run: in a child whose PATH holds only two
recording shell shims (`launchctl`, `plutil`) and whose HOME is the sandbox, so the
real launchctl cannot be found and the real plists are only ever READ (copied in).
The child refuses to start unless all of that holds; the five real plists and the
sentinel are stamped before and compared after. See F-SK-4.

Run:  ~/venvs/naiad/bin/python scripts/oracle_ondemand_fixtures.py
Exit: 0 if every fixture is green on REAL and red on BREAK; 1 otherwise.
"""
from __future__ import annotations

import ast
import contextlib
import hashlib
import io
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import types
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import oracle_wrapper as OW                    # noqa: E402

SKILL = ROOT / ".claude" / "skills" / "oracle" / "SKILL.md"
WRAPPER = ROOT / "scripts" / "oracle_wrapper.py"
ORACLE_SRC = ROOT / "scripts" / "oracle_daily.py"      # READ AS TEXT, never imported

# OR-1 STEP A, verbatim — the frontmatter is law to the byte.
SKILL_NAME = "oracle"
SKILL_DESCRIPTION = "Print an edition of The Daily Oracle on demand"

# The contract's OWN chain, written down a second time ON PURPOSE. F-SK-1 compares
# the skill against ONDEMAND_STEPS, which catches a step dropped from the skill —
# but a step deleted from BOTH the constant and the skill would agree with itself
# and pass. This literal is the third witness. OR-1 STEP A: "identity gate -> if
# ORACLE_DOWN.flag exists print it FIRST -> movers fetch (STEP E) -> in-scope
# top-up -> oracle_daily (full|refresh) -> open the render -> print the Front
# Page's top rows + the self-check verdict".
CONTRACT_CHAIN = ("identity-gate", "flag-first", "movers-fetch", "scope-topup",
                  "oracle-render", "open-render", "report-back")

# What the skill must say besides the chain: the three verbs as runnable commands,
# and the guardrails the suspension ruling earned.
SKILL_MUST_CARRY = (
    ("the full-edition command", "--job ondemand --slot on-demand-full"),
    ("the refresh command", "--job ondemand --slot on-demand-refresh"),
    ("the cache-only verb", "--no-fetch"),
    ("the dry run", "--dry-run"),
    ("the house interpreter", "~/venvs/naiad/bin/python"),
    ("the --install guardrail", "--install"),
    ("the rollback card", "research_outputs/oracle/SUSPENDED_2026-09-21.txt"),
    ("the LATE EDITION band", "LATE EDITION"),
    ("the macOS open", "open "),
    ("the closing Report line", "\nReport:"),
    # Fix round 1 (2026-09-21, verifier B2): the skill said "give the command a long
    # timeout", a wire-down edition outlives the harness's foreground ceiling, and a
    # cut-off run was silent and locked every retry out. The prose that ended that
    # is held here so it cannot be edited away.
    ("the detached run", "run_in_background"),
    ("the unbuffered interpreter", "python -u"),
    ("the edition's own log", "logs/launchd/oracle-ondemand.log"),
    ("the foreground ceiling", "600000"),
    ("what a polite cut-off says", "CUT OFF by signal"),
    ("what a hard cut-off leaves, and who reclaims it", "DEAD LOCK from"),
    ("the lock's age rule", "LOCK_STALE_MIN"),
    ("the --install refusal", "REFUSES --install"),
)

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


def step_ids() -> list[str]:
    return [s[0] for s in OW.ONDEMAND_STEPS]


# ══════════════════════════════════ F-SK-1 · THE SKILL FILE AND THE STEP LIST

_HEADING = re.compile(r"^#{2,4}\s*STEP\s+(\d+)\s*·\s*([a-z][a-z-]*)\s*$", re.M)
_DRY_LINE = re.compile(r"^\s+STEP\s+(\d+)\s+(\S+)\s+\[(wrapper|skill)\]", re.M)


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Minimal on purpose: `key: value` lines between two `---` rules, one pair of
    double quotes stripped. No YAML library — the venv has no pip, and a parser
    that accepted more than this would accept a frontmatter the harness may not."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("no frontmatter: line 1 is not '---'")
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        raise ValueError("frontmatter never closes: no second '---'") from None
    meta: dict[str, str] = {}
    for ln in lines[1:end]:
        if not ln.strip():
            continue
        if ":" not in ln:
            raise ValueError(f"frontmatter line is not key: value — {ln!r}")
        k, v = ln.split(":", 1)
        v = v.strip()
        if len(v) >= 2 and v[0] == v[-1] == '"':
            v = v[1:-1]
        meta[k.strip()] = v
    return meta, "\n".join(lines[end + 1:])


def _dry_run() -> tuple[int, str]:
    r = subprocess.run([sys.executable, str(WRAPPER), "--job", "ondemand", "--dry-run"],
                       cwd=str(ROOT), capture_output=True, text=True, timeout=60)
    return r.returncode, (r.stdout or "") + (r.stderr or "")


def _lane_stamp() -> tuple:
    """Existence + size + mtime of the three live files a dry run must not touch."""
    out = []
    for p in (OW.FLAG, OW.LOCK, OW.SELFCHECK):
        out.append((str(p), p.exists(),
                    (p.stat().st_size, p.stat().st_mtime_ns) if p.exists() else None))
    return tuple(out)


# Taken by f_sk_1() BEFORE prove() — i.e. before the BREAK leg's own dry run. The
# first version stamped inside the real leg, AFTER the break leg had already run
# one: a dry run that created the lock had done so before `before` was read, and
# the comparison could not see it (verifier mutation M11: dry run made to call
# acquire_lock, suite GREEN 8/8, lock file really on disk).
_LANE_BEFORE: tuple | None = None


def _dry_in_sandbox(plant: bool) -> tuple[bool, str]:
    """The same promise, where a fault can be PLANTED: the dry run through the real
    main() in the sandbox, with and without a standing flag. `plant=True` is M11 —
    a plan printer that takes the lock on its way."""
    seen = []
    for argv in (["--job", "ondemand", "--dry-run"],
                 REFRESH + ["--no-fetch", "--dry-run"]):
        for flagged in (False, True):
            with Sandbox() as sb:
                body = planted_flag_body()
                if flagged:
                    OW.FLAG.write_text(body, encoding="utf-8")
                if plant:
                    real_plan = OW.ondemand_plan_lines
                    OW.ondemand_plan_lines = (lambda slot, no_fetch: (
                        OW.acquire_lock("dry-run/planted", log=lambda *a: None),
                        real_plan(slot, no_fetch))[1])
                rc, out = sb.main(argv)
                left = sorted(p.name for p in sb.td.iterdir()
                              if p.name not in (OW.MOVERS_SCRIPT.name,
                                                OW.FLAG.name if flagged else ""))
                flag_same = (not flagged) or (OW.FLAG.exists() and
                                              OW.FLAG.read_text(encoding="utf-8") == body)
                seen.append({"argv": argv[-1], "flagged": flagged, "rc": rc,
                             "lock_takes": list(sb.lock_takes), "ran": list(sb.ran),
                             "movers": sb.movers_ran(), "rows": len(sb.rows()),
                             "files_left": left, "flag_same": flag_same,
                             "armed": list(sb.arm_calls),
                             "said": "NOTHING IS TOUCHED" in out})
    bad = [s for s in seen if s["rc"] != 0 or s["lock_takes"] or s["ran"] or s["movers"]
           or s["rows"] or s["files_left"] or not s["flag_same"] or s["armed"]
           or not s["said"]]
    if bad:
        return False, (f"a DRY run touched something — it says NOTHING IS TOUCHED and "
                       f"{len(bad)} of {len(seen)} sandboxed dry runs did not keep "
                       f"that: {bad[0]}")
    return True, (f"{len(seen)} sandboxed dry runs (full, refresh --no-fetch; with and "
                  f"without a standing flag): 0 lock takes, 0 jobs, no movers process, "
                  f"0 selfcheck rows, no file created, a standing flag byte-identical")


# "WITH THE EXPECTED OUTPUT LINES of each step" is only worth something if the
# lines are the wrapper's. So the wrapper is RUN (sandboxed, five scenarios) and
# every placeholder-free line it logs under these prefixes must be in the skill to
# the byte. Lines that carry a temp path, a stub's name, a wall-clock or the cwd
# cannot be quoted verbatim by anyone and are left out; the two slot strings are
# folded into one so the skill need not print step 5 twice.
_STATIC_PREFIXES = ("  STEP ", "  schedule: ", "  alarm left standing", "  no ORACLE_DOWN")
_STATIC_CACHE: list[str] | None = None   # the wrapper's lines do not depend on the
#                                          skill text a leg plants, so both legs share


def wrapper_static_lines() -> list[str]:
    global _STATIC_CACHE
    if _STATIC_CACHE is not None:
        return list(_STATIC_CACHE)
    scenarios = ((FULL, 0, True), (FULL, 0, False), (REFRESH, 0, False),
                 (FULL + ["--no-fetch"], 0, True), (FULL + ["--no-fetch"], 0, False),
                 (FULL, 1, False))
    found: list[str] = []
    for argv, topup_rc, flagged in scenarios:
        with Sandbox(topup_rc=topup_rc) as sb:
            if flagged:
                OW.FLAG.write_text(planted_flag_body(), encoding="utf-8")
            _, out = sb.main(argv)
            td = str(sb.td)
        for ln in out.splitlines():
            if (ln.startswith(_STATIC_PREFIXES) and td not in ln and "_stub" not in ln
                    and "identity-gate: PASS" not in ln
                    and not re.search(r"\d\.\d s\b", ln)):
                ln = ln.replace("on-demand-refresh", "on-demand-full")
                if ln not in found:
                    found.append(ln)
    # The lines only a CUT-OFF run logs, from real signals (F-SK-2h's child): the
    # CUT OFF sentence and the alarm line it ends on are placeholder-free; the DEAD
    # LOCK line carries a pid and a stamp, folded to the skill's <pid> and <iso>.
    with tempfile.TemporaryDirectory(prefix="oracle-ondemand-static-") as d:
        cut = _child(Path(d), no_trap=False, sig=signal.SIGTERM)
    found += [ln for ln in cut["out"].splitlines()
              if ln.startswith(("  CUT OFF by signal", "  STEP 7 alarm")) and ln not in found]
    with tempfile.TemporaryDirectory(prefix="oracle-ondemand-static-") as d:
        _child(Path(d), no_trap=False, sig=signal.SIGKILL)
        (Path(d) / Sandbox.TOPUP_STARTED).unlink(missing_ok=True)
        with Sandbox(td=Path(d)) as sb:
            _, out = sb.main(FULL + ["--no-fetch"])
    for ln in out.splitlines():
        if ln.startswith("  DEAD LOCK from"):
            ln = re.sub(r"\(pid \d+ is", "(pid <pid> is", ln)
            found.append(re.sub(r"stamped [^)]+\)", "stamped <iso>)", ln))
    if not any("CUT OFF" in ln for ln in found) or not any("DEAD LOCK" in ln for ln in found):
        found.append("[fixture] the cut-off child logged no CUT OFF / DEAD LOCK line")
    _STATIC_CACHE = list(found)
    return found


def _skill_probe(text: str, dry: tuple[int, str] | None,
                 static: list[str] | None = None) -> tuple[bool, str]:
    ids = step_ids()
    missing_contract = [c for c in CONTRACT_CHAIN if c not in ids]
    if missing_contract or [i for i in ids if i in CONTRACT_CHAIN] != list(CONTRACT_CHAIN):
        return False, (f"ONDEMAND_STEPS no longer carries the contract's chain in "
                       f"order: want {list(CONTRACT_CHAIN)} as an ordered subsequence "
                       f"of {ids}")
    try:
        meta, body = parse_frontmatter(text)
    except ValueError as e:
        return False, f"skill file does not parse: {e}"
    if meta.get("name") != SKILL_NAME or meta.get("description") != SKILL_DESCRIPTION:
        return False, (f"frontmatter is not the contract's: name={meta.get('name')!r} "
                       f"description={meta.get('description')!r}")
    walked = [(int(n), sid) for n, sid in _HEADING.findall(body)]
    walked_ids = [sid for _, sid in walked]
    if walked_ids != ids:
        gone = [i for i in ids if i not in walked_ids]
        extra = [i for i in walked_ids if i not in ids]
        return False, (f"missing from the skill: {gone or 'none'}; unknown to the "
                       f"wrapper: {extra or 'none'} — the skill walks "
                       f"{len(walked_ids)} step(s), ONDEMAND_STEPS has {len(ids)}, "
                       f"and the two lists must be equal in order")
    if [n for n, _ in walked] != list(range(1, len(ids) + 1)):
        return False, f"the skill's STEP numbers are not 1..{len(ids)}: {walked}"
    untold = [f"STEP {i} {sid}" for i, (sid, who, _) in enumerate(OW.ONDEMAND_STEPS, 1)
              if who == "wrapper" and f"STEP {i} {sid}" not in body]
    if untold:
        return False, (f"the skill never quotes the wrapper's own log tag for: "
                       f"{untold} — a step with no expected output")
    silent = [what for what, token in SKILL_MUST_CARRY if token not in body]
    if silent:
        return False, f"the skill is silent about: {', '.join(silent)}"
    drifted = [ln for ln in (static or []) if ln not in body]
    if drifted:
        return False, (f"{len(drifted)} line(s) the wrapper really logs are not in the "
                       f"skill verbatim — its expected outputs have drifted from the "
                       f"code: {drifted[:2]}")
    unquoted = [lead for lead in oracle_log_leads() if lead not in body]
    if unquoted:
        return False, (f"the Oracle logs line(s) the skill's STEP 5 block never shows: "
                       f"{unquoted} — {ORACLE_SRC.name} grew a line after the skill "
                       f"was written (OR-1 STEP F added '  edition …' exactly so)")
    if dry is None:
        return True, "skill text agrees with ONDEMAND_STEPS (dry run not exercised)"
    rc, out = dry
    if rc != 0:
        return False, f"--dry-run exited {rc}: {out.strip()[-300:]}"
    printed = [sid for _, sid, _ in _DRY_LINE.findall(out)]
    if printed != ids:
        return False, (f"--dry-run printed {printed}, ONDEMAND_STEPS is {ids} — the "
                       f"dry invocation does not print the chain")
    return True, (f"frontmatter name={meta['name']!r} description="
                  f"{meta['description']!r}; the skill walks {len(ids)} steps in "
                  f"ONDEMAND_STEPS order ({' -> '.join(ids)}), quotes the wrapper's "
                  f"log tag for all {sum(1 for s in OW.ONDEMAND_STEPS if s[1] == 'wrapper')} "
                  f"wrapper steps, quotes verbatim all {len(static or [])} placeholder-"
                  f"free lines the sandboxed chain logged, carries "
                  f"{len(SKILL_MUST_CARRY)} verbs/guardrails; "
                  f"the real `--job ondemand --dry-run` subprocess exited 0 and "
                  f"printed the same ordered list")


def oracle_log_leads() -> list[str]:
    """The literal LEAD of every labelled log() line in oracle_daily.py — 'ORACLE ',
    '  posture_canon.json ', '  edition ', '  fired events in the last '. The drift
    check above runs the WRAPPER and so cannot see the Oracle's own lines (its
    oracle_daily is a stand-in); this reads the real source as TEXT, by AST, the way
    the movers suite reads this lane's register. A lead that is only whitespace (the
    per-asset row, the three path lines) names nothing and is skipped."""
    leads: list[str] = []
    for n in ast.walk(ast.parse(ORACLE_SRC.read_text(encoding="utf-8"))):
        if not (isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
                and n.func.id == "log" and n.args):
            continue
        a = n.args[0]
        first = a.values[0] if isinstance(a, ast.JoinedStr) and a.values else a
        lead = first.value if isinstance(first, ast.Constant) else ""
        if isinstance(lead, str) and lead.strip() and lead not in leads:
            leads.append(lead)
    return leads



# ── THE BOARD ROW, READ OFF ITS PRODUCER ──────────────────────────────────────
# oracle_wrapper.front_page() (chain step 6, the summary the skill tells the operator
# to read back) recovers the Board rows by matching the Oracle's stdout with
# OW._BOARD_LINE. Until 2026-09-21 the ONLY producer of such a line anywhere in this
# suite was BOARD_LINES below — three string literals typed here and commented
# "oracle_daily.build_view's real line format" — with nothing tying them to
# oracle_daily.py:877, and oracle_log_leads() skips that line BY DESIGN (its lead is
# only whitespace, so it names nothing). Measured in a mirror: change `heat={heat:6.3f}`
# to `heat: {heat:6.3f}` and 0 of 18 real Board lines match, front_page() prints "no
# Board row was logged by this run (the Oracle did not get as far as the Board)" for a
# run that logged all 18 and rendered the edition — and every fixture here stays green,
# because F-SK-2a..h feed the stand-in's own literals and F-SK-1's drift detector
# returns an identical lead list for both sources. The loop closed on itself: SKILL.md
# quotes the same literal, and F-SK-1 validated the skill against this file's copy.
#
# So the f-string is RENDERED OUT OF THE PRODUCER'S SOURCE, by AST, and the wrapper's
# regex is run against THAT. Source read as TEXT: oracle_daily is never imported here.
BOARD_LOG_FN = "build_view"        # the one place a Board row is logged


def board_line_from_source(text: str) -> str:
    """oracle_daily's OWN per-asset log f-string (the whitespace-lead JoinedStr inside
    build_view), rendered with stand-in values."""
    tree = ast.parse(text)
    fn = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)
              and n.name == BOARD_LOG_FN)
    segs = [ast.get_source_segment(text, n.args[0])
            for n in ast.walk(fn)
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
            and n.func.id == "log" and n.args
            and isinstance(n.args[0], ast.JoinedStr)]
    if len(segs) != 1:
        raise ValueError(f"{BOARD_LOG_FN} has {len(segs)} f-string log() calls, "
                         f"expected exactly 1 — the Board row")
    src = "(" + "\n".join(l.strip() for l in segs[0].splitlines()) + ")"

    class _St:
        board_word = "ARMED"

    return eval(src, {}, {"sym": "BTCUSDT", "st": _St(), "heat": 6.248,
                          "reg": [0] * 35, "clusters": [0] * 14,
                          "atr_d": 2376.77, "len": len})


def _board_coupling() -> list[str]:
    """The wrapper's _BOARD_LINE against the line oracle_daily really logs, and the
    three literals below against the same line's column layout."""
    bad = []
    try:
        line = board_line_from_source(ORACLE_SRC.read_text(encoding="utf-8"))
    except Exception as e:
        return [f"the Board row could not be rendered from {BOARD_LOG_FN}() in "
                f"{ORACLE_SRC.name}: {e.__class__.__name__}: {e} — front_page() reads "
                f"that line and this suite can no longer say whether it still matches"]
    m = OW._BOARD_LINE.match(line)
    if not m:
        bad.append(f"oracle_wrapper._BOARD_LINE does not match the line "
                   f"{BOARD_LOG_FN}() really logs ({line!r}) — front_page() would say "
                   f"'the Oracle did not get as far as the Board' for a run that "
                   f"logged every row")
        return bad
    got = (m.group("sym"), m.group("station"), float(m.group("heat")))
    if got != ("BTCUSDT", "ARMED", 6.248):
        bad.append(f"oracle_wrapper._BOARD_LINE matched the producer's line but "
                   f"recovered {got}, not ('BTCUSDT', 'ARMED', 6.248) — the summary "
                   f"would print the wrong symbol, station or heat")
    for lit in BOARD_LINES:
        if not OW._BOARD_LINE.match(lit):
            bad.append(f"this file's stand-in Board literal {lit!r} does not match "
                       f"_BOARD_LINE — the sandbox is feeding the wrapper a line the "
                       f"wrapper cannot read")
    ref = OW._BOARD_LINE.match(BOARD_LINES[1])
    if ref and (ref.group("sym"), ref.group("station"), float(ref.group("heat"))) != got:
        bad.append(f"this file's BOARD_LINES[1] parses to "
                   f"{(ref.group('sym'), ref.group('station'), float(ref.group('heat')))} "
                   f"and the producer's own line to {got} — the stand-in is STANDING IN "
                   f"FOR the producer instead of being PINNED TO it")
    return bad


def _board_coupling_break() -> list[str]:
    """Two perturbations a real edit could produce. If either still matches, the leg
    passed and this fixture is void."""
    text = ORACLE_SRC.read_text(encoding="utf-8")
    out = []
    for name, mut in (
            ("`heat={heat:6.3f}` -> `heat: {heat:6.3f}` (the one reproduced: 0 of 18 "
             "real rows match)",
             text.replace("heat={heat:6.3f}", "heat: {heat:6.3f}")),
            ("the leading two spaces dropped from the row",
             text.replace('f"  {sym:14}', 'f"{sym:14}'))):
        if mut == text:
            out.append(f"BOARD PLANT ({name}) -> GREEN: the plant could not be planted")
            continue
        try:
            line = board_line_from_source(mut)
        except Exception as e:
            out.append(f"BOARD PLANT ({name}) -> RED: {e.__class__.__name__}: {e}")
            continue
        m = OW._BOARD_LINE.match(line)
        out.append(f"BOARD PLANT ({name}) -> "
                   + (f"GREEN (FIXTURE IS VOID): _BOARD_LINE still matches {line!r}"
                      if m else f"RED: _BOARD_LINE does not match {line!r}"))
    return out


def _skill_real() -> tuple[bool, str]:
    if not SKILL.exists():
        return False, f"{SKILL.relative_to(ROOT)} does not exist"
    before = _LANE_BEFORE if _LANE_BEFORE is not None else _lane_stamp()
    dry = _dry_run()
    after = _lane_stamp()
    if before != after:
        return False, (f"the live lane changed across this fixture's dry runs (stamped "
                       f"before the FIRST of them): before {before} after {after} — a "
                       f"dry run that writes, or another run writing to the live lane "
                       f"while this fixture ran")
    ok_dry, dry_detail = _dry_in_sandbox(plant=False)
    if not ok_dry:
        return False, dry_detail
    ok, detail = _skill_probe(SKILL.read_text(encoding="utf-8"), dry,
                              wrapper_static_lines())
    board = _board_coupling()
    if board:
        return False, "; ".join(board)
    line = board_line_from_source(ORACLE_SRC.read_text(encoding="utf-8"))
    return ok, detail + (f"; every labelled Oracle log lead {oracle_log_leads()} is in "
                         f"the skill; the Board row rendered OUT OF "
                         f"{BOARD_LOG_FN}()'s own f-string in {ORACLE_SRC.name} is "
                         f"{line!r}, oracle_wrapper._BOARD_LINE matches it and "
                         f"recovers ('BTCUSDT', 'ARMED', 6.248), and all "
                         f"{len(BOARD_LINES)} stand-in literals in this file match it "
                         f"with the same column layout — the sandbox's Board lines are "
                         f"PINNED TO the producer, not typed beside it; live flag, "
                         f"lock and selfcheck log byte-untouched "
                         f"from before the first dry run of the suite; {dry_detail}"
                         if ok else "")


def _skill_break() -> tuple[bool, str]:
    """A planted copy of the skill with ONE step heading removed — once per step,
    so every step is shown to be load-bearing, not just the first one tried."""
    if not SKILL.exists():
        return False, f"{SKILL.relative_to(ROOT)} does not exist — nothing to plant in"
    text = SKILL.read_text(encoding="utf-8")
    dry = _dry_run()
    static = wrapper_static_lines()
    slipped, reasons = [], []
    for sid in step_ids():
        planted, n = re.subn(rf"(?m)^#{{2,4}}\s*STEP\s+\d+\s*·\s*{re.escape(sid)}\s*$\n?",
                             "", text)
        if n != 1:
            return True, f"could not plant: heading for {sid} found {n} time(s)"
        ok, detail = _skill_probe(planted, dry, static)
        if ok:
            slipped.append(sid)
        elif sid == "movers-fetch":
            reasons.append(detail)
    # and one planted copy whose steps are all there but whose quoted output lies
    needle = "STEP 4 scope-topup: NOT CLEAN"
    if text.count(needle) != 1:
        return True, f"could not plant: {needle!r} found {text.count(needle)} time(s)"
    ok, drift_detail = _skill_probe(text.replace(needle, "STEP 4 scope-topup: not clean"),
                                    dry, static)
    if ok:
        slipped.append("a drifted expected-output line")
    # a planted copy that never shows the Oracle's '  edition ' line (the STEP F drift)
    lead = "  edition "
    if lead not in oracle_log_leads() or lead not in text:
        return True, f"could not plant: {lead!r} is not both an Oracle lead and in the skill"
    ok, lead_detail = _skill_probe(text.replace(lead, "  edtion "), dry, static)
    if ok:
        slipped.append("an Oracle log line the skill never shows")
    # a planted copy with the B2 prose taken back out
    ok, b2_detail = _skill_probe(text.replace("run_in_background", "a long timeout"),
                                 dry, static)
    if ok:
        slipped.append("the detached-run instruction")
    # and a planted DRY RUN that is not dry (verifier mutation M11)
    ok, dry_detail = _dry_in_sandbox(plant=True)
    if ok:
        slipped.append("a dry run that takes the lock")
    board = _board_coupling_break()
    if any("GREEN" in b for b in board):
        return True, " ‖ ".join(board)
    if slipped:
        return True, f"a skill missing {slipped} still passed"
    return False, (" ‖ ".join(board)
                   + f" || {len(step_ids())} planted copies, each with one step removed, "
                   f"all red; e.g. without movers-fetch: {reasons[0]} || 1 planted "
                   f"copy with one quoted log line altered, red: {drift_detail[:200]} "
                   f"|| 1 without the Oracle's edition line, red: {lead_detail[:160]} "
                   f"|| 1 without the detached-run instruction, red: {b2_detail[:120]} "
                   f"|| a planted dry run that takes the lock, red: {dry_detail[:220]}")


def f_sk_1() -> None:
    global _LANE_BEFORE
    _LANE_BEFORE = _lane_stamp()
    prove("F-SK-1", "THE SKILL — the file parses, walks every step of ONDEMAND_STEPS "
                    "in order, and a dry invocation prints the same list",
          _skill_break, _skill_real)


# ══════════════════════════════════ F-SK-2 / F-SK-3 · THE SANDBOX

FLAG_SENTINEL = "F-SK-2-SENTINEL — a failure planted by the fixture before the run"
BOARD_LINES = (                      # oracle_daily.build_view's real line format
    "  ETHUSDT        STALKING   heat= 1.500 levels= 31 clusters= 12 atr_d=101.5",
    "  BTCUSDT        ARMED      heat= 6.248 levels= 35 clusters= 14 atr_d=2376.77",
    "  SOLUSDT        DEAD       heat= 0.250 levels= 22 clusters=  9 atr_d=6.1",
)


def planted_flag_body() -> str:
    return "\n".join([
        "UTC   2026-09-21T09:55:22.000000+00:00", "JOB   topup", "SLOT  topup",
        "EXIT  1", "", "LAST 1 TRACEBACK LINE(S), NEWEST FAILURE LAST:",
        FLAG_SENTINEL, "", OW.FLAG_SENTENCE, ""])


class Sandbox:
    """The real wrapper module, with its far ends replaced and its paths moved."""
    ATTRS = ("ROOT", "FLAG", "LOCK", "SELFCHECK", "MOVERS_SCRIPT", "MOVERS_DIR",
             "MOVERS_TIMEOUT_S", "MOVERS_FAILURE_HOLDS_FLAG",
             "acquire_lock", "reclaim_dead_lock", "live_lock_holder",
             "_cut_render_path", "trap_cut_off",
             "run_topup", "run_oracle", "run_movers", "self_checks",
             "reschedule_if_drifted", "arm", "write_plist", "names_ondemand",
             "show_standing_flag", "ondemand_flag_action", "ondemand_skips",
             "ondemand_plan_lines", "identity_gate", "install_refusal")
    MOVERS_MODES = ("ok", "no-json", "exit1", "absent", "hang")
    TOPUP_STARTED = "topup.started"          # F-SK-2h: the child's "cut me now" marker
    ORACLE_STARTED = "oracle.started"        # the same, for a cut INSIDE STEP 5

    def __init__(self, topup_rc: int = 0, late_flag: bool = False, movers: str = "ok",
                 arm_raises: bool = True, topup_hangs: bool = False,
                 oracle_hangs: bool = False, td: Path | None = None):
        assert movers in self.MOVERS_MODES, movers
        self.topup_rc, self.late_flag, self.movers = topup_rc, late_flag, movers
        self.arm_raises, self.topup_hangs, self.given_td = arm_raises, topup_hangs, td
        self.oracle_hangs = oracle_hangs
        self.ran: list[str] = []            # jobs that actually ran, in order
        self.schedule_calls: list[str] = []  # any call into the schedule machinery
        self.arm_calls: list[str] = []       # every arm()/write_plist() call, by label
        self.lock_takes: list[str] = []      # every acquire_lock(who), granted or not
        self.lock_seen: dict[str, bool] = {}  # job -> was the lock held while it ran

    def __enter__(self):
        self.keep = {k: getattr(OW, k) for k in self.ATTRS}
        self.keep_failures = list(OW.FAILURES)
        self.keep_od = sys.modules.get("oracle_daily")
        self.keep_home = os.environ.get("HOME")
        if self.given_td is None:
            self._td = tempfile.TemporaryDirectory(prefix="oracle-ondemand-fx-")
            td = self.td = Path(self._td.name)
        else:                               # F-SK-2h: the parent owns the directory
            self._td = None
            td = self.td = Path(self.given_td)
        OW.FLAG = td / "ORACLE_DOWN.flag"
        OW.LOCK = td / ".oracle.lock"
        OW.SELFCHECK = td / "selfcheck_log.jsonl"
        OW.MOVERS_DIR = td / "movers"
        OW.MOVERS_SCRIPT = td / "oracle_movers_stub.py"
        self.movers_marker = td / "movers.ran"
        # The stand-in organ, one per way the real one can end (OR-1 STEP E's CLI
        # contract: exit 0 = json written; exit 1 = fetch failed). `ok` WRITES a
        # movers json — the first version of this stub did not, so every "clean"
        # scenario was in truth the no-json case and no failing case existed at all.
        stub = ["from pathlib import Path",
                f"held = Path({str(OW.LOCK)!r}).exists()",
                f"Path({str(self.movers_marker)!r}).write_text(f'lock={{held}}')"]
        if self.movers == "ok":
            stub += [f"d = Path({str(OW.MOVERS_DIR)!r}); d.mkdir(parents=True, exist_ok=True)",
                     "(d / 'movers_2026-09-21.json').write_text('{\"status\": \"OK\"}')",
                     "print('MOVERS-STUB universe 0 · fetched nothing (fixture)')"]
        elif self.movers == "no-json":
            stub += ["print('MOVERS-STUB universe 0 · fetched nothing (fixture)')"]
        elif self.movers == "exit1":
            stub += ["print('MOVERS-STUB status FAIL · the wire is down (fixture)')",
                     "raise SystemExit(1)"]
        elif self.movers == "hang":
            stub += ["import time", "time.sleep(60)"]
            OW.MOVERS_TIMEOUT_S = 1
        if self.movers != "absent":
            OW.MOVERS_SCRIPT.write_text("\n".join(stub) + "\n")
        OW.FAILURES.clear()

        real_acquire = self.keep["acquire_lock"]

        def _acquire(who, log=print):
            self.lock_takes.append(who)
            return real_acquire(who, log=log)
        OW.acquire_lock = _acquire

        def _schedule(name):
            def _stub(label, log=print):
                self.schedule_calls.append(f"{name}({label})")
                raise AssertionError(f"{name} called under a fixture")
            return _stub
        OW.reschedule_if_drifted = _schedule("reschedule_if_drifted")

        def _arming(name):
            def _stub(label, log=print, **_kw):     # **_kw: arm(enable=) since OR-2 R-4
                self.arm_calls.append(f"{name}({label})")
                self.schedule_calls.append(f"{name}({label})")
                if self.arm_raises:
                    raise AssertionError(f"{name} called under a fixture")
                return {"label": label, "stub": True}
            return _stub
        OW.arm = _arming("arm")
        OW.write_plist = _arming("write_plist")

        def _topup(slot, log=print):
            self.ran.append(f"topup[{slot}]")
            self.lock_seen["topup"] = OW.LOCK.exists()
            log(f"ORACLE TOP-UP · slot={slot} · 0 pair(s) from the pinned scope (stub)")
            if self.topup_hangs:            # F-SK-2h: a wire-down top-up, in small
                (td / self.TOPUP_STARTED).write_text(str(os.getpid()))
                time.sleep(120)
            if self.late_flag and OW.FLAG.exists():
                log(OW.FLAG.read_text(encoding="utf-8").rstrip("\n"))
            log(f"  top-up {'PASS' if self.topup_rc == 0 else 'FAIL'}: +0 rows across "
                f"0 pair(s), 0 gap(s)")
            return self.topup_rc
        OW.run_topup = _topup

        def _od_run(slot="full", as_of_ms=None, log=print):
            self.ran.append(f"oracle[{slot}]")
            self.lock_seen["oracle"] = OW.LOCK.exists()
            log(f"ORACLE {slot} · 2026-09-21 · lens 4h")
            for ln in BOARD_LINES:
                log(ln)
            out = td / "oracle_2026-09-21.html"
            out.write_text("<html><head><style>.stale{color:red} /* LATE EDITION */"
                           "</style></head><body><h1>THE DAILY ORACLE</h1>"
                           "<div class=\"stale\">LATE EDITION — wire stale since "
                           "2026-09-20T20:00Z</div></body></html>", encoding="utf-8")
            if self.oracle_hangs:
                # RUN()'S OWN ORDER, the window the review found: oracle_daily.run()
                # writes the WHOLE html (oracle_daily.py:2360) and logs this line
                # (:2361) BEFORE it writes the tape (:2364), the calibration (:2366)
                # and — back in the wrapper — the selfcheck row. A signal here leaves
                # an edition on disk that no self-check ever saw.
                b = out.read_bytes()
                log(f"  {out} {len(b):,} B sha256 {hashlib.sha256(b).hexdigest()}")
                (td / self.ORACLE_STARTED).write_text(str(os.getpid()))
                time.sleep(120)
            return {"html": out,
                    "html_sha": hashlib.sha256(out.read_bytes()).hexdigest()}
        sys.modules["oracle_daily"] = types.SimpleNamespace(run=_od_run)

        def _checks(log=print):
            res = {k: {"pass": True, "detail": "stub"} for k in
                   ("refresh_idempotence", "thumbnail_provenance",
                    "tape_append_integrity")}
            for k in res:
                log(f"  selfcheck {k}: PASS")
            return res
        OW.self_checks = _checks
        return self

    def __exit__(self, *exc):
        for k, v in self.keep.items():
            setattr(OW, k, v)
        OW.FAILURES[:] = self.keep_failures
        if self.keep_od is None:
            sys.modules.pop("oracle_daily", None)
        else:
            sys.modules["oracle_daily"] = self.keep_od
        if self.keep_home is None:
            os.environ.pop("HOME", None)
        else:
            os.environ["HOME"] = self.keep_home
        if self._td is not None:
            self._td.cleanup()
        return False

    def main(self, argv: list[str], allow_install: bool = False) -> tuple[int, str]:
        # belt and braces: refuse to drive main() at anything but the sandbox
        assert OW.FLAG.parent == self.td and OW.LOCK.parent == self.td \
            and OW.SELFCHECK.parent == self.td, "sandbox not in place"
        # --install reaches main() ONLY from F-SK-2e, ONLY by asking, and ONLY while
        # both arming functions are this sandbox's recorders: the real arm() rewrites
        # a retained plist and runs launchctl bootout + bootstrap.
        assert allow_install or "--install" not in argv, "--install without asking"
        assert OW.arm is not self.keep["arm"] and \
            OW.write_plist is not self.keep["write_plist"], "arming is not stubbed"
        sink = io.StringIO()
        with contextlib.redirect_stdout(sink):
            rc = OW.main(list(argv))
        return rc, sink.getvalue()

    def rows(self) -> list[dict]:
        if not OW.SELFCHECK.exists():
            return []
        return [json.loads(l) for l in OW.SELFCHECK.read_text().splitlines() if l.strip()]

    def movers_ran(self) -> bool:
        return self.movers_marker.exists()

    def locks(self) -> dict:
        seen = dict(self.lock_seen)
        if self.movers_marker.exists():
            seen["movers"] = self.movers_marker.read_text() == "lock=True"
        return seen


FULL = ["--job", "ondemand", "--slot", "on-demand-full"]
REFRESH = ["--job", "ondemand", "--slot", "on-demand-refresh"]
_JOB_LINE = re.compile(r"^(  STEP [345] |    movers\| |ORACLE TOP-UP ·|ORACLE on-demand)", re.M)


# ── F-SK-2a · the standing flag is printed FIRST

def _flag_first(late: bool) -> tuple[bool, str]:
    """`late=True` replants the world this step exists to end: nothing is said at
    step 2, and the flag's text only turns up once a job is already running."""
    with Sandbox(late_flag=late) as sb:
        body = planted_flag_body()
        OW.FLAG.write_text(body, encoding="utf-8")
        if late:
            OW.show_standing_flag = lambda log=print: False
        rc, out = sb.main(FULL)
    first_job = _JOB_LINE.search(out)
    if first_job is None:
        return False, "no job line in the captured run — the chain never started"
    at = out.find(body.rstrip("\n"))
    if at < 0:
        return False, ("a flag was standing and its body was never printed verbatim "
                       "— the operator is handed an edition with the alarm unread")
    if at > first_job.start():
        return False, (f"the flag body IS printed, but at offset {at}, AFTER the first "
                       f"job line at offset {first_job.start()} "
                       f"({first_job.group(0).strip()!r}) — not FIRST")
    gate = out.find("STEP 1 identity-gate: PASS")
    if not (0 <= gate < at):
        return False, "the flag was printed before the identity gate had passed"
    return True, (f"standing flag printed verbatim ({len(body.splitlines())} lines, "
                  f"sentinel included) at offset {at}, after the identity gate "
                  f"(offset {gate}) and before the first job line at offset "
                  f"{first_job.start()} ({first_job.group(0).strip()!r}); chain rc {rc}")


def f_sk_2a() -> None:
    prove("F-SK-2a", "FLAG FIRST — a standing ORACLE_DOWN.flag is printed verbatim "
                     "before any job line",
          lambda: _flag_first(late=True), lambda: _flag_first(late=False))


# ── F-SK-2b · the selfcheck row carries the on-demand slot

def _slot_tag(legacy: bool) -> tuple[bool, str]:
    """`legacy=True` replants the untagged world: the chain hands run_oracle the
    clock's own slot string, which is what two hand-run commands produced."""
    seen = []
    with Sandbox() as sb:
        if legacy:
            real = OW.run_oracle
            OW.run_oracle = (lambda slot, zr, started, log=print, catchup=False:
                             real(slot.replace("on-demand-", ""), zr, started,
                                  log=log, catchup=catchup))
        for argv, want in ((FULL, "on-demand-full"), (REFRESH, "on-demand-refresh")):
            n = len(sb.rows())
            rc, out = sb.main(argv)
            new = sb.rows()[n:]
            if len(new) != 1:
                return False, f"{want}: the run wrote {len(new)} selfcheck row(s), want 1"
            seen.append((want, new[0].get("slot"), new[0].get("verdict"), rc,
                         new[0].get("catchup")))
    wrong = [(w, g) for w, g, *_ in seen if w != g]
    if wrong:
        return False, (f"selfcheck row(s) carry the wrong slot (want, got): {wrong} — a "
                       f"run-based gate cannot tell this edition from the clock's")
    if any(v != "PASS" or rc != 0 or cu for _, _, v, rc, cu in seen):
        return False, f"rows tagged correctly but not clean PASS rows: {seen}"
    return True, (f"two runs through the real main() and the wrapper's own "
                  f"append_selfcheck: rows read back off disk carry slot="
                  f"{[g for _, g, *_ in seen]}, verdict PASS, catchup false, exit 0")


def f_sk_2b() -> None:
    prove("F-SK-2b", "THE TAG — the selfcheck row of an on-demand run carries "
                     "slot on-demand-full | on-demand-refresh",
          lambda: _slot_tag(legacy=True), lambda: _slot_tag(legacy=False))


# ── F-SK-2c · the hazard: failed top-up + clean render

def _hazard(two_commands: bool) -> tuple[bool, str]:
    """`two_commands=True` IS the 2026-09-21 morning, replayed through the legacy
    jobs: `--job topup` fails and raises the flag, `--job oracle` renders clean on
    the stale cache and clears it."""
    with Sandbox(topup_rc=1) as sb:
        if two_commands:
            rc_t, out_t = sb.main(["--job", "topup", "--slot", "topup"])
            raised = OW.FLAG.exists()
            rc, out = sb.main(["--job", "oracle", "--slot", "full"])
            out = out_t + out
            if not raised:
                return True, "could not plant: the legacy failed top-up raised no flag"
        else:
            rc, out = sb.main(FULL)
        standing = OW.FLAG.exists()
        body = OW.FLAG.read_text(encoding="utf-8") if standing else ""
        rows, ran = sb.rows(), list(sb.ran)
    if not any(r.startswith("topup") for r in ran) or not any(
            r.startswith("oracle") for r in ran):
        return False, f"the scenario did not run both jobs: {ran}"
    if not rows or rows[-1].get("verdict") != "PASS":
        return False, ("the render did not run clean after the failed top-up — ruling "
                       "T-3 says a failed top-up does NOT block the edition")
    if rc == 0 or not standing:
        return False, (f"top-up FAILED, render clean: final exit {rc}, flag standing="
                       f"{standing} — the clean render erased the alarm the failed "
                       f"top-up raised, which is the 2026-09-21 07:00 hazard exactly")
    want = [("the job", "JOB   ondemand"), ("the slot", "SLOT  on-demand-full"),
            ("the exit code", f"EXIT  {rc}"), ("why", "TOP-UP DID NOT PASS"),
            ("the sentence", OW.FLAG_SENTENCE)]
    silent = [n for n, t in want if t not in body]
    if silent:
        return False, f"flag standing but silent about: {', '.join(silent)}"
    if "ALARM CLEARED" in out:
        return False, "the flag stands at exit but was CLEARED and re-raised on the way"
    return True, (f"jobs ran {ran}; top-up rc 1, render clean (selfcheck row PASS, "
                  f"edition not blocked — T-3); chain exit {rc}; ORACLE_DOWN.flag "
                  f"STANDING at exit carrying job ondemand, slot, exit code and "
                  f"'TOP-UP DID NOT PASS'; never cleared on the way")


def f_sk_2c() -> None:
    prove("F-SK-2c", "THE HAZARD — a failed top-up under a clean render must exit "
                     "nonzero with the flag STANDING",
          lambda: _hazard(two_commands=True), lambda: _hazard(two_commands=False))


# ── F-SK-2d · --no-fetch skips both fetches and never clears a standing flag

def _no_fetch(plant: str | None) -> tuple[bool, str]:
    with Sandbox() as sb:
        body = planted_flag_body()
        OW.FLAG.write_text(body, encoding="utf-8")
        if plant == "old-flag-rule":          # any clean job clears — the T-7 rule
            OW.ondemand_flag_action = (lambda rc, no_fetch, movers_failed=False:
                                       "raise" if rc else "clear")
        elif plant == "no-skips":             # the verb accepted and ignored
            OW.ondemand_skips = lambda slot, no_fetch: {}
        rc, out = sb.main(FULL + ["--no-fetch"])
        ran, movers = list(sb.ran), sb.movers_ran()
        after = OW.FLAG.read_text(encoding="utf-8") if OW.FLAG.exists() else None
    if movers or any(r.startswith("topup") for r in ran):
        return False, (f"--no-fetch still fetched: movers ran={movers}, jobs={ran} — "
                       f"a cache-only edition that touches the wire")
    if ran != ["oracle[on-demand-full]"]:
        return False, f"--no-fetch did not render exactly once: {ran}"
    if rc != 0:
        return False, f"clean cache-only render exited {rc}"
    if after is None:
        return False, ("a --no-fetch run CLEARED the standing flag — a run that never "
                       "touched the wire gave the all-clear for it")
    if after != body:
        return False, "the standing flag was rewritten by a clean --no-fetch run"
    if "alarm left standing" not in out or "STEP 3 movers-fetch: SKIPPED" not in out \
            or "STEP 4 scope-topup: SKIPPED" not in out:
        return False, "skips or the standing alarm are not SAID in the log"
    if plant is None:
        # the verb MISTYPED must not become a run that fetches
        with Sandbox() as sb:
            rc_typo, out_typo = sb.main(FULL + ["--nofetch"])
            typo = (rc_typo, list(sb.ran), sb.movers_ran(), len(sb.lock_takes))
        if typo != (2, [], False, 0) or "--nofetch" not in out_typo:
            return False, (f"a mistyped `--nofetch` was not refused before any action: "
                           f"(rc, jobs, movers, lock takes) = {typo}")
    return True, (f"jobs ran {ran}, movers organ not started, top-up not called; exit "
                  f"{rc}; the planted flag is byte-identical at exit and the log says "
                  f"'alarm left standing' and SKIPPED for steps 3 and 4; a mistyped "
                  f"`--nofetch` HALTs exit 2 with nothing touched")


def _no_fetch_break() -> tuple[bool, str]:
    legs = {p: _no_fetch(p) for p in ("old-flag-rule", "no-skips")}
    slipped = [p for p, (ok, _) in legs.items() if ok]
    if slipped:
        return True, f"plant(s) {slipped} passed"
    return False, " || ".join(f"[{p}] {d[:150]}" for p, (_, d) in legs.items())


def f_sk_2d() -> None:
    prove("F-SK-2d", "CACHE-ONLY — --no-fetch skips the movers fetch and the top-up, "
                     "and never clears a standing flag",
          _no_fetch_break, lambda: _no_fetch(None))


# ── F-SK-2e · the schedule machinery is never entered

INSTALL_ARGVS = (                    # every one NAMES the on-demand edition
    FULL + ["--install"],
    ["--job", "ondemand", "--dry-run", "--install"],                  # verifier B1
    ["--install", "--job", "ondemand", "--slot", "on-demand-refresh", "--no-fetch"],
    ["--job=ondemand", "--install"],                                  # --job mistyped
    ["--slot", "on-demand-full", "--install"],                        # --job forgotten
)


def _install_refused(install_first: bool) -> tuple[bool, str]:
    """Verifier finding B1. main() looked for --install BEFORE it dispatched the
    on-demand job, so `--job ondemand --dry-run --install` armed all five suspended
    agents, printed no dry run, and exited 0 — and this suite could not see it,
    because Sandbox.main asserted --install was never handed over.
    `install_first=True` replants that order: nothing is recognised as on-demand
    ahead of --install. arm() is a recorder that does NOT raise here, so the planted
    world runs to its own exit 0 exactly as the real one did."""
    seen = []
    for argv in INSTALL_ARGVS:
        with Sandbox(arm_raises=False) as sb:
            body = planted_flag_body()
            OW.FLAG.write_text(body, encoding="utf-8")
            if install_first:
                OW.names_ondemand = lambda argv: False
                # OR-2 R-4: the world this plant rebuilds had no sentinel guard
                # either. Left in place, the guard would refuse these argvs on its
                # own and the plant would go red for a reason that is not B1's.
                OW.install_refusal = lambda argv: None
            rc, out = sb.main(argv, allow_install=True)
            seen.append({"argv": " ".join(argv), "rc": rc, "armed": len(sb.arm_calls),
                         "lock_takes": len(sb.lock_takes), "ran": list(sb.ran),
                         "movers": sb.movers_ran(), "rows": len(sb.rows()),
                         "flag_same": OW.FLAG.exists() and
                         OW.FLAG.read_text(encoding="utf-8") == body,
                         "said": "REFUSES --install" in out and "Nothing was touched" in out,
                         "arming_line": "ORACLE — arming" in out})
    bad = [s for s in seen if s["rc"] != 2 or s["armed"] or s["lock_takes"] or s["ran"]
           or s["movers"] or s["rows"] or not s["flag_same"] or not s["said"]
           or s["arming_line"]]
    if bad:
        return False, (f"{len(bad)} of {len(seen)} argv(s) naming the on-demand edition "
                       f"reached --install: e.g. `{bad[0]['argv']}` -> exit "
                       f"{bad[0]['rc']}, arm()/write_plist() called {bad[0]['armed']}x, "
                       f"'ORACLE — arming' printed={bad[0]['arming_line']} — the real "
                       f"arm() rewrites a retained plist and runs launchctl bootout + "
                       f"bootstrap on a label the operator suspended")
    return True, (f"{len(seen)} argvs carrying --install beside the on-demand edition "
                  f"(after it, before it, with --dry-run, with --job= mistyped, with "
                  f"--job forgotten): every one HALTs exit 2 saying 'REFUSES --install', "
                  f"0 arm()/write_plist() calls, 0 lock takes, 0 jobs, a standing flag "
                  f"byte-identical")


def _schedule_untouched(legacy_path: bool) -> tuple[bool, str]:
    """`legacy_path=True` is the on-demand edition built the cheap way — the old
    `--job oracle` path with an on-demand slot string — which walks straight into
    the reschedule loop. (The loop swallows exceptions, so the recorders RECORD as
    well as raise: a raise alone would vanish into `reschedule check failed`.)"""
    calls, outs, n_runs = [], [], 0
    scenarios = ([(["--job", "oracle", "--slot", "on-demand-full"], 0)] if legacy_path
                 else [(FULL, 0), (REFRESH, 0), (FULL + ["--no-fetch"], 0), (FULL, 1)])
    for argv, topup_rc in scenarios:
        with Sandbox(topup_rc=topup_rc) as sb:
            _, out = sb.main(argv)
            calls += sb.schedule_calls
            outs.append(out)
            n_runs += 1
    if calls:
        return False, (f"{len(calls)} call(s) into the schedule machinery from an "
                       f"on-demand edition: {calls[:3]}… — on drift that path rewrites "
                       f"a retained plist and bootstraps it, under a suspended clock")
    loud = [o for o in outs if "schedule OK on" in o or "SCHEDULE DRIFT" in o]
    if loud:
        return False, "no recorded call, yet the log still claims a schedule check"
    unsaid = [i for i, o in enumerate(outs) if "schedule: SUSPENDED by operator ruling "
              "2026-09-21" not in o]
    if unsaid:
        return False, f"run(s) {unsaid} skipped the check without SAYING so"
    return True, (f"{n_runs} on-demand runs (full, refresh, --no-fetch, failed top-up) "
                  f"through the real main(): 0 calls to reschedule_if_drifted, 0 to "
                  f"arm, no 'schedule OK' claim, and every log carries the SUSPENDED line")


def _suspended_break() -> tuple[bool, str]:
    legs = {"the legacy path": _schedule_untouched(legacy_path=True),
            "--install first": _install_refused(install_first=True)}
    slipped = [p for p, (ok, _) in legs.items() if ok]
    if slipped:
        return True, f"plant(s) {slipped} passed"
    return False, " || ".join(f"[{p}] {d[:330]}" for p, (_, d) in legs.items())


def _suspended_real() -> tuple[bool, str]:
    details = []
    for leg in (lambda: _schedule_untouched(legacy_path=False),
                lambda: _install_refused(install_first=False)):
        ok, detail = leg()
        if not ok:
            return False, detail
        details.append(detail)
    return True, " || ".join(details)


def f_sk_2e() -> None:
    prove("F-SK-2e", "THE SUSPENDED CLOCK — no on-demand argv may enter "
                     "reschedule_if_drifted, arm or --install",
          _suspended_break, _suspended_real)


# ── F-SK-2g · a failing movers organ never fails the edition

def _movers_failure(plant: str | None) -> tuple[bool, str]:
    """Verifier finding 3: the movers stub always exited 0, so 'a movers failure
    does NOT fail the edition and does not raise the flag' was asserted nowhere
    (mutation M9 — a movers failure forcing rc 1 — stayed GREEN 8/8).
    Plants: 'fails-the-edition' is M9; 'policy-ignored' is a flag rule that never
    hears about the movers verdict, so the [VETO] row MOVERS_FAILURE_HOLDS_FLAG
    would be a constant nothing reads."""
    real_movers, real_action = OW.run_movers, OW.ondemand_flag_action

    def _plant():
        if plant == "fails-the-edition":
            def _movers(log=print):
                res = real_movers(log=log)
                if not res["ok"]:
                    raise RuntimeError("movers organ failed")
                return res
            OW.run_movers = _movers
        elif plant == "policy-ignored":
            OW.ondemand_flag_action = (lambda rc, no_fetch, movers_failed=False:
                                       real_action(rc, no_fetch))

    said = {"exit1": "exited 1", "absent": "does not exist", "hang": "no answer inside",
            "no-json": "NO movers_*.json"}
    seen = {}
    for mode, phrase in said.items():
        with Sandbox(movers=mode) as sb:
            _plant()
            rc, out = sb.main(FULL)
            rows = sb.rows()
            seen[mode] = {"rc": rc, "ran": list(sb.ran), "flag": OW.FLAG.exists(),
                          "verdict": rows[-1].get("verdict") if rows else None,
                          "said": phrase in out and
                          ("WIRE DOWN for movers" in out or mode == "no-json"),
                          "started": sb.movers_ran()}
    want_ran = ["topup[on-demand]", "oracle[on-demand-full]"]
    bad = {m: s for m, s in seen.items() if s["rc"] != 0 or s["flag"] or
           s["ran"] != want_ran or s["verdict"] != "PASS" or not s["said"]}
    if bad:
        return False, (f"a movers failure changed the edition — (mode -> what "
                       f"happened): {bad} — it must log WIRE DOWN for movers, leave "
                       f"the exit code alone, raise no flag, and the top-up and the "
                       f"render must still run")
    if seen["absent"]["started"] or not seen["exit1"]["started"]:
        return False, f"the stub organ did not behave as planted: {seen}"

    # THE UNRULED HALF, held to its constant: what a movers failure does to a flag
    # that was ALREADY standing when the top-up and the render both came back clean.
    policy = {}
    for holds, mode, argv in ((False, "exit1", FULL), (True, "exit1", FULL),
                              (True, "ok", FULL), (True, "exit1", REFRESH)):
        with Sandbox(movers=mode) as sb:
            _plant()
            OW.MOVERS_FAILURE_HOLDS_FLAG = holds
            body = planted_flag_body()
            OW.FLAG.write_text(body, encoding="utf-8")
            rc, out = sb.main(argv)
            standing = OW.FLAG.exists()
            policy[(holds, mode, argv[-1])] = (
                rc, "STANDING" if standing else "CLEARED",
                standing and OW.FLAG.read_text(encoding="utf-8") == body,
                "MOVERS_FAILURE_HOLDS_FLAG is set" in out)
    want = {(False, "exit1", "on-demand-full"): (0, "CLEARED", False, False),
            (True, "exit1", "on-demand-full"): (0, "STANDING", True, True),
            (True, "ok", "on-demand-full"): (0, "CLEARED", False, False),
            (True, "exit1", "on-demand-refresh"): (0, "CLEARED", False, False)}
    if policy != want:
        diff = {k: (policy[k], want[k]) for k in want if policy[k] != want[k]}
        return False, (f"MOVERS_FAILURE_HOLDS_FLAG is not what decides — (holds, "
                       f"movers, slot) -> (got, want): {diff}")
    if OW.ONDEMAND_REGISTER["MOVERS_FAILURE_HOLDS_FLAG"]["ruled"] is not False or \
            "[VETO]" not in OW.ONDEMAND_REGISTER["MOVERS_FAILURE_HOLDS_FLAG"]["source"]:
        return False, "MOVERS_FAILURE_HOLDS_FLAG is no longer flagged unruled [VETO]"
    return True, (f"movers exit 1, script absent, a 1 s timeout and exit-0-without-a-"
                  f"json each: said plainly, chain exit 0, NO flag, jobs {want_ran}, "
                  f"selfcheck PASS; and on a STANDING flag the [VETO] constant decides: "
                  f"False (default) -> CLEARED by the clean top-up + render; True -> "
                  f"left STANDING byte-identical and said so; True with a clean organ, "
                  f"or on a refresh (organ not supposed to run) -> CLEARED")


def _movers_break() -> tuple[bool, str]:
    legs = {p: _movers_failure(p) for p in ("fails-the-edition", "policy-ignored")}
    slipped = [p for p, (ok, _) in legs.items() if ok]
    if slipped:
        return True, f"plant(s) {slipped} passed"
    return False, " || ".join(f"[{p}] {d[:300]}" for p, (_, d) in legs.items())


def f_sk_2g() -> None:
    prove("F-SK-2g", "WIRE DOWN FOR MOVERS — a failing movers organ never fails the "
                     "edition, never raises the flag, and the [VETO] row decides "
                     "whether it holds one",
          _movers_break, lambda: _movers_failure(None))


# ── F-SK-2h · the cut-off run

def _child(td: Path, no_trap: bool, sig: int, no_flush: bool = False,
           where: str = "topup", flat_denial: bool = False) -> dict:
    """Start this file as `--child-cutoff`, wait until its stub is hanging under the
    lock — in the TOP-UP (`where='topup'`, STEP 4) or INSIDE STEP 5 with the edition
    already written (`where='render'`) — send `sig`, and report what is left."""
    cmd = [sys.executable, str(Path(__file__).resolve()), "--child-cutoff", str(td)]
    cmd += (["--no-trap"] if no_trap else []) + (["--no-flush"] if no_flush else [])
    cmd += (["--hang-render"] if where == "render" else [])
    cmd += (["--flat-denial"] if flat_denial else [])
    p = subprocess.Popen(cmd, cwd=str(ROOT),
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    marker = td / (Sandbox.ORACLE_STARTED if where == "render" else Sandbox.TOPUP_STARTED)
    t0 = time.monotonic()
    while not marker.exists() and p.poll() is None and time.monotonic() - t0 < 60:
        time.sleep(0.05)
    reached = marker.exists()
    lock_during = (td / ".oracle.lock").exists()
    if p.poll() is None:
        p.send_signal(sig)
    try:
        out, _ = p.communicate(timeout=60)
    except subprocess.TimeoutExpired:
        p.kill()
        out, _ = p.communicate()
        out = (out or "") + "\n[fixture] child did not exit within 60 s of the signal"
    flag = td / "ORACLE_DOWN.flag"
    return {"rc": p.returncode, "out": out or "", "reached": reached, "pid": p.pid,
            "lock_during": lock_during, "lock_left": (td / ".oracle.lock").exists(),
            "flag": flag.read_text(encoding="utf-8") if flag.exists() else None,
            "rows": (td / "selfcheck_log.jsonl").exists()}


def _cut_off(plant: str | None) -> tuple[bool, str]:
    """Verifier finding B2, measured: SIGTERM 3 s into a chain -> exit -15, EMPTY
    capture, `.oracle.lock` left behind, no flag, no selfcheck row; the next run
    (`--no-fetch` included) stood down on that lock, exit 0, NO EDITION.
    Plants: 'no-trap' is that world for the polite signal; 'age-only-lock' is that
    world for the lock a SIGKILL leaves, which nothing can trap; 'no-flush' is the
    EMPTY capture — a stdout that keeps its block buffer until an exit that never
    comes, so a killed run takes every line it logged with it."""
    # (i) the polite cut-off
    with tempfile.TemporaryDirectory(prefix="oracle-ondemand-cut-") as d:
        t = _child(Path(d), no_trap=(plant == "no-trap"), sig=signal.SIGTERM)
    if not t["reached"] or not t["lock_during"]:
        return plant is not None, f"could not plant: the child never hung under the lock: {t}"
    want_rc = 128 + int(signal.SIGTERM)
    flag = t["flag"] or ""
    told = [s for s in ("STEP 4 scope-topup: slot=on-demand",
                        "CUT OFF by signal 15 (SIGTERM) during STEP 4 scope-topup",
                        "NO EDITION WAS PRINTED by this run",
                        "ALARM RAISED", f"=== exit {want_rc} ===") if s not in t["out"]]
    if t["rc"] != want_rc or t["lock_left"] or t["flag"] is None or told or t["rows"] \
            or "CUT OFF by signal 15" not in flag or "JOB   ondemand" not in flag:
        return False, (f"SIGTERM during the top-up: exit {t['rc']} (want {want_rc}), "
                       f"lock left behind={t['lock_left']}, flag raised="
                       f"{t['flag'] is not None}, selfcheck row={t['rows']}, "
                       f"{len(t['out'].splitlines())} line(s) of output reached the "
                       f"pipe, never said: {told} — a cut-off edition that is silent, "
                       f"raises no alarm and locks the next run out")

    # (ii) the hard cut-off, and the run after it
    with tempfile.TemporaryDirectory(prefix="oracle-ondemand-kill-") as d:
        td = Path(d)
        k = _child(td, no_trap=False, sig=signal.SIGKILL, no_flush=(plant == "no-flush"))
        if not k["lock_left"] or k["rc"] != -int(signal.SIGKILL):
            return plant is not None, (f"could not plant: SIGKILL left no lock "
                                       f"(rc {k['rc']}, lock {k['lock_left']})")
        unheard = [s for s in ("=== ORACLE WRAPPER · job=ondemand slot=on-demand-full",
                               "STEP 1 identity-gate: PASS",
                               "STEP 4 scope-topup: slot=on-demand") if s not in k["out"]]
        if unheard:
            return False, (f"SIGKILL while the top-up hung: {len(k['out'].splitlines())} "
                           f"line(s) of the run's log reached the pipe, never heard: "
                           f"{unheard} — the lines were logged and died in a block "
                           f"buffer, so whoever reads a killed edition's log is told "
                           f"nothing, not even which step it was in")
        (td / Sandbox.TOPUP_STARTED).unlink()
        with Sandbox(td=td) as sb:
            if plant == "age-only-lock":
                OW.reclaim_dead_lock = lambda log=print: False
            rc, out = sb.main(FULL + ["--no-fetch"])
            ran, rows, left = list(sb.ran), sb.rows(), OW.LOCK.exists()
    if rc != 0 or ran != ["oracle[on-demand-full]"] or len(rows) != 1 or left \
            or "DEAD LOCK from ondemand/on-demand-full" not in out:
        return False, (f"the run AFTER a SIGKILLed one (pid {k['pid']}, not running): "
                       f"exit {rc}, jobs {ran}, selfcheck rows {len(rows)}, said "
                       f"'NO EDITION WAS PRINTED'={'NO EDITION WAS PRINTED' in out} — a "
                       f"dead run's lock kept the next edition out (for up to "
                       f"{OW.LOCK_STALE_MIN} min, with exit 0)")

    # (iii) and the reclaim does not over-reach: a lock whose pid IS running stands
    with Sandbox() as sb:
        OW.LOCK.write_text(json.dumps({"who": "fixture/live-run", "pid": os.getpid(),
                                       "ts": datetime.now(timezone.utc).isoformat()}))
        rc3, out3 = sb.main(FULL + ["--no-fetch"])
        ran3, kept3 = list(sb.ran), OW.LOCK.exists()
    if ran3 or not kept3 or rc3 != 0 or "DEAD LOCK" in out3 \
            or "NO EDITION WAS PRINTED" not in out3:
        return False, (f"a lock held by a RUNNING pid was not respected: jobs {ran3}, "
                       f"lock kept={kept3}, exit {rc3}")
    # (iv) THE CUT INSIDE STEP 5, with the edition already on disk (review finding,
    # 2026-09-21). `rendered` is set only after run_oracle RETURNS, but oracle_daily
    # writes the whole html before the tape, the calibration and the selfcheck row —
    # so this run used to be told "NO EDITION WAS PRINTED by this run" one line below
    # the log line naming the edition it had just written. Plant 'flat-denial' is that
    # behaviour: _cut_render_path stubbed to None inside the child.
    with tempfile.TemporaryDirectory(prefix="oracle-ondemand-cut5-") as d:
        r = _child(Path(d), no_trap=False, sig=signal.SIGTERM, where="render",
                   flat_denial=(plant == "flat-denial"))
        html_left = (Path(d) / "oracle_2026-09-21.html").exists()
    if not r["reached"]:
        return plant is not None, f"could not plant: the child never hung inside STEP 5: {r}"
    if not html_left:
        return plant is not None, ("could not plant: the child wrote no edition "
                                   "before the signal")
    said5 = [s for s in ("CUT OFF by signal 15 (SIGTERM) during STEP 5 oracle-render",
                         "an edition was already written to",
                         "It is UNVERIFIED", "oracle_2026-09-21.html",
                         "NO SELFCHECK ROW WAS WRITTEN") if s not in r["out"]]
    flag5 = r["flag"] or ""
    if said5 or r["rows"] or "NO EDITION WAS PRINTED" in r["out"] \
            or "oracle_2026-09-21.html" not in flag5 \
            or "NO EDITION WAS PRINTED" in flag5:
        return False, (f"SIGTERM inside STEP 5 with the edition ALREADY on disk: never "
                       f"said {said5}, said 'NO EDITION WAS PRINTED'="
                       f"{'NO EDITION WAS PRINTED' in r['out']}, the flag body names "
                       f"the file={'oracle_2026-09-21.html' in flag5}, selfcheck "
                       f"row={r['rows']} — the operator is told there is no edition "
                       f"while a whole, current-dated one sits in briefs/oracle with "
                       f"no selfcheck row behind it")

    return True, (f"SIGTERM while the top-up hung under the lock: the child's piped "
                  f"output said 'CUT OFF by signal 15 (SIGTERM) during "
                  f"STEP 4 scope-topup' and 'NO EDITION WAS PRINTED', released the lock, "
                  f"raised the flag (job ondemand, the CUT OFF line in it), wrote no "
                  f"selfcheck row, exit {want_rc}; SIGKILL left the lock, as it must, yet "
                  f"all {len(k['out'].splitlines())} lines logged before the kill had "
                  f"already reached the pipe (flushed as logged, step 4's tag included), "
                  f"and the next --no-fetch run said 'DEAD LOCK from ondemand/on-demand-full "
                  f"(pid {k['pid']} is not running …' reclaimed it and printed its "
                  f"edition (exit 0, 1 selfcheck row); a lock held by a RUNNING pid "
                  f"still stood the chain down; and SIGTERM INSIDE STEP 5, with the "
                  f"edition already written, did NOT say 'NO EDITION WAS PRINTED' — "
                  f"it named the file, said NO SELFCHECK ROW WAS WRITTEN and called "
                  f"it UNVERIFIED, in the log and in the flag body, with no selfcheck "
                  f"row on disk")


def _cut_off_break() -> tuple[bool, str]:
    legs = {p: _cut_off(p) for p in ("no-trap", "age-only-lock", "no-flush",
                                    "flat-denial")}
    slipped = [p for p, (ok, _) in legs.items() if ok]
    if slipped:
        return True, f"plant(s) {slipped} passed"
    return False, " || ".join(f"[{p}] {d[:300]}" for p, (_, d) in legs.items())


class _BlockBuffered:
    """The 'no-flush' plant: a stdout whose flush() does nothing, i.e. the pipe as
    the chain found it before it flushed its own lines."""

    def __init__(self, stream):
        self._stream = stream

    def write(self, text):
        return self._stream.write(text)

    def flush(self):
        pass


def f_sk_2h() -> None:
    prove("F-SK-2h", "THE CUT-OFF RUN — a terminated edition says so, releases its "
                     "lock and raises the flag; a killed one cannot lock the next "
                     "edition out",
          _cut_off_break, lambda: _cut_off(None))


# ── F-SK-2i · a lock whose pid is ALIVE is never reclaimed on age

def _live_holder(plant: str | None) -> tuple[bool, str]:
    """Review finding, 2026-09-21. acquire_lock's stale rule is AGE ONLY: past
    LOCK_STALE_MIN it takes the lock from a holder that is STILL WORKING, and never
    asks _pid_running. That was safe at 40 pinned pairs and a 10-symbol roster; on
    the pinned 72 pairs and 18 symbols a wire-down full edition is ~29 min against
    LOCK_STALE_MIN = 30 (72 x >= 15 s per failing pair + MOVERS_TIMEOUT_S 600 s +
    the render), so the two would overlap: both write one briefs/oracle/
    oracle_<date>.html and one oracle_tape_<date>.parquet, neither write atomic,
    both append a selfcheck row, and then the FIRST run's unconditional
    release_lock() deletes the SECOND's lock and lets a third in.
    The holder here is a REAL live child process, and the lock is stamped
    LOCK_STALE_MIN + 1 minutes old, i.e. squarely inside the reclaim branch.
    Plant 'age-only': live_lock_holder never consulted, so the age rule is reached
    again — exactly the shipped-before behaviour."""
    holder = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(120)"])
    age = OW.LOCK_STALE_MIN + 1
    try:
        with Sandbox() as sb:
            if plant == "age-only":
                OW.live_lock_holder = lambda log=print: None
            stamp = (datetime.now(timezone.utc) - timedelta(minutes=age)).isoformat()
            body = json.dumps({"who": "ondemand/on-demand-full", "pid": holder.pid,
                               "ts": stamp})
            OW.LOCK.write_text(body)
            alive = holder.poll() is None     # the holder really is running, now
            rc, out = sb.main(list(FULL))
            ran, rows = list(sb.ran), sb.rows()
            kept = OW.LOCK.exists() and OW.LOCK.read_text() == body
            edition = (sb.td / "oracle_2026-09-21.html").exists()
            movers = sb.movers_ran()
    finally:
        holder.terminate()
        try:
            holder.wait(timeout=30)
        except subprocess.TimeoutExpired:
            holder.kill()
    if not alive:
        return plant is not None, ("could not plant: the holder process was not "
                                   "running when the chain started")
    if rc != 0 or ran or rows or edition or movers or not kept \
            or "LOCK HELD by a LIVE pid" not in out or "STALE LOCK" in out:
        return False, (f"a lock stamped {age} min old (> LOCK_STALE_MIN = "
                       f"{OW.LOCK_STALE_MIN}) whose pid {holder.pid} was ALIVE was "
                       f"RECLAIMED: exit {rc}, jobs {ran}, movers started={movers}, "
                       f"selfcheck rows {len(rows)}, an edition was written={edition}, "
                       f"the holder's lock body survived={kept}, said 'LOCK HELD by a "
                       f"LIVE pid'={'LOCK HELD by a LIVE pid' in out}, said 'STALE "
                       f"LOCK'={'STALE LOCK' in out} — two editions are now writing "
                       f"one oracle_<date>.html and one oracle_tape_<date>.parquet, "
                       f"and the first run's release_lock() will delete this one's lock")
    return True, (f"a lock stamped {age} min old — PAST LOCK_STALE_MIN = "
                  f"{OW.LOCK_STALE_MIN}, i.e. inside acquire_lock's reclaim branch — "
                  f"whose pid {holder.pid} was a REAL running process: the chain stood "
                  f"down, exit 0, no job ran, the movers organ was never started, no "
                  f"selfcheck row was written, no edition was rendered, the holder's "
                  f"lock body is byte-identical at exit, and the log says 'LOCK HELD "
                  f"by a LIVE pid' and never 'STALE LOCK'")


def f_sk_2i() -> None:
    prove("F-SK-2i", "THE LIVE HOLDER — a lock PAST LOCK_STALE_MIN whose pid is still "
                     "running is never reclaimed by an on-demand run: it stands down "
                     "and leaves the holder's lock untouched",
          lambda: _live_holder("age-only"), lambda: _live_holder(None))


def child_cutoff(argv: list[str]) -> int:
    """`--child-cutoff <dir> [--no-trap]` — F-SK-2h's child. The real wrapper's real
    main(), in the sandbox, in its own process, stdout a PIPE (so block-buffered
    unless the chain flushes), with a top-up that hangs until it is cut."""
    td = Path(argv[argv.index("--child-cutoff") + 1])
    render = "--hang-render" in argv
    with Sandbox(topup_hangs=not render, oracle_hangs=render, td=td) as sb:
        if "--no-trap" in argv:
            OW.trap_cut_off = lambda: {}
        if "--flat-denial" in argv:
            # the shipped-before-2026-09-21 behaviour: `rendered` is the only thing
            # consulted, so a cut inside STEP 5 denies an edition that is on disk
            OW._cut_render_path = lambda lines: None
        if "--no-flush" in argv:
            sys.stdout = _BlockBuffered(sys.stdout)
        assert OW.arm is not sb.keep["arm"]
        return OW.main(list(FULL))


# ── F-SK-2f · one lock for the whole chain

def _one_lock(two_commands: bool) -> tuple[bool, str]:
    """`two_commands=True` is the hand-run pair again: two processes' worth of
    main(), so the lock is dropped between the top-up and the render — the window
    in which another run can write the same dated tape (incident audit D4)."""
    with Sandbox() as sb:
        if two_commands:
            sb.main(["--job", "topup", "--slot", "topup"])
            rc, out = sb.main(["--job", "oracle", "--slot", "full"])
        else:
            rc, out = sb.main(FULL)
        takes, seen, left = list(sb.lock_takes), sb.locks(), OW.LOCK.exists()
        ran = list(sb.ran)
    if len(takes) != 1:
        return False, (f"{len(takes)} lock acquisitions {takes} for one edition — the "
                       f"lock is RELEASED between the top-up and the render, and "
                       f"another run can take it there")
    if seen != {"movers": True, "topup": True, "oracle": True}:
        return False, f"a job ran outside the lock (job -> lock held): {seen}"
    if left:
        return False, "the lock was left behind at exit"

    with Sandbox() as sb:                     # and a HELD lock stands the chain down
        OW.LOCK.write_text(json.dumps({"who": "fixture/other-run", "pid": 1,
                                       "ts": datetime.now(timezone.utc).isoformat()}))
        rc2, out2 = sb.main(FULL)
        ran2, kept, flag2 = list(sb.ran), OW.LOCK.exists(), OW.FLAG.exists()
        movers2 = sb.movers_ran()
    if ran2 or movers2 or not kept or flag2 or "NO EDITION WAS PRINTED" not in out2:
        return False, (f"a held lock was not respected: jobs={ran2} movers={movers2} "
                       f"other run's lock kept={kept} flag={flag2}")
    return True, (f"one acquisition {takes} covers {ran} and the movers process (lock "
                  f"held while each ran: {seen}); released at exit {rc}; and against "
                  f"another run's live lock the chain stood down — exit {rc2}, no job, "
                  f"no movers process, no flag, the other run's lock untouched, 'NO "
                  f"EDITION WAS PRINTED' said")


def f_sk_2f() -> None:
    prove("F-SK-2f", "ONE LOCK — the movers fetch, the top-up and the render share "
                     "a single lock acquisition",
          lambda: _one_lock(two_commands=True), lambda: _one_lock(two_commands=False))


# ══════════════════════════════════ F-SK-3 · THE IDENTITY GATE

def _identity(plant: str | None) -> tuple[bool, str]:
    """CONVENTIONS §0: "checking only the path passes a copy left behind in a
    cloud-synced tree, and checking only for the absence of markers passes any
    directory on the machine." Plants: 'marker-only' is the second mistake;
    'no-root-marker' is the first, in the one place it still bites once the path is
    checked — a $HOME that itself sits inside a synced tree, where ROOT IS
    $HOME/Naiad and only the marker test on ROOT can refuse it. (Verifier mutation
    M7c dropped ROOT from the marker loop and the first version stayed green: every
    ROOT-with-marker case it held was ALSO a path mismatch.)"""
    home = Path.home()
    cloud_home = home / "OneDrive" / "home"
    matrix = [
        ("the real tree", home / "Naiad", home, home / "Naiad", True),
        ("a OneDrive copy", home / "OneDrive" / "Naiad", home, home / "Naiad", False),
        ("an iCloud copy", home / "Library" / "Mobile Documents" /
         "com~apple~CloudDocs" / "Naiad", home, home / "Naiad", False),
        ("a stray clone", home / "src" / "Naiad", home, home / "Naiad", False),
        ("the real tree, run from a cloud cwd", home / "Naiad", home,
         home / "OneDrive" / "x", False),
        ("$HOME itself inside a cloud tree", cloud_home / "Naiad", cloud_home,
         Path("/"), False),
    ]

    def marker_only(root=None, home=None, cwd=None):
        return (not any(m in str(root or OW.ROOT) for m in OW.CLOUD_MARKERS),
                "marker side only")

    def no_root_marker(root=None, home=None, cwd=None):
        root = Path(OW.ROOT if root is None else root).resolve()
        home = Path(Path.home() if home is None else home).resolve()
        cwd = Path(Path.cwd() if cwd is None else cwd).resolve()
        if any(m in str(cwd) for m in OW.CLOUD_MARKERS):
            return False, "cwd carries a marker"
        return root == home / "Naiad", "path side + cwd marker only"

    gate = {"marker-only": marker_only, "no-root-marker": no_root_marker}.get(
        plant, OW.identity_gate)

    # THE CONSEQUENCE FIRST, through the real main(): what a misrouted tree DOES.
    touched = {}
    for name, sub, home_sub in (("cloud", ("OneDrive", "Naiad"), None),
                                ("stray", ("elsewhere", "Naiad"), None),
                                ("cloud-home", ("OneDrive", "home", "Naiad"),
                                 ("OneDrive", "home"))):
        with Sandbox() as sb:
            fake = sb.td.joinpath(*sub)
            fake.mkdir(parents=True)
            OW.ROOT = fake
            if home_sub:                     # restored by Sandbox.__exit__
                os.environ["HOME"] = str(sb.td.joinpath(*home_sub))
            if plant:
                OW.identity_gate = gate
            rc, out = sb.main(FULL)
            touched[name] = {"rc": rc, "ran": list(sb.ran), "movers": sb.movers_ran(),
                             "lock_takes": len(sb.lock_takes),
                             "flag": OW.FLAG.exists(), "rows": len(sb.rows()),
                             "halt": "STEP 1 identity-gate: HALT" in out}
    bad = {k: v for k, v in touched.items()
           if v["rc"] == 0 or v["ran"] or v["movers"] or v["lock_takes"] or v["flag"]
           or v["rows"] or not v["halt"]}
    if bad:
        return False, (f"a misrouted tree was NOT halted before any action — it took "
                       f"the lock, fetched and rendered: {bad}")
    wrong = [name for name, root, hm, cwd, want in matrix
             if gate(root=root, home=hm, cwd=cwd)[0] != want]
    if wrong:
        return False, f"the gate misjudges: {wrong}"
    return True, (f"through the real main() a cloud ROOT, a stray ROOT and a ROOT that "
                  f"IS $HOME/Naiad under a $HOME inside a cloud tree all HALT "
                  f"exit {sorted({v['rc'] for v in touched.values()})} with no lock "
                  f"taken, no job run, no movers process, no flag, no selfcheck row; "
                  f"and the pure gate is right on all {len(matrix)} cases (real tree, "
                  f"OneDrive copy, iCloud copy, stray clone, real tree from a cloud cwd, "
                  f"$HOME inside a cloud tree)")


def _identity_break() -> tuple[bool, str]:
    legs = {p: _identity(p) for p in ("marker-only", "no-root-marker")}
    slipped = [p for p, (ok, _) in legs.items() if ok]
    if slipped:
        return True, f"plant(s) {slipped} passed"
    return False, " || ".join(f"[{p}] {d[:300]}" for p, (_, d) in legs.items())


def f_sk_3() -> None:
    prove("F-SK-3", "THE IDENTITY GATE — two-sided, and it halts nonzero before "
                    "any action",
          _identity_break, lambda: _identity(None))


# ══════════════════════════════════ F-SK-4 · THE STRAY ARMING COMMAND (OR-2 R-4)
#
# WHAT THIS GUARDS. OR-1 finding OR1-b: `oracle_wrapper.py --install` typed alone
# was still the clock's arming verb. It rewrote the five retained plists, ran
# `launchctl bootout` + `bootstrap` on labels the operator had suspended, and
# printed `ARMED <label>` whatever bootstrap answered. Operator ruling R-4
# (2026-09-22): while research_outputs/oracle/SCHEDULE_SUSPENDED exists, --install
# alone REFUSES (exit 2, nothing touched) and names `--install --rearm`; on that
# explicit path every rc reaches the exit code and ARMED prints only on rc 0.
#
# HOW IT IS SAFE. The real gui domain is never reached, by construction:
#   · every scenario runs the REAL main() in a CHILD process (this file, run as
#     `--child-install <dir> [plants] -- <argv>`), whose PATH holds ONLY a
#     directory of two shell shims — `launchctl` and `plutil` — that RECORD their
#     argv, answer, and forward nothing. A missing shim raises FileNotFoundError;
#     it can never fall through to the real binary;
#   · the child's HOME is the sandbox, so Path.home()-derived AGENTS is too, and
#     the plists it may write are COPIES of the five real ones;
#   · the child refuses to start (exit 99, "F-SK-4 UNSAFE") unless PATH, both
#     `shutil.which` answers, HOME and AGENTS all point into the sandbox;
#   · the five REAL plists and the REAL sentinel are stamped (size, mtime_ns,
#     sha256) BEFORE prove() and compared after both legs; any change is a BREACH,
#     whatever the legs said, and their mtimes are held against the G-1 baseline
#     the OR-2 queue file recorded at STEP 0.

G1_QUEUE = ROOT / "exchange" / "queue" / "2026-09-22_OR2_oracle_rulings_ARGUS.md"
G1_LINE = re.compile(r"^\s+(com\.naiad\.oracle-[0-9a-z-]+)\.plist\s+(\d+)\s+·", re.M)
SK4_FAIL_ENV = "F_SK4_FAIL"
SK4_FAIL_LABEL = "com.naiad.oracle-1600"
SK4_REFUSED_ARGVS = (
    ["--install"],                                    # the stray command itself
    ["--install", "--job", "oracle", "--slot", "full"],
    ["--install", "--dry-run"],                       # looks harmless, is not
    ["--slot", "full", "--install"],
    ["--rearm"],                                      # would fall to the legacy job
    ["--install", "--rearm", "--dry-run"],            # the explicit path, disguised
)
SK4_LAUNCHCTL_SHIM = """#!/bin/sh
# F-SK-4's fake launchctl: records, answers, NEVER forwards. Shell builtins only.
printf '%s\\n' "$*" >> "{calls}"
case "$1" in
  bootstrap)
    p="$3"; p="${{p##*/}}"; l="${{p%.plist}}"
    if [ -n "$F_SK4_FAIL" ] && [ "$l" = "$F_SK4_FAIL" ]; then
      echo "Bootstrap failed: 5: Input/output error" >&2
      exit 5
    fi
    exit 0 ;;
  print) exit 113 ;;
  *) exit 0 ;;
esac
"""
SK4_PLUTIL_SHIM = """#!/bin/sh
printf '%s\\n' "$*" >> "{calls}"
echo "$2: OK"
exit 0
"""


def _real_agents() -> Path:
    """The REAL LaunchAgents directory, from the password database — not from $HOME,
    which a sandbox may have moved."""
    import pwd
    return Path(pwd.getpwuid(os.getuid()).pw_dir) / "Library" / "LaunchAgents"


def _stamp_real() -> dict:
    out = {}
    files = [_real_agents() / f"{label}.plist" for label in OW.SLOTS]
    files.append(ROOT / OW.SCHEDULE_SENTINEL_REL)
    for f in files:
        out[f.name] = ((f.stat().st_size, f.stat().st_mtime_ns,
                        hashlib.sha256(f.read_bytes()).hexdigest()) if f.exists() else None)
    return out


def _g1_baseline() -> dict:
    """label -> mtime (epoch seconds) as the OR-2 queue file recorded it at STEP 0."""
    txt = G1_QUEUE.read_text(encoding="utf-8") if G1_QUEUE.exists() else ""
    i = txt.find("G-1 BASELINE")
    return {} if i < 0 else {m.group(1): int(m.group(2)) for m in G1_LINE.finditer(txt[i:])}


def _sk4_run(argv: list[str], plants: tuple = (), fail_label: str | None = None) -> dict:
    """One scenario: the real main() in a child whose PATH is only the shims."""
    with tempfile.TemporaryDirectory(prefix="oracle-sk4-") as tds:
        td = Path(tds)
        (td / "bin").mkdir()
        agents = td / "home" / "Library" / "LaunchAgents"
        agents.mkdir(parents=True)
        calls, pcalls = td / "launchctl.calls", td / "plutil.calls"
        for name, body in (("launchctl", SK4_LAUNCHCTL_SHIM.format(calls=calls)),
                           ("plutil", SK4_PLUTIL_SHIM.format(calls=pcalls))):
            f = td / "bin" / name
            f.write_text(body, encoding="utf-8")
            f.chmod(0o755)
        for label in OW.SLOTS:
            src = _real_agents() / f"{label}.plist"
            if src.exists():
                shutil.copy2(src, agents / src.name)      # the real ones are only READ
        before = {f.name: f.stat().st_mtime_ns for f in agents.iterdir()}
        env = {"PATH": str(td / "bin"), "HOME": str(td / "home"),
               "PYTHONDONTWRITEBYTECODE": "1", "PYTHONIOENCODING": "utf-8"}
        if fail_label:
            env[SK4_FAIL_ENV] = fail_label
        r = subprocess.run([sys.executable, str(Path(__file__).resolve()), "--child-install",
                            str(td), *plants, "--", *argv],
                           cwd=ROOT, env=env, capture_output=True, text=True, timeout=120)
        after = {f.name: f.stat().st_mtime_ns for f in agents.iterdir()}
        return {"argv": " ".join(argv), "plants": plants, "rc": r.returncode,
                "out": r.stdout + r.stderr,
                "calls": calls.read_text().splitlines() if calls.exists() else [],
                "pcalls": pcalls.read_text().splitlines() if pcalls.exists() else [],
                "touched": sorted(k for k in after if after[k] != before.get(k))}


def _sk4_refusal_faults(r: dict) -> list[str]:
    tag = f"`{r['argv']}`"
    if "F-SK-4 UNSAFE" in r["out"] or r["rc"] == 99:
        return [f"{tag}: the child refused to start — the safety net did not hold: "
                f"{r['out'][:200]}"]
    bad = []
    if r["rc"] != 2:
        bad.append(f"{tag} -> exit {r['rc']}, not 2")
    if r["calls"]:
        verbs = sorted({c.split(" ", 1)[0] for c in r["calls"]})
        bad.append(f"{tag}: the shim recorded {len(r['calls'])} launchctl call(s) "
                   f"({', '.join(verbs)}; first `{r['calls'][0]}`) — a suspended label was "
                   f"booted out and bootstrapped")
    if r["pcalls"]:
        bad.append(f"{tag}: plutil ran {len(r['pcalls'])}x — a plist was written")
    if r["touched"]:
        bad.append(f"{tag}: sandbox plist(s) rewritten: {r['touched'][:2]}")
    if "Nothing was touched" not in r["out"]:
        bad.append(f"{tag}: the refusal does not say 'Nothing was touched'")
    if "--install --rearm" not in r["out"]:
        bad.append(f"{tag}: the refusal does not name the explicit path `--install --rearm`")
    if "ORACLE — arming" in r["out"] or re.search(r"^  ARMED com\.naiad\.", r["out"], re.M):
        bad.append(f"{tag}: an arming line printed")
    return bad


def _sk4_rearm_faults(r: dict, fail: str | None) -> list[str]:
    tag = f"`{r['argv']}`" + (f" (shim: {fail} bootstrap -> 5)" if fail else "")
    if "F-SK-4 UNSAFE" in r["out"] or r["rc"] == 99:
        return [f"{tag}: the child refused to start — the safety net did not hold"]
    bad = []
    armed = re.findall(r"^  ARMED (com\.naiad\.oracle-[0-9a-z-]+) ", r["out"], re.M)
    not_armed = re.findall(r"^  NOT ARMED (com\.naiad\.oracle-[0-9a-z-]+) ", r["out"], re.M)
    want_armed = [lb for lb in OW.SLOTS if lb != fail]
    if fail:
        if r["rc"] == 0:
            bad.append(f"{tag} -> exit 0 although a bootstrap answered 5 — the rc never "
                       f"reached the exit code")
        if fail in armed:
            bad.append(f"{tag}: `ARMED {fail}` printed for a label whose bootstrap answered 5")
        if not_armed != [fail]:
            bad.append(f"{tag}: NOT ARMED lines {not_armed}, want [{fail}]")
        elif not re.search(rf"^  NOT ARMED {re.escape(fail)} .*bootstrap rc 5", r["out"], re.M):
            bad.append(f"{tag}: the NOT ARMED line does not carry `bootstrap rc 5`")
    elif r["rc"] != 0 or not_armed:
        bad.append(f"{tag} -> exit {r['rc']}, NOT ARMED {not_armed}: a clean shim must arm all")
    if sorted(armed) != sorted(want_armed):
        bad.append(f"{tag}: ARMED lines for {sorted(armed)}, want {sorted(want_armed)}")
    for lb in OW.SLOTS:
        verbs = [c.split(" ", 1)[0] for c in r["calls"] if lb in c]
        if verbs[:4] != ["enable", "bootout", "bootstrap", "list"]:
            bad.append(f"{tag}: launchctl calls for {lb} read {verbs} — the explicit path is "
                       f"enable, (bootout), bootstrap, list")
            break
    if len(r["pcalls"]) != len(OW.SLOTS):
        bad.append(f"{tag}: plutil ran {len(r['pcalls'])}x, want {len(OW.SLOTS)}")
    return bad


def _sk4_real() -> tuple[bool, str]:
    bad = []
    sentinel = ROOT / OW.SCHEDULE_SENTINEL_REL
    if OW.SCHEDULE_SENTINEL != sentinel:
        bad.append(f"OW.SCHEDULE_SENTINEL is {OW.SCHEDULE_SENTINEL}, not the repo sentinel")
    if not sentinel.exists():
        bad.append(f"the sentinel {OW.SCHEDULE_SENTINEL_REL} is ABSENT — the guard is OFF")
    else:
        rl = [ln.split(None, 1)[1].strip() for ln in sentinel.read_text(encoding="utf-8").splitlines()
              if ln.startswith("REARM ")]
        if rl != [OW.REARM_COMMAND]:
            bad.append(f"the sentinel's REARM line {rl} is not OW.REARM_COMMAND byte for byte")
    src = WRAPPER.read_text(encoding="utf-8")
    if "/bin/launchctl" in src or OW.LAUNCHCTL != "launchctl":
        bad.append("the wrapper names launchctl by an absolute path — a PATH shim could be "
                   "bypassed")
    refused = [_sk4_run(a) for a in SK4_REFUSED_ARGVS]
    for r in refused:
        bad += _sk4_refusal_faults(r)
    r_fail = _sk4_run(["--install", "--rearm"], fail_label=SK4_FAIL_LABEL)
    r_ok = _sk4_run(["--install", "--rearm"])
    bad += _sk4_rearm_faults(r_fail, SK4_FAIL_LABEL) + _sk4_rearm_faults(r_ok, None)
    if bad:
        return False, "; ".join(bad[:6]) + (f" (+{len(bad) - 6} more)" if len(bad) > 6 else "")
    return True, (
        f"sentinel present, its REARM line == OW.REARM_COMMAND; {len(refused)} argvs "
        f"({' | '.join(r['argv'] for r in refused)}) each exit 2 saying 'Nothing was "
        f"touched' and naming `--install --rearm`: 0 launchctl calls, 0 plutil calls, 0 "
        f"plists rewritten. The explicit path against the shim: with {SK4_FAIL_LABEL}'s "
        f"bootstrap answering 5 -> exit {r_fail['rc']}, {len(OW.SLOTS) - 1} ARMED + 1 NOT "
        f"ARMED (bootstrap rc 5); clean -> exit 0, {len(OW.SLOTS)} ARMED; every label "
        f"enable -> bootout -> bootstrap -> list. The real gui domain was never reached: "
        f"PATH held only the shims")


def _sk4_break() -> tuple[bool, str]:
    plants = (
        ("GUARD PLANT (the sentinel guard removed: `--install` alone, as before R-4)",
         "the shim recorded",
         lambda: _sk4_refusal_faults(_sk4_run(["--install"], plants=("--no-guard",)))),
        ("RC-BLIND PLANT (ARMED whatever bootstrap said — OR1-b's false ARMED)",
         "whose bootstrap answered 5",
         lambda: _sk4_rearm_faults(_sk4_run(["--install", "--rearm"], plants=("--rc-blind",),
                                            fail_label=SK4_FAIL_LABEL), SK4_FAIL_LABEL)),
    )
    green, out = False, []
    for name, must, judge in plants:
        bad = judge()
        hits = [b for b in bad if must in b]
        if hits:
            out.append(f"{name} -> RED: {hits[0]}" + (f" [+{len(bad) - 1} more]" if len(bad) > 1 else ""))
        else:
            green = True
            out.append(f"{name} -> " + ("GREEN" if not bad else
                       f"RED FOR THE WRONG REASON (no finding says {must!r}; first: {bad[0]})"))
    return green, " ‖ ".join(out)


def child_install(args: list[str]) -> int:
    """F-SK-4's child: the REAL oracle_wrapper.main(), in a process whose PATH holds
    only the shims and whose HOME is the sandbox. It will not start unless every one
    of those holds, so no mistake in the parent can reach the real launchctl."""
    i, j = args.index("--child-install"), args.index("--")
    td = Path(args[i + 1])
    plants, wargv = args[i + 2:j], args[j + 1:]
    shim = td / "bin" / "launchctl"
    net = {"PATH is only the shim dir": os.environ.get("PATH") == str(td / "bin"),
           "launchctl resolves to the shim": shutil.which("launchctl") == str(shim),
           "plutil resolves to the shim": shutil.which("plutil") == str(td / "bin" / "plutil"),
           "HOME is the sandbox": Path.home() == td / "home",
           "AGENTS is in the sandbox": str(OW.AGENTS).startswith(str(td) + os.sep)}
    unsafe = [k for k, v in net.items() if not v]
    if unsafe:
        print(f"F-SK-4 UNSAFE — refusing to drive main(): {unsafe}")
        return 99
    OW.AGENTS = td / "home" / "Library" / "LaunchAgents"
    OW.LOGDIR = td / "logs"
    OW.FLAG, OW.LOCK, OW.SELFCHECK = (td / "ORACLE_DOWN.flag", td / ".oracle.lock",
                                       td / "selfcheck_log.jsonl")
    OW.LAUNCHCTL = str(shim)
    for pl in plants:
        if pl == "--no-guard":
            OW.install_refusal = lambda argv: None
        elif pl == "--rc-blind":
            OW.arm_ok = lambda rcs: True
        else:
            print(f"F-SK-4 child: unknown plant {pl!r}")
            return 98
    return OW.main(wargv)


def f_sk_4() -> None:
    before, base = _stamp_real(), _g1_baseline()
    prove("F-SK-4", "THE STRAY ARMING COMMAND — --install alone refuses while the "
                    "schedule is suspended; the explicit path says ARMED only on rc 0 "
                    "(against a fake launchctl, never the gui domain)",
          _sk4_break, _sk4_real)
    after = _stamp_real()
    breach = [k for k in before if before[k] != after.get(k)]
    g1 = []
    if sorted(base) != sorted(OW.SLOTS):
        g1.append(f"the G-1 baseline in {G1_QUEUE.name} names {sorted(base)}, the wrapper "
                  f"{sorted(OW.SLOTS)}")
    for lb, want in base.items():
        f = _real_agents() / f"{lb}.plist"
        got = int(f.stat().st_mtime) if f.exists() else None
        if got != want:
            g1.append(f"{lb}.plist mtime {got} != the STEP 0 baseline {want}")
    if breach or g1:
        msg = "; ".join([f"{k} changed during the fixture" for k in breach] + g1)
        print(f"  [BREACH] {msg}")
        if "F-SK-4" in PASSED:
            PASSED.remove("F-SK-4")
        FAILED.append(f"F-SK-4 (BREACH: {msg})")
    else:
        print(f"  [G-1] the {len(OW.SLOTS)} real plists and the sentinel: size, mtime and "
              f"sha256 unchanged across both legs; plist mtimes equal the STEP 0 baseline "
              f"recorded in {G1_QUEUE.name}")


# ══════════════════════════════════════════════════════════════════ MAIN

def main() -> int:
    print("=" * 78)
    print(f"ORACLE ON-DEMAND FIXTURES — {datetime.now(timezone.utc).isoformat()[:19]}Z")
    print(f"  skill    {SKILL.relative_to(ROOT)}")
    print(f"  wrapper  {WRAPPER.relative_to(ROOT)} sha256 "
          f"{hashlib.sha256(WRAPPER.read_bytes()).hexdigest()}")
    print(f"  chain    {' -> '.join(step_ids())}")
    print("=" * 78)
    fixtures = (f_sk_1, f_sk_2a, f_sk_2b, f_sk_2c, f_sk_2d, f_sk_2e, f_sk_2f,
                f_sk_2g, f_sk_2h, f_sk_2i, f_sk_3, f_sk_4)
    for fn in fixtures:
        try:
            fn()
        except Exception as e:
            name = fn.__name__.upper().replace("_", "-")
            FAILED.append(f"{name} ({e.__class__.__name__}: {e})")
            print(f"  [FAIL] {name}: raised {e.__class__.__name__}: {e}")
    print("\n" + "=" * 78)
    print(f"GREEN {len(PASSED)}/{len(fixtures)} · RED {len(FAILED)}")
    for f in FAILED:
        print(f"  RED: {f}")
    print("=" * 78)
    return 1 if FAILED else 0


if __name__ == "__main__":
    if "--child-cutoff" in sys.argv:
        raise SystemExit(child_cutoff(sys.argv[1:]))
    if "--child-install" in sys.argv:
        raise SystemExit(child_install(sys.argv[1:]))
    raise SystemExit(main())
