"""ORACLE MOVERS FIXTURES — F-MV-1 .. F-MV-7 of queue OR-1 (STEP E, fetch half).

Same law as the BR-1 and BR-1b sets: every fixture runs BOTH legs through
`prove()`, the BREAK leg first, and a fixture whose break leg passes is counted
RED ("proves nothing"). Both legs of every fixture run the SAME checker — the
break differs only in what it is pointed at — so the redness always comes from
the property under test and never from the wrapper's arithmetic (the lesson
written into F-TU-6's docstring).

A break leg here usually plants SEVERAL faults, one per claim the real leg
makes, each run through the checker ON ITS OWN (_every_plant_red): the leg is
RED only if EVERY plant was caught, and one plant that slips through makes the
whole fixture VOID by name. (The first build planted one fault per fixture;
the verifier showed by mutation that the unplanted halves — the AST half of
F-MV-1, the closure half of F-MV-2 — were sound but unproven by the suite.)

  F-MV-1  the kline cache is sha-identical across a REAL movers run, and the
          organ's AST references no cache-writing name          (contract)
  F-MV-2  firewall: import closure + source scan + the one write path (contract)
  F-MV-3  the written json: status OK, universe ≥ 150 AND ENUMERATED, both
          tables sorted by signed pct DESC, top-50 slices well-formed (contract)
  F-MV-4  key purity: no key of the json carries a banned outcome token — an
          ADDITION by the OR-1 build, because hard rule 7 binds this document
          and a rule with no fixture is prose
  F-MV-5  failure path: a dead wire writes today's json as FAIL with EMPTY
          tables over any earlier success, and exits 1 — an ADDITION by the
          OR-1 build, because "never stale numbers" is the contract's own
          sentence and nothing else here would notice it breaking. In-process,
          stub wire. Also: the placeholder is on disk BEFORE the first call, a
          dead sweep stops within (tolerated failures + workers) calls, a hung
          sweep is abandoned at the run deadline, every document has every key
  F-MV-6  a run that does NOT LIVE to see its failure — an ADDITION of fix
          round 1, and the reason there was one. The REAL organ in a CHILD
          PROCESS, the REAL engine.data._get with its REAL backoff (only requests.get is
          stubbed), the wire dying after the ticker call, an earlier same-day
          SUCCESS planted on disk: the child is SIGKILLed mid-sweep (what the
          on-demand wrapper's timeout does), sent SIGINT mid-sweep (what the
          operator's Ctrl-C does), and left to finish on a universe-sized dead
          wire against a clock. The FIRST BUILD of this organ wrote its document
          only at the END of main(); the verifier killed it mid-sweep and the planted
          success was still there, status OK, dated today — printable. F-MV-5
          could not see that: its stub replaces _get outright and nothing in it
          ever kills anything.
  F-MV-7  --dry-run prints the REGISTER and the endpoints, reaches the wire zero
          times and creates nothing — contract text ("--dry-run prints the
          REGISTER and endpoints and fetches nothing") that the first build left
          to a by-hand check, and that died with a ValueError whenever the
          output dir was redirected outside the repo

WHAT THIS SUITE DOES TO THE WORLD. F-MV-1's real leg performs ONE real fetch
(~530 calls, ~570 request weight) in a SUBPROCESS whose output directory is
redirected into a TemporaryDirectory by module-attribute assignment — the same
idiom oracle_topup.enumerate_scope uses — so re-running the suite NEVER rewrites
the day's real movers json, whose sha the build document cites. F-MV-3 and
F-MV-4 read the newest REAL json under research_outputs/oracle/movers and write
nothing. F-MV-5 drives the organ IN-PROCESS against a STUB network (no real
call) with its output dir redirected into a TemporaryDirectory. F-MV-6 does the
same in CHILD processes (no real call either: requests.get itself is replaced in
the child) and costs about two minutes of backoff, because waiting out the real
backoff is the point. F-MV-7 is in-process on a counting stub. Nothing here
writes the cache, the live lane, or the bus.

    F-MV-1 MUST NOT BE RUN CONCURRENTLY WITH A TOP-UP OR A BACKFILL. It
    fingerprints the whole kline cache (~632 MB) before and after the run; any
    other process that legitimately writes the cache in between turns it RED,
    and that RED would be TRUE ("the cache changed") while saying nothing about
    this organ. Run it on a quiet cache. The detail line names every file that
    was added, removed or changed, so a collision can at least be recognised.

Run:  ~/venvs/naiad/bin/python scripts/oracle_movers_fixtures.py
Exit: 0 if every fixture is green on REAL and red on BREAK; 1 otherwise.
"""
from __future__ import annotations

import ast
import contextlib
import copy
import hashlib
import io
import json
import math
import os
import re
import signal
import subprocess
import sys
import tempfile
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import oracle_movers as OM                     # noqa: E402
from engine.data import cache_dir              # noqa: E402  (the FIXTURE may name it; the organ may not)

ORGAN_SRC = ROOT / "scripts" / "oracle_movers.py"

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


def _every_plant_red(cases) -> tuple[bool, str]:
    """A BREAK leg made of several planted faults, each through the checker ALONE.

    Returns in break-leg sense: ok=True means VOID. If even one plant comes back
    green the leg says which — a checker that is red for three reasons out of
    four must not hide the fourth behind the other three."""
    got = [(label, *fn()) for label, fn in cases]
    green = [label for label, ok, _ in got if ok]
    if green:
        return True, f"PLANTED FAULT(S) NOT CAUGHT: {green}"
    return False, (f"all {len(got)} plant(s) caught, each alone — "
                   + " ‖ ".join(f"[{label}] {detail}" for label, _, detail in got))


# ══════════════════════════════════════════════════════ SHARED AST MACHINERY
# Fixtures scan CODE, not prose (BR-1 §2). The organ's docstring deliberately
# NAMES the things it never does; a substring scan would trip on that sentence
# — the one we most want to keep — so every scan below walks the AST.

def _docstring_ids(tree: ast.AST) -> set[int]:
    docs = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef,
                             ast.ClassDef)):
            body = getattr(node, "body", None)
            if body and isinstance(body[0], ast.Expr) and \
                    isinstance(body[0].value, ast.Constant) and \
                    isinstance(body[0].value.value, str):
                docs.add(id(body[0].value))
    return docs


def _string_constants(tree: ast.AST) -> list[str]:
    docs = _docstring_ids(tree)
    return [n.value for n in ast.walk(tree)
            if isinstance(n, ast.Constant) and isinstance(n.value, str)
            and id(n) not in docs]


def _identifiers(tree: ast.AST) -> set[str]:
    """Every name the code can REFER to: variables, attributes, imports, defs, args."""
    out: set[str] = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Name):
            out.add(n.id)
        elif isinstance(n, ast.Attribute):
            out.add(n.attr)
        elif isinstance(n, ast.alias):
            out.update(n.name.split("."))
            if n.asname:
                out.add(n.asname)
        elif isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            out.add(n.name)
        elif isinstance(n, ast.arg):
            out.add(n.arg)
        elif isinstance(n, ast.keyword) and n.arg:
            out.add(n.arg)
        if isinstance(n, ast.ImportFrom) and n.module:
            out.update(n.module.split("."))
    return out


def _imports(tree: ast.AST) -> list[str]:
    """Dotted names of everything imported, `from a.b import c` giving 'a.b.c'."""
    out = []
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            out += [a.name for a in n.names]
        elif isinstance(n, ast.ImportFrom):
            out += [f"{n.module or ''}.{a.name}".strip(".") for a in n.names]
    return out


def _organ_tree(extra_src: str = "") -> ast.AST:
    return ast.parse(ORGAN_SRC.read_text() + "\n" + extra_src)


# ══════════════════════════════════ F-MV-1 · THE CACHE IS NEVER WRITTEN

# Referencing ANY of these is a fault, whether or not it is ever called: the
# organ has no business holding a handle on the cache. `cache_dir` and the path
# builders are here because engine.data.cache_dir() itself performs a mkdir.
CACHE_WRITING_NAMES = (
    "backfill_klines", "_save_cache", "load_klines", "to_parquet", "oracle_topup",
    "cache_dir", "_kline_path", "_funding_path", "backfill_funding",
    "write_coverage_report", "read_parquet",
)


def cache_fingerprint(root: Path) -> dict:
    """sha256 over the sorted (relative path, size, sha256-of-content) of EVERY file.

    Content-hashed, not mtime-based: an in-place rewrite that keeps the size and
    restores the mtime still moves the fingerprint. ~632 MB is a few seconds.
    """
    rows = []
    total = 0
    for p in sorted(Path(root).rglob("*")):
        if not p.is_file():
            continue
        h = hashlib.sha256()
        with p.open("rb") as fh:
            for chunk in iter(lambda: fh.read(1 << 20), b""):
                h.update(chunk)
        size = p.stat().st_size
        total += size
        rows.append([p.relative_to(root).as_posix(), size, h.hexdigest()])
    rows.sort()
    sha = hashlib.sha256(json.dumps(rows, separators=(",", ":")).encode("utf-8")).hexdigest()
    return {"sha256": sha, "files": len(rows), "bytes": total,
            "table": {r[0]: (r[1], r[2]) for r in rows}}


def _cache_name_refs(extra_src: str = "") -> list[str]:
    tree = _organ_tree(extra_src)
    named = _identifiers(tree) | set(_string_constants(tree))   # getattr("…") too
    return sorted(n for n in CACHE_WRITING_NAMES if n in named)


def _real_movers_run() -> dict:
    """A REAL fetch by the real organ, in its own process, output dir redirected."""
    code = ("import sys; from pathlib import Path; "
            f"sys.path[:0] = [{str(ROOT)!r}, {str(ROOT / 'scripts')!r}]; "
            "import oracle_movers as OM; OM.MOVERS_DIR = Path(sys.argv[1]); "
            "raise SystemExit(OM.main([]))")
    with tempfile.TemporaryDirectory(prefix="oracle-movers-") as td:
        out = subprocess.run([sys.executable, "-c", code, td], cwd=ROOT,
                             capture_output=True, text=True, timeout=1500)
        files = sorted(Path(td).glob("movers_*.json"))
        doc = json.loads(files[-1].read_text()) if files else {}
    return {"status": doc.get("status", "NO-DOCUMENT"), "rc": out.returncode,
            "universe_count": doc.get("universe_count"),
            "weekly_rows": len(doc.get("weekly", [])),
            "overnight_rows": len(doc.get("overnight", [])),
            "runtime_seconds": doc.get("runtime_seconds"),
            "fail_reasons": doc.get("fail_reasons"),
            "stderr_tail": out.stderr[-300:]}


def _cache_untouched(root: Path, runner, extra_src: str = "") -> tuple[bool, str]:
    before = cache_fingerprint(root)
    info = runner()
    after = cache_fingerprint(root)
    bad = []
    if before["sha256"] != after["sha256"]:
        b, a = before["table"], after["table"]
        bad.append(f"the cache CHANGED across the run — added {sorted(set(a) - set(b))[:4]}, "
                   f"removed {sorted(set(b) - set(a))[:4]}, "
                   f"changed {sorted(k for k in set(a) & set(b) if a[k] != b[k])[:4]} "
                   f"({before['sha256'][:16]}… -> {after['sha256'][:16]}…)")
    refs = _cache_name_refs(extra_src)
    if refs:
        bad.append(f"the organ's AST references cache-writing name(s) {refs}")
    # An organ that died on its first line also leaves the cache untouched. The
    # proof only means something if the run REALLY fetched and REALLY wrote.
    if info.get("status") != "OK" or info.get("rc") != 0 or not info.get("weekly_rows"):
        bad.append(f"the movers run did not complete OK ({info}) — an unchanged cache "
                   f"after a run that did nothing proves nothing")
    if bad:
        return False, "; ".join(bad)
    return True, (f"kline cache sha-identical before and after a REAL movers run "
                  f"(universe {info['universe_count']}, {info['overnight_rows']} overnight + "
                  f"{info['weekly_rows']} weekly rows, {info['runtime_seconds']} s, rc 0): "
                  f"{before['files']} file(s), {before['bytes']:,} B, fingerprint "
                  f"sha256 {before['sha256']} both times; and the organ's AST references "
                  f"none of {len(CACHE_WRITING_NAMES)} cache-writing names "
                  f"{list(CACHE_WRITING_NAMES)}")


def f_mv_1() -> None:
    """MUST NOT be run concurrently with a top-up or a backfill — see the module docstring."""
    pretend_ok = {"status": "OK", "rc": 0, "universe_count": 0, "weekly_rows": 1,
                  "overnight_rows": 1, "runtime_seconds": 0.0}

    def new_file(fake: Path) -> None:
        (fake / "klines" / "PLANTEDUSDT_1d.parquet").write_bytes(b"PAR1-planted")

    def same_size_same_mtime_rewrite(fake: Path) -> None:
        # The case a size/mtime snapshot would miss, ISOLATED: same path, same
        # byte count, the old mtime put back. Only the content hash can move.
        p = fake / "klines" / "AAAUSDT_4h.parquet"
        st = p.stat()
        p.write_bytes(b"PAR1-fake-CLOSED-bars")
        os.utime(p, ns=(st.st_atime_ns, st.st_mtime_ns))

    def plant(writer=None, extra_src: str = ""):
        # A COPY-FREE fake cache: two small files in a temp dir, and a pretend
        # organ that reports a completed run. Same checker, same assertions as
        # the real leg; only the root, the runner and (for the AST half) the
        # source differ.
        def case() -> tuple[bool, str]:
            with tempfile.TemporaryDirectory(prefix="fake-cache-") as td:
                fake = Path(td)
                (fake / "klines").mkdir()
                (fake / "klines" / "AAAUSDT_4h.parquet").write_bytes(b"PAR1-fake-closed-bars")
                (fake / "klines" / "BBBUSDT_4h.parquet").write_bytes(b"PAR1-fake-other-bars!")

                def run() -> dict:
                    if writer:
                        writer(fake)
                    return dict(pretend_ok)
                return _cache_untouched(fake, run, extra_src)
        return case

    prove("F-MV-1", "THE CACHE IS NEVER WRITTEN — sha-identical across a real run",
          lambda: _every_plant_red([
              ("a new parquet dropped into the cache", plant(new_file)),
              ("an in-place rewrite, same size, same mtime", plant(same_size_same_mtime_rewrite)),
              ("cache untouched, but the source imports a cache writer",
               plant(extra_src="from engine.data import _save_cache\n")),
          ]),
          lambda: _cache_untouched(cache_dir(), _real_movers_run))


# ══════════════════════════════════ F-MV-2 · FIREWALL

# Component-wise, as F-BR-3 / F-TU-3: a banned token is banned at ANY dotted
# position, so `engine.journal` cannot hide behind a top-level-only test.
BANNED_COMPONENTS = ("journal", "forward_log", "positions", "publish_exchange", "trading",
                     "posture_engine", "oracle_daily", "oracle_topup", "analytics")

# An ALLOW-list on top of the ban-list. Measured 2026-09-21: the organ's closure
# holds exactly these estate modules — engine.data imports engine.cells and
# nothing else of ours, so NOTHING is inherited and there is no
# INHERITED_DISCLOSED table to keep (contrast F-BR-3, where tierc2_rules ->
# engine.s1 drags engine.trading and engine.journal in). If engine/data.py ever
# grows an estate import, this goes RED and names it, rather than quietly
# widening what the fetch organ can reach.
ESTATE_ALLOWED = {"engine", "engine.cells", "engine.data", "oracle_movers"}

BANNED_NAMES = ("read_journal", "load_journal", "journal_rows", "read_trades",
                "load_trades", "open_journal", "publish", "subprocess", "system",
                "popen", "Popen")

# Calls that can put bytes on disk or move them. Every one must sit lexically
# inside write_doc(), the organ's single write path.
WRITE_CALLS = ("open", "write_text", "write_bytes", "replace", "rename", "unlink",
               "mkdir", "makedirs", "touch", "remove", "rmtree", "copy", "copyfile",
               "move", "dump", "to_parquet", "to_csv", "to_json", "to_pickle", "save",
               "savez", "symlink_to", "hardlink_to")
WRITE_FUNCTION = "write_doc"
MOVERS_REL = "research_outputs/oracle/movers"
# The organ names ITSELF once (ORGAN_REL), to stamp its own sha256 into the json
# (a read) and to say in the json which file wrote it.
ORGAN_SELF = "scripts/oracle_movers.py"
# What counts as a path literal: segments of path characters joined by '/', no
# whitespace. An f-string fragment such as "/min)" or a lone "/" is not one; a
# URL endpoint, "exchange/reports/x.md" and "~/.cache/naiad" all are.
PATH_SHAPE = re.compile(r"^[\w.~-]*(?:/[\w.~-]+)+/?$")
# Directory names no path in the organ may be built from, even piecewise
# (ROOT / "exchange" / … has no '/' in any literal).
BANNED_DIR_LITERALS = ("exchange", "briefs", "klines", "funding", "data_cache",
                       "calibration", "tape", "payloads", "journal")

# The F-BR-10 vocabulary (oracle_daily.BANNED_CALIBRATION_KEYS), COPIED rather
# than imported: importing oracle_daily here would put the Oracle in the movers
# suite's process, and that file is under concurrent edit during the OR-1 build.
# _banned_vocabulary() unions this with the live tuple read by AST, no import.
BANNED_TOKENS = (
    "win", "loss", "pnl", "r_multiple", "net_r", "gross_r", "return", "outcome",
    "hit_rate", "expectancy", "profit", "equity", "mfe", "mae", "term_h20",
    "term_h100", "sharpe", "edge", "score_of_signal", "accuracy", "precision",
)


def _banned_vocabulary() -> tuple[tuple[str, ...], str]:
    try:
        tree = ast.parse((ROOT / "scripts" / "oracle_daily.py").read_text())
        for n in ast.walk(tree):
            if isinstance(n, ast.Assign) and any(
                    isinstance(t, ast.Name) and t.id == "BANNED_CALIBRATION_KEYS"
                    for t in n.targets):
                live = tuple(ast.literal_eval(n.value))
                merged = tuple(sorted(set(BANNED_TOKENS) | set(live)))
                return merged, (f"{len(merged)} terms = local copy ∪ live "
                                f"oracle_daily.BANNED_CALIBRATION_KEYS (read by AST, "
                                f"{len(live)} terms, not imported)")
    except Exception as e:                       # mid-edit or unparseable: say so
        return BANNED_TOKENS, (f"{len(BANNED_TOKENS)} terms, LOCAL COPY ONLY — "
                               f"oracle_daily.py unreadable ({e.__class__.__name__})")
    return BANNED_TOKENS, f"{len(BANNED_TOKENS)} terms, LOCAL COPY ONLY — live tuple not found"


def _stem(t: str) -> str:
    for suf in ("ies", "es", "s"):
        if len(t) > 3 and t.endswith(suf):
            return t[: -len(suf)] + ("y" if suf == "ies" else "")
    return t


def _token_hits(names, vocab) -> list[str]:
    """F-BR-10's matcher: a banned term must appear as whole (stemmed) `_`-tokens."""
    hits = []
    for k in names:
        toks = {_stem(t) for t in re.split(r"[^a-z0-9]+", str(k).lower()) if t}
        for w in vocab:
            wt = {_stem(t) for t in re.split(r"[^a-z0-9]+", w.lower()) if t}
            if wt and wt <= toks:
                hits.append(f"{k} (matched {w!r})")
    return sorted(set(hits))


def _closure(modname: str, plant: str = "") -> dict:
    """The import closure, measured in a SUBPROCESS. `plant` is one extra statement
    run after the import — the break leg's way of making the closure really hold a
    module it must not, so the closure scan is driven red by a real sys.modules."""
    code = ("import sys, json, os; sys.path.insert(0,'.'); sys.path.insert(0,'scripts'); "
            f"import {modname}; {plant or 'pass'}; root = os.path.realpath('.') + os.sep; "
            "est = [n for n, m in list(sys.modules.items()) if getattr(m, '__file__', None) "
            "and os.path.realpath(m.__file__).startswith(root)]; "
            "print(json.dumps({'all': sorted(set(sys.modules)), 'estate': sorted(est)}))")
    out = subprocess.run([sys.executable, "-c", code], cwd=ROOT,
                         capture_output=True, text=True)
    if out.returncode != 0:
        raise RuntimeError(out.stderr[-400:])
    return json.loads(out.stdout.strip().splitlines()[-1])


def _assigned_names(tree: ast.AST) -> set[str]:
    """Everything the code NAMES: assignment targets, args, keywords, dict keys."""
    out: set[str] = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store):
            out.add(n.id)
        elif isinstance(n, ast.arg):
            out.add(n.arg)
        elif isinstance(n, ast.keyword) and n.arg:
            out.add(n.arg)
        elif isinstance(n, ast.Dict):
            out.update(k.value for k in n.keys
                       if isinstance(k, ast.Constant) and isinstance(k.value, str))
    return out


def _write_sites(tree: ast.AST) -> list[str]:
    """Write-capable calls OUTSIDE write_doc(), as 'name@line'."""
    inside: set[int] = set()
    for n in ast.walk(tree):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == WRITE_FUNCTION:
            inside.update(id(x) for x in ast.walk(n))
    out = []
    for n in ast.walk(tree):
        if not isinstance(n, ast.Call) or id(n) in inside:
            continue
        f = n.func
        name = f.id if isinstance(f, ast.Name) else f.attr if isinstance(f, ast.Attribute) else None
        if name in WRITE_CALLS:
            out.append(f"{name}@L{n.lineno}")
    return out


def _firewall(extra_src: str = "", closure_plant: str = "") -> tuple[bool, str]:
    bad = []
    clo = _closure("oracle_movers", closure_plant)
    mods = clo["all"]
    for b in BANNED_COMPONENTS:
        hits = [m for m in mods if b in m.split(".")]
        if hits:
            bad.append(f"closure reaches {sorted(hits)[:3]}")
    stray = sorted(set(clo["estate"]) - ESTATE_ALLOWED)
    if stray:
        bad.append(f"closure holds estate module(s) outside the allow-list: {stray[:5]}")

    tree = _organ_tree(extra_src)
    for imp in _imports(tree):
        hit = [b for b in BANNED_COMPONENTS if b in imp.split(".")]
        if hit:
            bad.append(f"source imports {imp} (banned component {hit[0]!r})")
    ids = _identifiers(tree)
    for nm in BANNED_NAMES:
        if nm in ids:
            bad.append(f"source references a forbidden name: {nm!r}")
    for nm in CACHE_WRITING_NAMES:
        if nm in ids:
            bad.append(f"source references a cache name: {nm!r}")
    vocab, vocab_note = _banned_vocabulary()
    agg = _token_hits(_assigned_names(tree), vocab)
    if agg:
        bad.append(f"source assigns/keys an outcome-vocabulary name: {agg[:4]}")

    # ── the one write path ────────────────────────────────────────────────
    sites = _write_sites(tree)
    if sites:
        bad.append(f"write-capable call(s) outside {WRITE_FUNCTION}(): {sites[:5]}")
    consts = _string_constants(tree)
    pathy = sorted({c for c in consts if PATH_SHAPE.match(c)})
    foreign = [c for c in pathy
               if not (c == MOVERS_REL or c == ORGAN_SELF or c.startswith("/fapi/"))]
    if foreign:
        bad.append(f"path literal(s) that are neither the movers dir, a /fapi/ endpoint "
                   f"nor the organ's own name: {foreign[:4]}")
    bare = sorted({c for c in consts if c in BANNED_DIR_LITERALS})
    if bare:
        bad.append(f"bare directory literal(s) a foreign path could be built from: {bare}")
    ext = sorted({c for c in consts if not re.search(r"\s", c)
                  and re.search(r"\.(parquet|jsonl|html|md|csv|flag)$", c)})
    if ext:
        bad.append(f"file-name literal(s) of a kind this organ never writes: {ext[:4]}")
    if MOVERS_REL not in consts:
        bad.append(f"the movers path literal {MOVERS_REL!r} is not in the source")
    if OM.MOVERS_DIR != ROOT / "research_outputs" / "oracle" / "movers":
        bad.append(f"oracle_movers.MOVERS_DIR resolves to {OM.MOVERS_DIR}")

    if bad:
        return False, "; ".join(sorted(set(bad)))
    endpoints = [c for c in pathy if c.startswith("/fapi/")]
    return True, (
        f"import closure of oracle_movers is {len(mods)} modules; no component in "
        f"{list(BANNED_COMPONENTS)} at any dotted position; estate modules in the closure "
        f"are EXACTLY {sorted(clo['estate'])} — nothing inherited, nothing to disclose "
        f"(engine.data imports only engine.cells). AST of the organ: no banned import, "
        f"none of {len(BANNED_NAMES)} journal/publish/shell names, none of "
        f"{len(CACHE_WRITING_NAMES)} cache names, no assigned name / arg / dict key "
        f"carrying an outcome token ({vocab_note}). WRITE PATH: every write-capable call "
        f"({len(WRITE_CALLS)} kinds scanned) sits inside {WRITE_FUNCTION}(); the only "
        f"path literals are {MOVERS_REL!r}, the organ's own name {ORGAN_SELF!r} (read, for its sha) "
        f"and the endpoints {endpoints}; MOVERS_DIR "
        f"resolves to {OM.MOVERS_DIR.relative_to(ROOT)}")


def f_mv_2() -> None:
    prove("F-MV-2", "FIREWALL — import closure, source AST, one write path",
          lambda: _every_plant_red([
              # a direct journal READ in the source — the thing §2 actually forbids
              ("source imports a journal reader",
               lambda: _firewall(extra_src="from engine.journal import read_journal\n")),
              # the same module REALLY imported in the closure subprocess, source clean:
              # only the sys.modules ban-list can see it
              ("closure really holds engine.journal",
               lambda: _firewall(closure_plant="import engine.journal")),
              # an estate module that is on no ban-list: only the ALLOW-list can see it
              ("closure really holds an un-banned estate module",
               lambda: _firewall(closure_plant="import engine.version")),
          ]),
          lambda: _firewall())


# ══════════════════════════════════ F-MV-3 · THE WRITTEN JSON

# OR-1 STEP E / gate G-6, verbatim: "F-MV-3: universe count ≥ 150 and
# enumerated". The floor lives HERE and not in the organ, which by contract
# prints the count and never asserts it.
UNIVERSE_FLOOR = 150
ROW_KEYS = {"symbol", "pct", "last_price"}


def newest_doc() -> tuple[Path | None, dict | None]:
    files = sorted(OM.MOVERS_DIR.glob("movers_*.json"))
    if not files:
        return None, None
    return files[-1], json.loads(files[-1].read_text())


def _truncate(doc: dict, n: int) -> dict:
    """A CONSISTENT n-symbol copy: every list filtered, the count restated, the
    top slices recut — so the ONLY fault left in it is the size of the universe."""
    d = copy.deepcopy(doc)
    keep = set(d["universe"][:n])
    d["universe"] = [s for s in d["universe"] if s in keep]
    d["universe_count"] = len(d["universe"])
    for t in ("overnight", "weekly"):
        d[t] = [r for r in d[t] if r["symbol"] in keep]
        d[f"{t}_null"] = [r for r in d[f"{t}_null"] if r["symbol"] in keep]
        d[f"{t}_top"] = d[t][: d["top_n"]]
    return d


def _weekly_definition_proof() -> list[str]:
    """The pure definition, driven both ways on synthetic bars before any file is read."""
    day = OM.DAY_MS
    t = 1_790_000_000_000
    d0 = OM.day_open(t)
    closes = [100.0, 1, 2, 3, 4, 5, 6, 110.0]
    good = [[d0 - (7 - i) * day, "0", "0", "0", str(c)] for i, c in enumerate(closes)]
    wrong = []
    pct, last, why = OM.weekly_from_bars(good, t, t)
    if (pct, last, why) != (10.0, 110.0, None):
        wrong.append(f"8 good bars gave {(pct, last, why)}, want (10.0, 110.0, None)")
    holed = [b[:] for b in good]
    holed[0][0] -= day                                        # index 0 is 8 days back
    stale = [[b[0] - day] + b[1:] for b in good]              # last bar is yesterday
    for name, bars in (("7 bars", good[1:]), ("a hole", holed), ("a stale last bar", stale)):
        pct, last, why = OM.weekly_from_bars(bars, t, t)
        if pct is not None or not why:
            wrong.append(f"{name} gave a number ({pct}) instead of a listed null")
    return wrong


def _shape_faults(doc: dict) -> list[str]:
    """EVERY document carries EVERY key (OM.DOC_KEYS) — OK, FAIL and placeholder
    alike — so a reader never needs .get() to survive a FAIL document."""
    out = []
    missing, extra = sorted(set(OM.DOC_KEYS) - set(doc)), sorted(set(doc) - set(OM.DOC_KEYS))
    if missing or extra:
        out.append(f"top-level keys differ from DOC_KEYS — missing {missing}, "
                   f"undeclared {extra}")
    wf = doc.get("weekly_fetch")
    if not isinstance(wf, dict) or set(wf) != set(OM.WEEKLY_FETCH_KEYS):
        out.append(f"weekly_fetch keys are {sorted(wf) if isinstance(wf, dict) else wf!r}, "
                   f"not {sorted(OM.WEEKLY_FETCH_KEYS)}")
    return out


def _wellformed(doc: dict | None, path: Path | None) -> tuple[bool, str]:
    wrong = _weekly_definition_proof()
    if wrong:
        return False, "weekly definition is wrong on synthetic bars: " + "; ".join(wrong)
    if doc is None:
        return False, (f"no movers_*.json under {OM.MOVERS_DIR.relative_to(ROOT)} — "
                       f"run scripts/oracle_movers.py first")
    bad = []
    if doc.get("status") != "OK":
        bad.append(f"status is {doc.get('status')!r} ({doc.get('fail_reasons')}), not OK")
    if "DISPLAY-ONLY" not in str(doc.get("class", "")):
        bad.append("class line lacks the DISPLAY-ONLY fragment")
    if path is not None and path.name != f"movers_{doc.get('date')}.json":
        bad.append(f"file {path.name} carries date {doc.get('date')!r}")
    try:
        datetime.fromisoformat(doc["fetched_utc"])
    except Exception:
        bad.append(f"fetched_utc {doc.get('fetched_utc')!r} is not an ISO stamp")
    bad += _shape_faults(doc)
    if doc.get("in_flight") is not False:
        bad.append(f"in_flight is {doc.get('in_flight')!r} in a document that says OK — "
                   f"only the pre-fetch placeholder may carry true")

    uni = doc.get("universe") or []
    n_distinct = len(set(uni))
    # ENUMERATED, NOT ASSERTED: three independent counts must agree.
    if not (doc.get("universe_count") == len(uni) == n_distinct):
        bad.append(f"universe_count {doc.get('universe_count')} / len(universe) {len(uni)} / "
                   f"distinct {n_distinct} disagree")
    if uni != sorted(uni) or not all(isinstance(s, str) and s for s in uni):
        bad.append("universe is not a sorted list of symbols")
    if n_distinct < UNIVERSE_FLOOR:
        bad.append(f"universe holds {n_distinct} distinct symbol(s), below the contract "
                   f"floor of {UNIVERSE_FLOOR}")

    uset = set(uni)
    top_n = doc.get("top_n")
    if top_n != OM.TOP_N or top_n != 50:
        bad.append(f"top_n is {top_n!r}, ruling 7 says 50")
    for t in ("overnight", "weekly"):
        rows, nulls, top = doc.get(t) or [], doc.get(f"{t}_null") or [], doc.get(f"{t}_top")
        syms = [r.get("symbol") for r in rows]
        if any(set(r) != ROW_KEYS for r in rows):
            bad.append(f"{t}: a row's keys are not exactly {sorted(ROW_KEYS)}")
            continue
        if len(set(syms)) != len(syms):
            bad.append(f"{t}: duplicate symbol(s) in the table")
        if not all(isinstance(r["pct"], (int, float)) and math.isfinite(r["pct"])
                   and isinstance(r["last_price"], (int, float))
                   and math.isfinite(r["last_price"]) and r["last_price"] > 0 for r in rows):
            bad.append(f"{t}: a non-finite pct or a non-positive last_price")
            continue
        keys = [(-r["pct"], r["symbol"]) for r in rows]
        if keys != sorted(keys):
            i = next(i for i in range(len(keys) - 1) if keys[i] > keys[i + 1])
            bad.append(f"{t}: NOT sorted by signed pct DESC — row {i} {rows[i]['symbol']} "
                       f"{rows[i]['pct']} precedes {rows[i + 1]['symbol']} {rows[i + 1]['pct']}")
        nsyms = [r.get("symbol") for r in nulls]
        if set(syms) & set(nsyms) or (set(syms) | set(nsyms)) != uset:
            bad.append(f"{t}: rows + nulls do not account for the universe exactly "
                       f"(unaccounted {sorted(uset - set(syms) - set(nsyms))[:4]}, "
                       f"foreign {sorted((set(syms) | set(nsyms)) - uset)[:4]})")
        if any(not r.get("reason") for r in nulls):
            bad.append(f"{t}: a null is listed without a reason")
        if top != rows[: top_n or 0]:
            bad.append(f"{t}_top is not the first {top_n} rows of {t}")
        elif len(top) != top_n:
            bad.append(f"{t}_top holds {len(top)} row(s), not {top_n}")
    wf = doc.get("weekly_fetch") or {}
    if not (isinstance(wf.get("fraction"), (int, float))
            and wf["fraction"] >= OM.WEEKLY_SUCCESS_FLOOR):
        bad.append(f"weekly_fetch.fraction {wf.get('fraction')} is below the floor "
                   f"{OM.WEEKLY_SUCCESS_FLOOR} in a document that says OK")
    if bad:
        return False, "; ".join(bad)

    today = OM.local_date()
    o, w = doc["overnight"], doc["weekly"]
    return True, (
        f"{path.name if path else '<doc>'} (date {doc['date']}"
        f"{'' if doc['date'] == today else f' — NOT today {today}'}, fetched "
        f"{doc['fetched_utc']}): status OK; universe ENUMERATED — universe_count "
        f"{doc['universe_count']} == len(universe) {len(uni)} == distinct {n_distinct} "
        f">= {UNIVERSE_FLOOR}, sorted; overnight {len(o)} rows + "
        f"{len(doc['overnight_null'])} null and weekly {len(w)} rows + "
        f"{len(doc['weekly_null'])} null each account for the universe exactly; both "
        f"tables sorted by signed pct DESC (overnight {o[0]['symbol']} {o[0]['pct']:+.3f} … "
        f"{o[-1]['symbol']} {o[-1]['pct']:+.3f}; weekly {w[0]['symbol']} {w[0]['pct']:+.3f} … "
        f"{w[-1]['symbol']} {w[-1]['pct']:+.3f}); overnight_top and weekly_top are exactly "
        f"rows[:50]; weekly fetch fraction {wf['fraction']} >= {OM.WEEKLY_SUCCESS_FLOOR}; "
        f"all {len(OM.DOC_KEYS)} DOC_KEYS present and nothing undeclared, in_flight false; "
        f"weekly definition proven both ways on synthetic bars")


def f_mv_3() -> None:
    path, doc = newest_doc()
    def without(key: str) -> dict | None:
        d = copy.deepcopy(doc) if doc else None
        if d:
            d.pop(key, None)
        return d

    def unsorted_copy() -> dict | None:
        d = copy.deepcopy(doc) if doc else None
        if d and len(d.get("weekly") or []) > 1:
            d["weekly"][0], d["weekly"][-1] = d["weekly"][-1], d["weekly"][0]
            d["weekly_top"] = d["weekly"][: d["top_n"]]
        return d

    prove("F-MV-3", "THE JSON — status OK, universe ≥ 150 and enumerated, tables sorted",
          lambda: _every_plant_red([
              ("a consistent copy truncated to 100 symbols",
               lambda: _wellformed(_truncate(doc, 100) if doc else None, path)),
              ("the weekly table with its first and last rows swapped",
               lambda: _wellformed(unsorted_copy(), path)),
              ("a copy missing the key fetched_local",
               lambda: _wellformed(without("fetched_local"), path)),
          ]),
          lambda: _wellformed(doc, path))


# ══════════════════════════════════ F-MV-4 · KEY PURITY (hard rule 7)

def _keys_deep(o, out=None):
    out = [] if out is None else out
    if isinstance(o, dict):
        for k, v in o.items():
            out.append(str(k))
            _keys_deep(v, out)
    elif isinstance(o, list):
        for v in o:
            _keys_deep(v, out)
    return out


def _key_purity(doc: dict | None) -> tuple[bool, str]:
    if doc is None:
        return False, "no movers json to scan"
    vocab, note = _banned_vocabulary()
    keys = sorted(set(_keys_deep(doc)))
    hits = _token_hits(keys, vocab)
    if hits:
        return False, f"outcome-vocabulary key(s) in the movers json: {hits}"
    return True, (f"{len(keys)} distinct key(s) scanned recursively (register included), "
                  f"none carries a banned token ({note}); the number is called 'pct'")


def f_mv_4() -> None:
    _, doc = newest_doc()

    # UNCONDITIONAL plants (verifier finding on the first build: both used to sit behind
    # `if doc["weekly"]`, so on a day whose newest json is a FAIL document nothing
    # was planted and the fixture called itself void for a confusing reason). A
    # missing json still fails BOTH legs, which reads as what it is.
    def top_level() -> dict:
        d = copy.deepcopy(doc) if doc else {}
        d["range_edge"] = 1
        return d

    def nested_plural() -> dict:
        d = copy.deepcopy(doc) if doc else {}
        d.setdefault("weekly_fetch", {})["rows"] = [{"weekly_returns": 1.0}]   # dict in list in dict
        return d

    prove("F-MV-4", "KEY PURITY — no outcome token in any key of the json",
          lambda: _every_plant_red([
              ("a top-level key range_edge", lambda: _key_purity(top_level())),
              ("a PLURAL key weekly_returns nested in a list in a dict",
               lambda: _key_purity(nested_plural())),
          ]),
          lambda: _key_purity(doc))


# ══════════════════════════════════ F-MV-5 · FAILURE PATH (never stale numbers)

class _FakeResp:
    status_code = 200
    headers: dict = {}

    def __init__(self, payload):
        self._payload = payload

    def json(self):
        return self._payload


STUB_N = 200            # symbols on the stub exchange (F-MV-6 sizes its own)
HANG_S = 20.0           # how long a "hung" stub call blocks — far past IN_PROCESS_BOUND_S
HANG_DEADLINE_S = 1.0   # OM.RUN_DEADLINE_S as redirected for the hang mode
# Every in-process mode talks to a stub that answers at once, so main() has no
# business taking longer than this; the hang mode is the one that would.
IN_PROCESS_BOUND_S = 10.0

# The organ's OWN arithmetic, captured before any fault is planted on it.
_REAL_FLOOR_UNREACHABLE = OM.floor_unreachable
_REAL_WRITE_DOC = OM.write_doc


def _tolerated_failures(n: int) -> int:
    """The most failed fetches of n after which the floor can STILL be reached."""
    return max(f for f in range(n + 1) if not _REAL_FLOOR_UNREACHABLE(n, f))


def _stub_get(mode: str, n: int = STUB_N, on_call=None):
    """A stand-in for engine.data._get. NO real call is made in any mode.

      healthy        every endpoint answers            -> the organ must say OK
      outage         every call raises                 -> exchangeInfo fails
      weekly-outage  1 weekly call in 10 raises (0.90) -> under WEEKLY_SUCCESS_FLOOR
      dead-sweep     EVERY weekly call raises at once  -> the sweep must stop early
      hang           every weekly call blocks HANG_S   -> the run deadline must end it

    `fake_get.klines_calls` lists the symbols a weekly call was STARTED for;
    `on_call()` runs before every call (F-MV-5 uses it to look at the disk).
    """
    syms = [f"T{i:03d}USDT" for i in range(n)]
    started: list[str] = []

    def fake_get(url, params=None, retries=4):
        if on_call:
            on_call()
        if mode == "outage":
            raise ConnectionError("simulated network fault (F-MV-5)")
        if url.endswith(OM.EP_EXCHANGE_INFO):
            rows = [{"symbol": x, "contractType": "PERPETUAL", "status": "TRADING",
                     "quoteAsset": "USDT"} for x in syms]
            rows.append({"symbol": "STOCKUSDT", "contractType": "TRADIFI_PERPETUAL",
                         "status": "TRADING", "quoteAsset": "USDT"})
            return _FakeResp({"symbols": rows})
        if url.endswith(OM.EP_TICKER_24H):
            return _FakeResp([{"symbol": x, "priceChangePercent": str(i - 100),
                               "lastPrice": "1.5", "closeTime": OM.now_ms()}
                              for i, x in enumerate(syms)])
        if url.endswith(OM.EP_KLINES):
            started.append(params["symbol"])             # list.append is atomic
            i = int(params["symbol"][1:4])
            if mode == "weekly-outage" and i % 10 == 0:
                raise RuntimeError("failed after 4 attempts: simulated (F-MV-5)")
            if mode == "dead-sweep":
                raise RuntimeError("failed after 4 attempts: simulated dead wire (F-MV-5)")
            if mode == "hang":
                time.sleep(HANG_S)
                raise RuntimeError("failed after 4 attempts: simulated hang (F-MV-5)")
            d0 = OM.day_open(OM.now_ms())
            return _FakeResp([[d0 - (7 - j) * OM.DAY_MS, "1", "1", "1",
                               str(100 + (i if j == 7 else 0))] for j in range(8)])
        raise AssertionError(f"the organ called an endpoint the stub does not know: {url}")
    fake_get.klines_calls = started
    return fake_get


def _plant_fault(fault: str) -> None:
    """The two faults of the FIRST-BUILD organ, put back ONE AT A TIME (break legs only).
    In-process callers restore OM afterwards; an F-MV-6 child simply exits."""
    if fault == "no-placeholder":
        # first build: nothing was written until the END of main()
        def late_writer(doc):
            if doc.get("in_flight"):
                return OM.doc_path(doc["date"]), "", 0
            return _REAL_WRITE_DOC(doc)
        OM.write_doc = late_writer
    elif fault == "no-early-stop":
        # first build: the sweep ran every symbol through its full backoff regardless
        OM.floor_unreachable = lambda total, failed: False
    elif fault != "none":
        raise ValueError(f"unknown fault {fault!r}")


def _plant_earlier_success(p: Path) -> None:
    """AN EARLIER SUCCESS FROM THE SAME DAY — the thing that must not survive."""
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({"status": "OK", "date": OM.local_date(), "planted": True,
                             "fetched_utc": "2026-09-21T09:00:00+00:00",
                             "overnight": [{"symbol": "STALEUSDT", "pct": 99.0,
                                            "last_price": 1.0}]}))


def _stale_faults(doc: dict, who: str) -> list[str]:
    """What EVERY document left behind by a run that did not succeed must satisfy —
    shared by F-MV-5 (the run lives to write it) and F-MV-6 (it may not)."""
    if doc.get("status") == "OK" and doc.get("planted"):
        return [f"{who}: the earlier success SURVIVED — today's file still says status OK "
                f"and still carries {doc.get('overnight', [])[:1]}: STALE NUMBERS a reader "
                f"would print"]
    if doc.get("status") != "FAIL":
        # said once and alone: what follows only makes sense of a FAIL document
        return [f"{who}: status is {doc.get('status')!r}, not FAIL "
                f"(universe {doc.get('universe_count')}, "
                f"{len(doc.get('overnight', []))} overnight row(s))"]
    bad = []
    if doc.get("planted") or any(r.get("symbol") == "STALEUSDT"
                                 for r in doc.get("overnight", [])):
        bad.append(f"{who}: the earlier success SURVIVED — stale numbers")
    if not doc.get("fail_reasons"):
        bad.append(f"{who}: no fail reason was recorded")
    full = [k for k in ("overnight", "overnight_top", "overnight_null",
                        "weekly", "weekly_top", "weekly_null") if doc.get(k) != []]
    if full:
        bad.append(f"{who}: a non-OK document still carries rows in {full}")
    if doc.get("date") != OM.local_date():
        bad.append(f"{who}: the document is dated {doc.get('date')!r}, not today")
    bad += [f"{who}: {x}" for x in _shape_faults(doc)]
    return bad


# mode -> (what the fail reason must name, ceiling on weekly calls STARTED)
def _mode_expectations(mode: str) -> tuple[str, int]:
    return {
        "healthy": ("", STUB_N),
        "outage": ("exchangeInfo", 0),
        "crash": ("ZeroDivisionError", 0),
        # 1 in 10 fails, in universe order: the stop comes at the 11th failure. How
        # many SUCCESSES other workers start meanwhile is a thread race, so no
        # ceiling tighter than the universe is claimed; the count is reported.
        "weekly-outage": ("WEEKLY_SUCCESS_FLOOR", STUB_N),
        # Every call fails and every failure is counted by the worker that made it
        # BEFORE it may take another symbol: no symbol is taken once the floor is
        # unreachable, so at most (tolerated failures + KLINE_WORKERS) calls start.
        "dead-sweep": ("STOPPED EARLY", _tolerated_failures(STUB_N) + OM.KLINE_WORKERS),
        # Each worker takes one symbol and blocks; nobody takes a second.
        "hang": ("RUN_DEADLINE_S", OM.KLINE_WORKERS),
    }[mode]


def _failure_run(mode: str, fault: str = "none") -> tuple[bool, str]:
    """ONE run of the real main() against a stub wire; the SAME assertions every mode."""
    who = mode if fault == "none" else f"{mode} + {fault}"
    saved = (OM._get, OM.MOVERS_DIR, OM.fetch, OM.floor_unreachable, OM.write_doc,
             OM.RUN_DEADLINE_S)
    seen: list[dict] = []
    look = threading.Lock()
    with tempfile.TemporaryDirectory(prefix="oracle-movers-fail-") as td:
        OM.MOVERS_DIR = Path(td)
        p = OM.doc_path(OM.local_date())
        _plant_earlier_success(p)

        def on_disk_at_first_touch() -> None:
            # What a reader would find at the instant the run FIRST reaches for the
            # wire (or, in crash mode, enters fetch()). It must already be FAIL.
            with look:
                if not seen:
                    seen.append(json.loads(p.read_text()))

        stub = _stub_get(mode, on_call=on_disk_at_first_touch)
        if mode == "crash":
            def boom(log=print, started=None):
                on_disk_at_first_touch()
                raise ZeroDivisionError("simulated crash outside the guarded fetches")
            OM.fetch = boom
        else:
            OM._get = stub
        if mode == "hang":
            OM.RUN_DEADLINE_S = HANG_DEADLINE_S
        _plant_fault(fault)
        t0 = time.monotonic()
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                rc = OM.main([])
        finally:
            (OM._get, OM.MOVERS_DIR, OM.fetch, OM.floor_unreachable, OM.write_doc,
             OM.RUN_DEADLINE_S) = saved
        took = time.monotonic() - t0
        doc = json.loads(p.read_text())
        litter = sorted(f.name for f in Path(td).iterdir() if f.name != p.name)

    bad = _stale_faults(doc, who)
    if bad:
        return False, "; ".join(bad) + f" (rc {rc})"
    expect, ceiling = _mode_expectations(mode)
    calls = len(stub.klines_calls)
    if rc != 1:
        bad.append(f"{who}: status FAIL but main() returned {rc}, not 1")
    if doc.get("in_flight") is not False:
        bad.append(f"{who}: the run lived to write its result, yet the file is still the "
                   f"in_flight placeholder")
    if expect not in " ".join(doc["fail_reasons"]):
        bad.append(f"{who}: fail_reasons {doc['fail_reasons']} do not name {expect!r}")
    first = seen[0] if seen else {}
    if not (first.get("status") == "FAIL" and first.get("in_flight") is True
            and not first.get("planted")):
        bad.append(f"{who}: at the run's FIRST touch of the wire today's file was "
                   f"status {first.get('status')!r} / in_flight {first.get('in_flight')!r} / "
                   f"planted {first.get('planted')!r} — the placeholder was not there yet, "
                   f"so a kill at that instant leaves the earlier success printable")
    if calls > ceiling:
        bad.append(f"{who}: {calls} weekly call(s) were STARTED on a wire where the floor "
                   f"tolerates {_tolerated_failures(STUB_N)} failure(s) of {STUB_N} — the "
                   f"sweep must stop within {ceiling}")
    if took > IN_PROCESS_BOUND_S:
        bad.append(f"{who}: main() took {took:.1f} s against a stub wire "
                   f"(bound {IN_PROCESS_BOUND_S} s)")
    if litter:
        bad.append(f"{who}: the atomic write left litter behind: {litter}")
    if bad:
        return False, "; ".join(bad)
    return True, (f"{who}: FAIL, rc 1, placeholder on disk before the first call, "
                  f"{calls} weekly call(s) started (ceiling {ceiling}), {took:.1f} s — "
                  f"{doc['fail_reasons']}")


def _failure_path(modes) -> tuple[bool, str]:
    got = [_failure_run(m) for m in modes]
    bad = [d for ok, d in got if not ok]
    if bad:
        return False, "; ".join(bad)
    return True, ("against a STUB wire (no real call), every failure mode wrote TODAY's "
                  "json as status FAIL with EMPTY tables and ALL DOC_KEYS over an earlier "
                  "same-day success, had the in_flight placeholder on disk BEFORE its first "
                  "call, left no tmp litter, and main() returned 1 — "
                  + " | ".join(d for _, d in got))


def f_mv_5() -> None:
    # Plant 1 points the SAME assertions at a HEALTHY wire: the organ answers OK
    # with 200 rows, which is right for the organ and therefore fails the
    # failure-path assertions for a real reason — the redness is the organ's
    # verdict, not the wrapper's arithmetic (the F-TU-6 lesson). Plants 2 and 3
    # put the two faults of the FIRST-BUILD organ back, one at a time.
    prove("F-MV-5", "FAILURE PATH — a dead wire writes FAIL over success, never stale",
          lambda: _every_plant_red([
              ("a healthy wire", lambda: _failure_run("healthy")),
              ("a dead sweep with the early stop taken out",
               lambda: _failure_run("dead-sweep", fault="no-early-stop")),
              ("an outage with the placeholder taken out",
               lambda: _failure_run("outage", fault="no-placeholder")),
          ]),
          lambda: _failure_path(("outage", "weekly-outage", "dead-sweep", "hang", "crash")))


# ══════════════════════════════════ F-MV-6 · A RUN THAT DOES NOT LIVE TO SEE ITS FAILURE

# The child: the REAL organ and the REAL engine.data._get. Only requests.get is
# replaced (in the child's own process), so _get's own retry loop and its own
# 1.5 / 3 / 4.5 / 6 s backoff run for real — the thing F-MV-5's stub skips, and
# the thing that made the first build's dead-wire run outlive the wrapper's timeout.
# exchangeInfo and the ticker answer; every klines call is refused at once: the
# wire dies AFTER the ticker call, the one case the success floor exists for.
_CHILD = r"""
import sys
from pathlib import Path
sys.path[:0] = [sys.argv[1], sys.argv[1] + '/scripts']
import requests
import engine.data as ED
import oracle_movers as OM
import oracle_movers_fixtures as MF
out_dir, n, fault = Path(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
wire = MF._stub_get('healthy', n=n)
def dead_after_the_ticker(url, params=None, timeout=None, **kw):
    if url.endswith(OM.EP_KLINES):
        raise requests.ConnectionError('simulated: the wire died mid-sweep (F-MV-6)')
    return wire(url, params)
ED.requests.get = dead_after_the_ticker
OM.MOVERS_DIR = out_dir
MF._plant_fault(fault)
raise SystemExit(OM.main([]))
"""

# engine.data._get on a connection refused AT ONCE: 4 attempts, then 1.5 + 3 +
# 4.5 + 6 s of sleep (it sleeps after the last attempt too). Read from
# engine/data.py 2026-09-21 and confirmed by the verifier's measurement (200
# symbols, 8 workers, no early stop: 375.5 s = 25 batches x 15 s).
GET_DEAD_CALL_S = 15.0
# Interpreter start + pandas import + two stub calls + thread scheduling.
DEAD_WIRE_SLACK_S = 20.0
KILL_AFTER_S = 1.0          # into the sweep: every worker is inside its first backoff
CHILD_START_BOUND_S = 60.0  # for the child to reach the sweep at all
SIGINT_EXIT_BOUND_S = 20.0  # for an interrupted child to write its FAIL and be gone
FALLBACK_UNIVERSE_N = 528   # the real universe of 2026-09-21, if no json says otherwise
BREAK_UNIVERSE_N = 40       # the no-early-stop plant: 5 batches = 75 s unstopped, 15 s stopped


_SIGNALS = {"SIGKILL": signal.SIGKILL, "SIGTERM": signal.SIGTERM, "SIGINT": signal.SIGINT}


def _dead_wire_bound(n: int) -> tuple[float, int]:
    """Seconds a dead-wire run over n symbols may take, and the batches that is."""
    batches = math.ceil((_tolerated_failures(n) + 1) / OM.KLINE_WORKERS)
    return batches * GET_DEAD_CALL_S + DEAD_WIRE_SLACK_S, batches


def _wrapper_movers_timeout() -> int | None:
    """oracle_wrapper.ONDEMAND_REGISTER['MOVERS_TIMEOUT_S']['value'], read by AST —
    the wrapper is not imported (it is another step's file, and it shells out)."""
    try:
        tree = ast.parse((ROOT / "scripts" / "oracle_wrapper.py").read_text())
    except Exception:
        return None
    for n in ast.walk(tree):
        if not isinstance(n, ast.Dict):
            continue
        for k, v in zip(n.keys, n.values):
            if isinstance(k, ast.Constant) and k.value == "MOVERS_TIMEOUT_S" \
                    and isinstance(v, ast.Dict):
                for kk, vv in zip(v.keys, v.values):
                    if isinstance(kk, ast.Constant) and kk.value == "value":
                        try:
                            return int(ast.literal_eval(vv))
                        except Exception:
                            return None
    return None


def _real_universe_n() -> int:
    _, doc = newest_doc()
    n = (doc or {}).get("universe_count") or 0
    return n if n >= UNIVERSE_FLOOR else FALLBACK_UNIVERSE_N


def _killed_run(how: str, fault: str = "none", n: int = STUB_N) -> tuple[bool, str]:
    """ONE child run over a planted earlier success, ended the way `how` says:

      SIGKILL    killed KILL_AFTER_S into the sweep — subprocess.run(timeout=)'s
                 own mechanism, i.e. what the on-demand wrapper does at
                 MOVERS_TIMEOUT_S
      SIGTERM    the same instant, the polite way (launchd, `kill`, a shutdown):
                 Python's default disposition dies on the spot, no handler runs
      SIGINT     interrupted KILL_AFTER_S into the sweep — the operator's Ctrl-C
      dead-wire  left alone, against the clock: _dead_wire_bound(n)

    and then the SAME question every time: what does a reader find on disk?
    """
    who = f"{how}, {n} symbols" + ("" if fault == "none" else f" + {fault}")
    bound, batches = _dead_wire_bound(n)
    with tempfile.TemporaryDirectory(prefix="oracle-movers-kill-") as td:
        p = Path(td) / f"movers_{OM.local_date()}.json"
        _plant_earlier_success(p)
        t0 = time.monotonic()
        ch = subprocess.Popen([sys.executable, "-u", "-c", _CHILD, str(ROOT), td, str(n), fault],
                              cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                              text=True)
        lines: list[str] = []
        pump = threading.Thread(target=lambda: lines.extend(ch.stdout), daemon=True)
        pump.start()
        timed_out = False
        try:
            if how in _SIGNALS:
                # The ticker line is the organ's own word that the sweep comes next.
                while not any("overnight" in ln for ln in lines):
                    if ch.poll() is not None or time.monotonic() - t0 > CHILD_START_BOUND_S:
                        return False, (f"{who}: the child never reached the weekly sweep "
                                       f"(rc {ch.poll()}): {''.join(lines)[-300:]}")
                    time.sleep(0.05)
                time.sleep(KILL_AFTER_S)
                if ch.poll() is not None:
                    return False, f"{who}: the child had already exited (rc {ch.returncode})"
                ch.send_signal(_SIGNALS[how])
                ch.wait(timeout=SIGINT_EXIT_BOUND_S)
            else:
                ch.wait(timeout=bound)
        except subprocess.TimeoutExpired:
            timed_out = True
        finally:
            if ch.poll() is None:
                ch.kill()
                ch.wait()
        took = time.monotonic() - t0
        pump.join(timeout=5)
        doc = json.loads(p.read_text())
        litter = sorted(f.name for f in Path(td).iterdir() if f.name != p.name)

    rc = ch.returncode
    bad = _stale_faults(doc, who)
    if timed_out and how == "dead-wire":
        bad.append(f"{who}: STILL SWEEPING after {bound:.0f} s — the floor tolerates "
                   f"{_tolerated_failures(n)} failure(s) of {n}, so {batches} batch(es) of "
                   f"{OM.KLINE_WORKERS} dead calls x {GET_DEAD_CALL_S:.0f} s of backoff is "
                   f"all a dead wire is worth; unstopped it is "
                   f"{math.ceil(n / OM.KLINE_WORKERS)} batches = "
                   f"{math.ceil(n / OM.KLINE_WORKERS) * GET_DEAD_CALL_S:.0f} s")
    elif timed_out:
        bad.append(f"{who}: the child was still alive {SIGINT_EXIT_BOUND_S:.0f} s after the signal")
    if bad:
        return False, "; ".join(bad) + f" (rc {rc}, {took:.1f} s)"

    reasons = " ".join(doc["fail_reasons"])
    if how in ("SIGKILL", "SIGTERM"):
        want = [(rc == -_SIGNALS[how], f"rc {rc} is not {-_SIGNALS[how]}: the child did not "
                                       f"die of the signal"),
                (doc["in_flight"] is True, "the file is not the in_flight placeholder — "
                                           "something else wrote after the kill?"),
                ("NEVER FINISHED" in reasons, f"fail_reasons do not say so: {reasons[:120]}")]
    elif how == "SIGINT":
        want = [(rc not in (0, None), f"rc {rc}: an interrupted run must not exit 0"),
                (doc["in_flight"] is False, "the interrupt left the placeholder instead of "
                                            "writing what happened"),
                ("KeyboardInterrupt" in reasons, f"fail_reasons do not name the interrupt: "
                                                 f"{reasons[:120]}")]
    else:
        wrapper_s = _wrapper_movers_timeout()
        want = [(rc == 1, f"rc {rc}, not 1"),
                (doc["in_flight"] is False, "the file is still the in_flight placeholder"),
                ("STOPPED EARLY" in reasons, f"fail_reasons do not say the sweep stopped "
                                             f"early: {reasons[:120]}"),
                (doc["weekly_fetch"]["not_fetched"] > 0, "not_fetched is 0: every symbol was "
                                                         "swept on a dead wire"),
                (wrapper_s is None or bound < OM.RUN_DEADLINE_S < wrapper_s,
                 f"the clocks are out of order: dead-wire bound {bound:.0f} s, "
                 f"RUN_DEADLINE_S {OM.RUN_DEADLINE_S}, wrapper MOVERS_TIMEOUT_S {wrapper_s}")]
    bad = [f"{who}: {msg}" for ok, msg in want if not ok]
    if litter:
        bad.append(f"{who}: litter beside the document: {litter}")
    if bad:
        return False, "; ".join(bad)
    if how == "dead-wire":
        wf = doc["weekly_fetch"]
        return True, (f"{who}: the REAL _get's backoff ran and the run wrote FAIL by itself in "
                      f"{took:.1f} s (runtime_seconds {doc['runtime_seconds']}; bound "
                      f"{bound:.0f} s = {batches} batch(es) x {GET_DEAD_CALL_S:.0f} s + "
                      f"{DEAD_WIRE_SLACK_S:.0f} s; unstopped "
                      f"{math.ceil(n / OM.KLINE_WORKERS) * GET_DEAD_CALL_S:.0f} s), rc 1, "
                      f"{wf['failed']} failed + {wf['not_fetched']} not fetched of "
                      f"{wf['attempted']}; clocks in order: {bound:.0f} s < RUN_DEADLINE_S "
                      f"{OM.RUN_DEADLINE_S:.0f} s < wrapper MOVERS_TIMEOUT_S "
                      f"{_wrapper_movers_timeout()} s (read by AST)")
    return True, (f"{who}: rc {rc} after {took:.1f} s; on disk: status FAIL, in_flight "
                  f"{doc['in_flight']}, EMPTY tables, all DOC_KEYS, the planted success GONE")


def f_mv_6() -> None:
    n_real = _real_universe_n()

    def real() -> tuple[bool, str]:
        got = [_killed_run("SIGKILL"), _killed_run("SIGTERM"), _killed_run("SIGINT"),
               _killed_run("dead-wire", n=n_real)]
        bad = [d for ok, d in got if not ok]
        if bad:
            return False, "; ".join(bad)
        return True, ("the REAL organ in a child process, the REAL engine.data._get and its "
                      "backoff, the wire dying after the ticker call, an earlier same-day "
                      "SUCCESS planted on disk — " + " | ".join(d for _, d in got))

    # The break is THE FIRST BUILD OF THIS ORGAN, put back one fault at a time: the
    # document written only at the END of main(), and the sweep that never stops.
    prove("F-MV-6", "A RUN THAT DOES NOT LIVE TO SEE ITS FAILURE — killed, interrupted, dead wire",
          lambda: _every_plant_red([
              ("SIGKILL with the placeholder taken out (the first build)",
               lambda: _killed_run("SIGKILL", fault="no-placeholder")),
              ("a dead wire with the early stop taken out (the first build)",
               lambda: _killed_run("dead-wire", fault="no-early-stop", n=BREAK_UNIVERSE_N)),
          ]),
          real)


# ══════════════════════════════════ F-MV-7 · --dry-run FETCHES NOTHING, WRITES NOTHING

def _dry_run(argv: list[str]) -> tuple[bool, str]:
    """main(argv) with the wire replaced by a COUNTING stub and the output dir
    redirected OUTSIDE the repo — where the first build's --dry-run died with a ValueError
    (a bare relative_to(ROOT)); the fetch path had the guard, the dry path did not."""
    saved = (OM._get, OM.MOVERS_DIR)
    calls: list[int] = []
    buf = io.StringIO()
    with tempfile.TemporaryDirectory(prefix="oracle-movers-dry-") as td:
        OM.MOVERS_DIR = Path(td) / "never-created"
        OM._get = _stub_get("healthy", on_call=lambda: calls.append(1))
        try:
            with contextlib.redirect_stdout(buf):
                rc = OM.main(argv)
        except Exception as e:
            return False, f"main({argv}) raised {e.__class__.__name__}: {e}"
        finally:
            OM._get, OM.MOVERS_DIR = saved
        made = sorted(f.relative_to(td).as_posix() for f in Path(td).rglob("*"))
    out = buf.getvalue()
    bad = []
    if rc != 0:
        bad.append(f"rc {rc}")
    if calls:
        bad.append(f"{len(calls)} call(s) reached the wire")
    if made:
        bad.append(f"it wrote {made[:3]}")
    unruled = [k for k, row in OM.REGISTER.items() if not row["ruled"]]
    silent = [k for k in OM.REGISTER if f" {k} = " not in out]
    if silent:
        bad.append(f"REGISTER row(s) not printed: {silent}")
    if out.count("[VETO] ") < len(unruled):
        bad.append(f"{out.count('[VETO] ')} [VETO] chip(s) printed for {len(unruled)} unruled row(s)")
    quiet = [e for e in (OM.EP_EXCHANGE_INFO, OM.EP_TICKER_24H, OM.EP_KLINES) if e not in out]
    if quiet:
        bad.append(f"endpoint(s) not printed: {quiet}")
    if bad:
        return False, f"main({argv}): " + "; ".join(bad)
    return True, (f"main({argv}) with the output dir redirected outside the repo: rc 0, 0 calls "
                  f"on a counting stub wire, nothing created on disk; all {len(OM.REGISTER)} "
                  f"REGISTER rows printed, the {len(unruled)} unruled ones chipped [VETO] "
                  f"{unruled}; the three endpoints printed")


def f_mv_7() -> None:
    # The break is an ordinary run held to the dry run's promises: it calls the
    # wire and it writes — the two things a dry run must not do.
    prove("F-MV-7", "--dry-run — prints the REGISTER and the endpoints, fetches and writes nothing",
          lambda: _dry_run([]), lambda: _dry_run(["--dry-run"]))


# ══════════════════════════════════════════════════════════════════ MAIN

def main() -> int:
    fixtures = (f_mv_1, f_mv_2, f_mv_3, f_mv_4, f_mv_5, f_mv_6, f_mv_7)
    print("=" * 78)
    print(f"ORACLE MOVERS FIXTURES — {datetime.now(timezone.utc).isoformat()[:19]}Z")
    print(f"  organ       {ORGAN_SRC.relative_to(ROOT)}  sha256 {OM.sha256_file(ORGAN_SRC)}")
    print(f"  movers dir  {OM.MOVERS_DIR.relative_to(ROOT)}")
    print(f"  kline cache {cache_dir()}")
    print("=" * 78)
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
