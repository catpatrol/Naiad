#!/usr/bin/env python
"""TIER-C11 · STAGE TC11-D — the corridor's fixtures (scripts/tierc11_data.py).

TWO LEGS PER FIXTURE, the BREAK leg first, and it must go RED or the fixture
is VOID — a guard nobody has seen fail is a guard nobody has seen [the prove()
law of scripts/tierc10_rf_fixtures.py / tierc10_resume_fixtures.py].  Every
plant is made on a COPY (a dict, a frame, a temp file); no real artifact moves.
A plant that CRASHES is a fixture defect, never a catch (hardened plants()).
  F-D11-GUARD     FAILS IF the substrate guard accepts an unset variable, the live
                  cache, a directory inside it, the TC10 snapshot, a foreign
                  directory, or a TC11 path without klines/.
  F-D11-PORT      FAILS IF a port labelled VERBATIM is not AST-identical to its
                  source function in scripts/tierc10_data.py, a provenance comment
                  names the wrong lines or sha, or a label lies.
  F-D11-CLONE     FAILS IF any cloned pre-existing file's content up to its TC10
                  edge differs from the TC10 snapshot's bytes that re-hash to TC10's
                  manifest, or any untouched file's bytes differ from TC10's
                  manifest.  SABOTAGE: a flipped byte in a temp copy.
  F-D11-PIN       FAILS IF the filed pin is not 2026-09-25T00:00:00Z, not a 4h close,
                  not closed by the venue record in the file, or write-once lets a
                  rewrite through.  SABOTAGE: a pin that is not a 4h close.
  F-D11-PREFIX    FAILS IF any row that existed in PRE_STATE is not byte-identical
                  after the fetch.  SABOTAGE: a modified historical row in a temp copy.
  F-D11-EDGE      FAILS IF any lens of any asset does not end exactly at its last
                  bar closing <= the pin, has a gap, a duplicate or a row past the pin,
                  or a funding tape stops short of the pin's hour.  SABOTAGE: a
                  dropped bar.
  F-D11-DERIVE    FAILS IF 1d / 1w recomputed from native 4h by a plain loop differ
                  by one bit from the derived files.  SABOTAGE: a shifted week anchor.
  F-DET           FAILS IF two subprocess manifest builds (PYTHONHASHSEED 1 and
                  20260924) differ by one byte from each other or from the filed
                  bytes, or carry a clock field.
  F-D11-UNTOUCHED FAILS IF the TC10 snapshot does not re-hash to TC10's manifest
                  after the build, or the live cache MANIFEST.json's stat (size,
                  mtime, inode) moved across this run — stat ONLY, never opened.
BANNED: self-comparison; one example where cardinality was possible; a tuned
magnitude bound standing in for an identity; a check whose claim is not the
design's claim.  FROZEN SUBSTRATE: HALTs unless NAIAD_CACHE_DIR is the TC11
snapshot.  Seed 20260924.  The transcript carries no clock and no temp path.

Run:  export NAIAD_CACHE_DIR=$HOME/.cache/naiad/snapshots/tc11_20260925 PYTHONDONTWRITEBYTECODE=1
      ~/venvs/naiad/bin/python -B scripts/tierc11_data_fixtures.py \\
          [leg-substring ...] [--refile-transcript] [--root=DIR]
Exit 0 = every leg GREEN, every break RED · 1 = a RED or VOID fixture, a transcript
finding, or a HALT (SystemExit carries the reason).
"""
from __future__ import annotations

import ast
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from contextlib import contextmanager
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
import tierc11_data as D            # noqa: E402  its import-time guard HALTs off the TC11 snapshot
import numpy as np                  # noqa: E402
import pandas as pd                 # noqa: E402

SEED = 20260924
DET_SEEDS = (1, SEED)
OUT = D.OUT
RUN_ROOT = OUT                      # --root=DIR redirects transcript + F-DET twins
TRANSCRIPT = "FIXTURES_DATA.txt"
DET_FILES = ("STAGE_D_MANIFEST.json", "fee_schedule.json", "STAGE_D_MANIFEST.md")
AS_OF_LINE = "as_of_last_closed_4h: 2026-09-25T00:00:00Z"
# FIXTURE-TYPED second objects (never the module's own constants)
PIN_MS = 1_790_294_400_000
PIN_ISO = "2026-09-25T00:00:00Z"
STEP = {"5m": 300_000, "15m": 900_000, "1h": 3_600_000, "4h": 14_400_000,
        "12h": 43_200_000, "1d": 86_400_000, "1w": 604_800_000}
DAY, WEEK, MONDAY = 86_400_000, 604_800_000, 4 * 86_400_000     # 1970-01-05 was a Monday
LIVE_MANIFEST = D.LIVE_CACHE / "MANIFEST.json"                  # os.stat ONLY — never opened
CLOCK_FIELD = re.compile(r'"[^"]*(elapsed|wall_clock|perf_counter|_at_run|run_started)[^"]*"\s*:')
TMP_RX = re.compile(r"[^\s'\"]*f-d11-[A-Za-z0-9_]+")
LINES: list[str] = []
PASSED: list[str] = []
FAILED: list[str] = []
TALLY = {"break_red": 0, "break_void": 0, "real_green": 0, "real_red": 0}


def _norm(s: str) -> str:
    return TMP_RX.sub("<tmp>", s)


def say(line: str = "") -> None:            # deterministic -> transcript
    line = _norm(line)
    print(line)
    LINES.append(line)


def clock(line: str) -> None:               # wall clock, temp paths -> stdout ONLY
    print(f"  [clock · stdout only] {line}")


def prove(fid: str, title: str, fails_if: str, break_leg, real_leg) -> None:
    """Break first; it must go RED (ok False) or the fixture is VOID."""
    say(f"\n{fid} — {title}")
    say(f"  FAILS IF: {fails_if}")
    try:
        b_ok, b_why = break_leg()
    except Exception as e:                  # a break leg that errors proved nothing
        b_ok, b_why = True, f"break leg RAISED {type(e).__name__}: {e}"
    say(f"  [BREAK] deliberate violation -> "
        f"{'RED (correct)' if not b_ok else 'GREEN (FIXTURE IS VOID)'}: {b_why}")
    try:
        r_ok, r_why = real_leg()
    except SystemExit as e:                 # a HALT inside a real leg is a FAIL
        r_ok, r_why = False, f"HALT: {e}"
    except Exception as e:                  # a real leg that errors is a FAIL
        r_ok, r_why = False, f"raised {type(e).__name__}: {e}"
    say(f"  [{'PASS' if r_ok else 'FAIL'}] {fid}: {r_why}")
    TALLY["break_void" if b_ok else "break_red"] += 1
    TALLY["real_green" if r_ok else "real_red"] += 1
    if b_ok:
        FAILED.append(f"{fid} (break leg did not go RED — fixture proves nothing)")
    elif not r_ok:
        FAILED.append(fid)
    else:
        PASSED.append(fid)


# copied from scripts/tierc10_resume_fixtures.py:946-974 (hardened: a crash is a defect)
def plants(rows) -> tuple[bool, str]:
    passed, caught, crashed = [], [], []
    for name, thunk in rows:
        try:
            found = thunk()
        except SystemExit as e:             # a HALT is a finding, and the best kind
            found = [f"HALT: {e}"]
        except Exception as e:              # a CRASH proves nothing about the guard
            crashed.append(f"{name} -> RAISED {e.__class__.__name__}: {e}")
            continue
        (caught if found else passed).append(
            f"{name} -> {_norm(str(found[0]))[:150]}" if found else name)
    if crashed:
        return True, (f"{len(crashed)} plant(s) CRASHED instead of being CAUGHT — an "
                      f"unexpected exception is a FIXTURE DEFECT, not a finding: "
                      + " · ".join(crashed))
    if passed:
        return True, f"{len(passed)} plant(s) PASSED: {passed}"
    return False, (f"all {len(caught)} plants caught, one at a time: "
                   + " · ".join(caught))


@contextmanager
def mutated(obj, name: str, value):
    old = getattr(obj, name)
    setattr(obj, name, value)
    try:
        yield
    finally:
        setattr(obj, name, old)


def tmpdir() -> tempfile.TemporaryDirectory:
    return tempfile.TemporaryDirectory(prefix="f-d11-")


def read_json(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def tc10_expected() -> dict[str, str]:
    """rel -> sha256 from TC10's STAGE_D_MANIFEST.json, read here independently."""
    m = read_json(D.TC10_MANIFEST)
    exp = {f["path"]: f["sha256"] for f in m["files"] if f.get("present")}
    exp.update({o["path"]: o["sha256"] for o in m["out_of_scope_snapshot_files"]})
    return exp


def tree(root: Path) -> list[str]:
    return sorted(q.relative_to(root).as_posix() for q in root.rglob("*") if q.is_file())


def colset(rel: str) -> tuple[str, list[str]]:
    return (("open_time", D.KLINE_COLS) if rel.startswith("klines/")
            else ("funding_time", D.FUNDING_COLS))


def flip_byte_copy(src: Path, dst_dir: Path, rel: str) -> Path:
    q = dst_dir / rel
    q.parent.mkdir(parents=True, exist_ok=True)
    b = bytearray(src.read_bytes())
    b[len(b) // 2] ^= 0xFF
    q.write_bytes(bytes(b))
    return q


def frame_copy(df: pd.DataFrame, dst_dir: Path, rel: str) -> Path:
    q = dst_dir / rel
    q.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(q, index=False)
    return q


# ═══════════════════════════════════════════════ F-D11-GUARD
def guard_break():
    def halt(env):
        def t():
            D.guard_substrate(env)
            return []
        return t
    with tmpdir() as tmp:
        foreign = Path(tmp) / "foreign"
        (foreign / "klines").mkdir(parents=True)
        bare = Path(tmp) / "bare"
        bare.mkdir()

        def no_klines():
            with mutated(D, "SNAPSHOT", bare):
                D.guard_substrate(str(bare))
            return []
        return plants([("unset", halt(None)), ("empty string", halt("")),
                       ("the live cache (path string)", halt(str(D.LIVE_CACHE))),
                       ("a directory inside the live cache", halt(str(D.LIVE_CACHE / "klines"))),
                       ("the TC10 snapshot", halt(str(D.TC10_SNAPSHOT))),
                       ("a foreign directory holding klines/", halt(str(foreign))),
                       ("the snapshot of record with no klines/", no_klines)])


def guard_real():
    got = D.guard_substrate(os.environ.get("NAIAD_CACHE_DIR"))
    bound = Path(D.ED.cache_dir()).resolve()
    ok = got == D.SNAPSHOT.resolve() == bound and D.SNAPSHOT.name == "tc11_20260925"
    return ok, (f"NAIAD_CACHE_DIR resolves to {got.name}; engine.data.cache_dir() -> {bound.name}; "
                f"klines/ present: {(got / 'klines').is_dir()}")


# ═══════════════════════════════════════════════ F-D11-PORT
PROV_RX = re.compile(r"^# ported from scripts/tierc10_data\.py:(\d+)-(\d+) @ sha256 "
                     r"([0-9a-f]{16}) — (VERBATIM|CHANGED)")


def port_findings(my_src: str, tc10_src: str) -> tuple[list[str], dict]:
    mine = {n.name: n for n in ast.parse(my_src).body if isinstance(n, ast.FunctionDef)}
    theirs = {n.name: n for n in ast.parse(tc10_src).body if isinstance(n, ast.FunctionDef)}
    lines = my_src.splitlines()
    bad, st = [], {"VERBATIM": 0, "CHANGED": 0}
    for name, why in sorted(D.PORTS.items()):
        if name not in mine or name not in theirs:
            bad.append(f"{name}: missing ({'here' if name not in mine else 'in tierc10_data'})")
            continue
        m, t = mine[name], theirs[name]
        prov = None
        for k in range(m.lineno - 2, max(m.lineno - 6, -1), -1):
            prov = PROV_RX.match(lines[k])
            if prov:
                break
        if prov is None:
            bad.append(f"{name}: no provenance comment above its def")
            continue
        a, b, sha16, label = int(prov[1]), int(prov[2]), prov[3], prov[4]
        want = "VERBATIM" if why == "" else "CHANGED"
        same = ast.dump(m) == ast.dump(t)
        if (a, b) != (t.lineno, t.end_lineno):
            bad.append(f"{name}: comment names :{a}-{b}, the source def is :{t.lineno}-{t.end_lineno}")
        if sha16 != D.TC10_SRC_SHA256[:16]:
            bad.append(f"{name}: comment sha {sha16} != {D.TC10_SRC_SHA256[:16]}")
        if label != want:
            bad.append(f"{name}: labelled {label}, PORTS says {want}")
        if want == "VERBATIM" and not same:
            bad.append(f"{name}: labelled VERBATIM but its AST differs from tierc10_data.{name}")
        if want == "CHANGED" and same:
            bad.append(f"{name}: labelled CHANGED but AST-identical to its source")
        st[want] += 1
    return bad, st


def _srcs() -> tuple[str, str]:
    return (Path(D.__file__).read_text(encoding="utf-8"),
            D.TC10_SRC.read_text(encoding="utf-8"))


def port_break():
    mine, tc10 = _srcs()

    def edit(old: str, new: str) -> str:
        if mine.count(old) < 1:
            raise AssertionError(f"plant anchor not found: {old[:40]!r}")
        return mine.replace(old, new, 1)
    body = edit('h.update(f"{len(df)}|{\',\'.join(cols)}".encode())',
                'h.update(f"{len(df)};{\',\'.join(cols)}".encode())')
    rng = edit("scripts/tierc10_data.py:428-437 @", "scripts/tierc10_data.py:428-438 @")
    lab = edit("scripts/tierc10_data.py:472-517 @ sha256 2cbf9bb6bcfea3ec — CHANGED",
               "scripts/tierc10_data.py:472-517 @ sha256 2cbf9bb6bcfea3ec — VERBATIM")
    return plants([("frame_sha's separator changed in a copy of this module", lambda: port_findings(body, tc10)[0]),
                   ("frame_sha's provenance range off by one", lambda: port_findings(rng, tc10)[0]),
                   ("pin_as_of relabelled VERBATIM", lambda: port_findings(lab, tc10)[0])])


def port_real():
    mine, tc10 = _srcs()
    sha_now = hashlib.sha256(tc10.encode("utf-8")).hexdigest()
    bad, st = port_findings(mine, tc10)
    if sha_now != D.TC10_SRC_SHA256:
        bad.append(f"scripts/tierc10_data.py sha {sha_now[:16]} != the provenance sha")
    return (not bad), (f"{len(D.PORTS)} ports: {st['VERBATIM']} VERBATIM (AST-identical), "
                       f"{st['CHANGED']} CHANGED (each names its change); source sha "
                       f"{sha_now[:16]} == provenance" if not bad else f"{len(bad)} fault(s): {bad[:3]}")


# ═══════════════════════════════════════════════ F-D11-CLONE
def clone_findings(root: Path, rels: list[str], exp: dict, scope: set) -> tuple[list[str], dict]:
    """In-scope files: the TC10 snapshot's file must be TC10's manifest bytes, and
    the TC11 file's rows up to that file's last stamp must be those rows, byte for
    byte (raw column bytes).  Every other file: whole-file sha == TC10's record."""
    bad, st = [], {"prefix": 0, "whole": 0, "rows": 0}
    for rel in rels:
        q, src = root / rel, D.TC10_SNAPSHOT / rel
        if rel in scope:
            if D.file_sha256(src) != exp[rel]:
                bad.append(f"{rel}: the TC10 snapshot's own file is not TC10's manifest bytes")
                continue
            col, cols = colset(rel)
            t10 = pd.read_parquet(src).sort_values(col)
            cur = pd.read_parquet(q).sort_values(col)
            pref = cur[cur[col] <= int(t10[col].max())]
            if D.frame_sha(pref, cols) != D.frame_sha(t10, cols):
                bad.append(f"{rel}: rows up to the TC10 edge differ from the TC10 snapshot")
            st["prefix"] += 1
            st["rows"] += len(t10)
        else:
            want = exp.get(rel) or D.file_sha256(src)
            if D.file_sha256(q) != want:
                bad.append(f"{rel}: bytes differ from TC10's record")
            st["whole"] += 1
    return bad, st


def clone_break():
    exp = tc10_expected()
    pre = read_json(OUT / "PRE_STATE.json")
    other = sorted((r for r in exp if r not in pre["files"]),
                   key=lambda r: (D.SNAPSHOT / r).stat().st_size)[0]
    with tmpdir() as tmp:
        t = Path(tmp)
        flip_byte_copy(D.SNAPSHOT / other, t / "flip", other)
        f4 = pd.read_parquet(D.SNAPSHOT / "klines/BTCUSDT_4h.parquet").sort_values("open_time")
        f4 = f4.reset_index(drop=True)
        f4.loc[100, "close"] = f4.loc[100, "close"] + 0.1
        frame_copy(f4, t / "edit", "klines/BTCUSDT_4h.parquet")
        return plants([
            (f"a flipped byte in a temp copy of {other}",
             lambda: clone_findings(t / "flip", [other], exp, set(pre["files"]))[0]),
            ("a temp copy of klines/BTCUSDT_4h.parquet with one historical close moved",
             lambda: clone_findings(t / "edit", ["klines/BTCUSDT_4h.parquet"], exp,
                                    set(pre["files"]))[0])])


def clone_real():
    exp = tc10_expected()
    pre = read_json(OUT / "PRE_STATE.json")
    att = read_json(OUT / D.CLONE_ATTEST)
    have, src = tree(D.SNAPSHOT), tree(D.TC10_SNAPSHOT)
    bad = []
    if have != src:
        bad.append(f"file sets differ: +{sorted(set(have) - set(src))[:3]} "
                   f"-{sorted(set(src) - set(have))[:3]}")
    for rel, v in att["files"].items():
        if rel in exp and v["sha256"] != exp[rel]:
            bad.append(f"CLONE_ATTEST {rel}: clone sha != TC10 manifest")
    if set(att["files"]) != set(src):
        bad.append("CLONE_ATTEST does not list every file of the TC10 snapshot")
    f2, st = clone_findings(D.SNAPSHOT, have, exp, set(pre["files"]))
    bad += f2
    return (not bad), (f"{len(have)} files == the TC10 snapshot's set; CLONE_ATTEST {len(att['files'])} "
                       f"files, {sum(1 for r in att['files'] if r in exp)} pinned by TC10's manifest; "
                       f"{st['prefix']} in-scope files: rows up to the TC10 edge ({st['rows']} rows) "
                       f"byte-identical to the TC10 snapshot; {st['whole']} other files byte-identical"
                       if not bad else f"{len(bad)} fault(s): {bad[:3]}")


# ═══════════════════════════════════════════════ F-D11-PIN
def pin_break():
    pin = read_json(OUT / "AS_OF_PIN.json")
    keys = D.tc10_pin_keys()
    notclose = dict(pin, as_of_last_closed_4h_close_ms=pin["as_of_last_closed_4h_close_ms"] + 300_000)
    forming = dict(pin, venue_server_time_ms=pin["venue_close_time_of_pinned_bar_ms"] - 1)
    later = dict(pin, as_of_last_closed_4h_close_ms=pin["as_of_last_closed_4h_close_ms"] + D.MS_4H,
                 as_of_last_closed_4h_open_ms=pin["as_of_last_closed_4h_open_ms"] + D.MS_4H)
    dropped = {k: v for k, v in pin.items() if k != "local_clock_skew_ms"}
    return plants([("a pin that is not a 4h close (+5 min)", lambda: D.pin_findings(notclose, keys)),
                   ("a bar still forming by the venue clock", lambda: D.pin_findings(forming, keys)),
                   ("a pin one 4h bar later than the contract's", lambda: D.pin_findings(later, keys)),
                   ("a TC10 schema key dropped", lambda: D.pin_findings(dropped, keys))])


def pin_real():
    p = OUT / "AS_OF_PIN.json"
    pin = read_json(p)
    bad = list(D.pin_findings(pin, D.tc10_pin_keys()))
    c, k = pin["as_of_last_closed_4h_close_ms"], pin["venue_kline_of_pinned_bar"]
    if not (c == PIN_MS and pin["as_of_last_closed_4h"] == PIN_ISO and c % STEP["4h"] == 0):
        bad.append("not the contract's 4h close")
    if not (int(k[0]) + STEP["4h"] - 1 == int(k[6]) == c - 1 < pin["venue_server_time_ms"]):
        bad.append("the venue kline in the file does not prove the bar closed")
    seal = read_json(OUT / D.SEAL)
    if seal["files"]["AS_OF_PIN.json"]["sha256"] != D.file_sha256(p):
        bad.append("AS_OF_PIN.json moved since the seal")
    before = p.read_bytes()
    with tmpdir() as tmp:
        cp = Path(tmp) / "AS_OF_PIN.json"
        cp.write_bytes(before)
        refused = False
        try:
            D._dump_once(dict(pin, as_of_last_closed_4h_close_ms=c + D.MS_4H), cp)
        except SystemExit:
            refused = True
        if not refused or cp.read_bytes() != before:
            bad.append("write-once let a rewrite through")

        def no_net(*a, **kw):
            raise AssertionError("pin_as_of reached the network on a filed pin")
        with mutated(D.requests, "get", no_net):
            again = D.pin_as_of(Path(tmp))
        if again != pin or cp.read_bytes() != before:
            bad.append("a second pin_as_of did not re-read the filed pin")
    if p.read_bytes() != before:
        bad.append("the real pin file moved during this leg")
    return (not bad), (f"pin {pin['as_of_last_closed_4h']} (close ms {c}); venue closeTime "
                       f"{pin['venue_close_time_of_pinned_bar_ms']} < venue clock "
                       f"{pin['venue_server_time_ms']}; latest closed at the pin run "
                       f"{pin['latest_closed_4h_at_pin_run']}; TC10's {len(D.tc10_pin_keys())} "
                       f"keys all present; a rewrite HALTs and a second pin re-reads, no network"
                       if not bad else f"{len(bad)} fault(s): {bad[:3]}")


# ═══════════════════════════════════════════════ F-D11-PREFIX
def prefix_break():
    pre = read_json(OUT / "PRE_STATE.json")
    rel = "klines/BTCUSDT_12h.parquet"
    one = {"files": {rel: pre["files"][rel]}}
    f = pd.read_parquet(D.SNAPSHOT / rel).sort_values("open_time").reset_index(drop=True)
    with tmpdir() as tmp:
        t = Path(tmp)
        g = f.copy()
        g.loc[1000, "high"] = g.loc[1000, "high"] + 0.01
        frame_copy(g, t / "edit", rel)
        frame_copy(f.drop(index=2000), t / "drop", rel)
        ins = pd.concat([f, f.iloc[[3000]].assign(open_time=f.loc[3000, "open_time"] + 1)])
        frame_copy(ins.sort_values("open_time"), t / "ins", rel)

        def run(sub):
            return [r["why"] for r in D.verify_prefixes(one, t / sub) if not r["ok"]]
        return plants([("a historical 12h high moved by 0.01 in a temp copy", lambda: run("edit")),
                       ("a historical 12h row deleted in a temp copy", lambda: run("drop")),
                       ("a row inserted behind the edge in a temp copy", lambda: run("ins"))])


def prefix_real():
    pre = read_json(OUT / "PRE_STATE.json")
    rows = D.verify_prefixes(pre)
    bad = [r["file"] for r in rows if not r["ok"]]
    ext = sum(1 for r in rows if r["extended_by"])
    untouched = sum(1 for r in rows if r["untouched_file"])
    ok = not bad and len(rows) == 124 == len(pre["files"])
    return ok, (f"{len(rows)}/{len(pre['files'])} PRE_STATE files: every old row byte-identical "
                f"({sum(r['old_rows'] for r in rows)} rows); {ext} extended "
                f"(+{sum(r['extended_by'] for r in rows)} rows), {untouched} untouched byte for byte"
                if ok else f"{len(bad)} prefix(es) moved: {bad[:3]}")


# ═══════════════════════════════════════════════ F-D11-EDGE
def expected_last_open(iv: str) -> int:
    s, a = STEP[iv], (MONDAY if iv == "1w" else 0)
    x = PIN_MS - s
    return x - ((x - a) % s)


def edge_findings(root: Path, rel: str) -> list[str]:
    _, iv = D.split_rel(rel)
    t = np.sort(pd.read_parquet(root / rel, columns=["open_time"])["open_time"].to_numpy(np.int64))
    bad, want = [], expected_last_open(iv)
    if t[-1] != want:
        bad.append(f"{rel}: last open {D.iso(t[-1])} != the lens's last bar closing <= the pin "
                   f"{D.iso(want)}")
    d = np.diff(t)
    if (d != STEP[iv]).any():
        bad.append(f"{rel}: {int((d > STEP[iv]).sum())} gap(s), {int((d <= 0).sum())} duplicate/"
                   f"backward stamp(s)")
    if (t + STEP[iv] > PIN_MS).any():
        bad.append(f"{rel}: {int((t + STEP[iv] > PIN_MS).sum())} row(s) past the pin")
    return bad


def edge_break():
    rel = "klines/BTCUSDT_4h.parquet"
    f = pd.read_parquet(D.SNAPSHOT / rel).sort_values("open_time").reset_index(drop=True)
    with tmpdir() as tmp:
        t = Path(tmp)
        frame_copy(f.drop(index=len(f) // 2), t / "mid", rel)
        frame_copy(f.iloc[:-1], t / "last", rel)
        nxt = f.iloc[[-1]].assign(open_time=int(f["open_time"].iloc[-1]) + STEP["4h"])
        frame_copy(pd.concat([f, nxt]), t / "past", rel)
        return plants([("a dropped middle bar", lambda: edge_findings(t / "mid", rel)),
                       ("a dropped last bar", lambda: edge_findings(t / "last", rel)),
                       ("a bar appended past the pin", lambda: edge_findings(t / "past", rel))])


def edge_real():
    man = read_json(OUT / "STAGE_D_MANIFEST.json")
    rows = {f["path"]: f for f in man["files"]}
    bad, n_k, n_f = [], 0, 0
    for rel in D.scope_paths():
        q = D.SNAPSHOT / rel
        r = rows.get(rel)
        if r is None or r.get("sha256") != D.file_sha256(q):
            bad.append(f"{rel}: the manifest does not describe this file's bytes")
        if rel.startswith("klines/"):
            n_k += 1
            bad += edge_findings(D.SNAPSHOT, rel)
            if r and not (r["gap_count"] == 0 and r["complete_to_as_of"]
                          and r["last_bar_close_equals_lens_last_closed_at_pin"]):
                bad.append(f"{rel}: the manifest row disagrees (gaps/complete)")
        else:
            n_f += 1
            stem = rel[len("funding/"):-len(".parquet")]
            last = int(pd.read_parquet(q, columns=["funding_time"])["funding_time"].max())
            cov = D.funding_coverage(stem, PIN_MS)
            if last // 3_600_000 * 3_600_000 != PIN_MS or not cov["ok"]:
                bad.append(f"{rel}: last print {D.iso(last)} is not the pin's hour, or coverage fails")
    lens = sorted({D.split_rel(r)[1] for r in D.scope_paths() if r.startswith("klines/")},
                  key=list(STEP).index)
    return (not bad), (f"{n_k} kline files ({', '.join(lens)}) each end exactly at their lens's "
                       f"last bar closing <= {PIN_ISO}, zero gaps, zero duplicates, zero rows past "
                       f"the pin; {n_f} funding tapes carry the {PIN_ISO} print; the manifest's "
                       f"sha matches every file" if not bad else f"{len(bad)} fault(s): {bad[:3]}")


# ═══════════════════════════════════════════════ F-D11-DERIVE
def kahan(vals) -> float:
    """pandas' groupby sum is COMPENSATED (Kahan); a naive left-to-right sum
    differs from it in the last bit (measured: 792 BTC days) — so the plain
    loop states the compensated sum explicitly."""
    s = c = 0.0
    for v in vals:
        y = v - c
        t = s + y
        c = (t - s) - y
        s = t
    return s


def plain_derive(stem: str, naive: bool = False) -> tuple[np.ndarray, np.ndarray]:
    f = pd.read_parquet(D.kline_path(stem, "4h")).sort_values("open_time")
    t = f["open_time"].to_numpy(np.int64)
    o, h, l, c, v = (f[k].to_numpy(np.float64) for k in ("open", "high", "low", "close", "volume"))
    days: dict[int, list[int]] = {}
    for i in range(len(t)):
        if int(t[i]) + STEP["4h"] <= PIN_MS:
            days.setdefault(int(t[i]) // DAY, []).append(i)
    add = (lambda xs: sum(xs, 0.0)) if naive else kahan
    d1 = []
    for dk in sorted(days):
        ix = days[dk]
        if len(ix) == 6:
            d1.append((dk * DAY, o[ix[0]], max(h[j] for j in ix), min(l[j] for j in ix),
                       c[ix[-1]], add([v[j] for j in ix])))
    weeks: dict[int, list[tuple]] = {}
    for r in d1:
        weeks.setdefault((r[0] - MONDAY) // WEEK, []).append(r)
    w1 = []
    for wk in sorted(weeks):
        rs = weeks[wk]
        if len(rs) == 7:
            w1.append((wk * WEEK + MONDAY, rs[0][1], max(r[2] for r in rs), min(r[3] for r in rs),
                       rs[-1][4], add([r[5] for r in rs])))
    return np.array(d1, dtype=object), np.array(w1, dtype=object)


def same_frame(df: pd.DataFrame, ref: np.ndarray) -> bool:
    if len(df) != len(ref):
        return False
    if not len(df):
        return True
    if not np.array_equal(df["open_time"].to_numpy(np.int64), ref[:, 0].astype(np.int64)):
        return False
    return all(np.array_equal(df[k].to_numpy(np.float64), ref[:, i].astype(np.float64))
               for i, k in enumerate(("open", "high", "low", "close", "volume"), 1))


def derive_break():
    stem = "BTCUSDT"
    d1_file = pd.read_parquet(D.kline_path(stem, "1d"))
    d1_ref, w1_ref = plain_derive(stem)
    d1_naive, _ = plain_derive(stem, naive=True)

    def shifted():
        with mutated(D, "MONDAY_EPOCH_OFFSET_MS", 3 * DAY):           # a SUNDAY anchor
            w_bad, _ = D.derive_1w(d1_file)
        return [] if same_frame(w_bad, w1_ref) else [
            f"a Sunday-anchored 1w ({len(w_bad)} weeks, first {D.iso(w_bad['open_time'].iloc[0])}) "
            f"!= the Monday-anchored plain loop"]

    def naive():
        return [] if same_frame(d1_file, d1_naive) else [
            "the derived 1d file != a 1d whose volume is a naive (uncompensated) sum"]
    return plants([("the module's 1w with the week anchor shifted to Sunday", shifted),
                   ("the plain loop with an uncompensated volume sum", naive)])


def derive_real():
    bad, n_d, n_w = [], 0, 0
    for stem in D.PANEL17:
        d1_ref, w1_ref = plain_derive(stem)
        d1 = pd.read_parquet(D.kline_path(stem, "1d")).sort_values("open_time")
        w1 = pd.read_parquet(D.kline_path(stem, "1w")).sort_values("open_time")
        if not same_frame(d1, d1_ref):
            bad.append(f"{stem} 1d")
        if not same_frame(w1, w1_ref):
            bad.append(f"{stem} 1w")
        n_d += len(d1)
        n_w += len(w1)
    return (not bad), (f"{len(D.PANEL17)} assets: {n_d} days and {n_w} Monday-anchored weeks "
                       f"re-derived by a plain loop from native 4h (bars closed <= {PIN_ISO}) equal "
                       f"the derived files bit for bit on all six columns"
                       if not bad else f"{len(bad)} mismatch(es): {bad[:4]}")


# ═══════════════════════════════════════════════ F-DET
def det_runs() -> dict:
    procs = {}
    for s in DET_SEEDS:
        d = RUN_ROOT / "_det_data" / f"seed_{s}"
        if d.exists():
            shutil.rmtree(d)
        env = dict(os.environ, PYTHONHASHSEED=str(s), PYTHONDONTWRITEBYTECODE="1",
                   NAIAD_CACHE_DIR=str(D.SNAPSHOT))
        procs[s] = (d, subprocess.Popen(
            [sys.executable, "-B", str(ROOT / "scripts" / "tierc11_data.py"), "--manifest",
             "--out", str(d)], env=env, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True))
    outs = {}
    for s, (d, p) in procs.items():
        _, err = p.communicate(timeout=3600)
        if p.returncode:
            clock(f"F-DET seed {s} stderr tail: {err[-300:]}")
        outs[s] = (p.returncode, {n: (d / n).read_bytes() if (d / n).exists() else b""
                                  for n in DET_FILES})
    return outs


def det_break():
    filed = (OUT / "STAGE_D_MANIFEST.json").read_bytes()
    salted = filed.replace(b'"seed": 20260924', f'"seed": 20260924, "pid": {os.getpid()}'.encode(), 1)
    clocked = filed.replace(b'"seed": 20260924', b'"seed": 20260924, "wall_clock_utc": "x"', 1)
    return plants([("a process-dependent salt in a copy of the manifest",
                    lambda: [] if salted == filed else ["bytes differ from the filed manifest"]),
                   ("a clock field in a copy of the manifest",
                    lambda: [f"clock field {m}" for m in CLOCK_FIELD.findall(clocked.decode())])])


def det_real():
    o = det_runs()
    a, b = o[DET_SEEDS[0]], o[DET_SEEDS[1]]
    filed = {n: (OUT / n).read_bytes() for n in DET_FILES}
    bad = []
    if a[0] != 0 or b[0] != 0:
        bad.append(f"exit {a[0]}/{b[0]}")
    for n in DET_FILES:
        if not (a[1][n] and a[1][n] == b[1][n] == filed[n]):
            bad.append(f"{n} differs")
        if n.endswith(".json") and CLOCK_FIELD.findall(filed[n].decode()):
            bad.append(f"{n} carries a clock field")
    sh = hashlib.sha256(filed["STAGE_D_MANIFEST.json"]).hexdigest()
    return (not bad), (f"exit {a[0]}/{b[0]}; {len(DET_FILES)} files byte-identical under "
                       f"PYTHONHASHSEED {DET_SEEDS[0]} and {DET_SEEDS[1]} and == the filed bytes "
                       f"(STAGE_D_MANIFEST.json sha {sh[:16]}…); no clock field"
                       if not bad else f"{bad}")


# ═══════════════════════════════════════════════ F-D11-UNTOUCHED
def live_stat() -> tuple:
    st = os.stat(LIVE_MANIFEST)                      # metadata only; the file is never opened
    return (st.st_size, st.st_mtime_ns, st.st_ino)


LIVE_STAT_AT_START: tuple | None = None


def untouched_findings(root: Path, rels: list[str], exp: dict, ref: dict) -> list[str]:
    bad = []
    for rel in rels:
        want = exp.get(rel) or ref.get(rel)
        if D.file_sha256(root / rel) != want:
            bad.append(f"{rel}: the TC10 snapshot's bytes moved")
    return bad


def stat_findings(a: tuple, b: tuple) -> list[str]:
    moved = [k for k, x, y in zip(("size", "mtime_ns", "inode"), a, b) if x != y]
    return [f"live cache MANIFEST.json stat moved ({', '.join(moved)})"] if moved else []


def untouched_break():
    exp = tc10_expected()
    rel = sorted(exp, key=lambda r: (D.TC10_SNAPSHOT / r).stat().st_size)[0]
    s0 = LIVE_STAT_AT_START or live_stat()
    with tmpdir() as tmp:
        flip_byte_copy(D.TC10_SNAPSHOT / rel, Path(tmp), rel)
        return plants([(f"a flipped byte in a temp copy of TC10's {rel}",
                        lambda: untouched_findings(Path(tmp), [rel], exp, {})),
                       ("a live-cache stat whose mtime moved by 1 ns",
                        lambda: stat_findings(s0, (s0[0], s0[1] + 1, s0[2])))])


def untouched_real():
    exp = tc10_expected()
    att = read_json(OUT / D.CLONE_ATTEST)
    ref = {r: v["reference_sha256"] for r, v in att["files"].items() if r not in exp}
    have = tree(D.TC10_SNAPSHOT)
    bad = []
    if set(have) != set(exp) | set(ref):
        bad.append("the TC10 snapshot's file set moved")
    bad += untouched_findings(D.TC10_SNAPSHOT, have, exp, ref)
    bad += [f"TC10's own seal: {x}" for x in D.verify_seal(D.TC10_DATA)]
    s1 = live_stat()
    bad += stat_findings(LIVE_STAT_AT_START, s1)
    return (not bad), (f"{len(have)} TC10 snapshot files re-hash to TC10's manifest "
                       f"({len(exp)}) / the clone-time record ({len(ref)}); TC10's WRITE_ONCE_SEAL "
                       f"verifies; the live cache MANIFEST.json stat (size, mtime_ns, inode) is "
                       f"unchanged across this run (stat only, never opened)"
                       if not bad else f"{len(bad)} fault(s): {bad[:3]}")


FIXTURES = (
    ("F-D11-GUARD", "the substrate guard admits the TC11 snapshot and nothing else",
     "an unset variable, the live cache, a directory inside it, the TC10 snapshot, a foreign "
     "directory, or a snapshot path without klines/ is accepted, or the real env does not "
     "resolve to tc11_20260925 with engine.data bound to it", guard_break, guard_real),
    ("F-D11-PORT", "every port of tierc10_data is what its provenance comment says",
     "a VERBATIM port is not AST-identical to its source, a comment names the wrong lines or "
     "sha, a CHANGED label hides an identical copy, or tierc10_data.py's sha moved",
     port_break, port_real),
    ("F-D11-CLONE", "the clone reproduces TC10's bytes up to every TC10 edge",
     "any in-scope file's rows up to its TC10 edge differ from the TC10 snapshot's rows (whose "
     "file re-hashes to TC10's manifest), any other file differs from TC10's record, or the "
     "clone's file set differs from TC10's", clone_break, clone_real),
    ("F-D11-PIN", "one as-of pin, closed by the venue, written once",
     "the pin is not 2026-09-25T00:00:00Z, is not a 4h close, is not closed by the venue "
     "record in the file, lacks a TC10 key, moved since the seal, or write-once lets a "
     "rewrite through", pin_break, pin_real),
    ("F-D11-PREFIX", "no pre-existing row was rewritten by the fetch",
     "any of the 124 PRE_STATE files' old rows (<= its old edge) does not re-hash to its "
     "PRE_STATE content sha", prefix_break, prefix_real),
    ("F-D11-EDGE", "every lens ends exactly at its last bar closing <= the pin, whole",
     "a kline file's last open is not its lens's last bar closing <= the pin, it holds a gap, "
     "a duplicate or a row past the pin, the manifest mis-describes it, or a funding tape "
     "lacks the pin-hour print", edge_break, edge_real),
    ("F-D11-DERIVE", "1d / 1w are native 4h re-derived, bit for bit",
     "the plain-loop 1d (six complete 4h bars per UTC day) or 1w (seven complete days, "
     "Monday-anchored) differs from a derived file in any stamp or value", derive_break, derive_real),
    ("F-DET", "two subprocess manifest builds under different hash seeds, one set of bytes",
     "the PYTHONHASHSEED 1 and 20260924 builds differ from each other or from the filed "
     "bytes, either exits nonzero, or a JSON carries a clock field", det_break, det_real),
    ("F-D11-UNTOUCHED", "the TC10 snapshot and the live cache are as they were",
     "a TC10 snapshot file does not re-hash to TC10's manifest (or its clone-time record), "
     "TC10's own seal faults, or the live cache MANIFEST.json's stat moved across this run",
     untouched_break, untouched_real),
)


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


def main() -> int:
    global RUN_ROOT, LIVE_STAT_AT_START
    LIVE_STAT_AT_START = live_stat()
    args = sys.argv[1:]
    root = RUN_ROOT = Path(next((a.split("=", 1)[1] for a in args if a.startswith("--root=")), OUT))
    pick = [a.lower() for a in args if not a.startswith("--")]
    pin = read_json(OUT / "AS_OF_PIN.json")
    first = f"as_of_last_closed_4h: {pin['as_of_last_closed_4h']}"
    if first != AS_OF_LINE:
        raise SystemExit(f"HALT: the filed pin reads {first!r}, not {AS_OF_LINE!r}")
    say(first)
    say("=" * 78)
    say("TIER-C11 STAGE TC11-D FIXTURES — the corridor · break leg first, RED or void")
    say("=" * 78)
    say(f"seed {SEED} · substrate {D.SNAPSHOT.name} · pin close ms {pin['as_of_last_closed_4h_close_ms']}"
        f" · contract sha {D.CONTRACT_SHA256[:16]}… · module scripts/tierc11_data.py")
    say(f"[LEAN-HEPHAESTUS] {len(D.LEANS)} readings filed in STAGE_D_MANIFEST.json leans "
        f"(L-0.1, L-0.2, L-1.1, L-1.2 of research_outputs/tierc11/LEANS.md; D11-a..g)")
    for fid, title, fails_if, b, r in FIXTURES:
        if not pick or any(q in fid.lower() for q in pick):
            prove(fid, title, fails_if, b, r)
    say(f"\n  {len(PASSED)} GREEN, {len(FAILED)} RED · break legs RED (correct) "
        f"{TALLY['break_red']}/{TALLY['break_red'] + TALLY['break_void']} · real legs GREEN "
        f"{TALLY['real_green']}/{TALLY['real_green'] + TALLY['real_red']}")
    for f in FAILED:
        say(f"    RED: {f}")
    root.mkdir(parents=True, exist_ok=True)
    body = ("\n".join(LINES) + "\n").encode("utf-8")
    name = TRANSCRIPT if not pick else TRANSCRIPT.replace(".txt", "_partial.txt")
    bad = file_transcript(root / name, body, "--refile-transcript" in args or bool(pick))
    for x in bad:
        clock(x)
    if FAILED:
        print("*** HALT: fixture mismatch. Nothing downstream is trustworthy. ***")
    return 1 if (FAILED or bad) else 0


if __name__ == "__main__":
    raise SystemExit(main())
