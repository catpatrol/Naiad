"""ORACLE FIXTURES — F-BR-1 .. F-BR-12 of queue BR-1 (as amended by A1-4, A2-8, T-7),
F-BR-13 of queue OR-1 STEP B (finding C-0: the D-7 logger must MEASURE), and
F-BR-16 of queue OR-1 STEP C (the roster is ONE literal definition; 14 and 15 are
the numbers the OR-1 contract gives to STEP D and STEP F).

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
    """The HTML between one <h2> and the next — how F-BR-6 compares sections."""
    parts = re.split(r"<h2>", HTML)
    for p in parts[1:]:
        if p.lower().startswith(name.lower()):
            return p
    return ""


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

def _refresh(tamper=False) -> tuple[bool, str]:
    view = OD.build_view(log=lambda *a, **k: None)
    d1 = OD.render_html(view, DATE, PE.canon_sha())
    if tamper:
        view["assets"][0]["heat"] += 0.5
    d2 = OD.render_html(view, DATE, PE.canon_sha())
    diffs = []
    for name in ("The Board", "The Watch"):
        s1, s2 = _sec(d1, name), _sec(d2, name)
        if s1 != s2:
            diffs.append(f"{name}: {len(s1)} B vs {len(s2)} B")
    if diffs:
        return False, "; ".join(diffs)
    return True, (f"Board {len(_sec(d1,'The Board')):,} B and Watch "
                  f"{len(_sec(d1,'The Watch')):,} B byte-identical across two renders "
                  f"over unchanged data")


def _sec(doc: str, name: str) -> str:
    for p in re.split(r"<h2>", doc)[1:]:
        if p.lower().startswith(name.lower()):
            return p
    return ""


def f_br_6() -> None:
    prove("F-BR-6", "REFRESH IDEMPOTENCE — the 16:00 refresh over unchanged data",
          lambda: _refresh(tamper=True), lambda: _refresh(tamper=False))


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
                f_br_7, f_br_8, f_br_9, f_br_10, f_br_11, f_br_12, f_br_13, f_br_16)
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
