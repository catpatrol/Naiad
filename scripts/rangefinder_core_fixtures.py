#!/usr/bin/env python
"""F-RF-1c — THE ORACLE'S RANGE MACHINE IS THE MACHINE OF RECORD, COPY FOR COPY.

WHAT IS ON TRIAL. AMENDMENT A-OR1-1 clause iv (operator, 2026-09-22) moved the
Oracle's range machine to scripts/rangefinder_core.py: "The range module lives at
scripts/rangefinder_core.py; engine/ is outside this lane's write authority (BR-1 §2
clause 3); promotion into engine/ is APOLLO's call." It is a COPY of
engine/rangefinder.py (sha256 bbae464f…), which stays where it is, byte-frozen, as
TIER-C10's machine of record (F-C10-RESUME-6), and which the RangeFinder twin still
calls. Two copies of one machine drift the day one of them is edited alone. This
suite is what says they have not — "same pins, same event log" (OR-1 STEP D), proven
on every run rather than argued once.

THREE FIXTURES, TWO LEGS EACH, the BREAK leg first, and it must go RED for its own
named reason or the fixture is VOID [the prove() law of the RF and oracle suites]:

  F-RF-1c   THE EVENT LOGS OF RECORD. On the FROZEN record tape — BTCUSDT 4h cut in
            memory to open_time <= 1787371200000 (2026-08-22T04:00Z,
            rangefinder_twin.RECORD_ANCHOR_MS), the last 1,700 4h bars for v2 and the
            last 420 complete UTC days for v1, built by the twin's own loaders exactly
            as scripts/rangefinder_fixtures*.py build them — sha256(json.dumps(events,
            sort_keys=True)) of v2 macro, micro, leash, suppress and v1 body through
            rangefinder_core must equal (count, sha) of record, equal
            engine.rangefinder's on the same input, and equal a second run byte for
            byte; the tape itself, rebuilt through rangefinder_core.tape_from_klines, is
            the twin's tape (the record's tape sha bda85c2e…); and every other output
            (Range fields, pivots, coverage, kept/suppressed, flips, status lines) is
            equal between the two modules. BREAK: a pin perturbed on a COPY of the
            module's source loaded under another name; one input bar perturbed.
  F-RF-1d   SNAPSHOT PARITY — what the Oracle actually prints. snapshot() of the two
            modules over the live 4h cache, every ROSTER symbol (read by AST out of
            scripts/oracle_daily.py, never imported), exactly as range_layer() builds
            it: identical, key for key and byte for byte. BREAK: the perturbed copy
            must disagree on at least one symbol; one bar perturbed must disagree on
            its symbol.
  F-RF-1e   SOURCE EQUIVALENCE. An AST dump of every top-level definition (functions,
            the class, every constant, every import) compared NAME BY NAME between
            the two files, docstrings of those definitions included; which names
            differ is printed (expected: none), and the text below each module's
            docstring is byte-identical. BREAK: the perturbed copy must be named.

PRINT-ONLY. It WRITES NOTHING TO DISK: no transcript, no temp file, no export (the
perturbed copy is compiled from a string and lives in sys.modules only for the
moment it runs). It reads the live kline cache through engine.data.cache_dir() —
run it WITHOUT NAIAD_CACHE_DIR, as the Oracle runs. It does not run
rangefinder_twin's CLI or either RF suite's main (they rewrite
research_outputs/rangefinder/FIXTURES_v*.txt); it imports the twin's two loaders.

Run:  ~/venvs/naiad/bin/python scripts/rangefinder_core_fixtures.py
Exit: 0 if every fixture is green on REAL and red on BREAK; 1 otherwise.
"""
from __future__ import annotations

import ast
import hashlib
import json
import sys
import time
import types
from dataclasses import asdict
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from engine import rangefinder as E                                  # noqa: E402
from engine.data import cache_dir                                    # noqa: E402
import rangefinder_core as C                                         # noqa: E402
import rangefinder_twin as RF                                        # noqa: E402

CORE_PATH = ROOT / "scripts" / "rangefinder_core.py"
ENGINE_PATH = ROOT / "engine" / "rangefinder.py"
ENGINE_SHA256 = "bbae464fdc8e0e01fc90b286aa79e726fcff4422e6118dee1173f2460dab84d4"
ORACLE_SRC = ROOT / "scripts" / "oracle_daily.py"

# THE FIVE EVENT SHAS OF RECORD — typed HERE, a third object beside the two
# modules' docstrings, so the check is never one literal counted twice.
RECORD_SHAS = {
    "v2_macro": (92, "2145418831a00be710fb401c3a7c16722c0857feda4a29d58d503f3dc2b09ed4"),
    "v2_micro": (573, "73798d744a377d6f2398020b0ae891d2f34efab2e48fda1c0e745243e2b04c72"),
    "v2_leash": (153, "824cdff43675053a54f5c2cbbec9ba8b87c2e3661fca20c00459880bd17ec54e"),
    "v2_suppress": (17, "e7b0de6a072ea9ba0c5bb0b7dc2c0ebba72d68e2730b1e6056f26fa7189dba70"),
    "v1_body": (152, "af2485e664bf822492e8bb86ef4c45afb05844bed5e342f4a9aa30588dba5404"),
}
RECORD_ANCHOR_MS = 1_787_371_200_000       # 2026-08-22T04:00Z, a bar OPEN
RECORD_TAPE_SHA8 = "bda85c2e"              # csv of t0,o,h,l,c — tape_from_klines' docstring
RECORD_SYMBOL = "BTCUSDT"                  # the one symbol the pins were calibrated on

# THE PERTURBED COPY: one pin, one character, in the SOURCE TEXT of rangefinder_core.
PIN_PLANT = ('    "REV_MIN": 1.75,\n', '    "REV_MIN": 1.80,\n')
MUTANT_NAME = "rangefinder_core_f_rf_1c_mutant"
BAR_PLANT_I = 100                          # the bar the F-RF-1 break leg perturbs too

FAILED: list[str] = []
PASSED: list[str] = []


def check(fixture: str, ok: bool, detail: str) -> bool:
    print(f"  [{'PASS' if ok else 'FAIL'}] {fixture}: {detail}")
    return ok


def prove(fixture: str, title: str, break_leg, real_leg) -> None:
    """Both legs, in order. The break leg must go red or the fixture is void."""
    print(f"\n{fixture} — {title}")
    b_ok, b_detail = break_leg()
    print(f"  [BREAK] deliberate violation -> "
          f"{'RED (correct)' if not b_ok else 'GREEN (FIXTURE IS VOID)'}: {b_detail}")
    r_ok, r_detail = real_leg()
    green = check(fixture, r_ok, r_detail)
    if b_ok:
        FAILED.append(f"{fixture} (break leg passed — fixture proves nothing)")
    elif not green:
        FAILED.append(fixture)
    else:
        PASSED.append(fixture)


def judge_plants(plants) -> tuple[bool, str]:
    """(name, the finding it MUST produce, judge) — judged ONE AT A TIME (the F-BR-13
    idiom): each plant must go red on its own and for its own reason."""
    green, out = False, []
    for name, must, judge in plants:
        if judge is None:
            green = True
            out.append(f"{name} -> GREEN: the plant could not be planted")
            continue
        bad = judge()
        hits = [b for b in bad if must in b]
        if hits:
            out.append(f"{name} -> RED: {hits[0]}"
                       + (f" (+{len(hits) - 1} more of its kind)" if len(hits) > 1 else ""))
        else:
            green = True
            out.append(f"{name} -> " + ("GREEN" if not bad else
                       f"RED FOR THE WRONG REASON (no finding says {must!r}; first: {bad[0]})"))
    return green, " ‖ ".join(out)


# ═══════════════════════════════════════════════════════════ the inputs

def sha(x) -> str:
    return hashlib.sha256(json.dumps(x, sort_keys=True).encode()).hexdigest()


def file_sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def tape_sha(d: pd.DataFrame) -> str:
    return hashlib.sha256(d[["t0", "o", "h", "l", "c"]].to_csv(index=False).encode()).hexdigest()


D4 = RF.bars_4h(anchor_ms=RECORD_ANCHOR_MS)       # v2: the last 1,700 4h bars of record
D1 = RF.daily_bars(anchor_ms=RECORD_ANCHOR_MS)    # v1: the last 420 complete UTC days


def mutant() -> types.ModuleType:
    """rangefinder_core's SOURCE with PIN_PLANT applied, compiled from a string and
    executed as a module under ANOTHER NAME. It sits in sys.modules only while its
    body runs (the dataclass decorator resolves annotations through sys.modules) and
    is removed at once: nothing on disk, nothing left behind."""
    src = CORE_PATH.read_text(encoding="utf-8")
    if src.count(PIN_PLANT[0]) != 1:
        raise RuntimeError(f"the pin plant's anchor {PIN_PLANT[0]!r} is not in the source once")
    mod = types.ModuleType(MUTANT_NAME)
    mod.__file__ = f"<{MUTANT_NAME}>"
    sys.modules[MUTANT_NAME] = mod
    try:
        exec(compile(src.replace(*PIN_PLANT), mod.__file__, "exec"), mod.__dict__)
    finally:
        sys.modules.pop(MUTANT_NAME, None)
    return mod


_MUTANT: list[types.ModuleType] = []


def the_mutant() -> types.ModuleType:
    if not _MUTANT:
        _MUTANT.append(mutant())
    return _MUTANT[0]


def five(mod, d4: pd.DataFrame, d1: pd.DataFrame) -> dict[str, list]:
    """The five logs of record through `mod`, the way the RF suites cut them."""
    v2 = mod.run_v2(d4, mod.PINS_V2)
    return {"v2_macro": v2["macro"]["events"], "v2_micro": v2["micro"]["events"],
            "v2_leash": v2["leash"], "v2_suppress": v2["suppressed"],
            "v1_body": mod.run_machine(d1, mod.PINS)["events"]}


def whole(mod, d4: pd.DataFrame, d1: pd.DataFrame) -> dict[str, str]:
    """Everything else each module returns on the record tapes, serialised."""
    v2 = mod.run_v2(d4, mod.PINS_V2)
    v1 = mod.run_machine(d1, mod.PINS)
    out = {}
    for tag, m in (("v2.macro", v2["macro"]), ("v2.micro", v2["micro"]), ("v1", v1)):
        out[f"{tag}.ranges"] = json.dumps([asdict(r) for r in m["ranges"]], default=str)
        out[f"{tag}.pivots"] = json.dumps(m["pivots"], default=str)
        out[f"{tag}.summary"] = json.dumps({k: v for k, v in m.items()
                                            if k not in ("events", "ranges", "pivots")},
                                           default=str)
    for k in ("kept", "flips", "state", "macro_count_feb_aug", "status_line",
              "micro_kept_events"):
        out[f"v2.{k}"] = json.dumps(v2[k], default=str)
    out["pins"] = json.dumps([list(mod.PINS.items()), list(mod.PINS_V2.items()),
                              mod.ATR_LEN, mod.V2_WINDOW_BARS, mod.MEM_CAP_PER_SIDE])
    return out


def event_findings(mod, d4: pd.DataFrame, d1: pd.DataFrame, label: str) -> list[str]:
    """The five logs through `mod` against the record, (count, sha) each."""
    bad = []
    for k, ev in five(mod, d4, d1).items():
        n, want = RECORD_SHAS[k]
        got = (len(ev), sha(ev))
        if got != (n, want):
            bad.append(f"{label}: {k} differs from the record — {got[0]} events sha "
                       f"{got[1][:16]}…, record {n} events {want[:16]}…")
    return bad


# ═══════════════════════════════════ F-RF-1c · THE EVENT LOGS OF RECORD

def rf1c_break() -> tuple[bool, str]:
    d4 = D4.copy()
    d4.loc[d4.index[BAR_PLANT_I], "h"] = d4["h"].iloc[BAR_PLANT_I] * 1.02
    d1 = D1.copy()
    d1.loc[d1.index[BAR_PLANT_I], "h"] = d1["h"].iloc[BAR_PLANT_I] * 1.02
    return judge_plants((
        (f"PIN PLANT (a COPY of rangefinder_core's source, PINS "
         f"{PIN_PLANT[0].strip()} -> {PIN_PLANT[1].strip()}, loaded as {MUTANT_NAME})",
         "differs from the record",
         lambda: event_findings(the_mutant(), D4, D1, "the perturbed copy")),
        (f"BAR PLANT (one input bar perturbed: bar {BAR_PLANT_I}'s high x1.02 on both "
         f"record tapes, through the REAL rangefinder_core)",
         "differs from the record",
         lambda: event_findings(C, d4, d1, "the perturbed tape")),
    ))


def rf1c_real() -> tuple[bool, str]:
    bad = []
    t0 = time.perf_counter()
    core1 = five(C, D4.copy(), D1.copy())
    core2 = five(C, D4.copy(), D1.copy())
    eng = five(E, D4.copy(), D1.copy())
    lines = []
    for k, (n, want) in RECORD_SHAS.items():
        c1, c2, e = (len(core1[k]), sha(core1[k])), (len(core2[k]), sha(core2[k])), \
            (len(eng[k]), sha(eng[k]))
        ok = c1 == (n, want) and c2 == c1 and e == c1
        lines.append(f"{k} {n}/{want[:12]}… core {'==' if c1 == (n, want) else '!='} record · "
                     f"rerun {'==' if c2 == c1 else '!='} · engine {'==' if e == c1 else '!='}")
        print(f"      {k:12} {c1[0]:4d} events  {c1[1]}  record {'==' if c1 == (n, want) else '!='}"
              f" · second run {'==' if c2 == c1 else '!='} · engine.rangefinder "
              f"{'==' if e == c1 else '!='}")
        if not ok:
            bad.append(f"{k}: core {c1[0]}/{c1[1][:16]}… record {n}/{want[:16]}… rerun "
                       f"{c2[0]}/{c2[1][:16]}… engine {e[0]}/{e[1][:16]}…")
    # the tape itself: the twin's (engine-built) tape == the core-built tape == record
    raw = pd.read_parquet(cache_dir() / "klines" / f"{RECORD_SYMBOL}_4h.parquet")
    raw = raw[raw["open_time"] <= RECORD_ANCHOR_MS]
    dc = C.tape_from_klines(raw, C.V2_WINDOW_BARS)
    if tape_sha(dc) != tape_sha(D4) or not tape_sha(D4).startswith(RECORD_TAPE_SHA8):
        bad.append(f"the record tape through rangefinder_core.tape_from_klines "
                   f"{tape_sha(dc)[:16]}… vs the twin's {tape_sha(D4)[:16]}… vs the record "
                   f"{RECORD_TAPE_SHA8}…")
    if not D4.equals(dc):
        bad.append("the core-built tape is not the twin's tape frame for frame (ts or attrs)")
    # every other output, module against module
    wc, we = whole(C, D4, D1), whole(E, D4, D1)
    moved = [k for k in wc if wc[k] != we.get(k)] + [k for k in we if k not in wc]
    if moved:
        bad.append(f"rangefinder_core and engine.rangefinder disagree beyond the events on "
                   f"{moved[:6]}")
    secs = time.perf_counter() - t0
    print(f"      ({secs:.1f} s)")
    return (not bad), (
        f"on the FROZEN record tape (v2 {D4['ts'].iloc[0]} → {D4['ts'].iloc[-1]}, {len(D4)} 4h "
        f"bars, tape sha {tape_sha(D4)[:16]}… = the record's {RECORD_TAPE_SHA8}…, rebuilt "
        f"identically by rangefinder_core.tape_from_klines; v1 {D1['ts'].iloc[0]} → "
        f"{D1['ts'].iloc[-1]}, {len(D1)} complete days): all five logs through "
        f"rangefinder_core equal (count, sha) of record, equal engine.rangefinder's on the "
        f"same input and equal a second run byte for byte — "
        + "; ".join(lines)
        + f"; and {len(wc)} further outputs (Range fields, pivots, summaries, kept, flips, "
          f"state, status lines, micro_kept_events, the pins in key order) are equal "
          f"module against module" if not bad else "; ".join(bad[:4]))


# ═══════════════════════════════════════ F-RF-1d · SNAPSHOT PARITY

def roster() -> tuple[str, ...]:
    """REGISTER['ROSTER']['value'] out of oracle_daily.py's SOURCE, by AST: the
    Oracle is never imported here (it would drag analytics into this process)."""
    tree = ast.parse(ORACLE_SRC.read_text(encoding="utf-8"))
    for n in tree.body:
        tg = (n.targets if isinstance(n, ast.Assign)
              else [n.target] if isinstance(n, ast.AnnAssign) else [])
        if any(isinstance(t, ast.Name) and t.id == "REGISTER" for t in tg):
            for k, v in zip(n.value.keys, n.value.values):
                if isinstance(k, ast.Constant) and k.value == "ROSTER":
                    for kk, vv in zip(v.keys, v.values):
                        if isinstance(kk, ast.Constant) and kk.value == "value":
                            return tuple(ast.literal_eval(vv))
    raise RuntimeError("REGISTER['ROSTER']['value'] not found in oracle_daily.py")


_FRAMES: dict[str, pd.DataFrame] = {}


def frame(sym: str) -> pd.DataFrame:
    if sym not in _FRAMES:
        _FRAMES[sym] = pd.read_parquet(cache_dir() / "klines" / f"{sym}_4h.parquet")
    return _FRAMES[sym]


def snap(mod, f: pd.DataFrame) -> dict:
    """range_layer()'s three calls, verbatim in shape: the tape, the machine, the snapshot."""
    d = mod.tape_from_klines(f, n_bars=mod.V2_WINDOW_BARS)
    return mod.snapshot(d, mod.run_v2(d, mod.PINS_V2))


def snapshot_findings(mod_a, mod_b, syms, label: str, bent: str | None = None) -> list[str]:
    """snapshot() of mod_a vs mod_b per symbol, as json bytes. `bent` names one symbol
    whose frame mod_a sees with its LAST close perturbed x1.001."""
    bad = []
    for sym in syms:
        f = frame(sym)
        fa = f
        if sym == bent:
            fa = f.copy()
            fa.loc[fa.index[-1], "close"] = fa["close"].iloc[-1] * 1.001
        a, b = snap(mod_a, fa), snap(mod_b, f)
        ja, jb = json.dumps(a, sort_keys=True), json.dumps(b, sort_keys=True)
        if ja != jb:
            keys = [k for k in b if a.get(k) != b.get(k)]
            bad.append(f"{label}: snapshot() disagrees on {sym} — keys {keys[:5]}")
    return bad


def rf1d_break() -> tuple[bool, str]:
    syms = roster()
    return judge_plants((
        (f"PIN PLANT (the perturbed copy {MUTANT_NAME} against engine.rangefinder over the "
         f"{len(syms)} roster symbols)",
         "snapshot() disagrees",
         lambda: snapshot_findings(the_mutant(), E, syms, "the perturbed copy")),
        (f"BAR PLANT (rangefinder_core handed {syms[0]}'s frame with its last close x1.001)",
         "snapshot() disagrees",
         lambda: snapshot_findings(C, E, syms[:1], "the perturbed bar", bent=syms[0])),
    ))


def rf1d_real() -> tuple[bool, str]:
    syms = roster()
    t0 = time.perf_counter()
    bad = snapshot_findings(C, E, syms, "rangefinder_core vs engine.rangefinder")
    snaps = {s: snap(C, frame(s)) for s in syms}
    live = [s for s, r in snaps.items() if r["has_range"]]
    pend = [s for s, r in snaps.items() if r["pending"]]
    print(f"      ({time.perf_counter() - t0:.1f} s)")
    if len(syms) < 3:
        bad.append(f"only {len(syms)} roster symbol(s) — the contract asks for 3+")
    if not live:
        bad.append("not one roster symbol holds a live macro range today — parity was "
                   "measured on empty boxes only; fail closed")
    return (not bad), (
        f"snapshot() identical, key for key and byte for byte (json, sort_keys), between "
        f"rangefinder_core and engine.rangefinder for all {len(syms)} roster symbols on the "
        f"LIVE 4h cache ({cache_dir()}), each tape built exactly as range_layer() builds "
        f"it (tape_from_klines, the last {C.V2_WINDOW_BARS} bars → run_v2(PINS_V2) → "
        f"snapshot); {len(live)} hold a live macro range ({', '.join(live)}), "
        f"{len(pend)} a pending breach ({', '.join(pend) or 'none'}); as-of bars "
        f"{sorted({r['as_of'] for r in snaps.values()})}" if not bad else "; ".join(bad[:4]))


# ═══════════════════════════════════════ F-RF-1e · SOURCE EQUIVALENCE

def defs(src: str) -> dict[str, str]:
    """Every top-level statement but the module docstring, keyed by the name it binds,
    as an AST dump (no line numbers). Imports are keyed by their dump."""
    out: dict[str, str] = {}
    body = ast.parse(src).body
    if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) \
            and isinstance(body[0].value.value, str):
        body = body[1:]
    for n in body:
        dump = ast.dump(n, include_attributes=False)
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            key = n.name
        elif isinstance(n, ast.Assign):
            key = ",".join(ast.unparse(t) for t in n.targets)
        elif isinstance(n, ast.AnnAssign):
            key = ast.unparse(n.target)
        elif isinstance(n, (ast.Import, ast.ImportFrom)):
            key = f"import · {ast.unparse(n)}"
        else:
            key = f"statement · {ast.unparse(n)[:60]}"
        if key in out:
            key = f"{key} (#{sum(1 for k in out if k.startswith(key)) + 1})"
        out[key] = dump
    return out


def body_text(src: str) -> str:
    """The text below the module docstring."""
    tree = ast.parse(src)
    first = tree.body[0]
    lines = src.splitlines(keepends=True)
    return "".join(lines[first.end_lineno:]).lstrip("\n")


def source_findings(core_src: str, engine_src: str, label: str) -> tuple[list[str], dict]:
    a, b = defs(core_src), defs(engine_src)
    differ = sorted(k for k in a if k in b and a[k] != b[k])
    only_core = sorted(k for k in a if k not in b)
    only_engine = sorted(k for k in b if k not in a)
    bad = []
    if differ or only_core or only_engine:
        bad.append(f"{label}: the machine definitions are not one — names that differ "
                   f"{differ}, only in rangefinder_core {only_core}, only in engine "
                   f"{only_engine}")
    if body_text(core_src) != body_text(engine_src):
        bad.append(f"{label}: the text below the module docstring is not byte-identical")
    return bad, {"names": len(a), "differ": differ, "only_core": only_core,
                 "only_engine": only_engine}


def rf1e_break() -> tuple[bool, str]:
    core_src = CORE_PATH.read_text(encoding="utf-8")
    eng_src = ENGINE_PATH.read_text(encoding="utf-8")
    planted = core_src.replace(*PIN_PLANT) if core_src.count(PIN_PLANT[0]) == 1 else None
    return judge_plants((
        (f"PIN PLANT (the same one-character pin edit in a COPY of rangefinder_core's text: "
         f"{PIN_PLANT[0].strip()} -> {PIN_PLANT[1].strip()})",
         "names that differ ['PINS']",
         (lambda: source_findings(planted, eng_src, "the perturbed copy")[0])
         if planted else None),
    ))


def rf1e_real() -> tuple[bool, str]:
    core_src = CORE_PATH.read_text(encoding="utf-8")
    eng_src = ENGINE_PATH.read_text(encoding="utf-8")
    bad, info = source_findings(core_src, eng_src, "rangefinder_core vs engine/rangefinder.py")
    print(f"      names that differ: {info['differ'] or 'none'} · only in rangefinder_core: "
          f"{info['only_core'] or 'none'} · only in engine: {info['only_engine'] or 'none'}")
    return (not bad), (
        f"{info['names']} top-level definitions compared name by name as AST dumps "
        f"(functions and the Range class WITH their docstrings, every constant — PINS and "
        f"PINS_V2 in key order —, every import): names that differ: none; only in one "
        f"file: none. The text below each module docstring is byte-identical "
        f"({len(body_text(core_src).encode()):,} B). engine/rangefinder.py sha256 "
        f"{file_sha(ENGINE_PATH)} (the copy's basis, frozen: "
        f"{'==' if file_sha(ENGINE_PATH) == ENGINE_SHA256 else '!='} {ENGINE_SHA256[:16]}…)"
        if not bad else "; ".join(bad[:4]))


# ══════════════════════════════════════════════════════════════════ MAIN

def main() -> int:
    print("=" * 78)
    print("F-RF-1c/d/e — THE ORACLE'S RANGE MACHINE (scripts/rangefinder_core.py) IS THE "
          "MACHINE OF RECORD")
    print(f"  rangefinder_core      {CORE_PATH.relative_to(ROOT)} sha256 {file_sha(CORE_PATH)}")
    print(f"  engine.rangefinder    {ENGINE_PATH.relative_to(ROOT)} sha256 {file_sha(ENGINE_PATH)}"
          f" ({'the frozen basis' if file_sha(ENGINE_PATH) == ENGINE_SHA256 else 'NOT THE FROZEN BASIS ' + ENGINE_SHA256[:16] + '…'})")
    print(f"  record tape           {RECORD_SYMBOL} 4h, open_time <= {RECORD_ANCHOR_MS} "
          f"(2026-08-22T04:00Z); v2 {len(D4)} bars, v1 {len(D1)} days")
    print(f"  kline cache           {cache_dir()} (read-only)")
    print("  writes                NOTHING (print-only)")
    print("=" * 78)
    for fid, title, b, r in (
            ("F-RF-1c", "THE EVENT LOGS OF RECORD — five shas through rangefinder_core == the "
                        "record == engine.rangefinder == a second run", rf1c_break, rf1c_real),
            ("F-RF-1d", "SNAPSHOT PARITY — what the Oracle prints, both modules, every roster "
                        "symbol, live 4h cache", rf1d_break, rf1d_real),
            ("F-RF-1e", "SOURCE EQUIVALENCE — every top-level definition, name by name",
             rf1e_break, rf1e_real)):
        try:
            prove(fid, title, b, r)
        except Exception as e:                       # a fixture that errors is a fail
            FAILED.append(f"{fid} (raised {e.__class__.__name__}: {e})")
            print(f"  [FAIL] {fid}: raised {e.__class__.__name__}: {e}")
    print("\n" + "=" * 78)
    print(f"GREEN {len(PASSED)}/3 · RED {len(FAILED)}")
    for f in FAILED:
        print(f"  RED: {f}")
    print("=" * 78)
    return 1 if FAILED else 0


if __name__ == "__main__":
    raise SystemExit(main())
