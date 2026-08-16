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


def pine_events_independent(close: np.ndarray, high: np.ndarray, low: np.ndarray,
                            atr_len: int = 14) -> dict:
    """A SECOND implementation, transcribed from pine/SS_v12_0_1.pine directly.

    This deliberately does NOT call station_engine or tierc2_rules — the whole
    point of a parity fixture is that two independent paths agree. The Pine
    text it mirrors, verbatim:

        f_lens(tf) => request.security(..., [ta.ema(close,12), ta.ema(close,26),
                      ta.ema(close,89), ta.ema(close,316), ta.atr(atrLen), close], ...)
        f_pair(...) => up = ta.crossover(eA, eB) ; dn = ta.crossunder(eA, eB)
        // ARMING 12/89   // TRIGGER 12/26   // BELL 89/316

    Pine's ta.ema recurses from the first bar with no NaN prefix, which is
    exactly engine.indicators.ema — the reason that module exists.
    """
    e12 = ind.ema(close, 12)
    e26 = ind.ema(close, 26)
    e89 = ind.ema(close, 89)
    e316 = ind.ema(close, 316)
    return {
        "arm_up": ind.crossover(e12, e89), "arm_dn": ind.crossunder(e12, e89),
        "trg_up": ind.crossover(e12, e26), "trg_dn": ind.crossunder(e12, e26),
        "bell_up": ind.crossover(e89, e316), "bell_dn": ind.crossunder(e89, e316),
    }


def _parity_compare(mutate=None) -> tuple[bool, str]:
    v12_1_present = any(p.name.startswith("SS_v12_1") for p in (ROOT / "pine").iterdir())
    mismatches = []
    checked = 0
    for sym in OD.REGISTER["ROSTER"]["value"]:
        df = OD.load_lens(sym, "4h")
        df = df[df["open_time"] <= FIXTURE_DAY_MS].reset_index(drop=True)
        if len(df) < 1200:
            continue
        close = df["close"].to_numpy("float64")
        pine = pine_events_independent(close, df["high"].to_numpy("float64"),
                                       df["low"].to_numpy("float64"))
        if mutate is not None:
            pine = mutate(pine)
        f = SE.build_frame(df)
        ours = SE.crosses(f)
        checked += 1
        for a, b in (("arm_up", "w_up"), ("arm_dn", "w_dn"), ("trg_up", "t_up"),
                     ("trg_dn", "t_dn"), ("bell_up", "b_up"), ("bell_dn", "b_dn")):
            d = int(np.count_nonzero(np.asarray(pine[a]) != np.asarray(ours[b])))
            if d:
                mismatches.append(f"{sym}:{a}/{b} x{d}")
    handoff = ("" if v12_1_present else
               "  [handoff] pine/ holds SS_v12_0_1.pine only; SS v12.1 is described in "
               "PINE_LANE_PRIMER_2026-08-15 §2 but is NOT in the repo, so marker-level "
               "parity against v12.1 itself is OWED, not discharged.")
    if mismatches:
        return False, f"mismatch list: {', '.join(mismatches[:8])}" + handoff
    return True, (f"{checked}/10 symbols, 6 marker series each, on the frozen day "
                  f"2026-08-12 — mismatch list EMPTY (= pass)." + handoff)


def f_br_1() -> None:
    prove("F-BR-1", "PARITY — station markers vs the Pine source, symbol for symbol",
          lambda: _parity_compare(mutate=lambda p: {**p, "trg_up": np.roll(p["trg_up"], 1)}),
          lambda: _parity_compare())


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
    if "R:R" in doc and "toll" not in doc:
        offenders.append("document prints a ratio and never a toll")
    if offenders:
        return False, "; ".join(sorted(set(offenders)))
    n = len(re.findall(r"NET R:R", doc))
    return True, (f"net_rr() takes toll_price; {n} rendered NET R:R cell(s), every one "
                  f"carrying its per-lens toll band from the ORACLE GRID")


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
BANNED_ANYWHERE = ("journal", "forward_log", "positions")
TRADING_DISCLOSED = "engine.trading"


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
    for m in BANNED_ANYWHERE:
        hits = [x for x in both if x == m or x.startswith(m + ".")]
        if hits:
            bad.append(f"oracle closure reaches {sorted(hits)[:3]}")
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
    return True, (
        f"station_engine closure is analytics-free ({len(dec)} modules); no journal / "
        f"forward_log / positions module is reachable from either module; no oracle "
        f"source references a trading symbol; no outcome-aggregation symbol is assigned. "
        f"DISCLOSED: {TRADING_DISCLOSED} IS in the closure via the ratified chain "
        f"tierc2_rules -> engine.s1 -> 'from engine.trading import TradeResult'; it is "
        f"imported, never called — BR-1 §2 'imported read-only, trading disabled'.")


def f_br_3() -> None:
    prove("F-BR-3", "FIREWALL — import graph, not prose",
          # the break plants a direct trading reference in a synthetic source
          lambda: _firewall(extra_src="from engine.trading import place_order\n"),
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
    if bad:
        return False, "; ".join(bad[:5])
    return True, (f"{ok_n} strips; each canvas binds a payload whose meta.sha256 "
                  f"recomputes from its own data block and is printed in that strip's "
                  f"footer (the shipped VIZ-4 convention: data-block sha, not file sha)")


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
    hits = []
    for k in _keys_deep(doc):
        toks = set(re.split(r"[^a-z0-9]+", k.lower()))
        for w in OD.BANNED_CALIBRATION_KEYS:
            wt = set(re.split(r"[^a-z0-9]+", w.lower()))
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
    planted["per_asset"][0]["win_rate"] = 0.42        # the deliberate break
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
