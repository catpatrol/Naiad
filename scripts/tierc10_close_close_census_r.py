#!/usr/bin/env python
"""TIER-C10 · CLOSE · S2 CENSUS-R — the build document's CENSUS-R section, as a
SELECTION from the filed digest, with its fixtures in the same file.

WHAT THIS IS.  The contract's CLOSE orders "CENSUS-R tables, with
outcome-after-event, the acceptance head-to-head and height-vs-toll prominent"
(exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md, CLOSE).  This script writes
that section to research_outputs/tierc10/close/S2_CENSUS_R.md.  It takes a
SELECTION, by heading span, out of research_outputs/tierc10/census/
CENSUS_R_DIGEST.md and NEVER RETYPES IT: every block marked *verbatim* is the
digest's own bytes at the line span its label names.  Order (auditor's spec):
  2.1  §A  [Q-R4] acceptance head-to-head — the data's default NAMED, nothing
           promoted
  2.2  §B / B.3  [Q-R3] height-vs-toll — the gate and the POOLED verdict rows,
           every lens x scale kind x era
  2.3  §5  outcome after event — POOLED:CLASSIC5 and POOLED:UNSEEN12, frozen3.0,
           eras ALL and holdout, each with BOTH nulls beside (gaps+order = the
           null of record, R10)
  2.4  §1  coverage (the SCALE calibrator's whole grid stays in the digest)
  2.5  §2  F-RF-4

THE ONE THING HERE THAT IS NOT IN THE DIGEST.  The null stage pooled POOLED:ALL
only (null/<variant>/build_manifest.json commission.pooled), so the digest
prints no null beside its CLASSIC5 / UNSEEN12 blocks.  Those nulls are computed
here from the FILED per-cell null ledgers by the null build's OWN pooling path
(tierc10_census.grid_rows per draw -> canon -> tierc10_null.summarise ->
canon, exactly as tierc10_null.merge does for POOLED:ALL).  F-S2-NULL-ANCHOR
proves the path: it reproduces every filed POOLED:ALL null-summary row exactly,
and its REAL draw equals the census's own sub-pool outcome rows exactly.

FIXTURE LEGS — each states FAILS IF, and each carries a break leg that must go
RED first or the fixture is void [the prove() law of the TC10 suites]:
  F-S2-SLICE        a spliced block is not byte-identical to its digest span
  F-S2-PARQUET      a printed verdict_pass / ratio_median / edge_net_h20
                    differs from height_toll_verdict.parquet on (lens,
                    scale_kind, asset, era)
  F-S2-ORDER        outcome-after-event, the acceptance head-to-head and
                    height-vs-toll do not all precede coverage and F-RF-4
  F-S2-NULL         an outcome block lacks the gaps+order null beside it
  F-S2-NULL-ANCHOR  the close-time pooling path does not reproduce the filed
                    POOLED:ALL null, or its REAL draw is not the census's
  F-S2-PROMOTE      a named default is not the parquet's, or anything is
                    promoted
  F-S2-COLLAR       a 5m retest-hold row outside the tuning era is printed
  F-S2-SIZE         the file exceeds FLAG_BYTES unflagged (BOX_BYTES /
                    FLAG_BYTES read by ast.literal_eval from
                    scripts/publish_exchange.py, never imported)
  F-DET             two builds are not byte-identical

TIER-E, REPORT-ONLY: nothing is scored, no registration is read, no verdict is
consulted; no bar is read (the as-of is Stage D's AS_OF_PIN.json through
tierc10_data.load_pin).  Writes ONLY research_outputs/tierc10/close/.

FROZEN SUBSTRATE [TIER-C10 law 3]: HALTs unless NAIAD_CACHE_DIR is exported and
is not the live cache.  The transcript carries no wall clock.

Run: export NAIAD_CACHE_DIR=~/.cache/naiad/snapshots/tc10_20260921 \\
            PYTHONDONTWRITEBYTECODE=1
     ~/venvs/naiad/bin/python scripts/tierc10_close_close_census_r.py [leg ...]
     (any argument is matched as a substring of the leg id, case-blind; a
      partial run never overwrites the filed transcript)
Exit: 0 all GREEN · 1 a fixture RED · 2 HALT (substrate).
"""
from __future__ import annotations

import ast
import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
LIVE_CACHE = Path.home() / ".cache" / "naiad" / "data_cache"

# ── RUN / HALT preamble: nothing of TC10 is imported before the substrate is proven
_ENV = os.environ.get("NAIAD_CACHE_DIR")
if not _ENV or Path(_ENV).resolve() == LIVE_CACHE.resolve():
    print("*** HALT: NAIAD_CACHE_DIR must be exported to the FROZEN snapshot before python "
          "starts [TIER-C10 law 3]; the live cache is read-never for TC10. ***")
    raise SystemExit(2)

sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import numpy as np                                                   # noqa: E402
import pandas as pd                                                  # noqa: E402

import tierc10_census as C          # noqa: E402  HALTS at import off the snapshot
import tierc10_null as N            # noqa: E402
import tierc10_data as D            # noqa: E402  load_pin only; no bar is read here

TC10 = ROOT / "research_outputs" / "tierc10"
CENSUS = TC10 / "census"
NULL_ROOT = TC10 / "null"
DIGEST = CENSUS / "CENSUS_R_DIGEST.md"
RULINGS = TC10 / "OPERATOR_RULINGS.md"
VERDICT = CENSUS / "height_toll_verdict.parquet"
ACCEPT = CENSUS / "acceptance_head_to_head.parquet"
OUTCOME = CENSUS / "outcome_grid.parquet"
PUBLISH = ROOT / "scripts" / "publish_exchange.py"
OUT = TC10 / "close"
DOC = OUT / "S2_CENSUS_R.md"
TRANSCRIPT = OUT / "FIXTURES_CLOSE_census_r.txt"
SELF = Path(__file__).resolve()

KIND = next(k for k in C.SCALE_KINDS if k.startswith("frozen"))      # the pin of record
SUB_POOLS = (C.POOL_CLASSIC5, C.POOL_UNSEEN12)
SEL_ERAS = (C.ERA_ALL, C.ERA_HOLDOUT)
VARIANTS = ("gaps+order", "gaps-only")                # R10: the null of record FIRST
OF_RECORD = "gaps+order"
M_TABLES = (("acceptance_head_to_head", ACCEPT), ("height_toll_verdict", VERDICT),
            ("outcome_grid", OUTCOME), ("coverage", CENSUS / "coverage.parquet"),
            ("spring_overlap", CENSUS / "spring_overlap.parquet"))

FAILED: list[str] = []
PASSED: list[str] = []
T: list[str] = []                  # the transcript: deterministic lines only


def say(line: str = "") -> None:
    print(line)
    T.append(line)


def clock(line: str) -> None:
    """Wall-clock facts: stdout ONLY, never the filed transcript [F-DET law]."""
    print(f"  [clock · stdout only] {line}")


def check(fixture: str, ok: bool, detail: str) -> bool:
    say(f"  [{'PASS' if ok else 'FAIL'}] {fixture}: {detail}")
    return ok


def prove(fixture: str, title: str, fails_if: str, break_leg, real_leg) -> None:
    """Both legs, in order. The break leg must go red or the fixture is void."""
    say(f"\n{fixture} — {title}")
    say(f"  FAILS IF: {fails_if}")
    try:
        b_ok, b_detail = break_leg()
    except Exception as e:                       # a break leg that errors proved nothing
        b_ok, b_detail = True, f"break leg RAISED {e.__class__.__name__}: {e}"
    say(f"  [BREAK] deliberate violation -> "
        f"{'RED (correct)' if not b_ok else 'GREEN (FIXTURE IS VOID)'}: {b_detail}")
    try:
        r_ok, r_detail = real_leg()
    except Exception as e:                       # a fixture that errors is a fail
        r_ok, r_detail = False, f"raised {e.__class__.__name__}: {e}"
    green = check(fixture, r_ok, r_detail)
    if b_ok:
        FAILED.append(f"{fixture} (break leg passed — fixture proves nothing)")
    elif not green:
        FAILED.append(fixture)
    else:
        PASSED.append(fixture)


def plants(rows) -> tuple[bool, str]:
    """One plant per guard, judged ONE AT A TIME. `rows` = (name, thunk -> list
    of findings). A plant that yields NO finding passed — the break leg is then
    GREEN and the fixture void."""
    passed, caught = [], []
    for name, thunk in rows:
        found = thunk()
        (caught if found else passed).append(
            f"{name} -> {str(found[0])[:120]}" if found else name)
    if passed:
        return True, f"{len(passed)} plant(s) PASSED: {passed}"
    return False, f"all {len(caught)} plants caught, one at a time: " + " · ".join(caught)


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def rel(p: Path) -> str:
    return str(Path(p).resolve().relative_to(ROOT))


def halt(msg: str):
    raise SystemExit(f"HALT: {msg}")


# ═══════════════════════════════════════════════ 1 · SOURCES, READ AS BYTES
class Source:
    """A filed text, as bytes, line-addressed 1-based INCLUSIVE.  A heading
    span runs from its heading line to the line before the next heading of the
    same or a higher level."""

    def __init__(self, path: Path):
        self.path, self.name = path, path.name
        self.raw = path.read_bytes()
        self.lines = self.raw.splitlines(keepends=True)
        self.text = [x.decode("utf-8") for x in self.lines]
        self.sha = sha256(self.raw)
        self.heads = [(i + 1, len(t) - len(t.lstrip("#")), t.rstrip("\n"))
                      for i, t in enumerate(self.text) if re.match(r"#{1,6} ", t)]

    def get(self, a: int, b: int) -> bytes:
        if not (1 <= a <= b <= len(self.lines)):
            raise ValueError(f"{self.name}: span L{a}-L{b} outside 1..{len(self.lines)}")
        return b"".join(self.lines[a - 1:b])

    def span(self, prefix: str) -> tuple[int, int]:
        hit = [h for h in self.heads if h[2].startswith(prefix)]
        if len(hit) != 1:
            halt(f"heading {prefix!r} matched {len(hit)} time(s) in {self.name} — the "
                 "selection is by heading span and never guesses")
        return self.span_at(hit[0][0])

    def span_at(self, ln: int) -> tuple[int, int]:
        """The span of the heading ON line `ln` (1-based)."""
        lv = next(h[1] for h in self.heads if h[0] == ln)
        nxt = [h[0] for h in self.heads if h[0] > ln and h[1] <= lv]
        return ln, (nxt[0] - 1 if nxt else len(self.lines))

    def find(self, lo: int, hi: int, prefix: str) -> list[int]:
        return [i for i in range(lo, hi + 1) if self.text[i - 1].startswith(prefix)]

    def one(self, lo: int, hi: int, prefix: str) -> int:
        hit = self.find(lo, hi, prefix)
        if len(hit) != 1:
            halt(f"{self.name} L{lo}-L{hi}: line prefix {prefix!r} matched {len(hit)} "
                 "time(s)")
        return hit[0]

    def item(self, i: int) -> tuple[int, int]:
        """A list item and its indented continuation lines."""
        j = i
        while j < len(self.lines) and self.text[j].startswith("  "):
            j += 1
        return i, j

    def section_of(self, line: int) -> str:
        """The level-2 heading text a line falls under ('' = the title block)."""
        h2 = [h for h in self.heads if h[1] == 2 and h[0] <= line]
        return h2[-1][2] if h2 else ""


def merge(spans: list[tuple[int, int]]) -> list[tuple[int, int]]:
    out: list[list[int]] = []
    for a, b in spans:
        if out and a == out[-1][1] + 1:
            out[-1][1] = b
        else:
            out.append([a, b])
    return [(a, b) for a, b in out]


def fmt_spans(spans) -> str:
    return " + ".join(f"L{a}–L{b}" for a, b in spans)


def omitted(src: Source, lo: int, hi: int, spans) -> str:
    """Non-blank lines of [lo, hi] not spliced, as ranges (blank-only gaps merged)."""
    took = {i for a, b in spans for i in range(a, b + 1)}
    runs: list[list[int]] = []
    for i in range(lo, hi + 1):
        if i in took or not src.text[i - 1].strip():
            continue
        if runs and all(not src.text[k - 1].strip() for k in range(runs[-1][1] + 1, i)) \
                and not any(k in took for k in range(runs[-1][1] + 1, i)):
            runs[-1][1] = i
        else:
            runs.append([i, i])
    return " · ".join(f"L{a}" if a == b else f"L{a}–L{b}" for a, b in runs) or "nothing"


def classes_of(block: bytes) -> list[str]:
    """The class column of a §5 outcome block, in the block's own order."""
    rows = [x for x in block.decode("utf-8").splitlines() if x.startswith("| ")]
    return [r.split("|")[1].strip() for r in rows[1:]]      # rows[0] = the header


# ═══════════════════════════════════════════════ 2 · THE SELECTION
def select(dg: Source, ru: Source) -> dict:
    """The SELECTION, by heading span.  Returns spans (1-based inclusive) and
    the section bounds; it types selectors, never content."""
    S: dict = {}
    first_h2 = min(h[0] for h in dg.heads if h[1] == 2)
    ban = dg.one(1, first_h2 - 1, "**TIER-E MEASUREMENT")
    war = dg.one(1, first_h2 - 1, "- WARRANTY:")
    col = dg.one(1, first_h2 - 1, "> P-BRK-S1 IS SCORED")
    era = dg.one(1, first_h2 - 1, "> era = the ANCHOR")
    S["banner"] = merge([(ban, ban + 1), (war, war + 1), (col, col + 1), (era, era + 1)])
    S["title_block"] = (1, first_h2 - 1)

    # 2.1 · §A [Q-R4]
    a0, a1 = dg.span("## A · [Q-R4]")
    q = dg.one(a0, a1, "> LEDGER.md:835")
    nothing = dg.one(a0, a1, "**THE DATA'S DEFAULT IS NAMED BELOW")
    S["A"] = (a0, a1)
    S["A_head"] = merge([(q, q + 1), (nothing, nothing + 1)])
    S["A_lens"] = []
    for lens in C.LENSES:
        t = dg.one(a0, a1, f"**{lens} · {C.POOL_ALL} · {KIND} · era {C.ERA_ALL} · H20**")
        d = [i for i in dg.find(t, a1, "> THE DATA'S DEFAULT AT ")][0]
        sp = [(t, d + 1)]
        for e in (C.ERA_TUNING, C.ERA_HOLDOUT):
            x = dg.one(a0, a1, f"> THE DATA'S DEFAULT AT {lens} / {e} / H20:")
            sp.append((x, x + 1))
        S["A_lens"].append((lens, merge(sorted(sp))))
    h100 = dg.one(a0, a1, "**THE DATA'S DEFAULT AT H100**")
    S["A_tail"] = [(h100, a1)]

    # 2.2 · §B [Q-R3] + B.3
    b0, b1 = dg.span("## B · [Q-R3]")
    b_intro_end = min(h[0] for h in dg.heads if b0 < h[0] <= b1) - 1
    q = dg.one(b0, b_intro_end, "> LEDGER.md:834")
    sp = [(q, q + 1)]
    for p in ("- **THE HEIGHT GATE**", "- **THE EDGE-FADE LEG**", "- **THE CONJUNCTION**"):
        sp.append(dg.item(dg.one(b0, b_intro_end, p)))
    t0, t1 = dg.span("### B.3 ·")
    sp.append(dg.item(dg.one(t0, t1, "- **THE SAMPLE FLOOR**")))
    S["B"], S["B3"] = (b0, b1), (t0, t1)
    S["B_head"] = merge(sorted(sp))
    whole = dg.one(t0, t1, "**THE WHOLE GRID, ROW BY ROW, EVERY ERA.**")
    if not (dg.text[whole + 1].startswith("| lens | scale | asset |")
            and dg.text[whole + 2].startswith("|---")):
        halt("B.3: the whole-grid paragraph is not followed by its table header")
    rows, i = [], whole + 4
    while i <= t1 and dg.text[i - 1].startswith("|"):
        cells = [c.strip() for c in dg.text[i - 1].split("|")[1:-1]]
        if cells[2].startswith("POOLED:"):
            rows.append((i, i))
        i += 1
    S["B_grid_rows"] = i - (whole + 4)
    S["B_table"] = merge([(whole, whole + 3)] + rows)
    S["B_pooled_rows"] = len(rows)

    # 2.3 · §5 outcome after event
    f0, f1 = dg.span("## 5 · OUTCOME AFTER EVENT")
    first_sub = min(h[0] for h in dg.heads if f0 < h[0] <= f1)
    last_txt = max(k for k in range(f0 + 1, first_sub) if dg.text[k - 1].strip())
    S["F"] = (f0, f1)
    S["F_head"] = [(f0 + 2, last_txt + 1)]
    S["F_blocks"] = []
    for lens in C.LENSES:
        for e in SEL_ERAS:
            for pool in SUB_POOLS:
                h, end = dg.span(f"### {pool} · {lens} · {KIND} · era `{e}`")
                S["F_blocks"].append(((pool, lens, KIND, e), [(h, end)]))
    S["F_subs_total"] = sum(1 for h in dg.heads if f0 < h[0] <= f1 and h[1] == 3)
    r0, r1 = ru.span("## R10 ·")
    ruled = ru.one(r0, r1, "**Ruled:")
    S["R10"] = merge([(ruled, ruled + 1),
                      ru.item(ru.one(r0, r1, "- `gaps+order` is the null of record")),
                      ru.item(ru.one(r0, r1, "- `gaps-only`")),
                      ru.item(ru.one(r0, r1, "- **K=20"))])
    S["R10_span"] = (r0, r1)

    # 2.4 · §1 coverage (the calibrator stays in the digest)
    c0, c1 = dg.span("## 1 · COVERAGE")
    subs = [h for h in dg.heads if c0 < h[0] <= c1 and h[1] == 3]
    intro = c0 + 2
    sp = [(intro, intro + 1)]
    S["C_left"] = []
    for h in subs:
        s0, s1 = dg.span_at(h[0])
        if h[2].startswith("### The SCALE calibrator"):
            S["C_left"].append((s0, s1))
        else:
            sp.append((s0, s1))
    S["C"], S["C_body"] = (c0, c1), merge(sorted(sp))

    # 2.5 · §2 F-RF-4, whole
    g0, g1 = dg.span("## 2 · F-RF-4")
    S["G"], S["G_body"] = (g0, g1), [(g0 + 2, g1)]
    return S


# ═══════════════════════════════════════════════ 3 · THE NULL BESIDE, AT CLOSE
def null_manifest(v: str) -> dict:
    return json.loads((NULL_ROOT / N.VARIANT_DIR[v] / "build_manifest.json").read_text())


def compute_nulls(lenses=C.LENSES, variants=VARIANTS, pools=None) -> dict:
    """tierc10_null.merge's pooling, applied to every pool of the commission
    (not only POOLED:ALL): draw d of every member pooled with draw d of every
    other, the REAL draw with the REAL draw, the BINDING toll, then canon ->
    summarise -> canon.  Reads only the filed per-cell ledgers."""
    out: dict = {"summary": {}, "real": {}, "n_draws": {}, "assets": {}}
    for v in variants:
        man = null_manifest(v)
        assets = list(man["commission"]["assets"])
        nd = int(man["n_draws"])
        P = C.pools_for(assets) if pools is None else pools
        root = NULL_ROOT / N.VARIANT_DIR[v]
        out["n_draws"][v], out["assets"][v] = nd, assets
        for lens in lenses:
            ev = pd.concat([pd.read_parquet(C.cell_dir(root, s, lens) / "null_events.parquet",
                                            columns=N.POOL_COLUMNS) for s in assets],
                           ignore_index=True)
            ev = ev[ev["scale_kind"] == KIND]
            gr = pd.concat([pd.read_parquet(C.cell_dir(root, s, lens) / "null_grid.parquet")
                            for s in assets], ignore_index=True)
            gr = gr[gr["scale_kind"] == KIND]
            for pool, mem in P.items():
                led, tl = ev[ev["asset"].isin(mem)], gr[gr["asset"].isin(mem)]
                scales = sorted(set(tl["scale_mult"]))
                rows = []
                for draw in [N.REAL_DRAW] + list(range(nd)):
                    rows += [dict(r, draw=int(draw)) for r in C.grid_rows(
                        led[led["draw"] == draw], pool, lens, KIND,
                        scales[0] if len(scales) == 1 else float("nan"), None,
                        "per asset — see the asset rows", tolls=tl[tl["draw"] == draw])]
                g = C.canon(pd.DataFrame(rows), N.NULL_GRID_KEY)
                out["summary"][(v, lens, pool)] = C.canon(N.summarise(g), N.NULL_SUMMARY_KEY)
                out["real"][(v, lens, pool)] = g[g["draw"] == N.REAL_DRAW].reset_index(drop=True)
            del ev, gr
    return out


def null_cell(s: pd.DataFrame, cls: str, era: str, hn: str) -> str:
    """The digest's own null cell format (tierc10_census.digest, null_cell)."""
    q = s[(s["cls"] == cls) & (s["era"] == era) & (s["horizon"] == hn)
          & (s["stat"] == "median_term")]
    if len(q) != 1:
        return "—"
    r = q.iloc[0]
    if not np.isfinite(r["null_median"]):
        return "NaN"
    base = f"{r['null_median']:+.3f} [{r['null_q25']:+.3f}, {r['null_q75']:+.3f}]"
    return (base + f" pct {r['real_pctile_in_null']:.0f}"
            if np.isfinite(r["real_pctile_in_null"]) else base)


NULL_LABEL = ("*Tier-E · report-only · COMPUTED AT CLOSE, not in the digest · null beside "
              "{pool} · {lens} · {kind} · era {era} · median term, K = {k} draws*\n\n")
NULL_HEAD = ("| class | null gaps+order (H20) · of record | null gaps-only (H20) | "
             "null gaps+order (H100) · of record | null gaps-only (H100) |\n"
             "|---|---|---|---|---|\n")


def null_table(nl: dict, key: tuple, classes: list[str]) -> str:
    pool, lens, kind, era = key
    ks = sorted(set(nl["n_draws"].values()))
    s_rec = nl["summary"][(OF_RECORD, lens, pool)]
    s_alt = nl["summary"][(VARIANTS[1], lens, pool)]
    out = NULL_LABEL.format(pool=pool, lens=lens, kind=kind, era=era,
                            k="/".join(str(k) for k in ks)) + NULL_HEAD
    for cls in classes:
        out += ("| " + " | ".join([cls, null_cell(s_rec, cls, era, "H20"),
                                   null_cell(s_alt, cls, era, "H20"),
                                   null_cell(s_rec, cls, era, "H100"),
                                   null_cell(s_alt, cls, era, "H100")]) + " |\n")
    return out + "\n"


# ═══════════════════════════════════════════════ 4 · THE BUILD
VERB_LABEL = "*Tier-E · report-only · verbatim from `{src}` · {spans}*\n\n"


def publish_consts(text: str | None = None) -> dict:
    """BOX_BYTES / FLAG_BYTES by ast.literal_eval — the module is never imported."""
    tree = ast.parse(PUBLISH.read_text() if text is None else text)
    got: dict = {}
    for node in tree.body:
        if (isinstance(node, ast.Assign) and len(node.targets) == 1
                and isinstance(node.targets[0], ast.Name)
                and node.targets[0].id in ("BOX_BYTES", "FLAG_BYTES")):
            if node.targets[0].id in got:
                halt(f"{node.targets[0].id} assigned twice in scripts/publish_exchange.py")
            got[node.targets[0].id] = ast.literal_eval(node.value)
    if set(got) != {"BOX_BYTES", "FLAG_BYTES"}:
        halt(f"scripts/publish_exchange.py: found {sorted(got)}, need BOX_BYTES and FLAG_BYTES")
    return got


def m_log() -> list[tuple[str, int]]:
    out = []
    for name, p in M_TABLES:
        m = pd.read_parquet(p, columns=["m_looks_this_table"])["m_looks_this_table"].unique()
        if len(m) != 1:
            halt(f"{name}: m_looks_this_table is not one value ({list(m)})")
        out.append((name, int(m[0])))
    for v in VARIANTS:
        p = NULL_ROOT / N.VARIANT_DIR[v] / "null_summary.parquet"
        m = pd.read_parquet(p, columns=["m_looks_this_table"])["m_looks_this_table"].unique()
        if len(m) != 1:
            halt(f"null_summary {v}: m_looks_this_table is not one value")
        out.append((f"null_summary ({v})", int(m[0])))
    return out


def build(nl: dict, plant: str | None = None) -> tuple[bytes, dict]:
    """The section, as bytes.  `plant` exists for break legs only (never on disk)."""
    dg, ru = Source(DIGEST), Source(RULINGS)
    S = select(dg, ru)
    pin = D.load_pin()
    consts = publish_consts()
    mans = {v: null_manifest(v) for v in VARIANTS}
    pooled = sorted({p for m in mans.values() for p in m["commission"]["pooled"]})
    acc = pd.read_parquet(ACCEPT, columns=["promoted", "engine_default_after"])
    ver = pd.read_parquet(VERDICT, columns=["asset"])
    promoted, eda = acc["promoted"].unique(), acc["engine_default_after"].unique()
    if len(promoted) != 1 or len(eda) != 1:
        halt("acceptance_head_to_head: promoted / engine_default_after is not one value")

    parts: list = []                  # ("own", str) | ("verb", src, spans) | ("null", key, cls)

    def own(s: str):
        parts.append(("own", s))

    def verb(src: Source, spans):
        parts.append(("verb", src, list(spans)))

    # the F-S2-NULL rows count (for m) before rendering
    blocks = [(key, sp, classes_of(dg.get(*sp[0]))) for key, sp in S["F_blocks"]]
    for key, _, cl in blocks:
        if plant == "collar_off" and key[1] == "5m" and key[3] != C.ERA_TUNING:
            cl[:] = list(C.CLASSES)
    n_null_rows = sum(len(cl) for _, _, cl in blocks)
    n_null_cells = n_null_rows * len(C.HORIZONS) * len(VARIANTS)

    own("## 2 · CENSUS-R\n\n**Tier-E · A SELECTION, not a result · m logged**\n\n")
    own(f"- **Digest of record:** `{rel(DIGEST)}` · sha256 `{dg.sha}` · {len(dg.raw):,} B · "
        f"{len(dg.lines):,} lines. Every block labelled *verbatim* is that file's own bytes "
        "at the line span its label names — selected by heading span, never retyped — and "
        f"F-S2-SLICE checks each one byte for byte (`{rel(TRANSCRIPT)}`).\n")
    own(f"- **As of** {pin['as_of_last_closed_4h']} (`{rel(D.OUT / 'AS_OF_PIN.json')}`) · "
        f"substrate `{Path(_ENV).name}` · built by `{rel(SELF)}` from filed artifacts only. "
        "TIER-E, REPORT-ONLY: nothing below is scored, nothing gates anything, and no "
        "registration or verdict is read.\n")
    own(f"- **The one thing here that is not in the digest:** the *null beside* tables in "
        f"2.3. The null stage pooled {', '.join(pooled)} only (`null/<variant>/"
        "build_manifest.json` → `commission.pooled`), so the digest prints no null beside "
        f"its {SUB_POOLS[0]} / {SUB_POOLS[1]} blocks. They are computed here from the filed "
        "per-cell null ledgers by the null build's own pooling path (`tierc10_census."
        "grid_rows` per draw, then `tierc10_null.summarise`); F-S2-NULL-ANCHOR proves that "
        "path reproduces the filed POOLED:ALL null summary exactly, and that its REAL draw "
        "is the census's own sub-pool outcome row.\n")
    own("- **m logged**, read from each table's `m_looks_this_table` (no multiplicity "
        "correction; nothing here is a test): "
        + " · ".join(f"{n} m = {m:,}" for n, m in m_log())
        + f". This selection adds {n_null_cells:,} close-time null cells ({n_null_rows} class "
        f"rows × {len(C.HORIZONS)} horizons × {len(VARIANTS)} variants).\n")
    size_at = len(parts)
    own("")                                                   # the SIZE line, fixed below
    own("\n")
    if plant == "clock":
        own(f"<!-- built {time.time_ns()} -->\n\n")
    verb(dg, S["banner"])

    # 2.1 · §A
    a0, a1 = S["A"]
    a_sp = S["A_head"] + [s for _, sp in S["A_lens"] for s in sp] + S["A_tail"]
    own(f"### 2.1 · THE ACCEPTANCE HEAD-TO-HEAD [Q-R4] — digest §A (L{a0}–L{a1})\n\n"
        "The ruling and the no-promotion clause; the three full-history H20 tables "
        f"({C.POOL_ALL} · {KIND}), each with the data's default named under it; the tuning "
        "and holdout H20 defaults; the H100 defaults and the digest's own reading. "
        f"`promoted` reads “{promoted[0]}” and `engine_default_after` reads “{eda[0]}” on all "
        f"{len(acc):,} rows of `{rel(ACCEPT)}` (F-S2-PROMOTE). Left in the digest: "
        f"{omitted(dg, a0 + 1, a1, a_sp)}.\n\n")
    verb(dg, S["A_head"])
    for _, sp in S["A_lens"]:
        verb(dg, sp)
    verb(dg, S["A_tail"])

    # 2.2 · §B / B.3
    b0, b1 = S["B"]
    b_sp = S["B_head"] + S["B_table"]
    n_pool_keys = int(ver["asset"].str.startswith("POOLED:").sum())
    own(f"### 2.2 · HEIGHT-vs-TOLL [Q-R3] — digest §B (L{b0}–L{b1}), the POOLED verdict rows "
        "of B.3\n\n"
        "The gate: the ruling, the two legs, their conjunction and the sample floor. Then, "
        f"out of B.3's whole grid of {S['B_grid_rows']:,} filed rows, the "
        f"{S['B_pooled_rows']} POOLED rows (every pool × lens × scale kind × era — the "
        "verdict is keyed on the era, so every era is shown). F-S2-PARQUET checks every "
        "printed `verdict_pass`, `ratio_median` and `edge_net_h20` against "
        f"`{rel(VERDICT)}` ({n_pool_keys} POOLED keys there) on (lens, scale_kind, asset, "
        f"era). Left in the digest: {omitted(dg, b0 + 1, b1, b_sp)}.\n\n")
    verb(dg, S["B_head"])
    verb(dg, S["B_table"])

    # 2.3 · §5
    f0, f1 = S["F"]
    own(f"### 2.3 · OUTCOME AFTER EVENT — digest §5 (L{f0}–L{f1}), {SUB_POOLS[0]} and "
        f"{SUB_POOLS[1]}, beside their nulls\n\n"
        f"The method and the two filed null variants; then {len(blocks)} blocks — "
        f"{SUB_POOLS[0]} beside {SUB_POOLS[1]}, {KIND}, eras {SEL_ERAS[0]} and "
        f"{SEL_ERAS[1]}, every lens — each followed by its own pooled null, "
        f"{OF_RECORD} (the null of record) first. Left in the digest: the other "
        f"{S['F_subs_total'] - len(blocks)} blocks of §5 ({C.POOL_ALL} with its filed null, "
        "the tuning era, the calibrated SCALE) and its closing note.\n\n")
    verb(dg, S["F_head"])
    own(f"The null of record, from `{rel(RULINGS)}` §R10 (L{S['R10_span'][0]}–"
        f"L{S['R10_span'][1]}):\n\n")
    verb(ru, S["R10"])
    for key, sp, cl in blocks:
        verb(dg, sp)
        if plant == "drop_null" and key == blocks[0][0]:
            continue
        parts.append(("null", key, list(cl)))

    # 2.4 · §1
    c0, c1 = S["C"]
    own(f"### 2.4 · COVERAGE · CONFIRMED-RANGE DENSITY · MEAN LIFE — digest §1 (L{c0}–L{c1})"
        f"\n\nThe definitions and the per-lens tables. Left in the digest: the SCALE "
        f"calibrator's whole grid ({fmt_spans(S['C_left'])}).\n\n")
    verb(dg, S["C_body"])

    # 2.5 · §2
    g0, g1 = S["G"]
    own(f"### 2.5 · F-RF-4 — SPRING / UPTHRUST OVERLAP — digest §2 (L{g0}–L{g1}), whole\n\n")
    verb(dg, S["G_body"])

    # 2.6 · what stays in the digest
    took = [s for p in parts if p[0] == "verb" and p[1] is dg for s in p[2]]
    whole_left = []
    for ln, lv, title in dg.heads:
        if lv != 2:
            continue
        s0, s1 = dg.span_at(ln)
        if not any(s0 <= a <= s1 for a, _ in took):
            whole_left.append(f"§{title[3:]} (L{s0}–L{s1})")
    own("### 2.6 · WHAT STAYS IN THE DIGEST\n\n"
        f"Whole sections not selected: {' · '.join(whole_left)}. From its title block "
        f"(L{S['title_block'][0]}–L{S['title_block'][1]}) only the banner, the warranty, "
        "the collar and the era law are spliced above. The digest is the table of record; "
        "this section is a reading order, not a result.\n")

    def render(size_line: str) -> bytes:
        out = []
        for i, p in enumerate(parts):
            if i == size_at:
                out.append(size_line.encode())
            elif p[0] == "own":
                out.append(p[1].encode())
            elif p[0] == "verb":
                body = b"".join(p[1].get(a, b) for a, b in p[2])
                out.append(VERB_LABEL.format(src=p[1].name, spans=fmt_spans(p[2])).encode())
                out.append(body + (b"" if body.endswith(b"\n\n") else b"\n"))
            else:
                out.append(null_table(nl, p[1], p[2]).encode())
        return b"".join(out)

    def size_line(n: int) -> str:
        over = n > consts["FLAG_BYTES"] or plant == "unflag_over"
        flag = ("FLAG: **YES** — over the naming trip-wire: named to the operator at "
                "creation, with its intended home (`research_outputs/tierc10/close/`, "
                "spliced into the build document's §2 at CLOSE); naming only, never a "
                "refusal (`scripts/publish_exchange.py`, the FLAG_BYTES comment)"
                if over and plant != "unflag_over" else
                "FLAG: no — at or under the naming trip-wire")
        return (f"- **SIZE:** {n:,} B · FLAG_BYTES {consts['FLAG_BYTES']:,} B · BOX_BYTES "
                f"{consts['BOX_BYTES']:,} B (both read by `ast.literal_eval` from "
                f"`{rel(PUBLISH)}`) · {flag}.\n")

    n = 0
    for _ in range(12):                 # the SIZE line states its own file's size
        doc = render(size_line(n))
        if len(doc) == n:
            break
        n = len(doc)
    else:
        halt("the SIZE line did not reach a fixed point")
    info = {"digest": dg, "rulings": ru, "S": S, "consts": consts, "blocks": blocks,
            "n_null_rows": n_null_rows, "n_null_cells": n_null_cells, "pin": pin}
    return doc, info


# ═══════════════════════════════════════════════ 5 · PARSING THE FILED SECTION
_E = lambda s: re.escape(s.encode())                                   # noqa: E731
VERB_RE = re.compile(_E("*Tier-E · report-only · verbatim from `") + rb"([^`\n]+)"
                     + _E("` · ") + rb"((?:L\d+" + _E("–") + rb"L\d+)(?: \+ L\d+" + _E("–")
                     + rb"L\d+)*)" + _E("*\n\n"), re.M)
NULL_RE = re.compile(_E("*Tier-E · report-only · COMPUTED AT CLOSE, not in the digest · "
                        "null beside ") + rb"(POOLED:\S+)" + _E(" · ") + rb"(\S+)" + _E(" · ")
                     + rb"(\S+)" + _E(" · era ") + rb"(\S+)" + _E(" · ") + rb"[^\n]*\*\n\n",
                     re.M)
SPAN_RE = re.compile(rb"L(\d+)" + _E("–") + rb"L(\d+)")
NUM_CELL = re.compile(r"^[+-]\d+\.\d{3} \[[+-]\d+\.\d{3}, [+-]\d+\.\d{3}\]( pct \d+)?$")
BLOCK_HEAD = re.compile(r"^### (POOLED:\S+) · (\S+) · (\S+) · era `(\S+)`")


def labels(doc: bytes, sources: dict) -> list[dict]:
    """Every label in the section, in order, with the bytes it claims."""
    out = []
    for m in VERB_RE.finditer(doc):
        src = sources.get(m.group(1).decode())
        spans = [(int(a), int(b)) for a, b in SPAN_RE.findall(m.group(2))]
        out.append({"kind": "verb", "at": m.start(), "body_at": m.end(),
                    "src": m.group(1).decode(), "source": src, "spans": spans})
    for m in NULL_RE.finditer(doc):
        out.append({"kind": "null", "at": m.start(), "body_at": m.end(),
                    "key": tuple(x.decode() for x in m.groups())})
    return sorted(out, key=lambda x: x["at"])


def expected(lb: dict) -> bytes:
    return b"".join(lb["source"].get(a, b) for a, b in lb["spans"])


def table_after(doc: bytes, at: int) -> list[list[str]]:
    """The markdown table starting at byte `at`, as cell lists (header first,
    separator dropped); stops at the first line that is not a table row."""
    rows = []
    for ln in doc[at:].decode("utf-8").split("\n"):
        if not ln.startswith("|"):
            break
        if ln.startswith("|---"):
            continue
        rows.append([c.strip() for c in ln.split("|")[1:-1]])
    return rows


def sources_now() -> dict:
    return {DIGEST.name: Source(DIGEST), RULINGS.name: Source(RULINGS)}


def cat_of(dg: Source, lb: dict) -> str:
    if lb["kind"] == "null":
        return "outcome"
    if lb["src"] != DIGEST.name:
        return "ruling"
    sec = dg.section_of(lb["spans"][0][0])
    for pre, cat in (("## A ·", "acceptance"), ("## B ·", "height-vs-toll"),
                     ("## 5 ·", "outcome"), ("## 1 ·", "coverage"), ("## 2 ·", "F-RF-4")):
        if sec.startswith(pre):
            return cat
    return "banner" if not sec else "other"


# ═══════════════════════════════════════════════ 6 · THE CHECKS (pure, on bytes)
def slice_findings(doc: bytes, sources: dict) -> tuple[list[str], dict]:
    f, n_sp, n_b = [], 0, 0
    dg = sources[DIGEST.name]
    m = re.search(_E(f"`{rel(DIGEST)}` · sha256 `") + rb"([0-9a-f]{64})`", doc)
    if not m:
        f.append("the header does not name the digest's full path and sha256")
    elif m.group(1).decode() != dg.sha:
        f.append(f"header sha {m.group(1).decode()[:16]}… != digest on disk {dg.sha[:16]}…")
    lbs = [x for x in labels(doc, sources) if x["kind"] == "verb"]
    if not lbs:
        f.append("no verbatim block found")
    for lb in lbs:
        if lb["source"] is None:
            f.append(f"label cites unknown source {lb['src']!r}")
            continue
        try:
            want = expected(lb)
        except ValueError as e:
            f.append(str(e))
            continue
        got = doc[lb["body_at"]:lb["body_at"] + len(want)]
        n_sp += len(lb["spans"])
        n_b += len(want)
        if got != want:
            k = next((i for i, (x, y) in enumerate(zip(got, want)) if x != y), len(got))
            f.append(f"{lb['src']} {fmt_spans(lb['spans'])}: not byte-identical "
                     f"(first difference at block byte {k})")
    return f, {"blocks": len(lbs), "spans": n_sp, "bytes": n_b}


def parquet_findings(doc: bytes, sources: dict, ver: pd.DataFrame) -> tuple[list[str], int]:
    dg = sources[DIGEST.name]
    t0, t1 = dg.span("### B.3 ·")
    rows = []
    for lb in labels(doc, sources):
        if lb["kind"] != "verb" or lb["src"] != DIGEST.name \
                or not all(t0 <= a <= t1 for a, _ in lb["spans"]):
            continue
        body = doc[lb["body_at"]:lb["body_at"] + len(expected(lb))].decode("utf-8")
        for ln in body.split("\n"):
            c = [x.strip() for x in ln.split("|")[1:-1]] if ln.startswith("| ") else []
            if len(c) == 16 and c[0] != "lens":
                rows.append(c)
    f = []
    pv = ver[ver["asset"].str.startswith("POOLED:")].set_index(
        ["lens", "scale_kind", "asset", "era"])
    seen = set()

    def near(printed: str, x: float) -> bool:
        s = printed.replace(",", "")
        d = len(s.split(".")[1]) if "." in s else 0
        return np.isfinite(x) and abs(float(s) - x) <= 0.5 * 10 ** (-d) + 1e-9
    for c in rows:
        k = (c[0], c[1], c[2], c[3])
        if not k[2].startswith("POOLED:"):
            f.append(f"non-POOLED row printed: {k}")
            continue
        if k in seen:
            f.append(f"row printed twice: {k}")
        seen.add(k)
        if k not in pv.index:
            f.append(f"{k}: no such row in height_toll_verdict.parquet")
            continue
        r = pv.loc[k]
        verdict = {"**PASS**": True, "**FAIL**": False}.get(c[15])
        if verdict is None or verdict != bool(r["verdict_pass"]):
            f.append(f"{k}: verdict printed {c[15]} vs verdict_pass {bool(r['verdict_pass'])}")
        if not near(c[5], float(r["ratio_median"])):
            f.append(f"{k}: ratio median printed {c[5]} vs ratio_median "
                     f"{float(r['ratio_median']):.6f}")
        if not near(c[12], float(r["edge_net_h20"])):
            f.append(f"{k}: edge NET printed {c[12]} vs edge_net_h20 "
                     f"{float(r['edge_net_h20']):+.6f}")
    miss = sorted(set(pv.index) - seen)
    if miss:
        f.append(f"{len(miss)} POOLED key(s) of the parquet not printed, e.g. {miss[0]}")
    return f, len(rows)


def order_findings(doc: bytes, sources: dict) -> tuple[list[str], dict]:
    dg = sources[DIGEST.name]
    pos: dict = {}
    for lb in labels(doc, sources):
        pos.setdefault(cat_of(dg, lb), []).append(lb["at"])
    f = []
    first, last = ("acceptance", "height-vs-toll", "outcome"), ("coverage", "F-RF-4")
    for c in first + last:
        if c not in pos:
            f.append(f"no {c} block in the section")
    if not f:
        hi = max(max(pos[c]) for c in first)
        lo = min(min(pos[c]) for c in last)
        if hi >= lo:
            late = [c for c in first if max(pos[c]) >= lo]
            f.append(f"{late} sit(s) after the first coverage/F-RF-4 block (byte {lo:,})")
    return f, {c: len(v) for c, v in sorted(pos.items())}


def null_findings(doc: bytes, sources: dict, nl: dict) -> tuple[list[str], tuple]:
    lbs = labels(doc, sources)
    f, n_ok, n_rows = [], 0, 0
    blocks = []
    for i, lb in enumerate(lbs):
        if lb["kind"] != "verb" or lb["src"] != DIGEST.name:
            continue
        head = lb["source"].text[lb["spans"][0][0] - 1]
        m = BLOCK_HEAD.match(head)
        if m:
            blocks.append((i, lb, m.groups()))
    if not blocks:
        f.append("no outcome block in the section")
    for i, lb, key in blocks:
        want = expected(lb)
        end = lb["body_at"] + len(want)
        nxt = lbs[i + 1] if i + 1 < len(lbs) else None
        gap = doc[end:nxt["at"]] if nxt else doc[end:]
        if nxt is None or nxt["kind"] != "null" or gap.strip():
            f.append(f"{' · '.join(key)}: no null table immediately beside the block")
            continue
        if nxt["key"] != key:
            f.append(f"{' · '.join(key)}: the null beside it is for {' · '.join(nxt['key'])}")
            continue
        tab = table_after(doc, nxt["body_at"])
        head = tab[0] if tab else []
        col = {h: j for j, h in enumerate(head)}
        need = {f"null {v} (H{h})": None for v in VARIANTS for h in ("20", "100")}
        cols = {}
        for want_h in need:
            hit = [j for h, j in col.items() if h.startswith(want_h)]
            if len(hit) != 1:
                f.append(f"{' · '.join(key)}: the null table has no '{want_h}' column")
            else:
                cols[want_h] = hit[0]
        if len(cols) != len(need):
            continue
        blk = classes_of(want)
        got = [r[0] for r in tab[1:]]
        if got != blk:
            f.append(f"{' · '.join(key)}: null rows {got} != block rows {blk}")
            continue
        pool, lens, kind, era = key
        brow = {r[0]: r for r in table_after(want, want.index(b"| class"))[1:]}
        for r in tab[1:]:
            cls = r[0]
            for hn in ("H20", "H100"):
                for v in VARIANTS:
                    cell = r[cols[f"null {v} ({hn})"]]
                    if v == OF_RECORD and not NUM_CELL.match(cell):
                        f.append(f"{' · '.join(key)} {cls} {hn}: gaps+order cell {cell!r}")
                    truth = null_cell(nl["summary"][(v, lens, pool)], cls, era, hn)
                    if cell != truth:
                        f.append(f"{' · '.join(key)} {cls} {hn} {v}: printed {cell!r} "
                                 f"!= computed {truth!r}")
                s = nl["summary"][(OF_RECORD, lens, pool)]
                q = s[(s["cls"] == cls) & (s["era"] == era) & (s["horizon"] == hn)
                      & (s["stat"] == "median_term")]
                j_n, j_m = (1, 2) if hn == "H20" else (5, 6)
                if len(q) != 1 or f"{int(q['real_n'].iloc[0]):,}" != brow[cls][j_n] \
                        or f"{float(q['real'].iloc[0]):+.3f}" != brow[cls][j_m]:
                    f.append(f"{' · '.join(key)} {cls} {hn}: the null's REAL (n, median) is "
                             "not the block's printed n / median")
            n_rows += 1
        n_ok += 1
    return f, (n_ok, n_rows)


def _eq(a: pd.Series, b: pd.Series) -> pd.Series:
    num = pd.api.types.is_numeric_dtype
    if num(a) and num(b) and not (pd.api.types.is_bool_dtype(a) or pd.api.types.is_bool_dtype(b)):
        a, b = a.astype(float), b.astype(float)
        return (a == b) | (a.isna() & b.isna())
    return (a.astype(str) == b.astype(str))


def frame_diff(a: pd.DataFrame, b: pd.DataFrame, key: list, cols: list) -> list[str]:
    if len(a) != len(b):
        return [f"{len(a)} rows vs {len(b)}"]
    a = a.sort_values(key, kind="mergesort").reset_index(drop=True)
    b = b.sort_values(key, kind="mergesort").reset_index(drop=True)
    for k in key:
        if not (a[k].astype(str) == b[k].astype(str)).all():
            return [f"keys differ on {k}"]
    bad = [c for c in cols if not _eq(a[c], b[c]).all()]
    return [f"columns differ: {bad}"] if bad else []


SUMMARY_COLS = ["real", "real_n", "n_draws", "n_draws_valid", "null_n_events_median",
                "null_median", "null_q25", "null_q75", "null_iqr", "null_min", "null_max",
                "real_minus_null_median", "real_pctile_in_null", "nan_reason", "printable"]


def filed_null(v: str) -> pd.DataFrame:
    s = pd.read_parquet(NULL_ROOT / N.VARIANT_DIR[v] / "null_summary.parquet")
    return s[(s["asset"] == C.POOL_ALL) & (s["scale_kind"] == KIND)]


def anchor_findings(summ: dict, filed: dict, real: dict, census: pd.DataFrame,
                    census_label: dict | None = None) -> tuple[list[str], dict]:
    """summ[(v, lens)] = computed POOLED:ALL summary vs filed[v]; real[(v, lens, pool)]
    = computed REAL draw rows vs the census outcome_grid rows of census_label[pool]."""
    f, n_sum, n_real = [], 0, 0
    for (v, lens), mine in summ.items():
        ff = filed[v]
        ff = ff[ff["lens"] == lens]
        d = frame_diff(mine, ff, N.NULL_SUMMARY_KEY, SUMMARY_COLS)
        if d:
            f.append(f"POOLED:ALL {lens} {v}: computed != filed null_summary ({d[0]})")
        n_sum += len(ff)
    cols = list(N.ANCHOR_COLUMNS)
    key = ["cls", "era", "horizon"]
    for (v, lens, pool), mine in real.items():
        lab = (census_label or {}).get(pool, pool)
        cg = census[(census["asset"] == lab) & (census["lens"] == lens)
                    & (census["scale_kind"] == KIND)]
        d = frame_diff(mine[key + cols], cg[key + cols], key, cols)
        if d:
            f.append(f"{pool} {lens} {v}: REAL draw != census outcome_grid {lab} ({d[0]})")
        n_real += len(cg)
    return f, {"summary_rows": n_sum, "real_rows": n_real}


def promote_findings(doc: bytes, sources: dict, acc: pd.DataFrame) -> tuple[list[str], int]:
    f = []
    bad_p = acc[~acc["promoted"].astype(str).str.startswith("NOTHING")]
    if len(bad_p):
        f.append(f"{len(bad_p)} row(s) promote something: {bad_p['promoted'].iloc[0]!r}")
    bad_e = acc[~acc["engine_default_after"].astype(str).str.contains("UNCHANGED")]
    if len(bad_e):
        f.append(f"{len(bad_e)} row(s) move the engine default: "
                 f"{bad_e['engine_default_after'].iloc[0]!r}")
    dg = sources[DIGEST.name]
    a0, a1 = dg.span("## A · [Q-R4]")
    text = ""
    for lb in labels(doc, sources):
        if lb["kind"] == "verb" and lb["src"] == DIGEST.name \
                and all(a0 <= a <= a1 for a, _ in lb["spans"]):
            text += doc[lb["body_at"]:lb["body_at"] + len(expected(lb))].decode("utf-8")
    named = []
    for m in re.finditer(r"^> THE DATA'S DEFAULT AT (\S+) / (\S+) / (H20): \*\*([^*]+)\*\* "
                         r"\(NET ([+-][\d.]+) ATR on n = ([\d,]+)(.*)$", text, re.M):
        named.append(m.groups()[:6] + ("NAMED ONLY: no pin moves" in m.group(7),))
    h = text.find("**THE DATA'S DEFAULT AT H100**")
    for ln in text[h:].split("\n") if h >= 0 else []:
        c = [x.strip() for x in ln.split("|")[1:-1]] if ln.startswith("| ") else []
        if len(c) == 7 and c[0] in C.LENSES:
            named.append((c[0], c[1], "H100", c[2].strip("*"), c[3], c[4], True))
    P = acc[(acc["asset"] == C.POOL_ALL) & (acc["scale_kind"] == KIND)]
    cells = set(zip(P["lens"], P["era"], P["horizon"]))
    got = set()
    for lens, era, hz, rule, net, n, clause in named:
        s = P[(P["lens"] == lens) & (P["era"] == era) & (P["horizon"] == hz)]
        got.add((lens, era, hz))
        if not len(s):
            f.append(f"{lens}/{era}/{hz}: no parquet cell")
            continue
        b = s.loc[s["net"].idxmax()]
        d = len(net.split(".")[1])
        if rule != b["variant"]:
            f.append(f"{lens}/{era}/{hz}: named {rule!r} but the max-NET rule is "
                     f"{b['variant']!r}")
        elif abs(float(net) - float(b["net"])) > 0.5 * 10 ** (-d) + 1e-9 \
                or int(n.replace(",", "")) != int(b["n_declared"]):
            f.append(f"{lens}/{era}/{hz}: NET/n printed {net}/{n} vs {b['net']:+.6f}/"
                     f"{int(b['n_declared'])}")
        if not clause:
            f.append(f"{lens}/{era}/{hz}: the default is named without 'NAMED ONLY: no pin "
                     "moves'")
    if cells - got:
        f.append(f"{len(cells - got)} (lens, era, horizon) default(s) not named, e.g. "
                 f"{sorted(cells - got)[0]}")
    return f, len(named)


def collar_findings(doc: bytes, sources: dict) -> tuple[list[str], int]:
    f, n = [], 0
    for lb in labels(doc, sources):
        if lb["kind"] == "null":
            pool, lens, kind, era = lb["key"]
            rows = table_after(doc, lb["body_at"])[1:]
        elif lb["kind"] == "verb" and lb["src"] == DIGEST.name:
            m = BLOCK_HEAD.match(lb["source"].text[lb["spans"][0][0] - 1])
            if not m:
                continue
            pool, lens, kind, era = m.groups()
            want = expected(lb)
            rows = [[c] for c in classes_of(want)]
        else:
            continue
        for r in rows:
            n += 1
            if not C.printable(lens, r[0], era):
                f.append(f"{pool} · {lens} · era {era}: collared class {r[0]} printed "
                         f"({lb['kind']})")
    return f, n


SIZE_RE = re.compile(_E("- **SIZE:** ") + rb"([\d,]+)" + _E(" B · FLAG_BYTES ")
                     + rb"([\d,]+)" + _E(" B · BOX_BYTES ") + rb"([\d,]+)" + rb"[^\n]*?"
                     + rb"FLAG: (\*\*YES\*\*|no)")


def size_findings(doc: bytes, consts: dict) -> tuple[list[str], dict]:
    f = []
    m = SIZE_RE.search(doc)
    size, flag_b = len(doc), consts["FLAG_BYTES"]
    if not m:
        return ["no SIZE line"], {"bytes": size}
    said = int(m.group(1).decode().replace(",", ""))
    said_flag = int(m.group(2).decode().replace(",", ""))
    said_box = int(m.group(3).decode().replace(",", ""))
    flagged = m.group(4) == b"**YES**"
    if said != size:
        f.append(f"the SIZE line says {said:,} B; the file is {size:,} B")
    if said_flag != flag_b or said_box != consts["BOX_BYTES"]:
        f.append(f"the SIZE line says FLAG_BYTES {said_flag:,} / BOX_BYTES {said_box:,}; "
                 f"publish_exchange.py has {flag_b:,} / {consts['BOX_BYTES']:,}")
    if size > flag_b and not flagged:
        f.append(f"{size:,} B > FLAG_BYTES {flag_b:,} B and NOT flagged")
    if size <= flag_b and flagged:
        f.append(f"{size:,} B <= FLAG_BYTES {flag_b:,} B yet flagged")
    return f, {"bytes": size, "flagged": flagged, "over": size > flag_b}


# ═══════════════════════════════════════════════ 7 · THE LEGS
CTX: dict = {}


def leg_slice():
    doc, src = CTX["doc"], CTX["sources"]

    def flip_digit():
        lb = [x for x in labels(doc, src) if x["kind"] == "verb"][1]
        i = next(k for k in range(lb["body_at"], len(doc)) if 48 <= doc[k] <= 57)
        bad = doc[:i] + bytes([48 + (doc[i] - 47) % 10]) + doc[i + 1:]
        return slice_findings(bad, src)[0]

    def wrong_sha():
        return slice_findings(doc.replace(src[DIGEST.name].sha.encode(),
                                          sha256(b"another digest").encode()), src)[0]

    def shifted_span():
        lb = [x for x in labels(doc, src) if x["kind"] == "verb"][2]
        a, b = lb["spans"][0]
        old = f"L{a}–L{b}".encode()
        i = doc.index(old, lb["at"])
        bad = doc[:i] + f"L{a + 1}–L{b + 1}".encode() + doc[i + len(old):]
        return slice_findings(bad, src)[0]
    b = lambda: plants([("one digit flipped inside a spliced block", flip_digit),   # noqa: E731
                        ("the header names another digest's sha", wrong_sha),
                        ("a label cites its span shifted by one line", shifted_span)])

    def real():
        f, st = slice_findings(doc, src)
        return (not f, f"{st['blocks']} verbatim blocks · {st['spans']} spans · "
                       f"{st['bytes']:,} of {len(doc):,} B byte-identical to their sources; "
                       f"digest sha256 {src[DIGEST.name].sha[:16]}… = the header's"
                       + (f" · {f[:3]}" if f else ""))
    return b, real


def leg_parquet():
    doc, src, ver = CTX["doc"], CTX["sources"], CTX["ver"]

    def edit_parquet(col, how):
        v = ver.copy()
        i = v.index[v["asset"].str.startswith("POOLED:")][4]
        v.loc[i, col] = how(v.loc[i, col])
        return parquet_findings(doc, src, v)[0]

    def edit_doc():
        t = src[DIGEST.name]
        t0, _ = t.span("### B.3 ·")
        row = next(x for x in labels(doc, src) if x["kind"] == "verb"
                   and x["spans"][0][0] >= t0 and x["src"] == DIGEST.name)
        body = doc[row["body_at"]:]
        line = next(ln for ln in body.split(b"\n") if b"| POOLED:" in ln)
        cells = line.split(b"|")
        cells[13] = cells[13].replace(b"-", b"+", 1) if b"-" in cells[13] else \
            cells[13].replace(b"+", b"-", 1)
        return parquet_findings(doc.replace(line, b"|".join(cells), 1), src, ver)[0]

    def drop_row():
        line = next(ln for ln in doc.split(b"\n") if ln.startswith(b"| 4h | frozen3.0 | POOLED:"))
        return parquet_findings(doc.replace(line + b"\n", b"", 1), src, ver)[0]
    b = lambda: plants([                                                     # noqa: E731
        ("parquet: one ratio_median cell +0.01", lambda: edit_parquet("ratio_median",
                                                                      lambda x: x + 0.01)),
        ("parquet: one edge_net_h20 cell +0.001", lambda: edit_parquet("edge_net_h20",
                                                                       lambda x: x + 0.001)),
        ("parquet: one verdict_pass flipped", lambda: edit_parquet("verdict_pass",
                                                                   lambda x: not x)),
        ("section: one edge NET sign flipped", edit_doc),
        ("section: one POOLED row deleted", drop_row)])

    def real():
        f, n = parquet_findings(doc, src, ver)
        return (not f, f"{n} POOLED verdict rows printed = every POOLED key of "
                       f"{rel(VERDICT)}; verdict_pass exact, ratio_median / edge_net_h20 "
                       "within half a unit of the printed digit" + (f" · {f[:3]}" if f else ""))
    return b, real


def leg_order():
    doc, src = CTX["doc"], CTX["sources"]

    def move(sec_from: bytes, sec_to: bytes, before: bytes):
        i0 = doc.index(sec_from)
        i1 = doc.index(sec_to, i0)
        chunk, rest = doc[i0:i1], doc[:i0] + doc[i1:]
        j = rest.index(before)
        return order_findings(rest[:j] + chunk + rest[j:], src)[0]
    b = lambda: plants([                                                     # noqa: E731
        ("F-RF-4 moved to the front", lambda: move(b"### 2.5 ", b"### 2.6 ", b"### 2.1 ")),
        ("coverage moved ahead of the outcome tables",
         lambda: move(b"### 2.4 ", b"### 2.5 ", b"### 2.3 "))])

    def real():
        f, pos = order_findings(doc, src)
        return (not f, f"blocks per kind {pos}; every acceptance / height-vs-toll / outcome "
                       "block precedes the first coverage and F-RF-4 block"
                       + (f" · {f}" if f else ""))
    return b, real


def leg_null():
    doc, src, nl = CTX["doc"], CTX["sources"], CTX["nl"]

    def blank_cell():
        lb = next(x for x in labels(doc, src) if x["kind"] == "null")
        i = lb["body_at"] + doc[lb["body_at"]:].index(b"\n| ") + 3
        j = doc.index(b" | ", i) + 3
        k = doc.index(b" | ", j)
        return null_findings(doc[:j] + "—".encode() + doc[k:], src, nl)[0]

    def only_gaps_only():
        return null_findings(doc.replace(b"null gaps+order", b"null gaps-ONLY"), src, nl)[0]
    b = lambda: plants([                                                     # noqa: E731
        ("one null table removed", lambda: null_findings(CTX["doc_drop_null"], src, nl)[0]),
        ("one gaps+order cell blanked to an em dash", blank_cell),
        ("the gaps+order columns renamed away", only_gaps_only)])

    def real():
        f, (n, rows) = null_findings(doc, src, nl)
        return (not f, f"{n} of {len(CTX['info']['blocks'])} outcome blocks ({rows} class rows) "
                       "carry their pooled null beside them — gaps+order (of record) and "
                       "gaps-only, H20 and H100, one row per block row, every cell = the close-time "
                       "computation, the null's REAL (n, median) = the block's printed "
                       "n / median" + (f" · {f[:3]}" if f else ""))
    return b, real


def leg_anchor():
    nl, census = CTX["nl"], CTX["census"]
    filed = {v: filed_null(v) for v in VARIANTS}
    summ = {(v, lens): nl["summary"][(v, lens, C.POOL_ALL)]
            for v in VARIANTS for lens in C.LENSES}
    real = {(v, lens, p): nl["real"][(v, lens, p)]
            for v in VARIANTS for lens in C.LENSES for p in SUB_POOLS}

    def dropped():
        assets = nl["assets"][OF_RECORD]
        x = compute_nulls(lenses=("1d",), variants=(OF_RECORD,),
                          pools={C.POOL_ALL: assets[:-1]})
        return anchor_findings({(OF_RECORD, "1d"): x["summary"][(OF_RECORD, "1d", C.POOL_ALL)]},
                               filed, {}, census)[0]

    def swapped():
        return anchor_findings({(OF_RECORD, "1d"): summ[(VARIANTS[1], "1d")]}, filed, {},
                               census)[0]

    def wrong_pool():
        return anchor_findings({}, filed, {(OF_RECORD, "1d", SUB_POOLS[0]):
                                           real[(OF_RECORD, "1d", SUB_POOLS[0])]}, census,
                               {SUB_POOLS[0]: SUB_POOLS[1]})[0]
    b = lambda: plants([                                                     # noqa: E731
        ("POOLED:ALL 1d pooled over 16 of 17 members", dropped),
        ("the gaps-only computation held against the filed gaps+order", swapped),
        (f"{SUB_POOLS[0]}'s REAL held against the census's {SUB_POOLS[1]}", wrong_pool)])

    def real_leg():
        f, st = anchor_findings(summ, filed, real, census)
        mans = {v: null_manifest(v)["commission"]["pooled"] for v in VARIANTS}
        return (not f, f"the close-time path reproduces all {st['summary_rows']:,} filed "
                       f"POOLED:ALL null_summary rows ({KIND}, {len(C.LENSES)} lenses, both "
                       f"variants, {len(SUMMARY_COLS)} columns, exact) and its REAL draw "
                       f"equals {st['real_rows']:,} census outcome_grid rows of "
                       f"{'/'.join(SUB_POOLS)} ({len(N.ANCHOR_COLUMNS)} columns, exact); "
                       f"filed commission.pooled = {mans}" + (f" · {f[:3]}" if f else ""))
    return b, real_leg


def leg_promote():
    doc, src, acc = CTX["doc"], CTX["sources"], CTX["acc"]

    def promoted():
        a = acc.copy()
        a.loc[a.index[7], "promoted"] = "BREAK_CONFIRM_N=6 — PROMOTED"
        return promote_findings(doc, src, a)[0]

    def reorder():
        a = acc.copy()
        s = a[(a["asset"] == C.POOL_ALL) & (a["scale_kind"] == KIND) & (a["lens"] == "4h")
              & (a["era"] == C.ERA_ALL) & (a["horizon"] == "H20")]
        lo = s.loc[s["net"].idxmin()]
        a.loc[lo.name, "net"] = float(s["net"].max()) + 1.0
        return promote_findings(doc, src, a)[0]

    def renamed():
        m = re.search(rb"(> THE DATA'S DEFAULT AT \S+ / \S+ / H20: \*\*)([^*]+)(\*\*)", doc)
        other = b"2-close" if m.group(2) != b"2-close" else b"3-close"
        return promote_findings(doc[:m.start(2)] + other + doc[m.end(2):], src, acc)[0]
    b = lambda: plants([("parquet: one row's `promoted` names a pin move", promoted),  # noqa
                        ("parquet: another rule made the max-NET rule", reorder),
                        ("section: a named default swapped for another rule", renamed)])

    def real():
        f, n = promote_findings(doc, src, acc)
        return (not f, f"{n} named defaults (H20 + H100, every lens x era) = the max-NET rule "
                       f"of {rel(ACCEPT)}; `promoted` NOTHING and `engine_default_after` "
                       f"UNCHANGED on all {len(acc):,} rows" + (f" · {f[:3]}" if f else ""))
    return b, real


def leg_collar():
    doc, src = CTX["doc"], CTX["sources"]
    b = lambda: plants([("the null tables rendered with the collar off",      # noqa: E731
                         lambda: collar_findings(CTX["doc_collar_off"], src)[0])])

    def real():
        f, n = collar_findings(doc, src)
        return (not f, f"{n} outcome/null rows printed, none a 5m retest-hold row outside the "
                       "tuning era (tierc10_census.printable)" + (f" · {f[:3]}" if f else ""))
    return b, real


def leg_size():
    doc, consts = CTX["doc"], CTX["consts"]

    def over_unflagged():
        bad = CTX["doc_unflag"]
        pad = b"<!-- pad -->\n" * ((consts["FLAG_BYTES"] - len(bad)) // 13 + 2)
        body = bad + pad
        m = SIZE_RE.search(body)
        for _ in range(4):
            body = body[:m.start(1)] + f"{len(body):,}".encode() + body[m.end(1):]
            m = SIZE_RE.search(body)
        return size_findings(body, consts)[0]

    def off_by_one():
        m = SIZE_RE.search(doc)
        n = int(m.group(1).decode().replace(",", "")) + 1
        return size_findings(doc[:m.start(1)] + f"{n:,}".encode() + doc[m.end(1):], consts)[0]

    def misread():
        txt = PUBLISH.read_text()
        other = publish_consts(re.sub(r"(?m)^FLAG_BYTES = .*$", "FLAG_BYTES = 1_000_000", txt))
        return size_findings(doc, other)[0]
    b = lambda: plants([("a copy over FLAG_BYTES, unflagged", over_unflagged),  # noqa: E731
                        ("the SIZE line off by one byte", off_by_one),
                        ("FLAG_BYTES re-read from a doctored publish_exchange.py", misread)])

    def real():
        f, st = size_findings(doc, consts)
        return (not f, f"{st['bytes']:,} B · FLAG_BYTES {consts['FLAG_BYTES']:,} · BOX_BYTES "
                       f"{consts['BOX_BYTES']:,} ({100 * st['bytes'] / consts['BOX_BYTES']:.3f}% "
                       f"of the box) · {'OVER, FLAGGED' if st['over'] else 'under, unflagged'}"
                       + (f" · {f}" if f else ""))
    return b, real


def leg_det():
    doc = CTX["doc"]

    def clocked():
        x, _ = build(CTX["nl"], plant="clock")
        return [] if x == doc else ["a build carrying a wall-clock stamp differs"]

    def real():
        t0 = time.perf_counter()
        fresh_nl = compute_nulls()
        x, _ = build(fresh_nl)
        clock(f"F-DET second build (null recomputed): {time.perf_counter() - t0:.1f}s")
        on_disk = DOC.read_bytes()
        ok = x == doc == on_disk
        return (ok, f"a second build from scratch (null recomputed from the ledgers) is "
                    f"byte-identical to the first and to {rel(DOC)}: sha256 {sha256(x)[:16]}… "
                    f"{len(x):,} B" if ok else "second build differs")
    return (lambda: plants([("a wall-clock stamp in the build", clocked)])), real


LEGS = (
    ("F-S2-SLICE", "every spliced block is the digest's bytes, never retyped",
     "any spliced block is not byte-identical to its digest (or R10) span; the header does "
     "not name the digest's full path and on-disk sha256; a label cites a span outside its "
     "source.", leg_slice),
    ("F-S2-PARQUET", "the B.3 POOLED verdict rows = height_toll_verdict.parquet",
     "any printed verdict_pass / ratio_median / edge_net_h20 differs from "
     "height_toll_verdict.parquet on key (lens, scale_kind, asset, era) — ratio / NET beyond "
     "half a unit of the printed digit, verdict at all; a POOLED key is missing, doubled, or a "
     "non-POOLED row is printed.", leg_parquet),
    ("F-S2-ORDER", "the prominent tables come first",
     "outcome-after-event, the acceptance head-to-head and height-vs-toll do not all precede "
     "coverage and F-RF-4 (or any of the five is absent).", leg_order),
    ("F-S2-NULL", "every outcome block has the gaps+order null beside it",
     "an outcome block lacks the gaps+order null beside it — no null table immediately after "
     "it, a table keyed to another block, a missing gaps+order / gaps-only column at H20 or "
     "H100, a row missing, a gaps+order cell not a number, a cell not the close-time "
     "computation, or the null's REAL (n, median) not the block's printed n / median.",
     leg_null),
    ("F-S2-NULL-ANCHOR", "the close-time pooling path is the null build's own",
     "the path does not reproduce every filed POOLED:ALL null_summary row exactly (both "
     "variants, every lens), or its REAL draw differs from the census outcome_grid row of the "
     "same pool.", leg_anchor),
    ("F-S2-PROMOTE", "the data's default is named, nothing is promoted",
     "a named default (H20 or H100) is not the max-NET rule of acceptance_head_to_head.parquet "
     "at its (lens, era, horizon), its NET / n disagree, a cell is left unnamed, it is named "
     "without 'NAMED ONLY: no pin moves', any row's `promoted` is not NOTHING or "
     "`engine_default_after` not UNCHANGED.", leg_promote),
    ("F-S2-COLLAR", "LAW 4 + R1: the 5m retest-hold rows outside tuning stay unprinted",
     "any printed outcome or null row is a 5m retest-hold class outside the tuning era.",
     leg_collar),
    ("F-S2-SIZE", "the naming trip-wire, read from publish_exchange.py",
     "the size exceeds FLAG_BYTES unflagged; the SIZE line misstates the file's bytes, or "
     "FLAG_BYTES / BOX_BYTES as ast.literal_eval reads them from scripts/publish_exchange.py; "
     "a file at or under FLAG_BYTES is flagged.", leg_size),
    ("F-DET", "byte-identical on two builds",
     "a second build from scratch (the null recomputed from the ledgers) differs by one byte "
     "from the first or from the file on disk.", leg_det),
)


def main() -> int:
    want = [a.lower().replace("_", "-") for a in sys.argv[1:]]
    legs = [x for x in LEGS if not want or any(w in x[0].lower() for w in want)]
    pin = D.load_pin()
    say("=" * 78)
    say("TIER-C10 CLOSE · S2 CENSUS-R — Tier-E · A SELECTION, not a result · m logged")
    say("fixtures: break leg first, RED or void")
    say("=" * 78)
    say(f"substrate NAIAD_CACHE_DIR={_ENV} (the frozen snapshot; live cache untouched)")
    say(f"as_of_last_closed_4h {pin['as_of_last_closed_4h']} "
        f"({rel(D.OUT / 'AS_OF_PIN.json')}); no bar is read by this script")
    src = sources_now()
    for s in src.values():
        say(f"source {rel(s.path)} sha256 {s.sha} {len(s.raw):,} B {len(s.lines):,} lines")
    consts = publish_consts()
    say(f"publish_exchange BOX_BYTES {consts['BOX_BYTES']:,} · FLAG_BYTES "
        f"{consts['FLAG_BYTES']:,} (ast.literal_eval of {rel(PUBLISH)})")
    t0 = time.perf_counter()
    nl = compute_nulls()
    clock(f"close-time null pooling: {time.perf_counter() - t0:.1f}s")
    doc, info = build(nl)
    OUT.mkdir(parents=True, exist_ok=True)
    tmp = DOC.with_name(DOC.name + ".tmp")
    tmp.write_bytes(doc)
    os.replace(tmp, DOC)
    say(f"wrote {rel(DOC)} sha256 {sha256(doc)} {len(doc):,} B")
    for lb in labels(doc, src):
        if lb["kind"] == "verb":
            b = expected(lb)
            say(f"  verbatim {lb['src']:20} {len(b):>6,} B sha256 {sha256(b)[:16]} "
                f"[{cat_of(src[DIGEST.name], lb)}] {fmt_spans(lb['spans'])}")
        else:
            say(f"  computed null beside {' · '.join(lb['key'])}")
    CTX.update(doc=doc, info=info, nl=nl, sources=src, consts=consts,
               ver=pd.read_parquet(VERDICT), acc=pd.read_parquet(ACCEPT),
               census=pd.read_parquet(OUTCOME),
               doc_drop_null=build(nl, plant="drop_null")[0],
               doc_collar_off=build(nl, plant="collar_off")[0],
               doc_unflag=build(nl, plant="unflag_over")[0])
    for fid, title, fails_if, mk in legs:
        b, r = mk()
        prove(fid, title, fails_if, b, r)
    say(f"\nTIER-C10 CLOSE census_r FIXTURES: {len(PASSED)}/{len(legs)} GREEN"
        + (f" · FAILED: {FAILED}" if FAILED else ""))
    say("warranty: these lines are true AS OF the substrate and the files named above and of "
        "no other; the corridor advances with the cache [TC6V-a]")
    if not want:                       # a partial run never overwrites the full transcript
        tmp = TRANSCRIPT.with_name(TRANSCRIPT.name + ".tmp")
        tmp.write_text("\n".join(T) + "\n", encoding="utf-8")
        os.replace(tmp, TRANSCRIPT)
        print(f"transcript -> {rel(TRANSCRIPT)}")
    if FAILED:
        print("*** HALT: fixture mismatch. Nothing downstream is trustworthy. ***")
    return 1 if FAILED else 0


if __name__ == "__main__":
    raise SystemExit(main())
