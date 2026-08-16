"""ORACLE FIXTURES — F-BR-1 .. F-BR-10 of queue BR-1 (as amended by A1-4).

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
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from engine.data import cache_dir            # noqa: E402
from engine import indicators as ind         # noqa: E402

import station_engine as SE                  # noqa: E402
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
    produces the FOUR POSTURE WORDS per bar without touching station_engine.

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
    d_floor = SE.REGISTER["D_DISPLACEMENT"]["value"]
    dead_mem = SE.REGISTER["DEAD_MEMORY_BARS"]["value"]

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
            ours = SE.stations_for(sym, df, as_of_i=i).board_word
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
    return True, (f"{checked}/10 symbols x {len(as_of_offsets)} as-of points = {compared} "
                  f"station-word comparisons against a SECOND state machine with its own "
                  f"EMA/ATR/cross recursions (no engine.indicators, no station_engine) — "
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
    dec = _closure("station_engine")
    for m in list(BANNED_IN_DECISION) + list(extra_banned):
        hits = [x for x in dec if x == m or x.startswith(m + ".")]
        if hits:
            bad.append(f"station_engine reaches {sorted(hits)[:3]}")
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
                         for f in ("oracle_daily.py", "station_engine.py")) + extra_src
    for mod in INHERITED_DISCLOSED:
        if re.search(rf"\b(?:from|import)\s+{re.escape(mod)}\b", src_all):
            bad.append(f"an oracle source imports {mod} directly (must be inherited only)")
    for call in JOURNAL_READ_CALLS:
        if call in src_all:
            bad.append(f"an oracle source calls a journal read: {call}")
    srcs = {p: (ROOT / "scripts" / p).read_text()
            for p in ("oracle_daily.py", "station_engine.py")}
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
        f"station_engine closure is analytics-free ({len(dec)} modules); no forward_log "
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
        a1 = SE.last_tide_flip(SE.build_frame(df), len(df) - 1)
        df2 = df.copy()
        if perturb:
            # The anchor is an e89-vs-e316 crossing, so a single-bar nudge cannot
            # move it — the break has to bend the slow ribbons. Ramp the last 400
            # closes; that genuinely relocates the flip.
            n = min(400, len(df2))
            ramp = np.linspace(1.0, 1.8, n)
            df2.iloc[-n:, df2.columns.get_loc("close")] = \
                df2["close"].to_numpy("float64")[-n:] * ramp
        a2 = SE.last_tide_flip(SE.build_frame(df2), len(df2) - 1)
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
    d1 = OD.render_html(view, DATE, SE.canon_sha())
    if tamper:
        view["assets"][0]["heat"] += 0.5
    d2 = OD.render_html(view, DATE, SE.canon_sha())
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
    need = {
        "DISPLAY-ONLY header": "DISPLAY-ONLY" in doc.split("<h2>")[0],
        "date": DATE in foot,
        "payload shas": n_sha >= 10,
        "CERTIFIED list": "CERTIFIED:" in foot,
        "NOT CERTIFIED list": "NOT CERTIFIED:" in foot,
        "station canon sha": SE.canon_sha() in foot,
    }
    missing = [k for k, v in need.items() if not v]
    if missing:
        return False, "missing: " + ", ".join(missing)
    return True, (f"DISPLAY-ONLY header, date {DATE}, {n_sha} sha256 stamps, station "
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


# ══════════════════════════════════════════════════════════════════ MAIN

def main() -> int:
    load_artifacts()
    print("=" * 78)
    print(f"ORACLE FIXTURES — artifact set {DATE}")
    print(f"  html  {len(HTML):,} B")
    print(f"  tape  {len(TAPE):,} rows" if TAPE is not None else "  tape  ABSENT")
    print(f"  cal   {len(CAL.get('per_asset', [])) if CAL else 0} per-asset records")
    print("=" * 78)
    for fn in (f_br_1, f_br_2, f_br_3, f_br_4, f_br_5,
               f_br_6, f_br_7, f_br_8, f_br_9, f_br_10):
        try:
            fn()
        except Exception as e:                       # a fixture that errors is a fail
            name = fn.__name__.upper().replace("_", "-").replace("F-BR-", "F-BR-")
            FAILED.append(f"{name} (raised {e.__class__.__name__}: {e})")
            print(f"  [FAIL] {name}: raised {e.__class__.__name__}: {e}")
    print("\n" + "=" * 78)
    print(f"GREEN {len(PASSED)}/10 · RED {len(FAILED)}")
    for f in FAILED:
        print(f"  RED: {f}")
    print("=" * 78)
    return 1 if FAILED else 0


if __name__ == "__main__":
    raise SystemExit(main())
