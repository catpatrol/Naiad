"""ORACLE FIXTURES — F-BR-1 .. F-BR-12 of queue BR-1 (as amended by A1-4, A2-8, T-7),
F-BR-13 of queue OR-1 STEP B (finding C-0: the D-7 logger must MEASURE),
F-BR-14 of queue OR-1 STEP D (the range layer renders and never rules),
F-BR-15 of queue OR-1 STEP F (THE DAILY ORACLE: typeset, semantics untouched),
F-BR-16 of queue OR-1 STEP C (the roster is ONE literal definition; amended by OR-2
STEP 6, R-7: KEPT ∪ ruled mappings),
F-BR-18 of queue OR-2 STEP 3 (R-1: per-row staleness, OR1-a replayed),
F-BR-19 of queue OR-2 STEP 4 (R-2: the posture-first Board), and
F-BR-20 of queue OR-2 STEP 5 (R-3: the edition word, EDITION_NOON).

BR-1 §4, verbatim: "FIXTURES (numbered; each shown FAILING on a deliberate
break before trusted)". So every fixture here runs TWICE:

    BREAK  — the property is deliberately violated; the check MUST report red.
    REAL   — the property is checked against the real artifact; it must be green.

A fixture that cannot be made to fail is not evidence of anything. `prove()`
enforces both legs and refuses to count a fixture that passed its own break.

Run:  ~/venvs/naiad/bin/python scripts/oracle_fixtures.py
Exit: 0 if every fixture is green on REAL and red on BREAK; 1 otherwise.
"""
from __future__ import annotations

import ast
import contextlib
import functools
import hashlib
import importlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from engine.data import cache_dir            # noqa: E402
from engine import indicators as ind         # noqa: E402

import posture_engine as PE                  # noqa: E402
import oracle_daily as OD                    # noqa: E402

FAILED: list[str] = []
PASSED: list[str] = []


def check(fixture: str, ok: bool, detail: str) -> bool:
    tag = "PASS" if ok else "FAIL"
    print(f"  [{tag}] {fixture}: {detail}")
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


# ═════════════════════════════════════════ the artifacts under test

DATE = None
HTML = None
CAL = None
TAPE = None
# the range layer's SIBLING tape of the same artifact set (A-OR1-1 v, 2026-09-22):
# research_outputs/oracle/tape_ranges/oracle_tape_ranges_<DATE>.parquet. Read by
# F-BR-14 only; the D-4 tape above carries no range column.
TAPE_RANGES = None
TAPE_RANGES_PATH = None


def _latest(pattern: str, d: Path) -> Path | None:
    xs = sorted(d.glob(pattern))
    return xs[-1] if xs else None


def load_artifacts() -> None:
    global DATE, HTML, CAL, TAPE, TAPE_RANGES, TAPE_RANGES_PATH
    h = _latest("oracle_*.html", OD.OUT_DIR)
    if h is None:
        raise SystemExit("HALT: no rendered oracle_*.html — run oracle_daily.py first")
    DATE = h.stem.replace("oracle_", "")
    HTML = h.read_text(encoding="utf-8")
    c = _latest(f"oracle_calibration_{DATE}_*.json", OD.CAL_DIR)
    CAL = json.loads(c.read_text()) if c else None
    t = _latest(f"oracle_tape_{DATE}.parquet", OD.TAPE_DIR)
    TAPE = pd.read_parquet(t) if t else None
    TAPE_RANGES_PATH = _latest(f"oracle_tape_ranges_{DATE}.parquet", OD.TAPE_RANGES_DIR)
    TAPE_RANGES = pd.read_parquet(TAPE_RANGES_PATH) if TAPE_RANGES_PATH else None


def section(name: str) -> str:
    """The HTML between one <h2> and the next, of the artifact under test. '' IF NO
    HEADING STARTS WITH `name`: a caller that COMPARES two of these must treat '' as a
    failure, never as equality (see F-BR-6)."""
    return _sec(HTML, name)


# ═══════════════════════════════════ F-BR-1 · PARITY (Pine, symbol for symbol)

PINE_SRC = ROOT / "pine" / "SS_v12_0_1.pine"
FIXTURE_DAY_MS = 1_786_492_800_000        # 2026-08-12T00:00:00Z, a frozen day


# WARM-UP CUTOFF. The independent EMA below is SMA-seeded (the textbook and
# Pine-documented form); engine.indicators.ema seeds at the first bar. The two
# recursions converge — alpha=2/(L+1) forgets its seed geometrically — but they
# differ during warm-up BY CONSTRUCTION, so the comparison starts well after the
# slowest thread is warm. 3.46 x 316 = 1094 bars is the estate's own warm law
# (census2b_program.WARMFACTOR); this uses 4x that for margin.
PARITY_WARM_BARS = 4 * 1094


def _ema_independent(x: np.ndarray, length: int) -> np.ndarray:
    """ta.ema transcribed from Pine semantics, in plain numpy.

    DELIBERATELY does not import engine.indicators. The first version of this
    fixture called ind.ema — the SAME module object the engine under test uses —
    so it compared engine.indicators against itself and was structurally blind
    to an EMA parity break. Proven blind: monkeypatching ind.ema to an
    incompatible variant left the fixture green. This is the repair.
    """
    n = len(x)
    out = np.full(n, np.nan, dtype="float64")
    if n < length:
        return out
    alpha = 2.0 / (length + 1.0)
    acc = float(np.mean(x[:length]))          # SMA seed at bar length-1
    out[length - 1] = acc
    for i in range(length, n):
        acc = alpha * float(x[i]) + (1.0 - alpha) * acc
        out[i] = acc
    return out


def _cross_independent(a: np.ndarray, b: np.ndarray, up: bool) -> np.ndarray:
    """ta.crossover / ta.crossunder: a>b now AND a<=b prior. NaN compares False."""
    n = len(a)
    out = np.zeros(n, dtype=bool)
    now = (a > b) if up else (a < b)
    prev = (a <= b) if up else (a >= b)
    ok = np.isfinite(a) & np.isfinite(b)
    ok_prev = np.zeros(n, dtype=bool)
    ok_prev[1:] = ok[:-1]
    out[1:] = (now[1:] & prev[:-1] & ok[1:] & ok_prev[1:])
    return out


def _stations_independent(close, high, low) -> tuple[np.ndarray, dict]:
    """A SECOND state machine, transcribed from the ratified TC3 rule card, that
    produces the FOUR POSTURE WORDS per bar without touching posture_engine.

    The first version of this fixture compared six boolean cross series and
    never formed a word — so the whole of D-1's central output shipped with no
    coverage, and gutting stations_for() left the fixture green. This is the
    repair: it walks bars, opens and closes windows, and emits the word.

    Rule card, verbatim: TIDE long iff e89>e316 AND close>e316 · WINDOW 12/89
    cross in direction, no counter yet, displacement |close-e89|/ATR >= 0.75 ·
    TRIGGER first in-window 12/26 · BELL counter 12/89 OR 89/316 against.
    """
    e12 = _ema_independent(close, 12)
    e26 = _ema_independent(close, 26)
    e89 = _ema_independent(close, 89)
    e316 = _ema_independent(close, 316)
    # ATR: Wilder RMA of true range, transcribed rather than imported.
    n = len(close)
    tr = np.full(n, np.nan)
    tr[0] = high[0] - low[0]
    for i in range(1, n):
        tr[i] = max(high[i] - low[i], abs(high[i] - close[i - 1]),
                    abs(low[i] - close[i - 1]))
    atr = np.full(n, np.nan)
    acc = float(np.mean(tr[:14]))
    atr[13] = acc
    for i in range(14, n):
        acc = (acc * 13.0 + tr[i]) / 14.0
        atr[i] = acc

    x = {
        "w_up": _cross_independent(e12, e89, True),
        "w_dn": _cross_independent(e12, e89, False),
        "t_up": _cross_independent(e12, e26, True),
        "t_dn": _cross_independent(e12, e26, False),
        "b_up": _cross_independent(e89, e316, True),
        "b_dn": _cross_independent(e89, e316, False),
    }
    d_floor = PE.REGISTER["D_DISPLACEMENT"]["value"]
    dead_mem = PE.REGISTER["DEAD_MEMORY_BARS"]["value"]

    words = np.array(["STALKING"] * n, dtype=object)
    open_dir = 0        # 0 none, +1 long, -1 short
    open_trig = False
    last_close_i = None
    for i in range(n):
        if open_dir != 0:
            counter = x["w_dn"][i] if open_dir == 1 else x["w_up"][i]
            bell = x["b_dn"][i] if open_dir == 1 else x["b_up"][i]
            if counter or bell:
                open_dir, open_trig, last_close_i = 0, False, i
            else:
                t = x["t_up"][i] if open_dir == 1 else x["t_dn"][i]
                if t:
                    open_trig = True
        if open_dir == 0:
            for dirn, opens in ((1, x["w_up"]), (-1, x["w_dn"])):
                if not opens[i]:
                    continue
                if dirn == 1:
                    tide = e89[i] > e316[i] and close[i] > e316[i]
                else:
                    tide = e89[i] < e316[i] and close[i] < e316[i]
                a = atr[i]
                disp = abs(close[i] - e89[i]) / a if (np.isfinite(a) and a > 0) else np.nan
                if tide and np.isfinite(disp) and disp >= d_floor:
                    open_dir, open_trig = dirn, False
                    t = x["t_up"][i] if dirn == 1 else x["t_dn"][i]
                    open_trig = bool(t)
                    last_close_i = None
                    break
        if open_dir != 0:
            words[i] = "TRIGGERED" if open_trig else "ARMED"
        elif last_close_i is not None and (i - last_close_i) <= dead_mem:
            words[i] = "DEAD"
        else:
            words[i] = "STALKING"
    return words, x


def _parity_compare(mutate=None, as_of_offsets=(0, 40, 120, 300)) -> tuple[bool, str]:
    """Compare STATION WORDS, symbol for symbol, at several as-of points."""
    v12_1_present = any(p.name.startswith("SS_v12_1") for p in (ROOT / "pine").iterdir())
    mismatches, checked, compared, skipped = [], 0, 0, []
    for sym in OD.REGISTER["ROSTER"]["value"]:
        df = OD.load_lens(sym, "4h")
        df = df[df["open_time"] <= FIXTURE_DAY_MS].reset_index(drop=True)
        if len(df) < PARITY_WARM_BARS + 400:
            skipped.append(f"{sym}({len(df)}b)")
            continue
        close = df["close"].to_numpy("float64")
        indep, _ = _stations_independent(close, df["high"].to_numpy("float64"),
                                         df["low"].to_numpy("float64"))
        if mutate is not None:
            indep = mutate(indep)
        checked += 1
        for off in as_of_offsets:
            i = len(df) - 1 - off
            if i < PARITY_WARM_BARS:
                continue
            ours = PE.stations_for(sym, df, as_of_i=i).board_word
            theirs = str(indep[i])
            compared += 1
            if ours != theirs:
                mismatches.append(f"{sym}@-{off}: engine={ours} independent={theirs}")
    handoff = ("" if v12_1_present else
               "  [handoff] pine/ holds SS_v12_0_1.pine only; SS v12.1 is described in "
               "PINE_LANE_PRIMER_2026-08-15 §2 but is NOT in the repo, so marker-level "
               "parity against v12.1 itself is OWED, not discharged.")
    if not compared:
        return False, "VACUOUS: nothing was compared" + handoff
    if mismatches:
        return False, f"mismatch list ({len(mismatches)}): {'; '.join(mismatches[:6])}" + handoff
    skip_note = ("" if not skipped else
                 f"  SKIPPED {len(skipped)} symbol(s) with less than "
                 f"{PARITY_WARM_BARS + 400} 4h bars of pre-fixture-day history "
                 f"(the independent EMA is SMA-seeded and needs the warm-up): "
                 f"{', '.join(skipped)}.")
    # THE DENOMINATOR IS THE ROSTER'S LENGTH, NEVER A TYPED COUNT (OR-1 STEP C,
    # CONVENTIONS §6.4). This line read "{checked}/10 symbols" while the loop above
    # already walked REGISTER['ROSTER']: a VALUE dependent with no NAME in it, the
    # shape a name-only grep reports clean. On the 18-symbol roster of 2026-09-21 it
    # would have printed "13/10 symbols".
    n_roster = len(OD.REGISTER["ROSTER"]["value"])
    return True, (f"{checked}/{n_roster} roster symbols x {len(as_of_offsets)} as-of points = {compared} "
                  f"station-word comparisons against a SECOND state machine with its own "
                  f"EMA/ATR/cross recursions (no engine.indicators, no posture_engine) — "
                  f"mismatch list EMPTY (= pass)." + skip_note + handoff)


def f_br_1() -> None:
    # The break flips one word: the fixture must notice a WORD changing, which
    # is the thing the contract actually names.
    def _flip(words):
        w = words.copy()
        w[-1] = "DEAD" if w[-1] != "DEAD" else "ARMED"
        return w
    prove("F-BR-1", "PARITY — station WORDS vs an independent transcription, symbol for symbol",
          lambda: _parity_compare(mutate=_flip), lambda: _parity_compare())


# ═══════════════════════════════════════════════ F-BR-2 · TOLL PRESENCE

RATIO_WORDS = ("R:R", "net_rr", "net R:R")


def _toll_scan(src: str, doc: str) -> tuple[bool, str]:
    """A cost-free outcome column fails the build. Two legs, code and render."""
    tree = ast.parse(src)
    offenders = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "net_rr":
            args = [a.arg for a in node.args.args]
            if "toll_price" not in args:
                offenders.append("net_rr() does not take a toll")
    # every rendered ratio must carry its toll in the same table row
    for m in re.finditer(r"<tr>(?:(?!</tr>).)*?NET R:R(?:(?!</tr>).)*?</tr>", doc, re.S):
        if "toll" not in m.group(0):
            offenders.append("a rendered NET R:R row prints no toll")
    # FAIL CLOSED. The first version looped over NET R:R rows and, if the regex
    # matched none (a cosmetic restyle away from <tr>), passed vacuously. It also
    # accepted the bare WORD "toll" — which render_html hardcodes elsewhere — so
    # a value-free or fabricated ratio slipped through. Both are repaired here:
    # the count must equal the number of cards, and every ratio is RE-DERIVED
    # from the reward/risk/toll the page itself prints.
    cards = len(re.findall(r'class="card-h"', doc))
    rows = re.findall(r"<tr>(?:(?!</tr>).)*?NET R:R(?:(?!</tr>).)*?</tr>", doc, re.S)
    if cards and len(rows) != cards:
        offenders.append(f"{cards} card(s) but {len(rows)} NET R:R row(s) — fail closed")
    for row in rows:
        m = re.search(r"after toll\s+([0-9.]+)\s+ATR\s*=\s*([0-9.,eE+-]+)", row)
        if not m:
            offenders.append("a NET R:R row prints no toll VALUE (the bare word is not a toll)")
            continue
        try:
            float(m.group(1)); float(m.group(2).replace(",", ""))
        except ValueError:
            offenders.append("a NET R:R row's toll is not a number")
    if "R:R" in doc and not rows:
        offenders.append("document prints a ratio and no NET R:R row was found")
    if offenders:
        return False, "; ".join(sorted(set(offenders)))
    return True, (f"net_rr() takes toll_price; {len(rows)} NET R:R row(s) for {cards} "
                  f"card(s) — counts reconcile, and every row carries a NUMERIC per-lens "
                  f"toll in ATR and in price from the ORACLE GRID")


def f_br_2() -> None:
    src = (ROOT / "scripts" / "oracle_daily.py").read_text()
    broken = re.sub(r"toll_atr\{[^}]*\}", "", HTML)
    broken = HTML.replace("after toll", "").replace("toll", "TOLLREMOVED")
    prove("F-BR-2", "TOLL PRESENCE — no cost-free number prints anywhere",
          lambda: _toll_scan(src.replace("def net_rr(reward: float, risk: float, toll_price: float)",
                                         "def net_rr(reward, risk)"), broken),
          lambda: _toll_scan(src, HTML))


# ══════════════════════════════════════════════════════ F-BR-3 · FIREWALL

BANNED_IN_DECISION = ("analytics",)

# BR-1 §2 says engine modules are "imported read-only, trading disabled, never
# modified" — importing is contemplated, CALLING is what must not happen. And
# `engine.trading` IS in the closure: tierc2_rules -> engine.s1 -> `from
# engine.trading import TradeResult`. That is the ratified TC2 module's own
# inherited import, not something this build introduced, so banning the import
# would be banning the rule card. What this fixture bans is the journal (which
# must be unreachable at all) and any REFERENCE to a trading symbol from
# oracle code.
BANNED_ANYWHERE = ("forward_log", "positions")

# THE INHERITED IMPORTS, NAMED HONESTLY. The first version of this fixture
# banned the bare token "journal" and matched with `x == m or
# x.startswith(m + ".")` — which can never match `engine.journal`. So the ban
# was DEAD, and the build document printed "no journal ... module is reachable"
# as acceptance evidence. That sentence was FALSE: engine/s1.py does
# `from engine.journal import iso`, so engine.journal has been in the closure
# all along. The repair is not to hide it but to state it and to police what
# actually matters — that no journal is READ.
INHERITED_DISCLOSED = {
    "engine.trading": "TradeResult",
    "engine.journal": "iso",
}
# The chain both arrive by, and the only one they may arrive by.
INHERITED_VIA = "tierc2_rules -> engine.s1"
JOURNAL_READ_CALLS = ("read_journal", "load_journal", "journal_rows", "read_trades",
                      "load_trades", "open_journal", "journal(")


def _closure(modname: str) -> set[str]:
    code = ("import sys, json; sys.path.insert(0,'.'); sys.path.insert(0,'scripts'); "
            f"import {modname}; "
            "print(json.dumps(sorted(set(sys.modules))))")
    out = subprocess.run([sys.executable, "-c", code], cwd=ROOT,
                         capture_output=True, text=True)
    if out.returncode != 0:
        raise RuntimeError(out.stderr[-400:])
    return set(json.loads(out.stdout.strip().splitlines()[-1]))


def _firewall(extra_banned=(), extra_src="") -> tuple[bool, str]:
    bad = []
    dec = _closure("posture_engine")
    for m in list(BANNED_IN_DECISION) + list(extra_banned):
        hits = [x for x in dec if x == m or x.startswith(m + ".")]
        if hits:
            bad.append(f"posture_engine reaches {sorted(hits)[:3]}")
    both = dec | _closure("oracle_daily")
    # COMPONENT-WISE matching: a banned token is banned at ANY dotted position,
    # so `engine.forward_log` cannot hide behind a top-level-only test.
    def _reaches(mod: str, banned: str) -> bool:
        return banned in mod.split(".")
    for m in BANNED_ANYWHERE:
        hits = [x for x in both if _reaches(x, m)]
        if hits:
            bad.append(f"oracle closure reaches {sorted(hits)[:3]}")
    # The two inherited modules are permitted, but ONLY as inherited: no oracle
    # source may import or name them, and no journal READ may be called.
    src_all = "\n".join((ROOT / "scripts" / f).read_text()
                         for f in ("oracle_daily.py", "posture_engine.py")) + extra_src
    for mod in INHERITED_DISCLOSED:
        if re.search(rf"\b(?:from|import)\s+{re.escape(mod)}\b", src_all):
            bad.append(f"an oracle source imports {mod} directly (must be inherited only)")
    for call in JOURNAL_READ_CALLS:
        if call in src_all:
            bad.append(f"an oracle source calls a journal read: {call}")
    srcs = {p: (ROOT / "scripts" / p).read_text()
            for p in ("oracle_daily.py", "posture_engine.py")}
    srcs["<injected>"] = extra_src
    for name, src in srcs.items():
        if re.search(r"\b(?:from|import)\s+engine\.trading\b", src) or \
           re.search(r"\btrading\.[A-Za-z_]", src):
            bad.append(f"{name} references a trading symbol directly")
        for w in ("win_rate", "expectancy", "hit_rate", "pnl", "net_r"):
            if re.search(rf"\b{w}\s*=", src):
                bad.append(f"aggregation symbol {w} assigned in {name}")
    if bad:
        return False, "; ".join(sorted(set(bad)))
    present = {m: (m in both) for m in INHERITED_DISCLOSED}
    return True, (
        f"posture_engine closure is analytics-free ({len(dec)} modules); no forward_log "
        f"and no positions module is reachable (component-wise match); no oracle source "
        f"imports or names a trading or journal module; no journal read is called; no "
        f"outcome-aggregation symbol is assigned. "
        f"DISCLOSED, NOT DENIED — these ARE in the closure, inherited via "
        f"{INHERITED_VIA}: " +
        "; ".join(f"{m} (only {sym!r}) present={present[m]}"
                  for m, sym in INHERITED_DISCLOSED.items()) +
        ". BR-1 §2 permits engine modules 'imported read-only, trading disabled'; what "
        "§2 forbids is a journal READ, and that is what is asserted above.")


def f_br_3() -> None:
    prove("F-BR-3", "FIREWALL — import graph, not prose",
          # the break plants a direct journal READ, the thing §2 actually forbids
          lambda: _firewall(extra_src="from engine.journal import read_journal\n"),
          lambda: _firewall())


# ═══════════════════════════════════════ F-BR-4 · THUMBNAIL PROVENANCE

def _extract_payloads(doc: str) -> dict[str, str]:
    """Brace-match each inlined assignment. A regex cannot balance braces, and
    the payload JSON is nested, so this walks the text — string-aware, because
    a '}' inside a JSON string must not close the object."""
    pays: dict[str, str] = {}
    for m in re.finditer(r'window\.__PAYLOADS\[("(?:[^"\\]|\\.)*")\]=', doc):
        i = m.end()
        depth, in_str, esc = 0, False, False
        start = i
        while i < len(doc):
            ch = doc[i]
            if in_str:
                if esc:
                    esc = False
                elif ch == "\\":
                    esc = True
                elif ch == '"':
                    in_str = False
            elif ch == '"':
                in_str = True
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    break
            i += 1
        pays[m.group(1)] = doc[start:i + 1]
    return pays


def _thumbnails(doc: str) -> tuple[bool, str]:
    pays = _extract_payloads(doc)
    bad, ok_n = [], 0
    for canvas in re.finditer(r'<canvas[^>]*data-payload="([^"]+)"[^>]*>', doc):
        name = canvas.group(1)
        key = json.dumps(name)
        if key not in pays:
            bad.append(f"{name}: no inlined payload")
            continue
        pl = json.loads(pays[key])
        blob = json.dumps(pl["data"], sort_keys=True, separators=(",", ":")).encode()
        recomputed = hashlib.sha256(blob).hexdigest()
        if recomputed != pl["meta"]["sha256"]:
            bad.append(f"{name}: data-block sha mismatch")
            continue
        tail = doc[canvas.end(): canvas.end() + 900]
        if recomputed not in tail:
            bad.append(f"{name}: sha absent from the strip's own footer")
            continue
        ok_n += 1
    # The first version checked provenance only, so a render with the entire
    # paint routine deleted still passed — and the same function is the daily
    # unattended self-check. A strip whose bytes are provenanced but never drawn
    # is a blank box with a sha under it. Assert the painter is present too.
    need_js = ("function heatCanvas", "createImageData", "putImageData",
               "function divRGB", "function paintStrips",
               "addEventListener('DOMContentLoaded',paintStrips)")
    missing_js = [t for t in need_js if t not in doc]
    if missing_js:
        bad.append(f"paint routine absent from the render: missing {missing_js}")
    if bad:
        return False, "; ".join(bad[:5])
    return True, (f"{ok_n} strips; each canvas binds a payload whose meta.sha256 "
                  f"recomputes from its own data block and is printed in that strip's "
                  f"footer (the shipped VIZ-4 convention: data-block sha, not file sha); "
                  f"and the paint routine (divRGB/heatCanvas/putImageData/paintStrips + "
                  f"its DOMContentLoaded hook) is present in the document")


def f_br_4() -> None:
    # NB the replacement must be \g<1>, not \1: "\1" + "0"*64 reads as group 100.
    prove("F-BR-4", "THUMBNAIL PROVENANCE — strip bytes derive from a sha-stamped payload",
          lambda: _thumbnails(re.sub(r'("sha256":")[0-9a-f]{64}',
                                     r"\g<1>" + "0" * 64, HTML)),
          lambda: _thumbnails(HTML))


# ═════════════════════════════════════════ F-BR-5 · ANCHOR DETERMINISM

def _anchors(perturb=False) -> tuple[bool, str]:
    lines, bad = [], []
    for sym in OD.REGISTER["ROSTER"]["value"]:
        df = OD.load_lens(sym, "4h")
        a1 = PE.last_tide_flip(PE.build_frame(df), len(df) - 1)
        df2 = df.copy()
        if perturb:
            # The anchor is an e89-vs-e316 crossing, so a single-bar nudge cannot
            # move it — the break has to bend the slow ribbons. Ramp the last 400
            # closes; that genuinely relocates the flip.
            n = min(400, len(df2))
            ramp = np.linspace(1.0, 1.8, n)
            df2.iloc[-n:, df2.columns.get_loc("close")] = \
                df2["close"].to_numpy("float64")[-n:] * ramp
        a2 = PE.last_tide_flip(PE.build_frame(df2), len(df2) - 1)
        if a1 != a2:
            bad.append(f"{sym}: {a1} != {a2}")
        lines.append(f"{sym.replace('USDT','')}@{a1[1]}")
    if bad:
        return False, "; ".join(bad[:4])
    return True, ("anchor identical across two computations from the same substrate; "
                  "per-asset anchor timestamps: " + ", ".join(lines))


def f_br_5() -> None:
    prove("F-BR-5", "ANCHOR DETERMINISM — the C-4 tide-flip anchor, twice",
          lambda: _anchors(perturb=True), lambda: _anchors(perturb=False))


# ═══════════════════════════════════════ F-BR-6 · REFRESH IDEMPOTENCE

# THE SECTION NAMES (OR-1 STEP F, 2026-09-21). The contract's eight, in the operator's
# order, COPIED from the queue file and not read off the module under test. Every
# selector in this file finds a section by how its <h2> STARTS, so these eight strings
# are the coupling between the fixtures and the typesetting, typed ONCE here.
SECTIONS = ("Front Page", "The Docket", "The Watch", "Tide Tables", "Telegrams",
            "The Market Page", "Yesterday's Returns", "Colophon")
(SEC_BOARD, SEC_DOCKET, SEC_WATCH, SEC_TIDE, SEC_TELEGRAMS, SEC_MARKET, SEC_RETURNS,
 SEC_COLOPHON) = SECTIONS
# What F-BR-6 compares, and one thing each section MUST contain to count as found: the
# Board is a table, The Watch holds the strips.
REFRESH_SECTIONS = ((SEC_BOARD, "<table"), (SEC_WATCH, "<canvas"))
# The pre-STEP-F names, kept ONLY as F-BR-6's vacuity plant.
PRE_STEP_F_SECTIONS = (("The Board", "<table"), ("The Watch", "<canvas"))


# THE VACUOUS PASS, CLOSED (OR-1 STEP F). _sec() returns '' when no heading matches. The
# first version of _refresh compared _sec(d1, name) with _sec(d2, name) and nothing else,
# so the day a heading was renamed — STEP F renamed 'The Board' to 'Front Page' — it
# would have compared '' with '' and reported "byte-identical" for ever: in this fixture
# AND in the wrapper's daily production self-check, which calls this same function
# (oracle_wrapper.self_checks -> refresh_idempotence, the rows G-BR2-2 counts). A
# section that is missing, empty, or lacks the one thing it exists to show is now a
# FAIL that says so, and the old names are a standing break-leg plant.
def _refresh(tamper=False, sections=None, view=None) -> tuple[bool, str]:
    """`_refresh(tamper=False)` is a PRODUCTION API (the wrapper's per-edition self-check):
    the two new parameters are optional and are used by F-BR-6's break leg alone."""
    sections = REFRESH_SECTIONS if sections is None else sections
    view = OD.build_view(log=lambda *a, **k: None) if view is None else view
    d1 = OD.render_html(view, DATE, PE.canon_sha())
    heat0 = view["assets"][0]["heat"]
    try:
        if tamper:
            view["assets"][0]["heat"] = heat0 + 0.5
        d2 = OD.render_html(view, DATE, PE.canon_sha())
    finally:
        view["assets"][0]["heat"] = heat0          # a shared view leaves as it came
    void, diffs, sizes = [], [], []
    for name, must in sections:
        s1, s2 = _sec(d1, name), _sec(d2, name)
        if not s1.strip() or not s2.strip():
            void.append(f"no <h2> section starts with {name!r}")
        elif must not in s1 or must not in s2:
            void.append(f"the {name!r} section carries no {must!r}")
        elif s1 != s2:
            diffs.append(f"{name}: {len(s1)} B vs {len(s2)} B")
        else:
            sizes.append(f"{name} {len(s1):,} B")
    if void:
        return False, ("VACUOUS — " + "; ".join(void) + ": there is nothing to compare, and "
                       "'' == '' is not idempotence")
    if diffs:
        return False, "; ".join(diffs)
    return True, (f"{' and '.join(sizes)} byte-identical across two renders over unchanged "
                  f"data; both sections found, each carrying its table / its strips")


def _sec(doc: str, name: str) -> str:
    """The HTML from the <h2> that STARTS with `name` to the next <h2>; '' if none does.
    Never compare two of these without checking for '' first (see _refresh)."""
    for p in re.split(r"<h2>", doc)[1:]:
        if p.lower().startswith(name.lower()):
            return p
    return ""


def f_br_6() -> None:
    view = _pristine_view()
    # (name, the finding it MUST produce, how it is planted) — judged one at a time
    plants = (
        ("DATA PLANT (the first Board row's heat moved between the two renders)",
         f"{SEC_BOARD}:", dict(tamper=True, view=view)),
        ("SELECTOR PLANT (the pre-STEP-F heading names: 'The Board' matches nothing)",
         "VACUOUS", dict(sections=PRE_STEP_F_SECTIONS, view=view)),
        ("SELECTOR PLANT (a heading that is found, over a section without its content)",
         "VACUOUS", dict(sections=((SEC_TELEGRAMS, "<canvas"),), view=view)),
    )

    def _break() -> tuple[bool, str]:
        green, out = False, []
        for name, must, kw in plants:
            ok, detail = _refresh(**kw)
            if not ok and must in detail:
                out.append(f"{name} -> RED: {detail}")
            else:
                green = True
                out.append(f"{name} -> " + ("GREEN" if ok else
                           f"RED FOR THE WRONG REASON (nothing says {must!r}): {detail}"))
        return green, " ‖ ".join(out)

    prove("F-BR-6", "REFRESH IDEMPOTENCE — the refresh edition (/oracle refresh, slot "
                    "on-demand-refresh) over unchanged data, and never a comparison of "
                    "nothing with nothing",
          _break, lambda: _refresh(tamper=False))


# ══════════════════════════════════════════════════════ F-BR-7 · R1 FORMAT

R1_LINE = re.compile(r"^[A-Z0-9]+ (?:LIS_ABOVE|LIS_BELOW|INVAL|TARGET|ENTRY) "
                     r"-?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?$")


def _r1(doc: str) -> tuple[bool, str]:
    m = re.search(r'<pre class="r1">(.*?)</pre>', doc, re.S)
    if not m:
        return False, "no R1 block in the document"
    import html as _h
    lines = [ln for ln in _h.unescape(m.group(1)).strip().splitlines() if ln.strip()]
    # OR-2 R-1: a stale row's lines are HELD beneath the block, struck through. They are
    # read too — an all-stale edition has an EMPTY paste block, and "0 lines, every one
    # conforming" would otherwise be the whole of this fixture's evidence that day.
    mh = re.search(r'<pre class="held">(.*?)</pre>', doc, re.S)
    held = [re.sub(r"</?s>", "", ln) for ln in (mh.group(1).splitlines() if mh else [])
            if ln.strip()]
    held = [_h.unescape(ln) for ln in held]
    bad = [ln for ln in lines + held if not R1_LINE.match(ln.strip())]
    if bad:
        return False, f"{len(bad)} non-conforming line(s), first: {bad[0]!r}"
    if not lines and not held:
        return False, "the R1 block and the HELD block are both empty — nothing to check"
    return True, (f"{len(lines)} paste-ready alert lines + {len(held)} HELD (stale wire), "
                  f"every one matching <SYMBOL> <TAG> <PRICE> — prices only, no prose, "
                  f"no advice")


def f_br_7() -> None:
    broken = HTML.replace('<pre class="r1">',
                          '<pre class="r1">BTCUSDT: consider a long here\n', 1)
    prove("F-BR-7", "R1 FORMAT — alert block parses as price levels only",
          lambda: _r1(broken), lambda: _r1(HTML))


# ═════════════════════════════════════════════ F-BR-8 · PROVENANCE FOOTER

# One payload sha per roster symbol, checked BY NAME, not by a count. The line read
# `n_sha >= 10` (the old roster's size typed as a number, OR-1 STEP C / CONVENTIONS
# §6.4), then `n_sha >= n_roster` — but n_sha counted EVERY "sha256 <hex>" in the
# footer, and the footer also carries the posture canon sha. On an 18-symbol roster
# that is 19 stamps against a floor of 18: an edition that lost ONE payload stamp
# (17 + canon = 18) stayed green while the pass line claimed the floor was the
# roster's length. A >= floor is also blind to a duplicate stamp masking a missing
# one, so the test is SET EQUALITY against the names the render must print —
# REGISTER['ROSTER'] x REGISTER['LENS'], the same two rows oracle_daily builds the
# payload name from (oracle_daily.py:758), never typed here.
# CONSEQUENCE, unchanged and still deliberate: an edition printed from a DIFFERENT
# roster than the current one is red here — it is not an edition of this roster
# (F-BR-16 says which symbols differ). It now names them here too.
_PAY_STAMP = re.compile(r"payload (oracle_mantle_[0-9A-Z]+_[^ <]*\.json) sha256 [0-9a-f]{64}")


def _footer(doc: str) -> tuple[bool, str]:
    m = re.search(r"<footer>(.*?)</footer>", doc, re.S)
    if not m:
        return False, "no footer"
    foot = m.group(1)
    lens = OD.REGISTER["LENS"]["value"]
    want = {f"oracle_mantle_{s}_{lens}.json" for s in OD.REGISTER["ROSTER"]["value"]}
    got = _PAY_STAMP.findall(foot)
    unstamped = sorted(want - set(got))
    stray = sorted(set(got) - want)
    twice = sorted({n for n in got if got.count(n) > 1})
    row = (f"one payload sha per roster symbol ({len(got)} stamp(s) for a roster of "
           f"{len(want)}"
           + (f"; UNSTAMPED {unstamped}" if unstamped else "")
           + (f"; not on the roster {stray}" if stray else "")
           + (f"; stamped twice {twice}" if twice else "") + ")")
    need = {
        "DISPLAY-ONLY header": "DISPLAY-ONLY" in doc.split("<h2>")[0],
        "date": DATE in foot,
        row: not unstamped and not stray and not twice,
        "CERTIFIED list": "CERTIFIED:" in foot,
        "NOT CERTIFIED list": "NOT CERTIFIED:" in foot,
        "posture canon sha": PE.canon_sha() in foot,
    }
    missing = [k for k, v in need.items() if not v]
    if missing:
        return False, "missing: " + ", ".join(missing)
    return True, (f"DISPLAY-ONLY header, date {DATE}, exactly one payload sha256 stamp for "
                  f"each of the roster's {len(want)} symbols and for nothing else (the names "
                  f"derived from REGISTER['ROSTER'] x REGISTER['LENS'], never typed), the "
                  f"station canon sha on its own row, and BOTH the certified and "
                  f"not-certified lists present")


def f_br_8() -> None:
    prove("F-BR-8", "PROVENANCE FOOTER on the brief HTML",
          lambda: _footer(re.sub(r"NOT CERTIFIED:.*?<br>", "", HTML, flags=re.S)),
          lambda: _footer(HTML))


# ══════════════════════════════════════════════════════════ F-BR-9 · BOX

def _box(extra: Path | None = None) -> tuple[bool, str]:
    ex = ROOT / "exchange"
    offenders = [str(p.relative_to(ROOT)) for p in ex.rglob("*")
                 if p.is_file() and (p.suffix in (".parquet", ".html")
                                     or p.name.startswith("oracle_"))]
    if extra is not None:
        offenders.append(str(extra))
    if offenders:
        return False, f"{len(offenders)} forbidden artifact(s) under exchange/: {offenders[:3]}"
    html_p = OD.OUT_DIR / f"oracle_{DATE}.html"
    tape_p = OD.TAPE_DIR / f"oracle_tape_{DATE}.parquet"
    return True, (f"no .html and no .parquet under exchange/; the render lives at "
                  f"{html_p.relative_to(ROOT)} ({html_p.stat().st_size:,} B) and the tape "
                  f"at {tape_p.relative_to(ROOT)} ({tape_p.stat().st_size:,} B) — "
                  f"pointer lines only on the bus")


def f_br_9() -> None:
    prove("F-BR-9", "BOX — the render and the tape never enter exchange/",
          lambda: _box(extra=Path("exchange/reports/oracle_PRETEND.parquet")),
          lambda: _box())


# ════════════════════════════════ F-BR-10 · CALIBRATION PURITY (A1-4)

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


def _calibration(doc: dict) -> tuple[bool, str]:
    # Token-boundary matching, not substring: `open_window_ages_bars` contains
    # "win" and is display machinery, not an outcome. A banned term must appear
    # as a whole underscore-delimited token of a key name.
    def _stem(t: str) -> str:
        # plural forms escaped the first version: n_wins, losses, outcomes,
        # total_returns all passed a strict token-subset test. Stem them.
        for suf in ("ies", "es", "s"):
            if len(t) > 3 and t.endswith(suf):
                return t[: -len(suf)] + ("y" if suf == "ies" else "")
        return t

    hits = []
    for k in _keys_deep(doc):
        toks = {_stem(t) for t in re.split(r"[^a-z0-9]+", k.lower()) if t}
        for w in OD.BANNED_CALIBRATION_KEYS:
            wt = {_stem(t) for t in re.split(r"[^a-z0-9]+", w.lower()) if t}
            if wt and wt <= toks:
                hits.append(f"{k} (matched {w!r})")
    if hits:
        return False, f"outcome/performance field(s) present: {sorted(set(hits))}"
    n = len(doc.get("per_asset", []))
    keys = sorted({k for a in doc.get("per_asset", []) for k in a})
    return True, (f"{n} per-asset records; keys {keys} — display-machinery "
                  f"distributions only, no outcome field, no signal-performance field "
                  f"(banned vocabulary of {len(OD.BANNED_CALIBRATION_KEYS)} terms scanned)")


def f_br_10() -> None:
    planted = json.loads(json.dumps(CAL))
    planted["per_asset"][0]["n_wins"] = 3             # the deliberate break — PLURAL,
    planted["per_asset"][1]["losses"] = 7             # the form that used to escape
    prove("F-BR-10", "CALIBRATION PURITY — no outcome field may reach calibration/",
          lambda: _calibration(planted), lambda: _calibration(CAL))


# ═══════════════════════ F-BR-11 · CALIBRATION TOTALITY (finding of 2026-08-21)
#
# `lines_in_sand` writes None on a side with no qualifying cluster. The
# calibration writer read that side with `lis.get(k, {})`, which never reaches
# its default when the key is PRESENT holding None, so `.get("fallback")` on None
# raised AttributeError. Every scheduled run from 2026-08-20T10:00Z to
# 2026-08-22T02:49Z died there — six runs, no calibration record for two days,
# and F-BR-4/6 and the tape check gated off behind the nonzero exit. The brief
# rendered before the crash, so nothing on screen said the record was missing.
#
# The same line carried a second, quieter defect: it read a "fallback" key that
# `lines_in_sand` never writes (the fallback is marked source="fallback"), so
# `lis_fallback_used` recorded False for every asset on every side since
# 2026-08-16 and was structurally incapable of recording anything else.
#
# This fixture pins BOTH: the record must be produced over a None-bearing view,
# and every side of it must agree with what `lines_in_sand` actually returned.
# It writes into a throwaway CAL_DIR so it never lands a file in the real lane.

_VIEW = None


def _pristine_view() -> dict:
    """ONE real view for the fixtures that only READ it (F-BR-6's break leg, F-BR-11,
    F-BR-15). Whoever changes a field puts it back, or works on a copy."""
    global _VIEW
    if _VIEW is None:
        _VIEW = OD.build_view(log=lambda *a, **k: None)
    return _VIEW


def _view_with_null_lis() -> dict:
    """The real view, with a None side FORCED on the first asset.

    Forced rather than found: on 2026-08-21 three of ten assets had no line
    above, but a day where every asset has both sides must still exercise the
    property, or the fixture goes quietly vacuous exactly when the market is calm.
    """
    global _VIEW
    if _VIEW is None:
        _VIEW = OD.build_view(log=lambda *a, **k: None)
    v = dict(_VIEW)
    v["assets"] = [dict(a) for a in _VIEW["assets"]]
    v["assets"][0]["lis"] = dict(v["assets"][0]["lis"], above=None)
    return v


def _lis_provenance(doc: dict, view: dict) -> tuple[bool, str]:
    """Every per-asset record carries both sides, and each side tells the truth:
    None when there is no line, True when it came from the fallback rule, False
    when it came from the primary rule."""
    by_sym = {a["symbol"]: (a["lis"] if isinstance(a["lis"], dict) else {})
              for a in view["assets"]}
    bad: list[str] = []
    seen = {"none": 0, "primary": 0, "fallback": 0}
    for rec in doc.get("per_asset", []):
        lis = by_sym.get(rec["asset"], {})
        got = rec.get("lis_fallback_used")
        if not isinstance(got, dict) or set(got) != {"above", "below"}:
            bad.append(f"{rec['asset']}: lis_fallback_used is {got!r}")
            continue
        for side in ("above", "below"):
            ln = lis.get(side)
            want = None if not ln else (ln.get("source") == "fallback")
            seen["none" if want is None else ("fallback" if want else "primary")] += 1
            if got[side] != want:
                bad.append(f"{rec['asset']}.{side}: recorded {got[side]!r}, "
                           f"lines_in_sand said {want!r} "
                           f"(source={(ln or {}).get('source')!r})")
    if not doc.get("per_asset"):
        return False, "no per-asset records — the calibration record was not produced"
    if bad:
        return False, f"lis provenance misrecorded: {sorted(bad)[:6]}"
    return True, (f"{len(doc['per_asset'])} per-asset records, both sides each; "
                  f"{seen['none']} side(s) with no line recorded None, "
                  f"{seen['primary']} primary, {seen['fallback']} fallback — "
                  f"write_calibration completed over a None-bearing view")


def f_br_11() -> None:
    view = _view_with_null_lis()
    real_dir = OD.CAL_DIR
    try:
        with tempfile.TemporaryDirectory() as td:
            OD.CAL_DIR = Path(td)          # never write into the real lane
            cal_p, _, _ = OD.write_calibration(view, "0000-00-00", "fixture")
            doc = json.loads(Path(cal_p).read_text())
    finally:
        OD.CAL_DIR = real_dir
    # the deliberate break: the pre-repair behaviour — every side flatly False,
    # including the side that has no line at all
    planted = json.loads(json.dumps(doc))
    for rec in planted["per_asset"]:
        rec["lis_fallback_used"] = {"above": False, "below": False}
    prove("F-BR-11", "CALIBRATION TOTALITY — a None line-in-sand side must not stop "
                     "the record, and each side's provenance must be told",
          lambda: _lis_provenance(planted, view),
          lambda: _lis_provenance(doc, view))


# ═════════════════════════ F-BR-12 · THE ALARM (T-7, ruled 2026-08-22)
# The operator's ruling of 2026-08-22 was "flagfile": any run ending rc != 0
# writes ORACLE_DOWN.flag, and the next clean run removes it.
#
# WHAT THIS FIXTURE PROVES, AND WHAT IT REFUSES TO PROVE. It would be easy, and
# worthless, to call raise_flag() and check that a file appeared. The 2026-08-20
# outage was never a missing writer — it was a failure path that reached the end
# of the process without telling anybody. So both legs drive the REAL main(),
# with the render replaced by a planted failure, and then read the flag off disk.
# What is under test is the WIRING.
#
# Nothing reaches the real lane: FLAG and LOCK are redirected into a
# TemporaryDirectory and reschedule_if_drifted is stubbed, so no fixture run
# calls launchctl, touches ~/Library/LaunchAgents, or drops a flag in the repo.

FIXTURE_BOOM = "F-BR-12-BOOM — deliberate render failure planted by the fixture"


def _alarm_probe(armed: bool) -> tuple[bool, str]:
    """Two runs through the real main(): one forced to fail, then one clean.

    `armed=False` replants the PRE-T-7 world — the run still fails, but nothing
    writes the flag. That is the break leg, and it must go red."""
    import oracle_wrapper as OW
    keep = {k: getattr(OW, k) for k in
            ("FLAG", "LOCK", "run_oracle", "reschedule_if_drifted", "raise_flag")}
    keep_failures = list(OW.FAILURES)

    def _boom(slot, zr, started, log=print, catchup=False):
        raise RuntimeError(FIXTURE_BOOM)

    def _clean(slot, zr, started, log=print, catchup=False):
        return 0

    try:
        with tempfile.TemporaryDirectory() as td:
            OW.FLAG = Path(td) / "ORACLE_DOWN.flag"
            OW.LOCK = Path(td) / ".oracle.lock"
            OW.reschedule_if_drifted = (
                lambda label, log=print: {"label": label, "drift": False,
                                          "missing": False, "want": {}, "had": {}})
            if not armed:
                OW.raise_flag = lambda *a, **k: OW.FLAG      # the silence, replanted
            OW.FAILURES.clear()
            sink = io.StringIO()
            with contextlib.redirect_stdout(sink):
                OW.run_oracle = _boom
                rc_fail = OW.main(["--job", "oracle", "--slot", "full"])
                up = OW.FLAG.exists()
                body = OW.FLAG.read_text(encoding="utf-8") if up else ""
                OW.run_oracle = _clean
                rc_ok = OW.main(["--job", "oracle", "--slot", "full"])
                still_up = OW.FLAG.exists()
            sentence, cap = OW.FLAG_SENTENCE, OW.FLAG_TB_LINES
    finally:
        for k, v in keep.items():
            setattr(OW, k, v)
        OW.FAILURES[:] = keep_failures

    if rc_fail == 0:
        return False, "the planted render failure exited 0 — there is nothing to alarm about"
    if not up:
        return False, (f"the run exited {rc_fail} and NO ORACLE_DOWN.flag was written — "
                       f"the failure is silent, which is the 2026-08-20 outage exactly")
    want = [("the traceback", FIXTURE_BOOM), ("the job", "JOB   oracle"),
            ("the slot", "SLOT  full"), ("the exit code", f"EXIT  {rc_fail}"),
            ("the UTC timestamp", "UTC   "), ("the sentence", sentence)]
    silent = [n for n, t in want if t not in body]
    if silent:
        return False, f"flag written but silent about: {', '.join(silent)}"
    m = re.search(r"LAST (\d+) TRACEBACK LINE\(S\)", body)
    if not m or not (1 <= int(m.group(1)) <= cap):
        return False, f"flag carries no traceback tail of 1..{cap} lines"
    if rc_ok != 0:
        return False, f"the follow-up run exited {rc_ok}, so the self-clear was never tested"
    if still_up:
        return False, "the clean run left the flag standing — the alarm never self-clears"
    return True, (f"failed run exited {rc_fail} and raised the flag carrying "
                  f"{m.group(1)} traceback line(s), job, slot, exit code, UTC stamp "
                  f"and the sentence; the next clean run exited 0 and the flag was gone")


def f_br_12() -> None:
    prove("F-BR-12", "THE ALARM — a run ending rc != 0 must leave ORACLE_DOWN.flag "
                     "behind, and the next clean run must take it away",
          lambda: _alarm_probe(armed=False),
          lambda: _alarm_probe(armed=True))


# ═══════════ F-BR-13 · C-0 — THE D-7 LOGGER MEASURES (OR-1 STEP B, 2026-09-21)
#
# FINDING C-0 (ORACLE_CHAIN_CLOSE_2026-08-16, reported-not-fixed for five weeks):
# write_calibration wrote the LITERAL `"maturity_withheld_fraction": 0.0` for
# every asset on every run, and recorded neither family-cap binding nor target
# buckets — the three families BR-2 WORK(1) is supposed to recalibrate FROM these
# files. 57 calibration JSONs are hollow for it. F-BR-10 could never have caught
# this: it polices which KEYS may exist, not whether a value was measured.
#
# A typed constant and a measured zero print the same digit, so this fixture
# cannot simply read the number. It proves measurement three ways:
#
#   (a) CODE     an AST scan of oracle_daily.py: no constant is ever assigned to
#                'maturity_withheld_fraction', to ANY key ending 'withheld_fraction'
#                (the roster carries the same number one dict up), or to any other
#                record STEP B added; VW.maturity() is really called; the family
#                cap and the target buckets are IMPORTED from their one definition
#                and never copied (CONVENTIONS §6.4).
#   (b) MOTION   a synthetic 1h frame whose 7d window holds 20 bars (then 12) is
#                pushed through the REAL level_registry -> write_calibration path
#                and the number on disk MOVES: 0.4, then 0.5; a deep window reads
#                0.0 — and the ROSTER fraction of that document moves with it
#                (9 of 100 levels). The bar count is cross-checked against
#                rolling_vwap itself: a VWAP recomputed by hand over exactly that
#                many bars must equal the value rolling_vwap printed. And MEASURING
#                IS NOT WITHHOLDING: on every frame the registry must still hold
#                exactly the finite VWAP levels rolling_vwap printed, byte-equal
#                with and without the measuring side-channel.
#                The OTHER TWO families get the same treatment, because the day's
#                roster cannot be trusted to exercise them (2026-09-19: all six
#                open cards bucket NEAR on both ATR bases, and NO_TARGET has never
#                occurred — a logger that typed "NEAR" for every card would have
#                been right all day): cards planted at the midpoint of every
#                brief_render bucket, a card with no reward, no card at all, and
#                clusters built with cap-1 / cap / cap+1 same-family members must
#                read exactly what their construction says.
#   (c) THE RUN  a real build_view over the live roster, written to a throwaway
#                CAL_DIR: every asset carries all three families, every record is
#                tied to an independent source (the ledger below), and the
#                measured block is NOT constant across assets.
#
# WHAT "RE-DERIVED" MEANS HERE — the ledger, record by record. It was earned the
# hard way. Round 1 of this fixture printed "each re-derived from the view" while
# it checked the headline `target_bucket` only for membership in the name list,
# the roster occupancy only for its sum, the 'daily' ATR basis not at all, the
# roster `maturity_roster` only for presence and the roster cap binding only for
# `clusters`. The OR-1 STEP B adversarial verifier (2026-09-21) planted five
# mutants in scratch copies of oracle_daily.py — a typed headline bucket, a typed
# occupancy dict, the 'daily' basis silently computed in the lens ATR, a roster
# `"withheld_fraction": 0.0` (finding C-0 itself, one dict up) and a typed
# at_cap/over_cap — and all five came back GREEN. The measured numbers were
# right; the fixture could not have told. A PASS line may claim only what the
# checks do, so each record is now tied to a source the logger does not write:
#
#   per asset
#     maturity_windows[].bars         recounted by hand from a freshly loaded 1h
#                                     frame (not through OD.window_bars)
#     maturity_windows[].line/band_ok those bars against the IMPORTED 16/60 floors
#     maturity_candidate_levels       the vwap_rolling levels of a registry REBUILT
#                                     without the measuring side-channel
#     maturity_withheld_levels,
#     maturity_withheld_fraction      from those bars, floors and candidates
#     family_cap_binding              recounted from the view's own clusters
#     target_distance_atr lens/daily  card['reward'] over st.atr / over a['atr_d']
#     target_bucket_by_atr lens/daily brief_render's edges applied to those
#     target_bucket                   == the basis REGISTER['TARGET_BUCKET_ATR'] names
#   whole roster, in BOTH documents (the real run and the motion run)
#     maturity_roster, family_cap_binding (all three keys),
#     target_bucket_occupancy, target_bucket_occupancy_by_atr
#                                     == summed / counted from per_asset
#     maturity_roster.withheld_fraction   non-zero on the motion run
#   the motion run alone, BY CONSTRUCTION
#     target buckets NEAR/MID/FAR/NO_TARGET/NONE on planted cards, the two ATR
#     bases seen to separate; cap binding {3, 2, 1} on built clusters
#     thresholds_in_force             windows, floors, cap, bucket edges, ATR basis
#                                     == the imported constants; an unruled
#                                     TARGET_BUCKET_ATR is listed as awaiting ruling
#
# THE HONEST CAVEAT, measured and printed by the real leg rather than hidden:
# on 7d/30d windows over 1h bars the windows hold ~168/~720 bars against floors
# of 16/60, so on a healthy cache the maturity fraction is a TRUE 0.0 for every
# asset. "Measured values differ across assets" is therefore discharged by the
# measured block as a whole (cap binding, target distance), and leg (b) is what
# proves the maturity number itself is alive.
#
# BREAK LEG: the pre-OR-1 world and its near relatives, one plant at a time. EACH
# plant must go red ON ITS OWN and FOR ITS OWN REASON — a plant that is red only
# because some other check tripped proves nothing about the check it was aimed
# at, so every plant names the finding it must produce and is void without it.
#   SOURCE     the literal 0.0 back on the per-asset key; the literal 0.0 on the
#              roster's `withheld_fraction` (against (a)).
#   DOCUMENT   a calibration document doctored back to the hollow shape the 57
#              old files have (against (b) and (c)); then the verifier's five
#              surviving mutants, a mistyped bar count, "NEAR" typed for every
#              card and `>` typed as `>=`, each replanted at the document level
#              against the one guard that answers it.
#   REGISTRY   withholding dressed as measuring: the immature 7d bands dropped
#              from the registry while the logger still counts them.

C0_KEY = "maturity_withheld_fraction"
C0_ASSET_KEYS = (C0_KEY, "maturity_candidate_levels", "maturity_withheld_levels",
                 "maturity_windows", "family_cap_binding", "target_bucket",
                 "target_bucket_by_atr", "target_distance_atr")
C0_ROSTER_KEYS = ("maturity_roster", "family_cap_binding",
                  "target_bucket_occupancy", "target_bucket_occupancy_by_atr")
C0_DOC_KEYS = ("schema_version", *C0_ROSTER_KEYS)
C0_THRESHOLD_KEYS = ("vwap_windows_d", "target_buckets_atr", "target_bucket_atr_basis")
# keys whose VALUE may never be a typed constant anywhere in oracle_daily.py. The
# sub-keys are here because a roster dict is written inline: `"withheld_fraction":
# 0.0` inside `"maturity_roster": {...}` is finding C-0 wearing a longer name.
C0_NO_LITERAL = frozenset((*C0_ASSET_KEYS, *C0_ROSTER_KEYS, "withheld_fraction",
                           "candidate_levels", "withheld_levels", "at_cap", "over_cap"))
C0_CAP_KEYS = ("clusters", "at_cap", "over_cap")
C0_THIN_BARS = (20, 12)       # 20: line ok (>=16), bands withheld (<60) · 12: both withheld
C0_NO_ESTATE = ("engine", "analytics", "journal", "trading", "forward_log",
                "positions", "posture_engine")


def _c0_ast(src: str) -> list[str]:
    """Leg (a). Scans CODE, not prose: comments and docstrings cannot satisfy it."""
    tree = ast.parse(src)
    bad: list[str] = []

    def _const(n) -> bool:
        return (isinstance(n, ast.Constant)
                or (isinstance(n, ast.UnaryOp) and isinstance(n.operand, ast.Constant)))

    def _guarded(k) -> bool:
        return isinstance(k, str) and (k in C0_NO_LITERAL or k.endswith("withheld_fraction"))

    fn = next((n for n in ast.walk(tree)
               if isinstance(n, ast.FunctionDef) and n.name == "write_calibration"), None)
    if fn is None:
        return ["write_calibration() not found"]
    # names bound ONLY to constants inside write_calibration: `x = 0.0; {key: x}`
    # is the same literal wearing a coat
    bound: dict[str, list[bool]] = {}
    for n in ast.walk(fn):
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name):
            bound.setdefault(n.targets[0].id, []).append(_const(n.value))
    typed = {k for k, v in bound.items() if v and all(v)}

    writes: dict[str, int] = {}
    for n in ast.walk(tree):
        pairs = []
        if isinstance(n, ast.Dict):
            pairs = [(k.value, v) for k, v in zip(n.keys, n.values)
                     if isinstance(k, ast.Constant) and _guarded(k.value)]
        elif (isinstance(n, ast.Assign) and len(n.targets) == 1
              and isinstance(n.targets[0], ast.Subscript)
              and isinstance(n.targets[0].slice, ast.Constant)
              and _guarded(n.targets[0].slice.value)):
            pairs = [(n.targets[0].slice.value, n.value)]
        for key, v in pairs:
            writes[key] = writes.get(key, 0) + 1
            if _const(v):
                bad.append(f"line {v.lineno}: '{key}' is assigned the typed constant "
                           f"{ast.unparse(v)} — finding C-0 replanted")
            elif isinstance(v, ast.Name) and v.id in typed:
                bad.append(f"line {v.lineno}: '{key}' is assigned `{v.id}`, a name bound "
                           f"only to a constant")
    # fail closed: a record this scan cannot SEE being written is not a record it
    # has cleared (a key built at run time would walk straight past the scan)
    unseen = [k for k in sorted(C0_NO_LITERAL) if not writes.get(k)]
    if unseen:
        bad.append(f"no write of {unseen} found in oracle_daily.py — fail closed")

    calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call)
             and isinstance(n.func, ast.Attribute) and n.func.attr == "maturity"
             and isinstance(n.func.value, ast.Name) and n.func.value.id == "VW"]
    if not calls:
        bad.append("analytics.vwap.maturity() is never called (no VW.maturity(...) in the code)")

    # §6.4 — the one definition is imported, never copied
    for n in ast.walk(tree):
        tg = (n.targets if isinstance(n, ast.Assign)
              else [n.target] if isinstance(n, (ast.AnnAssign, ast.AugAssign)) else [])
        for t in tg:
            if isinstance(t, ast.Name) and t.id in ("TARGET_BUCKETS", "FAMILY_CAP"):
                bad.append(f"line {n.lineno}: {t.id} is ASSIGNED locally — a copy of a "
                           f"constant that has one definition elsewhere")
    imp = {a.name for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)
           and n.module == "brief_render" for a in n.names}
    if not {"TARGET_BUCKETS", "target_bucket"} <= imp:
        bad.append(f"TARGET_BUCKETS/target_bucket are not imported from brief_render (got {sorted(imp)})")
    cap = next((n for n in ast.walk(tree)
                if isinstance(n, ast.FunctionDef) and n.name == "family_cap_binding"), None)
    if cap is None:
        bad.append("family_cap_binding() not found")
    else:
        if not any(isinstance(n, ast.Attribute) and n.attr == "FAMILY_CAP"
                   and isinstance(n.value, ast.Name) and n.value.id == "L" for n in ast.walk(cap)):
            bad.append("family_cap_binding() never reads L.FAMILY_CAP")
        for n in ast.walk(cap):
            if isinstance(n, ast.Compare) and any(
                    isinstance(c, ast.Constant) and isinstance(c.value, (int, float))
                    and not isinstance(c.value, bool) and c.value != 0
                    for c in [n.left, *n.comparators]):
                bad.append(f"line {n.lineno}: family_cap_binding() compares against a bare "
                           f"number — the cap was copied, not imported")
    return bad


_C0_SYNTH = None
_C0_FRESH: dict = {}
_C0_CLOSURE = None


def _c0_synthetic(gate: bool = False) -> dict:
    """A seeded random-walk market: 40 days of 1h bars, 300 4h bars. Returns the
    `vwap_maturity` records the REAL level_registry measures over a deep frame
    and over frames whose last 7 days are thinned to C0_THIN_BARS bars, and — so
    that measuring can be told from withholding — what the registry ended up
    holding beside what rolling_vwap itself printed.

    `gate=True` is the REGISTRY PLANT of the break leg and is never cached: the
    7d bands of a thin frame are dropped on their way into the registry while
    level_registry goes on counting them — the semantic change OR-1 STEP B was
    forbidden to make, in the one disguise the logged numbers cannot show."""
    global _C0_SYNTH
    if not gate and _C0_SYNTH is not None:
        return _C0_SYNTH
    rng = np.random.default_rng(13)
    hour = 3_600_000
    VW = OD.VW

    def frame(n: int, step: int) -> pd.DataFrame:
        close = 100.0 * np.exp(np.cumsum(rng.normal(0, 0.004, n)))
        open_ = np.concatenate([[close[0]], close[:-1]])
        spread = np.abs(rng.normal(0, 0.003, n)) * close
        return pd.DataFrame({
            "open_time": FIXTURE_DAY_MS + np.arange(n, dtype="int64") * step,
            "open": open_, "high": np.maximum(open_, close) + spread,
            "low": np.minimum(open_, close) - spread, "close": close,
            "volume": rng.uniform(50.0, 500.0, n)})

    h1, h4 = frame(24 * 40, hour), frame(300, 4 * hour)
    atr_d = OD.daily_atr(h1)
    t = h1["open_time"].to_numpy("int64")
    in7 = np.flatnonzero(t > t[-1] - 7 * 86_400_000)
    out = {"frames": {}, "vm": {}, "vwap_by_hand": {}, "kept7": {},
           "reg_vwap": {}, "printed": {}, "same_without": {}}
    real_add = OD.L.LevelRegistry.add
    thin = {"now": False}

    def gated_add(self, family, label, level, source_layer, timeframe=None):
        if thin["now"] and family == "vwap_rolling" and "7d" in str(label) and "σ" in str(label):
            return self                 # withheld — and still counted by the caller
        return real_add(self, family, label, level, source_layer, timeframe)

    for label, keep in (("deep", None), *[(f"thin{k}", k) for k in C0_THIN_BARS]):
        if keep is None:
            f = h1
        else:       # keep `keep` bars of the last 7d, evenly spaced, the last bar included
            pick = in7[np.unique(np.linspace(0, len(in7) - 1, keep).round().astype(int))]
            f = h1.iloc[np.concatenate([np.arange(in7[0]), pick])].reset_index(drop=True)
        vm: list[dict] = []
        thin["now"] = keep is not None
        if gate:
            OD.L.LevelRegistry.add = gated_add
        try:
            reg, _m, clusters = OD.level_registry("SYNTHUSDT", h4, f, atr_d, maturity_out=vm)
            reg0, _m0, clusters0 = OD.level_registry("SYNTHUSDT", h4, f, atr_d)
        finally:
            OD.L.LevelRegistry.add = real_add
        out["frames"][label], out["vm"][label] = f, vm
        out["kept7"][label] = len(in7) if keep is None else keep    # by construction
        ft = f["open_time"].to_numpy("int64")
        fsrc = VW.hlc3(f["high"].to_numpy("float64"), f["low"].to_numpy("float64"),
                       f["close"].to_numpy("float64"))
        fvol = f["volume"].to_numpy("float64")
        # MEASURING IS NOT WITHHOLDING: the registry against rolling_vwap's own print
        printed = 0
        for wd in OD.REGISTER["VWAP_WINDOWS_D"]["value"]:
            rv = VW.rolling_vwap(ft, fsrc, fvol, wd)
            printed += sum(1 for k in ("vwap", "band_up_1", "band_dn_1", "band_up_2", "band_dn_2")
                           if rv.get(k) is not None and np.isfinite(float(np.asarray(rv[k])[-1])))
        out["printed"][label] = printed
        out["reg_vwap"][label] = sum(1 for lv in reg.as_list() if lv["family"] == "vwap_rolling")
        out["same_without"][label] = (
            json.dumps(reg.as_list(), sort_keys=True) == json.dumps(reg0.as_list(), sort_keys=True)
            and len(clusters) == len(clusters0))
        # the count is the membership rolling_vwap used, or it is nothing: a VWAP
        # taken by hand over exactly `bars` trailing bars must reproduce its value
        n7 = next(w["bars"] for w in vm if w["window_d"] == 7)
        rv7 = VW.rolling_vwap(ft, fsrc, fvol, 7)["vwap"][-1]
        out["vwap_by_hand"][label] = (float(np.sum(fsrc[-n7:] * fvol[-n7:]) / np.sum(fvol[-n7:])),
                                      float(rv7), n7)
    if not gate:
        _C0_SYNTH = out
    return out


def _c0_fresh(sym: str) -> dict:
    """An INDEPENDENT look at one roster asset, for leg (c): the frames are loaded
    again, the window bars are recounted BY HAND (deliberately not through
    OD.window_bars — a recount by the function under test is no recount), and
    the registry is rebuilt WITHOUT the measuring side-channel, so the logged
    candidates can be held against levels that really entered a registry."""
    if sym not in _C0_FRESH:
        h4 = OD.load_lens(sym, "4h")
        h1 = OD.load_lens(sym, "1h", tail=24 * 400)       # build_view's own read
        t = h1["open_time"].to_numpy("int64")
        reg, _m, _c = OD.level_registry(sym, h4, h1, OD.daily_atr(h1))
        _C0_FRESH[sym] = {
            "bars": {int(wd): int((t > t[-1] - int(wd) * 86_400_000).sum())
                     for wd in OD.REGISTER["VWAP_WINDOWS_D"]["value"]},
            "n_levels": len(reg),
            "n_vwap": sum(1 for lv in reg.as_list() if lv["family"] == "vwap_rolling")}
    return _C0_FRESH[sym]


def _c0_hollow(doc: dict) -> dict:
    """The PRE-OR-1 document, replanted: exactly the shape the 57 old files have —
    the literal 0.0 on every asset, and the other two families simply absent."""
    d = json.loads(json.dumps(doc))
    for k in (*C0_DOC_KEYS, "schema_note"):
        d.pop(k, None)
    for k in C0_THRESHOLD_KEYS:
        d.get("thresholds_in_force", {}).pop(k, None)
    d["veto_rows_awaiting_ruling"] = [k for k in d.get("veto_rows_awaiting_ruling", [])
                                      if k != "TARGET_BUCKET_ATR"]
    for rec in d.get("per_asset", []):
        for k in C0_ASSET_KEYS:
            rec.pop(k, None)
        rec[C0_KEY] = 0.0
    return d


# The verifier's five surviving mutants (and one of our own), replanted at the
# DOCUMENT level: each doctor writes what that mutant of oracle_daily.py would have
# written, and nothing else, so exactly one guard is asked to answer for it.
def _c0_doc_headline(d: dict) -> dict:
    d = json.loads(json.dumps(d))
    for rec in d["per_asset"]:
        rec["target_bucket"] = "NEAR"
    return d


def _c0_doc_occupancy(d: dict) -> dict:
    d = json.loads(json.dumps(d))
    d["target_bucket_occupancy"] = {**{k: 0 for k in d["target_bucket_occupancy"]},
                                    OD.BUCKET_NO_CARD: len(d["per_asset"])}
    return d


def _c0_doc_daily_in_lens(d: dict) -> dict:
    d = json.loads(json.dumps(d))
    for rec in d["per_asset"]:
        rec["target_distance_atr"]["daily"] = rec["target_distance_atr"]["lens"]
        rec["target_bucket_by_atr"]["daily"] = rec["target_bucket_by_atr"]["lens"]
    return d


def _c0_doc_roster_fraction(d: dict) -> dict:
    d = json.loads(json.dumps(d))
    d["maturity_roster"]["withheld_fraction"] = 0.0     # finding C-0, one dict up
    return d


def _c0_doc_roster_cap(d: dict) -> dict:
    d = json.loads(json.dumps(d))
    d["family_cap_binding"]["at_cap"] = d["family_cap_binding"]["over_cap"] = 0
    return d


def _c0_doc_bars(d: dict) -> dict:
    d = json.loads(json.dumps(d))
    for rec in d["per_asset"]:
        rec["maturity_windows"][-1]["bars"] += 1        # a bar count nobody counted
    return d


def _c0_doc_all_near(d: dict) -> dict:
    """"NEAR" typed for every card on every basis. On the 2026-09-19 roster this
    doctor changes NOTHING in the real document — which is the point: only the
    planted cards of the motion run can tell it from a measurement."""
    d = json.loads(json.dumps(d))
    keep = (OD.BUCKET_NO_CARD,)
    for rec in d["per_asset"]:
        rec["target_bucket_by_atr"] = {b: (v if v in keep else "NEAR")
                                       for b, v in rec["target_bucket_by_atr"].items()}
        rec["target_bucket"] = rec["target_bucket"] if rec["target_bucket"] in keep else "NEAR"
    names = list(d["target_bucket_occupancy"])
    d["target_bucket_occupancy"] = {n: sum(1 for r in d["per_asset"] if r["target_bucket"] == n)
                                    for n in names}
    d["target_bucket_occupancy_by_atr"] = {
        b: {n: sum(1 for r in d["per_asset"] if r["target_bucket_by_atr"][b] == n) for n in names}
        for b in d["target_bucket_occupancy_by_atr"]}
    return d


def _c0_doc_over_is_at(d: dict) -> dict:
    """`>` typed as `>=`: over_cap reads what at_cap reads, the roster re-summed to
    match so that only a re-count can object."""
    d = json.loads(json.dumps(d))
    for rec in d["per_asset"]:
        rec["family_cap_binding"]["over_cap"] = rec["family_cap_binding"]["at_cap"]
    d["family_cap_binding"]["over_cap"] = d["family_cap_binding"]["at_cap"]
    return d


def _c0_built_clusters() -> tuple[list, dict]:
    """Three clusters through the REAL analytics.levels.cluster(), holding
    FAMILY_CAP-1, FAMILY_CAP and FAMILY_CAP+1 members of one family — so what
    family_cap_binding must say about them follows from the imported cap alone."""
    L = OD.L
    members = [{"family": "structure", "label": f"built {g}.{j}", "level": 100.0 * (g + 1) + 1e-6 * j,
                "source_layer": "fixture", "timeframe": None}
               for g, k in enumerate((L.FAMILY_CAP - 1, L.FAMILY_CAP, L.FAMILY_CAP + 1))
               for j in range(k)]
    return L.cluster(members, 1.0), {"clusters": 3, "at_cap": 2, "over_cap": 1}


def _c0_judge(src: str | None = None, doctor=None, gate: bool = False) -> tuple[list[str], dict]:
    """Every finding, untruncated, plus what the PASS line needs to say so."""
    global _VIEW, _C0_CLOSURE
    import brief_render as BR
    VW, L = OD.VW, OD.L
    bad = _c0_ast((ROOT / "scripts" / "oracle_daily.py").read_text() if src is None else src)

    # the import OR-1 STEP B added must stay what it was measured to be: stdlib only
    if _C0_CLOSURE is None:
        _C0_CLOSURE = _closure("brief_render")
    dragged = sorted(m for m in _C0_CLOSURE
                     if any(c in m.split(".") for c in C0_NO_ESTATE))
    if dragged:
        bad.append(f"brief_render's import closure now drags {dragged[:4]}")
    if OD.TARGET_BUCKETS is not BR.TARGET_BUCKETS or OD.target_bucket is not BR.target_bucket:
        bad.append("oracle_daily's TARGET_BUCKETS/target_bucket are not brief_render's objects")

    if _VIEW is None:
        _VIEW = OD.build_view(log=lambda *a, **k: None)
    view = _VIEW
    syn = _c0_synthetic(gate=gate)
    labels = ["deep", *[f"thin{k}" for k in C0_THIN_BARS]]
    # THE MOTION VIEW: shallow copies of the real assets, each family replaced on
    # some of them by an input whose right answer is known BY CONSTRUCTION. The
    # three families read three different keys (vwap_maturity / card / clusters),
    # so one asset may carry more than one plant.
    mids = [(n, (lo + 1.0) if np.isinf(hi) else (lo + hi) / 2.0) for n, lo, hi in BR.TARGET_BUCKETS]
    need = max(len(labels), len(mids) + 3)
    if len(view["assets"]) < need:
        return [f"roster of {len(view['assets'])} is too small to carry the motion legs "
                f"(needs {need})"], {}
    motion = dict(view)
    motion["assets"] = [dict(a) for a in view["assets"]]
    carrier = {}
    for a, label in zip(motion["assets"], labels):
        a["vwap_maturity"] = syn["vm"][label]
        carrier[label] = a["symbol"]
    # cards planted at the MIDPOINT of every brief_render bucket in the lens ATR,
    # then a card that names no target, no card at all, and one card planted in
    # the DAILY ATR (the far bucket), so the two bases are seen apart
    t_plan = []                          # (symbol, what was planted, basis, bucket, distance)
    for a, (n, d) in zip(motion["assets"], mids):
        a["card"] = {"reward": d * float(a["station"].atr)}
        t_plan.append((a["symbol"], f"a card at {d:g} lens-ATR", "lens", n, round(d, 6)))
    a = motion["assets"][len(mids)]
    a["card"] = {"reward": None}
    t_plan.append((a["symbol"], "a card with no reward", "lens", OD.BUCKET_NO_TARGET, None))
    a = motion["assets"][len(mids) + 1]
    a["card"] = None
    t_plan.append((a["symbol"], "no card", "lens", OD.BUCKET_NO_CARD, None))
    a = motion["assets"][len(mids) + 2]
    a["card"] = {"reward": mids[-1][1] * float(a["atr_d"])}
    t_plan.append((a["symbol"], f"a card at {mids[-1][1]:g} daily-ATR", "daily", mids[-1][0],
                   round(mids[-1][1], 6)))
    built, built_want = _c0_built_clusters()
    motion["assets"][-1]["clusters"] = built
    cap_carrier = motion["assets"][-1]["symbol"]

    real_dir = OD.CAL_DIR
    try:
        with tempfile.TemporaryDirectory() as td:
            OD.CAL_DIR = Path(td)          # never write into the real lane
            p_real, _, _ = OD.write_calibration(view, "0000-00-00", "fixture-c0-real")
            p_mot, _, _ = OD.write_calibration(motion, "0000-00-00", "fixture-c0-motion")
            doc = json.loads(Path(p_real).read_text())
            mot = json.loads(Path(p_mot).read_text())
    finally:
        OD.CAL_DIR = real_dir
    if doctor is not None:
        doc, mot = doctor(doc), doctor(mot)

    # ── (b) MOTION ─────────────────────────────────────────────────────────
    # what the floors withhold, from the CONSTRUCTION of each frame: the 7d window
    # holds kept7 bars, the 30d window is deep in all three; a window offers 1 line
    # + 4 bands (up/dn x 1s/2s), so the roster of candidates is 5 per window
    n_win = len(OD.REGISTER["VWAP_WINDOWS_D"]["value"])
    want = {label: round(((syn["kept7"][label] < VW.LINE_MIN_BARS) * 1
                          + (syn["kept7"][label] < VW.BAND_MIN_BARS) * 4) / (5 * n_win), 6)
            for label in labels}
    got = {}
    for label in labels:
        rec = next(r for r in mot["per_asset"] if r["asset"] == carrier[label])
        got[label] = rec.get(C0_KEY)
        bars7 = next((w.get("bars") for w in rec.get("maturity_windows", [])
                      if w.get("window_d") == 7), None)
        exp_bars = syn["kept7"][label]
        if bars7 != exp_bars:
            bad.append(f"motion/{label}: the 7d window holds {exp_bars} bars, the record says {bars7!r}")
        if got[label] != want[label]:
            bad.append(f"motion/{label}: fraction on disk is {got[label]!r}, the floors "
                       f"{VW.LINE_MIN_BARS}/{VW.BAND_MIN_BARS} withhold {want[label]} — "
                       f"the number does not move with the data")
        hand, rv, n7 = syn["vwap_by_hand"][label]
        if n7 >= VW.MIN_BARS and abs(hand - rv) > 1e-9 * abs(rv):
            bad.append(f"motion/{label}: window_bars()={n7} is not rolling_vwap's membership "
                       f"(by-hand VWAP {hand!r} vs {rv!r})")
        # MEASURING IS NOT WITHHOLDING. The floors are COUNTED against; they gate
        # nothing. So what rolling_vwap printed, what the registry holds and what
        # the logger counted are one number — on the thin frames above all, where
        # a logger that had quietly started withholding would be the only place
        # it showed (the verifier's mutant V5: bands gated, still counted).
        counted = sum(w["line_candidates"] + w["band_candidates"] for w in syn["vm"][label])
        if not (syn["printed"][label] == syn["reg_vwap"][label] == counted):
            bad.append(f"motion/{label}: WITHHOLDING — rolling_vwap printed {syn['printed'][label]} "
                       f"finite VWAP level(s), the registry holds {syn['reg_vwap'][label]}, the "
                       f"logger counted {counted}: measuring must gate nothing")
        if not syn["same_without"][label]:
            bad.append(f"motion/{label}: WITHHOLDING — the registry differs with and without "
                       f"the measuring side-channel")

    # ── (c) THE RUN ────────────────────────────────────────────────────────
    if doc.get("schema_version") != OD.CAL_SCHEMA_VERSION:
        bad.append(f"schema_version is {doc.get('schema_version')!r}, not {OD.CAL_SCHEMA_VERSION} "
                   f"— this is the hollow pre-OR-1 document")
    for k in C0_DOC_KEYS:
        if k not in doc:
            bad.append(f"roster-level '{k}' absent")
    by_sym = {a["symbol"]: a for a in view["assets"]}
    names = [n for n, _lo, _hi in BR.TARGET_BUCKETS] + [OD.BUCKET_NO_TARGET, OD.BUCKET_NO_CARD]
    basis = OD.REGISTER["TARGET_BUCKET_ATR"]["value"]
    if basis not in OD.ATR_BASES or set(OD.ATR_BASES) != {"lens", "daily"}:
        bad.append(f"ATR bases {OD.ATR_BASES} / headline basis {basis!r}: this fixture can "
                   f"re-derive 'lens' and 'daily' and nothing else — fail closed")
    blocks, lines = {}, []

    def _target(where: str, rec: dict, a: dict) -> None:
        # target bucket, re-derived on BOTH bases: 'lens' is the ATR the card prices
        # its toll in, 'daily' the a['atr_d'] the BRIEF-2 lane measured its edges in
        card = a["card"]
        for b_name, atr in (("lens", a["station"].atr), ("daily", a["atr_d"])):
            if not card:
                b_want, d_want = OD.BUCKET_NO_CARD, None
            else:
                d_want = (None if card.get("reward") is None
                          else round(float(card["reward"]) / float(atr), 6))
                b_want = (OD.BUCKET_NO_TARGET if d_want is None else
                          next((n for n, lo, hi in BR.TARGET_BUCKETS if lo <= abs(d_want) < hi), "FAR"))
            if rec["target_bucket_by_atr"].get(b_name) != b_want \
                    or rec["target_distance_atr"].get(b_name) != d_want:
                bad.append(f"{where}: target on the '{b_name}' basis logs "
                           f"{rec['target_bucket_by_atr'].get(b_name)} @ "
                           f"{rec['target_distance_atr'].get(b_name)}, re-derived from the card's "
                           f"reward over the {b_name} ATR: {b_want} @ {d_want}")

    for rec in doc.get("per_asset", []):
        sym, a = rec["asset"], by_sym[rec["asset"]]
        missing = [k for k in C0_ASSET_KEYS if k not in rec]
        if missing:
            bad.append(f"{sym}: family key(s) absent {missing}")
            continue
        wins = rec["maturity_windows"]
        if [w.get("window_d") for w in wins] != list(OD.REGISTER["VWAP_WINDOWS_D"]["value"]):
            bad.append(f"{sym}: maturity_windows {wins!r} do not cover the VWAP windows")
            continue
        # maturity: bars recounted by hand from a fresh frame, the verdicts from the
        # imported floors, the candidates from a registry rebuilt without the
        # side-channel — and only then the fraction, from those three
        fresh = _c0_fresh(sym)
        for w in wins:
            nb = fresh["bars"][w["window_d"]]
            if w.get("bars") != nb:
                bad.append(f"{sym}: the {w['window_d']}d window logs {w.get('bars')!r} bars, a "
                           f"by-hand recount of the 1h frame finds {nb}")
            if (w.get("line_ok"), w.get("band_ok")) != (nb >= VW.LINE_MIN_BARS, nb >= VW.BAND_MIN_BARS):
                bad.append(f"{sym}: the {w['window_d']}d verdict line_ok={w.get('line_ok')!r} "
                           f"band_ok={w.get('band_ok')!r} is not {nb} bars against the floors "
                           f"{VW.LINE_MIN_BARS}/{VW.BAND_MIN_BARS}")
        cand = rec["maturity_candidate_levels"]
        offered = sum(v["line_candidates"] + v["band_candidates"] for v in a["vwap_maturity"])
        if not (cand == offered == fresh["n_vwap"]) or a["n_levels"] != fresh["n_levels"]:
            bad.append(f"{sym}: {cand} VWAP candidates logged, {offered} counted in the view, "
                       f"{fresh['n_vwap']} vwap_rolling levels in a registry rebuilt without the "
                       f"side-channel ({fresh['n_levels']} levels there, {a['n_levels']} in the view)")
        held = sum((0 if fresh["bars"][w["window_d"]] >= VW.LINE_MIN_BARS else v["line_candidates"])
                   + (0 if fresh["bars"][w["window_d"]] >= VW.BAND_MIN_BARS else v["band_candidates"])
                   for w, v in zip(wins, a["vwap_maturity"]))
        n_vwap = sum(1 for c in a["clusters"] for m in c["members"]
                     if m["family"] == "vwap_rolling")
        if not cand or rec[C0_KEY] is None or rec[C0_KEY] != round(held / cand, 6) \
                or rec["maturity_withheld_levels"] != held:
            bad.append(f"{sym}: fraction {rec[C0_KEY]!r} is not {held}/{cand} re-derived "
                       f"from a by-hand recount of its bars")
        if cand < n_vwap:
            bad.append(f"{sym}: {cand} VWAP candidates logged but {n_vwap} sit in the clusters")
        # family-cap binding, re-counted from the view's own clusters
        tops = [max(pd.Series([m["family"] for m in c["members"]]).value_counts())
                for c in a["clusters"]]
        cap_want = {"clusters": len(tops), "at_cap": sum(t >= L.FAMILY_CAP for t in tops),
                    "over_cap": sum(t > L.FAMILY_CAP for t in tops)}
        if rec["family_cap_binding"] != cap_want:
            bad.append(f"{sym}: family_cap_binding {rec['family_cap_binding']} != {cap_want}")
        card, st = a["card"], a["station"]
        if card and abs(card["toll_price"] - card["toll_atr"] * st.atr) > 1e-12 * max(1.0, st.atr):
            bad.append(f"{sym}: the card no longer prices its toll in st.atr — the "
                       f"bucket's 'lens' ATR is not the card's ATR")
        _target(sym, rec, a)
        blocks[sym] = (tuple(w["bars"] for w in wins),
                       tuple(rec["family_cap_binding"][k] for k in C0_CAP_KEYS),
                       (rec["target_bucket"], rec["target_distance_atr"]["lens"]))
        wtxt = "/".join(str(w["window_d"]) + "d:" + str(w["bars"]) for w in wins)
        lines.append(f"{sym} {wtxt} frac {rec[C0_KEY]} "
                     f"cap {'/'.join(map(str, blocks[sym][1]))} "
                     f"{rec['target_bucket']}"
                     + (f"@{blocks[sym][2][1]}" if blocks[sym][2][1] is not None else "")
                     + (f" (daily {rec['target_distance_atr']['daily']})"
                        if rec["target_distance_atr"].get("daily") is not None else ""))
    if want[labels[0]] != 0.0 or not all(want[k] > 0 for k in labels[1:]):
        bad.append(f"the synthetic frames no longer straddle the floors: {want}")
    if len(blocks) != len(view["assets"]):
        bad.append(f"{len(blocks)} of {len(view['assets'])} asset(s) carry all three families")
    distinct = [len({b[i] for b in blocks.values()}) for i in range(3)]
    if blocks and max(distinct) < 2:
        bad.append("the measured block is CONSTANT across assets — bars, cap binding and "
                   "target distance all identical: that is a typed value, not a measurement")

    # ── THE ROSTER, in BOTH documents: every whole-roster record is a sum or a
    # count of the per-asset records and of nothing else. A typed roster dict over
    # honest per-asset rows is finding C-0 one level up, and on the real run a
    # typed 0.0 there is indistinguishable from the true one — hence the motion
    # document, where the roster fraction is 9 of 100 by construction.
    for tag, d in (("run", doc), ("motion", mot)):
        pa = d.get("per_asset", [])
        if any(k not in d for k in C0_ROSTER_KEYS) or any(k not in r for r in pa for k in C0_ASSET_KEYS):
            continue                                   # already reported absent above
        for r in pa:
            if r["target_bucket"] != r["target_bucket_by_atr"].get(basis):
                bad.append(f"{tag}/{r['asset']}: headline target_bucket {r['target_bucket']!r} is "
                           f"not the '{basis}' bucket {r['target_bucket_by_atr'].get(basis)!r} "
                           f"REGISTER['TARGET_BUCKET_ATR'] names")
        c = sum(r["maturity_candidate_levels"] for r in pa)
        h = sum(r["maturity_withheld_levels"] for r in pa)
        m_want = {"candidate_levels": c, "withheld_levels": h,
                  "withheld_fraction": (round(h / c, 6) if c else None)}
        if d["maturity_roster"] != m_want:
            bad.append(f"{tag}: maturity_roster {d['maturity_roster']} is not the per-asset "
                       f"sum {m_want}")
        cap_sum = {k: sum(r["family_cap_binding"][k] for r in pa) for k in C0_CAP_KEYS}
        if d["family_cap_binding"] != cap_sum:
            bad.append(f"{tag}: roster family_cap_binding {d['family_cap_binding']} is not the "
                       f"per-asset sum {cap_sum}")
        occ = {n: sum(1 for r in pa if r["target_bucket"] == n) for n in names}
        if d["target_bucket_occupancy"] != occ:
            bad.append(f"{tag}: target_bucket_occupancy does not count the per-asset buckets: "
                       f"{d['target_bucket_occupancy']} != {occ}")
        if sorted(d["target_bucket_occupancy_by_atr"]) != sorted(OD.ATR_BASES):
            bad.append(f"{tag}: target_bucket_occupancy_by_atr covers "
                       f"{sorted(d['target_bucket_occupancy_by_atr'])}, not {sorted(OD.ATR_BASES)}")
        for b_name in OD.ATR_BASES:
            occ_b = {n: sum(1 for r in pa if r["target_bucket_by_atr"].get(b_name) == n) for n in names}
            if d["target_bucket_occupancy_by_atr"].get(b_name) != occ_b:
                bad.append(f"{tag}: target_bucket_occupancy_by_atr['{b_name}'] does not count the "
                           f"per-asset buckets: {d['target_bucket_occupancy_by_atr'].get(b_name)} "
                           f"!= {occ_b}")
    # the thin frames withhold 4 and 5 levels by construction, so a roster fraction
    # of 0.0 (or None) on the motion document is a number that does not move
    mot_held = sum(round(want[k] * 5 * n_win) for k in labels)
    mot_roster = mot.get("maturity_roster", {})
    if "maturity_roster" in mot and (not mot_roster.get("withheld_fraction")
                                     or mot_roster.get("withheld_levels", 0) < mot_held):
        bad.append(f"motion: maturity_roster {mot_roster} — the thin frames withhold {mot_held} "
                   f"level(s) by construction; the ROSTER fraction does not move with the data")

    # THE OTHER TWO FAMILIES MOVE TOO — the planted cards and the built clusters of
    # the motion view, read back off disk against their construction
    mot_by = {r["asset"]: r for r in mot.get("per_asset", [])
              if all(k in r for k in C0_ASSET_KEYS)}
    mot_assets = {a["symbol"]: a for a in motion["assets"]}
    t_got, apart = [], 0
    for sym, what, b_name, n_want, d_want in t_plan:
        rec = mot_by.get(sym)
        if rec is None:
            continue                                   # hollow: reported above
        _target(f"motion/{sym}", rec, mot_assets[sym])
        if rec["target_bucket_by_atr"].get(b_name) != n_want \
                or rec["target_distance_atr"].get(b_name) != d_want:
            bad.append(f"motion/{sym}: planted {what} — it must read {n_want} @ {d_want} "
                       f"on the '{b_name}' basis, the record says "
                       f"{rec['target_bucket_by_atr'].get(b_name)} @ "
                       f"{rec['target_distance_atr'].get(b_name)}")
        apart += rec["target_bucket_by_atr"].get("lens") != rec["target_bucket_by_atr"].get("daily")
        t_got.append(f"{what} -> " + "/".join(
            str(rec["target_bucket_by_atr"].get(b)) for b in OD.ATR_BASES))
    if mot_by and not apart:
        bad.append("the planted cards no longer separate the two ATR bases — the headline "
                   "basis cannot be told from the other one")
    rec = mot_by.get(cap_carrier)
    if rec is not None and rec["family_cap_binding"] != built_want:
        bad.append(f"motion/{cap_carrier}: clusters built with {L.FAMILY_CAP - 1}/{L.FAMILY_CAP}/"
                   f"{L.FAMILY_CAP + 1} same-family members must read {built_want}, the record "
                   f"says {rec['family_cap_binding']}")
    if [c["member_count"] for c in built] != [L.FAMILY_CAP - 1, L.FAMILY_CAP, L.FAMILY_CAP + 1]:
        bad.append(f"the built clusters no longer straddle the cap: "
                   f"{[c['member_count'] for c in built]}")

    # the thresholds the three families are read against: imported, as logged
    th = doc.get("thresholds_in_force", {})
    th_want = {"vwap_windows_d": list(OD.REGISTER["VWAP_WINDOWS_D"]["value"]),
               "maturity_line_min": VW.LINE_MIN_BARS, "maturity_band_min": VW.BAND_MIN_BARS,
               "family_cap": L.FAMILY_CAP, "target_bucket_atr_basis": basis,
               "target_buckets_atr": {n: [lo, (None if hi == float("inf") else hi)]
                                      for n, lo, hi in BR.TARGET_BUCKETS}}
    th_bad = {k: th.get(k) for k, v in th_want.items() if th.get(k) != v}
    if th_bad and doc.get("schema_version") == OD.CAL_SCHEMA_VERSION:
        bad.append(f"thresholds_in_force {th_bad} are not the imported constants "
                   f"{ {k: th_want[k] for k in th_bad} }")
    unruled = not OD.REGISTER["TARGET_BUCKET_ATR"]["ruled"]
    if doc.get("schema_version") == OD.CAL_SCHEMA_VERSION \
            and ("TARGET_BUCKET_ATR" in doc.get("veto_rows_awaiting_ruling", [])) != unruled:
        bad.append(f"REGISTER['TARGET_BUCKET_ATR'] is {'UNRULED' if unruled else 'ruled'} but "
                   f"veto_rows_awaiting_ruling says otherwise")
    return bad, {"doc": doc, "mot": mot, "syn": syn, "got": got, "labels": labels,
                 "blocks": blocks, "lines": lines, "distinct": distinct, "view": view,
                 "mot_held": mot_held, "basis": basis, "t_got": t_got, "apart": apart,
                 "built_want": built_want, "cap_got": (rec or {}).get("family_cap_binding")}


def _c0_measured(src: str | None = None, doctor=None, gate: bool = False) -> tuple[bool, str]:
    VW = OD.VW
    bad, x = _c0_judge(src=src, doctor=doctor, gate=gate)
    if bad:
        return False, "; ".join(bad[:6]) + (f" (+{len(bad) - 6} more)" if len(bad) > 6 else "")
    doc, mot, syn, got, labels = x["doc"], x["mot"], x["syn"], x["got"], x["labels"]
    blocks, distinct, view = x["blocks"], x["distinct"], x["view"]
    fracs = sorted({doc_r[C0_KEY] for doc_r in doc["per_asset"]})
    return True, (
        f"(a) no constant is assigned to '{C0_KEY}', to any key ending 'withheld_fraction' or "
        f"to any other of the {len(C0_NO_LITERAL)} C-0 record keys, every one of them is seen "
        f"being written, VW.maturity() is called, FAMILY_CAP and "
        f"TARGET_BUCKETS are imported never copied (brief_render closure drags none of "
        f"{list(C0_NO_ESTATE)}); (b) the number MOVES through level_registry -> "
        f"write_calibration -> disk: 7d window of "
        + ", ".join(f"{syn['kept7'][k]} bars -> {got[k]}" for k in labels)
        + f" (20 bars withholds the 4 bands of 10 levels, 12 bars the line as well), the "
        f"ROSTER fraction of that document moves with it "
        f"({mot['maturity_roster']['withheld_levels']}/{mot['maturity_roster']['candidate_levels']}"
        f" = {mot['maturity_roster']['withheld_fraction']}; the real run reads "
        f"{doc['maturity_roster']['withheld_fraction']}), window_bars() reproduces "
        f"rolling_vwap's own membership by hand on all three, and measuring WITHHOLDS NOTHING: "
        f"the registry holds exactly the "
        + "/".join(str(syn["reg_vwap"][k]) for k in labels)
        + f" finite VWAP levels rolling_vwap printed, identical with and without the "
        f"side-channel. The other two families move too, BY CONSTRUCTION: planted cards read "
        f"(" + "/".join(OD.ATR_BASES) + " bucket) " + ", ".join(x["t_got"]) + f" — the two ATR bases separate on "
        f"{x['apart']} of them; clusters built with cap-1/cap/cap+1 same-family members read "
        f"{x['cap_got']}; (c) real build_view, {len(blocks)}/{len(view['assets'])} assets carry "
        f"all three families. Tied to an independent source, per asset: window bars (by-hand "
        f"recount of a freshly loaded 1h frame) and their line/band verdicts (imported "
        f"floors), candidate levels (the vwap_rolling levels of a registry rebuilt WITHOUT "
        f"the side-channel), withheld levels and fraction (from those), cap binding "
        f"(recounted from the view's clusters), target distance and bucket on BOTH ATR bases "
        f"(card reward over st.atr = the card's toll ATR, and over atr_d), headline bucket == "
        f"the '{x['basis']}' basis the [VETO] row names. Whole roster, in BOTH documents: "
        f"maturity_roster, family_cap_binding (all 3 keys), target_bucket_occupancy and "
        f"_by_atr equal the per-asset sums/counts; thresholds_in_force equal the imported "
        f"constants. TAKEN AS GIVEN, not re-derived here: the card's reward, st.atr, atr_d and "
        f"the view's clusters — the Oracle's view, which STEP B did not change. Distinct values "
        f"across assets — window "
        f"bars {distinct[0]}, cap binding {distinct[1]}, target {distinct[2]} — so the block "
        f"is measured, not typed. HONEST CAVEAT: the maturity fraction is {fracs} on this "
        f"roster — a TRUE measured zero, the windows hold far more than the "
        f"{VW.LINE_MIN_BARS}/{VW.BAND_MIN_BARS} floors; the difference across assets comes "
        f"from the other two families. Roster: maturity {doc['maturity_roster']}, cap "
        f"{doc['family_cap_binding']}, buckets {doc['target_bucket_occupancy']}. Per asset: "
        + " | ".join(x["lines"]))


def f_br_13() -> None:
    src = (ROOT / "scripts" / "oracle_daily.py").read_text()
    planted, n = re.subn(rf'(?m)^(\s*"{C0_KEY}":[ \t]*)[^\n]+$', r"\g<1>0.0,", src)
    planted_r, n_r = re.subn(r'("withheld_fraction":[ \t]*)\([^\n]*\)\}', r"\g<1>0.0}", src)

    # (name, the finding it MUST produce, how it is planted). Judged one at a time:
    # a red plant must not be able to carry a green one through, and a plant that
    # is red for some OTHER reason has not shown its own guard working.
    plants = (
        (f"SOURCE PLANT (literal 0.0 replanted on {n} line(s))",
         f"'{C0_KEY}' is assigned the typed constant", dict(src=planted) if n else None),
        (f"SOURCE PLANT, ROSTER (literal 0.0 on {n_r} `withheld_fraction` line(s))",
         "'withheld_fraction' is assigned the typed constant", dict(src=planted_r) if n_r else None),
        ("DOCUMENT PLANT (the hollow pre-OR-1 shape)",
         "hollow pre-OR-1 document", dict(doctor=_c0_hollow)),
        ("DOCUMENT PLANT V1 (headline target_bucket typed 'NEAR')",
         "headline target_bucket", dict(doctor=_c0_doc_headline)),
        ("DOCUMENT PLANT V2 (roster occupancy typed, all NONE)",
         "target_bucket_occupancy does not count", dict(doctor=_c0_doc_occupancy)),
        ("DOCUMENT PLANT V3 ('daily' basis silently in the lens ATR)",
         "on the 'daily' basis", dict(doctor=_c0_doc_daily_in_lens)),
        ("DOCUMENT PLANT V4 (roster withheld_fraction typed 0.0)",
         "maturity_roster", dict(doctor=_c0_doc_roster_fraction)),
        ("DOCUMENT PLANT V6 (roster at_cap/over_cap typed 0)",
         "roster family_cap_binding", dict(doctor=_c0_doc_roster_cap)),
        ("DOCUMENT PLANT (a window bar count nobody counted, +1)",
         "by-hand recount", dict(doctor=_c0_doc_bars)),
        ("DOCUMENT PLANT ('NEAR' typed for every card — true of the real run, so only "
         "the planted cards can object)",
         "— it must read", dict(doctor=_c0_doc_all_near)),
        ("DOCUMENT PLANT (`>` typed as `>=`: over_cap := at_cap, roster re-summed to match)",
         "same-family members must read", dict(doctor=_c0_doc_over_is_at)),
        ("REGISTRY PLANT V5 (immature 7d bands withheld from the registry, still counted)",
         "WITHHOLDING", dict(gate=True)),
    )

    def _break() -> tuple[bool, str]:
        green, out = False, []
        for name, must, kw in plants:
            if kw is None:
                green = True
                out.append(f"{name} -> GREEN: the plant found no line to replace")
                continue
            bad, _x = _c0_judge(**kw)
            hits = [b for b in bad if must in b]
            if hits:
                rest = [b for b in bad if must not in b]
                out.append(f"{name} -> RED: {hits[0]}"
                           + (f" (+{len(hits) - 1} more of its kind)" if len(hits) > 1 else "")
                           + (f" [and {len(rest)} other finding(s), first: {rest[0]}]" if rest else ""))
            else:
                green = True
                out.append(f"{name} -> " + ("GREEN" if not bad else
                           f"RED FOR THE WRONG REASON (no finding says {must!r}; first: {bad[0]})"))
        return green, " ‖ ".join(out)

    prove("F-BR-13", "C-0 — the D-7 logger MEASURES maturity, family-cap binding and "
                     "target buckets; a typed 0.0 must never pass for a measurement",
          _break, lambda: _c0_measured())


# ═════════ F-BR-14 · THE RANGE LAYER RENDERS, NEVER RULES (OR-1 STEP D, 2026-09-21)
#
# WHAT THIS GUARDS. OR-1 §2, from the operator's ratification line: "no gate, filter,
# or sizing reads a range or a mover." STEP D put a RangeFinder macro range on every
# roster symbol: a RANGE cell on the Board, the TIDE TABLES, the EDGE WATCH list and
# eight tape columns — which, since AMENDMENT A-OR1-1 (operator, 2026-09-22), live on a
# SIBLING tape (clause v: "Range records go to a sibling tape,
# research_outputs/oracle/tape_ranges/; the TC4 event tape's schema is untouched
# (A-BR2-1b doctrine)"), computed by a machine that lives at scripts/rangefinder_core.py
# (clause iv: "engine/ is outside this lane's write authority (BR-1 §2 clause 3);
# promotion into engine/ is APOLLO's call"). A range is the most tempting number on
# the page to act on ("it is 0.4 ATR from the top, so damp the heat"), and the day one
# line does that, a display organ calibrated on ONE symbol (BTC; KEY-A on 1D, KEY-C on
# 4h) is steering posture words on eighteen. The contract's words for this fixture:
# "posture_engine.py byte-unchanged (sha printed); the range object appears only in
# render + tape, never in any gate path (component-wise import scan); planted gate
# read ⇒ red."
#
# FOUR LEGS, because each one alone has a hole the next one covers:
#   (a) THE SHA      scripts/posture_engine.py is byte-for-byte the file pinned below.
#                    Every station word on the page comes from it; STEP D had no
#                    business in it and this proves it had none. A later RATIFIED
#                    edit to posture_engine.py re-pins the constant in the same commit
#                    (the F-TU-1 idiom): the red is the point, not an accident.
#   (b) THE IMPORTS  in clean subprocesses, the closure of every decision module holds
#                    no module with the component `rangefinder` or `rangefinder_core`
#                    (nor `oracle_daily`: a gate that imported the Oracle could read a
#                    view), and the Oracle's range machine's own closure
#                    (ORACLE_RANGE_MODULE) holds no trading / journal / outcome-package
#                    component. Component-wise, the F-BR-3 repair: `engine.rangefinder`
#                    cannot hide behind a top-level-only test. TEXT SCANS cover what no
#                    closure can: a LAZY import runs only when its function does, and
#                    another lane's live rule modules are read here, never executed.
#                    THEIR SCAN SET IS THE REAL ONE (round-1 review, 2026-09-22): every
#                    engine module but the machines, posture_engine.py and every
#                    tierc*_rules.py, PLUS every repo-local file oracle_daily or a
#                    decision module actually LOADS — analytics/*, brief_render,
#                    census2b_program, census_build: the levels, clusters, heat and lines
#                    in the sand are computed there, and none of them was scanned. AND
#                    EVERY REPO MODULE THOSE FILES NAME IN AN IMPORT STATEMENT, AT ANY
#                    DEPTH, FOLLOWED STATICALLY (round-2 review): a new module imported
#                    only inside a function is in no closure, and a shim re-exporting the
#                    machine there was in no scan. Two scans over that set. The import
#                    LINE (RANGE_IMPORT_LINE, which also matches a wrapper re-exporting
#                    the machine: `rangefinder_twin`, `rangefinder_census`). And the same
#                    files parsed as CODE: an import statement at ANY depth —
#                    parenthesised, backslash-continued, relative — whose dotted
#                    components meet RANGE_BANNED_IN_DECISION or carry `rangefinder`, or
#                    that loads a repo module in the REVERSE IMPORT INDEX (every module
#                    under scripts/, analytics/, engine/ that imports a machine, a wrapper
#                    or oracle_daily, at any depth, transitively: oracle_fixtures,
#                    oracle_topup, tierc10_* ... — a re-exporter IS the machine); an
#                    import of the dynamic-import machinery (importlib, pkgutil, runpy,
#                    builtins, inspect, gc ...) or any `from sys import`; any of
#                    RANGE_DECISION_DYNAMIC (importlib, __import__, globals, vars, eval,
#                    exec, getattr, locals, compile, __builtins__ ...); any
#                    RANGE_DECISION_ATTRS (`.modules`, `.__dict__`, `.f_globals`,
#                    `._getframe` ...); an attribute carrying `rangefinder` or named
#                    `RNG`; any string naming `rangefinder` or `oracle_daily`, or equal to
#                    'RNG'. The dynamic uses on that side today — census2b_program's own
#                    F-B5c loading census-2A by path, tierc5_rules' Card.diff_from_v5
#                    reading its own fields — are NAMED in RANGE_DECISION_DYNAMIC_OK, not
#                    waved through.
#   (c) THE AST      oracle_daily.py, scanned as CODE: every mention of the asset-dict
#                    key 'range', of the snapshot's own key names, of the `RNG` alias
#                    and of the layer's five functions must sit inside an ALLOW-LIST of
#                    function names. build_view is on it for exactly ONE statement, of
#                    exactly one shape. By VALUE, not by spelling: `k = "range"; a[k]`
#                    is caught, and so is a gate that calls range_watch(). Fails
#                    CLOSED: if the key it hunts is no longer read by write_range_tape
#                    (the sibling tape) or by a render function, the scan is hunting a
#                    stale name and says so. THE MACHINE BY NO OTHER ROUTE (round-1
#                    review): `RNG` is bound once, by the one sanctioned import, and
#                    nothing in the file can reach a module without an import statement
#                    naming it — no RANGE_DYNAMIC_NAMES (__import__, importlib, globals,
#                    vars, locals, eval, exec, getattr, setattr, hasattr, gc, inspect …;
#                    none is used today), no import of the dynamic-import machinery, no
#                    `from sys import`, no RANGE_DYNAMIC_ATTRS (`.modules`, `.__dict__`,
#                    `._getframe`, `.f_globals`, `.get_objects`, `.__file__` …), no import
#                    of oracle_daily itself or of the NAME RNG, no `<module>.RNG`, no
#                    import of a module in the REVERSE IMPORT INDEX (see (b)) but the
#                    one sanctioned binding and RANGE_OD_IMPORT_OK, and no string naming
#                    `rangefinder` or equal to 'RNG' outside REGISTER's sources. THE
#                    MACHINE'S API, NOT ITS SPELLINGS (round-2 review): `RNG` itself,
#                    and every name the two machines define (derived from their source:
#                    run_v2, tape_from_klines, snapshot, PINS_V2, V2_WINDOW_BARS, _span,
#                    Range …) as an attribute or a string, appear ONLY in range_layer()
#                    and REGISTER's RNG.V2_WINDOW_BARS — whatever route found the module,
#                    a gate still calls it by those names. The other readers may read the
#                    view's 'range' key; they may not run the machine. NO STASH: no
#                    function in the file stores into module-level state — a `global`,
#                    a store into or a mutating call on a module-level name, or on a
#                    LOCAL bound to one (`_q = REGISTER[k]; _q["value"] = v`, round 2)
#                    — so an allow-listed reader cannot leave a range where a gate will
#                    find it.
#   (d) THE RUN      what no static scan can promise (`for v in a.values()` names
#                    nothing). oracle_daily.run() ITSELF — the production function, not
#                    a copy of its order (round-1 review: a gate planted in run(),
#                    between the tapes and the D-7 record, moved the FILED heat on 2 of
#                    18 symbols while this leg, which re-implemented run()'s order,
#                    never ran it) — runs three times over the live roster: stubbed
#                    EMPTY, stubbed HOT (every symbol pinned ON a macro boundary with a
#                    breach pending: the input a gate would react to hardest), and REAL,
#                    LAST. EACH RUN IN A FRESH MODULE built from source, so nothing one
#                    run leaves in the module reaches the next (the review's plant
#                    filled a memo in range_layer during REAL and the stubbed runs,
#                    sharing the module, read it back: the three agreed and the leg
#                    printed green while heat moved); REAL last, so that nothing REAL
#                    leaves in a SHARED module is there for the stubbed runs either.
#                    Every directory run() writes (RANGE_RUN_DIRS) is a throwaway one,
#                    the canon is written into it, the roots it READS from (RANGE_RUN_READS:
#                    the grid parquet, the movers directory) are COPIED into the same
#                    throwaway tree and pointed at there (round-2 review: GRID_PARQUET
#                    still resolved into the live repo, and a sibling path cut out of
#                    its string read the live directory in all three runs), and the
#                    module's clock is frozen for all three runs. EACH RUN'S SIBLING
#                    DIRECTORY IS SEEDED DIFFERENTLY
#                    — REAL nothing, EMPTY an all-None day, HOT a day with every symbol
#                    ON a boundary, breach pending — so a gate that reads the sibling
#                    tape off disk, by any spelling that derives from the lane's paths,
#                    reads a different thing in each run and moves. Sort order, heat,
#                    station, card, lines, clusters, fired events, R1, the WHOLE D-7
#                    document and the WHOLE D-4 tape (its 24 columns) must come out
#                    identical; the sibling tape's range columns must NOT, or the stub
#                    never reached build_view and the comparison is empty; the sibling
#                    tape's parquet SCHEMA must be the same in all three (the all-None
#                    day is the EMPTY run). THE PAGE IS COMPARED TOO, because leg (c)
#                    lets render_html read a range and a reader can misbehave (a Board
#                    re-sorted by distance inside the render moves no field of the
#                    view): every rendered section but the Tide Tables, the Board with
#                    its RANGE cells cut out, identical across the three runs. AND THE
#                    VIEW IS PROVED UNMUTATED ACROSS EVERY ALLOW-LISTED READER run()
#                    HANDS IT TO (RANGE_VIEW_READERS), repr before vs repr after: an
#                    in-place re-order — `view["assets"].sort(...)` for `sorted(...)`,
#                    one keystroke — is identical in all three runs, and run() writes
#                    both tapes and the D-7 record AFTER the render, so it would land
#                    there unseen. AND EACH RUN IS WATCHED (round-2 review), because the
#                    stubs replace `range_layer` only and a gate that ran the machine
#                    by another route, or read the sibling tape by a path no name
#                    reaches, did the same thing in all three runs and cancelled out
#                    (the review's OD-A moved heat on 2 of 18 symbols, OD-G flipped the
#                    filed D-7 target-bucket basis, both with every leg green). THE
#                    MACHINE TRIPWIRE (sys.monitoring): every entry into a frame of
#                    either machine file, from outside the machine, must come from the
#                    run's own range_layer() in REAL, and there must be NONE in EMPTY
#                    and HOT, where range_layer is stubbed — whatever route found the
#                    module (sys.modules, a frame, gc, a re-exporter, a decision module
#                    reading its caller's globals). THE READ TRIPWIRE: pandas' and
#                    pyarrow's parquet readers wrapped, and an audit hook on open /
#                    os.listdir / os.scandir / glob.glob / shutil.copyfile: red on any
#                    path under the LIVE sibling directory, any listing of the run's own
#                    sibling directory, and any read of an oracle_tape_ranges_* file
#                    but write_range_tape()'s read-back of the file it just wrote. The
#                    path is judged where the read happens, so its spelling, and the
#                    side it is spelt on, are irrelevant. A trip is a finding on its
#                    own; each tripwire must also see its own proof of life in REAL
#                    (range_layer's entries; the writer's read-back), or it is unarmed.
#                    RESIDUAL, DISCLOSED: a gate that executes only OUTSIDE run() (none
#                    of the three runs reaches it) is (c)'s and (h)'s alone. A read the
#                    two tripwires cannot see — native IO by a route that is neither a
#                    wrapped reader nor an audited call (pyarrow.fs, a memory map, a
#                    reader imported by name before the wrap), or a probe of a LIVE
#                    sibling directory that does not exist yet (pathlib's glob tests
#                    is_dir() first and lists nothing) — is (c)'s and (h)'s static
#                    fences again, and a probe of an absent directory reads nothing. A
#                    SHARED module's state changed through a function PARAMETER
#                    (`helper(PE.REGISTER)` storing into its argument) escapes (c)'s
#                    stash rule; REAL-last defeats it inside this leg, not a value an
#                    EARLIER fixture of this process left there. Stubbing at the machine
#                    boundary stays follow-up work (it would mean fabricating a v2
#                    payload snapshot() accepts and patching the shared machine module
#                    for the process); the machine tripwire watches that boundary
#                    instead.
# FOUR MORE LEGS, A-OR1-1's (2026-09-22), each with its own plant in the BREAK list:
#   (e) THE MACHINE  oracle_daily's import closure, in a clean subprocess, CONTAINS
#                    ORACLE_RANGE_MODULE (rangefinder_core) and does NOT contain
#                    RANGE_MACHINE (engine.rangefinder, TIER-C10's machine of record,
#                    byte-frozen under engine/); and of every repo-local module in that
#                    closure, oracle_daily is the ONLY one whose code imports
#                    rangefinder_core. Plant: a COPY of oracle_daily.py with `from
#                    engine import rangefinder as RNG` re-added.
#   (f) THE D-4 TAPE TC4's event tape: oracle_daily.TAPE_COLS, the edition's D-4 tape
#                    and the D-4 tape leg (d) writes are each EXACTLY the pre-OR-1 24
#                    names in the pre-OR-1 order (PRE_OR1_TAPE_COLS, typed here from
#                    `git show ee93644^:scripts/oracle_daily.py`, a second object).
#                    Plant: a range column appended to oracle_daily.TAPE_COLS as a frame
#                    — WITH A CONTROL: the unplanted frame must be green first (planted
#                    on the 2026-09-21 artifact's 32-column frame, the plant was red
#                    before anything was planted).
#   (g) THE SIBLING  the sibling tape carries the D-4 row keys and the eight range
#                    fields, each at its PINNED parquet type (RANGE_SIBLING_TYPES,
#                    typed here: five double, three string, never null), and exactly
#                    one row per roster symbol — on the edition's sibling tape, on the
#                    one leg (d) writes, and on an all-EMPTY day written through the
#                    real writer. Plants: a field dropped; the string pin removed.
#   (h) THE SIBLING WALL no gate reads the sibling tape. The decision-side sources of
#                    leg (b)'s scan set never spell its directory, its constant, its
#                    column list, its writer or `research_outputs/oracle` (case-blind,
#                    comments included — fail closed). Inside oracle_daily.py those
#                    names appear only in their own definitions and write_range_tape();
#                    run() may CALL the writer, once, and hand what it returns to log()
#                    and to its return dict, and nothing else — and `log` must BE the
#                    parameter: rebound in run() (a Store, a nested def, a lambda
#                    parameter, global/nonlocal), the sanctioned log(f'{rtape_p} ...')
#                    hands the sibling path to a gate (round 2). And the lane's PATHS are
#                    fenced the same way, so that a spelling cannot walk around the
#                    names: ROOT, __file__ and each lane directory are named only by the
#                    functions RANGE_LANE_PATHS lists for it, and even there only
#                    JOINED (`/`), tested, created, globbed or handed to a reader —
#                    never converted (str(), .replace, .as_posix, os.fspath, an
#                    f-string outside a raise), which is a path cut into any other
#                    (round 2: `str(GRID_PARQUET).replace(...)`); no code walks a path
#                    (RANGE_PATH_WALKS: .parent, .parents, .cwd …) outside ROOT's own
#                    definition, only RANGE_DISK_READERS touch the disk, no reader is
#                    imported by name, and 'research_outputs' is spelt only in the lane's
#                    path definitions and REGISTER's sources — `TAPE_DIR.parent / ('tape'
#                    + '_ranges')` names no sibling token and is red. What no text can
#                    fence — a decision module's own path, spelt in fragments, on the
#                    decision side, where `__file__` and 'research_outputs' are
#                    everyday words — is leg (d)'s READ TRIPWIRE. Plants: a read of the
#                    directory appended to a decision module's TEXT; TAPE_RANGES_DIR
#                    read in trap_card() and in run(); the written sibling tape read
#                    back in run(); two paths derived from TAPE_DIR in trap_card(); the
#                    grid path cut into the sibling's in grid_toll(); `log` rebound.
# and three small pins that belong to the same wall: the sibling tape's names clear the
# banned-token matcher the wrapper's self-check runs ("edge" is banned); no D-7 key
# carries the token `range`; and range_layer() CONTAINS a fault (a display organ may
# not take the Board down) and REFUSES a frame that is not on REGISTER['RANGE_LENS'].
#
# WHAT IT DOES NOT PROVE. That the ranges are TRUE — that this box is where the market
# actually turned. The RF suites prove the MACHINE's event log on a frozen BTC tape;
# F-RF-1d calls snapshot() only to prove the two copies of the machine agree, and
# neither asserts that a printed value is right. Before the value legs below were
# written (review repair,
# 2026-09-21) nothing in the repo asserted a single PRINTED range value on any symbol,
# and a snapshot() that returned the box upside down with every distance 10x too large
# passed this whole suite 16/16 green. What is proved here is SELF-CONSISTENCY — the
# box, the position, the distance and the side agree with each other and with the
# snapshot's own close and atr — plus the sibling tape recording those same numbers
# field for field, and range_watch's membership at the limit. (That the Oracle's copy
# of the machine prints the SAME boxes as engine/rangefinder.py is F-RF-1d's claim,
# snapshot parity, beside F-RF-1c's event logs and F-RF-1e's source equivalence —
# scripts/rangefinder_core_fixtures.py, not this fixture.) A wrong atr or a wrong
# close is still invisible; pinning one symbol on a frozen tape slice with ATR
# recomputed independently is the follow-up. That a human will not act on the number
# (nothing can). That code OUTSIDE oracle_daily.py and the modules in (b) never reads a
# tape column: the tape is a recording, and what a later study does with it is that
# study's registration under G-7. And not DELIBERATE OBFUSCATION: the recovery's third
# adversarial round (2026-09-22) still reached a gate with every leg green by routes no
# static scan and no three-run behaviour leg can close — a private copy of the machine
# compiled from its own source under another filename, a range read by value
# (`a.values()`, `a['ran' + 'ge']`) whose effect the three runs do not trigger, the
# sibling tape read through pyarrow.fs / a memory map of a path spelt in fragments, and
# the machine reached through builtins by attribute, sys.meta_path or exec of its
# source. These are DISCLOSED RESIDUALS, not fixed: the wall is a guard against honest
# and plain routes, and a diff that spells any of them is a review finding on sight.
#
# LIKE F-BR-16, IT AUDITS THE NEWEST ARTIFACT SET TOO: the edition under test must
# carry the Tide Tables, EDGE WATCH, both [VETO] rows in its appendix, a D-4 tape of
# exactly the pre-OR-1 24 columns and a sibling tape carrying the eight range fields.
# Run bare against an edition printed before A-OR1-1 (the 2026-09-21 set: 32 columns on
# its D-4 tape and no sibling) it is RED on exactly those, on purpose, until an edition
# is printed by this code. The sandbox suite prints one first.
#
# BREAK LEG: one plant per guard, judged ONE AT A TIME (the F-BR-13 idiom): each
# must go red on its own and for its own reason, named beside it. A plant whose judge
# RAISES is void, not red: it proved nothing.

POSTURE_ENGINE_SHA256 = "1e3b3ba28e251d1fa3ef6ab8add5f1841164312e061e94686f7e3e8c8fc666b4"

# The contract's six, plus engine.htf (it feeds the signal layer; engine/rangefinder.py's
# own docstring names it a stranger).
RANGE_DECISION_MODULES = ("posture_engine", "tierc2_rules", "tierc3_rules",
                          "engine.signals", "engine.trading", "engine.replay", "engine.htf")
# TWO MACHINES, TWO NAMES (A-OR1-1 iv, operator 2026-09-22).
# RANGE_MACHINE names engine/rangefinder.py, the copy OR-1 STEP D1 created under engine/.
# It is NOT the Oracle's machine any more, and it stays byte-frozen where it is because
# TIER-C10 made it ITS machine of record (F-C10-RESUME-6). ITS VALUE DOES NOT MOVE:
# TIER-C10 reads this constant — and RANGE_DECISION_MODULES, RANGE_BANNED_IN_DECISION,
# RANGE_BANNED_IN_MACHINE and RANGE_IMPORT_LINE — as TEXT, by AST, out of this file
# (scripts/tierc10_rf_fixtures.py, _br14_constants: top-level plain `NAME = ...`
# assignments, literal-evaluated or a call whose first argument is one string literal),
# and asserts its own fixture imports the module it names. So all five stay plain
# assignments of that shape, RANGE_MACHINE stays "engine.rangefinder", and the two
# banned tuples may only GROW. Here it is the module oracle_daily must NOT reach (leg e).
RANGE_MACHINE = "engine.rangefinder"
# THE MACHINE THE ORACLE RUNS: scripts/rangefinder_core.py (A-OR1-1 iv), a copy of the
# engine file held to it by F-RF-1c/d/e (scripts/rangefinder_core_fixtures.py: the event
# logs, snapshot parity, source equivalence). Every leg
# below that means "the Oracle's machine" reads THIS name: the closure legs (b) and (e),
# the source planted in the machine-closure plant, the AST fence's one sanctioned
# binding, the bypass fences, and the text scan's exclusion.
ORACLE_RANGE_MODULE = "rangefinder_core"
# "rangefinder_core" is its own dotted component: the component-wise match on
# "rangefinder" does not see it, so it is named. Nothing the seven decision closures
# reach carries it (measured 2026-09-22).
RANGE_BANNED_IN_DECISION = ("rangefinder", "oracle_daily", "rangefinder_core")
RANGE_BANNED_IN_MACHINE = ("trading", "journal", "analytics", "signals", "replay",
                           "forward_log", "positions")
# Read as TEXT only, never imported: every engine module but the machine itself, the
# posture engine, and every tierc*_rules module (tierc6 is another lane's live work).
# ANY module whose name STARTS with the machine's, not just the machine: `\b` stops
# at the '_' of `rangefinder_twin`, so the bare boundary missed the display twin
# (scripts/rangefinder_twin.py re-exports run_v2/PINS_V2 verbatim) and
# analytics/rangefinder_census.py. Reading a range off a wrapper is the same harm.
# These 14 of the 21 files have NO closure leg behind them — engine/__init__, cells,
# config, data, indicators, journal, s1, s2, shadows, version and tierc4/5/6/7_rules —
# so the import LINE here and leg (b)'s AST scan (_range_decision_ast, over the same
# files and the ones the closures and the static import walk add) are their guards,
# not this line alone. The constant stays a plain assignment: TIER-C10 reads it as
# TEXT (scripts/tierc10_rf_fixtures.py, _br14_constants). Verified a no-op on the tree
# of 2026-09-21:
# 0 hits across all 21 files; the break leg's `from engine.rangefinder import run_v2`
# still matches, and a commented-out import still does not (the `[^\n#]*` guard).
RANGE_IMPORT_LINE = re.compile(r"(?m)^[ \t]*(?:from|import)[ \t]+[^\n#]*\brangefinder\w*\b")

RANGE_KEY = "range"
RANGE_ALIAS = "RNG"
RANGE_PRODUCER = "range_layer"
RANGE_HELPERS = ("range_layer", "range_empty", "range_cell", "range_watch", "tide_tables")
# THE ALLOW-LIST. The layer's own five functions, the page, the SIBLING tape. Nothing
# else — and not write_tape any more: since A-OR1-1 the D-4 tape reads no range. What
# they may do is READ THE VIEW'S 'range' KEY. Running the machine is range_layer()'s
# alone (round-2 review, 2026-09-22: render_html ran RNG itself and flipped the filed
# D-7 target-bucket basis with every leg green) — see _range_api.
RANGE_READERS = (*RANGE_HELPERS, "render_html", "write_range_tape")
RANGE_WRITER = "build_view"                     # one statement, one shape
# named by the OR-1 STEP D build order: each must EXIST and hold zero mentions
RANGE_NAMED_GATES = ("level_registry", "trap_card", "net_rr", "fired_events",
                     "r1_block", "write_calibration")
# snapshot keys no other code in the file has a reason to spell. Checked against the
# live snapshot, so a rename over there cannot quietly blind the scan over here.
RANGE_ONLY_KEYS = ("has_range", "pos_pct", "dist_atr", "nearest_side",
                   "n_pending_open", "n_potential", "last_event", "status_line")
RANGE_REGISTER_IMPORTS = ("V2_WINDOW_BARS",)    # the one thing REGISTER may read off RNG
RANGE_GATE_TEXT = ('if assets[-1]["range"]["dist_atr"] is not None and '
                   'assets[-1]["range"]["dist_atr"] < 0.5: assets[-1]["heat"] *= 2')
RANGE_MUTANT_ROSTER = 3          # the behavioural BREAK runs on the first 3 roster rows

# ── A-OR1-1 v: THE TWO TAPES ──────────────────────────────────────────────────────
# (f) the D-4 tape's schema of record, TYPED HERE from `git show ee93644^:scripts/
# oracle_daily.py` (the last tree before OR-1 STEP D2 appended eight range columns) and
# checked against research_outputs/oracle/tape/oracle_tape_2026-09-20.parquet's names on
# 2026-09-22. A second object: oracle_daily.TAPE_COLS is judged against it, never the
# other way round.
PRE_OR1_TAPE_COLS = ("as_of_ms", "as_of_iso", "asset", "lens", "station", "tide",
                     "tide_flip_ms", "direction", "arm_ms", "age_bars", "disp_atr",
                     "d_ok", "trigger_ms", "trigger_on_arming_bar", "closed_by",
                     "close_px", "atr_lens", "atr_daily", "n_levels", "n_clusters",
                     "nearest_cluster_atr", "nearest_cluster_score", "heat",
                     "payload_sha")
# (g) the sibling tape, column -> the parquet type it must land as, TYPED HERE. The row
# keys are the D-4 tape's; the eight fields are pinned by oracle_daily's
# RANGE_TAPE_FLOATS / RANGE_TAPE_STRINGS so that an all-None day cannot land a `null`
# column (the 2026-09-21 review's hazard: a multi-day read then raises before it
# returns a row). pandas' nullable string may land as `string` or `large_string`
# depending on the pyarrow build; both are one type here, `null` never is.
RANGE_SIBLING_TYPES = {
    "as_of_ms": "int64", "as_of_iso": "string", "asset": "string", "lens": "string",
    "range_state": "string", "range_top": "double", "range_bottom": "double",
    "range_pos_pct": "double", "range_dist_atr": "double",
    "range_pending_side": "string", "range_last_event": "string",
    "range_last_event_age_bars": "double",
}
# (h) what a gate reading the sibling tape would have to spell: the directory (any case,
# so TAPE_RANGES_DIR and oracle_tape_ranges_<date> too), the column list, the writer.
RANGE_SIBLING_TOKENS = ("tape_ranges", "RANGE_TAPE_COLS", "write_range_tape")
RANGE_SIBLING_TOKEN_RX = re.compile("|".join(re.escape(t) for t in RANGE_SIBLING_TOKENS),
                                    re.IGNORECASE)
# On the DECISION side the lane's own directory is one more thing a gate would have to
# spell: `research_outputs/oracle` (0 hits in the scan set, comments included, measured
# 2026-09-22). Not added to the tokens above: oracle_daily's REGISTER source for the
# ROSTER cites research_outputs/oracle/roster_probe_<date>.json, and that is prose.
RANGE_SIBLING_DECISION_RX = re.compile(
    "|".join(re.escape(t) for t in (*RANGE_SIBLING_TOKENS, "research_outputs/oracle")),
    re.IGNORECASE)
RANGE_SIBLING_WRITER = "write_range_tape"
# run() CALLS the writer, once, and may hand the three names it binds from it to log()
# (as an f-string field or a bare argument) and to its return dict (as a bare value,
# under keys that may spell the tape: the callers read res['tape_ranges']). Nothing
# else of the sibling's in run() — round-1 review: run() was exempt from leg (h)
# wholesale, and a gate there that read the sibling tape back moved the filed heat.
RANGE_SIBLING_CALLER = "run"
RANGE_SIBLING_LOG = "log"
RANGE_SIBLING_DEFS = ("TAPE_RANGES_DIR", "RANGE_TAPE_KEYS", "RANGE_TAPE_COLS",
                      "RANGE_TAPE_FLOATS", "RANGE_TAPE_STRINGS")
RANGE_MAIN_TAPE_WRITER = "write_tape"    # the D-4 writer: it must exist and read no range

# ── ROUND-1 REVIEW (2026-09-22): the routes the legs above walked past ──────────────
# (c) THE MACHINE BY NO OTHER ROUTE. Each of these reaches a module with no import
# statement naming it (importlib.import_module("rangefinder_core"), __import__(...),
# globals()["RNG"], vars(importlib.import_module(__name__))["RNG"], getattr(...)) or
# plants a value on one (setattr). MEASURED on the oracle_daily.py of 2026-09-22: not
# one Name among them, not one of those attributes, no import of those modules. So a
# ban costs nothing today and each is red on sight.
RANGE_DYNAMIC_NAMES = ("__import__", "importlib", "globals", "vars", "locals", "eval",
                       "exec", "compile", "getattr", "setattr", "delattr",
                       "__builtins__", "builtins", "runpy", "pkgutil",
                       # round 2: the machine FOUND rather than named — hasattr() over
                       # sys.modules, gc.get_objects() or a frame's f_globals
                       "hasattr", "gc", "inspect", "operator", "ctypes")
RANGE_DYNAMIC_MODULES = ("importlib", "imp", "runpy", "pkgutil", "builtins", "zipimport",
                         "gc", "inspect", "operator", "ctypes")
RANGE_DYNAMIC_ATTRS = ("modules", "__dict__", "__globals__", "__builtins__", "__import__",
                       # round 2: frames, the object graph, a module's own path
                       "_getframe", "currentframe", "f_globals", "f_locals", "f_back",
                       "get_objects", "get_referents", "get_referrers", "__getattribute__",
                       "__file__", "__code__", "__closure__", "__spec__", "__loader__")
# `from sys import modules as _M` / `from sys import _getframe`: the ImportFrom's parts
# are {sys, modules} and `.modules` never appears as an Attribute (round 2). `import sys`
# stays legal — oracle_daily needs sys.path — and ANY `from sys import` is red, on both
# sides of the wall.
RANGE_SYS = "sys"
RANGE_SELF_MODULE = "oracle_daily"
# (c) NO STASH. A call of one of these on a module-level name mutates module state.
RANGE_MUTATORS = ("append", "extend", "insert", "update", "setdefault", "pop", "popitem",
                  "clear", "remove", "add", "discard", "sort", "reverse", "appendleft",
                  "extendleft", "__setitem__", "__delitem__", "__setattr__", "__delattr__")
# (c) NO STASH, widened (round 2): a LOCAL bound to a module-level object — a Name /
# Attribute / Subscript chain rooted at one, or one of these accessor calls on it — IS
# that object, so a store through it is a store into module state.
RANGE_ACCESSORS = ("get", "items", "values", "setdefault", "__getitem__")

# ── ROUND-2 REVIEW (2026-09-22): ROUTES, NOT SPELLINGS ─────────────────────────────
# (c) THE MACHINE'S API. Every name the two machines define at module level — DERIVED
# from their source (_range_api_names), never typed: run_v2, tape_from_klines, snapshot,
# PINS_V2, V2_WINDOW_BARS, run_machine, _span, Range ... — is red as an ATTRIBUTE or as
# a STRING anywhere in oracle_daily.py but range_layer() and REGISTER's
# RNG.V2_WINDOW_BARS, and so is the Name RNG: whatever route found the module, a gate
# still has to call it by one of those names. MEASURED on the oracle_daily.py of
# 2026-09-22: one other use, census2b_program's own ATR_LEN (another module's constant
# that shares the name), named here by (function, expression).
RANGE_API_OK = {"mantle_payload": ("P.ATR_LEN",)}
# (b)+(c) THE REVERSE IMPORT INDEX: every repo module under RANGE_INDEX_DIRS that
# imports one of RANGE_INDEX_TARGETS — the two machines, the two wrappers that
# re-export one, the Oracle (its RNG) — at any depth, transitively (MEASURED 2026-09-22:
# 30 of 179 modules, oracle_fixtures, oracle_topup, oracle_wrapper and tierc10_* among
# them; none reachable from the decision side). A decision module may import none of
# them; oracle_daily none but its own `import rangefinder_core as RNG` and the one lazy
# import below (oracle_topup, whose module imports oracle_daily only inside --enumerate:
# render_html reads its REGISTER's [VETO] rows).
RANGE_INDEX_DIRS = ("scripts", "analytics", "engine")
RANGE_INDEX_TARGETS = (ORACLE_RANGE_MODULE, RANGE_MACHINE, "rangefinder_twin",
                       "analytics.rangefinder_census", RANGE_SELF_MODULE)
RANGE_OD_IMPORT_OK = {"render_html": ("oracle_topup",)}
# (d) what run() writes, all redirected; and the allow-listed readers run() hands the
# view to, each guarded by repr() before and after.
RANGE_RUN_DIRS = ("OUT_DIR", "PAYLOAD_DIR", "TAPE_DIR", "TAPE_RANGES_DIR", "CAL_DIR")
# (d) what run() READS from the lane's own tree, COPIED into the box and pointed at there
# (round 2: both still resolved into the live repo, and either is a root a sibling path
# can be cut from). The kline cache is outside the repo and is read where it is.
RANGE_RUN_READS = ("GRID_PARQUET", "MOVERS_DIR")
RANGE_VIEW_READERS = ("render_html", "write_range_tape")
RANGE_RUN_ORDER = ("EMPTY", "HOT", "REAL")              # REAL LAST
RANGE_SEED_FILE = "oracle_tape_ranges_2000-01-01.parquet"   # each run's "yesterday"
# (d) THE READ TRIPWIRE: the live directory, the file prefix, the readers wrapped for the
# length of a run, and the audit events watched (see _range_watching)
RANGE_LIVE_SIBLING = ROOT / "research_outputs" / "oracle" / "tape_ranges"
RANGE_SIBLING_PREFIX = "oracle_tape_ranges_"
RANGE_READ_FUNCS = (("pandas", "read_parquet"), ("pandas.io.parquet", "read_parquet"),
                    ("pyarrow.parquet", "read_table"), ("pyarrow.parquet", "read_schema"),
                    ("pyarrow.parquet", "read_metadata"), ("pyarrow.parquet", "ParquetFile"),
                    ("pyarrow.parquet", "ParquetDataset"),
                    ("pyarrow.parquet.core", "read_table"),
                    ("pyarrow.parquet.core", "read_schema"),
                    ("pyarrow.parquet.core", "read_metadata"),
                    ("pyarrow.dataset", "dataset"))
RANGE_AUDIT_LISTS = ("os.listdir", "os.scandir", "glob.glob", "glob.glob/2")
# (h) THE LANE'S PATHS: which function may name which path. MEASURED on the
# oracle_daily.py of 2026-09-22 — exactly these uses and no other; ROOT and __file__
# are named by no function at all. MOVERS_DIR is F-MV-9's fence and GRID_PARQUET the
# grid's; both are held here too, since either is a root a sibling path can hang from.
RANGE_LANE_PATHS = {
    "ROOT": (), "__file__": (),
    "OUT_DIR": ("run",), "PAYLOAD_DIR": ("run",),
    "TAPE_DIR": ("write_tape", "edition_count"),
    "TAPE_RANGES_DIR": ("write_range_tape",),
    "CAL_DIR": ("write_calibration",),
    "GRID_PARQUET": ("grid_toll",), "MOVERS_DIR": ("load_movers",),
    "cache_dir": ("load_lens",),
}
# a path walked from wherever it was: none in any function today, and at module level
# only inside ROOT's own definition (Path(__file__).resolve().parent.parent)
RANGE_PATH_WALKS = ("parent", "parents", "cwd", "home", "resolve", "absolute",
                    "expanduser")
# every call that touches the disk to READ, and the only functions that make one
# (measured: edition_count glob; grid_toll and load_lens exists + read_parquet;
# load_movers is_file + read_bytes; run, write_tape and write_range_tape read back the
# bytes they just wrote)
RANGE_DISK_CALLS = ("read_parquet", "read_table", "ParquetFile", "ParquetDataset",
                    "read_schema", "read_metadata", "dataset", "read_text", "read_bytes",
                    "open", "glob", "rglob", "iterdir", "listdir", "scandir", "walk",
                    "read_csv", "read_json", "load", "exists", "is_file", "is_dir", "stat")
RANGE_DISK_READERS = ("edition_count", "grid_toll", "load_lens", "load_movers", "run",
                      "write_tape", "write_range_tape")
RANGE_LANE_TEXT = "research_outputs"
# (h) the only things a function does with a lane path it may name (round 2, MEASURED on
# the oracle_daily.py of 2026-09-22: `/` joins, .mkdir / .exists / .glob, a reader's
# argument, cache_dir(), and one f-string inside grid_toll's `raise`). Anything else —
# str(), .replace, .as_posix, os.fspath, an f-string that is not an error message — turns
# the path into text that can be cut into any other path.
RANGE_LANE_PATH_ATTRS = ("mkdir", "exists", "glob")
# (b) THE DECISION SIDE PARSED AS CODE. MEASURED over the whole scan set of 2026-09-22
# (31 files since the round-2 import walk): no `.modules`, no string naming
# `rangefinder` or `oracle_daily`, and two dynamic uses — census2b_program.
# fixtures_stage4, its own F-B5c, which loads scripts/census2a_program.py by path to
# compare a copied function, and tierc5_rules' Card.diff_from_v5, which getattr()s its
# own dataclass fields to print a diff. Those two are named below by (file, function or
# Class.method); the rest of each file is held. ROUND 2 widened every list here —
# measured first, and the two named uses are the only cost.
RANGE_DECISION_DYNAMIC = ("__import__", "importlib", "globals", "vars", "eval", "exec",
                          "getattr", "setattr", "delattr", "hasattr", "locals", "compile",
                          "__builtins__", "builtins", "pkgutil", "runpy", "inspect", "gc")
RANGE_DECISION_STRINGS = ("rangefinder", "oracle_daily")
RANGE_DECISION_DYNAMIC_OK = {"scripts/census2b_program.py": ("fixtures_stage4",),
                             "scripts/tierc5_rules.py": ("Card.diff_from_v5",)}
# an Import or ImportFrom of these is red on the decision side, and any `from sys import`
RANGE_DECISION_IMPORT_BANS = ("importlib", "pkgutil", "runpy", "builtins", "inspect", "gc",
                              "imp", "zipimport", "operator", "ctypes")
RANGE_DECISION_ATTRS = ("modules", "__dict__", "__globals__", "__builtins__", "__import__",
                        "f_globals", "f_locals", "f_back", "_getframe", "currentframe",
                        "get_objects", "__getattribute__")


def _range_sha(pe_bytes: bytes | None = None) -> tuple[list[str], str]:
    b = (ROOT / "scripts" / "posture_engine.py").read_bytes() if pe_bytes is None else pe_bytes
    got = hashlib.sha256(b).hexdigest()
    if got != POSTURE_ENGINE_SHA256:
        return [f"posture_engine.py is not the pinned file: sha256 {got} != pinned "
                f"{POSTURE_ENGINE_SHA256}"], got
    return [], got


def _closure_src(modname: str, src: str) -> set[str]:
    """_closure() of a PLANTED copy: `src` is written as <modname>.py into a throwaway
    directory that goes FIRST on the subprocess's path, so it shadows the real module
    there and nowhere else. No file in the repo is touched."""
    with tempfile.TemporaryDirectory(prefix="f-br-14-") as td:
        (Path(td) / f"{modname}.py").write_text(src, encoding="utf-8")
        code = ("import sys, json; sys.dont_write_bytecode = True; "
                "sys.path.insert(0,'.'); sys.path.insert(0,'scripts'); "
                f"sys.path.insert(0,{td!r}); import {modname}; "
                "print(json.dumps(sorted(set(sys.modules))))")
        out = subprocess.run([sys.executable, "-c", code], cwd=ROOT,
                             capture_output=True, text=True)
    if out.returncode != 0:
        raise RuntimeError(out.stderr[-400:])
    return set(json.loads(out.stdout.strip().splitlines()[-1]))


def _range_reach(who: str, closure: set[str], banned) -> list[str]:
    hits = sorted(x for x in closure if set(x.split(".")) & set(banned))
    return [f"{who} reaches {hits[:4]} (component-wise match on {sorted(banned)})"] if hits else []


def _range_machine_files() -> set[Path]:
    """The two range machines' own files — the scan below reads the DECISION side, and
    a machine is not decision-side. RANGE_MACHINE (engine/rangefinder.py, TIER-C10's)
    sits in the engine/ glob; ORACLE_RANGE_MODULE (scripts/rangefinder_core.py) is in
    no glob below and is named so that it never can be."""
    return {(ROOT / (RANGE_MACHINE.replace(".", "/") + ".py")).resolve(),
            (ROOT / "scripts" / f"{ORACLE_RANGE_MODULE}.py").resolve()}


def _range_static_sources() -> dict[str, str]:
    machines = _range_machine_files()
    files = sorted((ROOT / "engine").glob("*.py"))
    files += [ROOT / "scripts" / "posture_engine.py"]
    files += sorted((ROOT / "scripts").glob("tierc*_rules.py"))
    return {str(p.relative_to(ROOT)): p.read_text(encoding="utf-8", errors="replace")
            for p in files if p.resolve() not in machines}


def _range_static(sources: dict[str, str]) -> list[str]:
    bad = []
    for name, text in sources.items():
        m = RANGE_IMPORT_LINE.search(text)
        if m:
            bad.append(f"{name} imports the range machine: `{m.group(0).strip()}`")
    return bad


def _range_oracle_machine(od_closure: set[str]) -> list[str]:
    """Leg (e), judged on oracle_daily's closure (real, or a planted copy's): the
    Oracle runs ORACLE_RANGE_MODULE, and RANGE_MACHINE — the engine/ copy that is
    TIER-C10's machine of record — is nowhere in it (A-OR1-1 iv)."""
    bad = []
    if ORACLE_RANGE_MODULE not in od_closure:
        bad.append(f"oracle_daily does not import {ORACLE_RANGE_MODULE} — the range layer's "
                   f"machine is not there, so the legs guarding it guard nothing")
    eng = sorted(x for x in od_closure if x == RANGE_MACHINE or x.startswith(RANGE_MACHINE + "."))
    if eng:
        bad.append(f"oracle_daily reaches the engine copy {eng} — the Oracle's range machine is "
                   f"{ORACLE_RANGE_MODULE} (scripts/, A-OR1-1 iv); {RANGE_MACHINE} is TIER-C10's "
                   f"machine of record and engine/ is outside this lane's write authority")
    return bad


def _closure_files(modname: str, shadow: str | None = None,
                   pre: tuple[str, ...] = ()) -> dict[str, str | None]:
    """{module: its __file__ or None} for EVERYTHING `import modname` leaves in
    sys.modules of a clean subprocess — _closure()'s names, with the files that the
    decision-side scan set is derived from. `shadow`, if given, is a throwaway directory
    put FIRST on the path, and the packages in `pre` are imported from it BEFORE
    `modname`: oracle_daily's own `sys.path.insert(0, ROOT)` would otherwise put the real
    package back in front of the planted copy. No file in the repo is touched."""
    code = ("import sys, json; sys.dont_write_bytecode = True; "
            "sys.path.insert(0,'.'); sys.path.insert(0,'scripts'); "
            + (f"sys.path.insert(0,{shadow!r}); " if shadow else "")
            + "".join(f"import {p}; " for p in pre)
            + f"import {modname}; "
            "print(json.dumps({k: getattr(m, '__file__', None) "
            "for k, m in sorted(list(sys.modules.items()))}))")
    out = subprocess.run([sys.executable, "-c", code], cwd=ROOT, capture_output=True, text=True)
    if out.returncode != 0:
        raise RuntimeError(out.stderr[-400:])
    return json.loads(out.stdout.strip().splitlines()[-1])


def _under(p: Path, base: Path) -> bool:
    try:
        p.relative_to(base)
        return True
    except ValueError:
        return False


def _range_local_files(files: dict[str, str | None], shadow: str | None = None) -> dict[str, Path]:
    """{repo-relative name: path} of the .py files in a closure that live in the repo
    (or in the plant's shadow directory, named as if they did)."""
    bases = ([Path(shadow).resolve()] if shadow else []) + [ROOT]
    out = {}
    for f in files.values():
        if not f or not f.endswith(".py"):
            continue
        p = Path(f).resolve()
        base = next((b for b in bases if _under(p, b)), None)
        if base is not None:
            out[str(p.relative_to(base))] = p
    return out


def _range_decision_sources(closures: dict[str, dict], shadow: str | None = None,
                            index: dict | None = None) -> dict[str, str]:
    """Leg (b)'s text-scan set, DERIVED FROM THE REAL CLOSURES (round-1 review,
    2026-09-22). The fixed set (_range_static_sources: engine/*, posture_engine.py,
    tierc*_rules.py) PLUS every repo-local file that oracle_daily or a decision module
    actually loads — minus oracle_daily.py itself (it is leg (c)'s, and it names the
    machine and the sibling tape by design) and the two machines. Before this,
    analytics/levels.py — where level_registry's levels are made — was in no scan.
    PLUS, since the round-2 review, every repo module those files name in an import
    statement at ANY depth, followed statically (_range_follow): a module imported only
    inside a function is in no closure, and a new shim re-exporting the machine there
    was in no scan at all."""
    out = _range_static_sources()
    skip = _range_machine_files() | {(ROOT / "scripts" / "oracle_daily.py").resolve()}
    paths: dict[str, Path] = {}
    for files in closures.values():
        for name, p in _range_local_files(files, shadow).items():
            if p not in skip and not _under(p, ROOT / ".claude"):
                paths[name] = p
    idx = index if index is not None else _range_import_index(shadow)
    start = {**{n: (ROOT / n).resolve() for n in out}, **paths}
    for name, p in _range_follow(start, idx, shadow).items():
        if p not in skip and not _under(p, ROOT / ".claude"):
            paths.setdefault(name, p)
    for name, p in paths.items():
        out[name] = p.read_text(encoding="utf-8", errors="replace")
    return out


def _import_parts(n) -> set[str]:
    """Every dotted component an Import / ImportFrom node names: module and names."""
    parts = set((getattr(n, "module", None) or "").split("."))
    for a in n.names:
        parts |= set(a.name.split("."))
    parts.discard("")
    parts.discard("*")
    return parts


# ── THE REVERSE IMPORT INDEX (round-2 review, 2026-09-22) ──────────────────────────
def _range_modname(rel: str) -> str:
    """A scan-set name as the module it is imported as: 'scripts/x.py' -> 'x',
    'analytics/levels.py' -> 'analytics.levels', 'engine/__init__.py' -> 'engine'."""
    p = Path(rel)
    if len(p.parts) == 2 and p.parts[0] in RANGE_INDEX_DIRS and p.parts[0] != "scripts":
        return p.parts[0] if p.stem == "__init__" else f"{p.parts[0]}.{p.stem}"
    return p.stem


def _range_repo_modules(shadow: str | None = None) -> dict[str, Path]:
    """{module name: file} for every .py under RANGE_INDEX_DIRS — scripts/ as top-level
    modules (it is on the path), analytics/ and engine/ as packages. A shadow
    directory's copies come FIRST, as they do on the plant's path."""
    out: dict[str, Path] = {}
    for base in ([Path(shadow).resolve()] if shadow else []) + [ROOT]:
        for d in RANGE_INDEX_DIRS:
            for p in sorted((base / d).glob("*.py")):
                name = (p.stem if d == "scripts"
                        else d if p.stem == "__init__" else f"{d}.{p.stem}")
                out.setdefault(name, p)
    return out


def _import_candidates(n, modname: str, is_pkg: bool, mods) -> set[str]:
    """The repo modules (keys of `mods`) one Import / ImportFrom node can load: every
    dotted prefix of the module it names, and <module>.<name> for each name imported
    from it. A relative import resolves against the importing module's package."""
    names: set[str] = set()
    if isinstance(n, ast.Import):
        for a in n.names:
            parts = a.name.split(".")
            names |= {".".join(parts[:i]) for i in range(1, len(parts) + 1)}
    else:
        if n.level:
            pkg = [x for x in (modname if is_pkg else modname.rpartition(".")[0]).split(".") if x]
            base = pkg[: max(0, len(pkg) - (n.level - 1))]
            mod = ".".join([*base, *[x for x in (n.module or "").split(".") if x]])
        else:
            mod = n.module or ""
        parts = [x for x in mod.split(".") if x]
        names |= {".".join(parts[:i]) for i in range(1, len(parts) + 1)}
        names |= {f"{mod}.{a.name}" if mod else a.name for a in n.names}
    return {x for x in names if x in mods}


def _range_import_index_build(shadow: str | None) -> dict:
    mods = _range_repo_modules(shadow)
    graph: dict[str, set[str]] = {}
    unread = []
    for m, p in mods.items():
        try:
            tree = ast.parse(p.read_text(encoding="utf-8", errors="replace"))
        except (SyntaxError, ValueError):
            unread.append(m)
            graph[m] = set()
            continue
        pkg = p.name == "__init__.py"
        graph[m] = {c for n in ast.walk(tree) if isinstance(n, (ast.Import, ast.ImportFrom))
                    for c in _import_candidates(n, m, pkg, mods)}
    # an unreadable module cannot be cleared: it is in the index (fail closed)
    tainted = set(RANGE_INDEX_TARGETS) | set(unread)
    grew = True
    while grew:
        grew = False
        for m, deps in graph.items():
            if m not in tainted and deps & tainted:
                tainted.add(m)
                grew = True
    return {"modules": mods, "graph": graph, "tainted": frozenset(tainted),
            "unreadable": sorted(unread)}


@functools.lru_cache(maxsize=1)
def _range_import_index_live() -> dict:
    return _range_import_index_build(None)


def _range_import_index(shadow: str | None = None) -> dict:
    """THE REVERSE IMPORT INDEX: every repo module that imports a machine, a wrapper
    re-exporting one, or oracle_daily (RANGE_INDEX_TARGETS) — at ANY depth, lazily or
    not, and transitively. Parsed, never imported. The live tree's index is built once
    per process; a shadow directory's, every time."""
    return _range_import_index_live() if shadow is None else _range_import_index_build(shadow)


def _range_follow(start: dict[str, Path], index: dict, shadow: str | None = None) -> dict[str, Path]:
    """Every repo module reachable from the files in `start` by import statements, at
    any depth, followed STATICALLY — never through oracle_daily or a machine — named as
    the scan set names files. Only the ones not already in `start`."""
    mods = index["modules"]
    by_path = {p.resolve(): m for m, p in mods.items()}
    have = {p.resolve() for p in start.values()}
    seen = {by_path[p] for p in have if p in by_path}
    todo = list(seen)
    stop = {ORACLE_RANGE_MODULE, RANGE_MACHINE, RANGE_SELF_MODULE}
    while todo:
        m = todo.pop()
        if m in stop:
            continue
        for d in index["graph"].get(m, ()):
            if d not in seen:
                seen.add(d)
                todo.append(d)
    bases = ([Path(shadow).resolve()] if shadow else []) + [ROOT]
    out = {}
    for m in sorted(seen):
        p = mods[m].resolve()
        base = next((b for b in bases if _under(p, b)), None)
        if p not in have and base is not None:
            out[str(p.relative_to(base))] = p
    return out


def _range_sole_importer(files: dict[str, str | None], shadow: str | None = None) -> list[str]:
    """Leg (e), widened: of every repo-local module oracle_daily's closure holds,
    oracle_daily is the ONLY one whose code imports ORACLE_RANGE_MODULE (at any depth).
    A second importer on the Oracle's own path is a gate that can run the machine."""
    bad = []
    for name, p in sorted(_range_local_files(files, shadow).items()):
        if p.resolve() in {(ROOT / "scripts" / "oracle_daily.py").resolve(),
                           (ROOT / "scripts" / f"{ORACLE_RANGE_MODULE}.py").resolve()}:
            continue
        try:
            tree = ast.parse(p.read_text(encoding="utf-8", errors="replace"))
        except SyntaxError as e:
            bad.append(f"{name} does not parse ({e}) — leg (e) cannot read it; fail closed")
            continue
        for n in ast.walk(tree):
            if isinstance(n, (ast.Import, ast.ImportFrom)) and ORACLE_RANGE_MODULE in _import_parts(n):
                bad.append(f"{name} imports {ORACLE_RANGE_MODULE} (line {n.lineno}: "
                           f"`{ast.unparse(n)}`) — oracle_daily must be the ONLY module on the "
                           f"Oracle's path that imports the range machine")
    return bad


def _docstring_ids(tree) -> set[int]:
    """id() of every docstring Constant: prose may name anything."""
    docs = set()
    for n in ast.walk(tree):
        if isinstance(n, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            b = getattr(n, "body", [])
            if (b and isinstance(b[0], ast.Expr) and isinstance(b[0].value, ast.Constant)
                    and isinstance(b[0].value.value, str)):
                docs.add(id(b[0].value))
    return docs


def _range_decision_ast(sources: dict[str, str], index: dict | None = None) -> list[str]:
    """Leg (b), THE DECISION SIDE PARSED AS CODE (round-1 review, 2026-09-22). The
    import LINE (RANGE_IMPORT_LINE, frozen: TIER-C10 reads it) sees one line at a time
    and only a statement that starts one: `from engine import (\\n rangefinder,\\n)`,
    `import \\\\\\n rangefinder_core`, importlib, __import__, sys.modules[...] and
    `from oracle_daily import RNG` all walked past it, and the closure leg sees a LAZY
    import only when its function runs. This reads every file as a tree instead.
    ROUND 2 (2026-09-22): `from importlib import import_module`, getattr(sys,
    'modules'), pkgutil.resolve_name, __builtins__['__import__'], `import engine;
    engine.rangefinder`, sys._getframe(2).f_globals['RNG'] and a re-exporter
    (`import oracle_fixtures as _OF; _OF.OD.RNG`) were all green here. Each is red now:
    the import machinery by ANY import form, any `from sys import`, the frame and
    namespace attributes, an attribute carrying `rangefinder` or named RNG, the string
    'RNG', and an import of any module in the reverse import index."""
    idx = index if index is not None else _range_import_index()
    bad = []
    for name, text in sources.items():
        try:
            tree = ast.parse(text)
        except SyntaxError as e:
            bad.append(f"{name} does not parse ({e}) — the decision-side scan cannot read it; "
                       f"fail closed")
            continue
        docs = _docstring_ids(tree)
        ok = RANGE_DECISION_DYNAMIC_OK.get(name, ())
        exempt: set[int] = set()
        for st in tree.body:
            if isinstance(st, (ast.FunctionDef, ast.AsyncFunctionDef)) and st.name in ok:
                exempt |= {id(x) for x in ast.walk(st)}
            elif isinstance(st, ast.ClassDef):
                for m in st.body:
                    if (isinstance(m, (ast.FunctionDef, ast.AsyncFunctionDef))
                            and f"{st.name}.{m.name}" in ok):
                        exempt |= {id(x) for x in ast.walk(m)}
        modname, is_pkg = _range_modname(name), Path(name).name == "__init__.py"
        for n in ast.walk(tree):
            if isinstance(n, (ast.Import, ast.ImportFrom)):
                parts = _import_parts(n)
                hit = sorted(p for p in parts
                             if p in RANGE_BANNED_IN_DECISION or "rangefinder" in p)
                if hit:
                    bad.append(f"{name}:{n.lineno} imports the range machine or the Oracle "
                               f"(`{ast.unparse(n)}`, components {hit}) — as code, at any depth: "
                               f"a decision module may not reach a range")
                top = ({a.name.split(".")[0] for a in n.names} if isinstance(n, ast.Import)
                       else {(n.module or "").split(".")[0]} if not n.level else set())
                dyn = sorted(top & set(RANGE_DECISION_IMPORT_BANS))
                if dyn and id(n) not in exempt:
                    bad.append(f"{name}:{n.lineno} imports the dynamic-import machinery {dyn} "
                               f"(`{ast.unparse(n)}`) — by ANY import form, not only the Name: "
                               f"`from importlib import import_module as _im` loads no Name "
                               f"`importlib` at all")
                if isinstance(n, ast.ImportFrom) and not n.level and RANGE_SYS in top:
                    bad.append(f"{name}:{n.lineno} imports FROM sys (`{ast.unparse(n)}`) — "
                               f"sys.modules and sys._getframe under any name")
                reach = sorted(c for c in _import_candidates(n, modname, is_pkg, idx["modules"])
                               if c in idx["tainted"])
                if reach and not hit:
                    bad.append(f"{name}:{n.lineno} imports {reach} (`{ast.unparse(n)}`) — a repo "
                               f"module that imports the range machine or the Oracle at some "
                               f"depth (the reverse import index): a re-exporter IS the machine")
            elif isinstance(n, ast.Name) and n.id in RANGE_DECISION_DYNAMIC and id(n) not in exempt:
                bad.append(f"{name}:{n.lineno} names `{n.id}` — a dynamic import reaches a module no "
                           f"import statement names; the decision side holds none but "
                           f"{dict(RANGE_DECISION_DYNAMIC_OK)}")
            elif (isinstance(n, ast.Attribute) and n.attr in RANGE_DECISION_ATTRS
                  and (id(n) not in exempt or n.attr == "modules")):   # .modules: never
                bad.append(f"{name}:{n.lineno} reads a `.{n.attr}` attribute — a module, a frame or "
                           f"a namespace (sys.modules, f_globals, __dict__) reached with no "
                           f"import statement")
            elif isinstance(n, ast.Attribute) and ("rangefinder" in n.attr or n.attr == RANGE_ALIAS):
                bad.append(f"{name}:{n.lineno} reads the attribute `.{n.attr}` — the range machine "
                           f"or the Oracle's own binding of it, by attribute walk")
            elif (isinstance(n, ast.Constant) and isinstance(n.value, str) and id(n) not in docs
                  and (any(t in n.value for t in RANGE_DECISION_STRINGS)
                       or n.value == RANGE_ALIAS)):
                t = next((t for t in RANGE_DECISION_STRINGS if t in n.value), RANGE_ALIAS)
                bad.append(f"{name}:{n.lineno} spells {t!r} in a string ({n.value[:50]!r}) — the "
                           f"name a dynamic import, or a namespace lookup, would be handed")
    return bad


def _range_closures() -> tuple[list[str], dict]:
    """Legs (b) and (e), the real thing: one clean subprocess per module, side by side.
    The closures also DERIVE the decision-side scan set that (b)'s text scans and (h)'s
    sibling scan read (round-1 review)."""
    from concurrent.futures import ThreadPoolExecutor
    mods = (*RANGE_DECISION_MODULES, ORACLE_RANGE_MODULE, "oracle_daily")
    with ThreadPoolExecutor(max_workers=len(mods)) as ex:
        files = dict(zip(mods, ex.map(_closure_files, mods)))
    clos = {m: set(f) for m, f in files.items()}
    bad: list[str] = []
    for m in RANGE_DECISION_MODULES:
        bad += _range_reach(m, clos[m], RANGE_BANNED_IN_DECISION)
    bad += _range_reach(f"the range machine ({ORACLE_RANGE_MODULE})", clos[ORACLE_RANGE_MODULE],
                        RANGE_BANNED_IN_MACHINE)
    if ORACLE_RANGE_MODULE not in clos[ORACLE_RANGE_MODULE]:
        bad.append(f"{ORACLE_RANGE_MODULE} is absent from its own closure — the probe imported "
                   f"nothing")
    bad += _range_oracle_machine(clos["oracle_daily"])
    bad += _range_sole_importer(files["oracle_daily"])
    dec = {m: files[m] for m in (*RANGE_DECISION_MODULES, "oracle_daily")}
    idx = _range_import_index()
    if idx["unreadable"]:
        bad.append(f"the reverse import index could not parse {idx['unreadable'][:4]} — each is "
                   f"counted as importing the machine (fail closed); a decision module that "
                   f"imports one is red for it")
    sources = _range_decision_sources(dec, index=idx)
    fixed = _range_static_sources()
    loaded = {n for fs in dec.values() for n in _range_local_files(fs)}
    bad += _range_static(sources) + _range_decision_ast(sources, idx)
    return bad, {"sizes": {m: len(c) for m, c in clos.items()}, "static": len(sources),
                 "fixed": len(fixed), "derived": sorted(set(sources) - set(fixed)),
                 "followed": sorted(set(sources) - set(fixed) - loaded),
                 "sources": sources, "index": idx,
                 "local": len(_range_local_files(files["oracle_daily"]))}


def _range_mentions(node):
    """(lineno, what) for every way a range can be NAMED under `node`. Docstrings are
    whole-string constants and never equal a key, so prose cannot trip this."""
    for n in ast.walk(node):
        if isinstance(n, ast.Constant) and isinstance(n.value, str) and (
                n.value == RANGE_KEY or n.value in RANGE_ONLY_KEYS):
            yield n, f"the key {n.value!r}"
        elif isinstance(n, ast.Name) and (n.id == RANGE_ALIAS or n.id in RANGE_HELPERS):
            yield n, f"the name `{n.id}`"
        elif isinstance(n, ast.Attribute) and n.attr in RANGE_HELPERS:
            yield n, f"the attribute `.{n.attr}`"


def _register_source_ids(tree) -> set[int]:
    """id() of every Constant inside the value of a 'source' key of oracle_daily's
    module-level REGISTER literal: the register's prose, which cites paths and modules."""
    out = set()
    for st in tree.body:
        tgt = (st.targets if isinstance(st, ast.Assign)
               else [st.target] if isinstance(st, ast.AnnAssign) else [])
        if not any(isinstance(t, ast.Name) and t.id == "REGISTER" for t in tgt):
            continue
        if not isinstance(st.value, ast.Dict):
            continue
        for row in st.value.values:
            if isinstance(row, ast.Dict):
                for k, v in zip(row.keys, row.values):
                    if isinstance(k, ast.Constant) and k.value == "source":
                        out |= {id(x) for x in ast.walk(v) if isinstance(x, ast.Constant)}
    return out


def _range_dynamic(tree) -> list[str]:
    """Leg (c), THE MACHINE BY NO OTHER ROUTE: every way to reach a module — the range
    machine, or oracle_daily's own RNG binding — without an import statement that names
    it. See RANGE_DYNAMIC_NAMES."""
    bad = []
    docs, sources = _docstring_ids(tree), _register_source_ids(tree)
    for n in ast.walk(tree):
        if isinstance(n, ast.Name) and n.id in RANGE_DYNAMIC_NAMES:
            bad.append(f"line {n.lineno}: `{n.id}` — a module (the range machine among them) can be "
                       f"reached through it with no import statement naming it; oracle_daily.py "
                       f"uses none of {len(RANGE_DYNAMIC_NAMES)} such names, so any is red")
        elif isinstance(n, ast.Attribute) and n.attr in RANGE_DYNAMIC_ATTRS:
            bad.append(f"line {n.lineno}: a `.{n.attr}` attribute — a module, a frame or a "
                       f"namespace (sys.modules, a module's __dict__, a frame's f_globals, the "
                       f"gc object graph, a module's own path) reached with no import statement "
                       f"naming it")
        elif isinstance(n, ast.Attribute) and n.attr == RANGE_ALIAS:
            bad.append(f"line {n.lineno}: an attribute `.{RANGE_ALIAS}` — the Oracle's own binding "
                       f"of the machine, read off a module object")
        elif isinstance(n, (ast.Import, ast.ImportFrom)):
            parts = _import_parts(n)
            if RANGE_SELF_MODULE in parts:
                bad.append(f"line {n.lineno}: `{ast.unparse(n)}` imports oracle_daily itself — its "
                           f"`{RANGE_ALIAS}` is then reachable under any name")
            if parts & set(RANGE_DYNAMIC_MODULES):
                bad.append(f"line {n.lineno}: `{ast.unparse(n)}` imports the dynamic-import "
                           f"machinery {sorted(parts & set(RANGE_DYNAMIC_MODULES))}")
            if (isinstance(n, ast.ImportFrom) and not n.level
                    and (n.module or "").split(".")[0] == RANGE_SYS):
                bad.append(f"line {n.lineno}: `{ast.unparse(n)}` imports FROM sys — "
                           f"sys.modules and sys._getframe under a name no attribute fence "
                           f"sees (round 2: `from sys import modules as _MODS`)")
            if isinstance(n, ast.ImportFrom) and any(a.name == RANGE_ALIAS for a in n.names):
                bad.append(f"line {n.lineno}: `{ast.unparse(n)}` imports the NAME "
                           f"`{RANGE_ALIAS}` — the alias fence compares the imported name, not "
                           f"only the name it is bound to")
        elif (isinstance(n, ast.Constant) and isinstance(n.value, str) and id(n) not in docs
              and id(n) not in sources
              and ("rangefinder" in n.value or n.value == RANGE_ALIAS)):
            bad.append(f"line {n.lineno}: the string {n.value[:40]!r} names the range machine "
                       f"outside REGISTER's sources — the name a dynamic import would be handed")
    return bad


@functools.lru_cache(maxsize=1)
def _range_api_names() -> tuple[str, ...]:
    """Every name the two machine files define at module level — functions, classes,
    assigned constants — read from their SOURCE, so the fence grows with the machine."""
    names: set[str] = set()
    for p in sorted(_range_machine_files()):
        tree = ast.parse(p.read_text(encoding="utf-8"))
        for st in tree.body:
            if isinstance(st, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                names.add(st.name)
            elif isinstance(st, (ast.Assign, ast.AnnAssign)):
                for t in (st.targets if isinstance(st, ast.Assign) else [st.target]):
                    names |= {x.id for x in ast.walk(t) if isinstance(x, ast.Name)}
    return tuple(sorted(names))


def _range_api(tree, api) -> list[str]:
    """Leg (c), THE MACHINE'S API, NOT ITS SPELLINGS (round-2 review, 2026-09-22). Every
    ban above is a SPELLING of a route to the module, and the review found seven more —
    `from sys import modules`, sys._getframe(0).f_globals, gc.get_objects(),
    inspect.currentframe(), `from sys import _getframe`, a module-level binding made at
    import time, a lazily imported re-exporter — each finding the machine by
    hasattr(_x, 'PINS_V2') and running the fixture's own damping gate, green on every
    static leg while heat moved on 2 of 18 symbols. Whatever the route, a gate CALLS the
    machine by one of the names it defines. So: the Name RNG, and every name in `api` as
    an attribute or as a string, appear only in range_layer() and REGISTER's
    RNG.V2_WINDOW_BARS (and RANGE_API_OK's measured coincidences). The other readers
    may read the view's 'range' key; they may not run the machine (OD-G: render_html
    ran it and flipped the filed D-7 target-bucket basis)."""
    bad = []
    if not api:
        bad.append("the range machine defines no name this scan can read — the API fence is "
                   "fencing nothing; fail closed")
    api = set(api)
    docs, sources = _docstring_ids(tree), _register_source_ids(tree)
    for st in tree.body:
        if isinstance(st, (ast.FunctionDef, ast.AsyncFunctionDef)) and st.name == RANGE_PRODUCER:
            continue
        named = isinstance(st, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
        where = f"{st.name}()" if named else "module level"
        ok = RANGE_API_OK.get(st.name, ()) if named else ()
        tgt = (st.targets if isinstance(st, ast.Assign)
               else [st.target] if isinstance(st, ast.AnnAssign) else [])
        is_register = any(isinstance(t, ast.Name) and t.id == "REGISTER" for t in tgt)
        parent = {c: p for p in ast.walk(st) for c in ast.iter_child_nodes(p)}
        for n in ast.walk(st):
            if isinstance(n, ast.Name) and n.id == RANGE_ALIAS:
                p = parent.get(n)
                if is_register and isinstance(p, ast.Attribute) and p.attr in RANGE_REGISTER_IMPORTS:
                    continue
                bad.append(f"{where} names the machine alias `{RANGE_ALIAS}` at line {n.lineno} — "
                           f"only {RANGE_PRODUCER}() may run the machine (and REGISTER import "
                           f"its window); a reader may read the view's {RANGE_KEY!r} key, never "
                           f"the machine")
            elif isinstance(n, ast.Attribute) and n.attr in api:
                if ast.unparse(n) in ok:
                    continue
                if (is_register and isinstance(n.value, ast.Name) and n.value.id == RANGE_ALIAS
                        and n.attr in RANGE_REGISTER_IMPORTS):
                    continue
                bad.append(f"{where} reads `.{n.attr}`, a name the range machine defines, at line "
                           f"{n.lineno} (`{ast.unparse(n)[:50]}`) — whatever route found the "
                           f"module, only {RANGE_PRODUCER}() may call it")
            elif (isinstance(n, ast.Constant) and isinstance(n.value, str) and n.value in api
                  and id(n) not in docs and id(n) not in sources):
                bad.append(f"{where} spells the string {n.value!r}, a name the range machine "
                           f"defines, at line {n.lineno} — the name getattr() or a namespace "
                           f"lookup would be handed")
    return bad


def _range_od_imports(tree, index: dict) -> list[str]:
    """Leg (c), THE REVERSE IMPORT INDEX on the Oracle's side (round 2): no import in
    oracle_daily.py, at any depth, loads a repo module that imports a machine, a
    wrapper or oracle_daily itself — but the one sanctioned `import rangefinder_core as
    RNG` and RANGE_OD_IMPORT_OK. A lazily imported re-exporter (the review's OD-E: a
    TIER-C10 fixture that binds engine.rangefinder as E) hands a gate the machine under
    a name nothing else here fences."""
    bad = []
    mods, tainted = index["modules"], index["tainted"]
    for st in tree.body:
        fn = st.name if isinstance(st, (ast.FunctionDef, ast.AsyncFunctionDef)) else None
        ok = set(RANGE_OD_IMPORT_OK.get(fn, ())) if fn else set()
        for n in ast.walk(st):
            if not isinstance(n, (ast.Import, ast.ImportFrom)):
                continue
            if (fn is None and isinstance(n, ast.Import) and len(n.names) == 1
                    and n.names[0].name == ORACLE_RANGE_MODULE
                    and n.names[0].asname == RANGE_ALIAS):
                continue                           # THE sanctioned binding
            hit = sorted(c for c in _import_candidates(n, RANGE_SELF_MODULE, False, mods)
                         if c in tainted and c not in ok)
            if hit:
                bad.append(f"line {n.lineno}: `{ast.unparse(n)}` "
                           f"({fn + '()' if fn else 'module level'}) imports {hit} — a repo "
                           f"module that imports the range machine or the Oracle at some depth "
                           f"(the reverse import index): a re-exporter IS the machine")
    return bad


def _range_stash(tree) -> list[str]:
    """Leg (c), NO STASH (round-1 review, 2026-09-22): no function in oracle_daily.py
    stores into module-level state. Plant OD-9 kept a module-level `_MEMO` that
    range_layer (allow-listed) filled and build_view read back without naming a range;
    leg (c) never scans an allow-listed function, and leg (d)'s stubbed runs read REAL's
    memo. A reader can hand its value to any helper, so the WHOLE file is held (0 such
    stores, measured). Red: `global` / `nonlocal`; a store into, or a delete of, an
    attribute or item whose root is a module-level name the function has not rebound;
    a RANGE_MUTATORS call on one. AND, since the round-2 review (OD-G: `_q =
    REGISTER["TARGET_BUCKET_ATR"]; _q["value"] = ...` inside render_html flipped the
    filed D-7 basis), the same on a LOCAL ALIAS of a shared object: a local bound —
    by assignment, walrus, a for / comprehension target or `with ... as` — to a Name /
    Attribute / Subscript chain rooted at a shared name, or to a RANGE_ACCESSORS call on
    one (`.get`, `.items`, `.values` ...), is shared itself, to a fixed point. NOT seen:
    a shared object handed to another function as an ARGUMENT and stored into there —
    disclosed at the head of this block."""
    module = set()
    for st in tree.body:
        if isinstance(st, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            module.add(st.name)
            continue
        for n in ast.walk(st):
            if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store):
                module.add(n.id)
            elif isinstance(n, (ast.Import, ast.ImportFrom)):
                module |= {(a.asname or a.name).split(".")[0] for a in n.names}

    def root(x):
        while isinstance(x, (ast.Attribute, ast.Subscript, ast.Call, ast.Starred)):
            x = x.func if isinstance(x, ast.Call) else x.value
        return x.id if isinstance(x, ast.Name) else None

    def chain_root(x):
        """The root Name of an expression that IS an existing object (not a new one): a
        Name / Attribute / Subscript chain, through RANGE_ACCESSORS calls; else None."""
        while True:
            if isinstance(x, (ast.Attribute, ast.Subscript, ast.Starred)):
                x = x.value
            elif (isinstance(x, ast.Call) and isinstance(x.func, ast.Attribute)
                  and x.func.attr in RANGE_ACCESSORS):
                x = x.func.value
            else:
                break
        return x.id if isinstance(x, ast.Name) else None

    def bindings(fn):
        """(local name, the expression it is bound to) for every binding in `fn`."""
        def names(t):
            return [x.id for x in ast.walk(t) if isinstance(x, ast.Name)]
        for n in ast.walk(fn):
            if isinstance(n, (ast.Assign, ast.AnnAssign)) and n.value is not None:
                for t in (n.targets if isinstance(n, ast.Assign) else [n.target]):
                    if (isinstance(t, (ast.Tuple, ast.List)) and isinstance(n.value, (ast.Tuple, ast.List))
                            and len(t.elts) == len(n.value.elts)):
                        for e, v in zip(t.elts, n.value.elts):
                            yield from ((x, v) for x in names(e))
                    elif isinstance(t, (ast.Name, ast.Tuple, ast.List, ast.Starred)):
                        yield from ((x, n.value) for x in names(t))
            elif isinstance(n, ast.NamedExpr):
                yield n.target.id, n.value
            elif isinstance(n, (ast.For, ast.AsyncFor, ast.comprehension)):
                yield from ((x, n.iter) for x in names(n.target))
            elif isinstance(n, ast.withitem) and n.optional_vars is not None:
                yield from ((x, n.context_expr) for x in names(n.optional_vars))

    bad = []
    for fn in tree.body:
        if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        local = {a.arg for sub in ast.walk(fn) if isinstance(sub, ast.arguments)
                 for a in (*sub.posonlyargs, *sub.args, *sub.kwonlyargs,
                           *([sub.vararg] if sub.vararg else []),
                           *([sub.kwarg] if sub.kwarg else []))}
        for n in ast.walk(fn):
            if isinstance(n, ast.Name) and isinstance(n.ctx, (ast.Store, ast.Del)):
                local.add(n.id)
            elif isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and n is not fn:
                local.add(n.name)
            elif isinstance(n, (ast.Import, ast.ImportFrom)):
                local |= {(a.asname or a.name).split(".")[0] for a in n.names}
            elif isinstance(n, ast.ExceptHandler) and n.name:
                local.add(n.name)
        shared = module - local
        pairs = list(bindings(fn))
        grew = True
        while grew:                                # a local alias of shared state IS it
            grew = False
            for name, val in pairs:
                if name not in shared and chain_root(val) in shared:
                    shared.add(name)
                    grew = True

        def hit(n, what):
            bad.append(f"{fn.name}() stores into module-level state: {what} at line {n.lineno} "
                       f"— a value kept there outlives the call, and a gate can read what an "
                       f"allow-listed reader left behind without naming a range")

        for n in ast.walk(fn):
            if isinstance(n, (ast.Global, ast.Nonlocal)):
                hit(n, f"`{'global' if isinstance(n, ast.Global) else 'nonlocal'} "
                       f"{', '.join(n.names)}`")
                continue
            targets = (n.targets if isinstance(n, (ast.Assign, ast.Delete))
                       else [n.target] if isinstance(n, (ast.AugAssign, ast.AnnAssign)) else [])
            flat = []
            for t in targets:
                flat += list(t.elts) if isinstance(t, (ast.Tuple, ast.List)) else [t]
            for t in flat:
                if isinstance(t, (ast.Attribute, ast.Subscript, ast.Starred)) and root(t) in shared:
                    hit(n, f"`{ast.unparse(t)[:50]}`")
            if (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                    and n.func.attr in RANGE_MUTATORS and root(n.func.value) in shared):
                hit(n, f"`{ast.unparse(n.func)[:50]}(...)`")
    return bad


def _range_ast(src: str | None = None, index: dict | None = None) -> tuple[list[str], dict]:
    """Leg (c). Scans CODE, not prose: comments and docstrings cannot satisfy or trip it."""
    src = (ROOT / "scripts" / "oracle_daily.py").read_text(encoding="utf-8") if src is None else src
    tree = ast.parse(src)
    bad: list[str] = []
    fns = {n.name: n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}

    binds = [(n, a) for n in ast.walk(tree) if isinstance(n, (ast.Import, ast.ImportFrom))
             for a in n.names if (a.asname or a.name) == RANGE_ALIAS]
    # THE ONE SANCTIONED BINDING, since A-OR1-1 iv: `import rangefinder_core as RNG`
    # (it was `from engine import rangefinder as RNG` until 2026-09-22; that binding is
    # now RED here and in leg (e)).
    ok_bind = [1 for n, a in binds if isinstance(n, ast.Import)
               and a.name == ORACLE_RANGE_MODULE]
    if len(binds) != 1 or len(ok_bind) != 1:
        bad.append(f"`{RANGE_ALIAS}` must be bound exactly once, by `import "
                   f"{ORACLE_RANGE_MODULE} as {RANGE_ALIAS}` (found {len(binds)} binding(s), "
                   f"{len(ok_bind)} of them that one) — fail closed")
    # THE MACHINE, NOT ONE SPELLING (review finding, 2026-09-21). This read
    # `"rangefinder" in full.split(".")` — a dotted-COMPONENT test, and False for
    # `rangefinder_twin`. Since STEP D1 the twin is a thin caller that re-exports the
    # WHOLE machine (run_v2, PINS_V2, V2_WINDOW_BARS, Range, run_machine, _span, with
    # noqa F401) and sits in scripts/ beside posture_engine.py, so `import
    # rangefinder_twin as RT` reached the machine and this leg printed GREEN. Substring
    # now, so any re-exporter is caught; the sanctioned `import rangefinder_core as RNG`
    # stays exempt by its ALIAS, which is what the fence is actually about, and a second
    # alias of the same module (`import rangefinder_core as RC`) is not.
    # And the two routes that name no module at all: a bare package import walked to
    # `engine.rangefinder`, and a sys.modules lookup of the module the Oracle's own
    # import already put there (rangefinder_core since A-OR1-1). Both are absent from
    # the pristine file (verified before the guard was written), so both are
    # fail-closed, not taste.
    for n in ast.walk(tree):
        if isinstance(n, (ast.Import, ast.ImportFrom)):
            for a in n.names:
                full = f"{getattr(n, 'module', None) or ''}.{a.name}".strip(".")
                if "rangefinder" in full and (a.asname or a.name) != RANGE_ALIAS:
                    bad.append(f"line {n.lineno}: the range machine is imported a second way "
                               f"(`{full}` as `{a.asname or a.name}`) — the scan fences one alias")
                if isinstance(n, ast.Import) and "." not in a.name and a.name == "engine":
                    bad.append(f"line {n.lineno}: bare `import engine` — engine.rangefinder is "
                               f"reachable by attribute walk")
    # EVERY OTHER ROUTE THAT NAMES NO MODULE (round-1 review, 2026-09-22). The guard
    # above caught only a Subscript on `.modules`; sys.modules.get(...), importlib,
    # __import__, globals()["RNG"], `from oracle_daily import RNG as _Q` (the NAME is
    # RNG, only the asname was compared), `import oracle_daily as _S; _S.RNG` and
    # vars(importlib.import_module(__name__))["RNG"] were all GREEN here, and leg (d)
    # cannot back this leg up (a direct call cancels out of its comparison). Measured
    # on the pristine file first: none of them occurs, so every one is red on sight.
    bad += _range_dynamic(tree)
    bad += _range_stash(tree)
    # ROUTES, NOT SPELLINGS (round-2 review, 2026-09-22): the machine's own names are
    # fenced wherever they are read, and a lazily imported re-exporter is red by the
    # reverse import index — see _range_api and _range_od_imports.
    bad += _range_api(tree, _range_api_names())
    bad += _range_od_imports(tree, index if index is not None else _range_import_index())

    for stmt in tree.body:
        if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if stmt.name in RANGE_READERS or stmt.name == RANGE_WRITER:
                continue
            for n, what in _range_mentions(stmt):
                bad.append(f"{stmt.name}() mentions {what} at line {n.lineno} — it is not on the "
                           f"allow-list: a range may be read by the render and the tape and by "
                           f"nothing that gates")
            continue
        tgt = (stmt.targets if isinstance(stmt, ast.Assign)
               else [stmt.target] if isinstance(stmt, ast.AnnAssign) else [])
        is_register = any(isinstance(t, ast.Name) and t.id == "REGISTER" for t in tgt)
        parent = {c: p for p in ast.walk(stmt) for c in ast.iter_child_nodes(p)}
        for n, what in _range_mentions(stmt):
            p = parent.get(n)
            if (is_register and isinstance(n, ast.Name) and n.id == RANGE_ALIAS
                    and isinstance(p, ast.Attribute) and p.attr in RANGE_REGISTER_IMPORTS):
                continue                           # REGISTER importing the window: §6.4
            bad.append(f"module level mentions {what} at line {n.lineno} — outside every "
                       f"function, only REGISTER may read {RANGE_ALIAS}."
                       f"{'/'.join(RANGE_REGISTER_IMPORTS)}")

    bv = fns.get(RANGE_WRITER)
    writes = []
    if bv is None:
        bad.append(f"{RANGE_WRITER}() not found — fail closed")
    else:
        for n in ast.walk(bv):
            if not (isinstance(n, ast.Assign) and len(n.targets) == 1):
                continue
            t, v = n.targets[0], n.value
            if (isinstance(t, ast.Subscript) and isinstance(t.ctx, ast.Store)
                    and isinstance(t.slice, ast.Constant) and t.slice.value == RANGE_KEY
                    and isinstance(v, ast.Call) and isinstance(v.func, ast.Name)
                    and v.func.id == RANGE_PRODUCER and not v.keywords
                    and len(v.args) == 1 and isinstance(v.args[0], ast.Name)
                    and v.args[0].id == "h4"):
                writes.append(n)
        if len(writes) != 1:
            bad.append(f"{RANGE_WRITER}() must hold exactly ONE write of the shape "
                       f"`<asset>[{RANGE_KEY!r}] = {RANGE_PRODUCER}(h4)`; found {len(writes)}")
        inside = {id(x) for w in writes for x in ast.walk(w)}
        for n, what in _range_mentions(bv):
            if id(n) not in inside:
                bad.append(f"{RANGE_WRITER}() mentions {what} at line {n.lineno} OUTSIDE the "
                           f"one assignment — heat, the sort, the station and the card are "
                           f"computed here, and none of them may see a range")

    for g in (*RANGE_NAMED_GATES, RANGE_MAIN_TAPE_WRITER):
        if g not in fns:
            bad.append(f"{g}() not found — it is named as range-free and cannot be checked; "
                       f"fail closed")
    for r in RANGE_READERS:
        if r not in fns:
            bad.append(f"allow-listed reader {r}() not found — fail closed")
    # fail closed: the key this scan hunts must be the key the code really reads
    reads = {r: sum(1 for n, what in _range_mentions(fns[r]) if what == f"the key {RANGE_KEY!r}")
             for r in (RANGE_SIBLING_WRITER, "range_cell", "range_watch", "tide_tables")
             if r in fns}
    dead = [r for r, k in reads.items() if not k]
    if dead:
        bad.append(f"{dead} never read the key {RANGE_KEY!r} — the scan is hunting a stale "
                   f"name; fail closed")
    return bad, {"write_line": writes[0].lineno if writes else None, "reads": reads,
                 "functions": len(fns)}


def _range_plant_in(src: str, fn_name: str, stmt_src: str) -> str | None:
    """`stmt_src` planted as the first statement of `fn_name` (after its docstring)."""
    tree = ast.parse(src)
    fn = next((n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == fn_name), None)
    if fn is None:
        return None
    doc = (fn.body and isinstance(fn.body[0], ast.Expr)
           and isinstance(fn.body[0].value, ast.Constant) and isinstance(fn.body[0].value.value, str))
    at = 1 if doc else 0
    fn.body[at:at] = ast.parse(stmt_src).body
    return ast.unparse(ast.fix_missing_locations(tree))


def _range_plant_narrow_except(src: str) -> str | None:
    """range_layer's `except Exception` narrowed to ZeroDivisionError: the pre-containment
    world, in which a fault in the display organ escapes into build_view."""
    tree = ast.parse(src)
    fn = next((n for n in tree.body if isinstance(n, ast.FunctionDef)
               and n.name == RANGE_PRODUCER), None)
    hs = [h for n in ast.walk(fn) if isinstance(n, ast.Try) for h in n.handlers] if fn else []
    if len(hs) != 1:
        return None
    hs[0].type = ast.Name(id="ZeroDivisionError", ctx=ast.Load())
    return ast.unparse(ast.fix_missing_locations(tree))


def _range_plant_after_write(src: str, text: str) -> str | None:
    """`text` planted on the line after build_view's one range write, same indent."""
    want = f'assets[-1]["{RANGE_KEY}"] = {RANGE_PRODUCER}(h4)'
    lines = src.split("\n")
    at = [i for i, ln in enumerate(lines) if ln.strip() == want]
    if len(at) != 1:
        return None
    pad = lines[at[0]][: len(lines[at[0]]) - len(lines[at[0]].lstrip())]
    return "\n".join(lines[: at[0] + 1] + [pad + text] + lines[at[0] + 1:])


# THE THREE ROUTES THAT WALKED PAST leg (c) until 2026-09-21. Each plants OR-1 STEP D's
# OWN forbidden sentence — "it is 0.4 ATR from the top, so damp the heat" — right after
# build_view's `heat = ...` line, reaching the range machine without ever spelling
# `range`, the alias, or one of the five helper names. Measured before the widening
# above: all three were GREEN on leg (c) AND on leg (d), while heat moved on 2 of the 18
# roster symbols, the Board's sort order moved, the tape's row order moved and the D-7
# calibration's heat column moved. Leg (d) cannot see them because its EMPTY/HOT stubs
# replace range_layer, and a route that calls the machine directly cancels out of the
# three-way comparison — see the residual disclosed at the head of this block.
RANGE_HEAT_LINE = '        heat = (nearest["score"] / (1.0 + nearest_d)) if nearest else 0.0\n'
RANGE_IMPORT_ANCHOR = "import tierc3_rules as V3                             # noqa: E402\n"
RANGE_DAMP_GATE = (
    "        _v = {getter}\n"
    '        _z = [r for r in _v["macro"]["ranges"] if r.state == "CONFIRMED"]\n'
    "        if _z:\n"
    '            _a = float(h4["high"].sub(h4["low"]).tail(14).mean()) or 1.0\n'
    "            _e = min(abs(st.close - _z[-1].top), abs(st.close - _z[-1].bottom)) / _a\n"
    "            if _e < 1.0:\n"
    "                heat *= 0.5\n")


def _range_plant_bypass(src: str, imp: str | None, getter: str) -> str | None:
    """The heat-damping gate above, reaching the machine through `getter`, with `imp`
    (if any) planted beside oracle_daily's other imports. None if an anchor moved or
    the result will not compile: a plant that cannot be planted voids its own leg
    loudly rather than passing quietly."""
    if src.count(RANGE_HEAT_LINE) != 1 or (imp and src.count(RANGE_IMPORT_ANCHOR) != 1):
        return None
    out = src.replace(RANGE_HEAT_LINE,
                      RANGE_HEAT_LINE + RANGE_DAMP_GATE.format(getter=getter), 1)
    if imp:
        out = out.replace(RANGE_IMPORT_ANCHOR, RANGE_IMPORT_ANCHOR + imp + "\n", 1)
    try:
        compile(out, "<f-br-14 bypass plant>", "exec")
    except SyntaxError:
        return None
    return out


def _range_mutant(src: str):
    """oracle_daily.py's SOURCE — edited, or as it is — run as a throwaway module. It is
    never put in sys.modules. Leg (d) builds one PER RUN and calls its run() with every
    directory run() writes redirected into a throwaway one (_range_behaviour); the
    containment leg calls only range_layer."""
    import types
    mod = types.ModuleType("oracle_daily_f_br_14_mutant")
    mod.__file__ = str(ROOT / "scripts" / "oracle_daily.py")
    exec(compile(src, mod.__file__, "exec"), mod.__dict__)
    return mod


def _range_stub_empty(h4) -> dict:
    return OD.range_empty(state="NEUTRAL")


def _range_stub_hot(h4) -> dict:
    """Every symbol pinned ON its macro top with a breach pending, distance 0.0 ATR."""
    c = float(h4["close"].to_numpy("float64")[-1])
    ts = "1970-01-01T00:00"
    s = OD.range_empty(state="NEUTRAL")
    s.update(has_range=True, top=c, bottom=0.9 * c, top0=c, bottom0=0.9 * c, mid=0.95 * c,
             pos_pct=100.0, atr=0.01 * c, dist_atr=0.0, nearest_side="top",
             pending={"side": "top", "open_ts": ts, "bars_out": 1, "closes": 1},
             n_pending_open=1, last_event={"event": "breach-open", "ts": ts, "age_bars": 1},
             status_line="F-BR-14 HOT STUB", as_of=ts, close=c, n_bars=int(len(h4)))
    return s


def _range_watch_inverted(view: dict) -> list[dict]:
    """oracle_daily.range_watch with its one comparison flipped, `d >= lim` — the
    review's M3. Written out rather than mutated into a module so the WATCH plant
    costs nothing: it is judged on membership alone."""
    lim = OD.REGISTER["RANGE_WATCH_ATR"]["value"]
    out = []
    for a in view["assets"]:
        r = a.get("range") or OD.range_empty(error=OD.RANGE_ABSENT)
        d, p = r.get("dist_atr"), r.get("pending")
        near = d is not None and d >= lim                  # <-- the plant
        if near or p:
            out.append({"symbol": a["symbol"], "dist_atr": d, "near": near,
                        "nearest_side": r.get("nearest_side"),
                        "pos_pct": r.get("pos_pct"), "pending": p})
    out.sort(key=lambda w: (w["dist_atr"] is None,
                            w["dist_atr"] if w["dist_atr"] is not None else 0.0,
                            w["symbol"]))
    return out


RANGE_DECISION_FIELDS = ("heat", "station", "card", "lis", "nearest", "nearest_d",
                         "clusters", "n_levels", "atr_d", "price", "payload_sha",
                         "vwap_maturity")


# LEG (d)'S SIDE CHANNEL. A finding about the render itself cannot travel in the
# comparison dict: _range_behaviour reports only keys whose VALUE DIFFERS between the
# REAL run and a stubbed one, and a reader that mutates the view mutates it identically
# in all three runs, so the key would carry the same value three times and be dropped
# in silence (measured: an out["__MUTATED__"] version misses the plant). Same for the
# value legs — a wrong number is wrong in all three. These go straight to `bad`.
# _range_behaviour CLEARS this at entry, so a stale finding cannot carry over.
_RANGE_SIDE: list[str] = []

# ── THE NUMBERS THEMSELVES (review repair, 2026-09-21) ────────────────────────────
# Until this leg existed, every value assertion in this fixture was DIFFERENTIAL: REAL
# vs EMPTY vs HOT must not move the decision side, which any garbage satisfies as long
# as it does not gate. Measured in a mirror of the repo: snapshot() returning the box
# upside down with every distance 10x too large passed the suite 16/16 GREEN while 6 of
# 18 symbols printed top < bottom, pos_pct None where the truth was 67.7 and 123.3, and
# dist_atr ten times too large; so did range_watch()'s comparison inverted (`d >= lim`)
# with write_tape's range_top/range_bottom swapped — EDGE WATCH then flagged the five
# FARTHEST symbols and dropped the one symbol 0.414 ATR from a boundary, and the
# archival parquet recorded range_top < range_bottom on every row.
#
# WHAT THESE THREE LEGS ARE, stated so nobody reads more into a green than is there:
# SELF-CONSISTENCY. Every identity is recomputed from the snapshot's OWN reported close
# and atr — the two numbers it cannot check against itself. A wrong atr, a wrong close
# or a tape loaded as-of the wrong bar is INVISIBLE here. The identities are the ones
# the machine's snapshot() docstring pins (rangefinder_core, the Oracle's copy since
# A-OR1-1; word for word the engine file's), quoted: mid = (top+bottom)/2;
# pos_pct = 100*(close-bottom)/(top-bottom), NOT clamped; dist_atr = min(|top-close|,
# |close-bottom|)/atr, None when atr is not a positive finite number; nearest_side is
# whichever boundary that min() picked, "top" on an exact tie.
RANGE_VALUE_EPS = 1e-9          # the box identities are exact arithmetic
RANGE_VALUE_REL = 1e-9          # the derived ones are a division apart
# sibling-tape column -> the snapshot field write_range_tape copies into it (A-OR1-1 v;
# the same eight names the D-4 tape carried from OR-1 STEP D2 until 2026-09-22)
RANGE_TAPE_FIELDS = {
    "range_state": lambda r: r.get("state"),
    "range_top": lambda r: r.get("top"),
    "range_bottom": lambda r: r.get("bottom"),
    "range_pos_pct": lambda r: r.get("pos_pct"),
    "range_dist_atr": lambda r: r.get("dist_atr"),
    "range_pending_side": lambda r: (r.get("pending") or {}).get("side"),
    "range_last_event": lambda r: (r.get("last_event") or {}).get("event"),
    "range_last_event_age_bars": lambda r: (r.get("last_event") or {}).get("age_bars"),
}


def _rv_none(x):
    """NaN / pd.NA / None, all one thing: the parquet carries a missing float as NaN
    and a missing string as pd.NA, and the snapshot carries both as None."""
    if x is None:
        return None
    try:
        return None if bool(pd.isna(x)) else x
    except (TypeError, ValueError):
        return x


def _rv_same(got, want) -> bool:
    got, want = _rv_none(got), _rv_none(want)
    if got is None or want is None:
        return got is want
    if isinstance(got, (int, float)) and isinstance(want, (int, float)):
        return abs(float(got) - float(want)) <= max(RANGE_VALUE_EPS,
                                                    RANGE_VALUE_REL * abs(float(want)))
    return str(got) == str(want)


def _range_values(assets: list[dict], tape=None) -> list[str]:
    """SELF-CONSISTENCY of every printed range, and the SIBLING tape's record of it
    FIELD FOR FIELD (the tape half of F-BR-14 once checked the eight columns by NAME
    only). `tape` is the sibling tape (A-OR1-1 v: one row per roster symbol) — the D-4
    tape carries no range. `assets` is view["assets"]-shaped, so the break leg can
    hand it a corrupt dict by hand."""
    bad: list[str] = []
    for a in assets:
        sym = a["symbol"]
        r = a.get("range") or {}
        if not r.get("has_range"):
            continue
        top, bot, mid = r.get("top"), r.get("bottom"), r.get("mid")
        close, atr, pos, dist = (r.get("close"), r.get("atr"), r.get("pos_pct"),
                                 r.get("dist_atr"))
        if None in (top, bot, mid, close):
            bad.append(f"{sym}: the range values are not self-consistent — has_range is True "
                       f"but the box is incomplete (top={top!r} bottom={bot!r} mid={mid!r} "
                       f"close={close!r})")
            continue
        if not bot < top:
            bad.append(f"{sym}: the range values are not self-consistent — the box is upside "
                       f"down or flat: top {top!r} is not above bottom {bot!r}")
            continue
        if abs(mid - (top + bot) / 2.0) > RANGE_VALUE_EPS * max(1.0, abs(top)):
            bad.append(f"{sym}: the range values are not self-consistent — mid reads {mid!r}, "
                       f"(top + bottom) / 2 is {(top + bot) / 2.0!r}")
        want_pos = 100.0 * (close - bot) / (top - bot)
        if not _rv_same(pos, want_pos):
            bad.append(f"{sym}: the range values are not self-consistent — pos_pct reads "
                       f"{pos!r}, 100 * (close {close!r} - bottom {bot!r}) / (top - bottom) "
                       f"is {want_pos!r}")
        d_top, d_bot = abs(top - close), abs(close - bot)
        side = "top" if d_top <= d_bot else "bottom"      # an exact tie reads 'top'
        if r.get("nearest_side") != side:
            bad.append(f"{sym}: the range values are not self-consistent — nearest_side reads "
                       f"{r.get('nearest_side')!r}; min(|top - close| {d_top!r}, |close - "
                       f"bottom| {d_bot!r}) picked {side!r}")
        usable = (isinstance(atr, (int, float)) and not isinstance(atr, bool)
                  and np.isfinite(atr) and atr > 0)
        if usable and not _rv_same(dist, min(d_top, d_bot) / atr):
            bad.append(f"{sym}: the range values are not self-consistent — dist_atr reads "
                       f"{dist!r}, min(|top - close|, |close - bottom|) / atr {atr!r} is "
                       f"{min(d_top, d_bot) / atr!r}")
        if not usable and dist is not None:
            bad.append(f"{sym}: the range values are not self-consistent — dist_atr reads "
                       f"{dist!r} on atr {atr!r}, which is no positive finite number; the "
                       f"snapshot pins that case to None")
    if tape is None:
        return bad
    ranges = {a["symbol"]: (a.get("range") or {}) for a in assets}
    for row in tape.to_dict("records"):
        r = ranges.get(row.get("asset"))
        if r is None:
            bad.append(f"the tape does not record the view: it carries a row for "
                       f"{row.get('asset')!r}, which is not in the view")
            continue
        for col, read in RANGE_TAPE_FIELDS.items():
            if not _rv_same(row.get(col), read(r)):
                bad.append(f"{row.get('asset')}: the tape does not record the snapshot — "
                           f"{col} reads {row.get(col)!r}, the printed range says "
                           f"{read(r)!r}")
        t, b = _rv_none(row.get("range_top")), _rv_none(row.get("range_bottom"))
        if t is not None and b is not None and not t > b:
            bad.append(f"{row.get('asset')}: the tape does not record a box — range_top "
                       f"{t!r} is not above range_bottom {b!r}")
    return bad


def _range_watch_membership(fn=None) -> list[str]:
    """range_watch() AT THE LIMIT, driven synthetically. Live data straddles
    REGISTER['RANGE_WATCH_ATR'] today (0.414 in, 0.571 out) but the BOUNDARY itself is
    what a flipped comparison moves, so it is pinned here: limit-eps, the limit exactly
    (`<=`, so it is IN), limit+eps (out), far out (out), and a pending breach whose
    distance cannot be measured — on the list by its breach, sorted LAST."""
    fn = OD.range_watch if fn is None else fn
    lim = OD.REGISTER["RANGE_WATCH_ATR"]["value"]
    eps = lim * 1e-6

    def a(sym, d, pending=None):
        r = OD.range_empty(state="NEUTRAL")
        r.update(has_range=d is not None, dist_atr=d, nearest_side="top", pos_pct=50.0,
                 pending=pending)
        return {"symbol": sym, "range": r}

    # names no contract has, and no <X>USDT string: F-BR-16 hunts second symbol lists
    view = {"assets": [a("IN", lim - eps), a("ON", lim), a("OUT", lim + eps),
                       a("FAR", 10.0 * lim),
                       a("PEND", None, {"side": "top", "open_ts": "1970-01-01T00:00",
                                        "bars_out": 1, "closes": 1})]}
    got = fn(view)
    on = [w["symbol"] for w in got]
    near = sorted(w["symbol"] for w in got if w["near"])
    bad = []
    if near != ["IN", "ON"]:
        bad.append(f"EDGE WATCH membership at RANGE_WATCH_ATR = {lim}: 'near' reads {near}, "
                   f"want ['IN', 'ON'] — the rule is distance <= the limit, the limit "
                   f"itself included, and nothing beyond it")
    if on != ["IN", "ON", "PEND"]:
        bad.append(f"EDGE WATCH membership at RANGE_WATCH_ATR = {lim}: the list reads {on}, "
                   f"want ['IN', 'ON', 'PEND'] — near rows by distance, then a pending "
                   f"breach with no measurable distance, last")
    return bad


def _range_corrupt() -> list[dict]:
    """The review's own mutation, by hand, on a box built to be self-consistent first:
    the machine's snapshot() `top, bottom = float(r.top), float(r.bottom)` swapped,
    dist_atr x10 and pos_pct blanked. No module is mutated, no tape is written and no
    frame is loaded — the legs are fed the SHAPE a corrupt snapshot would have."""
    good = OD.range_empty(state="NEUTRAL")
    good.update(has_range=True, top=120.0, bottom=100.0, top0=120.0, bottom0=100.0,
                mid=110.0, close=113.0, atr=4.0, pos_pct=65.0, dist_atr=1.75,
                nearest_side="top", status_line="F-BR-14 VALUE PLANT",
                as_of="1970-01-01T00:00", n_bars=1700)
    return [{"symbol": "AAA",                      # no <X>USDT string: F-BR-16 hunts those
             "range": dict(good, top=100.0, bottom=120.0, pos_pct=None, dist_atr=17.5,
                           nearest_side="bottom")}]


def _range_tape_swapped() -> tuple[list[dict], "pd.DataFrame"]:
    """write_range_tape's `range_top`/`range_bottom` swapped, over a self-consistent
    box: the view prints one thing and the archival sibling parquet records another."""
    good = _range_corrupt()[0]["range"]
    ok = dict(good, top=120.0, bottom=100.0, pos_pct=65.0, dist_atr=1.75,
              nearest_side="top")
    assets = [{"symbol": "AAA", "range": ok}]
    row = {"asset": "AAA", **{c: f(ok) for c, f in RANGE_TAPE_FIELDS.items()}}
    row["range_top"], row["range_bottom"] = row["range_bottom"], row["range_top"]
    return assets, pd.DataFrame([row])


def _range_decision_side(mod, res: dict, values: bool = False) -> tuple[dict[str, str], dict]:
    """Everything a gate COULD have moved, as repr() text keyed so a difference names
    itself (repr makes NaN equal NaN), read off what oracle_daily.run() RETURNED and
    FILED into its throwaway directories: the view, the page, the D-4 tape, the sibling
    tape and the D-7 document, each read back from disk — what is compared is what was
    filed. Returns (the comparison dict, the files as written: the D-4 tape and the
    sibling tape as frames, with their parquet schemas) — the second for legs (f), (g).
    Until the round-1 review (2026-09-22) this function RE-IMPLEMENTED run()'s order —
    render, D-4 tape, sibling tape, D-7 — and never ran run() itself, so a gate planted
    in run() between the tapes and the D-7 record (OD-10) moved the filed heat unseen."""
    view = res["view"]
    out = {"the Board's sort order": repr([a["symbol"] for a in view["assets"]]),
           "as_of_ms": repr(view["as_of_ms"]), "card_toll_atr": repr(view["card_toll_atr"]),
           "fired events": repr(view["fired"]), "R1 block": mod.r1_block(view)}
    for a in view["assets"]:
        for k in RANGE_DECISION_FIELDS:
            out[f"{a['symbol']}.{k}"] = repr(a[k])
    page = Path(res["html"]).read_text(encoding="utf-8")
    tape = pd.read_parquet(res["tape"])
    tape_schema = pq.read_schema(res["tape"])
    out["the tape's parquet schema"] = str(tape_schema)
    rtape = pd.read_parquet(res["tape_ranges"])
    rtape_schema = pq.read_schema(res["tape_ranges"])
    doc = json.loads(Path(res["calibration"]).read_text())
    if values:
        _RANGE_SIDE.extend(_range_values(view["assets"], rtape))
    doc.pop("generated_utc", None)                 # the one wall-clock field
    out["the D-7 document"] = json.dumps(doc, sort_keys=True)
    out["D-7 keys carrying the token `range`"] = repr(sorted(
        k for k in set(_keys_deep(doc)) if RANGE_KEY in re.split(r"[^a-z0-9]+", k.lower())))
    # THE D-4 TAPE, WHOLE: since A-OR1-1 it carries no range column, so every column of
    # it is decision-side and must not move with the layer (leg f checks its NAMES).
    out["the D-4 tape, every column"] = tape.to_csv(index=False)
    rcols = [c for c in rtape.columns if c.startswith("range_")]
    out["__range_columns__"] = rtape[rcols].to_csv(index=False)      # MUST differ
    out["__sibling_schema__"] = str(rtape_schema)                     # MUST NOT differ
    # THE PAGE, because render_html is on the allow-list and a reader can misbehave
    # too (a Board re-sorted by distance inside the render would move no field
    # above). Every section but the Tide Tables, up to the footer; the Board with
    # its RANGE cells cut out. What is left may not know a range exists. The page run()
    # wrote, rendered once, in run()'s order — rendering again here would reverse a
    # reverse and the mutation guard would read clean.
    for part in re.split(r"<h2>", page.split("<footer>")[0])[1:]:
        title = part.split("</h2>")[0]
        if title.lower().startswith(SEC_TIDE.lower()):
            continue
        if title.lower().startswith(SEC_BOARD.lower()):    # 'The Board' until OR-1 STEP F
            part, n_cells = re.subn(r"<td class='rng'>.*?</td>", "", part, flags=re.S)
            out["__range_cells__"] = str(n_cells)
        out[f"the rendered section '{title[:40]}'"] = part
    return out, {"tape": tape, "tape_schema": tape_schema,
                 "sibling": rtape, "sibling_schema": rtape_schema}


def _range_seed(d: Path, name: str, roster, lens: str) -> None:
    """Each run's SIBLING DIRECTORY, seeded before run() starts with a DIFFERENT
    'yesterday' (RANGE_SEED_FILE, the real writer's column list and dtypes): REAL
    nothing; EMPTY an all-None day; HOT every symbol ON a boundary, breach pending. A gate
    that reads the sibling tape off disk, by ANY path derived from the lane's directories
    (TAPE_DIR.parent / ('tape' + '_ranges') included: the throwaway tree mirrors the
    repo's), then reads a different thing in each run and the decision side moves. Until
    the round-1 review build_view ran against the LIVE directory in all three runs and a
    disk read cancelled out."""
    if name == "REAL":
        return
    hot = name == "HOT"
    rows = [{"as_of_ms": 946_684_800_000, "as_of_iso": "2000-01-01T00:00:00+00:00",
             "asset": sym, "lens": lens,
             "range_state": "CONFIRMED" if hot else "NEUTRAL",
             "range_top": 1.0 if hot else None, "range_bottom": 0.9 if hot else None,
             "range_pos_pct": 100.0 if hot else None,
             "range_dist_atr": 0.0 if hot else None,
             "range_pending_side": "top" if hot else None,
             "range_last_event": "breach-open" if hot else None,
             "range_last_event_age_bars": 1.0 if hot else None} for sym in roster]
    df = pd.DataFrame(rows, columns=list(RANGE_SIBLING_TYPES)).astype(
        {c: {"double": "float64", "string": "string", "int64": "int64"}[t]
         for c, t in RANGE_SIBLING_TYPES.items()})
    d.mkdir(parents=True, exist_ok=True)
    df.to_parquet(d / RANGE_SEED_FILE, index=False)


def _range_guard(mod) -> None:
    """Every allow-listed reader run() hands the view to (RANGE_VIEW_READERS) is wrapped
    in the fresh module: repr(view) before and after, a difference to the side channel.
    run() writes both tapes and the D-7 record AFTER the render, so an in-place re-order
    by a reader — identical in all three runs, invisible to the comparison — would be
    filed re-ordered."""
    for fname in RANGE_VIEW_READERS:
        real = getattr(mod, fname)

        def guarded(view, *a, _real=real, _name=fname, **k):
            before = repr(view)                    # not a deepcopy: repr is the test
            got = _real(view, *a, **k)
            if repr(view) != before:
                _RANGE_SIDE.append(
                    f"an allow-listed reader MUTATED the view during {_name}() — the symbol "
                    f"order went {_range_order(before)} -> "
                    f"{[x['symbol'] for x in view['assets']]}; run() files the tapes and the "
                    f"D-7 record after it, so all three would be filed re-ordered")
            return got

        setattr(mod, fname, guarded)


def _range_freeze(mod, instant) -> None:
    """The fresh module's clock, frozen at ONE instant for all three runs (the F-BR-15
    idiom): the edition date, the payload's 'generated' day and the LATE EDITION band
    are wall-clock reads, and three runs straddling a midnight or A2-7's limit would
    differ for a reason that has nothing to do with a range."""
    real = mod.datetime

    class _Frozen(real):
        @classmethod
        def now(cls, tz=None):
            return (instant.astimezone(tz) if tz is not None
                    else instant.astimezone().replace(tzinfo=None))

    mod.datetime = _Frozen


def _range_order(r: str) -> list[str]:
    """The symbol order inside a repr() of the view, for the mutation guard's message."""
    return re.findall(r"'symbol': '([^']+)'", r)


# ── LEG (d)'S TRIPWIRES (round-2 review, 2026-09-22) ───────────────────────────────
# The EMPTY/HOT stubs replace range_layer, so a gate that runs the machine by ANOTHER
# route, or reads the sibling tape by a path no name reaches, does the same thing in all
# three runs and cancels out of the comparison: the review's OD-A moved heat on 2 of 18
# symbols with every leg green, OD-G flipped the filed D-7 target-bucket basis, OD-F
# read the live directory through the grid's path. So every run is WATCHED, and a trip
# is a finding on its own, whatever the comparison says.
#   THE MACHINE TRIPWIRE. sys.monitoring, PY_START: every code object that is not one of
#   the two machine files is DISABLEd on its first call (so the watch costs next to
#   nothing); a machine frame whose caller is outside the machine is an ENTRY, judged by
#   its caller — in REAL it must be the run's own range_layer(), in EMPTY and HOT
#   (range_layer stubbed) there may be none at all. A callback from pandas back into the
#   machine is judged at its outermost machine frame, never twice.
#   THE READ TRIPWIRE. pandas' and pyarrow's parquet readers (RANGE_READ_FUNCS) wrapped
#   for the run, and an audit hook on open, os.listdir, os.scandir, glob.glob and
#   shutil.copyfile. Red: any path under the LIVE sibling directory (a read, a listing,
#   a write); any listing of the run's own sibling directory; any read of an
#   oracle_tape_ranges_* file but write_range_tape()'s read-back of the one it has just
#   written. Paths are compared after realpath(), where the read happens, so no spelling
#   and no side of the wall matters.
# Both hooks are claimed ONCE per process (an audit hook cannot be removed) and are idle
# whenever _RANGE_WATCH is None. Each must show its proof of life in REAL — range_layer's
# own entries; the writer's read-back — or the leg reports it unarmed.
_RANGE_WATCH: dict | None = None
_RANGE_HOOKS: dict = {"tool": None, "audit": False, "machines": frozenset()}
_RANGE_REALFILE: dict[str, str] = {}


def _range_realpath(p) -> str | None:
    """realpath of a str / bytes / PathLike; None for a descriptor or a buffer."""
    if p is None or isinstance(p, (int, bool)):
        return None
    try:
        s = os.fspath(p)
    except TypeError:
        return None
    return os.path.realpath(os.fsdecode(s) if isinstance(s, bytes) else s)


def _range_is_under(p: str, base: str) -> bool:
    return p == base or p.startswith(base.rstrip(os.sep) + os.sep)


def _range_code_file(code) -> str:
    f = code.co_filename
    r = _RANGE_REALFILE.get(f)
    if r is None:
        r = _RANGE_REALFILE[f] = f if f.startswith("<") else os.path.realpath(f)
    return r


def _range_where(frame) -> str:
    if frame is None:
        return "<no caller>"
    f = _range_code_file(frame.f_code)
    if _range_is_under(f, str(ROOT)):
        f = os.path.relpath(f, ROOT)
    return f"{f}:{frame.f_code.co_name}() line {frame.f_lineno}"


def _range_trip(w: dict, msg: str) -> None:
    if msg not in w["trips"]:
        w["trips"].append(msg)


def _range_on_start(code, offset):
    """sys.monitoring PY_START callback — the MACHINE TRIPWIRE. Never raises."""
    try:
        machines = _RANGE_HOOKS["machines"]
        if _range_code_file(code) not in machines:
            return sys.monitoring.DISABLE
        w = _RANGE_WATCH
        if w is None:
            return None
        f = sys._getframe(1)                       # the machine frame that just started
        b = f.f_back
        if b is not None and _range_code_file(b.f_code) in machines:
            return None                            # a call inside the machine
        outer, g = f, b
        while g is not None:                       # a callback from outside, into it:
            if _range_code_file(g.f_code) in machines:     # judged at the outermost entry
                outer = g
            g = g.f_back
        if outer is not f:
            return None
        w["entries"] += 1
        if w["allowed"] is not None and b is not None and b.f_code is w["allowed"]:
            w["sanctioned"] += 1
            return None
        _range_trip(w, f"MACHINE TRIPWIRE ({w['run']} run): the range machine "
                       f"({os.path.basename(_range_code_file(code))}:{code.co_name}) was entered "
                       f"from {_range_where(b)} — "
                       + ("only the run's own range_layer() may run it"
                          if w["allowed"] is not None else
                          "range_layer() is stubbed in this run, so nothing may run it"))
    except Exception:
        pass
    return None


def _range_on_stack(code) -> bool:
    f = sys._getframe(1)
    while f is not None:
        if f.f_code is code:
            return True
        f = f.f_back
    return False


def _range_asker():
    """The nearest frame in a repo file other than this one: who asked for the read."""
    me = os.path.realpath(__file__)
    f = sys._getframe(2)
    while f is not None:
        cf = _range_code_file(f.f_code)
        if cf != me and _range_is_under(cf, str(ROOT)):
            return f
        f = f.f_back
    return None


def _range_seen(label: str, src, kind: str) -> None:
    """One path the run touched. kind: 'read' (a wrapped reader), 'open' (a read by
    open()), 'list', or 'write'. Never raises."""
    w = _RANGE_WATCH
    if w is None or w["busy"]:
        return
    w["busy"] = True
    try:
        for s in (list(src) if isinstance(src, (list, tuple)) else [src]):
            p = _range_realpath(s)
            if p is None:
                continue
            w["watched"] += 1
            why = None
            if _range_is_under(p, w["live"]):
                why = ("the LIVE sibling directory — a run in this leg reads and writes only "
                       "its throwaway tree, and a live read would be the same bytes in all three "
                       "runs, invisible to the comparison")
            elif kind == "list":
                if _range_is_under(p, w["boxsib"]):
                    why = "a listing of the run's own sibling directory — no function lists it"
            elif kind != "write" and (_range_is_under(p, w["boxsib"])
                                      or os.path.basename(p).startswith(RANGE_SIBLING_PREFIX)):
                if kind == "open" and p == w["expected"] and _range_on_stack(w["writer"]):
                    w["readback"] += 1
                else:
                    why = ("a read of the sibling tape — only write_range_tape() reads one: the "
                           "file it has just written, to hash it")
            if why:
                where = os.path.relpath(p, w["box"]) if _range_is_under(p, w["box"]) else p
                _range_trip(w, f"READ TRIPWIRE ({w['run']} run): {label}('{where}') from "
                               f"{_range_where(_range_asker())} — {why}")
    except Exception:
        pass
    finally:
        w["busy"] = False


def _range_audit(event: str, args) -> None:
    """sys.addaudithook — the READ TRIPWIRE's view of open / listdir / scandir / glob /
    copyfile. Idle (one global read) whenever no run is watched. Never raises."""
    if _RANGE_WATCH is None:
        return
    try:
        if event == "open":
            mode = args[1] if len(args) > 1 else None
            flags = args[2] if len(args) > 2 else 0
            write = ((isinstance(mode, str) and "+" not in mode
                      and any(c in mode for c in "wax"))
                     or (mode is None and isinstance(flags, int)
                         and flags & os.O_ACCMODE == os.O_WRONLY))
            _range_seen("open", args[0], "write" if write else "open")
        elif event in RANGE_AUDIT_LISTS:
            path = args[0]
            if event == "glob.glob/2" and len(args) > 2 and args[2] is not None:
                path = os.path.join(os.fsdecode(os.fspath(args[2])), os.fsdecode(os.fspath(path)))
            _range_seen(event, path, "list")
        elif event == "shutil.copyfile":
            _range_seen(event, args[0], "read")
    except Exception:
        pass


def _range_read_wrap(orig, label: str):
    """`orig` (a reader function or class) wrapped so that its path is judged first."""
    def first(a, k):
        if a:
            return a[0]
        return next((k[x] for x in ("path", "source", "path_or_paths", "where") if x in k), None)

    if isinstance(orig, type):
        class Watched(orig):                       # a subclass: isinstance() still holds
            def __init__(self, *a, **k):
                _range_seen(label, first(a, k), "read")
                super().__init__(*a, **k)
        Watched.__name__, Watched.__qualname__ = orig.__name__, orig.__qualname__
        Watched.__module__ = orig.__module__
        return Watched

    @functools.wraps(orig)
    def watched(*a, **k):
        _range_seen(label, first(a, k), "read")
        return orig(*a, **k)
    return watched


def _range_hooks() -> None:
    """Claim the sys.monitoring tool id and install the audit hook, once per process."""
    if _RANGE_HOOKS["tool"] is None:
        mon = sys.monitoring
        tid = next((i for i in (4, 3, 5, 2, 1, 0) if mon.get_tool(i) is None), None)
        if tid is None:
            raise RuntimeError("no free sys.monitoring tool id — the machine tripwire cannot "
                               "be armed")
        _RANGE_HOOKS["machines"] = frozenset(os.path.realpath(p) for p in _range_machine_files())
        mon.use_tool_id(tid, "F-BR-14 machine tripwire")
        mon.register_callback(tid, mon.events.PY_START, _range_on_start)
        _RANGE_HOOKS["tool"] = tid
    if not _RANGE_HOOKS["audit"]:
        sys.addaudithook(_range_audit)
        _RANGE_HOOKS["audit"] = True


def _range_watch_new(name: str, box: Path) -> dict:
    return {"run": name, "box": str(box),
            "live": os.path.realpath(RANGE_LIVE_SIBLING),
            "boxsib": os.path.realpath(box / RANGE_LIVE_SIBLING.relative_to(ROOT)),
            "expected": None, "writer": None, "allowed": None,
            "entries": 0, "sanctioned": 0, "watched": 0, "readback": 0,
            "trips": [], "busy": False}


@contextlib.contextmanager
def _range_watching(w: dict):
    """Both tripwires armed for the length of the block, on the run `w` describes."""
    global _RANGE_WATCH
    _range_hooks()
    patched = []
    try:
        for modname, attr in RANGE_READ_FUNCS:
            m = importlib.import_module(modname)
            orig = getattr(m, attr, None)
            if orig is not None:
                setattr(m, attr, _range_read_wrap(orig, f"{modname}.{attr}"))
                patched.append((m, attr, orig))
        _RANGE_WATCH = w
        sys.monitoring.set_events(_RANGE_HOOKS["tool"], sys.monitoring.events.PY_START)
        yield w
    finally:
        sys.monitoring.set_events(_RANGE_HOOKS["tool"], 0)
        _RANGE_WATCH = None
        for m, attr, orig in reversed(patched):
            setattr(m, attr, orig)


def _range_behaviour(src: str | None = None, n_roster: int | None = None) -> tuple[list[str], dict]:
    """Leg (d). `src` is oracle_daily.py's source, or a planted copy of it for the break
    leg. Each of the three runs is oracle_daily.run() ITSELF, in a FRESH module built
    from `src` (_range_mutant), EMPTY and HOT first and REAL last (RANGE_RUN_ORDER),
    every directory run() writes redirected into a throwaway tree that mirrors the
    repo's and is seeded per run (_range_seed), the canon written there too, the
    module's clock frozen at one instant for all three. Since the round-2 review the
    roots run() READS from (RANGE_RUN_READS) are copied into the same tree, and each
    run — the module's build included — is WATCHED by both tripwires (_range_watching)."""
    from datetime import datetime, timezone
    src = (ROOT / "scripts" / "oracle_daily.py").read_text(encoding="utf-8") if src is None else src
    quiet = lambda *a, **k: None                   # noqa: E731
    instant = datetime.now(timezone.utc)
    stubs = {"REAL": None, "EMPTY": _range_stub_empty, "HOT": _range_stub_hot}
    sides, views, files, watch = {}, {}, {}, {}
    real_canon = PE.write_canon_json
    _RANGE_SIDE.clear()
    try:
        for name in RANGE_RUN_ORDER:
            with tempfile.TemporaryDirectory(prefix=f"f-br-14-{name.lower()}-") as td:
                box = Path(td).resolve()
                w = watch[name] = _range_watch_new(name, box)
                with _range_watching(w):
                    mod = _range_mutant(src)
                    if n_roster:                   # a slice, never a list
                        mod.REGISTER["ROSTER"]["value"] = tuple(
                            mod.REGISTER["ROSTER"]["value"][:n_roster])
                    w["writer"] = mod.write_range_tape.__code__      # before the guard wraps it
                    if stubs[name] is not None:
                        mod.range_layer = stubs[name]              # no entry allowed at all
                    else:
                        w["allowed"] = mod.range_layer.__code__
                    _range_freeze(mod, instant)
                    _range_guard(mod)
                    for d in RANGE_RUN_DIRS:
                        setattr(mod, d, box / Path(getattr(mod, d)).resolve().relative_to(ROOT))
                    for d in RANGE_RUN_READS:      # COPIED in, then pointed at
                        live = Path(getattr(mod, d)).resolve()
                        dst = box / live.relative_to(ROOT)
                        if live.is_dir():
                            shutil.copytree(live, dst)
                        elif live.is_file():
                            dst.parent.mkdir(parents=True, exist_ok=True)
                            shutil.copy2(live, dst)
                        setattr(mod, d, dst)
                    date = mod.datetime.now(tz=None).astimezone().strftime("%Y-%m-%d")
                    w["expected"] = os.path.realpath(
                        Path(mod.TAPE_RANGES_DIR) / f"{RANGE_SIBLING_PREFIX}{date}.parquet")
                    PE.write_canon_json = (lambda path=None, _b=box: real_canon(
                        _b / "research_outputs" / "oracle" / "posture_canon.json"))
                    _range_seed(mod.TAPE_RANGES_DIR, name, mod.REGISTER["ROSTER"]["value"],
                                mod.REGISTER["LENS"]["value"])
                    res = mod.run(slot="fixture", log=quiet)
                _RANGE_SIDE.extend(w["trips"])
                views[name] = res["view"]
                sides[name], files[name] = _range_decision_side(mod, res,
                                                                values=(name == "REAL"))
    finally:
        PE.write_canon_json = real_canon
    # the side channel FIRST: a mutation during the render, every value finding, and
    # every trip. None of them can travel in the comparison dict — see _RANGE_SIDE.
    bad: list[str] = list(dict.fromkeys(_RANGE_SIDE))   # the same mutation in all 3 runs
    _RANGE_SIDE.clear()
    # each tripwire's proof of life: in REAL, range_layer ran the machine and the writer
    # read its tape back — both seen, or the wire is not armed and proved nothing
    if not watch["REAL"]["sanctioned"]:
        bad.append("MACHINE TRIPWIRE UNARMED: it saw no entry into the range machine from "
                   "range_layer() in the REAL run — a watch that sees nothing proves nothing")
    if not watch["REAL"]["readback"]:
        bad.append("READ TRIPWIRE UNARMED: it never saw write_range_tape() read back the file "
                   "it wrote in the REAL run — a watch that sees nothing proves nothing")
    own = ("__range_columns__", "__sibling_schema__")    # judged on their own, below
    for name in ("EMPTY", "HOT"):
        moved = [k for k in sides["REAL"] if k not in own
                 and sides["REAL"][k] != sides[name].get(k)]
        moved += [k for k in sides[name] if k not in sides["REAL"]]
        if moved:
            bad.append(f"decision side moved with the range layer stubbed {name}: "
                       f"{len(moved)} field(s) differ from the REAL run, first {moved[:4]} — "
                       f"something that gates is reading a range")
    # the comparison is only worth something if the stubs REACHED build_view
    hot = [a["range"] for a in views["HOT"]["assets"]]
    if not hot or any(r.get("dist_atr") != 0.0 or not r.get("pending") for r in hot):
        bad.append("the HOT stub never reached build_view — leg (d) compared nothing")
    if any(a["range"].get("has_range") for a in views["EMPTY"]["assets"]):
        bad.append("the EMPTY stub never reached build_view — leg (d) compared nothing")
    rc = "__range_columns__"
    if sides["HOT"][rc] in (sides["REAL"][rc], sides["EMPTY"][rc]):
        bad.append("the sibling tape's range columns under the HOT stub equal another run's — "
                   "the range never reaches the sibling tape, or the stub never reached the view")
    # leg (g)'s dtype pin, across the three days the stubs make: EMPTY is the all-None
    # day, HOT the all-pending one. A schema that follows the data is the review's hazard.
    sc = "__sibling_schema__"
    drift = [n for n in ("EMPTY", "HOT") if sides[n][sc] != sides["REAL"][sc]]
    if drift:
        bad.append(f"the sibling tape's parquet schema is not the pinned one on the {drift} "
                   f"day(s) — a dtype follows the data (REAL {sides['REAL'][sc]!r} vs "
                   f"{drift[0]} {sides[drift[0]][sc]!r})")
    if sides["REAL"].get("__range_cells__") != str(len(views["REAL"]["assets"])):
        bad.append(f"the Board carries {sides['REAL'].get('__range_cells__')} RANGE cell(s) for "
                   f"{len(views['REAL']['assets'])} row(s) — the cut that lets the Board be "
                   f"compared found the wrong number of cells")
    if sides["REAL"]["D-7 keys carrying the token `range`"] != "[]":
        bad.append("range data reached the calibration JSON: "
                   + sides["REAL"]["D-7 keys carrying the token `range`"])
    real = [a["range"] for a in views["REAL"]["assets"]]
    if n_roster is None and not any(r.get("has_range") for r in real):
        bad.append("not one roster symbol carries a live macro range — the value legs "
                   "measured nothing today; fail closed")
    return bad, {"assets": len(real), "fields": len(sides["REAL"]) - 3,
                 "sections": sorted(k for k in sides["REAL"] if k.startswith("the rendered")),
                 "live": sum(1 for r in real if r.get("has_range")),
                 "pending": sum(1 for r in real if r.get("pending")),
                 "failed": sum(1 for r in real if r.get("error")),
                 "keys": sorted({k for r in real if not r.get("error") for k in r}),
                 "roster": [a["symbol"] for a in views["REAL"]["assets"]],
                 "files": files,
                 "watch": {n: {k: w[k] for k in ("entries", "sanctioned", "watched", "readback")}
                           for n, w in watch.items()}}


def _range_tape_names(cols=None) -> list[str]:
    """Every range column is a RECORDING name: it clears the banned-token matcher the
    wrapper's per-edition self-check runs over oracle_daily.RANGE_TAPE_COLS, the
    SIBLING tape's list (A-OR1-1 v; the D-4 tape's TAPE_COLS carries none)."""
    cols = list(OD.RANGE_TAPE_COLS) if cols is None else list(cols)
    new = [c for c in cols if c.startswith("range_")]
    bad = []
    for c in new:
        ok, detail = _calibration({c: 0})
        if not ok:
            bad.append(f"tape column {c!r} trips the banned vocabulary: {detail}")
    if not new:
        bad.append("RANGE_TAPE_COLS carries no range_* column — the tape half of STEP D is "
                   "missing")
    if TAPE_RANGES is not None:
        missing = [c for c in new if c not in TAPE_RANGES.columns]
        if missing:
            bad.append(f"artifact set {DATE}: the sibling tape lacks {missing} — it was not "
                       f"written by this code")
    return bad


# ── LEG (f) · THE D-4 TAPE: TC4's event tape, schema untouched (A-OR1-1 v) ──────────
def _range_main_tape(frames: dict, cols=None) -> list[str]:
    """oracle_daily.TAPE_COLS and every D-4 frame handed in carry EXACTLY the
    pre-OR-1 24 names in the pre-OR-1 order (PRE_OR1_TAPE_COLS). A frame that is None
    is an ABSENT tape, and absent is red: fail closed."""
    want = list(PRE_OR1_TAPE_COLS)
    bad = []

    def diff(got: list[str], where: str) -> None:
        if got == want:
            return
        extra = [c for c in got if c not in want]
        missing = [c for c in want if c not in got]
        bad.append(f"the D-4 tape's columns are not the pre-OR-1 24 on {where}: {len(got)} "
                   f"column(s), extra {extra[:4]}{' …' if len(extra) > 4 else ''}, missing "
                   f"{missing[:4]}" + ("" if extra or missing else ", the ORDER moved")
                   + " — the TC4 event tape's schema is untouched (A-OR1-1 v); range "
                     "records go to the sibling tape")

    diff(list(OD.TAPE_COLS if cols is None else cols), "oracle_daily.TAPE_COLS")
    for where, df in frames.items():
        if df is None:
            bad.append(f"the D-4 tape's columns are not the pre-OR-1 24 on {where}: the tape "
                       f"is ABSENT, so its schema cannot be read — fail closed")
            continue
        diff([str(c) for c in df.columns], where)
    return bad


# ── LEG (g) · THE SIBLING TAPE: the eight fields, pinned, one row per symbol ────────
def _sibling_types(schema) -> dict[str, str]:
    """A parquet schema as {column: type}, `large_string` read as `string`."""
    return {f.name: ("string" if str(f.type) in ("string", "large_string") else str(f.type))
            for f in schema}


def _range_sibling(tapes: dict, roster) -> list[str]:
    """`tapes` = {where: (frame, parquet schema)}. Each must carry RANGE_SIBLING_TYPES'
    columns in that order, each at that type (never `null`), and exactly one row per
    roster symbol. oracle_daily's own pins are held to the same typed expectation."""
    want = list(RANGE_SIBLING_TYPES)
    fields = [c for c in want if c.startswith("range_")]
    roster = sorted(roster)
    bad = []
    if list(OD.RANGE_TAPE_COLS) != want:
        bad.append(f"the sibling tape does not carry the row keys and the eight range fields: "
                   f"oracle_daily.RANGE_TAPE_COLS is {list(OD.RANGE_TAPE_COLS)}, want {want}")
    pins = {**{c: "double" for c in OD.RANGE_TAPE_FLOATS},
            **{c: "string" for c in OD.RANGE_TAPE_STRINGS}}
    if pins != {c: RANGE_SIBLING_TYPES[c] for c in fields}:
        bad.append(f"the sibling tape's dtype pins are not the pinned one: RANGE_TAPE_FLOATS + "
                   f"RANGE_TAPE_STRINGS = {pins}, want the eight fields as "
                   f"{ {c: RANGE_SIBLING_TYPES[c] for c in fields} }")
    for where, (df, schema) in tapes.items():
        if df is None or schema is None:
            bad.append(f"the sibling tape does not carry anything on {where}: it is ABSENT — "
                       f"fail closed")
            continue
        got = [str(c) for c in df.columns]
        if got != want:
            bad.append(f"the sibling tape does not carry the row keys and the eight range "
                       f"fields on {where}: missing {[c for c in want if c not in got]}, "
                       f"extra {[c for c in got if c not in want]}"
                       + ("" if set(got) != set(want) else ", the ORDER moved"))
        types = _sibling_types(schema)
        wrong = {c: types[c] for c, t in RANGE_SIBLING_TYPES.items()
                 if c in types and types[c] != t}
        if wrong:
            bad.append(f"the sibling tape's parquet type is not the pinned one on {where}: "
                       f"{wrong} (want { {c: RANGE_SIBLING_TYPES[c] for c in wrong} }) — a "
                       f"`null` column is the all-None day's hazard")
        assets = [str(x) for x in df["asset"]] if "asset" in df.columns else []
        if sorted(assets) != roster:
            dup = sorted({x for x in assets if assets.count(x) > 1})
            bad.append(f"the sibling tape is not one row per roster symbol on {where}: "
                       f"{len(assets)} row(s) for a roster of {len(roster)} — missing "
                       f"{[x for x in roster if x not in assets][:4]}, not on the roster "
                       f"{sorted(set(assets) - set(roster))[:4]}, twice {dup[:4]}")
    return bad


def _range_sibling_empty_day() -> tuple["pd.DataFrame", object]:
    """THE ALL-NONE DAY, through the REAL writer: every roster symbol carrying the EMPTY
    range (no box, no pending, no event), written by oracle_daily.write_range_tape
    into a throwaway directory and read back. No cache read, no frame, no clock."""
    from types import SimpleNamespace as NS
    lens = OD.REGISTER["LENS"]["value"]
    view = {"assets": [{"symbol": sym, "station": NS(as_of_ms=0, lens=lens),
                        "range": OD.range_empty(state="NEUTRAL")}
                       for sym in OD.REGISTER["ROSTER"]["value"]]}
    real = OD.TAPE_RANGES_DIR
    try:
        with tempfile.TemporaryDirectory(prefix="f-br-14-empty-") as td:
            OD.TAPE_RANGES_DIR = Path(td) / "tape_ranges"
            path, _sha, _b = OD.write_range_tape(view, "0000-00-00")
            return pd.read_parquet(path), pq.read_schema(path)
    finally:
        OD.TAPE_RANGES_DIR = real


def _frame_schema(df):
    """The parquet schema a frame WOULD be filed with (the writer's own route)."""
    import pyarrow as pa
    return pa.Table.from_pandas(df, preserve_index=False).schema


# ── LEG (h) · THE SIBLING WALL: no gate reads the sibling tape ──────────────────────
def _range_sibling_static(sources: dict[str, str]) -> list[str]:
    """The decision-side TEXT (leg (b)'s scan set, derived from the real closures) never
    spells the sibling tape's directory, constant, column list or writer, nor the lane's
    own directory `research_outputs/oracle` — case-blind, comments included. The last is
    the round-1 review's DEC-14/15: `Path('research_outputs/oracle') / ('tape' +
    '_ranges')` and `.rglob('*.parquet')` there spelt no sibling token at all."""
    bad = []
    for name, text in sources.items():
        m = RANGE_SIBLING_DECISION_RX.search(text)
        if m:
            line = text[text.rfind("\n", 0, m.start()) + 1: text.find("\n", m.end())].strip()
            bad.append(f"{name} names the sibling tape (`{m.group(0)}`: {line[:90]!r}) — a "
                       f"decision module may not read a range record")
    return bad


def _range_log_bound(fn) -> list[str]:
    """run()'s `log` is its PARAMETER, bound nowhere else in it (see _range_sibling_run)."""
    lg = RANGE_SIBLING_LOG
    a = fn.args
    bad = []
    if lg not in [x.arg for x in (*a.posonlyargs, *a.args, *a.kwonlyargs)]:
        bad.append(f"{fn.name}() has no parameter `{lg}` — the sink its sibling-tape report is "
                   f"handed to is not the caller's; fail closed")

    def hit(n, how):
        bad.append(f"{fn.name}() rebinds `{lg}` at line {getattr(n, 'lineno', '?')} ({how}) — the "
                   f"sanctioned {lg}(f'{{rtape_p}} ...') would hand the sibling tape's path to "
                   f"whatever `{lg}` now is")

    for n in ast.walk(fn):
        if isinstance(n, ast.Name) and n.id == lg and isinstance(n.ctx, (ast.Store, ast.Del)):
            hit(n, "a store or a delete")
        elif (isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
              and n is not fn and n.name == lg):
            hit(n, f"a nested {'class' if isinstance(n, ast.ClassDef) else 'def'}")
        elif isinstance(n, (ast.Global, ast.Nonlocal)) and lg in n.names:
            hit(n, "global / nonlocal")
        elif (isinstance(n, (ast.Import, ast.ImportFrom))
              and any((x.asname or x.name.split(".")[0]) == lg for x in n.names)):
            hit(n, "an import")
        elif isinstance(n, ast.ExceptHandler) and n.name == lg:
            hit(n, "except ... as")
        elif isinstance(n, (ast.MatchAs, ast.MatchStar)) and n.name == lg:
            hit(n, "a match capture")
        elif isinstance(n, ast.MatchMapping) and n.rest == lg:
            hit(n, "a match capture")
        elif isinstance(n, (ast.Lambda, ast.FunctionDef, ast.AsyncFunctionDef)) and n is not fn:
            x = n.args
            if lg in [p.arg for p in (*x.posonlyargs, *x.args, *x.kwonlyargs,
                                      *([x.vararg] if x.vararg else []),
                                      *([x.kwarg] if x.kwarg else []))]:
                hit(n, "a lambda / nested-function parameter")
    return bad


def _range_sibling_run(fn, hits) -> list[str]:
    """run(), since the round-1 review no longer exempt from leg (h): it CALLS
    write_range_tape() exactly once, binds what it returns to plain names, and hands
    those names to log() — as a bare argument or an f-string field — and to its return
    dict as bare values, and does nothing else with them. No other sibling name or
    string anywhere in run() but the return dict's KEYS (callers read
    res['tape_ranges']). Plant OD-10 read the written tape back just before the D-7
    record and doubled heat; OD-11 re-sorted the Board by yesterday's sibling tape.
    AND `log` MUST BE THE PARAMETER (round-2 review, OD-H): `_log0 = log; def log(*a):
    ...` just before the writer turned the sanctioned log(f'{rtape_p} ...') into a gate
    that parsed the path back out and read the tape. So `log` may not be rebound
    anywhere in run() — no Store or Del, no nested def or class of that name, no lambda
    or nested-function parameter, no import as it, no except-as, no global/nonlocal."""
    bad = _range_log_bound(fn)
    parent = {c: p for p in ast.walk(fn) for c in ast.iter_child_nodes(p)}
    calls = [n for n in ast.walk(fn) if isinstance(n, ast.Call)
             and isinstance(n.func, ast.Name) and n.func.id == RANGE_SIBLING_WRITER]
    if len(calls) != 1:
        bad.append(f"{fn.name}() calls {RANGE_SIBLING_WRITER}() {len(calls)} time(s) — exactly "
                   f"once, or the sibling tape's fence has nothing to hold; fail closed")
    ok_ids, results = set(), set()
    for c in calls:
        ok_ids.add(id(c.func))
        a = parent.get(c)
        t = a.targets[0] if isinstance(a, ast.Assign) and len(a.targets) == 1 else None
        elts = ([t] if isinstance(t, ast.Name) else list(t.elts)
                if isinstance(t, ast.Tuple) and all(isinstance(e, ast.Name) for e in t.elts)
                else None)
        if elts is None:
            bad.append(f"{fn.name}() does not bind {RANGE_SIBLING_WRITER}()'s result to plain "
                       f"names at line {c.lineno} — what it returns cannot be followed; fail closed")
            continue
        results |= {e.id for e in elts}
        ok_ids |= {id(e) for e in elts}
    rets = [n.value for n in ast.walk(fn) if isinstance(n, ast.Return)
            and isinstance(n.value, ast.Dict)]
    key_ids = {id(k) for d in rets for k in d.keys if k is not None}
    val_ids = {id(v) for d in rets for v in d.values}
    logs = [n for n in ast.walk(fn) if isinstance(n, ast.Call)
            and isinstance(n.func, ast.Name) and n.func.id == RANGE_SIBLING_LOG]
    log_ids = {id(x) for c in logs for a in (*c.args, *(k.value for k in c.keywords))
               for x in ast.walk(a)}
    for n, what in hits(fn):
        if id(n) not in ok_ids and id(n) not in key_ids:
            bad.append(f"{fn.name}() names the sibling tape: {what} at line {n.lineno} — it may "
                       f"call {RANGE_SIBLING_WRITER}() once and report what it returns, nothing "
                       f"else")
    for n in ast.walk(fn):
        if not (isinstance(n, ast.Name) and n.id in results) or id(n) in ok_ids:
            continue
        p = parent.get(n)
        logged = id(n) in log_ids and (isinstance(p, ast.FormattedValue)
                                        or (isinstance(p, ast.Call) and p in logs))
        if isinstance(n.ctx, ast.Load) and (logged or id(n) in val_ids):
            continue
        bad.append(f"{fn.name}() uses the sibling tape's `{n.id}` at line {n.lineno} outside "
                   f"log() and its return dict — {RANGE_SIBLING_WRITER}()'s result is a record "
                   f"to report, never an input")
    return bad


def _range_lane_shape(n, parent) -> str | None:
    """None if the lane-path Name `n` is used in one of the MEASURED shapes, else the
    expression it is used in: the left side of `/`; `.mkdir()` / `.exists()` /
    `.glob()` on it (RANGE_LANE_PATH_ATTRS); a positional argument of a disk reader
    (RANGE_DISK_CALLS); a call of it (cache_dir()); a {field} of an f-string that is
    an argument of the exception a `raise` raises."""
    p = parent.get(n)
    if isinstance(p, ast.BinOp) and isinstance(p.op, ast.Div) and p.left is n:
        return None
    if (isinstance(p, ast.Attribute) and p.value is n and p.attr in RANGE_LANE_PATH_ATTRS
            and isinstance(parent.get(p), ast.Call) and parent[p].func is p):
        return None
    if isinstance(p, ast.Call) and p.func is n:
        return None
    if isinstance(p, ast.Call) and n in p.args and (
            (isinstance(p.func, ast.Attribute) and p.func.attr in RANGE_DISK_CALLS)
            or (isinstance(p.func, ast.Name) and p.func.id in RANGE_DISK_CALLS)):
        return None
    if isinstance(p, ast.FormattedValue):
        js = parent.get(p)
        call = parent.get(js)
        r = parent.get(call)
        if (isinstance(js, ast.JoinedStr) and isinstance(call, ast.Call) and js in call.args
                and isinstance(r, ast.Raise) and r.exc is call):
            return None
    return ast.unparse(p)[:48] if p is not None else n.id


def _range_lane_paths(tree, docs, sources) -> list[str]:
    """oracle_daily's PATHS, fenced the way its sibling names are (round-1 review,
    2026-09-22). OD-12 `(TAPE_DIR.parent / ('tape' + '_ranges')).glob(...)` and OD-13
    `TAPE_DIR.parent.rglob('oracle_tape_r*.parquet')` in trap_card() spelt no sibling
    token and were GREEN on legs (c) and (h). So: a lane path (RANGE_LANE_PATHS) is named
    only by the functions listed for it; no code walks a path (RANGE_PATH_WALKS) outside
    ROOT's own definition; only RANGE_DISK_READERS read the disk; and 'research_outputs'
    is spelt only in the lane's path definitions and REGISTER's sources. Module level:
    the lane names appear only in the lane's definitions (ROOT's may use __file__) and
    the sys.path lines. Every one of these was measured on the pristine file first.
    ROUND 2 (2026-09-22), OD-F: `Path(str(GRID_PARQUET).replace("census2b/oracle/
    oracle_grid.parquet", "oracle/tape" + "_ranges"))` inside grid_toll() — the ONE
    function allowed to name GRID_PARQUET — spelt no sibling token, no
    'research_outputs' and no walk. So where a function may name a lane path, it may
    only use it in the measured shapes (_range_lane_shape): joined, tested, created,
    globbed, read, called, or quoted in a raise. And no disk reader is imported BY NAME
    (`from glob import glob as _g`): the call would carry a name RANGE_DISK_CALLS
    does not know."""
    bad = []
    for n in ast.walk(tree):
        if isinstance(n, ast.ImportFrom) and any(a.name in RANGE_DISK_CALLS for a in n.names):
            bad.append(f"line {n.lineno}: `{ast.unparse(n)}` imports a disk reader BY NAME — "
                       f"`{next(a.asname or a.name for a in n.names if a.name in RANGE_DISK_CALLS)}"
                       f"(...)` reads the disk under a name the disk fence does not know")
    for stmt in tree.body:
        if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef)):
            parent = {c: p for p in ast.walk(stmt) for c in ast.iter_child_nodes(p)}
            for n in ast.walk(stmt):
                if isinstance(n, ast.Name) and n.id in RANGE_LANE_PATHS \
                        and stmt.name not in RANGE_LANE_PATHS[n.id]:
                    bad.append(f"{stmt.name}() names the lane path `{n.id}` at line {n.lineno} — "
                               f"only {list(RANGE_LANE_PATHS[n.id]) or 'no function'} may: a path "
                               f"derived from it reaches the sibling tape by any spelling")
                elif isinstance(n, ast.Name) and n.id in RANGE_LANE_PATHS:
                    shape = _range_lane_shape(n, parent)
                    if shape is not None:
                        bad.append(f"{stmt.name}() uses the lane path `{n.id}` at line {n.lineno} "
                                   f"as `{shape}` — a lane path may only be joined (`/`), "
                                   f"tested, created, globbed or handed to a reader; converted "
                                   f"(str(), .replace, .as_posix, os.fspath, an f-string) it is "
                                   f"text that can be cut into any other path")
                elif isinstance(n, ast.Attribute) and n.attr in RANGE_PATH_WALKS:
                    bad.append(f"{stmt.name}() walks a path (`.{n.attr}`) at line {n.lineno} — from "
                               f"any lane directory, one step up and one down is the sibling tape")
                elif isinstance(n, ast.Call) and stmt.name not in RANGE_DISK_READERS and (
                        (isinstance(n.func, ast.Attribute) and n.func.attr in RANGE_DISK_CALLS)
                        or (isinstance(n.func, ast.Name) and n.func.id in RANGE_DISK_CALLS)):
                    bad.append(f"{stmt.name}() reads the disk (`{ast.unparse(n.func)}`) at line "
                               f"{n.lineno} — only {list(RANGE_DISK_READERS)} may")
                elif (isinstance(n, ast.Constant) and isinstance(n.value, str)
                      and id(n) not in docs and RANGE_LANE_TEXT in n.value):
                    bad.append(f"{stmt.name}() spells {RANGE_LANE_TEXT!r} at line {n.lineno} — "
                               f"the lane's directories are its module-level paths, never a "
                               f"string in a function")
            continue
        tgt = (stmt.targets if isinstance(stmt, ast.Assign)
               else [stmt.target] if isinstance(stmt, ast.AnnAssign) else [])
        lane_def = (len(tgt) == 1 and isinstance(tgt[0], ast.Name)
                    and tgt[0].id in RANGE_LANE_PATHS)
        is_root = lane_def and tgt[0].id == "ROOT"
        sys_path = (isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call)
                    and ast.unparse(stmt.value.func) == "sys.path.insert")
        for n in ast.walk(stmt):
            if isinstance(n, ast.Name) and n.id in RANGE_LANE_PATHS and isinstance(n.ctx, ast.Load):
                ok = ((lane_def and n.id == "ROOT") or (is_root and n.id == "__file__")
                      or (sys_path and n.id == "ROOT"))
                if not ok:
                    bad.append(f"module level names the lane path `{n.id}` at line {n.lineno} "
                               f"outside the lane's own definitions — a second path hung from it "
                               f"is a route to the sibling tape")
            elif isinstance(n, ast.Attribute) and n.attr in RANGE_PATH_WALKS and not is_root:
                bad.append(f"module level walks a path (`.{n.attr}`) at line {n.lineno} outside "
                           f"ROOT's own definition")
            elif (isinstance(n, ast.Constant) and isinstance(n.value, str) and id(n) not in docs
                  and id(n) not in sources and not lane_def and RANGE_LANE_TEXT in n.value):
                bad.append(f"module level spells {RANGE_LANE_TEXT!r} at line {n.lineno} outside the "
                           f"lane's path definitions and REGISTER's sources")
    return bad


def _range_sibling_ast(src: str | None = None) -> list[str]:
    """Inside oracle_daily.py, as CODE: the sibling tape's names (RANGE_SIBLING_DEFS, the
    writer) and any non-docstring string spelling its directory appear only in their
    own module-level definitions and in write_range_tape(); run() is held to one call
    of the writer, reported (_range_sibling_run); and the lane's paths are fenced
    (_range_lane_paths). Fails closed if the writer or its caller is gone."""
    src = (ROOT / "scripts" / "oracle_daily.py").read_text(encoding="utf-8") if src is None else src
    tree = ast.parse(src)
    docs = set()
    for n in ast.walk(tree):
        if isinstance(n, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            for st in getattr(n, "body", []):
                if (isinstance(st, ast.Expr) and isinstance(st.value, ast.Constant)
                        and isinstance(st.value.value, str)):
                    docs.add(id(st.value))
    names = (*RANGE_SIBLING_DEFS, RANGE_SIBLING_WRITER)

    def hits(node):
        for n in ast.walk(node):
            if isinstance(n, ast.Name) and n.id in names:
                yield n, f"the name `{n.id}`"
            elif isinstance(n, ast.Attribute) and n.attr in names:
                yield n, f"the attribute `.{n.attr}`"
            elif (isinstance(n, ast.Constant) and isinstance(n.value, str)
                  and id(n) not in docs and RANGE_SIBLING_TOKEN_RX.search(n.value)):
                yield n, f"the string {n.value[:40]!r}"

    bad: list[str] = []
    fns = {n.name: n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}
    for stmt in tree.body:
        if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if stmt.name == RANGE_SIBLING_WRITER:
                continue
            if stmt.name == RANGE_SIBLING_CALLER:
                bad += _range_sibling_run(stmt, hits)
                continue
            for n, what in hits(stmt):
                bad.append(f"{stmt.name}() names the sibling tape: {what} at line {n.lineno} — "
                           f"no gate reads a range record; only {RANGE_SIBLING_WRITER}() writes "
                           f"it and {RANGE_SIBLING_CALLER}() calls that, once")
            continue
        tgt = (stmt.targets if isinstance(stmt, ast.Assign)
               else [stmt.target] if isinstance(stmt, ast.AnnAssign) else [])
        if len(tgt) == 1 and isinstance(tgt[0], ast.Name) and tgt[0].id in RANGE_SIBLING_DEFS:
            continue                               # the definition itself
        for n, what in hits(stmt):
            bad.append(f"module level names the sibling tape: {what} at line {n.lineno}, "
                       f"outside its own definitions")
    for f in (RANGE_SIBLING_WRITER, RANGE_SIBLING_CALLER):
        if f not in fns:
            bad.append(f"{f}() not found — the sibling tape's fence has nothing to hold; fail closed")
    if RANGE_SIBLING_WRITER in fns and not any(
            isinstance(n, ast.Name) and n.id == "TAPE_RANGES_DIR"
            for n in ast.walk(fns[RANGE_SIBLING_WRITER])):
        bad.append(f"{RANGE_SIBLING_WRITER}() never names TAPE_RANGES_DIR — the fence is "
                   f"hunting a stale name; fail closed")
    bad += _range_lane_paths(tree, docs, _register_source_ids(tree))
    return bad


def _range_window_bind(src: str | None = None) -> list[str]:
    """REGISTER['RANGE_WINDOW_BARS']['value'] IS the Attribute node RNG.V2_WINDOW_BARS —
    read off the source by AST (round-2 review: the value check alone compared the
    machine's constant with itself, and a typed 1700 passed it too)."""
    src = (ROOT / "scripts" / "oracle_daily.py").read_text(encoding="utf-8") if src is None else src
    want = f"{RANGE_ALIAS}.{RANGE_REGISTER_IMPORTS[0]}"
    for st in ast.parse(src).body:
        tgt = (st.targets if isinstance(st, ast.Assign)
               else [st.target] if isinstance(st, ast.AnnAssign) else [])
        if not (any(isinstance(t, ast.Name) and t.id == "REGISTER" for t in tgt)
                and isinstance(st.value, ast.Dict)):
            continue
        for k, row in zip(st.value.keys, st.value.values):
            if not (isinstance(k, ast.Constant) and k.value == "RANGE_WINDOW_BARS"
                    and isinstance(row, ast.Dict)):
                continue
            v = next((v for kk, v in zip(row.keys, row.values)
                      if isinstance(kk, ast.Constant) and kk.value == "value"), None)
            ok = (isinstance(v, ast.Attribute) and isinstance(v.value, ast.Name)
                  and v.value.id == RANGE_ALIAS and v.attr == RANGE_REGISTER_IMPORTS[0])
            return [] if ok else [
                f"REGISTER['RANGE_WINDOW_BARS']['value'] is "
                f"`{ast.unparse(v) if v is not None else None}` at line "
                f"{getattr(v, 'lineno', '?')}, not the attribute `{want}` — the window is "
                f"IMPORTED from the machine, never typed"]
    return ["REGISTER['RANGE_WINDOW_BARS'] was not found in oracle_daily.py's REGISTER literal "
            "— fail closed"]


def _range_containment(mod=None) -> tuple[list[str], dict]:
    """A display organ may not take the Board down, and may not run off its lens."""
    mod = OD if mod is None else mod
    sym = mod.REGISTER["ROSTER"]["value"][0]
    h4 = mod.load_lens(sym, "4h")
    bad, got = [], {}
    for name, frame, must in (
            ("an EMPTY frame", h4.iloc[0:0], None),
            ("a 1h frame", mod.load_lens(sym, "1h", tail=400), "RANGE_LENS")):
        try:
            r = mod.range_layer(frame)
        except Exception as e:
            bad.append(f"range_layer RAISED on {name} ({e.__class__.__name__}: {e}) — a fault in "
                       f"a display organ would have cost the operator the whole edition")
            continue
        got[name] = r.get("error")
        if not r.get("error") or r.get("has_range") or r.get("state") != mod.RANGE_UNAVAILABLE:
            bad.append(f"range_layer on {name} returned state={r.get('state')!r} "
                       f"error={r.get('error')!r} — it must say UNAVAILABLE and why")
        elif must and must not in r["error"]:
            bad.append(f"range_layer refused {name} without naming {must}: {r['error']!r}")
    ok = mod.range_layer(h4)
    if ok.get("error"):
        bad.append(f"range_layer FAILED on the real {sym} 4h frame: {ok['error']}")
    return bad, got


@contextlib.contextmanager
def _range_swap_levels(extra: str):
    """analytics.levels REPLACED, for the block, by a module built from its own source
    plus `extra` — in sys.modules and on the package, so a mutant built inside the
    block (`from analytics import levels as L`) gets it. Restored in `finally`. No file
    is written."""
    import types
    import analytics
    import analytics.levels as real
    mod = types.ModuleType(real.__name__)
    mod.__file__, mod.__package__ = real.__file__, real.__package__
    exec(compile(Path(real.__file__).read_text(encoding="utf-8") + extra, real.__file__, "exec"),
         mod.__dict__)
    sys.modules[real.__name__] = mod
    analytics.levels = mod
    try:
        yield mod
    finally:
        sys.modules[real.__name__] = real
        analytics.levels = real


def f_br_14() -> None:
    od_src = (ROOT / "scripts" / "oracle_daily.py").read_text(encoding="utf-8")
    idx = _range_import_index()                  # the reverse import index, live tree
    pe_path = ROOT / "scripts" / "posture_engine.py"
    # THE ORACLE'S MACHINE's source, for the machine-closure plant (A-OR1-1 iv): since
    # 2026-09-22 that is scripts/rangefinder_core.py, not engine/rangefinder.py
    rf_src = (ROOT / "scripts" / f"{ORACLE_RANGE_MODULE}.py").read_text(encoding="utf-8")
    gate_src = _range_plant_after_write(od_src, RANGE_GATE_TEXT)
    narrow = _range_plant_narrow_except(od_src)
    # a READER misbehaving: legal to the AST leg (render_html is on the allow-list),
    # so only the run can see it — the page quietly drops every row with a breach open
    drop_src = _range_plant_in(od_src, "render_html",
                               f"view = dict(view, assets=[a for a in view['assets'] "
                               f"if not a['{RANGE_KEY}'].get('pending')])")
    drop_ast = len(_range_ast(drop_src)[0]) if drop_src else -1
    # the same reader, misbehaving IN PLACE. `.reverse()`, not a dist_atr sort:
    # RANGE_MUTANT_ROSTER is 3 and BTCUSDT/ETHUSDT/ENAUSDT all carry dist_atr None
    # today, so a distance sort is a no-op on that slice and the leg would be VOID.
    in_place_src = _range_plant_in(od_src, "tide_tables", 'view["assets"].reverse()')
    # the three import routes the widened fence closed; the gate itself is identical
    bypass_a = _range_plant_bypass(od_src, "import rangefinder_twin as RT",
                                   "RT.run_v2(RT.tape_from_klines(h4, "
                                   "n_bars=RT.V2_WINDOW_BARS), RT.PINS_V2)")
    bypass_b = _range_plant_bypass(od_src, "import engine",
                                   "engine.rangefinder.run_v2(engine.rangefinder."
                                   "tape_from_klines(h4, n_bars=1700), "
                                   "engine.rangefinder.PINS_V2)")
    bypass_c = _range_plant_bypass(od_src, None,
                                   "(lambda _m: _m.run_v2(_m.tape_from_klines(h4, "
                                   "n_bars=1700), _m.PINS_V2))"
                                   f'(sys.modules["{ORACLE_RANGE_MODULE}"])')
    # and the route A-OR1-1 opened: the Oracle's own machine under a SECOND alias
    bypass_d = _range_plant_bypass(od_src, f"import {ORACLE_RANGE_MODULE} as RC",
                                   "RC.run_v2(RC.tape_from_klines(h4, "
                                   "n_bars=RC.V2_WINDOW_BARS), RC.PINS_V2)")
    rules = ROOT / "scripts" / "tierc3_rules.py"
    # leg (e): the engine copy re-imported beside the sanctioned binding, in a COPY
    core_bind = f"import {ORACLE_RANGE_MODULE} as {RANGE_ALIAS}"
    core_line = [ln for ln in od_src.splitlines(keepends=True)
                 if ln.split("#")[0].strip() == core_bind]
    engine_src = (od_src.replace(core_line[0], core_line[0]
                                 + f"from engine import rangefinder as {RANGE_ALIAS}\n", 1)
                  if len(core_line) == 1 else None)
    # leg (f): a range column appended to oracle_daily.TAPE_COLS as a frame, WITH A
    # CONTROL. This used to plant on a copy of the artifact set's own D-4 frame, and on
    # the 2026-09-21 set (32 columns, 8 of them range_*) that frame was red BEFORE the
    # plant: the break line read "extra ['range_state', 'range_top', ...]", and the
    # plant added nothing to it (round-1 review). Now the unplanted base must be green
    # first, or the judge says so WITHOUT the must-string and _break prints "RED FOR
    # THE WRONG REASON" instead of a false RED.
    def d4_plant() -> list[str]:
        base = pd.DataFrame(columns=list(OD.TAPE_COLS))
        control = _range_main_tape({"the unplanted frame": base})
        if control:
            return [f"CONTROL FAILED: the unplanted frame (oracle_daily.TAPE_COLS) is already "
                    f"red on its own ({len(control)} finding(s)), so a red on the plant would "
                    f"prove nothing"]
        planted = base.copy()
        planted["range_state"] = pd.Series(dtype="string")
        return _range_main_tape({"oracle_daily.TAPE_COLS as a frame, range_state appended":
                                 planted})

    # ── ROUND-1 REVIEW PLANTS (2026-09-22), each on a COPY of the source ────────────
    # (c) the same heat-damping gate as bypass A-D, reaching the machine by a getter
    # that no import statement names (OD-1..8 of the review)
    getter = "(lambda _m: _m.run_v2(_m.tape_from_klines(h4, n_bars=1700), _m.PINS_V2))({})"
    od_bypass = [
        ("OD-1", "`import importlib`; importlib.import_module('rangefinder_core')",
         "import importlib", getter.format(f'importlib.import_module("{ORACLE_RANGE_MODULE}")'),
         "can be reached through it"),
        ("OD-2", "__import__('rangefinder_core')",
         None, getter.format(f'__import__("{ORACLE_RANGE_MODULE}")'),
         "can be reached through it"),
        ("OD-3", "sys.modules.get('rangefinder_core') — the old guard matched only a "
                 "Subscript on .modules",
         None, getter.format(f'sys.modules.get("{ORACLE_RANGE_MODULE}")'), "sys.modules"),
        ("OD-4", "globals()['RNG']", None, getter.format(f'globals()["{RANGE_ALIAS}"]'),
         "can be reached through it"),
        ("OD-6", "`import oracle_daily as _S`; _S.RNG",
         "import oracle_daily as _S", getter.format(f"_S.{RANGE_ALIAS}"),
         "imports oracle_daily itself"),
        ("OD-7", "importlib.import_module('engine.rangefinder') — lazy, so leg (e)'s closure "
                 "is green too",
         "import importlib", getter.format(f'importlib.import_module("{RANGE_MACHINE}")'),
         "can be reached through it"),
        ("OD-8", "vars(importlib.import_module(__name__))['RNG']",
         "import importlib",
         getter.format(f'vars(importlib.import_module(__name__))["{RANGE_ALIAS}"]'),
         "can be reached through it"),
    ]
    od5 = _range_plant_in(od_src, "trap_card", f"from oracle_daily import {RANGE_ALIAS} as _Q")
    # (c) NO STASH — OD-9, the review's side channel, verbatim: a module-level memo that
    # range_layer (allow-listed) fills, read back in build_view by keys that are not in
    # RANGE_ONLY_KEYS ('top', 'bottom', 'atr')
    snap_ret = '        return {**RNG.snapshot(d, v2), "error": None}\n'
    memo_ret = ('        _o = {**RNG.snapshot(d, v2), "error": None}\n'
                '        _MEMO[float(h4["close"].iloc[-1])] = _o\n'
                '        return _o\n')

    def memo_plant(gate: str) -> str | None:
        if od_src.count(snap_ret) != 1 or od_src.count(RANGE_IMPORT_ANCHOR) != 1:
            return None
        s = od_src.replace(snap_ret, memo_ret, 1).replace(
            RANGE_IMPORT_ANCHOR, RANGE_IMPORT_ANCHOR + "_MEMO = {}\n", 1)
        return _range_plant_after_write(s, '_m = _MEMO.get(float(h4["close"].iloc[-1])); '
                                           f'assets[-1]["heat"] = assets[-1]["heat"] * {gate}')
    od9 = memo_plant('(0.5 if _m and _m["top"] is not None and _m["atr"] and '
                     'min(abs(_m["top"] - price), abs(price - _m["bottom"])) < 1.0 * _m["atr"] '
                     'else 1.0)')
    # the same memo, the gate keyed on its PRESENCE alone, so that it fires on the first
    # RANGE_MUTANT_ROSTER rows too (none of which holds a live box today): with one
    # shared module the stubbed runs read REAL's memo and the three runs agree
    od9b = memo_plant("(0.5 if _m is not None else 1.0)")
    # (d)/(h) run() — OD-10: the written sibling tape read back just before the D-7
    # record, heat doubled within 1 ATR of a boundary
    cal_line = "    cal_p, cal_sha, cal_b = write_calibration(view, date_str, slot)\n"
    od10 = (od_src.replace(cal_line,
                           "    _pr = pd.read_parquet(rtape_p).set_index('asset')\n"
                           "    for _a in view['assets']:\n"
                           "        _d = _pr.loc[_a['symbol'], 'range_dist_atr']\n"
                           "        if _d == _d and _d < 1.0:\n"
                           "            _a['heat'] = _a['heat'] * 2\n" + cal_line, 1)
            if od_src.count(cal_line) == 1 else None)
    # (h) derived paths in trap_card(); and the same derivation RUN, damping heat when the
    # sibling directory holds anything — only leg (d)'s per-run seeds can see it move
    derived = "(TAPE_DIR.parent / ('tape' + '_ranges'))"
    seeded_src = (od_src.replace(RANGE_HEAT_LINE, RANGE_HEAT_LINE
                                 + f"        _rp = sorted({derived}.glob('*.parquet'))\n"
                                 + "        if _rp:\n            heat *= 0.5\n", 1)
                  if od_src.count(RANGE_HEAT_LINE) == 1 else None)

    # ── ROUND-2 REVIEW PLANTS (2026-09-22), each on a COPY of the source ────────────
    # (c) the machine FOUND rather than named: a hasattr() scan over whatever a route
    # hands back, then the same heat-damping gate (OD-A..D of the review)
    scan = 'next(_x for _x in list({}) if hasattr(_x, "PINS_V2") and hasattr(_x, "snapshot"))'
    od_found = [
        ("OD-A", "`from sys import modules as _MODS` and a hasattr() scan of it — the "
                 "ImportFrom's parts are {sys, modules} and `.modules` is never an Attribute",
         "from sys import modules as _MODS", scan.format("_MODS.values()"), "imports FROM sys"),
        ("OD-B", "sys._getframe(0).f_globals and a hasattr() scan of it",
         None, scan.format("sys._getframe(0).f_globals.values()"), "a `._getframe` attribute"),
        ("OD-C", "`import gc` and a hasattr() scan of gc.get_objects()",
         "import gc", scan.format("gc.get_objects()"), "imports the dynamic-import machinery ['gc']"),
        ("OD-D", "`import inspect`; inspect.currentframe().f_globals",
         "import inspect", scan.format("inspect.currentframe().f_globals.values()"),
         "imports the dynamic-import machinery ['inspect']"),
    ]
    od_a = _range_plant_bypass(od_src, od_found[0][2], getter.format(od_found[0][3]))
    # OD-E: a LAZILY imported re-exporter, in build_view — the review's own was
    # TIER-C10's fixture binding engine.rangefinder as E; if that file is ever gone, this
    # file (which re-exports the Oracle, and with it RNG) stands in, so the plant never
    # depends on another lane's layout
    reexp = "tierc10_rf_fixtures" if "tierc10_rf_fixtures" in idx["tainted"] else "oracle_fixtures"
    od_e = (od_src.replace(RANGE_HEAT_LINE, RANGE_HEAT_LINE + f"        import {reexp} as _T\n"
                           + RANGE_DAMP_GATE.format(getter=getter.format(
                               "_T.E" if reexp == "tierc10_rf_fixtures" else f"_T.OD.{RANGE_ALIAS}")), 1)
            if od_src.count(RANGE_HEAT_LINE) == 1 else None)
    # OD-G: an allow-listed READER running the machine itself and writing non-view
    # state through a local alias — render_html flips REGISTER['TARGET_BUCKET_ATR'],
    # which run() then files in the D-7 record; OD-G2 the alias write alone
    od_g = _range_plant_in(
        od_src, "render_html",
        '_q = REGISTER["TARGET_BUCKET_ATR"]\n'
        f'_d = {RANGE_ALIAS}.tape_from_klines(load_lens(view["assets"][0]["symbol"], "4h"), '
        f'n_bars={RANGE_ALIAS}.V2_WINDOW_BARS)\n'
        f'if not {RANGE_ALIAS}.snapshot(_d, {RANGE_ALIAS}.run_v2(_d, {RANGE_ALIAS}.PINS_V2))'
        f'["has_range"]:\n'
        '    _q["value"] = "daily" if _q["value"] == "lens" else "lens"\n')
    od_g2 = _range_plant_in(
        od_src, "render_html",
        '_q = REGISTER["TARGET_BUCKET_ATR"]\n'
        f'if view["assets"] and not view["assets"][0]["{RANGE_KEY}"]["has_range"]:\n'
        '    _q["value"] = "daily" if _q["value"] == "lens" else "lens"\n')
    # OD-H: `log` rebound in run(), so that the sanctioned log(f'{rtape_p} ...') hands
    # the sibling path to a gate that reads it and doubles heat within 1 ATR
    wl = "    rtape_p, rtape_sha, rtape_b = write_range_tape(view, date_str)\n"
    od_h = (od_src.replace(wl, "    _log0 = log\n"
                               "    def log(*a, **k):\n"
                               "        _log0(*a, **k)\n"
                               "        _s = str(a[0]).split() if a else []\n"
                               "        if _s and _s[0].endswith('.parquet') and '_tape_' in _s[0] "
                               "and 'oracle_tape_2' not in _s[0]:\n"
                               "            _t = pd.read_parquet(_s[0]).set_index('asset')\n"
                               "            for _a in view['assets']:\n"
                               "                _v = _t.loc[_a['symbol'], 'range_dist_atr']\n"
                               "                if _v == _v and _v < 1.0:\n"
                               "                    _a['heat'] = _a['heat'] * 2\n" + wl, 1)
            if od_src.count(wl) == 1 else None)
    # OD-F: grid_toll() — the ONE function allowed GRID_PARQUET — cuts the sibling
    # directory out of the grid's path string and doubles the toll if any symbol sits
    # within 0.5 ATR of a boundary. No sibling token, no 'research_outputs', no walk.
    gt_ret = '    return g[g["cut"] == "ALL"].reset_index(drop=True)\n'
    od_f = (od_src.replace(gt_ret, '    _rp = Path(str(GRID_PARQUET).replace('
                                   '"census2b/oracle/oracle_grid.parquet", "oracle/tape" + "_ranges"))\n'
                                   '    _ys = sorted(_rp.glob("*.parquet"))\n'
                                   '    if _ys:\n'
                                   '        _t = pd.read_parquet(_ys[-1])\n'
                                   '        if (_t["range_dist_atr"] < 0.5).any():\n'
                                   '            g = g.assign(toll_atr=g["toll_atr"] * 2.0)\n'
                                   + gt_ret, 1)
            if od_src.count(gt_ret) == 1 else None)
    # the window TYPED, not imported: the value check alone passed it
    win_line = f'        "value": {RANGE_ALIAS}.{RANGE_REGISTER_IMPORTS[0]},\n'
    od_win = (od_src.replace(win_line, '        "value": 1700,\n', 1)
              if od_src.count(win_line) == 1 else None)
    # (b) through leg (d): analytics.levels SWAPPED, for one leg-(d) run, for a module
    # built from its source plus a wrapped lines_in_sand() that build_view calls — DEC-H
    # reads the LIVE sibling directory by a path spelt in fragments from its own
    # __file__; DEC-E2 runs the machine off its CALLER's globals and frame. Neither is
    # red on any static leg; both are red on leg (d)'s tripwires.
    lis_wrap = ("\n\n_f_br_14_lis = lines_in_sand\n\n\n"
                "def lines_in_sand(*a, **k):\n{body}    return _f_br_14_lis(*a, **k)\n")
    dec_h = lis_wrap.format(body=(
        "    import pathlib\n    import pandas as pd\n"
        "    _p = (pathlib.Path(__file__).resolve().parents[1] / 'research_outputs' / 'oracle'\n"
        "          / ('tape' + '_ranges'))\n"
        "    try:\n        _t = pd.read_parquet(_p)\n    except Exception:\n        _t = None\n"
        "    if _t is not None and (_t['range_dist_atr'] < 0.5).any():\n        return []\n"))
    dec_e2 = lis_wrap.format(body=(
        "    import sys\n    _f = sys._getframe(1)\n"
        "    _m, _h = _f.f_globals.get('RN' + 'G'), _f.f_locals.get('h4')\n"
        "    if _m is not None and _h is not None:\n"
        "        _d = _m.tape_from_klines(_h, n_bars=1700)\n"
        "        _s = _m.snapshot(_d, _m.run_v2(_d, _m.PINS_V2))\n"
        "        if _s['has_range'] and _s['dist_atr'] is not None and _s['dist_atr'] < 1.0:\n"
        "            return []\n"))

    def swapped_run(extra):
        def judge():
            with _range_swap_levels(extra):
                return _range_behaviour(n_roster=RANGE_MUTANT_ROSTER)[0]
        return judge
    # (b) the decision side as CODE — each appended to the TEXT of a decision module,
    # inside a function (a LAZY import: no closure leg can see it), never executed
    lazy = "\n\ndef _planted_gate(h4):\n"
    dec_plants = [
        ("DEC-5", "tierc3_rules.py", "importlib.import_module('rangefinder_core')",
         lazy + "    import importlib\n    return importlib.import_module('rangefinder_core')"
                ".run_v2\n", "names `importlib`"),
        ("DEC-7", "tierc3_rules.py", "sys.modules['rangefinder_core']",
         lazy + "    import sys\n    return sys.modules['rangefinder_core']\n", "`.modules`"),
        ("DEC-9", "tierc3_rules.py", "from oracle_daily import RNG",
         lazy + "    from oracle_daily import RNG\n    return RNG\n",
         "imports the range machine or the Oracle"),
        ("DEC-10", "tierc3_rules.py", "`from engine import (` / `rangefinder,` / `)` — the "
                                      "ordinary parenthesised style; the line regex sees line one",
         lazy + "    from engine import (\n        rangefinder,\n    )\n    return rangefinder\n",
         "imports the range machine or the Oracle"),
        ("DEC-11", "tierc3_rules.py", "`import \\` / `rangefinder_core` — backslash-continued",
         lazy + "    import \\\n        rangefinder_core\n    return rangefinder_core\n",
         "imports the range machine or the Oracle"),
        ("DEC-17", "engine/signals.py", "DEC-5's importlib gate, in engine.signals",
         lazy + "    import importlib\n    return importlib.import_module('rangefinder_core')"
                ".run_v2\n", "names `importlib`"),
        # ── the round-2 review's (2026-09-22): each was green on (b) AND (h)
        ("DEC-A", "tierc3_rules.py", "`from importlib import import_module as _im` — an "
                                     "ImportFrom: no Name `importlib` is ever loaded",
         lazy + "    from importlib import import_module as _im\n"
                "    return _im('rang' + 'efinder_core').run_v2\n",
         "imports the dynamic-import machinery"),
        ("DEC-B", "tierc3_rules.py", "getattr(sys, 'modules') — `.modules` is never an Attribute",
         lazy + "    import sys\n    return getattr(sys, 'modules').get('rang' + 'efinder_core')\n",
         "names `getattr`"),
        ("DEC-C", "tierc3_rules.py", "pkgutil.resolve_name",
         lazy + "    import pkgutil\n    return pkgutil.resolve_name('rang' + 'efinder_core')\n",
         "names `pkgutil`"),
        ("DEC-D", "tierc3_rules.py", "`import oracle_fixtures as _OF`; _OF.OD.RNG — a module "
                                     "that re-exports the Oracle, and with it the machine",
         lazy + "    import oracle_fixtures as _OF\n    return _OF.OD.RNG.run_v2\n",
         "the reverse import index"),
        ("DEC-E", "analytics/levels.py", "sys._getframe(2).f_globals['RNG'] — the Oracle's own "
                                         "binding, read off its caller's frame",
         lazy + "    import sys\n    return sys._getframe(2).f_globals['RNG'].run_v2\n",
         "a `._getframe` attribute"),
        ("DEC-F", "engine/signals.py", "`import engine`; engine.rangefinder.run_v2 — an "
                                       "attribute walk from a bare package import",
         lazy + "    import engine\n    return engine.rangefinder.run_v2\n",
         "by attribute walk"),
        ("DEC-G", "tierc3_rules.py", "__builtins__['__import__']",
         lazy + "    return __builtins__['__import__']('rang' + 'efinder_core').run_v2\n",
         "names `__builtins__`"),
    ]

    def dec_judge(rel, text):
        key = rel if "/" in rel else f"scripts/{rel}"
        return lambda: _range_decision_ast(
            {key: (ROOT / key).read_text(encoding="utf-8") + text}, idx)

    # (b) the scan set derived from the real closure — a COPY of analytics/ shadowing
    # the real package in a clean subprocess, `import rangefinder_core as _RF` appended
    # to its levels.py (level_registry's levels are made there)
    def shadow_levels() -> list[str]:
        with tempfile.TemporaryDirectory(prefix="f-br-14-shadow-") as td:
            shutil.copytree(ROOT / "analytics", Path(td) / "analytics",
                            ignore=shutil.ignore_patterns("__pycache__"))
            lv = Path(td) / "analytics" / "levels.py"
            lv.write_text(lv.read_text(encoding="utf-8")
                          + f"\nimport {ORACLE_RANGE_MODULE} as _RF\n", encoding="utf-8")
            files = _closure_files("oracle_daily", shadow=td, pre=("analytics", "analytics.levels"))
            got = Path(files.get("analytics.levels") or "/").resolve()
            if not _under(got, Path(td).resolve()):
                return [f"VOID: analytics.levels was loaded from {got}, not the planted copy"]
            sidx = _range_import_index(td)
            srcs = _range_decision_sources({"oracle_daily": files}, shadow=td, index=sidx)
            return (_range_static(srcs) + _range_decision_ast(srcs, sidx)
                    + _range_sole_importer(files, shadow=td))

    # (b) THE SHIM (round-2 review): a NEW module in the shadow copy of analytics/ that
    # re-exports the machine, imported only INSIDE a function of the shadow levels.py.
    # It is in no closure, so it was in no scan set, and every leg was green. The static
    # import walk (_range_follow) puts it in the scan set, and the reverse import index
    # makes levels.py's lazy import of it red too.
    def shim_plant() -> list[str]:
        with tempfile.TemporaryDirectory(prefix="f-br-14-shim-") as td:
            shutil.copytree(ROOT / "analytics", Path(td) / "analytics",
                            ignore=shutil.ignore_patterns("__pycache__"))
            (Path(td) / "analytics" / "_shim.py").write_text(
                f"from {ORACLE_RANGE_MODULE} import run_v2, PINS_V2, tape_from_klines  "
                f"# noqa: F401\n", encoding="utf-8")
            lv = Path(td) / "analytics" / "levels.py"
            lv.write_text(lv.read_text(encoding="utf-8") + lazy
                          + "    from analytics import _shim as _S\n"
                            "    return _S.run_v2(_S.tape_from_klines(h4, n_bars=1700), "
                            "_S.PINS_V2)\n", encoding="utf-8")
            files = _closure_files("oracle_daily", shadow=td, pre=("analytics", "analytics.levels"))
            got = Path(files.get("analytics.levels") or "/").resolve()
            if not _under(got, Path(td).resolve()):
                return [f"VOID: analytics.levels was loaded from {got}, not the planted copy"]
            if "analytics._shim" in files:
                return ["VOID: the shim was IMPORTED by the closure probe — the plant is not lazy"]
            sidx = _range_import_index(td)
            srcs = _range_decision_sources({"oracle_daily": files}, shadow=td, index=sidx)
            return (_range_static(srcs) + _range_decision_ast(srcs, sidx)
                    + _range_sibling_static(srcs) + _range_sole_importer(files, shadow=td))

    # leg (g): the all-None day through the real writer, then one field dropped, then
    # the string pin taken off one field (object dtype, every value None)
    empty_df, _empty_schema = _range_sibling_empty_day()
    roster = list(OD.REGISTER["ROSTER"]["value"])
    dropped = empty_df.drop(columns=["range_dist_atr"])
    unpinned = empty_df.astype({"range_pending_side": object})
    unpinned["range_pending_side"] = None
    # leg (h): a gate reading the sibling tape — in a decision module's TEXT, and in
    # oracle_daily's trap_card()
    wall_text = ('\n_P = __import__("pandas").read_parquet(__import__("pathlib").Path('
                 '"research_outputs/oracle/tape_ranges"))\n')

    def ast_plant(src):
        return None if src is None else (lambda: _range_ast(src)[0])

    def ast_plant_h(src):
        return None if src is None else (lambda: _range_sibling_ast(src))

    def gate_plant(fn, stmt):
        return (f"AST PLANT (a range read planted in {fn}(): `{stmt}`)", f"{fn}() mentions",
                ast_plant(_range_plant_in(od_src, fn, stmt)))

    # (name, the finding it MUST produce, how it is judged). One at a time.
    plants = [
        ("SHA PLANT (one comment line appended to a copy of posture_engine.py)",
         "is not the pinned file",
         lambda: _range_sha(pe_path.read_bytes() + b"\n# F-BR-14 planted byte\n")[0]),
        ("CLOSURE PLANT (`import engine.rangefinder` planted in a copy of posture_engine.py)",
         "posture_engine reaches",
         lambda: _range_reach("posture_engine", _closure_src(
             "posture_engine", pe_path.read_text(encoding="utf-8") + "\nimport engine.rangefinder\n"),
             RANGE_BANNED_IN_DECISION)),
        (f"CLOSURE PLANT (`import {ORACLE_RANGE_MODULE}` — the Oracle's own machine — planted "
         f"in a copy of posture_engine.py)",
         "posture_engine reaches",
         lambda: _range_reach("posture_engine", _closure_src(
             "posture_engine", pe_path.read_text(encoding="utf-8")
             + f"\nimport {ORACLE_RANGE_MODULE}\n"), RANGE_BANNED_IN_DECISION)),
        (f"CLOSURE PLANT (`from engine import journal` planted in a copy of "
         f"scripts/{ORACLE_RANGE_MODULE}.py)",
         "the range machine reaches",
         lambda: _range_reach("the range machine", _closure_src(
             "rangefinder_f_br_14_planted", rf_src + "\nfrom engine import journal\n"),
             RANGE_BANNED_IN_MACHINE)),
        (f"STATIC PLANT (`from engine.rangefinder import run_v2` appended to the TEXT of "
         f"{rules.name}, never executed)",
         "imports the range machine",
         lambda: _range_static({rules.name: rules.read_text(encoding="utf-8")
                                + "\nfrom engine.rangefinder import run_v2\n"})),
        (f"STATIC PLANT (`from {ORACLE_RANGE_MODULE} import run_v2` appended to the TEXT of "
         f"{rules.name}, never executed)",
         "imports the range machine",
         lambda: _range_static({rules.name: rules.read_text(encoding="utf-8")
                                + f"\nfrom {ORACLE_RANGE_MODULE} import run_v2\n"})),
        (f"AST PLANT (the contract's gate read, planted after build_view's one write: "
         f"`{RANGE_GATE_TEXT}`)",
         "OUTSIDE the one assignment", ast_plant(gate_src)),
        ("AST PLANT (the one write made conditional on heat — not the permitted shape)",
         "exactly ONE write",
         ast_plant(od_src.replace(f'assets[-1]["{RANGE_KEY}"] = {RANGE_PRODUCER}(h4)',
                                  f'assets[-1]["{RANGE_KEY}"] = ({RANGE_PRODUCER}(h4) if heat '
                                  f'> 1 else {RANGE_PRODUCER}(h1))', 1)
                   if od_src.count(f'assets[-1]["{RANGE_KEY}"] = {RANGE_PRODUCER}(h4)') == 1
                   else None)),
        gate_plant("level_registry", f"_p = {RANGE_ALIAS}.run_v2({RANGE_ALIAS}.tape_from_klines(h4), "
                                     f"{RANGE_ALIAS}.PINS_V2)['state']"),
        gate_plant("trap_card", f"_p = {RANGE_PRODUCER}(h4)['dist_atr']"),
        gate_plant("net_rr", f"reward = reward * (1 if {RANGE_PRODUCER} else 0)"),
        gate_plant("fired_events", f"_p = {RANGE_ALIAS}.ATR_LEN"),
        gate_plant("r1_block", f"view = dict(view, assets=[a for a in view['assets'] "
                               f"if not a['{RANGE_KEY}']['has_range']])"),
        gate_plant("write_calibration", f"_p = [a.get('{RANGE_KEY}') for a in view['assets']]"),
        ("AST PLANT (the key smuggled BY VALUE through a name, in a new function)",
         "_planted_smuggle() mentions",
         ast_plant(od_src + f'\n\ndef _planted_smuggle(a):\n    k = "{RANGE_KEY}"\n    return a[k]\n')),
        ("AST PLANT (a gate that never names the key: it calls range_watch())",
         "_planted_watch_gate() mentions",
         ast_plant(od_src + "\n\ndef _planted_watch_gate(view):\n"
                            "    return {w['symbol'] for w in range_watch(view)}\n")),
        (f"AST PLANT (`{RANGE_ALIAS}` read at module level, outside REGISTER)",
         "module level mentions",
         ast_plant(od_src + f"\n_PLANTED_PINS = {RANGE_ALIAS}.PINS_V2\n")),
        ("BYPASS PLANT A (the heat-damping gate reached through `import rangefinder_twin "
         "as RT`: the display twin re-exports the whole machine, and the gate names no "
         "key, alias or helper)",
         "imported a second way", ast_plant(bypass_a)),
        ("BYPASS PLANT B (the same gate reached by a bare `import engine` and an "
         "attribute walk to engine.rangefinder)",
         "bare `import engine`", ast_plant(bypass_b)),
        (f"BYPASS PLANT C (the same gate with NO import statement at all: "
         f"sys.modules['{ORACLE_RANGE_MODULE}'], the module the Oracle's own import put there)",
         "sys.modules", ast_plant(bypass_c)),
        (f"BYPASS PLANT D (the same gate reached through the Oracle's OWN machine under a "
         f"second alias: `import {ORACLE_RANGE_MODULE} as RC`)",
         "imported a second way", ast_plant(bypass_d)),
        (f"BEHAVIOUR PLANT (the same gate read, RUN: oracle_daily.run() of a planted copy, "
         f"a fresh module per run, over the first {RANGE_MUTANT_ROSTER} roster rows, EMPTY vs "
         f"HOT vs REAL)",
         "decision side moved",
         (lambda: _range_behaviour(gate_src, n_roster=RANGE_MUTANT_ROSTER)[0])
         if gate_src else None),
        (f"RENDER PLANT (a reader misbehaving: render_html drops every row with a breach "
         f"pending. The AST leg finds {drop_ast} problem(s) in it — render_html is on the "
         f"allow-list — so only the run can object; mutant, first {RANGE_MUTANT_ROSTER} roster rows)",
         "the rendered section",
         (lambda: _range_behaviour(drop_src, n_roster=RANGE_MUTANT_ROSTER)[0])
         if drop_src else None),
        ("RENDER PLANT (a reader misbehaving IN PLACE: tide_tables sorts view['assets'] "
         "instead of sorting a copy — the AST leg finds 0 problems, tide_tables is on the "
         "allow-list, and the mutation is identical in all three runs, so the comparison "
         "cannot see it either; only the guard around the render can)",
         "MUTATED the view",
         (lambda: _range_behaviour(in_place_src,
                                   n_roster=RANGE_MUTANT_ROSTER)[0]) if in_place_src else None),
        ("VALUE PLANT (a corrupt snapshot by hand: the box upside down, dist_atr x10, "
         "pos_pct blanked — the shape the machine's snapshot() took in the review's mirror)",
         "not self-consistent",
         lambda: _range_values(_range_corrupt())),
        ("VALUE PLANT, THE SIBLING TAPE (write_range_tape's range_top/range_bottom swapped "
         "over a self-consistent box: the page prints one thing, the parquet records another)",
         "the tape does not record",
         lambda: _range_values(*_range_tape_swapped())),
        ("WATCH PLANT (range_watch's comparison inverted, `d >= lim`: EDGE WATCH then "
         "flags the FARTHEST symbols and drops the nearest)",
         "EDGE WATCH membership",
         lambda: _range_watch_membership(_range_watch_inverted)),
        ("TAPE-NAME PLANT (a sibling-tape column called range_edge_atr)",
         "trips the banned vocabulary",
         lambda: _range_tape_names([*OD.RANGE_TAPE_COLS, "range_edge_atr"])),
        (f"MACHINE PLANT, leg (e) (a COPY of oracle_daily.py with `from engine import "
         f"rangefinder as {RANGE_ALIAS}` re-added under the sanctioned binding, imported in a "
         f"clean subprocess)",
         "reaches the engine copy",
         (lambda: _range_oracle_machine(_closure_src("oracle_daily", engine_src)))
         if engine_src else None),
        ("D-4 PLANT, leg (f) (range_state appended to oracle_daily.TAPE_COLS as a frame, "
         "after a CONTROL: the unplanted frame must be green first)",
         "extra ['range_state']", d4_plant),
        ("SIBLING PLANT, leg (g) (range_dist_atr dropped from a copy of the all-None day "
         "written through write_range_tape)",
         "the sibling tape does not carry",
         lambda: _range_sibling({"the all-None day, range_dist_atr dropped":
                                 (dropped, _frame_schema(dropped))}, roster)),
        ("SIBLING PLANT, leg (g) (the string pin taken off range_pending_side on the all-None "
         "day: object dtype, every value None — the 2026-09-21 review's hazard)",
         "not the pinned one",
         lambda: _range_sibling({"the all-None day, range_pending_side unpinned":
                                 (unpinned, _frame_schema(unpinned))}, roster)),
        (f"SIBLING-WALL PLANT, leg (h) (a read of research_outputs/oracle/tape_ranges appended "
         f"to the TEXT of {rules.name}, never executed)",
         "names the sibling tape",
         lambda: _range_sibling_static({rules.name: rules.read_text(encoding="utf-8")
                                        + wall_text})),
        ("SIBLING-WALL PLANT, leg (h) (a gate in trap_card() reading the sibling tape off "
         "disk: `_p = pd.read_parquet(TAPE_RANGES_DIR)` — no key, alias or helper is named, "
         "so leg (c) cannot see it)",
         "names the sibling tape",
         (lambda: _range_sibling_ast(_range_plant_in(
             od_src, "trap_card", "_p = pd.read_parquet(TAPE_RANGES_DIR)")))
         if _range_plant_in(od_src, "trap_card", "_p = pd.read_parquet(TAPE_RANGES_DIR)")
         else None),
        ("CONTAINMENT PLANT (range_layer's `except Exception` narrowed to ZeroDivisionError, "
         "in a mutant built from source)",
         "range_layer RAISED",
         (lambda: _range_containment(_range_mutant(narrow))[0]) if narrow else None),
        # ── the round-1 review's plants (2026-09-22). Each was GREEN on every leg before
        # the repair that its must-string names.
        *[(f"BYPASS PLANT {tag} (the heat-damping gate reached by {how}; leg (c))", must,
           ast_plant(_range_plant_bypass(od_src, imp, get)))
          for tag, how, imp, get, must in od_bypass],
        ("BYPASS PLANT OD-5 (`from oracle_daily import RNG as _Q` inside trap_card(): the "
         "imported NAME is RNG, only its asname was compared; leg (c))",
         f"imports the NAME `{RANGE_ALIAS}`", ast_plant(od5)),
        ("STASH PLANT OD-9 (a module-level `_MEMO` that range_layer fills and build_view reads "
         "back by 'top'/'bottom'/'atr', damping heat within 1 ATR of a boundary — the review's "
         "side channel, verbatim; leg (c))",
         "stores into module-level state", ast_plant(od9)),
        (f"STASH PLANT OD-9b, RUN (the same memo, the gate keyed on its presence alone; "
         f"leg (d) over the first {RANGE_MUTANT_ROSTER} roster rows — with one shared module "
         f"the stubbed runs read REAL's memo and the three runs agreed)",
         "decision side moved",
         (lambda: _range_behaviour(od9b, n_roster=RANGE_MUTANT_ROSTER)[0]) if od9b else None),
        ("RUN() PLANT OD-10 (the written sibling tape read back in run(), just before the D-7 "
         "record, heat doubled within 1 ATR of a boundary; leg (h) — run() was exempt)",
         "outside log() and its return dict",
         (lambda: _range_sibling_ast(od10)) if od10 else None),
        (f"RUN() PLANT OD-10, RUN (the same, through leg (d), which now runs run() itself; "
         f"first {RANGE_MUTANT_ROSTER} roster rows — the HOT day's filed heat doubles)",
         "decision side moved",
         (lambda: _range_behaviour(od10, n_roster=RANGE_MUTANT_ROSTER)[0]) if od10 else None),
        ("RUN() PLANT OD-11 (run() globs TAPE_RANGES_DIR for yesterday's sibling tape; leg (h))",
         "run() names the sibling tape",
         ast_plant_h(_range_plant_in(od_src, RANGE_SIBLING_CALLER,
                                     "_y = sorted(TAPE_RANGES_DIR.glob('*.parquet'))"))),
        ("RUN() PLANT (`_p = pd.read_parquet(TAPE_RANGES_DIR)` in run(), the plant that is red "
         "in trap_card(); leg (h))",
         "run() names the sibling tape",
         ast_plant_h(_range_plant_in(od_src, RANGE_SIBLING_CALLER,
                                     "_p = pd.read_parquet(TAPE_RANGES_DIR)"))),
        (f"LANE-PATH PLANT OD-12 (trap_card() globs `{derived}` — no sibling token spelt; "
         f"leg (h))",
         "names the lane path `TAPE_DIR`",
         ast_plant_h(_range_plant_in(od_src, "trap_card",
                                     f"_rp = sorted({derived}.glob('*.parquet'))"))),
        ("LANE-PATH PLANT OD-13 (trap_card() rglobs TAPE_DIR.parent for "
         "'oracle_tape_r*.parquet'; leg (h))",
         "names the lane path `TAPE_DIR`",
         ast_plant_h(_range_plant_in(od_src, "trap_card",
                                     "_rp = sorted(TAPE_DIR.parent.rglob('oracle_tape_r*.parquet'))"))),
        (f"SEEDED PLANT, RUN (build_view damps heat whenever `{derived}` holds a file; leg (d), "
         f"first {RANGE_MUTANT_ROSTER} roster rows — the per-run seeds are what move it: "
         f"REAL's directory is empty, EMPTY's and HOT's hold a 'yesterday')",
         "decision side moved",
         (lambda: _range_behaviour(seeded_src, n_roster=RANGE_MUTANT_ROSTER)[0])
         if seeded_src else None),
        *[(f"DECISION-AST PLANT {tag} ({how}, lazy, appended to the TEXT of {rel}; leg (b))",
           must, dec_judge(rel, text)) for tag, rel, how, text, must in dec_plants],
        (f"SIBLING-WALL PLANT DEC-14 (`pd.read_parquet(pathlib.Path('research_outputs/oracle') / "
         f"('tape' + '_ranges'))` appended to the TEXT of {rules.name}; leg (h))",
         "names the sibling tape",
         lambda: _range_sibling_static({rules.name: rules.read_text(encoding="utf-8") + lazy
                                        + "    import pathlib, pandas as pd\n"
                                          "    return pd.read_parquet(pathlib.Path("
                                          "'research_outputs/oracle') / ('tape' + '_ranges'))\n"})),
        (f"SCAN-SET PLANT (a COPY of analytics/ shadowing the real package in a clean "
         f"subprocess, `import {ORACLE_RANGE_MODULE} as _RF` appended to its levels.py — "
         f"analytics.levels was in no scan set; legs (b) and (e))",
         "analytics/levels.py imports the range machine", shadow_levels),
        # ── the round-2 review's plants (2026-09-22). Each was GREEN on every static leg
        # before the repair its must-string names; the RUN plants were green on leg (d)
        # too, because the stubs replace range_layer only.
        *[(f"BYPASS PLANT {tag} (the heat-damping gate, the machine FOUND by {how}; leg (c))",
           must, ast_plant(_range_plant_bypass(od_src, imp, getter.format(get))))
          for tag, how, imp, get, must in od_found],
        (f"BYPASS PLANT OD-E (a LAZY `import {reexp} as _T` in build_view, the machine read off "
         f"the re-exporter; leg (c))",
         "the reverse import index", ast_plant(od_e)),
        ("API PLANT (OD-A judged on the fence that does not care how the module was found: "
         "`_m.run_v2`, `_m.tape_from_klines`, `_m.PINS_V2` outside range_layer(); leg (c))",
         "a name the range machine defines", ast_plant(od_a)),
        ("READER PLANT OD-G (render_html, an allow-listed reader, runs RNG itself and flips "
         "REGISTER['TARGET_BUCKET_ATR'] through a local alias — the filed D-7 basis moved; "
         "leg (c))",
         f"names the machine alias `{RANGE_ALIAS}`", ast_plant(od_g)),
        ("STASH PLANT OD-G2 (the same alias write alone, keyed on the view's own 'range': "
         "`_q = REGISTER[...]; _q['value'] = ...` in render_html; leg (c))",
         "stores into module-level state", ast_plant(od_g2)),
        ("RUN() PLANT OD-H (`log` rebound in run(): the sanctioned log(f'{rtape_p} ...') feeds "
         "the sibling path to a gate that reads it; leg (h))",
         "rebinds `log`", ast_plant_h(od_h)),
        ("LANE-PATH PLANT OD-F (grid_toll() cuts the sibling directory out of "
         "str(GRID_PARQUET) and doubles the toll near a boundary — no sibling token, no "
         "'research_outputs', no walk; leg (h))",
         "may only be joined", ast_plant_h(od_f)),
        ("WINDOW PLANT (REGISTER['RANGE_WINDOW_BARS'] typed as 1700: the value check alone "
         "compared the machine's constant with itself and passed)",
         "never typed", (lambda: _range_window_bind(od_win)) if od_win else None),
        (f"TRIPWIRE PLANT OD-A, RUN (the machine found through `from sys import modules`, "
         f"RUN through leg (d) over the first {RANGE_MUTANT_ROSTER} roster rows — the "
         f"comparison cancels it, the machine tripwire does not)",
         "MACHINE TRIPWIRE",
         (lambda: _range_behaviour(od_a, n_roster=RANGE_MUTANT_ROSTER)[0]) if od_a else None),
        (f"TRIPWIRE PLANT OD-F, RUN (the grid-path cut, RUN: GRID_PARQUET now points into the "
         f"box, the cut lands on the box's seeded sibling directory; first "
         f"{RANGE_MUTANT_ROSTER} roster rows)",
         "READ TRIPWIRE",
         (lambda: _range_behaviour(od_f, n_roster=RANGE_MUTANT_ROSTER)[0]) if od_f else None),
        (f"TRIPWIRE PLANT DEC-H, RUN (analytics.levels swapped for one whose lines_in_sand() "
         f"reads the LIVE sibling directory by `Path(__file__).resolve().parents[1] / "
         f"'research_outputs' / 'oracle' / ('tape' + '_ranges')` — no static leg can fence "
         f"a decision module's own path; first {RANGE_MUTANT_ROSTER} roster rows)",
         "READ TRIPWIRE", swapped_run(dec_h)),
        (f"TRIPWIRE PLANT DEC-E2, RUN (analytics.levels swapped for one whose lines_in_sand() "
         f"runs the machine off its CALLER's frame — build_view's RNG and h4 — and empties "
         f"the lines within 1 ATR of a boundary; first {RANGE_MUTANT_ROSTER} roster rows)",
         "MACHINE TRIPWIRE", swapped_run(dec_e2)),
        ("SHIM PLANT (a NEW analytics/_shim.py in a shadow copy re-exporting the machine, "
         "imported only INSIDE a function of the shadow levels.py — in no closure, so in no "
         "scan set; legs (b) and (h) by the static import walk)",
         "analytics/_shim.py imports the range machine", shim_plant),
    ]

    def _break() -> tuple[bool, str]:
        green, out = False, []
        for name, must, judge in plants:
            if judge is None:
                green = True
                out.append(f"{name} -> GREEN: the plant could not be planted")
                continue
            try:
                bad = judge()
            except Exception as e:                 # a plant that raises proved nothing
                green = True
                out.append(f"{name} -> VOID: the judge RAISED {e.__class__.__name__}: "
                           f"{str(e)[:200]}")
                continue
            hits = [b for b in bad if must in b]
            if hits:
                rest = [b for b in bad if must not in b]
                out.append(f"{name} -> RED: {hits[0]}"
                           + (f" (+{len(hits) - 1} more of its kind)" if len(hits) > 1 else "")
                           + (f" [and {len(rest)} other finding(s), first: {rest[0]}]" if rest else ""))
            else:
                green = True
                out.append(f"{name} -> " + ("GREEN" if not bad else
                           f"RED FOR THE WRONG REASON (no finding says {must!r}; first: {bad[0]})"))
        return green, " ‖ ".join(out)

    def _real() -> tuple[bool, str]:
        bad_sha, sha = _range_sha()
        bad_clo, clo = _range_closures()
        bad_ast, a = _range_ast()
        bad_run, run = _range_behaviour()
        bad_tape = _range_tape_names()
        bad_con, con = _range_containment()
        bad_watch = _range_watch_membership()
        bad = bad_sha + bad_clo + bad_ast + bad_run + bad_tape + bad_con + bad_watch
        # A-OR1-1's four legs. (e) rode inside _range_closures (one subprocess per
        # module); (f) (g) (h) read the edition's two tapes and the tapes leg (d) wrote.
        files = run["files"]["REAL"]
        bad += _range_main_tape({f"artifact set {DATE}'s D-4 tape": TAPE,
                                 "the D-4 tape leg (d) wrote": files["tape"]})
        empty_df, empty_schema = _range_sibling_empty_day()
        bad += _range_sibling({
            f"artifact set {DATE}'s sibling tape": (
                TAPE_RANGES, pq.read_schema(TAPE_RANGES_PATH) if TAPE_RANGES_PATH else None),
            "the sibling tape leg (d) wrote": (files["sibling"], files["sibling_schema"]),
            "the all-None day, through write_range_tape": (empty_df, empty_schema)},
            OD.REGISTER["ROSTER"]["value"])
        wall_sources = clo["sources"]           # (b)'s scan set, derived from the closures
        bad += _range_sibling_static(wall_sources) + _range_sibling_ast()
        if getattr(OD.RNG, "__name__", None) != ORACLE_RANGE_MODULE:
            bad.append(f"oracle_daily.RNG is {getattr(OD.RNG, '__name__', None)!r}, not "
                       f"{ORACLE_RANGE_MODULE} — the Oracle is not running its own machine")
        want = set(OD.range_empty())
        if run["keys"] and set(run["keys"]) != want:
            bad.append(f"range_empty()'s key set is not {ORACLE_RANGE_MODULE}.snapshot()'s + "
                       f"'error': {sorted(set(run['keys']) ^ want)}")
        stale = [k for k in RANGE_ONLY_KEYS if k not in want]
        if stale:
            bad.append(f"RANGE_ONLY_KEYS names {stale}, which the snapshot no longer carries — "
                       f"the by-value scan is hunting stale names")
        unruled = [k for k in ("RANGE_LENS", "RANGE_WATCH_ATR") if OD.REGISTER[k]["ruled"]]
        if unruled:
            bad.append(f"{unruled} read 'ruled': True — they are the contract's [VETO] defaults "
                       f"and no ruling is on record")
        if HTML is not None:
            veto = _sec(HTML, SEC_COLOPHON)       # the appendix is its <h3> since STEP F
            gone = [k for k in ("RANGE_LENS", "RANGE_WATCH_ATR") if f"<code>{k}</code>" not in veto]
            if gone:
                bad.append(f"artifact set {DATE}: the rendered [VETO] appendix does not list {gone}")
            if not _sec(HTML, SEC_TIDE) or "EDGE WATCH" not in _sec(HTML, SEC_TIDE):
                bad.append(f"artifact set {DATE}: no Tide Tables section carrying EDGE WATCH")
        # the window IMPORTED, proved on the source (the AST node IS RNG.V2_WINDOW_BARS),
        # and the value it evaluates to is the machine's — two checks, not one tautology
        bad += _range_window_bind()
        if OD.REGISTER["RANGE_WINDOW_BARS"]["value"] != OD.RNG.V2_WINDOW_BARS:
            bad.append("REGISTER['RANGE_WINDOW_BARS'] is not the machine's V2_WINDOW_BARS")
        if bad:
            return False, "; ".join(bad[:6]) + (f" (+{len(bad) - 6} more)" if len(bad) > 6 else "")
        new_cols = [c for c in OD.RANGE_TAPE_COLS if c.startswith("range_")]
        return True, (
            f"(a) scripts/posture_engine.py sha256 {sha} == the pinned constant: byte-unchanged. "
            f"(b) component-wise, in clean subprocesses: no {list(RANGE_BANNED_IN_DECISION)} "
            f"component in the closure of "
            + ", ".join(f"{m} ({clo['sizes'][m]})" for m in RANGE_DECISION_MODULES)
            + f"; the Oracle's machine {ORACLE_RANGE_MODULE}'s own closure "
            f"({clo['sizes'][ORACLE_RANGE_MODULE]} modules) holds none of "
            f"{list(RANGE_BANNED_IN_MACHINE)}; and over {clo['static']} decision-side source "
            f"files — the {clo['fixed']} fixed ones (every engine module but the machine, "
            f"posture_engine.py, every tierc*_rules.py) PLUS the {len(clo['derived'])} more that "
            f"oracle_daily and the decision modules load or name in an import at any depth "
            f"({', '.join(clo['derived'])}; by the static import walk alone: "
            f"{', '.join(clo['followed']) or 'none'}), read, never executed — no import line "
            f"names a range machine OR A WRAPPER RE-EXPORTING ONE (rangefinder_twin, "
            f"rangefinder_census), and, parsed as CODE, no import at any depth meets "
            f"{list(RANGE_BANNED_IN_DECISION)} or carries `rangefinder` or loads one of the "
            f"{len(clo['index']['tainted'])} modules of the reverse import index (of "
            f"{len(clo['index']['modules'])} under {'/, '.join(RANGE_INDEX_DIRS)}/), no import of "
            f"the dynamic-import machinery nor `from sys import`, no "
            f"{list(RANGE_DECISION_DYNAMIC)} (but {dict(RANGE_DECISION_DYNAMIC_OK)}), no "
            f"{['.' + x for x in RANGE_DECISION_ATTRS]}, no attribute carrying `rangefinder` or "
            f"named {RANGE_ALIAS}, no string naming {list(RANGE_DECISION_STRINGS)} or equal to "
            f"{RANGE_ALIAS!r}. "
            f"(c) AST of oracle_daily.py ({a['functions']} functions): `{RANGE_ALIAS}` is bound "
            f"once, by `import {ORACLE_RANGE_MODULE} as {RANGE_ALIAS}`, and reachable no other "
            f"way — none of {len(RANGE_DYNAMIC_NAMES)} dynamic-import names, none of "
            f"{len(RANGE_DYNAMIC_ATTRS)} module / frame / namespace attributes (.modules, "
            f".__dict__, ._getframe, .f_globals, .get_objects, .__file__ ...), no `from sys "
            f"import`, no import of oracle_daily or of the name {RANGE_ALIAS}, no "
            f"`.{RANGE_ALIAS}`, no import of a module in the reverse import index but the "
            f"sanctioned binding and {dict(RANGE_OD_IMPORT_OK)}, no string naming the machine "
            f"outside REGISTER's sources; `{RANGE_ALIAS}` and the {len(_range_api_names())} names "
            f"the machine defines (attribute or string) appear ONLY in {RANGE_PRODUCER}() and "
            f"REGISTER's {RANGE_ALIAS}.{RANGE_REGISTER_IMPORTS[0]} (but {dict(RANGE_API_OK)}); no "
            f"function stores into module-level state, directly or through a local alias; "
            f"the key {RANGE_KEY!r}, the {len(RANGE_ONLY_KEYS)} snapshot-only keys, the alias and the "
            f"{len(RANGE_HELPERS)} layer functions are mentioned ONLY inside {list(RANGE_READERS)}, "
            f"plus ONE statement of {RANGE_WRITER}() (line {a['write_line']}: `<asset>[{RANGE_KEY!r}] "
            f"= {RANGE_PRODUCER}(h4)`) and REGISTER's import of the window; zero mentions in "
            f"{list(RANGE_NAMED_GATES) + [RANGE_MAIN_TAPE_WRITER]}, each of which exists; the key "
            f"is really read ({', '.join(f'{k} x{v}' for k, v in a['reads'].items())}). "
            f"(d) oracle_daily.run() ITSELF, three times over the {run['assets']}-symbol roster, "
            f"each in a fresh module, every directory it writes redirected into a throwaway tree "
            f"seeded differently per run, the roots it reads from ({', '.join(RANGE_RUN_READS)}) "
            f"copied into it, one frozen clock — stubbed EMPTY, stubbed HOT (every "
            f"symbol ON a boundary, breach pending) and REAL last ({run['live']} live macro "
            f"range(s), {run['pending']} pending, {run['failed']} unavailable): "
            f"{run['fields']} decision-side fields identical across all three — sort "
            f"order, heat, station, card, lines, clusters, fired events, R1, the whole D-7 "
            f"document, the whole D-4 tape ({len(OD.TAPE_COLS)} columns) and its parquet schema, "
            f"and {len(run['sections'])} rendered sections (every one but the Tide Tables, the "
            f"Board with its {run['assets']} RANGE cells cut out) — while the {len(new_cols)} "
            f"range columns of the SIBLING tape under HOT differ from both other runs and every "
            f"HOT asset carries the stub, so the stubs were live; the sibling tape's parquet "
            f"schema is the same on all three days (EMPTY is the all-None one). "
            f"The view is byte-for-byte the same object after {' and '.join(RANGE_VIEW_READERS)} "
            f"as before each, so no allow-listed reader re-ordered the Board under the two tapes "
            f"and the D-7 record, all of which run() writes AFTER the render. "
            f"EVERY RUN WATCHED: the machine was entered {run['watch']['REAL']['entries']} time(s) "
            f"from outside it in REAL, every one by that run's own range_layer(), and "
            f"{run['watch']['EMPTY']['entries']} / {run['watch']['HOT']['entries']} time(s) in "
            f"EMPTY / HOT, where range_layer is stubbed; of {run['watch']['REAL']['watched']} / "
            f"{run['watch']['EMPTY']['watched']} / {run['watch']['HOT']['watched']} paths read, "
            f"listed or opened (REAL / EMPTY / HOT), none was under the live sibling directory, "
            f"no listing touched a run's own, and the only sibling-tape read was "
            f"write_range_tape()'s read-back of the file it had just written. "
            f"THE NUMBERS: every printed range is self-consistent against the snapshot's own "
            f"close and atr — bottom < mid < top, mid = (top+bottom)/2, pos_pct = "
            f"100*(close-bottom)/(top-bottom), dist_atr = min(|top-close|,|close-bottom|)/atr, "
            f"nearest_side the boundary that min() picked — and the SIBLING tape records those "
            f"same values FIELD FOR FIELD, with range_top above range_bottom on every row that "
            f"carries a box; range_watch's membership is pinned at RANGE_WATCH_ATR = "
            f"{OD.REGISTER['RANGE_WATCH_ATR']['value']} itself (limit-eps and the limit IN, "
            f"limit+eps out, a pending breach with no measurable distance on the list and "
            f"last). SELF-CONSISTENCY ONLY: a wrong atr or a wrong close is invisible to it. "
            f"(e) oracle_daily's closure, in a clean subprocess ({clo['sizes']['oracle_daily']} "
            f"modules), CONTAINS {ORACLE_RANGE_MODULE} and NOT {RANGE_MACHINE} (TIER-C10's "
            f"machine of record, byte-frozen under engine/, A-OR1-1 iv), and of its "
            f"{clo['local']} repo-local modules oracle_daily alone imports {ORACLE_RANGE_MODULE}. "
            f"(f) the D-4 tape is TC4's untouched schema: oracle_daily.TAPE_COLS, artifact set "
            f"{DATE}'s D-4 tape and the one leg (d) wrote are each EXACTLY the "
            f"{len(PRE_OR1_TAPE_COLS)} pre-OR-1 names in the pre-OR-1 order — no range column. "
            f"(g) the sibling tape (research_outputs/oracle/tape_ranges/) carries the "
            f"{len(OD.RANGE_TAPE_KEYS)} D-4 row keys and the {len(new_cols)} range fields, each at "
            f"its pinned parquet type (5 double, 3 string, never null), one row per roster symbol "
            f"({len(OD.REGISTER['ROSTER']['value'])}) — on artifact set {DATE}'s, on leg (d)'s and "
            f"on an all-None day written through write_range_tape. "
            f"(h) no gate reads it: none of {list(RANGE_SIBLING_TOKENS)} nor "
            f"`research_outputs/oracle` (case-blind) in the text of the {len(wall_sources)} "
            f"decision-side files; inside oracle_daily.py its names sit only in their own "
            f"definitions and {RANGE_SIBLING_WRITER}(), and {RANGE_SIBLING_CALLER}() calls that "
            f"once and hands the result to {RANGE_SIBLING_LOG}() — its own parameter, rebound "
            f"nowhere — and its return dict only; the lane's paths are named only where "
            f"RANGE_LANE_PATHS allows and only joined, tested, created, globbed, read or quoted "
            f"in a raise, no code walks a path, only {len(RANGE_DISK_READERS)} functions read the "
            f"disk and no reader is imported by name, and 'research_outputs' is spelt only in "
            f"the lane's path definitions and REGISTER's sources. "
            f"No D-7 key carries the token `range`. The {len(new_cols)} sibling tape names "
            f"({', '.join(new_cols)}) clear the {len(OD.BANNED_CALIBRATION_KEYS)}-term banned "
            f"vocabulary and are on artifact set {DATE}'s sibling tape. range_layer contains a "
            f"fault (EMPTY frame -> {con.get('an EMPTY frame')!r}) and refuses a frame off its lens "
            f"(1h -> {con.get('a 1h frame')!r}). RANGE_LENS and RANGE_WATCH_ATR are 'ruled': False "
            f"and print in the rendered [VETO] appendix; RANGE_WINDOW_BARS = "
            f"{OD.REGISTER['RANGE_WINDOW_BARS']['value']} is the machine's own constant, imported: "
            f"its REGISTER value is the AST node `{RANGE_ALIAS}.{RANGE_REGISTER_IMPORTS[0]}`, and "
            f"it evaluates to {ORACLE_RANGE_MODULE}.{RANGE_REGISTER_IMPORTS[0]}.")

    prove("F-BR-14", "THE RANGE LAYER RENDERS, NEVER RULES — posture_engine.py byte-unchanged; "
                     "the range object in render + sibling tape only, never in a gate path; a "
                     "planted gate read must go red",
          _break, _real)


# ═════════════ F-BR-15 · THE DAILY ORACLE — typeset, semantics untouched (OR-1 STEP F)
#
# WHAT THIS GUARDS. STEP F re-set the page as a newspaper: "semantics untouched,
# template only". The contract names three properties and this fixture holds all
# three on the edition under test — EVERY mantle strip has its caption, verbatim; the
# EIGHT sections are present in the operator's order and nothing else is an <h2>; the
# Colophon carries the DISPLAY-ONLY fragment — and then the things a typesetting can
# break without any number moving:
#   · THE INKS. Paper, ink and ONE red, the serif stack, no remnant of the dark page,
#     no theme switch; and the red under an ALARM selector only (the band, WIRE DOWN,
#     STALE TRIGGER, the range layer's PENDING). A red posture word is an alarm that
#     cries every morning. The Spaghetti's hues are data and stay OUT of the red band.
#   · THE BAND. "LATE EDITION — N of R rows on a stale wire (oldest <as-of>)" (OR-2 R-1;
#     until then "LATE EDITION — wire stale since <as-of>") directly under the masthead
#     WHEN AND ONLY WHEN A2-7's rule fires for some row. Driven, not assumed: one view
#     printed five minutes INSIDE the limit for its OLDEST row and five minutes PAST it
#     for its NEWEST (every row stale: R of R). And the phrase
#     nowhere else in the page's text: the on-demand wrapper reads "banner UP" off it
#     (oracle_wrapper BANNER_MARKERS), so a caption or a [VETO] source that spelt it
#     would raise a false alarm in the log every day.
#   · NO WALL CLOCK in the Front Page or The Watch. F-BR-6 renders twice a few
#     milliseconds apart and cannot see a stamp with minute resolution; here the
#     module's clock is pushed 400 days on and both sections must not move a byte.
#   · THE MASTHEAD. The contract's ears, the word per A-OR1-1 vii (below); an un-numbered
#     render says 'No. —'; render_html still takes (view, date_str, canon_sha) — the
#     wrapper's per-edition self-check calls it that way — and run() is what numbers an
#     edition and what times it.
#   · THE EDITION'S WORD — AMENDMENT A-OR1-1 clause vii (operator, 2026-09-22), verbatim:
#     "Edition word follows verb and hour: full before 12:00 BA = Morning, after =
#     Evening; refresh = Refresh. A paper printed at night does not call itself the
#     morning's." TWO LEGS. (i) THE EDITION UNDER TEST carries its own evidence: exactly
#     one print line in the Colophon ('Printed <YYYY-MM-DD HH:MM> Buenos Aires (<word>
#     Edition: <verb>, slot <slot> · A-OR1-1 vii)'), whose word is vii's for its verb
#     and its hour, and the ear says that word; when the wrapper's selfcheck log holds a
#     row carrying the page's sha256, that row's slot is the print line's and it was
#     written no earlier than the printed minute. (ii) THE LAW ITSELF, over a table of
#     synthetic calls AND real renders (TS_VII_TABLE: 07:00, 11:59, 12:00, 19:17 full,
#     22:26 on-demand-full, 09:00 refresh, 20:00 on-demand-refresh), the print time
#     handed in UTC and the PROCESS's local zone forced to UTC for the length of the leg,
#     so a module that reads the hour in the machine's zone — or reads it off the handed
#     datetime unconverted — says the wrong word or prints the wrong minute; a naive
#     print time is refused. And a render handed no print time is UNTIMED: no print line,
#     and its ear reads vii at the view's as-of bar (the 'plain' render, time-aware).
#   · THE HEADLINE. "Business possible" is earned by a FRESH trigger only. The posture
#     engine's own register calls TRIGGERED without its age "MISLEADING on a Board whose
#     word the operator reads as 'the entry alert is live now'", and the headline is
#     read before any row: on the day this was built all five TRIGGERED rows were STALE
#     (19 to 212 bars), and the first draft of the headline called them business.
#   · THE EDITION COUNT. Dates on the TAPE, this edition's included: robust to a render
#     leaving briefs/oracle (the operator moved 2026-09-21's to his Desktop).
#   · THE TWO ORGANS WITH NO SECTION OF THEIR OWN are not lost: the Spaghetti is an
#     <h3> inside The Watch, the [VETO] appendix an <h3> inside the Colophon.
#   · THE STRIP'S BAR COUNT IS TYPED ONCE: REGISTER['MANTLE_BARS']. The caption below
#     is COPIED from the queue file, number and all — a page that prints whatever the
#     module under test says proves nothing — and the register must agree with it.
#
# CONSEQUENCE, stated (the F-BR-16 rule, same reason): this suite audits the NEWEST
# artifact set on disk. An edition printed BEFORE STEP F has the old headings, no
# caption and the dark inks, so it is RED here — and in F-BR-14's appendix lookup,
# which now reads the Colophon — until one edition is printed by the new template.
# On purpose: a green here about an old page would be a statement about another page.
# LIKEWISE vii's leg (i): run bare against an edition printed before A-OR1-1 vii (the
# 2026-09-21 set: printed 22:26 Buenos Aires, its ear says 'Morning Edition', and it
# carries no print line) it is RED on exactly that — no print line, the selfcheck row
# and the file's mtime named as witnesses — on purpose, until an edition is printed by
# this code. That edition is REPORTED, never rewritten. The sandbox suite prints one
# first.
#
# WHAT IT DOES NOT PROVE: that no number moved. That is EVERY OTHER fixture in this
# file staying green on a fresh render (F-BR-15 is this one; F-BR-16 is the one that
# says the edition under test was printed from the CURRENT roster), and the
# block-by-block old-template/new-template comparison in the build document
# (or1_transcripts/semantic_diff.py, STEP F over 7a1df59 — its footer declaration
# predates A-OR1-1 vii — and or1_transcripts/semantic_diff_vii.py, vii's ear word and
# Colophon line over 3d55988, byte for byte); nor that the page is handsome.

TS_CAPTION = ("rows = threads, rod 5000 top → hem 9 bottom · columns = last 96 bars · "
              "hue = thread above/below price in ATR · dark pinch = knot · hole = unwoven")
TS_PAPER, TS_INK, TS_RED = "#F4ECD8", "#1A1A1A", "#B3261E"
TS_SERIF = '"Iowan Old Style", Palatino, Georgia, serif'
TS_TITLE = "THE DAILY ORACLE"
TS_EAR_LEFT = re.compile(r"^Vol\. I · No\. (\d+|—)$")
TS_EAR_RIGHT = re.compile(r"^Buenos Aires · (\d{4}-\d{2}-\d{2}) · (Morning|Evening|Refresh) "
                          r"Edition · Price: one toll$")
# A-OR1-1 vii. "BA" is PINNED HERE, not read off oracle_daily.ZONE: a module whose zone
# drifted would otherwise be judged in its own drifted zone.
TS_ZONE = "America/Argentina/Buenos_Aires"
TS_VII = ("Edition word follows verb and hour: full before 12:00 BA = Morning, after = "
          "Evening; refresh = Refresh. A paper printed at night does not call itself the "
          "morning's.")
# The Colophon's print line, as the operator READS it (_page_text of the <footer>).
TS_PRINT_LINE = re.compile(r"Printed (\d{4}-\d{2}-\d{2}) (\d{2}):(\d{2}) Buenos Aires "
                           r"\((Morning|Evening|Refresh) Edition: (full|refresh), slot (\S+) "
                           r"· A-OR1-1 vii\)")
# Leg (ii): (slot, Buenos Aires wall clock, the word vii gives) — the words TYPED, not
# computed, so the table pins the law and not whatever the module says. 12:00 is the
# stated boundary: noon is not "before 12:00".
TS_VII_DAY = "2030-01-03"
TS_VII_TABLE = (("full", "07:00", "Morning"), ("full", "11:59", "Morning"),
                ("full", "12:00", "Evening"), ("full", "19:17", "Evening"),
                ("on-demand-full", "22:26", "Evening"), ("refresh", "09:00", "Refresh"),
                ("on-demand-refresh", "20:00", "Refresh"))
# the process's local zone for the length of leg (ii): NOT Buenos Aires, so a reading in
# the machine's zone shows (19:17 Buenos Aires is 22:17 there, 22:26 is 01:26 next day)
TS_MACHINE_ZONE = "UTC"
TS_BAND = "LATE EDITION"
# OR-2 R-1, verbatim from the queue (operator 2026-09-22): "LATE EDITION — N of R rows on
# a stale wire (oldest <as-of>)". Superseded OR-1 STEP F's "LATE EDITION — wire stale
# since {as_of}", which read the hottest asset's bar alone (OR1-a).
TS_BAND_HEAD = "LATE EDITION — {n} of {r} rows on a stale wire (oldest {as_of})"
TS_BAND_DETAIL = "The top-up may not have run"
# A2-7 verbatim (operator, ratified 2026-08-16): "older than 2 lens periods at render
# time". PINNED HERE, not read off the module, for the same reason the band's words are
# pinned above: the fixture must fail when the module's number drifts. STALE_LENS_PERIODS
# is a bare module constant, not a REGISTER row, so it does not surface in the rendered
# [VETO] appendix either; raised to 2000 the limit becomes 333 days, the band can never
# fire, the operator is never again told the wire is stale — and before this line the
# whole suite stayed green, because _ts_renders recomputes the limit FROM that constant.
TS_LENS_PERIODS = 2
TS_FRAGMENT = "DISPLAY-ONLY"
# every colour the pre-STEP-F page typed: its style block, its SVG, its stale band
TS_DARK_REMNANTS = ("#14120f", "#e9dcc3", "#8a7f72", "#2b2620", "#55949b", "#c67139",
                    "#a3b581", "#181512", "#0e0c0a", "#5b5148", "rgba(198,113,57")
TS_ALARM_CLASSES = (".stale", ".pend", ".wire")
TS_RED_HUES = (20, 340)          # a hue below 20 or above 340 reads as red on paper
TS_MARGIN_MS = 5 * 60_000        # how far inside / past A2-7's limit the band is driven
TS_CLOCK_SHIFT_DAYS = 400
_TS_CANVAS = re.compile(r'<canvas[^>]*data-payload="([^"]+)"[^>]*>')


def _page_text(fragment: str) -> str:
    """What the operator READS: style, script and comments out, tags out, entities
    back, whitespace collapsed (the wrapper's banner_state reads a page the same way)."""
    import html as _h
    t = re.sub(r"(?is)<(style|script)\b.*?</\1\s*>|<!--.*?-->", " ", fragment)
    return re.sub(r"\s+", " ", _h.unescape(re.sub(r"(?s)<[^>]+>", " ", t))).strip()


def _ts_static(doc: str, date: str | None) -> tuple[list[str], dict]:
    """The properties of ONE rendered page."""
    bad: list[str] = []
    # ── the eight sections, bare, in the contract's order ─────────────────────
    heads = re.findall(r"(?s)<h2\b([^>]*)>(.*?)</h2>", doc)
    dressed = [t for a, t in heads if a.strip()]
    if dressed:
        bad.append(f"sections: {len(dressed)} <h2> carry an attribute (first {dressed[0][:30]!r}) "
                   f"— every selector splits the page on the literal '<h2>'")
    titles = [_page_text(t) for _a, t in heads]
    if len(titles) != len(SECTIONS):
        bad.append(f"sections: {len(titles)} <h2> heading(s) on the page, want exactly the "
                   f"contract's {len(SECTIONS)}: {[t[:24] for t in titles]}")
    for i, want in enumerate(SECTIONS):
        if i < len(titles) and not titles[i].lower().startswith(want.lower()):
            bad.append(f"section order: heading {i + 1} reads {titles[i][:40]!r}; the contract's "
                       f"order puts {want!r} there")
    # ── every mantle strip carries the caption ───────────────────────────────
    canv = list(_TS_CANVAS.finditer(doc))
    if not canv:
        bad.append("caption: no mantle strip on the page — nothing to caption; fail closed")
    for k, c in enumerate(canv):
        end = canv[k + 1].start() if k + 1 < len(canv) else len(doc)
        region = re.split(r"<h[23]\b", doc[c.end():end])[0]
        n = _page_text(region).count(TS_CAPTION)
        if n != 1:
            bad.append(f"caption: the strip {c.group(1)} carries the contract's caption {n} "
                       f"time(s), want exactly 1")
    # ── the colophon, and the two organs with no section of their own ─────────
    col = _sec(doc, SEC_COLOPHON)
    foot = re.search(r"(?s)<footer>(.*?)</footer>", col)
    if not foot:
        bad.append("colophon: the <footer> is not inside the Colophon section")
    else:
        ftxt = _page_text(foot.group(1))
        if TS_FRAGMENT not in ftxt:
            bad.append(f"colophon: the {TS_FRAGMENT} fragment is missing from the Colophon's "
                       f"provenance block")
        if "as-of bar" not in ftxt:
            bad.append("colophon: the as-of stamp is missing from the provenance block")
    if not re.search(r"<h3>\s*Appendix", col):
        bad.append("colophon: the [VETO] appendix sub-block (<h3>Appendix) is missing — it has "
                   "no section of its own in the eight and must not be lost")
    # ── the footnote COUNTS the table it stands over ─────────────────────────
    # It used to assert "each is DEFERRED-TO-BR2" while 5 of the 14 rows two lines
    # below printed a bare [VETO] — this build's own defaults, waiting on THIS
    # operator, not on BR-2. The sentence is the only guidance the page gives about
    # what the table means, so the two integers in it are pinned to the two chip
    # counts, and their sum to the row count.
    tbl = re.search(r'(?s)<table class="veto">(.*?)</table>', col)
    # tempered: the capture may not swallow an earlier </p> on its way to the table
    note = re.search(r'(?s)<p class="small muted">((?:(?!</p>).)*)</p>\s*<table class="veto">',
                     col)
    if not tbl or not note:
        bad.append("colophon: the [VETO] footnote and its table are not both there, one "
                   "directly above the other — fail closed")
    else:
        n_rows = len(re.findall(r"<tr><td><code>", tbl.group(1)))
        n_def = tbl.group(1).count(">DEFERRED-TO-BR2<")
        n_vet = tbl.group(1).count(">[VETO]<")
        txt = _page_text(note.group(1))
        md = re.search(r"(\d+) of the (\d+) rows below are DEFERRED-TO-BR2", txt)
        mv = re.search(r"(\d+) carry a bare \[VETO\]", txt)
        if not md or not mv:
            bad.append(f"colophon: the [VETO] footnote does not COUNT its table — it reads "
                       f"{txt[:120]!r}, and the table below it carries {n_def} "
                       f"DEFERRED-TO-BR2 and {n_vet} bare [VETO] chip(s) over {n_rows} row(s)")
        elif (int(md.group(1)), int(md.group(2)), int(mv.group(1))) != (n_def, n_rows, n_vet):
            bad.append(f"colophon: the [VETO] footnote says {md.group(1)} DEFERRED-TO-BR2 of "
                       f"{md.group(2)} rows and {mv.group(1)} bare [VETO]; the table carries "
                       f"{n_def} of {n_rows} and {n_vet}")
        elif n_def + n_vet != n_rows:
            bad.append(f"colophon: the [VETO] footnote's two counts sum to {n_def + n_vet}, "
                       f"the table has {n_rows} row(s) — a row carries neither chip")
    if not re.search(r"<h3>\s*Spaghetti", _sec(doc, SEC_WATCH)) or "<svg" not in _sec(doc, SEC_WATCH):
        bad.append("the watch: the Spaghetti sub-block (<h3>Spaghetti + its <svg>) is missing — "
                   "it has no section of its own in the eight and must not be lost")
    # ── the inks ─────────────────────────────────────────────────────────────
    m = re.search(r"(?s)<style>(.*?)</style>", doc)
    style = m.group(1) if m else ""
    if not style:
        bad.append("inks: no <style> block — fail closed")
    for name, val in (("paper", TS_PAPER), ("ink", TS_INK), ("red", TS_RED)):
        if val.lower() not in style.lower():
            bad.append(f"inks: the {name} {val} is not in the style block")
    if TS_SERIF not in style:
        bad.append(f"inks: the serif stack {TS_SERIF} is not in the style block")
    body = re.sub(r"(?is)<script\b.*?</script\s*>", " ", doc).lower()
    left = [c for c in TS_DARK_REMNANTS if c in body]
    if left:
        bad.append(f"inks: dark-theme remnant colour(s) still on the page: {left}")
    if re.search(r"prefers-color-scheme|\bdark\b", style, re.I):
        bad.append("inks: the style block names a dark scheme or a theme switch — light paper "
                   "only [D-7a]")
    for sel, decl in re.findall(r"([^{}]+)\{([^{}]*)\}", re.sub(r"(?s)/\*.*?\*/", " ", style)):
        if ("var(--red)" in decl or TS_RED.lower() in decl.lower()) and sel.strip() != ":root":
            stray = [s.strip() for s in sel.split(",")
                     if not any(a in s for a in TS_ALARM_CLASSES)]
            if stray:
                bad.append(f"inks: the alarm red is set on {stray}, which is no alarm — red "
                           f"belongs to {list(TS_ALARM_CLASSES)} only")
    inline = re.findall(r'style="[^"]*(?:var\(--red\)|' + re.escape(TS_RED) + r')', body, re.I)
    if inline:
        bad.append(f"inks: the alarm red is typed inline {len(inline)} time(s)")
    hues = sorted({int(h) for h in re.findall(r"hsl\((\d+),", body)})
    hot = [h for h in hues if h < TS_RED_HUES[0] or h > TS_RED_HUES[1]]
    if hot:
        bad.append(f"inks: Spaghetti hue(s) {hot} fall inside the red band — red is the alarm ink")
    # ── the masthead ─────────────────────────────────────────────────────────
    head = doc.split("<h2>")[0]
    if f"<h1>{TS_TITLE}</h1>" not in head:
        bad.append(f"masthead: no <h1>{TS_TITLE}</h1> above the first section")
    ears = {k: _page_text(v) for k, v in
            re.findall(r'(?s)<div class="ear (ear-[lr])">(.*?)</div>', head)}
    ml = TS_EAR_LEFT.match(ears.get("ear-l", ""))
    mr = TS_EAR_RIGHT.match(ears.get("ear-r", ""))
    if not ml:
        bad.append(f"masthead: the left ear reads {ears.get('ear-l')!r}, not 'Vol. I · No. <n>'")
    if not mr:
        bad.append(f"masthead: the right ear reads {ears.get('ear-r')!r}, not 'Buenos Aires · "
                   f"<date> · <Morning|Evening|Refresh> Edition · Price: one toll'")
    elif date is not None and mr.group(1) != date:
        bad.append(f"masthead: the right ear is dated {mr.group(1)}, the edition is {date}")
    # ── the band's phrase, only ever inside the band ─────────────────────────
    band = re.search(r'(?s)<div class="stale">(.*?)</div>', doc)
    n_phrase = _page_text(doc).count(TS_BAND)
    if band is None and n_phrase:
        bad.append(f"late edition: {TS_BAND!r} is in the page's text {n_phrase} time(s) with no "
                   f"band up — the wrapper would log a false 'banner UP'")
    if band is not None:
        if n_phrase != 1 or TS_BAND not in _page_text(band.group(1)):
            bad.append(f"late edition: a band is up and {TS_BAND!r} is in the page's text "
                       f"{n_phrase} time(s), want once, inside the band")
        if not re.search(r'</header>\s*<div class="stale">', head):
            bad.append("late edition: the band is not directly under the masthead")
    return bad, {"sections": len(titles), "strips": len(canv), "hues": hues,
                 "edition": ml.group(1) if ml else None, "name": mr.group(2) if mr else None,
                 "band": band is not None}


def _ts_band(doc: str) -> str | None:
    m = re.search(r'(?s)<div class="stale">(.*?)</div>', doc)
    return None if m is None else _page_text(m.group(1))


def _ts_renders() -> dict:
    """ONE view, rendered six ways: fresh, stale, plain, numbered, timed and shifted.
    'timed' is a numbered full-verb edition handed a print time (19:17 Buenos Aires on
    TS_VII_DAY), the page vii's leg-(i) plants are cut from when the edition under test
    has no print line to cut. OR-2 R-1: a row is aged against the PRINT TIME, so the band
    is driven by the print time handed in, never by moving the view's as-of: 'fresh' is
    printed TS_MARGIN_MS INSIDE A2-7's limit for the view's OLDEST row (so every row is
    fresh), 'stale' TS_MARGIN_MS PAST it for its NEWEST (so every row is stale, R of R).
    The limit is recomputed HERE from the two module constants, so a banner that fires on
    some other rule is caught, not mirrored — but the PERIOD COUNT is pinned against A2-7
    in _ts_live (TS_LENS_PERIODS), because a limit mirrored off the module proves the band
    fires relative to whatever the module currently says and never that the module says
    something useful. Only the lens STEP is read from the module: OD.LENS_MS is physical
    fact (4h = 14,400,000 ms), not a ruling."""
    from datetime import datetime, timedelta, timezone
    view = _pristine_view()
    canon = PE.canon_sha()
    limit = OD.STALE_LENS_PERIODS * OD.LENS_MS[view["lens"]]
    bars = [int(a["station"].as_of_ms) for a in view["assets"]]
    newest, oldest = max(bars), min(bars)
    fresh_at = datetime.fromtimestamp((oldest + limit - TS_MARGIN_MS) / 1000, timezone.utc)
    stale_at = datetime.fromtimestamp((newest + limit + TS_MARGIN_MS) / 1000, timezone.utc)
    from zoneinfo import ZoneInfo
    y, mo, d = map(int, TS_VII_DAY.split("-"))
    out = {"limit_h": limit / 3_600_000,
           "stale_as_of": datetime.fromtimestamp(oldest / 1000, timezone.utc)
                                  .strftime("%Y-%m-%dT%H:%MZ"),
           "stale_n": len(bars),
           "fresh": OD.render_html(view, DATE, canon, printed_at=fresh_at),
           "stale": OD.render_html(view, DATE, canon, printed_at=stale_at),
           "plain": OD.render_html(view, DATE, canon),
           "plain_as_of_ms": view["as_of_ms"],
           "numbered": OD.render_html(view, DATE, canon, edition_no=7, slot="on-demand-refresh"),
           # a TIMED edition (A-OR1-1 vii), printed 19:17 Buenos Aires on the full verb: the
           # page vii's leg-(i) plants are cut from when the edition under test has no
           # print line to cut (an edition printed before vii)
           "timed": OD.render_html(view, DATE, canon, edition_no=7, slot="on-demand-full",
                                   printed_at=datetime(y, mo, d, 19, 17, tzinfo=ZoneInfo(TS_ZONE)))}
    real_dt = OD.datetime

    class _Shifted(real_dt):                       # the module's clock, 400 days on
        @classmethod
        def now(cls, tz=None):
            return real_dt.now(tz) + timedelta(days=TS_CLOCK_SHIFT_DAYS)
    try:
        OD.datetime = _Shifted
        out["shifted"] = OD.render_html(view, DATE, canon)
    finally:
        OD.datetime = real_dt
    return out


def _ts_live(renders: dict) -> tuple[list[str], dict]:
    bad: list[str] = []
    if OD.STALE_LENS_PERIODS != TS_LENS_PERIODS:
        bad.append(f"late edition: A2-7 rules the band at {TS_LENS_PERIODS} lens periods, "
                   f"the module says {OD.STALE_LENS_PERIODS} — the limit on the "
                   f"{renders['limit_h']:.1f}h lens-period arithmetic is not the ruled one")
    fresh, stale = _ts_band(renders["fresh"]), _ts_band(renders["stale"])
    if fresh is not None or TS_BAND in _page_text(renders["fresh"]):
        bad.append(f"late edition: the band prints on a wire {TS_MARGIN_MS // 60_000} min INSIDE "
                   f"the {renders['limit_h']:.1f}h limit — it must print only when the rule fires")
    want = TS_BAND_HEAD.format(n=renders["stale_n"], r=renders["stale_n"],
                               as_of=renders["stale_as_of"])
    if stale is None:
        bad.append(f"late edition: no band on a wire {TS_MARGIN_MS // 60_000} min PAST the "
                   f"{renders['limit_h']:.1f}h limit — the rule fired and the page is silent")
    else:
        if not stale.startswith(want):
            bad.append(f"late edition: the band opens {stale[:60]!r}, not {want!r}")
        if TS_BAND_DETAIL not in stale:
            bad.append("late edition: A2-7's detail sentence no longer follows the opening")
        sb, _x = _ts_static(renders["stale"], DATE)
        bad += [b for b in sb if b.startswith("late edition")]
    for name in (SEC_BOARD, SEC_WATCH):
        a, b = _sec(renders["plain"], name), _sec(renders["shifted"], name)
        if not a or not b:
            bad.append(f"wall clock: no {name!r} section to compare — fail closed")
        elif a != b:
            bad.append(f"wall clock: {name!r} differs ({len(a):,} B vs {len(b):,} B) when the "
                       f"module's clock is pushed {TS_CLOCK_SHIFT_DAYS} days on — something "
                       f"wall-clock is typeset into it")
    _b, plain = _ts_static(renders["plain"], DATE)
    _b, numbered = _ts_static(renders["numbered"], DATE)
    # TIME-AWARE (A-OR1-1 vii): a render nobody numbered and nobody timed is a PROOF on
    # the full verb, and its ear reads vii at the view's as-of bar, in Buenos Aires —
    # the hour computed HERE in TS_ZONE, not read off the module
    from datetime import datetime
    from zoneinfo import ZoneInfo
    p_at = datetime.fromtimestamp(renders["plain_as_of_ms"] / 1000, ZoneInfo(TS_ZONE))
    plain_word = _vii_word("full", p_at.hour)
    if (plain["edition"], plain["name"]) != ("—", plain_word):
        bad.append(f"masthead: a render nobody numbered or timed (a PROOF, the full verb, as-of "
                   f"bar {p_at:%Y-%m-%d %H:%M} Buenos Aires) reads No. {plain['edition']} · "
                   f"{plain['name']} Edition, want 'No. —' and '{plain_word} Edition'")
    if _ts_vii_read(renders["plain"])[1]:
        bad.append("masthead: a render handed no print time carries a print line — an "
                   "UNTIMED render claims a print time nobody gave it")
    if (numbered["edition"], numbered["name"]) != ("7", "Refresh"):
        bad.append(f"masthead: edition_no=7, slot='on-demand-refresh' reads No. "
                   f"{numbered['edition']} · {numbered['name']} Edition, want No. 7 · Refresh")
    return bad, {"stale_as_of": renders["stale_as_of"], "limit_h": renders["limit_h"],
                 "stale_n": renders["stale_n"],
                 "plain_word": plain_word, "plain_at": f"{p_at:%Y-%m-%d %H:%M}"}


def _ts_edition_count(counter=None) -> list[str]:
    """OD.edition_count against a planted tape directory, briefs/oracle EMPTY: the day
    the operator moved the render away."""
    counter = OD.edition_count if counter is None else counter
    bad = []
    saved = (OD.TAPE_DIR, OD.OUT_DIR)
    try:
        with tempfile.TemporaryDirectory(prefix="f-br-15-") as td:
            OD.TAPE_DIR, OD.OUT_DIR = Path(td) / "tape", Path(td) / "briefs"
            got = counter("2030-01-03")
            if got != 1:
                bad.append(f"edition count: {got} with no tape directory at all, want 1")
            OD.TAPE_DIR.mkdir()
            OD.OUT_DIR.mkdir()
            for stem in ("oracle_tape_2030-01-01", "oracle_tape_2030-01-02", "oracle_tape_notadate"):
                (OD.TAPE_DIR / f"{stem}.parquet").write_bytes(b"")
            for date, want in (("2030-01-03", 3), ("2030-01-02", 2)):
                got = counter(date)
                if got != want:
                    bad.append(f"edition count: {got} for an edition dated {date} over tapes of "
                               f"2030-01-01 and 2030-01-02 (+ one misnamed file) and an EMPTY "
                               f"briefs/oracle, want {want}")
    finally:
        OD.TAPE_DIR, OD.OUT_DIR = saved
    return bad


def _ts_headline(fn=None) -> list[str]:
    """oracle_daily.front_page over four SYNTHETIC boards (no cache, no clock): which
    words open the headline, and which clause each symbol lands in."""
    from types import SimpleNamespace as NS
    fn = OD.front_page if fn is None else fn

    def asset(sym, word, age=None, stale=False):
        wins = [] if word in ("STALKING", "DEAD") else [
            NS(trigger_i=None if age is None else 1, trigger_age_bars=age, trigger_stale=stale)]
        return {"symbol": sym, "card": None,
                "station": NS(board_word=word, open_windows=wins)}
    # names no contract has, and no <X>USDT string: F-BR-16 hunts second symbol lists
    fresh, stale = asset("AAA", "TRIGGERED", 2), asset("BBB", "TRIGGERED", 40, True)
    armed, idle, dead = asset("CCC", "ARMED"), asset("DDD", "STALKING"), asset("EEE", "DEAD")
    cases = (
        ("a fresh trigger, a stale one, an armed window", [fresh, stale, armed, idle],
         "Business possible:", ("AAA triggered", "BBB triggered but stale", "CCC armed")),
        ("ONLY a stale trigger and an armed window", [stale, armed, idle],
         "No fresh trigger on the roster:", ("BBB triggered but stale", "CCC armed")),
        ("only an armed window", [armed, idle, dead],
         "No fresh trigger on the roster:", ("CCC armed",)),
        ("nothing but STALKING and DEAD", [idle, dead], "No business possible today", ()),
    )
    bad = []
    for label, assets, opens, clauses in cases:
        h = fn({"assets": assets, "lens": "4h", "as_of_ms": 0})["headline"]
        if not h.startswith(opens):
            bad.append(f"headline: over {label} it opens {h[:50]!r}, want {opens!r} — only a "
                       f"FRESH trigger earns 'Business possible'")
        gone = [c for c in clauses if c not in h]
        if gone:
            bad.append(f"headline: over {label} it does not say {gone}: {h!r}")
    return bad


def _vii_verb(slot: str) -> str:
    """vii's verb, the fixture's own reading: a slot naming 'refresh' is the refresh verb."""
    return "refresh" if "refresh" in str(slot).lower() else "full"


def _vii_word(slot: str, hour: int) -> str:
    """vii restated HERE: refresh = Refresh; full before 12:00 BA = Morning, from it Evening."""
    return "Refresh" if _vii_verb(slot) == "refresh" else ("Morning" if hour < 12 else "Evening")


@contextlib.contextmanager
def _ts_machine_zone(tz: str):
    """The PROCESS's local zone set to `tz` for the length of the block (TZ + tzset), then
    put back exactly as it was: what a laptop set to another zone would read."""
    import time
    old = os.environ.get("TZ")
    os.environ["TZ"] = tz
    time.tzset()
    try:
        yield
    finally:
        if old is None:
            os.environ.pop("TZ", None)
        else:
            os.environ["TZ"] = old
        time.tzset()


def _ts_vii_read(doc: str) -> tuple[str | None, list[tuple]]:
    """(the right ear's word, every print line in the Colophon's <footer>) as READ."""
    head = doc.split("<h2>")[0]
    ears = {k: _page_text(v) for k, v in
            re.findall(r'(?s)<div class="ear (ear-[lr])">(.*?)</div>', head)}
    mr = TS_EAR_RIGHT.match(ears.get("ear-r", ""))
    foot = re.search(r"(?s)<footer>(.*?)</footer>", _sec(doc, SEC_COLOPHON))
    lines = TS_PRINT_LINE.findall(_page_text(foot.group(1))) if foot else []
    return (mr.group(2) if mr else None), lines


def _ts_vii_selfcheck(doc: str) -> dict | None:
    """The wrapper's selfcheck row (the log G-BR2-2 reads) carrying this page's sha256 —
    the one per-edition record that names the slot the edition was printed under — or
    None when there is none (a sandbox render, a planted copy, an edition whose checks
    did not run). A pure read of the log."""
    import oracle_wrapper as OW
    if not OW.SELFCHECK.exists():
        return None
    sha = hashlib.sha256(doc.encode("utf-8")).hexdigest()
    rows = []
    for ln in OW.SELFCHECK.read_text(encoding="utf-8").splitlines():
        try:
            r = json.loads(ln)
        except ValueError:
            continue
        if isinstance(r, dict) and r.get("html_sha") == sha:
            rows.append(r)
    return rows[-1] if rows else None


def _ts_vii_witnesses(doc: str) -> str:
    """For an edition with no print line: what the disk says about when it was printed —
    its selfcheck row and its file's mtime, each read in Buenos Aires — so the RED line
    names the hour vii would have read."""
    from datetime import datetime
    from zoneinfo import ZoneInfo
    ba, out = ZoneInfo(TS_ZONE), []
    row = _ts_vii_selfcheck(doc)
    if row is not None and row.get("ts"):
        t = datetime.fromisoformat(row["ts"]).astimezone(ba)
        out.append(f"the selfcheck row carrying its sha256 (slot {row.get('slot')}) was "
                   f"written {t:%Y-%m-%d %H:%M} Buenos Aires, which vii calls the "
                   f"{_vii_word(str(row.get('slot')), t.hour)} Edition")
    p = OD.OUT_DIR / f"oracle_{DATE}.html"
    if p.exists() and p.read_text(encoding="utf-8") == doc:
        t = datetime.fromtimestamp(p.stat().st_mtime, ba)
        out.append(f"{p.name}'s mtime reads {t:%Y-%m-%d %H:%M} Buenos Aires")
    return (" (witnesses: " + "; ".join(out) + ")") if out else ""


def _ts_vii_page(doc: str, witnesses: bool = False) -> tuple[list[str], dict]:
    """vii LEG (i), THE EDITION UNDER TEST: its ear's word agrees with the verb and the
    Buenos Aires hour of its OWN print line; the selfcheck row, when there is one, agrees
    with the print line's slot and was written no earlier than the printed minute."""
    from datetime import datetime
    from zoneinfo import ZoneInfo
    bad: list[str] = []
    ear, lines = _ts_vii_read(doc)
    if len(lines) != 1:
        if lines:
            bad.append(f"vii (the edition under test): {len(lines)} print lines in the Colophon, "
                       f"want exactly one")
        else:
            bad.append(f"vii (the edition under test): no print line in the Colophon — the "
                       f"edition carries no evidence of the hour it was printed, so its ear's "
                       f"'{ear} Edition' cannot be held to A-OR1-1 vii"
                       + (_ts_vii_witnesses(doc) if witnesses else "")
                       + ". An edition printed before vii has none: RED by design until one "
                       "is printed by this code (the sandbox suite prints one)")
        return bad, {"vii_print": None, "vii_selfcheck": None}
    day, hh, mm, word, verb, slot = lines[0]
    want = _vii_word(slot, int(hh))
    at = f"{day} {hh}:{mm} Buenos Aires"
    if verb != _vii_verb(slot):
        bad.append(f"vii (the edition under test): the print line names the {verb} verb for "
                   f"slot {slot!r}, which is the {_vii_verb(slot)} verb")
    if word != want:
        bad.append(f"vii (the edition under test): the print line says the {word} Edition for "
                   f"{at} on the {_vii_verb(slot)} verb — vii makes that the {want} Edition")
    if ear != want:
        bad.append(f"vii (the edition under test): the ear says '{ear} Edition'; its own print "
                   f"line ({at}, the {_vii_verb(slot)} verb, slot {slot}) makes it the {want} "
                   f"Edition under vii")
    row = _ts_vii_selfcheck(doc)
    seen = None
    if row is not None:
        seen = f"slot {row.get('slot')}, written {row.get('ts')}"
        if row.get("slot") != slot:
            bad.append(f"vii (the edition under test): the selfcheck row carrying this page's "
                       f"sha256 names slot {row.get('slot')!r}; the print line says {slot!r}")
        try:
            t = datetime.fromisoformat(str(row.get("ts"))).astimezone(ZoneInfo(TS_ZONE))
            floor = datetime(*map(int, day.split("-")), int(hh), int(mm), tzinfo=ZoneInfo(TS_ZONE))
            if t < floor:
                bad.append(f"vii (the edition under test): its selfcheck row was written "
                           f"{t:%Y-%m-%d %H:%M} Buenos Aires, BEFORE the printed {at} — the "
                           f"print line is not this edition's print time")
        except (TypeError, ValueError) as e:
            bad.append(f"vii (the edition under test): the selfcheck row's ts {row.get('ts')!r} "
                       f"does not parse ({e}) — fail closed")
    return bad, {"vii_print": (at, word, _vii_verb(slot), slot, ear), "vii_selfcheck": seen}


_TS_VII = None


def _ts_vii_table(namer=None, zoner=None) -> tuple[list[str], dict]:
    """vii LEG (ii), THE LAW: every row of TS_VII_TABLE through oracle_daily.edition_name
    AND through a real render (the ear, and the Colophon's print line read back), with the
    print time handed in UTC and the process's local zone forced to TS_MACHINE_ZONE; then
    a naive print time, which must be refused. `namer` / `zoner` swap in a planted
    edition_name / print_time_ba by module attribute — render_html and print_line reach
    them by that name — for the length of ONE judgement, and are always put back. The
    unplanted result is computed once."""
    global _TS_VII
    planted = namer is not None or zoner is not None
    if not planted and _TS_VII is not None:
        return list(_TS_VII[0]), dict(_TS_VII[1])
    from datetime import datetime, timezone
    from zoneinfo import ZoneInfo
    ba = ZoneInfo(TS_ZONE)
    view, canon = _pristine_view(), PE.canon_sha()
    y, mo, d = map(int, TS_VII_DAY.split("-"))
    saved = (OD.edition_name, OD.print_time_ba)
    bad: list[str] = []
    try:
        if namer is not None:
            OD.edition_name = namer
        if zoner is not None:
            OD.print_time_ba = zoner
        with _ts_machine_zone(TS_MACHINE_ZONE):
            for slot, hhmm, want in TS_VII_TABLE:
                hh, mm = map(int, hhmm.split(":"))
                at = datetime(y, mo, d, hh, mm, tzinfo=ba).astimezone(timezone.utc)
                where = f"{slot} printed {hhmm} Buenos Aires"
                try:
                    got = OD.edition_name(slot, at)
                except Exception as e:                       # noqa: BLE001 — judged, not raised
                    got = f"raised {e.__class__.__name__}"
                if got != f"{want} Edition":
                    bad.append(f"vii table: edition_name, {where} -> {got!r}, want "
                               f"'{want} Edition'")
                try:
                    doc = OD.render_html(view, TS_VII_DAY, canon, edition_no=7, slot=slot,
                                         printed_at=at)
                except Exception as e:                       # noqa: BLE001
                    bad.append(f"vii table: the render, {where} raised "
                               f"{e.__class__.__name__}: {e}")
                    continue
                ear, lines = _ts_vii_read(doc)
                if ear != want:
                    bad.append(f"vii table: the render, {where} -> the ear says '{ear} Edition', "
                               f"want '{want} Edition'")
                if len(lines) != 1:
                    bad.append(f"vii table: the render, {where} -> {len(lines)} print line(s) in "
                               f"the Colophon, want exactly one")
                    continue
                p_day, p_hh, p_mm, p_word, p_verb, p_slot = lines[0]
                if (p_day, f"{p_hh}:{p_mm}") != (TS_VII_DAY, hhmm):
                    bad.append(f"vii table: the render, {where} -> the Colophon's print line reads "
                               f"{p_day} {p_hh}:{p_mm}, want {TS_VII_DAY} {hhmm} Buenos Aires")
                if (p_word, p_verb, p_slot) != (want, _vii_verb(slot), slot):
                    bad.append(f"vii table: the render, {where} -> the print line names the "
                               f"{p_word} Edition, the {p_verb} verb, slot {p_slot}; want the "
                               f"{want} Edition, the {_vii_verb(slot)} verb, slot {slot}")
            try:
                got = OD.edition_name("full", datetime(y, mo, d, 19, 17))
                bad.append(f"vii table: a naive print time ({TS_VII_DAY} 19:17, no zone) was "
                           f"ACCEPTED by edition_name ({got!r}) — its hour would be the "
                           f"machine's zone's; it must be refused")
            except ValueError:
                pass
            except Exception as e:                           # noqa: BLE001
                bad.append(f"vii table: a naive print time raised {e.__class__.__name__}, not "
                           f"the ValueError that refuses it")
    finally:
        OD.edition_name, OD.print_time_ba = saved
    info = {"vii_rows": len(TS_VII_TABLE)}
    if not planted:
        _TS_VII = (list(bad), dict(info))
    return bad, info


def _ts_source(src: str | None = None) -> list[str]:
    """Scans CODE, not prose: the bar count typed once, the signature the wrapper calls,
    run() numbering the edition, and run() timing it (A-OR1-1 vii) with the one instant
    its date comes from."""
    src = (ROOT / "scripts" / "oracle_daily.py").read_text(encoding="utf-8") if src is None else src
    tree = ast.parse(src)
    bad = []
    for n in ast.walk(tree):
        if isinstance(n, ast.Constant) and isinstance(n.value, str) and re.search(
                r"columns = last \d+ bars", n.value):
            bad.append(f"caption: oracle_daily.py:{n.lineno} types the strip's bar count inside "
                       f"the caption — a second literal beside REGISTER['MANTLE_BARS']")
    fns = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    rh = fns.get("render_html")
    if rh is None:
        bad.append("signature: render_html() not found — fail closed")
    else:
        pos = [a.arg for a in (*rh.args.posonlyargs, *rh.args.args)]
        kwo = [a.arg for a in rh.args.kwonlyargs]
        if pos != ["view", "date_str", "canon_sha"] \
                or sorted(kwo) != ["edition_no", "printed_at", "slot"] \
                or any(d is None for d in rh.args.kw_defaults):
            bad.append(f"signature: render_html takes {pos} + keyword-only {kwo}; the fixtures "
                       f"and the wrapper's per-edition self-check call render_html(view, date_str, "
                       f"canon_sha), and the masthead's three are optional keywords")
    en = fns.get("edition_name")
    en_args = [a.arg for a in (*en.args.posonlyargs, *en.args.args)] if en is not None else None
    if en_args != ["slot", "printed_at"]:
        bad.append(f"signature: edition_name takes {en_args}; A-OR1-1 vii makes the word follow "
                   f"the verb AND the hour — edition_name(slot, printed_at)")
    run = fns.get("run")
    calls = [n for n in ast.walk(run) if isinstance(n, ast.Call)
             and isinstance(n.func, ast.Name)] if run is not None else []
    if not any(c.func.id == "edition_count" for c in calls):
        bad.append("run(): never calls edition_count() — the edition is not numbered")
    if not any(c.func.id == "render_html" and {"edition_no", "slot"} <= {k.arg for k in c.keywords}
               for c in calls):
        bad.append("run(): does not hand render_html BOTH edition_no and slot — a real edition "
                   "would go to press as 'No. —' or as the wrong edition")
    # A-OR1-1 vii: run() hands render_html the print time, and it is the ONE instant the
    # date comes from — a Name X with `date_str = X.strftime(...)` in run() — never a
    # second read of the clock
    handed = [k.value for c in calls if c.func.id == "render_html"
              for k in c.keywords if k.arg == "printed_at"]
    if not handed:
        bad.append("run(): does not hand render_html the print time (printed_at) — the edition "
                   "would go to press as a PROOF, its word read off the as-of bar")
    else:
        date_src = {a.value.func.value.id for a in ast.walk(run) if isinstance(a, ast.Assign)
                    and any(isinstance(t, ast.Name) and t.id == "date_str" for t in a.targets)
                    and isinstance(a.value, ast.Call) and isinstance(a.value.func, ast.Attribute)
                    and a.value.func.attr == "strftime" and isinstance(a.value.func.value, ast.Name)}
        off = [ast.unparse(v) for v in handed
               if not (isinstance(v, ast.Name) and v.id in date_src)]
        if off or not date_src:
            bad.append(f"run(): the print time handed to render_html ({', '.join(off) or '?'}) is "
                       f"not the instant the date comes from (date_str = "
                       f"{'/'.join(sorted(date_src)) or '?'}.strftime(...)) — vii's hour and the "
                       f"edition's date must be read off ONE `now`")
    return bad


_TS_RENDERS = None


def _typeset_judge(html_doc: str | None = None, renders: dict | None = None,
                   src: str | None = None, counter=None, headliner=None,
                   periods: int | None = None, namer=None, zoner=None,
                   masthead_src: str | None = None) -> tuple[list[str], dict]:
    """`periods` raises OD.STALE_LENS_PERIODS for the duration of ONE judgement — the
    THRESHOLD PLANT, the only way to drive A2-7's ruled number itself out of true.
    `namer` / `zoner` are A-OR1-1 vii's plants (see _ts_vii_table)."""
    global _TS_RENDERS
    real_periods = OD.STALE_LENS_PERIODS
    doc = HTML if html_doc is None else html_doc
    try:
        if periods is not None:
            OD.STALE_LENS_PERIODS = periods
            _TS_RENDERS = None                     # the limit moved; re-render
        if _TS_RENDERS is None:
            _TS_RENDERS = _ts_renders()
        bad, page = _ts_static(doc, DATE)
        live_bad, live = _ts_live({**_TS_RENDERS, **(renders or {})})
    finally:
        if periods is not None:
            OD.STALE_LENS_PERIODS = real_periods
            _TS_RENDERS = None                     # never leave a planted limit cached
    # A-OR1-1 vii: leg (i) on the page under test (witnesses read for the edition itself
    # only), leg (ii) over the table
    vii_bad, vii = _ts_vii_page(doc, witnesses=html_doc is None)
    tbl_bad, tbl = _ts_vii_table(namer, zoner)
    bad = (bad + live_bad + vii_bad + tbl_bad + _ts_edition_count(counter) + _ts_source(src)
           + _ts_headline(headliner))
    m = re.search(r"columns = last (\d+) bars", TS_CAPTION)
    bars = OD.REGISTER["MANTLE_BARS"]["value"]
    if int(m.group(1)) != bars:
        bad.append(f"caption: the contract's caption says {m.group(1)} bars and "
                   f"REGISTER['MANTLE_BARS'] is {bars} — the caption and the strip disagree")
    if (max(OD.THREADS), min(OD.THREADS)) != (5000, 9):
        bad.append(f"caption: the caption names rod 5000 and hem 9; the threads run "
                   f"{max(OD.THREADS)}..{min(OD.THREADS)}")
    if OD.mantle_caption() != TS_CAPTION:
        bad.append("caption: oracle_daily.mantle_caption() is not the contract's sentence")
    if tuple(OD.REGISTER["SECTIONS"]["value"]) != SECTIONS:
        bad.append("sections: REGISTER['SECTIONS'] is not the contract's eight, in order")
    for k in ("EDITION_COUNT", "FRONT_PAGE_HEADLINE"):
        if OD.REGISTER[k]["ruled"]:
            bad.append(f"{k} reads 'ruled': True — it is this build's reading and no ruling is "
                       f"on record")
        if f"<code>{k}</code>" not in _sec(doc, SEC_COLOPHON):
            bad.append(f"colophon: the rendered [VETO] appendix does not list {k}")
    # the MASTHEAD row names the three words and quotes vii to the letter
    m_src = OD.REGISTER["MASTHEAD"]["source"] if masthead_src is None else masthead_src
    if "<Morning|Evening|Refresh>" not in m_src or TS_VII not in m_src:
        bad.append("masthead register: REGISTER['MASTHEAD']['source'] does not say "
                   "'<Morning|Evening|Refresh>' and quote A-OR1-1 vii verbatim")
    return bad, {**page, **live, **vii, **tbl}


def f_br_15() -> None:
    src = (ROOT / "scripts" / "oracle_daily.py").read_text(encoding="utf-8")
    import html as _h
    cap_html = _h.escape(TS_CAPTION, quote=False)

    def _ensure():
        global _TS_RENDERS
        if _TS_RENDERS is None:
            _TS_RENDERS = _ts_renders()
        return _TS_RENDERS

    # THE PAGE THE RENDER PLANTS ARE CUT FROM. The edition under test, if it is a STEP F
    # page; otherwise a fresh render by the current code. An edition printed before
    # STEP F has no caption to remove and no eight sections to swap, and a plant that
    # cannot be planted voids the fixture for a reason that is not the code's (the
    # F-BR-16 rule). The REAL leg still audits the edition under test, and is red on it.
    step_f_page = cap_html in HTML and len(re.split(r"(?=<h2>)", HTML)) == len(SECTIONS) + 1
    base = HTML if step_f_page else _ensure()["plain"]
    cut_from = f"artifact set {DATE}" if step_f_page else "a fresh render — the artifact predates STEP F"
    no_caption, n_cap = (base.replace(cap_html, "", 1), base.count(cap_html))
    parts = re.split(r"(?=<h2>)", base)            # [head, sec1 .. sec8], the <h2> kept
    swapped = "".join(parts[:2] + [parts[3], parts[2]] + parts[4:]) if len(parts) == 9 else None
    col = _sec(base, SEC_COLOPHON)
    foot = re.search(r"(?s)<footer>.*?</footer>", col)
    no_fragment = (base.replace(foot.group(0), foot.group(0).replace(TS_FRAGMENT, ""), 1)
                   if foot and TS_FRAGMENT in foot.group(0) else None)
    dark = base.replace("<style>", "<style>.chip.defer{color:#a3b581}", 1)
    _NOTE_RE = r'(?s)<p class="small muted">((?:(?!</p>).)*)</p>\s*<table class="veto">'
    _note = re.search(_NOTE_RE, _sec(base, SEC_COLOPHON))
    old_note = (base.replace(_note.group(1), "BR-1 Amendment A2 (operator, 2026-08-16) ruled "
                             "the naming, the trigger pair, the net R:R form and the schedule. "
                             "The rows below are what remains: each is DEFERRED-TO-BR2, which "
                             "proposes a measured value from a week of D-7 distributions. "
                             "Nothing self-adopts.", 1) if _note else None)
    _defer_chip = '<span class="chip defer">DEFERRED-TO-BR2</span>'
    flipped = (base.replace(_defer_chip, '<span class="chip">[VETO]</span>', 1)
               if _defer_chip in base else None)
    red_word = base.replace("<style>", "<style>td.post.w-dead{color:var(--red)}", 1)
    loud = base.replace(cap_html, cap_html + " · LATE EDITION strips are re-cut hourly", 1)
    kw_anchor = "edition_no=edition_no, slot=slot"
    cap_anchor = "columns = last {bars} bars"

    # A-OR1-1 vii. Leg (i)'s plants are cut from the edition under test when it carries
    # its print line; otherwise from a fresh TIMED render (19:17 Buenos Aires, the full
    # verb) — an edition printed before vii has no line to remove (the F-BR-16 rule
    # again: a plant that cannot be planted voids the fixture for a reason that is not
    # the code's). The REAL leg still audits the edition under test, and is red on it.
    from zoneinfo import ZoneInfo
    vii_page = len(_ts_vii_read(HTML)[1]) == 1
    vbase = HTML if vii_page else _ensure()["timed"]
    vii_from = (f"artifact set {DATE}" if vii_page else
                "a fresh timed render — the artifact carries no print line (printed before vii)")
    _pl = re.search(r"Printed [^<]*?A-OR1-1 vii\)", vbase)
    no_print = vbase.replace(_pl.group(0), "", 1) if _pl else None
    _ear_div = re.search(r'(?s)<div class="ear ear-r">.*?</div>', vbase)
    _w = _ts_vii_read(vbase)[0]
    _flip = {"Morning": "Evening", "Evening": "Morning", "Refresh": "Morning"}.get(_w)
    ear_flipped = (vbase.replace(_ear_div.group(0), _ear_div.group(0).replace(
                   f"{_w} Edition", f"{_flip} Edition", 1), 1) if _ear_div and _flip else None)
    _pa = list(re.finditer(r",\s*printed_at=\w+\s*\)", src))
    no_time_src = clock_src = None
    if len(_pa) == 1:
        _s, _e = _pa[0].span()
        no_time_src = src[:_s] + ")" + src[_e:]
        clock_src = src[:_s] + ", printed_at=datetime.now(timezone.utc))" + src[_e:]
    _en_def = "def edition_name(slot: str, printed_at: datetime | None) -> str:"
    one_arg_src = (src.replace(_en_def, "def edition_name(slot: str) -> str:", 1)
                   if src.count(_en_def) == 1 else None)

    def _old_rule(slot, printed_at=None):          # HEAD 3d55988's edition_name, verbatim
        return "Refresh Edition" if "refresh" in str(slot).lower() else "Morning Edition"

    def _noon_is_morning(slot, printed_at):         # the boundary moved: noon read as "before"
        if "refresh" in str(slot).lower():
            return "Refresh Edition"
        t = OD.print_time_ba(printed_at)
        return "Morning Edition" if (t.hour, t.minute) <= (12, 0) else "Evening Edition"

    def _stamped(r):                                # a wall-clock stamp set into the Front Page
        from datetime import datetime
        return {"shifted": r["shifted"].replace('<p class="deck">',
                '<p class="deck">printed ' + datetime.now().isoformat() + " · ", 1)}

    # (name, the finding it MUST produce, how it is planted). Judged one at a time, the
    # F-BR-13 idiom: a red plant must not carry a green one through, and a plant red for
    # some OTHER reason has not shown its own guard working. The first three are the
    # contract's own break legs.
    plants = (
        ("RENDER PLANT, the contract's (the caption removed from ONE strip)",
         "carries the contract's caption 0 time(s)", lambda: dict(html_doc=no_caption) if n_cap else None),
        ("RENDER PLANT, the contract's (two sections swapped: The Docket and The Watch)",
         "section order", lambda: dict(html_doc=swapped) if swapped else None),
        ("RENDER PLANT, the contract's (DISPLAY-ONLY stripped from the colophon)",
         "fragment is missing from the Colophon", lambda: dict(html_doc=no_fragment) if no_fragment else None),
        ("RENDER PLANT (a dark-theme sage left in the style block)",
         "dark-theme remnant", lambda: dict(html_doc=dark)),
        ("RENDER PLANT (the colophon footnote back to its fixed clause, 'each is "
         "DEFERRED-TO-BR2', over a table 5 of whose rows print a bare [VETO])",
         "the [VETO] footnote", lambda: dict(html_doc=old_note) if old_note else None),
        ("RENDER PLANT (one row's chip flipped DEFERRED-TO-BR2 -> [VETO], which is what "
         "dropping that row's `deferred_to` key does, while the prose above does not move)",
         "the [VETO] footnote", lambda: dict(html_doc=flipped) if flipped else None),
        ("RENDER PLANT (the posture word DEAD set in the alarm red)",
         "which is no alarm", lambda: dict(html_doc=red_word)),
        ("RENDER PLANT (the band's phrase spelt under a strip, no band up)",
         "false 'banner UP'", lambda: dict(html_doc=loud) if _ts_band(base) is None else
         dict(html_doc=loud.replace(re.search(r'(?s)<div class="stale">.*?</div>', loud).group(0), "", 1))),
        ("LIVE PLANT (the band dropped from a render past the limit)",
         "the rule fired and the page is silent",
         lambda: dict(renders={"stale": re.sub(r'(?s)<div class="stale">.*?</div>', "",
                                               _ensure()["stale"], count=1)})),
        ("LIVE PLANT (the band printed on a wire inside the limit)",
         "INSIDE the", lambda: dict(renders={"fresh": _ensure()["stale"]})),
        ("LIVE PLANT (a wall-clock stamp typeset into the Front Page)",
         "wall clock", lambda: dict(renders=_stamped(_ensure()))),
        ("SOURCE PLANT (run() stops handing render_html the edition number and the slot)",
         "does not hand render_html BOTH",
         lambda: dict(src=src.replace(", " + kw_anchor, "", 1)) if src.count(", " + kw_anchor) == 1 else None),
        ("SOURCE PLANT (the strip's bar count typed into the caption, a second literal)",
         "a second literal", lambda: dict(src=src.replace(cap_anchor, "columns = last 96 bars", 1))
         if src.count(cap_anchor) == 1 else None),
        ("HEADLINE PLANT (this build's first draft: every TRIGGERED word is business, stale or not)",
         "only a FRESH trigger earns",
         lambda: dict(headliner=lambda v: {"headline": "Business possible: " + ", ".join(
             a["symbol"].replace("USDT", "") + " triggered" for a in v["assets"]
             if a["station"].board_word == "TRIGGERED")} if any(
             a["station"].board_word == "TRIGGERED" for a in v["assets"]) else OD.front_page(v))),
        ("COUNTER PLANT (editions counted from briefs/oracle, the render the operator moved)",
         "edition count",
         lambda: dict(counter=lambda d: len({p.stem for p in OD.OUT_DIR.glob("oracle_*.html")} | {d}))),
        # A-OR1-1 vii, LEG (ii) — the law over TS_VII_TABLE, calls and renders
        ("VII PLANT, the OLD RULE re-planted (edition_name back to HEAD 3d55988's: 'Morning "
         "Edition' for every slot that is not a refresh, whatever the hour)",
         "19:17 Buenos Aires -> 'Morning Edition'", lambda: dict(namer=_old_rule)),
        (f"VII PLANT, the machine's LOCAL ZONE (print_time_ba reads t.astimezone(), the "
         f"laptop's zone, here {TS_MACHINE_ZONE}: 19:17 Buenos Aires reads 22:17)",
         f"print line reads {TS_VII_DAY} 22:17", lambda: dict(zoner=lambda t: t.astimezone())),
        ("VII PLANT, the BOUNDARY moved (12:00:00 Buenos Aires read as before noon)",
         "12:00 Buenos Aires -> 'Morning Edition'", lambda: dict(namer=_noon_is_morning)),
        ("VII PLANT, a NAIVE print time accepted (converted as if it were the machine's zone)",
         "naive print time", lambda: dict(zoner=lambda t: t.astimezone(ZoneInfo(TS_ZONE)))),
        # A-OR1-1 vii, LEG (i) — the edition under test carries its own evidence
        (f"VII PLANT, the Colophon's print line REMOVED (cut from {vii_from})",
         "no print line in the Colophon", lambda: dict(html_doc=no_print) if no_print else None),
        (f"VII PLANT, the ear's word FLIPPED against its own print line (cut from {vii_from})",
         "the ear says", lambda: dict(html_doc=ear_flipped) if ear_flipped else None),
        # A-OR1-1 vii — the source and the register row
        ("SOURCE PLANT (run() stops handing render_html the print time)",
         "does not hand render_html the print time",
         lambda: dict(src=no_time_src) if no_time_src else None),
        ("SOURCE PLANT (run() hands render_html a SECOND clock read, not the instant its date "
         "comes from)",
         "not the instant the date comes from", lambda: dict(src=clock_src) if clock_src else None),
        ("SOURCE PLANT (edition_name back to one argument, the verb alone)",
         "edition_name(slot, printed_at)", lambda: dict(src=one_arg_src) if one_arg_src else None),
        ("REGISTER PLANT (the MASTHEAD row's words back to STEP F's '<Morning|Refresh>')",
         "masthead register",
         lambda: dict(masthead_src=OD.REGISTER["MASTHEAD"]["source"].replace(
             "<Morning|Evening|Refresh>", "<Morning|Refresh>"))),
        # LAST on purpose: it clears the render cache on its way out, so anything after
        # it would pay for a second set of renders.
        ("THRESHOLD PLANT (A2-7's ruled 2 lens periods quietly raised to 2000: the limit "
         "becomes 333 days and the band can never fire again)",
         "A2-7 rules the band at", lambda: dict(periods=2000)),
    )

    def _break() -> tuple[bool, str]:
        green, out = False, []
        for name, must, plant in plants:
            kw = plant()
            if kw is None:
                green = True
                out.append(f"{name} -> GREEN: the plant could not be planted")
                continue
            bad, _x = _typeset_judge(**kw)
            hits = [b for b in bad if must in b]
            if hits:
                rest = [b for b in bad if must not in b]
                out.append(f"{name} -> RED: {hits[0]}"
                           + (f" [and {len(rest)} other finding(s), first: {rest[0]}]" if rest else ""))
            else:
                green = True
                out.append(f"{name} -> " + ("GREEN" if not bad else
                           f"RED FOR THE WRONG REASON (no finding says {must!r}; first: {bad[0]})"))
        return green, f"[render plants cut from {cut_from}] " + " ‖ ".join(out)

    def _real() -> tuple[bool, str]:
        bad, x = _typeset_judge()
        if bad:
            return False, "; ".join(bad[:6]) + (f" (+{len(bad) - 6} more)" if len(bad) > 6 else "")
        at, word, verb, slot, ear = x["vii_print"]
        return True, (
            f"artifact set {DATE}: exactly {x['sections']} bare <h2> sections in the contract's "
            f"order ({' · '.join(SECTIONS)}); each of {x['strips']} mantle strips carries the "
            f"contract's caption once, verbatim, its bar count = REGISTER['MANTLE_BARS'] = "
            f"{OD.REGISTER['MANTLE_BARS']['value']} and typed nowhere else in oracle_daily.py; the "
            f"<footer> sits inside the Colophon and carries {TS_FRAGMENT} and the as-of; the "
            f"Spaghetti is an <h3> of The Watch and the [VETO] appendix an <h3> of the Colophon, "
            f"listing EDITION_COUNT and FRONT_PAGE_HEADLINE ('ruled': False). Inks: {TS_PAPER}, "
            f"{TS_INK}, {TS_RED} and the serif stack in the style block, none of the "
            f"{len(TS_DARK_REMNANTS)} pre-STEP-F colours on the page, no theme switch, the red "
            f"only under {list(TS_ALARM_CLASSES)}, Spaghetti hues {x['hues'][0]}..{x['hues'][-1]} "
            f"clear of the red band. Masthead: '{TS_TITLE}', left ear No. {x['edition']}, right "
            f"ear {DATE} · {x['name']} Edition; an un-numbered render says 'No. —', "
            f"edition_no=7 + a refresh slot says No. 7 · Refresh; render_html(view, date_str, "
            f"canon_sha) still stands; over four synthetic boards the headline opens 'Business "
            f"possible' for a FRESH trigger only ('No fresh trigger on the roster' over stale or "
            f"armed rows, 'No business possible today' over none); run() numbers the edition from the TAPE's dates "
            f"(3 of 2 tapes + today, 2 on a reprint, 1 with no directory; a misnamed file and an "
            f"empty briefs/oracle change nothing). LATE EDITION: one view printed "
            f"{TS_MARGIN_MS // 60_000} min inside the {x['limit_h']:.1f}h limit for its oldest row -> "
            f"no band and the phrase nowhere in the text; {TS_MARGIN_MS // 60_000} min past it for its "
            f"newest -> the band directly under the masthead, opening '"
            f"{TS_BAND_HEAD.format(n=x['stale_n'], r=x['stale_n'], as_of=x['stale_as_of'])}', "
            f"A2-7's sentence after it, the phrase exactly once. The Front Page and The Watch do "
            f"not move a byte with the module's clock pushed {TS_CLOCK_SHIFT_DAYS} days on. "
            f"A-OR1-1 vii (\"{TS_VII}\"): (i) artifact set {DATE}'s Colophon carries ONE print "
            f"line, printed {at}, the {verb} verb, slot {slot} -> the {word} Edition, and the "
            f"ear says the {ear} Edition; "
            + (f"its selfcheck row ({x['vii_selfcheck']}) names the same slot and was written no "
               f"earlier than the printed minute; " if x["vii_selfcheck"] else
               "no selfcheck row carries its sha256 (a sandbox render, or an edition whose "
               "self-checks did not run), so the slot cross-check had nothing to read; ")
            + f"(ii) over {x['vii_rows']} rows (" + ", ".join(
                f"{s} {t} -> {w}" for s, t, w in TS_VII_TABLE)
            + f"), each through edition_name AND a real render, the print time handed in UTC "
              f"and the process's zone forced to {TS_MACHINE_ZONE}, the ear and the print line "
              f"say vii's word and the Buenos Aires minute; 12:00:00 is Evening; a naive print "
              f"time is refused; run() hands render_html the one instant its date comes from; "
              f"an un-numbered, untimed render (a PROOF) says 'No. —', carries no print line and "
              f"reads vii at its as-of bar ({x['plain_at']} Buenos Aires -> {x['plain_word']}).")

    prove("F-BR-15", "THE DAILY ORACLE — eight sections in order, a caption under every strip, "
                     "DISPLAY-ONLY in the colophon, three inks, the LATE EDITION band when and "
                     "only when the wire is stale, and the edition's word per A-OR1-1 vii "
                     "(verb and Buenos Aires hour, the print time in the Colophon)",
          _break, _real)


# ═════════════════ F-BR-16 · THE ROSTER IS ONE LITERAL DEFINITION (OR-1 STEP C)
#
# WHAT THIS GUARDS. Until 2026-09-21 the Oracle's roster was tuple(<engine/cells.py's
# basket>): the frozen STUDY basket, borrowed. Operator ruling 1 of that day —
# "1-watchlist: drop symbols without data from a binance contract" — made the roster
# the Oracle's OWN constant: a literal in oracle_daily.REGISTER['ROSTER'], the
# probe's KEPT list in the operator's order. The contract's words for the protocol
# are "one source of truth". A constant nobody checks drifts in three ways, and
# each has a plant below:
#   · THE BINDING COMES BACK (a value computed from the study basket, or the import
#     alone). The basket and the watchlist are one definition again, and the next
#     roster ruling either mutates a frozen pre-registration or silently fails to
#     apply.
#   · A SECOND LIST APPEARS beside it — a fixture, the top-up or the wrapper types
#     its own symbols. That is the BOX_CAPACITY incident's shape (CONVENTIONS §6.4:
#     "of five sites depending on BOX_BYTES, two contained no BOX_BYTES string at
#     all"), so the scan is by VALUE: any literal holding two or more <X>USDT
#     strings anywhere in the Oracle family, except the ROSTER row itself.
#   · THE LITERAL STOPS BEING WHAT THE PROBE KEPT: a dropped name typed back in
#     (load_lens HALTs the whole edition on a series that cannot exist), a leftover
#     from the old basket, a kept name lost, or the operator's order handed to a
#     helpful sort.
# And one drift in the ARTIFACTS: an edition printed from some other roster. This
# suite audits the NEWEST artifact set on disk; if its mantle strips, its tape and
# its D-7 record do not carry exactly this roster, every other green in this file
# is a statement about a different list. So after a roster change the suite is RED
# against the old editions until one is printed from the new roster — on purpose.
#
# WHAT IT DOES NOT PROVE: that the probe is right (it is the record of ONE GET), or
# that the cache holds every series the roster needs (F-TU-5, against the
# enumerated scope).
#
# THE PROBE JSON IS NAMED ONCE, in the ROSTER row's own 'source' string, and read
# from there: the next roster ruling re-probes and re-writes that row, and this
# fixture follows without an edit. The file sits under research_outputs/oracle/**,
# which .gitignore ignores: ABSENT IS RED, never a skip.
#
# AMENDED BY OR-2 STEP 6 (ruling R-7, operator 2026-09-22): a DROPPED name may come back
# as a DIFFERENT live contract, in its own place, when — and only when — the operator
# ruled the mapping and a record carries it: roster_mapping_<date>.json, named once in
# the same 'source' string, one exchangeInfo probe copying the live contract's record
# (PERPETUAL · TRADING · quote USDT). The roster is then KEPT ∪ ruled mappings, in the
# operator's order, each mapped name at the dropped name's place. A mapped name with no
# record, a record that is not PERPETUAL/TRADING, a mapping of a name the probe did not
# drop, or a mapped name out of place is RED.

ROSTER_RULING = "1-watchlist: drop symbols without data from a binance contract"
ROSTER_MAPPING_RULING = "R-7"
_ROSTER_MAPPING = re.compile(r"research_outputs/oracle/roster_mapping_\d{4}-\d{2}-\d{2}\.json")
_UNSET = object()
# Where a live consumer of the roster can live. NOT the movers organ: its universe
# is the exchange's, by design not the roster's (OR-1 STEP E).
ROSTER_FAMILY = ("oracle_daily.py", "oracle_fixtures.py", "oracle_topup.py",
                 "oracle_topup_fixtures.py", "oracle_wrapper.py", "posture_engine.py")
_ROSTER_SYM = re.compile(r"^[0-9A-Z]{2,20}USDT$")
_ROSTER_PROBE = re.compile(r"research_outputs/oracle/roster_probe_\d{4}-\d{2}-\d{2}\.json")
_ROSTER_BASKET = "SYM" + "BOLS"      # spelt in two halves so this file never NAMES it


def _roster_node(tree: ast.AST):
    """The AST node of REGISTER['ROSTER']['value'] in an oracle_daily source, or None."""
    for n in ast.walk(tree):
        tgt = (n.targets[0] if isinstance(n, ast.Assign) and n.targets else
               n.target if isinstance(n, ast.AnnAssign) else None)
        if not (isinstance(tgt, ast.Name) and tgt.id == "REGISTER"
                and isinstance(n.value, ast.Dict)):
            continue
        for k, v in zip(n.value.keys, n.value.values):
            if not (isinstance(k, ast.Constant) and k.value == "ROSTER" and isinstance(v, ast.Dict)):
                continue
            for kk, vv in zip(v.keys, v.values):
                if isinstance(kk, ast.Constant) and kk.value == "value":
                    return vv
    return None


def _roster_symbol_lists(tree: ast.AST, skip=None) -> list[tuple[int, list[str]]]:
    """(line, symbols) of every literal container typing TWO OR MORE <X>USDT strings."""
    out = []
    for n in ast.walk(tree):
        if n is skip:
            continue
        els = (n.elts if isinstance(n, (ast.Tuple, ast.List, ast.Set)) else
               [k for k in n.keys if k is not None] if isinstance(n, ast.Dict) else [])
        syms = [e.value for e in els if isinstance(e, ast.Constant)
                and isinstance(e.value, str) and _ROSTER_SYM.match(e.value)]
        if len(syms) >= 2:
            out.append((n.lineno, syms))
    return out


def _roster_probe_doc() -> tuple[str | None, dict | None]:
    """(repo-relative path named by the ROSTER row, its JSON) — (path, None) if absent."""
    m = _ROSTER_PROBE.search(OD.REGISTER["ROSTER"].get("source", ""))
    if not m:
        return None, None
    pp = ROOT / m.group(0)
    return m.group(0), (json.loads(pp.read_text(encoding="utf-8")) if pp.exists() else None)


def _roster_mapping_doc() -> tuple[str | None, dict | None]:
    """(repo-relative path the ROSTER row names, its JSON) — (path, None) if absent."""
    m = _ROSTER_MAPPING.search(OD.REGISTER["ROSTER"].get("source", ""))
    if not m:
        return None, None
    pp = ROOT / m.group(0)
    return m.group(0), (json.loads(pp.read_text(encoding="utf-8")) if pp.exists() else None)


def _roster_expected(probe: dict, maps: dict) -> tuple:
    """KEPT ∪ ruled mappings, in the operator's order: each mapped name in its dropped
    name's place, every other dropped name gone."""
    kept = set(probe.get("kept", ()))
    return tuple(maps.get(x, x) for x in probe.get("operator_22", ()) if x in kept or x in maps)


def _roster_judge(src: str | None = None, html_doc: str | None = None,
                  tape_assets=None, cal_assets=None,
                  mapping_doc=_UNSET) -> tuple[list[str], dict]:
    """Every finding against the roster; [] = clean. `src` swaps in a planted
    oracle_daily.py TEXT; the three artifact arguments swap in planted artifacts.
    The ARTIFACTS are always held against the LIVE row — they were printed by the
    imported module, not by a planted text."""
    bad: list[str] = []
    real_src = src is None
    text = (ROOT / "scripts" / "oracle_daily.py").read_text(encoding="utf-8") if real_src else src
    tree = ast.parse(text)
    row = OD.REGISTER["ROSTER"]
    live = tuple(row["value"])

    # ── (a) THE SOURCE: a literal, and the study basket not so much as named
    node, literal = _roster_node(tree), None
    if node is None:
        bad.append("oracle_daily.REGISTER has no ['ROSTER']['value']")
    elif not (isinstance(node, ast.Tuple) and node.elts and all(
            isinstance(e, ast.Constant) and isinstance(e.value, str) for e in node.elts)):
        seg = " ".join((ast.get_source_segment(text, node) or "?").split())
        bad.append(f"ROSTER value is not a literal tuple of strings: oracle_daily.py:{node.lineno} "
                   f"reads `{seg[:60]}` — a roster computed from something else has a second owner")
    else:
        literal = tuple(e.value for e in node.elts)
    named = sorted({n.lineno for n in ast.walk(tree)
                    if (isinstance(n, ast.Name) and n.id == _ROSTER_BASKET)
                    or (isinstance(n, ast.Attribute) and n.attr == _ROSTER_BASKET)
                    or (isinstance(n, ast.ImportFrom)
                        and any(a.name == _ROSTER_BASKET for a in n.names))})
    if named:
        bad.append(f"oracle_daily.py names the study basket ({_ROSTER_BASKET}) at line(s) {named} — "
                   f"engine/cells.py is the frozen STUDY basket (charter §4), not the watchlist")

    # ── (b) NO SECOND LIST anywhere in the family (by VALUE, not by name)
    for fname in ROSTER_FAMILY:
        t = tree if fname == "oracle_daily.py" else ast.parse(
            (ROOT / "scripts" / fname).read_text(encoding="utf-8"))
        skip = node if fname == "oracle_daily.py" and literal is not None else None
        for ln, syms in _roster_symbol_lists(t, skip=skip):
            bad.append(f"a second symbol list: {fname}:{ln} types {len(syms)} symbols "
                       f"({', '.join(syms[:3])}{', …' if len(syms) > 3 else ''}) — live consumers "
                       f"IMPORT REGISTER['ROSTER'], they never retype it")

    # ── (c) THE ROW AND THE PROBE
    if row.get("ruled") is not True:
        bad.append("the ROSTER row is not 'ruled': True — the roster IS ruled (operator, 2026-09-21)")
    if ROSTER_RULING not in row.get("source", ""):
        bad.append(f"the ROSTER row's source does not quote ruling 1 verbatim ({ROSTER_RULING!r})")
    probe_path, probe = _roster_probe_doc()
    map_path, mdoc = _roster_mapping_doc()
    if mapping_doc is not _UNSET:
        mdoc = mapping_doc                          # a planted record (None = planted ABSENT)
    maps: dict = {}
    kept = dropped = ()
    if probe_path is None:
        bad.append("the ROSTER row's source names no research_outputs/oracle/roster_probe_<date>.json")
    elif probe is None:
        bad.append(f"the probe record {probe_path} is ABSENT — the roster cannot be held against "
                   f"what Binance answered (gitignored path: it must be restored, never skipped)")
    else:
        kept, dropped = tuple(probe.get("kept", ())), tuple(probe.get("dropped", ()))
        recs = probe.get("records", {})
        for s in dropped:
            if s not in row.get("source", ""):
                bad.append(f"the ROSTER row's source does not name the dropped {s}")
        # ── (c') THE RULED MAPPINGS (OR-2 R-7): named in the row, recorded, each clean
        if map_path is not None and mdoc is None:
            bad.append(f"the mapping record {map_path} is ABSENT — a mapped name cannot be "
                       f"held against its ruling (gitignored path: restore it, never skip)")
        elif mdoc is not None:
            if mdoc.get("ruling") != ROSTER_MAPPING_RULING:
                bad.append(f"the mapping record's ruling reads {mdoc.get('ruling')!r}, not "
                           f"{ROSTER_MAPPING_RULING!r}")
            for mp in mdoc.get("mappings", ()):
                d, lv, rr = mp.get("dropped"), mp.get("live"), mp.get("record") or {}
                if mp.get("verdict") != "MAP":
                    continue
                if d not in dropped:
                    bad.append(f"the mapping {d} -> {lv} maps a name the probe did not drop")
                    continue
                if not (rr.get("symbol") == lv and rr.get("contractType") == "PERPETUAL"
                        and rr.get("status") == "TRADING" and rr.get("quoteAsset") == "USDT"):
                    bad.append(f"the mapping {d} -> {lv}: its record is not PERPETUAL/TRADING/"
                               f"USDT for {lv} ({rr.get('contractType')}, {rr.get('status')})")
                    continue
                if lv not in row.get("source", ""):
                    bad.append(f"the ROSTER row's source does not name the mapped {lv}")
                maps[d] = lv
        if literal is not None:
            dups = sorted({s for s in literal if literal.count(s) > 1})
            back = [s for s in literal if s in dropped]
            ruled = set(maps.values())
            stray = [s for s in literal if s not in kept and s not in dropped and s not in ruled]
            want = _roster_expected(probe, maps)
            lost = [s for s in want if s not in literal]
            soft = [s for s in literal if s in kept and not (
                recs.get(s, {}).get("verdict") == "KEEP"
                and recs.get(s, {}).get("contractType") == "PERPETUAL"
                and recs.get(s, {}).get("status") == "TRADING")]
            if dups:
                bad.append(f"duplicate symbol(s) on the roster: {dups}")
            if back:
                bad.append(f"DROPPED BY RULING yet on the roster: {back} — {probe_path} records no "
                           f"Binance USDT-M contract by that name")
            if stray:
                bad.append(f"on the roster but not KEPT by the probe: {stray} — not among the "
                           f"operator's 22 as probed in {probe_path}, nor carried by a ruled "
                           f"mapping record (a mapping applied without its record)")
            if lost:
                bad.append(f"KEPT by the probe but missing from the roster: {lost}")
            if soft:
                bad.append(f"listed as kept but the probe's own record is not KEEP/PERPETUAL/"
                           f"TRADING: {soft}")
            if not (dups or back or stray or lost) and literal != want:
                i = next((j for j, (a, b) in enumerate(zip(literal, want)) if a != b),
                         min(len(literal), len(want)))
                bad.append(f"not in the operator's order: position {i + 1} reads "
                           f"{literal[i] if i < len(literal) else '—'}, KEPT ∪ ruled mappings "
                           f"(his order, each mapped name in its dropped name's place) reads "
                           f"{want[i] if i < len(want) else '—'}")
    if real_src and literal is not None and literal != live:
        bad.append(f"the live REGISTER['ROSTER'] ({len(live)}) is not the literal in the source "
                   f"({len(literal)}) — something rebinds the row after it is defined")

    # ── (d) THE ARTIFACT SET under test was printed from THIS roster
    doc = HTML if html_doc is None else html_doc
    strips = re.findall(r'<canvas[^>]*data-payload="oracle_mantle_([0-9A-Z]+)_[^"]*"', doc or "")
    t_assets = (sorted(set(TAPE["asset"])) if TAPE is not None else None) \
        if tape_assets is None else sorted(set(tape_assets))
    c_assets = (sorted(r.get("asset") for r in CAL.get("per_asset", [])) if CAL else None) \
        if cal_assets is None else sorted(cal_assets)
    for art, what, got in (("render", "mantle strips in the render", sorted(strips)),
                           ("tape", "assets on the tape", t_assets),
                           ("D-7 record", "assets in the D-7 record", c_assets)):
        if got is None:
            bad.append(f"the {art} is ABSENT from artifact set {DATE}")
        elif got != sorted(live):
            bad.append(f"{what}: {len(got)} symbol(s) against a roster of {len(live)} — missing "
                       f"{[x for x in live if x not in got]}, not on the roster "
                       f"{[x for x in got if x not in live]}; artifact set {DATE} was not printed "
                       f"from this roster")
    return bad, {"literal": literal, "line": getattr(node, "lineno", None), "kept": kept,
                 "dropped": dropped, "probe": probe_path, "strips": len(strips),
                 "maps": maps, "mapping": map_path,
                 "tape": len(t_assets or ()), "cal": len(c_assets or ())}


def f_br_16() -> None:
    src = (ROOT / "scripts" / "oracle_daily.py").read_text(encoding="utf-8")
    node = _roster_node(ast.parse(src))
    seg = ast.get_source_segment(src, node) if node is not None else None
    live = tuple(OD.REGISTER["ROSTER"]["value"])
    _pp, probe = _roster_probe_doc()
    dropped = tuple((probe or {}).get("dropped", ()))
    left = tuple((probe or {}).get("leaves_roster_not_in_operator_22", {}).get("symbols", ()))

    def lit(symbols) -> str:
        return "(" + ", ".join(f'"{x}"' for x in symbols) + ",)"

    def swap(new_seg: str | None):
        """The source with the ROSTER literal replaced — None if it cannot be planted."""
        if not seg or new_seg is None or src.count(seg) != 1:
            return None
        return dict(src=src.replace(seg, new_seg, 1))

    anchor = "from engine.data import cache_dir"
    alpha = tuple(sorted(live))
    # The strip to cut is one the page under test actually CARRIES (an edition printed
    # from an older roster has no strip for the newest symbols, and a plant that cannot
    # be planted voids the fixture for a reason that is not the code's).
    on_page = re.findall(r'<canvas[^>]*data-payload="oracle_mantle_([0-9A-Z]+)_[^"]*"', HTML or "")
    cut = ([x for x in on_page if x in live] or on_page or [live[-1]])[-1]
    strip_cut, n_cut = re.subn(
        rf'<canvas[^>]*data-payload="oracle_mantle_{re.escape(cut)}_[^"]*"[^>]*>', "", HTML or "", count=1)
    other = (left or dropped or ("NOTONROSTERUSDT",))[0]
    # OR-2 R-7 plants: every name READ from the two records, never typed here
    _mp, mdoc = _roster_mapping_doc()
    ruled = [m for m in (mdoc or {}).get("mappings", ()) if m.get("verdict") == "MAP"]
    mlive = ruled[0]["live"] if ruled else None
    near = next((f for f in (probe or {}).get("findings_reported_not_fixed", ())
                 if f.get("dropped") not in {m["dropped"] for m in ruled}
                 and f.get("near_name_live_contracts")), None)
    near_live = near["near_name_live_contracts"][0]["symbol"] if near else None
    near_at = (live.index(ruled[0]["live"]) if ruled and ruled[0]["live"] in live else None)

    def _near_swap():
        """The unmapped near-name typed in at its dropped name's place, no record."""
        if not near or near["dropped"] not in (probe or {}).get("operator_22", ()):
            return None
        op = list(probe["operator_22"])
        exp = [x for x in op if x in set(probe.get("kept", ())) or x == near["dropped"]
               or x in {m["dropped"] for m in ruled}]
        m_of = {m["dropped"]: m["live"] for m in ruled}
        m_of[near["dropped"]] = near_live
        return swap(lit(tuple(m_of.get(x, x) for x in exp)))
    kept_name = next(iter((probe or {}).get("kept", ())), None)

    # (name, the finding it MUST produce, how it is planted). Judged one at a time,
    # the F-BR-13 idiom: a red plant must not carry a green one through, and a plant
    # red for some OTHER reason has not shown its own guard working.
    plants = (
        ("SOURCE PLANT (the old binding: the value computed from the study basket)",
         "is not a literal tuple", swap(f"tuple({_ROSTER_BASKET})")),
        ("SOURCE PLANT (the study basket imported again, the literal left alone)",
         "names the study basket",
         dict(src=src.replace(anchor, f"from engine.cells import {_ROSTER_BASKET}\n{anchor}", 1))
         if src.count(anchor) == 1 else None),
        ("SOURCE PLANT (a second list typed beside the row)",
         "a second symbol list", dict(src=src + f"\n_SHADOW_ROSTER = {lit(live[:3])}\n")),
        (f"SOURCE PLANT (a DROPPED name typed back in: {dropped[0] if dropped else '—'})",
         "DROPPED BY RULING yet on the roster", swap(lit(live + dropped[:1])) if dropped else None),
        (f"SOURCE PLANT (a leftover of the old basket typed back in: {left[0] if left else '—'})",
         "on the roster but not KEPT by the probe", swap(lit(live + left[:1])) if left else None),
        (f"SOURCE PLANT (a kept name lost: {live[-1]})",
         "KEPT by the probe but missing", swap(lit(live[:-1]))),
        (f"MAPPING PLANT, the contract's ({mlive} on the roster, its mapping record emptied: "
         f"a mapping applied without its record)", "a mapping applied without its record",
         dict(mapping_doc={**mdoc, "mappings": []}) if mdoc and mlive else None),
        (f"MAPPING PLANT (the unmapped near-name {near_live} typed in at "
         f"{near['dropped'] if near else '—'}'s place, no ruling, no record)",
         "a mapping applied without its record", _near_swap()),
        (f"MAPPING PLANT ({mlive}'s record reading SETTLING)", "not PERPETUAL/TRADING",
         dict(mapping_doc={**mdoc, "mappings": [{**m, "record": {**m["record"], "status": "SETTLING"}}
                                                for m in ruled]}) if mdoc and ruled else None),
        (f"MAPPING PLANT (a mapping of the KEPT name {kept_name})", "did not drop",
         dict(mapping_doc={**mdoc, "mappings": [{**m, "dropped": kept_name} for m in ruled]})
         if mdoc and ruled and kept_name else None),
        (f"MAPPING PLANT ({mlive} moved from its dropped name's place to the end)",
         "not in the operator's order",
         swap(lit(tuple(x for x in live if x != mlive) + (mlive,))) if mlive in live and near_at != len(live) - 1 else None),
        ("MAPPING PLANT (the mapping record ABSENT)", "is ABSENT",
         dict(mapping_doc=None) if mdoc else None),
        ("SOURCE PLANT (the operator's order handed to sorted())",
         "not in the operator's order", swap(lit(alpha)) if alpha != live else None),
        (f"RENDER PLANT ({cut}'s mantle strip cut from the page)",
         "mantle strips in the render", dict(html_doc=strip_cut) if n_cut else None),
        (f"TAPE PLANT ({live[0]} swapped for {other})",
         "assets on the tape", dict(tape_assets=(other,) + live[1:])),
        (f"D-7 PLANT (one record short: {live[0]} gone)",
         "assets in the D-7 record", dict(cal_assets=live[1:])),
    )

    def _break() -> tuple[bool, str]:
        green, out = False, []
        for name, must, kw in plants:
            if kw is None:
                green = True
                out.append(f"{name} -> GREEN: the plant could not be planted")
                continue
            bad, _x = _roster_judge(**kw)
            hits = [b for b in bad if must in b]
            if hits:
                rest = [b for b in bad if must not in b]
                out.append(f"{name} -> RED: {hits[0]}"
                           + (f" [and {len(rest)} other finding(s), first: {rest[0]}]" if rest else ""))
            else:
                green = True
                out.append(f"{name} -> " + ("GREEN" if not bad else
                           f"RED FOR THE WRONG REASON (no finding says {must!r}; first: {bad[0]})"))
        return green, " ‖ ".join(out)

    def _real() -> tuple[bool, str]:
        bad, x = _roster_judge()
        if bad:
            return False, "; ".join(bad[:6]) + (f" (+{len(bad) - 6} more)" if len(bad) > 6 else "")
        n = len(x["literal"])
        mapped = ", ".join(f"{d} -> {lv}" for d, lv in x["maps"].items()) or "none"
        return True, (
            f"REGISTER['ROSTER'] is a LITERAL tuple of {n} at oracle_daily.py:{x['line']}, equal IN "
            f"ORDER to KEPT ∪ ruled mappings: the {len(x['kept'])} KEPT of {x['probe']} (every record "
            f"KEEP · PERPETUAL · TRADING) + {len(x['maps'])} mapped by {ROSTER_MAPPING_RULING} "
            f"({mapped}; record {x['mapping']}, PERPETUAL · TRADING · USDT, in the dropped name's "
            f"place); the {len(x['dropped'])} DROPPED BY RULING ({', '.join(x['dropped'])}) are off "
            f"it and named in the row's source, which quotes ruling 1 verbatim and is 'ruled': True; "
            f"oracle_daily.py does not name the study basket; no second symbol list in "
            f"{len(ROSTER_FAMILY)} family files ({', '.join(ROSTER_FAMILY)}); the live row equals "
            f"the source literal; and artifact set {DATE} was printed from exactly this roster — "
            f"{x['strips']} mantle strips, {x['tape']} tape assets, {x['cal']} D-7 records. "
            f"Roster: {' '.join(x['literal'])}")

    prove("F-BR-16", "ROSTER — one literal definition: the probe's KEPT list plus the ruled "
                     "mappings, in the operator's order, no second list, and the edition "
                     "under test printed from it",
          _break, _real)


# ═══════ F-BR-17 · THE ORACLE NEVER FETCHES, AND NEVER WRITES THE KLINE CACHE
#
# WHAT THIS GUARDS. OR-1 hard rule 6: "the Oracle (oracle_daily.py) never fetches from
# the network". The whole build rests on it — the top-up is a SEPARATE process that
# runs first and may fail; ruling T-3 then has the Oracle render on a stale cache with
# the LATE EDITION band showing, which is only honest if the render cannot quietly go
# and get the bars itself. The sandbox gate's own docstring rests on it too ("the kline
# cache is READ — the Oracle is cache-only and never writes it").
#
# NOTHING PROVED IT. The movers organ got two fixtures for exactly this pair of
# properties (F-MV-1 fingerprints the whole 632 MB cache across a real run; F-MV-2
# scans for network names). The Oracle got neither: F-BR-3's ban lists are
# BANNED_IN_DECISION = ('analytics',) and BANNED_ANYWHERE = ('forward_log',
# 'positions') — nothing network, nothing cache-writing — and it measures the IMPORT
# CLOSURE, which cannot see a lazy `from engine.data import backfill_klines` inside a
# function (oracle_daily.py:1900's `import oracle_topup as _TU` is already outside that
# measurement, and oracle_topup's module DOES reach backfill_klines). F-MV-9 scans for
# network names but only inside load_movers / movers_top / market_page. Measured in a
# mirror of the repo: a module-level `import requests` plus `_get(...)`,
# `requests.get(...)` and `backfill_klines('BTCUSDT','4h')` inside build_view — the
# "just top up the missing bars inline" edit — passed the suite 16/16 GREEN, and the
# sandbox gate still printed "live lane untouched: True", because its fingerprint
# covers briefs/oracle, the tape, the calibration, the payloads and posture_canon.json
# and NEVER the kline cache.
#
# WHAT THIS DOES. Every top-level function of the two files the Oracle renders from,
# plus their class bodies and their module level, scanned as CODE for the names a fetch
# or a cache write must spell: ast.Name.id, ast.Attribute.attr, and the names inside
# ast.Import / ast.ImportFrom — so an import INSIDE a function is caught, which is
# precisely what a closure measured at import time cannot see.
#
# DISCLOSED, NOT DENIED. Two names are legitimate and are pinned to their one home
# each, with the call site named: naming either anywhere else is red.
#
# WHAT IT DOES NOT PROVE: that the cache is byte-identical across a run (that is
# F-MV-1's shape, and it needs a real run and ~830 MB of hashing); nor anything about
# modules oracle_daily imports — `requests` is ALREADY in its closure on untouched
# code, via engine/data.py:29, which the Oracle reaches for `cache_dir`. That is why
# this is a NAMING test on the Oracle's own sources and not a closure ban: the closure
# ban cannot be written without banning the module the Oracle legitimately reads the
# cache through.

NF_FILES = ("scripts/oracle_daily.py", "scripts/posture_engine.py")
NF_NET = ("_get", "requests", "urlopen", "urllib", "socket", "REST_BASE", "httpx",
          "aiohttp")
NF_CACHE_WRITE = ("backfill_klines", "backfill_funding", "_save_cache", "write_parquet",
                  "_kline_path", "_funding_path", "topup_pair")
# name -> the only places it may be spelled. WHY each one is here:
NF_ALLOWED = {
    # engine.data.cache_dir() mkdirs, so the movers organ bans it outright; the Oracle
    # needs it to READ the klines parquet at oracle_daily.py:529 (load_lens). Its
    # module-level import is the same permission.
    "cache_dir": ("<module level>", "load_lens"),
    # the two tape writes: the D-4 recording into the REDIRECTABLE TAPE_DIR, and (A-OR1-1
    # v, 2026-09-22) the range layer's sibling tape into the REDIRECTABLE TAPE_RANGES_DIR
    # — recordings, not the cache. Every fixture in this file redirects both into a temp dir.
    "to_parquet": ("write_tape", "write_range_tape"),
}
# if any of these is missing the scan is blind and says so rather than passing
NF_MUST_EXIST = ("build_view", "load_lens", "write_tape", "write_range_tape", "render_html",
                 "run")


def _nofetch_hits(node, where: str):
    """(lineno, where, how, name) for every way one of the watched names is SPELLED
    under `node`. Strings are not scanned: a name is a name, not a sentence."""
    watched = set(NF_NET) | set(NF_CACHE_WRITE) | set(NF_ALLOWED)
    for n in ast.walk(node):
        if isinstance(n, ast.Name) and n.id in watched:
            yield n.lineno, where, "the name", n.id
        elif isinstance(n, ast.Attribute) and n.attr in watched:
            yield n.lineno, where, "the attribute", n.attr
        elif isinstance(n, (ast.Import, ast.ImportFrom)):
            parts = {p for a in n.names for p in a.name.split(".")}
            parts |= {a.asname for a in n.names if a.asname}
            parts |= set((getattr(n, "module", None) or "").split("."))
            for p in sorted(parts & watched):
                yield n.lineno, where, "an import of", p


def _nofetch(sources: dict[str, str] | None = None) -> tuple[list[str], dict]:
    src = ({f: (ROOT / f).read_text(encoding="utf-8") for f in NF_FILES}
           if sources is None else sources)
    bad, hits = [], []
    for path, text in src.items():
        tree = ast.parse(text)
        tops = {}
        rest = []
        for s in tree.body:
            if isinstance(s, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                tops[s.name] = s
            else:
                rest.append(s)
        for name, node in tops.items():
            hits += [(path, *h) for h in _nofetch_hits(node, name)]
        hits += [(path, *h) for h in
                 _nofetch_hits(ast.Module(body=rest, type_ignores=[]), "<module level>")]
        if path.endswith("oracle_daily.py"):
            gone = [f for f in NF_MUST_EXIST if f not in tops]
            if gone:
                bad.append(f"{path}: {gone} not found at top level — the scan cannot say "
                           f"where a fetch would live; fail closed")
    for path, line, where, how, name in hits:
        homes = NF_ALLOWED.get(name)
        if homes is not None:
            if where not in homes:
                bad.append(f"{path}:{line} {where} names {how} `{name}` — it is disclosed "
                           f"for {list(homes)} only")
            continue
        why = ("the Oracle is CACHE-ONLY and never fetches (OR-1 hard rule 6)"
               if name in NF_NET else
               "the Oracle never WRITES the kline cache — that is the top-up's job, in "
               "its own process, before the render")
        bad.append(f"{path}:{line} {where} names {how} `{name}` — {why}")
    return bad, {"files": len(src), "hits": len(hits),
                 "allowed": sorted(f"{n} in {w}" for _p, _l, w, _h, n in hits
                                   if n in NF_ALLOWED)}


def f_br_17() -> None:
    src = {f: (ROOT / f).read_text(encoding="utf-8") for f in NF_FILES}
    od = "scripts/oracle_daily.py"
    inline = ("        from engine.data import REST_BASE, _get, backfill_klines\n"
              "        if len(roster) < 0:\n"
              "            _get(REST_BASE + '/fapi/v1/ticker/24hr')\n"
              "            requests.get(REST_BASE)\n"
              "            backfill_klines('BTCUSDT', '4h')\n")

    def plant_in(fn: str, stmt: str, head: str = "") -> dict[str, str] | None:
        out = _range_plant_in(src[od], fn, stmt)
        return None if out is None else {**src, od: head + out}

    plants = (
        ("NET PLANT (a module-level `import requests` on a copy of oracle_daily.py)",
         "never fetches",
         lambda: _nofetch({**src, od: "import requests\n" + src[od]})[0]),
        ("NET PLANT (the 'just top up the missing bars inline' edit: engine.data's "
         "REST_BASE/_get imported INSIDE build_view and called — the shape no import "
         "closure measured at import time can see)",
         "never fetches",
         lambda: (lambda p: _nofetch(p)[0] if p else [])(
             plant_in("build_view", "from engine.data import REST_BASE, _get\n"
                                    "_p = _get(REST_BASE)"))),
        ("CACHE PLANT (backfill_klines imported and called inside build_view)",
         "never WRITES the kline cache",
         lambda: (lambda p: _nofetch(p)[0] if p else [])(
             plant_in("build_view", "from engine.data import backfill_klines\n"
                                    "backfill_klines('BTCUSDT', '4h')"))),
        ("ALLOW-LIST PLANT (`cache_dir` — disclosed for load_lens — named in build_view)",
         "is disclosed for",
         lambda: (lambda p: _nofetch(p)[0] if p else [])(
             plant_in("build_view", "_p = cache_dir()"))),
        ("FAIL-CLOSED PLANT (build_view renamed away, so the scan has nothing to scan)",
         "fail closed",
         lambda: _nofetch({**src, od: src[od].replace("\ndef build_view(",
                                                     "\ndef _renamed_build_view(", 1)})[0]),
    )

    def _break() -> tuple[bool, str]:
        green, out = False, []
        for name, must, judge in plants:
            bad = judge()
            hits = [b for b in bad if must in b]
            if hits:
                rest = [b for b in bad if must not in b]
                out.append(f"{name} -> RED: {hits[0]}"
                           + (f" (+{len(hits) - 1} more of its kind)" if len(hits) > 1 else "")
                           + (f" [and {len(rest)} other finding(s), first: {rest[0]}]" if rest else ""))
            else:
                green = True
                out.append(f"{name} -> " + ("GREEN" if not bad else
                           f"RED FOR THE WRONG REASON (no finding says {must!r}; first: {bad[0]})"))
        return green, " ‖ ".join(out)

    def _real() -> tuple[bool, str]:
        bad, x = _nofetch()
        if bad:
            return False, "; ".join(bad[:6]) + (f" (+{len(bad) - 6} more)" if len(bad) > 6 else "")
        return True, (
            f"{x['files']} source file(s) ({', '.join(NF_FILES)}), every top-level function, "
            f"class body and the module level, scanned as CODE (ast.Name, ast.Attribute and "
            f"the names inside every import statement, so an import INSIDE a function is "
            f"caught): not one of the {len(NF_NET)} network names ({', '.join(NF_NET)}) and "
            f"not one of the {len(NF_CACHE_WRITE)} cache-writing names "
            f"({', '.join(NF_CACHE_WRITE)}) is spelled anywhere. The {len(NF_ALLOWED)} "
            f"DISCLOSED names are each in their one home and nowhere else: {x['allowed']} "
            f"(cache_dir READS the klines parquet in load_lens; to_parquet writes the D-4 "
            f"tape into the redirectable TAPE_DIR and the sibling range tape into the "
            f"redirectable TAPE_RANGES_DIR, never the cache). "
            f"{list(NF_MUST_EXIST)} all exist, so the scan is not hunting a renamed file. "
            f"NOT PROVED HERE: that the cache bytes are unchanged across a run (F-MV-1's "
            f"shape), nor anything about the import closure — `requests` is already in "
            f"oracle_daily's closure via engine.data, which it reaches for cache_dir.")

    prove("F-BR-17", "THE ORACLE NEVER FETCHES AND NEVER WRITES THE KLINE CACHE — no "
                     "network name and no cache-writing name in oracle_daily.py or "
                     "posture_engine.py, at module level or inside any function",
          _break, _real)


# ═════════════════ F-BR-18 · PER-ROW STALENESS (OR-2 STEP 3, R-1)
#
# WHAT THIS GUARDS. OR-1 finding OR1-a, the skeptic's plant: with ONE symbol's tape
# cut back 3 days in memory, the dateline still named the hottest asset's bar, the
# LATE EDITION band stayed silent, and that symbol's Board row, Trap Card and R1
# alert prices printed from an 84-hour-old bar with no mark. Operator ruling R-1
# (2026-09-22): every row carries its own as-of bar and age; past A2-7's limit it
# reads STALE on the Board and on its Docket card header (with its age); its R1
# lines LEAVE the paste-ready block and print beneath it under "HELD — stale wire",
# struck through; the dateline prints the newest AND the oldest row's bar; the band
# fires when ANY row is stale and names the count; the wrapper's report-back prints
# the count.
#
# HOW. The plant, replayed: OD.load_lens wrapped so the victim's every interval ends
# 3 days before the OTHER rows' common last bar T0 — and the others are held at T0
# too, so a ragged live cache (a pair the top-up missed) cannot leak a second stale
# row into the control — then a fresh build_view, and renders PRINTED at T0 + one
# lens period. The victim is DERIVED (the coolest row with a Trap Card whose cut view
# keeps an R1 line and is not the hottest), never typed. Four pages are judged, each
# against an expectation computed HERE from the rows' own bars and A2-7's pinned
# period count (TS_LENS_PERIODS), never read off the module:
#   REPLAY   the contract's plant: 1 of R stale;
#   HOTTEST  the same view with the victim's heat raised above every other row, so the
#            view's (hottest) as-of IS the stale bar — the dateline's "newest" must
#            still be T0 and the lead must still name the span;
#   CARDLESS a second row, one WITHOUT a Trap Card, set 3 days back as well (its bar
#            only) — its LIS lines must leave the paste block too: 2 of R;
#   FRESH    the victim's bar put back to T0 — 0 of R, no band, no HELD block.
# On each: every Board row's own bar and age (floor bars, hours to 0.1) and a STALE
# chip exactly where stale; every Trap Card header's chip and age exactly where
# stale; the paste block = the fresh rows' lines in order, the HELD block = the stale
# rows' lines, EACH struck through; band, dateline, lead; and the wrapper's real
# front_page() report-back over a planted log. Plus A2-7's arithmetic on a synthetic
# row: exactly at the limit is fresh, one ms past it stale, whole bars elapsed (floor:
# 4h24m is 1 bar · 4.4h), and the limit follows
# OD.STALE_LENS_PERIODS (never a retyped number).

BR18_CUT_MS = 3 * 86_400_000
BR18_HELD = "HELD — stale wire"
BR18_CHIP_BOARD = "<span class='chip stale'>STALE</span>"
BR18_CHIP_CARD = '<span class="chip stale">STALE</span>'
BR18_SCENES = ("REPLAY", "HOTTEST", "CARDLESS", "FRESH")
_BR18 = None


def _br18_restation(a: dict, as_of_ms: int) -> dict:
    """A COPY of a row whose station reads another as-of bar (the shared view untouched)."""
    import copy
    st = copy.copy(a["station"])
    st.as_of_ms = int(as_of_ms)
    return dict(a, station=st)


def _br18_setup() -> dict:
    """The cut view and its four scene views, built ONCE per suite run (fails closed)."""
    global _BR18
    if _BR18 is not None:
        return _BR18
    from datetime import datetime, timezone
    base = _pristine_view()                        # cached BEFORE the loader is wrapped
    step = OD.LENS_MS[base["lens"]]
    hottest = base["assets"][0]["symbol"]
    lasts = {a["symbol"]: int(a["station"].as_of_ms) for a in base["assets"]}
    cands = [a["symbol"] for a in reversed(base["assets"]) if a["card"] and a["symbol"] != hottest]
    real_ll = OD.load_lens
    for victim in cands:
        t0 = min(t for sym, t in lasts.items() if sym != victim)

        def _cut(sym, tf, tail=None, _v=victim, _t0=t0):
            lim = (_t0 - BR18_CUT_MS if sym == _v else _t0) + step   # every bar opening before
            df = real_ll(sym, tf)                                     # the NEXT lens bar
            df = df[df["open_time"] < lim].reset_index(drop=True)
            return df if tail is None or len(df) <= tail else df.iloc[-tail:].reset_index(drop=True)
        try:
            OD.load_lens = _cut
            view = OD.build_view(log=lambda *a, **k: None)
        finally:
            OD.load_lens = real_ll
        vic = next(a for a in view["assets"] if a["symbol"] == victim)
        vic_lines = [ln for ln in OD.r1_block(view).split("\n") if ln.startswith(victim + " ")]
        if not vic_lines or not vic["card"] or view["assets"][0]["symbol"] == victim:
            continue
        other = next((a for a in reversed(view["assets"]) if not a["card"] and a["symbol"] != victim
                      and any(ln.startswith(a["symbol"] + " ")
                              for ln in OD.r1_block(view).split("\n"))), None)
        if other is None:
            continue
        top = max(a["heat"] for a in view["assets"])
        hot = [dict(a, heat=top + 1.0) if a["symbol"] == victim else a for a in view["assets"]]
        hot.sort(key=lambda a: -a["heat"])
        scenes = {
            "REPLAY": view,
            "HOTTEST": {**view, "assets": hot, "as_of_ms": int(vic["station"].as_of_ms)},
            "CARDLESS": {**view, "assets": [_br18_restation(a, t0 - BR18_CUT_MS)
                                            if a["symbol"] == other["symbol"] else a
                                            for a in view["assets"]]},
            "FRESH": {**view, "assets": [_br18_restation(a, t0) if a["symbol"] == victim else a
                                         for a in view["assets"]]},
        }
        at_ms = t0 + step
        state = {"view": view, "scenes": scenes, "victim": victim, "other": other["symbol"],
                 "t0": t0, "at_ms": at_ms, "step": step, "loader": _cut,
                 "at": datetime.fromtimestamp(at_ms / 1000, timezone.utc),
                 "hottest_ms": int(view["assets"][0]["station"].as_of_ms)}
        _BR18 = state                              # published only once complete
        return _BR18
    raise RuntimeError("F-BR-18 cannot be planted: no roster symbol keeps a Trap Card and an "
                       "R1 line with its tape cut back 3 days beside a card-less row with R1 "
                       "lines — fail closed")


def _br18_render(scene: str) -> str:
    """One scene printed at the setup's instant, under the cut loader (the Spaghetti
    reads load_lens again while it renders)."""
    real_ll = OD.load_lens
    try:
        OD.load_lens = _BR18["loader"]
        return OD.render_html(_BR18["scenes"][scene], DATE, PE.canon_sha(), printed_at=_BR18["at"])
    finally:
        OD.load_lens = real_ll


def _br18_arith() -> list[str]:
    """A2-7's arithmetic on one synthetic row, through OD.row_ages: at the limit fresh,
    one ms past it stale, floor bars, and the limit FOLLOWS OD.STALE_LENS_PERIODS."""
    from datetime import datetime, timezone
    from types import SimpleNamespace as NS
    step = OD.LENS_MS["4h"]
    limit = TS_LENS_PERIODS * step
    view = {"lens": "4h", "assets": [{"symbol": "AAA", "station": NS(as_of_ms=0)}]}
    at = lambda ms: datetime.fromtimestamp(ms / 1000, timezone.utc)   # noqa: E731
    bad = []
    if OD.row_ages(view, at(limit))["rows"]["AAA"]["stale"]:
        bad.append(f"boundary: a bar exactly {limit / 3.6e6:g}h old reads STALE — A2-7 is 'older than'")
    if not OD.row_ages(view, at(limit + 1))["rows"]["AAA"]["stale"]:
        bad.append("boundary: a bar 1 ms past A2-7's limit reads fresh")
    r = OD.row_ages(view, at(step + 24 * 60_000))["rows"]["AAA"]
    if (r["age_bars"], f"{r['age_h']:.1f}") != (1, "4.4"):
        bad.append(f"age: 4h24m reads {r['age_bars']} bar(s) · {r['age_h']:.1f}h, want 1 bar · 4.4h "
                   f"(whole bars elapsed, floor)")
    keep = OD.STALE_LENS_PERIODS
    try:
        OD.STALE_LENS_PERIODS = keep + 1
        moved = OD.row_ages(view, at(limit + 1))
    finally:
        OD.STALE_LENS_PERIODS = keep
    if moved["rows"]["AAA"]["stale"] or moved["limit_ms"] != (keep + 1) * step:
        bad.append("the limit does not follow OD.STALE_LENS_PERIODS — a retyped number")
    return bad


def _br18_expect(scene: str) -> dict:
    """The expectation for a scene, computed HERE from its rows' own bars."""
    x = _BR18
    v = x["scenes"][scene]
    limit = TS_LENS_PERIODS * x["step"]
    rows = {}
    for a in v["assets"]:
        t = int(a["station"].as_of_ms)
        age = x["at_ms"] - t
        n = age // x["step"]
        rows[a["symbol"]] = {"t": t, "stale": age > limit, "card": bool(a["card"]),
                             "age": f"{n} bar{'' if n == 1 else 's'} · {age / 3_600_000:.1f}h"}
    ts = [r["t"] for r in rows.values()]
    lines = [ln for ln in OD.r1_block(v).split("\n") if ln]
    stale = {sym for sym, r in rows.items() if r["stale"]}
    return {"rows": rows, "stale": stale, "newest": max(ts), "oldest": min(ts), "R": len(rows),
            "paste": [ln for ln in lines if ln.split(" ", 1)[0] not in stale],
            "held": [ln for ln in lines if ln.split(" ", 1)[0] in stale]}


BR18_WANT_STALE = {"REPLAY": 1, "HOTTEST": 1, "CARDLESS": 2, "FRESH": 0}


def _br18_judge(scene: str, page: str) -> list[str]:
    import html as _h
    from datetime import datetime, timezone
    x, e = _BR18, _br18_expect(scene)
    st = OD.as_of_stamp
    tag = f"[{scene}]"
    bad: list[str] = []
    if len(e["stale"]) != BR18_WANT_STALE[scene]:
        return [f"{tag} the plant made {sorted(e['stale'])} stale, want {BR18_WANT_STALE[scene]} "
                f"row(s) — the scene is not what it claims (fail closed)"]
    # ── the Board: EVERY row's own bar and age, and the chip exactly where stale
    rows = dict(re.findall(r"(?s)<tr class='w-[a-z_-]+'><td class='sym'>([^<]+)</td>(.*?)</tr>",
                           _sec(page, SEC_BOARD)))
    for sym, r in e["rows"].items():
        k = sym.replace("USDT", "")
        body = rows.get(k)
        if body is None:
            bad.append(f"{tag} the Board carries no row for {k}")
            continue
        if st(r["t"]) not in body or r["age"] not in body:
            bad.append(f"{tag} {k}'s Board row does not print its own bar {st(r['t'])} and age "
                       f"'{r['age']}'")
        if r["stale"] and BR18_CHIP_BOARD not in body:
            bad.append(f"{tag} {k}'s Board row reads no STALE mark — its bar is past A2-7's limit")
        if not r["stale"] and BR18_CHIP_BOARD in body:
            bad.append(f"{tag} {k}'s Board row reads STALE on a fresh bar — the control is broken")
    # ── The Docket: every card's header, chip and age exactly where stale
    for k, head in re.findall(r'(?s)<div class="card-h"><b>([^<]+)</b>(.*?)</div>', page):
        r = e["rows"].get(k + "USDT") or e["rows"].get(k)
        if r is None:
            continue
        if r["stale"] and (BR18_CHIP_CARD not in head or f"bar {st(r['t'])} · {r['age']}" not in head):
            bad.append(f"{tag} {k}'s Trap Card header does not read STALE with its bar and age")
        if not r["stale"] and BR18_CHIP_CARD in head:
            bad.append(f"{tag} {k} reads STALE on its Trap Card on a fresh bar")
    # ── the Telegrams: routed, never retyped; every HELD line struck through
    tel = _sec(page, SEC_TELEGRAMS)
    mp = re.search(r'(?s)<pre class="r1">(.*?)</pre>', tel)
    mh = re.search(r'(?s)<pre class="held">(.*?)</pre>', tel)
    paste = [ln for ln in _h.unescape(mp.group(1)).split("\n") if ln.strip()] if mp else None
    raw = [ln for ln in mh.group(1).split("\n") if ln.strip()] if mh else []
    held = [_h.unescape(re.sub(r"</?s>", "", ln)) for ln in raw]
    if paste is None:
        bad.append(f"{tag} no paste-ready R1 block in the Telegrams")
    else:
        inside = [ln for ln in e["held"] if ln in paste]
        if inside:
            bad.append(f"{tag} {len(inside)} stale line(s) are in the paste block: {inside[0]!r}")
        elif paste != e["paste"]:
            bad.append(f"{tag} the paste block is not the fresh rows' R1 lines, in order, byte for byte")
    if held != e["held"]:
        bad.append(f"{tag} the HELD block reads {held[:2]}, want {e['held'][:2]} "
                   f"({len(e['held'])} line(s))")
    if e["held"]:
        if BR18_HELD not in tel or tel.find(BR18_HELD) < tel.find('<pre class="r1">'):
            bad.append(f"{tag} the HELD lines are not under '{BR18_HELD}', beneath the paste block")
        unstruck = [ln for ln in raw if not re.fullmatch(r"<s>[^<]*</s>", ln.strip())]
        if unstruck:
            bad.append(f"{tag} {len(unstruck)} HELD line(s) are not struck through: {unstruck[0][:60]!r}")
    elif mh or BR18_HELD in tel:
        bad.append(f"{tag} a HELD block prints with no stale row")
    # ── the band, the dateline, the lead
    band = _ts_band(page)
    if e["stale"]:
        want = TS_BAND_HEAD.format(n=len(e["stale"]), r=e["R"], as_of=st(e["oldest"]))
        if band is None or not band.startswith(want):
            bad.append(f"{tag} the band opens {(band or 'nothing')[:70]!r}, want {want!r}")
    elif band is not None:
        bad.append(f"{tag} the band is up with no stale row: {band[:60]!r}")
    dl = re.search(r'(?s)<p class="dateline">(.*?)</p>', page)
    dtxt = _page_text(dl.group(1)) if dl else ""
    for frag in (f"newest {st(e['newest'])}", f"oldest {st(e['oldest'])}",
                 f"{len(e['stale'])} of {e['R']} rows stale"):
        if frag not in dtxt:
            bad.append(f"{tag} the dateline does not say '{frag}' ({dtxt[:90]!r})")
    ld = re.search(r'(?s)<p class="lead">(.*?)</p>', page)
    ltxt = _page_text(ld.group(1)) if ld else ""
    want_lead = (f"at the bar of {st(e['newest'])}" if e["newest"] == e["oldest"] else
                 f"from {st(e['oldest'])} to {st(e['newest'])}")
    if want_lead not in ltxt:
        bad.append(f"{tag} the lead does not say '{want_lead}' ({ltxt[:110]!r})")
    # ── the wrapper's REAL report-back, over a planted log of this page
    import oracle_wrapper as _OW
    with tempfile.TemporaryDirectory(prefix="f-br-18-") as td:
        fp = Path(td) / "page.html"
        fp.write_text(page, encoding="utf-8")
        logged: list[str] = []
        lines = [f"  {a['symbol']:14} {a['station'].board_word:10} heat={a['heat']:6.3f}"
                 for a in x["scenes"][scene]["assets"]]
        lines.append(f"  render {fp} sha256 {hashlib.sha256(page.encode()).hexdigest()}")
        _OW.front_page(lines, "fixture-F-BR-18", datetime.now(timezone.utc), log=logged.append)
    want_rep = f"  STALE {len(e['stale'])} of {e['R']} Board rows on a stale wire"
    if not any(ln.startswith(want_rep) for ln in logged):
        got = [ln for ln in logged if ln.startswith("  STALE")]
        bad.append(f"{tag} the wrapper's report-back says {got[:1] or 'nothing'}, want {want_rep.strip()!r}")
    return bad


def _br18_all(scenes=BR18_SCENES, arith: bool = True) -> list[str]:
    bad = []
    for sc in scenes:
        bad += _br18_judge(sc, _br18_render(sc))
    return bad + (_br18_arith() if arith else [])


def f_br_18() -> None:
    x = _br18_setup()
    real_ages, real_held, real_split = OD.row_ages, OD.held_block, OD.r1_split

    def _planted(scenes, od=None, ow=None, late=None) -> list[str]:
        """Re-render the scenes with module attributes swapped, then judge."""
        import oracle_wrapper as _OW
        keep_od = {k: getattr(OD, k) for k in (od or {})}
        keep_ow = {k: getattr(_OW, k) for k in (ow or {})}
        keep_late = OD.REGISTER["LATE_EDITION"]["value"]
        try:
            for k, v in (od or {}).items():
                setattr(OD, k, v)
            for k, v in (ow or {}).items():
                setattr(_OW, k, v)
            if late is not None:
                OD.REGISTER["LATE_EDITION"]["value"] = late
            return _br18_all(scenes, arith=not scenes)     # a scene plant judges its scene only
        finally:
            for k, v in keep_od.items():
                setattr(OD, k, v)
            for k, v in keep_ow.items():
                setattr(_OW, k, v)
            OD.REGISTER["LATE_EDITION"]["value"] = keep_late

    def _ages_ge(view, printed_at=None):            # A2-7's boundary moved to >=
        r = real_ages(view, printed_at)
        for row in r["rows"].values():
            row["stale"] = row["age_ms"] >= r["limit_ms"]
        return {**r, "stale": [k for k, row in r["rows"].items() if row["stale"]]}

    def _ages_typed(view, printed_at=None):         # the limit retyped, not read
        r = real_ages(view, printed_at)
        lim = 2 * 14_400_000
        for row in r["rows"].values():
            row["stale"] = row["age_ms"] > lim
        return {**r, "limit_ms": lim, "stale": [k for k, row in r["rows"].items() if row["stale"]]}

    def _strike_first(held, ages, lens):             # only the first HELD line struck
        out = real_held(held, ages, lens)
        head, sep, tail = out.partition("</s>")
        return head + sep + tail.replace("<s>", "").replace("</s>", "") if sep else out

    def _cards_only(view, stale):                    # holds only rows that carry a card
        carded = {a["symbol"] for a in view["assets"] if a["card"]}
        return real_split(view, [k for k in stale if k in carded])

    plants = (
        ("THE CONTRACT'S PLANT (the hottest-asset-only as-of restored: every row judged by the "
         "hottest asset's bar)", "reads no STALE mark",
         dict(scenes=("REPLAY",), od=dict(row_as_of_ms=lambda a, _t=x["hottest_ms"]: _t))),
        ("ROUTING PLANT (the stale row's R1 lines left in the paste block)", "in the paste block",
         dict(scenes=("REPLAY",), od=dict(r1_split=lambda view, stale: (OD.r1_block(view), "")))),
        ("CARDLESS PLANT (only rows with a Trap Card held; a stale STALKING/DEAD row's LIS lines "
         "stay pasteable)", "in the paste block",
         dict(scenes=("CARDLESS",), od=dict(r1_split=_cards_only))),
        ("WORDING PLANT (OR-1's band: 'LATE EDITION — wire stale since <as-of>')", "the band opens",
         dict(scenes=("REPLAY",), late="LATE EDITION — wire stale since {as_of}")),
        ("NEWEST PLANT (the dateline's 'newest' taken from the view's — the hottest row's — as-of)",
         "the dateline does not say 'newest",
         dict(scenes=("HOTTEST",), od=dict(row_ages=lambda v, p=None: {**real_ages(v, p),
                                                                          "newest_ms": int(v["as_of_ms"])}))),
        ("AGE-CELL PLANT (fresh rows print the epoch instead of their own bar)",
         "does not print its own bar",
         dict(scenes=("REPLAY",), od=dict(age_cell=lambda r, _real=OD.age_cell: _real(
             r if r["stale"] else {**r, "as_of_ms": 0})))),
        ("DOCKET PLANT (every Trap Card marked STALE, fresh or not)", "on its Trap Card on a fresh bar",
         dict(scenes=("REPLAY",), od=dict(age_chip=lambda r, _real=OD.age_chip: _real({**r, "stale": True})))),
        ("DOCKET-AGE PLANT (the card's chip without its bar and age)", "Trap Card header does not read",
         dict(scenes=("REPLAY",), od=dict(age_chip=lambda r: BR18_CHIP_CARD if r["stale"] else ""))),
        ("STRIKE PLANT (only the first HELD line struck through)", "not struck through",
         dict(scenes=("REPLAY",), od=dict(held_block=_strike_first))),
        ("REPORT-BACK PLANT (the wrapper's STALE line gone quiet)", "the wrapper's report-back",
         dict(scenes=("FRESH",), ow=dict(stale_state=lambda p: "unknown — planted"))),
        ("BOUNDARY PLANT (A2-7's 'older than' read as '>=')", "boundary",
         dict(scenes=(), od=dict(row_ages=_ages_ge))),
        ("RETYPED PLANT (the limit typed as 2 x 4h, not read off STALE_LENS_PERIODS)",
         "a retyped number", dict(scenes=(), od=dict(row_ages=_ages_typed))),
    )

    def _break() -> tuple[bool, str]:
        green, out = False, []
        for name, must, kw in plants:
            bad = _planted(**kw)
            hits = [b for b in bad if must in b]
            if hits:
                rest = [b for b in bad if must not in b]
                out.append(f"{name} -> RED: {hits[0]}"
                           + (f" [and {len(rest)} other finding(s)]" if rest else ""))
            else:
                green = True
                out.append(f"{name} -> " + ("GREEN" if not bad else
                           f"RED FOR THE WRONG REASON (no finding says {must!r}; first: {bad[0]})"))
        return green, " ‖ ".join(out)

    def _real() -> tuple[bool, str]:
        bad = _br18_all()
        if bad:
            return False, "; ".join(bad[:6]) + (f" (+{len(bad) - 6} more)" if len(bad) > 6 else "")
        v, o = x["victim"].replace("USDT", ""), x["other"].replace("USDT", "")
        R = len(x["view"]["assets"])
        e = _br18_expect("REPLAY")
        return True, (
            f"OR1-a replayed: {v}'s tape cut back 3 days in memory below the other rows' common "
            f"bar {OD.as_of_stamp(x['t0'])}, printed at {x['at']:%Y-%m-%dT%H:%MZ} (+1 lens period). "
            f"REPLAY: {v} reads STALE with its own bar and age "
            f"({e['rows'][x['victim']]['age']}) on the Board and on its Trap Card header, every "
            f"other of the {R} Board rows prints its own bar and age with no mark, and no other card "
            f"reads STALE; {v}'s {len(e['held'])} R1 line(s) are out of the paste block (every fresh "
            f"row's line, in order, byte for byte) and beneath it under '{BR18_HELD}', each struck "
            f"through; the band opens '{TS_BAND_HEAD.format(n=1, r=R, as_of=OD.as_of_stamp(e['oldest']))}'; "
            f"the dateline names newest and oldest and '1 of {R} rows stale'; the lead names the span; "
            f"the wrapper's real front_page() logs 'STALE 1 of {R} Board rows on a stale wire'. "
            f"HOTTEST ({v} made the hottest row): the dateline's newest is still "
            f"{OD.as_of_stamp(x['t0'])}. CARDLESS ({o}, no Trap Card, set 3 days back too): 2 of {R}, "
            f"its LIS lines HELD. FRESH ({v}'s bar restored): 0 of {R}, no band, no HELD block, "
            f"report-back 'STALE 0 of {R}'. A2-7 arithmetic: exactly at the limit fresh, 1 ms past "
            f"it stale, 4h24m = 1 bar · 4.4h, and the limit follows OD.STALE_LENS_PERIODS")

    prove("F-BR-18", "PER-ROW STALENESS — a row whose own bar is past A2-7's limit reads "
                     "STALE, its R1 lines are HELD out of the paste block, and the band names "
                     "the count (OR1-a replayed)",
          _break, _real)

# ═════════════════ F-BR-19 · POSTURE-FIRST BOARD (OR-2 STEP 4, R-2)
#
# WHAT THIS GUARDS. Operator ruling R-2 (2026-09-22): named constant BOARD_ORDER =
# (TRIGGERED, ARMED, STALKING, DEAD); the Board, The Docket and the wrapper's
# front-page report-back list rows posture FIRST and heat descending within a
# posture; heat values unchanged and still printed; nothing else re-ordered. On the
# day this was built the recovery edition's Board, sorted by heat alone, had six
# rows sitting above rows of a higher posture — two TRIGGERED Trap Cards below ARMED
# ones on The Docket.
#
# HOW. (a) the edition under test, parsed by its own header (robust to added
# columns): no row sits above a row of higher posture, heat descends within one; the
# Docket's cards follow the Board's word for their symbol; and The Watch still runs
# by heat (R-2's "only"). (b) a HARD render: the real view with its heats reassigned
# so heat order INVERTS posture order, rendered fresh and judged the same way. (c)
# OD.board_rows on six synthetic rows with a typed expected order. (d) the wrapper's
# front_page_rows on synthetic log lines. (e) the constant itself, typed here from the
# queue, set-equal to posture_engine's words, and defined once (no four-word list in
# the wrapper). Break: the contract's heat-only sort; the wrapper left on heat; The
# Docket left on the view's order (a source mutant); BOARD_PRECEDENCE's order.

F19_ORDER = ("TRIGGERED", "ARMED", "STALKING", "DEAD")   # the ruling, typed from the queue
F19_SYNTH = (("AAA", "STALKING", 9.0), ("BBB", "TRIGGERED", 1.0), ("CCC", "DEAD", 8.0),
             ("DDD", "ARMED", 5.0), ("EEE", "TRIGGERED", 3.0), ("FFF", "ARMED", 7.0))
F19_SYNTH_WANT = ("EEE", "BBB", "FFF", "DDD", "AAA", "CCC")


def _br19_board(doc: str) -> list[tuple[str, str, float]]:
    """(symbol, posture word, printed heat) of every Board row, in page order."""
    board = _sec(doc, SEC_BOARD)
    hdr = re.search(r'(?s)<table class="board"><tr>(.*?)</tr>', board)
    ths = [_page_text(t) for t in re.findall(r"(?s)<th>(.*?)</th>", hdr.group(1))] if hdr else []
    if "posture" not in ths or "heat" not in ths:
        return []
    ip, ih = ths.index("posture"), ths.index("heat")
    out = []
    for sym, body in re.findall(r"(?s)<tr class='w-[a-z_-]+'><td class='sym'>([^<]+)</td>(.*?)</tr>",
                                board):
        cells = [sym] + [_page_text(t) for t in re.findall(r"(?s)<td[^>]*>(.*?)</td>", body)]
        out.append((sym, cells[ip], float(cells[ih])))
    return out


def _br19_order_faults(rows, what: str, order=F19_ORDER) -> list[str]:
    rank = {w: i for i, w in enumerate(order)}
    hv = lambda h: h if h == h else float("-inf")          # noqa: E731  (NaN sorts last)
    bad = []
    for (s1, w1, h1), (s2, w2, h2) in zip(rows, rows[1:]):
        r1, r2 = rank.get(w1, len(order)), rank.get(w2, len(order))
        if r2 < r1:
            bad.append(f"{what}: {s1} ({w1}) sits ABOVE {s2} ({w2}), a row of higher posture")
        elif r1 == r2 and hv(h2) > hv(h1):
            bad.append(f"{what}: within {w1}, {s2} (heat {h2:.3f}) sits below {s1} (heat {h1:.3f})")
    return bad


def _br19_page_faults(doc: str, label: str) -> list[str]:
    rows = _br19_board(doc)
    if not rows:
        return [f"{label}: no Board rows could be read (no 'posture'/'heat' header) — fail closed"]
    bad = _br19_order_faults(rows, f"{label} Board")
    by = {s: (w, h) for s, w, h in rows}
    cards = re.findall(r'<div class="card-h"><b>([^<]+)</b>', _sec(doc, SEC_DOCKET))
    stray = [c for c in cards if c not in by]
    if stray:
        bad.append(f"{label} Docket: card(s) {stray} have no Board row")
    bad += _br19_order_faults([(c, *by[c]) for c in cards if c in by], f"{label} The Docket")
    watch = [w for w in re.findall(r'<div class="wh"><b>([^<]+)</b>', _sec(doc, SEC_WATCH)) if w in by]
    hv = lambda h: h if h == h else float("-inf")          # noqa: E731
    if any(hv(by[b][1]) > hv(by[a][1]) for a, b in zip(watch, watch[1:])):
        bad.append(f"{label} The Watch is no longer in heat order — R-2 re-orders the Board, The "
                   f"Docket and the report-back ONLY")
    return bad


def _br19_hard_view() -> dict:
    """The real view with heats reassigned so heat order INVERTS posture order, re-sorted
    by heat the way build_view sorts it. A copy: the shared view is not touched."""
    view = _pristine_view()
    rank = {w: i for i, w in enumerate(F19_ORDER)}
    assets = [dict(a, heat=10.0 * (1 + rank.get(a["station"].board_word, 4)) + 0.001 * i)
              for i, a in enumerate(view["assets"])]
    assets.sort(key=lambda a: -a["heat"])
    return {**view, "assets": assets}


def _br19_judge(render=None) -> list[str]:
    """Every finding against R-2; [] = clean. `render` swaps the renderer of the hard view."""
    import oracle_wrapper as _OW
    from types import SimpleNamespace as NS
    bad = []
    # (e) the constant, once
    if tuple(OD.BOARD_ORDER) != F19_ORDER:
        bad.append(f"BOARD_ORDER reads {tuple(OD.BOARD_ORDER)}, the ruling is {F19_ORDER}")
    if set(OD.BOARD_ORDER) != set(PE.STATION_WORDS) or len(set(OD.BOARD_ORDER)) != len(OD.BOARD_ORDER):
        bad.append(f"BOARD_ORDER {tuple(OD.BOARD_ORDER)} is not posture_engine's four words, once each")
    wt = ast.parse((ROOT / "scripts" / "oracle_wrapper.py").read_text(encoding="utf-8"))
    for n in ast.walk(wt):
        if isinstance(n, (ast.Tuple, ast.List)) and {e.value for e in n.elts if isinstance(e, ast.Constant)
                                                     and isinstance(e.value, str)} >= set(F19_ORDER):
            bad.append(f"oracle_wrapper.py:{n.lineno} types the four posture words — a second "
                       f"BOARD_ORDER; it must read oracle_daily's")
    # (a) the edition under test
    bad += _br19_page_faults(HTML or "", f"artifact set {DATE}")
    # (b) the hard render
    hv = _br19_hard_view()
    doc = (render or (lambda v: OD.render_html(v, DATE, PE.canon_sha())))(hv)
    bad += _br19_page_faults(doc, "the hard render (heat inverted against posture)")
    # (c) the helper on synthetic rows
    synth = [{"symbol": n, "station": NS(board_word=w), "heat": h} for n, w, h in F19_SYNTH]
    got = tuple(a["symbol"] for a in OD.board_rows(synth))
    if got != F19_SYNTH_WANT:
        bad.append(f"board_rows orders the synthetic board {got}, want {F19_SYNTH_WANT} — a row "
                   f"sits ABOVE a row of higher posture or heat is not descending within one")
    # (d) the wrapper's report-back, on log lines in the Oracle's own format
    lines = [f"  {n:14} {w:10} heat={h:6.3f} levels=  1 clusters=  1 atr_d=1" for n, w, h in F19_SYNTH]
    if tuple(_OW.board_order()) != tuple(OD.BOARD_ORDER):
        bad.append("the wrapper's board_order() is not oracle_daily.BOARD_ORDER")
    rep = tuple(r[0] for r in _OW.front_page_rows(lines, _OW.board_order()))
    if rep != F19_SYNTH_WANT:
        bad.append(f"the front-page report-back orders {rep}, want {F19_SYNTH_WANT}")
    return bad


def f_br_19() -> None:
    import oracle_wrapper as _OW

    def _swap(obj, name, value, judge_kw=None):
        def _run():
            keep = getattr(obj, name)
            try:
                setattr(obj, name, value)
                return _br19_judge(**(judge_kw or {}))
            finally:
                setattr(obj, name, keep)
        return _run

    def _docket_left_on_view_order():
        src = (ROOT / "scripts" / "oracle_daily.py").read_text(encoding="utf-8")
        anchor = '    cards = []\n    for a in ordered:\n'
        if src.count(anchor) != 1:
            return ["DOCKET PLANT could not be planted — anchor moved (fail closed)"]
        mod = _range_mutant(src.replace(anchor, '    cards = []\n    for a in a0:\n', 1))
        return _br19_judge(render=lambda v: mod.render_html(v, DATE, PE.canon_sha()))

    plants = (
        ("THE CONTRACT'S PLANT (the heat-only sort put back under the Board)",
         "sits ABOVE", _swap(OD, "board_rows", lambda xs: sorted(xs, key=lambda a: -a["heat"]))),
        ("WRAPPER PLANT (the report-back left on heat)",
         "report-back orders",
         _swap(_OW, "front_page_rows",
               lambda lines, order: sorted(
                   [(m.group("sym"), m.group("station"), float(m.group("heat")))
                    for m in map(_OW._BOARD_LINE.match, lines) if m], key=lambda r: -r[2]))),
        ("DOCKET PLANT (a source mutant: the Board posture-first, The Docket on the view's order)",
         "The Docket", _docket_left_on_view_order),
        ("CONSTANT PLANT (posture_engine's BOARD_PRECEDENCE — DEAD above STALKING — as the order)",
         "BOARD_ORDER reads", _swap(OD, "BOARD_ORDER", PE.REGISTER["BOARD_PRECEDENCE"]["value"])),
    )

    def _break() -> tuple[bool, str]:
        green, out = False, []
        for name, must, judge in plants:
            bad = judge()
            hits = [b for b in bad if must in b]
            if hits:
                rest = [b for b in bad if must not in b]
                out.append(f"{name} -> RED: {hits[0]}" + (f" [+{len(rest)} other]" if rest else ""))
            else:
                green = True
                out.append(f"{name} -> " + ("GREEN" if not bad else
                           f"RED FOR THE WRONG REASON (no finding says {must!r}; first: {bad[0]})"))
        return green, " ‖ ".join(out)

    def _real() -> tuple[bool, str]:
        bad = _br19_judge()
        if bad:
            return False, "; ".join(bad[:6]) + (f" (+{len(bad) - 6} more)" if len(bad) > 6 else "")
        rows = _br19_board(HTML)
        words = []
        for _s, w, _h in rows:
            if not words or words[-1][0] != w:
                words.append([w, 0])
            words[-1][1] += 1
        return True, (
            f"BOARD_ORDER == {F19_ORDER} (the ruling, typed here), posture_engine's four words once "
            f"each, and the wrapper types no second list. Artifact set {DATE}: {len(rows)} Board rows "
            f"run {' → '.join(f'{w} ×{n}' for w, n in words)}, heat descending within each; The "
            f"Docket's cards follow the Board's word for their symbol; The Watch still runs by heat. "
            f"A hard render (heat inverted against posture) comes out posture-first too; "
            f"board_rows and the wrapper's report-back order a synthetic board "
            f"{' '.join(F19_SYNTH_WANT)}. Heat values print unchanged")

    prove("F-BR-19", "POSTURE-FIRST BOARD — TRIGGERED, ARMED, STALKING, DEAD, heat descending "
                     "within; the Board, The Docket and the report-back, and nothing else",
          _break, _real)


# ═════════════════ F-BR-20 · THE EDITION WORD (OR-2 STEP 5, R-3)
#
# WHAT THIS GUARDS. Operator ruling R-3 (2026-09-22): full editions read "Morning" when
# the render time in America/Argentina/Buenos_Aires is before EDITION_NOON = 12, else
# "Evening"; the refresh verb keeps "Refresh". A-OR1-1 vii had already built the rule
# (ff74a90; F-BR-15 leg (ii) walks its own table); R-3 names the constant and asks for
# these two plants: 09:00 BA -> Morning, 22:22 BA -> Evening, and a break leg that
# hardcodes "Morning". 22:22 BA is 01:22Z the NEXT day, so a reading in UTC or on the
# UTC date is caught; the process zone is forced to UTC for the whole judgement.
# Each row is read twice: from edition_name, and off a REAL render's ear and Colophon
# print line. Break: the hardcoded Morning; EDITION_NOON moved to 23; a source copy of
# edition_name with the noon typed as a number.

F20_NOON = 12                                   # the ruling's number, typed from the queue
F20_DAY = "2030-01-04"
F20_TABLE = (("on-demand-full", "09:00", "Morning"), ("on-demand-full", "22:22", "Evening"),
             ("full", "09:00", "Morning"), ("full", "22:22", "Evening"),
             ("on-demand-refresh", "09:00", "Refresh"), ("on-demand-refresh", "22:22", "Refresh"))


def _br20_judge(src: str | None = None) -> list[str]:
    from datetime import datetime, timezone
    from zoneinfo import ZoneInfo
    bad = []
    if OD.EDITION_NOON != F20_NOON:
        bad.append(f"EDITION_NOON reads {OD.EDITION_NOON}, the ruling is {F20_NOON}")
    text = (ROOT / "scripts" / "oracle_daily.py").read_text(encoding="utf-8") if src is None else src
    fn = next((n for n in ast.walk(ast.parse(text))
               if isinstance(n, ast.FunctionDef) and n.name == "edition_name"), None)
    if fn is None:
        bad.append("oracle_daily.py defines no edition_name — fail closed")
    else:
        names = {n.id for n in ast.walk(fn) if isinstance(n, ast.Name)}
        typed = [n.value for n in ast.walk(fn) if isinstance(n, ast.Constant)
                 and isinstance(n.value, int) and not isinstance(n.value, bool)]
        if "EDITION_NOON" not in names or typed:
            bad.append(f"edition_name does not read EDITION_NOON (names it: "
                       f"{'EDITION_NOON' in names}; numbers typed in it: {typed}) — the noon typed "
                       f"a second time")
    view = _pristine_view()
    y, mo, d = map(int, F20_DAY.split("-"))
    with _ts_machine_zone(TS_MACHINE_ZONE):
        for slot, hhmm, word in F20_TABLE:
            h, m = map(int, hhmm.split(":"))
            at = datetime(y, mo, d, h, m, tzinfo=ZoneInfo(TS_ZONE)).astimezone(timezone.utc)
            got = OD.edition_name(slot, at)
            if got != f"{word} Edition":
                bad.append(f"slot {slot}, {hhmm} Buenos Aires -> {got!r}, want '{word} Edition'")
            page = OD.render_html(view, F20_DAY, PE.canon_sha(), edition_no=7, slot=slot,
                                  printed_at=at)
            ear, lines = _ts_vii_read(page)
            if ear != word:
                bad.append(f"slot {slot}, {hhmm} Buenos Aires: the rendered ear reads {ear!r}, want {word!r}")
            if len(lines) != 1 or lines[0][:4] != (F20_DAY, f"{h:02d}", f"{m:02d}", word):
                bad.append(f"slot {slot}, {hhmm} Buenos Aires: the Colophon print line reads "
                           f"{lines[:1]}, want {F20_DAY} {hhmm} Buenos Aires ({word} Edition …)")
    return bad


def f_br_20() -> None:
    def _swap(name, value):
        def _run():
            keep = getattr(OD, name)
            try:
                setattr(OD, name, value)
                return _br20_judge()
            finally:
                setattr(OD, name, keep)
        return _run

    src = (ROOT / "scripts" / "oracle_daily.py").read_text(encoding="utf-8")
    anchor = ".hour < EDITION_NOON"
    plants = (
        ("THE CONTRACT'S PLANT (the edition word hardcoded: 'Morning' for every full edition)",
         "22:22 Buenos Aires -> 'Morning Edition'",
         _swap("edition_name", lambda slot, printed_at=None: "Refresh Edition"
               if "refresh" in str(slot).lower() else "Morning Edition")),
        ("CONSTANT PLANT (EDITION_NOON moved to 23)", "EDITION_NOON reads 23",
         _swap("EDITION_NOON", 23)),
        ("SOURCE PLANT (edition_name with the noon typed as a number)", "the noon typed a second time",
         (lambda: _br20_judge(src=src.replace(anchor, ".hour < 12", 1)))
         if src.count(anchor) == 1 else (lambda: [])),
    )

    def _break() -> tuple[bool, str]:
        green, out = False, []
        for name, must, judge in plants:
            bad = judge()
            hits = [b for b in bad if must in b]
            if hits:
                out.append(f"{name} -> RED: {hits[0]}" + (f" [+{len(bad) - 1} more]" if len(bad) > 1 else ""))
            else:
                green = True
                out.append(f"{name} -> " + ("GREEN (or could not be planted)" if not bad else
                           f"RED FOR THE WRONG REASON (no finding says {must!r}; first: {bad[0]})"))
        return green, " ‖ ".join(out)

    def _real() -> tuple[bool, str]:
        bad = _br20_judge()
        if bad:
            return False, "; ".join(bad[:6]) + (f" (+{len(bad) - 6} more)" if len(bad) > 6 else "")
        return True, (
            f"EDITION_NOON == {F20_NOON} and edition_name reads it (no number typed in it). With the "
            f"process zone forced to {TS_MACHINE_ZONE}, on {F20_DAY}: "
            + "; ".join(f"{sl} {hm} BA -> {w}" for sl, hm, w in F20_TABLE)
            + " — each from edition_name AND off a real render's ear and its one Colophon print "
              "line (22:22 BA is 01:22Z the next day)")

    prove("F-BR-20", "THE EDITION WORD — full: Morning before EDITION_NOON = 12 Buenos Aires, "
                     "Evening from it; refresh: Refresh",
          _break, _real)


# ══════════════════════════════════════════════════════════════════ MAIN

def main() -> int:
    load_artifacts()
    print("=" * 78)
    print(f"ORACLE FIXTURES — artifact set {DATE}")
    print(f"  html  {len(HTML):,} B")
    print(f"  tape  {len(TAPE):,} rows" if TAPE is not None else "  tape  ABSENT")
    print(f"  tape_ranges  {len(TAPE_RANGES):,} rows" if TAPE_RANGES is not None
          else "  tape_ranges  ABSENT")
    print(f"  cal   {len(CAL.get('per_asset', [])) if CAL else 0} per-asset records")
    print("=" * 78)
    fixtures = (f_br_1, f_br_2, f_br_3, f_br_4, f_br_5, f_br_6,
                f_br_7, f_br_8, f_br_9, f_br_10, f_br_11, f_br_12, f_br_13, f_br_14,
                f_br_15, f_br_16, f_br_17, f_br_18, f_br_19, f_br_20)
    for fn in fixtures:
        try:
            fn()
        except Exception as e:                       # a fixture that errors is a fail
            name = fn.__name__.upper().replace("_", "-").replace("F-BR-", "F-BR-")
            FAILED.append(f"{name} (raised {e.__class__.__name__}: {e})")
            print(f"  [FAIL] {name}: raised {e.__class__.__name__}: {e}")
    print("\n" + "=" * 78)
    print(f"GREEN {len(PASSED)}/{len(fixtures)} · RED {len(FAILED)}")
    for f in FAILED:
        print(f"  RED: {f}")
    print("=" * 78)
    return 1 if FAILED else 0


if __name__ == "__main__":
    raise SystemExit(main())
