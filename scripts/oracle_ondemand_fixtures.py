"""ORACLE ON-DEMAND FIXTURES — F-SK-1, F-SK-2a..2f, F-SK-3 of queue OR-1, STEP A.

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
reschedule_if_drifted and arm are replaced by recorders that RAISE — so no fixture
run calls launchctl, touches ~/Library/LaunchAgents, fetches, renders into
briefs/oracle, or drops a flag in the repo. The five com.naiad.oracle-* agents are
suspended by operator ruling 2026-09-21 and this suite cannot re-arm one.

Run:  ~/venvs/naiad/bin/python scripts/oracle_ondemand_fixtures.py
Exit: 0 if every fixture is green on REAL and red on BREAK; 1 otherwise.
"""
from __future__ import annotations

import contextlib
import hashlib
import io
import json
import re
import subprocess
import sys
import tempfile
import types
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import oracle_wrapper as OW                    # noqa: E402

SKILL = ROOT / ".claude" / "skills" / "oracle" / "SKILL.md"
WRAPPER = ROOT / "scripts" / "oracle_wrapper.py"

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


# "WITH THE EXPECTED OUTPUT LINES of each step" is only worth something if the
# lines are the wrapper's. So the wrapper is RUN (sandboxed, five scenarios) and
# every placeholder-free line it logs under these prefixes must be in the skill to
# the byte. Lines that carry a temp path, a stub's name, a wall-clock or the cwd
# cannot be quoted verbatim by anyone and are left out; the two slot strings are
# folded into one so the skill need not print step 5 twice.
_STATIC_PREFIXES = ("  STEP ", "  schedule: ", "  alarm left standing", "  no ORACLE_DOWN")


def wrapper_static_lines() -> list[str]:
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


def _skill_real() -> tuple[bool, str]:
    if not SKILL.exists():
        return False, f"{SKILL.relative_to(ROOT)} does not exist"
    before = _lane_stamp()
    dry = _dry_run()
    after = _lane_stamp()
    if before != after:
        return False, (f"the DRY run touched the live lane: before {before} "
                       f"after {after}")
    ok, detail = _skill_probe(SKILL.read_text(encoding="utf-8"), dry,
                              wrapper_static_lines())
    return ok, detail + ("; flag, lock and selfcheck log byte-untouched by the dry run"
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
    if slipped:
        return True, f"a skill missing {slipped} still passed"
    return False, (f"{len(step_ids())} planted copies, each with one step removed, "
                   f"all red; e.g. without movers-fetch: {reasons[0]} || 1 planted "
                   f"copy with one quoted log line altered, red: {drift_detail[:200]}")


def f_sk_1() -> None:
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
             "acquire_lock", "run_topup", "run_oracle", "self_checks", "reschedule_if_drifted", "arm",
             "show_standing_flag", "ondemand_flag_action", "ondemand_skips",
             "identity_gate")

    def __init__(self, topup_rc: int = 0, late_flag: bool = False):
        self.topup_rc, self.late_flag = topup_rc, late_flag
        self.ran: list[str] = []            # jobs that actually ran, in order
        self.schedule_calls: list[str] = []  # any call into the schedule machinery
        self.lock_takes: list[str] = []      # every acquire_lock(who), granted or not
        self.lock_seen: dict[str, bool] = {}  # job -> was the lock held while it ran

    def __enter__(self):
        self.keep = {k: getattr(OW, k) for k in self.ATTRS}
        self.keep_failures = list(OW.FAILURES)
        self.keep_od = sys.modules.get("oracle_daily")
        self._td = tempfile.TemporaryDirectory(prefix="oracle-ondemand-fx-")
        td = self.td = Path(self._td.name)
        OW.FLAG = td / "ORACLE_DOWN.flag"
        OW.LOCK = td / ".oracle.lock"
        OW.SELFCHECK = td / "selfcheck_log.jsonl"
        OW.MOVERS_DIR = td / "movers"
        OW.MOVERS_SCRIPT = td / "oracle_movers_stub.py"
        self.movers_marker = td / "movers.ran"
        OW.MOVERS_SCRIPT.write_text(
            "from pathlib import Path\n"
            f"held = Path({str(OW.LOCK)!r}).exists()\n"
            f"Path({str(self.movers_marker)!r}).write_text(f'lock={{held}}')\n"
            "print('MOVERS-STUB universe 0 · fetched nothing (fixture)')\n")
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
        OW.arm = _schedule("arm")

        def _topup(slot, log=print):
            self.ran.append(f"topup[{slot}]")
            self.lock_seen["topup"] = OW.LOCK.exists()
            log(f"ORACLE TOP-UP · slot={slot} · 0 pair(s) from the pinned scope (stub)")
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
        self._td.cleanup()
        return False

    def main(self, argv: list[str]) -> tuple[int, str]:
        # belt and braces: refuse to drive main() at anything but the sandbox
        assert OW.FLAG.parent == self.td and OW.LOCK.parent == self.td \
            and OW.SELFCHECK.parent == self.td, "sandbox not in place"
        assert "--install" not in argv
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
            OW.ondemand_flag_action = lambda rc, no_fetch: "raise" if rc else "clear"
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


def f_sk_2e() -> None:
    prove("F-SK-2e", "THE SUSPENDED CLOCK — no on-demand run may enter "
                     "reschedule_if_drifted or arm",
          lambda: _schedule_untouched(legacy_path=True),
          lambda: _schedule_untouched(legacy_path=False))


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

def _identity(one_sided: bool) -> tuple[bool, str]:
    """CONVENTIONS §0: "checking only the path passes a copy left behind in a
    cloud-synced tree, and checking only for the absence of markers passes any
    directory on the machine." `one_sided=True` plants the second mistake."""
    home = Path.home()
    matrix = [
        ("the real tree", home / "Naiad", home / "Naiad", True),
        ("a OneDrive copy", home / "OneDrive" / "Naiad", home / "Naiad", False),
        ("an iCloud copy", home / "Library" / "Mobile Documents" /
         "com~apple~CloudDocs" / "Naiad", home / "Naiad", False),
        ("a stray clone", home / "src" / "Naiad", home / "Naiad", False),
        ("the real tree, run from a cloud cwd", home / "Naiad",
         home / "OneDrive" / "x", False),
    ]
    marker_only = (lambda root=None, home=None, cwd=None:
                   (not any(m in str(root or OW.ROOT) for m in OW.CLOUD_MARKERS),
                    "marker side only"))
    gate = marker_only if one_sided else OW.identity_gate

    # THE CONSEQUENCE FIRST, through the real main(): what a misrouted tree DOES.
    touched = {}
    for name, sub in (("cloud", ("OneDrive", "Naiad")), ("stray", ("elsewhere", "Naiad"))):
        with Sandbox() as sb:
            fake = sb.td.joinpath(*sub)
            fake.mkdir(parents=True)
            OW.ROOT = fake
            if one_sided:
                OW.identity_gate = marker_only
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
    wrong = [name for name, root, cwd, want in matrix
             if gate(root=root, home=home, cwd=cwd)[0] != want]
    if wrong:
        return False, f"the gate misjudges: {wrong}"
    return True, (f"through the real main() a cloud ROOT and a stray ROOT both HALT "
                  f"exit {sorted({v['rc'] for v in touched.values()})} with no lock "
                  f"taken, no job run, no movers process, no flag, no selfcheck row; "
                  f"and the pure gate is right on all {len(matrix)} cases (real tree, "
                  f"OneDrive copy, iCloud copy, stray clone, real tree from a cloud cwd)")


def f_sk_3() -> None:
    prove("F-SK-3", "THE IDENTITY GATE — two-sided, and it halts nonzero before "
                    "any action",
          lambda: _identity(one_sided=True), lambda: _identity(one_sided=False))


# ══════════════════════════════════════════════════════════════════ MAIN

def main() -> int:
    print("=" * 78)
    print(f"ORACLE ON-DEMAND FIXTURES — {datetime.now(timezone.utc).isoformat()[:19]}Z")
    print(f"  skill    {SKILL.relative_to(ROOT)}")
    print(f"  wrapper  {WRAPPER.relative_to(ROOT)} sha256 "
          f"{hashlib.sha256(WRAPPER.read_bytes()).hexdigest()}")
    print(f"  chain    {' -> '.join(step_ids())}")
    print("=" * 78)
    fixtures = (f_sk_1, f_sk_2a, f_sk_2b, f_sk_2c, f_sk_2d, f_sk_2e, f_sk_2f, f_sk_3)
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
    raise SystemExit(main())
