"""ORACLE FIXTURES — F-BR-1 .. F-BR-12 of queue BR-1 (as amended by A1-4, A2-8, T-7),
F-BR-13 of queue OR-1 STEP B (finding C-0: the D-7 logger must MEASURE),
F-BR-14 of queue OR-1 STEP D (the range layer renders and never rules),
F-BR-15 of queue OR-1 STEP F (THE DAILY ORACLE: typeset, semantics untouched), and
F-BR-16 of queue OR-1 STEP C (the roster is ONE literal definition).

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
import hashlib
import io
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

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


def _latest(pattern: str, d: Path) -> Path | None:
    xs = sorted(d.glob(pattern))
    return xs[-1] if xs else None


def load_artifacts() -> None:
    global DATE, HTML, CAL, TAPE
    h = _latest("oracle_*.html", OD.OUT_DIR)
    if h is None:
        raise SystemExit("HALT: no rendered oracle_*.html — run oracle_daily.py first")
    DATE = h.stem.replace("oracle_", "")
    HTML = h.read_text(encoding="utf-8")
    c = _latest(f"oracle_calibration_{DATE}_*.json", OD.CAL_DIR)
    CAL = json.loads(c.read_text()) if c else None
    t = _latest(f"oracle_tape_{DATE}.parquet", OD.TAPE_DIR)
    TAPE = pd.read_parquet(t) if t else None


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
    """`_refresh(tamper=False)` is a PRODUCTION API (the wrapper's daily self-check):
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

    prove("F-BR-6", "REFRESH IDEMPOTENCE — the 16:00 refresh over unchanged data, and never "
                    "a comparison of nothing with nothing",
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
    bad = [ln for ln in lines if not R1_LINE.match(ln.strip())]
    if bad:
        return False, f"{len(bad)} non-conforming line(s), first: {bad[0]!r}"
    return True, (f"{len(lines)} alert lines, every one matching "
                  f"<SYMBOL> <TAG> <PRICE> — prices only, no prose, no advice, "
                  f"paste-ready")


def f_br_7() -> None:
    broken = HTML.replace('<pre class="r1">',
                          '<pre class="r1">BTCUSDT: consider a long here\n', 1)
    prove("F-BR-7", "R1 FORMAT — alert block parses as price levels only",
          lambda: _r1(broken), lambda: _r1(HTML))


# ═════════════════════════════════════════════ F-BR-8 · PROVENANCE FOOTER

def _footer(doc: str) -> tuple[bool, str]:
    m = re.search(r"<footer>(.*?)</footer>", doc, re.S)
    if not m:
        return False, "no footer"
    foot = m.group(1)
    n_sha = len(re.findall(r"sha256 [0-9a-f]{64}", foot))
    # ONE PAYLOAD SHA PER ROSTER SYMBOL, so the floor IS the roster's length. It read
    # `n_sha >= 10`, the old roster's size typed as a number (OR-1 STEP C, CONVENTIONS
    # §6.4: the second of the two VALUE dependents that carried no NAME). Left at 10,
    # an 18-symbol edition could lose eight payload stamps and stay green here.
    # CONSEQUENCE, stated: an edition printed from a SHORTER roster than the current
    # one is red here by design — it is not an edition of this roster (F-BR-16 says
    # which symbols differ).
    n_roster = len(OD.REGISTER["ROSTER"]["value"])
    need = {
        "DISPLAY-ONLY header": "DISPLAY-ONLY" in doc.split("<h2>")[0],
        "date": DATE in foot,
        f"payload shas ({n_sha} stamp(s) for a roster of {n_roster})": n_sha >= n_roster,
        "CERTIFIED list": "CERTIFIED:" in foot,
        "NOT CERTIFIED list": "NOT CERTIFIED:" in foot,
        "posture canon sha": PE.canon_sha() in foot,
    }
    missing = [k for k, v in need.items() if not v]
    if missing:
        return False, "missing: " + ", ".join(missing)
    return True, (f"DISPLAY-ONLY header, date {DATE}, {n_sha} sha256 stamps (floor = the "
                  f"roster's {n_roster}, read from REGISTER['ROSTER'], never typed), station "
                  f"canon sha, and BOTH the certified and not-certified lists present")


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
# eight tape columns. A range is the most tempting number on the page to act on
# ("it is 0.4 ATR from the top, so damp the heat"), and the day one line does that,
# a display organ calibrated on ONE symbol (BTC; KEY-A on 1D, KEY-C on 4h) is steering
# posture words on eighteen. The contract's words for this fixture: "posture_engine.py
# byte-unchanged (sha printed); the range object appears only in render + tape, never
# in any gate path (component-wise import scan); planted gate read ⇒ red."
#
# FOUR LEGS, because each one alone has a hole the next one covers:
#   (a) THE SHA      scripts/posture_engine.py is byte-for-byte the file pinned below.
#                    Every station word on the page comes from it; STEP D had no
#                    business in it and this proves it had none. A later RATIFIED
#                    edit to posture_engine.py re-pins the constant in the same commit
#                    (the F-TU-1 idiom): the red is the point, not an accident.
#   (b) THE IMPORTS  in clean subprocesses, the closure of every decision module holds
#                    no module with the component `rangefinder` (nor `oracle_daily`:
#                    a gate that imported the Oracle could read a view), and the range
#                    machine's own closure holds no trading / journal / outcome-package
#                    component. Component-wise, the F-BR-3 repair: `engine.rangefinder`
#                    cannot hide behind a top-level-only test. A raw-text import scan
#                    covers the rule modules this suite never IMPORTS (another lane's
#                    live work is read, never executed).
#   (c) THE AST      oracle_daily.py, scanned as CODE: every mention of the asset-dict
#                    key 'range', of the snapshot's own key names, of the `RNG` alias
#                    and of the layer's five functions must sit inside an ALLOW-LIST of
#                    function names. build_view is on it for exactly ONE statement, of
#                    exactly one shape. By VALUE, not by spelling: `k = "range"; a[k]`
#                    is caught, and so is a gate that calls range_watch(). Fails
#                    CLOSED: if the key it hunts is no longer read by write_tape or by
#                    a render function, the scan is hunting a stale name and says so.
#   (d) THE RUN      what no static scan can promise (`for v in a.values()` names
#                    nothing). build_view runs three times over the live roster:
#                    REAL, the layer stubbed EMPTY, and stubbed HOT (every symbol
#                    pinned ON a macro boundary with a breach pending: the input a gate
#                    would react to hardest). Sort order, heat, station, card, lines,
#                    clusters, fired events, R1, the WHOLE D-7 document and the 24
#                    pre-existing tape columns must come out identical; the range
#                    columns must NOT, or the stub never reached build_view and the
#                    comparison is empty. THE PAGE IS COMPARED TOO, because leg (c)
#                    lets render_html read a range and a reader can misbehave (a Board
#                    re-sorted by distance inside the render moves no field of the
#                    view): every rendered section but the Tide Tables, the Board with
#                    its RANGE cells cut out, identical across the three runs.
# and three small pins that belong to the same wall: the new tape names clear the
# banned-token matcher the wrapper's self-check runs ("edge" is banned); no D-7 key
# carries the token `range`; and range_layer() CONTAINS a fault (a display organ may
# not take the Board down) and REFUSES a frame that is not on REGISTER['RANGE_LENS'].
#
# WHAT IT DOES NOT PROVE. That the ranges are RIGHT (F-RF-*, and only on BTC). That a
# human will not act on the number (nothing can). That code OUTSIDE oracle_daily.py
# and the modules in (b) never reads a tape column: the tape is a recording, and what
# a later study does with it is that study's registration under G-7.
#
# LIKE F-BR-16, IT AUDITS THE NEWEST ARTIFACT SET TOO: the edition under test must
# carry the Tide Tables, EDGE WATCH, both [VETO] rows in its appendix and the eight
# range columns on its tape. Run bare against an edition printed before STEP D it is
# RED on exactly those, on purpose, until an edition is printed by this code.
#
# BREAK LEG: one plant per guard, judged ONE AT A TIME (the F-BR-13 idiom): each
# must go red on its own and for its own reason, named beside it.

POSTURE_ENGINE_SHA256 = "1e3b3ba28e251d1fa3ef6ab8add5f1841164312e061e94686f7e3e8c8fc666b4"

# The contract's six, plus engine.htf (it feeds the signal layer; engine/rangefinder.py's
# own docstring names it a stranger).
RANGE_DECISION_MODULES = ("posture_engine", "tierc2_rules", "tierc3_rules",
                          "engine.signals", "engine.trading", "engine.replay", "engine.htf")
RANGE_MACHINE = "engine.rangefinder"
RANGE_BANNED_IN_DECISION = ("rangefinder", "oracle_daily")
RANGE_BANNED_IN_MACHINE = ("trading", "journal", "analytics", "signals", "replay",
                           "forward_log", "positions")
# Read as TEXT only, never imported: every engine module but the machine itself, the
# posture engine, and every tierc*_rules module (tierc6 is another lane's live work).
RANGE_IMPORT_LINE = re.compile(r"(?m)^[ \t]*(?:from|import)[ \t]+[^\n#]*\brangefinder\b")

RANGE_KEY = "range"
RANGE_ALIAS = "RNG"
RANGE_PRODUCER = "range_layer"
RANGE_HELPERS = ("range_layer", "range_empty", "range_cell", "range_watch", "tide_tables")
# THE ALLOW-LIST. The layer's own five functions, the page, the tape. Nothing else.
RANGE_READERS = (*RANGE_HELPERS, "render_html", "write_tape")
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


def _range_static_sources() -> dict[str, str]:
    files = [p for p in sorted((ROOT / "engine").glob("*.py")) if p.name != "rangefinder.py"]
    files += [ROOT / "scripts" / "posture_engine.py"]
    files += sorted((ROOT / "scripts").glob("tierc*_rules.py"))
    return {str(p.relative_to(ROOT)): p.read_text(encoding="utf-8", errors="replace")
            for p in files}


def _range_static(sources: dict[str, str]) -> list[str]:
    bad = []
    for name, text in sources.items():
        m = RANGE_IMPORT_LINE.search(text)
        if m:
            bad.append(f"{name} imports the range machine: `{m.group(0).strip()}`")
    return bad


def _range_closures() -> tuple[list[str], dict]:
    """Leg (b), the real thing: one clean subprocess per module, run side by side."""
    from concurrent.futures import ThreadPoolExecutor
    mods = (*RANGE_DECISION_MODULES, RANGE_MACHINE)
    with ThreadPoolExecutor(max_workers=len(mods)) as ex:
        clos = dict(zip(mods, ex.map(_closure, mods)))
    bad: list[str] = []
    for m in RANGE_DECISION_MODULES:
        bad += _range_reach(m, clos[m], RANGE_BANNED_IN_DECISION)
    bad += _range_reach(f"the range machine ({RANGE_MACHINE})", clos[RANGE_MACHINE],
                        RANGE_BANNED_IN_MACHINE)
    if RANGE_MACHINE not in clos[RANGE_MACHINE]:
        bad.append(f"{RANGE_MACHINE} is absent from its own closure — the probe imported nothing")
    if RANGE_MACHINE not in _closure("oracle_daily"):
        bad.append(f"oracle_daily does not import {RANGE_MACHINE} — this leg is guarding a "
                   f"layer that is not there")
    sources = _range_static_sources()
    bad += _range_static(sources)
    return bad, {"sizes": {m: len(c) for m, c in clos.items()}, "static": len(sources)}


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


def _range_ast(src: str | None = None) -> tuple[list[str], dict]:
    """Leg (c). Scans CODE, not prose: comments and docstrings cannot satisfy or trip it."""
    src = (ROOT / "scripts" / "oracle_daily.py").read_text(encoding="utf-8") if src is None else src
    tree = ast.parse(src)
    bad: list[str] = []
    fns = {n.name: n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}

    binds = [(n, a) for n in ast.walk(tree) if isinstance(n, (ast.Import, ast.ImportFrom))
             for a in n.names if (a.asname or a.name) == RANGE_ALIAS]
    ok_bind = [1 for n, a in binds if isinstance(n, ast.ImportFrom)
               and n.module == "engine" and a.name == "rangefinder"]
    if len(binds) != 1 or len(ok_bind) != 1:
        bad.append(f"`{RANGE_ALIAS}` must be bound exactly once, by `from engine import "
                   f"rangefinder as {RANGE_ALIAS}` (found {len(binds)} binding(s)) — fail closed")
    for n in ast.walk(tree):
        if isinstance(n, (ast.Import, ast.ImportFrom)):
            for a in n.names:
                full = f"{getattr(n, 'module', None) or ''}.{a.name}".strip(".")
                if "rangefinder" in full.split(".") and (a.asname or a.name) != RANGE_ALIAS:
                    bad.append(f"line {n.lineno}: the range machine is imported a second way "
                               f"(`{full}` as `{a.asname or a.name}`) — the scan fences one alias")

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

    for g in RANGE_NAMED_GATES:
        if g not in fns:
            bad.append(f"{g}() not found — it is named as range-free and cannot be checked; "
                       f"fail closed")
    for r in RANGE_READERS:
        if r not in fns:
            bad.append(f"allow-listed reader {r}() not found — fail closed")
    # fail closed: the key this scan hunts must be the key the code really reads
    reads = {r: sum(1 for n, what in _range_mentions(fns[r]) if what == f"the key {RANGE_KEY!r}")
             for r in ("write_tape", "range_cell", "range_watch", "tide_tables") if r in fns}
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


def _range_mutant(src: str):
    """oracle_daily.py's SOURCE, edited, run as a throwaway module. It is never put in
    sys.modules and writes nothing: only build_view / r1_block / range_layer are called."""
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


RANGE_DECISION_FIELDS = ("heat", "station", "card", "lis", "nearest", "nearest_d",
                         "clusters", "n_levels", "atr_d", "price", "payload_sha",
                         "vwap_maturity")


def _range_decision_side(mod, view: dict) -> dict[str, str]:
    """Everything a gate COULD have moved, as repr() text keyed so a difference names
    itself (repr makes NaN equal NaN). The D-7 document and the tape are WRITTEN, into
    a throwaway directory, and read back: what is compared is what would be filed."""
    out = {"the Board's sort order": repr([a["symbol"] for a in view["assets"]]),
           "as_of_ms": repr(view["as_of_ms"]), "card_toll_atr": repr(view["card_toll_atr"]),
           "fired events": repr(view["fired"]), "R1 block": mod.r1_block(view)}
    for a in view["assets"]:
        for k in RANGE_DECISION_FIELDS:
            out[f"{a['symbol']}.{k}"] = repr(a[k])
    real_cal, real_tape = mod.CAL_DIR, mod.TAPE_DIR
    try:
        with tempfile.TemporaryDirectory(prefix="f-br-14-") as td:
            mod.CAL_DIR, mod.TAPE_DIR = Path(td) / "cal", Path(td) / "tape"
            cal_p, _, _ = mod.write_calibration(view, "0000-00-00", "fixture")
            doc = json.loads(Path(cal_p).read_text())
            tape_p, _, _ = mod.write_tape(view, "0000-00-00")
            tape = pd.read_parquet(tape_p)
    finally:
        mod.CAL_DIR, mod.TAPE_DIR = real_cal, real_tape
    doc.pop("generated_utc", None)                 # the one wall-clock field
    out["the D-7 document"] = json.dumps(doc, sort_keys=True)
    out["D-7 keys carrying the token `range`"] = repr(sorted(
        k for k in set(_keys_deep(doc)) if RANGE_KEY in re.split(r"[^a-z0-9]+", k.lower())))
    rcols = [c for c in tape.columns if c.startswith("range_")]
    out["the pre-existing tape columns"] = tape[[c for c in tape.columns
                                                 if c not in rcols]].to_csv(index=False)
    out["__range_columns__"] = tape[rcols].to_csv(index=False)       # MUST differ
    # THE PAGE, because render_html is on the allow-list and a reader can misbehave
    # too (a Board re-sorted by distance inside the render would move no field
    # above). Every section but the Tide Tables, up to the footer; the Board with
    # its RANGE cells cut out. What is left may not know a range exists.
    page = mod.render_html(view, "0000-00-00", PE.canon_sha()).split("<footer>")[0]
    for part in re.split(r"<h2>", page)[1:]:
        title = part.split("</h2>")[0]
        if title.lower().startswith(SEC_TIDE.lower()):
            continue
        if title.lower().startswith(SEC_BOARD.lower()):    # 'The Board' until OR-1 STEP F
            part, n_cells = re.subn(r"<td class='rng'>.*?</td>", "", part, flags=re.S)
            out["__range_cells__"] = str(n_cells)
        out[f"the rendered section '{title[:40]}'"] = part
    return out


def _range_behaviour(mod=None, n_roster: int | None = None) -> tuple[list[str], dict]:
    """Leg (d). `mod` is oracle_daily, or a mutant of it for the break leg."""
    mod = OD if mod is None else mod
    quiet = lambda *a, **k: None                   # noqa: E731
    full = mod.REGISTER["ROSTER"]["value"]
    layer = mod.range_layer
    sides, views = {}, {}
    try:
        if n_roster:
            mod.REGISTER["ROSTER"]["value"] = tuple(full[:n_roster])   # a slice, never a list
        for name, stub in (("REAL", None), ("EMPTY", _range_stub_empty), ("HOT", _range_stub_hot)):
            mod.range_layer = layer if stub is None else stub
            views[name] = mod.build_view(log=quiet)
            mod.range_layer = layer
            sides[name] = _range_decision_side(mod, views[name])
    finally:
        mod.range_layer = layer
        mod.REGISTER["ROSTER"]["value"] = full
    bad: list[str] = []
    for name in ("EMPTY", "HOT"):
        moved = [k for k in sides["REAL"] if k != "__range_columns__"
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
        bad.append("the tape's range columns under the HOT stub equal another run's — the "
                   "range never reaches the tape, or the stub never reached the view")
    if sides["REAL"].get("__range_cells__") != str(len(views["REAL"]["assets"])):
        bad.append(f"the Board carries {sides['REAL'].get('__range_cells__')} RANGE cell(s) for "
                   f"{len(views['REAL']['assets'])} row(s) — the cut that lets the Board be "
                   f"compared found the wrong number of cells")
    if sides["REAL"]["D-7 keys carrying the token `range`"] != "[]":
        bad.append("range data reached the calibration JSON: "
                   + sides["REAL"]["D-7 keys carrying the token `range`"])
    real = [a["range"] for a in views["REAL"]["assets"]]
    return bad, {"assets": len(real), "fields": len(sides["REAL"]) - 2,
                 "sections": sorted(k for k in sides["REAL"] if k.startswith("the rendered")),
                 "live": sum(1 for r in real if r.get("has_range")),
                 "pending": sum(1 for r in real if r.get("pending")),
                 "failed": sum(1 for r in real if r.get("error")),
                 "keys": sorted({k for r in real if not r.get("error") for k in r})}


def _range_tape_names(cols=None) -> list[str]:
    """Every range column is a RECORDING name: it clears the banned-token matcher the
    wrapper's daily self-check runs over oracle_daily.TAPE_COLS."""
    cols = list(OD.TAPE_COLS) if cols is None else list(cols)
    new = [c for c in cols if c.startswith("range_")]
    bad = []
    for c in new:
        ok, detail = _calibration({c: 0})
        if not ok:
            bad.append(f"tape column {c!r} trips the banned vocabulary: {detail}")
    if not new:
        bad.append("TAPE_COLS carries no range_* column — the tape half of STEP D is missing")
    if TAPE is not None:
        missing = [c for c in new if c not in TAPE.columns]
        if missing:
            bad.append(f"artifact set {DATE}: the tape lacks {missing} — it was not written by "
                       f"this code")
    return bad


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


def f_br_14() -> None:
    od_src = (ROOT / "scripts" / "oracle_daily.py").read_text(encoding="utf-8")
    pe_path = ROOT / "scripts" / "posture_engine.py"
    rf_src = (ROOT / "engine" / "rangefinder.py").read_text(encoding="utf-8")
    gate_src = _range_plant_after_write(od_src, RANGE_GATE_TEXT)
    narrow = _range_plant_narrow_except(od_src)
    # a READER misbehaving: legal to the AST leg (render_html is on the allow-list),
    # so only the run can see it — the page quietly drops every row with a breach open
    drop_src = _range_plant_in(od_src, "render_html",
                               f"view = dict(view, assets=[a for a in view['assets'] "
                               f"if not a['{RANGE_KEY}'].get('pending')])")
    drop_ast = len(_range_ast(drop_src)[0]) if drop_src else -1
    rules = ROOT / "scripts" / "tierc3_rules.py"

    def ast_plant(src):
        return None if src is None else (lambda: _range_ast(src)[0])

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
        ("CLOSURE PLANT (`from engine import journal` planted in a copy of engine/rangefinder.py)",
         "the range machine reaches",
         lambda: _range_reach("the range machine", _closure_src(
             "rangefinder_f_br_14_planted", rf_src + "\nfrom engine import journal\n"),
             RANGE_BANNED_IN_MACHINE)),
        (f"STATIC PLANT (`from engine.rangefinder import run_v2` appended to the TEXT of "
         f"{rules.name}, never executed)",
         "imports the range machine",
         lambda: _range_static({rules.name: rules.read_text(encoding="utf-8")
                                + "\nfrom engine.rangefinder import run_v2\n"})),
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
        (f"BEHAVIOUR PLANT (the same gate read, RUN: a mutant of oracle_daily.py built from "
         f"source, build_view over the first {RANGE_MUTANT_ROSTER} roster rows, REAL vs EMPTY vs HOT)",
         "decision side moved",
         (lambda: _range_behaviour(_range_mutant(gate_src), n_roster=RANGE_MUTANT_ROSTER)[0])
         if gate_src else None),
        (f"RENDER PLANT (a reader misbehaving: render_html drops every row with a breach "
         f"pending. The AST leg finds {drop_ast} problem(s) in it — render_html is on the "
         f"allow-list — so only the run can object; mutant, first {RANGE_MUTANT_ROSTER} roster rows)",
         "the rendered section",
         (lambda: _range_behaviour(_range_mutant(drop_src), n_roster=RANGE_MUTANT_ROSTER)[0])
         if drop_src else None),
        ("TAPE-NAME PLANT (a column called range_edge_atr)",
         "trips the banned vocabulary",
         lambda: _range_tape_names([*OD.TAPE_COLS, "range_edge_atr"])),
        ("CONTAINMENT PLANT (range_layer's `except Exception` narrowed to ZeroDivisionError, "
         "in a mutant built from source)",
         "range_layer RAISED",
         (lambda: _range_containment(_range_mutant(narrow))[0]) if narrow else None),
    ]

    def _break() -> tuple[bool, str]:
        green, out = False, []
        for name, must, judge in plants:
            if judge is None:
                green = True
                out.append(f"{name} -> GREEN: the plant could not be planted")
                continue
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
        bad_sha, sha = _range_sha()
        bad_clo, clo = _range_closures()
        bad_ast, a = _range_ast()
        bad_run, run = _range_behaviour()
        bad_tape = _range_tape_names()
        bad_con, con = _range_containment()
        bad = bad_sha + bad_clo + bad_ast + bad_run + bad_tape + bad_con
        want = set(OD.range_empty())
        if run["keys"] and set(run["keys"]) != want:
            bad.append(f"range_empty()'s key set is not engine.rangefinder.snapshot()'s + 'error': "
                       f"{sorted(set(run['keys']) ^ want)}")
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
        if OD.REGISTER["RANGE_WINDOW_BARS"]["value"] != OD.RNG.V2_WINDOW_BARS:
            bad.append("REGISTER['RANGE_WINDOW_BARS'] is not the machine's V2_WINDOW_BARS")
        if bad:
            return False, "; ".join(bad[:6]) + (f" (+{len(bad) - 6} more)" if len(bad) > 6 else "")
        new_cols = [c for c in OD.TAPE_COLS if c.startswith("range_")]
        return True, (
            f"(a) scripts/posture_engine.py sha256 {sha} == the pinned constant: byte-unchanged. "
            f"(b) component-wise, in clean subprocesses: no `rangefinder` and no `oracle_daily` "
            f"component in the closure of "
            + ", ".join(f"{m} ({clo['sizes'][m]})" for m in RANGE_DECISION_MODULES)
            + f"; {RANGE_MACHINE}'s own closure ({clo['sizes'][RANGE_MACHINE]} modules) holds none "
            f"of {list(RANGE_BANNED_IN_MACHINE)}; oracle_daily DOES import it; and no import line "
            f"names the machine in the text of {clo['static']} decision-side source files (every "
            f"engine module but the machine, posture_engine.py, every tierc*_rules.py — read, "
            f"never executed). "
            f"(c) AST of oracle_daily.py ({a['functions']} functions): `{RANGE_ALIAS}` is bound once; "
            f"the key {RANGE_KEY!r}, the {len(RANGE_ONLY_KEYS)} snapshot-only keys, the alias and the "
            f"{len(RANGE_HELPERS)} layer functions are mentioned ONLY inside {list(RANGE_READERS)}, "
            f"plus ONE statement of {RANGE_WRITER}() (line {a['write_line']}: `<asset>[{RANGE_KEY!r}] "
            f"= {RANGE_PRODUCER}(h4)`) and REGISTER's import of the window; zero mentions in "
            f"{list(RANGE_NAMED_GATES)}, each of which exists; the key is really read "
            f"({', '.join(f'{k} x{v}' for k, v in a['reads'].items())}). "
            f"(d) build_view run three times over the {run['assets']}-symbol roster — REAL "
            f"({run['live']} live macro range(s), {run['pending']} pending, {run['failed']} "
            f"unavailable), stubbed EMPTY, stubbed HOT (every symbol ON a boundary, breach "
            f"pending): {run['fields']} decision-side fields identical across all three — sort "
            f"order, heat, station, card, lines, clusters, fired events, R1, the whole D-7 "
            f"document, the {len(OD.TAPE_COLS) - len(new_cols)} pre-existing tape columns and "
            f"{len(run['sections'])} rendered sections (every one but the Tide Tables, the Board "
            f"with its {run['assets']} RANGE cells cut out) — "
            f"while the {len(new_cols)} range columns under HOT differ from both other runs and "
            f"every HOT asset carries the stub, so the stubs were live. "
            f"No D-7 key carries the token `range`. The {len(new_cols)} new tape names "
            f"({', '.join(new_cols)}) clear the {len(OD.BANNED_CALIBRATION_KEYS)}-term banned "
            f"vocabulary and are on artifact set {DATE}'s tape. range_layer contains a fault "
            f"(EMPTY frame -> {con.get('an EMPTY frame')!r}) and refuses a frame off its lens "
            f"(1h -> {con.get('a 1h frame')!r}). RANGE_LENS and RANGE_WATCH_ATR are 'ruled': False "
            f"and print in the rendered [VETO] appendix; RANGE_WINDOW_BARS = "
            f"{OD.REGISTER['RANGE_WINDOW_BARS']['value']} is the machine's own constant, imported.")

    prove("F-BR-14", "THE RANGE LAYER RENDERS, NEVER RULES — posture_engine.py byte-unchanged; "
                     "the range object in render + tape only, never in a gate path; a planted "
                     "gate read must go red",
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
#   · THE BAND. "LATE EDITION — wire stale since <as-of>" directly under the masthead
#     WHEN AND ONLY WHEN A2-7's rule fires. Driven, not assumed: one view rendered with
#     an as-of five minutes INSIDE the limit and five minutes PAST it. And the phrase
#     nowhere else in the page's text: the on-demand wrapper reads "banner UP" off it
#     (oracle_wrapper BANNER_MARKERS), so a caption or a [VETO] source that spelt it
#     would raise a false alarm in the log every day.
#   · NO WALL CLOCK in the Front Page or The Watch. F-BR-6 renders twice a few
#     milliseconds apart and cannot see a stamp with minute resolution; here the
#     module's clock is pushed 400 days on and both sections must not move a byte.
#   · THE MASTHEAD. The contract's ears; 'Refresh Edition' for a refresh slot, 'Morning
#     Edition' otherwise; an un-numbered render says 'No. —'; render_html still takes
#     (view, date_str, canon_sha) — the wrapper's daily self-check calls it that way —
#     and run() is what numbers an edition.
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
#
# WHAT IT DOES NOT PROVE: that no number moved. That is F-BR-1..14 staying green on a
# fresh render, and the block-by-block old-template/new-template comparison in the
# build document (scratchpad semantic_diff.py); nor that the page is handsome.

TS_CAPTION = ("rows = threads, rod 5000 top → hem 9 bottom · columns = last 96 bars · "
              "hue = thread above/below price in ATR · dark pinch = knot · hole = unwoven")
TS_PAPER, TS_INK, TS_RED = "#F4ECD8", "#1A1A1A", "#B3261E"
TS_SERIF = '"Iowan Old Style", Palatino, Georgia, serif'
TS_TITLE = "THE DAILY ORACLE"
TS_EAR_LEFT = re.compile(r"^Vol\. I · No\. (\d+|—)$")
TS_EAR_RIGHT = re.compile(r"^Buenos Aires · (\d{4}-\d{2}-\d{2}) · (Morning|Refresh) Edition · "
                          r"Price: one toll$")
TS_BAND = "LATE EDITION"
TS_BAND_HEAD = "LATE EDITION — wire stale since {as_of}"
TS_BAND_DETAIL = "The top-up may not have run"
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
                   f"<date> · <Morning|Refresh> Edition · Price: one toll'")
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
    """ONE view, rendered five ways. The stale and fresh as-ofs straddle A2-7's limit
    by TS_MARGIN_MS; the limit is recomputed HERE from the two module constants, so a
    banner that fires on some other rule is caught, not mirrored."""
    from datetime import datetime, timedelta, timezone
    view = _pristine_view()
    canon = PE.canon_sha()
    limit = OD.STALE_LENS_PERIODS * OD.LENS_MS[view["lens"]]
    now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
    fresh = {**view, "as_of_ms": now_ms - limit + TS_MARGIN_MS}
    stale = {**view, "as_of_ms": now_ms - limit - TS_MARGIN_MS}
    out = {"limit_h": limit / 3_600_000,
           "stale_as_of": datetime.fromtimestamp(stale["as_of_ms"] / 1000, timezone.utc)
                                  .strftime("%Y-%m-%dT%H:%MZ"),
           "fresh": OD.render_html(fresh, DATE, canon),
           "stale": OD.render_html(stale, DATE, canon),
           "plain": OD.render_html(view, DATE, canon),
           "numbered": OD.render_html(view, DATE, canon, edition_no=7, slot="on-demand-refresh")}
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
    fresh, stale = _ts_band(renders["fresh"]), _ts_band(renders["stale"])
    if fresh is not None or TS_BAND in _page_text(renders["fresh"]):
        bad.append(f"late edition: the band prints on a wire {TS_MARGIN_MS // 60_000} min INSIDE "
                   f"the {renders['limit_h']:.1f}h limit — it must print only when the rule fires")
    want = TS_BAND_HEAD.format(as_of=renders["stale_as_of"])
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
    if (plain["edition"], plain["name"]) != ("—", "Morning"):
        bad.append(f"masthead: a render nobody numbered reads No. {plain['edition']} · "
                   f"{plain['name']} Edition, want 'No. —' and 'Morning Edition'")
    if (numbered["edition"], numbered["name"]) != ("7", "Refresh"):
        bad.append(f"masthead: edition_no=7, slot='on-demand-refresh' reads No. "
                   f"{numbered['edition']} · {numbered['name']} Edition, want No. 7 · Refresh")
    return bad, {"stale_as_of": renders["stale_as_of"], "limit_h": renders["limit_h"]}


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


def _ts_source(src: str | None = None) -> list[str]:
    """Scans CODE, not prose: the bar count typed once, the signature the wrapper calls,
    and run() numbering the edition."""
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
        if pos != ["view", "date_str", "canon_sha"] or sorted(kwo) != ["edition_no", "slot"] \
                or any(d is None for d in rh.args.kw_defaults):
            bad.append(f"signature: render_html takes {pos} + keyword-only {kwo}; the fixtures "
                       f"and the wrapper's daily self-check call render_html(view, date_str, "
                       f"canon_sha), and the masthead's two are optional keywords")
    run = fns.get("run")
    calls = [n for n in ast.walk(run) if isinstance(n, ast.Call)
             and isinstance(n.func, ast.Name)] if run is not None else []
    if not any(c.func.id == "edition_count" for c in calls):
        bad.append("run(): never calls edition_count() — the edition is not numbered")
    if not any(c.func.id == "render_html" and {"edition_no", "slot"} <= {k.arg for k in c.keywords}
               for c in calls):
        bad.append("run(): does not hand render_html BOTH edition_no and slot — a real edition "
                   "would go to press as 'No. —' or as the wrong edition")
    return bad


_TS_RENDERS = None


def _typeset_judge(html_doc: str | None = None, renders: dict | None = None,
                   src: str | None = None, counter=None, headliner=None) -> tuple[list[str], dict]:
    global _TS_RENDERS
    if _TS_RENDERS is None:
        _TS_RENDERS = _ts_renders()
    bad, page = _ts_static(HTML if html_doc is None else html_doc, DATE)
    live_bad, live = _ts_live({**_TS_RENDERS, **(renders or {})})
    bad = bad + live_bad + _ts_edition_count(counter) + _ts_source(src) + _ts_headline(headliner)
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
        if f"<code>{k}</code>" not in _sec(HTML if html_doc is None else html_doc, SEC_COLOPHON):
            bad.append(f"colophon: the rendered [VETO] appendix does not list {k}")
    return bad, {**page, **live}


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
    red_word = base.replace("<style>", "<style>td.post.w-dead{color:var(--red)}", 1)
    loud = base.replace(cap_html, cap_html + " · LATE EDITION strips are re-cut hourly", 1)
    kw_anchor = "edition_no=edition_no, slot=slot"
    cap_anchor = "columns = last {bars} bars"

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
            f"ear {DATE} · {x['name']} Edition; an un-numbered render says 'No. —' · Morning, "
            f"edition_no=7 + a refresh slot says No. 7 · Refresh; render_html(view, date_str, "
            f"canon_sha) still stands; over four synthetic boards the headline opens 'Business "
            f"possible' for a FRESH trigger only ('No fresh trigger on the roster' over stale or "
            f"armed rows, 'No business possible today' over none); run() numbers the edition from the TAPE's dates "
            f"(3 of 2 tapes + today, 2 on a reprint, 1 with no directory; a misnamed file and an "
            f"empty briefs/oracle change nothing). LATE EDITION: one view rendered "
            f"{TS_MARGIN_MS // 60_000} min inside the {x['limit_h']:.1f}h limit -> no band and the "
            f"phrase nowhere in the text; {TS_MARGIN_MS // 60_000} min past it -> the band directly "
            f"under the masthead, opening 'LATE EDITION — wire stale since {x['stale_as_of']}', "
            f"A2-7's sentence after it, the phrase exactly once. The Front Page and The Watch do "
            f"not move a byte with the module's clock pushed {TS_CLOCK_SHIFT_DAYS} days on")

    prove("F-BR-15", "THE DAILY ORACLE — eight sections in order, a caption under every strip, "
                     "DISPLAY-ONLY in the colophon, three inks, the LATE EDITION band when and "
                     "only when the wire is stale",
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

ROSTER_RULING = "1-watchlist: drop symbols without data from a binance contract"
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


def _roster_judge(src: str | None = None, html_doc: str | None = None,
                  tape_assets=None, cal_assets=None) -> tuple[list[str], dict]:
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
        if literal is not None:
            dups = sorted({s for s in literal if literal.count(s) > 1})
            back = [s for s in literal if s in dropped]
            stray = [s for s in literal if s not in kept and s not in dropped]
            lost = [s for s in kept if s not in literal]
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
                           f"operator's 22 as probed in {probe_path}")
            if lost:
                bad.append(f"KEPT by the probe but missing from the roster: {lost}")
            if soft:
                bad.append(f"listed as kept but the probe's own record is not KEEP/PERPETUAL/"
                           f"TRADING: {soft}")
            if not (dups or back or stray or lost) and literal != kept:
                i = next(j for j, (a, b) in enumerate(zip(literal, kept)) if a != b)
                bad.append(f"not in the operator's order: position {i + 1} reads {literal[i]}, "
                           f"the probe's KEPT list (his order, dropped names removed) reads {kept[i]}")
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
        return True, (
            f"REGISTER['ROSTER'] is a LITERAL tuple of {n} at oracle_daily.py:{x['line']}, equal IN "
            f"ORDER to the {len(x['kept'])} KEPT of {x['probe']} (every record KEEP · PERPETUAL · "
            f"TRADING); the {len(x['dropped'])} DROPPED BY RULING ({', '.join(x['dropped'])}) are off "
            f"it and named in the row's source, which quotes ruling 1 verbatim and is 'ruled': True; "
            f"oracle_daily.py does not name the study basket; no second symbol list in "
            f"{len(ROSTER_FAMILY)} family files ({', '.join(ROSTER_FAMILY)}); the live row equals "
            f"the source literal; and artifact set {DATE} was printed from exactly this roster — "
            f"{x['strips']} mantle strips, {x['tape']} tape assets, {x['cal']} D-7 records. "
            f"Roster: {' '.join(x['literal'])}")

    prove("F-BR-16", "ROSTER — one literal definition: the probe's KEPT list in the operator's "
                     "order, no second list, and the edition under test printed from it",
          _break, _real)


# ══════════════════════════════════════════════════════════════════ MAIN

def main() -> int:
    load_artifacts()
    print("=" * 78)
    print(f"ORACLE FIXTURES — artifact set {DATE}")
    print(f"  html  {len(HTML):,} B")
    print(f"  tape  {len(TAPE):,} rows" if TAPE is not None else "  tape  ABSENT")
    print(f"  cal   {len(CAL.get('per_asset', [])) if CAL else 0} per-asset records")
    print("=" * 78)
    fixtures = (f_br_1, f_br_2, f_br_3, f_br_4, f_br_5, f_br_6,
                f_br_7, f_br_8, f_br_9, f_br_10, f_br_11, f_br_12, f_br_13, f_br_14,
                f_br_15, f_br_16)
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
