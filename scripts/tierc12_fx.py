#!/usr/bin/env python
"""TIER-C12 · THE FIXTURE HARNESS [LEANS L-0.14] — one harness for every scripts/tierc12_*_fixtures.py.

A COPY, never an import, of the harness of record in scripts/tierc11_closure_fixtures.py: `say`,
`clock`, `prove`, `plants` and `file_transcript` below are that file's functions, AST-identical
(F-FX-MIRROR holds them by `ast.dump`; O-3: importing TC11's file would arm TC11's hooks).  STDLIB
ONLY: the frame-taking helper legs receive the shim `E`, `pandas` and their directory, grid or book
as ARGUMENTS from the calling suite, so this module imports no tierc12_env, numpy, pandas, lineage
or analytics module — that is what lets the pre-substrate suites use it and what earns its place
among the process tools (L-0.17).  It holds NO subprocess site, no exec / eval / compile and no
dynamic import (L-0.22: a non-fixture tierc12 module): an F-DET twin is launched by the calling
SUITE and handed to `det_twins`.

THE LEG LAW [L-0.14 A].  A leg is ONE `prove` call and ONE transcript block; the block id is the
`fid` handed to `prove`.  The BREAK leg runs first and must go RED, or the leg is VOID and counts
RED; a break leg that raises proves nothing (VOID).  A break leg is `plants(rows)`, rows =
(name, expected detector substring, thunk -> findings), judged ONE AT A TIME: CAUGHT only if a
finding NAMES THE INTENDED DETECTOR; no finding = the plant passed (VOID); a crash = a FIXTURE
DEFECT (VOID); a SystemExit is a finding carrying its own text.  Every block prints
    <block id> — <title>
      [BREAK] FAILS IF: …
      [BREAK] deliberate violation -> RED (correct): …
      [REAL]  FAILS IF: …
      [PASS|FAIL] <block id>: …

BLOCK IDS [L-0.14 B] = `<FID>` or `<FID> [<qualifier>]`; FID matches F-[A-Z0-9]+(-[A-Z0-9]+)*;
<qualifier> = <leg>, <instance> or `<leg> · <instance>`; no bracket inside a qualifier.

LEG STATES [L-0.14 C; the resume paste's "tier-e-never-halts"].
  PASS · FAIL      from `prove` (a VOID fixture counts FAIL).
  NOT RUN          `not_run(fid, title, reason)`, outside `prove`: the header and
                   `  [NOT RUN] <fid>: <reason>`.  Never PASS.  Lawful ONLY for a block id on
                   NOT_RUN_FIDS_T [seam 3]; any other id handed to `not_run` reads FAIL.
  CLOSED-NO-BOOK   a PASS, not a state: the real leg of a real-book leg whose registration is
                   closed by precondition prints `CLOSED-NO-BOOK <id>` and asserts STATUS.json
                   (`closed_real`; BREAK plants `closed_plants`, detector CLOSED-STATUS) [OD-17].
  NOT BUILT        `not_built(fid, title, reason)`: the header and `  [NOT BUILT] <fid>: <reason>`
                   — the F-GRID / F-KEY leg of a Tier-E table that could not be built as
                   specified.  Never PASS, never RED; the stage continues.  Lawful only for the
                   FIDs of NOT_BUILT_FIDS_T; any other reads FAIL.
THE TALLY is `  N GREEN, M RED, K NOT RUN` (C's form, unchanged); `legs_total` = N + M + K.  NOT
BUILT blocks are counted BESIDE it — one more line `  J NOT BUILT`, printed only when J > 0, and
`summary()["legs_not_built"]` — so a Tier-E table that was not built neither passes nor stops a gate.

TRANSCRIPTS [L-0.14 I].  First line `as_of_last_closed_4h: <pin ISO>`; at a record before TC12-D
the fixed pair `as_of_last_closed_4h: (pre-substrate stage)` / `substrate: none` (L-0.10 point 11);
then the banner and `seed … · substrate … · pin …`.  No clock, no temp path, no absolute home path,
no source line number.  NO-CLOBBER: an absent transcript without --refile-transcript is a finding
and nothing is written; identical bytes are silent; different bytes without the flag go to
<stem>_rerun.txt, the record untouched, RED; a leg-filtered run writes <stem>_partial.txt.  Exit 1
on any RED, VOID or transcript finding.

PUBLIC API (the other builders code against exactly this).  A suite either calls `header`, then
`prove` / `not_run` / `not_built` once per leg, then `finish`; or hands its rows to `run_suite`.
  state        LINES PASSED FAILED NOT_RUN NOT_BUILT (module lists; read them through `summary()`)
  the mirror   say(line="") · clock(line) · prove(fid, title, break_if, real_if, break_leg,
               real_leg) · plants(rows) -> (ok, why) · file_transcript(out, body, refile) -> findings
  states       not_run(fid, title, reason) · not_built(fid, title, reason)
               closed_status_findings(status, reg_id) -> findings · closed_plants(status, reg_id)
               -> rows · closed_real(status_path, reg_id) -> (ok, why)
  block ids    block_id(fid, leg=None, instance=None) -> str · split_block(block) -> (fid, qual)
               block_findings(block) -> findings · fid_of(block) -> str · blocks() -> [block id]
  the protocol opt(args, prefix, default=None) · picks(args) · header(banner, *, seed,
               substrate=None, as_of_iso=None, pin=None, typed=()) · run_leg(row) · tally()
               summary() -> dict · transcript_bytes() -> bytes · finish(root, transcript, args,
               t0=None) -> exit code · run_suite(*, args, root, transcript, banner, seed,
               fixtures, substrate=None, as_of_iso=None, pin=None, typed=()) -> exit code
               reset() · capture() (context manager: an inner session that leaves the outer alone)
  randomness   suite_tag(stem) -> str · stream_seed(seed, tag, block) -> [seed, crc32]
               stream(np, seed, tag, block) -> numpy Generator [L-0.14 F]
  hand sample  hand_sample(rows, *, key, k, categories=(), contract_named=(), rule="",
               n_asserted=None, rng=None) -> dict [L-0.14 G, the one law]
  text         sha_bytes(b) · rel(p, root=ROOT) · func_dump(text, name)
               literal_from_text(text, name, key=None)
  F-GRID       grid_cells(axes) · grid_count(axes) · grid_findings(TP, declared, written, *, …)
               grid_printed_findings(text, grid_id, cells) · grid_pointer_findings(grid_id,
               pointer, doc_bytes, cells) [L-0.15]
  F-COLLAR     collar_table_findings(name, df, *, collar_cols, ci_readings, registered, …)
               collar_leaf_findings(name, obj, …) · collar_doc_findings(name, text, *,
               registered_marker_ok, …) [L-0.16]
  F-KEY        key_findings(name, df, key, required=(), null_iff=None, *, as_of_cols=(),
               columns=None) · stamp_findings(name, df, stamp) · key_dir_findings(E, pd, root,
               specs, *, …) [L-0.21]
  F-DET        det_seeds(seed) · det_dir(directory, stage, hashseed) · det_twins(launch, directory,
               stage, seed) · read_dir(d) · det_file_set(typed, manifest, …) · clock_findings(files,
               *, pd=None, …) · det_findings(twins, canon, file_set, *, E=None, pd=None, …)
               det_dir_findings(E, pd, twins, canonical_dir, file_set, *, …) [L-0.20]
  L-V's legs   trav_ast_findings(module, src, *, …) [F-TRAV a] · trav_book_findings(book, t_values,
               filed_source, value, source) [F-TRAV e] · va_pins_e_findings(reg_id, declared,
               builder_src, *, va_cols, …) [F-VA-PINS e]
Every `*_findings` function returns a list of strings, each beginning with its DETECTOR NAME (the
substring a `plants` row names); an empty list is GREEN.

BANNED [L-0.14]: self-comparison; one example where cardinality was possible; a check whose claim
is not the design's claim.  A sabotage is planted INSIDE production (a shadow copy of the source or
a monkeypatched object in the production call path), never in the comparator.

Run (the self-test: every leg state and a planted mutation per law; the transcript goes to stdout,
nothing is written to the tree):
      ~/venvs/naiad/bin/python -B /Users/luis/Naiad/scripts/tierc12_fx.py
Exit 0 = every self-test leg GREEN, every break RED · 1 = a RED or VOID leg.
"""
from __future__ import annotations

import ast
import binascii
import contextlib
import hashlib
import io
import itertools
import json
import re
import shutil
import sys
import tempfile
import time
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# ── THE SESSION: one transcript per process ──
LINES: list[str] = []
PASSED: list[str] = []
FAILED: list[str] = []
NOT_RUN: list[str] = []
NOT_BUILT: list[str] = []
_STATE = ("LINES", "PASSED", "FAILED", "NOT_RUN", "NOT_BUILT")
_TMP_RX = re.compile(r"(/private)?/(var/folders|tmp)/[^\s'\"]+")
_LINE_RX = re.compile(r"\bline \d+")

# ── FIXTURE-TYPED TABLES of the harness (the commission; a second object, never production's own) ──
MIRRORED_T = ("say", "clock", "prove", "plants", "file_transcript")
# [seam 3] the block ids that may ever print NOT RUN: L-D's F-MIRROR (the drive unreachable) and
# the body-file leg of F-TOLL [data] (a recorded fee-page body whose file is absent, L-D leg (d)).
NOT_RUN_FIDS_T = ("F-MIRROR", "F-TOLL [data d]")
# the resume paste, "tier-e-never-halts": the FIDs whose leg may print NOT BUILT.
NOT_BUILT_FIDS_T = ("F-GRID", "F-KEY")
PRE_SUBSTRATE_AS_OF = "as_of_last_closed_4h: (pre-substrate stage)"      # L-0.10 point 11
PRE_SUBSTRATE_LINE = "substrate: none"
RULE = "=============================================================================="
STATUS_CLOSED_T = "CLOSED_BY_PRECONDITION"
STATUS_BUILT_T = "BUILT"
CELL_SEP = "¦"                                                           # L-0.15: `axis:level¦axis:level`
QUAL_SEP = " · "
COLLAR_LINE = "TIER-E — a SELECTION, not a result — gates nothing"       # L-0.16, in documents
COLLAR_DOC_WINDOW_T = 3                                                  # "within the three lines above its header"
FORBIDDEN_NAME_RX = re.compile(r"verdict|clears|spent_test", re.IGNORECASE)
REGISTERED_MARKER_RX = re.compile(r"<!-- registered: (?P<id>\S+) -->")
GRID_MARKER_RX = re.compile(r"<!-- grid: (?P<id>\S+) cells=(?P<n>\d+) -->")
# the fixture-typed copy of TC11-X's CLOCK_NAME_RX (x_rec/scripts/tc11x_books_fixtures.py:203-204):
# a worker count or a load average counts as a clock [L-0.20].
CLOCK_NAME_RX = re.compile(r"(elapsed|wall_clock|perf_counter|_at_(?:x_)?run|run_started|"
                           r"load_avg|loadavg|n_workers|worker_count)")
HASHSEED_FIRST_T = "1"                                                   # TC11 L-F.1's first twin
# F-TRAV [a]: what counts as a time-stop or traverse NAME, and as the 5m count's name.  Defaults;
# the calling suite hands its own typed patterns where its builder names them otherwise.
TRAV_NAME_RX = re.compile(r"^(T|T\d\w*|T_\w+|\w*time_stop\w*|\w*traverse\w*)$")
TRAV_5M_RX = re.compile(r"5m|^T5$")
VA_1W_PREFIX_T = "1w_"                                                   # F-VA-PINS [e]
FID_RX = re.compile(r"F-[A-Z0-9]+(?:-[A-Z0-9]+)*")
BLOCK_RX = re.compile(r"(?P<fid>F-[A-Z0-9]+(?:-[A-Z0-9]+)*)(?: \[(?P<q>[^\[\]]+)\])?")


# ═══════════════════════════════════════════ THE MIRROR — scripts/tierc11_closure_fixtures.py, AST-identical
def say(line: str = "") -> None:            # deterministic -> transcript
    line = _TMP_RX.sub("<tmp>", line)
    print(line)
    LINES.append(line)


def clock(line: str) -> None:               # wall clock, temp paths -> stdout ONLY
    print(f"  [clock · stdout only] {line}")


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def prove(fid: str, title: str, break_if: str, real_if: str, break_leg, real_leg) -> None:
    """Break first; it must go RED (ok False) or the fixture is VOID."""
    say(f"\n{fid} — {title}")
    say(f"  [BREAK] FAILS IF: {break_if}")
    try:
        b_ok, b_why = break_leg()
    except Exception as e:                  # a break leg that errors proved nothing
        b_ok, b_why = True, f"break leg RAISED {type(e).__name__}: {e}"
    say(f"  [BREAK] deliberate violation -> "
        f"{'RED (correct)' if not b_ok else 'GREEN (FIXTURE IS VOID)'}: {b_why}")
    say(f"  [REAL]  FAILS IF: {real_if}")
    try:
        r_ok, r_why = real_leg()
    except Exception as e:                  # a real leg that errors is a FAIL
        r_ok, r_why = False, f"raised {type(e).__name__}: {e}"
    say(f"  [{'PASS' if r_ok else 'FAIL'}] {fid}: {r_why}")
    if b_ok:
        FAILED.append(f"{fid} (break leg did not go RED — fixture proves nothing)")
    elif not r_ok:
        FAILED.append(fid)
    else:
        PASSED.append(fid)


def plants(rows) -> tuple[bool, str]:
    """rows = (name, expected detector substring, thunk -> list of findings).  Judged ONE AT A
    TIME.  CAUGHT only if a finding names the intended detector.  No finding = the plant PASSED
    (VOID); a finding without the substring = the WRONG detector (VOID); a crash = a FIXTURE
    DEFECT (VOID).  A HALT is a finding (it carries its own text)."""
    passed, wrong, caught, crashed = [], [], [], []
    for name, want, thunk in rows:
        try:
            found = thunk()
        except SystemExit as e:
            found = [str(e) if str(e).startswith("HALT") else f"HALT: {e}"]
        except Exception as e:
            crashed.append(f"{name} -> RAISED {type(e).__name__}: {e}")
            continue
        if not found:
            passed.append(name)
        elif not any(want in str(f) for f in found):
            wrong.append(f"{name} -> {str(found[0])[:160]} (wanted {want!r})")
        else:
            hit = next(str(f) for f in found if want in str(f))
            i = hit.index(want)
            shown = hit[:170] if i + len(want) <= 170 else (hit[:60] + " … " + hit[i:i + 150])
            shown = _LINE_RX.sub("line #", shown)   # a planted line's number moves with any edit
            caught.append(f"{name} [{len(found)} finding(s)] -> {shown}")
    if crashed:
        return True, (f"{len(crashed)} plant(s) CRASHED — a FIXTURE DEFECT, not a "
                      f"finding: " + " · ".join(crashed))
    if passed or wrong:
        return True, (f"{len(passed)} plant(s) PASSED {passed}; {len(wrong)} caught by the "
                      f"WRONG detector {wrong}")
    return False, (f"all {len(caught)} plants caught by their named detector, one at a "
                   f"time: " + " · ".join(caught))


def file_transcript(out: Path, body: bytes, refile: bool) -> list[str]:
    """NEVER CLOBBER the transcript of record [tierc10_resume_fixtures.file_transcript]."""
    if not out.exists() and not refile:
        return [f"{out.name} ABSENT — nothing written; re-file with --refile-transcript"]
    if out.exists() and out.read_bytes() == body:
        return []
    if out.exists() and not refile:
        (rr := out.with_name(out.stem + "_rerun.txt")).write_bytes(body)
        return [f"{out.name} NOT byte-identical; this run -> {rr.name}; record untouched"]
    out.write_bytes(body)
    return []


# ═══════════════════════════════════════════════════════ LEG STATES OUTSIDE prove [L-0.14 C]
def not_run(fid: str, title: str, reason: str) -> None:
    """The THIRD leg state.  Lawful only for a block id on NOT_RUN_FIDS_T, with `reason` the
    condition its owning reading names; any other leg that cannot run reads FAIL [seam 3]."""
    say(f"\n{fid} — {title}")
    if fid not in NOT_RUN_FIDS_T:
        say(f"  [FAIL] {fid}: NOT RUN is not lawful for this block — it is not on NOT_RUN_FIDS_T "
            f"{list(NOT_RUN_FIDS_T)}; a leg that cannot run reads FAIL [L-0.14 C, seam 3]; reason "
            f"given: {reason}")
        FAILED.append(f"{fid} (NOT RUN refused — not on NOT_RUN_FIDS_T)")
        return
    say(f"  [NOT RUN] {fid}: {reason}")
    NOT_RUN.append(fid)


def not_built(fid: str, title: str, reason: str) -> None:
    """The resume paste's "tier-e-never-halts": the F-GRID / F-KEY leg of a Tier-E table that could
    not be built as specified.  Never PASS, never RED; counted beside the tally and by the report."""
    say(f"\n{fid} — {title}")
    if fid_of(fid) not in NOT_BUILT_FIDS_T:
        say(f"  [FAIL] {fid}: NOT BUILT is not lawful for this block — its FID is not on "
            f"NOT_BUILT_FIDS_T {list(NOT_BUILT_FIDS_T)} (the paste names a Tier-E table's F-GRID / "
            f"F-KEY legs only); reason given: {reason}")
        FAILED.append(f"{fid} (NOT BUILT refused — not on NOT_BUILT_FIDS_T)")
        return
    say(f"  [NOT BUILT] {fid}: {reason}")
    NOT_BUILT.append(fid)


def closed_status_findings(status: dict, reg_id: str) -> list[str]:
    """CLOSED-STATUS: a STATUS record that does not say CLOSED_BY_PRECONDITION for `reg_id`, or
    that lists an arm."""
    out = []
    if status.get("registration") != reg_id:
        out.append(f"CLOSED-STATUS {reg_id}: STATUS names registration {status.get('registration')!r}")
    if status.get("status") != STATUS_CLOSED_T:
        out.append(f"CLOSED-STATUS {reg_id}: status reads {status.get('status')!r}, not "
                   f"{STATUS_CLOSED_T!r}")
    if status.get("arms") != []:
        out.append(f"CLOSED-STATUS {reg_id}: STATUS lists arm(s) {status.get('arms')!r}")
    return out


def closed_plants(status: dict, reg_id: str) -> list:
    """The two BREAK plants of a CLOSED-NO-BOOK real-book leg, as rows for `plants` (copies)."""
    built = dict(status, status=STATUS_BUILT_T)
    armed = dict(status, arms=["scored"])
    return [("a STATUS copy reading BUILT", "CLOSED-STATUS",
             lambda: closed_status_findings(built, reg_id)),
            ("a STATUS copy listing an arm", "CLOSED-STATUS",
             lambda: closed_status_findings(armed, reg_id))]


def closed_real(status_path, reg_id: str) -> tuple[bool, str]:
    """The REAL leg of a real-book leg on a registration closed by precondition: asserted FROM THE
    FILE regbooks/<id>/STATUS.json.  A PASS, never NOT RUN."""
    status = json.loads(Path(status_path).read_text(encoding="utf-8"))
    f = closed_status_findings(status, reg_id)
    return (not f), (f"CLOSED-NO-BOOK {reg_id} — STATUS.json status {status.get('status')!r}, arms "
                     f"{status.get('arms')!r}" + (f"; findings {f}" if f else ""))


# ═══════════════════════════════════════════════════════════════ BLOCK IDS [L-0.14 B]
def block_id(fid: str, leg: str | None = None, instance: str | None = None) -> str:
    q = QUAL_SEP.join(x for x in (leg, instance) if x)
    return f"{fid} [{q}]" if q else fid


def block_findings(block: str) -> list[str]:
    """BLOCK-ID: a block id outside the grammar."""
    m = BLOCK_RX.fullmatch(block)
    if not m:
        return [f"BLOCK-ID {block!r}: not `<FID>` or `<FID> [<qualifier>]` with FID matching "
                f"{FID_RX.pattern} and no bracket inside the qualifier"]
    q = m.group("q")
    if q is not None:
        parts = q.split(QUAL_SEP)
        if len(parts) > 2 or any(not p or p != p.strip() for p in parts):
            return [f"BLOCK-ID {block!r}: qualifier {q!r} is not `<leg>`, `<instance>` or "
                    f"`<leg> · <instance>`"]
    return []


def split_block(block: str) -> tuple[str, str | None]:
    f = block_findings(block)
    if f:
        raise ValueError(f[0])
    m = BLOCK_RX.fullmatch(block)
    return m.group("fid"), m.group("q")


def fid_of(block: str) -> str:
    """The FID of a block id (the text before ` [`); the whole string when it has no qualifier."""
    return block.split(" [", 1)[0]


def blocks() -> list[str]:
    """The block ids this session has filed, in order (read from the transcript lines)."""
    return [x[1:].split(" — ", 1)[0] for x in LINES
            if x.startswith("\n") and not x.startswith("\n ") and " — " in x]


# ═══════════════════════════════════════════════════════════════ THE main PROTOCOL
def opt(args, prefix: str, default=None):
    """The value of the first `--key=value` argument with that prefix (`opt(args, "--root=")`)."""
    return next((a.split("=", 1)[1] for a in args if a.startswith(prefix)), default)


def picks(args) -> list[str]:
    """The leg filter: lower-cased non-flag arguments.  A filtered run files <stem>_partial.txt."""
    return [a.lower() for a in args if not a.startswith("--")]


def reset() -> None:
    for k in _STATE:
        globals()[k].clear()


@contextlib.contextmanager
def capture():
    """An INNER session: the legs run inside write to fresh lists and print nothing; the outer
    session is restored on exit.  Yields {"LINES", "PASSED", "FAILED", "NOT_RUN", "NOT_BUILT"}."""
    g = globals()
    saved = {k: g[k] for k in _STATE}
    inner = {k: [] for k in _STATE}
    g.update(inner)
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            yield inner
    finally:
        g.update(saved)


def header(banner: str, *, seed, substrate=None, as_of_iso=None, pin=None, typed=()) -> None:
    """The transcript header [L-0.14 I].  `substrate=None` is a record before TC12-D: the fixed
    pre-substrate pair.  Otherwise `as_of_iso`, `pin` (ms) and `substrate` (the snapshot name) are
    the calling suite's, read from Stage D's records.  `typed` = the suite's typed literals, one
    line each (a seeded leg's count `n` among them)."""
    if substrate is None:
        if as_of_iso is not None or pin is not None:
            raise ValueError("a pre-substrate header names no pin")
        say(PRE_SUBSTRATE_AS_OF)
        say(PRE_SUBSTRATE_LINE)
        tail = f"seed {seed} · substrate none · pin (pre-substrate stage)"
    else:
        if as_of_iso is None or pin is None:
            raise ValueError("a substrate header needs as_of_iso and pin")
        say(f"as_of_last_closed_4h: {as_of_iso}")
        tail = f"seed {seed} · substrate {substrate} · pin {pin}"
    say(RULE)
    say(banner)
    say(RULE)
    say(tail)
    for t in typed:
        say(f"  typed: {t}")


def run_leg(row) -> None:
    """One fixture row: a 6-tuple (fid, title, break_if, real_if, break_leg, real_leg) goes to
    `prove`; a 2-tuple (fid, thunk) calls the thunk, which must file exactly that one block
    (through `prove`, `not_run` or `not_built`)."""
    if len(row) != 2:
        prove(*row)
        return
    fid, thunk = row
    before = len(blocks())
    thunk()
    filed = blocks()[before:]
    if filed != [fid]:
        FAILED.append(f"{fid} (the leg filed block(s) {filed}, not exactly its own)")


def tally() -> None:
    say(f"\n  {len(PASSED)} GREEN, {len(FAILED)} RED, {len(NOT_RUN)} NOT RUN")
    for f in FAILED:
        say(f"    RED: {f}")
    if NOT_BUILT:
        say(f"  {len(NOT_BUILT)} NOT BUILT")
        for f in NOT_BUILT:
            say(f"    NOT BUILT: {f}")


def summary() -> dict:
    """What a fixture record carries: `legs_total` = GREEN + RED + NOT RUN (C's identity);
    NOT BUILT blocks are counted beside it."""
    return {"legs_total": len(PASSED) + len(FAILED) + len(NOT_RUN), "legs_green": len(PASSED),
            "legs_red": len(FAILED), "legs_not_run": len(NOT_RUN),
            "legs_not_built": len(NOT_BUILT), "green": not FAILED}


def transcript_bytes() -> bytes:
    return ("\n".join(LINES) + "\n").encode("utf-8")


def finish(root, transcript: str, args, t0: float | None = None) -> int:
    """Tally, file the transcript under the no-clobber law, return the exit code.  A block id
    outside the grammar is counted RED.  Nothing is created when the transcript is absent and
    --refile-transcript was not given."""
    for b in blocks():
        if block_findings(b):
            for held in (PASSED, NOT_RUN, NOT_BUILT):
                while b in held:
                    held.remove(b)
            if not any(x == b or x.startswith(b + " (") for x in FAILED):
                FAILED.append(f"{b} (block id outside the grammar of L-0.14 B)")
    tally()
    pick = picks(args)
    refile = "--refile-transcript" in args or bool(pick)
    root = Path(root)
    if refile:
        root.mkdir(parents=True, exist_ok=True)
    body = transcript_bytes()
    name = transcript if not pick else transcript.replace(".txt", "_partial.txt")
    bad = file_transcript(root / name, body, refile)
    for x in bad:
        clock(x)
    wall = "" if t0 is None else f"wall {time.time() - t0:.1f}s · "
    clock(f"{wall}transcript sha {sha_bytes(body)}")
    if FAILED:
        print("*** HALT: fixture mismatch. Nothing downstream is trustworthy. ***")
    return 1 if (FAILED or bad) else 0


def run_suite(*, args, root, transcript: str, banner: str, seed, fixtures, substrate=None,
              as_of_iso=None, pin=None, typed=()) -> int:
    """The main protocol in one call.  `args` = sys.argv[1:]; `root` = the directory the suite
    resolved from `--root=` (its transcript and every write go under it); `fixtures` = rows for
    `run_leg`, run in order, filtered by the positional leg substrings."""
    reset()
    t0 = time.time()
    pick = picks(args)
    header(banner, seed=seed, substrate=substrate, as_of_iso=as_of_iso, pin=pin, typed=typed)
    for row in fixtures:
        if not pick or any(q in row[0].lower() for q in pick):
            run_leg(row)
    return finish(root, transcript, args, t0)


# ═══════════════════════════════════════════════════════════════ FIXTURE RANDOMNESS [L-0.14 F]
def suite_tag(stem) -> str:
    """The suite's stem without `tierc12_` and `_fixtures` (`va`, `stage_r`, `scalp`, `tide`, …)."""
    s = Path(str(stem)).stem
    s = s[len("tierc12_"):] if s.startswith("tierc12_") else s
    return s[:-len("_fixtures")] if s.endswith("_fixtures") else s


def stream_seed(seed, tag: str, block: str) -> list:
    """[SEED, crc32("<suite tag>|<block id>")] — the seed of one fixture stream."""
    return [seed, zlib.crc32(f"{tag}|{block}".encode("utf-8"))]


def stream(np, seed, tag: str, block: str):
    """numpy.random.default_rng([SEED, crc32("<suite tag>|<block id>")]); `np` is the suite's."""
    return np.random.default_rng([seed, zlib.crc32(f"{tag}|{block}".encode("utf-8"))])


# ═══════════════════════════════════════════════════════════════ THE HAND-SAMPLE LAW [L-0.14 G]
def hand_sample(rows, *, key, k: int, categories=(), contract_named=(), rule: str = "",
                n_asserted=None, rng=None) -> dict:
    """THE ONE LAW.  `rows` = the population; `key(row)` = the owning reading's key order; `k` =
    the contract's count; `categories` = ordered (name, predicate(row)) pairs frozen in the reading.
    Categories first: the first row of each category in key order.  (1) an empty category prints
    `NONE-EXISTS <category>` and its slot is taken by the next unchosen row in key order, printed
    `FILL` (so is the slot of a category whose first row an earlier category already took).
    (2) n < k: ALL n are verified, `ONLY <n> EXIST (contract count <k>)`; n = 0: `EMPTY
    POPULATION`.  (3) a shortfall, or an empty category named in `contract_named`, is a
    `FINDING: …` line, carried to the report.  (4) nothing here is RED on the size or composition
    of a population: `problems` is non-empty ONLY when the population handed in does not hold the
    count `n_asserted` (the population's own count, from its record).  No categories = a seeded
    draw (`rng`, a stream of `stream()`) over the key-sorted population.
    Returns {"chosen": [(label, row)], "lines": [str], "findings": [str], "problems": [str],
    "n": n, "k": k}; the leg prints `lines` and verifies every chosen row."""
    pop = sorted(rows, key=key)
    n = len(pop)
    lines = [f"hand-sample rule: {rule}"] if rule else []
    findings, problems, chosen = [], [], []
    taken: set = set()
    if n_asserted is not None and n_asserted != n:
        problems.append(f"HAND-SAMPLE-COUNT: the population handed in holds {n} row(s); its own "
                        f"record counts {n_asserted}")

    def take(label: str, i: int) -> None:
        taken.add(i)
        chosen.append((label, pop[i]))
        lines.append(f"{label}: {key(pop[i])}")

    if not categories:
        if n > k and rng is None:
            raise ValueError("a sample with no categories is a seeded draw: hand it a stream")
        idx = range(n) if n <= k else sorted(int(i) for i in rng.choice(n, size=k, replace=False))
        for i in idx:
            take("DRAW", i)
    else:
        owed = []
        for name, pred in categories:
            first = next((i for i in range(n) if pred(pop[i])), None)
            if first is None:
                lines.append(f"NONE-EXISTS {name} (its count in the population is 0)")
                if name in contract_named:
                    findings.append(f"FINDING: the contract-named category {name} is EMPTY in a "
                                    f"population of {n} — a finding-not-fixed owned by the operator")
                owed.append(name)
            elif first in taken:
                lines.append(f"SHARED {name}: its first row {key(pop[first])} is already chosen")
                owed.append(name)
            else:
                take(name, first)
        want = max(k, len(categories))
        while len(chosen) < min(want, n):
            i = next(j for j in range(n) if j not in taken)
            take(f"FILL (slot of {owed.pop(0)})" if owed else "FILL", i)
    if n == 0:
        lines.append(f"EMPTY POPULATION (contract count {k})")
    elif n < k:
        lines.append(f"ONLY {n} EXIST (contract count {k})")
    if n < k:
        findings.append(f"FINDING: the population holds {n} row(s), the contract's count is {k} — "
                        f"all {n} verified; a finding-not-fixed owned by the operator")
    lines += findings
    return {"chosen": chosen, "lines": lines, "findings": findings, "problems": problems,
            "n": n, "k": k}


# ═══════════════════════════════════════════════════════════════ TEXT REFEREES (read, never run)
def rel(p, root=ROOT) -> str:
    """A path as a transcript may print it: repo-relative posix, never an absolute home path."""
    try:
        return Path(p).resolve().relative_to(Path(root).resolve()).as_posix()
    except ValueError:
        return f"<outside the tree>/{Path(p).name}"


def func_dump(text: str, name: str) -> str:
    """`ast.dump` of the module-level function `name`, parsed from source TEXT."""
    for n in ast.parse(text).body:
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == name:
            return ast.dump(n)
    raise KeyError(f"no module-level function {name!r}")


def literal_from_text(text: str, name: str, key=None):
    """`ast.literal_eval` of the last module-level assignment to `name`, from source TEXT.  With
    `key`, the assignment must be a dict display and only the value under that constant key is
    evaluated (a dict whose other values are names — TC11-X's `COLLAR` holds `M_NOTE` by name —
    is not a literal as a whole)."""
    val = None
    for n in ast.parse(text).body:
        if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name
                                             for t in n.targets):
            val = n.value
        elif isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name) \
                and n.target.id == name and n.value is not None:
            val = n.value
    if val is None:
        raise KeyError(f"no module-level assignment to {name!r}")
    if key is None:
        return ast.literal_eval(val)
    if not isinstance(val, ast.Dict):
        raise KeyError(f"{name!r} is not a dict display")
    hits = [v for k, v in zip(val.keys, val.values)
            if isinstance(k, ast.Constant) and k.value == key]
    if len(hits) != 1:
        raise KeyError(f"{name!r} holds the constant key {key!r} {len(hits)} time(s), not once")
    return ast.literal_eval(hits[0])


# ═══════════════════════════════════════════════════════════════ F-GRID helper legs [L-0.15]
def grid_cells(axes) -> list[str]:
    """The cell list of a declared cross: the product in axis order, each cell the `¦`-joined
    `axis:level` tokens.  `axes` = an ordered mapping axis -> tuple of levels."""
    names = list(axes)
    return [CELL_SEP.join(f"{a}:{v}" for a, v in zip(names, combo))
            for combo in itertools.product(*(axes[a] for a in names))]


def grid_count(axes) -> int:
    n = 1
    for a in axes:
        n *= len(axes[a])
    return n


def grid_findings(TP, declared, written, *, grid_id: str, axes=None, built_count=None,
                  cell_col: str = "cell", require_cols=(), require_false=("promotable",),
                  population_n=None, n_col: str = "n", stat_cols=(),
                  nan_reason_col: str = "nan_reason", forbidden_rx=FORBIDDEN_NAME_RX) -> list[str]:
    """One grid, whole.  `TP` = the lineage panel module (the shim's `E.TP`); `declared` = the
    FIXTURE's typed cell list; `written` = the table as filed; `axes` = the fixture's typed axes;
    `built_count` = the builder's computed count; `population_n` = the population's row count read
    from the book (a grid that partitions it).  Detectors: GRID-WHOLE (a cell missing, undeclared
    or duplicated; a required column absent or null; `promotable` True) · GRID-COUNT · GRID-CELLS ·
    GRID-PARTITION · GRID-NAN (a statistic NaN without `nan_reason`) · GRID-VERDICT."""
    dec = [str(c) for c in declared]
    ok, lines = TP.grid_whole(dec, written, cell_col=cell_col, require_cols=tuple(require_cols),
                              require_false=tuple(require_false), label=grid_id)
    out = [f"GRID-WHOLE {x}" for x in lines if x.startswith("[BAD]")]
    if not ok and not out:
        out.append(f"GRID-WHOLE {grid_id}: TP.grid_whole is False with no [BAD] line")
    if axes is not None:
        if grid_count(axes) != len(dec):
            out.append(f"GRID-COUNT {grid_id}: the fixture types {len(dec)} cells; the product of "
                       f"its axes' cardinalities is {grid_count(axes)}")
        if sorted(grid_cells(axes)) != sorted(dec):
            out.append(f"GRID-CELLS {grid_id}: the fixture's cell list is not the product of its "
                       f"typed axes")
    if built_count is not None and built_count != len(dec):
        out.append(f"GRID-COUNT {grid_id}: the builder computed {built_count} cells; the fixture "
                   f"types {len(dec)}")
    cols = [str(c) for c in written.columns]
    if population_n is not None:
        s = int(written[n_col].sum()) if n_col in cols else None
        if s != population_n:
            out.append(f"GRID-PARTITION {grid_id}: the cells' `{n_col}` sum to {s}; the population "
                       f"holds {population_n}")
    for c in stat_cols:
        if c not in cols:
            out.append(f"GRID-NAN {grid_id}: statistic column `{c}` absent")
            continue
        nan = [bool(x) for x in written[c].isna().tolist()]
        why = ([bool(x) for x in written[nan_reason_col].isna().tolist()]
               if nan_reason_col in cols else [True] * len(nan))
        k = sum(1 for a, b in zip(nan, why) if a and b)
        if k:
            out.append(f"GRID-NAN {grid_id}: `{c}` is NaN on {k} row(s) with no `{nan_reason_col}`")
    bad = [c for c in cols if forbidden_rx.search(c)]
    if bad:
        out.append(f"GRID-VERDICT {grid_id}: the grid holds verdict-named column(s) {bad}")
    return out


def _md_tables(text: str) -> list[tuple[int, list[str]]]:
    """The markdown tables of a document: (index of the header line, its lines)."""
    lines = text.split("\n")
    out, i = [], 0
    while i < len(lines):
        if lines[i].lstrip().startswith("|"):
            j = i
            while j < len(lines) and lines[j].lstrip().startswith("|"):
                j += 1
            out.append((i, lines[i:j]))
            i = j
        else:
            i += 1
    return out


def _md_rows(table: list[str]) -> list[list[str]]:
    """The DATA rows of a markdown table (the header and its `|---|` rule dropped), as fields."""
    rows = [[f.strip() for f in ln.strip().strip("|").split("|")] for ln in table]
    return [r for r in rows[1:] if not all(set(f) <= set("-: ") for f in r)]


def grid_printed_findings(text: str, grid_id: str, cells) -> list[str]:
    """GRID-PRINTED: a grid printed in a document of record — the marker `<!-- grid: <ID>
    cells=<count> -->` carries the parquet's cell count and the table beneath it has exactly that
    many data rows, one per cell id of the parquet (`cells`).  No top-k, no ellipsis."""
    cells = [str(c) for c in cells]
    lines = text.split("\n")
    at = [i for i, ln in enumerate(lines)
          if (m := GRID_MARKER_RX.search(ln)) and m.group("id") == grid_id]
    if len(at) != 1:
        return [f"GRID-PRINTED {grid_id}: {len(at)} grid marker(s) in the document, not one"]
    n = int(GRID_MARKER_RX.search(lines[at[0]]).group("n"))
    out = []
    if n != len(cells):
        out.append(f"GRID-PRINTED {grid_id}: the marker says cells={n}; the parquet holds "
                   f"{len(cells)}")
    table = next((t for h, t in _md_tables(text) if h > at[0]), None)
    if table is None:
        return out + [f"GRID-PRINTED {grid_id}: no table follows the marker"]
    rows = _md_rows(table)
    got = [next((f for f in r if f in cells), None) for r in rows]
    miss = sorted(set(cells) - {g for g in got if g})
    dup = sorted({g for g in got if g and got.count(g) > 1})
    if len(rows) != len(cells) or miss or dup or None in got:
        out.append(f"GRID-PRINTED {grid_id}: the printed table has {len(rows)} data row(s) for "
                   f"{len(cells)} cell(s); cells not printed {miss or 'none'}, printed twice "
                   f"{dup or 'none'}, rows carrying no cell id {got.count(None)}")
    return out


def grid_pointer_findings(grid_id: str, pointer: dict, doc_bytes: bytes, cells) -> list[str]:
    """GRID-POINTER: a report's pointer row {path, sha256, cells} to a grid printed whole in its
    stage document — the sha, the cell count, and the stage document printing that grid whole."""
    out = []
    if pointer.get("sha256") != sha_bytes(doc_bytes):
        out.append(f"GRID-POINTER {grid_id}: the pointer row carries another sha than the stage "
                   f"document's")
    if pointer.get("cells") != len(list(cells)):
        out.append(f"GRID-POINTER {grid_id}: the pointer row says {pointer.get('cells')} cells; "
                   f"the grid holds {len(list(cells))}")
    out += [f"GRID-POINTER {x}" for x in
            grid_printed_findings(doc_bytes.decode("utf-8"), grid_id, cells)]
    return out


# ═══════════════════════════════════════════════════════════════ F-COLLAR helper legs [L-0.16]
def collar_table_findings(name: str, df, *, collar_cols, ci_readings, registered: bool,
                          m_expected=None, forbidden_rx=FORBIDDEN_NAME_RX,
                          ci_col: str = "would_read_ci_only", m_col: str = "m_looks_this_table",
                          promotable_col: str = "promotable") -> list[str]:
    """One parquet.  `collar_cols` and `ci_readings` (the four values) are the FIXTURE's typed
    copies; `registered` = the table is on REGISTERED_TABLES_T; `m_expected` = the fixture's own
    count of the table's intervals.  Detectors: COLLAR-REGISTERED (a registered table carries the
    collar) · COLLAR-COL · COLLAR-NULL · COLLAR-CI · COLLAR-PROMOTABLE · COLLAR-NAME · COLLAR-M."""
    cols = [str(c) for c in df.columns]
    if registered:
        have = [c for c in collar_cols if c in cols]
        return ([f"COLLAR-REGISTERED {name}: a table on REGISTERED_TABLES_T carries collar "
                 f"column(s) {have}"] if have else [])
    out = []
    lack = [c for c in collar_cols if c not in cols]
    if lack:
        out.append(f"COLLAR-COL {name}: collar column(s) absent {lack}")
    for c in [c for c in collar_cols if c in cols]:
        k = int(df[c].isna().sum())
        if k:
            out.append(f"COLLAR-NULL {name}: {k} null(s) in collar column {c}")
    if ci_col in cols:
        bad = sorted({str(v) for v in df[ci_col].tolist() if v not in tuple(ci_readings)})
        if bad:
            out.append(f"COLLAR-CI {name}: {ci_col} outside the four readings: {bad}")
    if promotable_col in cols and any(v is not None and v == v and bool(v)
                                      for v in df[promotable_col].tolist()):
        out.append(f"COLLAR-PROMOTABLE {name}: {promotable_col} is True on a row")
    named = [c for c in cols if forbidden_rx.search(c)]
    if named:
        out.append(f"COLLAR-NAME {name}: column(s) named for a verdict, a cleared bar or a spent "
                   f"test: {named}")
    if m_expected is not None and m_col in cols:
        got = sorted({str(v) for v in df[m_col].tolist()})
        if got not in ([], [str(m_expected)]):
            out.append(f"COLLAR-M {name}: {m_col} holds {got}; the fixture counts {m_expected} "
                       f"interval(s)")
    return out


def collar_leaf_findings(name: str, obj, forbidden_rx=FORBIDDEN_NAME_RX,
                         verdict_words=()) -> list[str]:
    """One collared JSON leaf.  COLLAR-NAME: a key, at any depth, named for a verdict, a cleared
    bar or a spent test · COLLAR-WORD: a string value that is one of the fixture's `verdict_words`."""
    keys, words = [], []

    def walk(o, path: str) -> None:
        if isinstance(o, dict):
            for k in sorted(o, key=str):
                p = f"{path}.{k}" if path else str(k)
                if forbidden_rx.search(str(k)):
                    keys.append(p)
                walk(o[k], p)
        elif isinstance(o, list):
            for i, v in enumerate(o):
                walk(v, f"{path}[{i}]")
        elif isinstance(o, str) and o in tuple(verdict_words):
            words.append(f"{path}={o!r}")

    walk(obj, "")
    out = []
    if keys:
        out.append(f"COLLAR-NAME {name}: key(s) named for a verdict, a cleared bar or a spent "
                   f"test: {keys}")
    if words:
        out.append(f"COLLAR-WORD {name}: verdict word(s) in a collared leaf: {words}")
    return out


def collar_doc_findings(name: str, text: str, *, registered_marker_ok: bool,
                        collar_line: str = COLLAR_LINE,
                        window: int = COLLAR_DOC_WINDOW_T) -> list[str]:
    """One document.  COLLAR-DOC: a markdown table with neither the registered marker nor the
    collar line within the `window` lines above its header · COLLAR-MARKER: the registered marker
    in a document where it is not allowed (`registered_marker_ok` False).  Tables are named by
    ordinal and header, never by line number."""
    lines = text.split("\n")
    out = []
    for k, (h, table) in enumerate(_md_tables(text)):
        above = lines[max(0, h - window):h]
        marked = any(REGISTERED_MARKER_RX.search(x) for x in above)
        collared = any(collar_line in x for x in above)
        if not (marked or collared):
            out.append(f"COLLAR-DOC {name}: table #{k + 1} ({table[0].strip()}) has neither the "
                       f"registered marker nor the collar line above its header")
        if marked and not registered_marker_ok:
            out.append(f"COLLAR-MARKER {name}: the registered marker stands above table #{k + 1} "
                       f"({table[0].strip()}) in a document where it is not allowed")
    return out


# ═══════════════════════════════════════════════════════════════ F-KEY helper legs [L-0.21]
def key_findings(name: str, df, key, required=(), null_iff=None, *, as_of_cols=(),
                 columns=None) -> list[str]:
    """One table against the fixture's typed commission.  KEY-DUP a duplicated key · KEY-NULL a
    null in (or the absence of) a key / required column · KEY-ASOF an as-of stamp absent or null ·
    KEY-FLAG a nullable column whose nulls disagree with its typed flag (`null_iff` = {column:
    (flag column, value)}: the column is null iff the flag equals the value — iff the flag is null
    when the value is None) · KEY-COLS the column list is not the typed one, in order."""
    out = []
    cols = [str(c) for c in df.columns]
    need = list(dict.fromkeys(list(key) + list(required)))
    miss = [c for c in need if c not in cols]
    if miss:
        out.append(f"KEY-NULL {name}: required column(s) absent {miss}")
    sub = [c for c in key if c in cols]
    dup = int(df.duplicated(subset=sub).sum()) if sub else 0
    if dup:
        out.append(f"KEY-DUP {name}: {dup} duplicated {list(key)} row(s)")
    for c in [c for c in need if c in cols]:
        k = int(df[c].isna().sum())
        if k:
            out.append(f"KEY-NULL {name}: {k} null(s) in required column {c}")
    lack = [c for c in as_of_cols if c not in cols]
    nul = [c for c in as_of_cols if c in cols and bool(df[c].isna().any())]
    if lack or nul:
        out.append(f"KEY-ASOF {name}: as-of stamp(s) absent {lack} / null {nul}")
    for c, (flag, val) in sorted((null_iff or {}).items()):
        if c not in cols or flag not in cols:
            out.append(f"KEY-FLAG {name}: {c} or its flag {flag} absent")
            continue
        isnull = [bool(x) for x in df[c].isna().tolist()]
        should = [bool(x) for x in (df[flag].isna() if val is None else df[flag] == val).tolist()]
        k = sum(1 for a, b in zip(isnull, should) if a != b)
        if k:
            out.append(f"KEY-FLAG {name}: {c} null on {sum(isnull)} row(s) but {flag}"
                       f"{' is null' if val is None else ' == ' + repr(val)} on {sum(should)} "
                       f"({k} disagree)")
    if columns is not None and tuple(cols) != tuple(columns):
        extra = [c for c in cols if c not in columns]
        gone = [c for c in columns if c not in cols]
        out.append(f"KEY-COLS {name}: column list != typed (absent {gone}, extra {extra}"
                   f"{', order differs' if not gone and not extra else ''})")
    return out


def stamp_findings(name: str, df, stamp: dict) -> list[str]:
    """KEY-STAMP — STAMP TRUTH: `stamp` = {stamp column: the value the fixture types for this
    table} (as_of_n_assets = the asset count of the panel the table declares, as_of_panel its
    name, as_of_last_closed_4h the edge L-0.13 assigns, as_of_substrate Stage D's snapshot name);
    every row must carry exactly that value."""
    out = []
    cols = [str(c) for c in df.columns]
    for c in sorted(stamp):
        if c not in cols:
            out.append(f"KEY-STAMP {name}: stamp column {c} absent")
            continue
        got = sorted({str(v) for v in df[c].tolist()})
        if got not in ([], [str(stamp[c])]):
            out.append(f"KEY-STAMP {name}: {c} holds {got}; the table's typed stamp is "
                       f"{str(stamp[c])!r}")
    return out


def key_dir_findings(E, pd, root, specs: dict, *, manifest: dict | None = None,
                     manifest_name: str = "build_manifest.json", as_of_cols=None, collar=None,
                     not_built=()) -> list[str]:
    """One parquet directory, the three filed meanings and TC12's two additions [L-0.21].
    `E` = the shim (E.TP.check_keys, E.TP.AS_OF_COLUMNS, E.TB._content_sha); `pd` = pandas;
    `specs` = the FIXTURE's typed commission, {table stem: {"key": [...], "required": (...),
    "null_iff": {...} | None, "columns": (...) | None, "stamp": {...} | None}}; `manifest` = a
    scoped manifest (a SHARED_DIRS_T view, L-0.9) or None for the directory's own; `collar` = None
    or {"cols": (...), "ci_readings": (...), "registered": (stems), "m": {stem: count}} for COLLAR
    TOTALITY on the same pass; `not_built` = typed stems of Tier-E tables printed NOT BUILT (they
    must be absent from disk and from the manifest).
    Detectors: KEY-TOTALITY (the lineage's check_keys: undeclared, ghost, dupes, as-of) ·
    KEY-UNDECLARED (a parquet the fixture does not type) · KEY-GHOST (a typed table absent) ·
    KEY-NOT-BUILT · KEY-DECL (the manifest's key is not the typed key) · KEY-SHA (the manifest's
    content sha is not the table's, read back) · and those of key_findings, stamp_findings and
    collar_table_findings."""
    root = Path(root)
    man = manifest if manifest is not None else json.loads(
        (root / manifest_name).read_text(encoding="utf-8"))
    aoc = tuple(E.TP.AS_OF_COLUMNS) if as_of_cols is None else tuple(as_of_cols)
    ok, lines = E.TP.check_keys(root, man, need_cols=aoc)
    out = [f"KEY-TOTALITY {x}" for x in lines if x.startswith("[BAD]")]
    if not ok and not out:
        out.append("KEY-TOTALITY: TP.check_keys is False with no [BAD] line")
    stems = sorted(p.stem for p in root.glob("*.parquet"))
    out += [f"KEY-UNDECLARED {s}: a parquet the fixture's commission does not type"
            for s in stems if s not in specs]
    out += [f"KEY-GHOST {s}: a typed table with no parquet in the directory"
            for s in sorted(specs) if s not in stems and s not in not_built]
    out += [f"KEY-NOT-BUILT {s}: printed NOT BUILT, yet on disk or in the manifest"
            for s in sorted(not_built) if s in stems or s in man.get("keys", {})]
    for s in [s for s in stems if s in specs]:
        sp = specs[s]
        df = pd.read_parquet(root / f"{s}.parquet")
        mkey = man.get("keys", {}).get(s)
        if mkey is None or list(mkey) != list(sp["key"]):
            out.append(f"KEY-DECL {s}: the manifest declares key {mkey}; the fixture types "
                       f"{list(sp['key'])}")
        out += key_findings(s, df, sp["key"], sp.get("required", ()), sp.get("null_iff"),
                            as_of_cols=aoc, columns=sp.get("columns"))
        sha = E.TB._content_sha(df)
        if man.get("sha", {}).get(s) != sha:
            out.append(f"KEY-SHA {s}: the manifest's content sha is not the table's read back "
                       f"({str(man.get('sha', {}).get(s))[:12]}… != {sha[:12]}…)")
        if sp.get("stamp"):
            out += stamp_findings(s, df, sp["stamp"])
        if collar is not None:
            out += collar_table_findings(
                s, df, collar_cols=collar["cols"], ci_readings=collar["ci_readings"],
                registered=s in collar.get("registered", ()), m_expected=collar.get("m", {}).get(s))
    return out


# ═══════════════════════════════════════════════════════════════ F-DET helper legs [L-0.20]
def det_seeds(seed) -> tuple[str, str]:
    """The two PYTHONHASHSEED twins: "1" and the tier seed.  The TIER SEED drives every ruler in
    BOTH twins; only the interpreter's hash seed differs."""
    return (HASHSEED_FIRST_T, str(seed))


def det_dir(directory, stage: str, hashseed) -> Path:
    """<dir>/_det_<stage>/seed_<s>/ (git-ignored)."""
    return Path(directory) / f"_det_{stage}" / f"seed_{hashseed}"


def det_twins(launch, directory, stage: str, seed) -> dict:
    """Run the directory's ONE writer twice.  `launch(twin_dir, hashseed)` is the calling SUITE's
    function: it starts the writer in a FRESH subprocess that imports E before any I/O, under
    PYTHONHASHSEED=hashseed, writing into twin_dir, and returns the exit code or a handle with
    `.wait()` (the harness holds no subprocess site).  Each twin directory is removed first.
    Returns {"seed <s>": (exit code, twin_dir)} in the fixed seed order."""
    dirs = [(s, det_dir(directory, stage, s)) for s in det_seeds(seed)]
    for _, d in dirs:
        if d.exists():
            shutil.rmtree(d)
    handles = [launch(d, s) for s, d in dirs]
    return {f"seed {s}": ((h if isinstance(h, int) else int(h.wait())), d)
            for (s, d), h in zip(dirs, handles)}


def read_dir(d) -> dict:
    """{file name: bytes} of the files directly in `d` (the lineage's checkers do not recurse)."""
    d = Path(d)
    return {p.name: p.read_bytes() for p in sorted(d.iterdir()) if p.is_file()} if d.exists() else {}


def det_file_set(typed, manifest: dict | None, skipped_empty_counts=None,
                 skip_empty_law: bool = True) -> tuple[list[str], list[str]]:
    """THE FILE SET of a directory: the fixture-typed set minus the manifest's `skipped_empty`,
    each skipped name asserted empty by the FIXTURE's own count (`skipped_empty_counts` = {name:
    rows}).  A regbook directory holds every arm, empty or not: `skip_empty_law=False`, and any
    skipped name is a finding.  Returns (the expected file names, DET-SKIPPED-EMPTY findings)."""
    skipped = list((manifest or {}).get("skipped_empty", []))
    out = []
    if skipped and not skip_empty_law:
        out.append(f"DET-SKIPPED-EMPTY: a regbook directory skipped {sorted(skipped)}; every arm "
                   f"its spec names is written, empty or not")
    for s in sorted(skipped):
        n = (skipped_empty_counts or {}).get(s)
        if n is None or n:
            out.append(f"DET-SKIPPED-EMPTY: `{s}` is listed under skipped_empty while the "
                       f"fixture's own count of its frame is {n}")
    drop = {f"{s}.parquet" for s in skipped} if skip_empty_law else set()
    return [f for f in typed if f not in drop], out


def _clock_keys(o, rx, exempt) -> list[str]:
    hits = []
    if isinstance(o, dict):
        for k in sorted(o, key=str):
            if rx.search(str(k)) and str(k) not in exempt:
                hits.append(str(k))
            hits += _clock_keys(o[k], rx, exempt)
    elif isinstance(o, list):
        for v in o:
            hits += _clock_keys(v, rx, exempt)
    return hits


def clock_findings(files: dict, *, pd=None, clock_rx=CLOCK_NAME_RX, exempt=()) -> list[str]:
    """DET-CLOCK: a clock-like KEY in a JSON / JSONL file, or a clock-like parquet column.
    `files` = {name: bytes}; `exempt` = keys exempted BY NAME by the owning reading."""
    out = []
    for name, b in sorted(files.items()):
        if name.endswith((".json", ".jsonl")):
            text = b.decode("utf-8")
            docs = ([json.loads(x) for x in text.split("\n") if x.strip()]
                    if name.endswith(".jsonl") else [json.loads(text)])
            hits = sorted({k for d in docs for k in _clock_keys(d, clock_rx, tuple(exempt))})
            if hits:
                out.append(f"DET-CLOCK {name}: clock-like key(s) {hits}")
        if name.endswith(".parquet"):
            if pd is None:
                raise RuntimeError("a parquet is in the file set: hand clock_findings pandas")
            cols = [str(c) for c in pd.read_parquet(io.BytesIO(b)).columns
                    if clock_rx.search(str(c))]
            if cols:
                out.append(f"DET-CLOCK {name}: clock-like column(s) {cols}")
    return out


def det_findings(twins: dict, canon: dict, file_set, *, E=None, pd=None,
                 clock_rx=CLOCK_NAME_RX, clock_exempt=()) -> list[str]:
    """`twins` = {label: (exit code, {name: bytes})}, the two in seed order; `canon` = {name:
    bytes} of the canonical directory; `file_set` = the expected names (`det_file_set`).
    Detectors: DET-EXIT · DET-FILESET (a twin's or the canonical file set is not the typed one) ·
    DET-BYTES (twin to twin, first twin to canonical) · DET-CONTENT-SHA (a parquet's
    E.TB._content_sha, read back) · DET-CLOCK."""
    labs = list(twins)
    if len(labs) != 2:
        raise ValueError("F-DET compares exactly two twins")
    a, b = twins[labs[0]], twins[labs[1]]
    want = sorted(file_set)
    out = [f"DET-EXIT {lab}: exit {rc}" for lab, (rc, _) in twins.items() if rc != 0]
    sides = ((labs[0], a[1]), (labs[1], b[1]), ("canonical", canon))
    for lab, x in sides:
        if sorted(x) != want:
            out.append(f"DET-FILESET {lab}: file set != typed (absent "
                       f"{sorted(set(want) - set(x))}, extra {sorted(set(x) - set(want))})")
    for lab, x, y in ((f"{labs[0]} vs {labs[1]}", a[1], b[1]),
                      (f"{labs[0]} vs canonical", a[1], canon)):
        for name in sorted(set(x) & set(y)):
            if x[name] != y[name]:
                lim = min(len(x[name]), len(y[name]))
                k = next((i for i in range(lim) if x[name][i] != y[name][i]), lim)
                out.append(f"DET-BYTES {lab}: {name} bytes differ at byte {k}")
            if name.endswith(".parquet"):
                if E is None or pd is None:
                    raise RuntimeError("a parquet is in the file set: hand det_findings E and pandas")
                ca = E.TB._content_sha(pd.read_parquet(io.BytesIO(x[name])))
                cb = E.TB._content_sha(pd.read_parquet(io.BytesIO(y[name])))
                if ca != cb:
                    out.append(f"DET-CONTENT-SHA {lab}: {name} content sha {ca[:12]}… != {cb[:12]}…")
    for lab, x in sides:
        out += [f"{z} [{lab}]" for z in clock_findings(x, pd=pd, clock_rx=clock_rx,
                                                        exempt=clock_exempt)]
    return out


def det_dir_findings(E, pd, twins: dict, canonical_dir, file_set, *,
                     manifest_name: str = "build_manifest.json", skipped_empty_counts=None,
                     skip_empty_law: bool = True, clock_exempt=()) -> list[str]:
    """The whole of L-0.20's GREEN on one directory.  `twins` = what `det_twins` returned;
    `file_set` = the FIXTURE's typed file names (READ_SET.json and rendered documents among them).
    Adds to det_findings: the skip-empty law on the file set (DET-SKIPPED-EMPTY) and, when the
    directory has a manifest, DET-CHECK — E.TP.check_det(twin, canonical) on it (same table set,
    no content sha moved, an independent byte re-hash of every parquet pair, equal input_sha)."""
    canonical_dir = Path(canonical_dir)
    mp = canonical_dir / manifest_name
    man = json.loads(mp.read_text(encoding="utf-8")) if mp.exists() else None
    expected, out = det_file_set(list(file_set), man, skipped_empty_counts, skip_empty_law)
    canon = {k: (canonical_dir / k).read_bytes() for k in expected if (canonical_dir / k).is_file()}
    out += det_findings({lab: (rc, read_dir(d)) for lab, (rc, d) in twins.items()}, canon,
                        expected, E=E, pd=pd, clock_exempt=clock_exempt)
    if man is not None:
        for lab, (_, d) in twins.items():
            if not (Path(d) / manifest_name).exists():
                out.append(f"DET-CHECK {lab}: the twin wrote no {manifest_name}")
                continue
            ok, lines = E.TP.check_det(d, canonical_dir)
            bad = [f"DET-CHECK {lab} vs canonical {x}" for x in lines if x.startswith("[BAD]")]
            out += bad if bad or ok else [f"DET-CHECK {lab} vs canonical: TP.check_det is False"]
    return out


# ═══════════════════════════════════════════════════════════════ L-V's helper legs — F-TRAV [a], [e] · F-VA-PINS [e]
def _ints(node) -> list:
    """The integer literals inside an expression; subscript indices excluded (x[0] is a position)."""
    skip = set()
    for m in ast.walk(node):
        if isinstance(m, ast.Subscript):
            skip |= {id(k) for k in ast.walk(m.slice)}
    return [m.value for m in ast.walk(node)
            if isinstance(m, ast.Constant) and type(m.value) is int and id(m) not in skip]


def _target_names(t) -> list[str]:
    if isinstance(t, ast.Name):
        return [t.id]
    if isinstance(t, ast.Attribute):
        return [t.attr]
    if isinstance(t, (ast.Tuple, ast.List)):
        return [x for e in t.elts for x in _target_names(e)]
    if isinstance(t, ast.Subscript) and isinstance(t.slice, ast.Constant) \
            and isinstance(t.slice.value, str):
        return [t.slice.value]
    return []


def _lens_quotient(node, lens_ms_name: str) -> bool:
    def lens(x) -> bool:
        v = x.value if isinstance(x, ast.Subscript) else None
        return (isinstance(v, ast.Name) and v.id == lens_ms_name) or \
               (isinstance(v, ast.Attribute) and v.attr == lens_ms_name)
    return any(isinstance(m, ast.BinOp) and isinstance(m.op, ast.FloorDiv) and lens(m.left)
               and lens(m.right) for m in ast.walk(node))


def trav_ast_findings(module: str, src: str, *, name_rx=TRAV_NAME_RX, call_sites=(),
                      factor_rx=TRAV_5M_RX, lens_ms_name: str = "LENS_MS") -> list[str]:
    """F-TRAV [a · <module>] — the site-targeted "typed constant" scan of ONE module's source TEXT
    (beside L-0.17's general scan).  TRAV-TYPED: an integer literal ASSIGNED to a time-stop or
    traverse name (a name, an attribute, a tuple element, a string subscript or a dict key matching
    `name_rx`; an augmented assignment and a parameter default included), or PASSED as one (a
    keyword matching `name_rx`, or a positional site of `call_sites` = ((callee, index), …), the
    suite's typed list).  TRAV-FACTOR: a name matching `factor_rx` (the 5m count) built by a product
    whose factor is not the `LENS_MS[…] // LENS_MS[…]` quotient.  No line number is printed."""
    out = []
    for n in ast.walk(ast.parse(src)):
        if isinstance(n, (ast.Assign, ast.AnnAssign, ast.AugAssign)) and n.value is not None:
            targets = n.targets if isinstance(n, ast.Assign) else [n.target]
            names = [x for t in targets for x in _target_names(t) if name_rx.search(x)]
            if names and _ints(n.value):
                out.append(f"TRAV-TYPED {module}: the integer literal(s) {_ints(n.value)} are "
                           f"assigned to the time-stop / traverse name(s) {names}")
            five = [x for x in names if factor_rx.search(x)]
            if five and any(isinstance(m, ast.Mult) for m in ast.walk(n.value)) \
                    and not _lens_quotient(n.value, lens_ms_name):
                out.append(f"TRAV-FACTOR {module}: {five} is a product whose factor is not the "
                           f"{lens_ms_name} quotient")
        elif isinstance(n, ast.Dict):
            for k, v in zip(n.keys, n.values):
                if isinstance(k, ast.Constant) and isinstance(k.value, str) \
                        and name_rx.search(k.value) and _ints(v):
                    out.append(f"TRAV-TYPED {module}: the integer literal(s) {_ints(v)} are "
                               f"assigned to the time-stop / traverse key {k.value!r}")
        elif isinstance(n, ast.Call):
            callee = (n.func.id if isinstance(n.func, ast.Name) else
                      n.func.attr if isinstance(n.func, ast.Attribute) else None)
            for k in n.keywords:
                if k.arg and name_rx.search(k.arg) and _ints(k.value):
                    out.append(f"TRAV-TYPED {module}: the integer literal(s) {_ints(k.value)} are "
                               f"passed as {callee}(…, {k.arg}=…)")
            for fn, pos in call_sites:
                if callee == fn and len(n.args) > pos and _ints(n.args[pos]):
                    out.append(f"TRAV-TYPED {module}: the integer literal(s) {_ints(n.args[pos])} "
                               f"are passed in the time-stop position of {fn}(…)")
        elif isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
            a = n.args
            pos = a.posonlyargs + a.args
            pairs = list(zip(pos[len(pos) - len(a.defaults):], a.defaults)) + \
                [(x, d) for x, d in zip(a.kwonlyargs, a.kw_defaults) if d is not None]
            for arg, d in pairs:
                if name_rx.search(arg.arg) and _ints(d):
                    out.append(f"TRAV-TYPED {module}: the integer literal(s) {_ints(d)} are the "
                               f"default of the time-stop / traverse parameter {arg.arg}")
    return out


def trav_book_findings(book: str, t_values, filed_source, value, source) -> list[str]:
    """F-TRAV [e · <book>] — one range book (real-book: CLOSED-NO-BOOK on a closed row).
    `t_values` = the `T` of every trade row (`df["T"].tolist()`); `filed_source` = what the book's
    manifest files as `time_stop_source` (for that lens); `(value, source)` = what the reader's
    `traverse(name)` returned, at its certified sha.  TRAV-ROW: a row's T is not the door's value ·
    TRAV-SOURCE: the manifest's `time_stop_source` is not the door's `source`."""
    out = []
    vals = list(t_values)
    bad = sum(1 for v in vals if v != value)
    if bad:
        out.append(f"TRAV-ROW {book}: {bad} of {len(vals)} trade row(s) carry a T that is not the "
                   f"door's value {value}")
    if filed_source != source or dict(source).get("value") != value:
        out.append(f"TRAV-SOURCE {book}: the manifest's time_stop_source {filed_source} is not the "
                   f"door's source {source}")
    return out


def va_pins_e_findings(reg_id: str, declared, builder_src: str, *, va_cols,
                       banned_prefix: str = VA_1W_PREFIX_T) -> list[str]:
    """F-VA-PINS [e · <registration>] — no registered construction, gate, licence or traverse reads
    a `1w_` column: proven on the registration spec's DECLARED VA reads and by an AST scan of its
    builder's source TEXT.  `va_cols` = the fixture's typed list of value-area column names.
    VA-PINS-1W: a `1w_` column on the declared list, or a string beginning `1w_` in the builder (an
    f-string's head included) · VA-PINS-UNDECLARED: the builder names a value-area column that is
    not on the registration's declared list."""
    declared = [str(c) for c in declared]
    out = []
    bad = sorted(c for c in declared if c.startswith(banned_prefix))
    if bad:
        out.append(f"VA-PINS-1W {reg_id}: the declared VA reads hold {bad}")
    strs = {n.value for n in ast.walk(ast.parse(builder_src))
            if isinstance(n, ast.Constant) and isinstance(n.value, str)}
    week = sorted(x for x in strs if x.startswith(banned_prefix))
    if week:
        out.append(f"VA-PINS-1W {reg_id}: the builder names {week}")
    und = sorted(x for x in strs if x in set(va_cols) and x not in declared
                 and not x.startswith(banned_prefix))
    if und:
        out.append(f"VA-PINS-UNDECLARED {reg_id}: the builder names value-area column(s) {und} that "
                   f"its registration does not declare")
    return out


# ═══════════════════════════════════════════════════════════════ SELF-TEST
# Everything below is the harness's own proof.  It runs only as __main__, prints its transcript to
# stdout and writes nothing to the tree (its scratch lives under $TMPDIR and is removed).  A plant
# is a sabotaged object swapped into the production call path (`_with`), or a mutated COPY of the
# data a detector reads; the comparators are never touched.
_SELF_MARK = "═ SELF-" + "TEST\n"                # the heading above, never this literal
_SELF_BANNER = ("TIER-C12 HARNESS SELF-TEST — scripts/tierc12_fx.py [L-0.14]: every leg state, the "
                "transcript law, and one planted mutation per law — break leg first, RED or void")
_SELF_REG = "P-SELF-1"
_SELF_NAME = "FIXTURES_SELF.txt"
# the self-test's typed commission (a second object: what the laws say, typed apart from the code)
_PRE_PAIR_T = ("as_of_last_closed_4h: (pre-substrate stage)", "substrate: none")
_GOOD_IDS_T = ("F-SCALP [a HAND-3]", "F-GATE [SET · P-ADM-1]", "F-KEY [stage_g]",
               "F-TRAV [e · P-SFP-VA-1__scored]", "F-TOLL [data a]", "F-LEDGER [PREFIX]",
               "F-NEST-ASOF [v6]", "F-DET", "F-D-2", "F-KEY [regbooks/P-SCALP-3]")
_BAD_IDS_T = ("F-GATE (P-ADM-1)", "F-GATE [a [b]]", "f-gate", "FGATE [x]", "F-GATE []",
              "F-GATE[P-ADM-1]", "F-GATE [a · b · c]", "F-GATE [ a]", "F-gate-x")
_TAGS_T = (("tierc12_va_fixtures", "va"), ("tierc12_stage_r_fixtures", "stage_r"),
           ("scripts/tierc12_scalp_fixtures.py", "scalp"), ("tierc12_tide_fixtures", "tide"))
_STATES_T = {"PASSED": ["F-SELF [a PASS]"],
             "FAILED": ["F-SELF [b FAIL]", "F-SELF [c VOID]", "F-SELF [d BREAK-RAISED]",
                        "F-SELF [e REAL-RAISED]", "F-SELF [f UNLISTED]", "F-SELF [g UNLISTED]"],
             "NOT_RUN": ["F-MIRROR"], "NOT_BUILT": ["F-GRID [SELF_GRID]"]}
_TALLY_T = "\n  1 GREEN, 6 RED, 1 NOT RUN"
_NOT_BUILT_T = "  1 NOT BUILT"


_REAL = {"prove": prove, "plants": plants, "file_transcript": file_transcript, "finish": finish,
         "hand_sample": hand_sample, "closed_status_findings": closed_status_findings}


def _with(name: str, obj, check):
    """Run `check` with the harness global `name` rebound to `obj` — a sabotage INSIDE the
    production call path; the binding is restored whatever happens."""
    g = globals()
    old = g[name]
    g[name] = obj
    try:
        return check()
    finally:
        g[name] = old


def _raise():
    raise RuntimeError("planted crash")


def _halt():
    raise SystemExit("HALT: pin moved")


def _red():
    return False, "the planted violation was found"


def _green():
    return True, "holds"


def _self_text() -> tuple[str, str]:
    """(the harness's own source above the self-test, the TC11 referee's source) — read as TEXT."""
    src = Path(__file__).read_text(encoding="utf-8")
    ref = (ROOT / "scripts" / "tierc11_closure_fixtures.py").read_text(encoding="utf-8")
    return src[:src.index(_SELF_MARK)], ref


def _mut(text: str, old: str, new: str) -> str:
    if text.count(old) != 1:
        raise RuntimeError(f"the plant's anchor occurs {text.count(old)} time(s), not once")
    return text.replace(old, new)


# ── [MIRROR] ──
def _mirror_findings(head: str, ref: str) -> list[str]:
    out = [f"FX-MIRROR {n}: ast.dump differs from the referee's" for n in MIRRORED_T
           if func_dump(head, n) != func_dump(ref, n)]
    tree = ast.parse(head)
    for n in ast.walk(tree):
        mods = ([a.name for a in n.names] if isinstance(n, ast.Import) else
                [n.module or ""] if isinstance(n, ast.ImportFrom) else [])
        for m in mods:
            if m.split(".")[0] not in sys.stdlib_module_names:
                out.append(f"FX-STDLIB: the harness imports {m}, outside the stdlib")
            if m.split(".")[0] == "subprocess":
                out.append("FX-CLOSURE: the harness imports subprocess (L-0.22 (iv): no subprocess "
                           "site in a non-fixture module)")
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) \
                and n.func.id in ("exec", "eval", "compile", "__import__"):
            out.append(f"FX-CLOSURE: the harness calls {n.func.id}(…) (L-0.22 (ii))")
    return out


def _mirror_break():
    head, ref = _self_text()
    return plants([
        ("`plants` in a harness copy changed to count a crash as a catch", "FX-MIRROR plants",
         lambda: _mirror_findings(_mut(head, "            crashed.append(f\"{name} -> RAISED "
                                             "{type(e).__name__}: {e}\")\n            continue\n",
                                       "            found = [want]\n"), ref)),
        ("`prove` in a harness copy changed to count a VOID leg GREEN", "FX-MIRROR prove",
         lambda: _mirror_findings(_mut(head, "    if b_ok:\n        FAILED.append(",
                                       "    if b_ok and not r_ok:\n        FAILED.append("), ref)),
        ("`file_transcript` in a harness copy changed to overwrite a differing record",
         "FX-MIRROR file_transcript",
         lambda: _mirror_findings(_mut(head, "    if out.exists() and not refile:\n",
                                       "    if out.exists() and not refile and not body:\n"), ref)),
        ("`import pandas` added to a harness copy", "FX-STDLIB",
         lambda: _mirror_findings(_mut(head, "import zlib\n", "import zlib\nimport pandas\n"), ref)),
        ("`import subprocess` added to a harness copy", "FX-CLOSURE",
         lambda: _mirror_findings(_mut(head, "import zlib\n", "import zlib\nimport subprocess\n"),
                                  ref)),
    ])


def _mirror_real():
    head, ref = _self_text()
    f = _mirror_findings(head, ref)
    shas = ", ".join(f"{n} {sha_bytes(func_dump(head, n).encode('utf-8'))[:12]}…" for n in MIRRORED_T)
    return (not f), (f"the {len(MIRRORED_T)} mirrored functions are AST-identical to the text of "
                     f"scripts/tierc11_closure_fixtures.py (node shas {shas}); every import of the "
                     f"harness is stdlib; no subprocess, exec, eval, compile or __import__ site"
                     + (f"; findings {f}" if f else ""))


# ── [STATES] ──
def _block_lines(lines: list, fid: str) -> list:
    """The transcript lines of one block: its header up to the next blank-led line."""
    j = next((i for i, x in enumerate(lines) if x.startswith(f"\n{fid} — ")), None)
    if j is None:
        return []
    end = next((i for i in range(j + 1, len(lines)) if lines[i].startswith("\n")), len(lines))
    return lines[j:end]


def _st_states() -> list[str]:
    with capture() as s:
        prove("F-SELF [a PASS]", "a leg that passes", "b", "r", _red, _green)
        prove("F-SELF [b FAIL]", "a real leg that fails", "b", "r", _red,
              lambda: (False, "the real leg found a mismatch"))
        prove("F-SELF [c VOID]", "a break leg that stays GREEN", "b", "r", _green, _green)
        prove("F-SELF [d BREAK-RAISED]", "a break leg that raises", "b", "r", _raise, _green)
        prove("F-SELF [e REAL-RAISED]", "a real leg that raises", "b", "r", _red, _raise)
        not_run("F-MIRROR", "the mirror drive", "the drive is unreachable")
        not_run("F-SELF [f UNLISTED]", "a leg that cannot run", "its input is absent")
        not_built("F-GRID [SELF_GRID]", "a Tier-E grid", "an empty frame")
        not_built("F-SELF [g UNLISTED]", "a registered table", "an empty frame")
        tally()
        got = summary()
    out = []
    fids = {k: [x.split(" (", 1)[0] for x in s[k]] for k in _STATES_T}
    if fids["PASSED"] != _STATES_T["PASSED"]:
        out.append(f"STATE-PASS: PASS holds {fids['PASSED']}, typed {_STATES_T['PASSED']}")
    for want in _STATES_T["FAILED"]:
        if want not in fids["FAILED"]:
            det = ("STATE-VOID" if "VOID" in want or "BREAK-RAISED" in want else
                   "STATE-NOT-RUN-LAW" if "[f " in want else
                   "STATE-NOT-BUILT-LAW" if "[g " in want else "STATE-FAIL")
            out.append(f"{det}: {want} is not RED (RED holds {fids['FAILED']})")
    if fids["NOT_RUN"] != _STATES_T["NOT_RUN"]:
        out.append(f"STATE-NOT-RUN: NOT RUN holds {fids['NOT_RUN']}, typed {_STATES_T['NOT_RUN']}")
    if fids["NOT_BUILT"] != _STATES_T["NOT_BUILT"]:
        out.append(f"STATE-NOT-BUILT: NOT BUILT holds {fids['NOT_BUILT']}, typed "
                   f"{_STATES_T['NOT_BUILT']}")
    if _TALLY_T not in s["LINES"] or _NOT_BUILT_T not in s["LINES"]:
        out.append(f"STATE-TALLY: the tally lines {_TALLY_T.strip()!r} / {_NOT_BUILT_T.strip()!r} "
                   f"are not in the transcript")
    if got["legs_total"] != sum(len(_STATES_T[k]) for k in ("PASSED", "FAILED", "NOT_RUN")) \
            or got["legs_not_run"] != len(_STATES_T["NOT_RUN"]) \
            or got["legs_not_built"] != len(_STATES_T["NOT_BUILT"]) or got["green"]:
        out.append(f"STATE-TALLY: summary() reads {got}")
    if _block_lines(s["LINES"], "F-MIRROR")[1:] != ["  [NOT RUN] F-MIRROR: the drive is unreachable"]:
        out.append("STATE-FORM: the NOT RUN block is not exactly its header and its [NOT RUN] line")
    for fid in ("F-SELF [a PASS]", "F-SELF [b FAIL]", "F-SELF [c VOID]"):
        blk = _block_lines(s["LINES"], fid)
        if sum("FAILS IF: " in x for x in blk) != 2 \
                or not blk[-1].startswith(("  [PASS] ", "  [FAIL] ")):
            out.append(f"STATE-FORM: the block of {fid} lacks a FAILS IF line or its verdict line")
    return out


def _sab_prove(fid, title, break_if, real_if, break_leg, real_leg):
    _REAL["prove"](fid, title, break_if, real_if, lambda: (False, "sabotage: every break RED"),
                   real_leg)


def _sab_not_run(fid, title, reason):
    say(f"\n{fid} — {title}")
    say(f"  [NOT RUN] {fid}: {reason}")
    PASSED.append(fid)


def _sab_not_built(fid, title, reason):
    say(f"\n{fid} — {title}")
    say(f"  [NOT BUILT] {fid}: {reason}")
    PASSED.append(fid)


def _sab_tally():
    say(f"\n  {len(PASSED)} GREEN, {len(FAILED)} RED")


def _states_break():
    return plants([
        ("`prove` swapped for one that counts every break leg RED (a VOID leg passes)",
         "STATE-VOID", lambda: _with("prove", _sab_prove, _st_states)),
        ("`not_run` swapped for one that files its block as PASS", "STATE-NOT-RUN: ",
         lambda: _with("not_run", _sab_not_run, _st_states)),
        ("NOT_RUN_FIDS_T widened by an unlisted block id", "STATE-NOT-RUN-LAW",
         lambda: _with("NOT_RUN_FIDS_T", NOT_RUN_FIDS_T + ("F-SELF [f UNLISTED]",), _st_states)),
        ("`not_built` swapped for one that files its block as PASS", "STATE-NOT-BUILT: ",
         lambda: _with("not_built", _sab_not_built, _st_states)),
        ("NOT_BUILT_FIDS_T widened to a registered table's FID", "STATE-NOT-BUILT-LAW",
         lambda: _with("NOT_BUILT_FIDS_T", NOT_BUILT_FIDS_T + ("F-SELF",), _st_states)),
        ("`tally` swapped for TC11's two-count line (no NOT RUN count)", "STATE-TALLY",
         lambda: _with("tally", _sab_tally, _st_states)),
    ])


def _states_real():
    f = _st_states()
    return (not f), (f"an inner session of {sum(len(v) for v in _STATES_T.values())} blocks reads "
                     f"PASS {_STATES_T['PASSED']}, RED {_STATES_T['FAILED']} (a FAIL, two VOID, a "
                     f"raised real leg, a refused NOT RUN, a refused NOT BUILT), NOT RUN "
                     f"{_STATES_T['NOT_RUN']}, NOT BUILT {_STATES_T['NOT_BUILT']}; tally "
                     f"{_TALLY_T.strip()!r} then {_NOT_BUILT_T.strip()!r}; legs_total counts PASS + "
                     f"RED + NOT RUN" + (f"; findings {f}" if f else ""))


# ── [PLANTS] ──
def _st_plants() -> list[str]:
    hit, other, none = (lambda: ["DET-X: found"]), (lambda: ["DET-Y: found"]), (lambda: [])
    cases = (("PLANTS-CAUGHT", "every plant caught by its named detector",
              [("p1", "DET-X", hit), ("p2", "DET-Y", other)], False),
             ("PLANTS-PASSED", "a plant that produced no finding",
              [("p1", "DET-X", hit), ("p2", "DET-X", none)], True),
             ("PLANTS-WRONG", "a plant caught by the wrong detector", [("p1", "DET-X", other)], True),
             ("PLANTS-CRASH", "a plant that crashed", [("p1", "DET-X", hit), ("p2", "DET-X", _raise)],
              True),
             ("PLANTS-HALT", "a HALT carrying its own text", [("p1", "HALT: pin moved", _halt)],
              False))
    out = []
    for det, label, rows, void in cases:
        b_ok, _ = plants(rows)
        if b_ok != void:
            out.append(f"{det}: {label} -> the break leg reads "
                       f"{'GREEN (VOID)' if b_ok else 'RED'}, the law says "
                       f"{'GREEN (VOID)' if void else 'RED'}")
    return out


def _sab_plants(how: str):
    def thunk_of(want, thunk):
        def run():
            try:
                found = thunk()
            except Exception:
                if how != "crash":
                    raise
                return [want]
            if how == "passed" and not found:
                return [want]
            if how == "wrong" and found:
                return [want]
            return found
        return run
    return lambda rows: _REAL["plants"]([(n, w, thunk_of(w, t)) for n, w, t in rows])


def _plants_break():
    return plants([
        ("`plants` swapped for one that counts a crash as a catch", "PLANTS-CRASH",
         lambda: _with("plants", _sab_plants("crash"), _st_plants)),
        ("`plants` swapped for one that counts no finding as a catch", "PLANTS-PASSED",
         lambda: _with("plants", _sab_plants("passed"), _st_plants)),
        ("`plants` swapped for one that accepts any detector's finding", "PLANTS-WRONG",
         lambda: _with("plants", _sab_plants("wrong"), _st_plants)),
    ])


def _plants_real():
    f = _st_plants()
    return (not f), ("five typed row sets judged one plant at a time: all caught -> RED; one plant "
                     "with no finding -> VOID; a finding from the wrong detector -> VOID; a crash "
                     "-> VOID (a fixture defect); a SystemExit -> a finding carrying its own text"
                     + (f"; findings {f}" if f else ""))


# ── [NO-CLOBBER] ──
def _session(n_legs: int, red: bool = False, bad_id: bool = False) -> None:
    header(_SELF_BANNER, seed=0)
    for i in range(n_legs):
        prove(f"F-SELF [LEG-{i}]", "a leg", "b", "r", _red, _green)
    if red:
        prove("F-SELF [RED]", "a failing leg", "b", "r", _red, lambda: (False, "mismatch"))
    if bad_id:
        prove("F-SELF (PAREN)", "a block id outside the grammar", "b", "r", _red, _green)


def _st_noclobber(tmp: Path) -> list[str]:
    root = Path(tempfile.mkdtemp(dir=tmp))
    rec = root / _SELF_NAME
    out = []
    with capture():
        _session(1)
        rc = finish(root, _SELF_NAME, [])
        body_a = transcript_bytes()
    if rc != 1 or sorted(p.name for p in root.iterdir()):
        out.append(f"CLOBBER-ABSENT: an absent transcript with no --refile-transcript -> exit {rc}, "
                   f"files {sorted(p.name for p in root.iterdir())} (the law: a finding, nothing written)")
    with capture():
        _session(1)
        rc = finish(root, _SELF_NAME, ["--refile-transcript"])
    if rc != 0 or not rec.exists() or rec.read_bytes() != body_a:
        out.append(f"CLOBBER-REFILE: --refile-transcript -> exit {rc}, record filed {rec.exists()}")
    with capture():
        _session(1)
        rc = finish(root, _SELF_NAME, [])
    if rc != 0 or sorted(p.name for p in root.iterdir()) != [_SELF_NAME]:
        out.append(f"CLOBBER-SILENT: identical bytes -> exit {rc}, files "
                   f"{sorted(p.name for p in root.iterdir())}")
    with capture():
        _session(2)
        rc = finish(root, _SELF_NAME, [])
        body_b = transcript_bytes()
    rr = root / _SELF_NAME.replace(".txt", "_rerun.txt")
    if rc != 1 or not rec.exists() or rec.read_bytes() != body_a or not rr.exists() \
            or rr.read_bytes() != body_b:
        out.append(f"CLOBBER-RECORD: different bytes without the flag -> exit {rc}, record "
                   f"untouched {rec.exists() and rec.read_bytes() == body_a}, _rerun filed "
                   f"{rr.exists()}")
    with capture():
        _session(2)
        rc = finish(root, _SELF_NAME, ["leg-0"])
    pp = root / _SELF_NAME.replace(".txt", "_partial.txt")
    if not pp.exists() or not rec.exists() or rec.read_bytes() != body_a:
        out.append(f"CLOBBER-PARTIAL: a leg-filtered run -> _partial filed {pp.exists()}, record "
                   f"untouched {rec.exists() and rec.read_bytes() == body_a}")
    red_root = Path(tempfile.mkdtemp(dir=tmp))
    with capture():
        _session(1, red=True)
        rc = finish(red_root, _SELF_NAME, ["--refile-transcript"])
    if rc != 1:
        out.append(f"EXIT-RED: a RED leg -> exit {rc}")
    with capture() as s:
        _session(1, bad_id=True)
        rc = finish(red_root, _SELF_NAME.replace("SELF", "SELF_ID"), ["--refile-transcript"])
    if rc != 1 or "F-SELF (PAREN)" in s["PASSED"]:
        out.append(f"EXIT-GRAMMAR: a block id outside the grammar -> exit {rc}, still PASS "
                   f"{'F-SELF (PAREN)' in s['PASSED']}")
    return out


def _sab_ft_absent(out: Path, body: bytes, refile: bool) -> list[str]:
    return _REAL["file_transcript"](out, body, True if not out.exists() else refile)


def _sab_ft_overwrite(out: Path, body: bytes, refile: bool) -> list[str]:
    return _REAL["file_transcript"](out, body, True)


def _sab_finish(root, transcript, args, t0=None) -> int:
    _REAL["finish"](root, transcript, args, t0)
    return 0


def _noclobber_legs(tmp: Path):
    def brk():
        return plants([
            ("`file_transcript` swapped for one that writes an absent record without the flag",
             "CLOBBER-ABSENT", lambda: _with("file_transcript", _sab_ft_absent,
                                             lambda: _st_noclobber(tmp))),
            ("`file_transcript` swapped for one that overwrites a differing record",
             "CLOBBER-RECORD", lambda: _with("file_transcript", _sab_ft_overwrite,
                                             lambda: _st_noclobber(tmp))),
            ("`finish` swapped for one that exits 0 whatever the tally", "EXIT-RED",
             lambda: _with("finish", _sab_finish, lambda: _st_noclobber(tmp))),
        ])

    def real():
        f = _st_noclobber(tmp)
        return (not f), ("in a scratch root: absent + no flag -> exit 1, nothing written; "
                         "--refile-transcript -> filed, exit 0; identical bytes -> silent, exit 0; "
                         "different bytes + no flag -> <stem>_rerun.txt, the record untouched, exit "
                         "1; a leg-filtered run -> <stem>_partial.txt, the record untouched; a RED "
                         "leg -> exit 1; a block id outside the grammar -> counted RED, exit 1"
                         + (f"; findings {f}" if f else ""))
    return brk, real


# ── [GRAMMAR] ──
def _st_grammar() -> list[str]:
    out = [f"GRAMMAR: refused the lawful block id {b!r}" for b in _GOOD_IDS_T if block_findings(b)]
    out += [f"GRAMMAR: admitted {b!r}" for b in _BAD_IDS_T if not block_findings(b)]
    built = (block_id("F-GATE", "SET", "P-ADM-1"), block_id("F-KEY", instance="stage_g"),
             block_id("F-SCALP", "a HAND-3"), block_id("F-DET"))
    if built != ("F-GATE [SET · P-ADM-1]", "F-KEY [stage_g]", "F-SCALP [a HAND-3]", "F-DET"):
        out.append(f"GRAMMAR: block_id builds {built}")
    try:
        parts = split_block("F-GATE [SET · P-ADM-1]")
    except ValueError:
        parts = None
    if parts != ("F-GATE", "SET · P-ADM-1") or fid_of("F-TOLL [data a]") != "F-TOLL":
        out.append("GRAMMAR: split_block / fid_of do not return the FID and the qualifier")
    return out


def _grammar_break():
    loose = re.compile(r"(?P<fid>F-[A-Z0-9]+(?:-[A-Z0-9]+)*)(?: [\[(](?P<q>[^\[\]]+)[\])])?")
    return plants([
        ("BLOCK_RX swapped for a pattern that admits a parenthesised qualifier",
         "GRAMMAR: admitted 'F-GATE (P-ADM-1)'", lambda: _with("BLOCK_RX", loose, _st_grammar)),
        ("QUAL_SEP swapped for a bare space (every word a part)", "GRAMMAR: refused",
         lambda: _with("QUAL_SEP", " ", _st_grammar)),
    ])


def _grammar_real():
    f = _st_grammar()
    return (not f), (f"{len(_GOOD_IDS_T)} typed lawful block ids admitted (the reading's seven "
                     f"examples among them), {len(_BAD_IDS_T)} typed unlawful ids refused "
                     f"{list(_BAD_IDS_T)}; block_id, split_block and fid_of agree"
                     + (f"; findings {f}" if f else ""))


# ── [HEADER] ──
def _st_header() -> list[str]:
    out = []
    with capture() as s:
        header(_SELF_BANNER, seed="SEED", typed=("X_T ('a', 'b')",))
    if tuple(s["LINES"][:2]) != _PRE_PAIR_T \
            or "seed SEED · substrate none · pin (pre-substrate stage)" not in s["LINES"] \
            or "  typed: X_T ('a', 'b')" not in s["LINES"]:
        out.append(f"HEADER-PRE: a pre-substrate header opens {s['LINES'][:2]}, not the fixed pair "
                   f"{list(_PRE_PAIR_T)} with its seed line")
    with capture() as s:
        header(_SELF_BANNER, seed="SEED", substrate="snap_x", as_of_iso="PIN-ISO", pin="PIN-MS")
    if s["LINES"][0] != "as_of_last_closed_4h: PIN-ISO" \
            or any(x in s["LINES"] for x in _PRE_PAIR_T) \
            or "seed SEED · substrate snap_x · pin PIN-MS" not in s["LINES"]:
        out.append(f"HEADER-PIN: a substrate header opens {s['LINES'][:1]} or carries the "
                   f"pre-substrate pair")
    with capture() as s:
        say("wrote /var/folders/zz/T/x.json and /private/tmp/y/z.txt")
        clock("wall of the run")
    if s["LINES"] != ["wrote <tmp> and <tmp>"]:
        out.append("HEADER-TMP: a temp path reached the transcript unscrubbed" if s["LINES"][:1]
                   != ["wrote <tmp> and <tmp>"] else
                   "HEADER-CLOCK: a clock line reached the transcript")
    return out


def _header_legs():
    def brk():
        return plants([
            ("PRE_SUBSTRATE_LINE swapped for a snapshot name", "HEADER-PRE",
             lambda: _with("PRE_SUBSTRATE_LINE", "substrate: tc12_snapshot", _st_header)),
            ("_TMP_RX swapped for a pattern that scrubs nothing", "HEADER-TMP",
             lambda: _with("_TMP_RX", re.compile(r"\A\Z never"), _st_header)),
            ("`clock` swapped for `say` (a clock line enters the transcript)", "HEADER-CLOCK",
             lambda: _with("clock", say, _st_header)),
        ])

    def real():
        f = _st_header()
        return (not f), (f"a pre-substrate header opens with the fixed pair {list(_PRE_PAIR_T)}; a "
                         f"substrate header opens with its pin ISO and never carries the pair; a "
                         f"temp path is scrubbed to <tmp>; a clock line stays on stdout"
                         + (f"; findings {f}" if f else ""))
    return brk, real


# ── [RNG] ──
class _StubRandom:
    def __init__(self):
        self.seen = None

    def default_rng(self, seed):
        self.seen = seed
        return self


class _StubNumpy:
    def __init__(self):
        self.random = _StubRandom()


def _st_rng(seed) -> list[str]:
    out = [f"RNG-TAG: suite_tag({a!r}) = {suite_tag(a)!r}, typed {b!r}" for a, b in _TAGS_T
           if suite_tag(a) != b]
    tag, blk = "va", "F-TRAV [e · P-SFP-VA-1__scored]"
    want = [seed, binascii.crc32(f"{tag}|{blk}".encode("utf-8"))]
    if stream_seed(seed, tag, blk) != want:
        out.append(f"RNG-SEED: stream_seed gives {stream_seed(seed, tag, blk)}, not [SEED, "
                   f"crc32('<suite tag>|<block id>')] = {want}")
    if stream_seed(seed, tag, blk) == stream_seed(seed, tag, "F-TRAV [a · tierc12_scalp]"):
        out.append("RNG-SEED: two block ids share one stream seed")
    np = _StubNumpy()
    stream(np, seed, tag, blk)
    if np.random.seen != want:
        out.append(f"RNG-STREAM: stream() seeds default_rng with {np.random.seen}, not {want}")
    return out


_RNG_DRAWS_T = 3            # the law is the FORM of a stream seed: proven on integer draws [L-0.2]


def _rng_legs():
    def st():
        return [x for draw in range(_RNG_DRAWS_T) for x in _st_rng(draw)]

    def brk():
        return plants([
            ("`stream_seed` swapped for one that hashes '<block id>|<suite tag>'", "RNG-SEED",
             lambda: _with("stream_seed", lambda s, t, b: [s, zlib.crc32(f"{b}|{t}".encode("utf-8"))],
                           st)),
            ("`suite_tag` swapped for the bare stem", "RNG-TAG",
             lambda: _with("suite_tag", lambda stem: Path(str(stem)).stem, st)),
            ("`stream` swapped for one seeded with the tier seed alone", "RNG-STREAM",
             lambda: _with("stream", lambda np, seed, t, b: np.random.default_rng([seed]), st)),
        ])

    def real():
        f = st()
        return (not f), (f"suite_tag strips `tierc12_` and `_fixtures` on {len(_TAGS_T)} typed "
                         f"stems; stream_seed == [SEED, crc32('<suite tag>|<block id>')] against "
                         f"binascii.crc32 (on the integer draws {list(range(_RNG_DRAWS_T))} in "
                         f"SEED's place; this leg takes no tier seed); two "
                         f"block ids give two seeds; stream() hands default_rng exactly that list"
                         + (f"; findings {f}" if f else ""))
    return brk, real


# ── [HAND-SAMPLE] ──
class _StubStream:
    def choice(self, n, size, replace):
        return list(range(n))[::-1][:size]


def _pop(*cats) -> list[dict]:
    return [{"k": i, "cat": c} for i, c in enumerate(cats)]


def _st_hand() -> list[str]:
    cats = tuple((c, (lambda r, c=c: r["cat"] == c)) for c in ("LONG", "SHORT", "STOP"))
    key = lambda r: r["k"]                                                    # noqa: E731
    out = []
    a = hand_sample(_pop("SHORT", "LONG", "LONG", "STOP", "SHORT", "STOP"), key=key, k=3,
                    categories=cats, rule="first row of LONG, SHORT, STOP in key order")
    if [(lab, r["k"]) for lab, r in a["chosen"]] != [("LONG", 1), ("SHORT", 0), ("STOP", 3)] \
            or a["findings"] or a["problems"]:
        out.append(f"HAND-FIRST: all categories present -> {[(x, r['k']) for x, r in a['chosen']]}")
    b = hand_sample(_pop("SHORT", "LONG", "LONG", "SHORT"), key=key, k=3, categories=cats,
                    contract_named=("STOP",))
    if [(lab, r["k"]) for lab, r in b["chosen"]] != [("LONG", 1), ("SHORT", 0),
                                                     ("FILL (slot of STOP)", 2)] \
            or not any(x.startswith("NONE-EXISTS STOP") for x in b["lines"]) \
            or not any(x.startswith("FINDING: the contract-named category STOP") for x in b["lines"]):
        out.append(f"HAND-FILL: an empty category -> {[(x, r['k']) for x, r in b['chosen']]}, "
                   f"lines {b['lines']}")
    if b["problems"]:
        out.append(f"HAND-SIZE-RED: an empty category made the leg RED: {b['problems']}")
    c = hand_sample(_pop("LONG", "SHORT"), key=key, k=3, categories=cats, n_asserted=2)
    if len(c["chosen"]) != 2 or "ONLY 2 EXIST (contract count 3)" not in c["lines"] \
            or not any(x.startswith("FINDING: the population holds 2") for x in c["lines"]):
        out.append(f"HAND-SHORT: n < k -> {len(c['chosen'])} chosen, lines {c['lines']}")
    if c["problems"]:
        out.append(f"HAND-SIZE-RED: a short population made the leg RED: {c['problems']}")
    d = hand_sample([], key=key, k=3, categories=cats, n_asserted=0)
    if d["chosen"] or "EMPTY POPULATION (contract count 3)" not in d["lines"]:
        out.append(f"HAND-EMPTY: n = 0 -> lines {d['lines']}")
    if d["problems"]:
        out.append(f"HAND-SIZE-RED: an empty population made the leg RED: {d['problems']}")
    e = hand_sample(_pop("LONG", "SHORT"), key=key, k=3, categories=cats, n_asserted=5)
    if not any(x.startswith("HAND-SAMPLE-COUNT") for x in e["problems"]):
        out.append("HAND-COUNT: a population that does not hold its record's count was accepted")
    f = hand_sample(_pop(*["LONG"] * 6), key=key, k=3, rng=_StubStream())
    g = hand_sample(_pop("LONG", "LONG"), key=key, k=3)
    if [r["k"] for _, r in f["chosen"]] != [3, 4, 5] or [r["k"] for _, r in g["chosen"]] != [0, 1]:
        out.append(f"HAND-DRAW: no categories -> {[r['k'] for _, r in f['chosen']]} / "
                   f"{[r['k'] for _, r in g['chosen']]}")
    return out


def _sab_hand(how: str):
    def run(rows, **kw):
        if how == "last":
            real_key = kw["key"]
            res = _REAL["hand_sample"](rows, **dict(kw, key=lambda r: -real_key(r)))
        elif how == "count":
            res = _REAL["hand_sample"](rows, **dict(kw, n_asserted=None))
        else:
            res = _REAL["hand_sample"](rows, **kw)
        if how == "nofill":
            res["chosen"] = [x for x in res["chosen"] if not x[0].startswith("FILL")]
        if how == "sizered" and res["n"] < res["k"]:
            res["problems"] = res["problems"] + ["HAND-SAMPLE-COUNT: too few rows"]
        return res
    return run


def _hand_break():
    return plants([
        ("`hand_sample` swapped for one that takes the LAST row of each category", "HAND-FIRST",
         lambda: _with("hand_sample", _sab_hand("last"), _st_hand)),
        ("`hand_sample` swapped for one that leaves an empty category's slot unfilled", "HAND-FILL",
         lambda: _with("hand_sample", _sab_hand("nofill"), _st_hand)),
        ("`hand_sample` swapped for one that is RED on a short population", "HAND-SIZE-RED",
         lambda: _with("hand_sample", _sab_hand("sizered"), _st_hand)),
        ("`hand_sample` swapped for one that never asserts the population's count", "HAND-COUNT",
         lambda: _with("hand_sample", _sab_hand("count"), _st_hand)),
    ])


def _hand_real():
    f = _st_hand()
    return (not f), ("seven typed populations: every category present -> its first row in key "
                     "order; an empty category -> NONE-EXISTS, its slot FILLed by the next unchosen "
                     "row, a FINDING when contract-named, never RED; n < k -> all n, `ONLY <n> "
                     "EXIST (contract count <k>)`, a FINDING, never RED; n = 0 -> `EMPTY "
                     "POPULATION`, never RED; a population that does not hold its record's count "
                     "-> HAND-SAMPLE-COUNT; no categories -> a seeded draw, all rows when n <= k"
                     + (f"; findings {f}" if f else ""))


# ── [CLOSED-NO-BOOK] ──
def _st_closed(tmp: Path) -> list[str]:
    d = Path(tempfile.mkdtemp(dir=tmp))
    closed = {"registration": _SELF_REG, "status": STATUS_CLOSED_T, "reason": "precondition unmet",
              "arms": []}
    out = []

    def filed(obj) -> Path:
        p = d / "STATUS.json"
        p.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return p

    ok, why = closed_real(filed(closed), _SELF_REG)
    if not ok or not why.startswith(f"CLOSED-NO-BOOK {_SELF_REG}"):
        out.append(f"CLOSED-OK: a closed STATUS reads {ok}: {why}")
    if closed_real(filed(dict(closed, status=STATUS_BUILT_T)), _SELF_REG)[0]:
        out.append("CLOSED-BUILT: a STATUS reading BUILT was accepted as CLOSED-NO-BOOK")
    if closed_real(filed(dict(closed, arms=["scored"])), _SELF_REG)[0]:
        out.append("CLOSED-ARMS: a STATUS listing an arm was accepted as CLOSED-NO-BOOK")
    if closed_real(filed(dict(closed, registration="P-OTHER-1")), _SELF_REG)[0]:
        out.append("CLOSED-ID: the STATUS of another registration was accepted")
    if plants(closed_plants(closed, _SELF_REG))[0]:
        out.append("CLOSED-PLANTS: the two standard plants are not both caught by CLOSED-STATUS")
    return out


def _closed_legs(tmp: Path):
    def keep(pred):
        return lambda status, reg_id: [x for x in _REAL["closed_status_findings"](status, reg_id)
                                       if pred(x)]

    def brk():
        return plants([
            ("`closed_status_findings` swapped for one that ignores a listed arm", "CLOSED-ARMS",
             lambda: _with("closed_status_findings", keep(lambda x: "lists arm" not in x),
                           lambda: _st_closed(tmp))),
            ("`closed_status_findings` swapped for one that ignores the status word",
             "CLOSED-BUILT",
             lambda: _with("closed_status_findings", keep(lambda x: "status reads" not in x),
                           lambda: _st_closed(tmp))),
        ])

    def real():
        f = _st_closed(tmp)
        ok, why = True, ""
        if not f:
            d = Path(tempfile.mkdtemp(dir=tmp)) / "STATUS.json"
            d.write_text(json.dumps({"registration": _SELF_REG, "status": STATUS_CLOSED_T,
                                     "reason": "precondition unmet", "arms": []}) + "\n",
                         encoding="utf-8")
            ok, why = closed_real(d, _SELF_REG)
        return (not f and ok), (f"{why} (a PASS, never NOT RUN); a STATUS copy reading BUILT, "
                                f"listing an arm or naming another registration is refused"
                                + (f"; findings {f}" if f else ""))
    return brk, real


# ── [DET] ──
_DET_FILES_T = ("DOC.md", "build_notes.json")


def _det_write(d: Path, extra: str = "") -> int:
    d.mkdir(parents=True, exist_ok=True)
    (d / "build_notes.json").write_text(
        json.dumps({"rows": 2, "stage": "SELF"}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (d / "DOC.md").write_text("# self\n\nline one\nline two\n" + extra, encoding="utf-8")
    return 0


def _det_setup(tmp: Path, seed) -> tuple[dict, dict]:
    base = Path(tempfile.mkdtemp(dir=tmp))
    _det_write(base)
    twins = det_twins(lambda d, s: _det_write(d), base, "SELF", seed)
    return ({lab: (rc, read_dir(d)) for lab, (rc, d) in twins.items()},
            {k: v for k, v in read_dir(base).items() if k in _DET_FILES_T})


def _det_legs(tmp: Path, seed):
    def bent(files: dict, name: str, new: bytes) -> dict:
        return dict(files, **{name: new})

    def brk():
        tw, canon = _det_setup(tmp, seed)
        (la, (_, fa)), (lb, (_, fb)) = tw.items()
        doc = bytearray(fb["DOC.md"])
        doc[len(doc) // 2] ^= 1
        clocked = bent(canon, "build_notes.json", (json.dumps(
            dict(json.loads(canon["build_notes.json"]), elapsed_s=1), indent=2, sort_keys=True)
            + "\n").encode("utf-8"))
        return plants([
            ("one byte bent in the second twin's copy of DOC.md", "DOC.md bytes differ",
             lambda: det_findings({la: (0, fa), lb: (0, bent(fb, "DOC.md", bytes(doc)))}, canon,
                                  _DET_FILES_T)),
            ("a line appended to the second twin's DOC.md (what a set-order line does)",
             f"DET-BYTES {la} vs {lb}",
             lambda: det_findings({la: (0, fa), lb: (0, bent(fb, "DOC.md", fb["DOC.md"]
                                                              + b"set order: b,a\n"))}, canon,
                                  _DET_FILES_T)),
            ("an `elapsed_s` key planted in every copy of build_notes.json", "DET-CLOCK",
             lambda: det_findings({la: (0, clocked), lb: (0, clocked)}, clocked, _DET_FILES_T)),
            ("one file deleted from a twin", "DET-FILESET",
             lambda: det_findings({la: (0, fa), lb: (0, {k: v for k, v in fb.items()
                                                         if k != "DOC.md"})}, canon, _DET_FILES_T)),
            ("a twin that exits 3", "DET-EXIT",
             lambda: det_findings({la: (0, fa), lb: (3, fb)}, canon, _DET_FILES_T)),
            ("a name listed under skipped_empty while the fixture counts a row in its frame",
             "DET-SKIPPED-EMPTY",
             lambda: det_file_set(("a.parquet", "b.parquet"), {"skipped_empty": ["b"]},
                                  {"b": 1})[1]),
            ("a regbook manifest that skips an empty arm", "DET-SKIPPED-EMPTY",
             lambda: det_file_set(("scored.parquet", "strip.parquet"), {"skipped_empty": ["strip"]},
                                  {"strip": 0}, skip_empty_law=False)[1]),
        ])

    def real():
        tw, canon = _det_setup(tmp, seed)
        f = det_findings(tw, canon, _DET_FILES_T)
        exp, g = det_file_set(("a.parquet", "b.parquet"), {"skipped_empty": ["b"]}, {"b": 0})
        if exp != ["a.parquet"] or g:
            f.append(f"DET-SKIPPED-EMPTY: a lawfully skipped empty table -> {exp}, {g}")
        if tuple(tw) != tuple(f"seed {s}" for s in (HASHSEED_FIRST_T, str(seed))):
            f.append(f"DET-SEEDS: the twins are labelled {list(tw)}")
        return (not f), (f"two twins of a stdlib writer under the labels {list(tw)} (PYTHONHASHSEED "
                         f"\"1\" and the tier seed; here launched in-process — the calling suite "
                         f"owns the subprocess) and the canonical directory: file set == typed "
                         f"{list(_DET_FILES_T)}, every file byte-identical, no clock-like key; the "
                         f"skip-empty law drops a table the fixture counts empty"
                         + (f"; findings {f}" if f else ""))
    return brk, real


# ── [DOCS] ──
_AXES_T = {"age": ("on", "off"), "win": ("on", "off")}
_CELLS_T = ("age:on¦win:on", "age:on¦win:off", "age:off¦win:on", "age:off¦win:off")


_LITERALS_T = ('M_NOTE = "m"\nCOLLAR = {"tier": "TIER-E", "gates": "nothing", "m_note": M_NOTE}\n'
               'COLLAR_COLS = ("tier", "gates")\n')


def _doc(cells=_CELLS_T, n=None, collar: bool = True, marker: str = "") -> str:
    rows = "".join(f"| {c} | 0 |\n" for c in cells)
    return ("# stage\n\n" + (COLLAR_LINE + "\n" if collar else "") + marker
            + f"<!-- grid: G_SELF cells={len(_CELLS_T) if n is None else n} -->\n"
            + "| cell | n |\n|---|---|\n" + rows + "\nend\n")


def _st_docs() -> list[str]:
    out = []
    if tuple(grid_cells(_AXES_T)) != _CELLS_T or grid_count(_AXES_T) != len(_CELLS_T):
        out.append(f"GRID-CELLS: grid_cells / grid_count give {grid_cells(_AXES_T)} / "
                   f"{grid_count(_AXES_T)}")
    good = _doc()
    out += grid_printed_findings(good, "G_SELF", _CELLS_T)
    out += collar_doc_findings("doc", good, registered_marker_ok=False)
    out += collar_doc_findings("score doc", _doc(collar=False, marker="<!-- registered: P-SELF-1 -->\n"),
                               registered_marker_ok=True)
    out += grid_pointer_findings("G_SELF", {"path": "stage.md", "sha256": sha_bytes(good.encode("utf-8")),
                                            "cells": len(_CELLS_T)}, good.encode("utf-8"), _CELLS_T)
    out += collar_leaf_findings("leaf", {"lo": 0, "rows": [{"would_read_ci_only": "no interval"}]})
    try:
        whole = literal_from_text(_LITERALS_T, "COLLAR")
    except ValueError:
        whole = None
    if literal_from_text(_LITERALS_T, "COLLAR_COLS") != ("tier", "gates") \
            or literal_from_text(_LITERALS_T, "COLLAR", key="gates") != "nothing" or whole is not None:
        out.append("TEXT-LITERAL: literal_from_text does not read a tuple, or one keyed value of a "
                   "dict display that holds a name, from source text")
    return out


def _docs_break():
    good = _doc()
    ptr = {"path": "stage.md", "sha256": sha_bytes(good.encode("utf-8")), "cells": len(_CELLS_T)}
    cut = _doc(cells=_CELLS_T[:-1])
    return plants([
        ("a printed table with one row deleted", "GRID-PRINTED",
         lambda: grid_printed_findings(cut, "G_SELF", _CELLS_T)),
        ("a grid marker whose count is not the parquet's", "GRID-PRINTED",
         lambda: grid_printed_findings(_doc(n=len(_CELLS_T) - 1), "G_SELF", _CELLS_T)),
        ("a pointer row whose stage document has that grid truncated", "GRID-POINTER",
         lambda: grid_pointer_findings("G_SELF", dict(ptr, sha256=sha_bytes(cut.encode("utf-8"))),
                                       cut.encode("utf-8"), _CELLS_T)),
        ("a pointer row carrying another sha", "GRID-POINTER",
         lambda: grid_pointer_findings("G_SELF", dict(ptr, sha256=sha_bytes(b"other")),
                                       good.encode("utf-8"), _CELLS_T)),
        ("a document table with its collar line deleted", "COLLAR-DOC",
         lambda: collar_doc_findings("doc", _doc(collar=False), registered_marker_ok=False)),
        ("the registered marker placed above a table of a document where it is not allowed",
         "COLLAR-MARKER",
         lambda: collar_doc_findings("doc", _doc(marker="<!-- registered: P-SELF-1 -->\n"),
                                     registered_marker_ok=False)),
        ("a `clears_literal_bar` key added to a collared leaf", "COLLAR-NAME",
         lambda: collar_leaf_findings("leaf", {"rows": [{"clears_literal_bar": True}]})),
        ("a verdict word in a collared leaf", "COLLAR-WORD",
         lambda: collar_leaf_findings("leaf", {"reading": "SUPPORTED"},
                                      verdict_words=("SUPPORTED",))),
        ("`literal_from_text` swapped for one that returns the first literal it meets",
         "TEXT-LITERAL", lambda: _with("literal_from_text", lambda text, name, key=None: "m",
                                       _st_docs)),
    ])


def _docs_real():
    f = _st_docs()
    return (not f), (f"grid_cells of the typed axes == the typed {len(_CELLS_T)} cells in axis "
                     f"order; a document printing that grid whole under its marker and its collar "
                     f"line is clean; a registered marker is clean where it is allowed; a pointer "
                     f"row with the document's sha and cell count is clean; a collared leaf with no "
                     f"forbidden key is clean; literal_from_text reads a tuple and one keyed value "
                     f"of a dict display from source text and refuses the dict as a whole when it "
                     f"holds a name" + (f"; findings {f}" if f else ""))


# ── [TRAV] ──
_VA_COLS_T = ("1h_state", "1h_val", "1h_vah", "4h_state", "1w_state", "1w_val")
_BUILDER_T = (
    "def build(E, R):\n"
    "    T, source = R.traverse('traverse.1h')\n"
    "    T5 = T * (E.LENS_MS['1h'] // E.LENS_MS['5m'])\n"
    "    rows = R.stamps(['1h_state', '1h_val'])\n"
    "    return walk(rows, time_stop=T, T_5m=T5), source\n")
_SOURCE_T = {"path": "va/TRAVERSE.json", "key": "by_lens.1h.T_of_record", "sha256": "ab", "value": 9}


def _st_trav() -> list[str]:
    out = trav_ast_findings("consumer", _BUILDER_T)
    out += trav_book_findings("book", [_SOURCE_T["value"]] * 3, dict(_SOURCE_T), _SOURCE_T["value"],
                              _SOURCE_T)
    out += va_pins_e_findings(_SELF_REG, ("1h_state", "1h_val"), _BUILDER_T, va_cols=_VA_COLS_T)
    return out


def _trav_break():
    v = _SOURCE_T["value"]
    return plants([
        ("`time_stop = <an integer>` typed in a copy of a consumer", "TRAV-TYPED",
         lambda: trav_ast_findings("consumer", _mut(_BUILDER_T, "time_stop=T,", "time_stop=12,"))),
        ("a T name assigned an integer in a copy of a consumer", "TRAV-TYPED",
         lambda: trav_ast_findings("consumer", _BUILDER_T + "T_1h = 12\n")),
        ("a typed 12 as the 5m factor", "TRAV-TYPED",
         lambda: trav_ast_findings("consumer", _mut(
             _BUILDER_T, "(E.LENS_MS['1h'] // E.LENS_MS['5m'])", "12"))),
        ("the 5m factor read from a name that is not the LENS_MS quotient", "TRAV-FACTOR",
         lambda: trav_ast_findings("consumer", _mut(
             _BUILDER_T, "(E.LENS_MS['1h'] // E.LENS_MS['5m'])", "FACTOR"))),
        ("a typed default `def walk(rows, time_stop=12)`", "TRAV-TYPED",
         lambda: trav_ast_findings("consumer", _BUILDER_T
                                   + "def walk(rows, time_stop=12, T_5m=None):\n    return rows\n")),
        ("one trade row's T changed in a copy of a range book", "TRAV-ROW",
         lambda: trav_book_findings("book", [v, v + 1, v], dict(_SOURCE_T), v, _SOURCE_T)),
        ("a manifest copy whose time_stop_source carries another sha", "TRAV-SOURCE",
         lambda: trav_book_findings("book", [v, v], dict(_SOURCE_T, sha256="cd"), v, _SOURCE_T)),
        ("a copy of a registered arm's spec that reads `1w_state`", "VA-PINS-1W",
         lambda: va_pins_e_findings(_SELF_REG, ("1h_state", "1h_val", "1w_state"), _BUILDER_T,
                                    va_cols=_VA_COLS_T)),
        ("a `1w_` column read in a copy of the builder", "VA-PINS-1W",
         lambda: va_pins_e_findings(_SELF_REG, ("1h_state", "1h_val"),
                                    _mut(_BUILDER_T, "'1h_val']", "'1h_val', '1w_val']"),
                                    va_cols=_VA_COLS_T)),
        ("an undeclared value-area column read in a copy of the builder", "VA-PINS-UNDECLARED",
         lambda: va_pins_e_findings(_SELF_REG, ("1h_state", "1h_val"),
                                    _mut(_BUILDER_T, "'1h_val']", "'1h_val', '4h_state']"),
                                    va_cols=_VA_COLS_T)),
    ])


def _trav_real():
    f = _st_trav()
    return (not f), ("a typed consumer text that takes T from the reader's traverse door, builds "
                     "its 5m count with the LENS_MS quotient and names only declared 1h columns is "
                     "clean under trav_ast_findings and va_pins_e_findings; a book whose every row "
                     "carries the door's value and whose manifest files the door's source is clean "
                     "under trav_book_findings" + (f"; findings {f}" if f else ""))


def _self_test() -> int:
    seed = json.loads((ROOT / "research_outputs" / "tierc12" / "PROGRESS.json")
                      .read_text(encoding="utf-8"))["seed"]
    tmp = Path(tempfile.mkdtemp(prefix="tierc12_fx_self_"))
    try:
        reset()
        header(_SELF_BANNER, seed=seed, typed=(
            f"MIRRORED_T {list(MIRRORED_T)}",
            f"NOT_RUN_FIDS_T {list(NOT_RUN_FIDS_T)} · NOT_BUILT_FIDS_T {list(NOT_BUILT_FIDS_T)}",
            f"states {_STATES_T}",
            f"block ids lawful {list(_GOOD_IDS_T)}",
            f"block ids unlawful {list(_BAD_IDS_T)}",
            f"suite tags {list(_TAGS_T)}",
            f"grid axes {_AXES_T} · cells {list(_CELLS_T)} · F-DET file set {list(_DET_FILES_T)}",
            f"VA columns {list(_VA_COLS_T)} · door source {_SOURCE_T}",
            "NOT EXERCISED HERE (they take pandas and the shim as arguments; the harness may "
            "import neither): grid_findings, collar_table_findings, key_findings, stamp_findings, "
            "key_dir_findings, det_dir_findings and the parquet branches of det_findings / "
            "clock_findings — proven by the tables suite's helper mirrors at TC12-ENV"))
        nb, nr = _noclobber_legs(tmp)
        hb, hr = _header_legs()
        rb, rr = _rng_legs()
        cb, cr = _closed_legs(tmp)
        db, dr = _det_legs(tmp, seed)
        for row in (
            ("F-FX-SELF [MIRROR]", "the five mirrored functions are the referee's; stdlib only",
             "a harness copy whose plants, prove or file_transcript differs from the referee, or "
             "that imports pandas or subprocess, is not found",
             "ast.dump of say, clock, prove, plants or file_transcript differs from the same "
             "function parsed from the TEXT of scripts/tierc11_closure_fixtures.py; the harness "
             "imports a module outside the stdlib, imports subprocess, or calls exec / eval / "
             "compile / __import__", _mirror_break, _mirror_real),
            ("F-FX-SELF [STATES]", "PASS · FAIL · VOID · NOT RUN · NOT BUILT, and the tally",
             "a harness that passes a VOID leg, files NOT RUN or NOT BUILT as PASS, admits either "
             "for an unlisted block, or drops the NOT RUN count from the tally is not found",
             "an inner session's PASS / RED / NOT RUN / NOT BUILT lists differ from the typed "
             "ones; a VOID leg, a raised leg, an unlisted NOT RUN or an unlisted NOT BUILT is not "
             "RED; the tally is not `  N GREEN, M RED, K NOT RUN` with NOT BUILT counted beside; "
             "summary() disagrees; a block lacks a FAILS IF line", _states_break, _states_real),
            ("F-FX-SELF [PLANTS]", "plants are judged one at a time, by their named detector",
             "a `plants` that counts a crash, a silent plant or the wrong detector as a catch is "
             "not found",
             "a row set with a silent plant, a wrong-detector finding or a crash is RED; a row set "
             "wholly caught, or a SystemExit carrying the detector's text, is VOID",
             _plants_break, _plants_real),
            ("F-FX-SELF [NO-CLOBBER]", "the transcript of record is never clobbered; exit codes",
             "a file_transcript that writes an absent record or overwrites a differing one, or a "
             "finish that exits 0 on a RED leg, is not found",
             "an absent transcript is written without --refile-transcript; a differing run "
             "overwrites the record or files no _rerun; a leg-filtered run touches the record or "
             "files no _partial; identical bytes are not silent; a RED leg or a block id outside "
             "the grammar exits 0", nb, nr),
            ("F-FX-SELF [GRAMMAR]", "the block id grammar",
             "a grammar that admits a parenthesised qualifier, or refuses a lawful two-part "
             "qualifier, is not found",
             "a typed lawful block id is refused, a typed unlawful one is admitted, or block_id / "
             "split_block / fid_of disagree with the grammar", _grammar_break, _grammar_real),
            ("F-FX-SELF [HEADER]", "the pre-substrate pair, the pin line, no temp path, no clock",
             "a header without the fixed `substrate: none` line, an unscrubbed temp path or a "
             "clock line in the transcript is not found",
             "a pre-substrate header does not open with the fixed pair; a substrate header does "
             "not open with its pin ISO or carries the pair; a temp path or a clock line reaches "
             "the transcript", hb, hr),
            ("F-FX-SELF [RNG]", "the fixture stream seed [SEED, crc32('<suite tag>|<block id>')]",
             "a stream seeded on another string, another tag or the tier seed alone is not found",
             "suite_tag does not strip `tierc12_` / `_fixtures`; stream_seed differs from [SEED, "
             "binascii.crc32('<suite tag>|<block id>')]; two block ids share a seed; stream() "
             "hands default_rng anything else", rb, rr),
            ("F-FX-SELF [HAND-SAMPLE]", "the one hand-sample law",
             "a sampler that takes another row than a category's first, leaves a slot unfilled, "
             "goes RED on a short population or never asserts the count is not found",
             "the chosen rows differ from the typed ones on a typed population; an empty category "
             "prints no NONE-EXISTS / FILL; a short or empty population prints no ONLY <n> EXIST / "
             "EMPTY POPULATION or is RED; a population not holding its record's count is accepted",
             _hand_break, _hand_real),
            ("F-FX-SELF [CLOSED-NO-BOOK]", "a real-book leg on a row closed by precondition",
             "a STATUS check that ignores a listed arm or the status word is not found",
             "a STATUS.json saying CLOSED_BY_PRECONDITION with no arm does not PASS with "
             "`CLOSED-NO-BOOK <id>`; a STATUS reading BUILT, listing an arm or naming another "
             "registration is accepted; the two standard plants are not caught by CLOSED-STATUS",
             cb, cr),
            ("F-FX-SELF [DET]", "F-DET's comparison of two twins and the canonical directory",
             "a bent byte, a twin-to-twin difference, a clock-like key, a missing file, a non-zero "
             "exit or a false skipped_empty entry is not found",
             "two twins of one writer and its canonical directory are reported different, or the "
             "skip-empty law does not drop a table the fixture counts empty", db, dr),
            ("F-FX-SELF [DOCS]", "a grid printed whole, the pointer row, the collar in documents, "
             "literals read from text",
             "a truncated printed grid, a false marker count, a false pointer row, a table with no "
             "collar line, a misplaced registered marker, a forbidden key in a leaf or a text "
             "reader returning the wrong literal is not found",
             "grid_cells is not the product of the typed axes in axis order; a clean document, "
             "pointer row or leaf is reported; literal_from_text misreads a literal from source "
             "text", _docs_break, _docs_real),
            ("F-FX-SELF [TRAV]", "L-V's helper legs: F-TRAV [a], [e] and F-VA-PINS [e]",
             "a typed time stop, a typed 5m factor, a row's T moved, a false time_stop_source, a "
             "`1w_` read or an undeclared value-area read is not found",
             "a consumer text with no typed time stop, a book carrying the door's T and source, or "
             "a builder naming only its declared value-area columns is reported",
             _trav_break, _trav_real),
        ):
            run_leg(row)
        for b in blocks():
            if block_findings(b):
                FAILED.append(f"{b} (block id outside the grammar of L-0.14 B)")
        tally()
        clock(f"transcript sha {sha_bytes(transcript_bytes())} (stdout only; nothing filed)")
        if FAILED:
            print("*** HALT: fixture mismatch. Nothing downstream is trustworthy. ***")
        return 1 if FAILED else 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(_self_test())
